// <advc.250b>

#include "CvGameCoreDLL.h"
#include "StartPointsAsHandicap.h"
#include "CvGame.h"
#include "CvPlayer.h"
#include "CvMap.h"

/*  advc (note): This was the first class added by AdvCiv and, apart from the
	includes above, it hasn't been looked at for the past few years, so there are
	probably things that could be improved. Seems to be working as intended though. */

using std::vector;
using std::wstring;
using std::wostringstream;
using std::ostringstream;


StartPointsAsHandicap::StartPointsAsHandicap() {

	pointsDisplayString = NULL;
	nCivs = nHuman = 0;
	randPoints = false;
	unequalDistrib = false;
}


StartPointsAsHandicap::~StartPointsAsHandicap() {

	for(size_t i = 0; i < civs.size(); i++)
		SAFE_DELETE(civs[i]);
	SAFE_DELETE(pointsDisplayString);
}


void StartPointsAsHandicap::reset() {

	for(size_t i = 0; i < civs.size(); i++)
		SAFE_DELETE(civs[i]);
	civs.clear();
	SAFE_DELETE(pointsDisplayString);
}


wstring* StartPointsAsHandicap::forSettingsScreen(bool bTab) const {

	updatePointsDisplayString(bTab);
	return pointsDisplayString;
}


void StartPointsAsHandicap::setInitialItems() {

	reset();
	gatherCivs();
	unequalDistrib = assignPoints();
	bool randomize = unequalDistrib;
	for(int i = 0; i < nCivs; i++)
		report += CvString::format("Points assigned to id %d: %d\n",
				i, civs[i]->startPoints_configured());
	if(randomize)
		randomize = GC.getDefineINT("SPAH_RANDOMIZE") > 0;
	if(randomize) {
		randomizePoints();
		report += CvString::format("Points after randomization:\n");
		for(int i = 0; i < nCivs; i++) {
			civs[i]->assignStartPoints();
			report += CvString::format("id %d: %d\n", i,
					civs[i]->startPoints_actual());
		}
	}
	else for(int i = 0; i < nCivs; i++)
		civs[i]->assignStartPoints();
	updatePointsDisplayString(true);
	// Report about game setup
	//gDLL->logMsg("debug_SPaH.log", report, true, true);
}


// Actual points of AI civs
void StartPointsAsHandicap::distribution(std::vector<int>& r) const {

	for(int i = 0; i < nCivs; i++)
		if(!civs[i]->isHuman())
			r.push_back(civs[i]->startPoints_actual());
}

void StartPointsAsHandicap::write(FDataStreamBase* pStream) {

	pStream->Write(randPoints);
	pStream->Write(nCivs);
	for(int i = 0; i < nCivs; i++) {
		allPts[2 * i] = civs[i]->startPoints_configured();
		allPts[2 * i + 1] = civs[i]->startPoints_actual();
	}
	pStream->Write(2 * MAX_CIV_PLAYERS, allPts);
}


void StartPointsAsHandicap::read(FDataStreamBase* pStream) {

	reset();
	pStream->Read(&randPoints);
	pStream->Read(&nCivs);
	pStream->Read(2 * MAX_CIV_PLAYERS, allPts);
	// Done loading from stream; now recreate objects
	nHuman = 0;
	for(int i = 0; i < nCivs; i++) {
		MajorCiv* mciv = new MajorCiv((PlayerTypes)i);
		mciv->setStartPoints_configured(allPts[2 * i]);
		mciv->setStartPoints_actual(allPts[2 * i + 1]);
		civs.push_back(mciv);
		if(mciv->isHuman())
			nHuman++;
	}
	std::sort(civs.begin(), civs.end(), isLeftPtsLessThanRight);
	updatePointsDisplayString(true);
}


