#include "CvGameCoreDLL.h"
#include "RiseFall.h"
#include "CvInfo_GameOption.h"
#include "CoreAI.h"
#include "CvCityAI.h"
#include "CvSelectionGroup.h"
#include "CvDeal.h"
#include "UWAIAgent.h" // advc.104
#include "CvTalkingHeadMessage.h"
#include "CvPopupInfo.h"
#include "CvReplayInfo.h"
#include "CvPlot.h"

using std::wstringstream;
using std::vector;
using std::wstring;
using std::pair; using std::make_pair;
using namespace fmath; // Single-player only, so this is fine.

// advc:
namespace
{
	__inline PlayerTypes getActivePlayer()
	{
		return GC.getGame().getActivePlayer();
	}
}


RiseFall::RiseFall() {

	originalName = NULL;
	reset();
}

RiseFall::~RiseFall() {

	reset();
}

void RiseFall::reset() {

	interludeLength = interludeCountdown = -1;
	selectingCiv = retryingCivSelection = false;
	SAFE_DELETE(originalName);
	for(size_t i = 0; i < chapters.size(); i++)
		SAFE_DELETE(chapters[i]);
	chapters.clear();
	offLimits.clear();
	clearDiploStrings();
	riseScore.reset();
}

void RiseFall::init() {

	// Caller can't tell whether initialization already done
	if(!chapters.empty())
		return;
	CvGame& g = GC.getGame();
	if(g.isGameMultiPlayer()) {
		shutOff(gDLL->getText("TXT_KEY_RF_SINGLEPL_ONLY"));
		return;
	}
	for(int i = 0; i < MAX_TEAMS; i++) {
		CvTeam const& t = GET_TEAM((TeamTypes)i);
		if(t.getNumMembers() > 1) {
			shutOff(gDLL->getText("TXT_KEY_RF_NO_TEAMS"));
			return;
		}
	}
	vector<GameOptionTypes> incompatible;
	incompatible.push_back(GAMEOPTION_SPAH);
	incompatible.push_back(GAMEOPTION_PERMANENT_ALLIANCES);
	incompatible.push_back(GAMEOPTION_ONE_CITY_CHALLENGE);
	for(size_t i = 0; i < incompatible.size(); i++) {
		if(g.isOption(incompatible[i])) {
			shutOff(gDLL->getText("TXT_KEY_RF_INVALID_OPTION",
					GC.getInfo(incompatible[i]).getTextKeyWide()));
			return;
		}
	}
	int maxChapters = GC.getDefineINT("RF_CHAPTERS_BASE");
	CvGameSpeedInfo& speed = GC.getInfo(g.getGameSpeedType());
	double chapterModifier = (speed.getGoldenAgePercent() + 150) / 250.0;
	int startTurn = g.getStartTurn();
	int endTurn = g.getEstimateEndTurn();
	int totalTurns = endTurn - startTurn;
	chapterModifier *= totalTurns / (double)endTurn;
	int civs = g.countCivPlayersAlive();
	{	// If few civs, stick to unmodified maxChapters.
		int maxChaptersModified = ::round(maxChapters * chapterModifier);
		if(maxChaptersModified > maxChapters) {
			int bound = std::max(::round(civs / 1.51), maxChapters);
			maxChapters = std::min(bound, maxChaptersModified);
		}
		else maxChapters = maxChaptersModified;
	}
	maxChapters = std::min(civs, maxChapters);
	if(maxChapters < 1) {
		shutOff(gDLL->getText("TXT_KEY_RF_INVALID_CHAPTERS", maxChapters));
		return;
	}
	interludeLength = GC.getDefineINT("RF_INTERLUDE_LENGTH_BASE");
	interludeLength = ::range(::round((interludeLength * speed.getTrainPercent())
			/ 100.0), std::min(interludeLength, 5), std::max(interludeLength, 10));
	int playLength = totalTurns - (maxChapters - 1) * interludeLength;
	int partialLength = 0;
	for(int i = 0; i < maxChapters - 1; i++) {
		chapters.push_back(new RFChapter(i, maxChapters, playLength));
		partialLength += chapters[i]->getLength();
	}
	int finalChLen = playLength - partialLength;
	bool timeLimit = (g.getMaxTurns() > 0);
	if(!timeLimit)
		finalChLen = -1;
	chapters.push_back(new RFChapter(maxChapters - 1, maxChapters,
			playLength, finalChLen));
	FAssert(chapters.size() == maxChapters);
	if(!chapters.empty() && !timeLimit)
		chapters[chapters.size() - 1]->setEndless(true);
	for(size_t i = 0; i < chapters.size(); i++) {
		int len = chapters[i]->getLength();
		if(len < 10 && !chapters[i]->isEndless()) {
			shutOff(gDLL->getText("TXT_KEY_RF_CHAPTER_TOO_SHORT", (int)i, len));
			return;
		}
	}
	double delayFirst = GC.getDefineINT("RF_SCORING_DELAY_FIRST") / 100.0;
	double delayPenult = GC.getDefineINT("RF_SCORING_DELAY_PENULTIMATE") / 100.0;
	int chapterStart = startTurn;
	for(size_t i = 0; i < chapters.size(); i++) {
		int nextChapterLength = (i >= chapters.size() - 1 ? 0 :
				chapters[i + 1]->getLength());
		if(nextChapterLength <= 0)
			chapters[i]->setDelay(-10000); // For a negative scoreTurn
		else {
			double delayMultiplier = delayPenult;
			if(maxChapters != 2) {
				delayMultiplier = delayFirst + i *
						(delayPenult - delayFirst) / (maxChapters - 2);
			}
			chapters[i]->setDelay(interludeLength + ::range((int)( // Round down
				// Avoid very long delays when chapters are long
				std::min(speed.getGoldenAgePercent(), nextChapterLength) *
				delayMultiplier) + 1,
				5, nextChapterLength - 5));
		}
		chapters[i]->setStartTurn(chapterStart);
		chapterStart += chapters[i]->getLength() + interludeLength;
	}
	FAssert(chapterStart - interludeLength == endTurn || !timeLimit);
	chapters[0]->setCiv(getActivePlayer());
	chapters[0]->start();
	originalName = new CvWString(GC.getInitCore().getLeaderName(chapters[0]->getCiv()));
	setPlayerName();
	/*  When the EXE calls CvGameTextMgr::getTurnTimerText on turn 0,
		RiseFall isn't initialized yet. Refresh the timer now that
		initialization is through. */
	gDLL->UI().setDirty(TurnTimer_DIRTY_BIT, true);
	/*  Initial auto-save. Normally happens already in CvGame::update, but
		RiseFall isn't yet initialized then. */
	g.autoSave(true);
	g.showDawnOfMan();
}

// Needs to happen earlier than init, hence a separate public function.
void RiseFall::setPlayerHandicap(PlayerTypes civId, bool bHuman, bool bIncrease) {

	HandicapTypes const eGameHandicap = GC.getGame().getHandicapType();
	int iAdjust = (!bIncrease ? 0 :
			range(GC.getDefineINT(CvGlobals::RF_PLAYER_HANDICAP_ADJUSTMENT),
			-eGameHandicap, GC.getNumHandicapInfos() - eGameHandicap - 1));
	GC.getInitCore().setHandicap(civId, (HandicapTypes)(bHuman ?
			eGameHandicap + iAdjust : GC.getGame().getAIHandicap() + iAdjust));
	/*	(Caller will have to call CvGame::updateAIHandicap if several AI player
		handicaps are changed, i.e. if the avg. handicap may have changed.) */
	CvPlayerAI& kCiv = GET_PLAYER(civId);
	kCiv.updateMaintenance();
	kCiv.AI_makeAssignWorkDirty();
	// (Further updates might be warranted)
}

void RiseFall::write(FDataStreamBase* pStream) {

	int savegameVersion = 1; // For later changes that may break compatibility
	pStream->Write(savegameVersion);
	bool origNameGiven = (originalName != NULL);
	pStream->Write(origNameGiven);
	if(origNameGiven)
		pStream->WriteString(originalName->c_str());
	pStream->Write(interludeLength);
	pStream->Write(interludeCountdown);
	pStream->Write((int)offLimits.size());
	for(std::set<TeamTypes>::const_iterator it = offLimits.begin();
			it != offLimits.end(); ++it)
		pStream->Write(*it);
	pStream->Write((int)chapters.size());
	for(size_t i = 0; i < chapters.size(); i++)
		chapters[i]->write(pStream);
	riseScore.write(pStream);
}

