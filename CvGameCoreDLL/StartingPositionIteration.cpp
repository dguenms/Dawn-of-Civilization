// advc.027: New file; see comment in header.

#include "CvGameCoreDLL.h"
#include "StartingPositionIteration.h"
#include "CvPlayerAI.h"
#include "CvTeamAI.h"
#include "CvGamePlay.h"
#include "CitySiteEvaluator.h"
#include "CvMap.h"
#include "CvArea.h"
#include "PlotRange.h"
#include "CvInfo_GameOption.h" // for StartingLocPercent handicap

using std::map;
using std::vector;
using std::pair;
using std::make_pair;

//#define SPI_LOG // Enables log file for starting position iteration

bool StartingPositionIteration::isDebug()
{
	#ifdef SPI_LOG
		return true;
	#else
		return false;
	#endif
}


StartingPositionIteration::StartingPositionIteration() :
	m_bRestrictedAreas(false), m_bScenario(false), m_bNormalizationTargetReady(false),
	m_pEval(NULL), m_pYieldValues(NULL), m_pYieldsPerArea(NULL),
	m_pPathDists(NULL), m_pPotentialSites(NULL)
{
	m_bScenario = GC.getInitCore().getWBMapScript();
	if (!GC.getDefineBOOL("ENABLE_STARTING_POSITION_ITERATION"))
		return;
	CvMap const& kMap = GC.getMap();
	if (kMap.numPlots() > GC.getDefineINT("SPI_PLOT_LIMIT"))
		return;
	/*	Bail on extremely overcrowded maps? SPI can't really deal with
		overlapping city radii, but neither can the BtS algorithm. */
	/*if (PlayerIter<CIV_ALIVE>::count() > 6 * GC.getGame().getRecommendedPlayers())
		return;*/

	/*	Generate a starting site for each civ, starting with humans,
		otherwise in a random order - just as CvGame::assignStartingPlots does.
		Map scripts might depend on this order. If a map script sets the
		starting sites, then we have to bail anyway, but we don't know that yet. */
	vector<CvPlayer*> apCivPlayers;
	for (PlayerRandIter<HUMAN,ANY_AGENT_RELATION> it(mapRand());
		it.hasNext(); ++it)
	{
		apCivPlayers.push_back(&(*it));
	}
	for (PlayerRandIter<CIV_ALIVE,ANY_AGENT_RELATION> it(mapRand());
		it.hasNext(); ++it)
	{
		if (!it->isHuman())
			apCivPlayers.push_back(&*it);
	}
	/*	For large team games (a matter of player count and average team size),
		I think the BtS algorithm will work better (i.e. less bad). */
	if (GC.getGame().isTeamGame() &&
		SQR((int)apCivPlayers.size()) > 36 * TeamIter<CIV_ALIVE>::count())
	{
		return;
	}
	/*	Pangaea overrides assignStartingPlots, but has relevant custom behavior
		only for team games (inland starts are prohibited then). */
	bool const bIgnoreScript = (GC.getInitCore().isPangaea() && !GC.getGame().isTeamGame());
	{
		bool bAllStartsFixed = m_bScenario;
		size_t i = 0;
		for (; i < apCivPlayers.size(); i++)
		{
			CvPlayer& kPlayer = *apCivPlayers[i];
			if (kPlayer.getStartingPlot() != NULL)
			{
				if (m_bScenario)
				{
					/*	Respect the per-plot StartingPlot flags in scenarios.
						But there can be fewer such plots than players. We'll
						deal with any players that don't have a starting site yet. */
					m_abFixedStart.set(kPlayer.getID(), true);
					continue;
				}
				/*	Meaning that, if a map script sets all starting sites in
					assignStartingPlots but still allows the default implementation,
					then starting position iteration is allowed but can't change
					the start areas. (for PerfectMongoose) */
				m_bRestrictedAreas = true;
				continue;
			}
			else bAllStartsFixed = false;
			gDLL->callUpdater();
			bool bSiteFoundByScript=false;
			bool bRestrictedAreas=false;
			CvPlot* pSite = kPlayer.findStartingPlot(
					&bSiteFoundByScript, &bRestrictedAreas);
			if (pSite == NULL || (bSiteFoundByScript && !bIgnoreScript))
				break;
			if (bRestrictedAreas)
				m_bRestrictedAreas = true;
			/*	Would rather not store sites at players until the end of our computations,
				but then findStartingPlot will return the same site over and over. */
			kPlayer.setStartingPlot(pSite);
		}
		if (bAllStartsFixed)
			return;
		/*	<advc.test> For getting an evaluation of a particular starting position
			(for particular RNG seeds set in CivilizationIV.ini). */
		/*int aiiForcedInitialPosition[][2] =
		{
			{22, 36}, {19, 13}, {29, 12}, {29, 23},
			{19, 29}, {32, 39}, {51, 11}, {55, 19},
		};
		for (int j = 0; j < ARRAYSIZE(aiiForcedInitialPosition); j++)
		{
			GET_PLAYER((PlayerTypes)j).setStartingPlot(&kMap.getPlot(
					aiiForcedInitialPosition[j][0], aiiForcedInitialPosition[j][1]), false);
		}*/ // </advc.test>
		if (i != apCivPlayers.size()) // Revert any changes and bail
		{
			for (PlayerIter<CIV_ALIVE> it; it.hasNext(); ++it)
				it->setStartingPlot(NULL);
			return;
		}
	} // Past this point, we'll have set sensible starting plots; won't revert anymore.

	// Precomputations (too costly to repeat in each iteration) ...

	m_pEval = createSiteEvaluator();
	PotentialSites potentialSiteGen(*m_pEval, m_bRestrictedAreas);
	if (potentialSiteGen.numSites() < apCivPlayers.size())
		return;
	/*for (PlayerIter<CIV_ALIVE> it; it.hasNext(); ++it) // (debug) Mark original sites with a ruin
		it->getStartingPlot()->setImprovementType(GC.getRUINS_IMPROVEMENT());*/
	// Remove the current solution. Just want the alternatives.
	potentialSiteGen.updateCurrSites();
	vector<CvPlot const*> apPotentialSites;
	potentialSiteGen.getPlots(apPotentialSites);
	/*for (size_t i = 0; i < apPotentialSites.size(); i++) // (debug) Mark alt. sites with a ruin
		GC.getMap().getPlotByIndex(GC.getMap().plotNum(*apPotentialSites[i])).setImprovementType(GC.getRUINS_IMPROVEMENT());*/

	EagerEnumMap<PlotNumTypes,scaled> yieldValues;
	map<CvArea const*,scaled> yieldsPerArea;
	{
		vector<scaled> arLandYields;
		CitySiteEvaluator yieldEval(m_pEval->getPlayer(), -1, /*bStartingLoc=*/false, true);
		FOR_EACH_ENUM(PlotNum)
		{
			CvPlot const& kPlot = kMap.getPlotByIndex(eLoopPlotNum);
			if (!kPlot.isPotentialCityWork())
				continue;
			// CitySiteEvaluator has many useful subroutines for this; handle it there.
			scaled rYieldVal = yieldEval.evaluateWorkablePlot(kPlot);
			yieldValues.set(eLoopPlotNum, rYieldVal);
			/*if(yieldValues.get(eLoopPlotNum) > 0) // (debug) Mark nonnegative-value plots with a ruin
				GC.getMap().getPlotByIndex(i).setImprovementType(GC.getRUINS_IMPROVEMENT());*/
			// Might possibly overflow w/o the divisor. Don't care about the scale anyway.
			rYieldVal /= 32;
			yieldsPerArea[kPlot.area()] += rYieldVal;
			if (!kPlot.isWater())
				arLandYields.push_back(rYieldVal);
		}
		m_rMedianLandYieldVal = stats::median(arLandYields);
	}

	DistanceTable const* pPathDists = NULL;
	{	// Temp data that I want to go out of scope
		// Need a vector of all sites. Add the original sites temporarily.
		for (size_t i = 0; i < apCivPlayers.size(); i++)
		{
			apPotentialSites.push_back(apCivPlayers[i]->getStartingPlot());
		}
		// Also want inter-site distances
		std::set<PlotNumTypes> sitePlotNums;
		for (size_t i = 0; i < apPotentialSites.size(); i++)
		{
			sitePlotNums.insert(apPotentialSites[i]->plotNum());
		}
		std::vector<CvPlot const*> relevantPlots;
		FOR_EACH_ENUM(PlotNum)
		{
			if (yieldValues.get(eLoopPlotNum) > 0 ||
				sitePlotNums.count(eLoopPlotNum) > 0)
			{
				relevantPlots.push_back(&kMap.getPlotByIndex(eLoopPlotNum));
			}
		}
		gDLL->callUpdater(); // Dunno if these are needed or have any effect really
		pPathDists = new DistanceTable(apPotentialSites, relevantPlots);
		gDLL->callUpdater();
		// Remove the original sites again
		for (size_t i = 0; i < apCivPlayers.size(); i++)
			apPotentialSites.pop_back();
	}
	// So that subroutines can read - but not write - these
	m_pYieldValues = &yieldValues;
	m_pYieldsPerArea = &yieldsPerArea;
	m_pPathDists = pPathDists;
	m_pPotentialSites = &potentialSiteGen;

	doIterations(potentialSiteGen); // May modify the potential sites

	m_sitesPerTeam.resize(MAX_CIV_TEAMS);
	if (GC.getGame().isTeamGame())
		assignSitesToTeams();
	else
	{
		for (size_t i = 0; i < apCivPlayers.size(); i++)
		{
			m_sitesPerTeam[apCivPlayers[i]->getTeam()].push_back(
					apCivPlayers[i]->getID());
		}
	}

	delete pPathDists;
	m_pPathDists = NULL;
}


StartingPositionIteration::~StartingPositionIteration()
{
	SAFE_DELETE(m_pEval);
}


NormalizationTarget* StartingPositionIteration::createNormalizationTarget() const
{
	if (!m_bNormalizationTargetReady)
		return NULL;
	NormalizationTarget& kResult = *new NormalizationTarget(
			*createSiteEvaluator(true), m_currSolutionAttribs);
	return &kResult;
}

// Allocates memory
CitySiteEvaluator* StartingPositionIteration::createSiteEvaluator(bool bNormalize) const
{
	/*	Teams have already received free tech at this point, so the player used
		for city site evaluation isn't irrelevant. (Its personality should be though.)
		Pick the player with the least tech, prefer human when breaking ties.
		But no 1-city challenge players! */
	bool const bOCC = GC.getGame().isOption(GAMEOPTION_ONE_CITY_CHALLENGE);
	CvPlayerAI const* pPlayer = NULL;
	int iBestPlayerVal = MAX_INT;
	for (PlayerAIIter<CIV_ALIVE> it; it.hasNext(); ++it)
	{
		int iVal = 10 * it->getTechScore();
		if (it->isHuman())
		{
			if (bOCC)
				iVal = MAX_INT;
			iVal--;
		}
		if (iVal < iBestPlayerVal)
		{
			iBestPlayerVal = iVal;
			pPlayer = &*it;
		}
	}
	CitySiteEvaluator* r = new CitySiteEvaluator(*pPlayer, -1, !bNormalize, bNormalize);
	// Evaluating the surroundings will be our job
	r->setIgnoreStartingSurroundings(true);
	return r;
}


