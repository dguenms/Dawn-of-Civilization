#pragma once

#ifndef CyPlayer_h
#define CyPlayer_h
//
// Python wrapper class for CvPlayer 
// 

//#include "CvEnums.h"
//#include "CvStructs.h"

class CyUnit;
class CvPlayer;
class CyCity;
class CyArea;
class CyPlot;
class CySelectionGroup;
class CyPlayer
{
public:
	CyPlayer();
	CyPlayer(CvPlayer* pPlayer);		// Call from C++
	CvPlayer* getPlayer() { return m_pPlayer;	}	// Call from C++
	bool isNone() { return (m_pPlayer==NULL); }

	int startingPlotRange();
	bool startingPlotWithinRange(CyPlot *pPlot, int /*PlayerTypes*/ ePlayer, int iRange, int iPass);

	CyPlot* findStartingPlot(bool bRandomize);

	CyCity* initCity(int x, int y);
	void acquireCity(CyCity* pCity, bool bConquest, bool bTrade);
	void killCities();

	std::wstring getNewCityName();

	CyUnit* initUnit(int /*UnitTypes*/ iIndex, int iX, int iY, UnitAITypes eUnitAI, DirectionTypes eFacingDirection);
	void disbandUnit(bool bAnnounce);

	void killUnits();
	bool hasTrait(int /*TraitTypes*/ iIndex);
	bool isHuman();
	bool isBarbarian();
	std::wstring getName();
	std::wstring getNameForm(int iForm);
	std::wstring getNameKey();
	std::wstring getCivilizationDescription(int iForm);
	std::wstring getCivilizationDescriptionKey();
	std::wstring getCivilizationShortDescription(int iForm);
	std::wstring getCivilizationShortDescriptionKey();
	std::wstring getCivilizationAdjective(int iForm);
	std::wstring getCivilizationAdjectiveKey();
	std::wstring getFlagDecal();
	bool isWhiteFlag();
	std::wstring getStateReligionName(int iForm);
	std::wstring getStateReligionKey();
	std::wstring getBestAttackUnitName(int iForm);
	std::wstring getWorstEnemyName();
	std::wstring getBestAttackUnitKey();
	int /*ArtStyleTypes*/ getArtStyleType();
	std::string getUnitButton(int eUnit);
	
	int findBestFoundValue();

	int countReligionSpreadUnits(CyArea* pArea, int /*ReligionTypes*/ eReligion);

	int countNumCoastalCities();
	int countNumCoastalCitiesByArea(CyArea* pArea);

	int countTotalCulture();
	int countOwnedBonuses(int /*BonusTypes*/ eBonus);
	int countUnimprovedBonuses(CyArea* pArea, CyPlot* pFromPlot);
	int countCityFeatures(int /*FeatureTypes*/ eFeature);
	int countNumBuildings(int /*BuildingTypes*/ eBuilding);
	int countPotentialForeignTradeCities(CyArea* pIgnoreArea);
	int countPotentialForeignTradeCitiesConnected();
	int countNumCitiesConnectedToCapital();

	bool canContact(int /*PlayerTypes*/ ePlayer);
	void contact(int /*PlayerTypes*/ ePlayer);
	bool canTradeWith(int /*PlayerTypes*/ eWhoTo);
	bool canTradeItem(int /*PlayerTypes*/ eWhoTo, TradeData item, bool bTestDenial);
	DenialTypes getTradeDenial(int /*PlayerTypes*/ eWhoTo, TradeData item);
	bool canTradeNetworkWith(int /*PlayerTypes*/ iPlayer);
	int getNumAvailableBonuses(int /*BonusTypes*/ eBonus);
	int getNumTradeableBonuses(int /*BonusTypes*/ eBonus);
	int getNumTradeBonusImports(int /*PlayerTypes*/ ePlayer);
	bool hasBonus(int /*BonusTypes*/ eBonus);

	bool canStopTradingWithTeam(int /*TeamTypes*/ eTeam);
	void stopTradingWithTeam(int /*TeamTypes*/ eTeam);
	void killAllDeals();
	bool isTurnActive( void );

