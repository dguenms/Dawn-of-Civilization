#include "CvGameCoreDLL.h"
#include "RFTotalScore.h"
#include "CvGamePlay.h"
#include "CvInfo_GameOption.h"
#include "RiseFall.h"
#include "RFChapterScore.h"

using namespace fmath;


RFTotalScore::RFTotalScore() {

	breakdownString = NULL;
	reset();
}

void RFTotalScore::reset() {

	SAFE_DELETE(breakdownString);
	total = fromScored = fromFinishedUnscored = fromVictory = unstarted =
			fromInitialRank = initialRank = initialRivals = fromRemainingTime =
			remainingTimePercent = fromDifficulty = difficultyPercent = 0;
	frozen = false;
}

void RFTotalScore::write(FDataStreamBase* pStream) {

	int savegameVersion = 0;
	pStream->Write(savegameVersion);
	pStream->Write(total);
	pStream->Write(fromScored);
	pStream->Write(fromFinishedUnscored);
	pStream->Write(fromVictory);
	pStream->Write(unstarted);
	pStream->Write(fromInitialRank);
	pStream->Write(initialRank);
	pStream->Write(initialRivals);
	pStream->Write(fromRemainingTime);
	pStream->Write(remainingTimePercent);
	pStream->Write(fromDifficulty);
	pStream->Write(difficultyPercent);
	pStream->Write(frozen);
}

void RFTotalScore::read(FDataStreamBase* pStream) {

	reset();
	int savegameVersion = -1;
	pStream->Read(&savegameVersion);
	pStream->Read(&total);
	pStream->Read(&fromScored);
	pStream->Read(&fromFinishedUnscored);
	pStream->Read(&fromVictory);
	pStream->Read(&unstarted);
	pStream->Read(&fromInitialRank);
	pStream->Read(&initialRank);
	pStream->Read(&initialRivals);
	pStream->Read(&fromRemainingTime);
	pStream->Read(&remainingTimePercent);
	pStream->Read(&fromDifficulty);
	pStream->Read(&difficultyPercent);
	pStream->Read(&frozen);
}

void RFTotalScore::update(std::vector<RFChapter*> const& chapters) {

	if(frozen) {
		updateString();
		return;
	}
	fromScored = 0;
	fromFinishedUnscored = 0;
	unstarted = 0;
	initialRank = 0;
	initialRivals = 0;
	remainingTimePercent = 0;
	PlayerTypes finalCiv = NO_PLAYER;
	for(size_t i = 0; i < chapters.size(); i++) {
		RFChapter& ch = *chapters[i];
		if(ch.hasEnded()) {
			int sc = ch.computeScore();
			if(ch.isScored())
				fromScored += sc;
			else fromFinishedUnscored += sc;
		}
		else if(!ch.hasStarted())
			unstarted++;
		else {
			RFChapterScore const& chSc = ch.computeScoreBreakdown();
			initialRank = chSc.getInitialRank();
			initialRivals = chSc.getInitialRivals();
			remainingTimePercent = ch.getRemainingTimePercent();
			finalCiv = ch.getCiv();
		}
	}
	int victoryBase = 150;
	CvGame& g = GC.getGame();
	if(g.getGameState() != GAMESTATE_ON) {
		// Once we know that the human player doesn't win
		TeamTypes winner = g.getWinner();
		if(winner == NO_TEAM || finalCiv == NO_PLAYER || winner != TEAMID(finalCiv)) {
			victoryBase = 0;
			unstarted = 0;
		}
	}
	int compensation = victoryBase * unstarted; // For missed chapters
	fromVictory = victoryBase + compensation;
	// Victory premium awarded when starting from rank 1
	int fromVictoryMin = (victoryBase / 3) * (1 + unstarted);
	fromInitialRank = ::round((-(fromVictory - fromVictoryMin) *
			(initialRivals - initialRank + 1.0)) /
			std::max(1, initialRivals));
	total = fromVictory + fromInitialRank;
	fromRemainingTime = remainingTimePercent;
	// Earlier formula:
	//fromRemainingTime = ::round(victoryBase * (remainingTimePercent / 100.0));
	// Even earlier:
	/*fromRemainingTime = std::max(0, ::round((total - compensation) *
			(remainingTimePercent / 200.0)));*/
	total += fromRemainingTime + fromScored + fromFinishedUnscored;
	CvHandicapInfo& handicap = GC.getInfo(GC.getGame().getHandicapType());
	difficultyPercent = ::round(100 *
			((handicap.getDifficulty() + 10) / 40.0) - 100);
	fromDifficulty = (total <= 0 ? 0 : ::round((difficultyPercent / 100.0) * total));
	total += fromDifficulty;
	updateString();
}

void RFTotalScore::updateString() {

	SAFE_DELETE(breakdownString);
	breakdownString = new std::wstring(gDLL->getText(
			"TXT_KEY_RF_RISE_BREAKDOWN", fromScored, fromFinishedUnscored,
			fromVictory, unstarted, -fromInitialRank, initialRank,
			initialRivals + 1, fromRemainingTime, remainingTimePercent,
			fromDifficulty, difficultyPercent,
			GC.getInfo(GC.getGame().getHandicapType()).getDescription(),
			total,
			RiseFall::fillWS(fromScored, true),
			RiseFall::fillWS(fromFinishedUnscored, true),
			RiseFall::fillWS(fromVictory), RiseFall::fillWS(fromInitialRank),
			RiseFall::fillWS(fromRemainingTime), RiseFall::fillWS(fromDifficulty),
			RiseFall::fillWS(total)));
	/*  Would be nice to show the Dan Quayle title after the total, but that title
		is computed in CvDanQuayle.py and can't be accessed from here. */
	if(GC.getGame().getGameState() == GAMESTATE_EXTENDED) {
		int normScore = getNormalizedScore();
		(*breakdownString) += L"\n" + gDLL->getText("TXT_KEY_RF_NORMALIZED",
				normScore, RiseFall::fillWS(normScore));
	}
}

std::wstring* RFTotalScore::getString() const {

	return breakdownString;
}

int RFTotalScore::getScore() const {

	return total;
}

int RFTotalScore::getNormalizedScore() const {

	// To match the adjusted (see advc.043) scale of the Dan Quayle screen
	return ::round(std::pow((getScore() + 250) / 12.5, 2.5));
}

void RFTotalScore::freezeTotal(std::vector<RFChapter*> const& chapters) {

	if(frozen)
		return;
	update(chapters);
	frozen = true;
}