StartingPositionIteration::PotentialSites::PotentialSites(
	CitySiteEvaluator const& kEval, bool bRestrictedAreas) :
	m_kEval(kEval)
{
	for (PlayerIter<CIV_ALIVE> it; it.hasNext(); ++it)
	{
		m_sitesClosestToCurrSite.insert(make_pair(
				it->getID(), new VoronoiCell()));
	}

	scaled const rMinFoundVal = computeMinFoundValue();
	std::set<CvArea const*> validAreas;
	if (bRestrictedAreas)
	{
		for (PlayerIter<CIV_ALIVE> it; it.hasNext(); ++it)
		{
			validAreas.insert(it->getStartingPlot()->area());
		}
	}
	CvMap const& kMap = GC.getMap();
	FOR_EACH_ENUM(PlotNum)
	{
		CvPlot const& kPlot = kMap.getPlotByIndex(eLoopPlotNum);
		if (bRestrictedAreas && validAreas.count(kPlot.area()) <= 0)
			continue;
		short iFoundValue = std::max<short>(0, m_kEval.evaluate(kPlot));
		if (iFoundValue >= rMinFoundVal)
		{
			// Randomize a little - mainly so that settling in place isn't a no-brainer
			iFoundValue = safeIntCast<short>(
					(iFoundValue + iFoundValue *
					((iFoundValue / rMinFoundVal - 1) * fixp(0.05) *
					(scaled::rand(mapRand(), NULL) - fixp(0.5)))).
					round());
			m_foundValuesPerSite.insert(make_pair(eLoopPlotNum, iFoundValue));
		}
	}
	uint const iPlayers = (uint)PlayerIter<CIV_ALIVE>::count();
	if (numSites() <= iPlayers)
		return;

	// "Clearing the neighborhood"

	EagerEnumMap<PlotNumTypes,scaled> arVicinityPenaltiesPerPlot;
	for (map<PlotNumTypes,short>::const_iterator itSite = m_foundValuesPerSite.begin();
		itSite != m_foundValuesPerSite.end(); ++itSite)
	{
		CvPlot const& p = kMap.getPlotByIndex(itSite->first);
		recordSite(p, itSite->second, true, arVicinityPenaltiesPerPlot);
	}
	while (numSites() > iPlayers * 8u)
	{
		/*	Stop earlier when running out of alternatives in some map region.
			(Tbd. - Perhaps better: take Voronoi cells with few sites left off limits.) */
		if (fewestPotentialSites() < 2 && numSites() < iPlayers * 15u)
			break;
		map<PlotNumTypes,short>::iterator minPos;
		scaled rMinVal = scaled::MAX;
		for (map<PlotNumTypes,short>::iterator it = m_foundValuesPerSite.begin();
			it != m_foundValuesPerSite.end(); ++it)
		{
			scaled rVal = it->second * std::max(fixp(0.3),
					1 - arVicinityPenaltiesPerPlot.get(it->first));
			if (rVal < rMinVal)
			{
				rMinVal = rVal;
				minPos = it;
			}
		}
		CvPlot const& kMinPlot = kMap.getPlotByIndex(minPos->first);
		short iMinFoundVal = minPos->second;
		m_foundValuesPerSite.erase(minPos);
		recordSite(kMinPlot, iMinFoundVal, false, arVicinityPenaltiesPerPlot);
	}
}


StartingPositionIteration::PotentialSites::~PotentialSites()
{
	for (PlayerIter<CIV_ALIVE> it; it.hasNext(); ++it)
	{
		delete m_sitesClosestToCurrSite[it->getID()];
	}
}


scaled StartingPositionIteration::PotentialSites::computeMinFoundValue()
{
	vector<short> aiFoundValuesPerCurrSite; // vector for stats::median
	short iWorstCurrFoundVal = MAX_SHORT;
	for (PlayerIter<CIV_ALIVE> it; it.hasNext(); ++it)
	{
		short iFoundVal = m_kEval.evaluate(*it->getStartingPlot());
		aiFoundValuesPerCurrSite.push_back(iFoundVal);
		m_foundValuesPerCurrSite.set(it->getID(), iFoundVal);
		iWorstCurrFoundVal = std::min(iWorstCurrFoundVal, iFoundVal);
	}
	scaled r = iWorstCurrFoundVal * fixp(0.88);
	r.increaseTo(stats::median(aiFoundValuesPerCurrSite) * fixp(0.7));
	return scaled::max(r, 1);
}

/*	(Could get the found value from m_foundValuesPerSite, but the callers
	happen to have it at hand.) */
void StartingPositionIteration::PotentialSites::recordSite(
	CvPlot const& kPlot, short iFoundValue, bool bAdd,
	EagerEnumMap<PlotNumTypes,scaled>& kVicinityPenaltiesPerPlot)
{
	// Update vicinity penalties
	int const iSign = (bAdd ? 1 : -1);
	for (PlotCircleIter it(kPlot, 8, false); it.hasNext(); ++it)
	{
		PlotNumTypes const eLoopPlot = it->plotNum();
		map<PlotNumTypes,short>::const_iterator pos = m_foundValuesPerSite.find(eLoopPlot);
		if (pos != m_foundValuesPerSite.end() && pos->second < iFoundValue)
		{
			kVicinityPenaltiesPerPlot.add(eLoopPlot, iSign *
					scaled(1, 4 << it.currPlotDist()));
			FAssert(!kVicinityPenaltiesPerPlot.get(eLoopPlot).isNegative());
		}
	}

	// Update Voronoi cells
	vector<PlayerTypes> aClosestPlayers;
	closestPlayers(kPlot, aClosestPlayers);
	if (aClosestPlayers.empty()) // Remote sites will be set by updateCurrSites
		return;
	for (size_t i = 0; i < aClosestPlayers.size(); i++)
	{
		VoronoiCell& kCell = *m_sitesClosestToCurrSite.find(aClosestPlayers[i])->second;
		PlotNumTypes ePlotNum = kPlot.plotNum();
		if (bAdd)
			kCell.insert(ePlotNum);
		else
		{
			VoronoiCell::iterator pos = kCell.find(ePlotNum);
			if (pos != kCell.end())
				kCell.erase(pos);
			else FAssert(pos != kCell.end());
		}
	}
}


void StartingPositionIteration::PotentialSites::closestPlayers(
	CvPlot const& kPlot, vector<PlayerTypes>& kResult) const
{
	FAssert(kResult.empty());
	vector<pair<int,PlayerTypes> > aiePlayersByDistance;
	CvMap const& kMap = GC.getMap();
	int iShortestDist = MAX_INT;
	int const iRemoteSiteThresh = 30;
	for (PlayerIter<CIV_ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		int iDist = kMap.stepDistance(&kPlot, itPlayer->getStartingPlot());
		if (iDist <= 0) // Don't include the current sites themselves in Voronoi cells
			return;
		if (!kPlot.isArea(itPlayer->getStartingPlot()->getArea()))
			iDist += 25;
		aiePlayersByDistance.push_back(make_pair(iDist, itPlayer->getID()));
		iShortestDist = std::min(iShortestDist, iDist);
	}
	if (iShortestDist > iRemoteSiteThresh)
		return;
	// Probably faster w/o sorting
	//std::sort(aiePlayersByDistance.begin(), aiePlayersByDistance.end());
	int const iDistThresh = std::min(2 * iShortestDist, iRemoteSiteThresh);
	for (size_t i = 0; i < aiePlayersByDistance.size(); i++)
	{
		if (aiePlayersByDistance[i].first < iDistThresh)
			kResult.push_back(aiePlayersByDistance[i].second);
		//else break;
	}
}


int StartingPositionIteration::PotentialSites::fewestPotentialSites() const
{
	int r = MAX_INT;
	for (map<PlayerTypes,VoronoiCell*>::const_iterator it =
		m_sitesClosestToCurrSite.begin();
		it != m_sitesClosestToCurrSite.end(); ++it)
	{
		r = std::min(r, (int)it->second->size());
	}
	return r;
}


void StartingPositionIteration::PotentialSites::updateCurrSites(bool bUpdateCells)
{
	CvMap const& kMap = GC.getMap();
	for (PlayerIter<CIV_ALIVE> it; it.hasNext(); ++it)
	{
		map<PlotNumTypes,short>::iterator pos = m_foundValuesPerSite.find(
				it->getStartingPlot()->plotNum());
		if (pos != m_foundValuesPerSite.end())
		{
			m_foundValuesPerCurrSite.set(it->getID(), pos->second);
			m_foundValuesPerSite.erase(pos);
		} /* If a player's current start site wasn't in foundValuesPerSite,
			 then that player's start site hasn't moved; no update needed. */
	}
	if (bUpdateCells)
	{
		for (PlayerIter<CIV_ALIVE> it; it.hasNext(); ++it)
		{
			m_sitesClosestToCurrSite[it->getID()]->clear();
		}
	}
	m_remoteSitesByAreaSize.clear();
	for (map<PlotNumTypes,short>::const_iterator it = m_foundValuesPerSite.begin();
		it != m_foundValuesPerSite.end(); ++it)
	{
		PlotNumTypes ePlotNum = it->first;
		CvPlot const& kPlot = kMap.getPlotByIndex(ePlotNum);
		vector<PlayerTypes> aClosestPlayers;
		closestPlayers(kPlot, aClosestPlayers);
		if (aClosestPlayers.empty())
		{
			m_remoteSitesByAreaSize.push_back(make_pair(
					kPlot.getArea().getNumTiles() * 100 + it->second, ePlotNum));
		}
		else if (bUpdateCells)
		{
			for (size_t i = 0; i < aClosestPlayers.size(); i++)
				m_sitesClosestToCurrSite[aClosestPlayers[i]]->insert(ePlotNum);
		}
	}
	std::sort(m_remoteSitesByAreaSize.rbegin(), m_remoteSitesByAreaSize.rend());
}


void StartingPositionIteration::PotentialSites::getPlots(
	vector<CvPlot const*>& r) const
{
	FAssert(r.empty());
	CvMap const& kMap = GC.getMap();
	for (map<PlotNumTypes,short>::const_iterator it = m_foundValuesPerSite.begin();
		it != m_foundValuesPerSite.end(); ++it)
	{
		r.push_back(&kMap.getPlotByIndex(it->first));
	}
}


StartingPositionIteration::VoronoiCell* StartingPositionIteration::
	PotentialSites::getCell(PlayerTypes eCurrSite) const
{
	map<PlayerTypes,VoronoiCell*>::const_iterator pos = m_sitesClosestToCurrSite.
			find(eCurrSite);
	if (pos == m_sitesClosestToCurrSite.end())
	{
		FErrorMsg("No current site found for given player");
		return NULL;
	}
	return pos->second;
}


PlotNumTypes StartingPositionIteration::PotentialSites::getRemoteSite(
	int iIndex) const
{
	if (iIndex >= (int)m_remoteSitesByAreaSize.size())
		return NO_PLOT_NUM;
	return m_remoteSitesByAreaSize[iIndex].second;
}


void StartingPositionIteration::PotentialSites::getCurrFoundValues(
	EagerEnumMap<PlayerTypes,short>& kFoundValuesPerPlayer) const
{
	for (PlayerIter<CIV_ALIVE> it; it.hasNext(); ++it)
	{
		map<PlotNumTypes,short>::const_iterator pos = m_foundValuesPerSite.
				find(it->getStartingPlot()->plotNum());
		if (pos != m_foundValuesPerSite.end())
			kFoundValuesPerPlayer.set(it->getID(), pos->second);
		else
		{
			short iCurrFoundVal = m_foundValuesPerCurrSite.get(it->getID());
			if (iCurrFoundVal > 0)
				kFoundValuesPerPlayer.set(it->getID(), iCurrFoundVal);
		}
	}
}


StartingPositionIteration::DistanceTable::DistanceTable(
	vector<CvPlot const*>& kSources, vector<CvPlot const*>& kDestinations)
{
	scaled rStartEraFactor = 1;
	if (GC.getNumEraInfos() > 1)
	{
		rStartEraFactor = scaled(GC.getGame().getStartEra(), GC.getNumEraInfos() - 1);
		rStartEraFactor = 1 - rStartEraFactor.sqrt() / 2;
	}
	m_iFirstFrontierCost = (short)(150 * rStartEraFactor).round();
	m_iSecondFrontierCost = (short)(155 * rStartEraFactor.pow(fixp(1.5))).round();

	CvMap const& kMap = GC.getMap();
	m_sourceIDs.resize(kMap.numPlots(), NOT_A_SOURCE);
	for (size_t i = 0; i < kSources.size(); i++)
	{
		m_sourceIDs[kSources[i]->plotNum()] = (SourceID)i;
	}
	// Need (fast) 2-way conversion for destination ids and plot numbers
	m_destinationIDs.resize(kMap.numPlots(), NOT_A_DESTINATION);
	m_destinationIDToPlotNum.resize(kDestinations.size(), NO_PLOT_NUM);
	for (size_t i = 0; i < kDestinations.size(); i++)
	{
		DestinationID eDst = (DestinationID)i;
		PlotNumTypes ePlotNum = kDestinations[i]->plotNum();
		m_destinationIDs[ePlotNum] = eDst;
		m_destinationIDToPlotNum[eDst] = ePlotNum;
	}
	m_distances.resize(kSources.size(),
			vector<short>(kDestinations.size(), MAX_SHORT));
	for (size_t i = 0; i < kSources.size(); i++)
	{
		CvPlot const& kSource = *kSources[i];
		computeDistances(kSource);
		/*	Destinations can be (potential) city sites or workable tiles.
			Water destinations are never city sites. To work a water tile,
			no ships are needed, so the frontier penalties applied by
			computeDistance are far too high. (computeDistances can't sort
			this out b/c it doesn't distinguish between moving a settler
			into/ through a plot and working a plot.) */
		for (size_t j = 0; j < kDestinations.size(); j++)
		{
			CvPlot const& kWaterDest = *kDestinations[j];
			if (!kWaterDest.isWater())
				continue;
			/*	Use the distance of the land destination closest to kSource
				that can work kDest. Bad land tiles aren't stored in the
				DistanceTable, so this will fail for e.g. an Ocean Fish workable
				only from a Snow tile. Fall back on CvMap::plotDist and
				CvPlot::sameArea in that case. */
			CvPlot const* pNearestLand = NULL;
			short iShortestDist = MAX_SHORT;
			bool bDest = false;
			bool bInnerRing = false;
			for (CityPlotIter it(kWaterDest, false); it.hasNext(); ++it)
			{
				if (!it->canFound())
					continue;
				bool bInnerRingLoop = (it.currID() < NUM_INNER_PLOTS);
				if (m_destinationIDs[it->plotNum()] != NOT_A_DESTINATION)
				{
					short iDist = d(kSource, *it);
					if (!bDest || iDist < iShortestDist)
					{
						bDest = true;
						iShortestDist = iDist;
						pNearestLand = &*it;
						bInnerRing = bInnerRingLoop;
					}
				}
				else if (!bDest && it->sameArea(kSource))
				{
					short iDist = static_cast<short>(kMap.plotDistance(&kSource, &*it));
					if (iDist < iShortestDist)
					{
						iShortestDist = iDist;
						pNearestLand = &*it;
						bInnerRing = bInnerRingLoop;
					}
				}
			}
			if (pNearestLand != NULL)
			{	// To account for the distance between pNearest and kWaterDest
				iShortestDist += getAvgCityDist() / 5;
				if (!bInnerRing)
					iShortestDist += getAvgCityDist() / 4;
				// Sea improvements are costlier than land improvements
				if (kWaterDest.getBonusType(NO_TEAM) != NO_BONUS)
					iShortestDist += (5 * getAvgCityDist()) / 8;
				setDistance(kSource, kWaterDest, iShortestDist);
			}
		}
	}
}

