// advc.tsl: New file; see comments in header.

#include "CvGameCoreDLL.h"
#include "TrueStarts.h"
#include "CvInfo_TrueStarts.h"
#include "CvInfo_Terrain.h"
#include "CvInfo_GameOption.h"
#include "CvMap.h"
#include "CvArea.h"
#include "CvGamePlay.h"
#include "PlotRange.h"
#include "BBAILog.h"

using std::auto_ptr;

// To enable, toggle 'false' to 'true' and also enable BBAI map logging.
#define IFLOG if (bLog && gMapLogLevel > 0 && false)


namespace
{
	/*	Treating peaks as continental boundaries is useful for game balance,
		but, here, we should care more about the intuitive impression that
		players have of the terrain surrounding the starting plot of a civ.
		Also makes life easier when counting peaks for relief-based preferences. */
	bool sameArea(CvPlot const& kFirst, CvPlot const& kSecond)
	{
		if (GC.getDefineBOOL(CvGlobals::PASSABLE_AREAS))
		{
			return (kFirst.getArea().getRepresentativeArea() ==
					kSecond.getArea().getRepresentativeArea());
		}
		return kFirst.sameArea(kSecond);
	}
}


TrueStarts::TrueStarts()
{
	m_eTemperateClimate = (ClimateTypes)GC.getInfoTypeForString("CLIMATE_TEMPERATE");
	if (GC.getGame().isScenario())
		overrideScenarioOptions();
	CvMap const& kMap = GC.getMap();
	{
		CvWString szMapName = GC.getInitCore().getMapScriptName();
		// The official non-Earth scenarios set all latitude values to 0
		m_bMapHasLatitudes =
				(kMap.getTopLatitude() > kMap.getBottomLatitude() &&
				// These scripts largely ignore latitude
				szMapName != CvWString("Ring") && szMapName != CvWString("Wheel") &&
				szMapName != CvWString("Arboria") && szMapName != CvWString("Caldera"));
		// Scenario makers tend to use peaks very liberally
		m_bAdjustPeakScore = (GC.getGame().isScenario() ||
				/*	This earth-like script also places lots of peaks.
					(advc.021a: Not that many anymore, but it varies quite a bit.
					In any case, adjusting the scoring won't hurt.) */
				szMapName == CvWString("Tectonics"));
	}
	m_bBonusesIgnoreLatitude = (!m_bMapHasLatitudes ||
			GC.getPythonCaller()->isBonusIgnoreLatitude());
	m_bBalancedResources = kMap.isCustomMapOption(gDLL->getText("TXT_KEY_MAP_BALANCED"));
	/*	Don't focus on the initial human player when
		any civ may come under human control later on */
	m_bPrioritizeHumans = !GC.getGame().isOption(GAMEOPTION_RISE_FALL);
	m_iMaxLatitudeDiffTimes10 = CvTruCivInfo::maxLatitude()
			- CvTruCivInfo::minLatitude();
	if (kMap.isWrapY())
		m_iMaxLatitudeDiffTimes10 /= 2;
	m_iMaxLongitudeDiffTimes10 = CvTruCivInfo::maxLongitude()
			- CvTruCivInfo::minLongitude();
	if (kMap.isWrapX())
		m_iMaxLongitudeDiffTimes10 /= 2;
	// Use the same approximation of Euclidean distance as plotDistance
	m_iMaxGeoDist = std::max(m_iMaxLongitudeDiffTimes10, m_iMaxLatitudeDiffTimes10)
			+ std::min(m_iMaxLongitudeDiffTimes10, m_iMaxLatitudeDiffTimes10) / 2;
	FOR_EACH_ENUM(TruCiv)
	{
		m_truCivs.set(GC.getInfo(eLoopTruCiv).getCiv(),
				&GC.getInfo(eLoopTruCiv));
	}
	// Ignore the truLeader info when leaders are unrestricted
	if (!GC.getGame().isOption(GAMEOPTION_LEAD_ANY_CIV))
	{
		FOR_EACH_ENUM(TruLeader)
		{
			m_truLeaders.set(GC.getInfo(eLoopTruLeader).getLeader(),
					&GC.getInfo(eLoopTruLeader));
		}
	}
	FOR_EACH_ENUM(TruBonus)
	{
		m_truBonuses.set(GC.getInfo(eLoopTruBonus).getBonus(),
				&GC.getInfo(eLoopTruBonus));
	}
	FOR_EACH_ENUM(Bonus)
	{
		CvTruBonusInfo const* pTruBonus = m_truBonuses.get(eLoopBonus);
		if (pTruBonus == NULL) // just to save time
			continue;
		int iEncouraged = 0;
		FOR_EACH_ENUM(Civilization)
		{
			if (isTruBonusEncouraged(pTruBonus, eLoopCivilization))
			{
				m_encouragedBonusesTotal.add(eLoopCivilization, 1);
				iEncouraged++;
			}
			if (isTruBonusDiscouraged(pTruBonus, eLoopCivilization))
			{
				m_discouragedBonusesTotal.add(eLoopCivilization, 1);
				iEncouraged--;
			}
		}
		if (iEncouraged < 0)
		{
			m_bonusDiscouragedRatio.set(eLoopBonus,
					scaled(-iEncouraged, GC.getNumCivilizationInfos()));
		}
	}
	initTargetLatitudes();
	/*	Would be nicer to cache these at CvGlobals (as the Global Warming code
		uses them too), but that's a bit annoying to implement. Also, this way,
		I can use the names most appropriate for the True Starts option. */
	m_eWarmForest = (FeatureTypes)GC.getDefineINT("WARM_FEATURE");
	m_eCoolForest = (FeatureTypes)GC.getDefineINT("TEMPERATE_FEATURE");
	/*	(Woods should be the natural vegetation of the biome represented by
		this terrain type) */
	m_eWoodland = (TerrainTypes)GC.getDefineINT("TEMPERATE_TERRAIN");
	m_eSteppe = (TerrainTypes)GC.getDefineINT("DRY_TERRAIN");
	m_eTundra = (TerrainTypes)GC.getDefineINT("COLD_TERRAIN");
	m_eDesert = (TerrainTypes)GC.getDefineINT("BARREN_TERRAIN");
	m_ePolarDesert = (TerrainTypes)GC.getDefineINT("FROZEN_TERRAIN");

	for (PlayerIter<CIV_ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		if (GC.getInitCore().wasCivRandomlyChosen(itPlayer->getID()) ||
			// Can't sync up the was-randomly-chosen info in time
			GC.getGame().isNetworkMultiPlayer() ||
			/*	Scenario with a fixed civ for each player - ignore that
				(b/c otherwise True Starts would not affect such scenarios). */
			(GC.getGame().isScenario() && !GC.getInitCore().getWBMapNoPlayers()))
		{
			m_truPlayers.push_back(&*itPlayer);
			if (itPlayer->isHuman())
				m_truHumans.push_back(&*itPlayer);
		}
	}
	for (TruPlayerIter itPlayer = truPlayers(); itPlayer.hasNext(); ++itPlayer)
	{
		calculateRadius(*itPlayer);
	}
	m_plotWeights.reset();
	for (TruPlayerIter itPlayer = truPlayers(); itPlayer.hasNext(); ++itPlayer)
	{
		calculatePlotWeights(*itPlayer);
	}
	{
		std::vector<scaled> arSpaceWeights;
		std::vector<scaled> arPeakScores;
		for (TruPlayerIter itPlayer = truPlayers(); itPlayer.hasNext(); ++itPlayer)
		{
			SurroundingsStats& kStats = *new SurroundingsStats(*itPlayer, *this);
			m_surrStats.set(itPlayer->getID(), &kStats);
			arSpaceWeights.push_back(kStats.areaSpaceWeights());
			arPeakScores.push_back(kStats.areaPeakScore());
		}
		if (!arSpaceWeights.empty())
			m_rMedianSpace = stats::median(arSpaceWeights);
		if (!arPeakScores.empty())
			m_rMedianPeakScore = stats::median(arPeakScores);
	}
}


TrueStarts::~TrueStarts()
{
	for (TruPlayerIter itPlayer = truPlayers(); itPlayer.hasNext(); ++itPlayer)
	{
		SurroundingsStats* pStats = m_surrStats.get(itPlayer->getID());
		if (pStats != NULL)
			delete pStats;
	}
}


void TrueStarts::overrideScenarioOptions()
{
	CvMap& kMap = GC.getMap();
	if ((kMap.getTopLatitude() != 90 && kMap.getTopLatitude() != 0) ||
		(kMap.getBottomLatitude() != -90 && kMap.getBottomLatitude() != 0))
	{	// Someone has already set custom latitude limits. Respect those.
		return;
	}
	bool bOverrideOptions = false;
	/*	These latitude values and size options are more sensible in general,
		not just for testing, but I don't want to change the WBSave files b/c
		including them in the mod may suggest that they've been overhauled or
		are curated content. */
	CvWString szMapName = GC.getInitCore().getMapScriptName();
	if (szMapName == CvWString("Earth18Civs.Civ4WorldBuilderSave") ||
		szMapName == CvWString("Earth.Civ4WorldBuilderSave") ||
		szMapName == CvWString("Earth_IceAge.CivBeyondSwordWBSave") ||
		szMapName == CvWString("Earth_IceAge.Civ4WorldBuilderSave"))
	{
		// (-65 matches the temperate latitudes better)
		kMap.setLatitudeLimits(90, -60);
		bOverrideOptions = true;
	}
	if (szMapName == CvWString("Planet.Civ4WorldBuilderSave"))
	{
		kMap.setLatitudeLimits(90, -90);
		bOverrideOptions = true;
	}
	if (szMapName == CvWString("Africa.Civ4WorldBuilderSave"))
	{
		kMap.setLatitudeLimits(37, -37);
		bOverrideOptions = true;
	}
	if (szMapName == CvWString("East Asia.Civ4WorldBuilderSave"))
	{
		kMap.setLatitudeLimits(61, 5);
		bOverrideOptions = true;
	}
	if (szMapName == CvWString("South America.Civ4WorldBuilderSave"))
	{
		kMap.setLatitudeLimits(-10, -57);
		bOverrideOptions = true;
	}
	if (szMapName == CvWString("Europe.Civ4WorldBuilderSave") ||
		szMapName == CvWString("Europe.CivBeyondSwordWBSave"))
	{
		kMap.setLatitudeLimits(65, 25);
		bOverrideOptions = true;
	}
	if (szMapName == CvWString("Eastern United States.Civ4WorldBuilderSave"))
	{
		kMap.setLatitudeLimits(48, 25);
		bOverrideOptions = true;
	}
	if (bOverrideOptions &&
		// Don't override if someone has changed the sea level in the WBSave
		kMap.getSeaLevel() == GC.getInfoTypeForString("SEALEVEL_MEDIUM"))
	{
		/*	These affect CvGame::getRecommendedPlayers, which we use for
			adjustments to the crowdedness of the map. */
		GC.getInitCore().setWorldSize(WORLDSIZE_HUGE);
		SeaLevelTypes eLowLevel = (SeaLevelTypes)GC.getInfoTypeForString("SEALEVEL_LOW");
		if (eLowLevel != NO_SEALEVEL)
			GC.getInitCore().setSeaLevel(eLowLevel);
	}
}


void TrueStarts::initTargetLatitudes()
{
	int const iAbsMaxLat = 90; // (don't base this on the map)
	scaled rDesertExtentChange;
	scaled rTundraLatChange;
	CvMap const& kMap = GC.getMap();
	if (m_eTemperateClimate != NO_CLIMATE && kMap.getClimate() != m_eTemperateClimate &&
		!GC.getGame().isScenario())
	{
		CvClimateInfo const& kTemperate = GC.getInfo(m_eTemperateClimate);
		CvClimateInfo const& kClimate = GC.getInfo(kMap.getClimate());
		/*	In a world with e.g. wetter climate, we want more tropical civs,
			so the target latitude values need to be adjusted a little.
			The math for this is ad hoc (like all math in this class really). */
		int const iTundraLatChangeDiffPermille = (int)(1000 *
				kClimate.getTundraLatitudeChange()
				- kTemperate.getTundraLatitudeChange());
		rTundraLatChange = per1000(iTundraLatChangeDiffPermille) *
				iAbsMaxLat;
		if (rTundraLatChange == 0)
		{
			int const iDesertExtentChangeDiffPermille = (int)(1000 *
					(kClimate.getDesertTopLatitudeChange()
					- kClimate.getDesertBottomLatitudeChange()) -
					(kTemperate.getDesertTopLatitudeChange()
					- kTemperate.getDesertBottomLatitudeChange()));
			rDesertExtentChange = per1000(iDesertExtentChangeDiffPermille) *
					iAbsMaxLat;
		}
	}
	FOR_EACH_ENUM(TruCiv)
	{
		CvTruCivInfo const& kTruCiv = GC.getInfo(eLoopTruCiv);
		int iAbsLatTimes10 = abs(kTruCiv.get(CvTruCivInfo::LatitudeTimes10));
		if (rTundraLatChange != 0)
		{
			scaled const rAbsLatRatio(iAbsLatTimes10, 10 * iAbsMaxLat);
			/*	If the Tundra is larger than normal, we want the multiplier
				to be maximal on all latitudes that allow Tundra or Snow on
				a temperate map. That's about 1/3 of a hemisphere. */
			scaled rMult = fixp(1.5) * rAbsLatRatio;
			rMult.decreaseTo(1);
			if (rTundraLatChange > 0)
			{
				/*	If our climate makes the Tundra smaller, then we assume that
					the tropics get larger by a greater amount, i.e. at the expense
					of all the higher latitudes. We want the multiplier to be 1
					in the high latitudes (got that already) and to increase
					toward 1.5 at the equator. */
				rMult += (1 - rMult) * fixp(1.5);
			}
			iAbsLatTimes10 += (rMult * rTundraLatChange * 10).round();
		}
		if (rDesertExtentChange != 0)
		{
			// Where deserts tend to be most common
			scaled const rPeakLatTimes10 = 3 * iAbsMaxLat; // 30% of max
			scaled const rDiffPeak = (iAbsLatTimes10 - rPeakLatTimes10).abs();
			/*	Would prefer sth. smoother, but this stuff makes my head swim,
				and hardly anyone uses non-temperate climate anyway ...
				As it is, the adjustment is 0 within 10 degrees of the peak
				(desert civs can keep their target latitude), then jumps
				to 100% (civs at the desert fringes shouldn't end up in the
				middle of the desert belt) and decreases linearly from there. */
			if (rDiffPeak > 100)
			{
				scaled rMult = 1 - rDiffPeak / (iAbsMaxLat * 10);
				rMult /= 2;
				if (iAbsLatTimes10 < rPeakLatTimes10)
					rMult *= -1;
				iAbsLatTimes10 += (rMult * rDesertExtentChange * 10).round();
			}
		}
		m_absTargetLatitudeTimes10.set(kTruCiv.getCiv(),
				range(iAbsLatTimes10, 0, iAbsMaxLat * 10));
	}
}