void RiseFall::read(FDataStreamBase* pStream) {

	reset();
	int savegameVersion = -1;
	pStream->Read(&savegameVersion);
	if(savegameVersion >= 1) { // else leave it as NULL
		bool origNameGiven = false;
		pStream->Read(&origNameGiven);
		if(origNameGiven) {
			wchar* tmp = pStream->ReadWideString();
			originalName = new CvWString(tmp);
			delete tmp;
		}
	}
	pStream->Read(&interludeLength);
	pStream->Read(&interludeCountdown);
	int sz = -1;
	pStream->Read(&sz);
	for(int i = 0; i < sz; i++) {
		int tId = -1;
		pStream->Read(&tId);
		offLimits.insert((TeamTypes)tId);
	}
	pStream->Read(&sz);
	for(int i = 0; i < sz; i++) {
		chapters.push_back(new RFChapter());
		chapters[i]->read(pStream);
	}
	// E.g. CvPlot::m_bAllFog not saved
	FAssertMsg(interludeCountdown < 0, "Mustn't load into interlude");
	riseScore.read(pStream);
}

int RiseFall::getInterludeCountdown() const {

	return interludeCountdown;
}

void RiseFall::reportElimination(PlayerTypes civId) {

	int pos = getCurrentChapter();
	if(pos < 0)
		return;
	if(pos > 0 && chapters[pos - 1]->getCiv() == civId)
		chapters[pos - 1]->score();
	if(chapters[pos]->getCiv() == civId) {
		chapters[pos]->score();
		setPlayerControl(civId, false);
		CvPlayer& nextAlive = GET_PLAYER(nextCivAlive(BARBARIAN_PLAYER));
		if(pos < (int)(chapters.size() - 1)) {
			GC.getGame().setActivePlayer(nextAlive.getID());
			nextAlive.setIsHuman(true);
			nextAlive.setNetID(0);
			CvPopupInfo* popup = new CvPopupInfo(BUTTONPOPUP_RF_DEFEAT);
			// So that launchDefeatPopup knows which chapter we've just scored (ended)
			popup->setData1(pos);
			nextAlive.addPopup(popup, true);
		}
		else {
			setPlayerControl(nextAlive.getID(), true);
			if(originalName != NULL)
				GC.getInitCore().setLeaderName(nextAlive.getID(), *originalName);
			FAssert(GC.getGame().countHumanPlayersAlive() > 0);
			// End the game directly when defeated in the final chapter
			GC.getGame().setGameState(GAMESTATE_OVER);
		}
	}
}

void RiseFall::retire() {

	int pos = getCurrentChapter();
	if(pos < 0)
		return;
	int t = getRetireTurns();
	if(t <= 0)
		return;
	CvGame& g = GC.getGame();
	if(chapters[pos]->getRetireTurn() < 0) // Don't store multiple timestamps
		chapters[pos]->setRetireTurn(g.getGameTurn());
	g.setAIAutoPlay(t);
	/*  Don't do this. CvPlayer not yet loaded. No need either - plans already
		abandoned at start of retirement. */
	//abandonPlans(chapters[pos]->getCiv());
}

int RiseFall::getRetireTurns() const {

	int pos = getCurrentChapter();
	if(pos < 0)
		return 0;
	return chapters[pos]->getEndTurn() - GC.getGame().getGameTurn() + 1;
}

bool RiseFall::hasRetired() const {

	int pos = getCurrentChapter();
	if(pos < 0)
		return false;
	int t = chapters[pos]->getRetireTurn();
	return t >= 0 && t <= GC.getGame().getGameTurn();
}

int RiseFall::getAutoPlayCountdown() const {

	if(isSelectingCiv()) /* Not sure if needed; be sure we're not showing
							a countdown while the popup is open. */
		return 0;
	PlayerTypes activePl = getActivePlayer();
	if(activePl == NO_PLAYER) {
		FAssert(activePl != NO_PLAYER);
		return -1;
	}
	CvPlayer const& pl = GET_PLAYER(activePl);
	if(pl.isHuman() && !pl.isHumanDisabled()) // Normal play
		return 0;
	if(hasRetired() && pl.isHumanDisabled()) {
		int r = GC.getGame().getAIAutoPlay();
		if(interludeCountdown < 0) // Anticipate interlude
			r += interludeLength;
		else r += interludeCountdown;
		return r + 1; // +1 for the turn of retirement
	}
	// +1 for the turn on which the chapter is ended
	return std::max(0, interludeCountdown + 1);
}

void RiseFall::atTurnEnd(PlayerTypes civId) {

	/*  Would rather get a call right before the turn of a civ begins, but can't
		find this in the DLL code; only for civ 0 (atActiveTurnStart). */
	CvGame& g = GC.getGame();
	if(g.getGameState() == GAMESTATE_EXTENDED)
		return;
	int gameTurn = g.getGameTurn();
	// The chapter of civ 0 needs to be started at the end of the previous game turn
	if(civId == BARBARIAN_PLAYER)
		gameTurn++;
	/*  Conduct scoring exactly as scheduled at the end of a turn of the
		civ being scored; show the score popup at the start of the next
		active player turn. */
	for(size_t i = 0; i < chapters.size(); i++) {
		if(chapters[i]->getCiv() == civId &&
				chapters[i]->getScoreTurn() == gameTurn)
			chapters[i]->score();
	}
	int currentChPos = getCurrentChapter();
	if(currentChPos < 0 || currentChPos >= (int)chapters.size()) {
		FAssertMsg(currentChPos < 0 || interludeCountdown < 0, "Interlude past final chapter");
		return;
	}
	RFChapter& currentCh = *chapters[currentChPos];
	PlayerTypes nextCivId = nextCivAlive(civId);
	if(nextCivId == currentCh.getCiv()) {
		if(nextCivId != getActivePlayer()) {
			if(GET_PLAYER(nextCivId).isAlive()) {
				setPlayerControl(nextCivId, true);
				interludeCountdown = -1;
				/*  Don't start a chapter across a game turn (i.e. during the
					barbs' turn). Switching to civ 0 is handled by atGameTurnStart. */
				if(nextCivId != (PlayerTypes)0)
					currentCh.start();
			}
			else if(!currentCh.isScored()) { /*  If scored, then defeat happened
				after starting the chapter, and normal civ selection is coming up.
				Otherwise, nextCiv has died in between selection and chapter start. */
				retryingCivSelection = true;
				haltForCivSelection(nextCivAlive(nextCivId));
			}
		}
	}
	if(gameTurn == currentCh.getEndTurn() && civId == currentCh.getCiv()) {
		currentCh.setScoreAtEnd(currentCh.computeScore());
		// Even if interludeLength is 0, parts of a round need to be skipped
		interludeCountdown = interludeLength;
		g.setAIAutoPlay(0); // In case that the player has retired
		setPlayerControl(currentCh.getCiv(), false);
		abandonPlans(currentCh.getCiv());
		CvWString replayText = gDLL->getText("TXT_KEY_RF_INTERLUDE_STARTED");
		g.addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, getActivePlayer(),
				replayText, GC.getColorType("HIGHLIGHT_TEXT"));
	}
}

void RiseFall::atGameTurnStart() {

	CvGame const& g = GC.getGame();
	int currentChPos = getCurrentChapter();
	if(currentChPos < 0 || interludeCountdown > 0) {
		interludeCountdown--;
		/*  I'd like to keep the camera in one place during interlude, but this
			only turns into a tug of war when the player moves the camera. */
		//centerCamera(getActivePlayer());
		return;
	}
	int gameTurn = g.getGameTurn();
	RFChapter& currentCh = *chapters[currentChPos];
	if(currentCh.getStartTurn() >= gameTurn) {
		FAssert(currentCh.getStartTurn() == gameTurn);
		if(currentCh.getCiv() == NO_PLAYER)
			haltForCivSelection(nextCivAlive(BARBARIAN_PLAYER));
	}
}