void StartPointsAsHandicap::gatherCivs() {

	for(int i = 0; i < MAX_CIV_PLAYERS; i++) {
		if((PlayerTypes)i == NO_PLAYER)
			continue;
		CvPlayer const& p = GET_PLAYER((PlayerTypes)i);
		if(!p.isAlive() || p.isMinorCiv())
			continue;
		MajorCiv* mciv = new MajorCiv(p.getID());
		civs.push_back(mciv);
	}
	nCivs = civs.size();
	/*  To ensure that the humans come first (which might be already guaranteed
		by the EXE and CvInitCore). */
	std::sort(civs.begin(), civs.end(), isLeftPtsLessThanRight);
	nHuman = 0;
	for(int i = 0; i < nCivs; i++) {
		if(civs[i]->isHuman()) {
			nHuman++;
			civs[i]->setStartPoints_configured(-1);
		}
		else break;
	}
	FAssert(nHuman > 0);
}


bool StartPointsAsHandicap::assignPoints() {

	int pointsEntered = GC.getInitCore().getNumAdvancedStartPoints();
	// (This value should not be used in a SPaH game)
	GC.getInitCore().setNumAdvancedStartPoints(-1);
	FAssert(pointsEntered > 0);
	report += CvString::format("Points entered: %d\n", pointsEntered);
	bool flatDistrib = (pointsEntered < 10000);
	if(flatDistrib) {
		report += CvString::format("Flat distribution");
		for(int i = 0; i < nCivs; i++) {
			if(!civs[i]->isHuman())
				civs[i]->setStartPoints_configured(pointsEntered);
		}
		return false;
	}
	report += CvString::format("Unequal distribution");
	int weakestPercent = pointsEntered % 100;
	int strongest = pointsEntered / 100;
	int weakest = intdiv::uround(weakestPercent * strongest, 100);
	report += CvString::format("Points strongest, weakest: (%d, %d)\n",
			strongest, weakest);
	int nAI = nCivs - nHuman;
	int middleAIIndex = nHuman + nAI / 2;
	/*  Rule 1: If there is a "middle" AI, that AI receives the mean of
		the weakest and strongest. */
	if(nAI % 2 != 0)
		civs[middleAIIndex]->setStartPoints_configured(
				intdiv::uround(strongest + weakest, 2));
	if(nAI <= 3) {
		// Rule 2: Strongest civ as entered
		civs[nCivs - 1]->setStartPoints_configured(strongest);
		// Rule 3: Weakest civ as entered
		if(nAI > 1)
			civs[nHuman]->setStartPoints_configured(weakest);
		return true;
	}
	/*  From 4 AI civs upwards, apply Rule 4: Form pairs of civs that receive
		equal points and let points increase linearly from pair to pair,
		starting at 'weakest' and ending with 'strongest'. */
	int nPairs = nAI / 2;
	scaled step(strongest - weakest, nPairs - 1);
	scaled pts = weakest;
	for(int i = nHuman; i < nCivs; i += 2) {
		// Middle element not paired; already set by Rule 1.
		if(nAI % 2 != 0 && i == middleAIIndex)
			i++;
		civs[i]->setStartPoints_configured(pts.round());
		if(nAI % 2 != 0 && i + 1 == middleAIIndex)
			i++;
		civs[i + 1]->setStartPoints_configured(
				civs[i]->startPoints_configured());
		pts += step;
	}
	return true;
}


void StartPointsAsHandicap::randomizePoints() {

	std::sort(civs.begin(), civs.end(), isLeftPtsLessThanRight);
	/*  Increase and decrease some point values randomly. The random changes are
		such that the following properties remain unchanged:
		 * the ordering of the civs (by points), e.g.
		   the civ with the 3rd most points will still
		   have the third most points after randomization;
		 * the sum of the points over all civs;
		 * the highest and the lowest point value among AI civs; and
		 * the human player's points. */
	int nAI = nCivs - nHuman;
	int middleAIIndex = nHuman + nAI / 2;
	if(nAI < 4)
		return;
	// Special pair [n-2],[2] (a sort of wrap-around)
	bounce(nCivs - 2, nHuman + 1);
	if(nAI < 6)
		return;
	for(int i = nHuman + 2; i <= nCivs - 3; i += 2) {
		if(nAI % 2 != 0 && i == middleAIIndex)
			i++;
		if(nAI % 2 != 0 && i + 1 == middleAIIndex) {
			bounce(i, i + 2);
			i++;
			continue;
		}
		bounce(i, i + 1);
	}
}