// Wrapper for convenience
bool TrueStarts::canHaveBonus(CvPlot const& kPlot, BonusTypes eBonus,
	bool bIgnoreFeature) const
{
	return kPlot.canHaveBonus(eBonus, m_bBonusesIgnoreLatitude, bIgnoreFeature, true);
}


bool TrueStarts::changingVegetationMakesBonusValid(CvPlot const& kPlot, BonusTypes eBonus,
	// Optional out param. Add this vegetation feature to make eBonus valid.
	FeatureTypes* peFeature) const
{
	LOCAL_REF(FeatureTypes, eFeature, peFeature, NO_FEATURE);
	if (!canHaveBonus(kPlot, eBonus, true))
		return false;
	if (kPlot.isFeature())
	{
		if (GC.getInfo(kPlot.getFeatureType()).getGrowthProbability() > 5 &&
			// Could be the wrong type of vegetation
			GC.getInfo(eBonus).isFeature(kPlot.getFeatureType()))
		{
			return true;
		}
		/*	Won't want to replace a non-vegetation feature. Replacing one
			vegetation feature with another gets too complicated to implement. */
		return false;
	}
	else // Consider adding vegetation
	{
		int iBestScore = 1;
		FOR_EACH_ENUM(Feature)
		{
			if (GC.getInfo(eBonus).isFeature(eLoopFeature) &&
				GC.getInfo(eBonus).isFeatureTerrain(kPlot.getTerrainType()) &&
				GC.getInfo(eLoopFeature).getGrowthProbability() > 5)
			{
				int iScore = SyncRandNum(2); // tie-breaker
				FOR_EACH_ADJ_PLOT(kPlot)
				{
					if (pAdj->getFeatureType() == eLoopFeature)
					{
						if (peFeature == NULL)
							return true; // Don't care which is the best
						iScore += 10;
					}
				}
				if (iScore > iBestScore)
				{
					iBestScore = iScore;
					eFeature = eLoopFeature;
				}
			}
		}
		return (eFeature != NO_FEATURE);
	}
}


CvPlot* TrueStarts::findValidBonusSwapDest(CvPlot& kOriginalDest, CvPlot const& kSource,
	FeatureTypes* peFeature) const // See changingVegetationMakesBonusValid
{
	BonusTypes const eBonus = kSource.getBonusType();
	if (canHaveBonus(kOriginalDest, eBonus) ||
		changingVegetationMakesBonusValid(kOriginalDest, eBonus, peFeature))
	{
		return &kOriginalDest;
	}
	for (int iPass = 0; iPass < 2; iPass++)
	{
		bool const bRemoveVegetation = (iPass == 1);
		FOR_EACH_ADJ_PLOT_VAR_RAND(kOriginalDest, mapRand())
		{
			if (pAdj->isWater() != kOriginalDest.isWater() || // save time
				pAdj->getBonusType() != NO_BONUS ||
				pAdj->isImproved()) // goody hut
			{
				continue;
			}
			bool bValid = true;
			for (PlayerIter<CIV_ALIVE> itPlayer;
				bValid && itPlayer.hasNext(); ++itPlayer)
			{
				if (itPlayer->getStartingPlot() == pAdj)
					bValid = false;
			}
			if (!bValid)
				continue;
			if (!bRemoveVegetation ? canHaveBonus(*pAdj, eBonus) :
				changingVegetationMakesBonusValid(*pAdj, eBonus, peFeature))
			{
				return pAdj;
			}
		}
	}
	return NULL;
}

// Return +1 if a feature was added, -1 if it was removed, 0 if moved.
int TrueStarts::changeVegetation(CvPlot& kPlot, BonusTypes eNewBonus, bool bReplace) const
{
	FeatureTypes const eOldFeature = kPlot.getFeatureType();
	FeatureTypes eNewFeature;
	#ifdef FASSERT_ENABLE
	bool bSuccess =
	#endif
	changingVegetationMakesBonusValid(
			kPlot, eNewBonus, &eNewFeature);
	FAssert(bSuccess);
	kPlot.setFeatureType(eNewFeature);
	if (eNewFeature != NO_FEATURE)
		return 1;
	if (eOldFeature == NO_FEATURE)
	{
		FErrorMsg("Tried to remove feature where none present");
		return 0;
	}
	if (!bReplace)
		return -1;
	/*	Don't want to change the map's overall vegetation density.
		Try to restore eOldFeature on an adjacent plot. */
	CvPlot* pBestPlot = NULL;
	int iBestScore = -1;
	/*	Also don't want to un-feature too many resources.
		Prefer to move the feature to an adjacent resource,
		ideally of a similar importance. A pretty long shot. */
	int const iTargetOrder = GC.getInfo(eNewBonus).getPlacementOrder();
	FOR_EACH_ADJ_PLOT_VAR_RAND(kPlot, mapRand())
	{
		if (pAdj->isFeature() || !pAdj->canHaveFeature(eOldFeature))
			continue;
		bool bValid = true;
		for (PlayerIter<CIV_ALIVE> itPlayer;
			bValid && itPlayer.hasNext(); ++itPlayer)
		{
			if (itPlayer->getStartingPlot() == pAdj)
				bValid = false;
		}
		if (!bValid)
			continue;
		int iScore = 0;
		if (pAdj->getBonusType() != NO_BONUS)
		{
			iScore += 100 - abs(iTargetOrder
					- GC.getInfo(pAdj->getBonusType()).getPlacementOrder());
		}
		if (iScore > iBestScore)
		{
			iScore = iBestScore;
			pBestPlot = pAdj;
		}
	}
	if (pBestPlot != NULL)
	{
		pBestPlot->setFeatureType(eOldFeature);
		bool bLog = true;
		IFLOG logBBAI("Feature %S added at (%d,%d) to compensate for removed %S\n\n",
				GC.getInfo(eOldFeature).getDescription(), pBestPlot->getX(), pBestPlot->getY(),
				GC.getInfo(eOldFeature).getDescription());
		return 0;
	}
	return -1;
}


void TrueStarts::logVegetationChange(CvPlot const& kPlot, BonusTypes eBonus) const
{
	if (canHaveBonus(kPlot, eBonus))
		return;
	if (kPlot.isFeature())
	{
		logBBAI("Removing feature %S from (%d,%d)",
				GC.getInfo(kPlot.getFeatureType()).getDescription(),
				kPlot.getX(), kPlot.getY());
	}
	else
	{
		FeatureTypes eFeature;
		changingVegetationMakesBonusValid(kPlot, eBonus, &eFeature);
		logBBAI("Adding feature %S to (%d,%d)", eFeature == NO_FEATURE ? L"none(!)" :
				GC.getInfo(eFeature).getDescription(),
				kPlot.getX(), kPlot.getY());
	}
}


void TrueStarts::setPlayerWeightsPerPlot(PlotNumTypes ePlot,
	EagerEnumMap<PlayerTypes,scaled>& kPlayerWeights, scaled rHumanMult) const
{
	for (TruPlayerIter itPlayer = truPlayers(); itPlayer.hasNext(); ++itPlayer)
	{
		kPlayerWeights.set(itPlayer->getID(),
				m_plotWeights.get(itPlayer->getID(), ePlot));
	}
	if (rHumanMult != 1)
	{
		for (TruPlayerIter itHuman = truHumans(); itHuman.hasNext(); ++itHuman)
		{
			kPlayerWeights.multiply(itHuman->getID(), rHumanMult);
		}
	}
}


void TrueStarts::sanitize()
{
	CvMap const& kMap = GC.getMap();
	std::vector<std::pair<scaled,PlotNumTypes> > areFitnessPerBonusPlot;
	FOR_EACH_ENUM_RAND(PlotNum, mapRand()) // Will frequently tie at 0 fitness
	{
		CvPlot const& kPlot = kMap.getPlotByIndex(eLoopPlotNum);
		if (kPlot.getBonusType() != NO_BONUS &&
			(!m_bBalancedResources ||
			!GC.getMap().isBonusBalanced(kPlot.getBonusType())))
		{
			EagerEnumMap<PlayerTypes,scaled> aerPlayerWeights;
			setPlayerWeightsPerPlot(eLoopPlotNum, aerPlayerWeights);
			scaled rFitness = calcBonusFitness(kPlot, aerPlayerWeights);
			areFitnessPerBonusPlot.push_back(std::make_pair(rFitness, eLoopPlotNum));
		}
	}
	// Consider swapping pairs of bonus plots with subpar fitness values
	std::sort(areFitnessPerBonusPlot.begin(), areFitnessPerBonusPlot.end());
	{
		bool bLog = true;
		IFLOG
		{
			int iNegativeFitPlots = 0;
			for (size_t i = 0; i < areFitnessPerBonusPlot.size(); i++)
			{
				if (areFitnessPerBonusPlot[i].first < 0)
					iNegativeFitPlots++;
			}
			logBBAI("%d plots with negative bonus fitness value", iNegativeFitPlots);
		}
	}
	int iFeaturesRemoved = 0, iFeaturesAdded = 0, iFeaturesMoved = 0;
	std::set<CvPlot*> apSwappedPlots; // Swap each bonus resource at most once
	/*	Yep, this variable name doesn't bode well. Perhaps the inner loop should
		just always go through all resource plots. I think the current implementation
		mostly saves time - by picking the best match only from among the first third
		or so of the vector unless no valid match is found there at all. Well, this
		also ensures that two problematic resources are dealt with in a single swap
		whenever that's possible. Then again, calcBonusSwapUtil would probably
		prefer such swaps even if swaps with unproblematic resources were
		considered right away ... */
	int iContinueInnerLoopAt = -1;
	scaled const rNeverSwapThresh = fixp(0.4);
	for (size_t i = 0; 3 * i < areFitnessPerBonusPlot.size() &&
		areFitnessPerBonusPlot[i].first < 0; i++)
	{
		CvPlot& kFirstPlot = kMap.getPlotByIndex(areFitnessPerBonusPlot[i].second);
		if (apSwappedPlots.count(&kFirstPlot) > 0)
			continue;
		scaled rMaxUtil;
		CvPlot* pBestPlot = NULL;
		int j;
		for (j = std::max<int>(i + 1, iContinueInnerLoopAt);
			areFitnessPerBonusPlot[j].first <= rNeverSwapThresh &&
			(iContinueInnerLoopAt >= 0 ?
			j < (int)areFitnessPerBonusPlot.size() :
			(2 * j < (int)areFitnessPerBonusPlot.size() &&
			(areFitnessPerBonusPlot[j].first <= 0 ||
			3 * j < (int)areFitnessPerBonusPlot.size()))); j++)
		{
			CvPlot& kSecondPlot = kMap.getPlotByIndex(areFitnessPerBonusPlot[j].second);
			if (apSwappedPlots.count(&kSecondPlot) > 0)
				continue;
			scaled rUtil = calcBonusSwapUtil(kFirstPlot, kSecondPlot,
					areFitnessPerBonusPlot[i].first, areFitnessPerBonusPlot[j].first);
			if (rUtil > rMaxUtil)
			{
				rMaxUtil = rUtil;
				pBestPlot = &kSecondPlot;
			}
		}
		bool bLog = true;
		if (pBestPlot == NULL)
		{
			IFLOG
			{
				logBBAI("No bonus resource found to swap with %S (%d,%d)",
						GC.getInfo(kFirstPlot.getBonusType()).getDescription(),
						kFirstPlot.getX(), kFirstPlot.getY());
				if (iContinueInnerLoopAt >= 0)
				{
					logBBAI("Breakdown of fitness calculation ...");
					// Re-calc fitness value with logging enabled
					EagerEnumMap<PlayerTypes,scaled> aerPlayerWeights;
					setPlayerWeightsPerPlot(kFirstPlot.plotNum(), aerPlayerWeights);
					calcBonusFitness(kFirstPlot, aerPlayerWeights, NO_BONUS, true);
					logBBAI("\n");
				}
			}
			if (iContinueInnerLoopAt < 0 && j + 1 < (int)areFitnessPerBonusPlot.size() &&
				areFitnessPerBonusPlot[j + 1].first <= rNeverSwapThresh)
			{
				iContinueInnerLoopAt = j + 1;
				IFLOG logBBAI("Checking resources not previously considered ...");
				i--;
			}
			else iContinueInnerLoopAt = -1;
			continue;
		}
		iContinueInnerLoopAt = -1;
		// (Not going to consider kFirstPlot again anyway)
		apSwappedPlots.insert(pBestPlot);
		CvPlot& kFirstSwapPlot = *findValidBonusSwapDest(kFirstPlot, *pBestPlot);
		CvPlot& kSecondSwapPlot = *findValidBonusSwapDest(*pBestPlot, kFirstPlot);
		IFLOG
		{
			logBBAI("Swapping bonus resources %S (%d,%d) and %S (%d,%d)",
					GC.getInfo(kFirstPlot.getBonusType()).getDescription(),
					kFirstPlot.getX(), kFirstPlot.getY(),
					GC.getInfo(pBestPlot->getBonusType()).getDescription(),
					pBestPlot->getX(), pBestPlot->getY());
			logVegetationChange(kFirstSwapPlot, pBestPlot->getBonusType());
			logVegetationChange(kSecondSwapPlot, kFirstPlot.getBonusType());
			if (&kFirstSwapPlot != &kFirstPlot)
			{
				logBBAI("Moving %S to adj. destination (%d,%d)",
						GC.getInfo(pBestPlot->getBonusType()).getDescription(),
						kFirstSwapPlot.getX(), kFirstSwapPlot.getY());
			}
			if (&kSecondSwapPlot != pBestPlot)
			{
				logBBAI("Moving %S to adj. destination (%d,%d)",
						GC.getInfo(kFirstPlot.getBonusType()).getDescription(),
						kSecondSwapPlot.getX(), kSecondSwapPlot.getY());
			}
			// Re-calc fitness, utility values with logging enabled
			logBBAI("Breakdown of fitness calculations ...");
			EagerEnumMap<PlayerTypes,scaled> aerPlayerWeights;
			setPlayerWeightsPerPlot(kFirstPlot.plotNum(), aerPlayerWeights);
			scaled rFirstVal = calcBonusFitness(
					kFirstPlot, aerPlayerWeights, NO_BONUS, true);
			setPlayerWeightsPerPlot(pBestPlot->plotNum(), aerPlayerWeights);
			scaled rSecondVal = calcBonusFitness(
					*pBestPlot, aerPlayerWeights, NO_BONUS, true);
			logBBAI("Breakdown of swap utility calculation ...");
			scaled rUtil = calcBonusSwapUtil(kFirstPlot, *pBestPlot,
					rFirstVal, rSecondVal, true);
			logBBAI("Swap utility is %d/100\n\n", rUtil.getPercent());
		}
		BonusTypes eFirstOriginalBonus = kFirstPlot.getBonusType();
		kFirstPlot.setBonusType(NO_BONUS);
		if (!canHaveBonus(kFirstSwapPlot, pBestPlot->getBonusType()))
		{
			int iChange = changeVegetation(kFirstSwapPlot, pBestPlot->getBonusType(),
					iFeaturesRemoved + 1 >= iFeaturesAdded);
			(iChange == 0 ? iFeaturesMoved :
					(iChange < 0 ? iFeaturesRemoved : iFeaturesAdded))++;
		}
		kFirstSwapPlot.setBonusType(pBestPlot->getBonusType());
		pBestPlot->setBonusType(NO_BONUS);
		if (!canHaveBonus(kSecondSwapPlot, eFirstOriginalBonus))
		{
			int iChange = changeVegetation(kSecondSwapPlot, eFirstOriginalBonus,
					iFeaturesRemoved + 1 >= iFeaturesAdded);
			(iChange == 0 ? iFeaturesMoved :
					(iChange < 0 ? iFeaturesRemoved : iFeaturesAdded))++;
		}
		kSecondSwapPlot.setBonusType(eFirstOriginalBonus);
	}
	{
		bool bLog = true;
		IFLOG logBBAI("Removed %d terrain features in total, moved %d, added %d.\n\n",
				iFeaturesRemoved, iFeaturesMoved, iFeaturesAdded);
	}
}