void RiseFall::atActiveTurnStart() {

	int pos = getCurrentChapter();
	if(pos < 0)
		return; // Happens on turn 0 b/c not yet initialized
	CvGame& g = GC.getGame();
	int gameTurn = g.getGameTurn();
	PlayerTypes activeId = getActivePlayer();
	if(activeId == NO_PLAYER)
		return;
	CvPlayerAI& active = GET_PLAYER(activeId);
	RFChapter& currentCh = *chapters[pos];
	if(currentCh.getCiv() != activeId)
		return;
	if(gameTurn == currentCh.getStartTurn() && pos > 0)
		welcomeToNextChapter(pos);
	g.autoSave();
	if(active.isHumanDisabled()) // Only popups from here
		return;
	updateOffLimits(); /* Any civ that is a vassal of ActiveTeam at some point
						  becomes ineligible for the next chapter */
	for(size_t i = 0; i < chapters.size(); i++) {
		if(chapters[i]->isScored() && !chapters[i]->isScoreShown()) {
			CvPopupInfo* popup = new CvPopupInfo(BUTTONPOPUP_TEXT);
			CvWString text;
			wchar const* civDescr = GET_PLAYER(chapters[i]->getCiv()).
					getCivilizationShortDescription();
			if(GET_PLAYER(chapters[i]->getCiv()).isAlive())
				text = gDLL->getText("TXT_KEY_RF_POPUP_SCORE", i + 1, civDescr);
			else text = gDLL->getText("TXT_KEY_RF_POPUP_SCORE_EARLY",  i + 1, civDescr);
			text.append(L":\n\n" +
					*chapters[i]->computeScoreBreakdown().getString());
			popup->setText(text);
			gDLL->UI().addPopup(popup, activeId);
			chapters[i]->setScoreShown(true);
		}
	}
	if(pos < ((int)chapters.size()) - 1 &&
			gameTurn == currentCh.getEndTurn() &&
			GC.getDefineINT("RF_ENABLE_FINAL_TURN_POPUP") > 0) {
		CvPopupInfo* popup = new CvPopupInfo(BUTTONPOPUP_TEXT);
		CvWString text = gDLL->getText("TXT_KEY_RF_POPUP_FINAL_TURN",
				pos + 1);
		if(interludeLength > 0)
			text.append(gDLL->getText("TXT_KEY_RF_POPUP_AUTO_PLAY",
					pos + 2, interludeLength));
		popup->setText(text);
		gDLL->UI().addPopup(popup, activeId);
	}
	vector<PlayerTypes> eligible;
	computeEligibleCivs(eligible, false);
	// Recommend retirement when top rank reached and not near victory
	if(pos > 0 && pos < ((int)chapters.size()) - 2 &&
			!chapters[pos]->wasRetireRecommended() &&
			!(((int)eligible.size()) > 1) && g.getPlayerRank(activeId) == 0 &&
			!active.AI_atVictoryStage3()) {
		RFChapterScore const& sc = chapters[pos]->computeScoreBreakdown();
		if(sc.getScore() >= 50 && sc.getScoreFromRemainingTime() >= 10 &&
				sc.getInitialRank() >= 3) {
			CvPopupInfo* popup = new CvPopupInfo(BUTTONPOPUP_TEXT);
			CvWString text = gDLL->getText("TXT_KEY_RF_POPUP_RECOMMEND_RETIRE",
					active.getCivilizationShortDescription());
			popup->setText(text);
			gDLL->UI().addPopup(popup, activeId);
			chapters[pos]->setRetireWasRecommended(true);
		}
	}
}

void RiseFall::setPlayerControl(PlayerTypes civId, bool b) {

	CvGame& g = GC.getGame();
	PlayerTypes formerHumanCiv = getActivePlayer();
	if(formerHumanCiv != NO_PLAYER && !GET_PLAYER(formerHumanCiv).isHuman())
		formerHumanCiv = NO_PLAYER;
	CvPlayer& civ = GET_PLAYER(civId);
	if(!b || !civ.isHuman()) // Unless human control continues
		gDLL->UI().clearQueuedPopups();
	setPlayerHandicap(civId, b, /* increase only human handicap here */ b);
	if(b)
		g.changeHumanPlayer(civId);
	else {
		civ.setNetID(-1);
		civ.setIsHuman(false, true);
		GC.getInitCore().setLeaderName(civId,
				GC.getInfo(civ.getLeaderType()).getDescription());
		gDLL->UI().flushTalkingHeadMessages();
		gDLL->UI().clearEventMessages();
		gDLL->UI().clearSelectedCities();
		gDLL->UI().clearSelectionList();
	}
	// (Un)fog the map
	if(b || !g.isDebugMode()) {
		CvPlot::setAllFog(!b);
		if(!b)
			g.updateActiveVisibility();
		setUIHidden(!b);
	}
	if (b) // (Otherwise CvPlayer::setIsHuman has already updated the full attitude cache)
	{
		for(int i = 0; i < MAX_CIV_PLAYERS; i++) {
			CvPlayerAI& other = GET_PLAYER((PlayerTypes)i);
			if(!other.isAlive() || other.isMinorCiv())
				continue;
			if(other.getID() != civId && GET_TEAM(civId).isHasMet(other.getTeam()))
				other.AI_updateAttitude(civId);
			if(formerHumanCiv != NO_PLAYER && civId != formerHumanCiv &&
					other.getID() != formerHumanCiv && GET_TEAM(formerHumanCiv).
					isHasMet(other.getTeam()))
				other.AI_updateAttitude(formerHumanCiv);
		}
	}
	if(b) { // Updates to apply human modifiers
		civ.updateWarWearinessPercentAnger();
		FOR_EACH_CITY_VAR(c, civ)
			c->updateMaintenance();
	}
}

void RiseFall::setUIHidden(bool b) {

	if(gDLL->UI().isBareMapMode() != b)
		gDLL->UI().toggleBareMapMode();
	/*  toggleScoresVisible(): Isn't actually hidden b/c CvMainInterface.py doesn't
		update itself during interlude.
		toggleTurnLog(): Can't check if it's open. */
	gDLL->UI().setDiplomacyLocked(b);
}

void RiseFall::setPlayerName() {

	PlayerTypes activeCiv = getActivePlayer();
	CvWString newName = GC.getInfo(GET_PLAYER(activeCiv).getLeaderType()).getDescription();
	/*  Must only use characters that are allowed in file names; otherwise,
		no replay file gets created for the HoF. */
	newName += L"'";
	GC.getInitCore().setLeaderName(activeCiv, newName);
	int pos = getCurrentChapter();
	if(pos >= 0) {
		CvWString replayText = gDLL->getText("TXT_KEY_RF_REPLAY_NEXT_CHAPTER",
				pos + 1, GET_PLAYER(activeCiv).getReplayName());
		GC.getGame().addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, activeCiv, replayText,
				GC.getColorType("HIGHLIGHT_TEXT"));
	}
}

void RiseFall::welcomeToNextChapter(int pos) {

	FAssert(pos > 0);
	/*  Message about revolution from the turn before human takeover lingers
		for some reason (and perhaps other messages too). Player will have to
		check the Event Log anyway, so let's just clear the screen. */
	gDLL->UI().clearEventMessages();
	RFChapter& ch = *chapters[pos];
	setPlayerName();
	CvPlayer& p = GET_PLAYER(ch.getCiv());
	/*	Wrong net ids can, apparently, mess with the diplo screen, making it
		impossible to add certain items to the table. It's probably sufficient
		to set the proper ids here, but I try to keep them up to date at all
		times. Would be nice to let CvPlayer::setIsHuman handle that, but that
		may not work in multiplayer modes and would break the net id update in
		CvGame::setActivePlayer. */
	FOR_EACH_ENUM(Player)
		GET_PLAYER(eLoopPlayer).setNetID(-1);
	p.setNetID(0);
	p.verifyCivics();
	resetProductionDecay(p.getID());
	// Doing this in setUIHidden has no effect
	GC.getGame().setGlobeView(false);
	centerCamera(p.getID());
	abandonPlans(p.getID()); // Also tries to move the camera
	GC.getGame().showDawnOfMan();
	showDoW();
	showQuests();
	offLimits.clear();
	updateOffLimits();
}