	void findNewCapital();	
	int getNumGovernmentCenters();
	bool canRaze(CyCity* pCity);
	void raze(CyCity* pCity);
	void disband(CyCity* pCity);
	bool canReceiveGoody(CyPlot* pPlot, int /*GoodyTypes*/ eGoody, CyUnit* pUnit);
	void receiveGoody(CyPlot* pPlot, int /*GoodyTypes*/ eGoody, CyUnit* pUnit);
	void doGoody(CyPlot* pPlot, CyUnit* pUnit);
	bool canFound(int iX, int iY);
	void found(int iX, int iY);
	bool canTrain(int /*UnitTypes*/ eUnit, bool bContinue, bool bTestVisible);
	bool canConstruct(int /*BuildingTypes*/eBuilding, bool bContinue, bool bTestVisible, bool bIgnoreCost);
	bool canCreate(int /*ProjectTypes*/ eProject, bool bContinue, bool bTestVisible);
	bool canMaintain(int /*ProcessTypes*/ eProcess, bool bContinue);	
	bool isProductionMaxedUnitClass(int /*UnitClassTypes*/ eUnitClass);
	bool isProductionMaxedBuildingClass(int /*BuildingClassTypes*/ eBuildingClass, bool bAcquireCity);
	bool isProductionMaxedProject(int /*ProjectTypes*/ eProject);
	int getUnitProductionNeeded(int /*UnitTypes*/ iIndex);
	int getBuildingProductionNeeded(int /*BuildingTypes*/ iIndex);
	int getProjectProductionNeeded(int /*ProjectTypes*/ iIndex);

	void chooseTech(int iDiscover, std::wstring szText, bool bFront);

	int getBuildingClassPrereqBuilding(int /*BuildingTypes*/ eBuilding, int /*BuildingClassTypes*/ ePrereqBuildingClass, int iExtra);

	void removeBuildingClass(int /*BuildingClassTypes*/ eBuildingClass);
	bool canBuild(CyPlot* pPlot, int /*BuildTypes*/ eBuild, bool bTestEra, bool bTestVisible);
	int /*RouteTypes*/ getBestRoute(CyPlot* pPlot) const;
	int getImprovementUpgradeRate() const;

	int calculateTotalYield(int /*YieldTypes*/ eYield);
	int calculateTotalExports(int /*YieldTypes*/ eYield);
	int calculateTotalImports(int /*YieldTypes*/ eYield);

	int calculateTotalCityHappiness();
	int calculateTotalCityUnhappiness();

	int calculateTotalCityHealthiness();
	int calculateTotalCityUnhealthiness();

	int calculateUnitCost();
	int calculateUnitSupply();
	int calculatePreInflatedCosts();
	int calculateInflationRate();
	int calculateInflatedCosts();
	int calculateGoldRate();
	int calculateTotalCommerce();
	int calculateResearchRate(int /*TechTypes*/ eTech);
	int calculateResearchModifier(int /*TechTypes*/ eTech);
	int calculateBaseNetResearch();
	bool isResearch();
	bool canEverResearch(int /*TechTypes*/ eTech);
	bool canResearch(int /*TechTypes*/ eTech, bool bTrade);
	int /* TechTypes */ getCurrentResearch();
	bool isCurrentResearchRepeat();
	bool isNoResearchAvailable();
	int getResearchTurnsLeft(int /*TechTypes*/ eTech, bool bOverflow);

	bool isCivic(int /*CivicTypes*/ eCivic);
	bool canDoCivics(int /*CivicTypes*/ eCivic);
	bool canRevolution(int /*CivicTypes**/ paeNewCivics);
	void revolution(int /*CivicTypes**/ paeNewCivics, bool bForce);
	int getCivicPercentAnger(int /*CivicTypes*/ eCivic);

	bool canDoReligion(int /*ReligionTypes*/ eReligion);
	bool canChangeReligion();
	bool canConvert(int /*ReligionTypes*/ iIndex);
	void convert(int /*ReligionTypes*/ iIndex);
	bool hasHolyCity(int /*ReligionTypes*/ eReligion);
	int countHolyCities();

	void foundReligion(int /*ReligionTypes*/ eReligion, int /*ReligionTypes*/ iSlotReligion, bool bAward);
	int getCivicAnarchyLength(boost::python::list& /*CivicTypes**/ paeNewCivics);
	int getReligionAnarchyLength();

	bool hasHeadquarters(int /*CorporationTypes*/ eCorporation);
	int countHeadquarters();
	int countCorporations(int /*CorporationTypes*/ eCorporation);
	void foundCorporation(int /*CorporationTypes*/ eCorporation);

