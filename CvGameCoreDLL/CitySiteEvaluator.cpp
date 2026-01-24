#include "CvGameCoreDLL.h"
#include "CitySiteEvaluator.h"
#include "CoreAI.h"
#include "CvCityAI.h"
#include "CvCivilization.h"
#include "PlotRange.h"
#include "CvArea.h"
#include "CvInfo_City.h"
#include "CvInfo_Terrain.h"
#include "CvInfo_GameOption.h"
#include "CvInfo_Civics.h"
#include "BBAILog.h"

// advc: New file; see comment in the header.

static int const iDEFAULT_BARB_DISCOURAGED_RANGE = 8; // advc.303

#define IFLOG if (gFoundLogLevel > 0 && AIFoundValue::isLoggingEnabled()) // advc.031c

// Body cut from K-Mod's CvPlayerAI::CvFoundSettings::CvFoundSettings
CitySiteEvaluator::CitySiteEvaluator(CvPlayerAI const& kPlayer, int iMinRivalRange,
	bool bStartingLoc, /* advc.031e: */ bool bNormalize)
:	m_kPlayer(kPlayer), m_iMinRivalRange(iMinRivalRange), m_bStartingLoc(bStartingLoc),
	m_bNormalize(bNormalize),
	m_bScenario(false), m_bAmbitious(false), m_bExtraYieldThresh(false),
	m_bExtraYieldNaturalThresh(false), // advc.908a
	m_bDefensive(false), m_bSeafaring(false), m_bExpansive(false),
	m_bDebug(false), // advc.007
	m_bAdvancedStart(false), /* advc.027: */ m_bIgnoreStartingSurroundings(false),
	m_iBarbDiscouragedRange(iDEFAULT_BARB_DISCOURAGED_RANGE) // advc.303
{
	m_bScenario = (bStartingLoc ? GC.getInitCore().getWBMapScript() : // advc.031f
			GC.getGame().isScenario()); // advc
	m_bAdvancedStart = (kPlayer.getAdvancedStartPoints() > 0);
	m_bEasyCulture = (kPlayer.getNumCities() <= 0 || // advc.108: from MNAI (was =bStartingLoc)
			m_bAdvancedStart); // advc.031
	m_bAllSeeing = (bStartingLoc || bNormalize || kPlayer.isBarbarian());
	// advc.031e: No longer use StartingLoc logic for normalization
	FAssert(!bNormalize || !bStartingLoc);

	CvLeaderHeadInfo const* pPersonality = NULL;
	CvCivilization const& kCiv = kPlayer.getCivilization();
	if (!m_bStartingLoc && !m_bNormalize)
	{
		// advc.001: Make sure that personality isn't used for human or StartingLoc
		if (!kPlayer.isHuman() || m_bDebug)
			pPersonality = &GC.getInfo(kPlayer.getPersonalityType());
		bool bEasyCultureFromTrait = false;
		m_bEasyCulture = kPlayer.AI_isEasyCulture(&bEasyCultureFromTrait);
		if (bEasyCultureFromTrait && pPersonality != NULL &&
			pPersonality->getBasePeaceWeight() <= 5)
		{
			m_bAmbitious = true;
		}
		FOR_EACH_ENUM(Trait)
		{
			if (!kPlayer.hasTrait(eLoopTrait))
				continue;

			CvTraitInfo const& kLoopTrait = GC.getInfo(eLoopTrait);
			if (kLoopTrait.getExtraYieldThreshold(YIELD_COMMERCE) > 0)
				m_bExtraYieldThresh = true;
			// <advc.908a>
			if (kLoopTrait.getExtraYieldNaturalThreshold(YIELD_COMMERCE) > 0)
				m_bExtraYieldNaturalThresh = true; // </advc.908a>
			if (kLoopTrait.isAnyFreePromotion()) // advc.003t
			{
				FOR_EACH_ENUM(Promotion)
				{
					if (kLoopTrait.isFreePromotion(eLoopPromotion))
					{
						// aggressive, protective... it doesn't really matter to me.
						if (pPersonality != NULL && pPersonality->getBasePeaceWeight() >= 5)
							m_bDefensive = true;
					}
				}
			}
			if (pPersonality != NULL && pPersonality->getMaxWarRand() <= 150) // advc.opt: moved up
			{
				for (int i = 0; i < kCiv.getNumUnits(); i++)
				{
					UnitTypes eFoundUnit = kCiv.unitAt(i);
					if (GC.getInfo(eFoundUnit).isFound() &&
						// advc.031: was > 0
						GC.getInfo(eFoundUnit).getProductionTraits(eLoopTrait) > 20 &&
						kPlayer.canTrain(eFoundUnit))
					{
						m_bAmbitious = true;
					}
				}
			}
		}
		// seafaring test for unique unit and unique building
		if (kPlayer.getCoastalTradeRoutes() > 0)
			m_bSeafaring = true;
		if (!m_bSeafaring)
		{
			for (int i = 0; i < kCiv.getNumUniqueUnits(); i++) // advc.003w
			{
				UnitTypes eUniqueUnit = kCiv.uniqueUnitAt(i);
				if (GC.getInfo(eUniqueUnit).getDomainType() == DOMAIN_SEA)
				{
					m_bSeafaring = true;
					break;
				}
			}
		}
		if (!m_bSeafaring)
		{
			for (int i = 0; i < kCiv.getNumUniqueBuildings(); i++) // advc.003w
			{
				BuildingTypes eUniqueBuilding = kCiv.uniqueBuildingAt(i);
				if (GC.getInfo(eUniqueBuilding).isWater())
				{
					m_bSeafaring = true;
					break;
				}
			}
		}
	}

	if (pPersonality != NULL && kPlayer.AI_getFlavorValue(FLAVOR_GROWTH) > 0)
		m_bExpansive = true;

	m_iClaimThreshold = 100; // will be converted into culture units
	if (!bStartingLoc && !bNormalize)
	{
		int iCitiesTarget = std::max(1,
				GC.getInfo(GC.getMap().getWorldSize()).getTargetNumCities());
		m_iClaimThreshold = 100 +
				(100 * kPlayer.getCurrentEra()) / std::max(1, GC.getNumEraInfos() - 1);
		m_iClaimThreshold += 80 * std::max(0,
				iCitiesTarget - kPlayer.getNumCities()) / iCitiesTarget;

		m_iClaimThreshold *= (!m_bEasyCulture ? 100 :
				(kPlayer.getCurrentEra() < 2 ? 200 : 150));
		m_iClaimThreshold *= (m_bAmbitious ? 150 : 100);
		m_iClaimThreshold /= 10000;
	}
	m_iClaimThreshold *= 2 * GC.getGame().getCultureThreshold((CultureLevelTypes)
			std::min(2, GC.getNumCultureLevelInfos() - 1));
	// note: plot culture is roughly 10x city culture (cf. CvCity::doPlotCultureTimes100)
	FAssert(m_iClaimThreshold > 0);

	if (m_bAdvancedStart)
	{
		FAssert(GC.getGame().isOption(GAMEOPTION_ADVANCED_START));
		if (m_bStartingLoc || m_bNormalize)
			m_bAdvancedStart = false;
	}
	IFLOG logSettings();
}


short CitySiteEvaluator::evaluate(CvPlot const& kPlot) const
{
	AIFoundValue foundVal(kPlot, *this);
	return foundVal.get();
}


short CitySiteEvaluator::evaluate(int iX, int iY) const
{
	CvPlot const* pPlot = GC.getMap().plot(iX, iY);
	if (pPlot == NULL)
		return 0;
	return evaluate(*pPlot);
}

// advc.300:
void CitySiteEvaluator::discourageBarbarians(int iRange)
{
	m_iBarbDiscouragedRange = iRange;
}

// <advc.027>
void CitySiteEvaluator::setIgnoreStartingSurroundings(bool b)
{
	m_bIgnoreStartingSurroundings = b;
}


scaled CitySiteEvaluator::evaluateWorkablePlot(CvPlot const& kPlot) const
{
	// Should only be used for StartingPositionIteration
	FAssert(isNormalizing() && !isDebug());
	/*	The evaluation is going to be largely independent from any city tile,
		but it could matter whether it's coastal and on the same landmass.
		And for the evaluation of water tiles, I want to be able to guess
		based on the potential city tile whether it's arctic water. */
	CvPlot const* pBestCityPlot = NULL;
	int iBestScore = 0;
	int const iBestPossibleScore = (kPlot.isWater() ? 4 : 5);
	for (CityPlotIter it(kPlot, false); it.hasNext(); ++it)
	{
		if (!m_kPlayer.canFound(*it))
			continue;
		int iScore = 1;
		if (kPlot.isWater())
		{
			if (it->isCoastalLand(-1))
				iScore += 2;
			if (GC.getInfo(it->getTerrainType()).getYield(YIELD_FOOD) > 0)
				iScore++;
		}
		else
		{
			if (kPlot.sameArea(*it))
				iScore += 4;
		}
		if (iScore > iBestScore)
		{
			pBestCityPlot = &*it;
			iBestScore = iScore;
			if (iScore >= iBestPossibleScore)
				break;
		}
	}
	if (pBestCityPlot == NULL) // kPlot not workable
		return 0;
	AIFoundValue foundVal(*pBestCityPlot, *this);
	CvGame& kGame = GC.getGame();
	CvGame::StartingPlotNormalizationLevel eOldLevel = kGame.
			getStartingPlotNormalizationLevel();
	// Make sure that resources get revealed
	kGame.setStartingPlotNormalizationLevel(CvGame::NORMALIZE_HIGH);
	scaled r = foundVal.evaluateWorkablePlot(kPlot);
	kGame.setStartingPlotNormalizationLevel(eOldLevel);
	return r;
} // </advc.027>

// advc.007:
void CitySiteEvaluator::setDebug(bool b)
{
	m_bDebug = b;
}

// <advc.031c>
short CitySiteEvaluator::evaluateWithLogging(CvPlot const& kPlot) const
{
	AIFoundValue::setLoggingEnabled(true);
	short r = evaluate(kPlot);
	AIFoundValue::setLoggingEnabled(false);
	return r;
}


void CitySiteEvaluator::log(CvPlot const& kPlot)
{
	/*  Important to ignore other city sites. Because, when CvPlayerAI::
		AI_updateCitySites computes the found value of the best site,
		none of the other sites are chosen yet. Here, all sites are chosen. */
	setDebug(true);
	if (isStartingLoc())
		logBBAI("\n\nStarting location found at (%d,%d)", kPlot.getX(), kPlot.getY());
	else if (isNormalizing())
		logBBAI("\n\nNormalizing starting plot (%d,%d)", kPlot.getX(), kPlot.getY());
	else
	{
		logBBAI("\n\n%S is about to found a city at (%d,%d); turn %d (year %d)", getPlayer().getName(),
				kPlot.getX(), kPlot.getY(), GC.getGame().getGameTurn(), GC.getGame().getGameTurnYear());
		logBBAI("Lower bound for found value: %d", getPlayer().AI_getMinFoundValue());
	}
	evaluateWithLogging(kPlot);
	if (isStartingLoc() || getPlayer().isBarbarian())
		return;
	{
		CvPlot const* pNextBestSite = NULL;
		int iBest = 0;
		for (int i = 0; i < getPlayer().AI_getNumCitySites(); i++)
		{
			CvPlot const& kLoopPlot = getPlayer().AI_getCitySite(i);
			if (&kLoopPlot == &kPlot)
				continue;
			int iValue = evaluate(kLoopPlot);
			if (iValue > iBest)
			{
				pNextBestSite = &kLoopPlot;
				iBest = iValue;
			}
		}
		if (pNextBestSite != NULL)
		{
			int iNextX = pNextBestSite->getX();
			int iNextY = pNextBestSite->getY();
			logBBAI("\nNext best site: %d (%d,%d)", iBest, iNextX, iNextY);
			evaluateWithLogging(kPlot);
		}
	}
	{
		CvPlot const* pBestAdjSite = NULL;
		int iBest = 0;
		FOR_EACH_ADJ_PLOT(kPlot)
		{
			int iValue = evaluate(*pAdj);
			if (iValue > iBest)
			{
				pBestAdjSite = pAdj;
				iBest = iValue;
			}
		}
		if (pBestAdjSite != NULL)
		{
			int iAdjX = pBestAdjSite->getX();
			int iAdjY = pBestAdjSite->getY();
			logBBAI("\nBest site adjacent to (%d,%d): %d (%d,%d)", kPlot.getX(), kPlot.getY(), iBest, iAdjX, iAdjY);
			evaluateWithLogging(kPlot);
		}
	}
}


bool AIFoundValue::bLoggingEnabled = false;


void AIFoundValue::setLoggingEnabled(bool b)
{
	bLoggingEnabled = b;
} // </advc.031c>

AIFoundValue::AIFoundValue(CvPlot const& kPlot, CitySiteEvaluator const& kSettings) :
	kPlot(kPlot), kArea(kPlot.getArea()), kSet(kSettings), kPlayer(kSet.getPlayer()),
	eTeam(kPlayer.getTeam()), ePlayer(kPlayer.getID()), kTeam(GET_TEAM(eTeam)),
	kGame(GC.getGame()), iX(kPlot.getX()), iY(kPlot.getY()), m_iResult(0)
{
	PROFILE_FUNC();
	if (!kPlayer.canFound(kPlot, false,
		/*	advc.181: Don't let action recommendations for human settlers
			give away rival cities founded in the fog of war. */
		!kPlayer.isHuman() || kSet.isAllSeeing()))
	{
		return;
	}
	bBarbarian = kPlayer.isBarbarian();
	eEra = kPlayer.getCurrentEra();
	rAIEraFactor = kPlayer.AI_getCurrEraFactor();
	bCoastal = kPlot.isCoastalLand(-1);
	iAreaCities = kArea.getCitiesPerPlayer(ePlayer);
	pCapital = kPlayer.AI_getCapital();
	// <advc.108> Barbarians shouldn't distinguish between earlier and later cities
	iCities = (bBarbarian ? 5 : kPlayer.getNumCities());
	FAssert(iCities > 0 || !kPlayer.isFoundedFirstCity());
	// </advc.108>

	//"nice hacky way to avoid messing with normalizer"
	// advc.031e: Now only used for calls from Python; see CyPlayer::AI_foundValue.
	//bNormalize = (kSet.isStartingLoc() && &kPlot == kPlayer.getStartingPlot());

	bFirstColony = false;
	iUnrevealedTiles = 0;

	m_iResult = evaluate();
}

/*  Body from CvPlayerAI::AI_foundValue_bulk, split into subroutines.
	More refactoring could be done; for one thing, some of the functions have
	long (return) parameter lists. Should probably introduce a class CityPlot
	for the data (and behavior) in the plot evaluation loop. At least it's
	no longer a single 1000-LoC function inside the largest GameCore class.
	K-Mod: Heavily edited (some changes marked, others not.)
	note, this function is called for every revealed plot for every player
	at the start of every turn. try to not make it too slow! */