/*	Even with the inline keyword (and CvMap.h included in the header),
	the compiler doesn't want to inline this. Haven't tried force-inline;
	the amount time spent on this function isn't that great anyway. */
short StartingPositionIteration::DistanceTable::d(
	CvPlot const& kSource, CvPlot const& kDestination) const
{
	FAssertMsg(!kSource.isWater(), "kSource should be a (potential) city site");
	SourceID eSource = m_sourceIDs[kSource.plotNum()];
	DestinationID eDestination = m_destinationIDs[kDestination.plotNum()];
	FAssertBounds(0, m_distances.size(), eSource);
	FAssertBounds(0, m_distances[eSource].size(), eDestination);
	return m_distances[eSource][eDestination];
}


void StartingPositionIteration::DistanceTable::setDistance(
	CvPlot const& kSource, CvPlot const& kDestination, short iDistance)
{
	SourceID eSource = m_sourceIDs[kSource.plotNum()];
	DestinationID eDestination = m_destinationIDs[kDestination.plotNum()];
	if (eDestination != NOT_A_DESTINATION)
	{
		FAssertBounds(0, m_distances.size(), eSource);
		FAssert(eDestination < (int)m_distances[eSource].size());
		m_distances[eSource][eDestination] = iDistance;
	}
}


namespace
{
	class Node
	{
		// No reference b/c that would block the implicit assignment operator
		CvPlot const* m_pPlot;
		short m_iDistance;
	public:
		Node(CvPlot const& kPlot, short iDistance) : m_pPlot(&kPlot), m_iDistance(iDistance) {}
		CvPlot const& get() const { return *m_pPlot; }
		short getDistance() const { return m_iDistance; }
		// For inverse ordering by distance
		bool operator<(Node const& kOther) const { return m_iDistance > kOther.m_iDistance; }
	};
}


void StartingPositionIteration::DistanceTable::computeDistances(CvPlot const& kSource)
{
	bool const bSourceCoastal = kSource.isCoastalLand(-1);
	// Plain old Dijkstra's algorithm
	std::priority_queue<Node> q;
	q.push(Node(kSource, 0));
	/*	Keep track of visited nodes in order to save time. Can't use m_distances
		for this b/c it only contains destinations; may have to visit all plots. */
	EagerEnumMap<PlotNumTypes,bool> abReached;
	while (!q.empty())
	{
		Node v = q.top();
		q.pop();
		CvPlot const& kAt = v.get();
		setDistance(kSource, kAt, v.getDistance());
		{
			PlotNumTypes eAt = kAt.plotNum();
			if (abReached.get(eAt))
				continue;
			abReached.set(eAt, true);
		}
		FOR_EACH_ADJ_PLOT(kAt)
		{
			/*	Note: even if not yet reached, it may already be in q;
				that's what the abReached[iAt] check above is for. */
			if (abReached.get(pAdj->plotNum()))
				continue;
			short iDistance = stepDist(kAt, *pAdj, bSourceCoastal);
			if (iDistance < MAX_SHORT)
				q.push(Node(*pAdj, v.getDistance() + iDistance));
		}
		/*	Might be more efficient to call std::make_heap once after pushing
			to the back of a vector (i.e. no priority_queue). Hard to say. */
	}
}

/*	If the scale of the distances is changed, the value returned by
	getAvgCityDist needs to be adjusted. */
short StartingPositionIteration::DistanceTable::stepDist(
	CvPlot const& kFrom, CvPlot const& kTo, bool bSourceCoastal) const
{
	static const TerrainTypes eShallowTerrain = GC.getWATER_TERRAIN(true);
	if (kTo.isImpassable() || GC.getMap().isSeparatedByIsthmus(kFrom, kTo))
		return MAX_SHORT;

	// Land to shallow water and shallow to deep water are frontiers
	short const iFrontierAdjustment = (bSourceCoastal ? -1 : 1) * 10;
	bool const bDiagonal = (kFrom.getX() != kTo.getX() && kFrom.getY() != kTo.getY());
	if (!kTo.isWater()) // Land to land, water to land
		return (bDiagonal ? 12 : 9);
	if (!kFrom.isWater()) // Land to water
	{
		if (kTo.getTerrainType() == eShallowTerrain)
			return m_iFirstFrontierCost + iFrontierAdjustment;
		// (Land to ocean. Can't normally be adjacent.)
		return m_iFirstFrontierCost + m_iSecondFrontierCost + 2 * iFrontierAdjustment;
	}
	else if (kFrom.getTerrainType() == eShallowTerrain)
	{
		if (kTo.getTerrainType() == eShallowTerrain) // Shallow to shallow
			return 5;
		/*	Shallow to ocean: Here we could be more sophisticated by
			shifting some of the cost to a case
			'ocean adjacent to shallow water -> ocean not adjacent to shallow water'
			-- to account for the possibility of border spread. Might be too slow. */
		return m_iSecondFrontierCost + iFrontierAdjustment;
	}
	return 4; // Ocean to water (shallow or deep)
}


StartingPositionIteration::Step::Step()
{
	for (PlayerIter<CIV_ALIVE> it; it.hasNext(); ++it)
	{
		m_originalPosition.push_back(make_pair(
				it->getID(), it->getStartingPlot()));
	}
}


void StartingPositionIteration::Step::move(PlayerTypes ePlayer, CvPlot& kTo)
{
	m_moves.push_back(std::make_pair(ePlayer, &kTo));
}


void StartingPositionIteration::Step::take()
{
	for (size_t i = 0; i < m_moves.size(); i++)
	{
		GET_PLAYER(m_moves[i].first).setStartingPlot(
				m_moves[i].second);
	}
}


void StartingPositionIteration::Step::takeBack()
{
	for (size_t i = 0; i < m_originalPosition.size(); i++)
	{
		GET_PLAYER(m_originalPosition[i].first).setStartingPlot(
				m_originalPosition[i].second);
	}
}

PlayerTypes StartingPositionIteration::Step::getFirstMovePlayer() const
{
	if (m_moves.empty())
		return NO_PLAYER;
	return m_moves[0].first;
}

// (Overloading operator<< for a nested private class would be messy)
std::string StartingPositionIteration::Step::debugStr() const
{
	std::ostringstream r;
	for (size_t i = 0; i < m_moves.size(); i++)
	{
		CvPlot const* pTo = m_moves[i].second;
		CvPlot const* pFrom = NULL;
		for (size_t j = 0; j < m_originalPosition.size(); j++)
		{
			if (m_originalPosition[j].first == m_moves[i].first)
			{
				pFrom = m_originalPosition[j].second;
				break;
			}
		}
		if (pFrom == NULL)
		{
			FAssert(pFrom != NULL);
			continue;
		}
		r << "Move player " << (int)m_moves[i].first << " from (" <<
				pFrom->getX() << "," << pFrom->getY() << ") to (" <<
				pTo->getX() << "," << pTo->getY() << ")";
		if (!pFrom->sameArea(*pTo))
			r << " [different landmass]";
		r << "\n";
	}
	return r.str();
}


void StartingPositionIteration::evaluateCurrPosition(
	SolutionAttributes& kResult, bool bLog) const
{
	EagerEnumMap<PlayerTypes,short> foundValues;
	m_pPotentialSites->getCurrFoundValues(foundValues);
	computeStartValues(foundValues, kResult, bLog);
	kResult.m_rStartPosVal = startingPositionValue(kResult);
}


StartingPositionIteration::SpaceEvaluator::SpaceEvaluator(
	DistanceTable const& kDists,
	EagerEnumMap<PlotNumTypes,scaled> const& kYieldValues, bool bLog)
:	m_kDists(kDists), m_kYieldValues(kYieldValues), m_bLog(bLog)
{
	CvMap const& kMap = GC.getMap();
	// Treat distances beyond this threshold as infinite in order to save time
	m_iDistThresh = (word)((5 * kDists.getLongDist()) / 4);
	m_iAvgCityDist = kDists.getAvgCityDist();
	// Use unsigned types because that'll make exponentiation a wee bit faster
	word const iDistThresh = m_iDistThresh;
	word const iAvgCityDist = (word)kDists.getAvgCityDist();
	/*	Will essentially measure distances from the edge of the starting city radius
		instead of the starting city tile */
	m_iDistSubtr = iAvgCityDist / 2;
	word const iDistSubtr = m_iDistSubtr;
	FOR_EACH_ENUM(PlotNum)
	{
		if (kYieldValues.get(eLoopPlotNum) <= 0)
			continue;
		claim_t rSum = 0;
		for (PlayerIter<CIV_ALIVE> it; it.hasNext(); ++it)
		{
			CvPlot const& kStartPlot = *it->getStartingPlot();
			CvPlot const& kLoopPlot = kMap.getPlotByIndex(eLoopPlotNum);
			if (kMap.plotDistance(&kStartPlot, &kLoopPlot) <= 2)
			{
				// Accounted for by found values
				m_sumOfClaims.set(eLoopPlotNum, 0);
				goto next_plot;
			}
			short iDist = kDists.d(kStartPlot, kLoopPlot) - iDistSubtr;
			if (iDist > iDistThresh)
				continue;
			rSum += claim_t(1, std::max<short>(1, iDist));
		}
		m_sumOfClaims.set(eLoopPlotNum, rSum);
		next_plot: continue;
	}

	for (PlayerIter<CIV_ALIVE> it; it.hasNext(); ++it)
		computeSpaceValue(it->getID());
}

//#define DEBUG_SPACE_BREAKDOWN
#ifdef DEBUG_SPACE_BREAKDOWN
struct BreakDownData { PlotNumTypes ePlot; scaled rYieldVal; scaled rAccessFactor;
	BreakDownData(PlotNumTypes ePlot, scaled rYieldVal, scaled rAccessFactor) :
	ePlot(ePlot), rYieldVal(rYieldVal), rAccessFactor(rAccessFactor) {}
	bool operator<(BreakDownData const& kOther) const{ return ePlot < kOther.ePlot; } };
#endif