void StartPointsAsHandicap::bounce(int i, int j) {

	/*  The "pursuer" of 'i' is the civ with strictly fewer points than 'i'
		(pursuerIpts < iPts) that has the minimal point distance to 'i'.
		often that is 'i-1', but it could be a lower index if several civs
		have the same amount of configured points. One of the postconditions
		of 'randomizePoints' (see above) is that no civ overtake another
		in terms of start points, though ties can be broken. */
	int iPts = civs[i]->startPoints_configured();
	int pursuerIpts = 0;
	int pursuerI;
	for(pursuerI = i; pursuerI >= nHuman; pursuerI--) {
		pursuerIpts = civs[pursuerI]->startPoints_configured();
		if(pursuerIpts < iPts)
			break;
	}
	int deltaMaxNeg = intdiv::round(iPts - pursuerIpts, 2);
	int jPts = civs[j]->startPoints_configured();
	int pursuedByJpts = 0;
	int pursuedByJ;
	for(pursuedByJ = j; pursuedByJ < nCivs; pursuedByJ++) {
		pursuedByJpts = civs[pursuedByJ]->startPoints_configured();
		if(pursuedByJpts > jPts)
			break;
	}
	int deltaMaxPos = intdiv::round(pursuedByJpts - jPts, 2);
	// To ensure that randomization leaves the sum of all points unchanged
	int deltaMax = deltaMaxNeg < deltaMaxPos ? deltaMaxNeg : deltaMaxPos;
	report += CvString::format("Bouncing apart civ ids %d (%d points) and %d"
			" (%d points) by at most plus/minus %d points\n",
			i, civs[i]->startPoints_configured(),
			j, civs[j]->startPoints_configured(),
			deltaMax);
	int delta = SyncRandNum(deltaMax);
	civs[i]->setStartPoints_actual(civs[i]->startPoints_configured() - delta);
	civs[j]->setStartPoints_actual(civs[j]->startPoints_configured() + delta);
}


void StartPointsAsHandicap::rearrangeStartingPlots() {

	if(!unequalDistrib)
		return;
	int nAI = nCivs - nHuman;
	if(nAI == 0)
		return;
	std::sort(civs.begin(), civs.end(), isLeftPtsLessThanRight);
	vector<MajorCiv*> civsByDist;
	for(int i = nHuman; i < nCivs; i++) {
		civsByDist.push_back(civs[i]);
		civs[i]->setDist(minDist(civs[i]->startingPlot()));
	}
	std::sort(civsByDist.begin(), civsByDist.end(), isLeftCloserThanRight);
	// Temporary vector for swapping plots
	std::vector<CvPlot*> newStartingPlot;
	for(int i = 0; i < nAI; i++)
		newStartingPlot.push_back(civsByDist[i]->startingPlot());
	for(int i = 0; i < nAI; i++)
		civs[nHuman + i]->assignStartingPlot(newStartingPlot[i]);
}


/*  Shortest distance to any human starting plot. Same metric as in CvGame::
	normalizeStartingPlotLocations. */
int StartPointsAsHandicap::minDist(CvPlot* p) {

	int r = MAX_INT;
	for(int i = 0; i < nHuman; i++) {
		CvPlot* q = civs[i]->startingPlot();
		int d = GC.getMap().calculatePathDistance(p, q);
		if(d < 0) // No (land) path
			d = 5 * ::plotDistance(p->getX(), p->getY(), q->getX(), q->getY());
		if(d < r)
			r = d;
	}
	return r;
}