short AIFoundValue::evaluate()
{
	IFLOG logSite();

	if (!isSiteValid() || !computeOverlap())
	{
		IFLOG logBBAI("Site disregarded");
		return 0;
	}

	// Bad tiles, unrevealed tiles, first colony
	int iBadTiles = 0;
	int iInnerBadTiles = 0;
	int iLandTiles = 0; // advc.031
	// <advc.040>
	bool bFirstColony = isPrioritizeAsFirstColony();
	IFLOG if(bFirstColony) logBBAI("First colony");
	// Scope for countBadTiles return parameters
	{
		int iRevealedDecentLand = 0;
		// </advc.040>
		int iUnrevealed = 0;
		iBadTiles = countBadTiles(iInnerBadTiles, iUnrevealed, iLandTiles,
				iRevealedDecentLand);
		iUnrevealedTiles = iUnrevealed;
		/*  <advc.040> Make sure we do naval exploration near the site before
			sending a Settler */
		if (iRevealedDecentLand < 4)
		{
			IFLOG if(bFirstColony) logBBAI("Only %d decent revealed land tiles; first-colony logic disabled.", iRevealedDecentLand);
			bFirstColony = false;
		} // </advc.040>
	}
	if (isTooManyBadTiles(iBadTiles, iInnerBadTiles))
	{
		IFLOG logBBAI("Too many bad tiles");
		return 0;
	}

	int iValue = baseCityValue();
	IFLOG logBBAI("Base city value: %d", iValue);

	IFLOG logBBAI("Evaluate city radius ...");
	std::vector<int> aiPlotValues(NUM_CITY_PLOTS, 0);

	std::vector<int> aiBonusCount(GC.getNumBonusInfos(), 0);
	int iResourceValue = 0;
	int aiSpecialYield[NUM_YIELD_TYPES] = {0, 0, 0}; // advc: Instead of individual variables
	/*  advc (comment): So that we can tell whether the city
		will be able to work its high-yield tiles */
	int iSpecialFoodPlus = 0;
	int iSpecialFoodMinus = 0;
	int iSpecialYieldTiles = 0; // advc.031: Number of tiles with special yield

	// advc: TeamMateTakenTiles code deleted (was dead code b/c of K-Mod changes)
	//int iYieldLostHere = 0; // advc: unused
	int iTakenTiles = 0;
	//bool bNeutralTerritory = true;
	bool bAnyForeignOwned = false; // advc.040: Replacing the above
	// <advc.031>
	int iGoody = 0; // for normalization
	bool bAnyGrowthBonus = false;
	int iStealPercent = 0;
	int iRiverTiles = 0;
	int iGreenTiles = 0;
	int iTotalFeatureProduction = 0; // </advc.031>
	int iHealth = 0;

	// K-Mod. (used to devalue cities which are unable to get any production.)
	scaled rBaseProduction; // (advc.031: scaled)

	FOR_EACH_ENUM(CityPlot)
	{
		// <advc.031>
		CvPlot const* pLoopPlot = plotCity(iX, iY, eLoopCityPlot);
		if (pLoopPlot != NULL && pLoopPlot->isGoody() &&
			eLoopCityPlot != CITY_HOME_PLOT) // advc.027
		{
			iGoody++;
		}
		bool bShare = false;
		bool bSteal = false; // </advc.031>
		bool bCityRadius = false;
		bool bForeignOwned = false;
		if (!isUsablePlot(eLoopCityPlot, iTakenTiles, bCityRadius, bForeignOwned,
			bAnyForeignOwned, bShare, bSteal))
		{
			continue;
		}
		CvPlot const& p = *pLoopPlot;
		bool const bHome = isHome(p);
		// advc.035: The own-exclusive-radius rule only helps if the radii don't overlap
		bool const bOwnExcl = (GC.getDefineBOOL(CvGlobals::OWN_EXCLUSIVE_RADIUS) &&
				!bCityRadius && bForeignOwned);

		bool bRemovableFeature = false; // K-Mod
		bool bPersistentFeature = false; // advc: was "eventuallyRemovable" in K-Mod
		int iFeatureProduction = 0; // advc.031
		FeatureTypes const eFeature = p.getFeatureType();
		bRemovableFeature = isRemovableFeature(p, bPersistentFeature,
					/* <advc.031> */ iFeatureProduction);
		bool const bCanNeverImprove = (eFeature != NO_FEATURE &&
				GC.getInfo(eFeature).isNoImprovement());
		/*  (Non-resource water also can't be improved; that's already covered by
			K-Mod code in evaluateYield) </advc.031> */
		if (!bHome)
		{
			FAssert(eFeature != NO_FEATURE || (!bRemovableFeature && !bPersistentFeature));
			int const iFeatureHealth = (eFeature == NO_FEATURE ? 0 :
					GC.getInfo(eFeature).getHealthPercent());
			if (!bRemovableFeature || iFeatureHealth > 0)
				iHealth += iFeatureHealth;
		}
		BonusTypes const eBonus = getBonus(p);
		// <advc.031> (This was much coarser in K-Mod)
		bool bCanTradeBonus = false;
		bool bCanSoonTradeBonus = false;
		bool bCanImproveBonus = false;
		bool bCanSoonImproveBonus = false;
		int aiBonusImprovementYield[NUM_YIELD_TYPES] = {0, 0, 0};
		ImprovementTypes eBonusImprovement = NO_IMPROVEMENT;
		{
			bool bImprovementRemovesFeature = false;
			eBonusImprovement = getBonusImprovement(eBonus, p,
					bCanTradeBonus, bCanSoonTradeBonus, aiBonusImprovementYield,
					bCanImproveBonus, bCanSoonImproveBonus, bImprovementRemovesFeature);
			if (!bImprovementRemovesFeature && eBonusImprovement != NO_IMPROVEMENT)
				iFeatureProduction = 0;
		} // </advc.031>

		int iCultureModifier = 100;
		if (!bHome) // advc.031: Shouldn't matter on home plot
		{
			iCultureModifier = calculateCultureModifier(
					p, bForeignOwned, bShare, bCityRadius, bSteal,
					abFlip[eLoopCityPlot], bOwnExcl, iTakenTiles, iStealPercent);
			FAssertBounds(0, 101, iCultureModifier);
		}  // <advc.031>
		iFeatureProduction = (iFeatureProduction * iCultureModifier) / 100;
		iTotalFeatureProduction += iFeatureProduction; // </advc.031>
		// K-Mod note. This used to be called iTempValue.
		int iPlotValue = 0;
		/*  advc: Renamed from aiYield for clarity. Improvement yields are only predicted
			for resource plots (aiSpecialYield). */
		int aiNatureYield[NUM_YIELD_TYPES];
		FOR_EACH_ENUM(Yield)
		{
			aiNatureYield[eLoopYield] = //p->getYield(eLoopYield);  // K-Mod replacement:
					p.calculateNatureYield(eLoopYield,
					/*	advc.031: NO_TEAM makes calculateNatureYield ignore the resource
						(whereas CvPlot::getBonusType treats NO_TEAM as all-revealing) */
					eBonus == NO_BONUS ? NO_TEAM : eTeam,
					!bPersistentFeature || bHome); // advc.031: City removes all features
			// <advc.031> Replacing deleted K-Mod code
			if (bHome)
			{
				aiNatureYield[eLoopYield] += p.calculateCityPlotYieldChange(
						eLoopYield, aiNatureYield[eLoopYield], 1);
			} // </advc.031>
		}
		if (bHome)
		{
			rBaseProduction += aiNatureYield[YIELD_PRODUCTION];
			iSpecialFoodPlus += std::max(0, aiNatureYield[YIELD_FOOD] -
					GC.getFOOD_CONSUMPTION_PER_POPULATION());
		}
		else
		{
			if (!bPersistentFeature && eFeature != NO_FEATURE)
			{
				iPlotValue += removableFeatureYieldVal(eFeature,
						bRemovableFeature, eBonus != NO_BONUS);
			}
			// <advc.031>
			if (!kSet.isStartingLoc()) // Don't factor traits into starting sites
			{
				FOR_EACH_ENUM(Yield)
				{
					
					{
						int iThresh = kPlayer.getExtraYieldThreshold(eLoopYield);
						if (iThresh > 0 &&
							aiNatureYield[eLoopYield] >= iThresh)
						{
							aiNatureYield[eLoopYield] += GC.getDefineINT(
									CvGlobals::EXTRA_YIELD);
						}
					}
					// <advc.908a>
					{
						int iThresh = kPlayer.getExtraYieldNaturalThreshold(eLoopYield);
						if (iThresh > 0 &&
							aiNatureYield[eLoopYield] + 1 >= iThresh)
						{
							aiNatureYield[eLoopYield] += GC.getDefineINT(
									CvGlobals::EXTRA_YIELD);
						}
					} // </advc.908a>
				}
			} // </advc.031>
			// K-Mod. add non-home plot production to BaseProduction.
			if (!bShare)
				rBaseProduction += aiNatureYield[YIELD_PRODUCTION];
			if (!bSteal)
				rBaseProduction += estimateImprovementProduction(p, bPersistentFeature);
			if (!p.isWater())
			{
				// freshwater health (home plot) will be counted later
				iPlotValue += evaluateFreshWater(p, aiNatureYield, bSteal,
						iRiverTiles, iGreenTiles);
			}
		}
		iPlotValue += evaluateYield(aiNatureYield, &p, bCanNeverImprove); // (K-Mod: iTempValue in BtS)
		if (bHome)
		{
			// <advc.031> Count home plot yield twice b/c it's immediately available
			iPlotValue *= 2;
			iValue += iPlotValue;
			if (eBonus != NO_BONUS)
			{
				// Replacing K-Mod code that had adjusted the home plot yield
				iValue += foundOnResourceValue( // (result normally negative)
						eBonusImprovement == NO_IMPROVEMENT ? NULL : aiBonusImprovementYield);
			} // </advc.031>
		}
		else
		{
			iPlotValue = applyCultureModifier(p, iPlotValue, iCultureModifier, bShare);
			aiPlotValues[eLoopCityPlot] = iPlotValue; // Sum these up later
		}
		bool const bEasyAccess = /* K-Mod (!!): */ ((p.isWater() && (bCoastal ||
				p.getArea().getCitiesPerPlayer(ePlayer, true) > 0)) || // advc.031
				p.sameArea(kPlot) || p.getArea().getCitiesPerPlayer(ePlayer) > 0);
		IFLOG logPlot(p, iPlotValue, aiNatureYield, iCultureModifier, eBonus, eBonusImprovement,
				bCanTradeBonus, bCanSoonTradeBonus, bCanImproveBonus, bCanSoonImproveBonus,
				bEasyAccess, iFeatureProduction, bPersistentFeature, bRemovableFeature);
		// <advc.031>
		if (bShare)
		{
			IFLOG if(eBonus!=NO_BONUS) logBBAI("Resource ignored (shared tile)");
			continue;
		}
		// Was 33 flat; the modifier is now computed differently.
		if (iCultureModifier <= (bSteal ? 40 : 20) &&// </advc.031>
			!bOwnExcl) // advc.035
		{
			IFLOG if(eBonus!=NO_BONUS) logBBAI("Resource ignored (unlikely to flip)");
			continue;
		}
		if (eBonus != NO_BONUS) // advc.040: Same-area checks moved into nonYieldBonusValue
		{
			if (!bBarbarian && // advc.303: Barbarians don't care about resource trade
				// advc.031: Otherwise we can already trade the resource
				getRevealedOwner(p) != ePlayer)
			{
				int iBonusValue = nonYieldBonusValue(p, eBonus,
						bCanTradeBonus, bCanSoonTradeBonus, bEasyAccess,
						bAnyGrowthBonus, &aiBonusCount, iCultureModifier);
				IFLOG if(iBonusValue!=0) logBBAI("+%d non-yield resource value (%S)",
						iBonusValue, GC.getInfo(eBonus).getDescription());
				//iValue += (iBonusValue + 10);
				iResourceValue += iBonusValue; // K-Mod
			}
			/*if (p.isWater())
				iValue += (bCoastal ? 0 : -800);*/ // (was ? 100 : -800)
			// <advc.031> Replacing the above
			if (p.isWater() && !bCoastal)
			{
				int const iPenalty = 165;
				IFLOG logBBAI("-%d from water resource near non-coastal site", iPenalty);
				iValue -= iPenalty;
			} // </advc.031>
		}
		if (!bHome) // (Home plot was handled upfront)
		{
			int iSpecialYieldModifier = calculateSpecialYieldModifier(iCultureModifier,
					bEasyAccess, eBonus != NO_BONUS, bCanSoonImproveBonus, bCanImproveBonus);
			calculateSpecialYields(p,
					eBonusImprovement == NO_IMPROVEMENT ? NULL : aiBonusImprovementYield,
					aiNatureYield, iSpecialYieldModifier,
					aiSpecialYield, iSpecialFoodPlus, iSpecialFoodMinus, iSpecialYieldTiles);
		}
	}

	iValue += sumUpPlotValues(aiPlotValues);
	// A sensible order (CITY_HOME_PLOT first) isn't guaranteed anymore, hence:
	aiPlotValues.clear();
	// advc.031: Preserve this for later
	int iNonYieldResourceVal = std::max(0, iResourceValue);
	if (iSpecialYieldTiles > 0) // advc.031
	{
		iResourceValue += evaluateSpecialYields(aiSpecialYield, iSpecialYieldTiles,
				iSpecialFoodPlus, iSpecialFoodMinus);
	}
	if (isTooManyTakenTiles(iTakenTiles, iResourceValue, iValue < 780))
	{
		IFLOG logBBAI("Too many taken tiles (%d)", iTakenTiles);
		return 0;
	}
	iValue += std::max(0, iResourceValue);

	iValue += evaluateLongTermHealth(iHealth); // (may increase iHealth)
	iValue += evaluateFeatureProduction(iTotalFeatureProduction); // advc.031

	if (bCoastal)
	{
		iValue += evaluateSeaAccess(
				// advc: Same conditions as in BtS ...
				kArea.getCitiesPerPlayer(ePlayer) == 0 &&
				!bAnyForeignOwned && iResourceValue > 0 && kSet.isSeafaring(),
				// <advc.031>
				fixp(0.7) * scaled::clamp(
				scaled::min(rBaseProduction + aiSpecialYield[YIELD_PRODUCTION],
				// Probably can't work high-production tiles when there is no food
				scaled(4 * (1 + iGreenTiles + iSpecialFoodPlus), 18)), fixp(0.1), 2),
				iLandTiles); // </advc.031>
	}
	iValue += evaluateDefense();
	IFLOG logBBAI("=%d in total before modifiers", iValue);

	if (!kSet.isStartingLoc() /* advc.031f: */ || kSet.isScenario())
	{
		/*  <advc.031> Moved down to the other modifiers. But don't adjust the
			non-yield resource value -- don't need food for a trade connection. */
		iValue = adjustToFood(iValue - iNonYieldResourceVal, iSpecialFoodPlus,
				iSpecialFoodMinus, iGreenTiles) + iNonYieldResourceVal;
		// </advc.031>
	}

	rBaseProduction += aiSpecialYield[YIELD_PRODUCTION]; // K-Mod
	iValue = adjustToProduction(iValue, rBaseProduction);

	// <advc.031>
	if (iResourceValue <= 0 && iSpecialFoodPlus <= 0 &&
		iUnrevealedTiles < 5) // advc.040
	{
		scaled rMultiplier = per100(60);
		if (iRiverTiles >= 4)
			rMultiplier = scaled::min(1, rMultiplier + per100(6) * iRiverTiles);
		iValue = (rMultiplier * iValue).round();
		IFLOG if(rMultiplier!=1) logBBAI("Times %d percent because the site offers nothing special", rMultiplier.getPercent());
	} // </advc.031>
	/*  advc.108: Obsoletion check added. Probably better not to let players start on
		a hidden resource; i.e. don't check this->getBonus(kPlot) != NO_BONUS. */
	if (kPlot.getNonObsoleteBonusType(eTeam) != NO_BONUS)
	{
		int iModifier = 100;
		if (kSet.isStartingLoc())
			iModifier = 50;
		else // advc.031: I don't think both penalties should be applied
			if (kSet.isAdvancedStart())
		{
			iModifier = 70;
		}
		iValue *= iModifier;
		iValue /= 100;
		IFLOG if(iModifier!=100) logBBAI("Times %d percent for starting on a resource", iModifier);
	}
	if (kSet.isStartingLoc())
		iValue = adjustToLandAreaBoundary(iValue);
	if (kSet.isStartingLoc() || /* advc.031e: */ kSet.isNormalizing())
	{	// <advc.027
		if (kSet.isIgnoreStartingSurroundings())
			iValue = adjustToStartingChoices(iValue);
		else // </advc.027>
			iValue = adjustToStartingSurroundings(iValue); // (advc: Moved down a bit)
	}
	if (bBarbarian)
		iValue = adjustToBarbarianSurroundings(iValue);
	else if (!kSet.isStartingLoc() /* advc.031e: */ && !kSet.isNormalizing())
		iValue = adjustToCivSurroundings(iValue, iStealPercent);

	if (iValue <= 0)
		return 1;

	iValue = adjustToCitiesPerArea(iValue);

	if (!kSet.isStartingLoc() /* advc.031e: */ && !kSet.isNormalizing())
		iValue = adjustToBonusCount(iValue, aiBonusCount);

	iValue = adjustToBadTiles(iValue, iBadTiles /* advc.031: */ + (4 * iTakenTiles) / 10
			-(bBarbarian ? 2 : (4 + iGreenTiles + iSpecialFoodPlus)) // advc.303
			/ (kSet.isStartingLoc() && !kSet.isScenario() ? 2 : 1)); // advc.108, advc.031f
	iValue = adjustToBadHealth(iValue, iHealth);
	// <advc.031>
	if (kSet.isNormalizing())
		iValue += evaluateGoodies(iGoody); // </advc.031>

	// advc: BtS code (iDifferentAreaTile) deleted
	// (disabled by K-Mod. This kind of stuff is already taken into account.)

	FAssert(iValue >= 0);
	IFLOG logBBAI("Bottom line (found-city value): %d\n", iValue);
	return std::max<short>(1, truncIntCast<short>(iValue));
}


bool AIFoundValue::isSiteValid() const
{
	//if (!kSet.isStartingLoc() && !kSet.isAdvancedStart())
	if(iCities > 0 && !bBarbarian) // advc.108
	{
		if (!bCoastal && iAreaCities == 0)
		{
			IFLOG logBBAI("First colony in area must be coastal");
			return false;
		}
	}

	int iMinRivalRange = kSet.getMinRivalRange();
	if (iMinRivalRange > 0)
	{
		for (SquareIter it(kPlot, iMinRivalRange); it.hasNext(); ++it)
		{
			if (it->plotCheck(PUF_isOtherTeam, ePlayer) != NULL)
			{
				IFLOG logBBAI("Rival plot (%d,%d) found in MinRivalRange", it->getX(), it->getY());
				return false;
			}
		}
	}
	if (kSet.isStartingLoc())
	{
		if (kPlot.isGoody() /* advc.027: */ && kSet.isScenario())
		{
			IFLOG logBBAI("Can't start on goody hut");
			return false;
		}
		FOR_EACH_ENUM(CityPlot)
		{
			CvPlot const* p = plotCity(iX, iY, eLoopCityPlot);
			if (p == NULL)
			{
				IFLOG logBBAI("Can't start near the edge of a flat map");
				return false;
			}
		}
	}
	else // advc.031: Not relevant for StartingLoc
	{
		int iOwnedTiles = 0;
		FOR_EACH_ENUM(CityPlot)
		{
			CvPlot const* p = plotCity(iX, iY, eLoopCityPlot);
			if (p == NULL)
				iOwnedTiles += 2;
			else if (getRevealedOwner(*p) != NO_PLAYER && getRevealedTeam(*p) != eTeam)
			{
				/*  advc.035 (comment): Would be good to check abFlip[i] here,
					but computeOverlap is a little costly. */
				iOwnedTiles++;
				/*  <advc.031> Count tiles only half if they're in our inner ring
					and can't be worked by any foreign city. */
				if (!adjacentOrSame(*p, kPlot) || p->isCityRadius())
					iOwnedTiles++; // </advc.031>
			}
		}
		//if(iOwnedTiles > NUM_CITY_PLOTS / 3)
		/*  <advc.031> Most owned tiles are counted twice now, and I want sth.
			closer to half of the tiles being owned. */
		int const iMaxOwnedTimes100 = 82 * NUM_CITY_PLOTS;
		if (100 * iOwnedTiles > iMaxOwnedTimes100) // </advc.031>
		{
			IFLOG logBBAI("%d tiles owned by other teams; allowed (times 100): %d", iOwnedTiles, iMaxOwnedTimes100);
			return false;
		}
	}
	return true;
}

// Returns false when there is too much overlap
bool AIFoundValue::computeOverlap()
{
	/*	K-Mod explanation of city site adjustment:
		Any plot which is otherwise within the radius of a city site is basically
		treated as if it's within an existing city radius */
	/*  advc.031: Changed to int in order to store the site id
		(only used for logging currently though) */
	aiCitySiteRadius.resize(NUM_CITY_PLOTS, -1);
	/*  <advc.035>
		Need to distinguish tiles within the radius of one of our team's cities
		from those within just any city radius. */
	abOwnCityRadius.resize(NUM_CITY_PLOTS, false);
	// Whether the tile flips to us once we settle near it
	abFlip.resize(NUM_CITY_PLOTS, false); // </advc.035>
	// K-Mod. bug fixes etc. (original code deleted)
	if (!kSet.isStartingLoc() /* advc.031e: */ && !kSet.isNormalizing() &&
		!kSet.isDebug() && // advc.007
		!bBarbarian) // advc.303: Barbarians don't have city sites
	{
		for (int iSite = 0; iSite < kPlayer.AI_getNumCitySites(); iSite++)
		{
			CvPlot const& kCitySitePlot = kPlayer.AI_getCitySite(iSite);
			if (&kCitySitePlot == &kPlot)
				continue;
			if (plotDistance(&kPlot, &kCitySitePlot) <=
				GC.getDefineINT(CvGlobals::MIN_CITY_RANGE) &&
				kCitySitePlot.sameArea(kPlot))
			{
				IFLOG logBBAI("Too close to one of the sites we've already chosen");
				return false;
			}
			for (CityPlotIter it(kPlot); it.hasNext(); ++it)
			{
				if (plotDistance(&(*it), &kCitySitePlot) <= CITY_PLOTS_RADIUS)
				{
					//Plot is inside the radius of a city site
					aiCitySiteRadius[it.currID()] = iSite;
				}
			}
		}
	} // K-Mod (bugfixes etc.) end
	// <advc.035> (also for advc.031)
	if (!kSet.isStartingLoc() && !kSet.isNormalizing() && !bBarbarian)
	{
		FOR_EACH_CITY(c, kPlayer)
		{
			FOR_EACH_ENUM(CityPlot)
			{
				CvPlot const* p = plotCity(iX, iY, eLoopCityPlot);
				if(p != NULL && plotDistance(p->getX(), p->getY(),
					c->getX(), c->getY()) <= CITY_PLOTS_RADIUS)
				{
					abOwnCityRadius[eLoopCityPlot] = true;
				}
			}
		}
		if (GC.getDefineBOOL(CvGlobals::OWN_EXCLUSIVE_RADIUS))
		{
			FOR_EACH_ENUM(CityPlot)
			{
				CvPlot const* p = plotCity(iX, iY, eLoopCityPlot);
				abFlip[eLoopCityPlot] = (!abOwnCityRadius[eLoopCityPlot] &&
						p != NULL && getRevealedOwner(*p) != NO_PLAYER &&
						p->isCityRadius() && getRevealedTeam(*p) != eTeam &&
						(p->getSecondOwner() == ePlayer ||
						/*  The above is enough b/c the tile may not be within the
							culture range of one of our cities; but it will be once
							the new city is founded. */
						p->findHighestCulturePlayer(true) == ePlayer));
			}
		} // </advc.035>
	}
	return true;
}