void RiseFall::resetProductionDecay(PlayerTypes civId) {

	/*	Production decay affects only humans, so the AI ignores it.
		Don't want human to suffer for that after assuming control.
		Well, mainly, I don't want humans to be distracted by (BULL) decay warnings.
		I'm setting the accumulated production to 0 iff decay has already started.
		Either way, the decay timer gets reset to 0. */
	int iBuildingThresh = GC.getDefineINT(CvGlobals::BUILDING_PRODUCTION_DECAY_TIME) *
			GC.getInfo(GC.getGame().getGameSpeedType()).getConstructPercent();
	int iUnitThresh = GC.getDefineINT(CvGlobals::UNIT_PRODUCTION_DECAY_TIME) *
			GC.getInfo(GC.getGame().getGameSpeedType()).getTrainPercent();
	FOR_EACH_CITY_VAR(pCity, GET_PLAYER(civId)) {
		FOR_EACH_ENUM(Building) {
			if (pCity->getBuildingProduction(eLoopBuilding) <= 0)
				continue;
			if (pCity->getBuildingProductionTime(eLoopBuilding) * 100 > iBuildingThresh)
				pCity->setBuildingProduction(eLoopBuilding, 0);
			pCity->setBuildingProductionTime(eLoopBuilding, 0);
		}
		FOR_EACH_ENUM(Unit) {
			if (pCity->getUnitProduction(eLoopUnit) <= 0)
				continue;
			if (pCity->getUnitProductionTime(eLoopUnit) * 100 > iUnitThresh)
				pCity->setUnitProduction(eLoopUnit, 0);
			pCity->setUnitProductionTime(eLoopUnit, 0);
		}
	}
}

void RiseFall::centerCamera(PlayerTypes civId) {

	if(GET_PLAYER(civId).hasCapital()) {
		/*  Apparently, this has no effect, at least not at the time that I call
			this function. Misplaced camera is also an issue when regenerating
			the map or using Civ Changer (Alt+Z); perhaps can't be fixed. */
		gDLL->UI().lookAt(GET_PLAYER(civId).getCapital()->getPlot().getPoint(),
				CAMERALOOKAT_NORMAL);
		// This doesn't seem to help either:
		/*NiPoint3 p3 = capitalPlot->getPoint();
		gDLL->getEngineIFace()->ClampToWorldCoords(&p3);*/
	}
}

void RiseFall::showDoW() {

	CvTeamAI& activeTeam = GET_TEAM(GC.getGame().getActiveTeam());
	/*  Would be nicer to show e.g. "Alexander has declared war on you in 1923",
		but would have to track additional info for this, or piece it together
		from past messages. Both too much work. */
	for(int i = 0; i < MAX_CIV_PLAYERS; i++) {
		CvPlayer& enemy = GET_PLAYER((PlayerTypes)i);
		if(!enemy.isAlive() || enemy.isMinorCiv() || !activeTeam.isAtWar(enemy.getTeam()))
			continue;
		gDLL->UI().addMessage(getActivePlayer(), true, -1, gDLL->getText("TXT_KEY_YOU_AT_WAR",
				enemy.getName()), NULL, MESSAGE_TYPE_INFO, NULL, GC.getColorType("WARNING_TEXT"),
				// advc.127b:
				enemy.getCapitalX(activeTeam.getID(), true), enemy.getCapitalY(activeTeam.getID(), true));
	}
}

void RiseFall::showQuests() {

	CvPlayer& p = GET_PLAYER(getActivePlayer());
	CvMessageQueue const& archive = p.getGameMessages();
	for(std::list<CvTalkingHeadMessage>::const_iterator it = archive.begin();
			it != archive.end(); ++it) {
		// CvPlayer::expireEvent should ensure that only ongoing quests are listed
		if(it->getMessageType() == MESSAGE_TYPE_QUEST) {
			gDLL->UI().addMessage(p.getID(), true, -1, gDLL->getText("TXT_KEY_GOT_QUESTS"),
					NULL, MESSAGE_TYPE_INFO, NULL);
			return;
		}
	}
}

void RiseFall::abandonPlans(PlayerTypes civId) {

	CvPlayerAI& civ = GET_PLAYER(civId);
	bool active = (civId == getActivePlayer() && civ.isHuman());
	FOR_EACH_GROUP_VAR(gr, civ)
		gr->splitGroup(1);
	CvCity* capital = civ.getCapital();
	bool unitSelected = false;
	FOR_EACH_GROUP_VAR(gr, civ) {
		if(gr->getHeadUnit() == NULL)
			continue;
		gr->setAutomateType(NO_AUTOMATE);
		// Remove all but the current mission
		while(gr->headMissionQueueNode() != NULL &&
				gr->nextMissionQueueNode(gr->headMissionQueueNode()) != NULL)
			gr->deleteMissionQueueNode(gr->nextMissionQueueNode(gr->headMissionQueueNode()));
		/*  If it's not a BUILD mission, remove the current mission too. Also
			remove MISSION_ROUTE_TO b/c it's not really just a single mission. */
		if(gr->getActivityType() != ACTIVITY_MISSION ||
				gr->getMissionType(0) != MISSION_BUILD) {
			gr->setActivityType(ACTIVITY_AWAKE);
			gr->clearMissionQueue();
			if(!active)
				continue;
		}
		// Not really the job of this function, but while we're at it:
		if(!unitSelected && capital != NULL && gr->atPlot(capital->plot())) {
			gDLL->UI().selectGroup(gr->getHeadUnit(),
					false, false, false);
			unitSelected = true;
			gDLL->UI().lookAtSelectionPlot();
		}
		// Without this, units outside owner's borders don't appear on the main interface.
		if(gr->plot()->getOwner() != civId)
			gr->plot()->updateCenterUnit();
		/* ^Perhaps no longer needed due to a change in CvPlot::updateVisibility
			(advc.061). Should test this some time. */
	}
	// Set research slider to a balanced-budget position
	int incr = GC.getDefineINT("COMMERCE_PERCENT_CHANGE_INCREMENTS");
	civ.setCommercePercent(COMMERCE_RESEARCH, 100);
	while(civ.calculateGoldRate() < 0 && civ.getCommercePercent(COMMERCE_RESEARCH) > 9)
		civ.setCommercePercent(COMMERCE_RESEARCH,
				civ.getCommercePercent(COMMERCE_RESEARCH) - incr);
	// 0 espionage weight
	for(int i = 0; i < MAX_CIV_TEAMS; i++)
		civ.setEspionageSpendingWeightAgainstTeam((TeamTypes)i, 0);
	// Clear research queue
	TechTypes currentTech = civ.getCurrentResearch();
	if(currentTech == NO_TECH)
		civ.clearResearchQueue();
	else civ.pushResearch(currentTech, true);
	FOR_EACH_CITYAI_VAR(c, civ) {
		// Turn off production emphasis. AvoidGrowth is also a type of emphasis.
		for(int i = 0; i < GC.getNumEmphasizeInfos(); i++)
			c->AI_setEmphasize((EmphasizeTypes)i, false);
		// Clear production queue
		c->setProductionAutomated(false, true);
		c->setCitizensAutomated(true);
	}
}

int RiseFall::getMaxChapters() const {

	return chapters.size();
}

RFChapter& RiseFall::getChapter(int i) const {

	FAssert(i >= 0 && i < (int)chapters.size());
	return *chapters[i];
}

wstring* RiseFall::chapterScoreBreakdown() {

	int pos = getCurrentChapter();
	if(pos < 0)
		return NULL;
	return chapters[pos]->computeScoreBreakdown().getString();
}

wstring* RiseFall::riseScoreBreakdown() {

	riseScore.update(chapters);
	return riseScore.getString();
}

int RiseFall::getCurrentChapter() const {

	for(size_t i = 0; i < chapters.size(); i++)
		if(chapters[i]->isOngoing())
			return i;
	return -1;
}