void StartPointsAsHandicap::updatePointsDisplayString(bool bTab) const {

	if(civs[nCivs - 1]->startPoints_configured() <= 0) {
		pointsDisplayString = new wstring();
		return;
	}
	char const* ind = (bTab ? "\t" : "  "); // indent
	wostringstream s;
	s << "Start Points As Handicap\n"
			<< ind << "(distribution: ";
	bool showActual = (GC.getDefineINT("SPAH_SHOW_RANDOMIZED") > 0);
	for(int i = nHuman; i < nCivs; i++) {
		int pts = showActual ? civs[i]->startPoints_actual() :
							   civs[i]->startPoints_configured();
		s << pts << ", ";
		if((i + 3 - nHuman) % 4 == 0 && i + 1 < nCivs)
			s << "\n" << ind;
	}
	s.seekp(((long)s.tellp()) - 2); // Drop final comma
	s << ")\n";
	if(randPoints && !showActual)
		s << "Not shown: randomization" << std::endl;
	pointsDisplayString = new wstring(s.str());
}

// Assumes that they're sorted
/*int StartPointsAsHandicap::maxStartPoints() {

	return civs[nCivs - 1]->startPoints_actual();
}
// (obsolete)
double StartPointsAsHandicap::meanStartPoints() {

	double sum = 0;
	for(int i = 0; i < nCivs; i++)
		sum += civs[i]->startPoints_actual();
	return sum / nCivs;
}*/


bool StartPointsAsHandicap::isLeftPtsLessThanRight(MajorCiv* left, MajorCiv* right) {

	if(left->isHuman() && !right->isHuman())
		return true;
	if(right->isHuman() && !left->isHuman())
		return false;
	if(left->startPoints_configured() < right->startPoints_configured())
		return true;
	if(left->startPoints_configured() > right->startPoints_configured())
		return false;
	return left->id() < right->id();
}


bool StartPointsAsHandicap::isLeftCloserThanRight(MajorCiv* left, MajorCiv* right) {

	return left->dist() < right->dist();
}


StartPointsAsHandicap::MajorCiv::MajorCiv(PlayerTypes civId) :
		civId(civId), actualPointsDone(false),
		startPoints_c(-1), startPoints_a(-1), d(-1) {}

void StartPointsAsHandicap::MajorCiv::setStartPoints_configured(int pts) {

	startPoints_c = adjust(pts);
	actualPointsDone = false;
}

void StartPointsAsHandicap::MajorCiv::setStartPoints_actual(int pts) {

	startPoints_a = adjust(pts);
	actualPointsDone = true;
}

void StartPointsAsHandicap::MajorCiv::assignStartPoints() {

	if(!actualPointsDone) {
		startPoints_a = startPoints_c;
		actualPointsDone = true;
	}
	GET_PLAYER(civId).setAdvancedStartPoints(startPoints_a);
}

int StartPointsAsHandicap::MajorCiv::startPoints_configured() const {

	return startPoints_c;
}

int StartPointsAsHandicap::MajorCiv::startPoints_actual() const {

	return startPoints_a;
}

void StartPointsAsHandicap::MajorCiv::assignStartingPlot(CvPlot* plot) {

	GET_PLAYER(civId).setStartingPlot(plot);
}

void StartPointsAsHandicap::MajorCiv::setDist(int dist) {

	d = dist;
}

int StartPointsAsHandicap::MajorCiv::dist() const {

	return d;
}

int StartPointsAsHandicap::MajorCiv::id() const {

	return GET_PLAYER(civId).getID();
}

CvPlot* StartPointsAsHandicap::MajorCiv::startingPlot() const {

	return GET_PLAYER(civId).getStartingPlot();
}

bool StartPointsAsHandicap::MajorCiv::isHuman() const {

	return GET_PLAYER(civId).isHuman();
}

int StartPointsAsHandicap::MajorCiv::adjust(int pts) {

	if(isHuman())
		return -1;
	int minPts = GC.getInitCore().getAdvancedStartMinPoints();
	if(pts < minPts)
		return minPts;
	return pts;
}
// </advc.250b>