// <advc.040>
bool AIFoundValue::isPrioritizeAsFirstColony() const
{

	return (bCoastal && iAreaCities <= 0 && !bBarbarian && iCities > 0 &&
			(kPlot.isFreshWater() ||
			/*  Don't prioritize colonies in tundra, snow and desert b/c
				these are likely surrounded by more (unrevealed) bad terrain. */
			kPlot.calculateNatureYield(YIELD_FOOD, eTeam, true) +
			kPlot.calculateNatureYield(YIELD_PRODUCTION, eTeam, true) > 1));
} // </advc.040>


int AIFoundValue::countBadTiles(/* advc.031: */ int& iInnerRadius,
	int& iUnrevealed, /* advc.031: */ int& iLand,
	int& iRevealedDecentLand) const // advc.040
{
	int iBadTiles = 0;
	FOR_EACH_ENUM(CityPlot)
	{
		CvPlot const* p = plotCity(iX, iY, eLoopCityPlot);
		// <advc.031>
		bool const bInner = (eLoopCityPlot < NUM_INNER_PLOTS);
		/*  NULL and impassable count as 2 bad tiles (as in BtS),
			but don't cheat with unrevealed tiles. */
		if (p == NULL)
		{
			if (bInner)
				iInnerRadius += 2;
			iBadTiles += 2;
			continue;
		}
		if (!isRevealed(*p))
		{
			iUnrevealed++; // advc.040
			if (bInner)
				iInnerRadius++;
			continue;
		}
		if (isHome(*p))
			continue;
		// <advc.303>
		if (bBarbarian && !adjacentOrSame(*p, kPlot))
		{
			/*  Rational Barbarians wouldn't mind settling one off the coast,
				but human players do mind, and some really hate this.
				Therefore, count the outer ring coast as bad if !bCoastal. */
			if(p != NULL && p->isWater() && !bCoastal &&
				p->calculateBestNatureYield(YIELD_FOOD, eTeam) <= 1)
			{
				iBadTiles++;
				if (bInner)
					iInnerRadius++;
			}
			continue;
		} // </advc.303>

		if (!p->isWater())
			iLand++;
		int iBadLoop = 0;
		if (p->isImpassable())
			iBadLoop += 2;
		// </advc.031>
		// K-Mod (original code deleted)
		else if (//!p->isFreshWater() &&
		/*  advc.031: Flood plains have high nature yield anyway,
			so this is about snow.
			Bonus check added (Incense). */
			getBonus(*p) == NO_BONUS &&
			(p->calculateBestNatureYield(YIELD_FOOD, eTeam) == 0 ||
			p->calculateTotalBestNatureYield(eTeam) <= 1))
		{
			/*  advc.031: Snow hills will count for BaseProduction, but, generally
				they're really bad. */
			iBadLoop += 2;
		}
		else if (p->isWater() && p->calculateBestNatureYield(YIELD_FOOD, eTeam) <= 1)
		{	/*  <advc.031> Removed the bCoastal check from the
				condition above b/c I want to count ocean tiles as
				half bad even when the city is at the coast. */
			if(!kSet.isSeafaring() &&
				p->calculateBestNatureYield(YIELD_COMMERCE, eTeam) <= 1)
			{
				iBadLoop++;
				// <advc.108> Ocean can't be "normalized" away later on
				if (kSet.isStartingLoc() /* adv.031f: */ && !kSet.isScenario())
					iBadLoop++; // </advc.108>
			}
			if(!bCoastal)
				iBadLoop++; // </advc.031>
		}
		else if (getRevealedOwner(*p) != NO_PLAYER)
		{
			if(!abFlip[eLoopCityPlot]) // advc.035
			{
				if (getRevealedTeam(*p) != eTeam || p->isBeingWorked())
					iBadLoop++;
				/*  (K-Mod) note: this final condition is...
					not something I intend to keep permanently. */
				// advc.031: poof
				/*else if (p->isCityRadius() || aiCitySiteRadius[iI] >= 0)
					iBadTiles++;*/
			} // advc.035
		}
		else iRevealedDecentLand++; // advc.040
		// <advc.031>
		iBadTiles += iBadLoop;
		if (bInner)
			iInnerRadius += iBadLoop;
	}
	iInnerRadius /= 2; // </advc.031>
	iBadTiles /= 2;
	IFLOG (iUnrevealed > 0 ? logBBAI("Bad tiles: %d known bad, %d unrevealed", iBadTiles, iUnrevealedTiles) :
							 logBBAI("Bad tiles: %d", iBadTiles));
	return iBadTiles;
}

// Returns true if the site should be disregarded
bool AIFoundValue::isTooManyBadTiles(int iBadTiles,
	int iInnerBadTiles) const // advc.031
{
	if (kSet.isStartingLoc() /* advc.031e: */ || kSet.isNormalizing())
		return false;
	if (2 * iBadTiles <= NUM_CITY_PLOTS && kArea.getNumTiles() > 2 &&
		(!bBarbarian || iBadTiles <= 3)) // advc.303
	{
		return false;
	}
	/*	advc.031: Cities with only worthless tiles in the inner ring will
		struggle to ever expand their borders. */
	bool bInnerOnly = (!kSet.isEasyCulture() && 3 * iInnerBadTiles >= 2 * NUM_INNER_PLOTS);
	bool bHasGoodBonus = false;
	int iMediocreBonuses = 0; // advc.031
	int iFreshWaterTiles = (kPlot.isFreshWater() ? 1 : 0); // advc.031 (count kPlot twice)
	for (CityPlotIter it(kPlot); it.hasNext(); ++it)
	{
		CvPlot const& p = *it;
		if(!isRevealed(p))
			continue;
		// <advc.031>
		if (bInnerOnly && it.currID() >= NUM_INNER_PLOTS &&
			getRevealedOwner(p) != ePlayer)
		{
			continue;
		} // </advc.031>
		// <advc.303>
		if(bBarbarian && !adjacentOrSame(p, kPlot))
			continue; // </advc.303>
		if(getRevealedOwner(p) != NO_PLAYER &&
			// <advc.031>
			(getRevealedOwner(p) != ePlayer ||
			p.getCityRadiusCount() > 0)) // </advc.031>
		{
			continue;
		}
		BonusTypes eBonus = getBonus(p); // advc.108
		if (eBonus != NO_BONUS &&
			!kTeam.isBonusObsolete(eBonus)) // K-Mod
		{
			if ((kPlayer.getNumTradeableBonuses(eBonus) == 0 ||
				kPlayer.AI_bonusVal(eBonus, 1, true) > 10 ||
				GC.getInfo(eBonus).getYieldChange(YIELD_FOOD) > 0) &&
				// <advc.031> Moved from above
				(p.isWater() || p.isArea(kArea) ||
				p.getArea().getCitiesPerPlayer(ePlayer) > 0)) // </advc.031>
			{
				bHasGoodBonus = true;
				break;
			} // <advc.031>
			else iMediocreBonuses++;
		}
		if(p.isFreshWater())
			iFreshWaterTiles++; // </advc.031>
	}

	return (!bHasGoodBonus && /* advc.040: */ !bFirstColony &&
			iFreshWaterTiles < 3 && iMediocreBonuses < 2); // advc.031
}


int AIFoundValue::baseCityValue() const
{
	// advc.031: was 800 in K-Mod and 1000 before K-Mod
	int r = 150;
	// <advc.108>
	if (iUnrevealedTiles <= 0)
		return r;
	if (iCities <= 0)
	{
		int const iCapitalValue = (50 * scaled(iUnrevealedTiles).sqrt()).round();
		IFLOG if(iCapitalValue>0) logBBAI("+%d base value for unrevealed tiles near initial city", iCapitalValue);
		r += iCapitalValue;
	} // </advc.108>
	// <advc.040>
	else if (bFirstColony)
	{
		int const iFirstColonyValue = 55 * std::min(5, iUnrevealedTiles);
		IFLOG logBBAI("+%d base value for unrevealed tiles near first colony", iFirstColonyValue);
		r += iFirstColonyValue;
	} // </advc.040>
	return r;
}


bool AIFoundValue::isUsablePlot(CityPlotTypes ePlot, int& iTakenTiles, bool& bCityRadius,
	bool& bForeignOwned, bool& bAnyForeignOwned, bool& bShare, bool& bSteal) const
{
	CvPlot const* p = plotCity(iX, iY, ePlot);
	if (p == NULL)
	{
		iTakenTiles++;
		return false;
	}
	bool const bInnerRing = adjacentOrSame(*p, kPlot);
	// <advc.303>
	if (bBarbarian && !bInnerRing)
		return false; // </advc.303>
	/*	advc.031: Moved up. If we can't see the tile, we don't really know if it's
		already taken by a rival. (Will find out when our Settler gets there.) */
	if (!isRevealed(*p))
	{
		IFLOG logBBAI("Unrevealed plot skipped: (%d,%d)", p->getX(), p->getY());
		return false;
	}
	if (isHome(*p))
		return true;
	// <advc.035>
	if (abFlip[ePlot])
	{
		IFLOG logBBAI("Assumed to flip: %S", p->debugStr());
		return true;
	}
	// </advc.035>
	// <advc.031>
	bCityRadius = p->isCityRadius();
	PlayerTypes const eOwner = getRevealedOwner(*p);
	bForeignOwned = (eOwner != NO_PLAYER && eOwner != ePlayer);
	bSteal = (bCityRadius && bForeignOwned);
	 // </advc.031>
	if (bCityRadius || aiCitySiteRadius[ePlot] >= 0)
	{
		iTakenTiles++;
		// <advc.040>
		if(bForeignOwned)
			bAnyForeignOwned = true; // </advc.040>
		//return false;
	}
	/*  K-Mod Note: it kind of sucks that no value is counted for taken tiles.
		Tile sharing / stealing should be allowed. */
	// <advc.031> ^Exactly
	/*  Still don't allow tiles to be shared between (planned) city sites
		-- too difficult to estimate how many tiles each site will need. */
	if (aiCitySiteRadius[ePlot] >= 0)
	{
		IFLOG logBBAI("%S reserved for higher-priority site at (%d,%d)", p->debugStr(),
				kPlayer.AI_getCitySite(aiCitySiteRadius[ePlot]).getX(), kPlayer.AI_getCitySite(aiCitySiteRadius[ePlot]).getY());
		return false;
	}
	bool bOtherInnerRing = false;
	CvCityAI const* pOtherCity = NULL;
	if (bCityRadius)
	{
		if (bBarbarian)
		{
			IFLOG logBBAI("(%d,%d) is in the radius of another city", p->getX(), p->getY());
			return false;
		}
		pOtherCity = p->AI_getWorkingCity();
		if (pOtherCity == NULL && abOwnCityRadius[ePlot])
		{
			IFLOG logBBAI("(%d,%d) is in the radius of a %S city whose borders haven't expanded yet",
					p->getX(), p->getY(), kPlayer.getCivilizationShortDescription());
			/*  Difficult to judge whether tile sharing makes sense;
				better wait for borders to expand. */
			return false;
		}
		if (pOtherCity != NULL && (kPlayer.isHuman() ? pOtherCity->isRevealed(eTeam) :
			(kTeam.AI_deduceCitySite(*pOtherCity) ||
			/*  At the start of the game, a single revealed tile should
				be enough to locate the city. */
			iCities == 0)))
		{
			bOtherInnerRing = adjacentOrSame(*p, *pOtherCity->plot());
			FAssert(!bInnerRing || !bOtherInnerRing || !pOtherCity->isArea(kArea) ||
					/*	In that case, stealing from the inner ring should
						perhaps be considered. (But AdvCiv uses range 2 like BtS,
						so I'm not going to address range 1.) */
					GC.getDefineINT(CvGlobals::MIN_CITY_RANGE) < 2);
			if (bForeignOwned && (bOtherInnerRing ||
				// Don't try to overlap with team member or master
				TEAMID(eOwner) == eTeam ||
				kTeam.isVassal(TEAMID(eOwner))))
			{
				IFLOG logBBAI("Don't count on stealing %S from %S", p->debugStr(), cityName(*pOtherCity));
				return false;
			}
			if (!bForeignOwned)
				bShare = true;
			// Else let iCultureModifier handle bSteal
		}
	}
	if (!bShare)
		return true;

	if(p->isBeingWorked() || bOtherInnerRing)
	{
		IFLOG logBBAI("Don't want to take (%d,%d) away from %S", p->getX(), p->getY(), cityName(*pOtherCity));
		return false;
	}
	CityPlotTypes const eOtherPlotIndex = pOtherCity->getCityPlotIndex(*p);
	if (GC.getCityPlotPriority()[ePlot] >= GC.getCityPlotPriority()[eOtherPlotIndex])
	{
		IFLOG logBBAI("%S has higher priority for (%d,%d)", cityName(*pOtherCity), p->getX(), p->getY());
		return false;
	}
	// Check if the other city is going to need the tile in the medium term
	if (pOtherCity->AI_isGoodPlot(eOtherPlotIndex) &&
		pOtherCity->AI_countGoodPlots() -
		pOtherCity->getPopulation() +
		pOtherCity->getSpecialistPopulation() <= 3)
	{
		IFLOG logBBAI("Don't want to take (%d,%d); %S might need it soon", p->getX(), p->getY(), cityName(*pOtherCity));
		return false;
	}
	// Else let the caller deal with bShare
	/*  (No special treatment for bShare&&bSteal; we'll
		probably win the tile if we have two cities near it.) */
	return true;
	// </advc.031>
}

// based on K-Mod code
bool AIFoundValue::isRemovableFeature(CvPlot const& p, bool& bPersistent,
	int& iFeatureProduction) const // advc.031
{
	bPersistent = false;
	iFeatureProduction = 0;
	// <advc.031>
	if (isHome(p))
		return true; // </advc.031>
	FeatureTypes const eFeature = p.getFeatureType();
	if (eFeature == NO_FEATURE)
		return false;

	CvFeatureInfo const& kFeature = GC.getInfo(eFeature);
	bPersistent = true;
	FOR_EACH_ENUM(Build)
	{
		CvBuildInfo const& kLoopBuild = GC.getInfo (eLoopBuild);
		if (!kLoopBuild.isFeatureRemove(eFeature))
			continue;

		bPersistent = false;
		// <advc.031>
		CvTerrainInfo const& kTerrain = GC.getInfo(p.getTerrainType());
		int iTerrainYieldSum = 0;
		int iFeatureYieldSum = 0;
		FOR_EACH_ENUM(Yield)
		{
			iTerrainYieldSum += kTerrain.getYield(eLoopYield);
			iFeatureYieldSum += kFeature.getYieldChange(eLoopYield);
		}
		// Count feature production only if the feature is (presumably) worth removing
		if (iTerrainYieldSum > iFeatureYieldSum)
		{
			CvCity* pDummy;
			iFeatureProduction = p.getFeatureProduction(eLoopBuild, eTeam, &pDummy, &kPlot, ePlayer);
			if (getRevealedTeam(p) == eTeam)
				iFeatureProduction /= 3; // Can already chop it
		}
		// CurrentResearch should be good enough
		TechTypes eTech1 = kLoopBuild.getTechPrereq();
		TechTypes eTech2 = kLoopBuild.getFeatureTech(eFeature);
		// </advc.031>
		if (kTeam.isHasTech(eTech1) &&
			kTeam.isHasTech(eTech2)) // advc.001: This check was missing
		{
			return true;
		}
		// <advc.031>
		for (MemberIter it(eTeam); it.hasNext(); ++it)
		{
			CvPlayer const& kMember = *it;
			if (kMember.getCurrentResearch() == eTech1 &&
				kMember.getCurrentResearch() == eTech2)
			{
				return true;
			}
		} // </advc.031>
	}
	return false;
}

// (replacing all CvPlot::isRevealed calls)
bool AIFoundValue::isRevealed(CvPlot const& p) const
{
	return (kSet.isAllSeeing() || p.isRevealed(eTeam));
}

// (replacing all CvPlot::getOwner and isOwned calls)
PlayerTypes AIFoundValue::getRevealedOwner(CvPlot const& p) const
{
	if (kSet.isAllSeeing())
		return p.getOwner();
	return p.getRevealedOwner(eTeam);
}

// (replacing all CvPlot::getTeam calls)
TeamTypes AIFoundValue::getRevealedTeam(CvPlot const& p) const
{
	PlayerTypes ePlayer = getRevealedOwner(p);
	if (ePlayer == NO_PLAYER)
		return NO_TEAM;
	return TEAMID(ePlayer);
}

// (replacing all CvPlot::getBonusType and getNonObsoleteBonusType calls)
BonusTypes AIFoundValue::getBonus(CvPlot const& p) const
{
	BonusTypes const eBonus = p.getBonusType();
	if (eBonus == NO_BONUS)
		return NO_BONUS;
	// <advc.108>
	if (kSet.isStartingLoc() /* advc.031e: */ || kSet.isNormalizing())
	{
		if (kGame.getStartingPlotNormalizationLevel() > CvGame::NORMALIZE_LOW)
			return eBonus;
		/*	Treat resources revealed by any starting tech as revealed.
			(No such resources exist in BtS, AdvCiv.) */
		TechTypes const eTech = GC.getInfo(eBonus).getTechReveal();
		if (eTech != NO_TECH &&
			GC.getInfo(eTech).getNumOrTechPrereqs() <= 0 &&
			GC.getInfo(eTech).getNumAndTechPrereqs() <= 0)
		{
			return eBonus;
		}
	} // </advc.108>
	return p.getBonusType(eTeam);
}