void TrueStarts::initContemporaries()
{
	/*	Precompute a list of contemporary leaders for every leader,
		and also store the time differences for those pairs of leaders
		and, for each leader, the maximum over all time differences
		from contemporary leaders. */
	m_contemporaries.reset();
	m_maxTimeDiff.reset();
	// All leaders for which start-of-reign data is available
	std::vector<LeaderHeadTypes> aeLeaders;
	{
		EagerEnumMap<LeaderHeadTypes,bool> aeAdded; // Just to skip duplicates
		// Cover all potentially valid leaders, i.e. also those not playable by the AI.
		for (size_t i = 0; i < m_validHumanCivs.size(); i++)
		{
			LeaderHeadTypes const eLoopLeader = m_validHumanCivs[i].second;
			if (m_truLeaders.get(eLoopLeader) == NULL ||
				m_truLeaders.get(eLoopLeader)->get(
				CvTruLeaderInfo::StartOfReign) == MIN_INT ||
				aeAdded.get(eLoopLeader))
			{
				continue;
			}
			aeAdded.set(eLoopLeader, true);
			aeLeaders.push_back(eLoopLeader);
		}
	}
	for (size_t i = 0; i < aeLeaders.size(); i++)
	{
		LeaderHeadTypes const eFirst = aeLeaders[i];
		int const iFirstStartOfReign = m_truLeaders.get(eFirst)->get(
				CvTruLeaderInfo::StartOfReign);
		std::vector<std::pair<int,LeaderHeadTypes> > aeiTimeDiffPerOther;
		for (size_t j = 0; j < aeLeaders.size(); j++)
		{
			LeaderHeadTypes const eSecond = aeLeaders[j];
			if (eFirst == eSecond)
				continue;
			int iSecondStartOfReign = m_truLeaders.get(eSecond)->get(
					CvTruLeaderInfo::StartOfReign);
			int iDeltaYears = abs(iFirstStartOfReign - iSecondStartOfReign);
			aeiTimeDiffPerOther.push_back(std::make_pair(
					iDeltaYears, eSecond));
		}
		std::sort(aeiTimeDiffPerOther.begin(), aeiTimeDiffPerOther.end());
		/*	I had used a constant value of 6 here, but then Alexander was
			always selected over Pericles. Some randomness should help. */
		int const iMaxContemporaries = 4 + MapRandNum(4);
		int iContemporaries = 0;
		for (size_t j = 0; j < aeiTimeDiffPerOther.size(); j++)
		{
			/*	The iMaxContemporaries nearest leaders are considered (somewhat)
				contemporary. If further leaders are still very close together
				(not going to be the case with the BtS leaders), then those also
				count as contemporary. By picking a constant (well, apart from
				being randomized) number of nearest leaders, a stricter notion
				for contemporaneity applies for periods that the game covers in
				some detail, like the Classical era. */
			if (aeiTimeDiffPerOther[j].first < 25 ||
				iContemporaries < iMaxContemporaries)
			{
				iContemporaries++;
				int iTimeDiff = aeiTimeDiffPerOther[j].first;
				m_contemporaries.set(eFirst,
						aeiTimeDiffPerOther[j].second, iTimeDiff);
				m_maxTimeDiff.set(eFirst,
						std::max(m_maxTimeDiff.get(eFirst), iTimeDiff));
			}
		}
	}
}


bool TrueStarts::isTruBonusDiscouraged(CvTruBonusInfo const* pTruBonus,
	CivilizationTypes eCiv) const
{
	if (pTruBonus == NULL)
		return false;
	CvTruCivInfo const* pTruCiv = m_truCivs.get(eCiv);
	EraTypes aeUntil[] = {
			pTruCiv == NULL || pTruCiv->getGeoRegion() == NO_ARTSTYLE ? (EraTypes)0 :
			pTruBonus->getRegionDiscouragedUntil(pTruCiv->getGeoRegion()),
			pTruBonus->getCivDiscouragedUntil(eCiv),
	};
	for (int i = 0; i < ARRAYSIZE(aeUntil); i++)
	{
		if (aeUntil[i] == NO_ERA || aeUntil[i] > GC.getGame().getStartEra())
			return true;
	}
	return false;
}


bool TrueStarts::isTruBonusEncouraged(CvTruBonusInfo const* pTruBonus,
	CivilizationTypes eCiv) const
{
	if (pTruBonus == NULL)
		return false;
	EraTypes eUntil = pTruBonus->getCivEncouragedUntil(eCiv);
	return (eUntil == NO_ERA || eUntil > GC.getGame().getStartEra());
}


CvTruBonusInfo const* TrueStarts::getTruBonus(CvPlot const& kPlot,
	BonusTypes eBonus) const
{
	if (eBonus == NO_BONUS)
		eBonus = kPlot.getBonusType();
	if (eBonus == NO_BONUS)
		return NULL;
	CvTruBonusInfo const* pTruBonus = m_truBonuses.get(eBonus);
	if (pTruBonus == NULL)
		return NULL;
	if (pTruBonus->get(CvTruBonusInfo::LandOnly) && kPlot.isWater())
		return NULL;
	return pTruBonus;
}


