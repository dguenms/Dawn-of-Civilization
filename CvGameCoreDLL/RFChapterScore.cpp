#include "CvGameCoreDLL.h"
#include "RFChapterScore.h"
#include "RiseFall.h"
#include "RFChapter.h"
#include "CvGamePlay.h"
#include "CvPlayerAI.h"

using namespace fmath;


RFChapterScore::RFChapterScore() {

	breakdownString = NULL;
	reset();
}

void RFChapterScore::reset() {

	SAFE_DELETE(breakdownString);
	chapter = NULL;
	total = totalScaled = fromRank = rank = fromInitialRank = initialRank =
			initialRivals = fromCivScore = civScorePercent =
			fromInitialCivScore = initialCivScorePercent =
			referenceRank = referenceRank2 = fromRepeat =
			fromRemainingTime = remainingTimePercent = 0;
	for(int i = 0; i < MAX_CIV_PLAYERS; i++)
		initialCivScores[i] = 0;
}

void RFChapterScore::write(FDataStreamBase* pStream) {

	int savegameVersion = 0;
	pStream->Write(savegameVersion);
	pStream->Write(total);
	pStream->Write(totalScaled);
	pStream->Write(fromRank);
	pStream->Write(rank);
	pStream->Write(fromInitialRank);
	pStream->Write(initialRank);
	pStream->Write(initialRivals);
	pStream->Write(fromCivScore);
	pStream->Write(civScorePercent);
	pStream->Write(fromInitialCivScore);
	pStream->Write(initialCivScorePercent);
	pStream->Write(referenceRank);
	pStream->Write(referenceRank2);
	pStream->Write(fromRemainingTime);
	pStream->Write(remainingTimePercent);
	pStream->Write(fromRepeat);
	for(int i = 0; i < MAX_CIV_PLAYERS; i++)
		pStream->Write(initialCivScores[i]);
}

void RFChapterScore::read(FDataStreamBase* pStream, RFChapter const* rfc) {

	reset();
	int savegameVersion = -1;
	pStream->Read(&savegameVersion);
	pStream->Read(&total);
	pStream->Read(&totalScaled);
	pStream->Read(&fromRank);
	pStream->Read(&rank);
	pStream->Read(&fromInitialRank);
	pStream->Read(&initialRank);
	pStream->Read(&initialRivals);
	pStream->Read(&fromCivScore);
	pStream->Read(&civScorePercent);
	pStream->Read(&fromInitialCivScore);
	pStream->Read(&initialCivScorePercent);
	pStream->Read(&referenceRank);
	pStream->Read(&referenceRank2);
	pStream->Read(&fromRemainingTime);
	pStream->Read(&remainingTimePercent);
	pStream->Read(&fromRepeat);
	pStream->Read(MAX_CIV_PLAYERS, initialCivScores);
	chapter = rfc;
}

void RFChapterScore::atChapterStart(RFChapter const& rfc) {

	chapter = &rfc;
	/*  Sometimes updated before the start of the first chapter anyway, but
		not guaranteed. */
	GC.getGame().updateScore(true);
	std::pair<int,int> rank_rivals = computeRank(true);
	initialRank = rank_rivals.first;
	initialRivals = rank_rivals.second;
}