/*  advc.031: Rewritten. K-Mod had added a crucial isImprovementBonusTrade check, but
	other important checks were still missing. */
ImprovementTypes AIFoundValue::getBonusImprovement(BonusTypes eBonus, CvPlot const& p,
	bool& bCanTrade, bool& bCanTradeSoon, int* aiYield,
	bool& bCanImprove, bool& bCanImproveSoon, bool& bRemoveFeature) const
{
	bCanTrade = bCanTradeSoon = bCanImprove = bCanImproveSoon = bRemoveFeature = false;
	if (eBonus == NO_BONUS)
		return NO_IMPROVEMENT;

	ImprovementTypes eBestImprovement = NO_IMPROVEMENT;
	int iBestYield = -1;
	FeatureTypes const eFeature = p.getFeatureType();
	FOR_EACH_ENUM(Build)
	{
		CvBuildInfo const& kLoopBuild = GC.getInfo(eLoopBuild);
		ImprovementTypes eImprovement = kLoopBuild.getImprovement();
		if (eImprovement == NO_IMPROVEMENT)
			continue;
		CvImprovementInfo const& kImprovement = GC.getInfo(eImprovement);
		TechTypes const eBuildPrereq = kLoopBuild.getTechPrereq();
		if (!kImprovement.isImprovementBonusMakesValid(eBonus) ||
			!kImprovement.isImprovementBonusTrade(eBonus) ||
			!isNearTech(eBuildPrereq))
		{
			continue;
		}
		TechTypes const eFeaturePrereq = (eFeature == NO_FEATURE ? NO_TECH :
				kLoopBuild.getFeatureTech(eFeature));
		if (!isNearTech(eFeaturePrereq))
			continue;
		bCanTradeSoon = true;
		bCanImproveSoon = true;
		if (kTeam.isHasTech(eBuildPrereq) && kTeam.isHasTech(eFeaturePrereq))
		{
			bCanTrade = true;
			bCanImprove = true;
		}
		else if (bCanTrade) // Prefer currently available build - regardless of yield
			continue;
		int iYieldValue = 0;
		bool bRemove = (eFeature != NO_FEATURE && kLoopBuild.isFeatureRemove(eFeature));
		FOR_EACH_ENUM(Yield) // Make sure we're not picking Fort over a yield improvement
		{
			iYieldValue += kImprovement.getYieldChange(eLoopYield) +
					kImprovement.getImprovementBonusYield(eBonus, eLoopYield);
			if (!bRemove && eFeature != NO_FEATURE)
				iYieldValue += GC.getInfo(eFeature).getYieldChange(eLoopYield);
		}
		if (iYieldValue > iBestYield)
		{
			eBestImprovement = eImprovement;
			iBestYield = iYieldValue;
			bRemoveFeature = bRemove;
		}
	}
	TechTypes eTradeTech = GC.getInfo(eBonus).getTechCityTrade();
	bCanTradeSoon = (bCanTradeSoon && isNearTech(eTradeTech));
	bCanTrade = (bCanTrade && bCanTradeSoon && kTeam.isHasTech(eTradeTech));
	/*  <advc.108> Depending on the NormalizationLevel, eBonus can be unrevealed
		when placing starting locations. */
	if (kSet.isStartingLoc() || kSet.isNormalizing())
	{
		TechTypes eRevealTech = GC.getInfo(eBonus).getTechReveal();
		if (!kTeam.isHasTech(eRevealTech))
		{
			bCanTrade = false;
			bCanImprove = false;
			if (!isNearTech(eRevealTech))
			{
				bCanTradeSoon = false;
				bCanImproveSoon = false;
			}
		}
	} // </advc.108>
	if (eBestImprovement == NO_IMPROVEMENT)
		return NO_IMPROVEMENT;
	FOR_EACH_ENUM(Yield)
	{
		aiYield[eLoopYield] = GC.getInfo(eBestImprovement).
				getImprovementBonusYield(eBonus, eLoopYield);
		/*	Note/ fixme: We don't count the improvement's YieldChange and
			IrrigatedYieldChange, i.e. we treat wet farms, dry farms and
			improvements that don't add any yield (plantation, pasture) all
			the same and thus overestimate the latter.
			This separate accounting for "special" yields really needs to go,
			and then CvPlot::calculateImprovementYieldChange could perhaps
			be used (for all plots). */
		if (!bRemoveFeature && eFeature != NO_FEATURE)
		{
			aiYield[eLoopYield] += GC.getInfo(eFeature).getYieldChange(eLoopYield);
			if (p.isRiver())
				aiYield[eLoopYield] += GC.getInfo(eFeature).getRiverYieldChange(eLoopYield);
		}
		else if (p.isRiver())
			aiYield[eLoopYield] += GC.getInfo(p.getTerrainType()).getRiverYieldChange(eLoopYield);
	}
	return eBestImprovement;
} // </advc.031>


bool AIFoundValue::isNearTech(TechTypes eTech) const
{
	return (eTech == NO_TECH || kTeam.isHasTech(eTech) ||
			kPlayer.getCurrentResearch() == eTech ||
			/*  <advc.108> With our first city, we can wait a bit a longer for the
				proper tech. (Not when starting in a later era though; research
				starts out slow then.) */
			(iCities <= 0 && eEra >= GC.getInfo(eTech).getEra() &&
			kGame.getStartEra() <= 0) || // </advc.108>
			/*	(The HasTech and CurrentResearch checks are redundant, I think,
				but faster.) */ kPlayer.canResearch(eTech));
}

// (not much pre-AdvCiv code left)
int AIFoundValue::calculateCultureModifier(CvPlot const& p, bool bForeignOwned,
	bool bShare, bool bCityRadius, bool bSteal, bool bFlip, bool bOwnExcl,
	int& iTakenTiles, int& iStealPercent) const
{
	scaled r = 100;
	/*  K-Mod note: iClaimThreshold is bigger for bEasyCulture and bAmbitious civs.
		Also note, if the multiplier was to be properly used for unowned plots,
		it would need to take into account the proximity of foreign cities and so on.
		(similar to the iForeignProximity calculation) */
	// advc.031: I'm including unowned plots, but only those in a foreign city radius.
	if ((!bForeignOwned && (bShare || !bCityRadius)) /* advc.035: */ || bFlip)
		return r.round();

	int iOurCulture = p.getCulture(ePlayer);
	int iOtherCulture = std::max(1,
			/*  advc.031: Could find out the owner of the bCityRadius
				city in the loop that computes abFlip, but it should be
				fine to assume that the owner has very little tile culture. */
			(!bForeignOwned ? 1 :
			p.getCulture(getRevealedOwner(p))));
	// <advc.031> Don't settle near rival capital (e.g. 2nd starting settler, OCC)
	if (bCityRadius && kGame.getElapsedGameTurns() <= 5)
		iOtherCulture = std::max(iOtherCulture, 200);
	CvCity* pForeignCity = p.getWorkingCity();
	if (bForeignOwned)
	{
		if ((pForeignCity != NULL && pForeignCity->isCapital()) ||
			// Likely to struggle with a single colony against multiple rival cities
			(iAreaCities <= 0 && p.getArea().getCitiesPerPlayer(getRevealedOwner(p)) > 1))
		{
			iOtherCulture = (3 * iOtherCulture) / 2;
		}
	} // </advc.031>
	r.mulDiv(iOurCulture + kSet.getClaimThreshold(), iOtherCulture + kSet.getClaimThreshold());
	if (!bOwnExcl) // advc.035: The above is OK if cities own their exclusive radius ...
	{	// <advc.031>
		// ... but w/o that rule, it's too optimistic when iOurCulture is small.
		r = (r + (iOurCulture * 100) / kSet.getClaimThreshold()) / 2;
	}
	// Take into account at least some factors that determine each side's culture rate
	scaled rRateModifier = 1;
	/*	Don't be _too_ optimistic against Barbarians - a civ (a rival - or us) will
		probably conquer pForeignCity eventually and might not raze it. */
	if (bForeignOwned && p.isBarbarian())
		rRateModifier *= fixp(1.55);
	else if(pForeignCity != NULL &&
		// advc.303: Barbarian borders won't expand
		!adjacentOrSame(p, *pForeignCity->plot()))
	{
		rRateModifier *= fixp(1.8);
	}
	if (!p.isArea(kArea))
		rRateModifier /= fixp(1.3);
	else if (pForeignCity != NULL && !pForeignCity->isArea(p.getArea()))
		rRateModifier *= fixp(1.3);
	/*  K-Mod had done *5/4 if EasyCulture; I think only free culture will really
		swing culture wars. */
	int iFreeForeignCulture = (bForeignOwned ? GET_PLAYER(getRevealedOwner(p)).
			getFreeCityCommerce(COMMERCE_CULTURE) : 0);
	if (pForeignCity != NULL && pForeignCity->isCapital())
	{
		/*  Tbd.: Should just use pForeignCity->getCommerceRate(COMMERCE_CULTURE).
			advc.045 hides foreign buildings, but it should, in theory, be possible
			to infer culture buildings from visible tile culture percentages.
			But will then also have to predict our own culture rate. */
		static BuildingTypes const eCapitalBuilding = GC.getInfo(
				pForeignCity->getCivilizationType()).
				getCivilizationBuildings(GC.getDefineINT("CAPITAL_BUILDINGCLASS"));
		if (eCapitalBuilding != NO_BUILDING)
		{
			iFreeForeignCulture += GC.getInfo(eCapitalBuilding).
					getCommerceChange(COMMERCE_CULTURE); // (normally 0)
			iFreeForeignCulture += GC.getInfo(eCapitalBuilding).
					getObsoleteSafeCommerceChange(COMMERCE_CULTURE);
		}
	}
	scaled const rFreeForeignCultureModifier(iFreeForeignCulture + 7, 7);
	// Extra pessimism about tiles that another civ is able to work (borders already expanded)
	if (bSteal)
	{
		rRateModifier = fixp(0.62);
		if (pForeignCity != NULL && adjacentOrSame(p, *pForeignCity->plot()))
			rRateModifier /= fixp(1.5);
		if (bForeignOwned)
			rRateModifier *= rFreeForeignCultureModifier;
	}
	if (adjacentOrSame(p, kPlot))
		rRateModifier *= fixp(1.5); // as in K-Mod
	else rRateModifier *= rFreeForeignCultureModifier;	
	if (bCityRadius && !bShare)
	{
		r *= rRateModifier * fixp(0.8);
		iStealPercent += std::min(75, r.round());
	}
	else r *= rRateModifier;
	// </advc.031>
	r.decreaseTo(100);
	// advc.031: Moved up
	if (r < (iAreaCities > 0 ? 25 : 50) &&
		!bSteal) // advc.031: Already counted as iTakenTiles
	{
		//discourage hopeless cases, especially on other continents.
		iTakenTiles += (iAreaCities > 0 ? 1 : 2);
	}
	// <advc.099b>
	if (!bCityRadius && bForeignOwned)
	{
		scaled rExclRadiusWeight = GC.AI_getGame().AI_exclusiveRadiusWeight(
				::plotDistance(&p, &kPlot));
		r *= 1 + rExclRadiusWeight;
		r.decreaseTo(100);
		// </advc.099b>  <advc.035>
		if (bOwnExcl)
		{
			// (The discouragement above is still useful for avoiding revolts)
			r.increaseTo(65);
		} // </advc.035>
	}
	return r.round();
}

// K-Mod: adjust for removable features (advc: moved into a subroutine)
int AIFoundValue::removableFeatureYieldVal(FeatureTypes eFeature,
	bool bRemovableFeature, bool bBonus) const
{
	int iR = 0;
	CvFeatureInfo const& kFeature = GC.getInfo(eFeature);
	FOR_EACH_ENUM(Yield)
	{
		if (bRemovableFeature)
			iR += 10 * kFeature.getYieldChange(eLoopYield);
		else if (kFeature.getYieldChange(eLoopYield) < 0)
		{
			iR -= (bBonus ? 25 : 5);
			// advc.031: was 30 *...
			iR += 25 * kFeature.getYieldChange(eLoopYield);
		}
	}
	IFLOG if(iR!=0) logBBAI("From (removable) feature yield: %d", iR);
	return iR;
}

/*	An estimate of how much production an improvement might add
	in the medium term if production is prioritized. Precision: times 100.
	Note: Any additional production from improving a bonus resource
	is counted as iSpecialProduction elsewhere. This function ignores
	bonus resources. */
scaled AIFoundValue::estimateImprovementProduction(CvPlot const& p,
	bool bPersistentFeature) const
{
	if (p.isWater())
	{
		// Tbd.: Should check for water improvements
		return 0;
	}
	//return (p.isHills() ? 200 : 100);
	/*  <advc.031> The above is pretty bad: We're not going to build
		Workshops everywhere, and it doesn't check for Peak or Desert. */
	FeatureTypes eFeature = p.getFeatureType();
	// If persistent, then production from feature is already counted above.
	if (eFeature != NO_FEATURE && !bPersistentFeature)
	{
		int iProductionChange = GC.getInfo(eFeature).getYieldChange(YIELD_PRODUCTION);
		if (iProductionChange > 0)
		{
			// 0.5 for chopping or Lumbermill (I shouldn't hardcode it like this ...)
			return iProductionChange + fixp(0.5);
		}
	}
	if (iCities <= 2)
	{
		scaled r;
		if(p.isHills())
			r += 2;
		return r;
	}
	scaled r;
	FOR_EACH_ENUM(Improvement)
	{
		// Not a perfectly safe way to check if we can build the improvement - but fast.
		if (kPlayer.getImprovementCount(eLoopImprovement) <= 0)
			continue;
		CvImprovementInfo const& kLoopImprovement = GC.getInfo(eLoopImprovement);
		int iYieldChange = kLoopImprovement.getYieldChange(YIELD_PRODUCTION) +
				kTeam.getImprovementYieldChange(eLoopImprovement, YIELD_PRODUCTION);
		// Will be less inclined to build improvement if it hurts other yields
		FOR_EACH_ENUM(Yield)
		{
			if (eLoopYield == YIELD_PRODUCTION)
				continue;
			int iOtherYield = kLoopImprovement.getYieldChange(eLoopYield);
			if (iOtherYield < 0)
				iYieldChange += iOtherYield;
		}
		/*  I'm not bothering with civics and routes here. It's OK to undercount
			b/c more production is needed by the time railroads become available.
			A Workshop may also remove a Forest; in that case, we're overcounting. */
		// Not fast; loops through all builds.
		if (iYieldChange <= 0 || !p.canHaveImprovement(eLoopImprovement, eTeam))
			continue;
		FAssertMsg(iYieldChange <= 3, "is this much production possible?");
		r.increaseTo(iYieldChange);
	}
	return r; // </advc.031>
}


int AIFoundValue::evaluateYield(int const* aiYield, CvPlot const* p,
	bool bCanNeverImprove) const
{
	int r = 0;
	int aiWeight[NUM_YIELD_TYPES] = {15, 15, 8 };
	// (note: these numbers have been adjusted for K-Mod)
	if (p != NULL && !p->isWater() && // advc.031: Exclude seafood
		(isHome(*p) || aiYield[YIELD_FOOD] >= GC.getFOOD_CONSUMPTION_PER_POPULATION())) 
	{
		r += 10;
		aiWeight[YIELD_FOOD] = 40;
		aiWeight[YIELD_PRODUCTION] = 30;
		aiWeight[YIELD_COMMERCE] = 20;
		/*if (kSet.isStartingLoc())
			r *= 2;*/ // BtS
	}
	else if (aiYield[YIELD_FOOD] == GC.getFOOD_CONSUMPTION_PER_POPULATION() - 1)
	{
		aiWeight[YIELD_FOOD] = 30;
		aiWeight[YIELD_PRODUCTION] = 25;
		aiWeight[YIELD_COMMERCE] = 12;
	}
	/*  <advc.108> For moving the starting Settler and for more
		early-game commerce in general */
	if(iCities <= 1 && eEra <= 0)
		aiWeight[YIELD_COMMERCE] += 5; // </advc.108>
	// <advc.303>
	if (bBarbarian)
	{
		aiWeight[YIELD_FOOD] -= 4;
		aiWeight[YIELD_PRODUCTION] += 5;
		aiWeight[YIELD_COMMERCE] -= 3;
	} // </advc.303>
	FOR_EACH_ENUM(Yield)
	{
		FAssert(aiWeight[eLoopYield] > 0); // advc.303
		int iYieldValue = aiYield[eLoopYield] * aiWeight[eLoopYield];
		/*	<advc.031> Mined resources (-1 production) get a too low value otherwise.
			See the comment at the end of getBonusImprovement. */
		if (iYieldValue < 0)
			iYieldValue /= 2; // </advc.031>
		r += iYieldValue;
	}
	if (p != NULL && p->isWater())
	{
		// K-Mod. kludge to account for lighthouse and lack of improvements.
		if (bCoastal)
		{
			r /= 2;
			r += 8 * (aiYield[YIELD_COMMERCE] + aiYield[YIELD_PRODUCTION]);
		}
		else r /= 3;
		if (kSet.isStartingLoc() && !bCoastal)
		{
			r -= 75; // advc.031: was -400 in BtS, -120 in K-Mod
			/*	(K-Mod comment: "I'm pretty much forbidding starting 1 tile
				inland non-coastal with more than a few non-lake water tiles.) */
		}
	}  // <advc.031>
	if (bCanNeverImprove)
		r = (r * 77) / 100; // </advc.031>
	return r;
}


int AIFoundValue::evaluateFreshWater(CvPlot const& p, int const* aiYield, bool bSteal,
	int& iRiverTiles, int& iGreenTiles) const
{
	int iR = 0;
	// <advc.053>
	bool bLowYield = (aiYield[YIELD_FOOD] + aiYield[YIELD_PRODUCTION] +
			aiYield[YIELD_COMMERCE] / 2 < 2); // </advc.053>
	if (p.isRiver())
	{
		//iR += 10; // BtS
		// <K-Mod>
		//iR += (kSet.isExtraYieldThreshold() || kSet.isStartingLoc()) ? 30 : 10;
		//iR += (pPlot->isRiver() ? 15 : 0); // </K-Mod>
		// advc: Replaced by the code below
		// <advc.053>
		if (bLowYield)
		{
			if (kSet.isExtraYieldThreshold())
				iR += 9;
			// advc.908a>
			if (kSet.isExtraYieldNaturalThreshold())
				iR += 5; // </advc.908a>
		}
		else // </advc.053>
		{
			// <advc.031>
			if (kSet.isExtraYieldThreshold())
				iR += 13;
			// <advc.908a>
			if (kSet.isExtraYieldNaturalThreshold())
				iR += 8; // </advc.908a>
			if (!bSteal)
			{
				iRiverTiles++;
				if (iCities <= 0) // advc.108
					iR += 10;
				/*  I'm guessing this K-Mod clause is supposed to
					steer the AI toward settling at rivers rather
					than trying to make all river plots workable. */
				if (kPlot.isRiver())
				{
					iR += (/* advc.108: */ iCities <= 0
							? 10 : 4);
				}
			} // </advc.031>
		}
	}  // in addition:
	if (p.canHavePotentialIrrigation() && /* advc.053: */ !bLowYield)
	{
		// <advc.031> was 5/5
		iR += 4;
		if (p.isFreshWater())
		{
			iR += 6;
			if (aiYield[YIELD_FOOD] >= GC.getFOOD_CONSUMPTION_PER_POPULATION() &&
				!bSteal)
			{
				iGreenTiles++;
			}
		} // <advc.031>
	}
	return iR;
}