void StartingPositionIteration::SpaceEvaluator::computeSpaceValue(PlayerTypes ePlayer)
{
	#ifdef DEBUG_SPACE_BREAKDOWN
		vector<pair<scaled,BreakDownData> > aSpaceBreakDown;
	#endif
	CvPlot const& kStartPlot = *GET_PLAYER(ePlayer).getStartingPlot();
	scaled rSpaceVal;
	word const iDistThresh = m_iDistThresh;
	word const iAvgDist = m_iAvgCityDist;
	word const iDistSubtr = m_iDistSubtr;
	scaled const rMaxClaimExp = 2 + (GC.getGame().isOption(GAMEOPTION_ALWAYS_PEACE) ?
			fixp(1/3.) : 0);
	// Low-level performance optimizations ...
	static vector<claim_t> arDelayCache = cacheDelayFactors(iDistThresh);
	#if MAX_CIV_PLAYERS > 25
		int const iCivsAlive = PlayerIter<CIV_ALIVE>::count();
	#endif
	// Use friend status to avoid FOR_EACH_ENUM(PlotNum)
	DistanceTable::SourceID const eSrc = m_kDists.m_sourceIDs[kStartPlot.plotNum()];
	for (size_t i = 0; i < m_kDists.m_distances[eSrc].size(); i++)
	{
		DistanceTable::DestinationID const eDst = (DistanceTable::DestinationID)i;
		PlotNumTypes eDestPlot = m_kDists.m_destinationIDToPlotNum[eDst];
		claim_t rSumOfClaims = m_sumOfClaims.get(eDestPlot);
		// (For investigating a particular access factor in the debugger:)
		/*CvPlot const& kDest = kMap.getPlotByIndex(eDestPlot);
		FAssert(kDest.getX() !=  || kDest.getY() !=  || kStartPlot.getX() !=  || kStartPlot.getY() != );*/
		if (rSumOfClaims <= 0)
			continue;
		short iStartDist = m_kDists.m_distances[eSrc][eDst];
		if (iStartDist > iDistThresh)
			continue;
		word iDist = (word)std::max(1, iStartDist - iDistSubtr);

		claim_t rClaim(1, iDist);
		rClaim /= rSumOfClaims;
		/*	If one player is twice as far away than the other, then the first player
			does not have a 1 in 3 chance to claim the plot. 1 in 9 sounds more accurate,
			but I want to reflect, to some extent, the possibility of claiming the plot
			militarily (except in Always Peace games; see rMaxClaimExp above).
			So let's not quite square the proportion. */
		// Not worth the extra time on super-huge maps
		#if MAX_CIV_PLAYERS > 25 // Make sure not to branch here w/ the 18-civ DLL
		if (iCivsAlive > 25)
		{
			rClaim *= rClaim;
		}
		else
		#endif
		{
			//rClaim.exponentiate(claim_t(190, 100));
			/*  Actually, the longer the distance of the claimants, the less decisive
				the differences in distance become. */
			claim_t rExp(std::max(iDist - iAvgDist, 0), iDistThresh - iAvgDist + 1);
			rExp = rMaxClaimExp - rExp;
			// Don't want to punish the closest claimant through a high exponent though
			if (rClaim > claim_t(1, 2))
				rExp.decreaseTo(claim_t(3, 2));
			rClaim.exponentiate(rExp);
		}
		// A small competing claim shouldn't make a difference
		rClaim.decreaseTo(claim_t(56, 100));
		/*	Apart from competition, nearby plots are better than remote ones.
			How much better really depends on the shape of the space for expansion;
			can't take that into account here. It's fair to say that remote plots
			tend to become worked later than nearby plots, and that an oblong shape
			is undesirable. Delay being the more important of the two reasons for
			reducing the yield value of a plot. */
		// (formula moved into cacheDelayFactors)
		scaled rAccessFactor = (rClaim * arDelayCache[iDist]).convert();
		scaled rYieldVal = m_kYieldValues.get(eDestPlot);
		rSpaceVal += rYieldVal * rAccessFactor;

		#ifdef DEBUG_SPACE_BREAKDOWN
			aSpaceBreakDown.push_back(make_pair(rYieldVal*rAccessFactor,BreakDownData(eDestPlot,rYieldVal,rAccessFactor)));
		#endif
	}
	#ifdef DEBUG_SPACE_BREAKDOWN
	if (m_bLog)
	{
		std::ostringstream out;
		out << "\nSpace breakdown for player" << ePlayer << "\n";
		std::sort(aSpaceBreakDown.rbegin(),aSpaceBreakDown.rend());
		uscaled rSumZero, rSumOne, rSumTwo, rSum3to9;
		for(size_t i = 0; i < aSpaceBreakDown.size(); i++) {
			if(aSpaceBreakDown[i].first.round() > 1)
				out << aSpaceBreakDown[i].first.round() << "="<< aSpaceBreakDown[i].second.rYieldVal.round() << "*" << aSpaceBreakDown[i].second.rAccessFactor.str(100) <<" (" << kMap.getPlotByIndex(aSpaceBreakDown[i].second.ePlot).getX() << "," << kMap.getPlotByIndex(aSpaceBreakDown[i].second.ePlot).getY() << ")\n";
			if(aSpaceBreakDown[i].first.round() == 0)
				rSumZero += aSpaceBreakDown[i].first;
			else if(aSpaceBreakDown[i].first.round() == 1)
				rSumOne += aSpaceBreakDown[i].first;
			else if(aSpaceBreakDown[i].first.round() == 2)
				rSumTwo += aSpaceBreakDown[i].first;
			else if(aSpaceBreakDown[i].first.round() < 10)
				rSum3to9 += aSpaceBreakDown[i].first;
		}
		out << "Near-0 space values sum up to " << rSumZero.round() << "\n";
		out << "Near-1 space values sum up to " << rSumOne.round() << "\n";
		out << "Near-2 space values sum up to " << rSumTwo.round() << "\n";
		out << "(3,9)-space values sum up to " << rSum3to9.round() << "\n";
		out << "All the rest sums up to " << (rSpaceVal - rSumZero - rSumOne - rSumTwo - rSum3to9).round() << "\n";
		out << std::endl;
		gDLL->logMsg("StartingPos.log", out.str().c_str(), false, false);
	}
	#endif
	m_spaceValues.set(ePlayer, rSpaceVal);
}

/*	Returning by value. Shouldn't really matter and allows me to keep the cache
	local to computeSpaceValue above. */
vector<StartingPositionIteration::SpaceEvaluator::claim_t>
StartingPositionIteration::SpaceEvaluator::cacheDelayFactors(word iMaxDist)
{
	std::vector<claim_t> aResult(iMaxDist);
	claim_t const rDiv = iMaxDist * claim_t(140, 100);
	for (word iDist = 1; iDist < iMaxDist; iDist++)
	{
		claim_t rDelay(iDist);
		/*	Weird formula - with iDist in both base and exponent, but seems to result
			in the kind of hyperbola I had in mind.
			ScaledNum::exponentiate is pretty slow for large bases. It was by far the
			biggest time sink of the whole SPI algorithm; hence this cache.
			(Exponentiating 1/iDist doesn't help either as very small bases aren't
			supported at all by ScaledNum.) */
		rDelay.exponentiate(iDist / rDiv);
		aResult[iDist] = claim_t(115, 100) / rDelay;
		// For plots very close to kStartPlot, the exact distances shouldn't matter
		aResult[iDist].decreaseTo(claim_t(56, 100));
	}
	return aResult;
}