std::pair<int,int> RFChapterScore::computeRank(bool storeCivScores,
		bool ignoreVictStage) {

	if(chapter == NULL) {
		FAssert(chapter != NULL);
		return std::make_pair(-1, -1);
	}
	double ourRank = 1;
	int ourRivals = 0;
	CvGame const& g = GC.getGame();
	CvPlayerAI const& we = GET_PLAYER(chapter->getCiv());
	int ourVictStage = g.getRiseFall().victoryStage(we.getID());
	int ourScore = modifiedCivScore(we.getID());
	for(int i = 0; i < MAX_CIV_PLAYERS; i++) {
		CvPlayer const& they = GET_PLAYER((PlayerTypes)i);
		if(!they.isAlive() || they.isMinorCiv() || they.isAVassal()) {
			if(storeCivScores)
				initialCivScores[i] = 0;
			continue;
		}
		if(storeCivScores)
			initialCivScores[i] = modifiedCivScore(they.getID());
		if(they.getID() == we.getID() ||
				/*  Current player civ can't hurt our rank if we're a
					previous player civ */
				they.isActive())
			continue;
		ourRivals++;
		if(!ignoreVictStage) {
			int theirVictStage = g.getRiseFall().victoryStage(they.getID());
			if(theirVictStage > ourVictStage) {
				ourRank++;
				continue;
			}
			if(ourVictStage > theirVictStage)
				continue;
		}
		int theirScore = modifiedCivScore(they.getID());
		if(theirScore > ourScore)
			ourRank++;
		if(ourScore == theirScore)
			ourRank += 0.5;
	}
	/*  Assume that the player starts in the middle, even if the AI starts with
		more free tech. */
	if(g.getGameTurn() <= g.getStartTurn() && we.isAlive())
		ourRank = 1 + ourRivals / 2.0;
	ourRank += 0.01; // Just to be explicit about rounding up
	return std::make_pair(::round(ourRank), ourRivals);
}

int RFChapterScore::modifiedCivScore(PlayerTypes civId) const {

	CvGame const& g = GC.getGame();
	/*  Count winning AI as having the highest score. Could also be an
		AI civ that the human player still gets score for, but not the current
		human civ. */
	if(g.getWinner() == TEAMID(civId) && !GET_PLAYER(civId).isActive())
		return g.getPlayerScore(g.getRankPlayer((PlayerTypes)0)) + 1;
	return g.getPlayerScore(civId);
}

void RFChapterScore::update() {

	if(chapter == NULL || initialRank <= 0)
		return;
	CvGame& g = GC.getGame();
	if(chapter->isScored()) { // Freeze data upon scoring
		updateString();
		return;
	}
	GC.getGame().updateScore(); // Necessary when update triggered by elimination
	/*  Could apply victory stages only to initial ranks by calling
		computeRank with ignoreVictStage=true here. */
	rank = computeRank(false).first;
	PlayerTypes chCiv = chapter->getCiv();
	int civScore = modifiedCivScore(chCiv);
	int nextBestScore = 0;
	bool nextRankFound = false;
	for(int i = 0; i < MAX_CIV_PLAYERS; i++) {
		CvPlayer const& civ = GET_PLAYER((PlayerTypes)i);
		if(!civ.isAlive() || civ.isMinorCiv() || civ.isAVassal())
			continue;
		int sc = modifiedCivScore(civ.getID());
		if(sc >= civScore)
			continue;
		nextBestScore = std::max(nextBestScore, sc);
		if(g.getPlayerRank(civ.getID()) >= g.getPlayerRank(chCiv))
			nextRankFound = true;
	}
	if(nextBestScore <= 0)
		nextBestScore = std::max(civScore, 1);
	// Special treatment for first chapter (when all start on par)
	if(chapter->getPosition() == 0 && g.countCivPlayersAlive() > rank)
		nextRankFound = true;
	referenceRank = nextRankFound ? rank + 1 : rank;
	int initialCivScore = initialCivScores[chCiv];
	std::vector<int> initialCivScoresSorted;
	for(int i = 0; i < MAX_CIV_PLAYERS; i++) {
		if(initialCivScores[i] > 0)
			initialCivScoresSorted.push_back(initialCivScores[i]);
	}
	std::sort(initialCivScoresSorted.begin(), initialCivScoresSorted.end(),
			std::greater<int>());
	/*  Want to use the same reference rank for 'fromCivScore' and
		'fromInitialCivScore', but there may not be enough non-vassal civs. */
	referenceRank2 = std::min(referenceRank, (int)initialCivScoresSorted.size());
	int referenceScore = initialCivScoresSorted[referenceRank2 - 1];
	FAssert(referenceScore > 0 && nextBestScore > 0);
	civScorePercent = ::round((100.0 * civScore) / nextBestScore);
	fromCivScore = civScorePercent;
	initialCivScorePercent = ::round((100.0 * initialCivScore) / referenceScore);
	/*  Assume that scores at game start are all equal (although that's not true
		on difficulty settings above Noble) */
	if(chapter->getPosition() == 0)
		initialCivScorePercent = 100;
	fromInitialCivScore = -initialCivScorePercent;
	fromRank = ::round((100.0 * (initialRivals - rank + 1)) /
			std::max(1, initialRivals));
	fromInitialRank = ::round((-100.0 * (initialRivals - initialRank + 1)) /
			std::max(1, initialRivals));
	remainingTimePercent = chapter->getRemainingTimePercent();
	total = fromRank + fromInitialRank + fromCivScore + fromInitialCivScore;
	fromRemainingTime = std::max(0, ::round(
			total * (remainingTimePercent / 200.0)));
	total += fromRemainingTime;
	if(chapter->isRepeat() && total > 0) {
		fromRepeat = ::round(total / -2.0);
		total += fromRepeat;
	}
	totalScaled = total;
	if(total < -9) // Want to make the score less negative; 9 = 3*srqt(9)
		totalScaled = -::round(std::sqrt(-1.0 * total) * 3);
	updateString();
}