	int unitsRequiredForGoldenAge();
	int unitsGoldenAgeCapable();
	int unitsGoldenAgeReady();
	int greatPeopleThreshold(bool bMilitary);
	int specialistYield(int /*SpecialistTypes*/ eSpecialist, int /*YieldTypes*/ eCommerce);
	int specialistCommerce(int /*SpecialistTypes*/ eSpecialist, int /*CommerceTypes*/ eCommerce);

	CyPlot* getStartingPlot();
	void setStartingPlot(CyPlot* pPlot, bool bUpdateStartDist);
	int getTotalPopulation();
	int getAveragePopulation();
	long getRealPopulation();

	int getTotalLand();
	int getTotalLandScored();

	int getGold();
	void setGold(int iNewValue);
	void changeGold(int iChange);
	int getGoldPerTurn();

	int getAdvancedStartPoints();
	void setAdvancedStartPoints(int iNewValue);
	void changeAdvancedStartPoints(int iChange);
	int getAdvancedStartUnitCost(int /*UnitTypes*/ eUnit, bool bAdd, CyPlot* pPlot);
	int getAdvancedStartCityCost(bool bAdd, CyPlot* pPlot);
	int getAdvancedStartPopCost(bool bAdd, CyCity* pCity);
	int getAdvancedStartCultureCost(bool bAdd, CyCity* pCity);
	int getAdvancedStartBuildingCost(int /*BuildingTypes*/ eBuilding, bool bAdd, CyCity* pCity);
	int getAdvancedStartImprovementCost(int /*ImprovementTypes*/ eImprovement, bool bAdd, CyPlot* pPlot);
	int getAdvancedStartRouteCost(int /*RouteTypes*/ eRoute, bool bAdd, CyPlot* pPlot);
	int getAdvancedStartTechCost(int /*TechTypes*/ eTech, bool bAdd);
	int getAdvancedStartVisibilityCost(bool bAdd, CyPlot* pPlot);

	int getEspionageSpending(int /*PlayerTypes*/ ePlayer);
	bool canDoEspionageMission(int /*EspionageMissionTypes*/ eMission, int /*PlayerTypes*/ eTargetPlayer, CyPlot* pPlot, int iExtraData);
	int getEspionageMissionCost(int /*EspionageMissionTypes*/ eMission, int /*PlayerTypes*/ eTargetPlayer, CyPlot* pPlot, int iExtraData);
	void doEspionageMission(int /*EspionageMissionTypes*/ eMission, int /*PlayerTypes*/ eTargetPlayer, CyPlot* pPlot, int iExtraData, CyUnit* pUnit);

	int getEspionageSpendingWeightAgainstTeam(int /*TeamTypes*/ eIndex);
	void setEspionageSpendingWeightAgainstTeam(int /*TeamTypes*/ eIndex, int iValue);
	void changeEspionageSpendingWeightAgainstTeam(int /*TeamTypes*/ eIndex, int iChange);

	int getGoldenAgeTurns();
	int getGoldenAgeLength();
	bool isGoldenAge();
	void changeGoldenAgeTurns(int iChange);	
	int getNumUnitGoldenAges();
	void changeNumUnitGoldenAges(int iChange);	
	int getAnarchyTurns();
	bool isAnarchy();
	void changeAnarchyTurns(int iChange);
	int getStrikeTurns();
	int getMaxAnarchyTurns();
	int getAnarchyModifier();
	int getGoldenAgeModifier();
	int getHurryModifier();
	void createGreatPeople(int eGreatPersonUnit, bool bIncrementThreshold, bool bIncrementExperience, int iX, int iY);
	int getGreatPeopleCreated();
	int getGreatGeneralsCreated();
	int getGreatPeopleThresholdModifier();
	int getGreatGeneralsThresholdModifier();
	int getGreatPeopleRateModifier();
	int getGreatGeneralRateModifier();
	int getDomesticGreatGeneralRateModifier();
	int getStateReligionGreatPeopleRateModifier();

	int getMaxGlobalBuildingProductionModifier();
	int getMaxTeamBuildingProductionModifier();
	int getMaxPlayerBuildingProductionModifier();
	int getFreeExperience();
	int getFeatureProductionModifier();
	int getWorkerSpeedModifier();
	int getImprovementUpgradeRateModifier();
	int getMilitaryProductionModifier();
	int getSpaceProductionModifier();
	int getCityDefenseModifier();
	int getNumNukeUnits();
	int getNumOutsideUnits();
	int getBaseFreeUnits();
	int getBaseFreeMilitaryUnits();