// The results are on the scale of AIFoundValue
void StartingPositionIteration::computeStartValues(
	EagerEnumMap<PlayerTypes,short> const& kFoundValues,
	SolutionAttributes& kResult, bool bLog) const
{
	#ifdef SPI_LOG
		std::ostringstream out;
		if (bLog)
			out << "Evaluating starting position ...\n\n";
	#endif

	// The computationally most expensive part:
	SpaceEvaluator spaceEval(*m_pPathDists, *m_pYieldValues, bLog);

	/*	Compute these upfront b/c it depends on the typical distance between
		starting sites whether a given distance is "too close" */
	EagerEnumMap<PlayerTypes,scaled> rivalDistFactors;
	scaled const rTypicalDistFactor = computeRivalDistFactors(rivalDistFactors, false);
	// Need this once for all rivals and once just for those in the same area
	EagerEnumMap<PlayerTypes,scaled> sameAreaRivalDistFactors;
	scaled rSameAreaTargetDistFactor = computeRivalDistFactors(
			sameAreaRivalDistFactors, true) * fixp(4/3.);
	// Need to know the distribution before computing the actual per-player values
	vector<scaled> arAreaYieldsPerPlayer;
	EagerEnumMap<PlayerTypes,scaled> areaYieldsPerPlayer;
	EagerEnumMap<PlayerTypes,scaled> spaceValues;
	int const iCivEverAlive = PlayerIter<CIV_ALIVE>::count();
	for (PlayerIter<CIV_ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		scaled rSpaceVal = spaceEval.getSpaceValue(itPlayer->getID());
		CvPlot const& kStartPlot = *itPlayer->getStartingPlot();
		/*	Area size needs to be taken into account explicitly b/c empires spread
			across multiple areas are difficult to defend and pay colony maintenance */
		scaled rAreaYields;
		map<CvArea const*,scaled>::const_iterator pos = m_pYieldsPerArea->
				find(kStartPlot.area());
		if (pos != m_pYieldsPerArea->end())
			rAreaYields = pos->second;
		int iSameAreaRivals = 0;
		for (PlayerIter<CIV_ALIVE> itRival; itRival.hasNext(); ++itRival)
		{
			if (&*itRival != &*itPlayer &&
				kStartPlot.sameArea(*itRival->getStartingPlot()))
			{
				iSameAreaRivals++;
			}
		}
		rAreaYields /= 1 + iSameAreaRivals;
		areaYieldsPerPlayer.set(itPlayer->getID(), rAreaYields);
		arAreaYieldsPerPlayer.push_back(rAreaYields);
		spaceValues.set(itPlayer->getID(), rSpaceVal);
	}

	vector<scaled> arFoundValues;
	vector<scaled> arSpaceValues;
	scaled const rMedianAreaYield = scaled::max(stats::median(arAreaYieldsPerPlayer), 1);
	for (PlayerIter<CIV_ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		scaled rAreaYields = areaYieldsPerPlayer.get(itPlayer->getID());
		scaled rRatio = rAreaYields / rMedianAreaYield;
		scaled rTolerance = fixp(0.23);
		if (rRatio + rTolerance < 1)
			spaceValues.multiply(itPlayer->getID(), rRatio + rTolerance);
		/*	If possible, we want there to be room for the core cities in
			the player's starting area. */
		scaled rTargetMinYields = GC.getInfo(GC.getMap().getWorldSize()).
				getTargetNumCities() * fixp(0.78) * m_rMedianLandYieldVal * NUM_CITY_PLOTS;
		// Adjust to crowdedness
		rTargetMinYields *= scaled(
				GC.getGame().getRecommendedPlayers(), iCivEverAlive).sqrt();
		// No colony maintenance if vassals are disabled
		if (GC.getGame().isOption(GAMEOPTION_NO_VASSAL_STATES))
			rTargetMinYields *= fixp(0.82);
		rRatio = rAreaYields / rTargetMinYields;
		if (rRatio < 1)
			spaceValues.multiply(itPlayer->getID(), rRatio.pow(fixp(0.36)));
		arFoundValues.push_back(kFoundValues.get(itPlayer->getID()));
		arSpaceValues.push_back(spaceValues.get(itPlayer->getID()));
	}
	
	scaled const rMedianFoundValue = stats::median(arFoundValues);
	scaled const rMedianSpaceValue = stats::median(arSpaceValues);

	kResult.m_volatilityValues.reset();
	CvGame const& kGame = GC.getGame();
	EraTypes const eStartEra = kGame.getStartEra();
	/*	Adjust this to set the overall balance between city radius
		and space for expansion */
	scaled rBaseSpaceWeight = fixp(2.25);
	if (eStartEra <= 1)
	{
		if (kGame.isOption(GAMEOPTION_NO_BARBARIANS))
			rBaseSpaceWeight *= fixp(1.025);
		else if (kGame.isOption(GAMEOPTION_RAGING_BARBARIANS))
			rBaseSpaceWeight *= fixp(0.95);
	}
	int const iAvgCityDist = m_pPathDists->getAvgCityDist();
	for (PlayerIter<CIV_ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		scaled rFoundValue = kFoundValues.get(itPlayer->getID());
		// Anticipate normalization
		if (!m_bScenario && rFoundValue < rMedianFoundValue)
		{
			rFoundValue = std::min((rMedianFoundValue + rFoundValue) / 2,
					rFoundValue + rMedianFoundValue / 10);
		}
		scaled rSpaceWeight = rBaseSpaceWeight;
		if (rMedianSpaceValue > 0)
		{
			rSpaceWeight *= rMedianFoundValue / rMedianSpaceValue;
			// Avoid overflow (at a later point) on extremely crowded maps
			rSpaceWeight.decreaseTo(50);
		}
		scaled rFoundWeight = 1;
		scaled rFromSpaceValue = spaceValues.get(itPlayer->getID());
		scaled rSpaceRatio;
		if (rMedianFoundValue > 0 && rMedianSpaceValue > 0 &&
			rFoundValue > 0)
		{	// Not healthy if these are far apart
			scaled rFoundRatio = rFoundValue / rMedianFoundValue;
			rSpaceRatio = rFromSpaceValue / rMedianSpaceValue;
			scaled rSmaller = std::min(rFoundRatio, rSpaceRatio);
			scaled rGreater = std::max(rFoundRatio, rSpaceRatio);
			if (rGreater > 0)
			{
				kResult.m_volatilityValues.add(itPlayer->getID(),
						scaled::max(0, 1 - (rSmaller / rGreater - fixp(0.1)) / 2));
			}
			/*	Very little space is always a problem and very very little
				really mustn't happen */
			scaled const rThresh = fixp(0.85);
			if (rSpaceRatio < rThresh)
			{
				kResult.m_volatilityValues.add(itPlayer->getID(),
						(rThresh - rSpaceRatio).pow(2) / rThresh);
				scaled rFoundMinus = rSpaceRatio.pow(2) * rFoundWeight;
				rFoundWeight -= rFoundMinus;
				/*	If space values are generally higher than found values, then
					shifting weight to space might increase the start value although
					the player actually has too little space. Hence the divisor. */
				rSpaceWeight += rFoundMinus / rBaseSpaceWeight;
			}
		}
		else FAssert(false);
		CvPlot const& kStartPlot = *itPlayer->getStartingPlot();
		int iWarTargets = 0;
		int iSameAreaTradeTargets = 0;
		int iDifferentAreaTradeTargets = 0;
		for (PlayerIter<CIV_ALIVE> itRival; itRival.hasNext(); ++itRival)
		{
			if (&*itRival == &*itPlayer)
				continue;
			CvPlot const& kRivalStartPlot = *itRival->getStartingPlot();
			short const iDist = m_pPathDists->d(kStartPlot, kRivalStartPlot);
			if (kStartPlot.sameArea(kRivalStartPlot))
			{
				iSameAreaTradeTargets++;
				iWarTargets++;
			}
			else if (iDist < 8 * iAvgCityDist)
				iDifferentAreaTradeTargets++;
		}
		scaled rWarFactor = 1;
		if (!kGame.isOption(GAMEOPTION_ALWAYS_PEACE))
		{
			if (iWarTargets == 0)
			{
				rWarFactor = fixp(1.1);
				// Having no war targets is not good when (somewhat) short on space
				scaled rSpaceRatioAdjusted = rSpaceRatio - fixp(0.08);
				if (rSpaceRatioAdjusted < 1)
				{
					rSpaceRatioAdjusted.increaseTo(fixp(0.5));
					rWarFactor = (fixp(1.5) * rWarFactor + rSpaceRatioAdjusted) / fixp(2.5);
				}
				/*	Strong starting site is less useful
					if there is no competition for space */
				scaled rFoundMinus = fixp(1/4.) * rFoundWeight;
				rFoundWeight -= rFoundMinus;
				rSpaceWeight += rFoundMinus / rBaseSpaceWeight;
			}
			else
			{
				scaled const rBaseWarFactor = fixp(0.4);
				rWarFactor = rBaseWarFactor;
				rWarFactor /= scaled(1 + std::min(3, iWarTargets) * rWarFactor).sqrt();
				rWarFactor /= rBaseWarFactor; // normalize
			}
		}
		scaled const rBaseTradeFactor = fixp(0.82);
		scaled rTradeFactor = rBaseTradeFactor;
		int const iTotalTradeTargets = iSameAreaTradeTargets + iDifferentAreaTradeTargets;
		if (iTotalTradeTargets > 0)
		{
			if (kGame.isOption(GAMEOPTION_NO_TECH_TRADING))
				rTradeFactor = fixp(0.4);
			else if (kGame.isOption(GAMEOPTION_NO_TECH_BROKERING))
				rTradeFactor -= fixp(0.04) * (std::min(4, iTotalTradeTargets) - 1);
			scaled const rTradeVal = iSameAreaTradeTargets + iDifferentAreaTradeTargets *
					(1 + fixp(0.2) * per100(GC.getDefineINT(CvGlobals::OVERSEAS_TRADE_MODIFIER)));
			rTradeFactor *= (1 + rTradeVal * rTradeFactor).pow(fixp(1/3.));
		}
		rTradeFactor /= fixp(1.5) * rBaseTradeFactor; // Normalize; looks nicer in the log file.
		// The above seems to give war targets and trade partners a bit much weight
		scaled rTradeWarDilution(1, 4);
		rWarFactor -= (rWarFactor - 1) * rTradeWarDilution;
		rTradeFactor -= (rTradeFactor - 1) * rTradeWarDilution;

		scaled rRivalDistFactor = rivalDistFactors.get(itPlayer->getID());
		scaled rSameAreaRivalDistFactor = sameAreaRivalDistFactors.get(itPlayer->getID());
		if (rRivalDistFactor < rTypicalDistFactor)
		{
			rRivalDistFactor /= rTypicalDistFactor;
			rRivalDistFactor.exponentiate(fixp(2/3.));
			/*	Doesn't hurt players that much beyond the effect already covered
				by rFromExpansionSpace. And overestimating the impact of close
				neighbors will make it likelier that SPI places civs with too much
				space close together to compensate. Better to discourage close starts
				through volatility. */
			kResult.m_volatilityValues.add(itPlayer->getID(), 2 * scaled::max(0,
					1 - rRivalDistFactor - fixp(1/16.)));
		}
		else
		{
			rRivalDistFactor = 1;
			/*	Too far apart isn't good either. The algorithm may try to balance a
				(sub-)continent with too much space overall by giving everyone there a
				coastal start and thus an awkward empire shape. Don't really want that. */
			if (rSameAreaTargetDistFactor > 0 &&
				rSameAreaRivalDistFactor > rSameAreaTargetDistFactor)
			{
				rSameAreaRivalDistFactor /= rSameAreaTargetDistFactor;
				rSameAreaRivalDistFactor.exponentiate(fixp(0.5));
				kResult.m_volatilityValues.add(itPlayer->getID(), scaled::max(0,
						rSameAreaRivalDistFactor - 1));
			}
			else if (rSameAreaRivalDistFactor == 0) // isolated
			{
				/*	All things equal, let's avoid isolation. And let's not try too
					hard to make up for isolation w/o sufficient space through a
					high found value. (That'll further increase volatility.) */
				kResult.m_volatilityValues.add(itPlayer->getID(), fixp(0.1));
			}
			// Otherwise, distances are sufficiently covered by rFromExpansionSpace.
		}
		rFromSpaceValue *= rSpaceWeight;
		scaled rRivalMultiplier = rWarFactor * rTradeFactor * rRivalDistFactor;

		/*	Note: NormalizationTarget relies on the start value formula having
			this basic form ((FoundValue * a + b) * c). */
		scaled rStartVal = rFoundValue * rFoundWeight + rFromSpaceValue;
		rStartVal *= rRivalMultiplier;

		kResult.m_startValues.set(itPlayer->getID(), rStartVal);
		kResult.m_foundValues.set(itPlayer->getID(), rFoundValue);
		kResult.m_foundWeights.set(itPlayer->getID(), rFoundWeight);
		kResult.m_rivalMultipliers.set(itPlayer->getID(), rRivalMultiplier);
		/*	Thought this might be a fun option, but actually doesn't seem
			all that interesting to disable volatility. */
		/*static bool const bIgnoreVolatility = GC.getDefineBOOL("ALLOW_UNUSUAL_STARTS", false);
		if (bIgnoreVolatility)
			kResult.m_volatilityValues.set(itPlayer->getID(), 0);*/
		#ifdef SPI_LOG
		scaled rFromFoundVal = rFoundValue * rFoundWeight;
		if (bLog)
		{
			out << "Site #" << (int)itPlayer->getID() << ": " <<
					CvString(itPlayer->getName()).c_str() << ", (" <<
					kStartPlot.getX() << "," << kStartPlot.getY() << ")\n";
			out << "From found value: " << rFromFoundVal.str(1);
			if (rFoundWeight.getPercent() != 100)
				out << " (weight " << rFoundWeight.str(100) << ")";
			out << "\n";
			out << "From exp. space: " << rFromSpaceValue.str(1) << "\n";
			if (rRivalDistFactor.getPercent() < 100)
				out << "Rival distance factor: " << rRivalDistFactor.str(100) << "\n";
			else if (rSameAreaRivalDistFactor > rSameAreaTargetDistFactor &&
				rSameAreaRivalDistFactor.getPercent() > 100)
			{
				out << "Rival distance factor: " << rSameAreaRivalDistFactor.str(100) << "\n";
			}
			if (kResult.m_volatilityValues.get(itPlayer->getID()) > 0)
				out << "Volatility: " << kResult.m_volatilityValues.get(itPlayer->getID()).str(100) << "\n";
			out << "War factor (" << iWarTargets << " pot. enemies): " << rWarFactor.str(100) << "\n";
			out << "Trade factor (" << iTotalTradeTargets << " pot. partners): " << rTradeFactor.str(100) << "\n";
			out << "Start value: " << rStartVal.str(1) << "\n\n";
		}
		#endif
	}
	#ifdef SPI_LOG
	if (bLog)
	{
		out << std::endl;
		gDLL->logMsg("StartingPos.log", out.str().c_str(), false, false);
	}
	#endif
}

/*	Returns a "typical" distance factor and stores per-player (i.e. per starting site)
	distances in the out parameter. Distance factors account for the path distances
	between the current starting sites. They're on the scale of DistanceTable::d.
	"Rivals" refers to any pair of different civ players here, even if they're
	on the same team. (Sites will probably get swapped around later, so same-team
	relationships aren't reliable at this point.) */
scaled StartingPositionIteration::computeRivalDistFactors(
	EagerEnumMap<PlayerTypes,scaled>& kResult, bool bSameArea) const
{
	vector<scaled> arRivalDistFactors;
	for (PlayerIter<CIV_ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		vector<short> aiRivalDists;
		CvPlot const& kStartPlot = *itPlayer->getStartingPlot();
		for (PlayerIter<CIV_ALIVE> itRival; itRival.hasNext(); ++itRival)
		{
			if (&*itPlayer == &*itRival)
				continue;
			if (!bSameArea || kStartPlot.sameArea(*itRival->getStartingPlot()))
			{
				aiRivalDists.push_back(m_pPathDists->d(
						kStartPlot, *itRival->getStartingPlot()));
			}
		}
		scaled rDistFactor = weightedDistance(aiRivalDists);
		kResult.set(itPlayer->getID(), rDistFactor);
		arRivalDistFactors.push_back(rDistFactor);
	}
	scaled rTypicalDistFactor;
	if (!arRivalDistFactors.empty())
	{
		rTypicalDistFactor = stats::median(arRivalDistFactors);
		rTypicalDistFactor = std::min(fixp(1.25) * rTypicalDistFactor,
				(rTypicalDistFactor + 3 * m_pPathDists->getAvgCityDist()) / 2);
	}
	return rTypicalDistFactor;
}

// Need this little formula in two places. Param isn't const b/c I need to sort it.
scaled StartingPositionIteration::weightedDistance(vector<short>& kDistances)
{
	std::sort(kDistances.begin(), kDistances.end());
	scaled r;
	scaled rSumOfWeights;
	for (size_t i = 0; i < kDistances.size(); i++)
	{
		scaled rWeight(1, (int)i + 1);
		scaled rPlus = kDistances[i] * rWeight;
		// Further rivals beyond the closest can only reduce rDistFactor
		rPlus.decreaseTo(kDistances[0]);
		rPlus *= rWeight;
		rSumOfWeights += rWeight;
		r += rPlus;
	}
	if (rSumOfWeights.isPositive())
		r /= rSumOfWeights;
	return r;
}


scaled StartingPositionIteration::outlierValue(
	EagerEnumMap<PlayerTypes,scaled> const& kStartValues,
	PlayerTypes eIndex,
	scaled& rPercentage, scaled rNegativeOutlierExtraWeight,
	scaled const* pMedian, // To save time if caller happens to have it
	bool* pbNegativeOutlier) const // Out-param
{
	if (pbNegativeOutlier != NULL)
		*pbNegativeOutlier = false;
	vector<scaled> arSamples;
	for (PlayerIter<CIV_ALIVE> it; it.hasNext(); ++it)
	{
		arSamples.push_back(kStartValues.get(it->getID()));
	}
	scaled rMedian;
	if (pMedian != NULL)
		rMedian = *pMedian;
	else rMedian = stats::median(arSamples);
	scaled rMax = stats::max(arSamples);

	scaled const rStartVal = kStartValues.get(eIndex);
	scaled r = (rStartVal - rMedian).abs();
	// Don't mind small differences (at all); uniformity isn't the goal.
	scaled const rPlusMinus = fixp(0.08);
	r -= rMedian * rPlusMinus;
	r.increaseTo(0);
	if (rStartVal < rMedian) // Small outliers are worse
	{
		if (pbNegativeOutlier != NULL)
			*pbNegativeOutlier = true;
		r *= fixp(2.12) * (1 + rNegativeOutlierExtraWeight);
		rPercentage = r / (rMedian * (1 + rPlusMinus));
	}
	else
	{	// The max (or very close to it) is extra problematic
		if (rStartVal > scaled::max(fixp(1.25) * rMedian, fixp(0.92) * rMax))
			r *= fixp(4/3.);
		rPercentage = r / (rMedian * (1 - rPlusMinus));
	}
	return r;
}