/*	<advc.031> A plot next to a resource will usually have a higher found value
	than the resource plot itself because of the improvement yields counted by
	evaluateSpecialYields. But not always - it depends on what else is in the
	city radius. Founding on a resource usually cannibalizes other potential
	city sites, so it needs to be discouraged a bit. */
int AIFoundValue::foundOnResourceValue(int const* aiBonusImprovementYield) const
{
	int r = -5;
	if (aiBonusImprovementYield == NULL)
		r -= 42; // When we can't currently improve the resource
	else
	{
		int iImprovementYieldValue = evaluateYield(aiBonusImprovementYield);
		if (iImprovementYieldValue > 0) // Make sure not to exponentiate a negative value
			r -= (scaled(iImprovementYieldValue).pow(fixp(1.5)) / fixp(4.2)).round();
	}
	/*	In (historical) scenarios, resources are sometimes placed just so that the AI
		doesn't settle in a particular tile. Try -a little bit- to respect that. */
	if (kGame.isScenario())
		r -= 13;
	IFLOG logBBAI("%d for founding on resource", r);
	return r;
} // </advc.031>


int AIFoundValue::applyCultureModifier(CvPlot const& p, int iPlotValue, int iCultureModifier,
	bool bShare) const
{
	scaled r = iPlotValue;
	r *= per100(iCultureModifier);
	// <advc.031>
	if (bShare) // bSteal is already factored into iCultureModifier
		r *= fixp(0.375);
	// </advc.031>
	return r.round();
}

// Note: aiBonusCount is only a partial count (resources evaluated up to this point)
int AIFoundValue::nonYieldBonusValue(CvPlot const& p, BonusTypes eBonus,
	bool bCanTrade, bool bCanTradeSoon, bool bEasyAccess, bool& bAnyGrowthBonus,
	std::vector<int>* paiBonusCount, int iCultureModifier) const
{
	/*int r = kPlayer.AI_bonusVal(eBonus, 1, true) * (!kSet.isStartingLoc() &&
			kPlayer.getNumTradeableBonuses(eBonus) == 0 && aiBonusCount[eBonus] == 1 ?
			80 : 20);*/ // BtS
	/*int iCount = kPlayer.getNumTradeableBonuses(eBonus) == 0 + aiBonusCount[eBonus];
	int r = AI_bonusVal(eBonus, 0, true) * 80 / (1 + 2*iCount);*/ // K-Mod
	/*  <advc.031> The "==0" looks like an error. Rather than correct that,
		I'll let AI_bonusVal handle the number of bonuses already connected (iChange=1).
		A division by NumTradeableBonuses here won't work well for strategic resources.*/
	// Coefficient was 80
	scaled r = kPlayer.AI_bonusVal(eBonus, 1, true) * 57;
	bool bSurplus = (kPlayer.getNumAvailableBonuses(eBonus) > 0);
	if (paiBonusCount != NULL)
	{
		if ((*paiBonusCount)[eBonus] > 0)
		{
			r /= 1 + (*paiBonusCount)[eBonus];
			bSurplus = true;
		} // </advc.031>
		(*paiBonusCount)[eBonus]++;
	}
	// <advc.031> (Would be cleaner to handle this in CvPlayerAI::AI_baseBonusVal.)
	bool bGrowthBonus = (!bAnyGrowthBonus && bCanTradeSoon && !bSurplus &&
			(GC.getInfo(eBonus).getHappiness() +
			// Basically only luxury resources qualify
			GC.getInfo(eBonus).getHealth() / 2 > 0) &&
			(bCanTrade || p.getFeatureType() == NO_FEATURE ||
			GC.getInfo(p.getFeatureType()).getHealthPercent() >= 0));
	if (bGrowthBonus) // Reward only the first new luxury
		bAnyGrowthBonus = true;
	// </advc.031>
	/*  K-Mod: try not to make the value of strategic resources too overwhelming.
		(note: I removed a bigger value reduction from the original code.) */
	scaled rEarlyGameModifier = 1;
	if (kSet.isStartingLoc())
	{	// <advc.031>
		if (bGrowthBonus)
			rEarlyGameModifier = fixp(0.4); // </advc.031>
		else
		{
			// (advc: Divisor was 4 in K-Mod; BtS had divided by 2 after evaluateSpecialYields.)
			rEarlyGameModifier = 
				/*  <advc.108> Don't need to decrease as much if reveal-techs are respected
						(also: advc.036 improves the evaluation of non-strategic resources) */
					(kGame.getStartingPlotNormalizationLevel() <= CvGame::NORMALIZE_LOW ?
					fixp(1/3.) : fixp(1/4.));
		}
	}
	else if (iCities <= 0) // For moving the starting Settler and normalization
	{
		if (bGrowthBonus)
			rEarlyGameModifier = fixp(0.75);
		else rEarlyGameModifier = fixp(0.55);
	} // </advc.108>
	// <advc.031> High values for strategic resources remain a problem during the early game
	/*	(note): Instead of special treatment just for the early game, the multiplier
		should arguably be based on an estimate of how many cities we'll have
		in some medium term - b/c AI_bonusVal is per city. */
	else
	{
		int const iTargetCities = GC.getInfo(GC.getMap().getWorldSize()).getTargetNumCities();
		if (iCities + 1 < iTargetCities)
		{
			FAssert(iTargetCities >= 3);
			if (bGrowthBonus) // Modifier climbs to 120%, then decreases to 100%.
			{
				int iPeakCity = (iTargetCities + 1) / 2;
				scaled rIncrement = fixp(0.3) / std::max(1, iPeakCity - 1);
				rEarlyGameModifier = fixp(0.9) + rIncrement *
						(iCities < iPeakCity ? iCities : iTargetCities - iCities - 1);
			}
			else // Modifier climbs to 100%
			{
				scaled rIncrement = fixp(0.5) / std::max(1, iTargetCities - 1);
				rEarlyGameModifier = fixp(0.55) + rIncrement * iCities;
			}
		}
	}
	IFLOG if(rEarlyGameModifier.getPercent()!=100) logBBAI("Early-game modifier for non-yield resource value: %d percent", rEarlyGameModifier.getPercent());
	r *= rEarlyGameModifier;
	/*	(cf. getBonusImprovement)
		AI_bonusValue can check for tech requirements, but it can't check requirements
		for building the improvement. Hence bAssumeEnabled=true is used in the
		AI_bonusValue call above and we take care of tech requirements ourselves. */		
	if (!bCanTrade)
	{
		if (!bSurplus)
		{
			/*  Important for high-value strategic resources that get revealed
				long before they can be traded, especially Oil. Scanning the whole map
				through CvPlayerAI::AI_countOwnedBonuses is too expensive I think,
				but I'm copying the city bonus count from there. */
			FOR_EACH_CITYAI(pCity, kPlayer)
			{
				if (pCity->AI_countNumBonuses(eBonus, true, true, -1) > 0)
				{
					bSurplus = true;
					break;
				}
			}
		}
		IFLOG if(bSurplus) logBBAI("Surplus resource");
		if (bCanTradeSoon)
			r *= fixp(0.7);
		else r *= fixp(1/3.);
		if (bSurplus)
			r *= fixp(0.3);
		// <advc.040>
		if (!bEasyAccess)
		{
			/*  Might be better to place a city in p.area(). But if that area
				is tiny, then accessing the resource from a different landmass
				is probably our best bet. */
			r *= (p.getArea().getNumTiles() <= 2 ? fixp(0.6) : fixp(0.45));
		} // </advc.040>
		if (bSurplus)
			r.decreaseTo(125);
	} // </advc.031>
	if (kSet.isStartingLoc() /* advc.031e: */ || kSet.isNormalizing())
		return r.round();

	// K-Mod. (original code deleted)
	if (!isHome(p))
	{	/*  <advc.031> Why halve the value of water bonuses? Perhaps because
			they're costly to improve. But that's only true in the early game.
			Because they tend to be common? AI_bonusVal takes care of that. */
		if (p.isWater()/*) {//r /= 2;*/ && eEra < CvEraInfo::AI_getAgeOfExploration())
		{
			int iWaterPenalty = (CvEraInfo::AI_getAgeOfExploration() - eEra) * 16;
			r -= iWaterPenalty;
			r.increaseTo(0);
			IFLOG logBBAI("Penalty for water resource: %d", iWaterPenalty);
		}
		// iCultureModifier should have this covered
		/*if (getRevealedOwner(p) != ePlayer && ::stepDistance(&kPlot, &p) > 1) {
			if (!kSet.isEasyCulture())
				r *= fixp(0.75);
		}*/
		// advc.031: Don't ignore culture modifier < 60
		scaled rModifier = (kSet.isAmbitious() && iCultureModifier >= 60 ?
				fixp(1.1) : per100(iCultureModifier));
		r *= rModifier;
		IFLOG if(rModifier!=per100(iCultureModifier)) logBBAI("Non-yield resource value increased b/c of ambitious personality");
	}
	else if (kSet.isAmbitious())
		r *= fixp(1.1);
	// K-Mod end
	return r.round();
}


int AIFoundValue::calculateSpecialYieldModifier(int iCultureModifier, bool bEasyAccess,
	bool bBonus, bool bCanSoonImproveBonus, bool bCanImproveBonus) const
{
	scaled r = iCultureModifier;
	// </advc.040>
	if (!bEasyAccess)
		r /= 2; // <advc.040>
	// <advc.031>
	if (bBonus)
	{
		if (!bCanSoonImproveBonus)
		{
			// Don't want to discount e.g. Wine too much near capital
			r = (r * (kSet.isStartingLoc() ? 4 : 3)) / 10;	
		}
		else if (!bCanImproveBonus)
			r *= fixp(0.75);
	} // </advc.031>
	return r.round();
}


void AIFoundValue::calculateSpecialYields(CvPlot const& p,
	int const* aiBonusImprovementYield, int const* aiNatureYield,
	int iModifier, int* aiSpecialYield,
	int& iSpecialFoodPlus, int& iSpecialFoodMinus, int& iSpecialYieldTiles) const
{
	int aiBuildingYield[NUM_YIELD_TYPES];
	calculateBuildingYields(p, aiNatureYield, aiBuildingYield);
	int const iEffectiveFood = aiNatureYield[YIELD_FOOD] + aiBuildingYield[YIELD_FOOD];
	if (aiBonusImprovementYield == NULL) // K-Mod: non bonus related special food
	{
		int iSurplus = (std::max(0,
				iEffectiveFood - GC.getFOOD_CONSUMPTION_PER_POPULATION()) *
				per100(iModifier)).uround(); // advc.031
		iSpecialFoodPlus += iSurplus;
		aiSpecialYield[YIELD_FOOD] += iSurplus; // advc.031: A little extra love for Flood Plains
		return;
	}
	// advc.031: No need to recompute nature yield here
	int iSpecialFood = 
			((aiNatureYield[YIELD_FOOD] + aiBonusImprovementYield[YIELD_FOOD]) *
			per100(iModifier)).round(); // advc.031
	aiSpecialYield[YIELD_FOOD] += iSpecialFood;
	int iFoodTemp = iSpecialFood - GC.getFOOD_CONSUMPTION_PER_POPULATION();
	// advc.031:
	iFoodTemp = (iFoodTemp * per100(iModifier)).round();
	iSpecialFoodPlus += std::max(0, iFoodTemp);
	iSpecialFoodMinus -= std::min(0, iFoodTemp);
	// <advc.031>
	int iSpecialProd = aiNatureYield[YIELD_PRODUCTION] +
			aiBonusImprovementYield[YIELD_PRODUCTION] +
			aiBuildingYield[YIELD_PRODUCTION];
	int iSpecialComm = aiNatureYield[YIELD_COMMERCE] +
			aiBonusImprovementYield[YIELD_COMMERCE] +
			aiBuildingYield[YIELD_COMMERCE];
	/*  No functional change above. Now count the tile as special and
		apply culture modifier. */
	bool const bSpecial =  (iSpecialFood > 0 || iSpecialComm > 0 || iSpecialProd > 0);
	if (bSpecial)
		iSpecialYieldTiles++;
	/*  To avoid rounding all yields to 0, don't reduce production and commerce
		to less than 1. */
	iSpecialProd = std::max(std::min(1, iSpecialProd),
			(iSpecialProd * per100(iModifier)).round());
	aiSpecialYield[YIELD_PRODUCTION] += iSpecialProd;
	iSpecialComm = std::max(std::min(1, iSpecialComm),
			(iSpecialComm * per100(iModifier)).round());
	aiSpecialYield[YIELD_COMMERCE] += iSpecialComm;
	IFLOG if(bSpecial) logBBAI("Special yield: %dF%dP%dC (modifier: %d percent)",
			iSpecialFood, iSpecialProd, iSpecialComm, iModifier);
	// </advc.031>
}

// advc: Function for K-Mod's "lighthouse kludge"
void AIFoundValue::calculateBuildingYields(CvPlot const& p, int const* aiNatureYield,
	int* aiBuildingYield) const
{
	FOR_EACH_ENUM(Yield)
		aiBuildingYield[eLoopYield] = 0;
	if (bCoastal && p.isWater() &&
		aiNatureYield[YIELD_COMMERCE] > 1)
	{
		aiBuildingYield[YIELD_FOOD]++;
	}
}

/*	advc.031: Weighted sum. (Using floating-point math until such a time that a
	logarithm function gets added to ScaledNum.) */
int AIFoundValue::sumUpPlotValues(std::vector<int>& aiPlotValues) const
{
	std::sort(aiPlotValues.begin(), aiPlotValues.end(), std::greater<int>());
	// CITY_HOME_PLOT should have 0 value here, others could have negative values.
	FAssert(aiPlotValues[NUM_CITY_PLOTS - 1] <= 0);
	double dMaxMultPercent = 153;
	double dMinMultPercent = 47;
	if (iCities <= 0) // Capital will grow large
	{
		dMaxMultPercent -= 8;
		dMinMultPercent += 8;
	}
	double const dNormalizMult = 1;
	double const dSubtr = 29;
	double const dExp = std::log(dMaxMultPercent - dMinMultPercent) /
			std::log(NUM_CITY_PLOTS - 1.0);
	int iR = 0;
	FOR_EACH_ENUM(CityPlot)
	{
		int iPlotValue = aiPlotValues[eLoopCityPlot];
		if (iPlotValue > 0)
		{
			iPlotValue = std::max(iPlotValue / 3,
					fmath::round(std::max(0.0, iPlotValue - dSubtr) * 0.01 *
					// Linearly decreasing multiplier:
					/*(maxMultPercent - i * ((maxMultPercent -
					minMultPercent) / (NUM_CITY_PLOTS - 1))));*/
					// Try power law instead:
					dNormalizMult * (dMinMultPercent + std::pow((double)
					std::abs(NUM_CITY_PLOTS - 1 - eLoopCityPlot), dExp))));
		}
		iR += iPlotValue;
	}
	IFLOG logBBAI("Weighted sum of plot values:\n+%d", iR);
	return iR;
}

/*	Note: aiSpecialYield includes aiNatureYield. Thus, nature yield is counted twice:
	once in evaluateYield, a second time in evaluateSpecialYield. This was already
	the case in BtS and it might work out more or less correctly on the bottom line,
	but it's messy. */
int AIFoundValue::evaluateSpecialYields(int const* aiSpecialYield,
	int iSpecialYieldTiles, int iSpecialFoodPlus, int iSpecialFoodMinus) const
{
	/*return iSpecialFood*50+iSpecialProduction*50+iSpecialCommerce*50;
	if (kSet.isStartingLoc())
		r /= 2;*/ // BtS
	/*	K-mod. It's tricky to get this right. Special commerce is great
		in the early game, but not so great later on. Food is always great -
		unless we already have too much.
		iSpecialFood is whatever food happens to be associated with bonuses.
		Don't value it highly, because it's also counted in a bunch of other ways. */
	//return iSpecialFood*20+iSpecialProduction*40+iSpecialCommerce*35;
	// <advc.031>
	scaled arWeight[NUM_YIELD_TYPES] = {
			// advc.108: So that less food gets placed during normalization - hopefully.
			kSet.isStartingLoc() ? fixp(0.45) :
			fixp(0.24),
			fixp(0.36),
			/*  advc.108: For moving the starting Settler. Though a commercial
				resource at the second city is also valuable, so: */
			iCities <= 1 && eEra <= 0 ? fixp(0.48) : fixp(0.32)};
	// <advc.031f> When there will be no normalization
	if (kSet.isStartingLoc() && kSet.isScenario())
	{
		arWeight[YIELD_FOOD] *= 2;
		arWeight[YIELD_PRODUCTION] *= fixp(1.7);
		arWeight[YIELD_COMMERCE] *= fixp(1.4);
	} // </advc.031f>
	scaled const rDiv = iSpecialYieldTiles;
	scaled rFromSpecial;
	FOR_EACH_ENUM(Yield)
		rFromSpecial += (aiSpecialYield[eLoopYield] / rDiv) * arWeight[eLoopYield];
	if(rFromSpecial > 0)
		rFromSpecial = rFromSpecial.pow(fixp(1.5)) * 75 * iSpecialYieldTiles;
	// advc.031: Apply the BtS/K-Mod food modifier only to the special yield value
	int iFoodSurplus = std::max(0, iSpecialFoodPlus - iSpecialFoodMinus);
	int iFoodDeficit = std::max(0, iSpecialFoodMinus - iSpecialFoodPlus);
	/*r *= 100 + 20 * std::max(0, std::min(iFoodSurplus, 2 * GC.getFOOD_CONSUMPTION_PER_POPULATION()));
	r /= 100 + 20 * std::max(0, iFoodDeficit);*/ // BtS
	// K-Mod. (note that iFoodSurplus and iFoodDeficit already have the "max(0, x)" built in.
	/*r *= 100 + (kSet.isExpansive() ? 20 : 15) * std::min(
			(iFoodSurplus + iSpecialFoodPlus)/2,
			2 * GC.getFOOD_CONSUMPTION_PER_POPULATION());
	r /= 100 + (kSet.isExpansive() ? 20 : 15) * iFoodDeficit;*/ // K-Mod end
	// Turn it into a single multiplier 'rFoodModifier' ...
	scaled rFoodWeight = fixp(0.15);
	if (kSet.isExpansive())
		rFoodWeight += fixp(0.05);
	scaled rSurplusMean(iFoodSurplus + iSpecialFoodPlus, 2);
	rSurplusMean.decreaseTo(2 * GC.getFOOD_CONSUMPTION_PER_POPULATION());
	scaled rFoodModifier = (1 + rFoodWeight * rSurplusMean) /
			(1 + rFoodWeight * iFoodDeficit);
	// ... and reduce the impact b/c of the new food modifier in adjustToFood
	if (!kSet.isStartingLoc())
		rFoodModifier = (rFoodModifier + 2) / 3;
	/*	Starting sites are exempt from adjustToFood. Mostly don't want them
		to be exempt from the special food adjustment. */
	else rFoodModifier = (rFoodModifier + fixp(0.5)) / fixp(1.5);
	int iResult = (rFromSpecial * rFoodModifier).round();
	IFLOG logBBAI("+%d from special yields %dF%dP%dC (food surplus modifier: %d percent)", iResult,
			aiSpecialYield[YIELD_FOOD], aiSpecialYield[YIELD_PRODUCTION], aiSpecialYield[YIELD_COMMERCE],
			rFoodModifier.getPercent());
	return iResult;
	// </advc.031>
}


