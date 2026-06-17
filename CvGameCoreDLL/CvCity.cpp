#include "CvGameCoreDLL.h"
#include "CvCity.h"
#include "CvCityAI.h"
#include "PlotRange.h"
#include "CvArea.h"
#include "CoreAI.h"
#include "CvUnit.h"
#include "CvSelectionGroup.h"
#include "CvInfo_City.h"
#include "CvInfo_Terrain.h"
#include "CvInfo_GameOption.h"
#include "CvInfo_Civics.h"
#include "CvPopupInfo.h"
#include "CvGameTextMgr.h"
#include "CvBugOptions.h" // advc.060
#include "BBAILog.h" // BETTER_BTS_AI_MOD, AI logging, 10/02/09, jdog5000


CvCity::CvCity() // advc.003u: Merged with the deleted reset function
{
	createEntity(this); // create and attach entity to city

	m_iID = 0;
	m_iX = INVALID_PLOT_COORD;
	m_iY = INVALID_PLOT_COORD;
	m_ePlot = NO_PLOT_NUM; // advc.opt
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
	m_iSurroundingGoodHealth = 0;
	m_iSurroundingBadHealth = 0;
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
	m_iSurroundingGoodHappiness = 0;
	m_iSurroundingBadHappiness = 0;
	m_iBonusGoodHappiness = 0;
	m_iBonusBadHappiness = 0;
	m_iReligionGoodHappiness = 0;
	m_iReligionBadHappiness = 0;
	m_iExtraHappiness = 0;
	m_iExtraHealth = 0;
	m_iNoUnhappinessCount = 0;
	m_iUnhealthyPopulationModifier = 0; // K-Mod
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
	m_iPopRushHurryCount = 0; // advc.912d
	m_iMostRecentOrder = -1; // advc.004x

	// doc
	m_iPowerConsumedCount = 0;
	m_iSpecialistGoodHappiness = 0;
	m_iSpecialistBadHappiness = 0;
	m_iCorporationGoodHappiness = 0;
	m_iCorporationBadHappiness = 0;
	m_iCorporationHealth = 0;
	m_iCorporationUnhealth = 0;
	m_iCultureGreatPeopleRateModifier = 0;
	m_iCultureHappiness = 0;
	m_iCultureTradeRouteModifier = 0;
	m_iBuildingUnignorableBombardDefense = 0;
	m_iCultureRank = 0;
	m_iStabilityPopulation = 0;
	m_iBuildingUnhealthModifier = 0;
	m_iCorporationUnhealthModifier = 0;
	m_iTotalCultureTimes100 = 0;
	m_iBuildingDamage = 0;
	m_iBuildingDamageChange = 0;
	m_iTotalPopulationLoss = 0;
	m_iPopulationLoss = 0;

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
	m_bInvestigate = false; // advc.103
	m_bMostRecentUnit = false; // advc.004x
	m_bChooseProductionDirty = false;

    // doc
    m_bMongolUP = false;

	m_eOwner = NO_PLAYER;
	m_eOriginalCiv = NO_CIVILIZATION;
	m_ePreviousCiv = NO_CIVILIZATION;
	m_eCultureLevel = NO_CULTURELEVEL;
    m_eArtStyle = NO_ARTSTYLE;
	m_eNextCoveredPlot = NO_CULTUREPLOT;

	m_aTradeCities.resize(GC.getDefineINT(CvGlobals::MAX_TRADE_ROUTES));

	// Rank cache
	m_iPopulationRank = -1;
	m_bPopulationRankValid = false;
}

CvCity::~CvCity() // advc.003u: Merged with the deleted uninit function
{
	removeEntity(); // remove entity from engine
	destroyEntity(); // delete CvCityEntity and detach from us

	m_orderQueue.clear();
}


void CvCity::init(int iID, PlayerTypes eOwner, int iX, int iY, bool bBumpUnits,
	bool bUpdatePlotGroups, /* advc.ctr: */ int iOccupationTimer)
{
	//reset(iID, eOwner, kPlot.getX(), kPlot.getY());
	// <advc.003u> Reset merged into constructor
	m_iID = iID;
	m_eOwner = eOwner;
	m_iX = iX;
	m_iY = iY;
	// </advc.003u>
	updatePlot(); // advc.opt
	setupGraphical();

	CvPlayer& kOwner = GET_PLAYER(getOwner());
	m_eOriginalCiv = kOwner.getCivilizationType();
	setName(kOwner.getNewCityName(), /* advc.106k: */ false, true);

	setEverOwned(getOwner(), true);
	/*  advc.ctr: To prevent updateCultureLevel from bumping units in
		surrounding tiles after trading a city under occupation. Don't call
		setOccupationTimer though -- don't need all those updates. */
	m_iOccupationTimer = iOccupationTimer;
	// <advc.908b>
	if (bUpdatePlotGroups) // new city (not acquired from someone else)
		initTraitCulture(); // </advc.908b>

    // doc: gradual border expansion
    updateCultureCosts();

    // doc: culture determines art style type
    updateArtStyleType();

    updateCultureLevel(false);

    // doc: gradual border expansion
    updateCoveredPlots(false);

	CvPlot& kPlot = getPlot();
	{
		int const iFreeCityPlotCulture = GC.getDefineINT("FREE_CITY_CULTURE");
		if (kPlot.getCulture(getOwner()) < iFreeCityPlotCulture)
			kPlot.setCulture(getOwner(), iFreeCityPlotCulture, bBumpUnits, false);
	}
	kPlot.setOwner(getOwner(), bBumpUnits, false);
	kPlot.setPlotCity(this);

	int const iFreeCityAdjacentCulture = GC.getDefineINT("FREE_CITY_ADJACENT_CULTURE");
	FOR_EACH_ADJ_PLOT_VAR(getPlot())
	{
		if (pAdj->getCulture(getOwner()) < iFreeCityAdjacentCulture)
		{
			pAdj->setCulture(getOwner(), iFreeCityAdjacentCulture,
					// advc.opt: Updated in the next line in any case
					false/*was bBumpUnits*/, false);
		}
		pAdj->updateCulture(bBumpUnits, false);
	}
	if (GET_TEAM(getTeam()).isAVassal()) // advc (replacing a loop over "all" masters)
	{
		kPlot.changeAdjacentSight(GET_TEAM(getTeam()).getMasterTeam(),
				GC.getDefineINT(CvGlobals::PLOT_VISIBILITY_RANGE), true, NULL, false);
	}
	if (GC.getPythonCaller()->isCitiesDestroyFeatures(iX, iY) && kPlot.isFeature())
		kPlot.setFeatureType(NO_FEATURE);

	kPlot.setImprovementType(NO_IMPROVEMENT);
	kPlot.updateCityRoute(false);

	for (TeamIter<ALIVE> it; it.hasNext(); ++it)
	{
		if (kPlot.isVisible(it->getID()))
			setRevealed(it->getID(), true);
	}

	updateMilitaryHappinessUnits(); // advc.184: Moved into new function

	FOR_EACH_ENUM(Commerce)
	{
		changeCommerceHappinessPer(eLoopCommerce,
				GC.getInfo(eLoopCommerce).getInitialHappiness());
	}

	getArea().changeCitiesPerPlayer(getOwner(), 1);
	// <advc.030b>
	{
		CvArea* pWaterArea = waterArea(true);
		if(pWaterArea != NULL)
			pWaterArea->changeCitiesPerPlayer(getOwner(), 1);
	} // </advc.030b>

	CvGame& kGame = GC.getGame(); // advc
	GET_TEAM(getTeam()).changeNumCities(1);
	kGame.changeNumCities(1);
	setGameTurnFounded(kGame.getGameTurn());
    setGameTurnAcquired(kGame.getGameTurn());

    // doc: apply state religion building yield change
	FOR_EACH_ENUM(Yield)
    {
        changeReligionYieldChange(GET_PLAYER(eOwner).getStateReligion(), eLoopYield, GET_PLAYER(eOwner).getReligionYieldChange(eLoopYield));
    }

    // doc: Chinese UP: +25% food kept on city growth
    if (getCivilizationType() == CHINA)
    {
        changeMaxFoodKeptPercent(25);
    }

    // doc: Malay UP: +2 trade routes for cities with different landmass within third ring
    if (getCivilizationType() == MALAYS)
    {
		FOR_EACH_ENUM(CulturePlot)
        {
            if (!plotCulture(getX(), getY(), eLoopCulturePlot)->isWater() && plotCulture(getX(), getY(), eLoopCulturePlot)->sameArea(getPlot()))
            {
                changeExtraTradeRoutes(2);
                break;
            }
        }
    }

    // doc: wonder effects applying to all cities of the owner
    processPlayerBuildingEffects(1);

    // TODO: move into initialPopulation()
    int iCurrentEra = GET_PLAYER(eOwner).getCurrentEra();
    int iExtraPopulation = iCurrentEra > 0 ? iCurrentEra : 0;

    if (GET_TEAM(GET_PLAYER(eOwner).getTeam()).isHasTech((TechTypes)EXPLORATION))
    {
        if (isColony())
        {
            iExtraPopulation += 1;
        }
    }

    // Leoreth: Harappan UU (City Builder)
    if (getCivilizationType() == HARAPPA)
    {
        iExtraPopulation += 1;
    }

    changePopulation(GC.getDefineINT("INITIAL_CITY_POPULATION") + iExtraPopulation);
    //changePopulation(GC.getDefineINT("INITIAL_CITY_POPULATION") + iExtraPop);
    // TODO: end

	changePopulation(/* advc.004b: */ initialPopulation()); // (Moved into subroutine)

	changeAirUnitCapacity(GC.getDefineINT(CvGlobals::CITY_AIR_UNIT_CAPACITY));

	updateFreshWaterHealth();
	updateSurroundingHealthHappiness();
	updatePowerHealth();

	kOwner.updateMaintenance();

	GC.getMap().updateWorkingCity();
	kGame.AI_makeAssignWorkDirty();
	//kOwner.setFoundedFirstCity(true); // advc.104: Moved to CvPlayer::initCity

	// advc: Moved down
	CvCivilization const& kCiv = getCivilization();
	for (int i = 0; i < kCiv.getNumBuildings(); i++)
	{
		if (kOwner.isBuildingFree(kCiv.buildingAt(i)))
			setNumFreeBuilding(kCiv.buildingAt(i), 1);
	}
	if (kGame.isFinalInitialized() && kOwner.getNumCities() == 1)
	{
		for (int i = 0; i < kCiv.getNumBuildings(); i++)
		{
			BuildingTypes eBuilding = kCiv.buildingAt(i);
			if (kCiv.isFreeBuilding(eBuilding))
				setNumRealBuilding(eBuilding, 1);
		}
		if (!isHuman() /* advc.250b: */ && !kGame.isOption(GAMEOPTION_SPAH))
			changeOverflowProduction(GC.getDefineINT("INITIAL_AI_CITY_PRODUCTION"), 0);
		// <advc.124g>
		if (isHuman() && isActiveOwned() &&
			kOwner.getCurrentResearch() == NO_TECH)
		{
			kOwner.chooseTech();
		} // </advc.124g>
	}

	updateEspionageVisibility(false);

	if (bUpdatePlotGroups)
		kGame.updatePlotGroups();

	GC.getLogger().logCityBuilt(*this); // advc.003t: Moved down so that just a single param needs to be passed
}

// graphical only setup
void CvCity::setupGraphical()
{
	if (!GC.IsGraphicsInitialized())
		return;

	CvDLLEntity::setup();

	setInfoDirty(true);
	setLayoutDirty(true);
}

// advc.095: Based on CvUnit::reloadEntity
void CvCity::reloadEntity()
{
	FAssert(GC.IsGraphicsInitialized());
	removeEntity();
	destroyEntity();
	createEntity(this);
	setupGraphical();
}


void CvCity::kill(bool bUpdatePlotGroups, /* advc.001: */ bool bBumpUnits)
{
	CvPlot& kPlot = getPlot();
	PlayerTypes const eOwner = getOwner();
	CvPlayer& kOwner = GET_PLAYER(eOwner);

	if (isCitySelected())
		gDLL->UI().clearSelectedCities();

	for (CityPlotIter it(*this); it.hasNext(); ++it)
	{
		if (it->getWorkingCityOverride() == this)
			it->setWorkingCityOverride(NULL);
	}

	setCultureLevel(NO_CULTURELEVEL, false);
	setNextCoveredPlot(FIRST_CULTURE_PLOT, false); // doc: gradual border expansion

	FOR_EACH_ENUM(Building)
	{
		setNumRealBuilding(eLoopBuilding, 0);
		setNumFreeBuilding(eLoopBuilding, 0);
	}
	FOR_EACH_ENUM(Specialist)
		setFreeSpecialistCount(eLoopSpecialist, 0);
	FOR_EACH_ENUM(Yield)
	{
		setTradeYield(eLoopYield, 0);
		setCorporationYield(eLoopYield, 0);
	}
	FOR_EACH_ENUM(Religion)
	{
		setHasReligion(eLoopReligion, false, false, true);
		if (isHolyCity(eLoopReligion))
			GC.getGame().setHolyCity(eLoopReligion, NULL, false);
	}
	FOR_EACH_ENUM(Corporation)
	{
		setHasCorporation(eLoopCorporation, false, false);
		if (isHeadquarters(eLoopCorporation))
			GC.getGame().setHeadquarters(eLoopCorporation, NULL, false);
	}

	setPopulation(0);
	AI().AI_assignWorkingPlots();
	clearOrderQueue();

	// remember the visibility before we take away the city from the plot below
	std::vector<bool> abEspionageVisibility(TeamIter<>::count(), false);
	for (TeamIter<CIV_ALIVE> it; it.hasNext(); ++it)
		abEspionageVisibility[it->getID()] = getEspionageVisibility(it->getID());
	/*  UNOFFICIAL_PATCH, Bugfix, 08/04/09, jdog5000:
		Need to clear trade routes of dead city, else they'll be claimed for the owner forever. */
	clearTradeRoutes();
	/*	<advc.001> The culture rate isn't relevant for gameplay, but let's still
		keep a correct count. (And other commerce types can be relevant in mods.) */
	/*	When in disorder the trait culture should already have been subtracted -
		or may never have been added when razing a city. (fix by keldath) */
	if (!isDisorder())
	{
		FOR_EACH_ENUM(Commerce)
		{
			changeCommerceRateTimes100(eLoopCommerce,
					-100 * kOwner.getFreeCityCommerce(eLoopCommerce));
		}
	} // </advc.001>

	kPlot.setPlotCity(NULL);
	kPlot.setRuinsName(getName()); // advc.005c

	// UNOFFICIAL_PATCH, replace floodplains after city is removed, 03/04/10, jdog5000: START
	if (kPlot.getBonusType() == NO_BONUS &&
		GC.getDefineBOOL("FLOODPLAIN_AFTER_RAZE")) // advc.129b
	{
		FOR_EACH_ENUM(Feature)
		{
			if (GC.getInfo(eLoopFeature).isRequiresRiver() &&
				kPlot.canHaveFeature(eLoopFeature) &&
				GC.getInfo(eLoopFeature).getAppearanceProbability() == 10000)
			{
				kPlot.setFeatureType(eLoopFeature);
				break;
			}
		}
	} // UNOFFICIAL_PATCH: END
	// <advc.104>
	for (PlayerAIIter<MAJOR_CIV> it; it.hasNext(); ++it)
		it->AI_cityKilled(*this); // </advc.104>
	getArea().changeCitiesPerPlayer(eOwner, -1);
	// <advc.030b>
	CvArea* pWaterArea = waterArea(true);
	/*  Can't really handle ice melted by global warming, but at least ensure
		that CitiesPerPlayer doesn't become negative. */
	if (pWaterArea != NULL && pWaterArea->getCitiesPerPlayer(eOwner, true) > 0)
		pWaterArea->changeCitiesPerPlayer(eOwner, -1); // </advc.030b>
	GET_TEAM(eOwner).changeNumCities(-1);

	GC.getGame().changeNumCities(-1);
#ifdef FASSERT_ENABLE
	FAssert(getWorkingPopulation() == 0);
	FAssert(!isWorkingPlot(CITY_HOME_PLOT));
	FAssert(getSpecialistPopulation() == 0);
	FAssert(getNumGreatPeople() == 0);
	FAssert(getBaseYieldRate(YIELD_FOOD) == 0);
	FAssert(getBaseYieldRate(YIELD_PRODUCTION) == 0);
	FAssert(getBaseYieldRate(YIELD_COMMERCE) == 0);
	FAssert(!isProduction());
	// <advc>
	FOR_EACH_ENUM(Commerce)
		FAssertMsg(getCommerceRate(eLoopCommerce) == 0,
				"Part of lost city's special commerce not subtracted from owner's cache");
	// </advc>
#endif
	bool const bCapital = isCapital();
	/*	<advc.106> For anouncement in case that capital moves.
		(Mustn't look for a new capital until the old one has been deleted.) */
	CvWString sNameKey;
	EagerEnumMap<PlayerTypes,bool> abRevealed;
	if (bCapital)
	{
		sNameKey = getNameKey();
		for (PlayerIter<MAJOR_CIV> itPlayer; itPlayer.hasNext(); ++itPlayer)
		{
			abRevealed.set(itPlayer->getID(), isRevealed(itPlayer->getTeam(),
					itPlayer->isSpectator())); // advc.127
		}
	} // </advc.106>
	kPlot.setImprovementType(GC.getRUINS_IMPROVEMENT());
	CvEventReporter::getInstance().cityLost(this);
	kOwner.deleteCity(getID());

    // doc: limited bonus effects
    kOwner.updateCultureRanks();

	kPlot.updateCulture(/*true*/ bBumpUnits, false); // advc.001
	/*	advc (note): setCultureLevel already updates culture in surrounding plots.
		I think this loop is only needed for rare cases where kPlot is part of a
		circle of plots granting ownership over a plot that is otherwise
		out of ownership range (see the end of CvPlot::calculateCulturalOwner). */
	FOR_EACH_ADJ_PLOT_VAR(kPlot)
		pAdj->updateCulture(true, false);

	if (GET_TEAM(eOwner).isAVassal()) // advc: Replacing a loop over "all" masters
	{
		kPlot.changeAdjacentSight(GET_TEAM(eOwner).getMasterTeam(),
				GC.getDefineINT(CvGlobals::PLOT_VISIBILITY_RANGE), false, NULL, false);
	}
	for (TeamIter<CIV_ALIVE> it; it.hasNext(); ++it)
	{
		if (abEspionageVisibility[it->getID()])
		{
			kPlot.changeAdjacentSight(it->getID(), GC.getDefineINT(
					CvGlobals::PLOT_VISIBILITY_RANGE), false, NULL, false);
		}
	}

	kOwner.updateMaintenance();
	GC.getMap().updateWorkingCity();
	GC.getGame().AI_makeAssignWorkDirty();

	if (bCapital)
	{
		kOwner.findNewCapital();
		// <advc.106> Announce new (and old) capital
		CvCity const* pNewCapital = kOwner.getCapital();
		if (pNewCapital != NULL)
		{
			CvWString szFullInfo = gDLL->getText("TXT_KEY_MISC_CAPITAL_MOVED",
					pNewCapital->getNameKey(),
					kOwner.getCivilizationShortDescriptionKey(), sNameKey.c_str());
			CvWString szOnlyOldKnown = gDLL->getText("TXT_KEY_MISC_NO_LONGER_CAPITAL",
					kOwner.getCivilizationShortDescriptionKey(), sNameKey.c_str());
			CvWString szOnlyNewKnown = gDLL->getText("TXT_KEY_MISC_IS_NOW_CAPITAL",
					pNewCapital->getNameKey(),
					kOwner.getCivilizationShortDescriptionKey());
			for (PlayerIter<MAJOR_CIV> it; it.hasNext(); ++it)
			{
				CvPlayer const& kObs = *it;
				if (kObs.getID() == getID())
					continue;
				if (GET_TEAM(getTeam()).isHasMet(kObs.getTeam()) ||
					 kObs.isSpectator()) // advc.127
				{
					CvWString* pszMsg = NULL;
					bool const bOldRevealed = abRevealed.get(kObs.getID());
					bool const bNewRevealed = pNewCapital->isRevealed(kObs.getTeam(),
							kObs.isSpectator()); // advc.127
					if (bOldRevealed && bNewRevealed)
						pszMsg = &szFullInfo;
					else if (bOldRevealed)
						pszMsg = &szOnlyOldKnown;
					else if (bNewRevealed)
						pszMsg = &szOnlyNewKnown;
					if (pszMsg != NULL)
					{
						CvPlot const& kFlashPlot = (bNewRevealed ?
								pNewCapital->getPlot() : kPlot);
						/*	<advc.127> Not really a major event, but minor events
							don't get shown in spectator mode. */
						InterfaceMessageTypes eMsgType = (kObs.isSpectator() ?
								MESSAGE_TYPE_MAJOR_EVENT : MESSAGE_TYPE_MINOR_EVENT);
						// </advc.127>
						gDLL->UI().addMessage(kObs.getID(), false, -1, *pszMsg, NULL,
								eMsgType, ARTFILEMGR.getInterfaceArtInfo(
								"INTERFACE_CITY_BAR_CAPITAL_TEXTURE")->getPath(),
								NO_COLOR, kFlashPlot.getX(), kFlashPlot.getY());
					}
				}
			}
		} // </advc.106>
		GET_TEAM(eOwner).resetVictoryProgress();
	}

	if (bUpdatePlotGroups)
		GC.getGame().updatePlotGroups();

	if (isActiveOwned())
		gDLL->UI().setDirty(SelectionButtons_DIRTY_BIT, true);
}


void CvCity::doTurn()
{
	PROFILE_FUNC();

	if (!isBombarded())
		changeDefenseDamage(-GC.getDefineINT(CvGlobals::CITY_DEFENSE_DAMAGE_HEAL_RATE));
	setLastDefenseDamage(getDefenseDamage());
	setBombarded(false);
	setPlundered(false);
	setDrafted(false);
	setAirliftTargeted(false);
	setCurrAirlift(0);
	m_bInvestigate = false; // advc.103

	AI().AI_doTurn();

	CvPlayer const& kOwner = GET_PLAYER(getOwner());

	// <advc.106k>
	if(!m_szPreviousName.empty() && m_szName.compare(m_szPreviousName) != 0)
	{
		FAssert(isHuman());
		GC.getGame().addReplayMessage(getPlot(), REPLAY_MESSAGE_MAJOR_EVENT,
				kOwner.getID(), gDLL->getText("TXT_KEY_MISC_CITY_RENAMED",
				m_szPreviousName.GetCString(), m_szName.GetCString()),
				kOwner.getPlayerTextColor());
		m_szPreviousName.clear();
	} // </advc.106k>
	bool const bForceProduction = true; // advc.064d
	/*bForceProduction =*/ doCheckProduction();

	doGrowth();
	doCulture();
	//doPlotCulture(false, kOwner.getID(), getCommerceRate(COMMERCE_CULTURE));
	// <K-Mod>
	doPlotCultureTimes100(false, kOwner.getID(),
			getCommerceRateTimes100(COMMERCE_CULTURE), true); // </K-Mod>
	doProduction(!bForceProduction);
	doDecay();
	doReligion();
	doGreatPeople();
	doMeltdown();
	/*	advc.004: Just so that human players don't get confused when inspecting
		an AI city. Will get updated at the start of the next turn anyway
		(CvPlayer::doTurn). Important not to update before doProduction as that
		would make production turns difficult to anticipate. */
	AI().AI_assignWorkingPlots();

	updateEspionageVisibility(true);

	if (!isDisorder())
	{
		for (WorkablePlotIter it(*this); it.hasNext(); ++it)
		{
			if (it->isBeingWorked())
				it->doImprovement();
            if (GET_PLAYER(getOwner()).isFreeImprovementUpgrade()) // doc: free improvement upgrade civic effect
                it->doImprovement();
		}
	}  // <advc.004x>
	else
	{
		if(isHuman() && !isProduction() && !isProductionAutomated() &&
			kOwner.getAnarchyTurns() == 1 &&
			GC.getGame().getGameState() != GAMESTATE_EXTENDED)
		{
			UnitTypes eMostRecentUnit = NO_UNIT;
			BuildingTypes eMostRecentBuilding = NO_BUILDING;
			ProjectTypes eMostRecentProject = NO_PROJECT;
			if(m_iMostRecentOrder >= 0)
			{
				if(m_bMostRecentUnit)
					eMostRecentUnit = (UnitTypes)m_iMostRecentOrder;
				else if(m_iMostRecentOrder >= GC.getNumBuildingInfos())
				{
					eMostRecentProject = (ProjectTypes)
							(m_iMostRecentOrder - GC.getNumBuildingInfos());
				}
				else eMostRecentBuilding = (BuildingTypes)m_iMostRecentOrder;
			}
			chooseProduction(eMostRecentUnit, eMostRecentBuilding,
					eMostRecentProject, m_iMostRecentOrder >= 0);
		}
	} // </advc.004x>

	// doc: ITER effect
    // TODO: refactor
	if (isHasBuildingEffect(ITER))
	{
		int iOldCommerce = getBuildingYieldChange((BuildingClassTypes)GC.getBuildingInfo((BuildingTypes)ITER).getBuildingClassType(), YIELD_COMMERCE);

		int iNewCommerce = 0;
		for (int iI = 0; iI < MAX_PLAYERS; iI++)
		{
			int iLoop;
			for (CvCity* pLoopCity = GET_PLAYER((PlayerTypes)iI).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER((PlayerTypes)iI).nextCity(&iLoop))
			{
				iNewCommerce += pLoopCity->getPowerConsumedCount();
			}
		}

		iNewCommerce /= 20;

		changeBuildingYieldChange((BuildingClassTypes)GC.getBuildingInfo((BuildingTypes)ITER).getBuildingClassType(), YIELD_COMMERCE, iNewCommerce - iOldCommerce);
	}

	if (getCultureUpdateTimer() > 0)
		changeCultureUpdateTimer(-1);

	/*  advc.023: Now handled in doRevolt (which is called at the start of a round,
		not the end of a player turn) */
	/*if (getOccupationTimer() > 0)
		changeOccupationTimer(-1);*/

	// doc: gradual city raze through population loss during occupation
	if (getPopulation() == 0)
	{
		completeRaze();
		return;
	}

	if (getHurryAngerTimer() > 0)
		changeHurryAngerTimer(-1);

	if (getConscriptAngerTimer() > 0)
		changeConscriptAngerTimer(-1);

	if (getDefyResolutionAngerTimer() > 0)
		changeDefyResolutionAngerTimer(-1);

	if (getHappinessTimer() > 0)
		changeHappinessTimer(-1);

	if (getEspionageHealthCounter() > 0)
		changeEspionageHealthCounter(-1);

	if (getEspionageHappinessCounter() > 0)
		changeEspionageHappinessCounter(-1);

	updateSurroundingHealthHappiness(); // advc.901

	if (isOccupation() || angryPopulation() > 0 || healthRate() < 0)
		setWeLoveTheKingDay(false);
    // doc: Brazilian UP: cities are guaranteed to celebrate
	else if (getPopulation() >= GC.getDefineINT("WE_LOVE_THE_KING_POPULATION_MIN_POPULATION") &&
		(getCivilizationType() == BRAZIL || SyncRandNum(GC.getDefineINT("WE_LOVE_THE_KING_RAND")) < getPopulation()))
	{
		setWeLoveTheKingDay(true);
	}
	else setWeLoveTheKingDay(false);

    // doc: culture determines updates art style type
    updateArtStyleType();

	CvEventReporter::getInstance().cityDoTurn(this, kOwner.getID());

	#ifdef _DEBUG // XXX
	FOR_EACH_ENUM(Yield)
	{	// <advc> Want to see the value in the debugger
		int iBaseYieldRate = getBaseYieldRate(eLoopYield);
		FAssert(iBaseYieldRate >= 0);
		FAssert(getYieldRate(eLoopYield) >= 0);
		// advc.104u: Code moved into auxiliary function
		int iCount = calculateBaseYieldRate(eLoopYield);
		FAssert(iCount == iBaseYieldRate); // </advc>
	}
	FOR_EACH_ENUM(Commerce)
	{
		FAssert(getBuildingCommerce(eLoopCommerce) >= 0);
		FAssert(getSpecialistCommerce(eLoopCommerce) >= 0);
		FAssert(getReligionCommerce(eLoopCommerce) >= 0);
		FAssert(getCorporationCommerce(eLoopCommerce) >= 0);
		FAssert(kOwner.getFreeCityCommerce(eLoopCommerce) >= 0);
	}
	FOR_EACH_ENUM(Bonus)
	{
		FAssert(isNoBonus(eLoopBonus) ||
				getNumBonuses(eLoopBonus) >= (!isConnectedToCapital() ? 0 :
				kOwner.getBonusImport(eLoopBonus) - kOwner.getBonusExport(eLoopBonus)));
	}
	#endif // XXX
}

// advc.104u: Cut, pasted, refactored from the end of CvCity::doTurn
int CvCity::calculateBaseYieldRate(YieldTypes eYield)
{
	int iR = 0;
	for (WorkingPlotIter it(*this); it.hasNext(); ++it)
	{
		CvPlot const* pPlot = getCityIndexPlot(it.currID());
		if(pPlot != NULL)
			iR += pPlot->getYield(eYield);
	}
	FOR_EACH_ENUM(Specialist)
	{
		iR += GET_PLAYER(getOwner()).specialistYield(eLoopSpecialist, eYield) *
				(getSpecialistCount(eLoopSpecialist) +
				getFreeSpecialistCount(eLoopSpecialist));
	}
	CvCivilization const& kCiv = getCivilization();
	for (int i = 0; i < kCiv.getNumBuildings(); i++)
	{
		BuildingTypes eBuilding = kCiv.buildingAt(i);
		CvBuildingInfo const& kBuilding = GC.getInfo(eBuilding);
		iR += getNumActiveBuilding(eBuilding) * (kBuilding.getYieldChange(eYield) +
				getBuildingYieldChange(kBuilding.getBuildingClassType(), eYield));
	}
	iR += getTradeYield(eYield);
	iR += getCorporationYield(eYield);
	return iR;
}

// advc: Code cut and pasted from CvPlot::doCulture; also refactored.
void CvCity::doRevolt()
{
	PROFILE_FUNC();
	// <advc.023>
	{
		scaled rDecrementProb = probabilityOccupationDecrement();
		if (SyncRandSuccess(rDecrementProb))
		{
			changeOccupationTimer(-1);
			return;
		}
	} // </advc.023>  <advc.099c>
	PlayerTypes eCulturalOwner = getPlot().calculateCulturalOwner();
	PlayerTypes eOwnerIgnRange = eCulturalOwner;
	if (GC.getDefineBOOL(CvGlobals::REVOLTS_IGNORE_CULTURE_RANGE))
		eOwnerIgnRange = getPlot().calculateCulturalOwner(true);
	// If not within culture range, can revolt but not flip.
	bool bCanFlip = (eOwnerIgnRange == eCulturalOwner);
	eCulturalOwner = eOwnerIgnRange;
	// </advc.099c>
	/*  <advc.101> To avoid duplicate code in CvDLLWidgetData::parseNationalityHelp,
		compute the revolt probability in a separate function. */
	{
		scaled rRevoltProb = revoltProbability();
		if (!SyncRandSuccess(rRevoltProb))
			return;
	} // </advc.101>
	damageGarrison(eCulturalOwner); // advc: Code moved into subroutine
	if (bCanFlip /* advc.099 */ && canCultureFlip(eCulturalOwner))
	{
		if (GET_PLAYER(eCulturalOwner).isOneCityChallenge())
			kill(true);
		else
		{	/*	<advc.023> Make sure that allowing cities to flip repeatedly
				while at war can't be exploited for racking up WS.
				Doesn't take care of shared war success, but that's hardly
				worth exploiting. */
			if (eCulturalOwner != BARBARIAN_PLAYER &&
				GET_TEAM(eCulturalOwner).isAtWar(getTeam()))
			{
				GET_TEAM(getTeam()).AI_changeWarSuccess(TEAMID(eCulturalOwner),
						-scaled::min(GC.getWAR_SUCCESS_CITY_CAPTURING(),
						GET_TEAM(getTeam()).AI_getWarSuccess(TEAMID(eCulturalOwner))));
			} // </advc.023>
			getPlot().setOwner(eCulturalOwner, true, true); // will delete pCity
		}
		/*  advc (comment): setOwner doesn't actually delete this object; just
			calls CvCity::kill. Messages also handled by setOwner (through
			CvPlayer::acquireCity). */
		return;
	}
	/*	K-Mod, 11/jan/11: Changed number of revolt turns to not depend on iCityStrength,
		because iCityStrength can be huge. */
	/*pCity->changeOccupationTimer(GC.getDefineINT("BASE_REVOLT_OCCUPATION_TURNS")
	+ ((iCityStrength * GC.getDefineINT("REVOLT_OCCUPATION_TURNS_PERCENT")) /
	100));*/ // BtS
	// <advc.023>
	/*  Removed factor 2 from the second summand. K-Mod 1.45 changelog said:
		'Decreased the duration of revolts from
		 3+2*(previous revolts) to 2+(previous revolts). (...)
		 The net effect of these changes is that (...) the number of turns spent
		 in revolt will be similar to before (...).'
		This is just what I need now that the occupation timer decreases
		probabilistically, but it wasn't committed to the K-Mod repository;
		so I'm adding it here. */
	int iTurnsOccupation = GC.getDefineINT("BASE_REVOLT_OCCUPATION_TURNS") +
			getNumRevolts(eCulturalOwner); // </advc.023>
	// K-Mod end
	changeNumRevolts(eCulturalOwner, 1);
	if (!isOccupation()) // advc.023: Don't prolong revolt
		changeOccupationTimer(iTurnsOccupation);
	CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_REVOLT_IN_CITY",
			GET_PLAYER(eCulturalOwner).getCivilizationAdjective(),
			getNameKey());
	// <advc.023>
	/*  Population loss if pCity should flip, but can't. We know at this point
		that the current revolt doesn't flip the city; but can it ever flip? */
	if ((!bCanFlip || !canCultureFlip(eCulturalOwner, false)) &&
		getNumRevolts(eCulturalOwner) > GC.getDefineINT(CvGlobals::NUM_WARNING_REVOLTS) &&
		getPopulation() > 1)
	{
		changePopulation(-1);
		// Says "Citizens have been killed"
		szBuffer.append(L" " + gDLL->getText("TXT_KEY_EVENT_HURRICANE_2"));
	} // </advc.023>
	/*  <advc.101> BtS comment: "XXX announce for all seen cities?"
		I guess that's better. Mustn't startle third parties with color
		and sound though. */
	for (PlayerIter<MAJOR_CIV> it; it.hasNext(); ++it)
	{
		CvPlayer const& kObs = *it;
		bool bAffected = (kObs.getID() == eCulturalOwner ||
				kObs.getID() == getOwner());
		if (!bAffected && !isRevealed(kObs.getTeam()))
			continue;
		InterfaceMessageTypes eMsg = MESSAGE_TYPE_INFO;
		LPCTSTR szSound = NULL;
		// Color of both the text and the flashing icon
		ColorTypes eColor = NO_COLOR;
		if (bAffected)
		{
			eMsg = MESSAGE_TYPE_MINOR_EVENT;
			szSound = "AS2D_CITY_REVOLT";
			eColor = GC.getColorType(kObs.getID() == getOwner() ? "RED" : "GREEN");
		}
		gDLL->UI().addMessage(kObs.getID(), false, -1, szBuffer, getPlot(),
				szSound, eMsg, ARTFILEMGR.getInterfaceArtPath("INTERFACE_RESISTANCE"), eColor);
	} // </advc.101>
}

// advc: Cut from CvPlot::doCulture; simplified.
void CvCity::damageGarrison(PlayerTypes eRevoltSource)
{
	FOR_EACH_UNIT_VAR_IN(pUnit, getPlot())
	{
		/*	advc.101: OK in BtS b/c Barbarian cities would flip on the first revolt.
			Now killed only when the city flips through CvPlot::setOwner. */
		/*if (pUnit->isBarbarian())
			pUnit->kill(false, eRevoltSource);
		else*/
		if(pUnit->canDefend())
			pUnit->changeDamage(pUnit->currHitPoints() / 2, eRevoltSource);
	}
}

bool CvCity::isCitySelected()
{
	return gDLL->UI().isCitySelected(this);
}


bool CvCity::canBeSelected() const
{
	CvGame const& kGame = GC.getGame();

	if (m_bInvestigate || // advc.103
		isActiveTeam() || kGame.isDebugMode())
	{
		return true;
	}
	TeamTypes const eActiveTeam = kGame.getActiveTeam();
	if (eActiveTeam != NO_TEAM && getPlot().isInvestigate(eActiveTeam))
		return true;

	FOR_EACH_ENUM(EspionageMission)
	{
		if (GC.getInfo(eLoopEspionageMission).isPassive() &&
			GC.getInfo(eLoopEspionageMission).isInvestigateCity() &&
			GET_PLAYER(kGame.getActivePlayer()).canDoEspionageMission(
			eLoopEspionageMission, getOwner(), plot()))
		{
			return true;
		}
	}
	return false;
}


void CvCity::updateSelectedCity(bool bTestProduction)
{
	for (CityPlotIter it(*this); it.hasNext(); ++it)
	{
		it->updateShowCitySymbols();
	}
	if (bTestProduction)
	{
		if (isActiveOwned() && !isProduction() &&
			!isProductionAutomated()) // K-Mod
		{
			chooseProduction(NO_UNIT, NO_BUILDING, NO_PROJECT, false, true);
		}
	}
}

// advc.103:
void CvCity::setInvestigate(bool b)
{
	m_bInvestigate = b;
}


void CvCity::updateYield()
{
	for (CityPlotIter it(*this); it.hasNext(); ++it)
	{
		it->updateYield();
	}
}

// XXX kill this?
void CvCity::updateVisibility()
{
	PROFILE_FUNC();

	if (!GC.IsGraphicsInitialized())
		return;

	FAssert(GC.getGame().getActiveTeam() != NO_TEAM);

	CvDLLEntity::setVisible(isRevealed(GC.getGame().getActiveTeam(), true));
}


void CvCity::createGreatPeople(UnitTypes eGreatPersonUnit, bool bIncrementThreshold,
	bool bIncrementExperience) /* advc: */ const
{
	GET_PLAYER(getOwner()).createGreatPeople(eGreatPersonUnit, bIncrementThreshold,
			bIncrementExperience, getPlot());
}


void CvCity::doTask(TaskTypes eTask, int iData1, int iData2, bool bOption,
	bool bAlt, bool bShift, bool bCtrl)
{
	bool bCede = false; // advc.ctr
	switch (eTask)
	{
	case TASK_RAZE:
		GET_PLAYER(getOwner()).raze(*this);
		break;

	case TASK_DISBAND:
		GET_PLAYER(getOwner()).disband(*this);
		break;
	// <advc.ctr>
	case TASK_CEDE: // Meaning (in this context): as part of a peace deal
		bCede = true;
		// fall through // </advc.ctr>
	case TASK_GIFT:
		if (getLiberationPlayer() == iData1)
			liberate(false, /* advc.ctr: */ bCede);
		else
		{
            CvPlot const& kPlot = getPlot();
			GET_PLAYER((PlayerTypes)iData1).acquireCity(this, false, true, true,
					bCede, bCede); // advc.ctr

            // doc: losing city affects maintenance
            GET_PLAYER(getOwner()).updateMaintenance();

		    // doc: trade city event
		    if (kPlot.isCity())
		    {
		        CvEventReporter::getInstance().cityGifted(kPlot.getPlotCity());
		    }
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
		AI().AI_setEmphasize((EmphasizeTypes)iData1, bOption);
		break;

	case TASK_CHANGE_SPECIALIST:
		alterSpecialistCount(((SpecialistTypes)iData1), iData2);
		break;

	case TASK_CHANGE_WORKING_PLOT:
		alterWorkingPlot((CityPlotTypes)iData1);
		break;

	case TASK_CLEAR_WORKING_OVERRIDE:
		clearWorkingOverride((CityPlotTypes)iData1);
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
		setRallyPlot(GC.getMap().plot(iData1, iData2));
		break;

	case TASK_CLEAR_RALLY_PLOT:
		setRallyPlot(NULL);
		break;

	default:
		FErrorMsg("eTask failed to match a valid option");
	}
}


void CvCity::chooseProduction(UnitTypes eTrainUnit, BuildingTypes eConstructBuilding,
	ProjectTypes eCreateProject, bool bFinish, bool bFront)
{
	// K-Mod. don't create the popup if the city is in disorder
	FAssert(isHuman() && !isProductionAutomated());
	if (isOccupation()) // advc.004x: was isDisorder
	{
		setChooseProductionDirty(true);
		return;
	}
	setChooseProductionDirty(false);
	// K-Mod end
	CvPopupInfo* pPopupInfo = new CvPopupInfo(BUTTONPOPUP_CHOOSEPRODUCTION);
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

	gDLL->UI().addPopup(pPopupInfo, getOwner(), false, bFront);
}

// advc.enum: Return type was int
CityPlotTypes CvCity::getCityPlotIndex(CvPlot const& kPlot) const
{
	return GC.getMap().plotCityXY(getX(), getY(), kPlot);
}

CvPlot* CvCity::getCityIndexPlot(CityPlotTypes ePlot) const // advc.enum: CityPlotTypes
{
	return GC.getMap().plotCity(getX(), getY(), ePlot);
}


bool CvCity::canWork(CvPlot const& kPlot) const
{
	if (kPlot.getWorkingCity() != this)
		return false;

	FAssert(getCityPlotIndex(kPlot) != NO_CITYPLOT);

	if (kPlot.plotCheck(PUF_canSiege, getOwner()) != NULL)
		return false;

	if (kPlot.isWater())
	{
		if (!GET_TEAM(getTeam()).isWaterWork())
			return false;

		if (kPlot.getBlockadedCount(getTeam()) > 0)
		{   /*  <advc.124> Should work, but I don't want units to overwrite
				blockades after all. */
			/*bool bDefended = false;
			for(int i = 0; i < MAX_CIV_PLAYERS; i++) {
				PlayerTypes eLoopPlayer = (PlayerTypes)i;
				if(GET_PLAYER(eLoopPlayer).isAlive() && GET_PLAYER(eLoopPlayer).getMasterTeam() ==
						GET_PLAYER(getOwner()).getMasterTeam() &&
						kPlot.isVisibleOtherUnit(eLoopPlayer)) {
					isDefended = true;
					break;
				}
			}
			if(!isDefended)*/ // </advc.124>
				return false;
		}

		// Replaced by blockade mission, above
		/*if (!kPlot.plotCheck(PUF_canDefend, -1, -1, NO_PLAYER, getTeam())) {
			FOR_EACH_ADJ_PLOT(kPlot) {
				if (pAdj->isWater() && pAdj->plotCheck(PUF_canSiege, getOwner()) != NULL)
					return false;
		} }*/
	}

	if (!kPlot.hasYield())
		return false;

	return true;
}


void CvCity::verifyWorkingPlot(CityPlotTypes ePlot) // advc.enum: CityPlotTypes
{
	FAssertEnumBounds(ePlot);
	if (isWorkingPlot(ePlot))
	{
		CvPlot* pPlot = getCityIndexPlot(ePlot);
		if (pPlot != NULL && !canWork(*pPlot))
		{
			setWorkingPlot(ePlot, false);
			AI_setAssignWorkDirty(true);
		}
	}
}


void CvCity::verifyWorkingPlots()
{
	FOR_EACH_ENUM(CityPlot)
		verifyWorkingPlot(eLoopCityPlot);
}


void CvCity::clearWorkingOverride(CityPlotTypes ePlot) // advc.enum: CityPlotTypes
{
	CvPlot* pPlot = getCityIndexPlot(ePlot);
	if (pPlot != NULL)
		pPlot->setWorkingCityOverride(NULL);
}


int CvCity::countNumImprovedPlots(ImprovementTypes eImprovement, bool bPotential) const
{
	int iCount = 0;
	for (WorkablePlotIter it(*this); it.hasNext(); ++it)
	{
		CvPlot const& kPlot = *it;
		if (eImprovement != NO_IMPROVEMENT)
		{
			if (kPlot.getImprovementType() == eImprovement ||
				(bPotential && kPlot.canHaveImprovement(eImprovement, getTeam())))
			{
				iCount++;
			}
		}
		else if (kPlot.isImproved())
			iCount++;
	}
	return iCount;
}

// doc (1SDAN)
// TODO: refactor
int CvCity::countNumBonusPlots(BonusTypes eBonus) const
{
	int iCount = 0;

	for (WorkingPlotIter it(*this); it.hasNext(); ++it)
	{
		if (eBonus != NO_BONUS)
		{
			if (it->getBonusType() == eBonus)
				iCount++;
		}
		else
		{
			if (it->getBonusType() != NO_BONUS)
				iCount++;
		}
	}

	return iCount;
}


int CvCity::countNumWaterPlots() const
{
	int iCount = 0;
	for (WorkablePlotIter it(*this); it.hasNext(); ++it)
	{
		if (it->isWater())
			iCount++;
	}
	return iCount;
}

int CvCity::countNumRiverPlots() const
{
	int iCount = 0;
	for (WorkablePlotIter it(*this); it.hasNext(); ++it)
	{
		if (it->isRiver())
			iCount++;
	}
	return iCount;
}


int CvCity::findPopulationRank() const
{
	if (m_bPopulationRankValid)
		return m_iPopulationRank;

	/*int iRank = 1;
	FOR_EACH_CITY(pLoopCity, GET_PLAYER(getOwner())) {
		if ((pLoopCity->getPopulation() > getPopulation()) ||
				((pLoopCity->getPopulation() == getPopulation()) && (pLoopCity->getID() < getID())))
			iRank++;
	}
	// shenanigans are to get around the const check
	m_bPopulationRankValid = true;
	m_iPopulationRank = iRank;*/ // BtS
	// K-Mod. Set all ranks at the same time.
	CvPlayer const& kPlayer = GET_PLAYER(getOwner());
	std::vector<std::pair<int,int> > aiiCityScores;
	FOR_EACH_CITY(pLoopCity, kPlayer)
	{
		aiiCityScores.push_back(std::make_pair(
				-pLoopCity->getPopulation(), pLoopCity->getID()));
	}
	// note: we are sorting by minimum of _negative_ score, and then by min cityID.
	std::sort(aiiCityScores.begin(), aiiCityScores.end());
	FAssert(aiiCityScores.size() == kPlayer.getNumCities());
	for (size_t i = 0; i < aiiCityScores.size(); i++)
	{
		CvCity* pLoopCity = kPlayer.getCity(aiiCityScores[i].second);
		pLoopCity->m_iPopulationRank = i + 1;
		pLoopCity->m_bPopulationRankValid = true;
	}
	FAssert(m_bPopulationRankValid);
	// K-Mod end
	return m_iPopulationRank;
}


int CvCity::findBaseYieldRateRank(YieldTypes eYield) const
{
	if (m_abBaseYieldRankValid.get(eYield))
		return m_aiBaseYieldRank.get(eYield); // advc
	/*int iRate = getBaseYieldRate(eYield);
	int iRank = 1;
	FOR_EACH_CITY(pLoopCity, GET_PLAYER(getOwner()) {
		if ((pLoopCity->getBaseYieldRate(eYield) > iRate) ||
			((pLoopCity->getBaseYieldRate(eYield) == iRate) && (pLoopCity->getID() < getID())))
			iRank++;
	}
	m_abBaseYieldRankValid.set(eYield, true);
	m_aiBaseYieldRank.set(eYield, iRank);*/ // BtS
	// K-Mod. Set all ranks at the same time.
	CvPlayer const& kPlayer = GET_PLAYER(getOwner());
	std::vector<std::pair<int, int> > city_scores;
	FOR_EACH_CITY(pLoopCity, kPlayer)
		city_scores.push_back(std::make_pair(-pLoopCity->getBaseYieldRate(eYield), pLoopCity->getID()));
	// note: we are sorting by minimum of _negative_ score, and then by min cityID.
	std::sort(city_scores.begin(), city_scores.end());
	FAssert(city_scores.size() == kPlayer.getNumCities());
	for (size_t i = 0; i < city_scores.size(); i++)
	{
		CvCity* pLoopCity = kPlayer.getCity(city_scores[i].second);
		pLoopCity->m_aiBaseYieldRank.set(eYield, i + 1);
		pLoopCity->m_abBaseYieldRankValid.set(eYield, true);
	}
	FAssert(m_abBaseYieldRankValid.get(eYield));
	// K-Mod end
	return m_aiBaseYieldRank.get(eYield);
}


int CvCity::findYieldRateRank(YieldTypes eYield) const
{
	if (m_abYieldRankValid.get(eYield))
		return m_aiYieldRank.get(eYield); // advc

	/*int iRate = getYieldRate(eYield);
	int iRank = 1;
	FOR_EACH_CITY(pLoopCity, GET_PLAYER(getOwner())) {
		if ((pLoopCity->getYieldRate(eYield) > iRate) ||
			((pLoopCity->getYieldRate(eYield) == iRate) && (pLoopCity->getID() < getID())))
			iRank++;
	}
	m_abYieldRankValid.set(eYield, true);
	m_aiYieldRank.set(eYield, iRank);*/ // BtS
	// K-Mod. Set all ranks at the same time.
	CvPlayer const& kPlayer = GET_PLAYER(getOwner());
	std::vector<std::pair<int,int> > city_scores;
	FOR_EACH_CITY(pLoopCity, kPlayer)
		city_scores.push_back(std::make_pair(-pLoopCity->getYieldRate(eYield), pLoopCity->getID()));
	// note: we are sorting by minimum of _negative_ score, and then by min cityID.
	std::sort(city_scores.begin(), city_scores.end());
	FAssert(city_scores.size() == kPlayer.getNumCities());
	for (size_t i = 0; i < city_scores.size(); i++)
	{
		CvCity* pLoopCity = kPlayer.getCity(city_scores[i].second);
		pLoopCity->m_aiYieldRank.set(eYield, i + 1);
		pLoopCity->m_abYieldRankValid.set(eYield, true);
	}
	FAssert(m_abYieldRankValid.get(eYield));
	// K-Mod end
	return m_aiYieldRank.get(eYield);
}


int CvCity::findCommerceRateRank(CommerceTypes eCommerce) const
{
	if (m_abCommerceRankValid.get(eCommerce))
		return m_aiCommerceRank.get(eCommerce);
	/*int iRate = getCommerceRateTimes100(eCommerce);
	int iRank = 1;
	FOR_EACH_CITY(pLoopCity, GET_PLAYER(getOwner()) {
		if ((pLoopCity->getCommerceRateTimes100(eCommerce) > iRate) ||
				((pLoopCity->getCommerceRateTimes100(eCommerce) == iRate) && (pLoopCity->getID() < getID())))
			iRank++;
	}
	m_abCommerceRankValid.set(eCommerce, true);
	m_aiCommerceRank.set(eCommerce, iRank);*/ // BtS
	// K-Mod. Set all ranks at the same time.
	CvPlayer const& kPlayer = GET_PLAYER(getOwner());
	std::vector<std::pair<int, int> > city_scores;
	FOR_EACH_CITY(pLoopCity, kPlayer)
		city_scores.push_back(std::make_pair(-pLoopCity->getCommerceRateTimes100(eCommerce), pLoopCity->getID()));
	// note: we are sorting by minimum of _negative_ score, and then by min cityID.
	std::sort(city_scores.begin(), city_scores.end());
	FAssert(city_scores.size() == kPlayer.getNumCities());
	for (size_t i = 0; i < city_scores.size(); i++)
	{
		CvCity* pLoopCity = kPlayer.getCity(city_scores[i].second);
		pLoopCity->m_aiCommerceRank.set(eCommerce, i + 1);
		pLoopCity->m_abCommerceRankValid.set(eCommerce, true);
	}
	FAssert(m_abCommerceRankValid.get(eCommerce));
	// K-Mod end
	return m_aiCommerceRank.get(eCommerce);
}

// Returns one of the upgrades
UnitTypes CvCity::allUpgradesAvailable(UnitTypes eUnit, int iUpgradeCount,
	BonusTypes eAssumeAvailable) const // advc.001u
{
	PROFILE_FUNC(); // advc

	FAssert(eUnit != NO_UNIT);

	CvCivilization const& kCiv = getCivilization();
	if (iUpgradeCount > kCiv.getNumUnits()) // (advc.003w: was >GC.getNumUnitClassInfos())
		return NO_UNIT;

	UnitTypes eUpgradeUnit = NO_UNIT;
	bool bUpgradeFound = false;
	bool bUpgradeAvailable = false;
	bool bUpgradeUnavailable = false;
	if (GC.getInfo(eUnit).isAnyUpgradeUnitClass()) // advc.003t
	{
		for (int i = 0; i < kCiv.getNumUnits(); i++)
		{
			if (!GC.getInfo(eUnit).getUpgradeUnitClass(kCiv.unitClassAt(i)))
				continue;

			bUpgradeFound = true;
			UnitTypes eTempUnit = allUpgradesAvailable(kCiv.unitAt(i), iUpgradeCount + 1,
					eAssumeAvailable); // advc.001u
			if (eTempUnit != NO_UNIT)
			{
				eUpgradeUnit = eTempUnit;
				bUpgradeAvailable = true;
			}
			else bUpgradeUnavailable = true;
		}
	}

	if (iUpgradeCount > 0)
	{
		if (bUpgradeFound && bUpgradeAvailable)
		{
			FAssert(eUpgradeUnit != NO_UNIT);
			return eUpgradeUnit;
		}
		if(canTrain(eUnit, false, false, false, true, /* advc.001b: */ false,
			eAssumeAvailable)) // advc.001u
		{
			return eUnit;
		}
	}
	else if (bUpgradeFound && !bUpgradeUnavailable)
		return eUpgradeUnit;

	return NO_UNIT;
}

// <advc.001b>
bool CvCity::canUpgradeTo(UnitTypes eUnit) const
{
	return canTrain(eUnit, false, false, true, false, false);
}// </advc.001b>

bool CvCity::isWorldWondersMaxed() const
{
	if (GET_PLAYER(getOwner()).isOneCityChallenge())
		return false;
	if (GC.getDefineINT(CvGlobals::MAX_WORLD_WONDERS_PER_CITY) == -1)
		return false;
	if (getNumWorldWonders() >= GC.getDefineINT(CvGlobals::MAX_WORLD_WONDERS_PER_CITY))
		return true;

    // doc: culture level determines wonder limit
    int iWonderLimit = GC.getInfo(getCultureLevel()).getWonderLimit();
    if (isCapital())
        iWonderLimit++;

    if (getNumActiveWorldWonders() >= iWonderLimit)
        return true;

	return false;
}


bool CvCity::isTeamWondersMaxed() const
{
	if (GET_PLAYER(getOwner()).isOneCityChallenge())
		return false;
	if (GC.getDefineINT(CvGlobals::MAX_TEAM_WONDERS_PER_CITY) == -1)
		return false;
	if (getNumTeamWonders() >= GC.getDefineINT(CvGlobals::MAX_TEAM_WONDERS_PER_CITY))
		return true;
	return false;
}


bool CvCity::isNationalWondersMaxed() const
{	// <advc.004w>
	int iLeft = getNumNationalWondersLeft();
	if(iLeft < 0)
		return false;
	return (iLeft == 0);
	// Moved the remainder of this function into getNumNationalWondersLeft
}

int CvCity::getNumNationalWondersLeft() const
{
    // doc: disable static national wonder limit
	/*int iMaxNumWonders = (GET_PLAYER(getOwner()).isOneCityChallenge() ?
			GC.getDefineINT(CvGlobals::MAX_NATIONAL_WONDERS_PER_CITY_FOR_OCC) :
			GC.getDefineINT(CvGlobals::MAX_NATIONAL_WONDERS_PER_CITY));
	if(iMaxNumWonders < 0)
	    return -1;*/

    // doc: culture level determines national wonder limit
    int iNationalWonderLimit = GC.getCultureLevelInfo(getCultureLevel()).getNationalWonderLimit();
    if (iNationalWonderLimit < 0)
        return -1;

	return std::max(0, iNationalWonderLimit - getNumNationalWonders());
} // </advc.004w>


bool CvCity::isBuildingsMaxed() const
{
	// <advc.opt> -1 unless a mod-mod changes it
	static int const iMaxBuildingsPerCity = GC.getDefineINT("MAX_BUILDINGS_PER_CITY");
	if (iMaxBuildingsPerCity < 0)
		return false; // </advc.opt>
	if (GET_PLAYER(getOwner()).isOneCityChallenge())
		return false;
	return (getNumBuildings() >= iMaxBuildingsPerCity);
}

// advc.064d:
void CvCity::verifyProduction()
{
	if(isProduction()) // Only want to address invalid orders here; no production is OK.
	{
		/*  This doesn't check all preconditions, just the ones that could change
			throughout a (human) turn. Don't want the AI to choose a new order
			b/c it might be another civ's turn, and, in that case,
			CvPlayerAI::AI_chooseProduction isn't guaranteed to work correctly. */
		checkCanContinueProduction(true, HUMAN_CHOOSE);
	}
}


bool CvCity::canTrain(UnitTypes eUnit, bool bContinue, bool bTestVisible, bool bIgnoreCost, bool bIgnoreUpgrades,
	bool bCheckAirUnitCap, // advc.001b
	BonusTypes eAssumeAvailable) const // advc.001u
{
	//PROFILE_FUNC(); // advc.003o
	FAssert(eUnit != NO_UNIT); // advc

	if (GC.getPythonCaller()->canTrainOverride(
		*this, eUnit, bContinue,  bTestVisible, bIgnoreCost, bIgnoreUpgrades))
	{
		return true;
	}

	if(!GET_PLAYER(getOwner()).canTrain(eUnit, bContinue, bTestVisible, bIgnoreCost))
		return false;

	if(!getPlot().canTrain(eUnit, bContinue, bTestVisible, /* advc.001b: */ bCheckAirUnitCap,
		eAssumeAvailable)) // advc.001u
	{
		return false;
	}
	// advc.opt: Moved down. Seems a bit slower than CvPlot::canTrain.
	if (!bIgnoreUpgrades)
	{
		if (allUpgradesAvailable(eUnit) != NO_UNIT)
			return false;
	}

	if (GC.getPythonCaller()->cannotTrainOverride(
		*this, eUnit, bContinue, bTestVisible, bIgnoreCost, bIgnoreUpgrades))
	{
		return false;
	}

    // doc: Exploration is required to train settlers in colonies
    if (GC.getUnitInfo(eUnit).isFound())
    {
		if (isColony() && !GET_TEAM(getTeam()).isHasTech(EXPLORATION))
			return false;
    }

    // doc: cannot train slaves
    // TODO: refactor
    if (GC.getUnitInfo(eUnit).isSlave())
    {
        return false;
    }

	return true;
}

bool CvCity::canTrain(UnitCombatTypes eUnitCombat) const
{
	CvCivilization const& kCiv = getCivilization();
	for (int i = 0; i < kCiv.getNumUnits(); i++)
	{
		UnitTypes eUnit = kCiv.unitAt(i);
		if (GC.getInfo(eUnit).getUnitCombatType() == eUnitCombat &&
			canTrain(eUnit))
		{
			return true;
		}
	}
	return false;
}

// advc: Refactored
bool CvCity::canConstruct(BuildingTypes eBuilding, bool bContinue,
	bool bTestVisible, bool bIgnoreCost, bool bIgnoreTech) const
{
	FAssert(eBuilding != NO_BUILDING); // advc

	if (GC.getPythonCaller()->canConstructOverride(
		*this, eBuilding, bContinue, bTestVisible, bIgnoreCost))
	{
		return true;
	}
	if(!GET_PLAYER(getOwner()).canConstruct(eBuilding, bContinue, bTestVisible, bIgnoreCost, bIgnoreTech))
		return false;

	if (getNumBuilding(eBuilding) >= GC.getDefineINT(CvGlobals::CITY_MAX_NUM_BUILDINGS))
		return false;

	CvBuildingInfo const& kBuilding = GC.getInfo(eBuilding);

    // doc: pagan buildings require no religions in the city
    if (kBuilding.isPagan())
    {
        if (GET_PLAYER(getOwner()).getStateReligion() != NO_RELIGION)
            return false;
        if (getReligionCount() > 1)
            return false;
        if (getReligionCount() == 1 && isHasReligion(JUDAISM))
            return false;
    }

	if (kBuilding.isPrereqReligion() && //getReligionCount() > 0
		getReligionCount() <= 0) // K-Mod (bugfix)
	{
		return false;
	}
	{
        // doc: alternative religion requirements
		ReligionTypes ePrereqReligion = kBuilding.getPrereqReligion();
        ReligionTypes ePrereqOrReligion = kBuilding.getPrereqOrReligion();
        bool bPrereqReligion = ePrereqReligion == NO_RELIGION || isHasReligion(ePrereqReligion);
        bool bPrereqOrReligion = ePrereqOrReligion != NO_RELIGION && isHasReligion(ePrereqOrReligion);
		if (!bPrereqReligion && !bPrereqOrReligion)
			return false;
	}
	if (kBuilding.isStateReligion())
	{
		ReligionTypes eStateReligion = GET_PLAYER(getOwner()).getStateReligion();
		if(eStateReligion == NO_RELIGION || !isHasReligion(eStateReligion))
			return false;
	}
	{
		CorporationTypes ePrereqCorp = kBuilding.getPrereqCorporation();
		if (ePrereqCorp != NO_CORPORATION)
		{
			if(!isHasCorporation(ePrereqCorp))
				return false;
		}
	}

	CorporationTypes eFoundCorp = kBuilding.getFoundsCorporation();
	if (eFoundCorp != NO_CORPORATION)
	{
		FOR_EACH_ENUM(Corporation)
		{
			if (isHeadquarters(eLoopCorporation) &&
				GC.getGame().isCompetingCorporation(eLoopCorporation, eFoundCorp))
			{
				return false;
			}
		}
	}
	if (!getPlot().canConstruct(eBuilding))
		return false;

	if (kBuilding.isGovernmentCenter() && isGovernmentCenter())
		return false;

	// doc: Moai Statues require 20 water tiles
	if (eBuilding == MOAI_STATUES)
	{
		int iNumWaterTiles = 0;
		for (CityPlotIter it(*this); it.hasNext(); ++it)
		{
			if (it->isWater()) iNumWaterTiles++;
		}

		if (iNumWaterTiles < 20) return false;
	}

	// doc: Guadalupe Basilica needs to be on different continent than Catholic holy city
    if (eBuilding == GUADALUPE_BASILICA)
	{
		CvCity* pHolyCity = GC.getGame().getHolyCity(CATHOLICISM);
		if (pHolyCity == NULL)
			return false;
		if (sameArea(*pHolyCity))
			return false;
		if (getRegionID() == REGION_SCANDINAVIA)
			return false;
	}

	// doc: Lotus Temple needs four religions
	if (eBuilding == LOTUS_TEMPLE)
	{
		if (getReligionCount() < 4)
			return false;
	}

	// doc: Global Seed Vault requires tundra
	if (eBuilding == GLOBAL_SEED_VAULT)
	{
		bool bFound = false;
		for (CityPlotIter it(*this); it.hasNext() && !bFound; ++it)
		{
			if (it->getTerrainType() == TERRAIN_TUNDRA) bFound = true;
		}

		if (!bFound)
			return false;
	}

	// doc: Burj Khalifa requires ten desert tiles
	if (eBuilding == BURJ_KHALIFA)
	{
		int iNumDesertTiles = 0;
		for (CityPlotIter it(*this); it.hasNext(); ++it)
		{
			switch (it->getTerrainType())
			{
			case TERRAIN_DESERT:
			case TERRAIN_SEMIDESERT:
			case TERRAIN_SALTFLAT:
				iNumDesertTiles++;
			}
		}

		if (iNumDesertTiles < 10)
			return false;
	}

	// doc: Delta Works requires only flatland
	if (eBuilding == DELTA_WORKS)
	{
		for (CityPlotIter it(*this); it.hasNext(); ++it)
		{
			if (it->isHills() || it->isPeak())
				return false;
		}
	}

	// doc: Al Khazneh requires Oasis in city radius
	if (eBuilding == AL_KHAZNEH)
	{
		bool bFound = false;
		for (CityPlotIter it(*this); it.hasNext() && !bFound; ++it)
		{
			if (it->getFeatureType() == FEATURE_OASIS) bFound = true;
		}

		if (!bFound)
			return false;
	}

	// doc: Machu Picchu and Mole Antonelliana require peaks
	if (eBuilding == MACHU_PICCHU || eBuilding == MOLE_ANTONELLIANA)
	{
		bool bFound = false;
		for (CityPlotIter it(*this); it.hasNext() && !bFound; ++it)
		{
			if (it->isPeak()) bFound = true;
		}

		if (!bFound)
			return false;
	}

	if (!bTestVisible)
	{
		if (!bContinue && getFirstBuildingOrder(eBuilding) != -1)
			return false;

		BuildingClassTypes eBuildingClass = (BuildingClassTypes)kBuilding.getBuildingClassType();
		CvBuildingClassInfo const& kBuildingClass = GC.getInfo(eBuildingClass);
		if (!kBuildingClass.isNoLimit())
		{
            // doc: buildable wonders only
			if (kBuildingClass.isWorldWonder() && kBuilding.getProductionCost() > 0)
			{
				if(isWorldWondersMaxed())
					return false;
			}
			else if (kBuildingClass.isTeamWonder())
			{
				if(isTeamWondersMaxed())
					return false;
			}
			else if (kBuildingClass.isNationalWonder())
			{
				if(isNationalWondersMaxed())
					return false;
			}
			else if(isBuildingsMaxed())
				return false;
		}
		{
			ReligionTypes eHolyCityReligion = kBuilding.getHolyCity();
			if (eHolyCityReligion != NO_RELIGION && !isHolyCity(eHolyCityReligion))
				return false;
		}
		if (kBuilding.getPrereqAndBonus() != NO_BONUS &&
			!hasBonus(kBuilding.getPrereqAndBonus()))
		{
			return false;
		}
		if (eFoundCorp != NO_CORPORATION)
		{
			bool bValidBonus = false;
			for (int i = 0; i < GC.getInfo(eFoundCorp).getNumPrereqBonuses(); i++)
			{
				if (hasBonus(GC.getInfo(eFoundCorp).getPrereqBonus(i)))
				{
					bValidBonus = true;
					break;
				}
			}
			if(!bValidBonus)
				return false;
		}

		if(getPlot().getLatitude() > kBuilding.getMaxLatitude())
			return false;
		if(getPlot().getLatitude() < kBuilding.getMinLatitude())
			return false;
		{
			bool bPrereqBonus = false;
			bool bValidBonus = false;
			for (int i = 0; i < kBuilding.getNumPrereqOrBonuses(); i++)
			{
				bPrereqBonus = true;
				if(hasBonus(kBuilding.getPrereqOrBonuses(i)))
					bValidBonus = true;
			}
			if(bPrereqBonus && !bValidBonus)
				return false;
		}
		FOR_EACH_NON_DEFAULT_KEY(kBuilding.
			isBuildingClassNeededInCity(), BuildingClass)
		{
			/*BuildingTypes ePrereqBuilding = (BuildingTypes)GC.getInfo(getCivilizationType()).getCivilizationBuildings(eLoopBuildingClass);
			if (ePrereqBuilding != NO_BUILDING) {
				if(getNumBuilding(ePrereqBuilding) <= 0)
						//&& (bContinue || (getFirstBuildingOrder(ePrereqBuilding) == -1))) // advc (comment): This was already commented out in Vanilla Civ 4
					return false;
			}*/  // <advc.003w>
			if (getNumBuilding(eLoopBuildingClass) <= 0)
				return false; // </advc.003w>
		}
	}

	if (GC.getPythonCaller()->cannotConstructOverride(
		*this, eBuilding, bContinue, bTestVisible, bIgnoreCost))
	{
		return false;
	}
	return true;
}


bool CvCity::canCreate(ProjectTypes eProject, bool bContinue, bool bTestVisible) const
{
	if (GC.getPythonCaller()->canCreateOverride(*this, eProject, bContinue, bTestVisible))
		return true;
	if (!GET_PLAYER(getOwner()).canCreate(eProject, bContinue, bTestVisible))
		return false;
	if (GC.getPythonCaller()->cannotCreateOverride(*this, eProject, bContinue, bTestVisible))
		return false;
	return true;
}


bool CvCity::canMaintain(ProcessTypes eProcess, bool bContinue) const
{
	if (GC.getPythonCaller()->canMaintainOverride(*this, eProcess, bContinue))
		return true;
	if (!GET_PLAYER(getOwner()).canMaintain(eProcess, bContinue))
		return false;
	if (GC.getPythonCaller()->cannotMaintainOverride(*this, eProcess, bContinue))
		return false;
	return true;
}


bool CvCity::canJoin() const
{
	return true;
}


int CvCity::getFoodTurnsLeft() const
{
	int const iFoodDiff = foodDifference(); // advc.opt
	// <advc.189>
	if (iFoodDiff == 0)
		return MAX_INT;
	if (iFoodDiff < 0) // Turns to starvation
	{
		int iFoodLeft = getFood();
		int iTurnsLeft = intdiv::uceil(iFoodLeft, -iFoodDiff);
		return std::min(-1, -iTurnsLeft);
	} // </advc.189>
	int iFoodLeft = growthThreshold() - getFood();
	/*	<advc> Simplified. I think negative iFoodLeft can happen through
		a random event. */
	if (iFoodLeft < 0)
		return 1;
	int iTurnsLeft = intdiv::uceil(iFoodLeft, iFoodDiff); // </advc>
	return std::max(1, iTurnsLeft);
}


bool CvCity::isProductionLimited() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();
	if (pOrderNode != NULL)
	{
		switch (pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
			return GC.getInfo((UnitTypes)pOrderNode->m_data.iData1).isLimited();
			break;

		case ORDER_CONSTRUCT:
			return GC.getInfo((BuildingTypes)pOrderNode->m_data.iData1).isLimited();
			break;

		case ORDER_CREATE:
			return GC.getInfo((ProjectTypes)pOrderNode->m_data.iData1).isLimited();
			break;

		case ORDER_MAINTAIN:
			break;

		default:
			FErrorMsg("pOrderNode->m_data.eOrderType failed to match a valid option");
		}
	}
	return false;
}


bool CvCity::isProductionUnit() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();
	if (pOrderNode != NULL)
		return (pOrderNode->m_data.eOrderType == ORDER_TRAIN);
	return false;
}


bool CvCity::isProductionBuilding() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();
	if (pOrderNode != NULL)
		return (pOrderNode->m_data.eOrderType == ORDER_CONSTRUCT);
	return false;
}


bool CvCity::isProductionProject() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();
	if (pOrderNode != NULL)
		return (pOrderNode->m_data.eOrderType == ORDER_CREATE);
	return false;
}


bool CvCity::isProductionProcess() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();
	if (pOrderNode != NULL)
		return (pOrderNode->m_data.eOrderType == ORDER_MAINTAIN);
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
		FErrorMsg("order.eOrderType failed to match a valid option");
	}
	return false;
}


int CvCity::getProductionExperience(UnitTypes eUnit, /* <advc.002f> */
	bool bScore) const
{
	FAssert(!bScore || eUnit == NO_UNIT); // </advc.002f>
	CvPlayer const& kOwner = GET_PLAYER(getOwner());
	int iExperience = getFreeExperience();
	iExperience += kOwner.getFreeExperience();
	iExperience += getSpecialistFreeExperience(); // K-Mod (moved from below)
	if (kOwner.getStateReligion() != NO_RELIGION)
	{
		if (isHasReligion(kOwner.getStateReligion()))
			iExperience += kOwner.getStateReligionFreeExperience();
	}
	if (eUnit != NO_UNIT)
	{
		if (GC.getInfo(eUnit).getUnitCombatType() != NO_UNITCOMBAT)
		{
			iExperience += getUnitCombatFreeExperience((UnitCombatTypes)
					GC.getInfo(eUnit).getUnitCombatType());
		}
		iExperience += getDomainFreeExperience(GC.getInfo(eUnit).getDomainType());
		//iExperience += getSpecialistFreeExperience();

	    // doc: domain specific experience from civics
	    if (GC.getInfo(eUnit).getDomainType() != NO_DOMAIN)
	    {
	        iExperience += GET_PLAYER(getOwner()).getDomainFreeExperience(GC.getInfo(eUnit).getDomainType());
	    }

	    // doc: Chapultepec Castle
	    if (GC.getInfo(eUnit).getCombat() > 0 && isHasBuildingEffect(CHAPULTEPEC_CASTLE))
	        iExperience += getCultureLevel();

	    // SuperSpies: TSHEEP - Only give spies spy specific xp
	    if (GC.getUnitInfo(eUnit).isSpy())
	    {
	        iExperience = 0;

	        if (GC.getInfo(eUnit).getUnitCombatType() != NO_UNITCOMBAT)
	        {
	            iExperience += getUnitCombatFreeExperience(GC.getInfo(eUnit).getUnitCombatType());
	        }
	    }
	}
	// <advc.002f> AI score for comparing cities wrt. their free XP
	else if (bScore)
	{
		int iNonGenericXP = 0;
		FOR_EACH_ENUM(UnitCombat)
			iNonGenericXP += getUnitCombatFreeExperience(eLoopUnitCombat);
		FOR_EACH_ENUM(Domain)
			iNonGenericXP += getDomainFreeExperience(eLoopDomain);
		iExperience += iExperience + (iNonGenericXP + 1) / 2;
	} // </advc.002f>
	return std::max(0, iExperience);
}


void CvCity::addProductionExperience(CvUnit* pUnit, bool bConscript)
{
	if (pUnit->canAcquirePromotionAny())
	{
		pUnit->changeExperience(getProductionExperience(pUnit->getUnitType()) /
				(bConscript ? 2 : 1));
	}
	if (isAnyFreePromotion()) // advc.opt
	{
		FOR_EACH_ENUM(Promotion)
		{
			if (isFreePromotion(eLoopPromotion))
			{
				if (pUnit->getUnitCombatType() != NO_UNITCOMBAT &&
					GC.getInfo(eLoopPromotion).getUnitCombat(pUnit->getUnitCombatType()))
				{
					pUnit->setHasPromotion(eLoopPromotion, true);
				}
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
			FErrorMsg("pOrderNode->m_data.eOrderType failed to match a valid option");
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
		case ORDER_CONSTRUCT:
		case ORDER_CREATE:
		case ORDER_MAINTAIN:
			break;
		default:
			FErrorMsg("pOrderNode->m_data.eOrderType failed to match a valid option");
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
		case ORDER_CREATE:
		case ORDER_MAINTAIN:
			break;
		default:
			FErrorMsg("pOrderNode->m_data.eOrderType failed to match a valid option");
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
		case ORDER_MAINTAIN:
			break;
		default:
			FErrorMsg("pOrderNode->m_data.eOrderType failed to match a valid option");
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
		default:
			FErrorMsg("pOrderNode->m_data.eOrderType failed to match a valid option");
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
			return GC.getInfo((UnitTypes) pOrderNode->m_data.iData1).getDescription();
		case ORDER_CONSTRUCT:
			return GC.getInfo((BuildingTypes) pOrderNode->m_data.iData1).getDescription();
		case ORDER_CREATE:
			return GC.getInfo((ProjectTypes) pOrderNode->m_data.iData1).getDescription();
		case ORDER_MAINTAIN:
			return GC.getInfo((ProcessTypes) pOrderNode->m_data.iData1).getDescription();
		default:
			FErrorMsg("pOrderNode->m_data.eOrderType failed to match a valid option");
		}
	}
	return L"";
}


const wchar* CvCity::getProductionNameKey() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();
	if (pOrderNode != NULL)
	{
		switch (pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
			return GC.getInfo((UnitTypes) pOrderNode->m_data.iData1).getTextKeyWide();
		case ORDER_CONSTRUCT:
			return GC.getInfo((BuildingTypes) pOrderNode->m_data.iData1).getTextKeyWide();
		case ORDER_CREATE:
			return GC.getInfo((ProjectTypes) pOrderNode->m_data.iData1).getTextKeyWide();
		case ORDER_MAINTAIN:
			return GC.getInfo((ProcessTypes) pOrderNode->m_data.iData1).getTextKeyWide();
		default:
			FErrorMsg("pOrderNode->m_data.eOrderType failed to match a valid option");
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
			FErrorMsg("pOrderNode->m_data.eOrderType failed to match a valid option");
			break;
		}
	}

	return false;
}


bool CvCity::isFoodProduction(UnitTypes eUnit) const
{
	if (GC.getInfo(eUnit).isFoodProduction())
		return true;
	if (GET_PLAYER(getOwner()).isMilitaryFoodProduction())
	{
		if (GC.getInfo(eUnit).isMilitaryProduction())
			return true;
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
				return iCount;
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
				return iCount;
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
				return iCount;
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
				iCount++;
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
		case ORDER_CONSTRUCT:
			return getBuildingProduction((BuildingTypes)(pOrderNode->m_data.iData1));
		case ORDER_CREATE:
			return getProjectProduction((ProjectTypes)(pOrderNode->m_data.iData1));
		case ORDER_MAINTAIN:
			break;
		default:
			FErrorMsg("pOrderNode->m_data.eOrderType failed to match a valid option");
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
		case ORDER_CONSTRUCT:
			return getProductionNeeded((BuildingTypes)(pOrderNode->m_data.iData1));
		case ORDER_CREATE:
			return getProductionNeeded((ProjectTypes)(pOrderNode->m_data.iData1));
		case ORDER_MAINTAIN:
			break;
		default:
			FErrorMsg("pOrderNode->m_data.eOrderType failed to match a valid option");
		}
	}
	return MAX_INT;
}

int CvCity::getProductionNeeded(UnitTypes eUnit) const
{
	return GET_PLAYER(getOwner()).getProductionNeeded(eUnit);
}


int CvCity::getProductionNeeded(BuildingTypes eBuilding) const
{
	int iProductionNeeded = GET_PLAYER(getOwner()).getProductionNeeded(eBuilding);
	int iPythonModifier = GC.getPythonCaller()->buildingCostMod(*this, eBuilding);
	if (iPythonModifier > 1)
	{
		iProductionNeeded *= iPythonModifier;
		iProductionNeeded /= 100;
	}
	return iProductionNeeded;
}

int CvCity::getProductionNeeded(ProjectTypes eProject) const
{
	return GET_PLAYER(getOwner()).getProductionNeeded(eProject);
}

/*  advc: Deleted. Did exactly the same thing as getProductionTurnsLeft below
	except returning 0 instead of MAX_INT for processes. Was unused in the DLL.
	Python export still in place (see CyCity.cpp). */
/*int CvCity::getGeneralProductionTurnsLeft() const {
	// ...
	return 0;
} */


int CvCity::getProductionTurnsLeft() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();
	if (pOrderNode != NULL)
	{
		int iData = pOrderNode->m_data.iData1;
		switch (pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
			return getProductionTurnsLeft((UnitTypes)iData, 0);
		case ORDER_CONSTRUCT:
			return getProductionTurnsLeft((BuildingTypes)iData, 0);
		case ORDER_CREATE:
			return getProductionTurnsLeft((ProjectTypes)iData, 0);
		case ORDER_MAINTAIN:
			break;
		default: FErrorMsg("Unknown order type");
		}
	}
	return MAX_INT;
}


int CvCity::getProductionTurnsLeft(UnitTypes eUnit, int iNum) const
{
	int iProduction = 0;
	int iFirstUnitOrder = getFirstUnitOrder(eUnit);
	if (iFirstUnitOrder == -1 || iFirstUnitOrder == iNum)
		iProduction += getUnitProduction(eUnit);

	int iProductionNeeded = getProductionNeeded(eUnit);
	int iProductionModifier = getProductionModifier(eUnit);
	// advc.064b: Moved into (yet another) auxiliary function
	return getProductionTurnsLeft(iProductionNeeded, iProduction,
			iProductionModifier, isFoodProduction(eUnit), iNum);
}


int CvCity::getProductionTurnsLeft(BuildingTypes eBuilding, int iNum) const
{
	int iProduction = 0;
	int iFirstBuildingOrder = getFirstBuildingOrder(eBuilding);
	if (iFirstBuildingOrder == -1 || iFirstBuildingOrder == iNum)
		iProduction += getBuildingProduction(eBuilding);

	int iProductionNeeded = getProductionNeeded(eBuilding);
	int iProductionModifier = getProductionModifier(eBuilding);
	// advc.064b:
	return getProductionTurnsLeft(iProductionNeeded, iProduction,
			iProductionModifier, false, iNum);
}


int CvCity::getProductionTurnsLeft(ProjectTypes eProject, int iNum) const
{
	int iProduction = 0;
	int iFirstProjectOrder = getFirstProjectOrder(eProject);
	if (iFirstProjectOrder == -1 || iFirstProjectOrder == iNum)
		iProduction += getProjectProduction(eProject);

	int iProductionNeeded = getProductionNeeded(eProject);
	int iProductionModifier = getProductionModifier(eProject);
	// advc.064b:
	return getProductionTurnsLeft(iProductionNeeded, iProduction,
			iProductionModifier, false, iNum);
}

/*  <advc.064b> New auxiliary function; some code cut from
	getProductionTurnsLeft(UnitTypes,int). Added a bit of code to predict
	overflow for queued orders (iNum>0); BtS never did that. */
int CvCity::getProductionTurnsLeft(int iProductionNeeded, int iProduction,
	int iProductionModifier, bool bFoodProduction, int iNum) const
{
	int iFirstProductionDifference = 0;
	// Per-turn production assuming no overflow and feature production
	int iProductionDifference = getProductionDifference(iProductionNeeded,
			iProduction, iProductionModifier, bFoodProduction, false, true);
	if (iNum > 1)
	{
		// Not going to predict overflow here
		iFirstProductionDifference = iProductionDifference;
	}
	else if (iNum == 1 && getProductionTurnsLeft() <= 1)
	{
		// Current production about to finish; predict overflow.
		OrderTypes eCurrentOrder = getOrderData(0).eOrderType;
		if(eCurrentOrder == ORDER_TRAIN || eCurrentOrder == ORDER_CONSTRUCT ||
			eCurrentOrder == ORDER_CREATE)
		{
			int iFeatureProduction = 0;
			int iCurrentProductionDifference = getCurrentProductionDifference(false,
					true, false, false, false, &iFeatureProduction);
			int iRawOverflow = getProduction() + iCurrentProductionDifference
					- getProductionNeeded();
			int iOverflow = computeOverflow(iRawOverflow, getProductionModifier(),
					eCurrentOrder);
			/*  This ignores that some production modifiers are applied to overflow,
				but it's certainly better than ignoring overflow altogether. */
			iFirstProductionDifference = iProductionDifference + iOverflow +
					((getFeatureProduction() - iFeatureProduction) *
					(100 + iProductionModifier)) / 100;
		}
	}
	else if (iNum == 1)
		iFirstProductionDifference = iProductionDifference;
	if (iNum <= 0)
	{
		iFirstProductionDifference = getProductionDifference(iProductionNeeded,
				iProduction, iProductionModifier, bFoodProduction, true, false);
	}
	return getProductionTurnsLeft(iProductionNeeded, iProduction,
			iFirstProductionDifference, iProductionDifference);
} // </advc.064b>

// <advc.064d> Body cut from popOrder
void CvCity::doPopOrder(CLLNode<OrderData>* pOrder)
{
	bool bStart = false;
	if(pOrder == headOrderQueueNode())
	{
		bStart = true;
		stopHeadOrder();
	}
	m_orderQueue.deleteNode(pOrder);
	if(bStart)
		startHeadOrder();
} // </advc.064d>

int CvCity::getProductionTurnsLeft(int iProductionNeeded, int iProduction, int iFirstProductionDifference, int iProductionDifference) const
{
	int iProductionLeft = std::max(0,
			iProductionNeeded - iProduction - iFirstProductionDifference);

	if (iProductionDifference == 0)
	{
		//return iProductionLeft + 1;
		return MAX_INT; // advc.004x
	}
	int iTurnsLeft = (iProductionLeft / iProductionDifference);
	if (iTurnsLeft * iProductionDifference < iProductionLeft)
		iTurnsLeft++; // advc (comment): rounds up

	iTurnsLeft++;

	return std::max(1, iTurnsLeft);
}

// advc.004x:
int CvCity::sanitizeProductionTurns(int iTurns, OrderTypes eOrder, int iData, bool bAssert) const
{
	if(iTurns < MAX_INT)
		return iTurns;
	FAssert(!bAssert);
	int iR = 1;
	switch(eOrder)
	{
	case ORDER_TRAIN: return iR + getProductionNeeded((UnitTypes)iData);
	case ORDER_CONSTRUCT: return iR + getProductionNeeded((BuildingTypes)iData);
	case ORDER_CREATE: return iR + getProductionNeeded((ProjectTypes)iData);
	case ORDER_MAINTAIN: return getProductionNeeded(); // (mustn't add 1 to that)
	default: return iR + getProductionNeeded();
	}
}


void CvCity::setProduction(int iNewValue)
{
	if (isProductionUnit())
		setUnitProduction(getProductionUnit(), iNewValue);
	else if (isProductionBuilding())
		setBuildingProduction(getProductionBuilding(), iNewValue);
	else if (isProductionProject())
		setProjectProduction(getProductionProject(), iNewValue);
	// <advc.004x>
	m_iMostRecentOrder = -1;
	m_bMostRecentUnit = false; // </advc.004x>
}


void CvCity::changeProduction(int iChange)
{
	if (isProductionUnit())
		changeUnitProduction(getProductionUnit(), iChange);
	else if (isProductionBuilding())
		changeBuildingProduction(getProductionBuilding(), iChange);
	else if (isProductionProject())
		changeProjectProduction(getProductionProject(), iChange);
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
		case ORDER_CONSTRUCT:
			return getProductionModifier((BuildingTypes)(pOrderNode->m_data.iData1));
		case ORDER_CREATE:
			return getProductionModifier((ProjectTypes)(pOrderNode->m_data.iData1));
		case ORDER_MAINTAIN:
			break;
		default:
			FErrorMsg("pOrderNode->m_data.eOrderType failed to match a valid option");
		}
	}
	return 0;
}


int CvCity::getProductionModifier(UnitTypes eUnit) const
{
	int iMultiplier = GET_PLAYER(getOwner()).getProductionModifier(eUnit);
	iMultiplier += getDomainProductionModifier((DomainTypes)
			GC.getInfo(eUnit).getDomainType());
	if (GC.getInfo(eUnit).isMilitaryProduction())
		iMultiplier += getMilitaryProductionModifier();

	if (GC.getInfo(eUnit).isAnyBonusProductionModifier()) // advc.003t
	{
		FOR_EACH_ENUM(Bonus)
		{
			if (hasBonus(eLoopBonus))
				iMultiplier += GC.getInfo(eUnit).getBonusProductionModifier(eLoopBonus);
		}
	}
	CvPlayer const& kOwner = GET_PLAYER(getOwner());
	if (kOwner.getStateReligion() != NO_RELIGION)
	{
		if (isHasReligion(kOwner.getStateReligion()))
			iMultiplier += kOwner.getStateReligionUnitProductionModifier();
	}
	//return std::max(0, iMultiplier);
	return std::max(-50, iMultiplier); // UNOFFICIAL_PATCH (for mods), 05/10/10, jdog5000
}


int CvCity::getProductionModifier(BuildingTypes eBuilding, bool bHurry) const
{
	int iMultiplier = GET_PLAYER(getOwner()).getProductionModifier(eBuilding);
	FOR_EACH_NON_DEFAULT_PAIR(GC.getInfo(eBuilding).
		getBonusProductionModifier(), Bonus, int)
	{
		if (hasBonus(perBonusVal.first))
			iMultiplier += perBonusVal.second;
	}
	CvPlayer const& kOwner = GET_PLAYER(getOwner());
	if (kOwner.getStateReligion() != NO_RELIGION)
	{
		if (isHasReligion(kOwner.getStateReligion()))
        {
            // doc: does not apply to world wonders
            if (!GC.getInfo(eBuilding).isWorldWonder())
            {
    			iMultiplier += kOwner.getStateReligionBuildingProductionModifier();
            }
        }
	}
	// return std::max(0, iMultiplier);
	return std::max(-50, iMultiplier); // UNOFFICIAL_PATCH (for mods), 05/10/10, jdog5000
}


int CvCity::getProductionModifier(ProjectTypes eProject) const
{
	int iMultiplier = GET_PLAYER(getOwner()).getProductionModifier(eProject);
	if (GC.getInfo(eProject).isSpaceship())
		iMultiplier += getSpaceProductionModifier();

	FOR_EACH_NON_DEFAULT_PAIR(GC.getInfo(eProject).
		getBonusProductionModifier(), Bonus, int)
	{
		if (hasBonus(perBonusVal.first))
			iMultiplier += perBonusVal.second;
	}
	// return std::max(0, iMultiplier);
	return std::max(-50, iMultiplier); // UNOFFICIAL_PATCH (for mods), 05/10/10, jdog5000
}


int CvCity::getProductionDifference(int iProductionNeeded, int iProduction,
	int iProductionModifier, bool bFoodProduction, bool bOverflow,  // <advc.064bc>
	bool bIgnoreFeatureProd, bool bIgnoreYieldRate,
	bool bForceFeatureProd, int* piFeatureProd) const // </advc.064bc>
{
	if (isDisorder() /* advc.004x: */ && !bForceFeatureProd)
		return 0;

	int iFoodProduction = (bFoodProduction ?
			std::max(0, (getYieldRate(YIELD_FOOD) - foodConsumption(
			/* advc.001 (K-Mod bug): */ true))
            // doc: civic food production modifier
            * (100 + GET_PLAYER(getOwner()).getFoodProductionModifier()) / 100) : 0);

	int iModifier = getBaseYieldRateModifier(YIELD_PRODUCTION, iProductionModifier);
	int iRate = /* advc.064: */ (bIgnoreYieldRate ? 0 :
			getBaseYieldRate(YIELD_PRODUCTION));
	//int iOverflow = (bOverflow ? (getOverflowProduction() + getFeatureProduction()) : 0);
	// <advc.064b> Replacing the above
	int iOverflow = 0;
	if (bOverflow)
		iOverflow = getOverflowProduction();
	int iFeatureProduction = 0;
	FAssert(!bIgnoreFeatureProd || (!bForceFeatureProd && piFeatureProd == NULL));
	if (!bIgnoreFeatureProd)
	{
		if (bForceFeatureProd)
			iFeatureProduction = getFeatureProduction();
		else /* Compute needed feature production (derived from the formula in the
				return statement) */
		{
			// Don't know what to call this; I need it in order to handle rounding.
			int iTmp = 100 * (iProductionNeeded - iProduction - iFoodProduction) -
					iOverflow * (100 + iProductionModifier);
			int iFeatureProdNeeded =  iTmp / iModifier - iRate;
			if(iTmp % iModifier != 0)
				iFeatureProdNeeded++;
			iFeatureProduction = ::range(iFeatureProdNeeded, 0, getFeatureProduction());
		}
	}
	if(piFeatureProd != NULL)
		*piFeatureProd = iFeatureProduction;
	/*  Replacing the BtS formula below. The BaseYieldRateModifier is now already
		applied when the overflow is generated; see comment in unmodifyOverflow. */
	return iFoodProduction +
			((iRate + iFeatureProduction) * iModifier +
			iOverflow * (100 + iProductionModifier)) / 100;
	// </advc.064b>
	//return ((iRate + iOverflow) * iModifier) / 100 + iFoodProduction;
}


int CvCity::getCurrentProductionDifference(bool bIgnoreFood, bool bOverflow,  // <advc.064bc>
	bool bIgnoreFeatureProd, bool bIgnoreYieldRate,
	bool bForceFeatureProd, int* piFeatureProd) const // </advc.064bc>
{
	return getProductionDifference(getProductionNeeded(), getProduction(),
			getProductionModifier(), !bIgnoreFood && isFoodProduction(), bOverflow,
			bIgnoreFeatureProd, bIgnoreYieldRate, bForceFeatureProd, piFeatureProd);
}


bool CvCity::canHurry(HurryTypes eHurry, bool bTestVisible) const
{
	if(!GET_PLAYER(getOwner()).canHurry(eHurry) &&   // advc.912d:
		(GC.getInfo(eHurry).getProductionPerPopulation() <= 0 || !canPopRush()))
	{
		return false;
	}
	if(isDisorder())
		return false;
	// <advc.064b> Add overflow and features
	if(getCurrentProductionDifference(true, true, false, true, true) + getProduction() +
		minPlotProduction() >= /* </advc.064b> */ getProductionNeeded())
	{
		return false;
	}
	// K-Mod. moved this check outside of !bTestVisible.
	if(!isProductionUnit() && !isProductionBuilding())
		return false;
	if(!bTestVisible)
	{
	    // doc: unit specific hurry
	    if (isProductionUnit() && !GC.getInfo(eHurry).isUnits())
	        return false;
	    // doc: building specific hurry
		if (isProductionBuilding() && !GC.getInfo(eHurry).isBuildings())
			return false;
		// <advc.064b> Only the iHurryGold <= 0 check is new
		if (GC.getInfo(eHurry).getGoldPerProduction() > 0)
		{
            // doc: cannot hurry civilian units with gold
			if (isProductionUnit() && !GC.getInfo(getProductionUnit()).isMilitaryProduction())
				return false;

			int iHurryGold = hurryGold(eHurry);
			if(iHurryGold <= 0)
				return false;
			if(GET_PLAYER(getOwner()).getGold() < iHurryGold)
				return false;
		} // </advc.064b>
		if(maxHurryPopulation() < hurryPopulation(eHurry))
			return false;
	}
	return true;
}

/*  advc.003j (comment): Not currently called b/c of a K-Mod change in
	CvCityAI::AI_bestUnitAI. Tbd.: I wonder if karadoc's reasoning ("inaccurate")
	also applies to calls to canHurryBuilding. */
bool CvCity::canHurryUnit(HurryTypes eHurry, UnitTypes eUnit, bool bIgnoreNew) const
{
	if (!GET_PLAYER(getOwner()).canHurry(eHurry) &&   // advc.912d
		(GC.getInfo(eHurry).getProductionPerPopulation() <= 0 || !canPopRush()))
	{
		return false;
	}
	if (isDisorder())
		return false;

    // doc: unit specific hurry
	if (!GC.getInfo(eHurry).isUnits())
		return false;

	if (getUnitProduction(eUnit) >= getProductionNeeded(eUnit))
		return false;

	if (GET_PLAYER(getOwner()).getGold() <
		getHurryGold(eHurry, getHurryCost(false, eUnit, bIgnoreNew)))
	{
		return false;
	}
	if (maxHurryPopulation() <
		getHurryPopulation(eHurry, getHurryCost(true, eUnit, bIgnoreNew)))
	{
		return false;
	}
	return true;
}

bool CvCity::canHurryBuilding(HurryTypes eHurry, BuildingTypes eBuilding, bool bIgnoreNew) const
{
	if (!GET_PLAYER(getOwner()).canHurry(eHurry) &&   // advc.912d
		(GC.getInfo(eHurry).getProductionPerPopulation() <= 0 || !canPopRush()))
	{
		return false;
	}
	if (isDisorder())
		return false;

    // doc: building specific hurry
	if (!GC.getInfo(eHurry).isBuildings())
		return false;

	if (getBuildingProduction(eBuilding) >= getProductionNeeded(eBuilding))
		return false;

	if (GET_PLAYER(getOwner()).getGold() < getHurryGold(eHurry, getHurryCost(false, eBuilding, bIgnoreNew)))
		return false;

	if (maxHurryPopulation() < getHurryPopulation(eHurry, getHurryCost(true, eBuilding, bIgnoreNew)))
		return false;

	return true;
}


void CvCity::hurry(HurryTypes eHurry)
{
	if (!canHurry(eHurry))
		return;

	int iHurryGold = hurryGold(eHurry);
	int iHurryPopulation = hurryPopulation(eHurry);
    int iHurryAngerLength = hurryAngerLength(eHurry);
    // doc: amount of sacrificed population increases hurry anger
    int iHurryAngerModifier = (iHurryPopulation + 1) / 2;

    // doc: track hurry to apply associated effects to unit
    if (isProductionUnit())
    {
        setUnitHurry((UnitClassTypes)GC.getUnitInfo(getProductionUnit()).getUnitClassType(), eHurry);
    }

	changeProduction(hurryProduction(eHurry));
	GET_PLAYER(getOwner()).changeGold(-(iHurryGold));
	changePopulation(-(iHurryPopulation));

    // doc: Russian UP: temporary unhappiness is applied to your happiest city
    CvCity* pHurryAngerCity = this;

    if (getCivilizationType() == RUSSIA)
    {
        FOR_EACH_CITY_VAR(pLoopCity, GET_PLAYER(getOwner()))
        {
            if (pLoopCity->happyLevel() - pLoopCity->unhappyLevel() > pHurryAngerCity->happyLevel() - pHurryAngerCity->unhappyLevel())
            {
                pHurryAngerCity = pLoopCity;
            }
        }
    }

	pHurryAngerCity->changeHurryAngerTimer(iHurryAngerLength * iHurryAngerModifier);

	if (gCityLogLevel >= 2) // BETTER_BTS_AI_MOD, AI logging, 10/02/09, jdog5000
	{
		CvWStringBuffer szBuffer; CvWString szString;
		if (isProductionUnit())
			szString = GC.getInfo(getProductionUnit()).getDescription();
		else if (isProductionBuilding())
			szString = GC.getInfo(getProductionBuilding()).getDescription();
		else if (isProductionProject())
			szString = GC.getInfo(getProductionProject()).getDescription();
		logBBAI("    City %S hurrying production of %S at cost of %d pop, %d gold, %d anger length", getName().GetCString(), szString.GetCString(), iHurryPopulation, iHurryGold, iHurryAngerLength);
	}

	if (isActiveOwned() && isCitySelected())
		gDLL->UI().setDirty(SelectionButtons_DIRTY_BIT, true);

	CvEventReporter::getInstance().cityHurry(this, eHurry);
}

// <advc.064b>
int CvCity::overflowCapacity(int iProductionModifier, int iPopulationChange) const
{
	int iBound1 = getCurrentProductionDifference(false, false, true); // as in BtS/K-Mod
	// New: Take out build-specific modifiers
	iBound1 = unmodifyOverflow(iBound1, iProductionModifier);
	// Was the production cost of the completed order in BtS/K-Mod
	int iBound2 = growthThreshold(iPopulationChange, true);
	return std::max(iBound1, iBound2);
}

// Based on code (BtS/unoffical patch) cut from popOrder
int CvCity::computeOverflow(int iRawOverflow, int iProductionModifier,
	OrderTypes eOrderType, int* piProductionGold, int* piLostProduction,
	int iPopulationChange) const
{
	LOCAL_REF(int, iProductionGold, piProductionGold, 0);
	LOCAL_REF(int, iLostProduction, piLostProduction, 0);
	/*  (BtS and the unofficial patch cap overflow before factoring out the modifiers.
		However, they also apply generic production modifiers to the overflow once
		work on the next order starts, which AdvCiv no longer does.) */
	int iOverflow = unmodifyOverflow(iRawOverflow, iProductionModifier);
	int iMaxOverflow = overflowCapacity(iProductionModifier, iPopulationChange);
	iLostProduction = iOverflow - iMaxOverflow;
	iOverflow = std::min(iMaxOverflow, iOverflow);
	if (iLostProduction <= 0)
		return iOverflow;
	iProductionGold = (iLostProduction * failGoldPercent(eOrderType)) / 100;
	return iOverflow;
} // </advc.064b>

// BUG - Hurry Overflow: (advc.064)
bool CvCity::hurryOverflow(HurryTypes eHurry, int* piProduction, int* piGold, bool bCountThisTurn) const
{
	LOCAL_REF(int, iProduction, piProduction, 0);
	LOCAL_REF(int, iGold, piGold, 0);

	if (!canHurry(eHurry))
		return false;

	if (GC.getInfo(eHurry).getProductionPerPopulation() == 0)
		return true;

	int iTotal, iCurrent, iModifier;
	OrderTypes eOrder = NO_ORDER; // advc.064b
	if (isProductionUnit())
	{
		UnitTypes eUnit = getProductionUnit();
		iTotal = getProductionNeeded(eUnit);
		iCurrent = getUnitProduction(eUnit);
		iModifier = getProductionModifier(eUnit);
		eOrder = ORDER_TRAIN;
	}
	else if (isProductionBuilding())
	{
		BuildingTypes eBuilding = getProductionBuilding();
		iTotal = getProductionNeeded(eBuilding);
		iCurrent = getBuildingProduction(eBuilding);
		iModifier = getProductionModifier(eBuilding);
		eOrder = ORDER_CONSTRUCT;
	}
	else if (isProductionProject())
	{
		ProjectTypes eProject = getProductionProject();
		iTotal = getProductionNeeded(eProject);
		iCurrent = getProjectProduction(eProject);
		iModifier = getProductionModifier(eProject);
		eOrder = ORDER_CREATE;
	}
	else return false;
	int iHurry = hurryProduction(eHurry);
	// <advc.064b>
	int iRawOverflow = iCurrent + iHurry - iTotal +
			/*  BUG ignores chops and previous overflow if !bCountThisTurn, but these
				are entirely predictable, so they shouldn't depend on the "this turn"
				option. However: Feature production can no longer contribute to
				overflow, so ignore that in any case. */
			getCurrentProductionDifference(!bCountThisTurn, true, true, !bCountThisTurn);
	iProduction = computeOverflow(iRawOverflow, iModifier, eOrder, piGold, NULL,
			-hurryPopulation(eHurry)); // </advc.064b>
	return true;
}

// <advc.912d>
bool CvCity::canPopRush() const
{
	return (m_iPopRushHurryCount > 0 || GET_PLAYER(getOwner()).canPopRush());
}

void CvCity::changePopRushCount(int iChange)
{
	m_iPopRushHurryCount += iChange;
} // </advc.912d>


UnitTypes CvCity::getConscriptUnit() const
{
	int iBestValue = 0;
	UnitTypes eBestUnit = NO_UNIT;
	CvCivilization const& kCiv = getCivilization();
	for (int i = 0; i < kCiv.getNumUnits(); i++)
	{
		UnitTypes eLoopUnit = kCiv.unitAt(i);
		if (canTrain(eLoopUnit))
		{
			int iValue = GC.getInfo(eLoopUnit).getConscriptionValue();
			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				eBestUnit = eLoopUnit;
			}
		}
	}

	UnitTypes ePythonUnit = GC.getPythonCaller()->conscriptUnitOverride(getOwner());
	if (ePythonUnit != NO_UNIT)
		eBestUnit = ePythonUnit;

	return eBestUnit;
}


int CvCity::getConscriptPopulation() const
{
	UnitTypes eConscriptUnit = getConscriptUnit();
	if (eConscriptUnit == NO_UNIT)
		return 0;

	if (GC.getDefineINT(CvGlobals::CONSCRIPT_POPULATION_PER_COST) == 0)
		return 0;

	return std::max(1, ((GC.getInfo(eConscriptUnit).getProductionCost()) /
			GC.getDefineINT(CvGlobals::CONSCRIPT_POPULATION_PER_COST)));
}


int CvCity::conscriptMinCityPopulation() const
{
	static int const iCONSCRIPT_MIN_CITY_POPULATION = GC.getDefineINT("CONSCRIPT_MIN_CITY_POPULATION"); // advc.opt
	return getConscriptPopulation() + iCONSCRIPT_MIN_CITY_POPULATION;
}


int CvCity::flatConscriptAngerLength() const
{
	static int const iConscriptAngerDivisor = GC.getDefineINT("CONSCRIPT_ANGER_DIVISOR"); // advc.opt
	int iAnger = iConscriptAngerDivisor;
	iAnger *= GC.getInfo(GC.getGame().getGameSpeedType()).getHurryConscriptAngerPercent();
	iAnger /= 100;

	return std::max(1, iAnger);
}


bool CvCity::canConscript(bool bForce) const
{
	if (isDisorder())
		return false;

	if (isDrafted())
		return false;

	if (getPopulation() <= getConscriptPopulation())
		return false;

	if (getPopulation() < conscriptMinCityPopulation())
		return false;

	if (getConscriptUnit() == NO_UNIT)
	    return false;

    if (bForce)
        return true;

    if (GET_PLAYER(getOwner()).getConscriptCount() >= GET_PLAYER(getOwner()).getMaxConscript())
        return false;

    // doc: Ottoman UP: extra conscript requires non-state religion
    if (getCivilizationType() == OTTOMANS)
    {
        if (GET_PLAYER(getOwner()).getConscriptCount() >= GET_PLAYER(getOwner()).getMaxConscript() - 2)
        {
            if (getReligionCount() == 0)
                return false;

            if (GET_PLAYER(getOwner()).getStateReligion() != NO_RELIGION && isHasReligion(GET_PLAYER(getOwner()).getStateReligion()) && getReligionCount() == 1)
                return false;
        }
    }

    // doc: Ottoman UP: conscript without culture threshold
    if (getCivilizationType() != OTTOMANS)
    {
        static int const iCONSCRIPT_MIN_CULTURE_PERCENT = GC.getDefineINT("CONSCRIPT_MIN_CULTURE_PERCENT"); // advc.opt
        if (getPlot().calculateTeamCulturePercent(getTeam()) < iCONSCRIPT_MIN_CULTURE_PERCENT)
            return false;
    }

	return true;
}

CvUnit* CvCity::initConscriptedUnit()
{
	UnitTypes eConscriptUnit = getConscriptUnit();
	if (eConscriptUnit == NO_UNIT)
		return NULL;

	CvPlayerAI& kOwner = GET_PLAYER(getOwner());

	UnitAITypes eCityAI = NO_UNITAI;
	if (kOwner.AI_unitValue(eConscriptUnit, UNITAI_ATTACK, area()) > 0)
		eCityAI = UNITAI_ATTACK;
	else if (kOwner.AI_unitValue(eConscriptUnit, UNITAI_CITY_DEFENSE, area()) > 0)
		eCityAI = UNITAI_CITY_DEFENSE;
	else if (kOwner.AI_unitValue(eConscriptUnit, UNITAI_CITY_COUNTER, area()) > 0)
		eCityAI = UNITAI_CITY_COUNTER;
	else if (kOwner.AI_unitValue(eConscriptUnit, UNITAI_CITY_SPECIAL, area()) > 0)
		eCityAI = UNITAI_CITY_SPECIAL;
	else eCityAI = NO_UNITAI;

	CvUnit* pUnit = kOwner.initUnit(eConscriptUnit, getX(), getY(), eCityAI);
	FAssertMsg(pUnit != NULL, "Failed to allocate CvUnit object");

	addProductionExperience(pUnit, true);
	pUnit->setMoves(0);
	// K-Mod, 26/Jun/2011: Conscription counts as building the unit
	CvEventReporter::getInstance().unitBuilt(this, pUnit);

	return pUnit;
}


void CvCity::conscript(bool bForce)
{
	if (!canConscript())
		return;

	int const iPopChange = -getConscriptPopulation();
	int const iAngerLength = flatConscriptAngerLength();
	changePopulation(iPopChange);

    // doc: Russian UP: temporary unhappiness is applied to happiest city
    if (!bForce)
    {
        CvCity* pConscriptAngerCity = this;

        if (getCivilizationType() == RUSSIA)
        {
            FOR_EACH_CITY_VAR(pLoopCity, GET_PLAYER(getOwner()))
            {
                if (pLoopCity->happyLevel() - pLoopCity->unhappyLevel() > pConscriptAngerCity->happyLevel() - pConscriptAngerCity->unhappyLevel())
                {
                    pConscriptAngerCity = pLoopCity;
                }
            }
        }

        pConscriptAngerCity->changeConscriptAngerTimer(iAngerLength);
    }

	setDrafted(true);

	GET_PLAYER(getOwner()).changeConscriptCount(1);

	CvUnit* pUnit = initConscriptedUnit();
	FAssert(pUnit != NULL);

	if (pUnit != NULL)
	{
		if (isActiveOwned() &&
			isHuman()) // advc.127, advc.706
		{
			/*	advc.001o: Conscription had caused the main map to black out.
				The true cause of that problem may lie elsewhere, but switching
				these two statements is at least a workaround. */
			gDLL->UI().selectUnit(pUnit, true, false, true);
			gDLL->UI().lookAt(getPlot().getPoint(), CAMERALOOKAT_NORMAL); // K-Mod
		}
		if (gCityLogLevel >= 2 && !isHuman()) logBBAI("      City %S does conscript of a %S at cost of %d pop, %d anger", getName().GetCString(), pUnit->getName().GetCString(), iPopChange, iAngerLength); // BETTER_BTS_AI_MOD, AI logging, 10/02/09, jdog5000
	}
}


int CvCity::getBonusHealth(BonusTypes eBonus) const
{
    // doc: limited bonus effect
	int iHealth = hasBonusEffect(eBonus) ? GC.getInfo(eBonus).getHealth() : 0;
	CvCivilization const& kCiv = getCivilization();
	for (int i = 0; i < kCiv.getNumBuildings(); i++)
	{
		BuildingTypes const eBuilding = kCiv.buildingAt(i);
		iHealth += getNumActiveBuilding(eBuilding) *
				GC.getInfo(eBuilding).getBonusHealthChanges(eBonus);
	}
	return iHealth;
}


int CvCity::getBonusHappiness(BonusTypes eBonus) const
{
    // doc: limited bonus effect
	int iHappiness = hasBonusEffect(eBonus) ? GC.getInfo(eBonus).getHappiness() : 0;
	CvCivilization const& kCiv = getCivilization();
	for (int i = 0; i < kCiv.getNumBuildings(); i++)
	{
		BuildingTypes const eBuilding = kCiv.buildingAt(i);
		iHappiness += getNumActiveBuilding(eBuilding) *
				GC.getInfo(eBuilding).getBonusHappinessChanges(eBonus);
	}
	return iHappiness;
}


int CvCity::getBonusPower(BonusTypes eBonus, bool bDirty) const
{
	int iCount = 0;
	CvCivilization const& kCiv = getCivilization();
	for (int i = 0; i < kCiv.getNumBuildings(); i++)
	{
		BuildingTypes const eBuilding = kCiv.buildingAt(i);
		if (getNumActiveBuilding(eBuilding) > 0 &&
			GC.getInfo(eBuilding).getPowerBonus() == eBonus &&
			GC.getInfo(eBuilding).isDirtyPower() == bDirty)
		{
			iCount += getNumActiveBuilding(eBuilding);
		}
	}
	return iCount;
}


int CvCity::getBonusYieldRateModifier(YieldTypes eYield, BonusTypes eBonus) const
{
	int iModifier = 0;
	CvCivilization const& kCiv = getCivilization();
	for (int i = 0; i < kCiv.getNumBuildings(); i++)
	{
		BuildingTypes const eBuilding = kCiv.buildingAt(i);
		iModifier += getNumActiveBuilding(eBuilding) *
				GC.getInfo(eBuilding).getBonusYieldModifier(eBonus, eYield);
	}
	return iModifier;
}


// doc
int CvCity::getBonusCommerceRateModifier(CommerceTypes eCommerce, BonusTypes eBonus) const
{
	int iModifier = 0;

	FOR_EACH_ENUM(Building)
	{
		iModifier += getNumActiveBuilding(eLoopBuilding) * GC.getInfo(eLoopBuilding).getBonusCommerceModifier(eBonus, eCommerce);
	}

	return iModifier;
}


void CvCity::processBonus(BonusTypes eBonus, int iChange)
{
	CvCivilization const& kCiv = getCivilization();
	{
		int iValue = GC.getInfo(eBonus).getHealth();
		int iGoodValue = std::max(0, iValue);
		int iBadValue = std::min(0, iValue);
		for (int i = 0; i < kCiv.getNumBuildings(); i++)
		{
			BuildingTypes const eBuilding = kCiv.buildingAt(i);
			iValue = GC.getInfo(eBuilding).getBonusHealthChanges(eBonus) *
					getNumActiveBuilding(eBuilding);
			if (iValue >= 0)
				iGoodValue += iValue;
			else iBadValue += iValue;
		}  // <advc.001w>
		if ((iGoodValue != 0 || iBadValue != 0) && isActiveOwned())
		{
			int iHealth = healthRate();
			if((iHealth < 0) != (iHealth + (iGoodValue - iBadValue) * iChange < 0))
				gDLL->UI().setDirty(CityInfo_DIRTY_BIT, true);
		} // </advc.001w>
		changeBonusGoodHealth(iGoodValue * iChange);
		changeBonusBadHealth(iBadValue * iChange);
	}
	{
		int iValue = GC.getInfo(eBonus).getHappiness();
		int iGoodValue = std::max(0, iValue);
		int iBadValue = std::min(0, iValue);
		for (int i = 0; i < kCiv.getNumBuildings(); i++)
		{
			BuildingTypes const eBuilding = kCiv.buildingAt(i);
			iValue = GC.getInfo(eBuilding).getBonusHappinessChanges(eBonus) *
					getNumActiveBuilding(eBuilding);
			if (iValue >= 0)
				iGoodValue += iValue;
			else iBadValue += iValue;
		}  // <advc.001w>
		if ((iGoodValue != 0 || iBadValue != 0) && isActiveOwned())
		{
			int iHappy = happyLevel() - unhappyLevel();
			if((iHappy < 0) != (iHappy + (iGoodValue - iBadValue) * iChange < 0))
				gDLL->UI().setDirty(CityInfo_DIRTY_BIT, true);
		} // </advc.001w>
		changeBonusGoodHappiness(iGoodValue * iChange);
		changeBonusBadHappiness(iBadValue * iChange);
	}

	changePowerCount(getBonusPower(eBonus, true) * iChange, true);
	changePowerCount(getBonusPower(eBonus, false) * iChange, false);

	FOR_EACH_ENUM(Yield)
	{
		changeBonusYieldRateModifier(eLoopYield,
				getBonusYieldRateModifier(eLoopYield, eBonus) * iChange);
	}

    FOR_EACH_ENUM(Commerce)
    {
        changeBonusCommerceRateModifier(eLoopCommerce,
                getBonusCommerceRateModifier(eLoopCommerce, eBonus) * iChange);
    }
}


// doc
// TODO: check overlap with existing code
// TODO: refactor
void CvCity::processBonusEffect(BonusTypes eBonus, int iChange)
{
    int iValue;
    int iGoodValue;
    int iBadValue;

    iValue = GC.getBonusInfo(eBonus).getHealth();
    iGoodValue = std::max(0, iValue);
    iBadValue = std::min(0, iValue);

    changeBonusGoodHealth(iGoodValue * iChange);
    changeBonusBadHealth(iBadValue * iChange);


    iValue = GC.getBonusInfo(eBonus).getHappiness();
    iGoodValue = std::max(0, iValue);
    iBadValue = std::min(0, iValue);

    changeBonusGoodHappiness(iGoodValue * iChange);
    changeBonusBadHappiness(iBadValue * iChange);
}


void CvCity::processBuilding(BuildingTypes eBuilding, int iChange, bool bObsolete)
{
	CvBuildingInfo const& kBuilding = GC.getInfo(eBuilding);
	CvGame const& kGame = GC.getGame();
	CvPlayer& kOwner = GET_PLAYER(getOwner());
	if (!GET_TEAM(getTeam()).isObsoleteBuilding(eBuilding) || bObsolete)
	{
		if (iChange > 0)
		{
			CorporationTypes eCorporation = kBuilding.getFoundsCorporation();
			if (eCorporation != NO_CORPORATION && !kGame.isCorporationFounded(eCorporation))
				setHeadquarters(eCorporation);
		}

		if (kBuilding.getNoBonus() != NO_BONUS)
			changeNoBonusCount(kBuilding.getNoBonus(), iChange);

		if (kBuilding.getFreeBonus() != NO_BONUS)
		{
			changeFreeBonus(kBuilding.getFreeBonus(),
					kGame.getNumFreeBonuses(eBuilding) * iChange);
		}

		if (kBuilding.getFreePromotion() != NO_PROMOTION)
		{
			changeFreePromotionCount(kBuilding.getFreePromotion(), iChange);
		}
		// <advc.912d>
		if (kGame.isOption(GAMEOPTION_NO_SLAVERY) && kOwner.isHuman() &&
			kBuilding.getHurryAngerModifier() < 0)
		{
			changePopRushCount(iChange);
		}
		changeMaxFoodKeptPercent(//kBuilding.getFoodKept() * iChange
				kOwner.getFoodKept(eBuilding) * iChange); // </advc.912d>
		changeEspionageDefenseModifier(kBuilding.getEspionageDefenseModifier() * iChange);
		changeGreatPeopleRateModifier(kBuilding.getGreatPeopleRateModifier() * iChange);
		changeFreeExperience(kBuilding.getFreeExperience() * iChange);
		changeMaxAirlift(kBuilding.getAirlift() * iChange);
		changeAirModifier(kBuilding.getAirModifier() * iChange);
		changeAirUnitCapacity(kBuilding.getAirUnitCapacity() * iChange);
		changeNukeModifier(kBuilding.getNukeModifier() * iChange);
		changeFreeSpecialist(kBuilding.getFreeSpecialist() * iChange);
		changeMaintenanceModifier(kBuilding.getMaintenanceModifier() * iChange);
		changeWarWearinessModifier(kBuilding.getWarWearinessModifier() * iChange);
		changeHurryAngerModifier(kBuilding.getHurryAngerModifier() * iChange);
		changeHealRate(kBuilding.getHealRateChange() * iChange);
		if (kBuilding.getHealth() > 0)
			changeBuildingGoodHealth(kBuilding.getHealth() * iChange);
		else changeBuildingBadHealth(kBuilding.getHealth() * iChange);
		if (kBuilding.getHappiness() > 0)
			changeBuildingGoodHappiness(kBuilding.getHappiness() * iChange);
		else changeBuildingBadHappiness(kBuilding.getHappiness() * iChange);

	    // doc: Indian UP: +1 health from buildings that provide happiness
	    if (getCivilizationType() == INDIA && kBuilding.getHappiness() > 0)
	    {
	        changeBuildingGoodHealth(iChange);
	    }

        if (kBuilding.getReligionType() != NO_RELIGION)
		{
			changeStateReligionHappiness(kBuilding.getReligionType(),
					kBuilding.getStateReligionHappiness() * iChange);
		}
		changeMilitaryProductionModifier(kBuilding.getMilitaryProductionModifier() * iChange);
		changeSpaceProductionModifier(kBuilding.getSpaceProductionModifier() * iChange);
		changeExtraTradeRoutes(kBuilding.getTradeRoutes() * iChange);
		changeTradeRouteModifier(kBuilding.getTradeRouteModifier() * iChange);
		changeForeignTradeRouteModifier(kBuilding.getForeignTradeRouteModifier() * iChange);
		changePowerCount(kBuilding.isPower() ? iChange : 0, kBuilding.isDirtyPower());
		changeGovernmentCenterCount(kBuilding.isGovernmentCenter() ? iChange : 0);
		changeNoUnhappinessCount(kBuilding.isNoUnhappiness() ? iChange : 0);
		//changeNoUnhealthyPopulationCount(kBuilding.isNoUnhealthyPopulation() ? iChange : 0);
		changeUnhealthyPopulationModifier(kBuilding.getUnhealthyPopulationModifier() * iChange); // K-Mod
		changeBuildingOnlyHealthyCount(kBuilding.isBuildingOnlyHealthy() ? iChange : 0);

        // doc: great people rate, happiness, trade routes from culture level
	    changeCultureGreatPeopleRateModifier(GC.getBuildingInfo(eBuilding).getCultureGreatPeopleRateModifier() * iChange);
	    changeCultureHappiness(GC.getBuildingInfo(eBuilding).getCultureHappiness() * iChange);
	    changeCultureTradeRouteModifier(GC.getBuildingInfo(eBuilding).getCultureTradeRouteModifier() * iChange);

	    changeBuildingUnhealthModifier(GC.getBuildingInfo(eBuilding).getBuildingUnhealthModifier() * iChange);

	    if (GC.getBuildingInfo(eBuilding).getCorporationUnhealthModifier() != 0)
	    {
	        changeCorporationUnhealthModifier(GC.getBuildingInfo(eBuilding).getCorporationUnhealthModifier() * iChange);
	        updateCorporationHealth();
	    }

		FOR_EACH_ENUM2(Yield, y)
		{
			changeSeaPlotYield(y, kBuilding.getSeaPlotYieldChange(y) * iChange);
			changeRiverPlotYield(y, kBuilding.getRiverPlotYieldChange(y) * iChange);
            changeFlatRiverPlotYield(y, kBuilding.getFlatRiverPlotYieldChange(y) * iChange);
			changeBaseYieldRate(y, (kBuilding.getYieldChange(y) +
					getBuildingYieldChange(kBuilding.getBuildingClassType(), y)) * iChange);
			changeYieldRateModifier(y, kBuilding.getYieldModifier(y) * iChange);
			changePowerYieldRateModifier(y, kBuilding.getPowerYieldModifier(y) * iChange);
		}

		FOR_EACH_ENUM(Commerce)
		{
			changeCommerceRateModifier(eLoopCommerce,
					kBuilding.getCommerceModifier(eLoopCommerce) * iChange);
			changeCommerceHappinessPer(eLoopCommerce,
					kBuilding.getCommerceHappiness(eLoopCommerce) * iChange);

            // doc: commerce rate modifier from power
            changePowerCommerceRateModifier(eLoopCommerce,
                    kBuilding.getPowerCommerceModifier(eLoopCommerce) * iChange);
            // doc: commerce rate from culture level
            changeCultureCommerceRateModifier(eLoopCommerce,
                    kBuilding.getCultureCommerceModifier(eLoopCommerce) * iChange);
		}
		FOR_EACH_NON_DEFAULT_PAIR(kBuilding.
			getReligionChange(), Religion, int)
		{
			changeReligionInfluence(perReligionVal.first,
					perReligionVal.second * iChange);
		}
		// <advc.enum> Based on code deleted from CvGame::doUpdateCacheOnTurn
		if (kBuilding.getHolyCity() != NO_RELIGION)
			m_aiShrine.add(kBuilding.getReligionType(), iChange); // </advc.enum>
		FOR_EACH_NON_DEFAULT_PAIR(kBuilding.
			getSpecialistCount(), Specialist, int)
		{
			changeMaxSpecialistCount(perSpecialistVal.first,
					perSpecialistVal.second * iChange);
		}
		FOR_EACH_NON_DEFAULT_PAIR(kBuilding.
			getFreeSpecialistCount(), Specialist, int)
		{
			changeFreeSpecialistCount(perSpecialistVal.first,
					perSpecialistVal.second * iChange);
		}
		FOR_EACH_NON_DEFAULT_PAIR(kBuilding.
			getImprovementFreeSpecialist(), Improvement, int)
		{
			changeImprovementFreeSpecialists(perImprovementVal.first,
					perImprovementVal.second * iChange);
		}
		FOR_EACH_ENUM(Bonus)
		{
			if (!hasBonus(eLoopBonus))
				continue;
			int const iBonusHealthChange = kBuilding.getBonusHealthChanges(eLoopBonus);
			if (iBonusHealthChange > 0)
				changeBonusGoodHealth(iChange * iBonusHealthChange);
			else changeBonusBadHealth(iChange * iBonusHealthChange);
			int const iBonusHappyChange = kBuilding.getBonusHappinessChanges(eLoopBonus);
			if (iBonusHappyChange > 0)
				changeBonusGoodHappiness(iChange * iBonusHappyChange);
			else changeBonusBadHappiness(iChange * iBonusHappyChange);
			if (kBuilding.getPowerBonus() == eLoopBonus)
				changePowerCount(iChange, kBuilding.isDirtyPower());
			if (kBuilding.getBonusYieldModifier().isAnyNonDefault()) // advc.opt
			{
				FOR_EACH_ENUM(Yield)
				{
					changeBonusYieldRateModifier(eLoopYield, iChange *
							kBuilding.getBonusYieldModifier(eLoopBonus, eLoopYield));
				}
			}
		    // doc: extra yield from improved bonuses
		    if (kBuilding.getBonusYieldChange().isAnyNonDefault())
            {
                FOR_EACH_ENUM(Yield)
                {
                    changeBonusYield(eLoopBonus, eLoopYield, iChange *
                            kBuilding.getBonusYieldChange(eLoopBonus, eLoopYield));
                }
            }
		}

		FOR_EACH_NON_DEFAULT_PAIR(kBuilding.
			getUnitCombatFreeExperience(), UnitCombat, int)
		{
			changeUnitCombatFreeExperience(perUnitCombatVal.first,
					iChange * perUnitCombatVal.second);
		}

		FOR_EACH_ENUM(Domain)
		{
			changeDomainFreeExperience(eLoopDomain, iChange *
					kBuilding.getDomainFreeExperience(eLoopDomain));
			changeDomainProductionModifier(eLoopDomain, iChange *
					kBuilding.getDomainProductionModifier(eLoopDomain));
		}

		updateExtraBuildingHappiness();
		updateExtraBuildingHealth();

		// doc: Byzantine UP: +1 espionage in capital per 100 gold in treasury and +1 gold per 100 culture in capital
		// TODO: refactor
        if (getCivilizationType() == BYZANTIUM && eBuilding == 0)
		{
			setBuildingCommerceChange((BuildingClassTypes)0, COMMERCE_ESPIONAGE, std::max(0, iChange * GET_PLAYER(getOwner()).getGold() / 100));
			setBuildingCommerceChange((BuildingClassTypes)0, COMMERCE_GOLD, std::max(0, iChange * getCulture(getOwner()) / 100));
		}

		// doc: special wonder effects
		// Pyramids
		if (eBuilding == PYRAMIDS)
		{
			changeBuildingGreatPeopleRateChange(PYRAMIDS, std::max(0, getBonusGoodHappiness() * iChange));
		}

		// Aqua Appia
		if (eBuilding == AQUA_APPIA)
		{
			setBuildingYieldChange(AQUA_APPIA, YIELD_FOOD, std::max(0, getCultureLevel() * iChange));
		}

		// Pyramid of the Sun
		if (eBuilding == PYRAMID_OF_THE_SUN)
		{
			setBuildingGreatPeopleRateChange(PYRAMID_OF_THE_SUN, std::max(0, getSpecialistCount(SPECIALIST_CITIZEN) * 3 * iChange));
		}

		// Mount Athos
		if (eBuilding == MOUNT_ATHOS)
		{
            FOR_EACH_CITY_VAR(pLoopCity, kOwner)
            {
				FOR_EACH_ENUM(Building)
				{
					if (!pLoopCity->isHasRealBuilding(eLoopBuilding))
						continue;
					
					int iGreatPeopleRate = GC.getInfo(eLoopBuilding).getGreatPeopleRateChange();
					if (iGreatPeopleRate > 0)
					{
						pLoopCity->changeBuildingGreatPeopleRateChange(GC.getInfo(eLoopBuilding).getBuildingClassType(), iChange * iGreatPeopleRate);
					}
				}
			}
		}

		// Prambanan
		if (eBuilding == PRAMBANAN)
		{
			setBuildingYieldChange(PRAMBANAN, YIELD_PRODUCTION, std::max(0, getBonusGoodHappiness() * iChange));
		}

		// Louvre
		if (eBuilding == LOUVRE)
		{
			int iWonderCulture = 0;
			FOR_EACH_CITY(pLoopCity, kOwner)
			{
				FOR_EACH_ENUM(Building)
				{
					if (!GC.getInfo(eLoopBuilding).isWorldWonder())
						continue;
					if (!pLoopCity->isHasRealBuilding(eLoopBuilding))
						continue;
					iWonderCulture += 2;
				}
			}

			setBuildingCommerceChange(LOUVRE, COMMERCE_CULTURE, std::max(0, iWonderCulture * iChange));
		}

		// Escorial
		else if (eBuilding == ESCORIAL)
		{
			setBuildingCommerceChange(ESCORIAL, COMMERCE_GOLD, std::max(0, (kOwner.getNumAvailableBonuses(BONUS_SILVER) + kOwner.getNumAvailableBonuses(BONUS_GOLD)) * 2 * iChange));
		}

		// Potala Palace
		else if (eBuilding == POTALA_PALACE)
		{
			int iNumHills = 0;
			for (CityPlotIter it(*this); it.hasNext(); ++it)
			{
				if (it->isHills())
					iNumHills++;
			}

			setBuildingGreatPeopleRateChange(POTALA_PALACE, std::max(0, iNumHills * iChange));
		}

		// Image of the World Square
		else if (eBuilding == IMAGE_OF_THE_WORLD_SQUARE)
		{
			changeExtraTradeRoutes(std::max(-getExtraTradeRoutes(), iChange * getCultureLevel()));
		}

		// Itsukushima Shrine
		else if (eBuilding == ITSUKUSHIMA_SHRINE)
		{
			int iNumWater = 0;
			for (CityPlotIter it(*this); it.hasNext(); ++it)
			{
				if (it->isWater())
					iNumWater++;
			}

			setBuildingGreatPeopleRateChange(ITSUKUSHIMA_SHRINE, std::max(0, iNumWater * iChange));
		}

		// Mole Antonelliana
		else if (eBuilding == MOLE_ANTONELLIANA)
		{
			int iNumPeaks = 0;
			for (CityPlotIter it(*this); it.hasNext(); ++it)
			{
				if (it->isPeak())
				{
					iNumPeaks++;
				}
			}

			setBuildingYieldChange(MOLE_ANTONELLIANA, YIELD_PRODUCTION, std::max(0, iNumPeaks * 2 * iChange));
		}

		// Metropolitain
		else if (eBuilding == METROPOLITAIN)
		{
			FOR_EACH_ENUM(BuildingClass)
			{
				if (GC.getInfo(eLoopBuildingClass).isNationalWonder() || GC.getInfo(eLoopBuildingClass).isWorldWonder())
					continue;

				BuildingTypes eBuilding = GC.getInfo(getCivilizationType()).getCivilizationBuildings(eLoopBuildingClass);
				if (eBuilding == NO_BUILDING)
					continue;

				int iCulture = GC.getInfo(eBuilding).getCommerceChange(COMMERCE_CULTURE) + GC.getInfo(eBuilding).getObsoleteSafeCommerceChange(COMMERCE_CULTURE);
				if (iCulture == 0)
					continue;

				changeBuildingYieldChange(eLoopBuildingClass, YIELD_COMMERCE, iChange * iCulture / 2);
			}
		}

		// Berlaymont
		else if (eBuilding == BERLAYMONT)
		{
			int iNumDefensivePacts = 0;
			for (TeamIter<FREE_MAJOR_CIV,NOT_SAME_TEAM_AS> it(getTeam()); it.hasNext(); ++it)
			{
				if (it->isDefensivePact(getTeam()))
					iNumDefensivePacts += 1;
			}

			changeFreeSpecialist(iChange * iNumDefensivePacts);
		}

		// Atomium
		else if (eBuilding == ATOMIUM)
		{
			int iAtomiumResearch = 10 * kOwner.getNumAvailableBonuses(BONUS_URANIUM)
				+ kOwner.getNumAvailableBonuses(BONUS_IRON) 
				+ kOwner.getNumAvailableBonuses(BONUS_COPPER) 
				+ kOwner.getNumAvailableBonuses(BONUS_ALUMINUM);
			setBuildingCommerceChange(ATOMIUM, COMMERCE_RESEARCH, std::max(0, iAtomiumResearch * iChange));
		}

		// Global Seed Vault
		else if (eBuilding == GLOBAL_SEED_VAULT)
		{
			if (iChange > 0)
			{
				int iResearch = 0;
				FOR_EACH_ENUM(Bonus)
				{
					FOR_EACH_ENUM(Build)
					{
						CvBuildInfo& kBuild = GC.getInfo(eLoopBuild);
						if (kBuild.isGraphicalOnly())
							continue;

						if (kBuild.getTechPrereq() == AGRICULTURE || kBuild.getTechPrereq() == POTTERY || kBuild.getTechPrereq() == CALENDAR)
						{
							CvImprovementInfo& kImprovement = GC.getInfo(kBuild.getImprovement());
							if (kImprovement.isGraphicalOnly())
								continue;
							if (kImprovement.isActsAsCity())
								continue;

							if (kImprovement.isImprovementBonusMakesValid(eLoopBonus))
							{
								iResearch += kOwner.getNumAvailableBonuses(eLoopBonus);
								break;
							}
						}
					}
				}

				setBuildingCommerceChange(GLOBAL_SEED_VAULT, COMMERCE_RESEARCH, iResearch * iChange);
			}
			else
			{
				setBuildingCommerceChange(GLOBAL_SEED_VAULT, COMMERCE_RESEARCH, 0);
			}
		}

		// ITER
		else if (eBuilding == ITER)
		{
			int iPowerConsumed = 0;
			for (PlayerIter<EVER_ALIVE> it; it.hasNext(); ++it)
			{
				FOR_EACH_CITY(pLoopCity, *it)
				{
					iPowerConsumed += pLoopCity->getPowerConsumedCount();
				}
			}

			setBuildingYieldChange(ITER, YIELD_COMMERCE, std::max(0, iPowerConsumed * iChange));
		}

        kOwner.changeAssets(iChange * kBuilding.getAssetValue());

        // doc: area effects apply to nearby landmasses
		getContinentArea().changePower(getOwner(), iChange * kBuilding.getPowerValue());
		kOwner.changePower(kBuilding.getPowerValue() * iChange);

		for (MemberIter it(getTeam()); it.hasNext(); ++it)
		{
			if (kBuilding.isTeamShare() || it->getID() == getOwner())
                // doc: area effects apply to nearby landmasses
				it->processBuilding(eBuilding, iChange, getArea());
		}
		GET_TEAM(getTeam()).processBuilding(eBuilding, iChange);
		GC.getGame().processBuilding(eBuilding, iChange);
	}

	if (!bObsolete)
	{
		/*  <advc.004c> Can avoid an update (which loops over all buildings)
			in the most common circumstances */
		if (kBuilding.getDefenseModifier() != 0 && getBuildingDefense() > 0)
			updateBuildingDefense();
		else // </advc.004c>
			changeBuildingDefense(kBuilding.getDefenseModifier() * iChange);
		// <advc.004c>
		if (kBuilding.get(CvBuildingInfo::RaiseDefense) > 0)
		{
			if (iChange >= 0)
			{
				changeBuildingDefense(std::max(kBuilding.get(CvBuildingInfo::RaiseDefense),
						getBuildingDefense()) - getBuildingDefense());
			}
			else updateBuildingDefense();
		} // </advc.004c>
		changeBuildingBombardDefense(kBuilding.getBombardDefenseModifier() * iChange);
	    changeBuildingUnignorableBombardDefense(kBuilding.getUnignorableBombardDefenseModifier() * iChange);

	    // doc: Mount Athos effect
	    if (kBuilding.getGreatPeopleRateChange() > 0)
	    {
	        if (kOwner.isHasBuildingEffect(MOUNT_ATHOS) && eBuilding != MOUNT_ATHOS)
	        {
	            changeBuildingGreatPeopleRateChange(kBuilding.getBuildingClassType(), iChange * kBuilding.getGreatPeopleRateChange());
	        }
	    }

	    // doc: Louvre effect
		if (kBuilding.isWorldWonder())
		{
			if (kOwner.isHasBuildingEffect(LOUVRE) && eBuilding != LOUVRE)
			{
				FOR_EACH_CITY_VAR(pLoopCity, kOwner)
				{
					if (pLoopCity->isHasRealBuilding(LOUVRE))
					{
						pLoopCity->changeBuildingCommerceChange(LOUVRE, COMMERCE_CULTURE, 2 * iChange);
						break;
					}
				}
			}
		}

        // advc.051: Moved
		//changeBaseGreatPeopleRate(kBuilding.getGreatPeopleRateChange() * iChange);
		if (kBuilding.getGreatPeopleUnitClass() != NO_UNITCLASS)
		{
			UnitTypes eGreatPeopleUnit = getCivilization().getUnit(
					kBuilding.getGreatPeopleUnitClass());
			if (eGreatPeopleUnit != NO_UNIT)
			{
				changeGreatPeopleUnitRate(eGreatPeopleUnit,
						kBuilding.getGreatPeopleRateChange() * iChange);
				/*  advc.051: Moved from above. Barbarians can obtain wonders, but
					don't have GP units, and shouldn't have a positive base GP rate. */
				changeBaseGreatPeopleRate(kBuilding.getGreatPeopleRateChange() * iChange);
			}
		}
		BuildingClassTypes eBuildingClass = kBuilding.getBuildingClassType();
		GET_TEAM(getTeam()).changeBuildingClassCount(eBuildingClass, iChange);
		kOwner.changeBuildingClassCount(eBuildingClass, iChange);

		kOwner.changeWondersScore(kGame.getWonderScore(
				kBuilding.getBuildingClassType()) * iChange);

        // doc: building processed event
	    CvEventReporter::getInstance().buildingProcessed(this, eBuilding, iChange);

		// <advc.004w>
		if (kGame.getCurrentLayer() == GLOBE_LAYER_RESOURCE)
		{
			// Update text of resource indicators (CvGameTextMgr::setBonusExtraHelp)
			PlayerTypes eDirtyPlayer = NO_PLAYER;
			if (kBuilding.isNationalWonder() && isActiveOwned())
				eDirtyPlayer = getOwner();
			else if (kBuilding.isWorldWonder())
				eDirtyPlayer = kGame.getActivePlayer();
			if (eDirtyPlayer != NO_PLAYER)
			{
				gDLL->UI().setDirty(GlobeLayer_DIRTY_BIT, true);
				// advc.003p:
				GET_PLAYER(getOwner()).setBonusHelpDirty();
			}
		} // </advc.004w>
	}

	updateBuildingCommerce();
	setLayoutDirty(true);
}


// TODO: refactor
void CvCity::processPlayerBuilding(BuildingTypes eBuilding, int iChange)
{
	// Himeji Castle
	if (eBuilding == HIMEJI_CASTLE)
	{
		changeCommerceRateModifier(COMMERCE_CULTURE, getBuildingDefense() * iChange);
	}

	// Old Synagogue
	else if (eBuilding == OLD_SYNAGOGUE)
	{
		for (int iJ = 0; iJ < GC.getNumBuildingInfos(); iJ++)
		{
			CvBuildingInfo& kBuilding = GC.getBuildingInfo((BuildingTypes)iJ);
			if (kBuilding.getReligionType() == JUDAISM)
			{
				changeBuildingCommerceChange((BuildingTypes)iJ, COMMERCE_GOLD, 2 * iChange);
			}
		}
	}

	// Las Lajas Sanctuary
	else if (eBuilding == LAS_LAJAS_SANCTUARY)
	{
		changeHealRate(10 * iChange);
	}
}


void CvCity::processPlayerBuildingEffect(BuildingTypes eBuilding, int iChange)
{
	if (GET_PLAYER(getOwner()).isHasBuildingEffect(eBuilding))
	{
		processPlayerBuilding(eBuilding, iChange);
	}
}


void CvCity::processPlayerBuildingEffects(int iChange)
{
	processPlayerBuildingEffect(TEMPLE_OF_KUKULKAN, iChange);
	processPlayerBuildingEffect(HIMEJI_CASTLE, iChange);
	processPlayerBuildingEffect(OLD_SYNAGOGUE, iChange);
	processPlayerBuildingEffect(LAS_LAJAS_SANCTUARY, iChange);
}


void CvCity::processProcess(ProcessTypes eProcess, int iChange)
{
    int iProductionToCommerceModifier;

	FOR_EACH_ENUM(Commerce)
	{
        iProductionToCommerceModifier = GC.getInfo(eProcess).getProductionToCommerceModifier(eLoopCommerce);

        // doc: civic effect
        if (iProductionToCommerceModifier > 0)
            iProductionToCommerceModifier += GET_PLAYER(getOwner()).getProcessModifier();

        // doc: Mexian UP: +50% production converted to research
        if (getCivilizationType() == MEXICO && eLoopCommerce == COMMERCE_RESEARCH)
            iProductionToCommerceModifier += 50;

		changeProductionToCommerceModifier(eLoopCommerce,
                iChange * iProductionToCommerceModifier);
	}
}


void CvCity::processSpecialist(SpecialistTypes eSpecialist, int iChange)
{
	CvSpecialistInfo const& kSpecialist = GC.getInfo(eSpecialist);
	UnitClassTypes eGPClass = (UnitClassTypes)kSpecialist.getGreatPeopleUnitClass();
	if (eGPClass != NO_UNITCLASS)
	{
		UnitTypes eGreatPeopleUnit = getCivilization().getUnit(eGPClass);
		if (eGreatPeopleUnit != NO_UNIT)
		{
			changeGreatPeopleUnitRate(eGreatPeopleUnit, kSpecialist.getGreatPeopleRateChange() * iChange);
			/*  advc.051: Moved from below. Barbarians don't have GP units; if they
				still end up with a specialist, the base GP rate shouldn't count it. */
			changeBaseGreatPeopleRate(kSpecialist.getGreatPeopleRateChange() * iChange);
		}
	}
	// advc.051: Moved into the block above
	//changeBaseGreatPeopleRate(kSpecialist.getGreatPeopleRateChange() * iChange);

	FOR_EACH_ENUM(Yield)
	{
		changeBaseYieldRate(eLoopYield, iChange *
				kSpecialist.getYieldChange(eLoopYield));
	}
	FOR_EACH_ENUM(Commerce)
	{
		changeSpecialistCommerce(eLoopCommerce, iChange *
				kSpecialist.getCommerceChange(eLoopCommerce));
	}
	updateExtraSpecialistYield();
	changeSpecialistFreeExperience(kSpecialist.getExperience() * iChange);

    changeSpecialistFreeExperience(GC.getSpecialistInfo(eSpecialist).getExperience() * iChange);

    if (kSpecialist.getHappiness() > 0)
        changeSpecialistGoodHappiness(kSpecialist.getHappiness() * iChange);
    else changeSpecialistBadHappiness(-kSpecialist.getHappiness() * iChange);
}


// <advc.004c>
void CvCity::updateBuildingDefense()
{
	int iMaxRaise = 0;
	int iModifier = 0;
	CvCivilization const& kCiv = getCivilization();
	for (int i = 0; i < kCiv.getNumBuildings(); i++)
	{
		BuildingTypes eBuilding = kCiv.buildingAt(i);
		if (getNumBuilding(eBuilding) <= 0)
			continue;
		// (No obsoletion to worry about)
		iMaxRaise = std::max(iMaxRaise, GC.getInfo(eBuilding).get(CvBuildingInfo::RaiseDefense));
		iModifier += GC.getInfo(eBuilding).getDefenseModifier();
	}
	changeBuildingDefense(std::max(iModifier, iMaxRaise) - getBuildingDefense());
} // </advc.004c>


HandicapTypes CvCity::getHandicapType() const
{
	return GET_PLAYER(getOwner()).getHandicapType();
}


CivilizationTypes CvCity::getCivilizationType() const
{
	return GET_PLAYER(getOwner()).getCivilizationType();
}

// advc.003w:
CvCivilization const& CvCity::getCivilization() const
{
	return GET_PLAYER(getOwner()).getCivilization();
}


LeaderHeadTypes CvCity::getPersonalityType() const
{
	return GET_PLAYER(getOwner()).getPersonalityType();
}


ArtStyleTypes CvCity::getArtStyleType() const
{
    // doc: did not include dynamic art style advciv code
	return m_eArtStyle;
}

// doc
// TODO: refactor
int CvCity::determineArtStyleType() const
{
	PlayerTypes eHighestCulture = findHighestCulture(true);

	if (eHighestCulture == NO_PLAYER)
	{
		eHighestCulture = getOwner();
	}

	CvPlayer& kHighestCulturePlayer = GET_PLAYER(eHighestCulture);
	CivilizationTypes eHighestCultureCiv = kHighestCulturePlayer.getCivilizationType();

	int eRegion = getRegionID();
	int eRegionGroup = getRegionGroup();

	if (kHighestCulturePlayer.isNative())
	{
		switch (eRegion)
		{
		case REGION_ARIDOAMERICA:
		case REGION_MESOAMERICA:
		case REGION_CENTRAL_AMERICA:
		case REGION_CARIBBEAN:
			return GC.getCivilizationInfo(AZTECS).getArtStyleType();
		}

		if (eRegionGroup == REGION_GROUP_NORTH_AMERICA)
		{
			return GC.getCivilizationInfo(NATIVE).getArtStyleType();
		}
		else if (eRegionGroup == REGION_GROUP_SOUTH_AMERICA)
		{
			return GC.getCivilizationInfo(INCA).getArtStyleType();
		}
		else if (eRegionGroup == REGION_GROUP_SUB_SAHARAN_AFRICA)
		{
			return GC.getCivilizationInfo(CONGO).getArtStyleType();
		}
	}
	else if (kHighestCulturePlayer.isIndependent() || kHighestCulturePlayer.isBarbarian() || (eHighestCultureCiv == MONGOLS && !isOriginalOwner(eHighestCulture)))
	{
		switch (eRegion)
		{
		case REGION_BRITAIN:
		case REGION_IRELAND:
			return GC.getCivilizationInfo(ENGLAND).getArtStyleType();
		case REGION_ARIDOAMERICA:
		case REGION_MESOAMERICA:
		case REGION_CARIBBEAN:
		case REGION_CENTRAL_AMERICA:
			if (eHighestCultureCiv == AZTECS || eHighestCultureCiv == MAYA)
			{
				return GC.getCivilizationInfo(eHighestCultureCiv).getArtStyleType();
			}
			return GC.getCivilizationInfo(SPAIN).getArtStyleType();
		case REGION_FRANCE:
		case REGION_QUEBEC:
		case REGION_LOWER_GERMANY:
		case REGION_CENTRAL_EUROPE:
		case REGION_POLAND:
			return GC.getCivilizationInfo(FRANCE).getArtStyleType();
		case REGION_IBERIA:
		case REGION_CALIFORNIA:
			return GC.getCivilizationInfo(SPAIN).getArtStyleType();
		case REGION_ITALY:
		case REGION_BALKANS:
		case REGION_GREECE:
			return GC.getCivilizationInfo(ROME).getArtStyleType();
		case REGION_BALTICS:
		case REGION_SCANDINAVIA:
			return GC.getCivilizationInfo(NORSE).getArtStyleType();
		case REGION_RUSSIA:
		case REGION_RUTHENIA:
		case REGION_EUROPEAN_ARCTIC:
		case REGION_VOLGA:
		case REGION_URALS:
		case REGION_SIBERIA:
			return GC.getCivilizationInfo(RUSSIA).getArtStyleType();
		case REGION_MAGHREB:
			if (isHasReligion(ISLAM))
			{
				return GC.getCivilizationInfo(ARABIA).getArtStyleType();
			}
			return GC.getCivilizationInfo(ROME).getArtStyleType();
		case REGION_ANATOLIA:
		case REGION_CAUCASUS:
			if (isHasReligion(ISLAM))
			{
				return GC.getCivilizationInfo(PERSIA).getArtStyleType();
			}
			return GC.getCivilizationInfo(ROME).getArtStyleType();
		case REGION_LEVANT:
			if (isHasReligion(ISLAM))
			{
				return GC.getCivilizationInfo(ARABIA).getArtStyleType();
			}
			return GC.getCivilizationInfo(CARTHAGE).getArtStyleType();
		case REGION_MESOPOTAMIA:
			if (isHasReligion(ISLAM))
			{
				return GC.getCivilizationInfo(ARABIA).getArtStyleType();
			}
			return GC.getCivilizationInfo(BABYLONIA).getArtStyleType();
		case REGION_ARABIA:
			return GC.getCivilizationInfo(ARABIA).getArtStyleType();
		case REGION_EGYPT:
			if (isHasReligion(ISLAM))
			{
				return GC.getCivilizationInfo(ARABIA).getArtStyleType();
			}
			else if (GET_PLAYER(eHighestCulture).getCurrentEra() == ERA_ANCIENT)
			{
				return GC.getCivilizationInfo(EGYPT).getArtStyleType();
			}
			return GC.getCivilizationInfo(ROME).getArtStyleType();
		case REGION_NUBIA:
			if (isHasReligion(ISLAM))
			{
				return GC.getCivilizationInfo(ARABIA).getArtStyleType();
			}
			else if (GET_PLAYER(eHighestCulture).getCurrentEra() == ERA_ANCIENT)
			{
				return GC.getCivilizationInfo(EGYPT).getArtStyleType();
			}
			return GC.getCivilizationInfo(CONGO).getArtStyleType();
		case REGION_PERSIA:
		case REGION_KHORASAN:
		case REGION_TRANSOXIANA:
			return GC.getCivilizationInfo(PERSIA).getArtStyleType();
		case REGION_HORN_OF_AFRICA:
		case REGION_SWAHILI_COAST:
		case REGION_SAHEL:
		case REGION_SAHARA:
			if (isHasReligion(ISLAM))
			{
				return GC.getCivilizationInfo(ARABIA).getArtStyleType();
			}
			return GC.getCivilizationInfo(CONGO).getArtStyleType();
		case REGION_INDOCHINA:
		case REGION_INDONESIA:
			return GC.getCivilizationInfo(KHMER).getArtStyleType();
		case REGION_PHILIPPINES:
			if (isHasReligion(CATHOLICISM))
			{
				return GC.getCivilizationInfo(SPAIN).getArtStyleType();
			}
			return GC.getCivilizationInfo(KHMER).getArtStyleType();
		case REGION_SOUTH_CHINA:
		case REGION_NORTH_CHINA:
		case REGION_TARIM_BASIN:
		case REGION_TIBET:
		case REGION_KOREA:
			return GC.getCivilizationInfo(CHINA).getArtStyleType();
		case REGION_JAPAN:
			return GC.getCivilizationInfo(JAPAN).getArtStyleType();
		case REGION_MONGOLIA:
		case REGION_MANCHURIA:
		case REGION_AMUR:
		case REGION_CENTRAL_ASIAN_STEPPE:
		case REGION_PONTIC_STEPPE:
			return GC.getCivilizationInfo(MONGOLS).getArtStyleType();
		}

		if (eRegionGroup == REGION_GROUP_NORTH_AMERICA)
		{
			return GC.getCivilizationInfo(AMERICA).getArtStyleType();
		}
		else if (eRegionGroup == REGION_GROUP_SOUTH_AMERICA)
		{
			return GC.getCivilizationInfo(INCA).getArtStyleType();
		}
		else if (eRegionGroup == REGION_GROUP_EUROPE)
		{
			return GC.getCivilizationInfo(FRANCE).getArtStyleType();
		}
		else if (eRegionGroup == REGION_GROUP_MIDDLE_EAST)
		{
			return GC.getCivilizationInfo(PERSIA).getArtStyleType();
		}
		else if (eRegionGroup == REGION_GROUP_NORTH_AFRICA)
		{
			if (isHasReligion(ISLAM))
			{
				return GC.getCivilizationInfo(ARABIA).getArtStyleType();
			}
			return GC.getCivilizationInfo(ROME).getArtStyleType();
		}
		else if (eRegionGroup == REGION_GROUP_SUB_SAHARAN_AFRICA)
		{
			return GC.getCivilizationInfo(CONGO).getArtStyleType();
		}
		else if (eRegionGroup == REGION_GROUP_SOUTH_ASIA)
		{
			if (isHasReligion(ISLAM))
			{
				return GC.getCivilizationInfo(PERSIA).getArtStyleType();
			}
			return GC.getCivilizationInfo(INDIA).getArtStyleType();
		}
		else if (eRegionGroup == REGION_GROUP_NORTH_ASIA)
		{
			return GC.getCivilizationInfo(MONGOLS).getArtStyleType();
		}
		else if (eRegionGroup == REGION_GROUP_EAST_ASIA)
		{
			return GC.getCivilizationInfo(CHINA).getArtStyleType();
		}
		else if (eRegionGroup == REGION_GROUP_OCEANIA)
		{
			return GC.getCivilizationInfo(POLYNESIA).getArtStyleType();
		}
	}
	else if (eHighestCultureCiv == MONGOLS)
	{
		if (getPopulation() >= 5)
		{
			return GC.getCivilizationInfo(CHINA).getArtStyleType();
		}
	}
	else if (eHighestCultureCiv == AZTECS || eHighestCultureCiv == MAYA || eHighestCultureCiv == INCA)
	{
		if (isHasReligion(CATHOLICISM))
		{
			return GC.getCivilizationInfo(SPAIN).getArtStyleType();
		}
	}

	return GC.getCivilizationInfo(eHighestCultureCiv).getArtStyleType();
}

// doc
// TODO: refactor
void CvCity::updateArtStyleType()
{
	ArtStyleTypes eNewArtStyle = (ArtStyleTypes)determineArtStyleType();

	if (m_eArtStyle != eNewArtStyle)
	{
		m_eArtStyle = eNewArtStyle;
		setLayoutDirty(true);
	}
}

CitySizeTypes CvCity::getCitySizeType() const
{
	return (CitySizeTypes)range((getPopulation() / 7), 0, NUM_CITYSIZE_TYPES - 1);
}

const CvArtInfoBuilding* CvCity::getBuildingArtInfo(BuildingTypes eBuilding) const
{
	return GC.getInfo(eBuilding).getArtInfo();
}

float CvCity::getBuildingVisibilityPriority(BuildingTypes eBuilding) const
{
	return GC.getInfo(eBuilding).getVisibilityPriority();
}

bool CvCity::hasTrait(TraitTypes eTrait) const
{
	return GET_PLAYER(getOwner()).hasTrait(eTrait);
}


bool CvCity::isBarbarian() const
{
	return GET_PLAYER(getOwner()).isBarbarian();
}


bool CvCity::isIndependent() const
{
	return GET_PLAYER(getOwner()).isIndependent();
}


bool CvCity::isMinorCiv() const
{
	return GET_PLAYER(getOwner()).isMinorCiv();
}


bool CvCity::isHuman() const
{
	return GET_PLAYER(getOwner()).isHuman();
}


bool CvCity::isVisible(TeamTypes eTeam, bool bDebug) const
{
	return getPlot().isVisible(eTeam, bDebug);
}


bool CvCity::isCapital() const
{
	return (GET_PLAYER(getOwner()).getCapital() == this);
}

// advc: Cut from CvPlot::canTrain
bool CvCity::isPrereqBonusSea() const
{
	FOR_EACH_ADJ_PLOT(getPlot())
	{
		if (pAdj->isWater() &&
			!pAdj->isImpassable() && // advc.041
			pAdj->getArea().isAnyBonus())
		{
			return true;
		}
	}
	return false;
}

bool CvCity::isCoastal(int iMinWaterSize) const
{
	return getPlot().isCoastalLand(iMinWaterSize);
}


bool CvCity::isDisorder() const
{
	return (isOccupation() || GET_PLAYER(getOwner()).isAnarchy());
}

// advc:
bool CvCity::isNoMaintenance() const
{
	return (isDisorder() || isWeLoveTheKingDay() || getPopulation() <= 0);
}


bool CvCity::isHolyCity(ReligionTypes eReligion) const
{
	return (GC.getGame().getHolyCity(eReligion) == this);
}


bool CvCity::isHolyCity() const
{
	FOR_EACH_ENUM(Religion)
	{
		if (isHolyCity(eLoopReligion))
			return true;
	}
	return false;
}


bool CvCity::isHeadquarters(CorporationTypes eCorp) const
{
	return (GC.getGame().getHeadquarters(eCorp) == this);
}

void CvCity::setHeadquarters(CorporationTypes eCorp)
{
	GC.getGame().setHeadquarters(eCorp, this, /* advc.106e: */ false);
	UnitClassTypes eFreeClass = GC.getInfo(eCorp).getFreeUnitClass();
	if (eFreeClass != NO_UNITCLASS)
	{
		UnitTypes eFreeUnit = getCivilization().getUnit(eFreeClass);
		if (eFreeUnit != NO_UNIT)
			GET_PLAYER(getOwner()).initUnit(eFreeUnit, getX(), getY());
	}
}

bool CvCity::isHeadquarters() const
{
	FOR_EACH_ENUM(Corporation)
	{
		if (isHeadquarters(eLoopCorporation))
			return true;
	}
	return false;
}


int CvCity::getOvercrowdingPercentAnger(int iExtra) const
{
	int iAnger = 0;
	int iPopulation = getPopulation() + iExtra;
    // doc: double unhappiness for population past 10
    int iOvercrowding = iPopulation + std::max(0, iPopulation-10);

	if (iOvercrowding > 0)
	{
		iAnger += (iOvercrowding * GC.getPERCENT_ANGER_DIVISOR()) /
				std::max(1, iPopulation) + 1;
	}
	return iAnger;
}


int CvCity::getNoMilitaryPercentAnger() const
{	// <advc.500b>
	static bool const bDEMAND_BETTER_PROTECTION = GC.getDefineBOOL(
			"DEMAND_BETTER_PROTECTION");
	if (!bDEMAND_BETTER_PROTECTION) // </advc.500b>
	{
		int iAnger = 0;
		if (getMilitaryHappinessUnits() == 0)
		{
			iAnger += //GC.getDefineINT(CvGlobals::NO_MILITARY_PERCENT_ANGER);
					GET_TEAM(getTeam()).getNoMilitaryAnger(); // advc.500c
		}
		return iAnger;
	}
	// <advc.500b>
	static scaled const rPOP_PERCENT = per100(GC.getDefineINT(
			"DEMAND_BETTER_PROTECTION_POP_PERCENT"));
	scaled rTargetGarrStr = getPopulation() * rPOP_PERCENT;
	scaled rActualGarrStr = defensiveGarrison(rTargetGarrStr);
	if (rActualGarrStr >= rTargetGarrStr)
		return 0;
	/* Currently (as per vanilla) 334, meaning 33.4% of the population get angry.
	   The caller adds up all the anger percentages (actually permillages)
	   before rounding, so rounding shouldn't be a concern in this function. */
	int iMaxAnger = GET_TEAM(getTeam()).getNoMilitaryAnger(); // advc.500c
	return iMaxAnger - (iMaxAnger * rActualGarrStr / rTargetGarrStr).floor();
	// </advc.500b>
}


int CvCity::getCulturePercentAnger() const
{
	//int iTotalCulture = getPlot().getTotalCulture(); // advc.opt: was countTotalCulture
	int iTotalCulture = countTotalCultureTimes100() / 100; // doc: use city culture
    if (iTotalCulture == 0)
		return 0;

	int iAngryCulture = 0;
	static int const iCulturePercentAnger = GC.getDefineINT("CULTURE_PERCENT_ANGER"); // advc.opt
	// <advc.099>
	static int const iAngerModCB = GC.getDefineINT("CLOSED_BORDERS_CULTURE_ANGER_MODIFIER");
	static int const iAngerModWar = GC.getDefineINT("AT_WAR_CULTURE_ANGER_MODIFIER");
	for (PlayerIter<EVER_ALIVE,NOT_SAME_TEAM_AS> it(getTeam()); it.hasNext(); ++it)
	{
		CvPlayer const& kRival = *it;

        // doc: ignore minor civs
        if (kRival.isMinorCiv())
            continue;

		int iCulture = getPlot().getCulture(kRival.getID());
		if(iCulture <= 0)
			continue;
		int iRelationsModifier = 0;
		if (!kRival.isBarbarian())
		{
			if (kRival.isAlive() && ::atWar(kRival.getTeam(), getTeam()))
				iRelationsModifier += iAngerModWar + iAngerModCB;
			else
			{
				bool const bCapitulatedVassal = (GET_TEAM(kRival.getTeam()).isCapitulated() &&
						GET_TEAM(kRival.getTeam()).isVassal(getTeam()));
				bool const bOB = GET_TEAM(getTeam()).isOpenBorders(kRival.getTeam());
				if ((!bOB && !bCapitulatedVassal) || !kRival.isAlive())
					iRelationsModifier += iAngerModCB;
			}
		}
		iCulture *= std::max(0, iRelationsModifier + 100);
		iCulture /= 100;

        // doc: dead civs count less
        if (!kRival.isAlive())
            iCulture /= 2;

		iAngryCulture += iCulture;
	} // </advc.099>
	return (iCulturePercentAnger * iAngryCulture) / iTotalCulture;
}

// <advc.104>
int CvCity::getReligionPercentAnger() const
{
	scaled r = 0;
	for (PlayerIter<CIV_ALIVE,ENEMY_OF> it(getTeam()); it.hasNext(); ++it)
	{
		r += getReligionPercentAnger(it->getID());
	}
	return r.round();
}


scaled CvCity::getReligionPercentAnger(PlayerTypes ePlayer) const
{
	// Replacing BtS code; fewer rounding artifacts.
	CvGame const& kGame = GC.getGame();
	if (kGame.getNumCities() == 0 || getReligionCount() == 0)
		return 0;
	CvPlayer const& kPlayer = GET_PLAYER(ePlayer);
	ReligionTypes eReligion = kPlayer.getStateReligion();
	if (eReligion == NO_RELIGION || !isHasReligion(eReligion))
		return 0;
	scaled rSameReligionCityRatio(kPlayer.getHasReligionCount(eReligion),
			kGame.getNumCities());
	static int const iRELIGION_PERCENT_ANGER = GC.getDefineINT("RELIGION_PERCENT_ANGER", 800); // advc.opt
	scaled rAngerFactor(iRELIGION_PERCENT_ANGER, getReligionCount());
	return rSameReligionCityRatio * rAngerFactor;
} // </advc.104>


int CvCity::getHurryPercentAnger(int iExtra) const
{
	if (getHurryAngerTimer() == 0)
		return 0;
	int iHurryPercentAnger = 1 + (((((getHurryAngerTimer() - 1) / flatHurryAngerLength()) + 1) *
			GC.getDefineINT(CvGlobals::HURRY_POP_ANGER) * GC.getPERCENT_ANGER_DIVISOR()) /
			std::max(1, getPopulation() + iExtra));

    // doc: Blue Mosque effect
    if (isHasBuildingEffect(BLUE_MOSQUE))
        iHurryPercentAnger = std::min(iHurryPercentAnger, GC.getPERCENT_ANGER_DIVISOR());

	return iHurryPercentAnger;
}


int CvCity::getConscriptPercentAnger(int iExtra) const
{
	if (getConscriptAngerTimer() == 0)
		return 0;

	int iConscriptPercentAnger = 1 + (((((getConscriptAngerTimer() - 1) / flatConscriptAngerLength()) + 1) *
			GC.getDefineINT(CvGlobals::CONSCRIPT_POP_ANGER) * GC.getPERCENT_ANGER_DIVISOR()) /
			std::max(1, getPopulation() + iExtra));

    // doc: Blue Mosque effect
    if (isHasBuildingEffect(BLUE_MOSQUE))
        iConscriptPercentAnger = std::min(iConscriptPercentAnger, GC.getPERCENT_ANGER_DIVISOR());

    return iConscriptPercentAnger;
}


int CvCity::getDefyResolutionPercentAnger(int iExtra) const
{
	if (getDefyResolutionAngerTimer() == 0)
		return 0;
	// advc.opt:
	int iDefyResolutionPercentAnger = 1 + (((((getDefyResolutionAngerTimer() - 1) / flatDefyResolutionAngerLength()) + 1) *
			GC.getDefineINT(CvGlobals::DEFY_RESOLUTION_POP_ANGER) *
			GC.getPERCENT_ANGER_DIVISOR()) /
			std::max(1, getPopulation() + iExtra));

    // doc: Blue Mosque effect
    if (isHasBuildingEffect(BLUE_MOSQUE))
        iDefyResolutionPercentAnger = std::min(iDefyResolutionPercentAnger, GC.getPERCENT_ANGER_DIVISOR());

    return iDefyResolutionPercentAnger;
}


int CvCity::getWarWearinessPercentAnger() const
{
	int iAnger = GET_PLAYER(getOwner()).getWarWearinessPercentAnger();
	iAnger *= std::max(0, getWarWearinessModifier() +
			GET_PLAYER(getOwner()).getWarWearinessModifier() + 100);
	iAnger /= 100;
	return iAnger;
}


int CvCity::getLargestCityHappiness() const
{
	if (findPopulationRank() <= GC.getInfo(GC.getMap().getWorldSize()).getTargetNumCities())
		return GET_PLAYER(getOwner()).getLargestCityHappiness();
	return 0;
}

int CvCity::getVassalHappiness() const
{	// <advc.003n>
	if(isBarbarian())
		return 0; // </advc.003n>
	int iHappy = 0;
	for (TeamIter<ALIVE,VASSAL_OF> it(getTeam()); it.hasNext(); ++it)
	{
		if (!it->isCapitulated()) // advc.142
		{
			iHappy += GC.getDefineINT(CvGlobals::VASSAL_HAPPINESS);
			break; // advc.142
		}
	}
	return iHappy;
}

int CvCity::getVassalUnhappiness() const
{
	// <advc.opt> Replacing loop over "all" masters
	if(GET_TEAM(getTeam()).isAVassal())
		return GC.getDefineINT(CvGlobals::VASSAL_HAPPINESS);
	return 0; // </advc.opt>
}


int CvCity::unhappyLevel(int iExtra) const
{
	if (isNoUnhappiness())
		return 0; // advc

	int iAngerPercent = 0;
	iAngerPercent += getOvercrowdingPercentAnger(iExtra);
	iAngerPercent += getNoMilitaryPercentAnger();
	iAngerPercent += getCulturePercentAnger();
	iAngerPercent += getReligionPercentAnger();
	iAngerPercent += getHurryPercentAnger(iExtra);
	iAngerPercent += getConscriptPercentAnger(iExtra);
	iAngerPercent += getDefyResolutionPercentAnger(iExtra);
	iAngerPercent += getWarWearinessPercentAnger();
	/*  K-Mod, 5/jan/11: global warming anger _percent_; as part per 100.
		Unfortunately, people who made the rest of the game used anger percent to mean part per 1000
		so I have to multiply my GwPercentAnger by 10 to make it fit in. */
	iAngerPercent += std::max(0, GET_PLAYER(getOwner()).getGwPercentAnger()*10);

	FOR_EACH_ENUM(Civic)
	{
		iAngerPercent += GET_PLAYER(getOwner()).getCivicPercentAnger(eLoopCivic);
	}

	int iUnhappiness = (iAngerPercent * (getPopulation() + iExtra)) / GC.getPERCENT_ANGER_DIVISOR();

	iUnhappiness -= std::min(0, getLargestCityHappiness());
	iUnhappiness -= std::min(0, getMilitaryHappiness());
	iUnhappiness -= std::min(0, getCurrentStateReligionHappiness());
	iUnhappiness -= std::min(0, getBuildingBadHappiness());
	iUnhappiness -= std::min(0, getExtraBuildingBadHappiness());
	iUnhappiness -= std::min(0, getSurroundingBadHappiness());
    iUnhappiness -= std::min(0, getCultureHappiness() * getCultureLevel()); // doc: unhappiness from culture level
    iUnhappiness -= std::min(0, getBonusBadHappiness());
	iUnhappiness -= std::min(0, getReligionBadHappiness());
	iUnhappiness -= std::min(0, getCommerceHappiness());
	iUnhappiness -= std::min(0, getContinentArea().getBuildingHappiness(getOwner())); // doc: area effects apply to nearby landmasses
	iUnhappiness -= std::min(0, GET_PLAYER(getOwner()).getBuildingHappiness());
	iUnhappiness -= std::min(0, (getExtraHappiness() + GET_PLAYER(getOwner()).getExtraHappiness()));
	iUnhappiness -= std::min(0, GC.getInfo(getHandicapType()).getHappyBonus());
	iUnhappiness += std::max(0, getVassalUnhappiness());
    iUnhappiness += std::max(0, getEspionageHappinessCounter());
    iUnhappiness += std::max(0, getSpecialistBadHappiness()); // doc: unhappiness from specialist
    iUnhappiness += std::max(0, getCorporationBadHappiness()); // doc: unhappiness from corporation

	return std::max(0, iUnhappiness);
}


int CvCity::happyLevel() const
{
	int iHappiness = 0;
	iHappiness += std::max(0, getLargestCityHappiness());
	iHappiness += std::max(0, getMilitaryHappiness());
	iHappiness += std::max(0, getCurrentStateReligionHappiness());
	iHappiness += std::max(0, getBuildingGoodHappiness());
	iHappiness += std::max(0, getExtraBuildingGoodHappiness());
    iHappiness += std::max(0, getSurroundingGoodHappiness());
    iHappiness += std::max(0, getCultureHappiness() * getCultureLevel()); // doc: happiness from culture level
	iHappiness += std::max(0, getBonusGoodHappiness());
	iHappiness += std::max(0, getReligionGoodHappiness());
	iHappiness += std::max(0, getCorporationGoodHappiness()); // doc: happiness from corporation
	iHappiness += std::max(0, getSpecialistGoodHappiness()); // doc: happiness from specialist
	iHappiness += std::max(0, getCommerceHappiness());
	iHappiness += std::max(0, getContinentArea().getBuildingHappiness(getOwner())); // doc: area effects apply to nearby landmasses
	iHappiness += std::max(0, GET_PLAYER(getOwner()).getBuildingHappiness());
	iHappiness += std::max(0, (getExtraHappiness() + GET_PLAYER(getOwner()).getExtraHappiness()));
	iHappiness += std::max(0, GC.getInfo(getHandicapType()).getHappyBonus());
	iHappiness += std::max(0, getVassalHappiness());
	iHappiness += std::max(0, getTempHappiness()); // doc: temporary happiness can stack beyond +1

	// doc: Shalimar Gardens effect
	if (isHasBuildingEffect(SHALIMAR_GARDENS))
	{
		iHappiness += std::max(0, goodHealth() - badHealth());
	}

	return std::max(0, iHappiness);
}


int CvCity::angryPopulation(int iExtra, /* advc.104: */ bool bIgnoreCultureRate) const
{
	return range((unhappyLevel(iExtra) - happyLevel() + (bIgnoreCultureRate ?
			// advc.104: Actually, ignore tales of "villainy" too.
			getCommerceHappiness() - getEspionageHappinessCounter() : 0)),
			0, (getPopulation() + iExtra));
}


int CvCity::visiblePopulation() const
{
	return getPopulation() - angryPopulation() - getWorkingPopulation();
}


int CvCity::totalFreeSpecialists() const
{
	int iCount = 0;
	if (getPopulation() > 0)
	{
		iCount += getFreeSpecialist();
		iCount += getContinentArea().getFreeSpecialist(getOwner()); // doc: area effects apply to nearby landmasses
		iCount += GET_PLAYER(getOwner()).getFreeSpecialist();
		if (isAnyImprovementFreeSpecialist()) // advc.opt
		{
			FOR_EACH_ENUM(Improvement)
			{
				int iNumSpecialistsPerImprovement = getImprovementFreeSpecialists(
						eLoopImprovement);
				if (iNumSpecialistsPerImprovement > 0)
				{
					iCount += iNumSpecialistsPerImprovement *
							countNumImprovedPlots(eLoopImprovement);
				}
			}
		}
	}
	return iCount;
}


int CvCity::extraPopulation() const
{
	return visiblePopulation() + std::min(0, extraFreeSpecialists());
}


int CvCity::extraSpecialists() const
{
	return visiblePopulation() + extraFreeSpecialists();
}


int CvCity::extraFreeSpecialists() const
{
	return totalFreeSpecialists() - getSpecialistPopulation();
}


int CvCity::unhealthyPopulation(bool bNoAngry, int iExtra) const
{
	/*if (isNoUnhealthyPopulation())
		return 0;
	return std::max(0, getPopulation() + iExtra - (bNoAngry ? angryPopulation(iExtra) : 0));*/ // BtS
	// K-Mod, 27/dec/10: replaced with UnhealthyPopulationModifier
	int iPopulation = getPopulation() + iExtra - (bNoAngry ? angryPopulation(iExtra) : 0);
	// doc: double unhealth per population past 10
    int iUnhealth = iPopulation + std::max(0, iPopulation - 10);
    iUnhealth *= std::max(0, 100 + getUnhealthyPopulationModifier());
	return intdiv::uround(std::max(0, iUnhealth), 100);
}


int CvCity::totalGoodBuildingHealth() const
{
    // doc: area effects apply to nearby landmasses
	return (getBuildingGoodHealth() + getContinentArea().getBuildingGoodHealth(getOwner()) +
			GET_PLAYER(getOwner()).getBuildingGoodHealth() + getExtraBuildingGoodHealth());
}


int CvCity::totalBadBuildingHealth() const
{
	if (isBuildingOnlyHealthy())
        return 0;

    // doc: area effects apply to nearby landmasses
	int iBuildingHealth = (getBuildingBadHealth() + getContinentArea().getBuildingBadHealth(getOwner()) +
				GET_PLAYER(getOwner()).getBuildingBadHealth() + getExtraBuildingBadHealth());

	// doc: building health modifier
	iBuildingHealth *= 100 + getBuildingUnhealthModifier();
	iBuildingHealth /= 100;

	return iBuildingHealth;
}


int CvCity::goodHealth() const
{
	int iHealth = 0;
	iHealth += std::max(0, getFreshWaterGoodHealth());
	iHealth += std::max(0, getSurroundingGoodHealth());
	iHealth += std::max(0, getPowerGoodHealth());
	iHealth += std::max(0, getBonusGoodHealth());
	iHealth += std::max(0, totalGoodBuildingHealth());
    iHealth += std::max(0, getImprovementHealth()); // doc: health from improvement // TODO: redundant with surrounding?
    iHealth += std::max(0, getCorporationHealth()); // doc: health from corporation
	iHealth += std::max(0,
			GET_PLAYER(getOwner()).getExtraHealth() + getExtraHealth());
	iHealth += std::max(0, GC.getInfo(getHandicapType()).getHealthBonus()); 
	iHealth += std::max(0, GET_PLAYER(getOwner()).getModifier(MODIFIER_HEALTH)); // doc: civilization base health
	return iHealth;
}


int CvCity::badHealth(bool bNoAngry, int iExtra) const
{
	int iHealth = 0;
	iHealth -= std::max(0, getEspionageHealthCounter());
	iHealth += std::min(0, getFreshWaterBadHealth());
	iHealth += std::min(0, getSurroundingBadHealth());
	iHealth += std::min(0, getPowerBadHealth());
	iHealth += std::min(0, getBonusBadHealth());
	iHealth += std::min(0, totalBadBuildingHealth());
    iHealth += std::min(0, getImprovementHealth()); // doc: heaalth from improvement // TODO: redundant with surrounding?
    iHealth += std::min(0, -getCorporationUnhealth()); // doc: health from corporation
	iHealth += std::min(0,
			GET_PLAYER(getOwner()).getExtraHealth() + getExtraHealth());
	iHealth += std::min(0, GC.getInfo(getHandicapType()).getHealthBonus());
	iHealth += std::min(0, GET_PLAYER(getOwner()).getModifier(MODIFIER_HEALTH)); // doc: civilization base health
	/*	advc.001 (from Better BUG AI, fix by Fuyu):
		Already counted by totalBadBuildingHealth. */
	//iHealth += std::min(0, getExtraBuildingBadHealth());
	return (unhealthyPopulation(bNoAngry, iExtra) - iHealth);
}


int CvCity::healthRate(bool bNoAngry, int iExtra) const
{
	return std::min(0, goodHealth() - badHealth(bNoAngry, iExtra));
}


int CvCity::foodConsumption(bool bNoAngry, int iExtra) const
{
	return ((getPopulation() + iExtra - (bNoAngry ? angryPopulation(iExtra) : 0)) *
			GC.getFOOD_CONSUMPTION_PER_POPULATION()) - healthRate(bNoAngry, iExtra);
}


int CvCity::foodDifference(bool bBottom, bool bIgnoreProduction) const
{
	if (isDisorder())
		return 0;
	int iDifference;
	//if (isFoodProduction())
	if (!bIgnoreProduction && isFoodProduction()) // K-Mod
		iDifference = std::min(0, getYieldRate(YIELD_FOOD) - foodConsumption());
	else iDifference = (getYieldRate(YIELD_FOOD) - foodConsumption());

	if (bBottom)
	{
		if (getPopulation() == 1 && getFood() == 0)
			iDifference = std::max(0, iDifference);
	}
	return iDifference;
}


int CvCity::growthThreshold(/* <advc.064b> */ int iPopulationChange,
	bool bIgnoreModifiers) const // </advc.064b>
{
	return (GET_PLAYER(getOwner()).getGrowthThreshold(getPopulation()
			+ iPopulationChange, bIgnoreModifiers)); // advc.064b
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
			iModifier = getHurryCostModifier((UnitTypes)
					pOrderNode->m_data.iData1, bIgnoreNew);
			break;
		case ORDER_CONSTRUCT:
			iModifier = getHurryCostModifier((BuildingTypes)
					pOrderNode->m_data.iData1, bIgnoreNew);
			break;
		case ORDER_CREATE:
		case ORDER_MAINTAIN:
			break;
		default:
			FErrorMsg("pOrderNode->m_data.eOrderType did not match a valid option");
		}
	}
	return iModifier;
}


int CvCity::getHurryCostModifier(UnitTypes eUnit, bool bIgnoreNew) const
{
	return getHurryCostModifier(GC.getInfo(eUnit).getHurryCostModifier(),
			getUnitProduction(eUnit), bIgnoreNew);
}


int CvCity::getHurryCostModifier(BuildingTypes eBuilding, bool bIgnoreNew) const
{
	return getHurryCostModifier(GC.getInfo(eBuilding).getHurryCostModifier(),
			getBuildingProduction(eBuilding), bIgnoreNew);
}


int CvCity::getHurryCostModifier(int iBaseModifier, int iProduction, bool bIgnoreNew) const
{
	int iModifier = 100;
	iModifier *= std::max(0, iBaseModifier + 100);
	iModifier /= 100;
	if (iProduction == 0 && !bIgnoreNew)
	{
		static int const iNEW_HURRY_MODIFIER = GC.getDefineINT("NEW_HURRY_MODIFIER"); // advc.opt
		iModifier *= std::max(0, iNEW_HURRY_MODIFIER + 100);
		iModifier /= 100;
	}
	iModifier *= std::max(0, GET_PLAYER(getOwner()).getHurryModifier() + 100);
	iModifier /= 100;
	return iModifier;
}


int CvCity::getHurryCost(bool bExtra, UnitTypes eUnit, bool bIgnoreNew) const
{
	int iProductionLeft = getProductionNeeded(eUnit) - getUnitProduction(eUnit);
	return getHurryCost(bExtra, iProductionLeft, getHurryCostModifier(eUnit, bIgnoreNew),
			getProductionModifier(eUnit));
}


int CvCity::getHurryCost(bool bExtra, BuildingTypes eBuilding, bool bIgnoreNew) const
{
	int iProductionLeft = getProductionNeeded(eBuilding) - getBuildingProduction(eBuilding);
	return getHurryCost(bExtra, iProductionLeft, getHurryCostModifier(eBuilding, bIgnoreNew),
			getProductionModifier(eBuilding, true)); // doc: set second argument to true // TODO: clarify what this means
}

int CvCity::getHurryCost(bool bExtra, int iProductionLeft, int iHurryModifier, int iModifier) const
{
	// <advc.064b>
	if (iProductionLeft == MAX_INT)
		return 0;
	iProductionLeft -= getCurrentProductionDifference(bExtra, true, false, bExtra, true);
	if(bExtra) // City yield rate uncertain if pop is sacrificed (bExtra) ...
	{	// ... but city production is going to be at least 1
		iProductionLeft -= minPlotProduction();
	}
	if(iProductionLeft <= 0)
		return 0;
	// </advc.064b>
	int iProduction = intdiv::uceil(iProductionLeft * iHurryModifier, 100);

	if (bExtra)
	{
		/*int iExtraProduction = getExtraProductionDifference(iProduction, iModifier);
		if (iExtraProduction > 0)
			iProduction = intdiv::uceil(SQR(iProduction), iExtraProduction);*/
		/*	<advc.001> Same as above, but rounds more intuitively, e.g.
			when iProduction=45 and iModifier=50 (settler at 55/100 production with
			Imperialistic trait). Based on a similar change in the CloseToHome mod. */
		iProduction = getInverseProductionDifference(iProduction,
				/*  advc.064c (note): Passing 0 here instead of iModifier would
					only apply generic modifiers */
				iModifier); // </advc.001>
	}

	return std::max(0, iProduction);
}


int CvCity::getHurryGold(HurryTypes eHurry, int iHurryCost) const
{
	if (GC.getInfo(eHurry).getGoldPerProduction() == 0)
		return 0;
	int iGold = iHurryCost * GC.getInfo(eHurry).getGoldPerProduction() / 100; // doc: hurry gold is times 100
	return std::max(0, iGold); // advc.064b: lower bound was 1
}


int CvCity::getHurryPopulation(HurryTypes eHurry, int iHurryCost) const
{
	if (GC.getInfo(eHurry).getProductionPerPopulation() == 0)
		return 0;
	int iPopulation = (iHurryCost - 1) / GC.getGame().getProductionPerPopulation(eHurry);
	return std::max(1, iPopulation + 1);
}

int CvCity::hurryProduction(HurryTypes eHurry) const
{
	bool bPopRush = (GC.getInfo(eHurry).getProductionPerPopulation() > 0);
	//int iProductionNeeded = productionLeft();
	// <advc.064b> ^Don't always need to generate that much production
	/*  If pop is to be removed, we can't rely on tile yields. (However, in that case,
		iProductionNeeded is only used for the assertion at the end. There's similar
		code for pop rushing in CvCity::getHurryCost.) */
	int iProductionDifference = getCurrentProductionDifference(bPopRush, true, false,
			bPopRush, true);
	if(bPopRush)
		iProductionDifference += minPlotProduction();
	int iProductionNeeded = std::max(0, getProductionNeeded() - getProduction() -
			iProductionDifference);
	// </advc.064b>
	if (!bPopRush)
		return iProductionNeeded;

	int iProduction = (100 * getExtraProductionDifference(hurryPopulation(eHurry) *
			GC.getGame().getProductionPerPopulation(eHurry)
			/*  advc.064c (comment): Passing 0 as a second arg would mean that only
				generic modifiers apply */
			)) / std::max(1, getHurryCostModifier());
	FAssert(iProduction >= iProductionNeeded);
	return iProduction;
}


int CvCity::flatHurryAngerLength() const
{
	int iAnger = GC.getGame().getHurryAngerLength();
	iAnger *= std::max(0, 100 + getHurryAngerModifier());
	iAnger /= 100;
	return std::max(1, iAnger);
}


int CvCity::hurryAngerLength(HurryTypes eHurry) const
{
	if (GC.getInfo(eHurry).isAnger())
		return flatHurryAngerLength();
	return 0;
}


int CvCity::maxHurryPopulation() const
{	// <advc.064c>
	static int const iMAX_HURRY_POP = GC.getDefineINT("MAX_HURRY_POP");
	return std::min(iMAX_HURRY_POP, /* </advc.064c> */ getPopulation() / 2);
}


int CvCity::cultureDistance(int iDX, int iDY)
{
	return std::max(1, plotDistance(0, 0, iDX, iDY));
}

// advc.101: Replaced most of the code, but it's still the same structure as in BtS.
int CvCity::cultureStrength(PlayerTypes ePlayer,
	bool bIgnoreWar, bool bIgnoreOccupation, // advc.023
	std::vector<GrievanceTypes>* paGrievances) const // Out parameter for UI support
{
	//int iStrength = 1 + getHighestPopulation() * 2; // BtS
	scaled rPopulation = getPopulation();
	CvGame const& kGame = GC.getGame();
	CvGameSpeedInfo const& kSpeed = GC.getInfo(kGame.getGameSpeedType());
	int iTimeOwned = kGame.getGameTurn() - getGameTurnAcquired();
	scaled rTimeRatio = iTimeOwned / scaled::max(1,
			fixp(0.75) * kSpeed.getGoldenAgePercent());
	scaled rTimeFactor = scaled::min(1, rTimeRatio);
	rPopulation += // Gradually shift to highest pop, then back to actual pop.
			(fixp(0.5) - (rTimeFactor - fixp(0.5)).abs()) *
			(getHighestPopulation() - rPopulation);
	scaled rEraFactor; // BtS used the game era here
	{
		/*	ePlayer can be dead, but the tech count should still be good.
			(CvPlayer::getTechScore / CvGame::getMaxTech would give
			too much weight to late-game tech.) */
		scaled rPlayerTechPercent(GET_TEAM(ePlayer).getTechCount(), GC.getNumTechInfos());
		scaled rOwnerTechPercent(GET_TEAM(getOwner()).getTechCount(), GC.getNumTechInfos());
		scaled rTechPercent = std::max(rPlayerTechPercent,
				((rTimeFactor + 1) / 2) * rOwnerTechPercent);
		// Decrease resolution - to avoid frequent changes in revolt chance
		int const iGrain = 10;
		int iTechPercentQuantized = intdiv::uround(rTechPercent.getPercent(), iGrain);
		if (iTechPercentQuantized > 0)
		{
			rEraFactor = iTechPercentQuantized * scaled(GC.getNumEraInfos() - 1, iGrain);
			rEraFactor.exponentiate(fixp(4/3.));
		}
		rEraFactor++;
	}
	CvPlot const& kCityPlot = getPlot();
	PlayerTypes const eCulturalOwner = kCityPlot.calculateCulturalOwner();
	bool bCanFlip = (canCultureFlip(ePlayer, false) && ePlayer == eCulturalOwner);
	scaled rStrengthFromInnerRadius;
	CvPlayer const& kOwner = GET_PLAYER(getOwner());
	// <advc.099c>
	if (ePlayer == BARBARIAN_PLAYER)
		rEraFactor /= 2; // </advc.099c>
	int iStolenInner = 0;
	FOR_EACH_ADJ_PLOT(getPlot())
	{
		// <advc.035>
		PlayerTypes eLoopOwner = pAdj->getOwner();
		if (GC.getDefineBOOL(CvGlobals::OWN_EXCLUSIVE_RADIUS) && eLoopOwner != NO_PLAYER &&
			!GET_TEAM(eLoopOwner).isAtWar(kOwner.getTeam()))
		{
			PlayerTypes const eSecondOwner = pAdj->getSecondOwner();
			if(eSecondOwner != eLoopOwner) // Checked only for easier debugging
				eLoopOwner = eSecondOwner;
		} // </advc.035>
		if (bCanFlip &&
			eLoopOwner == ePlayer) // advc.035
		{
			rStrengthFromInnerRadius += rEraFactor * scaled::clamp(
					rTimeRatio - fixp(2/3.), 0, fixp(3.5));
			iStolenInner++;
		}
		scaled rCap = fixp(0.25) + fixp(0.75) * rTimeFactor;
		rStrengthFromInnerRadius += rEraFactor * scaled::clamp(per100(
				pAdj->calculateCulturePercent(ePlayer) -
				pAdj->calculateCulturePercent(getOwner())), 0, rCap);
	}
	/*	Don't make cities that stay small for lack of workable tiles
		too easy to hold onto */
	rPopulation.increaseTo(scaled(iStolenInner, 2));
	// To put a cap on the early-game revolt chance in large cities:
	rPopulation.decreaseTo(rEraFactor * fixp(5/3.));
	scaled rStrength = 1 + 2 * rPopulation;
	/*	Era should also affect strength from population
		(only affects strength from surrounding tiles in BtS). */
	rStrength *= scaled::max(2, rEraFactor + 1).sqrt() / 2;
	rStrengthFromInnerRadius /= fixp(1.5); // To even out the change above
	if (!isBarbarian()) // Put engulfed Barbarian cities out of their misery
		rStrengthFromInnerRadius.decreaseTo(fixp(5/3.) * rStrength);
	rStrength += rStrengthFromInnerRadius;
	int const iHurryAnger = (getHurryPercentAnger() * getPopulation()) / 1000;
	FAssert((iHurryAnger == 0) == (getHurryAngerTimer() == 0));
	int const iConscriptAnger = (getConscriptPercentAnger() * getPopulation()) / 3000;
	int iAngry = iHurryAnger + iConscriptAnger;
	iAngry = std::min(iAngry, getPopulation());
	/*  HurryAnger also factors into GrievanceModifier below, but for small cities
		(where Slavery is most effective), this constant bonus matters more. */
	rStrength += 3 * iAngry;
	/*  K-Mod, 7/jan/11, karadoc
		changed so that culture strength asymptotes as the attacking culture approaches 100% */
	//iStrength *= std::max(0, (GC.getDefineINT("REVOLT_TOTAL_CULTURE_MODIFIER") * (kCityPlot.getCulture(ePlayer) - kCityPlot.getCulture(getOwner()))) / (kCityPlot.getCulture(getOwner()) + 1) + 100); //  K-Mod end
	// Restored BtS formula (more or less)
	rStrength *= scaled::max(0, 1 + scaled(
			/*  Don't like the multiplicative interaction between this and the grievances;
				now added to grievances. */
			//GC.getDefineINT("REVOLT_TOTAL_CULTURE_MODIFIER") *
			kCityPlot.getCulture(ePlayer) - kCityPlot.getCulture(getOwner()),
			kCityPlot.getCulture(ePlayer)));
	// New: Reduce strength if far less culture than some third party
	scaled rThirdPartyModifier = fixp(8/5.) * scaled(
			kCityPlot.calculateTeamCulturePercent(TEAMID(ePlayer)),
			kCityPlot.calculateTeamCulturePercent(kCityPlot.findHighestCultureTeam()));
	if(rThirdPartyModifier < 1)
		rStrength *= rThirdPartyModifier;
	// Also/ further reduce strength if owner has almost as much culture as ePlayer
	scaled rSecondPartyModifier(
			kCityPlot.getCulture(ePlayer),
			std::max(1, kCityPlot.getCulture(getOwner())));
	rSecondPartyModifier--;
	rSecondPartyModifier.clamp(0, 1);
	rStrength *= rSecondPartyModifier;

	/*	Culture strength too low in the late game - or garrison strength too high, but
		garrison strength is what players can directly control; needs to be simple, linear.
		Make this adjustment before applying grievance modifiers (or any other modifiers
		that the UI communicates to the player). */
	static scaled const rFOREIGN_CULTURE_STRENGTH_EXPONENT = per100(
			GC.getDefineINT("FOREIGN_CULTURE_STRENGTH_EXPONENT"));
	rStrength.exponentiate(rFOREIGN_CULTURE_STRENGTH_EXPONENT);
	rStrength *= per100(GC.getInfo(kOwner.getHandicapType()).get(
			CvHandicapInfo::ForeignCultureStrength));

	static scaled const rREVOLT_OFFENSE_STATE_RELIGION_MODIFIER = per100(
			GC.getDefineINT("REVOLT_OFFENSE_STATE_RELIGION_MODIFIER"));
	static scaled const rREVOLT_DEFENSE_STATE_RELIGION_MODIFIER = per100(
			GC.getDefineINT("REVOLT_DEFENSE_STATE_RELIGION_MODIFIER"));
	static scaled const rREVOLT_TOTAL_CULTURE_MODIFIER = per100(
			GC.getDefineINT("REVOLT_TOTAL_CULTURE_MODIFIER")); // 100
	scaled rGrievanceModifier;
	ReligionTypes const eOwnerStateReligion = kOwner.getStateReligion();
	CvPlayer const& kPlayer = GET_PLAYER(ePlayer);
	if (kPlayer.isAlive() &&
		(!GET_TEAM(kPlayer.getTeam()).isCapitulated() ||
		kPlayer.getMasterTeam() != getTeam()) &&
		kPlayer.getStateReligion() != NO_RELIGION &&
		isHasReligion(kPlayer.getStateReligion()))
	{
		/*iStrength *= std::max(0, GC.getDefineINT("REVOLT_OFFENSE_STATE_RELIGION_MODIFIER") + 100);
		iStrength /= 100;*/ // BtS
		rGrievanceModifier += rREVOLT_OFFENSE_STATE_RELIGION_MODIFIER;
	}
	else
	{
		/*  Religion offense might still make sense even when ePlayer is defeated, but
			can't expect the owner to memorize the state religions of defeated players.
			Instead, count some religion offense also when the owner's state religion
			is absent and at least one religion is in the city. This makes (some) sense
			whether ePlayer is defeated or not. */
		if(eOwnerStateReligion != NO_RELIGION && !isHasReligion(eOwnerStateReligion))
		{
			FOR_EACH_ENUM(Religion)
			{
				if(isHasReligion(eLoopReligion) && eLoopReligion != eOwnerStateReligion)
				{
					rGrievanceModifier += rREVOLT_OFFENSE_STATE_RELIGION_MODIFIER * fixp(2/3.);
					break;
				}
			}
		}
	}
	if(eOwnerStateReligion != NO_RELIGION && isHasReligion(eOwnerStateReligion))
	{
		/*iStrength *= std::max(0, GC.getDefineINT("REVOLT_DEFENSE_STATE_RELIGION_MODIFIER") + 100);
		iStrength /= 100;*/ // BtS
		/*  The OFFENSE modifier was originally set to 100 in XML and
			DEFENSE to -50, and they were cancelling out when both applied
			(multiplication by 100+100 and then by 100-50). I'm changing the values
			in XML so that they cancel out when added up. */
		rGrievanceModifier += rREVOLT_DEFENSE_STATE_RELIGION_MODIFIER;
	} /* No state religion is still better than some oppressive state religion that
		 the city doesn't share. */
	else if(eOwnerStateReligion == NO_RELIGION && rGrievanceModifier > 0)
		rGrievanceModifier += rREVOLT_DEFENSE_STATE_RELIGION_MODIFIER * fixp(3/5.);
	if (paGrievances != NULL && rGrievanceModifier > 0)
		paGrievances->push_back(GRIEVANCE_RELIGION);
	rGrievanceModifier += rREVOLT_TOTAL_CULTURE_MODIFIER - 1;
	if (iAngry > 0)
	{
		rGrievanceModifier += scaled(iAngry).sqrt() /
				(per100(kSpeed.getHurryConscriptAngerPercent()) + 1);
		if (paGrievances != NULL)
		{
			if (iHurryAnger > 0)
				paGrievances->push_back(GRIEVANCE_HURRY);
			if (iConscriptAnger > 0)
				paGrievances->push_back(GRIEVANCE_CONSCRIPT);
		}
	} // <advc.099c>
	if(GET_TEAM(getTeam()).isCapitulated() && bCanFlip)
		rGrievanceModifier += 1; // </advc.099c>
	// The defense modifier should only halve culture strength, not reduce by 100%
	if(rGrievanceModifier < 0)
		rGrievanceModifier /= 2;
	rStrength *= (1 + scaled::max(-1, rGrievanceModifier));
	/*	<advc.023> Occupation state helps the garrison. Kind of a negative grievance,
		but I think multiplying with grievances will be more intuitive. */
	int iOccupationDiv = 1;
	if (!bIgnoreOccupation && isOccupation())
		iOccupationDiv *= 2;
	if (!bIgnoreWar && isMartialLaw(eCulturalOwner))
		iOccupationDiv *= 2;
	rStrength /= iOccupationDiv;
	// </advc.023>
	return rStrength.round();
}

// advc.101: Changed entirely. The parameter is no longer used.
int CvCity::cultureGarrison(PlayerTypes ePlayer) const
{
	/*  BtS makes Barbarian units ineligible as culture garrison
		through CvPlot::doCulture (now renamed to CvPlot::doRevolts).
		Easier to do it here -- but I do want them to be eligible. */
	/*if(isBarbarian())
		return 0;*/
	int iGarrison = 0; // was 1
	FOR_EACH_UNIT_IN(pUnit, getPlot())
	{
		// <advc.184> Had been counting all units
		if (pUnit->getTeam() != TEAMID(ePlayer) &&
			pUnit->isGarrisonInTeamCity()) // </advc.184>
		{
			iGarrison += pUnit->garrisonStrength();
		}
	}
	/*if (atWar(TEAMID(ePlayer), getTeam()))
		iGarrison *= 2;*/ // advc.023: commented out
	return intdiv::uround(iGarrison, 100);
}

// advc.099c:
PlayerTypes CvCity::calculateCulturalOwner() const
{
	return getPlot().calculateCulturalOwner(GC.getDefineBOOL(CvGlobals::REVOLTS_IGNORE_CULTURE_RANGE));
}


int CvCity::getNumBuilding(BuildingTypes eBuilding) const
{
	return std::min(GC.getDefineINT(CvGlobals::CITY_MAX_NUM_BUILDINGS),
			getNumRealBuilding(eBuilding) + getNumFreeBuilding(eBuilding));
}

// advc.003w:
int CvCity::getNumBuilding(BuildingClassTypes eBuildingClass) const
{
	BuildingTypes eBuilding = getCivilization().getBuilding(eBuildingClass);
	if (eBuilding == NO_BUILDING)
		return 0;
	return getNumBuilding(eBuilding);
}


int CvCity::getNumActiveBuilding(BuildingTypes eBuilding) const
{
	if (GET_TEAM(getTeam()).isObsoleteBuilding(eBuilding))
		return 0;
	return getNumBuilding(eBuilding);
}

// TODO: advciv implements getReligionCount in header but doc has bCountLocalReligion parameter that excludes locals

// UNOFFICIAL_PATCH, War tactics AI, 03/04/10, Mongoose & jdog5000:
int CvCity::getNumActiveWorldWonders(int iStopCountAt, // advc
	PlayerTypes eOwner) const // advc.104d
{
	PROFILE_FUNC(); // advc.opt (tbd.): Cache the return value
	// advc.104d:
	CvTeam const& kObsTeam = GET_TEAM(eOwner == NO_PLAYER ? getTeam() : TEAMID(eOwner));

	int iCount = 0;
	CvCivilization const& kCiv = getCivilization();
	for (int i = 0; i < kCiv.getNumBuildings(); i++)
	{
		BuildingTypes const eBuilding = kCiv.buildingAt(i);
		if (GC.getInfo(eBuilding).isWorldWonder())
		{
			if (getNumRealBuilding(eBuilding) > 0 &&
				!kObsTeam.isObsoleteBuilding(eBuilding)) // advc.104d
			{
				iCount++;
				// <advc> So that hasActiveWorldWonder can defer to getNumActiveWorldWonders
				if (iCount >= iStopCountAt)
					return iCount; // </advc>
			}
		}
	}
	return iCount;
}

// advc:
CvCity* CvCity::fromIDInfo(IDInfo id)
{
	return ::getCity(id);
}


void CvCity::setID(int iID)
{
	m_iID = iID;
}

// advc.opt: Update cached CvPlot, CvArea pointer and plot index.
void CvCity::updatePlot()
{
	m_pPlot = GC.getMap().plotSoren(getX(), getY());
	if (m_pPlot != NULL)
		m_ePlot = GC.getMap().plotNum(getX(), getY());
	updateArea();
}


CvPlotGroup* CvCity::plotGroup(PlayerTypes ePlayer) const
{
	return getPlot().getPlotGroup(ePlayer);
}


bool CvCity::isConnectedTo(CvCity const& kCity) const
{
    // doc: airports connect cities
	return getPlot().isConnectedTo(kCity)  || (getMaxAirlift() > 0 && kCity.getMaxAirlift() > 0);
}


bool CvCity::isConnectedToCapital(PlayerTypes ePlayer) const
{
	return getPlot().isConnectedToCapital(ePlayer);
}

// advc: For handling area recalculation (after a WorldBuilder terrain change)
void CvCity::updateArea()
{
	m_pArea = (plot() == NULL ? NULL :getPlot().area());
}

// BETTER_BTS_AI_MOD, General AI, 01/02/09, jdog5000: param added
CvArea* CvCity::waterArea(bool bNoImpassable) const
{
	return getPlot().waterArea(bNoImpassable);
}

// BETTER_BTS_AI_MOD, General AI, 01/02/09, jdog5000: Expose plot function through city
CvArea* CvCity::secondWaterArea() const
{
	return getPlot().secondWaterArea();
}

// advc.003j (comment): Unused; may or may not work correctly.
// BETTER_BTS_AI_MOD, General AI, 01/02/09, jdog5000: START
// Find the largest water area shared by this city and other city, if any
CvArea* CvCity::sharedWaterArea(CvCity* pOtherCity) const
{
	CvArea* pWaterArea = waterArea(true);
	if (pWaterArea == NULL)
		return NULL; // advc

	CvArea* pOtherWaterArea = pOtherCity->waterArea(true);
	if (pOtherWaterArea != NULL)
	{
		if (pWaterArea == pOtherWaterArea)
			return pWaterArea;

		CvArea* pSecondWaterArea = secondWaterArea();
		CvArea* pOtherSecondWaterArea = pOtherCity->secondWaterArea();
		if (pSecondWaterArea != NULL && pSecondWaterArea == pOtherWaterArea)
			return pSecondWaterArea;
		else if (pOtherSecondWaterArea != NULL && pWaterArea == pOtherSecondWaterArea)
			return pWaterArea;
		else if (pSecondWaterArea != NULL && pOtherSecondWaterArea != NULL &&
			pSecondWaterArea == pOtherSecondWaterArea)
		{
			return pSecondWaterArea;
		}
	}
	return NULL;
}


// doc
CvArea* CvCity::continentArea() const
{
	return getPlot().continentArea();
}


// doc
CvArea& CvCity::getContinentArea() const
{
	return getPlot().getContinentArea();
}


bool CvCity::isBlockaded() const
{
	FOR_EACH_ADJ_PLOT(getPlot())
	{
		if (pAdj->getBlockadedCount(getTeam()) > 0)
			return true;
	}
	return false;
} // BETTER_BTS_AI_MOD: END


CvPlot* CvCity::getRallyPlot() const
{
	return GC.getMap().plotSoren(m_iRallyX, m_iRallyY);
}


void CvCity::setRallyPlot(CvPlot* pPlot)
{
	if (getRallyPlot() == pPlot)
		return; // advc

	if (pPlot != NULL)
	{
		m_iRallyX = pPlot->getX();
		m_iRallyY = pPlot->getY();
	}
	else
	{
		m_iRallyX = INVALID_PLOT_COORD;
		m_iRallyY = INVALID_PLOT_COORD;
	}

	if (isCitySelected())
		gDLL->UI().setDirty(ColoredPlots_DIRTY_BIT, true);

}


void CvCity::setGameTurnFounded(int iNewValue)
{
	if (getGameTurnFounded() != iNewValue)
	{
		m_iGameTurnFounded = iNewValue;
		FAssert(getGameTurnFounded() >= 0);

		GC.getMap().updateWorkingCity();
	}
}


void CvCity::setGameTurnAcquired(int iNewValue)
{
	m_iGameTurnAcquired = iNewValue;
	FAssert(getGameTurnAcquired() >= 0);
}


void CvCity::setPopulation(int iNewValue)
{
	int const iOldPopulation = getPopulation();
	if (iOldPopulation == iNewValue)
		return;
	m_iPopulation = iNewValue;
	FAssert(getPopulation() >= 0);

	GET_PLAYER(getOwner()).invalidatePopulationRankCache();
	if (getPopulation() > getHighestPopulation())
		setHighestPopulation(getPopulation());

	getArea().changePopulationPerPlayer(getOwner(), getPopulation() - iOldPopulation);
	GET_PLAYER(getOwner()).changeTotalPopulation(getPopulation() - iOldPopulation);
	GET_TEAM(getTeam()).changeTotalPopulation(getPopulation() - iOldPopulation);
	GC.getGame().changeTotalPopulation(getPopulation() - iOldPopulation);

	if (iOldPopulation > 0)
		getArea().changePower(getOwner(), -GC.getGame().getPopulationPower(iOldPopulation));
	if (getPopulation() > 0)
		getArea().changePower(getOwner(), GC.getGame().getPopulationPower(getPopulation()));
	// advc (note): For unused iPopulationChangeDivisor (YieldInfo) I think
	getPlot().updateYield();

    // doc: population affects global maintenance
	//updateMaintenance();
    GET_PLAYER(getOwner()).updateMaintenance();

	if ((iOldPopulation == 1 && getPopulation() > 1) ||
		(getPopulation() == 1 && iOldPopulation > 1) ||
		(getPopulation() > iOldPopulation &&
		GET_PLAYER(getOwner()).getNumCities() <= 2))
	{
		if (!isHuman())
			setChooseProductionDirty(true);
	}

	GET_PLAYER(getOwner()).AI_makeAssignWorkDirty();

	setInfoDirty(true);
	setLayoutDirty(true);

	getPlot().plotAction(PUF_makeInfoBarDirty);

	if (isActiveOwned() && isCitySelected())
	{
		gDLL->UI().setDirty(SelectionButtons_DIRTY_BIT, true);
		gDLL->UI().setDirty(CityScreen_DIRTY_BIT, true);
	}

    // doc: gradual population loss during occupation
    if (iNewValue < iOldPopulation)
    {
        setTotalPopulationLoss(std::max(0, getTotalPopulationLoss() + iNewValue - iOldPopulation));
    }

	//updateGenericBuildings();
}


void CvCity::changePopulation(int iChange)
{
	setPopulation(getPopulation() + iChange);
}

// advc: Return type was long. Not helpful since sizeof(int)==sizeof(long).
int CvCity::getRealPopulation() const
{
    // doc (Panopticon): increased population scaling with era
    float fPopExponent = GET_PLAYER(getOwner()).getCurrentEra() <= ERA_INDUSTRIAL ? 3.0f : 3.1f;
	long long iPop = (long long)(std::pow((float)getPopulation(), fPopExponent) * 1000);
	return truncIntCast<int>(iPop);
}


void CvCity::setHighestPopulation(int iNewValue)
{
 	m_iHighestPopulation = iNewValue;
	FAssert(getHighestPopulation() >= 0);
}


void CvCity::changeWorkingPopulation(int iChange)
{
	m_iWorkingPopulation += iChange;
	FAssert(getWorkingPopulation() >= 0);
}


void CvCity::changeSpecialistPopulation(int iChange)
{
	if (iChange != 0)
	{
		m_iSpecialistPopulation += iChange;
		FAssert(getSpecialistPopulation() >= 0);
		GET_PLAYER(getOwner()).invalidateYieldRankCache();
		updateCommerce();
	}
}


void CvCity::changeNumGreatPeople(int iChange)
{
	if (iChange != 0)
	{
		m_iNumGreatPeople += iChange;
		FAssert(getNumGreatPeople() >= 0);
		updateCommerce();
	}
}


int CvCity::getGreatPeopleRate() const
{
	if (isDisorder())
		return 0;
	return (getBaseGreatPeopleRate() * getTotalGreatPeopleRateModifier()) / 100;
}


int CvCity::getTotalGreatPeopleRateModifier() const
{
	int iModifier = getGreatPeopleRateModifier();
    iModifier += getCultureGreatPeopleRateModifier() * getCultureLevel(); // doc: great people rate from culture level
	iModifier += GET_PLAYER(getOwner()).getGreatPeopleRateModifier();

	CvPlayer const& kOwner = GET_PLAYER(getOwner());
	if (kOwner.getStateReligion() != NO_RELIGION)
	{
		if (isHasReligion(kOwner.getStateReligion()))
			iModifier += kOwner.getStateReligionGreatPeopleRateModifier();
	}

	if (kOwner.isGoldenAge())
	{
		static int const iGOLDEN_AGE_GREAT_PEOPLE_MODIFIER = GC.getDefineINT("GOLDEN_AGE_GREAT_PEOPLE_MODIFIER"); // advc.opt
		iModifier += iGOLDEN_AGE_GREAT_PEOPLE_MODIFIER;
	}

    // doc: Greek UP: +150% great people birth rate in the Classical era
    if (getCivilizationType() == GREECE && kOwner.getCurrentEra() <= ERA_CLASSICAL)
    {
        iModifier += 150;
    }

	return std::max(0, iModifier + 100);
}


void CvCity::changeBaseGreatPeopleRate(int iChange)
{
	m_iBaseGreatPeopleRate = (m_iBaseGreatPeopleRate + iChange);
	FAssert(getBaseGreatPeopleRate() >= 0);
}


// TODO: implemented in header but should contain Shwedagon Paya effect
int CvCity::getGreatPeopleRateModifier() const
{
	if (isHasBuildingEffect(SHWEDAGON_PAYA))
	{
		return m_iGreatPeopleRateModifier + GET_PLAYER(getOwner()).getCommercePercent(COMMERCE_GOLD);
	}

	return m_iGreatPeopleRateModifier;
}


void CvCity::changeGreatPeopleRateModifier(int iChange)
{
	m_iGreatPeopleRateModifier += iChange;
}

// BUG - Building Additional Great People - start
/*  Returns the total additional great people rate that adding one of the given buildings will provide.
	Doesn't check if the building can be constructed in this city. */
int CvCity::getAdditionalGreatPeopleRateByBuilding(BuildingTypes eBuilding) const
{
	int iRate = getBaseGreatPeopleRate();
	int iModifier = getTotalGreatPeopleRateModifier();
	int iExtra = ((iRate + getAdditionalBaseGreatPeopleRateByBuilding(eBuilding)) *
			(iModifier + getAdditionalGreatPeopleRateModifierByBuilding(eBuilding)) / 100) -
			(iRate * iModifier / 100);

	return iExtra;
}

/*  Returns the additional great people rate that adding one of the given buildings will provide.
	Doesn't check if the building can be constructed in this city. */
int CvCity::getAdditionalBaseGreatPeopleRateByBuilding(BuildingTypes eBuilding) const
{
	CvBuildingInfo& kBuilding = GC.getInfo(eBuilding);
	int iExtraRate = kBuilding.getGreatPeopleRateChange();
	if (!GET_TEAM(getTeam()).isObsoleteBuilding(eBuilding))
	{
		FOR_EACH_NON_DEFAULT_PAIR(kBuilding.
			getFreeSpecialistCount(), Specialist, int)
		{
			iExtraRate += getAdditionalBaseGreatPeopleRateBySpecialist(
					perSpecialistVal.first, perSpecialistVal.second);
		}
	}
	return iExtraRate;
}

// Doesn't check if the building can be constructed in this city.
int CvCity::getAdditionalGreatPeopleRateModifierByBuilding(BuildingTypes eBuilding) const
{
	int iExtraModifier = 0;
	if (!GET_TEAM(getTeam()).isObsoleteBuilding(eBuilding))
	{
		CvBuildingInfo& kBuilding = GC.getInfo(eBuilding);
		iExtraModifier += kBuilding.getGreatPeopleRateModifier();
		iExtraModifier += kBuilding.getGlobalGreatPeopleRateModifier();
	}

	return iExtraModifier;
}
// BUG - Building Additional Great People - end


// BUG - Specialist Additional Great People - start
/*  Returns the total additional great people rate that
	changing the number of the given specialist will provide/remove. */
int CvCity::getAdditionalGreatPeopleRateBySpecialist(SpecialistTypes eSpecialist, int iChange) const
{
	int iRate = getBaseGreatPeopleRate();
	int iModifier = getTotalGreatPeopleRateModifier();
	int iExtraRate = getAdditionalBaseGreatPeopleRateBySpecialist(eSpecialist, iChange);
	int iExtra = ((iRate + iExtraRate) * iModifier / 100) - (iRate * iModifier / 100);
	return iExtra;
}

/*  Returns the additional great people rate that
	changing the number of the given specialist will provide/remove. */
int CvCity::getAdditionalBaseGreatPeopleRateBySpecialist(SpecialistTypes eSpecialist, int iChange) const
{
	return iChange * GC.getInfo(eSpecialist).getGreatPeopleRateChange();
}
// BUG - Specialist Additional Great People - end

void CvCity::changeGreatPeopleProgress(int iChange)
{
	// <advc.078>
	if(m_iGreatPeopleProgress <= 0 && iChange > 0)
		GET_PLAYER(getOwner()).reportFirstGPP(); // </advc.078>
	m_iGreatPeopleProgress += iChange;
	FAssert(getGreatPeopleProgress() >= 0);
}


void CvCity::changeNumWorldWonders(int iChange)
{
	m_iNumWorldWonders += iChange;
	FAssert(getNumWorldWonders() >= 0);
}


void CvCity::changeNumTeamWonders(int iChange)
{
	m_iNumTeamWonders += iChange;
	FAssert(getNumTeamWonders() >= 0);
}


void CvCity::changeNumNationalWonders(int iChange)
{
	m_iNumNationalWonders += iChange;
	FAssert(getNumNationalWonders() >= 0);
}


void CvCity::changeNumBuildings(int iChange)
{
	m_iNumBuildings += iChange;
	FAssert(getNumBuildings() >= 0);
}


void CvCity::changeGovernmentCenterCount(int iChange)
{
	if (iChange != 0)
	{
		m_iGovernmentCenterCount += iChange;
		FAssert(getGovernmentCenterCount() >= 0);
		GET_PLAYER(getOwner()).updateMaintenance();
	}
}

// BUG - Building Saved Maintenance:
/*  Returns the total additional gold from saved maintenance times 100
	that adding one of the given buildings will provide.
	Doesn't check if the building can be constructed in this city. */
int CvCity::getSavedMaintenanceTimes100ByBuilding(BuildingTypes eBuilding) const
{
	CvBuildingInfo const& kBuilding = GC.getInfo(eBuilding);
	int iModifier = kBuilding.getMaintenanceModifier();
	if (iModifier != 0 && !isNoMaintenance())
	{
		int iNewMaintenance = calculateBaseMaintenanceTimes100() *
				std::max(0, getMaintenanceModifier() + iModifier + 100) / 100;
		return intdiv::round((getMaintenanceTimes100() - iNewMaintenance) *
				(100 + GET_PLAYER(getOwner()).calculateInflationRate()), 100); // K-Mod
	}
	return 0;
}


void CvCity::updateMaintenance()
{
	PROFILE_FUNC();

	int iOldMaintenance = getMaintenanceTimes100();
	int iNewMaintenance = 0;

	if (!isNoMaintenance())
	{
		iNewMaintenance = (calculateBaseMaintenanceTimes100() *
				std::max(0, getMaintenanceModifier() + 100)) / 100;
	}

	if (iOldMaintenance != iNewMaintenance)
	{
		FAssert(iOldMaintenance >= 0);
		FAssert(iNewMaintenance >= 0);

		m_iMaintenance = iNewMaintenance;
		FAssert(getMaintenance() >= 0);

		GET_PLAYER(getOwner()).changeTotalMaintenance(getMaintenanceTimes100() - iOldMaintenance);
	}
}

int CvCity::calculateDistanceMaintenance() const
{
	return calculateDistanceMaintenanceTimes100() / 100;
}

// advc.104: Added parameter
int CvCity::calculateDistanceMaintenanceTimes100(PlayerTypes eOwner) const
{
	// advc.004b: BtS code moved into new static function
	return CvCity::calculateDistanceMaintenanceTimes100(getPlot(),
			eOwner == NO_PLAYER ? getOwner() : eOwner, getPopulation());
}

int CvCity::calculateNumCitiesMaintenance() const
{
	return calculateNumCitiesMaintenanceTimes100() / 100;
}

// advc.104: Added parameter
int CvCity::calculateNumCitiesMaintenanceTimes100(PlayerTypes eOwner) const
{
	// advc.004b: BtS code moved into new static function
	return calculateNumCitiesMaintenanceTimes100(getPlot(),
			eOwner == NO_PLAYER ? getOwner() : eOwner,
			getPopulation());
}

int CvCity::calculateColonyMaintenance() const
{
	return calculateColonyMaintenanceTimes100() / 100;
}

// advc.104: Added parameter
int CvCity::calculateColonyMaintenanceTimes100(PlayerTypes eOwner) const
{
	// advc.004b: BtS code moved into new static function
	return calculateColonyMaintenanceTimes100(getPlot(),
			eOwner == NO_PLAYER ? getOwner() : eOwner,
			getPopulation());
}


int CvCity::calculateCorporationMaintenance() const
{
	return calculateCorporationMaintenanceTimes100() / 100;
}

int CvCity::calculateCorporationMaintenanceTimes100() const
{
	int iMaintenance = 0;
	FOR_EACH_ENUM(Corporation)
	{
		if (isActiveCorporation(eLoopCorporation))
			iMaintenance += calculateCorporationMaintenanceTimes100(eLoopCorporation);
	}
	FAssert(iMaintenance >= 0);
	return iMaintenance;
}

int CvCity::calculateCorporationMaintenanceTimes100(CorporationTypes eCorporation) const
{
	int iMaintenance = 0;
	FOR_EACH_ENUM(Commerce)
	{
		iMaintenance += 100 * GC.getInfo(eCorporation).
				getHeadquarterCommerce(eLoopCommerce);
	}

	int iNumBonuses = 0;
	for (int i = 0; i < GC.getInfo(eCorporation).getNumPrereqBonuses(); i++)
	{
		iNumBonuses += getNumBonuses(GC.getInfo(eCorporation).getPrereqBonus(i));
	}

	int iBonusMaintenance = GC.getInfo(eCorporation).getMaintenance() * iNumBonuses;
	iBonusMaintenance *= GC.getInfo(GC.getMap().getWorldSize()).
			getCorporationMaintenancePercent();
	iBonusMaintenance /= 100;
	iMaintenance += iBonusMaintenance;

	iMaintenance *= getPopulation() + 17;
	iMaintenance /= 18;

	iMaintenance *= GC.getInfo(getHandicapType()).getCorporationMaintenancePercent();
	iMaintenance /= 100;

	iMaintenance *= std::max(0, GET_PLAYER(getOwner()).
			getCorporationMaintenanceModifier() + 100);
	iMaintenance /= 100;

	int iInflation = GET_PLAYER(getOwner()).calculateInflationRate() + 100;
	if (iInflation > 0)
	{
		iMaintenance *= 100;
		iMaintenance /= iInflation;
	}

	/*	K-Mod note. This assert (and others like it) can fail sometimes during the process
		of updating plot groups; because the # of bonuses can be temporarily negative. */
	FAssert(iMaintenance >= 0);
	return iMaintenance;
}


int CvCity::calculateBaseMaintenanceTimes100(
	/* <advc.ctr> */ PlayerTypes eOwner) const
{
	if (eOwner == NO_PLAYER)
		eOwner = getOwner(); // </advc.ctr>
	int iR = calculateDistanceMaintenanceTimes100(eOwner) +
			calculateNumCitiesMaintenanceTimes100(eOwner) +
			calculateColonyMaintenanceTimes100(eOwner);
	// advc.ctr: Anticipating corporation maintenance gets too complicated
	if (eOwner == getOwner())
		iR += calculateCorporationMaintenanceTimes100();
	return iR;
}


void CvCity::changeMaintenanceModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iMaintenanceModifier += iChange;
		updateMaintenance();
	}
}


void CvCity::changeWarWearinessModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iWarWearinessModifier += iChange;
		AI_setAssignWorkDirty(true);
	}
}


void CvCity::changeHurryAngerModifier(int iChange)
{
	if (iChange == 0)
		return;

	int iRatio = 0;
	if (m_iHurryAngerTimer > 0)
	{
		iRatio = (100 * (m_iHurryAngerTimer - 1)) /
				std::max(1, 100 + getHurryAngerModifier());
	}
	m_iHurryAngerModifier += iChange;
	if (m_iHurryAngerTimer > 0)
	{
		m_iHurryAngerTimer = (iRatio *
				std::max(1, 100 + getHurryAngerModifier())) / 100 + 1;
	}
}


void CvCity::changeHealRate(int iChange)
{
	m_iHealRate += iChange;
	FAssert(getHealRate() >= 0);
}


void CvCity::changeEspionageHealthCounter(int iChange)
{
	m_iEspionageHealthCounter += iChange;
}


void CvCity::changeEspionageHappinessCounter(int iChange)
{
	m_iEspionageHappinessCounter += iChange;
}


void CvCity::updateFreshWaterHealth()
{
	int iNewGoodHealth = 0;
	int iNewBadHealth = 0;

	if (getPlot().isFreshWater())
	{
		if (GC.getDefineINT(CvGlobals::FRESH_WATER_HEALTH_CHANGE) > 0)
			iNewGoodHealth += GC.getDefineINT(CvGlobals::FRESH_WATER_HEALTH_CHANGE);
		else iNewBadHealth += GC.getDefineINT(CvGlobals::FRESH_WATER_HEALTH_CHANGE);
	}

	if (getFreshWaterGoodHealth() != iNewGoodHealth || getFreshWaterBadHealth() != iNewBadHealth)
	{
		m_iFreshWaterGoodHealth = iNewGoodHealth;
		m_iFreshWaterBadHealth = iNewBadHealth;
		FAssert(getFreshWaterGoodHealth() >= 0);
		FAssert(getFreshWaterBadHealth() <= 0);

		AI_setAssignWorkDirty(true);

		if (isActiveTeam())
			setInfoDirty(true);
	}
}

// advc.901: Use one update function for both health and happiness
void CvCity::updateSurroundingHealthHappiness()
{
	PROFILE_FUNC(); // advc.901: Now called once per turn; seems fine.
	int iNewGoodHappiness = 0;
	int iNewBadHappiness = 0;
	CvTeam const& kTeam = GET_TEAM(getTeam()); // advc.901
	for (CityPlotIter it(*this); it.hasNext(); ++it)
	{
		CvPlot const& kPlot = *it;
		{
			FeatureTypes eFeature = kPlot.getFeatureType();
			if (eFeature != NO_FEATURE)
			{
				int iHappy = GET_PLAYER(getOwner()).getFeatureHappiness(eFeature);
				if (kTeam.canAccessHappyHealth(kPlot, iHappy)) // advc.901
					(iHappy > 0 ? iNewGoodHappiness : iNewBadHappiness) += iHappy;
			}
		}
		{
			ImprovementTypes eImprovement = kPlot.getImprovementType();
			if (eImprovement != NO_IMPROVEMENT)
			{
				int iHappy = GC.getInfo(eImprovement).getHappiness();
				if (kTeam.canAccessHappyHealth(kPlot, iHappy)) // advc.901
					(iHappy > 0 ? iNewGoodHappiness : iNewBadHappiness) += iHappy;
			}

			// Temple of Kukulkan effect: +1 happiness from working Plantations
			if (eImprovement == IMPROVEMENT_PLANTATION)
			{
				if (GET_PLAYER(getOwner()).isHasBuildingEffect(TEMPLE_OF_KUKULKAN))
				{
					if (kPlot.getWorkingCity() == this)
					{
						iNewGoodHappiness += 1;
					}
				}
			}
		}
	}
	bool bDirty = false;
	if (getSurroundingGoodHappiness() != iNewGoodHappiness)
	{
		m_iSurroundingGoodHappiness = iNewGoodHappiness;
		FAssert(getSurroundingGoodHappiness() >= 0);
		bDirty = true;
	}
	if (getSurroundingBadHappiness() != iNewBadHappiness)
	{
		m_iSurroundingBadHappiness = iNewBadHappiness;
		FAssert(getSurroundingBadHappiness() <= 0);
		bDirty = true;
	}
	std::pair<int,int> iiGoodBad = calculateSurroundingHealth(); // advc.901: Moved into new function
	if (getSurroundingGoodHealth() != iiGoodBad.first ||
		getSurroundingBadHealth() != iiGoodBad.second)
	{
		m_iSurroundingGoodHealth = iiGoodBad.first;
		m_iSurroundingBadHealth = iiGoodBad.second;
		FAssert(getSurroundingGoodHealth() >= 0);
		FAssert(getSurroundingBadHealth() <= 0);
		bDirty = true;
	}
	if (bDirty)
	{
		AI_setAssignWorkDirty(true);
		if (isActiveTeam())
			setInfoDirty(true);
	}
}

// advc.901: Body cut from updateFeatureHealth; the parameter is new.
std::pair<int,int> CvCity::calculateSurroundingHealth(int iGoodExtraPercent, int iBadExtraPercent) const
{
	int iGoodHealth = iGoodExtraPercent;
	int iBadHealth = iBadExtraPercent;
	CvTeam const& kTeam = GET_TEAM(getTeam()); // advc.901
	for (CityPlotIter it(*this); it.hasNext(); ++it)
	{
		CvPlot const& kPlot = *it;
		{
			FeatureTypes eFeature = kPlot.getFeatureType();
			if (eFeature != NO_FEATURE)
			{
				int iHealthPercent = GC.getInfo(eFeature).getHealthPercent();

                // doc: Congo UP: no unhealth from jungle and marsh
				if (getCivilizationType() == CONGO && (eFeature == FEATURE_JUNGLE || eFeature == FEATURE_MARSH))
					iHealthPercent = 0;

                // doc: Hanging Gardens: no unhealth from flood plains
				if (GET_PLAYER(getOwner()).isHasBuildingEffect(HANGING_GARDENS) && eFeature == FEATURE_FLOOD_PLAINS)
					iHealthPercent = 0;

				if (kTeam.canAccessHappyHealth(kPlot, iHealthPercent)) // advc.901
					(iHealthPercent > 0 ? iGoodHealth : iBadHealth) += iHealthPercent;
			}
		}  // <advc.901> (based on updateFeatureHappiness)
		ImprovementTypes eImprovement = kPlot.getImprovementType();
		if (eImprovement != NO_IMPROVEMENT)
		{
			int iHealthPercent = GC.getInfo(eImprovement).get(CvImprovementInfo::HealthPercent);
			if (kTeam.canAccessHappyHealth(kPlot, iHealthPercent))
				(iHealthPercent > 0 ? iGoodHealth : iBadHealth) += iHealthPercent;
		} // </advc.901>
	}
	return std::make_pair(iGoodHealth / 100, iBadHealth / 100);
}

/*  <advc.901> This was previously handled (badly) by CvCityAI::AI_getImprovementValue.
	Returns the change in health, rounded (iHealthChange) and as a percentage
	(iHealthChangePercent), and the change in happiness (iHappyChange) that would
	result from replacing eOldImprov with eNewImprov in kPlot and possibly
	removing kPlot's feature.
	This function is for AI purposes (no need to tally good and bad effects
	separately), the one below is for UI purposes. */
void CvCity::calculateHealthHappyChange(CvPlot const& kPlot,
	ImprovementTypes eNewImprov, ImprovementTypes eOldImprov, bool bRemoveFeature,
	int& iHappyChange, int& iHealthChange, int& iHealthPercentChange) const
{
	int iGoodHappyChange, iBadHappyChange, iGoodHealthChange, iBadHealthChange,
			iGoodHealthPercentChange, iBadHealthPercentChange;
	goodBadHealthHappyChange(kPlot, eNewImprov, eOldImprov, bRemoveFeature,
			iGoodHappyChange, iBadHappyChange, iGoodHealthChange, iBadHealthChange,
			iGoodHealthPercentChange, iBadHealthPercentChange);
	iHappyChange = iGoodHappyChange + iBadHappyChange;
	iHealthChange = iGoodHealthChange + iBadHealthChange;
	iHealthPercentChange = iGoodHealthPercentChange + iBadHealthPercentChange;
}

/*  Positive and negative effects need to be tallied separately for "correct"
	rounding - as in BtS: bad jungle health and good forest health are rounded
	separately. */
void CvCity::goodBadHealthHappyChange(CvPlot const& kPlot, ImprovementTypes eNewImprov,
	ImprovementTypes eOldImprov, bool bRemoveFeature, int& iHappyChange,
	int& iUnhappyChange, int& iGoodHealthChange, int& iBadHealthChange,
	int& iGoodHealthPercentChange, int& iBadHealthPercentChange) const
{
	iHappyChange = iUnhappyChange = iGoodHealthChange = iBadHealthChange =
			iGoodHealthPercentChange = iBadHealthPercentChange = 0;
	if (eNewImprov == eOldImprov && !bRemoveFeature)
		return;

	CvTeam const& kTeam = GET_TEAM(getTeam());
	int iFeatureHappy = 0;
	int iFeatureGoodHealthPercent = 0;
	int iFeatureUnhappy = 0;
	int iFeatureBadHealthPercent = 0;
	if (bRemoveFeature)
	{
		FeatureTypes eFeature = kPlot.getFeatureType();
		if (eFeature != NO_FEATURE)
		{
			int iHappy = GET_PLAYER(getOwner()).getFeatureHappiness(eFeature);
			if (kTeam.canAccessHappyHealth(kPlot, iHappy))
				(iHappy > 0 ? iFeatureHappy : iFeatureUnhappy) = iHappy;
			int iHealthPercent = GC.getInfo(eFeature).getHealthPercent();
			if (kTeam.canAccessHappyHealth(kPlot, iHealthPercent))
			{
				(iHealthPercent > 0 ? iFeatureGoodHealthPercent :
						iFeatureBadHealthPercent) += iHealthPercent;
			}
		}
	}
	int iNewHappy = 0;
	int iNewUnhappy = 0;
	int iNewGoodHealthPercent = 0;
	int iNewBadHealthPercent = 0;
	if (eNewImprov != NO_IMPROVEMENT)
	{
		int iHappy = GC.getInfo(eNewImprov).getHappiness();
		if (kTeam.canAccessHappyHealth(kPlot, iHappy))
			(iHappy > 0 ? iNewHappy : iNewUnhappy) = iHappy;
		int iHealthPercent = GC.getInfo(eNewImprov).get(CvImprovementInfo::HealthPercent);
		if (kTeam.canAccessHappyHealth(kPlot, iHealthPercent))
			(iHealthPercent > 0 ? iNewGoodHealthPercent : iNewBadHealthPercent) += iHealthPercent;
	}
	int iOldHappy = 0;
	int iOldUnhappy = 0;
	int iOldGoodHealthPercent = 0;
	int iOldBadHealthPercent = 0;
	if (eOldImprov != NO_IMPROVEMENT)
	{
		int iHappy = GC.getInfo(eOldImprov).getHappiness();
		if (kTeam.canAccessHappyHealth(kPlot, iHappy))
			(iHappy > 0 ? iOldHappy : iOldUnhappy) = iHappy;
		int iHealthPercent = GC.getInfo(eOldImprov).get(CvImprovementInfo::HealthPercent);
		if (kTeam.canAccessHappyHealth(kPlot, iHealthPercent))
			(iHealthPercent > 0 ? iOldGoodHealthPercent : iOldBadHealthPercent) += iHealthPercent;
	}
	iHappyChange = iNewHappy - iOldHappy - iFeatureHappy;
	iUnhappyChange = iNewUnhappy - iOldUnhappy - iFeatureUnhappy;

	iGoodHealthPercentChange = iNewGoodHealthPercent - iOldGoodHealthPercent - iFeatureGoodHealthPercent;
	iBadHealthPercentChange = iNewBadHealthPercent - iOldBadHealthPercent - iFeatureBadHealthPercent;
	std::pair<int,int> iiNewHealth = calculateSurroundingHealth(iGoodHealthPercentChange, iBadHealthPercentChange);
	std::pair<int,int> iiOldHealth = calculateSurroundingHealth();
	iGoodHealthChange = iiNewHealth.first - iiOldHealth.first;
	iBadHealthChange = iiNewHealth.second - iiOldHealth.second;
} // </advc.901>

// BUG - Actual Effects - start
/*	Returns the additional angry population caused by the given happiness changes.
	Positive values for iBad mean an increase in unhappiness. */
int CvCity::getAdditionalAngryPopuplation(int iGood, int iBad) const
{
	int iHappy = happyLevel();
	int iUnhappy = unhappyLevel();
	int iPop = getPopulation();
	return range((iUnhappy + iBad) - (iHappy + iGood), 0, iPop) -
			range(iUnhappy - iHappy, 0, iPop);
}

/*  Returns the additional spoiled food caused by the given health changes.
	Positive values for iBad mean an increase in unhealthiness. */
int CvCity::getAdditionalSpoiledFood(int iGood, int iBad) const
{
	int iHealthy = goodHealth();
	int iUnhealthy = badHealth();
	int iRate = iHealthy - iUnhealthy;
	return std::min(0, iRate) - std::min(0, iRate + iGood - iBad);
}

// Returns the additional starvation caused by the given spoiled food.
int CvCity::getAdditionalStarvation(int iSpoiledFood) const
{
	int iFood = getYieldRate(YIELD_FOOD) - foodConsumption();
	if (iSpoiledFood > 0)
	{
		if (iFood <= 0)
			return iSpoiledFood;
		if (iSpoiledFood > iFood)
			return iSpoiledFood - iFood;
	}
	else if (iSpoiledFood < 0)
	{
		if (iFood < 0)
			return std::max(iFood, iSpoiledFood);
	}
	return 0;
} // BUG - Actual Effects - end

/*  <advc.001c> These two functions are based on code cut from
	CvGameTextMgr::parseGreatPeopleHelp */
int CvCity::GPTurnsLeft() const
{
	if(getGreatPeopleRate() <= 0)
		return -1;
	int iGPPLeft = GET_PLAYER(getOwner()).greatPeopleThreshold(false) - getGreatPeopleProgress();
	if (iGPPLeft <= 0)
		return 0;
	int iR = iGPPLeft / getGreatPeopleRate();
	if (iR * getGreatPeopleRate() < iGPPLeft)
		iR++;
	return iR;
}

void CvCity::GPProjection(std::vector<std::pair<UnitTypes,int> >& aeiProjection) const
{
	if (isDisorder())
		return;
	CvCivilization const& kCiv = getCivilization();
	int const iTurnsLeft = GPTurnsLeft();
	/*  (advc.001c: Can't use getGreatPeopleProgress() b/c the
		per-unit progress values won't add up to that in old saves.) */
	int iTotalUnitProgress = 0;
	for (int i = 0; i < kCiv.getNumUnits(); i++)
		iTotalUnitProgress += getGreatPeopleUnitProgress(kCiv.unitAt(i));
	/*	GPP total of the city on the turn that the GP will be born.
		(Usually greater than GET_PLAYER(getOwner()).greatPeopleThreshold().) */
	int iProjectedTotal = iTotalUnitProgress + iTurnsLeft * getGreatPeopleRate();
	int iRoundedPercentages = 0;
	FOR_EACH_ENUM(Unit)
	{
		scaled rShare = (getGreatPeopleUnitProgress(eLoopUnit) +
				per100(iTurnsLeft * getGreatPeopleUnitRate(eLoopUnit) *
				getTotalGreatPeopleRateModifier())) / iProjectedTotal;
		if (rShare > 0)
		{
			/*	I've seen 103 here with the Parthenon (150% modifier).
				Haven't investigated in detail, but I'm guessing that the calculation
				in the loop has fewer rounding errors than the one before the loop. */
			int iPercent = std::min(100, rShare.getPercent());
			iRoundedPercentages += iPercent;
			aeiProjection.push_back(std::make_pair(eLoopUnit, iPercent));
		}
	}
	if (!aeiProjection.empty())
	{
		int iTotalError = 100 - iRoundedPercentages;
		if (iTotalError >= 2)
		{
			FAssert(iTotalError == 2);
			/*	I'm too lazy to handle that error properly. Adding up to 99% is OK.
				Otherwise add 1 to the GP with the highest share. */
			size_t iArgmax = 0;
			int iMax = 0;
			for (size_t i = 0; i < aeiProjection.size(); i++)
			{
				if (aeiProjection[i].second > iMax)
				{
					iMax = aeiProjection[i].second;
					iArgmax = i;
				}
			}
			aeiProjection[iArgmax].second += iTotalError - 1;
		}
	}
} // </advc.001c>


int CvCity::getBuildingHealth(BuildingTypes eBuilding) const
{
	int iHealth = getBuildingGoodHealth(eBuilding);
	if (!isBuildingOnlyHealthy())
		iHealth += getBuildingBadHealth(eBuilding);
	return iHealth;
}

int CvCity::getBuildingGoodHealth(BuildingTypes eBuilding) const
{
	int iHealth = std::max(0, GC.getInfo(eBuilding).getHealth());
	iHealth += std::max(0, getBuildingHealthChange(
			GC.getInfo(eBuilding).getBuildingClassType()));
	iHealth += std::max(0, GET_PLAYER(getOwner()).getExtraBuildingHealth(eBuilding));

    // doc: Indian UP: +1 health from happiness buildings
    if (getCivilizationType() == INDIA && GC.getInfo(eBuilding).getHappiness() > 0)
        iHealth += 1;

    return iHealth;
}

int CvCity::getBuildingBadHealth(BuildingTypes eBuilding) const
{
	if (isBuildingOnlyHealthy())
		return 0;
	int iHealth = std::min(0, GC.getInfo(eBuilding).getHealth());
	iHealth += std::min(0, getBuildingHealthChange(
			GC.getInfo(eBuilding).getBuildingClassType()));
	iHealth += std::min(0, GET_PLAYER(getOwner()).getExtraBuildingHealth(eBuilding));
	return iHealth;
}

void CvCity::changeBuildingGoodHealth(int iChange)
{
	if (iChange == 0)
		return;
	m_iBuildingGoodHealth += iChange;
	FAssert(getBuildingGoodHealth() >= 0);
	AI_setAssignWorkDirty(true);
	if (isActiveTeam())
		setInfoDirty(true);
}


void CvCity::changeBuildingBadHealth(int iChange)
{
	if (iChange == 0)
		return;
	m_iBuildingBadHealth += iChange;
	FAssert(getBuildingBadHealth() <= 0);
	AI_setAssignWorkDirty(true);
	if (isActiveTeam())
		setInfoDirty(true);
}


void CvCity::updatePowerHealth()
{
	int iNewGoodHealth = 0;
	int iNewBadHealth = 0;

	int iPowerConsumed = getPowerConsumedCount();

	if (isPower())
	{
        // doc: power health scales with amount of power
		int iPowerHealth = GC.getDefineINT(CvGlobals::POWER_HEALTH_CHANGE) * iPowerConsumed;
		if (iPowerHealth > 0)
			iNewGoodHealth += iPowerHealth;
		else iNewBadHealth += iPowerHealth;
	}

	if (isDirtyPower())
	{
        // doc: power health scales with amount of power
		int iDirtyPowerHealth = GC.getDefineINT(CvGlobals::DIRTY_POWER_HEALTH_CHANGE) * iPowerConsumed;
		if (iDirtyPowerHealth > 0)
			iNewGoodHealth += iDirtyPowerHealth;
		else iNewBadHealth += iDirtyPowerHealth;
	}

	if (getPowerGoodHealth() != iNewGoodHealth ||
		getPowerBadHealth() != iNewBadHealth)
	{
		m_iPowerGoodHealth = iNewGoodHealth;
		m_iPowerBadHealth = iNewBadHealth;
		FAssert(getPowerGoodHealth() >= 0);
		FAssert(getPowerBadHealth() <= 0);
		AI_setAssignWorkDirty(true);
		if (isActiveTeam())
			setInfoDirty(true);
	}
}


void CvCity::changeBonusGoodHealth(int iChange)
{
	if (iChange == 0)
		return; // advc
	m_iBonusGoodHealth += iChange;
	FAssert(getBonusGoodHealth() >= 0);
	AI_setAssignWorkDirty(true);
	if (isActiveTeam())
		setInfoDirty(true);
}


void CvCity::changeBonusBadHealth(int iChange)
{
	if (iChange == 0)
		return; // advc
	m_iBonusBadHealth += iChange;
	FAssert(getBonusBadHealth() <= 0);
	AI_setAssignWorkDirty(true);
	if (isActiveTeam())
		setInfoDirty(true);
}


int CvCity::getMilitaryHappiness() const
{
    // doc: military happiness limited to half of city size
	return std::min(getMilitaryHappinessUnits() * GET_PLAYER(getOwner()).getHappyPerMilitaryUnit(), getPopulation() / 2);
}


void CvCity::changeMilitaryHappinessUnits(int iChange)
{
	if (iChange == 0)
		return;
	m_iMilitaryHappinessUnits += iChange;
	FAssert(getMilitaryHappinessUnits() >= 0);
	AI_setAssignWorkDirty(true);
	// <advc.004> Update the unhappiness indicator
	if (isActiveOwned())
		gDLL->UI().setDirty(CityInfo_DIRTY_BIT, true); // </advc.004>
}

// advc.184: Cut from init
void CvCity::updateMilitaryHappinessUnits()
{
	changeMilitaryHappinessUnits(getPlot().plotCount(PUF_isMilitaryHappiness)
			- getMilitaryHappinessUnits());
}


int CvCity::getBuildingHappiness(BuildingTypes eBuilding) const
{
	CvBuildingInfo const& kBuilding = GC.getInfo(eBuilding);
	int iHappiness = kBuilding.getHappiness();

    // doc: happiness from culture level
	iHappiness += kBuilding.getCultureHappiness() * getCultureLevel();

	if (kBuilding.getReligionType() != NO_RELIGION)
	{
		if (kBuilding.getReligionType() == GET_PLAYER(getOwner()).getStateReligion())
			iHappiness += kBuilding.getStateReligionHappiness();
	}
	iHappiness += GET_PLAYER(getOwner()).getExtraBuildingHappiness(eBuilding);

	FOR_EACH_ENUM(Commerce)
	{
		iHappiness += (kBuilding.getCommerceHappiness(eLoopCommerce) *
				GET_PLAYER(getOwner()).getCommercePercent(eLoopCommerce)) / 100;
	}
	iHappiness += getBuildingHappyChange(kBuilding.getBuildingClassType());

	return iHappiness;
}


void CvCity::changeBuildingGoodHappiness(int iChange)
{
	if (iChange != 0)
	{
		m_iBuildingGoodHappiness += iChange;
		FAssert(getBuildingGoodHappiness() >= 0);
		AI_setAssignWorkDirty(true);
	}
}


void CvCity::changeBuildingBadHappiness(int iChange)
{
	if (iChange != 0)
	{
		m_iBuildingBadHappiness += iChange;
		FAssert(getBuildingBadHappiness() <= 0);
		AI_setAssignWorkDirty(true);
	}
}


void CvCity::updateExtraBuildingHappiness()
{
	int iNewExtraBuildingGoodHappiness = 0;
	int iNewExtraBuildingBadHappiness = 0;

	CvCivilization const& kCiv = getCivilization();
	for (int i = 0; i < kCiv.getNumBuildings(); i++)
	{
		BuildingTypes const eBuilding = kCiv.buildingAt(i);
		int iChange = getNumActiveBuilding(eBuilding) *
				GET_PLAYER(getOwner()).getExtraBuildingHappiness(eBuilding);
		if (iChange > 0)
			iNewExtraBuildingGoodHappiness += iChange;
		else iNewExtraBuildingBadHappiness += iChange;
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

/*  BETTER_BTS_AI_MOD, City AI, 02/24/10, EmperorFool: START
	(BUG - Building Additional Happiness) */
namespace // advc: These had been declared as global functions in the header
{
	// Adds iValue to iGood if it is positive or its negative to iBad if it is negative.
	void addGoodOrBad(int iValue, int& iGood, int& iBad)
	{
		if (iValue > 0)
			iGood += iValue;
		else if (iValue < 0)
			iBad -= iValue;
	}

	// Subtracts iValue from iGood if it is positive or its negative from iBad if it is negative.
	void subtractGoodOrBad(int iValue, int& iGood, int& iBad)
	{
		if (iValue > 0)
			iGood -= iValue;
		else if (iValue < 0)
			iBad += iValue;
	}
}

/*	Returns the total additional happiness that adding one of the given buildings
	will provide and sets the good and bad levels individually.
	Doesn't reset iGood or iBad to zero.
	Doesn't check if the building can be constructed in this city. */
int CvCity::getAdditionalHappinessByBuilding(BuildingTypes eBuilding, int& iGood, int& iBad) const
{
	CvBuildingInfo& kBuilding = GC.getInfo(eBuilding);
	CvPlayer const& kOwner = GET_PLAYER(getOwner());

	int const iStarting = iGood - iBad;
	int const iStartingBad = iBad;

	// Basic
	addGoodOrBad(kBuilding.getHappiness(), iGood, iBad);

	// Building Class
	addGoodOrBad(getBuildingHappyChange(kBuilding.getBuildingClassType()), iGood, iBad);

	// Player Building
	addGoodOrBad(kOwner.getExtraBuildingHappiness(eBuilding), iGood, iBad);

	// Area
	addGoodOrBad(kBuilding.getAreaHappiness(), iGood, iBad);

	// Religion
	if (kBuilding.getReligionType() != NO_RELIGION &&
		kBuilding.getReligionType() == kOwner.getStateReligion())
	{
		iGood += kBuilding.getStateReligionHappiness();
	}

	// Bonus
	FOR_EACH_NON_DEFAULT_PAIR(kBuilding.
		getBonusHappinessChanges(), Bonus, int)
	{
		BonusTypes const eLoopBonus = perBonusVal.first;
		if ((hasBonus(eLoopBonus) || kBuilding.getFreeBonus() == eLoopBonus) &&
			kBuilding.getNoBonus() != eLoopBonus)
		{
			addGoodOrBad(perBonusVal.second, iGood, iBad);
		}
	}
	// Commerce
	FOR_EACH_ENUM(Commerce)
	{
		addGoodOrBad(kBuilding.getCommerceHappiness(eLoopCommerce) *
				kOwner.getCommercePercent(eLoopCommerce) / 100, iGood, iBad);
	}

	// War Weariness Modifier
	if (kBuilding.getWarWearinessModifier() != 0)
	{
		int iBaseAngerPercent = 0;
		iBaseAngerPercent += getOvercrowdingPercentAnger();
		iBaseAngerPercent += getNoMilitaryPercentAnger();
		iBaseAngerPercent += getCulturePercentAnger();
		iBaseAngerPercent += getReligionPercentAnger();
		iBaseAngerPercent += getHurryPercentAnger();
		iBaseAngerPercent += getConscriptPercentAnger();
		iBaseAngerPercent += getDefyResolutionPercentAnger();
		FOR_EACH_ENUM(Civic)
		{
			iBaseAngerPercent += kOwner.getCivicPercentAnger(eLoopCivic);
		}

		int iCurrentAngerPercent = iBaseAngerPercent + getWarWearinessPercentAnger();
		int iCurrentUnhappiness = iCurrentAngerPercent * getPopulation() /
				GC.getPERCENT_ANGER_DIVISOR();

		int iNewWarAngerPercent = kOwner.getWarWearinessPercentAnger();
		iNewWarAngerPercent *= std::max(0, kBuilding.getWarWearinessModifier() +
				getWarWearinessModifier() + kOwner.getWarWearinessModifier() + 100);
		iNewWarAngerPercent /= 100;
		int iNewAngerPercent = iBaseAngerPercent + iNewWarAngerPercent;
		int iNewUnhappiness = iNewAngerPercent * getPopulation() / GC.getPERCENT_ANGER_DIVISOR();

		iBad += iNewUnhappiness - iCurrentUnhappiness;
	}

	// K-Mod. If the city is immune to unhappiness, then clear the "bad" from this building.
	if (isNoUnhappiness())
		iBad = iStartingBad;
	// K-Mod end

	// No Unhappiness
	if (kBuilding.isNoUnhappiness())
	{
		// override extra unhappiness and completely negate all existing unhappiness
		iBad = iStartingBad - unhappyLevel();
	}

	return iGood - iBad - iStarting;
}

/*	Returns the total additional health that adding one of the given buildings
	will provide and sets the good and bad levels individually.
	Doesn't reset iGood or iBad to zero.
	Doesn't check if the building can be constructed in this city. */
int CvCity::getAdditionalHealthByBuilding(BuildingTypes eBuilding, int& iGood, int& iBad,
	bool bAssumeStrategicBonuses) const // advc.001h
{
	CvBuildingInfo& kBuilding = GC.getInfo(eBuilding);
	CvPlayer const& kOwner = GET_PLAYER(getOwner());

	int const iStarting = iGood - iBad;
	int const iStartingBad = iBad;

	// Basic
	addGoodOrBad(kBuilding.getHealth(), iGood, iBad);

	// Building Class
	addGoodOrBad(getBuildingHealthChange(kBuilding.getBuildingClassType()), iGood, iBad);

	// Player Building
	addGoodOrBad(kOwner.getExtraBuildingHealth(eBuilding), iGood, iBad);

	// Area
	addGoodOrBad(kBuilding.getAreaHealth(), iGood, iBad);

	// doc: Corporation health
	iBad += getCorporationUnhealth() * kBuilding.getCorporationUnhealthModifier() / 100;

	// doc: Indian UP: +1 health from buildings that provide happiness
	if (getCivilizationType() == INDIA && kBuilding.getHappiness() > 0)
		iGood += 1;

	// doc: building health modifier
	iBad += (iBad + totalBadBuildingHealth()) * kBuilding.getBuildingUnhealthModifier() / 100;

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
	FOR_EACH_NON_DEFAULT_PAIR(kBuilding.
		getBonusHealthChanges(), Bonus, int)
	{
		BonusTypes const eLoopBonus = perBonusVal.first;
		if ((hasBonus(eLoopBonus) || kBuilding.getFreeBonus() == eLoopBonus ||
			// <advc.001h>
			(bAssumeStrategicBonuses &&
			GC.getInfo(eLoopBonus).getHappiness() == 0 &&
			GC.getInfo(eLoopBonus).getHealth() == 0)) && // </advc.001h>
			kBuilding.getNoBonus() != eLoopBonus)
		{
			addGoodOrBad(perBonusVal.second, iGood, iBad);
		}
	}
	// advc.001h: Need this several times
	BonusTypes ePowBonus = kBuilding.getPowerBonus();
	// Power
	if (kBuilding.isPower() || kBuilding.isAreaCleanPower() ||
		(ePowBonus != NO_BONUS && (hasBonus(ePowBonus) ||
		// <advc.001h>
		(bAssumeStrategicBonuses &&
		GC.getInfo(ePowBonus).getHappiness() == 0 &&
		GC.getInfo(ePowBonus).getHealth() == 0)))) // </advc.001h>
	{
		// adding power
		if (!isPower())
		{
			addGoodOrBad(GC.getDefineINT(CvGlobals::POWER_HEALTH_CHANGE), iGood, iBad);

			// adding dirty power
			if (kBuilding.isDirtyPower())
			{
				addGoodOrBad(GC.getDefineINT(
						CvGlobals::DIRTY_POWER_HEALTH_CHANGE), iGood, iBad);
			}
		}
		/*	advc.001h: Count change from dirty to clean only if we
			already have the resource (i.e. Uranium) */
		else if(ePowBonus == NO_BONUS || hasBonus(ePowBonus))
		{
			// replacing dirty power with clean power
			if (isDirtyPower() && !kBuilding.isDirtyPower())
			{
				subtractGoodOrBad(GC.getDefineINT(
						CvGlobals::DIRTY_POWER_HEALTH_CHANGE), iGood, iBad);
			}
		}
	}
	// No Unhealthiness from Population
	/*if (kBuilding.isNoUnhealthyPopulation())
		iBad -= getPopulation();*/ // BtS
	/*  K-Mod, 27/dec/10, karadoc (start)
		replaced NoUnhealthyPopulation with UnhealthyPopulationModifier */
	// Modified unhealthiness from population
	int iEffectiveModifier = 0;
	if (kBuilding.getUnhealthyPopulationModifier() + getUnhealthyPopulationModifier() < -100)
		iEffectiveModifier = std::min(0, -100 - getUnhealthyPopulationModifier());
	else iEffectiveModifier = std::max(-100, kBuilding.getUnhealthyPopulationModifier());
	iBad += intdiv::round(getPopulation() * iEffectiveModifier, 100);
	// K-Mod end
	return iGood - iBad - iStarting;
}
// BETTER_BTS_AI_MOD: END

void CvCity::updateExtraBuildingHealth()
{
	int iNewExtraBuildingGoodHealth = 0;
	int iNewExtraBuildingBadHealth = 0;

	CvCivilization const& kCiv = getCivilization();
	for (int i = 0; i < kCiv.getNumBuildings(); i++)
	{
		BuildingTypes const eBuilding = kCiv.buildingAt(i);
		int iChange = getNumActiveBuilding(eBuilding) *
				GET_PLAYER(getOwner()).getExtraBuildingHealth(eBuilding);
		if (iChange > 0)
			iNewExtraBuildingGoodHealth += iChange;
		else iNewExtraBuildingBadHealth += iChange;
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


int CvCity::getBonusGoodHappiness(/* advc.912c: */ bool bIgnoreModifier) const
{
	//return m_iBonusGoodHappiness;
	// <advc.912c> Replacing the above
	int r = m_iBonusGoodHappiness;
	if (!bIgnoreModifier)
		r = (r * (100 + GET_PLAYER(getOwner()).getLuxuryModifier())) / 100;
	return r; // </advc.912c>
}


void CvCity::changeBonusGoodHappiness(int iChange)
{
	if (iChange != 0)
	{
		m_iBonusGoodHappiness += iChange;
		FAssert(getBonusGoodHappiness() >= 0);
		AI_setAssignWorkDirty(true);

		if (getBonusGoodHappiness() >= 0)
		{
			// doc: Pyramids effect
			if (isHasBuildingEffect(PYRAMIDS))
			{
				changeBuildingGreatPeopleRateChange(PYRAMIDS, iChange);
			}

			// doc: Prambanan effect
			if (isHasBuildingEffect(PRAMBANAN))
			{
				changeBuildingYieldChange(PRAMBANAN, YIELD_PRODUCTION, iChange);
			}
		}
	}
}


void CvCity::changeBonusBadHappiness(int iChange)
{
	if (iChange != 0)
	{
		m_iBonusBadHappiness += iChange;
		FAssert(getBonusBadHappiness() <= 0);
		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getReligionHappiness(ReligionTypes eReligion) const
{
	int iHappiness = 0;
    ReligionTypes eStateReligion = GET_PLAYER(getOwner()).getStateReligion();
	if (isHasReligion(eReligion))
	{
		if (eReligion == eStateReligion)
			iHappiness += GET_PLAYER(getOwner()).getStateReligionHappiness();
		else
        {
            // doc: no religion unhappiness from Hinduism/Buddhism or Confucianism/Taoism
            // TODO: remove because of Syncretism civic?
            bool bSyncretism = (eStateReligion == HINDUISM && eReligion == BUDDHISM) ||
                (eStateReligion == BUDDHISM && eReligion == HINDUISM) ||
                (eStateReligion == CONFUCIANISM && eReligion == TAOISM) ||
                (eStateReligion == TAOISM && eReligion == CONFUCIANISM);
            if (!bSyncretism)
    			iHappiness += GET_PLAYER(getOwner()).getNonStateReligionHappiness();
        }
	}
	return iHappiness;
}


void CvCity::updateReligionHappiness()
{
	int iNewReligionGoodHappiness = 0;
	int iNewReligionBadHappiness = 0;
	FOR_EACH_ENUM(Religion)
	{
		int iChange = getReligionHappiness(eLoopReligion);
		if (iChange > 0)
			iNewReligionGoodHappiness += iChange;
		else iNewReligionBadHappiness += iChange;
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


void CvCity::changeExtraHappiness(int iChange)
{
	if (iChange != 0)
	{
		m_iExtraHappiness += iChange;
		AI_setAssignWorkDirty(true);
	}
}


void CvCity::changeExtraHealth(int iChange)
{
	if (iChange != 0)
	{
		m_iExtraHealth += iChange;
		AI_setAssignWorkDirty(true);
	}
}


void CvCity::changeHurryAngerTimer(int iChange)
{
	if (iChange != 0)
	{
		m_iHurryAngerTimer += iChange;
		FAssert(getHurryAngerTimer() >= 0);
		AI_setAssignWorkDirty(true);
	}
}


void CvCity::changeConscriptAngerTimer(int iChange)
{
	if (iChange != 0)
	{
		m_iConscriptAngerTimer += iChange;
		FAssert(getConscriptAngerTimer() >= 0);
		AI_setAssignWorkDirty(true);
	}
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
	static int const iDEFY_RESOLUTION_ANGER_DIVISOR = GC.getDefineINT("DEFY_RESOLUTION_ANGER_DIVISOR"); // advc.opt
	int iAnger = iDEFY_RESOLUTION_ANGER_DIVISOR;

	iAnger *= GC.getInfo(GC.getGame().getGameSpeedType()).getHurryConscriptAngerPercent();
	iAnger /= 100;

	return std::max(1, iAnger);
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


void CvCity::changeNoUnhappinessCount(int iChange)
{
	if (iChange != 0)
	{
		m_iNoUnhappinessCount += iChange;
		FAssert(getNoUnhappinessCount() >= 0);
		AI_setAssignWorkDirty(true);
	}
}

/*int CvCity::getNoUnhealthyPopulationCount()	const {
	return m_iNoUnhealthyPopulationCount;
}
bool CvCity::isNoUnhealthyPopulation() const {
	if (GET_PLAYER(getOwner()).isNoUnhealthyPopulation())
		return true;
	return (getNoUnhealthyPopulationCount() > 0);
}
void CvCity::changeNoUnhealthyPopulationCount(int iChange) {
	if (iChange != 0) {
		m_iNoUnhealthyPopulationCount += iChange;
		FAssert(getNoUnhealthyPopulationCount() >= 0);
		AI_setAssignWorkDirty(true);
	}
}*/ // BtS
/*  K-Mod, 27/dec/10, karadoc
	replace NoUnhealthyPopulation with UnhealthyPopulationModifier */
int CvCity::getUnhealthyPopulationModifier() const
{
	return m_iUnhealthyPopulationModifier + GET_PLAYER(getOwner()).getUnhealthyPopulationModifier();
}


void CvCity::changeUnhealthyPopulationModifier(int iChange)
{
	m_iUnhealthyPopulationModifier += iChange;
}// K-Mod end


bool CvCity::isBuildingOnlyHealthy() const
 {
	if (GET_PLAYER(getOwner()).isBuildingOnlyHealthy())
		return true;
	return (getBuildingOnlyHealthyCount() > 0);
}


void CvCity::changeBuildingOnlyHealthyCount(int iChange)
{
	if (iChange != 0)
	{
		m_iBuildingOnlyHealthyCount += iChange;
		FAssert(getBuildingOnlyHealthyCount() >= 0);
		AI_setAssignWorkDirty(true);
	}
}


void CvCity::setFood(int iNewValue)
{
	if (getFood() != iNewValue)
	{
		m_iFood = iNewValue;
		if (isActiveTeam())
			setInfoDirty(true);
	}
}


void CvCity::changeFood(int iChange)
{
	setFood(getFood() + iChange);
}


void CvCity::setFoodKept(int iNewValue)
{
	m_iFoodKept = iNewValue;
}


void CvCity::changeFoodKept(int iChange)
{
	setFoodKept(getFoodKept() + iChange);
}


// TODO: implemented in header but has max value
int CvCity::getMaxFoodKeptPercent() const
{
	return std::min(m_iMaxFoodKeptPercent, 75);
}


void CvCity::changeMaxFoodKeptPercent(int iChange)
{
	m_iMaxFoodKeptPercent += iChange;
	FAssert(getMaxFoodKeptPercent() >= 0);
}


void CvCity::setOverflowProduction(int iNewValue)
{
	m_iOverflowProduction = iNewValue;
	FAssert(getOverflowProduction() >= 0);
}


void CvCity::changeOverflowProduction(int iChange, int iProductionModifier)
{
	setOverflowProduction(getOverflowProduction() +
			// advc.064b: Moved into new function
			unmodifyOverflow(iChange, iProductionModifier));
}

// <advc.064b> Cut from changeOverflowProduction
int CvCity::unmodifyOverflow(int iRawOverflow, int iProductionModifier) const
{
	return (100 * iRawOverflow) / std::max(1,
			//getBaseYieldRateModifier(YIELD_PRODUCTION, iProductionModifier)
			/*  Keep the BaseYieldRateModifier; same treatment as Processes, and
				that's what we want for production gold too. However, I'm also
				changing the code that uses up overflow production (see getProductionDifference)
				so that the BaseYieldRateModifier isn't applied for a second time.
				On the bottom line, it's almost the same as what the Unofficial Patch,
				does, but results in more intuitive help text. */
			iProductionModifier + 100);
} // </advc.064b>


void CvCity::setFeatureProduction(int iNewValue)
{
	m_iFeatureProduction = iNewValue;
	FAssert(getFeatureProduction() >= 0);
}


void CvCity::changeFeatureProduction(int iChange)
{
	setFeatureProduction(getFeatureProduction() + iChange);
}


void CvCity::changeMilitaryProductionModifier(int iChange)
{
	m_iMilitaryProductionModifier += iChange;
}


void CvCity::changeSpaceProductionModifier(int iChange)
{
	m_iSpaceProductionModifier += iChange;

    // doc: Golden Record project
    if (iChange != 0 && GET_TEAM(getTeam()).getProjectCount(PROJECT_GOLDEN_RECORD) > 0)
    {
        updateCommerce(COMMERCE_CULTURE);
    }
}


void CvCity::changeExtraTradeRoutes(int iChange)
{
	if (iChange != 0)
	{
		m_iExtraTradeRoutes += iChange;
		FAssert(getExtraTradeRoutes() >= 0);
		updateTradeRoutes();
	}
}


void CvCity::changeTradeRouteModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iTradeRouteModifier += iChange;
		updateTradeRoutes();
	}
}


void CvCity::changeForeignTradeRouteModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iForeignTradeRouteModifier += iChange;
		updateTradeRoutes();
	}
}

// K-Mod, 26/sep/10: Trade culture calculation
int CvCity::getTradeCultureRateTimes100() const // advc: unused param iLevel removed
{
	// <k146>
	//int iPercent = getCultureLevel();
	// Note: GC.getNumCultureLevelInfos() is 7 with the standard xml, which means legendary culture is level 6.
	// So we have 3, 4, 4, 5, 5, 6, 6
	int iPercent = (GC.getNumCultureLevelInfos() + getCultureLevel()) / 2;
	if (iPercent > 0)
	{
		// (originally this was 1% of culture rate for each culture level.) // </k146>
		return (m_aiCommerceRate.get(COMMERCE_CULTURE) * iPercent) / 100;
	}
	return 0;
} // K-Mod end


void CvCity::changeBuildingDefense(int iChange)
{
	if (iChange != 0)
	{
		m_iBuildingDefense += iChange;
		FAssert(getBuildingDefense() >= 0);
		setInfoDirty(true);
		getPlot().plotAction(PUF_makeInfoBarDirty);
	}
}

// BUG - Building Additional Defense - start
int CvCity::getAdditionalDefenseByBuilding(BuildingTypes eBuilding) const
{
	CvBuildingInfo& kBuilding = GC.getInfo(eBuilding);
	int iDefense = std::max(
			std::max(kBuilding.get(CvBuildingInfo::RaiseDefense), // advc.004c
			getBuildingDefense() + kBuilding.getDefenseModifier()),
			getNaturalDefense()) +
			GET_PLAYER(getOwner()).getCityDefenseModifier() +
			kBuilding.getAllCityDefenseModifier();

	// doesn't take bombardment into account
	return iDefense - getTotalDefense(false);
} // BUG - Building Additional Defense - end


void CvCity::changeBuildingBombardDefense(int iChange)
{
	if (iChange != 0)
	{
		m_iBuildingBombardDefense += iChange;
		FAssert(getBuildingBombardDefense() >= 0);
	}
}


void CvCity::changeFreeExperience(int iChange)
{
	m_iFreeExperience += iChange;
	FAssert(getFreeExperience() >= 0);
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


void CvCity::changeMaxAirlift(int iChange)
{
	m_iMaxAirlift += iChange;
	FAssert(getMaxAirlift() >= 0);
}


void CvCity::changeAirModifier(int iChange)
{
	m_iAirModifier += iChange;
}


int CvCity::getAirUnitCapacity(TeamTypes eTeam) const
{
	return (getTeam() == eTeam ? m_iAirUnitCapacity :
			GC.getDefineINT(CvGlobals::CITY_AIR_UNIT_CAPACITY));
}


void CvCity::changeAirUnitCapacity(int iChange)
{
	m_iAirUnitCapacity += iChange;
	FAssert(getAirUnitCapacity(getTeam()) >= 0);
}


void CvCity::changeNukeModifier(int iChange)
{
	m_iNukeModifier += iChange;
}


// TODO: implemented in header but contains special effects
int CvCity::getFreeSpecialist() const
{
    int iTotalFreeSpecialists = m_iFreeSpecialist;

    // doc: Italian UP: +1 free specialist until the Industrial era
    if (getCivilizationType() == ITALY && GET_PLAYER(getOwner()).getCurrentEra() <= ERA_RENAISSANCE)
        iTotalFreeSpecialists += 1;

    // doc: most cultured cities free specialists civic effect
    if (isConnectedToCapital() && getCultureRank() < GC.getWorldInfo(GC.getMap().getWorldSize()).getTargetNumCities()-1)
        iTotalFreeSpecialists += GET_PLAYER(getOwner()).getCulturedCityFreeSpecialists();

    return iTotalFreeSpecialists;
}

void CvCity::changeFreeSpecialist(int iChange)
{
	if (iChange != 0)
	{
		m_iFreeSpecialist += iChange;
		FAssert(getFreeSpecialist() >= 0);
		AI_setAssignWorkDirty(true);
	}
}


bool CvCity::isAreaCleanPower() const
{
    // doc: area effects apply to nearby landmasses
	return getContinentArea().isCleanPower(getTeam());
}


bool CvCity::isDirtyPower() const
{
	return (isPower() && getDirtyPowerCount() == getPowerCount() && !isAreaCleanPower());
}


void CvCity::changePowerCount(int iChange, bool bDirty)
{
	if(iChange == 0)
		return;

	bool bOldPower = isPower();
	bool bOldDirtyPower = isDirtyPower();

	m_iPowerCount += iChange;
	FAssert(getPowerCount() >= 0);
	if (bDirty)
	{
		m_iDirtyPowerCount += iChange;
		FAssert(getDirtyPowerCount() >= 0);
	}

	if (bOldPower != isPower())
	{
		GET_PLAYER(getOwner()).invalidateYieldRankCache();
		updateCommerce();
		if (isActiveTeam())
			setInfoDirty(true);
	}

	if (bOldDirtyPower != isDirtyPower() || bOldPower != isPower())
		updatePowerHealth();
}


void CvCity::changeDefenseDamage(int iChange)
{
	if (iChange == 0)
		return;
	m_iDefenseDamage = range(m_iDefenseDamage + iChange, 0, GC.getMAX_CITY_DEFENSE_DAMAGE());
	if (iChange > 0)
		setBombarded(true);
	setInfoDirty(true);
	getPlot().plotAction(PUF_makeInfoBarDirty);
}

void CvCity::changeDefenseModifier(int iChange)
{
	if(iChange == 0)
	{
		setBombarded(true); // advc.004c: Set bombarded even if no change
		return;
	}
	int iTotalDefense = getTotalDefense(false);
	if(iTotalDefense <= 0)
		return;
	//changeDefenseDamage(-(GC.getMAX_CITY_DEFENSE_DAMAGE() * iChange) / iTotalDefense);
	// <advc.004c> Replacing the above
	int iDefenseDmg = getDefenseDamage();
	int iDefenseMod = getDefenseModifier(false);
	iChange = -iDefenseDmg + (GC.getMAX_CITY_DEFENSE_DAMAGE() * iTotalDefense -
			(iDefenseMod + iChange) * GC.getMAX_CITY_DEFENSE_DAMAGE()) / iTotalDefense;
	changeDefenseDamage(iChange);
	// </advc.004c>
}

/*  advc.003j (comment): Not currently used (b/c K-Mod has removed AI_finalOddsThreshold).
	Gets set in CvCity::doTurn. */
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
	if (pUnit != NULL && !pUnit->isEnemy(getTeam()))
		return false;

	return (getDefenseModifier(false) > 0 ||
			// advc.004c: Don't give away 0 defense in the fog of war to human attacker
			(pUnit != NULL && pUnit->isHuman() && !isVisible(pUnit->getTeam())) ||
			/*  advc.004c: Allow bombarding defenseless cities (to keep their def at 0),
				except cities that have nothing to recover.
				Don't allow the AI to do this b/c the AI can't tell if it matters.
				Much easier to prevent 0-bombardment by the AI here than in CvUnitAI. */
			(getTotalDefense(false) > 0 && pUnit->isHuman() && !isBombarded()));
}


int CvCity::getNaturalDefense() const
{
	if (getCultureLevel() == NO_CULTURELEVEL)
		return 0;
	return GC.getInfo(getCultureLevel()).getCityDefenseModifier();
}


int CvCity::getTotalDefense(bool bIgnoreBuilding) const
{
	return std::max(bIgnoreBuilding ? 0 : getBuildingDefense(), getNaturalDefense()) +
			GET_PLAYER(getOwner()).getCityDefenseModifier();
}


int CvCity::getDefenseModifier(bool bIgnoreBuilding) const
{
	if (isOccupation())
		return 0;
	return ((getTotalDefense(bIgnoreBuilding) *
			(GC.getMAX_CITY_DEFENSE_DAMAGE() - getDefenseDamage())) /
			GC.getMAX_CITY_DEFENSE_DAMAGE());
}


void CvCity::setOccupationTimer(int iNewValue, bool bEffects)
{
	if(getOccupationTimer() == iNewValue)
		return;

	bool bOldOccupation = isOccupation();
	int iOldValue = m_iOccupationTimer;

	m_iOccupationTimer = iNewValue;
	FAssert(getOccupationTimer() >= 0);

	if (bOldOccupation != isOccupation())
	{
		updateCorporation();
		updateMaintenance();
		updateTradeRoutes();
		updateCommerce(); // K-Mod
		/*	<advc.908b> (Intended for conquered cities; will have no effect
			in other situations.) */
		if (!isOccupation())
			initTraitCulture(); // </advc.908b>
	    updateCultureLevel(true);;
	    updateCoveredPlots(true); // doc: gradual border expansion


		AI_setAssignWorkDirty(true);
	}

    if (bEffects && iNewValue < iOldValue)
    {
        applyBuildingDamage((iOldValue - iNewValue) * getBuildingDamageChange());
        applyPopulationLoss((iOldValue - iNewValue) * getPopulationLoss());

        if (!isDisorder())
        {
            setBuildingDamage(0);
            setBuildingDamageChange(0);
            setTotalPopulationLoss(0);
            setPopulationLoss(0);

            // K-Mod
            if (isHuman() && getPopulation() > 0 && isChooseProductionDirty() &&
                !isProduction() && !isProductionAutomated())
            {
                chooseProduction();
            } // K-Mod end
        }
    }

	setInfoDirty(true);
}


void CvCity::changeOccupationTimer(int iChange, bool bEffects)
{
	setOccupationTimer(getOccupationTimer() + iChange, bEffects);
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

// (advc: unused; the Python function also unused)
bool CvCity::isNeverLost() const
{
	return m_bNeverLost;
}


void CvCity::setNeverLost(bool bNewValue)
{
	m_bNeverLost = bNewValue;
}


void CvCity::setBombarded(bool bNewValue)
{
	m_bBombarded = bNewValue;
}


void CvCity::setDrafted(bool bNewValue)
{
	m_bDrafted = bNewValue;
}


void CvCity::setAirliftTargeted(bool bNewValue)
{
	m_bAirliftTargeted = bNewValue;
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
	if (isWeLoveTheKingDay() == bNewValue)
		return;

	m_bWeLoveTheKingDay = bNewValue;
	updateMaintenance();

    // doc: Swedish UP: +50% great people rate when city is celebrating
    if (getCivilizationType() == SWEDEN)
    {
        changeGreatPeopleRateModifier(50 * (bNewValue ? 1 : -1));
    }

	// <advc.001> Show message only when celebrations begin
	if (!isWeLoveTheKingDay())
		return; // </advc.001>
	CivicTypes eCivic = NO_CIVIC;
	FOR_EACH_ENUM(Civic)
	{
		if (GET_PLAYER(getOwner()).isCivic(eLoopCivic))
		{
			if (!CvWString(GC.getInfo(eLoopCivic).getWeLoveTheKing()).empty())
			{
				eCivic = eLoopCivic;
				break;
			}
		}
	}
	if (eCivic != NO_CIVIC)
	{
		CvWString szBuffer = gDLL->getText("TXT_KEY_CITY_CELEBRATE",
				getNameKey(), GC.getInfo(eCivic).getWeLoveTheKing());
		gDLL->UI().addMessage(getOwner(), false, -1, szBuffer, getPlot(),
				"AS2D_WELOVEKING", MESSAGE_TYPE_MINOR_EVENT,
				ARTFILEMGR.getInterfaceArtPath("INTERFACE_HAPPY_PERSON"));
	}
}


void CvCity::setCitizensAutomated(bool bNewValue)
{
	if (isCitizensAutomated() != bNewValue)
	{
		m_bCitizensAutomated = bNewValue;
		if (isCitizensAutomated())
			AI().AI_assignWorkingPlots();
		else
		{
			FOR_EACH_ENUM(Specialist)
				setForceSpecialistCount(eLoopSpecialist, 0);
		}
		if (isActiveOwned() && isCitySelected())
			gDLL->UI().setDirty(SelectionButtons_DIRTY_BIT, true);
	}
}


void CvCity::setProductionAutomated(bool bNewValue, bool bClear)
{
	if (isProductionAutomated() == bNewValue)
		return;

	m_bProductionAutomated = bNewValue;
	if (isActiveOwned() && isCitySelected())
	{
		gDLL->UI().setDirty(SelectionButtons_DIRTY_BIT, true);

		// if automated and not network game and all 3 modifiers down, clear the queue and choose again
		if (bNewValue && bClear)
			clearOrderQueue();
	}
	if (!isProduction())
		AI().AI_chooseProduction();
}

/*	allows you to programmatically specify a cities walls
	rather than having them be generated automagically */
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


CivilizationTypes CvCity::getPreviousCiv() const
{
	return m_ePreviousCiv;
}


void CvCity::setPreviousCiv(CivilizationTypes eNewValue)
{
	m_ePreviousCiv = eNewValue;
}


bool CvCity::isPreviousOwner(PlayerTypes ePlayer) const
{
	if (ePlayer == NO_PLAYER)
	{
		return false;
	}

	return GET_PLAYER(ePlayer).getCivilizationType() == getPreviousCiv();
}


CivilizationTypes CvCity::getOriginalCiv() const
{
	return m_eOriginalCiv;
}


void CvCity::setOriginalCiv(CivilizationTypes eNewValue)
{
	m_eOriginalCiv = eNewValue;
}


bool CvCity::isOriginalOwner(PlayerTypes ePlayer) const
{
	if (ePlayer == NO_PLAYER)
	{
		return false;
	}

	return GET_PLAYER(ePlayer).getCivilizationType() == getOriginalCiv();
}


TeamTypes CvCity::getTeam() const
{
	/*  advc.inl (comment): Not inlined b/c I don't want to include
		CvPlayer.h and CvTeam.h in CvCity.h. Should perhaps cache
		the owning team instead (as it's already done for CvPlot::getTeam). */
	return TEAMID(getOwner());
}


int CvCity::getCultureThreshold() const
{
	// doc: cap at fledgling for minors
	if (isMinorCiv() && getCultureLevel() >= CULTURELEVEL_FLEDGLING)
		return MAX_INT;

	return getCultureThreshold(getCultureLevel());
}

int CvCity::getCultureThreshold(CultureLevelTypes eLevel)
{
	if (eLevel == NO_CULTURELEVEL)
		return 1;
	return std::max(1,
			GC.getGame().getCultureThreshold((CultureLevelTypes)
			std::min(eLevel + 1, GC.getNumCultureLevelInfos() - 1)));
}


void CvCity::setCultureLevel(CultureLevelTypes eNewValue, bool bUpdatePlotGroups)
{
	CultureLevelTypes const eOldValue = getCultureLevel();
	if (eOldValue == eNewValue)
		return;
	m_eCultureLevel = eNewValue;
	if (eOldValue != NO_CULTURELEVEL)
	{
		/*	advc (note): The order of processing is important here b/c
			plot ownership won't be cleared so long as a tile is surrounded by
			owned tiles (even when a plot is no longer in range of any city);
			see CvPlot::calculateCulturalOwner. */
		for (ScanLinePlotIterator itPlot(getPlot(), eOldValue);
			itPlot.hasNext(); ++itPlot)
		{
			int iCultureRange = cultureDistance(itPlot.currXDist(), itPlot.currYDist());
			if (iCultureRange > getCultureLevel() && iCultureRange <= eOldValue)
			{
				FAssert(iCultureRange <= GC.getNumCultureLevelInfos());
				itPlot->changeCultureRangeCities(getOwner(), (CultureLevelTypes)
						iCultureRange, -1, bUpdatePlotGroups);
			}
		}
	}
	if (getCultureLevel() != NO_CULTURELEVEL)
	{
		for (ScanLinePlotIterator itPlot(getPlot(), getCultureLevel());
			itPlot.hasNext(); ++itPlot)
		{
			int iCultureRange = cultureDistance(itPlot.currXDist(), itPlot.currYDist());
			if (iCultureRange > eOldValue && iCultureRange <= getCultureLevel())
			{
				FAssert(iCultureRange <= GC.getNumCultureLevelInfos());
				itPlot->changeCultureRangeCities(getOwner(), (CultureLevelTypes)
						iCultureRange, 1, bUpdatePlotGroups);
			}
		}
	}
	if (GC.getGame().isFinalInitialized())
    {
	    if (eOldValue != NO_CULTURELEVEL && eNewValue != NO_CULTURELEVEL)
	    {
            // doc: Image of the World Square
	        if (isHasBuildingEffect(IMAGE_OF_THE_WORLD_SQUARE))
	        {
	            changeExtraTradeRoutes(eNewValue - eOldValue);
	        }

            // doc: Aqua Appia
	        if (isHasBuildingEffect(AQUA_APPIA))
	        {
	            changeBuildingYieldChange((BuildingClassTypes)GC.getBuildingInfo(AQUA_APPIA).getBuildingClassType(), YIELD_FOOD, eNewValue - eOldValue);
	        }
	    }

        if (getCultureLevel() > eOldValue && getCultureLevel() > 1)
	    {
		    CvWString szBuffer(gDLL->getText("TXT_KEY_MISC_BORDERS_EXPANDED", getNameKey()));
		    gDLL->UI().addMessage(getOwner(), false, -1, szBuffer, getPlot(),
				    "AS2D_CULTUREEXPANDS", MESSAGE_TYPE_MINOR_EVENT,
				    GC.getInfo(COMMERCE_CULTURE).getButton());
		    // <advc.106>
		    // To replace hardcoded getCultureLevel()==GC.getNumCultureLevelInfos()-1
		    int iVictoryCultureLevel = NO_CULTURELEVEL;
		    FOR_EACH_ENUM(Victory)
		    {
			    if (!GC.getGame().isVictoryValid(eLoopVictory))
				    continue;
			    int iLevel = GC.getInfo(eLoopVictory).getCityCulture();
			    if (iLevel > 0 && (iVictoryCultureLevel <= 0 || iVictoryCultureLevel > iLevel))
				    iVictoryCultureLevel = iLevel;
		    }
		    if (getCultureLevel() == iVictoryCultureLevel && iVictoryCultureLevel > 0)
		    {	// Cut from below. Use this for the replay message as well.
			    CvWString szMsg(gDLL->getText("TXT_KEY_MISC_CULTURE_LEVEL", getNameKey(),
					    GC.getInfo(getCultureLevel()).getTextKeyWide()));
			    // </advc.106>
			    for (PlayerIter<MAJOR_CIV> it; it.hasNext(); ++it)
			    {
				    CvPlayer const& kObs = *it;
				    if (isRevealed(kObs.getTeam()) /* advc.127: */ || kObs.isSpectator())
				    {
					    gDLL->UI().addMessage(kObs.getID(), false, -1, szMsg, getPlot(),
							    "AS2D_CULTURELEVEL", MESSAGE_TYPE_MAJOR_EVENT,
							    GC.getInfo(COMMERCE_CULTURE).getButton(),
							    GC.getColorType("HIGHLIGHT_TEXT"));
				    }
				    else
				    {
					    szBuffer = gDLL->getText("TXT_KEY_MISC_CULTURE_LEVEL_UNKNOWN",
							    GC.getInfo(getCultureLevel()).getTextKeyWide());
					    gDLL->UI().addMessage(kObs.getID(), false, -1, szBuffer,
							    "AS2D_CULTURELEVEL", MESSAGE_TYPE_MAJOR_EVENT,
							    GC.getInfo(COMMERCE_CULTURE).getButton(),
							    GC.getColorType("HIGHLIGHT_TEXT"));
				    }
			    } // <advc.106>
			    GC.getGame().addReplayMessage(getPlot(), REPLAY_MESSAGE_MAJOR_EVENT,
					    getOwner(), szMsg, GC.getColorType("HIGHLIGHT_TEXT"));
			    // </advc.106>
		    }
		    // ONEVENT - Culture growth
		    CvEventReporter::getInstance().cultureExpansion(this, getOwner());
		    //Stop Build Culture
		    /*if (isProductionProcess()) {
			    if (GC.getInfo(getProductionProcess()).getProductionToCommerceModifier(COMMERCE_CULTURE) > 0)
					    popOrder(0, false, true);
		    }*/ // BtS
		    /*	K-Mod does this in a different way, to avoid an overflow bug.
			    (And a different way to the Unofficial Patch, to avoid OOS) */
	    }
    }
}


void CvCity::updateCultureLevel(bool bUpdatePlotGroups)
{
	if (getCultureUpdateTimer() > 0)
		return;

	CultureLevelTypes eCultureLevel = (CultureLevelTypes)0;
	if (!isOccupation())
	{	// advc: Moved into subroutine
		eCultureLevel = calculateCultureLevel(getOwner());
	}
	setCultureLevel(eCultureLevel, bUpdatePlotGroups);
}

/*	advc: Cut from updateCultureLevel. Unlike getCulture(PlayerTypes), this function
	will always recalculate the culture level. */
CultureLevelTypes CvCity::calculateCultureLevel(PlayerTypes ePlayer) const
{
	int const iCultureTimes100 = getCultureTimes100(ePlayer);
	FOR_EACH_ENUM_REV(CultureLevel)
	{
		if(iCultureTimes100 >= 100 * GC.getGame().getCultureThreshold(eLoopCultureLevel))
			return eLoopCultureLevel;
	}
	FErrorMsg("No culture level threshold met");
	return (CultureLevelTypes)0;
}

// advc:
CultureLevelTypes CvCity::getCultureLevel(PlayerTypes ePlayer) const
{
	if (ePlayer == getOwner())
		return getCultureLevel();
	return calculateCultureLevel(ePlayer);
}

// advc.042: Mostly cut and pasted from CvDLLWidgetData::parseCultureHelp
int CvCity::getCultureTurnsLeft() const
{
	int iCultureRateTimes100 = getCommerceRateTimes100(COMMERCE_CULTURE);
	if(iCultureRateTimes100 <= 0)
		return -1;
	int iCultureLeftTimes100 = 100 * getCultureThreshold()
			- getCultureTimes100(getOwner());
	if(iCultureLeftTimes100 <= 0)
		return -1;
	int iR = (iCultureLeftTimes100 + iCultureRateTimes100 - 1) / iCultureRateTimes100;
	FAssert(iR != 0);
	return iR;
}

// advc.908b:
void CvCity::initTraitCulture()
{
	FOR_EACH_ENUM(Trait)
	{
		if (!GET_PLAYER(getOwner()).hasTrait(eLoopTrait))
			continue;
		int iFreeCityCulture = GC.getGame().freeCityCultureFromTrait(eLoopTrait)
				- getCulture(getOwner());
		if (iFreeCityCulture > 0)
			setCulture(getOwner(), iFreeCityCulture, true, false);
	}
}


void CvCity::changeSeaPlotYield(YieldTypes eYield, int iChange)
{
	if (iChange != 0)
	{
		m_aiSeaPlotYield.add(eYield, iChange);
		FAssert(getSeaPlotYield(eYield) >= 0);
		updateYield();
	}
}


void CvCity::changeRiverPlotYield(YieldTypes eYield, int iChange)
{
	if (iChange != 0)
	{
		m_aiRiverPlotYield.add(eYield, iChange);
		FAssert(getRiverPlotYield(eYield) >= 0);
		updateYield();
	}
}


// doc
// TODO: move to header
int CvCity::getFlatRiverPlotYield(YieldTypes eYield) const
{
    return m_aiFlatRiverPlotYield[eYield];
}


// doc
void CvCity::changeFlatRiverPlotYield(YieldTypes eYield, int iChange)
{
    if (iChange != 0)
    {
        m_aiFlatRiverPlotYield.add(eYield, iChange);
        FAssert(getRiverPlotYield(eYield) >= 0);
        updateYield();
    }
}


// doc
void CvCity::changeBonusYield(BonusTypes eBonus, YieldTypes eYield, int iChange)
{
    if (iChange != 0)
    {
		m_aeiiBonusYieldChange.add(eBonus, eYield, iChange);

        updateYield();
    }
}

// BUG - Building Additional Yield - start
/*	Returns the total additional yield that adding one of the given buildings will provide.
	Doesn't check if the building can be constructed in this city. */
int CvCity::getAdditionalYieldByBuilding(YieldTypes eYield, BuildingTypes eBuilding) const
{
	int iRate = getBaseYieldRate(eYield);
	int iModifier = getBaseYieldRateModifier(eYield);
	int iExtra = ((iRate + getAdditionalBaseYieldRateByBuilding(eYield, eBuilding)) *
		(iModifier + getAdditionalYieldRateModifierByBuilding(eYield, eBuilding)) / 100) -
		(iRate * iModifier / 100);
	return iExtra;
}

/*	Returns the additional yield rate that adding one of the given buildings will provide.
	Doesn't check if the building can be constructed in this city.
	advc: _MOD_FRACTRADE removed */
int CvCity::getAdditionalBaseYieldRateByBuilding(YieldTypes eYield,
	BuildingTypes eBuilding) const
{
	if (GET_TEAM(getTeam()).isObsoleteBuilding(eBuilding))
		return 0;

	int iExtraRate = 0;
	CvBuildingInfo const& kBuilding = GC.getInfo(eBuilding);
	// <advc.179> Some overlap with code in CvGameTextMgr::buildBuildingReligionYieldString
	CvCivilization const& kCiv = getCivilization();
	FOR_EACH_ENUM2(VoteSource, eVS)
	{
		if (eVS != kBuilding.getVoteSourceType())
			continue;
		CvVoteSourceInfo& kVS = GC.getInfo(eVS);
		if (kVS.getReligionYield(eYield) != 0)
		{
			ReligionTypes eVSReligion =
					// This would be NO_RELIGION b/c the vote source doesn't exist yet:
					//GC.getGame().getVoteSourceReligion(eVS);
					GET_PLAYER(getOwner()).getStateReligion();
			if (eVSReligion != NO_RELIGION)
			{
				// Akin to processVoteSource
				for(int i = 0; i < kCiv.getNumBuildings(); i++)
				{
					BuildingTypes eBuilding = kCiv.buildingAt(i);
					if(getNumBuilding(eBuilding) > 0 &&
						!GET_TEAM(getTeam()).isObsoleteBuilding(eBuilding))
					{
						if(GC.getInfo(eBuilding).getReligionType() == eVSReligion)
							iExtraRate += kVS.getReligionYield(eYield);
					}
				}
			}
		}
	} // </advc.179>
	if (kBuilding.getSeaPlotYieldChange(eYield) != 0)
	{
		int iChange = kBuilding.getSeaPlotYieldChange(eYield);
		for (WorkingPlotIter it(*this); it.hasNext(); ++it)
		{
			if (it->isWater())
				iExtraRate += iChange;
		}
	}
	if (kBuilding.getRiverPlotYieldChange(eYield) != 0)
	{
		int iChange = kBuilding.getRiverPlotYieldChange(eYield);
		for (WorkingPlotIter it(*this); it.hasNext(); ++it)
		{
			if (it->isRiver())
				iExtraRate += iChange;
		}
	}
	iExtraRate += kBuilding.getYieldChange(eYield);
	iExtraRate += getBuildingYieldChange(kBuilding.getBuildingClassType(), eYield);

	// Trade
	int iPlayerTradeYieldModifier = GET_PLAYER(getOwner()).getTradeYieldModifier(eYield);
	if (iPlayerTradeYieldModifier > 0 && (kBuilding.getTradeRouteModifier() != 0 ||
		kBuilding.getForeignTradeRouteModifier() != 0))
	{
		int iTotalTradeYield = 0;
		int iNewTotalTradeYield = 0;
		int iTradeProfitDivisor = 10000;
		for (int iI = 0; iI < getTradeRoutes(); ++iI)
		{
			CvCity* pCity = getTradeCity(iI);
			if (pCity == NULL)
				continue;
			int iTradeProfit = getBaseTradeProfit(pCity);
			int iTradeModifier = totalTradeModifier(pCity);
			int iTradeYield = ((iTradeProfit * iTradeModifier) / iTradeProfitDivisor) *
					(iPlayerTradeYieldModifier / 100);
			iTotalTradeYield += iTradeYield;
			iTradeModifier += kBuilding.getTradeRouteModifier();
			if (pCity->getOwner() != getOwner())
				iTradeModifier += kBuilding.getForeignTradeRouteModifier();
			int iNewTradeYield = ((iTradeProfit * iTradeModifier) / iTradeProfitDivisor) *
					(iPlayerTradeYieldModifier / 100);
			iNewTotalTradeYield += iNewTradeYield;
		}
		iExtraRate += iNewTotalTradeYield - iTotalTradeYield;
	}

	FOR_EACH_NON_DEFAULT_PAIR(kBuilding.
		getFreeSpecialistCount(), Specialist, int)
	{
		iExtraRate += getAdditionalBaseYieldRateBySpecialist(eYield,
				perSpecialistVal.first, perSpecialistVal.second);
	}

	return iExtraRate;
}

/*	Returns the additional yield rate modifier that adding one of
	the given buildings will provide. Doesn't check if the building can be
	constructed in this city. */
int CvCity::getAdditionalYieldRateModifierByBuilding(YieldTypes eYield,
	BuildingTypes eBuilding) const
{
	if (GET_TEAM(getTeam()).isObsoleteBuilding(eBuilding))
		return 0; // advc

	CvBuildingInfo const& kBuilding = GC.getInfo(eBuilding);
	int iExtraModifier = kBuilding.getYieldModifier(eYield);
	if (isPower())
		iExtraModifier += kBuilding.getPowerYieldModifier(eYield);
	else
	{
		if (kBuilding.isPower() || kBuilding.isAreaCleanPower() ||
			(kBuilding.getPowerBonus() != NO_BONUS &&
			hasBonus(kBuilding.getPowerBonus())))
		{
			CvCivilization const& kCiv = getCivilization();
			for (int i = 0; i < kCiv.getNumBuildings(); i++)
			{
				BuildingTypes eBuilding = kCiv.buildingAt(i);
				iExtraModifier += getNumActiveBuilding(eBuilding) *
						GC.getInfo(eBuilding).getPowerYieldModifier(eYield);
			}
		}
	}
	if (eYield == YIELD_PRODUCTION)
	{
		iExtraModifier += kBuilding.getMilitaryProductionModifier();
		iExtraModifier += kBuilding.getSpaceProductionModifier();
		iExtraModifier += kBuilding.getGlobalSpaceProductionModifier();

		int iMaxModifier = 0;
		FOR_EACH_ENUM(Domain)
		{
			iMaxModifier = std::max<int>(iMaxModifier,
					kBuilding.getDomainProductionModifier(eLoopDomain));
		}
		iExtraModifier += iMaxModifier;
	}
	FOR_EACH_NON_DEFAULT_PAIR(kBuilding.
		getBonusYieldModifier(), Bonus, YieldPercentMap)
	{
		if (hasBonus(perBonusVal.first))
			iExtraModifier += perBonusVal.second[eYield];
	}
	return iExtraModifier;
}
// BUG - Building Additional Yield - end

// BUG - Specialist Additional Yield - start
/*	Returns the total additional yield that changing the number
	of given specialists will provide/remove. */
int CvCity::getAdditionalYieldBySpecialist(YieldTypes eYield, SpecialistTypes eSpecialist, int iChange) const
{
	int iRate = getBaseYieldRate(eYield);
	int iModifier = getBaseYieldRateModifier(eYield);
	int iExtra = ((iRate + getAdditionalBaseYieldRateBySpecialist(eYield, eSpecialist, iChange)) *
			iModifier / 100) - (iRate * iModifier / 100);
	return iExtra;
}

/*	Returns the additional yield rate that changing the number
	of given specialists will provide/remove. */
int CvCity::getAdditionalBaseYieldRateBySpecialist(YieldTypes eYield, SpecialistTypes eSpecialist, int iChange) const
{
	CvSpecialistInfo& kSpecialist = GC.getInfo(eSpecialist);
	return iChange * (kSpecialist.getYieldChange(eYield) +
			GET_PLAYER(getOwner()).getSpecialistExtraYield(eSpecialist, eYield));
}
// BUG - Specialist Additional Yield - end

int CvCity::getBaseYieldRateModifier(YieldTypes eYield, int iExtra) const
{
	int iModifier = getYieldRateModifier(eYield);
	iModifier += getBonusYieldRateModifier(eYield);

	if (isPower())
		iModifier += getPowerYieldRateModifier(eYield);

    // doc: area effects apply to nerby landmasses
	iModifier += getContinentArea().getYieldRateModifier(getOwner(), eYield);
	iModifier += GET_PLAYER(getOwner()).getYieldRateModifier(eYield);

	if (isCapital())
		iModifier += GET_PLAYER(getOwner()).getCapitalYieldRateModifier(eYield);

	iModifier += iExtra;

	// note: player->invalidateYieldRankCache() must be called for anything that is checked here
	// so if any extra checked things are added here, the cache needs to be invalidated

	return std::max(0, iModifier + 100);
}


int CvCity::getYieldRate(YieldTypes eYield) const
{
    int iBaseYieldRate = getBaseYieldRate(eYield);

    // Harappan UP: Sanitation: positive health contributes to city growth
    if (eYield == YIELD_FOOD && getCivilizationType() == HARAPPA && GET_PLAYER(getOwner()).getCurrentEra() == ERA_ANCIENT && !isFoodProduction())
    {
        if (iBaseYieldRate * getBaseYieldRateModifier(eYield) - foodConsumption() * 100 > 1 && goodHealth() - badHealth() > 0)
        {
            iBaseYieldRate += goodHealth() - badHealth();
        }
    }

    // Khmer UP: Hydraulic Engineering: +1 food per 5 building production in capital
    if (eYield == YIELD_FOOD && getCivilizationType() == KHMER && isCapital() && isProductionBuilding() && !isFoodProduction())
    {
        iBaseYieldRate += getYieldRate(YIELD_PRODUCTION) * (100 + getProductionModifier(getProductionBuilding())) / 100 / 5;
    }

    // Lotus Temple effect
    if (eYield == YIELD_FOOD && GET_PLAYER(getOwner()).isHasBuildingEffect(LOTUS_TEMPLE))
    {
        iBaseYieldRate += (getReligionCount() - (GET_PLAYER(getOwner()).getStateReligion() != NO_RELIGION && isHasReligion(GET_PLAYER(getOwner()).getStateReligion()) ? 1 : 0));
    }

    return iBaseYieldRate * getBaseYieldRateModifier(eYield) / 100;
}


void CvCity::setBaseYieldRate(YieldTypes eYield, int iNewValue)
{
	if (getBaseYieldRate(eYield) == iNewValue)
		return;

	FAssert(iNewValue >= 0);
	//FAssert((iNewValue * 100) / 100 >= 0); // advc: ??

	m_aiBaseYieldRate.set(eYield, iNewValue);
	FAssert(getYieldRate(eYield) >= 0);

	updateCommerce();

	if (isActiveTeam())
	{
		setInfoDirty(true);
		if (isCitySelected())
		{
			gDLL->UI().setDirty(CityScreen_DIRTY_BIT, true);
			gDLL->UI().setDirty(InfoPane_DIRTY_BIT, true);
		}
	}
}


void CvCity::changeBaseYieldRate(YieldTypes eYield, int iChange)
{
	setBaseYieldRate(eYield, getBaseYieldRate(eYield) + iChange);
}


void CvCity::changeYieldRateModifier(YieldTypes eYield, int iChange)
{
	if (iChange == 0)
		return;

	m_aiYieldRateModifier.add(eYield, iChange);
	FAssert(getYieldRate(eYield) >= 0);
	GET_PLAYER(getOwner()).invalidateYieldRankCache(eYield);

	if (eYield == YIELD_COMMERCE)
		updateCommerce();
	AI_setAssignWorkDirty(true);

	if (isActiveTeam())
		setInfoDirty(true);
}


void CvCity::changePowerYieldRateModifier(YieldTypes eYield, int iChange)
{
	if (iChange == 0)
		return;

	m_aiPowerYieldRateModifier.add(eYield, iChange);
	FAssert(getYieldRate(eYield) >= 0);
	GET_PLAYER(getOwner()).invalidateYieldRankCache(eYield);

    // doc: power health scales with power consumed
    if (iChange > 0) changePowerConsumedCount(1);
    else if (iChange < 0) changePowerConsumedCount(-1);

	if (eYield == YIELD_COMMERCE)
		updateCommerce();
	AI_setAssignWorkDirty(true);

	if (isActiveTeam())
		setInfoDirty(true);
}


void CvCity::changeBonusYieldRateModifier(YieldTypes eYield, int iChange)
{
	if (iChange == 0)
		return;

	m_aiBonusYieldRateModifier.add(eYield, iChange);
	FAssert(getYieldRate(eYield) >= 0);
	GET_PLAYER(getOwner()).invalidateYieldRankCache(eYield);

	if (eYield == YIELD_COMMERCE)
		updateCommerce();
	AI_setAssignWorkDirty(true);

	if (isActiveTeam())
		setInfoDirty(true);
}


int CvCity::totalTradeModifier(CvCity const* pOtherCity) const
{
	static int const iCAPITAL_TRADE_MODIFIER = GC.getDefineINT("CAPITAL_TRADE_MODIFIER"); // advc.opt
	int iModifier = 100;

	iModifier += getTradeRouteModifier();
	iModifier += getPopulationTradeModifier();

	if (isConnectedToCapital())
		iModifier += iCAPITAL_TRADE_MODIFIER;

	if (pOtherCity != NULL)
	{
        // TODO: doc code uses continentArea so sameArea should be adapted
		if (!sameArea(*pOtherCity))
			iModifier += GC.getDefineINT(CvGlobals::OVERSEAS_TRADE_MODIFIER);

        // doc: no foreign trade route modifier civic effect
        if ((getTeam() != pOtherCity->getTeam() && !GET_PLAYER(getOwner()).isNoForeignTradeModifier()))
		{
			iModifier += getForeignTradeRouteModifier();
			iModifier += getPeaceTradeModifier(pOtherCity->getTeam());

			// doc: civic modifier for defensive pact partners
			iModifier += getDefensivePactTradeModifier(*pOtherCity);

			// doc: civic modfier for vassals
			iModifier += getVassalTradeModifier(*pOtherCity);

			// doc: Dravidian UP: +10% foreign trade yield per traded resource
			if (getCivilizationType() == DRAVIDIA)
			{
				iModifier += 10 * (GET_PLAYER(getOwner()).getNumTradeBonusImports(pOtherCity->getOwner()) + GET_PLAYER(getOwner()).getNumTradeBonusExports(pOtherCity->getOwner()));
			}

			// doc: Channel Tunnel effect
			if (GET_PLAYER(getOwner()).isHasBuildingEffect(CHANNEL_TUNNEL))
			{
				if (GET_PLAYER(pOtherCity->getOwner()).AI_getAttitude(getOwner()) >= ATTITUDE_FRIENDLY)
				{
					iModifier += 100;
				}
			}
		}

		// doc: modifier from city distance
		iModifier += getDistanceTradeModifier(*pOtherCity);

		// doc: modifier from culture level
		iModifier += getCultureTradeRouteModifier() * getCultureLevel();
	}

	return iModifier;
}

int CvCity::getDefensivePactTradeModifier(CvCity const& kOtherCity) const
{
	if (GET_TEAM(getTeam()).isDefensivePact(kOtherCity.getTeam()))
	{
		return GET_PLAYER(getOwner()).getDefensivePactTradeModifier();
	}

	return 0;
}

int CvCity::getVassalTradeModifier(CvCity const& kOtherCity) const
{
	if (GET_TEAM(kOtherCity.getTeam()).isVassal(getTeam()))
	{
		return GET_PLAYER(getOwner()).getVassalTradeModifier();
	}

	return 0;
}

int CvCity::getDistanceTradeModifier(CvCity const& kOtherCity) const
{
	int iDistance = stepDistance(getX(), getY(), kOtherCity.getX(), kOtherCity.getY());

	// doc: Mande UP: double trade yield from distance for inland cities
	if (getCivilizationType() == MALI && !isCoastal(GC.getDefineINT(CvGlobals::MIN_WATER_SIZE_FOR_OCEAN)))
		iDistance *= 2;

	return iDistance * GC.getDefineINT("DISTANCE_TRADE_MODIFIER");
}

int CvCity::getPopulationTradeModifier() const
{
	static int const iOUR_POPULATION_TRADE_MODIFIER = GC.getDefineINT("OUR_POPULATION_TRADE_MODIFIER"); // advc.opt
	static int const iOUR_POPULATION_TRADE_MODIFIER_OFFSET = GC.getDefineINT("OUR_POPULATION_TRADE_MODIFIER_OFFSET"); // advc.opt
	return std::max(0, (getPopulation() + iOUR_POPULATION_TRADE_MODIFIER_OFFSET) * iOUR_POPULATION_TRADE_MODIFIER);
}


int CvCity::getPeaceTradeModifier(TeamTypes eTeam) const
{
	FAssert(NO_TEAM != eTeam);
	FAssert(eTeam != getTeam());

	if (atWar(eTeam, getTeam()))
		return 0;

	static int const iFOREIGN_TRADE_FULL_CREDIT_PEACE_TURNS = GC.getDefineINT("FOREIGN_TRADE_FULL_CREDIT_PEACE_TURNS"); // advc.opt
	static int const iFOREIGN_TRADE_MODIFIER = GC.getDefineINT("FOREIGN_TRADE_MODIFIER"); // advc.opt
	int const iFullTurns = std::max(1, (iFOREIGN_TRADE_FULL_CREDIT_PEACE_TURNS *
			// <advc.130k>
			GC.getInfo(GC.getGame().getGameSpeedType()).get(
			CvGameSpeedInfo::FullTradeCreditPercent)) / 100);
	int iPeaceTurns = std::min(iFullTurns,
			GET_TEAM(getTeam()).getTurnsAtPeace(eTeam)); // was AI_getAtPeaceCounter
			// </advc.130k>

    // doc: Canadian UP: double trade route yield from years of peace
    if (getCivilizationType() == CANADA)
    {
        iPeaceTurns *= 2;
    }

    // doc: disable turn limit
	//if (GC.getGame().getElapsedGameTurns() <= iPeaceTurns)
	//	return iFOREIGN_TRADE_MODIFIER;
	return (iFOREIGN_TRADE_MODIFIER * iPeaceTurns) / iFullTurns;
}


int CvCity::getBaseTradeProfit(CvCity const* pCity) const // advc: const CvCity*
{
	static int const iTHEIR_POPULATION_TRADE_PERCENT = GC.getDefineINT("THEIR_POPULATION_TRADE_PERCENT"); // advc.opt
	static int const iTRADE_PROFIT_PERCENT = GC.getDefineINT("TRADE_PROFIT_PERCENT"); // advc.opt
	int iProfit = std::min(pCity->getPopulation() * iTHEIR_POPULATION_TRADE_PERCENT,
			plotDistance(getX(), getY(), pCity->getX(), pCity->getY()) *
			GC.getInfo(GC.getMap().getWorldSize()).getTradeProfitPercent());

	iProfit *= iTRADE_PROFIT_PERCENT;
	iProfit /= 100;

	iProfit = std::max(100, iProfit);
	return iProfit;
}


int CvCity::calculateTradeProfitTimes100(CvCity const* pCity) const // advc: const CvCity*
{
	int iProfit = getBaseTradeProfit(pCity);
	iProfit *= totalTradeModifier(pCity);
	iProfit /= /*10000*/100; // advc.004: Increase precision; function renamed accordingly.
	return iProfit;
}


int CvCity::calculateTradeYield(YieldTypes eYield, int iTradeProfit) const
{
	if (iTradeProfit > 0 && GET_PLAYER(getOwner()).getTradeYieldModifier(eYield) > 0)
		return (iTradeProfit * GET_PLAYER(getOwner()).getTradeYieldModifier(eYield)) / 100;
	return 0;
}

// BULL - Trade Hover:  (advc: simplified a bit, _MOD_FRACTRADE removed)
/*  Adds the yield and count for each trade route with eWithPlayer to the
	int references (out parameters). */
void CvCity::calculateTradeTotals(YieldTypes eYield, int& iDomesticYield, int& iDomesticRoutes,
	int& iForeignYield, int& iForeignRoutes, PlayerTypes eWithPlayer) const
{
	if(isDisorder())
		return;

	int iNumTradeRoutes = getTradeRoutes();
	for (int i = 0; i < iNumTradeRoutes; i++)
	{
		CvCity* pTradeCity = getTradeCity(i);
		if (pTradeCity != NULL && (eWithPlayer == NO_PLAYER ||
			pTradeCity->getOwner() == eWithPlayer))
		{
			int iTradeYield = calculateTradeYield(//YIELD_COMMERCE
					eYield, // advc.001
					calculateTradeProfit(pTradeCity));
			if (pTradeCity->getOwner() == getOwner())
			{
				iDomesticYield += iTradeYield;
				iDomesticRoutes++;
			}
			else
			{
				iForeignYield += iTradeYield;
				iForeignRoutes++;
			}
		}
	}
}


void CvCity::setTradeYield(YieldTypes eYield, int iNewValue)
{
	int const iOldValue = getTradeYield(eYield);
	if (iOldValue != iNewValue)
	{
		m_aiTradeYield.set(eYield, iNewValue);
		FAssert(getTradeYield(eYield) >= 0);
		changeBaseYieldRate(eYield, iNewValue - iOldValue);
	}
}


int CvCity::getExtraSpecialistYield(YieldTypes eYield, SpecialistTypes eSpecialist) const
{
	return (getSpecialistCount(eSpecialist) + getFreeSpecialistCount(eSpecialist)) *
			GET_PLAYER(getOwner()).getSpecialistExtraYield(eSpecialist, eYield);
}


void CvCity::updateExtraSpecialistYield(YieldTypes eYield)
{
	int iNewYield = 0;
	FOR_EACH_ENUM(Specialist)
		iNewYield += getExtraSpecialistYield(eYield, eLoopSpecialist);

	int const iChange = iNewYield - getExtraSpecialistYield(eYield); // advc
	if (iChange != 0)
	{
		m_aiExtraSpecialistYield.set(eYield, iNewYield);
		FAssert(getExtraSpecialistYield(eYield) >= 0);
		changeBaseYieldRate(eYield, iChange);
	}
}


void CvCity::updateExtraSpecialistYield()
{
	FOR_EACH_ENUM(Yield)
		updateExtraSpecialistYield(eLoopYield);
}


int CvCity::getCommerceRate(CommerceTypes eCommerce) const
{
	return getCommerceRateTimes100(eCommerce) / 100;
}


int CvCity::getCommerceRateTimes100(CommerceTypes eCommerce) const
{
	int iRate = m_aiCommerceRate.get(eCommerce);
	if (GC.getGame().isOption(GAMEOPTION_NO_ESPIONAGE))
	{
		if (eCommerce == COMMERCE_CULTURE)
			iRate += m_aiCommerceRate.get(COMMERCE_ESPIONAGE);
		else if (eCommerce == COMMERCE_ESPIONAGE)
			iRate = 0;
	}
	return iRate;
}

// doc
int CvCity::getModifiedCultureRateTimes100() const
{
    int iCultureTimes100 = getCommerceRateTimes100(COMMERCE_CULTURE);
    if (iCultureTimes100 <= 400)
        return iCultureTimes100;

    return iCultureTimes100 * GET_PLAYER(getOwner()).getModifier(MODIFIER_CULTURE) / 100;
}


// doc
// TODO: implement in header
int CvCity::getModifiedCultureRate() const
{
    return getModifiedCultureRateTimes100() / 100;
}

// <advc> Now that these are needed in two places
void CvCity::changeCommerceRateTimes100(CommerceTypes eCommerce, int iChange)
{
	setCommerceRateTimes100(eCommerce, m_aiCommerceRate.get(eCommerce) + iChange);
}

// Based on code cut from updateCommerce
void CvCity::setCommerceRateTimes100(CommerceTypes eCommerce, int iRate)
{
	int const iOldRate = m_aiCommerceRate.get(eCommerce);
	if (iOldRate != iRate)
	{
		m_aiCommerceRate.set(eCommerce, iRate);
		FAssert(m_aiCommerceRate.get(eCommerce) >= 0);
		GET_PLAYER(getOwner()).changeCommerceRateTimes100(eCommerce, iRate - iOldRate);
	}
} // </advc>


int CvCity::getCommerceFromPercent(CommerceTypes eCommerce, int iYieldRate) const
{
	int iCommerceRate = (iYieldRate *
			GET_PLAYER(getOwner()).getCommercePercent(eCommerce)) / 100;
	if (eCommerce == COMMERCE_GOLD)
	{
		iCommerceRate += (iYieldRate - iCommerceRate -
				getCommerceFromPercent(COMMERCE_RESEARCH, iYieldRate) -
				getCommerceFromPercent(COMMERCE_CULTURE, iYieldRate) -
				getCommerceFromPercent(COMMERCE_ESPIONAGE, iYieldRate));
	}
	return iCommerceRate;
}


int CvCity::getBaseCommerceRateTimes100(CommerceTypes eCommerce) const
{
	int iBaseCommerceRate = getCommerceFromPercent(eCommerce,
			getYieldRate(YIELD_COMMERCE) * 100);
	iBaseCommerceRate += 100 * ((getSpecialistPopulation() + getNumGreatPeople()) *
			GET_PLAYER(getOwner()).getSpecialistExtraCommerce(eCommerce));
	iBaseCommerceRate += 100 *
			(getBuildingCommerce(eCommerce) +
			getSpecialistCommerce(eCommerce) +
			getReligionCommerce(eCommerce) +
			getCorporationCommerce(eCommerce) +
			GET_PLAYER(getOwner()).getFreeCityCommerce(eCommerce));

    // doc: Himeji Castle effect
    if (eCommerce == COMMERCE_CULTURE && isHasBuildingEffect(HIMEJI_CASTLE))
    {
		FOR_EACH_UNIT_IN(pUnit, getPlot())
		{
			if (pUnit->getOwner() == getOwner() && pUnit->isFortifyable() && pUnit->getFortifyTurns() >= GC.getDefineINT("MAX_FORTIFY_TURNS"))
			{
				iBaseCommerceRate += 100 * pUnit->getLevel();
			}
		}
    }

	return iBaseCommerceRate;
}


int CvCity::getTotalCommerceRateModifier(CommerceTypes eCommerce) const
{
	CvPlayer const& kOwner = GET_PLAYER(getOwner());
	int iTotalModifier = 100;
    iTotalModifier += getCommerceRateModifier(eCommerce);
	iTotalModifier += kOwner.getCommerceRateModifier(eCommerce);
	iTotalModifier += isCapital() ? kOwner.getCapitalCommerceRateModifier(eCommerce) : 0;
    iTotalModifier += getBonusCommerceRateModifier(eCommerce); // doc: modifier from bonus
    iTotalModifier += isPower() ? getPowerCommerceRateModifier(eCommerce) : 0; // doc: modifier from power

    // doc: Golden Record project
    if (eCommerce == COMMERCE_CULTURE && GET_TEAM(getTeam()).getProjectCount(PROJECT_GOLDEN_RECORD) > 0)
    {
        iTotalModifier += getSpaceProductionModifier() / 2;
        iTotalModifier += GET_PLAYER(getOwner()).getSpaceProductionModifier() / 2;
    }

    return std::max(0, iTotalModifier);
}


void CvCity::updateCommerce(CommerceTypes eCommerce)
{
	int iNewRate = 0;
	if (!isDisorder())
	{
		iNewRate += (getBaseCommerceRateTimes100(eCommerce) *
				getTotalCommerceRateModifier(eCommerce)) / 100;
		iNewRate += getYieldRate(YIELD_PRODUCTION) *
				getProductionToCommerceModifier(eCommerce);
	}
	setCommerceRateTimes100(eCommerce, iNewRate); // advc: Moved into aux. function
	GET_PLAYER(getOwner()).invalidateCommerceRankCache(eCommerce);
	if (isCitySelected())
	{
		gDLL->UI().setDirty(InfoPane_DIRTY_BIT, true);
		gDLL->UI().setDirty(CityScreen_DIRTY_BIT, true);
	}
}


void CvCity::updateCommerce()
{
	GET_PLAYER(getOwner()).invalidateYieldRankCache();
	FOR_EACH_ENUM(Commerce)
		updateCommerce(eLoopCommerce);
}


void CvCity::changeProductionToCommerceModifier(CommerceTypes eCommerce, int iChange)
{
	if (iChange != 0)
	{
		m_aiProductionToCommerceModifier.add(eCommerce, iChange);
		updateCommerce(eCommerce);
	}
}


int CvCity::getBuildingCommerceByBuilding(CommerceTypes eCommerce, BuildingTypes eBuilding) const
{
	/*	K-Mod. I've rearranged some stuff so that bonus commerce does
		not get doubled at the end. (eg. the bonus culture that the Sistine Chapel
		gives to religious buildings should not be doubled.) */

	if (getNumBuilding(eBuilding) <= 0)
		return 0;
	CvBuildingInfo const& kBuilding = GC.getInfo(eBuilding);
	if (kBuilding.isCommerceChangeOriginalOwner(eCommerce) &&
		getBuildingOriginalOwner(eBuilding) != getOwner())
	{
		return 0;
	}

	int iTimeFactor = 1;
	// <advc.098>
	bool const bDelayedCommerceIncrease =
			(kBuilding.getCommerceChangeDoubleTime(eCommerce) > 0); // </advc.098>
	if (bDelayedCommerceIncrease &&
		getBuildingOriginalTime(eBuilding) != iBuildingOriginalTimeUnknown &&
		GC.getGame().getGameTurnYear() - getBuildingOriginalTime(eBuilding) >=
		kBuilding.getCommerceChangeDoubleTime(eCommerce))
	{
		iTimeFactor = 2;
	}
	/*	there are just two components which get multiplied by the time factor:
		1) the "safe" commerce and 2) the standard commerce;
		the rest of the components are bonuses which should not be doubled. */

	int iCommerceRate = kBuilding.getObsoleteSafeCommerceChange(eCommerce) *
			getNumBuilding(eBuilding);
	// <advc.098>
	if (bDelayedCommerceIncrease &&
		GC.getDefineBOOL(CvGlobals::DOUBLE_OBSOLETE_BUILDING_COMMERCE))
	{
		if (GET_TEAM(getTeam()).isObsoleteBuilding(eBuilding))
			iCommerceRate *= 2;
	}
	else // </advc.098>
		iCommerceRate *= iTimeFactor; // 1)

	if (getNumActiveBuilding(eBuilding) > 0)
	{
		iCommerceRate += kBuilding.getCommerceChange(eCommerce) *
				getNumActiveBuilding(eBuilding) * iTimeFactor; // 2)
		iCommerceRate += getBuildingCommerceChange(
				kBuilding.getBuildingClassType(), eCommerce) *
				getNumActiveBuilding(eBuilding);

		if (kBuilding.getReligionType() != NO_RELIGION &&
			kBuilding.getReligionType() == GET_PLAYER(getOwner()).getStateReligion())
		{
			iCommerceRate += GET_PLAYER(getOwner()).
					getStateReligionBuildingCommerce(eCommerce) *
					getNumActiveBuilding(eBuilding);
		}
		{
            // doc: global limit for shrine income
			ReligionTypes const eGlobalCommerceReligion = kBuilding.getGlobalReligionCommerce();
			int const iShrineLimit = GET_PLAYER(getOwner()).getShrineIncomeLimit();
            if (eGlobalCommerceReligion != NO_RELIGION)
			{
				iCommerceRate += std::min(iShrineLimit,
                        GC.getInfo(eGlobalCommerceReligion).getGlobalReligionCommerce(eCommerce) *
						GC.getGame().countReligionLevels(eGlobalCommerceReligion) *
						getNumActiveBuilding(eBuilding));
			}

		    // doc: Guadalupe Basilica effect
		    if (eBuilding == GUADALUPE_BASILICA && eCommerce == COMMERCE_GOLD)
		    {
		        iCommerceRate += std::min(iShrineLimit, getContinentArea().countHasReligion(CATHOLICISM));
		    }
		}
		{
			CorporationTypes const eGlobalCommerceCorp = kBuilding.getGlobalCorporationCommerce();
			if (eGlobalCommerceCorp != NO_CORPORATION)
			{
				iCommerceRate += (GC.getInfo(eGlobalCommerceCorp).
						getHeadquarterCommerce(eCommerce) *
						GC.getGame().countCorporationLevels(eGlobalCommerceCorp)) *
						getNumActiveBuilding(eBuilding);
			}
		}
	}
	return iCommerceRate;
}


void CvCity::updateBuildingCommerce()
{
	FOR_EACH_ENUM(Commerce)
	{	// advc: Moved into new function
		updateBuildingCommerce(eLoopCommerce);
	}
}

// advc.opt: Cut from updateBuildingCommerce above
void CvCity::updateBuildingCommerce(CommerceTypes eCommerce)
{
	int iNewBuildingCommerce = 0;
	FOR_EACH_ENUM(Building)
	{
		iNewBuildingCommerce += getBuildingCommerceByBuilding(
				eCommerce, eLoopBuilding);
	}
	if (getBuildingCommerce(eCommerce) != iNewBuildingCommerce)
	{
		m_aiBuildingCommerce.set(eCommerce, iNewBuildingCommerce);
		FAssert(getBuildingCommerce(eCommerce) >= 0);
		updateCommerce(eCommerce);
	}
}

// BUG - Building Additional Commerce - start
/*  Returns the total additional commerce times 100 that
	adding one of the given buildings will provide.
	Doesn't check if the building can be constructed in this city.
	Takes the NO_ESPIONAGE game option into account for CULTURE and ESPIONAGE. */
int CvCity::getAdditionalCommerceTimes100ByBuilding(CommerceTypes eCommerce,
	BuildingTypes eBuilding) const
{
	int iExtraRate = getAdditionalBaseCommerceRateByBuilding(eCommerce, eBuilding);
	int iExtraModifier = getAdditionalCommerceRateModifierByBuilding(eCommerce, eBuilding);
	if (iExtraRate == 0 && iExtraModifier == 0)
		return 0;

	int iRateTimes100 = getBaseCommerceRateTimes100(eCommerce);
	int iModifier = getTotalCommerceRateModifier(eCommerce);
	int iExtraTimes100 = ((iModifier + iExtraModifier) *
			(100 * iExtraRate + iRateTimes100) / 100)
			- (iModifier * iRateTimes100 / 100);

	return iExtraTimes100;
}

/*  Returns the additional base commerce rate constructing the given building will provide.
	Doesn't check if the building can be constructed in this city.
	Takes the NO_ESPIONAGE game option into account for CULTURE and ESPIONAGE. */
int CvCity::getAdditionalBaseCommerceRateByBuilding(CommerceTypes eCommerce,
	BuildingTypes eBuilding) const
{
	bool bNoEspionage = GC.getGame().isOption(GAMEOPTION_NO_ESPIONAGE);
	if (bNoEspionage && eCommerce == COMMERCE_ESPIONAGE)
		return 0;

	int iExtraRate = getAdditionalBaseCommerceRateByBuildingImpl(eCommerce, eBuilding);
	if (bNoEspionage && eCommerce == COMMERCE_CULTURE)
	{
		iExtraRate += getAdditionalBaseCommerceRateByBuildingImpl(
				COMMERCE_ESPIONAGE, eBuilding);
	}
	return iExtraRate;
}

/*  Returns the additional base commerce rate constructing the given building will provide.
	Doesn't check if the building can be constructed in this city. */
int CvCity::getAdditionalBaseCommerceRateByBuildingImpl(CommerceTypes eCommerce,
	BuildingTypes eBuilding) const
{
	CvBuildingInfo const& kBuilding = GC.getInfo(eBuilding);

	int iExtraRate = kBuilding.getObsoleteSafeCommerceChange(eCommerce);
	if (GET_TEAM(getTeam()).isObsoleteBuilding(eBuilding))
		return iExtraRate;

	iExtraRate += kBuilding.getCommerceChange(eCommerce);
	iExtraRate += getBuildingCommerceChange(kBuilding.getBuildingClassType(), eCommerce);
	CvPlayer const& kOwner = GET_PLAYER(getOwner());
	if (kBuilding.getReligionType() != NO_RELIGION)
	{
		if (kBuilding.getReligionType() == kOwner.getStateReligion())
			iExtraRate += kOwner.getStateReligionBuildingCommerce(eCommerce);
	}
	{
		ReligionTypes const eGlobalCommerceReligion = kBuilding.getGlobalReligionCommerce();
		if (eGlobalCommerceReligion != NO_RELIGION)
		{
			iExtraRate += GC.getInfo(eGlobalCommerceReligion).
					getGlobalReligionCommerce(eCommerce) *
					GC.getGame().countReligionLevels(eGlobalCommerceReligion);
		}
	}
	{
		CorporationTypes eGlobalCommerceCorp = kBuilding.getGlobalCorporationCommerce();
		if (eGlobalCommerceCorp != NO_CORPORATION)
		{
			iExtraRate += GC.getInfo(eGlobalCommerceCorp).
					getHeadquarterCommerce(eCommerce) *
					GC.getGame().countCorporationLevels(eGlobalCommerceCorp);
		}
	}
	// ignore double-time check since this assumes you are building it this turn

	FOR_EACH_NON_DEFAULT_PAIR(kBuilding.
		getFreeSpecialistCount(), Specialist, int)
	{
		iExtraRate += getAdditionalBaseCommerceRateBySpecialistImpl(eCommerce,
				perSpecialistVal.first, perSpecialistVal.second);
	}

	return iExtraRate;
}

/*  Doesn't check if the building can be constructed in this city.
	Takes the NO_ESPIONAGE game option into account for CULTURE and ESPIONAGE. */
int CvCity::getAdditionalCommerceRateModifierByBuilding(CommerceTypes eCommerce,
	BuildingTypes eBuilding) const
{
	bool const bNoEspionage = GC.getGame().isOption(GAMEOPTION_NO_ESPIONAGE);
	if (bNoEspionage && eCommerce == COMMERCE_ESPIONAGE)
		return 0;

	int iExtraModifier = getAdditionalCommerceRateModifierByBuildingImpl(
			eCommerce, eBuilding);
	if (bNoEspionage && eCommerce == COMMERCE_CULTURE)
	{
		iExtraModifier += getAdditionalCommerceRateModifierByBuildingImpl(
				COMMERCE_ESPIONAGE, eBuilding);
	}
	return iExtraModifier;
}

/*  Returns the additional commerce rate modifier constructing the given building will provide.
	Doesn't check if the building can be constructed in this city. */
int CvCity::getAdditionalCommerceRateModifierByBuildingImpl(CommerceTypes eCommerce,
	BuildingTypes eBuilding) const
{
	if (!GET_TEAM(getTeam()).isObsoleteBuilding(eBuilding))
	{
		CvBuildingInfo const& kBuilding = GC.getInfo(eBuilding);
		return kBuilding.getCommerceModifier(eCommerce) +
				kBuilding.getGlobalCommerceModifier(eCommerce);
	}
	return 0;
}
// BUG - Building Additional Commerce - end

void CvCity::changeSpecialistCommerce(CommerceTypes eCommerce, int iChange)
{
	if (iChange != 0)
	{
		m_aiSpecialistCommerce.add(eCommerce, iChange);
		FAssert(getSpecialistCommerce(eCommerce) >= 0);
		updateCommerce(eCommerce);
	}
}

// BUG - Specialist Additional Commerce - start
/*  Returns the total additional commerce times 100 that changing the number
	of given specialists will provide/remove.
	Takes the NO_ESPIONAGE game option into account for CULTURE and ESPIONAGE. */
int CvCity::getAdditionalCommerceTimes100BySpecialist(CommerceTypes eCommerce,
	SpecialistTypes eSpecialist, int iChange) const
{
	int iExtraRate = getAdditionalBaseCommerceRateBySpecialist(
			eCommerce, eSpecialist, iChange);
	if (iExtraRate == 0)
		return 0;

	int iRateTimes100 = getBaseCommerceRateTimes100(eCommerce);
	int iModifier = getTotalCommerceRateModifier(eCommerce);
	int iExtraTimes100 = (iModifier * (100 * iExtraRate + iRateTimes100) / 100) -
			(iModifier * iRateTimes100 / 100);

	return iExtraTimes100;
}

/*  Returns the additional base commerce rate that changing the number
	of given specialists will provide/remove.
	Takes the NO_ESPIONAGE game option into account for CULTURE and ESPIONAGE. */
int CvCity::getAdditionalBaseCommerceRateBySpecialist(CommerceTypes eCommerce,
	SpecialistTypes eSpecialist, int iChange) const
{
	bool const bNoEspionage = GC.getGame().isOption(GAMEOPTION_NO_ESPIONAGE);
	if (bNoEspionage && eCommerce == COMMERCE_ESPIONAGE)
		return 0;

	int iExtraRate = getAdditionalBaseCommerceRateBySpecialistImpl(
			eCommerce, eSpecialist, iChange);
	if (bNoEspionage && eCommerce == COMMERCE_CULTURE)
	{
		iExtraRate += getAdditionalBaseCommerceRateBySpecialistImpl(
				COMMERCE_ESPIONAGE, eSpecialist, iChange);
	}
	return iExtraRate;
}

/*	Returns the additional base commerce rate that changing the number
	of given specialists will provide/remove. */
int CvCity::getAdditionalBaseCommerceRateBySpecialistImpl(CommerceTypes eCommerce,
	SpecialistTypes eSpecialist, int iChange) const
{
	// advc: Forward to CvPlayer (based on MNAI - lfgr fix 01/2022)
	return iChange * GET_PLAYER(getOwner()).specialistCommerce(eSpecialist, eCommerce);
}
// BUG - Specialist Additional Commerce - end

int CvCity::getReligionCommerceByReligion(CommerceTypes eCommerce,
	ReligionTypes eReligion, /* advc: */ bool bForce) const
{
	int iCommerceRate = 0;
	// advc.172: Commented out
	/*if (GET_PLAYER(getOwner()).getStateReligion() == eReligion ||
		GET_PLAYER(getOwner()).getStateReligion() == NO_RELIGION)*/
	{
		if (isHasReligion(eReligion) /* advc: */ || bForce)
		{
			iCommerceRate += GC.getInfo(eReligion).getStateReligionCommerce(eCommerce);
			if (isHolyCity(eReligion))
				iCommerceRate += GC.getInfo(eReligion).getHolyCityCommerce(eCommerce);
		}
	}
	return iCommerceRate;
}

// XXX can this be simplified???
void CvCity::updateReligionCommerce(CommerceTypes eCommerce)
{
	int iNewReligionCommerce = 0;
	FOR_EACH_ENUM(Religion)
	{	// advc.172: No longer cumulative; use max.
		iNewReligionCommerce = std::max(iNewReligionCommerce,
				getReligionCommerceByReligion(eCommerce, eLoopReligion));
	}
	if (getReligionCommerce(eCommerce) != iNewReligionCommerce)
	{
		m_aiReligionCommerce.set(eCommerce, iNewReligionCommerce);
		FAssert(getReligionCommerce(eCommerce) >= 0);
		updateCommerce(eCommerce);
	}
}


void CvCity::updateReligionCommerce()
{
	FOR_EACH_ENUM(Commerce)
		updateReligionCommerce(eLoopCommerce);
}


void CvCity::setCorporationYield(YieldTypes eYield, int iNewValue)
{
	int const iOldValue = getCorporationYield(eYield);
	if (iOldValue != iNewValue)
	{
		m_aiCorporationYield.set(eYield, iNewValue);
		FAssert(getCorporationYield(eYield) >= 0);
		changeBaseYieldRate(eYield, iNewValue - iOldValue);
	}
}


int CvCity::getCorporationYieldByCorporation(YieldTypes eYield,
	CorporationTypes eCorporation) const
{
	int iYieldRate = 0;
	if (isActiveCorporation(eCorporation) && !isDisorder())
	{
		for (int i = 0; i < GC.getInfo(eCorporation).getNumPrereqBonuses(); i++)
		{
			BonusTypes const eBonus = GC.getInfo(eCorporation).getPrereqBonus(i);
			if (getNumBonuses(eBonus) > 0)
			{
                // TODO: removed corporation bonus limit, adjust corporation info and balance differently
				iYieldRate += (GC.getInfo(eCorporation).getYieldProduced(eYield) *
						getNumBonuses(eBonus) * GC.getInfo(GC.getMap().getWorldSize()).
						getCorporationMaintenancePercent()) / 100;
			}
		}
	}

    // doc: Dutch UP: double yield from trading company
    if (getCivilizationType() == NETHERLANDS && eCorporation == CORPORATION_TRADING_COMPANY)
        iYieldRate *= 2;

	return intdiv::uceil(iYieldRate, 100);
}

int CvCity::getCorporationCommerceByCorporation(CommerceTypes eCommerce,
	CorporationTypes eCorporation) const
{
	int iCommerceRate = 0;
	if (isActiveCorporation(eCorporation) && !isDisorder())
	{
		for (int i = 0; i < GC.getInfo(eCorporation).getNumPrereqBonuses(); i++)
		{
			BonusTypes const eBonus = GC.getInfo(eCorporation).getPrereqBonus(i);
			if (getNumBonuses(eBonus) > 0)
			{
                // TODO: removed corporation bonus limit, adjust corporation info and balance differently
				iCommerceRate += (GC.getInfo(eCorporation).
						getCommerceProduced(eCommerce) *
						getNumBonuses(eBonus) * GC.getInfo(GC.getMap().getWorldSize()).
						getCorporationMaintenancePercent()) / 100;
			}
		}
	}

    // doc: civic corporation commerce modifier
    iCommerceRate *= 100 + GET_PLAYER(getOwner()).getCorporationCommerceModifier();
    iCommerceRate /= 100;

    // doc: Dutch UP: double commerce from trading company
	if (getCivilizationType() == NETHERLANDS && eCorporation == CORPORATION_TRADING_COMPANY)
		iCommerceRate *= 2;

	return intdiv::uceil(iCommerceRate, 100);
}

void CvCity::updateCorporationCommerce(CommerceTypes eCommerce)
{
	int iNewRate = 0;
	FOR_EACH_ENUM(Corporation)
		iNewRate += getCorporationCommerceByCorporation(eCommerce, eLoopCorporation);

	if (getCorporationCommerce(eCommerce) != iNewRate)
	{
		m_aiCorporationCommerce.set(eCommerce, iNewRate);
		FAssert(getCorporationCommerce(eCommerce) >= 0);
		updateCommerce(eCommerce);
	}
}

void CvCity::updateCorporationYield(YieldTypes eYield)
{
	int const iOldRate = getCorporationYield(eYield);
	int iNewRate = 0;

	FOR_EACH_ENUM(Corporation)
		iNewRate += getCorporationYieldByCorporation(eYield, eLoopCorporation);

	if (iOldRate != iNewRate)
	{
		m_aiCorporationYield.set(eYield, iNewRate);
		FAssert(getCorporationYield(eYield) >= 0);
		changeBaseYieldRate(eYield, iNewRate - iOldRate);
	}
}

// doc
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


void CvCity::updateCorporation(/* advc.064d: */ bool bVerifyProduction)
{
	updateCorporationBonus(/* advc.06d: */ bVerifyProduction);
	updateBuildingCommerce();

	FOR_EACH_ENUM(Yield)
		updateCorporationYield(eLoopYield);

	FOR_EACH_ENUM(Commerce)
		updateCorporationCommerce(eLoopCommerce);

	updateMaintenance();

	updateCorporationHappiness();

	updateCorporationHealth();
}


void CvCity::updateCorporationBonus(/* advc.064d: */ bool bVerifyProduction)
{
	EagerEnumMap<BonusTypes,int> aiLastCorpProducedBonuses;
	EagerEnumMap<BonusTypes,bool> abHadBonuses;
    EagerEnumMap<BonusTypes,bool> abHadBonusEffects; // doc: limited bonus effects
	FOR_EACH_ENUM(Bonus)
	{
		abHadBonuses.set(eLoopBonus, hasBonus(eLoopBonus));
        abHadBonusEffects.set(eLoopBonus, hasBonusEffect(eLoopBonus));
		aiLastCorpProducedBonuses.set(eLoopBonus, getNumBonuses(eLoopBonus));
	}
	m_aiNumCorpProducedBonuses.reset();
	EagerEnumMap<BonusTypes,int> aiExtraCorpProducedBonuses;
	CvTeam const& kTeam = GET_TEAM(getTeam());
	for (int iIter = 0; iIter < GC.getNumCorporationInfos(); iIter++)
	{
		FOR_EACH_ENUM(Corporation)
		{
			BonusTypes eBonusProduced = GC.getInfo(eLoopCorporation).getBonusProduced();
			if (eBonusProduced == NO_BONUS ||
				kTeam.isBonusObsolete(eBonusProduced) ||
				!kTeam.isHasTech(GC.getInfo(eBonusProduced).getTechCityTrade()))
			{
				continue;
			}
			if (isHasCorporation(eLoopCorporation) &&
				GET_PLAYER(getOwner()).isActiveCorporation(eLoopCorporation))
			{
				for (int i = 0; i < GC.getInfo(eLoopCorporation).getNumPrereqBonuses(); i++)
				{
					BonusTypes eBonusConsumed = GC.getInfo(eLoopCorporation).
							getPrereqBonus(i);
					aiExtraCorpProducedBonuses.add(eBonusProduced,
							aiLastCorpProducedBonuses.get(eBonusConsumed));
				}
			}
		}
		bool bChanged = false;
		FOR_EACH_ENUM2(Bonus, e)
		{
			if (aiExtraCorpProducedBonuses.get(e) != 0)
			{
				m_aiNumCorpProducedBonuses.add(e, aiExtraCorpProducedBonuses.get(e));
				bChanged = true;
			}
			aiLastCorpProducedBonuses.set(e, aiExtraCorpProducedBonuses.get(e));
		}
		aiExtraCorpProducedBonuses.reset();
		if (!bChanged)
			break;
		FAssertMsg(iIter < GC.getNumCorporationInfos() - 1, "cyclical resource dependency");
	}

	FOR_EACH_ENUM(Bonus)
	{
		if (abHadBonuses.get(eLoopBonus) != hasBonus(eLoopBonus))
		{
			if (hasBonus(eLoopBonus))
				processBonus(eLoopBonus, 1);
			else
			{
				processBonus(eLoopBonus, -1);
				// <advc.064d>
				if (bVerifyProduction)
					verifyProduction(); // </advc.064d>
			}
		}

	    if (abHadBonusEffects.get(eLoopBonus) != hasBonusEffect(eLoopBonus))
	    {
	        if (hasBonusEffect(eLoopBonus))
	            processBonusEffect(eLoopBonus, 1);
	        else
	            processBonusEffect(eLoopBonus, -1);
	    }
	}
}


void CvCity::changeCommerceRateModifier(CommerceTypes eCommerce, int iChange)
{
	if (iChange != 0)
	{
		m_aiCommerceRateModifier.add(eCommerce, iChange);
		updateCommerce(eCommerce);
		AI_setAssignWorkDirty(true);
	}
}


// doc
// TODO: refactor
int CvCity::getPowerCommerceRateModifier(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");
	return m_aiPowerCommerceRateModifier[eIndex];
}


// doc
void CvCity::changePowerCommerceRateModifier(CommerceTypes eCommerce, int iChange)
{
	if (iChange != 0)
	{
		m_aiPowerCommerceRateModifier.add(eCommerce, iChange);

		if (iChange > 0)
		{
			changePowerConsumedCount(1);
		}
		else if (iChange < 0)
		{
			changePowerConsumedCount(-1);
		}

		updateCommerce(eCommerce);

		AI_setAssignWorkDirty(true);
	}
}


// doc
void CvCity::changeCultureCommerceRateModifier(CommerceTypes eCommerce, int iChange)
{
	if (iChange != 0)
	{
		m_aiCultureCommerceRateModifier.add(eCommerce, iChange);

		updateCommerce(eCommerce);

		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getCommerceHappinessByType(CommerceTypes eCommerce) const
{
	return ((getCommerceHappinessPer(eCommerce) *
			GET_PLAYER(getOwner()).getCommercePercent(eCommerce)) / 100);
}


int CvCity::getCommerceHappiness() const
{
	int iHappiness = 0;
	FOR_EACH_ENUM(Commerce)
		iHappiness += getCommerceHappinessByType(eLoopCommerce);
	return iHappiness;
}


void CvCity::changeCommerceHappinessPer(CommerceTypes eCommerce, int iChange)
{
	if (iChange != 0)
	{
		m_aiCommerceHappinessPer.add(eCommerce, iChange);
		FAssert(getCommerceHappinessPer(eCommerce) >= 0);
		AI_setAssignWorkDirty(true);
	}
}


void CvCity::changeDomainFreeExperience(DomainTypes eDomain, int iChange)
{
	m_aiDomainFreeExperience.add(eDomain, iChange);
	FAssert(getDomainFreeExperience(eDomain) >= 0);
}


void CvCity::changeDomainProductionModifier(DomainTypes eDomain, int iChange)
{
	m_aiDomainProductionModifier.add(eDomain, iChange);
}


// doc
// TODO: refactor
int CvCity::getCulture(CivilizationTypes eCivilization) const
{
	FAssertMsg(eCivilization >= 0, "eCivilization expected to be non-negative");
	FAssertMsg(eCivilization < NUM_TOTAL_CIVILIZATIONS, "eCivilization expected to be within maximum bounds");

	return getCultureTimes100(eCivilization) / 100;
}


// doc
int CvCity::getCulture(PlayerTypes ePlayer) const
{
	CivilizationTypes eCivilization = GET_PLAYER(ePlayer).getCivilizationType();
	if (eCivilization == NO_CIVILIZATION)
		return 0;

	return getCulture(eCivilization);
}

// doc
int CvCity::getActualCultureTimes100(CivilizationTypes eCivilization) const
{
	return m_aiCulture.get(eCivilization);
}

// doc
int CvCity::getActualCultureTimes100(PlayerTypes eIndex) const
{
	CivilizationTypes eCivilization = GET_PLAYER(eIndex).getCivilizationType();
	if (eCivilization == NO_CIVILIZATION)
		return 0;

	return getActualCultureTimes100(eCivilization);
}

// doc
int CvCity::getActualCulture(PlayerTypes ePlayer) const
{
	return getActualCultureTimes100(ePlayer) / 100;
}

// doc
int CvCity::getCultureTimes100(CivilizationTypes eCivilization) const
{
	if (plot()->getCultureConversionCivilization() == eCivilization)
	{
		return (getActualTotalCultureTimes100() - getActualCultureTimes100(eCivilization)) / 100 * getPlot().getCultureConversionRate() + getActualCultureTimes100(eCivilization);
	}

	return getActualCultureTimes100(eCivilization) / 100 * (100 - getPlot().getCultureConversionRate());
}

// doc
int CvCity::getCultureTimes100(PlayerTypes ePlayer) const
{
	CivilizationTypes eCivilization = GET_PLAYER(ePlayer).getCivilizationType();
	if (eCivilization == NO_CIVILIZATION)
		return 0;

	return getCultureTimes100(eCivilization);
}


int CvCity::countTotalCultureTimes100() const
{
	int iTotalCulture = 0;
	for (PlayerIter<EVER_ALIVE> it; it.hasNext(); ++it) // advc.099: was ALIVE
	{
        // doc: use actual culture
		iTotalCulture += getCultureTimes100(it->getID());
	}

	return iTotalCulture;
}


PlayerTypes CvCity::findHighestCulture(bool bIgnoreMinors) const
{
	PlayerTypes eBestPlayer = NO_PLAYER;
	int iBestValue = 0;
	for (PlayerIter<EVER_ALIVE> it; it.hasNext(); ++it) // advc.099: was ALIVE
	{
        // doc: optionally exclude minors
        if (bIgnoreMinors && it->isMinorCiv())
            continue;

		int iValue = getCultureTimes100(it->getID());
		if (iValue > iBestValue)
		{
			iBestValue = iValue;
			eBestPlayer = it->getID();
		}

	}
	return eBestPlayer;
}

/*	advc.101:
	Doesn't check if city will flip. Doesn't take into account that the revolt test
	is skipped when decreasing the occupation timer.
	Difference from getRevoltTestProbability: that function only returns the
	probability of the first revolt test, not the second one based on
	culture garrison.
	If bIgnoreWar is set, a probability is returned even if the city can't revolt
	(i.e. when it's already in occupation and at war with the cultural owner).
	If bIgnoreGarrison is set, culture garrison strength is treated as 0.
	If bIgnoreOccupation is set, the probability is computed assuming that the city
	isn't in occupation. */
scaled CvCity::revoltProbability(bool bIgnoreWar,
	bool bIgnoreGarrison, bool bIgnoreOccupation) const // advc.023
{
	PlayerTypes eCulturalOwner = calculateCulturalOwner(); // advc.099c
	static bool const bBARBS_REVOLT = GC.getDefineBOOL("BARBS_REVOLT");
	if (eCulturalOwner == NO_PLAYER || TEAMID(eCulturalOwner) == getTeam() ||
		// advc.099c: Barbarian revolts
		(eCulturalOwner == BARBARIAN_PLAYER && !bBARBS_REVOLT))
	{
		return 0;
	}
	int iCityStrength = cultureStrength(eCulturalOwner,
			bIgnoreWar, bIgnoreOccupation); // advc.023
	int iGarrison =
			(bIgnoreGarrison ? 0 : // advc.023
			cultureGarrison(eCulturalOwner));
	if (iCityStrength <= iGarrison)
		return 0;
	/*  About the two revolt tests: I guess the first one checks if the city tries
		to revolt, and the second if the garrison can stop the revolt.
		Restored the BtS formula for the second test. */
	scaled r = scaled::max(0, (1 - scaled(iGarrison, iCityStrength))) *
			getRevoltTestProbability();
	// Don't use probabilities that are too small to be displayed
	if (r.getPermille() < 1)
		return 0;
	if (r.getPermille() > 999)
		return 1;
	return r;
}

// advc.023:
scaled CvCity::probabilityOccupationDecrement() const
{
	if(!isOccupation())
		return 0;
	// While at war, require an occupying force.
	if(getMilitaryHappinessUnits() <= 0 && GET_PLAYER(getOwner()).isMajorCiv())
	{
		PlayerTypes eCulturalOwner = calculateCulturalOwner();
		if(eCulturalOwner != NO_PLAYER && GET_TEAM(eCulturalOwner).isAtWar(getTeam()))
			return 0;
	}
	scaled r;
	scaled rRevoltProb = revoltProbability(true, false, true);
	/*	Cancel out the speed adjustment included in rRevoltProb
		(because the countdown length is not speed-adjusted) */
	rRevoltProb *= per100(GC.getInfo(GC.getGame().getGameSpeedType()).get(
			CvGameSpeedInfo::RevoltDivPercent));
	if (rRevoltProb < 1)
		r = (1 - rRevoltProb).pow(GC.getDefineINT(CvGlobals::OCCUPATION_COUNTDOWN_EXPONENT));
	// Don't use probabilities that are too small to be displayed
	if (r.getPermille() < 1)
		return 0;
	if (r.getPermille() > 999)
		return 1;
	return r;
}

// K-Mod: Whether or not the city is allowed to flip to the given player
bool CvCity::canCultureFlip(PlayerTypes eToPlayer,
	bool bCheckPriorRevolts) const // advc.101
{
	/*if (isBarbarian())
		return true;*/ // advc.101: Commented out
	// <advc.099c>
	if (eToPlayer == NO_PLAYER)
		eToPlayer = getPlot().calculateCulturalOwner();
	else if (!getPlot().isWithinCultureRange(eToPlayer))
		return false;
	if(eToPlayer == NO_PLAYER || eToPlayer == getOwner() ||
		!GET_PLAYER(eToPlayer).isAlive() || eToPlayer == BARBARIAN_PLAYER ||
		GET_TEAM(eToPlayer).isVassal(getTeam()))
	{
		return false;
	} // </advc.099c>
	return (!GC.getGame().isOption(GAMEOPTION_NO_CITY_FLIPPING) &&
			// advc.101: City flipping option negated (now has inverse meaning)
			(!GC.getGame().isOption(GAMEOPTION_NO_FLIPPING_AFTER_CONQUEST) ||
			getPreviousCiv() == NO_CIVILIZATION ||
			!isPreviousOwner(eToPlayer)) && // advc
			(!bCheckPriorRevolts || // advc.101
			getNumRevolts(eToPlayer) >= GC.getDefineINT(CvGlobals::NUM_WARNING_REVOLTS)
			- (isBarbarian() ? 1 : 0))); // advc.101
}

// advc.023: Conditions for easier suppression while at war
bool CvCity::isMartialLaw(PlayerTypes eRevoltPlayer) const
{
	CvPlayer const& kRevoltPlayer = GET_PLAYER(eRevoltPlayer);
	return (kRevoltPlayer.isAlive() && kRevoltPlayer.isMajorCiv() &&
			GET_TEAM(getTeam()).isAtWar(kRevoltPlayer.getTeam()));
}


// doc: civilization based culture
int CvCity::calculateCulturePercent(CivilizationTypes eCivilization) const
{
    int iTotalCulture = countTotalCultureTimes100() / 100;
    if (iTotalCulture > 0)
        return getCultureTimes100(eCivilization) / iTotalCulture;
    if (getCivilizationType() == eCivilization)
        return 100;
    return 0;
}


// doc: civilization based culture
int CvCity::calculateCulturePercent(PlayerTypes ePlayer) const
{
    return calculateCulturePercent(GET_PLAYER(ePlayer).getCivilizationType());
}


// doc: civilization based culture
// TODO: refactor
int CvCity::calculateOverallCulturePercent(CivilizationTypes eCivilization) const
{
    int iTotalCulture = 0;
	FOR_EACH_ENUM(Civilization)
    {
        iTotalCulture += getCultureTimes100(eLoopCivilization);
    }

    if (iTotalCulture > 0)
    {
		iTotalCulture /= 100;
		return getCultureTimes100(eCivilization) / iTotalCulture;
    }

    return 0;
}


// doc: civilization based culture
// TODO: refactor
int CvCity::calculateOverallCulturePercent(PlayerTypes ePlayer) const
{
    int iTotalCulture = calculateOverallCulturePercent(GET_PLAYER(ePlayer).getCivilizationType());

    if (iTotalCulture == 0 && getOwner() == ePlayer)
    {
        return 100;
    }

    return iTotalCulture;
}


int CvCity::calculateTeamCulturePercent(TeamTypes eTeam) const
{
	int iR = 0;
	for (PlayerIter<EVER_ALIVE,MEMBER_OF> it(eTeam); it.hasNext(); ++it) // advc.099: was ALIVE
	{
		iR += calculateCulturePercent(it->getID());
	}
	return iR;
}


// doc: civilization based culture
void CvCity::setCulture(CivilizationTypes eCivilization, int iNewValue)
{
    setCultureTimes100(eCivilization, 100 * iNewValue);
}


void CvCity::setCulture(PlayerTypes ePlayer, int iNewValue, bool bPlots,
	bool bUpdatePlotGroups)
{
	setCultureTimes100(ePlayer, 100 * iNewValue, bPlots, bUpdatePlotGroups);
}

// doc: civilization based culture
void CvCity::setCultureTimes100(CivilizationTypes eCivilization, int iNewValue)
{
    // doc: culture conversion
    int const iOldValue = getActualCultureTimes100(eCivilization);
    if (iNewValue == iOldValue)
        return;
    m_aiCulture.set(eCivilization, iNewValue);
    FAssert(getCultureTimes100(ePlayer) >= 0);

    // doc: track total culture
    m_iTotalCultureTimes100 += iNewValue - iOldValue;

    // doc: Byzantine UP: +1 gold per 200 culture in capital
    if (getCivilizationType() == BYZANTIUM && eCivilization == BYZANTIUM)
    {
        if (isCapital())
        {
            int iGoldChange = iNewValue / 20000 - iOldValue / 20000;
            if (iGoldChange != 0)
            {
                // TODO: building class enum
                changeBuildingCommerceChange(BUILDINGCLASS_PALACE, COMMERCE_GOLD, iGoldChange);
            }
        }
    }
}

// K-Mod, 26/sep/10: fixed so that plots actually get the culture difference
void CvCity::setCultureTimes100(PlayerTypes ePlayer, int iNewValue, bool bPlots,
	bool bUpdatePlotGroups)
{
    // doc: culture conversion
	int const iOldValue = getActualCultureTimes100(ePlayer);
	if (iNewValue == iOldValue)
		return;
	setCultureTimes100(GET_PLAYER(ePlayer).getCivilizationType(), iNewValue);
	FAssert(getCultureTimes100(ePlayer) >= 0);
	updateCultureLevel(bUpdatePlotGroups);
    updateCoveredPlots(bUpdatePlotGroups); // doc: gradual border expansion
	if (bPlots)
	{
		//doPlotCulture(true, ePlayer, 0);
		//doPlotCulture(true, ePlayer, (iNewValue - iOldValue) / 100);
		doPlotCultureTimes100(true, ePlayer, iNewValue - iOldValue, false);
		/*	note: this function no longer applies free city culture.
			also, note that if a city's culture is decreased to zero,
			there will probably still be some residual plot culture around the city.
			this is because the culture level on the way up
			will be higher than it is on the way down. */
	}
}

// doc: civilization based culture
void CvCity::changeCulture(CivilizationTypes eCivilization, int iChange)
{
    // doc: culture conversion
	setCultureTimes100(eCivilization, getActualCultureTimes100(eCivilization) + 100 * iChange);
}

void CvCity::changeCulture(PlayerTypes ePlayer, int iChange, bool bPlots,
	bool bUpdatePlotGroups)
{
    // doc: culture conversion
	setCultureTimes100(ePlayer, getActualCultureTimes100(ePlayer) + 100 * iChange,
			bPlots, bUpdatePlotGroups);
}

// doc: civilization based culture
void CvCity::changeCultureTimes100(CivilizationTypes eCivilization, int iChange)
{
    // doc: culture conversion
    setCultureTimes100(eCivilization, getActualCultureTimes100(eCivilization) + iChange);
}


void CvCity::changeCultureTimes100(PlayerTypes ePlayer, int iChange, bool bPlots,
	bool bUpdatePlotGroups)
{
    // doc: culture conversion
	setCultureTimes100(ePlayer, getActualCultureTimes100(ePlayer) + iChange,
			bPlots, bUpdatePlotGroups);
}

// advc.099c: To the current cultural owner
int CvCity::getNumRevolts() const
{
	PlayerTypes eCultOwner = calculateCulturalOwner();
	if(eCultOwner == NO_PLAYER)
		return 0;
	return getNumRevolts(eCultOwner);
} // </advc.099c>


void CvCity::changeNumRevolts(PlayerTypes ePlayer, int iChange)
{
	m_aiNumRevolts.add(ePlayer, iChange);
	FAssert(getNumRevolts(ePlayer) >= 0);
}


scaled CvCity::getRevoltTestProbability() const // advc.101: Return type was int
{
	// <advc.101>
	CvGame const& kGame = GC.getGame();
	scaled rSpeedFactor = std::max(scaled::epsilon(),
			per100(GC.getInfo(kGame.getGameSpeedType()).get(
			// K-Mod had used VictoryDelayPercent
			CvGameSpeedInfo::RevoltDivPercent)));
	// Need to cut cities recently acquired by Barbarians some slack
	if (isBarbarian() && kGame.getGameTurn() - getGameTurnAcquired() < 8 * rSpeedFactor)
		return 0; // </advc.101>
	static scaled const rREVOLT_TEST_PROB = per100(GC.getDefineINT("REVOLT_TEST_PROB")); // advc.opt
	scaled r = rREVOLT_TEST_PROB * per100(100 - getRevoltProtection());
	r /= rSpeedFactor;
	r.decreaseTo(1); // advc.101: Upper bound used to be handled by the caller
	return r;
}

// advc.101: Cut from getRevoltTestProbability
int CvCity::getRevoltProtection() const
{
	int iBestModifier = 0;
	for (CLLNode<IDInfo> const* pUnitNode = getPlot().headUnitNode(); pUnitNode != NULL;
		pUnitNode = getPlot().nextUnitNode(pUnitNode))
	{
		CvUnit const* pLoopUnit = ::getUnit(pUnitNode->m_data);
		if (pLoopUnit->getRevoltProtection() > iBestModifier)
			iBestModifier = pLoopUnit->getRevoltProtection();
	}
	return range(iBestModifier, 0, 100);
}

// advc: Cut from CvPlot::setOwner
void CvCity::addRevoltFreeUnits()
{
	UnitTypes eBestUnit = AI().AI_bestUnitAI(UNITAI_CITY_DEFENSE);
	if (eBestUnit == NO_UNIT)
		eBestUnit = AI().AI_bestUnitAI(UNITAI_ATTACK);

	if (eBestUnit != NO_UNIT)
	{
		int iFreeUnits = (GC.getDefineINT("BASE_REVOLT_FREE_UNITS") +
				(getHighestPopulation() * GC.getDefineINT("REVOLT_FREE_UNITS_PERCENT")) / 100);
		for (int i = 0; i < iFreeUnits; i++)
		{
			GET_PLAYER(getOwner()).initUnit(eBestUnit, getX(), getY(), UNITAI_CITY_DEFENSE);
		}
	}
}


// doc
bool CvCity::isEverOwned(CivilizationTypes eCivilization) const
{
	return m_abEverOwned.get(eCivilization);
}


// doc
bool CvCity::isEverOwned(PlayerTypes ePlayer) const
{
    CivilizationTypes eCivilization = GET_PLAYER(ePlayer).getCivilizationType();
    if (eCivilization == NO_CIVILIZATION)
        return false;

    return isEverOwned(eCivilization);
}


// doc
void CvCity::setEverOwned(CivilizationTypes eCivilization, bool bNewValue)
{
	m_abEverOwned.set(eCivilization, bNewValue);
}


// doc
void CvCity::setEverOwned(PlayerTypes ePlayer, bool bNewValue)
{
    CivilizationTypes eCivilization = GET_PLAYER(ePlayer).getCivilizationType();
    if (eCivilization != NO_CIVILIZATION)
    {
        setEverOwned(eCivilization, bNewValue);
    }
}


void CvCity::setTradeRoute(PlayerTypes ePlayer, bool bNewValue)
{
	m_abTradeRoute.set(ePlayer, bNewValue);
}


bool CvCity::isRevealed(TeamTypes eTeam, bool bDebug) const
{
	if (bDebug && GC.getGame().isDebugMode())
		return true;
	return isRevealed(eTeam); // advc.inl: Call inline version
}


void CvCity::setRevealed(TeamTypes eTeam, bool bNewValue)
{
	if(isRevealed(eTeam) == bNewValue)
		return;
	// <advc.130n>
	for (MemberAIIter itMember(eTeam); itMember.hasNext(); ++itMember)
		itMember->AI_updateIdeologyAttitude(-1, *this); // </advc.130n>
	m_abRevealed.set(eTeam, bNewValue);
	// <advc.130n>
	for (MemberAIIter itMember(eTeam); itMember.hasNext(); ++itMember)
		itMember->AI_updateIdeologyAttitude(1, *this); // </advc.130n>
	// K-Mod
	if (bNewValue)
	{
		GET_TEAM(eTeam).makeHasSeen(getTeam());
		// <advc.130w>
		if (GET_TEAM(eTeam).isMajorCiv() &&
			GET_TEAM(getTeam()).isMajorCiv() &&
			getPlot().findHighestCultureTeam() != getTeam())
		{
			GET_TEAM(eTeam).AI_updateAttitude(getTeam());
		} // </advc.130w>
	} // K-Mod end

	updateVisibility();

	if (eTeam == GC.getGame().getActiveTeam())
	{
		for (CityPlotIter it(*this); it.hasNext(); ++it)
		{
			it->updateSymbols();
		}
	}
}


void CvCity::setEspionageVisibility(TeamTypes eTeam, bool bNewValue, bool bUpdatePlotGroups)
{
	if (getEspionageVisibility(eTeam) != bNewValue)
	{
		getPlot().updateSight(false, bUpdatePlotGroups);
		m_abEspionageVisibility.set(eTeam, bNewValue);
		getPlot().updateSight(true, bUpdatePlotGroups);
	}
}

void CvCity::updateEspionageVisibility(bool bUpdatePlotGroups)
{
	std::vector<EspionageMissionTypes> aMission;
	FOR_EACH_ENUM(EspionageMission)
	{
		if (GC.getInfo(eLoopEspionageMission).isPassive() &&
			GC.getInfo(eLoopEspionageMission).getVisibilityLevel() > 0)
		{
			aMission.push_back(eLoopEspionageMission);
		}
	}
	for (TeamIter<CIV_ALIVE,NOT_SAME_TEAM_AS> itTeam(getTeam()); itTeam.hasNext(); ++itTeam)
	{
		TeamTypes eOtherTeam = itTeam->getID();
		if (!isRevealed(eOtherTeam))
			continue;

		bool bVisibility = false;
		for (MemberIter itMember(eOtherTeam); itMember.hasNext() &&
			!bVisibility; ++itMember)
		{
			CvPlayer& kMember = *itMember;
			for (size_t i = 0; i < aMission.size(); i++)
			{
				if (kMember.canDoEspionageMission(aMission[i], getOwner(), plot()))
				{
					bVisibility = true;
					break;
				}
			}
		}
		setEspionageVisibility(eOtherTeam, bVisibility, bUpdatePlotGroups);
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


void CvCity::setName(const wchar* szNewValue, bool bFound, /* advc.106k: */ bool bInitial)
{
	CvWString szName(szNewValue);
	//gDLL->stripSpecialCharacters(szName); // rfc: enable ascii charset

	if (!szName.empty())
	{
		if (GET_PLAYER(getOwner()).isCityNameValid(szName, false))
		{	// <advc.106k>
			if(bInitial)
				m_szPreviousName.clear();
			else if(m_szPreviousName.empty())
				m_szPreviousName = m_szName; // </advc.106k>
			m_szName = szName;

			setInfoDirty(true);
			if (isCitySelected())
				gDLL->UI().setDirty(CityScreen_DIRTY_BIT, true);
		}
		if (bFound)
			doFoundMessage();
	}
}


void CvCity::doFoundMessage()
{
	CvWString szBuffer;
	/*	advc.106b: Seems that messages aren't supposed to be shown during advanced start
		and changing the message type causes the EXE to display the message. */
	if (GET_PLAYER(getOwner()).getAdvancedStartPoints() < 0)
	{
		szBuffer = gDLL->getText("TXT_KEY_MISC_CITY_HAS_BEEN_FOUNDED", getNameKey());
		gDLL->UI().addMessage(getOwner(), false, -1, szBuffer,
				ARTFILEMGR.getInterfaceArtInfo("WORLDBUILDER_CITY_EDIT")->getPath(),
				MESSAGE_TYPE_MAJOR_EVENT_LOG_ONLY, // advc.106b
				NULL, NO_COLOR, getX(), getY());
	}
    // rfc: display civilization birth when capital is founded
    if (isCapital() && !GET_PLAYER(getOwner()).isBarbarian() && !GET_PLAYER(getOwner()).isMinorCiv())
    {
	    szBuffer = gDLL->getText("TXT_KEY_MISC_CIV_IS_BORN", GET_PLAYER(getOwner()).getCivilizationShortDescription());
	    GC.getGame().addReplayMessage(getPlot(), REPLAY_MESSAGE_CITY_FOUNDED,
			    getOwner(), szBuffer,
			    //(ColorTypes)GC.getInfoTypeForString("COLOR_ALT_HIGHLIGHT_TEXT")
			    // advc.106: Use ALT_HIGHLIGHT for research-related stuff now
			    GET_PLAYER(getOwner()).getPlayerTextColor());
    }
}

// TODO: used?
// TODO: align/reuse with doFoundMessage
void CvCity::doFoundReplayMessage()
{
	if (isCapital() && !GET_PLAYER(getOwner()).isBarbarian() && !GET_PLAYER(getOwner()).isMinorCiv())
	{
		CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_CIV_IS_BORN", GET_PLAYER(getOwner()).getCivilizationShortDescription());
		GC.getGame().addReplayMessage(getPlot(), REPLAY_MESSAGE_CITY_FOUNDED, getOwner(), szBuffer, (ColorTypes)GC.getInfoTypeForString("COLOR_ALT_HIGHLIGHT_TEXT"));
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


void CvCity::changeNoBonusCount(BonusTypes eBonus, int iChange)
{
	if (iChange == 0)
		return; // advc

	if (getNumBonuses(eBonus) > 0)
	{
		processBonus(eBonus, -1);
		verifyProduction(); // advc.064d
	}

	m_aiNoBonus.add(eBonus, iChange);
	FAssert(getNoBonusCount(eBonus) >= 0);

	if (getNumBonuses(eBonus) > 0)
		processBonus(eBonus, 1);

	updateCorporation();

	AI_setAssignWorkDirty(true);
	setInfoDirty(true);
}


void CvCity::changeFreeBonus(BonusTypes eBonus, int iChange)
{
	if (iChange != 0)
	{
		getPlot().updatePlotGroupBonus(false, /* advc.064d: */ false);
		m_aiFreeBonus.add(eBonus, iChange);
		FAssert(getFreeBonus(eBonus) >= 0);
		getPlot().updatePlotGroupBonus(true);
	}
}

int CvCity::getNumBonuses(BonusTypes eBonus) const
{
	if (isNoBonus(eBonus))
		return 0;
	return m_aiNumBonuses.get(eBonus) + //m_aiNumCorpProducedBonuses.get(eBonus);
			// advc.003j: Don't want to leave this function entirely unused
			getNumCorpProducedBonuses(eBonus);
}


// doc: limited bonus effects
bool CvCity::hasBonusEffect(BonusTypes eBonus) const
{
    return getNumBonuses(eBonus) * GC.getBonusInfo(eBonus).getAffectedCities() > getCultureRank();
}


void CvCity::changeNumBonuses(BonusTypes eBonus, int iChange,
	bool bVerifyProduction) // advc.064d
{
	if (iChange == 0)
		return;

	bool const bOldHasBonus = hasBonus(eBonus);
    bool const bOldHasBonusEffect = hasBonusEffect(eBonus);
	m_aiNumBonuses.add(eBonus, iChange);
	if (bOldHasBonus != hasBonus(eBonus))
	{
		if (hasBonus(eBonus))
			processBonus(eBonus, 1);
		else processBonus(eBonus, -1);
	}
    if (bOldHasBonusEffect != hasBonusEffect(eBonus))
    {
        if (hasBonusEffect(eBonus))
            processBonusEffect(eBonus, 1);
        else processBonusEffect(eBonus, -1);
    }

	if (isCorporationBonus(eBonus))
		updateCorporation(/* advc.06d: */ bVerifyProduction);
}

// advc.149:
int CvCity::countUniqueBonuses() const
{
	int r = 0;
	FOR_EACH_ENUM(Bonus)
	{
		if (hasBonus(eLoopBonus))
			r++;
	}
	return r;
}


bool CvCity::isCorporationBonus(BonusTypes eBonus) const
{
	FOR_EACH_ENUM(Corporation)
	{
		if (!GET_PLAYER(getOwner()).isActiveCorporation(eLoopCorporation))
			continue;
		for (int i = 0; i < GC.getInfo(eLoopCorporation).getNumPrereqBonuses(); i++)
		{
			if (GC.getInfo(eLoopCorporation).getPrereqBonus(i) == eBonus &&
				isHasCorporation(eLoopCorporation))
			{
				return true;
			}
		}
	}
	return false;
}

bool CvCity::isActiveCorporation(CorporationTypes eCorporation) const
{
	FAssert(eCorporation >= 0 && eCorporation < GC.getNumCorporationInfos());

	if (!isHasCorporation(eCorporation))
		return false;

	if (!GET_PLAYER(getOwner()).isActiveCorporation(eCorporation))
		return false;

    // doc (edead): corporation spread via Python
    return true;

	/*for (int i = 0; i < GC.getInfo(eCorporation).getNumPrereqBonuses(); i++)
	{
		if (getNumBonuses(GC.getInfo(eCorporation).getPrereqBonus(i)) > 0)
			return true;
	}

	return false;*/
}


void CvCity::setBuildingProduction(BuildingTypes eBuilding, int iNewValue)
{
	if (getBuildingProduction(eBuilding) == iNewValue)
		return;

	m_aiBuildingProduction.set(eBuilding, iNewValue);
	FAssert(getBuildingProduction(eBuilding) >= 0);

	if (isActiveTeam())
		setInfoDirty(true);

	if (isActiveOwned() && isCitySelected())
		gDLL->UI().setDirty(CityScreen_DIRTY_BIT, true);
}


void CvCity::changeBuildingProduction(BuildingTypes eBuilding, int iChange)
{
	setBuildingProduction(eBuilding, getBuildingProduction(eBuilding) + iChange);
}


void CvCity::setBuildingProductionTime(BuildingTypes eBuilding, int iNewValue)
{
	m_aiBuildingProductionTime.set(eBuilding, iNewValue);
	FAssert(getBuildingProductionTime(eBuilding) >= 0);
}


void CvCity::changeBuildingProductionTime(BuildingTypes eBuilding, int iChange)
{
	setBuildingProductionTime(eBuilding, getBuildingProductionTime(eBuilding) + iChange);
}


void CvCity::setProjectProduction(ProjectTypes eProject, int iNewValue)
{
	if (getProjectProduction(eProject) == iNewValue)
		return;

	m_aiProjectProduction.set(eProject, iNewValue);
	FAssert(getProjectProduction(eProject) >= 0);

	if (isActiveTeam())
		setInfoDirty(true);

	if (isActiveOwned() && isCitySelected())
		gDLL->UI().setDirty(CityScreen_DIRTY_BIT, true);
}


void CvCity::changeProjectProduction(ProjectTypes eProject, int iChange)
{
	setProjectProduction(eProject, getProjectProduction(eProject) + iChange);
}


void CvCity::setUnitProduction(UnitTypes eUnit, int iNewValue)
{
	if (getUnitProduction(eUnit) == iNewValue)
		return;

	m_aiUnitProduction.set(eUnit, iNewValue);
	FAssert(getUnitProduction(eUnit) >= 0);

	if (isActiveTeam())
		setInfoDirty(true);

	if (isActiveOwned() && isCitySelected())
		gDLL->UI().setDirty(CityScreen_DIRTY_BIT, true);
}


void CvCity::changeUnitProduction(UnitTypes eUnit, int iChange)
{
	setUnitProduction(eUnit, getUnitProduction(eUnit) + iChange);
}


// doc: track hurried units
// TODO: refactor
HurryTypes CvCity::getUnitHurry(UnitClassTypes eUnitClass) const
{
    for (std::vector< std::pair < UnitClassTypes, HurryTypes > >::const_iterator it = m_hurriedUnits.begin(); it != m_hurriedUnits.end(); ++it)
    {
        if ((*it).first == eUnitClass)
        {
            return (*it).second;
        }
    }

    return NO_HURRY;
}


// doc: track hurried units
// TODO: refactor
void CvCity::setUnitHurry(UnitClassTypes eUnitClass, HurryTypes eHurry)
{
    if (eHurry == NO_HURRY)
    {
        for (std::vector< std::pair < UnitClassTypes, HurryTypes > >::iterator it = m_hurriedUnits.begin(); it != m_hurriedUnits.end(); ++it)
        {
            if ((*it).first == eUnitClass)
            {
                m_hurriedUnits.erase(it);
                return;
            }
        }
    }

    m_hurriedUnits.push_back(std::make_pair(eUnitClass, eHurry));
}


void CvCity::setUnitProductionTime(UnitTypes eUnit, int iNewValue)
{
	m_aiUnitProductionTime.set(eUnit, iNewValue);
	FAssert(getUnitProductionTime(eUnit) >= 0);
}


void CvCity::changeUnitProductionTime(UnitTypes eUnit, int iChange)
{
	setUnitProductionTime(eUnit, getUnitProductionTime(eUnit) + iChange);
}

// BULL - Production Decay - start
/*	advc.094: Using the preprocessor is less bad than keeping two copies
	of this moderately complex code */
#define IMPLEMENT_BUG_PRODUCTION_DECAY_GETTERS(ORDER, Order, Verb) \
/* Returns true if the given order will decay this turn */ \
bool CvCity::is##Order##ProductionDecay(Order##Types e##Order) const \
{ \
	return (/*isHuman() &&*/ /* advc.094: Not the place to check this */ \
			getProduction##Order() != e##Order && \
			get##Order##Production(e##Order) > 0 && \
			100 * get##Order##ProductionTime(e##Order) >= \
			GC.getDefineINT(CvGlobals::ORDER##_PRODUCTION_DECAY_TIME) * \
			GC.getInfo(GC.getGame().getGameSpeedType()).get##Verb##Percent()); \
} \
\
/*	Returns the amount by which the given order will decay once it reaches the limit. */ \
/*	Ignores whether or not the order will actually decay this turn. */ \
int CvCity::get##Order##ProductionDecay(Order##Types e##Order) const \
{ \
	int const iProduction = get##Order##Production(e##Order); \
	return iProduction - \
			(iProduction * \
			GC.getDefineINT(CvGlobals::ORDER##_PRODUCTION_DECAY_PERCENT)) / 100; \
} \
\
/* Returns the number of turns left before the given order will decay */ \
int CvCity::get##Order##ProductionDecayTurns(Order##Types e##Order) const \
{ \
	return 1 + std::max(0, \
			intdiv::uceil( \
			GC.getDefineINT(CvGlobals::ORDER##_PRODUCTION_DECAY_TIME) * \
			GC.getInfo(GC.getGame().getGameSpeedType()).get##Verb##Percent(), \
			100) \
			- get##Order##ProductionTime(e##Order)); \
}
IMPLEMENT_BUG_PRODUCTION_DECAY_GETTERS(BUILDING, Building, Construct)
IMPLEMENT_BUG_PRODUCTION_DECAY_GETTERS(UNIT, Unit, Train)
// BULL - Production Decay - end

// advc.opt: Taking advantage of EnumMap.hasContent
bool CvCity::isAnyProductionProgress(OrderTypes eOrder) const
{
	switch(eOrder)
	{
	case ORDER_CONSTRUCT: return m_aiBuildingProduction.isAnyNonDefault();
	case ORDER_CREATE:	return m_aiProjectProduction.isAnyNonDefault();
	case ORDER_MAINTAIN: return false; // Can't make progress on a process
	case ORDER_TRAIN: return m_aiUnitProduction.isAnyNonDefault();
	default: FErrorMsg("Unknown type of production order");
		return false;
	}
}


void CvCity::setGreatPeopleUnitRate(UnitTypes eUnit, int iNewValue)
{
	if (GC.getGame().isOption(GAMEOPTION_NO_ESPIONAGE) &&
		GC.getInfo(eUnit).getEspionagePoints() > 0)
	{
		return;
	}
	m_aiGreatPeopleUnitRate.set(eUnit, iNewValue);
	FAssert(getGreatPeopleUnitRate(eUnit) >= 0);
}


void CvCity::changeGreatPeopleUnitRate(UnitTypes eUnit, int iChange)
{
	setGreatPeopleUnitRate(eUnit, getGreatPeopleUnitRate(eUnit) + iChange);
}


void CvCity::setGreatPeopleUnitProgress(UnitTypes eUnit, int iNewValue)
{
	m_aiGreatPeopleUnitProgress.set(eUnit, iNewValue);
	FAssert(getGreatPeopleUnitProgress(eUnit) >= 0);
}


void CvCity::changeGreatPeopleUnitProgress(UnitTypes eUnit, int iChange)
{
	setGreatPeopleUnitProgress(eUnit, getGreatPeopleUnitProgress(eUnit) + iChange);
}


void CvCity::setSpecialistCount(SpecialistTypes eSpecialist, int iNewValue)
{
	int const iOldValue = getSpecialistCount(eSpecialist);
	if (iOldValue == iNewValue)
		return;

	m_aiSpecialistCount.set(eSpecialist, iNewValue);
	FAssert(getSpecialistCount(eSpecialist) >= 0);

	changeSpecialistPopulation(iNewValue - iOldValue);
	processSpecialist(eSpecialist, (iNewValue - iOldValue));

	if (isCitySelected())
		gDLL->UI().setDirty(CitizenButtons_DIRTY_BIT, true);
}


void CvCity::changeSpecialistCount(SpecialistTypes eSpecialist, int iChange)
{
	setSpecialistCount(eSpecialist, getSpecialistCount(eSpecialist) + iChange);
}


void CvCity::alterSpecialistCount(SpecialistTypes eSpecialist, int iChange)
{
	if(iChange == 0)
		return;

	if (isCitizensAutomated())
	{
		if (getForceSpecialistCount(eSpecialist) + iChange < 0)
			setCitizensAutomated(false);
	}

	if (isCitizensAutomated())
	{
		changeForceSpecialistCount(eSpecialist, iChange +
		/*	<advc.121> We're making sure below not to remove the specialist
			we've just added, but afterwards we let the AI juggle the citizens;
			so it can still happen that a human adds e.g. a 2nd scientist
			- the 1st having been assigned by the AI - and ends up with just
			1 scientist. Let's assume that any previously assigned specialists
			of type eSpecialist should also be forced. */
				(iChange <= 0 ? 0 :
				std::max(getSpecialistCount(eSpecialist)
				- getForceSpecialistCount(eSpecialist), 0))); // </advc.121>
		//return;
		/*	(K-Mod. Without the following block,
			extra care is needed inside AI_assignWorkingPlots.) */
	}
	if (iChange > 0)
	{
		for (int i = 0; i < iChange; i++)
		{
			if (extraPopulation() > 0 || AI().AI_removeWorstCitizen(eSpecialist))
			{
				if (isSpecialistValid(eSpecialist, 1))
					changeSpecialistCount(eSpecialist, 1);
			}
		}
	}
	else
	{
		for (int i = 0; i < -iChange; i++)
		{
			if (getSpecialistCount(eSpecialist) <= 0)
				continue;

			changeSpecialistCount(eSpecialist, -1);

			if (eSpecialist != GC.getDEFAULT_SPECIALIST() &&
				GC.getDEFAULT_SPECIALIST() != NO_SPECIALIST)
			{
				changeSpecialistCount(GC.getDEFAULT_SPECIALIST(), 1);
				continue;
			}
			if (extraFreeSpecialists() > 0)
			{
				AI().AI_addBestCitizen(false, true);
				continue;
			}
			int iNumCanWorkPlots = 0;
			for (CityPlotIter it(*this, false); it.hasNext(); ++it)
			{
				if (!isWorkingPlot(it.currID()) && canWork(*it))
					iNumCanWorkPlots++;
			}
			if (iNumCanWorkPlots > 0)
				AI().AI_addBestCitizen(true, false);
			else AI().AI_addBestCitizen(false, true);
		}
	}
}


// TODO: refctor
int CvCity::getMaxSpecialistCount(SpecialistTypes eSpecialist, bool bIgnoreCivic) const
{
	int iMaxSpecialistCount = m_aiMaxSpecialistCount.get(eSpecialist);

    // doc: specialist valid doubles slot instead of unlimited
    if (!bIgnoreCivic && GET_PLAYER(getOwner()).isSpecialistValid(eSpecialist))
        iMaxSpecialistCount *= 2;

    // doc: Korean UP: double specialist slots in capital
    if (getCivilizationType() == KOREA && isCapital())
        iMaxSpecialistCount *= 2;

    // doc: civic extra specialist slots
    if (!bIgnoreCivic)
        iMaxSpecialistCount += GET_PLAYER(getOwner()).getSpecialistExtraCount(eSpecialist);

    return iMaxSpecialistCount;
}


bool CvCity::isSpecialistValid(SpecialistTypes eSpecialist, int iExtra) const
{
	return (getSpecialistCount(eSpecialist) + iExtra <= getMaxSpecialistCount(eSpecialist) ||
		GET_PLAYER(getOwner()).isSpecialistValid(eSpecialist) ||
		eSpecialist == GC.getDEFAULT_SPECIALIST());
}


void CvCity::changeMaxSpecialistCount(SpecialistTypes eSpecialist, int iChange)
{
	if (iChange != 0)
	{
		//m_aiMaxSpecialistCount.set(eSpecialist, std::max(0, m_aiMaxSpecialistCount.get(eSpecialist) + iChange));
		// <advc>
		m_aiMaxSpecialistCount.add(eSpecialist, iChange);
		FAssert(m_aiMaxSpecialistCount.get(eSpecialist) >= 0); // </advc>
		AI_setAssignWorkDirty(true);
	}
}


void CvCity::setForceSpecialistCount(SpecialistTypes eSpecialist, int iNewValue)
{
	if (getForceSpecialistCount(eSpecialist) == iNewValue)
		return;

	//m_aiForceSpecialistCount.set(eSpecialist, std::max(0, iNewValue));
	// <advc>
	FAssert(iNewValue >= 0);
	m_aiForceSpecialistCount.set(eSpecialist, iNewValue); // </advc>

	if (isCitySelected())
		gDLL->UI().setDirty(Help_DIRTY_BIT, true);
	AI_setAssignWorkDirty(true);
}


void CvCity::changeForceSpecialistCount(SpecialistTypes eSpecialist, int iChange)
{
	setForceSpecialistCount(eSpecialist, getForceSpecialistCount(eSpecialist) + iChange);
}


// doc
// TODO: refactor
int CvCity::countNoGlobalEffectsFreeSpecialists() const
{
    int iCount = 0;
    for (int iI = 0; iI < GC.getNumSpecialistInfos(); iI++)
    {
        if (GC.getSpecialistInfo((SpecialistTypes)iI).isNoGlobalEffects())
        {
            iCount += getFreeSpecialistCount((SpecialistTypes)iI);
        }
    }

    return iCount;
}

int CvCity::getAddedFreeSpecialistCount(SpecialistTypes eSpecialist) const
{
	int iR = getFreeSpecialistCount(eSpecialist);
	CvCivilization const& kCiv = getCivilization();
	for (int i = 0; i < kCiv.getNumBuildings(); i++)
	{
		BuildingTypes eBuilding = kCiv.buildingAt(i);
		int iFreeSpecialists = GC.getInfo(eBuilding).getFreeSpecialistCount(eSpecialist);
		if (iFreeSpecialists > 0)
			iR -= getNumActiveBuilding(eBuilding) * iFreeSpecialists;
	}
	FAssert(iR >= 0);
	return std::max(0, iR);
}


void CvCity::setFreeSpecialistCount(SpecialistTypes eSpecialist, int iNewValue)
{
	int const iOldValue = getFreeSpecialistCount(eSpecialist);
	if (iOldValue == iNewValue)
		return;

	m_aiFreeSpecialistCount.set(eSpecialist, iNewValue);
	FAssert(getFreeSpecialistCount(eSpecialist) >= 0);

	changeNumGreatPeople(iNewValue - iOldValue);
	processSpecialist(eSpecialist, iNewValue - iOldValue);

	if (isCitySelected())
		gDLL->UI().setDirty(CitizenButtons_DIRTY_BIT, true);
}


void CvCity::changeFreeSpecialistCount(SpecialistTypes eSpecialist, int iChange)
{
	setFreeSpecialistCount(eSpecialist, getFreeSpecialistCount(eSpecialist) + iChange);
}


void CvCity::changeImprovementFreeSpecialists(ImprovementTypes eImprov, int iChange)
{
	//m_aiImprovementFreeSpecialists.set(eImprov, std::max(0, m_aiImprovementFreeSpecialists.get(eImprov) + iChange));
	// <advc>
	m_aiImprovementFreeSpecialists.add(eImprov, iChange);
	FAssert(m_aiImprovementFreeSpecialists.get(eImprov) >= 0); // </advc>
}


void CvCity::changeReligionInfluence(ReligionTypes eReligion, int iChange)
{
	setReligionInfluence(eReligion, getReligionInfluence(eReligion) + iChange);
}

// TODO: replace change as source of truth
void CvCity::setReligionInfluence(ReligionTypes eReligion, int iNewValue)
{
    int iOldValue = getReligionInfluence(eReligion);

    if (iOldValue != iNewValue)
    {
		m_aiReligionInfluence.set(eReligion, iNewValue);

        int iExtraRange = GC.getInfo(eReligion).isProselytizing() ? 3 : 0;

        spreadReligionInfluence(eReligion, iOldValue + iExtraRange, -1);
        spreadReligionInfluence(eReligion, iNewValue + iExtraRange, 1);
    }
}


int CvCity::getCurrentStateReligionHappiness() const
{
	if (GET_PLAYER(getOwner()).getStateReligion() != NO_RELIGION)
		return getStateReligionHappiness(GET_PLAYER(getOwner()).getStateReligion());
	return 0;
}


void CvCity::changeStateReligionHappiness(ReligionTypes eReligion, int iChange)
{
	if (iChange != 0)
	{
		m_aiStateReligionHappiness.add(eReligion, iChange);
		AI_setAssignWorkDirty(true);
	}
}


void CvCity::changeUnitCombatFreeExperience(UnitCombatTypes eUnitCombat, int iChange)
{
	m_aiUnitCombatFreeExperience.add(eUnitCombat, iChange);
	FAssert(getUnitCombatFreeExperience(eUnitCombat) >= 0);
}


void CvCity::changeFreePromotionCount(PromotionTypes ePromo, int iChange)
{
	m_aiFreePromotionCount.add(ePromo, iChange);
	FAssert(getFreePromotionCount(ePromo) >= 0);
}


void CvCity::changeSpecialistFreeExperience(int iChange)
{
	m_iSpecialistFreeExperience += iChange;
	FAssert(m_iSpecialistFreeExperience >= 0);
}


void CvCity::changeEspionageDefenseModifier(int iChange)
{
	m_iEspionageDefenseModifier += iChange;
}

// advc:
int CvCity::cultureTimes100InsertedByMission(EspionageMissionTypes eMission) const
{
	int iCultureAmount = GC.getInfo(eMission).getCityInsertCultureAmountFactor() *
			countTotalCultureTimes100();
	iCultureAmount /= 100;
	return std::max(100, iCultureAmount);
}


bool CvCity::isWorkingPlot(CvPlot const& kPlot) const
{
	// advc.enum: Use CityPlotTypes instead of int
	CityPlotTypes eIndex = getCityPlotIndex(kPlot);
	if (eIndex != NO_CITYPLOT)
		return isWorkingPlot(eIndex);
	return false;
}


void CvCity::setWorkingPlot(CityPlotTypes ePlot, bool bNewValue) // advc.enum: CityPlotTypes
{
	if (isWorkingPlot(ePlot) == bNewValue)
		return;
	// <advc.064b> To avoid unnecessary update of city screen
	bool bSelected = isCitySelected();
	int iOldTurns = -1;
	if(bSelected && GET_PLAYER(getOwner()).canGoldRush())
		iOldTurns = getProductionTurnsLeft();
	// </advc.064b>
	m_abWorkingPlot.set(ePlot, bNewValue);

	CvPlot* pPlot = getCityIndexPlot(ePlot);
	if (pPlot != NULL)
	{
		FAssertMsg(pPlot->getWorkingCity() == this, "WorkingCity is expected to be this");

		if (isWorkingPlot(ePlot))
		{
			if (ePlot != CITY_HOME_PLOT)
				changeWorkingPopulation(1);
			FOR_EACH_ENUM(Yield)
				changeBaseYieldRate(eLoopYield, pPlot->getYield(eLoopYield));
			// update plot builder special case where a plot is being worked but is (a) unimproved  or (b) un-bonus'ed
			pPlot->updatePlotBuilder();
		}
		else
		{
			if (ePlot != CITY_HOME_PLOT)
				changeWorkingPopulation(-1);
			FOR_EACH_ENUM(Yield)
				changeBaseYieldRate(eLoopYield, -pPlot->getYield(eLoopYield));
		}

		if (isActiveTeam() || GC.getGame().isDebugMode())
			pPlot->updateSymbolDisplay();
	}
	if (bSelected)
	{
		gDLL->UI().setDirty(InfoPane_DIRTY_BIT, true);
		gDLL->UI().setDirty(CityScreen_DIRTY_BIT, true);
		gDLL->UI().setDirty(ColoredPlots_DIRTY_BIT, true);
		// <advc.064b>
		if(iOldTurns >= 0 && getProductionTurnsLeft() != iOldTurns)
			gDLL->UI().setDirty(SelectionButtons_DIRTY_BIT, true);
		// </advc.064b>
	}

}


void CvCity::setWorkingPlot(CvPlot& kPlot, bool bNewValue)
{
	setWorkingPlot(getCityPlotIndex(kPlot), bNewValue);
}


void CvCity::alterWorkingPlot(CityPlotTypes ePlot)
{
	if (ePlot == CITY_HOME_PLOT)
	{
		setCitizensAutomated(true);
		return;
	}
	CvPlot* pPlot = getCityIndexPlot(ePlot);
	if (pPlot == NULL)
		return;
	if (!canWork(*pPlot))
	{
		if (pPlot->getOwner() == getOwner())
			pPlot->setWorkingCityOverride(this);
		return;
	}

	setCitizensAutomated(false);
	if (isWorkingPlot(ePlot))
	{
		setWorkingPlot(ePlot, false);
		if (GC.getDEFAULT_SPECIALIST() != NO_SPECIALIST)
			changeSpecialistCount(GC.getDEFAULT_SPECIALIST(), 1);
		else AI().AI_addBestCitizen(false, true);
	}
	else if (extraPopulation() > 0 || AI().AI_removeWorstCitizen())
		setWorkingPlot(ePlot, true);
}

// advc.003w:
int CvCity::getNumRealBuilding(BuildingClassTypes eBuildingClass) const
{
	BuildingTypes eBuilding = getCivilization().getBuilding(eBuildingClass);
	if (eBuilding == NO_BUILDING)
		return 0;
	return getNumRealBuilding(eBuilding);
}


void CvCity::setNumRealBuilding(BuildingTypes eBuilding, int iNewValue,
	bool bEndOfTurn) // advc.001x
{
	setNumRealBuildingTimed(eBuilding, iNewValue, true, getCivilizationType(),
			GC.getGame().getGameTurnYear(), /* advc.001x: */ bEndOfTurn);
}


void CvCity::setNumRealBuildingTimed(BuildingTypes eBuilding, int iNewValue, bool bFirst,
	CivilizationTypes eOriginalOwner, int iOriginalTime, /* advc.001x: */ bool bEndOfTurn)
{

	int const iChange = iNewValue - getNumRealBuilding(eBuilding);
	if(iChange == 0)
		return;

	int const iOldNumBuilding = getNumBuilding(eBuilding);
	m_aiNumRealBuilding.set(eBuilding, iNewValue);
	if (getNumRealBuilding(eBuilding) > 0)
	{
		m_aeBuildingOriginalOwner.set(eBuilding, eOriginalOwner);
		m_aiBuildingOriginalTime.set(eBuilding, iOriginalTime);
	}
	else
	{
		m_aeBuildingOriginalOwner.set(eBuilding, NO_CIVILIZATION);
		m_aiBuildingOriginalTime.set(eBuilding, iBuildingOriginalTimeUnknown);
	}
	CvBuildingInfo const& kBuilding = GC.getInfo(eBuilding);
	if (iOldNumBuilding != getNumBuilding(eBuilding))
	{
		if (getNumRealBuilding(eBuilding) > 0 && kBuilding.isStateReligion())
		{
			FOR_EACH_ENUM(VoteSource)
			{
				if (kBuilding.getVoteSourceType() == eLoopVoteSource &&
					GC.getGame().getVoteSourceReligion(eLoopVoteSource) == NO_RELIGION)
				{
					FAssert(GET_PLAYER(getOwner()).getStateReligion() != NO_RELIGION);
					GC.getGame().setVoteSourceReligion(eLoopVoteSource,
							GET_PLAYER(getOwner()).getStateReligion(), true);
				}
			}
		}
		// advc (note): Not the same as iChange, which only counts NumRealBuilding.
		processBuilding(eBuilding, getNumBuilding(eBuilding) - iOldNumBuilding);
	}
	if (!GC.getInfo(kBuilding.getBuildingClassType()).isNoLimit())
	{
		if (kBuilding.isWorldWonder())
			changeNumWorldWonders(iChange);
		else if (kBuilding.isTeamWonder())
			changeNumTeamWonders(iChange);
		else if (kBuilding.isNationalWonder())
			changeNumNationalWonders(iChange);
		else changeNumBuildings(iChange);
	}
	if (iChange > 0 && bFirst)
	{
		if (kBuilding.isCapital())
			GET_PLAYER(getOwner()).setCapital(this);

		if (GC.getGame().isFinalInitialized() && !gDLL->GetWorldBuilderMode())
		{
			CvWString szBuffer;
			CvPlayer& kOwner = GET_PLAYER(getOwner());

			if (kBuilding.isGoldenAge())
			{
				//kOwner.changeGoldenAgeTurns(iChange * (kOwner.getGoldenAgeLength() + 1));
				// <advc.001x>
				if (bEndOfTurn && !kOwner.isAnarchy()) // doc: golden age turns do not decrease during anarchy
				{
					for (int i = 0; i < iChange; i++)
						kOwner.startGoldenAgeDelayed();
				}
				else kOwner.changeGoldenAgeTurns(iChange * kOwner.getGoldenAgeLength());
                // </advc.001x>
			}
			if (kBuilding.getGlobalPopulationChange() != 0)
			{
				for (MemberAIIter it(getTeam()); it.hasNext(); ++it)
				{
					CvPlayerAI const& kMember = *it;
					if (kMember.getID() != getOwner() && !kBuilding.isTeamShare())
						continue;
					FOR_EACH_CITYAI_VAR(pLoopCity, kMember)
					{
						pLoopCity->setPopulation(std::max(1, pLoopCity->getPopulation() +
								iChange * kBuilding.getGlobalPopulationChange()));
						// so that subsequent cities don't starve with the extra citizen working nothing
						pLoopCity->AI_updateAssignWork();
					}
				}
			}
			FOR_EACH_NON_DEFAULT_PAIR(kBuilding.
				getReligionChange(), Religion, int)
			{
				if (perReligionVal.second > 0)
					setHasReligion(perReligionVal.first, true, true, true);
			}
			int const iFreeTechs = kBuilding.getFreeTechs() * iChange; // advc
			if (iFreeTechs > 0)
			{
				if (!isHuman())
				{
					for (int i = 0; i < iFreeTechs; i++)
						GET_PLAYER(getOwner()).AI_chooseFreeTech();
				}
				else
				{
					szBuffer = gDLL->getText(  // <advc.008e>
							kBuilding.nameNeedsArticle() ?
							"TXT_KEY_MISC_COMPLETED_WONDER_CHOOSE_TECH_THE" :
							"TXT_KEY_MISC_COMPLETED_WONDER_CHOOSE_TECH", // </advc.008e>
							kBuilding.getTextKeyWide());
					GET_PLAYER(getOwner()).chooseTech(iFreeTechs, szBuffer.GetCString());
				}
			}
			if (kBuilding.isWorldWonder())
			{
				szBuffer = gDLL->getText(  // <advc.008e>
						kBuilding.nameNeedsArticle() ?
						"TXT_KEY_MISC_COMPLETES_WONDER_THE" :
						"TXT_KEY_MISC_COMPLETES_WONDER", // </advc.008e>
						GET_PLAYER(getOwner()).getNameKey(), kBuilding.getTextKeyWide());
				GC.getGame().addReplayMessage(getPlot(), REPLAY_MESSAGE_MAJOR_EVENT,
						getOwner(), szBuffer, GC.getColorType("BUILDING_TEXT"));
				// <advc.106>
				for (PlayerIter<MAJOR_CIV> it; it.hasNext(); ++it)
				{
					CvPlayer& kObs = *it;
					bool const bRevealed = isRevealed(kObs.getTeam(), true);
					bool const bMet = GET_TEAM(kObs.getID()).isHasMet(getTeam());
					if (bRevealed /* advc.127: */ || kObs.isSpectator())
					{	// <advc.008e>
						szBuffer = gDLL->getText(kBuilding.nameNeedsArticle() ?
								"TXT_KEY_MISC_WONDER_COMPLETED_CITY_THE" :
								"TXT_KEY_MISC_WONDER_COMPLETED_CITY", // </advc.008e>
								GET_PLAYER(getOwner()).getCivilizationShortDescription(), // rfc
								kBuilding.getTextKeyWide(), getName().GetCString());
					}
					else if (bMet)
					{	// <advc.008e>
						szBuffer = gDLL->getText(kBuilding.nameNeedsArticle() ?
								"TXT_KEY_MISC_WONDER_COMPLETED_THE" :
								"TXT_KEY_MISC_WONDER_COMPLETED", // </advc.008e>
								GET_PLAYER(getOwner()).getCivilizationShortDescription(), // rfc
								kBuilding.getTextKeyWide());
					}
					else // <advc.008>
					{
						szBuffer = gDLL->getText(kBuilding.nameNeedsArticle() ?
								"TXT_KEY_MISC_WONDER_COMPLETED_UNKNOWN_THE" :
								"TXT_KEY_MISC_WONDER_COMPLETED_UNKNOWN",
								kBuilding.getTextKeyWide());
					}
					gDLL->UI().addMessage(kObs.getID(), false,
							-1, szBuffer, "AS2D_WONDER_BUILDING_BUILD",
							MESSAGE_TYPE_MAJOR_EVENT_LOG_ONLY, // advc.106b
							kBuilding.getArtInfo()->getButton(),
							GC.getColorType("BUILDING_TEXT"),
							// Indicate location only if revealed.
							bRevealed ? getX() : -1, bRevealed ? getY() : -1,
							bRevealed, bRevealed);
				} // </advc.106>
			}
		}
		if (kBuilding.isAllowsNukes())
			GC.getGame().makeNukesValid(true);

		GC.getGame().incrementBuildingClassCreatedCount(kBuilding.getBuildingClassType());
		/*  advc: Increments greater than 1 aren't supported. As for decrements:
			a building that gets destroyed has nevertheless been created ...
			That said, removing and recreating world wonders through WB will
			lead to failed assertions in CvGame::isBuildingClassMaxedOut. */
		FAssert(iChange == 1);
	}

	if (bFirst) //great wall
	{
		if (kBuilding.isAreaBorderObstacle() ||
		/*  advc.310: Show GW as 3D model even when playing w/o Barbarians
			(BorderObstacle ability disabled through CvBuildingInfo then). */
			kBuilding.getAreaTradeRoutes() > 0)
		{
			int iCountExisting = 0;
			CvCivilization const& kCiv = getCivilization();
			for (int i = 0; i < kCiv.getNumBuildings(); i++)
			{
				BuildingTypes eLoopBuilding = kCiv.buildingAt(i);
				if (eBuilding != eLoopBuilding &&
					GC.getInfo(eLoopBuilding).isAreaBorderObstacle())
				{
					iCountExisting += getNumRealBuilding(eLoopBuilding);
				}
			}
			//if (iCountExisting == 1 && iNewValue == 0)
			/*  advc.001: m_aiNumRealBuilding.get(eBuilding) has already been decreased
				(and the loop above skips eBuilding anyway), so iCountExisting isn't
				going to be 1. */
			if (iCountExisting <= 0 && iOldNumBuilding > 0 && iNewValue <= 0)
				gDLL->getEngineIFace()->RemoveGreatWall(this);
			else if (iCountExisting == 0 && iNewValue > 0)
			{
				//gDLL->getEngineIFace()->AddGreatWall(this);
				addGreatWall(); // advc.310
			}
		}
	}
}

// doc
bool CvCity::isHasBuildingEffect(BuildingTypes eBuilding) const
{
    return isHasRealBuilding(eBuilding) && GET_PLAYER(getOwner()).isHasBuildingEffect(eBuilding);
}

// rfc
bool CvCity::isHasRealBuilding(BuildingTypes eIndex) const
{
    return getNumRealBuilding(eIndex) > 0;
}

// rfc
void CvCity::setHasRealBuilding(BuildingTypes eIndex, bool bNewValue)
{
    setNumRealBuilding(eIndex, bNewValue ? 1 : 0);
}


void CvCity::setNumFreeBuilding(BuildingTypes eBuilding, int iNewValue)
{
	if(getNumFreeBuilding(eBuilding) == iNewValue)
		return;

	int const iOldNumBuilding = getNumBuilding(eBuilding);
	m_aiNumFreeBuilding.set(eBuilding, iNewValue);
	if (iOldNumBuilding != getNumBuilding(eBuilding))
		processBuilding(eBuilding, iNewValue - iOldNumBuilding);
}


void CvCity::setHasReligion(ReligionTypes eReligion, bool bNewValue, bool bAnnounce, bool bArrows,
	PlayerTypes eSpreadPlayer) // advc.106e
{
	if (isHasReligion(eReligion) == bNewValue)
		return;

	FOR_EACH_ENUM(VoteSource)
		processVoteSource(eLoopVoteSource, false);
	// <advc.130n>
	for (PlayerAIIter<MAJOR_CIV> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		if (isRevealed(itPlayer->getTeam()))
			itPlayer->AI_updateIdeologyAttitude(-1, *this);
	} // </advc.130n>
	m_abHasReligion.set(eReligion, bNewValue);
	// <advc.130n>
    // doc: religion spread via influence
    // TODO: refactor
    int iReligionInfluenceChange = GC.getDefineINT("RELIGION_PRESENCE_INFLUENCE");
    changeReligionInfluence(eReligion, bNewValue ? iReligionInfluenceChange : -iReligionInfluenceChange);
	for (PlayerAIIter<MAJOR_CIV> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		if (isRevealed(itPlayer->getTeam()))
			itPlayer->AI_updateIdeologyAttitude(1, *this);
	} // </advc.130n>
	FOR_EACH_ENUM(VoteSource)
		processVoteSource(eLoopVoteSource, true);

	CvPlayerAI& kOwner = GET_PLAYER(getOwner());
	kOwner.changeHasReligionCount(eReligion, isHasReligion(eReligion) ? 1 : -1);
	updateMaintenance();
	updateReligionHappiness();
	updateReligionCommerce();

	AI_setAssignWorkDirty(true);
	setInfoDirty(true);
	// <advc.106e>
	int const iOwnerEra = kOwner.getCurrentEra();
	int const iEraThresh = GC.getDefineINT("STOP_RELIGION_SPREAD_ANNOUNCE_ERA");
	bool const bAnnounceStateReligionSpread = (GC.getDefineINT(
			"ANNOUNCE_STATE_RELIGION_SPREAD") > 0);
	// </advc.106e>
	if (isHasReligion(eReligion))
	{
		CvGame& kGame = GC.getGame();
		kGame.makeReligionFounded(eReligion, kOwner.getID());
		if (bAnnounce)
		{
			if (kGame.getHolyCity(eReligion) != this)
			{
				for (PlayerIter<MAJOR_CIV> it; it.hasNext(); ++it)
				{
					CvPlayer const& kObs = *it;
					if (!isRevealed(kObs.getTeam()))
						continue;
					// <advc.106e>
					if ((iOwnerEra < iEraThresh && (bAnnounceStateReligionSpread ||
						kOwner.getStateReligion() != eReligion)) ||
						eSpreadPlayer == kObs.getID() || // </advc.106e>
						kOwner.getID() == kObs.getID() ||
						// advc.106e: Disable this clause
						//(kObs.getStateReligion() == eReligion) ||
						kObs.hasHolyCity(eReligion))
					{
						CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_RELIGION_SPREAD",
								GC.getInfo(eReligion).getTextKeyWide(), getNameKey());
						gDLL->UI().addMessage(kObs.getID(), false,
								-1, // (K-Mod note: event time was originally "long".)
								szBuffer, GC.getInfo(eReligion).getSound(),
								MESSAGE_TYPE_MINOR_EVENT, // advc.106b: was MAJOR
								GC.getInfo(eReligion).getButton(), NO_COLOR,
								getX(), getY(), bArrows, bArrows);
					}
				}
			}
			if (isHuman() && kOwner.getHasReligionCount(eReligion) == 1)
			{
				if (kOwner.canConvert(eReligion) && kOwner.getStateReligion() == NO_RELIGION)
				{
					CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_CHANGERELIGION);
					pInfo->setData1(eReligion);
					gDLL->UI().addPopup(pInfo, kOwner.getID());
				}
				/*	<advc.004w> Update text of resource indicators
					(CvGameTextMgr::setBonusExtraHelp) */
				if (isActiveOwned() && kGame.getCurrentLayer() == GLOBE_LAYER_RESOURCE)
				{
					gDLL->UI().setDirty(GlobeLayer_DIRTY_BIT, true);
					// advc.003p:
					kOwner.setBonusHelpDirty();
				} // </advc.004w>
			}
		}
	} // K-Mod start
	else // religion removed
	{
		if (bAnnounce)
		{	// <advc.106e> Announce removed religion to other civs as well
			for (PlayerIter<MAJOR_CIV> it; it.hasNext(); ++it)
			{
				CvPlayer const& kObs = *it;
				if (!isRevealed(kObs.getTeam()))
					continue;
				if (eSpreadPlayer != kObs.getID() && iOwnerEra >= iEraThresh &&
					kOwner.getID() != kObs.getID() && !kObs.hasHolyCity(eReligion))
				{
					continue;
				} // </advc.106e>
				CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_RELIGION_REMOVE",
						GC.getInfo(eReligion).getTextKeyWide(), getNameKey());
				gDLL->UI().addMessage(
						kObs.getID(), // advc.106e: was getOwner() in K-Mod
						false, -1, szBuffer, "AS2D_BLIGHT",
						MESSAGE_TYPE_MINOR_EVENT, // advc.106b: was MAJOR
						GC.getInfo(eReligion).getButton(), GC.getColorType("RED"),
						getX(), getY(), bArrows, bArrows);
			}
		}
	} // K-Mod end
	if (bNewValue)
		CvEventReporter::getInstance().religionSpread(eReligion, kOwner.getID(), this);
	else CvEventReporter::getInstance().religionRemove(eReligion, kOwner.getID(), this);
}

// K-Mod: A rating for how strong a religion can take hold in this city
int CvCity::getReligionGrip(ReligionTypes eReligion) const
{
	PROFILE_FUNC();
	if (!GC.getGame().isReligionFounded(eReligion))
		return 0;
	// <advc.opt>
	static int const iRELIGION_INFLUENCE_POPULATION_WEIGHT = GC.getDefineINT("RELIGION_INFLUENCE_POPULATION_WEIGHT");
	static int const iRELIGION_INFLUENCE_STATE_RELIGION_WEIGHT = GC.getDefineINT("RELIGION_INFLUENCE_STATE_RELIGION_WEIGHT");
	static int const iRELIGION_INFLUENCE_BUILDING_WEIGHT = GC.getDefineINT("RELIGION_INFLUENCE_BUILDING_WEIGHT");
	static int const iRELIGION_INFLUENCE_SHRINE_WEIGHT = GC.getDefineINT("RELIGION_INFLUENCE_SHRINE_WEIGHT");
	static int const iRELIGION_INFLUENCE_DISTANCE_WEIGHT = GC.getDefineINT("RELIGION_INFLUENCE_DISTANCE_WEIGHT");
	static int const iRELIGION_INFLUENCE_TIME_SCALE = GC.getDefineINT("RELIGION_INFLUENCE_TIME_SCALE");
	static int const iRELIGION_INFLUENCE_TIME_WEIGHT = GC.getDefineINT("RELIGION_INFLUENCE_TIME_WEIGHT");
	// </advc.opt>
	int iScore = 0;

	if (isHasReligion(eReligion))
	{
		int iTempScore = iRELIGION_INFLUENCE_POPULATION_WEIGHT * getPopulation();
		// <advc.099c> Try to satisfy foreign pop
		if (revoltProbability(true, false, true) > 0)
		{
			PlayerTypes cultOwner = calculateCulturalOwner();
			if(GET_PLAYER(cultOwner).getStateReligion() == eReligion)
				iTempScore *= 2;
		}
		iScore += iTempScore; // </advc.099c>
		if (GET_PLAYER(getOwner()).getStateReligion() == eReligion)
			iScore += iRELIGION_INFLUENCE_STATE_RELIGION_WEIGHT;
	}

	CvCivilization const& kCiv = getCivilization();
	for (int i = 0; i < kCiv.getNumBuildings(); i++)
	{
		BuildingTypes eBuilding = kCiv.buildingAt(i);
		if (GC.getInfo(eBuilding).getPrereqReligion() == eReligion)
		{
			iScore += iRELIGION_INFLUENCE_BUILDING_WEIGHT *
					getNumActiveBuilding(eBuilding);
		}
	}

	CvCity* pHolyCity = GC.getGame().getHolyCity(eReligion);
	if (pHolyCity && isConnectedTo(*pHolyCity))
	{
		if (pHolyCity->hasShrine(eReligion))
			iScore += iRELIGION_INFLUENCE_SHRINE_WEIGHT;

		int iDistance = plotDistance(getX(), getY(), pHolyCity->getX(), pHolyCity->getY());
		iScore += iRELIGION_INFLUENCE_DISTANCE_WEIGHT *
				// <advc.140> was maxPlotDistance
				(GC.getMap().maxTypicalDistance() - iDistance) /
				GC.getMap().maxTypicalDistance(); // </advc.140>
	}

	int iCurrentTurn = GC.getGame().getGameTurn();
	int iTurnFounded = GC.getGame().getReligionGameTurnFounded(eReligion);
	int iTimeScale = iRELIGION_INFLUENCE_TIME_SCALE * GC.getInfo(GC.getGame().
			getGameSpeedType()).getVictoryDelayPercent()/100;
	iScore += iRELIGION_INFLUENCE_TIME_WEIGHT * (iTurnFounded + iTimeScale) /
			(iCurrentTurn + iTimeScale);

	return iScore; // note. the random part is not included in this function.
}

// advc: Renamed from "processVoteSourceBonus"
void CvCity::processVoteSource(VoteSourceTypes eVoteSource, bool bActive)
{
	if (!GET_PLAYER(getOwner()).isLoyalMember(eVoteSource))
		return;

	if (!GC.getGame().isDiploVote(eVoteSource))
		return;

	ReligionTypes const eReligion = GC.getGame().getVoteSourceReligion(eVoteSource);
	{
		SpecialistTypes const eSpecialist = GC.getInfo(eVoteSource).getFreeSpecialist();
		if (eSpecialist != NO_SPECIALIST)
		{
			if (eReligion == NO_RELIGION || isHasReligion(eReligion))
				changeFreeSpecialistCount(eSpecialist, bActive ? 1 : -1);
		}
	}
	if (eReligion == NO_RELIGION || !isHasReligion(eReligion))
		return;

	FOR_EACH_ENUM(Yield)
	{
		int iChange = GC.getInfo(eVoteSource).getReligionYield(eLoopYield);
		if (!bActive)
			iChange = -iChange;
		if (iChange != 0)
		{
			FOR_EACH_ENUM(Building)
			{
				if (GC.getInfo(eLoopBuilding).getReligionType() == eReligion)
				{
					changeBuildingYieldChange(CvCivilization::buildingClass(eLoopBuilding),
							eLoopYield, iChange);
				}
			}
		}
	}
	FOR_EACH_ENUM(Commerce)
	{
		int iChange = GC.getInfo(eVoteSource).getReligionCommerce(eLoopCommerce);
		if (!bActive)
			iChange = -iChange;
		if (iChange != 0)
		{
			FOR_EACH_ENUM(Building)
			{
				if (GC.getInfo(eLoopBuilding).getReligionType() == eReligion)
				{
					changeBuildingCommerceChange(CvCivilization::buildingClass(eLoopBuilding),
							eLoopCommerce, iChange);
				}
			}
		}
	}
}


void CvCity::setHasCorporation(CorporationTypes eCorp, bool bNewValue, bool bAnnounce, bool bArrows)
{
	if (isHasCorporation(eCorp) == bNewValue)
		return;

	if (bNewValue)
	{
		bool bReplacedHeadquarters = false;
		FOR_EACH_ENUM(Corporation)
		{
			if (eLoopCorporation != eCorp && isHasCorporation(eLoopCorporation) &&
				GC.getGame().isCompetingCorporation(eLoopCorporation, eCorp))
			{
				if (GC.getGame().getHeadquarters(eLoopCorporation) == this)
				{
					GC.getGame().replaceCorporation(eLoopCorporation, eCorp);
					bReplacedHeadquarters = true;
				}
				else setHasCorporation(eLoopCorporation, false, false);
			}
		}
		if (bReplacedHeadquarters)
			return; // already set the corporation in this city
	}

	m_abHasCorporation.set(eCorp, bNewValue);
	GET_PLAYER(getOwner()).changeHasCorporationCount(eCorp, isHasCorporation(eCorp) ? 1 : -1);

	CvCity* pHeadquarters = GC.getGame().getHeadquarters(eCorp);
	if (pHeadquarters != NULL)
		pHeadquarters->updateCorporation();

	updateCorporation();

	AI_setAssignWorkDirty(true);
	setInfoDirty(true);

	if (isHasCorporation(eCorp))
		GC.getGame().makeCorporationFounded(eCorp, getOwner());

	if (bAnnounce)
	{
		CvCorporationInfo const& kCorp = GC.getInfo(eCorp);
		for (PlayerIter<MAJOR_CIV> it; it.hasNext(); ++it)
		{
			CvPlayer const& kObs = *it;
			// <advc.106e>
			if(kObs.hasHeadquarters(eCorp))
				getPlot().setRevealed(kObs.getTeam(), true, false, NO_TEAM, false);
			//if (getOwner() == kObs.getID() || kObs.hasHeadquarters(eCorp)) // BtS
			if (isRevealed(kObs.getTeam())) // </advc.106e>
			{
				if (getOwner() == kObs.getID())
				{
                    // doc (edead): disable bonus string
					/*CvWStringBuffer szBonusString;
					GAMETEXT.setCorporationHelpCity(szBonusString, eCorp, this);

					CvWString szBonusList;
					bool bFirst = true;
					for (int i = 0; i < kCorp.getNumPrereqBonuses(); i++)
					{
						BonusTypes eBonus = kCorp.getPrereqBonus(i);
						CvWString szTemp;
						szTemp.Format(L"%s", GC.getInfo(eBonus).getDescription());
						setListHelp(szBonusList, L"", szTemp, L", ", bFirst);
					}
					CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_CORPORATION_SPREAD_BONUS",
							kCorp.getTextKeyWide(), szBonusString.getCString(),
							getNameKey(), szBonusList.GetCString());
					gDLL->UI().addMessage(kObs.getID(), false, -1, szBuffer, kCorp.getSound(),
							MESSAGE_TYPE_MINOR_EVENT, kCorp.getButton(),
							NO_COLOR, getX(), getY(), bArrows, bArrows);

					CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_CORPORATION_SPREAD",
							kCorp.getTextKeyWide(), getNameKey());
					gDLL->UI().addMessage(kObs.getID(), false, -1, szBuffer,
							kCorp.getSound(),
							MESSAGE_TYPE_MINOR_EVENT, // advc.106b: was MAJOR
							kCorp.getButton(), NO_COLOR, getX(), getY(), bArrows, bArrows);*/

                    // doc (edead): add removal notification
                    // TODO: refactor
                    if (bNewValue) {
				        CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_CORPORATION_SPREAD", kCorp.getTextKeyWide(), getNameKey());
				        gDLL->getInterfaceIFace()->addMessage(kObs.getID(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, kCorp.getSound(), MESSAGE_TYPE_MAJOR_EVENT, kCorp.getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), getX(), getY(), bArrows, bArrows);
				    }
				    else
				    {
				        CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_CORPORATION_REMOVED", kCorp.getTextKeyWide(), getNameKey());
				        gDLL->getInterfaceIFace()->addMessage(kObs.getID(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, kCorp.getSound(), MESSAGE_TYPE_MAJOR_EVENT, kCorp.getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), getX(), getY(), bArrows, bArrows);
				    }

				} // K-Mod end
			}
		}
	}
	if (bNewValue)
		CvEventReporter::getInstance().corporationSpread(eCorp, getOwner(), this);
	else CvEventReporter::getInstance().corporationRemove(eCorp, getOwner(), this);
}


CvCity* CvCity::getTradeCity(int iIndex) const
{
	FAssertBounds(0, m_aTradeCities.size(), iIndex);
	return getCity(m_aTradeCities[iIndex]);
}


int CvCity::getTradeRoutes() const
{
	/*  <advc.123e> 0 trade routes result in 0 profit from plundering; see
		CvUnit::collectBlockadeGold */
	if(getOwner() == BARBARIAN_PLAYER)
		return 0; // </advc.123e>

	int iTradeRoutes = GC.getGame().getTradeRoutes();
	iTradeRoutes += GET_PLAYER(getOwner()).getTradeRoutes();
	// advc.310: Continental TR no longer included in player TR
	iTradeRoutes += getArea().getTradeRoutes(getOwner());
	if (isCoastal())
		iTradeRoutes += GET_PLAYER(getOwner()).getCoastalTradeRoutes();
    iTradeRoutes += getExtraTradeRoutes();

    // doc: Portuguese UP: +1 trade routes in colonies before the Industrial era
    if (getCivilizationType() == PORTUGAL && isColony() && GET_PLAYER(getOwner()).getCurrentEra() <= ERA_RENAISSANCE)
        iTradeRoutes += 1;

	return std::min(iTradeRoutes, GC.getDefineINT(CvGlobals::MAX_TRADE_ROUTES));
}


void CvCity::clearTradeRoutes()
{
	for (size_t i = 0; i < m_aTradeCities.size(); i++)
	{
		CvCity* pLoopCity = getTradeCity(i);
		if (pLoopCity != NULL)
			pLoopCity->setTradeRoute(getOwner(), false);
		m_aTradeCities[i].reset();
	}
}

// doc
// TODO: refactor
bool CvCity::canHaveTradeRouteWith(const CvCity* pCity) const
{
	if (GC.getDefineINT("IGNORE_PLOT_GROUP_FOR_TRADE_ROUTES"))
		return true;

	return pCity->plotGroup(getOwner()) == plotGroup(getOwner());
}


// XXX eventually, this needs to be done when roads are built/destroyed...
void CvCity::updateTradeRoutes()  // advc: refactored
{
	int const iMaxTradeRoutes = GC.getDefineINT(CvGlobals::MAX_TRADE_ROUTES);
	CvPlayer const& kOwner = GET_PLAYER(getOwner());

	clearTradeRoutes();

	if (!isDisorder() && !isPlundered())
	{
		int iTradeRoutes = getTradeRoutes();
		FAssert(iTradeRoutes <= (int)m_aTradeCities.size()); // advc
		static bool const bIgnorePlotGroups = (GC.getDefineBOOL("IGNORE_PLOT_GROUP_FOR_TRADE_ROUTES")); // advc.opt
		int* aiBestValue = new int[iMaxTradeRoutes](); // value-initialize
		for (PlayerIter<MAJOR_CIV> it; it.hasNext(); ++it)
		{
			CvPlayer const& kPartner = *it;
			if(!kOwner.canHaveTradeRoutesWith(kPartner.getID()))
				continue;

			FOR_EACH_CITY(pLoopCity, kPartner)
			{
				if(pLoopCity == this)
					continue;
				/*  <advc.124> A connection along revealed tiles ensures that the
					city tile is revealed, but not that the city is revealed. */
				if(pLoopCity->isDisorder() || !pLoopCity->isRevealed(getTeam()))
					continue; // <advc.124>
				if(pLoopCity->isTradeRoute(kOwner.getID()) &&
					getTeam() != kPartner.getTeam())
				{
					continue;
				}
				if(!bIgnorePlotGroups &&
					pLoopCity->plotGroup(kOwner.getID()) != plotGroup(kOwner.getID()))
				{
					continue;
				}
				/*	advc: Times 100 so that there are fewer ties (which, currently,
					are broken arbitrarily based on player and city id). */
				int iValue = calculateTradeProfitTimes100(pLoopCity);
				for (int i = 0; i < iTradeRoutes; i++)
				{
					if(iValue <= aiBestValue[i])
						continue;
					for (int j = iTradeRoutes - 1; j > i; j--)
					{
						aiBestValue[j] = aiBestValue[j - 1];
						FAssertBounds(1, m_aTradeCities.size(), j);
						m_aTradeCities[j] = m_aTradeCities[j - 1];
					}
					aiBestValue[i] = iValue;
					m_aTradeCities[i] = pLoopCity->getIDInfo();
					break;
				}
			}
		}
		SAFE_DELETE_ARRAY(aiBestValue);
	}

	int iTradeProfit = 0;
	for (int i = 0; i < iMaxTradeRoutes; i++)
	{
		CvCity* pLoopCity = getTradeCity(i);
		if (pLoopCity != NULL)
		{
			pLoopCity->setTradeRoute(kOwner.getID(), true);
			iTradeProfit += calculateTradeProfit(pLoopCity);
		}
	}
	FOR_EACH_ENUM(Yield)
	{
		// XXX could take this out if handled when CvPlotGroup changes...
		setTradeYield(eLoopYield, calculateTradeYield(eLoopYield, iTradeProfit));
	}
}


void CvCity::clearOrderQueue()
{
	while (headOrderQueueNode() != NULL)
	{
		popOrder(0);
	}
	if (isActiveTeam() || GC.getGame().isDebugMode())
		setInfoDirty(true);
}


void CvCity::pushOrder(OrderTypes eOrder, int iData1, int iData2, bool bSave,
	bool bPop, int iPosition, bool bForce)
{
	OrderData order;
	bool bBuildingUnit = false;
	bool bBuildingBuilding = false;

	if (bPop)
		popOrder(0);

	bool bValid = false;

	switch (eOrder)
	{
	case ORDER_TRAIN:
	{
		UnitTypes const eUnit = (UnitTypes)iData1; // advc
		if (canTrain(eUnit) || bForce)
		{
			if (iData2 == NO_UNITAI)
				iData2 = GC.getInfo(eUnit).getDefaultUnitAIType();
			UnitAITypes const eUnitAI = (UnitAITypes)iData2; // advc
			GET_PLAYER(getOwner()).changeUnitClassMaking(GC.getInfo(eUnit).getUnitClassType(), 1);
			getArea().changeNumTrainAIUnits(getOwner(), eUnitAI, 1);
			GET_PLAYER(getOwner()).AI_changeNumTrainAIUnits(eUnitAI, 1);

			bValid = true;
			bBuildingUnit = true;
			CvEventReporter::getInstance().cityBuildingUnit(this, eUnit);
			if (gCityLogLevel >= 1)
			{
				CvWString szString;
				getUnitAIString(szString, eUnitAI);
				logBBAI("    City %S pushes production of unit %S with UNITAI %S", getName().GetCString(), GC.getInfo(eUnit).getDescription(), szString.GetCString());
			}
		}
		break;
	}
	case ORDER_CONSTRUCT:
	{
		BuildingTypes const eBuilding = (BuildingTypes)iData1; // advc
		if (canConstruct(eBuilding) || bForce)
		{
			GET_PLAYER(getOwner()).changeBuildingClassMaking(
					GC.getInfo(eBuilding).getBuildingClassType(), 1);
			bValid = true;
			bBuildingBuilding = true;
			CvEventReporter::getInstance().cityBuildingBuilding(this, eBuilding);
			if (gCityLogLevel >= 1) logBBAI("    City %S pushes production of building %S", getName().GetCString(), GC.getInfo(eBuilding).getDescription());
		}
		break;
	}
	case ORDER_CREATE:
	{
		ProjectTypes const eProject = (ProjectTypes)iData1; // advc
		if (canCreate(eProject) || bForce)
		{
			GET_TEAM(getTeam()).changeProjectMaking(eProject, 1);
			bValid = true;
			if (gCityLogLevel >= 1) logBBAI("    City %S pushes production of project %S", getName().GetCString(), GC.getInfo(eProject).getDescription());
		}
		break;
	}
	case ORDER_MAINTAIN:
	{
		ProcessTypes const eProcess = (ProcessTypes)iData1; // advc
		if (canMaintain(eProcess) || bForce)
		{
			bValid = true;
			/*	K-Mod. For culture processes, use iData2 to flag the current culture level
				so that we know when to stop. We could do a similar thing with
				research processes and tech... but let's not. */
			if (isHuman() && GC.getInfo(eProcess).
				getProductionToCommerceModifier(COMMERCE_CULTURE) > 0)
			{
				FAssert(iData2 == -1);
				iData2 = getCultureLevel();
			}
			// K-Mod end
			if (gCityLogLevel >= 1) logBBAI("    City %S pushes production of process %S", getName().GetCString(), GC.getInfo((ProcessTypes)iData1).getDescription());
		}
		break;
	}
	default:
		FErrorMsg("iOrder did not match a valid option");
	}

	if (!bValid)
		return;

	bool const bWasEmpty = (m_orderQueue.getLength() == 0); // advc.004x
	order.eOrderType = eOrder;
	order.iData1 = iData1;
	order.iData2 = iData2;
	order.bSave = bSave;

	/*if (bAppend)
		m_orderQueue.insertAtEnd(order);
	else {
		stopHeadOrder();
		m_orderQueue.insertAtBeginning(order);
	}
	if (!bAppend || (getOrderQueueLength() == 1))
		startHeadOrder();*/ // BtS
	// K-Mod
	if (iPosition == 0 || getOrderQueueLength() == 0)
	{
		stopHeadOrder();
		m_orderQueue.insertAtBeginning(order);
		startHeadOrder();
	}
	else if (iPosition < 0 || iPosition >= getOrderQueueLength())
		m_orderQueue.insertAtEnd(order);
	else m_orderQueue.insertBefore(order, m_orderQueue.nodeNum(iPosition));
	// K-Mod end

	// Why does this cause a crash???
	// <advc.test> Uncommented. Was added and commented out by the Warlords expansion.
	if (bBuildingUnit)
		CvEventReporter::getInstance().cityBuildingUnit(this, (UnitTypes)iData1);
	else if (bBuildingBuilding)
		CvEventReporter::getInstance().cityBuildingBuilding(this, (BuildingTypes)iData1);
	// </advc.test>
	if (isActiveTeam() || GC.getGame().isDebugMode())
	{
		setInfoDirty(true);
		if (isCitySelected())
		{
			gDLL->UI().setDirty(InfoPane_DIRTY_BIT, true);
			gDLL->UI().setDirty(SelectionButtons_DIRTY_BIT, true);
			gDLL->UI().setDirty(CityScreen_DIRTY_BIT, true);
			gDLL->UI().setDirty(PlotListButtons_DIRTY_BIT, true);
		}
	}
	// <advc.004x>
	if (bWasEmpty && isActiveOwned())
		GET_PLAYER(getOwner()).killAll(BUTTONPOPUP_CHOOSEPRODUCTION, getID());
	// </advc.004x>
}


void CvCity::popOrder(int iNum, bool bFinish,
	ChooseProductionPlayers eChoose, // advc.064d (was bool bChoose)
	bool bEndOfTurn) // advc.001x
{
	CvPlayerAI& kOwner = GET_PLAYER(getOwner());
	bool const bWasFoodProduction = isFoodProduction();

	if (iNum == -1)
		iNum = (getOrderQueueLength() - 1);

	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();
	{
		int iCount = 0;
		while (pOrderNode != NULL)
		{
			if (iCount == iNum)
				break;
			iCount++;
			pOrderNode = nextOrderQueueNode(pOrderNode);
		}
	}
	if (pOrderNode == NULL)
		return;

	if (bFinish && pOrderNode->m_data.bSave)
	{
		pushOrder(pOrderNode->m_data.eOrderType, pOrderNode->m_data.iData1,
				pOrderNode->m_data.iData2, true, false, /* K-Mod: */ -1);
	}

	UnitTypes eTrainUnit = NO_UNIT;
    UnitClassTypes eTrainUnitClass = NO_UNITCLASS;
	BuildingTypes eConstructBuilding = NO_BUILDING;
	ProjectTypes eCreateProject = NO_PROJECT;
	int iMaxedBuildingOrProject = NO_BUILDING; // advc.123f

	OrderTypes eOrderType = pOrderNode->m_data.eOrderType;
	switch(eOrderType)
	{
	case ORDER_TRAIN:
	{
		eTrainUnit = (UnitTypes)pOrderNode->m_data.iData1;
        eTrainUnitClass = GC.getInfo(eTrainUnit).getUnitClassType();
		/*	<advc.064b> Moved into new function, and moved up to ensure that the
			next order isn't already being produced when calculating production
			modifiers for the overflow cap. */
		handleOverflow(getUnitProduction(eTrainUnit) - getProductionNeeded(eTrainUnit),
				getProductionModifier(eTrainUnit), eOrderType); // </advc.064b>
		UnitAITypes eTrainAIUnit = (UnitAITypes)pOrderNode->m_data.iData2;
		FAssert(eTrainUnit != NO_UNIT);
		FAssert(eTrainAIUnit != NO_UNITAI);
		kOwner.changeUnitClassMaking(GC.getInfo(eTrainUnit).getUnitClassType(), -1);
		getArea().changeNumTrainAIUnits(getOwner(), eTrainAIUnit, -1);
		kOwner.AI_changeNumTrainAIUnits(eTrainAIUnit, -1);
		/*  <advc.113b> So that the new worker can already be taken into account
			for choosing the next order */
		if(eTrainAIUnit == UNITAI_WORKER)
			AI().AI_changeWorkersHave(1); // </advc.113b>
		doPopOrder(pOrderNode); // advc.064d (see case ORDER_CONSTRUCT)
		if(!bFinish)
			break;
		/*	<advc.064b> 14 March 2019: K-Mod multi-production code removed
			(including bugfix advc.001v). Instead restored (two lines): */
		setUnitProduction(eTrainUnit, 0);
		setUnitProductionTime(eTrainUnit, 0); // EmperorFool, Bugfix, 06/10/10
		// </advc.064b>
		CvUnit* pUnit = kOwner.initUnit(eTrainUnit, getX(), getY(), eTrainAIUnit);
		pUnit->finishMoves();

	    // doc: apply hurry effects
	    HurryTypes eHurry = getUnitHurry(eTrainUnitClass);
	    if (eHurry != NO_HURRY)
	    {
	        if (eHurry == HURRY_GOLD_UNITS)
	        {
	            // Phoenician UP: can hurry units without Mercenary promotion
	            if (getCivilizationType() != CARTHAGE)
	            {
	                pUnit->setHasPromotion(PROMOTION_MERCENARY, true);
	            }
	        }

	        // Masryeen UP: hurried units receive +3 experience with Slavery
	        if (getCivilizationType() == MISR && GET_PLAYER(getOwner()).getCivics(CIVICOPTION_SOCIETY) == CIVIC_SLAVERY)
	        {
	            if (pUnit->canFight() && pUnit->getDomainType() == DOMAIN_LAND)
	            {
	                pUnit->changeExperience(3);
	            }
	        }

	        setUnitHurry(eTrainUnitClass, NO_HURRY);
	    }

		addProductionExperience(pUnit);
		CvPlot* pRallyPlot = getRallyPlot(); // (advc.001b: moved up)
		if (GC.getInfo(eTrainUnit).getDomainType() == DOMAIN_AIR &&
			getPlot().countNumAirUnits(getTeam()) > getAirUnitCapacity(getTeam()))
		{
			// <advc.001b>
			if (pRallyPlot != NULL && pUnit->canMoveInto(*pRallyPlot))
				pUnit->move(*pRallyPlot, false, true);
			if (pUnit->at(*plot()))
			{
				pUnit->jumpToNearestValidPlot(); // (as in BtS)
				bool const bDead = pUnit->isDead();
				if (isActiveOwned())
				{
					CvWString szMsg(gDLL->getText("TXT_KEY_AIR_CAPACITY_EXCEEDED",
							pUnit->getNameKey(), getNameKey(), gDLL->getText(bDead ?
							"TXT_KEY_AIR_UNIT_SCRAPPED" : "TXT_KEY_AIR_UNIT_MOVED").GetCString()));
					gDLL->UI().addMessage(getOwner(), false, -1, szMsg, NULL, MESSAGE_TYPE_INFO,
							pUnit->getButton(), NO_COLOR,
							bDead ? getX() : pUnit->getX(), bDead ? getY() : pUnit->getY(), true, true);
				}
				if (bDead)
					break;
			}
			/*	The jump has already spent all moves. Spending all moves twice makes
				the unit unable to move on the next turn. Cf. CvUnit::doTurn. */
			pUnit->changeMoves(pUnit->maxMoves());
			// </advc.001b>
		}
		if (pRallyPlot != NULL/* advc.001b: */ && pUnit->at(getPlot()))
			pUnit->getGroup()->pushMission(MISSION_MOVE_TO, pRallyPlot->getX(), pRallyPlot->getY());
		if (kOwner.isHumanOption(PLAYEROPTION_START_AUTOMATED))
			pUnit->automate(AUTOMATE_BUILD);
		if (kOwner.isHumanOption(PLAYEROPTION_MISSIONARIES_AUTOMATED))
			pUnit->automate(AUTOMATE_RELIGION);
		CvEventReporter::getInstance().unitBuilt(this, pUnit);
		if (gCityLogLevel >= 1) // BETTER_BTS_AI_MOD, AI logging, 10/02/09, jdog5000
		{
			CvWString szString; getUnitAIString(szString, pUnit->AI_getUnitAIType());
			logBBAI("    City %S finishes production of unit %S with UNITAI %S", getName().GetCString(), pUnit->getName(0).GetCString(), szString.GetCString());
		}
		break;
	}
	case ORDER_CONSTRUCT:
	{
		eConstructBuilding = (BuildingTypes)pOrderNode->m_data.iData1;
		// <advc.064b> Moved into new function (and moved up)
		handleOverflow(getBuildingProduction(eConstructBuilding) -
				getProductionNeeded(eConstructBuilding),
				getProductionModifier(eConstructBuilding), eOrderType);
		// </advc.064b>
		BuildingClassTypes eBuildingClass = GC.getInfo(eConstructBuilding).getBuildingClassType();
		kOwner.changeBuildingClassMaking(eBuildingClass, -1);
		CvBuildingClassInfo const& kConstructClass = GC.getInfo(eBuildingClass);
		/*  advc.064d: processBuilding may now call verifyProduction. Important that
			the constructed building is no longer in the queue at that point. */
		doPopOrder(pOrderNode);
		if(!bFinish)
			break;
		if (kOwner.isBuildingClassMaxedOut(eBuildingClass,
			// UNOFFICIAL_PATCH, Bugfix, 10/08/09, davidlallen & jdog5000:
			kConstructClass.getExtraPlayerInstances()))
		{
			kOwner.removeBuildingClass(eBuildingClass);
		}
		setNumRealBuilding(eConstructBuilding, getNumRealBuilding(eConstructBuilding) + 1,
				bEndOfTurn); // advc.001x
		setBuildingProduction(eConstructBuilding, 0);
		setBuildingProductionTime(eConstructBuilding, 0); // Bugfix, 06/10/10, EmperorFool
		// <advc.123f>
		if (kConstructClass.isWorldWonder() &&
			GC.getGame().isBuildingClassMaxedOut(eBuildingClass))
		{
			iMaxedBuildingOrProject = eConstructBuilding;
		} // </advc.123f>
		CvEventReporter::getInstance().buildingBuilt(this, eConstructBuilding);
		if (gCityLogLevel >= 1) // BETTER_BTS_AI_MOD, AI logging, 10/02/09, jdog5000
			logBBAI("    City %S finishes production of building %S", getName().GetCString(), GC.getInfo(eConstructBuilding).getDescription());
		break;
	}
	case ORDER_CREATE:
	{
		eCreateProject = (ProjectTypes)pOrderNode->m_data.iData1;
		// <advc.064b> Moved into new function (and moved up)
		handleOverflow(getProjectProduction(eCreateProject) -
				getProductionNeeded(eCreateProject),
				getProductionModifier(eCreateProject), eOrderType);
		// </advc.064b>
		GET_TEAM(getTeam()).changeProjectMaking(eCreateProject, -1);
		doPopOrder(pOrderNode); // advc.064d
		if(!bFinish)
			break;

	    // doc: free unit for first to complete a project
	    if (GC.getGame().getProjectCreatedCount(eCreateProject) == 0)
	    {
	        if (GC.getInfo(eCreateProject).getFirstFreeUnit() != NO_UNIT)
	        {
	            UnitTypes eFreeUnit = GC.getInfo(eCreateProject).getFirstFreeUnit();
	            if (GC.getInfo(eFreeUnit).getDiscoverMultiplier() > 0 || GC.getInfo(eFreeUnit).getEspionagePoints() > 0 || GC.getInfo(eFreeUnit).getLeaderExperience() > 0)
	            {
	                createGreatPeople(eFreeUnit, false, false);
	            }
	            else
	            {
	                GET_PLAYER(getOwner()).initUnit(eFreeUnit, getX(), getY());
	            }
	        }
	    }

		/*	Event reported to Python before the project is built, so that we can
			show the movie before awarding free techs, for example */
		CvEventReporter::getInstance().projectBuilt(this, eCreateProject);
		GET_TEAM(getTeam()).changeProjectCount(eCreateProject, 1);
		if (GC.getInfo(eCreateProject).isSpaceship())
		{
			bool bNeedsArtType = true;
			VictoryTypes eVictory = GC.getInfo(eCreateProject).getVictoryPrereq();
			if (NO_VICTORY != eVictory && GET_TEAM(getTeam()).canLaunch(eVictory))
			{
				if(isHuman())
				{
                    // doc: do not show spaceship screen for Mars victory
					CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_LAUNCH, GC.getProjectInfo(eCreateProject).getVictoryPrereq());
				    gDLL->UI().addPopup(pInfo, getOwner());
                    /*if (GC.getGame().isNetworkMultiPlayer())
					{
						pInfo = new CvPopupInfo(BUTTONPOPUP_LAUNCH,
								GC.getInfo(eCreateProject).getVictoryPrereq());
					}
					else
					{
						pInfo = new CvPopupInfo(BUTTONPOPUP_PYTHON_SCREEN, eCreateProject);
						pInfo->setText(L"showSpaceShip");
						bNeedsArtType = false;
					}
					gDLL->UI().addPopup(pInfo, getOwner());*/
				}
				else kOwner.AI_launch(eVictory);
			}
            // doc: do not show spaceship screen for Mars victory
			/*else //show the spaceship progress
			{
				if (isHuman() &&
					BUGOption::isEnabled("TechWindow__ShowSSScreen", false)) // advc.060
				{
					if(!GC.getGame().isNetworkMultiPlayer())
					{
						CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_PYTHON_SCREEN, eCreateProject);
						pInfo->setText(L"showSpaceShip");
						gDLL->UI().addPopup(pInfo, getOwner());
						bNeedsArtType = false;
					}
				}
			}*/
			if(bNeedsArtType)
			{
				int iDefaultArtType = GET_TEAM(getTeam()).getProjectDefaultArtType(eCreateProject);
				int iProjectCount = GET_TEAM(getTeam()).getProjectCount(eCreateProject);
				GET_TEAM(getTeam()).setProjectArtType(eCreateProject, iProjectCount - 1, iDefaultArtType);
			}
		}
		setProjectProduction(eCreateProject, 0);
		// <advc.123f>
		if(GC.getGame().isProjectMaxedOut(eCreateProject))
			iMaxedBuildingOrProject = eCreateProject; // </advc.123f>
		if (gCityLogLevel >= 1) logBBAI("    City %S finishes production of project %S", getName().GetCString(), GC.getInfo(eCreateProject).getDescription()); // BETTER_BTS_AI_MOD, AI logging, 10/02/09, jdog5000
		break;
	}
	case ORDER_MAINTAIN:
		doPopOrder(pOrderNode); // advc.064d
		break;

	default:
		FErrorMsg("Unknown production order type");
		doPopOrder(pOrderNode); // advc.064d
	}
	/*  advc.064d: (BtS code moved into auxiliary function doPopOrder; called
		from within the switch block)  */
	pOrderNode = NULL; // for safety
	// <advc.123f> Fail gold from great wonders and world projects
	if (iMaxedBuildingOrProject != NO_BUILDING)
	{
		bool bProject = (eOrderType == ORDER_CREATE);
		ProjectTypes eProject = (bProject ? (ProjectTypes)iMaxedBuildingOrProject : NO_PROJECT);
		BuildingTypes eBuilding = (bProject ? NO_BUILDING :
				(BuildingTypes)iMaxedBuildingOrProject);
		BuildingClassTypes eBuildingClass = (bProject ? NO_BUILDINGCLASS :
				(BuildingClassTypes)GC.getInfo(eBuilding).getBuildingClassType());
		for (PlayerIter<CIV_ALIVE> it; it.hasNext(); ++it) // Not: Barbarians
		{
			CvPlayer& kPlayer = *it;
			if (kPlayer.getID() == getOwner()) // No fail gold for the city owner
				continue;
			// Just for efficiency
			if (!bProject && kPlayer.getBuildingClassMaking(eBuildingClass) <= 0)
				continue;
			FOR_EACH_CITY_VAR(pCity, kPlayer)
			{
				// Fail gold only for queued orders
				/*  If a mod-mod allows e.g. a wonder with up to 2 instances
					and p is building 2 instances in parallel when this city
					finishes 1 instance, abort only 1 of p's instances:
					the one with less production invested. */
				CvCity* pMinProductionCity = NULL;
				int iMinProduction = -1; // 0 production can happen
				for (int j = 0; j < pCity->getOrderQueueLength(); j++)
				{
					OrderData* pOrder = pCity->getOrderFromQueue(j);
					if (pOrder == NULL || pOrder->eOrderType !=
						(bProject ? ORDER_CREATE : ORDER_CONSTRUCT) ||
						pOrder->iData1 != iMaxedBuildingOrProject)
					{
						continue;
					}
					int iProductionInvested = (bProject ?
							pCity->getProjectProduction(eProject) :
							pCity->getBuildingProduction(eBuilding));
					if(iProductionInvested > iMinProduction)
					{
						iMinProduction = iProductionInvested;
						pMinProductionCity = pCity;
					}
				}
				if (pMinProductionCity != NULL)
				{
					// 0 fail gold for teammates
					if(kPlayer.getTeam() == getTeam())
						iMinProduction = 0;
					/*  No fail gold for overflow
						(Tbd.: Add the overflow to OverflowProduction?) */
					iMinProduction = std::min(iMinProduction,
							bProject ? getProductionNeeded(eProject) :
							getProductionNeeded(eBuilding));
					pMinProductionCity->failProduction(iMaxedBuildingOrProject,
							iMinProduction, bProject);
				}
			}
		}
	} // </advc.123f>

	CvDLLInterfaceIFaceBase& kUI = gDLL->UI();
	if (isActiveTeam() || GC.getGame().isDebugMode())
	{
		setInfoDirty(true);
		if (isCitySelected())
		{
			kUI.setDirty(InfoPane_DIRTY_BIT, true);
			kUI.setDirty(SelectionButtons_DIRTY_BIT, true);
			kUI.setDirty(CityScreen_DIRTY_BIT, true);
		}
	}

	bool bMessage = false;
	if (getOrderQueueLength() == 0 &&
		// <advc.064d>
		(eChoose == ALL_CHOOSE ||
		(eChoose != NONE_CHOOSE && (eChoose == HUMAN_CHOOSE) == isHuman()))) // </advc.064d>
	{
		if (!isHuman() || isProductionAutomated())
			AI().AI_chooseProduction();
		else
		{
			if (bWasFoodProduction)
				AI().AI_assignWorkingPlots();

			chooseProduction(eTrainUnit, eConstructBuilding, eCreateProject, bFinish);
			// <advc.004x> Remember the order in case the popup needs to be delayed
			m_bMostRecentUnit = (eTrainUnit != NO_UNIT);
			if(m_bMostRecentUnit)
				m_iMostRecentOrder = eTrainUnit;
			else if(eCreateProject != NO_PROJECT)
				m_iMostRecentOrder = GC.getNumBuildingInfos() + eCreateProject;
			else m_iMostRecentOrder = eConstructBuilding; // </advc.004x>
			bMessage = true;
		}
	}
	if (bFinish && !bMessage)
	{
		wchar szBuffer[1024]; // (advc: why not CvWString?)
		TCHAR szSound[1024];
		LPCSTR szIcon = NULL;
		if (eTrainUnit != NO_UNIT)
		{
			swprintf(szBuffer, gDLL->getText(
					GC.getInfo(eTrainUnit).isLimited() ?
					"TXT_KEY_MISC_TRAINED_UNIT_IN_LIMITED" :
					"TXT_KEY_MISC_TRAINED_UNIT_IN",
					GC.getInfo(eTrainUnit).getTextKeyWide(),
					getNameKey()).GetCString());
			strcpy(szSound, GC.getInfo(eTrainUnit).getArtInfo(
					0, kOwner.getCurrentEra(), NO_UNIT_ARTSTYLE)->getTrainSound());
			szIcon = kOwner.getUnitButton(eTrainUnit);
		}
		else if (eConstructBuilding != NO_BUILDING)
		{
			swprintf(szBuffer, gDLL->getText(
					GC.getInfo(eConstructBuilding).isLimited() ?
					"TXT_KEY_MISC_CONSTRUCTED_BUILD_IN_LIMITED" :
					"TXT_KEY_MISC_CONSTRUCTED_BUILD_IN",
					GC.getInfo(eConstructBuilding).getTextKeyWide(),
					getNameKey()).GetCString());
			strcpy(szSound, GC.getInfo(eConstructBuilding).getConstructSound());
			szIcon = GC.getInfo(eConstructBuilding).getButton();
		}
		else if (eCreateProject != NO_PROJECT)
		{
			swprintf(szBuffer, gDLL->getText(
					GC.getInfo(eCreateProject).isLimited() ?
					// <advc.008e>
					(GC.getInfo(eCreateProject).nameNeedsArticle() ?
					"TXT_KEY_MISC_CREATED_PROJECT_IN_LIMITED_THE" :
					"TXT_KEY_MISC_CREATED_PROJECT_IN_LIMITED") // </advc.008e>
					: "TXT_KEY_MISC_CREATED_PROJECT_IN",
					GC.getInfo(eCreateProject).getTextKeyWide(),
					getNameKey()).GetCString());
			strcpy(szSound, GC.getInfo(eCreateProject).getCreateSound());
			szIcon = GC.getInfo(eCreateProject).getButton();
		}
		if (isProduction())
		{
			wchar szTempBuffer[1024];
			swprintf(szTempBuffer, gDLL->getText(isProductionLimited() ?
					"TXT_KEY_MISC_WORK_HAS_BEGUN_LIMITED" :
					"TXT_KEY_MISC_WORK_HAS_BEGUN",
					getProductionNameKey()).GetCString());
			wcscat(szBuffer, szTempBuffer);
		}
		kUI.addMessage(getOwner(), false, -1, szBuffer,
				getPlot(), szSound, MESSAGE_TYPE_INFO, // advc.106b: was MINOR_EVENT
				szIcon);
	}

	if (isActiveTeam() || GC.getGame().isDebugMode())
	{
		setInfoDirty(true);
		if (isCitySelected())
		{
			kUI.setDirty(InfoPane_DIRTY_BIT, true);
			kUI.setDirty(SelectionButtons_DIRTY_BIT, true);
			kUI.setDirty(CityScreen_DIRTY_BIT, true);
			kUI.setDirty(PlotListButtons_DIRTY_BIT, true);
		}
	}
}


void CvCity::startHeadOrder()
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();
	if (pOrderNode != NULL)
	{
		if (pOrderNode->m_data.eOrderType == ORDER_MAINTAIN)
			processProcess((ProcessTypes)pOrderNode->m_data.iData1, 1);
		AI_setAssignWorkDirty(true);
	}
}


void CvCity::stopHeadOrder()
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();
	if (pOrderNode != NULL)
	{
		if (pOrderNode->m_data.eOrderType == ORDER_MAINTAIN)
			processProcess((ProcessTypes)pOrderNode->m_data.iData1, -1);
	}
}


OrderData* CvCity::getOrderFromQueue(int iIndex) /* advc: */ const
{
	CLLNode<OrderData>* pOrderNode = m_orderQueue.nodeNum(iIndex);
	if (pOrderNode != NULL)
		return &pOrderNode->m_data;
	return NULL;
}


OrderData CvCity::getOrderData(int iIndex) const
{
	int iCount = 0;
	CLLNode<OrderData>* pNode = headOrderQueueNode();
	while (pNode != NULL)
	{
		if (iIndex == iCount)
			return pNode->m_data;
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

// <advc.310>
void CvCity::addGreatWall(int iAttempt)
{
	if (GC.getDefineINT("GREAT_WALL_GRAPHIC_MODE") != 1)
	{
		gDLL->getEngineIFace()->AddGreatWall(this);
		return;
	}
	// All plots orthogonally adjacent to a (desired) wall segment
	std::set<int> aiWallPlots;
	/*	To determine if we have enough segments in the end.
		But I think it's better to place too few segments than
		to relax the placement rules arbitrarily ... */
	/*int iInside = 0;
	int iOutside = 0;*/
	CvMap& kMap = GC.getMap();
	for (int i = 0; i < kMap.numPlots(); i++)
	{
		CvPlot const& kInside = kMap.getPlotByIndex(i);
		if(!isArea(kInside.getArea()) || kInside.getOwner() != getOwner() || // as in BtS
			kInside.isImpassable()) // new: don't wall off peaks
		{
			continue;
		}
		/*	Add kInside if we find an adjacent pOutside such that the two should
			be separated by a segment */
		bool bFound = false;
		FOR_EACH_ORTH_ADJ_PLOT2(pOutside, kInside)
		{
			bool bValid = needsGreatWallSegment(kInside, *pOutside, iAttempt);
			if (!bValid && pOutside->sameArea(kInside) && !pOutside->isImpassable()
				/*	Commenting this condition out extends the wall by 1 tile into
					unhabitable terrain. Otherwise, it looks like Barbarians could just
					slip around the margins. */
				/*&& pOutside->isHabitable()*/)
			{
				/*	Also try the two plots that are orthogonally adjacent to pOutside
					and diagonally adjacent to kInside. The segment will still go between
					kInside and pOutside b/c there are no diagonal segments.
					(But never if pOutside is water or impassable; see checks above.) */
				FOR_EACH_ORTH_ADJ_PLOT(*pOutside)
				{
					if (stepDistance(pAdj, &kInside) == 1 &&
						needsGreatWallSegment(kInside, *pAdj, iAttempt))
					{
						bValid = true;
						break;
					}
				}
			}
			if (bValid)
			{
				aiWallPlots.insert(pOutside->plotNum());
				bFound = true;
				//iOutside++;
			}
		}
		if(bFound)
		{
			aiWallPlots.insert(kInside.plotNum());
			//iInside++;
		}
	}
	/*if (iAttempt == 0 && std::min(iInside, iOutside) <= 2)
	{
		addGreatWall(iAttempt + 1);
		return;
	}*/
	/*  Hack: Use a dummy CvArea object to prevent CvEngine from placing segments
		along plots not in aiWallPlots. */
	CvArea* pTmpArea = kMap.addArea();
	pTmpArea->init(false);
	/*  The city plot needs to be in the area as well b/c CvEngine will consider
		only tiles in the same CvArea as the Great Wall city */
	aiWallPlots.insert(plotNum());
	for(std::set<int>::iterator it = aiWallPlots.begin(); it != aiWallPlots.end(); ++it)
		kMap.plotByIndex(*it)->setArea(pTmpArea, /*bProcess=*/false);
	gDLL->getEngineIFace()->AddGreatWall(this);
	// Restore actual area
	for(std::set<int>::iterator it = aiWallPlots.begin(); it != aiWallPlots.end(); ++it)
		kMap.plotByIndex(*it)->setArea(area(), false);
	kMap.deleteArea(pTmpArea->getID());
}

// Helper function for placing Great Wall segments
bool CvCity::needsGreatWallSegment(/* not currently used: */CvPlot const& kInside,
	CvPlot const& kOutside, int iAttempt) const
{
	if(!isArea(kOutside.getArea()) || kOutside.isImpassable() ||
		!kOutside.isHabitable(true))
	{
		return false;
	}
	PlayerTypes eOutsideOwner = kOutside.getOwner();
	if(eOutsideOwner != NO_PLAYER && eOutsideOwner != BARBARIAN_PLAYER) // Not: any civ
		return false;
	if (iAttempt > 0)
		return true;
	/*	To avoid creating a Gaza strip, require a third plot that must be habitable,
		adjacent to the outside plot but not adjacent to our territory. */
	FOR_EACH_ADJ_PLOT2(pThird, kOutside)
	{
		if(!isArea(pThird->getArea()) ||
			pThird->isImpassable() || !pThird->isHabitable(true))
		{
			continue;
		}
		PlayerTypes eThirdOwner = pThird->getOwner();
		if((eThirdOwner == NO_PLAYER || eThirdOwner == BARBARIAN_PLAYER) &&
			!pThird->isAdjacentPlayer(getOwner(), true))
		{
			return true;
		}
	}
	return false;
} // </advc.310>


const std::vector< std::pair<float, float> >& CvCity::getWallOverridePoints() const
{
	return m_kWallOverridePoints;
}


void CvCity::doGrowth()
{
	if (GC.getPythonCaller()->doGrowth(*this))
		return;

	int iDiff = foodDifference();
	changeFood(iDiff);
	if(iDiff > 0) // advc.160: Don't empty the Granary when insufficient food
		changeFoodKept(iDiff);

	setFoodKept(range(getFoodKept(), 0, (growthThreshold() * getMaxFoodKeptPercent()) / 100));

	if (getFood() >= growthThreshold())
	{
		if (AI().AI_isEmphasizeAvoidGrowth())
			setFood(growthThreshold());
		else
		{
			changeFood(-std::max(0, growthThreshold() - getFoodKept()));
			changePopulation(1);
			CvEventReporter::getInstance().cityGrowth(this, getOwner());
		}
	}
	else if (getFood() < 0)
	{
		changeFood(-getFood());
		if (getPopulation() > 1)
		{
			changePopulation(-1);
			// <advc.160>
			changeFood(getFoodKept());
			setFoodKept(0); // </advc.160>
		}
	}
}


void CvCity::doCulture()
{
	if (GC.getPythonCaller()->doCulture(*this))
		return;
	// <advc.099b>
	if (isOccupation())
		return; // </advc.099b>
	// <advc.125>
	static int const iUseKModTradeCulture = GC.getDefineINT("USE_KMOD_TRADE_CULTURE");
	if (iUseKModTradeCulture != 0 && // </advc.125>
		// K-Mod, 26/sep/10, 31/oct/10 - Trade culture: START
		getCultureLevel() > 0 /* advc.098: */ && !isDisorder())
	{
		/*	add up the culture contribution for each player before applying it
			so that we avoid excessive calls to change culture and reduce rounding errors */
		EagerEnumMap<PlayerTypes,int> aiTradeCultureTimes100;
		for (int i = 0; i < GC.getDefineINT(CvGlobals::MAX_TRADE_ROUTES); i++)
		{
			CvCity* pLoopCity = getTradeCity(i);
			if(pLoopCity != NULL)
			{	// foreign and domestic
				//if (pLoopCity->getOwner() != getOwner())
				aiTradeCultureTimes100.add(pLoopCity->getOwner(),
						pLoopCity->getTradeCultureRateTimes100());
			}
		}
		for (PlayerIter<MAJOR_CIV> it; it.hasNext(); ++it) // advc.003n: MAJOR
		{
			PlayerTypes ePlayer = it->getID();
			if (aiTradeCultureTimes100.get(ePlayer) > 0)
			{
				// <advc.125>
				if(iUseKModTradeCulture < 0 && getPlot().getCulture(ePlayer) <= 0)
					continue; // </advc.125>
				// plot culture only.
				//changeCultureTimes100(ePlayer, aiTradeCultureTimes100.get(ePlayer), false, false);
				doPlotCultureTimes100(false, ePlayer, aiTradeCultureTimes100.get(ePlayer), false);
			}
		}
		// K-Mod END
	}
	changeCultureTimes100(getOwner(), getCommerceRateTimes100(COMMERCE_CULTURE), false, true);

    // doc: culture of dead civilizations decays
    // TODO: refactor
    int iTotalCultureTimes100 = countTotalCultureTimes100();

    bool bChanged = false;
	FOR_EACH_ENUM(Civilization)
    {
        if (!isCivAlive(eLoopCivilization))
        {
            int iChange = std::min(getActualCultureTimes100(eLoopCivilization), iTotalCultureTimes100 / 100);

            if (iChange > 0)
            {
                // culture of dead civilizations decreases by 1% of total city culture per turn
                changeCultureTimes100(eLoopCivilization, -iChange);
                bChanged = true;
            }
        }
    }

    if (bChanged)
    {
        updateCultureLevel(true);
        updateCoveredPlots(true);
    }
}

/*	This function has essentially been rewritten for K-Mod.
	(and it used to not be 'times 100') */
void CvCity::doPlotCultureTimes100(bool bUpdate, PlayerTypes ePlayer,
	int iCultureRateTimes100, bool bCityCulture)
{
	PROFILE_FUNC(); // advc: Let's keep an eye on this
	if (GC.getPythonCaller()->doPlotCultureTimes100(*this, ePlayer, bUpdate, iCultureRateTimes100))
		return;
	CultureLevelTypes const eCultureLevel = getCultureLevel(ePlayer);

	/*  K-Mod, 30/oct/10: start
		increased culture range, added a percentage based distance bonus
		(decreasing the importance of the flat rate bonus).
	Experimental culture profile ...
	Ae^(-bx). A = 10 (no effect), b = log(full_range_ratio)/range */
	//const int iOuterRatio = 10;
	//const double iB = log((double)iOuterRatio)/iCultureRange;
	/*	(iScale-1)(iDistance - iRange)^2/(iRange^2) + 1
		This approximates the exponential pretty well */
	int const iScale = plotCultureScale();
	int const iCultureRange = eCultureLevel + plotCultureExtraRange();

	if (bCityCulture)
	{
		FAssertMsg(iCultureRateTimes100 >= 0, "dubious");
		// <advc.098> Putting this BtS define back to use (with new semantics)
		static int const iCITY_FREE_CULTURE_GROWTH_FACTOR = GC.getDefineINT("CITY_FREE_CULTURE_GROWTH_FACTOR");
		iCultureRateTimes100 += iCITY_FREE_CULTURE_GROWTH_FACTOR * 100; // </advc.098>
	}

	if (eCultureLevel == NO_CULTURELEVEL ||
		(bCityCulture && isDisorder()) || // advc.098
		//getCultureTimes100(ePlayer) <= 0
		abs(iCultureRateTimes100 * iScale) < 100)
	{
		return;
	}
	// <advc.025>
	scaled rCultureToMaster = 1;
	if (GET_TEAM(getTeam()).isCapitulated())
	{
		static scaled const rCAPITULATED_TO_MASTER_CULTURE_PERCENT = per100(
				GC.getDefineINT("CAPITULATED_TO_MASTER_CULTURE_PERCENT"));
		rCultureToMaster = rCAPITULATED_TO_MASTER_CULTURE_PERCENT;
	} // </advc.025>
	for (SquareIter itPlot(getPlot(), iCultureRange); itPlot.hasNext(); ++itPlot)
	{
		int iDistance = cultureDistance(itPlot.currXDist(), itPlot.currYDist());
		if(iDistance > iCultureRange)
			continue;
		CvPlot& p = *itPlot;
		if ((p.isWater() && // advc.098
			!p.isPotentialCityWorkForArea(getArea())) ||
			(!isArea(p.getArea()) && iDistance > eCultureLevel + 1)) // advc.098
		{
			continue;
		}
		// <advc.098>
		if (iDistance > eCultureLevel && !p.isOwned())
			continue; // </advc.098>


	    // doc: cannot spread culture into birth protected civilizations
	    PlayerTypes eBirthProtectionPlayer = p.getBirthProtected();
	    bool bBirthProtected = eBirthProtectionPlayer != NO_PLAYER && eBirthProtectionPlayer != ePlayer;

	    // doc: however only if it is actually within culture range of one of their cities
        if (bBirthProtected)
	    {
	        for (int iDistance = 2; iDistance >= 0; iDistance--)
	        {
	            if (p.isCultureRangeCity(eBirthProtectionPlayer, (CultureLevelTypes)iDistance))
	            {
					bBirthProtected = false;
	                break;
	            }
	        }
	    }

        if (bBirthProtected)
            continue;

	    // doc: culture can only spread into foreign core if city itself is in foreign core
        bool bCanSpreadCore = true;
	    if (!p.isCore(ePlayer) && iCultureRange > 2)
	    {
			for (PlayerIter<MAJOR_CIV> it; it.hasNext(); ++it)
	        {
	            // Leoreth: only for civs that have already spawned yet
	            if (GC.getGame().getGameTurn() < it->getInitialBirthTurn())
	                continue;

	            if (p.isCore(it->getID()) && p.isCultureRangeCity(it->getID(), (CultureLevelTypes)iCultureRange))
	            {
	                if (plot()->isCore(it->getID()))
	                {
	                    bCanSpreadCore = true;
	                    break;
	                }
	                else
	                {
	                    bCanSpreadCore = false;
	                }
	            }
	        }
	    }

        if (!bCanSpreadCore)
            continue;

		// BtS formula for culture to add (the 20 was "CITY_FREE_CULTURE_GROWTH_FACTOR"):
		//eCultureLevel < iDistance ? 0 : (iCultureRateTimes100/100 + 1 + (eCultureLevel - iDistance) * 20;
		// K-Mod 1.45 (older K-Mod code deleted):
		//int iCultureToAdd = iCultureRateTimes100*((iScale-1)*(iDistance-iCultureRange)*(iDistance-iCultureRange) + iCultureRange*iCultureRange)/(100*iCultureRange*iCultureRange);
		/*  <advc.001> Secure this against overflow from culture added through WB.
			(K-Mod 1.46 does so too - by using floating-point math.) */
		scaled rDistFactor(SQR(iCultureRange - iDistance), SQR(iCultureRange));
		/*	Observation (rephrasing a deleted K-Mod comment):
			If iDistance is 0, then we add the culture rate times iScale.
			(However, culture distance is always at least 1 - even for the city plot.)
			If iDistance equals iCultureRange, then we add the culture rate (times 1). */
		scaled rCultureToAdd = per100(iCultureRateTimes100) * (1 + rDistFactor * (iScale - 1));
		// </advc.001>  <advc.025>
		if (p.getTeam() != getTeam() &&
			p.getTeam() == GET_TEAM(getTeam()).getMasterTeam())
		{
			rCultureToAdd *= rCultureToMaster;
		} // </advc.025>
		// <advc.098> Don't spread too deep into foreign territory
		if (rCultureToAdd > 0 && p.getOwner() != getOwner())
		{
			int const iDistToOwnedCap = plotCultureExtraRange() + 2;
			int iDistToOwned = iDistToOwnedCap;
			for (PlotCircleIter itInnerLoopPlot(p, iDistToOwned - 1, false);
				itInnerLoopPlot.hasNext(); ++itInnerLoopPlot)
			{
				if (itInnerLoopPlot.currPlotDist() < iDistToOwned)
				{
					if (itInnerLoopPlot->getOwner() == getOwner() ||
						// Needed when the city is just being founded
						&*itInnerLoopPlot == plot())
					{
						iDistToOwned = itInnerLoopPlot.currPlotDist();
					}
				}
				/*	Take advantage of the iterator's spiral pattern to
					cancel the search asap */
				else if (itInnerLoopPlot.currPlotDist() > iDistToOwned)
					break;
			}
			if (iDistToOwned >= plotCultureExtraRange())
			{
				if (iDistToOwned >= iDistToOwnedCap)
					continue;
				rCultureToAdd *= scaled(iDistToOwnedCap - iDistToOwned,
						iDistToOwnedCap - iDistToOwned + 1);
			}
		} // </advc.098>
		// <kekm.23> Loss of tile culture upon city trade
		if (rCultureToAdd.isNegative())
			rCultureToAdd.increaseTo(-p.getCulture(ePlayer)); // </kekm.23>
		p.changeCulture(ePlayer, rCultureToAdd.floor(), bUpdate || !p.isOwned());
	} // K-Mod end
}


bool CvCity::doCheckProduction()
{
	CvPlayerAI& kOwner = GET_PLAYER(getOwner());
	CvCivilization const& kCiv = getCivilization();

	if (isAnyProductionProgress(ORDER_TRAIN)) // advc.opt
	{
		for (int i = 0; i < kCiv.getNumUnits(); i++)
		{
			UnitTypes eUnit = kCiv.unitAt(i);
			if (getUnitProduction(eUnit) <= 0)
				continue;
			if (kOwner.isProductionMaxedUnitClass(kCiv.unitClass(eUnit)))
			{	// advc.123f: Commented out (fail gold from national units)
				/*int iProductionGold = ((getUnitProduction(eUnit) * GC.getDefineINT("MAXED_UNIT_GOLD_PERCENT")) / 100);
				if (iProductionGold > 0) {
					kOwner.changeGold(iProductionGold);
					CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_LOST_WONDER_PROD_CONVERTED", getNameKey(), GC.getInfo(eUnit).getTextKeyWide(), iProductionGold);
					gDLL->UI().addMessage(getOwner(), false, -1, szBuffer, getPlot(), "AS2D_WONDERGOLD", MESSAGE_TYPE_MINOR_EVENT, GC.getInfo(COMMERCE_GOLD).getButton(), GC.getColorType("RED"));
				}*/
				setUnitProduction(eUnit, 0);
			}
		}
	}
	if (isAnyProductionProgress(ORDER_CONSTRUCT)) // advc.opt
	{
		for (int i = 0; i < kCiv.getNumBuildings(); i++)
		{
			BuildingTypes eBuilding = kCiv.buildingAt(i);
			if (getBuildingProduction(eBuilding) <= 0)
				continue;
			if (kOwner.isProductionMaxedBuildingClass(kCiv.buildingClass(eBuilding)))
			{	// advc.123f: Commented out. Fail gold now handled in popOrder.
				/*iProductionGold = ((getBuildingProduction(eBuilding) * GC.getDefineINT("MAXED_BUILDING_GOLD_PERCENT")) / 100);
				if(iProductionGold > 0) {
					kOwner.changeGold(iProductionGold);
					CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_LOST_WONDER_PROD_CONVERTED", getNameKey(), GC.getInfo(eBuilding).getTextKeyWide(), iProductionGold);
					gDLL->UI().addMessage(getOwner(), false, -1, szBuffer, getPlot(), "AS2D_WONDERGOLD", MESSAGE_TYPE_MINOR_EVENT, GC.getInfo(COMMERCE_GOLD).getButton(), GC.getColorType("RED"));
				}*/
				setBuildingProduction(eBuilding, 0);
			}
		}
	}
	if (isAnyProductionProgress(ORDER_CREATE)) // advc.opt
	{
		FOR_EACH_ENUM(Project)
		{
			if (getProjectProduction(eLoopProject) <= 0)
				continue;
			if (kOwner.isProductionMaxedProject(eLoopProject))
			{	// advc.123f: Commented out. Fail gold now handled in popOrder.
				/*iProductionGold = ((getProjectProduction(eLoopProject) * GC.getDefineINT("MAXED_BUILDING_GOLD_PERCENT")) / 100);
				if(iProductionGold > 0) {
					kOwner.changeGold(iProductionGold);
					CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_LOST_WONDER_PROD_CONVERTED", getNameKey(), GC.getInfo(eLoopProject).getTextKeyWide(), iProductionGold);
					gDLL->UI().addMessage(getOwner(), false, -1, szBuffer, getPlot(), "AS2D_WONDERGOLD", MESSAGE_TYPE_MINOR_EVENT, GC.getInfo(COMMERCE_GOLD).getButton(), GC.getColorType("RED"));
				}*/
				setProjectProduction(eLoopProject, 0);
			}
		}
	}
	if (!isProduction() && !isDisorder() && isHuman() && !isProductionAutomated())
	{
		chooseProduction();
		return true;
	}
	// <advc.064d> Moved into new functions
	upgradeProduction();
	return checkCanContinueProduction(false); // </advc.064d>
}

// advc.064d: Cut from doCheckProduction
void CvCity::upgradeProduction()
{
	CvPlayerAI& kOwner = GET_PLAYER(getOwner());
	CvCivilization const& kCiv = getCivilization();
	for (int i = 0; i < kCiv.getNumUnits(); i++)
	{
		UnitTypes eUnit = kCiv.unitAt(i);
		if (getFirstUnitOrder(eUnit) == -1)
			continue;

		UnitTypes eUpgradeUnit = allUpgradesAvailable(eUnit);
		if (eUpgradeUnit == NO_UNIT)
			continue;
		FAssert(eUpgradeUnit != eUnit);

		int iUpgradeProduction = getUnitProduction(eUnit);
		setUnitProduction(eUnit, 0);
		setUnitProduction(eUpgradeUnit, iUpgradeProduction);

		CLLNode<OrderData>* pOrderNode = headOrderQueueNode();
		while (pOrderNode != NULL)
		{
			if (pOrderNode->m_data.eOrderType == ORDER_TRAIN &&
				pOrderNode->m_data.iData1 == eUnit)
			{
				kOwner.changeUnitClassMaking(GC.getInfo((UnitTypes)
						pOrderNode->m_data.iData1).getUnitClassType(), -1);
				pOrderNode->m_data.iData1 = eUpgradeUnit;
				if (kOwner.AI_unitValue(eUpgradeUnit, (UnitAITypes)pOrderNode->m_data.iData2, area()) == 0)
				{
					getArea().changeNumTrainAIUnits(getOwner(), (UnitAITypes)pOrderNode->m_data.iData2, -1);
					kOwner.AI_changeNumTrainAIUnits(((UnitAITypes)pOrderNode->m_data.iData2), -1);
					pOrderNode->m_data.iData2 = GC.getInfo(eUpgradeUnit).getDefaultUnitAIType();
					getArea().changeNumTrainAIUnits(getOwner(), (UnitAITypes)pOrderNode->m_data.iData2, 1);
					kOwner.AI_changeNumTrainAIUnits((UnitAITypes)pOrderNode->m_data.iData2, 1);
				}
				// advc (note): pOrderNode may have changed
				kOwner.changeUnitClassMaking(GC.getInfo((UnitTypes)
						pOrderNode->m_data.iData1).getUnitClassType(), 1);
			}
			pOrderNode = nextOrderQueueNode(pOrderNode);
		}
	}
}

// advc.064d: Cut from doCheckProduction
bool CvCity::checkCanContinueProduction(bool bCheckUpgrade,
	ChooseProductionPlayers eChoose)
{
	bool bAllContinued = true;
	for (int i = getOrderQueueLength() - 1; i >= 0; i--)
	{
		OrderData* pOrder = getOrderFromQueue(i);
		if (pOrder != NULL && !canContinueProduction(*pOrder))
		{
			if (bCheckUpgrade)
			{
				upgradeProduction();
				return checkCanContinueProduction(false, eChoose);
			}
			popOrder(i, false, eChoose);
			bAllContinued = false;
		}
	}  // <advc.004x> Relaunch choose-production popups
	if (!bAllContinued)
		GET_PLAYER(getOwner()).killAll(NO_BUTTONPOPUP); // </advc.004x>
	return bAllContinued;
}


void CvCity::doProduction(bool bAllowNoProduction)
{
	if (GC.getPythonCaller()->doProduction(*this))
		return;

	if (!isHuman() || isProductionAutomated())
	{
		if (!isProduction() || isProductionProcess() ||
			isChooseProductionDirty())
		{
			AI().AI_chooseProduction();
		}
	}

	if (!bAllowNoProduction && !isProduction())
		return;

	if (isProductionProcess())
	{
		// K-Mod. End the culture process if our borders have expanded.
		// (This function is called after "doResearch" etc.)
		// TODO: this should also cancel if tile covered
		OrderData const& kOrder = headOrderQueueNode()->m_data;
		if (kOrder.iData2 > 0 && GC.getInfo((ProcessTypes)kOrder.iData1).
			getProductionToCommerceModifier(COMMERCE_CULTURE) > 0 &&
			getCultureLevel() > kOrder.iData2)
		{
			popOrder(0, false, ALL_CHOOSE);
		}
		// K-Mod end
		return;
	}

	if (isDisorder())
		return;

	if (isProduction())
	{
		int iFeatureProductionUsed=0; // advc.064b
		changeProduction(getCurrentProductionDifference(false, true, false,
				false, false, &iFeatureProductionUsed)); // advc.064b
		setOverflowProduction(0);
		//setFeatureProduction(0);
		changeFeatureProduction(-iFeatureProductionUsed); // advc.064b

		if (getProduction() >= getProductionNeeded())
			popOrder(0, true, ALL_CHOOSE);
	}
	else
	{
		changeOverflowProduction(getCurrentProductionDifference(false, false,
				/* advc.064b: */ true), getProductionModifier());
	}
}


void CvCity::doDecay()
{
	FOR_EACH_ENUM(Building)
	{
		if (getProductionBuilding() == eLoopBuilding)
			continue;
		if (getBuildingProduction(eLoopBuilding) > 0)
		{
			changeBuildingProductionTime(eLoopBuilding, 1);
			if (isHuman())
			{
				int const iGameSpeedPercent = GC.getInfo(GC.getGame().
						getGameSpeedType()). getConstructPercent();
				if (100 * getBuildingProductionTime(eLoopBuilding) >
					GC.getDefineINT(CvGlobals::BUILDING_PRODUCTION_DECAY_TIME) * iGameSpeedPercent)
				{
					int iProduction = getBuildingProduction(eLoopBuilding);
					int const iDecayPercent = GC.getDefineINT(CvGlobals::BUILDING_PRODUCTION_DECAY_PERCENT);
					setBuildingProduction(eLoopBuilding, iProduction -
							(iProduction * (100 - iDecayPercent) + iGameSpeedPercent - 1) /
							iGameSpeedPercent);
				}
			}
		}
		else setBuildingProductionTime(eLoopBuilding, 0);
	}
	FOR_EACH_ENUM(Unit)
	{
		if (getProductionUnit() == eLoopUnit)
			continue;
		if (getUnitProduction(eLoopUnit) > 0)
		{
			changeUnitProductionTime(eLoopUnit, 1);
			if (isHuman())
			{
				int const iGameSpeedPercent = GC.getInfo(GC.getGame().
						getGameSpeedType()).getTrainPercent();
				if (100 * getUnitProductionTime(eLoopUnit) >
					GC.getDefineINT(CvGlobals::UNIT_PRODUCTION_DECAY_TIME) * iGameSpeedPercent)
				{
					int iProduction = getUnitProduction(eLoopUnit);
					int const iDecayPercent = GC.getDefineINT(CvGlobals::UNIT_PRODUCTION_DECAY_PERCENT);
					setUnitProduction(eLoopUnit, iProduction -
							(iProduction * (100 - iDecayPercent) + iGameSpeedPercent - 1) /
							iGameSpeedPercent);
				}
			}
		}
		else setUnitProductionTime(eLoopUnit, 0);
	}
}

// doc
bool CvCity::canSpread(ReligionTypes eReligion, bool bMissionary) const
{
	if (isHasReligion(eReligion)) return false;

	if (bMissionary) return true;

	if (!getPlot().canSpread(eReligion)) return false;

	ReligionSpreadTypes eSpread = GET_PLAYER(getOwner()).getSpreadType(getPlot(), eReligion);

	if (eSpread == RELIGION_SPREAD_NONE) return false;

	if (eSpread == RELIGION_SPREAD_MINORITY && getReligionCount() == 0) return false;

	if (GC.getInfo(eReligion).isLocal() && GC.getGame().isReligionFounded(eReligion) && GET_PLAYER(GC.getGame().getHolyCity(eReligion)->getOwner()).isMinorCiv())
		return false;

	return true;
}

// doc
int CvCity::getTurnsToSpread(ReligionTypes eReligion) const
{
	bool bDistant = GET_PLAYER(getOwner()).isDistantSpread(*this, eReligion);
	ReligionSpreadTypes eSpread = GET_PLAYER(getOwner()).getSpreadType(getPlot(), eReligion, bDistant);
	ReligionTypes eStateReligion = GET_PLAYER(getOwner()).getStateReligion();
	int iIncrement = 50;

	if (eStateReligion != eReligion && eStateReligion != NO_RELIGION && eSpread != RELIGION_SPREAD_FAST) 
		iIncrement += 20;

	if (eSpread == RELIGION_SPREAD_FAST)
	{
		iIncrement -= 10;

		if (getReligionCount() == 0)
		{
			iIncrement -= 10;

			if (bDistant)
				iIncrement -= 10;
		}

		if (getArea().countHasReligion(eReligion, getOwner()) == 0)
			iIncrement -= 10;
	}

	int iCurrentTurn = GC.getGame().getGameTurn();
	int iFoundingTurn = GC.getGame().getReligionGameTurnFounded(eReligion);

	if (iCurrentTurn - iFoundingTurn <= getTurns(GC.getDefineINT("RELIGION_FOUNDING_SPREAD_TURNS"))) 
		iIncrement -= 10;

	int iTurns = iIncrement;

	FOR_EACH_ENUM(Religion)
	{
		if (isHasReligion(eLoopReligion) && !GET_PLAYER(getOwner()).isTolerating(eLoopReligion))
			iTurns += iIncrement;
	}

	if (isHasConflicting(eReligion)) 
		iTurns += iIncrement;

	if (eStateReligion == eReligion && isHasPrecursor(eReligion)) 
		iTurns -= iIncrement / 2;

	if (eSpread == RELIGION_SPREAD_MINORITY) 
		iTurns *= 2;

	if (GC.getReligionInfo(eReligion).isLocal() && eSpread == RELIGION_SPREAD_MINORITY && !isHasPrecursor(eReligion))
		iTurns *= 2;

	return getTurns(iTurns);
}

// doc
bool CvCity::isHasPrecursor(ReligionTypes eReligion) const
{
	if (eReligion == CONFUCIANISM) return isHasReligion(TAOISM);
	if (eReligion == TAOISM) return isHasReligion(CONFUCIANISM);
	if (eReligion == BUDDHISM) return isHasReligion(HINDUISM);

	if (GET_PLAYER(getOwner()).getStateReligion() == eReligion)
	{
		if (eReligion == ISLAM) return isHasReligion(CATHOLICISM) || isHasReligion(ORTHODOXY);

		if (eReligion == ORTHODOXY) return isHasReligion(JUDAISM) && !isHasReligion(CATHOLICISM) && !isHasReligion(PROTESTANTISM);
		if (eReligion == CATHOLICISM) return isHasReligion(JUDAISM) && !isHasReligion(ORTHODOXY) && !isHasReligion(PROTESTANTISM);
	}

	return false;
}

// doc
bool CvCity::isHasConflicting(ReligionTypes eReligion) const
{
	if (eReligion == ORTHODOXY || eReligion == CATHOLICISM || eReligion == PROTESTANTISM)
	{
		return isHasReligion(ORTHODOXY) || isHasReligion(CATHOLICISM) || isHasReligion(PROTESTANTISM) || isHasReligion(ISLAM);
	}

	return false;
}

// doc
int CvCity::getReligionPopulation(ReligionTypes eReligion) const
{
	if (!isHasReligion(eReligion)) return 0;

	ReligionTypes eStateReligion = GET_PLAYER(getOwner()).getStateReligion();

	// if there is no state religion (pagan or secular), we assign an equal part to either pagan or nonreligious
	if (eStateReligion == NO_RELIGION)
	{
		return getPopulation() / (getReligionCount() + 1);
	}
	else
	{
		// if the state religion is present in the city, assign at least 50% to the state religion and split the rest evenly between all religions
		if (isHasReligion(eStateReligion))
		{
			return (eStateReligion == eReligion ? getPopulation() / 2 : 0) + getPopulation() / (2 * getReligionCount());
		}
		// otherwise we simply split evenly between all religions
		else
		{
			return getPopulation() / getReligionCount();
		}
	}
}

// doc: custom spread logic without using the advciv implementation
void CvCity::doReligion()
{
	FOR_EACH_ENUM(Religion)
    {
        if (!canSpread(eLoopReligion) && !(GET_PLAYER(getOwner()).isDistantSpread(*this, eLoopReligion))) continue;

        int iChance = getTurnsToSpread(eLoopReligion);
        int iRand = GC.getGame().getSorenRandNum(iChance, "Religion spread");

        if (iRand == 0)
        {
            spreadReligion(eLoopReligion);
            return;
        }
    }

    ReligionTypes eDisappearingReligion = disappearingReligion();

    if (eDisappearingReligion != NO_RELIGION && !GET_PLAYER(getOwner()).isDistantSpread(*this, eDisappearingReligion))
    {
        int iChance = GET_PLAYER(getOwner()).getSpreadType(getPlot(), eDisappearingReligion) * 25 + 25;
        int iRand = GC.getGame().getSorenRandNum(iChance, "Religion disappearance");

        if (iRand == 0)
        {
            removeReligion(eDisappearingReligion);
        }
    }
}


void CvCity::doGreatPeople()
{
	if (GC.getPythonCaller()->doGreatPeople(*this))
		return;

	if (isDisorder())
		return;

	CvCivilization const& kCiv = getCivilization();

	changeGreatPeopleProgress(getGreatPeopleRate());
	// <advc> Verify that GreatPeopleRate is the sum of the GreatPeopleUnitRates
	#ifdef FASSERT_ENABLE
		int iTotalUnitRate = 0;
	#endif // </advc>
	/*	(advc.001c: Don't check the same for Progress values b/c it won't be true
		for old saves) */
	int const iTotalGreatPeopleRateModifier = getTotalGreatPeopleRateModifier(); // advc.001c
	for (int i = 0; i < kCiv.getNumUnits(); i++)
	{
		UnitTypes eUnit = kCiv.unitAt(i);
		int iUnitRate = getGreatPeopleUnitRate(eUnit); // advc
		changeGreatPeopleUnitProgress(eUnit, (iUnitRate *
				/*	advc.001c: Seems like an oversight - per-unit progress
					should include modifiers. */
				iTotalGreatPeopleRateModifier) / 100);
		// <advc>
		#ifdef FASSERT_ENABLE
			iTotalUnitRate += iUnitRate;
		#endif // </advc>
	}
	FAssert(iTotalUnitRate == getBaseGreatPeopleRate()); // advc
	if (getGreatPeopleProgress() >= GET_PLAYER(getOwner()).greatPeopleThreshold())
	{
		int iTotalGreatPeopleUnitProgress = 0;
		for (int i = 0; i < kCiv.getNumUnits(); i++)
		{
			iTotalGreatPeopleUnitProgress += getGreatPeopleUnitProgress(kCiv.unitAt(i));
		}
		/*	<advc> Should only happen in old savegames (due to a bug in AdvCiv 0.97).
			NB: If we break savegame compatibility, then we should call
			CvRandom::weightedChoice here (to avoid code duplication). */
		bool const bOverflow = (iTotalGreatPeopleUnitProgress > CvRandom::getRange());
		if (bOverflow)
			iTotalGreatPeopleUnitProgress = per100(iTotalGreatPeopleUnitProgress).ceil();
		// </advc>
		UnitTypes eGreatPeopleUnit = NO_UNIT;
		{
			int iGreatPeopleUnitRand = SyncRandNum(iTotalGreatPeopleUnitProgress);
			for (int i = 0; i < kCiv.getNumUnits(); i++)
			{
				UnitTypes eLoopGP = kCiv.unitAt(i);
				int iLoopProgress = getGreatPeopleUnitProgress(eLoopGP);
				// <advc> (see above)
				if (bOverflow)
					iLoopProgress = per100(iLoopProgress).ceil(); // </advc>
				if (iGreatPeopleUnitRand < iLoopProgress)
				{
					eGreatPeopleUnit = eLoopGP;
					break;
				}
				iGreatPeopleUnitRand -= iLoopProgress;
			}
		}
		if (eGreatPeopleUnit != NO_UNIT)
		{
			changeGreatPeopleProgress(-GET_PLAYER(getOwner()).greatPeopleThreshold(false));
			for (int i = 0; i < kCiv.getNumUnits(); i++)
			{
				setGreatPeopleUnitProgress(kCiv.unitAt(i), 0);
			}
			createGreatPeople(eGreatPeopleUnit, true, false);
		}
	}
}


void CvCity::doMeltdown()
{
	if (GC.getPythonCaller()->doMeltdown(*this))
		return;

	CvCivilization const& kCiv = getCivilization();
	for (int i = 0; i < kCiv.getNumBuildings(); i++)
	{
		BuildingTypes eDangerBuilding = kCiv.buildingAt(i);
		if (!isMeltdownBuilding(eDangerBuilding))
			continue;
		// advc.opt: Roll the dice before checking for a safe power source
		{
			int iOddsDivisor = GC.getInfo(eDangerBuilding).getNukeExplosionRand();
			// <advc.652>
			iOddsDivisor *= GC.getGame().getSpeedPercent();
			iOddsDivisor /= 100; // </advc.652>
			if (!SyncRandOneChanceIn(iOddsDivisor) ||
				isMeltdownBuildingSuperseded(eDangerBuilding)) // kekm.5
			{
				continue;
			}
		}
        triggerMeltdown(eDangerBuilding);
		break;
	}
}


// doc
void CvCity::triggerMeltdown(BuildingTypes eBuilding)
{
    if (getNumRealBuilding(eBuilding) > 0)
        setNumRealBuilding(eBuilding, 0);

    getPlot().nukeExplosion(1, /* K-Mod: */ 0, false);

    CvWString szBuffer(gDLL->getText("TXT_KEY_MISC_MELTDOWN_CITY", getNameKey()));
    // advc.106: Notify all players
    for (PlayerIter<MAJOR_CIV> it; it.hasNext(); ++it)
    {
        CvPlayer const& kObs = *it;
        if (isRevealed(kObs.getTeam()) /* advc.127: */ || kObs.isSpectator())
        {
            bool bAffected = kObs.getID() == getOwner();
            gDLL->UI().addMessage(kObs.getID(), false, -1, szBuffer, getPlot(),
                    "AS2D_MELTDOWN",
                    // advc.106: Was MINOR (and only the owner was notified)
                    bAffected ? MESSAGE_TYPE_MAJOR_EVENT : MESSAGE_TYPE_MINOR_EVENT,
                    ARTFILEMGR.getInterfaceArtPath("INTERFACE_UNHEALTHY_PERSON"),
                    GC.getColorType(bAffected ? "RED" : "BUILDING_TEXT"));
        }
    }
    // <advc.106> Replay msg - or maybe not. Doesn't really affect the cause of the game.
    /*GC.getGame().addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, getOwner(), szBuffer,
            getX(), getY(), GET_PLAYER(getOwner()).getPlayerTextColor());*/ // </advc.106>
}

// advc.652: Kek-Mod code moved into subroutine
bool CvCity::isMeltdownBuilding(BuildingTypes eBuilding) const
{
	CvBuildingInfo const& kBuilding = GC.getInfo(eBuilding);
	// <kekm.5>
	if (kBuilding.getNukeExplosionRand() <= 0)
		return false;
	if (getNumActiveBuilding(eBuilding) <= 0) // getNumBuilding in Kek-Mod
		return false;
	if (isAreaCleanPower() ||
		(!kBuilding.isPower() && kBuilding.getPowerBonus() == NO_BONUS) ||
		(kBuilding.getPowerBonus() != NO_BONUS &&
		!hasBonus(kBuilding.getPowerBonus())))
	{
		return false;
	} // </kekm.5>
	return true;
}

/*	advc.652: Kek-Mod code moved into subroutine. Caller should ensure that
	eDangerBuilding can cause a meltdown when assuming that no other power source
	exists in this city. */
bool CvCity::isMeltdownBuildingSuperseded(BuildingTypes eDangerBuilding) const
{
	CvBuildingInfo const& kDangerBuilding = GC.getInfo(eDangerBuilding);
	CvCivilization const& kCiv = getCivilization();
	// <kekm.5>
	// Check for hydroplant (or any modded plant with less severe drawbacks)
	for (int i = 0; i < kCiv.getNumBuildings(); i++)
	{
		BuildingTypes eSafeBuilding = kCiv.buildingAt(i);
		if (eDangerBuilding == eSafeBuilding ||
			getNumActiveBuilding(eSafeBuilding) <= 0)
		{
			continue;
		}
		CvBuildingInfo const& kSafeBuilding = GC.getInfo(eSafeBuilding);
		if(!kSafeBuilding.isPower() &&
			(kSafeBuilding.getPowerBonus() == NO_BONUS ||
			!hasBonus(kSafeBuilding.getPowerBonus())))
		{
			continue;
		}
		if (kDangerBuilding.isDirtyPower() && !kSafeBuilding.isDirtyPower())
			return true;

		if (kDangerBuilding.isDirtyPower() != kSafeBuilding.isDirtyPower())
			continue;
		if (kSafeBuilding.getNukeExplosionRand() == 0)
			return true;
		if (kDangerBuilding.getNukeExplosionRand() >
			kSafeBuilding.getNukeExplosionRand())
		{
			continue;
		}
		if (kDangerBuilding.getNukeExplosionRand() < kSafeBuilding.getNukeExplosionRand())
			return true;
		if (eDangerBuilding < eSafeBuilding)
			return true;
	}
	return false;
}


// TODO: validate that it covers all members and matches write
void CvCity::read(FDataStreamBase* pStream)
{
	uint uiFlag=0;
	pStream->Read(&uiFlag);

	pStream->Read(&m_iID);
	pStream->Read(&m_iX);
	pStream->Read(&m_iY);
	updatePlot(); // advc.opt
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
	pStream->Read(&m_iSurroundingGoodHealth);
	pStream->Read(&m_iSurroundingBadHealth);
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
	pStream->Read(&m_iSurroundingGoodHappiness);
	pStream->Read(&m_iSurroundingBadHappiness);
	pStream->Read(&m_iBonusGoodHappiness);
	pStream->Read(&m_iBonusBadHappiness);
	pStream->Read(&m_iReligionGoodHappiness);
	pStream->Read(&m_iReligionBadHappiness);
	pStream->Read(&m_iExtraHappiness);
	pStream->Read(&m_iExtraHealth);
	pStream->Read(&m_iNoUnhappinessCount);
	//pStream->Read(&m_iNoUnhealthyPopulationCount);
	pStream->Read(&m_iUnhealthyPopulationModifier); // K-Mod
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

	// doc
	pStream->Read(&m_iPowerConsumedCount);
	pStream->Read(&m_iSpecialistGoodHappiness);
	pStream->Read(&m_iSpecialistBadHappiness);
	pStream->Read(&m_iCorporationGoodHappiness);
	pStream->Read(&m_iCorporationBadHappiness);
	pStream->Read(&m_iCorporationHealth);
	pStream->Read(&m_iCorporationUnhealth);
	pStream->Read(&m_iCultureGreatPeopleRateModifier);
	pStream->Read(&m_iCultureHappiness);
	pStream->Read(&m_iCultureTradeRouteModifier);
	pStream->Read(&m_iBuildingUnignorableBombardDefense);
	pStream->Read(&m_iCultureRank);
	pStream->Read(&m_iStabilityPopulation);
	pStream->Read(&m_iTotalCultureTimes100);
	pStream->Read(&m_iBuildingDamage);
	pStream->Read(&m_iBuildingDamageChange);
	pStream->Read(&m_iTotalPopulationLoss);
	pStream->Read(&m_iPopulationLoss);

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
	pStream->Read(&m_bMongolUP); // doc

	pStream->Read(&m_bInvestigate);
	pStream->Read(&m_bChooseProductionDirty);

	pStream->Read((int*)&m_eOwner);
	pStream->Read((int*)&m_ePreviousCiv);
	pStream->Read((int*)&m_eOriginalCiv);
	pStream->Read((int*)&m_eCultureLevel);
	pStream->Read((int*)&m_eArtStyle); // doc
	pStream->Read((int*)&m_eNextCoveredPlot); // doc

	m_aiSeaPlotYield.read(pStream);
	m_aiRiverPlotYield.read(pStream);
    m_aiFlatRiverPlotYield.read(pStream); // doc
	m_aiBaseYieldRate.read(pStream);
	m_aiYieldRateModifier.read(pStream);
	m_aiPowerYieldRateModifier.read(pStream);
	m_aiBonusYieldRateModifier.read(pStream);
	m_aiTradeYield.read(pStream);
	m_aiCorporationYield.read(pStream);
	m_aiExtraSpecialistYield.read(pStream);
    m_aiHappinessYield.read(pStream); // doc
	m_aiCommerceRate.read(pStream);
	m_aiProductionToCommerceModifier.read(pStream);
	m_aiBuildingCommerce.read(pStream);
	m_aiSpecialistCommerce.read(pStream);
	m_aiReligionCommerce.read(pStream);
	m_aiCorporationCommerce.read(pStream);
	m_aiCommerceRateModifier.read(pStream);
    m_aiPowerCommerceRateModifier.read(pStream); // doc
    m_aiCultureCommerceRateModifier.read(pStream); // doc
    m_aiBonusCommerceRateModifier.read(pStream); // doc
	m_aiCommerceHappinessPer.read(pStream);
	m_aiDomainFreeExperience.read(pStream);
	m_aiDomainProductionModifier.read(pStream);
	m_aiCulture.read(pStream);
	m_aiNumRevolts.read(pStream);
    m_aiGameTurnCivLost.read(pStream); // doc
    m_aiCulturePlots.read(pStream); // doc
    m_aiCultureCosts.read(pStream); // doc

	m_abEverOwned.read(pStream);
	m_abTradeRoute.read(pStream);
	m_abRevealed.read(pStream);
	m_abEspionageVisibility.read(pStream);

	pStream->ReadString(m_szName);
	pStream->ReadString(m_szPreviousName); // </advc.106k>
	pStream->ReadString(m_szScriptData);

	m_aiNoBonus.read(pStream);
	m_aiFreeBonus.read(pStream);
	m_aiNumBonuses.read(pStream);
	m_aiNumCorpProducedBonuses.read(pStream);
	m_aiProjectProduction.read(pStream);
	m_aiBuildingProduction.read(pStream);
	m_aiBuildingProductionTime.read(pStream);
	m_aeBuildingOriginalOwner.read(pStream);
	m_aiBuildingOriginalTime.read(pStream);
	m_aiUnitProduction.read(pStream);
	m_aiUnitProductionTime.read(pStream);
	m_aiGreatPeopleUnitRate.read(pStream);
	m_aiGreatPeopleUnitProgress.read(pStream);
	m_aiSpecialistCount.read(pStream);
	m_aiMaxSpecialistCount.read(pStream);
	m_aiForceSpecialistCount.read(pStream);
	m_aiFreeSpecialistCount.read(pStream);
	m_aiImprovementFreeSpecialists.read(pStream);
	m_aiReligionInfluence.read(pStream);
	m_aiShrine.read(pStream); // </advc.enum>
	m_aiStateReligionHappiness.read(pStream);
	m_aiUnitCombatFreeExperience.read(pStream);
	m_aiFreePromotionCount.read(pStream);
	m_aiNumRealBuilding.read(pStream);
	m_aiNumFreeBuilding.read(pStream);

	m_abWorkingPlot.read(pStream);
	m_abHasReligion.read(pStream);
	m_abHasCorporation.read(pStream);

	for (size_t i = 0; i < m_aTradeCities.size(); i++)
	{
		pStream->Read((int*)&m_aTradeCities[i].eOwner);
		pStream->Read(&m_aTradeCities[i].iID);
		m_aTradeCities[i].validateOwner(); // advc.opt
	}

	m_orderQueue.Read(pStream);

	pStream->Read(&m_iPopulationRank);
	pStream->Read(&m_bPopulationRankValid);

	m_aiBaseYieldRank.read(pStream);
	m_abBaseYieldRankValid.read(pStream);
	m_aiYieldRank.read(pStream);
	m_abYieldRankValid.read(pStream);
	m_aiCommerceRank.read(pStream);
	m_abCommerceRankValid.read(pStream);

	int iNumElts=-1;

	pStream->Read(&iNumElts);
	m_hurriedUnits.clear();
	for (int i = 0; i < iNumElts; ++i)
	{
		UnitClassTypes eUnitClass;
		HurryTypes eHurry;
		pStream->Read((int*)&eUnitClass);
		pStream->Read((char*)&eHurry);
		m_hurriedUnits.push_back(std::make_pair(eUnitClass, eHurry));
	}

	pStream->Read(&iNumElts);
	m_aEventsOccured.clear();
	for (int i = 0; i < iNumElts; ++i)
	{
		EventTypes eEvent;
		pStream->Read((int*)&eEvent);
		m_aEventsOccured.push_back(eEvent);
	}

	m_aeiiBuildingYieldChange.read(pStream);
	m_aeiiBuildingCommerceChange.read(pStream);
	m_aeiBuildingHappyChange.read(pStream);
	m_aeiBuildingHealthChange.read(pStream);
	m_aeiiBonusYieldChange.read(pStream); // doc
    m_aeiBuildingGreatPeopleRateChange.read(pStream); // doc

	pStream->Read(&m_iPopRushHurryCount);
	pStream->Read(&m_iMostRecentOrder);
	pStream->Read(&m_bMostRecentUnit);
}

void CvCity::write(FDataStreamBase* pStream)
{
	PROFILE_FUNC(); // advc
	REPRO_TEST_BEGIN_WRITE(CvString::format("City(%d,%d)", getX(), getY()));
	uint uiFlag = 0;
	pStream->Write(uiFlag);

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
	pStream->Write(m_iSurroundingGoodHealth);
	pStream->Write(m_iSurroundingBadHealth);
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
	pStream->Write(m_iSurroundingGoodHappiness);
	pStream->Write(m_iSurroundingBadHappiness);
	pStream->Write(m_iBonusGoodHappiness);
	pStream->Write(m_iBonusBadHappiness);
	pStream->Write(m_iReligionGoodHappiness);
	pStream->Write(m_iReligionBadHappiness);
	pStream->Write(m_iExtraHappiness);
	pStream->Write(m_iExtraHealth);
	pStream->Write(m_iNoUnhappinessCount);
	//pStream->Write(m_iNoUnhealthyPopulationCount);
	pStream->Write(m_iUnhealthyPopulationModifier); // K-Mod
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

	// doc
	pStream->Write(m_iPowerConsumedCount);
	pStream->Write(m_iSpecialistGoodHappiness);
	pStream->Write(m_iSpecialistBadHappiness);
	pStream->Write(m_iCorporationGoodHappiness);
	pStream->Write(m_iCorporationBadHappiness);
	pStream->Write(m_iCorporationHealth);
	pStream->Write(m_iCorporationUnhealth);

	pStream->Write(m_iCultureGreatPeopleRateModifier);
	pStream->Write(m_iCultureHappiness);
	pStream->Write(m_iCultureTradeRouteModifier);

	pStream->Write(m_iBuildingUnignorableBombardDefense);

	pStream->Write(m_iCultureRank);

	pStream->Write(m_iStabilityPopulation); // doc

	pStream->Write(m_iTotalCultureTimes100); // doc

	pStream->Write(m_iBuildingDamage); // doc
	pStream->Write(m_iBuildingDamageChange); // doc
	pStream->Write(m_iTotalPopulationLoss); // doc
	pStream->Write(m_iPopulationLoss); // doc

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
	pStream->Write(m_bMongolUP); // doc
	pStream->Write(m_bInvestigate); // advc.103
	pStream->Write(m_bChooseProductionDirty); // advc.003u

	pStream->Write(m_eOwner);
	pStream->Write(m_ePreviousCiv); // doc
	pStream->Write(m_eOriginalCiv); // doc
	pStream->Write(m_eCultureLevel);
	pStream->Write(m_eArtStyle); // doc
	pStream->Write(m_eNextCoveredPlot); // doc

	m_aiSeaPlotYield.write(pStream);
	m_aiRiverPlotYield.write(pStream);
    m_aiFlatRiverPlotYield.write(pStream); // doc
	m_aiBaseYieldRate.write(pStream);
	m_aiYieldRateModifier.write(pStream);
	m_aiPowerYieldRateModifier.write(pStream);
	m_aiBonusYieldRateModifier.write(pStream);
	m_aiTradeYield.write(pStream);
	m_aiCorporationYield.write(pStream);
	m_aiExtraSpecialistYield.write(pStream);
	m_aiCommerceRate.write(pStream);
	m_aiProductionToCommerceModifier.write(pStream);
	m_aiBuildingCommerce.write(pStream);
	m_aiSpecialistCommerce.write(pStream);
	m_aiReligionCommerce.write(pStream);
	m_aiCorporationCommerce.write(pStream);
    m_aiPowerCommerceRateModifier.write(pStream); // doc
    m_aiCultureCommerceRateModifier.write(pStream); // doc
    m_aiBonusCommerceRateModifier.write(pStream); // doc
	m_aiCommerceRateModifier.write(pStream);
	m_aiCommerceHappinessPer.write(pStream);
	m_aiDomainFreeExperience.write(pStream);
	m_aiDomainProductionModifier.write(pStream);
	m_aiCulture.write(pStream);
	m_aiNumRevolts.write(pStream);
    m_aiGameTurnCivLost.write(pStream); // doc
    m_aiCulturePlots.write(pStream); // doc
    m_aiCultureCosts.write(pStream); // doc

	m_abEverOwned.write(pStream);
	m_abTradeRoute.write(pStream);
	m_abRevealed.write(pStream);
	m_abEspionageVisibility.write(pStream);

	pStream->WriteString(m_szName);
	pStream->WriteString(m_szPreviousName); // advc.106k
	pStream->WriteString(m_szScriptData);

	m_aiNoBonus.write(pStream);
	m_aiFreeBonus.write(pStream);
	m_aiNumBonuses.write(pStream);
	m_aiNumCorpProducedBonuses.write(pStream);
	m_aiProjectProduction.write(pStream);
	m_aiBuildingProduction.write(pStream);
	m_aiBuildingProductionTime.write(pStream);
	m_aeBuildingOriginalOwner.write(pStream);
	m_aiBuildingOriginalTime.write(pStream);
	m_aiUnitProduction.write(pStream);
	m_aiUnitProductionTime.write(pStream);
	m_aiGreatPeopleUnitRate.write(pStream);
	m_aiGreatPeopleUnitProgress.write(pStream);
	m_aiSpecialistCount.write(pStream);
	m_aiMaxSpecialistCount.write(pStream);
	m_aiForceSpecialistCount.write(pStream);
	m_aiFreeSpecialistCount.write(pStream);
	m_aiImprovementFreeSpecialists.write(pStream);
	m_aiReligionInfluence.write(pStream);
	m_aiShrine.write(pStream); // advc.enum
	m_aiStateReligionHappiness.write(pStream);
	m_aiUnitCombatFreeExperience.write(pStream);
	m_aiFreePromotionCount.write(pStream);
	m_aiNumRealBuilding.write(pStream);
	m_aiNumFreeBuilding.write(pStream);

	m_abWorkingPlot.write(pStream);
	m_abHasReligion.write(pStream);
	m_abHasCorporation.write(pStream);

	for (size_t i = 0; i < m_aTradeCities.size(); i++)
	{
		pStream->Write(m_aTradeCities[i].eOwner);
		pStream->Write(m_aTradeCities[i].iID);
	}

	m_orderQueue.Write(pStream);
	/*	These caches are (or ought to be) reliably invalidated,
		don't need to be in-sync at all times. */
	REPRO_TEST_END_WRITE();
	pStream->Write(m_iPopulationRank);
	pStream->Write(m_bPopulationRankValid);
	m_aiBaseYieldRank.write(pStream);
	m_abBaseYieldRankValid.write(pStream);
	m_aiYieldRank.write(pStream);
	m_abYieldRankValid.write(pStream);
	m_aiCommerceRank.write(pStream);
	m_abCommerceRankValid.write(pStream);
	REPRO_TEST_BEGIN_WRITE(CvString::format("City(%d,%d) pt2", getX(), getY()));

    pStream->Write(m_hurriedUnits.size());
    for (std::vector< std::pair <UnitClassTypes, HurryTypes> >::iterator it = m_hurriedUnits.begin(); it != m_hurriedUnits.end(); ++it)
    {
        pStream->Write((int)(*it).first);
        pStream->Write((char)(*it).second);
    }

    pStream->Write(m_aEventsOccured.size());
	for (std::vector<EventTypes>::iterator it = m_aEventsOccured.begin();
		it != m_aEventsOccured.end(); ++it)
	{
		pStream->Write(*it);
	}

	m_aeiiBuildingYieldChange.write(pStream);
	m_aeiiBuildingCommerceChange.write(pStream);
	m_aeiBuildingHappyChange.write(pStream);
	m_aeiBuildingHealthChange.write(pStream);
	m_aeiiBonusYieldChange.write(pStream);
    m_aeiBuildingGreatPeopleRateChange.write(pStream);

	pStream->Write(m_iPopRushHurryCount); // advc.912d
	// <advc.004x>
	pStream->Write(m_iMostRecentOrder);
	pStream->Write(m_bMostRecentUnit); // </advc.004x>
	REPRO_TEST_END_WRITE();
}


class VisibleBuildingComparator
{
public:
	bool operator() (BuildingTypes e1, BuildingTypes e2)
	{
		if (GC.getInfo(e1).getVisibilityPriority() > GC.getInfo(e2).getVisibilityPriority())
			return true;
		else if (GC.getInfo(e1).getVisibilityPriority() == GC.getInfo(e2).getVisibilityPriority())
		{
			//break ties by building type higher building type
			if (e1 > e2)
				return true;
		}
		return false;
	}
};

/*	Fill the kVisible array with buildings that you want shown in city,
	as well as the number of generics
	This function is called whenever CvCity::setLayoutDirty() is called. */
void CvCity::getVisibleBuildings(std::list<BuildingTypes>& kChosenVisible,
	int& iChosenNumGenerics)
{
	// <advc.045>
	TeamTypes const eActiveTeam = GC.getGame().getActiveTeam();
	bool const bAllVisible = (eActiveTeam != NO_TEAM &&
			isAllBuildingsVisible(eActiveTeam, true)); // </advc.045>
	std::vector<BuildingTypes> kVisible;
	CvCivilization const& kCiv = getCivilization();
	for (int i = 0; i < kCiv.getNumBuildings(); i++)
	{
		BuildingTypes const eBuilding = kCiv.buildingAt(i);
		// <advc.045>
		if(getNumBuilding(eBuilding) <= 0)
			continue;
		// Copied these two checks from Rise of Mankind
		CvBuildingInfo const& kBuilding = GC.getInfo(eBuilding);
		bool const bWonder = kBuilding.isLimited();
		bool const bDefense = (kBuilding.getDefenseModifier() > 0 ||
				kBuilding.get(CvBuildingInfo::RaiseDefense) > 0); // advc.004c
		if (!bAllVisible && !bWonder && !bDefense)
		{
			bool bVisibleYieldChange = false;
			YieldChangeMap aiSeaPlotYieldChanges = kBuilding.getSeaPlotYieldChange();
			YieldChangeMap aiRiverPlotYieldChanges = kBuilding.getRiverPlotYieldChange();
			FOR_EACH_ENUM(Yield)
			{
				if(aiRiverPlotYieldChanges[eLoopYield] != 0 ||
					aiSeaPlotYieldChanges[eLoopYield] != 0)
				{
					bVisibleYieldChange = true;
					break;
				}
			}
			if(!bVisibleYieldChange)
				continue;
		} // </advc.045>
		kVisible.push_back(eBuilding);
	}

	// sort the visible ones by decreasing priority
	VisibleBuildingComparator kComp;
	std::sort(kVisible.begin(), kVisible.end(), kComp);

	// how big is this city, in terms of buildings?
	// general rule: no more than fPercentUnique percent of a city can be uniques
	int iTotalVisibleBuildings;
	if (::stricmp(GC.getDefineSTRING("GAME_CITY_SIZE_METHOD"), "METHOD_EXPONENTIAL") == 0)
	{
		int iCityScaleMod = (int)(std::pow((float)getPopulation(),
				GC.getDefineFLOAT("GAME_CITY_SIZE_EXP_MODIFIER")) * 2);
		iTotalVisibleBuildings = 10 + iCityScaleMod;
	}
	else
	{
		float fLo = GC.getDefineFLOAT("GAME_CITY_SIZE_LINMAP_AT_0");
		float fHi = GC.getDefineFLOAT("GAME_CITY_SIZE_LINMAP_AT_50");
		iTotalVisibleBuildings = (int)(((fHi - fLo) / 50.0f) * getPopulation() + fLo);
	}
	float fMaxUniquePercent = GC.getDefineFLOAT("GAME_CITY_SIZE_MAX_PERCENT_UNIQUE");
	int iMaxNumUniques = (int)(fMaxUniquePercent * iTotalVisibleBuildings);

	// compute how many buildings are generics vs. unique Civ buildings?
	int const iNumUniques = std::min((int)kVisible.size(), iMaxNumUniques);
	int const iNumGenerics = iTotalVisibleBuildings - iNumUniques + getCitySizeBoost();

	// return
	iChosenNumGenerics = iNumGenerics;
	for(int i = 0; i < iNumUniques; i++)
	{
		kChosenVisible.push_back(kVisible[i]);
	}
}

// advc.045:
bool CvCity::isAllBuildingsVisible(TeamTypes eTeam, bool bDebug) const
{
	if (bDebug && GC.getGame().isDebugMode())
		return true;
	if (GC.getDefineBOOL(CvGlobals::TREAT_REVEALED_BUILDINGS_AS_VISIBLE) &&
		isRevealed(eTeam, bDebug))
	{
		return true;
	}
	return (getTeam() == eTeam || getPlot().isInvestigate(eTeam) ||
			getPlot().plotCheck(NULL, -1, -1, NO_PLAYER, eTeam) > 0 != NULL);
}

// (advc: natGetDeterministicRandom deleted; should use 'hash' in CvGameCoreUtils instead.)

/*	Fill the kEffectNames array with references to effects in CIV4EffectInfos.xml
	to have a city play a given set of effects. This is called whenever the interface
	updates the city billboard or when the zoom level changes. */
void CvCity::getVisibleEffects(ZoomLevelTypes eCurZoom,
	std::vector<const TCHAR*>& kEffectNames)
{
	if (isOccupation() && isVisible(getTeam()) == true)
	{
		if (eCurZoom  == ZOOM_DETAIL)
		{
			kEffectNames.push_back("EFFECT_CITY_BIG_BURNING_SMOKE");
			kEffectNames.push_back("EFFECT_CITY_FIRE");
		}
		else kEffectNames.push_back("EFFECT_CITY_BIG_BURNING_SMOKE");
		return;
	}

	if (isActiveTeam() || GC.getGame().isDebugMode())
	{
		if (angryPopulation() > 0)
			kEffectNames.push_back("EFFECT_CITY_BURNING_SMOKE");

		if (healthRate() < 0)
			kEffectNames.push_back("EFFECT_CITY_DISEASED");

		if (isWeLoveTheKingDay())
		{	// <advc> Cut from deleted free function natGetDeterministicRandom
			srand(7297 * getX() + 2909  * getY());
			int iSeed = (rand() % 32767); // </advc>
			CvRandom kRand;
			kRand.init(iSeed);

			// fireworks
			static TCHAR const* szFireworkEffects[] = // advc: static
			{
				"FIREWORKS_RED_LARGE_SLOW",
				"FIREWORKS_RED_SMALL_FAST",
				"FIREWORKS_GREEN_LARGE_SLOW",
				"FIREWORKS_GREEN_SMALL_FAST",
				"FIREWORKS_PURPLE_LARGE_SLOW",
				"FIREWORKS_PURPLE_SMALL_FAST",
				"FIREWORKS_YELLOW_LARGE_SLOW",
				"FIREWORKS_YELLOW_SMALL_FAST",
				"FIREWORKS_BLUE_LARGE_SLOW",
				"FIREWORKS_BLUE_SMALL_FAST"
			};
			int const iNumEffects = ARRAYSIZE(szFireworkEffects);
			for (int i = 0; i < (iNumEffects < 3 ? iNumEffects : 3); i++)
			{
				kEffectNames.push_back(szFireworkEffects[kRand.get(iNumEffects)]);
			}
		}
	}
}


void CvCity::getCityBillboardSizeIconColors(NiColorA& kDotColor, NiColorA& kTextColor) const
{
	PlayerColorTypes const ePlayerColor = //GET_PLAYER(getOwner()).getPlayerColor())
		/*  advc.001: CvPlayer::getPlayerColor will return the Barbarian color
			if the city owner hasn't been met (city revealed through map trade) */
			GC.getInitCore().getColor(getOwner());
	NiColorA kPlayerColor = GC.getInfo(GC.getInfo(ePlayerColor).
			getColorTypePrimary()).getColor();
	NiColorA kGrowing(0.73f, 1,0.73f, 1);
	NiColorA kShrinking(1, 0.73f, 0.73f, 1);
	NiColorA kStagnant(0.83f, 0.83f, 0.83f, 1);
	NiColorA kUnknown(.5f, .5f, .5f, 1);
	NiColorA kWhite(1, 1, 1, 1);
	NiColorA kBlack(0, 0, 0, 1);

	/*if (isActiveTeam() // advc.127:
        && isHuman())
	{
		kTextColor = kBlack;
		int const iFoodDifference = foodDifference();
		int const iFood = getFood();
		int const iGrowthThreshold = growthThreshold();
		if (iFoodDifference < 0)
		{
			if (iFoodDifference == -1 && iFood * 100 >= 75 * iGrowthThreshold)
				kDotColor = kStagnant;
			else kDotColor = kShrinking;
		}
		else if (iFoodDifference > 0)
		{	// <advc.002f>
			if (AI().AI_isEmphasizeAvoidGrowth())
			{
				if (iFood + iFoodDifference >= iGrowthThreshold) // Food being wasted
					kDotColor = kShrinking;
				else kDotColor = kStagnant; // Food will be wasted - and not growing
			} // </advc.002f>
			else kDotColor = kGrowing;
		}
		else kDotColor = kStagnant;
	}
	else*/

    // rfc: disable conditional billboard color
	{
		kDotColor = kPlayerColor;
		NiColorA kPlayerSecondaryColor = GC.getInfo(
				GC.getInfo(ePlayerColor). // advc.001
				getColorTypeSecondary()).getColor();
		kTextColor = kPlayerSecondaryColor;
	}
}


const TCHAR* CvCity::getCityBillboardProductionIcon() const
{
	if (!canBeSelected() || !isProduction())
	{
		return ARTFILEMGR.getInterfaceArtInfo(
				"INTERFACE_BUTTONS_NOPRODUCTION")->getPath();
	}
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();
	TCHAR const* szIcon = NULL;
	switch (pOrderNode->m_data.eOrderType)
	{
	case ORDER_TRAIN:
	{
		UnitTypes eType = getProductionUnit();
		szIcon = GET_PLAYER(getOwner()).getUnitButton(eType);
		break;
	}
	case ORDER_CONSTRUCT:
	{
		BuildingTypes eType = getProductionBuilding();
		szIcon = GC.getInfo(eType).getButton();
		break;
	}
	case ORDER_CREATE:
	{
		ProjectTypes eType = getProductionProject();
		szIcon = GC.getInfo(eType).getButton();
		break;
	}
	case ORDER_MAINTAIN:
	{
		ProcessTypes eType = getProductionProcess();
		szIcon = GC.getInfo(eType).getButton();
		break;
	}
	default: FAssert(false);
	}
	return szIcon;
}


bool CvCity::getFoodBarPercentages(std::vector<float>& afPercentages) const
{
	if (!canBeSelected())
		return false;

	afPercentages.resize(NUM_INFOBAR_TYPES, 0.0f);
	if (foodDifference() < 0)
	{
		afPercentages[INFOBAR_STORED] = std::max(0, getFood() + foodDifference()) /
				(float)growthThreshold();
		afPercentages[INFOBAR_RATE_EXTRA] = std::min(-foodDifference(), getFood()) /
				(float)growthThreshold();
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
		return false;

	if (!isProductionProcess())
	{
		afPercentages.resize(NUM_INFOBAR_TYPES, 0.0f);
		int iProductionDiffNoFood = getCurrentProductionDifference(true, true);
		int iProductionDiffJustFood = getCurrentProductionDifference(false, true)
				- iProductionDiffNoFood;
		afPercentages[INFOBAR_STORED] = getProduction() / (float) getProductionNeeded();
		afPercentages[INFOBAR_RATE] = iProductionDiffNoFood / (float) getProductionNeeded();
		afPercentages[INFOBAR_RATE_EXTRA] = iProductionDiffJustFood / (float) getProductionNeeded();
	}

	return true;
}


NiColorA CvCity::getBarBackgroundColor() const
{
	if (::atWar(getTeam(), GC.getGame().getActiveTeam()))
		return NiColorA(0.5f, 0, 0, 0.5f); // red
	return NiColorA(0, 0, 0, 0.5f);
}


bool CvCity::isStarCity() const
{
	return isCapital();
}


int CvCity::getTriggerValue(EventTriggerTypes eTrigger) const
{
	if (!GC.getPythonCaller()->canTriggerEvent(*this, eTrigger))
		return MIN_INT;

	CvEventTriggerInfo& kTrigger = GC.getInfo(eTrigger);

	if (kTrigger.getNumBuildings() > 0 && kTrigger.getNumBuildingsRequired() > 0)
	{
		bool bFoundValid = false;
		for (int i = 0; i < kTrigger.getNumBuildingsRequired(); i++)
		{
			BuildingClassTypes eBuildingClass = (BuildingClassTypes)
					kTrigger.getBuildingRequired(i);
			if (eBuildingClass != NO_BUILDINGCLASS &&
				getNumRealBuilding(eBuildingClass) > 0) // advc.003w: simplified
			{
				bFoundValid = true;
				break;
			}
		}
		if (!bFoundValid)
			return MIN_INT;
	}


	if (getReligionCount() < kTrigger.getNumReligions())
		return MIN_INT;

	if (kTrigger.getNumReligions() > 0 && kTrigger.getNumReligionsRequired() > 0)
	{
		bool bFoundValid = false;
		for (int i = 0; i < kTrigger.getNumReligionsRequired(); i++)
		{
			if (!kTrigger.isStateReligion() ||
				kTrigger.getReligionRequired(i) == GET_PLAYER(getOwner()).getStateReligion())
			{
				ReligionTypes eReligion = (ReligionTypes)kTrigger.getReligionRequired(i);
				if (isHasReligion(eReligion))
				{
					if (!kTrigger.isHolyCity() || isHolyCity(eReligion))
						bFoundValid = true;
				}
			}
		}
		if (!bFoundValid)
			return MIN_INT;
	}

	if (getCorporationCount() < kTrigger.getNumCorporations())
		return MIN_INT;

	if (kTrigger.getNumCorporations() > 0 && kTrigger.getNumCorporationsRequired() > 0)
	{
		bool bFoundValid = false;
		for (int i = 0; i < kTrigger.getNumCorporationsRequired(); i++)
		{
			CorporationTypes eCorp = (CorporationTypes)kTrigger.getCorporationRequired(i);
			if (isHasCorporation(eCorp))
			{
				if (!kTrigger.isHeadquarters() || isHeadquarters(eCorp))
					bFoundValid = true;
			}
		}
		if (!bFoundValid)
			return MIN_INT;
	}

	if (kTrigger.getMinPopulation() > 0)
	{
		if (getPopulation() < kTrigger.getMinPopulation())
			return MIN_INT;
	}

	if (kTrigger.getMaxPopulation() > 0)
	{
		if (getPopulation() > kTrigger.getMaxPopulation())
			return MIN_INT;
	}

	if (kTrigger.getAngry() > 0)
	{
		if (unhappyLevel(0) - happyLevel() < kTrigger.getAngry())
			return MIN_INT;
	}
	else if (kTrigger.getAngry() < 0)
	{
		if (happyLevel() - unhappyLevel(0) < -kTrigger.getAngry())
			return MIN_INT;
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
			return MIN_INT;
	}

	if (kTrigger.isPrereqEventCity() && kTrigger.getNumPrereqEvents() > 0)
	{
		bool bFoundValid = true;

		for (int i = 0; i < kTrigger.getNumPrereqEvents(); i++)
		{
			if (!isEventOccured((EventTypes)kTrigger.getPrereqEvent(i)))
			{
				bFoundValid = false;
				break;
			}
		}
		if (!bFoundValid)
			return MIN_INT;
	}

	if (getFood() == 0 && kTrigger.getCityFoodWeight() > 0)
		return MIN_INT;
	return getFood() * kTrigger.getCityFoodWeight();
}


bool CvCity::canApplyEvent(EventTypes eEvent, const EventTriggeredData& kTriggeredData) const
{
	CvEventInfo& kEvent = GC.getInfo(eEvent);
    // doc: events cannot affect minors
    if (GET_PLAYER(getOwner()).isMinorCiv())
        return false;

	if (!kEvent.isCityEffect() && !kEvent.isOtherPlayerCityEffect())
		return true;

	if (kTriggeredData.m_iCityId == -1 && kEvent.isCityEffect())
		return false;

	if (kTriggeredData.m_iOtherPlayerCityId  == -1 && kEvent.isOtherPlayerCityEffect())
		return false;

	if (kEvent.getFood() + ((100 + kEvent.getFoodPercent()) * getFood()) / 100 < 0)
		return false;

	if (kEvent.getPopulationChange() + getPopulation() <= 0)
		return false;

	if (100 * kEvent.getCulture() + getCultureTimes100(getOwner()) < 0)
		return false;

	BuildingClassTypes const eBuildingClass = (BuildingClassTypes)kEvent.getBuildingClass();
	if (eBuildingClass != NO_BUILDINGCLASS)
	{
		BuildingTypes eBuilding = getCivilization().getBuilding(eBuildingClass);
		if (eBuilding == NO_BUILDING)
			return false;

		if (kEvent.getBuildingChange() > 0)
		{
			if (getNumBuilding(eBuilding) >= GC.getDefineINT(CvGlobals::CITY_MAX_NUM_BUILDINGS))
				return false;
		}
		else if (kEvent.getBuildingChange() < 0)
		{
			if (getNumRealBuilding(eBuilding) + kEvent.getBuildingChange() < 0)
				return false;
		}
	}

	if (kEvent.getMaxNumReligions() != -1 &&
		getReligionCount() > kEvent.getMaxNumReligions())
	{
		return false;
	}

	if (kEvent.getMinPillage() > 0)
	{
		int iNumImprovements = 0;
		for (CityPlotIter it(*this, false); it.hasNext(); ++it)
		{
			if (it->getOwner() == getOwner() && it->isImproved() &&
				!GC.getInfo(it->getImprovementType()).isPermanent())
			{
				iNumImprovements++;
			}
		}
		if (iNumImprovements < kEvent.getMinPillage())
			return false;
	}

	return true;
}


void CvCity::applyEvent(EventTypes eEvent,
	EventTriggeredData const& kTriggeredData, bool bClear)
{
	if (!canApplyEvent(eEvent, kTriggeredData))
		return;

	setEventOccured(eEvent, true);
	CvEventInfo const& kEvent = GC.getInfo(eEvent);
	if (kEvent.isCityEffect() || kEvent.isOtherPlayerCityEffect())
	{
		if (kEvent.getHappy() != 0)
			changeExtraHappiness(kEvent.getHappy());

		if (kEvent.getHealth() != 0)
			changeExtraHealth(kEvent.getHealth());

		if (kEvent.getHurryAnger() != 0)
			changeHurryAngerTimer(kEvent.getHurryAnger() * flatHurryAngerLength());

		if (kEvent.getHappyTurns() != 0)
            // doc: event happiness scales with game speed
			changeHappinessTimer(getTurns(kEvent.getHappyTurns()));

		if (kEvent.getFood() != 0 || kEvent.getFoodPercent() != 0)
			changeFood(kEvent.getFood() + (kEvent.getFoodPercent() * getFood()) / 100);

		if (kEvent.getPopulationChange() != 0)
			changePopulation(kEvent.getPopulationChange());

		if (kEvent.getRevoltTurns() > 0)
		{
			changeCultureUpdateTimer(kEvent.getRevoltTurns());
			changeOccupationTimer(kEvent.getRevoltTurns());
		}

		if (kEvent.getSpaceProductionModifier() != 0)
			changeSpaceProductionModifier(kEvent.getSpaceProductionModifier());

		if (kEvent.getMaxPillage() > 0)
		{
			FAssert(kEvent.getMaxPillage() >= kEvent.getMinPillage());
			int iNumPillage = kEvent.getMinPillage() +
					SyncRandNum(kEvent.getMaxPillage() - kEvent.getMinPillage());

			int iNumPillaged = 0;
			for (int i = 0; i < iNumPillage; i++)
			{
				int iRandOffset = SyncRandNum(NUM_CITY_PLOTS);
				FOR_EACH_ENUM(CityPlot)
				{
					CityPlotTypes const ePlot = (CityPlotTypes)
							((eLoopCityPlot + iRandOffset) % NUM_CITY_PLOTS);
					if (ePlot == CITY_HOME_PLOT)
						continue;
					CvPlot* pPlot = getCityIndexPlot(ePlot);
					if (pPlot == NULL || pPlot->getOwner() != getOwner())
						continue;
					if (pPlot->isImproved() &&
						!GC.getInfo(pPlot->getImprovementType()).isPermanent())
					{
						CvWString szBuffer = gDLL->getText(
								"TXT_KEY_EVENT_CITY_IMPROVEMENT_DESTROYED",
								GC.getInfo(pPlot->getImprovementType()).getTextKeyWide());
						gDLL->UI().addMessage(getOwner(), false, -1, szBuffer, *pPlot,
								"AS2D_PILLAGED", MESSAGE_TYPE_INFO,
								GC.getInfo(pPlot->getImprovementType()).getButton(),
								GC.getColorType("RED"));
						pPlot->setImprovementType(NO_IMPROVEMENT);
						iNumPillaged++;
						break;
					}
				}
			}

			PlayerTypes eOtherPlayer = kTriggeredData.m_eOtherPlayer;
			if (!kEvent.isCityEffect() && kEvent.isOtherPlayerCityEffect())
				eOtherPlayer = kTriggeredData.m_ePlayer;

			if (eOtherPlayer != NO_PLAYER)
			{
				CvWString szBuffer = gDLL->getText("TXT_KEY_EVENT_NUM_CITY_IMPROVEMENTS_DESTROYED",
						iNumPillaged, GET_PLAYER(getOwner()).getCivilizationAdjectiveKey());
				gDLL->UI().addMessage(eOtherPlayer, false, -1, szBuffer,
						"AS2D_PILLAGED", MESSAGE_TYPE_INFO);
			}
		}

		FOR_EACH_ENUM(Specialist)
		{
			if (kEvent.getFreeSpecialistCount(eLoopSpecialist) > 0)
			{
				changeFreeSpecialistCount(eLoopSpecialist,
						kEvent.getFreeSpecialistCount(eLoopSpecialist));
			}
		}
		if (kEvent.getCulture() != 0)
			changeCulture(getOwner(), kEvent.getCulture(), true, true);
	}
	{
		UnitClassTypes eUnitClass = (UnitClassTypes)kEvent.getUnitClass(); // advc
		if (eUnitClass != NO_UNITCLASS)
		{
			UnitTypes eUnit = getCivilization().getUnit(eUnitClass);
			if (eUnit != NO_UNIT)
			{
				for (int i = 0; i < kEvent.getNumUnits(); i++)
				{
					GET_PLAYER(getOwner()).initUnit(eUnit, getX(), getY());
				}
			}
		}
	}
	{
		BuildingClassTypes eBuildingClass = (BuildingClassTypes)kEvent.getBuildingClass(); // advc
		if (eBuildingClass != NO_BUILDINGCLASS)
		{
			BuildingTypes eBuilding = getCivilization().getBuilding(eBuildingClass);
			if (eBuilding != NO_BUILDING)
			{
				if (kEvent.getBuildingChange() != 0)
				{
					setNumRealBuilding(eBuilding, getNumRealBuilding(eBuilding) +
							kEvent.getBuildingChange());
				}
			}
		}
	}
	FOR_EACH_NON_DEFAULT_PAIR(kEvent.
		getBuildingYieldChange(), BuildingClass, YieldChangeMap)
	{
		FOR_EACH_NON_DEFAULT_PAIR(perBuildingClassVal.second, Yield, int)
		{
			changeBuildingYieldChange(perBuildingClassVal.first,
					perYieldVal.first, perYieldVal.second);
		}
	}
	FOR_EACH_NON_DEFAULT_PAIR(kEvent.
		getBuildingCommerceChange(), BuildingClass, CommerceChangeMap)
	{
		FOR_EACH_NON_DEFAULT_PAIR(perBuildingClassVal.second, Commerce, int)
		{
			changeBuildingCommerceChange(perBuildingClassVal.first,
					perCommerceVal.first, perCommerceVal.second);
		}
	}
	FOR_EACH_NON_DEFAULT_PAIR(kEvent.getBuildingHappyChange(), BuildingClass, int)
	{
		setBuildingHappyChange(perBuildingClassVal.first, perBuildingClassVal.second);
	}
	FOR_EACH_NON_DEFAULT_PAIR(kEvent.getBuildingHealthChange(), BuildingClass, int)
	{
		setBuildingHealthChange(perBuildingClassVal.first, perBuildingClassVal.second);
	}

	if (bClear)
	{
		FOR_EACH_ENUM(Event)
			setEventOccured(eLoopEvent, false);
	}
}


bool CvCity::isEventOccured(EventTypes eEvent) const
{
	for (size_t i = 0; i < m_aEventsOccured.size(); i++)
	{
		if (m_aEventsOccured[i] == eEvent)
			return true;
	}
	return false;
}


void CvCity::setEventOccured(EventTypes eEvent, bool bOccured)
{
	for (std::vector<EventTypes>::iterator it = m_aEventsOccured.begin();
		it != m_aEventsOccured.end(); ++it)
	{
		if (*it == eEvent)
		{
			if (!bOccured)
				m_aEventsOccured.erase(it);
			return;
		}
	}
	if (bOccured)
		m_aEventsOccured.push_back(eEvent);
}

// advc.003y: Ported from CvEventManager.py; Python code there deleted.
void CvCity::doPartisans()
{
	if (GC.getGame().isOption(GAMEOPTION_NO_EVENTS))
		return;
	/*	(advc.001: The population check in CvEventManager had had no effect b/c of a typo.
		Note that population loss from conquest will have already occurred when razing.) */
	if (getPopulation() <= 1 || isBarbarian())
		return;
	// advc: Was based on city culture instead of plot culture
	PlayerTypes eHighestCulturePlayer = getPlot().findHighestCulturePlayer();
	if (eHighestCulturePlayer == getOwner() || eHighestCulturePlayer == BARBARIAN_PLAYER)
		return;
	CvPlayer& kPartisanPlayer = GET_PLAYER(eHighestCulturePlayer);
	// advc.099: alive check
	if (!kPartisanPlayer.isAlive() || kPartisanPlayer.getNumCities() <= 0)
		return;
	if (!::atWar(getTeam(), kPartisanPlayer.getTeam()))
		return;
	// advc: Important now that getNumPartisanUnits subtracts 1 from the culture level
	if (getNumPartisanUnits(kPartisanPlayer.getID()) <= 0)
		return;

	EventTriggerTypes eTrigger = (EventTriggerTypes)GC.getInfoTypeForString("EVENTTRIGGER_PARTISANS");
	FAssert(eTrigger != NO_EVENTTRIGGER);
	if (!GC.getGame().isEventActive(eTrigger) ||
		/*  Non-negative probability means, apparently, that the event is
			not supposed to be triggered manually like this. */
		kPartisanPlayer.getEventTriggerWeight(eTrigger) >= 0)
	{
		return;
	}
	kPartisanPlayer.initTriggeredData(eTrigger, /*bFire=*/true, -1, getX(), getY(), getOwner(), getID());
}

/*	advc.003y: Ported from CvRandomEventInterface.py; Python code there deleted.
	Subtracting 1 is an idea by CFC user SmokeyTheBear. It means e.g. that 0 units
	appear when culture is "poor". */
int CvCity::getNumPartisanUnits(PlayerTypes ePartisanPlayer) const
{
	// advc.001: The culture level computation in Python was erroneous
	return std::max(0, calculateCultureLevel(ePartisanPlayer) - 1);
}


void CvCity::invalidateYieldRankCache(YieldTypes eYield)
{
	if (eYield == NO_YIELD)
	{
		FOR_EACH_ENUM(Yield)
		{
			m_abBaseYieldRankValid.set(eLoopYield, false);
			m_abYieldRankValid.set(eLoopYield, false);
		}
	}
	else
	{
		m_abBaseYieldRankValid.set(eYield, false);
		m_abYieldRankValid.set(eYield, false);
	}
}


void CvCity::invalidateCommerceRankCache(CommerceTypes eCommerce)
{
	if (eCommerce == NO_COMMERCE)
	{
		FOR_EACH_ENUM(Commerce)
			m_abCommerceRankValid.set(eLoopCommerce, false);
	}
	else m_abCommerceRankValid.set(eCommerce, false);
}


void CvCity::setBuildingYieldChange(BuildingClassTypes eBuildingClass,
	YieldTypes eYield, int iChange)
{
	BuildingTypes eBuilding = getCivilization().getBuilding(eBuildingClass); // advc.003w
	// advc: Simplified this function a lot
	if (eBuilding == NO_BUILDING)
		return;
	int const iOldChange = m_aeiiBuildingYieldChange.get(eBuildingClass, eYield);
	if (iOldChange == iChange)
		return;
	m_aeiiBuildingYieldChange.set(eBuildingClass, eYield, iChange);
	if (getNumActiveBuilding(eBuilding) > 0)
	{
		changeBaseYieldRate(eYield,
				(iChange - iOldChange) * getNumActiveBuilding(eBuilding));
	}
}


void CvCity::changeBuildingYieldChange(BuildingClassTypes eBuildingClass,
	YieldTypes eYield, int iChange)
{
	setBuildingYieldChange(eBuildingClass, eYield,
			getBuildingYieldChange(eBuildingClass, eYield) + iChange);
}


void CvCity::setBuildingCommerceChange(BuildingClassTypes eBuildingClass,
	CommerceTypes eCommerce, int iChange)
{	// advc: Simplified this function a lot
	BuildingTypes eBuilding = getCivilization().getBuilding(eBuildingClass);
	if (eBuilding == NO_BUILDING)
		return;
	int const iOldChange = m_aeiiBuildingCommerceChange.get(eBuildingClass, eCommerce);
	if (iOldChange == iChange)
		return;
	m_aeiiBuildingCommerceChange.set(eBuildingClass, eCommerce, iChange);
	if (getNumActiveBuilding(eBuilding) > 0)
		updateBuildingCommerce(/* advc.opt: */ eCommerce);
}

// TODO: removed doc updatebuildingcommercechange


void CvCity::changeBuildingCommerceChange(BuildingClassTypes eBuildingClass,
	CommerceTypes eCommerce, int iChange)
{
	setBuildingCommerceChange(eBuildingClass, eCommerce,
			getBuildingCommerceChange(eBuildingClass, eCommerce) + iChange);
}


void CvCity::setBuildingHappyChange(BuildingClassTypes eBuildingClass, int iChange)
{
	BuildingTypes eBuilding = getCivilization().getBuilding(eBuildingClass); // advc.003w
	// advc: Simplified this function a lot
	int const iOldChange = m_aeiBuildingHappyChange.get(eBuildingClass);
	if (iOldChange == iChange)
		return;
	m_aeiBuildingHappyChange.set(eBuildingClass, iChange);
	/*	UNOFFICIAL_PATCH (Bugfix), 10/22/09, jdog5000: START
		(advc: BtS code deleted) */
	if (getNumActiveBuilding(eBuilding) > 0)
	{
		if (iOldChange > 0)
			changeBuildingGoodHappiness(-iOldChange);
		else if (iOldChange < 0)
			changeBuildingBadHappiness(-iOldChange);
		if (iChange > 0)
			changeBuildingGoodHappiness(iChange);
		else if (iChange < 0)
			changeBuildingBadHappiness(iChange);
	} // UNOFFICIAL_PATCH: END
}


void CvCity::setBuildingHealthChange(BuildingClassTypes eBuildingClass, int iChange)
{
	BuildingTypes eBuilding = getCivilization().getBuilding(eBuildingClass); // advc.003w
	// advc: Simplified this function a lot
	int const iOldChange = m_aeiBuildingHealthChange.get(eBuildingClass);
	if (iOldChange == iChange)
		return;
	m_aeiBuildingHealthChange.set(eBuildingClass, iChange);
	/*	UNOFFICIAL_PATCH (Bugfix), 10/22/09, jdog5000: START
		(advc: BtS code deleted) */
	if (getNumActiveBuilding(eBuilding) > 0)
	{
		if (iOldChange > 0)
			changeBuildingGoodHealth(-iOldChange);
		else if (iOldChange < 0)
			changeBuildingBadHealth(-iOldChange);
		if (iChange > 0)
			changeBuildingGoodHealth(iChange);
		else if (iChange < 0)
			changeBuildingBadHealth(iChange);
	} // UNOFFICIAL_PATCH: END
}

// advc.071:
void CvCity::meetNewOwner(TeamTypes eOtherTeam, TeamTypes eNewOwner) const
{
	if (!isRevealed(eOtherTeam) || GET_TEAM(eOtherTeam).isHasMet(eNewOwner))
		return;
	FirstContactData fcData;
	fcData.x1 = getX();
	fcData.y1 = getY();
	GET_TEAM(eOtherTeam).meet(eNewOwner, true, &fcData);
}


void CvCity::liberate(bool bConquest, /* advc.ctr: */ bool bPeaceDeal)
{
	PlayerTypes ePlayer = getLiberationPlayer(bConquest);
	if(ePlayer == NO_PLAYER)
		return; // advc
	// kekm.23: No longer used
	/*CvPlot* pPlot = plot();
	int iOldOwnerCulture = getCultureTimes100(getOwner());
	bool bPreviouslyOwned = isEverOwned(ePlayer);*/ // K-Mod, for use below
	int iOldMasterLand = 0;
	int iOldVassalLand = 0;
    PlayerTypes eOwner = getOwner(); // doc
	CvTeam& kLiberationTeam = GET_TEAM(ePlayer); // advc

    // doc: release to independent with fewest cities
    if (ePlayer == NO_PLAYER)
    {
        for (PlayerIter<ALIVE> it; it.hasNext(); ++it)
        {
            if (it->isIndependent())
            {
                if (ePlayer == NO_PLAYER || it->getNumCities() < GET_PLAYER(ePlayer).getNumCities())
                    ePlayer = it->getID();
            }
        }
    }

	if (kLiberationTeam.isVassal(getTeam()))
	{
		iOldMasterLand = GET_TEAM(getTeam()).getTotalLand();
		iOldVassalLand = std::max(10, // advc.112: Lower bound added
				kLiberationTeam.getTotalLand(false));
	}

	CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_CITY_LIBERATED", getNameKey(),
			GET_PLAYER(getOwner()).getNameKey(),
			GET_PLAYER(ePlayer).getCivilizationAdjectiveKey());
	for (PlayerIter<MAJOR_CIV> it; it.hasNext(); ++it)
	{
		CvPlayer const& kObs = *it;
		// advc.071: Meet before the announcement (with indicator at city coordinates)
		meetNewOwner(kObs.getTeam(), TEAMID(ePlayer));
		if (isRevealed(kObs.getTeam()) /* advc.127: */ || kObs.isSpectator())
		{
			gDLL->UI().addMessage(kObs.getID(), false, -1, szBuffer, getPlot(),
					"AS2D_REVOLTEND",
					MESSAGE_TYPE_MAJOR_EVENT_LOG_ONLY, // advc.106b
					ARTFILEMGR.getInterfaceArtPath("WORLDBUILDER_CITY_EDIT"),
					GC.getColorType("HIGHLIGHT_TEXT"));
		}
	}
	GC.getGame().addReplayMessage(getPlot(), REPLAY_MESSAGE_MAJOR_EVENT,
			getOwner(), szBuffer, GC.getColorType("HIGHLIGHT_TEXT"));
	// <advc.ctr>
	if (!bPeaceDeal)
		GET_PLAYER(ePlayer).AI_rememberLiberation(*this, bConquest); // </advc.ctr>

    CvEventReporter::getInstance().cityLost(this); // doc

	GET_PLAYER(ePlayer).acquireCity(this, false, true, true);

	if (kLiberationTeam.isVassal(getTeam()))
	{
		int iNewMasterLand = GET_TEAM(getTeam()).getTotalLand();
		int iNewVassalLand = std::max(10, // advc.112: Lower bound added
				kLiberationTeam.getTotalLand(false));

		kLiberationTeam.setMasterPower(kLiberationTeam.getMasterPower() +
				iNewMasterLand - iOldMasterLand);
		kLiberationTeam.setVassalPower(kLiberationTeam.getVassalPower() +
				iNewVassalLand - iOldVassalLand);
	}
	GET_PLAYER(ePlayer).AI_updateAttitude(getOwner()); // advc.ctr
	// kekm.23: setCulture now done by advc.ctr in acquireCity
	/*if (NULL != pPlot) {
		CvCity* pCity = pPlot->getPlotCity();
		if (NULL != pCity) {
			// K-Mod, 7/jan/11:
			// This mechanic was exploitable. Players could increase their culture indefinitely in a single turn by gifting cities backwards and forwards.
			// I've attempted to close the exploit.
			if (!bPreviouslyOwned)
				pCity->setCultureTimes100(ePlayer, pCity->getCultureTimes100(ePlayer) + iOldOwnerCulture / 2, true, true);
			// K-Mod end
		}
		if (kLiberationTeam.isAVassal()) {
			for (int i = 0; i < GC.getDefineINT("COLONY_NUM_FREE_DEFENDERS"); ++i)
				pCity->initConscriptedUnit();
		}
	}*/

    // doc: global population affects maintenance
    GET_PLAYER(eOwner).updateMaintenance();
}


PlayerTypes CvCity::getLiberationPlayer(bool bConquest) const  // advc: refactoring changes
{
	PROFILE_FUNC(); // advc: Fine so far; not frequently called.
	if (isCapital())
		return NO_PLAYER;

	CvPlayer const& kOwner = GET_PLAYER(getOwner());

	for (PlayerIter<MAJOR_CIV> it; it.hasNext(); ++it)
	{
		CvPlayer& kLoopPlayer = *it;
		if (kLoopPlayer.getParent() == kOwner.getID())
		{
			if (kLoopPlayer.hasCapital())
			{
				if (sameArea(*kLoopPlayer.getCapital()))
					return kLoopPlayer.getID();
			}
		}
	}

	// advc: This is pointless b/c the splitEmpirePlayer is never alive
	/*if (kOwner.canSplitEmpire() && kOwner.canSplitArea(getArea())) {
		PlayerTypes eSplitPlayer = kOwner.getSplitEmpirePlayer(getArea());
		if (eSplitPlayer != NO_PLAYER && GET_PLAYER(eSplitPlayer).isAlive())
			return eSplitPlayer;
	}*/

	PlayerTypes eBestPlayer = NO_PLAYER;
	int iBestValue = 25; // doc: require minimal culture
	int const iTotalCityCultureTimes100 = countTotalCultureTimes100();
	// K-Mod - Base culture which is added to dilute the true culture values
	int const iBaseCulture = (GC.getNumCultureLevelInfos() <= 1 ? 100 :
			50 * GC.getInfo((CultureLevelTypes)1).getSpeedThreshold(GC.getGame().getGameSpeedType()));
	// K-Mod end

	// advc.ctr (comment): I guess liberation to a minor civ would be OK // doc: handle minors separately
	for (PlayerIter<MAJOR_CIV> it; it.hasNext(); ++it)
	{
		CvPlayer const& kLoopPlayer = *it;
		// K-Mod. I've flattened the if blocks into if! continue conditions.
		if (!kLoopPlayer.canReceiveTradeCity())
			continue;
		/*  <advc.ctr> The iBaseCulture term added by K-Mod had allowed liberation
			at culture level 0, i.e. to players who never owned the city. */
		if (!isEverOwned(kLoopPlayer.getID()))
			continue; // </advc.ctr>
		int iCapitalDistance = -1;
		{
			CvCity* pCapital = kLoopPlayer.getCapital();
			if (pCapital == NULL)
				continue;
			iCapitalDistance = ::plotDistance(getX(), getY(),
					pCapital->getX(), pCapital->getY());
			if (!sameArea(*pCapital))
				iCapitalDistance *= 2;
		}
		int iCultureScore = getCultureTimes100(kLoopPlayer.getID()) /* K-Mod: */ + iBaseCulture;
		if (bConquest && isOriginalOwner(kLoopPlayer.getID()))
		{
			iCultureScore *= 3;
			iCultureScore /= 2;
		}
		if (kLoopPlayer.getTeam() == getTeam() ||
			GET_TEAM(kLoopPlayer.getTeam()).isVassal(getTeam()) ||
			GET_TEAM(getTeam()).isVassal(kLoopPlayer.getTeam()))
		{
			// K-Mod: I don't see why the total culture should be used in this way. (I haven't changed anything)
			/*iCultureTimes100 *= 2;
			iCultureTimes100 = (iCultureTimes100 + iTotalCultureTimes100) / 2;*/
			/*  advc: Simplified (no functional change). I guess this is a sort of
				50% bonus for non-rivals. */
			iCultureScore += iTotalCityCultureTimes100 / 2;
		}
		// K-Mod - adjust culture score based on plot ownership.
		iCultureScore *= 100 + getPlot().calculateTeamCulturePercent(kLoopPlayer.getTeam());
		iCultureScore /= 100;
		// K-Mod end

		//int iValue = std::max(100, iCultureTimes100) / std::max(1, iCapitalDistance);
		int iValue = iCultureScore / std::max(1, iCapitalDistance); // K-Mod (minimum culture moved higher up)

        // doc: core value
		if (getPlot().isCore())
			iValue *= 3;
		// doc: settler value
		else if (getPlot().getSettlerValue(getOwner()) > 0)
			iValue *= 2;

        if (iValue > iBestValue)
		{
			iBestValue = iValue;
			eBestPlayer = kLoopPlayer.getID();
		}
	}

	if (eBestPlayer != NO_PLAYER)
	{
		if (kOwner.getID() == eBestPlayer)
			return NO_PLAYER;
	}

	return eBestPlayer;
}

// advc.003j: Unused since karadoc rewrote CvCityAI::AI_yieldValue
/*int CvCity::getBestYieldAvailable(YieldTypes eYield) const
{
	// ... (body deleted)
}*/


bool CvCity::isAutoRaze(/* <advc> */ PlayerTypes eConqueror) const
{
	CvPlayer const& kAssumedOwner = GET_PLAYER(eConqueror == NO_PLAYER ?
			getOwner() : eConqueror);
    // doc: cannot raze holy cities
	if (kAssumedOwner.isOneCityChallenge()) // </advc>
		return true;
	if (GC.getGame().isOption(GAMEOPTION_NO_CITY_RAZING))
		return false;
	if (GC.getGame().getMaxCityElimination() > 0)
		return true;
	if (getHighestPopulation() == 1)
		return true;
	return false;
}


int CvCity::getMusicScriptId() const
{
	bool bHappy = true;
	if (isActiveTeam())
	{
		if (angryPopulation() > 0)
			bHappy = false;
	}
	else
	{
		if (GET_TEAM(GC.getGame().getActiveTeam()).isAtWar(getTeam()))
			bHappy = false;
	}
	CvLeaderHeadInfo const& kLeaderInfo = GC.getInfo(GET_PLAYER(getOwner()).getLeaderType());
	EraTypes eCurEra = GET_PLAYER(getOwner()).getCurrentEra();
	if (bHappy)
		return (kLeaderInfo.getDiploPeaceMusicScriptIds(eCurEra));
	return (kLeaderInfo.getDiploWarMusicScriptIds(eCurEra));
}


int CvCity::getSoundscapeScriptId() const
{
	return	// advc.002q:
			(!BUGOption::isEnabled("CityScreen__CitySoundScapes", true) ? -1 :
			GC.getInfo(GET_PLAYER(getOwner()).getCurrentEra()).
			getCitySoundscapeScriptId(getCitySizeType()));
}


void CvCity::cheat(bool bCtrl, bool bAlt, bool bShift)
{
	//if (gDLL->getChtLvl() > 0)
	if(GC.getGame().isDebugMode()) // advc.007b
	{
		if (bCtrl)
			changeCulture(getOwner(), 10, true, true);
		else if (bShift)
			changePopulation(1);
		else
		{
			popOrder(0, true,
					NONE_CHOOSE, // advc.001x
					false);
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
			astrQueue.push_back(GC.getInfo((UnitTypes)pNode->m_data.iData1).getType());
			break;
		case ORDER_CONSTRUCT:
			astrQueue.push_back(GC.getInfo((BuildingTypes)pNode->m_data.iData1).getType());
			break;
		case ORDER_CREATE:
			astrQueue.push_back(GC.getInfo((ProjectTypes)pNode->m_data.iData1).getType());
			break;
		case ORDER_MAINTAIN:
			astrQueue.push_back(GC.getInfo((ProcessTypes)pNode->m_data.iData1).getType());
			break;
		default:
			FAssert(false);
		}
		pNode = nextOrderQueueNode(pNode);
	}
}

// <advc.004b> See CvCity.h
int CvCity::initialPopulation()
{
	return GC.getDefineINT("INITIAL_CITY_POPULATION") +
			GC.getInfo(GC.getGame().getStartEra()).getFreePopulation();
}

// advc.004b, advc.104: Parameters added
int CvCity::calculateDistanceMaintenanceTimes100(CvPlot const& kCityPlot,
	PlayerTypes eOwner, int iPopulation, bool bNoPlayerModifiers)
{
	if(iPopulation < 0)
		iPopulation = initialPopulation();
	/*CvCity* pLoopCity;
	int iWorstCityMaintenance;
	int iBestCapitalMaintenance;
	int iTempMaintenance;
	int iLoop;
	iWorstCityMaintenance = 0;
	iBestCapitalMaintenance = MAX_INT;
	for (pLoopCity = GET_PLAYER(getOwner()).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER(getOwner()).nextCity(&iLoop))
		iTempMaintenance = 100 * (GC.getDefineINT("MAX_DISTANCE_CITY_MAINTENANCE") *
				plotDistance(getX(), getY(), pLoopCity->getX(), pLoopCity->getY()));*/ // BtS
	// <K-Mod> 17/dec/10 - improved efficiency
	int iTempMaintenance = 100 *
			/*	advc (note): MAX_DISTANCE_CITY_MAINTENANCE is named a bit misleadingly.
				It's simply a (multiplicative) factor. The ratio of maintenance distance to
				maxTypicalDistance can be regarded as another factor, normally between 0 and 1.
				Insofar, MAX_DISTANCE_CITY_MAINTENANCE is the maximal result of multiplying
				those two factors. */
			GC.getDefineINT(CvGlobals::MAX_DISTANCE_CITY_MAINTENANCE) *
			// K-Mod: Moved the search for maintenance distance to a separate function
			calculateMaintenanceDistance(&kCityPlot, eOwner);
	{
		iTempMaintenance *= (iPopulation + 7);
		iTempMaintenance /= 10;
		if (!bNoPlayerModifiers) // advc
		{
			iTempMaintenance *= std::max(0, GET_PLAYER(eOwner).
					getDistanceMaintenanceModifier() + 100);
			iTempMaintenance /= 100;
			iTempMaintenance *= GC.getInfo(GET_PLAYER(eOwner).
					getHandicapType()).getDistanceMaintenancePercent();
			iTempMaintenance /= 100;
		}
		iTempMaintenance *= GC.getInfo(GC.getMap().getWorldSize()).getDistanceMaintenancePercent();
		iTempMaintenance /= 100;
		iTempMaintenance /= GC.getMap().maxTypicalDistance(); // advc.140: was maxPlotDistance
	}
	/*iWorstCityMaintenance = std::max(iWorstCityMaintenance, iTempMaintenance);
		if (pLoopCity->isGovernmentCenter())
			iBestCapitalMaintenance = std::min(iBestCapitalMaintenance, iTempMaintenance);
	}
	iTempMaintenance = std::min(iWorstCityMaintenance, iBestCapitalMaintenance);*/ // BtS
	// </K-Mod>
	FAssert(iTempMaintenance >= 0);
	return iTempMaintenance;
}

// K-Mod. new function to help with maintenance calculations
// advc.004b, advc.104: Parameters added
int CvCity::calculateMaintenanceDistance(CvPlot const* pCityPlot, PlayerTypes eOwner)
{
	int iLongestDist = 0;
	int iShortestGovernment = MAX_INT;
	FOR_EACH_CITY(pLoopCity, GET_PLAYER(eOwner))
	{
		int iDist = plotDistance(pCityPlot, pLoopCity->plot());
		iLongestDist = std::max(iLongestDist, iDist);
		if(pLoopCity->isGovernmentCenter())
			iShortestGovernment = std::min(iShortestGovernment, iDist);
	}
	int iR = std::min(iLongestDist, iShortestGovernment);
	// <advc.140> Upper bound added
	int iCap = GC.getMap().maxMaintenanceDistance();
	return std::min(iR, iCap); // </advc.140>
}

// advc.004b, advc.104: Parameters added
int CvCity::calculateNumCitiesMaintenanceTimes100(
	CvPlot const& kCityPlot, // (unused - not relevant for NumCitiesMaintenance)
	PlayerTypes eOwner, int iPopulation, int iExtraCities)
{
	if(iPopulation < 0)
		iPopulation = initialPopulation();

	scaled rNumCitiesFactor = 1;

	rNumCitiesFactor.mulDiv(iPopulation + 17, 18);

	CvWorldInfo const& kWorld = GC.getInfo(GC.getMap().getWorldSize());
	rNumCitiesFactor *= per100(kWorld.getNumCitiesMaintenancePercent());

	CvPlayer const& kOwner = GET_PLAYER(eOwner);

	// doc
	rNumCitiesFactor *= per100(kOwner.getModifier(MODIFIER_CITIES_MAINTENANCE));

	// doc: population maintenance
	int iTotalPopulation = kOwner.getTotalPopulation();
	int iThreshold = 10 * (6 + 2 * kOwner.getCurrentEra()) * kOwner.getNumCities();

	if (iTotalPopulation - iThreshold > 0)
	{
		int iPercentage = (100 * (iTotalPopulation - iThreshold) / iThreshold - 100) / 10;
		rNumCitiesFactor *= per100(100 + 10 * iPercentage);
	}

	rNumCitiesFactor *= per100(GC.getInfo(kOwner.getHandicapType()).
			getNumCitiesMaintenancePercent());
	// <advc.140>
	scaled rCrowdednessFactor(GC.getGame().getCivPlayersEverAlive(),
			GC.getGame().getRecommendedPlayers());
	rNumCitiesFactor *= rCrowdednessFactor.sqrt(); // </advc.140>

	int iNumVassalCities = 0;
	for (PlayerIter<ALIVE,VASSAL_OF> it(kOwner.getTeam()); it.hasNext(); ++it)
		iNumVassalCities += it->getNumCities();
	iNumVassalCities /= std::max(1, MemberIter::count(kOwner.getTeam()));
	int iMaintenanceCities = kOwner.getNumCities() + iExtraCities +
			// K-Mod, 04/sep/10: Reduced vassal maintenance
			iNumVassalCities / 2;
    // doc: disable all maintenance limits
    // TODO: disable by XML instead?
	// K-Mod: Removed maintenance cap  // advc.exp: I've disabled it through XML instead
	//scaled rMaxMaintenanceCities = GC.getInfo(GET_PLAYER(eOwner).getHandicapType()).
	//		getMaxNumCitiesMaintenance();
	// <advc.exp.1> Upper bound set through GlobalDefines
	//static int const iMAX_CITY_COUNT_FOR_MAINTENANCE = GC.getDefineINT("MAX_CITY_COUNT_FOR_MAINTENANCE");
	//rMaxMaintenanceCities.decreaseTo(scaled(iMAX_CITY_COUNT_FOR_MAINTENANCE) /
	//		(1 + per100(kWorld.getNumCitiesMaintenancePercent())));
	//iMaintenanceCities = std::min(iMaintenanceCities, rMaxMaintenanceCities.round());
	// </advc.exp.1>
    scaled rNumCitiesMaintenance = iMaintenanceCities * rNumCitiesFactor;

    // rfc: city size modifier
    rNumCitiesMaintenance *= per100(10 * (iPopulation + 9));

    // doc: large empire penalty
    int iSizeThreshold = 6 + 3 * kOwner.getCurrentEra();
    int iMultiplier = 3;
    int iEmpireSize = std::min(kOwner.getNumCities(), kOwner.getTotalPopulation() / iSizeThreshold);

    if (iEmpireSize > 16)
        rNumCitiesMaintenance *= per100(100 + iMultiplier * (kOwner.getNumCities() - 16));

	rNumCitiesMaintenance *= per100(std::max(0, kOwner.getNumCitiesMaintenanceModifier() + 100));
	FAssert(rNumCitiesMaintenance >= 0);
	return rNumCitiesMaintenance.getPercent();
}

// advc.004b, advc.104: Parameters added
int CvCity::calculateColonyMaintenanceTimes100(CvPlot const& kCityPlot,
	PlayerTypes eOwner, int iPopulation, int iExtraCities)
{
	if(iPopulation < 0)
		iPopulation = initialPopulation();
	HandicapTypes const eOwnerHandicap = GET_PLAYER(eOwner).getHandicapType();
	CvArea const& kCityArea = kCityPlot.getArea();

	if (GC.getGame().isOption(GAMEOPTION_NO_VASSAL_STATES))
		return 0;
	{
		CvCity* pCapital = GET_PLAYER(eOwner).getCapital();
        // doc: use overseas definition
		if (pCapital != NULL && !kCityPlot.isOverseas(pCapital->getPlot()))
			return 0;
	}

    // doc: no colony maintenance for single city areas
    if (kCityArea.getNumCities() == 1)
        return 0;

    // doc: not for minor civs
    if (GET_PLAYER(eOwner).isMinorCiv())
        return 0;

	int iNumCitiesPercent = 100;

	iNumCitiesPercent *= (iPopulation + 17);
	iNumCitiesPercent /= 18;

	iNumCitiesPercent *= GC.getInfo(eOwnerHandicap).getColonyMaintenancePercent();
	iNumCitiesPercent /= 100;

    int iNumCities = kCityArea.getCitiesPerPlayer(eOwner) + iExtraCities;

    // doc: English UP: reduced colony maintenance scaling
    if (GET_PLAYER(eOwner).getCivilizationType() == ENGLAND)
        iNumCities -= 1;

    iNumCities *= iNumCitiesPercent;

	int iMaintenance = SQR(iNumCities) / 100;
	//iMaintenance = std::min(iMaintenance, (GC.getInfo(getHandicapType()).getMaxColonyMaintenance() * calculateDistanceMaintenanceTimes100()) / 100);
	/*  K-Mod, 17/dec/10: Changed colony maintenance cap to not include
		distance maintenance modifiers (such as state property) */
	// advc: Let's do that without duplicating code
	int iMaintenanceCap = GC.getDefineINT(CvGlobals::MAX_DISTANCE_CITY_MAINTENANCE) *
			calculateDistanceMaintenanceTimes100(kCityPlot, eOwner, iPopulation,
			true); // advc
    // doc: disable cap scaling
	//iMaintenanceCap *= GC.getInfo(eOwnerHandicap).getMaxColonyMaintenance();
	//iMaintenanceCap /= 100;
	// <advc.912g>
	//iMaintenanceCap *= std::max(0, GET_PLAYER(eOwner).
	//		getColonyMaintenanceModifier() + 100);
	//iMaintenanceCap /= 100;
	// </advc.912g>
	iMaintenance = std::min(iMaintenance, iMaintenanceCap);
	/*	<advc.exp.3> Alt. idea to the civic-based modifier: High colony maintenance
		only in faraway cities (overall proportional to square of maintenance dist). */
	/*iMaintenance *= calculateMaintenanceDistance(&kCityPlot, eOwner);
	iMaintenance /= GC.getMap().maxMaintenanceDistance();*/ // </advc.exp.3>

    // doc: apply world scaling after exponential effect for proportional impact
    iMaintenance *= GC.getInfo(GC.getMap().getWorldSize()).getColonyMaintenancePercent();
    iMaintenance /= 100;

    // doc: civic colony maintenance modifier
    iMaintenance *= std::max(0, GET_PLAYER(eOwner).getColonyMaintenanceModifier() + 100);
    iMaintenance /= 100;

    // doc: civilization colony maintenance modifier
    iMaintenance *= GET_PLAYER(eOwner).getModifier(MODIFIER_COLONY_MAINTENANCE);
    iMaintenance /= 100;

	FAssert(iMaintenance >= 0);
	return iMaintenance;
}

// advc.500b:
scaled CvCity::defensiveGarrison(
	scaled rStopCountingAt) const // Param important for performance
{
	/*  Time is acceptable - but not negligible (slightly above 1% of an AI turn) -
		with rOUTDATED_PERCENT < 1. Perhaps fine if I keep it at 1 in XML.
		Otherwise, I should simply cache the result of getNoMilitaryPercentAnger. */
	PROFILE_FUNC();

	scaled r = 0;
	CvPlayer const& kOwner = GET_PLAYER(getOwner());
	// ("Obsolete" isn't really the right term for units)
	static scaled const rOUTDATED_PERCENT = per100(GC.getDefineINT(
			"DEMAND_BETTER_PROTECTION_OBSOLETE_PERCENT"));
	CvCity const* pCapital = kOwner.getCapital();
	if (pCapital == this)
		pCapital = NULL;
	FOR_EACH_UNIT_IN(pUnit, getPlot())
	{
		// Exclude naval units but not Explorer and Gunship
		if (!pUnit->isMilitaryHappiness() &&
			pUnit->getUnitInfo().getCultureGarrisonValue() <= 0)
		{
			continue;
		}
		scaled rDefStr = per100(pUnit->maxCombatStr(plot(), NULL, NULL, true));
		if (rOUTDATED_PERCENT != 1 &&
			allUpgradesAvailable(pUnit->getUnitType()) != NO_UNIT ||
			/*	Check capital too. Player might remove access to e.g. Copper
				to avoid Warrior obsoletion penalty, but also cutting the capital
				off from a strategic resource will rarely be worthwhile. */
			(pCapital != NULL && pCapital->allUpgradesAvailable(pUnit->getUnitType())))
		{
			rDefStr *= rOUTDATED_PERCENT;
		}
		r += rDefStr;
		if (rStopCountingAt > 0 && r > rStopCountingAt)
			return r;
	}
	return r;
}

// advc.123f:
void CvCity::failProduction(int iOrderData, int iInvestedProduction, bool bProject)
{
	// Based on code in doCheckProduction
	if (bProject)
		setProjectProduction((ProjectTypes)iOrderData, 0);
	else setBuildingProduction((BuildingTypes)iOrderData, 0);
	OrderTypes eOrderType = (bProject ? ORDER_CREATE : ORDER_CONSTRUCT);
	for (int i = getOrderQueueLength() - 1; i >= 0; i--)
	{
		OrderData* od = getOrderFromQueue(i);
		if (od != NULL && od->eOrderType == eOrderType && od->iData1 == iOrderData)
		{
			FAssert(!canContinueProduction(*od));
			popOrder(i, false, HUMAN_CHOOSE);
		}
	}
	int iGoldPercent = failGoldPercent(eOrderType);
	if (iGoldPercent <= 0)
		return;
	int iProductionGold = (iInvestedProduction * iGoldPercent) / 100;
	GET_PLAYER(getOwner()).changeGold(iProductionGold);
	CvWString szMsg = gDLL->getText("TXT_KEY_MISC_LOST_WONDER_PROD_CONVERTED",
			getNameKey(), bProject ?
			GC.getInfo((ProjectTypes)iOrderData).getTextKeyWide() :
			GC.getInfo((BuildingTypes)iOrderData).getTextKeyWide(),
			iProductionGold);
	gDLL->UI().addMessage(getOwner(), false, -1, szMsg, getPlot(), "AS2D_WONDERGOLD",
			MESSAGE_TYPE_MINOR_EVENT, GC.getInfo(COMMERCE_GOLD).getButton(),
			GC.getColorType("RED"));
}

// <advc.064b>
int CvCity::failGoldPercent(OrderTypes eOrder) const // Fail and overflow gold
{
	/*  To make any future changes to the process conversion rates easier, tie
		fail gold to the Wealth process. */
	int r = GC.getInfo((ProcessTypes)0).getProductionToCommerceModifier(COMMERCE_GOLD);
	switch(eOrder)
	{
	case ORDER_TRAIN: r *= GC.getDefineINT("MAXED_UNIT_GOLD_PERCENT"); break;
	case ORDER_CONSTRUCT: r *= GC.getDefineINT("MAXED_BUILDING_GOLD_PERCENT"); break;
	case ORDER_CREATE: r *= GC.getDefineINT("MAXED_PROJECT_GOLD_PERCENT"); break;
	default: r *= 100; FAssert(false);
	}
	return r / 100;
}


void CvCity::handleOverflow(int iRawOverflow, int iProductionModifier, OrderTypes eOrderType)
{
	if(iRawOverflow < 0) // Can happen through the "+" cheat (Debug mode)
		return;
	FAssert(getOverflowProduction() == 0);
	int iProductionGold = 0;
	int iLostProduction = 0;
	int iOverflow = computeOverflow(iRawOverflow, iProductionModifier, eOrderType,
			&iProductionGold, &iLostProduction);
	if(iOverflow <= 0)
		return;
	setOverflowProduction(iOverflow);
	if(iProductionGold > 0 || iLostProduction > 0)
		payOverflowGold(iLostProduction, iProductionGold);
}


void CvCity::payOverflowGold(int iLostProduction, int iProductionGold)
{
	CvPlayer& kOwner = GET_PLAYER(getOwner());
	kOwner.changeGold(iProductionGold);
	CvWString szMsg(gDLL->getText("TXT_KEY_MISC_OVERFLOW_GOLD", iLostProduction,
			getNameKey(), iProductionGold));
	gDLL->UI().addMessage(getOwner(), false, -1, szMsg,
			"AS2D_WONDERGOLD", MESSAGE_TYPE_INFO, GC.getInfo(COMMERCE_GOLD).
			getButton(), NO_COLOR, getX(), getY(), false, false);
} // </advc.064b>


//doc
int CvCity::getRegionID() const
{
	return plot()->getRegionID();
}

// doc
// TODO: move to header
int CvCity::getSpecialistGoodHappiness() const
{
	return m_iSpecialistGoodHappiness;
}

// doc
int CvCity::getSpecialistBadHappiness() const
{
	int iSpecialistBadHappiness = m_iSpecialistBadHappiness;

	// doc: increased unhappiness from Egalitarianism
	int iAngerModifier = 0;
	FOR_EACH_ENUM(Civic)
	{
		iAngerModifier += GET_PLAYER(getOwner()).getCivicPercentAnger(eLoopCivic, false);
	}

	return iSpecialistBadHappiness * (GC.getPERCENT_ANGER_DIVISOR() + 4 * iAngerModifier) / GC.getPERCENT_ANGER_DIVISOR();
}

// doc
void CvCity::changeSpecialistGoodHappiness(int iChange)
{
	m_iSpecialistGoodHappiness += iChange;
}

// doc
void CvCity::changeSpecialistBadHappiness(int iChange)
{
	m_iSpecialistBadHappiness += iChange;
}

// doc
// TODO: move to header
bool CvCity::isMongolUP() const
{
	return m_bMongolUP;
}

// doc
void CvCity::setMongolUP(bool bNewValue)
{
	m_bMongolUP = bNewValue;
}

// doc
// TODO: move to header
int CvCity::getCorporationGoodHappiness() const
{
	return m_iCorporationGoodHappiness;
}

// doc
// TODO: move to header
int CvCity::getCorporationBadHappiness() const
{
	return m_iCorporationBadHappiness;
}

// doc
// TODO: refactor
int CvCity::getCorporationHappinessByCorporation(CorporationTypes eCorporation) const
{
	FAssertMsg(eCorporation >= 0, "eCorporation expected to be >= 0");
	FAssertMsg(eCorporation < GC.getNumCorporationInfos(), "GC.getNumCorporationInfos expected to be >= 0");

	int iNumBonuses = 0;
	int iHappiness = 0;

	if (isActiveCorporation(eCorporation) && !isDisorder())
	{
		for (int i = 0; i < GC.getDefineINT("NUM_CORPORATION_PREREQ_BONUSES"); ++i)
		{
			BonusTypes eBonus = GC.getInfo(eCorporation).getPrereqBonus(i);
			if (eBonus == NO_BONUS)
				continue;

			iNumBonuses = getNumBonuses(eBonus);
			if (iNumBonuses > 0)
				iHappiness += GC.getInfo(eCorporation).getHappiness() * std::min(12, iNumBonuses);
		}
	}

	// doc: corporation bad happiness modifier
	if (iHappiness < 0)
	{
		iHappiness *= 100 + GET_PLAYER(getOwner()).getCorporationUnhappinessModifier();
		iHappiness /= 100;
	}

	return iHappiness / 10;
}

// doc
// TODO: move to header
int CvCity::getCorporationHealth() const
{
	return m_iCorporationHealth;
}

// doc
// TODO: move to header
int CvCity::getCorporationUnhealth() const
{
	return m_iCorporationUnhealth;
}

// doc
// TODO: refactor
int CvCity::getCorporationHealthByCorporation(CorporationTypes eCorporation) const
{
	int iHealth = 0;

	if (isActiveCorporation(eCorporation) && !isDisorder())
	{
		for (int i = 0; i < GC.getDefineINT("NUM_CORPORATION_PREREQ_BONUSES"); ++i)
		{
			BonusTypes eBonus = GC.getInfo(eCorporation).getPrereqBonus(i);
			if (eBonus == NO_BONUS)
				continue;

			int iNumBonuses = getNumBonuses(eBonus);
			if (iNumBonuses > 0)
			{
				iHealth += GC.getInfo(eCorporation).getHealth() * std::min(12, iNumBonuses);
			}
		}
	}

	// doc: corporation unhealth modifier
	if (iHealth < 0)
	{
		iHealth *= 100 + getCorporationUnhealthModifier();
		iHealth /= 100;
	}

	return iHealth / 10;
}

// doc
void CvCity::setGameTurnCivLost(CivilizationTypes eCivilization, int iNewValue)
{
	m_aiGameTurnCivLost.set(eCivilization, iNewValue);
}

// doc
int CvCity::getGameTurnPlayerLost(PlayerTypes ePlayer)
{
	CivilizationTypes eCivilization = GET_PLAYER(ePlayer).getCivilizationType();
	if (eCivilization == NO_CIVILIZATION)
	{
		return -1;
	}

	return getGameTurnCivLost(eCivilization);
}

// doc
void CvCity::setGameTurnPlayerLost(PlayerTypes ePlayer, int iNewValue)
{
	CivilizationTypes eCivilization = GET_PLAYER(ePlayer).getCivilizationType();
	if (eCivilization != NO_CIVILIZATION)
	{
		setGameTurnCivLost(eCivilization, iNewValue);
	}
}

// doc
bool CvCity::isColony() const
{
	CvCity* pCapital = GET_PLAYER(getOwner()).getCapitalCity();
	if (pCapital == NULL) 
		return false;

	return getPlot().isOverseas(pCapital->getPlot());
}

// doc
bool CvCity::canSlaveJoin() const
{
	if (!GET_PLAYER(getOwner()).canUseSlaves()) 
		return false;
	if (!isColony()) 
		return false;

	int iNumSlaves = getFreeSpecialistCount(SPECIALIST_SLAVE);
	return 2 * iNumSlaves < getPopulation();
}

// doc
int CvCity::calculateCultureCost(CvPlot const& kPlot, bool bOrdering) const
{
	if (at(kPlot))
		return 0;

	// tiles with forts can be covered for free
	if (kPlot.getImprovementType() != NO_IMPROVEMENT && GC.getInfo(kPlot.getImprovementType()).isActsAsCity())
		return 0;

	int iCost = kPlot.calculateCultureCost();
	int iExtraCost = 0;

	int iDistance = std::max(plotDistance(plot(), &kPlot), GC.getMap().calculatePathDistance(plot(), &kPlot));

	if (bOrdering)
	{
		if (kPlot.getBonusType() == NO_BONUS && iCost >= getTurns(15))
			iExtraCost += 100;

		iExtraCost += 100 * iDistance;

		if (kPlot.isWater() && !kPlot.isLake() && kPlot.getBonusType() == NO_BONUS && iDistance > 1)
		{
			if (!isCoastal(20))
				iExtraCost += 1000;
			else
				iExtraCost += 5;
		}
	}

	if (kPlot.getBonusType() != NO_BONUS && GET_TEAM(GET_PLAYER(getOwner()).getTeam()).isHasTech(GC.getInfo(kPlot.getBonusType()).getTechReveal()))
		iExtraCost += GC.getDefineINT("CULTURE_COST_BONUS");

	if (iDistance <= 1)
		iExtraCost -= GC.getDefineINT("CULTURE_COST_DISTANCE");
	else
		iExtraCost += std::min(3, iDistance) * GC.getDefineINT("CULTURE_COST_DISTANCE");

	if (getPlot().isRiver() && kPlot.isRiver())
		iExtraCost += GC.getDefineINT("CULTURE_COST_RIVER");

	// doc: Inca UP
	if (getCivilizationType() == INCA && (GET_PLAYER(getOwner()).getPeriod() == NO_PERIOD || GET_PLAYER(getOwner()).getPeriod() == PERIOD_LATE_INCA) && kPlot.isPeak())
		iExtraCost += GC.getDefineINT("CULTURE_COST_HILL") - GC.getDefineINT("CULTURE_COST_PEAK");

	// doc: Congolese UP
	if (getCivilizationType() == CONGO)
	{
		if (kPlot.getFeatureType() == FEATURE_MARSH || kPlot.getFeatureType() == FEATURE_JUNGLE || kPlot.getFeatureType() == FEATURE_RAINFOREST)
			iExtraCost -= GC.getInfo(kPlot.getFeatureType()).getCultureCostModifier();
	}

	// doc: Steppe Empires
	if (getCivilizationType() == TURKS || getCivilizationType() == MONGOLS)
	{
		if (kPlot.getTerrainType() == TERRAIN_DESERT || kPlot.getTerrainType() == TERRAIN_STEPPE || kPlot.getTerrainType() == TERRAIN_SEMIDESERT)
			iExtraCost -= GC.getInfo(TERRAIN_DESERT).getCultureCostModifier();

		if (kPlot.getTerrainType() == TERRAIN_PLAINS)
			iExtraCost -= 5;
	}

	// doc: respect game speed
	iExtraCost = getTurns(iExtraCost);
	iCost += iExtraCost;

	return bOrdering ? iCost : std::max(0, iCost);
}

// doc: takes local index, returns plot as global index
int CvCity::getCulturePlotIndex(CulturePlotTypes eCulturePlot) const
{
	return m_aiCulturePlots.get(eCulturePlot);
}

// doc: takes local index, returns plot via global index
CvPlot& CvCity::getCulturePlot(CulturePlotTypes eCulturePlot) const
{
	int iIndex = getCulturePlotIndex(eCulturePlot);

	// negative index means tile beyond northern or southern edge, just return city tile in this case, additional coverage of this tile does not hurt
	if (iIndex < 0) return getPlot();

	return GC.getMap().getPlotByIndex(iIndex);
}

// doc: costs for local index
int CvCity::getCultureCost(CulturePlotTypes eCulturePlot) const
{
	return m_aiCultureCosts.get(eCulturePlot);
}

// doc
struct cultureCompare
{
	CvCity* city;

	bool operator() (int index1, int index2)
	{
		CvPlot* pPlot1 = GC.getMap().plotByIndex(index1);
		CvPlot* pPlot2 = GC.getMap().plotByIndex(index2);

		// sort by plot culture costs
		int iCost1 = (pPlot1 != NULL && city != NULL) ? city->calculateCultureCost(*pPlot1, true) : MAX_INT;
		int iCost2 = (pPlot2 != NULL && city != NULL) ? city->calculateCultureCost(*pPlot2, true) : MAX_INT;

		return (iCost1 < iCost2);
	}
};

// doc
// TODO: use city relative index instead of global index
void CvCity::updateCultureCosts()
{
	std::vector<int> plots;
	std::vector<int> openPlots;

	FOR_EACH_ENUM(CulturePlot)
	{
		int iIndex = m_aiCulturePlots.get(eLoopCulturePlot);
		if (eLoopCulturePlot < getNextCoveredPlot())
			plots.push_back(iIndex);
		else
			openPlots.push_back(iIndex);
	}

	cultureCompare cmp;
	cmp.city = this;
	std::sort(openPlots.begin(), openPlots.end(), cmp);

	for (std::vector<int>::iterator it = openPlots.begin(); it != openPlots.end(); ++it)
	{
		plots.push_back(*it);
	}

	int iCumulativeCosts = 0;
	FOR_EACH_ENUM(CulturePlot)
	{
		int iIndex = plots[eLoopCulturePlot];
		m_aiCulturePlots.set(eLoopCulturePlot, iIndex);
		
		CvPlot* pPlot = GC.getMap().plotByIndex(iIndex);
		if (pPlot != NULL)
			iCumulativeCosts += calculateCultureCost(*pPlot);

		m_aiCultureCosts.set(eLoopCulturePlot, iCumulativeCosts);
	}
}

// doc
// TODO: refactor
void CvCity::setNextCoveredPlot(CulturePlotTypes eCulturePlot, bool bUpdatePlotGroups)
{
	CulturePlotTypes eCurrentCulturePlot = getNextCoveredPlot();
	bool bMinor = GET_PLAYER(getOwner()).isMinorCiv();

	if (eCulturePlot < eCurrentCulturePlot)
	{
		m_eNextCoveredPlot = eCulturePlot;

		if (eCurrentCulturePlot > 0)
		{
			for (CulturePlotTypes eLoopCulturePlot = (CulturePlotTypes)(eCurrentCulturePlot-1); eLoopCulturePlot >= eCulturePlot; eLoopCulturePlot--)
			{
				if (eLoopCulturePlot >= NUM_CULTURE_PLOTS) 
					continue;

				CvPlot& kCulturePlot = getCulturePlot(eLoopCulturePlot);
				int iCultureRange = std::max(0, plotDistance(plot(), &kCulturePlot));

				// doc: only two rings for minor civilizations
				if (bMinor && iCultureRange > 2)
					continue;

				kCulturePlot.changeCultureRangeCities(getOwner(), (CultureLevelTypes)iCultureRange, -1, bUpdatePlotGroups);
			}
		}
	}

	if (eCulturePlot > eCurrentCulturePlot)
	{
		m_eNextCoveredPlot = eCulturePlot;

		bool bCoveredNewPlot = false;

		if (eCulturePlot > 0)
		{
			for (CulturePlotTypes eLoopCulturePlot = eCurrentCulturePlot; eLoopCulturePlot < eCulturePlot; eLoopCulturePlot++)
			{
				CvPlot& kCulturePlot = getCulturePlot(eLoopCulturePlot);
				int iCultureRange = std::max(0, plotDistance(plot(), &kCulturePlot));

				// doc: only two rings for minor civilizations
				if (bMinor && iCultureRange > 2)
					continue;

				if (!kCulturePlot.isCultureRangeCity(getOwner(), (CultureLevelTypes)iCultureRange))
					bCoveredNewPlot = true;

				kCulturePlot.changeCultureRangeCities(getOwner(), (CultureLevelTypes)iCultureRange, 1, bUpdatePlotGroups);
			}
		}

		if (GC.getGame().isFinalInitialized())
		{
			// TODO: introduce getLastCoveredPlot()
			if (getNextCoveredPlot() > 0 && getCultureCost((CulturePlotTypes)(getNextCoveredPlot()-1)) > 0 && bCoveredNewPlot)
			{
				CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_BORDERS_EXPANDED", getNameKey());
				gDLL->getInterfaceIFace()->addMessage(getOwner(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_CULTUREEXPANDS", MESSAGE_TYPE_MINOR_EVENT, GC.getCommerceInfo(COMMERCE_CULTURE).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), getX(), getY(), true, true);

				CvEventReporter::getInstance().cultureExpansion(this, getOwner());
			}
		}
	}
}

// doc
void CvCity::updateCoveredPlots(bool bUpdatePlotGroups)
{
	if (getCultureUpdateTimer() > 0)
		return;

	int iCulture = getCulture(getOwner());

	// TODO: is this really the "next" covered plot?
	FOR_EACH_ENUM(CulturePlot)
	{
		if (iCulture < getCultureCost((CulturePlotTypes)(eLoopCulturePlot + 1)))
		{
			setNextCoveredPlot(eLoopCulturePlot, bUpdatePlotGroups);
			break;
		}
	}
}

// doc: skip plots that are already covered by a city
CulturePlotTypes CvCity::getEffectiveNextCoveredPlot() const
{
	CulturePlotTypes eNextCoveredPlot = getNextCoveredPlot();

	// TODO: this may have a one off error
	FOR_EACH_ENUM(CulturePlot)
	{
		CvPlot const& kCulturePlot = getCulturePlot(eLoopCulturePlot);
		int iDistance = plotDistance(plot(), &kCulturePlot);

		if (!kCulturePlot.isOwned() && (eLoopCulturePlot >= eNextCoveredPlot || (iDistance > getCultureLevel() && iDistance > 0 && getCultureCost(eNextCoveredPlot) > getCultureThreshold((CultureLevelTypes)(iDistance - 1)))))
		{
			return eLoopCulturePlot;
		}
	}

	return FIRST_CULTURE_PLOT;
}

// doc: takes local culture plot id, returns true if plot costs less culture than the culture expansion to reach it
bool CvCity::isCoveredBeforeExpansion(CulturePlotTypes eCulturePlot) const
{
	CvPlot const& kCulturePlot = getCulturePlot(eCulturePlot);
	int iDistance = plotDistance(plot(), &kCulturePlot);

	return (getCultureCost(eCulturePlot) < getCultureThreshold((CultureLevelTypes)iDistance));
}

// doc: redraw Great Wall around this city
void CvCity::updateGreatWall()
{
	gDLL->getEngineIFace()->RemoveGreatWall(this);
	gDLL->getEngineIFace()->AddGreatWall(this);
}

// doc: estimate how many points the city will grow in the next X turns
// TODO: used?
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

		iGrowthThreshold = GET_PLAYER(getOwner()).getGrowthThreshold(iPopulation);
		iFoodStored = iGrowthThreshold * getMaxFoodKeptPercent() / 100;

		iFoodDifference -= (iPopulation < NUM_CITY_PLOTS) ? 1 : 2;
	}

	return iPopulation - getPopulation();
}

// doc
void CvCity::replaceReligion(ReligionTypes eOldReligion, ReligionTypes eNewReligion)
{
	if (eOldReligion == NO_RELIGION) 
		return;
	if (!isHasReligion(eOldReligion)) 
		return;

	FOR_EACH_ENUM(Building)
	{
		CvBuildingInfo const& kBuilding = GC.getInfo(eLoopBuilding);
		if (kBuilding.isWorldWonder())
			continue;
		if (kBuilding.getSpecialBuildingType() == NO_SPECIALBUILDING)
			continue;

		if (isHasRealBuilding(eLoopBuilding) && kBuilding.getPrereqReligion() == eOldReligion)
			setHasRealBuilding(eLoopBuilding, false);

		if (eNewReligion != NO_RELIGION && kBuilding.getPrereqReligion() == eNewReligion)
			setHasRealBuilding(eLoopBuilding, true);
	}


	if (!isHolyCity(eOldReligion))
		setHasReligion(eOldReligion, false, true, true);

	if (eNewReligion != NO_RELIGION)
		setHasReligion(eNewReligion, true, true, true);
}

// doc
void CvCity::removeReligion(ReligionTypes eReligion)
{
	replaceReligion(eReligion, NO_RELIGION);
}

// doc
// TODO: refactor
void CvCity::spreadReligion(ReligionTypes eReligion, bool bMissionary)
{
	setHasReligion(eReligion, true, true, !bMissionary);

	ReligionTypes eDisappearingReligion = disappearingReligion(eReligion);

	int iDisappearanceChance = bMissionary ? 2 : 3;

	if (eDisappearingReligion != NO_RELIGION && GC.getGame().getSorenRandNum(iDisappearanceChance, "Religion disappearance") == 0)
	{
		removeReligion(eDisappearingReligion);
	}
}

// doc
struct disappearingReligionCompare
{
	const CvCity* city;

	bool operator() (ReligionTypes eLeftReligion, ReligionTypes eRightReligion)
	{
		int iLeftValue = 0;
		int iRightValue = 0;

		if (city != NULL)
		{
			iLeftValue += GET_PLAYER(city->getOwner()).getSpreadType(city->getPlot(), eLeftReligion, false, true) * 3;
			iRightValue += GET_PLAYER(city->getOwner()).getSpreadType(city->getPlot(), eRightReligion, false, true) * 3;

			iLeftValue += city->getReligionInfluence(eLeftReligion);
			iRightValue += city->getReligionInfluence(eRightReligion);
		}
		else
		{
			iLeftValue += (int)eLeftReligion;
			iRightValue += (int)eRightReligion;
		}

		return (iLeftValue < iRightValue);
	}
};

// doc
// TODO: refactor
ReligionTypes CvCity::disappearingReligion(ReligionTypes eNewReligion, bool bConquest) const
{
	if (!GC.getGame().isFinalInitialized())
		return NO_RELIGION;

	CvPlayer const& kOwner = GET_PLAYER(getOwner());
	std::vector<ReligionTypes> religions;

	FOR_EACH_ENUM(Religion)
	{
		if (eLoopReligion == eNewReligion)
			continue;
		if (!isHasReligion(eLoopReligion))
			continue;
		if (kOwner.isStateReligion() && kOwner.getStateReligion() == eLoopReligion)
			continue;
		if (isHolyCity(eLoopReligion))
			continue;

		if (kOwner.getSpreadType(getPlot(), eLoopReligion, false, true) == RELIGION_SPREAD_NONE)
			religions.push_back(eLoopReligion);
	}

	disappearingReligionCompare cmp;
	cmp.city = this;

	if (religions.size() > 0)
		return *min_element(religions.begin(), religions.end(), cmp);

	if (eNewReligion == NO_RELIGION && !bConquest)
		return NO_RELIGION;

	int iMaxReligions = std::max(2, 1 + getPopulation() / 5);
	if (!bConquest)
	{
		if (eNewReligion == NO_RELIGION)
			return NO_RELIGION;
		if (getReligionCount() <= iMaxReligions)
			return NO_RELIGION;
	}

	ReligionSpreadTypes eNewReligionSpread = eNewReligion != NO_RELIGION ? kOwner.getSpreadType(getPlot(), eNewReligion, false, true) : RELIGION_SPREAD_MINORITY;
	religions.clear();

	FOR_EACH_ENUM(Religion)
	{
		if (eLoopReligion == eNewReligion)
			continue;
		if (!isHasReligion(eLoopReligion))
			continue;
		if (kOwner.getStateReligion() == eLoopReligion)
			continue;

		ReligionSpreadTypes eCurrentSpread = kOwner.getSpreadType(getPlot(), eLoopReligion, false, true);
		if (eCurrentSpread <= eNewReligionSpread)
			religions.push_back(eLoopReligion);
	}

	if (religions.size() > 0)
		return *min_element(religions.begin(), religions.end(), cmp);

	return NO_RELIGION;
}

// doc
// TODO: move to header
int CvCity::getPowerConsumedCount() const
{
	return m_iPowerConsumedCount;
}

// doc
void CvCity::changePowerConsumedCount(int iChange)
{
	if (iChange != 0)
	{
		m_iPowerConsumedCount += iChange;

		updatePowerHealth();
	}
}

// doc
void CvCity::changeCultureGreatPeopleRateModifier(int iChange)
{
	m_iCultureGreatPeopleRateModifier += iChange;
}

// doc
void CvCity::changeCultureHappiness(int iChange)
{
	if (iChange != 0)
	{
		m_iCultureHappiness += iChange;

		AI_setAssignWorkDirty(true);
	}
}

// doc
void CvCity::changeCultureTradeRouteModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iCultureTradeRouteModifier += iChange;

		updateTradeRoutes();
	}
}

// doc
void CvCity::changeBuildingUnignorableBombardDefense(int iChange)
{
	m_iBuildingUnignorableBombardDefense += iChange;
}

// doc
int CvCity::getAdditionalUnignorableBombardDefenseByBuilding(BuildingTypes eBuilding) const
{
	CvBuildingInfo const& kBuilding = GC.getBuildingInfo(eBuilding);
	int iBaseDefense = getBuildingUnignorableBombardDefense();

	// cap total bombard defense at 100
	return std::min(kBuilding.getUnignorableBombardDefenseModifier() + iBaseDefense, 100) - iBaseDefense;
}

// doc
void CvCity::setBuildingOriginalOwner(BuildingTypes eBuilding, CivilizationTypes eCivilization)
{
	m_aeBuildingOriginalOwner.set(eBuilding, eCivilization);
}

// doc
void CvCity::setBuildingOriginalTime(BuildingTypes eBuilding, int iYear)
{
	m_aiBuildingOriginalTime.set(eBuilding, iYear);
}

// doc
void CvCity::setCultureRank(int iNewValue)
{
	if (m_iCultureRank != iNewValue)
	{
		bool* abOldHasBonusEffect = new bool[GC.getNumBonusInfos()];
		FOR_EACH_ENUM(Bonus)
		{
			abOldHasBonusEffect[eLoopBonus] = hasBonusEffect(eLoopBonus);
		}

		m_iCultureRank = iNewValue;

		FOR_EACH_ENUM(Bonus)
		{
			if (abOldHasBonusEffect[eLoopBonus] != hasBonusEffect(eLoopBonus))
				processBonusEffect(eLoopBonus, hasBonusEffect(eLoopBonus) ? 1 : -1);
		}

		AI_setAssignWorkDirty(true);
	}
}

// doc
void CvCity::setStabilityPopulation(int iNewValue)
{
	m_iStabilityPopulation = iNewValue;
}

// doc
void CvCity::setBuildingUnhealthModifier(int iNewValue)
{
	m_iBuildingUnhealthModifier = iNewValue;
}

// doc
void CvCity::changeBuildingUnhealthModifier(int iChange)
{
	m_iBuildingUnhealthModifier += iChange;
}

// doc
void CvCity::setCorporationUnhealthModifier(int iNewValue)
{
	m_iCorporationUnhealthModifier = iNewValue;
}

// doc
void CvCity::changeCorporationUnhealthModifier(int iChange)
{
	m_iCorporationUnhealthModifier += iChange;
}

// doc
// TODO: refactor
int CvCity::countSatellites() const
{
	int iCount = 0;
	FOR_EACH_ENUM(Specialist)
	{
		if (GC.getInfo(eLoopSpecialist).isSatellite())
			iCount += getFreeSpecialistCount(eLoopSpecialist);
	}

	return iCount;
}

int CvCity::getSatelliteSlots() const
{
	if (!GET_TEAM(getTeam()).isHasTech((TechTypes)SATELLITES))
	{
		return 0;
	}

	int iSpecialistSlots = 0;

	for (int iI = 0; iI < GC.getNumSpecialistInfos(); iI++)
	{
		iSpecialistSlots += getMaxSpecialistCount((SpecialistTypes)iI);
	}

	return iSpecialistSlots / 5;
}

// doc
bool CvCity::canSatelliteJoin() const
{
	return countSatellites() < getSatelliteSlots();
}

// doc
// TODO: refactor
int CvCity::getSpecialistGreatPeopleRateChange(SpecialistTypes eSpecialist) const
{
	CvSpecialistInfo& kSpecialist = GC.getSpecialistInfo(eSpecialist);
	int iGreatPeopleRate = kSpecialist.getGreatPeopleRateChange();

	/*if (!kSpecialist.isNoGlobalEffects())
	{
		int iCultureLevelRate = kSpecialist.getCultureLevelGreatPeopleRateChange(getCultureLevel());
		FAssert(iCultureLevelRate == 0);
		iGreatPeopleRate += iCultureLevelRate;
	}*/

	// Pyramid of the Sun: +3 great people rate per citizen
	if (eSpecialist == SPECIALIST_CITIZEN)
	{
		if (isHasBuildingEffect(PYRAMID_OF_THE_SUN))
		{
			iGreatPeopleRate += 3;
		}
	}

	// International Space Station: +2 great people rate per satellite
	if (kSpecialist.isSatellite())
	{
		if (GET_TEAM(getTeam()).getProjectCount(PROJECT_INTERNATIONAL_SPACE_STATION))
		{
			iGreatPeopleRate += 2;
		}
	}

	return iGreatPeopleRate;
}

// doc
// TODO: move to header
int CvCity::getActualTotalCultureTimes100() const
{
	return m_iTotalCultureTimes100;
}

// doc
// TODO: move to header
int CvCity::getBuildingDamage() const
{
	return m_iBuildingDamage;
}

// doc
void CvCity::setBuildingDamage(int iNewValue)
{
	m_iBuildingDamage = iNewValue;
}

// doc
void CvCity::changeBuildingDamage(int iChange)
{
	m_iBuildingDamage += iChange;
}

// doc
// TODO: move to header
int CvCity::getBuildingDamageChange() const
{
	return m_iBuildingDamageChange;
}

// doc
void CvCity::setBuildingDamageChange(int iNewValue)
{
	m_iBuildingDamageChange = iNewValue;
}

// doc
void CvCity::changeBuildingDamageChange(int iChange)
{
	m_iBuildingDamageChange += iChange;
}

// doc
struct buildingDamageCompare
{
	CvCity* city;

	bool operator() (int iLeftBuilding, int iRightBuilding)
	{
		CvBuildingInfo const& kLeftBuilding = GC.getBuildingInfo((BuildingTypes)iLeftBuilding);
		CvBuildingInfo const& kRightBuilding = GC.getBuildingInfo((BuildingTypes)iRightBuilding);

		int iLeftProbability = kLeftBuilding.getConquestProbability();
		int iRightProbability = kRightBuilding.getConquestProbability();

		if (kLeftBuilding.getPrereqReligion() != NO_RELIGION && !GET_PLAYER(city->getOwner()).isTolerating(kLeftBuilding.getPrereqReligion()))
			iLeftProbability /= 2;

		if (kRightBuilding.getPrereqReligion() != NO_RELIGION && !GET_PLAYER(city->getOwner()).isTolerating(kRightBuilding.getPrereqReligion()))
			iRightProbability /= 2;

		return iLeftProbability < iRightProbability || (iLeftProbability == iRightProbability && kLeftBuilding.getProductionCost() < kRightBuilding.getProductionCost());
	}
};

// doc
// TODO: refactor
void CvCity::applyBuildingDamage(int iDamage)
{
	int iRemainingDamage = getBuildingDamage() + iDamage;

	if (iRemainingDamage == 0)
	{
		return;
	}

	std::vector<int> buildings;

	for (int iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		if (!isHasRealBuilding((BuildingTypes)iI))
		{
			continue;
		}

		if (GC.getBuildingInfo((BuildingTypes)iI).getDefenseModifier() > 0)
		{
			continue;
		}

		if (GC.getBuildingInfo((BuildingTypes)iI).getProductionCost() == 0)
		{
			continue;
		}

		if (GC.getBuildingInfo((BuildingTypes)iI).getConquestProbability() == 100)
		{
			continue;
		}

		// buildings that are impossible to conquer have been removed immediately on conquest
		// so if they are restored some other way, do not remove them again
		if (GC.getBuildingInfo((BuildingTypes)iI).getConquestProbability() == 0)
		{
			continue;
		}

		for (int iJ = 0; iJ < getNumRealBuilding((BuildingTypes)iI); iJ++)
		{
			buildings.push_back(iI);
		}
	}

	buildingDamageCompare cmp;
	cmp.city = this;
	std::sort(buildings.begin(), buildings.end(), cmp);

	BuildingTypes eBuilding;
	int iCost;
	for (std::vector<int>::iterator it = buildings.begin(); it != buildings.end(); ++it)
	{
		eBuilding = (BuildingTypes)*it;
		CvBuildingInfo& kBuilding = GC.getBuildingInfo(eBuilding);
		iCost = kBuilding.getProductionCost() * kBuilding.getConquestProbability() / 100;

		if (iCost > iRemainingDamage) break;

		setNumRealBuilding(eBuilding, getNumRealBuilding(eBuilding) - 1);
		iRemainingDamage -= iCost;
	}

	setBuildingDamage(getOccupationTimer() > 0 ? iRemainingDamage : 0);
}

// doc
// TODO: move to header
int CvCity::getTotalPopulationLoss() const
{
	return m_iTotalPopulationLoss;
}

// doc
void CvCity::setTotalPopulationLoss(int iNewValue)
{
	m_iTotalPopulationLoss = iNewValue;
}

// doc
void CvCity::changeTotalPopulationLoss(int iChange)
{
	setTotalPopulationLoss(getTotalPopulationLoss() + iChange);
}

// doc
// TODO: move to header
int CvCity::getPopulationLoss() const
{
	return m_iPopulationLoss;
}

// doc
void CvCity::setPopulationLoss(int iNewValue)
{
	m_iPopulationLoss = iNewValue;
}

// doc
void CvCity::applyPopulationLoss(int iLoss)
{
	int iLostPopulation = std::min(getTotalPopulationLoss(), iLoss);
	setPopulation(std::max(0, getPopulation() - iLostPopulation));
}

// doc
int CvCity::getRebuildProduction() const
{
	int iProduction = 0;
	FOR_EACH_ENUM(BuildingClass)
	{
		BuildingTypes eLoopBuilding = GC.getInfo(getCivilizationType()).getCivilizationBuildings(eLoopBuildingClass);
		if (eLoopBuilding == NO_BUILDING)
			continue;
		if (isHasRealBuilding(eLoopBuilding))
			continue;

		CvBuildingInfo const& kBuilding = GC.getInfo(eLoopBuilding);
		if (kBuilding.getFreeStartEra() == NO_ERA)
			continue;

		if (GET_PLAYER(getOwner()).getCurrentEra() < kBuilding.getFreeStartEra())
			continue;
		if (!canConstruct(eLoopBuilding))
			continue;

		iProduction += kBuilding.getProductionCost();
	}

	return iProduction;
}

// doc
void CvCity::completeAcquisition(int iCaptureGold, bool bChooseProduction)
{
	int iOccupationTime = getOccupationTimer();
	int iTotalBuildingDamage = getBuildingDamage();

	if (iCaptureGold > 0)
	{
		CvEventReporter::getInstance().cityCaptureGold(this, getOwner(), iCaptureGold);
	}

	if (iOccupationTime > 0)
	{
		setBuildingDamage(0);
		setBuildingDamageChange(iTotalBuildingDamage / iOccupationTime);

		if (getTotalPopulationLoss() > 0)
		{
			setPopulationLoss(std::max(1, getTotalPopulationLoss() / iOccupationTime));

			if (getTotalPopulationLoss() > iOccupationTime)
			{
				int iImmediateLoss = getTotalPopulationLoss() % iOccupationTime;
				changePopulation(-iImmediateLoss);
			}
		}
	}
	else
	{
		applyBuildingDamage(iTotalBuildingDamage);

		if (getPopulation() > getTotalPopulationLoss())
		{
			changePopulation(-getTotalPopulationLoss());

			if (bChooseProduction)
			{
				chooseProduction();
			}
		}
		else
		{
			completeRaze();
		}
	}
}

// doc
void CvCity::sack(PlayerTypes eHighestCulturePlayer, int iCaptureGold)
{
	if (!GET_PLAYER(getOwner()).isNoResistance())
	{
		changeOccupationTimer(1 + getOccupationTimer() / 2);
	}

	changeBuildingDamage(getBuildingDamage());
	changeTotalPopulationLoss(1 + getTotalPopulationLoss() / 2);

	int iSackGold = iCaptureGold / 2;

	// Leoreth: Norse UP
	if (getCivilizationType() == NORSE && GET_PLAYER(getOwner()).getCurrentEra() <= ERA_MEDIEVAL)
	{
		iSackGold += iCaptureGold + iSackGold;
	}

	GET_PLAYER(getOwner()).changeGold(iSackGold);

	FOR_EACH_ENUM(Building)
	{
		if (!isHasRealBuilding(eLoopBuilding))
			continue;

		CvBuildingInfo const& kBuilding = GC.getInfo(eLoopBuilding);
		if (kBuilding.isWorldWonder())
			continue;

		if (kBuilding.getDefenseModifier() > 0 || kBuilding.getBombardDefenseModifier() > 0 || kBuilding.getUnignorableBombardDefenseModifier() > 0)
		{
			setHasRealBuilding(eLoopBuilding, false);
		}
	}

	FOR_EACH_ENUM(Player)
	{
		if (getOwner() == eLoopPlayer)
			continue;

		setCulture(eLoopPlayer, getActualCulture(eLoopPlayer) * 8 / 10, true, true);
	}

	ReligionTypes eDisappearingReligion = disappearingReligion(NO_RELIGION, true);
	if (eDisappearingReligion != NO_RELIGION)
	{
		removeReligion(eDisappearingReligion);
	}

	if (eHighestCulturePlayer != NO_PLAYER && eHighestCulturePlayer != getOwner())
	{
		GET_PLAYER(eHighestCulturePlayer).AI_changeMemoryCount(getOwner(), MEMORY_SACKED_CITY, 1);
	}

	completeAcquisition(iCaptureGold + iSackGold);

	CvEventReporter::getInstance().citySacked(this);
}

// doc
void CvCity::spare(int iCaptureGold)
{
	int iSpareGold = 2 * getBuildingDamage() + iCaptureGold;

	if (getOccupationTimer() > 0)
	{
		changeOccupationTimer(-(1 + getOccupationTimer() / 2), false);
	}

	setBuildingDamage(getBuildingDamage() / 3);
	changeTotalPopulationLoss(-(1 + getTotalPopulationLoss() / 2));

	GET_PLAYER(getOwner()).changeGold(-iSpareGold);

	completeAcquisition(0);
}

// doc
void CvCity::raze(int iCaptureGold)
{
	setTotalPopulationLoss(getPopulation());
	completeAcquisition(iCaptureGold);
}

// doc
void CvCity::completeRaze()
{
	plot()->resetCultureConversion();

	FOR_EACH_ENUM(Direction)
	{
		CvPlot* pAdjacentPlot = plotDirection(getX(), getY(), eLoopDirection);
		if (pAdjacentPlot == NULL)
			continue;

		pAdjacentPlot->resetCultureConversion();
	}

	doTask(TASK_RAZE);
}

// doc
bool CvCity::canLiberate() const
{
	if (isOccupation())
		return false;
	if (isOriginalOwner(getOwner()))
		return false;
	if (GC.getGame().getGameTurn() - getGameTurnAcquired() < getTurns(10))
		return false;

	return true;
}

// doc
int CvCity::calculateBaseYieldRate(YieldTypes eYield) const
{
	int iYield = 0;
	FOR_EACH_ENUM(CityPlot)
	{
		if (isWorkingPlot(eLoopCityPlot))
			iYield += getCityIndexPlot(eLoopCityPlot)->getYield(eYield);
	}

	FOR_EACH_ENUM(Building)
	{
		if (!isHasRealBuilding(eLoopBuilding))
			continue;
		if (GET_TEAM(getTeam()).isObsoleteBuilding(eLoopBuilding))
			continue;

		iYield += GC.getInfo(eLoopBuilding).getYieldChange(eYield);
		iYield += getBuildingYieldChange(GC.getInfo(eLoopBuilding).getBuildingClassType(), eYield);
	}

	FOR_EACH_ENUM(Specialist)
	{
		int iNumSpecialists = getSpecialistCount(eLoopSpecialist) + getFreeSpecialistCount(eLoopSpecialist);
		
		iYield += iNumSpecialists * GC.getInfo(eLoopSpecialist).getYieldChange(eYield);
		iYield += iNumSpecialists * GET_PLAYER(getOwner()).getSpecialistExtraYield(eLoopSpecialist, eYield);
	}

	iYield += getTradeYield(eYield);
	iYield += getCorporationYield(eYield);

	return iYield;
}

// doc
// TODO: refactor
int CvCity::calculateBaseGreatPeopleRate() const
{
	int iRate = 0;

	for (int iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		if (isHasRealBuilding((BuildingTypes)iI))
		{
			iRate += GC.getBuildingInfo((BuildingTypes)iI).getGreatPeopleRateChange();

			if (!GET_TEAM(getTeam()).isObsoleteBuilding((BuildingTypes)iI))
			{
				iRate += getBuildingGreatPeopleRateChange((BuildingClassTypes)GC.getBuildingInfo((BuildingTypes)iI).getBuildingClassType());
			}
		}
	}

	for (int iI = 0; iI < GC.getNumSpecialistInfos(); iI++)
	{
		int iChange = (getSpecialistCount((SpecialistTypes)iI) + getFreeSpecialistCount((SpecialistTypes)iI)) * getSpecialistGreatPeopleRateChange((SpecialistTypes)iI);
		iRate += iChange;
	}

	return iRate;
}

// doc
bool CvCity::isCore(CivilizationTypes eCivilization) const
{
	return plot()->isCore(eCivilization);
}

// doc
bool CvCity::isCore(PlayerTypes ePlayer) const
{
	return plot()->isCore(ePlayer);
}

// doc
// TODO: redundant?
bool CvCity::isCore() const
{
	return plot()->isCore();
}

// doc
bool CvCity::rebuild(EraTypes eEra)
{
	if (eEra == NO_ERA)
	{
		eEra = GET_PLAYER(getOwner()).getCurrentEra();
	}

	bool bBuilt = false;
	FOR_EACH_ENUM(BuildingClass)
	{
		BuildingTypes eLoopBuilding = GC.getInfo(getCivilizationType()).getCivilizationBuildings(eLoopBuildingClass);
		if (eLoopBuilding == NO_BUILDING)
			continue;

		CvBuildingInfo const& kBuilding = GC.getInfo(eLoopBuilding);
		if (kBuilding.getFreeStartEra() == NO_ERA)
			continue;
		if (kBuilding.getFreeStartEra() > eEra)
			continue;
		if (!canConstruct(eLoopBuilding) && getFirstBuildingOrder(eLoopBuilding) == -1)
			continue;

		setNumRealBuilding(eLoopBuilding, 1);
		bBuilt = true;
	}

	return bBuilt;
}

// doc
int CvCity::getRegionGroup() const
{
	return plot()->getRegionGroup();
}

// doc
// TODO: refactor
int CvCity::getTempHappiness() const
{
	int iHappinessTurns = getTurns(GC.getDefineINT("TEMP_HAPPY_TURNS"));

	return (getHappinessTimer() + iHappinessTurns - 1) / iHappinessTurns;
}