pair<int,int> RiseFall::getChapterCountdown() const {

	int chIndex = getCurrentChapter();
	int r1 = -1, r2 = -1;
	if(chIndex >= 0) {
		RFChapter const& ch = *chapters[chIndex];
		// Start at 1
		r1 = GC.getGame().getGameTurn() - ch.getStartTurn() + 1;
		r2 = ch.getLength();
	}
	return make_pair(r1, r2);
}

bool RiseFall::isBlockPopups() const {

	int pos = getCurrentChapter();
	if(pos < 1)
		return false;
	/*  Since the AI chooses the production of all cities before the player
		gets to take over, there shouldn't be a reason to show a choose-
		production popup during the initial turn of a chapter.
		Conceivable exception: The player conquers a city on the initial turn,
		and there is no disorder because the city was formerly owned. I guess
		in this case, the player won't be prompted to choose production, which
		is bad, but rare and won't crash the game.

		I'm now also using this function for tech-choice popups, contact by
		the AI and Civ4lerts. */
	return chapters[pos]->getStartTurn() == GC.getGame().getGameTurn();
}

bool RiseFall::isDeliverMessages(PlayerTypes civId) const {

	// False if civId not human and human takeover of civId impossible
	if(civId == NO_PLAYER || civId == BARBARIAN_PLAYER ||
			GET_PLAYER(civId).isMinorCiv())
		return false;
	// Don't accommodate civs getting played more than once
	for(size_t i = 0; i < chapters.size(); i++)
		if(chapters[i]->hasEnded() && chapters[i]->getCiv() == civId)
			return false;
	// First player civ not in slot 0; initialization not yet done.
	if(chapters.empty())
		return true;
	// Can't switch after the final chapter
	int pos = getCurrentChapter();
	if(pos == chapters.size() - 1)
		return chapters[pos]->getCiv() == civId;
	return true;
}

bool RiseFall::isCooperationRestricted(PlayerTypes aiCiv) const {

	PlayerTypes masterId = GET_TEAM(GET_PLAYER(aiCiv).getMasterTeam()).getLeaderID();
	if(masterId != aiCiv)
		return isCooperationRestricted(masterId);
	PlayerTypes human = getActivePlayer();
	if(aiCiv == human)
		return false;
	int currentChPos = getCurrentChapter();
	if(currentChPos < 0)
		return false;
	RFChapter const& currentCh = *chapters[currentChPos];
	if(currentCh.isFinalChapter()) {
		if(currentCh.isEndless()) // Game already ended
			return false;
		// Only civ still to be scored: the one from the previous chapter
		PlayerTypes prevChCiv = NO_PLAYER;
		if(currentChPos > 0)
			prevChCiv = chapters[currentChPos - 1]->getCiv();
		return prevChCiv == aiCiv;
	}
	for(int i = 0; i <= currentChPos; i++)
		if(chapters[i]->getCiv() == aiCiv)
			return !chapters[i]->isScored();
	CvGame const& g = GC.getGame();
	int aiVictStage = victoryStage(aiCiv);
	/*if(aiVictStage >= 4)
		return true; */
	int humanVictStage = victoryStage(human);
	if(aiVictStage < 3)
		aiVictStage = 0;
	if(humanVictStage < 3)
		humanVictStage = 0;
	if(aiVictStage != humanVictStage)
		return (aiVictStage < humanVictStage);
	return (g.getPlayerRank(aiCiv) > g.getPlayerRank(human));
}

// currently unused
RFChapter* RiseFall::mostRecentlyFinished() const {

	for(size_t i = chapters.size() - 1; i >= 0; i--) {
		if(chapters[i]->hasEnded())
			return chapters[i];
	}
	return NULL;
}

void RiseFall::computeEligibleCivs(vector<PlayerTypes>& r, bool allowRepeat) const {

	for(int i = 0; i < MAX_CIV_PLAYERS; i++) {
		PlayerTypes civId = (PlayerTypes)i;
		if(isEligible(civId, allowRepeat))
			r.push_back(civId);
	}
}

bool RiseFall::isEligible(PlayerTypes civId, bool allowRepeat) const {

	CvPlayer const& civ = GET_PLAYER(civId);
	if(!civ.isAlive() || civ.isMinorCiv() || offLimits.count(civ.getTeam()) > 0)
		return false;
	for(size_t i = 0; i < chapters.size(); i++) {
		if(chapters[i]->getCiv() != civId)
			continue;
		if(chapters[i]->hasEnded()) {
			if(allowRepeat)
				return chapters[i]->isScored();
			return false;
		}
	}
	return true;
}

void RiseFall::updateOffLimits() {

	for(int i = 0; i < MAX_CIV_TEAMS; i++) {
		CvTeam& t = GET_TEAM((TeamTypes)i);
		if(t.isAlive() && t.isVassal(GC.getGame().getActiveTeam()))
			offLimits.insert(t.getID());
	}
}

void RiseFall::haltForCivSelection(PlayerTypes haltCiv) {

	CvGame& g = GC.getGame();
	/*  Set to active human for a moment, just to get the civ selection
		popup through. Reset to AI-control in handleCivSelection. */
	CvPlayer& h = GET_PLAYER(haltCiv);
	GET_PLAYER(getActivePlayer()).setNetID(-1);
	/*	(bForceHotSeat would take care of the net id, but would also show a
		"you now control such-and-such" popup.) */
	g.setActivePlayer(haltCiv);
	GET_PLAYER(haltCiv).setNetID(0);
	h.setIsHuman(true);
	CvPopupInfo* popup = new CvPopupInfo(BUTTONPOPUP_RF_CHOOSECIV);
	h.addPopup(popup, true);
	selectingCiv = true;
}

PlayerTypes RiseFall::nextCivAlive(PlayerTypes startExcluded) const {

	int r = (startExcluded + 1) % MAX_PLAYERS;
	while(!GET_PLAYER((PlayerTypes)r).isAlive() && r != startExcluded)
		r = (r + 1) % MAX_PLAYERS;
	if(r == startExcluded)
		return NO_PLAYER;
	FAssert(startExcluded == BARBARIAN_PLAYER || startExcluded < r || r == BARBARIAN_PLAYER);
	return (PlayerTypes)r;
}

void RiseFall::prepareForExtendedGame() {

	CvGame& g = GC.getGame();
	int pos = getCurrentChapter();
	if(pos < 0) {
		/*  Score the latest chapter to avoid confusion about whether it is
			covered by the points from "unscored finished" */
		for(size_t i = chapters.size() - 1; i >= 0; i--) {
			if(chapters[i]->hasStarted()) {
				chapters[i]->score();
				break;
			}
		}
		riseScore.freezeTotal(chapters);
		/*  Show the latest started chapter as endless, but will actually remain
			in between chapters indefinitely. */
		for(size_t i = chapters.size() - 1; i >= 0; i--) {
			if(chapters[i]->hasStarted()) {
				chapters[i]->setEndless(true);
				break;
			}
		}
		TeamTypes winnerId = g.getWinner();
		if(winnerId == NO_TEAM) // Can this be?
			winnerId = (TeamTypes)0;
		// Try to avoid giving the player control of the winner b/c it's confusing
		PlayerTypes haltId = nextCivAlive(GET_TEAM(winnerId).getLeaderID());
		if(haltId == NO_PLAYER)
			haltId = GET_TEAM(winnerId).getLeaderID();
		setPlayerControl(haltId, true);
		interludeCountdown = -1;
		/*  Don't want the player to be addressed by the name of an arbitray civ
			on the Dan Quayle screen; restore the original player name. */
		if(originalName != NULL)
			GC.getInitCore().setLeaderName(haltId, *originalName);
	}
	else if(interludeCountdown < 0) {
		// Score the current chapter b/c it's not counted under finished unscored
		if(g.getWinner() != TEAMID(chapters[pos]->getCiv()))
			chapters[pos]->score();
		riseScore.freezeTotal(chapters);
		chapters[pos]->setEndless(true);
		/*  So that the game end turn gets shown as the score turn. The popup
			that switches to extended game appears one turn after victory. */
		chapters[pos]->setScored(GC.getGame().getGameTurn() - 1);
		if(g.getAIAutoPlay()) {
			abandonPlans(chapters[pos]->getCiv());
			g.setAIAutoPlay(0);
		}
	}
	else {
		PlayerTypes civId = chapters[pos]->getCiv();
		if(civId == NO_PLAYER)
			civId = nextCivAlive(civId);
		// Come back from retirement
		riseScore.freezeTotal(chapters);
		setPlayerControl(civId, true);
		interludeCountdown = -1;
	}
	// Player needs to be in control for the game end sequence
	FAssert(interludeCountdown < 0);
	FAssert(GET_PLAYER(getActivePlayer()).isHuman());
	FAssert(!GET_PLAYER(getActivePlayer()).isHumanDisabled());
}