bool AIFoundValue::isTooManyTakenTiles(int iTaken, int iResourceValue,
	bool bLowValue) const
{
	return (((iTaken > NUM_CITY_PLOTS / 3 ||
			(bBarbarian && iTaken > 2)) &&// advc.303
			iResourceValue < 250 && bLowValue) ||
			/* <advc.031> */ (iTaken > (2 * NUM_CITY_PLOTS) / 3 &&
			iResourceValue < 800)); // </advc.031>
}

/*	advc.031: Unlike the food modifier in evaluateSpecialYields, this modifier applies
	to all yields and takes into account grassland farms.*/
int AIFoundValue::adjustToFood(int iValue, int iSpecialFoodPlus, int iSpecialFoodMinus,
	int iGreenTiles) const
{
	scaled rLowFoodModifier = 1;
	if (eEra < CvEraInfo::AI_getAgeOfFertility())
	{
		int iSpecialSurplus = (iSpecialFoodPlus - iSpecialFoodMinus + 1) / 2; // ceil
		rLowFoodModifier = (fixp(8.5) + iGreenTiles + iSpecialSurplus) / fixp(11.5);
		rLowFoodModifier.clamp(fixp(0.5), 1);
	}
	IFLOG if(rLowFoodModifier.getPercent()!=100) logBBAI("Times %d percent for lack of food "
			"(special food +/-: %d/%d, green tiles: %d)", rLowFoodModifier.getPercent(),
			iSpecialFoodPlus, iSpecialFoodMinus, iGreenTiles);
	return (iValue * rLowFoodModifier).round();
}

// (adjustToBadHealth deals with short-term health)
int AIFoundValue::evaluateLongTermHealth(int& iHealthPercent) const
{
	int r = 0;
	int iFreshWaterHealth = 0;
	if (kPlot.isFreshWater())
	{
		iFreshWaterHealth = GC.getDefineINT(CvGlobals::FRESH_WATER_HEALTH_CHANGE);
		iHealthPercent += 100 * iFreshWaterHealth; // advc.031
	}
	//iValue += (iHealth / 5);
	/*  <advc.031> The above may have accounted for feature production; now
		evaluated separately elsewhere. */
	if (iHealthPercent > 0 || eEra >= CvEraInfo::AI_getAgeOfPestilence())
		r += std::min(iHealthPercent, 350) / 6;
	// Extra bonus for persistent health (as in BtS/ K-Mod): // </advc.031> 
	r += iFreshWaterHealth * 30;
	// (K-Mod (commented this out, compensated by the river bonuses I added.)
	/*if (iFreshWaterHealth > 0)
		r += 40;*/
	IFLOG if(r!=0) logBBAI("+%d from %d/100 health", r, iHealthPercent);
	return r;
}

// advc.031:
int AIFoundValue::evaluateFeatureProduction(int iProduction) const
{
	/*  Can't chop in the very early game (would be nicer to check for
		feature removal tech and sufficient workers than to go by era) */
	scaled r = iProduction * 3;
	if (rAIEraFactor <= 0)
		r /= 4;
	else r /= rAIEraFactor + 2;
	IFLOG if(r!=0) logBBAI("+%d from %d feature production", r, iProduction);
	return r.round();
}


int AIFoundValue::evaluateSeaAccess(bool bGoodFirstColony, scaled rProductionModifier,
	int iLandTiles) const
{
	int iR = 0;
	// <advc.303>
	if (bBarbarian)
	{
		iR += 350;
		IFLOG logBBAI("+%d for coastal (Barbarian)", iR);
		return iR;
	} // </advc.303>
	//if (kSet.isStartingLoc())
	if (/* advc.108: */ iCities <= 0)
	{
		// BtS: "let other penalties bring this down."
		iR += (kSet.isStartingLoc() ? 360 // advc.031: was 600 in BtS, 500 in K-Mod
				: 200); // advc.031: Less when normalizing or moving 1st settler
		if (!kSet.isNormalizing() && kArea.getNumStartingPlots() <= 0)
		{
			// advc.031: An inland sea will probably do an isolated civ no good
			if (GC.getMap().findBiggestArea(true) == kPlot.waterArea(true))
				iR += 450; // advc.031: was 1000 in BtS, 600 in K-Mod
		}
		IFLOG logBBAI("+%d for coastal (1st city)", iR);
		return iR;
	}
	if (kArea.getCitiesPerPlayer(ePlayer) <= 0)
	{
		//r += (iResourceValue > 0) ? 800 : 100; // (BtS)
		// K-Mod replacement:
		//r += iResourceValue > 0 ? (kSet.isSeafaring() ? 600 : 400) : 100;
		// advc.040: Mostly handled by the bFirstColony code elsewhere now
		if (bGoodFirstColony)
		{
			iR += 250;
			IFLOG logBBAI("+%d for promising first colony", iR);
		}
		return iR + 60; // advc.031: For trade routes, ability to produce ships
	}
	/*  BETTER_BTS_AI_MOD, Settler AI, 02/03/09, jdog5000: START
		(edited by K-Mod) */
	// Push players to get more coastal cities so they can build navies
	CvArea* pWaterArea = kPlot.waterArea(true);
	if (pWaterArea != NULL)
	{
		//120 + (kSet.isSeafaring() ? 160 : 0);
		iR += (kSet.isSeafaring() ? 150 : 100); // advc.031
		if (kTeam.AI_isWaterAreaRelevant(*pWaterArea) &&
			/*  advc.031: Don't worry about coastal production if we
				already have many coastal cities. */
			kPlayer.countNumCoastalCities() <= iCities / 3)
		{
			//iR += 120 + (kSet.isSeafaring() ? 160 : 0);
			iR += (kSet.isSeafaring() ? 240 : 125); // advc.031
			/*if (kPlayer.countNumCoastalCities() < iCities / 4 ||
				kPlayer.countNumCoastalCitiesByArea(kPlot.getArea()) == 0)*/
			if (// advc.031: Disabled this clause
				//kPlayer.countNumCoastalCities() < iCities / 4 ||
				(kPlot.getArea().getCitiesPerPlayer(ePlayer) > 0 &&
				kPlayer.countNumCoastalCitiesByArea(kPlot.getArea()) == 0))
			{
				iR += 200;
			}
		}
	}  // <advc.031>
	// Modify based on production (since the point is to build a navy)
	scaled rMult = rProductionModifier;
	if (GC.getInitCore().isPangaea())
		rMult /= 2;
	iR = (iR * rMult).round();
	// Encourage canals
	if (pWaterArea != NULL &&
		/*  ... but not if there is so little land that some city
			will probably create a canal in any case */
		iLandTiles >= 8)
	{
		CvArea* pWater2 = kPlot.secondWaterArea();
		if (pWater2 != NULL && pWater2 != pWaterArea)
		{
			int iSz1 = pWaterArea->getNumTiles();
			int iSz2 = pWater2->getNumTiles();
			int iSizeFactor = std::min(30, std::min(iSz1, iSz2));
			if (iSizeFactor >= GC.getDefineINT(CvGlobals::MIN_WATER_SIZE_FOR_OCEAN))
			{
				iR += 9 * iSizeFactor;
				IFLOG logBBAI("Connecting waterbodies of at least size %d", iSizeFactor);
			}
		}
	} // </advc.031>
	iR += 50; // advc: as in K-Mod (was 200 in BBAI)
	// BETTER_BTS_AI_MOD: END
	IFLOG logBBAI("+%d from coastal", iR);
	return iR;
}

/*  advc: Should perhaps merge this with the diploFactor code in adjustToCivSurroundings.
	Could then also add a chokepoint evaluation. */
int AIFoundValue::evaluateDefense() const
{
	if (bBarbarian) // advc.031: Don't make Barbarian cities too difficult to assail
		return 0;
	int iR = 0;
	if (kPlot.isHills())
	{
		/*  advc.031: Was 100+100 in K-Mod, 200 flat in BtS. Reduced b/c
			counted again for diploFactor below. */
		iR += 75 + (kSet.isDefensive() ? 75 : 0);
		IFLOG logBBAI("+%d from hill defense", iR);
	}
	return iR;
}


int AIFoundValue::evaluateGoodies(int iGoodies) const
{
	return iGoodies * 50;
}

/*	advc.027: Starting near a mountain chain that separates a landmass
	into two sizable areas is bad b/c normalization may (or may not)
	remove that obstacle; makes the site difficult to evaluate. */
int AIFoundValue::adjustToLandAreaBoundary(int iValue) const
{
	/*	Change advc.030 makes this check easy to implement. Can't do it
		if that's disabled. */
	if (!GC.getDefineBOOL(CvGlobals::PASSABLE_AREAS))
		return iValue;
	std::set<int> otherLandAreas;
	bool bFoundImpassable = false;
	int const iReprArea = kArea.getRepresentativeArea();
	/*	Range corresponds to CvGame::normalizeRemovePeaks. Need to go one farther
		b/c the boundary itself takes up one tile and could belong to kArea. */
	int const iPeakRemovalRange = 3;
	for (SquareIter itPlot(kPlot, iPeakRemovalRange + 1); itPlot.hasNext(); ++itPlot)
	{
		if (!itPlot->isArea(kArea) &&
			itPlot->getArea().getRepresentativeArea() == iReprArea)
		{
			otherLandAreas.insert(itPlot->getArea().getID());
		}
		if (itPlot->isImpassable() && itPlot.currStepDist() <= iPeakRemovalRange)
			bFoundImpassable = true;
	}
	if (!bFoundImpassable)
		return iValue;
	int iOtherLandAreaSize = 0;
	for (std::set<int>::const_iterator it = otherLandAreas.begin();
		it != otherLandAreas.end(); ++it)
	{
		iOtherLandAreaSize += GC.getMap().getArea(*it)->getNumTiles();
	}
	if (iOtherLandAreaSize <= 0)
		return iValue;
	int iAreaSize = kArea.getNumTiles();
	scaled rAdjust;
	if (iOtherLandAreaSize >= iAreaSize)
	{
		rAdjust = scaled(iAreaSize, iOtherLandAreaSize);
		rAdjust.increaseTo(fixp(1/4.));
	}
	else rAdjust = 1 - scaled(iOtherLandAreaSize, 2 * iAreaSize);
	return (iValue * rAdjust).round();
}

// Taking into account tiles beyond the city radius
int AIFoundValue::adjustToStartingSurroundings(int iValue) const
{
	int iR = iValue;
	int iGreaterBadTile = 0;
	int const iRange = 6; // K-Mod (was 5)
	for (SquareIter it(kPlot, iRange); it.hasNext(); ++it)
	{
		CvPlot const& p = *it;
		if ((p.isWater() || p.isArea(kArea)) && it.currPlotDist() <= iRange)
		{
			/*int iTempValue = (p->getYield(YIELD_FOOD) * 15);
			iTempValue += (p->getYield(YIELD_PRODUCTION) * 11);
			iTempValue += (p->getYield(YIELD_COMMERCE) * 5);
			r += iTempValue;
			if (iTempValue < 21) {
				iGreaterBadTile += 2;
				if (p->isFeature()) {
					if (p->calculateBestNatureYield(YIELD_FOOD, eTeam) > 1)
						iGreaterBadTile--;
				}
			}*/ // BtS
			// K-Mod
			int iTempValue = 0;
			iTempValue += p.getYield(YIELD_FOOD) * 9;
			iTempValue += p.getYield(YIELD_PRODUCTION) * 5;
			iTempValue += p.getYield(YIELD_COMMERCE) * 3;
			iTempValue += p.isRiver() ? 1 : 0;
			iTempValue += p.isWater() ? -2 : 0;
			if (iTempValue < 13)
			{
				/*	3 points for unworkable plots (desert, ice, far-ocean)
					2 points for bad plots (ocean, tundra)
					1 point for fixable bad plots (jungle) */
				iGreaterBadTile++;
				if (p.calculateBestNatureYield(YIELD_FOOD, eTeam) < 2)
				{
					iGreaterBadTile++;
					if (iTempValue <= 0)
						iGreaterBadTile++;
				}
			}
			if (p.isWater() || p.isArea(kArea))
				iR += iTempValue;
			else if (iTempValue >= 13)
				iGreaterBadTile++; // add at least 1 badness point for other islands.
			// K-Mod end
		}
	}
	IFLOG logBBAI("+%d from surroundings", iR - iValue);
	if (kSet.isNormalizing())
		return iR;
	/*iGreaterBadTile /= 2;
	if (iGreaterBadTile > 12) {
		r *= 11;
		r /= iGreaterBadTile;
	}*/ // BtS
	// K-Mod. note: the range has been extended, and the 'bad' counting has been rescaled.
	iGreaterBadTile /= 3;
	int iGreaterRangePlots = 2 * (SQR(iRange) + iRange) + 1;
	int iGreaterRangeFactor = iGreaterRangePlots / 6;
	if (iGreaterBadTile > iGreaterRangeFactor)
	{
		iR *= iGreaterRangeFactor;
		iR /= iGreaterBadTile;
		IFLOG logBBAI("Times %d/%d for bad tiles in the greater range", iGreaterRangeFactor, iGreaterBadTile);
	}

	// Maybe we can make a value adjustment based on the resources and players currently in this area
	// (wip)
	// advc.031: Deleted. This should be the responsibility of CvPlayer::findStartingAreas.

	/*  advc: Unused BtS and K-Mod code dealing with WaterCount and
		MinOriginalStartDist deleted */

	int const iTempValue = iR; // advc.031c
	int iMinDistanceFactor = MAX_INT;
	int const iMinRange = //startingPlotRange();
			kGame.getStartingPlotRange(); // advc.opt (now cached)
	//r *= 100; // (disabled by K-Mod to prevent int overflow)
	for (PlayerIter<CIV_ALIVE> it; it.hasNext(); ++it)
	{
		CvPlayer const& kOther = *it;
		if (kOther.getID() == ePlayer)
			continue;
		int iClosenessFactor = kOther.startingPlotDistanceFactor(kPlot, ePlayer, iMinRange);
		iMinDistanceFactor = std::min(iClosenessFactor, iMinDistanceFactor);
		if (iClosenessFactor < 1000)
		{
			iR *= 2000 + iClosenessFactor;
			iR /= 3000;
		}
	}
	if (iMinDistanceFactor > 1000)
	{
		//give a maximum boost of 25% for somewhat distant locations, don't go overboard.
		iMinDistanceFactor = std::min(1500, iMinDistanceFactor);
		iR *= (1000 + iMinDistanceFactor);
		iR /= 2000;
	}
	else if (iMinDistanceFactor < 1000)
	{
		//this is too close so penalize again.
		iR *= iMinDistanceFactor;
		iR /= 1000;
		/*iR *= iMinDistanceFactor;
		iR /= 1000;*/
		// <advc.031> Squaring the iMinDistanceFactor/1000 ratio is too drastic
	}
	if (iMinDistanceFactor < 666)
	{
		iR *= iMinDistanceFactor;
		iR /= 666;
	} // </advc.031>
	IFLOG logBBAI("%d from distance to other players", iR - iTempValue);
	return iR;
}

/*	advc.027:  (Not sure how to name this function. It's supposed to encourage
	-some- strong tiles in the first ring of tiles outside the city radius
	in order to make the choice whether to settle in place more interesting.) */
int AIFoundValue::adjustToStartingChoices(int iValue) const
{
	int iResources = 0;
	int iHighYield = 0;
	int iLowYield = 0;
	for (PlotCircleIter it(kPlot, CITY_PLOTS_RADIUS + 1, false); it.hasNext(); ++it)
	{
		if (it.currPlotDist() <= CITY_PLOTS_RADIUS)
			continue;
		CvPlot const& p = *it;
		// Off the cuff ...
		if (getBonus(p) != NO_BONUS)
		{
			iResources++; // Don't care about the yield or other specifics
			continue;
		}
		int iYieldVal = 0;
		FOR_EACH_ENUM(Yield)
		{
			iYieldVal += (eLoopYield == YIELD_COMMERCE ? 1 : 2) *
					p.calculateNatureYield(eLoopYield);
		}
		if (p.isRiver())
			iYieldVal++;
		if (iYieldVal > 4) // E.g. Plains tile as a baseline
			iHighYield++;
		else if (iYieldVal < 4)
			iLowYield++;
	}
	iLowYield = std::max(0, iLowYield - 4); // A few low-yield tiles aren't a problem
	// One resource and one high-yield tile is plenty
	int iModifier = std::min(10, 4 * iHighYield - 2 * iLowYield + 7 * iResources);
	if (iModifier < 0)
		iModifier /= 2;
	return (iValue * (100 + iModifier / 2)) / 100;
}


int AIFoundValue::adjustToProduction(int iValue, scaled rBaseProduction) const
{
	// K-Mod. reduce value of cities which will struggle to get any productivity.
	// <advc.040>
	if(bFirstColony)
	{
		rBaseProduction += scaled::max(iUnrevealedTiles * fixp(0.5),
				(rBaseProduction * iUnrevealedTiles) / NUM_CITY_PLOTS);
	} // </advc.040>
	rBaseProduction.increaseTo(GC.getInfo(YIELD_PRODUCTION).getMinCity()); // advc.031
	FAssert(!isRevealed(kPlot) ||
			// advc.test: I've seen this fail when there are Gems under Jungle (fixme)
			rBaseProduction >= GC.getInfo(YIELD_PRODUCTION).getMinCity());
	scaled rThreshold = fixp(8.5); // advc.031: was 9
	// <advc.303> Can't expect that much production from just the inner ring.
	if(bBarbarian)
		rThreshold = 4; // </advc.303>
	if (rBaseProduction < rThreshold)
	{
		iValue = ((iValue * rBaseProduction) / rThreshold).round();
		IFLOG logBBAI("Times (%d/%d) for low production", rBaseProduction.getPercent(), rThreshold.getPercent());
	} // K-Mod end
	return iValue;
}