void TrueStarts::changeCivs()
{
	m_civs.reset();
	m_leaders.reset();
	m_civTaken.reset();
	m_leaderTaken.reset();
	m_biasFromLeaderCount.reset();
	{
		CvWString szMapName = GC.getInitCore().getMapScriptName();
		// (Only using this locally for now, but might want to use it elsewhere later.)
		m_bEmptyNewWorld =
		(
				szMapName == CvWString("Terra") ||
				szMapName == CvWString("Earth2") ||
				((szMapName == CvWString("PerfectMongoose") ||
				szMapName == CvWString("Tectonics") ||
				szMapName == CvWString("RandomScriptMap")) &&
				// This will only work when playing in English
				GC.getMap().isCustomMapOption("Old World", true)) ||
				(szMapName == CvWString("NewWorld") &&
				/*	If someone adds options to that map, then there might be
					multiple options with a choice named just "Yes".
					Not supported. */
				GC.getInitCore().getNumCustomMapOptions() <= 4 &&
				GC.getMap().isCustomMapOption("Yes")) ||
				(szMapName == CvWString("Totestra") &&
				GC.getMap().isCustomMapOption("empty", true)) ||
				(szMapName == CvWString("RandomScriptMap") &&
				GC.getMap().isCustomMapOption("Terra")) ||
				(szMapName == CvWString("Caldera") &&
				GC.getMap().isCustomMapOption("Encourage"))
		);
	}
	{
		for (PlayerIter<CIV_ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
		{
			if (std::find(m_truPlayers.begin(), m_truPlayers.end(), &*itPlayer) ==
				m_truPlayers.end())
			{
				m_civs.set(itPlayer->getID(), itPlayer->getCivilizationType());
				m_leaders.set(itPlayer->getID(), itPlayer->getLeaderType());
				m_civTaken.set(itPlayer->getCivilizationType(), true);
				m_leaderTaken.set(itPlayer->getLeaderType(), true);
			}
		}
	}
	bool bUniqueCivs = true;
	{
		std::vector<CivilizationTypes> aeValidHumanCivs;
		std::vector<CivilizationTypes> aeValidAICivs;
		m_validHumanCivs.clear();
		m_validAICivs.clear();
		// (Unnecessary performance tweak ...)
		aeValidHumanCivs.reserve(GC.getNumCivilizationInfos());
		aeValidAICivs.reserve(GC.getNumCivilizationInfos());
		m_validHumanCivs.reserve(GC.getNumLeaderHeadInfos());
		m_validAICivs.reserve(GC.getNumLeaderHeadInfos());
		for (int iPass = 0; iPass < 2; iPass++)
		{
			// Randomize to avoid persistent biases when fitness values are tied
			FOR_EACH_ENUM_RAND(TruCiv, mapRand())
			{
				CvTruCivInfo const& kTruCiv = GC.getInfo(eLoopTruCiv);
				CivilizationTypes const eCiv = kTruCiv.getCiv();
				if (m_civTaken.get(eCiv))
					continue;
				CvCivilizationInfo const& kLoopCiv = GC.getInfo(eCiv);
				if (m_bEmptyNewWorld &&
					(iPass == 0)) // May need all the civs we have on super-Huge maps
				{
					int iLongitudeTimes10 = kTruCiv.get(CvTruCivInfo::LongitudeTimes10);
					int iLatitudeTimes10 = kTruCiv.get(CvTruCivInfo::LatitudeTimes10);
					if (iLongitudeTimes10 < 300 || // Americas
						// Future-proof for Australia
						(iLongitudeTimes10 > 1100 && iLatitudeTimes10 < -100))
					{
						continue;
					}
				}
				if (kLoopCiv.isPlayable())
					aeValidHumanCivs.push_back(eCiv);
				if (kLoopCiv.isAIPlayable())
					aeValidAICivs.push_back(eCiv);
			}
			if (aeValidHumanCivs.size() >= m_truHumans.size() &&
				aeValidAICivs.size() >= m_truPlayers.size())
			{
				break;
			}
		}
		FOR_EACH_ENUM_RAND(LeaderHead, mapRand())
		{
			for (size_t i = 0; i < aeValidAICivs.size(); i++)
			{
				if (GC.getInfo(aeValidAICivs[i]).isLeaders(eLoopLeaderHead) &&
					!m_leaderTaken.get(eLoopLeaderHead))
				{
					m_validAICivs.push_back(std::make_pair(
							aeValidAICivs[i], eLoopLeaderHead));
				}
			}
			for (size_t i = 0; i < aeValidHumanCivs.size(); i++)
			{
				if (GC.getInfo(aeValidHumanCivs[i]).isLeaders(eLoopLeaderHead))
				{
					m_validHumanCivs.push_back(std::make_pair(
							aeValidHumanCivs[i], eLoopLeaderHead));
				}
			}
		}
		if (m_validAICivs.size() < m_truPlayers.size() ||
			m_validHumanCivs.size() < m_truHumans.size())
		{
			FErrorMsg("Too few valid leaders found");
			return;
		}
		if (m_validAICivs.size() < m_truPlayers.size() ||
			aeValidHumanCivs.size() < m_truHumans.size())
		{
			bUniqueCivs = false;
		}
	}
	{
		EagerEnumMap<CivilizationTypes,int> aeiLeaderCounts;
		for (size_t i = 0; i < m_validAICivs.size(); i++)
			aeiLeaderCounts.add(m_validAICivs[i].first, 1);
		scaled rExtraWeight = per100(GC.getDefineINT(
				"PER_EXTRA_LEADER_CIV_SELECTION_WEIGHT"));
		/*	Players might actually set this to 1, but such a high bias
			is not going to work well.
			(Negative weight might work out OK, doesn't have to be supported.) */
		rExtraWeight.decreaseTo(fixp(0.6));
		/*	This XML setting wasn't intended for True Starts. A weight of 0
			is supposed to result in no bias from the leader count. We can easily
			do that. A weight of 100% is supposed to give every leader the same
			chance of getting chosen. We can't guarantee that, can only use a
			pretty strong bias in that case. */
		scaled const rBiasStrength = fixp(4/3.) * (1 - SQR(rExtraWeight - 1));
		FOR_EACH_ENUM(Civilization)
		{
			m_biasFromLeaderCount.set(eLoopCivilization,
					(scaled(range(aeiLeaderCounts.get(eLoopCivilization) - 1, 0, 4)).
					pow(rBiasStrength) * rBiasStrength * 10).round());
		}
	}
	initContemporaries(); // Want to use the valid-civ lists above; hence not in ctor.
	{
		std::vector<scaled> arOceanityTargets;
		for (size_t i = 0; i < m_validAICivs.size(); i++)
		{
			CvTruCivInfo const& kTruCiv = *m_truCivs.get(m_validAICivs[i].first);
			scaled rSample = per100(kTruCiv.get(
					CvTruCivInfo::Oceanity));
			if (rSample >= 0)
				arOceanityTargets.push_back(rSample);
			m_iMaxMaxElevationTarget = std::max(m_iMaxMaxElevationTarget,
					kTruCiv.get(CvTruCivInfo::MaxElevation));
		}
		if (!arOceanityTargets.empty())
			m_rMedianOceanityTarget = stats::median(arOceanityTargets);
	}
	updateFitnessValues();

	std::vector<std::pair<int,PlayerTypes> > aiePriorityPerPlayer;
	for (TruPlayerIter itPlayer = truPlayers(); itPlayer.hasNext(); ++itPlayer)
	{
		int iBestFitVal = MIN_INT;
		std::vector<std::pair<CivilizationTypes,LeaderHeadTypes> > const& validCivs =
				(itPlayer->isHuman() ? m_validHumanCivs : m_validAICivs);
		for (size_t i = 0; i < validCivs.size(); i++)
		{
			iBestFitVal = std::max(iBestFitVal,
					m_fitnessVals.at(itPlayer->getID()).
					get(validCivs[i].first, validCivs[i].second));
		}
		// Prioritize the most difficult player (worst fit)
		int iPriority = -iBestFitVal;
		if (m_bPrioritizeHumans)
		{
			if (itPlayer->isHuman())
				iPriority += 1000; // absolute priority
			scaled rMinDistHuman = 1;
			for (PlayerIter<HUMAN> itHuman; itHuman.hasNext(); ++itHuman)
			{
				scaled rDistHuman(plotDistance(itPlayer->getStartingPlot(),
						itHuman->getStartingPlot()), GC.getMap().maxPlotDistance());
				rMinDistHuman.decreaseTo(rDistHuman);
			}
			scaled rMult = rMinDistHuman;
			rMult.decreaseTo(fixp(0.5));
			if (iPriority > 0)
				rMult = 1 - rMult;
			rMult += 1; // dilute
			iPriority = (iPriority * (1 + rMult)).round();
		}
		aiePriorityPerPlayer.push_back(std::make_pair(
				iPriority, itPlayer->getID()));
	}
	std::sort(aiePriorityPerPlayer.rbegin(), aiePriorityPerPlayer.rend());
	for (size_t i = 0; i < aiePriorityPerPlayer.size(); i++)
	{
		PlayerTypes const ePlayer = aiePriorityPerPlayer[i].second;
		if (m_leaders.get(ePlayer) != NO_LEADER)
			continue;

		bool bLog = true;
		std::pair<CivilizationTypes,LeaderHeadTypes> ee2ndBestFit(
				NO_CIVILIZATION, NO_LEADER);
		int i2ndBestFitVal = MIN_INT;

		std::pair<CivilizationTypes,LeaderHeadTypes> eeBestFit(
				NO_CIVILIZATION, NO_LEADER);
		int iBestFitVal = MIN_INT;
		std::vector<std::pair<CivilizationTypes,LeaderHeadTypes> > const& validCivs =
				(GET_PLAYER(ePlayer).isHuman() ? m_validHumanCivs : m_validAICivs);
		for (size_t j = 0; j < validCivs.size(); j++)
		{
			if (m_leaderTaken.get(validCivs[j].second) ||
				(bUniqueCivs && m_civTaken.get(validCivs[j].first)))
			{
				continue;
			}
			int iFitVal = m_fitnessVals.at(ePlayer).get(
					validCivs[j].first, validCivs[j].second);
			if (iFitVal > iBestFitVal)
			{
				IFLOG  // Different leader of same civ isn't going to be interesting
				if (validCivs[j].first != eeBestFit.first)
				{
					i2ndBestFitVal = iBestFitVal;
					ee2ndBestFit = eeBestFit;
				}
				iBestFitVal = iFitVal;
				eeBestFit = validCivs[j];
			}
			else
			{
				IFLOG
				{
					if (iFitVal > i2ndBestFitVal &&
						validCivs[j].first != eeBestFit.first)
					{
						i2ndBestFitVal = iFitVal;
						ee2ndBestFit = validCivs[j];
					}
				}
			}
		}
		if (eeBestFit.first != NO_CIVILIZATION &&
			eeBestFit.second != NO_LEADER)
		{
			IFLOG // Recalc w/ log output
			{
				calcFitness(GET_PLAYER(ePlayer),
						eeBestFit.first, eeBestFit.second, true);
				// Also break down calculation for second best fit
				if (ee2ndBestFit.first != NO_CIVILIZATION &&
					ee2ndBestFit.second != NO_LEADER)
				{
					logBBAI("Best alternative to %S:", GC.getInfo(eeBestFit.first).getShortDescription());
					calcFitness(GET_PLAYER(ePlayer),
							ee2ndBestFit.first, ee2ndBestFit.second, true);
				}
				/*	For logging a particular leader that perhaps should've been
					chosen instead. */
				/*LeaderHeadTypes eLeader = (LeaderHeadTypes)
						GC.getInfoTypeForString("LEADER_");
				if (eeBestFit.second && ee2ndBestFit.second != eLeader &&
					!m_leaderTaken.get(eLeader))
				{
					CivilizationTypes eLeaderCiv = NO_CIVILIZATION;
					FOR_EACH_ENUM(Civilization)
					{
						if (GC.getInfo(eLoopCivilization).isLeaders(eLeader) &&
							!m_civTaken.get(eLoopCivilization))
						{
							eLeaderCiv = eLoopCivilization;
							break;
						}
					}
					if (eLeaderCiv != NO_CIVILIZATION)
					{
						logBBAI("For comparison: Fitness eval for %S", GC.getInfo(eLeader).getDescription());
						calcFitness(GET_PLAYER(ePlayer), eLeaderCiv, eLeader, true);
					}
				}*/
			}
			if (GC.getGame().isOption(GAMEOPTION_LEAD_ANY_CIV))
			{
				/*	When leaders are unrestricted, then the best-fit has been
					selected only based on a civ. Stick to that civ, and
					combine it with a random leader. */
				std::vector<LeaderHeadTypes> aeAvailableLeaders;
				for (size_t j = 0; j < validCivs.size(); j++)
				{
					if (!m_leaderTaken.get(validCivs[j].second))
						aeAvailableLeaders.push_back(validCivs[j].second);
				}
				if (!aeAvailableLeaders.empty())
				{
					eeBestFit.second = aeAvailableLeaders[MapRandNum(
							aeAvailableLeaders.size())];
				}
				else FErrorMsg("At least eeBestFit.second should be available");
			}
			m_civs.set(ePlayer, eeBestFit.first);
			m_leaders.set(ePlayer, eeBestFit.second);
			m_civTaken.set(eeBestFit.first, true);
			m_leaderTaken.set(eeBestFit.second, true);
			// To avoid assigning alternative colors in the loop below
			GC.getInitCore().setColor((PlayerTypes)ePlayer, NO_PLAYERCOLOR);
		}
		updateFitnessValues(); // Recalc each time we lock a player in
	}
	bool bLog = true;
	scaled rAvgFitness;
	for (TruPlayerIter itPlayer = truPlayers(); itPlayer.hasNext(); ++itPlayer)
	{
		CivilizationTypes const eCiv = m_civs.get(itPlayer->getID());
		LeaderHeadTypes const eLeader = m_leaders.get(itPlayer->getID());
		if (eCiv == NO_CIVILIZATION)
		{
			FErrorMsg("No civ found for player");
			continue;
		}
		if (eLeader == NO_LEADER)
		{
			FErrorMsg("No leader found for player");
			continue;
		}
		/*	bChangeDescr param:
			Non-scenario games leave all civ and leader names empty,
			which means that CvInfo descriptions get used. That's fine, but
			the hardwired names in scenarios need to be changed explicitly. */
		itPlayer->changeCiv(eCiv, GC.getGame().isScenario(), true);
		itPlayer->changeLeader(eLeader, GC.getGame().isScenario());
		IFLOG rAvgFitness += m_fitnessVals.at(itPlayer->getID()).get(eCiv, eLeader);
	}
	IFLOG if(rAvgFitness!=0) logBBAI("Avg. fitness val: %d\n\n",
			(rAvgFitness / m_truPlayers.size()).round());
}


void TrueStarts::calculateRadius(CvPlayer const& kPlayer)
{
	CvMap const& kMap = GC.getMap();
	scaled rRadius = 6 + kMap.getWorldSize();
	{
		scaled rCrowdedness(PlayerIter<CIV_ALIVE>::count(),
				GC.getGame().getRecommendedPlayers());
		if (rCrowdedness > 1)
			rRadius /= rCrowdedness.sqrt();
		else rRadius += 2 / rCrowdedness - 1;
	}
	// Increase radius when there's a lot of ocean in surrounding plots
	int iExtra = 0;
	scaled const rTargetNonOcean = fixp(1.85) * SQR(rRadius);
	CvPlot const& kStart = *kPlayer.getStartingPlot();
	do
	{
		int iNonOcean = 0;
		for (PlotCircleIter itPlot(kStart, rRadius.round() + iExtra);
			itPlot.hasNext(); ++itPlot)
		{
			if (sameArea(*itPlot, kStart) ||
				(itPlot->getTerrainType() == GC.getWATER_TERRAIN(true) &&
				itPlot->isAdjacentToArea(kStart.getArea())))
			{
				/*	Would be nice not to count plots fully that are close to
					another starting plot (tbd.?) */
				iNonOcean++;
			}
		}
		if (iNonOcean >= rTargetNonOcean)
			break;
		iExtra++;
	} while (iExtra < fixp(0.4) * rRadius);
	rRadius += iExtra;
	m_radii.set(kPlayer.getID(), rRadius.round());
}


void TrueStarts::updateFitnessValues()
{
	m_fitnessVals.clear();
	m_fitnessVals.resize(NUM_CIV_PLAYER_TYPES);
	/*	(Could probably skip the players that we're already done with,
		but I don't think performance matters much here.) */
	for (TruPlayerIter itPlayer = truPlayers(); itPlayer.hasNext(); ++itPlayer)
	{
		std::vector<std::pair<CivilizationTypes,LeaderHeadTypes> > const& validCivs =
				(itPlayer->isHuman() ? m_validHumanCivs : m_validAICivs);
		for (size_t i = 0; i < validCivs.size(); i++)
		{
			m_fitnessVals.at(itPlayer->getID()).set(
					validCivs[i].first, validCivs[i].second,
					calcFitness(*itPlayer, validCivs[i].first, validCivs[i].second));
		}
	}
}


namespace
{
	scaled distWeight(CvPlot const& kStart, CvPlot const& kPlot, int iMaxDist)
	{
		int iPlotDist = plotDistance(&kStart, &kPlot);
		if (!kStart.sameArea(kPlot)) // (Don't use our local sameArea function here)
			iPlotDist *= 2;
		return scaled::max(0, 1 - scaled(iPlotDist, iMaxDist + 1).
				pow(fixp(1.7)));
	}
}

// Tallies stats about kPlayer's starting surroundings for the fitness evaluation
TrueStarts::SurroundingsStats::SurroundingsStats(CvPlayer const& kPlayer,
	TrueStarts const& kTruStarts)
:	m_iTemperateDesertPenalty(0), m_iTemperateTundraPenalty(0)
{
	CvPlot const& kStart = *kPlayer.getStartingPlot();
	bool const bSmallMap = (GC.getMap().getWorldSize() <= 2);
	auto_ptr<PlotCircleIter> pSurroundings = kTruStarts.getSurroundings(kPlayer);
	for (PlotCircleIter& itPlot = *pSurroundings; itPlot.hasNext(); ++itPlot)
	{
		scaled const rWeight = kTruStarts.m_plotWeights.get(
				kPlayer.getID(), itPlot->plotNum());
		if (itPlot->isLake())
			continue;
		if (!sameArea(*itPlot, kStart))
		{
			/*	Water in the high latitudes is usually less relevant for gameplay,
				probably won't feel like playing a maritime civ. */
			scaled rLatMult = 1;
			if (!itPlot->isWater()) // Count land area double
				m_rDifferentAreaPlotWeights += rWeight;
			else if (kTruStarts.m_bMapHasLatitudes)
			{
				int const iMaxLat = CvTruCivInfo::maxLatitude() / 10;
				scaled const rTemperateLat = fixp(0.58) * iMaxLat;
				int const iAbsPlotLat = itPlot->getLatitude();
				// Count water that's warmer than the starting plot fully
				if (scaled::max(rTemperateLat, kStart.getLatitude()) < iAbsPlotLat)
				{
					rLatMult -= ((scaled::min(iAbsPlotLat, iMaxLat) - rTemperateLat)
							/ iMaxLat).sqrt();
				}
			}
			m_rDifferentAreaPlotWeights += rWeight * rLatMult;
			continue;
		}
		{
			scaled rSpaceWeight = rWeight.sqrt();
			m_rAreaSpaceWeights += rSpaceWeight;
			m_rAreaXSpaceWeights += GC.getMap().xDistance(
					kStart.getX(), itPlot->getX());
			m_rAreaYSpaceWeights += GC.getMap().yDistance(
					kStart.getY(), itPlot->getY());
		}
		m_rAreaPlotWeights += rWeight;
		if (itPlot->isHills())
		{
			m_rAreaHillScore += rWeight;
			int iOrthAdj = 0;
			FOR_EACH_ORTH_ADJ_PLOT(*itPlot)
			{
				if (pAdj->isHills() || pAdj->isPeak())
				{
					m_rAreaHillScore += 2 * rWeight / (3 + iOrthAdj);
					iOrthAdj++;
				}
			}
			int iDiagAdj = 0;
			FOR_EACH_DIAG_ADJ_PLOT(*itPlot)
			{
				if (pAdj->isHills() || pAdj->isPeak())
				{
					m_rAreaHillScore += rWeight / (2 + iOrthAdj + iDiagAdj);
					iDiagAdj++;
				}
			}
		}
		else if (itPlot->isPeak())
		{
			/*	Caveat: If this calculation is changed, then the rTypicalPeakScore
				value in calcFitness may also need to be changed. */
			m_rAreaPeakScore += rWeight;
			FOR_EACH_ORTH_ADJ_PLOT(*itPlot)
			{
				if (pAdj->isPeak())
					m_rAreaPeakScore += 2 * rWeight / 3;
				if (pAdj->isHills())
					m_rAreaPeakScore += rWeight / 3;
			}
			FOR_EACH_DIAG_ADJ_PLOT(*itPlot)
			{
				if (pAdj->isPeak())
					m_rAreaPeakScore += rWeight / 2;
			}
		}
		// Decrease weight for distant plots when it comes to rivers
		scaled rRiverWeight = SQR(rWeight);
		m_rAreaRiverWeights += rRiverWeight;
		if (itPlot->isRiver())
		{
			m_rAreaRiverScore += (itPlot->getRiverCrossingCount()
					+ 2) * rRiverWeight; // dilute
		}
		if (itPlot->getTerrainType() == kTruStarts.m_eDesert)
		{
			if (itPlot.currPlotDist() <= CITY_PLOTS_RADIUS)
				m_iTemperateDesertPenalty = (bSmallMap ? 70 : 125);
			else if (m_iTemperateDesertPenalty == 0 &&
				itPlot.currPlotDist() == CITY_PLOTS_RADIUS + 1)
			{
				m_iTemperateDesertPenalty = (bSmallMap ? 50 : 95);
			}
		}
		if (itPlot->getTerrainType() == kTruStarts.m_eTundra)
		{
			if (itPlot.currPlotDist() == CITY_PLOTS_RADIUS)
				m_iTemperateTundraPenalty = (bSmallMap ? 45 : 70);
			else if (m_iTemperateTundraPenalty == 0 &&
				itPlot.currPlotDist() == CITY_PLOTS_RADIUS + 1)
			{
				m_iTemperateTundraPenalty = (bSmallMap ? 30 : 50);
			}
		}
	}
}


int TrueStarts::calcFitness(CvPlayer const& kPlayer, CivilizationTypes eCiv,
	LeaderHeadTypes eLeader, bool bLog) const
{
	CvPlot const& kStart = *kPlayer.getStartingPlot();
	IFLOG logBBAI("Fitness calc for %S of %S on (%d,%d)",
			GC.getInfo(eLeader).getDescription(), GC.getInfo(eCiv).getShortDescription(),
			kStart.getX(), kStart.getY());
	CvTruCivInfo const& kTruCiv = *m_truCivs.get(eCiv);
	int iFitness = 1000;
	if (m_bMapHasLatitudes)
	{
		int const iAbsStartLat = kStart.getLatitude();
		int iAbsStartLatAdjustedTimes10 = iAbsStartLat * 10;
		/*	Try to match latitudes slightly higher than the actual latitudes -
			to bias the civ choice toward the temperate zones and subtropics. */
		iAbsStartLatAdjustedTimes10 += (scaled(std::max(0,
				40 - iAbsStartLat)).pow(fixp(0.3)) * 10).round();
		// Temperate latitudes need to keep some distance from the Tundra
		iAbsStartLatAdjustedTimes10 -= (scaled(std::max(0,
				std::min(52, iAbsStartLat) - 40)).pow(fixp(0.4)) * 10).round();
		int iAbsLatTimes10 = range(iAbsStartLatAdjustedTimes10, 0, 900);
		int iCivAbsLatTimes10 = m_absTargetLatitudeTimes10.get(eCiv);
		int iError = iCivAbsLatTimes10 - iAbsLatTimes10;
		bool const bStartTooWarm = (iError > 0);
		iError = abs(iError);
		int const iMaxMagnifiedError = 5;
		int iErrorMagnifier = std::max(0, iMaxMagnifiedError -
				/*	Errors near the temperate-subarctic and the subtropic-tropic
					boundaries are especially noticeable */
				(bStartTooWarm ? abs(iAbsStartLat - 20) : abs(iAbsStartLat - 50)));
		/*	Not so bad to place very northerly civs farther south; they'll still
			be pretty close to Tundra terrain. */
		if (bStartTooWarm && iAbsStartLat > 52)
			iErrorMagnifier = -3; // minify
		// Placing desert civs too far north is also not too bad
		if (!bStartTooWarm && iCivAbsLatTimes10 >= 250 && iCivAbsLatTimes10 < 350)
			iErrorMagnifier = -2;
		iError = std::max(0, iError - iMaxMagnifiedError * 10) + // Not magnified
				(std::min(iError, iMaxMagnifiedError * 10) * // Magnify this portion
				// At most double it
				(100 + (100 * iErrorMagnifier) / iMaxMagnifiedError)) / 100;
		int iLatPenalty = (3 * iError) / 2; // weight
		/*	(The latitude adjustment for non-Temperate climates seems to work
			quite well, so I don't think we should lower our confidence much here.) */
		if (GC.getMap().getClimate() != m_eTemperateClimate)
			iLatPenalty = (iLatPenalty * 75) / 100;
		IFLOG logBBAI("Penalty for latitude %d (starting at %d, target: %d/10)",
				iLatPenalty, iAbsStartLat, m_absTargetLatitudeTimes10.get(eCiv));
		iFitness -= iLatPenalty;
	}
	{
		CvMap const& kMap = GC.getMap();
		int const iCivLatitudeTimes10 = kTruCiv.get(CvTruCivInfo::LatitudeTimes10);
		int const iCivLongitudeTimes10 = kTruCiv.get(CvTruCivInfo::LongitudeTimes10);
		int iOtherPlayers = 0;
		int iAvgDistErrorPercent = 0;
		// Include the players with fixed civs (non-"tru" players) in this loop
		FOR_EACH_NON_DEFAULT_PAIR(m_civs, Player, CivilizationTypes)
		{
			if (perPlayerVal.first == kPlayer.getID())
				continue;
			iOtherPlayers++;
			CvTruCivInfo const& kLoopTruCiv = *m_truCivs.get(perPlayerVal.second);
			CvPlot const& kOtherStart = *GET_PLAYER(perPlayerVal.first).getStartingPlot();
			int iDist = kMap.plotDistance(&kOtherStart, &kStart);
			int iMaxDist = GC.getMap().maxPlotDistance();
			int iLoopLatitudeTimes10 = kLoopTruCiv.get(CvTruCivInfo::LatitudeTimes10);
			int iLatitudeDiffTimes10 = abs(iCivLatitudeTimes10 - iLoopLatitudeTimes10);
			if (iLatitudeDiffTimes10 > m_iMaxLatitudeDiffTimes10) // wrap
			{
				iLatitudeDiffTimes10 = 2 * m_iMaxLatitudeDiffTimes10
						- iLatitudeDiffTimes10;
				FAssert(kMap.isWrapY());
			}
			int iLongitudeDiffTimes10 = abs(iCivLongitudeTimes10
					- kLoopTruCiv.get(CvTruCivInfo::LongitudeTimes10));
			if (iLongitudeDiffTimes10 > m_iMaxLongitudeDiffTimes10)
			{
				iLongitudeDiffTimes10 = 2 * m_iMaxLongitudeDiffTimes10
						- iLongitudeDiffTimes10;
			}
			int iGeoDist = std::max(iLongitudeDiffTimes10, iLatitudeDiffTimes10)
					+ std::min(iLongitudeDiffTimes10, iLatitudeDiffTimes10) / 2;
			int iGeoDistPercent = 100 * iGeoDist / m_iMaxGeoDist;
			FAssert(iGeoDistPercent <= 100);
			int iDistPercent = 100 * iDist / iMaxDist;
			/*	(Don't need such an adjustment for geo dist - America and Eurasia
				are pretty far apart anyway, and all other relevant places are
				connected by land.) */
			if (!sameArea(kStart, kOtherStart))
				iDistPercent += (18 * (100 - iDistPercent)) / 100;
			int iErrorPercent = abs(iDistPercent - iGeoDistPercent);
			{
				/*	Mean dist value at which the error is given maximal weight.
					Because, if both distances are short or long, it's not so important
					how short or long exactly. Don't need a scale model; mainly want to
					have the right neighbors. */
				int const iMaxErr = 25;
				iErrorPercent *= (iMaxErr + std::max(0, iMaxErr - std::min(
						abs(std::max(iDistPercent, iGeoDistPercent) - iMaxErr),
						abs(std::min(iDistPercent, iGeoDistPercent) - iMaxErr))));
				iErrorPercent /= iMaxErr;
				/*	Avoid placing civs that are supposed to be close together
					at opposing sides of the equator */
				if (iCivLatitudeTimes10 * iLoopLatitudeTimes10 < 0)
					iErrorPercent = std::max(iErrorPercent, iMaxErr + 5);
			}
			if (GET_PLAYER(perPlayerVal.first).isHuman() && m_bPrioritizeHumans)
				iErrorPercent *= 2;
			iAvgDistErrorPercent += iErrorPercent;
			IFLOG logBBAI("Dist error for %S: %d pts. (plot dist %d percent, geo dist %d percent)",
					GC.getInfo(perPlayerVal.second).getShortDescription(), iErrorPercent, iDistPercent, iGeoDistPercent);
		}
		scaled rAvgDistErrorPenalty = iAvgDistErrorPercent * fixp(0.72);
		if (iOtherPlayers > 0)
		{
			/*	Not quite an average (that would be pow(1)). I do want distances
				to matter more as the last few civs are chosen. */
			rAvgDistErrorPenalty /= scaled(iOtherPlayers).pow(fixp(0.7));
			IFLOG logBBAI("Subtracting %d from fitness for dist error", rAvgDistErrorPenalty.round());
		}
		iFitness -= rAvgDistErrorPenalty.round();
	}
	int const iOurMaxTimeDiff = m_maxTimeDiff.get(eLeader);
	if (iOurMaxTimeDiff >= 0)
	{
		int iFromContemporaries = 0;
		int const iWeight = 36;
		int const iFixed = 14;
		/*	Go through all players already assigned whose leader is
			contemporary with eLeader. We only care which leaders are in
			the game here, not where they're located on the map.
			And we include players with forced leader (non-"tru" players). */
		FOR_EACH_NON_DEFAULT_PAIR(m_leaders, Player, LeaderHeadTypes)
		{
			if (perPlayerVal.first == kPlayer.getID())
				continue;
			int iTimeDiff = m_contemporaries.get(eLeader, perPlayerVal.second);
			/*	Contemporary relations aren't always symmetrical, If we're
				their contemporary, that's also good. */
			bool bMutuallyContemporary = false;
			int iMaxTimeDiff = iOurMaxTimeDiff;
			if (iTimeDiff < 0)
			{
				iTimeDiff = m_contemporaries.get(perPlayerVal.second, eLeader);
				iMaxTimeDiff = m_maxTimeDiff.get(perPlayerVal.second);
			}
			else
			{
				bMutuallyContemporary = (0 <=
						m_contemporaries.get(perPlayerVal.second, eLeader));
			}
			if (iTimeDiff >= 0)
			{
				FAssert(iTimeDiff <= iMaxTimeDiff);
				int iPlus = (iMaxTimeDiff - iTimeDiff) * iWeight / iMaxTimeDiff;
				int iMult = 1;
				if (TEAMID(perPlayerVal.first) == kPlayer.getTeam())
					iMult += 1;
				if (GET_PLAYER(perPlayerVal.first).isHuman() && m_bPrioritizeHumans)
					iMult += 1;
				iPlus *= iMult;
				iPlus += iFixed;
				if (bMutuallyContemporary)
					iPlus += iFixed; // add a second time
				else IFLOG logBBAI("Not counted as mutually contemporary");
				iFromContemporaries += iPlus;
				IFLOG logBBAI("Contemporary leader on the map: %S. Time difference is %d years. Adding %d to fitness (to be adjusted to civ count)",
						GC.getInfo(perPlayerVal.second).getDescription(), iTimeDiff, iPlus);
			}
		}
		iFitness += (iFromContemporaries /
				scaled(m_leaders.numNonDefault()).sqrt()).round();
	}
	{
		scaled rFromBonuses;
		scaled rBonusDiscourageFactor = -scaled(3750, std::max(1,
				m_discouragedBonusesTotal.get(eCiv))).sqrt();
		scaled rBonusEncourageFactor = scaled(750, std::max(1,
				m_encouragedBonusesTotal.get(eCiv))).sqrt();
		bool const bSanitize = (GC.getGame().isScenario() ?
				GC.getDefineBOOL(CvGlobals::TRUE_STARTS_SANITIZE_SCENARIOS) :
				GC.getDefineBOOL(CvGlobals::TRUE_STARTS_SANITIZE));
		// Higher coefficients when ill-fitting resources can't be sanitized away
		if (!bSanitize)
		{
			rBonusDiscourageFactor *= 2;
			rBonusEncourageFactor *= 2;
		}
		/*	For the escalating effect of these counts, it's significant
			that the order of plot traversal is a spiral away from the center. */
		EagerEnumMap<BonusTypes,int> aeiEncouragedCount;
		EagerEnumMap<BonusTypes,int> aeiDiscouragedCount;
		auto_ptr<PlotCircleIter> pSurroundings = getSurroundings(kPlayer);
		for (PlotCircleIter& itPlot = *pSurroundings; itPlot.hasNext(); ++itPlot)
		{
			scaled const rWeight = m_plotWeights.get(
					kPlayer.getID(), itPlot->plotNum());
			BonusTypes const eBonus = itPlot->getBonusType();
			if (eBonus != NO_BONUS)
			{
				if (isBonusDiscouraged(*itPlot, eCiv))
				{
					aeiDiscouragedCount.add(eBonus, 1);
					scaled rVal = rWeight * rBonusDiscourageFactor;
					if (bSanitize) // Multiple bad resources will be difficult to sanitize
						rVal *= scaled(aeiDiscouragedCount.get(eBonus)).pow(fixp(2/3.));
					IFLOG logBBAI("Discouraging %S at %d,%d (dist. factor: %d percent): -%d/100 fitness",
							GC.getInfo(eBonus).getDescription(), itPlot->getX(), itPlot->getY(),
							rWeight.getPercent(), -rVal.getPercent());
					rFromBonuses += rVal;
				}
				else if (isBonusEncouraged(*itPlot, eCiv))
				{
					aeiEncouragedCount.add(eBonus, 1);
					scaled rVal = rWeight * rBonusEncourageFactor /
							// Mainly want to encourage a single instance
							aeiEncouragedCount.get(eBonus);
					/*	Extra encouragement for resources that are widely discouraged
						(read: Corn). B/c those resources will have to go _somewhere_
						when sanitizing, so having a civ on the map that actually
						likes them is helpful. */
					if (bSanitize)
					{
						int iAlreadyEncouraged = 0;
						FOR_EACH_NON_DEFAULT_PAIR(m_civs, Player, CivilizationTypes)
						{
							if (isBonusEncouraged(*itPlot, perPlayerVal.second) &&
								/*	Only "tru" players here; those with a fixed civ
									are disregarded during sanitization. */
								std::find(m_truPlayers.begin(), m_truPlayers.end(),
								&GET_PLAYER(perPlayerVal.first)) != m_truPlayers.end())
							{
								IFLOG logBBAI("%S already encouraged by %S", GC.getInfo(eBonus).getDescription(),
										GC.getInfo(perPlayerVal.second).getShortDescription());
								iAlreadyEncouraged++;
							}
						}
						rVal *= 1 + (m_bonusDiscouragedRatio.get(eBonus) / (iAlreadyEncouraged + 1));
					}
					IFLOG if(rVal.getPercent()!=0) logBBAI("Encouraging %S at %d,%d (dist. factor: %d percent): +%d/100 fitness",
							GC.getInfo(eBonus).getDescription(), itPlot->getX(), itPlot->getY(),
							rWeight.getPercent(), rVal.getPercent());
					rFromBonuses += rVal;
				}
			}
		}
		IFLOG if(rFromBonuses!=0) logBBAI("Total fitness from bonus resources: %d",
				rFromBonuses.round());
		iFitness += rFromBonuses.round();
		{
			int iFromClimate = calcClimateFitness(kPlayer,
					kTruCiv.get(CvTruCivInfo::Precipitation),
					kTruCiv.get(CvTruCivInfo::ClimateVariation), bLog);
			IFLOG logBBAI("Fitness value from climate: %d", iFromClimate);
			iFitness += iFromClimate;
		}
		SurroundingsStats const& kStats = *m_surrStats.get(kPlayer.getID());
		{
			int const iAbsLatitudeTargetTimes10 = abs(kTruCiv.get(
					CvTruCivInfo::LatitudeTimes10));
			{
				int iPenalty = kStats.temperateDesertPenalty();
				// Climate fitness val isn't good at discouraging small desert patches
				if (iPenalty > 0 &&
					/*	With the BtS civ roster, this covers only Europe incl. Turkey
						(but not all of Europe). */
					(iAbsLatitudeTargetTimes10 >= 409 &&
					kTruCiv.get(CvTruCivInfo::Oceanity) >= 10) ||
					// Korea and Japan
					(kTruCiv.get(CvTruCivInfo::Precipitation) >= 1000 &&
					kTruCiv.get(CvTruCivInfo::Oceanity) >= 50))
				{
					if (iAbsLatitudeTargetTimes10 < 415)
						iPenalty /= 2;
					IFLOG logBBAI("Fitness penalty of %d for desert close to starting plot", iPenalty);
					iFitness -= iPenalty;
				}
			}
			{
				int iPenalty = kStats.temperateTundraPenalty();
				// Climate fitness val only looks at precipitation, not temperature.
				if (iPenalty > 0 &&
					iAbsLatitudeTargetTimes10 <= 535 &&
					kTruCiv.get(CvTruCivInfo::Oceanity) >= 10)
				{
					IFLOG logBBAI("Fitness penalty of %d for tundra close to starting plot", iPenalty);
					iFitness -= iPenalty;
				}
			}
		}
		{
			scaled const rTargetOceanity = per100(kTruCiv.get(CvTruCivInfo::Oceanity));
			if (rTargetOceanity >= 0)
			{
				scaled rSameAreaRatio = kStats.areaPlotWeights();
				if (kStats.areaPlotWeights() > 0)
				{
					rSameAreaRatio /= kStats.areaPlotWeights() +
							kStats.differentAreaPlotWeights();
				}
				IFLOG logBBAI("Same-area plot ratio: %d percent", rSameAreaRatio.getPercent());
				// Give typical oceanity targets less impact on fitness
				scaled rOceanityWeight = rTargetOceanity - m_rMedianOceanityTarget;
				/*	Normalize; i.e. if the median is 0.25, then the weight should
					be more sensitive for targets below the median than above. */
				if (rOceanityWeight > 0 && m_rMedianOceanityTarget < 1)
					rOceanityWeight /= 1 - m_rMedianOceanityTarget;
				else if (m_rMedianOceanityTarget > 0)
					rOceanityWeight /= m_rMedianOceanityTarget;
				rOceanityWeight = rOceanityWeight.abs();
				FAssert(rOceanityWeight <= 1);
				rOceanityWeight += fixp(0.5); // dilute
				/*	Reduce weight for high targets b/c we're unlikely to encounter
					that much water on a Civ map */
				rOceanityWeight *= scaled::min(1, fixp(1.5) - rTargetOceanity);
				IFLOG logBBAI("Target ratio: %d percent, weight factor %d percent (median oceanity: %d percent)",
						(1 - rTargetOceanity).getPercent(), rOceanityWeight.getPercent(),
						m_rMedianOceanityTarget.getPercent());
				scaled rFromOceanity = (1 - rSameAreaRatio - rTargetOceanity).abs() * -175 *
						rOceanityWeight;
				IFLOG logBBAI("Fitness penalty from oceanity: %d", -rFromOceanity.round());
				iFitness += rFromOceanity.round();
				if (rTargetOceanity <= 0 && kStart.isCoastalLand(-1))
				{
					int iExtra = 45;
					IFLOG logBBAI("Extra penalty of %d for continental civ starting at coast", iExtra);
					iFitness -= iExtra;
				}
			}
			else IFLOG logBBAI("No oceanity data available");
		}
		{
			int const iMajorRiverWeight = kTruCiv.get(CvTruCivInfo::MajorRiverWeight);
			if (iMajorRiverWeight != 0 && kStats.areaRiverWeights() > 0)
			{
				scaled rMeanRiverScore = kStats.areaRiverScore() /
						kStats.areaRiverWeights();
				bool bNearRiver = kStart.isRiver();
				if (!bNearRiver)
				{
					FOR_EACH_ADJ_PLOT(kStart)
					{
						if (pAdj->isRiver())
						{
							bNearRiver = true;
							break;
						}
					}
				}
				if (!bNearRiver)
				{
					IFLOG logBBAI("No river near starting plot");
					rMeanRiverScore /= 2;
				}
				IFLOG logBBAI("Mean river score per area plot: %d", rMeanRiverScore.getPercent());
				scaled rFromRiver = (SQR(rMeanRiverScore) * fixp(1.1) - 1) * 100;
				rFromRiver.decreaseTo(150);
				if (rFromRiver < 0 && iMajorRiverWeight > 0)
					rFromRiver *= fixp(1.5);
				rFromRiver *= per100(iMajorRiverWeight);
				IFLOG logBBAI("Fitness from major river: %d (civ weight: %d percent)",
						rFromRiver.round(), iMajorRiverWeight);
				iFitness += rFromRiver.round();
			}
		}
		{
			scaled rDiv = scaled::max(kStats.areaPlotWeights(), 1);
			scaled rAreaHillScore = kStats.areaHillScore();
			scaled rAreaPeakScore = kStats.areaPeakScore();
			rAreaHillScore /= rDiv;
			rAreaPeakScore /= rDiv;
			IFLOG logBBAI("Area hills and peak score: %d, %d",
					rAreaHillScore.getPercent(), rAreaPeakScore.getPercent());
			scaled const rTypicalPeakScore = 7;
			if (m_bAdjustPeakScore && m_rMedianPeakScore > 2 * rTypicalPeakScore)
			{
				rAreaPeakScore *= (rTypicalPeakScore / m_rMedianPeakScore).pow(fixp(0.6));
				IFLOG logBBAI("Peak score adjusted to map: %d", rAreaPeakScore.getPercent());
			}
			scaled const rTargetMountainCover = kTruCiv.get(CvTruCivInfo::MountainousArea);
			if (rTargetMountainCover >= 0)
			{
				scaled rMountainCover = 100 * (rAreaHillScore / 2 + rAreaPeakScore);
				scaled rFromMountainCover = (rMountainCover - rTargetMountainCover).
						abs() * -2; // arbitrary weight factor
				IFLOG logBBAI("Fitness penalty from mountainous area: %d (target %d percent, have %d)",
						rFromMountainCover.round(), rTargetMountainCover.round(), rMountainCover.round());
				iFitness += rFromMountainCover.round();
			}
			int iTargetMaxElev = kTruCiv.get(CvTruCivInfo::MaxElevation);
			if (iTargetMaxElev > MIN_INT)
			{
				scaled rMaxElev = (rAreaPeakScore.getPercent() + 8) * 200;
				// Scenarios may have enormous clumps of peaks
				rMaxElev.decreaseTo(m_iMaxMaxElevationTarget);
				scaled rFromMaxElev = (rMaxElev.sqrt() - scaled(iTargetMaxElev).sqrt()).
						abs() * -fixp(2.4); // arbitrary weight factor
				IFLOG logBBAI("Fitness penalty from max. elevation: %d (target %d m, have %d m)",
						rFromMaxElev.round(), iTargetMaxElev, rMaxElev.round());
				iFitness += rFromMaxElev.round();
			}
		}
		{
			int const iHistoricalArea = kTruCiv.get(CvTruCivInfo::TotalArea);
			if (iHistoricalArea >= 0)
			{
				scaled rTargetSpace = iHistoricalArea;
				rTargetSpace.clamp(10, 5000); // So these can be pretty far apart
				// ... but we don't want the target space multipliers to be far apart
				rTargetSpace.exponentiate(fixp(0.215));
				rTargetSpace += 4;
				rTargetSpace /= fixp(8.35);
				/*	Generally, I don't think the fitness calc should take into account
					the overall properties of the map. E.g. if a player picks a
					Tropical climate, they should get tropical civs - not the same civs
					as always. The space preference is an exception: civs are perceived
					as small or large very much in relation to other civs on the map. */
				scaled rSpace = kStats.areaSpaceWeights() / m_rMedianSpace;
				int iFromSpace = 20 - (((rTargetSpace - rSpace) * 100).
						abs().pow(fixp(4/3.)) / fixp(2.25)).round();
				IFLOG logBBAI("Fitness val from space for expansion: %d (target %d percent, have %d)",
						iFromSpace, rTargetSpace.getPercent(), rSpace.getPercent());
				iFitness += iFromSpace;
			}
			int const iHStretchPercent = kTruCiv.get(CvTruCivInfo::HStretch);
			if (iHStretchPercent >= 0)
			{
				scaled rTargetHStretch = per100(iHStretchPercent);
				scaled rHStretch = kStats.areaXSpaceWeights() /
						std::max(kStats.areaYSpaceWeights(), scaled::epsilon());
				int iFromShape=0;
				if ((rHStretch - 1) * (rTargetHStretch - 1) > 0)
				{
					iFromShape = std::min(
							(1 - rHStretch).abs(),
							(1 - rTargetHStretch).abs()).getPercent();
				}
				else
				{
					iFromShape = -std::min(
							(rHStretch - 1).abs(),
							(rTargetHStretch - 1).abs()).getPercent();
				}
				IFLOG if(iFromShape!=0) logBBAI("Fitness val from shape: %d (target %d percent, have %d)",
						iFromShape, rTargetHStretch.getPercent(), rHStretch.getPercent());
				iFitness += iFromShape;
			}
		}
	}
	{
		int const iBiasFromLeaderCount = m_biasFromLeaderCount.get(eCiv);
		int iCivBias = kTruCiv.get(CvTruCivInfo::Bias);
		if (iCivBias < 0)
		{
			// Could use map rand - except that logging wouldn't work then.
			std::vector<int> aiInputs;
			aiInputs.push_back(eCiv);
			aiInputs.push_back(kStart.getX());
			aiInputs.push_back(kStart.getY());
			aiInputs.push_back(GC.getGame().getInitialRandSeed().first);
			/*	So that civs with easy-to-meet preferences at least sometimes
				don't appear even in games with a high civ count */
			if (scaled::hash(aiInputs) * 100 < -iCivBias)
			{
				IFLOG logBBAI("Negative bias randomly doubled");
				iCivBias *= 2;
			}
		}
		iCivBias += iBiasFromLeaderCount;
		CvTruLeaderInfo const* pTruLeader = m_truLeaders.get(eLeader);
		int const iLeaderBias = (pTruLeader == NULL ? 0 :
				pTruLeader->get(CvTruLeaderInfo::Bias));
		iFitness *= 100 + iCivBias * (iFitness < 0 ? -1 : 1);
		iFitness /= 100;
		iFitness *= 100 + iLeaderBias * (iFitness < 0 ? -1 : 1);
		iFitness /= 100;
		iFitness += iCivBias + iLeaderBias;
		IFLOG if(iCivBias!=0) logBBAI("Bias for or against %S: %d percent (%d from leader count)",
				GC.getInfo(eCiv).getShortDescription(), iCivBias, iBiasFromLeaderCount);
		IFLOG if(iLeaderBias!=0) logBBAI("Bias for or against %S: %d percent",
				GC.getInfo(eLeader).getDescription(), iLeaderBias);
	}
	IFLOG logBBAI("Bottom line: %d fitness\n\n", iFitness);
	return iFitness;
}


void TrueStarts::calculatePlotWeights(CvPlayer const& kPlayer)
{
	CvPlot const& kStart = *kPlayer.getStartingPlot();
	auto_ptr<PlotCircleIter> pSurroundings = getSurroundings(kPlayer);
	for (PlotCircleIter& itPlot = *pSurroundings; itPlot.hasNext(); ++itPlot)
	{
		scaled const rDistWeight = distWeight(kStart, *itPlot, itPlot.radius());
		scaled rWeight = rDistWeight;
		// Reduce based on rival weights
		for (TruPlayerIter itOther = truPlayers(); itOther.hasNext(); ++itOther)
		{
			if (itOther->getID() != kPlayer.getID())
			{
				scaled rOtherDistWeight = distWeight(
						*itOther->getStartingPlot(), *itPlot, itPlot.radius());
				rWeight *= 1 - scaled::max(0, rOtherDistWeight - rDistWeight);
			}
		}
		/*	Initially, I was going to call CvMap::xDistance, yDistance here and
			adjust the weights to the civ's shape preference. However, then the
			weights should also be recomputed (for every player-civ pair) each
			time a civ is placed b/c the weights of neighboring civs interfere
			with each other. This is computationally expensive enough to introduce
			a delay of several seconds on maps with 18 civs and may make
			super-Huge maps a very slow affair. (So I'll be using a cruder mechanism
			for shape preferences instead.) Framework for civ-specific weights
			deleted on 2 Jan 2021. */
		m_plotWeights.set(kPlayer.getID(), itPlot->plotNum(), rWeight);
	}
}


auto_ptr<PlotCircleIter> TrueStarts::getSurroundings(CvPlayer const& kPlayer) const
{
	return auto_ptr<PlotCircleIter>(
			new PlotCircleIter(*kPlayer.getStartingPlot(),
			m_radii.get(kPlayer.getID())));
}


class PrecipitationRegion
{
	scaled m_rWeight;
	scaled m_rPrecipitation;
	CvPlot const* m_pCenter; // (Reference would prevent copying)
public:
	PrecipitationRegion(CvPlot const& kCenter, scaled rWeight, scaled rPrecipitation)
	:	m_pCenter(&kCenter), m_rWeight(rWeight), m_rPrecipitation(rPrecipitation)
	{ FAssert(rWeight < 20); } // Make sure the params don't get mixed up
	scaled getWeight() const { return m_rWeight; }
	scaled getPrecipitation() const { return m_rPrecipitation; }
	CvPlot const& getCenter() const { return *m_pCenter; }
};


int TrueStarts::calcClimateFitness(CvPlayer const& kPlayer, int iTargetPrecipitation,
	int iTargetVariation, bool bLog) const
{
	CvPlot const& kStart = *kPlayer.getStartingPlot();
	/*	Computing a weighted mean over the entire surroundings of kStart
		doesn't work well (I've tried); it's usually a muddle. Need to look at
		subregions with more distinct characteristics. I think that's how
		players perceive the map, e.g. "there's a major desert." */
	std::vector<PrecipitationRegion> aRegions;
	int const iDistBetweenRegions = (GC.getMap().getWorldSize() < 2 ? 3 : 4);
	for (PlotCircleIter itCenter(kStart, iDistBetweenRegions);
		itCenter.hasNext(); ++itCenter)
	{
		bool const bStart = (&*itCenter == &kStart);
		// Center the regions on a circle (i.e. on its rim), and one on kStart.
		if (itCenter.currPlotDist() != iDistBetweenRegions && !bStart)
			continue;
		{
			/*	Only consider the 8 plots on a straight orthogonal or
				diagonal line from kStart */
			int iDX = abs(itCenter->getX() - kStart.getX());
			int iDY = abs(itCenter->getY() - kStart.getY());
			if (iDX != 0 && iDY != 0 && iDX != iDY)
				continue;
		}
		std::vector<std::pair<scaled,scaled> > arrRegionData;
		for (CityPlotIter itPlot(*itCenter); itPlot.hasNext(); ++itPlot)
		{
			int iPrecipitation = precipitation(*itPlot, plotDistance(&*itPlot, &kStart));
			if (iPrecipitation < 0)
				continue;
			scaled rWeight = m_plotWeights.get(kPlayer.getID(), itPlot->plotNum());
			// Extra weight for the most prominent characteristics
			if (itPlot->getFeatureType() == m_eWarmForest)
				rWeight *= fixp(5/3.);
			/*	Desert needs a very high weight b/c all-desert regions
				don't really exist on random maps; need to treat regions
				dominated by desert as having very low overall precipitation
				or else the Fertile Crescent civs never get used. */
			else if (itPlot->getTerrainType() == m_eDesert)
				rWeight *= 10;
			arrRegionData.push_back(std::make_pair(iPrecipitation, rWeight));
		}
		// Discard some outliers
		std::sort(arrRegionData.begin(), arrRegionData.end());
		{
			int const iValidThresh = (NUM_CITY_PLOTS * 5) / 7;
			int const iMaxOutliers = 2; // at each end of the list
			int const iOutliers = std::min(iMaxOutliers,
					(((int)arrRegionData.size()) - iValidThresh) / 2);
			/*	(This would be easier to read with a std::list and pop_front,
				but sorting lists is expensive. It's still kind of expensive
				with a vector. The region data calculation is -currently-
				the slowest part of the True Starts code. List code replaced
				on 2 Jan 2021.) */
			if (iOutliers > 0)
			{
				for (size_t i = 0; i + iOutliers < arrRegionData.size(); i++)
					arrRegionData[i] = arrRegionData[i + iOutliers];
				for (int i = 0; i < 2 * iOutliers; i++)
					arrRegionData.pop_back();
			}
		}
		int const iValidPlots = (int)arrRegionData.size();
		scaled rRegionWeight;
		scaled rRegionPrecipitation;
		for (size_t i = 0; i < arrRegionData.size(); i++)
		{
			rRegionPrecipitation += arrRegionData[i].first;
			rRegionWeight += arrRegionData[i].second;
		}
		if (iValidPlots * 3 < (bStart ? 0 : NUM_CITY_PLOTS) || rRegionWeight <= 0)
		{
			if (bStart)
			{
				FErrorMsg("At least kStart has to be valid");
				return 0;
			}
			continue;
		}
		rRegionPrecipitation /= iValidPlots;
		rRegionWeight /= iValidPlots;
		aRegions.push_back(PrecipitationRegion(
				*itCenter, rRegionWeight, rRegionPrecipitation));
	}
	if (aRegions.empty())
	{
		FErrorMsg("At least the start region should be valid");
		return 0;
	}
	IFLOG
	{
		logBBAI("Climate regions ...");
		for (size_t i = 0; i < aRegions.size(); i++)
		{
			logBBAI("(%d,%d): %d mm, weight %d percent", aRegions[i].getCenter().getX(), aRegions[i].getCenter().getY(),
					aRegions[i].getPrecipitation().round(), aRegions[i].getWeight().getPercent());
		}
	}
	std::vector<scaled> arPrecipitationFactors;
	// The region around kStart is always important
	arPrecipitationFactors.push_back(aRegions[0].getPrecipitation());
	IFLOG logBBAI("Precipitation in region around start: %d", aRegions[0].getPrecipitation().round());
	{
		// Let's also consider a typical region
		std::vector<std::pair<scaled,scaled> > arrRegionData;
		for (size_t i = 1; i < aRegions.size(); i++) // (skip region around kStart)
		{
			arrRegionData.push_back(std::make_pair(
					aRegions[i].getPrecipitation(), aRegions[i].getWeight()));
		}
		if (!arrRegionData.empty())
		{
			scaled rMedianPrecipitation = stats::weightedMedian(arrRegionData);
			arPrecipitationFactors.push_back(rMedianPrecipitation);
			IFLOG logBBAI("Precipitation of median region: %d", rMedianPrecipitation.round());
		}
	}
	/*	Lastly, see if we can find a region that reinforces the impression
		of the region around kStart. */
	{
		scaled rMinError = scaled::MAX;
		int iBestIndex = -1;
		for (size_t i = 1; i < aRegions.size(); i++)
		{
			scaled rError = (1 / aRegions[i].getWeight()) * // Magnify error if weight small
					(aRegions[i].getPrecipitation() - aRegions[0].getPrecipitation()).
					abs();
			if (rError < rMinError)
			{
				rMinError = rError;
				iBestIndex = i;
			}
		}
		if (iBestIndex > 0)
		{
			scaled rSimilarPrecipitation = aRegions[iBestIndex].getPrecipitation();
			arPrecipitationFactors.push_back(rSimilarPrecipitation);
			IFLOG logBBAI("Precipitation in region most akin to start: %d", rSimilarPrecipitation.round());
		}
	}
	scaled rPrecipitation;
	for (size_t i = 0; i < arPrecipitationFactors.size(); i++)
		rPrecipitation += arPrecipitationFactors[i];
	if (!arPrecipitationFactors.empty())
		rPrecipitation /= arPrecipitationFactors.size();
	{	// Not as varied as the real world. Exaggerate any unusual values.
		int const iTypicalPrecipitation = 600;
		scaled rAdjust = std::min((rPrecipitation - iTypicalPrecipitation).abs(),
				rPrecipitation).pow(fixp(0.7));
		if (rPrecipitation < iTypicalPrecipitation)
			rAdjust *= -1;
		IFLOG logBBAI("Adjusting overall precipitation by %d, to exaggerate.", rAdjust.round());
		rPrecipitation += rAdjust;
	}
	IFLOG logBBAI("Overall precipitation: %d", rPrecipitation.round());
	/*	Very unlikely to match extremely low target precipitation (at least on a
		random map, but even the Earth scenarios aren't that dry), shouldn't
		penalize such a mismatch much. */
	scaled const rVeryLowPrecipThresh = scaled::min(135, rPrecipitation);
	scaled rFitness;
	if (iTargetPrecipitation >= 0)
	{
		rFitness -= (rPrecipitation - scaled::max(iTargetPrecipitation,
				rVeryLowPrecipThresh)).abs() / 2 +
				scaled::max(0, rVeryLowPrecipThresh - iTargetPrecipitation) / 4;
		IFLOG logBBAI("%d fitness penalty from target precipitation of %d",
				-rFitness.round(), iTargetPrecipitation);
		if (aRegions.size() > 1)
		{
			int iCloseMatches = 0;
			int iPossibleMatches = 0;
			for (size_t i = (aRegions.size() <= 2 ? 0 : 1); i < aRegions.size(); i++)
			{
				iPossibleMatches++;
				if ((aRegions[i].getPrecipitation()
					- scaled::max(iTargetPrecipitation, rVeryLowPrecipThresh)).abs() * 5 <
					scaled::max(aRegions[i].getPrecipitation(), iTargetPrecipitation))
				{
					iCloseMatches++;
				}
			}
			scaled rFromCloseMatches = 200 * std::min(scaled(iPossibleMatches, 10),
					scaled(scaled(iCloseMatches, iPossibleMatches).sqrt()
					- fixp(1/3.).sqrt()));
			rFitness += rFromCloseMatches;
			IFLOG logBBAI("Adding %d for %d close matches among %d regions",
					rFromCloseMatches.round(), iCloseMatches, iPossibleMatches);
		}
	}
	else IFLOG logBBAI("No precipitation data available");
	if (iTargetVariation >= 0)
	{
		scaled rTotalError;
		int iSamples = 0;
		for (size_t i = 1; i < arPrecipitationFactors.size(); i++)
		{ 
			rTotalError += (arPrecipitationFactors[i]
					- arPrecipitationFactors[0]).abs();
			iSamples++;
		}
		if (arPrecipitationFactors.size() > 1)
		{
			// Don't want one region full of jungle to dominate the calculation
			scaled const rPrecipThresh = 1350;
			scaled const rMedian = std::min(arPrecipitationFactors[1], rPrecipThresh);
			for (size_t i = 1; i < aRegions.size(); i++)
			{
				scaled const rRegionPrecip = scaled::min(rPrecipThresh,
						aRegions[i].getPrecipitation());
				/*	Square error to emphasize outliers, double to somewhat match the
					scale of the absolute errors counted above. */
				rTotalError += 2 * SQR((rRegionPrecip - rMedian).abs()) /
						std::max(rMedian + rVeryLowPrecipThresh, scaled::epsilon());
				iSamples++;
			}
		}
		scaled rMeanError = rTotalError / iSamples;
		scaled rVariationScore = rMeanError / 345;
		rVariationScore.decreaseTo(1);
		scaled rFromVariation = (iTargetVariation - rVariationScore.getPercent())
				* fixp(1.5);
		if (rFromVariation < 0) // Too much variation is more problematic
			rFromVariation *= fixp(1.78);
		rFromVariation = -rFromVariation.abs();
		rFitness += rFromVariation;
		IFLOG logBBAI("From mismatch in climate variation: %d (score %d percent, target %d percent)",
				rFromVariation.round(), rVariationScore.getPercent(), iTargetVariation);
	}
	else IFLOG logBBAI("No climate variation data available");
	return rFitness.round();
}

// Millimeters annual, -1 if undetermined.
int TrueStarts::precipitation(CvPlot const& kPlot, int iDistStart) const
{
	if (kPlot.isWater() || kPlot.isPeak())
		return -1; // Only consider flat land and hills
	FeatureTypes const eFeature = kPlot.getFeatureType();
	TerrainTypes const eTerrain = kPlot.getTerrainType();
	bool bWarmForest = (eFeature == m_eWarmForest);
	/*	Normalization removes Jungle, obscuring high-precipitation starts.
		Compensate for that (or we'll never have starts wet enough for the Maya). */
	if (!bWarmForest &&
		iDistStart <= CITY_PLOTS_RADIUS + 2 && // cf. CvGame::normalizeRemoveBadFeatures
		(eTerrain == m_eWoodland || eTerrain == m_eSteppe))
	{
		FOR_EACH_ADJ_PLOT(kPlot)
		{
			if (pAdj->getFeatureType() == m_eWarmForest)
			{
				bWarmForest = true;
				break;
			}
		}
	}
	if (bWarmForest)
	{
		return (!m_bMapHasLatitudes ? 2000 :
				3000 - 70 * std::min(25, kPlot.getLatitude()));
	}
	if (eTerrain == m_eWoodland)
	{
		if (eFeature == m_eCoolForest)
		{	/*	This calculation is tailored toward Japan.
				Very wet temperate forest there. */
			int iExtra = 0;
			FOR_EACH_ADJ_PLOT(kPlot)
			{
				if (pAdj->isWater())
					iExtra += 75;
				if (pAdj->getTerrainType() == kPlot.getTerrainType() &&
					pAdj->getFeatureType() == kPlot.getFeatureType())
				{
					iExtra += 95;
				}
			}
			return 825 + std::min(iExtra, 550);
		}
		return 750;
	}
	if (eTerrain != m_eDesert && eTerrain != m_ePolarDesert)
	{
		/*	Extra precipitation for oceanic plots;
			to get the Vikings placed more often. */
		int iExtra = 0;
		int iWater = 0;
		FOR_EACH_ADJ_PLOT(kPlot)
		{
			if (pAdj->isWater())
			{
				iWater++;
				if (iWater >= 4)
				{
					iExtra += 110;
					break;
				}
			}
		}
		if (iWater > 0 && kPlot.isHills()) // "fjords"
			iExtra += 75;
		if (eFeature == m_eCoolForest)
			return 500 + iExtra; // Taiga, forest steppe
		// Treat plots likely affected by normalization as semi-arid
		if (eTerrain == m_eSteppe && iExtra <= 0 &&
			iDistStart <= CITY_PLOTS_RADIUS + 1) // cf. CvGame::normalizeRemoveBadTerrain
		{
			int iAdjDesert = 0;
			int iAdjSteppe = 0;
			FOR_EACH_ADJ_PLOT(kPlot)
			{
				if (pAdj->getTerrainType() == m_eDesert)
					iAdjDesert++;
				else if (pAdj->getTerrainType() == m_eSteppe &&
					pAdj->getFeatureType() == NO_FEATURE)
				{
					iAdjSteppe++;
				}
				if (iAdjDesert > 0 && iAdjDesert * 5 + iAdjSteppe * 2 >= 9)
					return 210;
			}
		}
		return 350 + iExtra / 2; // Tundra, steppe
	}
	// I interpret this as the northernmost taiga
	if (eTerrain == m_ePolarDesert && m_eCoolForest)
		return 250;
	// (Polar) desert ...
	int iExtra = 0;
	FOR_EACH_ADJ_PLOT(kPlot)
	{
		if (pAdj->getTerrainType() == kPlot.getTerrainType() &&
			pAdj->getFeatureType() == kPlot.getFeatureType())
		{
			iExtra -= 30;
		}
	}
	return std::max(1, 200 + iExtra);
}

/*	+1 means the best possible fit, -1 the worst.
	All nonnegative values are acceptable, negative values might be worth
	a swap (but not necessarily; that's for calcBonusSwapUtil to decide). */
scaled TrueStarts::calcBonusFitness(CvPlot const& kPlot,
	EagerEnumMap<PlayerTypes,scaled> const& kPlayerWeights,
	BonusTypes eBonus, bool bLog) const
{
	if (eBonus == NO_BONUS)
		eBonus = kPlot.getBonusType();
	scaled rMinPlayerFitness;
	scaled rTotal;
	for (TruPlayerIter itPlayer = truPlayers(); itPlayer.hasNext(); ++itPlayer)
	{
		scaled rWeight = kPlayerWeights.get(itPlayer->getID());
		if (rWeight <= 0) // Save time, don't pollute log.
			continue;
		if (itPlayer->isHuman() && m_bPrioritizeHumans)
			rWeight *= fixp(4/3.);
		IFLOG logBBAI("Fitness weight of %S for %S (%d,%d): %d percent",
				itPlayer->getName(), GC.getInfo(eBonus).getDescription(),
				kPlot.getX(), kPlot.getY(), rWeight.getPercent());
		scaled rPlayerFitness = rWeight *
				calcBonusFitness(kPlot, *itPlayer, eBonus, bLog);
		rTotal += rPlayerFitness;
		rMinPlayerFitness = std::min(rPlayerFitness, rMinPlayerFitness);
	}
	/*	(Adjustment to the player count shouldn't be necessary:
		Larger maps shouldn't have more overlap between starting surroundings
		than smaller maps, and, if they do, more swapping will be appropriate.
		Crowdedness is already taken into account by the player weights. */
	return (rTotal + rMinPlayerFitness) / 2;
}

/*	Same scale as above if we assume that eBonus is right next to kPlayer's
	starting plot. (Distances are the caller's job to evaluate.)
	However, the +1 is so far only a theoretical upper limit - I don't
	want the encouraged resources to have as strong an effect as the
	discouraged ones. */
scaled TrueStarts::calcBonusFitness(CvPlot const& kPlot, CvPlayer const& kPlayer,
	BonusTypes eBonus, bool bLog) const
{
	scaled const rEncouragement =
			(isBonusEncouraged(kPlot, kPlayer.getCivilizationType(), eBonus) ? fixp(0.4) :
			(isBonusDiscouraged(kPlot, kPlayer.getCivilizationType(), eBonus) ? -1 : 0));
	IFLOG if(rEncouragement!=0) logBBAI("Encouragement value of %S (%d,%d) near %S: %d percent",
			GC.getInfo(eBonus).getDescription(), kPlot.getX(), kPlot.getY(),
			kPlayer.getName(), rEncouragement.getPercent());
	return rEncouragement;
}

namespace
{
	EraTypes getTechRevealEra(CvBonusInfo const& kBonus)
	{
		return (kBonus.getTechReveal() == NO_TECH ? NO_ERA :
				GC.getInfo(kBonus.getTechReveal()).getEra());
	}

	int getClassUniqueRange(CvBonusInfo const& kBonus)
	{
		return (kBonus.getBonusClassType() == NO_BONUSCLASS ? 0 :
				GC.getInfo(kBonus.getBonusClassType()).getUniqueRange());
	}

	/*	Counts the bonus resources within a given range, but only counts
		adjacent bonus resources fully, others weighted by distance. */
	scaled sameBonusInRangeScore(CvPlot const& kPlot, CvBonusInfo const& kBonus,
		int iMaxRange, bool bBonusClass = false)
	{
		scaled rScore;
		for (SquareIter itPlot(kPlot, iMaxRange, false); itPlot.hasNext(); ++itPlot)
		{
			if (itPlot->getBonusType() == NO_BONUS)
				continue;
			CvBonusInfo const& kLoopBonus = GC.getInfo(itPlot->getBonusType());
			if (bBonusClass ?
				(kLoopBonus.getBonusClassType() == kBonus.getBonusClassType()) :
				(&kLoopBonus == &kBonus))
			{
				rScore += 1 - scaled(
						2 * std::max(0, itPlot.currPlotDist() - 1), 3 * iMaxRange).
						pow(fixp(1.5));
			}
		}
		return rScore;
	}
}

/*	Utility greater than 0 means that the swap is worth making all in all,
	i.e. taking into account not just fitness values but also the overall
	disturbance to the map, balance, increase in predictability ...
	The specific positive value says how good the swap is (all in all).
	0 or less means that the swap should not be made, won't generally say
	_how_ bad it is. */
scaled TrueStarts::calcBonusSwapUtil(
	CvPlot const& kFirstPlot, CvPlot const& kSecondPlot,
	scaled rFirstFitness, scaled rSecondFitness, bool bLog) const
{
	CvPlot const* pDestOfSecond = findValidBonusSwapDest(
			/*	Doesn't actually change the plot - but may return it as non-const.
				CvMap only contains non-const CvPlot instances, so such casts are safe. */
			const_cast<CvPlot&>(kFirstPlot), kSecondPlot);
	if (pDestOfSecond == NULL)
	{
		FAssert(!bLog); // I intend to log only valid swaps
		return 0;
	}
	CvPlot const* pDestOfFirst = findValidBonusSwapDest(
			const_cast<CvPlot&>(kSecondPlot), kFirstPlot);
	if (pDestOfFirst == NULL)
	{
		FAssert(!bLog);
		return 0;
	}
	EagerEnumMap<PlayerTypes,scaled> aerPlayerWeights;
	setPlayerWeightsPerPlot(pDestOfSecond->plotNum(), aerPlayerWeights,
			m_bPrioritizeHumans ? 2 : 1);
	scaled rFirstFitnessAfterSwap = calcBonusFitness(
			*pDestOfSecond, aerPlayerWeights, kSecondPlot.getBonusType(), bLog);
	setPlayerWeightsPerPlot(pDestOfFirst->plotNum(), aerPlayerWeights);
	scaled rSecondFitnessAfterSwap = calcBonusFitness(
			*pDestOfFirst, aerPlayerWeights, kFirstPlot.getBonusType(), bLog);
	scaled rUtil = rFirstFitnessAfterSwap + rSecondFitnessAfterSwap
			- rFirstFitness - rSecondFitness;
	{
		scaled rDisturbance = fixp(1/4.) + // Base penalty - ideally don't swap anything
				calcBonusSwapDisturbance(
				*pDestOfFirst, kSecondPlot, kFirstPlot.getBonusType(), bLog) +
				calcBonusSwapDisturbance(
				*pDestOfSecond, kFirstPlot, kSecondPlot.getBonusType(), bLog);
		IFLOG logBBAI("Subtracting %d/100 utility for disturbance of original map",
				rDisturbance.getPercent());
		rUtil -= rDisturbance;
	}
	CvBonusInfo const& kFirstBonus = GC.getInfo(kFirstPlot.getBonusType());
	CvBonusInfo const& kSecondBonus = GC.getInfo(kSecondPlot.getBonusType());
	{	// Try to preserve locality of bonus resource types
		scaled rDistPenalty;
		if (!sameArea(*pDestOfFirst, *pDestOfSecond) &&
			// Don't care if resources bleed onto small continents
			2 * pDestOfFirst->getArea().getNumTiles() > 3 * NUM_CITY_PLOTS &&
			2 * pDestOfSecond->getArea().getNumTiles() > 3 * NUM_CITY_PLOTS)
		{
			if (pDestOfFirst->getArea().getNumBonuses(kFirstPlot.getBonusType()) <= 0 &&
				kFirstBonus.isOneArea())
			{
				rDistPenalty += fixp(0.25);
			}
			if (pDestOfSecond->getArea().getNumBonuses(kSecondPlot.getBonusType()) <= 0 &&
				kSecondBonus.isOneArea())
			{
				rDistPenalty += fixp(0.25);
			}
		}
		scaled rSwapDist(plotDistance(pDestOfFirst, pDestOfSecond),
				GC.getMap().maxPlotDistance());
		if (rSwapDist > fixp(0.2))
			rDistPenalty += fixp(0.05);
		IFLOG if(rDistPenalty!=0) logBBAI("Swap distance penalty: %d/100", rDistPenalty.getPercent());
		rUtil -= rDistPenalty;
	}
	{
		scaled rSameInRangeScore =
				sameBonusInRangeScore(
				*pDestOfFirst, kFirstBonus, kFirstBonus.getUniqueRange()) +
				sameBonusInRangeScore(
				*pDestOfSecond, kSecondBonus, kSecondBonus.getUniqueRange()) +
				sameBonusInRangeScore(
				*pDestOfFirst, kFirstBonus, getClassUniqueRange(kFirstBonus), true) +
				sameBonusInRangeScore(
				*pDestOfSecond, kSecondBonus, getClassUniqueRange(kSecondBonus), true);
		rSameInRangeScore *= fixp(0.75); // weight factor
		IFLOG if(rSameInRangeScore!=0) logBBAI("Penalty for same or similar resources nearby: %d/100",
				rSameInRangeScore.getPercent());
		rUtil -= rSameInRangeScore;
	}
	return rUtil;
}


scaled TrueStarts::calcBonusSwapDisturbance(CvPlot const& kDest,
	CvPlot const& kOriginalDest, BonusTypes eNewBonus, bool bLog) const
{
	BonusTypes eOldBonus = kOriginalDest.getBonusType();
	scaled rDisturbance;
	if (&kDest != &kOriginalDest)
		rDisturbance += fixp(0.1);
	if (kDest.isFeature() && // just to save time
		!canHaveBonus(kDest, eOldBonus))
	{
		rDisturbance += fixp(0.06);
	}
	IFLOG if(rDisturbance!=0)logBBAI("Disturbance from non-resource changes at (%d,%d): %d/100",
			kDest.getX(), kDest.getY(), rDisturbance.getPercent());
	CvBonusInfo const& kOldBonus = GC.getInfo(eOldBonus);
	CvBonusInfo const& kNewBonus = GC.getInfo(eNewBonus);
	/*	Note that the penalties for dissimilar resources get counted twice,
		as this function gets called for both plots that are being swapped. */
	{
		EraTypes const eOldRevealEra = getTechRevealEra(kOldBonus);
		EraTypes const eNewRevealEra = getTechRevealEra(kNewBonus);
		EraTypes const eStartEra = GC.getGame().getStartEra();
		scaled rFromReveal = scaled(abs(std::max(eStartEra, eOldRevealEra)
				- std::max(eStartEra, eNewRevealEra))).sqrt() / 9;
		IFLOG if(rFromReveal!=0) logBBAI(
				"Disturbance from swapping revealed with unrevealed resource (%S for %S): %d/100",
				kNewBonus.getDescription(), kOldBonus.getDescription(), rFromReveal.getPercent());
		rDisturbance += rFromReveal;
	}
	if (kOldBonus.isNormalize() != kNewBonus.isNormalize())
	{
		scaled rFromNormalize = fixp(0.04);
		IFLOG logBBAI(
				"Disturbance from swapping resource suitable for normalization with one unsuitable (%S for %S): %d/100",
				kNewBonus.getDescription(), kOldBonus.getDescription(), rFromNormalize.getPercent());
		rDisturbance += rFromNormalize;
	}
	if (rDisturbance > 0)
	{	
		// Disturbances near starting plots are worse
		/*	(Would be better to include players with fixed civs here, but I don't
			think I want to compute weights for those players just for this purpose.) */
		for (TruPlayerIter itPlayer = truPlayers(); itPlayer.hasNext(); ++itPlayer)
		{
			rDisturbance *= 1 + SQR(m_plotWeights.get(itPlayer->getID(),
					kDest.plotNum()));
		}
	}
	return rDisturbance;
}