scaled StartingPositionIteration::startingPositionValue(
	SolutionAttributes& kResult) const
{
	scaled rWorstOutlierVal;
	kResult.m_eWorstOutlier = NO_PLAYER;
	kResult.m_rAvgError = 0;
	scaled rMedian;
	scaled rMax;
	scaled rSum;
	scaled rWorstVolatility;
	PlayerTypes eWorstVolatilityPlayer = NO_PLAYER;
	{
		vector<scaled> arSamples;
		for (PlayerIter<CIV_ALIVE> it; it.hasNext(); ++it)
		{
			scaled rStartVal = kResult.m_startValues.get(it->getID());
			arSamples.push_back(rStartVal);
			/*	Generally between 0 (unproblematic) and
				1 (highly volatile or otherwise degenerate) */
			scaled rVolatitlity = kResult.m_volatilityValues.get(it->getID());
			rSum += rStartVal * (1 - rVolatitlity);
			if (rVolatitlity > rWorstVolatility)
			{
				rWorstVolatility = rVolatitlity;
				eWorstVolatilityPlayer = it->getID();
			}
		}
		rMedian = stats::median(arSamples);
	}
	// Encourage strong starting positions
	scaled r = rSum * fixp(0.4);
	// Encourage balanced starting positions
	PlayerIter<CIV_ALIVE> it;
	for (; it.hasNext(); ++it)
	{
		scaled rError;
		scaled rOutlierVal = outlierValue(
				kResult.m_startValues, it->getID(), rError, 0, &rMedian);
		if (rOutlierVal > rWorstOutlierVal)
		{
			rWorstOutlierVal = rOutlierVal;
			kResult.m_eWorstOutlier = it->getID();
		}  /* Not a high exponent b/c there's already tolerance built into
			  outlierValue, which (relatively speaking) magnifies outliers. */
		rOutlierVal.exponentiate(fixp(1.1));
		r -= rOutlierVal / fixp(1.5); // Divisor for normalization
		rError += kResult.m_volatilityValues.get(it->getID()) * fixp(2/3.);
		kResult.m_rAvgError += rError;
	}
	kResult.m_rAvgError /= it.nextIndex();
	// Volatility outliers need some strong discouragement
	scaled rTolerance = fixp(0.12);
	if (rWorstVolatility > rTolerance)
	{
		scaled rVolatilityPenalty = 1 - fixp(1.1) *
				(rWorstVolatility - rTolerance) /
				scaled(it.nextIndex()).sqrt();
		rVolatilityPenalty.increaseTo(fixp(0.3));
		if (r.isPositive())
			r *= rVolatilityPenalty;
		else r /= rVolatilityPenalty;
		if (kResult.m_eWorstOutlier == NO_PLAYER)
			kResult.m_eWorstOutlier = eWorstVolatilityPlayer;
	}
	return r;
}


void StartingPositionIteration::currAltSites(PlayerTypes eCurrSitePlayer,
	// (Low first val means high priority)
	vector<pair<short,PlotNumTypes> >& kAltSitesByPriority,
	bool bIncludeRemote, PlotNumTypes eTakenSite) const
{
	VoronoiCell const* pCell = m_pPotentialSites->getCell(eCurrSitePlayer);
	if (pCell == NULL)
		return;
	CvPlot const& kCurrSite = *GET_PLAYER(eCurrSitePlayer).getStartingPlot();
	short iCurrClosestPathDist = MAX_SHORT;
	for (PlayerIter<CIV_ALIVE> it; it.hasNext(); ++it)
	{
		if (it->getID() != eCurrSitePlayer)
		{
			iCurrClosestPathDist = std::min(iCurrClosestPathDist,
					m_pPathDists->d(kCurrSite, *it->getStartingPlot()));
		}
	}
	vector<pair<short,PlotNumTypes> > altSitesByDist;
	CvMap const& kMap = GC.getMap();
	std::vector<CvPlot const*> apRivalSites;
	if (eTakenSite != NO_PLOT_NUM)
		apRivalSites.push_back(&kMap.getPlotByIndex(eTakenSite));
	for (PlayerIter<CIV_ALIVE> itRival; itRival.hasNext(); ++itRival)
	{
		if (itRival->getID() != eCurrSitePlayer)
			apRivalSites.push_back(itRival->getStartingPlot());
	}
	for (VoronoiCell::const_iterator itSite = pCell->begin(); itSite != pCell->end();
		++itSite)
	{
		if (*itSite == eTakenSite)
			continue;
		CvPlot const& kAltSite = kMap.getPlotByIndex(*itSite);
		/*	startingPositionValue discourages starting sites that are
			too close together, but want to _guarantee_ a lower bound. */
		short iAltClosestPathDist = MAX_SHORT;
		int iAltClosestPlotDist = MAX_INT;
		for (size_t i = 0; i < apRivalSites.size(); i++)
		{
			iAltClosestPathDist = std::min(iAltClosestPathDist,
					m_pPathDists->d(kAltSite, *apRivalSites[i]));
			iAltClosestPlotDist = std::min(iAltClosestPlotDist,
					plotDistance(&kAltSite, apRivalSites[i]));
		}
		if (iAltClosestPathDist >= iCurrClosestPathDist ||
			(2 * iAltClosestPathDist >= 3 * m_pPathDists->getAvgCityDist() &&
			iAltClosestPlotDist > 5)) // Avoid overlapping city radii
		{
			altSitesByDist.push_back(make_pair(
					m_pPathDists->d(kCurrSite, kAltSite), *itSite));
		}
	}
	std::sort(altSitesByDist.begin(), altSitesByDist.end());
	/*	Depending on how evenly the potential sites are distributed, a cell could
		contain a few dozen of them. Don't need that many alternatives. */
	while (altSitesByDist.size() > 6)
		altSitesByDist.pop_back();

	/*	Could directly add remote sites to kAltSitesByPriority w/ first value 0
		for maximal priority. Or with minimal priority if this block is moved up.
		For now, add remote sites and their distance values to altSitesByDist
		and then sort that container again. */
	if (bIncludeRemote)
	{
		int iIsolatedSitesAdded = 0;
		for (int i = 0; i < 3; i++)
		{
			PlotNumTypes eRemoteSite = m_pPotentialSites->getRemoteSite(i);
			if (eRemoteSite == NO_PLOT_NUM || eRemoteSite == eTakenSite)
				break;
			altSitesByDist.push_back(make_pair(
					m_pPathDists->d(kCurrSite, kMap.getPlotByIndex(eRemoteSite)),
					eRemoteSite));
			iIsolatedSitesAdded++;
		}
		/*	The above are "remote" sites in a strict sense - remote from everyone.
			Also include sites that are merely remote from eCurrSitePlayer. */
		// (Would be better to encapsulate this slice of STL hell somehow ...)
		typedef map<CvArea const*,std::set<PlotNumTypes>*> AreaSiteMap;
		AreaSiteMap otherAreaSites;
		/*	Going through rival Voronoi cells ensures that the sites aren't
			remote sites in the strict sense nor sites in our pCell. */
		for (PlayerIter<CIV_ALIVE> itRival; itRival.hasNext(); ++itRival)
		{
			if (itRival->getID() == eCurrSitePlayer)
				continue;
			VoronoiCell const* pRivalCell = m_pPotentialSites->getCell(itRival->getID());
			if (pRivalCell == NULL)
				continue;
			for (VoronoiCell::const_iterator itRemoteSite = pRivalCell->begin();
				itRemoteSite != pRivalCell->end(); ++itRemoteSite)
			{
				if (*itRemoteSite == eTakenSite)
					continue;
				CvPlot const& kRemoteSite = kMap.getPlotByIndex(*itRemoteSite);
				if (kRemoteSite.sameArea(kCurrSite) || pCell->count(*itRemoteSite) > 0)
					continue;
				std::set<PlotNumTypes>* pAreaSites = NULL;
				AreaSiteMap::iterator pos = otherAreaSites.find(kRemoteSite.area());
				if (pos == otherAreaSites.end())
				{
					pAreaSites = new std::set<PlotNumTypes>();
					otherAreaSites.insert(make_pair(kRemoteSite.area(), pAreaSites));
				}
				else pAreaSites = pos->second;
				pAreaSites->insert(*itRemoteSite);
			}
		}
		vector<pair<PlotNumTypes,int> > otherAreasBySize;
		for (AreaSiteMap::const_iterator it = otherAreaSites.begin();
			it != otherAreaSites.end(); ++it)
		{
			otherAreasBySize.push_back(make_pair(
					it->first->getNumTiles(), it->first->getID()));
		}
		std::sort(otherAreasBySize.rbegin(), otherAreasBySize.rend());
		for (size_t i = 0; i < otherAreasBySize.size() &&
			// Consider at most 5 remote sites in total
			i < std::min(3u, (size_t)std::max(0, 5 - iIsolatedSitesAdded)); i++)
		{
			AreaSiteMap::const_iterator pos = otherAreaSites.find(
					kMap.getArea(otherAreasBySize[i].second));
			// Find the most isolated site in the area
			PlotNumTypes eBestSite = NO_PLOT_NUM;
			scaled rBestDist = -1;
			for (std::set<PlotNumTypes>::const_iterator itSite = pos->second->begin();
				itSite != pos->second->end(); ++itSite)
			{
				if (*itSite == eTakenSite)
					continue;
				CvPlot const& kSite = kMap.getPlotByIndex(*itSite);
				vector<short> aDists;
				for (PlayerIter<CIV_ALIVE> it; it.hasNext(); ++it)
				{
					if (it->getID() != eCurrSitePlayer)
						aDists.push_back(m_pPathDists->d(*it->getStartingPlot(), kSite));
				}
				scaled rDistFactor = weightedDistance(aDists);
				if (rDistFactor > rBestDist)
				{
					eBestSite = *itSite;
					rBestDist = rDistFactor;
				}
			}
			if (eBestSite != NO_PLOT_NUM)
			{
				altSitesByDist.push_back(make_pair(
						m_pPathDists->d(kCurrSite, kMap.getPlotByIndex(eBestSite)),
						eBestSite));
			}
		}
		for (AreaSiteMap::iterator it = otherAreaSites.begin();
			it != otherAreaSites.end(); ++it)
		{
			delete it->second;
		}
		// Sort again now that remote sites are in
		std::sort(altSitesByDist.begin(), altSitesByDist.end());
	}
	for (size_t i = 0; i < altSitesByDist.size(); i++)
		kAltSitesByPriority.push_back(altSitesByDist[i]);
}


bool StartingPositionIteration::considerStep(Step& kStep,
	SolutionAttributes& kCurrSolutionAttribs) const
{
	FAssertMsg(kCurrSolutionAttribs.m_eWorstOutlier != NO_PLAYER, "Should've terminated already");
	kStep.take();
	SolutionAttributes newSolutionAttribs;
	evaluateCurrPosition(newSolutionAttribs);
	if (newSolutionAttribs.m_rStartPosVal > kCurrSolutionAttribs.m_rStartPosVal)
	{
		if (newSolutionAttribs.m_eWorstOutlier == NO_PLAYER ||
			// Minor improvement in overall fairness and new worst outlier or getting close
			((newSolutionAttribs.m_eWorstOutlier != kCurrSolutionAttribs.m_eWorstOutlier ||
			kCurrSolutionAttribs.m_rAvgError < per1000(50)) &&
			newSolutionAttribs.m_rAvgError + per1000(10) < kCurrSolutionAttribs.m_rAvgError) ||
			// Same worst outlier and significant improvement in overall fairness
			newSolutionAttribs.m_rAvgError +
			std::max(per1000(23), fixp(0.08) * kCurrSolutionAttribs.m_rAvgError) <
			kCurrSolutionAttribs.m_rAvgError)
		{
			//if (kStep.getNumMoves() > 1) // Single move can have side-effects too ...
			{
				/*	One last check: The outlier value of the site moved in kStep's first move
					needs to improve. That's the site we're primarily interested in. */
				PlayerTypes eFirst = kStep.getFirstMovePlayer();
				scaled rDummy;
				scaled rNewOutlierVal = outlierValue(newSolutionAttribs.m_startValues,
						eFirst, rDummy);
				bool bNegativeOutlier=false;
				scaled rCurrOutlierVal = outlierValue(kCurrSolutionAttribs.m_startValues,
						eFirst, rDummy, 0, NULL, &bNegativeOutlier);
				scaled rCurrStartVal = kCurrSolutionAttribs.m_startValues.get(eFirst);
				if (rNewOutlierVal * fixp(1.01) > rCurrOutlierVal ||
					/*	Start value of negative outlier needs to increase,
						start value of positive outlier needs to decrease.
						Don't want the outlier value to go down just as a side-effect
						of the second move. */
					bNegativeOutlier !=
					(rCurrStartVal < newSolutionAttribs.m_startValues.get(eFirst)))
				{
					//logStep(kStep, kCurrSolutionAttribs, newSolutionAttribs, false);
					kStep.takeBack();
					return false;
				}
			}
			logStep(kStep, kCurrSolutionAttribs, newSolutionAttribs, true);
			/*	Commit to this step (w/o considering further alternatives).
				Tbd.: Could probably get better results by considering all alternatives. */
			// Copy newSolutionAttribs into kCurrSolutionAttribs
			kCurrSolutionAttribs = newSolutionAttribs;
			return true;
		}
	}
	// This step makes matters worse or isn't a significant improvement
	//logStep(kStep, kCurrSolutionAttribs, newSolutionAttribs, false);
	kStep.takeBack();
	return false;
}