void RFChapterScore::updateString() {

	SAFE_DELETE(breakdownString);
	/*  Inverted sign on the two subtrahends b/c the minus sign is already produced
		by XML */
	breakdownString = new std::wstring(gDLL->getText(
			"TXT_KEY_RF_CHAPTER_BREAKDOWN", fromRank, rank, -fromInitialRank,
			initialRank, initialRivals + 1, fromCivScore, civScorePercent,
			referenceRank, -fromInitialCivScore, initialCivScorePercent,
			referenceRank2,
			RiseFall::fillWS(fromRank), RiseFall::fillWS(fromInitialRank),
			RiseFall::fillWS(fromCivScore), RiseFall::fillWS(fromInitialCivScore)));
	bool isScored = (chapter != NULL && chapter->isScored());
	if(!isScored || remainingTimePercent > 0) {
		(*breakdownString) += L"\n";
		if(!isScored)
			(*breakdownString) += gDLL->getText("TXT_KEY_RF_CHAPTER_SCORE_IF_RETIRING",
					fromRemainingTime, remainingTimePercent, RiseFall::fillWS(fromRemainingTime));
		else (*breakdownString) += gDLL->getText("TXT_KEY_RF_CHAPTER_SCORE_RETIRED",
					fromRemainingTime, remainingTimePercent, RiseFall::fillWS(fromRemainingTime));
	}
	if(chapter->isRepeat() && chapter->getCiv() != NO_PLAYER)
		(*breakdownString) += L"\n" + gDLL->getText("TXT_KEY_RF_CHAPTER_SCORE_REPEAT",
		-fromRepeat, GET_PLAYER(chapter->getCiv()).getCivilizationShortDescription(),
		RiseFall::fillWS(fromRepeat));
	(*breakdownString) += L"\n   ------------------------------------------------------------\n";
	(*breakdownString) += ((total < 0 && totalScaled > total) ?
			gDLL->getText("TXT_KEY_RF_CHAPTER_BOTTOM_LINE_MINUS", total, totalScaled,
			RiseFall::fillWS(total), RiseFall::fillWS(totalScaled)) :
			gDLL->getText("TXT_KEY_RF_CHAPTER_BOTTOM_LINE_PLUS", total,
			RiseFall::fillWS(total)));
}

std::wstring* RFChapterScore::getString() const {

	return breakdownString;
}

int RFChapterScore::getInitialRank() const {

	return initialRank;
}

int RFChapterScore::getInitialRivals() const {

	return initialRivals;
}

int RFChapterScore::getScore() const {

	return totalScaled;
}

int RFChapterScore::getScoreFromRemainingTime() const {

	return fromRemainingTime;
}