	int getFreeUnitsPopulationPercent();
	int getFreeMilitaryUnitsPopulationPercent();
	int getGoldPerUnit();
	int getGoldPerMilitaryUnit();
	int getExtraUnitCost();
	int getNumMilitaryUnits();
	int getHappyPerMilitaryUnit();
	bool isMilitaryFoodProduction();
	int getHighestUnitLevel();

	int getConscriptCount();
	void setConscriptCount(int iNewValue);
	void changeConscriptCount(int iChange);

	int getMaxConscript();
	int getOverflowResearch();
	bool isNoUnhealthyPopulation();
	bool getExpInBorderModifier();
	bool isBuildingOnlyHealthy();

	int getDistanceMaintenanceModifier();
	int getNumCitiesMaintenanceModifier();
	int getCorporationMaintenanceModifier();
	int getTotalMaintenance();
	int getUpkeepModifier();
	int getLevelExperienceModifier() const;

	int getExtraHealth();
	int getBuildingGoodHealth();
	int getBuildingBadHealth();

	int getExtraHappiness();
	void changeExtraHappiness(int iChange);

	int getBuildingHappiness();
	int getLargestCityHappiness();
	int getWarWearinessPercentAnger();
	int getWarWearinessModifier();
	int getFreeSpecialist();
	bool isNoForeignTrade();
	bool isNoCorporations();
	bool isNoForeignCorporations();
	int getCoastalTradeRoutes();
	void changeCoastalTradeRoutes(int iChange);
	int getTradeRoutes();
	int getConversionTimer();
	int getRevolutionTimer();

	bool isStateReligion();
	bool isNoNonStateReligionSpread();
	int getStateReligionHappiness();
	int getNonStateReligionHappiness();
	int getStateReligionUnitProductionModifier();
	void changeStateReligionUnitProductionModifier(int iChange);
	int getStateReligionBuildingProductionModifier();
	void changeStateReligionBuildingProductionModifier(int iChange);
	int getStateReligionFreeExperience();
	CyCity* getCapitalCity();
	int getCitiesLost();

	int getWinsVsBarbs();

	int getAssets();
	void changeAssets(int iChange);
	int getPower();
	int getPopScore();
	int getLandScore();
	int getWondersScore();
	int getTechScore();
	int getTotalTimePlayed();
	bool isMinorCiv();
	bool isAlive();
	bool isEverAlive();
	bool isExtendedGame();
	bool isFoundedFirstCity();
	
	bool isStrike();

	int getID();
	int /* HandicapTypes */ getHandicapType();
	int /* CivilizationTypes */ getCivilizationType();
	int /*LeaderHeadTypes*/ getLeaderType();
	int /*LeaderHeadTypes*/ getPersonalityType();
	void setPersonalityType(int /*LeaderHeadTypes*/ eNewValue);
	int /*ErasTypes*/ getCurrentEra();
	void setCurrentEra(int /*EraTypes*/ iNewValue);

	int /*ReligonTypes*/ getStateReligion();
	void setLastStateReligion(int /*ReligionTypes*/ iNewReligion);

	int getTeam();
	
	int /*PlayerColorTypes*/ getPlayerColor();
	int getPlayerTextColorR();
	int getPlayerTextColorG();
	int getPlayerTextColorB();
	int getPlayerTextColorA();

	int getSeaPlotYield(YieldTypes eIndex);
	int getYieldRateModifier(YieldTypes eIndex);
	int getCapitalYieldRateModifier(YieldTypes eIndex);
	int getExtraYieldThreshold(YieldTypes eIndex);
	int getTradeYieldModifier(YieldTypes eIndex);
	int getFreeCityCommerce(CommerceTypes eIndex);
	int getCommercePercent(int /*CommerceTypes*/ eIndex);
	void setCommercePercent(CommerceTypes eIndex, int iNewValue);
	void changeCommercePercent(CommerceTypes eIndex, int iChange);
	int getCommerceRate(CommerceTypes eIndex);
	int getCommerceRateModifier(CommerceTypes eIndex);
	int getCapitalCommerceRateModifier(CommerceTypes eIndex);
	int getStateReligionBuildingCommerce(CommerceTypes eIndex);
	int getSpecialistExtraCommerce(CommerceTypes eIndex);