void StartingPositionIteration::logStep(Step const& kStep,
	SolutionAttributes const& kOldSolution,
	SolutionAttributes& kNewSolution, bool bStepTaken) const
{
#ifdef SPI_LOG
	std::ostringstream out;
	if (!bStepTaken)
		out << "Step not taken:\n";
	out << kStep.debugStr();
	// ScaledNum doesn't really support streams; need to cache strings locally.
	CvString szNewErr = kNewSolution.m_rAvgError.str(1000);
	CvString szOldErr = kOldSolution.m_rAvgError.str(1000);
	out << (kNewSolution.m_rAvgError < kOldSolution.m_rAvgError ?
			"Reduces" : "Increases") <<
			" avg. error to " << szNewErr <<
			" (was " << szOldErr << ")\n";
	CvString szNewVal = kNewSolution.m_rStartPosVal.str(1);
	CvString szOldVal = kOldSolution.m_rStartPosVal.str(1);
	out << (kNewSolution.m_rStartPosVal > kOldSolution.m_rStartPosVal ?
			"Increases" : "Decreases") << " start position value to " <<
			szNewVal << " (was " << szOldVal << ")\n";
	if (kNewSolution.m_eWorstOutlier != kOldSolution.m_eWorstOutlier)
	{
		out << "New worst outlier: " << kNewSolution.m_eWorstOutlier <<
				" (was " << kOldSolution.m_eWorstOutlier << ")\n";
	}
	out << std::endl;
	gDLL->logMsg("StartingPos.log", out.str().c_str(), false, false);
	evaluateCurrPosition(kNewSolution, /*bLog=*/true);
#endif
}