int RiseFall::getFinalRiseScore() const {

	return riseScore.getScore();
}

int RiseFall::getNormalizedFinalScore() const {

	return riseScore.getNormalizedScore();
}

bool RiseFall::launchDefeatPopup(CvPopup* popup, CvPopupInfo& info) {

	int startTurn = 0;
	int pos = info.getData1();
	if(pos >= 0 && pos < (int)(chapters.size() - 1))
		startTurn = chapters[pos + 1]->getStartTurn();
	else FAssert(false);
	CvWString text = gDLL->getText("TXT_KEY_MISC_DEFEAT") + L"\n\n";
	text += gDLL->getText("TXT_KEY_RF_DEFEAT", startTurn, startTurn -
			GC.getGame().getGameTurn());
	gDLL->UI().popupSetBodyString(popup, text);
	gDLL->UI().popupAddGenericButton(popup,
			gDLL->getText("TXT_KEY_POPUP_EXIT_TO_MAIN_MENU"), NULL,
			1, WIDGET_GENERAL);
	gDLL->UI().popupLaunch(popup);
	return true;
}

void RiseFall::handleDefeatPopup(int buttonClicked, int pos) {

	if(buttonClicked == 1) {
		setUIHidden(false);
		CvPlot::setAllFog(false);
		GC.getGame().exitToMenu();
		return;
	}
	if(pos < 0 || pos >= (int)(chapters.size() - 1)) {
		FAssert(false);
		pos = -1;
	}
	// -1: Current turn already passed
	interludeCountdown = chapters[pos + 1]->getStartTurn() - GC.getGame().getGameTurn() - 1;
	FAssert(interludeCountdown >= 0);
	CvPlayer& h = GET_PLAYER(getActivePlayer());
	h.setNetID(-1);
	h.setIsHuman(false);
}

bool RiseFall::launchCivSelectionPopup(CvPopup* popup, CvPopupInfo& info) {

	vector<PlayerTypes> eligible;
	eligibleByRecommendation(eligible);
	int pos = getCurrentChapter();
	// Don't show the popup again when loading the auto-save created at chapter start
	if(pos >= 0 && chapters[pos]->getCiv() != NO_PLAYER)
		return false;
	if(eligible.empty()) {
		CvWString text = gDLL->getText("TXT_KEY_RF_CIV_SELECTION_EMPTY", pos + 1);
		/*  The handler for this "skip chapter" button isn't properly implemented
			See comment in afterCivSelection. */
		/*text += L" " + gDLL->getText("TXT_KEY_RF_CIV_SELECTION_EMPTY2");
		if(pos >= 0 && !chapters[pos]->isScored())
			text += L" " + gDLL->getText("TXT_KEY_RF_CIV_SELECTION_UNSCORED", pos);
		gDLL->UI().popupSetBodyString(popup, text);
		gDLL->UI().popupAddGenericButton(popup,
				gDLL->getText("TXT_KEY_RF_SKIP_CHAPTER", pos + 1,
				chapters[pos]->getLength() + interludeLength), NULL,
				1, WIDGET_GENERAL);*/
		gDLL->UI().popupAddGenericButton(popup,
				gDLL->getText("TXT_KEY_RF_RETIRE_ALL"), NULL,
				2, WIDGET_GENERAL);
		gDLL->UI().popupLaunch(popup, false, POPUPSTATE_IMMEDIATE);
		return true;
	}
	CvWString text = gDLL->getText("TXT_KEY_RF_CIV_SELECTION",
			pos + 1);
	if(retryingCivSelection) {
		text += L"\n" + gDLL->getText("TXT_KEY_RF_CIV_SELECTION_RETRY");
		retryingCivSelection = false;
	}
	gDLL->UI().popupSetBodyString(popup, text);
	for(size_t i = 0; i < eligible.size(); i++) {
		wstringstream wss;
		wss << (eligible.size() - i) << ". " << knownName(eligible[i], false);
		gDLL->UI().popupAddGenericButton(popup,
				wss.str(), NULL, 0, WIDGET_RF_CIV_CHOICE, eligible[i]);
	}
	gDLL->UI().popupLaunch(popup, false, POPUPSTATE_IMMEDIATE);
	return true;
}

void RiseFall::assignCivSelectionHelp(CvWStringBuffer& szBuffer,
		PlayerTypes selectedCiv) {

	CvGame& g = GC.getGame();
	wstringstream wss;
	wss << knownName(selectedCiv, false) << L"\n";
	int victStage = victoryStage(selectedCiv);
	if(victStage > 0) {
		wss << gDLL->getText("TXT_KEY_RF_CIV_SELECTION_VICTSTAGE") << L": "
				<< victStage << L"/4\n";
	}
	wss << gDLL->getText("TXT_KEY_RF_CIV_SELECTION_SCORE",
			g.getPlayerScore(selectedCiv));
	CvTeam& t = GET_TEAM(selectedCiv);
	if(t.isAVassal()) {
		wss << L"\n";
		PlayerTypes masterLeader = GET_TEAM(t.getMasterTeam()).getLeaderID();
		if(t.isCapitulated())
			 wss << gDLL->getText("TXT_KEY_RF_CIV_SELECTION_CAPVASSAL") << L" " <<
					knownName(masterLeader, true);
		else wss << gDLL->getText("TXT_KEY_RF_CIV_SELECTION_VOLVASSAL") << L" " <<
					knownName(masterLeader, true);
	}
	if(t.getNumWars() > 0) {
		wss <<  L"\n" << gDLL->getText("TXT_KEY_RF_CIV_SELECTION_WAR") << L": ";
		vector<PlayerTypes> warEnemies; // To get the commas right
		for(int i = 0; i < MAX_CIV_PLAYERS; i++) {
			CvPlayer& enemy = GET_PLAYER((PlayerTypes)i);
			if(enemy.isAlive() && !enemy.isMinorCiv() &&
					t.isAtWar(enemy.getTeam()))
				warEnemies.push_back(enemy.getID());
		}
		for(size_t i = 0; i < warEnemies.size(); i++) {
			wss << knownName(warEnemies[i], true);
			if(i < warEnemies.size() - 1)
				wss << L", ";
		}
	}
	int repeatCh = getCivChapter(selectedCiv);
	int currentCh = getCurrentChapter();
	if(repeatCh >= 0 && repeatCh <= currentCh) // 2nd condition important when loading
		wss << L"\n" << gDLL->getText("TXT_KEY_RF_CIV_SELECTION_REPEAT",
					repeatCh + 1, currentCh + 1);
	szBuffer.assign(wss.str());
}

CvWString RiseFall::knownName(PlayerTypes civId, bool nameNumber) const {

	bool hasMet = false;
	for(size_t i = 0; i < chapters.size(); i++) {
		if(!chapters[i]->hasEnded())
			break;
		if(GET_TEAM(chapters[i]->getCiv()).isHasMet(TEAMID(civId))) {
			hasMet = true;
			break;
		}
	}
	if(hasMet) {
		CvPlayer const& civ = GET_PLAYER(civId);
		bool unique = true;
		for(int i = 0; i < MAX_CIV_PLAYERS; i++) {
			CvPlayer const& other = GET_PLAYER((PlayerTypes)i);
			if(other.isEverAlive() && other.getID() != civId &&
					other.getCivilizationType() == civ.getCivilizationType()) {
				unique = false;
				break;
			}
		}
		wchar const* civDescr = civ.getCivilizationShortDescription();
		/*  Nicer to show civ names, but if one civ is in the game multiple times,
			will have to show the leader name. */
		if(unique)
			return civDescr;
		return CvWString(GC.getInfo(civ.getLeaderType()).getDescription()) +
				L"'s " + civDescr;
	}
	if(!nameNumber)
		return gDLL->getText("TXT_KEY_TOPCIVS_UNKNOWN");
	// Order has to be consistent with the numbering in launchCivSelectionPopup
	vector<PlayerTypes> eligible;
	eligibleByRecommendation(eligible);
	size_t index = 0;
	for(; index < eligible.size(); index++)
		if(eligible[index] == civId)
			break;
	if(index >= eligible.size())
		return gDLL->getText("TXT_KEY_TOPCIVS_UNKNOWN");
	return gDLL->getText("TXT_KEY_RF_CIV_SELECTION_NUMBER",
			eligible.size() - index);
}