int AIFoundValue::adjustToBarbarianSurroundings(int iValue) const
{
	int r = iValue;
	int const iRange = kSet.getBarbarianDiscouragedRange();
	if (iRange <= 0)
		return r;
	CvCity* pNearestCity = GC.getMap().findCity(iX, iY, NO_PLAYER);
	/*  <advc.303>, advc.300. Now that the outer ring isn't counted, I worry
		that an absolute penalty would reduce iValue to 0 too often. Also want
		to discourage touching borders a bit more, which the relative penalty
		should accomplish better.
		I don't see the need for special treatment of nearest city in a
		different area. CvGame avoids settling uninhabited areas anyway. */
	if (pNearestCity == NULL)
		pNearestCity = GC.getMap().findCity(iX, iY, NO_PLAYER, NO_TEAM, false);
	if (pNearestCity != NULL)
	{
		r *= std::min(iRange, plotDistance(iX, iY,
				pNearestCity->getX(), pNearestCity->getY()));
		r /= iRange;
		IFLOG if(iValue!=r) logBBAI("%d from %S being near a Barbarian site (discouraged range: %d)",
				r - iValue, cityName(*pNearestCity), iRange);
	}
	/*if (pNearestCity)
		r -= (std::max(0, (8 - plotDistance(iX, iY, pNearestCity->getX(), pNearestCity->getY()))) * 200);
	else {
		pNearestCity = GC.getMap().findCity(iX, iY, NO_PLAYER, NO_TEAM, false);
		if (pNearestCity != NULL) {
			int iDistance = plotDistance(iX, iY, pNearestCity->getX(), pNearestCity->getY());
			r -= std::min(500 * iDistance, (8000 * iDistance) / GC.getMap().maxPlotDistance());
		}
	}*/ // </advc.303>
	return r;
}


int AIFoundValue::adjustToCivSurroundings(int iValue, int iStealPercent) const
{
	// K-Mod. Adjust based on proximity to other players, and the shape of our empire.
	int iForeignProximity = 0;
	bool bFreeForeignCulture = false; // advc.031
	int iOurProximity = 0;
	CvCity const* pOurNearestCity = NULL;
	CvCity const* pNearestForeignCity = NULL; // advc.031
	int iMaxDistanceFromCapital = 0;
	for (PlayerIter<CIV_ALIVE,KNOWN_TO> it(eTeam); it.hasNext(); ++it)
	{
		CvPlayer const& kLoopPlayer = *it;
		if (kArea.getCitiesPerPlayer(kLoopPlayer.getID()) <= 0 ||
			GET_TEAM(kLoopPlayer.getTeam()).isVassal(eTeam))
		{
			continue;
		}
		int iProximity = 0;
		FOR_EACH_CITY(pLoopCity, /* *this */ kLoopPlayer) // advc.001: Not this player!
		{
			if (kLoopPlayer.getID() == ePlayer && pCapital != NULL)
			{
				iMaxDistanceFromCapital = std::max(iMaxDistanceFromCapital,
						plotDistance(pCapital->plot(), pLoopCity->plot()));
			}
			if (!pLoopCity->isArea(kArea))
				continue;
			// <advc.031> Don't cheat
			if (!kSet.isAllSeeing() && !kTeam.AI_deduceCitySite(*pLoopCity))
				continue; // </advc.031>
			int const iDistance = plotDistance(iX, iY,
					pLoopCity->getX(), pLoopCity->getY());
			if (kLoopPlayer.getID() == ePlayer)
			{
				if (pOurNearestCity == NULL ||
					iDistance < plotDistance(iX, iY,
					pOurNearestCity->getX(), pOurNearestCity->getY()))
				{
					pOurNearestCity = pLoopCity;
				}
			}
			// <advc.031>
			else if (kLoopPlayer.hasCapital())
			{
				if (pNearestForeignCity == NULL ||
					iDistance < plotDistance(iX, iY,
					pNearestForeignCity->getX(), pNearestForeignCity->getY()))
				{
					pNearestForeignCity = pLoopCity;
				}
			} // </advc.031>
			int iCultureRange = pLoopCity->getCultureLevel() + 3;
			if (iDistance <= iCultureRange && kTeam.AI_deduceCitySite(*pLoopCity))
			{
				// cf. culture distribution in CvCity::doPlotCultureTimes100
				iProximity += 90*(iDistance-iCultureRange)*(iDistance-iCultureRange)/
						(iCultureRange*iCultureRange) + 10;
			}
		}
		if (kLoopPlayer.getTeam() == eTeam)
			iOurProximity = std::max(iOurProximity, iProximity);
		else if (iProximity > iForeignProximity)
		{
			iForeignProximity = iProximity;
			// advc.031:
			bFreeForeignCulture = (kLoopPlayer.getFreeCityCommerce(COMMERCE_CULTURE) > 1);
		}
	}
	// Reduce the value if we are going to get squeezed out by culture.
	// Increase the value if we are hoping to block the other player!
	if (iForeignProximity > 0)
	{
		/*	As a rough guide of scale, settling 3 steps from a level 2 city
			in isolation would give a proximity of 24.
			4 steps from a level 2 city = 13
			4 steps from a level 3 city = 20 */
		int iDelta = iForeignProximity - iOurProximity;
		IFLOG logBBAI("Proximity difference (foreign minus ours): %d - %d = %d", iForeignProximity, iOurProximity, iDelta);
		if (iDelta > 50)
		{
			IFLOG logBBAI("Site disregarded: proximity difference too great");
			return 0; // we'd be crushed and eventually flipped if we settled here.
		}
		int const iTempValue = iValue; // advc.031
		bool bEasyCulture = (!bFreeForeignCulture && kSet.isEasyCulture()); // advc.031
		if (iDelta > -20 && iDelta <= (kSet.isAmbitious() ? 10 : 0) *
			(bEasyCulture ? 2 : 1))
		{
			/*	we want to get this spot before our opponents do.
				The lower our advantage, the more urgent the site is. */
			iValue *= 120 + iDelta/2 + (kSet.isAmbitious() ? 5 : 0)
					// advc.031: The 2nd city should focus more on high yields
					- (iCities <= 1 ? 12 : 0);
			iValue /= 100;
			/*  <advc.031> Don't rush to settle marginal spots (which might
				not even make the MinFoundValue cut w/o the boost above). */
			if (iTempValue < 2000)
			{
				iValue *= iTempValue;
				iValue /= 2000;
				iValue = std::max(iTempValue, iValue);
			} // </advc.031>
		}
		iDelta -= bEasyCulture ? 20 : 10;
		if (iDelta > 0)
		{
			iValue *= 100 - iDelta*3/2;
			iValue /= 100;
		}
		IFLOG if(iValue!=iTempValue) logBBAI("%d from foreign proximity", iValue - iTempValue);
		/*  <advc.031> This is not about being squeezed, but squeezing others
			and thereby angering them. StealPercent says how much we
			squeeze them (cultural strength is already taken into account). */
		if (iStealPercent >= 100)
		{
			/*  Between 130 (Alexander, G. Khan, Louis, Montezuma) and
				80 (Gandhi, Joao, Justinian). A leader who likes limited war
				should be less concerned about creating border troubles. */
			scaled rDiploFactor = (kPlayer.isHuman() && !kSet.isDebug() ? 100 :
					GC.getInfo(kPlayer.getPersonalityType()).getLimitedWarPowerRatio());
			if (kSet.isDefensive())
				rDiploFactor += 33;
			if (kPlot.isHills())
				rDiploFactor += 16;
			// The importance of a few stolen tiles decreases over time
			rDiploFactor += rAIEraFactor * 13;
			rDiploFactor = fixp(1.6) * rDiploFactor / iStealPercent;
			rDiploFactor.clamp(fixp(0.6), 1);
			iValue = (iValue * rDiploFactor).round();
			IFLOG logBBAI("Times %d percent (diplo modifier) from stealing %d/100 tiles",
					rDiploFactor.getPercent(), iStealPercent);
		} // </advc.031>
	}  // <advc.108> Avoid moving the starting settler far on crowded maps
	else if (iCities <= 0 && !kSet.isStartingLoc() && !kSet.isNormalizing() &&
		kPlayer.getStartingPlot() != NULL && &kPlot != kPlayer.getStartingPlot())
	{
		int iCivAlive = PlayerIter<CIV_ALIVE>::count();
		int iRecommended = kGame.getRecommendedPlayers();
		if (iCivAlive > iRecommended && iRecommended > 0)
		{
			int iDistFromStart = plotDistance(kPlayer.getStartingPlot(), &kPlot);
			if (iDistFromStart > 1)
			{
				scaled rMultiplier(iRecommended,
						iCivAlive + std::min(iDistFromStart, 5) - 1);
				IFLOG logBBAI("Times %d percent for moving starting Settler %d tiles on a crowded map",
						rMultiplier.getPercent(), iDistFromStart);
				iValue = (iValue * rMultiplier).round();
			}
		}
	} // </advc.108>
	// K-Mod end (the rest is original code - but I've made some edits...)

	if (pOurNearestCity != NULL)
	{
		int const iTempValue = iValue; // advc.031c
		int const iDistance = plotDistance(&kPlot, pOurNearestCity->plot());
		/*  advc: BtS code dealing with iDistance deleted;
			K-Mod comment: Close cities are penalised in other ways */
		// with that max distance, we could fit a city in the middle!
		int const iTargetRange = //(kSet.isExpansive() ? 6 : 5)
				/*	advc.031: Simply 5 unless a mod changes the city radius.
					Handle expansive setting below. */
				(5 + CITY_PLOTS_DIAMETER) / 2;
		int iNearestDistance = iDistance;
		/*	<advc.031> There can already be a city "in the middle" that iDistance
			doesn't account for - namely when it's a foreign city. */
		if (iNearestDistance > iTargetRange && pNearestForeignCity != NULL)
		{
			CvPlayer const& kNearestOwner = GET_PLAYER(pNearestForeignCity->getOwner());
			// (We've already ensured that they have a capital)
			CvPlot const& kTheirCapitalPlot = kNearestOwner.getCapital()->getPlot();
			int iForeignDistance = plotDistance(&kPlot, pNearestForeignCity->plot());
			if (iForeignDistance < iNearestDistance && pCapital != NULL &&
				(!kTheirCapitalPlot.isArea(kArea) ||
				3 * plotDistance(&kPlot, &kTheirCapitalPlot) >
				2 * plotDistance(&kPlot, pCapital->plot())))
			{
				iNearestDistance = (2 * iNearestDistance + 3 * iForeignDistance) / 5;
			}
		} // </advc.031>
		// K-Mod.
		/*  advc.031: Make expansive leaders indifferent about distance 5 vs. 6,
			but don't encourage greater distances. */
		if (iNearestDistance > iTargetRange +
			(kSet.isExpansive() ? 1 : 0)) // advc.031
		{
			int const iExcessDistance = std::min(iTargetRange,
					iNearestDistance - iTargetRange);
			//iValue -= iExcessDistance * 400;
			/*	<advc.031> Penalizing distance like this will lead to cities that aren't
				locally optimal. Can't really do anything about that here. Should perhaps
				be handled by AI_updateCitySites instead. */
			if (iExcessDistance > 0)
			{
				iValue -= 150;
				if (iExcessDistance > 1)
					iValue -= 250;
				if (iExcessDistance > 2)
					iValue -= (iExcessDistance - 2) * 325;
			} // </advc.031>
		}
		iValue *= 8 + 4 * iCities;
		// 5, not iTargetRange, because 5 is better. (advc: iTargetRange is 5 now)
		iValue /= 2 + 4 * iCities + std::max(iTargetRange, iDistance);
		IFLOG if(iTempValue!=iValue) logBBAI("%d from %d distance to %S",
				iValue - iTempValue, iDistance, cityName(*pOurNearestCity));

		if (!pOurNearestCity->isCapital() && pCapital != NULL)
		// K-Mod end
		{
			/*  Provide up to a 50% boost to value (80% for adv.start) for
				city sites which are relatively close to the core compared
				with the most distant city from the core (having a boost
				rather than distance penalty avoids some distortion).
				This is not primarily about maintenance but more about empire
				shape as such[, so] forbidden palace/state property are not
				[a] big deal. */ // advc: "so" added b/c the comment didn't make sense to me
			int iDistanceToCapital = ::plotDistance(pCapital->plot(), &kPlot);
			FAssert(iMaxDistanceFromCapital > 0);
			/*iValue *= 100 + (((kSet.isAdvancedStart() ? 80 : 50) * std::max(0, (iMaxDistanceFromCapital - iDistance))) / iMaxDistanceFromCapital);
			iValue /= 100;*/ // BtS
			/*  K-Mod. just a touch of flavour. (note, for a long time this
				adjustment used iDistance instead of iDistanceToCapital; and
				so I've reduced the scale to compensate) */
			/*int iShapeWeight = kSet.isAdvancedStart() ? 50 : (kSet.isAmbitious() ? 15 : 30);
			iValue *= 100 + iShapeWeight * std::max(0, iMaxDistanceFromCapital - iDistanceToCapital) / iMaxDistanceFromCapital;
			iValue /= 100 + iShapeWeight;*/
			// K-Mod end
			// <advc> I'm folding this into a single multiplier for easier debugging
			scaled const rShapeWeight = (kSet.isAdvancedStart() ? fixp(0.5) :
					(kSet.isAmbitious() ? fixp(0.15) : fixp(0.3)));
			scaled rShapeModifier = (1 + rShapeWeight * std::max(0,
					iMaxDistanceFromCapital - iDistanceToCapital) /
					iMaxDistanceFromCapital) / (1 + rShapeWeight);
			iValue = (iValue * rShapeModifier).round(); // </advc>
			IFLOG logBBAI("Times %d percent (shape modifier); distance from capital: %d, max. distance: %d",
					rShapeModifier.getPercent(), iDistanceToCapital, iMaxDistanceFromCapital);
		}
		return iValue;
	}
	pOurNearestCity = GC.getMap().findCity(iX, iY, ePlayer, eTeam, false);
	if (pOurNearestCity == NULL)
		return iValue;

	int iDistance = /* advc.031: */ std::min(GC.getMap().maxMaintenanceDistance(),
			::plotDistance(iX, iY, pOurNearestCity->getX(), pOurNearestCity->getY()));
	// <advc.031> Don't discourage settling on small nearby landmasses
	if (pCapital == NULL || pCapital->isArea(kArea) ||
		::plotDistance(&kPlot, pCapital->plot()) >= 10 ||
		kArea.getNumTiles() >= NUM_CITY_PLOTS)
	{
		//int iDistPenalty = 8000;
		int iDistPenalty = 5100 - (scaled::min(4, rAIEraFactor) * 775).round();
		// </advc.031> (no functional change below)
		iDistPenalty *= iDistance;
		iDistPenalty /= GC.getMap().maxTypicalDistance(); // advc.140: was maxPlotDistance
		iDistPenalty = std::min(500 * iDistance, iDistPenalty);
		iValue -= iDistPenalty;
		IFLOG logBBAI("%d from distance penalty (%d distance to %S)", iDistPenalty, iDistance, cityName(*pOurNearestCity));
	}

	return iValue;
}


int AIFoundValue::adjustToCitiesPerArea(int iValue) const
{
	// <advc.130v>
	if (kTeam.isCapitulated() || iCities <= 0)
		return iValue; // </advc.130v>

	if (kArea.getNumCivCities() <= 0) // advc.031: Had been counting Barbarian cities
	{
		//iValue *= 2;
		// K-Mod: presumably this is meant to be a bonus for being the first on a new continent.
		// But I don't want it to be a bonus for settling on tiny islands, so I'm changing it.
		int const iModifier = range(100 * (kArea.//getNumTiles()
				getNumRevealedTiles(eTeam) // advc.031: Don't cheat
				- 15) / //15
				20 // req. 40 revealed tiles for the full bonus
				, 100, 200);
		iValue *= iModifier;
		iValue /= 100;
		// K-Mod end
		IFLOG if(iModifier!=100) logBBAI("Times %d for being the first to colonize this landmass", iModifier);
	}
	/*  advc.031: BtS code deleted that was supposed to discourage colonies on
		the home continents of other civs. */
	return iValue;
}


int AIFoundValue::adjustToBonusCount(int iValue,
	std::vector<int> const& aiBonusCount) const
{
	if (iCities > 0)
	{
		int iBonusCount = 0;
		/*  <advc.052> Count bonus in the city tile double, as settling on a bonus
			is especially greedy. (I think this section is about not grabbing all
			the resources with a single city when there are a lot of resources
			in one place.) */
		if (getBonus(kPlot) != NO_BONUS)
			iBonusCount++; // </advc.052>
		int iUniqueBonusCount = 0;
		FOR_EACH_ENUM(Bonus)
		{
			iBonusCount += aiBonusCount[eLoopBonus];
			iUniqueBonusCount += (aiBonusCount[eLoopBonus] > 0 ? 1 : 0);
		}
		scaled rModifier = 1; // advc: No functional change except rounding
		if (iBonusCount > 4) 
			rModifier.mulDiv(5, 1 + iBonusCount);
		/*else if (iUniqueBonusCount > 2) {
			iValue *= 5;
			iValue /= (3 + iUniqueBonusCount);
		}*/
		/*  <advc.031> I can see how multiple bonuses of the same type
			could help city specialization and thus shouldn't be discouraged as much,
			but iBonus < 5 (unique or not) shouldn't be discouraged at all. */
		if (iBonusCount + iUniqueBonusCount >= 10)
		{
			rModifier *= scaled::max(fixp(0.7),
					(1 - fixp(0.08) * (iBonusCount + iUniqueBonusCount - 9)));
		}
		iValue = (iValue * rModifier).round();
		IFLOG if(rModifier.getPercent()!=100) logBBAI("Times %d percent for high resource count (%d resources, %d unique)",
				rModifier.getPercent(), iBonusCount, iUniqueBonusCount);
	}
	if (!bBarbarian) // advc.303
	{
		int iDeadLockCount = countDeadlockedBonuses();
		if (kSet.isAdvancedStart() && iDeadLockCount > 0)
			iDeadLockCount += /*advc.031 (was 2):*/ 1;
		//iValue /= (1 + iDeadLockCount);
		// advc.031: Replacing the above, which is too harsh.
		iValue = (2 * iValue) / (2 + iDeadLockCount);
		IFLOG if(iDeadLockCount!=0) logBBAI("Times %d/%d for %d deadlocked resources", 2, 2 + iDeadLockCount, iDeadLockCount);
	}
	return iValue;
}


