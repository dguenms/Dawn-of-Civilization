#pragma once

#ifndef RF_CHAPTER_SCORE_H
#define RF_CHAPTER_SCORE_H

class RFChapter;

/*  advc.700: New class. Computes and stores the score awarded for a
	RFChapter. */
class RFChapterScore {

public:
	RFChapterScore();
	void reset();
	void write(FDataStreamBase* pStream);
	void read(FDataStreamBase* pStream, RFChapter const* rfc);
	void update();
	void atChapterStart(RFChapter const& rfc);
	int getScore() const;
	int getScoreFromRemainingTime() const;
	std::wstring* getString() const;
	int getInitialRank() const;
	int getInitialRivals() const;

private:
	void updateString();
	std::pair<int,int> computeRank(bool storeCivScores, bool ignoreVictStage = false);
	int modifiedCivScore(PlayerTypes civId) const;

	std::wstring* breakdownString;
	int total, totalScaled, fromRank, rank, fromInitialRank, initialRank,
			initialRivals, fromCivScore, civScorePercent,
			fromInitialCivScore, initialCivScorePercent,
			referenceRank, referenceRank2,
			fromRemainingTime, remainingTimePercent, fromRepeat;
	int initialCivScores[MAX_CIV_PLAYERS];
	RFChapter const* chapter;
};

#endif