void RiseFall::eligibleByRecommendation(vector<PlayerTypes>& r) const {

	vector<PlayerTypes> noRepeat;
	computeEligibleCivs(noRepeat, false);
	std::sort(noRepeat.begin(), noRepeat.end(), byRecommendation);
	r.insert(r.begin(), noRepeat.begin(), noRepeat.end());
	vector<PlayerTypes> all;
	computeEligibleCivs(all, true);
	/*  Sort those in 'all' minus 'noRepeat' separately and append the result to 'r'.
		(Would be nicer to let byRecommendation handle this, but that's difficult
		w/o accessing non-static functions, and I don't want to turn
		byRecommendation into a functor.) */
	vector<PlayerTypes> repeat;
	for(size_t i = 0; i < all.size(); i++) {
		bool found = false;
		for(size_t j = 0; j < noRepeat.size(); j++) {
			if(noRepeat[j] == all[i]) {
				found = true;
				break;
			}
		}
		if(!found)
			repeat.push_back(all[i]);
	}
	std::sort(repeat.begin(), repeat.end(), byRecommendation);
	r.insert(r.end(), repeat.begin(), repeat.end());
}

bool RiseFall::byRecommendation(PlayerTypes one, PlayerTypes two) {

	CvPlayer const& p1 = GET_PLAYER(one);
	CvPlayer const& p2 = GET_PLAYER(two);
	CvTeam const& t1 = GET_TEAM(one);
	CvTeam const& t2 = GET_TEAM(two);
	if(t1.isCapitulated() && !t2.isCapitulated())
		return false;
	if(t2.isCapitulated() && !t1.isCapitulated())
		return true;
	if(p1.isAVassal() && !p2.isAVassal())
		return false;
	if(p2.isAVassal() && !p1.isAVassal())
		return true;
	int vs1 = victoryStage(one);
	int vs2 = victoryStage(two);
	if(vs1 > vs2)
		return false;
	if(vs2 > vs1)
		return false;
	CvGame const& g = GC.getGame();
	int sc1 = g.getPlayerScore(one);
	int sc2 = g.getPlayerScore(two);
	if(sc1 > sc2)
		return false;
	if(sc2 > sc1)
		return true;
	return g.getPlayerRank(one) > g.getPlayerRank(two);
}

int RiseFall::victoryStage(PlayerTypes civId) {

	if(civId == NO_PLAYER) {
		FAssert(false);
		return 0;
	}
	CvPlayerAI const& civ = GET_PLAYER(civId);
	if(!civ.isAlive())
		return -1;
	int r = 0;
	// Stages 1 and 2 aren't meaningful enough
	if(civ.AI_atVictoryStage3())
		r = 3;
	if(civ.AI_atVictoryStage4())
		r = 4;
	/*  Culture4 is normally quite a bit farther away from victory than
		the other stage-4 strategies. Need to recompute the culture
		victory stage with a lowered countdownThresh. */
	if(r == 4 && civ.AI_atVictoryStage(AI_VICTORY_CULTURE4 &
			~AI_VICTORY_DIPLOMACY4 & ~AI_VICTORY_CONQUEST4 &
			~AI_VICTORY_DOMINATION4 & ~AI_VICTORY_SPACE4))
		r = std::max(3, civ.AI_calculateCultureVictoryStage(167));
	return r;
}

CvWString RiseFall::retireConfirmMsg() const {

	CvWString r = gDLL->getText("TXT_KEY_RF_CONFIRM_RETIRE", getRetireTurns());
	if(interludeLength > 0 && getCurrentChapter() < (int)(chapters.size() - 1))
		r.append(L" (" + gDLL->getText("TXT_KEY_RF_CONFIRM_RETIRE_INTERLUDE",
				interludeLength) + L")");
	r.append(NEWLINE);
	r.append(NEWLINE);
	r.append(gDLL->getText("TXT_KEY_RF_RETIRE_FOR_GOOD"));
	return r;
}

bool RiseFall::launchRetirePopup(CvPopup* popup, CvPopupInfo& info) {

	int pos = getCurrentChapter();
	FAssert(pos >= 0);
	bool bEndless = (pos >= 0 && chapters[pos]->isEndless());
	CvDLLInterfaceIFaceBase& base = *gDLL->getInterfaceIFace();
	base.popupSetBodyString(popup, bEndless ?
			gDLL->getText("TXT_KEY_POPUP_ARE_YOU_SURE") :
			retireConfirmMsg());
	// The popupAddGenericButton calls are copied from CvDLLButtonPopup::launchConfirmMenu
	if(!bEndless) {
		base.popupAddGenericButton(popup, gDLL->getText("TXT_KEY_POPUP_RETIRE"),
				NULL, 0, WIDGET_GENERAL);
	}
	base.popupAddGenericButton(popup, gDLL->getText("TXT_KEY_POPUP_CANCEL"),
			NULL, 1, WIDGET_GENERAL);
	base.popupAddGenericButton(popup, gDLL->getText("TXT_KEY_RF_END_GAME"),
			NULL, 2, WIDGET_GENERAL);
	base.popupLaunch(popup, false, POPUPSTATE_IMMEDIATE);
	return true;
}

void RiseFall::handleRetirePopup(int buttonClicked) {

	if(buttonClicked == 2)
		GC.getGame().retire();
	else if(buttonClicked == 0)
		retire();
}

int RiseFall::getCivChapter(PlayerTypes civId) const {

	int r = -1;
	for(size_t i = 0; i < chapters.size(); i++) {
		if(chapters[i]->getCiv() == civId)
			r = i;
	}
	return r;
}

bool RiseFall::isSelectingCiv() const {

	return selectingCiv;
}

void RiseFall::afterCivSelection(int buttonClicked) {

	CvGame& g = GC.getGame();
	CvPlayer& h = GET_PLAYER(getActivePlayer());
	int pos = getCurrentChapter();
	if(buttonClicked == 1) {
		FAssert(false);
		/*  Tbd.: Not working at all, at least not when the game ends during
			the upcoming chapter. Probably doesn't work otherwise either. */
		/*setPlayerControl(h.getID(), true);
		int t = chapters[pos + 1]->getStartTurn();
		if(pos >= (int)(chapters.size() - 1))
			t = chapters[pos]->getEndTurn() + 1 + interludeLength;
		t -= (g.getGameTurn() + 1);
		g.setAIAutoPlay(t);*/
		selectingCiv = false;
		return;
	}
	else if(buttonClicked == 2) {
		PlayerTypes nextCiv = NO_PLAYER;
		if(pos > 0)
			nextCiv = chapters[pos - 1]->getCiv();
		else nextCiv = nextCivAlive(BARBARIAN_PLAYER);
		chapters[pos]->setCiv(nextCiv);
		setPlayerControl(nextCiv, true);
		interludeCountdown = -1;
		chapters[pos]->start();
		g.setGameState(GAMESTATE_OVER);
	}
	// (buttonClicked==0 handled by handleCivSelection)
	selectingCiv = false;
	if(pos > 0) { // Relevant when loading a savegame
		CvPlayer& prev = GET_PLAYER(chapters[pos - 1]->getCiv());
		prev.setNetID(-1);
		prev.setIsHuman(false);
	}
	if(pos >= 0 && chapters[pos]->getCiv() == h.getID()) {
		// Start of human turn was missed; need to fill in some steps.
		setPlayerControl(h.getID(), true);
		interludeCountdown = -1;
		chapters[pos]->start();
		// Save before firing popups
		g.autoSave();
		welcomeToNextChapter(pos);
		return;
	}
	h.setNetID(-1);
	h.setIsHuman(false);
}

