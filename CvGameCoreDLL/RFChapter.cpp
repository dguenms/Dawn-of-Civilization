#include "CvGameCoreDLL.h"
#include "RFChapter.h"
#include "CoreAI.h"


RFChapter::RFChapter() { reset(); }

void RFChapter::reset() {

	length = delay = startTurn = scoreTimestamp = position = chapters =
			retireTurn = -1;
	scoreAtEnd = 0;
	civ = NO_PLAYER;
	endless = scoreShown = retireRecommended = repeat = false;
	breakdown.reset();
}

RFChapter::RFChapter(int pos, int maxChapters, int playLength) {

	reset(); // Can't use constructor initializer list with this pattern
	position = pos;
	chapters = maxChapters;
	double meanChapterLength = playLength / (double)maxChapters;
	double lengthShift = GC.getDefineINT("RF_CHAPTER_LENGTH_SHIFT_PERCENT") / 100.0;
	length = fmath::roundToMultiple(meanChapterLength * ::dRange(
			1 - lengthShift + 2 * pos * (lengthShift / (maxChapters - 1)),
			0.25, 1.75), 5);
}

RFChapter::RFChapter(int pos, int maxChapters, int playLength, int len) {

	reset(); // Can't use constructor initializer list with this pattern
	position = pos;
	chapters = maxChapters;
	length = len;
}

void RFChapter::write(FDataStreamBase* pStream) {

	int savegameVersion = 0;
	pStream->Write(savegameVersion);
	pStream->Write(length);
	pStream->Write(endless);
	pStream->Write(delay);
	pStream->Write(startTurn);
	pStream->Write(scoreTimestamp);
	pStream->Write(scoreShown);
	pStream->Write(retireRecommended);
	pStream->Write(position);
	pStream->Write(scoreAtEnd);
	pStream->Write(retireTurn);
	pStream->Write(repeat);
	pStream->Write(civ);
	pStream->Write(chapters);
	breakdown.write(pStream);
}

void RFChapter::read(FDataStreamBase* pStream) {

	reset();
	int savegameVersion = -1;
	pStream->Read(&savegameVersion);
	pStream->Read(&length);
	pStream->Read(&endless);
	pStream->Read(&delay);
	pStream->Read(&startTurn);
	pStream->Read(&scoreTimestamp);
	pStream->Read(&scoreShown);
	pStream->Read(&retireRecommended);
	pStream->Read(&position);
	pStream->Read(&scoreAtEnd);
	pStream->Read(&retireTurn);
	pStream->Read(&repeat);
	int tmp = -1;
	pStream->Read(&tmp);
	civ = (PlayerTypes)tmp;
	pStream->Read(&chapters);
	breakdown.read(pStream, hasStarted() ? this : NULL);
}

void RFChapter::setEndless(bool b) {

	endless = b;
}

void RFChapter::setDelay(int scoringDelay) {

	delay = scoringDelay;
}

void RFChapter::setStartTurn(int t) {

	startTurn = t;
}

void RFChapter::setCiv(PlayerTypes playerId) {

	FAssert(playerId != NO_PLAYER && !GET_PLAYER(playerId).isMinorCiv());
	civ = playerId;
}

void RFChapter::start() {

	CvGame const& g = GC.getGame();
	FAssert(startTurn == g.getGameTurn());
	/*  This shouldn't do anything currently. (I.e. chapters start exactly as
		planned, but could change in a future version.) */
	startTurn = g.getGameTurn();
	breakdown.atChapterStart(*this);
}

void RFChapter::setScoreAtEnd(int sc) {

	scoreAtEnd = sc;
}

void RFChapter::score() {

	if(isScored())
		return;
	breakdown.update();
	scoreTimestamp = GC.getGame().getGameTurn();
}

void RFChapter::setScored(int turn) {

	scoreTimestamp = turn;
}

void RFChapter::setRetireTurn(int t) {

	retireTurn = t;
}

void RFChapter::setRetireWasRecommended(bool b) {

	retireRecommended = b;
}

bool RFChapter::wasRetireRecommended() const {

	return retireRecommended;
}

int RFChapter::getRetireTurn() const {

	return retireTurn;
}

int RFChapter::getLength() const {

	return length;
}

int RFChapter::getDelay() const {

	return delay;
}

bool RFChapter::hasStarted() const {

	return GC.getGame().getGameTurn() >= getStartTurn();
}

bool RFChapter::hasEnded() const {

	if(isScored())
		return true;
	if(isEndless())
		return false;
	return GC.getGame().getGameTurn() > getEndTurn();
}

bool RFChapter::isOngoing() const {

	return hasStarted() && !hasEnded();
}

int RFChapter::getStartTurn() const {

	return startTurn;
}

int RFChapter::getEndTurn() const {

	if(isEndless())
		return -1;
	// The end turn is still part of the chapter (not an Auto Play turn)
	return getStartTurn() + getLength() - 1;
}

int RFChapter::getScoreTurn() const {

	if(scoreTimestamp >= 0)
		return scoreTimestamp;
	if(isEndless())
		return -1;
	return getDelay() + getEndTurn();
}

int RFChapter::computeScore() {

	if(!isScored() && hasEnded()) {
		PlayerTypes activeId = GC.getGame().getActivePlayer();
		/*  If current Civ score unknown to active player, provide the last known
			chapter score instead. */
		if(activeId != NO_PLAYER && getCiv() != NO_PLAYER &&
				!GET_TEAM(activeId).isHasMet(TEAMID(getCiv())))
			return scoreAtEnd;
	}
	breakdown.update();
	return breakdown.getScore();
}

PlayerTypes RFChapter::getCiv() const {

	return civ;
}

bool RFChapter::isEndless() const {

	return endless;
}

bool RFChapter::isFinalChapter() const {

	return getPosition() >= chapters - 1;
}

int RFChapter::getPosition() const {

	return position;
}

bool RFChapter::isScored() const {

	return scoreTimestamp >= 0;
}

bool RFChapter::isScoreShown() const {

	return scoreShown;
}

void RFChapter::setScoreShown(bool b) {

	scoreShown = b;
}

int RFChapter::getRemainingTimePercent() const {

	int t = getRetireTurn();
	if(t < 0 && (getCiv() == NO_PLAYER ||
			GET_PLAYER(getCiv()).isAlive())) // Defeat is not retirement
		t = GC.getGame().getGameTurn();
	return (length <= 0 ? 100 :
			// Minus 1 b/c the current turn is already spent
			fmath::round((length - t + getStartTurn() - 1.0) / (0.01 * length)));
}

bool RFChapter::isRepeat() const {

	return repeat;
}

void RFChapter::setRepeat(bool b) {

	repeat = b;
}

RFChapterScore const& RFChapter::computeScoreBreakdown() {

	breakdown.update();
	return breakdown;
}

// </advc.700>