	bool isCommerceFlexible(int /*CommerceTypes*/ eIndex);
	int getGoldPerTurnByPlayer(int /*PlayerTypes*/ eIndex);
	void setGoldPerTurnByPlayer(int /*PlayerTypes*/ eIndex, int iValue);

	bool isFeatAccomplished(int /*FeatTypes*/ eIndex);	
	void setFeatAccomplished(int /*FeatTypes*/ eIndex, bool bNewValue);
	bool isOption(int /*PlayerOptionTypes*/ eIndex);	
	void setOption(int /*PlayerOptionTypes*/ eIndex, bool bNewValue);
	bool isLoyalMember(int /*VoteSourceTypes*/ eIndex);	
	void setLoyalMember(int /*VoteSourceTypes*/ eIndex, bool bNewValue);
	int getVotes(int /*VoteTypes*/ eVote, int /*VoteSourceTypes*/ eVoteSource);
	bool isFullMember(int /*VoteSourceTypes*/ eVoteSource) const;
	bool isVotingMember(int /*VoteSourceTypes*/ eVoteSource) const;
	bool isPlayable();
	void setPlayable(bool bNewValue);
	int getBonusExport(int /*BonusTypes*/ iIndex);
	int getBonusImport(int /*BonusTypes*/ iIndex);

	int getImprovementCount(int /*ImprovementTypes*/ iIndex);

	bool isBuildingFree(int /*BuildingTypes*/ iIndex);
	int getExtraBuildingHappiness(int /*BuildingTypes*/ iIndex);
	int getExtraBuildingHealth(int /*BuildingTypes*/ iIndex);
	int getFeatureHappiness(int /*FeatureTypes*/ iIndex);
	int getUnitClassCount(int /*UnitClassTypes*/ eIndex);
	bool isUnitClassMaxedOut(int /*UnitClassTypes*/ eIndex, int iExtra);
	int getUnitClassMaking(int /*UnitClassTypes*/ eIndex);
	int getUnitClassCountPlusMaking(int /*UnitClassTypes*/ eIndex);

	int getBuildingClassCount(int /*BuildingClassTypes*/ iIndex);
	bool isBuildingClassMaxedOut(int /*BuildingClassTypes*/ iIndex, int iExtra);
	int getBuildingClassMaking(int /*BuildingClassTypes*/ iIndex);
	int getBuildingClassCountPlusMaking(int /*BuildingClassTypes*/ iIndex);
	int getHurryCount(int /*HurryTypes*/ eIndex);
	bool canHurry(int /*HurryTypes*/ eIndex);
	int getSpecialBuildingNotRequiredCount(int /*SpecialBuildingTypes*/ eIndex);
	bool isSpecialBuildingNotRequired(int /*SpecialBuildingTypes*/ eIndex);

	bool isHasCivicOption(int /*CivicOptionTypes*/ eIndex);
	bool isNoCivicUpkeep(int /*CivicOptionTypes*/ iIndex);
	int getHasReligionCount(int /*ReligionTypes*/ eIndex);
	int countTotalHasReligion();
	int findHighestHasReligionCount();
	int getHasCorporationCount(int /*CorporationTypes*/ eIndex);
	int countTotalHasCorporation();

	int getUpkeepCount(int /*UpkeepTypes*/ eIndex);
	bool isSpecialistValid(int /*SpecialistTypes*/ iIndex);
	bool isResearchingTech(int /*TechTypes*/ iIndex);
	int /*CivicTypes*/ getCivics(int /*CivicOptionTypes*/ iIndex);
	int getSingleCivicUpkeep(int /*CivicTypes*/ eCivic, bool bIgnoreAnarchy);
	int getCivicUpkeep(boost::python::list&  /*CivicTypes*/ paiCivics, bool bIgnoreAnarchy);
	void setCivics(int /*CivicOptionTypes*/ eIndex, int /*CivicTypes*/ eNewValue);

	int getCombatExperience() const;
	void changeCombatExperience(int iChange);
	void setCombatExperience(int iExperience);

	int getSpecialistExtraYield(int /*SpecialistTypes*/ eIndex1, int /*YieldTypes*/ eIndex2);

	int findPathLength(int /*TechTypes*/ eTech, bool bCost);