void StartingPositionIteration::doIterations(PotentialSites& kPotentialSites)
{
	evaluateCurrPosition(m_currSolutionAttribs, true);
	m_bNormalizationTargetReady = true;

	if (m_currSolutionAttribs.m_eWorstOutlier == NO_PLAYER)
		return;

	CvMap const& kMap = GC.getMap();
	bool bPrevStepRemote = false;
	/*	Iterate until we return due to getting stuck in a (local) optimum
		or until we run out of time */
	int iStepsConsidered = 0;
	/*	On watery maps, SPI may have to consider a higher number of
		long-distance moves, but a higher land ratio seems to result
		in greater computational effort overall. */
	int const iPlots = (5 * kMap.getLandPlots() + 2 * kMap.getWaterPlots()) / 3;
	/*	The effort is pretty much proportional to plots times civs,
		but everything takes longer on large maps, so players ought to
		have more patience. Hence the exponent. */
	int iMaxSteps = (1000000 /
			scaled(iPlots * PlayerIter<CIV_ALIVE>::count()).
			pow(fixp(0.61))).round();
	iMaxSteps *= GC.getDefineINT("SPI_TIME_LIMIT_PERCENT");
	iMaxSteps /= 100;
	if (iMaxSteps <= 0)
	{
		FAssert(iMaxSteps > 0);
		return;
	}
	/*	Just so that players can check whether SPI was used - the preconditions
		are pretty complex. Not a Python thing, but I don't want to create a
		separate logfile just for this one message. */
	gDLL->logMsg("PythonDbg.log", "\nRunning Starting Position Iteration (AdvCiv mod)\n");
	while (iStepsConsidered < iMaxSteps)
	{
		vector<pair<scaled,PlayerTypes> > currSitesByOutlierVal;
		for (PlayerIter<CIV_ALIVE> it; it.hasNext(); ++it)
		{
			if (m_abFixedStart.get(it->getID()))
				continue;
			// Focus on negative outliers while the avg. error is high
			scaled rNegativeOutlierExtraWeight = fixp(1.15) * 
					(m_currSolutionAttribs.m_rAvgError - fixp(0.1));
			if (iStepsConsidered % 2 == 0) // A little bit of variation
				rNegativeOutlierExtraWeight += fixp(0.25);
			scaled rDummy;
			scaled rOutlierVal = outlierValue(m_currSolutionAttribs.m_startValues,
					it->getID(), rDummy, rNegativeOutlierExtraWeight);
			if (rOutlierVal > 0)
			{	/*	Also take into account volatility. Crowded areas tend to have higher
					volatility. Need to avoid moving a small number of high-value
					outliers that have small areas to themselves onto a large landmass
					that is already overcrowded. Or better to do this more explicitly?
					Can't easily check for crowdedness here though ... */
				/*int iAreaPlayers = 1;
				for (PlayerIter<CIV_ALIVE> itRival; itRival.hasNext(); ++itRival)
				{
					if (&*itRival != &*it &&
						itRival->getStartingPlot()->sameArea(*it->getStartingPlot()))
					{
						iAreaPlayers++;
					}
				}
				rOutlierVal += rOutlierVal * (m_currSolutionAttribs.m_rAvgError - fixp(0.1)) *
						scaled(iAreaPlayers).sqrt();*/
				rOutlierVal += rOutlierVal * (m_currSolutionAttribs.m_rAvgError - fixp(0.1)) *
						2 * m_currSolutionAttribs.m_volatilityValues.get(it->getID());
				currSitesByOutlierVal.push_back(make_pair(rOutlierVal, it->getID()));
			}
		}
		if (currSitesByOutlierVal.empty())
			return;
		std::sort(currSitesByOutlierVal.rbegin(), currSitesByOutlierVal.rend());
		for (size_t i = 0; i < currSitesByOutlierVal.size(); i++)
		{
			PlayerTypes const eCurrSitePlayer = currSitesByOutlierVal[i].second;
			CvPlot const& kCurrSite = *GET_PLAYER(eCurrSitePlayer).getStartingPlot();
			/*	(Low first val meaning high priority. For now, the priority values
				are distance values.) */
			vector<pair<short,PlotNumTypes> > altSitesByPriority;
			currAltSites(eCurrSitePlayer, altSitesByPriority,
					/*	To save time, stop considering remote sites when approaching
						a decent solution. Unless the prev. step was still a remote one. */
					bPrevStepRemote || m_currSolutionAttribs.m_rAvgError > per1000(295));
			for (size_t j = 0; j < altSitesByPriority.size(); j++)
			{
				PlotNumTypes const eAltSite = altSitesByPriority[j].second;
				CvPlot& kAltSite = kMap.getPlotByIndex(eAltSite);
				short const iMoveDist = m_pPathDists->d(kCurrSite, kAltSite);
				bool const bStepRemote = (
						m_pPathDists->d(kCurrSite, kAltSite) >= m_pPathDists->getLongDist());
				Step singleMoveStep;
				singleMoveStep.move(eCurrSitePlayer, kAltSite);
				vector<pair<short,PlayerTypes> > otherCurrSitesByDist;
				for (PlayerIter<CIV_ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
				{
					if (itPlayer->getID() != eCurrSitePlayer &&
						!m_abFixedStart.get(itPlayer->getID()))
					{
						short d = std::min<short>(
								m_pPathDists->d(*itPlayer->getStartingPlot(), kAltSite),
								/*	Prefer moving the player closest to the new site
									of eCurrPlayer, but, if none are really close,
									also consider moving the player closest to the
									old site of eCurrPlayer. */
								(m_pPathDists->d(*itPlayer->getStartingPlot(),
								kCurrSite) * 3) / 2);
						if (d < m_pPathDists->getLongDist())
							otherCurrSitesByDist.push_back(make_pair(d, itPlayer->getID()));
					}
				}
				/*	If there are no other starting sites near the alt. site nor
					the current site, then consider moving only the current site. */
				if (otherCurrSitesByDist.empty())
				{
					iStepsConsidered++;
					if (considerStep(singleMoveStep, m_currSolutionAttribs))
					{
						bPrevStepRemote = bStepRemote;
						goto next_iteration;
					}
				}
				std::sort(otherCurrSitesByDist.begin(), otherCurrSitesByDist.end());
				/*	Don't try a great number of combinations in this deeply nested loop.
					Rather run more iterations of the main loop instead. */
				while (otherCurrSitesByDist.size() > 2)
					otherCurrSitesByDist.pop_back();
				for (size_t k = 0; k < otherCurrSitesByDist.size(); k++)
				{
					if (2 * otherCurrSitesByDist[k].first >
						3 * otherCurrSitesByDist[0].first)
					{
						continue;
					}
					vector<pair<short,PlotNumTypes> > otherAltSitesByDist;
					currAltSites(otherCurrSitesByDist[k].second, otherAltSitesByDist,
							// Allow remote site for 2nd move only if 1st move is remote
							iMoveDist > m_pPathDists->getLongDist(),
							// Don't move the second player to the same site as the first
							eAltSite);
					for (size_t a = 0; a < otherAltSitesByDist.size(); a++)
					{
						Step doubleMoveStep(singleMoveStep);
						doubleMoveStep.move(otherCurrSitesByDist[k].second,
								kMap.getPlotByIndex(otherAltSitesByDist[a].second));
						iStepsConsidered++;
						if (considerStep(doubleMoveStep, m_currSolutionAttribs))
						{	/*	Never mind the 2nd move; can't be remote if the
								1st isn't remote. */
							bPrevStepRemote = bStepRemote;
							goto next_iteration;
						}
					}
				}
				// No double-move step is worthwhile. Consider the single-move step.
				iStepsConsidered++;
				if (considerStep(singleMoveStep, m_currSolutionAttribs))
				{
					bPrevStepRemote = bStepRemote;
					goto next_iteration;
				}
			}
		}
		return; // No step taken; apparently we're done.
		next_iteration: // To allow breaking out of the inner loops
		gDLL->callUpdater();
		kPotentialSites.updateCurrSites(true); // Also ensures that we never return to a site
	}
#ifdef SPI_LOG
	gDLL->logMsg("StartingPos.log", "Terminated b/c of time limit", false, false);
#endif
}


void StartingPositionIteration::assignSitesToTeams()
{
	vector<std::pair<int,TeamTypes> > aieTeamsBySize;
	for (TeamIter<CIV_ALIVE> itTeam; itTeam.hasNext(); ++itTeam)
		aieTeamsBySize.push_back(make_pair(itTeam->getNumMembers(), itTeam->getID()));
	if (aieTeamsBySize.empty())
	{
		FAssert(false);
		return;
	}
	/*	Start with the large teams; small teams will be at a disadvantage in any case,
		and that's probably what the player who sets up the game intends.
		Stable sort just so that ties aren't broken arbitrarily; not important though
		b/c CvGame will swap the team starts around later. */
	std::stable_sort(aieTeamsBySize.rbegin(), aieTeamsBySize.rend());
	std::set<PlayerTypes> aeAvailableSites; // Identify sites by players
	for (PlayerIter<CIV_ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
		aeAvailableSites.insert(itPlayer->getID());
	#ifdef SPI_LOG
		std::ostringstream out;
	#endif
	int iLoopTeamIndex = 0;
	while (!aeAvailableSites.empty())
	{
		TeamTypes eCurrTeam = aieTeamsBySize[iLoopTeamIndex].second;
		typedef std::set<PlayerTypes>::iterator AvailSitesIter;
		AvailSitesIter itCurrSite = aeAvailableSites.end();
		int iMaxSiteVal = MIN_INT;
		for (AvailSitesIter itSite = aeAvailableSites.begin();
			itSite != aeAvailableSites.end(); ++itSite)
		{
			int iVal = teamValue(*itSite, eCurrTeam);
			if (iVal > iMaxSiteVal || (iVal == iMaxSiteVal &&
				(itCurrSite == aeAvailableSites.end() ||
				/*	One last tiebreaker that I haven't been able to fit into teamValue:
					assign bad starting sites first */
				m_currSolutionAttribs.m_startValues.get(*itSite) <
				m_currSolutionAttribs.m_startValues.get(*itCurrSite))))
			{
				iMaxSiteVal = iVal;
				itCurrSite = itSite;
			}
		}
		#ifdef SPI_LOG
			out << "Assigning site (" << GET_PLAYER(*itCurrSite).getStartingPlot()->getX()
					<< "," << GET_PLAYER(*itCurrSite).getStartingPlot()->getY()
					<< ") to team " << (int)eCurrTeam << "\n";
		#endif
		m_sitesPerTeam[eCurrTeam].push_back(*itCurrSite);
		aeAvailableSites.erase(itCurrSite);
		// Round robin placing two members of one team at a time
		int const iLoopTeamSites = m_sitesPerTeam[eCurrTeam].size();
		if (GET_TEAM(eCurrTeam).getNumMembers() <= iLoopTeamSites ||
			iLoopTeamSites % 2 == 0)
		{
			iLoopTeamIndex++;
			iLoopTeamIndex %= aieTeamsBySize.size();
		}
	}
	#ifdef SPI_LOG
		gDLL->logMsg("StartingPos.log", out.str().c_str(), false, false);
	#endif
}

/*	Both agents are placeholders that will get swapped around later.
	The only relevant data about them are m_sitesPerTeam. */
int StartingPositionIteration::teamValue(PlayerTypes eSitePlayer, TeamTypes eForTeam) const
{
	CvPlot const& kSite = *GET_PLAYER(eSitePlayer).getStartingPlot();
	int const iAreaSites = kSite.getArea().getNumStartingPlots();
	EagerEnumMap<TeamTypes,int> aiAreaSitesPerTeam;
	int iTeamsInArea = 0;
	vector<scaled> arFriendlyCloseness;
	vector<scaled> arRivalCloseness;
	int iAreaTakenSites = 0;
	for (size_t i = 0; i < m_sitesPerTeam.size(); i++)
	{
		TeamTypes eLoopTeam = (TeamTypes)i;
		for (size_t j = 0; j < m_sitesPerTeam[i].size(); j++)
		{
			if (!GET_PLAYER(m_sitesPerTeam[i][j]).getStartingPlot()->
				isArea(kSite.getArea()))
			{
				continue;
			}
			if (aiAreaSitesPerTeam.get(eLoopTeam) == 0)
				iTeamsInArea++;
			aiAreaSitesPerTeam.add(eLoopTeam, 1);
			iAreaTakenSites++;
			bool const bFriendly = (eLoopTeam == eForTeam);
			if (!bFriendly &&
				/*	Ignore closeness to sites of rivals that have already
					placed all there members */
				m_sitesPerTeam[i].size() == GET_TEAM(eLoopTeam).getNumMembers())
			{
				continue;
			}
			int const iOtherAreaSites = m_sitesPerTeam[eLoopTeam].size();
			for (int k = 0; k < iOtherAreaSites; k++)
			{
				CvPlot const& kOtherSite = *GET_PLAYER(
						m_sitesPerTeam[eLoopTeam][k]).getStartingPlot();
				FAssert(&kOtherSite != &kSite);
				short iCloseness = m_pPathDists->getLongDist() -
						m_pPathDists->d(kSite, kOtherSite);
				if (iCloseness > 0)
				{
					(bFriendly ? arFriendlyCloseness : arRivalCloseness).
							push_back(iCloseness);
				}
			}
		}
	}
	int iVicinityFactor = 0;
	if (!arFriendlyCloseness.empty())
	{
		iVicinityFactor = ((stats::min(arFriendlyCloseness) +
				stats::mean(arFriendlyCloseness)) / 2).round();
	}
	/*	When placing the first site of a team in an area,
		try to keep a distance from rival sites in case that
		those rivals will add more members to the area.
		When there are no rival sites either, try to maximize
		the distance from the unassigned sites, if any.*/
	else
	{
		vector<scaled> arUnassignedCloseness;
		vector<scaled> const* parCloseness = NULL;
		if (arRivalCloseness.empty())
		{
			for (PlayerIter<CIV_ALIVE> itOther; itOther.hasNext(); ++itOther)
			{
				if (itOther->getID() != eSitePlayer)
				{
					short iCloseness = m_pPathDists->getLongDist() -
							m_pPathDists->d(kSite, *itOther->getStartingPlot());
					if (iCloseness > 0)
						arUnassignedCloseness.push_back(iCloseness);
				}
			}
			if (!arUnassignedCloseness.empty())
				parCloseness = &arUnassignedCloseness;
		}
		else parCloseness = &arRivalCloseness;
		if (parCloseness != NULL)
		{
			iVicinityFactor = -((stats::min(*parCloseness) +
					stats::mean(*parCloseness)) / 2).round();
		}
	}
	int const iRemainingAreaSites = iAreaSites - iAreaTakenSites;
	// Top priority: Area with the highest number of remaining sites;
	int const iRemainingSiteWeight = 100000;
	int iValue = iRemainingSiteWeight * iRemainingAreaSites;
	// Stick close to sites already assigned to teammates
	iValue += iVicinityFactor;
	/*	Total area sites as tiebreaker; especially when a team has
		no assigned sites yet (0 vicinity factor everywhere). */
	iValue += iAreaSites;
	/*	When taking the final site in the area, try to avoid letting
		some team outnumber another. */
	if (iRemainingAreaSites == 1 && iAreaTakenSites > 0)
	{
		// Pretend that eForTeam is already placed in the area
		iAreaTakenSites++;
		if (aiAreaSitesPerTeam.get(eForTeam) <= 0)
			iTeamsInArea++;
		scaled rMeanAreaSitesPerTeam(iAreaTakenSites, iTeamsInArea);
		scaled rSquareError;
		for (TeamIter<CIV_ALIVE> itTeam; itTeam.hasNext(); ++itTeam)
		{
			int iLoopSites = aiAreaSitesPerTeam.get(itTeam->getID());
			if (itTeam->getID() == eForTeam)
				iLoopSites++;
			if (iLoopSites <= 0)
				continue;
			rSquareError += SQR((iLoopSites - rMeanAreaSitesPerTeam).abs());
		}
		// Greater impact than vicinity
		iValue -= 3 * (rSquareError / iTeamsInArea).getPermille();
	}
	/*	If there's at least one friendly area site (and more than one remains
		to be assigned), treat the area as if it had one additional free site.
		To avoid scattering teams too much across multiple areas. */
	else if (aiAreaSitesPerTeam.get(eForTeam) > 0)
		iValue += iRemainingSiteWeight;
	return iValue;
}


CvPlot* StartingPositionIteration::getTeamSite(TeamTypes eTeam, int iMember) const
{
	FAssert(eTeam >= 0 && iMember >= 0);
	if (eTeam >= (int)m_sitesPerTeam.size())
		return NULL;
	if (iMember >= (int)m_sitesPerTeam[eTeam].size())
		return NULL;
	return GET_PLAYER(m_sitesPerTeam[eTeam][iMember]).getStartingPlot();
}


NormalizationTarget::NormalizationTarget(CitySiteEvaluator& kEval,
	StartingPositionIteration::SolutionAttributes const& kSolution)
{
	m_pEval = &kEval;
	for (PlayerIter<CIV_ALIVE> it; it.hasNext(); ++it)
	{
		PlayerTypes ePlayer = it->getID();
		m_startValData.insert(make_pair(
				it->getStartingPlot()->plotNum(),
				StartValBreakdown(
				kSolution.m_startValues.get(ePlayer),
				kSolution.m_volatilityValues.get(ePlayer),
				kSolution.m_foundValues.get(ePlayer),
				kSolution.m_foundWeights.get(ePlayer),
				kSolution.m_rivalMultipliers.get(ePlayer))));
	}
}


NormalizationTarget::~NormalizationTarget()
{
	delete m_pEval;
}


bool NormalizationTarget::isReached(CvPlot const& kStartSite,
	bool bNearlyReached, bool bClearlyExceeded) const
{
	CvMap const& kMap = GC.getMap();

	scaled rCurrStartVal = -1;
	short iCurrFoundVal = -1;
	vector<scaled> arCurrFoundValues;
	vector<scaled> arCurrStartValues;
	for (map<PlotNumTypes,StartValBreakdown>::const_iterator it =
		m_startValData.begin(); it != m_startValData.end(); ++it)
	{
		PlotNumTypes const eLoopPlot = it->first;
		CvPlot const& kLoopPlot = kMap.getPlotByIndex(eLoopPlot);
		short iFoundVal = m_pEval->evaluate(kLoopPlot);
		arCurrFoundValues.push_back(iFoundVal);
		StartValBreakdown svb = it->second;
		scaled rStartVal = svb.rTotal;
		/*	Eliminate the multipliers, subtract the pre-normalization found value,
			add the current found value, re-apply the multipliers. */
		if (svb.rRivalMult.isPositive())
			rStartVal /= svb.rRivalMult;
		// svb.rFoundVal is the unweighted pre-normalization found value
		rStartVal = rStartVal + (iFoundVal - svb.rFoundVal) * svb.rFoundWeight;
		if (svb.rRivalMult.isPositive())
			rStartVal *= svb.rRivalMult;
		arCurrStartValues.push_back(rStartVal);
		if (&kLoopPlot == &kStartSite)
		{
			iCurrFoundVal = iFoundVal;
			rCurrStartVal = rStartVal;
		}
	}
	FAssert(iCurrFoundVal != -1 && rCurrStartVal != -1);
	scaled const rMedianCurrFoundVal = stats::median(arCurrFoundValues);
	scaled const rMedianCurrStartVal = stats::median(arCurrStartValues);
	scaled const rMaxCurrStartVal = stats::max(arCurrStartValues);
	
	scaled rIncreaseNeeded =
			// Don't increase kStartSite's found value far beyond the median found value
			std::min(fixp(1.1) * rMedianCurrFoundVal - iCurrFoundVal,
			// Don't keep kStartSite's start value far below the highest start value
			std::max(fixp(0.8) * rMaxCurrStartVal - rCurrStartVal, std::max(
			/*	If kStartSite's start value is below the median start value,
				then increase kStartSite's foundValue at least to the median found value. */
			std::min(rMedianCurrStartVal - rCurrStartVal,
			rMedianCurrFoundVal - iCurrFoundVal),
			/*	Try to ensure that the found value isn't far below the median found value -
				regardless of start values. */
			fixp(0.85) * (rMedianCurrFoundVal - iCurrFoundVal))));
	if (bClearlyExceeded)
		return (-rIncreaseNeeded > per100(5) * iCurrFoundVal);
	scaled rTolerance = fixp(2.5);
	if (bNearlyReached)
	{
		/*	(Not sure if rTolerance really has a big impact in general.
			It did in some of my tests.) */
		switch(GC.getGame().getStartingPlotNormalizationLevel())
		{
		case CvGame::NORMALIZE_HIGH: rTolerance += 2;
		case CvGame::NORMALIZE_MEDIUM: rTolerance += 4;
		default: rTolerance += 6;
		}
	}
	rTolerance /= 100;
	/*	Be more tolerant of a subpar starting site if the player at that site
		is supposed to be handicapped.
		(Should get the player through a parameter I guess. Eh ...) */
	for (PlayerIter<CIV_ALIVE> it; it.hasNext(); ++it)
	{
		if (it->getStartingPlot() == &kStartSite)
		{
			rTolerance += rTolerance * per100(GC.getInfo(it->getHandicapType()).
					getStartingLocationPercent() - 50) * per100(75);
			rTolerance.increaseTo(0);
			break;
		}
	}
	return (rIncreaseNeeded <= rTolerance * iCurrFoundVal);
}


scaled NormalizationTarget::getStartValue(CvPlot const& kStartSite) const
{
	StartValBreakdown const* pBrk = getBreakdown(kStartSite);
	if (pBrk == NULL)
		return -1;
	return pBrk->rTotal;
}


scaled NormalizationTarget::getVolatilityValue(CvPlot const& kStartSite) const
{
	StartValBreakdown const* pBrk = getBreakdown(kStartSite);
	if (pBrk == NULL)
		return 0;
	return pBrk->rVolatility;
}


NormalizationTarget::StartValBreakdown const* NormalizationTarget::getBreakdown(
	CvPlot const& kSite) const
{
	PlotNumTypes const ePlot = kSite.plotNum();
	map<PlotNumTypes,StartValBreakdown>::const_iterator pos = m_startValData.find(ePlot);
	if (pos == m_startValData.end())
	{
		FErrorMsg("Starting plot not found in normalization inputs");
		return NULL;
	}
	return &pos->second;
}