int AIFoundValue::adjustToBadTiles(int iValue, int iBadTiles) const
{
	scaled r = iValue;
	// <advc.040>
	if(bFirstColony)
		iBadTiles += iUnrevealedTiles / 2; // </advc.040>
	// <advc.031>
	if(iBadTiles > 0)
	{
		/*	A scenario is more likely to mix some very good tiles with a lot of
			bad ones. Better to be more conservative on regular maps. */
		scaled const rExponent = (kSet.isScenario() && !kSet.isStartingLoc() ?
				fixp(1.385) : fixp(1.5));
		r -= scaled(iBadTiles).pow(rExponent) * 100 *  // <advc.108>
				(fixp(1/3.) + (kSet.isStartingLoc() ?
				fixp(1/3.) : 0) + (iCities <= 0 ? fixp(1/3.) : 0)); // </advc.108>
		r.increaseTo(0);
	} // </advc.031>
	IFLOG if(r.round()!=iValue) logBBAI("%d from %d bad tiles too many", r.round() - iValue, iBadTiles);
	return r.round();
}

// advc.031: Stifling bad health needs to be discouraged rigorously
int AIFoundValue::adjustToBadHealth(int iValue, int iGoodHealth) const
{
	int iBonusHealth = 0;
	if (pCapital != NULL)
		iBonusHealth += pCapital->getBonusGoodHealth();
	if (iCities > 0) // Connection to the capital can be slow/costly in the early game
		iBonusHealth = std::min(iBonusHealth, (iBonusHealth * (1 + iCities)) / 4);
	int iBadHealth = -iGoodHealth/100 - iBonusHealth -
			GC.getInfo(kPlayer.getHandicapType()).getHealthBonus();
	if (iBadHealth >= -2) // I.e. can only grow to size 2
	{
		scaled rDiv = scaled::max(1, 3 - rAIEraFactor + iBadHealth);
		int iMult = 1;
		if (rDiv <= 1)
		{
			iMult = 2;
			rDiv = 3;
			if (kSet.isStartingLoc() && !kSet.isScenario())
			{
				iMult = 3;
				rDiv = 4;
			}
		}
		iValue = ((iMult * iValue) / rDiv).round();
		IFLOG if (rDiv.round()>1) logBBAI("Times %d/%d for bad health", iMult, rDiv.round());
	}
	return iValue;
}

// advc: Moved from CvPlayerAI since it's only used for computing found values
int AIFoundValue::countDeadlockedBonuses() const
{
	int r = 0;
	int const iMinRange = GC.getDefineINT(CvGlobals::MIN_CITY_RANGE); // 2
	int const iRange = iMinRange * 2;
	for (SquareIter it(kPlot, iRange); it.hasNext(); ++it)
	{
		if (it.currPlotDist() > CITY_PLOTS_RADIUS)
		{
			// <advc.031>
			if (!isRevealed(*it))
				continue; // </advc.031>
			// <advc> Checks moved into subroutine
			if(isDeadlockedBonus(*it, iMinRange))
				r++; // </advc>
		}
	}
	return r;
}

// advc: Cut from countDeadlockedBonuses
bool AIFoundValue::isDeadlockedBonus(CvPlot const& kBonusPlot, int iMinRange) const
{
	if(getBonus(kBonusPlot) == NO_BONUS || kBonusPlot.isCityRadius())
		return false;
	// advc: kArea is the area of the first potential city site (kPlot) near kBonusPlot
	if(!kBonusPlot.isArea(kArea) && !kBonusPlot.isWater())
		return false;
	bool bCanFound = false;
	bool bNeverFound = true;
	//look for a city site [kOtherSite] within a city radius [around kBonusPlot]
	for (CityPlotIter it(kBonusPlot); it.hasNext(); ++it)
	{
		CvPlot const& kOtherSite = *it;
		// <advc.031> Won't want to settle on top of another resource
		if(getBonus(kOtherSite) != NO_BONUS)
			continue; // </advc.031>
		// <advc.031> Need to be able to see if there's land
		if (!isRevealed(kOtherSite) && !kOtherSite.isAdjacentRevealed(eTeam))
			continue; // </advc.031>
		//canFound usually returns very quickly
		if (kPlayer.canFound(kOtherSite,
			false, kSet.isAllSeeing())) // advc.181
		{
			bNeverFound = false;
			if (stepDistance(&kPlot, &kOtherSite) > iMinRange ||
				// advc.031: No distance restriction for cities in different land areas
				!kPlot.sameArea(kOtherSite))
			{
				bCanFound = true;
				break;
			}
		}
	}
	return (!bNeverFound && !bCanFound);
}

// <advc.031c>
void CitySiteEvaluator::logSettings() const
{
	logBBAI("Found parameters for %S:", isStartingLoc() ?
			L"starting location" : getPlayer().getName());
	logBBAI("Culture claim treshold: %d", getClaimThreshold());
	if (getMinRivalRange() != -1)
		logBBAI("MinRivalRange: %d", getMinRivalRange());
	// <advc.300>
	if (getBarbarianDiscouragedRange() != iDEFAULT_BARB_DISCOURAGED_RANGE)
		logBBAI("BarbarianDiscouragedRange: %d", getBarbarianDiscouragedRange());
	// </advc.300>
	if (isStartingLoc())
		logBBAI("StartingLoc");
	if (isScenario())
		logBBAI("WBScenario");
	// <advc.031e>
	if (isNormalizing())
		logBBAI("Normalizing"); // </advc.031e>
	// <advc.007>  <advc.027>
	if (isIgnoreStartingSurroundings())
		logBBAI("Ignoring starting surroundings");
	// <advc.027>
	if (isDebug())
		logBBAI("Ignoring other sites"); // </advc.007>
	if (isAllSeeing())
		logBBAI("All-seeing");
	if (isAdvancedStart())
		logBBAI("in Advanced Start");
	if (isEasyCulture())
		logBBAI("Easy culture");
	if (isAmbitious())
		logBBAI("Ambitious");
	// <advc.908a>
	if (isExtraYieldNaturalThreshold())
		logBBAI("Financial (AdvCiv effect)"); // </advc.908a>
	if (isExtraYieldThreshold())
		logBBAI("Financial (BtS effect)");
	if (isDefensive())
		logBBAI("Defensive");
	if (isSeafaring())
		logBBAI("Seafaring");
	if (isExpansive())
		logBBAI("Expansive (tall)");
}

void AIFoundValue::logSite() const
{
	logBBAI("Computing found value for %S", kPlot.debugStr());
	if (bCoastal)
		logBBAI("Site is coastal");
	if (!kSet.isStartingLoc() && !kSet.isNormalizing())
		logBBAI("%d other %S cities in the area, %d in total", iAreaCities, kPlayer.getCivilizationShortDescription(), iCities);
}

void AIFoundValue::logPlot(CvPlot const& p, int iPlotValue, int const* aiYield,
	int iCultureModifier, BonusTypes eBonus, ImprovementTypes eBonusImprovement,
	bool bCanTradeBonus, bool bCanSoonTradeBonus, bool bCanImproveBonus,
	bool bCanSoonImproveBonus, bool bEasyAccess,
	int iFeatureProduction, bool bPersistentFeature, bool bRemovableFeature) const
{
	int const F = YIELD_FOOD, P = YIELD_PRODUCTION, C = YIELD_COMMERCE;
	if (isHome(p))
		logBBAI("Home plot: val=%d, %dF%dP%dC", iPlotValue, aiYield[F], aiYield[P], aiYield[C]);
	else logBBAI("Plot in radius: %S; val=%d, %dF%dP%dC", p.debugStr(), iPlotValue, aiYield[F], aiYield[P], aiYield[C]);
	if (iCultureModifier != 100)
		logBBAI("Culture modifier: %d", iCultureModifier);
	if (eBonus != p.getBonusType())
	{
		FAssert(eBonus == NO_BONUS);
		logBBAI("Bonus resource hidden");
	}
	if (eBonus != NO_BONUS)
	{
		// Try not to output redundant information here ...
		if (eBonusImprovement == NO_IMPROVEMENT)
		{
			logBBAI("Can't improve resource");
			FAssert(!bCanImproveBonus && !bCanTradeBonus);
		}
		else
		{
			FAssert(bCanSoonImproveBonus || kSet.isAllSeeing());
			if (!bCanSoonTradeBonus)
				logBBAI("Can't connect resource");
			else if (!bCanTradeBonus)
				logBBAI("Can soon connect resource");
			if ((!bCanSoonTradeBonus || !bCanTradeBonus) && bCanImproveBonus)
				logBBAI("Can improve resource");
			else if (!bCanSoonTradeBonus && !bCanTradeBonus)
				logBBAI("Can soon improve resource");
		}
		FAssert(!bCanTradeBonus || bCanSoonTradeBonus);
		if (!bEasyAccess)
			logBBAI("Difficult to access");
	}
	if (isHome(p))
		return;
	if (iFeatureProduction != 0)
	{
		FAssert(!bPersistentFeature);
		logBBAI("Feature production: %d%s", iFeatureProduction, bRemovableFeature ? "" :
				" (reduced b/c can't remove yet)");
	}
	else if (bRemovableFeature)
	{
		FAssert(!bPersistentFeature);
		logBBAI("can remove feature");
	}
}

wchar const* AIFoundValue::cityName(CvCity const& kCity)
{
	static CvWString szName;
	szName = kCity.getName().GetCString();
	return szName;
}
// </advc.031c>

/*	advc.027: Computes a hypothetical contribution that p could make to the
	found value of some future city, e.g. in this->kPlot, but, for the most part,
	it shouldn't matter where the city will be and we can't really tell. */
scaled AIFoundValue::evaluateWorkablePlot(CvPlot const& p) const
{
	FAssert(!isLoggingEnabled()); // The output wouldn't make much sense

	scaled r;

	/*	This preamble is mostly copy-pasted from AIFoundValue::evaluate.
		A bit different b/c we have a longer time horizon here. */
	bool bRemovableFeature = false;
	bool bPersistentFeature = false;
	FeatureTypes const eFeature = p.getFeatureType();
	{
		int iFeatureProduction = 0;
		bRemovableFeature = isRemovableFeature(p, bPersistentFeature, iFeatureProduction);
		r += evaluateFeatureProduction(iFeatureProduction);
	}
	BonusTypes const eBonus = getBonus(p);
	bool bCanTradeBonus = false;
	bool bCanImproveBonus = false;
	bool bCanSoonTradeBonus = false;
	bool bCanSoonImproveBonus = false;
	int aiBonusImprovementYield[NUM_YIELD_TYPES] = {0, 0, 0};
	ImprovementTypes eBonusImprovement = NO_IMPROVEMENT;
	if (eBonus != NO_BONUS)
	{
		bool bImprovementRemovesFeature = false;
		eBonusImprovement = getBonusImprovement(eBonus, p,
				bCanTradeBonus, bCanSoonTradeBonus, aiBonusImprovementYield,
				bCanImproveBonus, bCanSoonImproveBonus, bImprovementRemovesFeature);
		if (eBonusImprovement == NO_IMPROVEMENT) // We're nowhere near the tech reqs
		{
			FAssert(aiBonusImprovementYield[YIELD_FOOD] == 0 &&
					aiBonusImprovementYield[YIELD_PRODUCTION] == 0 &&
					aiBonusImprovementYield[YIELD_COMMERCE] == 0);
			// To account for w/e yields the improved resource will provide eventually
			aiBonusImprovementYield[YIELD_PRODUCTION] = 1;
		}
	}
	if (!bPersistentFeature && eFeature != NO_FEATURE)
	{
		int iRemovableFeatureYieldVal = removableFeatureYieldVal(
				eFeature, bRemovableFeature, eBonus != NO_BONUS);
		int iNonPersistentFeatureYieldVal = removableFeatureYieldVal(
				eFeature, true, eBonus != NO_BONUS);
		/*	Weighted average to account for chopping becoming available later.
			Mostly treat chopping as available b/c Jungle seems to get valued
			too lowly; I guess b/c bonus improvement yields aren't counted. */
		r += scaled(iRemovableFeatureYieldVal + 3 * iNonPersistentFeatureYieldVal, 4);
	}
	int aiYield[NUM_YIELD_TYPES];
	FOR_EACH_ENUM(Yield)
	{
		aiYield[eLoopYield] = p.calculateNatureYield(eLoopYield,
				eBonus == NO_BONUS ? NO_TEAM : eTeam,
				!bPersistentFeature);
	}
	scaled const rSpecialYieldModifier =
			per100(calculateSpecialYieldModifier(100,
			true, eBonus != NO_BONUS, true, bCanImproveBonus)) +
			per100(calculateSpecialYieldModifier(100,
			true, eBonus != NO_BONUS, bCanSoonImproveBonus, bCanImproveBonus));

	/*	Here I deviate from AIFoundValue::evaluate b/c evaluating special yields
		separately wouldn't work here (and it was a bad idea in the first place).
		I'll apply the special yield modifier to the (whole) yield value in the end. */
	int aiBuildingYield[NUM_YIELD_TYPES];
	calculateBuildingYields(p, aiYield, aiBuildingYield);
	bool bAnySpecial = false;
	FOR_EACH_ENUM(Yield)
	{
		int iSpecial = aiBonusImprovementYield[eLoopYield] +
				aiBuildingYield[eLoopYield];
		if (iSpecial != 0)
		{
			aiYield[eLoopYield] += iSpecial;
			bAnySpecial = true;
		}
	}
	scaled rYieldVal;
	// Equal weight for food and production, but penalize low food later.
	int const aiYieldWeight[NUM_YIELD_TYPES] = {20, 20, 10};
	FOR_EACH_ENUM(Yield)
	{
		scaled rWeight = aiYieldWeight[eLoopYield];
		int iYield = aiYield[eLoopYield];
		if (iYield < 0) // BonusImprovementYield can be negative
			rWeight /= 2;
		rYieldVal += aiYield[eLoopYield] * rWeight;
	}
	{
		bool const bCanNeverImprove = (eFeature != NO_FEATURE &&
				GC.getInfo(eFeature).isNoImprovement());
		// Anticipate terrain improvement
		if (!bCanNeverImprove && !bAnySpecial && !p.isWater())
		{
			rYieldVal *= (  // Too slow for what it accomplishes?
					/*p.isFreshWater() && p.canHavePotentialIrrigation()) ? fixp(1.8) :*/
					fixp(1.75));
		}
		if (bCanNeverImprove) // Not having to improve it is valuable
			rYieldVal *= fixp(4/3.);
	}
	if (aiYield[YIELD_FOOD] < GC.getFOOD_CONSUMPTION_PER_POPULATION())
		rYieldVal *= fixp(0.9); // 0 food isn't necessarily worse
	rYieldVal -= (GC.getFOOD_CONSUMPTION_PER_POPULATION() + fixp(1/3.))
			* aiYieldWeight[YIELD_FOOD] // for pop growth and sustenance
			+ scaled(aiYieldWeight[YIELD_COMMERCE], 4); // expenses per population
	if (rYieldVal > 0)
	{
		rYieldVal.exponentiate(fixp(1.3));
		rYieldVal *= rSpecialYieldModifier;
		r += rYieldVal;
	}
	if (!p.isImpassable())
	{	/*	Even with marginal tile yields, just having space is valuable
			for city placement. */
		int iVal = aiYield[YIELD_FOOD] + aiYield[YIELD_PRODUCTION] +
				aiYield[YIELD_COMMERCE] / 2 +
				(eBonus != NO_BONUS || eFeature != NO_FEATURE ? 2 : 0);
		if ((iVal >= 1 && !p.isWater()) || iVal >= 2)
		{
			r += 4;
			if (iVal >= 2)
			{
				iVal += 4;
				if (!p.isWater() || p.isLake())
					r += 10;
			}
		}
	}
	if (eBonus != NO_BONUS)
	{
		bool bDummy=false;
		/*	It won't necessarily be the first instance of eBonus, but we also want
			to look a bit farther ahead than "soon"; that ought to even out. */
		scaled rNonYieldBonusVal = nonYieldBonusValue(p, eBonus, bCanTradeBonus,
				bCanSoonTradeBonus, true, bDummy, NULL, 100);
		if (!bCanSoonImproveBonus)
		{	/*	Midgame and late-game resources need to be (greatly) devalued though;
				b/c their reward is greatly delayed and b/c they're not supposed to
				steer starting positions much in any case. */
			TechTypes eTech = GC.getInfo(eBonus).getTechImprove(p.isWater());
			scaled rEraDiff = CvEraInfo::normalizeEraNum(
					(eTech == NO_TECH ? 0 : GC.getInfo(eTech).getEra() - eEra));
			if (rEraDiff >= 4)
			{	/*	Some special yield is counted for all resources; that should be
					enough and more for late-game resources. */
				rNonYieldBonusVal = 0;
			}
			else if (rEraDiff.isPositive())
			{
				rNonYieldBonusVal *= 2;
				rNonYieldBonusVal /= (2 + SQR(rEraDiff));
			}
		}
		// Settling near low-yield resources (especially Snow Fur) is an inconvenience
		scaled const rYieldThresh = 48;
		if (rYieldVal < rYieldThresh)
		{
			// Halve if rYieldVal equal to -rYieldThresh or less; 75% if rYieldVal=0.
			scaled rLowYieldMult = fixp(0.75) +
					(1 / (4 * rYieldThresh)) * scaled::max(-rYieldThresh, rYieldVal);
			rNonYieldBonusVal *= rLowYieldMult;
		}
		r += rNonYieldBonusVal;
	}
	{
		int const iFeatureHealth = (eFeature == NO_FEATURE ? 0 :
				GC.getInfo(eFeature).getHealthPercent());
		if (iFeatureHealth > 0 || bPersistentFeature)
			r += iFeatureHealth * fixp(1/6.);
		else if (!bRemovableFeature)
			r += iFeatureHealth * fixp(1/9.);
	}
	if (r > 0 && p.isWater())
	{
		/*	Decrease value if surrounding land is bad.
			Save time by only looking at kPlot. */
		int iYieldScore = 5 * kPlot.calculateNatureYield(YIELD_FOOD, NO_TEAM, true, true) +
				4 * kPlot.calculateNatureYield(YIELD_PRODUCTION, NO_TEAM, true, true) +
				2 * kPlot.calculateNatureYield(YIELD_COMMERCE, NO_TEAM, true, true);
		int const iTargetScore = 8;
		if (iYieldScore < iTargetScore)
			r *= 1 - (iTargetScore - iYieldScore) * per100(4);
	}
	if (p.isGoody())
	{
		//r += evaluateGoodies(1);
		/*	They're more valuable than this, but don't want to encourage
			goodies close to starting sites. */
		r += 18;
	}
	return scaled::max(r, 0);
}