	int getQueuePosition( int /*TechTypes*/ eTech );
	void clearResearchQueue();
	bool pushResearch(int /*TechTypes*/ iIndex, bool bClear);
	void popResearch(int /*TechTypes*/ eTech);
	int getLengthResearchQueue();
	void addCityName(std::wstring szName);
	int getNumCityNames();
	std::wstring getCityName(int iIndex);
	python::tuple firstCity(bool bRev);	// returns tuple of (CyCity, iterOut)
	python::tuple nextCity(int iterIn, bool bRev);		// returns tuple of (CyCity, iterOut)
	int getNumCities();
	CyCity* getCity(int iID);
	python::tuple firstUnit(bool bRev);	// returns tuple of (CyUnit, iterOut)
	python::tuple nextUnit(int iterIn, bool bRev);		// returns tuple of (CyUnit, iterOut)
	int getNumUnits();
	CyUnit* getUnit(int iID);
	python::tuple firstSelectionGroup(bool bRev);	// returns tuple of (CySelectionGroup, iterOut)
	python::tuple nextSelectionGroup(int iterIn, bool bRev);	// returns tuple of (CySelectionGroup, iterOut)
	int getNumSelectionGroups();
	CySelectionGroup* getSelectionGroup(int iID);

	void trigger(/*EventTriggerTypes*/int eEventTrigger);
	const EventTriggeredData* getEventOccured(int /*EventTypes*/ eEvent) const;
	void resetEventOccured(/*EventTypes*/ int eEvent);
	EventTriggeredData* getEventTriggered(int iID) const;
	EventTriggeredData* initTriggeredData(int /*EventTriggerTypes*/ eEventTrigger, bool bFire, int iCityId, int iPlotX, int iPlotY, int /*PlayerTypes*/ eOtherPlayer, int iOtherPlayerCityId, int /*ReligionTypes*/ eReligion, int /*CorporationTypes*/ eCorporation, int iUnitId, int /*BuildingTypes*/ eBuilding);
	int getEventTriggerWeight(int /*EventTriggerTypes*/ eTrigger);

	void AI_updateFoundValues(bool bStartingLoc);
	int AI_foundValue(int iX, int iY, int iMinUnitRange/* = -1*/, bool bStartingLoc/* = false*/);
	bool AI_isFinancialTrouble();
	bool AI_demandRebukedWar(int /*PlayerTypes*/ ePlayer);
	AttitudeTypes AI_getAttitude(int /*PlayerTypes*/ ePlayer);
	int AI_unitValue(int /*UnitTypes*/ eUnit, int /*UnitAITypes*/ eUnitAI, CyArea* pArea);
	int AI_civicValue(int /*CivicTypes*/ eCivic);
	int AI_totalUnitAIs(int /*UnitAITypes*/ eUnitAI);
	int AI_totalAreaUnitAIs(CyArea* pArea, int /*UnitAITypes*/ eUnitAI);
	int AI_totalWaterAreaUnitAIs(CyArea* pArea, int /*UnitAITypes*/ eUnitAI);
	int AI_getNumAIUnits(int /*UnitAITypes*/ eIndex);
	int AI_getAttitudeExtra(int /*PlayerTypes*/ eIndex);
	void AI_setAttitudeExtra(int /*PlayerTypes*/ eIndex, int iNewValue);
	void AI_changeAttitudeExtra(int /*PlayerTypes*/ eIndex, int iChange);
	int AI_getMemoryCount(int /*PlayerTypes*/ eIndex1, int /*MemoryTypes*/ eIndex2);
	void AI_changeMemoryCount(int /*PlayerTypes*/ eIndex1, int /*MemoryTypes*/ eIndex2, int iChange);
	int AI_getExtraGoldTarget() const;
	void AI_setExtraGoldTarget(int iNewValue);


	int getScoreHistory(int iTurn) const;
	int getEconomyHistory(int iTurn) const;
	int getIndustryHistory(int iTurn) const;
	int getAgricultureHistory(int iTurn) const;
	int getPowerHistory(int iTurn) const;
	int getCultureHistory(int iTurn) const;
	int getEspionageHistory(int iTurn) const;

	std::string getScriptData() const;
	void setScriptData(std::string szNewValue);

	int AI_maxGoldTrade(int iPlayer);
	int AI_maxGoldPerTurnTrade(int iPlayer);

	bool splitEmpire(int iAreaId);
	bool canSplitEmpire() const;
	bool canSplitArea(int iAreaId) const;

	bool canHaveTradeRoutesWith(int iPlayer);

	void forcePeace(int iPlayer);

private:
	CvPlayer* m_pPlayer;
};

#endif	// CyPlayer_h
