#pragma once

#ifndef RF_TOTAL_SCORE_H
#define RF_TOTAL_SCORE_H

#include "RFChapter.h"

// advc.700: New class. Computes and stores the total awarded Rise score.
class RFTotalScore {

public:
	RFTotalScore();
	void reset();
	void write(FDataStreamBase* pStream);
	void read(FDataStreamBase* pStream);
	void update(std::vector<RFChapter*> const& chapters);
	int getScore() const;
	int getNormalizedScore() const;
	void freezeTotal(std::vector<RFChapter*> const& chapters);
	std::wstring* getString() const;

private:
	void updateString();

	std::wstring* breakdownString;
	bool frozen;
	int total, fromScored, fromFinishedUnscored, fromVictory, unstarted,
		fromInitialRank, initialRank, initialRivals, fromRemainingTime,
		remainingTimePercent, fromDifficulty, difficultyPercent;
};

#endif
