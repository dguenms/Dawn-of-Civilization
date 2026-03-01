#pragma once

#ifndef RF_CHAPTER_H
#define RF_CHAPTER_H

#include "RFChapterScore.h"

/*  advc.700: New class. Encapsulates data about a chapter of a
	Rise & Fall game. */
class RFChapter {

public:
	RFChapter();
	// Computes own length
	RFChapter(int pos, int maxChapters, int playLength);
	// Chapter length set by caller
	RFChapter(int pos, int maxChapters, int playLength, int length);
	void write(FDataStreamBase* pStream);
	void read(FDataStreamBase* pStream);
	void setEndless(bool b);
	void setDelay(int scoringDelay);
	void setStartTurn(int t);
	void setCiv(PlayerTypes playerId);
	void start();
	void setScoreAtEnd(int sc);
	void score();
	void setScored(int turn);
	void setRetireWasRecommended(bool b);
	bool wasRetireRecommended() const;
	void setRetireTurn(int t);
	int getRetireTurn() const;
	int getLength() const;
	int getDelay() const;
	bool hasStarted() const;
	bool hasEnded() const;
	bool isOngoing() const;
	bool isEndless() const;
	bool isFinalChapter() const;
	int getPosition() const;
	bool isScored() const;
	bool isScoreShown() const;
	void setScoreShown(bool b);
	int getRemainingTimePercent() const;
	bool isRepeat() const;
	void setRepeat(bool b);
	RFChapterScore const& computeScoreBreakdown();
	// Exposed to Python through CvGame:
	  // First turn on which the player is in control
	  int getStartTurn() const;
	  // Last turn on which the player is in control
	  int getEndTurn() const;
	  int getScoreTurn() const;
	  PlayerTypes getCiv() const;
	  int computeScore();

private:
	void reset();

	int length;
	int delay;
	int startTurn;
	int scoreTimestamp;
	int position;
	PlayerTypes civ;
	int chapters;
	bool endless;
	int scoreAtEnd;
	int retireTurn;
	RFChapterScore breakdown;
	bool scoreShown;
	bool retireRecommended;
	bool repeat;
};

#endif