void RiseFall::handleCivSelection(PlayerTypes selectedCiv) {

	int pos = getCurrentChapter();
	if(pos < 0) {
		FAssert(pos >= 0);
		return;
	}
	if(getCivChapter(selectedCiv) >= 0)
		chapters[pos]->setRepeat(true);
	chapters[pos]->setCiv(selectedCiv);
}

bool RiseFall::isSquareDeal(CLinkList<TradeData> const& humanReceives,
			CLinkList<TradeData> const& aiReceives, PlayerTypes aiCiv) const {

	PlayerTypes human = getActivePlayer();
		/*  Actually no problem if the human receives sth. non-dual, e.g. gold
			for peace. */
	if(//allSquare(humanReceives, aiCiv, human) &&
			allSquare(aiReceives, human, aiCiv))
		return true;
	return false;
}

bool RiseFall::isNeededWarTrade(CLinkList<TradeData> const& humanReceives) const {

	CvPlayerAI const& human = GET_PLAYER(getActivePlayer());
	FOR_EACH_TRADE_ITEM(humanReceives) {
		if(pItem->m_eItemType == TRADE_WAR) {
			TeamTypes targetId = (TeamTypes)pItem->m_iData;
			if(targetId == NO_TEAM) {
				FAssert(targetId != NO_TEAM);
				return false;
			}
			if(/*GET_TEAM(targetId).AI_getWarSuccess(human.getTeam()) >
					GC.getWAR_SUCCESS_CITY_CAPTURING() &&*/
					GET_TEAM(human.getTeam()).AI_getEnemyPowerPercent() > 100)
				return true;
		}
	}
	return false;
}

bool RiseFall::allSquare(CLinkList<TradeData> const& list, PlayerTypes from,
		PlayerTypes to) const {

	bool allVassal = true;
	bool allDual = true;
	bool allLiberation = true;
	FOR_EACH_TRADE_ITEM(list) {
		TradeableItems item = pItem->m_eItemType;
		if(!CvDeal::isDual(item))
			allDual = false;
		if(item != TRADE_SURRENDER && item != TRADE_VASSAL)
			allVassal = false;
		if(item == TRADE_CITIES) {
			CvCity const* c = GET_PLAYER(from).getCity(pItem->m_iData);
			if(c == NULL || c->getLiberationPlayer() != to)
				allLiberation = false;
		}
		else allLiberation = false;
	}
	return allDual || allVassal || allLiberation;
}

int RiseFall::pessimisticDealVal(PlayerTypes aiCivId, int dealVal,
		CLinkList<TradeData> const& humanReceives) const {

	int r = dealVal;
	PlayerTypes humanCivId = getActivePlayer();
	TeamTypes humanTeamId = TEAMID(humanCivId);
	if(humanTeamId == NO_TEAM || humanCivId == NO_PLAYER) {
		FAssert(false);
		return r;
	}
	TeamTypes aiTeamId = TEAMID(aiCivId);
	CvTeamAI const& aiTeam = GET_TEAM(aiTeamId);
	CvTeamAI const& humanTeam = GET_TEAM(humanTeamId);
	CvPlayerAI const& humanCiv = GET_PLAYER(humanCivId);
	// Loop based on CvPlayerAI::AI_dealVal
	FOR_EACH_TRADE_ITEM(humanReceives) {
		int itemVal = 0;
		/*  What the AI thinks that the item should be worth to the human civ.
			In most cases, there is no code for this, and then replVal has to
			be set based on itemVal (what the AI normally demands for the item). */
		int replVal = -1;
		int data = pItem->m_iData;
		switch(pItem->m_eItemType) {
		case TRADE_PEACE:
			itemVal = humanTeam.AI_makePeaceTradeVal((TeamTypes)data, aiTeamId);
			break;
		case TRADE_WAR:
			itemVal = humanTeam.AI_declareWarTradeVal((TeamTypes)data, aiTeamId);
			if(getUWAI().isEnabled()) // advc.104
				replVal = GET_TEAM(humanTeamId).uwai().tradeValJointWar(
						(TeamTypes)data, aiTeam.getID());
			break;
		case TRADE_EMBARGO:
			itemVal = humanCiv.AI_stopTradingTradeVal((TeamTypes)data, aiCivId);
			break;
		case TRADE_CIVIC:
			itemVal = humanCiv.AI_civicTradeVal((CivicTypes)data, aiCivId);
			break;
		case TRADE_RELIGION:
			itemVal = humanCiv.AI_religionTradeVal((ReligionTypes)data, aiCivId);
			break;
		}
		/*  Don't hinder low-value trades (e.g. a little payment for switching
			to a religion that is already the majority religion) */
		if(itemVal <= (GC.AI_getGame().AI_getCurrEraFactor() + 1) * 100)
			continue;
		if(replVal < 0)
			replVal = ::round(itemVal / 1.5);
		r = r - itemVal + replVal;
	}
	return std::max(r, 0);
}

double RiseFall::dealThresh(bool annual) const {

	if(annual) // Resource trades (and peace treaties) are less problematic
		return 0.35;
	return 0.65;
}

void RiseFall::substituteDiploText(bool gift) {

	if(!gift)  /* Possibly still to be implemented: Response along the lines of */
		return;/* "you're too generous" to a rejected trade offer.              */
	CvDiplomacyResponse* resp = findThanks();
	if(resp == NULL || resp->getNumDiplomacyText() <= 0)
		return;
	/*  Conversion from wstring: breaks if multi-byte chars are involved
		(i.e. non-ASCII). */
	CvString replacement(gDLL->getText("TXT_KEY_RF_NO_THANKS"));
	clearDiploStrings();
	for(int j = 0; j < resp->getNumDiplomacyText(); j++) {
		originalThanks.push_back(new CvString(resp->getDiplomacyText(j)));
		resp->setDiplomacyText(j, replacement);
	}
}

void RiseFall::restoreDiploText() {

	if(originalThanks.empty())
		return;
	CvDiplomacyResponse* resp = findThanks();
	if(resp == NULL)
		return;
	FAssert(resp->getNumDiplomacyText() == originalThanks.size());
	for(int j = 0; j < resp->getNumDiplomacyText(); j++)
		resp->setDiplomacyText(j, *originalThanks[j]);
	clearDiploStrings();
}

wchar const* RiseFall::fillWS(int n, bool addPlus) {

	addPlus = (addPlus && n >= 0);
	n = (int)std::abs(n);
	if(n >= 1000) // Spell out the literals in order to avoid dynamic memory
		return (addPlus ? L"+" : L"");
	if(n >= 100)
		return (addPlus ? L"  +" : L"  ");
	if(n >= 10)
		return (addPlus ? L"    +" : L"    ");
	return (addPlus ? L"      +" : L"      ");
}

CvDiplomacyResponse* RiseFall::findThanks() {

	CvDiplomacyInfo* thanks = NULL;
	for(int i = 0; i < GC.getNumDiplomacyInfos(); i++) {
		if(_tcscmp(GC.getDiplomacyInfo(i).getType(), TEXT("AI_DIPLOCOMMENT_THANKS")) == 0)
			thanks = &GC.getDiplomacyInfo(i);
	}
	if(thanks == NULL)
		return NULL;
	for(int i = 0; i < thanks->getNumResponses(); i++) {
		return &thanks->getResponse_(i);
	}
	return NULL;
}

void RiseFall::clearDiploStrings() {

	for(size_t i = 0; i < originalThanks.size(); i++)
		SAFE_DELETE(originalThanks[i]);
	originalThanks.clear();
}

void RiseFall::shutOff(CvWString errorMsg) {

	showError(gDLL->getText("TXT_KEY_RF_SHUT_OFF"));
	showError(errorMsg);
	GC.getGame().setOption(GAMEOPTION_RISE_FALL, false);
	reset();
}

void RiseFall::showError(CvWString errorMsg) {

	gDLL->UI().addMessage(getActivePlayer(), true, 1, errorMsg,
			NULL, MESSAGE_TYPE_MAJOR_EVENT, NULL, GC.getColorType("RED"));
}
