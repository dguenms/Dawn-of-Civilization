// city.cpp

#include "CvGameCoreDLL.h"
#include "CvGlobals.h"
#include "CvCity.h"
#include "CvArea.h"
#include "CvGameAI.h"
#include "CvMap.h"
#include "CvPlot.h"
#include "CvTeamAI.h"
#include "CvGameCoreUtils.h"
#include "CvPlayerAI.h"
#include "CvUnit.h"
#include "CvInfos.h"
#include "CvRandom.h"
#include "CvArtFileMgr.h"
#include "CvPopupInfo.h"
#include "CyCity.h"
#include "CyArgsList.h"
#include "FProfiler.h"
#include "CvGameTextMgr.h"

// interfaces used
#include "CvDLLEngineIFaceBase.h"
#include "CvDLLPythonIFaceBase.h"
#include "CvDLLEntityIFaceBase.h"
#include "CvDLLInterfaceIFaceBase.h"
#include "CvEventReporter.h"

#include "CvRhyes.h" //Rhye
#include <algorithm>

// Public Functions...

CvCity::CvCity()
{
	m_aiSeaPlotYield = new int[NUM_YIELD_TYPES];
	m_aiRiverPlotYield = new int[NUM_YIELD_TYPES];
	m_aiBaseYieldRate = new int[NUM_YIELD_TYPES];
	m_aiYieldRateModifier = new int[NUM_YIELD_TYPES];
	m_aiPowerYieldRateModifier = new int[NUM_YIELD_TYPES];
	m_aiBonusYieldRateModifier = new int[NUM_YIELD_TYPES];
	m_aiTradeYield = new int[NUM_YIELD_TYPES];
	m_aiCorporationYield = new int[NUM_YIELD_TYPES];
	m_aiExtraSpecialistYield = new int[NUM_YIELD_TYPES];
	m_aiCommerceRate = new int[NUM_COMMERCE_TYPES];
	m_aiProductionToCommerceModifier = new int[NUM_COMMERCE_TYPES];
	m_aiBuildingCommerce = new int[NUM_COMMERCE_TYPES];
	m_aiSpecialistCommerce = new int[NUM_COMMERCE_TYPES];
	m_aiReligionCommerce = new int[NUM_COMMERCE_TYPES];
	m_aiCorporationCommerce = new int[NUM_COMMERCE_TYPES];
	m_aiCommerceRateModifier = new int[NUM_COMMERCE_TYPES];
	m_aiBonusCommerceRateModifier = new int[NUM_COMMERCE_TYPES]; // Leoreth
	m_aiCommerceHappinessPer = new int[NUM_COMMERCE_TYPES];
	m_aiDomainFreeExperience = new int[NUM_DOMAIN_TYPES];
	m_aiDomainProductionModifier = new int[NUM_DOMAIN_TYPES];

	m_aiCulture = new int[MAX_PLAYERS];
	m_aiNumRevolts = new int[MAX_PLAYERS];
	m_aiGameTurnPlayerLost = new int[MAX_PLAYERS]; // Leoreth

	m_abEverOwned = new bool[MAX_PLAYERS];
	m_abTradeRoute = new bool[MAX_PLAYERS];
	m_abRevealed = new bool[MAX_TEAMS];
	m_abEspionageVisibility = new bool[MAX_TEAMS];

	m_aiCulturePlots = new int[NUM_CITY_PLOTS_3]; // Leoreth
	m_aiCultureCosts = new int[NUM_CITY_PLOTS_3]; // Leoreth

	m_paiNoBonus = NULL;
	m_paiFreeBonus = NULL;
	m_paiNumBonuses = NULL;
	m_paiNumCorpProducedBonuses = NULL;
	m_paiProjectProduction = NULL;
	m_paiBuildingProduction = NULL;
	m_paiBuildingProductionTime = NULL;
	m_paiBuildingOriginalOwner = NULL;
	m_paiBuildingOriginalTime = NULL;
	m_paiUnitProduction = NULL;
	m_paiUnitProductionTime = NULL;
	m_paiGreatPeopleUnitRate = NULL;
	m_paiGreatPeopleUnitProgress = NULL;
	m_paiSpecialistCount = NULL;
	m_paiMaxSpecialistCount = NULL;
	m_paiForceSpecialistCount = NULL;
	m_paiFreeSpecialistCount = NULL;
	m_paiImprovementFreeSpecialists = NULL;
	m_paiReligionInfluence = NULL;
	m_paiStateReligionHappiness = NULL;
	m_paiUnitCombatFreeExperience = NULL;
	m_paiFreePromotionCount = NULL;
	m_paiNumRealBuilding = NULL;
	m_paiNumFreeBuilding = NULL;

	m_pabWorkingPlot = NULL;
	m_pabHasReligion = NULL;
	m_pabHasCorporation = NULL;
	m_pabIsUnitHurried = NULL;

	// Leoreth
	m_ppaiBonusYield = NULL;

	m_paTradeCities = NULL;

	CvDLLEntity::createCityEntity(this);		// create and attach entity to city

	m_aiBaseYieldRank = new int[NUM_YIELD_TYPES];
	m_abBaseYieldRankValid = new bool[NUM_YIELD_TYPES];
	m_aiYieldRank = new int[NUM_YIELD_TYPES];
	m_abYieldRankValid = new bool[NUM_YIELD_TYPES];
	m_aiCommerceRank = new int[NUM_COMMERCE_TYPES];
	m_abCommerceRankValid = new bool[NUM_COMMERCE_TYPES];

	reset(0, NO_PLAYER, 0, 0, true);
}

CvCity::~CvCity()
{
	CvDLLEntity::removeEntity();			// remove entity from engine
	CvDLLEntity::destroyEntity();			// delete CvCityEntity and detach from us

	uninit();

	SAFE_DELETE_ARRAY(m_aiBaseYieldRank);
	SAFE_DELETE_ARRAY(m_abBaseYieldRankValid);
	SAFE_DELETE_ARRAY(m_aiYieldRank);
	SAFE_DELETE_ARRAY(m_abYieldRankValid);
	SAFE_DELETE_ARRAY(m_aiCommerceRank);
	SAFE_DELETE_ARRAY(m_abCommerceRankValid);

	SAFE_DELETE_ARRAY(m_aiSeaPlotYield);
	SAFE_DELETE_ARRAY(m_aiRiverPlotYield);
	SAFE_DELETE_ARRAY(m_aiBaseYieldRate);
	SAFE_DELETE_ARRAY(m_aiYieldRateModifier);
	SAFE_DELETE_ARRAY(m_aiPowerYieldRateModifier);
	SAFE_DELETE_ARRAY(m_aiBonusYieldRateModifier);
	SAFE_DELETE_ARRAY(m_aiTradeYield);
	SAFE_DELETE_ARRAY(m_aiCorporationYield);
	SAFE_DELETE_ARRAY(m_aiExtraSpecialistYield);
	SAFE_DELETE_ARRAY(m_aiCommerceRate);
	SAFE_DELETE_ARRAY(m_aiProductionToCommerceModifier);
	SAFE_DELETE_ARRAY(m_aiBuildingCommerce);
	SAFE_DELETE_ARRAY(m_aiSpecialistCommerce);
	SAFE_DELETE_ARRAY(m_aiReligionCommerce);
	SAFE_DELETE_ARRAY(m_aiCorporationCommerce);
	SAFE_DELETE_ARRAY(m_aiCommerceRateModifier);
	SAFE_DELETE_ARRAY(m_aiBonusCommerceRateModifier); //Leoreth
	SAFE_DELETE_ARRAY(m_aiCommerceHappinessPer);
	SAFE_DELETE_ARRAY(m_aiDomainFreeExperience);
	SAFE_DELETE_ARRAY(m_aiDomainProductionModifier);
	SAFE_DELETE_ARRAY(m_aiCulture);
	SAFE_DELETE_ARRAY(m_aiNumRevolts);
	SAFE_DELETE_ARRAY(m_aiGameTurnPlayerLost); // Leoreth
	SAFE_DELETE_ARRAY(m_aiCulturePlots); // Leoreth
	SAFE_DELETE_ARRAY(m_aiCultureCosts); // Leoreth
	SAFE_DELETE_ARRAY(m_abEverOwned);
	SAFE_DELETE_ARRAY(m_abTradeRoute);
	SAFE_DELETE_ARRAY(m_abRevealed);
	SAFE_DELETE_ARRAY(m_abEspionageVisibility);
}


void CvCity::init(int iID, PlayerTypes eOwner, int iX, int iY, bool bBumpUnits, bool bUpdatePlotGroups)
{
	CvPlot* pAdjacentPlot;
	CvPlot* pPlot;
	BuildingTypes eLoopBuilding;
	int iI;

	pPlot = GC.getMapINLINE().plotINLINE(iX, iY);

	// Leoreth: can cities be founded on top of others?
	/*if (pPlot->isCity())
	{
		GC.getGame().logMsg("\nFOUNDED CITY ON TOP OF ANOTHER CITY!\n");
	}*/

	//--------------------------------
	// Log this event
	if (GC.getLogging())
	{
		if (gDLL->getChtLvl() > 0)
		{
			TCHAR szOut[1024];
			sprintf(szOut, "Player %d City %d built at %d:%d\n", eOwner, iID, iX, iY);
			gDLL->messageControlLog(szOut);
		}
	}

	//--------------------------------
	// Init saved data
	reset(iID, eOwner, pPlot->getX_INLINE(), pPlot->getY_INLINE());

	// Leoreth: update art style before graphics are set up
	updateArtStyleType();

	//--------------------------------
	// Init non-saved data
	setupGraphical();

	//--------------------------------
	// Init other game data
	setName(GET_PLAYER(getOwnerINLINE()).getNewCityName());

	setEverOwned(getOwnerINLINE(), true);

	updateCultureLevel(false);
	updateCoveredPlots(false);

	if (pPlot->getCulture(getOwnerINLINE()) < GC.getDefineINT("FREE_CITY_CULTURE"))
	{
		pPlot->setCulture(getOwnerINLINE(), GC.getDefineINT("FREE_CITY_CULTURE"), bBumpUnits, false);
	}
	pPlot->setOwner(getOwnerINLINE(), bBumpUnits, false);
	pPlot->setPlotCity(this);

	for (iI = 0; iI < NUM_DIRECTION_TYPES; iI++)
	{
		pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

		if (pAdjacentPlot != NULL)
		{
			if (pAdjacentPlot->getCulture(getOwnerINLINE()) < GC.getDefineINT("FREE_CITY_ADJACENT_CULTURE"))
			{
				pAdjacentPlot->setCulture(getOwnerINLINE(), GC.getDefineINT("FREE_CITY_ADJACENT_CULTURE"), bBumpUnits, false);
			}
			pAdjacentPlot->updateCulture(bBumpUnits, false);
		}
	}

	for (iI = 0; iI < MAX_TEAMS; iI++)
	{
		if (GET_TEAM(getTeam()).isVassal((TeamTypes)iI))
		{
			pPlot->changeAdjacentSight((TeamTypes)iI, GC.getDefineINT("PLOT_VISIBILITY_RANGE"), true, NULL, false);
		}
	}

	CyArgsList argsList;
	argsList.add(iX);
	argsList.add(iY);
	long lResult=0;
	gDLL->getPythonIFace()->callFunction(PYGameModule, "citiesDestroyFeatures", argsList.makeFunctionArgs(), &lResult);

	if (lResult == 1)
	{
		if (pPlot->getFeatureType() != NO_FEATURE && pPlot->getFeatureType() != (FeatureTypes)GC.getInfoTypeForString("FEATURE_FLOOD_PLAINS")) //Leoreth: flood plains are not removed by cities
		{
			pPlot->setFeatureType(NO_FEATURE);
		}
	}

	pPlot->setImprovementType(NO_IMPROVEMENT);
	pPlot->updateCityRoute(false);

	for (iI = 0; iI < MAX_TEAMS; iI++)
	{
		if (GET_TEAM((TeamTypes)iI).isAlive())
		{
			if (pPlot->isVisible(((TeamTypes)iI), false))
			{
				setRevealed(((TeamTypes)iI), true);
			}
		}
	}

	changeMilitaryHappinessUnits(pPlot->plotCount(PUF_isMilitaryHappiness, (int)getOwnerINLINE())); // Leoreth: no military happiness for other players

	for (iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
	{
		changeCommerceHappinessPer(((CommerceTypes)iI), GC.getCommerceInfo((CommerceTypes)iI).getInitialHappiness());
	}

	for (iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		if (GET_PLAYER(getOwnerINLINE()).isBuildingFree((BuildingTypes)iI))
		{
			setNumFreeBuilding(((BuildingTypes)iI), 1);
		}
	}

	area()->changeCitiesPerPlayer(getOwnerINLINE(), 1);

	GET_TEAM(getTeam()).changeNumCities(1);

	GC.getGameINLINE().changeNumCities(1);

	setGameTurnFounded(GC.getGameINLINE().getGameTurn());
	setGameTurnAcquired(GC.getGameINLINE().getGameTurn()); //Rhye - infinite loop????

	

	// Leoreth: apply state religion building yield change
	for (iI = 0; iI < NUM_YIELD_TYPES; iI++)
	{
		changeReligionYieldChange(GET_PLAYER(eOwner).getStateReligion(), (YieldTypes)iI, GET_PLAYER(eOwner).getReligionYieldChange((YieldTypes)iI));
	}

	int iCurrentEra = GET_PLAYER(eOwner).getCurrentEra();
	int iExtraPopulation = iCurrentEra > 0 ? iCurrentEra : 0;

	if (GET_TEAM(GET_PLAYER(eOwner).getTeam()).isHasTech((TechTypes)ASTRONOMY))
	{
		if (isColony())
		{
			iExtraPopulation += 1;
		}
	}

    // Leoreth: Harappan UU (City Builder)
	if (getOwnerINLINE() == HARAPPA)
	{
		iExtraPopulation += 1;
	}

	changePopulation(GC.getDefineINT("INITIAL_CITY_POPULATION") + iExtraPopulation);
	//changePopulation(GC.getDefineINT("INITIAL_CITY_POPULATION") + iExtraPop);
	//Rhye - end switch

	changeAirUnitCapacity(GC.getDefineINT("CITY_AIR_UNIT_CAPACITY"));

	updateFreshWaterHealth();
	updateFeatureHealth();
	updateFeatureHappiness();
	updatePowerHealth();

	GET_PLAYER(getOwnerINLINE()).updateMaintenance();

	GC.getMapINLINE().updateWorkingCity();

	GC.getGameINLINE().AI_makeAssignWorkDirty();

	GET_PLAYER(getOwnerINLINE()).setFoundedFirstCity(true);

	if (GC.getGameINLINE().isFinalInitialized())
	{
		if (GET_PLAYER(getOwnerINLINE()).getNumCities() == 1)
		{
			for (iI = 0; iI < GC.getNumBuildingClassInfos(); iI++)
			{
				if (GC.getCivilizationInfo(getCivilizationType()).isCivilizationFreeBuildingClass(iI))
				{
					eLoopBuilding = ((BuildingTypes)(GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(iI)));

					if (eLoopBuilding != NO_BUILDING)
					{
						setNumRealBuilding(eLoopBuilding, true);
					}
				}
			}

			if (!isHuman())
			{
				changeOverflowProduction(GC.getDefineINT("INITIAL_AI_CITY_PRODUCTION"), 0);
			}
		}
	}

	updateEspionageVisibility(false);

	if (bUpdatePlotGroups)
	{
		GC.getGameINLINE().updatePlotGroups();
	}

	AI_init();
}


void CvCity::uninit()
{
	SAFE_DELETE_ARRAY(m_paiNoBonus);
	SAFE_DELETE_ARRAY(m_paiFreeBonus);
	SAFE_DELETE_ARRAY(m_paiNumBonuses);
	SAFE_DELETE_ARRAY(m_paiNumCorpProducedBonuses);
	SAFE_DELETE_ARRAY(m_paiProjectProduction);
	SAFE_DELETE_ARRAY(m_paiBuildingProduction);
	SAFE_DELETE_ARRAY(m_paiBuildingProductionTime);
	SAFE_DELETE_ARRAY(m_paiBuildingOriginalOwner);
	SAFE_DELETE_ARRAY(m_paiBuildingOriginalTime);
	SAFE_DELETE_ARRAY(m_paiUnitProduction);
	SAFE_DELETE_ARRAY(m_paiUnitProductionTime);
	SAFE_DELETE_ARRAY(m_paiGreatPeopleUnitRate);
	SAFE_DELETE_ARRAY(m_paiGreatPeopleUnitProgress);
	SAFE_DELETE_ARRAY(m_paiSpecialistCount);
	SAFE_DELETE_ARRAY(m_paiMaxSpecialistCount);
	SAFE_DELETE_ARRAY(m_paiForceSpecialistCount);
	SAFE_DELETE_ARRAY(m_paiFreeSpecialistCount);
	SAFE_DELETE_ARRAY(m_paiImprovementFreeSpecialists);
	SAFE_DELETE_ARRAY(m_paiReligionInfluence);
	SAFE_DELETE_ARRAY(m_paiStateReligionHappiness);
	SAFE_DELETE_ARRAY(m_paiUnitCombatFreeExperience);
	SAFE_DELETE_ARRAY(m_paiFreePromotionCount);
	SAFE_DELETE_ARRAY(m_paiNumRealBuilding);
	SAFE_DELETE_ARRAY(m_paiNumFreeBuilding);

	SAFE_DELETE_ARRAY(m_pabWorkingPlot);
	SAFE_DELETE_ARRAY(m_pabHasReligion);
	SAFE_DELETE_ARRAY(m_pabHasCorporation);
	SAFE_DELETE_ARRAY(m_pabIsUnitHurried); // Leoreth

	// Leoreth
	if (m_ppaiBonusYield != NULL)
	{
		for (int i = 0; i < GC.getNumBonusInfos(); i++)
		{
			SAFE_DELETE_ARRAY(m_ppaiBonusYield[i]);
		}
		SAFE_DELETE_ARRAY(m_ppaiBonusYield);
	}

	SAFE_DELETE_ARRAY(m_paTradeCities);

	m_orderQueue.clear();
}

// FUNCTION: reset()
// Initializes data members that are serialized.
void CvCity::reset(int iID, PlayerTypes eOwner, int iX, int iY, bool bConstructorCall)
{
	int iI, iJ;

	//--------------------------------
	// Uninit class
	uninit();

	m_iID = iID;
	m_iX = iX;
	m_iY = iY;
	m_iRallyX = INVALID_PLOT_COORD;
	m_iRallyY = INVALID_PLOT_COORD;
	m_iGameTurnFounded = 0;
	m_iGameTurnAcquired = 0;
	m_iPopulation = 0;
	m_iHighestPopulation = 0;
	m_iWorkingPopulation = 0;
	m_iSpecialistPopulation = 0;
	m_iNumGreatPeople = 0;
	m_iBaseGreatPeopleRate = 0;
	m_iGreatPeopleRateModifier = 0;
	m_iGreatPeopleProgress = 0;
	m_iNumWorldWonders = 0;
	m_iNumTeamWonders = 0;
	m_iNumNationalWonders = 0;
	m_iNumBuildings = 0;
	m_iGovernmentCenterCount = 0;
	m_iMaintenance = 0;
	m_iMaintenanceModifier = 0;
	m_iWarWearinessModifier = 0;
	m_iHurryAngerModifier = 0;
	m_iHealRate = 0;
	m_iEspionageHealthCounter = 0;
	m_iEspionageHappinessCounter = 0;
	m_iFreshWaterGoodHealth = 0;
	m_iFreshWaterBadHealth = 0;
	m_iFeatureGoodHealth = 0;
	m_iFeatureBadHealth = 0;
	m_iBuildingGoodHealth = 0;
	m_iBuildingBadHealth = 0;
	m_iPowerGoodHealth = 0;
	m_iPowerBadHealth = 0;
	m_iBonusGoodHealth = 0;
	m_iBonusBadHealth = 0;
	m_iHurryAngerTimer = 0;
	m_iConscriptAngerTimer = 0;
	m_iDefyResolutionAngerTimer = 0;
	m_iHappinessTimer = 0;
	m_iMilitaryHappinessUnits = 0;
	m_iBuildingGoodHappiness = 0;
	m_iBuildingBadHappiness = 0;
	m_iExtraBuildingGoodHappiness = 0;
	m_iExtraBuildingBadHappiness = 0;
	m_iExtraBuildingGoodHealth = 0;
	m_iExtraBuildingBadHealth = 0;
	m_iFeatureGoodHappiness = 0;
	m_iFeatureBadHappiness = 0;
	m_iBonusGoodHappiness = 0;
	m_iBonusBadHappiness = 0;
	m_iReligionGoodHappiness = 0;
	m_iReligionBadHappiness = 0;
	m_iExtraHappiness = 0;
	m_iExtraHealth = 0;
	m_iNoUnhappinessCount = 0;
	m_iNoUnhealthyPopulationCount = 0;
	m_iBuildingOnlyHealthyCount = 0;
	m_iFood = 0;
	m_iFoodKept = 0;
	m_iMaxFoodKeptPercent = 0;
	m_iOverflowProduction = 0;
	m_iFeatureProduction = 0;
	m_iMilitaryProductionModifier = 0;
	m_iSpaceProductionModifier = 0;
	m_iExtraTradeRoutes = 0;
	m_iTradeRouteModifier = 0;
	m_iForeignTradeRouteModifier = 0;
	m_iBuildingDefense = 0;
	m_iBuildingBombardDefense = 0;
	m_iFreeExperience = 0;
	m_iCurrAirlift = 0;
	m_iMaxAirlift = 0;
	m_iAirModifier = 0;
	m_iAirUnitCapacity = 0;
	m_iNukeModifier = 0;
	m_iFreeSpecialist = 0;
	m_iPowerCount = 0;
	m_iDirtyPowerCount = 0;
	m_iDefenseDamage = 0;
	m_iLastDefenseDamage = 0;
	m_iOccupationTimer = 0;
	m_iCultureUpdateTimer = 0;
	m_iCitySizeBoost = 0;
	m_iSpecialistFreeExperience = 0;
	m_iEspionageDefenseModifier = 0;

	// Leoreth
	m_iSpecialistGoodHappiness = 0;
	m_iSpecialistBadHappiness = 0;

	m_iCorporationGoodHappiness = 0;
	m_iCorporationBadHappiness = 0;
	m_iCorporationHealth = 0;
	m_iCorporationUnhealth = 0;

	m_iNextCoveredPlot = 0;

	m_bNeverLost = true;
	m_bBombarded = false;
	m_bDrafted = false;
	m_bAirliftTargeted = false;
	m_bWeLoveTheKingDay = false;
	m_bCitizensAutomated = true;
	m_bProductionAutomated = false;
	m_bWallOverride = false;
	m_bInfoDirty = true;
	m_bLayoutDirty = false;
	m_bPlundered = false;
	m_bMongolUP = false;

/************************************************************************************************/
/* UNOFFICIAL_PATCH                       12/07/09                         denev & jdog5000     */
/*                                                                                              */
/* Bugfix                                                                                       */
/************************************************************************************************/
	m_bPopProductionProcess = false;
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/

	m_eOwner = eOwner;
	m_ePreviousOwner = NO_PLAYER;
	m_eOriginalOwner = eOwner;
	m_eCultureLevel = NO_CULTURELEVEL;
	m_eArtStyle = (eOwner != NO_PLAYER) ? GET_PLAYER(eOwner).getArtStyleType() : NO_ARTSTYLE;

	for (iI = 0; iI < NUM_YIELD_TYPES; iI++)
	{
		m_aiSeaPlotYield[iI] = 0;
		m_aiRiverPlotYield[iI] = 0;
		m_aiBaseYieldRate[iI] = 0;
		m_aiYieldRateModifier[iI] = 0;
		m_aiPowerYieldRateModifier[iI] = 0;
		m_aiBonusYieldRateModifier[iI] = 0;
		m_aiTradeYield[iI] = 0;
		m_aiCorporationYield[iI] = 0;
		m_aiExtraSpecialistYield[iI] = 0;
	}

	for (iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
	{
		m_aiCommerceRate[iI] = 0;
		m_aiProductionToCommerceModifier[iI] = 0;
		m_aiBuildingCommerce[iI] = 0;
		m_aiSpecialistCommerce[iI] = 0;
		m_aiReligionCommerce[iI] = 0;
		m_aiCorporationCommerce[iI] = 0;
		m_aiCommerceRateModifier[iI] = 0;
		m_aiBonusCommerceRateModifier[iI] = 0; // Leoreth
		m_aiCommerceHappinessPer[iI] = 0;
	}

	for (iI = 0; iI < NUM_DOMAIN_TYPES; iI++)
	{
		m_aiDomainFreeExperience[iI] = 0;
		m_aiDomainProductionModifier[iI] = 0;
	}

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		m_aiCulture[iI] = 0;
		m_aiNumRevolts[iI] = 0;
		m_aiGameTurnPlayerLost[iI] = -1; // Leoreth
	}

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		m_abEverOwned[iI] = false;
		m_abTradeRoute[iI] = false;
	}

	for (iI = 0; iI < MAX_TEAMS; iI++)
	{
		m_abRevealed[iI] = false;
	}

	for (iI = 0; iI < MAX_TEAMS; iI++)
	{
		m_abEspionageVisibility[iI] = false;
	}

	m_szName.clear();
	m_szScriptData = "";

	m_bPopulationRankValid = false;
	m_iPopulationRank = -1;

	for (iI = 0; iI < NUM_YIELD_TYPES; iI++)
	{
		m_abBaseYieldRankValid[iI] = false;
		m_abYieldRankValid[iI] = false;
		m_aiBaseYieldRank[iI] = -1;
		m_aiYieldRank[iI] = -1;
	}

	for (iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
	{
		m_abCommerceRankValid[iI] = false;
		m_aiCommerceRank[iI] = -1;
	}

	if (!bConstructorCall)
	{
		FAssertMsg((0 < GC.getNumBonusInfos()),  "GC.getNumBonusInfos() is not greater than zero but an array is being allocated in CvCity::reset");
		m_paiNoBonus = new int[GC.getNumBonusInfos()];
		m_paiFreeBonus = new int[GC.getNumBonusInfos()];
		m_paiNumBonuses = new int[GC.getNumBonusInfos()];
		m_paiNumCorpProducedBonuses = new int[GC.getNumBonusInfos()];
		for (iI = 0; iI < GC.getNumBonusInfos(); iI++)
		{
			m_paiNoBonus[iI] = 0;
			m_paiFreeBonus[iI] = 0;
			m_paiNumBonuses[iI] = 0;
			m_paiNumCorpProducedBonuses[iI] = 0;
		}

		m_paiProjectProduction = new int[GC.getNumProjectInfos()];
		for (iI = 0; iI < GC.getNumProjectInfos(); iI++)
		{
			m_paiProjectProduction[iI] = 0;
		}

		FAssertMsg((0 < GC.getNumBuildingInfos()),  "GC.getNumBuildingInfos() is not greater than zero but an array is being allocated in CvCity::reset");
		//m_ppBuildings = new CvBuilding *[GC.getNumBuildingInfos()];
		m_paiBuildingProduction = new int[GC.getNumBuildingInfos()];
		m_paiBuildingProductionTime = new int[GC.getNumBuildingInfos()];
		m_paiBuildingOriginalOwner = new int[GC.getNumBuildingInfos()];
		m_paiBuildingOriginalTime = new int[GC.getNumBuildingInfos()];
		m_paiNumRealBuilding = new int[GC.getNumBuildingInfos()];
		m_paiNumFreeBuilding = new int[GC.getNumBuildingInfos()];
		for (iI = 0; iI < GC.getNumBuildingInfos(); iI++)
		{
			//m_ppBuildings[iI] = NULL;
			m_paiBuildingProduction[iI] = 0;
			m_paiBuildingProductionTime[iI] = 0;
			m_paiBuildingOriginalOwner[iI] = -1;
			m_paiBuildingOriginalTime[iI] = MIN_INT;
			m_paiNumRealBuilding[iI] = 0;
			m_paiNumFreeBuilding[iI] = 0;
		}

		FAssertMsg((0 < GC.getNumUnitInfos()),  "GC.getNumUnitInfos() is not greater than zero but an array is being allocated in CvCity::reset");
		m_paiUnitProduction = new int[GC.getNumUnitInfos()];
		m_paiUnitProductionTime = new int[GC.getNumUnitInfos()];
		m_paiGreatPeopleUnitRate = new int[GC.getNumUnitInfos()];
		m_paiGreatPeopleUnitProgress = new int[GC.getNumUnitInfos()];
		m_pabIsUnitHurried = new bool[GC.getNumUnitInfos()]; // Leoreth
		for (iI = 0;iI < GC.getNumUnitInfos();iI++)
		{
			m_paiUnitProduction[iI] = 0;
			m_paiUnitProductionTime[iI] = 0;
			m_paiGreatPeopleUnitRate[iI] = 0;
			m_paiGreatPeopleUnitProgress[iI] = 0;
			m_pabIsUnitHurried[iI] = false; // Leoreth
		}

		FAssertMsg((0 < GC.getNumSpecialistInfos()),  "GC.getNumSpecialistInfos() is not greater than zero but an array is being allocated in CvCity::reset");
		m_paiSpecialistCount = new int[GC.getNumSpecialistInfos()];
		m_paiMaxSpecialistCount = new int[GC.getNumSpecialistInfos()];
		m_paiForceSpecialistCount = new int[GC.getNumSpecialistInfos()];
		m_paiFreeSpecialistCount = new int[GC.getNumSpecialistInfos()];
		for (iI = 0; iI < GC.getNumSpecialistInfos(); iI++)
		{
			m_paiSpecialistCount[iI] = 0;
			m_paiMaxSpecialistCount[iI] = 0;
			m_paiForceSpecialistCount[iI] = 0;
			m_paiFreeSpecialistCount[iI] = 0;
		}

		FAssertMsg((0 < GC.getNumImprovementInfos()),  "GC.getNumImprovementInfos() is not greater than zero but an array is being allocated in CvCity::reset");
		m_paiImprovementFreeSpecialists = new int[GC.getNumImprovementInfos()];
		for (iI = 0; iI < GC.getNumImprovementInfos(); iI++)
		{
			m_paiImprovementFreeSpecialists[iI] = 0;
		}

		m_paiReligionInfluence = new int[GC.getNumReligionInfos()];
		m_paiStateReligionHappiness = new int[GC.getNumReligionInfos()];
		m_pabHasReligion = new bool[GC.getNumReligionInfos()];
		for (iI = 0; iI < GC.getNumReligionInfos(); iI++)
		{
			m_paiReligionInfluence[iI] = 0;
			m_paiStateReligionHappiness[iI] = 0;
			m_pabHasReligion[iI] = false;
		}

		m_pabHasCorporation = new bool[GC.getNumCorporationInfos()];
		for (iI = 0; iI < GC.getNumCorporationInfos(); iI++)
		{
			m_pabHasCorporation[iI] = false;
		}

		FAssertMsg((0 < GC.getNumUnitCombatInfos()),  "GC.getNumUnitCombatInfos() is not greater than zero but an array is being allocated in CvCity::reset");
		m_paiUnitCombatFreeExperience = new int[GC.getNumUnitCombatInfos()];
		for (iI = 0; iI < GC.getNumUnitCombatInfos(); iI++)
		{
			m_paiUnitCombatFreeExperience[iI] = 0;
		}

		FAssertMsg((0 < GC.getNumPromotionInfos()),  "GC.getNumPromotionInfos() is not greater than zero but an array is being allocated in CvCity::reset");
		m_paiFreePromotionCount = new int[GC.getNumPromotionInfos()];
		for (iI = 0; iI < GC.getNumPromotionInfos(); iI++)
		{
			m_paiFreePromotionCount[iI] = 0;
		}

		FAssertMsg((0 < NUM_CITY_PLOTS),  "NUM_CITY_PLOTS is not greater than zero but an array is being allocated in CvCity::reset");
		m_pabWorkingPlot = new bool[NUM_CITY_PLOTS];
		for (iI = 0; iI < NUM_CITY_PLOTS; iI++)
		{
			m_pabWorkingPlot[iI] = false;
		}

		// Leoreth
		m_ppaiBonusYield = new int*[GC.getNumBonusInfos()];
		for (iI = 0; iI < GC.getNumBonusInfos(); iI++)
		{
			m_ppaiBonusYield[iI] = new int[NUM_YIELD_TYPES];
			for (iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
			{
				m_ppaiBonusYield[iI][iJ] = 0;
			}
		}

		FAssertMsg((0 < GC.getDefineINT("MAX_TRADE_ROUTES")),  "GC.getMAX_TRADE_ROUTES() is not greater than zero but an array is being allocated in CvCity::reset");
		m_paTradeCities = new IDInfo[GC.getDefineINT("MAX_TRADE_ROUTES")];
		for (iI = 0; iI < GC.getDefineINT("MAX_TRADE_ROUTES"); iI++)
		{
			m_paTradeCities[iI].reset();
		}

		m_aEventsOccured.clear();
		m_aBuildingYieldChange.clear();
		m_aBuildingCommerceChange.clear();
		m_aBuildingHappyChange.clear();
		m_aBuildingHealthChange.clear();
	}

	int iX, iY, iIndex;
	for (iI = 0; iI < NUM_CITY_PLOTS_3; iI++)
	{
		iX = getX() + GC.getCityPlot3X()[iI];
		iY = getY() + GC.getCityPlot3Y()[iI];

		// wrap around X coordinate
		if (iX >= GC.getMap().getGridWidthINLINE()) iX -= GC.getMap().getGridWidthINLINE();
		else if (iX < 0) iX += GC.getMap().getGridWidthINLINE();

		// handle invalid Y coordinates
		if (iY >= GC.getMap().getGridHeightINLINE() || iY < 0) iIndex = -1;
		else iIndex = GC.getMap().plotNum(getX() + GC.getCityPlot3X()[iI], getY() + GC.getCityPlot3Y()[iI]);

		m_aiCulturePlots[iI] = iIndex;
	}

	updateCultureCosts();

	if (!bConstructorCall)
	{
		AI_reset();
	}
}


//////////////////////////////////////
// graphical only setup
//////////////////////////////////////
void CvCity::setupGraphical()
{
	if (!GC.IsGraphicsInitialized())
	{
		return;
	}

	CvDLLEntity::setup();

	setInfoDirty(true);
	setLayoutDirty(true);
}

void CvCity::kill(bool bUpdatePlotGroups)
{
	CvPlot* pPlot;
	CvPlot* pAdjacentPlot;
	CvPlot* pLoopPlot;
	PlayerTypes eOwner;
	bool bCapital;
	int iI;

	if (isCitySelected())
	{
		gDLL->getInterfaceIFace()->clearSelectedCities();
	}

	pPlot = plot();

	for (iI = 0; iI < NUM_CITY_PLOTS; iI++)
	{
		pLoopPlot = getCityIndexPlot(iI);

		if (pLoopPlot != NULL)
		{
			if (pLoopPlot->getWorkingCityOverride() == this)
			{
				pLoopPlot->setWorkingCityOverride(NULL);
			}
		}
	}

	setCultureLevel(NO_CULTURELEVEL, false);
	setNextCoveredPlot(0, false);

	for (iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		setNumRealBuilding(((BuildingTypes)iI), 0);
		setNumFreeBuilding(((BuildingTypes)iI), 0);
	}

	for (iI = 0; iI < GC.getNumSpecialistInfos(); iI++)
	{
		setFreeSpecialistCount(((SpecialistTypes)iI), 0);
	}

	for (iI = 0; iI < NUM_YIELD_TYPES; iI++)
	{
		setTradeYield(((YieldTypes)iI), 0);
		setCorporationYield(((YieldTypes) iI), 0);
	}

	for (iI = 0; iI < GC.getNumReligionInfos(); iI++)
	{
		setHasReligion(((ReligionTypes)iI), false, false, true);

		if (isHolyCity((ReligionTypes)iI))
		{
			GC.getGameINLINE().setHolyCity(((ReligionTypes)iI), NULL, false);
		}
	}

	for (iI = 0; iI < GC.getNumCorporationInfos(); iI++)
	{
		setHasCorporation(((CorporationTypes)iI), false, false);

		if (isHeadquarters((CorporationTypes)iI))
		{
			GC.getGameINLINE().setHeadquarters(((CorporationTypes)iI), NULL, false);
		}
	}

	setPopulation(0);

	AI_assignWorkingPlots();

	clearOrderQueue();

	// remember the visibility before we take away the city from the plot below
	std::vector<bool> abEspionageVisibility;
	for (iI = 0; iI < MAX_TEAMS; iI++)
	{
		abEspionageVisibility.push_back(getEspionageVisibility((TeamTypes)iI));
	}

/************************************************************************************************/
/* UNOFFICIAL_PATCH                       08/04/09                                jdog5000      */
/*                                                                                              */
/* Bugfix                                                                                       */
/************************************************************************************************/
	// Need to clear trade routes of dead city, else they'll be claimed for the owner forever
	clearTradeRoutes();
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/

	pPlot->setPlotCity(NULL);

	area()->changeCitiesPerPlayer(getOwnerINLINE(), -1);

	GET_TEAM(getTeam()).changeNumCities(-1);

	GC.getGameINLINE().changeNumCities(-1);

	FAssertMsg(getWorkingPopulation() == 0, "getWorkingPopulation is expected to be 0");
	FAssertMsg(!isWorkingPlot(CITY_HOME_PLOT), "isWorkingPlot(CITY_HOME_PLOT) is expected to be false");
	FAssertMsg(getSpecialistPopulation() == 0, "getSpecialistPopulation is expected to be 0");
	FAssertMsg(getNumGreatPeople() == 0, "getNumGreatPeople is expected to be 0");
	FAssertMsg(getBaseYieldRate(YIELD_FOOD) == 0, "getBaseYieldRate(YIELD_FOOD) is expected to be 0");
	FAssertMsg(getBaseYieldRate(YIELD_PRODUCTION) == 0, "getBaseYieldRate(YIELD_PRODUCTION) is expected to be 0");
	FAssertMsg(getBaseYieldRate(YIELD_COMMERCE) == 0, "getBaseYieldRate(YIELD_COMMERCE) is expected to be 0");
	FAssertMsg(!isProduction(), "isProduction is expected to be false");

	eOwner = getOwnerINLINE();

	bCapital = isCapital();

	pPlot->setImprovementType((ImprovementTypes)(GC.getDefineINT("RUINS_IMPROVEMENT")));

	CvEventReporter::getInstance().cityLost(this);

	GET_PLAYER(getOwnerINLINE()).deleteCity(getID());

	pPlot->updateCulture(true, false);

	for (iI = 0; iI < NUM_DIRECTION_TYPES; iI++)
	{
		pAdjacentPlot = plotDirection(pPlot->getX_INLINE(), pPlot->getY_INLINE(), ((DirectionTypes)iI));

		if (pAdjacentPlot != NULL)
		{
			pAdjacentPlot->updateCulture(true, false);
		}
	}

	for (iI = 0; iI < MAX_TEAMS; iI++)
	{
		if (GET_TEAM(GET_PLAYER(eOwner).getTeam()).isVassal((TeamTypes)iI))
		{
			pPlot->changeAdjacentSight((TeamTypes)iI, GC.getDefineINT("PLOT_VISIBILITY_RANGE"), false, NULL, false);
		}
	}

	for (iI = 0; iI < MAX_TEAMS; iI++)
	{
		if (abEspionageVisibility[iI])
		{
			pPlot->changeAdjacentSight((TeamTypes)iI, GC.getDefineINT("PLOT_VISIBILITY_RANGE"), false, NULL, false);
		}
	}

	GET_PLAYER(eOwner).updateMaintenance();

	GC.getMapINLINE().updateWorkingCity();

	GC.getGameINLINE().AI_makeAssignWorkDirty();

	if (bCapital)
	{
		GET_PLAYER(eOwner).findNewCapital();

		GET_TEAM(GET_PLAYER(eOwner).getTeam()).resetVictoryProgress();
	}

	if (bUpdatePlotGroups)
	{
		GC.getGameINLINE().updatePlotGroups();
	}

	if (eOwner == GC.getGameINLINE().getActivePlayer())
	{
		gDLL->getInterfaceIFace()->setDirty(SelectionButtons_DIRTY_BIT, true);
	}
}


void CvCity::doTurn()
{
	PROFILE("CvCity::doTurn()");

	if (GC.getGame().getActivePlayer() == getOwner())
	{		
		GC.getGame().logMsg("CvCity::doTurn(): %d", GC.getGame().getGameTurn());
	}

	CvPlot* pLoopPlot;
	int iI;

	if (!isBombarded())
	{
		changeDefenseDamage(-(GC.getDefineINT("CITY_DEFENSE_DAMAGE_HEAL_RATE")));
	}

	setLastDefenseDamage(getDefenseDamage());
	setBombarded(false);
	setPlundered(false);
	setDrafted(false);
	setAirliftTargeted(false);
	setCurrAirlift(0);

	AI_doTurn();

	bool bAllowNoProduction = !doCheckProduction();

	doGrowth();

/*************************************************************************************************/
/**	SPEEDTWEAK (BarbCities) Sephi                                            					**/
/**	This function can be very slow for barbarian cities(adds 1-3sec to turn time).Reason unknown**/
/**	                                                                 							**/
/*************************************************************************************************/
/** orig
	doCulture();
**/
    if (!isBarbarian())
    {
        doCulture();
    }
/*************************************************************************************************/
/**	END                                                                  						**/
/*************************************************************************************************/

	doPlotCulture(false, getOwnerINLINE(), getCommerceRate(COMMERCE_CULTURE));

	doProduction(bAllowNoProduction);

	doDecay();

	doReligion();

	doGreatPeople();

	doMeltdown();

	updateEspionageVisibility(true);

	if (!isDisorder())
	{
		for (iI = 0; iI < NUM_CITY_PLOTS; iI++)
		{
			pLoopPlot = getCityIndexPlot(iI);

			if (pLoopPlot != NULL)
			{
				if (pLoopPlot->getWorkingCity() == this)
				{
					if (pLoopPlot->isBeingWorked())
					{
						pLoopPlot->doImprovement();
					}
				}
			}
		}
	}

	if (getCultureUpdateTimer() > 0)
	{
		changeCultureUpdateTimer(-1);
	}

	if (getOccupationTimer() > 0)
	{
		changeOccupationTimer(-1);
	}

	if (getHurryAngerTimer() > 0)
	{
		changeHurryAngerTimer(-1);
	}

	if (getConscriptAngerTimer() > 0)
	{
		changeConscriptAngerTimer(-1);
	}

	if (getDefyResolutionAngerTimer() > 0)
	{
		changeDefyResolutionAngerTimer(-1);
	}

	if (getHappinessTimer() > 0)
	{
		changeHappinessTimer(-1);
	}

	if (getEspionageHealthCounter() > 0)
	{
		changeEspionageHealthCounter(-1);
	}

	if (getEspionageHappinessCounter() > 0)
	{
		changeEspionageHappinessCounter(-1);
	}

	if (isOccupation() || (angryPopulation() > 0) || (healthRate() < 0))
	{
		setWeLoveTheKingDay(false);
	}
	else if ((getPopulation() >= GC.getDefineINT("WE_LOVE_THE_KING_POPULATION_MIN_POPULATION")) && (GC.getGameINLINE().getSorenRandNum(GC.getDefineINT("WE_LOVE_THE_KING_RAND"), "Do We Love The King?") < getPopulation()))
	{
		setWeLoveTheKingDay(true);
	}
	else
	{
		if (getHappinessTimer() == 0) //Leoreth
		{
			setWeLoveTheKingDay(false);
		}
	}

	// Leoreth: update art style type once per turn
	updateArtStyleType();

	
	if (GC.getGame().getActivePlayer() == getOwner())
	{		
		GC.getGame().logMsg("End CvCity::doTurn(): %d", GC.getGame().getGameTurn());
	}

	// ONEVENT - Do turn
/*************************************************************************************************/
/**	SPEEDTWEAK (Block Python) Sephi                                               	            **/
/**	If you want to allow modmodders to enable this Callback, see CvCity::cancreate for example  **/
/*************************************************************************************************/
/**
	CvEventReporter::getInstance().cityDoTurn(this, getOwnerINLINE());
/*************************************************************************************************/
/**	END	                                        												**/
/*************************************************************************************************/

	// XXX
#ifdef _DEBUG
	{
		CvPlot* pPlot;
		int iCount;
		int iI, iJ;

		for (iI = 0; iI < NUM_YIELD_TYPES; iI++)
		{
			FAssert(getBaseYieldRate((YieldTypes)iI) >= 0);
			FAssert(getYieldRate((YieldTypes)iI) >= 0);

			iCount = 0;

			for (iJ = 0; iJ < NUM_CITY_PLOTS; iJ++)
			{
				if (isWorkingPlot(iJ))
				{
					pPlot = getCityIndexPlot(iJ);

					if (pPlot != NULL)
					{
						iCount += pPlot->getYield((YieldTypes)iI);
					}
				}
			}

			for (iJ = 0; iJ < GC.getNumSpecialistInfos(); iJ++)
			{
				iCount += (GET_PLAYER(getOwnerINLINE()).specialistYield(((SpecialistTypes)iJ), ((YieldTypes)iI)) * (getSpecialistCount((SpecialistTypes)iJ) + getFreeSpecialistCount((SpecialistTypes)iJ)));
			}

			for (iJ = 0; iJ < GC.getNumBuildingInfos(); iJ++)
			{
				iCount += getNumActiveBuilding((BuildingTypes)iJ) * (GC.getBuildingInfo((BuildingTypes) iJ).getYieldChange(iI) + getBuildingYieldChange((BuildingClassTypes)GC.getBuildingInfo((BuildingTypes) iJ).getBuildingClassType(), (YieldTypes)iI));
			}

			iCount += getTradeYield((YieldTypes)iI);
			iCount += getCorporationYield((YieldTypes)iI);

			FAssert(iCount == getBaseYieldRate((YieldTypes)iI));
		}

		for (iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
		{
			FAssert(getBuildingCommerce((CommerceTypes)iI) >= 0);
			FAssert(getSpecialistCommerce((CommerceTypes)iI) >= 0);
			FAssert(getReligionCommerce((CommerceTypes)iI) >= 0);
			FAssert(getCorporationCommerce((CommerceTypes)iI) >= 0);
			FAssert(GET_PLAYER(getOwnerINLINE()).getFreeCityCommerce((CommerceTypes)iI) >= 0);
		}

		for (iI = 0; iI < GC.getNumBonusInfos(); iI++)
		{
			FAssert(isNoBonus((BonusTypes)iI) || getNumBonuses((BonusTypes)iI) >= ((isConnectedToCapital()) ? (GET_PLAYER(getOwnerINLINE()).getBonusImport((BonusTypes)iI) - GET_PLAYER(getOwnerINLINE()).getBonusExport((BonusTypes)iI)) : 0));
		}
	}
#endif
	// XXX
}


bool CvCity::isCitySelected()
{
	return gDLL->getInterfaceIFace()->isCitySelected(this);
}


bool CvCity::canBeSelected() const
{
	if ((getTeam() == GC.getGameINLINE().getActiveTeam()) || GC.getGameINLINE().isDebugMode())
	{
		return true;
	}

	if (GC.getGameINLINE().getActiveTeam() != NO_TEAM)
	{
		if (plot()->isInvestigate(GC.getGameINLINE().getActiveTeam()))
		{
			return true;
		}
	}

	// EspionageEffect
	for (int iLoop = 0; iLoop < GC.getNumEspionageMissionInfos(); iLoop++)
	{
		// Check the XML
		if (GC.getEspionageMissionInfo((EspionageMissionTypes)iLoop).isPassive() && GC.getEspionageMissionInfo((EspionageMissionTypes)iLoop).isInvestigateCity())
		{
			// Is Mission good?
			if (GET_PLAYER(GC.getGameINLINE().getActivePlayer()).canDoEspionageMission((EspionageMissionTypes)iLoop, getOwnerINLINE(), plot(), -1, NULL))
			{
				return true;
			}
		}
	}

	return false;
}


void CvCity::updateSelectedCity(bool bTestProduction)
{
	for (int iI = 0; iI < NUM_CITY_PLOTS; iI++)
	{
		CvPlot* pLoopPlot = getCityIndexPlot(iI);
		if (pLoopPlot != NULL)
		{
			pLoopPlot->updateShowCitySymbols();
		}
	}

	if (bTestProduction)
	{
		if ((getOwnerINLINE() == GC.getGameINLINE().getActivePlayer()) && !isProduction())
		{
			chooseProduction(NO_UNIT, NO_BUILDING, NO_PROJECT, false, true);
		}
	}
}


void CvCity::updateYield()
{
	CvPlot* pLoopPlot;
	int iI;

	for (iI = 0; iI < NUM_CITY_PLOTS; iI++)
	{
		pLoopPlot = getCityIndexPlot(iI);

		if (pLoopPlot != NULL)
		{
			pLoopPlot->updateYield();
		}
	}
}


// XXX kill this?
void CvCity::updateVisibility()
{
	PROFILE_FUNC();

	if (!GC.IsGraphicsInitialized())
	{
		return;
	}

	FAssert(GC.getGameINLINE().getActiveTeam() != NO_TEAM);

	CvDLLEntity::setVisible(isRevealed(GC.getGameINLINE().getActiveTeam(), true));
}


void CvCity::createGreatPeople(UnitTypes eGreatPersonUnit, bool bIncrementThreshold, bool bIncrementExperience)
{
	GET_PLAYER(getOwnerINLINE()).createGreatPeople(eGreatPersonUnit, bIncrementThreshold, bIncrementExperience, getX_INLINE(), getY_INLINE());
}


void CvCity::doTask(TaskTypes eTask, int iData1, int iData2, bool bOption, bool bAlt, bool bShift, bool bCtrl)
{
	switch (eTask)
	{
	case TASK_RAZE:
		GET_PLAYER(getOwnerINLINE()).raze(this);
		break;

	case TASK_DISBAND:
		GET_PLAYER(getOwnerINLINE()).disband(this);
		break;

	case TASK_GIFT:
		if (getLiberationPlayer(false) == iData1)
		{
			liberate(false);
		}
		else
		{
			GET_PLAYER((PlayerTypes)iData1).acquireCity(this, false, true, true);
			GET_PLAYER(getOwnerINLINE()).updateMaintenance(); // Leoreth
		}
		break;

	case TASK_LIBERATE:
		liberate(iData1 != 0);
		break;

	case TASK_SET_AUTOMATED_CITIZENS:
		setCitizensAutomated(bOption);
		break;

	case TASK_SET_AUTOMATED_PRODUCTION:
		setProductionAutomated(bOption, bAlt && bShift && bCtrl);
		break;

	case TASK_SET_EMPHASIZE:
		AI_setEmphasize(((EmphasizeTypes)iData1), bOption);
		break;

	case TASK_CHANGE_SPECIALIST:
		alterSpecialistCount(((SpecialistTypes)iData1), iData2);
		break;

	case TASK_CHANGE_WORKING_PLOT:
		alterWorkingPlot(iData1);
		break;

	case TASK_CLEAR_WORKING_OVERRIDE:
		clearWorkingOverride(iData1);
		break;

	case TASK_HURRY:
		hurry((HurryTypes)iData1);
		break;

	case TASK_CONSCRIPT:
		conscript();
		break;

	case TASK_CLEAR_ORDERS:
		clearOrderQueue();
		break;

	case TASK_RALLY_PLOT:
		setRallyPlot(GC.getMapINLINE().plotINLINE(iData1, iData2));
		break;

	case TASK_CLEAR_RALLY_PLOT:
		setRallyPlot(NULL);
		break;

	default:
		FAssertMsg(false, "eTask failed to match a valid option");
		break;
	}
}


void CvCity::chooseProduction(UnitTypes eTrainUnit, BuildingTypes eConstructBuilding, ProjectTypes eCreateProject, bool bFinish, bool bFront)
{
	CvPopupInfo* pPopupInfo = new CvPopupInfo(BUTTONPOPUP_CHOOSEPRODUCTION);
	if (NULL == pPopupInfo)
	{
		return;
	}
	pPopupInfo->setData1(getID());
	pPopupInfo->setOption1(bFinish);

	if (eTrainUnit != NO_UNIT)
	{
		pPopupInfo->setData2(ORDER_TRAIN);
		pPopupInfo->setData3(eTrainUnit);
	}
	else if (eConstructBuilding != NO_BUILDING)
	{
		pPopupInfo->setData2(ORDER_CONSTRUCT);
		pPopupInfo->setData3(eConstructBuilding);
	}
	else if (eCreateProject != NO_PROJECT)
	{
		pPopupInfo->setData2(ORDER_CREATE);
		pPopupInfo->setData3(eCreateProject);
	}
	else
	{
		pPopupInfo->setData2(NO_ORDER);
		pPopupInfo->setData3(NO_UNIT);
	}

	gDLL->getInterfaceIFace()->addPopup(pPopupInfo, getOwnerINLINE(), false, bFront);
}


int CvCity::getCityPlotIndex(const CvPlot* pPlot) const
{
	return plotCityXY(this, pPlot);
}


CvPlot* CvCity::getCityIndexPlot(int iIndex) const
{
	return plotCity(getX_INLINE(), getY_INLINE(), iIndex);
}


bool CvCity::canWork(CvPlot* pPlot) const
{
	if (pPlot->getWorkingCity() != this)
	{
		return false;
	}

	FAssertMsg(getCityPlotIndex(pPlot) != -1, "getCityPlotIndex(pPlot) is expected to be assigned (not -1)");

	if (pPlot->plotCheck(PUF_canSiege, getOwnerINLINE()) != NULL)
	{
		return false;
	}

	if (pPlot->isWater())
	{
		if (!(GET_TEAM(getTeam()).isWaterWork()))
		{
			return false;
		}

		if (pPlot->getBlockadedCount(getTeam()) > 0)
		{
			return false;
		}

		/* Replaced by blockade mission, above
		if (!(pPlot->plotCheck(PUF_canDefend, -1, -1, NO_PLAYER, getTeam())))
		{
			for (int iI = 0; iI < NUM_DIRECTION_TYPES; iI++)
			{
				CvPlot* pLoopPlot = plotDirection(pPlot->getX_INLINE(), pPlot->getY_INLINE(), ((DirectionTypes)iI));

				if (pLoopPlot != NULL)
				{
					if (pLoopPlot->isWater())
					{
						if (pLoopPlot->plotCheck(PUF_canSiege, getOwnerINLINE()) != NULL)
						{
							return false;
						}
					}
				}
			}
		}
		*/
	}

	if (!(pPlot->hasYield()))
	{
		return false;
	}

	return true;
}


void CvCity::verifyWorkingPlot(int iIndex)
{
	CvPlot* pPlot;

	FAssertMsg(iIndex >= 0, "iIndex expected to be >= 0");
	FAssertMsg(iIndex < NUM_CITY_PLOTS, "iIndex expected to be < NUM_CITY_PLOTS");

	if (isWorkingPlot(iIndex))
	{
		pPlot = getCityIndexPlot(iIndex);

		if (pPlot != NULL)
		{
			if (!canWork(pPlot))
			{
				setWorkingPlot(iIndex, false);

				AI_setAssignWorkDirty(true);
			}
		}
	}
}


void CvCity::verifyWorkingPlots()
{
	int iI;

	for (iI = 0; iI < NUM_CITY_PLOTS; iI++)
	{
		verifyWorkingPlot(iI);
	}
}


void CvCity::clearWorkingOverride(int iIndex)
{
	CvPlot* pPlot;

	pPlot = getCityIndexPlot(iIndex);

	if (pPlot != NULL)
	{
		pPlot->setWorkingCityOverride(NULL);
	}
}


int CvCity::countNumImprovedPlots(ImprovementTypes eImprovement, bool bPotential) const
{
	CvPlot* pLoopPlot;
	int iCount;
	int iI;

	iCount = 0;

	for (iI = 0; iI < NUM_CITY_PLOTS; iI++)
	{
		pLoopPlot = getCityIndexPlot(iI);

		if (pLoopPlot != NULL)
		{
			if (pLoopPlot->getWorkingCity() == this)
			{
				if (eImprovement != NO_IMPROVEMENT)
				{
					if (pLoopPlot->getImprovementType() == eImprovement ||
						(bPotential && pLoopPlot->canHaveImprovement(eImprovement, getTeam())))
					{
						++iCount;
					}
				}
				else if (pLoopPlot->getImprovementType() != NO_IMPROVEMENT)
				{
					iCount++;
				}
			}
		}
	}

	return iCount;
}


int CvCity::countNumWaterPlots() const
{
	CvPlot* pLoopPlot;
	int iCount;
	int iI;

	iCount = 0;

	for (iI = 0; iI < NUM_CITY_PLOTS; iI++)
	{
		pLoopPlot = getCityIndexPlot(iI);

		if (pLoopPlot != NULL)
		{
			if (pLoopPlot->getWorkingCity() == this)
			{
				if (pLoopPlot->isWater())
				{
					iCount++;
				}
			}
		}
	}

	return iCount;
}

int CvCity::countNumRiverPlots() const
{
	int iCount = 0;

	for (int iI = 0; iI < NUM_CITY_PLOTS; iI++)
	{
		CvPlot* pLoopPlot = getCityIndexPlot(iI);

		if (pLoopPlot != NULL)
		{
			if (pLoopPlot->getWorkingCity() == this)
			{
				if (pLoopPlot->isRiver())
				{
					++iCount;
				}
			}
		}
	}

	return iCount;
}


int CvCity::findPopulationRank() const
{
	if (!m_bPopulationRankValid)
	{
		int iRank = 1;

		int iLoop;
		CvCity* pLoopCity;
		for (pLoopCity = GET_PLAYER(getOwnerINLINE()).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER(getOwnerINLINE()).nextCity(&iLoop))
		{
			if ((pLoopCity->getPopulation() > getPopulation()) ||
				((pLoopCity->getPopulation() == getPopulation()) && (pLoopCity->getID() < getID())))
			{
				iRank++;
			}
		}

		// shenanigans are to get around the const check
		m_bPopulationRankValid = true;
		m_iPopulationRank = iRank;
	}

	return m_iPopulationRank;
}


int CvCity::findBaseYieldRateRank(YieldTypes eYield) const
{
	if (!m_abBaseYieldRankValid[eYield])
	{
		int iRate = getBaseYieldRate(eYield);

		int iRank = 1;

		int iLoop;
		CvCity* pLoopCity;
		for (pLoopCity = GET_PLAYER(getOwnerINLINE()).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER(getOwnerINLINE()).nextCity(&iLoop))
		{
			if ((pLoopCity->getBaseYieldRate(eYield) > iRate) ||
				((pLoopCity->getBaseYieldRate(eYield) == iRate) && (pLoopCity->getID() < getID())))
			{
				iRank++;
			}
		}

		m_abBaseYieldRankValid[eYield] = true;
		m_aiBaseYieldRank[eYield] = iRank;
	}

	return m_aiBaseYieldRank[eYield];
}


int CvCity::findYieldRateRank(YieldTypes eYield) const
{
	if (!m_abYieldRankValid[eYield])
	{
		int iRate = getYieldRate(eYield);

		int iRank = 1;

		int iLoop;
		CvCity* pLoopCity;
		for (pLoopCity = GET_PLAYER(getOwnerINLINE()).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER(getOwnerINLINE()).nextCity(&iLoop))
		{
			if ((pLoopCity->getYieldRate(eYield) > iRate) ||
				((pLoopCity->getYieldRate(eYield) == iRate) && (pLoopCity->getID() < getID())))
			{
				iRank++;
			}
		}

		m_abYieldRankValid[eYield] = true;
		m_aiYieldRank[eYield] = iRank;
	}

	return m_aiYieldRank[eYield];
}


int CvCity::findCommerceRateRank(CommerceTypes eCommerce) const
{
	if (!m_abCommerceRankValid[eCommerce])
	{
		int iRate = getCommerceRateTimes100(eCommerce);

		int iRank = 1;

		int iLoop;
		CvCity* pLoopCity;
		for (pLoopCity = GET_PLAYER(getOwnerINLINE()).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER(getOwnerINLINE()).nextCity(&iLoop))
		{
			if ((pLoopCity->getCommerceRateTimes100(eCommerce) > iRate) ||
					((pLoopCity->getCommerceRateTimes100(eCommerce) == iRate) && (pLoopCity->getID() < getID())))
			{
				iRank++;
			}
		}

		m_abCommerceRankValid[eCommerce] = true;
		m_aiCommerceRank[eCommerce] = iRank;
	}

	return m_aiCommerceRank[eCommerce];
}


// Returns one of the upgrades...
UnitTypes CvCity::allUpgradesAvailable(UnitTypes eUnit, int iUpgradeCount) const
{
	UnitTypes eUpgradeUnit;
	UnitTypes eTempUnit;
	UnitTypes eLoopUnit;
	bool bUpgradeFound;
	bool bUpgradeAvailable;
	bool bUpgradeUnavailable;
	int iI;

	FAssertMsg(eUnit != NO_UNIT, "eUnit is expected to be assigned (not NO_UNIT)");

	if (iUpgradeCount > GC.getNumUnitClassInfos())
	{
		return NO_UNIT;
	}

	eUpgradeUnit = NO_UNIT;

	bUpgradeFound = false;
	bUpgradeAvailable = false;
	bUpgradeUnavailable = false;

	for (iI = 0; iI < GC.getNumUnitClassInfos(); iI++)
	{
		if (GC.getUnitInfo(eUnit).getUpgradeUnitClass(iI))
		{
			eLoopUnit = (UnitTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(iI);

			if (eLoopUnit != NO_UNIT)
			{
				bUpgradeFound = true;

				eTempUnit = allUpgradesAvailable(eLoopUnit, (iUpgradeCount + 1));

				if (eTempUnit != NO_UNIT)
				{
					eUpgradeUnit = eTempUnit;
					bUpgradeAvailable = true;
				}
				else
				{
					bUpgradeUnavailable = true;
				}
			}
		}
	}

	if (iUpgradeCount > 0)
	{
		if (bUpgradeFound && bUpgradeAvailable)
		{
			FAssertMsg(eUpgradeUnit != NO_UNIT, "eUpgradeUnit is expected to be assigned (not NO_UNIT)");
			return eUpgradeUnit;
		}

		if (canTrain(eUnit, false, false, false, true))
		{
			return eUnit;
		}
	}
	else
	{
		if (bUpgradeFound && !bUpgradeUnavailable)
		{
			return eUpgradeUnit;
		}
	}

	return NO_UNIT;
}


bool CvCity::isWorldWondersMaxed() const
{
	if (GC.getGameINLINE().isOption(GAMEOPTION_ONE_CITY_CHALLENGE) && isHuman())
	{
		return false;
	}

	if (GC.getDefineINT("MAX_WORLD_WONDERS_PER_CITY") == -1)
	{
		return false;
	}

	if (getNumWorldWonders() >= GC.getDefineINT("MAX_WORLD_WONDERS_PER_CITY"))
	{
		return true;
	}

	return false;
}


bool CvCity::isTeamWondersMaxed() const
{
	if (GC.getGameINLINE().isOption(GAMEOPTION_ONE_CITY_CHALLENGE) && isHuman())
	{
		return false;
	}

	if (GC.getDefineINT("MAX_TEAM_WONDERS_PER_CITY") == -1)
	{
		return false;
	}

	if (getNumTeamWonders() >= GC.getDefineINT("MAX_TEAM_WONDERS_PER_CITY"))
	{
		return true;
	}

	return false;
}


bool CvCity::isNationalWondersMaxed() const
{
	int iMaxNumWonders = (GC.getGameINLINE().isOption(GAMEOPTION_ONE_CITY_CHALLENGE) && isHuman()) ? GC.getDefineINT("MAX_NATIONAL_WONDERS_PER_CITY_FOR_OCC") : GC.getDefineINT("MAX_NATIONAL_WONDERS_PER_CITY");

	if (iMaxNumWonders == -1)
	{
		return false;
	}

	if (getNumNationalWonders() >= iMaxNumWonders)
	{
		return true;
	}

	return false;
}


bool CvCity::isBuildingsMaxed() const
{
	if (GC.getGameINLINE().isOption(GAMEOPTION_ONE_CITY_CHALLENGE) && isHuman())
	{
		return false;
	}

	if (GC.getDefineINT("MAX_BUILDINGS_PER_CITY") == -1)
	{
		return false;
	}

	if (getNumBuildings() >= GC.getDefineINT("MAX_BUILDINGS_PER_CITY"))
	{
		return true;
	}

	return false;
}


bool CvCity::canTrain(UnitTypes eUnit, bool bContinue, bool bTestVisible, bool bIgnoreCost, bool bIgnoreUpgrades) const
{
	if (eUnit == NO_UNIT)
	{
		return false;
	}

	if(GC.getUSE_CAN_TRAIN_CALLBACK())
	{
		CyCity* pyCity = new CyCity((CvCity*)this);
		CyArgsList argsList;
		argsList.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
		argsList.add(eUnit);
		argsList.add(bContinue);
		argsList.add(bTestVisible);
		argsList.add(bIgnoreCost);
		argsList.add(bIgnoreUpgrades);
		long lResult=0;
		gDLL->getPythonIFace()->callFunction(PYGameModule, "canTrain", argsList.makeFunctionArgs(), &lResult);
		delete pyCity;	// python fxn must not hold on to this pointer
		if (lResult == 1)
		{
			return true;
		}
	}

	if (!(GET_PLAYER(getOwnerINLINE()).canTrain(eUnit, bContinue, bTestVisible, bIgnoreCost)))
	{
		return false;
	}

	if (!bIgnoreUpgrades)
	{
		if (allUpgradesAvailable(eUnit) != NO_UNIT)
		{
			return false;
		}
	}

	if (!plot()->canTrain(eUnit, bContinue, bTestVisible))
	{
		return false;
	}

	if(GC.getUSE_CANNOT_TRAIN_CALLBACK())
	{
		CyCity *pyCity = new CyCity((CvCity*)this);
		CyArgsList argsList2; // XXX
		argsList2.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
		argsList2.add(eUnit);
		argsList2.add(bContinue);
		argsList2.add(bTestVisible);
		argsList2.add(bIgnoreCost);
		argsList2.add(bIgnoreUpgrades);
		long lResult=0;
		gDLL->getPythonIFace()->callFunction(PYGameModule, "cannotTrain", argsList2.makeFunctionArgs(), &lResult);
		delete pyCity;	// python fxn must not hold on to this pointer
		if (lResult == 1)
		{
			return false;
		}
	}

	// Leoreth - build settlers only in cities on the same continent as the capital until the discovery of Astronomy
	if((int)eUnit == 4) // settler
	{
		int iCapitalRegion = GET_PLAYER(getOwner()).getCapitalCity()->getRegionID();
		int iRegion = getRegionID();

		int iCapitalContinent = -1;
		int iCityContinent = -1;

		switch (iCapitalRegion)
		{
			case REGION_BRITAIN:
			case REGION_IBERIA:
			case REGION_ITALY:
			case REGION_BALKANS:
			case REGION_SCANDINAVIA:
			case REGION_EUROPE:
			case REGION_RUSSIA:
				iCapitalContinent = 0;	// Europe = 0
				break;
			case REGION_ANATOLIA:
			case REGION_MESOPOTAMIA:
			case REGION_ARABIA:
			case REGION_EGYPT:
			case REGION_MAGHREB:
			case REGION_PERSIA:
				iCapitalContinent = 1; // Middle East = 1
				break;
			case REGION_INDIA:
			case REGION_DECCAN:
			case REGION_INDOCHINA:
			case REGION_INDONESIA:
			case REGION_CHINA:
			case REGION_KOREA:
			case REGION_JAPAN:
			case REGION_MANCHURIA:
			case REGION_TIBET:
			case REGION_CENTRAL_ASIA:
			case REGION_SIBERIA:
				iCapitalContinent = 2;	// East Asia = 2
				break;
			case REGION_AUSTRALIA:
			case REGION_OCEANIA:
				iCapitalContinent = 3;	// Australia = 3
				break;
			case REGION_ETHIOPIA:
			case REGION_WEST_AFRICA:
			case REGION_SOUTH_AFRICA:
				iCapitalContinent = 4;	// Africa = 4;
				break;
			case REGION_CANADA:
			case REGION_ALASKA:
			case REGION_UNITED_STATES:
			case REGION_CARIBBEAN:
			case REGION_MESOAMERICA:
				iCapitalContinent = 5;	// North America = 5
				break;
			case REGION_BRAZIL:
			case REGION_ARGENTINA:
			case REGION_PERU:
			case REGION_COLOMBIA:
				iCapitalContinent = 6;	// South America = 6
				break;
			default:
				FAssert(false);
				break;
		}

		
		switch (iRegion)
		{
			case REGION_BRITAIN:
			case REGION_IBERIA:
			case REGION_ITALY:
			case REGION_BALKANS:
			case REGION_SCANDINAVIA:
			case REGION_EUROPE:
			case REGION_RUSSIA:
				iCityContinent = 0;	// Europe = 0
				break;
			case REGION_ANATOLIA:
			case REGION_MESOPOTAMIA:
			case REGION_ARABIA:
			case REGION_EGYPT:
			case REGION_MAGHREB:
			case REGION_PERSIA:
				iCityContinent = 1; // Middle East = 1
				break;
			case REGION_INDIA:
			case REGION_DECCAN:
			case REGION_INDOCHINA:
			case REGION_INDONESIA:
			case REGION_CHINA:
			case REGION_KOREA:
			case REGION_JAPAN:
			case REGION_MANCHURIA:
			case REGION_TIBET:
			case REGION_CENTRAL_ASIA:
			case REGION_SIBERIA:
				iCityContinent = 2;	// East Asia = 2
				break;
			case REGION_AUSTRALIA:
			case REGION_OCEANIA:
				iCityContinent = 3;	// Australia = 3
				break;
			case REGION_ETHIOPIA:
			case REGION_WEST_AFRICA:
			case REGION_SOUTH_AFRICA:
				iCityContinent = 4;	// Africa = 4;
				break;
			case REGION_CANADA:
			case REGION_ALASKA:
			case REGION_UNITED_STATES:
			case REGION_CARIBBEAN:
			case REGION_MESOAMERICA:
				iCityContinent = 5;	// North America = 5
				break;
			case REGION_BRAZIL:
			case REGION_ARGENTINA:
			case REGION_PERU:
			case REGION_COLOMBIA:
				iCityContinent = 6;	// South America = 6
				break;
			default:
				FAssert(false);
				break;
		}

		bool bException = false;

		if (iCapitalRegion == REGION_RUSSIA && iRegion == REGION_SIBERIA)
		{
			bException = true;
		}
		else if ((iCapitalRegion == REGION_ANATOLIA || iCapitalRegion == REGION_BALKANS) && (iCityContinent == 0 || iCityContinent == 1))
		{
			bException = true;
		}
		else if ((iCapitalRegion == REGION_IBERIA && iRegion == REGION_MAGHREB) || (iCapitalRegion == REGION_MAGHREB && iRegion == REGION_IBERIA))
		{
			bException = true;
		}

		if (iCapitalContinent != iCityContinent && !bException)
		{
			if (!GET_TEAM(GET_PLAYER(getOwner()).getTeam()).isHasTech((TechTypes)ASTRONOMY))
			{
				return false;
			}
		}
	}

	// Leoreth: can't train slaves
	if (GC.getUnitInfo(eUnit).getUnitClassType() == GC.getInfoTypeForString("UNITCLASS_SLAVE"))
	{
		return false;
	}

	return true;
}

bool CvCity::canTrain(UnitCombatTypes eUnitCombat) const
{
	for (int i = 0; i < GC.getNumUnitClassInfos(); i++)
	{
		UnitTypes eUnit = (UnitTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(i);

		if (NO_UNIT != eUnit)
		{
			if (GC.getUnitInfo(eUnit).getUnitCombatType() == eUnitCombat)
			{
				if (canTrain(eUnit))
				{
					return true;
				}
			}
		}
	}

	return false;
}


bool CvCity::canConstruct(BuildingTypes eBuilding, bool bContinue, bool bTestVisible, bool bIgnoreCost) const
{
	BuildingTypes ePrereqBuilding;
	bool bRequiresBonus;
	bool bNeedsBonus;
	int iI;
	CorporationTypes eCorporation;

	if (eBuilding == NO_BUILDING)
	{
		return false;
	}

	if(GC.getUSE_CAN_CONSTRUCT_CALLBACK())
	{
		CyCity* pyCity = new CyCity((CvCity*)this);
		CyArgsList argsList;
		argsList.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
		argsList.add(eBuilding);
		argsList.add(bContinue);
		argsList.add(bTestVisible);
		argsList.add(bIgnoreCost);
		long lResult=0;
		gDLL->getPythonIFace()->callFunction(PYGameModule, "canConstruct", argsList.makeFunctionArgs(), &lResult);
		delete pyCity;	// python fxn must not hold on to this pointer
		if (lResult == 1)
		{
			return true;
		}
	}

	if (!(GET_PLAYER(getOwnerINLINE()).canConstruct(eBuilding, bContinue, bTestVisible, bIgnoreCost)))
	{
		return false;
	}

	if (getNumBuilding(eBuilding) >= GC.getCITY_MAX_NUM_BUILDINGS())
	{
		return false;
	}

	// Leoreth: pagan temples only if no religion present
	if (eBuilding == (BuildingTypes)PAGAN_TEMPLE)
	{
		if (getReligionCount() > 0)
		{
			return false;
		}
	}

	if (GC.getBuildingInfo(eBuilding).isPrereqReligion())
	{
		if (getReligionCount() > 0)
		{
			return false;
		}
	}

	if (GC.getBuildingInfo(eBuilding).isStateReligion())
	{
		ReligionTypes eStateReligion = GET_PLAYER(getOwnerINLINE()).getStateReligion();
		if (NO_RELIGION == eStateReligion || !isHasReligion(eStateReligion))
		{
			return false;
		}
	}

	bool bReligion = true;
	if (GC.getBuildingInfo(eBuilding).getPrereqReligion() != NO_RELIGION)
	{
		if (!(isHasReligion((ReligionTypes)(GC.getBuildingInfo(eBuilding).getPrereqReligion()))))
		{
			bReligion = false;
		}
	}

	// Leoreth: OR religion requirement
	bool bOrReligion = false;
	if (GC.getBuildingInfo(eBuilding).getOrPrereqReligion() != NO_RELIGION)
	{
		bOrReligion = true;
		if (!(isHasReligion((ReligionTypes)GC.getBuildingInfo(eBuilding).getOrPrereqReligion())))
		{
			bOrReligion = false;
		}
	}

	if (!bReligion && !bOrReligion)
	{
		return false;
	}

	eCorporation = (CorporationTypes)GC.getBuildingInfo(eBuilding).getPrereqCorporation();
	if (eCorporation != NO_CORPORATION)
	{
		if (!isHasCorporation(eCorporation))
		{
			return false;
		}
	}

	eCorporation = (CorporationTypes)GC.getBuildingInfo(eBuilding).getFoundsCorporation();
	if (eCorporation != NO_CORPORATION)
	{
		if (GC.getGameINLINE().isCorporationFounded(eCorporation))
		{
			return false;
		}

		for (int iCorporation = 0; iCorporation < GC.getNumCorporationInfos(); ++iCorporation)
		{
			if (isHeadquarters((CorporationTypes)iCorporation))
			{
				if (GC.getGameINLINE().isCompetingCorporation((CorporationTypes)iCorporation, eCorporation))
				{
					return false;
				}
			}
		}
	}

	if (!isValidBuildingLocation(eBuilding))
	{
		return false;
	}

	if (GC.getBuildingInfo(eBuilding).isGovernmentCenter())
	{
		if (isGovernmentCenter())
		{
			return false;
		}
	}

	//Rhye - start
	if (eBuilding == OLYMPIC_PARK)
	{
		if (GET_PLAYER(getOwnerINLINE()).isOlympics()) return false;
	}
	//Rhye - end

	// Leoreth: Moai Statues require 20 water tiles
	if (eBuilding == MOAI_STATUES)
	{
		int iNumWaterTiles = 0;
		for (iI = 0; iI < NUM_CITY_PLOTS; iI++)
		{
			if (getCityIndexPlot(iI)->isWater()) iNumWaterTiles++;
		}

		if (iNumWaterTiles < 20) return false;
	}

	//Rhye - start switch for the UHV
	if (eBuilding == RED_FORT)
	{
		if (getOwnerINLINE() != MUGHALS)
		{
			if (GET_PLAYER((PlayerTypes)MUGHALS).isHuman())
			{
				if (!GET_PLAYER((PlayerTypes)MUGHALS).isAlive())
				{
					return false;
				}
			}
		}
	}

	if (eBuilding == WEMBLEY || eBuilding == THREE_GORGES_DAM || eBuilding == CRISTO_REDENTOR)
	{
		if (getOwnerINLINE() != BRAZIL)
		{
			if (GET_PLAYER((PlayerTypes)BRAZIL).isHuman())
			{
				if (!GET_PLAYER((PlayerTypes)BRAZIL).isAlive())
				{
					return false;
				}
			}
		}
	}

	if (eBuilding == TEMPLE_OF_KUKULKAN)
	{
		if (getOwnerINLINE() != MAYA)
		{
			if (GET_PLAYER((PlayerTypes)MAYA).isHuman())
			{
				if (!GET_PLAYER((PlayerTypes)MAYA).isAlive())
				{
					return false;
				}
			}
		}
	}

	if (eBuilding == NOTRE_DAME)
	{
		if (getOwnerINLINE() != FRANCE)
		{
			if (GET_PLAYER((PlayerTypes)FRANCE).isHuman())
			{
				if (!GET_PLAYER((PlayerTypes)FRANCE).isAlive())
				{
					return false;
				}
			}
		}
	}

	if (eBuilding == STATUE_OF_LIBERTY)
	{
		if (getOwnerINLINE() != AMERICA)
		{
			if (GET_PLAYER((PlayerTypes)AMERICA).isHuman())
			{
				if (!GET_PLAYER((PlayerTypes)AMERICA).isAlive())
				{
					return false;
				}
			}
		}
	}
	//Rhye - end

	if (!bTestVisible)
	{
		if (!bContinue)
		{
			if (getFirstBuildingOrder(eBuilding) != -1)
			{
				return false;
			}
		}

		if (!(GC.getBuildingClassInfo((BuildingClassTypes)(GC.getBuildingInfo(eBuilding).getBuildingClassType())).isNoLimit()))
		{
			if (isWorldWonderClass((BuildingClassTypes)(GC.getBuildingInfo(eBuilding).getBuildingClassType())))
			{
				if (isWorldWondersMaxed())
				{
					return false;
				}
			}
			else if (isTeamWonderClass((BuildingClassTypes)(GC.getBuildingInfo(eBuilding).getBuildingClassType())))
			{
				if (isTeamWondersMaxed())
				{
					return false;
				}
			}
			else if (isNationalWonderClass((BuildingClassTypes)(GC.getBuildingInfo(eBuilding).getBuildingClassType())))
			{
				if (isNationalWondersMaxed())
				{
					return false;
				}
			}
			else
			{
				if (isBuildingsMaxed())
				{
					return false;
				}
			}
		}

		if (GC.getBuildingInfo(eBuilding).getHolyCity() != NO_RELIGION)
		{
			if (!isHolyCity(((ReligionTypes)(GC.getBuildingInfo(eBuilding).getHolyCity()))))
			{
				return false;
			}
		}

		if (GC.getBuildingInfo(eBuilding).getPrereqAndBonus() != NO_BONUS)
		{
			if (!hasBonus((BonusTypes)GC.getBuildingInfo(eBuilding).getPrereqAndBonus()))
			{
				return false;
			}
		}

		eCorporation = (CorporationTypes)GC.getBuildingInfo(eBuilding).getFoundsCorporation();
		if (eCorporation != NO_CORPORATION)
		{
			if (GC.getGameINLINE().isCorporationFounded(eCorporation))
			{
				return false;
			}

			if (GET_PLAYER(getOwnerINLINE()).isNoCorporations())
			{
				return false;
			}

			bool bValid = false;
			for (int i = 0; i < GC.getNUM_CORPORATION_PREREQ_BONUSES(); ++i)
			{
				BonusTypes eBonus = (BonusTypes)GC.getCorporationInfo(eCorporation).getPrereqBonus(i);
				if (NO_BONUS != eBonus)
				{
					if (hasBonus(eBonus))
					{
						bValid = true;
						break;
					}
				}
			}

			if (!bValid)
			{
				return false;
			}
		}

		if (plot()->getLatitude() > GC.getBuildingInfo(eBuilding).getMaxLatitude())
		{
			return false;
		}

		if (plot()->getLatitude() < GC.getBuildingInfo(eBuilding).getMinLatitude())
		{
			return false;
		}

		bRequiresBonus = false;
		bNeedsBonus = true;

		for (iI = 0; iI < GC.getNUM_BUILDING_PREREQ_OR_BONUSES(); iI++)
		{
			if (GC.getBuildingInfo(eBuilding).getPrereqOrBonuses(iI) != NO_BONUS)
			{
				bRequiresBonus = true;

				if (hasBonus((BonusTypes)GC.getBuildingInfo(eBuilding).getPrereqOrBonuses(iI)))
				{
					bNeedsBonus = false;
				}
			}
		}

		if (bRequiresBonus && bNeedsBonus)
		{
			return false;
		}

		for (iI = 0; iI < GC.getNumBuildingClassInfos(); iI++)
		{
			if (GC.getBuildingInfo(eBuilding).isBuildingClassNeededInCity(iI))
			{
				ePrereqBuilding = ((BuildingTypes)(GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(iI)));

				if (ePrereqBuilding != NO_BUILDING)
				{
					if (0 == getNumBuilding(ePrereqBuilding) /* && (bContinue || (getFirstBuildingOrder(ePrereqBuilding) == -1))*/)
					{
						return false;
					}
				}
			}
		}
	}

	if(GC.getUSE_CANNOT_CONSTRUCT_CALLBACK())
	{
		CyCity *pyCity = new CyCity((CvCity*)this);
		CyArgsList argsList2; // XXX
		argsList2.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
		argsList2.add(eBuilding);
		argsList2.add(bContinue);
		argsList2.add(bTestVisible);
		argsList2.add(bIgnoreCost);
		long lResult=0;
		gDLL->getPythonIFace()->callFunction(PYGameModule, "cannotConstruct", argsList2.makeFunctionArgs(), &lResult);
		delete pyCity;	// python fxn must not hold on to this pointer
		if (lResult == 1)
		{
			return false;
		}
	}

	return true;
}


bool CvCity::canCreate(ProjectTypes eProject, bool bContinue, bool bTestVisible) const
{
	//Rhye - start
//Speed: Modified by Kael 04/19/2007
//	CyCity* pyCity = new CyCity((CvCity*)this);
//	CyArgsList argsList;
//	argsList.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
//	argsList.add(eProject);
//	argsList.add(bContinue);
//	argsList.add(bTestVisible);
//	long lResult=0;
//	gDLL->getPythonIFace()->callFunction(PYGameModule, "canCreate", argsList.makeFunctionArgs(), &lResult);
//	delete pyCity;	// python fxn must not hold on to this pointer
//	if (lResult == 1)
//	{
//		return true;
//	}
//Speed: End Modify
	//Rhye - end

	if (!(GET_PLAYER(getOwnerINLINE()).canCreate(eProject, bContinue, bTestVisible)))
	{
		return false;
	}

	//Rhye - start
//Speed: Modified by Kael 04/19/2007
//	pyCity = new CyCity((CvCity*)this);
//	CyArgsList argsList2; // XXX
//	argsList2.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
//	argsList2.add(eProject);
//	argsList2.add(bContinue);
//	argsList2.add(bTestVisible);
//	lResult=0;
//	gDLL->getPythonIFace()->callFunction(PYGameModule, "cannotCreate", argsList2.makeFunctionArgs(), &lResult);
//	delete pyCity;	// python fxn must not hold on to this pointer
//	if (lResult == 1)
//	{
//		return false;
//	}
//Speed: End Modify
	//Rhye - end

	return true;
}


bool CvCity::canMaintain(ProcessTypes eProcess, bool bContinue) const
{
	//Rhye - start
//Speed: Modified by Kael 04/19/2007
//	CyCity* pyCity = new CyCity((CvCity*)this);
//	CyArgsList argsList;
//	argsList.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
//	argsList.add(eProcess);
//	argsList.add(bContinue);
//	long lResult=0;
//	gDLL->getPythonIFace()->callFunction(PYGameModule, "canMaintain", argsList.makeFunctionArgs(), &lResult);
//	delete pyCity;	// python fxn must not hold on to this pointer
//	if (lResult == 1)
//	{
//		return true;
//	}
//Speed: End Modify
	//Rhye - end

	if (!(GET_PLAYER(getOwnerINLINE()).canMaintain(eProcess, bContinue)))
	{
		return false;
	}

	//Rhye - start
//Speed: Modified by Kael 04/19/2007
//	pyCity = new CyCity((CvCity*)this);
//	CyArgsList argsList2; // XXX
//	argsList2.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
//	argsList2.add(eProcess);
//	argsList2.add(bContinue);
//	lResult=0;
//	gDLL->getPythonIFace()->callFunction(PYGameModule, "cannotMaintain", argsList2.makeFunctionArgs(), &lResult);
//	delete pyCity;	// python fxn must not hold on to this pointer
//	if (lResult == 1)
//	{
//		return false;
//	}
//Speed: End Modify
	//Rhye - end

	return true;
}


bool CvCity::canJoin() const
{
	return true;
}


int CvCity::getFoodTurnsLeft() const
{
	int iFoodLeft;
	int iTurnsLeft;

	iFoodLeft = (growthThreshold() - getFood());

	if (foodDifference() <= 0)
	{
		return iFoodLeft;
	}

	iTurnsLeft = (iFoodLeft / foodDifference());

	if ((iTurnsLeft * foodDifference()) <  iFoodLeft)
	{
		iTurnsLeft++;
	}

	return std::max(1, iTurnsLeft);
}


bool CvCity::isProduction() const
{
	return (headOrderQueueNode() != NULL);
}


bool CvCity::isProductionLimited() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		switch (pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
			return isLimitedUnitClass((UnitClassTypes)(GC.getUnitInfo((UnitTypes)(pOrderNode->m_data.iData1)).getUnitClassType()));
			break;

		case ORDER_CONSTRUCT:
			return isLimitedWonderClass((BuildingClassTypes)(GC.getBuildingInfo((BuildingTypes)(pOrderNode->m_data.iData1)).getBuildingClassType()));
			break;

		case ORDER_CREATE:
			return isLimitedProject((ProjectTypes)(pOrderNode->m_data.iData1));
			break;

		case ORDER_MAINTAIN:
			break;

		default:
			FAssertMsg(false, "pOrderNode->m_data.eOrderType failed to match a valid option");
			break;
		}
	}

	return false;
}


bool CvCity::isProductionUnit() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		return (pOrderNode->m_data.eOrderType == ORDER_TRAIN);
	}

	return false;
}


bool CvCity::isProductionBuilding() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		return (pOrderNode->m_data.eOrderType == ORDER_CONSTRUCT);
	}

	return false;
}


bool CvCity::isProductionProject() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		return (pOrderNode->m_data.eOrderType == ORDER_CREATE);
	}

	return false;
}


bool CvCity::isProductionProcess() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		return (pOrderNode->m_data.eOrderType == ORDER_MAINTAIN);
	}

	return false;
}


bool CvCity::canContinueProduction(OrderData order)
{
	switch (order.eOrderType)
	{
	case ORDER_TRAIN:
		return canTrain((UnitTypes)(order.iData1), true);
		break;

	case ORDER_CONSTRUCT:
		return canConstruct((BuildingTypes)(order.iData1), true);
		break;

	case ORDER_CREATE:
		return canCreate((ProjectTypes)(order.iData1), true);
		break;

	case ORDER_MAINTAIN:
		return canMaintain((ProcessTypes)(order.iData1), true);
		break;

	default:
		FAssertMsg(false, "order.eOrderType failed to match a valid option");
		break;
	}

	return false;
}


int CvCity::getProductionExperience(UnitTypes eUnit)
{
	int iExperience;

	iExperience = getFreeExperience();
	iExperience += GET_PLAYER(getOwnerINLINE()).getFreeExperience();

	if (eUnit != NO_UNIT)
	{
		if (GC.getUnitInfo(eUnit).getUnitCombatType() != NO_UNITCOMBAT)
		{
			iExperience += getUnitCombatFreeExperience((UnitCombatTypes)(GC.getUnitInfo(eUnit).getUnitCombatType()));
		}
		iExperience += getDomainFreeExperience((DomainTypes)(GC.getUnitInfo(eUnit).getDomainType()));

		if (!GC.getUnitInfo(eUnit).isSpy()) iExperience += getSpecialistFreeExperience();

		// Leoreth: domain specific experience from civics
		if (GC.getUnitInfo(eUnit).getDomainType() != NO_DOMAIN)
		{
			iExperience += GET_PLAYER(getOwnerINLINE()).getDomainExperienceModifier((DomainTypes)GC.getUnitInfo(eUnit).getDomainType());
		}
	}

	if (GET_PLAYER(getOwnerINLINE()).getStateReligion() != NO_RELIGION)
	{
		if (isHasReligion(GET_PLAYER(getOwnerINLINE()).getStateReligion()))
		{
			iExperience += GET_PLAYER(getOwnerINLINE()).getStateReligionFreeExperience();

			//Leoreth: Harmandir Sahib effect
            if (GET_PLAYER(getOwnerINLINE()).isHasBuilding((BuildingTypes)HARMANDIR_SAHIB))
                iExperience += 2;
		}
	}
	
	//SuperSpies: TSHEEP - Only give spies spy specific xp
	if (eUnit != NO_UNIT)
	{
        if(GC.getUnitInfo(eUnit).isSpy())
        {
            iExperience = 0;

            if (GC.getUnitInfo(eUnit).getUnitCombatType() != NO_UNITCOMBAT)
            {
                iExperience += getUnitCombatFreeExperience((UnitCombatTypes)(GC.getUnitInfo(eUnit).getUnitCombatType()));
            }
        }
	}
	//SuperSpies: TSHEEP end

	return std::max(0, iExperience);
}


void CvCity::addProductionExperience(CvUnit* pUnit, bool bConscript)
{
	int iI;

	if (pUnit->canAcquirePromotionAny())
	{
		pUnit->changeExperience(getProductionExperience(pUnit->getUnitType()) / ((bConscript) ? 2 : 1));
	}

	for (iI = 0; iI < GC.getNumPromotionInfos(); iI++)
	{
		if (isFreePromotion((PromotionTypes)iI))
		{
			if ((pUnit->getUnitCombatType() != NO_UNITCOMBAT) && GC.getPromotionInfo((PromotionTypes)iI).getUnitCombat(pUnit->getUnitCombatType()))
			{
				pUnit->setHasPromotion(((PromotionTypes)iI), true);
			}
		}
	}

	pUnit->testPromotionReady();
}


UnitTypes CvCity::getProductionUnit() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		switch (pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
			return ((UnitTypes)(pOrderNode->m_data.iData1));
			break;

		case ORDER_CONSTRUCT:
		case ORDER_CREATE:
		case ORDER_MAINTAIN:
			break;

		default:
			FAssertMsg(false, "pOrderNode->m_data.eOrderType failed to match a valid option");
			break;
		}
	}

	return NO_UNIT;
}


UnitAITypes CvCity::getProductionUnitAI() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		switch (pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
			return ((UnitAITypes)(pOrderNode->m_data.iData2));
			break;

		case ORDER_CONSTRUCT:
		case ORDER_CREATE:
		case ORDER_MAINTAIN:
			break;

		default:
			FAssertMsg(false, "pOrderNode->m_data.eOrderType failed to match a valid option");
			break;
		}
	}

	return NO_UNITAI;
}


BuildingTypes CvCity::getProductionBuilding() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		switch (pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
			break;

		case ORDER_CONSTRUCT:
			return ((BuildingTypes)(pOrderNode->m_data.iData1));
			break;

		case ORDER_CREATE:
		case ORDER_MAINTAIN:
			break;

		default:
			FAssertMsg(false, "pOrderNode->m_data.eOrderType failed to match a valid option");
			break;
		}
	}

	return NO_BUILDING;
}


ProjectTypes CvCity::getProductionProject() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		switch (pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
		case ORDER_CONSTRUCT:
			break;

		case ORDER_CREATE:
			return ((ProjectTypes)(pOrderNode->m_data.iData1));
			break;

		case ORDER_MAINTAIN:
			break;

		default:
			FAssertMsg(false, "pOrderNode->m_data.eOrderType failed to match a valid option");
			break;
		}
	}

	return NO_PROJECT;
}


ProcessTypes CvCity::getProductionProcess() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		switch (pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
		case ORDER_CONSTRUCT:
		case ORDER_CREATE:
			break;

		case ORDER_MAINTAIN:
			return ((ProcessTypes)(pOrderNode->m_data.iData1));
			break;

		default:
			FAssertMsg(false, "pOrderNode->m_data.eOrderType failed to match a valid option");
			break;
		}
	}

	return NO_PROCESS;
}


const wchar* CvCity::getProductionName() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		switch (pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
			return GC.getUnitInfo((UnitTypes) pOrderNode->m_data.iData1).getDescription();
			break;

		case ORDER_CONSTRUCT:
			return GC.getBuildingInfo((BuildingTypes) pOrderNode->m_data.iData1).getDescription();
			break;

		case ORDER_CREATE:
			return GC.getProjectInfo((ProjectTypes) pOrderNode->m_data.iData1).getDescription();
			break;

		case ORDER_MAINTAIN:
			return GC.getProcessInfo((ProcessTypes) pOrderNode->m_data.iData1).getDescription();
			break;

		default:
			FAssertMsg(false, "pOrderNode->m_data.eOrderType failed to match a valid option");
			break;
		}
	}

	return L"";
}


int CvCity::getGeneralProductionTurnsLeft() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		switch (pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
			return getProductionTurnsLeft((UnitTypes)pOrderNode->m_data.iData1, 0);
			break;

		case ORDER_CONSTRUCT:
			return getProductionTurnsLeft((BuildingTypes)pOrderNode->m_data.iData1, 0);
			break;

		case ORDER_CREATE:
			return getProductionTurnsLeft((ProjectTypes)pOrderNode->m_data.iData1, 0);
			break;

		case ORDER_MAINTAIN:
			return 0;
			break;

		default:
			FAssertMsg(false, "pOrderNode->m_data.eOrderType failed to match a valid option");
			break;
		}
	}

	return 0;
}


const wchar* CvCity::getProductionNameKey() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		switch (pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
			return GC.getUnitInfo((UnitTypes) pOrderNode->m_data.iData1).getTextKeyWide();
			break;

		case ORDER_CONSTRUCT:
			return GC.getBuildingInfo((BuildingTypes) pOrderNode->m_data.iData1).getTextKeyWide();
			break;

		case ORDER_CREATE:
			return GC.getProjectInfo((ProjectTypes) pOrderNode->m_data.iData1).getTextKeyWide();
			break;

		case ORDER_MAINTAIN:
			return GC.getProcessInfo((ProcessTypes) pOrderNode->m_data.iData1).getTextKeyWide();
			break;

		default:
			FAssertMsg(false, "pOrderNode->m_data.eOrderType failed to match a valid option");
			break;
		}
	}

	return L"";
}


bool CvCity::isFoodProduction() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		switch (pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
			return isFoodProduction((UnitTypes)(pOrderNode->m_data.iData1));
			break;

		case ORDER_CONSTRUCT:
		case ORDER_CREATE:
		case ORDER_MAINTAIN:
			break;

		default:
			FAssertMsg(false, "pOrderNode->m_data.eOrderType failed to match a valid option");
			break;
		}
	}

	return false;
}


bool CvCity::isFoodProduction(UnitTypes eUnit) const
{
	if (GC.getUnitInfo(eUnit).isFoodProduction())
	{
		return true;
	}

	if (GET_PLAYER(getOwnerINLINE()).isMilitaryFoodProduction())
	{
		if (GC.getUnitInfo(eUnit).isMilitaryProduction())
		{
			return true;
		}
	}

	return false;
}


int CvCity::getFirstUnitOrder(UnitTypes eUnit) const
{
	int iCount = 0;

	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	while (pOrderNode != NULL)
	{
		if (pOrderNode->m_data.eOrderType == ORDER_TRAIN)
		{
			if (pOrderNode->m_data.iData1 == eUnit)
			{
				return iCount;
			}
		}

		iCount++;

		pOrderNode = nextOrderQueueNode(pOrderNode);
	}

	return -1;
}


int CvCity::getFirstBuildingOrder(BuildingTypes eBuilding) const
{
	int iCount = 0;

	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	while (pOrderNode != NULL)
	{
		if (pOrderNode->m_data.eOrderType == ORDER_CONSTRUCT)
		{
			if (pOrderNode->m_data.iData1 == eBuilding)
			{
				return iCount;
			}
		}

		iCount++;

		pOrderNode = nextOrderQueueNode(pOrderNode);
	}

	return -1;
}


int CvCity::getFirstProjectOrder(ProjectTypes eProject) const
{
	int iCount = 0;

	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	while (pOrderNode != NULL)
	{
		if (pOrderNode->m_data.eOrderType == ORDER_CREATE)
		{
			if (pOrderNode->m_data.iData1 == eProject)
			{
				return iCount;
			}
		}

		iCount++;

		pOrderNode = nextOrderQueueNode(pOrderNode);
	}

	return -1;
}


int CvCity::getNumTrainUnitAI(UnitAITypes eUnitAI) const
{
	int iCount = 0;

	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	while (pOrderNode != NULL)
	{
		if (pOrderNode->m_data.eOrderType == ORDER_TRAIN)
		{
			if (pOrderNode->m_data.iData2 == eUnitAI)
			{
				iCount++;
			}
		}

		pOrderNode = nextOrderQueueNode(pOrderNode);
	}

	return iCount;
}


int CvCity::getProduction() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		switch (pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
			return getUnitProduction((UnitTypes)(pOrderNode->m_data.iData1));
			break;

		case ORDER_CONSTRUCT:
			return getBuildingProduction((BuildingTypes)(pOrderNode->m_data.iData1));
			break;

		case ORDER_CREATE:
			return getProjectProduction((ProjectTypes)(pOrderNode->m_data.iData1));
			break;

		case ORDER_MAINTAIN:
			break;

		default:
			FAssertMsg(false, "pOrderNode->m_data.eOrderType failed to match a valid option");
			break;
		}
	}

	return 0;
}


int CvCity::getProductionNeeded() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		switch (pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
			return getProductionNeeded((UnitTypes)(pOrderNode->m_data.iData1));
			break;

		case ORDER_CONSTRUCT:
			return getProductionNeeded((BuildingTypes)(pOrderNode->m_data.iData1));
			break;

		case ORDER_CREATE:
			return getProductionNeeded((ProjectTypes)(pOrderNode->m_data.iData1));
			break;

		case ORDER_MAINTAIN:
			break;

		default:
			FAssertMsg(false, "pOrderNode->m_data.eOrderType failed to match a valid option");
			break;
		}
	}

	return MAX_INT;
}

int CvCity::getProductionNeeded(UnitTypes eUnit) const
{
	return GET_PLAYER(getOwnerINLINE()).getProductionNeeded(eUnit);
}

int CvCity::getProductionNeeded(BuildingTypes eBuilding) const
{
	int iProductionNeeded = GET_PLAYER(getOwnerINLINE()).getProductionNeeded(eBuilding);

	// Python cost modifier
	if (GC.getUSE_GET_BUILDING_COST_MOD_CALLBACK())
	{
		CyArgsList argsList;
		argsList.add(getOwnerINLINE());	// Player ID
		argsList.add(getID());	// City ID
		argsList.add(eBuilding);	// Building ID
		long lResult=0;
		gDLL->getPythonIFace()->callFunction(PYGameModule, "getBuildingCostMod", argsList.makeFunctionArgs(), &lResult);

		if (lResult > 1)
		{
			iProductionNeeded *= lResult;
			iProductionNeeded /= 100;
		}
	}

	return iProductionNeeded;
}

int CvCity::getProductionNeeded(ProjectTypes eProject) const
{
	return GET_PLAYER(getOwnerINLINE()).getProductionNeeded(eProject);
}

int CvCity::getProductionTurnsLeft() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		switch (pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
			return getProductionTurnsLeft(((UnitTypes)(pOrderNode->m_data.iData1)), 0);
			break;

		case ORDER_CONSTRUCT:
			return getProductionTurnsLeft(((BuildingTypes)(pOrderNode->m_data.iData1)), 0);
			break;

		case ORDER_CREATE:
			return getProductionTurnsLeft(((ProjectTypes)(pOrderNode->m_data.iData1)), 0);
			break;

		case ORDER_MAINTAIN:
			break;

		default:
			FAssertMsg(false, "pOrderNode->m_data.eOrderType failed to match a valid option");
			break;
		}
	}

	return MAX_INT;
}


int CvCity::getProductionTurnsLeft(UnitTypes eUnit, int iNum) const
{
	int iProduction;
	int iFirstUnitOrder;
	int iProductionNeeded;
	int iProductionModifier;

	iProduction = 0;

	iFirstUnitOrder = getFirstUnitOrder(eUnit);

	if ((iFirstUnitOrder == -1) || (iFirstUnitOrder == iNum))
	{
		iProduction += getUnitProduction(eUnit);
	}

	iProductionNeeded = getProductionNeeded(eUnit);
	iProductionModifier = getProductionModifier(eUnit);

	return getProductionTurnsLeft(iProductionNeeded, iProduction, getProductionDifference(iProductionNeeded, iProduction, iProductionModifier, isFoodProduction(eUnit), (iNum == 0)), getProductionDifference(iProductionNeeded, iProduction, iProductionModifier, isFoodProduction(eUnit), false));
}


int CvCity::getProductionTurnsLeft(BuildingTypes eBuilding, int iNum) const
{
	int iProduction;
	int iFirstBuildingOrder;
	int iProductionNeeded;
	int iProductionModifier;

	iProduction = 0;

	iFirstBuildingOrder = getFirstBuildingOrder(eBuilding);

	if ((iFirstBuildingOrder == -1) || (iFirstBuildingOrder == iNum))
	{
		iProduction += getBuildingProduction(eBuilding);
	}

	iProductionNeeded = getProductionNeeded(eBuilding);

	iProductionModifier = getProductionModifier(eBuilding);

	return getProductionTurnsLeft(iProductionNeeded, iProduction, getProductionDifference(iProductionNeeded, iProduction, iProductionModifier, false, (iNum == 0)), getProductionDifference(iProductionNeeded, iProduction, iProductionModifier, false, false));
}


int CvCity::getProductionTurnsLeft(ProjectTypes eProject, int iNum) const
{
	int iProduction;
	int iFirstProjectOrder;
	int iProductionNeeded;
	int iProductionModifier;

	iProduction = 0;

	iFirstProjectOrder = getFirstProjectOrder(eProject);

	if ((iFirstProjectOrder == -1) || (iFirstProjectOrder == iNum))
	{
		iProduction += getProjectProduction(eProject);
	}

	iProductionNeeded = getProductionNeeded(eProject);
	iProductionModifier = getProductionModifier(eProject);

	return getProductionTurnsLeft(iProductionNeeded, iProduction, getProductionDifference(iProductionNeeded, iProduction, iProductionModifier, false, (iNum == 0)), getProductionDifference(iProductionNeeded, iProduction, iProductionModifier, false, false));
}


int CvCity::getProductionTurnsLeft(int iProductionNeeded, int iProduction, int iFirstProductionDifference, int iProductionDifference) const
{
	int iProductionLeft;
	int iTurnsLeft;

	iProductionLeft = std::max(0, (iProductionNeeded - iProduction - iFirstProductionDifference));

	if (iProductionDifference == 0)
	{
		return iProductionLeft + 1;
	}

	iTurnsLeft = (iProductionLeft / iProductionDifference);

	if ((iTurnsLeft * iProductionDifference) < iProductionLeft)
	{
		iTurnsLeft++;
	}

	iTurnsLeft++;

	return std::max(1, iTurnsLeft);
}


void CvCity::setProduction(int iNewValue)
{
	if (isProductionUnit())
	{
		setUnitProduction(getProductionUnit(), iNewValue);
	}
	else if (isProductionBuilding())
	{
		setBuildingProduction(getProductionBuilding(), iNewValue);
	}
	else if (isProductionProject())
	{
		setProjectProduction(getProductionProject(), iNewValue);
	}
}


void CvCity::changeProduction(int iChange)
{
	if (isProductionUnit())
	{
		changeUnitProduction(getProductionUnit(), iChange);
	}
	else if (isProductionBuilding())
	{
		changeBuildingProduction(getProductionBuilding(), iChange);
	}
	else if (isProductionProject())
	{
		changeProjectProduction(getProductionProject(), iChange);
	}
}


int CvCity::getProductionModifier() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		switch (pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
			return getProductionModifier((UnitTypes)(pOrderNode->m_data.iData1));
			break;

		case ORDER_CONSTRUCT:
			return getProductionModifier((BuildingTypes)(pOrderNode->m_data.iData1));
			break;

		case ORDER_CREATE:
			return getProductionModifier((ProjectTypes)(pOrderNode->m_data.iData1));
			break;

		case ORDER_MAINTAIN:
			break;

		default:
			FAssertMsg(false, "pOrderNode->m_data.eOrderType failed to match a valid option");
			break;
		}
	}

	return 0;
}


int CvCity::getProductionModifier(UnitTypes eUnit) const
{
	int iI;

	int iMultiplier = GET_PLAYER(getOwnerINLINE()).getProductionModifier(eUnit);

	iMultiplier += getDomainProductionModifier((DomainTypes)(GC.getUnitInfo(eUnit).getDomainType()));

	if (GC.getUnitInfo(eUnit).isMilitaryProduction())
	{
		iMultiplier += getMilitaryProductionModifier();
	}

	for (iI = 0; iI < GC.getNumBonusInfos(); iI++)
	{
		if (hasBonus((BonusTypes)iI))
		{
			iMultiplier += GC.getUnitInfo(eUnit).getBonusProductionModifier(iI);
		}
	}

	if (GET_PLAYER(getOwnerINLINE()).getStateReligion() != NO_RELIGION)
	{
		if (isHasReligion(GET_PLAYER(getOwnerINLINE()).getStateReligion()))
		{
			iMultiplier += GET_PLAYER(getOwnerINLINE()).getStateReligionUnitProductionModifier();
		}
	}

	// Leoreth: Statue of Zeus effect: +25% military production speed in cities with pagan temples
	if (GET_PLAYER(getOwnerINLINE()).isHasBuilding((BuildingTypes)STATUE_OF_ZEUS) && !GET_TEAM((TeamTypes)getOwnerINLINE()).isHasTech((TechTypes)THEOLOGY))
	{
		if (isHasRealBuilding(getUniqueBuilding(getCivilizationType(), (BuildingTypes)PAGAN_TEMPLE)))
		{
			iMultiplier += 25;
		}
	}

	return std::max(0, iMultiplier);
}


int CvCity::getProductionModifier(BuildingTypes eBuilding) const
{
	int iMultiplier = GET_PLAYER(getOwnerINLINE()).getProductionModifier(eBuilding);

	for (int iI = 0; iI < GC.getNumBonusInfos(); iI++)
	{
		if (hasBonus((BonusTypes)iI))
		{
			iMultiplier += GC.getBuildingInfo(eBuilding).getBonusProductionModifier(iI);
		}
	}

	if (GET_PLAYER(getOwnerINLINE()).getStateReligion() != NO_RELIGION)
	{
		if (isHasReligion(GET_PLAYER(getOwnerINLINE()).getStateReligion()))
		{
			iMultiplier += GET_PLAYER(getOwnerINLINE()).getStateReligionBuildingProductionModifier();
		}
	}

	// Leoreth: new Roman UP
	if (getOwnerINLINE() == ROME)
	{
		if (GET_PLAYER(getOwnerINLINE()).getCapitalCity()->isHasRealBuilding(eBuilding))
		{
			iMultiplier += 30;
		}
	}

	// Leoreth: Holy Roman UP: +100% production of state religion buildings
	if (getOwnerINLINE() == HOLY_ROME)
	{
		if (GC.getBuildingInfo(eBuilding).getPrereqReligion() != NO_RELIGION && GC.getBuildingClassInfo((BuildingClassTypes)GC.getBuildingInfo(eBuilding).getBuildingClassType()).getMaxGlobalInstances() != 1)
		{
			if (GC.getBuildingInfo(eBuilding).getPrereqReligion() == GET_PLAYER(getOwnerINLINE()).getStateReligion())
			{
				iMultiplier += 100;
			}
		}
	}

	return std::max(0, iMultiplier);
}


int CvCity::getProductionModifier(ProjectTypes eProject) const
{
	int iMultiplier = GET_PLAYER(getOwnerINLINE()).getProductionModifier(eProject);

	if (GC.getProjectInfo(eProject).isSpaceship())
	{
		iMultiplier += getSpaceProductionModifier();
	}

	for (int iI = 0; iI < GC.getNumBonusInfos(); iI++)
	{
		if (hasBonus((BonusTypes)iI))
		{
			iMultiplier += GC.getProjectInfo(eProject).getBonusProductionModifier(iI);
		}
	}

	return std::max(0, iMultiplier);
}


int CvCity::getProductionDifference(int iProductionNeeded, int iProduction, int iProductionModifier, bool bFoodProduction, bool bOverflow) const
{
	if (isDisorder())
	{
		return 0;
	}

	int iFoodProduction = ((bFoodProduction) ? std::max(0, (getYieldRate(YIELD_FOOD) - foodConsumption(true))) : 0);

	int iOverflow = ((bOverflow) ? (getOverflowProduction() + getFeatureProduction()) : 0);

	return (((getBaseYieldRate(YIELD_PRODUCTION) + iOverflow) * getBaseYieldRateModifier(YIELD_PRODUCTION, iProductionModifier)) / 100 + iFoodProduction);

}


int CvCity::getCurrentProductionDifference(bool bIgnoreFood, bool bOverflow) const
{
	return getProductionDifference(getProductionNeeded(), getProduction(), getProductionModifier(), (!bIgnoreFood && isFoodProduction()), bOverflow);
}


int CvCity::getExtraProductionDifference(int iExtra) const
{
	return getExtraProductionDifference(iExtra, getProductionModifier());
}

int CvCity::getExtraProductionDifference(int iExtra, UnitTypes eUnit) const
{
	return getExtraProductionDifference(iExtra, getProductionModifier(eUnit));
}

int CvCity::getExtraProductionDifference(int iExtra, BuildingTypes eBuilding) const
{
	return getExtraProductionDifference(iExtra, getProductionModifier(eBuilding));
}

int CvCity::getExtraProductionDifference(int iExtra, ProjectTypes eProject) const
{
	return getExtraProductionDifference(iExtra, getProductionModifier(eProject));
}

int CvCity::getExtraProductionDifference(int iExtra, int iModifier) const
{
	return ((iExtra * getBaseYieldRateModifier(YIELD_PRODUCTION, iModifier)) / 100);
}


bool CvCity::canHurry(HurryTypes eHurry, bool bTestVisible) const
{
	if (!(GET_PLAYER(getOwnerINLINE()).canHurry(eHurry)))
	{
		return false;
	}

	if (isDisorder())
	{
		return false;
	}

	if (getProduction() >= getProductionNeeded())
	{
		return false;
	}

	if (!bTestVisible)
	{
		if (!isProductionUnit() && !isProductionBuilding())
		{
			return false;
		}

		// Leoreth: hurry gold now split into buildings and units
		if (isProductionUnit() && !GC.getHurryInfo(eHurry).isUnits())
		{
			return false;
		}

		if (isProductionBuilding() && !GC.getHurryInfo(eHurry).isBuildings())
		{
			return false;
		}

		// non-military units cannot be hurried
		if (isProductionUnit() && !GC.getUnitInfo(getProductionUnit()).isMilitaryProduction() && hurryGold(eHurry) > 0)
		{
			return false;
		}

		if (GET_PLAYER(getOwnerINLINE()).getGold() < hurryGold(eHurry))
		{
			return false;
		}

		if (maxHurryPopulation() < hurryPopulation(eHurry))
		{
			return false;
		}
	}

	return true;
}

bool CvCity::canHurryUnit(HurryTypes eHurry, UnitTypes eUnit, bool bIgnoreNew) const
{
	if (!(GET_PLAYER(getOwnerINLINE()).canHurry(eHurry)))
	{
		return false;
	}

	if (isDisorder())
	{
		return false;
	}

	if (!GC.getHurryInfo(eHurry).isUnits())
	{
		return false;
	}

	if (getUnitProduction(eUnit) >= getProductionNeeded(eUnit))
	{
		return false;
	}

	if (GET_PLAYER(getOwnerINLINE()).getGold() < getHurryGold(eHurry, getHurryCost(false, eUnit, bIgnoreNew)))
	{
		return false;
	}

	if (maxHurryPopulation() < getHurryPopulation(eHurry, getHurryCost(true, eUnit, bIgnoreNew)))
	{
		return false;
	}

	return true;
}

bool CvCity::canHurryBuilding(HurryTypes eHurry, BuildingTypes eBuilding, bool bIgnoreNew) const
{
	if (!(GET_PLAYER(getOwnerINLINE()).canHurry(eHurry)))
	{
		return false;
	}

	if (isDisorder())
	{
		return false;
	}

	if (!GC.getHurryInfo(eHurry).isBuildings())
	{
		return false;
	}

	if (getBuildingProduction(eBuilding) >= getProductionNeeded(eBuilding))
	{
		return false;
	}

	if (GET_PLAYER(getOwnerINLINE()).getGold() < getHurryGold(eHurry, getHurryCost(false, eBuilding, bIgnoreNew)))
	{
		return false;
	}

	if (maxHurryPopulation() < getHurryPopulation(eHurry, getHurryCost(true, eBuilding, bIgnoreNew)))
	{
		return false;
	}

	return true;
}


void CvCity::hurry(HurryTypes eHurry)
{
	int iHurryGold;
	int iHurryPopulation;
	int iHurryAngerLength;
	int iHurryAngerModifier;

	if (!canHurry(eHurry))
	{
		return;
	}

	iHurryGold = hurryGold(eHurry);
	iHurryPopulation = hurryPopulation(eHurry);
	iHurryAngerLength = hurryAngerLength(eHurry);

	changeProduction(hurryProduction(eHurry));

	// Leoreth: remember if a unit is being hurried to apply the mercenary promotion, includes Phoenician UP
	if (isProductionUnit() && iHurryGold > 0 && getOwnerINLINE() != PHOENICIA)
	{
		setUnitHurried(getProductionUnit(), true);
	}

	GET_PLAYER(getOwnerINLINE()).changeGold(-(iHurryGold));
	changePopulation(-(iHurryPopulation));

	// Leoreth: amount of sacrificed population increases hurry anger
	iHurryAngerModifier = (iHurryPopulation + 1) / 2;

	// Leoreth: Pyramids negate unhappiness scaling
	if (GET_PLAYER(getOwnerINLINE()).isHasBuildingEffect((BuildingTypes)PYRAMIDS))
		iHurryAngerModifier = 1;

	changeHurryAngerTimer(iHurryAngerLength * iHurryAngerModifier);

	if ((getOwnerINLINE() == GC.getGameINLINE().getActivePlayer()) && isCitySelected())
	{
		gDLL->getInterfaceIFace()->setDirty(SelectionButtons_DIRTY_BIT, true);
	}

	// Python Event
	CvEventReporter::getInstance().cityHurry(this, eHurry);
}

// BUG - Hurry Assist - start
bool CvCity::hurryOverflow(HurryTypes eHurry, int* iProduction, int* iGold, bool bCountThisTurn) const
{
	if (!canHurry(eHurry))
	{
		return false;
	}

	if (GC.getHurryInfo(eHurry).getProductionPerPopulation() == 0)
	{
		*iProduction = 0;
		*iGold = 0;
		return true;
	}

	int iTotal, iCurrent, iModifier, iGoldPercent;

	if (isProductionUnit())
	{
		UnitTypes eUnit = getProductionUnit();
		FAssertMsg(eUnit != NO_UNIT, "eUnit is expected to be assigned a valid unit type");
		iTotal = getProductionNeeded(eUnit);
		iCurrent = getUnitProduction(eUnit);
		iModifier = getProductionModifier(eUnit);
		iGoldPercent = GC.getDefineINT("MAXED_UNIT_GOLD_PERCENT");
	}
	else if (isProductionBuilding())
	{
		BuildingTypes eBuilding = getProductionBuilding();
		FAssertMsg(eBuilding != NO_BUILDING, "eBuilding is expected to be assigned a valid building type");
		iTotal = getProductionNeeded(eBuilding);
		iCurrent = getBuildingProduction(eBuilding);
		iModifier = getProductionModifier(eBuilding);
		iGoldPercent = GC.getDefineINT("MAXED_BUILDING_GOLD_PERCENT");
	}
	else if (isProductionProject())
	{
		ProjectTypes eProject = getProductionProject();
		FAssertMsg(eProject != NO_PROJECT, "eProject is expected to be assigned a valid project type");
		iTotal = getProductionNeeded(eProject);
		iCurrent = getProjectProduction(eProject);
		iModifier = getProductionModifier(eProject);
		iGoldPercent = GC.getDefineINT("MAXED_PROJECT_GOLD_PERCENT");
	}
	else
	{
		return false;
	}

	int iHurry = hurryProduction(eHurry);
	int iOverflow = iCurrent + iHurry - iTotal;
	if (bCountThisTurn)
	{
		// include chops and previous overflow here
		iOverflow += getCurrentProductionDifference(false, true);
	}
	int iMaxOverflow = std::max(iTotal, getCurrentProductionDifference(false, false));
	int iLostProduction = std::max(0, iOverflow - iMaxOverflow);
	int iBaseModifier = getBaseYieldRateModifier(YIELD_PRODUCTION);
	int iTotalModifier = getBaseYieldRateModifier(YIELD_PRODUCTION, iModifier);

	iOverflow = std::min(iOverflow, iMaxOverflow);
	iLostProduction *= iBaseModifier;
	iLostProduction /= std::max(1, iTotalModifier);

	*iProduction = (iBaseModifier * iOverflow) / std::max(1, iTotalModifier);
	*iGold = ((iLostProduction * iGoldPercent) / 100);

	return true;
}
// BUG - Hurry Assist - end


UnitTypes CvCity::getConscriptUnit() const
{
	UnitTypes eLoopUnit;
	UnitTypes eBestUnit;
	int iValue;
	int iBestValue;
	int iI;

	long lConscriptUnit;

	iBestValue = 0;
	eBestUnit = NO_UNIT;

	for (iI = 0; iI < GC.getNumUnitClassInfos(); iI++)
	{
		eLoopUnit = (UnitTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(iI);

		if (eLoopUnit != NO_UNIT)
		{
			if (canTrain(eLoopUnit))
			{
				iValue = GC.getUnitInfo(eLoopUnit).getConscriptionValue();

				if (iValue > iBestValue)
				{
					iBestValue = iValue;
					eBestUnit = eLoopUnit;
				}
			}
		}
	}

	// Allow the player to determine the conscripted unit type
	CyArgsList argsList;
	argsList.add(getOwnerINLINE());	// pass in player
	lConscriptUnit = -1;
/*************************************************************************************************/
/**	SPEEDTWEAK (Block Python) Sephi                                               	            **/
/**	If you want to allow modmodders to enable this Callback, see CvCity::cancreate for example  **/
/*************************************************************************************************/
/**
	gDLL->getPythonIFace()->callFunction(PYGameModule, "getConscriptUnitType", argsList.makeFunctionArgs(),&lConscriptUnit);
/*************************************************************************************************/
/**	END	                                        												**/
/*************************************************************************************************/

	if (lConscriptUnit != -1)
	{
		eBestUnit = ((UnitTypes)lConscriptUnit);
	}

	//Leoreth: enslavement
	if (canEnslave(true))
	{
		eBestUnit = (UnitTypes)GC.getCivilizationInfo(GET_PLAYER(getOwnerINLINE()).getCivilizationType()).getCivilizationUnits(GC.getInfoTypeForString("UNITCLASS_SLAVE"));
	}

	return eBestUnit;
}


int CvCity::getConscriptPopulation() const
{
	UnitTypes eConscriptUnit;

	eConscriptUnit = getConscriptUnit();

	if (eConscriptUnit == NO_UNIT)
	{
		return 0;
	}

	if (GC.getDefineINT("CONSCRIPT_POPULATION_PER_COST") == 0)
	{
		return 0;
	}

	return std::max(1, ((GC.getUnitInfo(eConscriptUnit).getProductionCost()) / GC.getDefineINT("CONSCRIPT_POPULATION_PER_COST")));
}


int CvCity::conscriptMinCityPopulation() const
{
	int iPopulation;

	iPopulation = GC.getDefineINT("CONSCRIPT_MIN_CITY_POPULATION");

	iPopulation += getConscriptPopulation();

	return iPopulation;
}


int CvCity::flatConscriptAngerLength() const
{
	int iAnger;

	iAnger = GC.getDefineINT("CONSCRIPT_ANGER_DIVISOR");

	iAnger *= GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getHurryConscriptAngerPercent();
	iAnger /= 100;

	return std::max(1, iAnger);
}


bool CvCity::canConscript() const
{
	if (isDisorder())
	{
		return false;
	}

	if (isDrafted())
	{
		return false;
	}

	if (GET_PLAYER(getOwnerINLINE()).getConscriptCount() >= GET_PLAYER(getOwnerINLINE()).getMaxConscript())
	{
		return false;
	}

	// Turkish UP: extra conscript requires non-state religion
	if (getOwnerINLINE() == TURKEY && GET_PLAYER(getOwnerINLINE()).getConscriptCount() - GET_PLAYER(getOwnerINLINE()).getMaxConscript() >= -2)
	{
		if (!GET_PLAYER(getOwnerINLINE()).isStateReligion())
		{
			if (getReligionCount() == 0)
			{
				return false;
			}
		}
		else
		{
			if ((isHasReligion(GET_PLAYER(getOwnerINLINE()).getStateReligion()) && getReligionCount() == 1) || getReligionCount() == 0)
			{
				return false;
			}
		}
	}

	if (getPopulation() <= getConscriptPopulation())
	{
		return false;
	}

	if (getPopulation() < conscriptMinCityPopulation())
	{
		return false;
	}

	if (plot()->calculateTeamCulturePercent(getTeam()) < GC.getDefineINT("CONSCRIPT_MIN_CULTURE_PERCENT"))
	{
		return false;
	}

	if (getConscriptUnit() == NO_UNIT)
	{
		return false;
	}

	return true;
}

CvUnit* CvCity::initConscriptedUnit()
{
	UnitAITypes eCityAI = NO_UNITAI;

	UnitTypes eConscriptUnit = getConscriptUnit();

	if (NO_UNIT == eConscriptUnit)
	{
		return NULL;
	}

	if (GET_PLAYER(getOwnerINLINE()).AI_unitValue(eConscriptUnit, UNITAI_ATTACK, area()) > 0)
	{
		eCityAI = UNITAI_ATTACK;
	}
	else if (GET_PLAYER(getOwnerINLINE()).AI_unitValue(eConscriptUnit, UNITAI_CITY_DEFENSE, area()) > 0)
	{
		eCityAI = UNITAI_CITY_DEFENSE;
	}
	else if (GET_PLAYER(getOwnerINLINE()).AI_unitValue(eConscriptUnit, UNITAI_CITY_COUNTER, area()) > 0)
	{
		eCityAI = UNITAI_CITY_COUNTER;
	}
	else if (GET_PLAYER(getOwnerINLINE()).AI_unitValue(eConscriptUnit, UNITAI_CITY_SPECIAL, area()) > 0)
	{
		eCityAI = UNITAI_CITY_SPECIAL;
	}
	else
	{
		eCityAI = NO_UNITAI;
	}

	CvUnit* pUnit = GET_PLAYER(getOwnerINLINE()).initUnit(eConscriptUnit, getX_INLINE(), getY_INLINE(), eCityAI);
	FAssertMsg(pUnit != NULL, "pUnit expected to be assigned (not NULL)");

	if (NULL != pUnit)
	{
		addProductionExperience(pUnit, true);

		pUnit->setMoves(0);
	}

	return pUnit;
}


void CvCity::conscript()
{
	if (!canConscript() && !canEnslave())
	{
		return;
	}
	
	CvUnit* pUnit = initConscriptedUnit();
	FAssertMsg(pUnit != NULL, "pUnit expected to be assigned (not NULL)");

	changePopulation(-(getConscriptPopulation()));
	changeConscriptAngerTimer(flatConscriptAngerLength());

	setDrafted(true);

	GET_PLAYER(getOwnerINLINE()).changeConscriptCount(1);

	if (NULL != pUnit)
	{
		if (GC.getGameINLINE().getActivePlayer() == getOwnerINLINE())
		{
			gDLL->getInterfaceIFace()->selectUnit(pUnit, true, false, true);
		}
	}
}




int CvCity::getBonusHealth(BonusTypes eBonus) const
{
	int iHealth;
	int iI;

	iHealth = GC.getBonusInfo(eBonus).getHealth();

	for (iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		iHealth += getNumActiveBuilding((BuildingTypes)iI) * GC.getBuildingInfo((BuildingTypes) iI).getBonusHealthChanges(eBonus);
	}

	return iHealth;
}


int CvCity::getBonusHappiness(BonusTypes eBonus) const
{
	int iHappiness;
	int iI;

	iHappiness = GC.getBonusInfo(eBonus).getHappiness();

	for (iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		iHappiness += getNumActiveBuilding((BuildingTypes)iI) * GC.getBuildingInfo((BuildingTypes) iI).getBonusHappinessChanges(eBonus);
	}

	return iHappiness;
}


int CvCity::getBonusPower(BonusTypes eBonus, bool bDirty) const
{
	int iCount;
	int iI;

	iCount = 0;

	for (iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		if (getNumActiveBuilding((BuildingTypes)iI) > 0)
		{
			if (GC.getBuildingInfo((BuildingTypes) iI).getPowerBonus() == eBonus)
			{
				if (GC.getBuildingInfo((BuildingTypes) iI).isDirtyPower() == bDirty)
				{
					iCount += getNumActiveBuilding((BuildingTypes)iI);
				}
			}
		}
	}

	return iCount;
}


int CvCity::getBonusYieldRateModifier(YieldTypes eIndex, BonusTypes eBonus) const
{
	int iModifier;
	int iI;

	iModifier = 0;

	for (iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		iModifier += getNumActiveBuilding((BuildingTypes)iI) * GC.getBuildingInfo((BuildingTypes) iI).getBonusYieldModifier(eBonus, eIndex);
	}

	return iModifier;
}

// Leoreth
int CvCity::getBonusCommerceRateModifier(CommerceTypes eIndex, BonusTypes eBonus) const
{
	int iModifier;
	int iI;

	iModifier = 0;

	for (iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		iModifier += getNumActiveBuilding((BuildingTypes)iI) * GC.getBuildingInfo((BuildingTypes)iI).getBonusCommerceModifier(eBonus, eIndex);
	}

	return iModifier;
}


void CvCity::processBonus(BonusTypes eBonus, int iChange)
{
	int iI;
	int iValue;
	int iGoodValue;
	int iBadValue;

	iValue = GC.getBonusInfo(eBonus).getHealth();
	iGoodValue = std::max(0, iValue);
	iBadValue = std::min(0, iValue);

	for (iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		iValue = GC.getBuildingInfo((BuildingTypes) iI).getBonusHealthChanges(eBonus) * getNumActiveBuilding((BuildingTypes)iI);

		if (iValue >= 0)
		{
			iGoodValue += iValue;
		}
		else
		{
			iBadValue += iValue;
		}
	}

	changeBonusGoodHealth(iGoodValue * iChange);
	changeBonusBadHealth(iBadValue * iChange);


	iValue = GC.getBonusInfo(eBonus).getHappiness();
	iGoodValue = std::max(0, iValue);
	iBadValue = std::min(0, iValue);

	for (iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		iValue = getNumActiveBuilding((BuildingTypes)iI) * GC.getBuildingInfo((BuildingTypes) iI).getBonusHappinessChanges(eBonus);

		if (iValue >= 0)
		{
			iGoodValue += iValue;
		}
		else
		{
			iBadValue += iValue;
		}
	}

	changeBonusGoodHappiness(iGoodValue * iChange);
	changeBonusBadHappiness(iBadValue * iChange);

	changePowerCount((getBonusPower(eBonus, true) * iChange), true);
	changePowerCount((getBonusPower(eBonus, false) * iChange), false);

	for (iI = 0; iI < NUM_YIELD_TYPES; iI++)
	{
		changeBonusYieldRateModifier(((YieldTypes)iI), (getBonusYieldRateModifier(((YieldTypes)iI), eBonus) * iChange));
	}

	for (iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
	{
		changeBonusCommerceRateModifier(((CommerceTypes)iI), (getBonusCommerceRateModifier(((CommerceTypes)iI), eBonus) * iChange));
	}
}


void CvCity::processBuilding(BuildingTypes eBuilding, int iChange, bool bObsolete)
{
	UnitTypes eGreatPeopleUnit;
	int iI, iJ;

	if (!(GET_TEAM(getTeam()).isObsoleteBuilding(eBuilding)) || bObsolete)
	{
		if (iChange > 0)
		{
			CorporationTypes eCorporation = (CorporationTypes)GC.getBuildingInfo(eBuilding).getFoundsCorporation();
			if (NO_CORPORATION != eCorporation && !GC.getGameINLINE().isCorporationFounded(eCorporation))
			{
				setHeadquarters(eCorporation);
			}
		}

		if (GC.getBuildingInfo(eBuilding).getNoBonus() != NO_BONUS)
		{
			changeNoBonusCount(((BonusTypes)(GC.getBuildingInfo(eBuilding).getNoBonus())), iChange);
		}

		if (GC.getBuildingInfo(eBuilding).getFreeBonus() != NO_BONUS)
		{
			changeFreeBonus(((BonusTypes)(GC.getBuildingInfo(eBuilding).getFreeBonus())), (GC.getGameINLINE().getNumFreeBonuses(eBuilding) * iChange));
		}

		if (GC.getBuildingInfo(eBuilding).getFreePromotion() != NO_PROMOTION)
		{
			changeFreePromotionCount(((PromotionTypes)(GC.getBuildingInfo(eBuilding).getFreePromotion())), iChange);
		}

		changeEspionageDefenseModifier(GC.getBuildingInfo(eBuilding).getEspionageDefenseModifier() * iChange);
		changeGreatPeopleRateModifier(GC.getBuildingInfo(eBuilding).getGreatPeopleRateModifier() * iChange);
		changeFreeExperience(GC.getBuildingInfo(eBuilding).getFreeExperience() * iChange);
		changeMaxFoodKeptPercent(GC.getBuildingInfo(eBuilding).getFoodKept() * iChange);
		changeMaxAirlift(GC.getBuildingInfo(eBuilding).getAirlift() * iChange);
		changeAirModifier(GC.getBuildingInfo(eBuilding).getAirModifier() * iChange);
		changeAirUnitCapacity(GC.getBuildingInfo(eBuilding).getAirUnitCapacity() * iChange);
		changeNukeModifier(GC.getBuildingInfo(eBuilding).getNukeModifier() * iChange);
		changeFreeSpecialist(GC.getBuildingInfo(eBuilding).getFreeSpecialist() * iChange);
		changeMaintenanceModifier(GC.getBuildingInfo(eBuilding).getMaintenanceModifier() * iChange);
		changeWarWearinessModifier(GC.getBuildingInfo(eBuilding).getWarWearinessModifier() * iChange);
		changeHurryAngerModifier(GC.getBuildingInfo(eBuilding).getHurryAngerModifier() * iChange);
		changeHealRate(GC.getBuildingInfo(eBuilding).getHealRateChange() * iChange);
		if (GC.getBuildingInfo(eBuilding).getHealth() > 0)
		{
			changeBuildingGoodHealth(GC.getBuildingInfo(eBuilding).getHealth() * iChange);
		}
		else
		{
			changeBuildingBadHealth(GC.getBuildingInfo(eBuilding).getHealth() * iChange);
		}
		if (GC.getBuildingInfo(eBuilding).getHappiness() > 0)
		{
			changeBuildingGoodHappiness(GC.getBuildingInfo(eBuilding).getHappiness() * iChange);
		}
		else
		{
			changeBuildingBadHappiness(GC.getBuildingInfo(eBuilding).getHappiness() * iChange);
		}
		if (GC.getBuildingInfo(eBuilding).getReligionType() != NO_RELIGION)
		{
			changeStateReligionHappiness(((ReligionTypes)(GC.getBuildingInfo(eBuilding).getReligionType())), (GC.getBuildingInfo(eBuilding).getStateReligionHappiness() * iChange));
		}
		changeMilitaryProductionModifier(GC.getBuildingInfo(eBuilding).getMilitaryProductionModifier() * iChange);
		changeSpaceProductionModifier(GC.getBuildingInfo(eBuilding).getSpaceProductionModifier() * iChange);
		changeExtraTradeRoutes(GC.getBuildingInfo(eBuilding).getTradeRoutes() * iChange);
		changeTradeRouteModifier(GC.getBuildingInfo(eBuilding).getTradeRouteModifier() * iChange);
		changeForeignTradeRouteModifier(GC.getBuildingInfo(eBuilding).getForeignTradeRouteModifier() * iChange);
		changePowerCount(((GC.getBuildingInfo(eBuilding).isPower()) ? iChange : 0), GC.getBuildingInfo(eBuilding).isDirtyPower());
		changeGovernmentCenterCount((GC.getBuildingInfo(eBuilding).isGovernmentCenter()) ? iChange : 0);
		changeNoUnhappinessCount((GC.getBuildingInfo(eBuilding).isNoUnhappiness()) ? iChange : 0);
		changeNoUnhealthyPopulationCount((GC.getBuildingInfo(eBuilding).isNoUnhealthyPopulation()) ? iChange : 0);
		changeBuildingOnlyHealthyCount((GC.getBuildingInfo(eBuilding).isBuildingOnlyHealthy()) ? iChange : 0);

		for (iI = 0; iI < NUM_YIELD_TYPES; iI++)
		{
			changeSeaPlotYield(((YieldTypes)iI), (GC.getBuildingInfo(eBuilding).getSeaPlotYieldChange(iI) * iChange));
			changeRiverPlotYield(((YieldTypes)iI), (GC.getBuildingInfo(eBuilding).getRiverPlotYieldChange(iI) * iChange));
			changeBaseYieldRate(((YieldTypes)iI), ((GC.getBuildingInfo(eBuilding).getYieldChange(iI) + getBuildingYieldChange((BuildingClassTypes)GC.getBuildingInfo(eBuilding).getBuildingClassType(), (YieldTypes)iI))* iChange));
			// Leoreth: catch the overflow bug
			if (getBaseYieldRate((YieldTypes)iI) < 0 || getBaseYieldRate((YieldTypes)iI) > 1000) {
				GC.getGame().logMsg("Overflow in (%d, %d) for processBuilding", getX(), getY());
				gDLL->getInterfaceIFace()->addMessage(GC.getGame().getActivePlayer(), true, GC.getEVENT_MESSAGE_TIME(), gDLL->getText("TXT_KEY_OVERFLOW", getX(), getY(), "processBuilding()"), "", MESSAGE_TYPE_MAJOR_EVENT, ARTFILEMGR.getInterfaceArtInfo("WORLDBUILDER_CITY_EDIT")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_RED"), getX_INLINE(), getY_INLINE(), true, true);
				GC.getGame().setAIAutoPlay(0);
				GC.getGame().setAIAutoPlayCatapult(0);
				gDLL->getEngineIFace()->AutoSave(true);
			}
			changeYieldRateModifier(((YieldTypes)iI), (GC.getBuildingInfo(eBuilding).getYieldModifier(iI) * iChange));
			changePowerYieldRateModifier(((YieldTypes)iI), (GC.getBuildingInfo(eBuilding).getPowerYieldModifier(iI) * iChange));
		}

		for (iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
		{
			changeCommerceRateModifier(((CommerceTypes)iI), (GC.getBuildingInfo(eBuilding).getCommerceModifier(iI) * iChange));
			changeCommerceHappinessPer(((CommerceTypes)iI), (GC.getBuildingInfo(eBuilding).getCommerceHappiness(iI) * iChange));
		}

		for (iI = 0; iI < GC.getNumReligionInfos(); iI++)
		{
			changeReligionInfluence(((ReligionTypes)iI), (GC.getBuildingInfo(eBuilding).getReligionChange(iI) * iChange));
		}

		for (iI = 0; iI < GC.getNumSpecialistInfos(); iI++)
		{
			changeMaxSpecialistCount(((SpecialistTypes)iI), GC.getBuildingInfo(eBuilding).getSpecialistCount(iI) * iChange);
			changeFreeSpecialistCount(((SpecialistTypes)iI), GC.getBuildingInfo(eBuilding).getFreeSpecialistCount(iI) * iChange);
		}

		for (iI = 0; iI < GC.getNumImprovementInfos(); ++iI)
		{
			changeImprovementFreeSpecialists((ImprovementTypes)iI, GC.getBuildingInfo(eBuilding).getImprovementFreeSpecialist(iI) * iChange);
		}

		FAssertMsg((0 < GC.getNumBonusInfos()) && "GC.getNumBonusInfos() is not greater than zero but an array is being allocated in CvPlotGroup::reset", "GC.getNumBonusInfos() is not greater than zero but an array is being allocated in CvPlotGroup::reset");
		for (iI = 0; iI < GC.getNumBonusInfos(); iI++)
		{
			if (hasBonus((BonusTypes)iI))
			{
				if (GC.getBuildingInfo(eBuilding).getBonusHealthChanges(iI) > 0)
				{
					changeBonusGoodHealth(GC.getBuildingInfo(eBuilding).getBonusHealthChanges(iI) * iChange);
				}
				else
				{
					changeBonusBadHealth(GC.getBuildingInfo(eBuilding).getBonusHealthChanges(iI) * iChange);
				}
				if (GC.getBuildingInfo(eBuilding).getBonusHappinessChanges(iI) > 0)
				{
					changeBonusGoodHappiness(GC.getBuildingInfo(eBuilding).getBonusHappinessChanges(iI) * iChange);
				}
				else
				{
					changeBonusBadHappiness(GC.getBuildingInfo(eBuilding).getBonusHappinessChanges(iI) * iChange);
				}

				if (GC.getBuildingInfo(eBuilding).getPowerBonus() == iI)
				{
					changePowerCount(iChange, GC.getBuildingInfo(eBuilding).isDirtyPower());
				}

				for (iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
				{
					changeBonusYieldRateModifier(((YieldTypes)iJ), (GC.getBuildingInfo(eBuilding).getBonusYieldModifier(iI, iJ) * iChange));
				}

				// Leoreth
				for (iJ = 0; iJ < NUM_COMMERCE_TYPES; iJ++)
				{
					changeBonusCommerceRateModifier(((CommerceTypes)iJ), (GC.getBuildingInfo(eBuilding).getBonusCommerceModifier(iI, iJ) * iChange));
				}
			}
		}

		for (iI = 0; iI < GC.getNumUnitCombatInfos(); iI++)
		{
			changeUnitCombatFreeExperience(((UnitCombatTypes)iI), GC.getBuildingInfo(eBuilding).getUnitCombatFreeExperience(iI) * iChange);
		}

		for (iI = 0; iI < NUM_DOMAIN_TYPES; iI++)
		{
			changeDomainFreeExperience(((DomainTypes)iI), GC.getBuildingInfo(eBuilding).getDomainFreeExperience(iI) * iChange);
			changeDomainProductionModifier(((DomainTypes)iI), GC.getBuildingInfo(eBuilding).getDomainProductionModifier(iI) * iChange);
		}

		// Leoreth
		for (iI = 0; iI < GC.getNumBonusInfos(); iI++)
		{
			for (iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
			{
				changeBonusYield((BonusTypes)iI, (YieldTypes)iJ, GC.getBuildingInfo(eBuilding).getBonusYieldChange(iI, iJ) * iChange);
			}
		}

		updateExtraBuildingHappiness();
		updateExtraBuildingHealth();

		GET_PLAYER(getOwnerINLINE()).changeAssets(GC.getBuildingInfo(eBuilding).getAssetValue() * iChange);

		area()->changePower(getOwnerINLINE(), (GC.getBuildingInfo(eBuilding).getPowerValue() * iChange));
		GET_PLAYER(getOwnerINLINE()).changePower(GC.getBuildingInfo(eBuilding).getPowerValue() * iChange);

		for (iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).getTeam() == getTeam())
			{
				if (GC.getBuildingInfo(eBuilding).isTeamShare() || (iI == getOwnerINLINE()))
				{
					GET_PLAYER((PlayerTypes)iI).processBuilding(eBuilding, iChange, area());
				}
			}
		}

		GET_TEAM(getTeam()).processBuilding(eBuilding, iChange);

		GC.getGameINLINE().processBuilding(eBuilding, iChange);
	}

	if (!bObsolete)
	{
		changeBuildingDefense(GC.getBuildingInfo(eBuilding).getDefenseModifier() * iChange);
		changeBuildingBombardDefense(GC.getBuildingInfo(eBuilding).getBombardDefenseModifier() * iChange);

		// Leoreth: Himeji Castle effect: defense modifiers affect culture
		if (GET_PLAYER(getOwner()).isHasBuildingEffect((BuildingTypes)HIMEJI_CASTLE))
		{
			changeCommerceRateModifier(COMMERCE_CULTURE, GC.getBuildingInfo(eBuilding).getDefenseModifier() * iChange);
		}

		changeBaseGreatPeopleRate(GC.getBuildingInfo(eBuilding).getGreatPeopleRateChange() * iChange);

		if (GC.getBuildingInfo(eBuilding).getGreatPeopleUnitClass() != NO_UNITCLASS)
		{
			eGreatPeopleUnit = ((UnitTypes)(GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(GC.getBuildingInfo(eBuilding).getGreatPeopleUnitClass())));

			if (eGreatPeopleUnit != NO_UNIT)
			{
				changeGreatPeopleUnitRate(eGreatPeopleUnit, GC.getBuildingInfo(eBuilding).getGreatPeopleRateChange() * iChange);
			}
		}

		GET_TEAM(getTeam()).changeBuildingClassCount((BuildingClassTypes)GC.getBuildingInfo(eBuilding).getBuildingClassType(), iChange);
		GET_PLAYER(getOwnerINLINE()).changeBuildingClassCount((BuildingClassTypes)GC.getBuildingInfo(eBuilding).getBuildingClassType(), iChange);

		GET_PLAYER(getOwnerINLINE()).changeWondersScore(getWonderScore((BuildingClassTypes)(GC.getBuildingInfo(eBuilding).getBuildingClassType())) * iChange);
	}

	updateBuildingCommerce();

	setLayoutDirty(true);
}


void CvCity::processProcess(ProcessTypes eProcess, int iChange)
{
	int iI;

	for (iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
	{
		//Leoreth: process efficiency modifier inside (civic)
		changeProductionToCommerceModifier(((CommerceTypes)iI), ((GC.getProcessInfo(eProcess).getProductionToCommerceModifier(iI) * (100 + GET_PLAYER(getOwner()).getProcessModifier()) / 100 * iChange)));
	}
}


void CvCity::processSpecialist(SpecialistTypes eSpecialist, int iChange)
{
	UnitTypes eGreatPeopleUnit;
	int iI;

	if (GC.getSpecialistInfo(eSpecialist).getGreatPeopleUnitClass() != NO_UNITCLASS)
	{
		eGreatPeopleUnit = ((UnitTypes)(GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(GC.getSpecialistInfo(eSpecialist).getGreatPeopleUnitClass())));

		if (eGreatPeopleUnit != NO_UNIT)
		{
			changeGreatPeopleUnitRate(eGreatPeopleUnit, GC.getSpecialistInfo(eSpecialist).getGreatPeopleRateChange() * iChange);
		}
	}

	changeBaseGreatPeopleRate(GC.getSpecialistInfo(eSpecialist).getGreatPeopleRateChange() * iChange);

	for (iI = 0; iI < NUM_YIELD_TYPES; iI++)
	{
		changeBaseYieldRate(((YieldTypes)iI), (GC.getSpecialistInfo(eSpecialist).getYieldChange(iI) * iChange));
		// Leoreth: catch the overflow bug
		if (getBaseYieldRate((YieldTypes)iI) < 0 || getBaseYieldRate((YieldTypes)iI) > 1000) {
				GC.getGame().logMsg("Overflow in (%d, %d) for processSpecialist", getX(), getY());
			gDLL->getInterfaceIFace()->addMessage(GC.getGame().getActivePlayer(), true, GC.getEVENT_MESSAGE_TIME(), gDLL->getText("TXT_KEY_OVERFLOW", getX(), getY(), "processSpecialist()"), "", MESSAGE_TYPE_MAJOR_EVENT, ARTFILEMGR.getInterfaceArtInfo("WORLDBUILDER_CITY_EDIT")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_RED"), getX_INLINE(), getY_INLINE(), true, true);
			GC.getGame().setAIAutoPlay(0);
			GC.getGame().setAIAutoPlayCatapult(0);
			gDLL->getEngineIFace()->AutoSave(true);
		}
	}

	for (iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
	{
		changeSpecialistCommerce(((CommerceTypes)iI), (GC.getSpecialistInfo(eSpecialist).getCommerceChange(iI) * iChange));
	}

	updateExtraSpecialistYield();

	changeSpecialistFreeExperience(GC.getSpecialistInfo(eSpecialist).getExperience() * iChange);

	int iHappinessChange = GC.getSpecialistInfo(eSpecialist).getHappiness();
	if (iHappinessChange > 0)
	{
		changeSpecialistGoodHappiness(iHappinessChange * iChange);
	}
	else
	{
		changeSpecialistBadHappiness(-iHappinessChange * iChange);
	}
}


HandicapTypes CvCity::getHandicapType() const
{
	return GET_PLAYER(getOwnerINLINE()).getHandicapType();
}


CivilizationTypes CvCity::getCivilizationType() const
{
	return GET_PLAYER(getOwnerINLINE()).getCivilizationType();
}


LeaderHeadTypes CvCity::getPersonalityType() const
{
	return GET_PLAYER(getOwnerINLINE()).getPersonalityType();
}


ArtStyleTypes CvCity::getArtStyleType() const
{
	return m_eArtStyle;
}

void CvCity::updateArtStyleType()
{
	bool bECS = (GC.getDefineINT("ETHNIC_CITY_STYLES") == 1);
	PlayerTypes eHighestCulture = findHighestCulture(true);
	if (eHighestCulture == NO_PLAYER) eHighestCulture = getOwnerINLINE();
	int id = getRegionID();

	ArtStyleTypes eNewArtStyle = GET_PLAYER(eHighestCulture).getArtStyleType();

	if (bECS)
	{
		if (eHighestCulture == NATIVE)
		{
			switch (id)
			{
			case REGION_ALASKA:
			case REGION_CANADA:
			case REGION_UNITED_STATES:
				eNewArtStyle = (ArtStyleTypes)ARTSTYLE_NATIVE_AMERICA;
				break;
			case REGION_MESOAMERICA:
			case REGION_CARIBBEAN:
				eNewArtStyle = (ArtStyleTypes)ARTSTYLE_MESO_AMERICA;
				break;
			case REGION_BRAZIL:
			case REGION_ARGENTINA:
			case REGION_PERU:
			case REGION_COLOMBIA:
				eNewArtStyle = (ArtStyleTypes)ARTSTYLE_SOUTH_AMERICA;
				break;
			case REGION_ETHIOPIA:
			case REGION_WEST_AFRICA:
			case REGION_SOUTH_AFRICA:
				eNewArtStyle = (ArtStyleTypes)ARTSTYLE_AFRICA;
				break;
			default:
				break;
			}
		}
		else if (eHighestCulture == INDEPENDENT || eHighestCulture == INDEPENDENT2 || eHighestCulture == BARBARIAN || (eHighestCulture == MONGOLIA && getOriginalOwner() != MONGOLIA))
		{
			switch (id)
			{
			case REGION_ALASKA:
			case REGION_CANADA:
			case REGION_UNITED_STATES:
			case REGION_BRITAIN:
				eNewArtStyle = (ArtStyleTypes)ARTSTYLE_ANGLO_AMERICA;
				break;
			case REGION_MESOAMERICA:
			case REGION_CARIBBEAN:
				if (eHighestCulture == AZTECS || eHighestCulture == MAYA) eNewArtStyle = (ArtStyleTypes)ARTSTYLE_MESO_AMERICA;
				else eNewArtStyle = (ArtStyleTypes)ARTSTYLE_IBERIA;
				break;
			case REGION_BRAZIL:
			case REGION_ARGENTINA:
			case REGION_PERU:
			case REGION_COLOMBIA:
				if (eHighestCulture == INCA) eNewArtStyle = (ArtStyleTypes)ARTSTYLE_SOUTH_AMERICA;
				else eNewArtStyle = (ArtStyleTypes)ARTSTYLE_IBERIA;
				break;
			case REGION_ETHIOPIA:
			case REGION_WEST_AFRICA:
			case REGION_SOUTH_AFRICA:
				eNewArtStyle = (ArtStyleTypes)ARTSTYLE_AFRICA;
				break;
			case REGION_IBERIA:
				eNewArtStyle = (ArtStyleTypes)ARTSTYLE_IBERIA;
				break;
			case REGION_ITALY:
			case REGION_BALKANS:
				eNewArtStyle = (ArtStyleTypes)ARTSTYLE_GRECO_ROMAN;
				break;
			case REGION_MAGHREB:
				if (isHasReligion((ReligionTypes)ISLAM)) eNewArtStyle = (ArtStyleTypes)ARTSTYLE_ARABIA;
				else eNewArtStyle = (ArtStyleTypes)ARTSTYLE_GRECO_ROMAN;
				break;
			case REGION_ANATOLIA:
				if (isHasReligion((ReligionTypes)ISLAM)) eNewArtStyle = (ArtStyleTypes)ARTSTYLE_CRESCENT;
				else eNewArtStyle = (ArtStyleTypes)ARTSTYLE_GRECO_ROMAN;
				break;
			case REGION_EUROPE:
				eNewArtStyle = (ArtStyleTypes)ARTSTYLE_EUROPE;
				break;
			case REGION_SCANDINAVIA:
				eNewArtStyle = (ArtStyleTypes)ARTSTYLE_NORSE;
				break;
			case REGION_RUSSIA:
			case REGION_SIBERIA:
				eNewArtStyle = (ArtStyleTypes)ARTSTYLE_RUSSIA;
				break;
			case REGION_ARABIA:
				eNewArtStyle = (ArtStyleTypes)ARTSTYLE_ARABIA;
				break;
			case REGION_EGYPT:
				if (isHasReligion((ReligionTypes)ISLAM)) eNewArtStyle = (ArtStyleTypes)ARTSTYLE_ARABIA;
				else if (GET_PLAYER(eHighestCulture).getCurrentEra() == ERA_ANCIENT) eNewArtStyle = (ArtStyleTypes)ARTSTYLE_EGYPT;
				else eNewArtStyle = (ArtStyleTypes)ARTSTYLE_GRECO_ROMAN;
				break;
			case REGION_INDIA:
			case REGION_DECCAN:
				if (isHasReligion((ReligionTypes)ISLAM)) eNewArtStyle = (ArtStyleTypes)ARTSTYLE_CRESCENT;
				else eNewArtStyle = (ArtStyleTypes)ARTSTYLE_INDIA;
				break;
			case REGION_INDOCHINA:
			case REGION_INDONESIA:
				eNewArtStyle = (ArtStyleTypes)ARTSTYLE_SOUTH_EAST_ASIA;
				break;
			case REGION_CHINA:
			case REGION_MANCHURIA:
			case REGION_TIBET:
			case REGION_KOREA:
				eNewArtStyle = (ArtStyleTypes)ARTSTYLE_ASIA;
				break;
			case REGION_JAPAN:
				eNewArtStyle = (ArtStyleTypes)ARTSTYLE_JAPAN;
				break;
			case REGION_CENTRAL_ASIA:
				eNewArtStyle = (ArtStyleTypes)ARTSTYLE_MONGOLIA;
				break;
			case REGION_AUSTRALIA:
			case REGION_OCEANIA:
				eNewArtStyle = (ArtStyleTypes)ARTSTYLE_SOUTH_PACIFIC;
				break;
			default:
				break;
			}
		}
		else if (eHighestCulture == MONGOLIA)
		{
			if (getPopulation() >= 5) eNewArtStyle = GET_PLAYER((PlayerTypes)CHINA).getArtStyleType();
		}
		else if (eHighestCulture == AZTECS || eHighestCulture == MAYA || eHighestCulture == INCA)
		{
			if (GET_PLAYER(eHighestCulture).getStateReligion() == CATHOLICISM) eNewArtStyle = (ArtStyleTypes)ARTSTYLE_IBERIA;
		}
	}
	else 
	{
		if (eHighestCulture == INDEPENDENT || eHighestCulture == INDEPENDENT2 || eHighestCulture == BARBARIAN)
		{
			switch (id)
			{
			case REGION_BRITAIN:
			case REGION_EUROPE:
			case REGION_SCANDINAVIA:
			case REGION_RUSSIA:
			case REGION_SIBERIA:
			case REGION_AUSTRALIA:
			case REGION_CANADA:
			case REGION_ALASKA:
			case REGION_UNITED_STATES:
				eNewArtStyle = ARTSTYLE_EUROPEAN;
				break;
			case REGION_ITALY:
				if (GET_PLAYER(eHighestCulture).getCurrentEra() >= ERA_MEDIEVAL) eNewArtStyle = ARTSTYLE_EUROPEAN;
				else eNewArtStyle = ARTSTYLE_GRECO_ROMAN_OLD;
				break;
			case REGION_IBERIA:
				if (isHasReligion((ReligionTypes)ISLAM)) eNewArtStyle = ARTSTYLE_MIDDLE_EAST;
				else if (GET_PLAYER(eHighestCulture).getCurrentEra() >= ERA_MEDIEVAL) eNewArtStyle = ARTSTYLE_EUROPEAN;
				else eNewArtStyle = ARTSTYLE_GRECO_ROMAN_OLD;
				break;
			case REGION_ANATOLIA:
			case REGION_MAGHREB:
				if (isHasReligion((ReligionTypes)ISLAM)) eNewArtStyle = ARTSTYLE_MIDDLE_EAST;
				else eNewArtStyle = ARTSTYLE_GRECO_ROMAN_OLD;
				break;
			case REGION_MESOPOTAMIA:
			case REGION_ARABIA:
			case REGION_EGYPT:
			case REGION_PERSIA:
			case REGION_INDIA:
			case REGION_DECCAN:
				eNewArtStyle = ARTSTYLE_MIDDLE_EAST;
				break;
			case REGION_INDOCHINA:
			case REGION_INDONESIA:
			case REGION_CHINA:
			case REGION_KOREA:
			case REGION_JAPAN:
			case REGION_MANCHURIA:
			case REGION_TIBET:
			case REGION_CENTRAL_ASIA:
				eNewArtStyle = ARTSTYLE_ASIAN;
				break;
			case REGION_OCEANIA:
				eNewArtStyle = ARTSTYLE_BARBARIAN_OLD;
				break;
			case REGION_ETHIOPIA:
			case REGION_WEST_AFRICA:
			case REGION_SOUTH_AFRICA:
				eNewArtStyle = ARTSTYLE_AFRICAN;
				break;
			case REGION_CARIBBEAN:
			case REGION_MESOAMERICA:
			case REGION_BRAZIL:
			case REGION_ARGENTINA:
			case REGION_PERU:
			case REGION_COLOMBIA:
				if (isHasReligion((ReligionTypes)CATHOLICISM) || isHasReligion((ReligionTypes)PROTESTANTISM)) eNewArtStyle = ARTSTYLE_EUROPEAN;
				else eNewArtStyle = ARTSTYLE_SOUTH_AMERICA_OLD;
				break;
			default:
				break;
			}
		}
	}

	if (m_eArtStyle != eNewArtStyle)
	{
		m_eArtStyle = eNewArtStyle;
		setLayoutDirty(true);
	}
}


CitySizeTypes CvCity::getCitySizeType() const
{
	return ((CitySizeTypes)(range((getPopulation() / 7), 0, (NUM_CITYSIZE_TYPES - 1))));
}

const CvArtInfoBuilding* CvCity::getBuildingArtInfo(BuildingTypes eBuilding) const
{
	return GC.getBuildingInfo(eBuilding).getArtInfo();
}

float CvCity::getBuildingVisibilityPriority(BuildingTypes eBuilding) const
{
	return GC.getBuildingInfo(eBuilding).getVisibilityPriority();
}

bool CvCity::hasTrait(TraitTypes eTrait) const
{
	return GET_PLAYER(getOwnerINLINE()).hasTrait(eTrait);
}


bool CvCity::isBarbarian() const
{
	return GET_PLAYER(getOwnerINLINE()).isBarbarian();
}


bool CvCity::isHuman() const
{
	return GET_PLAYER(getOwnerINLINE()).isHuman();
}


bool CvCity::isVisible(TeamTypes eTeam, bool bDebug) const
{
	return plot()->isVisible(eTeam, bDebug);
}


bool CvCity::isCapital() const
{
	return (GET_PLAYER(getOwnerINLINE()).getCapitalCity() == this);
}


bool CvCity::isCoastal(int iMinWaterSize) const
{
	return plot()->isCoastalLand(iMinWaterSize);
}

//Rhye - start
bool CvCity::isCoastalOld() const
{
	return plot()->isCoastalLand(0);
}
//Rhye - end


bool CvCity::isDisorder() const
{
	return (isOccupation() || GET_PLAYER(getOwnerINLINE()).isAnarchy());
}


bool CvCity::isHolyCity(ReligionTypes eIndex) const
{
	return (GC.getGameINLINE().getHolyCity(eIndex) == this);
}


bool CvCity::isHolyCity() const
{
	int iI;

	for (iI = 0; iI < GC.getNumReligionInfos(); iI++)
	{
		if (isHolyCity((ReligionTypes)iI))
		{
			return true;
		}
	}

	return false;
}


bool CvCity::isHeadquarters(CorporationTypes eIndex) const
{
	return (GC.getGameINLINE().getHeadquarters(eIndex) == this);
}

void CvCity::setHeadquarters(CorporationTypes eIndex)
{
	GC.getGameINLINE().setHeadquarters(eIndex, this, true);

	if (GC.getCorporationInfo(eIndex).getFreeUnitClass() != NO_UNITCLASS)
	{
		UnitTypes eFreeUnit = ((UnitTypes)(GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(GC.getCorporationInfo(eIndex).getFreeUnitClass())));

		if (eFreeUnit != NO_UNIT)
		{
			GET_PLAYER(getOwnerINLINE()).initUnit(eFreeUnit, getX_INLINE(), getY_INLINE());
		}
	}
}

bool CvCity::isHeadquarters() const
{
	int iI;

	for (iI = 0; iI < GC.getNumCorporationInfos(); iI++)
	{
		if (isHeadquarters((CorporationTypes)iI))
		{
			return true;
		}
	}

	return false;
}


int CvCity::getOvercrowdingPercentAnger(int iExtra) const
{
	int iOvercrowding;
	int iAnger;

	iAnger = 0;

	iOvercrowding = (getPopulation() + iExtra);

	if (iOvercrowding > 0)
	{
		iAnger += (((iOvercrowding * GC.getPERCENT_ANGER_DIVISOR()) / std::max(1, (getPopulation() + iExtra))) + 1);
	}

	return iAnger;
}


int CvCity::getNoMilitaryPercentAnger() const
{
	int iAnger;

	iAnger = 0;

	if (getMilitaryHappinessUnits() == 0)
	{
		iAnger += GC.getDefineINT("NO_MILITARY_PERCENT_ANGER");
	}

	return iAnger;
}


int CvCity::getCulturePercentAnger() const
{
	int iTotalCulture;
	int iAngryCulture;
	int iCulture;
	int iI;

	//iTotalCulture = plot()->countTotalCulture();
	iTotalCulture = countTotalCultureTimes100() / 100;

	if (iTotalCulture == 0)
	{
		return 0;
	}

	iAngryCulture = 0;

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		// Leoreth: worry about culture even if they're dead
		if (/*GET_PLAYER((PlayerTypes)iI).isAlive() &&*/ !GET_PLAYER((PlayerTypes)iI).isMinorCiv() && iI != INDEPENDENT && iI != INDEPENDENT2)
		{
			if (GET_PLAYER((PlayerTypes)iI).getTeam() != getTeam())
			{
				//iCulture = plot()->getCulture((PlayerTypes)iI);
				iCulture = getCulture((PlayerTypes)iI);

				if (iCulture > 0)
				{
					if (!GET_PLAYER((PlayerTypes)iI).isAlive())
					{
						iCulture *= 50;
						iCulture /= 100;
					}
					else if (atWar(GET_PLAYER((PlayerTypes)iI).getTeam(), getTeam()))
					{
						iCulture *= std::max(0, (GC.getDefineINT("AT_WAR_CULTURE_ANGER_MODIFIER") + 100));
						iCulture /= 100;
					}

					iAngryCulture += iCulture;
				}
			}
		}
	}

	return ((GC.getDefineINT("CULTURE_PERCENT_ANGER") * iAngryCulture) / iTotalCulture);
}


int CvCity::getReligionPercentAnger() const
{
	int iCount;
	int iAnger;
	int iI;

	if (GC.getGameINLINE().getNumCities() == 0)
	{
		return 0;
	}

	if (getReligionCount() == 0)
	{
		return 0;
	}

	iCount = 0;

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			if (atWar(GET_PLAYER((PlayerTypes)iI).getTeam(), getTeam()))
			{
				FAssertMsg(GET_PLAYER((PlayerTypes)iI).getTeam() != getTeam(), "Player is at war with himself! :O");

				if (GET_PLAYER((PlayerTypes)iI).getStateReligion() != NO_RELIGION)
				{
					if (isHasReligion(GET_PLAYER((PlayerTypes)iI).getStateReligion()))
					{
						iCount += GET_PLAYER((PlayerTypes)iI).getHasReligionCount(GET_PLAYER((PlayerTypes)iI).getStateReligion());
					}
				}
			}
		}
	}

	iAnger = GC.getDefineINT("RELIGION_PERCENT_ANGER");

	iAnger *= iCount;
	iAnger /= GC.getGameINLINE().getNumCities();

	iAnger /= getReligionCount();

	return iAnger;
}


int CvCity::getHurryPercentAnger(int iExtra) const
{
	if (getHurryAngerTimer() == 0)
	{
		return 0;
	}

	return ((((((getHurryAngerTimer() - 1) / flatHurryAngerLength()) + 1) * GC.getDefineINT("HURRY_POP_ANGER") * GC.getPERCENT_ANGER_DIVISOR()) / std::max(1, getPopulation() + iExtra)) + 1);
}


int CvCity::getConscriptPercentAnger(int iExtra) const
{
	if (getConscriptAngerTimer() == 0)
	{
		return 0;
	}

	return ((((((getConscriptAngerTimer() - 1) / flatConscriptAngerLength()) + 1) * GC.getDefineINT("CONSCRIPT_POP_ANGER") * GC.getPERCENT_ANGER_DIVISOR()) / std::max(1, getPopulation() + iExtra)) + 1);
}

int CvCity::getDefyResolutionPercentAnger(int iExtra) const
{
	if (getDefyResolutionAngerTimer() == 0)
	{
		return 0;
	}

	return ((((((getDefyResolutionAngerTimer() - 1) / flatDefyResolutionAngerLength()) + 1) * GC.getDefineINT("DEFY_RESOLUTION_POP_ANGER") * GC.getPERCENT_ANGER_DIVISOR()) / std::max(1, getPopulation() + iExtra)) + 1);
}


int CvCity::getWarWearinessPercentAnger() const
{
	int iAnger;

	iAnger = GET_PLAYER(getOwnerINLINE()).getWarWearinessPercentAnger();

	iAnger *= std::max(0, (getWarWearinessModifier() + GET_PLAYER(getOwnerINLINE()).getWarWearinessModifier() + 100));
	iAnger /= 100;

	return iAnger;
}


int CvCity::getLargestCityHappiness() const
{
	if (findPopulationRank() <= GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getTargetNumCities())
	{
		return GET_PLAYER(getOwnerINLINE()).getLargestCityHappiness();
	}

	return 0;
}

int CvCity::getVassalHappiness() const
{
	int iHappy = 0;

	for (int i = 0; i < MAX_TEAMS; i++)
	{
		if (getTeam() != i)
		{
			if (GET_TEAM((TeamTypes)i).isVassal(getTeam()))
			{
				iHappy += GC.getDefineINT("VASSAL_HAPPINESS");
			}
		}
	}

	return iHappy;
}

int CvCity::getVassalUnhappiness() const
{
	int iUnhappy = 0;

	for (int i = 0; i < MAX_TEAMS; i++)
	{
		if (getTeam() != i)
		{
			if (GET_TEAM(getTeam()).isVassal((TeamTypes)i))
			{
				iUnhappy += GC.getDefineINT("VASSAL_HAPPINESS");
			}
		}
	}

	return iUnhappy;
}


int CvCity::unhappyLevel(int iExtra) const
{
	int iAngerPercent;
	int iUnhappiness;
	int iI;

	iUnhappiness = 0;

	if (!isNoUnhappiness())
	{
		iAngerPercent = 0;

		iAngerPercent += getOvercrowdingPercentAnger(iExtra);
		iAngerPercent += getNoMilitaryPercentAnger();
		iAngerPercent += getCulturePercentAnger();
		iAngerPercent += getReligionPercentAnger();
		iAngerPercent += getHurryPercentAnger(iExtra);
		iAngerPercent += getConscriptPercentAnger(iExtra);
		iAngerPercent += getDefyResolutionPercentAnger(iExtra);
		iAngerPercent += getWarWearinessPercentAnger();

		for (iI = 0; iI < GC.getNumCivicInfos(); iI++)
		{
			iAngerPercent += GET_PLAYER(getOwnerINLINE()).getCivicPercentAnger((CivicTypes)iI);
		}

		iUnhappiness = ((iAngerPercent * (getPopulation() + iExtra)) / GC.getPERCENT_ANGER_DIVISOR());

		iUnhappiness -= std::min(0, getLargestCityHappiness());
		iUnhappiness -= std::min(0, getMilitaryHappiness());
		iUnhappiness -= std::min(0, getCurrentStateReligionHappiness());
		iUnhappiness -= std::min(0, getBuildingBadHappiness());
		iUnhappiness -= std::min(0, getExtraBuildingBadHappiness());
		iUnhappiness -= std::min(0, getFeatureBadHappiness());
		iUnhappiness -= std::min(0, getBonusBadHappiness());
		iUnhappiness -= std::min(0, getReligionBadHappiness());
		iUnhappiness -= std::min(0, getCommerceHappiness());
		iUnhappiness -= std::min(0, area()->getBuildingHappiness(getOwnerINLINE()));
		iUnhappiness -= std::min(0, GET_PLAYER(getOwnerINLINE()).getBuildingHappiness());
		iUnhappiness -= std::min(0, (getExtraHappiness() + GET_PLAYER(getOwnerINLINE()).getExtraHappiness()));
		iUnhappiness -= std::min(0, GC.getHandicapInfo(getHandicapType()).getHappyBonusByID(getOwner()));
		iUnhappiness += std::max(0, getVassalUnhappiness());
		iUnhappiness += std::max(0, getEspionageHappinessCounter());
		iUnhappiness += std::max(0, getSpecialistBadHappiness()); // Leoreth
		iUnhappiness += std::max(0, getCorporationBadHappiness()); // Leoreth
	}

	return std::max(0, iUnhappiness);
}


int CvCity::happyLevel() const
{
	int iHappiness;

	iHappiness = 0;

	iHappiness += std::max(0, getLargestCityHappiness());
	iHappiness += std::max(0, getMilitaryHappiness());
	iHappiness += std::max(0, getCurrentStateReligionHappiness());
	iHappiness += std::max(0, getBuildingGoodHappiness());
	iHappiness += std::max(0, getExtraBuildingGoodHappiness());
	iHappiness += std::max(0, getFeatureGoodHappiness());
	iHappiness += std::max(0, getBonusGoodHappiness());
	iHappiness += std::max(0, getReligionGoodHappiness());
	iHappiness += std::max(0, getCorporationGoodHappiness()); // Leoreth
	iHappiness += std::max(0, getSpecialistGoodHappiness()); // Leoreth
	iHappiness += std::max(0, getCommerceHappiness());
	iHappiness += std::max(0, area()->getBuildingHappiness(getOwnerINLINE()));
	iHappiness += std::max(0, GET_PLAYER(getOwnerINLINE()).getBuildingHappiness());
	iHappiness += std::max(0, (getExtraHappiness() + GET_PLAYER(getOwnerINLINE()).getExtraHappiness()));
	iHappiness += std::max(0, GC.getHandicapInfo(getHandicapType()).getHappyBonusByID(getOwner()));
	iHappiness += std::max(0, getVassalHappiness());

	if (getHappinessTimer() > 0)
	{
		iHappiness += GC.getDefineINT("TEMP_HAPPY");
	}

	return std::max(0, iHappiness);
}


int CvCity::angryPopulation(int iExtra) const
{
	PROFILE("CvCityAI::angryPopulation");

	return range((unhappyLevel(iExtra) - happyLevel()), 0, (getPopulation() + iExtra));
}


int CvCity::visiblePopulation() const
{
	return (getPopulation() - angryPopulation() - getWorkingPopulation());
}


int CvCity::totalFreeSpecialists() const
{
	int iCount = 0;
	if (getPopulation() > 0)
	{
		iCount += getFreeSpecialist();
		iCount += area()->getFreeSpecialist(getOwnerINLINE());
		iCount += GET_PLAYER(getOwnerINLINE()).getFreeSpecialist();

		for (int iImprovement = 0; iImprovement < GC.getNumImprovementInfos(); ++iImprovement)
		{
			int iNumSpecialistsPerImprovement = getImprovementFreeSpecialists((ImprovementTypes)iImprovement);
			if (iNumSpecialistsPerImprovement > 0)
			{
				iCount += iNumSpecialistsPerImprovement * countNumImprovedPlots((ImprovementTypes)iImprovement);
			}
		}
	}

	return iCount;
}


int CvCity::extraPopulation() const
{
	return (visiblePopulation() + std::min(0, extraFreeSpecialists()));
}


int CvCity::extraSpecialists() const
{
	return (visiblePopulation() + extraFreeSpecialists());
}


int CvCity::extraFreeSpecialists() const
{
	return (totalFreeSpecialists() - getSpecialistPopulation());
}


int CvCity::unhealthyPopulation(bool bNoAngry, int iExtra) const
{
	if (isNoUnhealthyPopulation())
	{
		return 0;
	}

	return std::max(0, ((getPopulation() + iExtra - ((bNoAngry) ? angryPopulation(iExtra) : 0))));
}


int CvCity::totalGoodBuildingHealth() const
{
	return (getBuildingGoodHealth() + area()->getBuildingGoodHealth(getOwnerINLINE()) + GET_PLAYER(getOwnerINLINE()).getBuildingGoodHealth() + getExtraBuildingGoodHealth());
}


int CvCity::totalBadBuildingHealth() const
{
	if (!isBuildingOnlyHealthy())
	{
		return (getBuildingBadHealth() + area()->getBuildingBadHealth(getOwnerINLINE()) + GET_PLAYER(getOwnerINLINE()).getBuildingBadHealth() + getExtraBuildingBadHealth());
	}

	return 0;
}


int CvCity::goodHealth() const
{
	int iTotalHealth;
	int iHealth;

	iTotalHealth = 0;

	iHealth = getFreshWaterGoodHealth();
	if (iHealth > 0)
	{
		iTotalHealth += iHealth;
	}

	iHealth = getFeatureGoodHealth();
	if (iHealth > 0)
	{
		iTotalHealth += iHealth;
	}

	iHealth = getPowerGoodHealth();
	if (iHealth > 0)
	{
		iTotalHealth += iHealth;
	}

	iHealth = getBonusGoodHealth();
	if (iHealth > 0)
	{
		iTotalHealth += iHealth;
	}

	iHealth = totalGoodBuildingHealth();
	if (iHealth > 0)
	{
		iTotalHealth += iHealth;
	}

	// Leoreth
	iHealth = getCorporationHealth();
	if (iHealth > 0)
	{
		iTotalHealth += iHealth;
	}

	iHealth = GET_PLAYER(getOwnerINLINE()).getExtraHealth() + getExtraHealth();
	if (iHealth > 0)
	{
		iTotalHealth += iHealth;
	}

	//iHealth = GC.getHandicapInfo(getHandicapType()).getHealthBonus(); //Rhye
	iHealth = GC.getHandicapInfo(getHandicapType()).getHealthBonusByID(getOwnerINLINE()); //Rhye
	if (iHealth > 0)
	{
		iTotalHealth += iHealth;
	}

	//Leoreth: Indian UP: +1 health per specialist - deprecated
	/*if (getOwner() == INDIA)
	{
		iHealth = getSpecialistPopulation();
		if (iHealth > 0)
		{
			iTotalHealth += iHealth;
		}
	}*/

	// Leoreth: Indian UP: +1 health for every 3 excess happiness
	if (getOwner() == INDIA)
	{
		iHealth = (happyLevel() - unhappyLevel()) / 3;
		if (iHealth > 0)
		{
			iTotalHealth += iHealth;
		}
	}

	return iTotalHealth;
}


int CvCity::badHealth(bool bNoAngry, int iExtra) const
{
	int iTotalHealth;
	int iHealth;

	iTotalHealth = 0;

	iHealth = getEspionageHealthCounter();
	if (iHealth > 0)
	{
		iTotalHealth -= iHealth;
	}

	iHealth = getFreshWaterBadHealth();
	if (iHealth < 0)
	{
		iTotalHealth += iHealth;
	}

	iHealth = getFeatureBadHealth();
	if (iHealth < 0)
	{
		iTotalHealth += iHealth;
	}

	iHealth = getPowerBadHealth();
	if (iHealth < 0)
	{
		iTotalHealth += iHealth;
	}

	iHealth = getBonusBadHealth();
	if (iHealth < 0)
	{
		iTotalHealth += iHealth;
	}

	iHealth = totalBadBuildingHealth();
	if (iHealth < 0)
	{
		iTotalHealth += iHealth;
	}

	// Leoreth
	iHealth = -getCorporationUnhealth();
	if (iHealth < 0)
	{
		iTotalHealth += iHealth;
	}

	iHealth = GET_PLAYER(getOwnerINLINE()).getExtraHealth() + getExtraHealth();
	if (iHealth < 0)
	{
		iTotalHealth += iHealth;
	}

	//iHealth = GC.getHandicapInfo(getHandicapType()).getHealthBonus(); //Rhye
	iHealth = GC.getHandicapInfo(getHandicapType()).getHealthBonusByID(getOwnerINLINE()); //Rhye
	if (iHealth < 0)
	{
		iTotalHealth += iHealth;
	}

	iHealth = getExtraBuildingBadHealth();
	if (iHealth < 0)
	{
		iTotalHealth += iHealth;
	}

	//Leoreth: civic pollution modifier
	iTotalHealth = iTotalHealth * (100 + GET_PLAYER(getOwner()).getPollutionModifier()) / 100;

	return (unhealthyPopulation(bNoAngry, iExtra) - iTotalHealth);
}


int CvCity::healthRate(bool bNoAngry, int iExtra) const
{
	return std::min(0, (goodHealth() - badHealth(bNoAngry, iExtra)));
}


int CvCity::foodConsumption(bool bNoAngry, int iExtra) const
{
	return ((((getPopulation() + iExtra) - ((bNoAngry) ? angryPopulation(iExtra) : 0)) * GC.getFOOD_CONSUMPTION_PER_POPULATION()) - healthRate(bNoAngry, iExtra));
}


int CvCity::foodDifference(bool bBottom) const
{
	int iDifference;

	if (isDisorder())
	{
		return 0;
	}

	if (isFoodProduction())
	{
		iDifference = std::min(0, (getYieldRate(YIELD_FOOD) - foodConsumption()));
	}
	else
	{
		iDifference = (getYieldRate(YIELD_FOOD) - foodConsumption());
	}

	if (bBottom)
	{
		if ((getPopulation() == 1) && (getFood() == 0))
		{
			iDifference = std::max(0, iDifference);
		}
	}

	return iDifference;
}


int CvCity::growthThreshold() const
{
	return (GET_PLAYER(getOwnerINLINE()).getGrowthThreshold(getPopulation()));
}


int CvCity::productionLeft() const
{
	return (getProductionNeeded() - getProduction());
}

int CvCity::getHurryCostModifier(bool bIgnoreNew) const
{
	int iModifier = 100;
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		switch (pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
			iModifier = getHurryCostModifier((UnitTypes) pOrderNode->m_data.iData1, bIgnoreNew);
			break;

		case ORDER_CONSTRUCT:
			iModifier = getHurryCostModifier((BuildingTypes) pOrderNode->m_data.iData1, bIgnoreNew);
			break;

		case ORDER_CREATE:
		case ORDER_MAINTAIN:
			break;

		default:
			FAssertMsg(false, "pOrderNode->m_data.eOrderType did not match a valid option");
			break;
		}
	}

	return iModifier;
}

int CvCity::getHurryCostModifier(UnitTypes eUnit, bool bIgnoreNew) const
{
	return getHurryCostModifier(GC.getUnitInfo(eUnit).getHurryCostModifier(), getUnitProduction(eUnit), bIgnoreNew);
}

int CvCity::getHurryCostModifier(BuildingTypes eBuilding, bool bIgnoreNew) const
{
	return getHurryCostModifier(GC.getBuildingInfo(eBuilding).getHurryCostModifier(), getBuildingProduction(eBuilding), bIgnoreNew);
}

int CvCity::getHurryCostModifier(int iBaseModifier, int iProduction, bool bIgnoreNew) const
{
	int iModifier = 100;
	iModifier *= std::max(0, iBaseModifier + 100);
	iModifier /= 100;

	if (iProduction == 0 && !bIgnoreNew)
	{
		iModifier *= std::max(0, (GC.getDefineINT("NEW_HURRY_MODIFIER") + 100));
		iModifier /= 100;
	}

	iModifier *= std::max(0, (GET_PLAYER(getOwnerINLINE()).getHurryModifier() + 100));
	iModifier /= 100;

	return iModifier;
}


int CvCity::hurryCost(bool bExtra) const
{
	return (getHurryCost(bExtra, productionLeft(), getHurryCostModifier(), getProductionModifier()));
}

int CvCity::getHurryCost(bool bExtra, UnitTypes eUnit, bool bIgnoreNew) const
{
	int iProductionLeft = getProductionNeeded(eUnit) - getUnitProduction(eUnit);

	return getHurryCost(bExtra, iProductionLeft, getHurryCostModifier(eUnit, bIgnoreNew), getProductionModifier(eUnit));
}

int CvCity::getHurryCost(bool bExtra, BuildingTypes eBuilding, bool bIgnoreNew) const
{
	int iProductionLeft = getProductionNeeded(eBuilding) - getBuildingProduction(eBuilding);

	return getHurryCost(bExtra, iProductionLeft, getHurryCostModifier(eBuilding, bIgnoreNew), getProductionModifier(eBuilding));
}

int CvCity::getHurryCost(bool bExtra, int iProductionLeft, int iHurryModifier, int iModifier) const
{
	int iProduction = (iProductionLeft * iHurryModifier + 99) / 100; // round up

	if (bExtra)
	{
		int iExtraProduction = getExtraProductionDifference(iProduction, iModifier);
		if (iExtraProduction > 0)
		{
			int iAdjustedProd = iProduction * iProduction;

			// round up
			iProduction = (iAdjustedProd + (iExtraProduction - 1)) / iExtraProduction;
		}
	}

	return std::max(0, iProduction);
}

int CvCity::hurryGold(HurryTypes eHurry) const
{
	return getHurryGold(eHurry, hurryCost(false));
}

int CvCity::getHurryGold(HurryTypes eHurry, int iHurryCost) const
{
	int iGold;

	if (GC.getHurryInfo(eHurry).getGoldPerProduction() == 0)
	{
		return 0;
	}

	iGold = (iHurryCost * GC.getHurryInfo(eHurry).getGoldPerProduction());
	
	// Phoenician UP: -50% mercenary cost
	if (getOwnerINLINE() == PHOENICIA && GC.getHurryInfo(eHurry).isUnits())
	{
		iGold /= 2;
	}

	return std::max(1, iGold);
}


int CvCity::hurryPopulation(HurryTypes eHurry) const
{
	return (getHurryPopulation(eHurry, hurryCost(true)));
}

int CvCity::getHurryPopulation(HurryTypes eHurry, int iHurryCost) const
{
	if (GC.getHurryInfo(eHurry).getProductionPerPopulation() == 0)
	{
		return 0;
	}

	int iPopulation = (iHurryCost - 1) / GC.getGameINLINE().getProductionPerPopulation(eHurry);

	return std::max(1, (iPopulation + 1));
}

int CvCity::hurryProduction(HurryTypes eHurry) const
{
	int iProduction;

	if (GC.getHurryInfo(eHurry).getProductionPerPopulation() > 0)
	{
		iProduction = (100 * getExtraProductionDifference(hurryPopulation(eHurry) * GC.getGameINLINE().getProductionPerPopulation(eHurry))) / std::max(1, getHurryCostModifier());
		FAssert(iProduction >= productionLeft());
	}
	else
	{
		iProduction = productionLeft();
	}

	return iProduction;
}


int CvCity::flatHurryAngerLength() const
{
	int iAnger;

	iAnger = GC.getDefineINT("HURRY_ANGER_DIVISOR");
	iAnger *= GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getHurryConscriptAngerPercent();
	iAnger /= 100;
	iAnger *= std::max(0, 100 + getHurryAngerModifier());
	iAnger /= 100;

	return std::max(1, iAnger);
}


int CvCity::hurryAngerLength(HurryTypes eHurry) const
{
	if (GC.getHurryInfo(eHurry).isAnger())
	{
		return flatHurryAngerLength();
	}
	else
	{
		return 0;
	}
}


int CvCity::maxHurryPopulation() const
{
	return (getPopulation() / 2);
}


int CvCity::cultureDistance(int iDX, int iDY) const
{
	return std::max(1, plotDistance(0, 0, iDX, iDY));
}


int CvCity::cultureStrength(PlayerTypes ePlayer) const
{
	CvPlot* pLoopPlot;
	int iStrength;
	int iI;

	iStrength = 1;

	iStrength += (getHighestPopulation() * 2);

	for (iI = 0; iI < NUM_DIRECTION_TYPES; iI++)
	{
		pLoopPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

		if (pLoopPlot != NULL)
		{
			if (pLoopPlot->getOwnerINLINE() == ePlayer)
			{
				iStrength += (GC.getGameINLINE().getCurrentEra() + 1);
			}
		}
	}

	iStrength *= std::max(0, (((GC.getDefineINT("REVOLT_TOTAL_CULTURE_MODIFIER") * (plot()->getCulture(ePlayer) - plot()->getCulture(getOwnerINLINE()) + 1)) / (plot()->getCulture(ePlayer) + 1)) + 100));
	iStrength /= 100;

	if (GET_PLAYER(ePlayer).getStateReligion() != NO_RELIGION)
	{
		if (isHasReligion(GET_PLAYER(ePlayer).getStateReligion()))
		{
			iStrength *= std::max(0, (GC.getDefineINT("REVOLT_OFFENSE_STATE_RELIGION_MODIFIER") + 100));
			iStrength /= 100;
		}
	}

	if (GET_PLAYER(getOwnerINLINE()).getStateReligion() != NO_RELIGION)
	{
		if (isHasReligion(GET_PLAYER(getOwnerINLINE()).getStateReligion()))
		{
			iStrength *= std::max(0, (GC.getDefineINT("REVOLT_DEFENSE_STATE_RELIGION_MODIFIER") + 100));
			iStrength /= 100;
		}
	}

	return iStrength;
}


int CvCity::cultureGarrison(PlayerTypes ePlayer) const
{
	CLLNode<IDInfo>* pUnitNode;
	CvUnit* pLoopUnit;
	int iGarrison;

	iGarrison = 1;

	pUnitNode = plot()->headUnitNode();

	while (pUnitNode != NULL)
	{
		pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = plot()->nextUnitNode(pUnitNode);

		iGarrison += pLoopUnit->getUnitInfo().getCultureGarrisonValue();
	}

	if (atWar(GET_PLAYER(ePlayer).getTeam(), getTeam()))
	{
		iGarrison *= 2;
	}

	return iGarrison;
}

//Rhye - start
bool CvCity::hasBuilding(BuildingTypes eIndex) const
{
	return (getNumBuilding(eIndex));
}


bool CvCity::hasActiveBuilding(BuildingTypes eIndex) const
{
	return (getNumActiveBuilding(eIndex));
}
//Rhye - end

int CvCity::getNumBuilding(BuildingTypes eIndex) const
{
	FAssertMsg(eIndex != NO_BUILDING, "BuildingType eIndex is expected to not be NO_BUILDING");

	return std::min(GC.getCITY_MAX_NUM_BUILDINGS(), getNumRealBuilding(eIndex) + getNumFreeBuilding(eIndex));
}


int CvCity::getNumActiveBuilding(BuildingTypes eIndex) const
{
	FAssertMsg(eIndex != NO_BUILDING, "BuildingType eIndex is expected to not be NO_BUILDING");

	if (GET_TEAM(getTeam()).isObsoleteBuilding(eIndex))
	{
		return 0;
	}

	return (getNumBuilding(eIndex));
}


bool CvCity::hasActiveWorldWonder() const
{
	int iI;

	for (iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		if (isWorldWonderClass((BuildingClassTypes)(GC.getBuildingInfo((BuildingTypes)iI).getBuildingClassType())))
		{
			if (getNumRealBuilding((BuildingTypes)iI) > 0 && !(GET_TEAM(getTeam()).isObsoleteBuilding((BuildingTypes)iI)))
			{
				return true;
			}
		}
	}

	return false;
}

/************************************************************************************************/
/* UNOFFICIAL_PATCH                       03/04/10                                jdog5000      */
/*                                                                                              */
/* Bugfix                                                                                       */
/************************************************************************************************/
int CvCity::getNumActiveWorldWonders() const
{
	int iI;
	int iCount = 0;

	for (iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		if (isWorldWonderClass((BuildingClassTypes)(GC.getBuildingInfo((BuildingTypes)iI).getBuildingClassType())))
		{
			if (getNumRealBuilding((BuildingTypes)iI) > 0 && !(GET_TEAM(getTeam()).isObsoleteBuilding((BuildingTypes)iI)))
			{
				iCount++;
			}
		}
	}

	return iCount;
}
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/

int CvCity::getReligionCount() const
{
	int iCount;
	int iI;

	iCount = 0;

	for (iI = 0; iI < GC.getNumReligionInfos(); iI++)
	{
		if (isHasReligion((ReligionTypes)iI))
		{
			iCount++;
		}
	}

	return iCount;
}

int CvCity::getCorporationCount() const
{
	int iCount;
	int iI;

	iCount = 0;

	for (iI = 0; iI < GC.getNumCorporationInfos(); iI++)
	{
		if (isHasCorporation((CorporationTypes)iI))
		{
			iCount++;
		}
	}

	return iCount;
}


int CvCity::getID() const
{
	return m_iID;
}


int CvCity::getIndex() const
{
	return (getID() & FLTA_INDEX_MASK);
}


IDInfo CvCity::getIDInfo() const
{
	IDInfo city(getOwnerINLINE(), getID());
	return city;
}


void CvCity::setID(int iID)
{
	m_iID = iID;
}


int CvCity::getX() const
{
	return m_iX;
}


int CvCity::getY() const
{
	return m_iY;
}


bool CvCity::at(int iX,  int iY) const
{
	return ((getX_INLINE() == iX) && (getY_INLINE() == iY));
}


bool CvCity::at(CvPlot* pPlot) const
{
	return (plot() == pPlot);
}


CvPlot* CvCity::plot() const
{
	return GC.getMapINLINE().plotSorenINLINE(getX_INLINE(), getY_INLINE());
}


CvPlotGroup* CvCity::plotGroup(PlayerTypes ePlayer) const
{
	return plot()->getPlotGroup(ePlayer);
}


bool CvCity::isConnectedTo(CvCity* pCity) const
{
	return (plot()->isConnectedTo(pCity) || (getMaxAirlift() > 0 && pCity->getMaxAirlift() > 0)); // Leoreth: airports connect cities
}


bool CvCity::isConnectedToCapital(PlayerTypes ePlayer) const
{
	return plot()->isConnectedToCapital(ePlayer);
}


int CvCity::getArea() const
{
	return plot()->getArea();
}

CvArea* CvCity::area() const
{
	return plot()->area();
}


CvArea* CvCity::waterArea() const
{
	return plot()->waterArea();
}


CvPlot* CvCity::getRallyPlot() const
{
	return GC.getMapINLINE().plotSorenINLINE(m_iRallyX, m_iRallyY);
}


void CvCity::setRallyPlot(CvPlot* pPlot)
{
	if (getRallyPlot() != pPlot)
	{
		if (pPlot != NULL)
		{
			m_iRallyX = pPlot->getX_INLINE();
			m_iRallyY = pPlot->getY_INLINE();
		}
		else
		{
			m_iRallyX = INVALID_PLOT_COORD;
			m_iRallyY = INVALID_PLOT_COORD;
		}

		if (isCitySelected())
		{
			gDLL->getInterfaceIFace()->setDirty(ColoredPlots_DIRTY_BIT, true);
		}
	}
}


int CvCity::getGameTurnFounded() const
{
	return m_iGameTurnFounded;
}


void CvCity::setGameTurnFounded(int iNewValue)
{
	if (getGameTurnFounded() != iNewValue)
	{
		m_iGameTurnFounded = iNewValue;
		FAssert(getGameTurnFounded() >= 0);

		GC.getMapINLINE().updateWorkingCity();
	}
}


int CvCity::getGameTurnAcquired() const
{
	return m_iGameTurnAcquired;
}


void CvCity::setGameTurnAcquired(int iNewValue)
{
	m_iGameTurnAcquired = iNewValue;
	FAssert(getGameTurnAcquired() >= 0);
}


int CvCity::getPopulation() const
{
	return m_iPopulation;
}


void CvCity::setPopulation(int iNewValue)
{
	int iOldPopulation;

	iOldPopulation = getPopulation();

	if (iOldPopulation != iNewValue)
	{
		m_iPopulation = iNewValue;

		FAssert(getPopulation() >= 0);

		GET_PLAYER(getOwnerINLINE()).invalidatePopulationRankCache();

		if (getPopulation() > getHighestPopulation())
		{
			setHighestPopulation(getPopulation());
		}

		area()->changePopulationPerPlayer(getOwnerINLINE(), (getPopulation() - iOldPopulation));
		GET_PLAYER(getOwnerINLINE()).changeTotalPopulation(getPopulation() - iOldPopulation);
		GET_TEAM(getTeam()).changeTotalPopulation(getPopulation() - iOldPopulation);
		GC.getGameINLINE().changeTotalPopulation(getPopulation() - iOldPopulation);

		if (iOldPopulation > 0)
		{
			area()->changePower(getOwnerINLINE(), -(getPopulationPower(iOldPopulation)));
		}
		if (getPopulation() > 0)
		{
			area()->changePower(getOwnerINLINE(), getPopulationPower(getPopulation()));
		}

		plot()->updateYield();

		// Leoreth: population now affects overall maintenance modifier
		//updateMaintenance();
		GET_PLAYER(getOwnerINLINE()).updateMaintenance();

		if (((iOldPopulation == 1) && (getPopulation() > 1)) ||
			  ((getPopulation() == 1) && (iOldPopulation > 1))
			  || ((getPopulation() > iOldPopulation) && (GET_PLAYER(getOwnerINLINE()).getNumCities() <= 2)))
		{
			if (!isHuman())
			{
				AI_setChooseProductionDirty(true);
			}
		}

		GET_PLAYER(getOwnerINLINE()).AI_makeAssignWorkDirty();

		setInfoDirty(true);
		setLayoutDirty(true);

		plot()->plotAction(PUF_makeInfoBarDirty);

		if ((getOwnerINLINE() == GC.getGameINLINE().getActivePlayer()) && isCitySelected())
		{
			gDLL->getInterfaceIFace()->setDirty(SelectionButtons_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(CityScreen_DIRTY_BIT, true);
		}

		//updateGenericBuildings();
	}
}


void CvCity::changePopulation(int iChange)
{
	setPopulation(getPopulation() + iChange);
}


long CvCity::getRealPopulation() const
{
	//return (((long)(pow((float)getPopulation(), 2.8f))) * 1000); //Rhye
	if (GET_PLAYER(getOwnerINLINE()).getCurrentEra() <= 4)
	{
		return (((long)(pow((float)getPopulation(), 3.0f))) * 1000); //Panopticon
	}
	else
	{
		return (((long)(pow((float)getPopulation(), 3.1f))) * 1000); //Panopticon
	}
}

int CvCity::getHighestPopulation() const
{
	return m_iHighestPopulation;
}


void CvCity::setHighestPopulation(int iNewValue)
{
 	m_iHighestPopulation = iNewValue;
	FAssert(getHighestPopulation() >= 0);
}


int CvCity::getWorkingPopulation() const
{
	return m_iWorkingPopulation;
}


void CvCity::changeWorkingPopulation(int iChange)
{
	m_iWorkingPopulation = (m_iWorkingPopulation + iChange);
	FAssert(getWorkingPopulation() >= 0);
}


int CvCity::getSpecialistPopulation() const
{
	return m_iSpecialistPopulation;
}


void CvCity::changeSpecialistPopulation(int iChange)
{
	if (iChange != 0)
	{
		m_iSpecialistPopulation = (m_iSpecialistPopulation + iChange);
		FAssert(getSpecialistPopulation() >= 0);

		GET_PLAYER(getOwnerINLINE()).invalidateYieldRankCache();

		updateCommerce();
	}
}


int CvCity::getNumGreatPeople() const
{
	return m_iNumGreatPeople;
}


void CvCity::changeNumGreatPeople(int iChange)
{
	if (iChange != 0)
	{
		m_iNumGreatPeople = (m_iNumGreatPeople + iChange);
		FAssert(getNumGreatPeople() >= 0);

		updateCommerce();
	}
}


int CvCity::getBaseGreatPeopleRate() const
{
	return m_iBaseGreatPeopleRate;
}


int CvCity::getGreatPeopleRate() const
{
	if (isDisorder())
	{
		return 0;
	}

	//Rhye - start switch
	int baseValue = (getBaseGreatPeopleRate() * getTotalGreatPeopleRateModifier()) / 100;
	int result = baseValue;
	//int iI;

	if (getOwnerINLINE() == GREECE) {
		//Rhye - start UP
		if (GET_PLAYER(getOwnerINLINE()).getCurrentEra() <= 1) //Leoreth: expires after Classical now
			result = (baseValue*250/100);
		//Rhye - end UP
	}
	//switch used to be here, now in CvPlayer::greatPeopleThreshold()

	// Leoreth - Italian UP OLD
	/*
	if (getOwnerINLINE() == ROME && GET_PLAYER(getOwnerINLINE()).isReborn())
	{
	    for (iI = HEROICEPIC; iI < NUM_WONDERS; iI++)
	    {
	        if (hasBuilding((BuildingTypes)iI))
	        {
	            result += GC.getBuildingInfo((BuildingTypes)iI).getCommerceChange(COMMERCE_CULTURE);
	        }
	    }
	}*/

	return result;

	//return ((getBaseGreatPeopleRate() * getTotalGreatPeopleRateModifier()) / 100);
	//Rhye - end
}


int CvCity::getTotalGreatPeopleRateModifier() const
{
	int iModifier;

	iModifier = getGreatPeopleRateModifier();

	iModifier += GET_PLAYER(getOwnerINLINE()).getGreatPeopleRateModifier();

	if (GET_PLAYER(getOwnerINLINE()).getStateReligion() != NO_RELIGION)
	{
		if (isHasReligion(GET_PLAYER(getOwnerINLINE()).getStateReligion()))
		{
			iModifier += GET_PLAYER(getOwnerINLINE()).getStateReligionGreatPeopleRateModifier();
		}
	}

	if (GET_PLAYER(getOwnerINLINE()).isGoldenAge())
	{
		iModifier += GC.getDefineINT("GOLDEN_AGE_GREAT_PEOPLE_MODIFIER");
	}

	return std::max(0, (iModifier + 100));
}


void CvCity::changeBaseGreatPeopleRate(int iChange)
{
	m_iBaseGreatPeopleRate = (m_iBaseGreatPeopleRate + iChange);
	FAssert(getBaseGreatPeopleRate() >= 0);
}


int CvCity::getGreatPeopleRateModifier() const
{
	return m_iGreatPeopleRateModifier;
}


void CvCity::changeGreatPeopleRateModifier(int iChange)
{
	m_iGreatPeopleRateModifier = (m_iGreatPeopleRateModifier + iChange);
}


int CvCity::getGreatPeopleProgress() const
{
	return m_iGreatPeopleProgress;
}


void CvCity::changeGreatPeopleProgress(int iChange)
{
	m_iGreatPeopleProgress = (m_iGreatPeopleProgress + iChange);
	FAssert(getGreatPeopleProgress() >= 0);
}


// BUG - Building Additional Great People - start
/*
 * Returns the total additional great people rate that adding one of the given buildings will provide.
 *
 * Doesn't check if the building can be constructed in this city.
 */
int CvCity::getAdditionalGreatPeopleRateByBuilding(BuildingTypes eBuilding) const
{
	FAssertMsg(eBuilding >= 0, "eBuilding expected to be >= 0");
	FAssertMsg(eBuilding < GC.getNumBuildingInfos(), "eBuilding expected to be < GC.getNumBuildingInfos()");

	int iRate = getBaseGreatPeopleRate();
	int iModifier = getTotalGreatPeopleRateModifier();
	int iExtra = ((iRate + getAdditionalBaseGreatPeopleRateByBuilding(eBuilding)) * (iModifier + getAdditionalGreatPeopleRateModifierByBuilding(eBuilding)) / 100) - (iRate * iModifier / 100);

	return iExtra;
}

/*
 * Returns the additional great people rate that adding one of the given buildings will provide.
 *
 * Doesn't check if the building can be constructed in this city.
 */
int CvCity::getAdditionalBaseGreatPeopleRateByBuilding(BuildingTypes eBuilding) const
{
	FAssertMsg(eBuilding >= 0, "eBuilding expected to be >= 0");
	FAssertMsg(eBuilding < GC.getNumBuildingInfos(), "eBuilding expected to be < GC.getNumBuildingInfos()");

	CvBuildingInfo& kBuilding = GC.getBuildingInfo(eBuilding);
	bool bObsolete = GET_TEAM(getTeam()).isObsoleteBuilding(eBuilding);
	int iExtraRate = 0;

	iExtraRate += kBuilding.getGreatPeopleRateChange();

	// Specialists
	if (!bObsolete)
	{
		for (int iI = 0; iI < GC.getNumSpecialistInfos(); ++iI)
		{
			if (kBuilding.getFreeSpecialistCount((SpecialistTypes)iI) != 0)
			{
				iExtraRate += getAdditionalBaseGreatPeopleRateBySpecialist((SpecialistTypes)iI, kBuilding.getFreeSpecialistCount((SpecialistTypes)iI));
			}
		}
	}

	return iExtraRate;
}

/*
 * Returns the additional great people rate modifier that adding one of the given buildings will provide.
 *
 * Doesn't check if the building can be constructed in this city.
 */
int CvCity::getAdditionalGreatPeopleRateModifierByBuilding(BuildingTypes eBuilding) const
{
	FAssertMsg(eBuilding >= 0, "eBuilding expected to be >= 0");
	FAssertMsg(eBuilding < GC.getNumBuildingInfos(), "eBuilding expected to be < GC.getNumBuildingInfos()");

	CvBuildingInfo& kBuilding = GC.getBuildingInfo(eBuilding);
	bool bObsolete = GET_TEAM(getTeam()).isObsoleteBuilding(eBuilding);
	int iExtraModifier = 0;

	if (!bObsolete)
	{
		iExtraModifier += kBuilding.getGreatPeopleRateModifier();
		iExtraModifier += kBuilding.getGlobalGreatPeopleRateModifier();
	}

	return iExtraModifier;
}
// BUG - Building Additional Great People - end


// BUG - Specialist Additional Great People - start
/*
 * Returns the total additional great people rate that changing the number of the given specialist will provide/remove.
 */
int CvCity::getAdditionalGreatPeopleRateBySpecialist(SpecialistTypes eSpecialist, int iChange) const
{
	int iRate = getBaseGreatPeopleRate();
	int iModifier = getTotalGreatPeopleRateModifier();
	int iExtraRate = getAdditionalBaseGreatPeopleRateBySpecialist(eSpecialist, iChange);

	int iExtra = ((iRate + iExtraRate) * iModifier / 100) - (iRate * iModifier / 100);

	return iExtra;
}

/*
 * Returns the additional great people rate that changing the number of the given specialist will provide/remove.
 */
int CvCity::getAdditionalBaseGreatPeopleRateBySpecialist(SpecialistTypes eSpecialist, int iChange) const
{
	FAssertMsg(eSpecialist >= 0, "eSpecialist expected to be >= 0");
	FAssertMsg(eSpecialist < GC.getNumSpecialistInfos(), "eSpecialist expected to be < GC.getNumSpecialistInfos()");

	return iChange * GC.getSpecialistInfo(eSpecialist).getGreatPeopleRateChange();
}
// BUG - Specialist Additional Great People - end


int CvCity::getNumWorldWonders() const
{
	return m_iNumWorldWonders;
}


void CvCity::changeNumWorldWonders(int iChange)
{
	m_iNumWorldWonders = (m_iNumWorldWonders + iChange);
	FAssert(getNumWorldWonders() >= 0);
}


int CvCity::getNumTeamWonders() const
{
	return m_iNumTeamWonders;
}


void CvCity::changeNumTeamWonders(int iChange)
{
	m_iNumTeamWonders = (m_iNumTeamWonders + iChange);
	FAssert(getNumTeamWonders() >= 0);
}


int CvCity::getNumNationalWonders() const
{
	return m_iNumNationalWonders;
}


void CvCity::changeNumNationalWonders(int iChange)
{
	m_iNumNationalWonders = (m_iNumNationalWonders + iChange);
	FAssert(getNumNationalWonders() >= 0);
}


int CvCity::getNumBuildings() const
{
	return m_iNumBuildings;
}


void CvCity::changeNumBuildings(int iChange)
{
	m_iNumBuildings = (m_iNumBuildings + iChange);
	FAssert(getNumBuildings() >= 0);
}


int CvCity::getGovernmentCenterCount() const
{
	return m_iGovernmentCenterCount;
}


bool CvCity::isGovernmentCenter() const
{
	return (getGovernmentCenterCount() > 0);
}


void CvCity::changeGovernmentCenterCount(int iChange)
{
	if (iChange != 0)
	{
		m_iGovernmentCenterCount = (m_iGovernmentCenterCount + iChange);
		FAssert(getGovernmentCenterCount() >= 0);

		GET_PLAYER(getOwnerINLINE()).updateMaintenance();
	}
}


// BUG - Building Saved Maintenance - start
/*
 * Returns the rounded total additional gold from saved maintenance that adding one of the given buildings will provide.
 *
 * Doesn't check if the building can be constructed in this city.
 */
int CvCity::getSavedMaintenanceByBuilding(BuildingTypes eBuilding) const
{
	return getSavedMaintenanceTimes100ByBuilding(eBuilding) / 100;
}

/*
 * Returns the total additional gold from saved maintenance times 100 that adding one of the given buildings will provide.
 *
 * Doesn't check if the building can be constructed in this city.
 */
int CvCity::getSavedMaintenanceTimes100ByBuilding(BuildingTypes eBuilding) const
{
	FAssertMsg(eBuilding >= 0, "eBuilding expected to be >= 0");
	FAssertMsg(eBuilding < GC.getNumBuildingInfos(), "eBuilding expected to be < GC.getNumBuildingInfos()");

	CvBuildingInfo& kBuilding = GC.getBuildingInfo(eBuilding);
	int iModifier = kBuilding.getMaintenanceModifier();
	if (iModifier != 0 && !isDisorder() && !isWeLoveTheKingDay() && (getPopulation() > 0))
	{
		int iNewMaintenance = calculateBaseMaintenanceTimes100() * std::max(0, getMaintenanceModifier() + iModifier + 100) / 100;
		return std::max(0, getMaintenanceTimes100() - iNewMaintenance);
	}

	return 0;
}
// BUG - Building Saved Maintenance - end

int CvCity::getMaintenance() const
{
	return m_iMaintenance / 100;
}

int CvCity::getMaintenanceTimes100() const
{
	return m_iMaintenance;
}


void CvCity::updateMaintenance()
{
	int iOldMaintenance;
	int iNewMaintenance;

	iOldMaintenance = getMaintenanceTimes100();

	iNewMaintenance = 0;

	if (!isDisorder() && !isWeLoveTheKingDay() && (getPopulation() > 0))
	{
		iNewMaintenance = (calculateBaseMaintenanceTimes100() * std::max(0, (getMaintenanceModifier() + 100))) / 100;
	}

	if (iOldMaintenance != iNewMaintenance)
	{
		FAssert(iOldMaintenance >= 0);
		FAssert(iNewMaintenance >= 0);

		m_iMaintenance = iNewMaintenance;
		FAssert(getMaintenance() >= 0);

		GET_PLAYER(getOwnerINLINE()).changeTotalMaintenance(getMaintenanceTimes100() - iOldMaintenance);
	}
}

int CvCity::calculateDistanceMaintenance() const
{
	return (calculateDistanceMaintenanceTimes100() / 100);
}

int CvCity::calculateDistanceMaintenanceTimes100() const
{
	CvCity* pLoopCity;
	int iWorstCityMaintenance;
	int iBestCapitalMaintenance;
	int iTempMaintenance;
	int iDistance;
	int iLoop;

	iWorstCityMaintenance = 0;
	iBestCapitalMaintenance = MAX_INT;

	for (pLoopCity = GET_PLAYER(getOwnerINLINE()).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER(getOwnerINLINE()).nextCity(&iLoop))
	{
		iDistance = plotDistance(getX_INLINE(), getY_INLINE(), pLoopCity->getX_INLINE(), pLoopCity->getY_INLINE());

		// Leoreth: English UP: distance capped at 10
		if (getOwnerINLINE() == ENGLAND)
		{
			iDistance = std::min(10, iDistance);
		}

		iTempMaintenance = 100 * (GC.getDefineINT("MAX_DISTANCE_CITY_MAINTENANCE") * iDistance);

		iTempMaintenance *= (getPopulation() + 7);
		iTempMaintenance /= 10;

		iTempMaintenance *= std::max(0, (GET_PLAYER(getOwnerINLINE()).getDistanceMaintenanceModifier() + 100));
		iTempMaintenance /= 100;

		iTempMaintenance *= GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getDistanceMaintenancePercent();
		iTempMaintenance /= 100;

		//iTempMaintenance *= GC.getHandicapInfo(getHandicapType()).getDistanceMaintenancePercent(); //Rhye
		iTempMaintenance *= GC.getHandicapInfo(getHandicapType()).getDistanceMaintenancePercentByID(getOwnerINLINE()); //Rhye
		iTempMaintenance /= 100;

		iTempMaintenance /= GC.getMapINLINE().maxPlotDistance();

		iWorstCityMaintenance = std::max(iWorstCityMaintenance, iTempMaintenance);

		if (pLoopCity->isGovernmentCenter())
		{
			iBestCapitalMaintenance = std::min(iBestCapitalMaintenance, iTempMaintenance);
		}
	}

	iTempMaintenance = std::min(iWorstCityMaintenance, iBestCapitalMaintenance);
	FAssert(iTempMaintenance >= 0);

	return iTempMaintenance;
}

int CvCity::calculateNumCitiesMaintenance() const
{
	return (calculateNumCitiesMaintenanceTimes100() / 100);
}

int CvCity::calculateNumCitiesMaintenanceTimes100() const
{
	int iNumCitiesPercent = 100;

	iNumCitiesPercent *= GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getNumCitiesMaintenancePercent();
	iNumCitiesPercent /= 100;

	//iNumCitiesPercent *= GC.getHandicapInfo(getHandicapType()).getNumCitiesMaintenancePercent(); //Rhye
	iNumCitiesPercent *= GC.getHandicapInfo(getHandicapType()).getNumCitiesMaintenancePercentByID(getOwnerINLINE()); //Rhye
	iNumCitiesPercent /= 100;

	int iNumVassalCities = 0;
	for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; iPlayer++)
	{
		CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iPlayer);
		if (kLoopPlayer.getTeam() != getTeam() && GET_TEAM(kLoopPlayer.getTeam()).isVassal(getTeam()))
		{
			iNumVassalCities += kLoopPlayer.getNumCities();
		}
	}
	iNumVassalCities /= std::max(1, GET_TEAM(getTeam()).getNumMembers());

	int iNumCitiesMaintenance = (GET_PLAYER(getOwnerINLINE()).getNumCities() + iNumVassalCities) * iNumCitiesPercent;

	//iNumCitiesMaintenance = std::min(iNumCitiesMaintenance, GC.getHandicapInfo(getHandicapType()).getMaxNumCitiesMaintenance() * 100);

	// Rhye: modify by city size
	iNumCitiesPercent *= (getPopulation() + 9);
	iNumCitiesPercent /= 10;

	// Leoreth: apply large empire penalty here
	int iSizeThreshold = 6 + 3 * GET_PLAYER(getOwnerINLINE()).getCurrentEra();
	int iMultiplier = 5; //(GET_PLAYER(getOwnerINLINE()).isHuman()) ? 10 : 5;
	int iNumCities = GET_PLAYER(getOwnerINLINE()).getTotalPopulation() / iSizeThreshold;

	if (iNumCities > 10)
	{
		iNumCitiesMaintenance *= 100 + iMultiplier * (iNumCities - 10);
		iNumCitiesMaintenance /= 100;
	}

	iNumCitiesMaintenance *= std::max(0, (GET_PLAYER(getOwnerINLINE()).getNumCitiesMaintenanceModifier() + 100));
	iNumCitiesMaintenance /= 100;

	FAssert(iNumCitiesMaintenance >= 0);

	return iNumCitiesMaintenance;
}


int CvCity::calculateColonyMaintenance() const
{
	return (calculateColonyMaintenanceTimes100() / 100);
}

int CvCity::calculateColonyMaintenanceTimes100() const
{
	if (GC.getGameINLINE().isOption(GAMEOPTION_NO_VASSAL_STATES))
	{
		return 0;
	}

	CvCity* pCapital = GET_PLAYER(getOwnerINLINE()).getCapitalCity();
	if (pCapital && pCapital->area() == area())
	{
		return 0;
	}

	//Rhye - start switch
	switch (getOwnerINLINE())
	{
		case INDEPENDENT:
		case INDEPENDENT2:
		case NATIVE:
		case CELTIA: //late start too, as Byzantium stands in the junction point of 3 continents
		case SELJUKS:
			return 0;
	}
	//Rhye - end

	int iNumCitiesPercent = 100;

	iNumCitiesPercent *= (getPopulation() + 17);
	iNumCitiesPercent /= 18;

	iNumCitiesPercent *= GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getColonyMaintenancePercent();
	iNumCitiesPercent /= 100;

	iNumCitiesPercent *= GC.getHandicapInfo(getHandicapType()).getColonyMaintenancePercent();
	iNumCitiesPercent /= 100;

	int iNumCities = (area()->getCitiesPerPlayer(getOwnerINLINE()) - 1) * iNumCitiesPercent;

	int iMaintenance = (iNumCities * iNumCities) / 100;

	// influenced by English UP here
	iMaintenance = std::min(iMaintenance, (GC.getHandicapInfo(getHandicapType()).getMaxColonyMaintenance() * calculateDistanceMaintenanceTimes100()) / 100);

	FAssert(iMaintenance >= 0);

	return iMaintenance;
}


int CvCity::calculateCorporationMaintenance() const
{
	return (calculateCorporationMaintenanceTimes100() / 100);
}

int CvCity::calculateCorporationMaintenanceTimes100() const
{
	int iMaintenance = 0;

	for (int iCorporation = 0; iCorporation < GC.getNumCorporationInfos(); ++iCorporation)
	{
		if (isActiveCorporation((CorporationTypes)iCorporation))
		{
			iMaintenance += calculateCorporationMaintenanceTimes100((CorporationTypes)iCorporation);
		}
	}

	FAssert(iMaintenance >= 0);

	return iMaintenance;
}

int CvCity::calculateCorporationMaintenanceTimes100(CorporationTypes eCorporation) const
{
	int iMaintenance = 0;

	for (int iCommerce = 0; iCommerce < NUM_COMMERCE_TYPES; ++iCommerce)
	{
		iMaintenance += 100 * GC.getCorporationInfo(eCorporation).getHeadquarterCommerce(iCommerce);
	}

	int iNumBonuses = 0;
	for (int i = 0; i < GC.getNUM_CORPORATION_PREREQ_BONUSES(); ++i)
	{
		BonusTypes eBonus = (BonusTypes)GC.getCorporationInfo(eCorporation).getPrereqBonus(i);
		if (NO_BONUS != eBonus)
		{
			iNumBonuses += getNumBonuses(eBonus);
		}
	}

	int iBonusMaintenance = GC.getCorporationInfo(eCorporation).getMaintenance() * iNumBonuses;
	iBonusMaintenance *= GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getCorporationMaintenancePercent();
	iBonusMaintenance /= 100;
	iMaintenance += iBonusMaintenance;

	iMaintenance *= (getPopulation() + 17);
	iMaintenance /= 18;

	iMaintenance *= GC.getHandicapInfo(getHandicapType()).getCorporationMaintenancePercent();
	iMaintenance /= 100;

	iMaintenance *= std::max(0, (GET_PLAYER(getOwnerINLINE()).getCorporationMaintenanceModifier() + 100));
	iMaintenance /= 100;

	int iInflation = GET_PLAYER(getOwnerINLINE()).calculateInflationRate() + 100;
	if (iInflation > 0)
	{
		iMaintenance *= 100;
		iMaintenance /= iInflation;
	}

	FAssert(iMaintenance >= 0);

	return iMaintenance;
}


int CvCity::calculateBaseMaintenanceTimes100() const
{
	return (calculateDistanceMaintenanceTimes100() + calculateNumCitiesMaintenanceTimes100() + calculateColonyMaintenanceTimes100() + calculateCorporationMaintenanceTimes100());
}


int CvCity::getMaintenanceModifier() const
{
	return m_iMaintenanceModifier;
}


void CvCity::changeMaintenanceModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iMaintenanceModifier = (m_iMaintenanceModifier + iChange);

		updateMaintenance();
	}
}


int CvCity::getWarWearinessModifier() const
{
	return m_iWarWearinessModifier;
}


void CvCity::changeWarWearinessModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iWarWearinessModifier = (m_iWarWearinessModifier + iChange);

		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getHurryAngerModifier() const
{
	return m_iHurryAngerModifier;
}


void CvCity::changeHurryAngerModifier(int iChange)
{
	if (0 != iChange)
	{
		int iRatio = 0;

		if (m_iHurryAngerTimer > 0)
		{
			iRatio = (100 * (m_iHurryAngerTimer - 1)) / std::max(1, 100 + getHurryAngerModifier());
		}

		m_iHurryAngerModifier += iChange;

		if (m_iHurryAngerTimer > 0)
		{
			m_iHurryAngerTimer = (iRatio * std::max(1, 100 + getHurryAngerModifier())) / 100 + 1;
		}
	}
}


int CvCity::getHealRate() const
{
	return m_iHealRate;
}


void CvCity::changeHealRate(int iChange)
{
	m_iHealRate = (m_iHealRate + iChange);
	FAssert(getHealRate() >= 0);
}

int CvCity::getEspionageHealthCounter() const
{
	return m_iEspionageHealthCounter;
}


void CvCity::changeEspionageHealthCounter(int iChange)
{
	if (iChange != 0)
	{
		m_iEspionageHealthCounter += iChange;
	}
}

int CvCity::getEspionageHappinessCounter() const
{
	return m_iEspionageHappinessCounter;
}


void CvCity::changeEspionageHappinessCounter(int iChange)
{
	if (iChange != 0)
	{
		m_iEspionageHappinessCounter += iChange;
	}
}


int CvCity::getFreshWaterGoodHealth() const
{
	return m_iFreshWaterGoodHealth;
}


int CvCity::getFreshWaterBadHealth() const
{
	return m_iFreshWaterBadHealth;
}


void CvCity::updateFreshWaterHealth()
{
	int iNewGoodHealth;
	int iNewBadHealth;

	iNewGoodHealth = 0;
	iNewBadHealth = 0;

	if (plot()->isFreshWater())
	{
		if (GC.getDefineINT("FRESH_WATER_HEALTH_CHANGE") > 0)
		{
			iNewGoodHealth += GC.getDefineINT("FRESH_WATER_HEALTH_CHANGE");
		}
		else
		{
			iNewBadHealth += GC.getDefineINT("FRESH_WATER_HEALTH_CHANGE");
		}
	}

	if ((getFreshWaterGoodHealth() != iNewGoodHealth) || (getFreshWaterBadHealth() != iNewBadHealth))
	{
		m_iFreshWaterGoodHealth = iNewGoodHealth;
		m_iFreshWaterBadHealth = iNewBadHealth;
		FAssert(getFreshWaterGoodHealth() >= 0);
		FAssert(getFreshWaterBadHealth() <= 0);

		AI_setAssignWorkDirty(true);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);
		}
	}
}


int CvCity::getFeatureGoodHealth() const
{
	return m_iFeatureGoodHealth;
}


int CvCity::getFeatureBadHealth() const
{
	return m_iFeatureBadHealth;
}


void CvCity::updateFeatureHealth()
{
	CvPlot* pLoopPlot;
	FeatureTypes eFeature;
	int iNewGoodHealth;
	int iNewBadHealth;
	int iI;

	iNewGoodHealth = 0;
	iNewBadHealth = 0;

	for (iI = 0; iI < NUM_CITY_PLOTS; iI++)
	{
		pLoopPlot = getCityIndexPlot(iI);

		if (pLoopPlot != NULL)
		{
			eFeature = pLoopPlot->getFeatureType();

			if (eFeature != NO_FEATURE)
			{
				if (GC.getFeatureInfo(eFeature).getHealthPercent() > 0)
				{
					iNewGoodHealth += GC.getFeatureInfo(eFeature).getHealthPercent();
				}
				else
				{
					// Leoreth: Congo UP: no unhealthiness from jungle and marsh
					if (!(getOwnerINLINE() == CONGO && (eFeature == GC.getInfoTypeForString("FEATURE_JUNGLE") || eFeature == GC.getInfoTypeForString("FEATURE_MARSH"))))
						iNewBadHealth += GC.getFeatureInfo(eFeature).getHealthPercent();
				}
			}
		}
	}

	iNewGoodHealth /= 100;
	iNewBadHealth /= 100;

	if ((getFeatureGoodHealth() != iNewGoodHealth) || (getFeatureBadHealth() != iNewBadHealth))
	{
		m_iFeatureGoodHealth = iNewGoodHealth;
		m_iFeatureBadHealth = iNewBadHealth;
		FAssert(getFeatureGoodHealth() >= 0);
		FAssert(getFeatureBadHealth() <= 0);

		AI_setAssignWorkDirty(true);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);
		}
	}
}


int CvCity::getBuildingGoodHealth() const
{
	return m_iBuildingGoodHealth;
}


int CvCity::getBuildingBadHealth() const
{
	return m_iBuildingBadHealth;
}


int CvCity::getBuildingHealth(BuildingTypes eBuilding) const
{
	int iHealth = getBuildingGoodHealth(eBuilding);

	if (!isBuildingOnlyHealthy())
	{
		iHealth += getBuildingBadHealth(eBuilding);
	}

	return iHealth;
}

int CvCity::getBuildingGoodHealth(BuildingTypes eBuilding) const
{
	int iHealth = std::max(0, GC.getBuildingInfo(eBuilding).getHealth());
	iHealth += std::max(0, getBuildingHealthChange((BuildingClassTypes)GC.getBuildingInfo(eBuilding).getBuildingClassType()));
	iHealth += std::max(0, GET_PLAYER(getOwnerINLINE()).getExtraBuildingHealth(eBuilding));

	return iHealth;
}

int CvCity::getBuildingBadHealth(BuildingTypes eBuilding) const
{
	if (isBuildingOnlyHealthy())
	{
		return 0;
	}

	int iHealth = std::min(0, GC.getBuildingInfo(eBuilding).getHealth());
	iHealth += std::min(0, getBuildingHealthChange((BuildingClassTypes)GC.getBuildingInfo(eBuilding).getBuildingClassType()));
	iHealth += std::min(0, GET_PLAYER(getOwnerINLINE()).getExtraBuildingHealth(eBuilding));

	return iHealth;
}

void CvCity::changeBuildingGoodHealth(int iChange)
{
	if (iChange != 0)
	{
		m_iBuildingGoodHealth = (m_iBuildingGoodHealth + iChange);
		FAssert(getBuildingGoodHealth() >= 0);

		AI_setAssignWorkDirty(true);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);
		}
	}
}


void CvCity::changeBuildingBadHealth(int iChange)
{
	if (iChange != 0)
	{
		m_iBuildingBadHealth += iChange;
		FAssert(getBuildingBadHealth() <= 0);

		AI_setAssignWorkDirty(true);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);
		}
	}
}


int CvCity::getPowerGoodHealth() const
{
	return m_iPowerGoodHealth;
}


int CvCity::getPowerBadHealth() const
{
	return m_iPowerBadHealth;
}


void CvCity::updatePowerHealth()
{
	int iNewGoodHealth;
	int iNewBadHealth;

	iNewGoodHealth = 0;
	iNewBadHealth = 0;

	if (isPower())
	{
		int iPowerHealth = GC.getDefineINT("POWER_HEALTH_CHANGE");
		if (iPowerHealth > 0)
		{
			iNewGoodHealth += iPowerHealth;
		}
		else
		{
			iNewBadHealth += iPowerHealth;
		}
	}

	if (isDirtyPower())
	{
		int iDirtyPowerHealth = GC.getDefineINT("DIRTY_POWER_HEALTH_CHANGE");
		if (iDirtyPowerHealth > 0)
		{
			iNewGoodHealth += iDirtyPowerHealth;
		}
		else
		{
			iNewBadHealth += iDirtyPowerHealth;
		}
	}

	if ((getPowerGoodHealth() != iNewGoodHealth) || (getPowerBadHealth() != iNewBadHealth))
	{
		m_iPowerGoodHealth = iNewGoodHealth;
		m_iPowerBadHealth = iNewBadHealth;
		FAssert(getPowerGoodHealth() >= 0);
		FAssert(getPowerBadHealth() <= 0);

		AI_setAssignWorkDirty(true);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);
		}
	}
}


int CvCity::getBonusGoodHealth() const
{
	return m_iBonusGoodHealth;
}


int CvCity::getBonusBadHealth() const
{
	return m_iBonusBadHealth;
}


void CvCity::changeBonusGoodHealth(int iChange)
{
	if (iChange != 0)
	{
		m_iBonusGoodHealth += iChange;
		FAssert(getBonusGoodHealth() >= 0);

		FAssertMsg(getBonusGoodHealth() >= 0, "getBonusGoodHealth is expected to be >= 0");

		AI_setAssignWorkDirty(true);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);
		}
	}
}


void CvCity::changeBonusBadHealth(int iChange)
{
	if (iChange != 0)
	{
		m_iBonusBadHealth += iChange;
		FAssert(getBonusBadHealth() <= 0);

		FAssertMsg(getBonusBadHealth() <= 0, "getBonusBadHealth is expected to be <= 0");

		AI_setAssignWorkDirty(true);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);
		}
	}
}


int CvCity::getMilitaryHappinessUnits() const
{
	int iMilitaryHappinessLimit = GET_PLAYER(getOwnerINLINE()).getMilitaryHappinessLimit();

	if (iMilitaryHappinessLimit > 0)
	{
		return std::min(m_iMilitaryHappinessUnits, iMilitaryHappinessLimit);
	}
	else
	{
		return m_iMilitaryHappinessUnits;
	}
}


int CvCity::getMilitaryHappiness() const
{
	return (getMilitaryHappinessUnits() * GET_PLAYER(getOwnerINLINE()).getHappyPerMilitaryUnit());
}


void CvCity::changeMilitaryHappinessUnits(int iChange)
{
	if (iChange != 0)
	{
		m_iMilitaryHappinessUnits = (m_iMilitaryHappinessUnits + iChange);
		FAssert(getMilitaryHappinessUnits() >= 0);

		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getBuildingGoodHappiness() const
{
	return m_iBuildingGoodHappiness;
}


int CvCity::getBuildingBadHappiness() const
{
	return m_iBuildingBadHappiness;
}


int CvCity::getBuildingHappiness(BuildingTypes eBuilding) const
{
	int iHappiness;
	int iI;

	iHappiness = GC.getBuildingInfo(eBuilding).getHappiness();

	if (GC.getBuildingInfo(eBuilding).getReligionType() != NO_RELIGION)
	{
		if (GC.getBuildingInfo(eBuilding).getReligionType() == GET_PLAYER(getOwnerINLINE()).getStateReligion())
		{
			iHappiness += GC.getBuildingInfo(eBuilding).getStateReligionHappiness();
		}
	}

	iHappiness += GET_PLAYER(getOwnerINLINE()).getExtraBuildingHappiness(eBuilding);

	for (iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
	{
		iHappiness += ((GC.getBuildingInfo(eBuilding).getCommerceHappiness(iI) * GET_PLAYER(getOwnerINLINE()).getCommercePercent((CommerceTypes)iI)) / 100);
	}

	iHappiness += getBuildingHappyChange((BuildingClassTypes)GC.getBuildingInfo(eBuilding).getBuildingClassType());

	return iHappiness;
}


void CvCity::changeBuildingGoodHappiness(int iChange)
{
	if (iChange != 0)
	{
		m_iBuildingGoodHappiness = (m_iBuildingGoodHappiness + iChange);
		FAssert(getBuildingGoodHappiness() >= 0);

		AI_setAssignWorkDirty(true);
	}
}


void CvCity::changeBuildingBadHappiness(int iChange)
{
	if (iChange != 0)
	{
		m_iBuildingBadHappiness = (m_iBuildingBadHappiness + iChange);
		FAssert(getBuildingBadHappiness() <= 0);

		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getExtraBuildingGoodHappiness() const
{
	return m_iExtraBuildingGoodHappiness;
}


int CvCity::getExtraBuildingBadHappiness() const
{
	return m_iExtraBuildingBadHappiness;
}


void CvCity::updateExtraBuildingHappiness()
{
	int iNewExtraBuildingGoodHappiness;
	int iNewExtraBuildingBadHappiness;
	int iChange;
	int iI;

	iNewExtraBuildingGoodHappiness = 0;
	iNewExtraBuildingBadHappiness = 0;

	for (iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		iChange = getNumActiveBuilding((BuildingTypes)iI) * GET_PLAYER(getOwnerINLINE()).getExtraBuildingHappiness((BuildingTypes)iI);

		if (iChange > 0)
		{
			iNewExtraBuildingGoodHappiness += iChange;
		}
		else
		{
			iNewExtraBuildingBadHappiness += iChange;
		}
	}

	if (getExtraBuildingGoodHappiness() != iNewExtraBuildingGoodHappiness)
	{
		m_iExtraBuildingGoodHappiness = iNewExtraBuildingGoodHappiness;
		FAssert(getExtraBuildingGoodHappiness() >= 0);

		AI_setAssignWorkDirty(true);
	}

	if (getExtraBuildingBadHappiness() != iNewExtraBuildingBadHappiness)
	{
		m_iExtraBuildingBadHappiness = iNewExtraBuildingBadHappiness;
		FAssert(getExtraBuildingBadHappiness() <= 0);

		AI_setAssignWorkDirty(true);
	}
}

// BUG - Building Additional Happiness - start
/*
 * Returns the total additional happiness that adding one of the given buildings will provide.
 *
 * Doesn't check if the building can be constructed in this city.
 */
int CvCity::getAdditionalHappinessByBuilding(BuildingTypes eBuilding) const
{
	int iGood = 0, iBad = 0, iAngryPop = 0;
	return getAdditionalHappinessByBuilding(eBuilding, iGood, iBad, iAngryPop);
}

/*
 * Returns the total additional happiness that adding one of the given buildings will provide
 * and sets the good and bad levels individually and any resulting additional angry population.
 *
 * Doesn't reset iGood or iBad to zero.
 * Doesn't check if the building can be constructed in this city.
 */
int CvCity::getAdditionalHappinessByBuilding(BuildingTypes eBuilding, int& iGood, int& iBad, int& iAngryPop) const
{
	FAssertMsg(eBuilding >= 0, "eBuilding expected to be >= 0");
	FAssertMsg(eBuilding < GC.getNumBuildingInfos(), "eBuilding expected to be < GC.getNumBuildingInfos()");

	CvBuildingInfo& kBuilding = GC.getBuildingInfo(eBuilding);
	int iI;
	int iStarting = iGood - iBad;
	int iStartingBad = iBad;

	// Basic
	addGoodOrBad(kBuilding.getHappiness(), iGood, iBad);

	// Building Class
	addGoodOrBad(getBuildingHappyChange((BuildingClassTypes)kBuilding.getBuildingClassType()), iGood, iBad);

	// Other Building Classes
	CvCivilizationInfo& kCivilization = GC.getCivilizationInfo(getCivilizationType());
	for (iI = 0; iI < GC.getNumBuildingClassInfos(); iI++)
	{
		int iBuildingHappinessChanges = kBuilding.getBuildingHappinessChanges(iI);
		if (iBuildingHappinessChanges != 0)
		{
			BuildingTypes eLoopBuilding = (BuildingTypes)kCivilization.getCivilizationBuildings(iI);
			if (eLoopBuilding != NO_BUILDING)
			{
				addGoodOrBad(iBuildingHappinessChanges * (getNumBuilding(eLoopBuilding) + (eBuilding == eLoopBuilding ? 1 : 0)), iGood, iBad);
			}
		}
	}

	// Player Building
	addGoodOrBad(GET_PLAYER(getOwnerINLINE()).getExtraBuildingHappiness(eBuilding), iGood, iBad);

	// Area
	addGoodOrBad(kBuilding.getAreaHappiness(), iGood, iBad);

	// Global
	addGoodOrBad(kBuilding.getGlobalHappiness(), iGood, iBad);

	// Religion
	if (kBuilding.getReligionType() != NO_RELIGION && kBuilding.getReligionType() == GET_PLAYER(getOwnerINLINE()).getStateReligion())
	{
		iGood += kBuilding.getStateReligionHappiness();
	}

	// Bonus
	for (iI = 0; iI < GC.getNumBonusInfos(); iI++)
	{
		if ((hasBonus((BonusTypes)iI) || kBuilding.getFreeBonus() == iI) && kBuilding.getNoBonus() != iI)
		{
			addGoodOrBad(kBuilding.getBonusHappinessChanges(iI), iGood, iBad);
		}
	}

	// Commerce
	for (iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
	{
		addGoodOrBad(kBuilding.getCommerceHappiness(iI) * GET_PLAYER(getOwnerINLINE()).getCommercePercent((CommerceTypes)iI) / 100, iGood, iBad);
	}

	// War Weariness Modifier
	int iWarWearinessModifier = kBuilding.getWarWearinessModifier() + kBuilding.getGlobalWarWearinessModifier();
	if (iWarWearinessModifier != 0)
	{
		int iBaseAngerPercent = 0;

		iBaseAngerPercent += getOvercrowdingPercentAnger();
		iBaseAngerPercent += getNoMilitaryPercentAnger();
		iBaseAngerPercent += getCulturePercentAnger();
		iBaseAngerPercent += getReligionPercentAnger();
		iBaseAngerPercent += getHurryPercentAnger();
		iBaseAngerPercent += getConscriptPercentAnger();
		iBaseAngerPercent += getDefyResolutionPercentAnger();
		for (iI = 0; iI < GC.getNumCivicInfos(); iI++)
		{
			iBaseAngerPercent += GET_PLAYER(getOwnerINLINE()).getCivicPercentAnger((CivicTypes)iI);
		}

		int iCurrentAngerPercent = iBaseAngerPercent + getWarWearinessPercentAnger();
		int iCurrentUnhappiness = iCurrentAngerPercent * getPopulation() / GC.getPERCENT_ANGER_DIVISOR();

		int iNewWarAngerPercent = GET_PLAYER(getOwnerINLINE()).getWarWearinessPercentAnger();
		iNewWarAngerPercent *= std::max(0, (iWarWearinessModifier + getWarWearinessModifier() + GET_PLAYER(getOwnerINLINE()).getWarWearinessModifier() + 100));
		iNewWarAngerPercent /= 100;
		int iNewAngerPercent = iBaseAngerPercent + iNewWarAngerPercent;
		int iNewUnhappiness = iNewAngerPercent * getPopulation() / GC.getPERCENT_ANGER_DIVISOR();

		iBad += iNewUnhappiness - iCurrentUnhappiness;
	}

	// No Unhappiness
	if (kBuilding.isNoUnhappiness())
	{
		// override extra unhappiness and completely negate all existing unhappiness
		iBad = iStartingBad - unhappyLevel();
	}

	// Effect on Angry Population
	int iHappy = happyLevel();
	int iUnhappy = unhappyLevel();
	int iPop = getPopulation();
	iAngryPop += range((iUnhappy + iBad) - (iHappy + iGood), 0, iPop) - range(iUnhappy - iHappy, 0, iPop);

	return iGood - iBad - iStarting;
}


/*
 * Returns the total additional health that adding one of the given buildings will provide.
 *
 * Doesn't check if the building can be constructed in this city.
 */
int CvCity::getAdditionalHealthByBuilding(BuildingTypes eBuilding) const
{
	int iGood = 0, iBad = 0, iSpoiledFood = 0;
	return getAdditionalHealthByBuilding(eBuilding, iGood, iBad, iSpoiledFood);
}

/*
 * Returns the total additional health that adding one of the given buildings will provide
 * and sets the good and bad levels individually and any resulting additional spoiled food.
 *
 * Doesn't reset iGood or iBad to zero.
 * Doesn't check if the building can be constructed in this city.
 */
int CvCity::getAdditionalHealthByBuilding(BuildingTypes eBuilding, int& iGood, int& iBad, int& iSpoiledFood) const
{
	FAssertMsg(eBuilding >= 0, "eBuilding expected to be >= 0");
	FAssertMsg(eBuilding < GC.getNumBuildingInfos(), "eBuilding expected to be < GC.getNumBuildingInfos()");

	CvBuildingInfo& kBuilding = GC.getBuildingInfo(eBuilding);
	int iI;
	int iStarting = iGood - iBad;
	int iStartingBad = iBad;

	// Basic
	addGoodOrBad(kBuilding.getHealth(), iGood, iBad);

	// Building Class
	addGoodOrBad(getBuildingHealthChange((BuildingClassTypes)kBuilding.getBuildingClassType()), iGood, iBad);

	// Player Building
	addGoodOrBad(GET_PLAYER(getOwnerINLINE()).getExtraBuildingHealth(eBuilding), iGood, iBad);

	// Area
	addGoodOrBad(kBuilding.getAreaHealth(), iGood, iBad);

	// Global
	addGoodOrBad(kBuilding.getGlobalHealth(), iGood, iBad);

	// No Unhealthiness from Buildings
	if (isBuildingOnlyHealthy())
	{
		// undo bad from this building
		iBad = iStartingBad;
	}
	if (kBuilding.isBuildingOnlyHealthy())
	{
		// undo bad from this and all existing buildings
		iBad = iStartingBad + totalBadBuildingHealth();
	}

	// Bonus
	for (iI = 0; iI < GC.getNumBonusInfos(); iI++)
	{
		if ((hasBonus((BonusTypes)iI) || kBuilding.getFreeBonus() == iI) && kBuilding.getNoBonus() != iI)
		{
			addGoodOrBad(kBuilding.getBonusHealthChanges(iI), iGood, iBad);
		}
	}

	// Power
	if (kBuilding.isPower() || kBuilding.isAreaCleanPower() || (kBuilding.getPowerBonus() != NO_BONUS && hasBonus((BonusTypes)kBuilding.getPowerBonus())))
	{
		// adding power
		if (!isPower())
		{
			addGoodOrBad(GC.getDefineINT("POWER_HEALTH_CHANGE"), iGood, iBad);

			// adding dirty power
			if (kBuilding.isDirtyPower())
			{
				addGoodOrBad(GC.getDefineINT("DIRTY_POWER_HEALTH_CHANGE"), iGood, iBad);
			}
		}
		else
		{
			// replacing dirty power with clean power
			if (isDirtyPower() && !kBuilding.isDirtyPower())
			{
				subtractGoodOrBad(GC.getDefineINT("DIRTY_POWER_HEALTH_CHANGE"), iGood, iBad);
			}
		}
	}

	// No Unhealthiness from Population
	if (kBuilding.isNoUnhealthyPopulation())
	{
		iBad -= getPopulation();
	}

	// Effect on Spoiled Food
	int iHealthy = goodHealth();
	int iUnhealthy = badHealth();
	iSpoiledFood -= std::min(0, (iHealthy + iGood) - (iUnhealthy + iBad)) - std::min(0, iHealthy - iUnhealthy);

	return iGood - iBad - iStarting;
}

/*
 * Adds iValue to iGood if it is positive or its negative to iBad if it is negative.
 */
void addGoodOrBad(int iValue, int& iGood, int& iBad)
{
	if (iValue > 0)
	{
		iGood += iValue;
	}
	else if (iValue < 0)
	{
		iBad -= iValue;
	}
}

/*
 * Subtracts iValue from iGood if it is positive or its negative from iBad if it is negative.
 */
void subtractGoodOrBad(int iValue, int& iGood, int& iBad)
{
	if (iValue > 0)
	{
		iGood -= iValue;
	}
	else if (iValue < 0)
	{
		iBad += iValue;
	}
}
// BUG - Building Additional Happiness - end


int CvCity::getExtraBuildingGoodHealth() const
{
	return m_iExtraBuildingGoodHealth;
}


int CvCity::getExtraBuildingBadHealth() const
{
	return m_iExtraBuildingBadHealth;
}


void CvCity::updateExtraBuildingHealth()
{
	int iNewExtraBuildingGoodHealth = 0;
	int iNewExtraBuildingBadHealth = 0;
	int iChange;
	int iI;

	for (iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		iChange = getNumActiveBuilding((BuildingTypes)iI) * GET_PLAYER(getOwnerINLINE()).getExtraBuildingHealth((BuildingTypes)iI);

		if (iChange > 0)
		{
			iNewExtraBuildingGoodHealth += iChange;
		}
		else
		{
			iNewExtraBuildingBadHealth += iChange;
		}
	}

	if (getExtraBuildingGoodHealth() != iNewExtraBuildingGoodHealth)
	{
		m_iExtraBuildingGoodHealth = iNewExtraBuildingGoodHealth;
		FAssert(getExtraBuildingGoodHealth() >= 0);

		AI_setAssignWorkDirty(true);
	}

	if (getExtraBuildingBadHealth() != iNewExtraBuildingBadHealth)
	{
		m_iExtraBuildingBadHealth = iNewExtraBuildingBadHealth;
		FAssert(getExtraBuildingBadHealth() <= 0);

		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getFeatureGoodHappiness() const
{
	return m_iFeatureGoodHappiness;
}


int CvCity::getFeatureBadHappiness() const
{
	return m_iFeatureBadHappiness;
}


void CvCity::updateFeatureHappiness()
{
	int iNewFeatureGoodHappiness = 0;
	int iNewFeatureBadHappiness = 0;

	for (int iI = 0; iI < NUM_CITY_PLOTS; iI++)
	{
		CvPlot* pLoopPlot = getCityIndexPlot(iI);

		if (pLoopPlot != NULL)
		{
			FeatureTypes eFeature = pLoopPlot->getFeatureType();

			if (eFeature != NO_FEATURE)
			{
				int iHappy = GET_PLAYER(getOwnerINLINE()).getFeatureHappiness(eFeature);
				if (iHappy > 0)
				{
					iNewFeatureGoodHappiness += iHappy;
				}
				else
				{
					iNewFeatureBadHappiness += iHappy;
				}
			}

			ImprovementTypes eImprovement = pLoopPlot->getImprovementType();

			if (NO_IMPROVEMENT != eImprovement)
			{
				int iHappy = GC.getImprovementInfo(eImprovement).getHappiness();
				if (iHappy > 0)
				{
					iNewFeatureGoodHappiness += iHappy;
				}
				else
				{
					iNewFeatureBadHappiness += iHappy;
				}
			}
		}
	}

	if (getFeatureGoodHappiness() != iNewFeatureGoodHappiness)
	{
		m_iFeatureGoodHappiness = iNewFeatureGoodHappiness;
		FAssert(getFeatureGoodHappiness() >= 0);

		AI_setAssignWorkDirty(true);
	}

	if (getFeatureBadHappiness() != iNewFeatureBadHappiness)
	{
		m_iFeatureBadHappiness = iNewFeatureBadHappiness;
		FAssert(getFeatureBadHappiness() <= 0);

		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getBonusGoodHappiness() const
{
	return m_iBonusGoodHappiness;
}


int CvCity::getBonusBadHappiness() const
{
	return m_iBonusBadHappiness;
}


void CvCity::changeBonusGoodHappiness(int iChange)
{
	if (iChange != 0)
	{
		m_iBonusGoodHappiness = (m_iBonusGoodHappiness + iChange);
		FAssert(getBonusGoodHappiness() >= 0);

		AI_setAssignWorkDirty(true);
	}
}


void CvCity::changeBonusBadHappiness(int iChange)
{
	if (iChange != 0)
	{
		m_iBonusBadHappiness = (m_iBonusBadHappiness + iChange);
		FAssert(getBonusBadHappiness() <= 0);

		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getReligionGoodHappiness() const
{
	return m_iReligionGoodHappiness;
}


int CvCity::getReligionBadHappiness() const
{
	if (getOwnerINLINE() == (PlayerTypes)MUGHALS)
		return 0;

	return m_iReligionBadHappiness;
}


int CvCity::getReligionHappiness(ReligionTypes eReligion) const
{
	int iHappiness;
	ReligionTypes eStateReligion = GET_PLAYER(getOwnerINLINE()).getStateReligion();

	iHappiness = 0;

	if (isHasReligion(eReligion))
	{
		if (eReligion == eStateReligion)
		{
			iHappiness += GET_PLAYER(getOwnerINLINE()).getStateReligionHappiness();
		}
		else
		{
			// Leoreth: no religion unhappiness from syncretic pairs Hinduism/Buddhism and Confucianism/Taoism
			bool bSyncretism = ((eStateReligion == HINDUISM && eReligion == BUDDHISM) || (eStateReligion == BUDDHISM && eReligion == HINDUISM) || (eStateReligion == CONFUCIANISM && eReligion == TAOISM) || (eStateReligion == TAOISM && eReligion == CONFUCIANISM));
			if (!bSyncretism)
				iHappiness += GET_PLAYER(getOwnerINLINE()).getNonStateReligionHappiness();
		}
	}

	return iHappiness;
}


void CvCity::updateReligionHappiness()
{
	int iNewReligionGoodHappiness;
	int iNewReligionBadHappiness;
	int iChange;
	int iI;

	iNewReligionGoodHappiness = 0;
	iNewReligionBadHappiness = 0;

	for (iI = 0; iI < GC.getNumReligionInfos(); iI++)
	{
		iChange = getReligionHappiness((ReligionTypes)iI);

		if (iChange > 0)
		{
			iNewReligionGoodHappiness += iChange;
		}
		else
		{
			iNewReligionBadHappiness += iChange;
		}
	}

	if (getReligionGoodHappiness() != iNewReligionGoodHappiness)
	{
		m_iReligionGoodHappiness = iNewReligionGoodHappiness;
		FAssert(getReligionGoodHappiness() >= 0);

		AI_setAssignWorkDirty(true);
	}

	if (getReligionBadHappiness() != iNewReligionBadHappiness)
	{
		m_iReligionBadHappiness = iNewReligionBadHappiness;
		FAssert(getReligionBadHappiness() <= 0);

		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getExtraHappiness() const
{
	return m_iExtraHappiness;
}


void CvCity::changeExtraHappiness(int iChange)
{
	if (iChange != 0)
	{
		m_iExtraHappiness += iChange;

		AI_setAssignWorkDirty(true);
	}
}

int CvCity::getExtraHealth() const
{
	return m_iExtraHealth;
}


void CvCity::changeExtraHealth(int iChange)
{
	if (iChange != 0)
	{
		m_iExtraHealth += iChange;

		AI_setAssignWorkDirty(true);
	}
}



int CvCity::getHurryAngerTimer() const
{
	return m_iHurryAngerTimer;
}


void CvCity::changeHurryAngerTimer(int iChange)
{
	if (iChange != 0)
	{
		m_iHurryAngerTimer = (m_iHurryAngerTimer + iChange);
		FAssert(getHurryAngerTimer() >= 0);

		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getConscriptAngerTimer() const
{
	return m_iConscriptAngerTimer;
}


void CvCity::changeConscriptAngerTimer(int iChange)
{
	if (iChange != 0)
	{
		m_iConscriptAngerTimer = (m_iConscriptAngerTimer + iChange);
		FAssert(getConscriptAngerTimer() >= 0);

		AI_setAssignWorkDirty(true);
	}
}

int CvCity::getDefyResolutionAngerTimer() const
{
	return m_iDefyResolutionAngerTimer;
}


void CvCity::changeDefyResolutionAngerTimer(int iChange)
{
	if (iChange != 0)
	{
		m_iDefyResolutionAngerTimer += iChange;
		FAssert(getDefyResolutionAngerTimer() >= 0);

		AI_setAssignWorkDirty(true);
	}
}

int CvCity::flatDefyResolutionAngerLength() const
{
	int iAnger;

	iAnger = GC.getDefineINT("DEFY_RESOLUTION_ANGER_DIVISOR");

	iAnger *= GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getHurryConscriptAngerPercent();
	iAnger /= 100;

	return std::max(1, iAnger);
}


int CvCity::getHappinessTimer() const
{
	return m_iHappinessTimer;
}


void CvCity::changeHappinessTimer(int iChange)
{
	if (iChange != 0)
	{
		m_iHappinessTimer += iChange;
		FAssert(getHappinessTimer() >= 0);

		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getNoUnhappinessCount() const
{
	return m_iNoUnhappinessCount;
}


bool CvCity::isNoUnhappiness() const
{
	return (getNoUnhappinessCount() > 0);
}


void CvCity::changeNoUnhappinessCount(int iChange)
{
	if (iChange != 0)
	{
		m_iNoUnhappinessCount = (m_iNoUnhappinessCount + iChange);
		FAssert(getNoUnhappinessCount() >= 0);

		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getNoUnhealthyPopulationCount()	const
{
	return m_iNoUnhealthyPopulationCount;
}


bool CvCity::isNoUnhealthyPopulation() const
{
	if (GET_PLAYER(getOwnerINLINE()).isNoUnhealthyPopulation())
	{
		return true;
	}

	return (getNoUnhealthyPopulationCount() > 0);
}


void CvCity::changeNoUnhealthyPopulationCount(int iChange)
{
	if (iChange != 0)
	{
		m_iNoUnhealthyPopulationCount = (m_iNoUnhealthyPopulationCount + iChange);
		FAssert(getNoUnhealthyPopulationCount() >= 0);

		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getBuildingOnlyHealthyCount() const
{
	return m_iBuildingOnlyHealthyCount;
}


bool CvCity::isBuildingOnlyHealthy() const
 {
	if (GET_PLAYER(getOwnerINLINE()).isBuildingOnlyHealthy())
	{
		return true;
	}

	return (getBuildingOnlyHealthyCount() > 0);
}


void CvCity::changeBuildingOnlyHealthyCount(int iChange)
{
	if (iChange != 0)
	{
		m_iBuildingOnlyHealthyCount = (m_iBuildingOnlyHealthyCount + iChange);
		FAssert(getBuildingOnlyHealthyCount() >= 0);

		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getFood() const
{
	return m_iFood;
}


void CvCity::setFood(int iNewValue)
{
	if (getFood() != iNewValue)
	{
		m_iFood = iNewValue;

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);
		}
	}
}


void CvCity::changeFood(int iChange)
{
	setFood(getFood() + iChange);
}


int CvCity::getFoodKept() const
{
	return m_iFoodKept;
}


void CvCity::setFoodKept(int iNewValue)
{
	m_iFoodKept = iNewValue;
}


void CvCity::changeFoodKept(int iChange)
{
	setFoodKept(getFoodKept() + iChange);
}


int CvCity::getMaxFoodKeptPercent() const
{
	return m_iMaxFoodKeptPercent;
}


void CvCity::changeMaxFoodKeptPercent(int iChange)
{
	m_iMaxFoodKeptPercent = (m_iMaxFoodKeptPercent + iChange);
	FAssert(getMaxFoodKeptPercent() >= 0);
}


int CvCity::getOverflowProduction() const
{
	return m_iOverflowProduction;
}


void CvCity::setOverflowProduction(int iNewValue)
{
	m_iOverflowProduction = iNewValue;
	FAssert(getOverflowProduction() >= 0);
}


void CvCity::changeOverflowProduction(int iChange, int iProductionModifier)
{
	int iOverflow = (100 * iChange) / std::max(1, getBaseYieldRateModifier(YIELD_PRODUCTION, iProductionModifier));

	setOverflowProduction(getOverflowProduction() + iOverflow);
}


int CvCity::getFeatureProduction() const
{
	return m_iFeatureProduction;
}


void CvCity::setFeatureProduction(int iNewValue)
{
	m_iFeatureProduction = iNewValue;
	FAssert(getFeatureProduction() >= 0);
}


void CvCity::changeFeatureProduction(int iChange)
{
	setFeatureProduction(getFeatureProduction() + iChange);
}


int CvCity::getMilitaryProductionModifier()	const
{
	return m_iMilitaryProductionModifier;
}


void CvCity::changeMilitaryProductionModifier(int iChange)
{
	m_iMilitaryProductionModifier = (m_iMilitaryProductionModifier + iChange);
}


int CvCity::getSpaceProductionModifier() const
{
	return m_iSpaceProductionModifier;
}


void CvCity::changeSpaceProductionModifier(int iChange)
{
	m_iSpaceProductionModifier = (m_iSpaceProductionModifier + iChange);
}


int CvCity::getExtraTradeRoutes() const
{
	return m_iExtraTradeRoutes;
}


void CvCity::changeExtraTradeRoutes(int iChange)
{
	if (iChange != 0)
	{
		m_iExtraTradeRoutes = (m_iExtraTradeRoutes + iChange);
		FAssert(getExtraTradeRoutes() >= 0);

		updateTradeRoutes();
	}
}


int CvCity::getTradeRouteModifier() const
{
	int iResult = m_iTradeRouteModifier;

    // Leoreth - new Phoenician UP: the power of seafaring, +50% trade route yield.
    //if (getOwner() == PHOENICIA)
    //    iResult += 50;

	//Leoreth: Porcelain Tower effect (removed)
	/*if (GET_PLAYER(getOwner()).isHasBuilding((BuildingTypes)PORCELAIN))
		for (int iI = 0; iI < NUM_MAJOR_PLAYERS; iI++)
			if (GET_PLAYER(getOwner()).canContact((PlayerTypes)iI) && !GET_TEAM((TeamTypes)getOwner()).isOpenBorders((TeamTypes)iI))
				iResult += 10;*/

	return iResult;
}

void CvCity::changeTradeRouteModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iTradeRouteModifier = (m_iTradeRouteModifier + iChange);

		updateTradeRoutes();
	}
}

int CvCity::getForeignTradeRouteModifier() const
{
	return m_iForeignTradeRouteModifier;
}

void CvCity::changeForeignTradeRouteModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iForeignTradeRouteModifier = (m_iForeignTradeRouteModifier + iChange);

		updateTradeRoutes();
	}
}


int CvCity::getBuildingDefense() const
{
	return m_iBuildingDefense;
}


void CvCity::changeBuildingDefense(int iChange)
{
	if (iChange != 0)
	{
		m_iBuildingDefense = (m_iBuildingDefense + iChange);
		FAssert(getBuildingDefense() >= 0);

		setInfoDirty(true);

		plot()->plotAction(PUF_makeInfoBarDirty);
	}
}

// BUG - Building Additional Defense - start
int CvCity::getAdditionalDefenseByBuilding(BuildingTypes eBuilding) const
{
	FAssertMsg(eBuilding >= 0, "eBuilding expected to be >= 0");
	FAssertMsg(eBuilding < GC.getNumBuildingInfos(), "eBuilding expected to be < GC.getNumBuildingInfos()");

	CvBuildingInfo& kBuilding = GC.getBuildingInfo(eBuilding);
	int iDefense = std::max(getBuildingDefense() + kBuilding.getDefenseModifier(), getNaturalDefense()) + GET_PLAYER(getOwnerINLINE()).getCityDefenseModifier() + kBuilding.getAllCityDefenseModifier();

	// doesn't take bombardment into account
	return iDefense - getTotalDefense(false);
}
// BUG - Building Additional Defense - end


int CvCity::getBuildingBombardDefense() const
{
	return m_iBuildingBombardDefense;
}


void CvCity::changeBuildingBombardDefense(int iChange)
{
	if (iChange != 0)
	{
		m_iBuildingBombardDefense += iChange;
		FAssert(getBuildingBombardDefense() >= 0);
	}
}

// BUG - Building Additional Bombard Defense - start
int CvCity::getAdditionalBombardDefenseByBuilding(BuildingTypes eBuilding) const
{
	FAssertMsg(eBuilding >= 0, "eBuilding expected to be >= 0");
	FAssertMsg(eBuilding < GC.getNumBuildingInfos(), "eBuilding expected to be < GC.getNumBuildingInfos()");

	CvBuildingInfo& kBuilding = GC.getBuildingInfo(eBuilding);
	int iBaseDefense = getBuildingBombardDefense();

	// cap total bombard defense at 100
	return std::min(kBuilding.getBombardDefenseModifier() + iBaseDefense, 100) - iBaseDefense;
}
// BUG - Building Additional Bombard Defense - end


int CvCity::getFreeExperience() const
{
	return m_iFreeExperience;
}


void CvCity::changeFreeExperience(int iChange)
{
	m_iFreeExperience = (m_iFreeExperience + iChange);
	FAssert(getFreeExperience() >= 0);
}


int CvCity::getCurrAirlift() const
{
	return m_iCurrAirlift;
}


void CvCity::setCurrAirlift(int iNewValue)
{
	m_iCurrAirlift = iNewValue;
	FAssert(getCurrAirlift() >= 0);
}


void CvCity::changeCurrAirlift(int iChange)
{
	setCurrAirlift(getCurrAirlift() + iChange);
}


int CvCity::getMaxAirlift() const
{
	return m_iMaxAirlift;
}


void CvCity::changeMaxAirlift(int iChange)
{
	m_iMaxAirlift = (m_iMaxAirlift + iChange);
	FAssert(getMaxAirlift() >= 0);
}

int CvCity::getAirModifier() const
{
	return m_iAirModifier;
}

void CvCity::changeAirModifier(int iChange)
{
	m_iAirModifier += iChange;
}

int CvCity::getAirUnitCapacity(TeamTypes eTeam) const
{
	return (getTeam() == eTeam ? m_iAirUnitCapacity : GC.getDefineINT("CITY_AIR_UNIT_CAPACITY"));
}

void CvCity::changeAirUnitCapacity(int iChange)
{
	m_iAirUnitCapacity += iChange;
	FAssert(getAirUnitCapacity(getTeam()) >= 0);
}

int CvCity::getNukeModifier() const
{
	return m_iNukeModifier;
}


void CvCity::changeNukeModifier(int iChange)
{
	m_iNukeModifier = (m_iNukeModifier + iChange);
}


int CvCity::getFreeSpecialist() const
{
    // Leoreth: Italian UP, only until the industrial era
    int iItalianSpecialists = 0;
	int iCoreSpecialists = 0;

    if (getOwner() == ITALY && GET_PLAYER((PlayerTypes)ITALY).getCurrentEra() < 4)
    {
		iItalianSpecialists = 1;
    }

	//Leoreth: handle free specialists for core here for simplicity
	if (GET_PLAYER(getOwner()).getCoreFreeSpecialist() > 0)
	{
		if (plotDistance(getX(), getY(), GET_PLAYER(getOwner()).getCapitalCity()->getX(), GET_PLAYER(getOwner()).getCapitalCity()->getY()) <= 3)
		{
			iCoreSpecialists = GET_PLAYER(getOwner()).getCoreFreeSpecialist();
		}
	}

	return m_iFreeSpecialist+iItalianSpecialists+iCoreSpecialists;
}


void CvCity::changeFreeSpecialist(int iChange)
{
	if (iChange != 0)
	{
		m_iFreeSpecialist = (m_iFreeSpecialist + iChange);
		FAssert(getFreeSpecialist() >= 0);

		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getPowerCount() const
{
	return m_iPowerCount;
}


bool CvCity::isPower() const
{
	return ((getPowerCount() > 0) || isAreaCleanPower());
}


bool CvCity::isAreaCleanPower() const
{
	if (area() == NULL)
	{
		return false;
	}

	return area()->isCleanPower(getTeam());
}


int CvCity::getDirtyPowerCount() const
{
	return m_iDirtyPowerCount;
}


bool CvCity::isDirtyPower() const
{
	return (isPower() && (getDirtyPowerCount() == getPowerCount()) && !isAreaCleanPower());
}


void CvCity::changePowerCount(int iChange, bool bDirty)
{
	bool bOldPower;
	bool bOldDirtyPower;

	if (iChange != 0)
	{
		bOldPower = isPower();
		bOldDirtyPower = isDirtyPower();

		m_iPowerCount = (m_iPowerCount + iChange);
		FAssert(getPowerCount() >= 0);
		if (bDirty)
		{
			m_iDirtyPowerCount += iChange;
			FAssert(getDirtyPowerCount() >= 0);
		}

		if (bOldPower != isPower())
		{
			GET_PLAYER(getOwnerINLINE()).invalidateYieldRankCache();

			updateCommerce();

			if (getTeam() == GC.getGameINLINE().getActiveTeam())
			{
				setInfoDirty(true);
			}
		}

		if (bOldDirtyPower != isDirtyPower() || bOldPower != isPower())
		{
			updatePowerHealth();
		}
	}
}


int CvCity::getDefenseDamage() const
{
	return m_iDefenseDamage;
}


void CvCity::changeDefenseDamage(int iChange)
{
	if (iChange != 0)
	{
		m_iDefenseDamage = range((m_iDefenseDamage + iChange), 0, GC.getMAX_CITY_DEFENSE_DAMAGE());

		if (iChange > 0)
		{
			setBombarded(true);
		}

		setInfoDirty(true);

		plot()->plotAction(PUF_makeInfoBarDirty);
	}
}

void CvCity::changeDefenseModifier(int iChange)
{
	if (iChange != 0)
	{
		int iTotalDefense = getTotalDefense(false);

		if (iTotalDefense > 0)
		{
			changeDefenseDamage(-(GC.getMAX_CITY_DEFENSE_DAMAGE() * iChange) / iTotalDefense);
		}
	}
}


int CvCity::getLastDefenseDamage() const
{
	return m_iLastDefenseDamage;
}


void CvCity::setLastDefenseDamage(int iNewValue)
{
	m_iLastDefenseDamage = iNewValue;
}


bool CvCity::isBombardable(const CvUnit* pUnit) const
{
	if (NULL != pUnit && !pUnit->isEnemy(getTeam()))
	{
		return false;
	}

	return (getDefenseModifier(false) > 0);
}


int CvCity::getNaturalDefense() const
{
	if (getCultureLevel() == NO_CULTURELEVEL)
	{
		return 0;
	}

	return GC.getCultureLevelInfo(getCultureLevel()).getCityDefenseModifier();
}


int CvCity::getTotalDefense(bool bIgnoreBuilding) const
{
	return (std::max(((bIgnoreBuilding) ? 0 : getBuildingDefense()), getNaturalDefense()) + GET_PLAYER(getOwnerINLINE()).getCityDefenseModifier());
}


int CvCity::getDefenseModifier(bool bIgnoreBuilding) const
{
	if (isOccupation())
	{
		return 0;
	}

	return ((getTotalDefense(bIgnoreBuilding) * (GC.getMAX_CITY_DEFENSE_DAMAGE() - getDefenseDamage())) / GC.getMAX_CITY_DEFENSE_DAMAGE());
}


int CvCity::getOccupationTimer() const
{
	return m_iOccupationTimer;
}


bool CvCity::isOccupation() const
{
	return (getOccupationTimer() > 0);
}


void CvCity::setOccupationTimer(int iNewValue)
{
	bool bOldOccupation;

	//Leoreth: cap city disorder at 5 turns
	iNewValue = std::min(iNewValue, 5);

	if (getOccupationTimer() != iNewValue)
	{
		bOldOccupation = isOccupation();

		m_iOccupationTimer = iNewValue;
		FAssert(getOccupationTimer() >= 0);

		if (bOldOccupation != isOccupation())
		{
			updateCorporation();
			updateMaintenance();
			updateTradeRoutes();

			updateCultureLevel(true);
			updateCoveredPlots(true); // Leoreth

			AI_setAssignWorkDirty(true);
		}

		setInfoDirty(true);
	}
}


void CvCity::changeOccupationTimer(int iChange)
{
	//Leoreth: occupation time capped at 5
	setOccupationTimer(std::min(getOccupationTimer() + iChange, 5));
}


int CvCity::getCultureUpdateTimer() const
{
	return m_iCultureUpdateTimer;
}


void CvCity::setCultureUpdateTimer(int iNewValue)
{
	m_iCultureUpdateTimer = iNewValue;
	FAssert(getOccupationTimer() >= 0);
}


void CvCity::changeCultureUpdateTimer(int iChange)
{
	setCultureUpdateTimer(getCultureUpdateTimer() + iChange);
}


int CvCity::getCitySizeBoost() const
{
	return m_iCitySizeBoost;
}


void CvCity::setCitySizeBoost(int iBoost)
{
	if (getCitySizeBoost() != iBoost)
	{
		m_iCitySizeBoost = iBoost;

		setLayoutDirty(true);
	}
}


bool CvCity::isNeverLost() const
{
	return m_bNeverLost;
}


void CvCity::setNeverLost(bool bNewValue)
{
	m_bNeverLost = bNewValue;
}


bool CvCity::isBombarded() const
{
	return m_bBombarded;
}


void CvCity::setBombarded(bool bNewValue)
{
	m_bBombarded = bNewValue;
}


bool CvCity::isDrafted() const
{
	return m_bDrafted;
}


void CvCity::setDrafted(bool bNewValue)
{
	m_bDrafted = bNewValue;
}


bool CvCity::isAirliftTargeted() const
{
	return m_bAirliftTargeted;
}


void CvCity::setAirliftTargeted(bool bNewValue)
{
	m_bAirliftTargeted = bNewValue;
}


bool CvCity::isPlundered() const
{
	return m_bPlundered;
}


void CvCity::setPlundered(bool bNewValue)
{
	if (bNewValue != isPlundered())
	{
		m_bPlundered = bNewValue;

		updateTradeRoutes();
	}
}


bool CvCity::isWeLoveTheKingDay() const
{
	return m_bWeLoveTheKingDay;
}


void CvCity::setWeLoveTheKingDay(bool bNewValue)
{
	CvWString szBuffer;
	CivicTypes eCivic;
	int iI;

	if (isWeLoveTheKingDay() != bNewValue)
	{
		m_bWeLoveTheKingDay = bNewValue;

		updateMaintenance();

		eCivic = NO_CIVIC;

		for (iI = 0; iI < GC.getNumCivicInfos(); iI++)
		{
			if (GET_PLAYER(getOwnerINLINE()).isCivic((CivicTypes)iI))
			{
				if (!CvWString(GC.getCivicInfo((CivicTypes)iI).getWeLoveTheKing()).empty())
				{
					eCivic = ((CivicTypes)iI);
					break;
				}
			}
		}

		if (eCivic != NO_CIVIC)
		{
			szBuffer = gDLL->getText("TXT_KEY_CITY_CELEBRATE", getNameKey(), GC.getCivicInfo(eCivic).getWeLoveTheKing());
			gDLL->getInterfaceIFace()->addMessage(getOwnerINLINE(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_WELOVEKING", MESSAGE_TYPE_MINOR_EVENT, ARTFILEMGR.getInterfaceArtInfo("INTERFACE_HAPPY_PERSON")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), getX_INLINE(), getY_INLINE(), true, true);
		}
	}
}


bool CvCity::isCitizensAutomated() const
{
	return m_bCitizensAutomated;
}


void CvCity::setCitizensAutomated(bool bNewValue)
{
	int iI;

	if (isCitizensAutomated() != bNewValue)
	{
		m_bCitizensAutomated = bNewValue;

		if (isCitizensAutomated())
		{
			AI_assignWorkingPlots();
		}
		else
		{
			for (iI = 0; iI < GC.getNumSpecialistInfos(); iI++)
			{
				setForceSpecialistCount(((SpecialistTypes)iI), 0);
			}
		}

		if ((getOwnerINLINE() == GC.getGameINLINE().getActivePlayer()) && isCitySelected())
		{
			gDLL->getInterfaceIFace()->setDirty(SelectionButtons_DIRTY_BIT, true);
		}
	}
}


bool CvCity::isProductionAutomated() const
{
	return m_bProductionAutomated;
}


void CvCity::setProductionAutomated(bool bNewValue, bool bClear)
{
	if (isProductionAutomated() != bNewValue)
	{
		m_bProductionAutomated = bNewValue;

		if ((getOwnerINLINE() == GC.getGameINLINE().getActivePlayer()) && isCitySelected())
		{
			gDLL->getInterfaceIFace()->setDirty(SelectionButtons_DIRTY_BIT, true);

			// if automated and not network game and all 3 modifiers down, clear the queue and choose again
			if (bNewValue && bClear)
			{
				clearOrderQueue();
			}
		}

		if (!isProduction())
		{
		    AI_chooseProduction();
		}
	}
}


bool CvCity::isWallOverride() const
{
	return m_bWallOverride;
}


void CvCity::setWallOverride(bool bOverride)
{
	if (isWallOverride() != bOverride)
	{
		m_bWallOverride = bOverride;

		setLayoutDirty(true);
	}
}


bool CvCity::isInfoDirty() const
{
	return m_bInfoDirty;
}


void CvCity::setInfoDirty(bool bNewValue)
{
	m_bInfoDirty = bNewValue;
}


bool CvCity::isLayoutDirty() const
{
	return m_bLayoutDirty;
}


void CvCity::setLayoutDirty(bool bNewValue)
{
	m_bLayoutDirty = bNewValue;
}


PlayerTypes CvCity::getOwner() const
{
	return getOwnerINLINE();
}


PlayerTypes CvCity::getPreviousOwner() const
{
	return m_ePreviousOwner;
}


void CvCity::setPreviousOwner(PlayerTypes eNewValue)
{
	m_ePreviousOwner = eNewValue;
}


PlayerTypes CvCity::getOriginalOwner() const
{
	return m_eOriginalOwner;
}


void CvCity::setOriginalOwner(PlayerTypes eNewValue)
{
	m_eOriginalOwner = eNewValue;
}


TeamTypes CvCity::getTeam() const
{
	return GET_PLAYER(getOwnerINLINE()).getTeam();
}


CultureLevelTypes CvCity::getCultureLevel() const
{
	//Leoreth: cap at two for minors
	if (getOwnerINLINE() == INDEPENDENT || getOwnerINLINE() == INDEPENDENT2 || getOwnerINLINE() == SELJUKS)
		return std::min(m_eCultureLevel, (CultureLevelTypes)2);

	return m_eCultureLevel;
}


int CvCity::getCultureThreshold() const
{
	return getCultureThreshold(getCultureLevel());
}

int CvCity::getCultureThreshold(CultureLevelTypes eLevel)
{
	if (eLevel == NO_CULTURELEVEL)
	{
		return 1;
	}

	return std::max(1, GC.getGameINLINE().getCultureThreshold((CultureLevelTypes)(std::min((eLevel + 1), (GC.getNumCultureLevelInfos() - 1)))));
}


void CvCity::setCultureLevel(CultureLevelTypes eNewValue, bool bUpdatePlotGroups)
{
	//CvPlot* pLoopPlot;
	CvWString szBuffer;
	CultureLevelTypes eOldValue;
	//int iCultureRange;
	//int iDX, iDY;
	int iI;

	eOldValue = getCultureLevel();

	if (eOldValue != eNewValue)
	{
		m_eCultureLevel = eNewValue;

		/*if (eOldValue != NO_CULTURELEVEL)
		{
			for (iDX = -eOldValue; iDX <= eOldValue; iDX++)
			{
				for (iDY = -eOldValue; iDY <= eOldValue; iDY++)
				{
					iCultureRange = cultureDistance(iDX, iDY);

					if (iCultureRange > getCultureLevel())
					{
						if (iCultureRange <= eOldValue)
						{
							FAssert(iCultureRange <= GC.getNumCultureLevelInfos());

							pLoopPlot = plotXY(getX_INLINE(), getY_INLINE(), iDX, iDY);

							if (pLoopPlot != NULL)
							{
								pLoopPlot->changeCultureRangeCities(getOwnerINLINE(), iCultureRange, -1, bUpdatePlotGroups);
							}
						}
					}
				}
			}
		}

		if (getCultureLevel() != NO_CULTURELEVEL)
		{
			for (iDX = -getCultureLevel(); iDX <= getCultureLevel(); iDX++)
			{
				for (iDY = -getCultureLevel(); iDY <= getCultureLevel(); iDY++)
				{
					iCultureRange = cultureDistance(iDX, iDY);

					if (iCultureRange > eOldValue)
					{
						if (iCultureRange <= getCultureLevel())
						{
							FAssert(iCultureRange <= GC.getNumCultureLevelInfos());

							pLoopPlot = plotXY(getX_INLINE(), getY_INLINE(), iDX, iDY);

							if (pLoopPlot != NULL)
							{
								pLoopPlot->changeCultureRangeCities(getOwnerINLINE(), iCultureRange, 1, bUpdatePlotGroups);
							}
						}
					}
				}
			}
		}*/

		if (GC.getGameINLINE().isFinalInitialized())
		{
			if ((getCultureLevel() > eOldValue) && (getCultureLevel() > 1))
			{
				//szBuffer = gDLL->getText("TXT_KEY_MISC_BORDERS_EXPANDED", getNameKey());
				//gDLL->getInterfaceIFace()->addMessage(getOwnerINLINE(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_CULTUREEXPANDS", MESSAGE_TYPE_MINOR_EVENT, GC.getCommerceInfo(COMMERCE_CULTURE).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), getX_INLINE(), getY_INLINE(), true, true);

				if (getCultureLevel() == (GC.getNumCultureLevelInfos() - 1))
				{
					for (iI = 0; iI < MAX_PLAYERS; iI++)
					{
						if (GET_PLAYER((PlayerTypes)iI).isAlive())
						{
							if (isRevealed(GET_PLAYER((PlayerTypes)iI).getTeam(), false))
							{
								szBuffer = gDLL->getText("TXT_KEY_MISC_CULTURE_LEVEL", getNameKey(), GC.getCultureLevelInfo(getCultureLevel()).getTextKeyWide());
								gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_CULTURELEVEL", MESSAGE_TYPE_MAJOR_EVENT, GC.getCommerceInfo(COMMERCE_CULTURE).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"), getX_INLINE(), getY_INLINE(), true, true);
							}
							else
							{
								szBuffer = gDLL->getText("TXT_KEY_MISC_CULTURE_LEVEL_UNKNOWN", GC.getCultureLevelInfo(getCultureLevel()).getTextKeyWide());
								gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_CULTURELEVEL", MESSAGE_TYPE_MAJOR_EVENT, GC.getCommerceInfo(COMMERCE_CULTURE).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"));
							}
						}
					}
				}

				// ONEVENT - Culture growth
				//CvEventReporter::getInstance().cultureExpansion(this, getOwnerINLINE());

				//Stop Build Culture
/************************************************************************************************/
/* UNOFFICIAL_PATCH                       12/07/09                         denev & jdog5000     */
/*                                                                                              */
/* Bugfix, Odd behavior                                                                         */
/************************************************************************************************/
/* original BTS code
				if (isProductionProcess())
				{
					if (GC.getProcessInfo(getProductionProcess()).getProductionToCommerceModifier(COMMERCE_CULTURE) > 0)
					{
						popOrder(0, false, true);						
					}
				}
*/
				// For AI this is completely unnecessary.  Timing also appears to cause bug with overflow production, 
				// giving extra hammers innappropriately.
				/*if( isHuman() && !isProductionAutomated() )
				{
					if (isProductionProcess())
					{
						if (GC.getProcessInfo(getProductionProcess()).getProductionToCommerceModifier(COMMERCE_CULTURE) > 0)
						{
							//popOrder(0, false, true);
							m_bPopProductionProcess = true;
						}
					}
				}
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/
			}
		}
	}
}


void CvCity::updateCultureLevel(bool bUpdatePlotGroups)
{
	if (getCultureUpdateTimer() > 0)
	{
		return;
	}

	CultureLevelTypes eCultureLevel = ((CultureLevelTypes)0);

	if (!isOccupation())
	{
		for (int iI = (GC.getNumCultureLevelInfos() - 1); iI > 0; iI--)
		{
			if (getCultureTimes100(getOwnerINLINE()) >= 100 * GC.getGameINLINE().getCultureThreshold((CultureLevelTypes)iI))
			{
				eCultureLevel = ((CultureLevelTypes)iI);
				break;
			}
		}
	}

	setCultureLevel(eCultureLevel, bUpdatePlotGroups);
}


int CvCity::getSeaPlotYield(YieldTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");
	return m_aiSeaPlotYield[eIndex];
}


void CvCity::changeSeaPlotYield(YieldTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");

	if (iChange != 0)
	{
		m_aiSeaPlotYield[eIndex] = (m_aiSeaPlotYield[eIndex] + iChange);
		FAssert(getSeaPlotYield(eIndex) >= 0);

		updateYield();
	}
}


int CvCity::getRiverPlotYield(YieldTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");
	return m_aiRiverPlotYield[eIndex];
}


void CvCity::changeRiverPlotYield(YieldTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");

	if (iChange != 0)
	{
		m_aiRiverPlotYield[eIndex] += iChange;
		FAssert(getRiverPlotYield(eIndex) >= 0);

		updateYield();
	}
}


// Leoreth
int CvCity::getBonusYield(BonusTypes eBonus, YieldTypes eYield) const
{
	return m_ppaiBonusYield[eBonus][eYield];
}


// Leoreth
void CvCity::changeBonusYield(BonusTypes eBonus, YieldTypes eYield, int iChange)
{
	if (iChange != 0)
	{
		m_ppaiBonusYield[eBonus][eYield] += iChange;

		updateYield();
	}
}

// BUG - Building Additional Yield - start
/*
 * Returns the total additional yield that adding one of the given buildings will provide.
 *
 * Doesn't check if the building can be constructed in this city.
 */
int CvCity::getAdditionalYieldByBuilding(YieldTypes eIndex, BuildingTypes eBuilding) const
{
	int iRate = getBaseYieldRate(eIndex);
	int iModifier = getBaseYieldRateModifier(eIndex);
	int iExtra = ((iRate + getAdditionalBaseYieldRateByBuilding(eIndex, eBuilding)) * (iModifier + getAdditionalYieldRateModifierByBuilding(eIndex, eBuilding)) / 100) - (iRate * iModifier / 100);

	return iExtra;
}

/*
 * Returns the additional yield rate that adding one of the given buildings will provide.
 *
 * Doesn't check if the building can be constructed in this city.
 */
int CvCity::getAdditionalBaseYieldRateByBuilding(YieldTypes eIndex, BuildingTypes eBuilding) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");
	FAssertMsg(eBuilding >= 0, "eBuilding expected to be >= 0");
	FAssertMsg(eBuilding < GC.getNumBuildingInfos(), "eBuilding expected to be < GC.getNumBuildingInfos()");

	CvBuildingInfo& kBuilding = GC.getBuildingInfo(eBuilding);
	bool bObsolete = GET_TEAM(getTeam()).isObsoleteBuilding(eBuilding);
	int iExtraRate = 0;

	if (!bObsolete)
	{
		if (kBuilding.getSeaPlotYieldChange(eIndex) != 0)
		{
			int iChange = kBuilding.getSeaPlotYieldChange(eIndex);
			for (int iI = 0; iI < NUM_CITY_PLOTS; ++iI)
			{
				if (isWorkingPlot(iI) && getCityIndexPlot(iI)->isWater())
				{
					iExtraRate += iChange;
				}
			}
		}
		if (kBuilding.getRiverPlotYieldChange(eIndex) != 0)
		{
			int iChange = kBuilding.getRiverPlotYieldChange(eIndex);
			for (int iI = 0; iI < NUM_CITY_PLOTS; ++iI)
			{
				if (isWorkingPlot(iI) && getCityIndexPlot(iI)->isRiver())
				{
					iExtraRate += iChange;
				}
			}
		}
		iExtraRate += kBuilding.getYieldChange(eIndex);
		iExtraRate += getBuildingYieldChange((BuildingClassTypes)kBuilding.getBuildingClassType(), eIndex);

		// Trade
		int iPlayerTradeYieldModifier = GET_PLAYER(getOwnerINLINE()).getTradeYieldModifier(eIndex);
		if (iPlayerTradeYieldModifier > 0 && (kBuilding.getTradeRouteModifier() != 0 || kBuilding.getForeignTradeRouteModifier() != 0))
		{
			int iTotalTradeYield = 0;
			int iNewTotalTradeYield = 0;
// BUG - Fractional Trade Routes - start
#ifdef _MOD_FRACTRADE
			int iTradeProfitDivisor = 100;
#else
			int iTradeProfitDivisor = 10000;
#endif
// BUG - Fractional Trade Routes - end

			for (int iI = 0; iI < getTradeRoutes(); ++iI)
			{
				CvCity* pCity = getTradeCity(iI);
				if (pCity)
				{
					int iTradeProfit = getBaseTradeProfit(pCity);
					int iTradeModifier = totalTradeModifier(pCity);
					int iTradeYield = iTradeProfit * iTradeModifier / iTradeProfitDivisor * iPlayerTradeYieldModifier / 100;
					iTotalTradeYield += iTradeYield;

					iTradeModifier += kBuilding.getTradeRouteModifier();
					if (pCity->getOwnerINLINE() != getOwnerINLINE())
					{
						iTradeModifier += kBuilding.getForeignTradeRouteModifier();
					}
					int iNewTradeYield = iTradeProfit * iTradeModifier / iTradeProfitDivisor * iPlayerTradeYieldModifier / 100;
					iNewTotalTradeYield += iNewTradeYield;
				}
			}

// BUG - Fractional Trade Routes - start
#ifdef _MOD_FRACTRADE
			iTotalTradeYield /= 100;
			iNewTotalTradeYield /= 100;
#endif
// BUG - Fractional Trade Routes - end
			iExtraRate += iNewTotalTradeYield - iTotalTradeYield;
		}

		// Specialists
		for (int iI = 0; iI < GC.getNumSpecialistInfos(); ++iI)
		{
			if (kBuilding.getFreeSpecialistCount((SpecialistTypes)iI) != 0)
			{
				iExtraRate += getAdditionalBaseYieldRateBySpecialist(eIndex, (SpecialistTypes)iI, kBuilding.getFreeSpecialistCount((SpecialistTypes)iI));
			}
		}
	}

	return iExtraRate;
}

/*
 * Returns the additional yield rate modifier that adding one of the given buildings will provide.
 *
 * Doesn't check if the building can be constructed in this city.
 */
int CvCity::getAdditionalYieldRateModifierByBuilding(YieldTypes eIndex, BuildingTypes eBuilding) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");
	FAssertMsg(eBuilding >= 0, "eBuilding expected to be >= 0");
	FAssertMsg(eBuilding < GC.getNumBuildingInfos(), "eBuilding expected to be < GC.getNumBuildingInfos()");

	CvBuildingInfo& kBuilding = GC.getBuildingInfo(eBuilding);
	bool bObsolete = GET_TEAM(getTeam()).isObsoleteBuilding(eBuilding);
	int iExtraModifier = 0;

	if (!bObsolete)
	{
		iExtraModifier += kBuilding.getYieldModifier(eIndex);
		if (!isPower())
		{
			if (kBuilding.isPower() || kBuilding.isAreaCleanPower() || (kBuilding.getPowerBonus() != NO_BONUS && hasBonus((BonusTypes)kBuilding.getPowerBonus())))
			{
				for (int i = 0; i < GC.getNumBuildingInfos(); i++)
				{
					iExtraModifier += getNumActiveBuilding((BuildingTypes)i) * GC.getBuildingInfo((BuildingTypes)i).getPowerYieldModifier(eIndex);
				}
			}
		}
		if (eIndex == YIELD_PRODUCTION)
		{
			iExtraModifier += kBuilding.getMilitaryProductionModifier();
			iExtraModifier += kBuilding.getSpaceProductionModifier();
			iExtraModifier += kBuilding.getGlobalSpaceProductionModifier();

			int iMaxModifier = 0;
			for (int i = 0; i < NUM_DOMAIN_TYPES; i++)
			{
				iMaxModifier = std::max(iMaxModifier, kBuilding.getDomainProductionModifier((DomainTypes)i));
			}
			iExtraModifier += iMaxModifier;
		}
		for (int iI = 0; iI < GC.getNumBonusInfos(); ++iI)
		{
			if (hasBonus((BonusTypes)iI))
			{
				iExtraModifier += kBuilding.getBonusYieldModifier(iI, eIndex);
			}
		}
	}

	return iExtraModifier;
}
// BUG - Building Additional Yield - end


// BUG - Specialist Additional Yield - start
/*
 * Returns the total additional yield that changing the number of given specialists will provide/remove.
 */
int CvCity::getAdditionalYieldBySpecialist(YieldTypes eIndex, SpecialistTypes eSpecialist, int iChange) const
{
	int iRate = getBaseYieldRate(eIndex);
	int iModifier = getBaseYieldRateModifier(eIndex);
	int iExtra = ((iRate + getAdditionalBaseYieldRateBySpecialist(eIndex, eSpecialist, iChange)) * iModifier / 100) - (iRate * iModifier / 100);

	return iExtra;
}

/*
 * Returns the additional yield rate that changing the number of given specialists will provide/remove.
 */
int CvCity::getAdditionalBaseYieldRateBySpecialist(YieldTypes eIndex, SpecialistTypes eSpecialist, int iChange) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");
	FAssertMsg(eSpecialist >= 0, "eSpecialist expected to be >= 0");
	FAssertMsg(eSpecialist < GC.getNumSpecialistInfos(), "eSpecialist expected to be < GC.getNumSpecialistInfos()");
	
	CvSpecialistInfo& kSpecialist = GC.getSpecialistInfo(eSpecialist);
	return iChange * (kSpecialist.getYieldChange(eIndex) + GET_PLAYER(getOwnerINLINE()).getSpecialistExtraYield(eSpecialist, eIndex));
}
// BUG - Specialist Additional Yield - end


int CvCity::getBaseYieldRate(YieldTypes eIndex)	const													
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");
	return m_aiBaseYieldRate[eIndex];
}


int CvCity::getBaseYieldRateModifier(YieldTypes eIndex, int iExtra) const
{
	int iModifier;

	iModifier = getYieldRateModifier(eIndex);

	iModifier += getBonusYieldRateModifier(eIndex);

	if (isPower())
	{
		iModifier += getPowerYieldRateModifier(eIndex);
	}

	if (area() != NULL)
	{
		iModifier += area()->getYieldRateModifier(getOwnerINLINE(), eIndex);
	}

	iModifier += GET_PLAYER(getOwnerINLINE()).getYieldRateModifier(eIndex);

	if (isCapital())
	{
		iModifier += GET_PLAYER(getOwnerINLINE()).getCapitalYieldRateModifier(eIndex);
	}

	iModifier += iExtra;

	// note: player->invalidateYieldRankCache() must be called for anything that is checked here
	// so if any extra checked things are added here, the cache needs to be invalidated

	return std::max(0, (iModifier + 100));
}


int CvCity::getYieldRate(YieldTypes eIndex) const
{
	int iYieldRateTimes100 = getBaseYieldRate(eIndex) * getBaseYieldRateModifier(eIndex);

	// Harappan UP: Sanitation: positive health contributes to city growth
	if (eIndex == YIELD_FOOD && getOwnerINLINE() == HARAPPA && GET_PLAYER(getOwnerINLINE()).getCurrentEra() == ERA_ANCIENT  && !isFoodProduction())
	{
		if (iYieldRateTimes100 - foodConsumption() * 100 > 1 && goodHealth() - badHealth() > 0)
		{
			iYieldRateTimes100 += 100 * (goodHealth() - badHealth());
		}
	}

	return (iYieldRateTimes100 / 100);
}


void CvCity::setBaseYieldRate(YieldTypes eIndex, int iNewValue)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");

	if (getBaseYieldRate(eIndex) != iNewValue)
	{
		FAssertMsg(iNewValue >= 0, "iNewValue expected to be >= 0");
		FAssertMsg(((iNewValue * 100) / 100) >= 0, "((iNewValue * 100) / 100) expected to be >= 0");

		m_aiBaseYieldRate[eIndex] = iNewValue;
		FAssert(getYieldRate(eIndex) >= 0);

		updateCommerce();

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);

			if (isCitySelected())
			{
				gDLL->getInterfaceIFace()->setDirty(CityScreen_DIRTY_BIT, true);
				gDLL->getInterfaceIFace()->setDirty(InfoPane_DIRTY_BIT, true );
			}
		}
	}
}


void CvCity::changeBaseYieldRate(YieldTypes eIndex, int iChange)
{
	setBaseYieldRate(eIndex, (getBaseYieldRate(eIndex) + iChange));
}


int CvCity::getYieldRateModifier(YieldTypes eIndex)	const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");
	return m_aiYieldRateModifier[eIndex];
}


void CvCity::changeYieldRateModifier(YieldTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");

	if (iChange != 0)
	{
		m_aiYieldRateModifier[eIndex] = (m_aiYieldRateModifier[eIndex] + iChange);
		FAssert(getYieldRate(eIndex) >= 0);

		GET_PLAYER(getOwnerINLINE()).invalidateYieldRankCache(eIndex);

		if (eIndex == YIELD_COMMERCE)
		{
			updateCommerce();
		}

		AI_setAssignWorkDirty(true);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);
		}
	}
}


int CvCity::getPowerYieldRateModifier(YieldTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");
	return m_aiPowerYieldRateModifier[eIndex];
}


void CvCity::changePowerYieldRateModifier(YieldTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");

	if (iChange != 0)
	{
		m_aiPowerYieldRateModifier[eIndex] = (m_aiPowerYieldRateModifier[eIndex] + iChange);
		FAssert(getYieldRate(eIndex) >= 0);

		GET_PLAYER(getOwnerINLINE()).invalidateYieldRankCache(eIndex);

		if (eIndex == YIELD_COMMERCE)
		{
			updateCommerce();
		}

		AI_setAssignWorkDirty(true);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);
		}
	}
}


int CvCity::getBonusYieldRateModifier(YieldTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");
	return m_aiBonusYieldRateModifier[eIndex];
}


void CvCity::changeBonusYieldRateModifier(YieldTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");

	if (iChange != 0)
	{
		m_aiBonusYieldRateModifier[eIndex] = (m_aiBonusYieldRateModifier[eIndex] + iChange);
		FAssert(getYieldRate(eIndex) >= 0);

		GET_PLAYER(getOwnerINLINE()).invalidateYieldRankCache(eIndex);

		if (eIndex == YIELD_COMMERCE)
		{
			updateCommerce();
		}

		AI_setAssignWorkDirty(true);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);
		}
	}
}


// Leoreth
int CvCity::getBonusCommerceRateModifier(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");
	return m_aiBonusCommerceRateModifier[eIndex];
}


void CvCity::changeBonusCommerceRateModifier(CommerceTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");

	if (iChange != 0)
	{
		m_aiBonusCommerceRateModifier[eIndex] = (m_aiBonusCommerceRateModifier[eIndex] + iChange);
		FAssert(getCommerceRate(eIndex) >= 0);

		GET_PLAYER(getOwnerINLINE()).invalidateCommerceRankCache(eIndex);

		updateCommerce(eIndex);

		AI_setAssignWorkDirty(true);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);
		}
	}
}


int CvCity::getTradeYield(YieldTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");
	return m_aiTradeYield[eIndex];
}


int CvCity::totalTradeModifier(CvCity* pOtherCity) const
{
	int iModifier = 100;

	iModifier += getTradeRouteModifier();

	iModifier += getPopulationTradeModifier();

	if (isConnectedToCapital())
	{
		iModifier += GC.getDefineINT("CAPITAL_TRADE_MODIFIER");
	}

	if (NULL != pOtherCity)
	{
	    // Leoreth: includes Porcelain Tower effect
		if (area() != pOtherCity->area() || GET_PLAYER(getOwner()).isHasBuilding((BuildingTypes)PORCELAIN_TOWER))
		{
			iModifier += GC.getDefineINT("OVERSEAS_TRADE_MODIFIER");
		}

        // Leoreth: includes Porcelain Tower effect
		if ((getTeam() != pOtherCity->getTeam() && !GET_PLAYER(getOwner()).isNoForeignTradeModifier()) || GET_PLAYER(getOwner()).isHasBuilding((BuildingTypes)PORCELAIN_TOWER))
		{
			iModifier += getForeignTradeRouteModifier();

			iModifier += getPeaceTradeModifier(pOtherCity->getTeam());
		}

		// Leoreth: new distance modifier
		iModifier += getDistanceTradeModifier(pOtherCity);

		// Leoreth: new modifier for trade routes with capital
		iModifier += getCapitalTradeModifier(pOtherCity);

		// Leoreth: new modifier for trade routes with defensive pact partners
		iModifier += getDefensivePactTradeModifier(pOtherCity);
	}

	return iModifier;
}

int CvCity::getCapitalTradeModifier(CvCity* pOtherCity) const
{
	if (pOtherCity == NULL) return 0;

	if (isCapital() || (pOtherCity->getOwner() == getOwner() && pOtherCity->isCapital()))
	{
		return GET_PLAYER(getOwner()).getCapitalTradeModifier();
	}

	return 0;
}

int CvCity::getDefensivePactTradeModifier(CvCity* pOtherCity) const
{
	if (GET_TEAM(getTeam()).isDefensivePact(pOtherCity->getTeam()))
	{
		return GET_PLAYER(getOwner()).getDefensivePactTradeModifier();
	}

	return 0;
}

int CvCity::getDistanceTradeModifier(CvCity* pOtherCity) const
{
	if (pOtherCity == NULL) return 0;
	
	int iDistance = stepDistance(getX_INLINE(), getY_INLINE(), pOtherCity->getX_INLINE(), pOtherCity->getY_INLINE());
	iDistance /= 5;
	iDistance *= 5;
		
	return iDistance * GC.getDefineINT("DISTANCE_TRADE_MODIFIER");
}

int CvCity::getPopulationTradeModifier() const
{
	return std::max(0, (getPopulation() + GC.getDefineINT("OUR_POPULATION_TRADE_MODIFIER_OFFSET")) * GC.getDefineINT("OUR_POPULATION_TRADE_MODIFIER"));
}

int CvCity::getPeaceTradeModifier(TeamTypes eTeam) const
{
	FAssert(NO_TEAM != eTeam);
	FAssert(eTeam != getTeam());

	if (atWar(eTeam, getTeam()))
	{
		return 0;
	}

	int iPeaceTurns = std::min(GC.getDefineINT("FOREIGN_TRADE_FULL_CREDIT_PEACE_TURNS"), GET_TEAM(getTeam()).AI_getAtPeaceCounter(eTeam));

	if (GC.getGameINLINE().getElapsedGameTurns() <= iPeaceTurns)
	{
		return GC.getDefineINT("FOREIGN_TRADE_MODIFIER");
	}

	return ((GC.getDefineINT("FOREIGN_TRADE_MODIFIER") * iPeaceTurns) / std::max(1, GC.getDefineINT("FOREIGN_TRADE_FULL_CREDIT_PEACE_TURNS")));
}

int CvCity::getBaseTradeProfit(CvCity* pCity) const
{
	int iProfit = std::min(pCity->getPopulation() * GC.getDefineINT("THEIR_POPULATION_TRADE_PERCENT"), plotDistance(getX_INLINE(), getY_INLINE(), pCity->getX_INLINE(), pCity->getY_INLINE()) * GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getTradeProfitPercent());

	iProfit *= GC.getDefineINT("TRADE_PROFIT_PERCENT");
	iProfit /= 100;

	iProfit = std::max(100, iProfit);

	return iProfit;
}

// BUG - Fractional Trade Routes - start
#ifdef _MOD_FRACTRADE

// Note: getBaseTradeProfit() already returns a times-100 value.

/*
 * Returns the fractional (times 100) trade profit for the route to the given city.
 */
int CvCity::calculateTradeProfitTimes100(CvCity* pCity) const
{
	int iProfit = getBaseTradeProfit(pCity);

	iProfit *= totalTradeModifier(pCity);
	iProfit /= 100;

	return iProfit;
}

/*
 * Returns the truncated trade profit for the route to the given city.
 *
 * This function is kept only for old Python code.
 */
int CvCity::calculateTradeProfit(CvCity* pCity) const
{
	return calculateTradeProfitTimes100(pCity) / 100;
}

#else

// unchanged

int CvCity::calculateTradeProfit(CvCity* pCity) const
{
	int iProfit = getBaseTradeProfit(pCity);

	iProfit *= totalTradeModifier(pCity);
	iProfit /= 10000;

	return iProfit;
}

#endif
// BUG - Fractional Trade Routes - end

int CvCity::calculateTradeYield(YieldTypes eIndex, int iTradeProfit) const
{
	if ((iTradeProfit > 0) && (GET_PLAYER(getOwnerINLINE()).getTradeYieldModifier(eIndex) > 0))
	{
		return ((iTradeProfit * GET_PLAYER(getOwnerINLINE()).getTradeYieldModifier(eIndex)) / 100);
	}
	else
	{
		return 0;
	}
}

// BUG - Trade Totals - start
/*
 * Adds the yield and count for each trade route with eWithPlayer.
 *
 * The yield and counts are not reset to zero.
 * If Fractional Trade Routes is enabled and bRound is false, or if bBase if true, the yield values are left times 100.
 */
void CvCity::calculateTradeTotals(YieldTypes eIndex, int& iDomesticYield, int& iDomesticRoutes, int& iForeignYield, int& iForeignRoutes, PlayerTypes eWithPlayer, bool bRound, bool bBase) const
{
	if (!isDisorder())
	{
		int iCityDomesticYield = 0;
		int iCityDomesticRoutes = 0;
		int iCityForeignYield = 0;
		int iCityForeignRoutes = 0;
		int iNumTradeRoutes = getTradeRoutes();
		PlayerTypes ePlayer = getOwnerINLINE();

		for (int iI = 0; iI < iNumTradeRoutes; ++iI)
		{
			CvCity* pTradeCity = getTradeCity(iI);
			if (pTradeCity && pTradeCity->getOwnerINLINE() >= 0 && (NO_PLAYER == eWithPlayer || pTradeCity->getOwnerINLINE() == eWithPlayer))
			{
				int iTradeYield;

				if (bBase)
				{
					iTradeYield = getBaseTradeProfit(pTradeCity);
				}
				else
				{
// BUG - Fractional Trade Routes - start
#ifdef _MOD_FRACTRADE
					int iTradeProfit = calculateTradeProfitTimes100(pTradeCity);
#else
					int iTradeProfit = calculateTradeProfit(pTradeCity);
#endif
// BUG - Fractional Trade Routes - end
					iTradeYield = calculateTradeYield(YIELD_COMMERCE, iTradeProfit);
				}

				if (pTradeCity->getOwnerINLINE() == ePlayer)
				{
					iCityDomesticYield += iTradeYield;
					iCityDomesticRoutes++;
				}
				else
				{
					iCityForeignYield += iTradeYield;
					iCityForeignRoutes++;
				}
			}
		}

// BUG - Fractional Trade Routes - start
#ifdef _MOD_FRACTRADE
		if (bRound)
		{
			iDomesticYield += iCityDomesticYield / 100;
			iDomesticRoutes += iCityDomesticRoutes / 100;
			iForeignYield += iCityForeignYield / 100;
			iForeignRoutes += iCityForeignRoutes / 100;
		}
		else
#endif
// BUG - Fractional Trade Routes - end
		{
			iDomesticYield += iCityDomesticYield;
			iDomesticRoutes += iCityDomesticRoutes;
			iForeignYield += iCityForeignYield;
			iForeignRoutes += iCityForeignRoutes;
		}
	}
}

/*
 * Returns the total trade yield.
 *
 * If Fractional Trade Routes is enabled or bBase is true, the yield value is left times 100.
 * UNUSED
 */
int CvCity::calculateTotalTradeYield(YieldTypes eIndex, PlayerTypes eWithPlayer, bool bRound, bool bBase) const
{
	int iDomesticYield = 0;
	int iDomesticRoutes = 0;
	int iForeignYield = 0;
	int iForeignRoutes = 0;
	
	calculateTradeTotals(eIndex, iDomesticYield, iDomesticRoutes, iForeignYield, iForeignRoutes, eWithPlayer, bRound, bBase);
	return iDomesticYield + iForeignRoutes;
}
// BUG - Trade Totals - end


void CvCity::setTradeYield(YieldTypes eIndex, int iNewValue)
{
	int iOldValue;

	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");

	iOldValue = getTradeYield(eIndex);

	if (iOldValue != iNewValue)
	{
		m_aiTradeYield[eIndex] = iNewValue;
		FAssert(getTradeYield(eIndex) >= 0);

		changeBaseYieldRate(eIndex, (iNewValue - iOldValue));
		// Leoreth: catch the overflow bug
		if (getBaseYieldRate(eIndex) < 0 || getBaseYieldRate(eIndex) > 1000) {
				GC.getGame().logMsg("Overflow in (%d, %d) for setTradeYield", getX(), getY());
			gDLL->getInterfaceIFace()->addMessage(GC.getGame().getActivePlayer(), true, GC.getEVENT_MESSAGE_TIME(), gDLL->getText("TXT_KEY_OVERFLOW", getX(), getY(), "setTradeYield()"), "", MESSAGE_TYPE_MAJOR_EVENT, ARTFILEMGR.getInterfaceArtInfo("WORLDBUILDER_CITY_EDIT")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_RED"), getX_INLINE(), getY_INLINE(), true, true);
			GC.getGame().setAIAutoPlay(0);
			GC.getGame().setAIAutoPlayCatapult(0);
			gDLL->getEngineIFace()->AutoSave(true);
		}
	}
}


int CvCity::getExtraSpecialistYield(YieldTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");
	return m_aiExtraSpecialistYield[eIndex];
}


int CvCity::getExtraSpecialistYield(YieldTypes eIndex, SpecialistTypes eSpecialist) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");
	FAssertMsg(eSpecialist >= 0, "eSpecialist expected to be >= 0");
	FAssertMsg(eSpecialist < GC.getNumSpecialistInfos(), "GC.getNumSpecialistInfos expected to be >= 0");

	if (eSpecialist == (SpecialistTypes)GC.getInfoTypeForString("SPECIALIST_SLAVE"))
		return 0;

	return ((getSpecialistCount(eSpecialist) + getFreeSpecialistCount(eSpecialist)) * (GET_PLAYER(getOwnerINLINE()).getSpecialistExtraYield(eSpecialist, eIndex)));
}

int CvCity::getExtraSpecialistThresholdYield(YieldTypes eIndex, SpecialistTypes eSpecialist) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");
	FAssertMsg(eSpecialist >= 0, "eSpecialist expected to be >= 0");
	FAssertMsg(eSpecialist < GC.getNumSpecialistInfos(), "GC.getNumSpecialistInfos expected to be >= 0");
	if (isSpecialistExtraYieldThreshold() && eSpecialist != (SpecialistTypes)GC.getInfoTypeForString("SPECIALIST_SLAVE"))
	{
		return ((std::min(getSpecialistCount(eSpecialist), (eSpecialist != GC.getInfoTypeForString("SPECIALIST_CITIZEN")? getMaxSpecialistCount(eSpecialist) : getSpecialistCount(eSpecialist))) + getFreeSpecialistCount(eSpecialist)) * (GET_PLAYER(getOwnerINLINE()).getSpecialistThresholdExtraYield(eSpecialist, eIndex)));
	}
	else
	{
		return 0;
	}
}

bool CvCity::isSpecialistExtraYieldThreshold() const
{
	CvPlot* pLoopPlot;
	int iCount = 0;
	int iBaseThreshold = GET_PLAYER(getOwner()).getSpecialistExtraYieldBaseThreshold();
	int iEraThreshold = GET_PLAYER(getOwner()).getSpecialistExtraYieldEraThreshold();

	if (iBaseThreshold == 0 && iEraThreshold == 0)
	{
		return false;
	}

	for (int iI = 0; iI < NUM_CITY_PLOTS; iI++)
	{
		pLoopPlot = getCityIndexPlot(iI);

		if (pLoopPlot->getWorkingCity() == this && pLoopPlot->isBeingWorked() && !pLoopPlot->isWater())
		{
			iCount++;
		}
	}

	iCount--; // city tile shouldn't count

	if (iCount <= iBaseThreshold + iEraThreshold * GET_PLAYER(getOwner()).getCurrentEra())
	{
		return true;
	}

	return false;
}


void CvCity::updateExtraSpecialistYield(YieldTypes eYield)
{
	int iOldYield;
	int iNewYield;
	int iI;

	FAssertMsg(eYield >= 0, "eYield expected to be >= 0");
	FAssertMsg(eYield < NUM_YIELD_TYPES, "eYield expected to be < NUM_YIELD_TYPES");

	iOldYield = getExtraSpecialistYield(eYield);

	iNewYield = 0;

	for (iI = 0; iI < GC.getNumSpecialistInfos(); iI++)
	{
		iNewYield += getExtraSpecialistYield(eYield, ((SpecialistTypes)iI));
		iNewYield += getExtraSpecialistThresholdYield(eYield, ((SpecialistTypes)iI));
	}

	if (iOldYield != iNewYield)
	{
		m_aiExtraSpecialistYield[eYield] = iNewYield;
		FAssert(getExtraSpecialistYield(eYield) >= 0);

		changeBaseYieldRate(eYield, (iNewYield - iOldYield));
		// Leoreth: catch the overflow bug
		if (getBaseYieldRate(eYield) < 0 || getBaseYieldRate(eYield) > 1000) {
				GC.getGame().logMsg("Overflow in (%d, %d) for updateExtraSpecialistYield", getX(), getY());
			gDLL->getInterfaceIFace()->addMessage(GC.getGame().getActivePlayer(), true, GC.getEVENT_MESSAGE_TIME(), gDLL->getText("TXT_KEY_OVERFLOW", getX(), getY(), "updateExtraSpecialistYield()"), "", MESSAGE_TYPE_MAJOR_EVENT, ARTFILEMGR.getInterfaceArtInfo("WORLDBUILDER_CITY_EDIT")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_RED"), getX_INLINE(), getY_INLINE(), true, true);
			GC.getGame().setAIAutoPlay(0);
			GC.getGame().setAIAutoPlayCatapult(0);
			gDLL->getEngineIFace()->AutoSave(true);
		}
	}
}


void CvCity::updateExtraSpecialistYield()
{
	int iI;

	for (iI = 0; iI < NUM_YIELD_TYPES; iI++)
	{
		updateExtraSpecialistYield((YieldTypes)iI);
	}
}


int CvCity::getCommerceRate(CommerceTypes eIndex) const
{
	return getCommerceRateTimes100(eIndex) / 100;
}

int CvCity::getCommerceRateTimes100(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");

	int iRate = m_aiCommerceRate[eIndex];
	if (GC.getGameINLINE().isOption(GAMEOPTION_NO_ESPIONAGE))
	{
		if (eIndex == COMMERCE_CULTURE)
		{
			iRate += m_aiCommerceRate[COMMERCE_ESPIONAGE];
		}
		else if (eIndex == COMMERCE_ESPIONAGE)
		{
			iRate = 0;
		}
	}

	return iRate;
}


int CvCity::getCommerceFromPercent(CommerceTypes eIndex, int iYieldRate) const
{
	int iCommerce;

	iCommerce = ((iYieldRate * GET_PLAYER(getOwnerINLINE()).getCommercePercent(eIndex)) / 100);

	if (eIndex == COMMERCE_GOLD)
	{
	    // Leoreth: Byzantine espionage bonus gets subtracted from income to (as commerce spent on espionage), so counterbalance it DISABLED
	    /*if ((int) getOwner() == BYZANTIUM)
	    {
	        iCommerce += (iYieldRate - iCommerce - getCommerceFromPercent(COMMERCE_RESEARCH, iYieldRate) - getCommerceFromPercent(COMMERCE_CULTURE, iYieldRate) - getCommerceFromPercent(COMMERCE_ESPIONAGE, iYieldRate) + 200 * (int)getCultureLevel());
	    }else*/
	    //{
        iCommerce += (iYieldRate - iCommerce - getCommerceFromPercent(COMMERCE_RESEARCH, iYieldRate) - getCommerceFromPercent(COMMERCE_CULTURE, iYieldRate) - getCommerceFromPercent(COMMERCE_ESPIONAGE, iYieldRate));
	    //}
	}

	// Leoreth: Byzantine UP DISABLED
	/*if ((int)getOwner() == BYZANTIUM)
	{
        if (eIndex == COMMERCE_ESPIONAGE)
        {
            iCommerce += 200 * (int)getCultureLevel();
        }
	}*/

	return iCommerce;
}


int CvCity::getBaseCommerceRate(CommerceTypes eIndex) const
{
	return (getBaseCommerceRateTimes100(eIndex) / 100);
}

int CvCity::getBaseCommerceRateTimes100(CommerceTypes eIndex) const
{
	int iBaseCommerceRate;

	iBaseCommerceRate = getCommerceFromPercent(eIndex, getYieldRate(YIELD_COMMERCE) * 100);

	iBaseCommerceRate += 100 * ((getSpecialistPopulation() + getNumGreatPeople() - getFreeSpecialistCount((SpecialistTypes)GC.getInfoTypeForString("SPECIALIST_SLAVE"))) * GET_PLAYER(getOwnerINLINE()).getSpecialistExtraCommerce(eIndex));
	iBaseCommerceRate += 100 * (getBuildingCommerce(eIndex) + getSpecialistCommerce(eIndex) + getReligionCommerce(eIndex) + getCorporationCommerce(eIndex) + GET_PLAYER(getOwnerINLINE()).getFreeCityCommerce(eIndex));

	// Leoreth: Himeji Castle effect
	if (eIndex == COMMERCE_CULTURE && isHasRealBuilding((BuildingTypes)HIMEJI_CASTLE) && GET_PLAYER(getOwnerINLINE()).isHasBuildingEffect((BuildingTypes)HIMEJI_CASTLE))
	{
		CvUnit* pUnit;
		for (int i = 0; i < plot()->getNumUnits(); i++)
		{
			pUnit = plot()->getUnitByIndex(i);

			if (pUnit->getOwner() == getOwner() && pUnit->isFortifyable() && pUnit->getFortifyTurns() >= GC.getDefineINT("MAX_FORTIFY_TURNS"))
			{
				iBaseCommerceRate += 100 * pUnit->getLevel();
			}
		}
	}

	return iBaseCommerceRate;
}


int CvCity::getTotalCommerceRateModifier(CommerceTypes eIndex) const
{
	return std::max(0, (getCommerceRateModifier(eIndex) + GET_PLAYER(getOwnerINLINE()).getCommerceRateModifier(eIndex) + ((isCapital()) ? GET_PLAYER(getOwnerINLINE()).getCapitalCommerceRateModifier(eIndex) : 0) + getBonusCommerceRateModifier(eIndex) + 100)); // Leoreth
}


void CvCity::updateCommerce(CommerceTypes eIndex)
{
	int iOldCommerce;
	int iNewCommerce;

	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");

	iOldCommerce = m_aiCommerceRate[eIndex];

	if (isDisorder())
	{
		iNewCommerce = 0;
	}
	else
	{
		iNewCommerce = (getBaseCommerceRateTimes100(eIndex) * getTotalCommerceRateModifier(eIndex)) / 100;
		iNewCommerce += getBaseYieldRate(YIELD_PRODUCTION) * getProductionToCommerceModifier(eIndex); // Leoreth: no production modifiers for processes anymore
	}

	if (iOldCommerce != iNewCommerce)
	{
		m_aiCommerceRate[eIndex] = iNewCommerce;
		FAssert(m_aiCommerceRate[eIndex] >= 0);

		GET_PLAYER(getOwnerINLINE()).invalidateCommerceRankCache(eIndex);

		GET_PLAYER(getOwnerINLINE()).changeCommerceRate(eIndex, (iNewCommerce - iOldCommerce));

		if (isCitySelected())
		{
			gDLL->getInterfaceIFace()->setDirty(InfoPane_DIRTY_BIT, true );
			gDLL->getInterfaceIFace()->setDirty(CityScreen_DIRTY_BIT, true);
		}
	}
}


void CvCity::updateCommerce()
{
	GET_PLAYER(getOwnerINLINE()).invalidateYieldRankCache();

	for (int iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
	{
		updateCommerce((CommerceTypes)iI);
	}
}


int CvCity::getProductionToCommerceModifier(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");
	return m_aiProductionToCommerceModifier[eIndex];
}


void CvCity::changeProductionToCommerceModifier(CommerceTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");

	if (iChange != 0)
	{
		m_aiProductionToCommerceModifier[eIndex] = (m_aiProductionToCommerceModifier[eIndex] + iChange);

		updateCommerce(eIndex);
	}
}


int CvCity::getBuildingCommerce(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");
	return m_aiBuildingCommerce[eIndex];
}


int CvCity::getBuildingCommerceByBuilding(CommerceTypes eIndex, BuildingTypes eBuilding) const
{
	int iCommerce;

	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");
	FAssertMsg(eBuilding >= 0, "eBuilding expected to be >= 0");
	FAssertMsg(eBuilding < GC.getNumBuildingInfos(), "GC.getNumBuildingInfos expected to be >= 0");

	iCommerce = 0;

	if (getNumBuilding(eBuilding) > 0)
	{
		CvBuildingInfo& kBuilding = GC.getBuildingInfo(eBuilding);
		if (!(kBuilding.isCommerceChangeOriginalOwner(eIndex)) || (getBuildingOriginalOwner(eBuilding) == getOwnerINLINE()))
		{
			iCommerce += kBuilding.getObsoleteSafeCommerceChange(eIndex) * getNumBuilding(eBuilding);

			if (getNumActiveBuilding(eBuilding) > 0)
			{
				iCommerce += (GC.getBuildingInfo(eBuilding).getCommerceChange(eIndex) + getBuildingCommerceChange((BuildingClassTypes)GC.getBuildingInfo(eBuilding).getBuildingClassType(), eIndex)) * getNumActiveBuilding(eBuilding);

				if (GC.getBuildingInfo(eBuilding).getReligionType() != NO_RELIGION)
				{
					if (GC.getBuildingInfo(eBuilding).getReligionType() == GET_PLAYER(getOwnerINLINE()).getStateReligion())
					{
						iCommerce += GET_PLAYER(getOwnerINLINE()).getStateReligionBuildingCommerce(eIndex) * getNumActiveBuilding(eBuilding);
					}
				}

				if (GC.getBuildingInfo(eBuilding).getGlobalReligionCommerce() != NO_RELIGION)
				{
				    // modified by Leoreth to account for Solomon's Temple's effect
				    int limit;
				    if (GET_PLAYER(getOwner()).isHasBuildingEffect((BuildingTypes)DOME_OF_THE_ROCK))
				    {
				        limit = MAX_COM_SHRINE*2;
				    }
				    else
				    {
				        limit = MAX_COM_SHRINE;
				    }
                    //Rhye - start (max commerce from a shrine)
                    //iCommerce += (GC.getReligionInfo((ReligionTypes)(GC.getBuildingInfo(eBuilding).getGlobalReligionCommerce())).getGlobalReligionCommerce(eIndex) * GC.getGameINLINE().countReligionLevels((ReligionTypes)(GC.getBuildingInfo(eBuilding).getGlobalReligionCommerce())));
                    iCommerce += std::min(limit, (GC.getReligionInfo((ReligionTypes)(GC.getBuildingInfo(eBuilding).getGlobalReligionCommerce())).getGlobalReligionCommerce(eIndex) * GC.getGameINLINE().countReligionLevels((ReligionTypes)(GC.getBuildingInfo(eBuilding).getGlobalReligionCommerce()))));
                    //Rhye - end
				}

				if (GC.getBuildingInfo(eBuilding).getGlobalCorporationCommerce() != NO_CORPORATION)
				{
					iCommerce += (GC.getCorporationInfo((CorporationTypes)(GC.getBuildingInfo(eBuilding).getGlobalCorporationCommerce())).getHeadquarterCommerce(eIndex) * GC.getGameINLINE().countCorporationLevels((CorporationTypes)(GC.getBuildingInfo(eBuilding).getGlobalCorporationCommerce()))) * getNumActiveBuilding(eBuilding);
				}
			}

			if ((GC.getBuildingInfo(eBuilding).getCommerceChangeDoubleTime(eIndex) != 0) &&
				(getBuildingOriginalTime(eBuilding) != MIN_INT) &&
				((GC.getGameINLINE().getGameTurnYear() - getBuildingOriginalTime(eBuilding)) >= GC.getBuildingInfo(eBuilding).getCommerceChangeDoubleTime(eIndex)))
			{
				return (iCommerce * 2);
			}

			return iCommerce;
		}
	}

	return 0;
}

// BUG - Building Additional Commerce - start
/*
 * Returns the rounded total additional commerce that adding one of the given buildings will provide.
 *
 * Doesn't check if the building can be constructed in this city.
 * Takes the NO_ESPIONAGE game option into account for CULTURE and ESPIONAGE.
 */
int CvCity::getAdditionalCommerceByBuilding(CommerceTypes eIndex, BuildingTypes eBuilding) const
{
	return getAdditionalCommerceTimes100ByBuilding(eIndex, eBuilding) / 100;
}

/*
 * Returns the total additional commerce times 100 that adding one of the given buildings will provide.
 *
 * Doesn't check if the building can be constructed in this city.
 * Takes the NO_ESPIONAGE game option into account for CULTURE and ESPIONAGE.
 */
int CvCity::getAdditionalCommerceTimes100ByBuilding(CommerceTypes eIndex, BuildingTypes eBuilding) const
{
	int iExtraRate = getAdditionalBaseCommerceRateByBuilding(eIndex, eBuilding);
	int iExtraModifier = getAdditionalCommerceRateModifierByBuilding(eIndex, eBuilding);
	if (iExtraRate == 0 && iExtraModifier == 0)
	{
		return 0;
	}

	int iRateTimes100 = getBaseCommerceRateTimes100(eIndex);
	int iModifier = getTotalCommerceRateModifier(eIndex);
	int iExtraTimes100 = ((iModifier + iExtraModifier) * (100 * iExtraRate + iRateTimes100) / 100) - (iModifier * iRateTimes100 / 100);

	return iExtraTimes100;
}

/*
 * Returns the additional base commerce rate constructing the given building will provide.
 *
 * Doesn't check if the building can be constructed in this city.
 * Takes the NO_ESPIONAGE game option into account for CULTURE and ESPIONAGE.
 */
int CvCity::getAdditionalBaseCommerceRateByBuilding(CommerceTypes eIndex, BuildingTypes eBuilding) const
{
	bool bNoEspionage = GC.getGameINLINE().isOption(GAMEOPTION_NO_ESPIONAGE);
	if (bNoEspionage && eIndex == COMMERCE_ESPIONAGE)
	{
		return 0;
	}

	int iExtraRate = getAdditionalBaseCommerceRateByBuildingImpl(eIndex, eBuilding);
	if (bNoEspionage && eIndex == COMMERCE_CULTURE)
	{
		iExtraRate += getAdditionalBaseCommerceRateByBuildingImpl(COMMERCE_ESPIONAGE, eBuilding);
	}
	return iExtraRate;
}

/*
 * Returns the additional base commerce rate constructing the given building will provide.
 *
 * Doesn't check if the building can be constructed in this city.
 */
int CvCity::getAdditionalBaseCommerceRateByBuildingImpl(CommerceTypes eIndex, BuildingTypes eBuilding) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");
	FAssertMsg(eBuilding >= 0, "eBuilding expected to be >= 0");
	FAssertMsg(eBuilding < GC.getNumBuildingInfos(), "eBuilding expected to be < GC.getNumBuildingInfos()");

	CvBuildingInfo& kBuilding = GC.getBuildingInfo(eBuilding);
	bool bObsolete = GET_TEAM(getTeam()).isObsoleteBuilding(eBuilding);
	int iExtraRate = 0;

	iExtraRate += kBuilding.getObsoleteSafeCommerceChange(eIndex);
	if (!bObsolete)
	{
		iExtraRate += kBuilding.getCommerceChange(eIndex);
		iExtraRate += getBuildingCommerceChange((BuildingClassTypes)kBuilding.getBuildingClassType(), eIndex);
		if (kBuilding.getReligionType() != NO_RELIGION)
		{
			if (kBuilding.getReligionType() == GET_PLAYER(getOwnerINLINE()).getStateReligion())
			{
				iExtraRate += GET_PLAYER(getOwnerINLINE()).getStateReligionBuildingCommerce(eIndex);
			}
		}
		if (kBuilding.getGlobalReligionCommerce() != NO_RELIGION)
		{
			iExtraRate += GC.getReligionInfo((ReligionTypes)(kBuilding.getGlobalReligionCommerce())).getGlobalReligionCommerce(eIndex) * GC.getGameINLINE().countReligionLevels((ReligionTypes)(kBuilding.getGlobalReligionCommerce()));
		}
		if (kBuilding.getGlobalCorporationCommerce() != NO_CORPORATION)
		{
			iExtraRate += GC.getCorporationInfo((CorporationTypes)(kBuilding.getGlobalCorporationCommerce())).getHeadquarterCommerce(eIndex) * GC.getGameINLINE().countCorporationLevels((CorporationTypes)(kBuilding.getGlobalCorporationCommerce()));
		}
		// ignore double-time check since this assumes you are building it this turn

		// Specialists
		for (int iI = 0; iI < GC.getNumSpecialistInfos(); ++iI)
		{
			if (kBuilding.getFreeSpecialistCount((SpecialistTypes)iI) != 0)
			{
				iExtraRate += getAdditionalBaseCommerceRateBySpecialistImpl(eIndex, (SpecialistTypes)iI, kBuilding.getFreeSpecialistCount((SpecialistTypes)iI));
			}
		}
	}
	
	return iExtraRate;
}

/*
 * Returns the additional commerce rate modifier constructing the given building will provide.
 *
 * Doesn't check if the building can be constructed in this city.
 * Takes the NO_ESPIONAGE game option into account for CULTURE and ESPIONAGE.
 */
int CvCity::getAdditionalCommerceRateModifierByBuilding(CommerceTypes eIndex, BuildingTypes eBuilding) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");
	FAssertMsg(eBuilding >= 0, "eBuilding expected to be >= 0");
	FAssertMsg(eBuilding < GC.getNumBuildingInfos(), "eBuilding expected to be < GC.getNumBuildingInfos()");

	bool bNoEspionage = GC.getGameINLINE().isOption(GAMEOPTION_NO_ESPIONAGE);
	if (bNoEspionage && eIndex == COMMERCE_ESPIONAGE)
	{
		return 0;
	}

	int iExtraModifier = getAdditionalCommerceRateModifierByBuildingImpl(eIndex, eBuilding);
	if (bNoEspionage && eIndex == COMMERCE_CULTURE)
	{
		iExtraModifier += getAdditionalCommerceRateModifierByBuildingImpl(COMMERCE_ESPIONAGE, eBuilding);
	}
	return iExtraModifier;
}

/*
 * Returns the additional commerce rate modifier constructing the given building will provide.
 *
 * Doesn't check if the building can be constructed in this city.
 */
int CvCity::getAdditionalCommerceRateModifierByBuildingImpl(CommerceTypes eIndex, BuildingTypes eBuilding) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");
	FAssertMsg(eBuilding >= 0, "eBuilding expected to be >= 0");
	FAssertMsg(eBuilding < GC.getNumBuildingInfos(), "eBuilding expected to be < GC.getNumBuildingInfos()");

	CvBuildingInfo& kBuilding = GC.getBuildingInfo(eBuilding);
	bool bObsolete = GET_TEAM(getTeam()).isObsoleteBuilding(eBuilding);
	int iExtraModifier = 0;

	if (!bObsolete)
	{
		iExtraModifier += kBuilding.getCommerceModifier(eIndex);
		iExtraModifier += kBuilding.getGlobalCommerceModifier(eIndex);
	}
	
	return iExtraModifier;
}
// BUG - Building Additional Commerce - end

void CvCity::updateBuildingCommerce()
{
	int iNewBuildingCommerce;
	int iI, iJ;

	for (iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
	{
		iNewBuildingCommerce = 0;

		for (iJ = 0; iJ < GC.getNumBuildingInfos(); iJ++)
		{
			iNewBuildingCommerce += getBuildingCommerceByBuilding(((CommerceTypes)iI), ((BuildingTypes)iJ));
		}

		if (getBuildingCommerce((CommerceTypes)iI) != iNewBuildingCommerce)
		{
			m_aiBuildingCommerce[iI] = iNewBuildingCommerce;
			FAssert(getBuildingCommerce((CommerceTypes)iI) >= 0);

			updateCommerce((CommerceTypes)iI);
		}
	}
}


int CvCity::getSpecialistCommerce(CommerceTypes eIndex)	const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");
	return m_aiSpecialistCommerce[eIndex];
}


void CvCity::changeSpecialistCommerce(CommerceTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");

	if (iChange != 0)
	{
		m_aiSpecialistCommerce[eIndex] = (m_aiSpecialistCommerce[eIndex] + iChange);
		FAssert(getSpecialistCommerce(eIndex) >= 0);

		updateCommerce(eIndex);
	}
}


// BUG - Specialist Additional Commerce - start
/*
 * Returns the total additional commerce that changing the number of given specialists will provide/remove.
 *
 * Takes the NO_ESPIONAGE game option into account for CULTURE and ESPIONAGE.
 */
int CvCity::getAdditionalCommerceBySpecialist(CommerceTypes eIndex, SpecialistTypes eSpecialist, int iChange) const
{
	return getAdditionalCommerceTimes100BySpecialist(eIndex, eSpecialist, iChange) / 100;
}

/*
 * Returns the total additional commerce times 100 that changing the number of given specialists will provide/remove.
 *
 * Takes the NO_ESPIONAGE game option into account for CULTURE and ESPIONAGE.
 */
int CvCity::getAdditionalCommerceTimes100BySpecialist(CommerceTypes eIndex, SpecialistTypes eSpecialist, int iChange) const
{
	int iExtraRate = getAdditionalBaseCommerceRateBySpecialist(eIndex, eSpecialist, iChange);
	if (iExtraRate == 0)
	{
		return 0;
	}

	int iRateTimes100 = getBaseCommerceRateTimes100(eIndex);
	int iModifier = getTotalCommerceRateModifier(eIndex);
	int iExtraTimes100 = (iModifier * (100 * iExtraRate + iRateTimes100) / 100) - (iModifier * iRateTimes100 / 100);

	return iExtraTimes100;
}

/*
 * Returns the additional base commerce rate that changing the number of given specialists will provide/remove.
 *
 * Takes the NO_ESPIONAGE game option into account for CULTURE and ESPIONAGE.
 */
int CvCity::getAdditionalBaseCommerceRateBySpecialist(CommerceTypes eIndex, SpecialistTypes eSpecialist, int iChange) const
{
	bool bNoEspionage = GC.getGameINLINE().isOption(GAMEOPTION_NO_ESPIONAGE);
	if (bNoEspionage && eIndex == COMMERCE_ESPIONAGE)
	{
		return 0;
	}

	int iExtraRate = getAdditionalBaseCommerceRateBySpecialistImpl(eIndex, eSpecialist, iChange);
	if (bNoEspionage && eIndex == COMMERCE_CULTURE)
	{
		iExtraRate += getAdditionalBaseCommerceRateBySpecialistImpl(COMMERCE_ESPIONAGE, eSpecialist, iChange);
	}
	return iExtraRate;
}

/*
 * Returns the additional base commerce rate that changing the number of given specialists will provide/remove.
 */
int CvCity::getAdditionalBaseCommerceRateBySpecialistImpl(CommerceTypes eIndex, SpecialistTypes eSpecialist, int iChange) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");
	FAssertMsg(eSpecialist >= 0, "eSpecialist expected to be >= 0");
	FAssertMsg(eSpecialist < GC.getNumSpecialistInfos(), "eSpecialist expected to be < GC.getNumSpecialistInfos()");

	CvSpecialistInfo& kSpecialist = GC.getSpecialistInfo(eSpecialist);
	return iChange * (kSpecialist.getCommerceChange(eIndex) + GET_PLAYER(getOwnerINLINE()).getSpecialistExtraCommerce(eIndex));
}
// BUG - Specialist Additional Commerce - end


int CvCity::getReligionCommerce(CommerceTypes eIndex) const												 
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");
	return m_aiReligionCommerce[eIndex];
}


int CvCity::getReligionCommerceByReligion(CommerceTypes eIndex, ReligionTypes eReligion) const
{
	int iCommerce;

	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");
	FAssertMsg(eReligion >= 0, "eReligion expected to be >= 0");
	FAssertMsg(eReligion < GC.getNumReligionInfos(), "GC.getNumReligionInfos expected to be >= 0");

	iCommerce = 0;

	if ((GET_PLAYER(getOwnerINLINE()).getStateReligion() == eReligion) || (GET_PLAYER(getOwnerINLINE()).getStateReligion() == NO_RELIGION))
	{
		if (isHasReligion(eReligion))
		{
			iCommerce += GC.getReligionInfo(eReligion).getStateReligionCommerce(eIndex);

			if (isHolyCity(eReligion))
			{
				iCommerce += GC.getReligionInfo(eReligion).getHolyCityCommerce(eIndex);
			}
		}
	}

	return iCommerce;
}


// XXX can this be simplified???
void CvCity::updateReligionCommerce(CommerceTypes eIndex)
{
	int iNewReligionCommerce;
	int iI;

	iNewReligionCommerce = 0;

	for (iI = 0; iI < GC.getNumReligionInfos(); iI++)
	{
		iNewReligionCommerce += getReligionCommerceByReligion(eIndex, ((ReligionTypes)iI));
	}

	if (getReligionCommerce(eIndex) != iNewReligionCommerce)
	{
		m_aiReligionCommerce[eIndex] = iNewReligionCommerce;
		FAssert(getReligionCommerce(eIndex) >= 0);

		updateCommerce(eIndex);
	}
}


void CvCity::updateReligionCommerce()
{
	int iI;

	for (iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
	{
		updateReligionCommerce((CommerceTypes)iI);
	}
}


int CvCity::getCorporationYield(YieldTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");
	return m_aiCorporationYield[eIndex];
}

void CvCity::setCorporationYield(YieldTypes eIndex, int iNewValue)
{
	int iOldValue;

	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");

	iOldValue = getCorporationYield(eIndex);

	if (iOldValue != iNewValue)
	{
		m_aiCorporationYield[eIndex] = iNewValue;
		FAssert(getCorporationYield(eIndex) >= 0);

		changeBaseYieldRate(eIndex, (iNewValue - iOldValue));
		// Leoreth: catch the overflow bug
		if (getBaseYieldRate(eIndex) < 0 || getBaseYieldRate(eIndex) > 1000) {
				GC.getGame().logMsg("Overflow in (%d, %d) for setCorporationYield", getX(), getY());
			gDLL->getInterfaceIFace()->addMessage(GC.getGame().getActivePlayer(), true, GC.getEVENT_MESSAGE_TIME(), gDLL->getText("TXT_KEY_OVERFLOW", getX(), getY(), "setCorporationYield()"), "", MESSAGE_TYPE_MAJOR_EVENT, ARTFILEMGR.getInterfaceArtInfo("WORLDBUILDER_CITY_EDIT")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_RED"), getX_INLINE(), getY_INLINE(), true, true);
			GC.getGame().setAIAutoPlay(0);
			GC.getGame().setAIAutoPlayCatapult(0);
			gDLL->getEngineIFace()->AutoSave(true);
		}
	}
}

int CvCity::getCorporationCommerce(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");
	return m_aiCorporationCommerce[eIndex];
}


int CvCity::getCorporationYieldByCorporation(YieldTypes eIndex, CorporationTypes eCorporation) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");
	FAssertMsg(eCorporation >= 0, "eCorporation expected to be >= 0");
	FAssertMsg(eCorporation < GC.getNumCorporationInfos(), "GC.getNumCorporationInfos expected to be >= 0");

	int iYield = 0;

	if (isActiveCorporation(eCorporation) && !isDisorder())
	{
		for (int i = 0; i < GC.getNUM_CORPORATION_PREREQ_BONUSES(); ++i)
		{
			BonusTypes eBonus = (BonusTypes)GC.getCorporationInfo(eCorporation).getPrereqBonus(i);
			if (NO_BONUS != eBonus && getNumBonuses(eBonus) > 0)
			{
				// Leoreth: Dutch UP
				if (getOwner() == (PlayerTypes)NETHERLANDS && eCorporation == (CorporationTypes)1) // trading company
				{
					iYield += 2 * (GC.getCorporationInfo(eCorporation).getYieldProduced(eIndex) * std::min(12, getNumBonuses(eBonus)) * GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getCorporationMaintenancePercent()) / 100;;
				}
				else
				{
					//iYield += (GC.getCorporationInfo(eCorporation).getYieldProduced(eIndex) * getNumBonuses(eBonus) * GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getCorporationMaintenancePercent()) / 100;
					iYield += (GC.getCorporationInfo(eCorporation).getYieldProduced(eIndex) * std::min(12, getNumBonuses(eBonus)) * GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getCorporationMaintenancePercent()) / 100; //Rhye - corporation cap
				}
			}
		}
	}

	return (iYield + 99) / 100;
}

int CvCity::getCorporationCommerceByCorporation(CommerceTypes eIndex, CorporationTypes eCorporation) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");
	FAssertMsg(eCorporation >= 0, "eCorporation expected to be >= 0");
	FAssertMsg(eCorporation < GC.getNumCorporationInfos(), "GC.getNumCorporationInfos expected to be >= 0");

	int iCommerce = 0;
	int iNumBonuses = 0;

	if (isActiveCorporation(eCorporation) && !isDisorder())
	{
		for (int i = 0; i < GC.getNUM_CORPORATION_PREREQ_BONUSES(); ++i)
		{
			BonusTypes eBonus = (BonusTypes)GC.getCorporationInfo(eCorporation).getPrereqBonus(i);
			iNumBonuses = getNumBonuses(eBonus);

			// Leoreth: Brazilian UP (sugar counts as oil for oil industry)
			if (getOwner() == BRAZIL && eBonus == BONUS_OIL && eCorporation == (CorporationTypes)6)
			{
				iNumBonuses += getNumBonuses(BONUS_SUGAR);
			}

			// Leoreth: includes Dutch UP (double yield from trading company)
			if (NO_BONUS != eBonus && iNumBonuses > 0)
			{
				//iCommerce += (GC.getCorporationInfo(eCorporation).getCommerceProduced(eIndex) * iNumBonuses * GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getCorporationMaintenancePercent()) / 100;
				iCommerce += ((getOwner() == NETHERLANDS && eCorporation == (CorporationTypes)1) ? 2 : 1) * (GC.getCorporationInfo(eCorporation).getCommerceProduced(eIndex) * std::min(12, getNumBonuses(eBonus)) * GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getCorporationMaintenancePercent()) / 100; //Rhye - corporation cap
			}
		}
	}

	if (GET_PLAYER(getOwner()).getCorporationCommerceModifier() < -100 || GET_PLAYER(getOwner()).getCorporationCommerceModifier() > 100)
	{
		GC.getGameINLINE().logMsg("OVERFLOW - corporation commerce modifier: %d", GET_PLAYER(getOwner()).getCorporationCommerceModifier());
	}
	else
	{
		//Leoreth: civic corporation commerce modifier
		iCommerce = iCommerce * (100 + GET_PLAYER(getOwner()).getCorporationCommerceModifier()) / 100;
	}

	

	return (iCommerce + 99) / 100;
}

void CvCity::updateCorporationCommerce(CommerceTypes eIndex)
{
	int iNewCommerce = 0;

	for (int iI = 0; iI < GC.getNumCorporationInfos(); iI++)
	{
		//iNewCommerce += getCorporationCommerceByCorporation(eIndex, ((CorporationTypes)iI)); //Rhye - corporation cap (headquarters)
		iNewCommerce += std::min(25, getCorporationCommerceByCorporation(eIndex, ((CorporationTypes)iI))); //Rhye - corporation cap (headquarters)
	}

	if (getCorporationCommerce(eIndex) != iNewCommerce)
	{
		m_aiCorporationCommerce[eIndex] = iNewCommerce;
		FAssert(getCorporationCommerce(eIndex) >= 0);

		updateCommerce(eIndex);
	}
}

void CvCity::updateCorporationYield(YieldTypes eIndex)
{
	int iOldYield = getCorporationYield(eIndex);
	int iNewYield = 0;

	for (int iI = 0; iI < GC.getNumCorporationInfos(); iI++)
	{
		//iNewYield += getCorporationYieldByCorporation(eIndex, (CorporationTypes)iI); //Rhye - corporation cap (headquarters)
		iNewYield += std::min(25, getCorporationYieldByCorporation(eIndex, (CorporationTypes)iI)); //Rhye - corporation cap (headquarters)
	}

	if (iNewYield > 1000 || iNewYield < -1000)
	{
		GC.getGameINLINE().logMsg("OVERFLOW: x=%d, y=%d", getX(), getY());
		GC.getGameINLINE().setAIAutoPlayCatapult(0);
	}

	if (iOldYield != iNewYield)
	{
		m_aiCorporationYield[eIndex] = iNewYield;
		FAssert(getCorporationYield(eIndex) >= 0);

		changeBaseYieldRate(eIndex, (iNewYield - iOldYield));
		// Leoreth: catch the overflow bug
		if (getBaseYieldRate(eIndex) < 0 || getBaseYieldRate(eIndex) > 1000) {
				GC.getGame().logMsg("Overflow in (%d, %d) for updateCorporationYield", getX(), getY());
			gDLL->getInterfaceIFace()->addMessage(GC.getGame().getActivePlayer(), true, GC.getEVENT_MESSAGE_TIME(), gDLL->getText("TXT_KEY_OVERFLOW", getX(), getY(), "updateCorporationYield()"), "", MESSAGE_TYPE_MAJOR_EVENT, ARTFILEMGR.getInterfaceArtInfo("WORLDBUILDER_CITY_EDIT")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_RED"), getX_INLINE(), getY_INLINE(), true, true);
			GC.getGame().setAIAutoPlay(0);
			GC.getGame().setAIAutoPlayCatapult(0);
			gDLL->getEngineIFace()->AutoSave(true);
		}
	}
}

// Leoreth
void CvCity::updateCorporationHappiness()
{
	int iHappiness;

	int iOldGoodHappiness = getCorporationGoodHappiness();
	int iNewGoodHappiness = 0;

	int iOldBadHappiness = getCorporationBadHappiness();
	int iNewBadHappiness = 0;

	for (int iI = 0; iI < GC.getNumCorporationInfos(); iI++)
	{
		iHappiness = getCorporationHappinessByCorporation((CorporationTypes)iI);

		if (iHappiness > 0)
		{
			iNewGoodHappiness += iHappiness;
		}

		if (iHappiness < 0)
		{
			iNewBadHappiness -= iHappiness;
		}
	}
	
	if (iOldGoodHappiness != iNewGoodHappiness)
	{
		m_iCorporationGoodHappiness = iNewGoodHappiness;
		FAssert(getCorporationGoodHappiness() >= 0);
	}

	if (iOldBadHappiness != iNewBadHappiness)
	{
		m_iCorporationBadHappiness = iNewBadHappiness;
		FAssert(getCorporationBadHappiness() >= 0);
	}
}


// Leoreth
void CvCity::updateCorporationHealth()
{
	int iHealth;

	int iOldHealth = getCorporationHealth();
	int iNewHealth = 0;

	int iOldUnhealth = getCorporationUnhealth();
	int iNewUnhealth = 0;

	for (int iI = 0; iI < GC.getNumCorporationInfos(); iI++)
	{
		iHealth = getCorporationHealthByCorporation((CorporationTypes)iI);

		if (iHealth > 0)
		{
			iNewHealth += iHealth;
		}

		if (iHealth < 0)
		{
			iNewUnhealth -= iHealth;
		}
	}

	if (iOldHealth != iNewHealth)
	{
		m_iCorporationHealth = iNewHealth;
		FAssert(getCorporationHealth() >= 0);
	}

	if (iOldUnhealth != iNewUnhealth)
	{
		m_iCorporationUnhealth = iNewUnhealth;
		FAssert(getCorporationUnhealth() >= 0);
	}
}


void CvCity::updateCorporation()
{
	updateCorporationBonus();

	updateBuildingCommerce();

	for (int iI = 0; iI < NUM_YIELD_TYPES; ++iI)
	{
		updateCorporationYield((YieldTypes)iI);
	}

	for (int iI = 0; iI < NUM_COMMERCE_TYPES; ++iI)
	{
		updateCorporationCommerce((CommerceTypes)iI);
	}

	updateMaintenance();

	updateCorporationHappiness();

	updateCorporationHealth();
}


void CvCity::updateCorporationBonus()
{
	std::vector<int> aiExtraCorpProducedBonuses;
	std::vector<int> aiLastCorpProducedBonuses;
	std::vector<bool> abHadBonuses;

	for (int iI = 0; iI < GC.getNumBonusInfos(); ++iI)
	{
		abHadBonuses.push_back(hasBonus((BonusTypes)iI));
		m_paiNumCorpProducedBonuses[iI] = 0;
		aiLastCorpProducedBonuses.push_back(getNumBonuses((BonusTypes)iI));
		aiExtraCorpProducedBonuses.push_back(0);
	}

	for (int iIter = 0; iIter < GC.getNumCorporationInfos(); ++iIter)
	{
		for (int iCorp = 0; iCorp < GC.getNumCorporationInfos(); ++iCorp)
		{
			int iBonusProduced = GC.getCorporationInfo((CorporationTypes)iCorp).getBonusProduced();

			if (NO_BONUS != iBonusProduced)
			{
				if (!GET_TEAM(getTeam()).isBonusObsolete((BonusTypes)iBonusProduced))
				{
					if (GET_TEAM(getTeam()).isHasTech((TechTypes)(GC.getBonusInfo((BonusTypes)iBonusProduced).getTechCityTrade())))
					{
						if (isHasCorporation((CorporationTypes)iCorp) && GET_PLAYER(getOwnerINLINE()).isActiveCorporation((CorporationTypes)iCorp))
						{
							for (int i = 0; i < GC.getNUM_CORPORATION_PREREQ_BONUSES(); ++i)
							{
								int iBonusConsumed = GC.getCorporationInfo((CorporationTypes)iCorp).getPrereqBonus(i);
								if (NO_BONUS != iBonusConsumed)
								{
									aiExtraCorpProducedBonuses[iBonusProduced] += aiLastCorpProducedBonuses[iBonusConsumed];
								}
							}
						}
					}
				}
			}
		}

		bool bChanged = false;

		for (int iI = 0; iI < GC.getNumBonusInfos(); ++iI)
		{
			if (aiExtraCorpProducedBonuses[iI] != 0)
			{
				m_paiNumCorpProducedBonuses[iI] += aiExtraCorpProducedBonuses[iI];

				bChanged = true;
			}

			aiLastCorpProducedBonuses[iI] = aiExtraCorpProducedBonuses[iI];
			aiExtraCorpProducedBonuses[iI] = 0;
		}

		if (!bChanged)
		{
			break;
		}

		FAssertMsg(iIter < GC.getNumCorporationInfos() - 1, "Corporation cyclical resource dependency");
	}

	for (int iI = 0; iI < GC.getNumBonusInfos(); ++iI)
	{
		if (abHadBonuses[iI] != hasBonus((BonusTypes)iI))
		{
			if (hasBonus((BonusTypes)iI))
			{
				processBonus((BonusTypes)iI, 1);
			}
			else
			{
				processBonus((BonusTypes)iI, -1);
			}
		}
	}
}


int CvCity::getCommerceRateModifier(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");
	return m_aiCommerceRateModifier[eIndex];
}


void CvCity::changeCommerceRateModifier(CommerceTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");

	if (iChange != 0)
	{
		m_aiCommerceRateModifier[eIndex] = (m_aiCommerceRateModifier[eIndex] + iChange);

		updateCommerce(eIndex);

		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getCommerceHappinessPer(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");

	return m_aiCommerceHappinessPer[eIndex];
}


int CvCity::getCommerceHappinessByType(CommerceTypes eCommerce) const
{
	int iHappiness = ((getCommerceHappinessPer(eCommerce) * GET_PLAYER(getOwnerINLINE()).getCommercePercent(eCommerce)) / 100);

	return iHappiness;
}


int CvCity::getCommerceHappiness() const
{
	int iHappiness;
	int iI;

	iHappiness = 0;

	for (iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
	{
		iHappiness += getCommerceHappinessByType((CommerceTypes)iI);
	}

	return iHappiness;
}


void CvCity::changeCommerceHappinessPer(CommerceTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");

	if (iChange != 0)
	{
		m_aiCommerceHappinessPer[eIndex] = (m_aiCommerceHappinessPer[eIndex] + iChange);
		FAssert(getCommerceHappinessPer(eIndex) >= 0);

		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getDomainFreeExperience(DomainTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_DOMAIN_TYPES, "eIndex expected to be < NUM_DOMAIN_TYPES");
	return m_aiDomainFreeExperience[eIndex];
}


void CvCity::changeDomainFreeExperience(DomainTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_DOMAIN_TYPES, "eIndex expected to be < NUM_DOMAIN_TYPES");
	m_aiDomainFreeExperience[eIndex] = (m_aiDomainFreeExperience[eIndex] + iChange);
	FAssert(getDomainFreeExperience(eIndex) >= 0);
}


int CvCity::getDomainProductionModifier(DomainTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_DOMAIN_TYPES, "eIndex expected to be < NUM_DOMAIN_TYPES");
	return m_aiDomainProductionModifier[eIndex];
}


void CvCity::changeDomainProductionModifier(DomainTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_DOMAIN_TYPES, "eIndex expected to be < NUM_DOMAIN_TYPES");
	m_aiDomainProductionModifier[eIndex] = (m_aiDomainProductionModifier[eIndex] + iChange);
}


int CvCity::getCulture(PlayerTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < MAX_PLAYERS, "eIndex expected to be < MAX_PLAYERS");

	return (m_aiCulture[eIndex]) / 100;
}

int CvCity::getCultureTimes100(PlayerTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < MAX_PLAYERS, "eIndex expected to be < MAX_PLAYERS");

	return m_aiCulture[eIndex];
}


int CvCity::countTotalCultureTimes100() const
{
	int iTotalCulture;
	int iI;

	iTotalCulture = 0;

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		//if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			iTotalCulture += getCultureTimes100((PlayerTypes)iI);
		}
	}

	return iTotalCulture;
}


PlayerTypes CvCity::findHighestCulture(bool bIgnoreMinors) const
{
	PlayerTypes eBestPlayer;
	int iValue;
	int iBestValue;
	int iI;

	iBestValue = 0;
	eBestPlayer = NO_PLAYER;

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (bIgnoreMinors && GET_PLAYER((PlayerTypes)iI).isMinorCiv()) continue;

		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			iValue = getCultureTimes100((PlayerTypes)iI);

			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				eBestPlayer = ((PlayerTypes)iI);
			}
		}
	}

	return eBestPlayer;
}


int CvCity::calculateCulturePercent(PlayerTypes eIndex) const
{
	int iTotalCulture;

	iTotalCulture = countTotalCultureTimes100();

	if (iTotalCulture > 0)
	{
		return ((getCultureTimes100(eIndex) * 100) / iTotalCulture);
	}

	return 0;
}


// Leoreth
int CvCity::calculateOverallCulturePercent(PlayerTypes eIndex) const
{
	int iTotalCulture = 0;

	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		iTotalCulture += getCultureTimes100((PlayerTypes)iI);
	}

	iTotalCulture /= 100;

	if (iTotalCulture > 0)
	{
		return (getCultureTimes100(eIndex) / iTotalCulture);
	}

	if (eIndex == getOwner())
	{
		return 100;
	}

	return 0;
}


int CvCity::calculateTeamCulturePercent(TeamTypes eIndex) const
{
	int iTeamCulturePercent;
	int iI;

	iTeamCulturePercent = 0;

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			if (GET_PLAYER((PlayerTypes)iI).getTeam() == eIndex)
			{
				iTeamCulturePercent += calculateCulturePercent((PlayerTypes)iI);
			}
		}
	}

	return iTeamCulturePercent;
}


void CvCity::setCulture(PlayerTypes eIndex, int iNewValue, bool bPlots, bool bUpdatePlotGroups)
{
	setCultureTimes100(eIndex, 100 * iNewValue, bPlots, bUpdatePlotGroups);
}

void CvCity::setCultureTimes100(PlayerTypes eIndex, int iNewValue, bool bPlots, bool bUpdatePlotGroups)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < MAX_PLAYERS, "eIndex expected to be < MAX_PLAYERS");

	// Leoreth: includes K-Mod fixes / culture spread changes
	//int iOldValue = getCultureTimes100(eIndex);

	if (getCultureTimes100(eIndex) != iNewValue)
	{
		m_aiCulture[eIndex] = iNewValue;
		FAssert(getCultureTimes100(eIndex) >= 0);

		updateCultureLevel(bUpdatePlotGroups);
		updateCoveredPlots(bUpdatePlotGroups); // Leoreth

		if (bPlots)
		{
			doPlotCulture(true, eIndex, 0);
			
			// tried K-Mod code
			//doPlotCulture(true, eIndex, (iNewValue-iOldValue)/100);
			//doPlotCultureTimes100(true, eIndex, (iNewValue-iOldValue), false);
			// note: this function no longer applies free city culture.
			// also, note that if a city's culture is decreased to zero, there will probably still be some residual plot culture around the city
			// this is because the culture level on the way up will be higher than it is on the way down.
		}
	}
}


void CvCity::changeCulture(PlayerTypes eIndex, int iChange, bool bPlots, bool bUpdatePlotGroups)
{
	setCultureTimes100(eIndex, (getCultureTimes100(eIndex) + 100  * iChange), bPlots, bUpdatePlotGroups);
}

void CvCity::changeCultureTimes100(PlayerTypes eIndex, int iChange, bool bPlots, bool bUpdatePlotGroups)
{
	setCultureTimes100(eIndex, (getCultureTimes100(eIndex) + iChange), bPlots, bUpdatePlotGroups);
}


int CvCity::getNumRevolts(PlayerTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < MAX_PLAYERS, "eIndex expected to be < MAX_PLAYERS");
	return m_aiNumRevolts[eIndex];
}


void CvCity::changeNumRevolts(PlayerTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < MAX_PLAYERS, "eIndex expected to be < MAX_PLAYERS");
	m_aiNumRevolts[eIndex] = (m_aiNumRevolts[eIndex] + iChange);
	FAssert(getNumRevolts(eIndex) >= 0);
}

int CvCity::getRevoltTestProbability() const
{
	int iBestModifier = 0;

	CLLNode<IDInfo>* pUnitNode = plot()->headUnitNode();
	while (pUnitNode)
	{
		CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = plot()->nextUnitNode(pUnitNode);

		if (pLoopUnit->getRevoltProtection() > iBestModifier)
		{
			iBestModifier = pLoopUnit->getRevoltProtection();
		}
	}
	iBestModifier = range(iBestModifier, 0, 100);

	//Rhye - start switch

	//return ((GC.getDefineINT("REVOLT_TEST_PROB") * (100 - iBestModifier)) / 100);
	int result = (GC.getDefineINT("REVOLT_TEST_PROB") * (100 - iBestModifier)) / 100;
	switch (getOwnerINLINE())
	{
		case MONGOLIA:
			result *= 0;
			break;
		case TURKEY:
			result /= 2;
			break;
		case NATIVE:
			result *= 3;
			result /= 2;
			break;
		case CELTIA:
			result *= 3;
			result /= 2;
			break;
		case INDEPENDENT:
		case INDEPENDENT2:
		case BARBARIAN:
			result *= 3;
			result = std::min(std::max(result, 3), 12);
		default:
			break;
	}

	if (getScenario() >= SCENARIO_600AD) { //late start condition
		if (getX_INLINE() == 59 && getY_INLINE() == 47) //Mediolanum
			result /= 8;
		else if (getX_INLINE() == 60 && getY_INLINE() == 47) //Venice
			result /= 8;
		else if (getX_INLINE() == 60 && getY_INLINE() == 44) //Rome
			result /= 8;
		else if (getOwnerINLINE() == CELTIA) //Byzantium
			result *= 2;
		else if (getX_INLINE() == 68 && getY_INLINE() == 45) //Constantinopolis
			result /= 16;
	}
	if (getX_INLINE() == 63 && getY_INLINE() == 49) //Vienna
			result /= 16;

	if (getX_INLINE() == 59 && getY_INLINE() == 53) //Hamburg
			result /= 8;

	if (isCapital() && getOwnerINLINE() < NUM_MAJOR_PLAYERS)
		result /= 4;

	return (result);

	//Rhye - end
}

bool CvCity::isEverOwned(PlayerTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < MAX_PLAYERS, "eIndex expected to be < MAX_PLAYERS");
	return m_abEverOwned[eIndex];
}


void CvCity::setEverOwned(PlayerTypes eIndex, bool bNewValue)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < MAX_PLAYERS, "eIndex expected to be < MAX_PLAYERS");
	m_abEverOwned[eIndex] = bNewValue;
}


bool CvCity::isTradeRoute(PlayerTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < MAX_PLAYERS, "eIndex expected to be < MAX_PLAYERS");
	return m_abTradeRoute[eIndex];
}


void CvCity::setTradeRoute(PlayerTypes eIndex, bool bNewValue)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < MAX_PLAYERS, "eIndex expected to be < MAX_PLAYERS");
	if (m_abTradeRoute[eIndex] != bNewValue)
	{
		m_abTradeRoute[eIndex] = bNewValue;
	}
}


bool CvCity::isRevealed(TeamTypes eIndex, bool bDebug) const
{
	if (bDebug && GC.getGameINLINE().isDebugMode())
	{
		return true;
	}
	else
	{
		FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
		FAssertMsg(eIndex < MAX_TEAMS, "eIndex expected to be < MAX_TEAMS");

		return m_abRevealed[eIndex];
	}
}


void CvCity::setRevealed(TeamTypes eIndex, bool bNewValue)
{
	CvPlot* pLoopPlot;
	int iI;

	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < MAX_TEAMS, "eIndex expected to be < MAX_TEAMS");

	if (isRevealed(eIndex, false) != bNewValue)
	{
		m_abRevealed[eIndex] = bNewValue;

		updateVisibility();

		if (eIndex == GC.getGameINLINE().getActiveTeam())
		{
			for (iI = 0; iI < NUM_CITY_PLOTS; iI++)
			{
				pLoopPlot = getCityIndexPlot(iI);

				if (pLoopPlot != NULL)
				{
					pLoopPlot->updateSymbols();
				}
			}
		}
	}
}


bool CvCity::getEspionageVisibility(TeamTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < MAX_TEAMS, "eIndex expected to be < MAX_TEAMS");

	return m_abEspionageVisibility[eIndex];
}


void CvCity::setEspionageVisibility(TeamTypes eIndex, bool bNewValue, bool bUpdatePlotGroups)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < MAX_TEAMS, "eIndex expected to be < MAX_TEAMS");

	if (getEspionageVisibility(eIndex) != bNewValue)
	{
		plot()->updateSight(false, bUpdatePlotGroups);

		m_abEspionageVisibility[eIndex] = bNewValue;

		plot()->updateSight(true, bUpdatePlotGroups);
	}
}

void CvCity::updateEspionageVisibility(bool bUpdatePlotGroups)
{
	std::vector<EspionageMissionTypes> aMission;
	for (int iMission = 0; iMission < GC.getNumEspionageMissionInfos(); ++iMission)
	{
		if (GC.getEspionageMissionInfo((EspionageMissionTypes)iMission).isPassive() && GC.getEspionageMissionInfo((EspionageMissionTypes)iMission).getVisibilityLevel() > 0)
		{
			aMission.push_back((EspionageMissionTypes)iMission);
		}
	}

	for (int iTeam = 0; iTeam < MAX_CIV_TEAMS; ++iTeam)
	{
		bool bVisibility = false;

		if (iTeam != getTeam())
		{
			if (isRevealed((TeamTypes)iTeam, false))
			{
				for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; ++iPlayer)
				{
					CvPlayer& kPlayer = GET_PLAYER((PlayerTypes)iPlayer);
					if (kPlayer.isAlive() && kPlayer.getTeam() == iTeam)
					{
						for (std::vector<EspionageMissionTypes>::iterator it = aMission.begin(); it != aMission.end(); ++it)
						{
							if (kPlayer.canDoEspionageMission(*it, getOwnerINLINE(), plot(), -1, NULL))
							{
								bVisibility = true;
								break;
							}
						}

						if (bVisibility)
						{
							break;
						}
					}
				}
			}
		}

		setEspionageVisibility((TeamTypes)iTeam, bVisibility, bUpdatePlotGroups);
	}
}

const wchar* CvCity::getNameKey() const
{
	return m_szName;
}


const CvWString CvCity::getName(uint uiForm) const
{
	return gDLL->getObjectText(m_szName, uiForm, true);
}


void CvCity::setName(const wchar* szNewValue, bool bFound)
{
	CvWString szName(szNewValue);
	//gDLL->stripSpecialCharacters(szName); //Rhye - enable &#xxx;

	if (!szName.empty())
	{
		if (GET_PLAYER(getOwnerINLINE()).isCityNameValid(szName, false))
		{
			m_szName = szName;

			setInfoDirty(true);

			if (isCitySelected())
			{
				gDLL->getInterfaceIFace()->setDirty(CityScreen_DIRTY_BIT, true);
			}
		}
		if (bFound)
		{
			doFoundMessage();
		}
	}
}


void CvCity::doFoundMessage()
{
	CvWString szBuffer;

	szBuffer = gDLL->getText("TXT_KEY_MISC_CITY_HAS_BEEN_FOUNDED", getNameKey());
	gDLL->getInterfaceIFace()->addMessage(getOwnerINLINE(), false, -1, szBuffer, ARTFILEMGR.getInterfaceArtInfo("WORLDBUILDER_CITY_EDIT")->getPath(), MESSAGE_TYPE_MAJOR_EVENT, NULL, NO_COLOR, getX_INLINE(), getY_INLINE());

	//Rhye - start
	//szBuffer = gDLL->getText("TXT_KEY_MISC_CITY_IS_FOUNDED", getNameKey());
	//GC.getGameINLINE().addReplayMessage(REPLAY_MESSAGE_CITY_FOUNDED, getOwnerINLINE(), szBuffer, getX_INLINE(), getY_INLINE(), (ColorTypes)GC.getInfoTypeForString("COLOR_ALT_HIGHLIGHT_TEXT"));
	if (isCapital() && !GET_PLAYER(getOwner()).isBarbarian() && !GET_PLAYER(getOwner()).isMinorCiv()) {
		szBuffer = gDLL->getText("TXT_KEY_MISC_CIV_IS_BORN", GET_PLAYER(getOwnerINLINE()).getCivilizationShortDescription());
	GC.getGameINLINE().addReplayMessage(REPLAY_MESSAGE_CITY_FOUNDED, getOwnerINLINE(), szBuffer, getX_INLINE(), getY_INLINE(), (ColorTypes)GC.getInfoTypeForString("COLOR_ALT_HIGHLIGHT_TEXT"));
}
	//Rhye - end
}

void CvCity::doFoundReplayMessage()
{
	CvWString szBuffer;

	if (isCapital() && !GET_PLAYER(getOwner()).isBarbarian() && !GET_PLAYER(getOwner()).isMinorCiv()) {
		szBuffer = gDLL->getText("TXT_KEY_MISC_CIV_IS_BORN", GET_PLAYER(getOwnerINLINE()).getCivilizationShortDescription());
		GC.getGameINLINE().addReplayMessage(REPLAY_MESSAGE_CITY_FOUNDED, getOwnerINLINE(), szBuffer, getX_INLINE(), getY_INLINE(), (ColorTypes)GC.getInfoTypeForString("COLOR_ALT_HIGHLIGHT_TEXT"));
	}
}


std::string CvCity::getScriptData() const
{
	return m_szScriptData;
}


void CvCity::setScriptData(std::string szNewValue)
{
	m_szScriptData = szNewValue;
}


int CvCity::getNoBonusCount(BonusTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBonusInfos(), "eIndex expected to be < GC.getNumBonusInfos()");
	return m_paiNoBonus[eIndex];
}

bool CvCity::isNoBonus(BonusTypes eIndex) const
{
	return (getNoBonusCount(eIndex) > 0);
}

void CvCity::changeNoBonusCount(BonusTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBonusInfos(), "eIndex expected to be < GC.getNumBonusInfos()");

	if (iChange != 0)
	{
		if (getNumBonuses(eIndex) > 0)
		{
			processBonus(eIndex, -1);
		}

		m_paiNoBonus[eIndex] += iChange;
		FAssert(getNoBonusCount(eIndex) >= 0);

		if (getNumBonuses(eIndex) > 0)
		{
			processBonus(eIndex, 1);
		}

		updateCorporation();

		AI_setAssignWorkDirty(true);

		setInfoDirty(true);
	}
}


int CvCity::getFreeBonus(BonusTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBonusInfos(), "eIndex expected to be < GC.getNumBonusInfos()");
	return m_paiFreeBonus[eIndex];
}


void CvCity::changeFreeBonus(BonusTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBonusInfos(), "eIndex expected to be < GC.getNumBonusInfos()");

	if (iChange != 0)
	{
		plot()->updatePlotGroupBonus(false);
		m_paiFreeBonus[eIndex] += iChange;
		FAssert(getFreeBonus(eIndex) >= 0);
		plot()->updatePlotGroupBonus(true);
	}
}

int CvCity::getNumBonuses(BonusTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBonusInfos(), "eIndex expected to be < GC.getNumBonusInfos()");

	if (isNoBonus(eIndex))
	{
		return 0;
	}

	return m_paiNumBonuses[eIndex] + m_paiNumCorpProducedBonuses[eIndex];
}


bool CvCity::hasBonus(BonusTypes eIndex) const
{
	return (getNumBonuses(eIndex) > 0);
}


void CvCity::changeNumBonuses(BonusTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBonusInfos(), "eIndex expected to be < GC.getNumBonusInfos()");

	if (iChange != 0)
	{
		bool bOldHasBonus = hasBonus(eIndex);

		m_paiNumBonuses[eIndex] += iChange;

		if (bOldHasBonus != hasBonus(eIndex))
		{
			if (hasBonus(eIndex))
			{
				processBonus(eIndex, 1);
			}
			else
			{
				processBonus(eIndex, -1);
			}
		}

		if (isCorporationBonus(eIndex))
		{
			updateCorporation();
		}
	}
}

int CvCity::getNumCorpProducedBonuses(BonusTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBonusInfos(), "eIndex expected to be < GC.getNumBonusInfos()");
	return m_paiNumCorpProducedBonuses[eIndex];
}


bool CvCity::isCorporationBonus(BonusTypes eBonus) const
{
	FAssert(eBonus >= 0);
	FAssert(eBonus < GC.getNumBonusInfos());

	for (int iCorp = 0; iCorp < GC.getNumCorporationInfos(); ++iCorp)
	{
		if (GET_PLAYER(getOwnerINLINE()).isActiveCorporation((CorporationTypes)iCorp))
		{
			for (int i = 0; i < GC.getNUM_CORPORATION_PREREQ_BONUSES(); ++i)
			{
				if (NO_BONUS != GC.getCorporationInfo((CorporationTypes)iCorp).getPrereqBonus(i))
				{
					if (GC.getCorporationInfo((CorporationTypes)iCorp).getPrereqBonus(i) == eBonus && isHasCorporation((CorporationTypes)iCorp))
					{
						return true;
					}
				}
			}
		}
	}

	return false;
}

bool CvCity::isActiveCorporation(CorporationTypes eCorporation) const
{
	FAssert(eCorporation >= 0 && eCorporation < GC.getNumCorporationInfos());

	if (!isHasCorporation(eCorporation))
	{
		return false;
	}

	if (!GET_PLAYER(getOwnerINLINE()).isActiveCorporation(eCorporation))
	{
		return false;
	}

	// edead: start
	return true;

	// for (int i = 0; i < GC.getNUM_CORPORATION_PREREQ_BONUSES(); ++i)
	// {
		// BonusTypes eBonus = (BonusTypes)GC.getCorporationInfo(eCorporation).getPrereqBonus(i);

		// if (NO_BONUS != eBonus)
		// {
			// if (getNumBonuses(eBonus) > 0)
			// {
				// return true;
			// }
		// }
	// }

	// return false;
	// edead: end
}

int CvCity::getBuildingProduction(BuildingTypes eIndex)	const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBuildingInfos(), "eIndex expected to be < GC.getNumBuildingInfos()");
	return m_paiBuildingProduction[eIndex];
}


void CvCity::setBuildingProduction(BuildingTypes eIndex, int iNewValue)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBuildingInfos(), "eIndex expected to be < GC.getNumBuildingInfos()");

	if (getBuildingProduction(eIndex) != iNewValue)
	{
		m_paiBuildingProduction[eIndex] = iNewValue;
		FAssert(getBuildingProduction(eIndex) >= 0);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);
		}

		if ((getOwnerINLINE() == GC.getGameINLINE().getActivePlayer()) && isCitySelected())
		{
			gDLL->getInterfaceIFace()->setDirty(CityScreen_DIRTY_BIT, true);
		}
	}
}


void CvCity::changeBuildingProduction(BuildingTypes eIndex, int iChange)
{
	setBuildingProduction(eIndex, (getBuildingProduction(eIndex) + iChange));
}


int CvCity::getBuildingProductionTime(BuildingTypes eIndex)	const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBuildingInfos(), "eIndex expected to be < GC.getNumBuildingInfos()");
	return m_paiBuildingProductionTime[eIndex];
}


void CvCity::setBuildingProductionTime(BuildingTypes eIndex, int iNewValue)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBuildingInfos(), "eIndex expected to be < GC.getNumBuildingInfos()");
	m_paiBuildingProductionTime[eIndex] = iNewValue;
	FAssert(getBuildingProductionTime(eIndex) >= 0);
}


void CvCity::changeBuildingProductionTime(BuildingTypes eIndex, int iChange)
{
	setBuildingProductionTime(eIndex, (getBuildingProductionTime(eIndex) + iChange));
}


// BUG - Production Decay - start
/*
 * Returns true if the given building will decay this turn.
 */
bool CvCity::isBuildingProductionDecay(BuildingTypes eIndex) const																			 
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBuildingInfos(), "eIndex expected to be < GC.getNumBuildingInfos()");
	return isHuman() && getProductionBuilding() != eIndex && getBuildingProduction(eIndex) > 0 
			&& 100 * getBuildingProductionTime(eIndex) >= GC.getDefineINT("BUILDING_PRODUCTION_DECAY_TIME") * GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getConstructPercent();
}

/*
 * Returns the amount by which the given building will decay once it reaches the limit.
 * Ignores whether or not the building will actually decay this turn.
 */
int CvCity::getBuildingProductionDecay(BuildingTypes eIndex) const																			 
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBuildingInfos(), "eIndex expected to be < GC.getNumBuildingInfos()");
	int iProduction = getBuildingProduction(eIndex);
	return iProduction - ((iProduction * GC.getDefineINT("BUILDING_PRODUCTION_DECAY_PERCENT")) / 100);
}

/*
 * Returns the number of turns left before the given building will decay.
 */
int CvCity::getBuildingProductionDecayTurns(BuildingTypes eIndex) const																			 
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBuildingInfos(), "eIndex expected to be < GC.getNumBuildingInfos()");
	return std::max(0, (GC.getDefineINT("BUILDING_PRODUCTION_DECAY_TIME") * GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getConstructPercent() + 99) / 100 - getBuildingProductionTime(eIndex)) + 1;
}
// BUG - Production Decay - end


int CvCity::getProjectProduction(ProjectTypes eIndex) const																 
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumProjectInfos(), "eIndex expected to be < GC.getNumProjectInfos()");
	return m_paiProjectProduction[eIndex];
}


void CvCity::setProjectProduction(ProjectTypes eIndex, int iNewValue)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumProjectInfos(), "eIndex expected to be < GC.getNumProjectInfos()");

	if (getProjectProduction(eIndex) != iNewValue)
	{
		m_paiProjectProduction[eIndex] = iNewValue;
		FAssert(getProjectProduction(eIndex) >= 0);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);
		}

		if ((getOwnerINLINE() == GC.getGameINLINE().getActivePlayer()) && isCitySelected())
		{
			gDLL->getInterfaceIFace()->setDirty(CityScreen_DIRTY_BIT, true);
		}
	}
}


void CvCity::changeProjectProduction(ProjectTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumProjectInfos(), "eIndex expected to be < GC.getNumProjectInfos()");
	setProjectProduction(eIndex, (getProjectProduction(eIndex) + iChange));
}


int CvCity::getBuildingOriginalOwner(BuildingTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBuildingInfos(), "eIndex expected to be < GC.getNumBuildingInfos()");
	return m_paiBuildingOriginalOwner[eIndex];
}


int CvCity::getBuildingOriginalTime(BuildingTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBuildingInfos(), "eIndex expected to be < GC.getNumBuildingInfos()");
	return m_paiBuildingOriginalTime[eIndex];
}


int CvCity::getUnitProduction(UnitTypes eIndex)	const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumUnitInfos(), "eIndex expected to be < GC.getNumUnitInfos()");
	return m_paiUnitProduction[eIndex];
}


void CvCity::setUnitProduction(UnitTypes eIndex, int iNewValue)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumUnitInfos(), "eIndex expected to be < GC.getNumUnitInfos()");

	if (getUnitProduction(eIndex) != iNewValue)
	{
		m_paiUnitProduction[eIndex] = iNewValue;
		FAssert(getUnitProduction(eIndex) >= 0);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);
		}

		if ((getOwnerINLINE() == GC.getGameINLINE().getActivePlayer()) && isCitySelected())
		{
			gDLL->getInterfaceIFace()->setDirty(CityScreen_DIRTY_BIT, true);
		}
	}
}


void CvCity::changeUnitProduction(UnitTypes eIndex, int iChange)
{
	setUnitProduction(eIndex, (getUnitProduction(eIndex) + iChange));
}


// Leoreth
bool CvCity::isUnitHurried(UnitTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumUnitInfos(), "eIndex expected to be < GC.getNumUnitInfos()");
	return m_pabIsUnitHurried[eIndex];
}


void CvCity::setUnitHurried(UnitTypes eIndex, bool bNewValue)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumUnitInfos(), "eIndex expected to be < GC.getNumUnitInfos()");
	m_pabIsUnitHurried[eIndex] = bNewValue;
}


int CvCity::getUnitProductionTime(UnitTypes eIndex)	const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumUnitInfos(), "eIndex expected to be < GC.getNumUnitInfos()");
	return m_paiUnitProductionTime[eIndex];
}


void CvCity::setUnitProductionTime(UnitTypes eIndex, int iNewValue)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumUnitInfos(), "eIndex expected to be < GC.getNumUnitInfos()");
	m_paiUnitProductionTime[eIndex] = iNewValue;
	FAssert(getUnitProductionTime(eIndex) >= 0);
}


void CvCity::changeUnitProductionTime(UnitTypes eIndex, int iChange)
{
	setUnitProductionTime(eIndex, (getUnitProductionTime(eIndex) + iChange));
}


// BUG - Production Decay - start
/*
 * Returns true if the given unit will decay this turn.
 */
bool CvCity::isUnitProductionDecay(UnitTypes eIndex) const																			 
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumUnitInfos(), "eIndex expected to be < GC.getNumUnitInfos()");
	return isHuman() && getProductionUnit() != eIndex && getUnitProduction(eIndex) > 0 
			&& 100 * getUnitProductionTime(eIndex) >= GC.getDefineINT("UNIT_PRODUCTION_DECAY_TIME") * GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getTrainPercent();
}

/*
 * Returns the amount by which the given unit will decay once it reaches the limit.
 * Ignores whether or not the unit will actually decay this turn.
 */
int CvCity::getUnitProductionDecay(UnitTypes eIndex) const																			 
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumUnitInfos(), "eIndex expected to be < GC.getNumUnitInfos()");
	int iProduction = getUnitProduction(eIndex);
	return iProduction - ((iProduction * GC.getDefineINT("UNIT_PRODUCTION_DECAY_PERCENT")) / 100);
}

/*
 * Returns the number of turns left before the given unit will decay.
 */
int CvCity::getUnitProductionDecayTurns(UnitTypes eIndex) const																			 
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumUnitInfos(), "eIndex expected to be < GC.getNumUnitInfos()");
	return std::max(0, (GC.getDefineINT("UNIT_PRODUCTION_DECAY_TIME") * GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getTrainPercent() + 99) / 100 - getUnitProductionTime(eIndex)) + 1;
}
// BUG - Production Decay - end


int CvCity::getGreatPeopleUnitRate(UnitTypes eIndex) const																 
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumUnitInfos(), "eIndex expected to be < GC.getNumUnitInfos()");
	return m_paiGreatPeopleUnitRate[eIndex];
}


void CvCity::setGreatPeopleUnitRate(UnitTypes eIndex, int iNewValue)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumUnitInfos(), "eIndex expected to be < GC.getNumUnitInfos()");
	if (GC.getGameINLINE().isOption(GAMEOPTION_NO_ESPIONAGE) && GC.getUnitInfo(eIndex).getEspionagePoints() > 0)
	{
		return;
	}

	m_paiGreatPeopleUnitRate[eIndex] = iNewValue;
	FAssert(getGreatPeopleUnitRate(eIndex) >= 0);
}


void CvCity::changeGreatPeopleUnitRate(UnitTypes eIndex, int iChange)
{
	setGreatPeopleUnitRate(eIndex, (getGreatPeopleUnitRate(eIndex) + iChange));
}


int CvCity::getGreatPeopleUnitProgress(UnitTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumUnitInfos(), "eIndex expected to be < GC.getNumUnitInfos()");
	return m_paiGreatPeopleUnitProgress[eIndex];
}


void CvCity::setGreatPeopleUnitProgress(UnitTypes eIndex, int iNewValue)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumUnitInfos(), "eIndex expected to be < GC.getNumUnitInfos()");
	m_paiGreatPeopleUnitProgress[eIndex] = iNewValue;
	FAssert(getGreatPeopleUnitProgress(eIndex) >= 0);
}


void CvCity::changeGreatPeopleUnitProgress(UnitTypes eIndex, int iChange)
{
	setGreatPeopleUnitProgress(eIndex, (getGreatPeopleUnitProgress(eIndex) + iChange));
}


int CvCity::getSpecialistCount(SpecialistTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumSpecialistInfos(), "eIndex expected to be < GC.getNumSpecialistInfos()");
	return m_paiSpecialistCount[eIndex];
}


void CvCity::setSpecialistCount(SpecialistTypes eIndex, int iNewValue)
{
	int iOldValue;

	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumSpecialistInfos(), "eIndex expected to be < GC.getNumSpecialistInfos()");

	iOldValue = getSpecialistCount(eIndex);

	if (iOldValue != iNewValue)
	{
		m_paiSpecialistCount[eIndex] = iNewValue;
		FAssert(getSpecialistCount(eIndex) >= 0);

		changeSpecialistPopulation(iNewValue - iOldValue);
		processSpecialist(eIndex, (iNewValue - iOldValue));

		if (isCitySelected())
		{
			gDLL->getInterfaceIFace()->setDirty(CitizenButtons_DIRTY_BIT, true);
		}
	}
}


void CvCity::changeSpecialistCount(SpecialistTypes eIndex, int iChange)
{
	setSpecialistCount(eIndex, (getSpecialistCount(eIndex) + iChange));
}


void CvCity::alterSpecialistCount(SpecialistTypes eIndex, int iChange)
{
	int iI;

	if (iChange != 0)
	{
		if (isCitizensAutomated())
		{
			if ((getForceSpecialistCount(eIndex) + iChange) < 0)
			{
				setCitizensAutomated(false);
			}
		}

		if (isCitizensAutomated())
		{
			changeForceSpecialistCount(eIndex, iChange);
		}
		else
		{
			if (iChange > 0)
			{
				for (iI = 0; iI < iChange; iI++)
				{
					if ((extraPopulation() > 0) || AI_removeWorstCitizen(eIndex))
					{
						if (isSpecialistValid(eIndex, 1))
						{
							changeSpecialistCount(eIndex, 1);
						}
					}
				}
			}
			else
			{
				for (iI = 0; iI < -(iChange); iI++)
				{
					if (getSpecialistCount(eIndex) > 0)
					{
						changeSpecialistCount(eIndex, -1);

						if ((eIndex != GC.getDefineINT("DEFAULT_SPECIALIST")) && (GC.getDefineINT("DEFAULT_SPECIALIST") != NO_SPECIALIST))
						{
							changeSpecialistCount(((SpecialistTypes)GC.getDefineINT("DEFAULT_SPECIALIST")), 1);
						}
						else if (extraFreeSpecialists() > 0)
						{
							AI_addBestCitizen(false, true);
						}
						else
						{
							int iNumCanWorkPlots = 0;
							for (int iI = 0; iI < NUM_CITY_PLOTS; iI++)
							{
								if (iI != CITY_HOME_PLOT)
								{
									if (!isWorkingPlot(iI))
									{
										CvPlot* pLoopPlot = getCityIndexPlot(iI);

										if (pLoopPlot != NULL)
										{
											if (canWork(pLoopPlot))
											{
												++iNumCanWorkPlots;
											}
										}
									}
								}
							}

							if (iNumCanWorkPlots > 0)
							{
								AI_addBestCitizen(true, false);
							}
							else
							{
								AI_addBestCitizen(false, true);
							}
						}
					}
				}
			}
		}
	}
}


int CvCity::getMaxSpecialistCount(SpecialistTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumSpecialistInfos(), "eIndex expected to be < GC.getNumSpecialistInfos()");

	int iMaxSpecialistCount = m_paiMaxSpecialistCount[eIndex];
	
	// srpt new Canadian UP
	/*if (getOwnerINLINE() == CANADA)
	{
		int iMulticulturalism = 0;
		for (int iI =  0; iI < NUM_RELIGIONS; iI++)
		{
			if ((GET_PLAYER(getOwnerINLINE()).getStateReligion() != ((ReligionTypes)iI)) && (isHasReligion((ReligionTypes)iI)))
			{
				iMulticulturalism += 1;
			}
		}
		if ((eIndex == (SpecialistTypes)2) && (hasBuilding((BuildingTypes)GC.getInfoTypeForString("BUILDING_THEATRE")))) // artist
		{
			iMaxSpecialistCount += iMulticulturalism;
		}
		if ((eIndex == (SpecialistTypes)3) && (hasBuilding((BuildingTypes)GC.getInfoTypeForString("BUILDING_LIBRARY")))) // scientist
		{
			iMaxSpecialistCount += iMulticulturalism;
		}
	}*/
	// srpt end
				

	// Leoreth: Wat Preah Pisnulok effect
	if (GET_PLAYER(getOwner()).isHasBuilding((BuildingTypes)WAT_PREAH_PISNULOK) && !GET_TEAM(GET_PLAYER(getOwner()).getTeam()).isHasTech((TechTypes)SCIENTIFIC_METHOD))
	{
		if (eIndex == (SpecialistTypes)2) // artist
		{
			iMaxSpecialistCount += m_paiMaxSpecialistCount[(SpecialistTypes)1]; // priest
		}

		if (eIndex == (SpecialistTypes)1) // priest
		{
			int iPriestsToArtists = max(0, getSpecialistCount((SpecialistTypes)2) - getFreeSpecialistCount((SpecialistTypes)2) - m_paiMaxSpecialistCount[(SpecialistTypes)2]);
			iMaxSpecialistCount -= iPriestsToArtists;
		}
	}

	// Leoreth: unlimited specialist effects now only double available specialists
	if (GET_PLAYER(getOwnerINLINE()).isSpecialistValid(eIndex))
	{
		iMaxSpecialistCount *= 2;
	}

	return iMaxSpecialistCount;
}


bool CvCity::isSpecialistValid(SpecialistTypes eIndex, int iExtra) const
{
	// Leoreth: Sphinx effect included (disabled)
	return (((getSpecialistCount(eIndex) + iExtra) <= getMaxSpecialistCount(eIndex)) || /*GET_PLAYER(getOwnerINLINE()).isSpecialistValid(eIndex) ||*/ /*(isHasRealBuilding((BuildingTypes)STONEHENGE) && eIndex == (SpecialistTypes)2)  ||*/ (eIndex == GC.getDefineINT("DEFAULT_SPECIALIST")));
}


void CvCity::changeMaxSpecialistCount(SpecialistTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumSpecialistInfos(), "eIndex expected to be < GC.getNumSpecialistInfos()");

	if (iChange != 0)
	{
		m_paiMaxSpecialistCount[eIndex] = std::max(0, (m_paiMaxSpecialistCount[eIndex] + iChange));

		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getForceSpecialistCount(SpecialistTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumSpecialistInfos(), "eIndex expected to be < GC.getNumSpecialistInfos()");
	return m_paiForceSpecialistCount[eIndex];
}


bool CvCity::isSpecialistForced() const
{
	int iI;

	for (iI = 0; iI < GC.getNumSpecialistInfos(); iI++)
	{
		if (getForceSpecialistCount((SpecialistTypes)iI) > 0)
		{
			return true;
		}
	}

	return false;
}


void CvCity::setForceSpecialistCount(SpecialistTypes eIndex, int iNewValue)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumSpecialistInfos(), "eIndex expected to be < GC.getNumSpecialistInfos()");

	if (getForceSpecialistCount(eIndex) != iNewValue)
	{
		m_paiForceSpecialistCount[eIndex] = std::max(0, iNewValue);

		if (isCitySelected())
		{
			gDLL->getInterfaceIFace()->setDirty(Help_DIRTY_BIT, true);
		}

		AI_setAssignWorkDirty(true);
	}
}


void CvCity::changeForceSpecialistCount(SpecialistTypes eIndex, int iChange)
{
	setForceSpecialistCount(eIndex, (getForceSpecialistCount(eIndex) + iChange));
}


int CvCity::getFreeSpecialistCount(SpecialistTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumSpecialistInfos(), "eIndex expected to be < GC.getNumSpecialistInfos()");
	return m_paiFreeSpecialistCount[eIndex];
}

int CvCity::getAddedFreeSpecialistCount(SpecialistTypes eIndex) const
{
	int iNumAddedSpecialists = getFreeSpecialistCount(eIndex);

	for (int iJ = 0; iJ < GC.getNumBuildingInfos(); ++iJ)
	{
		CvBuildingInfo& kBuilding = GC.getBuildingInfo((BuildingTypes)iJ);
		if (kBuilding.getFreeSpecialistCount(eIndex) > 0)
		{
			iNumAddedSpecialists -= getNumActiveBuilding((BuildingTypes)iJ) * kBuilding.getFreeSpecialistCount(eIndex);
		}
	}

	FAssert(iNumAddedSpecialists >= 0);
	return std::max(0, iNumAddedSpecialists);
}

void CvCity::setFreeSpecialistCount(SpecialistTypes eIndex, int iNewValue)
{
	int iOldValue;

	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumSpecialistInfos(), "eIndex expected to be < GC.getNumSpecialistInfos()");

	iOldValue = getFreeSpecialistCount(eIndex);

	if (iOldValue != iNewValue)
	{
		m_paiFreeSpecialistCount[eIndex] = iNewValue;
		FAssert(getFreeSpecialistCount(eIndex) >= 0);

		changeNumGreatPeople(iNewValue - iOldValue);
		processSpecialist(eIndex, (iNewValue - iOldValue));

		if (isCitySelected())
		{
			gDLL->getInterfaceIFace()->setDirty(CitizenButtons_DIRTY_BIT, true);
		}
	}
}

void CvCity::changeFreeSpecialistCount(SpecialistTypes eIndex, int iChange)
{
	setFreeSpecialistCount(eIndex, (getFreeSpecialistCount(eIndex) + iChange));
}

int CvCity::getImprovementFreeSpecialists(ImprovementTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumImprovementInfos(), "eIndex expected to be < GC.getNumImprovementInfos()");
	return m_paiImprovementFreeSpecialists[eIndex];
}

void CvCity::changeImprovementFreeSpecialists(ImprovementTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumImprovementInfos(), "eIndex expected to be < GC.getNumImprovementInfos()");

	if (iChange != 0)
	{
		m_paiImprovementFreeSpecialists[eIndex] = std::max(0, (m_paiImprovementFreeSpecialists[eIndex] + iChange));
	}
}

int CvCity::getReligionInfluence(ReligionTypes eReligion) const
{
	FAssertMsg(eReligion >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eReligion < GC.getNumReligionInfos(), "eIndex expected to be < GC.getNumReligionInfos()");
	return m_paiReligionInfluence[eReligion];
}


void CvCity::changeReligionInfluence(ReligionTypes eReligion, int iChange)
{
	FAssertMsg(eReligion >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eReligion < GC.getNumReligionInfos(), "eIndex expected to be < GC.getNumReligionInfos()");
	setReligionInfluence(eReligion, getReligionInfluence(eReligion) + iChange);
	FAssert(getReligionInfluence(eReligion) >= 0);
}


void CvCity::setReligionInfluence(ReligionTypes eReligion, int iNewValue)
{
	int iOldValue = getReligionInfluence(eReligion);

	if (iOldValue != iNewValue)
	{
		m_paiReligionInfluence[eReligion] = iNewValue;

		log(CvWString::format(L"Change religion influence in %s from %d to %d", getName().GetCString(), iOldValue, iNewValue));

		int iFactor = GC.getReligionInfo(eReligion).isProselytizing() ? 2 : 1;

		spreadReligionInfluence(eReligion, iFactor * iOldValue, -1);
		spreadReligionInfluence(eReligion, iFactor * iNewValue, 1);
	}
}


void CvCity::spreadReligionInfluence(ReligionTypes eReligion, int iRange, int iChange)
{
	int iSpreadRange = 2 * iRange;

	for (int iDX = -iSpreadRange; iDX <= iSpreadRange; iDX++)
	{
		for (int iDY = -iSpreadRange; iDY <= iSpreadRange; iDY++)
		{
			CvPlot* pLoopPlot = plotXY(getX_INLINE(), getY_INLINE(), iDX, iDY);
			int iDistance = cultureDistance(iDX, iDY);

			if (pLoopPlot != NULL)
			{
				if (iDistance <= iRange || (plot()->getSpreadFactor(eReligion) >= REGION_SPREAD_HISTORICAL && iDistance <= iSpreadRange))
				{
					pLoopPlot->changeReligionInfluence(eReligion, iChange);
				}
			}
		}
	}
}


int CvCity::getCurrentStateReligionHappiness() const
{
	if (GET_PLAYER(getOwnerINLINE()).getStateReligion() != NO_RELIGION)
	{
		return getStateReligionHappiness(GET_PLAYER(getOwnerINLINE()).getStateReligion());
	}

	return 0;
}


int CvCity::getStateReligionHappiness(ReligionTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumReligionInfos(), "eIndex expected to be < GC.getNumReligionInfos()");
	return m_paiStateReligionHappiness[eIndex];
}


void CvCity::changeStateReligionHappiness(ReligionTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumReligionInfos(), "eIndex expected to be < GC.getNumReligionInfos()");

	if (iChange != 0)
	{
		m_paiStateReligionHappiness[eIndex] = (m_paiStateReligionHappiness[eIndex] + iChange);

		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getUnitCombatFreeExperience(UnitCombatTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumUnitCombatInfos(), "eIndex expected to be < GC.getNumUnitCombatInfos()");
	return m_paiUnitCombatFreeExperience[eIndex];
}


void CvCity::changeUnitCombatFreeExperience(UnitCombatTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumUnitCombatInfos(), "eIndex expected to be < GC.getNumUnitCombatInfos()");
	m_paiUnitCombatFreeExperience[eIndex] = (m_paiUnitCombatFreeExperience[eIndex] + iChange);
	FAssert(getUnitCombatFreeExperience(eIndex) >= 0);
}


int CvCity::getFreePromotionCount(PromotionTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumPromotionInfos(), "eIndex expected to be < GC.getNumPromotionInfos()");
	return m_paiFreePromotionCount[eIndex];
}


bool CvCity::isFreePromotion(PromotionTypes eIndex) const
{
	return (getFreePromotionCount(eIndex) > 0);
}


void CvCity::changeFreePromotionCount(PromotionTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumPromotionInfos(), "eIndex expected to be < GC.getNumPromotionInfos()");
	m_paiFreePromotionCount[eIndex] = (m_paiFreePromotionCount[eIndex] + iChange);
	FAssert(getFreePromotionCount(eIndex) >= 0);
}


int CvCity::getSpecialistFreeExperience() const
{
	return m_iSpecialistFreeExperience;
}


void CvCity::changeSpecialistFreeExperience(int iChange)
{
	m_iSpecialistFreeExperience += iChange;
	FAssert(m_iSpecialistFreeExperience >= 0);
}


int CvCity::getEspionageDefenseModifier() const
{
	return m_iEspionageDefenseModifier;
}


void CvCity::changeEspionageDefenseModifier(int iChange)
{
	if (0 != iChange)
	{
		m_iEspionageDefenseModifier += iChange;
	}
}

bool CvCity::isWorkingPlot(int iIndex) const
{
	FAssertMsg(iIndex >= 0, "iIndex expected to be >= 0");
	FAssertMsg(iIndex < NUM_CITY_PLOTS, "iIndex expected to be < NUM_CITY_PLOTS");

	return m_pabWorkingPlot[iIndex];
}


bool CvCity::isWorkingPlot(const CvPlot* pPlot) const
{
	int iIndex;

	iIndex = getCityPlotIndex(pPlot);

	if (iIndex != -1)
	{
		return isWorkingPlot(iIndex);
	}

	return false;
}


void CvCity::setWorkingPlot(int iIndex, bool bNewValue)
{
	CvPlot* pPlot;
	int iI;

	FAssertMsg(iIndex >= 0, "iIndex expected to be >= 0");
	FAssertMsg(iIndex < NUM_CITY_PLOTS, "iIndex expected to be < NUM_CITY_PLOTS");

	if (isWorkingPlot(iIndex) != bNewValue)
	{
		m_pabWorkingPlot[iIndex] = bNewValue;

		pPlot = getCityIndexPlot(iIndex);

		if (pPlot != NULL)
		{
			FAssertMsg(pPlot->getWorkingCity() == this, "WorkingCity is expected to be this");

			if (isWorkingPlot(iIndex))
			{
				if (iIndex != CITY_HOME_PLOT)
				{
					changeWorkingPopulation(1);
					updateExtraSpecialistYield(); //Leoreth: city states
				}

				for (iI = 0; iI < NUM_YIELD_TYPES; iI++)
				{
					changeBaseYieldRate(((YieldTypes)iI), pPlot->getYield((YieldTypes)iI));
					// Leoreth: catch the overflow bug
					if (getBaseYieldRate((YieldTypes)iI) < 0 || getBaseYieldRate((YieldTypes)iI) > 1000) {
						GC.getGame().logMsg("Overflow in (%d, %d) for setWorkingPlot", getX(), getY());
						gDLL->getInterfaceIFace()->addMessage(GC.getGame().getActivePlayer(), true, GC.getEVENT_MESSAGE_TIME(), gDLL->getText("TXT_KEY_OVERFLOW", getX(), getY(), "setWorkingPlot()"), "", MESSAGE_TYPE_MAJOR_EVENT, ARTFILEMGR.getInterfaceArtInfo("WORLDBUILDER_CITY_EDIT")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_RED"), getX_INLINE(), getY_INLINE(), true, true);
						GC.getGame().setAIAutoPlay(0);
						GC.getGame().setAIAutoPlayCatapult(0);
						gDLL->getEngineIFace()->AutoSave(true);
					}
				}

				// update plot builder special case where a plot is being worked but is (a) unimproved  or (b) un-bonus'ed
				pPlot->updatePlotBuilder();
			}
			else
			{
				if (iIndex != CITY_HOME_PLOT)
				{
					changeWorkingPopulation(-1);
					updateExtraSpecialistYield(); //Leoreth: city states
				}

				for (iI = 0; iI < NUM_YIELD_TYPES; iI++)
				{
					changeBaseYieldRate(((YieldTypes)iI), -(pPlot->getYield((YieldTypes)iI)));
					// Leoreth: catch the overflow bug
					if (getBaseYieldRate((YieldTypes)iI) < 0 || getBaseYieldRate((YieldTypes)iI) > 1000) {
						GC.getGame().logMsg("Overflow in (%d, %d) for setWorkingPlot2", getX(), getY());
						gDLL->getInterfaceIFace()->addMessage(GC.getGame().getActivePlayer(), true, GC.getEVENT_MESSAGE_TIME(), gDLL->getText("TXT_KEY_OVERFLOW", getX(), getY(), "setWorkingPlot2()"), "", MESSAGE_TYPE_MAJOR_EVENT, ARTFILEMGR.getInterfaceArtInfo("WORLDBUILDER_CITY_EDIT")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_RED"), getX_INLINE(), getY_INLINE(), true, true);
						GC.getGame().setAIAutoPlay(0);
						GC.getGame().setAIAutoPlayCatapult(0);
						gDLL->getEngineIFace()->AutoSave(true);
					}
				}
			}

			if ((getTeam() == GC.getGameINLINE().getActiveTeam()) || GC.getGameINLINE().isDebugMode())
			{
				pPlot->updateSymbolDisplay();
			}
		}

		if (isCitySelected())
		{
			gDLL->getInterfaceIFace()->setDirty(InfoPane_DIRTY_BIT, true );
			gDLL->getInterfaceIFace()->setDirty(CityScreen_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(ColoredPlots_DIRTY_BIT, true);
		}
	}
}


void CvCity::setWorkingPlot(CvPlot* pPlot, bool bNewValue)
{
	setWorkingPlot(getCityPlotIndex(pPlot), bNewValue);
}


void CvCity::alterWorkingPlot(int iIndex)
{
	CvPlot* pPlot;

	FAssertMsg(iIndex >= 0, "iIndex expected to be >= 0");
	FAssertMsg(iIndex < NUM_CITY_PLOTS, "iIndex expected to be < NUM_CITY_PLOTS");

	if (iIndex == CITY_HOME_PLOT)
	{
		setCitizensAutomated(true);
	}
	else
	{
		pPlot = getCityIndexPlot(iIndex);

		if (pPlot != NULL)
		{
			if (canWork(pPlot))
			{
				setCitizensAutomated(false);

				if (isWorkingPlot(iIndex))
				{
					setWorkingPlot(iIndex, false);

					if (GC.getDefineINT("DEFAULT_SPECIALIST") != NO_SPECIALIST)
					{
						changeSpecialistCount(((SpecialistTypes)GC.getDefineINT("DEFAULT_SPECIALIST")), 1);
					}
					else
					{
						AI_addBestCitizen(false, true);
					}
				}
				else
				{
					if ((extraPopulation() > 0) || AI_removeWorstCitizen())
					{
						setWorkingPlot(iIndex, true);
					}
				}
			}
			else if (pPlot->getOwnerINLINE() == getOwnerINLINE())
			{
				pPlot->setWorkingCityOverride(this);
			}
		}
	}
}

//Rhye - start
bool CvCity::isHasRealBuilding(BuildingTypes eIndex) const
{
	return getNumRealBuilding(eIndex);
}


void CvCity::setHasRealBuilding(BuildingTypes eIndex, bool bNewValue)
{
    if (bNewValue == true)
        setNumRealBuilding(eIndex, 1);
    else
        setNumRealBuilding(eIndex, 0);
}
//Rhye - end

int CvCity::getNumRealBuilding(BuildingTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBuildingInfos(), "eIndex expected to be < GC.getNumBuildingInfos()");
	return m_paiNumRealBuilding[eIndex];
}


void CvCity::setNumRealBuilding(BuildingTypes eIndex, int iNewValue)
{
	setNumRealBuildingTimed(eIndex, iNewValue, true, getOwnerINLINE(), GC.getGameINLINE().getGameTurnYear());
}


void CvCity::setNumRealBuildingTimed(BuildingTypes eIndex, int iNewValue, bool bFirst, PlayerTypes eOriginalOwner, int iOriginalTime)
{
	CvCity* pLoopCity;
	CvWString szBuffer;
	int iOldNumBuilding;
	int iChangeNumRealBuilding;
	int iLoop;
	int iI;

	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBuildingInfos(), "eIndex expected to be < GC.getNumBuildingInfos()");

	iChangeNumRealBuilding = iNewValue - getNumRealBuilding(eIndex);

	if (iChangeNumRealBuilding != 0)
	{
		iOldNumBuilding = getNumBuilding(eIndex);

		m_paiNumRealBuilding[eIndex] = iNewValue;

		if (getNumRealBuilding(eIndex) > 0)
		{
			m_paiBuildingOriginalOwner[eIndex] = eOriginalOwner;
			m_paiBuildingOriginalTime[eIndex] = iOriginalTime;
		}
		else
		{
			m_paiBuildingOriginalOwner[eIndex] = NO_PLAYER;
			m_paiBuildingOriginalTime[eIndex] = MIN_INT;
		}

		if (iOldNumBuilding != getNumBuilding(eIndex))
		{
			if (getNumRealBuilding(eIndex) > 0)
			{
				if (GC.getBuildingInfo(eIndex).isStateReligion())
				{
					for (iI = 0; iI < GC.getNumVoteSourceInfos(); ++iI)
					{
						if (GC.getBuildingInfo(eIndex).getVoteSourceType() == (VoteSourceTypes)iI)
						{
							if (GC.getGameINLINE().getVoteSourceReligion((VoteSourceTypes)iI) == NO_RELIGION)
							{
								FAssert(GET_PLAYER(getOwnerINLINE()).getStateReligion() != NO_RELIGION);
								GC.getGameINLINE().setVoteSourceReligion((VoteSourceTypes)iI, (ReligionTypes)GC.getBuildingInfo(eIndex).getReligionType(), true);
							}
						}
					}
				}
			}

			processBuilding(eIndex, getNumBuilding(eIndex) - iOldNumBuilding);
		}

		if (!(GC.getBuildingClassInfo((BuildingClassTypes)(GC.getBuildingInfo(eIndex).getBuildingClassType())).isNoLimit()))
		{
			if (isWorldWonderClass((BuildingClassTypes)(GC.getBuildingInfo(eIndex).getBuildingClassType())))
			{
				changeNumWorldWonders(iChangeNumRealBuilding);
			}
			else if (isTeamWonderClass((BuildingClassTypes)(GC.getBuildingInfo(eIndex).getBuildingClassType())))
			{
				changeNumTeamWonders(iChangeNumRealBuilding);
			}
			else if (isNationalWonderClass((BuildingClassTypes)(GC.getBuildingInfo(eIndex).getBuildingClassType())))
			{
				changeNumNationalWonders(iChangeNumRealBuilding);
			}
			else
			{
				changeNumBuildings(iChangeNumRealBuilding);
			}
		}

		if (iChangeNumRealBuilding > 0)
		{
			if (bFirst)
			{
				if (GC.getBuildingInfo(eIndex).isCapital())
				{
					GET_PLAYER(getOwnerINLINE()).setCapitalCity(this);
				}

				if (GC.getGameINLINE().isFinalInitialized() && !(gDLL->GetWorldBuilderMode()))
				{
					if (GC.getBuildingInfo(eIndex).isGoldenAge())
					{
						// Leoreth: adjusting for turn changes not required during anarchy because it doesn't count down
						GET_PLAYER(getOwnerINLINE()).changeGoldenAgeTurns(iChangeNumRealBuilding * (GET_PLAYER(getOwnerINLINE()).getGoldenAgeLength() + (GET_PLAYER(getOwnerINLINE()).isAnarchy() ? 0 : 1)));
					}

					if (GC.getBuildingInfo(eIndex).getGlobalPopulationChange() != 0)
					{
						for (iI = 0; iI < MAX_PLAYERS; iI++)
						{
							if (GET_PLAYER((PlayerTypes)iI).isAlive())
							{
								if (GET_PLAYER((PlayerTypes)iI).getTeam() == getTeam())
								{
									if (GC.getBuildingInfo(eIndex).isTeamShare() || (iI == getOwnerINLINE()))
									{
										for (pLoopCity = GET_PLAYER((PlayerTypes)iI).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER((PlayerTypes)iI).nextCity(&iLoop))
										{
											pLoopCity->setPopulation(std::max(1, (pLoopCity->getPopulation() + iChangeNumRealBuilding * GC.getBuildingInfo(eIndex).getGlobalPopulationChange())));
											pLoopCity->AI_updateAssignWork();  // so subsequent cities don't starve with the extra citizen working nothing
										}
									}
								}
							}
						}
					}

					for (iI = 0; iI < GC.getNumReligionInfos(); iI++)
					{
						if (GC.getBuildingInfo(eIndex).getReligionChange(iI) > 0)
						{
							log(CvWString::format(L"From building: %s in %s", GC.getReligionInfo((ReligionTypes)iI).getText(), getName().GetCString()));
							setHasReligion(((ReligionTypes)iI), true, true, true);
						}
					}

					if (GC.getBuildingInfo(eIndex).getFreeTechs() > 0)
					{
						if (!isHuman())
						{
							for (iI = 0; iI < GC.getBuildingInfo(eIndex).getFreeTechs(); iI++)
							{
								for (int iLoop = 0; iLoop < iChangeNumRealBuilding; iLoop++)
								{
									GET_PLAYER(getOwnerINLINE()).AI_chooseFreeTech();
								}
							}
						}
						else
						{
							szBuffer = gDLL->getText("TXT_KEY_MISC_COMPLETED_WONDER_CHOOSE_TECH", GC.getBuildingInfo(eIndex).getTextKeyWide());
							GET_PLAYER(getOwnerINLINE()).chooseTech(GC.getBuildingInfo(eIndex).getFreeTechs() * iChangeNumRealBuilding, szBuffer.GetCString());
						}
					}

					if (isWorldWonderClass((BuildingClassTypes)(GC.getBuildingInfo(eIndex).getBuildingClassType())))
					{
						//szBuffer = gDLL->getText("TXT_KEY_MISC_COMPLETES_WONDER", GET_PLAYER(getOwnerINLINE()).getNameKey(), GC.getBuildingInfo(eIndex).getTextKeyWide()); //Rhye
						szBuffer = gDLL->getText("TXT_KEY_MISC_COMPLETES_WONDER", GET_PLAYER(getOwnerINLINE()).getCivilizationShortDescription(), GC.getBuildingInfo(eIndex).getTextKeyWide()); //Rhye
						GC.getGameINLINE().addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, getOwnerINLINE(), szBuffer, getX_INLINE(), getY_INLINE(), (ColorTypes)GC.getInfoTypeForString("COLOR_BUILDING_TEXT"));

						for (iI = 0; iI < MAX_PLAYERS; iI++)
						{
							if (GET_PLAYER((PlayerTypes)iI).isAlive())
							{
								if (isRevealed(GET_PLAYER((PlayerTypes)iI).getTeam(), false))
								{
									//szBuffer = gDLL->getText("TXT_KEY_MISC_WONDER_COMPLETED", GET_PLAYER(getOwnerINLINE()).getNameKey(), GC.getBuildingInfo(eIndex).getTextKeyWide()); //Rhye
									szBuffer = gDLL->getText("TXT_KEY_MISC_WONDER_COMPLETED", GET_PLAYER(getOwnerINLINE()).getCivilizationShortDescription(), GC.getBuildingInfo(eIndex).getTextKeyWide()); //Rhye
									gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_WONDER_BUILDING_BUILD", MESSAGE_TYPE_MAJOR_EVENT, GC.getBuildingInfo(eIndex).getArtInfo()->getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_BUILDING_TEXT"), getX_INLINE(), getY_INLINE(), true, true);
								}
								else
								{
									szBuffer = gDLL->getText("TXT_KEY_MISC_WONDER_COMPLETED_UNKNOWN", GC.getBuildingInfo(eIndex).getTextKeyWide());
									gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_WONDER_BUILDING_BUILD", MESSAGE_TYPE_MAJOR_EVENT, GC.getBuildingInfo(eIndex).getArtInfo()->getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_BUILDING_TEXT"));
								}
							}
						}
					}
				}

				if (GC.getBuildingInfo(eIndex).isAllowsNukes())
				{
					GC.getGameINLINE().makeNukesValid(true);
				}

				GC.getGameINLINE().incrementBuildingClassCreatedCount((BuildingClassTypes)(GC.getBuildingInfo(eIndex).getBuildingClassType()));
			}
		}

		//great wall
		if (bFirst)
		{
			if (GC.getBuildingInfo(eIndex).isAreaBorderObstacle())
			{
				int iCountExisting = 0;
				for (iI = 0; iI < GC.getNumBuildingInfos(); iI++)
				{
					if (eIndex != iI && GC.getBuildingInfo((BuildingTypes)iI).isAreaBorderObstacle())
					{
						iCountExisting += getNumRealBuilding((BuildingTypes)iI);
					}
				}

				if (iCountExisting == 1 && iNewValue == 0)
				{
					gDLL->getEngineIFace()->RemoveGreatWall(this);
				}
				else if (iCountExisting == 0 && iNewValue > 0)
				{
					gDLL->getEngineIFace()->AddGreatWall(this);
				}
			}
		}
	}
}


int CvCity::getNumFreeBuilding(BuildingTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBuildingInfos(), "eIndex expected to be < GC.getNumBuildingInfos()");
	return m_paiNumFreeBuilding[eIndex];
}


void CvCity::setNumFreeBuilding(BuildingTypes eIndex, int iNewValue)
{
	int iOldNumBuilding;

	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBuildingInfos(), "eIndex expected to be < GC.getNumBuildingInfos()");

	if (getNumFreeBuilding(eIndex) != iNewValue)
	{
		iOldNumBuilding = getNumBuilding(eIndex);

		m_paiNumFreeBuilding[eIndex] = iNewValue;

		if (iOldNumBuilding != getNumBuilding(eIndex))
		{
			processBuilding(eIndex, iNewValue - iOldNumBuilding);
		}
	}
}


bool CvCity::isHasReligion(ReligionTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumReligionInfos(), "eIndex expected to be < GC.getNumReligionInfos()");
	return m_pabHasReligion[eIndex];
}


void CvCity::setHasReligion(ReligionTypes eIndex, bool bNewValue, bool bAnnounce, bool bArrows)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumReligionInfos(), "eIndex expected to be < GC.getNumReligionInfos()");

	if (isHasReligion(eIndex) != bNewValue)
	{
		for (int iVoteSource = 0; iVoteSource < GC.getNumVoteSourceInfos(); ++iVoteSource)
		{
			processVoteSourceBonus((VoteSourceTypes)iVoteSource, false);
		}

		m_pabHasReligion[eIndex] = bNewValue;

		int iReligionInfluenceChange = GC.getDefineINT("RELIGION_PRESENCE_INFLUENCE");
		changeReligionInfluence(eIndex, bNewValue ? iReligionInfluenceChange : -iReligionInfluenceChange);

		for (int iVoteSource = 0; iVoteSource < GC.getNumVoteSourceInfos(); ++iVoteSource)
		{
			processVoteSourceBonus((VoteSourceTypes)iVoteSource, true);
		}

		GET_PLAYER(getOwnerINLINE()).changeHasReligionCount(eIndex, ((isHasReligion(eIndex)) ? 1 : -1));

		updateMaintenance();
		updateReligionHappiness();
		updateReligionCommerce();

		AI_setAssignWorkDirty(true);

		setInfoDirty(true);

		if (isHasReligion(eIndex))
		{
			GC.getGameINLINE().makeReligionFounded(eIndex, getOwnerINLINE());
		}

		if (bAnnounce)
		{
			if (GC.getGameINLINE().getHolyCity(eIndex) != this)
			{
				for (int iI = 0; iI < MAX_PLAYERS; iI++)
				{
					if (GET_PLAYER((PlayerTypes)iI).isAlive())
					{
						if (isRevealed(GET_PLAYER((PlayerTypes)iI).getTeam(), false))
						{
							if ((getOwnerINLINE() == iI) || (GET_PLAYER((PlayerTypes)iI).getStateReligion() == eIndex) || GET_PLAYER((PlayerTypes)iI).hasHolyCity(eIndex))
							{
								CvWString szBuffer = gDLL->getText(bNewValue ? "TXT_KEY_MISC_RELIGION_SPREAD" : "TXT_KEY_MISC_RELIGION_DISAPPEARANCE", GC.getReligionInfo(eIndex).getTextKeyWide(), getNameKey());
								gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getDefineINT("EVENT_MESSAGE_TIME_LONG"), szBuffer, GC.getReligionInfo(eIndex).getSound(), MESSAGE_TYPE_MAJOR_EVENT, GC.getReligionInfo(eIndex).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), getX_INLINE(), getY_INLINE(), bArrows, bArrows);
							}
						}
					}
				}
			}
		}

		if (isHasReligion(eIndex))
		{
			if (isHuman())
			{
				if (GET_PLAYER(getOwnerINLINE()).getHasReligionCount(eIndex) == 1)
				{
					if (GET_PLAYER(getOwnerINLINE()).canConvert(eIndex) && (GET_PLAYER(getOwnerINLINE()).getStateReligion() == NO_RELIGION))
					{
						CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_CHANGERELIGION);
						if (NULL != pInfo)
						{
							pInfo->setData1(eIndex);
							gDLL->getInterfaceIFace()->addPopup(pInfo, getOwnerINLINE());
						}
					}
				}
			}
		}

		if (bNewValue)
		{
			// Python Event
			CvEventReporter::getInstance().religionSpread(eIndex, getOwnerINLINE(), this);
		}
		else
		{
			// Python Event
			CvEventReporter::getInstance().religionRemove(eIndex, getOwnerINLINE(), this);
		}

	}
}


void CvCity::processVoteSourceBonus(VoteSourceTypes eVoteSource, bool bActive)
{
	if (!GET_PLAYER(getOwnerINLINE()).isLoyalMember(eVoteSource))
	{
		return;
	}

	if (GC.getGameINLINE().isDiploVote(eVoteSource))
	{
		ReligionTypes eReligion = GC.getGameINLINE().getVoteSourceReligion(eVoteSource);

		SpecialistTypes eSpecialist = (SpecialistTypes)GC.getVoteSourceInfo(eVoteSource).getFreeSpecialist();
		if (NO_SPECIALIST != eSpecialist)
		{
			if (NO_RELIGION == eReligion || isHasReligion(eReligion))
			{
				changeFreeSpecialistCount(eSpecialist, bActive ? 1 : -1);
			}
		}

		if (NO_RELIGION != eReligion && isHasReligion(eReligion))
		{
			for (int iYield = 0; iYield < NUM_YIELD_TYPES; ++iYield)
			{
				int iChange = GC.getVoteSourceInfo(eVoteSource).getReligionYield(iYield);
				if (!bActive)
				{
					iChange = -iChange;
				}

				if (0 != iChange)
				{
					for (int iBuilding = 0; iBuilding < GC.getNumBuildingInfos(); ++iBuilding)
					{
						if (GC.getBuildingInfo((BuildingTypes)iBuilding).getReligionType() == eReligion)
						{
							changeBuildingYieldChange((BuildingClassTypes)GC.getBuildingInfo((BuildingTypes)iBuilding).getBuildingClassType(), (YieldTypes)iYield, iChange);
						}
					}
				}
			}

			for (int iCommerce = 0; iCommerce < NUM_COMMERCE_TYPES; ++iCommerce)
			{
				int iChange = GC.getVoteSourceInfo(eVoteSource).getReligionCommerce(iCommerce);
				if (!bActive)
				{
					iChange = -iChange;
				}

				if (0 != iChange)
				{
					for (int iBuilding = 0; iBuilding < GC.getNumBuildingInfos(); ++iBuilding)
					{
						if (GC.getBuildingInfo((BuildingTypes)iBuilding).getReligionType() == eReligion)
						{
							changeBuildingCommerceChange((BuildingClassTypes)GC.getBuildingInfo((BuildingTypes)iBuilding).getBuildingClassType(), (CommerceTypes)iCommerce, iChange);
						}
					}
				}
			}
		}
	}
}


bool CvCity::isHasCorporation(CorporationTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumCorporationInfos(), "eIndex expected to be < GC.getNumCorporationInfos()");
	return m_pabHasCorporation[eIndex];
}


void CvCity::setHasCorporation(CorporationTypes eIndex, bool bNewValue, bool bAnnounce, bool bArrows)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumCorporationInfos(), "eIndex expected to be < GC.getNumCorporationInfos()");

	if (isHasCorporation(eIndex) != bNewValue)
	{
		if (bNewValue)
		{
			bool bReplacedHeadquarters = false;
			for (int iCorp = 0; iCorp < GC.getNumCorporationInfos(); ++iCorp)
			{
				if (iCorp != eIndex && isHasCorporation((CorporationTypes)iCorp))
				{
					if (GC.getGameINLINE().isCompetingCorporation((CorporationTypes)iCorp, eIndex))
					{
						if (GC.getGameINLINE().getHeadquarters((CorporationTypes)iCorp) == this)
						{
							GC.getGameINLINE().replaceCorporation((CorporationTypes)iCorp, eIndex);
							bReplacedHeadquarters = true;
						}
						else
						{
							setHasCorporation((CorporationTypes)iCorp, false, false);
						}
					}
				}
			}

			if (bReplacedHeadquarters)
			{
				return; // already set the corporation in this city
			}
		}

		m_pabHasCorporation[eIndex] = bNewValue;

		GET_PLAYER(getOwnerINLINE()).changeHasCorporationCount(eIndex, ((isHasCorporation(eIndex)) ? 1 : -1));

		CvCity* pHeadquarters = GC.getGameINLINE().getHeadquarters(eIndex);

		if (NULL != pHeadquarters)
		{
			pHeadquarters->updateCorporation();
		}

		updateCorporation();

		AI_setAssignWorkDirty(true);

		setInfoDirty(true);

		if (isHasCorporation(eIndex))
		{
			GC.getGameINLINE().makeCorporationFounded(eIndex, getOwnerINLINE());
		}

		if (bAnnounce)
		{
			for (int iI = 0; iI < MAX_PLAYERS; iI++)
			{
				if (GET_PLAYER((PlayerTypes)iI).isAlive())
				{
					if (getOwnerINLINE() == iI || GET_PLAYER((PlayerTypes)iI).hasHeadquarters(eIndex))
					{
						// edead: begin removal announcement too
						// CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_CORPORATION_SPREAD", GC.getCorporationInfo(eIndex).getTextKeyWide(), getNameKey());
						// gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, GC.getCorporationInfo(eIndex).getSound(), MESSAGE_TYPE_MAJOR_EVENT, GC.getCorporationInfo(eIndex).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), getX_INLINE(), getY_INLINE(), bArrows, bArrows);
						if (bNewValue) {
							CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_CORPORATION_SPREAD", GC.getCorporationInfo(eIndex).getTextKeyWide(), getNameKey());
							gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, GC.getCorporationInfo(eIndex).getSound(), MESSAGE_TYPE_MAJOR_EVENT, GC.getCorporationInfo(eIndex).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), getX_INLINE(), getY_INLINE(), bArrows, bArrows);
						}
						else
						{
							CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_CORPORATION_REMOVED", GC.getCorporationInfo(eIndex).getTextKeyWide(), getNameKey());
							gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, GC.getCorporationInfo(eIndex).getSound(), MESSAGE_TYPE_MAJOR_EVENT, GC.getCorporationInfo(eIndex).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), getX_INLINE(), getY_INLINE(), bArrows, bArrows);
						}
						// edead: end

						if (getOwnerINLINE() == iI)
						{
							CvWStringBuffer szBonusString;
							GAMETEXT.setCorporationHelpCity(szBonusString, eIndex, this);

							CvWString szBonusList;
							bool bFirst = true;
							for (int iJ = 0; iJ < GC.getDefineINT("NUM_CORPORATION_PREREQ_BONUSES"); ++iJ)
							{
								int iBonus = GC.getCorporationInfo(eIndex).getPrereqBonus(iJ);
								if (iBonus != NO_BONUS)
								{
									CvWString szTemp;
									szTemp.Format(L"%s", GC.getBonusInfo((BonusTypes)iBonus).getDescription());
									setListHelp(szBonusList, L"", szTemp, L", ", bFirst);
									bFirst = false;
								}
							}

							// edead: start comment (no bonus info)
							// szBuffer = gDLL->getText("TXT_KEY_MISC_CORPORATION_SPREAD_BONUS", GC.getCorporationInfo(eIndex).getTextKeyWide(), szBonusString.getCString(), getNameKey(), szBonusList.GetCString());
							// gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, GC.getCorporationInfo(eIndex).getSound(), MESSAGE_TYPE_MINOR_EVENT, GC.getCorporationInfo(eIndex).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), getX_INLINE(), getY_INLINE(), bArrows, bArrows);
							// edead: end comment
						}
					}
				}
			}
		}

		if (bNewValue)
		{
			// Python Event
			CvEventReporter::getInstance().corporationSpread(eIndex, getOwnerINLINE(), this);
		}
		else
		{
			// Python Event
			CvEventReporter::getInstance().corporationRemove(eIndex, getOwnerINLINE(), this);
		}
	}
}


CvCity* CvCity::getTradeCity(int iIndex) const
{
	FAssert(iIndex >= 0);
	FAssert(iIndex < GC.getDefineINT("MAX_TRADE_ROUTES"));
	return getCity(m_paTradeCities[iIndex]);
}


int CvCity::getTradeRoutes() const
{
	int iTradeRoutes;

	iTradeRoutes = GC.getGameINLINE().getTradeRoutes();
	iTradeRoutes += GET_PLAYER(getOwnerINLINE()).getTradeRoutes();
	if (isCoastal(GC.getMIN_WATER_SIZE_FOR_OCEAN()))
	{
		iTradeRoutes += GET_PLAYER(getOwnerINLINE()).getCoastalTradeRoutes();
	}
	iTradeRoutes += getExtraTradeRoutes();

	return std::min(iTradeRoutes, GC.getDefineINT("MAX_TRADE_ROUTES"));
}


void CvCity::clearTradeRoutes()
{
	CvCity* pLoopCity;
	int iI;

	for (iI = 0; iI < GC.getDefineINT("MAX_TRADE_ROUTES"); iI++)
	{
		pLoopCity = getTradeCity(iI);

		if (pLoopCity != NULL)
		{
			pLoopCity->setTradeRoute(getOwnerINLINE(), false);
		}

		m_paTradeCities[iI].reset();
	}
}


// XXX eventually, this needs to be done when roads are built/destroyed...
void CvCity::updateTradeRoutes()
{
	int* paiBestValue;
	CvCity* pLoopCity;
	int iTradeRoutes;
	int iTradeProfit;
	int iValue;
	int iLoop;
	int iI, iJ, iK;

	paiBestValue = new int[GC.getDefineINT("MAX_TRADE_ROUTES")];

	for (iI = 0; iI < GC.getDefineINT("MAX_TRADE_ROUTES"); iI++)
	{
		paiBestValue[iI] = 0;
	}

	clearTradeRoutes();

	if (!isDisorder() && !isPlundered())
	{
		iTradeRoutes = getTradeRoutes();

		FAssert(iTradeRoutes <= GC.getDefineINT("MAX_TRADE_ROUTES"));

		for (iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if (GET_PLAYER(getOwnerINLINE()).canHaveTradeRoutesWith((PlayerTypes)iI))
			{
				for (pLoopCity = GET_PLAYER((PlayerTypes)iI).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER((PlayerTypes)iI).nextCity(&iLoop))
				{
					if (pLoopCity != this)
					{
						if (!(pLoopCity->isTradeRoute(getOwnerINLINE())) || (getTeam() == GET_PLAYER((PlayerTypes)iI).getTeam()))
						{
							if (pLoopCity->plotGroup(getOwnerINLINE()) == plotGroup(getOwnerINLINE()) || GC.getDefineINT("IGNORE_PLOT_GROUP_FOR_TRADE_ROUTES"))
							{
// BUG - Fractional Trade Routes - start
#ifdef _MOD_FRACTRADE
								iValue = calculateTradeProfitTimes100(pLoopCity);
#else
								iValue = calculateTradeProfit(pLoopCity);
#endif
// BUG - Fractional Trade Routes - end

								for (iJ = 0; iJ < iTradeRoutes; iJ++)
								{
									if (iValue > paiBestValue[iJ])
									{
										for (iK = (iTradeRoutes - 1); iK > iJ; iK--)
										{
											paiBestValue[iK] = paiBestValue[(iK - 1)];
											m_paTradeCities[iK] = m_paTradeCities[(iK - 1)];
										}

										paiBestValue[iJ] = iValue;
										m_paTradeCities[iJ] = pLoopCity->getIDInfo();

										break;
									}
								}
							}
						}
					}
				}
			}
		}
	}

	iTradeProfit = 0;

	for (iI = 0; iI < GC.getDefineINT("MAX_TRADE_ROUTES"); iI++)
	{
		pLoopCity = getTradeCity(iI);

		if (pLoopCity != NULL)
		{
			pLoopCity->setTradeRoute(getOwnerINLINE(), true);

// BUG - Fractional Trade Routes - start
#ifdef _MOD_FRACTRADE
			iTradeProfit += calculateTradeProfitTimes100(pLoopCity);
#else
			iTradeProfit += calculateTradeProfit(pLoopCity);
#endif
// BUG - Fractional Trade Routes - end
		}
	}

	for (iI = 0; iI < NUM_YIELD_TYPES; iI++)
	{
// BUG - Fractional Trade Routes - start
#ifdef _MOD_FRACTRADE
		setTradeYield(((YieldTypes)iI), calculateTradeYield(((YieldTypes)iI), iTradeProfit) / 100); // XXX could take this out if handled when CvPlotGroup changes...
#else
		setTradeYield(((YieldTypes)iI), calculateTradeYield(((YieldTypes)iI), iTradeProfit)); // XXX could take this out if handled when CvPlotGroup changes...
#endif
// BUG - Fractional Trade Routes - end
	}

	SAFE_DELETE_ARRAY(paiBestValue);
}


void CvCity::clearOrderQueue()
{
	while (headOrderQueueNode() != NULL)
	{
		popOrder(0);
	}

	if ((getTeam() == GC.getGameINLINE().getActiveTeam()) || GC.getGameINLINE().isDebugMode())
	{
		setInfoDirty(true);
	}
}


void CvCity::pushOrder(OrderTypes eOrder, int iData1, int iData2, bool bSave, bool bPop, bool bAppend, bool bForce)
{
  OrderData order;
	bool bValid;
	bool bBuildingUnit = false;
	bool bBuildingBuilding = false;

	if (bPop)
	{
		popOrder(0);
	}

	bValid = false;

  switch (eOrder)
  {
	case ORDER_TRAIN:
		if (canTrain((UnitTypes)iData1) || bForce)
		{
			if (iData2 == -1)
			{
				iData2 = GC.getUnitInfo((UnitTypes)iData1).getDefaultUnitAIType();
			}

			GET_PLAYER(getOwnerINLINE()).changeUnitClassMaking(((UnitClassTypes)(GC.getUnitInfo((UnitTypes) iData1).getUnitClassType())), 1);

			area()->changeNumTrainAIUnits(getOwnerINLINE(), ((UnitAITypes)iData2), 1);
			GET_PLAYER(getOwnerINLINE()).AI_changeNumTrainAIUnits(((UnitAITypes)iData2), 1);

			bValid = true;
			bBuildingUnit = true;
/*************************************************************************************************/
/**	SPEEDTWEAK (Block Python) Sephi                                               	            **/
/**	If you want to allow modmodders to enable this Callback, see CvCity::cancreate for example  **/
/*************************************************************************************************/
/**
			CvEventReporter::getInstance().cityBuildingUnit(this, (UnitTypes)iData1);
/*************************************************************************************************/
/**	END	                                        												**/
/*************************************************************************************************/
		}
    break;

	case ORDER_CONSTRUCT:
		if (canConstruct((BuildingTypes)iData1) || bForce)
		{
			GET_PLAYER(getOwnerINLINE()).changeBuildingClassMaking(((BuildingClassTypes)(GC.getBuildingInfo((BuildingTypes) iData1).getBuildingClassType())), 1);

			bValid = true;
			bBuildingBuilding = true;
/*************************************************************************************************/
/**	SPEEDTWEAK (Block Python) Sephi                                               	            **/
/**	If you want to allow modmodders to enable this Callback, see CvCity::cancreate for example  **/
/*************************************************************************************************/
/**
			CvEventReporter::getInstance().cityBuildingBuilding(this, (BuildingTypes)iData1);
/*************************************************************************************************/
/**	END	                                        												**/
/*************************************************************************************************/
		}
		break;

	case ORDER_CREATE:
		if (canCreate((ProjectTypes)iData1) || bForce)
		{
			GET_TEAM(getTeam()).changeProjectMaking(((ProjectTypes)iData1), 1);

			bValid = true;
// BUG - Project Started Event - start
			CvEventReporter::getInstance().cityBuildingProject(this, (ProjectTypes)iData1);
// BUG - Project Started Event - end
		}
		break;

	case ORDER_MAINTAIN:
		if (canMaintain((ProcessTypes)iData1) || bForce)
		{
			bValid = true;
// BUG - Process Started Event - start
			CvEventReporter::getInstance().cityBuildingProcess(this, (ProcessTypes)iData1);
// BUG - Process Started Event - end
		}
		break;

  default:
    FAssertMsg(false, "iOrder did not match a valid option");
    break;
  }

	if (!bValid)
	{
		return;
	}

  order.eOrderType = eOrder;
	order.iData1 = iData1;
	order.iData2 = iData2;
	order.bSave = bSave;

	if (bAppend)
	{
		m_orderQueue.insertAtEnd(order);
	}
	else
	{
		stopHeadOrder();
		m_orderQueue.insertAtBeginning(order);
	}

	if (!bAppend || (getOrderQueueLength() == 1))
	{
		startHeadOrder();
	}

	// Why does this cause a crash???

/*	if (bBuildingUnit)
	{
		CvEventReporter::getInstance().cityBuildingUnit(this, (UnitTypes)iData1);
	}
	else if (bBuildingBuilding)
	{
		CvEventReporter::getInstance().cityBuildingBuilding(this, (BuildingTypes)iData1);
	}*/

	if ((getTeam() == GC.getGameINLINE().getActiveTeam()) || GC.getGameINLINE().isDebugMode())
	{
		setInfoDirty(true);

		if (isCitySelected())
		{
			gDLL->getInterfaceIFace()->setDirty(InfoPane_DIRTY_BIT, true );
			gDLL->getInterfaceIFace()->setDirty(SelectionButtons_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(CityScreen_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(PlotListButtons_DIRTY_BIT, true);
		}
	}
}


void CvCity::popOrder(int iNum, bool bFinish, bool bChoose)
{
	CLLNode<OrderData>* pOrderNode;
	CvUnit* pUnit;
	CvPlot* pRallyPlot;
	wchar szBuffer[1024];
	wchar szTempBuffer[1024];
	TCHAR szSound[1024];
	ProjectTypes eCreateProject;
	BuildingTypes eConstructBuilding;
	UnitTypes eTrainUnit;
	UnitAITypes eTrainAIUnit;
	bool bWasFoodProduction;
	bool bStart;
	bool bMessage;
	int iCount;
	int iProductionNeeded;
	int iOverflow;

	bWasFoodProduction = isFoodProduction();

	if (iNum == -1)
	{
		iNum = (getOrderQueueLength() - 1);
	}

	iCount = 0;

	pOrderNode = headOrderQueueNode();

	while (pOrderNode != NULL)
	{
		if (iCount == iNum)
		{
			break;
		}

		iCount++;

		pOrderNode = nextOrderQueueNode(pOrderNode);
	}

  if (pOrderNode == NULL)
  {
		return;
	}

	if (bFinish && pOrderNode->m_data.bSave)
	{
		pushOrder(pOrderNode->m_data.eOrderType, pOrderNode->m_data.iData1, pOrderNode->m_data.iData2, true, false, true);
	}

	eTrainUnit = NO_UNIT;
	eConstructBuilding = NO_BUILDING;
	eCreateProject = NO_PROJECT;

	switch (pOrderNode->m_data.eOrderType)
	{
	case ORDER_TRAIN:
		eTrainUnit = ((UnitTypes)(pOrderNode->m_data.iData1));
		eTrainAIUnit = ((UnitAITypes)(pOrderNode->m_data.iData2));
		FAssertMsg(eTrainUnit != NO_UNIT, "eTrainUnit is expected to be assigned a valid unit type");
		FAssertMsg(eTrainAIUnit != NO_UNITAI, "eTrainAIUnit is expected to be assigned a valid unit AI type");

		GET_PLAYER(getOwnerINLINE()).changeUnitClassMaking(((UnitClassTypes)(GC.getUnitInfo(eTrainUnit).getUnitClassType())), -1);

		area()->changeNumTrainAIUnits(getOwnerINLINE(), eTrainAIUnit, -1);
		GET_PLAYER(getOwnerINLINE()).AI_changeNumTrainAIUnits(eTrainAIUnit, -1);

		if (bFinish)
		{
			iProductionNeeded = getProductionNeeded(eTrainUnit);

			// max overflow is the value of the item produced (to eliminate prebuild exploits)
			iOverflow = getUnitProduction(eTrainUnit) - iProductionNeeded;
			int iMaxOverflow = std::max(iProductionNeeded, getCurrentProductionDifference(false, false));
// BUG - Overflow Gold Fix - start
			int iLostProduction = std::max(0, iOverflow - iMaxOverflow);
// BUG - Overflow Gold Fix - end
			iOverflow = std::min(iMaxOverflow, iOverflow);
			if (iOverflow > 0)
			{
				changeOverflowProduction(iOverflow, getProductionModifier(eTrainUnit));
			}
			setUnitProduction(eTrainUnit, 0);

// BUG - Overflow Gold Fix - start
			iLostProduction *= getBaseYieldRateModifier(YIELD_PRODUCTION);
			iLostProduction /= std::max(1, getBaseYieldRateModifier(YIELD_PRODUCTION, getProductionModifier(eTrainUnit)));
			int iProductionGold = ((iLostProduction * GC.getDefineINT("MAXED_UNIT_GOLD_PERCENT")) / 100);
// BUG - Overflow Gold Fix - end
			if (iProductionGold > 0)
			{
				GET_PLAYER(getOwnerINLINE()).changeGold(iProductionGold);
			}


			pUnit = GET_PLAYER(getOwnerINLINE()).initUnit(eTrainUnit, getX_INLINE(), getY_INLINE(), eTrainAIUnit);
			FAssertMsg(pUnit != NULL, "pUnit is expected to be assigned a valid unit object");

			pUnit->finishMoves();

			// Leoreth: if unit was hurried, apply the mercenary promotion, and reset the hurry memory
			if (isUnitHurried(eTrainUnit))
			{
				pUnit->setHasPromotion((PromotionTypes)GC.getInfoTypeForString("PROMOTION_MERCENARY"), true);
				setUnitHurried(eTrainUnit, false);
			}

			addProductionExperience(pUnit);

			pRallyPlot = getRallyPlot();

			if (pRallyPlot != NULL)
			{
				pUnit->getGroup()->pushMission(MISSION_MOVE_TO, pRallyPlot->getX_INLINE(), pRallyPlot->getY_INLINE());
			}

			if (isHuman())
			{
				if (GET_PLAYER(getOwnerINLINE()).isOption(PLAYEROPTION_START_AUTOMATED))
				{
					pUnit->automate(AUTOMATE_BUILD);
				}

				if (GET_PLAYER(getOwnerINLINE()).isOption(PLAYEROPTION_MISSIONARIES_AUTOMATED))
				{
					pUnit->automate(AUTOMATE_RELIGION);
				}
			}

			CvEventReporter::getInstance().unitBuilt(this, pUnit);

			if (GC.getUnitInfo(eTrainUnit).getDomainType() == DOMAIN_AIR)
			{
				if (plot()->countNumAirUnits(getTeam()) > getAirUnitCapacity(getTeam()))
				{
					pUnit->jumpToNearestValidPlot();  // can destroy unit
				}
			}
		}
		break;

	case ORDER_CONSTRUCT:
		eConstructBuilding = ((BuildingTypes)(pOrderNode->m_data.iData1));

		GET_PLAYER(getOwnerINLINE()).changeBuildingClassMaking(((BuildingClassTypes)(GC.getBuildingInfo(eConstructBuilding).getBuildingClassType())), -1);

		if (bFinish)
		{
/*************************************************************************************************/
/* UNOFFICIAL_PATCH                       10/08/09                  davidlallen & jdog5000       */
/*                                                                                               */
/* Bugfix                                                                                        */
/*************************************************************************************************/
/* original bts code
			if (GET_PLAYER(getOwnerINLINE()).isBuildingClassMaxedOut(((BuildingClassTypes)(GC.getBuildingInfo(eConstructBuilding).getBuildingClassType())), 1))
*/
			if (GET_PLAYER(getOwnerINLINE()).isBuildingClassMaxedOut(((BuildingClassTypes)(GC.getBuildingInfo(eConstructBuilding).getBuildingClassType())), GC.getBuildingClassInfo((BuildingClassTypes)(GC.getBuildingInfo(eConstructBuilding).getBuildingClassType())).getExtraPlayerInstances()))
/*************************************************************************************************/
/* UNOFFICIAL_PATCH                         END                                                  */
/*************************************************************************************************/
			{
				GET_PLAYER(getOwnerINLINE()).removeBuildingClass((BuildingClassTypes)(GC.getBuildingInfo(eConstructBuilding).getBuildingClassType()));
			}

			setNumRealBuilding(eConstructBuilding, getNumRealBuilding(eConstructBuilding) + 1);

			iProductionNeeded = getProductionNeeded(eConstructBuilding);
			// max overflow is the value of the item produced (to eliminate prebuild exploits)
			int iOverflow = getBuildingProduction(eConstructBuilding) - iProductionNeeded;
			int iMaxOverflow = std::max(iProductionNeeded, getCurrentProductionDifference(false, false));
// BUG - Overflow Gold Fix - start
			int iLostProduction = std::max(0, iOverflow - iMaxOverflow);
// BUG - Overflow Gold Fix - end
			iOverflow = std::min(iMaxOverflow, iOverflow);
			if (iOverflow > 0)
			{
				changeOverflowProduction(iOverflow, getProductionModifier(eConstructBuilding));
			}
			setBuildingProduction(eConstructBuilding, 0);

// BUG - Overflow Gold Fix - start
			iLostProduction *= getBaseYieldRateModifier(YIELD_PRODUCTION);
			iLostProduction /= std::max(1, getBaseYieldRateModifier(YIELD_PRODUCTION, getProductionModifier(eConstructBuilding)));
			int iProductionGold = ((iLostProduction * GC.getDefineINT("MAXED_BUILDING_GOLD_PERCENT")) / 100);
// BUG - Overflow Gold Fix - end
			if (iProductionGold > 0)
			{
				GET_PLAYER(getOwnerINLINE()).changeGold(iProductionGold);
			}

			//Rhye - start
			if (eConstructBuilding == OLYMPIC_PARK) {
				GET_PLAYER(getOwnerINLINE()).setOlympics(true);
			}
			//Rhye - end

			CvEventReporter::getInstance().buildingBuilt(this, eConstructBuilding);
		}
		break;

	case ORDER_CREATE:
		eCreateProject = ((ProjectTypes)(pOrderNode->m_data.iData1));

		GET_TEAM(getTeam()).changeProjectMaking(eCreateProject, -1);

		if (bFinish)
		{
			// Event reported to Python before the project is built, so that we can show the movie before awarding free techs, for example
			CvEventReporter::getInstance().projectBuilt(this, eCreateProject);

			GET_TEAM(getTeam()).changeProjectCount(eCreateProject, 1);

			if (GC.getProjectInfo(eCreateProject).isSpaceship())
			{
				bool needsArtType = true;
				VictoryTypes eVictory = (VictoryTypes)GC.getProjectInfo(eCreateProject).getVictoryPrereq();

				if (NO_VICTORY != eVictory && GET_TEAM(getTeam()).canLaunch(eVictory))
				{
					if (isHuman())
					{
						CvPopupInfo* pInfo = NULL;

						if (GC.getGameINLINE().isNetworkMultiPlayer())
						{
							pInfo = new CvPopupInfo(BUTTONPOPUP_LAUNCH, GC.getProjectInfo(eCreateProject).getVictoryPrereq());
						}
						else
						{
							pInfo = new CvPopupInfo(BUTTONPOPUP_PYTHON_SCREEN, eCreateProject);
							pInfo->setText(L"showSpaceShip");
							needsArtType = false;
						}

						gDLL->getInterfaceIFace()->addPopup(pInfo, getOwnerINLINE());
					}
					else
					{
						GET_PLAYER(getOwnerINLINE()).AI_launch(eVictory);
					}
				}
				else
				{
					//show the spaceship progress
					if(isHuman())
					{
						if(!GC.getGameINLINE().isNetworkMultiPlayer())
						{
							CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_PYTHON_SCREEN, eCreateProject);
							pInfo->setText(L"showSpaceShip");
							gDLL->getInterfaceIFace()->addPopup(pInfo, getOwnerINLINE());
							needsArtType = false;
						}
					}
				}

				if(needsArtType)
				{
                    int defaultArtType = GET_TEAM(getTeam()).getProjectDefaultArtType(eCreateProject);
					int projectCount = GET_TEAM(getTeam()).getProjectCount(eCreateProject);
					GET_TEAM(getTeam()).setProjectArtType(eCreateProject, projectCount - 1, defaultArtType);
				}
			}

			iProductionNeeded = getProductionNeeded(eCreateProject);
			// max overflow is the value of the item produced (to eliminate pre-build exploits)
			iOverflow = getProjectProduction(eCreateProject) - iProductionNeeded;
			int iMaxOverflow = std::max(iProductionNeeded, getCurrentProductionDifference(false, false));
// BUG - Overflow Gold Fix - start
			int iLostProduction = std::max(0, iOverflow - iMaxOverflow);
// BUG - Overflow Gold Fix - end
			iOverflow = std::min(iMaxOverflow, iOverflow);
			if (iOverflow > 0)
			{
				changeOverflowProduction(iOverflow, getProductionModifier(eCreateProject));
			}
			setProjectProduction(eCreateProject, 0);

// BUG - Overflow Gold Fix - start
			iLostProduction *= getBaseYieldRateModifier(YIELD_PRODUCTION);
			iLostProduction /= std::max(1, getBaseYieldRateModifier(YIELD_PRODUCTION, getProductionModifier(eCreateProject)));
			int iProductionGold = ((iLostProduction * GC.getDefineINT("MAXED_PROJECT_GOLD_PERCENT")) / 100);
// BUG - Overflow Gold Fix - end
			if (iProductionGold > 0)
			{
				GET_PLAYER(getOwnerINLINE()).changeGold(iProductionGold);
			}
		}
		break;

	case ORDER_MAINTAIN:
		break;

	default:
		FAssertMsg(false, "pOrderNode->m_data.eOrderType is not a valid option");
		break;
	}

	if (pOrderNode == headOrderQueueNode())
	{
		bStart = true;
		stopHeadOrder();
	}
	else
	{
		bStart = false;
	}

	m_orderQueue.deleteNode(pOrderNode);
	pOrderNode = NULL;

	if (bStart)
	{
		startHeadOrder();
	}

	if ((getTeam() == GC.getGameINLINE().getActiveTeam()) || GC.getGameINLINE().isDebugMode())
	{
		setInfoDirty(true);

		if (isCitySelected())
		{
			gDLL->getInterfaceIFace()->setDirty(InfoPane_DIRTY_BIT, true );
			gDLL->getInterfaceIFace()->setDirty(SelectionButtons_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(CityScreen_DIRTY_BIT, true);
		}
	}

	bMessage = false;

	if (bChoose)
	{
		if (getOrderQueueLength() == 0)
		{
			if (!isHuman() || isProductionAutomated())
			{
				AI_chooseProduction();
			}
			else
			{
				if (bWasFoodProduction)
				{
					AI_assignWorkingPlots();
				}

				chooseProduction(eTrainUnit, eConstructBuilding, eCreateProject, bFinish);

				bMessage = true;
			}
		}
	}

	LPCSTR szIcon = NULL;

	if (bFinish && !bMessage)
	{
		if (eTrainUnit != NO_UNIT)
		{
			swprintf(szBuffer, gDLL->getText(((isLimitedUnitClass((UnitClassTypes)(GC.getUnitInfo(eTrainUnit).getUnitClassType()))) ? "TXT_KEY_MISC_TRAINED_UNIT_IN_LIMITED" : "TXT_KEY_MISC_TRAINED_UNIT_IN"), GC.getUnitInfo(eTrainUnit).getTextKeyWide(), getNameKey()).GetCString());
			strcpy( szSound, GC.getUnitInfo(eTrainUnit).getArtInfo(0,GET_PLAYER(getOwnerINLINE()).getCurrentEra(), NO_UNIT_ARTSTYLE)->getTrainSound() );
			szIcon = GET_PLAYER(getOwnerINLINE()).getUnitButton(eTrainUnit);
		}
		else if (eConstructBuilding != NO_BUILDING)
		{
			swprintf(szBuffer, gDLL->getText(((isLimitedWonderClass((BuildingClassTypes)(GC.getBuildingInfo(eConstructBuilding).getBuildingClassType()))) ? "TXT_KEY_MISC_CONSTRUCTED_BUILD_IN_LIMITED" : "TXT_KEY_MISC_CONSTRUCTED_BUILD_IN"), GC.getBuildingInfo(eConstructBuilding).getTextKeyWide(), getNameKey()).GetCString());
			strcpy(szSound, GC.getBuildingInfo(eConstructBuilding).getConstructSound());
			szIcon = GC.getBuildingInfo(eConstructBuilding).getButton();
		}
		else if (eCreateProject != NO_PROJECT)
		{
			swprintf(szBuffer, gDLL->getText(((isLimitedProject(eCreateProject)) ? "TXT_KEY_MISC_CREATED_PROJECT_IN_LIMITED" : "TXT_KEY_MISC_CREATED_PROJECT_IN"), GC.getProjectInfo(eCreateProject).getTextKeyWide(), getNameKey()).GetCString());
			strcpy(szSound, GC.getProjectInfo(eCreateProject).getCreateSound());
			szIcon = GC.getProjectInfo(eCreateProject).getButton();
		}
		if (isProduction())
		{
			swprintf(szTempBuffer, gDLL->getText(((isProductionLimited()) ? "TXT_KEY_MISC_WORK_HAS_BEGUN_LIMITED" : "TXT_KEY_MISC_WORK_HAS_BEGUN"), getProductionNameKey()).GetCString());
			wcscat(szBuffer, szTempBuffer);
		}
		gDLL->getInterfaceIFace()->addMessage(getOwnerINLINE(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, szSound, MESSAGE_TYPE_MINOR_EVENT, szIcon, (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), getX_INLINE(), getY_INLINE(), true, true);
	}

	if ((getTeam() == GC.getGameINLINE().getActiveTeam()) || GC.getGameINLINE().isDebugMode())
	{
		setInfoDirty(true);

		if (isCitySelected())
		{
			gDLL->getInterfaceIFace()->setDirty(InfoPane_DIRTY_BIT, true );
			gDLL->getInterfaceIFace()->setDirty(SelectionButtons_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(CityScreen_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(PlotListButtons_DIRTY_BIT, true);
		}
	}
}


void CvCity::startHeadOrder()
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		if (pOrderNode->m_data.eOrderType == ORDER_MAINTAIN)
		{
			processProcess(((ProcessTypes)(pOrderNode->m_data.iData1)), 1);
		}

		AI_setAssignWorkDirty(true);
	}
}


void CvCity::stopHeadOrder()
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		if (pOrderNode->m_data.eOrderType == ORDER_MAINTAIN)
		{
			processProcess(((ProcessTypes)(pOrderNode->m_data.iData1)), -1);
		}
	}
}


int CvCity::getOrderQueueLength()
{
	return m_orderQueue.getLength();
}

OrderData* CvCity::getOrderFromQueue(int iIndex)
{
	CLLNode<OrderData>* pOrderNode;

	pOrderNode = m_orderQueue.nodeNum(iIndex);

	if (pOrderNode != NULL)
	{
		return &(pOrderNode->m_data);
	}
	else
	{
		return NULL;
	}
}

CLLNode<OrderData>* CvCity::nextOrderQueueNode(CLLNode<OrderData>* pNode) const
{
	return m_orderQueue.next(pNode);
}

CLLNode<OrderData>* CvCity::headOrderQueueNode() const
{
	return m_orderQueue.head();
}

int CvCity::getNumOrdersQueued() const
{
	return m_orderQueue.getLength();
}

OrderData CvCity::getOrderData(int iIndex) const
{
	int iCount = 0;
	CLLNode<OrderData>* pNode = headOrderQueueNode();
	while (pNode != NULL)
	{
		if (iIndex == iCount)
		{
			return pNode->m_data;
		}
		iCount++;
		pNode = nextOrderQueueNode(pNode);
	}
	OrderData kData;
	kData.eOrderType = NO_ORDER;
	kData.iData1 = -1;
	kData.iData2 = -1;
	kData.bSave = false;
	return kData;
}

void CvCity::setWallOverridePoints(const std::vector< std::pair<float, float> >& kPoints)
{
	m_kWallOverridePoints = kPoints;
	setLayoutDirty(true);
}

const std::vector< std::pair<float, float> >& CvCity::getWallOverridePoints() const
{
	return m_kWallOverridePoints;
}

// Protected Functions...

void CvCity::doGrowth()
{
	int iDiff;

	//Rhye - start
//Speed: Modified by Kael 04/19/2007
//	CyArgsList argsList;
//	argsList.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
//	long lResult=0;
//	gDLL->getPythonIFace()->callFunction(PYGameModule, "doGrowth", argsList.makeFunctionArgs(), &lResult);
//	delete pyCity;	// python fxn must not hold on to this pointer
//	if (lResult == 1)
//	{
//		return;
//	}
//FfH: End Modify
	//Rhye - end

	iDiff = foodDifference();

	changeFood(iDiff);
	changeFoodKept(iDiff);

	setFoodKept(range(getFoodKept(), 0, ((growthThreshold() * getMaxFoodKeptPercent()) / 100)));

	if (getFood() >= growthThreshold())
	{
		if (AI_isEmphasizeAvoidGrowth())
		{
			setFood(growthThreshold());
		}
		else
		{
			changeFood(-(std::max(0, (growthThreshold() - getFoodKept()))));
			changePopulation(1);

			// ONEVENT - City growth
			CvEventReporter::getInstance().cityGrowth(this, getOwnerINLINE());
		}
	}
	else if (getFood() < 0)
	{
		changeFood(-(getFood()));

		if (getPopulation() > 1)
		{
			changePopulation(-1);
		}
	}
}


void CvCity::doCulture()
{
	if 	(getCommerceRate(COMMERCE_CULTURE) <= 4)
	{
		changeCultureTimes100(getOwnerINLINE(), getCommerceRateTimes100(COMMERCE_CULTURE), false, true);
		return;
	}

	PlayerTypes eOwner = getOwnerINLINE();
	int iCultureModifier = GET_PLAYER(eOwner).getModifier(MODIFIER_CULTURE);

	changeCultureTimes100(eOwner, getCommerceRateTimes100(COMMERCE_CULTURE) * iCultureModifier / 100, false, true);

	// Leoreth: let culture of dead civilizations decay
	int iTotalCultureTimes100 = countTotalCultureTimes100();

	PlayerTypes ePlayer;
	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		ePlayer = (PlayerTypes)iI;
		if (!GET_PLAYER(ePlayer).isAlive() && getCulture(ePlayer) > 0)
		{
			// culture of dead civilizations decreases by 1% of total city culture per turn
			changeCultureTimes100(ePlayer, -iTotalCultureTimes100 / 100, false, true);
		}
	}
}


void CvCity::doPlotCulture(bool bUpdate, PlayerTypes ePlayer, int iCultureRate)
{
	CvPlot* pLoopPlot;
	int iDX, iDY;
	int iCultureRange;
	CultureLevelTypes eCultureLevel = (CultureLevelTypes)0;

	//Rhye - start
//Speed: Modified by Kael 04/19/2007
//	CyCity* pyCity = new CyCity(this);
//	CyArgsList argsList;
//	argsList.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
//	argsList.add(bUpdate);
//	long lResult=0;
//	gDLL->getPythonIFace()->callFunction(PYGameModule, "doPlotCulture", argsList.makeFunctionArgs(), &lResult);
//	delete pyCity;	// python fxn must not hold on to this pointer
//	if (lResult == 1)
//	{
//		return;
//	}
//Speed: End Modify
	//Rhye - end

	FAssert(NO_PLAYER != ePlayer);

	if (getOwnerINLINE() == ePlayer)
	{
		eCultureLevel = getCultureLevel();
	}
	else
	{
		for (int iI = (GC.getNumCultureLevelInfos() - 1); iI > 0; iI--)
		{
			if (getCultureTimes100(ePlayer) >= 100 * GC.getGameINLINE().getCultureThreshold((CultureLevelTypes)iI))
			{
				eCultureLevel = (CultureLevelTypes)iI;
				break;
			}
		}
	}

	int iFreeCultureRate = GC.getDefineINT("CITY_FREE_CULTURE_GROWTH_FACTOR");
	if (getCultureTimes100(ePlayer) > 0)
	{
		/*for (int iI = 0; iI < getNextCoveredPlot(); iI++)
		{
			pLoopPlot = GC.getMap().plotByIndex(getCulturePlot(iI));

			if (pLoopPlot->isPotentialCityWorkForArea(area()))
			{
				// Leoreth: culture can only invade foreign core if city itself is in foreign core
				bool bCanSpreadCore = true;

				if (!pLoopPlot->isCore(ePlayer))
				{
					for (int iJ = 0; iJ < NUM_MAJOR_PLAYERS; iJ++)
					{
						// Leoreth: only for civs that have already spawned yet
						if (GC.getGame().getGameTurnYear() < startingTurnYear[iJ]) continue;

						if (pLoopPlot->isCore((PlayerTypes)iJ) && !plot()->isCore((PlayerTypes)iJ)) bCanSpreadCore = false;

						if (pLoopPlot->isCore((PlayerTypes)iJ) && plot()->isCore((PlayerTypes)iJ))
						{
							bCanSpreadCore = true;
							break;
						}
					}
				}

				if (bCanSpreadCore)
				{
					// Leoreth: probably needs a more sophistated calculation now with iCultureRange
					int iChange = ((eCultureLevel - iCultureRange) * iFreeCultureRate) + iCultureRate + 1;
					if (ePlayer == ITALY) iChange /= 2;
					pLoopPlot->changeCulture(ePlayer, iChange, (bUpdate || !(pLoopPlot->isOwned())));
				}
			}
		}*/

		if (eCultureLevel != NO_CULTURELEVEL)
		{
			for (iDX = -eCultureLevel; iDX <= eCultureLevel; iDX++)
			{
				for (iDY = -eCultureLevel; iDY <= eCultureLevel; iDY++)
				{
					iCultureRange = cultureDistance(iDX, iDY);

					if (iCultureRange <= eCultureLevel)
					{
						pLoopPlot = plotXY(getX_INLINE(), getY_INLINE(), iDX, iDY);

						if (pLoopPlot != NULL)
						{
							if (pLoopPlot->isPotentialCityWorkForArea(area()) || getOwnerINLINE() == POLYNESIA)
							{
								// Leoreth: culture can only invade foreign core if city itself is in foreign core
								bool bCanSpreadCore = true;

								if (!pLoopPlot->isCore(ePlayer) && iCultureRange > 2)
								{
									for (int iI = 0; iI < NUM_MAJOR_PLAYERS; iI++)
									{
										// Leoreth: only for civs that have already spawned yet
										if (GC.getGame().getGameTurnYear() < GET_PLAYER((PlayerTypes)iI).getBirthYear()) continue;

										if (pLoopPlot->isCore((PlayerTypes)iI) && !plot()->isCore((PlayerTypes)iI)) bCanSpreadCore = false;

										if (pLoopPlot->isCore((PlayerTypes)iI) && plot()->isCore((PlayerTypes)iI))
										{
											bCanSpreadCore = true;
											break;
										}
									}
								}

								if (bCanSpreadCore)
								{
									int iChange = ((eCultureLevel - iCultureRange) * iFreeCultureRate) + iCultureRate + 1;
									if (ePlayer == ITALY) iChange /= 2;
									pLoopPlot->changeCulture(ePlayer, iChange, (bUpdate || !(pLoopPlot->isOwned())));
								}
							}
						}
					}
				}
			}
		}
	}
}

// This function has essentially been rewriten for K-Mod. (and it use to not be 'times 100')
// A note about scale: the city plot itself gets roughly 10x culture. The outer edges of the cultural influence get 1x culture (ie. the influence that extends beyond the borders).
void CvCity::doPlotCultureTimes100(bool bUpdate, PlayerTypes ePlayer, int iCultureRateTimes100, bool bCityCulture)
{
	CultureLevelTypes eCultureLevel = (CultureLevelTypes)0;

	/*if (GC.getUSE_DO_PLOT_CULTURE_CALLBACK()) // K-Mod. block unused python callbacks
	{
		CyCity* pyCity = new CyCity(this);
		CyArgsList argsList;
		argsList.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
		argsList.add(bUpdate);
		argsList.add(ePlayer);
		//argsList.add(iCultureRate);
		argsList.add(iCultureRateTimes100/100); // K-Mod
		long lResult=0;
		gDLL->getPythonIFace()->callFunction(PYGameModule, "doPlotCulture", argsList.makeFunctionArgs(), &lResult);
		delete pyCity;	// python fxn must not hold on to this pointer 
		if (lResult == 1)
		{
			return;
		}
	}*/

	FAssert(NO_PLAYER != ePlayer);

	if (getOwnerINLINE() == ePlayer)
	{
		eCultureLevel = getCultureLevel();
	}
	else
	{
		for (int iI = (GC.getNumCultureLevelInfos() - 1); iI > 0; iI--)
		{
			if (getCultureTimes100(ePlayer) >= 100 * GC.getGameINLINE().getCultureThreshold((CultureLevelTypes)iI))
			{
				eCultureLevel = (CultureLevelTypes)iI;
				break;
			}
		}
	}

/**
*** K-Mod, 30/oct/10, Karadoc
*** increased culture range, added a percentage based distance bonus (decreasing the importance flat rate bonus).
**/
	// (original bts code deleted)

	// Experimental culture profile...
	// Ae^(-bx). A = 10 (no effect), b = log(full_range_ratio)/range
	// (iScale-1)(iDistance - iRange)^2/(iRange^2) + 1   // This approximates the exponential pretty well
	const int iScale = 10;
	const int iCultureRange = eCultureLevel + 3;

	//const int iOuterRatio = 10;
	//const double iB = log((double)iOuterRatio)/iCultureRange;

	// free culture bonus for cities
	iCultureRateTimes100+=(bCityCulture && iCultureRateTimes100 > 0)?600 :0;

	// note, original code had "if (getCultureTimes100(ePlayer) > 0)". I took that part out.
	if (eCultureLevel != NO_CULTURELEVEL &&	(std::abs(iCultureRateTimes100*iScale) >= 100 || bCityCulture))
	{
		for (int iDX = -iCultureRange; iDX <= iCultureRange; iDX++)
		{
			for (int iDY = -iCultureRange; iDY <= iCultureRange; iDY++)
			{
				int iDistance = cultureDistance(iDX, iDY);

				if (iDistance <= iCultureRange)
				{
					CvPlot* pLoopPlot = plotXY(getX_INLINE(), getY_INLINE(), iDX, iDY);

					if (pLoopPlot != NULL)
					{
						if (pLoopPlot->isPotentialCityWorkForArea(area()))
						{
							/* int iCultureToAdd =
								(iInnerFactor * iCultureRange - iDistance * (iInnerFactor - iOuterFactor))
								* iCultureRateTimes100 / (iCultureRange * 100); */
							//int iCultureToAdd = (int)(iScale*iCultureRateTimes100*exp(-iB*iDistance)/100);
							int iCultureToAdd =
								iCultureRateTimes100*((iScale-1)*(iDistance-iCultureRange)*(iDistance-iCultureRange) + iCultureRange*iCultureRange)/(100*iCultureRange*iCultureRange);

							pLoopPlot->changeCulture(ePlayer, iCultureToAdd, (bUpdate || !(pLoopPlot->isOwned())));
						}
					}
				}
			}
		}
	}
/*
** K-Mod end
*/
}

bool CvCity::doCheckProduction()
{
	CLLNode<OrderData>* pOrderNode;
	OrderData* pOrder;
	UnitTypes eUpgradeUnit;
	int iUpgradeProduction;
	int iProductionGold;
	CvWString szBuffer;
	int iI;
	bool bOK = true;

	for (iI = 0; iI < GC.getNumUnitInfos(); iI++)
	{
		if (getUnitProduction((UnitTypes)iI) > 0)
		{
			if (GET_PLAYER(getOwnerINLINE()).isProductionMaxedUnitClass((UnitClassTypes)(GC.getUnitInfo((UnitTypes)iI).getUnitClassType())))
			{
				iProductionGold = ((getUnitProduction((UnitTypes)iI) * GC.getDefineINT("MAXED_UNIT_GOLD_PERCENT")) / 100);

				if (iProductionGold > 0)
				{
					GET_PLAYER(getOwnerINLINE()).changeGold(iProductionGold);

					szBuffer = gDLL->getText("TXT_KEY_MISC_LOST_WONDER_PROD_CONVERTED", getNameKey(), GC.getUnitInfo((UnitTypes)iI).getTextKeyWide(), iProductionGold);
					gDLL->getInterfaceIFace()->addMessage(getOwnerINLINE(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_WONDERGOLD", MESSAGE_TYPE_MINOR_EVENT, GC.getCommerceInfo(COMMERCE_GOLD).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_RED"), getX_INLINE(), getY_INLINE(), true, true);
				}

				setUnitProduction(((UnitTypes)iI), 0);
			}
		}
	}

	for (iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		if (getBuildingProduction((BuildingTypes)iI) > 0)
		{
			if (GET_PLAYER(getOwnerINLINE()).isProductionMaxedBuildingClass((BuildingClassTypes)(GC.getBuildingInfo((BuildingTypes)iI).getBuildingClassType())))
			{
				iProductionGold = ((getBuildingProduction((BuildingTypes)iI) * GC.getDefineINT("MAXED_BUILDING_GOLD_PERCENT")) / 100);

				if (iProductionGold > 0)
				{
					GET_PLAYER(getOwnerINLINE()).changeGold(iProductionGold);

					szBuffer = gDLL->getText("TXT_KEY_MISC_LOST_WONDER_PROD_CONVERTED", getNameKey(), GC.getBuildingInfo((BuildingTypes)iI).getTextKeyWide(), iProductionGold);
					gDLL->getInterfaceIFace()->addMessage(getOwnerINLINE(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_WONDERGOLD", MESSAGE_TYPE_MINOR_EVENT, GC.getCommerceInfo(COMMERCE_GOLD).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_RED"), getX_INLINE(), getY_INLINE(), true, true);
				}

				setBuildingProduction(((BuildingTypes)iI), 0);
			}
		}
	}

	for (iI = 0; iI < GC.getNumProjectInfos(); iI++)
	{
		if (getProjectProduction((ProjectTypes)iI) > 0)
		{
			if (GET_PLAYER(getOwnerINLINE()).isProductionMaxedProject((ProjectTypes)iI))
			{
				iProductionGold = ((getProjectProduction((ProjectTypes)iI) * GC.getDefineINT("MAXED_PROJECT_GOLD_PERCENT")) / 100);

				if (iProductionGold > 0)
				{
					GET_PLAYER(getOwnerINLINE()).changeGold(iProductionGold);

					szBuffer = gDLL->getText("TXT_KEY_MISC_LOST_WONDER_PROD_CONVERTED", getNameKey(), GC.getProjectInfo((ProjectTypes)iI).getTextKeyWide(), iProductionGold);
					gDLL->getInterfaceIFace()->addMessage(getOwnerINLINE(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_WONDERGOLD", MESSAGE_TYPE_MINOR_EVENT, GC.getCommerceInfo(COMMERCE_GOLD).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_RED"), getX_INLINE(), getY_INLINE(), true, true);
				}

				setProjectProduction(((ProjectTypes)iI), 0);
			}
		}
	}

	if (!isProduction() && !isDisorder() && isHuman() && !isProductionAutomated())
	{
		chooseProduction();
		return bOK;
	}

	for (iI = 0; iI < GC.getNumUnitInfos(); iI++)
	{
		if (getFirstUnitOrder((UnitTypes)iI) != -1)
		{
			eUpgradeUnit = allUpgradesAvailable((UnitTypes)iI);

			if (eUpgradeUnit != NO_UNIT)
			{
				FAssertMsg(eUpgradeUnit != iI, "eUpgradeUnit is expected to be different from iI");
				iUpgradeProduction = getUnitProduction((UnitTypes)iI);
				setUnitProduction(((UnitTypes)iI), 0);
				setUnitProduction(eUpgradeUnit, iUpgradeProduction);

				pOrderNode = headOrderQueueNode();

				while (pOrderNode != NULL)
				{
					if (pOrderNode->m_data.eOrderType == ORDER_TRAIN)
					{
						if (pOrderNode->m_data.iData1 == iI)
						{
							GET_PLAYER(getOwnerINLINE()).changeUnitClassMaking(((UnitClassTypes)(GC.getUnitInfo((UnitTypes)(pOrderNode->m_data.iData1)).getUnitClassType())), -1);
							pOrderNode->m_data.iData1 = eUpgradeUnit;
							if (GET_PLAYER(getOwnerINLINE()).AI_unitValue(eUpgradeUnit, ((UnitAITypes)(pOrderNode->m_data.iData2)), area()) == 0)
							{
								area()->changeNumTrainAIUnits(getOwnerINLINE(), ((UnitAITypes)(pOrderNode->m_data.iData2)), -1);
								GET_PLAYER(getOwnerINLINE()).AI_changeNumTrainAIUnits(((UnitAITypes)(pOrderNode->m_data.iData2)), -1);
								pOrderNode->m_data.iData2 = GC.getUnitInfo(eUpgradeUnit).getDefaultUnitAIType();
								area()->changeNumTrainAIUnits(getOwnerINLINE(), ((UnitAITypes)(pOrderNode->m_data.iData2)), 1);
								GET_PLAYER(getOwnerINLINE()).AI_changeNumTrainAIUnits(((UnitAITypes)(pOrderNode->m_data.iData2)), 1);
							}
							GET_PLAYER(getOwnerINLINE()).changeUnitClassMaking(((UnitClassTypes)(GC.getUnitInfo((UnitTypes)(pOrderNode->m_data.iData1)).getUnitClassType())), 1);
						}
					}

					pOrderNode = nextOrderQueueNode(pOrderNode);
				}
			}
		}
	}

	for (iI = (getOrderQueueLength() - 1); iI >= 0; iI--)
	{
		pOrder = getOrderFromQueue(iI);

		if (pOrder != NULL)
		{
			if (!canContinueProduction(*pOrder))
			{
				popOrder(iI, false, true);
				bOK = false;
			}
		}
	}

	return bOK;
}


void CvCity::doProduction(bool bAllowNoProduction)
{
	//Rhye - start
//Speed: Modified by Kael 04/19/2007
//	CyCity* pyCity = new CyCity(this);
//	CyArgsList argsList;
//	argsList.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
//	long lResult=0;
//	gDLL->getPythonIFace()->callFunction(PYGameModule, "doProduction", argsList.makeFunctionArgs(), &lResult);
//	delete pyCity;	// python fxn must not hold on to this pointer
//	if (lResult == 1)
//	{
//		return;
//	}
//Speed: End Modify
	//Rhye - end

	if (!isHuman() || isProductionAutomated())
	{
		if (!isProduction() || isProductionProcess() || AI_isChooseProductionDirty())
		{
			AI_chooseProduction();
		}
	}

	if (!bAllowNoProduction && !isProduction())
	{
		return;
	}

	if (isProductionProcess())
	{
/************************************************************************************************/
/* UNOFFICIAL_PATCH                       12/07/09                         denev & jdog5000     */
/*                                                                                              */
/* Bugfix, Odd behavior                                                                         */
/************************************************************************************************/
		if (m_bPopProductionProcess)
		{
			popOrder(0, false, true);
			m_bPopProductionProcess = false;
		}
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/
		return;
	}

	if (isDisorder())
	{
		return;
	}

	if (isProduction())
	{
		changeProduction(getCurrentProductionDifference(false, true));
		setOverflowProduction(0);
		setFeatureProduction(0);

		if (getProduction() >= getProductionNeeded())
		{
			popOrder(0, true, true);
		}
	}
	else
	{
		changeOverflowProduction(getCurrentProductionDifference(false, false), getProductionModifier());
	}
}


void CvCity::doDecay()
{
	int iI;

	for (iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		BuildingTypes eBuilding = (BuildingTypes) iI;
		if (getProductionBuilding() != eBuilding)
		{
			if (getBuildingProduction(eBuilding) > 0)
			{
				changeBuildingProductionTime(eBuilding, 1);

				if (isHuman())
				{
					int iGameSpeedPercent = GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getConstructPercent();
					if (100 * getBuildingProductionTime(eBuilding) > GC.getDefineINT("BUILDING_PRODUCTION_DECAY_TIME") * iGameSpeedPercent)
					{
						int iProduction = getBuildingProduction(eBuilding);
						setBuildingProduction(eBuilding, iProduction - (iProduction * (100 - GC.getDefineINT("BUILDING_PRODUCTION_DECAY_PERCENT")) + iGameSpeedPercent - 1) / iGameSpeedPercent);
					}
				}
			}
			else
			{
				setBuildingProductionTime(eBuilding, 0);
			}
		}
	}

	for (iI = 0; iI < GC.getNumUnitInfos(); iI++)
	{
		UnitTypes eUnit = (UnitTypes) iI;
		if (getProductionUnit() != eUnit)
		{
			if (getUnitProduction(eUnit) > 0)
			{
				changeUnitProductionTime(eUnit, 1);

				if (isHuman())
				{
					int iGameSpeedPercent = GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getTrainPercent();
					if (100 * getUnitProductionTime(eUnit) > GC.getDefineINT("UNIT_PRODUCTION_DECAY_TIME") * iGameSpeedPercent)
					{
						int iProduction = getUnitProduction(eUnit);
						setUnitProduction(eUnit, iProduction - (iProduction * (100 - GC.getDefineINT("UNIT_PRODUCTION_DECAY_PERCENT")) + iGameSpeedPercent - 1) / iGameSpeedPercent);
					}
				}
			}
			else
			{
				setUnitProductionTime(eUnit, 0);
			}
		}
	}
}

bool CvCity::canSpread(ReligionTypes eReligion, bool bMissionary) const
{
	if (isHasReligion(eReligion)) return false;

	if (!bMissionary && !plot()->canSpread(eReligion)) return false;

	ReligionSpreadTypes eSpread = GET_PLAYER(getOwner()).getSpreadType(plot(), eReligion);

	if (eSpread == RELIGION_SPREAD_NONE) return false;

	if (!bMissionary && eSpread == RELIGION_SPREAD_MINORITY && getReligionCount() == 0) return false;

	return true;
}

int CvCity::getTurnsToSpread(ReligionTypes eReligion) const
{
	bool bDistant = GET_PLAYER(getOwner()).isDistantSpread(this, eReligion);
	ReligionSpreadTypes eSpread = GET_PLAYER(getOwner()).getSpreadType(plot(), eReligion, bDistant);
	ReligionTypes eStateReligion = GET_PLAYER(getOwner()).getStateReligion();
	int iIncrement = 50;
	
	if (eStateReligion != eReligion && eStateReligion != NO_RELIGION && eSpread != RELIGION_SPREAD_FAST) iIncrement += 20;

	if (eSpread == RELIGION_SPREAD_FAST)
	{
		iIncrement -= 10;

		if (getReligionCount() == 0)
		{
			iIncrement -= 10;
		}
	}

	int iCurrentTurn = GC.getGame().getGameTurn();
	int iFoundingTurn = GC.getGame().getReligionGameTurnFounded(eReligion);

	if (iCurrentTurn - iFoundingTurn <= getTurns(GC.getDefineINT("RELIGION_FOUNDING_SPREAD_TURNS"))) iIncrement -= 10;

	int iTurns = iIncrement;
	int iI;

	ReligionTypes eLoopReligion;
	for (iI = 0; iI < NUM_RELIGIONS; iI++)
	{
		eLoopReligion = (ReligionTypes)iI;
		if (isHasReligion(eLoopReligion) && !GET_PLAYER(getOwner()).isTolerating(eLoopReligion))
		{
			iTurns += iIncrement;
		}
	}

	if (eStateReligion == eReligion && isHasPrecursor(eReligion)) iTurns -= iIncrement / 2;

	if (eSpread == RELIGION_SPREAD_MINORITY) iTurns *= 2;

	if (getOwner() == CONGO)
	{
		log(CvWString::format(L"Congo: eSpread: %d, iIncrement: %d, iTurns: %d", eSpread, iIncrement, iTurns));
	}

	return getTurns(iTurns);
}

bool CvCity::isHasPrecursor(ReligionTypes eReligion) const
{
	if (eReligion == CONFUCIANISM) return isHasReligion(TAOISM);
	if (eReligion == TAOISM) return isHasReligion(CONFUCIANISM);
	if (eReligion == BUDDHISM) return isHasReligion(HINDUISM);

	if (eReligion == ISLAM) return isHasReligion(CATHOLICISM) || isHasReligion(ORTHODOXY);

	if (eReligion == CATHOLICISM || eReligion == ORTHODOXY) return isHasReligion(JUDAISM);
}

int CvCity::getReligionPopulation(ReligionTypes eReligion) const
{
	if (!isHasReligion(eReligion)) return 0;

	if (getReligionCount() == 1) return getPopulation();

	ReligionTypes eStateReligion = GET_PLAYER(getOwner()).getStateReligion();

	if (eStateReligion == eReligion) return getPopulation() / 2 + getPopulation() / (2 * getReligionCount());

	if (eStateReligion == NO_RELIGION) return getPopulation() / getReligionCount();

	return getPopulation() / (2 * getReligionCount());
}

void CvCity::doReligion()
{
	int iI;
	ReligionTypes eReligion, eDisappearingReligion;
	int iReligionInfluence;
	int iChance, iRand;

	for (iI = 0; iI < NUM_RELIGIONS; iI++)
	{
		eReligion = (ReligionTypes)iI;

		if (!canSpread(eReligion) && !(GET_PLAYER(getOwner()).isDistantSpread(this, eReligion))) continue;

		iReligionInfluence = plot()->getReligionInfluence(eReligion);
		iChance = getTurnsToSpread(eReligion);
		iRand = GC.getGameINLINE().getSorenRandNum(iChance, "Religion spread");
		log(CvWString::format(L"Spread religion %s in %s: 1/%d chance", GC.getReligionInfo(eReligion).getText(), getName().GetCString(), iChance));
		
		if (iRand == 0)
		{
			spreadReligion(eReligion);
			return;
		}
	}

	eDisappearingReligion = disappearingReligion();

	if (eDisappearingReligion != NO_RELIGION && !GET_PLAYER(getOwner()).isDistantSpread(this, eDisappearingReligion))
	{
		iChance = GET_PLAYER(getOwner()).getSpreadType(plot(), eDisappearingReligion) * 25 + 25;
		iRand = GC.getGame().getSorenRandNum(iChance, "Religion disappearance");
		log(CvWString::format(L"Disappearing religion %s in %s: 1/%d chance", GC.getReligionInfo(eDisappearingReligion).getText(), getName().GetCString(), iChance));

		if (iRand == 0)
		{
			removeReligion(eReligion);
		}
	}
	
	/*CvCity* pLoopCity;
	ReligionTypes eReligion;
	PlayerTypes ePlayer;
	bool bStateReligion;
	bool bDistanceReduction;
	int iRandThreshold;
	int iSpread, iSpreadFactor, iRegionFactor;
	int iLoop;
	int iI, iJ;

	int iReligionCount = getReligionCount();
	bool bNoStateReligion = !GET_PLAYER(getOwnerINLINE()).isStateReligion();

	int iReligionDistanceDivisor = GC.getDefineINT("RELIGION_SPREAD_DISTANCE_DIVISOR");
	int iMaxDistance = GC.getMapINLINE().maxPlotDistance();

	int iReligionSpreadRand = GC.getDefineINT("RELIGION_SPREAD_RAND");

	/*for (iI = 0; iI < GC.getNumReligionInfos(); iI++)
	{
		eReligion = (ReligionTypes)iI;

		// Leoreth: prevent Zoroastrianism spread after 1000 AD
		if (eReligion == ZOROASTRIANISM && GC.getGame().getGameTurnYear() >= 1000) continue;

		if (!isHasReligion(eReligion))
		{
			bStateReligion = (GET_PLAYER(getOwnerINLINE()).getStateReligion() == iI);
			iRegionFactor = getRegionSpreadFactor(getRegionID(), eReligion);

			if (!bStateReligion)
			{
				if (GET_PLAYER(getOwnerINLINE()).isNoNonStateReligionSpread()) continue;
				if (iRegionFactor < 0) continue;
				if (iRegionFactor == 0 && iReligionCount == 0) continue;
			}

			iRandThreshold = 0;

			for (iJ = 0; iJ < MAX_PLAYERS; iJ++)
			{
				ePlayer = (PlayerTypes)iJ;

				if (GET_PLAYER(ePlayer).isAlive())
				{
					for (pLoopCity = GET_PLAYER(ePlayer).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER(ePlayer).nextCity(&iLoop))
					{
						if (pLoopCity->isConnectedTo(this))
						{
							iSpread = pLoopCity->getReligionInfluence(eReligion);

							iSpreadFactor = getSpreadFactor(eReligion) * GC.getReligionInfo(eReligion).getSpreadFactor() / 100;
							iSpread *= iSpreadFactor;

							if (iSpread > 0)
							{
								bDistanceReduction = true;

								//if ((bStateReligion || bNoStateReligion) && iRegionFactor == 2) bDistanceReduction = false;
								if (eReligion == CATHOLICISM && getOwnerINLINE() == CONGO && GET_PLAYER(getOwnerINLINE()).getStateReligion() == NO_RELIGION) bDistanceReduction = false;

								if (bStateReligion && iRegionFactor > 0) iSpread *= 2;

								if (bDistanceReduction)
								{
									iSpread /= std::max(1, ((iReligionDistanceDivisor * plotDistance(getX_INLINE(), getY_INLINE(), pLoopCity->getX_INLINE(), pLoopCity->getY_INLINE())) / iMaxDistance) - 5);
								}

								iSpread /= (iReligionCount + 1);

								iRandThreshold = std::max(iRandThreshold, iSpread);
							}
						}
					}
				}
			
				if (GC.getGameINLINE().getSorenRandNum(iReligionSpreadRand, "Religion Spread") < iRandThreshold)
				{
					setHasReligion(eReligion, true, true, true);
					break;
				}
			}
		}
	}*/

	/*if (getReligionCount() == 0)
	{
		for (iI = 0; iI < GC.getNumReligionInfos(); iI++)
		{
			if (!isHasReligion((ReligionTypes)iI))
			{
				if ((iI == GET_PLAYER(getOwnerINLINE()).getStateReligion()) || !(GET_PLAYER(getOwnerINLINE()).isNoNonStateReligionSpread()))
				{
					iRandThreshold = 0;

					for (iJ = 0; iJ < MAX_PLAYERS; iJ++)
					{
						if (GET_PLAYER((PlayerTypes)iJ).isAlive())
						{
							for (pLoopCity = GET_PLAYER((PlayerTypes)iJ).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER((PlayerTypes)iJ).nextCity(&iLoop))
							{
								if (pLoopCity->isConnectedTo(this))
								{
									iSpread = pLoopCity->getReligionInfluence((ReligionTypes)iI);

									//Rhye - start
									//iSpread *= GC.getReligionInfo((ReligionTypes)iI).getSpreadFactor();
									int iBaseSpreadFactor = GC.getReligionInfo((ReligionTypes)iI).getSpreadFactor();
									int iSpreadFactor = GET_PLAYER(getOwnerINLINE()).getSpreadFactor((ReligionTypes)iI) * iBaseSpreadFactor / 100;

									iSpread *= iSpreadFactor;

									//Leoreth: prohibit Zoroastrianism from spreading again
									if (iI == ZOROASTRIANISM && GC.getGame().getGameTurnYear() >= 1000)
										iSpread = 0;

                                    //Leoreth: disabled, but do something to get rid of Christianity in Anatolia when Byzantium collapses
									//if (!GET_PLAYER((PlayerTypes)EGYPT).isPlayable()) //late start condition
									//	if (iI == 1 && getOwnerINLINE() == CELTIA) //no spread of Christianity in the Byzantine empire, because otherwise the Turks will get it
									//		iSpread = 0;
									//Rhye - end

									if (iSpread > 0)
									{
										bool bDistanceReduction = true;

										//Leoreth: allow Congo to get Catholicism for the UHV
										if (getOwnerINLINE() == CONGO && iI == CATHOLICISM && GET_PLAYER((PlayerTypes)CONGO).getStateReligion() != CATHOLICISM)
											bDistanceReduction = false;

										//Leoreth: Christianity spreads easier to the New World
										if (iI == CATHOLICISM || iI == PROTESTANTISM)
										{
											if (GET_PLAYER(getOwnerINLINE()).getStateReligion() == NO_RELIGION || GET_PLAYER(getOwnerINLINE()).getStateReligion() == CATHOLICISM || GET_PLAYER(getOwnerINLINE()).getStateReligion() == PROTESTANTISM)
											{
												if (getRegionID() == REGION_CANADA || getRegionID() == REGION_ALASKA || getRegionID() == REGION_UNITED_STATES || getRegionID() == REGION_CARIBBEAN || getRegionID() == REGION_MESOAMERICA || getRegionID() == REGION_BRAZIL || getRegionID() == REGION_ARGENTINA || getRegionID() == REGION_PERU || getRegionID() == REGION_COLOMBIA || getRegionID() == REGION_SOUTH_AFRICA || getRegionID() == REGION_AUSTRALIA)
												{
													bDistanceReduction = false;
												}
											}
										}

										// same for Orthodoxy in Siberia
										if (iI == ORTHODOXY)
										{
											if (getRegionID() == REGION_SIBERIA)
											{
												bDistanceReduction = false;
											}
										}

										if (bDistanceReduction)
											iSpread /= std::max(1, (((GC.getDefineINT("RELIGION_SPREAD_DISTANCE_DIVISOR") * plotDistance(getX_INLINE(), getY_INLINE(), pLoopCity->getX_INLINE(), pLoopCity->getY_INLINE())) / GC.getMapINLINE().maxPlotDistance()) - 5));
										
										//iSpread /= (getReligionCount() + 1);

										iRandThreshold = std::max(iRandThreshold, iSpread);
									}
								}
							}
						}
					}

					if (GC.getGameINLINE().getSorenRandNum(GC.getDefineINT("RELIGION_SPREAD_RAND"), "Religion Spread") < iRandThreshold)
					{
						setHasReligion(((ReligionTypes)iI), true, true, true);
						break;
					}
				}
			}
		}
	}*/
}


void CvCity::doGreatPeople()
{
	//Rhye - start
//Speed: Modified by Kael 04/19/2007
//	CyCity* pyCity = new CyCity(this);
//	CyArgsList argsList;
//	argsList.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
//	long lResult=0;
//	gDLL->getPythonIFace()->callFunction(PYGameModule, "doGreatPeople", argsList.makeFunctionArgs(), &lResult);
//	delete pyCity;	// python fxn must not hold on to this pointer
//	if (lResult == 1)
//	{
//		return;
//	}
//Speed: End Modify
	//Rhye - end

	if (isDisorder())
	{
		return;
	}

	changeGreatPeopleProgress(getGreatPeopleRate());

	for (int iI = 0; iI < GC.getNumUnitInfos(); iI++)
	{
		changeGreatPeopleUnitProgress(((UnitTypes)iI), getGreatPeopleUnitRate((UnitTypes)iI));
	}

	if (getGreatPeopleProgress() >= GET_PLAYER(getOwnerINLINE()).greatPeopleThreshold(false))
	{
		int iTotalGreatPeopleUnitProgress = 0;
		for (int iI = 0; iI < GC.getNumUnitInfos(); iI++)
		{
			iTotalGreatPeopleUnitProgress += getGreatPeopleUnitProgress((UnitTypes)iI);
		}

		int iGreatPeopleUnitRand = GC.getGameINLINE().getSorenRandNum(iTotalGreatPeopleUnitProgress, "Great Person");

		UnitTypes eGreatPeopleUnit = NO_UNIT;
		for (int iI = 0; iI < GC.getNumUnitInfos(); iI++)
		{
			if (iGreatPeopleUnitRand < getGreatPeopleUnitProgress((UnitTypes)iI))
			{
				eGreatPeopleUnit = ((UnitTypes)iI);
				break;
			}
			else
			{
				iGreatPeopleUnitRand -= getGreatPeopleUnitProgress((UnitTypes)iI);
			}
		}

		if (eGreatPeopleUnit != NO_UNIT)
		{
			changeGreatPeopleProgress(-(GET_PLAYER(getOwnerINLINE()).greatPeopleThreshold(false)));

			for (int iI = 0; iI < GC.getNumUnitInfos(); iI++)
			{
				setGreatPeopleUnitProgress(((UnitTypes)iI), 0);
			}

			createGreatPeople(eGreatPeopleUnit, true, false);
		}
	}
}


void CvCity::doMeltdown()
{
	CvWString szBuffer;
	int iI;

/*************************************************************************************************/
/**	SPEEDTWEAK (Block Python) Sephi                                               	            **/
/**	If you want to allow modmodders to enable this Callback, see CvCity::cancreate for example  **/
/*************************************************************************************************/
/**
	CyCity* pyCity = new CyCity(this);
	CyArgsList argsList;
	argsList.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
	long lResult=0;
	gDLL->getPythonIFace()->callFunction(PYGameModule, "doMeltdown", argsList.makeFunctionArgs(), &lResult);
	delete pyCity;	// python fxn must not hold on to this pointer
	if (lResult == 1)
	{
		return;
	}
/*************************************************************************************************/
/**	END	                                        												**/
/*************************************************************************************************/

	for (iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		if (getNumBuilding((BuildingTypes)iI) > 0)
		{
			if (GC.getBuildingInfo((BuildingTypes)iI).getNukeExplosionRand() != 0)
			{
				if (GC.getGameINLINE().getSorenRandNum(GC.getBuildingInfo((BuildingTypes)iI).getNukeExplosionRand(), "Meltdown!!!") == 0)
				{
					if (getNumRealBuilding((BuildingTypes)iI) > 0)
					{
						setNumRealBuilding(((BuildingTypes)iI), 0);
					}

					plot()->nukeExplosion(1);

					szBuffer = gDLL->getText("TXT_KEY_MISC_MELTDOWN_CITY", getNameKey());
					gDLL->getInterfaceIFace()->addMessage(getOwnerINLINE(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_MELTDOWN", MESSAGE_TYPE_MINOR_EVENT, ARTFILEMGR.getInterfaceArtInfo("INTERFACE_UNHEALTHY_PERSON")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_RED"), getX_INLINE(), getY_INLINE(), true, true);

					break;
				}
			}
		}
	}
}

// Private Functions...

void CvCity::read(FDataStreamBase* pStream)
{
	int iI;
	int iNumElts;

	// Init data before load
	reset();

	uint uiFlag=0;
	pStream->Read(&uiFlag);	// flags for expansion

	pStream->Read(&m_iID);
	pStream->Read(&m_iX);
	pStream->Read(&m_iY);
	pStream->Read(&m_iRallyX);
	pStream->Read(&m_iRallyY);
	pStream->Read(&m_iGameTurnFounded);
	pStream->Read(&m_iGameTurnAcquired);
	pStream->Read(&m_iPopulation);
	pStream->Read(&m_iHighestPopulation);
	pStream->Read(&m_iWorkingPopulation);
	pStream->Read(&m_iSpecialistPopulation);
	pStream->Read(&m_iNumGreatPeople);
	pStream->Read(&m_iBaseGreatPeopleRate);
	pStream->Read(&m_iGreatPeopleRateModifier);
	pStream->Read(&m_iGreatPeopleProgress);
	pStream->Read(&m_iNumWorldWonders);
	pStream->Read(&m_iNumTeamWonders);
	pStream->Read(&m_iNumNationalWonders);
	pStream->Read(&m_iNumBuildings);
	pStream->Read(&m_iGovernmentCenterCount);
	pStream->Read(&m_iMaintenance);
	pStream->Read(&m_iMaintenanceModifier);
	pStream->Read(&m_iWarWearinessModifier);
	pStream->Read(&m_iHurryAngerModifier);
	pStream->Read(&m_iHealRate);
	pStream->Read(&m_iEspionageHealthCounter);
	pStream->Read(&m_iEspionageHappinessCounter);
	pStream->Read(&m_iFreshWaterGoodHealth);
	pStream->Read(&m_iFreshWaterBadHealth);
	pStream->Read(&m_iFeatureGoodHealth);
	pStream->Read(&m_iFeatureBadHealth);
	pStream->Read(&m_iBuildingGoodHealth);
	pStream->Read(&m_iBuildingBadHealth);
	pStream->Read(&m_iPowerGoodHealth);
	pStream->Read(&m_iPowerBadHealth);
	pStream->Read(&m_iBonusGoodHealth);
	pStream->Read(&m_iBonusBadHealth);
	pStream->Read(&m_iHurryAngerTimer);
	pStream->Read(&m_iConscriptAngerTimer);
	pStream->Read(&m_iDefyResolutionAngerTimer);
	pStream->Read(&m_iHappinessTimer);
	pStream->Read(&m_iMilitaryHappinessUnits);
	pStream->Read(&m_iBuildingGoodHappiness);
	pStream->Read(&m_iBuildingBadHappiness);
	pStream->Read(&m_iExtraBuildingGoodHappiness);
	pStream->Read(&m_iExtraBuildingBadHappiness);
	pStream->Read(&m_iExtraBuildingGoodHealth);
	pStream->Read(&m_iExtraBuildingBadHealth);
	pStream->Read(&m_iFeatureGoodHappiness);
	pStream->Read(&m_iFeatureBadHappiness);
	pStream->Read(&m_iBonusGoodHappiness);
	pStream->Read(&m_iBonusBadHappiness);
	pStream->Read(&m_iReligionGoodHappiness);
	pStream->Read(&m_iReligionBadHappiness);
	pStream->Read(&m_iExtraHappiness);
	pStream->Read(&m_iExtraHealth);
	pStream->Read(&m_iNoUnhappinessCount);
	pStream->Read(&m_iNoUnhealthyPopulationCount);
	pStream->Read(&m_iBuildingOnlyHealthyCount);
	pStream->Read(&m_iFood);
	pStream->Read(&m_iFoodKept);
	pStream->Read(&m_iMaxFoodKeptPercent);
	pStream->Read(&m_iOverflowProduction);
	pStream->Read(&m_iFeatureProduction);
	pStream->Read(&m_iMilitaryProductionModifier);
	pStream->Read(&m_iSpaceProductionModifier);
	pStream->Read(&m_iExtraTradeRoutes);
	pStream->Read(&m_iTradeRouteModifier);
	pStream->Read(&m_iForeignTradeRouteModifier);
	pStream->Read(&m_iBuildingDefense);
	pStream->Read(&m_iBuildingBombardDefense);
	pStream->Read(&m_iFreeExperience);
	pStream->Read(&m_iCurrAirlift);
	pStream->Read(&m_iMaxAirlift);
	pStream->Read(&m_iAirModifier);
	pStream->Read(&m_iAirUnitCapacity);
	pStream->Read(&m_iNukeModifier);
	pStream->Read(&m_iFreeSpecialist);
	pStream->Read(&m_iPowerCount);
	pStream->Read(&m_iDirtyPowerCount);
	pStream->Read(&m_iDefenseDamage);
	pStream->Read(&m_iLastDefenseDamage);
	pStream->Read(&m_iOccupationTimer);
	pStream->Read(&m_iCultureUpdateTimer);
	pStream->Read(&m_iCitySizeBoost);
	pStream->Read(&m_iSpecialistFreeExperience);
	pStream->Read(&m_iEspionageDefenseModifier);

	// Leoreth
	pStream->Read(&m_iSpecialistGoodHappiness);
	pStream->Read(&m_iSpecialistBadHappiness);
	pStream->Read(&m_iCorporationGoodHappiness);
	pStream->Read(&m_iCorporationBadHappiness);
	pStream->Read(&m_iCorporationHealth);
	pStream->Read(&m_iCorporationUnhealth);
	pStream->Read(&m_iNextCoveredPlot); // Leoreth

	pStream->Read(&m_bNeverLost);
	pStream->Read(&m_bBombarded);
	pStream->Read(&m_bDrafted);
	pStream->Read(&m_bAirliftTargeted);
	pStream->Read(&m_bWeLoveTheKingDay);
	pStream->Read(&m_bCitizensAutomated);
	pStream->Read(&m_bProductionAutomated);
	pStream->Read(&m_bWallOverride);
	// m_bInfoDirty not saved...
	// m_bLayoutDirty not saved...
	pStream->Read(&m_bPlundered);
	pStream->Read(&m_bMongolUP); // Leoreth

	pStream->Read((int*)&m_eOwner);
	pStream->Read((int*)&m_ePreviousOwner);
	pStream->Read((int*)&m_eOriginalOwner);
	pStream->Read((int*)&m_eCultureLevel);
	pStream->Read((int*)&m_eArtStyle); // Leoreth

	pStream->Read(NUM_YIELD_TYPES, m_aiSeaPlotYield);
	pStream->Read(NUM_YIELD_TYPES, m_aiRiverPlotYield);
	pStream->Read(NUM_YIELD_TYPES, m_aiBaseYieldRate);
	pStream->Read(NUM_YIELD_TYPES, m_aiYieldRateModifier);
	pStream->Read(NUM_YIELD_TYPES, m_aiPowerYieldRateModifier);
	pStream->Read(NUM_YIELD_TYPES, m_aiBonusYieldRateModifier);
	pStream->Read(NUM_YIELD_TYPES, m_aiTradeYield);
	pStream->Read(NUM_YIELD_TYPES, m_aiCorporationYield);
	pStream->Read(NUM_YIELD_TYPES, m_aiExtraSpecialistYield);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiCommerceRate);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiProductionToCommerceModifier);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiBuildingCommerce);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiSpecialistCommerce);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiReligionCommerce);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiCorporationCommerce);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiCommerceRateModifier);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiBonusCommerceRateModifier); // Leoreth
	pStream->Read(NUM_COMMERCE_TYPES, m_aiCommerceHappinessPer);
	pStream->Read(NUM_DOMAIN_TYPES, m_aiDomainFreeExperience);
	pStream->Read(NUM_DOMAIN_TYPES, m_aiDomainProductionModifier);
	pStream->Read(MAX_PLAYERS, m_aiCulture);
	pStream->Read(MAX_PLAYERS, m_aiNumRevolts);
	pStream->Read(MAX_PLAYERS, m_aiGameTurnPlayerLost); // Leoreth

	pStream->Read(MAX_PLAYERS, m_abEverOwned);
	pStream->Read(MAX_PLAYERS, m_abTradeRoute);
	pStream->Read(MAX_TEAMS, m_abRevealed);
	pStream->Read(MAX_TEAMS, m_abEspionageVisibility);

	pStream->Read(NUM_CITY_PLOTS_3, m_aiCulturePlots); // Leoreth
	pStream->Read(NUM_CITY_PLOTS_3, m_aiCultureCosts); // Leoreth

	pStream->ReadString(m_szName);
	pStream->ReadString(m_szScriptData);

	pStream->Read(GC.getNumBonusInfos(), m_paiNoBonus);
	pStream->Read(GC.getNumBonusInfos(), m_paiFreeBonus);
	pStream->Read(GC.getNumBonusInfos(), m_paiNumBonuses);
	pStream->Read(GC.getNumBonusInfos(), m_paiNumCorpProducedBonuses);
	pStream->Read(GC.getNumProjectInfos(), m_paiProjectProduction);
	pStream->Read(GC.getNumBuildingInfos(), m_paiBuildingProduction);
	pStream->Read(GC.getNumBuildingInfos(), m_paiBuildingProductionTime);
	pStream->Read(GC.getNumBuildingInfos(), m_paiBuildingOriginalOwner);
	pStream->Read(GC.getNumBuildingInfos(), m_paiBuildingOriginalTime);
	pStream->Read(GC.getNumUnitInfos(), m_paiUnitProduction);
	pStream->Read(GC.getNumUnitInfos(), m_paiUnitProductionTime);
	pStream->Read(GC.getNumUnitInfos(), m_paiGreatPeopleUnitRate);
	pStream->Read(GC.getNumUnitInfos(), m_paiGreatPeopleUnitProgress);
	pStream->Read(GC.getNumSpecialistInfos(), m_paiSpecialistCount);
	pStream->Read(GC.getNumSpecialistInfos(), m_paiMaxSpecialistCount);
	pStream->Read(GC.getNumSpecialistInfos(), m_paiForceSpecialistCount);
	pStream->Read(GC.getNumSpecialistInfos(), m_paiFreeSpecialistCount);
	pStream->Read(GC.getNumImprovementInfos(), m_paiImprovementFreeSpecialists);
	pStream->Read(GC.getNumReligionInfos(), m_paiReligionInfluence);
	pStream->Read(GC.getNumReligionInfos(), m_paiStateReligionHappiness);
	pStream->Read(GC.getNumUnitCombatInfos(), m_paiUnitCombatFreeExperience);
	pStream->Read(GC.getNumPromotionInfos(), m_paiFreePromotionCount);
	pStream->Read(GC.getNumBuildingInfos(), m_paiNumRealBuilding);
	pStream->Read(GC.getNumBuildingInfos(), m_paiNumFreeBuilding);

	pStream->Read(NUM_CITY_PLOTS, m_pabWorkingPlot);
	pStream->Read(GC.getNumReligionInfos(), m_pabHasReligion);
	pStream->Read(GC.getNumCorporationInfos(), m_pabHasCorporation);
	pStream->Read(GC.getNumUnitInfos(), m_pabIsUnitHurried); // Leoreth

	// Leoreth
	for (int i = 0; i < GC.getNumBonusInfos(); i++)
	{
		pStream->Read(NUM_YIELD_TYPES, m_ppaiBonusYield[i]);
	}

	for (iI=0;iI<GC.getDefineINT("MAX_TRADE_ROUTES");iI++)
	{
		pStream->Read((int*)&m_paTradeCities[iI].eOwner);
		pStream->Read(&m_paTradeCities[iI].iID);
	}

	m_orderQueue.Read(pStream);

	pStream->Read(&m_iPopulationRank);
	pStream->Read(&m_bPopulationRankValid);
	pStream->Read(NUM_YIELD_TYPES, m_aiBaseYieldRank);
	pStream->Read(NUM_YIELD_TYPES, m_abBaseYieldRankValid);
	pStream->Read(NUM_YIELD_TYPES, m_aiYieldRank);
	pStream->Read(NUM_YIELD_TYPES, m_abYieldRankValid);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiCommerceRank);
	pStream->Read(NUM_COMMERCE_TYPES, m_abCommerceRankValid);

	pStream->Read(&iNumElts);
	m_aEventsOccured.clear();
	for (int i = 0; i < iNumElts; ++i)
	{
		EventTypes eEvent;
		pStream->Read((int*)&eEvent);
		m_aEventsOccured.push_back(eEvent);
	}

	pStream->Read(&iNumElts);
	m_aBuildingYieldChange.clear();
	for (int i = 0; i < iNumElts; ++i)
	{
		BuildingYieldChange kChange;
		kChange.read(pStream);
		m_aBuildingYieldChange.push_back(kChange);
	}

	pStream->Read(&iNumElts);
	m_aBuildingCommerceChange.clear();
	for (int i = 0; i < iNumElts; ++i)
	{
		BuildingCommerceChange kChange;
		kChange.read(pStream);
		m_aBuildingCommerceChange.push_back(kChange);
	}

	pStream->Read(&iNumElts);
	m_aBuildingHappyChange.clear();
	for (int i = 0; i < iNumElts; ++i)
	{
		int iBuildingClass;
		pStream->Read(&iBuildingClass);
		int iChange;
		pStream->Read(&iChange);
		m_aBuildingHappyChange.push_back(std::make_pair((BuildingClassTypes)iBuildingClass, iChange));
	}

	pStream->Read(&iNumElts);
	m_aBuildingHealthChange.clear();
	for (int i = 0; i < iNumElts; ++i)
	{
		int iBuildingClass;
		pStream->Read(&iBuildingClass);
		int iChange;
		pStream->Read(&iChange);
		m_aBuildingHealthChange.push_back(std::make_pair((BuildingClassTypes)iBuildingClass, iChange));
	}
}

void CvCity::write(FDataStreamBase* pStream)
{
	int iI;

	uint uiFlag=0;
	pStream->Write(uiFlag);		// flag for expansion

	pStream->Write(m_iID);
	pStream->Write(m_iX);
	pStream->Write(m_iY);
	pStream->Write(m_iRallyX);
	pStream->Write(m_iRallyY);
	pStream->Write(m_iGameTurnFounded);
	pStream->Write(m_iGameTurnAcquired);
	pStream->Write(m_iPopulation);
	pStream->Write(m_iHighestPopulation);
	pStream->Write(m_iWorkingPopulation);
	pStream->Write(m_iSpecialistPopulation);
	pStream->Write(m_iNumGreatPeople);
	pStream->Write(m_iBaseGreatPeopleRate);
	pStream->Write(m_iGreatPeopleRateModifier);
	pStream->Write(m_iGreatPeopleProgress);
	pStream->Write(m_iNumWorldWonders);
	pStream->Write(m_iNumTeamWonders);
	pStream->Write(m_iNumNationalWonders);
	pStream->Write(m_iNumBuildings);
	pStream->Write(m_iGovernmentCenterCount);
	pStream->Write(m_iMaintenance);
	pStream->Write(m_iMaintenanceModifier);
	pStream->Write(m_iWarWearinessModifier);
	pStream->Write(m_iHurryAngerModifier);
	pStream->Write(m_iHealRate);
	pStream->Write(m_iEspionageHealthCounter);
	pStream->Write(m_iEspionageHappinessCounter);
	pStream->Write(m_iFreshWaterGoodHealth);
	pStream->Write(m_iFreshWaterBadHealth);
	pStream->Write(m_iFeatureGoodHealth);
	pStream->Write(m_iFeatureBadHealth);
	pStream->Write(m_iBuildingGoodHealth);
	pStream->Write(m_iBuildingBadHealth);
	pStream->Write(m_iPowerGoodHealth);
	pStream->Write(m_iPowerBadHealth);
	pStream->Write(m_iBonusGoodHealth);
	pStream->Write(m_iBonusBadHealth);
	pStream->Write(m_iHurryAngerTimer);
	pStream->Write(m_iConscriptAngerTimer);
	pStream->Write(m_iDefyResolutionAngerTimer);
	pStream->Write(m_iHappinessTimer);
	pStream->Write(m_iMilitaryHappinessUnits);
	pStream->Write(m_iBuildingGoodHappiness);
	pStream->Write(m_iBuildingBadHappiness);
	pStream->Write(m_iExtraBuildingGoodHappiness);
	pStream->Write(m_iExtraBuildingBadHappiness);
	pStream->Write(m_iExtraBuildingGoodHealth);
	pStream->Write(m_iExtraBuildingBadHealth);
	pStream->Write(m_iFeatureGoodHappiness);
	pStream->Write(m_iFeatureBadHappiness);
	pStream->Write(m_iBonusGoodHappiness);
	pStream->Write(m_iBonusBadHappiness);
	pStream->Write(m_iReligionGoodHappiness);
	pStream->Write(m_iReligionBadHappiness);
	pStream->Write(m_iExtraHappiness);
	pStream->Write(m_iExtraHealth);
	pStream->Write(m_iNoUnhappinessCount);
	pStream->Write(m_iNoUnhealthyPopulationCount);
	pStream->Write(m_iBuildingOnlyHealthyCount);
	pStream->Write(m_iFood);
	pStream->Write(m_iFoodKept);
	pStream->Write(m_iMaxFoodKeptPercent);
	pStream->Write(m_iOverflowProduction);
	pStream->Write(m_iFeatureProduction);
	pStream->Write(m_iMilitaryProductionModifier);
	pStream->Write(m_iSpaceProductionModifier);
	pStream->Write(m_iExtraTradeRoutes);
	pStream->Write(m_iTradeRouteModifier);
	pStream->Write(m_iForeignTradeRouteModifier);
	pStream->Write(m_iBuildingDefense);
	pStream->Write(m_iBuildingBombardDefense);
	pStream->Write(m_iFreeExperience);
	pStream->Write(m_iCurrAirlift);
	pStream->Write(m_iMaxAirlift);
	pStream->Write(m_iAirModifier);
	pStream->Write(m_iAirUnitCapacity);
	pStream->Write(m_iNukeModifier);
	pStream->Write(m_iFreeSpecialist);
	pStream->Write(m_iPowerCount);
	pStream->Write(m_iDirtyPowerCount);
	pStream->Write(m_iDefenseDamage);
	pStream->Write(m_iLastDefenseDamage);
	pStream->Write(m_iOccupationTimer);
	pStream->Write(m_iCultureUpdateTimer);
	pStream->Write(m_iCitySizeBoost);
	pStream->Write(m_iSpecialistFreeExperience);
	pStream->Write(m_iEspionageDefenseModifier);

	// Leoreth
	pStream->Write(m_iSpecialistGoodHappiness);
	pStream->Write(m_iSpecialistBadHappiness);
	pStream->Write(m_iCorporationGoodHappiness);
	pStream->Write(m_iCorporationBadHappiness);
	pStream->Write(m_iCorporationHealth);
	pStream->Write(m_iCorporationUnhealth);

	pStream->Write(m_iNextCoveredPlot);

	pStream->Write(m_bNeverLost);
	pStream->Write(m_bBombarded);
	pStream->Write(m_bDrafted);
	pStream->Write(m_bAirliftTargeted);
	pStream->Write(m_bWeLoveTheKingDay);
	pStream->Write(m_bCitizensAutomated);
	pStream->Write(m_bProductionAutomated);
	pStream->Write(m_bWallOverride);
	// m_bInfoDirty not saved...
	// m_bLayoutDirty not saved...
	pStream->Write(m_bPlundered);
	pStream->Write(m_bMongolUP); // Leoreth

	pStream->Write(m_eOwner);
	pStream->Write(m_ePreviousOwner);
	pStream->Write(m_eOriginalOwner);
	pStream->Write(m_eCultureLevel);
	pStream->Write(m_eArtStyle); // Leoreth

	pStream->Write(NUM_YIELD_TYPES, m_aiSeaPlotYield);
	pStream->Write(NUM_YIELD_TYPES, m_aiRiverPlotYield);
	pStream->Write(NUM_YIELD_TYPES, m_aiBaseYieldRate);
	pStream->Write(NUM_YIELD_TYPES, m_aiYieldRateModifier);
	pStream->Write(NUM_YIELD_TYPES, m_aiPowerYieldRateModifier);
	pStream->Write(NUM_YIELD_TYPES, m_aiBonusYieldRateModifier);
	pStream->Write(NUM_YIELD_TYPES, m_aiTradeYield);
	pStream->Write(NUM_YIELD_TYPES, m_aiCorporationYield);
	pStream->Write(NUM_YIELD_TYPES, m_aiExtraSpecialistYield);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiCommerceRate);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiProductionToCommerceModifier);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiBuildingCommerce);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiSpecialistCommerce);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiReligionCommerce);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiCorporationCommerce);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiCommerceRateModifier);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiBonusCommerceRateModifier); // Leoreth
	pStream->Write(NUM_COMMERCE_TYPES, m_aiCommerceHappinessPer);
	pStream->Write(NUM_DOMAIN_TYPES, m_aiDomainFreeExperience);
	pStream->Write(NUM_DOMAIN_TYPES, m_aiDomainProductionModifier);
	pStream->Write(MAX_PLAYERS, m_aiCulture);
	pStream->Write(MAX_PLAYERS, m_aiNumRevolts);
	pStream->Write(MAX_PLAYERS, m_aiGameTurnPlayerLost); // Leoreth

	pStream->Write(MAX_PLAYERS, m_abEverOwned);
	pStream->Write(MAX_PLAYERS, m_abTradeRoute);
	pStream->Write(MAX_TEAMS, m_abRevealed);
	pStream->Write(MAX_TEAMS, m_abEspionageVisibility);

	pStream->Write(NUM_CITY_PLOTS_3, m_aiCulturePlots); // Leoreth
	pStream->Write(NUM_CITY_PLOTS_3, m_aiCultureCosts); // Leoreth

	pStream->WriteString(m_szName);
	pStream->WriteString(m_szScriptData);

	pStream->Write(GC.getNumBonusInfos(), m_paiNoBonus);
	pStream->Write(GC.getNumBonusInfos(), m_paiFreeBonus);
	pStream->Write(GC.getNumBonusInfos(), m_paiNumBonuses);
	pStream->Write(GC.getNumBonusInfos(), m_paiNumCorpProducedBonuses);
	pStream->Write(GC.getNumProjectInfos(), m_paiProjectProduction);
	pStream->Write(GC.getNumBuildingInfos(), m_paiBuildingProduction);
	pStream->Write(GC.getNumBuildingInfos(), m_paiBuildingProductionTime);
	pStream->Write(GC.getNumBuildingInfos(), m_paiBuildingOriginalOwner);
	pStream->Write(GC.getNumBuildingInfos(), m_paiBuildingOriginalTime);
	pStream->Write(GC.getNumUnitInfos(), m_paiUnitProduction);
	pStream->Write(GC.getNumUnitInfos(), m_paiUnitProductionTime);
	pStream->Write(GC.getNumUnitInfos(), m_paiGreatPeopleUnitRate);
	pStream->Write(GC.getNumUnitInfos(), m_paiGreatPeopleUnitProgress);
	pStream->Write(GC.getNumSpecialistInfos(), m_paiSpecialistCount);
	pStream->Write(GC.getNumSpecialistInfos(), m_paiMaxSpecialistCount);
	pStream->Write(GC.getNumSpecialistInfos(), m_paiForceSpecialistCount);
	pStream->Write(GC.getNumSpecialistInfos(), m_paiFreeSpecialistCount);
	pStream->Write(GC.getNumImprovementInfos(), m_paiImprovementFreeSpecialists);
	pStream->Write(GC.getNumReligionInfos(), m_paiReligionInfluence);
	pStream->Write(GC.getNumReligionInfos(), m_paiStateReligionHappiness);
	pStream->Write(GC.getNumUnitCombatInfos(), m_paiUnitCombatFreeExperience);
	pStream->Write(GC.getNumPromotionInfos(), m_paiFreePromotionCount);
	pStream->Write(GC.getNumBuildingInfos(), m_paiNumRealBuilding);
	pStream->Write(GC.getNumBuildingInfos(), m_paiNumFreeBuilding);

	pStream->Write(NUM_CITY_PLOTS, m_pabWorkingPlot);
	pStream->Write(GC.getNumReligionInfos(), m_pabHasReligion);
	pStream->Write(GC.getNumCorporationInfos(), m_pabHasCorporation);
	pStream->Write(GC.getNumUnitInfos(), m_pabIsUnitHurried); // Leoreth

	// Leoreth
	for (iI = 0; iI < GC.getNumBonusInfos(); iI++)
	{
		pStream->Write(NUM_YIELD_TYPES, m_ppaiBonusYield[iI]);
	}

	for (iI=0;iI<GC.getDefineINT("MAX_TRADE_ROUTES");iI++)
	{
		pStream->Write(m_paTradeCities[iI].eOwner);
		pStream->Write(m_paTradeCities[iI].iID);
	}

	m_orderQueue.Write(pStream);

	pStream->Write(m_iPopulationRank);
	pStream->Write(m_bPopulationRankValid);
	pStream->Write(NUM_YIELD_TYPES, m_aiBaseYieldRank);
	pStream->Write(NUM_YIELD_TYPES, m_abBaseYieldRankValid);
	pStream->Write(NUM_YIELD_TYPES, m_aiYieldRank);
	pStream->Write(NUM_YIELD_TYPES, m_abYieldRankValid);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiCommerceRank);
	pStream->Write(NUM_COMMERCE_TYPES, m_abCommerceRankValid);

	pStream->Write(m_aEventsOccured.size());
	for (std::vector<EventTypes>::iterator it = m_aEventsOccured.begin(); it != m_aEventsOccured.end(); ++it)
	{
		pStream->Write(*it);
	}

	pStream->Write(m_aBuildingYieldChange.size());
	for (std::vector<BuildingYieldChange>::iterator it = m_aBuildingYieldChange.begin(); it != m_aBuildingYieldChange.end(); ++it)
	{
		(*it).write(pStream);
	}

	pStream->Write(m_aBuildingCommerceChange.size());
	for (std::vector<BuildingCommerceChange>::iterator it = m_aBuildingCommerceChange.begin(); it != m_aBuildingCommerceChange.end(); ++it)
	{
		(*it).write(pStream);
	}

	pStream->Write(m_aBuildingHappyChange.size());
	for (BuildingChangeArray::iterator it = m_aBuildingHappyChange.begin(); it != m_aBuildingHappyChange.end(); ++it)
	{
		pStream->Write((*it).first);
		pStream->Write((*it).second);
	}

	pStream->Write(m_aBuildingHealthChange.size());
	for (BuildingChangeArray::iterator it = m_aBuildingHealthChange.begin(); it != m_aBuildingHealthChange.end(); ++it)
	{
		pStream->Write((*it).first);
		pStream->Write((*it).second);
	}
}


//------------------------------------------------------------------------------------------------
class VisibleBuildingComparator
{
public:
	bool operator() (BuildingTypes e1, BuildingTypes e2)
	{
		if(GC.getBuildingInfo(e1).getVisibilityPriority() > GC.getBuildingInfo(e2).getVisibilityPriority())
			return true;
		else if(GC.getBuildingInfo(e1).getVisibilityPriority() == GC.getBuildingInfo(e2).getVisibilityPriority())
		{
			//break ties by building type higher building type
			if(e1 > e2)
				return true;
		}

		return false;
	}
};

void CvCity::getVisibleBuildings(std::list<BuildingTypes>& kChosenVisible, int& iChosenNumGenerics)
{
	int iNumBuildings;
	BuildingTypes eCurType;
	std::vector<BuildingTypes> kVisible;

	// Leoreth: graphics paging
	if ( !plot()->shouldHaveFullGraphics() )
	{
		iChosenNumGenerics = 0;
		return;
	}

	iNumBuildings = GC.getNumBuildingInfos();
	for(int i = 0; i < iNumBuildings; i++)
	{
		eCurType = (BuildingTypes) i;
		if(getNumBuilding(eCurType) > 0)
		{
			kVisible.push_back(eCurType);
		}
	}

	// sort the visible ones by decreasing priority
	VisibleBuildingComparator kComp;
	std::sort(kVisible.begin(), kVisible.end(), kComp);

	// how big is this city, in terms of buildings?
	// general rule: no more than fPercentUnique percent of a city can be uniques
	int iTotalVisibleBuildings;
	if(stricmp(GC.getDefineSTRING("GAME_CITY_SIZE_METHOD"), "METHOD_EXPONENTIAL") == 0)
	{
		int iCityScaleMod =  ((int)(pow((float)getPopulation(), GC.getDefineFLOAT("GAME_CITY_SIZE_EXP_MODIFIER")))) * 2;
		iTotalVisibleBuildings = (10 + iCityScaleMod);
	}
	else
	{
		float fLo = GC.getDefineFLOAT("GAME_CITY_SIZE_LINMAP_AT_0");
		float fHi = GC.getDefineFLOAT("GAME_CITY_SIZE_LINMAP_AT_50");
		float fCurSize = (float)getPopulation();
		iTotalVisibleBuildings = int(((fHi - fLo) / 50.0f) * fCurSize + fLo);
	}
	float fMaxUniquePercent = GC.getDefineFLOAT("GAME_CITY_SIZE_MAX_PERCENT_UNIQUE");
	int iMaxNumUniques = (int)(fMaxUniquePercent * iTotalVisibleBuildings);

	// compute how many buildings are generics vs. unique Civ buildings?
	int iNumGenerics;
	int iNumUniques;
	if((int)kVisible.size() > iMaxNumUniques)
	{
		iNumUniques = iMaxNumUniques;
	}
	else
	{
		iNumUniques = kVisible.size();
	}
	iNumGenerics = iTotalVisibleBuildings - iNumUniques + getCitySizeBoost();

	// return
	iChosenNumGenerics = iNumGenerics;
	for(int i = 0; i < iNumUniques; i++)
	{
		kChosenVisible.push_back(kVisible[i]);
	}
}

static int natGetDeterministicRandom(int iMin, int iMax, int iSeedX, int iSeedY)
{
	srand(7297 * iSeedX + 2909  * iSeedY);
	return (rand() % (iMax - iMin)) + iMin;
}

void CvCity::getVisibleEffects(ZoomLevelTypes eCurZoom, std::vector<const TCHAR*>& kEffectNames)
{
	if (isOccupation() && isVisible(getTeam(), false) == true)
	{
		if (eCurZoom  == ZOOM_DETAIL)
		{
			kEffectNames.push_back("EFFECT_CITY_BIG_BURNING_SMOKE");
			kEffectNames.push_back("EFFECT_CITY_FIRE");
		}
		else
		{
			kEffectNames.push_back("EFFECT_CITY_BIG_BURNING_SMOKE");
		}
		return;
	}

	if ((getTeam() == GC.getGameINLINE().getActiveTeam()) || GC.getGameINLINE().isDebugMode())
	{

		if (angryPopulation() > 0)
		{
			kEffectNames.push_back("EFFECT_CITY_BURNING_SMOKE");
		}

		if (healthRate() < 0)
		{
			kEffectNames.push_back("EFFECT_CITY_DISEASED");
		}


		if (isWeLoveTheKingDay())
		{
			int iSeed = natGetDeterministicRandom(0, 32767, getX_INLINE(), getY_INLINE());
			CvRandom kRand;
			kRand.init(iSeed);

			// fireworks
			const TCHAR* szFireworkEffects[] =
			{"FIREWORKS_RED_LARGE_SLOW",
				"FIREWORKS_RED_SMALL_FAST",
				"FIREWORKS_GREEN_LARGE_SLOW",
				"FIREWORKS_GREEN_SMALL_FAST",
				"FIREWORKS_PURPLE_LARGE_SLOW",
				"FIREWORKS_PURPLE_SMALL_FAST",
				"FIREWORKS_YELLOW_LARGE_SLOW",
				"FIREWORKS_YELLOW_SMALL_FAST",
				"FIREWORKS_BLUE_LARGE_SLOW",
				"FIREWORKS_BLUE_SMALL_FAST"};

			int iNumEffects = sizeof(szFireworkEffects) / sizeof(TCHAR*);
			for(int i = 0; i < (iNumEffects < 3 ? iNumEffects : 3); i++)
			{
				kEffectNames.push_back(szFireworkEffects[kRand.get(iNumEffects)]);
			}
		}
	}
}

void CvCity::getCityBillboardSizeIconColors(NiColorA& kDotColor, NiColorA& kTextColor) const
{
	NiColorA kPlayerColor = GC.getColorInfo((ColorTypes) GC.getPlayerColorInfo(GET_PLAYER(getOwnerINLINE()).getPlayerColor()).getColorTypePrimary()).getColor();
	NiColorA kGrowing;
	kGrowing = NiColorA(0.73f,1,0.73f,1);
	NiColorA kShrinking(1,0.73f,0.73f,1);
	NiColorA kStagnant(0.83f,0.83f,0.83f,1);
	NiColorA kUnknown(.5f,.5f,.5f,1);
	NiColorA kWhite(1,1,1,1);
	NiColorA kBlack(0,0,0,1);

	//Rhye - start comment
	/*if ((getTeam() == GC.getGameINLINE().getActiveTeam()))
	{
		if (foodDifference() < 0)
		{
			if ((foodDifference() == -1) && (getFood() >= ((75 * growthThreshold()) / 100)))
			{
				kDotColor = kStagnant;
				kTextColor = kBlack;
			}
			else
			{
				kDotColor = kShrinking;
				kTextColor = kBlack;
			}
		}
		else if (foodDifference() > 0)
		{
			kDotColor = kGrowing;
			kTextColor = kBlack;
		}
		else if (foodDifference() == 0)
		{
			kDotColor = kStagnant;
			kTextColor = kBlack;
		}
	}
	else
	{*/
		kDotColor = kPlayerColor;
		NiColorA kPlayerSecondaryColor = GC.getColorInfo((ColorTypes) GC.getPlayerColorInfo(GET_PLAYER(getOwnerINLINE()).getPlayerColor()).getColorTypeSecondary()).getColor();
		kTextColor = kPlayerSecondaryColor;
	//} //Rhye
}

const TCHAR* CvCity::getCityBillboardProductionIcon() const
{
	if (canBeSelected() && isProduction())
	{
		CLLNode<OrderData>* pOrderNode;
		pOrderNode = headOrderQueueNode();
		FAssert(pOrderNode != NULL);

		const TCHAR* szIcon = NULL;
		switch(pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
			{
				UnitTypes eType = getProductionUnit();
				FAssert(eType != NO_UNIT);
				szIcon = GET_PLAYER(getOwnerINLINE()).getUnitButton(eType);
				break;
			}
		case ORDER_CONSTRUCT:
			{
				BuildingTypes eType = getProductionBuilding();
				FAssert(eType != NO_BUILDING);
				szIcon = GC.getBuildingInfo(eType).getButton();
				break;
			}
		case ORDER_CREATE:
			{
				ProjectTypes eType = getProductionProject();
				FAssert(eType != NO_PROJECT);
				szIcon = GC.getProjectInfo(eType).getButton();
				break;
			}
		case ORDER_MAINTAIN:
			{
				ProcessTypes eType = getProductionProcess();
				FAssert(eType != NO_PROCESS);
				szIcon = GC.getProcessInfo(eType).getButton();
				break;
			}
		default:
			{
				FAssert(false);
			}
		}
		return szIcon;
	}
	else
	{
		return ARTFILEMGR.getInterfaceArtInfo("INTERFACE_BUTTONS_NOPRODUCTION")->getPath();
	}
}

bool CvCity::getFoodBarPercentages(std::vector<float>& afPercentages) const
{
	if (!canBeSelected())
	{
		return false;
	}

	afPercentages.resize(NUM_INFOBAR_TYPES, 0.0f);
	if (foodDifference() < 0)
	{
		afPercentages[INFOBAR_STORED] = std::max(0, (getFood() + foodDifference())) / (float) growthThreshold();
		afPercentages[INFOBAR_RATE_EXTRA] = std::min(-foodDifference(), getFood()) / (float) growthThreshold();
	}
	else
	{
		afPercentages[INFOBAR_STORED] = getFood() / (float) growthThreshold();
		afPercentages[INFOBAR_RATE] = foodDifference() / (float) growthThreshold();
	}

	return true;
}

bool CvCity::getProductionBarPercentages(std::vector<float>& afPercentages) const
{
	if (!canBeSelected())
	{
		return false;
	}

	if (!isProductionProcess())
	{
		afPercentages.resize(NUM_INFOBAR_TYPES, 0.0f);
		int iProductionDiffNoFood = getCurrentProductionDifference(true, true);
		int iProductionDiffJustFood = getCurrentProductionDifference(false, true) - iProductionDiffNoFood;
		afPercentages[INFOBAR_STORED] = getProduction() / (float) getProductionNeeded();
		afPercentages[INFOBAR_RATE] = iProductionDiffNoFood / (float) getProductionNeeded();
		afPercentages[INFOBAR_RATE_EXTRA] = iProductionDiffJustFood / (float) getProductionNeeded();
	}

	return true;
}

NiColorA CvCity::getBarBackgroundColor() const
{
	if (atWar(getTeam(), GC.getGameINLINE().getActiveTeam()))
	{
		return NiColorA(0.5f, 0, 0, 0.5f); // red
	}
	return NiColorA(0, 0, 0, 0.5f);
}

bool CvCity::isStarCity() const
{
	return isCapital();
}

bool CvCity::isValidBuildingLocation(BuildingTypes eBuilding) const
{
	// if both the river and water flags are set, we require one of the two conditions, not both
	if (GC.getBuildingInfo(eBuilding).isWater())
	{
		if (!GC.getBuildingInfo(eBuilding).isRiver() || !plot()->isRiver())
		{
			if (!isCoastal(GC.getBuildingInfo(eBuilding).getMinAreaSize()))
			{
				return false;
			}
		}
	}
	else
	{
		if (area()->getNumTiles() < GC.getBuildingInfo(eBuilding).getMinAreaSize())
		{
			return false;
		}

		if (GC.getBuildingInfo(eBuilding).isRiver())
		{
			if (!(plot()->isRiver()))
			{
				return false;
			}
		}
	}

	return true;
}

int CvCity::getTriggerValue(EventTriggerTypes eTrigger) const
{
	FAssert(eTrigger >= 0);
	FAssert(eTrigger < GC.getNumEventTriggerInfos());

	CvEventTriggerInfo& kTrigger = GC.getEventTriggerInfo(eTrigger);


	if (!CvString(kTrigger.getPythonCanDoCity()).empty())
	{
		long lResult;

		CyArgsList argsList;
		argsList.add(eTrigger);
		argsList.add(getOwnerINLINE());
		argsList.add(getID());

		gDLL->getPythonIFace()->callFunction(PYRandomEventModule, kTrigger.getPythonCanDoCity(), argsList.makeFunctionArgs(), &lResult);

		if (0 == lResult)
		{
			return MIN_INT;
		}
	}

	if (kTrigger.getNumBuildings() > 0 && kTrigger.getNumBuildingsRequired() > 0)
	{
		bool bFoundValid = false;

		for (int i = 0; i < kTrigger.getNumBuildingsRequired(); ++i)
		{
			if (kTrigger.getBuildingRequired(i) != NO_BUILDINGCLASS)
			{
				BuildingTypes eBuilding = (BuildingTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(kTrigger.getBuildingRequired(i));
				if (NO_BUILDING != eBuilding)
				{
					if (getNumRealBuilding(eBuilding) > 0)
					{
						bFoundValid = true;
					}
				}
			}
		}

		if (!bFoundValid)
		{
			return MIN_INT;
		}
	}


	if (getReligionCount() < kTrigger.getNumReligions())
	{
		return MIN_INT;
	}

	if (kTrigger.getNumReligions() > 0 && kTrigger.getNumReligionsRequired() > 0)
	{
		bool bFoundValid = false;

		for (int i = 0; i < kTrigger.getNumReligionsRequired(); ++i)
		{
			if (!kTrigger.isStateReligion() || kTrigger.getReligionRequired(i) == GET_PLAYER(getOwnerINLINE()).getStateReligion())
			{
				if (isHasReligion((ReligionTypes)kTrigger.getReligionRequired(i)))
				{
					if (!kTrigger.isHolyCity() || isHolyCity((ReligionTypes)kTrigger.getReligionRequired(i)))
					{
						bFoundValid = true;
					}
				}
			}
		}

		if (!bFoundValid)
		{
			return MIN_INT;
		}
	}

	if (getCorporationCount() < kTrigger.getNumCorporations())
	{
		return MIN_INT;
	}

	if (kTrigger.getNumCorporations() > 0 && kTrigger.getNumCorporationsRequired() > 0)
	{
		bool bFoundValid = false;

		for (int i = 0; i < kTrigger.getNumCorporationsRequired(); ++i)
		{
			if (isHasCorporation((CorporationTypes)kTrigger.getCorporationRequired(i)))
			{
				if (!kTrigger.isHeadquarters() || isHeadquarters((CorporationTypes)kTrigger.getCorporationRequired(i)))
				{
					bFoundValid = true;
				}
			}
		}

		if (!bFoundValid)
		{
			return MIN_INT;
		}
	}

	if (kTrigger.getMinPopulation() > 0)
	{
		if (getPopulation() < kTrigger.getMinPopulation())
		{
			return MIN_INT;
		}
	}


	if (kTrigger.getMaxPopulation() > 0)
	{
		if (getPopulation() > kTrigger.getMaxPopulation())
		{
			return MIN_INT;
		}
	}

	if (kTrigger.getAngry() > 0)
	{
		if (unhappyLevel(0) - happyLevel() < kTrigger.getAngry())
		{
			return MIN_INT;
		}
	}
	else if (kTrigger.getAngry() < 0)
	{
		if (happyLevel() - unhappyLevel(0) < -kTrigger.getAngry())
		{
			return MIN_INT;
		}
	}

	if (kTrigger.getUnhealthy() > 0)
	{
		if (badHealth(false, 0) - goodHealth() < kTrigger.getUnhealthy())
		{
			return MIN_INT;
		}
	}
	else if (kTrigger.getUnhealthy() < 0)
	{
		if (goodHealth() - badHealth(false, 0) < -kTrigger.getUnhealthy())
		{
			return MIN_INT;
		}
	}

	if (kTrigger.isPrereqEventCity() && kTrigger.getNumPrereqEvents() > 0)
	{
		bool bFoundValid = true;

		for (int iI = 0; iI < kTrigger.getNumPrereqEvents(); ++iI)
		{
			if (!isEventOccured((EventTypes)kTrigger.getPrereqEvent(iI)))
			{
				bFoundValid = false;
				break;
			}
		}

		if (!bFoundValid)
		{
			return MIN_INT;
		}
	}


	int iValue = 0;

	if (0 == getFood() && kTrigger.getCityFoodWeight() > 0)
	{
		return MIN_INT;
	}

	iValue += getFood() * kTrigger.getCityFoodWeight();

	return iValue;
}

bool CvCity::canApplyEvent(EventTypes eEvent, const EventTriggeredData& kTriggeredData) const
{
	CvEventInfo& kEvent = GC.getEventInfo(eEvent);

	if (GET_PLAYER((PlayerTypes)getOwnerINLINE()).isMinorCiv())
	{
		return false;
	}

	if (!kEvent.isCityEffect() && !kEvent.isOtherPlayerCityEffect())
	{
		return true;
	}

	if (-1 == kTriggeredData.m_iCityId && kEvent.isCityEffect())
	{
		return false;
	}

	if (-1 == kTriggeredData.m_iOtherPlayerCityId && kEvent.isOtherPlayerCityEffect())
	{
		return false;
	}

	if (kEvent.getFood() + ((100 + kEvent.getFoodPercent()) * getFood()) / 100 < 0)
	{
		return false;
	}

	if (kEvent.getPopulationChange() + getPopulation() <= 0)
	{
		return false;
	}

	if (100 * kEvent.getCulture() + getCultureTimes100(getOwnerINLINE()) < 0)
	{
		return false;
	}

	if (kEvent.getBuildingClass() != NO_BUILDINGCLASS)
	{
		BuildingTypes eBuilding = (BuildingTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(kEvent.getBuildingClass());
		if (eBuilding == NO_BUILDING)
		{
			return false;
		}

		if (kEvent.getBuildingChange() > 0)
		{
			if (getNumBuilding(eBuilding) >= GC.getCITY_MAX_NUM_BUILDINGS())
			{
				return false;
			}
		}
		else if (kEvent.getBuildingChange() < 0)
		{
			if (getNumRealBuilding(eBuilding) + kEvent.getBuildingChange() < 0)
			{
				return false;
			}
		}
	}

	if (-1 != kEvent.getMaxNumReligions() && getReligionCount() > kEvent.getMaxNumReligions())
	{
		return false;
	}

	if (kEvent.getMinPillage() > 0)
	{
		int iNumImprovements = 0;
		for (int i = 0; i < NUM_CITY_PLOTS; ++i)
		{
			if (CITY_HOME_PLOT != i)
			{
				CvPlot* pPlot = getCityIndexPlot(i);
				if (NULL != pPlot && pPlot->getOwnerINLINE() == getOwnerINLINE())
				{
					if (NO_IMPROVEMENT != pPlot->getImprovementType() && !GC.getImprovementInfo(pPlot->getImprovementType()).isPermanent())
					{
						++iNumImprovements;
					}
				}
			}
		}

		if (iNumImprovements < kEvent.getMinPillage())
		{
			return false;
		}
	}

	return true;
}

void CvCity::applyEvent(EventTypes eEvent, const EventTriggeredData& kTriggeredData, bool bClear)
{
	if (!canApplyEvent(eEvent, kTriggeredData))
	{
		return;
	}

	setEventOccured(eEvent, true);

	CvEventInfo& kEvent = GC.getEventInfo(eEvent);

	if (kEvent.isCityEffect() || kEvent.isOtherPlayerCityEffect())
	{
		if (kEvent.getHappy() != 0)
		{
			changeExtraHappiness(kEvent.getHappy());
		}

		if (kEvent.getHealth() != 0)
		{
			changeExtraHealth(kEvent.getHealth());
		}

		if (kEvent.getHurryAnger() != 0)
		{
			changeHurryAngerTimer(kEvent.getHurryAnger() * flatHurryAngerLength());
		}

		if (kEvent.getHappyTurns() != 0)
		{
			changeHappinessTimer(kEvent.getHappyTurns());
		}

		if (kEvent.getFood() != 0 || kEvent.getFoodPercent() != 0)
		{
			changeFood(kEvent.getFood() + (kEvent.getFoodPercent() * getFood()) / 100);
		}

		if (kEvent.getPopulationChange() != 0)
		{
			changePopulation(kEvent.getPopulationChange());
		}

		if (kEvent.getRevoltTurns() > 0)
		{
			changeCultureUpdateTimer(kEvent.getRevoltTurns());
			changeOccupationTimer(kEvent.getRevoltTurns());
		}

		if (0 != kEvent.getSpaceProductionModifier())
		{
			changeSpaceProductionModifier(kEvent.getSpaceProductionModifier());
		}

		if (kEvent.getMaxPillage() > 0)
		{
			FAssert(kEvent.getMaxPillage() >= kEvent.getMinPillage());
			int iNumPillage = kEvent.getMinPillage() + GC.getGameINLINE().getSorenRandNum(kEvent.getMaxPillage() - kEvent.getMinPillage(), "Pick number of event pillaged plots");

			int iNumPillaged = 0;
			for (int i = 0; i < iNumPillage; ++i)
			{
				int iRandOffset = GC.getGameINLINE().getSorenRandNum(NUM_CITY_PLOTS, "Pick event pillage plot");
				for (int j = 0; j < NUM_CITY_PLOTS; ++j)
				{
					int iPlot = (j + iRandOffset) % NUM_CITY_PLOTS;
					if (CITY_HOME_PLOT != iPlot)
					{
						CvPlot* pPlot = getCityIndexPlot(iPlot);
						if (NULL != pPlot && pPlot->getOwnerINLINE() == getOwnerINLINE())
						{
							if (NO_IMPROVEMENT != pPlot->getImprovementType() && !GC.getImprovementInfo(pPlot->getImprovementType()).isPermanent())
							{
								CvWString szBuffer = gDLL->getText("TXT_KEY_EVENT_CITY_IMPROVEMENT_DESTROYED", GC.getImprovementInfo(pPlot->getImprovementType()).getTextKeyWide());
								gDLL->getInterfaceIFace()->addMessage(getOwnerINLINE(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_PILLAGED", MESSAGE_TYPE_INFO, GC.getImprovementInfo(pPlot->getImprovementType()).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_RED"), pPlot->getX_INLINE(), pPlot->getY_INLINE(), true, true);
								pPlot->setImprovementType(NO_IMPROVEMENT);
								++iNumPillaged;
								break;
							}
						}
					}
				}
			}

			PlayerTypes eOtherPlayer = kTriggeredData.m_eOtherPlayer;
			if (!kEvent.isCityEffect() && kEvent.isOtherPlayerCityEffect())
			{
				eOtherPlayer = kTriggeredData.m_ePlayer;
			}

			if (NO_PLAYER != eOtherPlayer)
			{
				CvWString szBuffer = gDLL->getText("TXT_KEY_EVENT_NUM_CITY_IMPROVEMENTS_DESTROYED", iNumPillaged, GET_PLAYER(getOwnerINLINE()).getCivilizationAdjectiveKey());
				gDLL->getInterfaceIFace()->addMessage(eOtherPlayer, false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_PILLAGED", MESSAGE_TYPE_INFO);
			}
		}

		for (int i = 0; i < GC.getNumSpecialistInfos(); ++i)
		{
			if (kEvent.getFreeSpecialistCount(i) > 0)
			{
				changeFreeSpecialistCount((SpecialistTypes)i, kEvent.getFreeSpecialistCount(i));
			}
		}

		if (kEvent.getCulture() != 0)
		{
			changeCulture(getOwnerINLINE(), kEvent.getCulture(), true, true);
		}
	}


	if (kEvent.getUnitClass() != NO_UNITCLASS)
	{
		UnitTypes eUnit = (UnitTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(kEvent.getUnitClass());
		if (eUnit != NO_UNIT)
		{
			for (int i = 0; i < kEvent.getNumUnits(); ++i)
			{
				GET_PLAYER(getOwnerINLINE()).initUnit(eUnit, getX_INLINE(), getY_INLINE());
			}
		}
	}

	if (kEvent.getBuildingClass() != NO_BUILDINGCLASS)
	{
		BuildingTypes eBuilding = (BuildingTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(kEvent.getBuildingClass());
		if (eBuilding != NO_BUILDING)
		{
			if (0 != kEvent.getBuildingChange())
			{
				setNumRealBuilding(eBuilding, getNumRealBuilding(eBuilding) + kEvent.getBuildingChange());
			}
		}
	}

	if (kEvent.getNumBuildingYieldChanges() > 0)
	{
		for (int iBuildingClass = 0; iBuildingClass < GC.getNumBuildingClassInfos(); ++iBuildingClass)
		{
			for (int iYield = 0; iYield < NUM_YIELD_TYPES; ++iYield)
			{
				setBuildingYieldChange((BuildingClassTypes)iBuildingClass, (YieldTypes)iYield, getBuildingYieldChange((BuildingClassTypes)iBuildingClass, (YieldTypes)iYield) + kEvent.getBuildingYieldChange(iBuildingClass, iYield));
			}
		}
	}

	if (kEvent.getNumBuildingCommerceChanges() > 0)
	{
		for (int iBuildingClass = 0; iBuildingClass < GC.getNumBuildingClassInfos(); ++iBuildingClass)
		{
			for (int iCommerce = 0; iCommerce < NUM_COMMERCE_TYPES; ++iCommerce)
			{
				setBuildingCommerceChange((BuildingClassTypes)iBuildingClass, (CommerceTypes)iCommerce, getBuildingCommerceChange((BuildingClassTypes)iBuildingClass, (CommerceTypes)iCommerce) + kEvent.getBuildingCommerceChange(iBuildingClass, iCommerce));
			}
		}
	}

	if (kEvent.getNumBuildingHappyChanges() > 0)
	{
		for (int iBuildingClass = 0; iBuildingClass < GC.getNumBuildingClassInfos(); ++iBuildingClass)
		{
			setBuildingHappyChange((BuildingClassTypes)iBuildingClass, kEvent.getBuildingHappyChange(iBuildingClass));
		}
	}

	if (kEvent.getNumBuildingHealthChanges() > 0)
	{
		for (int iBuildingClass = 0; iBuildingClass < GC.getNumBuildingClassInfos(); ++iBuildingClass)
		{
			setBuildingHealthChange((BuildingClassTypes)iBuildingClass, kEvent.getBuildingHealthChange(iBuildingClass));
		}
	}

	if (bClear)
	{
		for (int i = 0; i < GC.getNumEventInfos(); ++i)
		{
			setEventOccured((EventTypes)i, false);
		}
	}
}

bool CvCity::isEventOccured(EventTypes eEvent) const
{
	for (std::vector<EventTypes>::const_iterator it = m_aEventsOccured.begin(); it != m_aEventsOccured.end(); ++it)
	{
		if (*it == eEvent)
		{
			return true;
		}
	}

	return false;
}

void CvCity::setEventOccured(EventTypes eEvent, bool bOccured)
{
	for (std::vector<EventTypes>::iterator it = m_aEventsOccured.begin(); it != m_aEventsOccured.end(); ++it)
	{
		if (*it == eEvent)
		{
			if (!bOccured)
			{
				m_aEventsOccured.erase(it);
			}
			return;
		}
	}

	if (bOccured)
	{
		m_aEventsOccured.push_back(eEvent);
	}
}

// CACHE: cache frequently used values
///////////////////////////////////////
bool CvCity::hasShrine(ReligionTypes eReligion)
{
	bool bHasShrine = false;

	// note, for normal XML, this count will be one, there is only one shrine of each religion
	int	shrineBuildingCount = GC.getGameINLINE().getShrineBuildingCount(eReligion);
	for (int iI = 0; iI < shrineBuildingCount; iI++)
	{
		BuildingTypes eBuilding = GC.getGameINLINE().getShrineBuilding(iI, eReligion);

		if (getNumBuilding(eBuilding) > 0)
		{
			bHasShrine = true;
			break;
		}
	}

	return bHasShrine;
}

void CvCity::invalidatePopulationRankCache()
{
	m_bPopulationRankValid = false;
}

void CvCity::invalidateYieldRankCache(YieldTypes eYield)
{
	FAssertMsg(eYield >= NO_YIELD && eYield < NUM_YIELD_TYPES, "invalidateYieldRankCache passed bogus yield index");

	if (eYield == NO_YIELD)
	{
		for (int iI = 0; iI < NUM_YIELD_TYPES; iI++)
		{
			m_abBaseYieldRankValid[iI] = false;
			m_abYieldRankValid[iI] = false;
		}
	}
	else
	{
		m_abBaseYieldRankValid[eYield] = false;
		m_abYieldRankValid[eYield] = false;
	}
}

void CvCity::invalidateCommerceRankCache(CommerceTypes eCommerce)
{
	FAssertMsg(eCommerce >= NO_YIELD && eCommerce < NUM_YIELD_TYPES, "invalidateCommerceRankCache passed bogus commerce index");

	if (eCommerce == NO_COMMERCE)
	{
		for (int iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
		{
			m_abCommerceRankValid[iI] = false;
		}
	}
	else
	{
		m_abCommerceRankValid[eCommerce] = false;
	}
}

int CvCity::getBuildingYieldChange(BuildingClassTypes eBuildingClass, YieldTypes eYield) const
{
	for (std::vector<BuildingYieldChange>::const_iterator it = m_aBuildingYieldChange.begin(); it != m_aBuildingYieldChange.end(); ++it)
	{
		if ((*it).eBuildingClass == eBuildingClass && (*it).eYield == eYield)
		{
			return (*it).iChange;
		}
	}

	return 0;
}

void CvCity::setBuildingYieldChange(BuildingClassTypes eBuildingClass, YieldTypes eYield, int iChange)
{
	for (std::vector<BuildingYieldChange>::iterator it = m_aBuildingYieldChange.begin(); it != m_aBuildingYieldChange.end(); ++it)
	{
		if ((*it).eBuildingClass == eBuildingClass && (*it).eYield == eYield)
		{
			int iOldChange = (*it).iChange;
			if (iOldChange != iChange)
			{

				if (iChange == 0)
				{
					m_aBuildingYieldChange.erase(it);
				}
				else
				{
					(*it).iChange = iChange;
				}

				updateBuildingYieldChange(eBuildingClass, eYield, iChange - iOldChange);
			}

			return;
		}
	}

	if (0 != iChange)
	{
		BuildingYieldChange kChange;
		kChange.eBuildingClass = eBuildingClass;
		kChange.eYield = eYield;
		kChange.iChange = iChange;
		m_aBuildingYieldChange.push_back(kChange);

		updateBuildingYieldChange(eBuildingClass, eYield, iChange);
	}
}

void CvCity::changeBuildingYieldChange(BuildingClassTypes eBuildingClass, YieldTypes eYield, int iChange)
{
	setBuildingYieldChange(eBuildingClass, eYield, getBuildingYieldChange(eBuildingClass, eYield) + iChange);
}

// Leoreth
void CvCity::updateBuildingYieldChange(BuildingClassTypes eBuildingClass, YieldTypes eYield, int iChange)
{
	BuildingTypes eBuilding = (BuildingTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(eBuildingClass);
	if (NO_BUILDING != eBuilding)
	{
		if (getNumActiveBuilding(eBuilding) > 0)
		{
			changeBaseYieldRate(eYield, iChange * getNumActiveBuilding(eBuilding));
			// Leoreth: catch the overflow bug
			if (getBaseYieldRate(eYield) < 0 || getBaseYieldRate(eYield) > 1000) {
				GC.getGame().logMsg("Overflow in (%d, %d) for updateBuildingYieldChange()", getX(), getY());
				gDLL->getInterfaceIFace()->addMessage(GC.getGame().getActivePlayer(), true, GC.getEVENT_MESSAGE_TIME(), gDLL->getText("TXT_KEY_OVERFLOW", getX(), getY(), "setBuildingYieldChange2()"), "", MESSAGE_TYPE_MAJOR_EVENT, ARTFILEMGR.getInterfaceArtInfo("WORLDBUILDER_CITY_EDIT")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_RED"), getX_INLINE(), getY_INLINE(), true, true);
				GC.getGame().setAIAutoPlay(0);
				GC.getGame().setAIAutoPlayCatapult(0);
				gDLL->getEngineIFace()->AutoSave(true);
			}
		}
	}
}

void CvCity::changeReligionYieldChange(ReligionTypes eReligion, YieldTypes eYield, int iChange)
{
	if (eReligion == NO_RELIGION) return;

	int iI;
	BuildingTypes eBuilding;
	for (iI = 0; iI < GC.getNumBuildingClassInfos(); iI++)
	{
		eBuilding = (BuildingTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(iI);
		if (eBuilding != NO_BUILDING && GC.getBuildingInfo(eBuilding).getReligionType() == eReligion)
		{
			changeBuildingYieldChange((BuildingClassTypes)iI, eYield, iChange);
		}
	}
}

int CvCity::getBuildingCommerceChange(BuildingClassTypes eBuildingClass, CommerceTypes eCommerce) const
{
	for (std::vector<BuildingCommerceChange>::const_iterator it = m_aBuildingCommerceChange.begin(); it != m_aBuildingCommerceChange.end(); ++it)
	{
		if ((*it).eBuildingClass == eBuildingClass && (*it).eCommerce == eCommerce)
		{
			return (*it).iChange;
		}
	}

	return 0;
}

void CvCity::setBuildingCommerceChange(BuildingClassTypes eBuildingClass, CommerceTypes eCommerce, int iChange)
{
	for (std::vector<BuildingCommerceChange>::iterator it = m_aBuildingCommerceChange.begin(); it != m_aBuildingCommerceChange.end(); ++it)
	{
		if ((*it).eBuildingClass == eBuildingClass && (*it).eCommerce == eCommerce)
		{
			if ((*it).iChange != iChange)
			{
				if (iChange == 0)
				{
					m_aBuildingCommerceChange.erase(it);
				}
				else
				{
					(*it).iChange = iChange;
				}

				updateBuildingCommerce();
			}

			return;
		}
	}

	if (0 != iChange)
	{
		BuildingCommerceChange kChange;
		kChange.eBuildingClass = eBuildingClass;
		kChange.eCommerce = eCommerce;
		kChange.iChange = iChange;
		m_aBuildingCommerceChange.push_back(kChange);

		updateBuildingCommerce();
	}
}

void CvCity::changeBuildingCommerceChange(BuildingClassTypes eBuildingClass, CommerceTypes eCommerce, int iChange)
{
	setBuildingCommerceChange(eBuildingClass, eCommerce, getBuildingCommerceChange(eBuildingClass, eCommerce) + iChange);
}

/************************************************************************************************/
/* UNOFFICIAL_PATCH                       10/22/09                                jdog5000      */
/*                                                                                              */
/* Bugfix                                                                                       */
/************************************************************************************************/
/* orginal bts code
void CvCity::setBuildingHappyChange(BuildingClassTypes eBuildingClass, int iChange)
{
	for (BuildingChangeArray::iterator it = m_aBuildingHappyChange.begin(); it != m_aBuildingHappyChange.end(); ++it)
	{
		if ((*it).first == eBuildingClass)
		{
			if ((*it).second != iChange)
			{
				if ((*it).second > 0)
				{
					changeBuildingGoodHappiness(-(*it).second);
				}
				else if ((*it).second < 0)
				{
					changeBuildingBadHappiness((*it).second);
				}

				if (iChange == 0)
				{
					m_aBuildingHappyChange.erase(it);
				}
				else
				{
					(*it).second = iChange;
				}

				if (iChange > 0)
				{
					changeBuildingGoodHappiness(iChange);
				}
				else if (iChange < 0)
				{
					changeBuildingGoodHappiness(-iChange);
				}
			}

			return;
		}
	}

	if (0 != iChange)
	{
		m_aBuildingHappyChange.push_back(std::make_pair(eBuildingClass, iChange));

		if (iChange > 0)
		{
			changeBuildingGoodHappiness(iChange);
		}
		else if (iChange < 0)
		{
			changeBuildingGoodHappiness(-iChange);
		}
	}
}
*/
void CvCity::setBuildingHappyChange(BuildingClassTypes eBuildingClass, int iChange)
{
	for (BuildingChangeArray::iterator it = m_aBuildingHappyChange.begin(); it != m_aBuildingHappyChange.end(); ++it)
	{
		if ((*it).first == eBuildingClass)
		{
			if ((*it).second != iChange)
			{
				int iOldChange = (*it).second;

				m_aBuildingHappyChange.erase(it);

				BuildingTypes eBuilding = (BuildingTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(eBuildingClass);
				if (NO_BUILDING != eBuilding)
				{
					if (getNumActiveBuilding(eBuilding) > 0)
					{

						if (iOldChange > 0)
						{
							changeBuildingGoodHappiness(-iOldChange);
						}
						else if (iOldChange < 0)
						{
							changeBuildingBadHappiness(-iOldChange);
						}

						if( iChange != 0 )
						{
							m_aBuildingHappyChange.push_back(std::make_pair(eBuildingClass, iChange));
							if (iChange > 0)
							{
								changeBuildingGoodHappiness(iChange);
							}
							else if (iChange < 0)
							{
								changeBuildingBadHappiness(iChange);
							}
						}
					}
				}
			}

			return;
		}
	}

	if (0 != iChange)
	{
		BuildingTypes eBuilding = (BuildingTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(eBuildingClass);
		if (NO_BUILDING != eBuilding)
		{
			if (getNumActiveBuilding(eBuilding) > 0)
			{
				m_aBuildingHappyChange.push_back(std::make_pair(eBuildingClass, iChange));

				if (iChange > 0)
				{
					changeBuildingGoodHappiness(iChange);
				}
				else if (iChange < 0)
				{
					changeBuildingBadHappiness(iChange);
				}
			}
		}
	}
}
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/

int CvCity::getBuildingHappyChange(BuildingClassTypes eBuildingClass) const
{
	for (BuildingChangeArray::const_iterator it = m_aBuildingHappyChange.begin(); it != m_aBuildingHappyChange.end(); ++it)
	{
		if ((*it).first == eBuildingClass)
		{
			return (*it).second;
		}
	}

	return 0;
}

/************************************************************************************************/
/* UNOFFICIAL_PATCH                       10/22/09                                jdog5000      */
/*                                                                                              */
/* Bugfix                                                                                       */
/************************************************************************************************/
/* orginal bts code
void CvCity::setBuildingHealthChange(BuildingClassTypes eBuildingClass, int iChange)
{
	for (BuildingChangeArray::iterator it = m_aBuildingHealthChange.begin(); it != m_aBuildingHealthChange.end(); ++it)
	{
		if ((*it).first == eBuildingClass)
		{
			if ((*it).second != iChange)
			{
				if ((*it).second > 0)
				{
					changeBuildingGoodHealth(-(*it).second);
				}
				else if ((*it).second < 0)
				{
					changeBuildingBadHealth((*it).second);
				}

				if (iChange == 0)
				{
					m_aBuildingHealthChange.erase(it);
				}
				else
				{
					(*it).second = iChange;
				}

				if (iChange > 0)
				{
					changeBuildingGoodHealth(iChange);
				}
				else if (iChange < 0)
				{
					changeBuildingBadHealth(-iChange);
				}
			}

			return;
		}
	}

	if (0 != iChange)
	{
		m_aBuildingHealthChange.push_back(std::make_pair(eBuildingClass, iChange));

		if (iChange > 0)
		{
			changeBuildingGoodHappiness(iChange);
		}
		else if (iChange < 0)
		{
			changeBuildingGoodHappiness(-iChange);
		}
	}
}
*/
void CvCity::setBuildingHealthChange(BuildingClassTypes eBuildingClass, int iChange)
{
	for (BuildingChangeArray::iterator it = m_aBuildingHealthChange.begin(); it != m_aBuildingHealthChange.end(); ++it)
	{
		if ((*it).first == eBuildingClass)
		{
			if ((*it).second != iChange)
			{
				int iOldChange = (*it).second;

				m_aBuildingHealthChange.erase(it);

				BuildingTypes eBuilding = (BuildingTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(eBuildingClass);
				if (NO_BUILDING != eBuilding)
				{
					if (getNumActiveBuilding(eBuilding) > 0)
					{
						if (iOldChange > 0)
						{
							changeBuildingGoodHealth(-iOldChange);
						}
						else if (iOldChange < 0)
						{
							changeBuildingBadHealth(-iOldChange);
						}

						if( iChange != 0 )
						{
							m_aBuildingHealthChange.push_back(std::make_pair(eBuildingClass, iChange));
							if (iChange > 0)
							{
								changeBuildingGoodHealth(iChange);
							}
							else if (iChange < 0)
							{
								changeBuildingBadHealth(iChange);
							}
						}
					}
				}
			}

			return;
		}
	}

	if (0 != iChange)
	{
		BuildingTypes eBuilding = (BuildingTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(eBuildingClass);
		if (NO_BUILDING != eBuilding)
		{
			if (getNumActiveBuilding(eBuilding) > 0)
			{	
				m_aBuildingHealthChange.push_back(std::make_pair(eBuildingClass, iChange));

				if (iChange > 0)
				{
					changeBuildingGoodHealth(iChange);
				}
				else if (iChange < 0)
				{
					changeBuildingBadHealth(iChange);
				}
			}
		}
	}
}
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/

int CvCity::getBuildingHealthChange(BuildingClassTypes eBuildingClass) const
{
	for (BuildingChangeArray::const_iterator it = m_aBuildingHealthChange.begin(); it != m_aBuildingHealthChange.end(); ++it)
	{
		if ((*it).first == eBuildingClass)
		{
			return (*it).second;
		}
	}

	return 0;
}

void CvCity::liberate(bool bConquest)
{
	CvPlot* pPlot = plot();
	PlayerTypes ePlayer = getLiberationPlayer(bConquest);
	PlayerTypes eOwner = getOwnerINLINE();

	// Leoreth: release to independents
	if (ePlayer == NO_PLAYER)
	{
		ePlayer = GET_PLAYER(INDEPENDENT).getNumCities() > GET_PLAYER(INDEPENDENT2).getNumCities() ? INDEPENDENT2 : INDEPENDENT;
	}

	if (NO_PLAYER != ePlayer)
	{
		int iOldOwnerCulture = getCultureTimes100(eOwner);
		int iOldMasterLand = 0;
		int iOldVassalLand = 0;
		if (GET_TEAM(GET_PLAYER(ePlayer).getTeam()).isVassal(GET_PLAYER(eOwner).getTeam()))
		{
			iOldMasterLand = GET_TEAM(GET_PLAYER(eOwner).getTeam()).getTotalLand();
			iOldVassalLand = GET_TEAM(GET_PLAYER(ePlayer).getTeam()).getTotalLand(false);
		}

		CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_CITY_LIBERATED", getNameKey(), GET_PLAYER(eOwner).getNameKey(), GET_PLAYER(ePlayer).getCivilizationAdjectiveKey());
		for (int iI = 0; iI < MAX_PLAYERS; ++iI)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				if (isRevealed(GET_PLAYER((PlayerTypes)iI).getTeam(), false))
				{
					gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_REVOLTEND", MESSAGE_TYPE_MAJOR_EVENT, ARTFILEMGR.getInterfaceArtInfo("WORLDBUILDER_CITY_EDIT")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"), getX_INLINE(), getY_INLINE(), true, true);
				}
			}
		}
		GC.getGameINLINE().addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, eOwner, szBuffer, getX_INLINE(), getY_INLINE(), (ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"));

		GET_PLAYER(ePlayer).acquireCity(this, false, true, true);
		GET_PLAYER(ePlayer).AI_changeMemoryCount(eOwner, MEMORY_LIBERATED_CITIES, 1);

		if (GET_TEAM(GET_PLAYER(ePlayer).getTeam()).isVassal(GET_PLAYER(eOwner).getTeam()))
		{
			int iNewMasterLand = GET_TEAM(GET_PLAYER(eOwner).getTeam()).getTotalLand();
			int iNewVassalLand = GET_TEAM(GET_PLAYER(ePlayer).getTeam()).getTotalLand(false);

			GET_TEAM(GET_PLAYER(ePlayer).getTeam()).setMasterPower(GET_TEAM(GET_PLAYER(ePlayer).getTeam()).getMasterPower() + iNewMasterLand - iOldMasterLand);
			GET_TEAM(GET_PLAYER(ePlayer).getTeam()).setVassalPower(GET_TEAM(GET_PLAYER(ePlayer).getTeam()).getVassalPower() + iNewVassalLand - iOldVassalLand);
		}

		if (NULL != pPlot)
		{
			CvCity* pCity = pPlot->getPlotCity();
			if (NULL != pCity)
			{
				pCity->setCultureTimes100(ePlayer, pCity->getCultureTimes100(ePlayer) + iOldOwnerCulture / 2, true, true);
				pCity->setCultureTimes100(eOwner, iOldOwnerCulture / 2, true, true); // Leoreth: overall culture remains constant
			}

			if (GET_TEAM(GET_PLAYER(ePlayer).getTeam()).isAVassal())
			{
				for (int i = 0; i < GC.getDefineINT("COLONY_NUM_FREE_DEFENDERS"); ++i)
				{
					pCity->initConscriptedUnit();
				}
			}
		}
	}

	GET_PLAYER(eOwner).updateMaintenance(); // Leoreth
}

PlayerTypes CvCity::getLiberationPlayer(bool bConquest) const
{
	if (isCapital())
	{
		return NO_PLAYER;
	}

	//Rhye - start comment
	/*
	//for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; ++iPlayer) //Rhye
	for (int iPlayer = 0; iPlayer < NUM_MAJOR_PLAYERS; ++iPlayer) //Rhye
	{
		CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iPlayer);
		if (kLoopPlayer.isAlive() && kLoopPlayer.getParent() == getOwnerINLINE())
		{
			CvCity* pLoopCapital = kLoopPlayer.getCapitalCity();
			if (NULL != pLoopCapital)
			{
				if (pLoopCapital->area() == area())
				{
					return (PlayerTypes)iPlayer;
				}
			}
		}
	}

	CvPlayer& kOwner = GET_PLAYER(getOwnerINLINE());
	if (kOwner.canSplitEmpire() && kOwner.canSplitArea(area()->getID()))
	{
		PlayerTypes ePlayer = GET_PLAYER(getOwnerINLINE()).getSplitEmpirePlayer(area()->getID());

		if (NO_PLAYER != ePlayer)
		{
			if (GET_PLAYER(ePlayer).isAlive())
			{
				return ePlayer;
			}
		}
	}*/
	//Rhye - end comment

	PlayerTypes eBestPlayer = NO_PLAYER;
	//int iBestValue = 0;
	int iBestValue = 25; // Leoreth: some minimum amount of culture required

	int iTotalCultureTimes100 = countTotalCultureTimes100();

	//for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; ++iPlayer) //Rhye
	for (int iPlayer = 0; iPlayer < NUM_MAJOR_PLAYERS; ++iPlayer) //Rhye
	{
		CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iPlayer);

		if (kLoopPlayer.isAlive())
		{
			if (kLoopPlayer.canReceiveTradeCity())
			{
				CvCity* pCapital = kLoopPlayer.getCapitalCity();
				if (NULL != pCapital)
				{
					int iCapitalDistance = ::plotDistance(getX_INLINE(), getY_INLINE(), pCapital->getX_INLINE(), pCapital->getY_INLINE());
					if (area() != pCapital->area())
					{
						iCapitalDistance *= 2;
					}

					int iCultureTimes100 = getCultureTimes100((PlayerTypes)iPlayer);

					if (bConquest)
					{
						if (iPlayer == getOriginalOwner())
						{
							iCultureTimes100 *= 3;
							iCultureTimes100 /= 2;
						}
					}

					if (GET_PLAYER((PlayerTypes)iPlayer).getTeam() == getTeam()
						|| GET_TEAM(GET_PLAYER((PlayerTypes)iPlayer).getTeam()).isVassal(getTeam())
						|| GET_TEAM(getTeam()).isVassal(GET_PLAYER((PlayerTypes)iPlayer).getTeam()))
					{
						iCultureTimes100 *= 2;
						iCultureTimes100 = (iCultureTimes100 + iTotalCultureTimes100) / 2;
					}

					int iValue = std::max(100, iCultureTimes100) / std::max(1, iCapitalDistance);

					// Leoreth: better value for core and historical tiles
					if (plot()->isCore(getOwner()))
						iValue *= 3;
					else if (plot()->getSettlerValue(getOwner()) > 90)
						iValue *= 2;

					if (iValue > iBestValue)
					{
						iBestValue = iValue;
						eBestPlayer = (PlayerTypes)iPlayer;
					}
				}
			}
		}
	}

	if (NO_PLAYER != eBestPlayer)
	{
		if (getOwnerINLINE() == eBestPlayer)
		{
			return NO_PLAYER;
		}

		for (int iPlot = 0; iPlot < NUM_CITY_PLOTS; ++iPlot)
		{
			CvPlot* pLoopPlot = ::plotCity(getX_INLINE(), getY_INLINE(), iPlot);

			if (NULL != pLoopPlot)
			{
				if (pLoopPlot->isVisibleEnemyUnit(eBestPlayer))
				{
					return NO_PLAYER;
				}
			}
		}
	}

	return eBestPlayer;
}

int CvCity::getBestYieldAvailable(YieldTypes eYield) const
{
	int iBestYieldAvailable = 0;

	for (int iJ = 0; iJ < NUM_CITY_PLOTS; ++iJ)
	{
		if (iJ != CITY_HOME_PLOT)
		{
			if (!isWorkingPlot(iJ))
			{
				CvPlot* pPlot = getCityIndexPlot(iJ);

				if (NULL != pPlot && canWork(pPlot))
				{
					if (pPlot->getYield(eYield) > iBestYieldAvailable)
					{
						iBestYieldAvailable = pPlot->getYield(eYield);
					}
				}
			}
		}
	}

	for (int iJ = 0; iJ < GC.getNumSpecialistInfos(); ++iJ)
	{
		if (isSpecialistValid((SpecialistTypes)iJ, 1))
		{
			int iYield = GC.getSpecialistInfo((SpecialistTypes)iJ).getYieldChange(eYield);
			if (iYield > iBestYieldAvailable)
			{
				iBestYieldAvailable = iYield;
			}
		}
	}

	return iBestYieldAvailable;
}

bool CvCity::isAutoRaze() const
{
	// Leoreth: don't raze holy cities
	if (isHolyCity())
	{
		return false;
	}

	if (!GC.getGameINLINE().isOption(GAMEOPTION_NO_CITY_RAZING))
	{
		if (getHighestPopulation() == 1)
		{
			return true;
		}

		if (GC.getGameINLINE().getMaxCityElimination() > 0)
		{
			return true;
		}
	}

	if (GC.getGameINLINE().isOption(GAMEOPTION_ONE_CITY_CHALLENGE) && isHuman())
	{
		return true;
	}

	return false;
}

int CvCity::getMusicScriptId() const
{
	bool bIsHappy = true;
	if (GC.getGameINLINE().getActiveTeam() == getTeam())
	{
		if (angryPopulation() > 0)
		{
			bIsHappy = false;
		}
	}
	else
	{
		if (GET_TEAM(GC.getGameINLINE().getActiveTeam()).isAtWar(getTeam()))
		{
			bIsHappy = false;
		}
	}

	CvLeaderHeadInfo& kLeaderInfo = GC.getLeaderHeadInfo(GET_PLAYER(getOwnerINLINE()).getLeaderType());
	EraTypes eCurEra = GET_PLAYER(getOwnerINLINE()).getCurrentEra();
	if (bIsHappy)
	{
		return (kLeaderInfo.getDiploPeaceMusicScriptIds(eCurEra));
	}
	else
	{
		return (kLeaderInfo.getDiploWarMusicScriptIds(eCurEra));
	}
}

int CvCity::getSoundscapeScriptId() const
{
	return GC.getEraInfo(GET_PLAYER(getOwnerINLINE()).getCurrentEra()).getCitySoundscapeSciptId(getCitySizeType());
}

void CvCity::cheat(bool bCtrl, bool bAlt, bool bShift)
{
	if (gDLL->getChtLvl() > 0)
	{
		if (bCtrl)
		{
			changeCulture(getOwnerINLINE(), 10, true, true);
		}
		else if (bShift)
		{
			changePopulation(1);
		}
		else
		{
			popOrder(0, true);
		}
	}
}

void CvCity::getBuildQueue(std::vector<std::string>& astrQueue) const
{
	CLLNode<OrderData>* pNode = headOrderQueueNode();
	while (pNode != NULL)
	{
		switch (pNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
			astrQueue.push_back(GC.getUnitInfo((UnitTypes)(pNode->m_data.iData1)).getType());
			break;

		case ORDER_CONSTRUCT:
			astrQueue.push_back(GC.getBuildingInfo((BuildingTypes)(pNode->m_data.iData1)).getType());
			break;

		case ORDER_CREATE:
			astrQueue.push_back(GC.getProjectInfo((ProjectTypes)(pNode->m_data.iData1)).getType());
			break;

		case ORDER_MAINTAIN:
			astrQueue.push_back(GC.getProcessInfo((ProcessTypes)(pNode->m_data.iData1)).getType());
			break;

		default:
			FAssert(false);
			break;
		}

		pNode = nextOrderQueueNode(pNode);
	}
}

int CvCity::getRegionID() const
{
	return GC.getMapINLINE().plotSorenINLINE(getX_INLINE(), getY_INLINE())->getRegionID();
}

//Leoreth: to protect Middle Eastern cities from repeated invasions
bool CvCity::isMiddleEast() const
{
	return (getRegionID() == REGION_PERSIA || getRegionID() == REGION_MESOPOTAMIA || getRegionID() == REGION_ANATOLIA || (getX_INLINE() == 68 && getY_INLINE() == 45));
}

bool CvCity::canEnslave() const
{
	return canEnslave(false);
}

bool CvCity::canEnslave(bool bGeneral) const
{			
	if (GET_PLAYER(getOwnerINLINE()).canEnslave())
	{
		if (getRegionID() == REGION_WEST_AFRICA || getRegionID() == REGION_SOUTH_AFRICA || getRegionID() == REGION_ETHIOPIA)
		{
			if (bGeneral)
			{
				return true;
			}

			if (isDisorder())
			{
				return false;
			}

			if (isDrafted())
			{
				return false;
			}

			if (getPopulation() <= 2)
			{
				return false;
			}

			if (getPopulation() < GC.getDefineINT("CONSCRIPT_MIN_CITY_POPULATION")+2)
			{
				return false;
			}

			return true;
		}
	}

	return false;
}

int CvCity::getSpecialistGoodHappiness() const
{
	return m_iSpecialistGoodHappiness;
}

int CvCity::getSpecialistBadHappiness() const
{
	int iSpecialistBadHappiness = m_iSpecialistBadHappiness;

	// Leoreth: increased unhappiness from Egalitarianism
	int iAngerModifier = 0;
	for (int iI = 0; iI < GC.getNumCivicInfos(); iI++)
	{
		iAngerModifier += GET_PLAYER(getOwnerINLINE()).getCivicPercentAnger((CivicTypes)iI, false);
	}

	return iSpecialistBadHappiness * (GC.getPERCENT_ANGER_DIVISOR() + 4 * iAngerModifier) / GC.getPERCENT_ANGER_DIVISOR();
}

void CvCity::changeSpecialistGoodHappiness(int iChange)
{
	m_iSpecialistGoodHappiness += iChange;
}

void CvCity::changeSpecialistBadHappiness(int iChange)
{
	m_iSpecialistBadHappiness += iChange;
}

// Leoreth
bool CvCity::isMongolUP() const
{
	return m_bMongolUP;
}

void CvCity::setMongolUP(bool bNewValue)
{
	m_bMongolUP = bNewValue;
}

int CvCity::getCorporationGoodHappiness() const
{
	return m_iCorporationGoodHappiness;
}

int CvCity::getCorporationBadHappiness() const
{
	return m_iCorporationBadHappiness;
}

int CvCity::getCorporationHappinessByCorporation(CorporationTypes eCorporation) const
{
	FAssertMsg(eCorporation >= 0, "eCorporation expected to be >= 0");
	FAssertMsg(eCorporation < GC.getNumCorporationInfos(), "GC.getNumCorporationInfos expected to be >= 0");

	int iNumBonuses = 0;
	int iHappiness = 0;

	if (isActiveCorporation(eCorporation) && !isDisorder())
	{
		for (int i = 0; i < GC.getNUM_CORPORATION_PREREQ_BONUSES(); ++i)
		{
			BonusTypes eBonus = (BonusTypes)GC.getCorporationInfo(eCorporation).getPrereqBonus(i);
			iNumBonuses = getNumBonuses(eBonus);

			if (NO_BONUS != eBonus && iNumBonuses > 0)
			{
				iHappiness += GC.getCorporationInfo(eCorporation).getHappiness() * std::min(12, iNumBonuses);
			}
		}
	}
	
	// Leoreth: corporation bad happiness modifier
	if (iHappiness < 0)
	{
		iHappiness *= 100 + GET_PLAYER(getOwner()).getCorporationUnhappinessModifier();
		iHappiness /= 100;
	}

	return iHappiness / 10;
}

int CvCity::getCorporationHealth() const
{
	return m_iCorporationHealth;
}

int CvCity::getCorporationUnhealth() const
{
	return m_iCorporationUnhealth;
}

int CvCity::getCorporationHealthByCorporation(CorporationTypes eCorporation) const
{
	FAssertMsg(eCorporation >= 0, "eCorporation expected to be >= 0");
	FAssertMsg(eCorporation < GC.getNumCorporationInfos(), "GC.getNumCorporationInfos expected to be >= 0");

	int iNumBonuses = 0;
	int iHealth = 0;

	if (isActiveCorporation(eCorporation) && !isDisorder())
	{
		for (int i = 0; i < GC.getNUM_CORPORATION_PREREQ_BONUSES(); ++i)
		{
			BonusTypes eBonus = (BonusTypes)GC.getCorporationInfo(eCorporation).getPrereqBonus(i);
			iNumBonuses = getNumBonuses(eBonus);

			if (NO_BONUS != eBonus && iNumBonuses > 0)
			{
				iHealth += GC.getCorporationInfo(eCorporation).getHealth() * std::min(12, iNumBonuses);
			}
		}
	}

	return iHealth / 10;
}

// Leoreth
int CvCity::getGameTurnPlayerLost(PlayerTypes ePlayer)
{
	return m_aiGameTurnPlayerLost[ePlayer];
}

void CvCity::setGameTurnPlayerLost(PlayerTypes ePlayer, int iNewValue)
{
	m_aiGameTurnPlayerLost[ePlayer] = iNewValue;
}

// Leoreth
bool CvCity::isColony() const
{
	CvCity* pCapital = GET_PLAYER(getOwner()).getCapitalCity();

	if (pCapital == NULL) return false;

	return (GC.getMap().getArea(getArea())->getClosestAreaSize(30) != GC.getMap().getArea(pCapital->getArea())->getClosestAreaSize(30));
}

// Leoreth: at most half of the population may be slaves
bool CvCity::canSlaveJoin() const
{
	if (!plot()->canUseSlave(getOwner())) return false;

	SpecialistTypes eSlave = (SpecialistTypes)GC.getInfoTypeForString("SPECIALIST_SLAVE");
	int iNumSlaves = getFreeSpecialistCount(eSlave);

	return (2 * iNumSlaves < getPopulation());
}

// Leoreth
int CvCity::calculateCultureCost(CvPlot* pPlot, bool bOrdering) const
{
	if (plot() == pPlot) return 0;

	// tiles with forts can be covered for free
	if (pPlot->getImprovementType() != NO_IMPROVEMENT && GC.getImprovementInfo(pPlot->getImprovementType()).isActsAsCity()) return 0;

	int iCost = pPlot->calculateCultureCost();
	//int iDistance = plotDistance(getX(), getY(), pPlot->getX(), pPlot->getY());
	int iDistance = std::max(plotDistance(getX(), getY(), pPlot->getX(), pPlot->getY()), GC.getMap().calculatePathDistance(plot(), pPlot));

	if (bOrdering)
	{
		if (pPlot->getBonusType() < 0 && iCost >= 15) iCost += 100; 
		iCost += 100 * iDistance;
		if (pPlot->isWater() && !pPlot->isLake() && pPlot->getBonusType() == -1 && iDistance > 1)
		{
			if (!isCoastal(20)) iCost += 1000;
			else if (iDistance > 1) iCost += 5;
		}

		// skip already owned tiles - no, only causes problems in case the controlling city is lost
		//if (pPlot->getOwner() == getOwner()) iCost += 1000;

		// even with Polynesian UP Oceans should still be covered last
		if (getOwnerINLINE() == POLYNESIA && pPlot->getTerrainType() == TERRAIN_OCEAN) iCost += GC.getTerrainInfo(TERRAIN_OCEAN).getCultureCostModifier();
	}

	if (pPlot->getBonusType() >= 0 && GET_TEAM(GET_PLAYER(getOwner()).getTeam()).isHasTech((TechTypes)GC.getBonusInfo(pPlot->getBonusType()).getTechReveal())) iCost += GC.getDefineINT("CULTURE_COST_BONUS");
	
	if (iDistance <= 1) iCost -= GC.getDefineINT("CULTURE_COST_DISTANCE");
	else iCost += std::max(3, iDistance) * GC.getDefineINT("CULTURE_COST_DISTANCE");

	if (plot()->isRiver() && pPlot->isRiver()) iCost += GC.getDefineINT("CULTURE_COST_RIVER");

	// Leoreth: Inca UP
	if (getOwnerINLINE() == INCA && pPlot->isPeak()) iCost += GC.getDefineINT("CULTURE_COST_HILL") - GC.getDefineINT("CULTURE_COST_PEAK");

	// Leoreth: Polynesian UP
	if (getOwnerINLINE() == POLYNESIA && pPlot->getTerrainType() == TERRAIN_OCEAN) iCost -= GC.getTerrainInfo(TERRAIN_OCEAN).getCultureCostModifier();

	// Leoreth: Congolese UP
	if (getOwnerINLINE() == CONGO)
	{
		if (pPlot->getFeatureType() == FEATURE_MARSH || pPlot->getFeatureType() == FEATURE_JUNGLE || pPlot->getFeatureType() == FEATURE_RAINFOREST)
		{
			iCost  -= GC.getFeatureInfo(pPlot->getFeatureType()).getCultureCostModifier();
		}
	}

	if (!bOrdering && getOwner() == INDIA) log("Plot: (%d, %d), iDistance: %d, iCost: %d", pPlot->getX(), pPlot->getY(), iDistance, iCost);

	return bOrdering ? iCost : std::max(0, iCost);
}

// Leoreth: takes local index, returns plot as global index
int CvCity::getCulturePlotIndex(int i) const
{
	return m_aiCulturePlots[i];
}

// Leoreth: takes local index, returns plot via global index
CvPlot* CvCity::getCulturePlot(int i) const
{
	int iIndex = getCulturePlotIndex(i);

	// negative index means tile beyond northern or southern edge, just return city tile in this case, additional coverage of this tile does not hurt
	if (iIndex < 0) return GC.getMap().plot(getX(), getY());

	return GC.getMap().plotByIndex(iIndex);
}

// Leoreth: costs for local index
int CvCity::getCultureCost(int i) const
{
	return m_aiCultureCosts[i];
}

struct cultureCompare
{
	CvCity* city;

	bool operator() (int index1, int index2) 
	{ 
		CvPlot* kPlot1 = GC.getMap().plotByIndex(index1);
		CvPlot* kPlot2 = GC.getMap().plotByIndex(index2);

		// sort by plot culture costs
		int iCost1 = (kPlot1 != NULL && city != NULL) ? city->calculateCultureCost(kPlot1, true) : MAX_INT;
		int iCost2 = (kPlot2 != NULL && city != NULL) ? city->calculateCultureCost(kPlot2, true) : MAX_INT;

		return (iCost1 < iCost2);
	}
};

// Leoreth
void CvCity::updateCultureCosts()
{
	//setNextCoveredPlot(0, true);

	std::vector<int> plots;
	std::vector<int> openPlots;

	int iI;
	for (iI = 0; iI < getNextCoveredPlot(); iI++)
	{
		plots.push_back(m_aiCulturePlots[iI]);
	}

	for (iI = getNextCoveredPlot(); iI < NUM_CITY_PLOTS_3; iI++)
	{
		openPlots.push_back(m_aiCulturePlots[iI]);
	}

	cultureCompare cmp;
	cmp.city = this;
	std::sort(openPlots.begin(), openPlots.end(), cmp);

	for (std::vector<int>::iterator it = openPlots.begin(); it != openPlots.end(); ++it)
	{
		plots.push_back(*it);
	}

	iI = 0;
	int iCumulativeCosts = 0;
	int iCurrentCosts;
	CvPlot* plot;
	//if (getOwner() == EGYPT) GC.getGameINLINE().logMsg("Cumulative costs for x=%d, y=%d", getX(), getY());
	for (std::vector<int>::iterator it = plots.begin(); it != plots.end(); ++it)
	{
		m_aiCulturePlots[iI] = *it;
		plot = GC.getMap().plotByIndex(*it);
		iCurrentCosts = (plot != NULL) ? calculateCultureCost(plot) : 0;
		iCumulativeCosts += iCurrentCosts;
		m_aiCultureCosts[iI] = iCumulativeCosts; 
		//if (getOwner() == EGYPT) GC.getGameINLINE().logMsg("%d = %d (+%d)", iI, iCumulativeCosts, iCurrentCosts);
		iI++;
	}
}

int CvCity::getNextCoveredPlot() const
{
	return m_iNextCoveredPlot;
}

void CvCity::setNextCoveredPlot(int iNewValue, bool bUpdatePlotGroups)
{
	CvPlot* pLoopPlot;
	CvWString szBuffer;
	int iOldValue;
	int iCultureRange;
	int iI;

	//if (getOwner() == EGYPT) GC.getGameINLINE().logMsg("Next covered plot set to: %d (culture = %d)", iNewValue, getCultureTimes100(getOwnerINLINE()) / 100);

	iOldValue = getNextCoveredPlot();

	//GC.getGameINLINE().logMsg("iOldValue = %d, iNewValue = %d", iOldValue, iNewValue);

	if (iNewValue < iOldValue)
	{
		m_iNextCoveredPlot = iNewValue;

		if (iOldValue > 0)
		{
			for (iI = iOldValue; iI > iNewValue; iI--)
			{
				if (iI >= NUM_CITY_PLOTS_3) continue;

				pLoopPlot = getCulturePlot(iI);

				if (pLoopPlot != NULL)
				{
					//GC.getGameINLINE().logMsg("Removed coverage for x=%d, y=%d on x=%d, y=%d", getX(), getY(), pLoopPlot->getX(), pLoopPlot->getY());
					iCultureRange = std::max(0, plotDistance(getX_INLINE(), getY_INLINE(), pLoopPlot->getX(), pLoopPlot->getY()));
					pLoopPlot->changeCultureRangeCities(getOwnerINLINE(), iCultureRange, -1, bUpdatePlotGroups);
				}
			}
		}
	}

	if (iNewValue > iOldValue)
	{
		m_iNextCoveredPlot = iNewValue;

		bool bCoveredNewPlot = false;

		if (iNewValue > 0)
		{
			for (iI = iOldValue; iI < iNewValue; iI++)
			{
				pLoopPlot = getCulturePlot(iI);

				if (pLoopPlot != NULL)
				{
					//GC.getGameINLINE().logMsg("Added coverage for x=%d, y=%d on x=%d, y=%d (id=%d)", getX(), getY(), pLoopPlot->getX(), pLoopPlot->getY(), getCulturePlot(iI));
					iCultureRange = std::max(0, plotDistance(getX_INLINE(), getY_INLINE(), pLoopPlot->getX(), pLoopPlot->getY()));

					if (pLoopPlot->getCultureRangeCities(getOwnerINLINE(), iCultureRange) == 0)
					{
						bCoveredNewPlot = true;
					}

					pLoopPlot->changeCultureRangeCities(getOwnerINLINE(), iCultureRange, 1, bUpdatePlotGroups);
				}
			}
		}

		if (GC.getGameINLINE().isFinalInitialized())
		{
			if (getNextCoveredPlot() > 0 && getCultureCost(getNextCoveredPlot()-1) > 0 && bCoveredNewPlot)
			{
				szBuffer = gDLL->getText("TXT_KEY_MISC_BORDERS_EXPANDED", getNameKey());
				gDLL->getInterfaceIFace()->addMessage(getOwnerINLINE(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_CULTUREEXPANDS", MESSAGE_TYPE_MINOR_EVENT, GC.getCommerceInfo(COMMERCE_CULTURE).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), getX_INLINE(), getY_INLINE(), true, true);

				// ONEVENT - Culture growth
				CvEventReporter::getInstance().cultureExpansion(this, getOwnerINLINE());

				if (isHuman() && !isProductionAutomated())
				{
					if (isProductionProcess())
					{
						if (GC.getProcessInfo(getProductionProcess()).getProductionToCommerceModifier(COMMERCE_CULTURE) > 0)
						{
							m_bPopProductionProcess = true;
						}
					}
				}
			}
		}
	}
}

void CvCity::updateCoveredPlots(bool bUpdatePlotGroups)
{
	if (getCultureUpdateTimer() > 0)
	{
		return;
	}

	int iCulture = getCulture(getOwnerINLINE());
	int iNextCoveredPlot = 0;
	for (int iI = 0; iI < NUM_CITY_PLOTS_3; iI++)
	{
		if (iCulture < getCultureCost(iI)) break;
		iNextCoveredPlot++;
	}

	setNextCoveredPlot(iNextCoveredPlot, bUpdatePlotGroups);
}

// Leoreth: skip plots that are already covered by a city
int CvCity::getEffectiveNextCoveredPlot() const
{
	int iNextCoveredPlot = getNextCoveredPlot();
	int iI = 0;

	CvPlot* pLoopPlot;
	int iDistance;
	while (iI < NUM_CITY_PLOTS_3)
	{
		pLoopPlot = getCulturePlot(iI);
		iDistance = plotDistance(getX(), getY(), pLoopPlot->getX(), pLoopPlot->getY());

		if (pLoopPlot->getOwner() == NO_PLAYER && (iI >= iNextCoveredPlot || (iDistance > getCultureLevel() && iDistance > 0 && getCultureCost(iNextCoveredPlot) > getCultureThreshold((CultureLevelTypes)(iDistance-1))))) break;

		iI++;
	}

	return iI;
}

// Leoreth: takes local culture plot id, returns true if plot costs less culture than the culture expansion to reach it
bool CvCity::isCoveredBeforeExpansion(int i) const
{
	CvPlot* pPlot = getCulturePlot(i);
	int iDistance = plotDistance(getX(), getY(), pPlot->getX(), pPlot->getY());

	return (getCultureCost(i) < getCultureThreshold((CultureLevelTypes)iDistance));
}

// Leoreth: redraw Great Wall around this city
void CvCity::updateGreatWall()
{
	gDLL->getEngineIFace()->RemoveGreatWall(this);
	gDLL->getEngineIFace()->AddGreatWall(this);
}

// Leoreth: estimate how many points the city will grow in the next X turns
int CvCity::estimateGrowth(int iTurns) const
{
	int iTurnsLeft = iTurns;
	int iFoodStored = getFood();
	int iPopulation = getPopulation();
	int iFoodDifference = foodDifference();
	int iGrowthThreshold = growthThreshold();

	while (iFoodDifference > 0 && (iGrowthThreshold - iFoodStored) / iFoodDifference <= iTurnsLeft)
	{
		iPopulation++;
		iTurnsLeft -= (iGrowthThreshold - iFoodStored) / iFoodDifference;

		iGrowthThreshold = GET_PLAYER(getOwnerINLINE()).getGrowthThreshold(iPopulation);
		iFoodStored = iGrowthThreshold * getMaxFoodKeptPercent() / 100;

		iFoodDifference -= (iPopulation < NUM_CITY_PLOTS) ? 1 : 2;
	}

	return iPopulation - getPopulation();
}

void CvCity::replaceReligion(ReligionTypes eOldReligion, ReligionTypes eNewReligion)
{
	if (eOldReligion == NO_RELIGION) return;

	if (!isHasReligion(eOldReligion)) return;

	std::vector<int> removedBuildings;
	int iI;
	bool bRemoved;

	for (iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		CvBuildingInfo& kBuilding = GC.getBuildingInfo((BuildingTypes)iI);

		if (isHasRealBuilding((BuildingTypes)iI) && !isWorldWonderClass((BuildingClassTypes)kBuilding.getBuildingClassType()) && kBuilding.getSpecialBuildingType() != NO_SPECIALBUILDING && kBuilding.getPrereqReligion() == eOldReligion)
		{
			removedBuildings.push_back(kBuilding.getSpecialBuildingType());
			setHasRealBuilding((BuildingTypes)iI, false);
		}
	}

	if (!isHolyCity(eOldReligion))
	{
		setHasReligion(eOldReligion, false, true, true);
	}

	if (eNewReligion == NO_RELIGION) return;

	for (iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		CvBuildingInfo& kBuilding = GC.getBuildingInfo((BuildingTypes)iI);
		bRemoved = std::find(removedBuildings.begin(), removedBuildings.end(), kBuilding.getSpecialBuildingType()) != removedBuildings.end();

		if (bRemoved && kBuilding.getPrereqReligion() == eNewReligion)
		{
			setHasRealBuilding((BuildingTypes)iI, true);
		}
	}

	setHasReligion(eNewReligion, true, true, true);
}

void CvCity::removeReligion(ReligionTypes eReligion)
{
	replaceReligion(eReligion, NO_RELIGION);
}

void CvCity::spreadReligion(ReligionTypes eReligion, bool bMissionary)
{
	setHasReligion(eReligion, true, true, !bMissionary);

	ReligionTypes eDisappearingReligion = disappearingReligion(eReligion);

	int iDisappearanceChance = bMissionary ? 2 : 3;

	if (eDisappearingReligion != NO_RELIGION && GC.getGame().getSorenRandNum(iDisappearanceChance, "Religion disappearance") == 0)
	{
		log(CvWString::format(L"Remove religion %s from %s after spread", GC.getReligionInfo(eDisappearingReligion).getText(), getName().GetCString()));
		removeReligion(eDisappearingReligion);
	}

	if (isHasRealBuilding(PAGAN_TEMPLE))
	{
		setHasRealBuilding(PAGAN_TEMPLE, false);

		ReligionTypes eStateReligion = GET_PLAYER(getOwnerINLINE()).getStateReligion();
		if (eStateReligion != NO_RELIGION && eStateReligion == eReligion)
		{
			for (int iI = 0; iI < GC.getNumBuildingClassInfos(); iI++)
			{
				BuildingTypes eBuilding = (BuildingTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(iI);

				if (canConstruct(eBuilding) && GC.getBuildingInfo(eBuilding).getReligionType() == eStateReligion && GC.getBuildingInfo(eBuilding).getSpecialBuildingType() == GC.getInfoTypeForString("SPECIALBUILDING_TEMPLE"))
				{
					setHasRealBuilding(eBuilding, true);
					gDLL->getInterfaceIFace()->addMessage(getOwnerINLINE(), false, GC.getEVENT_MESSAGE_TIME(), gDLL->getText("TXT_KEY_PAGAN_TEMPLE_REPLACED", GC.getReligionInfo(eReligion).getText(), getName().GetCString(), GC.getBuildingInfo(eBuilding).getText()), GC.getBuildingInfo(eBuilding).getConstructSound(), MESSAGE_TYPE_MAJOR_EVENT, GC.getBuildingInfo(eBuilding).getArtInfo()->getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), getX_INLINE(), getY_INLINE(), true, true);
					break;
				}
			}
		}
		else
		{
			gDLL->getInterfaceIFace()->addMessage(getOwnerINLINE(), false, GC.getEVENT_MESSAGE_TIME(), gDLL->getText("TXT_KEY_PAGAN_TEMPLE_REMOVED", GC.getReligionInfo(eReligion).getText(), getName().GetCString()), "", MESSAGE_TYPE_MAJOR_EVENT, "", (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), getX_INLINE(), getY_INLINE(), true, true);
		}
	}
}

ReligionTypes CvCity::disappearingReligion(ReligionTypes eNewReligion) const
{
	int iI;
	ReligionTypes eReligion;
	std::vector<ReligionTypes> religions;

	for (iI = 0; iI < NUM_RELIGIONS; iI++)
	{
		eReligion = (ReligionTypes)iI;
		if (eReligion != eNewReligion)
		{
			if (isHasReligion(eReligion) && GET_PLAYER(getOwnerINLINE()).getSpreadType(plot(), eReligion) == RELIGION_SPREAD_NONE)
			{
				religions.push_back(eReligion);
			}
		}
	}

	if (religions.size() > 0)
	{
		return religions[GC.getGame().getSorenRandNum(religions.size(), "Disappearing religion")];
	}

	int iMaxReligions = std::max(2, 1 + getPopulation() / 5);

	ReligionSpreadTypes eCurrentSpread;
	ReligionSpreadTypes eNewReligionSpread = GET_PLAYER(getOwnerINLINE()).getSpreadType(plot(), eReligion);
	ReligionSpreadTypes eWorstSpread = RELIGION_SPREAD_FAST;
	religions.clear();

	if (getReligionCount() > iMaxReligions)
	{
		for (iI = 0; iI < NUM_RELIGIONS; iI++)
		{
			eReligion = (ReligionTypes)iI;
			if (eReligion != eNewReligion && isHasReligion(eReligion))
			{
				eCurrentSpread = GET_PLAYER(getOwnerINLINE()).getSpreadType(plot(), eReligion);
				if (eCurrentSpread <= eNewReligionSpread)
				{
					if (eCurrentSpread < eWorstSpread)
					{
						eWorstSpread = eCurrentSpread;
						religions.clear();
						religions.push_back(eReligion);
					} 
					else if (eCurrentSpread == eWorstSpread)
					{
						religions.push_back(eReligion);
					}
				}
			}
		}

		if (religions.size() > 0)
		{
			return religions[GC.getGame().getSorenRandNum(religions.size(), "Disappearing religion")];
		}
	}

	return NO_RELIGION;
}