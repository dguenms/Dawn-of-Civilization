#include "CvGameCoreDLL.h"
#include "CvCityAI.h"
#include "CoreAI.h"
#include "CvSelectionGroupAI.h"
#include "UWAIAgent.h" // advc.031b (for trait checks)
#include "CityPlotIterator.h"
#include "CvUnit.h"
#include "CvArea.h"
#include "CvInfo_City.h"
#include "CvInfo_Terrain.h"
#include "CvInfo_GameOption.h"
#include "CvInfo_Civics.h"
#include "BBAILog.h" // BETTER_BTS_AI_MOD, AI logging, 10/02/09, jdog5000


CvCityAI::CvCityAI() // advc.003u: Merged with AI_reset
{
	FAssert(GC.getNumEmphasizeInfos() > 0);
	m_pbEmphasize = new bool[GC.getNumEmphasizeInfos()]();
	/*  (Could also declare these as arrays in CvCityAI.h, but would then have to
		use loops to zero-initialize them) */
	m_aiEmphasizeYieldCount = new int[NUM_YIELD_TYPES]();
	m_aiEmphasizeCommerceCount = new int[NUM_COMMERCE_TYPES]();
	m_aiSpecialYieldMultiplier = new int[NUM_YIELD_TYPES]();
	m_aiPlayerCloseness = new int[MAX_PLAYERS]();
	// <advc.opt> Store closeness cache meta data for each player separately
	m_aiCachePlayerClosenessTurn = new int[MAX_PLAYERS];
	for (int i = 0; i < MAX_PLAYERS; i++)
		m_aiCachePlayerClosenessTurn[i] = -1;
	m_aiCachePlayerClosenessDistance = new int[MAX_PLAYERS];
	for (int i = 0; i < MAX_PLAYERS; i++)
		m_aiCachePlayerClosenessDistance[i] = -1; // </advc.opt>
	/*	These two were declared as arrays, but it's neater to treat them all alike.
		And the build values had been set to NO_BUILD instead of 0. */
	m_aiBestBuildValue = new int[NUM_CITY_PLOTS]();
	m_aeBestBuild = new BuildTypes[NUM_CITY_PLOTS];
	FOR_EACH_ENUM(CityPlot)
		m_aeBestBuild[eLoopCityPlot] = NO_BUILD;
	m_eBestBuild = NO_BUILD; // advc.opt

	AI_ClearConstructionValueCache(); // K-Mod

	m_iCultureWeight = 30; // K-Mod
	m_iEmphasizeAvoidGrowthCount = 0;
	m_iEmphasizeGreatPeopleCount = 0;
	m_iWorkersNeeded = 0;
	m_iWorkersHave = 0;
	m_iNeededFloatingDefenders = -1;
	m_iNeededFloatingDefendersCacheTurn = -1;
	m_iCityValPercent = 0; // advc.139

	m_bForceEmphasizeCulture = false;
	m_bStrongEmphasis = false; // advc.131d
	m_bAssignWorkDirty = false;
	m_eSafety = CITYSAFETY_SAFE; // advc.139
}


CvCityAI::~CvCityAI()
{
	SAFE_DELETE_ARRAY(m_pbEmphasize); // advc.003u: Moved from deleted AI_uninit
	SAFE_DELETE_ARRAY(m_aiEmphasizeYieldCount);
	SAFE_DELETE_ARRAY(m_aiEmphasizeCommerceCount);
	SAFE_DELETE_ARRAY(m_aiSpecialYieldMultiplier);
	SAFE_DELETE_ARRAY(m_aiPlayerCloseness);

	SAFE_DELETE_ARRAY(m_aiBestBuildValue);
	SAFE_DELETE_ARRAY(m_aeBestBuild);
}

// Instead of having CvCity::init call CvCityAI::AI_init
void CvCityAI::init(int iID, PlayerTypes eOwner, int iX, int iY,
	bool bBumpUnits, bool bUpdatePlotGroups, /* advc.ctr: */ int iOccupationTimer)
{
	CvCity::init(iID, eOwner, iX, iY, bBumpUnits, bUpdatePlotGroups, iOccupationTimer);
	//AI_reset(); // advc.003u: Merged into constructor
	AI_assignWorkingPlots();
	// BETTER_BTS_AI_MOD, City AI, Worker AI, 11/14/09, jdog5000: calls swapped
	AI_updateBestBuild();
	AI_updateWorkersHaveAndNeeded();
	// BETTER_BTS_AI_MOD: END
}


void CvCityAI::AI_doTurn()
{
	PROFILE_FUNC();

	if (!isHuman())
	{
		FOR_EACH_ENUM(Specialist)
			setForceSpecialistCount(eLoopSpecialist, 0);
		AI_stealPlots();
	}
	/*AI_updateWorkersHaveAndNeeded();
	AI_updateBestBuild();*/
	// BETTER_BTS_AI_MOD, City AI, Worker AI, 11/14/09, jdog5000: START
	if (!isDisorder()) // K-Mod
		AI_updateBestBuild();
	AI_updateWorkersHaveAndNeeded();
	// BETTER_BTS_AI_MOD: END
	AI_updateRouteToCity();

	if (isHuman())
	{
		if (isProductionAutomated())
			AI_doHurry();
		return;
	}
	AI_doPanic();
	AI_doDraft();
	AI_doHurry();
	AI_doEmphasize();
}

// (Most of this function has been rewritten for K-Mod)
void CvCityAI::AI_assignWorkingPlots(/* advc.131d: */ bool bEmphasize)
{
	PROFILE_FUNC();

	/*if (0 != GC.getDefineINT("AI_SHOULDNT_MANAGE_PLOT_ASSIGNMENT"))
		return;*/ // K-Mod. that bts option would break a bunch of stuff.

    // doc: Manchu UP: should update whenever there is a reason to assign working plots
    if (getCivilizationType() == MANCHU)
        updateYield();

	// remove any plots we can no longer work for any reason
	verifyWorkingPlots();

	// if we have more specialists of any type than this city can have, reduce to the max
	FOR_EACH_ENUM2(Specialist, e)
	{
		if (!isSpecialistValid(e))
		{
			if (getSpecialistCount(e) > getMaxSpecialistCount(e))
			{
				setSpecialistCount(e, getMaxSpecialistCount(e));
			}
			// K-Mod. Apply the cap to forced specialist count as well.
			if (getForceSpecialistCount(e) > getMaxSpecialistCount(e))
				setForceSpecialistCount(e, getMaxSpecialistCount(e));

			FAssert(isSpecialistValid(e));
		}
	}

	// always work the home plot (center)
	CvPlot* pHomePlot = getCityIndexPlot(CITY_HOME_PLOT);
	if (pHomePlot != NULL)
	{
		setWorkingPlot(CITY_HOME_PLOT,
				getPopulation() > 0 && canWork(*pHomePlot));
	}

	// keep removing the worst citizen until we are not over the limit
	while (extraPopulation() < 0)
	{
		if (!AI_removeWorstCitizen())
		{
			FErrorMsg("failed to remove extra population");
			break;
		}
	}

	// extraSpecialists() is less than extraPopulation()
	FAssertMsg(extraSpecialists() >= 0, "extraSpecialists() is expected to be non-negative (invalid Index)");

	// K-Mod. If the city is in disorder, then citizen assignment doesn't matter.
	if (isDisorder())
	{
		FAssert((getWorkingPopulation() + getSpecialistPopulation()) <= (totalFreeSpecialists() + getPopulation()));
		AI_setAssignWorkDirty(false);

		if (isActiveOwned() && isCitySelected())
		{
			gDLL->UI().setDirty(CitizenButtons_DIRTY_BIT, true);
		}
		return;
	}

	//update the special yield multiplier to be current
	AI_updateSpecialYieldMultiplier();

	// Remove all assigned plots before automatic assignment.
	/*if (!isHuman() || isCitizensAutomated()) {
		FOR_EACH_ENUM(CityPlot)
			setWorkingPlot(eLoopCityPlot, false);
	}*/

	// make sure at least the forced amount of specialists are assigned
	// K-Mod note: it's best if we don't clear all working specialists,
	// because AI_specialistValue uses our current GPP rate in its evaluation.
	bool bNewlyForcedSpecialists = false;
	if (isSpecialistForced()) // advc.opt
	{
		FOR_EACH_ENUM2(Specialist, e)
		{
			int iForcedSpecialistCount = getForceSpecialistCount(e);

			if (getSpecialistCount(e) < iForcedSpecialistCount)
			{
				setSpecialistCount(e, iForcedSpecialistCount);
				bNewlyForcedSpecialists = true;
				FAssert(isSpecialistValid(e));
			}
		}
	}
	// If we added new specialists, we might need to remove something else.
	if (bNewlyForcedSpecialists)
	{
		while (extraPopulation() < 0)
		{
			if (!AI_removeWorstCitizen())
			{
				FErrorMsg("failed to remove extra population");
				break;
			}
		}
	}

	// do we have population unassigned
	while (extraPopulation() > 0)
	{
		// (AI_addBestCitizen now handles forced specialist logic)
		if (!AI_addBestCitizen(/*bWorkers*/ true, /*bSpecialists*/ true))
		{
			FErrorMsg("failed to assign extra population");
			break;
		}
	}

	// if we still have population to assign, assign specialists
	while (extraSpecialists() > 0)
	{
		if (!AI_addBestCitizen(/*bWorkers*/ false, /*bSpecialists*/ true))
		{
			FErrorMsg("failed to assign extra specialist");
			break;
		}
	}

	FAssertMsg(extraSpecialists() >= 0, "added too many specialists");

	// if automated, look for better choices than the current ones
	if (!isHuman() || isCitizensAutomated())
		AI_juggleCitizens(/* advc.131d: */ bEmphasize);

	// at this point, we should not be over the limit
	FAssert((getWorkingPopulation() + getSpecialistPopulation()) <= (totalFreeSpecialists() + getPopulation()));
	FAssert(extraPopulation() == 0); // K-Mod.

	AI_setAssignWorkDirty(false);

	if (isActiveOwned() && isCitySelected())
		gDLL->UI().setDirty(CitizenButtons_DIRTY_BIT, true);
}


void CvCityAI::AI_updateAssignWork()
{
	if (AI_isAssignWorkDirty())
		AI_assignWorkingPlots();
}

// advc.003j: Unused K-Mod function (one call commented out in CvGameTextMgr)
/*bool CvCityAI::AI_ignoreGrowth() {
	PROFILE_FUNC();
	if (!AI_isEmphasizeYield(YIELD_FOOD) && !AI_isEmphasizeGreatPeople()) {
		if (!AI_foodAvailable((isHuman()) ? 0 : 1))
			return true;
	}
	return false;
}*/


// units of ~400x commerce
int CvCityAI::AI_specialistValue(SpecialistTypes eSpecialist, bool bRemove, bool bIgnoreFood, int iGrowthValue) const
{
	// K-Mod. To reduce code duplication, this function now uses AI_jobChangeValue. (original code deleted)
	if (bRemove)
	{
		return -AI_jobChangeValue(std::make_pair(false, -1), std::make_pair(true, eSpecialist),
				bIgnoreFood, false, iGrowthValue);
	}
	return AI_jobChangeValue(std::make_pair(true, eSpecialist), std::make_pair(false, -1),
			bIgnoreFood, false, iGrowthValue);
}

// K-Mod. The value of a long-term specialist, for use in calculating great person value, and value of free specialists from buildings.
// value is roughly 4 * 100 * commerce
int CvCityAI::AI_permanentSpecialistValue(SpecialistTypes eSpecialist) const
{
	const CvPlayerAI& kPlayer = GET_PLAYER(getOwner());

	const int iCommerceValue = 4;
	const int iProdValue = 7;
	const int iFoodValue = 11;

	int iValue = 0;

	// AI_getYieldMultipliers takes a little bit of time, so lets only do it if we need to.
	bool bHasYield = false;
	FOR_EACH_ENUM(Yield)
	{
		if (kPlayer.specialistYield(eSpecialist, eLoopYield) != 0)
		{
			bHasYield = true;
			break;
		}
	}

	if (bHasYield)
	{
		int iFoodX, iProdX, iComX, iUnused;
		AI_getYieldMultipliers(iFoodX, iProdX, iComX, iUnused);
		// I'm going to dilute the yield value multipliers, because they are ultimately less stable than commerce multipliers.
		iValue += iFoodValue * kPlayer.specialistYield(eSpecialist, YIELD_FOOD) *
				AI_yieldMultiplier(YIELD_FOOD) * (100+iFoodX) / 200;
		iValue += iProdValue * kPlayer.specialistYield(eSpecialist, YIELD_PRODUCTION) *
				AI_yieldMultiplier(YIELD_PRODUCTION) * (100+iProdX) / 200;
		iValue += iCommerceValue * kPlayer.specialistYield(eSpecialist, YIELD_COMMERCE) *
				AI_yieldMultiplier(YIELD_COMMERCE) * (100+iComX) / 200;
	}

	FOR_EACH_ENUM(Commerce)
	{
		int iTemp = iCommerceValue * kPlayer.specialistCommerce(
				eSpecialist, eLoopCommerce);
		if (iTemp != 0)
		{
			iTemp *= getTotalCommerceRateModifier(eLoopCommerce);
			iTemp *= kPlayer.AI_commerceWeight(eLoopCommerce, this);
			iTemp /= 100;
			iValue += iTemp;
		}
	}

	int iGreatPeopleRate = GC.getInfo(eSpecialist).getGreatPeopleRateChange();

	if (iGreatPeopleRate != 0)
	{
		int iGPPValue = 4;

		int iTempValue = 100 * iGreatPeopleRate * iGPPValue;

		// Scale based on how often this city will actually get a great person.
		/* Actually... don't do that. That's not the kind of thing we should take into account for permanent specialists.
		int iCityRate = getGreatPeopleRate();
		int iHighestRate = 0;
		FOR_EACH_CITY(pLoopCity, GET_PLAYER(getOwner())) {
			int x = pLoopCity->getGreatPeopleRate();
			if (x > iHighestRate)
				iHighestRate = x;
		}
		if (iHighestRate > iCityRate) {
			iTempValue *= 100;
			iTempValue /= (2*100*(iHighestRate+3))/(iCityRate+3) - 100;
		} */
		iTempValue *= kPlayer.AI_getGreatPersonWeight((UnitClassTypes)GC.getInfo(eSpecialist).getGreatPeopleUnitClass());
		iTempValue /= 100;

		iTempValue *= getTotalGreatPeopleRateModifier();
		iTempValue /= 100;

		iValue += iTempValue;
	}

	int iExperience = GC.getInfo(eSpecialist).getExperience();
	if (iExperience != 0)
	{
		int iProductionRank = findYieldRateRank(YIELD_PRODUCTION);
		int iHasMetCount = GET_TEAM(getTeam()).getHasMetCivCount(true);

		int iTempValue = 100 * iExperience * ((iHasMetCount > 0) ? 4 : 2);
		if (iProductionRank <= kPlayer.getNumCities()/2 + 1)
		{
			iTempValue += 100 * iExperience *  4;
		}
		iTempValue += (getMilitaryProductionModifier() * iExperience * 6); // was * 8

		iTempValue *= 100;
		iTempValue /= (100+15*(getFreeExperience()/5));

		iValue += iTempValue;
	}

	return iValue;
}

/*	advc.192: Based on K-Mod code cut from AI_chooseProduction --
	to make the AI logic there consistent with AI_buildingValue. */
namespace
{
	__inline bool AI_isSwiftBorderExpansion(int iProductionTurns)
	{
		// (advc.192: K-Mod had returned true when there is no higher culture level)
		return (GC.getNumCultureLevelInfos() >= 2 &&
			/*	advc.192: Coefficients added that make this check more lenient - b/c
				citizens may well get reassigned once we commit to a culture building. */
				2 * iProductionTurns <=
				3 * GC.getGame().getCultureThreshold((CultureLevelTypes)2));
	}
}

#define BUILDINGFOCUS_FOOD					(1 << 1)
#define BUILDINGFOCUS_PRODUCTION			(1 << 2)
#define BUILDINGFOCUS_GOLD					(1 << 3)
#define BUILDINGFOCUS_RESEARCH				(1 << 4)
#define BUILDINGFOCUS_CULTURE				(1 << 5)
#define BUILDINGFOCUS_DEFENSE				(1 << 6)
#define BUILDINGFOCUS_HAPPY					(1 << 7)
#define BUILDINGFOCUS_HEALTHY				(1 << 8)
#define BUILDINGFOCUS_EXPERIENCE			(1 << 9)
#define BUILDINGFOCUS_MAINTENANCE			(1 << 10)
#define BUILDINGFOCUS_SPECIALIST			(1 << 11)
#define BUILDINGFOCUS_ESPIONAGE				(1 << 12)
#define BUILDINGFOCUS_BIGCULTURE			(1 << 13)
//#define BUILDINGFOCUS_WORLDWONDER			(1 << 14)
#define BUILDINGFOCUS_WORLDWONDER			(1 << 14 | 1 << 16) // K-Mod (WORLDWONDER implies WONDEROK)
#define BUILDINGFOCUS_DOMAINSEA				(1 << 15)
#define BUILDINGFOCUS_WONDEROK				(1 << 16)
#define BUILDINGFOCUS_CAPITAL				(1 << 17)

// Heavily edited by K-Mod. (note, I've deleted a lot of the old code from BtS and from BBAI, and some of my changes are unmarked.)
void CvCityAI::AI_chooseProduction()
{
	PROFILE_FUNC();

	bool bWasFoodProduction = isFoodProduction();
	bool bDanger = AI_isDanger();

	CvPlayerAI& kPlayer = GET_PLAYER(getOwner());
	// <advc>
	CvTeamAI const& kTeam = GET_TEAM(getTeam());
	CvGame const& kGame = GC.getGame();
	CvArea const& kArea = getArea();
	CvCityAI const* pCapital = kPlayer.AI_getCapital();
	// </advc>

	if (isProduction())
	{
		if (getProduction() > 0)
		{
			//if we are killing our growth to train this, then finish it.
			if (!bDanger && isFoodProduction() && (getProductionUnitAI() != UNITAI_SETTLE ||
				(!kPlayer.AI_isFinancialTrouble() &&
				kPlayer.AI_getNumCitySites() > 0))) // advc.031b
			{
				if (kArea.getAreaAIType(getTeam()) != AREAAI_DEFENSIVE)
					return;
			}
			// if less than 3 turns left, keep building current item
			else if (getProductionTurnsLeft() <= 3)
				return;
			// if building a combat unit, and we have no defenders, keep building it
			UnitTypes eProductionUnit = getProductionUnit();
			if (eProductionUnit != NO_UNIT)
			{
				if (getPlot().getNumDefenders(getOwner()) == 0)
				{
					if (GC.getInfo(eProductionUnit).getCombat() > 0)
						return;
				}
			}
			// if we are building a wonder, do not cancel, keep building it (if no danger)
			/*BuildingTypes eProductionBuilding = getProductionBuilding();
			if (!bDanger && eProductionBuilding != NO_BUILDING && CvBuildingInfo::isLimited(eProductionBuilding))
				return;*/ // BtS
			// K-Mod. same idea, but with a few more conditions
			BuildingTypes eProductionBuilding = getProductionBuilding();
			if (eProductionBuilding != NO_BUILDING && GC.getInfo(eProductionBuilding).isLimited())
			{
				int iCompletion = 100*getBuildingProduction(eProductionBuilding) /
						std::max(1, getProductionNeeded(eProductionBuilding));
				int iThreshold = 25;
				iThreshold += kPlayer.AI_isLandWar(kArea) ? 40 : 0;
				iThreshold += kPlayer.AI_isDoStrategy(AI_STRATEGY_TURTLE) ? 25 : 0; // (in addition to land war)
				iThreshold += !GC.getInfo(eProductionBuilding).isWorldWonder() ? 10 : 0;
				if (iCompletion >= iThreshold)
					return;
			}
			// K-Mod end
		}
		clearOrderQueue();
	}
	//if (kPlayer.isAnarchy())
	if (isDisorder()) // K-Mod
		return;

	// only clear the dirty bit if we actually do a check, multiple items might be queued
	setChooseProductionDirty(false);
	if (bWasFoodProduction)
		AI_assignWorkingPlots();

	if (GC.getPythonCaller()->AI_chooseProduction(*this))
		return;

	//if (isHuman() && isProductionAutomated())
	if (isHuman())
	{
		AI_buildGovernorChooseProduction();
		return;
	}

	if (isBarbarian())
	{
		AI_barbChooseProduction();
		return;
	}

	CvArea* pWaterArea = waterArea(true);
	bool bMaybeWaterArea = false;
	bool bWaterDanger = false;

	if (pWaterArea != NULL)
	{
		bMaybeWaterArea = true;
		if (!kTeam.AI_isWaterAreaRelevant(*pWaterArea))
			pWaterArea = NULL;
		bWaterDanger = kPlayer.AI_isAnyWaterDanger(getPlot(), 4);
	}
	// advc: Some old and unused code deleted
    bool bMajorWar = kTeam.isAtWarWithMajorPlayer(); // doc
	bool bLandWar = kPlayer.AI_isLandWar(kArea); // K-Mod
	bool const bWarPrep = kTeam.AI_isSneakAttackPreparing(); // advc.104s
	bool const bDefenseWar = (kArea.getAreaAIType(getTeam()) == AREAAI_DEFENSIVE);
	bool const bAssaultAssist = (kArea.getAreaAIType(getTeam()) == AREAAI_ASSAULT_ASSIST);
	bool const bTotalWar = (kTeam.AI_getNumWarPlans(WARPLAN_TOTAL) // K-Mod
			/* <advc.104s> */ + (!getUWAI().isEnabled() ? 0 :
			kTeam.AI_getNumWarPlans(WARPLAN_PREPARING_TOTAL)) > 0); // </advc.104s>
	bool bAssault = (bAssaultAssist ||
			kArea.getAreaAIType(getTeam()) == AREAAI_ASSAULT ||
			kArea.getAreaAIType(getTeam()) == AREAAI_ASSAULT_MASSING);
	bool const bPrimaryArea = kPlayer.AI_isPrimaryArea(kArea);
	bool const bFinancialTrouble = kPlayer.AI_isFinancialTrouble();
	int const iNumCitiesInArea = kArea.getCitiesPerPlayer(getOwner());
	// advc: Renamed from bImportantCity
	bool bCultureCity = false; //be very careful about setting this.
	int const iCultureRateRank = findCommerceRateRank(COMMERCE_CULTURE);
	int const iCulturalVictoryNumCultureCities = kGame.culturalVictoryNumCultureCities();

	int const iWarSuccessRating = kTeam.AI_getWarSuccessRating();
	int iEnemyPowerPerc = kTeam.AI_getEnemyPowerPercent(true);
	// <cdtw> (comment by Dave_uk:)
	/*  if we are the weaker part of a team, and have a land war in our primary
		area, increase enemy power percent so we aren't overconfident due to a
		powerful team-mate who may not actually be that much help */
	if (bLandWar && bPrimaryArea && !kTeam.isAVassal() && kTeam.getNumMembers() > 1)
	{
		int iOurPowerPercent = (100 * kPlayer.getPower()) / kTeam.getPower(false);
		if (iOurPowerPercent * kTeam.getNumMembers() < 100)
		{
			iEnemyPowerPerc *= 100;
			iEnemyPowerPerc /= std::max(1, iOurPowerPercent * kTeam.getNumMembers());
		}
	} // </cdtw>
	if (!bLandWar && !bAssault && kTeam.isAVassal())
	{
		bLandWar = kTeam.AI_isMasterPlanningLandWar(kArea);
		if (!bLandWar)
			bAssault = kTeam.AI_isMasterPlanningSeaWar(kArea);
	}

	bool const bGetBetterUnits = kPlayer.AI_isDoStrategy(AI_STRATEGY_GET_BETTER_UNITS);
	bool const bDagger = kPlayer.AI_isDoStrategy(AI_STRATEGY_DAGGER);
	bool const bAggressiveAI = kGame.isOption(GAMEOPTION_AGGRESSIVE_AI);
	bool const bAlwaysPeace = //kGame.isOption(GAMEOPTION_ALWAYS_PEACE);
			!GET_TEAM(getTeam()).AI_isWarPossible(); // advc.001j

	/* bts code
	int iUnitCostPercentage = (kPlayer.calculateUnitCost() * 100) / std::max(1, kPlayer.calculatePreInflatedCosts()); */
	// K-Mod. (note, this is around 3x bigger than the original formula)
	int const iUnitSpending = kPlayer.AI_unitCostPerMil();
	int const iWaterPercent = AI_calculateWaterWorldPercent();

	int const iBuildUnitProb = AI_buildUnitProb();
	// advc.109: Moved into AI_buildUnitProb
	//iBuildUnitProb /= kPlayer.AI_isDoStrategy(AI_STRATEGY_ECONOMY_FOCUS) ? 2 : 1; // K-Mod

	int const iExistingWorkers = kPlayer.AI_totalAreaUnitAIs(kArea, UNITAI_WORKER);
	int const iNeededWorkers = kPlayer.AI_neededWorkers(kArea);
	int const iMissingWorkers = iNeededWorkers - iExistingWorkers; // advc.113
	// Sea worker need independent of whether water area is militarily relevant
	int const iNeededSeaWorkers = (bMaybeWaterArea) ? AI_neededSeaWorkers() : 0;
	int const iExistingSeaWorkers = (pWaterArea != NULL) ?
			kPlayer.AI_totalWaterAreaUnitAIs(*pWaterArea, UNITAI_WORKER_SEA) : 0;

	int iAreaBestFoundValue=-1;
	int const iNumAreaCitySites = kPlayer.AI_getNumAreaCitySites(kArea, iAreaBestFoundValue);

	int iWaterAreaBestFoundValue = 0;
	CvArea* pWaterSettlerArea = pWaterArea;
	if (pWaterSettlerArea == NULL)
	{
		pWaterSettlerArea = GC.getMap().findBiggestArea(true);
		if(pWaterSettlerArea != NULL && // advc.001: What if there is no water at all?
			kPlayer.AI_totalWaterAreaUnitAIs(*pWaterSettlerArea, UNITAI_SETTLER_SEA) == 0)
		{
			pWaterSettlerArea = NULL;
		}
	}
	int iNumWaterAreaCitySites = (pWaterSettlerArea == NULL) ? 0 :
			kPlayer.AI_getNumAdjacentAreaCitySites(iWaterAreaBestFoundValue,
			*pWaterSettlerArea, &kArea);
	int iNumSettlers = kPlayer.AI_totalUnitAIs(UNITAI_SETTLE);

    int const iAreaBestSettlerValue = kPlayer.AI_bestCitySiteSettlerValue(pArea->getID());
    int const iWaterAreaBestSettlerValue = (pWaterSettlerArea != NULL) ? kPlayer.AI_bestAdjacentCitySiteSettlerValue(pWaterSettlerArea->getID()) : 0;

	bool bCapitalArea = false;
	int iNumCapitalAreaCities = 0;
	if (pCapital != NULL)
	{
		iNumCapitalAreaCities = pCapital->getArea().getCitiesPerPlayer(getOwner());
		if (sameArea(*pCapital))
			bCapitalArea = true;
	}

	int iMaxSettlers = 0;
	if (!bFinancialTrouble)
	{
		iMaxSettlers = std::min((kPlayer.getNumCities() + 1) / 2,
				iNumAreaCitySites + iNumWaterAreaCitySites);
		if ((bLandWar || bAssault) && bMajorWar) // doc: must be a major war
			iMaxSettlers = (iMaxSettlers + 2) / 3;
	}
	int iSettlerPriority = 0; // advc.031b

	if (iNumCitiesInArea > 2 &&
		kPlayer.AI_atVictoryStage(AI_VICTORY_CULTURE2) &&
		iCultureRateRank <= iCulturalVictoryNumCultureCities + 1)
	{
		/*	if we do not have enough cities, then the highest culture city
			will not get special attention. */
		if (iCultureRateRank > 1 ||
			kPlayer.getNumCities() > iCulturalVictoryNumCultureCities + 1)
		{
			if (iNumAreaCitySites + iNumWaterAreaCitySites > 0 &&
				kPlayer.getNumCities() < 6 && SyncRandOneChanceIn(2))
			{
				bCultureCity = false;
			}
			else bCultureCity = true;
		}
	}

	// Free experience for various unit domains
	/*int const iFreeLandExperience = getSpecialistFreeExperience() +
		getDomainFreeExperience(DOMAIN_LAND);*/ // advc: unused
	int const iFreeSeaExperience = getSpecialistFreeExperience() +
			getDomainFreeExperience(DOMAIN_SEA);
	int const iFreeAirExperience = getSpecialistFreeExperience() +
			getDomainFreeExperience(DOMAIN_AIR);

	int const iProductionRank = findYieldRateRank(YIELD_PRODUCTION);

	int const iOwnerEra = kPlayer.getCurrentEra(); // advc
	scaled const rOwnerAIEraFactor = kPlayer.AI_getCurrEraFactor(); // advc.erai
	// K-Mod.
	BuildingTypes eBestBuilding = AI_bestBuildingThreshold(); // go go value cache!
	int iBestBuildingValue = (eBestBuilding == NO_BUILDING) ? 0 : AI_buildingValue(eBestBuilding);
	/*	for the purpose of adjusting production probabilities,
		scale the building value up for early eras
		(because early-game buildings are relatively weaker) */
	if (GC.getNumEraInfos() > 1)
	{
		FAssert(iOwnerEra < GC.getNumEraInfos());
		iBestBuildingValue *= 2 * (GC.getNumEraInfos() - 1) - iOwnerEra;
		iBestBuildingValue /= GC.getNumEraInfos() - 1;
	}
	// also, reduce the value to encourage early expansion until we reach the recommend city target
	{
		int iCitiesTarget = GC.getInfo(GC.getMap().getWorldSize()).getTargetNumCities();
		if (iNumAreaCitySites > 0 && kPlayer.getNumCities() < iCitiesTarget)
		{
			iBestBuildingValue *= kPlayer.getNumCities() + iCitiesTarget;
			iBestBuildingValue /= 2*iCitiesTarget;
		}
	}

	// Check for military exemption for commerce cities and underdeveloped cities.
	// Don't give exemptions to cities that don't have anything good to build anyway.
	bool bUnitExempt = false;
	if (iBestBuildingValue >= 40 &&
		(iProductionRank - 1) * 2 > kPlayer.getNumCities())
	{
		bool bBelowMedian = true;
		FOR_EACH_ENUM(Commerce)
		{
			/*	I'd use the total commerce rank, but there currently
				isn't a cached value of that. */
			int iRank = findCommerceRateRank(eLoopCommerce);
			if (iRank < iProductionRank)
			{
				bUnitExempt = true;
				break;
			}
			if ((iRank - 1) * 2 < kPlayer.getNumCities())
				bBelowMedian = false;
		}
		if (bBelowMedian)
			bUnitExempt = true;
	}
	// K-Mod end


	if (gCityLogLevel >= 3) logBBAI("      City %S pop %d considering new production: iProdRank %d, iBuildUnitProb %d%s, iBestBuildingValue %d", getName().GetCString(), getPopulation(), iProductionRank, iBuildUnitProb, bUnitExempt?"*":"", iBestBuildingValue);

	// if we need to pop borders, then do that immediately if we have drama and can do it
	if (getCultureLevel() <= 1)
	{
		// K-Mod. If our best building is a cultural building, just start building it.
		bool bCultureBuilding = false;
		int iProductionTurns = MAX_SHORT;
		if (eBestBuilding != NO_BUILDING)
		{
			CvBuildingInfo const& kBestBuilding = GC.getInfo(eBestBuilding);
			if (kBestBuilding.getCommerceChange(COMMERCE_CULTURE) +
				kBestBuilding.getObsoleteSafeCommerceChange(COMMERCE_CULTURE) > 0 &&
				!kBestBuilding.isLimited() && // advc.192: No wonders here
				AI_countGoodTiles(true, false) > 0) // advc.opt: Moved down
			{
				bCultureBuilding = true;
				iProductionTurns = getProductionTurnsLeft(eBestBuilding, 0);
			}
		}
		if (bCultureBuilding &&
			// advc.192: Moved into auxiliary function
			AI_isSwiftBorderExpansion(iProductionTurns))
		{
			pushOrder(ORDER_CONSTRUCT, eBestBuilding);
			return;
		} // K-Mod end
		if (AI_chooseProcess(COMMERCE_CULTURE))
			return;
		/*	<advc.192> If city keeps growing, but production stays slow,
			then we should bite the bullet and start a slow culture building
			rather sooner than later. */
		if (iBestBuildingValue >= 60 && getPopulation() > 2 &&
			AI_isSwiftBorderExpansion(iProductionTurns /
			std::min(getPopulation() - 1, 3)))
		{
			pushOrder(ORDER_CONSTRUCT, eBestBuilding);
			return;
		} // </advc.192>
	}

	if (getPlot().getNumDefenders(getOwner()) == 0) // XXX check for other team's units?
	{
		if (gCityLogLevel >= 2) logBBAI("      City %S uses no defenders", getName().GetCString());
		if (AI_chooseUnit(UNITAI_CITY_DEFENSE))
			return;
		if (AI_chooseUnit(UNITAI_CITY_COUNTER))
			return;
		if (AI_chooseUnit(UNITAI_CITY_SPECIAL))
			return;
		if (AI_chooseUnit(UNITAI_ATTACK))
			return;
	}

	if (kPlayer.isStrike())
	{
		int iStrikeFlags = 0;
		iStrikeFlags |= BUILDINGFOCUS_GOLD;
		iStrikeFlags |= BUILDINGFOCUS_MAINTENANCE;

		if (AI_chooseBuilding(iStrikeFlags))
		{
			if (gCityLogLevel >= 2) logBBAI("      City %S uses strike building (w/ flags)", getName().GetCString());
			return;
		}

		if (AI_chooseBuilding())
		{
			if (gCityLogLevel >= 2) logBBAI("      City %S uses strike building (w/o flags)", getName().GetCString());
			return;
		}
	}

	// K-Mod. Make room for a 'best project'. -1 indicates that we haven't yet calculated the best project.
	// Well evaluate it soon if we are aiming for a space victory; otherwise we'll just leave it until the end.
	ProjectTypes eBestProject = NO_PROJECT;
	int iProjectValue = -1;
	// K-Mod end

	// K-Mod, short-circuit production choice if we already have something really good in mind
	if (kPlayer.getNumCities() > 1) // don't use this short circuit if this is our only city.
	{
		if (kPlayer.AI_atVictoryStage(AI_VICTORY_SPACE4))
		{
			eBestProject = AI_bestProject(&iProjectValue);
			if (eBestProject != NO_PROJECT && iProjectValue > iBestBuildingValue)
			{
				int iOdds = std::max(0, 100 * iProjectValue / (3 * iProjectValue + 300) - 10);
				if (SyncRandSuccess100(iOdds))
				{
					pushOrder(ORDER_CREATE, eBestProject);
					if (gCityLogLevel >= 2) logBBAI("      City %S uses choose project short-circuit 1. (project value: %d, building value: %d, odds: %d)", getName().GetCString(), iProjectValue, iBestBuildingValue, iOdds);
					return;
				}
			}
		}

		int iOdds = std::max(0, 100 * iBestBuildingValue / (3 * iBestBuildingValue + 300) - 10);
		if (AI_chooseBuilding(0, MAX_INT, 0, iOdds))
		{
			if (gCityLogLevel >= 2) logBBAI("      City %S uses building value short-circuit 1 (odds: %d)", getName().GetCString(), iOdds);
			return;
		}
	} // K-Mod end

	// So what's the right detection of defense which works in early game too?
	int iPlotSettlerCount = (iNumSettlers == 0) ? 0 : getPlot().plotCount(
			PUF_isUnitAIType, UNITAI_SETTLE, -1, getOwner());
	int iPlotCityDefenderCount = /* advc.107: */ std::max(
			getPlot().plotCount(PUF_isUnitAIType, UNITAI_CITY_DEFENSE, -1, getOwner()),
			/*	<advc.107> I guess we want non-CITY_DEFENSE units on GUARD_CITY mission to
				switch to different missions eventually. But not counting them at all
				sometimes leads to too much unit production before the 2nd city. */
			getPlot().plotCount(PUF_isMissionAIType, MISSIONAI_GUARD_CITY, -1, getOwner()) /
			iNumCitiesInArea); // </advc.107>
	if (iOwnerEra == 0)
	{
		/*	Warriors are blocked from UNITAI_CITY_DEFENSE,
			in early game this confuses AI city building */
		if (kPlayer.AI_totalUnitAIs(UNITAI_CITY_DEFENSE) <= kPlayer.getNumCities())
		{
			if (kPlayer.AI_bestCityUnitAIValue(UNITAI_CITY_DEFENSE, this) == 0)
			{
				iPlotCityDefenderCount = getPlot().plotCount(PUF_canDefend, -1, -1,
						getOwner(), NO_TEAM, PUF_isDomainType, DOMAIN_LAND);
			}
		}
	}

	//minimal defense.
	//if (iPlotCityDefenderCount <= iPlotSettlerCount)
	if (!bUnitExempt && iPlotSettlerCount > 0 && iPlotCityDefenderCount <= iPlotSettlerCount)
	{
		if (gCityLogLevel >= 2) logBBAI("      City %S needs escort for existing settler", getName().GetCString());
		if (AI_chooseUnit(UNITAI_CITY_DEFENSE))
		{
			// BBAI TODO: Does this work right after settler is built???
			if (gCityLogLevel >= 2) logBBAI("      City %S uses escort existing settler 1 defense", getName().GetCString());
			return;
		}

		if (AI_chooseUnit(UNITAI_ATTACK))
		{
			if (gCityLogLevel >= 2) logBBAI("      City %S uses escort existing settler 1 attack", getName().GetCString());
			return;
		}
	}

	if (getPopulation() > 5 && AI_needsCultureToWorkFullRadius() &&
		!kPlayer.AI_isDoStrategy(AI_STRATEGY_TURTLE))
	{
		if (AI_chooseBuilding(BUILDINGFOCUS_CULTURE, 30))
		{
			if (gCityLogLevel >= 2) logBBAI("      City %S uses zero culture build", getName().GetCString());
			return;
		}
	}

	// Early game worker logic
	// <advc.113>
	bool bCloseToNewTech = false;
	TechTypes eCurrentResearch = kPlayer.getCurrentResearch();
	if (eCurrentResearch != NO_TECH && bPrimaryArea)
	{
		int iTurnsLeft = kPlayer.getResearchTurnsLeft(eCurrentResearch, true);
		/*  Research turns per tech tend to stay the same throughout the game
			(in AdvCiv), but production turns per worker decrease. */
		if(iTurnsLeft >= 0 && iTurnsLeft <= 12 / (rOwnerAIEraFactor + 1))
			bCloseToNewTech = true;
	} // </advc.113>
	// K-Mod 10/sep/10: iLandBonuses moved up
	int const iLandBonuses = AI_countNumImprovableBonuses(true,
			//kPlayer.getCurrentResearch()
			bCloseToNewTech ? eCurrentResearch : NO_TECH); // advc.113

	bool bChooseWorker = false;

	if (isCapital() &&
		kGame.getElapsedGameTurns() * 100 <
		30 * GC.getInfo(kGame.getGameSpeedType()).getTrainPercent() &&
		!bDanger && !kPlayer.AI_isDoStrategy(AI_STRATEGY_TURTLE))
	{
		if (!bWaterDanger && getPopulation() < 3 &&
			iNeededSeaWorkers > 0 && iExistingSeaWorkers <= 0)
		{
			// Build Work Boat first since it doesn't stop growth
			if (AI_chooseUnit(UNITAI_WORKER_SEA))
			{
				if (gCityLogLevel >= 2) logBBAI("      City %S uses choose worker sea 1a", getName().GetCString());
				return;
			}
		}
		if (iExistingWorkers == 0 && /* advc.113: */ iMissingWorkers > 0 &&
			//AI_totalBestBuildValue(kArea) > 10
			AI_totalBestBuildValue(kArea) + 50 * iLandBonuses > 100) // K-Mod
		{
			if (!bChooseWorker && AI_chooseUnit(UNITAI_WORKER))
			{
				if (gCityLogLevel >= 2) logBBAI("      City %S uses choose worker 1a", getName().GetCString());
				return;
			}
			bChooseWorker = true;
		}
	}

	if (!(bDefenseWar && iWarSuccessRating < -50) && !bDanger)
	{
		if (iExistingWorkers == 0)
		{	/*  K-Mod, 10/sep/10, Karadoc
				I've taken iLandBonuses from here and moved it higher for use elsewhere. */
			//int iLandBonuses = ...
			if (iLandBonuses > 1 || (getPopulation() > 3 && //iNeededWorkers > 0
				// <advc.113>
				iMissingWorkers > 0 &&
				// Wait for the mainland to send a worker
				(bPrimaryArea ||
				(iMissingWorkers > 1 && SyncRandSuccess100(20 * iMissingWorkers)))
				/* </advc.113> */))
			{
				if (!bChooseWorker && AI_chooseUnit(UNITAI_WORKER))
				{
					if (gCityLogLevel >= 2) logBBAI("      City %S uses choose worker 1", getName().GetCString());
					return;
				}
				bChooseWorker = true;
			}

			if (!bWaterDanger && iNeededSeaWorkers > iExistingSeaWorkers && getPopulation() < 3)
			{
				if (AI_chooseUnit(UNITAI_WORKER_SEA))
				{
					if (gCityLogLevel >= 2) logBBAI("      City %S uses choose worker sea 1", getName().GetCString());
					return;
				}
			}

			if (iLandBonuses >= 1  && getPopulation() > 1)
			{
				if (!bChooseWorker && AI_chooseUnit(UNITAI_WORKER))
				{
					if (gCityLogLevel >= 2) logBBAI("      City %S uses choose worker 2", getName().GetCString());
					return;
				}
				bChooseWorker = true;
			}
		}
	}
	/*if (kPlayer.AI_atVictoryStage(AI_VICTORY_DOMINATION3)) {
		if (goodHealth() - badHealth(true, 0) < 1) {
			if (AI_chooseBuilding(BUILDINGFOCUS_HEALTHY, 20, 0, (kPlayer.AI_atVictoryStage(AI_VICTORY_DOMINATION4) ? 50 : 20)))
				return;
		}
	}
	if (kTeam.isAVassal() && kTeam.isCapitulated()) {
		if (!bLandWar) {
			if (goodHealth() - badHealth(true, 0) < 1) {
				if (AI_chooseBuilding(BUILDINGFOCUS_HEALTHY, 30, 0, 3*getPopulation()))
					return;
			}
			if (getPopulation() > 3 && getCommerceRate(COMMERCE_CULTURE) < 5) {
				if (AI_chooseBuilding(BUILDINGFOCUS_CULTURE, 30, 0 + 3*iWarTroubleThreshold, 3*getPopulation()))
					return;
			}
		}
	}*/ // BtS  <cdtw.6>
	if(!kPlayer.isHuman() && kPlayer.AI_atVictoryStage(AI_VICTORY_SPACE4) &&
		!isCoastal() && !isCapital() && bCapitalArea && !bDanger && !bLandWar &&
		pCapital != NULL && pCapital->isCoastal() &&
		getPlot().calculateCulturePercent(getOwner()) >= 50 &&
		// Dave_uk's code (directly) based on AI_cityThreat looked too slow
		AI_neededFloatingDefenders(true) <= pCapital->AI_neededFloatingDefenders(true) &&
		AI_chooseBuilding(BUILDINGFOCUS_CAPITAL, 12))
	{
		return;
	} // </cdtw.6>

	// -------------------- BBAI Notes -------------------------
	// Minimal attack force, both land and sea
	if (bDanger)
	{
		int iAttackNeeded = 4;
		iAttackNeeded += std::max(0, AI_neededDefenders() -
				getPlot().plotCount(PUF_isUnitAIType, UNITAI_CITY_DEFENSE, -1, getOwner()));

		if (kPlayer.AI_totalAreaUnitAIs(kArea, UNITAI_ATTACK) <  iAttackNeeded)
		{
			if (AI_chooseUnit(UNITAI_ATTACK))
			{
				if (gCityLogLevel >= 2) logBBAI("      City %S uses danger minimal attack", getName().GetCString());
				return;
			}
		}
	}

    // doc: be more proactive about settling in the late game before considering other options
    int iMinFoundValue = kPlayer.AI_getMinFoundValue();
    if (bDanger)
    {
        iMinFoundValue *= 3;
        iMinFoundValue /= 2;
    }

    // TODO: refactor
    if (iNumSettlers <= 1 && iNumSettlers < iMaxSettlers && GET_PLAYER(getOwnerINLINE()).AI_getNumTrainAIUnits(UNITAI_SETTLE) == 0)
    {
        if (GET_PLAYER(getOwnerINLINE()).getCurrentEra() >= ERA_RENAISSANCE)
        {
            if (iAreaBestFoundValue > iMinFoundValue && iAreaBestSettlerValue >= 5)
            {
                if (AI_chooseUnit(UNITAI_SETTLE))
                {
                    return;
                }
            }
        }
    }

	// <advc.124> Need these values again later
	int iSeaExplorersTarget = 0;
	int iSeaExplorersNow = 0;
	if(pWaterArea != NULL)
	{
		iSeaExplorersTarget = kPlayer.AI_neededExplorers(*pWaterArea);
		iSeaExplorersNow = kPlayer.AI_totalWaterAreaUnitAIs(*pWaterArea,
				UNITAI_EXPLORE_SEA);
	} // </advc.124>
    // doc: prevent independents from making ships
	if (bMaybeWaterArea && !isIndependent())
	{
		if (!(bLandWar && iWarSuccessRating < -30) && !bDanger && !bFinancialTrouble)
		{	/*  <advc.017> These were calls to AI_getNumTrainAIUnits, i.e. the
				BBAI code ensured that we're not building lots of ships in parallel.
				I want to make sure that we don't end up with more than a
				minimal naval force. */
			std::vector<UnitAITypes> aeSeaAttackTypes;
			aeSeaAttackTypes.push_back(UNITAI_ATTACK_SEA);
			aeSeaAttackTypes.push_back(UNITAI_PIRATE_SEA);
			aeSeaAttackTypes.push_back(UNITAI_RESERVE_SEA);
			if ((bMaybeWaterArea && bWaterDanger) ||
				(pWaterArea != NULL && bPrimaryArea &&
				0 < kPlayer.AI_countNumAreaHostileUnits(*pWaterArea, true, false, false, false,
				plot()))) // advc.081: Range limit
			{
				/*	pWaterArea can be NULL if bMaybeWaterArea, i.e. if there is only an
					unimportant water area. Need to deal with bWaterDanger either way,
					and need to make sure, either way, not to train too many ships. */
				CvArea const* pAnyWaterArea = waterArea(true);
				if (pAnyWaterArea != NULL &&
					kPlayer.AI_totalWaterAreaUnitAIs(*pAnyWaterArea, aeSeaAttackTypes)
					/* </advc.017> */  < std::min(3, kPlayer.getNumCities()))
				{
					if (gCityLogLevel >= 2) logBBAI("      City %S uses minimal naval", getName().GetCString());
					/*  <advc.017> Don't prioritize those ships quite as much
						(was 100% chance in BBAI) */
					int iOdds = 60;
					if(bLandWar && iWarSuccessRating < 0)
						iOdds += 2 * iWarSuccessRating;
					// </advc.017>
					if (AI_chooseUnit(UNITAI_ATTACK_SEA, iOdds))
						return;
					/*  advc.017: Don't want to fall back on these when the above
						fails due to iOdds. Shouldn't be needed either; pirate and
						reserve units can also function as attackers. */
					/*if (AI_chooseUnit(UNITAI_PIRATE_SEA))
						return;
					if (AI_chooseUnit(UNITAI_RESERVE_SEA))
						return;*/
				}
			}

			if (pWaterArea != NULL)
			{
				int iOdds = -1;
				if (iAreaBestFoundValue == 0 || iWaterAreaBestFoundValue > iAreaBestFoundValue)
					iOdds = 100;
				else if (iWaterPercent > 60)
					iOdds = 13;
				if (iOdds >= 0)
				{
                    // doc: prioritise settlers if stuck on an island
                    if (iNumSettlers == 0 && iWaterAreaBestSettlerValue >= 10 && area().getNumUnownedTiles() <= 1 && GET_PLAYER(getOwner()).AI_getNumTrainAIUnits(UNITAI_SETTLE) == 0)
                    {
                        if (AI_chooseUnit(UNITAI_SETTLE))
                        {
                            return;
                        }
                    }

                    // <advc.040>
					if (GC.getInfo(kPlayer.getCurrentEra()).get(CvEraInfo::AIAgeOfExploration) ?
						(iSeaExplorersTarget > iSeaExplorersNow) : // </advc.040>
						/*  advc.124: No functional change from the K-Mod code.
							Original BtS condition deleted (it didn't check
							seaExplorersTarget). */
						(iSeaExplorersNow == 0 && iSeaExplorersTarget > 0))
					{
						iOdds /= (iSeaExplorersNow + 1); // advc.040
						if (AI_chooseUnit(UNITAI_EXPLORE_SEA, iOdds))
						{
							if (gCityLogLevel >= 2) logBBAI("      City %S uses early sea explore", getName().GetCString());
							return;
						}
					}
					// BBAI TODO: Really only want to do this if no good area city sites ... 13% chance on water heavy maps
					// of slow start, little benefit
					/*  <advc.017b> ^That, and we certainly don't want a SETTLER_SEA
						when iWaterAreaBestFoundValue is 0. Especially now that
						CvUnitAI::AI_settlerSeaMove gives unneeded SETTLER_SEA ships
						a different AI type b/c then we keep training ships */
				}
				if((iWaterAreaBestFoundValue > 0 ||
					/*  Should afford one Galleon eventually, if only to
						ferry Workers (advc.040). */
				(iOwnerEra >= CvEraInfo::AI_getAgeOfExploration() &&
                    iNumSettler > 0 && // doc: otherwise we should make settlers
					kPlayer.getNumCities() >= 4)) &&
					pCapital != NULL && sameArea(*pCapital) &&
					// </advc.017b>
					kPlayer.AI_totalWaterAreaUnitAIs(*pWaterArea, UNITAI_SETTLER_SEA) <= 0)
				{
					// <advc.017b>
					iOdds = (iWaterAreaBestFoundValue > iAreaBestFoundValue ?
							-60 : -100);
					if(iAreaBestFoundValue <= 0)
						iOdds = 100;
					else iOdds += (150 * iWaterAreaBestFoundValue) / iAreaBestFoundValue;
					// </advc.017b>
					if (AI_chooseUnit(UNITAI_SETTLER_SEA, iOdds))
					{
						if (gCityLogLevel >= 2) logBBAI("      City %S uses early settler sea", getName().GetCString());
						return;
					}
				}
			}
		}
	}
	// -------------------- BBAI Notes -------------------------
	// Top normal priorities
	/* if (!bPrimaryArea && !bLandWar) {
		if (AI_chooseBuilding(BUILDINGFOCUS_FOOD, 60, 10 + 2*iWarTroubleThreshold, 50)) {
			if (gCityLogLevel >= 2) logBBAI("      City %S uses choose BUILDINGFOCUS_FOOD 1", getName().GetCString());
			return;
		}
	}
	if (!bDanger && ((iOwnerEra > (kGame.getStartEra() + iProductionRank / 2))) || (iOwnerEra > (GC.getNumEraInfos() / 2))) {
		if (AI_chooseBuilding(BUILDINGFOCUS_PRODUCTION, 20 - iWarTroubleThreshold, 15, ((bLandWar || bAssault) ? 25 : -1))) {
			if (gCityLogLevel >= 2) logBBAI("      City %S uses choose BUILDINGFOCUS_PRODUCTION 1", getName().GetCString());
			return;
		}
		if (!(bDefenseWar && iWarSuccessRatio < -30)) {
			if ((iExistingWorkers < ((iNeededWorkers + 1) / 2))) {
				if (getPopulation() > 3 || (iProductionRank < (kPlayer.getNumCities() + 1) / 2)) {
					if (!bChooseWorker && AI_chooseUnit(UNITAI_WORKER)) {
						if (gCityLogLevel >= 2) logBBAI("      City %S uses choose worker 3", getName().GetCString());
						return;
					}
					bChooseWorker = true;
				}
			}
		}
	} */ // K-Mod disabled this stuff

	// advc.113: Moved this conditional block (way) up to prioritize workers
	// note: this is the only worker test that allows us to reach the full number of needed workers.
	if (!(bLandWar && iWarSuccessRating < -30) && !bDanger)
	{	// <advc.113>
		if (iMissingWorkers > 0)
		{	// 1 added on both sides of the inequation so that "have 1, need 2" is invalid
			bool bValid = (3 * (AI_getWorkersHave() + 1) / 2 < AI_getWorkersNeeded() + 1  && // local
					// Wait for existing workers if new city
					getGameTurnFounded() + 5 < kGame.getGameTurn());
			//|| SyncRandNum(80) < iBestBuildingValue + (iBuildUnitProb + 50) / 2
			// Replacing the alt. condition above
			if(!bValid)
			{
				int iWorkerOdds = 110;
				// Discourage training workers in parallel
				int iMaking = kArea.getNumTrainAIUnits(getOwner(), UNITAI_WORKER);
				iWorkerOdds -= (100 * iMaking) / std::max(1, kPlayer.getNumCities() - 1);
				/*  If nearly enough workers, then rather train more settlers first.
					(Use sth. like AI_calculateSettlerPriority*iExistingWorkers^2/iNeededWorkers^2 instead?) */
				if(10 * iExistingWorkers >= 8 * iNeededWorkers && iMaxSettlers > iNumSettlers)
					iWorkerOdds -= 10 * (iMaxSettlers - iNumSettlers);
				iWorkerOdds -= iBestBuildingValue + (iBuildUnitProb + 50) / // no change
						(bWarPrep ? 1 : 2); // Don't halve when prepping
				if(iWorkerOdds > 0 && !bPrimaryArea)
					iWorkerOdds /= 2; // Wait for the mainland to send workers
				bValid = SyncRandSuccess100(iWorkerOdds);
			}
			if(bValid) // </advc.113>
			{
				if (!bChooseWorker && AI_chooseUnit(UNITAI_WORKER))
				{
					if (gCityLogLevel >= 2) logBBAI("      City %S uses choose worker 6", getName().GetCString());
					return;
				}
				bChooseWorker = true;
			}
		}
	}

	bool bCrushStrategy = kPlayer.AI_isDoStrategy(AI_STRATEGY_CRUSH);
	int iNeededFloatingDefenders = (isBarbarian() || bCrushStrategy) ?  0 :
			kPlayer.AI_getTotalFloatingDefendersNeeded(kArea);
	// K-Mod. (note: this has a different scale to the original code).
	int iMaxUnitSpending = kPlayer.AI_maxUnitCostPerMil(&kArea, iBuildUnitProb);

	if (kPlayer.AI_isDoStrategy(AI_STRATEGY_ECONOMY_FOCUS)) // K-Mod
		iNeededFloatingDefenders = (2 * iNeededFloatingDefenders + 2)/3;

 	int iTotalFloatingDefenders = (isBarbarian() ? 0 :
			kPlayer.AI_getTotalFloatingDefenders(kArea));

	// advc: Replacing raw vector of pairs "floatingDefenderTypes"
	UnitAIWeightMap floatingDefenderWeight;
	floatingDefenderWeight.set(UNITAI_CITY_DEFENSE, 125);
	floatingDefenderWeight.set(UNITAI_CITY_COUNTER, 100);
	//floatingDefenderWeight.set(UNITAI_CITY_SPECIAL, 0);
	floatingDefenderWeight.set(UNITAI_RESERVE, 100);
	floatingDefenderWeight.set(UNITAI_COLLATERAL, 80); // K-Mod, down from 100.

	if (iTotalFloatingDefenders < (iNeededFloatingDefenders + 1) / (bGetBetterUnits ? 3 : 2))
	{
		if (!bUnitExempt && iUnitSpending < iMaxUnitSpending + 5)
		{
			if (kArea.getAreaAIType(getTeam()) != AREAAI_NEUTRAL ||
				kPlayer.AI_isDoStrategy(AI_STRATEGY_ALERT1) ||
				SyncRandNum(iNeededFloatingDefenders) >
				iTotalFloatingDefenders * (2*iUnitSpending + iMaxUnitSpending) /
				std::max(1, 3*iMaxUnitSpending))
			{
				if (AI_chooseLeastRepresentedUnit(floatingDefenderWeight))
				{
					if (gCityLogLevel >= 2) logBBAI("      City %S uses choose floating defender 1", getName().GetCString());
					return;
				}
			}
		}
	}

	// If losing badly in war, need to build up defenses and counter attack force
	//if (bLandWar && (iWarSuccessRatio < -30 || iEnemyPowerPerc > 150))
	// K-Mod. I've changed the condition on this; but to be honest, I'm thinking it should just be completely removed.
	// The normal unit selection function should know what kind of units we should be building...
	if (bLandWar && iWarSuccessRating < -10 && iEnemyPowerPerc - iWarSuccessRating > 150)
	{
		UnitAIWeightMap defensiveWeight; // advc: Was vector of pairs "defensiveTypes"
		defensiveWeight.set(UNITAI_COUNTER, 100);
		defensiveWeight.set(UNITAI_ATTACK, 100);
		defensiveWeight.set(UNITAI_RESERVE, 60);
		//defensiveWeight.push_back(std::make_pair(UNITAI_COLLATERAL, 60));
		defensiveWeight.set(UNITAI_COLLATERAL, 80);
		if (bDanger || (iTotalFloatingDefenders <
			(5*iNeededFloatingDefenders) / (bGetBetterUnits ? 6 : 4)))
		{
			defensiveWeight.set(UNITAI_CITY_DEFENSE, 200);
			defensiveWeight.set(UNITAI_CITY_COUNTER, 50);
		}
		int iOdds = iBuildUnitProb;
		if (iWarSuccessRating < -50)
			iOdds -= iWarSuccessRating / 3;
		// K-Mod
		iOdds *= (-iWarSuccessRating + 20 + iBestBuildingValue);
		iOdds /= (-iWarSuccessRating + 2 * iBestBuildingValue);
		// K-Mod end
		if (bDanger)
			iOdds += 10;

		if (AI_chooseLeastRepresentedUnit(defensiveWeight, iOdds))
		{
			if (gCityLogLevel >= 2) logBBAI("      City %S uses choose losing extra defense with odds %d", getName().GetCString(), iOdds);
			return;
		}
	}

	if (!bDefenseWar && iWarSuccessRating < -50)
	{
	/*  K-Mod, 10/sep/10, Karadoc
		Disabled iExistingWorkers == 0. Changed Pop > 3 to Pop >=3.
		Changed Rank < (cities + 1)/2 to Rank <= ...  So that it can catch the case
		where we only have 1 city. */
		//if (iExistingWorkers != 0)
		if (!bDanger && iExistingWorkers < (iNeededWorkers + 1) / 2)
		{
			if (getPopulation() >= 3 || iProductionRank <= (kPlayer.getNumCities() + 1) / 2)
			{
				if (!bChooseWorker &&
					// advc.113: Wait for mainland to send workers
					(bPrimaryArea || SyncRandSuccess100(15 * iMissingWorkers)) &&
					AI_chooseUnit(UNITAI_WORKER))
				{
					if (gCityLogLevel >= 2) logBBAI("      City %S uses choose worker 4", getName().GetCString());
					return;
				}
				bChooseWorker = true;
			}
		}
	}

	//do a check for one tile island type thing?
	//this can be overridden by "wait and grow more"
	// K-Mod, 10/sep/10: was "if (bDanger", I have changed it to "if (!bDanger"
	if (!bDanger && iExistingWorkers == 0 && (isCapital() ||
		iMissingWorkers > 0 || // advc.113: was iNeededWorkers>0
		iNeededSeaWorkers > iExistingSeaWorkers))
	{
		if (!(bDefenseWar && iWarSuccessRating < -30) &&
			!kPlayer.AI_isDoStrategy(AI_STRATEGY_TURTLE))
		{
			if (AI_countNumBonuses(NO_BONUS, /*bIncludeOurs*/ true,
				/*bIncludeNeutral*/ true, -1, /*bLand*/ true, /*bWater*/ false) > 0 ||
				(isCapital() && getPopulation() > 3 && iNumCitiesInArea > 1))
			{
				if (!bChooseWorker && AI_chooseUnit(UNITAI_WORKER))
				{
					if (gCityLogLevel >= 2) logBBAI(" 	 City %S uses choose worker 5", getName().GetCString());
					return;
				}
				bChooseWorker = true;
			}

			if (iNeededSeaWorkers > iExistingSeaWorkers)
			{
				if (AI_chooseUnit(UNITAI_WORKER_SEA,
					60)) // advc.131: From MNAI; was -1.
				{
					if (gCityLogLevel >= 2) logBBAI("      City %S uses choose worker sea 2", getName().GetCString());
					return;
				}
			}
		}
	}

	if (!(bDefenseWar && iWarSuccessRating < -30))
	{
		if (!bWaterDanger && iNeededSeaWorkers > iExistingSeaWorkers)
		{
			if (AI_chooseUnit(UNITAI_WORKER_SEA))
			{
				if (gCityLogLevel >= 2) logBBAI("      City %S uses choose worker sea 3", getName().GetCString());
				return;
			}
		}
	}

    // doc: second additional settler check
    // TODO: refactor
    if (iNumSettlers == 0 && iNumSettlers < iMaxSettlers && GET_PLAYER(getOwnerINLINE()).AI_getNumTrainAIUnits(UNITAI_SETTLE) == 0)
    {
        if (iAreaBestFoundValue > iMinFoundValue && iAreaBestSettlerValue >= 10)
        {
            if (!bFinancialTrouble && !bAreaThreatened && happyLevel() <= unhappyLevel())
            {
                if (AI_chooseUnit(UNITAI_SETTLE))
                {
                    return;
                }
            }
        }
    }

    // doc: only consider major wars
	if	(!(bLandWar && bMajorWar) && !bAssault && AI_needsCultureToWorkFullRadius())
	{
		if (AI_chooseBuilding(BUILDINGFOCUS_CULTURE,
			bAggressiveAI ? 10 : 20, 0, bAggressiveAI ? 33 : 50))
		{
			if (gCityLogLevel >= 2) logBBAI("      City %S uses minimal culture rate", getName().GetCString());
			return;
		}
	}

	// BBAI TODO: Check that this works to produce early rushes on tight maps
	if (!bUnitExempt && !bGetBetterUnits && bCapitalArea &&
		iAreaBestFoundValue < iMinFoundValue * 2 &&
		// <advc.017>
		!kPlayer.AI_isDoStrategy(AI_STRATEGY_ECONOMY_FOCUS) &&
		// (Maybe check CvTeamAI::AI_isLandTarget?)
		kArea.getNumCities() > kTeam.countNumCitiesByArea(kArea))
		// </advc.017>
	{	//Building city hunting stack.
		if (getDomainFreeExperience(DOMAIN_LAND) == 0 &&
			getYieldRate(YIELD_PRODUCTION) > 4)
		{
			if (AI_chooseBuilding(BUILDINGFOCUS_EXPERIENCE,
				rOwnerAIEraFactor > 1 ? 0 : 7, 33))
			{
				if (gCityLogLevel >= 2) logBBAI("      City %S uses special BUILDINGFOCUS_EXPERIENCE 1a", getName().GetCString());
				return;
			}
		}
		int iStartAttackStackRand = 0;
		if (kArea.getCitiesPerPlayer(BARBARIAN_PLAYER) > 0)
			iStartAttackStackRand += 15;
		if (kArea.getNumCities() - iNumCitiesInArea > 0)
			iStartAttackStackRand += iBuildUnitProb / 2;
		if (iStartAttackStackRand > 0)
		{
			int iAttackCityCount = kPlayer.AI_totalAreaUnitAIs(kArea, UNITAI_ATTACK_CITY);
			int iAttackCount = iAttackCityCount +
					kPlayer.AI_totalAreaUnitAIs(kArea, UNITAI_ATTACK);
			if (iAttackCount == 0)
			{
				if (!bFinancialTrouble)
				{
					if (AI_chooseUnit(UNITAI_ATTACK, iStartAttackStackRand))
						return;
				}
			}
			else
			{
				//if((iAttackCount > 1) && (iAttackCityCount == 0))
				/*  <advc.017> Just 1 city-attacker? Isn't it supposed to be a
					"city hunting stack"? Early units don't have the ATTACK_CITY
					AI type, but AI_chooseUnit doesn't care much about the AI types
					assigned in XML. Otoh, ATTACK units will be more useful than
					ATTACK_CITY if we don't end up hunting for any cities ... */
				if (iAttackCount >= iAttackCityCount &&
					iAttackCityCount < 1 + iBuildUnitProb / 19) // </advc.017>
				{
					if (AI_chooseUnit(UNITAI_ATTACK_CITY))
					{
						if (gCityLogLevel >= 2) logBBAI("      City %S chooses to start city attack stack", getName().GetCString());
						return;
					}
				}
				//else if (iAttackCount < 3 + iBuildUnitProb / 10)
				else if (iAttackCount < 2 + iBuildUnitProb / 18) // advc.017
				{
					if (AI_chooseUnit(UNITAI_ATTACK))
					{
						if (gCityLogLevel >= 2) logBBAI("      City %S chooses to add to city attack stack", getName().GetCString());
						return;
					}
				}
			}
			/*	<advc.300> The above won't enable the AI to take Barbarian cities;
				perhaps it was intended to, if so, I think it's far off the mark.
				It might be helpful for giving the AI an appetite for warfare, so
				I'm going to keep it. Now, to at least sometimes conquer Barbarians: */
			if (!kPlayer.AI_isFocusWar())
			{
				int iNeededCityAtt = (kPlayer.AI_neededCityAttackersVsBarbarians()
						/*	Safety margin; some may well be guarding cities or
							have trouble reaching the main stack. */
						* fixp(4/3.)).uceil();
				/*	Even go 1 above the safety margin eventually - in case that
					the Barbarians have unusually many defenders. */
				if (iAttackCityCount <= iNeededCityAtt)
				{
					scaled rProb = kPlayer.AI_barbarianTargetCityScore(getArea());
					if (rProb > 0) // to save time
					{
						if (iAttackCityCount >= iNeededCityAtt)
							rProb /= scaled::max(1, 6 - kPlayer.AI_getCurrEraFactor());
						else
						{
							/*	Inertia - the more attackers we still need, the less
								we're inclined to train any. */
							scaled rDiv = iNeededCityAtt - iAttackCityCount;
							rDiv.exponentiate(std::max(fixp(0.5),
									2 - kPlayer.AI_getCurrEraFactor() / 2));
							rProb /= rDiv;
						}
						/*	The iOdds param causes a re-roll after every production turn.
							Perhaps that should be amended. For now, avoid using it. */
						std::vector<int> aiInputs;
						aiInputs.push_back(getID());
						aiInputs.push_back(iAttackCityCount);
						if (scaled::hash(aiInputs, getOwner()) < rProb &&
							AI_chooseUnit(UNITAI_ATTACK_CITY))
						{
							if (gCityLogLevel >= 2) logBBAI("      City %S trains city attacker vs. Barbarians", getName().GetCString());
							return;
						}
					}
				}
			} // </advc.300>
		}
	}

	//opportunistic wonder build (1)
	if (!bDanger && !hasActiveWorldWonder() && kPlayer.getNumCities() <= 3 &&
		(kPlayer.getNumCities() > 1 || iNumSettlers > 0)) // K-Mod
	{
		// For small civ at war, don't build wonders unless winning
		//if (!bLandWar || (iWarSuccessRating > 30))
		// K-Mod. Don't do this if there is any war at all.
		if (kArea.getAreaAIType(getTeam()) == AREAAI_NEUTRAL)
		{
			int iWonderTime = SyncRandNum(GC.getInfo(getPersonalityType()).
					getWonderConstructRand());
			iWonderTime /= 5;
			iWonderTime += 7;
			if (AI_chooseBuilding(BUILDINGFOCUS_WORLDWONDER, iWonderTime))
			{
				if (gCityLogLevel >= 2) logBBAI("      City %S uses opportunistic wonder build 1", getName().GetCString());
				return;
			}
		}
	}

    // rfc: disable
	/*if (!bDanger && !bCapitalArea &&
		kArea.getCitiesPerPlayer(getOwner()) > iNumCapitalAreaCities)
	{
		// BBAI TODO: Should be handled by CvPlayer, not CvCity. And optimize placement.
		// If losing badly in war, don't build big things.
		if (!bLandWar || iWarSuccessRating > -30)
		{
			// advc.131: Added multipliers to create some inertia
			if (pCapital == NULL || (4 * kArea.getPopulationPerPlayer(getOwner()) >
				5 * pCapital->getArea().getPopulationPerPlayer(getOwner()) &&
				// advc.131:
				findBaseYieldRateRank(YIELD_PRODUCTION) <= kPlayer.getNumCities() / 2))
			{
				int iOdds = 3 * kArea.getCitiesPerPlayer(getOwner()); // advc.131: was 15 flat
				if (AI_chooseBuilding(BUILDINGFOCUS_CAPITAL, iOdds))
					return;
			}
		}
	}*/

	// K-Mod.
	if (iProjectValue < 0 &&
		(kPlayer.AI_atVictoryStage(AI_VICTORY_SPACE3) ||
		!(bLandWar && iWarSuccessRating < 30)))
	{
		eBestProject = AI_bestProject(&iProjectValue);
	} // K-Mod end

	int iSpreadUnitThreshold = 1000;
	if (bLandWar)
		iSpreadUnitThreshold += 800 - 10*iWarSuccessRating;
	iSpreadUnitThreshold += 1000*getPlot().plotCount(
			PUF_isUnitAIType, UNITAI_MISSIONARY, -1, getOwner());
	UnitTypes eBestSpreadUnit = NO_UNIT;
	int iBestSpreadUnitValue = -1;
	if (!bDanger && !kPlayer.AI_isDoStrategy(AI_STRATEGY_TURTLE) &&
        !isIndependent() && // doc: not for independents
		!bAssault) // advc.131 (from MNAI)
	{
		int iSpreadUnitRoll = (100 - iBuildUnitProb) / 3;
		// <advc.104s>
		if (bWarPrep)
			iSpreadUnitRoll -= 5; // </advc.104s>
		else if (!bLandWar)
			iSpreadUnitRoll += 10;
		// K-Mod
		iSpreadUnitRoll *= (200 + std::max(iProjectValue, iBestBuildingValue));
		iSpreadUnitRoll /= (100 + 3 * std::max(iProjectValue, iBestBuildingValue));
		// K-Mod end
		if (AI_bestSpreadUnit(true, true, iSpreadUnitRoll,
			&eBestSpreadUnit, &iBestSpreadUnitValue) &&
			iBestSpreadUnitValue > iSpreadUnitThreshold)
		{
			if (AI_chooseUnit(eBestSpreadUnit, UNITAI_MISSIONARY))
			{
				if (gCityLogLevel >= 2) logBBAI("      City %S uses choose missionary 1", getName().GetCString());
					return;
			}
			FErrorMsg("AI_bestSpreadUnit should provide a valid unit when it returns true");
		}
	}
	// K-Mod
	if (eBestProject != NO_PROJECT && iProjectValue > iBestBuildingValue &&
        !bDanger) // doc: keep danger check
	{
		int iOdds = 100 * (iProjectValue - iBestBuildingValue) /
				(iProjectValue + iBestBuildingValue + iBuildUnitProb);
		if (SyncRandSuccess100(iOdds))
		{
			pushOrder(ORDER_CREATE, eBestProject);
			if (gCityLogLevel >= 2) logBBAI("      City %S uses choose project 1. (project value: %d, building value: %d, odds: %d)", getName().GetCString(), iProjectValue, iBestBuildingValue, iOdds);
			return;
		}
	} // K-Mod end
	// <advc>
	int const iMinDefenders = AI_minDefenders() + iPlotSettlerCount;
	bool const bSpendingExempt = (bUnitExempt ||
			(bFinancialTrouble && iUnitSpending > iMaxUnitSpending)); // </advc>
	//minimal defense.
	//if (!bUnitExempt && iPlotCityDefenderCount < (AI_minDefenders() + iPlotSettlerCount))
	/*	K-Mod.. take into account any defenders that are on their way.
		(recall that in AI_guardCityMinDefender, defenders can be shuffled around)
		(I'm doing the min defender check twice for efficiency -
		so that we don't count targetmissionAIs when we don't need to) */
	if (!bSpendingExempt &&
		iPlotCityDefenderCount < iMinDefenders &&
		iPlotCityDefenderCount < iMinDefenders - kPlayer.AI_plotTargetMissionAIs(getPlot(), MISSIONAI_GUARD_CITY))
	// K-Mod end
	{
		if (AI_chooseUnit(UNITAI_CITY_DEFENSE))
		{
			if (gCityLogLevel >= 2) logBBAI("      City %S uses choose min defender", getName().GetCString());
			return;
		}

		if (AI_chooseUnit(UNITAI_ATTACK))
		{
			if (gCityLogLevel >= 2) logBBAI("      City %S uses choose min defender (attack ai)", getName().GetCString());
			return;
		}
	}
	int const iNukeWeight = kPlayer.AI_nukeWeight(); // K-Mod (advc: moved up)
	// <advc.650> This has much higher priority than the !bLandWar code later on
	if (!bSpendingExempt && iNukeWeight > 0)
	{
		int iNukesHave = kPlayer.AI_totalUnitAIs(UNITAI_ICBM);
		int iNukesWant = 1 + std::min(kPlayer.getNumCities(),
				kGame.getNumCities() - kPlayer.getNumCities()) / 5;
		if (iNukesHave < iNukesWant)
		{
			/*	Relying on the RNG in this function seems generally questionable
				b/c the AI reconsiders orders during the first few production turns */
			std::vector<int> aiInputs;
			aiInputs.push_back(getID());
			aiInputs.push_back(GC.getGame().getGameTurn() / 8);
			scaled rTrainProb(iNukeWeight * (iNukesWant - iNukesHave), 425 * iNukesWant);
			if (scaled::hash(aiInputs, getOwner()) < rTrainProb)
			{
				if (AI_chooseUnit(UNITAI_ICBM))
					return;
			}
		}
	} // </advc.650>

	if (!(bDefenseWar && iWarSuccessRating < -50))
	{
		if (iAreaBestFoundValue > iMinFoundValue || iWaterAreaBestFoundValue > iMinFoundValue)
		{	/*  BBAI TODO: Needs logic to check for early settler builds,
				settler builds in small cities, whether settler sea exists
				for water area sites? */
			if (pWaterArea != NULL)
			{
				int iTotalCities = kPlayer.getNumCities();
				int iSettlerSeaNeeded = std::min(iNumWaterAreaCitySites, ((iTotalCities + 4) / 8) + 1);
				bool bColonies = false; // advc.017b
				// TODO: this is disabled in doc?
                if (pCapital != NULL)
				{
					int iOverSeasColonies = iTotalCities -
							pCapital->getArea().getCitiesPerPlayer(getOwner());
					// <advc.017b>
					if(iOverSeasColonies > 0)
						bColonies = true; // </advc.017b>
					int iLoop = 2;
					int iExtras = 0;
					while (iOverSeasColonies >= iLoop)
					{
						iExtras++;
						iLoop += iLoop + 2;
					}
					iSettlerSeaNeeded += std::min(kPlayer.AI_totalUnitAIs(UNITAI_WORKER) / 4, iExtras);
				}
				if (bAssault)
				{
					iSettlerSeaNeeded = std::min(1, iSettlerSeaNeeded);
					// <advc.017b> For consistency with CvUnitAI::AI_settlerSeaMove
					if(!bColonies && kPlayer.AI_totalUnitAIs(UNITAI_SETTLE) <= 0)
						iSettlerSeaNeeded = 0; // </advc.017b>
				}

				if (kPlayer.AI_totalWaterAreaUnitAIs(*pWaterArea, UNITAI_SETTLER_SEA) < iSettlerSeaNeeded)
				{
					if (AI_chooseUnit(UNITAI_SETTLER_SEA))
					{
						if (gCityLogLevel >= 2) logBBAI("      City %S uses main settler sea", getName().GetCString());
						return;
					}
				}
			}

			if (iPlotSettlerCount <= 0 && iNumSettlers < iMaxSettlers)
			{
				// <advc.031b> Store the result for "build settler 2"
				iSettlerPriority = AI_calculateSettlerPriority(iNumAreaCitySites,
						iAreaBestFoundValue, iNumWaterAreaCitySites, iWaterAreaBestFoundValue);
				// </advc.031b>
				if (AI_chooseUnit(UNITAI_SETTLE, //bLandWar ? 50 : -1))
					// advc.031b: Replacing the above
					iSettlerPriority * (bLandWar ? 1 : 2)))
				{
					if (gCityLogLevel >= 2) logBBAI("      City %S uses build settler 1", getName().GetCString());
					if (kPlayer.getNumMilitaryUnits() <= kPlayer.getNumCities() + 1)
					{
						if (AI_chooseUnit(UNITAI_CITY_DEFENSE))
						{
							if (gCityLogLevel >= 2) logBBAI("      City %S uses build settler 1 extra quick defense", getName().GetCString());
							return;
						}
					}
					return;
				}
			}
		}
	}

	// don't build frivolous things in an important culture city unless at war
	if (!bCultureCity || bLandWar || bAssault)
	{
		if (bPrimaryArea && !bFinancialTrouble)
		{
			if (kPlayer.AI_totalAreaUnitAIs(kArea, UNITAI_ATTACK) == 0)
			{
				if (AI_chooseUnit(UNITAI_ATTACK))
				{
					if (gCityLogLevel >= 2) logBBAI("      City %S uses choose attacker", getName().GetCString()); // advc
					return;
				}
			}
		}

		if (!bLandWar && !bDanger && !bFinancialTrouble)
		{
			int iMissingExplorers = kPlayer.AI_neededExplorers(kArea) -
					kPlayer.AI_totalAreaUnitAIs(kArea, UNITAI_EXPLORE);
			if (iMissingExplorers > 0)
			{
				if (AI_chooseUnit(UNITAI_EXPLORE,
					34 * iMissingExplorers)) // advc.131: was 100 flat (MNAI uses 25 flat)
				{
					if (gCityLogLevel >= 2) logBBAI("      City %S uses choose missing explorer", getName().GetCString()); // advc
					return;
				}
			}
		}

		// K-Mod (the spies stuff used to be lower down)
		int iNumSpies = kPlayer.AI_totalAreaUnitAIs(kArea, UNITAI_SPY);
				// advc.001j: already counted
				//+ kPlayer.AI_getNumTrainAIUnits(UNITAI_SPY);
		int iNeededSpies = iNumCitiesInArea / 3;
		if (bPrimaryArea)
			iNeededSpies += intdiv::uround(kPlayer.getCommerceRate(COMMERCE_ESPIONAGE), 100);
		iNeededSpies *= GC.getInfo(kPlayer.getPersonalityType()).getEspionageWeight();
		iNeededSpies /= 100;
		{
			if (pCapital != NULL && sameArea(*pCapital))
				iNeededSpies++;
		}
		iNeededSpies -= (bDefenseWar ? 1 : 0);
		if (kPlayer.AI_isDoStrategy(AI_STRATEGY_ESPIONAGE_ECONOMY))
			iNeededSpies++;
		else iNeededSpies /= kPlayer.AI_isDoStrategy(AI_STRATEGY_ECONOMY_FOCUS) ? 2 : 1;

		if (iNumSpies < iNeededSpies)
		{
			int iOdds = 35;
			if (kPlayer.AI_isDoStrategy(AI_STRATEGY_ESPIONAGE_ECONOMY))
				//|| kTeam.getAnyWarPlanCount(true)
				//|| kPlayer.AI_isFocusWar(&kArea)) // advc.105: if anything ...
			{
				iOdds += 10;
			}
			/*  <advc.120> ... but, actually, I don't think training extra
				spies during war is a good idea at all. */
			else if (kTeam.AI_getNumWarPlans(WARPLAN_PREPARING_TOTAL) > 0)
				iOdds += 10;
			else if (kTeam.AI_getNumWarPlans(WARPLAN_PREPARING_LIMITED) > 0)
				iOdds += 5; // </advc.120>
			iOdds *= 50 + std::max(iProjectValue, iBestBuildingValue);
			iOdds /= 20 + 2 * std::max(iProjectValue, iBestBuildingValue);
			iOdds *= iNeededSpies;
			iOdds /= 4*iNumSpies + iNeededSpies;
			iOdds -= bUnitExempt ? 10 : 0; // not completely exempt, but at least reduced probability.
			iOdds = std::max(0, iOdds);
			if (AI_chooseUnit(UNITAI_SPY, iOdds))
			{
				if (gCityLogLevel >= 2) logBBAI("      City %S chooses spy with %d/%d needed, at %d odds", getName().GetCString(), iNumSpies, iNeededSpies, iOdds);
				return;
			}
		}
	    // K-Mod end

        // doc
	    if (!(bLandWar && bMajorWar) && !bDanger)
	    {
	        if (kPlayer.AI_totalAreaUnitAIs(pArea, UNITAI_EXPLORE) < (kPlayer.AI_neededExplorers(pArea)))
	        {
	            if (AI_chooseUnit(UNITAI_EXPLORE))
	            {
	                return;
	            }
	        }
	    }

		if (bDefenseWar || (bLandWar && iWarSuccessRating < -30))
		{
			UnitAIWeightMap panicDefenderWeight; // advc: Was vector of pairs "defensiveTypes"
			panicDefenderWeight.set(UNITAI_RESERVE, 100);
			panicDefenderWeight.set(UNITAI_COUNTER, 100);
			panicDefenderWeight.set(UNITAI_COLLATERAL, 100);
			panicDefenderWeight.set(UNITAI_ATTACK, 100);
			if (AI_chooseLeastRepresentedUnit(panicDefenderWeight,
				(bGetBetterUnits ? 40 : 60) - iWarSuccessRating/3))
			{
				if (gCityLogLevel >= 2) logBBAI("      City %S uses choose panic defender", getName().GetCString());
				return;
			}
		}
	}

	/*	<advc.124> Could've modified the K-Mod condition above, but that one
		is aimed at exploration for the sake of initial meetings and expansion,
		not (specifically) at trade. Rather handle trade here separately. */
	if (!bDanger && !bDefenseWar && pWaterArea != NULL && iSeaExplorersNow == 0)
	{
		bool bNavalTrade = false;
		FOR_EACH_ENUM(Terrain)
		{
			if(GC.getInfo(eLoopTerrain).isWater() &&
				GET_TEAM(getOwner()).isTerrainTrade(eLoopTerrain))
			{
				bNavalTrade = true;
				break;
			}
		}
		if (bNavalTrade)
		{
			/*	Don't rely on seaExplorersTarget. Can be 0 if already met all
				other civs or if there is a larger separate water area. */
			bool bEnoughWaterUnits = false;
			int iWaterUnits = 0;
			for (MemberIter itMember(getTeam()); itMember.hasNext(); ++itMember)
			{
				iWaterUnits += pWaterArea->getNumAIUnits(itMember->getID(), NO_UNITAI);
				if (iWaterUnits >= 3)
				{
					bEnoughWaterUnits = true;
					break;
				}
			}
			/*	Would rather use a condition based on the number of unrevealed
				tiles, but it's difficult to count just the tiles that an explorer
				could actually reach. */
			if (!bEnoughWaterUnits && AI_chooseUnit(UNITAI_EXPLORE_SEA, 25))
			{
				if (gCityLogLevel >= 2) logBBAI("      City %S uses choose sea explorer for naval trade", getName().GetCString());
				return;
			}
		}
	} // </advc.124>

	// We don't need this. It just ends up putting aqueducts everywhere.
	/*if (AI_chooseBuilding(BUILDINGFOCUS_FOOD, 60, 10, (bLandWar ? 30 : -1))) {
		if (gCityLogLevel >= 2) logBBAI("      City %S uses choose BUILDINGFOCUS_FOOD 3", getName().GetCString());
		return;
	}*/ // BtS

	//opportunistic wonder build
	if (!bDanger && (!hasActiveWorldWonder() || kPlayer.getNumCities() > 3))
	{
		// For civ at war, don't build wonders if losing
		if (!bTotalWar && (!bLandWar || iWarSuccessRating > 0)) // was -30
		{
			int iWonderTime = SyncRandNum(GC.getInfo(getPersonalityType()).
					getWonderConstructRand());
			iWonderTime /= 5;
			iWonderTime += 8;
			/*if (AI_chooseBuilding(BUILDINGFOCUS_WORLDWONDER, iWonderTime)) {
				if (gCityLogLevel >= 2) logBBAI("      City %S uses opportunistic wonder build 2", getName().GetCString());
				return;
			}*/
			// K-Mod
			/*	Reduce the max time when at war
				(arbitrary - but then again, this part of the AI is not for strategy.
				It's for flavour.) */
			if (kArea.getAreaAIType(getTeam()) != AREAAI_NEUTRAL)
				iWonderTime = iWonderTime * 2/3;
			// And only build the wonder if it is at least as valuable as the building we would have chosen anyway.
			BuildingTypes eBestWonder = AI_bestBuildingThreshold(BUILDINGFOCUS_WORLDWONDER, iWonderTime);
			if (eBestWonder != NO_BUILDING && AI_buildingValue(eBestWonder) >= iBestBuildingValue)
			{
				if (gCityLogLevel >= 2) logBBAI("      City %S uses opportunistic wonder build 2", getName().GetCString());
				pushOrder(ORDER_CONSTRUCT, eBestWonder);
				return;
			} // K-Mod end
		}
	}

	// K-Mod, short-circuit 2 - a strong chance to build some high value buildings.
	{
		bool const bLowOdds = (bLandWar || (bAssault && pWaterArea != NULL));
		bool const bExtraLowOdds = (bLowOdds && bWarPrep); // advc.104s
		//int iOdds = (bLowOdds ? 80 : 130);
		int iOdds = (bLowOdds ? (bExtraLowOdds ?
				(bTotalWar ? 77 : 84) - iBuildUnitProb/3 : // advc.104s
				90 - iBuildUnitProb/4) :
				150 - iBuildUnitProb/2);
		iOdds *= iBestBuildingValue;
		iOdds /= iBestBuildingValue + 40 + iBuildUnitProb; // was ...+20+...
		iOdds = std::max(0, iOdds - 20); // was -25
		if (AI_chooseBuilding(0, MAX_INT, 0, iOdds))
		{
			if (gCityLogLevel >= 2) logBBAI("      City %S uses building value short-circuit 2 (odds: %d)", getName().GetCString(), iOdds);
   			return;
		}
	}
	// <advc.081>
	if(pWaterArea != NULL && !bUnitExempt && !bCultureCity &&
		iEnemyPowerPerc - iWarSuccessRating < 150 && // else give up at sea
		kTeam.getNumWars(false, true) > 0) // for performance
	{
		int iHostile = kPlayer.AI_countNumAreaHostileUnits(*pWaterArea, true, false, false, false, plot());
		if(iHostile > 0)
		{
			int iOurWarships = 0;
			std::vector<UnitAITypes> aeSeaAttackTypes;
			aeSeaAttackTypes.push_back(UNITAI_ATTACK_SEA);
			aeSeaAttackTypes.push_back(UNITAI_PIRATE_SEA);
			aeSeaAttackTypes.push_back(UNITAI_RESERVE_SEA);
			for(size_t i = 0; i < aeSeaAttackTypes.size(); i++)
				iOurWarships += kPlayer.AI_getNumTrainAIUnits(aeSeaAttackTypes[i]);
			if(3 * iOurWarships < 4 * iHostile) // for performance
			{
				iOurWarships += kPlayer.AI_totalWaterAreaUnitAIs(*pWaterArea, aeSeaAttackTypes);
				if(3 * iOurWarships < 4 * iHostile) // Odds: 0.75*35% to 70% plus 2*XP
				{
					int iOdds = (35 * iHostile) / std::max(iHostile/2, std::max(1, iOurWarships));
					iOdds += 2 * iFreeSeaExperience;
					if(AI_chooseUnit(UNITAI_ATTACK_SEA, iOdds))
					{
						if (gCityLogLevel >= 2) logBBAI("      City %S trains warship to attack hostiles in territory", getName().GetCString());
						return;
					}
				}
			}
		}
	} // </advc.081>
	if (!bDanger)
	{
        // doc: not for independents
		if (!isIndependent() && iBestSpreadUnitValue > (iSpreadUnitThreshold * (bLandWar ? 80 : 60)) / 100)
		{
			if (AI_chooseUnit(eBestSpreadUnit, UNITAI_MISSIONARY))
			{
				if (gCityLogLevel >= 2) logBBAI("      City %S uses choose missionary 2", getName().GetCString());
				return;
			}
			FErrorMsg("AI_bestSpreadUnit should provide a valid unit when it returns true");
		}
	}

	if (getDomainFreeExperience(DOMAIN_LAND) == 0 && getYieldRate(YIELD_PRODUCTION) > 4)
	{
		if (AI_chooseBuilding(BUILDINGFOCUS_EXPERIENCE,
			rOwnerAIEraFactor > 1 ? 0 : 7, 33))
		{
			if (gCityLogLevel >= 2) logBBAI("      City %S uses special BUILDINGFOCUS_EXPERIENCE 1", getName().GetCString());
			return;
		}
	}

	int iCarriers = kPlayer.AI_totalUnitAIs(UNITAI_CARRIER_SEA);

	// Revamped logic for production for invasions
	if (iUnitSpending < iMaxUnitSpending + 25) // was + 10 (new unit spending metric)
	{
		bool bBuildAssault = bAssault;
		CvArea* pAssaultWaterArea = NULL;
		if (pWaterArea != NULL)
		{
			// Coastal city extra logic

			pAssaultWaterArea = pWaterArea;

			// If on offensive and can't reach enemy cities from here, act like using AREAAI_ASSAULT
			if (pAssaultWaterArea != NULL && !bBuildAssault && kTeam.AI_isAnyWarPlan() &&
				kArea.getAreaAIType(getTeam()) != AREAAI_DEFENSIVE)
			{
				// <advc.030b>
				bool bAssaultTargetFound = false;
				for (PlayerIter<CIV_ALIVE,KNOWN_POTENTIAL_ENEMY_OF> itTarget(getTeam());
					itTarget.hasNext(); ++itTarget)
				{
					if(kTeam.AI_getWarPlan(itTarget->getTeam()) == NO_WARPLAN)
						continue;
					if(pWaterArea->getCitiesPerPlayer(itTarget->getID(), true) > 0)
					{
						bAssaultTargetFound = true;
						break;
					}
				}
				if (!bAssaultTargetFound)
					pAssaultWaterArea = NULL;
				if (bAssaultTargetFound && // </advc.030b>
					!GET_TEAM(getTeam()).AI_isHasPathToEnemyCity(getPlot()))
				{
					bBuildAssault = true;
				}
			}
		}

		if (bBuildAssault)
		{
			if (gCityLogLevel >= 2) logBBAI("      City %S uses build assault", getName().GetCString());

			UnitTypes eBestAssaultUnit = NO_UNIT;
			if (pAssaultWaterArea != NULL)
				kPlayer.AI_bestCityUnitAIValue(UNITAI_ASSAULT_SEA, this, &eBestAssaultUnit);
			else kPlayer.AI_bestCityUnitAIValue(UNITAI_ASSAULT_SEA, NULL, &eBestAssaultUnit);

			int iBestSeaAssaultCapacity = 0;
			if (eBestAssaultUnit != NO_UNIT)
				iBestSeaAssaultCapacity = GC.getInfo(eBestAssaultUnit).getCargoSpace();

			int iAreaAttackCityUnits = kPlayer.AI_totalAreaUnitAIs(kArea, UNITAI_ATTACK_CITY);

			int iUnitsToTransport = iAreaAttackCityUnits;
			iUnitsToTransport += kPlayer.AI_totalAreaUnitAIs(kArea, UNITAI_ATTACK);
			iUnitsToTransport += kPlayer.AI_totalAreaUnitAIs(kArea, UNITAI_COUNTER)/2;

			int const iLocalTransports = kPlayer.AI_totalAreaUnitAIs(kArea, UNITAI_ASSAULT_SEA);
			int iTransportsAtSea = 0;
			if (pAssaultWaterArea != NULL)
				iTransportsAtSea = kPlayer.AI_totalAreaUnitAIs(*pAssaultWaterArea, UNITAI_ASSAULT_SEA);
			else iTransportsAtSea = kPlayer.AI_totalUnitAIs(UNITAI_ASSAULT_SEA) / 2;

			/*	The way of calculating numbers is a bit fuzzy since the ships
				can make return trips. When massing for a war it'll train enough
				ships to move it's entire army. Once the war is underway it'll stop
				training so many ships on the assumption that those out at sea
				will return... */

			int const iTransports = iLocalTransports + (bPrimaryArea ?
					iTransportsAtSea/2 : iTransportsAtSea/4);
			int const iTransportCapacity = iBestSeaAssaultCapacity * iTransports;

			if (pAssaultWaterArea != NULL)
			{
				int iEscorts = kPlayer.AI_totalAreaUnitAIs(kArea, UNITAI_ESCORT_SEA);
				iEscorts += kPlayer.AI_totalAreaUnitAIs(*pAssaultWaterArea, UNITAI_ESCORT_SEA);

				int iTransportViability = kPlayer.AI_calculateUnitAIViability(
						UNITAI_ASSAULT_SEA, DOMAIN_SEA);

				//int iDesiredEscorts = ((1 + 2 * iTransports) / 3);
				int iDesiredEscorts = iTransports; // K-Mod

				if (iTransportViability > 95)
				{
					// Transports are stronger than escorts (usually Galleons and Caravels)
					iDesiredEscorts /= 2; // was /3
				}
				// <advc.017>
				iDesiredEscorts = ((rOwnerAIEraFactor * iDesiredEscorts) /
						(rOwnerAIEraFactor + 1)).round();
				/*  Use max, not sum, b/c multiple war enemies are unlikely
					to coordinate an attack on our transports. */
				scaled rMaxThreat = 0;
				for (PlayerAIIter<CIV_ALIVE,KNOWN_POTENTIAL_ENEMY_OF> it(kTeam.getID());
					it.hasNext(); ++it)
				{
					CvPlayerAI const& kEnemy = *it;
					if (kTeam.AI_getWarPlan(kEnemy.getMasterTeam()) == NO_WARPLAN)
						continue;
					/*  Tbd.: Should perhaps check if the enemy sea attackers even
						pose a danger to our cargo ships; could be e.g. Frigates
						against Industrial-era Transports. */
					bool bAreaAlone = kEnemy.AI_isCapitalAreaAlone();
					scaled rThreat;
					/*  Don't want to just count the enemy ships (not open info);
						count their coastal cities instead. */
					FOR_EACH_CITY(c, kEnemy)
					{
						if(c->isRevealed(kTeam.getID()) &&
							c->getPlot().isAdjacentToArea(*pAssaultWaterArea))
						{
							// Isolated civs tend to build more ships
							rThreat += (bAreaAlone ? fixp(1.4) : 1);
						}
					}
					rMaxThreat.increaseTo(rThreat);
				}
				iDesiredEscorts = std::min(iDesiredEscorts,
						(fixp(1.4) * rMaxThreat).round());
				iDesiredEscorts = std::max(iDesiredEscorts,
						((rOwnerAIEraFactor / 2) * rMaxThreat).round());
				// </advc.017>
				/*if (iEscorts < iDesiredEscorts) {
					if (AI_chooseUnit(UNITAI_ESCORT_SEA, (iEscorts < iDesiredEscorts/3) ? -1 : 50)) */
				// K-Mod
				if (iEscorts < iDesiredEscorts && iDesiredEscorts > 0)
				{
					int iOdds = 100;
					iOdds *= iDesiredEscorts;
					iOdds /= iDesiredEscorts + 2*iEscorts;
					if (AI_chooseUnit(UNITAI_ESCORT_SEA, iOdds))
				// K-Mod end
					{
						AI_chooseBuilding(BUILDINGFOCUS_DOMAINSEA, 12);
						return;
					}
				}

				UnitTypes eBestAttackSeaUnit = NO_UNIT;
				kPlayer.AI_bestCityUnitAIValue(UNITAI_ATTACK_SEA, this, &eBestAttackSeaUnit);
				if (eBestAttackSeaUnit != NO_UNIT)
				{
					// (tweaked for K-Mod)
					int iAttackSea = kPlayer.AI_totalAreaUnitAIs(kArea, UNITAI_ATTACK_SEA);
					iAttackSea += kPlayer.AI_totalAreaUnitAIs(*pAssaultWaterArea, UNITAI_ATTACK_SEA);

					int iDesiredAttackSea = 1 + 4*iTransports /
							(GC.getInfo(eBestAttackSeaUnit).getBombardRate() == 0 ? 10 : 3);
					// <advc.017>
					/*  Don't build lots of sea attackers if we already have
						lots of escorts */
					iDesiredAttackSea = std::max(1 + iDesiredAttackSea / 3,
							iDesiredAttackSea - iEscorts); // </advc.017>
					if (iAttackSea < iDesiredAttackSea)
					{
						int iOdds = 20 + 50 * (iDesiredAttackSea - iAttackSea)/iDesiredAttackSea;
						if (iUnitSpending > iMaxUnitSpending)
							iOdds /= 3;
						// Note: there is a hard limit condition on iUnitSpending earlier in the code.

						if (SyncRandSuccess100(iOdds) &&
							AI_chooseUnit(eBestAttackSeaUnit, UNITAI_ATTACK_SEA))
						{
							AI_chooseBuilding(BUILDINGFOCUS_DOMAINSEA, 12);
							return;
						}
					}
				}
				/*  <advc.104p> Cargo space isn't that expensive; make sure
					AI landings don't get delayed by a lack of transport capacity.
					Existing cargo units can also be stuck somewhere. */
				int iTargetCapacity = intdiv::uround(5 * iUnitsToTransport, 4);
				if(iTargetCapacity > iTransportCapacity) // </advc.104p>
				{
					//if ((iUnitSpending < iMaxUnitSpending) || (iUnitsToTransport > 2*iTransportCapacity))
					// K-Mod
					if (iUnitSpending < iMaxUnitSpending ||
						SyncRandSuccess100(
						// advc.104p: Changed 100 to 350
						(350 * (iTargetCapacity - iTransportCapacity)) /
						std::max(1, iTransportCapacity)))
					// K-Mod end
					{
						if (AI_chooseUnit(UNITAI_ASSAULT_SEA))
						{
							AI_chooseBuilding(BUILDINGFOCUS_DOMAINSEA, 8);
							return;
						}
					}
				}
			}

			if (iUnitSpending < iMaxUnitSpending)
			{
				if (pAssaultWaterArea != NULL)
				{
					if (!bFinancialTrouble && iCarriers < (kPlayer.AI_totalUnitAIs(UNITAI_ASSAULT_SEA) / 4))
					{
						// Reduce chances of starting if city has low production
						if (AI_chooseUnit(UNITAI_CARRIER_SEA, (iProductionRank <= ((kPlayer.getNumCities() / 3) + 1)) ? -1 : 30))
						{
							AI_chooseBuilding(BUILDINGFOCUS_DOMAINSEA, 16);
							return;
						}
					}
				}
			}

			// Consider building more land units to invade with
			int iTrainInvaderChance = iBuildUnitProb + 10;

			iTrainInvaderChance += (bAggressiveAI ? 8 : 0); // advc.019: was ?15:0
			iTrainInvaderChance += bTotalWar ? 10 : 0; // K-Mod
			iTrainInvaderChance /= (bAssaultAssist ? 2 : 1);
			iTrainInvaderChance /= (bCultureCity ? 2 : 1);
			iTrainInvaderChance /= (bGetBetterUnits ? 2 : 1);

			// K-Mod
			iTrainInvaderChance *= (100 + std::max(iProjectValue, iBestBuildingValue));
			iTrainInvaderChance /= (20 + 3 * std::max(iProjectValue, iBestBuildingValue));
			// K-Mod end

			iUnitsToTransport *= 9;
			iUnitsToTransport /= 10;

			if (iUnitsToTransport > iTransportCapacity && iUnitsToTransport > (bAssaultAssist ? 2 : 4)*iBestSeaAssaultCapacity)
			{
				// Already have enough
				iTrainInvaderChance /= 2;
			}
			else if (iUnitsToTransport < (iLocalTransports*iBestSeaAssaultCapacity))
			{
				iTrainInvaderChance += 8; // advc.019: was 15
			}

			if (getPopulation() < 4)
			{
				// Let small cities build themselves up first
				iTrainInvaderChance /= (5 - getPopulation());
			}

			UnitAIWeightMap invaderWeight; // advc: Was vector of pairs "defensiveTypes"
			invaderWeight.set(UNITAI_ATTACK_CITY, 110); // was 100
			invaderWeight.set(UNITAI_COUNTER, 40); // was 50
			invaderWeight.set(UNITAI_ATTACK, 50); // was 40
			if (kPlayer.AI_isDoStrategy(AI_STRATEGY_AIR_BLITZ))
				invaderWeight.set(UNITAI_PARADROP, 20);

			if (AI_chooseLeastRepresentedUnit(invaderWeight, iTrainInvaderChance))
			{
				if (!bCultureCity && iUnitsToTransport >=
					iLocalTransports*iBestSeaAssaultCapacity)
				{	// Have time to build barracks first
					AI_chooseBuilding(BUILDINGFOCUS_EXPERIENCE, 20);
				}
				return;
			}
			// kekm.15: missile carrier code moved
		}
	}

	UnitAIWeightMap airWeight; // advc: Was vector of pairs "airUnitTypes"
	int iAircraftNeed = 0;
	int iAircraftHave = 0;
	UnitTypes eBestAttackAircraft = NO_UNIT;
	UnitTypes eBestMissile = NO_UNIT;
	// K-Mod. was +4, now +12 for the new unit spending metric
	if (iUnitSpending < iMaxUnitSpending + 12 && (!bCultureCity || bDefenseWar))
	{
		if (bLandWar || bAssault || iFreeAirExperience > 0 || SyncRandOneChanceIn(3))
		{
			int iBestAirValue = kPlayer.AI_bestCityUnitAIValue(
					UNITAI_ATTACK_AIR, this, &eBestAttackAircraft);
			int iBestMissileValue = kPlayer.AI_bestCityUnitAIValue(
					UNITAI_MISSILE_AIR, this, &eBestMissile);
			if ((iBestAirValue + iBestMissileValue) > 0)
			{
				iAircraftHave = kPlayer.AI_totalUnitAIs(UNITAI_ATTACK_AIR) +
						kPlayer.AI_totalUnitAIs(UNITAI_DEFENSE_AIR) +
						kPlayer.AI_totalUnitAIs(UNITAI_MISSILE_AIR);
				if (NO_UNIT != eBestAttackAircraft)
				{
					iAircraftNeed = (2 + kPlayer.getNumCities() *
							(3 * GC.getInfo(eBestAttackAircraft).getAirCombat())) /
							(2 * std::max(1, kGame.getBestLandUnitCombat()));
					int iBestDefenseValue = kPlayer.AI_bestCityUnitAIValue(
							UNITAI_DEFENSE_AIR, this);
					if (iBestDefenseValue > 0)
					{	// <K-Mod>
						iAircraftNeed = std::max(iAircraftNeed,
								kPlayer.AI_getTotalAirDefendersNeeded()); // </K-Mod>
						if (iBestAirValue > iBestDefenseValue)
							iAircraftNeed = iAircraftNeed*3/2;
					}
					/* if ((iBestDefenseValue > 0) && (iBestAirValue > iBestDefenseValue))
					{
						iAircraftNeed *= 3;
						iAircraftNeed /= 2;
					} */ // (bts code, reworded above.)
				}
				if (iBestMissileValue > 0)
				{
					iAircraftNeed = std::max(iAircraftNeed, 1 + kPlayer.getNumCities() / 2);
				}

				bool bAirBlitz = kPlayer.AI_isDoStrategy(AI_STRATEGY_AIR_BLITZ);
				bool bLandBlitz = kPlayer.AI_isDoStrategy(AI_STRATEGY_LAND_BLITZ);
				if (bAirBlitz)
				{
					iAircraftNeed *= 3;
					iAircraftNeed /= 2;
				}
				else if (bLandBlitz)
				{
					iAircraftNeed /= 2;
					iAircraftNeed += 1;
				}

				airWeight.set(UNITAI_ATTACK_AIR, bAirBlitz ? 125 : 80);
				airWeight.set(UNITAI_DEFENSE_AIR, /*bLandBlitz ? 100 : 100*/ 100); // advc: huh?
				if (iBestMissileValue > 0)
					airWeight.set(UNITAI_MISSILE_AIR, bAssault ? 60 : 40);

				//airWeight.set(UNITAI_ICBM, 20);
				airWeight.set(UNITAI_ICBM, 20 * iNukeWeight / 100); // K-Mod

				if (iAircraftHave * 2 < iAircraftNeed)
				{
					if (AI_chooseLeastRepresentedUnit(airWeight))
					{
						if (gCityLogLevel >= 2) logBBAI("      City %S uses build least represented air", getName().GetCString());
						return;
					}
				}
				// Additional check for air defenses
				int iFightersHave = kPlayer.AI_totalUnitAIs(UNITAI_DEFENSE_AIR);

				if(3*iFightersHave < iAircraftNeed)
						// <cdtw.7> (Disabled again)
						/*(kPlayer.AI_atVictoryStage(AI_VICTORY_CULTURE4) &&
						3*iFightersHave < 2*kPlayer.getNumCities())) */// </cdtw.7>
				{
					if (AI_chooseUnit(UNITAI_DEFENSE_AIR))
					{
						if (gCityLogLevel >= 2) logBBAI("      City %S uses build air defence", getName().GetCString());
						return;
					}
				}
			}
		}
	}

	// Check for whether to produce planes to fill carriers
	if ((bLandWar || bAssault) && iUnitSpending < iMaxUnitSpending)
	{
		if (iCarriers > 0 && !bCultureCity)
		{
			UnitTypes eBestCarrierUnit = NO_UNIT;
			kPlayer.AI_bestCityUnitAIValue(UNITAI_CARRIER_SEA, NULL, &eBestCarrierUnit);
			if (eBestCarrierUnit != NO_UNIT)
			{
				FAssert(GC.getInfo(eBestCarrierUnit).getDomainCargo() == DOMAIN_AIR);

				int iCarrierAirNeeded = iCarriers * GC.getInfo(eBestCarrierUnit).getCargoSpace();

				// Reduce chances if city gives no air experience
				if (kPlayer.AI_totalUnitAIs(UNITAI_CARRIER_AIR) < iCarrierAirNeeded)
				{
					if (AI_chooseUnit(UNITAI_CARRIER_AIR, (iFreeAirExperience > 0) ? -1 : 35))
					{
						if (gCityLogLevel >= 2) logBBAI("      City %S uses build carrier air", getName().GetCString());
						return;
					}
				}
			}
		}
	} // <kekm.15>
	int iMissileCarriers = kPlayer.AI_totalUnitAIs(UNITAI_MISSILE_CARRIER_SEA);
	if (!bFinancialTrouble && iMissileCarriers > 0 && !bCultureCity)
	{	// Bugfix(?): was '<=' in BtS
		// advc: Make it '>=' though, not '>'.
		if (iProductionRank >= kPlayer.getNumCities() / 2 + 1)
		{
			UnitTypes eBestMissileCarrierUnit = NO_UNIT;
			kPlayer.AI_bestCityUnitAIValue(UNITAI_MISSILE_CARRIER_SEA, NULL, &eBestMissileCarrierUnit);
			if (eBestMissileCarrierUnit != NO_UNIT)
			{
				FAssert(GC.getInfo(eBestMissileCarrierUnit).getDomainCargo() == DOMAIN_AIR);

				int iMissileCarrierAirNeeded = iMissileCarriers * GC.getInfo(eBestMissileCarrierUnit).getCargoSpace();

				if ((kPlayer.AI_totalUnitAIs(UNITAI_MISSILE_AIR) < iMissileCarrierAirNeeded) ||
						(bPrimaryArea && (kPlayer.AI_totalAreaUnitAIs(kArea, UNITAI_MISSILE_CARRIER_SEA) *
						GC.getInfo(eBestMissileCarrierUnit).getCargoSpace()
						// Bugfix: was '<' in BtS
						> kPlayer.AI_totalAreaUnitAIs(kArea, UNITAI_MISSILE_AIR))))
				{
					// Don't always build missiles, more likely if really low on missiles.
					if (AI_chooseUnit(UNITAI_MISSILE_AIR, (kPlayer.AI_totalUnitAIs(UNITAI_MISSILE_AIR) < iMissileCarrierAirNeeded/2) ? 50 : 20))
					{
						if (gCityLogLevel >= 2) logBBAI("      City %S uses build missile", getName().GetCString());
						return;
					}
				}
			}
		}
	} // </kekm.15>

	/*if (!bAlwaysPeace && !(bLandWar || bAssault) && (kPlayer.AI_isDoStrategy(AI_STRATEGY_OWABWNW) || SyncRandOneChanceIn(12))) {
		if (!bFinancialTrouble) {
			int iTotalNukes = kPlayer.AI_totalUnitAIs(UNITAI_ICBM);
			int iNukesWanted = 1 + 2 * std::min(kPlayer.getNumCities(), kGame.getNumCities() - kPlayer.getNumCities());
			if ((iTotalNukes < iNukesWanted) && (SyncRandNum(100) < (90 - (80 * iTotalNukes) / iNukesWanted))) {
				if (pWaterArea != NULL) {
					if (AI_chooseUnit(UNITAI_MISSILE_CARRIER_SEA, 50))
						return;
				}
				if (AI_chooseUnit(UNITAI_ICBM))
					return;
			}
		}
	}*/ // BtS
	/*	K-Mod. Roughly the same conditions for building a nuke,
		but with a few adjustments for flavour and strategy */
    // doc: only exclude major war
	if (!(bLandWar && bMajorWar) && !bUnitExempt && !bFinancialTrouble &&
		iNukeWeight > 0) // advc.143b
	{
		if ((kPlayer.AI_isDoStrategy(AI_STRATEGY_OWABWNW) ||
			SyncRandNum(1200) < std::min(400, iNukeWeight)) &&
			(!bAssault || SyncRandNum(400) < std::min(200, 50 + iNukeWeight/2)))
		{
			int iTotalNukes = kPlayer.AI_totalUnitAIs(UNITAI_ICBM);
			int iNukesWanted = 1 + 2 * std::min(kPlayer.getNumCities(),
					kGame.getNumCities() - kPlayer.getNumCities());
			if (iTotalNukes < iNukesWanted &&
				SyncRandNum(100) * iNukesWanted < 90 - (80 * iTotalNukes))
			{
				if (pWaterArea != NULL &&
					kPlayer.AI_totalUnitAIs(UNITAI_MISSILE_CARRIER_SEA) * 2 < iTotalNukes &&
					SyncRandOneChanceIn(3))
				{
					if (AI_chooseUnit(UNITAI_MISSILE_CARRIER_SEA, 50))
						return;
				}
				if (AI_chooseUnit(UNITAI_ICBM))
					return;
			}
		}
	}
	// K-Mod end

	// Assault case now completely handled above
	if (!bAssault && (!bCultureCity || bDefenseWar) && iUnitSpending < iMaxUnitSpending)
	{
		if (!bFinancialTrouble && (bLandWar || (bDagger && !bGetBetterUnits)))
		{	// <advc.081>
			bool bNavalSiege = false;
			bool bAssaultAlongCoast = false;
			// </advc.081>
			//int iTrainInvaderChance = iBuildUnitProb + 10;
			int iTrainInvaderChance = iBuildUnitProb + (bTotalWar ? 16 : 8); // K-Mod

			if (bAggressiveAI)
				iTrainInvaderChance += 5; // advc.019: was +15

			if (bGetBetterUnits)
				iTrainInvaderChance /= 2;
			else if (kArea.getAreaAIType(getTeam()) == AREAAI_MASSING ||
				kArea.getAreaAIType(getTeam()) == AREAAI_ASSAULT_MASSING)
			{
				iTrainInvaderChance = (100 - ((100 - iTrainInvaderChance) /
						// advc.018: Was 6 in the Crush case
						(bCrushStrategy ? 2 : 3)));
				// <advc.081>
				CvCity* pTargetCity = kArea.AI_getTargetCity(kPlayer.getID());
				if(pTargetCity != NULL && sameArea(*pTargetCity) &&
					pWaterArea != NULL && pWaterArea == pTargetCity->waterArea(true) &&
					(!pTargetCity->isVisible(kPlayer.getTeam()) ||
					pTargetCity->getDefenseModifier(true) > 10))
				{
					bAssaultAlongCoast = true;
					UnitTypes eBestNavalSiege = AI_bestUnitAI(UNITAI_ATTACK_SEA);
					if(eBestNavalSiege != NO_UNIT &&
						GC.getInfo(eBestNavalSiege).getBombardRate() >= 8)
					{
						bNavalSiege = true;
					}
				} // </advc.081>
			}

			if (AI_chooseBuilding(BUILDINGFOCUS_EXPERIENCE, 20, 0, bDefenseWar ? 10 : 30))
			{
				if (gCityLogLevel >= 2) logBBAI("      City %S uses special BUILDINGFOCUS_EXPERIENCE 2", getName().GetCString()); // advc
				return;
			}

			UnitAIWeightMap invaderWeight; // advc: Was vector of pairs "invaderTypes"
			invaderWeight.set(UNITAI_ATTACK_CITY,// 100
					// <advc.081>
					bNavalSiege ? 96 : 100);
			if(bNavalSiege)
				invaderWeight.set(UNITAI_ATTACK_SEA, 8);
			if(bAssaultAlongCoast) {
				invaderWeight.set(UNITAI_ASSAULT_SEA, 8 -
						(bNavalSiege ? 4 : 0));
			} // </advc.081>
			invaderWeight.set(UNITAI_COUNTER, 50);
			invaderWeight.set(UNITAI_ATTACK, 40);
			invaderWeight.set(UNITAI_PARADROP,
					(kPlayer.AI_isDoStrategy(AI_STRATEGY_AIR_BLITZ) ? 30 : 20) /
					(bAssault ? 2 : 1));
			//if (!bAssault)
			//if (!bAssault && !bCrushStrategy) // K-Mod
			if(!bCrushStrategy) // advc: !bAssault already guaranteed
			{
				if (kPlayer.AI_totalAreaUnitAIs(kArea, UNITAI_PILLAGE) <=
					(iNumCitiesInArea + 1) / 2)
				{
					invaderWeight.set(UNITAI_PILLAGE, 30);
				}
			}
			// K-Mod - get more siege units for crush
			if (bCrushStrategy && SyncRandSuccess100(iTrainInvaderChance))
			{
				// <cdtw.8> Moved up
				UnitTypes eCityAttackUnit = NO_UNIT;
				kPlayer.AI_bestCityUnitAIValue(UNITAI_ATTACK_CITY, this, &eCityAttackUnit);
				// </cdtw.8>
				if (eCityAttackUnit != NO_UNIT && GC.getInfo(eCityAttackUnit).getBombardRate() > 0)
				{
					if (AI_chooseUnit(eCityAttackUnit, UNITAI_ATTACK_CITY))
					{
						if (gCityLogLevel >= 2) logBBAI("      City %S uses extra crush bombard", getName().GetCString());
						return;
					}
				}
			}
			// K-Mod end
			// <cdtw.8> (Don't do this after all)
			/*if(iUnitSpending > (iBuildUnitProb / 2)) {
				if(eCityAttackUnit == NO_UNIT ||
					(!GC.getInfo(eCityAttackUnit).getUnitAIType(UNITAI_ATTACK_CITY) &&
					kPlayer.AI_bestCityUnitAIValue(UNITAI_ATTACK_CITY, this, &eCityAttackUnit) <= 110))
				iTrainInvaderChance /= 2;*/ // </cdtw.8>
			if (AI_chooseLeastRepresentedUnit(invaderWeight, iTrainInvaderChance))
				return;
		}
	}

	if (pWaterArea != NULL && !bDefenseWar && !bAssault)
	{
		if (!bFinancialTrouble)
		{
			// Force civs with foreign colonies to build a few assault transports to defend the colonies
			if (kPlayer.AI_totalUnitAIs(UNITAI_ASSAULT_SEA) < (kPlayer.getNumCities() - iNumCapitalAreaCities)/3)
			{
				if (AI_chooseUnit(UNITAI_ASSAULT_SEA))
					return;
			}

			if (kPlayer.AI_calculateUnitAIViability(UNITAI_SETTLER_SEA, DOMAIN_SEA) < 61)
			{
				// Force civs to build escorts for settler_sea units
				if (kPlayer.AI_totalUnitAIs(UNITAI_SETTLER_SEA) > kPlayer.AI_getNumAIUnits(UNITAI_RESERVE_SEA))
				{
					if (AI_chooseUnit(UNITAI_RESERVE_SEA))
						return;
				}
			}
		}
	}

    // doc: Arr.
	// Don't build pirates in financial trouble as they'll be disbanded with high probability
	if (pWaterArea != NULL && !bLandWar && !bAssault &&
		!bFinancialTrouble && !bUnitExempt &&
		!GET_TEAM(getTeam()).isCapitulated()) // advc.033
	{
		int iPirateCount = kPlayer.AI_totalWaterAreaUnitAIs(*pWaterArea, UNITAI_PIRATE_SEA);
		int iNeededPirates = 1 + (pWaterArea->getNumTiles() /
				std::max(1, 200 - iBuildUnitProb));
		iNeededPirates *= 20 + iWaterPercent;
		iNeededPirates /= 100;

		if (kPlayer.isNoForeignTrade())
		{
			iNeededPirates *= 3;
			iNeededPirates /= 2;
		}
		if (kPlayer.AI_totalWaterAreaUnitAIs(*pWaterArea, UNITAI_PIRATE_SEA) < iNeededPirates)
		{
			if (kPlayer.AI_calculateUnitAIViability(UNITAI_PIRATE_SEA, DOMAIN_SEA) > 49)
			{
				if (AI_chooseUnit(UNITAI_PIRATE_SEA, iWaterPercent / (1 + iPirateCount)))
					return;
			}
		}
	}

    // doc: only exclude major wars
	if (!(bLandWar && bMajorWar) && !bFinancialTrouble &&
		pWaterArea != NULL && iWaterPercent > 40 &&
		kPlayer.AI_totalAreaUnitAIs(kArea, UNITAI_SPY) > 0 &&
		kPlayer.AI_totalWaterAreaUnitAIs(*pWaterArea, UNITAI_SPY_SEA) == 0)
	{
		if (AI_chooseUnit(UNITAI_SPY_SEA))
			return;
	}

    // doc: not for independent
	if (!isIndependent() && iBestSpreadUnitValue > (iSpreadUnitThreshold * 40) / 100)
	{
		if (AI_chooseUnit(eBestSpreadUnit, UNITAI_MISSIONARY))
		{
			if (gCityLogLevel >= 2) logBBAI("      City %S uses choose missionary 3", getName().GetCString());
			return;
		}
		FErrorMsg("AI_bestSpreadUnit should provide a valid unit when it returns true");
	}

	if (!bUnitExempt && iTotalFloatingDefenders < iNeededFloatingDefenders &&
		(!bFinancialTrouble || bLandWar))
	{
		if (AI_chooseLeastRepresentedUnit(floatingDefenderWeight, 50))
		{
			if (gCityLogLevel >= 2) logBBAI("      City %S uses choose floating defender 2", getName().GetCString());
			return;
		}
	}

	if (bLandWar && !bDanger)
	{
		if (iPlotSettlerCount <= 0 && // advc.031b: Same condition as for "build settler 1"
			iNumSettlers < iMaxSettlers)
		{
			if (!bFinancialTrouble && iAreaBestFoundValue > iMinFoundValue)
			{	// <advc.031b>
				if(iSettlerPriority <= 0) // "build settler 1" may have already computed it
				{
					iSettlerPriority = AI_calculateSettlerPriority(iNumAreaCitySites,
							iAreaBestFoundValue, iNumWaterAreaCitySites, iWaterAreaBestFoundValue);
				} // </advc.031b>
				if (AI_chooseUnit(UNITAI_SETTLE, /* advc.031b: */ (iSettlerPriority * 3) / 2))
				{
					if (gCityLogLevel >= 2) logBBAI("      City %S uses build settler 2", getName().GetCString());
					return;
				}
			}
		}
	}

	//if ((iProductionRank <= ((kPlayer.getNumCities() > 8) ? 3 : 2))
	// Ideally we'd look at relative production, not just rank.
	if (iProductionRank <= kPlayer.getNumCities() / 9 + 2 && getPopulation() > 3)
	{
		int iWonderRand = 8 + SyncRandNum(GC.getInfo(getPersonalityType()).
				getWonderConstructRand());

		// increase chance of going for an early wonder
		if (kGame.getElapsedGameTurns() * 100 <
			100 * GC.getInfo(kGame.getGameSpeedType()).getConstructPercent() &&
			iNumCitiesInArea > 1)
		{
			iWonderRand *= 35;
			iWonderRand /= 100;
		}
		else if (iNumCitiesInArea >= 3)
		{
			iWonderRand *= 30;
			iWonderRand /= 100;
		}
		else
		{
			iWonderRand *= 25;
			iWonderRand /= 100;
		}

		if (bAggressiveAI)
		{
            // rfc: reduce impact
			//iWonderRand *= 2;
			//iWonderRand /= 3;
            iWonderRand *= 4;
            iWonderRand /= 5;
		}

		/* if (bLandWar && bTotalWar)
		{
			iWonderRand *= 2;
			iWonderRand /= 3;
		} */
		// K-Mod. When losing a war, it's not really an "opportune" time to build a wonder...
		if (bLandWar)
			iWonderRand = iWonderRand * 2/3;
		if (bTotalWar)
			iWonderRand = iWonderRand * 2/3;
		if (iWarSuccessRating < 0)
			iWonderRand = iWonderRand * 10/(10-iWarSuccessRating);
		// K-Mod end

		int iWonderRoll = SyncRandNum(100);

		if (iProductionRank == 1)
			iWonderRoll /= 2;

		if (iWonderRoll < iWonderRand)
		{
			int iWonderMaxTurns = 20 + ((iWonderRand - iWonderRoll) * 2);
			if (bLandWar)
				iWonderMaxTurns /= 2;
			if (AI_chooseBuilding(BUILDINGFOCUS_WORLDWONDER, iWonderMaxTurns))
			{
				if (gCityLogLevel >= 2) logBBAI("      City %S uses opportunistic wonder build 3", getName().GetCString());
				return;
			}
		}
	}

	if (iUnitSpending < iMaxUnitSpending + 12 && !bFinancialTrouble) // was +4 (new metric)
	{
		if (iAircraftHave * 2 >= iAircraftNeed && iAircraftHave < iAircraftNeed)
		{
			int iOdds = 33;
			if (iFreeAirExperience > 0 || iProductionRank <= 1 + kPlayer.getNumCities() / 2)
				iOdds = -1;
			if (AI_chooseLeastRepresentedUnit(airWeight, iOdds))
				return;
		}
	}

    // doc: only exclude major wars
	if (!(bLandWar && bMajorWar))
	{
		if (pWaterArea != NULL && bFinancialTrouble &&
			kPlayer.AI_totalAreaUnitAIs(kArea, UNITAI_MISSIONARY) > 0 &&
			kPlayer.AI_totalWaterAreaUnitAIs(*pWaterArea, UNITAI_MISSIONARY_SEA) <= 0)
		{
			if (AI_chooseUnit(UNITAI_MISSIONARY_SEA))
				return;
		}
	}


	if (AI_needsCultureToWorkFullRadius())
	{
		if (AI_chooseBuilding(BUILDINGFOCUS_CULTURE, 30))
			return;
	}

	if (!bAlwaysPeace)
	{
		if (!bDanger)
		{
			if (AI_chooseBuilding(BUILDINGFOCUS_EXPERIENCE, 20, 0, 3 * getPopulation()))
			{
				if (gCityLogLevel >= 2) logBBAI("      City %S uses special BUILDINGFOCUS_EXPERIENCE 3", getName().GetCString()); // advc
				return;
			}
		}

		if (AI_chooseBuilding(BUILDINGFOCUS_DEFENSE, 20, 0, bDanger ? -1 : 3 * getPopulation()))
		{
			if (gCityLogLevel >= 2) logBBAI("      City %S uses special BUILDINGFOCUS_DEFENSE", getName().GetCString()); // advc
			return;
		}
		if (bDanger)
		{
			if (AI_chooseBuilding(BUILDINGFOCUS_EXPERIENCE, 20, 0, 2 * getPopulation()))
			{
				if (gCityLogLevel >= 2) logBBAI("      City %S uses special BUILDINGFOCUS_EXPERIENCE 4", getName().GetCString()); // advc
				return;
			}
		}
	}

	// Short-circuit 3 - a last chance to catch important buildings
	{
		int iOdds = std::max(0, (bLandWar ? 160 : 220) * iBestBuildingValue / (iBestBuildingValue
				/* <advc.131> was +32 */ + 20 /* </advc.131> */) - 100);
		if (AI_chooseBuilding(0, MAX_INT, 0, iOdds))
		{
			if (gCityLogLevel >= 2) logBBAI("      City %S uses building value short-circuit 3 (odds: %d)", getName().GetCString(), iOdds);
   			return;
		}
	}

    // doc: only exclude major wars
	if (!(bLandWar && bMajorWar))
	{
		if (pWaterArea != NULL)
		{
			if (bPrimaryArea)
			{	// advc.124 (no functional change)
				if (iSeaExplorersNow < std::min(1, iSeaExplorersTarget))
				{
					if (AI_chooseUnit(UNITAI_EXPLORE_SEA))
						return;
				}
			}
		}
	}

	// advc.017: UNITAI_CITY_COUNTER block moved down
	// ...

	// we do a similar check lower, in the landwar case. (umm. no you don't. I'm changing this.)
	//if (!bLandWar && bFinancialTrouble)
	// <advc.110>
	//if(bFinancialTrouble)
	// Afforess - don't wait until we are in trouble, preventative medicine is best
	if (kPlayer.AI_financialTroubleMargin() < 10) // </advc.110>
	{
		if (AI_chooseBuilding(BUILDINGFOCUS_GOLD))
		{
			if (gCityLogLevel >= 2) logBBAI("      City %S uses choose financial trouble gold", getName().GetCString());
			return;
		}
	}

	bool bChooseUnit = false;
	if (iUnitSpending < iMaxUnitSpending + 15) // was +5 (new metric)
	{
		/*	advc: iBuildUnitProb gets used in a bunch of places.
			Shouldn't sneakily modify it here. */
		int iBuildUnitProbAdjusted = iBuildUnitProb;
		// K-Mod
		iBuildUnitProbAdjusted *= (250 + std::max(iProjectValue, iBestBuildingValue));
		iBuildUnitProbAdjusted /= (100 + 3 * std::max(iProjectValue, iBestBuildingValue));
		// K-Mod end
		if (bLandWar || (kPlayer.getNumCities() <= 3 && kGame.getElapsedGameTurns() < 60) ||
			(!bUnitExempt && SyncRandSuccess100(iBuildUnitProbAdjusted)) ||
			(isHuman() && getGameTurnFounded() == kGame.getGameTurn()))
		{
			if (AI_chooseUnit()) // advc.031b (note): Can train Settlers, but that rarely happens.
			{
				if (gCityLogLevel >= 2) logBBAI("      City %S uses choose unit by probability", getName().GetCString());
				return;
			}
			bChooseUnit = true;
		}
	}

	// Only cities with reasonable production
	/*if ((iProductionRank <= ((kPlayer.getNumCities() > 8) ? 3 : 2))
			&& (getPopulation() > 3)) {
		if (AI_chooseProject()) {
			if (gCityLogLevel >= 2) logBBAI("      City %S uses choose project 2", getName().GetCString());
			return;
		}
	}*/ // BtS
	// K-Mod
	FAssert((eBestProject == NO_PROJECT) == (iProjectValue <= 0));
	if (iProjectValue < 0)
		eBestProject = AI_bestProject(&iProjectValue);
	if (iProjectValue > iBestBuildingValue)
	{
		FAssert(eBestProject != NO_PROJECT);
		pushOrder(ORDER_CREATE, eBestProject);
		if (gCityLogLevel >= 2) logBBAI("      City %S uses choose project 2. (project value: %d, building value: %d)", getName().GetCString(), iProjectValue, iBestBuildingValue);
		return;
	}

	ProcessTypes eBestProcess = AI_bestProcess();
	if (eBestProcess != NO_PROCESS)
	{	// unfortunately, the evaluation of eBestProcess is duplicated.
		// Here we calculate roughly how many turns it would take for the building to pay itself back, where the cost it the value we could have had from building a process..
		// Note that as soon as we start working the process, our citizens will rearrange in a way that is likely to devalue the process for the next turn.
		int iOdds = 100;
		if (eBestBuilding != NO_BUILDING)
		{	// <advc.004x>
			int iConstructTurnsLeft = getProductionTurnsLeft(eBestBuilding, 0);
			if(iConstructTurnsLeft == MAX_INT)
				iOdds = 0;
			else // </advc.004x>
			{
				int iBuildingCost = AI_processValue(eBestProcess) * iConstructTurnsLeft;
				int iScaledTime = 10000 * iBuildingCost / (std::max(1, iBestBuildingValue) *
						GC.getInfo(kGame.getGameSpeedType()).getConstructPercent());
				iOdds = 100*(iScaledTime - 400)/(iScaledTime + 600); // <= 4 turns means 0%. 20 turns ~ 61%.
			}
		}
		if (SyncRandSuccess100(iOdds))
		{
			pushOrder(ORDER_MAINTAIN, eBestProcess);
			if (gCityLogLevel >= 2) logBBAI("      City %S uses choose process by value", getName().GetCString());
			return;
		}
	}
	// K-Mod end

	// advc.017: Moved here; used to come before the Process check
	if (!bUnitExempt && getPlot().plotCheck(PUF_isUnitAIType, UNITAI_CITY_COUNTER, -1, getOwner()) == NULL)
	{
		if (AI_chooseUnit(UNITAI_CITY_COUNTER))
		{
			return;
		}
	}

	if (AI_chooseBuilding())
	{
		if (gCityLogLevel >= 2) logBBAI("      City %S uses choose building by probability", getName().GetCString());
		return;
	}

	if (!bChooseUnit && !bFinancialTrouble && kPlayer.AI_isDoStrategy(AI_STRATEGY_FINAL_WAR))
	{
		if (AI_chooseUnit())
		{
			if (gCityLogLevel >= 2) logBBAI("      City %S uses choose unit by default", getName().GetCString());
			return;
		}
	}

	//if (AI_chooseProcess())
	if (eBestProcess != NO_PROCESS)
	{
		pushOrder(ORDER_MAINTAIN, eBestProcess);
		if (gCityLogLevel >= 2) logBBAI("      City %S uses choose process by default", getName().GetCString());
		return;
	}
}

UnitTypes CvCityAI::AI_bestUnit(bool bAsync, AdvisorTypes eIgnoreAdvisor, UnitAITypes* peBestUnitAI) /* advc: */ const
{
	if (peBestUnitAI != NULL)
		*peBestUnitAI = NO_UNITAI;

	CvPlayerAI const& kOwner = GET_PLAYER(getOwner()); // K-Mod

	// BETTER_BTS_AI_MOD, City AI, 11/30/08, jdog5000: bNoImpassable=true
	CvArea* pWaterArea = waterArea(true);

	bool const bWarPlan = GET_PLAYER(getOwner()).AI_isFocusWar(area()); // advc.105
			//(GET_TEAM(getTeam()).getAnyWarPlanCount(true) > 0);
	bool const bDefense = (getArea().getAreaAIType(getTeam()) == AREAAI_DEFENSIVE);
	//bLandWar = (bDefense || (getArea().getAreaAIType(getTeam()) == AREAAI_OFFENSIVE) || (getArea().getAreaAIType(getTeam()) == AREAAI_MASSING));
	bool const bLandWar = kOwner.AI_isLandWar(getArea()); // K-Mod
	bool const bAssault = (getArea().getAreaAIType(getTeam()) == AREAAI_ASSAULT);
	bool const bPrimaryArea = kOwner.AI_isPrimaryArea(getArea());
	bool const bAreaAlone = kOwner.AI_isAreaAlone(getArea());
	bool const bFinancialTrouble = kOwner.AI_isFinancialTrouble();
	bool const bWarPossible = GET_TEAM(getTeam()).AI_isWarPossible();
	bool const bDanger = AI_isDanger();

	int const iHasMetCount = GET_TEAM(getTeam()).getHasMetCivCount(true);
	int const iMilitaryWeight = kOwner.AI_militaryWeight(area());
	int const iNumCitiesInArea = getArea().getCitiesPerPlayer(getOwner());

	int iCoastalCities = 0;
	if (pWaterArea != NULL)
		iCoastalCities = kOwner.countNumCoastalCitiesByArea(*pWaterArea);

	int aiUnitAIVal[NUM_UNITAI_TYPES] = { 0 };

	int iDummy=-1;
	if (!bFinancialTrouble && (bPrimaryArea ?
		//kOwner.findBestFoundValue() > 0 : getArea().getBestFoundValue(getOwner()) > 0
		// <advc.opt>
		kOwner.AI_getNumCitySites() > 0 :
		kOwner.AI_getNumAreaCitySites(getArea(), iDummy) > 0)) // </advc.opt>
	{
		aiUnitAIVal[UNITAI_SETTLE]++;
	}
	aiUnitAIVal[UNITAI_WORKER] += kOwner.AI_neededWorkers(getArea());

	aiUnitAIVal[UNITAI_ATTACK] += iMilitaryWeight /
			(bWarPlan || bLandWar || bAssault ? 7 : 12) +
			(bPrimaryArea && bWarPossible ? 2 : 0) + 1;

	aiUnitAIVal[UNITAI_CITY_DEFENSE] += iNumCitiesInArea + 1;
	aiUnitAIVal[UNITAI_CITY_COUNTER] += (5 * (iNumCitiesInArea + 1)) / 8;
	aiUnitAIVal[UNITAI_CITY_SPECIAL] += (iNumCitiesInArea + 1) / 2;

	if (bWarPossible)
	{
		aiUnitAIVal[UNITAI_ATTACK_CITY] += iMilitaryWeight /
				(bWarPlan || bLandWar || bAssault ? 10 : 17) +
				(bPrimaryArea ? 1 : 0);
		aiUnitAIVal[UNITAI_COUNTER] += iMilitaryWeight /
				(bWarPlan || bLandWar || bAssault ? 13 : 22) +
				(bPrimaryArea ? 1 : 0);
		aiUnitAIVal[UNITAI_PARADROP] += iMilitaryWeight /
				(bWarPlan || bLandWar || bAssault ? 5 : 8) +
				(bPrimaryArea ? 1 : 0);

		//aiUnitAIVal[UNITAI_DEFENSE_AIR] += (kOwner.getNumCities() + 1);
		aiUnitAIVal[UNITAI_DEFENSE_AIR] += kOwner.AI_getTotalAirDefendersNeeded(); // K-Mod
		aiUnitAIVal[UNITAI_CARRIER_AIR] += kOwner.AI_countCargoSpace(
				UNITAI_CARRIER_SEA);
		aiUnitAIVal[UNITAI_MISSILE_AIR] += kOwner.AI_countCargoSpace(
				UNITAI_MISSILE_CARRIER_SEA);

		if (bPrimaryArea)
		{
			//aiUnitAIVal[UNITAI_ICBM] += std::max((kOwner.getTotalPopulation() / 25), ((GC.getGame().countCivPlayersAlive() + GC.getGame().countTotalNukeUnits()) / (GC.getGame().countCivPlayersAlive() + 1)));
			// K-Mod
			aiUnitAIVal[UNITAI_ICBM] += std::max(kOwner.getTotalPopulation() / 25,
					(GC.getGame().countFreeTeamsAlive() +
					GC.getGame().countTotalNukeUnits() +
					GC.getGame().getNukesExploded()) /
					(GC.getGame().countFreeTeamsAlive() + 1));
		}
	}

	if (isBarbarian())
		aiUnitAIVal[UNITAI_ATTACK] *= 2;
	else
	{
		if (!bLandWar)
			aiUnitAIVal[UNITAI_EXPLORE] += kOwner.AI_neededExplorers(getArea());

		if (pWaterArea != NULL)
		{
			aiUnitAIVal[UNITAI_WORKER_SEA] += AI_neededSeaWorkers();
			if (kOwner.getNumCities() > 3 || getArea().getNumUnownedTiles() < 10)
			{
				if (bPrimaryArea)
					aiUnitAIVal[UNITAI_EXPLORE_SEA] += kOwner.AI_neededExplorers(*pWaterArea);
				if (bPrimaryArea && kOwner.findBestFoundValue() > 0 &&
					pWaterArea->getNumTiles() > 300)
				{
					aiUnitAIVal[UNITAI_SETTLER_SEA]++;
				}
				if (bPrimaryArea &&
					kOwner.AI_totalAreaUnitAIs(getArea(), UNITAI_MISSIONARY) > 0 &&
					pWaterArea->getNumTiles() > 400)
				{
					aiUnitAIVal[UNITAI_MISSIONARY_SEA]++;
				}

				if (bPrimaryArea && kOwner.AI_totalAreaUnitAIs(getArea(), UNITAI_SPY) > 0 &&
					pWaterArea->getNumTiles() > 500)
				{
					aiUnitAIVal[UNITAI_SPY_SEA]++;
				}

				aiUnitAIVal[UNITAI_PIRATE_SEA] += pWaterArea->getNumTiles() / 600;

				if (bWarPossible)
				{
					// K-Mod note: this is bogus. TODO: change it so that it scales properly with map size.
					aiUnitAIVal[UNITAI_ATTACK_SEA] += std::min(
							pWaterArea->getNumTiles() / 150,
							(iCoastalCities * 2 + iMilitaryWeight / 9) / (bAssault ? 4 : 6) +
							(bPrimaryArea ? 1 : 0));
					aiUnitAIVal[UNITAI_RESERVE_SEA] += std::min(
							pWaterArea->getNumTiles() / 200,
							(iCoastalCities * 2 + iMilitaryWeight / 7) / 5 +
							(bPrimaryArea ? 1 : 0));
					aiUnitAIVal[UNITAI_ESCORT_SEA] += (kOwner.AI_totalWaterAreaUnitAIs(
							*pWaterArea, UNITAI_ASSAULT_SEA) +
							(kOwner.AI_totalWaterAreaUnitAIs(
							*pWaterArea, UNITAI_CARRIER_SEA) * 2));
					aiUnitAIVal[UNITAI_ASSAULT_SEA] += std::min(pWaterArea->getNumTiles() / 250,
							(iCoastalCities * 2 + iMilitaryWeight / 6) / (bAssault ? 5 : 8) +
							(bPrimaryArea ? 1 : 0));
					aiUnitAIVal[UNITAI_CARRIER_SEA] += std::min(
							pWaterArea->getNumTiles() / 350,
							(iCoastalCities * 2 + iMilitaryWeight / 8) / 7 +
							(bPrimaryArea ? 1 : 0));
					aiUnitAIVal[UNITAI_MISSILE_CARRIER_SEA] += std::min(
							pWaterArea->getNumTiles() / 350,
							(iCoastalCities * 2 + iMilitaryWeight / 8) / 7 +
							(bPrimaryArea ? 1 : 0));
				}
			}
		}

		if ((iHasMetCount > 0) && bWarPossible)
		{
			if (bLandWar || bAssault || !bFinancialTrouble ||
				kOwner.calculateUnitCost() == 0)
			{
				aiUnitAIVal[UNITAI_ATTACK] +=
						iMilitaryWeight / (bLandWar || bAssault ? 9 : 16) +
						(bPrimaryArea && !bAreaAlone ? 1 : 0);
				aiUnitAIVal[UNITAI_ATTACK_CITY] +=
						iMilitaryWeight / (bLandWar || bAssault ? 7 : 15) +
						(bPrimaryArea && !bAreaAlone ? 1 : 0);
				aiUnitAIVal[UNITAI_COLLATERAL] +=
						iMilitaryWeight / (bDefense ? 8 : 14) +
						(bPrimaryArea && !bAreaAlone ? 1 : 0);
				aiUnitAIVal[UNITAI_PILLAGE] +=
						iMilitaryWeight / (bLandWar ? 10 : 19) +
						(bPrimaryArea && !bAreaAlone ? 1 : 0);
				aiUnitAIVal[UNITAI_RESERVE] +=
						iMilitaryWeight / (bLandWar ? 12 : 17) +
						(bPrimaryArea && !bAreaAlone ? 1 : 0);
				aiUnitAIVal[UNITAI_COUNTER] +=
						iMilitaryWeight / (bLandWar || bAssault ? 9 : 16) +
						(bPrimaryArea && !bAreaAlone ? 1 : 0);
				aiUnitAIVal[UNITAI_PARADROP] +=
						iMilitaryWeight / (bLandWar || bAssault ? 4 : 8) +
						(bPrimaryArea && !bAreaAlone ? 1 : 0);

				//aiUnitAIVal[UNITAI_ATTACK_AIR] += (kOwner.getNumCities() + 1);
				// K-Mod (extra air attack and defence). Note: iMilitaryWeight is (pArea->getPopulationPerPlayer(getID()) + pArea->getCitiesPerPlayer(getID())
				aiUnitAIVal[UNITAI_ATTACK_AIR] += (bLandWar ? 2 : 1) *
						kOwner.getNumCities() + 1;
				// it would be nice if this was based on enemy air power...
				aiUnitAIVal[UNITAI_DEFENSE_AIR] += (bDefense ? 1 : 0) *
						kOwner.getNumCities() + 1;

				if (pWaterArea != NULL)
				{
					if (kOwner.getNumCities() > 3 || getArea().getNumUnownedTiles() < 10)
					{
						aiUnitAIVal[UNITAI_ATTACK_SEA] += std::min(
								pWaterArea->getNumTiles() / 100,
								(iCoastalCities * 2 + iMilitaryWeight / 10) / (bAssault ? 5 : 7) +
								(bPrimaryArea ? 1 : 0));
						aiUnitAIVal[UNITAI_RESERVE_SEA] += std::min(
								pWaterArea->getNumTiles() / 150,
								(iCoastalCities * 2 + iMilitaryWeight / 11) / 8 +
								(bPrimaryArea ? 1 : 0));
					}
				}
			}
			// K-Mod
			if (bLandWar && !bDefense && !isHuman() &&
				GET_TEAM(getTeam()).AI_getNumWarPlans(WARPLAN_TOTAL) > 0)
			{
				// if we're winning, then focus on capturing cities.
				int iSuccessRatio = GET_TEAM(getTeam()).AI_getWarSuccessRating();
				if (iSuccessRatio > 0)
				{
					aiUnitAIVal[UNITAI_ATTACK] += iSuccessRatio * iMilitaryWeight / 800;
					aiUnitAIVal[UNITAI_ATTACK_CITY] += iSuccessRatio * iMilitaryWeight / 1000;
					aiUnitAIVal[UNITAI_COUNTER] += iSuccessRatio * iMilitaryWeight / 1400;
					aiUnitAIVal[UNITAI_PARADROP] += iSuccessRatio * iMilitaryWeight / 1000;
				}
			} // K-Mod end
		}
	}

	// XXX this should account for air and heli units too...
	/*	K-Mod. Human players don't choose the AI type of the units they build.
		Therefore we shouldn't use the unit AI counts to decide what to build next. */
	if (isHuman())
	{
		aiUnitAIVal[UNITAI_SETTLE] = 0;
		aiUnitAIVal[UNITAI_WORKER] = 0;
		aiUnitAIVal[UNITAI_WORKER_SEA] = 0;
		aiUnitAIVal[UNITAI_EXPLORE] = 0;
		aiUnitAIVal[UNITAI_EXPLORE_SEA] = 0;
		aiUnitAIVal[UNITAI_ATTACK_CITY] /= 3;
		aiUnitAIVal[UNITAI_COLLATERAL] /= 2;
		aiUnitAIVal[UNITAI_PILLAGE] /= 3;
	}
	else // K-Mod end
	{
		FOR_EACH_ENUM(UnitAI)
		{
			if (kOwner.AI_unitAIDomainType(eLoopUnitAI) == DOMAIN_SEA)
			{
				if (pWaterArea != NULL)
				{
					aiUnitAIVal[eLoopUnitAI] -= kOwner.AI_totalWaterAreaUnitAIs(
							*pWaterArea, eLoopUnitAI);
				}
			}
			else if (kOwner.AI_unitAIDomainType(eLoopUnitAI) == DOMAIN_AIR ||
				eLoopUnitAI == UNITAI_ICBM)
			{
				aiUnitAIVal[eLoopUnitAI] -= kOwner.AI_totalUnitAIs(
						eLoopUnitAI);
			}
			else
			{
				aiUnitAIVal[eLoopUnitAI] -= kOwner.AI_totalAreaUnitAIs(
						getArea(), eLoopUnitAI);
			}
		}
	}

	aiUnitAIVal[UNITAI_SETTLE] *= (bDanger ? 8 : 12); // was ? 8 : 20
	aiUnitAIVal[UNITAI_WORKER] *= (bDanger ? 2 : 7);
	aiUnitAIVal[UNITAI_ATTACK] *= 3;
	aiUnitAIVal[UNITAI_ATTACK_CITY] *= 5; // K-Mod, up from *4
	aiUnitAIVal[UNITAI_COLLATERAL] *= 5;
	aiUnitAIVal[UNITAI_PILLAGE] *= 3;
	aiUnitAIVal[UNITAI_RESERVE] *= 3;
	/*aiUnitAIVal[UNITAI_COUNTER] *= 3;
	aiUnitAIVal[UNITAI_COUNTER] *= 2;*/
	/*  advc.131: The double weights look unintentional, but apparently,
		they somewhat work. Let's use 4 as a compromise. */
	aiUnitAIVal[UNITAI_COUNTER] *= 4;
	aiUnitAIVal[UNITAI_CITY_DEFENSE] *= 2;
	aiUnitAIVal[UNITAI_CITY_COUNTER] *= 2;
	aiUnitAIVal[UNITAI_CITY_SPECIAL] *= 2;
	aiUnitAIVal[UNITAI_EXPLORE] *= (bDanger ? 6 : 15);
	//aiUnitAIVal[UNITAI_ICBM] *= 18;
	aiUnitAIVal[UNITAI_ICBM] *= 18 * kOwner.AI_nukeWeight() / 100; // K-Mod
	aiUnitAIVal[UNITAI_WORKER_SEA] *= (bDanger ? 3 : 10);
	aiUnitAIVal[UNITAI_ATTACK_SEA] *= 5;
	aiUnitAIVal[UNITAI_RESERVE_SEA] *= 4;
	aiUnitAIVal[UNITAI_ESCORT_SEA] *= 20;
	aiUnitAIVal[UNITAI_EXPLORE_SEA] *= 18;
	aiUnitAIVal[UNITAI_ASSAULT_SEA] *= 14;
	aiUnitAIVal[UNITAI_SETTLER_SEA] *= 16;
	aiUnitAIVal[UNITAI_MISSIONARY_SEA] *= 12;
	aiUnitAIVal[UNITAI_SPY_SEA] *= 10;
	aiUnitAIVal[UNITAI_CARRIER_SEA] *= 8;
	aiUnitAIVal[UNITAI_MISSILE_CARRIER_SEA] *= 8;
	aiUnitAIVal[UNITAI_PIRATE_SEA] *= 5;
	aiUnitAIVal[UNITAI_ATTACK_AIR] *= 6;
	aiUnitAIVal[UNITAI_DEFENSE_AIR] *= 4; // K-Mod, up from *3
	aiUnitAIVal[UNITAI_CARRIER_AIR] *= 15;
	aiUnitAIVal[UNITAI_MISSILE_AIR] *= 15;

    // rfc: civilization based unit AI value
	switch (getCivilizationType())
	{
	case EGYPT:
		aiUnitAIVal[UNITAI_EXPLORE] /= 2;
		aiUnitAIVal[UNITAI_EXPLORE_SEA] /= 3;
		if (GET_TEAM((TeamTypes)getOwnerINLINE()).isHasTech((TechTypes)FEUDALISM))
			aiUnitAIVal[UNITAI_SETTLE] /= 3;
		break;
	case BABYLONIA:
		aiUnitAIVal[UNITAI_EXPLORE] /= 2;
		aiUnitAIVal[UNITAI_EXPLORE_SEA] /= 3;
		aiUnitAIVal[UNITAI_ATTACK] *= 2;
        aiUnitAIVal[UNITAI_SETTLE] /= 50;
		break;
	case HARAPPA:
		aiUnitAIVal[UNITAI_SETTLE] *= 3;
		aiUnitAIVal[UNITAI_WORKER] *= 2;
		aiUnitAIVal[UNITAI_CITY_DEFENSE] /= 2;
		break;
	case ASSYRIA:
		aiUnitAIVal[UNITAI_CITY_DEFENSE] /= 2;
		aiUnitAIVal[UNITAI_ATTACK_CITY] *= 3;
		aiUnitAIVal[UNITAI_SETTLE] /= 50;
		break;
	case NUBIA:
		aiUnitAIVal[UNITAI_CITY_DEFENSE] *= 3;
		aiUnitAIVal[UNITAI_CITY_COUNTER] *= 2;
		break;
	case GREECE:
		aiUnitAIVal[UNITAI_SETTLE] *= 2;
		aiUnitAIVal[UNITAI_EXPLORE] *= 2;
		aiUnitAIVal[UNITAI_EXPLORE_SEA] *= 3;
		aiUnitAIVal[UNITAI_EXPLORE_SEA] /= 2;
		break;
	case CHINA:
		aiUnitAIVal[UNITAI_EXPLORE] /= 4;
		aiUnitAIVal[UNITAI_EXPLORE_SEA] /= 5;
		aiUnitAIVal[UNITAI_COUNTER] /= 2;
		aiUnitAIVal[UNITAI_ATTACK] *= 3;
		aiUnitAIVal[UNITAI_SETTLE] *= 3;
		aiUnitAIVal[UNITAI_SETTLE] /= 2;
		aiUnitAIVal[UNITAI_WORKER] *= 2;
		aiUnitAIVal[UNITAI_MISSIONARY] /= 5;
		break;
	case INDIA:
		aiUnitAIVal[UNITAI_EXPLORE] /= 2;
		aiUnitAIVal[UNITAI_EXPLORE_SEA] /= 3;
		aiUnitAIVal[UNITAI_ICBM] *= 2;
		//aiUnitAIVal[UNITAI_SETTLE] /= 50;
		break;
	case CARTHAGE:
		aiUnitAIVal[UNITAI_EXPLORE] *= 2;
		aiUnitAIVal[UNITAI_EXPLORE_SEA] *= 3;
		aiUnitAIVal[UNITAI_SETTLER_SEA] *= 3;
		if (!GET_TEAM((TeamTypes)getOwnerINLINE()).isHasTech((TechTypes)OPTICS))
				aiUnitAIVal[UNITAI_SETTLE] *= 2;
		break;
	case POLYNESIA:
		aiUnitAIVal[UNITAI_SETTLER_SEA] *= 3;
		aiUnitAIVal[UNITAI_EXPLORE_SEA] *= 2;
		break;
	case PERSIA:
		aiUnitAIVal[UNITAI_ATTACK] *= 2;
		break;
	case CELTS:
		aiUnitAIVal[UNITAI_SETTLE] *= 2;
		aiUnitAIVal[UNITAI_ATTACK] *= 2;
		aiUnitAIVal[UNITAI_PILLAGE] *= 3;
		break;
	case ROME:      // leave unit AI unchanged so far
        aiUnitAIVal[UNITAI_ASSAULT_SEA] *= 2;
        //aiUnitAIVal[UNITAI_COUNTER] *= 2;
		aiUnitAIVal[UNITAI_ATTACK_CITY] *= 2;
		aiUnitAIVal[UNITAI_COLLATERAL] *= 2;
		break;
		/*aiUnitAIVal[UNITAI_EXPLORE] /= 2;
		aiUnitAIVal[UNITAI_EXPLORE_SEA] /= 2;
		aiUnitAIVal[UNITAI_SETTLE] *= 2;
		aiUnitAIVal[UNITAI_SETTLE] /= 3;
		break;*/
	case DRAVIDIA:
		aiUnitAIVal[UNITAI_ASSAULT_SEA] *= 3;
		aiUnitAIVal[UNITAI_SETTLER_SEA] *= 3;
		break;
	case TOLTECS:
		aiUnitAIVal[UNITAI_WORKER] *= 2;
		break;
	case KUSHANS:
		aiUnitAIVal[UNITAI_MISSIONARY] *= 2;
		break;
	case ETHIOPIA:
		break;
    case KOREA:
        aiUnitAIVal[UNITAI_EXPLORE] /= 2;
        aiUnitAIVal[UNITAI_EXPLORE_SEA] /= 3;
        aiUnitAIVal[UNITAI_SETTLE] /= 2;
        aiUnitAIVal[UNITAI_ASSAULT_SEA] *= 2;
        break;
	case MAYA:
		aiUnitAIVal[UNITAI_EXPLORE] /= 2;
		break;
    case BYZANTIUM:
		aiUnitAIVal[UNITAI_ASSAULT_SEA] *= 2;
		aiUnitAIVal[UNITAI_EXPLORE] *= 2;
		aiUnitAIVal[UNITAI_WORKER] *= 2;
		aiUnitAIVal[UNITAI_ATTACK_CITY] /= 2;
		aiUnitAIVal[UNITAI_COUNTER] *= 2;
        aiUnitAIVal[UNITAI_SETTLE] /= 3;
		break;
	case MALAYS:
		aiUnitAIVal[UNITAI_SETTLER_SEA] *= 3;
		aiUnitAIVal[UNITAI_ESCORT_SEA] *= 2;
		aiUnitAIVal[UNITAI_EXPLORE_SEA] /= 5;
		break;
	case JAPAN:
		if (!GET_TEAM((TeamTypes)getOwnerINLINE()).isHasTech((TechTypes)MACHINE_TOOLS))
				aiUnitAIVal[UNITAI_ATTACK_SEA] /= 3;
		else
				aiUnitAIVal[UNITAI_ATTACK_SEA] *= 3;
		aiUnitAIVal[UNITAI_ASSAULT_SEA] *= 2;
		aiUnitAIVal[UNITAI_EXPLORE] /= 4;
		aiUnitAIVal[UNITAI_EXPLORE_SEA] /= 4;
		aiUnitAIVal[UNITAI_SETTLER_SEA] /= 2;
		aiUnitAIVal[UNITAI_SETTLE] *= 2;
		aiUnitAIVal[UNITAI_SETTLE] /= 3;
		break;
	case NORSE:
		aiUnitAIVal[UNITAI_EXPLORE_SEA] *= 3;
		aiUnitAIVal[UNITAI_SETTLER_SEA] *= 2;
		aiUnitAIVal[UNITAI_ATTACK_SEA] *= 3;
		aiUnitAIVal[UNITAI_ASSAULT_SEA] *= 3;
		aiUnitAIVal[UNITAI_SETTLE] *= 2;
		aiUnitAIVal[UNITAI_SETTLE] /= 2;
		aiUnitAIVal[UNITAI_ATTACK_CITY] *= 2;
		aiUnitAIVal[UNITAI_COUNTER] *= 2;
		break;
	case TURKS:
		aiUnitAIVal[UNITAI_ATTACK] *= 2;
		aiUnitAIVal[UNITAI_ATTACK_CITY] *= 3;
		break;
	case ARABIA:
		aiUnitAIVal[UNITAI_ATTACK] *= 2;
		aiUnitAIVal[UNITAI_CITY_DEFENSE] *= 3;
		aiUnitAIVal[UNITAI_CITY_DEFENSE] /= 2;
		aiUnitAIVal[UNITAI_MISSIONARY] *= 2;
		aiUnitAIVal[UNITAI_ICBM] *= 2;
		break;
	case TIBET:
		aiUnitAIVal[UNITAI_MISSIONARY] *= 5;
		break;
	case JAVA:
		aiUnitAIVal[UNITAI_ASSAULT_SEA] *= 3;
		aiUnitAIVal[UNITAI_ATTACK_SEA] *= 2;
		aiUnitAIVal[UNITAI_SETTLER_SEA] *= 3;
		aiUnitAIVal[UNITAI_EXPLORE_SEA] /= 5;
		break;
	case MOORS:
		aiUnitAIVal[UNITAI_EXPLORE_SEA] /= 2;
		//aiUnitAIVal[UNITAI_ASSAULT_SEA] *= 2;
		//aiUnitAIVal[UNITAI_SETTLER_SEA] *= 2;
		aiUnitAIVal[UNITAI_PIRATE_SEA] *= 2;
		aiUnitAIVal[UNITAI_CITY_DEFENSE] /= 2;
		break;
	case SPAIN:
		aiUnitAIVal[UNITAI_EXPLORE_SEA] *= 5;
		aiUnitAIVal[UNITAI_SETTLER_SEA] *= 3;
		aiUnitAIVal[UNITAI_ESCORT_SEA] *= 2;
		if (GET_TEAM(getTeam()).isHasTech((TechTypes)EXPLORATION))
			aiUnitAIVal[UNITAI_SETTLE] *= 3;
		aiUnitAIVal[UNITAI_MISSIONARY_SEA] *= 2;
		aiUnitAIVal[UNITAI_MISSIONARY] *= 2;
		break;
	case FRANCE:
		aiUnitAIVal[UNITAI_COUNTER] *= 2;
		aiUnitAIVal[UNITAI_EXPLORE_SEA] *= 2;
		aiUnitAIVal[UNITAI_SETTLER_SEA] *= 2;
		aiUnitAIVal[UNITAI_ESCORT_SEA] *= 2;
		if (GET_TEAM(getTeam()).isHasTech((TechTypes)EXPLORATION))
			aiUnitAIVal[UNITAI_SETTLE] *= 2;
		break;
	case KHMER:
		aiUnitAIVal[UNITAI_EXPLORE_SEA] *= 2;
		//aiUnitAIVal[UNITAI_SETTLER_SEA] *= 2;
		break;
	case ENGLAND:
		aiUnitAIVal[UNITAI_EXPLORE_SEA] *= 5;
		aiUnitAIVal[UNITAI_EXPLORE_SEA] /= 2;
		aiUnitAIVal[UNITAI_SETTLER_SEA] *= 2;
		aiUnitAIVal[UNITAI_ESCORT_SEA] *= 2;
		if (GET_TEAM(getTeam()).isHasTech((TechTypes)EXPLORATION))
			aiUnitAIVal[UNITAI_SETTLE] *= 2;
		aiUnitAIVal[UNITAI_DEFENSE_AIR] *= 2;
		aiUnitAIVal[UNITAI_RESERVE_SEA] *= 2;
		aiUnitAIVal[UNITAI_WORKER_SEA] *= 3;
		aiUnitAIVal[UNITAI_WORKER_SEA] /= 2;
		aiUnitAIVal[UNITAI_ASSAULT_SEA] *= 3;
		aiUnitAIVal[UNITAI_ASSAULT_SEA] /= 2;
		aiUnitAIVal[UNITAI_DEFENSE_AIR] *= 3;
		aiUnitAIVal[UNITAI_DEFENSE_AIR] /= 2;
		break;
	case HOLY_ROME:
		aiUnitAIVal[UNITAI_COUNTER] *= 2;
		aiUnitAIVal[UNITAI_ATTACK_CITY] /= 2;
		aiUnitAIVal[UNITAI_CITY_DEFENSE] *= 2;
		break;
	case BURMA:
		aiUnitAIVal[UNITAI_ATTACK] *= 3;
		aiUnitAIVal[UNITAI_EXPLORE_SEA] /= 5;
		aiUnitAIVal[UNITAI_ASSAULT_SEA] /= 3;
		aiUnitAIVal[UNITAI_ATTACK_SEA] /= 3;
		aiUnitAIVal[UNITAI_ESCORT_SEA] /= 3;
		break;
	case RUSSIA:
		aiUnitAIVal[UNITAI_EXPLORE] *= 3;
		aiUnitAIVal[UNITAI_EXPLORE] /= 2;
		aiUnitAIVal[UNITAI_EXPLORE_SEA] /= 2;
		aiUnitAIVal[UNITAI_SETTLER_SEA] /= 2;
		aiUnitAIVal[UNITAI_SETTLE] *= 2;
		aiUnitAIVal[UNITAI_RESERVE] *= 2;
		aiUnitAIVal[UNITAI_ICBM] *= 2;
		break;
	case RUS:
		aiUnitAIVal[UNITAI_EXPLORE] *= 2;
		aiUnitAIVal[UNITAI_ATTACK_CITY] /= 2;
		break;
	case VIETNAM:
		aiUnitAIVal[UNITAI_CITY_DEFENSE] *= 2;
		aiUnitAIVal[UNITAI_CITY_COUNTER] *= 3;
		aiUnitAIVal[UNITAI_COUNTER] *= 3;
		break;
	case SWAHILI:
		aiUnitAIVal[UNITAI_ESCORT_SEA] *= 2;
		aiUnitAIVal[UNITAI_EXPLORE_SEA] *= 3;
		aiUnitAIVal[UNITAI_SETTLER_SEA] *= 2;
		break;
	case MALI:
		break;
	case POLAND:
		aiUnitAIVal[UNITAI_ASSAULT_SEA] /= 3;
		aiUnitAIVal[UNITAI_EXPLORE_SEA] /= 3;
		aiUnitAIVal[UNITAI_SETTLER_SEA] /= 3;
		break;
	case MUGHALS:
		aiUnitAIVal[UNITAI_ASSAULT_SEA] /= 2;
		aiUnitAIVal[UNITAI_EXPLORE_SEA] /= 2;
		aiUnitAIVal[UNITAI_ATTACK_CITY] *= 2;
		aiUnitAIVal[UNITAI_ASSAULT_SEA] /= 3;
		aiUnitAIVal[UNITAI_EXPLORE_SEA] /= 3;
		break;
	case OTTOMANS:
		aiUnitAIVal[UNITAI_ATTACK_CITY] *= 2;
		aiUnitAIVal[UNITAI_ATTACK] *= 2;
		aiUnitAIVal[UNITAI_COUNTER] *= 3;
		aiUnitAIVal[UNITAI_COUNTER] /= 2;
		break;
	case PORTUGAL:
		aiUnitAIVal[UNITAI_EXPLORE_SEA] *= 5;
		aiUnitAIVal[UNITAI_SETTLER_SEA] *= 3;
		aiUnitAIVal[UNITAI_ESCORT_SEA] *= 2;
		if (GET_TEAM(getTeam()).isHasTech((TechTypes)CARTOGRAPHY))
		{
			aiUnitAIVal[UNITAI_SETTLE] *= 2;
		}
		aiUnitAIVal[UNITAI_RESERVE_SEA] *= 2;
		aiUnitAIVal[UNITAI_WORKER_SEA] *= 3;
		aiUnitAIVal[UNITAI_WORKER_SEA] /= 2;
		break;
	case INCA:
		aiUnitAIVal[UNITAI_EXPLORE] *= 2;
		aiUnitAIVal[UNITAI_EXPLORE_SEA] /= 4;
		aiUnitAIVal[UNITAI_ATTACK_SEA] /= 4;
		aiUnitAIVal[UNITAI_ESCORT_SEA] /= 4;
		aiUnitAIVal[UNITAI_SETTLER_SEA] /= 4;
		aiUnitAIVal[UNITAI_RESERVE_SEA] /= 4;
		break;
	case ITALY:
        aiUnitAIVal[UNITAI_SETTLE] *= 2;
        //aiUnitAIVal[UNITAI_ASSAULT_SEA] *= 2;
        aiUnitAIVal[UNITAI_EXPLORE] *= 2;
        aiUnitAIVal[UNITAI_WORKER] *= 2;
        aiUnitAIVal[UNITAI_ATTACK_CITY] *= 3;
        aiUnitAIVal[UNITAI_ATTACK_CITY] /= 2;
		break;
	case MONGOLS:
		aiUnitAIVal[UNITAI_ATTACK] *= 2;
		break;
	case AZTECS:
		aiUnitAIVal[UNITAI_EXPLORE] /= 2;
		aiUnitAIVal[UNITAI_EXPLORE_SEA] /= 2;
		aiUnitAIVal[UNITAI_SETTLE] *= 2;
		aiUnitAIVal[UNITAI_SETTLE] /= 3;
		break;
	case THAILAND:
		aiUnitAIVal[UNITAI_COUNTER] *= 2;
		break;
	case SWEDEN:
		if (GET_PLAYER(getOwnerINLINE()).getCurrentEra() == ERA_RENAISSANCE)
		{
			aiUnitAIVal[UNITAI_ATTACK] *= 2;
		}
		break;
	case CONGO:
		aiUnitAIVal[UNITAI_EXPLORE_SEA] /= 4;
		break;
	case NETHERLANDS:
		aiUnitAIVal[UNITAI_EXPLORE_SEA] *= 5;
		aiUnitAIVal[UNITAI_EXPLORE_SEA] /= 2;
		aiUnitAIVal[UNITAI_SETTLER_SEA] *= 3;
		aiUnitAIVal[UNITAI_ESCORT_SEA] *= 2;
		if (GET_TEAM(getTeam()).isHasTech((TechTypes)EXPLORATION))
			aiUnitAIVal[UNITAI_SETTLE] *= 2;
		aiUnitAIVal[UNITAI_RESERVE_SEA] *= 2;
		aiUnitAIVal[UNITAI_WORKER_SEA] *= 3;
		aiUnitAIVal[UNITAI_WORKER_SEA] /= 2;
		aiUnitAIVal[UNITAI_ASSAULT_SEA] *= 3;
		aiUnitAIVal[UNITAI_ASSAULT_SEA] /= 2;
		break;
	case GERMANY:
		aiUnitAIVal[UNITAI_ATTACK_CITY] *= 2;
		aiUnitAIVal[UNITAI_ATTACK_AIR] *= 2;
		aiUnitAIVal[UNITAI_DEFENSE_AIR] *= 2;
		aiUnitAIVal[UNITAI_RESERVE_SEA] *= 2;
		aiUnitAIVal[UNITAI_ICBM] *= 2;
		break;
	case AMERICA:
		aiUnitAIVal[UNITAI_SETTLE] *= 5;
		aiUnitAIVal[UNITAI_RESERVE] *= 2;
		aiUnitAIVal[UNITAI_ASSAULT_SEA] *= 2;
		aiUnitAIVal[UNITAI_ICBM] *= 2;
		aiUnitAIVal[UNITAI_CARRIER_AIR] *= 2;
		aiUnitAIVal[UNITAI_ATTACK_AIR] *= 2;
		aiUnitAIVal[UNITAI_DEFENSE_AIR] *= 2;
		break;
	case ARGENTINA:
		aiUnitAIVal[UNITAI_ATTACK_CITY] *= 2;
		break;
	case BRAZIL:
		aiUnitAIVal[UNITAI_WORKER] *= 2;
		aiUnitAIVal[UNITAI_CITY_DEFENSE] *= 3;
		aiUnitAIVal[UNITAI_CITY_DEFENSE] /= 2;
		break;
	case NATIVE:
		aiUnitAIVal[UNITAI_CITY_DEFENSE] /= 5;
		aiUnitAIVal[UNITAI_CITY_COUNTER] /= 2;
		aiUnitAIVal[UNITAI_PILLAGE] *= 2;
		break;
	default:
		break;
	}

	if (GET_PLAYER(getOwnerINLINE()).AI_getNumAIUnits(UNITAI_EXPLORE_SEA) == 0)
	{
		switch (getCivilizationType())
		{
		case FRANCE:
		case SPAIN:
		case ENGLAND:
		case PORTUGAL:
		case NETHERLANDS:
			aiUnitAIVal[UNITAI_EXPLORE_SEA] *= 10;
			break;
		default:
			break;
		}
	}

	// K-Mod
	if (GET_PLAYER(getOwner()).AI_isDoStrategy(AI_STRATEGY_CRUSH))
	{
		aiUnitAIVal[UNITAI_ATTACK_CITY] *= 2;
		aiUnitAIVal[UNITAI_ATTACK] *= 2;
		aiUnitAIVal[UNITAI_ATTACK_AIR] *= 3;
	}
	if (GET_TEAM(getTeam()).AI_getRivalAirPower() <=
		8 * GET_PLAYER(getOwner()).AI_totalAreaUnitAIs(getArea(), UNITAI_DEFENSE_AIR))
	{
		/*	unfortunately, I don't have an easy way to get the approximate power
			of our air defence units. So I'm just going to assume the power of
			each unit is around 12 - the power of a fighter plane. */
		aiUnitAIVal[UNITAI_DEFENSE_AIR] /= 4;
	}
	// K-Mod end
	FOR_EACH_ENUM(UnitAI)
	{
		// advc.131: AIWeight would have the opposite effect on negative AIVal
		if (aiUnitAIVal[eLoopUnitAI] > 0)
		{
			aiUnitAIVal[eLoopUnitAI] *= std::max(0, 100 +
					GC.getInfo(getPersonalityType()).getUnitAIWeightModifier(eLoopUnitAI));
			aiUnitAIVal[eLoopUnitAI] /= 100;
		}
	} // <advc.033>
	if (GET_TEAM(getOwner()).isCapitulated())
	{
		aiUnitAIVal[UNITAI_PIRATE_SEA] = 0;
		aiUnitAIVal[UNITAI_ICBM] = 0; // advc.143b
	} // </advc.033>
	int iBestValue = 0;
	UnitTypes eBestUnit = NO_UNIT;

	FOR_EACH_ENUM(UnitAI)
	{
		if (aiUnitAIVal[eLoopUnitAI] <= 0)
			continue;
		if (bAsync)
		{
			aiUnitAIVal[eLoopUnitAI] += GC.getASyncRand().get(
					iMilitaryWeight, "AI Best UnitAI ASYNC");
		}
		else aiUnitAIVal[eLoopUnitAI] += SyncRandNum(iMilitaryWeight);
		if (aiUnitAIVal[eLoopUnitAI] > iBestValue)
		{
			UnitTypes eUnit = AI_bestUnitAI(eLoopUnitAI, bAsync, eIgnoreAdvisor);
			if (eUnit != NO_UNIT)
			{
				iBestValue = aiUnitAIVal[eLoopUnitAI];
				eBestUnit = eUnit;
				if (peBestUnitAI != NULL)
					*peBestUnitAI = eLoopUnitAI;
			}
		}
	}
	return eBestUnit;
}

// Choose the best unit to build for the given AI type.
// Note: a lot of this function has been restructured / rewritten for K-Mod
UnitTypes CvCityAI::AI_bestUnitAI(UnitAITypes eUnitAI, bool bAsync, AdvisorTypes eIgnoreAdvisor) /* advc: */ const
{
	PROFILE_FUNC();
	FAssertMsg(eUnitAI != NO_UNITAI, "UnitAI is not assigned a valid value");

	bool bGrowMore = false;
	int const iFoodDiff = /* K-Mod: */ foodDifference(true, true);
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());
	if (iFoodDiff > 0)
	{
		bool bAssumeImprovements = (AI_getWorkersHave() > 0 || isHuman()); // advc.113
		// BBAI NOTE: This is where small city worker and settler production is blocked
		if (kOwner.getNumCities() <= 2)
		{
			//bGrowMore = ((getPopulation() < 3) && (AI_countGoodTiles(true, false, 100) >= getPopulation()));
			// K-Mod. We need to allow the starting city to build a worker at size 1.
			bGrowMore = ((eUnitAI != UNITAI_WORKER ||
					kOwner.AI_totalAreaUnitAIs(getArea(), UNITAI_WORKER) > 0) && // K-Mod end
					getPopulation() < 3 && AI_countGoodTiles(true, false, 100,
					//false) >= getPopulation()
					/*  advc.113: Assume improvements and req. a good tile for the
						extra citizen as well ('>' instead of '>=') */
					bAssumeImprovements) > getPopulation());
			// <advc.052> Train Settler at size 2 if growth is slow in capital
			if(bGrowMore && getPopulation() == 2 &&
				kOwner.getNumCities() == 1 && eUnitAI == UNITAI_SETTLE &&
				getFoodTurnsLeft() * 100 >=
				6 * GC.getInfo(GC.getGame().getGameSpeedType()).getTrainPercent() &&
				/*  This is more often true than I'd like b/c of improvements
					under construction. Could check Worker count and
					improvement count ... */
				iFoodDiff <= 2 &&
				// No point in an early settler if we can't escort it yet
				(kOwner.getNumCities() > 1 ||
				getPlot().plotCount(PUF_isMissionAIType, MISSIONAI_GUARD_CITY, -1, getOwner()) >=
				AI_neededDefenders()))
			{
				bGrowMore = false;
			} // </advc.052>
		}
		else
		{	// advc.113: Require a value-50 tile for bGrowMore even if the city is size 1 or 2
			bGrowMore = (AI_countGoodTiles(true, false, 50, bAssumeImprovements) > getPopulation() &&
					((getPopulation() < 3 /* advc.052: */ && iFoodDiff > 1) ||
					// advc.113: Was '>='. (Don't assume improvements here; be pessimistic.)
					AI_countGoodTiles(true, false, 100) > getPopulation()));
		}

		if (!bGrowMore && getPopulation() < 6 &&
			// advc.113: Was '>='. And assume improvements.
			AI_countGoodTiles(true, false, 80, bAssumeImprovements) > getPopulation())
		{
			if (getFood() - getFoodKept() / 2 >= growthThreshold() / 2 &&
				//angryPopulation(1) == 0 && healthRate(false, 1) == 0)
				// advc.113: Handle anger below
				healthRate(false, 1) <= 0)
			{
				bGrowMore = true;
			}
		}
		/*else if (bGrowMore) {
			if (angryPopulation(1) > 0)
				bGrowMore = false;
		}*/ // advc.113: Replacing the K-Mod code above ('else' removed)
		bGrowMore = (bGrowMore && angryPopulation(1) <= 0);
	}


	std::vector<std::pair<int, UnitTypes> > candidates;
	int iBestBaseValue = 0;

	CvCivilization const& kCiv = getCivilization(); // advc.003w
	for (int i = 0; i < kCiv.getNumUnits(); i++)
	{
		UnitTypes eUnit = kCiv.unitAt(i);
		CvUnitInfo const& kUnit = GC.getInfo(eUnit);
		if (eIgnoreAdvisor != NO_ADVISOR && kUnit.getAdvisorType() == eIgnoreAdvisor)
			continue;

		if (bGrowMore && isFoodProduction(eUnit))
			continue;

		if (!canTrain(eUnit))
			continue;
		// <advc.041> Mostly cut and pasted from CvPlot::canTrain
		int iMinAreaSz = kUnit.getMinAreaSize();
		if (iMinAreaSz > 0)
		{
			CvPlot const& p = getPlot();
			if ((kUnit.getDomainType() == DOMAIN_SEA &&
				!p.isCoastalLand(iMinAreaSz)) ||
				(kUnit.getDomainType() != DOMAIN_SEA &&
				p.getArea().getNumTiles() < iMinAreaSz))
			{
				continue;
			}
		} // </advc.041>
		int iValue = kOwner.AI_unitValue(eUnit, eUnitAI, area());
		if (iValue > 0)
		{
			candidates.push_back(std::make_pair(iValue, eUnit));
			if (iValue > iBestBaseValue)
				iBestBaseValue = iValue;
		}
	}

	int iBestValue = 0;
	UnitTypes eBestUnit = NO_UNIT;

	for (size_t i = 0; i < candidates.size(); i++)
	{
		UnitTypes const eUnit = candidates[i].second;

		int iValue = candidates[i].first;
		if (iValue < iBestBaseValue*2/3 || (eUnitAI == UNITAI_EXPLORE && iValue < iBestBaseValue))
			continue;

		CvUnitInfo const& kUnit = GC.getInfo(eUnit);

		iValue *= (getProductionExperience(eUnit) + 10);
		iValue /= 10;

		// Take into account free promotions, and available promotions that suit the AI type.
		// Note: it might be better if this was in AI_unitValue rather than here, but the
		// advantage of doing it here is that we can check city promotions at the same time.
		int iPromotionValue = 0;
		bool bHasGoodPromotion = false; // check that appropriate non-free promotions are available
		FOR_EACH_ENUM2(Promotion, ePromo)
		{
			bool bFree = kUnit.getFreePromotions(ePromo);
			CvPromotionInfo const& kPromo = GC.getInfo(ePromo);

			if (!bFree && isFreePromotion(ePromo))
			{
				if (kUnit.getUnitCombatType() != NO_UNITCOMBAT &&
					kPromo.getUnitCombat(kUnit.getUnitCombatType()))
				{
					bFree = true;
				}
			}

			if (!bFree)
			{
				UnitCombatTypes eCombat = kUnit.getUnitCombatType();
				if (eCombat != NO_UNITCOMBAT) // advc: Moved up
				{
					FOR_EACH_ENUM(Trait)
					{
						if (hasTrait(eLoopTrait) && GC.getInfo(eLoopTrait).isFreePromotion(ePromo))
						{
							if (GC.getInfo(eLoopTrait).isFreePromotionUnitCombat(eCombat))
								bFree = true;
						}
					}
				}
			}

			// For simplicity, I'll assume that each promotion only gives one type of bonus.
			// (eg. if the promotion gives + city defence, assume that it's a defensive promotion)
			// This may not be true in general, but I think it's a good enough approximation.
			if (!bHasGoodPromotion)
			{
				if (eUnitAI == UNITAI_ATTACK_CITY)
				{
					if (kPromo.getCityAttackPercent() > 0)
					{
						if (bFree || kUnit.isPromotionValid(ePromo, false))
						{
							bHasGoodPromotion = true;
							iPromotionValue += 15;
						}
					}
				}
				else if (eUnitAI == UNITAI_CITY_DEFENSE)
				{
					if (kPromo.getCityDefensePercent() > 0)
					{
						if (bFree || kUnit.isPromotionValid(ePromo, false))
						{
							bHasGoodPromotion = true;
							iPromotionValue += 12;
						}
					}
				}
			}

			if (bFree)
			{
				// Note: in the original bts code, all free promotions were worth 15 points.
				if (kPromo.getCityAttackPercent() > 0)
				{
					if (eUnitAI == UNITAI_CITY_DEFENSE)
						iPromotionValue += 4;
					else if (eUnitAI == UNITAI_ATTACK || eUnitAI == UNITAI_ATTACK_CITY)
						iPromotionValue += 20;
					else iPromotionValue += 8;
				}
				else if (kPromo.isAmphib())
				{
					if (eUnitAI == UNITAI_CITY_DEFENSE)
						iPromotionValue += 4;
					else if (eUnitAI == UNITAI_ATTACK || eUnitAI == UNITAI_ATTACK_CITY)
					{
						AreaAITypes eAreaAI = getArea().getAreaAIType(getTeam());
						if (eAreaAI == AREAAI_ASSAULT_MASSING)
							iPromotionValue += 35;
						else if (eAreaAI == AREAAI_ASSAULT || eAreaAI == AREAAI_ASSAULT_ASSIST)
							iPromotionValue += 20;
						else iPromotionValue += 12;
					}
					else iPromotionValue += 8;
				}
				else if (kPromo.getCityDefensePercent() > 0)
				{
					if (eUnitAI == UNITAI_CITY_DEFENSE)
						iPromotionValue += 15;
					else if (eUnitAI == UNITAI_ATTACK || eUnitAI == UNITAI_ATTACK_CITY)
						iPromotionValue += 4;
					else iPromotionValue += 8;
				}
				else if (kPromo.getSameTileHealChange())
				{
					if (eUnitAI == UNITAI_ATTACK_CITY)
						iPromotionValue += 4;
					else iPromotionValue += 12;
				}
				else if (kPromo.getCombatPercent() > 0)
					iPromotionValue += 15;
				else iPromotionValue += 12; // generic
			}
		}

		iValue *= (iPromotionValue + 100);
		iValue /= 100;

		if (bAsync)
		{
			iValue *= (GC.getASyncRand().get(50, "AI Best Unit ASYNC") + 100);
			iValue /= 100;
		}
		else
		{
			iValue *= SyncRandNum(50) + 100;
			iValue /= 100;
		}


		// K-Mod note: I've removed the happy-from-hurry calculation, because it was inaccurate and difficult to fix.
		// (int iBestHappy = 0; ... canHurryUnit ...)

		/*iValue *= (kOwner.getNumCities() * 2);
		iValue /= (kOwner.getUnitClassCountPlusMaking((UnitClassTypes)iI) +
				kOwner.getNumCities() + 1);*/ // BtS
		// K-Mod
		{
			int iUnits = kOwner.getUnitClassCountPlusMaking(kUnit.getUnitClassType());
			int iCities = kOwner.getNumCities();

			iValue *= 6 + iUnits + 4*iCities;
			iValue /= 3 + 3*iUnits + 2*iCities;
			// this is a factor between 1/3 and 2. It's equal to 1 roughly when iUnits == iCities.
		}
		// K-Mod end

		FAssert(MAX_INT / 1000 > iValue);
		//iValue *= 1000;
		/*  advc.001: The K-Mod code below multiplies by ProductionModifier, which
			is at least 100. Don't need that much precision, and the results get
			too close to MAX_INT. */
		iValue *= 10;

		bool bSuicide = GC.getInfo(eUnit).isSuicide();

		if (bSuicide)
		{
			//much of this is compensated
			iValue /= 3;
		}

		//iValue /= std::max(1, (getProductionTurnsLeft(eLoopUnit, 0) + (GC.getInfo(eLoopUnit).isSuicide() ? 1 : 4))); // advc.004x: Replaced by K-Mod. Also note that this would result in an integer overflow during disorder.
		// K-Mod. The number of turns is usually not so important. What's important is how much it is going to cost us to build this unit.
		int iProductionNeeded = getProductionNeeded(eUnit) - getUnitProduction(eUnit);
		// note: this is a 'multiplier' rather than modifier.
		int iProductionModifier = getBaseYieldRateModifier(YIELD_PRODUCTION, getProductionModifier(eUnit));
		iValue *= iProductionModifier;
		// a bit of dilution.
		iValue /= std::max(1, iProductionNeeded +
				getBaseYieldRate(YIELD_PRODUCTION) * iProductionModifier / 100);
		// maybe we should have a special bonus for building it in 1 turn?  ... maybe not.
		// K-Mod end

		iValue = std::max(1, iValue);
		if (iValue > iBestValue)
		{
			iBestValue = iValue;
			eBestUnit = eUnit;
		}
	}

	return eBestUnit;
}


BuildingTypes CvCityAI::AI_bestBuilding(int iFocusFlags, int iMaxTurns,
	bool bAsync, AdvisorTypes eIgnoreAdvisor) const
{
	return AI_bestBuildingThreshold(iFocusFlags, iMaxTurns, /*iMinThreshold*/ 0, bAsync, eIgnoreAdvisor);
}

BuildingTypes CvCityAI::AI_bestBuildingThreshold(int iFocusFlags, int iMaxTurns,
	int iMinThreshold, bool bAsync, AdvisorTypes eIgnoreAdvisor) const
{
	PROFILE_FUNC(); // advc.opt
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner()); // K-Mod

	bool bAreaAlone = kOwner.AI_isAreaAlone(getArea());
	int iProductionRank = findYieldRateRank(YIELD_PRODUCTION);

	int iBestValue = 0;
	BuildingTypes eBestBuilding = NO_BUILDING;

	if (iFocusFlags & BUILDINGFOCUS_CAPITAL)
	{
		int iBestTurnsLeft = (iMaxTurns > 0 ? iMaxTurns : MAX_INT);
		CvCivilization const& kCiv = getCivilization(); // advc.003w
		for (int i = 0; i < kCiv.getNumBuildings(); i++)
		{
			BuildingTypes eLoopBuilding = kCiv.buildingAt(i);
			if (GC.getInfo(eLoopBuilding).isCapital())
			{
				if (canConstruct(eLoopBuilding))
				{
					int iTurnsLeft = getProductionTurnsLeft(eLoopBuilding, 0);
					if (iTurnsLeft <= iBestTurnsLeft)
					{
						eBestBuilding = eLoopBuilding;
						iBestTurnsLeft = iTurnsLeft;
					}
				}
			}
		}

		return eBestBuilding;
	}

	// K-Mote note: I've rearranged most of the code below to improve readability and efficiency.
	// Some changes are marked, but most are not.
	// (At least 6 huge nested 'if' blocks have been replaced with 'continue' conditions.)
	CvCivilization const& kCiv = getCivilization(); // advc.003w
	for (int i = 0; i < kCiv.getNumBuildings(); i++)
	{
		BuildingClassTypes eLoopClass = kCiv.buildingClassAt(i);
		if (kOwner.isBuildingClassMaxedOut(eLoopClass, GC.getInfo(eLoopClass).getExtraPlayerInstances()))
			continue;
		BuildingTypes eLoopBuilding = kCiv.buildingAt(i);
		if (getNumBuilding(eLoopBuilding) >= GC.getDefineINT(CvGlobals::CITY_MAX_NUM_BUILDINGS))
			continue;

		if (iFocusFlags & BUILDINGFOCUS_WORLDWONDER &&
			!GC.getInfo(eLoopClass).isWorldWonder())
		{
			continue;
		}
		if (GC.getInfo(eLoopClass).isLimited())
		{
			if (isProductionAutomated())
				continue;
			if (iFocusFlags != 0 && !(iFocusFlags & BUILDINGFOCUS_WONDEROK))
				continue;
		}

		CvBuildingInfo const& kBuilding = GC.getInfo(eLoopBuilding);

		if (eIgnoreAdvisor != NO_ADVISOR && eIgnoreAdvisor == kBuilding.getAdvisorType())
			continue;

		if (!canConstruct(eLoopBuilding))
			continue;

		if (isProductionAutomated() &&
			// advc.003t: Replacing loop
			kBuilding.getPrereqNumOfBuildingClass().isAnyNonDefault())
		{
			continue;
		}

		int iValue = AI_buildingValue(eLoopBuilding, iFocusFlags, iMinThreshold, bAsync);
		if (iValue <= 0)
			continue;

		//

		/*if (kBuilding.getFreeBuildingClass() != NO_BUILDINGCLASS) {
			BuildingTypes eFreeBuilding = (BuildingTypes)GC.getInfo(getCivilizationType()).getCivilizationBuildings(kBuilding.getFreeBuildingClass());
			if (NO_BUILDING != eFreeBuilding) {
				//iValue += (AI_buildingValue(eFreeBuilding, iFocusFlags) * (kOwner.getNumCities() - kOwner.getBuildingClassCountPlusMaking((BuildingClassTypes)kBuilding.getFreeBuildingClass())));
				iValue += (AI_buildingValue(eFreeBuilding, iFocusFlags, 0, bAsync) * (kOwner.getNumCities() - kOwner.getBuildingClassCountPlusMaking((BuildingClassTypes)kBuilding.getFreeBuildingClass())));
			}
		}*/ // BtS - Moved into AI_buildingValue

		// K-Mod
		TechTypes const eObsoleteTech = kBuilding.getObsoleteTech();
		TechTypes const eSpObsoleteTech =
				kBuilding.getSpecialBuildingType() == NO_SPECIALBUILDING ? NO_TECH
				: GC.getInfo(kBuilding.getSpecialBuildingType()).getObsoleteTech();

		if ((eObsoleteTech != NO_TECH && kOwner.getCurrentResearch() == eObsoleteTech) ||
			(eSpObsoleteTech != NO_TECH && kOwner.getCurrentResearch() == eSpObsoleteTech))
		{
			iValue /= 2;
		}
		// K-Mod end

		int const iTurnsLeft = getProductionTurnsLeft(eLoopBuilding, 0);

		// K-Mod
		/*	Block construction of limited buildings in bad places
			(the value check is just for efficiency.
			1250 accounts for the possible +25 random boost) */
		if (iFocusFlags == 0 && /* advc.004x: */ iTurnsLeft < MAX_INT &&
			iValue * 1250 / std::max(1, iTurnsLeft + 3) >= iBestValue)
		{
			int iLimit = GC.getInfo(eLoopClass).getLimit();
			if (iLimit == -1)
			{
				// We're not out of the woods yet. Check for prereq buildings.
				FOR_EACH_NON_DEFAULT_PAIR(kBuilding.
					getPrereqNumOfBuildingClass(), BuildingClass, int)
				{
					BuildingClassTypes const ePrereqClass = perBuildingClassVal.first;
					// I wish this was easier to calculate...
					int iBuilt = kOwner.getBuildingClassCount(eLoopClass);
					int iBuilding = kOwner.getBuildingClassMaking(eLoopClass);
					int iPrereqEach = kOwner.getBuildingClassPrereqBuilding(eLoopBuilding,
							ePrereqClass, -iBuilt);
					int iPrereqBuilt = kOwner.getBuildingClassCount(ePrereqClass);
					FAssert(iPrereqEach > 0);
					iLimit = iPrereqBuilt / iPrereqEach - iBuilt - iBuilding;
					FAssert(iLimit > 0);
					break; // advc (note): I.e. only support one prereq class per building
				}
			}
			if (iLimit != -1)
			{
				const int iMaxNumWonders = (GET_PLAYER(getOwner()).isOneCityChallenge() ?
						GC.getDefineINT(CvGlobals::MAX_NATIONAL_WONDERS_PER_CITY_FOR_OCC) :
						GC.getDefineINT(CvGlobals::MAX_NATIONAL_WONDERS_PER_CITY));
				if (kBuilding.isNationalWonder() && iMaxNumWonders != -1)
				{
					iValue *= iMaxNumWonders + 1 - getNumNationalWonders();
					iValue /= iMaxNumWonders + 1;
				}
				FOR_EACH_CITYAI(pLoopCity, kOwner)
				{
					if (pLoopCity->canConstruct(eLoopBuilding))
					{
						int iLoopValue = pLoopCity->AI_buildingValue(eLoopBuilding, 0, 0, bAsync);
						if (kBuilding.isNationalWonder() && iMaxNumWonders != -1)
						{
							iLoopValue *= iMaxNumWonders + 1 - pLoopCity->getNumNationalWonders();
							iLoopValue /= iMaxNumWonders + 1;
						}
						if (80 * iLoopValue > 100 * iValue)
						{
							if (--iLimit <= 0)
							{
								iValue = 0;
								break;
							}
						}
					}
				}
				// Subtract some points from wonder value, just to stop us from wasting it
				if (kBuilding.isNationalWonder())
				{
					iValue -= 40 + (iMaxNumWonders <= 0 ? 0 :
							(60 * getNumNationalWonders()) / iMaxNumWonders);
				}
			}
		}
		// K-Mod end

		if (kBuilding.isWorldWonder())
		{
			if (iProductionRank <= std::min(3, ((kOwner.getNumCities() + 2) / 3)))
			{
				int iTempValue;
				if (bAsync)
				{
					iTempValue = GC.getASyncRand().get(GC.getInfo(getPersonalityType()).
							getWonderConstructRand(), "Wonder Construction Rand ASYNC");
				}
				else
				{
					iTempValue = SyncRandNum(GC.getInfo(getPersonalityType()).
							getWonderConstructRand());
				}
				if (bAreaAlone)
					iTempValue *= 2;
				iValue += iTempValue;
			}
		}
								if (isWorldWonderClass((BuildingClassTypes)iI))
								{
									if (iProductionRank <= std::min(3, ((GET_PLAYER(getOwnerINLINE()).getNumCities() + 2) / 3)))
									{
										if (bAsync)
										{
											iTempValue = GC.getASyncRand().get(GC.getLeaderHeadInfo(getPersonalityType()).getWonderConstructRand(), "Wonder Construction Rand ASYNC");
										}
										else
										{
											iTempValue = GC.getGameINLINE().getSorenRandNum(GC.getLeaderHeadInfo(getPersonalityType()).getWonderConstructRand(), "Wonder Construction Rand");
										}

										if (bAreaAlone)
										{
											iTempValue *= 2;
										}
										iValue += iTempValue;
									}
								}

		if (bAsync)
		{
			iValue *= (GC.getASyncRand().get(25, "AI Best Building ASYNC") + 100);
			iValue /= 100;
		}
		else
		{
			iValue *= 100 + syncRand().get(25, "AI Best Building",
					eLoopClass, m_iID); // advc.007
			iValue /= 100;
		}

		//iValue += getBuildingProduction(eLoopBuilding);
		iValue += getBuildingProduction(eLoopBuilding) / 4; // K-Mod

		bool bValid = iMaxTurns <= 0 ? true : false;
		if (!bValid)
		{
			bValid = (iTurnsLeft <= GC.AI_getGame().AI_turnsPercent(
					iMaxTurns, GC.getInfo(GC.getGame().getGameSpeedType()).
					getConstructPercent()));
		}
		if (!bValid)
		{
			FOR_EACH_ENUM(Hurry)
			{
				if (canHurryBuilding(eLoopHurry, eLoopBuilding, true) &&
					AI_getHappyFromHurry(eLoopHurry, eLoopBuilding, true) > 0)
				{
					bValid = true;
					break;
				}
			}
		}

		if (bValid /* advc.004x: */ && iTurnsLeft < MAX_INT)
		{
			FAssert(MAX_INT / 1000 > iValue);
			iValue *= 1000;
			iValue /= std::max(1, iTurnsLeft + 3);

			iValue = std::max(1, iValue);
			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				eBestBuilding = eLoopBuilding;
			}
		}
	}
	return eBestBuilding;
}


// (I don't see the point of this function being separate to the "threshold" version)
/*int CvCityAI::AI_buildingValue(BuildingTypes eBuilding, int iFocusFlags) const {
	return AI_buildingValueThreshold(eBuilding, iFocusFlags, 0);
}*/ // BtS

/*	XXX should some of these count cities, buildings, etc. based on teams
	(because wonders are shared...)
	XXX in general, this function needs to be more sensitive to what makes this
	city unique (more likely to build airports if there already is a harbor...) */
/*	This function has been heavily edited for K-Mod
	Scale is roughly 4 = 1 commerce / turn */
int CvCityAI::AI_buildingValue(BuildingTypes eBuilding, int iFocusFlags,
	int iThreshold, bool bConstCache, bool bAllowRecursion,
	bool bIgnoreSpecialists, // advc.121b
	bool bObsolete) const // advc.004c
{
	PROFILE_FUNC();

	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());
	CvTeamAI const& kTeam = GET_TEAM(kOwner.getTeam()); // kekm.16
	CvGame const& kGame = GC.getGame();
	int const iOwnerEra = kOwner.getCurrentEra();
	int const iCitizenValue = AI_citizenValue(); // advc
	CvBuildingInfo const& kBuilding = GC.getInfo(eBuilding);
	BuildingClassTypes const eBuildingClass = kBuilding.getBuildingClassType();
	int const iLimitedWonderLimit = GC.getInfo(eBuildingClass).getLimit();
	bool const bLimitedWonder = (iLimitedWonderLimit >= 0);
	// <advc.131>
	int iTotalBonusYieldMod = 0;
	int iTotalImprFreeSpecialists = 0;
	bool bAnySeaPlotYieldChange = false; // </advc.131>
	// <K-Mod>
	/*	This new value, iPriorityFactor, is used to boost the value of
		productivity buildings without overvaluing productivity.
		The point is to get the AI to build productiviy buildings quickly,
		but not if they come with large negative side effects.
		I may use it for other adjustments in the future. */
	int iPriorityFactor = 100;

	/*	bRemove means that we're evaluating the cost of losing this building
		rather than adding it. the definition used here is just a kludge because
		there currently isn't any other way to tell the difference.
		Currently, bRemove is only in a few parts of the evaluation
		where it is particularly important; for example, bRemove is critical for
		calculating the lost value of obsoleting walls and castles.
		There are several sections which could, in the future, be improved
		using bRemove - but I don't see it as a high priority. */
	bool const bRemove = (getNumBuilding(eBuilding) >=
			GC.getDefineINT(CvGlobals::CITY_MAX_NUM_BUILDINGS));
	// advc.004c: bRemove && !bObsolete is OK; that means spy attack.
	FAssert(!bObsolete || bRemove);

	/*	Veto checks: return zero if the building is not suitable.
		Note: these checks are essentially the same as in the original code,
		they've just been moved. */
	if (iFocusFlags & BUILDINGFOCUS_WORLDWONDER)
	{
		if (!kBuilding.isWorldWonder() ||
			findBaseYieldRateRank(YIELD_PRODUCTION) <= 3)
		{
			/*	Note / TODO: the production condition is from the original BtS code.
				I intend to remove / change that condition in the future. */
			return 0;
		}
	}
	if (kBuilding.isCapital())
		return 0;

    // doc: no pagan wonders if state religion is preferred
    if (kBuilding.isPagan() && GC.getInfo(kOwner.getLeader()).getFavoriteReligion() != NO_RELIGION)
        return 0;

	// <advc.014>
	if(GET_TEAM(getOwner()).isCapitulated() && kBuilding.isWorldWonder() &&
		kBuilding.getHolyCity() == NO_RELIGION)
	{
		return 0;
	} // </advc.014>
	// rfc: disable
    /*FOR_EACH_NON_DEFAULT_PAIR(kBuilding.
		getReligionChange(), Religion, int)
	{
		if (perReligionVal.second > 0 &&
			!GET_TEAM(getTeam()).hasHolyCity(perReligionVal.first))
		{
			return 0;
		}
	}*/
	// Construction value cache.
	/*	Note: the WONDEROK and WORLDWONDER flags should not affect
		the final value - and so cache should not be disabled by those flags. */
	bool const bNeutralFlags = (iFocusFlags &
			~(BUILDINGFOCUS_WONDEROK | BUILDINGFOCUS_WORLDWONDER)) == 0;
	bool const bUseConstructionValueCache = (bNeutralFlags && iThreshold == 0);
	if (bUseConstructionValueCache && m_aiConstructionValue[eBuildingClass] != -1)
		return m_aiConstructionValue[eBuildingClass];
	// </K-Mod>

	ReligionTypes const eStateReligion = kOwner.getStateReligion();

	bool const bAreaAlone = kOwner.AI_isAreaAlone(getArea());
	int const iHasMetCount = GET_TEAM(getTeam()).getHasMetCivCount(true);

	/*	K-Mod note: I've set this to ignore "food is production"
		so that building value is not distorted by that effect. */
	int const iFoodDifference = foodDifference(false, true);

	// Reduce reaction to temporary happy/health problems
	// K-Mod
	int const iHappinessLevel = happyLevel() - unhappyLevel() +
			getEspionageHappinessCounter()/2 - getMilitaryHappiness()/2;
	int const iHealthLevel = goodHealth() - badHealth() +
			getEspionageHealthCounter()/2;
	// K-Mod end
	bool const bProvidesPower = (kBuilding.isPower() ||
			(kBuilding.getPowerBonus() != NO_BONUS &&
			hasBonus(kBuilding.getPowerBonus())) ||
			kBuilding.isAreaCleanPower());
	int const iTotalPopulation = kOwner.getTotalPopulation();
	int const iNumCities = kOwner.getNumCities();
	int const iNumCitiesInArea = getArea().getCitiesPerPlayer(getOwner());
	// <K-Mod>
	int const iCitiesTarget = GC.getInfo(GC.getMap().getWorldSize()).
			getTargetNumCities(); // </K-Mod>

	bool const bHighProductionCity = (findBaseYieldRateRank(YIELD_PRODUCTION) <=
			std::max(3, iNumCities / 2));

	int const iCultureRank = findCommerceRateRank(COMMERCE_CULTURE);
	int const iCulturalVictoryNumCultureCities = kGame.culturalVictoryNumCultureCities();

	bool const bFinancialTrouble = kOwner.AI_isFinancialTrouble();


	// BETTER_BTS_AI_MOD, Victory Strategy AI, 03/08/10, jdog5000: START
	bool const bCulturalVictory1 = kOwner.AI_atVictoryStage(AI_VICTORY_CULTURE1);
	bool const bCulturalVictory2 = kOwner.AI_atVictoryStage(AI_VICTORY_CULTURE2);
	bool const bCulturalVictory3 = kOwner.AI_atVictoryStage(AI_VICTORY_CULTURE3);
	bool const bSpaceVictory1 = kOwner.AI_atVictoryStage(AI_VICTORY_SPACE1);
	// BETTER_BTS_AI_MOD: END

	bool const bCanPopRush = /*kOwner.*/canPopRush(); // advc.912d
	bool const bWarPlan = kOwner.AI_isFocusWar(area()); // advc.105
			//GET_TEAM(getTeam()).getAnyWarPlanCount(true) > 0; // K-Mod
	int const iFoodKept = kOwner.getFoodKept(eBuilding); // advc.912d

	bool bForeignTrade = false;
	{
		int const iNumTradeRoutes = getTradeRoutes();
		for (int i = 0; i < iNumTradeRoutes; i++)
		{
			CvCity* pTradeCity = getTradeCity(i);
			if (pTradeCity == NULL)
				continue;
            // TODO: use continent area
			if (TEAMID(pTradeCity->getOwner()) != getTeam() ||
				!sameArea(*pTradeCity))
			{
				bForeignTrade = true;
				break;
			}
		}
	}

	int iValue = 0;
	for (int iPass = 0; iPass < 2; iPass++)
	{
		/*	K-Mod. This entire block was originally wrapped with the following condition:
			if ((iFocusFlags == 0) || (iValue > 0) || (iPass == 0))
			I've moved this condition to the end of the block
			and tweaked it for better readability. */

		if ((iFocusFlags & BUILDINGFOCUS_DEFENSE) || iPass > 0)
		{
			// <advc> Moved into new function
			iValue += AI_defensiveBuildingValue(eBuilding, bAreaAlone, bWarPlan,
					iNumCities, iNumCitiesInArea, bRemove, bObsolete); // </advc>
		}

		if ((iFocusFlags & BUILDINGFOCUS_ESPIONAGE) || iPass > 0)
		{
			iValue += kBuilding.getEspionageDefenseModifier() / 8;
		}

		if (((iFocusFlags & BUILDINGFOCUS_HAPPY) || iPass > 0) && !isNoUnhappiness())
		{
			int iBestHappy = 0;
			FOR_EACH_ENUM(Hurry)
			{
				if (canHurryBuilding(eLoopHurry, eBuilding, true))
				{
					int iHappyFromHurry = AI_getHappyFromHurry(eLoopHurry, eBuilding, true);
					if (iHappyFromHurry > iBestHappy)
						iBestHappy = iHappyFromHurry;
				}
			}
			iValue += iBestHappy * 10;

			if (kBuilding.isNoUnhappiness())
			{
				//iValue += ((iAngryPopulation * 10) + getPopulation());
				// K-Mod
				int iEstGrowth = iFoodDifference + std::max(0,
						-iHealthLevel+iFoodDifference);
				iValue += std::max(0,
						(getPopulation() - std::max(0, 2*iHappinessLevel)) *
						2 + std::max(0, -iHappinessLevel) * 6 +
						std::max(0, -iHappinessLevel+iEstGrowth) * 4);
				// K-Mod end
			}
			int iGood=0, iBad=0;
			int iBuildingActualHappiness = getAdditionalHappinessByBuilding(
					eBuilding,iGood,iBad);

            // doc: worked improvements
            // TODO: redundant?
            FOR_EACH_ENUM(Improvement)
            {
                iBuildingActualHappiness += kBuilding.getImprovementHappinessPercent(eLoopImprovement) * aiWorkedImprovementCount[eLoopImprovement] / 100;
            }

            // doc: Gardens by the By
            // TODO: move to getAdditionalHappinessByBuilding?
            if (eBuilding == GARDENS_BY_THE_BAY)
                iBuildingActualHappiness += getBuildingGoodHealth() > 0 ? 1 : 0;

			// K-Mod
			int iAngerDelta = std::max(0, -iHappinessLevel + iBuildingActualHappiness)
					-std::max(0, -iHappinessLevel);
			// High value for any immediate change in anger.
			iValue -= iAngerDelta * 4 * iCitizenValue;
			// some extra value if we are still growing (this is a positive change bias)
			if (iAngerDelta < 0 && iFoodDifference > 1)
				iValue -= 10 * iAngerDelta;
			// finally, a little bit of value for happiness which gives us some padding
			int iHappyModifier = 10 * iCitizenValue /
					(3 + std::max(0, iHappinessLevel+  iBuildingActualHappiness) +
					std::max(0, iHappinessLevel) + std::max(0, -iHealthLevel));
			iValue += std::max(0, iBuildingActualHappiness) * iHappyModifier;
			/*	The "iHappinessModifer" is used for some percentage-based happy effects.
				(note. this not the same magnitude as the original definition.) */

			if (iHappinessLevel >= 10)
			{
				iHappyModifier = 1;
			}
			// K-Mod end

			iValue += (-kBuilding.getHurryAngerModifier() * getHurryPercentAnger()) / 100;

			FOR_EACH_ENUM(Commerce)
			{
				//iValue += (kBuilding.getCommerceHappiness(eLoopCommerce) * iHappyModifier) / 4;
				// K-Mod (note, commercehappiness already counted by iBuildingActualHappiness)
				iValue += kBuilding.getCommerceHappiness(eLoopCommerce) * iHappyModifier / 50;
			}

			int iWarWearinessModifer = kBuilding.getWarWearinessModifier();
			if (iWarWearinessModifer != 0)
			{
				//iValue += (-iWarWearinessModifer * iHappyModifier) / 16;
				// K-Mod (again, the immediate effects of this are already counted)
				iValue += -iWarWearinessModifer * getPopulation() * iHappyModifier /
						(bWarPlan ? 400 : 1000);
			}

			/*iValue += (kBuilding.getAreaHappiness() * (iNumCitiesInArea - 1) * 8);
			iValue += (kBuilding.getGlobalHappiness() * iNumCities * 8);*/
			// K-Mod - just a tweak.. nothing fancy.
			iValue += kBuilding.getAreaHappiness() * (iNumCitiesInArea + iCitiesTarget/3) *
					iCitizenValue;
			iValue += kBuilding.getGlobalHappiness() * (iNumCities + iCitiesTarget/2) *
					iCitizenValue;
			// K-Mod end

			int iWarWearinessPercentAnger = kOwner.getWarWearinessPercentAnger();
			int iGlobalWarWearinessModifer = kBuilding.getGlobalWarWearinessModifier();
			if (iGlobalWarWearinessModifer != 0)
			{
				/* iValue += (-(((iGlobalWarWearinessModifer * iWarWearinessPercentAnger / 100) / GC.getPERCENT_ANGER_DIVISOR())) * iNumCities);
				iValue += (-iGlobalWarWearinessModifer * iHappyModifier) / 16; */
				// <K-Mod>
				iValue += iCitizenValue * iNumCities * -iGlobalWarWearinessModifer *
						(iWarWearinessPercentAnger +
						GC.getPERCENT_ANGER_DIVISOR() / (bWarPlan ? 10 : 20)) /
						(100 * GC.getPERCENT_ANGER_DIVISOR()); // </K-Mod>
			}
			FOR_EACH_NON_DEFAULT_PAIR(kBuilding.
				getBuildingHappinessChanges(), BuildingClass, int)
			{
				iValue += (perBuildingClassVal.second *
						kOwner.getBuildingClassCount(perBuildingClassVal.first) * 8);
			}
		}

		if ((iFocusFlags & BUILDINGFOCUS_HEALTHY) || iPass > 0)
			//&& !isNoUnhealthyPopulation() // K-Mod: commented out
		{
			int iGood = 0, iBad = 0; // advc: Better initialize these
			int iBuildingActualHealth = getAdditionalHealthByBuilding(eBuilding,
					iGood, iBad, /* <advc.001h>: */ true);
			int iFutureHealthLevel = iHealthLevel;
			/*  Pretend that we have one less health than we actually do (b/c the
				future holds electrical power and other baddies) */
			if (iOwnerEra >= CvEraInfo::AI_getAgeOfPollution() && !isPower())
			{	// NB: POWER_HEALTH_CHANGE is negative
				iFutureHealthLevel += GC.getDefineINT(CvGlobals::POWER_HEALTH_CHANGE) / 2;
			}
			/*  And replaced four instances of iHealthLevel with iFutureHealthLevel
				in this block of code ... */
			// </advc.001h>
			/*	K-Mod. I've essentially rewritten this evaluation of health;
				but there may still be some bbai code / original bts code. */
			int iWasteDelta = std::max(0, -iFutureHealthLevel - iBuildingActualHealth) -
					std::max(0, -iFutureHealthLevel);
			// High value for change in our food deficit.
			iValue -= (fixp(2.5) * // advc.001h: Increased from 2 to 2.5
					iCitizenValue * (std::max(0, -(iFoodDifference - iWasteDelta)) -
					// advc.001h: Added +futureHealthLevel-iHealthLevel
					std::max(0, -(iFoodDifference + iFutureHealthLevel
					- iHealthLevel)))).round();
			// medium value for change in waste
			//iValue -= iCitValue * iWasteDelta;
			// <advc.001h> Replacing the above; be more afraid of high iWasteDelta
			if(iWasteDelta <= 0)
				iValue -= iCitizenValue * iWasteDelta; // </advc.001h>
			else iValue -= (iCitizenValue * scaled(iWasteDelta).pow(fixp(1.3))).round();
			/*	some extra value if the change will help us grow
				(this is a positive change bias) */
			if (iWasteDelta < 0 && iHappinessLevel > 0)
				iValue -= iCitizenValue * iWasteDelta;
			// finally, a little bit of value for health which gives us some padding
			// advc.001h: Reduced first factor from 10 to 8 (minor balancing)
			iValue += 8 * iCitizenValue * std::max(0, iBuildingActualHealth)/
					(6 + std::max(0, iFutureHealthLevel + iBuildingActualHealth) +
					std::max(0, iFutureHealthLevel));

			/*	If the GW threshold has been reached,
				add some additional value for pollution reduction
				Note. health benefits have already been evaluated */
			if (iBad < 0 && kGame.getGlobalWarmingIndex() > 0)
			{
				int iCleanValue = -2 * iBad;
				iCleanValue *= (100 + 5 * kOwner.getGwPercentAnger());
				iCleanValue /= 100;
				FAssert(iCleanValue >= 0);
				iValue += iCleanValue;
			}
		    // K-Mod end

		    // doc: building health modifier
            // TODO: move to getAdditionalHealthByBuilding
		    if (kBuilding.getBuildingUnhealthModifier() != 0)
		    {
		        int iBadHealthRemoved = (-getBuildingBadHealth() * kBuilding.getBuildingUnhealthModifier()) / 100;
		        iValue += (std::min(iBadHealthRemoved, iBadHealth) * 12) + ((std::max(0, iBadHealthRemoved - iBadHealth) + 1) * iHealthModifier);
		    }

		    // doc: corporation health modifier
            // TODO: move to getAdditionalHealthByBuilding
		    if (kBuilding.getCorporationUnhealthModifier() != 0)
		    {
		        int iBadHealthRemoved = (-getCorporationUnhealth() * kBuilding.getCorporationUnhealthModifier()) / 100;
		        iValue += (std::min(iBadHealthRemoved, iBadHealth) * 12) + ((std::max(0, iBadHealthRemoved - iBadHealth) + 1) * iHealthModifier);
		    }

            // TODO: merge with getAdditionalHealthByBuilding
		    int iBuildingHealth = kBuilding.getHealth();

            // doc: improvement health
		    FOR_EACH_ENUM(Improvement)
		    {
		        iBuildingHealth += kBuilding.getImprovementHealthPercent(eLoopImprovement) * aiWorkedImprovementCount[eLoopImprovement] / 100;
		    }

		    // doc: Indian UP: +1 health from buildings that provide happiness
		    if (getCivilizationType() == INDIA && kBuilding.getHappiness() > 0)
		    {
		        iBuildingHealth += 1;
		    }

            // doc: apply additional building health effects
            if (iBuildingHealth != 0)
		    {
		        iValue += (std::min(iBuildingHealth, iBadHealth) * 12)
                    + (std::max(0, iBuildingHealth - iBadHealth) * iHealthModifier);
		    }

			iValue += kBuilding.getAreaHealth() * (iNumCitiesInArea-1) * 4;
			iValue += kBuilding.getGlobalHealth() * iNumCities * 4;
		}

		if (iFocusFlags & BUILDINGFOCUS_EXPERIENCE || iPass > 0)
		{
			/*	K-Mod (note). currently this new code matches the functionality
				of the old (deleted) code exactly, except that the value is
				reduced in cities that we don't expect to be building troops in. */
			int iWeight = 12;
			iWeight /= iHasMetCount > 0 ? 1 : 2;
			iWeight /= (bWarPlan || (bHighProductionCity &&
					// <advc.017> Avoid Barracks before first Settler
					(isBarbarian() || kOwner.getNumCities() > 1 ||
					kOwner.AI_getNumAIUnits(UNITAI_SETTLE) > 0 ||
					kOwner.AI_getNumCitySites() <= 0)) ? 1 : 4); // </advc.017>
			iValue += kBuilding.getFreeExperience() * iWeight;

			FOR_EACH_NON_DEFAULT_PAIR(kBuilding.
				getUnitCombatFreeExperience(), UnitCombat, int)
			{
				if (canTrain(perUnitCombatVal.first))
					iValue += (perUnitCombatVal.second * iWeight) / 2;
			}

			FOR_EACH_ENUM(Domain)
			{
				int iDomainXPValue = kBuilding.getDomainFreeExperience(eLoopDomain);
				switch (eLoopDomain)
				{
				case DOMAIN_LAND:
					iDomainXPValue *= iWeight; // full weight
					break;
				case DOMAIN_SEA:
					// advc.041: No longer guaranteed by the building's MinAreaSize
					if(isCoastal(GC.getDefineINT(CvGlobals::MIN_WATER_SIZE_FOR_OCEAN) * 2))
					{
						/*	special case. Don't use 'iWeight' because, for sea,
							bHighProductionCity may be too strict. */
						iDomainXPValue *= 7;
					}
					break;
				default:
					iDomainXPValue *= iWeight;
					iDomainXPValue /= 2;
				}
				iValue += iDomainXPValue;
			}
			// K-Mod end
		}

		// since this duplicates BUILDINGFOCUS_EXPERIENCE checks, do not repeat on pass 1
		if ((iFocusFlags & BUILDINGFOCUS_DOMAINSEA))
		{
			iValue += (kBuilding.getFreeExperience() * (iHasMetCount > 0 ? 16 : 8));
			CvCivilization const& kCiv = getCivilization(); // advc.003w
			for (int i = 0; i < kCiv.getNumUnits(); i++)
			{
				UnitTypes eUnit = kCiv.unitAt(i);
				CvUnitInfo& kUnitInfo = GC.getInfo(eUnit);
				UnitCombatTypes eCombatType = kUnitInfo.getUnitCombatType();
				// <advc.rom4> Avoid canTrain call; credits: alberts2 (C2C).
				if(eCombatType == NO_UNITCOMBAT ||
					kUnitInfo.getDomainType() != DOMAIN_SEA ||
					kBuilding.getUnitCombatFreeExperience(eCombatType) == 0)
				{
					continue;
				} // </advc.rom4>
				if(canTrain(eUnit))
				{
					iValue += (kBuilding.getUnitCombatFreeExperience(eCombatType) *
							(iHasMetCount > 0 ? 6 : 3));
				}
			}
			iValue += (kBuilding.getDomainFreeExperience(DOMAIN_SEA) *
					(iHasMetCount > 0 ? 16 : 8));
			// advc.041: No longer guaranteed by the building's MinAreaSize
			if(isCoastal(GC.getDefineINT(CvGlobals::MIN_WATER_SIZE_FOR_OCEAN) * 2))
				iValue += (kBuilding.getDomainProductionModifier(DOMAIN_SEA) / 4);
		}

		if ((iFocusFlags & BUILDINGFOCUS_MAINTENANCE) ||
			(iFocusFlags & BUILDINGFOCUS_GOLD) || (iPass > 0))
		{
			/*	K-Mod, bugfix. getMaintenanceTimes100 is the total,
				with modifiers already applied.
				(note. ideally we'd use "calculateBaseMaintenanceTimes100",
				and that would a avoid problem caused by "we love the X day".
				but doing it this way is slightly faster.) */
			if (kBuilding.getMaintenanceModifier())
			{
				int iExistingUpkeep = getMaintenanceTimes100();
				int iBaseMaintenance = 100 * iExistingUpkeep /
						std::max(1, 100 + getMaintenanceModifier());
				int iNewUpkeep = (iBaseMaintenance * std::max(0,
						100 + getMaintenanceModifier() +
						kBuilding.getMaintenanceModifier())) / 100;
				// slightly more then 4x savings, just to accommodate growth.
				int iTempValue = (iExistingUpkeep - iNewUpkeep) / 22;
				// We want absolute savings, including inflation.
				iTempValue = iTempValue * (100+kOwner.calculateInflationRate()) / 100;
				/*	(note, not just for this particular city -
					because this isn't direct gold production) */
				/* iTempValue *= kOwner.AI_commerceWeight(COMMERCE_GOLD, 0);
				iTempValue /= 100; */

				if (bFinancialTrouble)
					iTempValue = iTempValue*2;

				iValue += iTempValue;
			}
			// K-Mod end
		}

		if (/* advc.121b: */ !bIgnoreSpecialists &&
			((iFocusFlags & BUILDINGFOCUS_SPECIALIST) || iPass > 0))
		{
			// K-Mod. (original code deleted)
			int iSpecialistsValue = 0;
			//int iUnusedSpecialists = 0;
			SpecialistTypes const eDefaultSpecialist = GC.getDEFAULT_SPECIALIST();
			int iAvailableWorkers = iFoodDifference / 2;
			if (eDefaultSpecialist != NO_SPECIALIST)
				iAvailableWorkers += getSpecialistCount(eDefaultSpecialist);
			FOR_EACH_ENUM(Specialist)
			{
				if (eLoopSpecialist == eDefaultSpecialist)
					continue;

				int iLimit = kOwner.isSpecialistValid(eLoopSpecialist) ?
						getPopulation() :
						std::max(0, getMaxSpecialistCount(eLoopSpecialist)
						-getSpecialistCount(eLoopSpecialist));
				/*	in rare situations, this function can be called while citizens are
					incorrectly assigned. So I've forced the min condition in the line above. */
				FAssert(iLimit >= 0);
				//iUnusedSpecialists += iLimit;

				if (kBuilding.getSpecialistCount(eLoopSpecialist) > 0 && iLimit <= 2)
				{
					int iTempValue = AI_specialistValue(eLoopSpecialist, false, false);

					iTempValue *= (iLimit == 0 ? 60 : 0) + 40 * std::min<int>(iAvailableWorkers,
							kBuilding.getSpecialistCount(eLoopSpecialist));
					/*	I'm choosing not to reduce 'iAvailableWorkers'...
						It's a tough call. Either way, the answer is going to be wrong! */
					iTempValue /= 100 + 200 * iLimit;
					iSpecialistsValue += iTempValue / 100;
				}
			}
			if (iSpecialistsValue > 0)
				iValue += iSpecialistsValue;
			// K-Mod end
		}

		if ((iFocusFlags & (BUILDINGFOCUS_GOLD | BUILDINGFOCUS_RESEARCH)) || iPass > 0)
		{
			// trade routes
			// K-Mod. (original code deleted)
			int iTotalTradeModifier = totalTradeModifier();
			int iTempValue = kBuilding.getTradeRoutes() *
					(getTradeRoutes() > 0 ?
					5 * getTradeYield(YIELD_COMMERCE) / getTradeRoutes() :
					5 * (getPopulation() / 5 + 1) * iTotalTradeModifier / 100);
			//int iGlobalTradeValue = (6 * iTotalPopulation / (5 * iNumCities) + 1) * kOwner.AI_averageYieldMultiplier(YIELD_COMMERCE) / 100;
			/*	1.2 * average population seems wrong. Instead, do something
				roughly comparable to what's used in CvPlayerAI::AI_civicValue.*/
			int iGlobalTradeValue = (bForeignTrade ? 5 : 3) *
					(2 * (iOwnerEra + 1) + GC.getNumEraInfos()) / GC.getNumEraInfos();

            // doc: include culture level trade route modifier
            int iTotalTradeRouteModifier = kBuilding.getTradeRouteModifier() + kBuilding.getCultureTradeRouteModifier() * getCultureLevel();
			iTempValue += 5 * iTotalTradeRouteModifier *
					getTradeYield(YIELD_COMMERCE) / std::max(1, iTotalTradeModifier);

			if (bForeignTrade)
			{
				iTempValue += 3 * kBuilding.getForeignTradeRouteModifier() *
						getTradeYield(YIELD_COMMERCE) /
						std::max(1, iTotalTradeModifier+getForeignTradeRouteModifier());
			}

			iTempValue *= AI_yieldMultiplier(YIELD_COMMERCE);
			iTempValue /= 100;
			{
				int const iCoastalTradeRoutes = kBuilding.getCoastalTradeRoutes();
				if (iCoastalTradeRoutes != 0)
				{
					int const iCoastalCities = kOwner.countNumCoastalCities();
					// <advc.131>
					scaled rCoastalCitySites;
					int const iCitySites = kOwner.AI_getNumCitySites();
					for (int i = 0; i < iCitySites; i++)
					{
						if (kOwner.AI_getCitySite(i).isCoastalLand(-1))
						{	/*	Less likely to claim lower-priority sites;
								and it'll take longer. */
							rCoastalCitySites += 1 - scaled(i, iCitySites);
						}
					}
					// K-Mod formula:
					//std::max((iCitiesTarget+1)/2, kOwner.countNumCoastalCities())
					int iProjectedCoastalCities = (iCoastalCities + rCoastalCitySites +
							/*	City placement will favor the coast more once we have
								extra trade routes */
							scaled(iCoastalTradeRoutes, 2)).uround();
					// </advc.131>
					iTempValue += iCoastalTradeRoutes * iProjectedCoastalCities *
							iGlobalTradeValue;
				}
			}
			// <advc.310>
			iTempValue += kBuilding.getAreaTradeRoutes() *
					// Same formula as for AreaHappiness (Notre Dame)
					(iNumCitiesInArea + iCitiesTarget / 3) // </advc.310>
					//std::max(iCitiesTarget, iNumCities)
					* iGlobalTradeValue;
			// K-Mod end

			if (bFinancialTrouble)
				iTempValue *= 2;
			if (kOwner.isNoForeignTrade())
				iTempValue /= 2; // was /3

			iValue += iTempValue;
		}

		if (iPass > 0)
		{
			/*	K-Mod. The value of golden age buildings.
				(This was not counted by the original AI.) */
			{
				int iGoldenPercent =  0;
				if (kBuilding.isGoldenAge())
					iGoldenPercent += 100;
				if (kBuilding.getGoldenAgeModifier() != 0)
				{
					iGoldenPercent *= kBuilding.getGoldenAgeModifier();
					iGoldenPercent /= 100;
					/*	It's difficult to estimate the value of the golden age modifier.
						Firstly, we don't know how many golden ages we are going to have;
						but that's a relatively minor problem. We can just guess that.
						A bigger problem is that the value of a golden age can change a lot
						depending on the state of the civilzation.
						The upshot is that the value here is going to be rough... */
					iGoldenPercent += 3 * kBuilding.getGoldenAgeModifier() *
							(GC.getNumEraInfos() - iOwnerEra) / (GC.getNumEraInfos() + 1);
				}
				if (iGoldenPercent > 0)
				{
					/*	note, the value returned by AI_calculateGoldenAgeValue is roughly
						in units of commerce points; whereas, iValue in this function is
						roughly in units of 4 * commerce / turn.
						I'm just going to say 44 points of golden age commerce is roughly
						worth 1 commerce per turn. (so conversion is 4/44) */
					iValue += (kOwner.AI_calculateGoldenAgeValue(false) *
							iGoldenPercent) / (100 * 11);
				}
			}
			// K-Mod end

			// BETTER_BTS_AI_MOD, City AI, 02/24/10, jdog5000 & Afforess: START
			if (kBuilding.isAreaCleanPower() && !getArea().isCleanPower(getTeam()))
			{
				FOR_EACH_CITY(pLoopCity, kOwner)
				{
					if (sameArea(*pLoopCity))
					{
						if (pLoopCity->isDirtyPower())
							iValue += 12;
						else if (!pLoopCity->isPower())
						{
							//iValue += 8;
							/*	K-Mod. Giving power should be more valuable
								than replacing existing power! */
							iValue += 24;
						}
					}
				}
			}

			if (kBuilding.getDomesticGreatGeneralRateModifier() != 0)
				iValue += (kBuilding.getDomesticGreatGeneralRateModifier() / 10);

			if (kBuilding.isAreaBorderObstacle() &&
				!getArea().isBorderObstacle(getTeam()) &&
				// advc.001n: AI_getNumAreaCitySites might cache FoundValue
				!bConstCache)
			{	// <advc.310>
				int iGameEra = kGame.getCurrentEra();
				/*  A check for GAMEOPTION_NO_BARBARIANS is unnecessary
					b/c the Great Wall ability is then disabled via CvInfos. */
				if (!GC.getInfo((EraTypes)iGameEra).isNoBarbUnits() ||
					getArea().getCitiesPerPlayer(BARBARIAN_PLAYER) > iGameEra)
				{	//  Available city sites should correlate with nearby barb activity.
					int iDummy=-1;
					int iAreaCitySites = kOwner.AI_getNumAreaCitySites(getArea(), iDummy);
					if(kGame.isOption(GAMEOPTION_RAGING_BARBARIANS))
						iAreaCitySites *= 2;
					iValue += 6 * iAreaCitySites;
					// BBAI code:
					/* if(!g.isOption(GAMEOPTION_NO_BARBARIANS)) {
						iValue += (iNumCitiesInArea);
						if(g.isOption(GAMEOPTION_RAGING_BARBARIANS))
							iValue += (iNumCitiesInArea);
					} */ // </advc.310>
				}
			} // BETTER_BTS_AI_MOD: END

			if (kBuilding.isGovernmentCenter())
			{
				FAssert(!kBuilding.isCapital());
				//iValue += ((calculateDistanceMaintenance() - 3) * iNumCitiesInArea);
				// K-mod. More bonus for colonies, because it reduces that extra maintenance too.
				int iTempValue = 2*(calculateDistanceMaintenance() - 2) * iNumCitiesInArea;
				if (!kOwner.hasCapital() || !sameArea(*kOwner.getCapital()))
					iTempValue *= 2;
				iValue += iTempValue;
				// K-Mod end
			}

			if (kBuilding.isMapCentering())
				iValue++;

			if (kBuilding.getFreeBonus() != NO_BONUS)
			{
				iValue += kOwner.AI_bonusVal((BonusTypes)kBuilding.getFreeBonus(), 1) *
						((kOwner.getNumTradeableBonuses(
						(BonusTypes)kBuilding.getFreeBonus()) == 0) ? 2 : 1) *
						(iNumCities + //kBuilding.getNumFreeBonuses()
						// advc.001: Based on the Mongoose Mod changelog (15 Feb 2013)
						kGame.getNumFreeBonuses(eBuilding));
			}

			if (kBuilding.getNoBonus() != NO_BONUS)
				iValue -= kOwner.AI_bonusVal(kBuilding.getNoBonus(), /* K-Mod: */ 0);

			if (kBuilding.getFreePromotion() != NO_PROMOTION)
			{
				//iValue += ((iHasMetCount > 0) ? 100 : 40); // XXX some sort of promotion value???
				// K-Mod.
				/*	Ideally, we'd use AI_promotionValue to work out what the promotion
					is worth, but, unfortunately, that function requires a target unit,
					and I can't think of a good way to choose a suitable unit for evaluation.
					So.. I'm just going to do a really basic kludge to stop the Dun
					from being worth more than Red Cross */
				CvPromotionInfo const& kInfo = GC.getInfo(kBuilding.getFreePromotion());
				bool const bAdvanced = (kInfo.getPrereqPromotion() != NO_PROMOTION ||
						kInfo.getPrereqOrPromotion1() != NO_PROMOTION ||
						kInfo.getPrereqOrPromotion2() != NO_PROMOTION ||
						kInfo.getPrereqOrPromotion3() != NO_PROMOTION);
				int iTemp = (bAdvanced ? 200 : 40);
				int iProduction = getYieldRate(YIELD_PRODUCTION);
				iTemp *= 2*iProduction;
				iTemp /= 30 + iProduction;
				iTemp *= getFreeExperience() + 1;
				iTemp /= getFreeExperience() + 2;
				iValue += iTemp;
				// cf. iValue += (kBuilding.getFreeExperience() * ((iHasMetCount > 0) ? 12 : 6));
				// K-Mod end
			}

			CivicOptionTypes const eCivicOption = kBuilding.getCivicOption();
			if (eCivicOption != NO_CIVICOPTION)
			{	// k146 (Todo): compare to current civics!
				// <advc.131> Will do:
				scaled rCivicOptionValue;
				/*	Should actually be 4(!), but I don't think it's good for game balance
					to make the AI that interested in the Pyramids. */
				scaled const rScaleAdjustment = fixp(2.5);
				scaled rCurrentCivicValue = rScaleAdjustment *
						kOwner.AI_civicValue(kOwner.getCivics(eCivicOption));
				scaled rBestNewCivicValue = scaled::min(0, rCurrentCivicValue);
				FOR_EACH_ENUM(Civic)
				{
					if (GC.getInfo(eLoopCivic).getCivicOptionType() != eCivicOption ||
						kOwner.canDoCivics(eLoopCivic))
					{
						continue; // advc
					}
					//iValue += (kOwner.AI_civicValue(eLoopCivic) / 10);
					scaled rCivicValue = rScaleAdjustment *
							kOwner.AI_civicValue(eLoopCivic);
					if (rCivicValue > 0)
					{
						// Devalue civics that we'll soon unlock anyway
						TechTypes eTech = GC.getInfo(eLoopCivic).getTechPrereq();
						if (!kTeam.isHasTech(eTech) &&
							GC.getInfo(eTech).getEra() <= kOwner.getCurrentEra())
						{
							rCivicValue /= 2;
						}
						// Having choices is good; even if they're not the best right now.
						rCivicOptionValue += rCivicValue / 12;
					}
					rBestNewCivicValue.increaseTo(rCivicValue);
				}
				rCivicOptionValue += rBestNewCivicValue - rCurrentCivicValue;
				iValue += rCivicOptionValue.round();
				// </advc.131>
			}

			int iGreatPeopleRateModifier = kBuilding.getGreatPeopleRateModifier();

            // doc: culture level great people rate modifier
		    iGreatPeopleRateModifier += kBuilding.getCultureGreatPeopleRateModifier() * getCultureLevel();

            // doc: Shwedagon Paya effect
		    if (eBuilding == SHWEDAGON_PAYA)
		        iGreatPeopleRateModifier += 50;

			if (iGreatPeopleRateModifier > 0)
			{
				int iGreatPeopleRate = getBaseGreatPeopleRate();
				// advc.131: was 10 flat
				int const iTargetGPRate = 5 + 2 * std::max(1, iOwnerEra);

				// either not a wonder, or a wonder and our GP rate is at least the target rate
				if (!bLimitedWonder || iGreatPeopleRate >= iTargetGPRate)
				{	/*  advc.131: Divisor was 16. I think GPP are worth more than that,
						and need to account for future growth. */
					iValue += (iGreatPeopleRateModifier * iGreatPeopleRate) / 9;
				}
				/*	otherwise, this is a limited wonder (aka National Epic),
					we _really_ do not want to build this here.
					subtract from the value.
					(if this wonder has a lot of other stuff, we still might build it.) */
				else
				{
					iValue -= (iGreatPeopleRateModifier *
							(iTargetGPRate - iGreatPeopleRate)) / 12;
				}
			}

			iValue += (kBuilding.getGlobalGreatPeopleRateModifier() * iNumCities) / 8;
			iValue -= kBuilding.getAnarchyModifier() / 4;
			iValue -= kBuilding.getGlobalHurryModifier() * 2;
			iValue += kBuilding.getGlobalFreeExperience() * iNumCities *
					(iHasMetCount > 0 ? 6 : 3);

			/*if (bCanPopRush)
				iValue += iFoodKept / 2;*/ // BtS
			// (moved to where the rest of foodKept is valued)

			/*iValue += kBuilding.getAirlift() * (getPopulation()*3 + 10);
			int iAirDefense = -kBuilding.getAirModifier();
			if (iAirDefense > 0) {
				if (((kOwner.AI_totalUnitAIs(UNITAI_DEFENSE_AIR) > 0) && (kOwner.AI_totalUnitAIs(UNITAI_ATTACK_AIR) > 0)) || (kOwner.AI_totalUnitAIs(UNITAI_MISSILE_AIR) > 0))
					iValue += iAirDefense / ((iHasMetCount > 0) ? 2 : 4);
			}
			iValue += kBuilding.getAirUnitCapacity() * (getPopulation() * 2 + 10);
			iValue += (-(kBuilding.getNukeModifier()) / ((iHasMetCount > 0) ? 10 : 20));*/ // BtS
			// (This stuff is already counted in the defense section.)
			// <K-Mod>
			iValue += std::max(0, kBuilding.getAirUnitCapacity() -
					getPlot().airUnitSpaceAvailable(getTeam())/2) *
					(getPopulation() + 12); // </K-Mod>

			/*iValue += (kBuilding.getFreeSpecialist() * 16);
			iValue += (kBuilding.getAreaFreeSpecialist() * iNumCitiesInArea * 12);
			iValue += (kBuilding.getGlobalFreeSpecialist() * iNumCities * 12);*/ // BtS
			// K-Mod. Still very rough, but a bit closer to true value.  (this is for the Statue of Liberty)
			{
				int iFreeSpecialists = kBuilding.getFreeSpecialist() +
						kBuilding.getAreaFreeSpecialist() * iNumCitiesInArea +
						kBuilding.getGlobalFreeSpecialist() * iNumCities;
				if (iFreeSpecialists > 0)
				{
					int iSpecialistValue = 20 * 100; // rough base value
					// additional bonuses
					FOR_EACH_ENUM(Commerce)
					{
						if (kOwner.getSpecialistExtraCommerce(eLoopCommerce))
						{
							iSpecialistValue +=
									kOwner.getSpecialistExtraCommerce(eLoopCommerce) *
									4 * kOwner.AI_commerceWeight(eLoopCommerce);
						}
					}
					iSpecialistValue += 8 * std::max(0,
							kOwner.AI_averageGreatPeopleMultiplier() - 100);
					iValue += iFreeSpecialists * iSpecialistValue / 100;
				}
			}
			// K-Mod end

			iValue += ((kBuilding.getWorkerSpeedModifier() *
					kOwner.AI_getNumAIUnits(UNITAI_WORKER)) / 10);

			int iMilitaryProductionModifier = kBuilding.getMilitaryProductionModifier();
			if (iHasMetCount > 0 && iMilitaryProductionModifier > 0)
			{
				// either not a wonder, or a wonder and we are a high production city
				if (!bLimitedWonder || bHighProductionCity)
				{
					iValue += iMilitaryProductionModifier / 4;
					// if a wonder, then pick one of the best cities
					if (bLimitedWonder)
					{
						// if one of the top 3 production cities, give a big boost
						if (findBaseYieldRateRank(YIELD_PRODUCTION) <=
							2 + iLimitedWonderLimit)
						{
							iValue += (2 * iMilitaryProductionModifier) /
									(2 + findBaseYieldRateRank(YIELD_PRODUCTION));
						}
					}
					// otherwise, any of the top half of cities will do
					else if (bHighProductionCity)
						iValue += iMilitaryProductionModifier / 4;
					iValue += (iMilitaryProductionModifier *
							(getFreeExperience() + getSpecialistFreeExperience())) / 10;
				}
				/*	otherwise, this is a limited wonder (aka Heroic Epic),
					we _really_ do not want to build this here
					subtract from the value (if this wonder has a lot of other stuff,
					we still might build it) */
				else
				{
					iValue -= (iMilitaryProductionModifier *
							findBaseYieldRateRank(YIELD_PRODUCTION)) / 5;
				}
			}

			iValue += (kBuilding.getSpaceProductionModifier() / 5);
			iValue += ((kBuilding.getGlobalSpaceProductionModifier() * iNumCities) / 20);

			// advc.020: Handled later now
			/*if (kBuilding.getGreatPeopleUnitClass() != NO_UNITCLASS)
				iValue++; // XXX improve this for diversity...*/

			/*	prefer to build great people buildings in places
				that already have some GP points */
			//iValue += (kBuilding.getGreatPeopleRateChange() * 10) * (1 + (getBaseGreatPeopleRate() / 2));
			/*	K-Mod... here's some code like the specialist value function.
				Kind of long, but much better. */
			{
				// everything seems to be x4 around here
				int iTempValue = 100 * kBuilding.getGreatPeopleRateChange() * 2 * 4;
				UnitClassTypes eGPClass = kBuilding.getGreatPeopleUnitClass();
				// <advc.020>
				if(iTempValue > 0 && eGPClass != NO_UNITCLASS)
				{
					UnitTypes eGPUnit = getCivilization().getUnit(eGPClass);
					if(eGPUnit != NO_UNIT)
					{
						/*	Just adding a flavor bonus may overrate GPP in general.
							Apply a small malus when the flavor does not match. */
						int iFlavorModifier = -1;
						FOR_EACH_ENUM(Flavor)
						{
							// Mostly 5 or 2, occasionally 10
							iFlavorModifier += std::min(GC.getInfo(kOwner.
									getPersonalityType()).getFlavorValue(eLoopFlavor),
									// GP flavor is at most 1
									5 * GC.getInfo(eGPUnit).getFlavorValue(eLoopFlavor));
						}
						iTempValue += iFlavorModifier *
								kBuilding.getGreatPeopleRateChange() * 100;
					}
				} // </advc.020>
				int iCityRate = getGreatPeopleRate();
				int iHighestRate = 0;
				FOR_EACH_CITY(pLoopCity, kOwner)
				{
					int x = pLoopCity->getGreatPeopleRate();
					if (x > iHighestRate)
						iHighestRate = x;
				}
				if (iHighestRate > iCityRate)
				{
					iTempValue *= 100;
					iTempValue /= (2 * 100 * (iHighestRate + 3)) / (iCityRate + 3) - 100;
				}
				iTempValue *= getTotalGreatPeopleRateModifier();
				iTempValue /= 100;
				iValue += iTempValue / 100;
			}
			// K-Mod end
			if (!bAreaAlone)
				iValue += (kBuilding.getHealRateChange() / 2);
			iValue += kBuilding.getGlobalPopulationChange() * iNumCities * 4;
			// iValue += (kBuilding.getFreeTechs() * 80);
			/*	K-Mod. A slightly more nuanced evaluation of free techs
				(but still very rough) */
			if (kBuilding.getFreeTechs() > 0)
			{
				int iTotalTechValue = 0;
				int iMaxTechValue = 0;
				int iTechCount = 0;

				FOR_EACH_ENUM(Tech)
				{
					if (kOwner.canResearch(eLoopTech, false, true)) // advc
					{
						int iTechValue = GET_TEAM(getTeam()).getResearchCost(eLoopTech);
						iTotalTechValue += iTechValue;
						iTechCount++;
						iMaxTechValue = std::max(iMaxTechValue, iTechValue);
					}
				}
				if (iTechCount > 0)
				{
					int iTechValue = ((iTotalTechValue / iTechCount) + iMaxTechValue) / 2;

					/*  It's hard to measure an instant boost with units of
						commerce per turn... So I'm just going to divide it by
						(k146) ~12.5, scaled by game speed */
					iValue += iTechValue * 8 / GC.getInfo(GC.getGame().getGameSpeedType()).
							getResearchPercent();
				}
				// else: If there is nothing to research, a free tech is worthless.
			}

			iValue += kBuilding.getEnemyWarWearinessModifier() / 2;
			FOR_EACH_NON_DEFAULT_PAIR(kBuilding.
				getFreeSpecialistCount(), Specialist, int)
			{
				iValue += AI_permanentSpecialistValue(
						perSpecialistVal.first/*, false, false*/) * // K-Mod
						perSpecialistVal.second / /* K-Mod: was 50 */ 100;
			}
			FOR_EACH_NON_DEFAULT_PAIR(kBuilding.
				getImprovementFreeSpecialist(), Improvement, int)
			{
				iValue += countNumImprovedPlots(perImprovementVal.first, true) * 50 *
						perImprovementVal.second;
				iTotalImprFreeSpecialists += perImprovementVal.second; // advc.131
			}
			FOR_EACH_ENUM(Domain)
			{
				iValue += (kBuilding.getDomainProductionModifier(eLoopDomain) / 5);
				if (bHighProductionCity)
					iValue += kBuilding.getDomainProductionModifier(eLoopDomain) / 5;
			}

			FOR_EACH_ENUM(Unit)
			{
				if (GC.getInfo(eLoopUnit).getPrereqBuilding() == eBuilding)
				{
					// BBAI TODO: Smarter monastery construction, better support for mods

					if (kOwner.AI_totalAreaUnitAIs(getArea(),
						GC.getInfo(eLoopUnit).getDefaultUnitAIType()) == 0)
					{
						iValue += iNumCitiesInArea;

                        // doc: really make sure that we can build nukes
                        if (GC.getInfo(eLoopUnit).getNukeRange() > 0)
                            iValue *= 5;
					}
					iValue++;
					ReligionTypes const eReligion = GC.getInfo(eLoopUnit).getPrereqReligion();
					if (eReligion != NO_RELIGION)
					{
						//encouragement to get some minimal ability to train special units
						if (bCulturalVictory1 || isHolyCity(eReligion) || isCapital())
							iValue += (2 + iNumCitiesInArea);

						if (bCulturalVictory2 &&
							GC.getInfo(eLoopUnit).getReligionSpreads(eReligion))
						{
							/*	this gives a very large extra value - if the religion is
								(nearly) unique - to no extra value for a fully spread religion.
								I'm torn between huge boost and enough to bias towards
								the best monastery type. */
							int iReligionCount = kOwner.getHasReligionCount(eReligion);
							iValue += (100 * (iNumCities - iReligionCount)) /
									(iNumCities * (iReligionCount + 1));
						}
					}
				}
			}

			// is this building needed to build other buildings?

			// K-Mod
			// (I've deleted the original code for this section.)
			if (bAllowRecursion)
			{	// (moved from AI_bestBuildingThreshold)
				BuildingClassTypes eFreeClass = kBuilding.getFreeBuildingClass();
				if (eFreeClass != NO_BUILDINGCLASS)
				{
					BuildingTypes eFreeBuilding = getCivilization().getBuilding(eFreeClass);
					if (NO_BUILDING != eFreeBuilding)
					{	/*  K-Mod note: this is actually a pretty poor approximation
							because the value of the free building is
							likely to be different in the other cities. also,
							if the free building is very powerful, then our
							other cities will probably build it themselves
							before they get the freebie!
							(that's why I reduce the city count below) */
						int iFreeBuildingValue = std::min(
								AI_buildingValue(eFreeBuilding, 0, 0, bConstCache, false),
								kOwner.getProductionNeeded(eFreeBuilding) / 2);
						iValue += iFreeBuildingValue *
								(std::max(iCitiesTarget, kOwner.getNumCities()*2/3) -
								kOwner.getBuildingClassCountPlusMaking(eFreeClass));
					}
				}
				CvCivilization const& kCiv = getCivilization(); // advc.003w
				for (int i = 0; i < kCiv.getNumBuildings(); i++)
				{
					BuildingTypes eLoopBuilding = kCiv.buildingAt(i);
					BuildingClassTypes eLoopClass = kCiv.buildingClassAt(i);
					int iPrereqBuildings = 0; // number of eBuilding required by eLoopBuilding
					CvBuildingInfo const& kLoopBuilding = GC.getInfo(eLoopBuilding);
					int const iLimitForLoopBuilding = GC.getInfo(eLoopClass).getLimit();
					int const iPrereqNumOfBuildingClass = kLoopBuilding.
							getPrereqNumOfBuildingClass(eBuildingClass);
					if ((iPrereqNumOfBuildingClass <= 0 &&
						!kLoopBuilding.isBuildingClassNeededInCity(eBuildingClass)) ||
						(iLimitForLoopBuilding > 0 &&
						// advc.opt: Was getBuildingClassMaking; no need to call canConstruct for that.
						kOwner.getBuildingClassCountPlusMaking(eLoopClass) >= iLimitForLoopBuilding) ||
						!kOwner.canConstruct(eLoopBuilding, false, true, false))
					{
						/*	either we don't need eBuilding in order to build eLoopBuilding,
							or we can't construct eLoopBuilding anyway */
						/*  NOTE: the above call to canConstruct will return true even
							if the city already has the maximum number of national wonders.
							This is a minor flaw in the AI. */
						continue;
					}

					if (iPrereqNumOfBuildingClass > 0)
					{	/*	calculate how many more of eBuilding we actually need,
							given that we might be constructing some eLoopBuilding already. */
						iPrereqBuildings = kOwner.getBuildingClassPrereqBuilding(
								eLoopBuilding, eBuildingClass,
								kOwner.getBuildingClassMaking(eLoopClass));
						FAssert(iPrereqBuildings > 0);
						/*	subtract the number of eBuildings we have already.
							(Note, both BuildingClassCount and BuildingClassMaking
							are cached. This is fast.) */
						iPrereqBuildings -= kOwner.getBuildingClassCount(eBuildingClass);
					}

					/*	only score the local building requirement
						if the civ-wide requirement is already met */
					if (kLoopBuilding.isBuildingClassNeededInCity(eBuildingClass) &&
						getNumBuilding(eBuilding) == 0 && iPrereqBuildings <= 0)
					{
						if (kBuilding.getProductionCost() > 0 &&
							kLoopBuilding.getProductionCost() > 0)
						{
							int iTempValue = AI_buildingValue(
									eLoopBuilding, 0, 0, bConstCache, false);
							if (iTempValue > 0)
							{
								/*	scale the bonus value by a rough approximation of
									how likely we are the build the thing (note. the
									combined production cost is essentially the cost of completing
									kLoopBuilding given our current position.) */
								iTempValue *= 2 * kBuilding.getProductionCost();
								iTempValue /= 2 * kBuilding.getProductionCost() +
										3 * kLoopBuilding.getProductionCost();
								iValue += iTempValue;
							}
						}
					}

					if (iPrereqBuildings <= 0 || iPrereqBuildings > iNumCities)
						continue;
					/*	We've already subtracted the number of eBuilding
						that are already built. Now we subtract the number of eBuilding
						that we are currently constructing. */
					iPrereqBuildings -= kOwner.getBuildingClassMaking(eBuildingClass);
							// (keep it simple)
							//- (getFirstBuildingOrder(eBuilding) < 0 ? 0 : 1);
					if (iPrereqBuildings <= 0)
						continue;
					/*	Now we work out how valuable it would be
						to enable eLoopBuilding; and then scale that value
						by how many more eBuildings we need. */
					int iCanBuildPrereq = 0;
					FOR_EACH_CITY(pLoopCity, kOwner)
					{
						if (pLoopCity->canConstruct(eBuilding) &&
							pLoopCity->getProductionBuilding() != eBuilding)
						{
							iCanBuildPrereq++;
						}
					}
					if (iCanBuildPrereq < iPrereqBuildings)
						continue;
					int iHighestValue = 0;
					FOR_EACH_CITYAI(pLoopCity, kOwner)
					{
						if (pLoopCity->getProductionBuilding() != eLoopBuilding &&
						/*  advc (comment): bVisible=true means: check only if the building
							appears in the production list. In particular, prereq buildings
							aren't checked, which is good. However, the national wonder limit
							also isn't checked, which is bad.
							Same problem a bit higher up in this function (K-Mod comment:
							"This is a minor flaw in the AI.") */
							pLoopCity->canConstruct(eLoopBuilding, false, true))
						{
							iHighestValue = std::max(
									pLoopCity->AI_buildingValue(
									eLoopBuilding, 0, 0, bConstCache, false),
									iHighestValue);
						}
					}
					int iTempValue = iHighestValue;
					iTempValue *= iCanBuildPrereq + 3 * iPrereqBuildings;
					iTempValue /= (iPrereqBuildings + 1) *
							(3 * iCanBuildPrereq + iPrereqBuildings);
					/*	That's between 1/(iPrereqBuildings+1) and 1/3*(iPrereqBuildings+1),
						depending on # needed and # buildable */
					iValue += iTempValue;
				}
			}
			// K-Mod end (prereqs)

			FOR_EACH_ENUM2(VoteSource, eVS)
			{
				if(kBuilding.getVoteSourceType() != eVS)
					continue; // advc
				// BETTER_BTS_AI_MOD, City AI, Victory Strategy AI, 05/24/10, jdog5000: START
				int iTempValue = 0;
				if (kBuilding.isStateReligion())
				{
					int iShareReligionCount = 0;
					int iOtherPlayers = 0;
					for(PlayerIter<MAJOR_CIV> itOther; itOther.hasNext(); ++itOther)
					{
						if (itOther->getID() == getOwner())
							continue;
						iOtherPlayers++;
						if (kOwner.getStateReligion() == itOther->getStateReligion())
							iShareReligionCount++;
					}
					//iTempValue += (200 * (1 + iShareReligionCount)) / (1 + iPlayerCount);
					// <advc.178>
					iTempValue += ((125 *
							/*  Don't need everyone to share the religion
								(but at least someone) */
							scaled::min(scaled(iOtherPlayers, 2), iShareReligionCount)) /
							std::max(1, iOtherPlayers)).round(); // </advc.178>
				}
				else
				{
					//iTempValue += 100;
					iTempValue += 75; // advc.115b
				}
				// BETTER_BTS_AI_MOD: END
				// <advc.115b>
				int iDiploStage = 0;
				if(kOwner.AI_atVictoryStage(AI_VICTORY_DIPLOMACY1))
					iDiploStage++;
				/*  Don't want to push AP as much b/c the victory stage is (so far)
					hardly meaningful for that */
				if(!kBuilding.isStateReligion() &&
					kOwner.AI_atVictoryStage(AI_VICTORY_DIPLOMACY2))
				{
					iDiploStage++;
				}
				// (3 and 4 aren't possible without the respective vote source)
				//iValue += iTempValue * 3 * diploStage;
				iTempValue *= 3 * iDiploStage;
				/*  K-Mod code didn't factor in AI_VICTORY_DIPLOMACY2 b/c that
					stage wasn't used at the time */
				//iValue += (iTempValue * (kOwner.AI_atVictoryStage(AI_VICTORY_DIPLOMACY1) ? 5 : 1));
				// Don't pave the way for rival victory
				int iMaxRivalStage = 0;
				bool bHumanRival = false;
				for (PlayerAIIter<FREE_MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> it(getTeam());
					it.hasNext(); ++it)
				{
					CvPlayerAI const& kRival = *it;
					int iRivalStage = 0;
					if(kRival.AI_atVictoryStage(AI_VICTORY_DIPLOMACY1))
						iRivalStage++;
					if(!kBuilding.isStateReligion() &&
						kOwner.AI_atVictoryStage(AI_VICTORY_DIPLOMACY2))
					{
						iRivalStage++;
					}
					if(iRivalStage > iMaxRivalStage ||
						(iRivalStage >= iMaxRivalStage && kRival.isHuman()))
					{
						iMaxRivalStage = iRivalStage;
						bHumanRival = kRival.isHuman();
					}
				}
				if(iMaxRivalStage > iDiploStage ||
					(bHumanRival && iMaxRivalStage >= iDiploStage))
				{
					iTempValue = 0;
					if(iMaxRivalStage >= 3)
						return 0;
				}
				iValue += iTempValue;
				// </advc.115b>  <advc.179>
				if (kBuilding.isStateReligion() && kOwner.isStateReligion())
				{
					std::vector<BuildingTypes> aeReligionBuildings;
					FOR_EACH_ENUM(Building)
					{
						if (GC.getInfo(eLoopBuilding).getReligionType() == eStateReligion)
							aeReligionBuildings.push_back(eBuilding);
					}
					scaled rOurBuildings = AI_estimateReligionBuildings(
							kOwner.getID(), eStateReligion, aeReligionBuildings);
					scaled rTempValue = rOurBuildings;
					scaled rRivalFactor = fixp(1.5) *
							scaled(kGame.countCivPlayersAlive()).sqrt();
					int const iEverAlive = kGame.getCivPlayersEverAlive();
					for (PlayerIter<CIV_ALIVE,KNOWN_TO> it(getTeam()); it.hasNext(); ++it)
					{
						CvPlayer const& kBrother = *it; // Brothers in the faith
						if(kBrother.getID() == kOwner.getID() ||
							kBrother.getStateReligion() != eStateReligion)
						{
							continue;
						}
						AttitudeTypes eTowardThem = ATTITUDE_FURIOUS;
						if(!kBrother.isMinorCiv())
						{
							if (!isHuman())
							{
								eTowardThem = kOwner.AI_getAttitude(kBrother.getID());
								if(GET_TEAM(getTeam()).AI_getWarPlan(
									kBrother.getTeam()) != NO_WARPLAN)
								{
									eTowardThem = std::min(eTowardThem, ATTITUDE_ANNOYED);
								}
							}
							else eTowardThem = kOwner.AI_getAttitude(kBrother.getID());
						}
						bool bTheyAhead = (kGame.getPlayerRank(kBrother.getID()) <
								std::min<int>(kGame.getPlayerRank(kOwner.getID()),
								iEverAlive / 2));
						// Don't care if they benefit from ReligionYield then
						if(!bTheyAhead && eTowardThem <= ATTITUDE_CAUTIOUS &&
							eTowardThem > ATTITUDE_FURIOUS)
						{
							continue;
						}
						scaled rLoopBuildings = AI_estimateReligionBuildings(
								kBrother.getID(), eStateReligion, aeReligionBuildings);
						// Don't want to help competitors win; let _them_ produce eBuilding.
						if(bTheyAhead && eTowardThem < ATTITUDE_FRIENDLY)
							rLoopBuildings.flipSign();
						else
						{
							rLoopBuildings.decreaseTo(rOurBuildings);
							rLoopBuildings /= rRivalFactor;
						}
						rTempValue += rLoopBuildings;
					}
					FOR_EACH_ENUM(Yield)
					{
						int iChange = GC.getInfo(eVS).getReligionYield(eLoopYield);
						if(iChange == 0)
							continue;
						/*  Would be nicer to use CvPlayerAI::AI_commerceWeight,
							but that would have to be applied earlier. */
						rTempValue *= iChange * (eLoopYield == YIELD_COMMERCE ? 4 : 8);
					}
					iValue += rTempValue.round();
				}
			} // </advc.179>
			// BETTER_BTS_AI_MOD, City AI, Victory Strategy AI, 05/24/10, jdog5000: START
			FOR_EACH_ENUM2(VoteSource, eVS)
			{	// advc: some refactoring in this block
				if (!kGame.isDiploVote(eVS) || !kOwner.isLoyalMember(eVS))
					continue;
				// Value religion buildings based on AP gains
				ReligionTypes eReligion = kGame.getVoteSourceReligion(eVS);
				if (eReligion != NO_RELIGION && isHasReligion(eReligion) &&
					kBuilding.getReligionType() == eReligion)
				{	// advc: Renamed "iTempValue" in the two loops below - name clash
					FOR_EACH_ENUM(Yield)
					{
						int iChange = GC.getInfo(eVS).getReligionYield(eLoopYield);
						// K-Mod
						int iYieldVal = iChange * 4; // was 6
						iYieldVal *= AI_yieldMultiplier(eLoopYield);
						//iYieldVal /= 100; // advc: Increase precision
						// advc.001 (loop variables were mixed up here)
						if (eLoopYield == YIELD_PRODUCTION)
						{
							/*	priority += 2.8% per 1% in production increase.
								roughly. More when at war. */
							iPriorityFactor += std::min(100,
									(bWarPlan ? 320 : 280) * iYieldVal /
									// (advc: divisor times 100)
									(100 * std::max(1,
									4 * getYieldRate(YIELD_PRODUCTION))));
						} // K-Mod end
						iYieldVal *= kOwner.AI_yieldWeight(eLoopYield, this);
						iYieldVal /= /*100*/10000; // advc
						iValue += iYieldVal;
					}
					FOR_EACH_ENUM(Commerce)
					{
						int iChange = GC.getInfo(eVS).getReligionCommerce(eLoopCommerce);
						int iCommerceVal = iChange * 4;
						// K-Mod
						if (iCommerceVal == 0)
							continue;
						iCommerceVal *= getTotalCommerceRateModifier(eLoopCommerce);
						//iCommerceVal /= 100; // advc: Increase precision
						// K-Mod end
						iCommerceVal *= kOwner.AI_commerceWeight(eLoopCommerce, this);
						/*	+99 mirrors code below, I think because commerce weight
							can be pretty small. (It's so it rounds up, not down. - K-Mod) */
						iCommerceVal = (iCommerceVal + /*99*/9900) / /*100*/10000; // advc
						iValue += iCommerceVal;
					}
				}
				// BETTER_BTS_AI_MOD: END
			}
		}

		if (iPass > 0)
		{
			/*	K-Mod, I've moved this from inside the yield types loop;
				and I've increased the value to compensate. */
			if (iFoodDifference > 0 && iFoodKept != 0)
			{
				//iValue += iFoodKept / 2;
				iValue += (std::max(0,
						2 * (std::max(4, AI_getTargetPopulation()) - getPopulation()) +
						(bCanPopRush ? 3 : 1)) * iFoodKept) / 4;
			} // K-Mod end

			FOR_EACH_ENUM(Yield)
			{
				// K-Mod - I've shuffled some parts of this code around.
				int iTempValue = 0;

				/*iTempValue += ((kBuilding.getYieldModifier(eLoopYield) * getBaseYieldRate(eLoopYield)) / 10);
				iTempValue += ((kBuilding.getPowerYieldModifier(eLoopYield) * getBaseYieldRate(eLoopYield)) / ((bProvidesPower || isPower()) ? 12 : 15));*/
				// K-Mod
				// +2 just to represent potential growth.
				int iBaseRate = getBaseYieldRate(eLoopYield) + 2;
				iTempValue += kBuilding.getYieldModifier(eLoopYield) * iBaseRate / 25;
				iTempValue += kBuilding.getPowerYieldModifier(eLoopYield) * iBaseRate /
						(bProvidesPower || isPower() ? 27 : 50);

				if (bProvidesPower && !isPower())
				{
					iTempValue += (getPowerYieldRateModifier(eLoopYield) * iBaseRate) /
							27; // was 12
				}

				FOR_EACH_NON_DEFAULT_PAIR(kBuilding.
					getBonusYieldModifier(), Bonus, YieldPercentMap)
				{
					if (hasBonus(perBonusVal.first))
					{
						int iBonusYieldMod = perBonusVal.second[eLoopYield];
						iTempValue += (iBonusYieldMod * iBaseRate) /
								27; // was 12
						iTotalBonusYieldMod += iBonusYieldMod; // advc.131
					}
				}

                // doc (1SDAN): bonus yield change
                // TODO: NESTED ARRAY EXAMPLE
                FOR_EACH_NON_DEFAULT_PAIR(kBuilding.
                    getBonusYieldChange(), Bonus, YieldPercentMap)
                {
                    int iBonusYieldMod = perBonusVal.second[eLoopYield] * countNumBonusPlots[perBonusVal.first];
                    iTempValue += iBonusYieldMod / 27; // was 12
                    // TODO: we should not add this to advc.131
                }

				/*	if this is a limited wonder, and we are not in the top 4
					of this category, subtract the value - we do _not_ want this here
					(unless the value was small anyway) */
				//if (bLimitedWonder && (findBaseYieldRateRank(eLoopYield) > (3 + iLimitedWonderLimit)))
				/*	K-Mod: lets say top 1/3 instead. There are now other mechanisms
					to stop us from wasting buildings. */
				if (bLimitedWonder &&
					findBaseYieldRateRank(eLoopYield) >
					iNumCities/3 + 1 + iLimitedWonderLimit)
				{
					iTempValue *= -1;
				}

				/*	(K-Mod)...and now the things that should not depend
					on whether or not we have a good yield rank */
				int iRawYieldValue = 0;
				/*	K-Mod, don't count trade commerce here, because that has already
					been counted earlier... (the systme is a mess, I know.) */
				if (eLoopYield != YIELD_COMMERCE)
				{
					iRawYieldValue += ((kBuilding.getTradeRouteModifier() *
							getTradeYield(eLoopYield)) / 26); // was 12 (and 'iValue')
					//if (bForeignTrade)
					if (bForeignTrade && !kOwner.isNoForeignTrade()) // K-Mod
					{
						iRawYieldValue += ((kBuilding.getForeignTradeRouteModifier() *
								getTradeYield(eLoopYield)) / 35); // was 12 (and 'iValue')
					}
				}

				/*if (iFoodDifference > 0)
					iValue += iFoodKept / 2;*/ // BtS
				// (We're inside a yield types loop. This would be triple counted here!)

				// advc.131: was >
				if (kBuilding.getSeaPlotYieldChange(eLoopYield) != 0)
				{
					iRawYieldValue += kBuilding.getSeaPlotYieldChange(eLoopYield) *
							//AI_buildingSpecialYieldChangeValue(eBuilding, eLoopYield);
							// <K-Mod>
							AI_buildingSeaYieldChangeWeight(eBuilding,
							iFoodDifference > 0 && iHappinessLevel > 0); // </K-Mod>
					bAnySeaPlotYieldChange = true; // advc.131
				}
				// advc.131: was >
				if (kBuilding.getRiverPlotYieldChange(eLoopYield) != 0)
				{
					iRawYieldValue += kBuilding.getRiverPlotYieldChange(eLoopYield) *
							countNumRiverPlots() *
                            // doc: emphasize food and commerce more
                            4 * (eLoopYield == YIELD_FOOD ? 5 : 1) * (eLoopYield == YIELD_COMMERCE ? 2 : 1);
				}
                // doc: flat river plot yield change
                // TODO: count FLAT river plots
                if (kBuilding.getFlatRiverPlotYieldChange(eLoopYield) != 0)
                {
                    iRawYieldValue += kBuildingFlatRiverPlotYieldChange(eLoopYield) *
                            countNumRiverPlots() *
                            // doc: emphasize food and commerce more
                            4 * (eLoopYield == YIELD_FOOD ? 5 : 1) * (eLoopYield == YIELD_COMMERCE ? 2 : 1);
                }
				iRawYieldValue += kBuilding.getYieldChange(eLoopYield) * 4; // was 6

				iRawYieldValue *= AI_yieldMultiplier(eLoopYield);
				iRawYieldValue /= 100;
				iTempValue += iRawYieldValue;
				FOR_EACH_NON_DEFAULT_PAIR(kBuilding.
					getSpecialistYieldChange(), Specialist, YieldChangeMap)
				{
					iTempValue += (perSpecialistVal.second[eLoopYield] *
							iTotalPopulation) / 5;
				}
				iTempValue += kBuilding.getGlobalSeaPlotYieldChange(eLoopYield) *
						kOwner.countNumCoastalCities() * 8;
				iTempValue += (kBuilding.getAreaYieldModifier(eLoopYield) *
						iNumCitiesInArea) / 3;
				iTempValue += (kBuilding.getGlobalYieldModifier(eLoopYield) *
						iNumCities) / 3;
				if (iTempValue != 0)
				{
					/*if (bFinancialTrouble && iI == YIELD_COMMERCE)
						iTempValue *= 2;*/ // BtS (this is rolled into AI_yieldWeight)

					// K-Mod
					if (eLoopYield == YIELD_PRODUCTION)
					{
						// priority += 2.4% per 1% in production increase. roughly. More when at war.
						iPriorityFactor += std::min(100, (bWarPlan ? 280 : 240) *
								iTempValue/std::max(1, 4*getYieldRate(YIELD_PRODUCTION)));
					} // K-Mod end
					iTempValue *= kOwner.AI_yieldWeight(eLoopYield, this);
					iTempValue /= 100;
					// (limited wonder condition use to be here. I've moved it. - Karadoc)
					iValue += iTempValue;
				}
			}
		}
		else
		{
			if (iFocusFlags & BUILDINGFOCUS_FOOD)
			{
				iValue += iFoodKept;
				// advc.131: was >
				if (kBuilding.getSeaPlotYieldChange(YIELD_FOOD) != 0)
				{
					int iTempValue = kBuilding.getSeaPlotYieldChange(YIELD_FOOD) *
							//AI_buildingSpecialYieldChangeValue(eBuilding, YIELD_FOOD)
							// <K-Mod>
							AI_buildingSeaYieldChangeWeight(eBuilding,
							iFoodDifference > 0 && iHappinessLevel > 0); // </K-Mod>
					if (iTempValue < 8 && getPopulation() > 3)
					{
						// don't bother
					}
					else iValue += (iTempValue * 4) / std::max(2, iFoodDifference);
				}
				// advc.131: was >
				if (kBuilding.getRiverPlotYieldChange(YIELD_FOOD) != 0)
				{
					iValue += (kBuilding.getRiverPlotYieldChange(YIELD_FOOD) *
							countNumRiverPlots() * 8); // doc: increased from 4 - emphasize river food
				}
                // doc: flat river plot yield change
                // TODO: count FLAT river plots
                if (kBuilding.getFlatRiverPlotYieldChange(YIELD_FOOD) != 0)
                {
                    iValue += kBuilding.getFlatRiverPlotYieldChange(YIELD_FOOD) * countNumRiverPlots() * 8);
                }
			}
			if (iFocusFlags & BUILDINGFOCUS_PRODUCTION)
			{
				int iTempValue = (kBuilding.getYieldModifier(YIELD_PRODUCTION) *
						getBaseYieldRate(YIELD_PRODUCTION)) / 20;
				iTempValue += (kBuilding.getPowerYieldModifier(YIELD_PRODUCTION) *
						getBaseYieldRate(YIELD_PRODUCTION)) /
						((bProvidesPower || isPower()) ? 24 : 30);
				if (kBuilding.getSeaPlotYieldChange(YIELD_PRODUCTION) > 0)
				{
					int iNumWaterPlots = countNumWaterPlots();
					if (!bLimitedWonder || iNumWaterPlots > NUM_CITY_PLOTS / 2)
					{
						iTempValue += kBuilding.getSeaPlotYieldChange(YIELD_PRODUCTION) *
								iNumWaterPlots;
					}
				}
				// advc.131: was >
				if (kBuilding.getRiverPlotYieldChange(YIELD_PRODUCTION) != 0)
				{
					iTempValue += (kBuilding.getRiverPlotYieldChange(YIELD_PRODUCTION) *
							countNumRiverPlots() * 4);
				}
                // doc: flat river plot yield
                // TODO: count FLAT river plots
                if (kBuilding.getFlatRiverPlotYieldChange(YIELD_PRODUCTION) != 0)
                {
                    iTempValue += kBuilding.getFlatRiverPlotYieldChange(YIELD_PRODUCTION) *
                            countNumRiverPlots() * 4);
                }
				if (bProvidesPower && !isPower())
				{
					iTempValue += (getPowerYieldRateModifier(YIELD_PRODUCTION) *
							//getBaseYieldRate(YIELD_PRODUCTION)) / 12;
							getBaseYieldRate(YIELD_PRODUCTION)) / 24; // K-Mod, consistency
				}

				/*	if this is a limited wonder, and we are not in the top 4
					of this category, subtract the value -  we do _not_ want this here
					(unless the value was small anyway) */
				if (bLimitedWonder &&
					findBaseYieldRateRank(YIELD_PRODUCTION) >
					3 + iLimitedWonderLimit)
				{
					iTempValue *= -1;
				}
				iValue += iTempValue;
			}

			if (iFocusFlags & BUILDINGFOCUS_GOLD)
			{
				int iTempValue = (kBuilding.getYieldModifier(YIELD_COMMERCE) *
						getBaseYieldRate(YIELD_COMMERCE));
				iTempValue *= kOwner.getCommercePercent(COMMERCE_GOLD);
				if (bFinancialTrouble)
					iTempValue *= 2;
				iTempValue /= 3000;

				/*if (MAX_INT == aiCommerceRank[COMMERCE_GOLD])
					aiCommerceRank[COMMERCE_GOLD] = findCommerceRateRank(COMMERCE_GOLD);*/

				/*	if this is a limited wonder, and we are not in the top 4
					of this category, subtract the value -  we do _not_ want this here
					(unless the value was small anyway) */
				if (bLimitedWonder &&
					findCommerceRateRank(COMMERCE_GOLD) >
					3 + iLimitedWonderLimit)
				{
					iTempValue *= -1;
				}
				iValue += iTempValue;
			}
		}
		if (iPass > 0)
		{
			FOR_EACH_ENUM(Commerce)
			{
				int iTempValue = kBuilding.getCommerceChange(eLoopCommerce) * 4;
				iTempValue += kBuilding.getObsoleteSafeCommerceChange(eLoopCommerce) * 4;
				// BETTER_BTS_AI_MOD, City AI, 03/13/10, jdog5000: START
				if (kBuilding.getReligionType() != NO_RELIGION &&
					kBuilding.getReligionType() == kOwner.getStateReligion())
				{
					iTempValue += kOwner.getStateReligionBuildingCommerce(eLoopCommerce) * 3;
				}
				// BETTER_BTS_AI_MOD END
				// Moved from below (K-Mod)
				iTempValue += ((kBuilding.getSpecialistExtraCommerce(eLoopCommerce) *
						iTotalPopulation) / 3);
				//iTempValue *= 100 + kBuilding.getCommerceModifier(eLoopCommerce);
				// K-Mod. Note that getTotalCommerceRateModifier() includes the +100.
				iTempValue *= getTotalCommerceRateModifier(eLoopCommerce) +
						kBuilding.getCommerceModifier(eLoopCommerce);
				iTempValue /= 100;
				int const iCommerceChangeDoubleTime = kBuilding.
						getCommerceChangeDoubleTime(eLoopCommerce);
				if (iCommerceChangeDoubleTime > 0)
				{
					if (kBuilding.getCommerceChange(eLoopCommerce) > 0)
					{	//iTempValue += (1000 / kBuilding.getCommerceChangeDoubleTime(eLoopCommerce));
						// K-Mod (still very rough...):
						iTempValue += (iTempValue * 250) / iCommerceChangeDoubleTime;
					}
					if (kBuilding.getObsoleteSafeCommerceChange(eLoopCommerce) > 0)
					{
						iTempValue += (iTempValue * 250) /
								// <advc.098>
								(GC.getDefineBOOL(CvGlobals::DOUBLE_OBSOLETE_BUILDING_COMMERCE) ?
								1000 : // </advc.098>
								iCommerceChangeDoubleTime);
					}
				}
				bool bExpandBorders = false; // advc.192
				if (eLoopCommerce == COMMERCE_CULTURE)
				{
					if (bCulturalVictory1)
						iTempValue *= 2;
					/*	K-Mod. Build culture buildings quickly to pop our borders
						(but not wonders / special buildings) */
					if (iTempValue > 0 && !bLimitedWonder &&
						kBuilding.getProductionCost() > 0 &&
						AI_needsCultureToWorkFullRadius())
					{
						iPriorityFactor += 25;
						//iTempValue += 16;
						/*	<advc.192> (This will execute mostly in the early game.
							We have time for some computations.) */
						bExpandBorders = true; // Remember for later
						int iClaimedBonuses = 0;
						int iClaimedBonusVal = 0;
						for (CityPlotIter itPlot(*this, false); itPlot.hasNext(); ++itPlot)
						{
							if (itPlot->getOwner() == kOwner.getID() ||
								!itPlot->isRevealed(kOwner.getTeam()))
							{
								continue;
							}
							BonusTypes eBonus = itPlot->getNonObsoleteBonusType(kOwner.getTeam());
							if (eBonus != NO_BONUS)
							{
								iClaimedBonuses++;
								FOR_EACH_ENUM(Build)
								{
									if (kOwner.doesImprovementConnectBonus(
										GC.getInfo(eLoopBuild).getImprovement(), eBonus) &&
										kOwner.canBuild(*itPlot, eLoopBuild,
										false, true)) // To allow unowned plots
									{
										iClaimedBonusVal += kOwner.AI_bonusVal(eBonus, 1);
										break;
									}
								}
							}
						}
						int iClaimValue = 0;
						if (iClaimedBonuses > 0)
						{
							/*	All cities could benefit ... possibly, and we'll need
								a worker; therefore halve the value. */
							iClaimValue += (iClaimedBonusVal * kOwner.getNumCities()) / 2;
							iClaimValue += (9 * scaled(iClaimedBonuses).
									pow(fixp(0.75))).uround();
						}
						iClaimValue += 7;
						/*	Prefer to expand soon - also to be consistent with preferential
							treatment for fast expansion in AI_chooseProduction. */
						if (!AI_isSwiftBorderExpansion(getProductionTurnsLeft(eBuilding, 0)))
							iClaimValue /= 2;
						iTempValue += iClaimValue;
						//</advc.192>
					} // K-Mod end
				}

				/*	K-Mod. the getCommerceChangeDoubleTime bit use to be here.
					I moved it up to be before the culture value boost. */

				// add value for a commerce modifier
				int iCommerceModifier = kBuilding.getCommerceModifier(eLoopCommerce);
				int iBaseCommerceRate = getBaseCommerceRate(eLoopCommerce);
				// <advc.131> CapitalYieldRate is not included in BaseCommerceRate
				if(isCapital())
				{
					iBaseCommerceRate *= 100 + kOwner.
							getCapitalYieldRateModifier(YIELD_COMMERCE);
					iBaseCommerceRate /= 100;
				} // Anticipate growth and techs that increase yield
				iBaseCommerceRate = (iBaseCommerceRate * scaled::max(1,
						fixp(4/3.) - kGame.gameTurnProgress() / 2)).
						round(); // </advc.131>
				{ // K-Mod.
					/*  inflate the base commerce rate, to account for the fact
						that commerce multipliers give us flexibility. */
					/*  <k146> But not for espionage. Because... reasons.
						(Espionage gets a priority bonus later. That's good
						enough.) */
					int x = std::max(eLoopCommerce == COMMERCE_ESPIONAGE ? 0 : 5,
							kOwner.getCommercePercent(eLoopCommerce));
					// </k146>
					if (eLoopCommerce == COMMERCE_CULTURE)
					{
						x += x <= 45 && bCulturalVictory1 ? 10 : 0;
						x += x <= 45 && bCulturalVictory2 ? 10 : 0;
						x += x <= 45 && bCulturalVictory3 ? 10 : 0;
					}
					iBaseCommerceRate += getYieldRate(YIELD_COMMERCE) * x *
							(100 - x) / 10000;
				} // K-Mod end

				int iCommerceMultiplierValue = iCommerceModifier * iBaseCommerceRate;
				if (eLoopCommerce == COMMERCE_CULTURE && iCommerceModifier != 0)
				{	/*	K-Mod: bug fix, and improvement.
						(the old code was missing /= 100, and it was too conditional) */
					/*	(disabled indefinitely. culture pressure is counted in other ways;
						so I want to test without this boost.) */
					//iCommerceMultiplierValue *= culturePressureFactor() + 100;
					//iCommerceMultiplierValue /= 200;
					// K-Mod end

					/*	K-Mod. the value of culture is now boosted primarily
						inside AI_commerceWeight so I've decreased the value boost
						in the following block. */
					if (bCulturalVictory1)
					{
						/*	if this is one of our top culture cities,
							then we want to build this here first! */
						if (iCultureRank <= iCulturalVictoryNumCultureCities)
						{
							iCommerceMultiplierValue /= 15; // was 8

							// if we at culture level 3, then these need to get built asap
							if (bCulturalVictory3)
							{
								int iHighestRate = 0;
								FOR_EACH_CITY(pLoopCity, kOwner)
								{
									iHighestRate = std::max(iHighestRate,
											pLoopCity->getCommerceRate(COMMERCE_CULTURE));
								}
								FAssert(iHighestRate >= getCommerceRate(COMMERCE_CULTURE));
								/*	it's most important to build in the lowest rate city,
									but important everywhere */
								iCommerceMultiplierValue += (iHighestRate -
										getCommerceRate(COMMERCE_CULTURE)) *
										iCommerceModifier / 15; // was 8
							}
						}
						else
						{
							//int iCountBuilt = kOwner.getBuildingClassCountPlusMaking(eBuildingClass);
							/*	K-Mod (to match the number used by
								getBuildingClassPrereqBuilding) */
							int iCountBuilt = kOwner.getBuildingClassCount(eBuildingClass);

							// do we have enough buildings to build extras?
							bool bHaveEnough = true;

							/*	if its limited and the limit is less than the
								number we need in culture cities, do not build here */
							if (bLimitedWonder &&
								iLimitedWonderLimit <= iCulturalVictoryNumCultureCities)
							{
								bHaveEnough = false;
							}
							FOR_EACH_ENUM(BuildingClass)
							{
								// K-Mod: bug fix.
								/*// count excess the number of prereq buildings which do not have this building built for yet
								int iPrereqBuildings = kOwner.getBuildingClassPrereqBuilding(eBuilding, eLoopBuildingClass, -iCountBuilt);
								// do we not have enough built (do not count ones in progress)
								if (iPrereqBuildings > 0 && kOwner.getBuildingClassCount(eLoopBuildingClass) < iPrereqBuildings)
									bHaveEnough = false;*/ // BtS
								// Whatever that code was meant to do, I'm pretty sure it was wrong.
								int iPrereqBuildings = kOwner.getBuildingClassPrereqBuilding(
										eBuilding, eLoopBuildingClass,
										iCulturalVictoryNumCultureCities - iCountBuilt);
								if (kOwner.getBuildingClassCount(eLoopBuildingClass) <
									iPrereqBuildings)
								{
									break;
								} // K-Mod end
							}

							/*	if we have enough and our rank is close to the top,
								then possibly build here too */
							if (bHaveEnough &&
								(iCultureRank - iCulturalVictoryNumCultureCities) <= 3)
							{
								iCommerceMultiplierValue /= 20; // was 12
							}
							// otherwise, we really do not want to build this here
							else iCommerceMultiplierValue /= 50; // was 30
						}
					}
					else
					{
						iCommerceMultiplierValue /= 25; // was 15

						// increase priority if we need culture oppressed city
						/*	K-Mod: moved this to outside of the current "if".
							It should still apply even when going for a cultural victory! */
						//iCommerceMultiplierValue *= (100 - calculateCulturePercent(getOwner()));
					}
				}
				else
				{
					iCommerceMultiplierValue /= 25; // was 15
				}
				iTempValue += iCommerceMultiplierValue;

				// K-Mod. help get the ball rolling on espionage.
				if (eLoopCommerce == COMMERCE_ESPIONAGE && iTempValue > 0 &&
					!kGame.isOption(GAMEOPTION_NO_ESPIONAGE))
				{
					/*	priority += 1% per 1% increase in total espionage,
						more for big espionage strategy */
					iPriorityFactor += std::min(100,
							(kOwner.AI_isDoStrategy(AI_STRATEGY_BIG_ESPIONAGE) ? 150 : 100) *
							iTempValue/std::max(1, 4 *
							kOwner.getCommerceRate(COMMERCE_ESPIONAGE)));
				}

				/*	... and increase the priority of research buildings
					if aiming for a space victory. */
				if (eLoopCommerce == COMMERCE_RESEARCH && bSpaceVictory1)
					iPriorityFactor += std::min(25, iTempValue/2);
				// K-Mod end

				iTempValue += (kBuilding.getGlobalCommerceModifier(eLoopCommerce) * iNumCities) / 4;
				// moved up (K-Mod)
				// iTempValue += ((kBuilding.getSpecialistExtraCommerce(eLoopCommerce) * iTotalPopulation) / 3);

				/*if (eStateReligion != NO_RELIGION)
					iTempValue += (kBuilding.getStateReligionCommerce(eLoopCommerce) * kOwner.getHasReligionCount(eStateReligion) * 3);
				*/ // BtS
				/*	K-Mod. A more accurate calculation of the value from
					increasing commerce on all state religion buildings. (eg. Sankore) */
				if (eStateReligion != NO_RELIGION &&
					kBuilding.getStateReligionCommerce(eLoopCommerce) != 0)
				{
					int iCount = 0;
					CvCivilization const& kCiv = getCivilization(); // advc.003w
					for (int i = 0; i < kCiv.getNumBuildings(); i++)
					{
						BuildingTypes eLoopBuilding = kCiv.buildingAt(i);
						if (GC.getInfo(eLoopBuilding).getReligionType() == eStateReligion &&
							!GET_TEAM(kOwner.getTeam()).isObsoleteBuilding(eLoopBuilding))
						{
							iCount += kOwner.getBuildingClassCountPlusMaking(
									kCiv.buildingClassAt(i));
						}
					}
					iCount = std::max(iCount, kOwner.getHasReligionCount(eStateReligion));
					iTempValue += iCount * 35 *
							kOwner.AI_averageCommerceMultiplier(eLoopCommerce) / 1000;
				}
				// K-Mod end
				ReligionTypes const eGlobalCommerceReligion = kBuilding.
						getGlobalReligionCommerce();
				if (eGlobalCommerceReligion != NO_RELIGION)
				{
					/*iTempValue += (GC.getInfo((ReligionTypes)(kBuilding.getGlobalReligionCommerce())).getGlobalReligionCommerce(eLoopCommerce) * g.countReligionLevels((ReligionTypes)kBuilding.getGlobalReligionCommerce()) * 2);
					if (eStateReligion == (ReligionTypes)(kBuilding.getGlobalReligionCommerce()))
						iTempValue += 10;*/
					// K-Mod
					int iExpectedSpread = kGame.countReligionLevels(eGlobalCommerceReligion);
					iExpectedSpread += ((//GC.getNumEraInfos() - iOwnerEra +
							// <advc.erai> Current era plus subsequent eras
							1 + CvEraInfo::normalizeEraNum(
							GC.getNumEraInfos() - iOwnerEra - 1) + // </advc.erai>
							(eStateReligion == eGlobalCommerceReligion ? 2 : 0)) *
							//GC.getInfo(GC.getMap().getWorldSize()).getDefaultPlayers()
							kGame.getRecommendedPlayers()).round(); // advc.137
					iTempValue += GC.getInfo(eGlobalCommerceReligion).
							getGlobalReligionCommerce(eLoopCommerce) * iExpectedSpread * 4;
				}
				/*	K-Mod: I've moved the corporation stuff that use to be here
					to outside this loop so that it isn't quadriple counted */
				if (kBuilding.isCommerceFlexible(eLoopCommerce) &&
					!kOwner.isCommerceFlexible(eLoopCommerce))
				{
					iTempValue += 40;
				}
				if (kBuilding.isCommerceChangeOriginalOwner(eLoopCommerce))
				{
					if (kBuilding.getCommerceChange(eLoopCommerce) > 0 ||
						kBuilding.getObsoleteSafeCommerceChange(eLoopCommerce) > 0)
					{
						iTempValue++;
					}
				}
				if (iTempValue != 0)
				{
					if (bFinancialTrouble && eLoopCommerce == COMMERCE_GOLD)
						iTempValue *= 2;
					/*	advc.192: Culture weight doesn't account for additional
						workable plots. If that's what we're after, we should
						ignore the weight (which is going to be small). */
					if (!bExpandBorders || eLoopCommerce != COMMERCE_CULTURE)
					{
						iTempValue *= kOwner.AI_commerceWeight(eLoopCommerce, this);
						iTempValue = intdiv::uceil(iTempValue, 100);
					}
					/*	if this is a limited wonder, and we are not in the top 4
						of this category, subtract the value - we do _not_ want this here
						(unless the value was small anyway) */
					/*if (MAX_INT == aiCommerceRank[eLoopCommerce])
						aiCommerceRank[eLoopCommerce] = findCommerceRateRank(eLoopCommerce);*/
					/*if (bLimitedWonder && aiCommerceRank[eLoopCommerce] > 3 + iLimitedWonderLimit)
						|| (bCulturalVictory1 && eLoopCommerce == COMMERCE_CULTURE && aiCommerceRank[eLoopCommerce] == 1))
					{
						iTempValue *= -1;
						// for culture, just set it to zero, not negative, just about every wonder gives culture
						if (eLoopCommerce == COMMERCE_CULTURE)
						{
							iTempValue = 0;
						}
					}*/ // BtS
					/*	K-Mod, let us build culture wonders to defend
						against culture pressure. also, lets say top 1/3 instead.
						There are now other mechanisms to stop us from wasting buildings. */
					if (bLimitedWonder)
					{
						if (eLoopCommerce == COMMERCE_CULTURE)
						{
							if (bCulturalVictory1 &&
								((bCulturalVictory2 &&
								findCommerceRateRank(eLoopCommerce) == 1) ||
								findCommerceRateRank(eLoopCommerce) >
								iNumCities/3 + 1 + iLimitedWonderLimit))
							{
								iTempValue = 0;
							}
						}
						else if (findCommerceRateRank(eLoopCommerce) >
							iNumCities/3 + 1 + iLimitedWonderLimit)
						{
							iTempValue *= -1;
						}
					} // K-Mod end
					iValue += iTempValue;
				}
			}
			// corp evaluation moved here, and rewritten for K-Mod
			{
				CorporationTypes const eCorporation = kBuilding.getFoundsCorporation();
				int iCorpValue = 0;
				int iExpectedSpread = (kOwner.AI_atVictoryStage4() ? 45 :
						(70 - (bWarPlan ? 10 : 0))); // advc: parentheses added for clarity
				/*	note: expected spread starts as percent (for precision),
					but is later converted to # of cities. */
				if (kOwner.isNoCorporations())
					iExpectedSpread = 0;
				if (eCorporation != NO_CORPORATION && iExpectedSpread > 0)
				{
					//iCorpValue = kOwner.AI_corporationValue(eCorporation, this);
					// K-Mod: consider the corporation for the whole civ, not just this city.
					iCorpValue = kOwner.AI_corporationValue(eCorporation);
					FOR_EACH_ENUM(Corporation)
					{
						if (eLoopCorporation != eCorporation &&
							kOwner.hasHeadquarters(eLoopCorporation) &&
							GC.getGame().isCompetingCorporation(eCorporation, eLoopCorporation))
						{
							/*	This new corp is no good to us if our competing corp
								is already better. note: evaluation of the competing corp
								for this particular city is ok. */
							if (kOwner.AI_corporationValue(eLoopCorporation, this) > iCorpValue)
							{
								iExpectedSpread = 0;
								break;
							}
							// expect to spread the corp to fewer cities.
							iExpectedSpread /= 2;
						}
					}
					// convert spread from percent to # of cities
					iExpectedSpread = iExpectedSpread * iNumCities / 100;

					// scale corp value by the expected spread
					iCorpValue *= iExpectedSpread;
					/*	Rescale from 100x commerce down to 4x commerce.
						(AI_corporationValue returns roughly 100x commerce) */
					iCorpValue *= 4;
					iCorpValue /= 100;
				}
				if (kBuilding.getGlobalCorporationCommerce() != NO_CORPORATION)
				{
					iExpectedSpread += kGame.countCorporationLevels(
							kBuilding.getGlobalCorporationCommerce());
					if (iExpectedSpread > 0)
					{
						FOR_EACH_ENUM(Commerce)
						{
							int iHqValue = 4 * GC.getInfo(
									kBuilding.getGlobalCorporationCommerce()).
									getHeadquarterCommerce(eLoopCommerce) * iExpectedSpread;
							if (iHqValue != 0)
							{
								iHqValue *= getTotalCommerceRateModifier(eLoopCommerce);
								iHqValue *= kOwner.AI_commerceWeight(eLoopCommerce, this);
								iHqValue /= 10000;
							}
							/*	use rank as a tie-breaker...
								with number of national wonders thrown in to,
								(I'm trying to boost the chance that the
								AI will put wallstreet with its corp HQs.) */
							if (iHqValue > 0)
							{
								iHqValue *= 3*iNumCities
										- findCommerceRateRank(eLoopCommerce)
										- getNumNationalWonders() / 2;
								iHqValue /= 2*iNumCities;
							}
							iCorpValue += iHqValue;
						}
					}
				}
				if (iCorpValue > 0)
					iValue += iCorpValue;
			}
			// K-Mod end (corp)
            // rfc: disable
			/*FOR_EACH_NON_DEFAULT_PAIR(kBuilding.
				getReligionChange(), Religion, int)
			{
				ReligionTypes const eLoopReligion = perReligionVal.first;
				int iReligionChange = perReligionVal.second;
				if (iReligionChange > 0 &&
					GET_TEAM(getTeam()).hasHolyCity(eLoopReligion))
				{
					if (eStateReligion == eLoopReligion)
						iReligionChange *= 10;
					iValue += iReligionChange;
				}
			}*/
			if (kBuilding.getVoteSourceType() != NO_VOTESOURCE)
				iValue += 100;
		}
		else
		{
			if (iFocusFlags & BUILDINGFOCUS_GOLD)
			{
				int iTempValue = ((kBuilding.getCommerceModifier(COMMERCE_GOLD) *
						getBaseCommerceRate(COMMERCE_GOLD)) / 40);
				if (iTempValue != 0)
				{
					if (bFinancialTrouble)
						iTempValue *= 2;

					/*if (MAX_INT == aiCommerceRank[COMMERCE_GOLD])
						aiCommerceRank[COMMERCE_GOLD] = findCommerceRateRank(COMMERCE_GOLD);*/

					/*	if this is a limited wonder, and we are not one of the top 4 in
						this category, subtract the value. we do _not_ want to build this here.
						(unless the value was small anyway) */
					if (bLimitedWonder &&
						findCommerceRateRank(COMMERCE_GOLD) > 3 + iLimitedWonderLimit)
					{
						iTempValue *= -1;
					}
					iValue += iTempValue;
				}

				iValue += (kBuilding.getCommerceChange(COMMERCE_GOLD) * 4);
				iValue += (kBuilding.getObsoleteSafeCommerceChange(COMMERCE_GOLD) * 4);
			}

			if (iFocusFlags & BUILDINGFOCUS_RESEARCH)
			{
				int iTempValue = ((kBuilding.getCommerceModifier(COMMERCE_RESEARCH) *
						getBaseCommerceRate(COMMERCE_RESEARCH)) / 40);
				if (iTempValue != 0)
				{
					/*if (MAX_INT == aiCommerceRank[COMMERCE_RESEARCH])
						aiCommerceRank[COMMERCE_RESEARCH] = findCommerceRateRank(COMMERCE_RESEARCH);*/

					// (see comment above)
					if (bLimitedWonder &&
						findCommerceRateRank(COMMERCE_RESEARCH) > 3 + iLimitedWonderLimit)
					{
						iTempValue *= -1;
					}
					iValue += iTempValue;
				}
				iValue += kBuilding.getCommerceChange(COMMERCE_RESEARCH) * 4;
				iValue += kBuilding.getObsoleteSafeCommerceChange(COMMERCE_RESEARCH) * 4;
			}

			if (iFocusFlags & BUILDINGFOCUS_CULTURE)
			{
				int iTempValue = (kBuilding.getCommerceChange(
						COMMERCE_CULTURE) * 3);
				iTempValue += (kBuilding.getObsoleteSafeCommerceChange(
						COMMERCE_CULTURE) * 3);
				if (kGame.isOption(GAMEOPTION_NO_ESPIONAGE))
				{
					iTempValue += kBuilding.getCommerceChange(
							COMMERCE_ESPIONAGE) * 3;
					iTempValue += kBuilding.getObsoleteSafeCommerceChange(
							COMMERCE_ESPIONAGE) * 3;
				}
				//if ((getCommerceRate(COMMERCE_CULTURE) == 0) && (AI_calculateTargetCulturePerTurn() == 1))
				if (iTempValue >= 3 && AI_needsCultureToWorkFullRadius())
					iTempValue += 7;
				// K-Mod, this stuff was moved from below
				iTempValue += ((kBuilding.getCommerceModifier(COMMERCE_CULTURE) *
						getBaseCommerceRate(COMMERCE_CULTURE)) / 15);
				if (kGame.isOption(GAMEOPTION_NO_ESPIONAGE))
				{
					iTempValue += ((kBuilding.getCommerceModifier(COMMERCE_ESPIONAGE) *
							getBaseCommerceRate(COMMERCE_ESPIONAGE)) / 15);
				} // K-Mod end
				if (iTempValue != 0)
				{
					/*if (MAX_INT == aiCommerceRank[COMMERCE_CULTURE])
						aiCommerceRank[COMMERCE_CULTURE] = findCommerceRateRank(COMMERCE_CULTURE);*/

					/*	if this is a limited wonder, and we are not one of the top 4
						in this category, do not count the culture value.
						we probably do not want to build this here (but we might). */
					/*if (bLimitedWonder && (findCommerceRateRank(COMMERCE_CULTURE) > (3 + iLimitedWonderLimit)))
						iTempValue  = 0;*/ // BtS
					/*	K-Mod. The original code doesn't take prereq buildings into account,
						and it was in the wrong place. To be honest, I think this
						"building focus" flag system is pretty bad; but I'm fixing it anyway. */
					if (findCommerceRateRank(COMMERCE_CULTURE) > iCulturalVictoryNumCultureCities)
					{
						bool bAvoid = false;
						if (bLimitedWonder &&
							findCommerceRateRank(COMMERCE_CULTURE)
							- iLimitedWonderLimit >= iCulturalVictoryNumCultureCities)
						{
							bAvoid = true;
						}
						for (int iJ = 0; !bAvoid && iJ < GC.getNumBuildingClassInfos(); iJ++)
						{
							int iPrereqBuildings = kOwner.getBuildingClassPrereqBuilding(
									eBuilding, (BuildingClassTypes)iJ,
									iCulturalVictoryNumCultureCities
									- kOwner.getBuildingClassCount(eBuildingClass));
							if (kOwner.getBuildingClassCount((BuildingClassTypes)iJ) <
								iPrereqBuildings)
							{
								bAvoid = true;
							}
						}
						if (bAvoid)
							iTempValue = 0;
					}
					// K-Mod end
					iValue += iTempValue;
				}

				/*iValue += ((kBuilding.getCommerceModifier(COMMERCE_CULTURE) * getBaseCommerceRate(COMMERCE_CULTURE)) / 15);
				if (kGame.isOption(GAMEOPTION_NO_ESPIONAGE))
					iValue += ((kBuilding.getCommerceModifier(COMMERCE_ESPIONAGE) * getBaseCommerceRate(COMMERCE_ESPIONAGE)) / 15);*/ // BtS
				// (K-Mod has moved this stuff up to be before the limited wonder checks.)
			}

			if (iFocusFlags & BUILDINGFOCUS_BIGCULTURE)
			{
				int iTempValue = kBuilding.getCommerceModifier(COMMERCE_CULTURE) / 5;
				if (iTempValue != 0)
				{
					/*if (MAX_INT == aiCommerceRank[COMMERCE_CULTURE])
						aiCommerceRank[COMMERCE_CULTURE] = findCommerceRateRank(COMMERCE_CULTURE);*/

					// (see comment above)
					if (bLimitedWonder &&
						findCommerceRateRank(COMMERCE_CULTURE) >
						3 + iLimitedWonderLimit)
					{
						iTempValue  = 0;
					}

					iValue += iTempValue;
				}
			}
			//if (iFocusFlags & BUILDINGFOCUS_ESPIONAGE || (g.isOption(GAMEOPTION_NO_ESPIONAGE) && (iFocusFlags & BUILDINGFOCUS_CULTURE)))
			/*	K-Mod: the "no espionage" stuff is already taken into account
				in the culture section. */
			if (iFocusFlags & BUILDINGFOCUS_ESPIONAGE &&
				!kGame.isOption(GAMEOPTION_NO_ESPIONAGE))
			{	// BETTER_BTS_AI_MOD, City AI, 01/09/10, jdog5000: START
				// K-Mod, changed this section.
				int iTempValue = ((kBuilding.getCommerceModifier(COMMERCE_ESPIONAGE) *
						getBaseCommerceRate(COMMERCE_ESPIONAGE)) / 50);
				if (iTempValue != 0)
				{
					/*	if this is a limited wonder, and we are not one of the top 4
						in this category, subtract the value.
						we do _not_ want to build this here (unless the value was small anyway). */
					if (bLimitedWonder &&
						findCommerceRateRank(COMMERCE_ESPIONAGE) > 3 + iLimitedWonderLimit)
					{
						iTempValue *= -1;
					}

					iValue += iTempValue;
				}
				iTempValue = kBuilding.getCommerceChange(COMMERCE_ESPIONAGE) * 4;
				iTempValue += kBuilding.getObsoleteSafeCommerceChange(COMMERCE_ESPIONAGE) * 4;
				iTempValue *= 100 + getTotalCommerceRateModifier(COMMERCE_ESPIONAGE) +
						kBuilding.getCommerceModifier(COMMERCE_ESPIONAGE);
				iValue += iTempValue / 100;
				// BETTER_BTS_AI_MOD: END
			}
		}

		/*if ((iThreshold > 0) && (iPass == 0))
		{
			if (iValue < iThreshold)
				iValue = 0;
		}*/ // BtS
		// K-Mod
		if (!bNeutralFlags && iValue <= iThreshold)
		{
			iValue = 0;
			break;
		} // K-Mod end
	}
	iValue = std::max(0, iValue);
	// K-Mod
	if (iValue > 0)
	{
		// priority factor
		if (kBuilding.isWorldWonder())
		{
			/*	this could be adjusted based on iWonderConstructRand,
				or on rival's tech, or whatever... */
			iPriorityFactor += 20;
		}
		if (kBuilding.getProductionCost() > 0)
		{
			iValue *= iPriorityFactor;
			iValue /= 100;
		}

		// flavour factor. (original flavour code deleted)
		if (!isHuman())
		{
			iValue += kBuilding.getAIWeight();
			if (iValue > 0 &&
				// K-Mod. Only use flavour adjustments for constructing ordinary buildings.
				kBuilding.getProductionCost() > 0 && !bRemove)
			{
				int iFlavour = 0;
				FOR_EACH_NON_DEFAULT_PAIR(kBuilding.
					getFlavorValue(), Flavor, int)
				{
					//iValue += (kOwner.AI_getFlavorValue(eLoopFlavor) * kBuilding.getFlavorValue(eLoopFlavor));
					// <K-Mod>
					iFlavour += std::min(kOwner.AI_getFlavorValue(perFlavorVal.first),
							perFlavorVal.second); // </K-Mod>
				}
				// K-Mod. (This will give +100% for 10-10 flavour matchups.)
				//iValue = iValue * (10 + iFlavour) / 10;
				iValue = iValue * (8 + iFlavour) / 12; // advc.020
			}
		}
	} // <advc.131>
	if (iValue > 0 &&
		kBuilding.isNationalWonder() && isCapital() &&
		kOwner.AI_getCurrEraFactor() < fixp(3.5) &&
		iTotalImprFreeSpecialists <= 0 &&
		iTotalBonusYieldMod < 40 &&
		kBuilding.getGreatGeneralRateModifier() < 40 &&
		kBuilding.getMilitaryProductionModifier() < 40 &&
		kBuilding.getFreeExperience() < 4)
	{
		int iTotalCommerceMod = 0;
		FOR_EACH_ENUM(Commerce)
			iTotalCommerceMod += kBuilding.getCommerceModifier(eLoopCommerce);
		if (iTotalCommerceMod < 40)
		{
			int iSlotsLeft = getNumNationalWondersLeft();
			// Special treatment for Moai
			if (iSlotsLeft == 2 && bAnySeaPlotYieldChange)
				iSlotsLeft--;
			scaled rSlotMod = scaled::min(1, scaled(iSlotsLeft + 1, 4));
			iValue = (iValue * rSlotMod).uround();
			FAssert(iSlotsLeft >= 0);
			/*  0 is also bad, but can happen if canConstruct was only checked
				with bTestVisible=true. */
			if (iSlotsLeft == 0)
				iValue = 0;
		}
	} // </advc.131>
	// constructionValue cache
	if (bUseConstructionValueCache && !bConstCache)
		m_aiConstructionValue[eBuildingClass] = iValue;
    // K-Mod end

    // doc: AI building value weights
    int iBuildingClassPreference = GET_PLAYER(getOwner()).getBuildingClassPreference(eBuildingClass);
    if (iBuildingClassPreference != -MAX_INT)
    {
        if (iBuildingClassPreference == 0)
        {
            return -MAX_INT;
        }
        else if (iBuildingClassPreference > 0)
        {
            iValue *= iBuildingClassPreference;
            iValue /= 10;
        }
        else if (iBuildingClassPreference < 0)
        {
            iValue *= 10;
            iValue /= iBuildingClassPreference;
        }
    }

	return iValue;
}

/*  advc: Cut from AI_buildingValue.
	bRemove means that eBuilding needs to be evaluated under the assumption
	that eBuilding isn't already present. So it should generally be a
	positive value; see also the comment above AI_buildingValue. */
int CvCityAI::AI_defensiveBuildingValue(BuildingTypes eBuilding,
	bool bAreaAlone, bool bWarPlan, int iNumCities, int iNumCitiesInArea,
	bool bRemove, bool bObsolete) const
{
	int r = 0;
	CvBuildingInfo const& kBuilding = GC.getInfo(eBuilding);
	if (!bAreaAlone && (GC.getGame().getBestLandUnit() == NO_UNIT ||
		!GC.getInfo(GC.getGame().getBestLandUnit()).isIgnoreBuildingDefense()))
	{
		int const iBombardMod = kBuilding.getBombardDefenseModifier();
		int const iDefMod = kBuilding.getDefenseModifier();
		// <advc.004c>
		int const iDefRaise = kBuilding.get(CvBuildingInfo::RaiseDefense);
		if (iDefMod != 0 || iBombardMod != 0 || iDefRaise > 0)
		{
			int const iOwnerDefMod = GET_PLAYER(getOwner()).getCityDefenseModifier();
			/*  Defense abilities don't go obsolete. Looks like K-Mod had gotten that wrong.
				Tagging advc.001 (bugfix). */
			bool bRemoveDef = (bRemove && !bObsolete);
			if (bRemoveDef)
			{
				// Spy attack; don't know by whom. They don't know our preparations.
				bWarPlan = (GET_TEAM(getTeam()).getNumWars() > 0);
			} // </advc.004c>
			// defence bonus
			/*r += std::max(0, std::min(kBuilding.getDefenseModifier(),
					(bRemoveDef ? 0 : kBuilding.getDefenseModifier()) +
					getBuildingDefense() - getNaturalDefense() - 10)) / 4;*/
			/*  <advc.004c> Don't quite see the logic behind the above. Might be pretty
				good but idk how to extend it. */
			int iOldDefenseModifier = getTotalDefense(false);
			int iNewDefenseModifier = iOldDefenseModifier;
			if (bRemoveDef)
			{
				if (iDefMod != 0)
				{
					iNewDefenseModifier = std::max(getNaturalDefense(),
							iNewDefenseModifier - iDefMod) + iOwnerDefMod;
				}
				if (iDefRaise > 0)
				{
					// Don't bother checking if there'll be other defensive buildings left
					iNewDefenseModifier = getNaturalDefense() + iOwnerDefMod;
				}
				std::swap(iOldDefenseModifier, iNewDefenseModifier);
			}
			else
			{
				iNewDefenseModifier = std::max(iDefRaise, std::max(getNaturalDefense(),
						iNewDefenseModifier + iDefMod + iOwnerDefMod));
			}
			r += (iNewDefenseModifier - iOldDefenseModifier) / 4;
			if (iBombardMod != 0) // </advc.004c>
			{
				// bombard reduction
				int iOldBombardMod = getBuildingBombardDefense() - (bRemoveDef ? iBombardMod : 0);
				r += /*std::max(getNaturalDefense(),
						(bRemove ? 0 : iDefMod) + getBuildingDefense())*/
						iNewDefenseModifier * // advc.004c
						std::min(iBombardMod, 100 - iOldBombardMod) /
						std::max(80, 8 * (100 - iOldBombardMod));
			}
			r *= (bWarPlan ? 3 : 2);
			r /= 3;
		}
	}
	// K-Mod. I've merged and modified the code from here and the code
	// from higher up. [advc: i.e. from above the call location in AI_buildingValue]
	r += kBuilding.getAllCityDefenseModifier() * iNumCities / (bWarPlan ? 4 : 5);
	r += kBuilding.getAirlift() * 10 + (iNumCitiesInArea < iNumCities &&
			kBuilding.getAirlift() > 0 ? getPopulation() + 25 : 0);
	int iAirDefense = -kBuilding.getAirModifier();
	if (iAirDefense > 0)
	{
		int iTemp = iAirDefense;
		iTemp *= std::min(200, 100 * GET_TEAM(getTeam()).AI_getRivalAirPower() /
				std::max(1, GET_TEAM(getTeam()).AI_getAirPower() + 4 * iNumCities));
		iTemp /= 200;
		r += iTemp;
	}
	//r += -kBuilding.getNukeModifier() / (g.isNukesValid() && !g.isNoNukes() ? 4 : 40);
	// K-Mod end
	// <kekm.16> Replacing the line above.
	// DarkLunaPhantom - "Bomb Shelters should be of much higher value, I copied and adjusted rough estimates from AI_projectValue()."
	int iNukeDefense = -kBuilding.getNukeModifier();
	if (iNukeDefense > 0)
	{
		int iNukeEvasionProbability = 0;
		int iNukeUnitTypes = 0;
		FOR_EACH_ENUM(Unit)
		{
			CvUnitInfo const& kLoopUnit = GC.getInfo(eLoopUnit);
			if (kLoopUnit.isNuke() &&
				kLoopUnit.getProductionCost() > 0) // advc
			{
				iNukeEvasionProbability += kLoopUnit.getEvasionProbability();
				iNukeUnitTypes++;
			}
		}
		iNukeEvasionProbability /= std::max(1, iNukeUnitTypes);
		int iTargetValue = AI_nukeEplosionValue();
		/*  "Lazy attempt to estimate the value of the strongest
			unit stack this shelter might defend." */
		int iStackValue = 0;
		for (MemberIter itMember(getTeam()); itMember.hasNext(); ++itMember)
		{
				iStackValue += getArea().getPower(itMember->getID());
		}
		iStackValue *= 7;
		iStackValue /= 20;
		int iTempValue = iNukeDefense * (iStackValue + iTargetValue);
		iTempValue /= 100;
		iTempValue *= 10000 - GET_TEAM(getTeam()).getNukeInterception() *
				(100 - iNukeEvasionProbability);
		iTempValue /= 10000;
		iTempValue /= GET_PLAYER(getOwner()).AI_nukeDangerDivisor();
		r += iTempValue;
	} // </kekm.16>
	return r;
}

// This function has been significantly modified for K-Mod
ProjectTypes CvCityAI::AI_bestProject(int* piBestValue, /* advc.001n: */ bool bAsync) /* advc: */ const
{
	// <advc.014>
	if(GET_TEAM(getOwner()).isCapitulated())
		return NO_PROJECT;
	// </advc.014>
	int iProductionRank = findYieldRateRank(YIELD_PRODUCTION);
	ProjectTypes eBestProject = NO_PROJECT;
	int iBestValue = 0;
	FOR_EACH_ENUM2(Project, eProject)
	{
		if (!canCreate(eProject))
			continue; // can't build it. skip to the next project.
		CvProjectInfo const& kProject = GC.getInfo(eProject);

		int iTurnsLeft = getProductionTurnsLeft(eProject, 0);
		// <advc.004x>
		if(iTurnsLeft == MAX_INT)
			continue; // </advc.004x>
		int iRelativeTurns = (100 * iTurnsLeft + 50) /
				GC.getInfo(GC.getGame().getGameSpeedType()).getCreatePercent();
		if (iRelativeTurns > 10 && kProject.getMaxTeamInstances() > 0 &&
			GET_TEAM(getTeam()).isHuman())
		{
			// not fast enough to risk blocking our human allies from building it.
			continue;
		}
		if (iRelativeTurns > 20 &&
			iProductionRank > std::max(3, GET_PLAYER(getOwner()).getNumCities() / 2))
		{
			// not fast enough to risk blocking our more productive cities from building it.
			continue;
		}
		// otherwise, the project is something we can consider building!

		int iValue = AI_projectValue(eProject);

		/*	give a small chance of building global projects
			regardless of strategy, just for a bit of variety. */
		if (kProject.getEveryoneSpecialUnit() != NO_SPECIALUNIT ||
			kProject.getEveryoneSpecialBuilding() != NO_SPECIALBUILDING ||
			kProject.isAllowsNukes())
		{	// <advc.001n>
			if ((bAsync ?
				GC.getASyncRand().get(100, "Project Everyone ASYNC") : // </advc.001n>
				SyncRandNum(100)) == 0)
			{
				iValue++;
			}
		}
		if (iValue <= 0)
			continue; // the project is worthless. Skip it.

		bool bVictory = false;
		bool bGoodFit = false;

		if (GET_PLAYER(getOwner()).AI_atVictoryStage(AI_VICTORY_SPACE3))
		{
			FOR_EACH_ENUM2(Victory, eProjVictory)
			{
				if (!GC.getGame().isVictoryValid(eProjVictory) ||
					kProject.getVictoryThreshold(eProjVictory) <= 0)
				{
					continue;
				}
				bVictory = true;
				/*	count the total number of projects we still require
					for this type of victory. */
				int iNeededPieces = 0;
				FOR_EACH_ENUM2(Project, eAnyProject)
				{
					iNeededPieces += std::max(0,
							GC.getInfo(eAnyProject).getVictoryThreshold(eProjVictory)
							- GET_TEAM(getTeam()).getProjectCount(eAnyProject));
				}
				if (GET_TEAM(getTeam()).getProjectCount(eProject) <
					kProject.getVictoryThreshold(eProjVictory))
				{
					// we need more of this project. ie. it is a high priority.
					FAssert(iNeededPieces > 0);
					bGoodFit = bGoodFit || iProductionRank <= iNeededPieces;
				}
				else
				{
					/*	build this with high priority, but save our best cities
						for the projects that we still need. */
					bGoodFit = bGoodFit || iProductionRank > iNeededPieces;
				}
			}
		}
		if (!bVictory)
		{
			// work out how many of this project we can still build
			int iLimit = -1;
			if (kProject.getMaxGlobalInstances() >= 0) // global limit
			{
				int iRemaining = std::max(0, kProject.getMaxGlobalInstances()
						- GC.getGame().getProjectCreatedCount(eProject)
						- GET_TEAM(getTeam()).getProjectMaking(eProject));
				if (iLimit < 0 || iRemaining < iLimit)
					iLimit = iRemaining;
			}
			if (kProject.getMaxTeamInstances() >= 0) // team limit
			{
				int iRemaining = std::max(0, kProject.getMaxTeamInstances()
						- GET_TEAM(getTeam()).getProjectCount(eProject)
						- GET_TEAM(getTeam()).getProjectMaking(eProject));
				if (iLimit < 0 || iRemaining < iLimit)
					iLimit = iRemaining;
			}
			bGoodFit = iProductionRank <= iLimit;
		}
		if (bGoodFit)
		{
			// building the project in this city is probably a good idea.
			iValue += getProjectProduction(eProject);
			if (bVictory)
				iValue += getProductionNeeded(eProject) / 4 + iValue / 2;
		}
		else
		{
			if (bVictory)
			{
				iValue *= 3;
				iValue /= iRelativeTurns + 3;
			}
			else
			{
				iValue *= 5;
				iValue /= iRelativeTurns + 5;
			}
		}
		if (iValue > iBestValue)
		{
			iBestValue = iValue;
			eBestProject = eProject;
		}
	}
	if (piBestValue) // note: piBestValue is set even if there is no best project.
		*piBestValue = iBestValue;
	return eBestProject;
}

/*	This function has been completely rewritten for K-Mod.
	The return value is roughly in units of 4 * commerce per turn,
	to match AI_buildingValue. However, note that most projects don't actually
	give commerce per turn - so the evaluation is quite rough. */
int CvCityAI::AI_projectValue(ProjectTypes eProject) /* advc: */ const
{
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());
	CvTeamAI const& kTeam = GET_TEAM(kOwner.getTeam());
	CvProjectInfo const& kProject = GC.getInfo(eProject);

    int iSatelliteCount = 0;
    FOR_EACH_CITY(pLoopCity; GET_PLAYER(getOwner()))
    {
        iSatelliteCount = pLoopCity->countSatellites();
    }

	int iValue = 0;

	if (kProject.getTechShare() > 0)
	{
		if (kProject.getTechShare() < //kTeam.getHasMetCivCount(/*bIgnoreMinors=*/true)
			// kekm.38: (Minors can spread tech - but are unlikely to have good tech)
			PlayerIter<MAJOR_CIV,OTHER_KNOWN_TO>::count(kTeam.getID()) &&
			!kOwner.AI_avoidScience())
		{
			//iValue += 20 / kProject.getTechShare(); // BtS (this was all)
			TechTypes eSampleTech = kOwner.getCurrentResearch();
			if (eSampleTech == NO_TECH)
			{	// advc (comment): Use costliest tech that we have
				int iMaxCost = 0;
				FOR_EACH_ENUM(Tech)
				{
					if (!kTeam.isHasTech(eLoopTech))
						continue;
					int iLoopCost = GC.getInfo(eLoopTech).getResearchCost();
					if (iLoopCost > iMaxCost)
					{
						eSampleTech = eLoopTech;
						iMaxCost = iLoopCost;
					}
				}
			}
			if (eSampleTech != NO_TECH)
			{
				int iRelativeTechScore = kTeam.getBestKnownTechScorePercent();
				int iTechValue = 50 * kTeam.getResearchCost(eSampleTech) /
						std::max(1, iRelativeTechScore);
				// again, for emphasis.
				iTechValue = 100 * iTechValue / std::max(1, iRelativeTechScore);
				iTechValue *= (2 * GC.getNumEraInfos() - kOwner.getCurrentEra());
				iTechValue /= std::max(1,
						2 * GC.getNumEraInfos() - GC.getGame().getStartEra());
				iValue += iTechValue;
			}
			else FAssert(eSampleTech != NO_TECH);
		}
	}

	// SDI
	if (kProject.getNukeInterception() > 0)
	{
		//iValue += (GC.getInfo(eProject).getNukeInterception() / 10);
		int iForeignNukes = 0;
		PlayerIter<CIV_ALIVE,KNOWN_POTENTIAL_ENEMY_OF> itRival(getTeam());
		for (; itRival.hasNext(); ++itRival)
		{	// advc.650:
			if (!GET_TEAM(itRival->getTeam()).AI_isAvoidWar(getTeam()))
				iForeignNukes += kOwner.AI_estimateNukeCount(itRival->getID());
		}
		// advc.650: Was misleadingly named "iTeamsMet". Now only counts dangerous players.
		int const iMet = itRival.nextIndex();
		if (!GC.getGame().isNoNukes() || iForeignNukes > iMet)
		{
			int iTargetValue = AI_nukeEplosionValue();
			int iEstimatedNukeAttacks = (iForeignNukes * (2 + iMet)) / (2 + 2 * iMet) +
					(GC.getGame().isNoNukes() ? 0 :
					2 + GC.getGame().getNukesExploded() / (2 + iMet));
			iValue += kProject.getNukeInterception() * iEstimatedNukeAttacks *
					iTargetValue / 100;
		}
	}
	// Manhattan project
	if (kProject.isAllowsNukes() && !GC.getGame().isNoNukes())
	{
		/*	evaluating this is difficult, because it enables the nukes for enemies.
			In general, I want the AI to lean in favour of -not- building the
			Manhattan project, so that the human players generally get to decide
			whether or not the game will have nukes.
			But I do want the AI to build it if it will be particular adventageous
			for them. eg. when they want a conquest victory, and they know
			that their enemies don't have uranium... */
		//if (kOwner.AI_isDoStrategy(AI_STRATEGY_CRUSH | AI_STRATEGY_DAGGER) || kOwner.AI_atVictoryStage(AI_VICTORY_CONQUEST4))
		// <advc.650>
		CvGame const& kGame = GC.getGame();
		TeamTypes eWinningTeam = NO_TEAM;
		/*	This loop overlaps with KingMaking::addWinning, which, however,
			is difficult to separate from the UWAI component. */
		int iBestScore = 0;
		int iOurScore = 0;
		for (TeamAIIter<FREE_MAJOR_CIV,KNOWN_TO> itTeam(kTeam.getID());
			itTeam.hasNext(); ++itTeam)
		{
			int iScore = kGame.getTeamScore(itTeam->getID());
			if (itTeam->AI_anyMemberAtVictoryStage3())
			{
				iScore *= 140;
				iScore /= 100;
				if (itTeam->AI_anyMemberAtVictoryStage4())
				{
					iScore *= 155;
					iScore /= 100;
				}
			}
			if (iScore > iBestScore)
			{
				iBestScore = iScore;
				eWinningTeam = itTeam->getID();
			}
			if (&*itTeam == &kTeam)
				iOurScore = iScore;
		}
		if (!kTeam.AI_anyMemberAtVictoryStage4() &&
			kTeam.getID() != eWinningTeam && eWinningTeam != NO_TEAM &&
			// If it's close, then focus on our own victory strategy.
			100 * iOurScore < 95 * iBestScore &&
			// Willing to thwart victory through nuclear war?
			(((4 * iOurScore > 3 * iBestScore ||
			10 * kTeam.getPower(true) > 7 * GET_TEAM(eWinningTeam).getPower(false)) &&
			kTeam.AI_noWarAttitudeProb((AttitudeTypes)std::min(NUM_ATTITUDE_TYPES - 1,
			kTeam.AI_getAttitude(eWinningTeam) + 1)) < 100) ||
			/*	Need defensive nukes? (When already losing a war,
				then getting nukes will take too long.) */
			kTeam.AI_countMembersWithStrategy(AI_STRATEGY_ALERT1) > 0 ||
			(GET_TEAM(eWinningTeam).AI_anyMemberAtVictoryStage(AI_VICTORY_MILITARY3) &&
			GET_TEAM(eWinningTeam).AI_getAttitude(kTeam.getID()) <
			(GET_TEAM(eWinningTeam).AI_anyMemberAtVictoryStage(AI_VICTORY_MILITARY4) ?
			ATTITUDE_PLEASED : ATTITUDE_CAUTIOUS))))
			// </advc.650>
		{
			int iNukeValue = 0;
			int const iCivsAlive = PlayerIter<CIV_ALIVE>::count(); // advc.650
			FOR_EACH_ENUM(Unit)
			{
				CvUnitInfo const& kLoopUnit = GC.getInfo(eLoopUnit);
				if (!kLoopUnit.isNuke() || kLoopUnit.getProductionCost() < 0)
					continue; // either not a unit, or not normally buildable
				for (PlayerAIIter<CIV_ALIVE,KNOWN_TO> itLoopPlayer(kTeam.getID());
					itLoopPlayer.hasNext(); ++itLoopPlayer)
				{
					CvPlayerAI const& kLoopPlayer = *itLoopPlayer;
					CvTeamAI const& kLoopTeam = GET_TEAM(kLoopPlayer.getTeam());
					if (!kLoopTeam.isCapitulated() && // advc.130v
						// advc.650: These have too much to lose from nukes
						!kLoopTeam.AI_anyMemberAtVictoryStage4() &&
						kLoopPlayer.getCivilization().getUnit(
						kLoopUnit.getUnitClassType()) == eLoopUnit)
					{
						int iTemp=0; // advc
						if (kLoopPlayer.getID() == kOwner.getID())
						{
							iTemp = GC.getInfo(kOwner.getPersonalityType()).
									/*	victory weight is between 0 and 100. (usually around 30).
										(advc, note: Just for flavor, don't check whether
										conquest is actually possible.) */
									getConquestVictoryWeight() / 2
									/*  advc.650: Was just 85. More civs =>
										more targets to choose from. */
									+ 70 + 2 * iCivsAlive;
						}
						else if (kLoopPlayer.getTeam() == kOwner.getTeam())
							iTemp = 90;
						else if (kTeam.AI_getWarPlan(kLoopPlayer.getTeam()) != NO_WARPLAN ||
							kLoopPlayer.isHuman()) // advc.650
						{
							iTemp = -100;
						}
						else
						{
							iTemp = std::max(-100,
									(kOwner.AI_getAttitudeWeight(kLoopPlayer.getID()) - 125) /
									3); // advc.650: was 2
						}
						// tech prereqs.  reduce the value for each missing prereq
						if (!kLoopTeam.isHasTech(kLoopUnit.getPrereqAndTech()))
						{
							iTemp /= 2;
							if (!kLoopPlayer.canResearch(kLoopUnit.getPrereqAndTech()))
								iTemp /= 3;
						}
						for (int k = 0; k < kLoopUnit.getNumPrereqAndTechs(); k++)
						{
							TechTypes const ePrereqTech = kLoopUnit.getPrereqAndTechs(k);
							if (!kLoopTeam.isHasTech(ePrereqTech))
							{
								iTemp /= 2;
								if (!kLoopPlayer.canResearch(ePrereqTech))
									iTemp /= 3;
							}
						}

						// resource prereq.
						BonusTypes ePrereqBonus = kLoopUnit.getPrereqAndBonus();
						if (ePrereqBonus != NO_BONUS && !kLoopPlayer.hasBonus(ePrereqBonus) &&
							!kLoopPlayer.AI_isAnyOwnedBonus(ePrereqBonus))
						{
							iTemp /= 5;
						}
						iTemp *= 3 * kLoopPlayer.getPower();
						iTemp /= std::max(1, 2 * kOwner.getPower() + kLoopPlayer.getPower());
						iNukeValue += iTemp;
					}
				}
			}
			if (iNukeValue > 0)
			{
				/*	ok. At this point, the scale of iNukeValue is roughly a percentage
					of the number of different nuke units which would be helpful to us...
					kind of. It's very likely to be to be less than 100. In a situation
					where nukes would be very helpful, I estimate that iNukeValue
					would currently be around 30.
					I'm just going to do a very rough job or rescaling it to be
					more like the other project values. But first, I want to make
					a few more situational adjustments to the value. */
				iNukeValue *= (2 + //kTeam.getAnyWarPlanCount(true));
						//(GET_PLAYER(getOwner()).AI_isFocusWar() ? 1 : 0) // advc.105
						/*	<advc.650> All other war plans need faster action or
							aren't serious enough */
						kTeam.AI_getNumWarPlans(WARPLAN_PREPARING_TOTAL) +
						kTeam.AI_countMembersWithStrategy(AI_STRATEGY_ALERT1));
						// </advc.650>
				iNukeValue /= 2;
				iNukeValue *= AI_nukeEplosionValue();
				iNukeValue /= 25;
				iValue += iNukeValue;
			}
		}
	}

	// Space victory
	/*	How am I meant to gauge the value of a direct step towards victory?
		It just doesn't conform to the usual metrics...
		this is going to be very arbitrary...
		-- and it will be based on the original BtS code! */
	int iSpaceValue = 0;

	// a project which enables other projects... i.e. the Apollo Program
	FOR_EACH_ENUM(Project)
	{
		iSpaceValue += 8 * std::max(0, // was *10
				GC.getInfo(eLoopProject).getProjectsNeeded(eProject)
				- GET_TEAM(getTeam()).getProjectCount(eProject));
	}
	if (kOwner.AI_atVictoryStage(AI_VICTORY_SPACE1))
	{
		// a boost to compound with the other boosts lower down.
		iSpaceValue = (3 * iSpaceValue) / 2;
	}
	/*	projects which are required components for victory.
		(ie. components of the spaceship) */
	FOR_EACH_NON_DEFAULT_PAIR(kProject.
		getVictoryThreshold(), Victory, int)
	{
		VictoryTypes const eLoopVictory = perVictoryVal.first;
		if (!GC.getGame().isVictoryValid(eLoopVictory))
			continue;
		/*iSpaceValue += 20;
		iSpaceValue += std::max(0, kProject.getVictoryThreshold(eLoopVictory) - GET_TEAM(getTeam()).getProjectCount(eProject)) * 20;*/
		iSpaceValue += 15;
		iSpaceValue += std::max(0,
				kProject.getVictoryMinThreshold(eLoopVictory)
				- GET_TEAM(getTeam()).getProjectCount(eProject)) *
				(kOwner.AI_atVictoryStage(AI_VICTORY_SPACE4) ? 60 : 30);
		iSpaceValue += kProject.getSuccessRate();
		iSpaceValue += kProject.getVictoryDelayPercent() /
				(4 * perVictoryVal.second);
	}

	if (kOwner.AI_atVictoryStage(AI_VICTORY_SPACE4))
		iSpaceValue *= 4;
	else if (kOwner.AI_atVictoryStage(AI_VICTORY_SPACE3))
		iSpaceValue *= 3;
	else if (kOwner.AI_atVictoryStage(AI_VICTORY_SPACE2))
		iSpaceValue *= 2;
	else if (!kOwner.AI_atVictoryStage(AI_VICTORY_SPACE1) && kOwner.AI_atVictoryStage4())
		iSpaceValue = (2 * iSpaceValue) / 3;

	if (getArea().getAreaAIType(kOwner.getTeam()) != AREAAI_NEUTRAL)
	{
		iSpaceValue = getArea().getAreaAIType(kOwner.getTeam()) == AREAAI_DEFENSIVE ?
				iSpaceValue/2 : 2*iSpaceValue/3;
	}
	// <advc.115> Check if we have remotely enough production capacity for SS parts
	if(iSpaceValue > 0 && kOwner.calculateTotalYield(YIELD_PRODUCTION) <
		GC.getInfo(GC.getGame().getGameSpeedType()).getCreatePercent())
	{
		iSpaceValue = 0;
	} // </advc.115>
	iValue += iSpaceValue;

	// doc: map reveal
	if (kProject.isRevealsMap())
	{
		iValue += 5;
	}

    // doc: satellite attack
	if (kProject.isSatelliteAttack())
	{
        FOR_EACH_ENUM(Project)
        {
            if (GC.getInfo(eLoopProject).isSatelliteAttack() || GC.getProjectInfo(eLoopProject).isSatelliteIntercept())
            {
                iValue += GC.getGame().getProjectCreatedCount(eLoopProject) * 5;
            }
        }
	}

    // doc: satellite intercept
	if (kProject.isSatelliteIntercept())
	{
		if (GC.getGame().canTrainNukes())
		{
			iValue += 10;
		}
	}

    // doc: first enemy anarchy
	if (kProject.isFirstEnemyAnarchy())
	{
		if (GC.getGameINLINE().getProjectCreatedCount(eProject) == 0)
		{
		    for (PlayerIter<MAJOR_CIV,CIV_ALIVE> it; it.hasNext(); ++it)
            {
                if (it->getID() != getOwner() && GET_TEAM(it->getTeam()).isProjectMaking(eProject))
                {
                    if (GET_PLAYER(getOwner()).AI_getAttitude(it->getID()) < ATTITUDE_PLEASED)
                    {
                        iValue += 10;
                    }
                }
            }
		}
	}

    // doc: first air experience
	if (kProject.getFirstAirExperience() != 0)
	{
		if (GC.getGame().getProjectCreatedCount(eProject) == 0)
		{
			iValue += (kProject.getFirstAirExperience() * GET_PLAYER(getOwner()).getNumCities() * (bWarPlan ? 8 : 5) * iWarmongerPercent) / 500;
		}
	}

    // doc: air experience
	iValue += (kProject.getAirExperience() * GET_PLAYER(getOwnerINLINE()).getNumCities() * (bWarPlan ? 8 : 5) * iWarmongerPercent) / 500;

    // doc: special unit
	if (kProject.getSpecialUnit() != NO_SPECIALUNIT)
	{
        FOR_EACH_ENUM(Unit)
        {
            if (GC.getInfo(eLoopUnit).getSpecialUnitType() == kProject.getSpecialUnit())
            {
                iValue += GET_PLAYR(getOwner()).AI_getUnitEnabledValue(eLoopUnit) / 20;
            }
        }

		for (iI = 0; iI < GC.getNumUnitInfos(); iI++)
		{
			if (GC.getUnitInfo((UnitTypes)iI).getSpecialUnitType() == kProject.getSpecialUnit())
			{
				iValue += GET_PLAYER(getOwnerINLINE()).AI_getUnitEnabledValue((UnitTypes)iI) / 20;
			}
		}
	}

    // doc: golden age
	if (kProject.isGoldenAge())
	{
		iValue += 10;
	}

    // doc: free promotion
	if (kProject.getFreePromotion() != NO_PROMOTION)
	{
		iValue += 5;
	}

	// project is anywhere on the prereq chain for a victory project
	for (iI = 0; iI < GC.getNumVictoryInfos(); iI++)
	{
		for (int iJ = 0; iJ < GC.getNumProjectInfos(); iJ++)
		{
			if (GC.getProjectInfo((ProjectTypes)iJ).getVictoryThreshold(iI) > 0)
			{
				if (GC.getProjectInfo((ProjectTypes)iJ).getAnyoneProjectPrereq() == eProject)
				{
					iValue += 5;
				}

				ProjectTypes ePrereq = (ProjectTypes)iJ;
				while (true)
				{
					if (ePrereq == eProject && ePrereq != iJ)
					{
						iValue += 10;
						break;
					}

					for (int iK = 0; iK < GC.getNumProjectInfos(); iK++)
					{
						if (GC.getProjectInfo(ePrereq).getProjectsNeeded(iK) > 0)
						{
							ePrereq = (ProjectTypes)iK;
							continue;
						}
					}

					break;
				}
			}
		}
	}

    // doc: golden record
	if (eProject == PROJECT_GOLDEN_RECORD)
	{
		if (GET_PLAYER(getOwner()).AI_isDoStrategy(AI_STRATEGY_CULTURE2))
		{
			iValue += 5;
			iValue += iSatelliteCount / 5;
		}

		if (GET_PLAYER(getOwner()).AI_isDoStrategy(AI_STRATEGY_CULTURE4))
		{
			iValue += 10;
			iValue += iSatelliteCount / 2;
		}
	}

    // doc: the internet
	if (eProject == PROJECT_THE_INTERNET)
	{
		iValue += GET_PLAYER(getOwner()).AI_averageYieldMultiplier(YIELD_COMMERCE) * GET_PLAYER(getOwnerINLINE()).getTotalPopulation() / 15 / 1000;
	}

    // doc: human genome project
	if (eProject == PROJECT_HUMAN_GENOME_PROJECT)
	{
        FOR_EACH_ENUM(Improvement)
        {
            if (GC.getInfo(eLoopImprovement).getYieldChange(YIELD_COMMERCE) > 3)
            {
                iValue += GET_PLAYER(getOwner()).AI_averageYieldMultiplier(YIELD_FOOD) * GET_PLAYER(getOwner()).getImprovementCount(eLoopImprovement) / 1000;
            }
        }
	}

    // doc: international space station
	if (eProject == PROJECT_INTERNATIONAL_SPACE_STATION)
	{
		iValue += 5;
		iValue += GET_PLAYER(getOwner()).AI_averageCommerceMultiplier(COMMERCE_RESEARCH) * iSatelliteCount * 2 / 1000;
	}

    // doc: great firewall
	if (eProject == PROJECT_GREAT_FIREWALL)
	{
		iValue += 5;
		if (GET_PLAYER(getOwner()).AI_isDoStrategy(AI_STRATEGY_BIG_ESPIONAGE))
		{
			iValue += 5;
		}
	}

    // doc: lunar colony
	if (eProject == PROJECT_LUNAR_COLONY)
	{
		iValue += 5;
		iValue += GET_PLAYER(getOwner()).AI_averageYieldMultiplier(YIELD_PRODUCTION) * iSatelliteCount * 2 / 1000;
		iValue += GET_PLAYER(getOwner()).getNumCities() / 2;
	}

	return iValue;
}

/*	advc.650: K-Mod code cut from CvCityAI::AI_projectValue
	(used there repeatedly). K-Mod comments:
	"a very rough estimate of the cost of being nuked"
	"roughly in units of 4 * commerce per turn"
	It's also used for estimating the usefulness of nukes against
	enemy cities. Really shouldn't be a CvCityAI function because the
	city creating a nuke-related project isn't necessarily a
	typical city in terms of its economic output. Still, I'm leaving the
	logic as in K-Mod because this might provide a useful incentive for
	producing nuke-related projects in a high-yield city. These tend to be
	pretty important projects. */
int CvCityAI::AI_nukeEplosionValue() const
{
	return 10 +
		(getYieldRate(YIELD_PRODUCTION) * 5 +
		getYieldRate(YIELD_COMMERCE) * 3) / 2;
}

ProcessTypes CvCityAI::AI_bestProcess(CommerceTypes eCommerceType) const
{
	ProcessTypes eBestProcess = NO_PROCESS;
	int iBestValue = 0;
	FOR_EACH_ENUM(Process)
	{
		if (canMaintain(eLoopProcess))
		{
			int iValue = AI_processValue(eLoopProcess, eCommerceType);
			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				eBestProcess = eLoopProcess;
			}
		}
	}
	return eBestProcess;
}

/*	K-Mod. I've rearranged / rewritten most of this function.
	units of ~4x commerce */
int CvCityAI::AI_processValue(ProcessTypes eProcess, CommerceTypes eCommerceType) const
{
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());
	bool bValid = (eCommerceType == NO_COMMERCE);
	int iValue = 0;

	/* if (GC.getInfo(eProcess).getProductionToCommerceModifier(COMMERCE_GOLD) && GET_PLAYER(getOwner()).AI_isFinancialTrouble())
	{
		iValue += GC.getInfo(eProcess).getProductionToCommerceModifier(COMMERCE_GOLD);
	} */

	// pop borders
	if (getCultureLevel() <= 1)
		iValue += GC.getInfo(eProcess).getProductionToCommerceModifier(COMMERCE_CULTURE);

	int iAdjustFactor = 0;
	FOR_EACH_ENUM(Commerce)
	{
		iAdjustFactor += kOwner.getCommercePercent(eLoopCommerce) *
				kOwner.AI_averageCommerceMultiplier(eLoopCommerce);
	}
	iAdjustFactor /= 100;

	FOR_EACH_ENUM(Commerce)
	{
		int iTempValue = GC.getInfo(eProcess).
				getProductionToCommerceModifier(eLoopCommerce);
		if (iTempValue == 0)
			continue;
		if (eLoopCommerce == eCommerceType && iTempValue > 0)
		{
			bValid = true;
			iTempValue *= 2;
		}

		// K-Mod. Calculate the quantity of commerce produced.
		iTempValue *= getYieldRate(YIELD_PRODUCTION);
		//iTempValue /= 100; // keep this factor of 100 for now.
		/*	Culture is local, the other commerce types are non-local.
			We don't want the non-local commerceWeights in this function
			because maintaining a process is just a short-term arrangement. */
		iTempValue *= kOwner.AI_commerceWeight(eLoopCommerce,
				eLoopCommerce == COMMERCE_CULTURE ? this : 0);
		iTempValue /= 100;
		// K-Mod end

		/* iTempValue *= GET_PLAYER(getOwner()).AI_averageCommerceExchange(eLoopCommerce);
		iTempValue /= 60; */
		/*	K-Mod. Amplify the value of commerce processes with
			low average multipliers so that we can run higher percentages
			in commerce types with high average multipliers. */
		if (kOwner.isCommerceFlexible(eLoopCommerce) &&
			kOwner.getCommercePercent(eLoopCommerce) > 0)
		{
			/*iTempValue *= 100 + kOwner.getCommercePercent(eLoopCommerce) * (iAdjustFactor - 100) / 100;
			iTempValue /= std::max(100, 100 + kOwner.getCommercePercent(eLoopCommerce) *
					(kOwner.AI_averageCommerceMultiplier(eLoopCommerce) - 100) / 100);*/
			// (that wasn't a strong enough effect)
			iTempValue *= iAdjustFactor * std::max(100,
					200 - 2*kOwner.getCommercePercent(eLoopCommerce)) / 100;
			iTempValue /= std::max(100,
					kOwner.AI_averageCommerceMultiplier(eLoopCommerce) +
					iAdjustFactor * std::max(0,
					100 - kOwner.getCommercePercent(eLoopCommerce)) / 100);
		}
		// K-Mod end

		iValue += iTempValue;
	}

	// note, currently iValue has units of 100x commerce. We want to return 4x commerce.
	return (bValid ? iValue / 25 : 0);
}


int CvCityAI::AI_neededSeaWorkers() /* advc: */ const
{
	int iNeededSeaWorkers = 0;

	/*  <advc.305> Normally counted per area, but a Barbarian city should only
		train workers for its own needs.
		(Partially based on code in CvPlayer::AI_countUnimprovedBonuses.) */
	if(isBarbarian())
	{
		FOR_EACH_ADJ_PLOT(getPlot())
		{
			if(!pAdj->isWater())
				continue;
			BonusTypes eBonus = pAdj->getNonObsoleteBonusType(getTeam());
			if(eBonus != NO_BONUS && !GET_PLAYER(getOwner()).
				doesImprovementConnectBonus(pAdj->getImprovementType(), eBonus))
			{
				iNeededSeaWorkers++;
			}
		}
		return iNeededSeaWorkers;
	} // </advc.305>

	// BETTER_BTS_AI_MOD, Worker AI, 01/01/09, jdog5000: START
	CvArea* pWaterArea = waterArea(true);
	if (pWaterArea == NULL)
		return 0;
	iNeededSeaWorkers += GET_PLAYER(getOwner()).AI_countUnimprovedBonuses(*pWaterArea, plot(),
			5); // advc.042
	// Check if second water area city can reach was any unimproved bonuses
	pWaterArea = secondWaterArea();
	if (pWaterArea != NULL)
	{
		iNeededSeaWorkers += GET_PLAYER(getOwner()).AI_countUnimprovedBonuses(*pWaterArea, plot(),
				5); // advc.042
	}
	// BETTER_BTS_AI_MOD: END
	return iNeededSeaWorkers;
}

// advc.110: Replacing AI_isDefended
int CvCityAI::AI_countExcessDefenders() const
{
	PROFILE_FUNC();
	// XXX check for other team's units?
	return (getPlot().plotCount(PUF_canDefendGroupHead, -1, -1, getOwner(), NO_TEAM, PUF_isCityAIType) -
			AI_neededDefenders());
}

/*bool CvCityAI::AI_isAirDefended(int iExtra) {
	PROFILE_FUNC();
	return ((getPlot().plotCount(PUF_canAirDefend, -1, -1, getOwner(), NO_TEAM, PUF_isDomainType, DOMAIN_AIR) + iExtra) >= AI_neededAirDefenders()); // XXX check for other team's units?
}*/ // BtS
// BETTER_BTS_AI_MOD, Air AI, 10/17/08, jdog5000: START  (disabled by K-Mod)
// Function now answers question of whether city has enough ready air defense, no longer just counts fighters
/* bool CvCityAI::AI_isAirDefended(bool bCountLand, int iExtra) {
	PROFILE_FUNC();
	int iAirDefenders = iExtra;
	int iAirIntercept = 0;
	int iLandIntercept = 0;
	CvUnit* pLoopUnit;
	CLLNode<IDInfo>* pUnitNode = getPlot().headUnitNode();
	while (pUnitNode != NULL) {
		pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = getPlot().nextUnitNode(pUnitNode);
		if ((pLoopUnit->getOwner() == getOwner())) {
			if (pLoopUnit->canAirDefend()) {
				if (pLoopUnit->getDomainType() == DOMAIN_AIR) {
					// can find units which are already air patrolling using group activity
					if (pLoopUnit->getGroup()->getActivityType() == ACTIVITY_INTERCEPT)
						iAirIntercept += pLoopUnit->currInterceptionProbability();
					else {
						// Count air units which can air patrol
						if (pLoopUnit->getDamage() == 0 && !pLoopUnit->hasMoved()) {
							if (pLoopUnit->AI_getUnitAIType() == UNITAI_DEFENSE_AIR)
								iAirIntercept += pLoopUnit->currInterceptionProbability();
							else iAirIntercept += pLoopUnit->currInterceptionProbability()/3;
						}
					}
				}
				else if (pLoopUnit->getDomainType() == DOMAIN_LAND)
					iLandIntercept += pLoopUnit->currInterceptionProbability();
			}
		}
	}
	iAirDefenders += (iAirIntercept/100);
	if (bCountLand)
		iAirDefenders += (iLandIntercept/100);
	int iNeededAirDefenders = AI_neededAirDefenders();
	bool bHaveEnough = (iAirDefenders >= iNeededAirDefenders);
	return bHaveEnough;
}*/ // BETTER_BTS_AI_MOD: END

/*	K-Mod. I've reverted AI_isAirDefended back to its original simple functionality.
	I've done this because my new version of AI_neededAirDefenders is
	not suitable for use in the bbai version of AI_isAirDefended.
	I may put some more work into this stuff in the future
	if I ever work through CvUnitAI::AI_defenseAirMove.
	function signature changed to match bbai usage. */
bool CvCityAI::AI_isAirDefended(
	bool bCountLand, // advc (note): Either way, only aircraft are currently counted.
	int iExtra) /* advc: */ const
{
	PROFILE_FUNC();
	return (getPlot().plotCount(PUF_isAirIntercept, -1, -1, getOwner()) + iExtra >=
			AI_neededAirDefenders());
}

// BETTER_BTS_AI_MOD, War strategy AI, Barbarian AI, 04/25/10, jdog5000:
int CvCityAI::AI_neededDefenders(/* advc.139: */ bool bIgnoreEvac,
	bool bConstCache) const // advc.001n
{
	PROFILE_FUNC();

	bool const bOffenseWar = (getArea().getAreaAIType(getTeam()) == AREAAI_OFFENSIVE ||
			getArea().getAreaAIType(getTeam()) == AREAAI_MASSING);
	bool const bDefenseWar = (getArea().getAreaAIType(getTeam()) == AREAAI_DEFENSIVE);
	CvGameAI const& kGame = GC.AI_getGame();
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());
	int iDefenders = 1;
	if (isBarbarian())
	{
		iDefenders = GC.getInfo(kGame.getHandicapType()).getBarbarianInitialDefenders();
		// advc.300: Numerator was pop+2
		iDefenders += (getPopulation() + kOwner.getCurrentEra()) / 7;
		// <advc.300> Extra defenders when far behind in tech, especially early New World.
		int const iAreaCities = getArea().getCitiesPerPlayer(getOwner());
		iDefenders += std::max(0, kGame.AI_getCurrEra() - kOwner.AI_getCurrEra()
				- (iAreaCities > 1 && getArea().getNumCivCities() * 3 <= iAreaCities ?
				0 : 1)); // </advc.300>
		return iDefenders;
	} // advc.003n: Switched the order of these two branches
	if (!GET_TEAM(getTeam()).AI_isWarPossible())
		return iDefenders;

	if (hasActiveWorldWonder() || isCapital() || isHolyCity())
	{
		iDefenders++;
		if(kOwner.AI_isDoStrategy(AI_STRATEGY_ALERT1) ||
			kOwner.AI_isDoStrategy(AI_STRATEGY_TURTLE))
		{
			iDefenders++;
		}
	}
	/*  advc.300: When Barbarians are a big threat and civs aren't, free up units
		for fog-busting (CvUnitAI::AI_guardCitySite) and guarding food bonuses. */
	if (!kOwner.AI_isDefenseFocusOnBarbarians(getArea()))
	{
		/*if (!GET_PLAYER(getOwner()).AI_isDoStrategy(AI_STRATEGY_CRUSH))
			iDefenders += AI_neededFloatingDefenders();
		else iDefenders += (AI_neededFloatingDefenders() + 2) / 4;*/
		/*  <advc.139> Replacing the above. No functional change other than passing
			along bIgnoreEvac and (advc.001n) bConstCache */
		int iNeededFloating = AI_neededFloatingDefenders(bIgnoreEvac, bConstCache,
				true); // advc.099c: To save time (avoid calling AI_neededCultureDefenders 2x)
		if (kOwner.AI_isDoStrategy(AI_STRATEGY_CRUSH))
			iNeededFloating = intdiv::uround(iNeededFloating, 4);
		iDefenders += iNeededFloating;
		// </advc.139>
	}

	if (bDefenseWar || kOwner.AI_isDoStrategy(AI_STRATEGY_ALERT2))
	{
		if (!getPlot().isHills())
			iDefenders++;
	}

	if (kGame.getGameTurn() - getGameTurnAcquired() < 10)
	{	/*if (bOffenseWar) {
			if (!hasActiveWorldWonder() && !isHolyCity()) {
				iDefenders /= 2;
				iDefenders = std::max(1, iDefenders);
			}
		} if (kGame.getGameTurn() - getGameTurnAcquired() < 10) {
			iDefenders = std::max(2, iDefenders);
			if (AI_isDanger())
				iDefenders ++;
			if (bDefenseWar)
				iDefenders ++;
		}*/ // BtS
		iDefenders = std::max(2, iDefenders);

		if (bOffenseWar && getTotalDefense(true) > 0 &&
			!hasActiveWorldWonder() && !isHolyCity())
		{
			iDefenders /= 2;
		}
		if (!bConstCache && // advc.001n: Can lead to an update of the border danger cache
			AI_isDanger())
		{
			iDefenders++;
		}
		if (bDefenseWar)
			iDefenders++;
	}

	if (kOwner.AI_isDoStrategy(AI_STRATEGY_LAST_STAND))
		iDefenders += 5; // advc.107: From MNAI; was 10.

	if (kOwner.AI_atVictoryStage(AI_VICTORY_CULTURE3))
	{
		if (findCommerceRateRank(COMMERCE_CULTURE) <=
			kGame.culturalVictoryNumCultureCities())
		{
			iDefenders += 2; // advc.107: From MNAI; was 4 in BtS, 1 in MNAI.
			if (bDefenseWar /* cdtw: */ || isCoastal())
				iDefenders += 2;
		}
	}

	if(kOwner.AI_atVictoryStage(AI_VICTORY_SPACE3))
	{	// advc.107: Added bOffenseWar clause
		if((isCapital() || isProductionProject()) && !bOffenseWar)
		{
			iDefenders += 2; // advc.107: was +=4
			if(bDefenseWar)
				iDefenders += 3;
		}
		if(isCapital() && kOwner.AI_atVictoryStage(AI_VICTORY_SPACE4))
			iDefenders += 6;
	}

	/*	advc (note): Take into account finances? (Idea from MNAI, which
		halves iDefenders when in financial trouble - but seems excessive to me.) */

	iDefenders = std::max(iDefenders, AI_neededCultureDefenders()); // advc.099c
	iDefenders = std::max(iDefenders, AI_minDefenders());

	return iDefenders;
}


int CvCityAI::AI_minDefenders() const
{
	/*	advc: Could afford to check CvPlayerAI::AI_feelsSafe here and
		then not add the 3rd defender in coastal cities. But this function
		does get called somewhat frequently, so, maybe not worth it. */
	PROFILE_FUNC();
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());
	int iDefenders = 1;
	{
		//if (kOwner.getCurrentEra() > 0)
		/*	<advc.107> Chosen so that the extra defender comes in the Medieval era
			on Immortal and Deity and in Renaissance otherwise. That said,
			the training modifier decreases as the game progresses, so things get
			a little fuzzy (which is fine with me). */
		scaled rExtraDefenderEraFactor = fixp(2.5);
		scaled rTrainModifier = kOwner.trainingModifierFromHandicap() /
				kOwner.AI_trainUnitSpeedAdustment(); // advc.253
		if (rTrainModifier < 1)
			rExtraDefenderEraFactor *= SQR(rTrainModifier);
		if (kOwner.AI_getCurrEraFactor() > rExtraDefenderEraFactor)
		{	// </advc.107>
			iDefenders++;
		}
	}
	int const iEra = kOwner.getCurrentEra();
	if (//iEra - GC.getGame().getStartEra() / 2 >= GC.getNumEraInfos() / 2 &&
		// <advc.107>
		iEra > GC.getGame().getStartEra() &&
		iEra >= CvEraInfo::AI_getAgeOfExploration() &&
		getPopulation() > 2 + iEra && // </advc.107>
		// advc.107: Times 2 - a small water area doesn't justify an extra defender.
		isCoastal(2 * GC.getDefineINT(CvGlobals::MIN_WATER_SIZE_FOR_OCEAN)))
	{
		iDefenders++;
	}
	return iDefenders;
}


int CvCityAI::AI_neededFloatingDefenders(/* <advc.139> */ bool bIgnoreEvac,
	bool bConstCache, // advc.001n
	bool bIgnoreCulture) const // advc.099c
{
	if(!bIgnoreEvac && AI_isEvacuating())
		return 0; // </advc.139>
	int iR = m_iNeededFloatingDefenders;
	if(m_iNeededFloatingDefendersCacheTurn != GC.getGame().getGameTurn())
	{
		iR = AI_calculateNeededFloatingDefenders(bConstCache, // advc.001n
				bIgnoreCulture); // advc.099c
	}
	return iR;
}

int CvCityAI::AI_calculateNeededFloatingDefenders(bool bConstCache,
	bool bIgnoreCulture) const // advc.099c
{
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());

	int iFloatingDefenders = kOwner.AI_getTotalFloatingDefendersNeeded(getArea());
	iFloatingDefenders -= getArea().getCitiesPerPlayer(getOwner());
	// advc.107: (Can perhaps already be negative in BtS - on small islands)
	iFloatingDefenders = std::max(0, iFloatingDefenders);
	{
		int iLocalThreat = AI_cityThreat();
		int iTotalThreat = std::max(1, kOwner.AI_getTotalAreaCityThreat(getArea()));
		iFloatingDefenders = intdiv::uround(iFloatingDefenders * iLocalThreat, iTotalThreat);
	}
	// <advc.099c>
	if (!bIgnoreCulture)
	{
		int iCultureDefendersNeeded = AI_neededCultureDefenders() - AI_minDefenders();
		iFloatingDefenders = std::max(iFloatingDefenders, iCultureDefendersNeeded);
	} // </advc.099c>

	if (!bConstCache) // advc.001n
	{
		m_iNeededFloatingDefenders = iFloatingDefenders;
		m_iNeededFloatingDefendersCacheTurn = GC.getGame().getGameTurn();
	}
	return iFloatingDefenders; // advc.001n
}

// advc.099c:
int CvCityAI::AI_neededCultureDefenders() const
{
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());
	if (getPlot().calculateCulturePercent(kOwner.getID()) >= 50)
		return 0; // To save time
	PlayerTypes const eCulturalOwner = calculateCulturalOwner();
	if(eCulturalOwner == kOwner.getID() || revoltProbability(true, true) <= 0)
		return 0;

	int const iPop = getPopulation();
	bool const bWillFlip = canCultureFlip(eCulturalOwner);
	scaled rTargetProb = scaled::max(0, 50 - iPop) / 1000;
	if (bWillFlip)
		rTargetProb = 0;
	else if (getNumRevolts(eCulturalOwner) > 0)
		rTargetProb /= 4;
	int const iCultureStr = cultureStrength(eCulturalOwner,
			false, true); // advc.023
	// Based on the formula in CvCity::revoltProbability
	scaled rTargetGarrisonStr = iCultureStr - iCultureStr * rTargetProb /
			scaled::max(per100(1), getRevoltTestProbability());

	scaled const rAIEraFactor = kOwner.AI_getCurrEraFactor();
	scaled r = rTargetGarrisonStr / scaled::max(3,
			(rAIEraFactor + fixp(0.5)) * (rAIEraFactor < fixp(3.5) ? 3 : 4));
	if (r > scaled::max(iPop, 3 + rAIEraFactor))
		return 0; // Not worth it
	if (isOccupation())
		r++;
	else if (kOwner.AI_isFocusWar(area()) &&
		// Don't move out units until war is imminent
		!GET_TEAM(kOwner.getTeam()).AI_isSneakAttackPreparing())
	{
		if (!bWillFlip)
			r /= 2;
		else
		{
			int iWSRating = range(GET_TEAM(kOwner.getTeam()).
					AI_getWarSuccessRating(), -100, 100);
			r *= fixp(0.75) + scaled(iWSRating, 400);
		}
	}
	return r.round();
}

// This function has been completely rewritten for K-Mod. (The original code has been deleted.)
// My version is still very simplistic, but it has the advantage of being consistent with other AI calculations.
int CvCityAI::AI_neededAirDefenders(/* advc.001n: */ bool bConstCache) /* advc: */ const
{
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());

	if (!GET_TEAM(kOwner.getTeam()).AI_isWarPossible())
		return 0;

	const int iRange = 5;

	// Essentially I'm going to bootstrap off the hard work already done in AI_neededFloatingDefenders.
	// We'll just count the number of floating defenders needed in nearby cities; and use this to
	// calculate what proportion of our airforce we should deploy here.
	int iNearbyFloaters = 0;
	int iNearbyCities = 0;
	int iTotalFloaters = 0;

	// Note: checking the nearby plots directly to look for cities may scale better than this
	//		 on very large maps; but that would make it harder to work out iTotalFloaters.
	FOR_EACH_CITYAI(pLoopCity, kOwner)
	{
		int iFloaters = pLoopCity->AI_neededFloatingDefenders(
				false, bConstCache); // advc.001n
		iTotalFloaters += iFloaters;
		if (plotDistance(plot(), pLoopCity->plot()) <= iRange)
		{
			iNearbyCities++;
			iNearbyFloaters += iFloaters;
			// Note: floaters for this city really should be divided by the number of cities near
			// pLoopCity rather than thenumber near 'this'. But that would be a longer calculation.
		}
	}
	FAssert(iNearbyCities > 0);
	// 'iNearbyFloaters / iTotalFloaters' is the proportion of our air defenders we should use in this city.
	// ie. a proportion of the total air defenders for our civ we already have or expect to have.
	int iNeeded = (std::max(kOwner.AI_getTotalAirDefendersNeeded(),
			kOwner.AI_getNumAIUnits(UNITAI_DEFENSE_AIR)) * iNearbyFloaters +
			(iNearbyCities * iTotalFloaters)/2) /
			std::max(1, iNearbyCities * iTotalFloaters);
	return std::min(iNeeded, getAirUnitCapacity(kOwner.getTeam())); // Capped at the air capacity of the city.

	//Note: because of the air capacity cap, and rounding, and the shortcut used for the nearbyFloater averaging,
	// the sum of AI_neededAirDefenders for each city won't necessarily equal our intended total.
}

bool CvCityAI::AI_isDanger() /* advc: */ const
{
	// BETTER_BTS_AI_MOD, City AI, Efficiency, 08/20/09, jdog5000: was AI_getPlotDanger
	return GET_PLAYER(getOwner()).AI_isAnyPlotDanger(getPlot(), 2, false);
}

// <advc.139>
void CvCityAI::AI_updateSafety(bool bUpdatePerfectSafety)
{
	PROFILE_FUNC();
	m_eSafety = CITYSAFETY_SAFE;
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());
	if(kOwner.getNumCities() <= 1)
		return;
	/*  iRange = 1 b/c I want to be sure that an attack is imminent. Won't work
		against fast attackers, but usually dangerous attack stacks involve some
		slow units. More important not to declare cities lost that still
		have a realistic chance. */
	int iAttackers = 0;
	int iAttStrength = kOwner.AI_localAttackStrength(plot(), NO_TEAM,
			DOMAIN_LAND, 1, true, false, false, &iAttackers);
	bool bSafe = true;
	int iDefenders = -1;
	int iDefStrength = -1;
	if (iAttStrength > 0) // To save time
	{
		iDefStrength = kOwner.AI_localDefenceStrength(plot(), getTeam(),
				DOMAIN_LAND, 3, true, /*bCheckMoves=*/true,
				false, /*bPredictPromotions=*/true);
		/*  Could let AI_localDefenceStrength do the counting, but I don't want
			to rely on defenders that could possibly(!) be rallied too much. */
		iDefenders = getPlot().getNumDefenders(getOwner());
		// Check if we'll finish a defender at the end of our turn
		if (iDefenders > 0 && isProductionUnit() && getProductionTurnsLeft() == 1)
		{
			CvUnitInfo const& kProductionUnit = GC.getInfo(getProductionUnit());
			if (kProductionUnit.getCombat() > 0) // Assume an average defender
				iDefStrength = (iDefStrength * (iDefenders + 1)) / iDefenders;
		}
		bSafe = (iAttStrength * 2 < iDefStrength);
		// Potentially expensive
		if(bSafe && GET_TEAM(getTeam()).getNumWars(false, true) > 0)
		{
			int iAttStrengthWiderRange = kOwner.AI_localAttackStrength(
					plot(), NO_TEAM, DOMAIN_LAND, 3);
			bSafe = (iAttStrengthWiderRange * 2 < iDefStrength);
		}
	}
	if (bSafe)
	{	// <advc.ctr>
		if (bUpdatePerfectSafety &&
			!getPlot().isVisibleEnemyCityAttacker(kOwner.getID(), NO_TEAM, 2))
		{
			m_eSafety = CITYSAFETY_PERFECT; // </advc.ctr>
		}
		return;
	}
	FAssert(iDefenders >= 0 && iDefStrength >= 0);
	bool bEvac = false;
	// Only bail if they can take the city in one turn or almost
	if (iAttackers + 1 >= iDefenders)
	{
		static scaled const rAI_EVACUATION_THRESH = per100(
				GC.getDefineINT("AI_EVACUATION_THRESH"));
		scaled rThresh = rAI_EVACUATION_THRESH;
		//  Higher threshold for important cities
		scaled rRelativeCityVal = per100(AI_getCityValPercent());
		if (rRelativeCityVal > fixp(0.5))
			rThresh *= fixp(0.5) + rRelativeCityVal;
		if (kOwner.getNumCities() <= 2 && isCapital())
			rThresh *= 2;
		bEvac = (scaled(iAttStrength, iDefStrength + 1) > rThresh);
	}
	if (bEvac)
		m_eSafety = CITYSAFETY_EVACUATING;
	else m_eSafety = CITYSAFETY_THREATENED;
}


void CvCityAI::AI_setCityValPercent(int iValue)
{
	FAssert(iValue <= 101);
	m_iCityValPercent = iValue;
} // </advc.139>

// K-Mod (advc: Moved from CvCity)
int CvCityAI::AI_culturePressureFactor() const
{
	int iAnswer = 0;
	const int iDivisor = 60;

	for (CityPlotIter itPlot(*this); itPlot.hasNext(); ++itPlot)
	{
		CvPlot const& kPlot = *itPlot;
		if (!kPlot.isWithinCultureRange(getOwner()))
			continue;
		for (PlayerIter<CIV_ALIVE,NOT_SAME_TEAM_AS> it(getTeam()); it.hasNext(); ++it)
		{
			CvPlayer const& kPlayer = *it;
			int iForeignCulture = kPlot.getCulture(kPlayer.getID());
			// scale it by how it compares to our culture
			iForeignCulture = (100 * iForeignCulture) /
					std::max(1, iForeignCulture + kPlot.getCulture(getOwner()));
			iForeignCulture *= 2;
			iForeignCulture /= 2 +
					// lower the value if the foreign culture is not allowed take control of the plot
					((!kPlot.isWithinCultureRange(kPlayer.getID()) ||
					GET_TEAM(kPlayer.getTeam()).isVassal(getTeam())) ? 2 : 0) +
					// lower the value if the foreign culture is not allowed to flip the city
					(!canCultureFlip(kPlayer.getID()) ? 1 : 0);
			iAnswer += iForeignCulture * iForeignCulture;
		}
	}
	// dull the effects in the late-game.
	/*iAnswer *= GC.getNumEraInfos();
	iAnswer /= GET_PLAYER(getOwner()).getCurrentEra() + GC.getNumEraInfos();*/
	iAnswer *= GC.getGame().getEstimateEndTurn();
	iAnswer /= GC.getGame().getGameTurn() + GC.getGame().getEstimateEndTurn();
	// capped to avoid overly distorting the value of buildings and great people points.
	return std::min(500, 100 + iAnswer / iDivisor);
}


CvCityAI* CvCityAI::AI_getRouteToCity() const // advc.003u: return type was CvCity*
{
	return AI_getCity(m_routeToCity);
}


void CvCityAI::AI_updateRouteToCity()
{
	PROFILE_FUNC(); // advc.opt

	gDLL->getFAStarIFace()->ForceReset(&GC.getRouteFinder());

	int iBestValue = MAX_INT;
	CvCity const* pBestCity = NULL;

	for (MemberIter itMember(getTeam()); itMember.hasNext(); ++itMember)
	{
		FOR_EACH_CITY(pLoopCity, *itMember)
		{
			if(pLoopCity == this || !sameArea(*pLoopCity))
				continue;
			/*	advc (note): This calls CvPlayer::getBestRoute
				(via routeValid in CvGameCoreUtils.cpp) to determine whether
				railroads are available */
			if (!gDLL->getFAStarIFace()->GeneratePath(&GC.getRouteFinder(),
				getX(), getY(), pLoopCity->getX(),
				pLoopCity->getY(), false, getOwner(), true))
			{
				int iValue = plotDistance(getX(), getY(),
						pLoopCity->getX(), pLoopCity->getY());
				if (iValue < iBestValue)
				{
					iBestValue = iValue;
					pBestCity = pLoopCity;
				}
			}
		}
	}
	if(pBestCity != NULL)
		m_routeToCity = pBestCity->getIDInfo();
	else m_routeToCity.reset();
}


int CvCityAI::AI_getEmphasizeYieldCount(YieldTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiEmphasizeYieldCount[eIndex];
}


bool CvCityAI::AI_isEmphasizeYield(YieldTypes eIndex) const
{
	return (AI_getEmphasizeYieldCount(eIndex) > 0);
}


int CvCityAI::AI_getEmphasizeCommerceCount(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return (m_aiEmphasizeCommerceCount[eIndex] > 0);
}


bool CvCityAI::AI_isEmphasizeCommerce(CommerceTypes eIndex) const
{
	return (AI_getEmphasizeCommerceCount(eIndex) > 0);
}


bool CvCityAI::AI_isEmphasize(EmphasizeTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumEmphasizeInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	FAssertMsg(m_pbEmphasize != NULL, "m_pbEmphasize is not expected to be equal with NULL");
	return m_pbEmphasize[eIndex];
}


void CvCityAI::AI_setEmphasize(EmphasizeTypes eIndex, bool bNewValue)
{
	FAssert(eIndex >= 0);
	FAssert(eIndex < GC.getNumEmphasizeInfos());

	if (AI_isEmphasize(eIndex) == bNewValue)
		return;

	m_pbEmphasize[eIndex] = bNewValue;
	/*	advc.131d: Re-evaluate whether strong emphasis is appropriate each time that
		emphasis settings change */
	m_bStrongEmphasis = false;

	if (GC.getInfo(eIndex).isAvoidGrowth())
	{
		m_iEmphasizeAvoidGrowthCount += (AI_isEmphasize(eIndex) ? 1 : -1);
		FAssert(AI_getEmphasizeAvoidGrowthCount() >= 0);
		// <advc.002f> Can affect label of the food bar or city bar icon
		gDLL->UI().setDirty(gDLL->UI().isCityScreenUp() ?
				CityScreen_DIRTY_BIT : CityInfo_DIRTY_BIT, true); // </advc.002f>
	}

	if (GC.getInfo(eIndex).isGreatPeople())
	{
		m_iEmphasizeGreatPeopleCount += (AI_isEmphasize(eIndex) ? 1 : -1);
		FAssert(AI_getEmphasizeGreatPeopleCount() >= 0);
	}

	FOR_EACH_ENUM(Yield)
	{
		if (GC.getInfo(eIndex).getYieldChange(eLoopYield))
		{
			m_aiEmphasizeYieldCount[eLoopYield] += (AI_isEmphasize(eIndex) ? 1 : -1);
			FAssert(AI_getEmphasizeYieldCount(eLoopYield) >= 0);
		}
	}

	FOR_EACH_ENUM(Commerce)
	{
		if (GC.getInfo(eIndex).getCommerceChange(eLoopCommerce))
		{
			m_aiEmphasizeCommerceCount[eLoopCommerce] += (AI_isEmphasize(eIndex) ? 1 : -1);
			FAssert(AI_getEmphasizeCommerceCount(eLoopCommerce) >= 0);
		}
	}

	AI_assignWorkingPlots(/* advc.131d: */ bNewValue);
	if (isActiveOwned() && isCitySelected())
		gDLL->UI().setDirty(SelectionButtons_DIRTY_BIT, true);
}

// advc.131d:
void CvCityAI::AI_setStrongEmphasis(bool bStrongEmphasis)
{
	if (m_bStrongEmphasis == bStrongEmphasis)
		return;
	m_bStrongEmphasis = bStrongEmphasis;
	AI_assignWorkingPlots();
}

// advc.003j: Added in BtS, was never used as far as I can tell.
/*void CvCityAI::AI_forceEmphasizeCulture(bool bNewValue)
{
	if (m_bForceEmphasizeCulture != bNewValue)
	{
		m_bForceEmphasizeCulture = bNewValue;

		m_aiEmphasizeCommerceCount[COMMERCE_CULTURE] += (bNewValue ? 1 : -1);
		FAssert(m_aiEmphasizeCommerceCount[COMMERCE_CULTURE] >= 0);
	}
}*/


int CvCityAI::AI_totalBestBuildValue(CvArea const& kArea) /* advc:  */ const
{
	int iTotalValue = 0;
	for (CityPlotIter itPlot(*this, false); itPlot.hasNext(); ++itPlot)
	{
		if (itPlot->isArea(kArea) && !GET_PLAYER(getOwner()).isAutomationSafe(*itPlot))
			iTotalValue += AI_getBestBuildValue(itPlot.currID());
	}
	return iTotalValue;
}


int CvCityAI::AI_clearFeatureValue(CityPlotTypes ePlot) const
{
	CvPlot const& kPlot = *plotCity(getX(), getY(), ePlot);
	CvFeatureInfo const& kFeature = GC.getInfo(kPlot.getFeatureType());
	/*int iValue = 0;
	iValue += kFeature.getYieldChange(YIELD_FOOD) * 100;
	iValue += kFeature.getYieldChange(YIELD_PRODUCTION) * 60;
	iValue += kFeature.getYieldChange(YIELD_COMMERCE) * 40;
	if (iValue > 0 && kPlot.isBeingWorked()) {
		iValue *= 3;
		iValue /= 2;
	}
	if (iValue != 0) {
		BonusTypes eBonus = kPlot.getBonusType(getTeam());
		if (eBonus != NO_BONUS) {
			iValue *= 3;
			if (kPlot.getImprovementType() != NO_IMPROVEMENT) {
				if (GC.getInfo(kPlot.getImprovementType()).isImprovementBonusTrade(eBonus))
					iValue *= 4;
			}
		}
	}*/ // BtS
	// K-Mod. All that yield change stuff is taken into account by the improvement evaluation function anyway.
	// ... except the bit about keeping good features on top of bonuses
	int iValue = 0;
	{
		BonusTypes const eBonus = kPlot.getNonObsoleteBonusType(getTeam());
		if (eBonus != NO_BONUS &&
			!GET_TEAM(getTeam()).isHasTech(GC.getInfo(eBonus).getTechCityTrade()))
		{
			iValue += kFeature.getYieldChange(YIELD_FOOD) * 100;
			iValue += kFeature.getYieldChange(YIELD_PRODUCTION) * 80; // was 60
			iValue += kFeature.getYieldChange(YIELD_COMMERCE) * 40;
			iValue *= 2;
			/*	that should be enough incentive to keep good features
				until we have the tech to decide on the best improvement. */
		}
	} // K-Mod end
	{
		int iHealthValue = 0;
		if (kFeature.getHealthPercent() != 0)
		{
			int iHealth = goodHealth() - badHealth();
			/*iHealthValue += (6 * kFeature.getHealthPercent()) / std::max(3, 1 + iHealth);
			if (iHealthValue > 0 && !kPlot.isBeingWorked()) {
				iHealthValue *= 3;
				iHealthValue /= 2;
			}*/ // BtS
			// K-Mod start
			iHealthValue += (iHealth < 0 ? 100 : 400 / (4 + iHealth)) +
					100 * kPlot.getPlayerCityRadiusCount(getOwner());
			iHealthValue *= kFeature.getHealthPercent();
			iHealthValue /= 100;
			/*  note: health is not any more valuable when we aren't working it.
				That kind of thing should be handled by the chop code. */
			// K-Mod end
		}
		iValue += iHealthValue;
	}
	// K-Mod
	// We don't want defensive features adjacent to our city
	if (ePlot < NUM_INNER_PLOTS)
		iValue -= kFeature.getDefenseModifier() / 2;
	if (GC.getGame().getGwEventTally() >= 0) // if GW Threshold has been reached
	{
		iValue += kFeature.getWarmingDefense() *
				(150 + 5 * GET_PLAYER(getOwner()).getGwPercentAnger()) / 100;
	} // K-Mod end
	if (iValue > 0)
	{
		if (kPlot.isImproved() &&
			GC.getInfo(kPlot.getImprovementType()).isRequiresFeature())
		{
			iValue += 500;
		}
		if (GET_PLAYER(getOwner()).getAdvancedStartPoints() >= 0)
			iValue += 400;
	}
	return -iValue;
}

// K-Mod. if aiYields == 0, then it will be calculated based on the 'best build' of the plot.
bool CvCityAI::AI_isGoodPlot(CityPlotTypes ePlot, int* aiYields) const // advc.enum: CityPlotTypes
{
	int tempArray[NUM_YIELD_TYPES];

	/*	it doesn't matter if this assert is wrong.
		I just don't expect to ever want this for the center plot. */
	FAssert(ePlot != CITY_HOME_PLOT);
	CvPlot* pPlot = getCityIndexPlot(ePlot);

	if (pPlot == NULL || pPlot->getWorkingCity() != this)
	{
		FAssertMsg(aiYields == NULL, "yields specified for non-existent plot");
		return false;
	}

	if (aiYields == NULL)
	{
		aiYields = tempArray;

		BuildTypes eBuild = NO_BUILD;
		if (m_aeBestBuild[ePlot] != NO_BUILD && m_aiBestBuildValue[ePlot] > 50)
			eBuild = m_aeBestBuild[ePlot];

		if (eBuild != NO_BUILD)
		{
			FOR_EACH_ENUM(Yield)
				aiYields[eLoopYield] = pPlot->getYieldWithBuild(eBuild, eLoopYield, true);
		}
		else
		{
			FOR_EACH_ENUM(Yield)
				aiYields[eLoopYield] = pPlot->getYield(eLoopYield);
		}
	}
	// the numbers used here are arbitrary; and I want to make sure high food tiles count as 'good'.
	FAssert((1 + GC.getFOOD_CONSUMPTION_PER_POPULATION()) * 10 > 27);
	return aiYields[YIELD_FOOD] * 10 + aiYields[YIELD_PRODUCTION] * 7 +
			aiYields[YIELD_COMMERCE] * 4 > (pPlot->isWater() ? 27 : 21);
}
// K-Mod end

// K-Mod rewritten to use my new function - AI_isGoodPlot.
int CvCityAI::AI_countGoodPlots() const
{
	int iCount = 0;
	for (CityPlotTypes ePlot = FIRST_ADJACENT_PLOT; ePlot < NUM_CITY_PLOTS; ++ePlot)
		iCount += AI_isGoodPlot(ePlot) ? 1 : 0;
	return iCount;
}

int CvCityAI::AI_countWorkedPoorPlots() const
{
	int iCount = 0;
	for (CityPlotTypes ePlot = FIRST_ADJACENT_PLOT; ePlot < NUM_CITY_PLOTS; ++ePlot)
		iCount += (isWorkingPlot(ePlot) && !AI_isGoodPlot(ePlot) ? 1 : 0);
	return iCount;
}

// K-Mod, based on BBAI ideas
int CvCityAI::AI_getTargetPopulation() const
{
	int iHealth = goodHealth() - badHealth();
			/*  advc.120e: Considering that this function isn't used for
				short-term evaluation (like juggling citizens),
				temporary penalties from espionage should be ignored. */
			// + getEspionageHealthCounter();
	int iTargetSize = AI_countGoodPlots() + std::max(0, getSpecialistPopulation() - totalFreeSpecialists() - 1);
	if (GET_PLAYER(getOwner()).AI_getFlavorValue(FLAVOR_GROWTH) > 0)
		iTargetSize += iTargetSize / 6; // specialists.

	iTargetSize = std::min(iTargetSize, 2 + getPopulation() + iHealth/2);

	if (iTargetSize < getPopulation())
	{
		iTargetSize = std::max(iTargetSize, getPopulation() - AI_countWorkedPoorPlots() + std::min(0, iHealth/2));
	}

	iTargetSize = std::min(iTargetSize, 1 + getPopulation()+(happyLevel()-unhappyLevel()));
			// advc.120e: Commented out
			//+getEspionageHappinessCounter()));

	return iTargetSize;
}

/*	K-Mod note: This function was once used for Debug only,
	but I've made it the one and only way to get the yield multipliers.
	This way we don't have to put up with duplicated code.
	This function has been mostly rewritten for K-Mod.
	Some parts of the original code still exist (particularly near the end),
	but most of the old code is gone. */
void CvCityAI::AI_getYieldMultipliers(int &iFoodMultiplier, int &iProductionMultiplier,
	int &iCommerceMultiplier, int &iDesiredFoodChange) const
{
	PROFILE_FUNC();

	iFoodMultiplier = 100;
	iCommerceMultiplier = 100;
	iProductionMultiplier = 100;

	int aiUnworkedYield[NUM_YIELD_TYPES] = {};
	int aiWorkedYield[NUM_YIELD_TYPES] = {};
	int iUnworkedPlots = 0;
	int iWorkedPlots = 0;

	CvPlayerAI& kPlayer = GET_PLAYER(getOwner());

	int iGoodTileCount = 0;

	for (WorkablePlotIter it(*this, false); it.hasNext(); ++it)
	{
		CvPlot const& kPlot = *it;
		CityPlotTypes const ePlot = it.currID();

		BuildTypes eBuild = NO_BUILD;
		if (m_aeBestBuild[ePlot] != NO_BUILD && m_aiBestBuildValue[ePlot] > 50)
			eBuild = m_aeBestBuild[ePlot];

		int aiPlotYields[NUM_YIELD_TYPES];
		if (eBuild != NO_BUILD)
		{
			FOR_EACH_ENUM(Yield)
				aiPlotYields[eLoopYield] = kPlot.getYieldWithBuild(eBuild, eLoopYield, true);
		}
		else
		{
			// K-Mod note. unfortunately, this counts GA yield whereas getYieldWithBuild does not.
			FOR_EACH_ENUM(Yield)
				aiPlotYields[eLoopYield] = kPlot.getYield(eLoopYield);
		}

		bool const bGoodPlot = AI_isGoodPlot(ePlot, aiPlotYields);
		if (bGoodPlot)
		{
			iGoodTileCount++;
			// note: worked plots are already counted.
			if (!kPlot.isBeingWorked())
			{
				FOR_EACH_ENUM(Yield)
					aiUnworkedYield[eLoopYield] += aiPlotYields[eLoopYield];
				iUnworkedPlots++;
				// note. this can count plots that are low on food.
			}
		}

		if (kPlot.isBeingWorked())
		{
			FOR_EACH_ENUM(Yield)
				aiWorkedYield[eLoopYield] += aiPlotYields[eLoopYield];
			iWorkedPlots++;
		}
	}

	/*	I'd like to use AI_getTargetPopulation here, to avoid code duplication,
		but that would result in us doing a bunch of unneccessary recalculations. */
	int iSpecialistCount = getSpecialistPopulation() - totalFreeSpecialists();
	int iHealth = goodHealth() - badHealth();
			// advc.120e: Mustn't de-emphasize food in response to spy attack!
			//+ getEspionageHealthCounter();
	int iTargetSize = iGoodTileCount + std::max(0, iSpecialistCount - 1);
	if (kPlayer.AI_getFlavorValue(FLAVOR_GROWTH) > 0)
		iTargetSize += iGoodTileCount / 6;
	iTargetSize = std::min(iTargetSize, //2 + getPopulation() + iHealth/2);
			/*  advc.120e: The above grows a bit too readily into bad health.
				E.g. if the city is size 8 and already has 1 bad health,
				TargetSize would be capped at 10, resulting in 3 bad health once the
				city gets there. My formula sets TargetSize to 9 in this example.
				1.55 to ensure that we round up when Health is even. */
			(fixp(1.55) + getPopulation() + scaled(iHealth, 2)).round());

	if (iTargetSize < getPopulation())
	{
		iTargetSize = std::max(iTargetSize, getPopulation() -
				AI_countWorkedPoorPlots() + std::min(0, iHealth/2));
	}

	iTargetSize = std::min(iTargetSize, 1 + getPopulation()+(happyLevel()-unhappyLevel()));
			// <advc.120e> Commented out
			//+getEspionageHappinessCounter()));
	// Never shrink aggressively
	if(iTargetSize < getPopulation())
		iTargetSize = std::max(iTargetSize, getPopulation() - 2); // </advc.120e>
	// <advc.300> Make Barbarians a little less afraid of angry citizens
	if(isBarbarian())
		iTargetSize++; // </advc.300>

	// total food and production include yield from buildings, corporations, specialists, and so on.
	int iFoodTotal = getBaseYieldRate(YIELD_FOOD);
	int iProductionTotal = getBaseYieldRate(YIELD_PRODUCTION);

	int iFutureFoodAdjustment = 0;
	if (iUnworkedPlots > 0)
	{
		/*	calculate approximately how much extra food we could work
			if we used our specialists and our extra population. */
		iFutureFoodAdjustment = (std::min(iUnworkedPlots,
				iSpecialistCount + std::max(0, iTargetSize - getPopulation())) *
				aiUnworkedYield[YIELD_FOOD]) / iUnworkedPlots;
	}
	iFoodTotal += iFutureFoodAdjustment;
	iProductionTotal += aiUnworkedYield[YIELD_PRODUCTION];

	int iExtraFoodForGrowth = 0;
	if (iTargetSize > getPopulation())
	{
		/* <advc.121> As far as I understand, ExtraFoodForGrowth says how much
		   food surplus is desirable. The original formula doesn't seem to grow
		   the cities fast enough. (The proper TargetSize is a different
		   question, but if you want to grow, do so quickly.) */
		int iDelta = iTargetSize - getPopulation() - 1; /*  TargetSize is often
				one greater than what the current happiness supports. Not what I
				want here, so subtract 1. */
		if(iDelta <= 3)
			iExtraFoodForGrowth = std::max(0, iDelta + 1);
		else iExtraFoodForGrowth = iDelta;
		// K-Mod formula now only for Barbarians:
		if(isBarbarian()) // advc.300:
			iExtraFoodForGrowth = (iTargetSize - getPopulation())/2 + 1;
		// </advc.121>
	}

	int iFoodDifference = iFoodTotal - (iTargetSize *
			GC.getFOOD_CONSUMPTION_PER_POPULATION() + iExtraFoodForGrowth);

	iDesiredFoodChange = -iFoodDifference + std::max(0, -iHealth);
	//

	/*if (iFoodDifference < 0)
		iFoodMultiplier +=  -iFoodDifference * 4;
	if (iFoodDifference > 4)
		iFoodMultiplier -= 8 + 4 * iFoodDifference;*/

	int iProductionTarget = 1 + std::max(getPopulation(), iTargetSize * 3 / 5);
	// <advc.300> +50% production target
	if(isBarbarian())
	{
		iProductionTarget *= 150;
		iProductionTarget /= 100;
	} // </advc.300>

	if (iProductionTotal < iProductionTarget)
	{
		iProductionMultiplier += 8 * (iProductionTarget - iProductionTotal);
	}

	// K-Mod.
	if (kPlayer.AI_getFlavorValue(FLAVOR_PRODUCTION) > 0 ||
		kPlayer.AI_getFlavorValue(FLAVOR_MILITARY) >= 10 ||
		isBarbarian()) // advc.300
	{
		/* iProductionMultiplier *= 113 + 2 * kPlayer.AI_getFlavorValue(FLAVOR_PRODUCTION) + kPlayer.AI_getFlavorValue(FLAVOR_MILITARY);
		iProductionMultiplier /= 100; */
		iCommerceMultiplier *= 100;
		iCommerceMultiplier /= 113 + 2 * kPlayer.AI_getFlavorValue(FLAVOR_PRODUCTION) +
				kPlayer.AI_getFlavorValue(FLAVOR_MILITARY);
	}
	// K-Mod end
	// <advc.300>
	if (isBarbarian())
	{
		int iCommerceToProductionShift = AI_commerceToProductionMultiplierShift();
		iProductionMultiplier += iCommerceToProductionShift;
		iCommerceMultiplier -= iCommerceToProductionShift;
		return;
	} // </advc.300>

	int iNetCommerce = kPlayer.AI_getAvailableIncome(); // K-Mod
	int iNetExpenses = kPlayer.calculateInflatedCosts() +
			std::max(0, -kPlayer.getGoldPerTurn()); // unofficial patch

	int iRatio = (100 * iNetExpenses) / std::max(1, iNetCommerce);

	if (iRatio > 40)
	{
		//iCommerceMultiplier += (33 * (iRatio - 40)) / 60;
		// K-Mod, just a bit steeper
		iCommerceMultiplier += (50 * (iRatio - 40)) / 60;
	}

	int iProductionAdvantage = 100 * AI_yieldMultiplier(YIELD_PRODUCTION);
	iProductionAdvantage /= kPlayer.AI_averageYieldMultiplier(YIELD_PRODUCTION);
	iProductionAdvantage *= kPlayer.AI_averageYieldMultiplier(YIELD_COMMERCE);
	iProductionAdvantage /= AI_yieldMultiplier(YIELD_COMMERCE);

	// adjust based on # of cities. (same as the original bts code)

	int iCommerceYieldMultiplier = AI_yieldMultiplier(YIELD_COMMERCE);
	if (iCommerceYieldMultiplier != 0)
	{
		iProductionAdvantage *= kPlayer.AI_averageYieldMultiplier(YIELD_COMMERCE);
		iProductionAdvantage /= iCommerceYieldMultiplier;
	}

	//now we normalize the effect by # of cities

	int iNumCities = kPlayer.getNumCities();
	FAssert(iNumCities > 0);
	iProductionAdvantage = (iProductionAdvantage * (iNumCities - 1) + 200) / (iNumCities + 1);

	FAssert(iNumCities > 0);//superstisious?

	//in short in an OCC the relative multipliers should *never* make a difference
	//so this indeed equals "100" for the iNumCities == 0 case.
	iProductionAdvantage = ((iProductionAdvantage * (iNumCities - 1) + 200) / (iNumCities + 1));

	iProductionMultiplier *= iProductionAdvantage;
	iProductionMultiplier /= 100;

	iCommerceMultiplier *= 100;
	iCommerceMultiplier /= iProductionAdvantage;

	/* int iGreatPeopleAdvantage = 100 * getTotalGreatPeopleRateModifier();

	int iGreatPeopleAdvantage = 100 * getTotalGreatPeopleRateModifier();
	iGreatPeopleAdvantage /= kPlayer.AI_averageGreatPeopleMultiplier();
	iGreatPeopleAdvantage = (iGreatPeopleAdvantage * (iNumCities - 1) + 200) / (iNumCities + 1);
	iGreatPeopleAdvantage += 200; // dilute
	iGreatPeopleAdvantage /= 3;

	//With great people we want to slightly increase food priority at the expense of commerce
	//this gracefully handles both wonder and specialist based GPP...
	iCommerceMultiplier *= 100;
	iCommerceMultiplier /= iGreatPeopleAdvantage;
	iFoodMultiplier *= iGreatPeopleAdvantage;
	iFoodMultiplier /= 100; */

	// Note: the AI does not use this kind of emphasis
	if (isHuman())
	{
		/*if (AI_isEmphasizeYield(YIELD_FOOD)) {
			iFoodMultiplier *= 140; // was 130
			iFoodMultiplier /= 100;
		}*/ // moved lower
		if (AI_isEmphasizeYield(YIELD_PRODUCTION))
		{
			iProductionMultiplier *= 130 // was 140
					+ (AI_isStrongEmphasis() ? 25 : 0); // advc.131d
			iProductionMultiplier /= 100;
			// K-Mod
			if (!AI_isEmphasizeYield(YIELD_COMMERCE))
			{
				iCommerceMultiplier *= 80
						- (AI_isStrongEmphasis() ? 13 : 0); // advc.131d
				iCommerceMultiplier /= 100;
			} // K-Mod end
		}
		if (AI_isEmphasizeYield(YIELD_COMMERCE))
		{
			iCommerceMultiplier *= 140
					+ (AI_isStrongEmphasis() ? 33 : 0); // advc.131d
			iCommerceMultiplier /= 100;
		}
	iFoodMultiplier /= 100;

	// if leader flavor likes production, increase production, reduce commerce
	if (kPlayer.AI_isDoStrategy(AI_STRATEGY_PRODUCTION))
	{
		iProductionMultiplier += 10;
		iCommerceMultiplier -= 10;
	}
	else

	if (iFoodMultiplier < 100)
	{
		// K-Mod. strategy / personality modifiers.
		// <advc> Moved into subroutine
		{
			int iCommerceToProductionShift = AI_commerceToProductionMultiplierShift();
			iProductionMultiplier += iCommerceToProductionShift;
			iCommerceMultiplier -= iCommerceToProductionShift;
		} // </advc>
		if (kPlayer.AI_getFlavorValue(FLAVOR_PRODUCTION) > 0)
			iProductionMultiplier += 5 + 2*kPlayer.AI_getFlavorValue(FLAVOR_PRODUCTION);
		if (kPlayer.AI_isDoStrategy(AI_STRATEGY_ECONOMY_FOCUS))
		{
			iProductionMultiplier -= 10;
			iCommerceMultiplier += 20;
		}
		/* else if (kPlayer.AI_getFlavorValue(FLAVOR_SCIENCE) + kPlayer.AI_getFlavorValue(FLAVOR_GOLD) > 2)
			iCommerceMultiplier += 5 + kPlayer.AI_getFlavorValue(FLAVOR_SCIENCE) + kPlayer.AI_getFlavorValue(FLAVOR_GOLD);*/
		// K-Mod end
	}
	if (iProductionMultiplier < 100)
		iProductionMultiplier = 10000 / (200 - iProductionMultiplier);
	if (iCommerceMultiplier < 100)
		iCommerceMultiplier = 10000 / (200 - iCommerceMultiplier);

	// K-Mod. experimental food value
	//iFoodMultiplier = (80 * iProduction + 40 * iCommerce) / (food needed for jobs)  * (Food needed for jobs + growth) / (food have total)
	//iFoodMultiplier = (80 * iProductionMultiplier * iProductionTotal + 40 * iCommerceMultiplier * iCommerceTotal) * (iFoodTotal + iDesiredFoodChange) / std::max(1, 100 * iTargetSize * GC.getFOOD_CONSUMPTION_PER_POPULATION() * iFoodTotal);

	/*	emphasise the yield that we are working, so that
		the weakest of the 'good' plots don't drag down the average quite so much.
		note: the multipliers on production and commerce
		should match the numbers used in AI_getImprovementValue. */
	iFoodMultiplier = 80 * iProductionMultiplier *
			(aiUnworkedYield[YIELD_PRODUCTION] + aiWorkedYield[YIELD_PRODUCTION] * 2) *
			(iUnworkedPlots + iWorkedPlots);
	iFoodMultiplier += 40 * iCommerceMultiplier *
			(aiUnworkedYield[YIELD_COMMERCE] + aiWorkedYield[YIELD_COMMERCE] * 2) *
			(iUnworkedPlots + iWorkedPlots);
	iFoodMultiplier /= 100 * std::max(1, iUnworkedPlots + 2*iWorkedPlots);
	iFoodMultiplier += 160 * iDesiredFoodChange;
	iFoodMultiplier = std::max(iFoodMultiplier, 200); // (a minimum yield value for small cities.)

	//iFoodMultiplier *= iTargetSize;
	//iFoodMultiplier /= std::max(iTargetSize, getPopulation() + iUnworkedPlots - std::max(0, iDesiredFoodChange));

	iFoodMultiplier *= (iFoodTotal + iDesiredFoodChange);
	iFoodMultiplier /= std::max(1, (iUnworkedPlots + iWorkedPlots) *
			GC.getFOOD_CONSUMPTION_PER_POPULATION() *
			(iFoodTotal-iExtraFoodForGrowth));
	/*	advc.121: I've seen this go above 60000. I guess the formulas above
		don't deal well with tiny cities that are supposed to grow big. */
	iFoodMultiplier = std::min(iFoodMultiplier, 5000);

	// Note: this food multiplier calculation still doesn't account for possible food yield multipliers. Sorry.

	if (isHuman() && AI_isEmphasizeYield(YIELD_FOOD))
	{
		iFoodMultiplier *= 140
				+ (AI_isStrongEmphasis() ? 33 : 0); // advc.131d
		iFoodMultiplier /= 100;
	}
	// K-Mod end

	if (iFoodMultiplier < 100)
		iFoodMultiplier = 10000 / (200 - iFoodMultiplier);
}


int CvCityAI::AI_getImprovementValue(CvPlot const& kPlot, ImprovementTypes eImprovement,
	int iFoodPriority, int iProductionPriority, int iCommercePriority, int iDesiredFoodChange,
	int iClearFeatureValue, bool bEmphasizeIrrigation, BuildTypes* peBestBuild) const
{
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner()); // K-Mod
	BonusTypes eBonus = kPlot.getBonusType(getTeam());
	BonusTypes eNonObsoleteBonus = kPlot.getNonObsoleteBonusType(getTeam());

	BuildTypes eBestTempBuild = NO_BUILD;
	// first check if the improvement is valid on this plot
	// this also allows us work out whether or not the improvement will remove the plot feature...
	bool bValid = false;
	bool bIgnoreFeature = false;
	if (eImprovement == kPlot.getImprovementType())
		bValid = true;
	else
	{
		int iBestTempBuildValue = 0;
		FOR_EACH_ENUM(Build)
		{
			if (GC.getInfo(eLoopBuild).getImprovement() != eImprovement)
				continue;
            // doc: shortcut to skip slave plantation etc
            if (GC.getInfo(eLoopBuild).isGraphicalOnly())
                continue;
			if (kOwner.canBuild(kPlot, eLoopBuild, false))
			{
				int iValue = 10000;
				iValue /= (GC.getInfo(eLoopBuild).getTime() + 1);
				// XXX feature production???  // (advc: I think the chop decision in AI_updateBestBuild will handle that)
				if (iValue > iBestTempBuildValue)
				{
					iBestTempBuildValue = iValue;
					eBestTempBuild = eLoopBuild;
				}
			}
		}
		if (eBestTempBuild != NO_BUILD)
		{
			bValid = true;
			if (kPlot.isFeature() &&
				GC.getInfo(eBestTempBuild).isFeatureRemove(kPlot.getFeatureType()))
			{
				bIgnoreFeature = true;
				if (GC.getInfo(kPlot.getFeatureType()).getYieldChange(YIELD_PRODUCTION) > 0 &&
					eNonObsoleteBonus == NO_BONUS)
				{
					if (kOwner.isHumanOption(PLAYEROPTION_LEAVE_FORESTS))
						bValid = false;
					else if (healthRate() < 0 &&
						GC.getInfo(kPlot.getFeatureType()).getHealthPercent() > 0)
					{
						bValid = false;
					}
					else if (kOwner.getFeatureHappiness(kPlot.getFeatureType()) > 0)
						bValid = false;
				}
			}
		}
	}
	if (!bValid)
	{
		if (peBestBuild != NULL)
			*peBestBuild = NO_BUILD;
		return 0;
	}

	// Now get the value of the improvement itself.
	ImprovementTypes eFinalImprovement = CvImprovementInfo::finalUpgrade(eImprovement);
	if (eFinalImprovement == NO_IMPROVEMENT)
		eFinalImprovement = eImprovement;

	scaled rValue;
	//int aiDiffYields[NUM_YIELD_TYPES]; // removed by K-Mod (replaced by time-weighted yields!)
	//int aiFinalYields[NUM_YIELD_TYPES];

	if (eBonus != NO_BONUS && eNonObsoleteBonus != NO_BONUS)
	{
		//if (GC.getInfo(eFinalImprovement).isImprovementBonusTrade(eNonObsoleteBonus))
		if (kOwner.doesImprovementConnectBonus(eFinalImprovement, eNonObsoleteBonus))
		{
			// K-Mod
			rValue += kOwner.AI_bonusVal(eNonObsoleteBonus, 1) * 50;
			rValue += 100;
			// K-Mod end
			/*	<advc.121> Kludge to force the AI to prefer improvements with yields
				over forts. Don't want to rule out forts altogether b/c of gems in a
				jungle -- w/o IW, a fort is the only way to connect the resource. */
			int iImprYieldChange = 0;
			FOR_EACH_ENUM(Yield)
			{
				iImprYieldChange += kPlot.calculateImprovementYieldChange(
						eImprovement, eLoopYield, kOwner.getID());
			}
			if (iImprYieldChange <= 0 && kPlot.getWorkingCity() != NULL)
				rValue /= 3;
			// </advc.121>
		}
		else
		{
			// K-Mod, bug fix. (original code deleted now.)
			/*  Presumably the original author wanted to subtract 1000 if eBestBuild would
				take away the bonus; not ... the nonsense they actually wrote. */
			if (kOwner.doesImprovementConnectBonus(kPlot.getImprovementType(), eNonObsoleteBonus))
			{
				// By the way, AI_bonusVal is typically 10 for the first bonus, and 2 for subsequent.
				rValue -= kOwner.AI_bonusVal(eNonObsoleteBonus, -1) * 50;
				rValue -= 100;
			}
		}
	}
	else
	{
		FOR_EACH_ENUM(Bonus)
		{
			if (GC.getInfo(eFinalImprovement).getImprovementBonusDiscoverRand(eLoopBonus) > 0)
				rValue++;
		}
	}

	//if (rValue >= 0) // condition disabled by K-Mod. (maybe the yield will be worth it!)

	EagerEnumMap<YieldTypes,scaled> weightedFinalYields;
	EagerEnumMap<YieldTypes,scaled> weightedYieldDiffs;
	{
		// K-Mod. Get a weighted average of the yields for improvements which upgrade (eg. cottages).
		int iTimeScale = 60;
		if (10 * GC.getGame().getElapsedGameTurns() < 3 * GC.getGame().getEstimateEndTurn())
			iTimeScale += 10;
		if (kOwner.AI_atVictoryStage4())
			iTimeScale -= 30;
		else if (10 * GC.getGame().getElapsedGameTurns() >
			7 * GC.getGame().getEstimateEndTurn())
		{
			iTimeScale -= 10;
		}
		// advc.001: was AI_isDoVictoryStrategy
		if (kOwner.AI_isDoStrategy(AI_STRATEGY_ECONOMY_FOCUS))
			iTimeScale += 50;
		if (GET_TEAM(getTeam()).AI_getNumWarPlans(WARPLAN_TOTAL) +
			// advc.001: Surely(?) preparations should count here as well
			GET_TEAM(getTeam()).AI_getNumWarPlans(WARPLAN_PREPARING_TOTAL) > 0)
		{
			iTimeScale -= 20;
		}
		else if (kOwner.AI_getFlavorValue(FLAVOR_MILITARY) > 0)
			iTimeScale -= 10;
		if (eNonObsoleteBonus != NO_BONUS &&
			!kOwner.doesImprovementConnectBonus(eImprovement, eNonObsoleteBonus))
		{
			iTimeScale = std::min(30, iTimeScale);
		}
		iTimeScale = std::max(iTimeScale, 20);
		// Other adjustments?

		// Adjustments to match calculation in CvPlot::doImprovement
		iTimeScale *= GC.getInfo(GC.getGame().getGameSpeedType()).getImprovementPercent();
		iTimeScale /= 100;
		iTimeScale *= GC.getInfo(GC.getGame().getStartEra()).getImprovementPercent();
		iTimeScale /= 100;
		{
			int iUpgrRate = kOwner.getImprovementUpgradeRate();
			// <advc.912f>
			if (iUpgrRate == 0)
				iTimeScale = 0;
			else
			{	/*	<advc.001> This fraction was flipped. Pretty sure that this was wrong.
					The ImprovementPercentModifiers apply to the time needed for an upgrade,
					whereas the upgrade rate applies to the time spent working the tile.
					A higher upgrade rate means that we should be more interested in
					delayed rewards, which is what a high iTimeScale value does. Note that
					the upgrade rate factors into the evaluation at no other point. */
				iTimeScale *= iUpgrRate;
				iTimeScale /= 100; // </advc.001>
				// </advc.912f>
			}
		}

		/*	Getting the time-weighted yields for the new and old improvements;
			then use them to calculate the final yield and yield difference. */
		AI_timeWeightedImprovementYields(kPlot, eImprovement,
				iTimeScale, weightedFinalYields);
		AI_timeWeightedImprovementYields(kPlot, kPlot.getImprovementType(),
				iTimeScale, weightedYieldDiffs);
	}
	FOR_EACH_ENUM(Yield)
	{
		weightedFinalYields.add(eLoopYield,
				kPlot.calculateNatureYield(eLoopYield, getTeam(), bIgnoreFeature));
		weightedYieldDiffs.set(eLoopYield, weightedFinalYields.get(eLoopYield) -
				(weightedYieldDiffs.get(eLoopYield) +
				kPlot.calculateNatureYield(eLoopYield, getTeam())));
	}

	// K-Mod
	/*  If this improvement results in a change in food, then building it
		will result in a change in the food multiplier.
		We should try to preempt that change to prevent best-build from oscillating.
		In our situation, we have
		iDesiredFoodChange ~= -iFoodDifference and
		aiDiffYields[0] == 2 * food change from the improvement.
		Unfortunately, it's a bit of a lengthy calculation to work out
		all of the factors involved in iFoodPriority. So I'll just use a
		very rough approximation. Hopefully it will be better than nothing. */
	int iCorrectedFoodPriority = iFoodPriority;
	if (weightedYieldDiffs.get(YIELD_FOOD) != 0 && isWorkingPlot(kPlot))
	{
		/*	16 is arbitrary. It would be possible to get something better
			using targetPop and so on, but that would be slower... */
		int iTotalFood = 16 * GC.getFOOD_CONSUMPTION_PER_POPULATION();
		iCorrectedFoodPriority = (iCorrectedFoodPriority *
				(iTotalFood - weightedYieldDiffs.get(YIELD_FOOD)) /
				std::max(1, iTotalFood)).round();
	}
	FAssert(iCorrectedFoodPriority == iFoodPriority ||
			((iCorrectedFoodPriority < iFoodPriority) ==
			(weightedYieldDiffs.get(YIELD_FOOD) > 0)));
	// This corrected priority isn't perfect, but I think it will be better than nothing.
	// K-Mod end

	rValue += weightedYieldDiffs.get(YIELD_FOOD) * iCorrectedFoodPriority;
	rValue += weightedYieldDiffs.get(YIELD_PRODUCTION) * iProductionPriority * fixp(0.8); // was 0.6
	rValue += weightedYieldDiffs.get(YIELD_COMMERCE) * iCommercePriority * fixp(0.4);

	/*	K-Mod. If we're going to have too much food
		regardless of the improvement on this plot, then reduce the food value */
	if (iDesiredFoodChange < 0 && -iDesiredFoodChange >=
		weightedFinalYields.get(YIELD_FOOD) - weightedYieldDiffs.get(YIELD_FOOD))
	{
		 // reduce the weight of food. (cf. values above.)
		rValue -= weightedYieldDiffs.get(YIELD_FOOD) * iCorrectedFoodPriority * fixp(0.4);
	} // K-Mod end

	if (rValue > 0)
	{
		// this is mainly to make it improve better tiles first
		//flood plain > grassland > plain > tundra
		rValue += weightedFinalYields.get(YIELD_FOOD) * 8; // was 10
		rValue += weightedFinalYields.get(YIELD_PRODUCTION) * 7; // was 6
		rValue += weightedFinalYields.get(YIELD_COMMERCE) * 4;

		if (weightedFinalYields.get(YIELD_FOOD) >=
			GC.getFOOD_CONSUMPTION_PER_POPULATION())
		{
			//this is a food yielding tile
			if (iCorrectedFoodPriority > 100)
				rValue.mulDiv(100 + iCorrectedFoodPriority, 200);
			if (iDesiredFoodChange > 0)
			{
				//iValue += (10 * (1 + aiDiffYields[YIELD_FOOD]) * (1 + aiFinalYields[YIELD_FOOD] - GC.getFOOD_CONSUMPTION_PER_POPULATION()) * iDesiredFoodChange * iCorrectedFoodPriority) / 100;
				// <K-Mod>
				rValue += (10 * (1 + weightedYieldDiffs.get(YIELD_FOOD)) *
						(1 + weightedFinalYields.get(YIELD_FOOD)
						- GC.getFOOD_CONSUMPTION_PER_POPULATION()) *
						std::min(1 + iDesiredFoodChange / 3, 4) *
						iCorrectedFoodPriority) / 100; // </K-Mod>
			}
			if (iCommercePriority > 100)
			{
				//iValue *= 100 + (((iCommercePriority - 100) * aiDiffYields[YIELD_COMMERCE]) / 2);
				//iValue /= 100;
				rValue += (rValue * ((iCommercePriority - 100) *
						weightedYieldDiffs.get(YIELD_COMMERCE))) / 200;
			}
		}
		/* else if (aiFinalYields[YIELD_FOOD] < GC.getFOOD_CONSUMPTION_PER_POPULATION()) {
			if ((aiDiffYields[YIELD_PRODUCTION] > 0) && (aiFinalYields[YIELD_FOOD]+aiFinalYields[YIELD_PRODUCTION] > 3)) {
				if (iCorrectedFoodPriority < 100 || kOwner.getCurrentEra() < 2) {
					//value booster for mines on hills
					iValue *= (100 + 25 * aiDiffYields[YIELD_PRODUCTION]);
					iValue /= 100;
				}
			}
		}*/

		if (iCorrectedFoodPriority < 100 && iProductionPriority > 100)
		{
			rValue *= 200 + (iProductionPriority - 100) *
					weightedFinalYields.get(YIELD_PRODUCTION);
			rValue /= 200;
		}
		if (eNonObsoleteBonus == NO_BONUS)
		{
			if (iDesiredFoodChange > 0)
			{
				//We want more food.
				rValue *= 2 + scaled::max(0, weightedYieldDiffs.get(YIELD_FOOD));
				rValue /= 2 * (1 + scaled::max(0, -weightedYieldDiffs.get(YIELD_FOOD)));
			}
		}
	}

	if (bEmphasizeIrrigation &&
		GC.getInfo(eFinalImprovement).isCarriesIrrigation())
	{
		rValue += 400; // advc.131: was 500
	}
	if (getImprovementFreeSpecialists(eFinalImprovement) > 0)
		// advc.131: Was 2000. That beats crucial strategic resources too easily.
		rValue += 1200;
	if (kOwner.getAdvancedStartPoints() < 0)
	{	// <advc.901> Code moved into (recursive) auxiliary function
		rValue += AI_healthHappyImprovementValue(kPlot, eImprovement,
				eFinalImprovement, bIgnoreFeature, false); // </advc.901>
	}
	/*  <advc.131> When considering to replace an improvement, iValue is
		based on the yield difference. A small negative value means that the
		new improvement is almost as good as the old one. Temporarily increase
		the value to allow ImprovementWeightModifier to tip the scales. */
	int const iPadding = 50;
	rValue += iPadding; // </advc.131>
	if (!isHuman() /* advc.131: */ && rValue > 0)
	{
		rValue *= std::max(0, GC.getInfo(getPersonalityType()).
				// advc.005a: was +200
				getImprovementWeightModifier(eFinalImprovement) + 100);
		rValue /= 100; // advc.005a: was /=200
	}
	rValue -= iPadding; // advc.131
	if (!kPlot.isImproved())
	{
		if (kPlot.isBeingWorked() &&
			// K-Mod. (don't boost the value if it means removing a good feature.)
			(iClearFeatureValue >= 0 || eBestTempBuild == NO_BUILD ||
			!GC.getInfo(eBestTempBuild).isFeatureRemove(kPlot.getFeatureType())))
		{
			rValue *= 5;
			rValue /= 4;
		}
		/*if (eBestTempBuild != NO_BUILD) {
			if (kPlot.isFeature()) {
				if (GC.getInfo(eBestTempBuild).isFeatureRemove(kPlot.getFeatureType())) {
					CvCity* pCity;
					iValue += kPlot.getFeatureProduction(eBestTempBuild, getTeam(), &pCity) * 2;
					FAssert(pCity == this);
					iValue += iClearFeatureValue;
				}
			}
		}*/ // K-Mod. I've moved this out of the if statement, because it should apply regardless of whether there is already an improvement on the plot.
	}
	else

	if (angryPopulation(1) > 0)
	{
		// cottage/villages (don't want to chop them up if turns have been invested)
		ImprovementTypes eImprovementDowngrade = GC.getInfo(kPlot.getImprovementType()).
				getImprovementPillage();
		/*while (eImprovementDowngrade != NO_IMPROVEMENT) {
			CvImprovementInfo& kImprovementDowngrade = GC.getInfo(eImprovementDowngrade);
			iValue -= kImprovementDowngrade.getUpgradeTime() * 8;
			eImprovementDowngrade = (ImprovementTypes)kImprovementDowngrade.getImprovementPillage();
		}*/ // BtS
		// K-Mod. Be careful not to get trapped in an infinite loop of improvement downgrades.
		if (eImprovementDowngrade != NO_IMPROVEMENT)
		{
			std::set<ImprovementTypes> cited_improvements;
			while (eImprovementDowngrade != NO_IMPROVEMENT &&
				cited_improvements.insert(eImprovementDowngrade).second)
			{
				CvImprovementInfo const& kImprovementDowngrade = GC.getInfo(eImprovementDowngrade);
				rValue -= kImprovementDowngrade.getUpgradeTime() * 8;
				eImprovementDowngrade = kImprovementDowngrade.getImprovementPillage();
			}
		} // K-Mod end

		if (GC.getInfo(kPlot.getImprovementType()).getImprovementUpgrade() != NO_IMPROVEMENT)
		{
			rValue -= scaled(8 * kPlot.getUpgradeProgress() *
					GC.getInfo(kPlot.getImprovementType()).getUpgradeTime(),
					100 * std::max(1,
					GC.getGame().getImprovementUpgradeTime(kPlot.getImprovementType())));
		}
		if (eNonObsoleteBonus == NO_BONUS)
		{
			if (isWorkingPlot(kPlot))
			{
				if ((iCorrectedFoodPriority < 100 &&
					weightedFinalYields.get(YIELD_FOOD) >=
					GC.getFOOD_CONSUMPTION_PER_POPULATION()) ||
					GC.getInfo(kPlot.getImprovementType()).getImprovementPillage() != NO_IMPROVEMENT)
				{
					rValue -= 70;
					rValue.mulDiv(2, 3);
				}
			}
		}
		if (kOwner.isHumanOption(PLAYEROPTION_SAFE_AUTOMATION) &&
			rValue.isPositive()) // advc.001
		{
			rValue /= 4; // Greatly prefer builds which are legal.
		}
	}
	// K-Mod. Feature value. (moved from the 'no improvement' block above.)
	if (kPlot.isFeature() && eBestTempBuild != NO_BUILD &&
		GC.getInfo(eBestTempBuild).isFeatureRemove(kPlot.getFeatureType()))
	{
		/*CvCity* pCity; iValue += kPlot.getFeatureProduction(eBestTempBuild, getTeam(), &pCity) * 2;
		FAssert(pCity == this);*/ // handle chop value elsewhere
		rValue += iClearFeatureValue;
	} // K-Mod end
	if (peBestBuild != NULL)
		*peBestBuild = eBestTempBuild;

	return rValue.round();
}

/*  advc.901: Cut from AI_getImprovementValue so that benefits for nearby team cities
	can be taken into account (through recursive calls). */
int CvCityAI::AI_healthHappyImprovementValue(CvPlot const& kPlot,
	ImprovementTypes eImprovement, ImprovementTypes eFinalImprovement,
	bool bIgnoreFeature, bool bIgnoreOtherCities) const
{
	PROFILE_FUNC(); // advc.901: To be tested: see if the recursive calls are a problem
	int r = 0;
	// <advc.901>
	int iHappyChange, iHealthChange, iHealthPercentChange;
	// Complicated calculation (and also needed for the UI) -> another auxiliary function
	calculateHealthHappyChange(kPlot, eFinalImprovement, kPlot.getImprovementType(),
			bIgnoreFeature, iHappyChange, iHealthChange, iHealthPercentChange);
	// </advc.901>
	if (iHappyChange != 0)
	{
		//int iHappyLevel = iHappyAdjust + (happyLevel() - unhappyLevel(0));
		int iHappyLevel = happyLevel() - unhappyLevel(); // iHappyAdjust isn't currently being used.
		if (eImprovement == kPlot.getImprovementType())
			iHappyLevel -= iHappyChange;
		bool const bCanGrow = true;// (getYieldRate(YIELD_FOOD) > foodConsumption());
		/*int iHealthLevel = goodHealth() - badHealth(false, 0);
		if (iHappyLevel <= iHealthLevel)
			iHappyValue += 200 * std::max(0, (bCanGrow ? std::min(6, 2 + iHealthLevel - iHappyLevel) : 0) - iHappyLevel);
		else*/ // BtS code commented out by K-Mod
		int iHappyValue = 200 * std::max(0, (bCanGrow ? 1 : 0) - iHappyLevel);
		if (iHappyLevel <= 0) // advc: moved down
			iHappyValue += 400;
		iHappyValue = std::max(iHappyValue, 5); // advc.901: Count at least a marginal value
		if (!kPlot.isBeingWorked())
		{
			iHappyValue *= 4;
			iHappyValue /= 3;
		}
		//iHappyValue += std::max(0, kPlot.getCityRadiusCount() - 1) * (iHappyValue > 0 ? iHappyLevel / 2 : 200); // BtS
		/*iHappyValue *= (kPlot.getPlayerCityRadiusCount(getOwner()) + 1);
		iHappyValue /= 2;*/ // K-Mod (advc.901: Replaced with recursive call at the end)
		r += iHappyValue * iHappyChange;
	}  // <advc.901> Similar treatment for health (but the fractions complicate things)
	if (iHealthPercentChange != 0)
	{
		// The fractional health lost to rounding (don't treat that as having 0 value)
		int iHealthTendency = 0;
		int iDeltaPercent = iHealthPercentChange - 100 * iHealthChange;
		if (iDeltaPercent >= 0)
			iHealthTendency = iDeltaPercent % 100;
		else iHealthTendency = -(-iDeltaPercent % 100);
		/*  Health changes from clearing features are already taken into account by
			AI_clearFeatureValue. That function can't deal with rounding, but it's
			needed for chop evaluation, which doesn't currently involve _this_ function.
			Perhaps the way to untangle this would be to use AI_getImprovementValue
			also for evaluating chopping (with eImprovement=NO_IMPROVEMENT). For now,
			let's at least subtract the double counted health from the tendency value. */
		if (bIgnoreFeature)
		{
			FeatureTypes const eFeature = kPlot.getFeatureType();
			if (eFeature != NO_FEATURE)
				iHealthTendency += GC.getInfo(eFeature).getHealthPercent();
			FAssert(eFeature != NO_FEATURE); // Caller arguably shouldn't set bIgnoreFeature otherwise
		}

		int iHealthLevel = goodHealth() - badHealth();
		if (eImprovement == kPlot.getImprovementType())
			iHealthLevel -= iHealthChange;
		int iHealthValue = 75 * std::max(0, 1 - iHealthLevel);
		if (iHealthLevel <= 0)
			iHealthValue += 150;
		iHealthValue = std::max(iHealthValue, 2);
		if (!kPlot.isBeingWorked())
		{
			iHealthValue *= 4;
			iHealthValue /= 3;
		}
		r += (iHealthValue * (iHealthChange * 400 + iHealthTendency)) / 400;
	}
	// Other affected team cities matter just as much
	if (!bIgnoreOtherCities && r != 0) // Slightly reckless; for performance.
	{
		for (CityPlotIter it(kPlot, false); it.hasNext(); ++it)
		{
			CvCityAI* pCity = it->AI_getPlotCity();
			if (pCity == NULL || pCity == this || pCity->getTeam() != getTeam())
				continue;
			r += AI_healthHappyImprovementValue(kPlot, eImprovement,
					eFinalImprovement, bIgnoreFeature);
		}
	} // </advc.901>
	return r;
}


BuildTypes CvCityAI::AI_getBestBuild(CityPlotTypes ePlot) const // advc.enum: CityPlotTypes
{
	// <advc.opt> Now also store the best build among all city plots
	if(ePlot == NO_CITYPLOT)
		return m_eBestBuild; // </advc.opt>
	FAssertEnumBounds(ePlot);
	return m_aeBestBuild[ePlot];
}


int CvCityAI::AI_countBestBuilds(CvArea const& kArea) const
{
	int iCount = 0;
	for (CityPlotIter it(*this, false); it.hasNext(); ++it)
	{
		if (it->isArea(kArea) && AI_getBestBuild(it.currID()) != NO_BUILD)
			iCount++;
	}
	return iCount;
}

// Note: this function has been somewhat mangled by K-Mod
void CvCityAI::AI_updateBestBuild()
{
	PROFILE_FUNC(); // advc
	CvPlayerAI& kOwner = GET_PLAYER(getOwner()); // K-Mod

	int iFoodMultiplier, iProductionMultiplier, iCommerceMultiplier, iDesiredFoodChange;
	AI_getYieldMultipliers(iFoodMultiplier, iProductionMultiplier, iCommerceMultiplier, iDesiredFoodChange);

	/* I've disabled these for now
	int iHappyAdjust = 0;
	int iHealthAdjust = 0; */

	bool bChop = false;

	if (getProductionProcess() == NO_PROCESS) // K-Mod. (never chop if building a process.)
	{
		if (!bChop)
		{
			ProjectTypes eProductionProject = getProductionProject();
			if (eProductionProject != NO_PROJECT && AI_projectValue(eProductionProject) > 0)
				bChop = true;
		}
		if (!bChop)
		{
			BuildingTypes eProductionBuilding = getProductionBuilding();
			if (eProductionBuilding != NO_BUILDING &&
				GC.getInfo(eProductionBuilding).isWorldWonder())
			{
				bChop = true;
			}
		}
		/*if (!bChop)
			bChop = ((getArea().getAreaAIType(getTeam()) == AREAAI_OFFENSIVE) || (getArea().getAreaAIType(getTeam()) == AREAAI_DEFENSIVE) || (getArea().getAreaAIType(getTeam()) == AREAAI_MASSING));
		if (!bChop) {
			UnitTypes eProductionUnit = getProductionUnit();
			bChop = (eProductionUnit != NO_UNIT && GC.getInfo(eProductionUnit).isFoodProduction());
		}*/ // BtS
		// K-Mod. Chop when a new city with low productivity is trying to construct a (useful) building.
		if (!bChop && getProductionBuilding() != NO_BUILDING)
		{
			// ideally this would be based on the value of what we are building, and on the number of things we still want to build.
			// But it currently isn't easy to get that infomation, so I'm just going to use arbitrary minimums. Sorry.
			// (The scale of this is roughly a 2 pop whip or 2 mines of productivity - higher with productive flavour.)
			if (kOwner.AI_getFlavorValue(FLAVOR_PRODUCTION) > 0
				? (getHighestPopulation() <= 6 && getBaseYieldRate(YIELD_PRODUCTION) <= 10)
				: (getHighestPopulation() <= 4 && getBaseYieldRate(YIELD_PRODUCTION) <= 7))
			{
				bChop = true;
			}
		}
		CvWorldInfo const& kWorld = GC.getInfo(GC.getMap().getWorldSize()); // advc
		// Chop when trying to expand, and when at war -- but only if there is not financial trouble.
		if (!bChop)
		{
			int iDummy;
			if (kOwner.AI_isLandWar(getArea()) ||
				(kOwner.getNumCities() < kWorld.getTargetNumCities() &&
				kOwner.AI_getNumAreaCitySites(getArea(), iDummy) > 0))
			{
				if (!kOwner.AI_isFinancialTrouble())
					bChop = true;
			}
		}
		// Chop for workers, if we are short.
		if (!bChop && getProductionUnitAI() == UNITAI_WORKER)
		{
			int const iAreaWorkers = getArea().getNumAIUnits(getOwner(), UNITAI_WORKER);
			int const iAreaCities = getArea().getCitiesPerPlayer(getOwner());
			//if(iAreaWorkers < std::max(iAreaCities, kWorld.getTargetNumCities())*3/2)
			/*  <advc.113> Note that, if we have time to chop, then we can't be really
				short on workers. (I guess kOwner.AI_neededWorkers would be too slow here.) */
			if (getProductionTurnsLeft() > 3 &&
				(3 * iAreaWorkers < 4 * iAreaCities ||
				(2 * iAreaWorkers < 3 * iAreaCities &&
				AI_getWorkersHave() <= 0 && AI_getWorkersNeeded() > 0)))
			{ // </advc.113>
				bChop = true;
			}
		}
		// K-Mod end
	}

	/*if (getProductionBuilding() != NO_BUILDING) {
		iHappyAdjust += getBuildingHappiness(getProductionBuilding());
		iHealthAdjust += getBuildingHealth(getProductionBuilding());
	}*/

	for (WorkablePlotIter it(*this, false); it.hasNext(); ++it)
	{
		CvPlot& kPlot = *it;
		CityPlotTypes const ePlot = it.currID();
		BuildTypes const eLastBestBuildType = m_aeBestBuild[ePlot];

		AI_bestPlotBuild(kPlot, &m_aiBestBuildValue[ePlot], &m_aeBestBuild[ePlot],
				iFoodMultiplier, iProductionMultiplier, iCommerceMultiplier, bChop,
				0, 0, iDesiredFoodChange); //iHappyAdjust, iHealthAdjust, iDesiredFoodChange);
		// K-Mod, originally this was all workers at the city.
		//int iWorkerCount = GET_PLAYER(getOwner()).AI_plotTargetMissionAIs(&kPlot, MISSIONAI_BUILD);
		/*m_aiBestBuildValue[ePlot] *= 4;
		m_aiBestBuildValue[ePlot] += 3 + iWorkerCount; // (round up)
		m_aiBestBuildValue[ePlot] /= (4 + iWorkerCount);*/ // disabled by K-Mod. I don't think this really helps us.
		// (advc: conditionals turned into assertions)
		FAssert(m_aiBestBuildValue[ePlot] <= 0 || m_aeBestBuild[ePlot] != NO_BUILD);
		FAssert(m_aeBestBuild[ePlot] == NO_BUILD || m_aiBestBuildValue[ePlot] > 0);

		// K-Mod, make some adjustments to our yield weights based on our new bestbuild
		// [really we want (isWorking || was good plot), but that's harder and more expensive...]
		if (m_aeBestBuild[ePlot] == eLastBestBuildType)
			continue;

		if (isWorkingPlot(ePlot)) // [or was 'good plot' with previous build]
		{
			// its a new best-build, so lets adjust our multiplier values.
			// This adjustment is rough, but better than nothing. (at least, I hope so...)
			// (The most accurate way to do this would be to use AI_getYieldMultipliers; but I think that would be too slow.)
			// food
			int iDelta = (m_aeBestBuild[ePlot] == NO_BUILD ?  // new
					kPlot.getYield(YIELD_FOOD) :
					kPlot.getYieldWithBuild(m_aeBestBuild[ePlot], YIELD_FOOD, true));
			iDelta -= (eLastBestBuildType == NO_BUILD ? kPlot.getYield(YIELD_FOOD) :  // old
					kPlot.getYieldWithBuild(eLastBestBuildType, YIELD_FOOD, true));
			if (iDelta != 0)
			{
				int iTotalFood = 16 * GC.getFOOD_CONSUMPTION_PER_POPULATION();
				iFoodMultiplier *= iTotalFood - iDelta;
				iFoodMultiplier /= std::max(1, iTotalFood);
				// cf. adjustment in AI_getImprovementValue.
				iDesiredFoodChange -= iDelta;
			}

			// production
			iDelta = (m_aeBestBuild[ePlot] == NO_BUILD ? kPlot.getYield(YIELD_PRODUCTION) : // new
					kPlot.getYieldWithBuild(m_aeBestBuild[ePlot], YIELD_PRODUCTION, true));
			iDelta -= (eLastBestBuildType == NO_BUILD ? kPlot.getYield(YIELD_PRODUCTION) : // old
					kPlot.getYieldWithBuild(eLastBestBuildType, YIELD_PRODUCTION, true));
			if (iDelta != 0)
			{
				int iProductionTotal = getBaseYieldRate(YIELD_PRODUCTION);
				int iProductionTarget = 1 + getPopulation();
				// note: the true values depend on unworked plots and so on. this is just a rough approximation.
				if (iProductionTotal < iProductionTarget)
				{
					iProductionMultiplier -= 6 * std::min(iDelta,
							iProductionTarget - iProductionTotal);
					// cf. iProductionMultiplier += 8 * (iProductionTarget - iProductionTotal);
				}
				// iProductionTotal += iDelta;
			}
			// Happiness modifers.. maybe I'll do this later, after testing etc.
		}

		// since best-build has changed, cancel all current build missions on this plot
		if (eLastBestBuildType != NO_BUILD)
		{
			FOR_EACH_GROUPAI_VAR(pLoopSelectionGroup, kOwner)
			{
				if (pLoopSelectionGroup->AI_getMissionAIPlot() == &kPlot &&
					pLoopSelectionGroup->AI_getMissionAIType() == MISSIONAI_BUILD)
				{
					FAssert(pLoopSelectionGroup->getHeadUnitAIType() == UNITAI_WORKER ||
							pLoopSelectionGroup->getHeadUnitAIType() == UNITAI_WORKER_SEA);
					pLoopSelectionGroup->clearMissionQueue();
				}
			}
		}
		// K-Mod end
	}

	//new experimental yieldValue calcuation

	CityPlotTypes eBestPlot = NO_CITYPLOT;
	int iBestPlotValue = -1;
	int iBestUnworkedPlotValue = 0;
	// advc: Was naked array w/o initial values
	std::vector<int> aiValues(NUM_CITY_PLOTS, MAX_INT);
	int const iGrowthValue = AI_growthValuePerFood(); // K-Mod
	for (WorkablePlotIter itPlot(*this, false); itPlot.hasNext(); ++itPlot)
	{
		CvPlot const& kPlot = *itPlot;
		CityPlotTypes const ePlot = itPlot.currID();

		if (m_aeBestBuild[ePlot] != NO_BUILD)
		{
			int aiYields[NUM_YIELD_TYPES]; // advc: Moved into the loop; don't reuse.
			int iValue = 0;
			FOR_EACH_ENUM(Yield)
			{
				aiYields[eLoopYield] = kPlot.getYieldWithBuild(
						m_aeBestBuild[ePlot], eLoopYield, true);
			}
			iValue += AI_yieldValue(aiYields, 0, false, false, true, true, iGrowthValue);
			aiValues[ePlot] = iValue;
			// K-Mod
			/*	Also evaluate the _change_ in yield,
				so that we aren't always tinkering with our best plots
				Note: AI_yieldValue wasn't intended to be used with negative yields.
				But I think it will work; and it doesn't need to be perfectly accurate anyway. */
			FOR_EACH_ENUM(Yield)
				aiYields[eLoopYield] -= kPlot.getYield(eLoopYield);
			iValue += AI_yieldValue(aiYields, 0, false, false, true, true, iGrowthValue);
			// priority increase for chopping when we want to chop
			//if (bChop)
			/*  <advc.117> Also increase the value a little when
				constructing sth. nonurgent */
			if (kPlot.isFeature() && GC.getInfo(m_aeBestBuild[ePlot]).
				isFeatureRemove(kPlot.getFeatureType())) // </advc.117>
			{
				// Increase chop multipier from 2 to 3; handle nonurgent construction orders.
				CvCity* pCity=NULL;
				int iChopValue = kPlot.getFeatureProduction(
						m_aeBestBuild[ePlot], getTeam(), &pCity) * 3;
				// Based on K-Mod 1.45
				if(ePlot < NUM_INNER_PLOTS && iChopValue > 0 &&
					GC.getInfo(kPlot.getFeatureType()).getDefenseModifier() > 0)
				{
					iChopValue += 10;
				}
				if (bChop /* advc.300: */ && !isBarbarian())
					iValue += iChopValue;
				else if (getProductionBuilding() != NO_BUILDING)
					iValue += iChopValue / 3;
				// </advc.117>
				/*  note: the scale of iValue here is roughly 4x commerce per turn.
					So a boost of 40 would be signficant. */
				FAssert(pCity == this);
			}
			/*  make some minor adjustments to prioritize plots that are easy to access,
				and plots which aren't already improved. */
			if (iValue > 0)
			{
				if (kPlot.isRoute())
					iValue += 2;
				if (!kPlot.isImproved())
					iValue += 4;
				if (kPlot.getNumCultureRangeCities(getOwner()) > 1)
					iValue += 1;
			}
			// K-Mod end

			iValue = std::max(0, iValue);
			m_aiBestBuildValue[ePlot] *= iValue + 100;
			m_aiBestBuildValue[ePlot] /= 100;
			if (iValue > iBestPlotValue)
			{
				eBestPlot = ePlot;
				iBestPlotValue = iValue;
			}
		}
		if (!kPlot.isBeingWorked())
		{
			int aiYields[NUM_YIELD_TYPES];
			FOR_EACH_ENUM(Yield)
				aiYields[eLoopYield] = kPlot.getYield(eLoopYield);
			int iValue = AI_yieldValue(aiYields, 0, false, false, true, true, iGrowthValue);
			iBestUnworkedPlotValue = std::max(iBestUnworkedPlotValue, iValue);
		}
	}
	if (eBestPlot != NO_CITYPLOT)
	{
		//m_aiBestBuildValue[iBestPlot] *= 2;
		m_aiBestBuildValue[eBestPlot] = m_aiBestBuildValue[eBestPlot] * 3 / 2; // K-Mod
		m_eBestBuild = m_aeBestBuild[eBestPlot]; // advc.opt
	}
	else m_eBestBuild = NO_BUILD; // advc.opt

	//Prune plots which are sub-par.
	// K-Mod. I've rearranged the following code. But kept most of the original functionality.
	if (iBestUnworkedPlotValue <= 0)
		return;
	{
		PROFILE("AI_updateBestBuild pruning phase");
		for (WorkablePlotIter itPlot(*this, false); itPlot.hasNext(); ++itPlot)
		{
			CvPlot const& kPlot = *itPlot;
			CityPlotTypes const ePlot = itPlot.currID();

			/*	K-Mod. If the new improvement will upgrade over time, then don't mark it
				as being low-priority. We want to build it sooner rather than later. */
			if (m_aeBestBuild[ePlot] != NO_BUILD &&
				GC.getInfo(m_aeBestBuild[ePlot]).getImprovement() != NO_IMPROVEMENT &&
				GC.getInfo(GC.getInfo(m_aeBestBuild[ePlot]).getImprovement()).
				getImprovementUpgrade() == NO_IMPROVEMENT)
			{
				if (!kPlot.isImproved() &&
				/*	<advc.117> Don't "prune" removal of forests; not sure if this
					could otherwise happen. */
					(!kPlot.isFeature() ||
					!GC.getInfo(m_aeBestBuild[ePlot]).isFeatureRemove(kPlot.getFeatureType())))
				{	// </advc.117>
					if (!kPlot.isBeingWorked() && aiValues[ePlot] <= iBestUnworkedPlotValue &&
						aiValues[ePlot] < 400) // was 500. (reduced due to some rescaling)
					{
						m_aiBestBuildValue[ePlot] = 1;
					}
				}
				else
				{
					int aiYields[NUM_YIELD_TYPES];
					FOR_EACH_ENUM(Yield)
						aiYields[eLoopYield] = kPlot.getYield(eLoopYield);
					int iValue = AI_yieldValue(aiYields, 0, false, false, true, true, iGrowthValue);
					if (iValue > aiValues[ePlot])
						m_aiBestBuildValue[ePlot] = 1;
				}
			}
		}
	}
}

// advc.129:
int CvCityAI::AI_countOvergrownBonuses(FeatureTypes eFeature) const
{
	int iR = 0;
	for (CityPlotIter it(*this, false); it.hasNext(); ++it)
	{
		CvPlot const& p = *it;
		if (p.getOwner() == getID() && p.getFeatureType() == eFeature && !p.isImproved())
		{
			BonusTypes eBonus = p.getNonObsoleteBonusType(getTeam());
			if (eBonus == NO_BONUS)
				continue;
			FOR_EACH_ENUM(Build)
			{
				CvBuildInfo const& kLoopBuild = GC.getInfo(eLoopBuild);
				if(kLoopBuild.getImprovement() == NO_IMPROVEMENT ||
					!kLoopBuild.isFeatureRemove(eFeature))
				{
					continue;
				}
				if (!GC.getInfo(kLoopBuild.getImprovement()).isImprovementBonusMakesValid(eBonus))
					continue;
				/*  This function is used for tech evaluation; too complicated
					to check if the required tech is on the path to the tech
					that is being evaluated. It's really only for Bronze Working
					anyway, so an era check suffices.
					The tech under evaluation is assumed to enable eBuild, so
					no need to check getFeatureTech either. */
				TechTypes eReq = kLoopBuild.getTechPrereq();
				if (eReq == NO_TECH ||
					GC.getInfo(eReq).getEra() <= GET_PLAYER(getOwner()).getCurrentEra())
				{
					iR++;
					break;
				}
			}
		}
	}
	return iR;
}


void CvCityAI::AI_doDraft(bool bForce)
{
	PROFILE_FUNC();

	FAssert(!isHuman());
	if (isBarbarian() || !canConscript())
		return; // advc

	// BETTER_BTS_AI_MOD,City AI, War Strategy AI, 07/12/09, jdog5000: START
	//if (GC.getGame().AI_combatValue(getConscriptUnit()) > 33) // disabled by K-Mod
	if (bForce)
	{
		conscript();
		return;
	}

	const CvPlayerAI& kOwner = GET_PLAYER(getOwner());
	//bool bLandWar = (getArea().getAreaAIType(getTeam()) == AREAAI_OFFENSIVE || getArea().getAreaAIType(getTeam()) == AREAAI_DEFENSIVE || getArea().getAreaAIType(getTeam()) == AREAAI_MASSING);
	bool bLandWar = kOwner.AI_isLandWar(getArea()); // K-Mod
	bool bDanger = (!AI_isDefended() && AI_isDanger());
	int iUnitCostPerMil = kOwner.AI_unitCostPerMil(); // K-Mod

	// Don't go broke from drafting
	//if (!bDanger && kOwner.AI_isFinancialTrouble())
	// K-Mod. (cf. conditions for scrapping units in AI_doTurnUnitPost)
	if (!bDanger && iUnitCostPerMil > kOwner.AI_maxUnitCostPerMil(area(), 50))
		return;

	// K-Mod. See if our drafted unit is particularly good value.
	// (cf. my calculation in CvPlayerAI::AI_civicValue)
	UnitTypes eConscriptUnit = getConscriptUnit();
	int iConscriptPop = std::max(1, GC.getInfo(eConscriptUnit).getProductionCost() /
			GC.getDefineINT(CvGlobals::CONSCRIPT_POPULATION_PER_COST));

	// call it "good value" if we get at least 1.4 times the normal hammers-per-conscript-pop.
	// (with standard settings, this only happens for riflemen)
	bool bGoodValue = 10 * GC.getInfo(eConscriptUnit).getProductionCost() /
			(iConscriptPop * GC.getDefineINT(CvGlobals::CONSCRIPT_POPULATION_PER_COST)) >= 14;

	// one more thing... it's not "good value" if we already have too many troops.
	if (!bLandWar && bGoodValue)
	{
		bGoodValue = iUnitCostPerMil <= kOwner.AI_maxUnitCostPerMil(area(), 20) +
				kOwner.AI_getFlavorValue(FLAVOR_MILITARY);
	}
	// K-Mod end - although, I've put a bunch of 'bGoodValue' conditions in all through the rest of this function.

	// Don't shrink cities too much
	//int iConscriptPop = getConscriptPopulation();
	if (//!bGoodValue && // advc.017: Don't shrink them arbitrarily just b/c it's "good value"!
		!bDanger && (3 * (getPopulation() - iConscriptPop) < getHighestPopulation() * 2))
	{
		return;
	} // <advc.017>
	// Cut-and-pasted from below:
	bool bTooMuchPop = AI_countWorkedPoorPlots() > 0 ||
			foodDifference(false, true)+getFood() < 0 ||
			(foodDifference(false, true) < 0 && healthRate() <= -4);
	// Don't just draft for no particular reason
	if(!bDanger && !kOwner.AI_isFocusWar() && !bTooMuchPop)
		return; // </advc.017>
	// Large cities want a little spare happiness
	int iHappyDiff = GC.getDefineINT(CvGlobals::CONSCRIPT_POP_ANGER) - iConscriptPop + (bGoodValue ? 0 : getPopulation()/10);

	if((!bGoodValue && !bLandWar) || angryPopulation(iHappyDiff) > 0)
		return; // advc
	bool bWait = true;
	if(kOwner.AI_isDoStrategy(AI_STRATEGY_TURTLE))
	{	// Full out defensive
		/*if (bDanger || getPopulation() >= std::max(5, getHighestPopulation() - 1))
			bWait = false;
		else if (AI_countWorkedPoorPlots() >= 1)
			bWait = false;*/ // BtS
		// K-Mod: full out defensive indeed. We've already checked for happiness, and we're desperate for units.
		// Just beware of happiness sources that might expire - such as military happiness.
		if (getConscriptAngerTimer() == 0 || AI_countWorkedPoorPlots() > 0)
			bWait = false;
	}

	if (bWait && bDanger)
	{
		// If city might be captured, don't hold back
		/* BBAI code
		int iOurDefense = GET_TEAM(getTeam()).AI_getOurPlotStrength(plot(),0,true,false,true);
		int iEnemyOffense = GET_PLAYER(getOwner()).AI_getEnemyPlotStrength(plot(),2,false,false);
		if (iOurDefense == 0 || 3 * iEnemyOffense > 2 * iOurDefense)*/
		// K-Mod
		int iOurDefense = kOwner.AI_localDefenceStrength(plot(), getTeam(), DOMAIN_LAND, 0);
		int iEnemyOffense = kOwner.AI_localAttackStrength(plot(), NO_TEAM, DOMAIN_LAND, 2);
		if (iOurDefense < iEnemyOffense) // K-Mod end
			bWait = false;
	}

	if (bWait)
	{
		// Non-critical, only burn population if population is not worth much
		if (SyncRandSuccess100(AI_buildUnitProb(true)) && // advc.017
			(getConscriptAngerTimer() == 0 || isNoUnhappiness()) && // K-Mod
			(bGoodValue || bTooMuchPop)) // advc.017  (no functional change here)
		{
			bWait = false;
		}
	}

	if (!bWait && gCityLogLevel >= 2)
		logBBAI("      City %S (size %d, highest %d) chooses to conscript with danger: %d, land war: %d, poor tiles: %d%s", getName().GetCString(), getPopulation(), getHighestPopulation(), bDanger, bLandWar, AI_countWorkedPoorPlots(), bGoodValue ? ", good value" : "");
	// BETTER_BTS_AI_MOD: END
	if (!bWait)
		conscript();
}

// This function has been heavily edited for K-Mod
void CvCityAI::AI_doHurry(bool bForce)
{
	PROFILE_FUNC();

	FAssert(!isHuman() || isProductionAutomated());

	const CvPlayerAI& kOwner = GET_PLAYER(getOwner());

	if (kOwner.isBarbarian())
		return;

	if (getProduction() == 0 && !bForce)
		return;

	UnitTypes eProductionUnit = getProductionUnit();
	UnitAITypes eProductionUnitAI = getProductionUnitAI();
	BuildingTypes eProductionBuilding = getProductionBuilding();

	FOR_EACH_ENUM2(Hurry, eHurry)
	{
		if (!canHurry(eHurry))
			continue;

		if (bForce)
		{
			hurry(eHurry);
			break;
		}

		// gold hurry information
		int const iHurryGold = hurryGold(eHurry);
		int iGoldCost = 0;
		if (iHurryGold > 0)
		{
			if (iHurryGold > kOwner.getGold() - kOwner.AI_goldTarget(true))
				continue; // we don't have enough gold for this hurry type.
			int const iGoldTarget = kOwner.AI_goldTarget();
			iGoldCost = iHurryGold;
			if (kOwner.getGold() - iHurryGold >= iGoldTarget)
			{
				iGoldCost *= 100;
				iGoldCost /= 100 + 50 * (kOwner.getGold() - iHurryGold) /
						std::max(iGoldTarget, iHurryGold);
			}
			if (kOwner.isHuman())
				iGoldCost = iGoldCost * 3 / 2;
		}
		//

		// population hurry information
		int const iHurryAngerLength = hurryAngerLength(eHurry);
		int const iHurryPopulation = hurryPopulation(eHurry);

		// <advc.101> Don't whip in cities with revolt chance
		if (iHurryAngerLength >= 3 && (revoltProbability(false, false, true) > 0 ||
			(getNumRevolts() >= GC.getDefineINT(CvGlobals::NUM_WARNING_REVOLTS) &&
			revoltProbability(true, true, true) > 0)))
		{
			continue;
		} // </advc.101>
		int iPopCost = 0;
		int iHappyDiff = 0;
		int iOverflow = 0; // advc.121b
		if (iHurryPopulation > 0)
		{
			if (!isNoUnhappiness())
			{
				iHappyDiff = iHurryPopulation - GC.getDefineINT(CvGlobals::HURRY_POP_ANGER);
				if (iHurryAngerLength > 0 && getHurryAngerTimer() > 1)
				{
					iHappyDiff -= intdiv::uround(
							(kOwner.AI_getFlavorValue(FLAVOR_GROWTH) > 0 ? 4 : 3) *
							getHurryAngerTimer(), iHurryAngerLength);
				}
			}
			int iHappy = happyLevel() - unhappyLevel();
			if (iHappyDiff > 0 && iGoldCost == 0)
			{
				if (iHappy < 0 && iHurryPopulation < -4*iHappy) // don't kill 4 citizens to remove 1 angry citizen.
				{
					if (gCityLogLevel >= 2)
						logBBAI("      City %S whips to reduce unhappiness", getName().GetCString());
					hurry(eHurry);
					return;
				}
			}
			else if (iHappy + iHappyDiff < 0)
				continue; // not enough happiness to afford this hurry

			if (iHappy + iHappyDiff >= 1 && iGoldCost == 0 && foodDifference() < -iHurryPopulation)
			{
				if (gCityLogLevel >= 2)
					logBBAI("      City %S whips to reduce food loss", getName().GetCString());
				hurry(eHurry);
				return;
			}

			iPopCost = AI_citizenSacrificeCost(iHurryPopulation, iHappy,
					GC.getDefineINT(CvGlobals::HURRY_POP_ANGER), iHurryAngerLength);
			iPopCost += std::max(0, 6 * -iHappyDiff) * iHurryAngerLength;

			if (kOwner.isHuman())
				iPopCost = iPopCost * 3 / 2;
			/*  subtract overflow from the cost; but only if we can be confident the
				city isn't being over-whipped. (iHappyDiff has been adjusted above based on the anger-timer) */
			if (iHappyDiff > 0 || isNoUnhappiness() ||
				(iHappy > 1 && (getHurryAngerTimer() <= 1 || iHurryAngerLength == 0)))
			{	/*int iOverflow = (hurryProduction(eHurry) - productionLeft()); // raw overflow
				iOverflow *= getBaseYieldRateModifier(YIELD_PRODUCTION); // limit which multiplier apply to the overflow
				iOverflow /= std::max(1, getBaseYieldRateModifier(YIELD_PRODUCTION, getProductionModifier()));*/
				// <advc.064b> Replacing the above
				hurryOverflow(eHurry, &iOverflow, NULL /* (ignore gold) */, false);
				if(iOverflow > 0)
				{
					// Need to subtract current overflow b/c Slavery isn't causing that
					int iCurrentOverflow = getOverflowProduction();
					if(iCurrentOverflow > 0)
					{
						/*  Extra production modifiers are still to be applied to
							iCurrentOverflow, but generic modifiers are already included. */
						iCurrentOverflow *= getBaseYieldRateModifier(YIELD_PRODUCTION, getProductionModifier());
						iCurrentOverflow /= std::max(1, getBaseYieldRateModifier(YIELD_PRODUCTION));
						iOverflow = std::max(0, iOverflow - iCurrentOverflow);
					} // </advc.064b>
					//iOverflow *= ((kOwner.AI_getFlavorValue(FLAVOR_PRODUCTION) > 0) ? 6 : 4); // value factor
					// <advc.121b> Replacing the above
					int iFlavorBoost = 0;
					if(kOwner.AI_getFlavorValue(FLAVOR_PRODUCTION) > 0)
					{
						iFlavorBoost++;
						/*  Growth also matters in AI_citizenSacrificeCost, but
							not that much. */
						if(kOwner.AI_getFlavorValue(FLAVOR_GROWTH) <= 0 &&
							kOwner.AI_getFlavorValue(FLAVOR_PRODUCTION) > 2)
						{
							iFlavorBoost++;
						}
					}
					iOverflow *= 4 + iFlavorBoost;
					iOverflow /= 4;
					// Will add overflow later // </advc.121b>
					//iPopCost -= iOverflow;
				}
			}
			// convert units from 4x commerce to 1x commerce
			iPopCost /= 4;
		} // advc.121b: Renamed from iTotalCost b/c iOverflow now counted separately
		int iHurryCost = iPopCost + iGoldCost;
		// <advc.064b>
		int iProductionAdded = std::max(0, productionLeft()
				- getCurrentProductionDifference(iPopCost > 0, true,
				false, iPopCost > 0, true)); // </advc.064b>
		if (eProductionUnit != NO_UNIT)
		{
			const CvUnitInfo& kUnitInfo = GC.getInfo(eProductionUnit);

			int iValue = 0;
			if (kOwner.AI_isFinancialTrouble())
			/*{ iTotalCost = std::max(0, iTotalCost); // overflow is not good when it is being used to build units that we don't want.
			} else*/
			// advc: The above meant that we don't hurry (iValue=0, iTotalCost>=0); simpler:
				continue;

			//iValue = std::max(0, productionLeft());
			// advc.064b: Hurry no longer covers the entire productionLeft
			iValue = iProductionAdded;
			switch (eProductionUnitAI)
			{
			case UNITAI_WORKER:
			case UNITAI_SETTLE:
			case UNITAI_WORKER_SEA:
			{
				iValue *= kUnitInfo.isFoodProduction() ? 5 : 4;
				int foo=-1;
				// cf. value of commerce/turn
				iValue += ((eProductionUnitAI == UNITAI_SETTLE &&
						getArea().getNumAIUnits(getOwner(), UNITAI_SETTLE) <= 0 &&
						// advc.121b: Check for local city sites
						kOwner.AI_getNumAreaCitySites(getArea(), foo) > 0) ? 24 : 14) *
						/*  <advc.064b> Second arg for getProductionTurnsLeft was 1,
							perhaps by accident, or so that overflow and chopping production
							are ignored, but that's not going to work anymore.
							2 would still work, but I think we should use the actual
							production turns here - how much earlier are we getting the unit? */
						std::min(getProductionTurnsLeft(eProductionUnit, 0) - 1,
						getProductionNeeded(eProductionUnit)); // </advc.064b>
				break;
			}
			case UNITAI_SETTLER_SEA:
			case UNITAI_EXPLORE_SEA:
				iValue *= kOwner.AI_getNumAIUnits(eProductionUnitAI) == 0 ? 5 : 4;
				break;
			default:
				if (kUnitInfo.getUnitCombatType() == NO_UNITCOMBAT)
				{
					//iValue *= 4;
					/*  <advc.121b> Rarely urgent, suggests that this city doesn't
						have anything to produce, which is why it also shouldn't
						be too fond of overflow. */
					iValue *= 2;
					iOverflow /= 2; // </advc.121b>
				}
				else
				{
					if (AI_isDanger())
						iValue *= 6;
					else if (kUnitInfo.getDomainType() == DOMAIN_SEA &&
						(getArea().getAreaAIType(kOwner.getTeam()) == AREAAI_ASSAULT ||
						getArea().getAreaAIType(kOwner.getTeam()) == AREAAI_ASSAULT_ASSIST ||
						getArea().getAreaAIType(kOwner.getTeam()) == AREAAI_ASSAULT_MASSING))
					{
						iValue *= 5;
					}
					else
					{
						if (getArea().getAreaAIType(kOwner.getTeam()) == AREAAI_DEFENSIVE)
						{
							int iSuccessRating = GET_TEAM(kOwner.getTeam()).AI_getWarSuccessRating();
							iValue *= iSuccessRating < -5 ? (iSuccessRating < -50 ? 6 : 5) : 4;
						}
						else if (kOwner.AI_isDoStrategy(AI_STRATEGY_CRUSH) &&
							(getArea().getAreaAIType(kOwner.getTeam()) == AREAAI_OFFENSIVE ||
							getArea().getAreaAIType(kOwner.getTeam()) == AREAAI_MASSING))
						{
							int iSuccessRating = GET_TEAM(kOwner.getTeam()).AI_getWarSuccessRating();
							//iValue *= iSuccessRating < 35 ? (iSuccessRating < 1 ? 6 : 5) : 4;
							/*  advc.018: Replacing the line above. No need to hurry things
								if we're winning anyway. */
							iValue *= iSuccessRating < 35 ? (iSuccessRating < 1 ? 5 : 3) : 1;
						}
						else
						{
							if (getArea().getAreaAIType(kOwner.getTeam()) == AREAAI_NEUTRAL)
							{
								iValue *= kOwner.AI_unitCostPerMil() >= kOwner.AI_maxUnitCostPerMil(
										area(), AI_buildUnitProb()) ? 0 : 3;
								iOverflow = (2 * iOverflow) / 3; // advc.021b
							} // <advc.121b>
							else if(!kOwner.AI_isFocusWar() &&
								!kOwner.AI_isDoStrategy(AI_STRATEGY_ALERT1) &&
								!kOwner.AI_isDefenseFocusOnBarbarians(getArea()))
							{
								iValue *= 3;
								iOverflow = (iOverflow * 3) / 4;
							} // </advc.121b>
							else iValue *= 4;
						}
					}
				}
				break;
			}
			iValue /= 4 + std::max(0, -iHappyDiff)
					+ 2; // advc.121b: Whip fewer units
			if (iHurryCost < iValue + /* advc.121b: */ iOverflow)
			{
				if (gCityLogLevel >= 2) logBBAI("      City %S (%d) hurries %S. %d pop (%d) + %d gold (%d) to save %d turns. (value %d) (hd %d)", getName().GetCString(), getPopulation(), GC.getInfo(eProductionUnit).getDescription(0), iHurryPopulation, iPopCost, iHurryGold, iGoldCost, getProductionTurnsLeft(eProductionUnit, /* advc.064b: was 1 */ 2), iValue, iHappyDiff);
				hurry(eHurry);
				return;
			}
		}
		else if (eProductionBuilding != NO_BUILDING)
		{
			/*  advc.121b: AI_buildingValue isn't cost-adjusted; need sth. to
				prevent the AI from hurrying every wonder. */
			if(iProductionAdded + iOverflow > iHurryCost)
			{
				const CvBuildingInfo& kBuildingInfo = GC.getInfo(eProductionBuilding);
				int iValue = AI_buildingValue(eProductionBuilding, 0, 0, false,
				/*  advc.121b: No recursion b/c that's for long-term benefits and no
					specialists b/c the city will probably not be able to use them
					right away after the population loss from hurrying */
						false, (iHurryPopulation > 0)) *
				// <advc.064b> Second arg was 1; see comment in the units branch above.
						std::min(getProductionTurnsLeft(eProductionBuilding, 0) - 1,
						getProductionNeeded(eProductionBuilding)); // </advc.064b>
				iValue /= std::max(4, 4 - iHappyDiff) + (iHurryPopulation+1)/2;
				/*	<advc.121b> AI_buildingValue doesn't say if the building is
					immediately useful */
				if(iValue + iOverflow > iHurryCost) // Just for performance
				{
					/*  Buildings with an unconditional happy/health effect don't
						usually have other important abilities */
					int iHappy = kBuildingInfo.getHappiness();
					int iHealth = kBuildingInfo.getHealth();
					if((iHappy > 0 && iHealth <= 0 && happyLevel() > unhappyLevel()) ||
						(iHealth > 0 && iHappy <= 0 && goodHealth() >= badHealth()))
					{
						iValue = 0;
						/*  If the current building isn't really needed, then we
							may not have much use for overflow either. */
						iOverflow /= 2;
					}
				} // </advc.121b>
				if (iValue + iOverflow > iHurryCost)
				{
					if (gCityLogLevel >= 2)
					{
						logBBAI("      City %S (%d) hurries %S. %d pop (%d) + %d gold (%d) to save %d turns with %d building value (%d) (hd %d)", getName().GetCString(), getPopulation(), kBuildingInfo.getDescription(0), iHurryPopulation, iPopCost, iHurryGold, iGoldCost, getProductionTurnsLeft(eProductionBuilding, /* advc.064b: was 1 */ 2), AI_buildingValue(eProductionBuilding), iValue, iHappyDiff);
					}
					hurry(eHurry);
					return;
				}
			}
		}
	}
}

// Improved use of emphasize by Blake, to go with his whipping strategy - thank you!
//Note from Blake:
//Emphasis proved to be too clumsy to manage AI economies,
//as such it's been nearly completely phased out by
//the AI_specialYieldMultiplier system which allows arbitary
//value-boosts and works very well.
//Ideally the AI should never use emphasis.
void CvCityAI::AI_doEmphasize()
{
	PROFILE_FUNC();

	FAssert(!isHuman());
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());
	// BETTER_BTS_AI_MOD, Victory Strategy AI, 03/08/10, jdog5000:
	bool bCultureVictory = kOwner.AI_atVictoryStage(AI_VICTORY_CULTURE2);

	bool bFirstTech = false;
	if (kOwner.getCurrentResearch() != NO_TECH)
		bFirstTech = kOwner.AI_isFirstTech(kOwner.getCurrentResearch());

	int iPopulationRank = findPopulationRank();

	FOR_EACH_ENUM(Emphasize)
	{
		bool bEmphasize = false;
		/*if (GC.getInfo((EmphasizeTypes)iI).getYieldChange(YIELD_FOOD) > 0)
		{}*/
		/*if (GC.getInfo((EmphasizeTypes)iI).getYieldChange(YIELD_PRODUCTION) > 0)
		{}*/ // advc: Empty branches commented out
		if (AI_specialYieldMultiplier(YIELD_PRODUCTION) >= 50)
			continue; // advc

		CvEmphasizeInfo const& kLoopEmphasize = GC.getInfo(eLoopEmphasize); // advc
		if (kLoopEmphasize.getYieldChange(YIELD_COMMERCE) > 0)
		{
			if (bFirstTech)
				bEmphasize = true;
		}
		if (kLoopEmphasize.getCommerceChange(COMMERCE_RESEARCH) > 0)
		{
			if (bFirstTech && !bCultureVictory)
			{
				if (iPopulationRank < kOwner.getNumCities() / 4 + 1)
					bEmphasize = true;
			}
		}
		if (kLoopEmphasize.isGreatPeople())
		{
			int iHighFoodTotal = 0;
			int iHighFoodPlotCount = 0;
			int iHighHammerPlotCount = 0;
			int iHighHammerTotal = 0;
			int iGoodFoodSink = 0;
			int const iFoodPerPop = GC.getFOOD_CONSUMPTION_PER_POPULATION();
			for (WorkablePlotIter it(*this); it.hasNext(); ++it)
			{
				CvPlot const& kPlot = *it;

				int iFood = kPlot.getYield(YIELD_FOOD);
				if (iFood > iFoodPerPop)
				{
					iHighFoodTotal += iFood;
					iHighFoodPlotCount++;
				}
				int iHammers = kPlot.getYield(YIELD_PRODUCTION);
				if (iHammers >= 3 && iHammers + iFood >= 4)
				{
					iHighHammerPlotCount++;
					iHighHammerTotal += iHammers;
				}
				int iCommerce = kPlot.getYield(YIELD_COMMERCE);
				if (iCommerce * 2 + iHammers * 3 > 9)
					iGoodFoodSink += std::max(0, iFoodPerPop - iFood);
			}
			if (iHighFoodTotal + iHighFoodPlotCount - iGoodFoodSink >= foodConsumption(true))
			{
				if (iHighHammerPlotCount < 2 && iHighHammerTotal < getPopulation())
				{
					if (AI_countGoodTiles(true, false, 100, true) < getPopulation())
						bEmphasize = true;
				}
			}
		}
		AI_setEmphasize(eLoopEmphasize, bEmphasize);
	}
}

bool CvCityAI::AI_chooseUnit(UnitAITypes eUnitAI, /* BBAI: */ int iOdds)
{
	UnitTypes eBestUnit;
	if (eUnitAI != NO_UNITAI)
		eBestUnit = AI_bestUnitAI(eUnitAI);
	else eBestUnit = AI_bestUnit(false, NO_ADVISOR, &eUnitAI);

	if (eBestUnit != NO_UNIT)
	{	// <advc.033> Don't build outdated pirates
		if(!isBarbarian() && eUnitAI == UNITAI_PIRATE_SEA)
		{
			TechTypes eTech = GC.getInfo(eBestUnit).getPrereqAndTech();
			if(eTech != NO_TECH &&
				GC.getInfo(eTech).getEra() < GC.getGame().getCurrentEra())
			{
				return false;
			}
		} // </advc.033>

		/*if (iOdds < 0 ||
			getUnitProduction(eBestUnit) > 0 ||
			SyncRandNum(100) < iOdds)*/ // BtS
		// K-Mod. boost the odds based on our completion percentage.
		if (iOdds < 0 || SyncRandSuccess100(iOdds +
			/*	advc.131: Coefficient was 100. Should we re-roll at all once
				production has been started? Same issue in AI_chooseBuilding. */
			(250 * getUnitProduction(eBestUnit)) /
			std::max(1, getProductionNeeded(eBestUnit)))) // K-Mod end
		{
			pushOrder(ORDER_TRAIN, eBestUnit, eUnitAI);
			return true;
		}
	}

	return false;
}

bool CvCityAI::AI_chooseUnit(UnitTypes eUnit, UnitAITypes eUnitAI)
{
	if (eUnit != NO_UNIT)
	{
		pushOrder(ORDER_TRAIN, eUnit, eUnitAI);
		return true;
	}
	return false;
}


bool CvCityAI::AI_chooseDefender()
{
	if (getPlot().plotCheck(PUF_isUnitAIType, UNITAI_CITY_SPECIAL, -1, getOwner()) == NULL)
	{
		if (AI_chooseUnit(UNITAI_CITY_SPECIAL))
			return true;
	}

	if (getPlot().plotCheck(PUF_isUnitAIType, UNITAI_CITY_COUNTER, -1, getOwner()) == NULL)
	{
		if (AI_chooseUnit(UNITAI_CITY_COUNTER))
			return true;
	}

	if (AI_chooseUnit(UNITAI_CITY_DEFENSE))
		return true;

	return false;
}

// advc: Param was vector of pairs "allowedTypes"
bool CvCityAI::AI_chooseLeastRepresentedUnit(UnitAIWeightMap const& kWeights,
	int iOdds) // BBAI
{
	std::vector<std::pair<int, UnitAITypes> > bestTypes; // K-Mod (replacing multimap)
	FOR_EACH_NON_DEFAULT_PAIR(kWeights, UnitAI, int)
	{
		UnitAITypes const eUnitAI = perUnitAIVal.first;
		int iValue = perUnitAIVal.second;
		iValue *= 750 + syncRand().get(250, "AI choose least represented unit",
				eUnitAI); // advc.007
		iValue /= 1 + GET_PLAYER(getOwner()).AI_totalAreaUnitAIs(getArea(), eUnitAI);
		bestTypes.push_back(std::make_pair(iValue, eUnitAI)); // K-Mod
	}
	// <K-Mod>
	std::sort(bestTypes.begin(), bestTypes.end(), std::greater<std::pair<int, UnitAITypes> >());
	std::vector<std::pair<int, UnitAITypes> >::iterator best_it; // </K-Mod>
 	for (best_it = bestTypes.begin(); best_it != bestTypes.end(); ++best_it)
 	{
		if (AI_chooseUnit(best_it->second, iOdds))
		{
			return true;
		}
 	}
	return false;
}

bool CvCityAI::AI_bestSpreadUnit(bool bMissionary, bool bExecutive, int iBaseChance, UnitTypes* eBestSpreadUnit, int* iBestSpreadUnitValue)
{
	CvPlayerAI const& kPlayer = GET_PLAYER(getOwner());
	CvTeamAI const& kTeam = GET_TEAM(getTeam());

	FAssert(eBestSpreadUnit != NULL && iBestSpreadUnitValue != NULL);

	int iBestValue = 0;

	if (bMissionary)
	{
		FOR_EACH_ENUM2(Religion, eReligion)
		{
			if (!isHasReligion(eReligion))
				continue;
			int iHasCount = kPlayer.getHasReligionCount(eReligion);
			FAssert(iHasCount > 0);
			{
				int iChance = (iHasCount > 4) ? iBaseChance :
						(((100 - iBaseChance) / iHasCount) + iBaseChance);
				if (kPlayer.AI_isDoStrategy(AI_STRATEGY_MISSIONARY))
				{
					iChance *= (kPlayer.getStateReligion() == eReligion ? 170 : 65);
					iChance /= 100;
				}
				// BETTER_BTS_AI_MOD (03/08/10, jdog5000, Victory Strategy AI): START
				if (kPlayer.AI_atVictoryStage(AI_VICTORY_CULTURE2))
					iChance += 25; // BETTER_BTS_AI_MOD: END
				else if (!kTeam.hasHolyCity(eReligion) &&
					kPlayer.getStateReligion() != eReligion
                    // doc: religious leaders focus on missionaries even without holy city
                    GC.getInfo(getPersonalityType()).getFlavorValue(FLAVOR_RELIGION) < 2)
				{
					iChance /= 2;
					/*if (kPlayer.isNoNonStateReligionSpread())
						iChance /= 2;*/ // disabled by K-mod
				}
				if (!SyncRandSuccess100(iChance))
					continue;
			}
			int iReligionValue = kPlayer.AI_missionaryValue(eReligion, area());
			if (iReligionValue <= 0)
				continue;

			CvCivilization const& kCiv = getCivilization(); // advc.003w
			for (int i = 0; i < kCiv.getNumUnits(); i++)
			{
				UnitTypes eLoopUnit = kCiv.unitAt(i);
				CvUnitInfo& kUnitInfo = GC.getInfo(eLoopUnit);
				if (kUnitInfo.getReligionSpreads(eReligion) > 0)
				{
					if (canTrain(eLoopUnit))
					{
						int iValue = iReligionValue;
						iValue /= kUnitInfo.getProductionCost();
						if (iValue > iBestValue)
						{
							iBestValue = iValue;
							*eBestSpreadUnit = eLoopUnit;
							*iBestSpreadUnitValue = iReligionValue;
						}
					}
				}
			}
		}
	}

	if (bExecutive)
	{
		FOR_EACH_ENUM2(Corporation, eCorporation)
		{
			if (!isActiveCorporation(eCorporation))
				continue;
			int iHasCount = kPlayer.getHasCorporationCount(eCorporation);
			FAssert(iHasCount > 0);
			{
				int iChance = (iHasCount > 4) ? iBaseChance :
						(((100 - iBaseChance) / iHasCount) + iBaseChance);
				/* if (!kTeam.hasHeadquarters(eCorporation))
					iChance /= 8;*/
				// K-Mod
				if (kTeam.hasHeadquarters(eCorporation))
					iChance += 10;
				else iChance /= 2;
				// K-Mod end
				if (!SyncRandSuccess100(iChance))
					continue;
			}
			int iCorporationValue = kPlayer.AI_executiveValue(eCorporation, area());
			if (iCorporationValue <= 0)
				continue;

			CvCivilization const& kCiv = getCivilization(); // advc.003w
			for (int i = 0; i < kCiv.getNumUnits(); i++)
			{
				UnitTypes eLoopUnit = kCiv.unitAt(i);
				CvUnitInfo& kUnitInfo = GC.getInfo(eLoopUnit);
				if (kUnitInfo.getCorporationSpreads(eCorporation) > 0)
				{
					if (canTrain(eLoopUnit))
					{	/*int iValue = iCorporationValue;
						iValue /= kUnitInfo.getProductionCost();
						int iTotalCount = 0;
						int iPlotCount = 0;
						FOR_EACH_UNITAI(pLoopUnit, kPlayer) {
							if ((pLoopUnit->AI_getUnitAIType() == UNITAI_MISSIONARY) && (pLoopUnit->getUnitInfo().getCorporationSpreads(eCorporation) > 0)) {
							iTotalCount++;
							if (pLoopUnit->at(getPlot()))
								iPlotCount++;
							}
						}
						iCorporationValue /= std::max(1, (iTotalCount / 4) + iPlotCount);*/ // BtS
						// K-Mod
						UnitClassTypes eLoopClass = kCiv.unitClassAt(i);
						int iExistingUnits = kPlayer.getUnitClassCount(eLoopClass) +
								kPlayer.getUnitClassMaking(eLoopClass)/2;
						iCorporationValue *= 3;
						iCorporationValue /= iExistingUnits > 1 ? 2 + iExistingUnits : 3;

						int iValue = iCorporationValue;
						iValue /= kUnitInfo.getProductionCost();
						// K-Mod end

						/*int iCost = std::max(0, GC.getInfo(eCorporation).getSpreadCost() * (100 + GET_PLAYER(getOwner()).calculateInflationRate()));
						iCost /= 100;
						if (kPlayer.getGold() >= iCost) {
							iCost *= GC.getDefineINT("CORPORATION_FOREIGN_SPREAD_COST_PERCENT");
							iCost /= 100;
							if (kPlayer.getGold() < iCost && iTotalCount > 1)
								iCorporationValue /= 2;
						}
						else if (iTotalCount > 1)
						iCorporationValue /= 5;*/ // BtS
						if (iValue > iBestValue)
						{
							iBestValue = iValue;
							*eBestSpreadUnit = eLoopUnit;
							*iBestSpreadUnitValue = iCorporationValue;
						}
					}
				}
			}
		}
	}

	return (*eBestSpreadUnit != NULL);
}

bool CvCityAI::AI_chooseBuilding(int iFocusFlags, int iMaxTurns, int iMinThreshold,
	int iOdds) // BBAI
{
	BuildingTypes eBestBuilding = NO_BUILDING; // advc
	eBestBuilding = AI_bestBuildingThreshold(iFocusFlags, iMaxTurns, iMinThreshold);
	if (eBestBuilding != NO_BUILDING)
	{
		/*if (iOdds < 0 ||
			getBuildingProduction(eBestBuilding) > 0 ||
			SyncRandNum(100) < iOdds)*/ // BBAI
		// K-Mod
		int iRand=0;
		if (iOdds < 0 ||
			(iRand = SyncRandNum(100)) < iOdds ||
			// advc.131: Coefficient was 100; cf. CvCityAI::AI_chooseUnit.
			iRand < iOdds + (250 * getBuildingProduction(eBestBuilding)) /
			std::max(1, getProductionNeeded(eBestBuilding)))
		// K-Mod end
		{
			pushOrder(ORDER_CONSTRUCT, eBestBuilding);
			return true;
		}
	}

	return false;
}

// advc.003j: Replaced by K-Mod code in AI_chooseProduction
/*bool CvCityAI::AI_chooseProject() {
	ProjectTypes eBestProject;
	eBestProject = AI_bestProject();
	if (eBestProject != NO_PROJECT) {
		pushOrder(ORDER_CREATE, eBestProject);
		return true;
	}
	return false;
}*/


bool CvCityAI::AI_chooseProcess(CommerceTypes eCommerceType)
{
	ProcessTypes eBestProcess = AI_bestProcess(eCommerceType);
	if (eBestProcess != NO_PROCESS)
	{
		pushOrder(ORDER_MAINTAIN, eBestProcess);
		return true;
	}
	return false;
}

// Returns true if a citizen was added to a plot...
bool CvCityAI::AI_addBestCitizen(bool bWorkers, bool bSpecialists,
	CityPlotTypes* peBestPlot, // advc.enum: CityPlotTypes
	SpecialistTypes* peBestSpecialist)
{
	PROFILE_FUNC();

	int iGrowthValue = AI_growthValuePerFood(); // K-Mod

	int iBestValue = -1;
	SpecialistTypes eBestSpecialist = NO_SPECIALIST;

	if (bSpecialists)
	{
		// K-Mod. I've deleted a lot of original BtS code for handling forced specialists and replaced it with a simpler method.
		// We allow specialists only if they are either a forced type, or there are no forced types available.
		// (the original code attempted to assign specialists in the same proportions to their force counts.)
		bool bForcedSpecAvailable = false;
		if (isSpecialistForced()) // advc.opt
		{
			FOR_EACH_ENUM(Specialist)
			{
				if (getForceSpecialistCount(eLoopSpecialist) > 0 && isSpecialistValid(eLoopSpecialist, 1))
					bForcedSpecAvailable = true;
			}
		}
		FOR_EACH_ENUM(Specialist)
		{
			if (isSpecialistValid(eLoopSpecialist, 1) &&
				(!bForcedSpecAvailable || getForceSpecialistCount(eLoopSpecialist) > 0))
			{
				int iValue = AI_specialistValue(eLoopSpecialist, false, false, iGrowthValue);
				if (iValue > iBestValue)
				{
					iBestValue = iValue;
					eBestSpecialist = eLoopSpecialist;
				}
			}
		}
	}

	CityPlotTypes eBestPlot = NO_CITYPLOT;
	if (bWorkers)
	{
		for (CityPlotIter it(*this, false); it.hasNext(); ++it)
		{
			CvPlot const& kPlot = *it;
			CityPlotTypes const ePlot = it.currID();
			if (!isWorkingPlot(ePlot) && canWork(kPlot))
			{
				int iValue = AI_plotValue(kPlot, false, false, false, iGrowthValue);
				if (iValue > iBestValue)
				{
					iBestValue = iValue;
					eBestPlot = ePlot;
					eBestSpecialist = NO_SPECIALIST;
				}
			}
		}
	}

	if (eBestSpecialist != NO_SPECIALIST)
	{
		changeSpecialistCount(eBestSpecialist, 1);
		if (peBestPlot != NULL)
		{
			FAssert(peBestSpecialist != NULL);
			*peBestSpecialist = eBestSpecialist;
			*peBestPlot = NO_CITYPLOT;
		}
		return true;
	}
	else if (eBestPlot != NO_CITYPLOT)
	{
		setWorkingPlot(eBestPlot, true);
		if (peBestPlot != NULL)
		{
			FAssert(peBestSpecialist != NULL);
			*peBestSpecialist = NO_SPECIALIST;
			*peBestPlot = eBestPlot;

		}
		return true;
	}

	return false;
}

// Returns true if a citizen was removed from a plot...
bool CvCityAI::AI_removeWorstCitizen(SpecialistTypes eIgnoreSpecialist)
{
	// if we are using more specialists than the free ones we get
	if (extraFreeSpecialists() < 0)
	{
		// does generic 'citizen' specialist exist?
		if (GC.getDEFAULT_SPECIALIST() != NO_SPECIALIST)
		{
			// is ignore something other than generic citizen?
			if (eIgnoreSpecialist != GC.getDEFAULT_SPECIALIST())
			{
				// do we have at least one more generic citizen than we are forcing?
				if (getSpecialistCount((SpecialistTypes)GC.getDEFAULT_SPECIALIST()) >
					getForceSpecialistCount((SpecialistTypes)GC.getDEFAULT_SPECIALIST()))
				{
					// remove the extra generic citzen
					changeSpecialistCount((SpecialistTypes)GC.getDEFAULT_SPECIALIST(), -1);
					return true;
				}
			}
		}
	}

	//bAvoidGrowth = AI_avoidGrowth();
	//bIgnoreGrowth = AI_ignoreGrowth();
	int iGrowthValue = AI_growthValuePerFood();

	int iWorstValue = MAX_INT;
	SpecialistTypes eWorstSpecialist = NO_SPECIALIST;
	CityPlotTypes eWorstPlot = NO_CITYPLOT;

	// if we are using more specialists than the free ones we get
	if (extraFreeSpecialists() < 0)
	{
		FOR_EACH_ENUM(Specialist)
		{
			if (eIgnoreSpecialist == eLoopSpecialist ||
				getSpecialistCount(eLoopSpecialist) <= getForceSpecialistCount(eLoopSpecialist))
			{
				continue; // advc
			}
			int iValue = AI_specialistValue(eLoopSpecialist, true, false, iGrowthValue);
			if (iValue < iWorstValue)
			{
				iWorstValue = iValue;
				eWorstSpecialist = eLoopSpecialist;
				eWorstPlot = NO_CITYPLOT;
			}
		}
	}

	// check all the plots we are working
	for (WorkingPlotIter it(*this, false); it.hasNext(); ++it)
	{
		int iValue = AI_plotValue(*it, true, false, false, iGrowthValue);
		if (iValue < iWorstValue)
		{
			iWorstValue = iValue;
			eWorstSpecialist = NO_SPECIALIST;
			eWorstPlot = it.currID();
		}
	}

	if (eWorstSpecialist != NO_SPECIALIST)
	{
		changeSpecialistCount(eWorstSpecialist, -1);
		// K-Mod. If we had to remove a forced specialist, reduce the force count to match what we did.
		if (getSpecialistCount(eWorstSpecialist) < getForceSpecialistCount(eWorstSpecialist))
			setForceSpecialistCount(eWorstSpecialist, getSpecialistCount(eWorstSpecialist));
		//
		return true;
	}
	else if (eWorstPlot != NO_CITYPLOT)
	{
		setWorkingPlot(eWorstPlot, false);
		return true;
	}

	// if we still have not removed one, then try again, but do not ignore the one we were told to ignore
	if (extraFreeSpecialists() < 0)
	{
		FOR_EACH_ENUM(Specialist)
		{
			if (getSpecialistCount(eLoopSpecialist) <= 0)
				continue; // advc
			int iValue = AI_specialistValue(eLoopSpecialist, true, false, iGrowthValue);
			if (iValue < iWorstValue)
			{
				iWorstValue = iValue;
				eWorstSpecialist = eLoopSpecialist;
				eWorstPlot = NO_CITYPLOT;
			}
		}
	}

	if (eWorstSpecialist != NO_SPECIALIST)
	{
		changeSpecialistCount(eWorstSpecialist, -1);
		return true;
	}

	return false;
}

// This function has been completely rewritten for K-Mod - original code deleted
void CvCityAI::AI_juggleCitizens(/* advc.131d: */ bool bEmphasize)
{
	PROFILE_FUNC();

	int iTotalFreeSpecialists = totalFreeSpecialists();
	bool bAnyForcedSpecs = isSpecialistForced();

	// work out how much food deficit would be acceptable
	int iStarvingAllowance = 0;
	{
		int iFoodLevel = getFood();
		int iFoodToGrow = growthThreshold();
		int iHappinessLevel = happyLevel() - unhappyLevel(0);

		if (AI_isEmphasizeAvoidGrowth() || iHappinessLevel < (isHuman() ? 0 : 1))
		{
			iStarvingAllowance = std::max(0, (iFoodLevel - std::max(1, ((7 * iFoodToGrow) / 10))));
			iStarvingAllowance /= (iHappinessLevel+getEspionageHappinessCounter()/2 >= 0 ? 2 : 1);
		}
	}

	//

	typedef std::pair<int, std::pair<bool,int> > PotentialJob_t; // (value, (isSpecialist, plot/specialist index))
	// I'd like to use std::tuple<int, bool, int>, but it isn't supported by this version of C++
	std::vector<PotentialJob_t> worked_jobs;
	std::vector<PotentialJob_t> unworked_jobs;
	std::vector<std::pair<bool, int> > new_jobs; // jobs assigned by this juggling process

	bool bDone = false;
	bool bAnyNewJobTaken = false; // advc.131d
	int iCycles = 0;
	do
	{
		int iGrowthValue = AI_growthValuePerFood(); // recalcuate on each cycle?
		int iFoodPerTurn = getYieldRate(YIELD_FOOD) - foodConsumption();

		worked_jobs.clear();
		unworked_jobs.clear();

		// populate jobs lists.
		// evaluate plots
		for (CityPlotIter it(*this, false); it.hasNext(); ++it)
		{
			CityPlotTypes const ePlot = it.currID();
			CvPlot const& kPlot = *it;
			if (isWorkingPlot(ePlot))
			{
				int iValue = AI_plotValue(kPlot, false, false, iFoodPerTurn >= 0, iGrowthValue);
				worked_jobs.push_back(PotentialJob_t(iValue, std::make_pair(false, ePlot)));
				// Note: the juggling process works better if worked and unworked plots are compared in the same way.
				// So I'm using 'bRemove = false' here even though we would be removing this worker.
			}
			else if (canWork(kPlot))
			{
				int iValue = AI_plotValue(kPlot, false, false, iFoodPerTurn >= 0, iGrowthValue);
				unworked_jobs.push_back(PotentialJob_t(iValue, std::make_pair(false, ePlot)));
			}
		}

		// check if it is still possible to assign new specialists of types that are forced
		bool bForcedSpecAvailable = false;
		if (bAnyForcedSpecs)
		{
			FOR_EACH_ENUM(Specialist)
			{
				if (getForceSpecialistCount(eLoopSpecialist) > 0 &&
					isSpecialistValid(eLoopSpecialist, 1))
				{
					bForcedSpecAvailable = true;
				}
			}
		}

		// evaluate specialists
		FOR_EACH_ENUM2(Specialist, e)
		{
			if (getSpecialistCount(e) > getForceSpecialistCount(e))
			{
				// don't allow unforced specialists unless none of the forced type are available
				int iValue = (bForcedSpecAvailable && getForceSpecialistCount(e) == 0 ? 0 :
						AI_specialistValue(e, false, false, iGrowthValue));
				worked_jobs.push_back(PotentialJob_t(iValue, std::make_pair(true, e)));
			}
			if (isSpecialistValid(e, 1))
			{
				int iValue = (bForcedSpecAvailable && getForceSpecialistCount(e) == 0 ? 0 :
						AI_specialistValue(e, false, false, iGrowthValue));
				unworked_jobs.push_back(PotentialJob_t(iValue, std::make_pair(true, e)));
				if (getForceSpecialistCount(e) > 0)
					bForcedSpecAvailable = true;
			}
		}

		//
		std::sort(worked_jobs.begin(), worked_jobs.end());
		std::sort(unworked_jobs.begin(), unworked_jobs.end(), std::greater<PotentialJob_t>());
		// if values are equal - prefer to work the specialist job. (perhaps a different city can use the plot)
		// Note: PotentialJob_t is (value, (bSpecialist, index)), and bSpecialist == true is a higher value than bSpecialist == false.

		std::vector<PotentialJob_t>::iterator worked_it = worked_jobs.begin();
		std::vector<PotentialJob_t>::iterator unworked_it = unworked_jobs.begin();
		bool bTakeNewJob = false;

		while (!bTakeNewJob && worked_it != worked_jobs.end() && unworked_it != unworked_jobs.end()
			&& unworked_it->first > worked_it->first)
		{
			bTakeNewJob = true; // default position is the take the new job.

			// Don't take the job if it would make us starve
			int iCurrentFood = worked_it->second.first
				? GET_PLAYER(getOwner()).specialistYield((SpecialistTypes)worked_it->second.second, YIELD_FOOD)
				: getCityIndexPlot((CityPlotTypes)worked_it->second.second)->getYield(YIELD_FOOD);

			int iNextFood = unworked_it->second.first
				? GET_PLAYER(getOwner()).specialistYield((SpecialistTypes)unworked_it->second.second, YIELD_FOOD)
				: getCityIndexPlot((CityPlotTypes)unworked_it->second.second)->getYield(YIELD_FOOD);

			if (iFoodPerTurn >= 0 && iFoodPerTurn + iNextFood - iCurrentFood + iStarvingAllowance < 0)
			{
				bTakeNewJob = false;
			}
			// block removal of free specialists
			else if (worked_it->second.first && !unworked_it->second.first &&
				getSpecialistPopulation() <= iTotalFreeSpecialists)
			{
				bTakeNewJob = false;
			}
			// if forced specialists are still available, don't allow non-forced specialists.
			else if ((bForcedSpecAvailable || (worked_it->second.first && getForceSpecialistCount((SpecialistTypes)worked_it->second.second) > 0)) &&
				unworked_it->second.first && getForceSpecialistCount((SpecialistTypes)unworked_it->second.second) == 0)
			{
				bTakeNewJob = false;
			}
			// don't remove jobs that were assigned by the juggling process
			else if (std::find(new_jobs.begin(), new_jobs.end(), worked_it->second) != new_jobs.end())
			{
				bTakeNewJob = false;
			}
			// finally, don't take the new job if a direct comparison shows that it is not more valuable than the old job.
			// (exception, switching away from zero-value jobs, such as unwanted specialists)
			else if (worked_it->first > 0 && AI_jobChangeValue(unworked_it->second, worked_it->second, false, false, iGrowthValue) <= 0)
			{
				bTakeNewJob = false;
			}

			// If we can't do this job switch, check another option. Loop through worked jobs first, then unworked jobs.
			if (!bTakeNewJob)
			{
				++worked_it;
				if (worked_it == worked_jobs.end() || worked_it->first >= unworked_it->first)
				{
					worked_it = worked_jobs.begin();
					++unworked_it;
				}
			}
			// else we're done.
		}

		if (!bTakeNewJob)
		{
			bDone = true; // no more job swaps. So we're finished.
		}
		else
		{
			bAnyNewJobTaken = true; // advc.131d
			// remove the current job
			if (worked_it->second.first)
			{
				FAssert(getSpecialistCount((SpecialistTypes)worked_it->second.second) > 0);
				changeSpecialistCount((SpecialistTypes)worked_it->second.second, -1);
			}
			else
			{
				FAssert(isWorkingPlot((CityPlotTypes)worked_it->second.second));
				setWorkingPlot((CityPlotTypes)worked_it->second.second, false);
			}

			// assign the new job
			if (unworked_it->second.first)
			{
				FAssert(isSpecialistValid((SpecialistTypes)unworked_it->second.second, 1));
				changeSpecialistCount((SpecialistTypes)unworked_it->second.second, 1);
			}
			else
			{
				FAssert(!isWorkingPlot((CityPlotTypes)unworked_it->second.second));
				setWorkingPlot((CityPlotTypes)unworked_it->second.second, true);
			}
			// add the new job to the new jobs list
			new_jobs.push_back(unworked_it->second);
		}

		if (iCycles > getPopulation() + iTotalFreeSpecialists)
		{
			// This isn't a serious problem. I just want to know how offen it happens.
			//FErrorMsg("juggle citizens failed to find a stable solution.");
			PROFILE("juggle citizen failure");
			bDone = true;
		}
		iCycles++;
	} while (!bDone);
	// <advc.131d>
	if (bEmphasize && isHuman() && !bAnyNewJobTaken && !AI_isStrongEmphasis())
	{
		/*	The player probably wanted there to be a change.
			Let's try harder. */
		AI_setStrongEmphasis(true);
	} // </advc.131d>
	// Record keeping, to test efficiency.
#ifdef LOG_JUGGLE_CITIZENS
	{
		TCHAR message[20];
		_snprintf(message, 20, "%d+%d : %d\n", getPopulation(), iTotalFreeSpecialists, iCycles);
		gDLL->logMsg("juggle_log.txt", message ,false, false);
	}
#endif
}

/*	K-Mod: Estimate the cost of recovery after losing iQuantity number of citizens
	in this city. (units of 4x commerce.) Replacing AI_citizenLossCost in BtS. */
int CvCityAI::AI_citizenSacrificeCost(int iCitLoss, int iHappyLevel, int iNewAnger, int iAngerTimer)
{
	PROFILE_FUNC();

	const CvPlayerAI& kOwner = GET_PLAYER(getOwner());

	iCitLoss = std::min(getPopulation()-1, iCitLoss);
	if (iCitLoss < 1)
		return 0;

	if (isNoUnhappiness())
	{
		iNewAnger = 0;
		iAngerTimer = 0;
	}

	int iYields[NUM_YIELD_TYPES] = {};
	int iYieldWeights[NUM_YIELD_TYPES] =
	{
		9, // food
		7, // production
		4, // commerce
	}; // <advc.121b>
	if(isCapital())
		iYieldWeights[YIELD_COMMERCE]++; // </advc.121b>
	std::vector<int> job_scores;
	int iTotalScore = 0;

	for (int i = 0; i < -iHappyLevel; i++)
		job_scores.push_back(0);

	if ((int)job_scores.size() < iCitLoss)
	{
		for (WorkingPlotIter it(*this, false); it.hasNext(); ++it)
		{
			CvPlot const& kPlot = *it;
			FAssert(kPlot.getWorkingCity() == this);
			// ideally, the plots would be scored using AI_plotValue, but I'm worried that would be too slow.
			// so here's a really rough estimate of the plot value
			int iPlotScore = 0;
			for (int j = 0; j < NUM_YIELD_TYPES; j++)
			{
				int y = kPlot.getYield((YieldTypes)j);
				iYields[j] += y;
				iPlotScore += y * iYieldWeights[j];
			}
			if (kPlot.isImproved() &&
				GC.getInfo(kPlot.getImprovementType()).getImprovementUpgrade() != NO_IMPROVEMENT)
			{
				iYields[YIELD_COMMERCE] += 2;
				iPlotScore += 2 * iYieldWeights[YIELD_COMMERCE];
			}
			/*	<advc.121b> Anticipate improvement. CitySiteEvaluator has proper code
				for this, but don't want to go through all improvements here. */
			if (!kPlot.isImproved() && AI_getWorkersHave() > 0)
				iPlotScore *= 2; // </advc.121b>
			iTotalScore += iPlotScore;
			job_scores.push_back(iPlotScore);
		}
	}
	if ((int)job_scores.size() < iCitLoss)
	{
		FOR_EACH_ENUM(Specialist)
		{
			if (getSpecialistCount(eLoopSpecialist) <= 0)
				continue; // advc
			// very rough..
			int iSpecScore = 0;
			for (int j = 0; j < NUM_YIELD_TYPES; j++)
			{
				int y = kOwner.specialistYield(eLoopSpecialist, (YieldTypes)j)*3/2;
				iYields[j] += y;
				iSpecScore += y * iYieldWeights[j];
			}
			FOR_EACH_ENUM(Commerce)
			{
				int c = kOwner.specialistCommerce(eLoopSpecialist, eLoopCommerce)*3/2;
				iYields[YIELD_COMMERCE] += c;
				iSpecScore += c * iYieldWeights[YIELD_COMMERCE];
			}
			iTotalScore += iSpecScore * getSpecialistCount(eLoopSpecialist);
			job_scores.resize(job_scores.size() +
					getSpecialistCount(eLoopSpecialist), iSpecScore);
		}
	}

	if ((int)job_scores.size() < iCitLoss)
	{
		FErrorMsg("Not enough job data to calculate citizen loss cost.");
		int iBogusData = (1+GC.getFOOD_CONSUMPTION_PER_POPULATION()) * iYieldWeights[YIELD_FOOD];
		job_scores.resize(iCitLoss, iBogusData);
		iTotalScore += iBogusData;
	}

	FAssert((int)job_scores.size() >= iCitLoss);
	std::partial_sort(job_scores.begin(), job_scores.begin()+iCitLoss, job_scores.end());
	int iAverageScore = intdiv::round(iTotalScore, job_scores.size());

	int iWastedFood = -healthRate();
	int iTotalFood = getYieldRate(YIELD_FOOD) - iWastedFood;

	// calculate the total cost-per-turn from missing iCitLoss citizens.
	int iBaseCostPerTurn = 0;
	for (int j = 0; j < NUM_YIELD_TYPES; j++)
	{
		if (iYields[j] > 0)
			iBaseCostPerTurn += 4 * iYields[j] * AI_yieldMultiplier((YieldTypes)j) * kOwner.AI_yieldWeight((YieldTypes)j) / 100;
	}
	// reduce value of food used for production - otherwise our citizens might be overvalued due to working extra food.
	if (isFoodProduction())
	{
		int iExtraFood = iTotalFood - getPopulation() * GC.getFOOD_CONSUMPTION_PER_POPULATION();
		iExtraFood = std::min(iExtraFood, iYields[YIELD_FOOD]*AI_yieldMultiplier(YIELD_FOOD)/100);
		iBaseCostPerTurn -= 4 * iExtraFood * (kOwner.AI_yieldWeight(YIELD_FOOD)-kOwner.AI_yieldWeight(YIELD_PRODUCTION)); // note that we're keeping a factor of 100.
	}

	int iCost = 0; // accumulator for the final return value
	int iScoreLoss = 0;
	for (int i = 0; i < iCitLoss; i++)
	{
		// since the score estimate is very rough, I'm going to flatten it out a bit by combining it with the average score
		job_scores[i] = (2*job_scores[i] + iAverageScore + 2)/3;
		iScoreLoss += job_scores[i];
	}

	for (int i = iCitLoss; i > 0; i--)
	{
		int iFoodLoss = kOwner.getGrowthThreshold(getPopulation() - i) *
				(105 - getMaxFoodKeptPercent()) / 100;
		int iFoodRate = iTotalFood - (iScoreLoss * AI_yieldMultiplier(YIELD_FOOD) * iYields[YIELD_FOOD]
				/*  advc.121b: Round up and then some. Err on the side of under-
					estimating the food rate. */
				+ (2 * 100 * iTotalScore) / 3) /
				std::max(1, iTotalScore * 100);
		iFoodRate -= (getPopulation() - i) * GC.getFOOD_CONSUMPTION_PER_POPULATION();
		iFoodRate += std::min(iWastedFood, i);
		// if we're at the happiness cap, assume we've got some spare food that we're not currently working.
		iFoodRate += iHappyLevel <= 0 ? i : 0;

		int iRecoveryTurns = iFoodRate > 0 ? (iFoodLoss+iFoodRate-1) / iFoodRate : iFoodLoss;

		int iCostPerTurn = iBaseCostPerTurn;
		iCostPerTurn *= iScoreLoss;
		iCostPerTurn /= std::max(1, iTotalScore * 100);

		// extra food from reducing the population:
		iCostPerTurn -= 4 * (std::min(iWastedFood, i) +
				i*GC.getFOOD_CONSUMPTION_PER_POPULATION()) *
				kOwner.AI_yieldWeight(YIELD_FOOD)/100;
		iCostPerTurn += 2*i; // just a little bit of extra cost, to show that we care...

		FAssert(iRecoveryTurns > 0); // iCostPerTurn <= 0 is possible, but it should be rare

		// recovery isn't complete if the citizen is still angry
		iAngerTimer -= iRecoveryTurns;
		if (iAngerTimer > 0 && iHappyLevel + i - iNewAnger < 0)
		{
			iCost += iAngerTimer * GC.getFOOD_CONSUMPTION_PER_POPULATION() * 4 * kOwner.AI_yieldWeight(YIELD_FOOD) / 100;
			iRecoveryTurns += iAngerTimer;
		}

		iCost += iRecoveryTurns * iCostPerTurn;

		iScoreLoss -= job_scores[i-1];
	}
	// if there is any anger left over after regrowing, we might as well count some cost for that too.
	if (iAngerTimer > 0 && iHappyLevel - 1 - iNewAnger < 0)
	{
		int iGrowthTime = std::max(1, iTotalFood - getPopulation()*GC.getFOOD_CONSUMPTION_PER_POPULATION()); // just the food rate here
		iGrowthTime = (kOwner.getGrowthThreshold(getPopulation()) - getFood() + iGrowthTime - 1)/iGrowthTime; // now it's the time.

		iAngerTimer -= iGrowthTime;
		if (iAngerTimer > 0)
		{
			int iCostPerTurn = iBaseCostPerTurn;

			iCostPerTurn *= iAverageScore * (iNewAnger + 1 - iHappyLevel);
			iCostPerTurn /= std::max(1, iTotalScore * 100);

			iCostPerTurn += (iNewAnger + 1 - iHappyLevel) * GC.getFOOD_CONSUMPTION_PER_POPULATION() * 4 * kOwner.AI_yieldWeight(YIELD_FOOD) / 100;

			FAssert(iCostPerTurn > 0 && iAngerTimer > 0);

			iCost += iCostPerTurn * iAngerTimer;
		}
	}
	if (kOwner.AI_getFlavorValue(FLAVOR_GROWTH) > 0)
	{
		iCost *= 120 + kOwner.AI_getFlavorValue(FLAVOR_GROWTH);
		iCost /= 100;
	}

	return iCost;
}

/*	advc: K-Mod formula that was used in two places. I also want to use it in a
	third place. */
int CvCityAI::AI_citizenValue() const
{
	/*	advc.erai (note): Kek-Mod normalizes the era here, but
		I don't think we should assume (implicitly) that mods with fewer eras
		have more perks (like extra tile yields) per era. */
	return 6 + GET_PLAYER(getOwner()).getCurrentEra();
}

//  advc.enum: Param was a pointer to a CvPlot member array of yields.
//	Replaced all uses of that param with kPlot.getYield(YieldTypes), which,
//	due to inlining, should be just as fast.
// Never mind - it's unused anyway.
/*bool CvCityAI::AI_potentialPlot(CvPlot const& kPlot) const
{
	int iNetFood = kPlot.getYield(YIELD_FOOD) - GC.getFOOD_CONSUMPTION_PER_POPULATION();
	if (iNetFood < 0)
	{
 		if (kPlot.getYield(YIELD_FOOD) == 0)
		{
			if (kPlot.getYield(YIELD_PRODUCTION) + kPlot.getYield(YIELD_COMMERCE) < 2)
				return false;
		}
		else
		{
			if (kPlot.getYield(YIELD_PRODUCTION) + kPlot.getYield(YIELD_COMMERCE) == 0)
				return false;
		}
	}
	return true;
}

bool CvCityAI::AI_foodAvailable(int iExtra) const
{
	PROFILE_FUNC();

	int iFoodCount = 0;

	bool abPlotAvailable[NUM_CITY_PLOTS] = { false };
	for (CityPlotIter it(*this); it.hasNext(); ++it)
	{
		CityPlotTypes const ePlot = it.currID();
		CvPlot const& kPlot = *it;
		if (ePlot == CITY_HOME_PLOT)
			iFoodCount += kPlot.getYield(YIELD_FOOD);
		else if (it->getWorkingCity() == this && AI_potentialPlot(kPlot))
			abPlotAvailable[ePlot] = true;
	}

	int iPopulation = (getPopulation() + iExtra);
	while (iPopulation > 0)
	{
		int iBestPlot = CITY_HOME_PLOT;
		int iBestValue = 0;
		FOR_EACH_ENUM(CityPlot)
		{
			if (abPlotAvailable[eLoopCityPlot])
			{
				int iValue = getCityIndexPlot(eLoopCityPlot)->getYield(YIELD_FOOD);
				if (iValue > iBestValue)
				{
					iBestValue = iValue;
					iBestPlot = eLoopCityPlot;
				}
			}
		}

		if (iBestPlot != CITY_HOME_PLOT)
		{
			iFoodCount += iBestValue;
			abPlotAvailable[iBestPlot] = false;
		}
		else break;

		iPopulation--;
	}

	FOR_EACH_ENUM(Specialist)
	{
		iFoodCount += (GC.getInfo(eLoopSpecialist).getYieldChange(YIELD_FOOD) *
				getFreeSpecialistCount(eLoopSpecialist));
	}

	if (iFoodCount < foodConsumption(false, iExtra))
		return false;

	return true;
}*/

/*	K-Mod: I've rewritten large chunks of this function.
	I've deleted much of the original code, rather than commenting it;
	just to keep things a bit tidier and clearer.
	Note. I've changed the scale to match the building evaluation code: ~4x commerce. */
/*	advc.make: Array types changed from short to int to avoid problems with /W4.
	(Ideally 'typedef yield_t char' would be used for all yields ...) */
int CvCityAI::AI_yieldValue(int* piYields, int* piCommerceYields, bool bRemove,
	bool bIgnoreFood, bool bIgnoreStarvation, bool bWorkerOptimization, int iGrowthValue) const
{
	PROFILE_FUNC();
	const CvPlayerAI& kOwner = GET_PLAYER(getOwner());
	//const int iBaseProductionValue = 9; // (K-Mod: was 7 before I removed the averageCommerceExchange factor from the commerce values.)
	/*  advc.121b: So I guess the K-Mod line above sets the priority as in BtS.
		Let's set a lower priority then, in part to even out the use of Slavery. */
	const int iBaseProductionValue = 8;
	const int iBaseCommerceValue = 4;

	bool const bEmphasizeFood = AI_isEmphasizeYield(YIELD_FOOD);
	bool const bFoodIsProduction = isFoodProduction();
	//bool bCanPopRush = GET_PLAYER(getOwner()).canPopRush();

	// a kludge to handle the NULL yields easily.
	int aiZeroYields[NUM_YIELD_TYPES] = {};
	if (piYields == NULL)
		piYields = aiZeroYields;

	int const iBaseProductionModifier = getBaseYieldRateModifier(YIELD_PRODUCTION);
	int const iExtraProductionModifier = getProductionModifier();
	int iProductionTimes100 = piYields[YIELD_PRODUCTION] *
			(iBaseProductionModifier + iExtraProductionModifier);
	int const iCommerceYieldTimes100 = piYields[YIELD_COMMERCE] *
			getBaseYieldRateModifier(YIELD_COMMERCE);
	int const iFoodYieldTimes100 = piYields[YIELD_FOOD] *
			getBaseYieldRateModifier(YIELD_FOOD);
	int const iFoodYield = iFoodYieldTimes100/100;

	int iValue = 0; // total value

	// Commerce
	int iCommerceValue = 0;
	ProcessTypes eProcess = getProductionProcess();

	FOR_EACH_ENUM2(Commerce, eCommerce)
	{
		int iCommerceTimes100 = iCommerceYieldTimes100 *
				kOwner.getCommercePercent(eCommerce) / 100;
		if (piCommerceYields != NULL)
			iCommerceTimes100 += piCommerceYields[eCommerce] * 100;

		iCommerceTimes100 *= getTotalCommerceRateModifier(eCommerce);
		iCommerceTimes100 /= 100;

		//FAssert(iCommerceTimes100 >= 0);

		if (eProcess != NO_PROCESS)
		{
			iCommerceTimes100 += (GC.getInfo(getProductionProcess()).
					getProductionToCommerceModifier(eCommerce) * iProductionTimes100) / 100;
		}
		if (iCommerceTimes100 != 0)
		{
			// (Should we still use this with bWorkerOptimization?)
			int iCommerceWeight = kOwner.AI_commerceWeight(eCommerce, this);
			if (AI_isEmphasizeCommerce(eCommerce))
				iCommerceWeight *= 2 + /* advc.131d: */ (AI_isStrongEmphasis() ? 1 : 0);
			if (!bWorkerOptimization && eCommerce == COMMERCE_CULTURE &&
				getCultureLevel() <= 1)
			{
				// bring on the artists
				if (getCommerceRateTimes100(COMMERCE_CULTURE)
					- (bRemove ? iCommerceTimes100 : 0) < 100)
				{
					iCommerceValue += 20 * (iCommerceTimes100 > 0 ? 1 : -1);
				}
				iCommerceWeight = std::max(iCommerceWeight, 200);
			}

			iCommerceValue += iCommerceWeight * iCommerceTimes100 * iBaseCommerceValue
					//* GET_PLAYER(getOwner()).AI_averageCommerceExchange((CommerceTypes)iI) / 1000000;
					/*	K-Mod. (averageCommerceExchange should be part of commerceWeight
						if we want it, and we probably don't want it anyway.) */
					/ 10000;
		}
	}

	// Production
	int iProductionValue = 0;
	if (eProcess == NO_PROCESS)
	{
		if (bFoodIsProduction)
			iProductionTimes100 += iFoodYieldTimes100;

		iProductionValue += iProductionTimes100 * iBaseProductionValue / 100;
		// If city has more than enough food, but very little production, add large value to production
		// Particularly helps coastal cities with plains forests
		// (based on BBAI code)
		if (!bWorkerOptimization && iProductionTimes100 > 0 && !bFoodIsProduction && isProduction())
		{
			if (!isHuman() || AI_isEmphasizeYield(YIELD_PRODUCTION) ||
				(!bEmphasizeFood && !AI_isEmphasizeYield(YIELD_COMMERCE) &&
				!AI_isEmphasizeGreatPeople()))
			{
				/*	don't worry about minimum production if there is any hurry type
					available for us. If we need the productivity, we can just buy it. */
				bool bAnyHurry = false;
				/*	advc.121: I don't think a human will want to hurry production
					when setting a city to "emphasize production" */
				if (!isHuman())
				{
					for (HurryTypes i = (HurryTypes)0;
						!bAnyHurry && i < GC.getNumHurryInfos(); i=(HurryTypes)(i+1))
					{
						bAnyHurry = kOwner.canHurry(i);
					}
				}
				if (!bAnyHurry &&
					foodDifference(false) - (bRemove ? iFoodYield : 0) >=
					GC.getFOOD_CONSUMPTION_PER_POPULATION())
				{
					/*if (getYieldRate(YIELD_PRODUCTION) - (bRemove ? iProductionTimes100/100 : 0)  < 1 + getPopulation()/3)
						iValue += 60 + iBaseProductionValue * iProductionTimes100 / 100;*/
					int iCurrentProduction = getCurrentProductionDifference(true, false)
							- (bRemove ? iProductionTimes100/100 : 0);
					if (iCurrentProduction < 1 + getPopulation()/3)
					{
						iValue += 5 * iBaseProductionValue *
								std::min(iProductionTimes100,
								(1 + getPopulation()/3 - iCurrentProduction)*100) / 100;
					}
				}
			}
		}
		if (!isProduction() && !isHuman())
			iProductionValue /= 2;
	}

	int iSlaveryValue = 0;
	int iFoodGrowthValue = 0;
	if (!bIgnoreFood && iFoodYield != 0)
	{
		if (iGrowthValue < 0)
			iGrowthValue = AI_growthValuePerFood();
		// <k146>
		if (bEmphasizeFood)
		{
			iGrowthValue += 8 // in addition to other effects.
					+ (AI_isStrongEmphasis() ? 3 : 0); // advc.131d
		} // </k146>
		// tiny food factor, to ensure that even when we don't want to grow,
		// we still prefer more food if everything else is equal
		iValue += bFoodIsProduction ? 0 : (iFoodYieldTimes100+50)/100;

		int const iFoodPerTurn = getYieldRate(YIELD_FOOD) - foodConsumption() -
				(bRemove? iFoodYield : 0);
		int const iFoodLevel = getFood();
		int const iFoodToGrow = growthThreshold();
		int const iPopulation = getPopulation();
		/*	(I'd like to lower this when evaluating plots we might switch to -
			but currently there is no way to know we're doing that.) */
		int const iAdjustedFoodPerTurn = iFoodPerTurn;

		int iHealthLevel = goodHealth() - badHealth();
		int iHappinessLevel = (isNoUnhappiness() ?
				std::max(3, iHealthLevel + 5) : happyLevel() - unhappyLevel(0));

		// if we not human, allow us to starve to half full if avoiding growth
		if (!bIgnoreStarvation)
		{
			int iStarvingAllowance = 0;
			if (AI_isEmphasizeAvoidGrowth() || iHappinessLevel < (isHuman() ? 0 : 1))
			{
				iStarvingAllowance = std::max(0,
						iFoodLevel - std::max(1, (7 * iFoodToGrow) / 10));
				iStarvingAllowance /= 1 +
						(iHappinessLevel+getEspionageHappinessCounter()/2 >= 0 ? 1 : 0) +
						(iHealthLevel+getEspionageHealthCounter() > 0 ? 1 : 0);
			}

			// if still starving
			if (iFoodPerTurn + iStarvingAllowance < 0)
			{
				// if working plots all like this one will save us from starving
				//if (((bReassign?1:0)+iExtraPopulationThatCanWork+std::max(0, getSpecialistPopulation() - totalFreeSpecialists())) * iFoodYield >= -iFoodPerTurn)
				/*if ((iExtraPopulationThatCanWork+std::max(bReassign?1:0, getSpecialistPopulation() - totalFreeSpecialists())) * iFoodYield >= -iFoodPerTurn + (bReassign ? std::min(iFoodYield, iConsumtionPerPop) : 0))
				{
					iValue += 2048;
				}*/

				// value food high, but not forced
				//iValue += 36 * std::min(iFoodYield, -iFoodPerTurn+(bReassign ? iConsumtionPerPop : 0));
				iValue += (iHappinessLevel >= 0 ? 2: 1)*std::max(iGrowthValue, iBaseProductionValue*3) * std::min(iFoodYield, -(iFoodPerTurn + iStarvingAllowance));
				// note. iGrowthValue only counts unworked plots - so it isn't entirely suitable for this. Hence the arbitrary minimum value.
			}
		}

		// if food isn't production, then adjust for growth
		if ((bWorkerOptimization || !bFoodIsProduction) && !AI_isEmphasizeAvoidGrowth())
		{
			/*	only do relative checks on food if we want to grow AND do not emph food.
				the emph food case will just give a big boost
				to all food under all circumstances */
			//if (bWorkerOptimization || (!bIgnoreGrowth && !bEmphasizeFood))
			if (iGrowthValue > 0)
			{
				/*  K-Mod. Happiness boost we expect before we grow.
					(originally, the boost was added directly to iHappyLevel) */
				int iFutureHappy = 0;

				// we have less than 10 extra happy, do some checks to see if we can increase it
				//if (iHappinessLevel < 10)
				/*	K-Mod. make it 5.
					We shouldn't really be worried about growing 10 pop all at once... */
				if (iHappinessLevel < 5)
				{
					/*	if we have anger becase no military, do not count it,
						on the assumption that it will be remedied soon,
						and that we still want to grow */
					if (getMilitaryHappinessUnits() == 0 && kOwner.getNumCities() > 2)
					{
						iHappinessLevel += (//GC.getDefineINT(CvGlobals::NO_MILITARY_PERCENT_ANGER)
								GET_TEAM(getTeam()).getNoMilitaryAnger() * // advc.500c
								(iPopulation + 1)) / GC.getPERCENT_ANGER_DIVISOR();
					}

					int const kMaxHappyIncrease = 2;

					// if happy is large enough so that it will be over zero after we do the checks
					if (iHappinessLevel + kMaxHappyIncrease > 0)
					{
						/*	not including reassignment penalty
							because it's better to overestimate food here. */
						int iNewFoodPerTurn = iFoodPerTurn + iFoodYield;
						int iApproxTurnsToGrow = (iNewFoodPerTurn <= 0 ? MAX_INT :
								((iFoodToGrow - iFoodLevel + iNewFoodPerTurn - 1) / iNewFoodPerTurn));

						// do we have hurry anger?
						int iHurryAngerTimer = getHurryAngerTimer();
						if (iHurryAngerTimer > 0)
						{
							int iTurnsUntilAngerIsReduced = iHurryAngerTimer % flatHurryAngerLength();

							// angry population is bad but if we'll recover by the time we grow...
							if (iTurnsUntilAngerIsReduced <= iApproxTurnsToGrow)
								iFutureHappy++;
						}

						// do we have conscript anger?
						int iConscriptAngerTimer = getConscriptAngerTimer();
						if (iConscriptAngerTimer > 0)
						{
							int iTurnsUntilAngerIsReduced = iConscriptAngerTimer % flatConscriptAngerLength();

							// angry population is bad but if we'll recover by the time we grow...
							if (iTurnsUntilAngerIsReduced <= iApproxTurnsToGrow)
								iFutureHappy++;
						}

						// do we have defy resolution anger?
						int iDefyResolutionAngerTimer = getDefyResolutionAngerTimer();
						if (iDefyResolutionAngerTimer > 0)
						{
							int iTurnsUntilAngerIsReduced = iDefyResolutionAngerTimer %
									flatDefyResolutionAngerLength();

							// angry population is bad but if we'll recover by the time we grow...
							if (iTurnsUntilAngerIsReduced <= iApproxTurnsToGrow)
								iFutureHappy++;
						}
					}
				}
				/*  advc.121: Want the AI to grow cities a bit more aggressively
					(but I don't quite know what I'm doing). Surely, in the
					time that the city grows four times, we should be able to
					procure an extra happiness. If not, the bonus to iFutureHappy
					should go away once we near the cap (because iHappinessLevel
					will drop under 4), and food can be de-emphasized. */
				iFutureHappy += iHappinessLevel / 4;

				if (bEmphasizeFood)
				{
					//If we are emphasize food, pay less heed to caps.
					iHealthLevel += 5;
					iFutureHappy += 3; // k146: was +=2
					// <advc.131d>
					if (AI_isStrongEmphasis())
					{
						iHealthLevel++;
						iFutureHappy++;
					} // </advc.131d>
				}

				bool const bBarFull = (iFoodLevel + iAdjustedFoodPerTurn >
						iFoodToGrow * 80 / 100);

				int iPopToGrow = std::max(0, iHappinessLevel+iFutureHappy);
				int iGoodTiles = AI_countGoodTiles(iHealthLevel > 0, true, 50,
						// K-Mod comment: so that we pretend the plots are already improved
						// advc.121: Don't do that if no worker is assigned
						isHuman() || AI_getWorkersHave() > 0);
				iGoodTiles += AI_countGoodSpecialists(iHealthLevel > 0);

				if (!bEmphasizeFood)
				{
					iPopToGrow = std::min(iPopToGrow,
							iGoodTiles + (bWorkerOptimization ? 1 : 0));
					// <k146>
					if (iPopulation < 3 && iHappinessLevel+iFutureHappy > 0)
						iPopToGrow = std::max(iPopToGrow, 1); // </k146>
					if (AI_isEmphasizeYield(YIELD_PRODUCTION) || AI_isEmphasizeGreatPeople())
					{
						iPopToGrow = std::min(iPopToGrow, 2
								- (AI_isStrongEmphasis() ? 1 : 0)); // advc.131d
					}
					else if (AI_isEmphasizeYield(YIELD_COMMERCE))
					{
						iPopToGrow = std::min(iPopToGrow, 3
								- (AI_isStrongEmphasis() ? 1 : 0)); // advc.131d
					}
				}

				// if we have growth pontential, then get the food bar close to full
				bool bFillingBar = false;
				if (iPopToGrow == 0 && iHappinessLevel >= 0 &&
					iGoodTiles >= 0 && iHealthLevel >= 0)
				{
					if (!bBarFull)
					{
						//if (AI_specialYieldMultiplier(YIELD_PRODUCTION) < 50)
						{
							bFillingBar = true;
						}
					}
				}

				/*	We don't want to count growth value for tiles with nothing else to contribute.
					But since AI_yieldValue is used for AI_jobChangeValue,
					we can't assume that we're evaluating a plot. */
				// (placeholder, just in case we restore this kind of check in the future)
				bool const bRelativeComparison = true;
				if ((iPopToGrow > 0 || bFillingBar) &&
					(bRelativeComparison ||
					iFoodYield > GC.getFOOD_CONSUMPTION_PER_POPULATION() ||
					iProductionValue > 0 || iCommerceValue > 0))
				{
					if (bFillingBar)
					{
						iGrowthValue = iGrowthValue * iFoodToGrow /
								std::max(1, 2*iFoodToGrow + iFoodLevel + iAdjustedFoodPerTurn);
					}
					if (iHealthLevel < (bFillingBar ? 0 : 1))
						iGrowthValue = iGrowthValue * 2/3;

					//iFoodGrowthValue = iFoodYield * iFactorPopToGrow;
					/*	K-Mod. iGrowthValue is the initial value per piece of food,
						but the value decreases by iDevalueRate for each piece.
						Think of the integral with respect to x of
						iGrowthValue * (100 - iDevalueRate*(iAdjustedFoodPerTurn+x))/100. */
					int iDevalueRate = 0;
					if (!bEmphasizeFood)
					{
						if (bFillingBar)
						{
							iDevalueRate = 25 + 15 *
									(iFoodLevel + iAdjustedFoodPerTurn) / iFoodToGrow;
						}
						else // k146: was 20-...
							iDevalueRate = 18 - std::min(5, iPopToGrow)*3;
						if (iHealthLevel < 1)
							iDevalueRate += 5;
					}
					// maximum value for this amount of food.
					int iBestFoodYield = std::max(0,
							std::min(iFoodYield, 100/std::max(1, iDevalueRate)
							- iAdjustedFoodPerTurn));
					iFoodGrowthValue = iBestFoodYield * iGrowthValue *
							(100 - iDevalueRate*iAdjustedFoodPerTurn) / 100;
					iFoodGrowthValue -= iBestFoodYield * iBestFoodYield *
							iDevalueRate * iGrowthValue / 200;
					FAssert(iFoodGrowthValue >= 0);
					// K-Mod end
				}
			}

			// Slavery evaluation
			// K-Mod. Rescaled values and conditions.
			//if (!bWorkerOptimization && isProduction() && kOwner.canPopRush() && getHurryAngerTimer() <= std::min(3,getPopulation()/2)+2*iHappinessLevel) // K-Mod
			// k146: Replacing the above
			if (!bWorkerOptimization && isProduction() &&
				/*kOwner.*/canPopRush() && // advc.912d
				iHappinessLevel >= 0)
			{
				//iSlaveryValue = 30 * 14 * std::max(0, aiYields[YIELD_FOOD] - ((iHealthLevel < 0) ? 1 : 0));
				int iProductionPerPop = 0;
				FOR_EACH_ENUM2(Hurry, eHurry)
				{
					if (kOwner.canHurry(eHurry) /* advc.912d: */ || canPopRush())
					{
						iProductionPerPop = std::max(iProductionPerPop,
								GC.getGame().getProductionPerPopulation(eHurry)
								// Don't use modifiers weights, because slavery usage is erratic.
								/* *iBaseProductionModifier / 100*/);

					}
				}
				FAssert(iProductionPerPop > 0);
				/*
				// Note: '80' means that we're only counting 90% of the potential production, because slavery require careful micromangement to get 100% of the value.
				iSlaveryValue = 80 * iProductionPerPop * iBaseProductionValue * std::max(0, iFoodYield - ((iHealthLevel < 0) ? 1 : 0));
				iSlaveryValue /= std::max(10*100, (growthThreshold() * (100 - getMaxFoodKeptPercent())));
				iSlaveryValue *= 100;
				iSlaveryValue /= getHurryCostModifier(true);
				iSlaveryValue *= iConsumtionPerPop * 2;
				//iSlaveryValue /= iConsumtionPerPop * 2 + std::max(0, iAdjustedFoodDifference);
				iSlaveryValue /= iConsumtionPerPop * 2 + std::max(0, iAdjustedFoodPerTurn - iConsumtionPerPop * iHappinessLevel);
				*/
				/*	<k146> Replacing the old calculation above:
					Use the same 'devalue rate' system as we used for growth value earlier.
					Ideally, we'd try to take our infrastructure needs into account.
					(ie. how much do we still need to build.) */

				// the factor of 100 is removed at the end.
				int iWhipValue = 100 * iProductionPerPop * iBaseProductionValue;

				int iDevalueRate = 0;
				if (!bEmphasizeFood && !isNoUnhappiness())
				{
					/*	What we really care about is how many turns it will take
						to grow the population lost from whipping.
						But that calculation isn't easy
						(given that number of turns will depend on which plots we choose to work
						potentially resulting in circular reasoning.)
						So we're just going to do some ad hoc calculation instead. */
					iDevalueRate = std::max(0, 10 + getHurryAngerTimer() *
							// 1*timer for size 1. 1/3 * in limit.
							(3 + iPopulation) / (1 + 3 * iPopulation) - iHappinessLevel * 3);

					if (iHealthLevel < 0)
						iDevalueRate += 5;
				}
				// maximum value for this amount of food.
				int iBestFoodYield = std::max(0, std::min(iFoodYield,
						100 / std::max(1, iDevalueRate) - iAdjustedFoodPerTurn));
				iSlaveryValue = iBestFoodYield * iWhipValue *
						(100 - iDevalueRate * iAdjustedFoodPerTurn) / 100;
				iSlaveryValue -= iBestFoodYield * iBestFoodYield *
						iDevalueRate * iWhipValue / 200;

				iSlaveryValue *= 100;
				iSlaveryValue /= getHurryCostModifier(true);
				iSlaveryValue /= std::max(10 * 100, growthThreshold() *
						(100 - getMaxFoodKeptPercent()));

				FAssert(iSlaveryValue >= 0); // </k146>
			}
		}
	}

	/*	Note: iSlaveryValue use to be counted in the production section.
		(There are argument for and against - but this is easier.) */
	int iFoodValue = iFoodGrowthValue;

	if (iSlaveryValue > iFoodGrowthValue)
	{
		//iFoodValue = (iSlaveryValue + iFoodGrowthValue)/2; // Use the average - to account for the fact that we won't always be making use of slavery.
		// advc.121b: Replacing the above. We'll only sometimes use Slavery.
		iFoodValue = (iSlaveryValue + 2 * iFoodGrowthValue) / 3;
	}

	/*	Lets have some fun with the multipliers, this basically bluntens the
		impact of massive bonuses..... */

	/*	normalize the production... this allows the system to account for rounding
		and such while preventing an "out to lunch smoking weed" scenario with
		unusually high transient production modifiers.
		Other yields don't have transient bonuses in quite the same way. */

	/*	Rounding can be a problem, particularly for small commerce amounts.
		Added safeguards to make sure commerce is counted, even if just a tiny amount. */
	if (AI_isEmphasizeYield(YIELD_PRODUCTION))
	{
		int const iMultPercent = 140 // was 130
				+ (AI_isStrongEmphasis() ? 25 : 0); // advc.131d
		iProductionValue *= iMultPercent;
		iProductionValue /= 100;
		if (bFoodIsProduction)
		{
			iFoodValue *= iMultPercent;
			iFoodValue /= 100;
		}
	}
	else if (iProductionValue > 0 && AI_isEmphasizeYield(YIELD_COMMERCE))
	{
		iProductionValue *= 75
				- (AI_isStrongEmphasis() ? 8 : 0); // advc.131d
		iProductionValue /= 100;
		iProductionValue = std::max(1, iProductionValue);
	}

	if (AI_isEmphasizeYield(YIELD_FOOD))
	{
		if (!bFoodIsProduction)
		{
			iFoodValue *= 130
					+ (AI_isStrongEmphasis() ? 15 : 0); // advc.131d
			iFoodValue /= 100;
		}
	}
	/* else if (iFoodValue > 0 && (AI_isEmphasizeYield(YIELD_PRODUCTION) || AI_isEmphasizeYield(YIELD_COMMERCE)))
	{
		iFoodValue *= 75; // was 75 for production, and 80 for commerce. (now same for both.)
		iFoodValue /= 100;
		iFoodValue = std::max(1, iFoodValue);
	} */ // K-Mod. Food value is now scaled elsewhere.

	if (AI_isEmphasizeYield(YIELD_COMMERCE))
	{
		iCommerceValue *= 140 // was 130
				+ (AI_isStrongEmphasis() ? 17 : 0); // advc.131d
		iCommerceValue /= 100;
	}
	else if (iCommerceValue > 0 && AI_isEmphasizeYield(YIELD_PRODUCTION))
	{
		iCommerceValue *= 75 // was 60
				- (AI_isStrongEmphasis() ? 15 : 0); // advc.131d
		iCommerceValue /= 100;
		iCommerceValue = std::max(1, iCommerceValue);
	}

	if (iProductionValue > 0)
	{
		if (bFoodIsProduction)
		{
			iProductionValue *= 100 + (bWorkerOptimization ? 0 :
					AI_specialYieldMultiplier(YIELD_PRODUCTION));
			iProductionValue /= 100;
		}
		else
		{
			iProductionValue *= iBaseProductionModifier;
			iProductionValue /= (iBaseProductionModifier + iExtraProductionModifier);

			// Note: iSlaveryValue use to be added here. Now it is counted as food value instead.
			iProductionValue *= 100 + (bWorkerOptimization ? 0 :
					AI_specialYieldMultiplier(YIELD_PRODUCTION));
			iProductionValue /= kOwner.AI_averageYieldMultiplier(YIELD_PRODUCTION);
		}

		iValue += std::max(1,iProductionValue);
	}

	if (iCommerceValue > 0)
	{
		iCommerceValue *= (100 + (bWorkerOptimization ? 0 : AI_specialYieldMultiplier(YIELD_COMMERCE)));
		iCommerceValue /= kOwner.AI_averageYieldMultiplier(YIELD_COMMERCE);
		iValue += std::max(1, iCommerceValue);
	}
//
	if (iFoodValue > 0)
	{
		iFoodValue *= 100;
		iFoodValue /= kOwner.AI_averageYieldMultiplier(YIELD_FOOD);
		iValue += std::max(1, iFoodValue);
	}

	return iValue;
}

// units of 400x commerce
int CvCityAI::AI_plotValue(CvPlot const& kPlot, bool bRemove, bool bIgnoreFood,
	bool bIgnoreStarvation, int iGrowthValue) const
{
	FAssert(getCityPlotIndex(kPlot) < NUM_CITY_PLOTS);
	/*	K-Mod. To reduce code duplication, this function now uses AI_jobChangeValue.
		(original code deleted) */
	if (bRemove)
	{
		return -AI_jobChangeValue(std::make_pair(false, -1),
				std::make_pair(false, getCityPlotIndex(kPlot)),
				bIgnoreFood, bIgnoreStarvation, iGrowthValue);
	}
	else
	{
		return AI_jobChangeValue(std::make_pair(false, getCityPlotIndex(kPlot)),
				std::make_pair(false, -1),
				bIgnoreFood, bIgnoreStarvation, iGrowthValue);
	}
}

/*	K-Mod. value gained by working new_job, and stopping work of old_job.
	jobs are (bSpecialist, iIndex) pairs. iIndex < 0 indicates "no job".
	Return value is roughly 400x commerce per turn.
	This function replaces AI_plotValue and AI_specialistValue. */
int CvCityAI::AI_jobChangeValue(std::pair<bool, int> new_job, std::pair<bool, int> old_job,
	bool bIgnoreFood, bool bIgnoreStarvation, int iGrowthValue) const
{
	PROFILE_FUNC();

	FAssert(new_job.second < 0 || (new_job.first ? new_job.second < GC.getNumSpecialistInfos() : getCityIndexPlot((CityPlotTypes)new_job.second)));
	FAssert(old_job.second < 0 || (old_job.first ? old_job.second < GC.getNumSpecialistInfos() : getCityIndexPlot((CityPlotTypes)old_job.second)));

	const CvPlayerAI& kOwner = GET_PLAYER(getOwner());
	int iTotalValue = 0;

	// Calculate and evaluate direct changes in yields
	int aiYieldGained[NUM_YIELD_TYPES] = {};
	int aiYieldLost[NUM_YIELD_TYPES] = {};

	FOR_EACH_ENUM(Yield)
	{
		int iYield = 0;
		if (new_job.second >= 0)
		{
			iYield += new_job.first ?
					kOwner.specialistYield((SpecialistTypes)new_job.second, eLoopYield) :
					getCityIndexPlot((CityPlotTypes)new_job.second)->getYield(eLoopYield);
		}

		if (old_job.second >= 0)
		{
			iYield -= old_job.first ?
					kOwner.specialistYield((SpecialistTypes)old_job.second, eLoopYield) :
					getCityIndexPlot((CityPlotTypes)old_job.second)->getYield(eLoopYield);
		}

		if (iYield >= 0)
			aiYieldGained[eLoopYield] = iYield;
		else aiYieldLost[eLoopYield] = -iYield;
	}
	int iYieldValue = 0;
	iYieldValue += 100 * AI_yieldValue(aiYieldGained, NULL, false,
			bIgnoreFood, bIgnoreStarvation, false, iGrowthValue);
	iYieldValue -= 100 * AI_yieldValue(aiYieldLost, NULL, true,
			bIgnoreFood, bIgnoreStarvation, false, iGrowthValue);

	/*	Check whether either the old job or the new job
		involves an upgradable improvement. (eg. a cottage)
		Note, AI_finalImprovementYieldDifference will update the yield vectors. */
	bool bUpgradeYields = false;
	if (new_job.second >= 0 && !new_job.first && AI_finalImprovementYieldDifference(
		*getCityIndexPlot((CityPlotTypes)new_job.second), aiYieldGained))
	{
		bUpgradeYields = true;
	}
	if (old_job.second >= 0 && !old_job.first && AI_finalImprovementYieldDifference(
		*getCityIndexPlot((CityPlotTypes)old_job.second), aiYieldLost))
	{
		bUpgradeYields = true;
	}
	if (bUpgradeYields)
	{
		FOR_EACH_ENUM2(Yield, y)
		{
			int iYield = aiYieldGained[y] - aiYieldLost[y];
			if (iYield >= 0)
			{
				aiYieldGained[y] = iYield;
				aiYieldLost[y] = 0;
			}
			else
			{
				aiYieldGained[y] = 0;
				aiYieldLost[y] = -iYield;
			}
		}
		/*	Combine the old and new values in the same way as AI_plotValue.
			(cf. AI_plotValue) */
		int iFinalYieldValue = 0;
		iFinalYieldValue += 100 * AI_yieldValue(aiYieldGained, NULL, false,
				bIgnoreFood, bIgnoreStarvation, false, iGrowthValue);
		iFinalYieldValue -= 100 * AI_yieldValue(aiYieldLost, NULL, true,
				bIgnoreFood, bIgnoreStarvation, false, iGrowthValue);

		if (iFinalYieldValue > iYieldValue)
			iYieldValue = (40 * iYieldValue + 60 * iFinalYieldValue) / 100;
		else iYieldValue = (60 * iYieldValue + 40 * iFinalYieldValue) / 100;
	}
	iTotalValue += iYieldValue;
	// (end of yield value)

	// Special consideration of plot improvements.
	int iImprovementsValue = 0;
	if (new_job.second >= 0 && !new_job.first)
	{
		iImprovementsValue += AI_specialPlotImprovementValue(
				*getCityIndexPlot((CityPlotTypes)new_job.second));
	}
	if (old_job.second >= 0 && !old_job.first)
	{
		iImprovementsValue -= AI_specialPlotImprovementValue(
				*getCityIndexPlot((CityPlotTypes)old_job.second));
	}
	iTotalValue += iImprovementsValue;

	// Specialist extras
	if (new_job.first || old_job.first)
	{
		// Raw commerce value (plots don't give raw commerce)
		int aiCommerceGained[NUM_COMMERCE_TYPES] = {};
		int aiCommerceLost[NUM_COMMERCE_TYPES] = {};

		FOR_EACH_ENUM(Commerce)
		{
			int iCommerce = 0;

			if (new_job.second >= 0 && new_job.first)
			{
				iCommerce += kOwner.specialistCommerce((SpecialistTypes)
						new_job.second, eLoopCommerce);
			}
			if (old_job.second >= 0 && old_job.first)
			{
				iCommerce -= kOwner.specialistCommerce((SpecialistTypes)
						old_job.second, eLoopCommerce);
			}
			if (iCommerce >= 0)
				aiCommerceGained[eLoopCommerce] = iCommerce;
			else
				aiCommerceLost[eLoopCommerce] = -iCommerce;
		}
		iTotalValue += 100 * AI_yieldValue(NULL, aiCommerceGained, false,
				bIgnoreFood, bIgnoreStarvation, false, iGrowthValue);
		iTotalValue -= 100 * AI_yieldValue(NULL, aiCommerceLost, true,
				bIgnoreFood, bIgnoreStarvation, false, iGrowthValue);

		int iGPPGained = 0;
		int iGPPLost = 0;
		if (new_job.second >= 0 && new_job.first)
			iGPPGained += GC.getInfo((SpecialistTypes)new_job.second).getGreatPeopleRateChange();
		if (old_job.second >= 0 && old_job.first)
			iGPPLost += GC.getInfo((SpecialistTypes)old_job.second).getGreatPeopleRateChange();

		if (iGPPGained || iGPPLost)
		{
			int iEmphasisCount = AI_isEmphasizeYield(YIELD_COMMERCE) +
					AI_isEmphasizeYield(YIELD_FOOD) + AI_isEmphasizeYield(YIELD_PRODUCTION);

			int iBaseValue = AI_isEmphasizeGreatPeople() ? 12 :
					(iEmphasisCount > 0 ? 3 : 4);
				// note: each point of iEmphasisCount reduces the value at the end.

			int iGPPValue = 0;

			/*	Value for GPP, dependant on great person type.
				(Note: currently for humans, great person weights are all 100.) */
			if (iGPPGained)
			{
				iGPPValue += iGPPGained * iBaseValue * kOwner.AI_getGreatPersonWeight((UnitClassTypes)
						GC.getInfo((SpecialistTypes)new_job.second).getGreatPeopleUnitClass());
			}
			if (iGPPLost)
			{
				iGPPValue -= iGPPLost * iBaseValue * kOwner.AI_getGreatPersonWeight((UnitClassTypes)
						GC.getInfo((SpecialistTypes)old_job.second).getGreatPeopleUnitClass());
			}
			iGPPValue *= getTotalGreatPeopleRateModifier();
			iGPPValue /= 100;

			// Bonus value for GPP when we're close to getting another great person
			if (!isHuman() || AI_isEmphasizeGreatPeople())
			{
				int iProgress = getGreatPeopleProgress();
				if (iProgress > 0)
				{
					int iThreshold = kOwner.greatPeopleThreshold();
					int iCloseBonus = (iGPPGained - iGPPLost) * (isHuman() ? 1 : 4) *
							iBaseValue * iProgress / iThreshold;
					iCloseBonus *= iProgress;
					iCloseBonus /= iThreshold;
					iGPPValue += iCloseBonus;
				}
			}

			// Scale based on how often this city will actually get a great person.
			if (iGPPValue != 0 && // k146
				!AI_isEmphasizeGreatPeople())
			{
				int iCityRate = getGreatPeopleRate() + iGPPGained - iGPPLost;
				int iHighestRate = 0;
				FOR_EACH_CITY(pLoopCity, kOwner)
					iHighestRate = std::max(iHighestRate, pLoopCity->getGreatPeopleRate());
				if (iHighestRate > iCityRate)
				{
					iGPPValue *= 100;
					/*	the +8 is just so that we don't block ourselves
						from assigning the first couple of specialists. */
					iGPPValue /= (2*100*(iHighestRate+8))/(iCityRate+8) - 100;
				}
				/*	each successive great person costs more points.
					So the points are effectively worth less...
					(note: I haven't tried to match this value decrease
					with the actual cost increase,
					because the value of the great people changes as well.) */
				iGPPValue *= 138; // advc.121: was *=100
				// it would be nice if we had a flavour modifier for this.
				iGPPValue /= 90 + 9 * kOwner.getGreatPeopleCreated(); // advc.121: was 90+7*...
			}

			//iTempValue /= kOwner.AI_averageGreatPeopleMultiplier();
			/*	K-Mod note: ultimately, I don't think the value should be divided
				by the average multiplier.
				because more great people points is always better,
				regardless of what the average multiplier is.
				However, because of the flawed way that food is currently evaluated,
				I need to dilute the value of GPP
				so that specialists don't get value more highly than food tiles.
				(I hope to correct this later.) */
			iGPPValue *= 100;
			iGPPValue /= (300 + kOwner.AI_averageGreatPeopleMultiplier())/4;

			iGPPValue /= (1 + iEmphasisCount);

			iTotalValue += iGPPValue;
		} /* advc.001: Moved the XP code out of the 'iGPPGained || iGPPLost' block.
			 That (unused) ability shouldn't be assumed to imply a GPP rate. */
		// Evaluate military experience from specialists
		int iExperience = 0;
		if (new_job.second >= 0 && new_job.first)
			iExperience += GC.getInfo((SpecialistTypes)new_job.second).getExperience();
		if (old_job.second >= 0 && old_job.first)
		{	// advc.001: was +=
			iExperience -= GC.getInfo((SpecialistTypes)old_job.second).getExperience();
		}
		if (iExperience != 0)
		{
			int iProductionRank = findYieldRateRank(YIELD_PRODUCTION);
			int iExperienceValue = 100 * iExperience * 4;
			if (iProductionRank <= kOwner.getNumCities() / 2 + 1
				|| isBarbarian()) // advc.300: Yield rank shouldn't matter for them
			{
				iExperienceValue += 100 * iExperience * 4;
			}
			iExperienceValue += (getMilitaryProductionModifier() * iExperience * 8);
			iTotalValue += iExperienceValue;
		}
		// Devalue generic citizens (for no specific reason). (cf. AI_specialistValue)
		/* if (no gpp) {
			SpecialistTypes eGenericCitizen = (SpecialistTypes)GC.getDEFAULT_SPECIALIST();
			if (eGenericCitizen != NO_SPECIALIST) {
				if (new_job.first && new_job.second == eGenericCitizen)
					iTotalValue = iTotalValue * 80 / 100;
				if (old_job.first && old_job.second == eGenericCitizen)
					iTotalValue = iTotalValue * 100 / 80;
			} } */
	}

	return iTotalValue;
}

/*	K-Mod. Difference between current yields and
	yields after plot improvement reaches final upgrade.
	piYields will have final yields added to it, and current yields subtracted.
	Return true iff any yields are changed. */
bool CvCityAI::AI_finalImprovementYieldDifference(/* advc: */ CvPlot const& kPlot,
	int* piYields) const // advc.make: was short* (cf. AI_yieldValue)
{
	FAssert(piYields != NULL);

	CvPlayer const& kOwner = GET_PLAYER(getOwner());
	bool bAnyChange = false;

	ImprovementTypes eCurrentImprovement = kPlot.getImprovementType();
	ImprovementTypes eFinalImprovement = CvImprovementInfo::finalUpgrade(eCurrentImprovement);
	if (eFinalImprovement != NO_IMPROVEMENT && eFinalImprovement != eCurrentImprovement)
	{
		FOR_EACH_ENUM(Yield)
		{
			int iYieldDiff = kPlot.calculateImprovementYieldChange(
					eFinalImprovement, eLoopYield, getOwner()) -
					kPlot.calculateImprovementYieldChange(
					eCurrentImprovement, eLoopYield, getOwner());
			// <advc.908a>
			int extraYieldThresh = kOwner.getExtraYieldThreshold(eLoopYield);
			if(extraYieldThresh > 0 &&
				// Otherwise the improvement doesn't matter
				kPlot.calculateNatureYield(eLoopYield, getTeam()) < extraYieldThresh)
			{
				if(kPlot.getYield(eLoopYield) > extraYieldThresh)
					iYieldDiff -= GC.getDefineINT(CvGlobals::EXTRA_YIELD);
				if(kPlot.getYield(eLoopYield) + iYieldDiff > extraYieldThresh)
					iYieldDiff += GC.getDefineINT(CvGlobals::EXTRA_YIELD);
				// Replacing the line below // </advc.908a>
				//iYieldDiff += (pPlot->getYield(i) >= kOwner.getExtraYieldThreshold(i) ? -GC.getEXTRA_YIELD() : 0) + (pPlot->getYield(i)+iYieldDiff >= kOwner.getExtraYieldThreshold(i) ? GC.getEXTRA_YIELD() : 0);
			}

			if (iYieldDiff != 0)
			{
				bAnyChange = true;
				piYields[eLoopYield] += iYieldDiff;
			}
		}
	}
	return bAnyChange;
}


/*	For improvements which upgrade when worked, this function calculates
	a time-weighted average of their yields.
	The average is calculated with continous weighting such that
	~63% of the weight is in the time from now until 'time_scale' turns have past.
	(More precisely, the weight drops exponentially w.r.t. the number of turns,
	decreasing by a factor of `e` for each `time_scale` turns.) */
bool CvCityAI::AI_timeWeightedImprovementYields(CvPlot const& kPlot, ImprovementTypes eImprovement,
	int iTimeScale, // advc.912f (note): 0 now means infinity
	EagerEnumMap<YieldTypes,scaled>& kWeightedYields) const // advc: was vector<float>&
{
	PROFILE_FUNC();

	FAssert(iTimeScale >= 0); // advc.912f: was >0

	/*	This is an experimental function, designed to be 'the right way'
		to evaluate improvements which upgrade over time,
		with no concern for calculation speed.
		If it isn't too slow, I'll use it for lots of things. */
	// weighted yield = integral from 0 to inf. of (yield(t) * e^(-t/scale)), w.r.t.  t

	kWeightedYields.reset();
	std::set<ImprovementTypes> citedImprovements;
	int iTotalTurns = 0;

	while (eImprovement != NO_IMPROVEMENT &&
		citedImprovements.insert(eImprovement).second)
	{
		CvImprovementInfo const& kImprovement = GC.getInfo(eImprovement);
		/*	<advc.912f> If upgrades will never happen, use factor 1 for the current improv
			and skip the rest. */
		scaled rValueFactor;
		if (iTimeScale == 0)
		{
			if (iTotalTurns == 0)
				rValueFactor = 1;
			else break;
		}
		else // </advc.912f>
		{
			// piecewise integration
			// each piece is exp(-t0/T) - exp(-t1/T)
			// [advc: Comment had said 't1' instead of '-t1'; but I think the code is right.]
			rValueFactor = scaled(iTotalTurns, -iTimeScale).exp() -
					(kImprovement.getImprovementUpgrade() == NO_IMPROVEMENT ? 0 :
					scaled(iTotalTurns + kImprovement.getUpgradeTime(), -iTimeScale).exp());
		}
		FOR_EACH_ENUM(Yield)
		{
			int iYieldDiff = kPlot.calculateImprovementYieldChange(
					eImprovement, eLoopYield, getOwner());
			/*	todo: Extra yield for finacial civs
				(see AI_finalImprovementYieldDifference for guidence.) */
			//if (kOwner.getExtraYieldThreshold(i) > 0)
				// ;

			kWeightedYields.add(eLoopYield, iYieldDiff * rValueFactor);
		}

		iTotalTurns += kImprovement.getUpgradeTime();
		eImprovement = kImprovement.getImprovementUpgrade();
	}

	if (eImprovement != NO_IMPROVEMENT /* advc.912f: */ && iTimeScale > 0)
	{
		/*	If we didn't reach final improvement;
			normalise the yield values based on what we've got so far. */
		FOR_EACH_ENUM(Yield)
		{
			kWeightedYields.set(eLoopYield, kWeightedYields.get(eLoopYield) /
					(1 - scaled(iTotalTurns, -iTimeScale).exp()));
		}
	}
	// return true if the improvement had any upgrades
	return (citedImprovements.size() > 1);
}

/*	K-Mod. Value for working a plot in addition to its yields.
	(Returns ~400x commerce per turn.) */
int CvCityAI::AI_specialPlotImprovementValue(CvPlot const& kPlot) const
{
	ImprovementTypes const eImprovement = kPlot.getImprovementType();
	if (eImprovement == NO_IMPROVEMENT)
		return 0;
	int iValue = 0;
	if (GC.getInfo(eImprovement).getImprovementUpgrade() != NO_IMPROVEMENT)
	{
		/*	Prefer plots that are close to upgrading, but
			not over immediate yield differences. (kludge) */
		iValue += kPlot.getUpgradeProgress() /
				std::max(1, GC.getGame().getImprovementUpgradeTime(eImprovement));
	}
	/*	small value bonus for the possibility of popping new resources.
		(cf. CvGame::doFeature) */
	if (kPlot.getBonusType(getTeam()) == NO_BONUS)
	{
		FOR_EACH_ENUM(Bonus)
		{
			if (GET_TEAM(getTeam()).canDiscoverBonus(eLoopBonus) &&
				GC.getInfo(eImprovement).getImprovementBonusDiscoverRand(eLoopBonus) > 0)
			{
				iValue += 20;
			}
		}
	}
	return iValue;
}

/*	K-Mod: Value of each unit of food for the purpose of population growth.
	Units ~4x commerce. Note: the value here is at the high end..
	it should be reduced based on things such as the happiness cap. */
int CvCityAI::AI_growthValuePerFood() const
{
	int iFoodMultiplier = getBaseYieldRateModifier(YIELD_FOOD);
	int iConsumtionPerPop = std::max(1, GC.getFOOD_CONSUMPTION_PER_POPULATION());
	// <k146>
	/*  Note, although we are trying to evaluate growth value, we still need to
		take into account jobs we are already working, because some of our food
		goes into supporting those jobs; and if they are significantly more
		valuable than the unworked jobs, then our cities just won't want to grow.
		(This function is probably a good place to calculate the 'devalue rate'
		used in food evaluation. But we aren't doing that right now.) */
	std::vector<int> unworked_jobs;
	std::vector<int> worked_jobs;
	for (WorkablePlotIter it(*this, false); it.hasNext(); ++it)
	{
		CvPlot const& kPlot = *it;
		CityPlotTypes const ePlot = it.currID();

		if (isWorkingPlot(ePlot) && kPlot.getYield(YIELD_FOOD) >= iConsumtionPerPop)
			continue; // we don't need to evaluate self-sufficient plots already being worked.

		int iValue = AI_plotValue(kPlot, isWorkingPlot(ePlot), true, true, -1);
		iValue *= 100 * iConsumtionPerPop + iFoodMultiplier * kPlot.getYield(YIELD_FOOD);
		iValue /= 100 * iConsumtionPerPop;

		if (isWorkingPlot(ePlot))
			worked_jobs.push_back(iValue);
		else unworked_jobs.push_back(iValue);
	}

	const CvPlayerAI& kOwner = GET_PLAYER(getOwner());

	FOR_EACH_ENUM2(Specialist, eSpec)
	{
		// cf. CvCity::isSpecialistValid
		int iAvailable = (kOwner.isSpecialistValid(eSpec) ||
				eSpec == GC.getDEFAULT_SPECIALIST()) ? 3 :
				std::min(3, getMaxSpecialistCount(eSpec) - getSpecialistCount(eSpec));
		// this could get messed up by free specialists. I'm not sure if that's a problem.
		int iCurrent = getSpecialistCount(eSpec);
		/*	consider using totalFreeSpecialists() or something to find out
			if we are actually feeding these specialists. */

		if (iAvailable > 0  || (iCurrent > 0 &&
			kOwner.specialistYield(eSpec, YIELD_FOOD) < iConsumtionPerPop))
		{
			FAssert(iAvailable == 0 || isSpecialistValid(eSpec, iAvailable));
			/*	note. I'm just sticking with 'bRemove == false'
				so that we don't have to evaluate twice. */
			int iValue = AI_specialistValue(eSpec, false, true, -1);
			iValue *= 100 * iConsumtionPerPop + iFoodMultiplier *
					kOwner.specialistYield(eSpec, YIELD_FOOD);
			iValue /= 100 * iConsumtionPerPop;
			if (iCurrent > 0)
			{
				while (--iCurrent >= 0)
					worked_jobs.push_back(iValue);
			}
			if (iAvailable > 0)
			{
				while (--iAvailable >= 0)
					unworked_jobs.push_back(iValue);
			}
		}
	}
	/*  ok. we've surveyed the available jobs.
		To calculate the food value, we'll use the values of the best 3 unworked
		jobs; but we'll also consider the worst of the worked jobs.
		(To be honest, I'm really not sure what is the best way to handle the
		worked jobs. The current system can cause flip-flopping, due to
		food value decreasing when food is being worked.)
		Note: from here on, "unworked_jobs" isn't only for unworked jobs. */
	while (worked_jobs.size() < 3)
		worked_jobs.push_back(0);
	std::partial_sort(worked_jobs.begin(), worked_jobs.begin() +
			3, worked_jobs.end(), std::less_equal<int>()); // worst 3 worked jobs.
	for (int i = 0; i < 3; ++i)
		unworked_jobs.push_back(worked_jobs[i]);
	// best 3 unworked (or best of the worsed worked)
	std::partial_sort(unworked_jobs.begin(), unworked_jobs.begin() + 3,
			unworked_jobs.end(), std::greater<int>());
	return (unworked_jobs[0]*4 + unworked_jobs[1]*2 + unworked_jobs[2]*1) /
			/*	advc.121: Coefficient was 700. I think that prioritized growth
				too much. */
			(800 * iConsumtionPerPop);
	// </k146>
}


int CvCityAI::AI_experienceWeight()
{
	//return ((getProductionExperience() + getDomainFreeExperience(DOMAIN_SEA)) * 2);
	// K-Mod
	return 2 * getProductionExperience() +
			getDomainFreeExperience(DOMAIN_LAND) + getDomainFreeExperience(DOMAIN_SEA)
			- 2; /*  advc.017: Barracks are pretty ubiquitous; shouldn't add 3
					 to buildUnitProb. Rather make cities w/o Barracks hesitant
					 to train units. */
	// K-Mod end
}

// BBAI / K-Mod // <advc.017> Draft param added; count XP weight only half then.
int CvCityAI::AI_buildUnitProb(bool bDraft)
{
	scaled r = per100(GC.getInfo(getPersonalityType()).getBuildUnitProb() - 5); // rfc: adjust build unit prob

    // rfc: blanket reduction
    if (!isBarbarian())
    {
        iProb *= 3;
        iProb /= 4;
    }
    if (GET_PLAYER(getOwner()).getCurrentEra() >= ERA_RENAISSANCE)
    {
        if (!GET_TEAM(getTeam()).isAtWar(GC.getGame().getActiveTeam()))
        {
            iProb *= 4;
            iProb /= 5;
        }
    }

    int iXPWeight = AI_experienceWeight();
	if (bDraft)
		iXPWeight /= 2;
	r += per100(iXPWeight);
	// </advc.017>
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());
	// <advc.253>
	if (kOwner.AI_getCurrEraFactor() >= 1)
		r *= kOwner.AI_trainUnitSpeedAdustment(); // <advc.253>
	bool bGreatlyReduced = false; // advc.017
	// BETTER_BTS_AI_MOD, 05/29/10, jdog5000: City AI, Barbarian AI
	if (!isBarbarian() && kOwner.AI_isFinancialTrouble())
	{
		r /= 2;
		bGreatlyReduced = true; // advc.017
	}
	//else if (GET_TEAM(getTeam()).getHasMetCivCount(false) == 0)
	/*	<advc.109> Replacing the BBAI code above. The ECONOMY_FOCUS check is from K-Mod;
		moved from AI_chooseProduction. */
	else if (kOwner.AI_isDoStrategy(AI_STRATEGY_ECONOMY_FOCUS) ||
		(kOwner.getNumCities() <= 1 && isCapital()))
	{
		r /= 2; // </advc.109>
		bGreatlyReduced = true; // advc.017
	}
	// advc.017: Don't always adjust to era
	if (kOwner.AI_isDoStrategy(AI_STRATEGY_GET_BETTER_UNITS))
	{
		scaled rEraDiff = GC.AI_getGame().AI_getCurrEraFactor()
				- kOwner.AI_getCurrEraFactor();
		if (rEraDiff.isPositive())
			r *= scaled::max(fixp(0.4), 1 - fixp(0.2) * rEraDiff);
	}
	// <advc.017>
	if (!bDraft)
	{
		// Lowered multiplier from 2 to 1.5
		r *= 1 + fixp(1.5) * per100(getMilitaryProductionModifier());
	}
	if (!isBarbarian())
	{
		int const iCities = kOwner.getNumCities();
		if (iCities > 1)
		{
			CvTeamAI const& kOurTeam = GET_TEAM(getTeam());
			int iHighestRivalPow = 0;
			for (TeamAIIter<FREE_MAJOR_CIV,OTHER_KNOWN_TO> it(getTeam());
				it.hasNext(); ++it)
			{
				CvTeamAI const& kRival = *it; // (Akin to code in CvPlayerAI::AI_feelsSafe)
				if (kOurTeam.AI_getWarPlan(kRival.getID()) != NO_WARPLAN ||
					!kOurTeam.AI_isAvoidWar(kRival.getID(), true) ||
					!kRival.AI_isAvoidWar(kOurTeam.getID()) ||
					kOurTeam.AI_anyMemberAtVictoryStage(
					AI_VICTORY_MILITARY3 | AI_VICTORY_MILITARY4) ||
					kRival.AI_anyMemberAtVictoryStage(
					AI_VICTORY_MILITARY3 | AI_VICTORY_MILITARY4))
				{
					iHighestRivalPow = std::max(kRival.getPower(true), iHighestRivalPow);
				}
			}
			// Don't throttle at all until we're clearly ahead of the best rival
			scaled rTargetAdvantage = per100(25);
			if (kOwner.AI_atVictoryStage(AI_VICTORY_MILITARY1))
				rTargetAdvantage += per100(5);
			if (kOwner.AI_atVictoryStage(AI_VICTORY_MILITARY2))
				rTargetAdvantage += per100(5);
			if (kOwner.AI_atVictoryStage(AI_VICTORY_MILITARY3))
				rTargetAdvantage += per100(7);
			if (kOwner.AI_atVictoryStage(AI_VICTORY_MILITARY4))
				rTargetAdvantage += per100(8);
			scaled rTargetPow = (rTargetAdvantage + 1) * iHighestRivalPow;
			rTargetPow.increaseTo(scaled::epsilon());
			scaled rPowRatio = kOurTeam.getPower(false) / rTargetPow;
			if (rPowRatio > 1)
			{
				scaled rAdvantage = rPowRatio - 1;
				if (rAdvantage >= fixp(1.5))
				{
					r /= 4;
					bGreatlyReduced = true;
				}
				else r *= 1 - rAdvantage / 2;
			}
		}
		/*  Can't afford to specialize one city entirely on military production
			until we've expanded a bit */
		r.decreaseTo(fixp(0.2) * (1 + iCities));
		/*  Don't get too careless in the early game when most cities have
			negative AI_experienceWeight */
		if (!bGreatlyReduced)
			r.increaseTo(per100(25 - 2 * iCities));
	} // </advc.017>
	r.decreaseTo(1); // experimental (K-Mod)
	return r.getPercent();
}

// advc: Body cut from AI_bestPlotBuild (K-Mod code)
bool CvCityAI::AI_emphasizeIrrigatingPlot(CvPlot const& kPlot) const
{
	/*BonusTypes eNonObsoleteBonus = kPlot.getNonObsoleteBonusType(getTeam());
	bool bHasBonusImprovement = false;
	if (eNonObsoleteBonus != NO_BONUS) {
		if (pPlot->getImprovementType() != NO_IMPROVEMENT) {
			if (GC.getInfo(pPlot->getImprovementType()).isImprovementBonusTrade(eNonObsoleteBonus))
				bHasBonusImprovement = true;
		}
	}*/ // BtS
	if (kPlot.getNonObsoleteBonusType(getTeam(), true) != NO_BONUS
		|| isBarbarian()) // advc.300
	{
		return false;
	}
	/*	It looks unwieldly but the code has to be rigid to avoid "worker ADD"
		where they keep connecting then disconnecting a crops resource or building
		multiple farms to connect a single crop resource.
		isFreshWater is used to ensure invalid plots are pruned early, the inner loop
		really doesn't run that often.

		using logic along the lines of "Will irrigating me make crops wet"
		wont really work... it has to be "am i the tile the crops want to be irrigated"

		I optimized through the use of "isIrrigated" which is just checking a bool...
		once everything is nicely irrigated, this code should be really fast... */
	if (!kPlot.isIrrigated() &&
		(!kPlot.isFreshWater() || !kPlot.canHavePotentialIrrigation()))
	{
		return false;
	}
	FOR_EACH_ADJ_PLOT(kPlot)
	{
		if (pAdj->getOwner() != getOwner() || !pAdj->isCityRadius())
			continue;
		if (pAdj->isFreshWater() ||
			/*	check for a city? cities can conduct irrigation and that effect is
				quite useful... so I think irrigate cities. */
			!pAdj->isPotentialIrrigation())
		{
			continue;
		}
		CvPlot* eBestIrrigationPlot = NULL;
		FOR_EACH_ADJ_PLOT_VAR2(pDistTwoPlot, *pAdj)
		{
			if (pDistTwoPlot->getOwner() != getOwner())
				continue;
			BonusTypes const eDistTwoBonus = pDistTwoPlot->
					getNonObsoleteBonusType(getTeam());
			if (pAdj->isIrrigated() &&
				//the irrigation has to be coming from somewhere
				pDistTwoPlot->isIrrigated())
			{
				/*	if we find a tile which is already carrying irrigation
					then lets not replace that one... */
				eBestIrrigationPlot = pDistTwoPlot;
				if (pDistTwoPlot->isCity() || eDistTwoBonus != NO_BONUS ||
					!pDistTwoPlot->isCityRadius())
				{
					if (pDistTwoPlot->isFreshWater())
					{
						//these are all ideal for irrigation chains so stop looking.
						break;
					}
				}
			}
			else
			{
				if (eDistTwoBonus == NO_BONUS)
				{
					if (pDistTwoPlot->canHavePotentialIrrigation() &&
						pDistTwoPlot->isIrrigationAvailable())
					{
						/*	could use more sophisticated logic
							however this would rely on things like
							smart irrigation chaining of out-of-city plots */
						eBestIrrigationPlot = pDistTwoPlot;
						break;
					}
				}
			}
		}
		if (&kPlot == eBestIrrigationPlot)
			return true;
	}
	return false;
}


void CvCityAI::AI_bestPlotBuild(CvPlot const& kPlot, int* piBestValue, BuildTypes* peBestBuild,
	int iFoodPriority, int iProductionPriority, int iCommercePriority, bool bChop,
	int iHappyAdjust, int iHealthAdjust, // advc (note): obsolete
	int iDesiredFoodChange) const
{
	PROFILE_FUNC();

	if (piBestValue != NULL)
		*piBestValue = 0;
	if (peBestBuild != NULL)
		*peBestBuild = NO_BUILD;

	if (kPlot.getWorkingCity() != this)
		return;

	/*	When improving new plots only, count emphasis twice
		helps to avoid too much tearing up of old improvements. */

	/*	K-Mod: I've deleted the section about counting emphasis twice...
		It's absurd to think it would help avoid tearing up old improvements.
		If the emphasis changes as soon as the improvment is built, then that
		is likely to cause us to tear up the improvement! */

	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());
	FAssert(kPlot.getOwner() == kOwner.getID());
	BonusTypes const eBonus = kPlot.getBonusType(getTeam());
	// (advc: bHasBonusImprovement moved into AI_emphasizeIrrigatingPlot)
	int iClearFeatureValue = 0;
	/*	K-Mod. I've removed the yield change evaluation from AI_clearFeatureValue
		(to avoid double counting it elsewhere)
		but for the parts of this function, we want to count that value... */
	int iClearValue_wYield = 0; // So I've made this new number for that purpose.
	if (kPlot.isFeature())
	{
		iClearFeatureValue = AI_clearFeatureValue(getCityPlotIndex(kPlot));
		CvFeatureInfo const& kFeature = GC.getInfo(kPlot.getFeatureType());
		iClearValue_wYield = iClearFeatureValue;
		iClearValue_wYield -= kFeature.getYieldChange(YIELD_FOOD) *
				100 * iFoodPriority / 100;
		iClearValue_wYield -= kFeature.getYieldChange(YIELD_PRODUCTION) *
				80 * iProductionPriority / 100; // was 60
		iClearValue_wYield -= kFeature.getYieldChange(YIELD_COMMERCE) *
				40 * iCommercePriority / 100;
	}

	BuildTypes eBestBuild = NO_BUILD;
	int iBestValue = 0;

	// advc.300: Improve only worked plots for their yield
	if (!isBarbarian() || isWorkingPlot(kPlot))
	{	// advc: Moved into subroutine
		bool bEmphasizeIrrigation = AI_emphasizeIrrigatingPlot(kPlot);
		FOR_EACH_ENUM(Improvement)
		{
			BuildTypes eBestTempBuild;
			int iValue = AI_getImprovementValue(kPlot, eLoopImprovement, iFoodPriority,
					iProductionPriority, iCommercePriority, iDesiredFoodChange,
					iClearFeatureValue, bEmphasizeIrrigation, &eBestTempBuild);
			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				eBestBuild = eBestTempBuild;
			}
		}
	}

	// K-Mod. Don't chop the feature if we need it for our best improvement!
	/* advc.117: This seems to be ok (no change). River-side and hill-side forests
	   are still being chopped. */
	if (eBestBuild == NO_BUILD ?
		(!kPlot.isImproved() ||
		GC.getInfo(kPlot.getImprovementType()).isRequiresFeature()) :
		(GC.getInfo(eBestBuild).getImprovement() != NO_IMPROVEMENT &&
		GC.getInfo(GC.getInfo(eBestBuild).getImprovement()).isRequiresFeature()))
	{
		bChop = false;
	}
	else if (iClearValue_wYield > 0)
	// K-Mod end
	{
		FAssert(kPlot.isFeature());
		/*if ((GC.getInfo(kPlot.getFeatureType()).getHealthPercent() < 0) ||
			((GC.getInfo(kPlot.getFeatureType()).getYieldChange(YIELD_FOOD) + GC.getInfo(kPlot.getFeatureType()).getYieldChange(YIELD_PRODUCTION) + GC.getInfo(kPlot.getFeatureType()).getYieldChange(YIELD_COMMERCE)) < 0)) {*/
		// Disabled by K-Mod. That stuff is already taken into account by iClearValue_wYield.

		FOR_EACH_ENUM(Build)
		{
			if (GC.getInfo(eLoopBuild).getImprovement() == NO_IMPROVEMENT &&
				GC.getInfo(eLoopBuild).isFeatureRemove(kPlot.getFeatureType()) &&
				kOwner.canBuild(kPlot, eLoopBuild))
			{
				int iValue = iClearValue_wYield;
				{
					CvCity* pCity=NULL;
					iValue += (kPlot.getFeatureProduction(eLoopBuild, getTeam(), &pCity)
							* 5); // was * 10
				}
				iValue *= 400;
				iValue /= std::max(1, GC.getInfo(eLoopBuild).getFeatureTime(
						kPlot.getFeatureType()) + 100);

				if (iValue > iBestValue) // K-Mod. (removed redundant checks)
					//|| (iValue > 0 && eBestBuild == NO_BUILD))
				{
					iBestValue = iValue;
					eBestBuild = eLoopBuild;
				}
			}
		}
	}

	/*	Chop - maybe integrate this better with the other feature-clear code
		though the logic is kinda different */
	if (bChop && eBonus == NO_BONUS && kPlot.isFeature() &&
		!kPlot.isImproved() && !kOwner.isHumanOption(PLAYEROPTION_LEAVE_FORESTS))
	{
		FOR_EACH_ENUM(Build)
		{
			if (GC.getInfo(eLoopBuild).getImprovement() != NO_IMPROVEMENT ||
				!GC.getInfo(eLoopBuild).isFeatureRemove(kPlot.getFeatureType()) ||
				!kOwner.canBuild(kPlot, eLoopBuild))
			{
				continue;
			}
			CvCity* pCity=NULL;
			int iValue = (kPlot.getFeatureProduction(eLoopBuild, getTeam(), &pCity)) * 10;
			FAssert(pCity == this);
			if (iValue <= 0)
				continue;
			// K-Mod. Inflate the production value in the early expansion phase of the game.
			int iCitiesTarget = GC.getInfo(GC.getMap().getWorldSize()).getTargetNumCities();
			if (kOwner.getNumCities() < iCitiesTarget && kOwner.AI_getNumCitySites() > 0)
				iValue = (iValue * 3 * iCitiesTarget) /
						std::max(1, 2 * kOwner.getNumCities() + iCitiesTarget);
			/*	Increase the value if it is large compared to the city's natural production rate
				(note: iValue is chop production * 10) */
			iValue += iValue / (getBaseYieldRate(YIELD_PRODUCTION)*20 + iValue);
			// K-Mod end
			iValue += iClearValue_wYield;
			// K-Mod
			if (!kPlot.isBeingWorked() && iClearFeatureValue < 0)
			{	// extra points for passive feature bonuses such as health
				iValue += iClearFeatureValue/2;
			} // K-Mod end
			if (iValue <= 0)
				continue;
			if (kOwner.AI_isDoStrategy(AI_STRATEGY_DAGGER))
			{
				iValue += 20;
				iValue *= 2;
			}
			// K-Mod, flavour production, military, and growth.
			if (kOwner.AI_getFlavorValue(FLAVOR_PRODUCTION) > 0 ||
				kOwner.AI_getFlavorValue(FLAVOR_MILITARY) +
				kOwner.AI_getFlavorValue(FLAVOR_GROWTH) > 2)
			{
				iValue *= 110 + 3 * kOwner.AI_getFlavorValue(FLAVOR_PRODUCTION) +
						2 * kOwner.AI_getFlavorValue(FLAVOR_MILITARY) +
						2 * kOwner.AI_getFlavorValue(FLAVOR_GROWTH);
				iValue /= 100;
			} // K-Mod end
			iValue *= 500;
			iValue /= std::max(1, GC.getInfo(eLoopBuild).
					getFeatureTime(kPlot.getFeatureType()) + 100);
			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				eBestBuild = eLoopBuild;
			}
		}
	}

	FOR_EACH_ENUM(Route)
	{
		RouteTypes const eOldRoute = kPlot.getRouteType();
		if (eLoopRoute == eOldRoute)
			continue;

		int iTempValue = 0;
		if (kPlot.isImproved())
		{
			CvImprovementInfo const& kCurrentImprov = GC.getInfo(kPlot.getImprovementType());
			if (eOldRoute == NO_ROUTE || GC.getInfo(eLoopRoute).getValue() > GC.getInfo(eOldRoute).getValue())
			{
				iTempValue += kCurrentImprov.getRouteYieldChanges(eLoopRoute, YIELD_FOOD) * 100;
				iTempValue += kCurrentImprov.getRouteYieldChanges(eLoopRoute, YIELD_PRODUCTION) * 80; // was 60
				iTempValue += kCurrentImprov.getRouteYieldChanges(eLoopRoute, YIELD_COMMERCE) * 40;
			}
			if (kPlot.isBeingWorked())
				iTempValue *= 2;
			//road up bonuses if sort of bored.
			if (!kPlot.isWater() && // K-Mod
				eOldRoute == NO_ROUTE && eBonus != NO_BONUS)
			{
				iTempValue += (kPlot.isConnectedToCapital() ? 10 : 30);
			}
		}
		if (iTempValue > 0)
		{
			FOR_EACH_ENUM(Build)
			{
				if (GC.getInfo(eLoopBuild).getRoute() == eLoopRoute &&
					kOwner.canBuild(kPlot, eLoopBuild, false))
				{
					//the value multiplier is based on the default time...
					int iValue = iTempValue * 5 * 300;
					iValue /= GC.getInfo(eLoopBuild).getTime();
					if (iValue > iBestValue || (iValue > 0 && eBestBuild == NO_BUILD))
					{
						iBestValue = iValue;
						eBestBuild = eLoopBuild;
        if (eRoute != eOldRoute)
        {
        	int iTempValue = 0;
            if (pPlot->getImprovementType() != NO_IMPROVEMENT)
            {
                if ((eOldRoute == NO_ROUTE) || (GC.getRouteInfo(eRoute).getValue() > GC.getRouteInfo(eOldRoute).getValue()))
                {
                    iTempValue += ((GC.getImprovementInfo(pPlot->getImprovementType()).getRouteYieldChanges(eRoute, YIELD_FOOD)) * 100);
                    iTempValue += ((GC.getImprovementInfo(pPlot->getImprovementType()).getRouteYieldChanges(eRoute, YIELD_PRODUCTION)) * 60);
                    iTempValue += ((GC.getImprovementInfo(pPlot->getImprovementType()).getRouteYieldChanges(eRoute, YIELD_COMMERCE)) * 40);
                }

                if (pPlot->isBeingWorked())
                {
                	iTempValue *= 2;
                }
				//road up bonuses if sort of bored.
				if ((eOldRoute == NO_ROUTE) && (eBonus != NO_BONUS))
				{
					iTempValue += (pPlot->isConnectedToCapital() ? 10 : 30);
				}
            }

			if (iTempValue > 0)
			{
				for (iJ = 0; iJ < GC.getNumBuildInfos(); iJ++)
				{
					eBuild = ((BuildTypes)iJ);
					if (GC.getBuildInfo(eBuild).getRoute() == eRoute)
					{
						if (GET_PLAYER(getOwnerINLINE()).canBuild(pPlot, eBuild, false))
						{
							//the value multiplier is based on the default time...
							iValue = iTempValue * 5 * 300;
							iValue /= GC.getBuildInfo(eBuild).getTime();

							if ((iValue > iBestValue) || ((iValue > 0) && (eBestBuild == NO_BUILD)))
							{
								iBestValue = iValue;
								eBestBuild = eBuild;
							}
						}
					}
				}
			}
		}
	}

	if (eBestBuild != NO_BUILD)
	{
		FAssert(iBestValue > 0);

		/*//Now modify the priority for this build.
		if (kOwner.AI_isFinancialTrouble()) {
			if (GC.getInfo(eBestBuild).getImprovement() != NO_IMPROVEMENT) {
				iBestValue += (iBestValue * std::max(0, aiBestDiffYields[YIELD_COMMERCE])) / 4;
				iBestValue = std::max(1, iBestValue);
			}
		}*/

		if (piBestValue != NULL)
			*piBestValue = iBestValue;
		if (peBestBuild != NULL)
			*peBestBuild = eBestBuild;
	}
}


int CvCityAI::AI_getHappyFromHurry(HurryTypes eHurry) const
{
	return AI_getHappyFromHurry(hurryPopulation(eHurry));
}

int CvCityAI::AI_getHappyFromHurry(int iHurryPopulation) const
{
	PROFILE_FUNC();

	int iHappyDiff = iHurryPopulation - GC.getDefineINT(CvGlobals::HURRY_POP_ANGER);
	if (iHappyDiff > 0)
	{
		if (getHurryAngerTimer() <= 1)
		{
			if (2 * angryPopulation(1) - healthRate(false, 1) > 1)
			{
				return iHappyDiff;
			}
		}
	}

	return 0;
}

int CvCityAI::AI_getHappyFromHurry(HurryTypes eHurry, UnitTypes eUnit, bool bIgnoreNew) const
{
	return AI_getHappyFromHurry(getHurryPopulation(eHurry, getHurryCost(true, eUnit, bIgnoreNew)));
}

int CvCityAI::AI_getHappyFromHurry(HurryTypes eHurry, BuildingTypes eBuilding, bool bIgnoreNew) const
{
	return AI_getHappyFromHurry(getHurryPopulation(eHurry, getHurryCost(true, eBuilding, bIgnoreNew)));
}

// K-Mod. I'm essentially rewritten this function. note: units ~ commerce x100
int CvCityAI::AI_splitEmpireValue() const
{
	PROFILE_FUNC();
	/*AreaAITypes eAreaAI = getArea().getAreaAIType(getTeam());
	if (eAreaAI == AREAAI_OFFENSIVE || eAreaAI == AREAAI_MASSING || eAreaAI == AREAAI_DEFENSIVE)
		return 0;*/ // (BtS) This isn't relevant to city value. It should be handled elsewhere.

	// K-Mod: disorder causes the commerce rates to go to zero... so that would  mess up our calculations
	if (isDisorder())
	{
		//return 0;
		/*	advc.ctr: Could always use this, but the K-Mod code yields similar results,
			is faster and, for the moment, no trouble to maintain. */
		return -GET_PLAYER(getOwner()).AI_assetVal(*this, false).getPercent();
	}

	int iValue = 0;

	/*iValue += getCommerceRateTimes100(COMMERCE_GOLD);
	iValue += getCommerceRateTimes100(COMMERCE_RESEARCH);
	iValue += 100 * getYieldRate(YIELD_PRODUCTION);
	iValue -= 3 * calculateColonyMaintenanceTimes100();*/ // BtS
	// K-Mod. The original code fails for civs using high espionage or high culture.
	const CvPlayerAI& kOwner = GET_PLAYER(getOwner());
	iValue += getCommerceRateTimes100(COMMERCE_RESEARCH) *
			kOwner.AI_commerceWeight(COMMERCE_RESEARCH);
	iValue += getCommerceRateTimes100(COMMERCE_ESPIONAGE) *
			kOwner.AI_commerceWeight(COMMERCE_ESPIONAGE);
	iValue /= 100;
	/*	Culture isn't counted, because its value is local.
		Unfortunately this will mean that civs running 100% culture
		(ie CULTURE4) will give up their non-core cities. It could be argued
		that this would be good strategy, but the problem is
		that CULTURE4 doesn't always run its full course. ...
		so I'm going to make a small ad hoc adjustment... */
	iValue += 100 * getYieldRate(YIELD_PRODUCTION);
	iValue *= (kOwner.AI_atVictoryStage(AI_VICTORY_CULTURE4) ? 2 : 1);
	/*	Gold value is not weighted, and does not get the cultural victory boost,
		because gold is directly comparable to maintenance. */
	iValue += getCommerceRateTimes100(COMMERCE_GOLD);

	int iCosts = calculateColonyMaintenanceTimes100() + 2*getMaintenanceTimes100()/3;
	iCosts = iCosts * (100+kOwner.calculateInflationRate()) / 100;

	// slightly encourage empire split when aiming for a diplomatic victory
	if (kOwner.AI_atVictoryStage(AI_VICTORY_DIPLOMACY3) &&
		kOwner.getCommercePercent(COMMERCE_GOLD) > 0)
	{
		iCosts = iCosts * 4 / 3;
	}
	// target pop is not a good measure for small cities w/ unimproved tiles.
	int iTargetPop = std::max(5, AI_getTargetPopulation());
	if (getPopulation() > 0 && getPopulation() < iTargetPop)
	{
		iValue *= iTargetPop + 3;
		iValue /= getPopulation() + 3;
		iCosts *= getPopulation() + 6;
		iCosts /= iTargetPop + 6;
	}
	iValue -= iCosts;
	// K-Mod end
	return -iValue; // advc.ctr: Sign flipped to match the new function name
}

void CvCityAI::AI_doPanic() // advc: Unused return type bool removed, body refactored.
{
	/*	advc.139 (comment): This gets called after defenders have moved,
		so AI_isSafe wouldn't be reliable. */
	if (//(getArea().getAreaAIType(getTeam()) == AREAAI_OFFENSIVE || getArea().getAreaAIType(getTeam()) == AREAAI_DEFENSIVE || getArea().getAreaAIType(getTeam()) == AREAAI_MASSING)
		!GET_PLAYER(getOwner()).AI_isLandWar(getArea())) // K-Mod
	{
		return;
	}
	int iOurDefense = GET_PLAYER(getOwner()).AI_localDefenceStrength(plot(), getTeam());
	int iEnemyOffense = GET_PLAYER(getOwner()).AI_localAttackStrength(plot());
	scaled rRatio(iEnemyOffense, std::max(1, iOurDefense));
	if (rRatio <= 1)
		return;

	UnitTypes eProductionUnit = getProductionUnit();
	if (eProductionUnit != NO_UNIT && getProduction() > 0 &&
		GC.getInfo(eProductionUnit).getCombat() > 0)
	{
		AI_doHurry(true);
		return;
	}
	if ((SyncRandOneChanceIn(2) && AI_chooseUnit(UNITAI_CITY_COUNTER)) ||
		AI_chooseUnit(UNITAI_CITY_DEFENSE) || AI_chooseUnit(UNITAI_ATTACK))
	{
		AI_doHurry(rRatio > fixp(1.4));
	}
}

/* disabled by K-Mod. (this function is buggy, and obsolete)
int CvCityAI::AI_calculateCulturePressure(bool bGreatWork) const
{ ... }*/ // advc: BtS code deleted


// K-Mod: I've completely butchered this function. ie. deleted the bulk of it, and rewritten it.
void CvCityAI::AI_buildGovernorChooseProduction()
{
	PROFILE_FUNC();

	setChooseProductionDirty(false);
	clearOrderQueue();

	CvPlayerAI& kOwner = GET_PLAYER(getOwner());
	CvArea* pWaterArea = waterArea();
	bool const bDanger = AI_isDanger();

	BuildingTypes eBestBuilding = AI_bestBuildingThreshold(); // go go value cache!
	int iBestBuildingValue = (eBestBuilding == NO_BUILDING) ? 0 :
			AI_buildingValue(eBestBuilding);

	// pop borders
	if (AI_needsCultureToWorkFullRadius())
	{
		if (eBestBuilding != NO_BUILDING && AI_countGoodTiles(true, false) > 0)
		{
			const CvBuildingInfo& kBestBuilding = GC.getInfo(eBestBuilding);
			if (kBestBuilding.getCommerceChange(COMMERCE_CULTURE) +
				kBestBuilding.getObsoleteSafeCommerceChange(COMMERCE_CULTURE) > 0
				&& (GC.getNumCultureLevelInfos() < 2 ||
				getProductionTurnsLeft(eBestBuilding, 0) <=
				GC.getGame().getCultureThreshold((CultureLevelTypes)2)))
			{
				pushOrder(ORDER_CONSTRUCT, eBestBuilding);
				return;
			}
		}
		if (AI_countGoodTiles(true, true, 60) == 0 && AI_chooseProcess(COMMERCE_CULTURE))
			return;
	}

	//workboat
	if (pWaterArea != NULL &&
		kOwner.AI_totalWaterAreaUnitAIs(*pWaterArea, UNITAI_WORKER_SEA) == 0 &&
		AI_neededSeaWorkers() > 0)
	{
		bool bLocalResource = (AI_countNumImprovableBonuses(true, NO_TECH, false, true) > 0);
		if (bLocalResource || iBestBuildingValue < 20)
		{
			int iOdds = 100;
			iOdds *= 50 + iBestBuildingValue;
			iOdds /= 50 + (bLocalResource ? 3 : 5) * iBestBuildingValue;
			if (AI_chooseUnit(UNITAI_WORKER_SEA, iOdds))
			{
				return;
			}
		}
	}

	if (kOwner.AI_isPrimaryArea(getArea())) // if its not a primary area, let the player ship units in.
	{
		//worker
		if (!bDanger)
		{
			int iExistingWorkers = kOwner.AI_totalAreaUnitAIs(getArea(), UNITAI_WORKER);
			int iNeededWorkers = kOwner.AI_neededWorkers(getArea());

			if (iExistingWorkers < (iNeededWorkers + 2)/3) // I don't want to build more workers than the player actually wants.
			{
				int iOdds = 100;
				iOdds *= iNeededWorkers - iExistingWorkers;
				iOdds /= std::max(1, iNeededWorkers);
				iOdds *= 50 + iBestBuildingValue;
				iOdds /= 50 + 5 * iBestBuildingValue;

				if (AI_chooseUnit(UNITAI_WORKER, iOdds))
				{
					return;
				}
			}
		}

		// adjust iBestBuildValue for the remaining comparisons. (military and spies.)
		if (GC.getNumEraInfos() > 1)
		{
			FAssert(kOwner.getCurrentEra() < GC.getNumEraInfos());
			iBestBuildingValue *= 2 * (GC.getNumEraInfos() - 1) - kOwner.getCurrentEra();
			iBestBuildingValue /= GC.getNumEraInfos() - 1;
		}

		//military
		bool bWar = getArea().getAreaAIType(kOwner.getTeam()) != AREAAI_NEUTRAL;
		/*	(I'd like to check AI_neededFloatingDefenders, but I don't want to
			have to calculate it just for this singluar case.) */
		if (bDanger || iBestBuildingValue < (bWar ? 70 : 35))
		{
			int iOdds = (bWar ? 100 : 60) - kOwner.AI_unitCostPerMil()/2;
			iOdds += AI_experienceWeight();
			iOdds *= 100 + 2*getMilitaryProductionModifier();
			iOdds /= 100;

			iOdds *= 60 + iBestBuildingValue;
			iOdds /= 60 + 10 * iBestBuildingValue;

			if (SyncRandSuccess100(iOdds))
			{
				UnitAITypes eUnitAI;
				UnitTypes eBestUnit = AI_bestUnit(false, NO_ADVISOR, &eUnitAI);
				if (eBestUnit != NO_UNIT)
				{
					CvUnitInfo const& kUnit = GC.getInfo(eBestUnit);
					if (kUnit.getUnitCombatType() != NO_UNITCOMBAT)
					{
						BuildingTypes eExperienceBuilding = AI_bestBuildingThreshold(
								BUILDINGFOCUS_EXPERIENCE);
						if (eExperienceBuilding != NO_BUILDING)
						{
							const CvBuildingInfo& kBuilding = GC.getInfo(eExperienceBuilding);
							if (kBuilding.getFreeExperience() > 0 ||
								kBuilding.getUnitCombatFreeExperience(kUnit.getUnitCombatType()) > 0 ||
								kBuilding.getDomainFreeExperience(kUnit.getDomainType()) > 0)
							{
								// This building helps the unit we want
								// ...so do the building first.
								pushOrder(ORDER_CONSTRUCT, eBestBuilding);
								return;
							}
						}
					}
					// otherwise, we're ready to build the unit
					pushOrder(ORDER_TRAIN, eBestUnit, eUnitAI);
					return;
				}
			}
		}

		//spies
		if (!kOwner.AI_isAreaAlone(getArea()))
		{
			int iNumSpies = kOwner.AI_totalAreaUnitAIs(getArea(), UNITAI_SPY);
					// advc.001j: Commented out
					//+ kOwner.AI_getNumTrainAIUnits(UNITAI_SPY);
			int iNeededSpies = 2 + getArea().getCitiesPerPlayer(kOwner.getID()) / 5;
			iNeededSpies += kOwner.getCommercePercent(COMMERCE_ESPIONAGE)/20;

			if (iNumSpies < iNeededSpies)
			{
				int iOdds = 35 - iBestBuildingValue/3;
				if (iOdds > 0)
				{
					iOdds *= (40 + iBestBuildingValue);
					iOdds /= (20 + 3 * iBestBuildingValue);
					iOdds *= iNeededSpies;
					iOdds /= (4*iNumSpies+iNeededSpies);
					if (AI_chooseUnit(UNITAI_SPY, iOdds))
					{
						return;
					}
				}
			}
		}

		//spread
		int iSpreadUnitOdds = std::max(0, 80 - iBestBuildingValue*2);

		int iSpreadUnitThreshold = 1200 + (bWar ? 800: 0) + iBestBuildingValue * 25;
		// is it wrong to use UNITAI values for human players?
		iSpreadUnitThreshold += kOwner.AI_totalAreaUnitAIs(getArea(), UNITAI_MISSIONARY) * 1000;

		UnitTypes eBestSpreadUnit = NO_UNIT;
		int iBestSpreadUnitValue = -1;
		if (AI_bestSpreadUnit(true, true, iSpreadUnitOdds, &eBestSpreadUnit, &iBestSpreadUnitValue))
		{
			if (iBestSpreadUnitValue > iSpreadUnitThreshold)
			{
				if (AI_chooseUnit(eBestSpreadUnit, UNITAI_MISSIONARY))
				{
					return;
				}
				FErrorMsg("AI_bestSpreadUnit should provide a valid unit when it returns true");
			}
		}
	}

	//process
	ProcessTypes eBestProcess = AI_bestProcess();
	if (eBestProcess != NO_PROCESS)
	{
		// similar to AI_chooseProduction
		int iOdds = 100;
		if (eBestBuilding != NO_BUILDING)
		{	// <advc.004x>
			int iConstructionTurns = getProductionTurnsLeft(eBestBuilding, 0);
			if(iConstructionTurns == MAX_INT)
				iOdds = 0;
			else // </advc.004x>
			{
				int iBuildingCost = AI_processValue(eBestProcess) * iConstructionTurns;
				int iScaledTime = 10000 * iBuildingCost /
						(std::max(1, iBestBuildingValue) *
						GC.getInfo(GC.getGame().getGameSpeedType()).getConstructPercent());
				// <= 4 turns means 0%. 20 turns ~ 61%.
				iOdds = 100 * (iScaledTime - 400) / (iScaledTime + 600);
			}
		}
		if (SyncRandSuccess100(iOdds))
		{
			pushOrder(ORDER_MAINTAIN, eBestProcess);
			return;
		}
	}

	//default
	if (AI_chooseBuilding())
		return;

	/*if (AI_chooseProcess())
		return; */

	if (AI_chooseUnit())
		return;
}

/*	K-Mod: This is a chunk of code that I moved out of AI_chooseProduction.
	The only reason I've moved it is to reduce clutter in the other function. */
void CvCityAI::AI_barbChooseProduction()
{
	const CvPlayerAI& kPlayer = GET_PLAYER(getOwner());

	CvArea const* pWaterArea = waterArea(true);
	bool bMaybeWaterArea = false;
	bool bWaterDanger = false;
	if (pWaterArea != NULL)
	{
		bMaybeWaterArea = true;
		if (!GET_TEAM(getTeam()).AI_isWaterAreaRelevant(*pWaterArea))
			pWaterArea = NULL;

		bWaterDanger = kPlayer.AI_isAnyWaterDanger(getPlot(), 4);
	}
	int const iWaterPercent = AI_calculateWaterWorldPercent();
	bool const bDanger = AI_isDanger();
	int const iNumCitiesInArea = getArea().getCitiesPerPlayer(getOwner());
	int const iExistingWorkers = kPlayer.AI_totalAreaUnitAIs(getArea(), UNITAI_WORKER);
	int const iNeededWorkers = kPlayer.AI_neededWorkers(getArea());

	int iBuildUnitProb = AI_buildUnitProb();

	if (!AI_isDefended(getPlot().plotCount(
		PUF_isUnitAIType, UNITAI_ATTACK, -1, getOwner()))) // XXX check for other team's units?
	{
		if (AI_chooseDefender())
			return;
		if (AI_chooseUnit(UNITAI_ATTACK))
			return;
	}

	// advc.303: Disabled.
	// K-Mod. Allow barbs to pop their borders when they can.
	//if (getCultureLevel() <= 1 && AI_chooseProcess(COMMERCE_CULTURE))
		//return;
	// K-Mod end
	// advc.305:
	int iCityAge = GC.getGame().getGameTurn() - getGameTurnAcquired();

	if (!bDanger && (2*iExistingWorkers < iNeededWorkers) && (AI_getWorkersNeeded() > 0) && (AI_getWorkersHave() == 0))
	{
		// <advc.305>
		int iPopThresh = 3; // was 2
		int iTimeThresh = isCoastal() ? 25 : 20; // was 15 flat
		int iTrainPercent = GC.getInfo(GC.getGame().
				getGameSpeedType()).getTrainPercent();
		if (getPopulation() >= iPopThresh ||
			iCityAge > (iTimeThresh * iTrainPercent) / 100) // </advc.305>
		{
			if (AI_chooseUnit(UNITAI_WORKER))
			{
				if (gCityLogLevel >= 2) logBBAI("      City %S uses barb choose worker 1", getName().GetCString());
				return;
			}
		}
	}
	if (!bDanger && !bWaterDanger &&
		(getPopulation() > 1 || iCityAge >= 12)) // advc.305
	{
		// advc.opt: Sea worker counts moved down; only needed here.
		int iNeededSeaWorkers = (bMaybeWaterArea) ? AI_neededSeaWorkers() : 0;
		int iExistingSeaWorkers = (waterArea(true) != NULL) ?
				kPlayer.AI_totalWaterAreaUnitAIs(*waterArea(true), UNITAI_WORKER_SEA) : 0;
		if (iNeededSeaWorkers > 0 &&
			iExistingSeaWorkers <= 0 )// advc.001: safer (as in AI_chooseProduction)
		{
			if (AI_chooseUnit(UNITAI_WORKER_SEA))
			{
				if (gCityLogLevel >= 2) logBBAI("      City %S uses barb choose worker sea 1", getName().GetCString());
				return;
			}
		}
	}
	{
		int iFreeLandExperience = getSpecialistFreeExperience() +
				getDomainFreeExperience(DOMAIN_LAND);
		iBuildUnitProb += (3 * iFreeLandExperience);
	}
	//bool bRepelColonists = false; // advc.300: no longer used
	if (getArea().getNumCities() > getArea().getCitiesPerPlayer(BARBARIAN_PLAYER) + 2)
	{
		if (getArea().getCitiesPerPlayer(BARBARIAN_PLAYER) > getArea().getNumCities()/3)
		{
			//bRepelColonists = true;
			// New world scenario with invading colonists ... fight back!
			iBuildUnitProb += 8*(getArea().getNumCities() - getArea().getCitiesPerPlayer(BARBARIAN_PLAYER));
		}
	}

	if (!bDanger && !SyncRandSuccess100(iBuildUnitProb))
	{
		int iBarbarianFlags = 0;
		if (getPopulation() < 4)
			iBarbarianFlags |= BUILDINGFOCUS_FOOD;
		iBarbarianFlags |= BUILDINGFOCUS_PRODUCTION;
		iBarbarianFlags |= BUILDINGFOCUS_EXPERIENCE;
		if (getPopulation() > 3)
			iBarbarianFlags |= BUILDINGFOCUS_DEFENSE;

		if (AI_chooseBuilding(iBarbarianFlags, 15))
		{
			if (gCityLogLevel >= 2) logBBAI("      City %S uses barb AI_chooseBuilding with flags and iBuildUnitProb = %d", getName().GetCString(), iBuildUnitProb);
			return;
		}
		if (!SyncRandSuccess100(iBuildUnitProb))
		{
			if (AI_chooseBuilding())
			{
				if (gCityLogLevel >= 2) logBBAI("      City %S uses barb AI_chooseBuilding without flags and iBuildUnitProb = %d", getName().GetCString(), iBuildUnitProb);
				return;
			}
		}
	}

	if (getPlot().plotCount(PUF_isUnitAIType, UNITAI_ASSAULT_SEA, -1, getOwner()) > 0)
	{
		if (AI_chooseUnit(UNITAI_ATTACK_CITY))
		{
			if (gCityLogLevel >= 2) logBBAI("      City %S uses barb choose attack city for transports", getName().GetCString());
			return;
		}
	}

	if (!bDanger && pWaterArea != NULL && iWaterPercent > 30)
	{
		if (SyncRandOneChanceIn(3)) // AI Coast Raiders
		{
			if (kPlayer.AI_totalUnitAIs(UNITAI_ASSAULT_SEA) <= 1 + kPlayer.getNumCities() / 2)
			{
				if (AI_chooseUnit(UNITAI_ASSAULT_SEA))
				{
					if (gCityLogLevel >= 2) logBBAI("      City %S uses barb choose transport", getName().GetCString());
					return;
				}
			}
		}
		if (SyncRandNum(110) < iWaterPercent + 10)
		{
			if (kPlayer.AI_totalUnitAIs(UNITAI_PIRATE_SEA) <= kPlayer.getNumCities())
			{
				if (AI_chooseUnit(UNITAI_PIRATE_SEA))
				{
					if (gCityLogLevel >= 2) logBBAI("      City %S uses barb choose pirate", getName().GetCString());
					return;
				}
			}

			if (kPlayer.AI_totalAreaUnitAIs(*pWaterArea, UNITAI_ATTACK_SEA) < iNumCitiesInArea)
			{
				if (AI_chooseUnit(UNITAI_ATTACK_SEA))
				{
					if (gCityLogLevel >= 2) logBBAI("      City %S uses barb choose attack sea", getName().GetCString());
					return;
				}
			}
		}
	}

	if (SyncRandOneChanceIn(2))
	{
		if (!bDanger && iExistingWorkers < iNeededWorkers &&
			AI_getWorkersNeeded() > 0 && AI_getWorkersHave() == 0)
		{
			if (getPopulation() > 1)
			{
				if (AI_chooseUnit(UNITAI_WORKER))
				{
					if (gCityLogLevel >= 2) logBBAI("      City %S uses barb choose worker 2", getName().GetCString());
					return;
				}
			}
		}
	}

	UnitAIWeightMap unitAIWeight; // advc: Was vector of pairs "barbarianTypes"
	unitAIWeight.set(UNITAI_ATTACK, //125
			// <advc.300>
			std::max(65, 100 - 15 *
			getPlot().plotCount(PUF_isUnitAIType, UNITAI_ATTACK, -1, getOwner())));
	AreaAITypes const eAreaAI = getArea().getAreaAIType(getTeam()); // </advc.300>
	unitAIWeight.set(UNITAI_ATTACK_CITY,
			//bRepelColonists ? 100 : 50
			/*	advc.300: (Note that naval invaders for existing transports have
				already been considered above) */
			eAreaAI == AREAAI_OFFENSIVE ? 100 : (eAreaAI != AREAAI_ASSAULT ? 60 : 30));
	unitAIWeight.set(UNITAI_COUNTER, //100
			// <advc.300>
			std::max(25, 100 - 20 *
			getPlot().plotCount(PUF_isUnitAIType, UNITAI_COUNTER, -1, getOwner())));
			// </advc.300>
	unitAIWeight.set(UNITAI_CITY_DEFENSE, //50
			// <advc.300>
			25 + 10 * std::max(0,
			GC.getInfo(GC.getGame().getHandicapType()).getBarbarianInitialDefenders() -
			getPlot().plotCount(PUF_isMissionAIType, MISSIONAI_GUARD_CITY, -1, getOwner())));
			// </advc.300>
	if (AI_chooseLeastRepresentedUnit(unitAIWeight))
		return;

	if (AI_chooseUnit())
		return;
}


int CvCityAI::AI_calculateWaterWorldPercent()
{
	int iFriendlyCities = 0;
	// <advc> Count sibling vassals too
	for (TeamIter<ALIVE,NOT_A_RIVAL_OF> it(getTeam()); it.hasNext(); ++it)
		iFriendlyCities += it->countNumCitiesByArea(getArea());
	if (iFriendlyCities <= 0)
		return 0;
	int const iAreaCities = getArea().getNumCities();
	// Cheats with visiblity, but that was also the case in BtS.
	int const iRivalCities = iAreaCities - iFriendlyCities;
	// </advc>
	int iWaterPercent = 0;
	if (iRivalCities > 0)
	{
		iWaterPercent = 100 -
				(iAreaCities * 100) / std::max(1, GC.getGame().getNumCities());
	}
	else iWaterPercent = 100;
	iWaterPercent *= 50;
	iWaterPercent /= 100;
	iWaterPercent += (50 * (2 + iFriendlyCities)) / (2 + iAreaCities);
	iWaterPercent = std::max(1, iWaterPercent);
	return iWaterPercent;
}

//Please note, takes the yield multiplied by 100
int CvCityAI::AI_getYieldMagicValue(const int* piYieldsTimes100, bool bHealthy) const
{
	FAssert(piYieldsTimes100 != NULL);

	int iPopEats = GC.getFOOD_CONSUMPTION_PER_POPULATION();
	iPopEats += (bHealthy ? 0 : 1);
	iPopEats *= 100;
	int iValue = (piYieldsTimes100[YIELD_FOOD] * 95 + // advc.121: was *100
			piYieldsTimes100[YIELD_PRODUCTION] * 70 + // K-Mod: was *55 in BBAI and BtS
			piYieldsTimes100[YIELD_COMMERCE] * 40 -
			iPopEats * 100); // advc.121: was *102
	iValue /= 100;
	return iValue;
}

/*	The magic value is basically "Look at this plot, is it worth working"
	-50 or lower means the plot is worthless in a "workers kill yourself" kind of way.
	-50 to -1 means the plot isn't worth growing to work - might be okay with emphasize though.
	Between 0 and 50 means it is marginal.
	50-100 means it's okay.
	Above 100 means it's definitely decent - seriously question ever not working it.
	This function deliberately doesn't use emphasize settings. */
int CvCityAI::AI_getPlotMagicValue(CvPlot const& kPlot, bool bHealthy, bool bWorkerOptimization) const // advc: const CvPlot
{	// <k146>
	int aiYields[NUM_YIELD_TYPES];
	bool bFinalBuildAssumed = (bWorkerOptimization &&
			kPlot.getWorkingCity() == this &&
			AI_getBestBuild(getCityPlotIndex(kPlot)) != NO_BUILD);

	FOR_EACH_ENUM(Yield)
	{
		if (bFinalBuildAssumed)
		{
			aiYields[eLoopYield] = kPlot.getYieldWithBuild(AI_getBestBuild(
					getCityPlotIndex(kPlot)), eLoopYield, true)
					* 100; // advc.001: times-100 scale!
		}
		else aiYields[eLoopYield] = kPlot.getYield(eLoopYield) * 100;
	}
	ImprovementTypes eCurrentImprovement = kPlot.getImprovementType();
	if (eCurrentImprovement != NO_IMPROVEMENT && !bFinalBuildAssumed)
	{
		int aiYieldDiffs[NUM_YIELD_TYPES] = {};
		AI_finalImprovementYieldDifference(kPlot, aiYieldDiffs);
		// Remember, aiYields has values *100.
		FOR_EACH_ENUM(Yield)
		{
			//aiYields[eLoopYield] += bWorkerOptimization ? aiYieldDiffs[eLoopYield]*100 : aiYieldDiffs[eLoopYield]*50;
			aiYields[eLoopYield] += aiYieldDiffs[eLoopYield] * 100; //  Just use the final values.
 		}
	} // </k146>
	return AI_getYieldMagicValue(aiYields, bHealthy);
}

//useful for deciding whether or not to grow... or whether the city needs terrain
//improvement.
//if healthy is false it assumes bad health conditions.
int CvCityAI::AI_countGoodTiles(bool bHealthy, bool bUnworkedOnly, int iThreshold, bool bWorkerOptimization) const
{
	//PROFILE_FUNC(); // advc.opt: Apparently not responsible for AI_yieldValue being somewhat slow
	int iCount = 0;

	for (CityPlotIter it(*this, false); it.hasNext(); ++it)
	{
		CvPlot const& kPlot = *it;
		//if (kPlot.getWorkingCity() == this)
		// <advc.113> Anticipate border expansion
		bool bValid = (kPlot.getWorkingCity() == this);
		if(!bValid && kPlot.getOwner() == NO_PLAYER &&
			getCultureLevel() == 1 && getCultureTurnsLeft() <= 5)
		{
			bValid = true;
		}
		if(!bValid)
			continue; // </advc.113>

		if (!bUnworkedOnly || !kPlot.isBeingWorked())
		{
			if (AI_getPlotMagicValue(kPlot, bHealthy,
				/* <k146> */ bWorkerOptimization /* </k146> */) > iThreshold)
			{
				iCount++;
			}
		}
	}
	return iCount;
}

/* disabled by K-Mod. (this function always returns 1, so I've decided not to use it at all)
int CvCityAI::AI_calculateTargetCulturePerTurn() const
{ ... } */ // advc: BtS code deleted


int CvCityAI::AI_countGoodSpecialists(bool bHealthy) const
{
	CvPlayerAI& kPlayer = GET_PLAYER(getOwner());
	int iCount = 0;
	FOR_EACH_ENUM2(Specialist, eSpecialist)
	{
		int iValue = 0;

		iValue += 100 * kPlayer.specialistYield(eSpecialist, YIELD_FOOD);
		iValue += 65 * kPlayer.specialistYield(eSpecialist, YIELD_PRODUCTION);
		iValue += 40 * kPlayer.specialistYield(eSpecialist, YIELD_COMMERCE);

		iValue += 40 * kPlayer.specialistCommerce(eSpecialist, COMMERCE_RESEARCH);
		iValue += 40 * kPlayer.specialistCommerce(eSpecialist, COMMERCE_GOLD);
		iValue += 20 * kPlayer.specialistCommerce(eSpecialist, COMMERCE_ESPIONAGE);
		iValue += 15 * kPlayer.specialistCommerce(eSpecialist, COMMERCE_CULTURE);
		iValue += 25 * getSpecialistGreatPeopleRateChange(eSpecialist); // doc: specialist great people rate change from different sources

		if (iValue >= (bHealthy ? 200 : 300))
		{
			//iCount += getMaxSpecialistCount(eSpecialist);
			// K-Mod
			if (kPlayer.isSpecialistValid(eSpecialist) ||
				eSpecialist == GC.getDEFAULT_SPECIALIST())
			{
				return getPopulation(); // unlimited
			}
			int iDelta = getMaxSpecialistCount(eSpecialist)
					- getSpecialistCount(eSpecialist);
			/*  <advc.006> CvTeam::doResearch can obsolete a building
				(Egyptian Obelisk; any others?) and then, apparently,
				CvCityAI::AI_updateAssignWork isn't called soon enough.
				Not really a problem I guess. */
			if (iDelta < 0)
			{
				FAssert(AI_isAssignWorkDirty());
				iDelta = 0;
			} // </advc.006>
			iCount += iDelta;
			// K-Mod end
		}
	}
	//iCount -= getFreeSpecialist();
	iCount -= totalFreeSpecialists(); // K-Mod

	//return iCount;
	return std::max(0, iCount); // K-Mod
}

// return value: 0 is normal. greater than 0 has a special meaning.
/*	(K-Mod todo: this function is currently only used for CvCityAI::AI_stealPlots,
	and even there it is only used in a very binary way.
	I think I can make this function more versatile, and
	then use it to bring some consistency to other parts of the code.) */
int CvCityAI::AI_getCityImportance(bool bEconomy, bool bMilitary)
{
	int iValue = 0;
	if (GET_PLAYER(getOwner()).AI_atVictoryStage(
		AI_VICTORY_CULTURE3)) // K-Mod (was culture2 in BBAI)
	{
		int iCultureRateRank = findCommerceRateRank(COMMERCE_CULTURE);
		int iCulturalVictoryNumCultureCities = GC.getGame().culturalVictoryNumCultureCities();

		if (iCultureRateRank <= iCulturalVictoryNumCultureCities)
		{
			iValue += 100;
			if (getCultureLevel() < CvCultureLevelInfo::finalCultureLevel())
				iValue += !bMilitary ? 100 : 0;
			else iValue += bMilitary ? 100 : 0;
		}
	}
	return iValue;
}


void CvCityAI::AI_stealPlots()
{
	PROFILE_FUNC();

	int iImportance = AI_getCityImportance(true, false);
	for (CityPlotIter it(*this); it.hasNext(); ++it)
	{
		CvPlot& kPlot = *it;
		if (iImportance > 0 && kPlot.getOwner() == getOwner())
		{
			CvCityAI* pWorkingCity = kPlot.AI_getWorkingCity();
			if (pWorkingCity != this && pWorkingCity != NULL)
			{
				FAssert(pWorkingCity->getOwner() == getOwner());
				if (iImportance > pWorkingCity->AI_getCityImportance(true, false))
					kPlot.setWorkingCityOverride(this);
			}
		}

		if (kPlot.getWorkingCityOverride() == this &&
			kPlot.getOwner() != getOwner())
		{
			kPlot.setWorkingCityOverride(NULL);
		}
	}
}



// original description (obsolete):
/*	+1/+3/+5 plot based on base food yield (1/2/3)
	+4 if being worked.
	+4 if a bonus.
	Unworked ocean ranks very lowly. Unworked lake ranks at 3. Worked lake at 7.
	Worked bonus in ocean ranks at like 11 */
//int CvCityAI::AI_buildingSpecialYieldChangeValue(BuildingTypes kBuilding, YieldTypes eYield) const

/*	K-Mod: I've rewritten this function to give a lower but more consistent value.
	The function should return roughly 4x the number of affected plots which are
	expected to be worked.
	+4 if either being worked, or would be good after the extra yield.
	(~consumption rate +4 commerce / 2 yield)
	+2 to +3 if would be ok after the extra yield.
	(~consumption rate +2 commerce / 1 yield)
	+1 otherwise */
int CvCityAI::AI_buildingSeaYieldChangeWeight(BuildingTypes eBuilding, bool bGrowing) const
{
	int iValue = 0;
	CvBuildingInfo const& kBuilding = GC.getInfo(eBuilding);

	/*	only add the building's yield if it isn't already built -
		otherwise the building will be overvalued for sabotage missions. */
	bool const bAddBuilding = (getNumBuilding(eBuilding) <
			GC.getDefineINT(CvGlobals::CITY_MAX_NUM_BUILDINGS));
	int const iCommerceValue = 4;
	int const iProdValue = 7;
	int const iFoodValue = 11;
	int const iBaseValue = iFoodValue * GC.getFOOD_CONSUMPTION_PER_POPULATION();
	// <advc.131>
	int iDecentUnworkedLand = 0;
	// Count plots not currently worked separately
	int iPotentialValue = 0; // </advc.131>
	for (WorkablePlotIter it(*this); it.hasNext(); ++it)
	{
		CvPlot const& kPlot = *it;
		if (kPlot.isWater())
		{
			if (kPlot.isBeingWorked())
			{
				iValue += 4;
				continue;
			}
		}
		else if (kPlot.isBeingWorked())
			continue;
		bool bAddYield = (bAddBuilding && kPlot.isWater()); // advc.131
		int iPlotValue =
				iFoodValue * (kPlot.getYield(YIELD_FOOD) +
				(bAddYield ? kBuilding.getSeaPlotYieldChange(YIELD_FOOD) : 0)) +
				iProdValue * (kPlot.getYield(YIELD_PRODUCTION) +
				(bAddYield ? kBuilding.getSeaPlotYieldChange(YIELD_PRODUCTION) : 0)) +
				iCommerceValue * (kPlot.getYield(YIELD_COMMERCE) +
				(bAddYield ? kBuilding.getSeaPlotYieldChange(YIELD_COMMERCE) : 0));
		// <advc.131> Threshold corresponds to a flat Grassland Cottage
		if (!kPlot.isWater() && iPlotValue >= iBaseValue + iCommerceValue)
		{
			iDecentUnworkedLand++;
			continue;
		} // </advc.131>
		if (iPlotValue > iBaseValue + 3 * iCommerceValue)
			iPotentialValue += 4;
		else if (iPlotValue >= iBaseValue + 2 * iCommerceValue)
			iPotentialValue += (bGrowing ? 3 : 2);
		else iPotentialValue += 1;
	}
	// <advc.131>
	iPotentialValue *= std::max(2, 10 - iDecentUnworkedLand);
	iPotentialValue /= 10; // </advc.131>
	return iValue + iPotentialValue;
}


int CvCityAI::AI_yieldMultiplier(YieldTypes eYield) const
{
	PROFILE_FUNC();

	int iMultiplier = getBaseYieldRateModifier(eYield);
	if (eYield == YIELD_PRODUCTION)
		iMultiplier += (getMilitaryProductionModifier() / 2);

	if (eYield == YIELD_COMMERCE)
	{
		/*iMultiplier += (getCommerceRateModifier(COMMERCE_RESEARCH) * 60) / 100;
		iMultiplier += (getCommerceRateModifier(COMMERCE_GOLD) * 35) / 100;
		iMultiplier += (getCommerceRateModifier(COMMERCE_CULTURE) * 15) / 100;*/ // BtS
		// K-Mod
		// this breakdown seems wrong... lets try it a different way.
		const CvPlayer& kPlayer = GET_PLAYER(getOwner());
		int iExtra = 0;
		FOR_EACH_ENUM(Commerce)
		{
			iExtra += getTotalCommerceRateModifier(eLoopCommerce) *
					kPlayer.getCommercePercent(eLoopCommerce);
		}
		// base commerce modifier compounds with individual commerce modifiers.
		iMultiplier *= iExtra;
		iMultiplier /= 10000;
		// K-Mod end
	}

	return iMultiplier;
}

/*	This should be called before doing governor stuff.
	This is the function which replaces emphasis.
	Could stand for a Commerce Variety to be added,
	especially now that there is Espionage. */
void CvCityAI::AI_updateSpecialYieldMultiplier()
{
	PROFILE_FUNC();

	int iOldProductionMult = m_aiSpecialYieldMultiplier[YIELD_PRODUCTION]; // advc.121
	FOR_EACH_ENUM(Yield)
		m_aiSpecialYieldMultiplier[eLoopYield] = 0;

	UnitTypes eProductionUnit = getProductionUnit();
	if (eProductionUnit != NO_UNIT)
	{
		/*if (GC.getInfo(eProductionUnit).getDefaultUnitAIType() == UNITAI_WORKER_SEA) {
			m_aiSpecialYieldMultiplier[YIELD_PRODUCTION] += 50;
			m_aiSpecialYieldMultiplier[YIELD_COMMERCE] -= 50;
		}
		if ((GC.getInfo(eProductionUnit).getDefaultUnitAIType() == UNITAI_WORKER) ||
			(GC.getInfo(eProductionUnit).getDefaultUnitAIType() == UNITAI_SETTLE))
			m_aiSpecialYieldMultiplier[YIELD_COMMERCE] -= 50;*/ // BtS
		// K-Mod. note: when food is production, food is counted as production!
		UnitAITypes eUnitAI = GC.getInfo(eProductionUnit).getDefaultUnitAIType();
		if (eUnitAI == UNITAI_WORKER_SEA ||
			eUnitAI == UNITAI_WORKER || eUnitAI == UNITAI_SETTLE)
		{
			m_aiSpecialYieldMultiplier[YIELD_PRODUCTION] += 50;
			m_aiSpecialYieldMultiplier[YIELD_COMMERCE] -= 25;
		}
		// K-Mod end
	} // <advc.300>
	if (isBarbarian())
	{
		int iCommerceToProductionShift = AI_commerceToProductionMultiplierShift();
		m_aiSpecialYieldMultiplier[YIELD_PRODUCTION] += iCommerceToProductionShift;
		m_aiSpecialYieldMultiplier[YIELD_COMMERCE] -= iCommerceToProductionShift;
		return;
	} // </advc.300>

	BuildingTypes eProductionBuilding = getProductionBuilding();
	if (eProductionBuilding != NO_BUILDING)
	{
		if (GC.getInfo(eProductionBuilding).isWorldWonder() || isProductionProject())
		{
			m_aiSpecialYieldMultiplier[YIELD_PRODUCTION] += 50;
			m_aiSpecialYieldMultiplier[YIELD_COMMERCE] -= 25;
		}
		m_aiSpecialYieldMultiplier[YIELD_PRODUCTION] += std::max(-25,
				//GC.getInfo(eProductionBuilding).getFoodKept()
				GET_PLAYER(getOwner()).getFoodKept(eProductionBuilding)); // advc.912d

		/*if ((GC.getInfo(eProductionBuilding).getCommerceChange(COMMERCE_CULTURE) > 0)
			|| (GC.getInfo(eProductionBuilding).getObsoleteSafeCommerceChange(COMMERCE_CULTURE) > 0)) {
			int iTargetCultureRate = AI_calculateTargetCulturePerTurn();
			if (iTargetCultureRate > 0) {
				if (getCommerceRate(COMMERCE_CULTURE) == 0)
					m_aiSpecialYieldMultiplier[YIELD_PRODUCTION] += 50;
				else if (getCommerceRate(COMMERCE_CULTURE) < iTargetCultureRate)
					m_aiSpecialYieldMultiplier[YIELD_PRODUCTION] += 20;
			}
		}*/ // BtS - emphasising production to get culture is nice, but not if it slows growth
	}

	if (isHuman())
		return;
	// non-human production value increase

	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());
	AreaAITypes const eAreaAIType = getArea().getAreaAIType(getTeam());

	// K-Mod. special strategy / personality adjustments
	// <advc> Moved into subroutine
	{
		int iCommerceToProductionShift = AI_commerceToProductionMultiplierShift();
		m_aiSpecialYieldMultiplier[YIELD_PRODUCTION] += iCommerceToProductionShift;
		m_aiSpecialYieldMultiplier[YIELD_COMMERCE] -= iCommerceToProductionShift;
	} // </advc>
	if (kOwner.AI_getFlavorValue(FLAVOR_PRODUCTION) > 0)
	{
		m_aiSpecialYieldMultiplier[YIELD_PRODUCTION] += 5 +
				2 * kOwner.AI_getFlavorValue(FLAVOR_PRODUCTION);
	}
	if (kOwner.AI_isDoStrategy(AI_STRATEGY_ECONOMY_FOCUS))
	{
		m_aiSpecialYieldMultiplier[YIELD_PRODUCTION] -= 10;
		m_aiSpecialYieldMultiplier[YIELD_COMMERCE] += 20;
	}  // advc.001: was AI_isDoVictoryStrategy
	else if (kOwner.AI_isDoStrategy(AI_STRATEGY_GET_BETTER_UNITS)) // doesn't stack with ec focus.
	{
		m_aiSpecialYieldMultiplier[YIELD_COMMERCE] += 20;
	} // K-Mod end
	// advc: Moved down
	if (kOwner.AI_atVictoryStage(AI_VICTORY_CULTURE1 | AI_VICTORY_SPACE1))
		m_aiSpecialYieldMultiplier[YIELD_COMMERCE] += 5;

	if ((kOwner.AI_isDoStrategy(AI_STRATEGY_DAGGER) && getPopulation() >= 4) ||
		(eAreaAIType == AREAAI_OFFENSIVE) || (eAreaAIType == AREAAI_DEFENSIVE) ||
		(eAreaAIType == AREAAI_MASSING) || (eAreaAIType == AREAAI_ASSAULT))
	{
		/*m_aiSpecialYieldMultiplier[YIELD_PRODUCTION] += 10;
		if (!kOwner.AI_isFinancialTrouble())
			m_aiSpecialYieldMultiplier[YIELD_COMMERCE] -= 40;*/ // BtS
		// K-Mod. Don't sacrifice lots of commerce unless we're on the defensive, or this is 'total war'.
		// advc.018: Removed crush from the isDoStrategy call
		m_aiSpecialYieldMultiplier[YIELD_PRODUCTION] += kOwner.
				AI_isDoStrategy(AI_STRATEGY_DAGGER | AI_STRATEGY_TURTLE) ? 20 : 10;
		if (eAreaAIType != AREAAI_NEUTRAL && !kOwner.AI_isFinancialTrouble() &&
			!kOwner.AI_isDoStrategy(AI_STRATEGY_ECONOMY_FOCUS | AI_STRATEGY_GET_BETTER_UNITS))
		{
			bool bSeriousWar = (eAreaAIType == AREAAI_DEFENSIVE || kOwner.isBarbarian());
			for (TeamIter<CIV_ALIVE,KNOWN_POTENTIAL_ENEMY_OF> itEnemy(getTeam());
				!bSeriousWar && itEnemy.hasNext(); ++itEnemy)
			{
				WarPlanTypes eWarPlan = GET_TEAM(getTeam()).AI_getWarPlan(itEnemy->getID());
				bSeriousWar = (eWarPlan == WARPLAN_PREPARING_TOTAL || eWarPlan == WARPLAN_TOTAL);
			}
			m_aiSpecialYieldMultiplier[YIELD_COMMERCE] -= (bSeriousWar ? 35 : 10);
		} // K-Mod end
	}

	//int iIncome = 1 + kOwner.getCommerceRate(COMMERCE_GOLD) + kOwner.getCommerceRate(COMMERCE_RESEARCH) + std::max(0, kOwner.getGoldPerTurn());
	int iIncome = 1 + kOwner.AI_getAvailableIncome(); // K-Mod
	int iExpenses = 1 + kOwner.calculateInflatedCosts() +
			//-std::min(0, kOwner.getGoldPerTurn());
			// K-Mod (just to be consistent with similar calculations)
			std::max(0, -kOwner.getGoldPerTurn());
	FAssert(iIncome > 0);

	int iRatio = (100 * iExpenses) / iIncome;
	/*	Gold -> Production Reduced To
		40- -> 100%; 60 -> 83%; 100 -> 28%; 110+ -> 14% */
	m_aiSpecialYieldMultiplier[YIELD_PRODUCTION] += 100;
	if (iRatio > 60)
	{	//Greatly decrease production weight
		m_aiSpecialYieldMultiplier[YIELD_PRODUCTION] *= std::max(10, 120 - iRatio);
		m_aiSpecialYieldMultiplier[YIELD_PRODUCTION] /= 72;
	}
	else if (iRatio > 40)
	{	//Slightly decrease production weight.
		m_aiSpecialYieldMultiplier[YIELD_PRODUCTION] *= 160 - iRatio;
		m_aiSpecialYieldMultiplier[YIELD_PRODUCTION] /= 120;
	}
	m_aiSpecialYieldMultiplier[YIELD_PRODUCTION] -= 100;
	// <advc.121> Inertia, to avoid oscillation (not sure if really a problem).
	m_aiSpecialYieldMultiplier[YIELD_PRODUCTION] += iOldProductionMult;
	m_aiSpecialYieldMultiplier[YIELD_PRODUCTION] /= 2; // </advc.121>
}


int CvCityAI::AI_specialYieldMultiplier(YieldTypes eYield) const
{
	return m_aiSpecialYieldMultiplier[eYield];
}

/*	advc: Helper to avoid duplicate code. Cut from AI_getYieldMultipliers/
	AI_updateSpecialYieldMultiplier. A K-Mod comment had said that those two
	should be kept "roughly consistent" with each other and they were performing
	in fact the exact same calculation. Not a nice function name; it's unclear
	to me why other, similar adjustments aren't shared by the two functions as well
	or what the difference between yield multipliers and special yield multipliers
	is even supposed to be. Would need more insight to refactor this better. */
int CvCityAI::AI_commerceToProductionMultiplierShift() const
{
	int iR = 0;
	/*	<advc.300> Delay Cottaging of New World to make it a little less
		attractive for conquerors */
	if (isBarbarian())
	{
		if (getArea().getNumCivCities() <= 0)
		{
			iR += range(CvEraInfo::AI_getAgeOfExploration()
					- GC.getGame().getCurrentEra(), 0, 2) * 10;
		}
		return iR;
	} // </advc.300>
	if (GET_PLAYER(getOwner()).AI_isDoStrategy(AI_STRATEGY_PRODUCTION))
		iR = 20;
	else if (3 * findBaseYieldRateRank(YIELD_PRODUCTION) <=
		GET_PLAYER(getOwner()).getNumCities() &&
		findBaseYieldRateRank(YIELD_PRODUCTION) <
		findBaseYieldRateRank(YIELD_COMMERCE))
	{
		iR = 10;
	}
	return iR;
}

// advc: Similar code had been used (somewhat inconsistently) in several places
bool CvCityAI::AI_needsCultureToWorkFullRadius() const
{
	return (!isDisorder() && getCommerceRate(COMMERCE_CULTURE) <= 0 &&
			getCultureLevel() + 1 <= CITY_PLOTS_RADIUS);
}


int CvCityAI::AI_countNumBonuses(BonusTypes eBonus,
	bool bIncludeOurs, bool bIncludeNeutral, int iOtherCultureThreshold,
	bool bLand, bool bWater) const
{
	FAssert(bLand || bWater); // advc
	int iCount = 0;
	for (CityPlotIter it(*this); it.hasNext(); ++it)
	{
		CvPlot const& kPlot = *it;
		// advc.040 (tbd.): Param for including resources in different land areas?
		// <advc.001> As in AI_countNumImprovableBonuses. BtS hadn't checked bLand.
		if (!((bLand && isArea(kPlot.getArea())) ||
			(bWater && kPlot.isWater())))
		{
			continue; // advc
		}
		BonusTypes eLoopBonus = kPlot.getBonusType(getTeam());
		if (eLoopBonus == NO_BONUS)
			continue;

		if (eBonus != NO_BONUS && eBonus != eLoopBonus)
			continue;

		if (bIncludeOurs && kPlot.getOwner() == getOwner() &&
			kPlot.getWorkingCity() == this)
		{
			iCount++;
		}
		else if (bIncludeNeutral && !kPlot.isOwned())
			iCount++;
		else if (iOtherCultureThreshold > 0 && kPlot.isOwned() &&
			kPlot.getOwner() != getOwner())
		{
			if (kPlot.getCulture(kPlot.getOwner()) - kPlot.getCulture(getOwner()) <
				iOtherCultureThreshold)
			{
				iCount++;
			}
		}
	}
	return iCount;
}

// BBAI (11/14/09, jdog5000): City AI
// K-Mod - rearranged some stuff and fixed some bugs
// advc (tbd.): Some overlap with CvPlayerAI::AI_isUnimprovedBonus -- merge?
int CvCityAI::AI_countNumImprovableBonuses(bool bIncludeNeutral, TechTypes eExtraTech, bool bLand,
	bool bWater) /* advc: */ const
{
	int iCount = 0;
	for (CityPlotIter it(*this, false); it.hasNext(); ++it)
	{
		CvPlot const& kPlot = *it;
		if (!((bLand && isArea(kPlot.getArea())) ||
			(bWater && kPlot.isWater())))
		{
			continue;
		}
		BonusTypes const eLoopBonus = kPlot.getBonusType(getTeam());
		if (eLoopBonus != NO_BONUS &&
			(GET_TEAM(getTeam()).isHasTech((TechTypes)
			GC.getInfo(eLoopBonus).getTechCityTrade()) ||
			GC.getInfo(eLoopBonus).getTechCityTrade() == eExtraTech))
		{
			if ((kPlot.getOwner() == getOwner() &&
				kPlot.getWorkingCity() == this) ||
				(bIncludeNeutral && !kPlot.isOwned()))
			{	// <advc.001>
				ImprovementTypes eCurrentImp = kPlot.getImprovementType();
				if (eCurrentImp != NO_IMPROVEMENT &&
					(GET_TEAM(getTeam()).isBonusObsolete(eLoopBonus) ||
					GET_TEAM(getTeam()).doesImprovementConnectBonus(eCurrentImp, eLoopBonus)))
				{
					continue;
				} // </advc.001>
				FOR_EACH_ENUM(Build)
				{
					ImprovementTypes const eImp = GC.getInfo(eLoopBuild).getImprovement();
					if (eImp == NO_IMPROVEMENT || !kPlot.canBuild(eLoopBuild, getOwner()))
						continue;
					if (GC.getInfo(eImp).isImprovementBonusTrade(eLoopBonus) ||
						GC.getInfo(eImp).isActsAsCity())
					{
						if (GET_PLAYER(getOwner()).canBuild(kPlot, eLoopBuild))
						{	/*  advc.001: If owner can already connect the resource
								but built sth. else instead, then it's probably deliberate. */
							if(eCurrentImp == NO_IMPROVEMENT)
							{
								iCount++;
								break;
							}
						}
						else if (eExtraTech != NO_TECH &&
							GC.getInfo(eLoopBuild).getTechPrereq() == eExtraTech)
						{
							iCount++;
							break;
						}
					}
				}
			}
		}
	}
	return iCount;
}


int CvCityAI::AI_playerCloseness(PlayerTypes eIndex, int iMaxDistance,
	bool bConstCache) const // advc.001n
{
	FAssert(GET_PLAYER(eIndex).isAlive());

	int iCloseness = m_aiPlayerCloseness[eIndex];
	if ((m_aiCachePlayerClosenessTurn[eIndex] != GC.getGame().getGameTurn() ||
		m_aiCachePlayerClosenessDistance[eIndex] != iMaxDistance))
	{
		iCloseness = AI_calculatePlayerCloseness(iMaxDistance,
				eIndex, bConstCache); // advc.001n
	}
	return iCloseness;
}

// advc.opt: Renamed from "AI_cachePlayerCloseness"; no longer updates the whole cache.
// BETTER_BTS_AI_MOD (5/16/10, jdog5000): General AI, closeness changes
int CvCityAI::AI_calculatePlayerCloseness(int iMaxDistance, PlayerTypes ePlayer,
	bool bConstCache) const // advc.001n
{
	PROFILE_FUNC();

	int iCloseness = 0;
	CvPlayer const& kPlayer = GET_PLAYER(ePlayer);

	int iValue = 0;
	int iBestValue = 0;
	CvMap const& kMap = GC.getMap();
	FOR_EACH_CITY(pLoopCity, kPlayer)
	{
		if (pLoopCity == this)
			continue;
		int iDistance = stepDistance(getX(), getY(),
				pLoopCity->getX(), pLoopCity->getY());
		/*  <advc.107> No functional change here. It's OK to use a higher
			search range for cities on other continents; but will have to
			decrease the distance later on when computing the closeness value. */
		bool const bSameArea = sameArea(*pLoopCity);
		if (!bSameArea) // </advc.107>
		{
			iDistance += 1;
			iDistance /= 2;
		}
		if (iDistance > iMaxDistance)
			continue;
		if (bSameArea) // advc.107 (no functional change)
		{
			int iPathDistance = kMap.calculatePathDistance(plot(), pLoopCity->plot());
			if (iPathDistance > 0)
				iDistance = iPathDistance;
			if (iDistance > iMaxDistance)
				continue;
		}
		// Weight by population of both cities, not just pop of other city
		//iTempValue = 20 + 2*pLoopCity->getPopulation();
		int iTempValue = 20 + pLoopCity->getPopulation() + getPopulation();
		iTempValue *= 1 + iMaxDistance - iDistance;
		iTempValue /= 1 + iMaxDistance;
		//reduce for small islands.
		int iAreaCityCount = pLoopCity->getArea().getNumCities();
		iTempValue *= std::min(iAreaCityCount, 5);
		iTempValue /= 5;
		if (iAreaCityCount < 3)
			iTempValue /= 2;
		if (pLoopCity->isBarbarian())
			iTempValue /= 4;
		// <advc.107>
		if(!bSameArea)
			iTempValue /= (pLoopCity->isCoastal() ? 2 : 3); // </advc.107>
		iValue += iTempValue;
		iBestValue = std::max(iBestValue, iTempValue);
	}
	iCloseness = iBestValue + iValue / 4;
	if (!bConstCache) // advc.001n
	{
		m_aiPlayerCloseness[kPlayer.getID()] = iCloseness;
		m_aiCachePlayerClosenessTurn[ePlayer] = GC.getGame().getGameTurn();
		m_aiCachePlayerClosenessDistance[ePlayer] = iMaxDistance;
	}
	return iCloseness;
}

// K-Mod
int CvCityAI::AI_highestTeamCloseness(TeamTypes eTeam, /* advc.001n: */ bool bConstCache) const
{
	int iCloseness = -1;
	for (MemberIter itMember(eTeam); itMember.hasNext(); ++itMember)
	{
		iCloseness = std::max(iCloseness, AI_playerCloseness(
				itMember->getID(), DEFAULT_PLAYER_CLOSENESS,
				bConstCache)); // advc.001n
	}
	return iCloseness;
}

/*K-Mod // advc.003j: unused
// return true if there is an adjacent plot not owned by us.
bool CvCityAI::AI_isFrontlineCity() const {
	FOR_EACH_ADJ_PLOT(getPlot()) {
		if (pAdj != NULL && !pAdj->isWater() && pAdj->getTeam() != getTeam())
			return true;
	}
	return false;
}*/

// K-Mod: (advc.650 - Was unused in K-Mod; now has a use.)
int CvCityAI::AI_calculateMilitaryOutput() const
{
	int iValue = getBaseYieldRate(YIELD_PRODUCTION);
	//UnitTypes eDefaultUnit = getConscriptUnit();
	iValue *= 100 + getMilitaryProductionModifier() + 10 * getProductionExperience();
	iValue /= 100;
	return iValue;
}

/*	K-Mod has made significant structural & function changes to this function.
	(loosely described in the comments throughout the function.) */
int CvCityAI::AI_cityThreat(/*bool bDangerPercent*/) const // advc: param unused
{
	PROFILE_FUNC();

	int iTotalThreat = 0; // was (iValue)
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner()); // K-Mod
	bool const bCrushStrategy = kOwner.AI_isDoStrategy(AI_STRATEGY_CRUSH);

	// advc.001: Exclude unmet players (bugfix?), vassals; K-Mod had only excluded the master.
	for (PlayerAIIter<ALIVE,KNOWN_POTENTIAL_ENEMY_OF> itPlayer(getTeam());
		itPlayer.hasNext(); ++itPlayer)
	{
		CvPlayerAI const& kRival = *itPlayer;

		int iAccessFactor = // (was "iTempValue")
				AI_playerCloseness(kRival.getID(), DEFAULT_PLAYER_CLOSENESS);
		// (this is roughly 20 points for each neighbouring city.)

		// K-Mod
		// Add some more points for each plot the loop player owns in our fat-cross.
		if (iAccessFactor > 0)
		{
			for (CityPlotIter itPlot(*this); itPlot.hasNext(); ++itPlot)
			{
				if (itPlot->getOwner() == kRival.getID())
				{
					iAccessFactor += (stepDistance(plot(), &(*itPlot)) <= 1 ? 2 : 1);
				}
			}
		}

		// Evaluate the posibility of a naval assault.
		if (isCoastal( // advc.131: Area size threshold was 10, now 20
			2 * GC.getDefineINT(CvGlobals::MIN_WATER_SIZE_FOR_OCEAN)))
		{
			/*	This evaluation may be expensive (when I finish writing it),
				so only do it if there is reason to be concerned. */
			if (kOwner.AI_atVictoryStage4() ||
				GET_TEAM(getTeam()).AI_getWarPlan(kRival.getTeam()) != NO_WARPLAN ||
				(!kOwner.AI_isLandWar(getArea()) &&
				//kLoopPlayer.AI_getAttitude(getOwner()) < ATTITUDE_PLEASED))
				/*  <advc.109> Don't presume human attitude. Using PLEASED as the
					AI threshold (instead of calling CvTeamAI::AI_isAvoidWar)
					seems OK as the AI tends to be reluctant to start naval wars. */
				((kRival.isHuman() && kOwner.AI_getAttitude(kRival.getID()) < ATTITUDE_FRIENDLY) ||
				(!kRival.isHuman() && kRival.AI_getAttitude(getOwner()) < ATTITUDE_PLEASED))))
				// </advc.109>
			{
				int iNavalAccess = 0;

				//PROFILE("AI_cityThreat naval assault");
				/*	(temporary calculation based on the original bts code.
					I intend to make this significantly more detailed - eventually.) */
				/*int iCurrentEra = kOwner.getCurrentEra();
				iValue += std::max(0, ((10 * iCurrentEra) / 3) - 6);*/
				int iEra = GC.getGame().getCurrentEra();
				iNavalAccess += std::max(0,
						30 * (iEra + 1) / (GC.getNumEraInfos() + 1) - 10);
				iAccessFactor = std::max(iAccessFactor, iNavalAccess);
			}
		}
		// K-Mod end

		if (iAccessFactor > 0)
		{
			/*	K-Mod. (originally the following code had
				iTempValue *= foo; rather than iCivFactor = foo;) */
			int iCivFactor=0;
			/*  advc.018: Commented out. I don't see why crush should make us
				more protective of our cities. The
				if(bCrushStrategy) iCivFactor/=2 a bit farther down seems to be
				the better approach. */
			/*if (bCrushStrategy && GET_TEAM(getTeam()).AI_getWarPlan(kLoopPlayer.getTeam()) != NO_WARPLAN)
				iCivFactor = 400;
			else*/
			if (GET_TEAM(getTeam()).isAtWar(kRival.getTeam()))
				iCivFactor = 300;
			// Beef up border security before starting war, but not too much (bbai)
			else if (GET_TEAM(getTeam()).AI_getWarPlan(kRival.getTeam()) != NO_WARPLAN)
				iCivFactor = 180;
			else
			{	// <advc.022>
				AttitudeTypes eTowardThem = kOwner.AI_getAttitude(kRival.getID());
				AttitudeTypes eTowardUs = kRival.AI_getAttitude(kOwner.getID());
				if (!kRival.isHuman())
				{
					// Round toward eTowardUs
					int iTowardThem = eTowardThem;
					if(eTowardUs > iTowardThem)
						iTowardThem++;
					eTowardUs = (AttitudeTypes)((eTowardUs + iTowardThem) / 2);
				} // Replaced below:
				//switch (kOwner.AI_getAttitude((PlayerTypes)iI))
				/*	(K-Mod note: for good strategy,
					this should probably be _their_ attitude rather than ours.
					But perhaps for role-play it is better the way it is.) */
				switch(eTowardUs) // Yep, use their attitude. </advc.022>
				{
				case ATTITUDE_FURIOUS:
					iCivFactor = 180;
					break;
				case ATTITUDE_ANNOYED:
					iCivFactor = 130;
					break;
				case ATTITUDE_CAUTIOUS:
					iCivFactor = 100;
					break;
				case ATTITUDE_PLEASED:
					iCivFactor = 50;
					break;
				case ATTITUDE_FRIENDLY:
					iCivFactor = 20;
					break;
				default:
					FAssert(false);
				}

				// K-Mod
				// Reduce threat level of our vassals, particularly from capitulated vassals.
				if (GET_TEAM(kRival.getTeam()).isVassal(getTeam()))
				{
					iCivFactor = std::min(iCivFactor,
							GET_TEAM(kRival.getTeam()).isCapitulated() ? 30 : 50);
				}
				else
				{
					/*	Increase threat level for cities that we have captured from this player
						I may add a turn limit later if this produces unwanted behaviour.
						(getGameTurn() - getGameTurnAcquired() < 40) */
					if (getPreviousOwner() == kRival.getID())
						iCivFactor = (iCivFactor * 3) / 2;
					// Don't get too comfortable if kLoopPlayer is using a military victory strategy.
					if (kRival.AI_atVictoryStage(AI_VICTORY_MILITARY4))
						iCivFactor = std::max(100, iCivFactor);
				}
				// K-Mod end

				if (bCrushStrategy)
					iCivFactor /= 2;
			}

			// K-Mod. Amplify the threat rating for rivals which have high power.
			if (kRival.getPower() > kOwner.getPower())
			{
				/*iTempValue *= std::min(400, (100 * GET_PLAYER((PlayerTypes)iI).getPower())/std::max(1, GET_PLAYER(getOwner()).getPower()));
				iTempValue /= 100;*/ // BBAI

				/*	exclude population power. (Should this use the same power comparison
					used to calculate areaAI and war values?) */
				int iLoopPower = kRival.getPower() - GC.getGame().
						getPopulationPower(kRival.getTotalPopulation());
				int iOurPower = kOwner.getPower() - GC.getGame().
						getPopulationPower(kOwner.getTotalPopulation());
				iCivFactor *= range(100 * iLoopPower/std::max(1, iOurPower), 100, 400);
				iCivFactor /= 100;
			}

			/* iTempValue /= 100;
			iTotalThreat += iTempValue; */
			iTotalThreat += iAccessFactor * iCivFactor / 100; // K-Mod
		}
	}

	/*if (isCoastal(GC.getMIN_WATER_SIZE_FOR_OCEAN())) {
		int iCurrentEra = kOwner.getCurrentEra();
		iValue += std::max(0, ((10 * iCurrentEra) / 3) - 6); //there are better ways to do this
	} */ // BtS - this is now included in the iAccessFactor calculation

	/*iValue += getNumActiveWorldWonders() * 5;
	if (kOwner.AI_atVictoryStage(AI_VICTORY_CULTURE3)) {
		iValue += 5;
		iValue += getCommerceRateModifier(COMMERCE_CULTURE) / 20;
		if (getCultureLevel() >= GC.getNumCultureLevelInfos() - 2) {
			iValue += 20;
			if (getCultureLevel() >= GC.getNumCultureLevelInfos() - 1)
				iValue += 30;
		}
	}*/ // BtS

	iTotalThreat += 3 * kOwner.AI_getPlotDanger(*plot(), 3, false); // was 2 *

	/*	K-Mod. Increase the threat rating for high-value cities.
		(Note: this replaces the culture & wonder stuff above)
		(Note2: I may end up moving this stuff into AI_getCityImportance) */
	if (iTotalThreat > 0)
	{
		int iImportanceFactor = 100;
		iImportanceFactor += 20 * getNumActiveWorldWonders();
		iImportanceFactor += isHolyCity() ? 20 : 0;
		FOR_EACH_ENUM(Corporation)
		{
			if (isHeadquarters(eLoopCorporation))
			{
				/*	note: the corp HQ building counts
					as an active world wonder in addition to this value. */
				iImportanceFactor += 10;
			}
		}

		if (kOwner.AI_atVictoryStage(AI_VICTORY_CULTURE3))
		{
			if (getCultureLevel() >= GC.getGame().culturalVictoryCultureLevel() - 1)
			{
				iImportanceFactor += 20;
				if (findCommerceRateRank(COMMERCE_CULTURE) <= GC.getGame().culturalVictoryNumCultureCities())
				{
					iImportanceFactor += 30;
					if (kOwner.AI_atVictoryStage(AI_VICTORY_CULTURE4))
					{
						iImportanceFactor += 100;
					}
				}
			}
		}
		if (isCapital())
		{
			iImportanceFactor = std::max(iImportanceFactor, 150);
			if (GET_TEAM(kOwner.getTeam()).AI_getLowestVictoryCountdown() > 0)
				iImportanceFactor += 100;
		}
		iTotalThreat = iTotalThreat * iImportanceFactor / 100;
	} // K-Mod end

	return iTotalThreat;
}

/*  advc.031b: Between 1 and 100 (not 0 b/c the caller should ensure that there
	is at least one acceptable and reachable city site). Note that the result
	is currently usually doubled and then used as the per-cent probability of
	training a Settler, meaning that values greater than 50 get clamped. */
int CvCityAI::AI_calculateSettlerPriority(int iAreaSites, int iBestAreaFoundValue,
	int iWaterAreaSites, int iBestWaterAreaFoundValue) const
{
	FAssert(iAreaSites + iWaterAreaSites > 0);
	if(iAreaSites <= 0)
		return 60; // Don't really want to pace AI colonization
	int iPriority = 20;
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());
	int iMinFoundValue = std::max(1, kOwner.AI_getMinFoundValue());
	iPriority += (10 * std::max(iBestAreaFoundValue, iBestWaterAreaFoundValue)) / iMinFoundValue;
	CvTeam const& kTeam = GET_TEAM(getTeam());
	if(kTeam.isAlwaysWar())
		iPriority -= 10;
	else if(!GET_TEAM(getTeam()).AI_isWarPossible() || // Can't expand through war
		(kTeam.isAVassal() && !kTeam.isCapitulated()) ||
		(getUWAI().isEnabled() && kOwner.uwai().getCache().hasDefensiveTrait()))
	{
		iPriority += 15;
	}
	// Imperialistic trait? Awkward to check ...
	// I don't think the number of sites should matter(?)
	return std::min(100, iPriority);
}

// advc.118b (see comments about the corresponding CvPlayerAI function)
int CvCityAI::AI_defianceAngerCost(ReligionTypes eVSReligion) const
{
	if (eVSReligion != NO_RELIGION && !isHasReligion(eVSReligion))
		return 0;
	/*	(For a more sophisticated calculation, CvPlayerAI::AI_getHappinessWeight
		should be split up between CvPlayerAI and CvCityAI.) */
	if (isNoUnhappiness())
		return 0;
	int const iHappy = happyLevel();
	int const iUnhappy = unhappyLevel();
	int const iUnhappyIncr = std::max(0,
			GC.getDefineINT(CvGlobals::DEFY_RESOLUTION_POP_ANGER) +
			iUnhappy - iHappy) - std::max(0, iUnhappy - iHappy);
	return iUnhappyIncr * AI_citizenValue() *
			// Discourage repeated denial
			(getDefyResolutionAngerTimer() > 0 ? 2 : 1);
}

//Workers have/needed is not intended to be a strict
//target but rather an indication.
//if needed is at least 1 that means a worker
//will be doing something useful
int CvCityAI::AI_getWorkersHave() /* advc: */ const
{
	return m_iWorkersHave;
}


int CvCityAI::AI_getWorkersNeeded() /* advc: */ const
{
	return m_iWorkersNeeded;
}


void CvCityAI::AI_changeWorkersHave(int iChange)
{
	m_iWorkersHave += iChange;
	//FAssert(m_iWorkersHave >= 0);
	m_iWorkersHave = std::max(0, m_iWorkersHave);
}


void CvCityAI::AI_updateWorkersHaveAndNeeded()
{
	PROFILE_FUNC();

	int iWorkersNeeded = 0;
	int iWorkersHave = 0;
	int iUnimprovedWorkedPlotCount = 0;
	int iUnimprovedUnworkedPlotCount = 0;
	int iWorkedUnimprovableCount = 0;
	int iImprovedUnworkedPlotCount = 0;

	int iSpecialCount = 0;

	int iWorstWorkedPlotValue = MAX_INT;
	int iBestUnworkedPlotValue = 0;

	int iGrowthValue = AI_growthValuePerFood(); // K-Mod

	if (getProductionUnit() != NO_UNIT)
	{
		if (getProductionUnitAI() == UNITAI_WORKER)
		{
			if (getProductionTurnsLeft() <= 3) // advc.113: was <=2
				iWorkersHave++;
		}
	}
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());
	int aiYields[NUM_YIELD_TYPES] /* advc: */ = {};
	for (WorkablePlotIter it(*this); it.hasNext(); ++it)
	{
		CvPlot const& kPlot = *it;
		CityPlotTypes const ePlot = it.currID();

		//if (kPlot.getArea() == getArea()) // (disabled by K-Mod)

		/*  BtS comment: How slow is this? It could be almost NUM_CITY_PLOT times faster
			by iterating groups and seeing if the plot target lands in this city
			but since this is only called once/turn i'm not sure it matters. */
		/*  advc.113b: I also want to count workers in transports, so let's indeed
			go through the groups just once (at the end of this function). */
		//iWorkersHave += kOwner.AI_plotTargetMissionAIs(pLoopPlot, MISSIONAI_BUILD);
		iWorkersHave += kPlot.plotCount(PUF_isUnitAIType, UNITAI_WORKER, -1, getOwner(), getTeam(),
				//PUF_isNoMission, -1, -1);
				// advc.113b: Perhaps move this into the group loop too (tbd.)?
				PUF_isMissionPlotWorkingCity, getID(), getOwner());
		if (ePlot == CITY_HOME_PLOT)
			continue;

		if (!kPlot.isImproved())
		{
			if (kPlot.isBeingWorked())
			{
				if (AI_getBestBuild(ePlot) != NO_BUILD &&
					isArea(kPlot.getArea())) // K-Mod
				{
					iUnimprovedWorkedPlotCount++;
				}
				else iWorkedUnimprovableCount++;
			}
			else if (AI_getBestBuild(ePlot) != NO_BUILD &&
				isArea(kPlot.getArea())) // K-Mod
			{
				iUnimprovedUnworkedPlotCount++;
			}
		}
		else if (!kPlot.isBeingWorked())
			iImprovedUnworkedPlotCount++;

		for (int iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
			aiYields[iJ] = kPlot.getYield((YieldTypes)iJ);

		if (kPlot.isBeingWorked())
		{
			int iPlotValue = AI_yieldValue(aiYields, NULL, false, false, true, true, iGrowthValue);
			iWorstWorkedPlotValue = std::min(iWorstWorkedPlotValue, iPlotValue);
		}
		else
		{
			int iPlotValue = AI_yieldValue(aiYields, NULL, false, false, true, true, iGrowthValue);
			iBestUnworkedPlotValue = std::max(iBestUnworkedPlotValue, iPlotValue);
		}
	}
	//specialists?

	//iUnimprovedWorkedPlotCount += std::min(iUnimprovedUnworkedPlotCount, iWorkedUnimprovableCount) / 2;
	// K-Mod
	int iPopDelta = AI_getTargetPopulation() - getPopulation();
	int iFutureWork = std::max(0, iWorkedUnimprovableCount + range((iPopDelta+1)/2, 0, 3) - iImprovedUnworkedPlotCount);
	//iUnimprovedWorkedPlotCount += (std::min(iUnimprovedUnworkedPlotCount, iFutureWork)+1) / 2
	// K-Mod end
	// <advc.113> Replacing the line above
	iUnimprovedWorkedPlotCount +=
			(scaled(std::min(iUnimprovedUnworkedPlotCount, iFutureWork) + 1, 2) *
			per100((GC.getDefineINT(CvGlobals::WORKER_RESERVE_PERCENT) + 100 +
			// Flavor was previously counted in CvPlayerAI::AI_neededWorkers
			2 * kOwner.AI_getFlavorValue(FLAVOR_GROWTH)))).round();
	// </advc.113>
	iWorkersNeeded += 2 * iUnimprovedWorkedPlotCount;

	int iBestPotentialPlotValue = -1;
	int iChop = 0; // advc.117
	if (iWorstWorkedPlotValue != MAX_INT)
	{
		//Add an additional citizen to account for future growth.
		CityPlotTypes eBestPlot = NO_CITYPLOT;
		SpecialistTypes eBestSpecialist = NO_SPECIALIST;

		if (angryPopulation() == 0)
			AI_addBestCitizen(true, true, &eBestPlot, &eBestSpecialist);

		for (WorkablePlotIter it(*this, false); it.hasNext(); ++it)
		{
			CvPlot const& kPlot = *it;
			CityPlotTypes const ePlot = it.currID();
			if (!isArea(kPlot.getArea()) || AI_getBestBuild(ePlot) == NO_BUILD)
			{
				continue;
			}
			FOR_EACH_ENUM(Yield)
			{
				aiYields[eLoopYield] = kPlot.getYieldWithBuild(
						m_aeBestBuild[ePlot], eLoopYield, true);
			}
			int iPlotValue = AI_yieldValue(aiYields, NULL, false, false, true, true, iGrowthValue);
			ImprovementTypes const eImprovement = GC.getInfo(AI_getBestBuild(ePlot)).getImprovement();
			if (eImprovement != NO_IMPROVEMENT)
			{
				if (getImprovementFreeSpecialists(eImprovement) > 0 ||
					GC.getInfo(eImprovement).getHappiness() > 0||
					// advc.901:
					GC.getInfo(eImprovement).get(CvImprovementInfo::HealthPercent) >= 50)
				{
					iSpecialCount++;
				} // <advc.117>
				FeatureTypes eFeature = kPlot.getFeatureType();
				if(eFeature != NO_FEATURE && GC.getInfo(AI_getBestBuild(ePlot)).
					//getFeatureProduction(eFeature) > 0 // Let's count jungle too
					isFeatureRemove(eFeature))
				{
					iChop++;
				} // </advc.117>
			}
			iBestPotentialPlotValue = std::max(iBestPotentialPlotValue, iPlotValue);
		}

		if (eBestPlot != NO_CITYPLOT)
			setWorkingPlot(eBestPlot, false);
		if (eBestSpecialist != NO_SPECIALIST)
			changeSpecialistCount(eBestSpecialist, -1);
		if (iBestPotentialPlotValue > iWorstWorkedPlotValue)
			iWorkersNeeded += 2;
	}

	scaled const rOwnerAIEraFactor = kOwner.AI_getCurrEraFactor(); // advc.erai
	iWorkersNeeded += ((std::max(0, iUnimprovedWorkedPlotCount - 1) *
			rOwnerAIEraFactor) / 3).round();
	// advc.113: Disabled. Not clear to me that additional workers help with finances.
	/*if (kOwner.AI_isFinancialTrouble()) {
		iWorkersNeeded *= 3;
		iWorkersNeeded /= 2;
	}*/

	// advc.117: Chopping isn't considered when counting (un)improved (un)worked tiles
	iWorkersNeeded += (6 * iChop) / 10;

	// advc.113: Moved the iSpecialistExtra code up so that the division by 3 happens afterwards
	int iSpecialistExtra = std::min((getSpecialistPopulation() - totalFreeSpecialists()), iUnimprovedUnworkedPlotCount);
	iSpecialistExtra -= iImprovedUnworkedPlotCount;
	//iWorkersNeeded += std::max(0, 1 + iSpecialistExtra) / 2;
	// advc.113b: Instead divide by 3 below
	iWorkersNeeded += std::max(0, iSpecialistExtra);

	if (iWorkersNeeded > 0)
		iWorkersNeeded = std::max(1, (iWorkersNeeded + 1) / 3);

	if (iWorstWorkedPlotValue <= iBestUnworkedPlotValue &&
			iBestUnworkedPlotValue >= iBestPotentialPlotValue)
		iWorkersNeeded /= 2;

	if (angryPopulation(1) > 0)
		iWorkersNeeded = (iWorkersNeeded + 1) / 2;

	iWorkersNeeded += (iSpecialCount + 1) / 2;

	iWorkersNeeded = std::max((iUnimprovedWorkedPlotCount + 1) / 2, iWorkersNeeded);
	// <advc.113> Greater than 3 is dubious. Allow 4 only in the late game.
	if (iWorkersNeeded >= 4)
		iWorkersNeeded--;
	iWorkersNeeded = std::min(iWorkersNeeded, 2 + ((2 + rOwnerAIEraFactor) / 3).round());
	// </advc.113>
	/*  <advc.113b> Replacing the more expensive AI_plotTargetMissionAIs call
		in the city plot loop above. */
	FOR_EACH_GROUPAI(pGroup, kOwner)
	{
		int const iSize = pGroup->getNumUnits();
		if (iSize <= 0)
			continue;
		// Already counted in the city plot loop
		if (pGroup->getPlot().getWorkingCity() == this)
			continue;
		CvPlot* pMissionPlot = pGroup->AI_getMissionAIPlot();
		int const iRange = (9 * (1 + rOwnerAIEraFactor / 2)).round();
		if (pMissionPlot == NULL || ::plotDistance(pMissionPlot, pGroup->plot()) > iRange)
			continue;
		MissionAITypes eGroupMissionAI = pGroup->AI_getMissionAIType();
		if (eGroupMissionAI == MISSIONAI_BUILD)
		{
			if (pMissionPlot->getWorkingCity() == this)
				iWorkersHave += iSize;
		}
		// CvUnitAI::AI_ferryWorkers uses MISSIONAI_FOUND
		else if (eGroupMissionAI == MISSIONAI_FOUND && pGroup->getDomainType() == DOMAIN_SEA)
		{
			if (pMissionPlot == plot())
				iWorkersHave += pGroup->getHeadUnit()->getUnitAICargo(UNITAI_WORKER);
		}
	}

	m_iWorkersNeeded = iWorkersNeeded;
	m_iWorkersHave = iWorkersHave;
}

// advc.179:
scaled CvCityAI::AI_estimateReligionBuildings(PlayerTypes ePlayer, ReligionTypes eReligion,
	std::vector<BuildingTypes> const& aeBuildings) const
{
	/*  Player whose buildings we're counting
		(we = the owner of this CvCity) */
	CvPlayer const& kPlayer = GET_PLAYER(ePlayer);
	int iPotential = 0;
	int iCertain = 0;
	FOR_EACH_CITY(c, kPlayer)
	{
		if(!c->isRevealed(getTeam()))
		{
			iPotential++;
			continue;
		}
		if(!c->isHasReligion(eReligion))
		{
			// As AP owner, we may well spread eReligion to all our cities.
			if(ePlayer == getOwner() || c->getReligionCount() <= 0)
				iPotential++;
			continue;
		}
		if(c->getTeam() != getTeam() && !c->getPlot().isInvestigate(getTeam()))
		{
			iPotential += 3;
			continue;
		}
		for(size_t i = 0; i < aeBuildings.size(); i++)
		{
			if(GET_TEAM(c->getTeam()).isObsoleteBuilding(aeBuildings[i]))
				continue;
			iCertain += c->getNumBuilding(aeBuildings[i]);
			int iCost = GC.getInfo(aeBuildings[i]).getProductionCost();
			// Anticipate only regular buildings
			if(iCost > 0 && iCost < 100 && c->canConstruct(aeBuildings[i]))
				iPotential += 2;
		}
	}
	scaled r(iCertain + iPotential, 4);
	bool bObsolete = false;
	for(size_t i = 0; i < aeBuildings.size(); i++)
	{
		TechTypes eObsTech = GC.getInfo(aeBuildings[i]).getObsoleteTech();
		if(eObsTech != NO_TECH &&
			GC.getInfo(eObsTech).getEra() <= kPlayer.getCurrentEra())
		{
			bObsolete = true;
			break;
		}
	}
	if(bObsolete)
		r /= 2;
	return r;
}


BuildingTypes CvCityAI::AI_bestAdvancedStartBuilding(int iPass) const
{
	int iFocusFlags = 0;
	if (iPass >= 0)
		iFocusFlags |= BUILDINGFOCUS_FOOD;
	if (iPass >= 1)
		iFocusFlags |= BUILDINGFOCUS_PRODUCTION;
	if (iPass >= 2)
		iFocusFlags |= BUILDINGFOCUS_EXPERIENCE;
	if (iPass >= 3)
		iFocusFlags |= (BUILDINGFOCUS_HAPPY | BUILDINGFOCUS_HEALTHY);
	if (iPass >= 4)
	{
		iFocusFlags |= (BUILDINGFOCUS_GOLD | BUILDINGFOCUS_RESEARCH | BUILDINGFOCUS_MAINTENANCE);
		if (!GC.getGame().isOption(GAMEOPTION_NO_ESPIONAGE))
			iFocusFlags |= BUILDINGFOCUS_ESPIONAGE;
	}
	return AI_bestBuildingThreshold(iFocusFlags, 0, std::max(0, 20 - iPass * 5));
}

// K-Mod:
void CvCityAI::AI_ClearConstructionValueCache()
{
	m_aiConstructionValue.assign(GC.getNumBuildingClassInfos(), -1);
}


// doc: return first non-state religion to make it work for now
// TODO: refactor
ReligionTypes CvCityAI::AI_getPersecutionReligion(ReligionTypes eIgnoredReligion)
{
	for (int iI = 0; iI < GC.getNumReligionInfos(); iI++)
	{
		if (eIgnoredReligion == iI)
		{
			continue;
		}

		if (GET_PLAYER(getOwner()).getStateReligion() != iI)
		{
			if (GET_PLAYER(getOwner()).AI_getPersecutionValue((ReligionTypes)iI) < 0)
			{
				break;
			}

			if (isHasReligion((ReligionTypes)iI) && !isHolyCity((ReligionTypes)iI))
			{
				return (ReligionTypes)iI;
			}
		}
	}

	return NO_RELIGION;
}

// Leoreth: building AI weights, civ specific preferences and special conditions for some wonders
// TODO: refactor
// TODO: used?
int CvCityAI::AI_buildingWeight(BuildingTypes eBuilding) const
{
	CvBuildingInfo& kBuilding = GC.getBuildingInfo(eBuilding);
	CvPlayer& kPlayer = GET_PLAYER(getOwnerINLINE());

	int iWeight = kBuilding.getAIWeight();
	int iPreference = kPlayer.getBuildingClassPreference((BuildingClassTypes)kBuilding.getBuildingClassType());

	if (eBuilding == HANGING_GARDENS)
	{
		int iFloodPlainsCount = 0;
		for (int iI = 0; iI < NUM_CITY_PLOTS; iI++)
		{
			if (getCityIndexPlot(iI)->getFeatureType() == FEATURE_FLOOD_PLAINS)
			{
				iFloodPlainsCount += 1;
			}
		}

		if (iFloodPlainsCount < 2)
		{
			return -MAX_INT;
		}
	}
	else if (eBuilding == AQUA_APPIA)
	{
		if (getCultureLevel() < 2)
		{
			return -MAX_INT;
		}
	}
	else if (eBuilding == PANTHEON)
	{
		if (GET_PLAYER(getOwnerINLINE()).countNumBuildings(getUniqueBuilding(getCivilizationType(), PAGAN_TEMPLE)) < 3)
		{
			return -MAX_INT;
		}
	}
	else if (eBuilding == MACHU_PICCHU || eBuilding == MOLE_ANTONELLIANA)
	{
		int iPeakCount = 0;
		for (int iI = 0; iI < NUM_CITY_PLOTS; iI++)
		{
			if (getCityIndexPlot(iI)->isPeak())
			{
				iPeakCount += 1;
			}
		}

		if (iPeakCount < 5)
		{
			return -MAX_INT;
		}
	}
	else if (eBuilding == GREAT_ADOBE_MOSQUE)
	{
		int iDesertCount = 0;
		for (int iI = 0; iI < NUM_CITY_PLOTS; iI++)
		{
			if (getCityIndexPlot(iI)->getTerrainType() == TERRAIN_DESERT || getCityIndexPlot(iI)->getTerrainType() == TERRAIN_SEMIDESERT)
			{
				iDesertCount += 1;
			}
		}

		if (iDesertCount < 5)
		{
			return -MAX_INT;
		}
	}
	else if (eBuilding == POTALA_PALACE)
	{
		int iHillCount = 0;
		for (int iI = 0; iI < NUM_CITY_PLOTS; iI++)
		{
			if (getCityIndexPlot(iI)->isHills())
			{
				iHillCount += 1;
			}
		}

		if (iHillCount < 8)
		{
			return -MAX_INT;
		}
	}
	else if (eBuilding == ITSUKUSHIMA_SHRINE)
	{
		int iWaterCount = 0;
		for (int iI = 0; iI < NUM_CITY_PLOTS; iI++)
		{
			if (getCityIndexPlot(iI)->isWater())
			{
				iWaterCount += 1;
			}
		}

		if (iWaterCount < 8)
		{
			return -MAX_INT;
		}
	}
	else if (eBuilding == IMAGE_OF_THE_WORLD_SQUARE || eBuilding == HERMITAGE || eBuilding == CHAPULTEPEC_CASTLE)
	{
		if (getCultureLevel() < 3)
		{
			return -MAX_INT;
		}
	}
	else if (eBuilding == SHALIMAR_GARDENS)
	{
		if (goodHealth() - badHealth() < 4)
		{
			return -MAX_INT;
		}
	}
	else if (eBuilding == WESTMINSTER_PALACE)
	{
		if (GET_PLAYER(getOwnerINLINE()).countColonies() <= 5)
		{
			return -MAX_INT;
		}
	}
	else if (eBuilding == CHANNEL_TUNNEL)
	{
		int iFriendlyRelationCount = 0;
		for (int iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if (getOwnerINLINE() != iI && GET_PLAYER((PlayerTypes)iI).isAlive() && GET_PLAYER((PlayerTypes)iI).AI_getAttitude(getOwnerINLINE()) == ATTITUDE_FRIENDLY)
			{
				iFriendlyRelationCount += 1;
			}
		}

		if (iFriendlyRelationCount < 1)
		{
			return -MAX_INT;
		}
	}
	else if (eBuilding == HARBOUR_OPERA)
	{
		if (!GET_PLAYER(getOwnerINLINE()).AI_isDoStrategy(AI_STRATEGY_CULTURE2) && !GET_PLAYER(getOwnerINLINE()).AI_isDoStrategy(AI_STRATEGY_CULTURE3) && !GET_PLAYER(getOwnerINLINE()).AI_isDoStrategy(AI_STRATEGY_CULTURE4))
		{
			return -MAX_INT;
		}
	}

	if (iPreference > -MAX_INT)
	{
		if (iPreference <= 0)
		{
			iWeight = 0;
		}
		else
		{
			iWeight *= (100 + iPreference);
			iWeight /= 100;
		}
	}

	return iWeight;
}

void CvCityAI::read(FDataStreamBase* pStream)
{
	CvCity::read(pStream);

	uint uiFlag=0;
	pStream->Read(&uiFlag);

	pStream->Read(&m_iEmphasizeAvoidGrowthCount);
	pStream->Read(&m_iEmphasizeGreatPeopleCount);
	pStream->Read(&m_bAssignWorkDirty);
	//pStream->Read(&m_bChooseProductionDirty);
	// <advc.003u>
	if (uiFlag < 5)
	{
		bool bTmp;
		pStream->Read(&bTmp);
	} // </advc.003u>

	pStream->Read((int*)&m_routeToCity.eOwner);
	pStream->Read(&m_routeToCity.iID);
	m_routeToCity.validateOwner(); // advc.opt

	pStream->Read(NUM_YIELD_TYPES, m_aiEmphasizeYieldCount);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiEmphasizeCommerceCount);
	pStream->Read(&m_bForceEmphasizeCulture);
	// <advc.131d>
	if (uiFlag >= 9)
		pStream->Read(&m_bStrongEmphasis); // </advc.131d>
	pStream->Read(NUM_CITY_PLOTS, m_aiBestBuildValue);
	pStream->Read(NUM_CITY_PLOTS, (int*)m_aeBestBuild);
	// <advc.opt>
	if(uiFlag >= 4)
		pStream->Read((int*)&m_eBestBuild); // </advc.opt>
	pStream->Read(GC.getNumEmphasizeInfos(), m_pbEmphasize);
	pStream->Read(NUM_YIELD_TYPES, m_aiSpecialYieldMultiplier);
	// <advc.opt>
	if (uiFlag < 6)
	{
		int iTmp; // Discard old closeness cache meta data
		pStream->Read(&iTmp);
		pStream->Read(&iTmp);
	}
	else
	{
		pStream->Read(MAX_PLAYERS, m_aiCachePlayerClosenessTurn);
		pStream->Read(MAX_PLAYERS, m_aiCachePlayerClosenessDistance);
	} // </advc.opt>
	pStream->Read(MAX_PLAYERS, m_aiPlayerCloseness);
	pStream->Read(&m_iNeededFloatingDefenders);
	pStream->Read(&m_iNeededFloatingDefendersCacheTurn);
	// <advc.139>
	if (uiFlag >= 8)
		pStream->Read((int*)&m_eSafety);
	else
	{
		bool bEvac = false;
		bool bSafe = true;
		if (uiFlag >= 3)
			pStream->Read(&bEvac);
		if (uiFlag >= 7)
			pStream->Read(&bSafe);
		if (bEvac)
			m_eSafety = CITYSAFETY_EVACUATING;
		else if (!bSafe)
			m_eSafety = CITYSAFETY_THREATENED;
	}
	if (uiFlag >= 7)
		pStream->Read(&m_iCityValPercent);
	// </advc.139>
	pStream->Read(&m_iWorkersNeeded);
	pStream->Read(&m_iWorkersHave);
	// K-Mod
	if (uiFlag >= 1)
	{
		FAssert(m_aiConstructionValue.size() == GC.getNumBuildingClassInfos());
		pStream->Read(GC.getNumBuildingClassInfos(), &m_aiConstructionValue[0]);
	}
	if (uiFlag >= 2)
		pStream->Read(&m_iCultureWeight);
	// K-Mod end
}


void CvCityAI::write(FDataStreamBase* pStream)
{
	CvCity::write(pStream);
	uint uiFlag;
	//uiFlag = 1; // K-Mod: m_aiConstructionValue
	//uiFlag = 2; // K-Mod: m_iCultureWeight
	//uiFlag = 3; // advc.139: m_bEvacuate
	//uiFlag = 4; // advc.opt: m_eBestBuild
	//uiFlag = 5; // advc.003u: Move m_bChooseProductionDirty to CvCity
	//uiFlag = 6; // advc.opt: Per-player meta data for closeness cache
	//uiFlag = 7; // advc.139: m_bSafe, m_iCityValPercent
	//uiFlag = 9; // advc.139: m_eSafety
	uiFlag = 9; // advc.131d
	pStream->Write(uiFlag);
	REPRO_TEST_BEGIN_WRITE(CvString::format("CityAI(%d,%d)", getX(), getY()));
	pStream->Write(m_iEmphasizeAvoidGrowthCount);
	pStream->Write(m_iEmphasizeGreatPeopleCount);
	pStream->Write(m_bAssignWorkDirty);
	//pStream->Write(m_bChooseProductionDirty); // advc.003u

	pStream->Write(m_routeToCity.eOwner);
	pStream->Write(m_routeToCity.iID);

	pStream->Write(NUM_YIELD_TYPES, m_aiEmphasizeYieldCount);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiEmphasizeCommerceCount);
	pStream->Write(m_bForceEmphasizeCulture);
	pStream->Write(m_bStrongEmphasis); // advc.131d
	pStream->Write(NUM_CITY_PLOTS, m_aiBestBuildValue);
	pStream->Write(NUM_CITY_PLOTS, (int*)m_aeBestBuild);
	pStream->Write(m_eBestBuild); // advc.opt
	pStream->Write(GC.getNumEmphasizeInfos(), m_pbEmphasize);
	pStream->Write(NUM_YIELD_TYPES, m_aiSpecialYieldMultiplier);
	REPRO_TEST_END_WRITE();
	// The closeness cache is prone to OOS/ reproducibility problems
	REPRO_TEST_BEGIN_WRITE(CvString::format("CityAI(%d,%d) caches", getX(), getY()));
	pStream->Write(/*<advc.opt>*/MAX_PLAYERS/*</advc.opt>*/, m_aiCachePlayerClosenessTurn);
	pStream->Write(/*<advc.opt>*/MAX_PLAYERS/*</advc.opt>*/, m_aiCachePlayerClosenessDistance);
	pStream->Write(MAX_PLAYERS, m_aiPlayerCloseness);
	pStream->Write(m_iNeededFloatingDefenders);
	pStream->Write(m_iNeededFloatingDefendersCacheTurn);
	// <advc.139>
	pStream->Write(m_eSafety);
	pStream->Write(m_iCityValPercent);
	// </advc.139>
	//This needs to be serialized for human workers.
	pStream->Write(m_iWorkersNeeded);
	pStream->Write(m_iWorkersHave);
	// K-Mod (note: cache needs to be saved, otherwise players who join mid-turn might go out of sync when the cache is used)
	pStream->Write(GC.getNumBuildingClassInfos(), &m_aiConstructionValue[0]);
	pStream->Write(m_iCultureWeight);
	// K-Mod end
	REPRO_TEST_END_WRITE();
}

// advc:
CvCityAI* CvCityAI::fromIDInfo(IDInfo id)
{
	return ::AI_getCity(id);
}
