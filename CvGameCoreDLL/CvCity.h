#pragma once

#ifndef CIV4_CITY_H
#define CIV4_CITY_H

#include "CvDLLEntity.h"

class CvPlot;
class CvPlotGroup;
class CvArea;
class CvGenericBuilding;
class CvArtInfoBuilding;
class CvCityAI; // advc.003u
class CvCivilization; // advc.003w


class CvCity : public CvDLLCityEntity
{
public:
	virtual ~CvCity();

	void setupGraphical();
	void reloadEntity(); // advc.095
	void kill(bool bUpdatePlotGroups, /* advc.001: */ bool bBumpUnits = true);									// Exposed to Python
	void doTurn();
	void doRevolt(); // advc: previously in CvPlot::doCulture
	/*	K-Mod. public for the "insert culture" espionage mission.
		(I've also changed the functionality of it quite a bit.) */
	void doPlotCultureTimes100(bool bUpdate, PlayerTypes ePlayer, int iCultureRateTimes100, bool bCityCulture);
	/*	advc.120j: Was 10 as a local variable (doPlotCultureTimes100).
		Should still be 10. */
	static int plotCultureScale()
	{
		return GC.getNumCultureLevelInfos() + plotCultureExtraRange();
	}
	// advc.ctr: Replacing local variable in doPlotCultureTimes100
	static int plotCultureExtraRange()
	{
		return 3;
	}

	bool isCitySelected();
	DllExport bool canBeSelected() const;
	DllExport void updateSelectedCity(bool bTestProduction);
	void setInvestigate(bool b); // advc.103

	void updateYield();
	void updateVisibility();

	void createGreatPeople(UnitTypes eGreatPersonUnit, bool bIncrementThreshold,								// Exposed to Python
			 bool bIncrementExperience) const;
	void doTask(TaskTypes eTask, int iData1 = -1, int iData2 = -1, bool bOption = false,						// Exposed to Python
			bool bAlt = false, bool bShift = false, bool bCtrl = false);
	void chooseProduction(UnitTypes eTrainUnit = NO_UNIT,														// Exposed to Python
			BuildingTypes eConstructBuilding = NO_BUILDING,
			ProjectTypes eCreateProject = NO_PROJECT,
			bool bFinish = false, bool bFront = false);
	// <advc.003u> Moved from CvCityAI b/c it's also used to trigger human choose-production popups
	bool isChooseProductionDirty() const
	{
		return m_bChooseProductionDirty;
	}
	void setChooseProductionDirty(bool bNewValue)
	{
		m_bChooseProductionDirty = bNewValue;
	} // </advc.003u>

	CityPlotTypes getCityPlotIndex(CvPlot const& kPlot) const;													// Exposed to Python
	CvPlot* getCityIndexPlot(CityPlotTypes ePlot) const;														// Exposed to Python

	bool canWork(CvPlot const& kPlot) const;																	// Exposed to Python
	void verifyWorkingPlot(CityPlotTypes ePlot);
	void verifyWorkingPlots();
	void clearWorkingOverride(CityPlotTypes ePlot);																// Exposed to Python
	int countNumImprovedPlots(ImprovementTypes eImprovement = NO_IMPROVEMENT, bool bPotential = false) const;																			// Exposed to Python
	int countNumBonusPlots(BonusTypes eBonus = NO_BONUS) const; // 1SDAN																		// Exposed to Python
	int countNumWaterPlots() const;																				// Exposed to Python
	int countNumRiverPlots() const;																				// Exposed to Python

	int findPopulationRank() const;																				// Exposed to Python
	int findBaseYieldRateRank(YieldTypes eYield) const;															// Exposed to Python
	int findYieldRateRank(YieldTypes eYield) const;																// Exposed to Python
	int findCommerceRateRank(CommerceTypes eCommerce) const;													// Exposed to Python

	UnitTypes allUpgradesAvailable(UnitTypes eUnit, int iUpgradeCount = 0,										// Exposed to Python
			BonusTypes eAssumeVailable = NO_BONUS) const; // advc.001u
	bool isWorldWondersMaxed() const;																			// Exposed to Python
	bool isTeamWondersMaxed() const;																			// Exposed to Python
	bool isNationalWondersMaxed() const;																		// Exposed to Python
	int getNumNationalWondersLeft() const; // advc.004w, advc.131
	bool isBuildingsMaxed() const;																				// Exposed to Python

	void verifyProduction(); // advc.064d: public wrapper for doCheckProduction
	bool canTrain(UnitTypes eUnit, bool bContinue = false, bool bTestVisible = false,							// Exposed to Python
			bool bIgnoreCost = false, bool bIgnoreUpgrades = false,
			bool bCheckAirUnitCap = true, // advc.001b
			BonusTypes eAssumeVailable = NO_BONUS) const; // advc.001u
	bool canUpgradeTo(UnitTypes eUnit) const; // advc.001b
	bool canTrain(UnitCombatTypes eUnitCombat) const;
	bool canConstruct(BuildingTypes eBuilding, bool bContinue = false,											// Exposed to Python
			bool bTestVisible = false, bool bIgnoreCost = false,
			bool bIgnoreTech = false) const; // K-Mod
	bool canCreate(ProjectTypes eProject, bool bContinue = false, bool bTestVisible = false) const;				// Exposed to Python
	bool canMaintain(ProcessTypes eProcess, bool bContinue = false) const;										// Exposed to Python
	bool canJoin() const;																						// Exposed to Python

	int getFoodTurnsLeft() const;																				// Exposed to Python
	bool isProduction() const { return (headOrderQueueNode() != NULL); }										// Exposed to Python
	bool isProductionLimited() const;																			// Exposed to Python
	bool isProductionUnit() const;																				// Exposed to Python
	bool isProductionBuilding() const;																			// Exposed to Python
	bool isProductionProject() const;																			// Exposed to Python
	bool isProductionProcess() const;																			// Exposed to Python

	bool canContinueProduction(OrderData order);																// Exposed to Python
	int getProductionExperience(UnitTypes eUnit = NO_UNIT,														// Exposed to Python
			bool bScore = false) const; // advc.002f
	void addProductionExperience(CvUnit* pUnit, bool bConscript = false);										// Exposed to Python

	UnitTypes getProductionUnit() const;																		// Exposed to Python
	UnitAITypes getProductionUnitAI() const;																	// Exposed to Python
	BuildingTypes getProductionBuilding() const;																// Exposed to Python
	ProjectTypes getProductionProject() const;																	// Exposed to Python
	ProcessTypes getProductionProcess() const;																	// Exposed to Python
	const wchar* getProductionName() const;																		// Exposed to Python
	const wchar* getProductionNameKey() const;																	// Exposed to Python

	bool isFoodProduction() const;																				// Exposed to Python
	bool isFoodProduction(UnitTypes eUnit) const;																// Exposed to Python
	int getFirstUnitOrder(UnitTypes eUnit) const;																// Exposed to Python
	int getFirstBuildingOrder(BuildingTypes eBuilding) const;													// Exposed to Python
	int getFirstProjectOrder(ProjectTypes eProject) const;														// Exposed to Python
	int getNumTrainUnitAI(UnitAITypes eUnitAI) const;															// Exposed to Python

	int getProduction() const;																					// Exposed to Python
	int getProductionNeeded() const;																			// Exposed to Python
	int getProductionNeeded(UnitTypes eUnit) const;
	int getProductionNeeded(BuildingTypes eBuilding) const;
	int getProductionNeeded(ProjectTypes eProject) const;
	//int getGeneralProductionTurnsLeft() const; // advc: Redundant; use the function below.					// Exposed to Python
	int getProductionTurnsLeft() const;																			// Exposed to Python
	int getProductionTurnsLeft(UnitTypes eUnit, int iNum) const;												// Exposed to Python
	int getProductionTurnsLeft(BuildingTypes eBuilding, int iNum) const;										// Exposed to Python
	int getProductionTurnsLeft(ProjectTypes eProject, int iNum) const;											// Exposed to Python
	int getProductionTurnsLeft(int iProductionNeeded, int iProduction,
			int iFirstProductionDifference, int iProductionDifference) const;
	int sanitizeProductionTurns(int iTurns, OrderTypes eOrder = NO_ORDER,
			int iData = -1, bool bAssert = false) const; // advc.004x
	void setProduction(int iNewValue);																			// Exposed to Python
	void changeProduction(int iChange);																			// Exposed to Python

	int getProductionModifier() const;																			// Exposed to Python
	int getProductionModifier(UnitTypes eUnit) const;															// Exposed to Python
	int getProductionModifier(BuildingTypes eBuilding, bool bHurry = false) const;											// Exposed to Python
	int getProductionModifier(ProjectTypes eProject) const;														// Exposed to Python
	// advc.003j: Vanilla Civ 4 declaration that never had an implementation
	//int getOverflowProductionDifference(int iProductionNeeded, int iProduction, int iProductionModifier, int iDiff, int iModifiedProduction) const;
	int getProductionDifference(int iProductionNeeded, int iProduction,
			int iProductionModifier, bool bFoodProduction, bool bOverflow,
			// <advc.064bc>
			bool bIgnoreFeatureProd = false, bool bIgnoreYieldRate = false,
			bool bForceFeatureProd = false, int* piFeatureProd = NULL) const;
			// </advc.064bc>
	int getCurrentProductionDifference(bool bIgnoreFood, bool bOverflow,										// Exposed to Python
			// <advc.064bc>
			bool bIgnoreFeatureProd = false, bool bIgnoreYieldRate = false,
			bool bForceFeatureProd = false, int* iFeatureProdReturn = NULL) const;
			// </advc.064bc>
	int getExtraProductionDifference(int iExtra) const															// Exposed to Python
	{
		return getExtraProductionDifference(iExtra, getProductionModifier());
	}

	bool canHurry(HurryTypes eHurry, bool bTestVisible = false) const;											// Exposed to Python
	void hurry(HurryTypes eHurry);																				// Exposed to Python
	// <advc.064b>
	int overflowCapacity(int iProductionModifier, int iPopulationChange = 0) const;
	int computeOverflow(int iRawOverflow, int iProductionModifier, OrderTypes eOrderType,
			int* piProductionGold = NULL, int* piLostProduction = NULL,
			int iPopulationChange = 0) const;
	int minPlotProduction() const
	{	// Let pop-hurry ignore guaranteed production
		return 0;/*GC.getInfo(YIELD_PRODUCTION).getMinCity()*/
	} // (exposed to Python) </advc.064b>  <advc.064>
	bool hurryOverflow(HurryTypes eHurry, int* piProduction, int* piGold,
			bool bCountThisTurn = false) const;		// (exposed to Python)
	// </advc.064>
	// <advc.912d>
	bool canPopRush() const;
	void changePopRushCount(int iChange);
	// </advc.912d>
	UnitTypes getConscriptUnit() const;																			// Exposed to Python
	CvUnit* initConscriptedUnit();
	int getConscriptPopulation() const;																			// Exposed to Python
	int conscriptMinCityPopulation() const;																		// Exposed to Python
	int flatConscriptAngerLength() const;																		// Exposed to Python
	bool canConscript(bool bForce = false) const;																				// Exposed to Python
	void conscript(bool bForce = false);																											// Exposed to Python

	int getBonusHealth(BonusTypes eBonus) const;																// Exposed to Python
	int getBonusHappiness(BonusTypes eBonus) const;																// Exposed to Python
	int getBonusPower(BonusTypes eBonus, bool bDirty) const;													// Exposed to Python
	int getBonusYieldRateModifier(YieldTypes eYield, BonusTypes eBonus) const;									// Exposed to Python
	int getBonusCommerceRateModifier(CommerceTypes eIndex, BonusTypes eBonus) const; // doc

	void processBonus(BonusTypes eBonus, int iChange);
	void processBuilding(BuildingTypes eBuilding, int iChange, bool bObsolete = false);
	void processPlayerBuilding(BuildingTypes eBuilding, int iChange);
	void processProcess(ProcessTypes eProcess, int iChange);
	void processSpecialist(SpecialistTypes eSpecialist, int iChange);
	void processVoteSource(VoteSourceTypes eVoteSource, bool bActive);

	void processPlayerBuildingEffects(int iChange);
	void processPlayerBuildingEffect(BuildingTypes eBuilding, int iChange);

	HandicapTypes getHandicapType() const;																		// Exposed to Python
	CivilizationTypes getCivilizationType() const;																// Exposed to Python
	CvCivilization const& getCivilization() const; // advc.003w
	LeaderHeadTypes getPersonalityType() const;																	// Exposed to Python
	DllExport ArtStyleTypes getArtStyleType() const;															// Exposed to Python
	CitySizeTypes getCitySizeType() const;																		// Exposed to Python
	DllExport const CvArtInfoBuilding* getBuildingArtInfo(BuildingTypes eBuilding) const;
	DllExport float getBuildingVisibilityPriority(BuildingTypes eBuilding) const;

	bool hasTrait(TraitTypes eTrait) const;																		// Exposed to Python
	bool isBarbarian() const;
	bool isIndependent() const; // doc																			// Exposed to Python
	bool isMinorCiv() const; // doc
	bool isHuman() const;																						// Exposed to Python
	DllExport bool isVisible(TeamTypes eTeam, bool bDebug) const;												// Exposed to Python
	// advc: Make bDebug=false the default
	bool isVisible(TeamTypes eTeam) const
	{
		return isVisible(eTeam, false);
	}

	bool isCapital() const;																						// Exposed to Python
	bool isPrereqBonusSea() const; // advc
	/* advc: -1 means use MIN_WATER_SIZE_FOR_OCEAN. Removed MIN_WATER_SIZE_FOR_OCEAN
	   from all calls to this function (except those from Python). */
	bool isCoastal(int iMinWaterSize = -1) const;																// Exposed to Python
	bool isDisorder() const;																					// Exposed to Python
	bool isNoMaintenance() const; //advc
	bool isHolyCity(ReligionTypes eReligion) const;																// Exposed to Python
	bool isHolyCity() const;																					// Exposed to Python
	bool hasShrine(ReligionTypes eReligion) const
	{	// advc.enum: Replacing implementation based on a cache at CvGame
		return (m_aiShrine.get(eReligion) > 0);
	}
	bool isHeadquarters(CorporationTypes eCorp) const;															// Exposed to Python
	bool isHeadquarters() const;																				// Exposed to Python
	void setHeadquarters(CorporationTypes eCorp);

	int getOvercrowdingPercentAnger(int iExtra = 0) const;														// Exposed to Python
	int getNoMilitaryPercentAnger() const;																		// Exposed to Python
	int getCulturePercentAnger() const;																			// Exposed to Python
	int getReligionPercentAnger() const;																		// Exposed to Python
	/*  advc.104: Moved parts of getReligionPercentAnger() into a subroutine.
		getReligionPercentAnger(PlayerTypes) doesn't check if the city owner is
		at war with ePlayer; can be used for predicting anger caused by a DoW. */
	scaled getReligionPercentAnger(PlayerTypes ePlayer) const;
	int getHurryPercentAnger(int iExtra = 0) const;																// Exposed to Python
	int getConscriptPercentAnger(int iExtra = 0) const;															// Exposed to Python
	int getDefyResolutionPercentAnger(int iExtra = 0) const;
	int getWarWearinessPercentAnger() const;																	// Exposed to Python
	int getLargestCityHappiness() const;																		// Exposed to Python
	int getVassalHappiness() const;																				// Exposed to Python
	int getVassalUnhappiness() const;																			// Exposed to Python
	int unhappyLevel(int iExtra = 0) const;																		// Exposed to Python
	int happyLevel() const;																						// Exposed to Python
	int angryPopulation(int iExtra = 0, /* advc.104: */ bool bIgnoreCultureRate = false) const;					// Exposed to Python
	int visiblePopulation() const;
	int totalFreeSpecialists() const;																			// Exposed to Python
	int extraPopulation() const;																				// Exposed to Python
	int extraSpecialists() const;																				// Exposed to Python
	int extraFreeSpecialists() const;																			// Exposed to Python

	int unhealthyPopulation(bool bNoAngry = false, int iExtra = 0) const;										// Exposed to Python
	int totalGoodBuildingHealth() const;																		// Exposed to Python
	int totalBadBuildingHealth() const;																			// Exposed to Python
	int goodHealth() const;																						// Exposed to Python
	int badHealth(bool bNoAngry = false, int iExtra = 0) const;													// Exposed to Python
	int healthRate(bool bNoAngry = false, int iExtra = 0) const;												// Exposed to Python
	int foodConsumption(bool bNoAngry = false, int iExtra = 0) const;											// Exposed to Python
	int foodDifference(bool bBottom = true, bool bIgnoreProduction = false) const;	// Exposed to Python, K-Mod added bIgnoreProduction
	int growthThreshold(/* <advc.064b> */int iPopulationChange = 0,												// Exposed to Python
			bool bIgnoreModifiers = false) const; // </advc.064b>

	int productionLeft() const { return (getProductionNeeded() - getProduction()); }							// Exposed to Python
	int hurryCost(bool bExtra) const																			// Exposed to Python
	{
		return getHurryCost(bExtra, productionLeft(),
				getHurryCostModifier(), getProductionModifier());
	}
	int getHurryCostModifier(bool bIgnoreNew = false) const;
	int hurryGold(HurryTypes eHurry) const																		// Exposed to Python
	{
		return getHurryGold(eHurry, hurryCost(false));
	}
	int hurryPopulation(HurryTypes eHurry) const																// Exposed to Python
	{
		return getHurryPopulation(eHurry, hurryCost(true));
	}
	int hurryProduction(HurryTypes eHurry) const;																// Exposed to Python
	int flatHurryAngerLength() const;																			// Exposed to Python
	int hurryAngerLength(HurryTypes eHurry) const;																// Exposed to Python
	int maxHurryPopulation() const;																				// Exposed to Python

	static int cultureDistance(int iDX, int iDY); // advc: static												// Exposed to Python
	enum GrievanceTypes { GRIEVANCE_HURRY, GRIEVANCE_CONSCRIPT, GRIEVANCE_RELIGION }; // advc.101
	int cultureStrength(PlayerTypes ePlayer,																	// Exposed to Python
			bool bIgnoreWar = false, bool bIgnoreOccupation = false, // advc.023
			std::vector<GrievanceTypes>* paGrievances = NULL) const; // advc.101
	int cultureGarrison(PlayerTypes ePlayer) const;																// Exposed to Python
	PlayerTypes calculateCulturalOwner() const; // advc.099c

	bool hasBuilding(BuildingTypes eIndex) const; // rfc								// Exposed to Python
	bool hasActiveBuilding(BuildingTypes eIndex) const;	// rfc					// Exposed to Python

	int getNumBuilding(BuildingTypes eBuilding) const;															// Exposed to Python
	int getNumBuilding(BuildingClassTypes eBuildingClass) const; // advc.003w
	int getNumActiveBuilding(BuildingTypes eBuilding) const;													// Exposed to Python
	bool hasActiveWorldWonder() const																			// Exposed to Python
	{
		return (getNumActiveWorldWonders(1) > 0); // advc
	}
	// UNOFFICIAL_PATCH, Bugfix, 03/04/10, Mongoose & jdog5000:
	int getNumActiveWorldWonders(/* advc: */ int iStopCountAt = MAX_INT,
			PlayerTypes eOwner = NO_PLAYER) const; // advc.104d: Hypothetical owner

	// TODO: doc getReligionCount has bCountLocal
	int getReligionCount() const { return m_abHasReligion.numNonDefault(); } // advc.opt							// Exposed to Python
	int getCorporationCount() const { return m_abHasCorporation.numNonDefault(); } // advc.opt					// Exposed to Python
	static CvCity* fromIDInfo(IDInfo id); // advc
	// <advc.inl>
	DllExport int getID() const { return m_iID; }																// Exposed to Python
	int getIndex() const { return (getID() & FLTA_INDEX_MASK); }
	DllExport IDInfo getIDInfo() const { return IDInfo(getOwner(), getID()); }
	// </advc.inl>
	void setID(int iID);
	PlotNumTypes plotNum() const { return m_ePlot; } // advc.104

	int getRegionID() const; // doc
	int getRegionGroup() const; // doc

	DllExport int getX() const { return m_iX; } // advc.inl: was "getX_INLINE"									// Exposed to Python
	DllExport int getY() const { return m_iY; } // advc.inl: was "getY_INLINE"									// Exposed to Python

	bool at(int iX, int iY) const  { return (getX() == iX && getY() == iY); }									// Exposed to Python
	bool at(CvPlot const* pPlot) const // advc: const CvPlot*													// Exposed to Python as atPlot
	{
		return (plot() == pPlot);
	}  // <advc>
	bool at(CvPlot const& kPlot) const
	{
		return (plot() == &kPlot);
	} // </advc>
	DllExport CvPlot* plot() const { return m_pPlot; } // advc.opt: cached										// Exposed to Python
	CvPlot& getPlot() const { return *m_pPlot; } // advc
	void updatePlot(); // advc.opt
	CvPlotGroup* plotGroup(PlayerTypes ePlayer) const;
	bool isConnectedTo(CvCity const& kCity) const;																// Exposed to Python
	bool isConnectedToCapital(PlayerTypes ePlayer = NO_PLAYER) const;											// Exposed to Python
	// <advc>
	CvArea* area() const { return m_pArea; }																	// Exposed to Python
	//int getArea() const;
	CvArea& getArea() const { return *m_pArea; }
	bool isArea(CvArea const& kArea) const { return (area() == &kArea); }
	bool sameArea(CvCity const& kOther) const { return (area() == kOther.area()); }
	void updateArea();
	// </advc>
	// BETTER_BTS_AI_MOD, 01/02/09, jdog5000: START
	CvArea* waterArea(bool bNoImpassable = false) const;														// Exposed to Python
	CvArea* secondWaterArea() const;
	CvArea* sharedWaterArea(CvCity* pCity) const;
	CvArea* continentArea() const; // doc
	CvArea& getContinentArea() const; // doc
	bool isBlockaded() const;
	// BETTER_BTS_AI_MOD: END

	CvPlot* getRallyPlot() const;																				// Exposed to Python
	void setRallyPlot(CvPlot* pPlot);

	int getGameTurnFounded() const { return m_iGameTurnFounded; }												// Exposed to Python
	void setGameTurnFounded(int iNewValue);
	int getGameTurnAcquired() const { return m_iGameTurnAcquired; }												// Exposed to Python
	void setGameTurnAcquired(int iNewValue);

	int getPopulation() const { return m_iPopulation; }															// Exposed to Python
	void setPopulation(int iNewValue);																			// Exposed to Python
	void changePopulation(int iChange);																			// Exposed to Python
	int getRealPopulation() const;																				// Exposed to Python
	int getHighestPopulation() const { return m_iHighestPopulation; }											// Exposed to Python
	void setHighestPopulation(int iNewValue);
	int getWorkingPopulation() const { return m_iWorkingPopulation; }											// Exposed to Python
	void changeWorkingPopulation(int iChange);
	int getSpecialistPopulation() const { return m_iSpecialistPopulation; }										// Exposed to Python
	void changeSpecialistPopulation(int iChange);

	int getNumGreatPeople() const { return m_iNumGreatPeople; }													// Exposed to Python
	void changeNumGreatPeople(int iChange);
	int getBaseGreatPeopleRate() const { return m_iBaseGreatPeopleRate; }										// Exposed to Python
	int getGreatPeopleRate() const;																				// Exposed to Python
	int getTotalGreatPeopleRateModifier() const;																// Exposed to Python
	void changeBaseGreatPeopleRate(int iChange);																// Exposed to Python
	int getGreatPeopleRateModifier() const;																		// Exposed to Python
	void changeGreatPeopleRateModifier(int iChange);
	// BUG - Building Additional Great People - start
	int getAdditionalGreatPeopleRateByBuilding(BuildingTypes eBuilding) const;
	int getAdditionalBaseGreatPeopleRateByBuilding(BuildingTypes eBuilding) const;
	int getAdditionalGreatPeopleRateModifierByBuilding(BuildingTypes eBuilding) const;
	// BUG - Building Additional Great People - end
	// BUG - Specialist Additional Great People - start
	int getAdditionalGreatPeopleRateBySpecialist(SpecialistTypes eSpecialist, int iChange = 1) const;
	int getAdditionalBaseGreatPeopleRateBySpecialist(SpecialistTypes eSpecialist, int iChange = 1) const;
	// BUG - Specialist Additional Great People - end
	int getGreatPeopleProgress() const { return m_iGreatPeopleProgress; }										// Exposed to Python
	void changeGreatPeopleProgress(int iChange);																// Exposed to Python

	int getNumWorldWonders() const { return m_iNumWorldWonders; }												// Exposed to Python
	void changeNumWorldWonders(int iChange);
	int getNumTeamWonders() const { return m_iNumTeamWonders; }													// Exposed to Python
	void changeNumTeamWonders(int iChange);
	int getNumNationalWonders() const { return m_iNumNationalWonders; }											// Exposed to Python
	void changeNumNationalWonders(int iChange);
	int getNumBuildings() const { return m_iNumBuildings; }														// Exposed to Python
	void changeNumBuildings(int iChange);

	int getGovernmentCenterCount() const { return m_iGovernmentCenterCount; }
	bool isGovernmentCenter() const { return (getGovernmentCenterCount() > 0); }								// Exposed to Python
	void changeGovernmentCenterCount(int iChange);
	// BUG - Building Saved Maintenance:
	int getSavedMaintenanceTimes100ByBuilding(BuildingTypes eBuilding) const;
	int getMaintenance() const { return m_iMaintenance / 100; }													// Exposed to Python
	int getMaintenanceTimes100() const { return m_iMaintenance; }												// Exposed to Python
	void updateMaintenance();
	int calculateDistanceMaintenance() const;																	// Exposed to Python
	int calculateNumCitiesMaintenance() const;																	// Exposed to Python
	int calculateColonyMaintenance() const;																		// Exposed to Python
	int calculateCorporationMaintenance() const;																// Exposed to Python
	/* <advc.104> Added an optional parameter to allow the computation of
	   projected maintenance for cities yet to be conquered. */
	int calculateDistanceMaintenanceTimes100(PlayerTypes eOwner = NO_PLAYER) const;								// Exposed to Python
	int calculateColonyMaintenanceTimes100(PlayerTypes eOwner = NO_PLAYER) const;								// Exposed to Python
	int calculateNumCitiesMaintenanceTimes100(PlayerTypes eOwner = NO_PLAYER) const;							// Exposed to Python
	// </advc.104>
	// <advc.004b> A projection for cities yet to be founded
	static int calculateDistanceMaintenanceTimes100(CvPlot const& kCityPlot,
			PlayerTypes eOwner, int iPopulation = -1,
			bool bNoPlayerModifiers = false);
	static int calculateNumCitiesMaintenanceTimes100(CvPlot const& kCityPlot,
			PlayerTypes eOwner, int iPopulation = -1, int iExtraCities = 0);
	static int calculateColonyMaintenanceTimes100(CvPlot const& kCityPlot,
			PlayerTypes eOwner, int iPopulation = -1, int iExtraCities = 0);
	static int initialPopulation();
	// </advc.004b>
	int calculateCorporationMaintenanceTimes100(CorporationTypes eCorporation) const;							// Exposed to Python
	int calculateCorporationMaintenanceTimes100() const;														// Exposed to Python
	int calculateBaseMaintenanceTimes100(
			PlayerTypes eOwner = NO_PLAYER) const; // advc.ctr
	int getMaintenanceModifier() const { return m_iMaintenanceModifier; }										// Exposed to Python
	void changeMaintenanceModifier(int iChange);

	int getWarWearinessModifier() const { return m_iWarWearinessModifier; }										// Exposed to Python
	void changeWarWearinessModifier(int iChange);
	int getHurryAngerModifier() const { return m_iHurryAngerModifier; }											// Exposed to Python
	void changeHurryAngerModifier(int iChange);

	int getHealRate() const { return m_iHealRate; }																// Exposed to Python
	void changeHealRate(int iChange);

	int getEspionageHealthCounter() const { return m_iEspionageHealthCounter; }									// Exposed to Python
	void changeEspionageHealthCounter(int iChange);																// Exposed to Python
	int getEspionageHappinessCounter() const { return m_iEspionageHappinessCounter; }							// Exposed to Python
	void changeEspionageHappinessCounter(int iChange);															// Exposed to Python

	int getFreshWaterGoodHealth() const { return m_iFreshWaterGoodHealth; }										// Exposed to Python
	int getFreshWaterBadHealth() const { return m_iFreshWaterBadHealth; }										// Exposed to Python
	void updateFreshWaterHealth();
	// advc.901: Renamed everything with "featureHealth/Happiness" in its name
	int getSurroundingGoodHealth() const { return m_iSurroundingGoodHealth; }									// Exposed to Python
	int getSurroundingBadHealth() const { return m_iSurroundingBadHealth; }										// Exposed to Python
	void updateSurroundingHealthHappiness();
	// <advc.901>
	void calculateHealthHappyChange(CvPlot const& kPlot, ImprovementTypes eNewImprov,
			ImprovementTypes eOldImprov, bool bRemoveFeature, int& iHappyChange,
			int& iHealthChange, int& iHealthPercentChange) const;
	void goodBadHealthHappyChange(CvPlot const& kPlot, ImprovementTypes eNewImprov,
			ImprovementTypes eOldImprov, bool bRemoveFeature, int& iHappyChange,
			int& iUnhappyChange, int& iGoodHealthChange, int& iBadHealthChange,
			int& iGoodHealthPercentChange, int& iBadHealthPercentChange) const;
	// </advc.901>
	// BUG - Actual Effects - start
	int getAdditionalAngryPopuplation(int iGood, int iBad) const;
	int getAdditionalSpoiledFood(int iGood, int iBad) const;
	int getAdditionalStarvation(int iSpoiledFood) const;
	// BUG - Actual Effects - end
	// <advc.001c>
	int GPTurnsLeft() const;
	void GPProjection(std::vector<std::pair<UnitTypes,int> >& aeiProjection) const; // (exposed to Python)
	// </advc.001c>
	int getBuildingGoodHealth() const { return m_iBuildingGoodHealth; }											// Exposed to Python
	int getBuildingBadHealth() const { return m_iBuildingBadHealth; }											// Exposed to Python
	int getBuildingHealth(BuildingTypes eBuilding) const;														// Exposed to Python
	int getBuildingGoodHealth(BuildingTypes eBuilding) const;
	int getBuildingBadHealth(BuildingTypes eBuilding) const;
	void changeBuildingGoodHealth(int iChange);
	void changeBuildingBadHealth(int iChange);

	int getPowerGoodHealth() const { return m_iPowerGoodHealth; }												// Exposed to Python
	int getPowerBadHealth() const { return m_iPowerBadHealth; }													// Exposed to Python
	void updatePowerHealth();

	int getBonusGoodHealth() const { return m_iBonusGoodHealth; }												// Exposed to Python
	int getBonusBadHealth() const { return m_iBonusBadHealth; }													// Exposed to Python
	void changeBonusGoodHealth(int iChange);
	void changeBonusBadHealth(int iChange);

	int getMilitaryHappiness() const;																			// Exposed to Python
	int getMilitaryHappinessUnits() const { return m_iMilitaryHappinessUnits; }									// Exposed to Python
	void changeMilitaryHappinessUnits(int iChange);
	void updateMilitaryHappinessUnits(); // advc.184

	int getBuildingGoodHappiness() const { return m_iBuildingGoodHappiness; }									// Exposed to Python
	int getBuildingBadHappiness() const { return m_iBuildingBadHappiness; }										// Exposed to Python
	int getBuildingHappiness(BuildingTypes eBuilding) const;							// Exposed to Python
	void changeBuildingGoodHappiness(int iChange);
	void changeBuildingBadHappiness(int iChange);

	int getExtraBuildingGoodHappiness() const { return m_iExtraBuildingGoodHappiness; }							// Exposed to Python
	int getExtraBuildingBadHappiness() const { return m_iExtraBuildingBadHappiness; }							// Exposed to Python
	void updateExtraBuildingHappiness();
	// BETTER_BTS_AI_MOD, from BUG, 02/24/10, EmperorFool:
	int getAdditionalHappinessByBuilding(BuildingTypes eBuilding, int& iGood, int& iBad) const;

	int getExtraBuildingGoodHealth() const { return m_iExtraBuildingGoodHealth; }								// Exposed to Python
	int getExtraBuildingBadHealth() const { return m_iExtraBuildingBadHealth; }									// Exposed to Python
	void updateExtraBuildingHealth();

	// BETTER_BTS_AI_MOD, from BUG, 02/24/10, EmperorFool:
	int getAdditionalHealthByBuilding(BuildingTypes eBuilding, int& iGood, int& iBad,
			bool bAssumeStrategicBonuses = false) const; // advc.001h

	int getSurroundingGoodHappiness() const { return m_iSurroundingGoodHappiness; }								// Exposed to Python
	int getSurroundingBadHappiness() const { return m_iSurroundingBadHappiness; }								// Exposed to Python
	//void updateFeatureHappiness(); // advc.901: Replaced by updateSurroundingHealthHappiness

	int getBonusGoodHappiness(/* advc.912c: */ bool bIgnoreModifier = false) const;								// Exposed to Python
	int getBonusBadHappiness() const { return m_iBonusBadHappiness; }											// Exposed to Python
	void changeBonusGoodHappiness(int iChange);
	void changeBonusBadHappiness(int iChange);

	int getReligionGoodHappiness() const { return m_iReligionGoodHappiness; }									// Exposed to Python
	int getReligionBadHappiness() const { return m_iReligionBadHappiness; }										// Exposed to Python
	int getReligionHappiness(ReligionTypes eReligion) const;													// Exposed to Python
	void updateReligionHappiness();

	int getExtraHappiness() const { return m_iExtraHappiness; }													// Exposed to Python
	void changeExtraHappiness(int iChange);																		// Exposed to Python
	int getExtraHealth() const { return m_iExtraHealth; }														// Exposed to Python
	void changeExtraHealth(int iChange);																		// Exposed to Python

	int getHurryAngerTimer() const { return m_iHurryAngerTimer; }												// Exposed to Python
	void changeHurryAngerTimer(int iChange);																	// Exposed to Python
	int getConscriptAngerTimer() const { return m_iConscriptAngerTimer; }										// Exposed to Python
	void changeConscriptAngerTimer(int iChange);																// Exposed to Python
	int getDefyResolutionAngerTimer() const { return m_iDefyResolutionAngerTimer; }								// Exposed to Python
	void changeDefyResolutionAngerTimer(int iChange);															// Exposed to Python
	int flatDefyResolutionAngerLength() const;																	// Exposed to Python
	int getHappinessTimer() const { return m_iHappinessTimer; }													// Exposed to Python
	void changeHappinessTimer(int iChange);																		// Exposed to Python
	int getTempHappiness() const; // doc
	int getNoUnhappinessCount() const { return m_iNoUnhappinessCount; }
	bool isNoUnhappiness() const { return (getNoUnhappinessCount() > 0); }										// Exposed to Python
	void changeNoUnhappinessCount(int iChange);
	/*int getNoUnhealthyPopulationCount() const;
	bool isNoUnhealthyPopulation() const;																		// Exposed to Python
	void changeNoUnhealthyPopulationCount(int iChange);*/ // BtS
	/*  K-Mod, 27/dec/10, karadoc
		replace NoUnhealthyPopulation with UnhealthyPopulationModifier */
	int getUnhealthyPopulationModifier() const; // Exposed to Python
	void changeUnhealthyPopulationModifier(int iChange);
	// K-Mod end

	int getBuildingOnlyHealthyCount() const { return m_iBuildingOnlyHealthyCount; }
	bool isBuildingOnlyHealthy() const;																			// Exposed to Python
	void changeBuildingOnlyHealthyCount(int iChange);

	int getImprovementHealth() const; // doc
	int getImprovementHealthPercent() const; // doc
	void setImprovementHealthPercent(int iNewValue); // doc
	void changeImprovementHealthPercent(int iChange); // doc

	int getFood() const { return m_iFood; }																		// Exposed to Python
	void setFood(int iNewValue);																				// Exposed to Python
	void changeFood(int iChange);																				// Exposed to Python
	int getFoodKept() const { return m_iFoodKept; }																// Exposed to Python
	void setFoodKept(int iNewValue);
	void changeFoodKept(int iChange);
	int getMaxFoodKeptPercent() const;																			// Exposed to Python
	void changeMaxFoodKeptPercent(int iChange);

	int getOverflowProduction() const { return m_iOverflowProduction; }											// Exposed to Python
	void setOverflowProduction(int iNewValue);																	// Exposed to Python
	void changeOverflowProduction(int iChange, int iProductionModifier);
	// advc.064b:
	int unmodifyOverflow(int iRawOverflow, int iProductionModifier) const;

	int getFeatureProduction() const { return m_iFeatureProduction; }											// Exposed to Python
	void setFeatureProduction(int iNewValue);																	// Exposed to Python
	void changeFeatureProduction(int iChange);

	int getMilitaryProductionModifier() const { return m_iMilitaryProductionModifier; }							// Exposed to Python
	void changeMilitaryProductionModifier(int iChange);
	int getSpaceProductionModifier() const { return m_iSpaceProductionModifier; }								// Exposed to Python
	void changeSpaceProductionModifier(int iChange);

	int getExtraTradeRoutes() const { return m_iExtraTradeRoutes; }												// Exposed to Python
	void changeExtraTradeRoutes(int iChange);																	// Exposed to Python
	int getTradeRouteModifier() const { return m_iTradeRouteModifier; }											// Exposed to Python
	void changeTradeRouteModifier(int iChange);
	int getForeignTradeRouteModifier() const { return m_iForeignTradeRouteModifier; }							// Exposed to Python
	void changeForeignTradeRouteModifier(int iChange);

	// K-Mod, 26/sep/10 (Trade culture calculation)
	int getTradeCultureRateTimes100() const;																	// Exposed to Python

	int getBuildingDefense() const { return m_iBuildingDefense; }												// Exposed to Python
	void changeBuildingDefense(int iChange);
	// BUG - Building Additional Defense:
	int getAdditionalDefenseByBuilding(BuildingTypes eBuilding) const;

	int getBuildingBombardDefense() const { return m_iBuildingBombardDefense; }									// Exposed to Python
	void changeBuildingBombardDefense(int iChange);

	int getFreeExperience() const { return m_iFreeExperience; }													// Exposed to Python
	void changeFreeExperience(int iChange);

	int getCurrAirlift() const { return m_iCurrAirlift; }														// Exposed to Python
	void setCurrAirlift(int iNewValue);
	void changeCurrAirlift(int iChange);
	int getMaxAirlift() const { return m_iMaxAirlift; }															// Exposed to Python
	void changeMaxAirlift(int iChange);

	int getAirModifier() const { return m_iAirModifier; }														// Exposed to Python
	void changeAirModifier(int iChange);

	int getAirUnitCapacity(TeamTypes eTeam) const;																// Exposed to Python
	void changeAirUnitCapacity(int iChange);																	// Exposed to Python

	int getNukeModifier() const { return m_iNukeModifier; }														// Exposed to Python
	void changeNukeModifier(int iChange);

	int getFreeSpecialist() const;																				// Exposed to Python
	void changeFreeSpecialist(int iChange);

	int getPowerCount() const { return m_iPowerCount; }
	bool isPower() const { return (getPowerCount() > 0 || isAreaCleanPower()); }								// Exposed to Python
	bool isAreaCleanPower() const;																				// Exposed to Python
	int getDirtyPowerCount() const { return m_iDirtyPowerCount; }
	bool isDirtyPower() const;																					// Exposed to Python
	void changePowerCount(int iChange, bool bDirty);

	int getPowerConsumedCount() const;
	void changePowerConsumedCount(int iChange);

	bool isAreaBorderObstacle() const;																			// Exposed to Python

	int getDefenseDamage() const { return m_iDefenseDamage; }													// Exposed to Python
	void changeDefenseDamage(int iChange);																		// Exposed to Python
	void changeDefenseModifier(int iChange);																	// Exposed to Python
	int getLastDefenseDamage() const;																			// Exposed to Python
	void setLastDefenseDamage(int iNewValue);

	bool isBombardable(const CvUnit* pUnit) const;																// Exposed to Python
	int getNaturalDefense() const;																				// Exposed to Python
	int getTotalDefense(bool bIgnoreBuilding) const;															// Exposed to Python
	int getDefenseModifier(bool bIgnoreBuilding) const;															// Exposed to Python

	int getOccupationTimer() const { return m_iOccupationTimer; }												// Exposed to Python
	bool isOccupation() const { return (getOccupationTimer() > 0); }											// Exposed to Python
	void setOccupationTimer(int iNewValue, bool bEffects = true);												// Exposed to Python
	void changeOccupationTimer(int iChange, bool bEffects = true);												// Exposed to Python

	int getCultureUpdateTimer() const { return m_iCultureUpdateTimer; }											// Exposed to Python
	void setCultureUpdateTimer(int iNewValue);
	void changeCultureUpdateTimer(int iChange);																	// Exposed to Python

	int getCitySizeBoost() const;
	void setCitySizeBoost(int iBoost);

	bool isNeverLost() const;																					// Exposed to Python
	void setNeverLost(bool bNewValue);																			// Exposed to Python

	bool isBombarded() const { return m_bBombarded; }															// Exposed to Python
	void setBombarded(bool bNewValue);																			// Exposed to Python

	bool isDrafted() const { return m_bDrafted; }																// Exposed to Python
	void setDrafted(bool bNewValue);																			// Exposed to Python

	bool isAirliftTargeted() const { return m_bAirliftTargeted; }												// Exposed to Python
	void setAirliftTargeted(bool bNewValue);																	// Exposed to Python

	bool isPlundered() const { return m_bPlundered; }															// Exposed to Python
	void setPlundered(bool bNewValue);																			// Exposed to Python

	bool isWeLoveTheKingDay() const;																			// Exposed to Python
	void setWeLoveTheKingDay(bool bNewValue);

	bool isCitizensAutomated() const { return m_bCitizensAutomated; }											// Exposed to Python
	void setCitizensAutomated(bool bNewValue);																	// Exposed to Python
	bool isProductionAutomated() const { return m_bProductionAutomated; }										// Exposed to Python
	void setProductionAutomated(bool bNewValue, bool bClear);													// Exposed to Python

	DllExport bool isWallOverride() const;
	void setWallOverride(bool bOverride);

	DllExport bool isInfoDirty() const;
	DllExport void setInfoDirty(bool bNewValue);
	DllExport bool isLayoutDirty() const;
	DllExport void setLayoutDirty(bool bNewValue);

	DllExport PlayerTypes getOwner() const { return m_eOwner; } // advc.inl: was "getOwnerINLINE"				// Exposed to Python
	DllExport TeamTypes getTeam() const;																		// Exposed to Python
	// <advc>
	bool isActiveOwned() const { return (GC.getInitCore().getActivePlayer() == getOwner()); }
	bool isActiveTeam() const { return (GC.getInitCore().getActiveTeam() == getTeam()); } // </advc>
	CivilizationTypes getPreviousCiv() const; // doc
	void setPreviousCiv(CivilizationTypes eNewValue); // doc
	bool isPreviousOwner(PlayerTypes ePlayer) const; // doc
	CivilizationTypes getOriginalCiv() const; // doc
	void setOriginalCiv(CivilizationTypes eNewValue); // doc
	bool isOriginalOwner(PlayerTypes ePlayer) const; // doc

	int getSettlerValue() const; // doc
	int getSettlerValue(PlayerTypes ePlayer) const; // doc
	int getSettlerValue(CivilizationTypes eCivilization) const; // doc
	int getWarValue() const; // doc
	int getWarValue(PlayerTypes ePlayer) const; // doc
	int getWarValue(CivilizationTypes eCivilization) const; // doc

	bool isBirthProtected() const; // doc
	PlayerTypes getBirthProtected() const; // doc
	bool isExpansionEffect(PlayerTypes ePlayer) const; // doc
	PlayerTypes getExpansion() const; // doc

	CultureLevelTypes getCultureLevel() const { return m_eCultureLevel; }										// Exposed to Python
	CultureLevelTypes getCultureLevel(PlayerTypes ePlayer) const; // advc
	int getCultureThreshold() const;																			// Exposed to Python
	static int getCultureThreshold(CultureLevelTypes eLevel);
	void setCultureLevel(CultureLevelTypes eNewValue, bool bUpdatePlotGroups);
	void updateCultureLevel(bool bUpdatePlotGroups);
	CultureLevelTypes calculateCultureLevel(PlayerTypes ePlayer) const; // advc
	int getNumPartisanUnits(PlayerTypes ePartisanPlayer) const; // advc.003y
	int getCultureTurnsLeft() const; // advc.042
	void initTraitCulture(); // advc.908b

	int getSeaPlotYield(YieldTypes eYield) const { return m_aiSeaPlotYield.get(eYield); }						// Exposed to Python
	void changeSeaPlotYield(YieldTypes eYield, int iChange);
	int getRiverPlotYield(YieldTypes eYield) const { return m_aiRiverPlotYield.get(eYield); }					// Exposed to Python
	void changeRiverPlotYield(YieldTypes eYield, int iChange);
	int getFlatRiverPlotYield(YieldTypes eYield) const; // doc
	void changeFlatRiverPlotYield(YieldTypes eYield, int iChange); // doc
	int getBonusYield(BonusTypes eBonus, YieldTypes eYield) const { return m_aeiiBonusYieldChange.get(eBonus, eYield); }; // doc
	void changeBonusYield(BonusTypes eBonus, YieldTypes eYield, int iChange); // doc

	// BUG - Building Additional Yield - start
	int getAdditionalYieldByBuilding(YieldTypes eYield, BuildingTypes eBuilding) const;
	int getAdditionalBaseYieldRateByBuilding(YieldTypes eYield, BuildingTypes eBuilding) const;
	int getAdditionalYieldRateModifierByBuilding(YieldTypes eYield, BuildingTypes eBuilding) const;
	// BUG - Building Additional Yield - end
	// BUG - Specialist Additional Yield - start
	int getAdditionalYieldBySpecialist(YieldTypes eYield, SpecialistTypes eSpecialist, int iChange = 1) const;
	int getAdditionalBaseYieldRateBySpecialist(YieldTypes eYield, SpecialistTypes eSpecialist, int iChange = 1) const;
	// BUG - Specialist Additional Yield - end

	int getBaseYieldRate(YieldTypes eYield) const { return m_aiBaseYieldRate.get(eYield); }						// Exposed to Python
	int getBaseYieldRateModifier(YieldTypes eYield, int iExtra = 0) const;										// Exposed to Python
	int getYieldRate(YieldTypes eYield) const;																	// Exposed to Python
	void setBaseYieldRate(YieldTypes eYield, int iNewValue);													// Exposed to Python
	void changeBaseYieldRate(YieldTypes eYield, int iChange);													// Exposed to Python
	int calculateBaseYieldRate(YieldTypes eYield); // advc.104u
	int getYieldRateModifier(YieldTypes eYield) const { return m_aiYieldRateModifier.get(eYield); }				// Exposed to Python
	void changeYieldRateModifier(YieldTypes eYield, int iChange);

	int getPowerYieldRateModifier(YieldTypes eYield) const														// Exposed to Python
	{
		return m_aiPowerYieldRateModifier.get(eYield);
	}
	void changePowerYieldRateModifier(YieldTypes eYield, int iChange);
	int getBonusYieldRateModifier(YieldTypes eYield) const														// Exposed to Python
	{
		return m_aiBonusYieldRateModifier.get(eYield);
	}
	void changeBonusYieldRateModifier(YieldTypes eYield, int iChange);
	int getBonusCommerceRateModifier(CommerceTypes eIndex) const; // doc
	void changeBonusCommerceRateModifier(CommerceTypes eIndex, int iChange); // doc
	int getTradeYield(YieldTypes eYield) const { return m_aiTradeYield.get(eYield); }							// Exposed to Python
	int totalTradeModifier(CvCity const* pOtherCity = NULL) const;												// Exposed to Python
	int getPopulationTradeModifier() const;
	int getPeaceTradeModifier(TeamTypes eTeam) const;
	int getBaseTradeProfit(CvCity const* pCity) const;
	int calculateTradeProfit(CvCity const* pCity) const															// Exposed to Python
	{
		return calculateTradeProfitTimes100(pCity) / 100;
	}
	int calculateTradeProfitTimes100(CvCity const* pCity) const; // advc.004
	int calculateTradeYield(YieldTypes eYield, int iTradeProfit) const;											// Exposed to Python
	// BULL - Trade Hover - start
	void calculateTradeTotals(YieldTypes eYield, int& iDomesticYield, int& iDomesticRoutes,
			int& iForeignYield, int& iForeignRoutes, PlayerTypes eWithPlayer = NO_PLAYER) const;
	// BULL - Trade Hover - end
	void setTradeYield(YieldTypes eYield, int iNewValue);

	int getExtraSpecialistYield(YieldTypes eYield) const;														// Exposed to Python
	int getExtraSpecialistYield(YieldTypes eYield, SpecialistTypes eSpecialist) const;							// Exposed to Python
	void updateExtraSpecialistYield(YieldTypes eYield);
	void updateExtraSpecialistYield();

	int getCommerceRate(CommerceTypes eCommerce) const;															// Exposed to Python
	int getCommerceRateTimes100(CommerceTypes eCommerce) const;													// Exposed to Python
	int getCommerceFromPercent(CommerceTypes eCommerce, int iYieldRate) const;									// Exposed to Python
	int getBaseCommerceRate(CommerceTypes eCommerce) const														// Exposed to Python
	{
		return (getBaseCommerceRateTimes100(eCommerce) / 100);
	}
	int getBaseCommerceRateTimes100(CommerceTypes eCommerce) const;												// Exposed to Python
	int getTotalCommerceRateModifier(CommerceTypes eCommerce) const;											// Exposed to Python
	void updateCommerce(CommerceTypes eCommerce);
	void updateCommerce();

	int getModifiedCultureRateTimes100() const; // doc
	int getModifiedCultureRate() const; // doc

	int getProductionToCommerceModifier(CommerceTypes eCommerce) const											// Exposed to Python
	{
		return m_aiProductionToCommerceModifier.get(eCommerce);
	}
	void changeProductionToCommerceModifier(CommerceTypes eCommerce, int iChange);

	int getBuildingCommerce(CommerceTypes eCommerce) const { return m_aiBuildingCommerce.get(eCommerce); }		// Exposed to Python
	int getBuildingCommerceByBuilding(CommerceTypes eCommerce, BuildingTypes eBuilding) const;					// Exposed to Python
	void updateBuildingCommerce();
	void updateBuildingCommerce(CommerceTypes eCommerce); // advc.opt
	// BUG - Building Additional Commerce - start (advc: unused getAdditionalCommerceByBuilding removed)
	int getAdditionalCommerceTimes100ByBuilding(CommerceTypes eCommerce, BuildingTypes eBuilding) const;
	int getAdditionalBaseCommerceRateByBuilding(CommerceTypes eCommerce, BuildingTypes eBuilding) const;
	int getAdditionalBaseCommerceRateByBuildingImpl(CommerceTypes eCommerce, BuildingTypes eBuilding) const;
	int getAdditionalCommerceRateModifierByBuilding(CommerceTypes eCommerce, BuildingTypes eBuilding) const;
	int getAdditionalCommerceRateModifierByBuildingImpl(CommerceTypes eCommerce, BuildingTypes eBuilding) const;
	// BUG - Building Additional Commerce - end
	int getSpecialistCommerce(CommerceTypes eCommerce) const													// Exposed to Python
	{
		return m_aiSpecialistCommerce.get(eCommerce);
	}
	void changeSpecialistCommerce(CommerceTypes eCommerce, int iChange);										// Exposed to Python
	// BUG - Specialist Additional Commerce - start
	int getAdditionalCommerceBySpecialist(CommerceTypes eCommerce,												// Exposed to Python
		SpecialistTypes eSpecialist, int iChange = 1) const
	{
		return getAdditionalCommerceTimes100BySpecialist(eCommerce, eSpecialist, iChange) / 100;
	}
	int getAdditionalCommerceTimes100BySpecialist(CommerceTypes eCommerce,										// Exposed to Python
			SpecialistTypes eSpecialist, int iChange = 1) const;
	int getAdditionalBaseCommerceRateBySpecialist(CommerceTypes eCommerce,										// Exposed to Python
			SpecialistTypes eSpecialist, int iChange = 1) const;
	int getAdditionalBaseCommerceRateBySpecialistImpl(CommerceTypes eCommerce,
			SpecialistTypes eSpecialist, int iChange = 1) const;
	// BUG - Specialist Additional Commerce - end

	int getReligionCommerce(CommerceTypes eCommerce) const														// Exposed to Python
	{
		return m_aiReligionCommerce.get(eCommerce);
	}
	int getReligionCommerceByReligion(CommerceTypes eCommerce,													// Exposed to Python
			ReligionTypes eReligion, bool bForce = false) const; //advc
	void updateReligionCommerce(CommerceTypes eCommerce);
	void updateReligionCommerce();

	void setCorporationYield(YieldTypes eYield, int iNewValue);
	int getCorporationCommerce(CommerceTypes eCommerce) const													// Exposed to Python
	{
		return m_aiCorporationCommerce.get(eCommerce);
	}
	int getCorporationCommerceByCorporation(CommerceTypes eCommerce, CorporationTypes eCorporation) const;		// Exposed to Python
	int getCorporationYield(YieldTypes eYield) const { return m_aiCorporationYield.get(eYield); }				// Exposed to Python
	int getCorporationYieldByCorporation(YieldTypes eYield, CorporationTypes eCorporation) const;				// Exposed to Python
	int getCorporationGoodHappiness() const; // doc
	int getCorporationBadHappiness() const; // doc
	int getCorporationHappinessByCorporation(CorporationTypes eCorporation) const; // doc
	int getCorporationHealth() const; // doc
	int getCorporationUnhealth() const; // doc
	int getCorporationHealthByCorporation(CorporationTypes eCorporation) const; // doc
	void updateCorporation(/* advc.064d: */ bool bVerifyProduction = true);
	void updateCorporationCommerce(CommerceTypes eCommerce);
	void updateCorporationYield(YieldTypes eYield);
	void updateCorporationBonus(/* advc.064d: */ bool bVerifyProduction = true);
	void updateCorporationHappiness(); // doc
	void updateCorporationHealth(); // doc

	int getCommerceRateModifier(CommerceTypes eCommerce) const													// Exposed to Python
	{
		return m_aiCommerceRateModifier.get(eCommerce);
	}
	void changeCommerceRateModifier(CommerceTypes eCommerce, int iChange);

	int getPowerCommerceRateModifier(CommerceTypes eIndex) const; // doc
	void changePowerCommerceRateModifier(CommerceTypes eIndex, int iChange); // doc
	int getCultureCommerceRateModifier(CommerceTypes eIndex) const; // doc
	void changeCultureCommerceRateModifier(CommerceTypes eIndex, int iChange); // doc

	int getCommerceHappinessPer(CommerceTypes eCommerce) const													// Exposed to Python
	{
		return m_aiCommerceHappinessPer.get(eCommerce);
	}
	int getCommerceHappinessByType(CommerceTypes eCommerce) const;												// Exposed to Python
	int getCommerceHappiness() const;																			// Exposed to Python
	void changeCommerceHappinessPer(CommerceTypes eCommerce, int iChange);

	int getDomainFreeExperience(DomainTypes eDomain) const														// Exposed to Python
	{
		return m_aiDomainFreeExperience.get(eDomain);
	}
	void changeDomainFreeExperience(DomainTypes eDomain, int iChange);

	int getDomainProductionModifier(DomainTypes eDomain) const													// Exposed to Python
	{
		return m_aiDomainProductionModifier.get(eDomain);
	}
	void changeDomainProductionModifier(DomainTypes eDomain, int iChange);

	int getCulture(CivilizationTypes eCivilization) const; // doc
	int getCulture(PlayerTypes ePlayer) const;																	// Exposed to Python
	int getCultureTimes100(CivilizationTypes eCivilization) const; // doc
	int getCultureTimes100(PlayerTypes ePlayer) const;															// Exposed to Python
	int countTotalCultureTimes100() const;																		// Exposed to Python
	int getActualTotalCultureTimes100() const; // doc
	PlayerTypes findHighestCulture(bool bIgnoreMinors = false) const;																		// Exposed to Python
	// advc.101:  (advc.ctr: exposed to Python)
	scaled revoltProbability( // <advc.023>
			bool bIgnoreWar = false, bool biIgnoreGarrison = false,
			bool bIgnoreOccupation = false) const;
	scaled probabilityOccupationDecrement() const; // </advc.023>
	// K-Mod: (advc.ctr: exposed to Python)
	bool canCultureFlip(PlayerTypes eToPlayer /* <advc.101> */ = NO_PLAYER,
			bool bCheckPriorRevolts = true) const; // </advc.101>
	bool isMartialLaw(PlayerTypes eRevoltPlayer) const; // advc.023
	int calculateCulturePercent(CivilizationTypes eCivilization) const; // doc
	int calculateCulturePercent(PlayerTypes ePlayer) const;														// Exposed to Python
	int calculateOverallCulturePercent(CivilizationTypes eCivilization) const; // doc
	int calculateOverallCulturePercent(PlayerTypes eIndex) const; // doc
	int calculateTeamCulturePercent(TeamTypes eTeam) const;														// Exposed to Python
	void setCulture(CivilizationTypes eCivilization, int iNewValue); // doc
	void setCulture(PlayerTypes ePlayer, int iNewValue, bool bPlots, bool bUpdatePlotGroups);					// Exposed to Python
	void setCultureTimes100(CivilizationTypes eCivilization, int iNewValue); // doc
	void setCultureTimes100(PlayerTypes ePlayer, int iNewValue, bool bPlots, bool bUpdatePlotGroups);			// Exposed to Python
	void changeCulture(CivilizationTypes eCivilization, int iChange); // doc
	void changeCulture(PlayerTypes ePlayer, int iChange, bool bPlots, bool bUpdatePlotGroups);					// Exposed to Python
	void changeCultureTimes100(CivilizationTypes eCivilization, int iChange); // doc
	void changeCultureTimes100(PlayerTypes ePlayer, int iChange, bool bPlots, bool bUpdatePlotGroups);			// Exposed to Python

	int getActualCultureTimes100(CivilizationTypes eCivilization) const; // doc
	int getActualCultureTimes100(PlayerTypes ePlayer) const; // doc
	int getActualCulture(CivilizationTypes eCivilization) const; // doc
	int getActualCulture(PlayerTypes ePlayer) const; // doc

	int getNumRevolts(PlayerTypes ePlayer) const
	{
		return m_aiNumRevolts.get(ePlayer);
	}
	int getNumRevolts() const; // advc.099c
	void changeNumRevolts(PlayerTypes ePlayer, int iChange);
	scaled getRevoltTestProbability() const; // advc.101: between 0 and 1
	int getRevoltProtection() const; // advc.101
	void addRevoltFreeUnits(); // advc

	bool isTradeRoute(PlayerTypes ePlayer) const																// Exposed to Python
	{
		return m_abTradeRoute.get(ePlayer);
	}
	void setTradeRoute(PlayerTypes ePlayer, bool bNewValue);

	bool isEverOwned(CivilizationTypes eCivilization) const; // doc
	bool isEverOwned(PlayerTypes ePlayer) const;																// Exposed to Python
	void setEverOwned(CivilizationTypes eCivilization, bool bNewValue); // doc
	void setEverOwned(PlayerTypes ePlayer, bool bNewValue);

	DllExport bool isRevealed(TeamTypes eTeam, bool bDebug) const;												// Exposed to Python
	// advc.inl: Faster implementation for non-UI code
	bool isRevealed(TeamTypes eToTeam) const
	{
		return m_abRevealed.get(eToTeam);
	}
	void setRevealed(TeamTypes eTeam, bool bNewValue);															// Exposed to Python

	bool getEspionageVisibility(TeamTypes eTeam) const															// Exposed to Python
	{
		return m_abEspionageVisibility.get(eTeam);
	}
	bool isAnyEspionageVisibility() const
	{	// advc.opt:
		return m_abEspionageVisibility.isAnyNonDefault();
	}
	void setEspionageVisibility(TeamTypes eTeam, bool bVisible, bool bUpdatePlotGroups);
	void updateEspionageVisibility(bool bUpdatePlotGroups);

	DllExport const CvWString getName(uint uiForm = 0) const;													// Exposed to Python
	DllExport const wchar* getNameKey() const;																	// Exposed to Python
	void setName(const wchar* szNewValue, bool bFound = false,													// Exposed to Python
			bool bInitial = false); // advc.106k
	void doFoundMessage();
	void doFoundReplayMessage(); // rfc

	// Script data needs to be a narrow string for pickling in Python
	std::string getScriptData() const;																			// Exposed to Python
	void setScriptData(std::string szNewValue);																	// Exposed to Python

	int getFreeBonus(BonusTypes eBonus) const																	// Exposed to Python
	{
		return m_aiFreeBonus.get(eBonus);
	}  // <advc.opt>
	bool isAnyFreeBonus() const
	{
		return m_aiFreeBonus.isAnyNonDefault();
	} // </advc.opt>
	void changeFreeBonus(BonusTypes eBonus, int iChange);														// Exposed to Python
	int getNumBonuses(BonusTypes eBonus) const;																	// Exposed to Python
	bool hasBonus(BonusTypes eBonus) const																		// Exposed to Python
	{
		return (getNumBonuses(eBonus) > 0);
	}
	void changeNumBonuses(BonusTypes eBonus, int iChange,
			bool bVerifyProduction = true); // advc.064d
	int countUniqueBonuses() const; // advc.149
	int getNumCorpProducedBonuses(BonusTypes eBonus) const
	{
		return m_aiNumCorpProducedBonuses.get(eBonus);
	}
	bool isCorporationBonus(BonusTypes eBonus) const;
	bool isActiveCorporation(CorporationTypes eCorporation) const;

	int getBuildingProduction(BuildingTypes eBuilding) const													// Exposed to Python
	{
		return m_aiBuildingProduction.get(eBuilding);
	}
	void setBuildingProduction(BuildingTypes eBuilding, int iNewValue);											// Exposed to Python
	void changeBuildingProduction(BuildingTypes eBuilding, int iChange);										// Exposed to Python

	int getBuildingProductionTime(BuildingTypes eBuilding) const												// Exposed to Python
	{
		return m_aiBuildingProductionTime.get(eBuilding);
	}
	void setBuildingProductionTime(BuildingTypes eBuilding, int iNewValue);										// Exposed to Python
	void changeBuildingProductionTime(BuildingTypes eBuilding, int iChange);									// Exposed to Python

	int getProjectProduction(ProjectTypes eProject) const														// Exposed to Python
	{
		return m_aiProjectProduction.get(eProject);
	}
	void setProjectProduction(ProjectTypes eProject, int iNewValue);
	void changeProjectProduction(ProjectTypes eProject, int iChange);

	CivilizationTypes getBuildingOriginalOwner(BuildingTypes eBuilding) const											// Exposed to Python
	{
		return m_aeBuildingOriginalOwner.get(eBuilding);
	}
	int getBuildingOriginalTime(BuildingTypes eBuilding) const													// Exposed to Python
	{
		return m_aiBuildingOriginalTime.get(eBuilding);
	}

	void setBuildingOriginalOwner(BuildingTypes eBuilding, CivilizationTypes eCivilization); // doc
	void setBuildingOriginalTime(BuildingTypes eBuilding, int iYear); // doc

	int getUnitProduction(UnitTypes eUnit) const																// Exposed to Python
	{
		return m_aiUnitProduction.get(eUnit);
	}
	void setUnitProduction(UnitTypes eUnit, int iNewValue);														// Exposed to Python
	void changeUnitProduction(UnitTypes eUnit, int iChange);													// Exposed to Python

	HurryTypes getUnitHurry(UnitClassTypes eUnitClass) const; // doc
	void setUnitHurry(UnitClassTypes eUnitClass, HurryTypes eHurry); // doc

	int getUnitProductionTime(UnitTypes eUnit) const								// Exposed to Python (for BULL - Production Decay)
	{
		return m_aiUnitProductionTime.get(eUnit);
	}
	void setUnitProductionTime(UnitTypes eUnit, int iNewValue);
	void changeUnitProductionTime(UnitTypes eUnit, int iChange);
	/*	BULL - Production Decay - start (advc.094 -
		NB: defined through IMPLEMENT_BUG_PRODUCTION_DECAY_GETTERS macro) */
	bool isBuildingProductionDecay(BuildingTypes eBuilding) const;												// Exposed to Python
	int getBuildingProductionDecay(BuildingTypes eBuilding) const;												// Exposed to Python
	int getBuildingProductionDecayTurns(BuildingTypes eBuilding) const;											// Exposed to Python
	bool isUnitProductionDecay(UnitTypes eUnit) const;															// Exposed to Python
	int getUnitProductionDecay(UnitTypes eUnit) const;															// Exposed to Python
	int getUnitProductionDecayTurns(UnitTypes eUnit) const;														// Exposed to Python
	// BULL - Production Decay - end
	bool isAnyProductionProgress(OrderTypes eOrder) const; // advc.opt

	int getGreatPeopleUnitRate(UnitTypes eUnit) const															// Exposed to Python
	{
		return m_aiGreatPeopleUnitRate.get(eUnit);
	}
	void setGreatPeopleUnitRate(UnitTypes eUnit, int iNewValue);
	void changeGreatPeopleUnitRate(UnitTypes eUnit, int iChange);

	int getGreatPeopleUnitProgress(UnitTypes eUnit) const														// Exposed to Python
	{
		return m_aiGreatPeopleUnitProgress.get(eUnit);
	}
	void setGreatPeopleUnitProgress(UnitTypes eUnit, int iNewValue);											// Exposed to Python
	void changeGreatPeopleUnitProgress(UnitTypes eUnit, int iChange);											// Exposed to Python

	int getSpecialistCount(SpecialistTypes eSpecialist) const													// Exposed to Python
	{
		return m_aiSpecialistCount.get(eSpecialist);
	}
	void setSpecialistCount(SpecialistTypes eSpecialist, int iNewValue);
	void changeSpecialistCount(SpecialistTypes eSpecialist, int iChange);
	void alterSpecialistCount(SpecialistTypes eSpecialist, int iChange);										// Exposed to Python

	int getMaxSpecialistCount(SpecialistTypes eSpecialist, bool bIgnoreCivic = false) const;					// Exposed to Python
	bool isSpecialistValid(SpecialistTypes eSpecialist, int iExtra = 0) const;									// Exposed to Python
	void changeMaxSpecialistCount(SpecialistTypes eSpecialist, int iChange);

	int getForceSpecialistCount(SpecialistTypes eSpecialist) const												// Exposed to Python
	{
		return m_aiForceSpecialistCount.get(eSpecialist);
	}
	bool isSpecialistForced() const																				// Exposed to Python
	{
		return m_aiForceSpecialistCount.isAnyNonDefault(); // advc.opt
	}
	void setForceSpecialistCount(SpecialistTypes eSpecialist, int iNewValue);									// Exposed to Python
	void changeForceSpecialistCount(SpecialistTypes eSpecialist, int iChange);									// Exposed to Python

	int getFreeSpecialistCount(SpecialistTypes eSpecialist) const												// Exposed to Python
	{
		return m_aiFreeSpecialistCount.get(eSpecialist);
	}
	void setFreeSpecialistCount(SpecialistTypes eSpecialist, int iNewValue);									// Exposed to Python
	void changeFreeSpecialistCount(SpecialistTypes eSpecialist, int iChange);									// Exposed to Python
	int getAddedFreeSpecialistCount(SpecialistTypes eSpecialist) const;											// Exposed to Python

	int getImprovementFreeSpecialists(ImprovementTypes eImprov) const											// Exposed to Python
	{
		return m_aiImprovementFreeSpecialists.get(eImprov);
	}
	bool isAnyImprovementFreeSpecialist() const
	{	// advc.opt:
		return m_aiImprovementFreeSpecialists.isAnyNonDefault();
	}
	void changeImprovementFreeSpecialists(ImprovementTypes eImprov, int iChange);								// Exposed to Python

	int getReligionInfluence(ReligionTypes eReligion) const														// Exposed to Python
	{
		return m_aiReligionInfluence.get(eReligion);
	}
	void setReligionInfluence(ReligionTypes eIndex, int iNewValue); // doc
	void changeReligionInfluence(ReligionTypes eReligion, int iChange);											// Exposed to Python
	void spreadReligionInfluence(ReligionTypes eReligion, int iRange, int iChange); // doc

	int getCurrentStateReligionHappiness() const;																// Exposed to Python
	int getStateReligionHappiness(ReligionTypes eReligion) const												// Exposed to Python
	{
		return m_aiStateReligionHappiness.get(eReligion);
	}
	void changeStateReligionHappiness(ReligionTypes eReligion, int iChange);									// Exposed to Python

	int getUnitCombatFreeExperience(UnitCombatTypes eUnitCombat) const											// Exposed to Python
	{
		return m_aiUnitCombatFreeExperience.get(eUnitCombat);
	}
	void changeUnitCombatFreeExperience(UnitCombatTypes eUnitCombat, int iChange);

	int getFreePromotionCount(PromotionTypes ePromo) const														// Exposed to Python
	{
		return m_aiFreePromotionCount.get(ePromo);
	}
	bool isFreePromotion(PromotionTypes ePromo) const															// Exposed to Python
	{
		return (getFreePromotionCount(ePromo) > 0);
	}
	bool isAnyFreePromotion() const
	{	// advc.opt:
		return m_aiFreePromotionCount.isAnyNonDefault();
	}
	void changeFreePromotionCount(PromotionTypes ePromo, int iChange);

	int getSpecialistFreeExperience() const																		// Exposed to Python
	{
		return m_iSpecialistFreeExperience;
	}
	void changeSpecialistFreeExperience(int iChange);

	int getEspionageDefenseModifier() const																		// Exposed to Python
	{
		return m_iEspionageDefenseModifier;
	}
	void changeEspionageDefenseModifier(int iChange);
	int cultureTimes100InsertedByMission(EspionageMissionTypes eMission) const; // advc

	bool isWorkingPlot(CityPlotTypes ePlot) const																// Exposed to Python
	{
		return m_abWorkingPlot.get(ePlot);
	}
	bool isWorkingPlot(CvPlot const& kPlot) const;																// Exposed to Python
	void setWorkingPlot(CityPlotTypes ePlot, bool bNewValue);
	void setWorkingPlot(CvPlot& kPlot, bool bNewValue);
	void alterWorkingPlot(CityPlotTypes ePlot);																	// Exposed to Python

	bool isHasRealBuilding(BuildingTypes eIndex) const;	// rfc												// Exposed to Python
	void setHasRealBuilding(BuildingTypes eIndex, bool bNewValue); // rfc	// Exposed to Python
	int getNumRealBuilding(BuildingTypes eBuilding) const														// Exposed to Python
	{
		return m_aiNumRealBuilding.get(eBuilding);
	}
	int getNumRealBuilding(BuildingClassTypes eBuildingClass) const; // advc.003w
	void setNumRealBuilding(BuildingTypes eBuilding, int iNewValue,												// Exposed to Python
			bool bEndOfTurn = false); // advc.001x
	void setNumRealBuildingTimed(BuildingTypes eBuilding, int iNewValue, bool bFirst,
			CivilizationTypes eOriginalOwner, int iOriginalTime, /* advc.001x */ bool bEndOfTurn = false);
	//bool isValidBuildingLocation(BuildingTypes eBuilding) const; // advc: Replaced by CvPlot::canConstruct

	int getNumFreeBuilding(BuildingTypes eBuilding) const														// Exposed to Python
	{
		return m_aiNumFreeBuilding.get(eBuilding);
	}
	void setNumFreeBuilding(BuildingTypes eBuilding, int iNewValue);

	bool isHasBuildingEffect(BuildingTypes eBuilding) const;

	bool isMeltdownBuilding(BuildingTypes eBuilding) const; // advc.652
	bool isMeltdownBuildingSuperseded(BuildingTypes eBuilding) const; // advc.652

	bool isHasReligion(ReligionTypes eReligion) const															// Exposed to Python
	{
		return m_abHasReligion.get(eReligion);
	}
	void setHasReligion(ReligionTypes eReligion, bool bNewValue, bool bAnnounce, bool bArrows = true,
			PlayerTypes eSpreadPlayer = NO_PLAYER); // advc.106e
	int getReligionGrip(ReligionTypes eReligion) const; // K-Mod

	void spreadReligion(ReligionTypes eReligion, bool bMissionary = false); // doc
	void removeReligion(ReligionTypes eReligion); // doc
	void replaceReligion(ReligionTypes eOldReligion, ReligionTypes eNewReligion); // doc

	ReligionTypes disappearingReligion(ReligionTypes eNewReligion = NO_RELIGION, bool bConquest = false) const;

	bool isHasCorporation(CorporationTypes eCorp) const															// Exposed to Python
	{
		return m_abHasCorporation.get(eCorp);
	}
	void setHasCorporation(CorporationTypes eCorp, bool bNewValue,
			bool bAnnounce, bool bArrows = true);

	CvCity* getTradeCity(int iIndex) const;																		// Exposed to Python
	int getTradeRoutes() const;																					// Exposed to Python
	void clearTradeRoutes();
	void updateTradeRoutes();
	bool canHaveTradeRouteWith(const CvCity* pCity) const; // doc

	void clearOrderQueue();																						// Exposed to Python
	//void pushOrder(OrderTypes eOrder, int iData1, int iData2, bool bSave, bool bPop, bool bAppend, bool bForce = false);
	// K-Mod. (the old version is still exposed to Python)
	void pushOrder(OrderTypes eOrder, int iData1, int iData2 = -1, bool bSave = false,
			bool bPop = false, int iPosition = 0, bool bForce = false);
	enum ChooseProductionPlayers { NONE_CHOOSE, HUMAN_CHOOSE, AI_CHOOSE, ALL_CHOOSE }; // advc.064d
	void popOrder(int iNum, bool bFinish = false, ChooseProductionPlayers eChoose = NONE_CHOOSE,				// Exposed to Python
			bool bEndOfTurn = true); // advc.001x
	void startHeadOrder();
	void stopHeadOrder();
	int getOrderQueueLength() /* advc: */ const																	// Exposed to Python
	{
		return m_orderQueue.getLength();
	}
	OrderData* getOrderFromQueue(int iIndex) const;																// Exposed to Python
	CLLNode<OrderData>* nextOrderQueueNode(CLLNode<OrderData>* pNode) const
	{
		return m_orderQueue.next(pNode);
	}  // <advc.003s>
	CLLNode<OrderData> const* nextOrderQueueNode(CLLNode<OrderData> const* pNode) const
	{
		return m_orderQueue.next(pNode);
	} // </advc.003s>
	CLLNode<OrderData>* headOrderQueueNode() const
	{
		return m_orderQueue.head();
	}
	DllExport int getNumOrdersQueued() const
	{
		return m_orderQueue.getLength();
	}
	DllExport OrderData getOrderData(int iIndex) const;

	DllExport void getVisibleBuildings(std::list<BuildingTypes>& kVisible, int& iNumGenerics);
	bool isAllBuildingsVisible(TeamTypes eTeam, bool bDebug) const; // advc.045

	DllExport void getVisibleEffects(ZoomLevelTypes eCurrentZoom, std::vector<const TCHAR*>& kEffectNames);

	// Billboard appearance controls
	DllExport void getCityBillboardSizeIconColors(NiColorA& kDotColor, NiColorA& kTextColor) const;
	DllExport const TCHAR* getCityBillboardProductionIcon() const;
	DllExport bool getFoodBarPercentages(std::vector<float>& afPercentages) const;
	DllExport bool getProductionBarPercentages(std::vector<float>& afPercentages) const;
	DllExport NiColorA getBarBackgroundColor() const;
	DllExport bool isStarCity() const;

	// Exposed to Python
	void setWallOverridePoints(const std::vector< std::pair<float, float> >&
			kPoints); // points are given in world space ... i.e. PlotXToPointX, etc
	DllExport const std::vector< std::pair<float, float> >& getWallOverridePoints() const;

	int getTriggerValue(EventTriggerTypes eTrigger) const;
	bool canApplyEvent(EventTypes eEvent, const EventTriggeredData& kTriggeredData) const;
	void applyEvent(EventTypes eEvent, const EventTriggeredData& kTriggeredData, bool bClear);
	bool isEventOccured(EventTypes eEvent) const;
	void setEventOccured(EventTypes eEvent, bool bOccured);
	void doPartisans(); // advc.003y

	int getBuildingYieldChange(BuildingClassTypes eBuildingClass, YieldTypes eYield) const						// Exposed to Python
	{
		return m_aeiiBuildingYieldChange.get(eBuildingClass, eYield);
	}
	void setBuildingYieldChange(BuildingClassTypes eBuildingClass, YieldTypes eYield, int iChange);				// Exposed to Python
	void changeBuildingYieldChange(BuildingClassTypes eBuildingClass, YieldTypes eYield, int iChange);
	int getBuildingCommerceChange(BuildingClassTypes eBuildingClass, CommerceTypes eCommerce) const				// Exposed to Python
	{
		return m_aeiiBuildingCommerceChange.get(eBuildingClass, eCommerce);
	}
	void setBuildingCommerceChange(BuildingClassTypes eBuildingClass, CommerceTypes eCommerce, int iChange);	// Exposed to Python
	void changeBuildingCommerceChange(BuildingClassTypes eBuildingClass, CommerceTypes eCommerce, int iChange);
	int getBuildingHappyChange(BuildingClassTypes eBuildingClass) const											// Exposed to Python
	{
		return m_aeiBuildingHappyChange.get(eBuildingClass);
	}
	void setBuildingHappyChange(BuildingClassTypes eBuildingClass, int iChange);								// Exposed to Python
	int getBuildingHealthChange(BuildingClassTypes eBuildingClass) const										// Exposed to Python
	{
		return m_aeiBuildingHealthChange.get(eBuildingClass);
	}
	void setBuildingHealthChange(BuildingClassTypes eBuildingClass, int iChange);								// Exposed to Python
	int getBuildingGreatPeopleRateChange(BuildingClassTypes eBuildingClass) const; // doc
	void setBuildingGreatPeopleRateChange(BuildingClassTypes eBuildingClass, int iChange); // doc
	void changeBuildingGreatPeopleRateChange(BuildingClassTypes eBuildingClass, int iChange); // doc

	void setBuildingYieldChange(BuildingTypes eBuilding, YieldTypes eYield, int iChange); // doc
	void setBuildingCommerceChange(BuildingTypes eBuilding, CommerceTypes eCommerce, int iChange); // doc
	void setBuildingGreatPeopleRateChange(BuildingTypes eBuilding, int iChange); // doc
	void changeBuildingYieldChange(BuildingTypes eBuilding, YieldTypes eYield, int iChange); // doc
	void changeBuildingCommerceChange(BuildingTypes eBuilding, CommerceTypes eCommerce, int iChange); // doc
	void changeBuildingGreatPeopleRateChange(BuildingTypes eBuilding, int iChange); // doc

	void updateBuildingYieldChange(BuildingClassTypes eBuildingType, YieldTypes eYield, int iChange); // doc
	void changeReligionYieldChange(ReligionTypes eReligion, YieldTypes eYield, int iChange); // doc

	PlayerTypes getLiberationPlayer(bool bConquest /* advc: */ = false) const;									// Exposed to Python
	void liberate(bool bConquest, /* advc.ctr: */ bool bPeaceDeal = false);										// Exposed to Python
	void meetNewOwner(TeamTypes eOtherTeam, TeamTypes eNewOwner) const; // advc.071

	void changeNoBonusCount(BonusTypes eBonus, int iChange);													// Exposed to Python
	int getNoBonusCount(BonusTypes eBonus) const
	{
		return m_aiNoBonus.get(eBonus);
	}
	bool isNoBonus(BonusTypes eBonus) const																		// Exposed to Python
	{
		return (getNoBonusCount(eBonus) > 0);
	}

	bool isAutoRaze(/* advc: */ PlayerTypes eConqueror = NO_PLAYER) const;

	int getSpecialistGoodHappiness() const; // doc
	int getSpecialistBadHappiness() const; // doc
	void changeSpecialistGoodHappiness(int iChange); // doc
	void changeSpecialistBadHappiness(int iChange); // doc

	bool isMongolUP() const; // doc
	void setMongolUP(bool bNewValue); // doc

	int getGameTurnCivLost(CivilizationTypes eCivilization) { return m_aiGameTurnCivLost.get(eCivilization); } // doc
	void setGameTurnCivLost(CivilizationTypes eCivilization, int iNewValue); // doc
	int getGameTurnPlayerLost(PlayerTypes ePlayer); // doc
	void setGameTurnPlayerLost(PlayerTypes ePlayer, int iNewValue); // doc

	bool isColony() const; // doc
	bool canSlaveJoin() const; // doc

	int calculateCultureCost(CvPlot const& kPlot, bool bOrdering = false) const; // doc
	void updateCultureCosts(); // doc
	void updateCoveredPlots(bool bUpdatePlotGroups); // doc
	int getCulturePlotIndex(CulturePlotTypes eCulturePlot) const; // doc
	CvPlot& getCulturePlot(CulturePlotTypes eCulturePlot) const; // doc
	int getCultureCost(CulturePlotTypes eCulturePlot) const; // doc
	CulturePlotTypes getNextCoveredPlot() const { return m_eNextCoveredPlot; } // doc
	void setNextCoveredPlot(CulturePlotTypes eCulturePlot, bool bUpdatePlotGroups); // doc
	CulturePlotTypes getEffectiveNextCoveredPlot() const; // doc
	bool isCoveredBeforeExpansion(CulturePlotTypes eCulturePlot) const; // doc

	void updateGreatWall(); // doc

	int determineArtStyleType() const; // doc
	void updateArtStyleType(); // doc

	int getDistanceTradeModifier(CvCity const& kOtherCity) const; // doc
	int getDefensivePactTradeModifier(CvCity const& kOtherCity) const; // doc
	int getVassalTradeModifier(CvCity const& kOtherCity) const; // doc

	int estimateGrowth(int iTurns) const; // doc

	bool canSpread(ReligionTypes eReligion, bool bMissionary = false) const; // doc
	int getTurnsToSpread(ReligionTypes eReligion) const; // doc
	bool isHasPrecursor(ReligionTypes eReligion) const; // doc
	bool isHasConflicting(ReligionTypes eReligion) const; // doc
	int getReligionPopulation(ReligionTypes eReligion) const; // doc

	int getCultureRank() const { return m_iCultureRank; } // doc
	void setCultureRank(int iNewValue); // doc

	int getCultureGreatPeopleRateModifier() const { return m_iCultureGreatPeopleRateModifier; } // doc
	void changeCultureGreatPeopleRateModifier(int iChange); // doc

	int getCultureHappiness() const { return m_iCultureHappiness; } // doc
	void changeCultureHappiness(int iChange); // doc

	int getCultureTradeRouteModifier() const { return m_iCultureTradeRouteModifier; } // doc
	void changeCultureTradeRouteModifier(int iChange); // doc

	int getBuildingUnignorableBombardDefense() const { return m_iBuildingUnignorableBombardDefense; } // doc
	void changeBuildingUnignorableBombardDefense(int iChange); // doc
	int getAdditionalUnignorableBombardDefenseByBuilding(BuildingTypes eBuilding) const; // doc

	void triggerMeltdown(BuildingTypes eBuilding); // doc

	bool hasBonusEffect(BonusTypes eBonus) const; // doc
	void processBonusEffect(BonusTypes eBonus, int iChange); // doc

	int getStabilityPopulation() const { return m_iStabilityPopulation; } // doc
	void setStabilityPopulation(int iNewValue); // doc

	int getBuildingUnhealthModifier() const { return m_iBuildingUnhealthModifier;  } // doc
	void setBuildingUnhealthModifier(int iNewValue); // doc
	void changeBuildingUnhealthModifier(int iChange); // doc

	int getCorporationUnhealthModifier() const { return m_iCorporationUnhealthModifier;  } // doc
	void setCorporationUnhealthModifier(int iNewValue); // doc
	void changeCorporationUnhealthModifier(int iChange); // doc

	int countNoGlobalEffectsFreeSpecialists() const; // doc
	int countSatellites() const; // doc
	int getSatelliteSlots() const; // doc
	bool canSatelliteJoin() const; // doc

	int getSpecialistGreatPeopleRateChange(SpecialistTypes eSpecialist) const; // doc

	int getBuildingDamage() const; // doc
	void setBuildingDamage(int iNewValue); // doc
	void changeBuildingDamage(int iChange); // doc

	int getBuildingDamageChange() const; // doc
	void setBuildingDamageChange(int iNewValue); // doc
	void changeBuildingDamageChange(int iChange); // doc

	void applyBuildingDamage(int iDamage); // doc
	void applyPopulationLoss(int iLoss); // doc

	int getTotalPopulationLoss() const; // doc
	void setTotalPopulationLoss(int iNewValue); // doc
	void changeTotalPopulationLoss(int iChange); // doc

	int getPopulationLoss() const; // doc
	void setPopulationLoss(int iNewValue); // doc

	void completeAcquisition(int iCaptureGold, bool bChooseProduction = true); // doc

	int getRebuildProduction() const; // doc

	void sack(PlayerTypes eHighestCulturePlayer, int iCaptureGold); // doc
	void spare(int iCaptureGold); // doc
	void raze(int iCaptureGold); // doc

	void completeRaze(); // doc

	bool canLiberate() const; // doc
	bool isCore(CivilizationTypes eCivilization) const; // doc
	bool isCore(PlayerTypes ePlayer) const; // doc
	bool isCore() const; // doc

	int getSpreadFactor(ReligionTypes eReligion) const; // doc

	bool rebuild(EraTypes eEra = NO_ERA); // doc

	DllExport int getMusicScriptId() const;
	DllExport int getSoundscapeScriptId() const;
	DllExport void cheat(bool bCtrl, bool bAlt, bool bShift);

	DllExport void getBuildQueue(std::vector<std::string>& astrQueue) const;

	void invalidatePopulationRankCache() { m_bPopulationRankValid = false; }
	void invalidateYieldRankCache(YieldTypes eYield = NO_YIELD);
	void invalidateCommerceRankCache(CommerceTypes eCommerce = NO_COMMERCE);
	//int getBestYieldAvailable(YieldTypes eYield) const; // advc.003j: obsolete

	// doc: exposed for CvPlayer::acquireCity
	void doPlotCulture(bool bUpdate, PlayerTypes ePlayer, int iCultureRate, bool bOwned = false);

	// <advc.003u>
	// virtual for FFreeListTrashArray
	virtual void read(FDataStreamBase* pStream);
	virtual void write(FDataStreamBase* pStream);
	CvCityAI& AI()
	{	//return *static_cast<CvCityAI*>(const_cast<CvCity*>(this));
		/*  The above won't work in an inline function b/c the compiler doesn't know
			that CvCityAI is derived from CvCity */
		return *reinterpret_cast<CvCityAI*>(this);
	}
	CvCityAI const& AI() const
	{	//return *static_cast<CvCityAI const*>(this);
		return *reinterpret_cast<CvCityAI const*>(this);
	}
	/*  Keep one pure virtual function to make the class abstract; remove all
		the others - the EXE doesn't call them. */ // </advc.003u>
	virtual void AI_setAssignWorkDirty(bool bNewValue) = 0;

	int calculateBaseYieldRate(YieldTypes eYield) const; // doc
	int calculateBaseGreatPeopleRate() const; // doc

protected:
	// <advc.003u>
	CvCity();
	/*  Subclasses need to call this; not called by base.
		May also want to override it. </advc.003u> */
	virtual void init(int iID, PlayerTypes eOwner, int iX, int iY, bool bBumpUnits, bool bUpdatePlotGroups,
			int iOccupationTimer); // advc.ctr

	// <advc> Moved here for quicker inspection in debugger
	CvWString m_szName;
	PlayerTypes m_eOwner; // </advc>
	int m_iID;
	int m_iX;
	int m_iY;
	PlotNumTypes m_ePlot; // advc.104: Cached b/c frequently accessed by UWAI
	int m_iRallyX;
	int m_iRallyY;
	int m_iGameTurnFounded;
	int m_iGameTurnAcquired;
	int m_iPopulation;
	int m_iHighestPopulation;
	int m_iWorkingPopulation;
	int m_iSpecialistPopulation;
	int m_iNumGreatPeople;
	int m_iBaseGreatPeopleRate;
	int m_iGreatPeopleRateModifier;
	int m_iGreatPeopleProgress;
	int m_iNumWorldWonders;
	int m_iNumTeamWonders;
	int m_iNumNationalWonders;
	int m_iNumBuildings;
	int m_iGovernmentCenterCount;
	int m_iMaintenance;
	int m_iMaintenanceModifier;
	int m_iWarWearinessModifier;
	int m_iHurryAngerModifier;
	int m_iHealRate;
	int m_iEspionageHealthCounter;
	int m_iEspionageHappinessCounter;
	int m_iFreshWaterGoodHealth;
	int m_iFreshWaterBadHealth;
	int m_iSurroundingGoodHealth;
	int m_iSurroundingBadHealth;
	int m_iBuildingGoodHealth;
	int m_iBuildingBadHealth;
	int m_iPowerGoodHealth;
	int m_iPowerBadHealth;
	int m_iBonusGoodHealth;
	int m_iBonusBadHealth;
	int m_iHurryAngerTimer;
	int m_iConscriptAngerTimer;
	int m_iDefyResolutionAngerTimer;
	int m_iHappinessTimer;
	int m_iMilitaryHappinessUnits;
	int m_iBuildingGoodHappiness;
	int m_iBuildingBadHappiness;
	int m_iExtraBuildingGoodHappiness;
	int m_iExtraBuildingBadHappiness;
	int m_iExtraBuildingGoodHealth;
	int m_iExtraBuildingBadHealth;
	int m_iSurroundingGoodHappiness;
	int m_iSurroundingBadHappiness;
	int m_iBonusGoodHappiness;
	int m_iBonusBadHappiness;
	int m_iReligionGoodHappiness;
	int m_iReligionBadHappiness;
	int m_iExtraHappiness;
	int m_iExtraHealth;
	int m_iNoUnhappinessCount;
	int m_iUnhealthyPopulationModifier; // K-Mod
	int m_iBuildingOnlyHealthyCount;
	int m_iFood;
	int m_iFoodKept;
	int m_iMaxFoodKeptPercent;
	int m_iOverflowProduction;
	int m_iFeatureProduction;
	int m_iMilitaryProductionModifier;
	int m_iSpaceProductionModifier;
	int m_iExtraTradeRoutes;
	int m_iTradeRouteModifier;
	int m_iForeignTradeRouteModifier;
	int m_iBuildingDefense;
	int m_iBuildingBombardDefense;
	int m_iFreeExperience;
	int m_iCurrAirlift;
	int m_iMaxAirlift;
	int m_iAirModifier;
	int m_iAirUnitCapacity;
	int m_iNukeModifier;
	int m_iFreeSpecialist;
	int m_iPowerCount;
	int m_iDirtyPowerCount;
	int m_iDefenseDamage;
	int m_iLastDefenseDamage;
	int m_iOccupationTimer;
	int m_iCultureUpdateTimer;
	int m_iCitySizeBoost;
	int m_iSpecialistFreeExperience;
	int m_iEspionageDefenseModifier;
	int m_iPopRushHurryCount; // advc.912d
	int m_iMostRecentOrder; // advc.004x

	int m_iPowerConsumedCount; // doc

	int m_iSpecialistGoodHappiness; // doc
	int m_iSpecialistBadHappiness; // doc

	int m_iCorporationGoodHappiness; // doc
	int m_iCorporationBadHappiness; // doc
	int m_iCorporationHealth; // doc
	int m_iCorporationUnhealth; // doc

	int m_iCultureGreatPeopleRateModifier; // doc
	int m_iCultureHappiness; // doc
	int m_iCultureTradeRouteModifier; // doc

	int m_iBuildingUnignorableBombardDefense; // doc

	int m_iCultureRank; // doc

	int m_iStabilityPopulation; // doc

	int m_iBuildingUnhealthModifier; // doc
	int m_iCorporationUnhealthModifier; // doc

	int m_iTotalCultureTimes100; // doc

	int m_iBuildingDamage; // doc
	int m_iBuildingDamageChange; // doc

	int m_iTotalPopulationLoss; // doc
	int m_iPopulationLoss; // doc

	bool m_bNeverLost;
	bool m_bBombarded;
	bool m_bDrafted;
	bool m_bAirliftTargeted;
	bool m_bWeLoveTheKingDay;
	bool m_bCitizensAutomated;
	bool m_bProductionAutomated;
	bool m_bWallOverride;
	bool m_bInfoDirty;
	bool m_bLayoutDirty;
	bool m_bPlundered;
	bool m_bInvestigate; // advc.103: Refers to the active team
	bool m_bMostRecentUnit; // advc.004x
	bool m_bChooseProductionDirty; // advc.003u: Moved from CvCityAI
	bool m_bMongolUP; // doc

	CivilizationTypes m_ePreviousCiv; // doc
	CivilizationTypes m_eOriginalCiv; // doc
	CultureLevelTypes m_eCultureLevel;
	ArtStyleTypes m_eArtStyle; // doc

	CulturePlotTypes m_eNextCoveredPlot; // doc

	// <advc.enum>
	YieldChangeMap m_aiSeaPlotYield;
	YieldChangeMap m_aiRiverPlotYield;
	YieldChangeMap m_aiFlatRiverPlotYield; // doc
	YieldTotalMap m_aiBaseYieldRate;
	YieldPercentMap m_aiYieldRateModifier;
	YieldPercentMap m_aiPowerYieldRateModifier;
	YieldPercentMap m_aiBonusYieldRateModifier;
	CommercePercentMap m_aiBonusCommerceRateModifier; // doc
	YieldTotalMap m_aiTradeYield;
	YieldTotalMap m_aiCorporationYield;
	YieldTotalMap m_aiExtraSpecialistYield;
	YieldTotalMap m_aiHappinessYield; // doc
	EagerEnumMap<CommerceTypes,int> m_aiCommerceRate; // (at times-100 precision)
	CommercePercentMap m_aiProductionToCommerceModifier;
	CommerceTotalMap m_aiBuildingCommerce;
	CommerceTotalMap m_aiSpecialistCommerce;
	CommerceTotalMap m_aiReligionCommerce;
	CommerceTotalMap m_aiCorporationCommerce;
	CommercePercentMap m_aiCommerceRateModifier;
	CommercePercentMap m_aiPowerCommerceRateModifier; // doc
	CommercePercentMap m_aiCultureCommerceRateModifier; // doc
	CommercePercentMap m_aiCommerceHappinessPer;
	ArrayEnumMap<DomainTypes,int,char> m_aiDomainFreeExperience;
	ArrayEnumMap<DomainTypes,int,short> m_aiDomainProductionModifier;
	EagerEnumMap<CivilizationTypes,int> m_aiCulture;
	ListEnumMap<PlayerTypes,int,short> m_aiNumRevolts;
	ListEnumMap<BonusTypes,int,char> m_aiNoBonus;
	ListEnumMap<BonusTypes,int,char> m_aiFreeBonus;
	EagerEnumMap<BonusTypes,int,short> m_aiNumBonuses;
	ListEnumMap<BonusTypes,int,short> m_aiNumCorpProducedBonuses;
	ListEnumMap<ProjectTypes,int> m_aiProjectProduction;
	ListEnumMap<BuildingTypes,int> m_aiBuildingProduction;
	ListEnumMap<BuildingTypes,int,short> m_aiBuildingProductionTime;
	ListEnumMap<BuildingTypes,CivilizationTypes> m_aeBuildingOriginalOwner;
	// advc: Was MIN_INT as a magic number
	static int const iBuildingOriginalTimeUnknown = MIN_SHORT;
	EagerEnumMap<BuildingTypes,int,short,iBuildingOriginalTimeUnknown> m_aiBuildingOriginalTime;
	EagerEnumMap<BuildingTypes,int,char> m_aiNumRealBuilding;
	ArrayEnumMap<BuildingTypes,int,char> m_aiNumFreeBuilding;
	ListEnumMap<UnitTypes,int> m_aiUnitProduction;
	ListEnumMap<UnitTypes,int,short> m_aiUnitProductionTime;
	ArrayEnumMap<UnitTypes,int,short> m_aiGreatPeopleUnitRate;
	ArrayEnumMap<UnitTypes,int> m_aiGreatPeopleUnitProgress;
	ArrayEnumMap<SpecialistTypes,int,short> m_aiSpecialistCount;
	ArrayEnumMap<SpecialistTypes,int,short> m_aiMaxSpecialistCount;
	ArrayEnumMap<SpecialistTypes,int,char> m_aiForceSpecialistCount;
	ArrayEnumMap<SpecialistTypes,int,char> m_aiFreeSpecialistCount;
	ListEnumMap<ImprovementTypes,int,char> m_aiImprovementFreeSpecialists;
	ArrayEnumMap<ReligionTypes,int,char> m_aiReligionInfluence;
	ArrayEnumMap<ReligionTypes,int,char> m_aiStateReligionHappiness;
	ArrayEnumMap<ReligionTypes,int,char> m_aiShrine; // advc.enum
	ArrayEnumMap<UnitCombatTypes,int,char> m_aiUnitCombatFreeExperience;
	ListEnumMap<PromotionTypes,int,char> m_aiFreePromotionCount;

	ListEnumMap<CivilizationTypes,int,short> m_aiGameTurnCivLost; // doc
	ArrayEnumMap<CulturePlotTypes,int,short> m_aiCulturePlots; // doc
	ArrayEnumMap<CulturePlotTypes,int,short> m_aiCultureCosts; // doc

	EagerEnumMap<CivilizationTypes,bool> m_abEverOwned;
	EagerEnumMap<PlayerTypes,bool> m_abTradeRoute;
	EagerEnumMap<TeamTypes,bool> m_abRevealed;
	ArrayEnumMap<TeamTypes,bool> m_abEspionageVisibility;
	EagerEnumMap<CityPlotTypes,bool> m_abWorkingPlot;
	ArrayEnumMap<ReligionTypes,bool> m_abHasReligion;
	ArrayEnumMap<CorporationTypes,bool> m_abHasCorporation;
	// </advc.enum>
	CvWString m_szPreviousName; // advc.106k
	CvString m_szScriptData;
	// <advc.opt>
	CvArea* m_pArea;
	CvPlot* m_pPlot; // </advc.opt>

	std::vector< std::pair < UnitClassTypes, HurryTypes > > m_hurriedUnits; // doc // TODO: find correct type

	std::vector<IDInfo> m_aTradeCities; // advc: was an array
	mutable CLinkList<OrderData> m_orderQueue;
	std::vector<std::pair<float,float> > m_kWallOverridePoints;
	std::vector<EventTypes> m_aEventsOccured;
	// <advc.enum> Replacing naked vectors of tuples
	Enum2IntEncMap<ListEnumMap<BuildingClassTypes,YieldChangeMap::enc_t>,
			YieldChangeMap> m_aeiiBuildingYieldChange;
	Enum2IntEncMap<ListEnumMap<BuildingClassTypes,CommerceChangeMap::enc_t>,
			CommerceChangeMap> m_aeiiBuildingCommerceChange;
	Enum2IntEncMap<ListEnumMap<BonusTypes,YieldChangeMap::enc_t>,
			YieldChangeMap> m_aeiiBonusYieldChange;
	ListEnumMap<BuildingClassTypes,int,char> m_aeiBuildingHappyChange;
	ListEnumMap<BuildingClassTypes,int,char> m_aeiBuildingHealthChange; // </advc.enum>
	ListEnumMap<BuildingClassTypes,int,char> m_aeiBuildingGreatPeopleRateChange; // doc

	// Rank cache
	mutable int	m_iPopulationRank;
	mutable bool m_bPopulationRankValid;
	// <advc.enum>
	/*	Made mutable (not strictly necessary b/c findBaseYieldRateRank
		accesses them through a CvCity pointer) */
	mutable EagerEnumMap<YieldTypes,int,short,-1> m_aiBaseYieldRank;
	mutable EagerEnumMap<YieldTypes,bool> m_abBaseYieldRankValid;
	mutable EagerEnumMap<YieldTypes,int,short,-1> m_aiYieldRank;
	mutable EagerEnumMap<YieldTypes,bool> m_abYieldRankValid;
	mutable EagerEnumMap<CommerceTypes,int,short,-1> m_aiCommerceRank;
	mutable EagerEnumMap<CommerceTypes,bool> m_abCommerceRankValid; // </advc.enum>

	void doGrowth();
	void doCulture();
	bool doCheckProduction();
	// <advc.064d>
	void upgradeProduction();
	bool checkCanContinueProduction(bool bCheckUpgrade = true,
			ChooseProductionPlayers eChoose = ALL_CHOOSE);
	// </advc.064d>
	void doProduction(bool bAllowNoProduction);
	void doDecay();
	void doReligion();
	void doGreatPeople();
	void doMeltdown();

	// <advc>
	void changeCommerceRateTimes100(CommerceTypes eCommerce, int iChange);
	void setCommerceRateTimes100(CommerceTypes eCommerce, int iRate); // </advc>
	int getExtraProductionDifference(int iExtra, UnitTypes eUnit) const
	{
		return getExtraProductionDifference(iExtra, getProductionModifier(eUnit));
	}
	int getExtraProductionDifference(int iExtra, BuildingTypes eBuilding) const
	{
		return getExtraProductionDifference(iExtra, getProductionModifier(eBuilding));
	}
	int getExtraProductionDifference(int iExtra, ProjectTypes eProject) const
	{
		return getExtraProductionDifference(iExtra, getProductionModifier(eProject));
	}
	int getExtraProductionDifference(int iExtra, int iModifier) const
	{
		return (iExtra * getBaseYieldRateModifier(YIELD_PRODUCTION, iModifier)) / 100;
	}
	// advc.001: For accurate calculation of hurry cost
	int getInverseProductionDifference(int iExtra, int iModifier) const
	{
		return intdiv::uceil(iExtra * 100, getBaseYieldRateModifier(YIELD_PRODUCTION, iModifier));
	}
	int getHurryCostModifier(UnitTypes eUnit, bool bIgnoreNew) const;
	int getHurryCostModifier(BuildingTypes eBuilding, bool bIgnoreNew) const;
	int getHurryCostModifier(int iBaseModifier, int iProduction, bool bIgnoreNew) const;
	int getHurryCost(bool bExtra, UnitTypes eUnit, bool bIgnoreNew) const;
	int getHurryCost(bool bExtra, BuildingTypes eBuilding, bool bIgnoreNew) const;
	int getHurryCost(bool bExtra, int iProductionLeft, int iHurryModifier, int iModifier) const;
	int getHurryPopulation(HurryTypes eHurry, int iHurryCost) const;
	int getHurryGold(HurryTypes eHurry, int iHurryCost) const;
	bool canHurryUnit(HurryTypes eHurry, UnitTypes eUnit, bool bIgnoreNew) const;
	bool canHurryBuilding(HurryTypes eHurry, BuildingTypes eBuilding, bool bIgnoreNew) const;
	// <advc.310>
	void addGreatWall(int iAttempt = 0); // Wrapper for CvEngine::AddGreatWall
	bool needsGreatWallSegment(CvPlot const& kInside, CvPlot const& kOutside,
			int iAttempt) const;
	// </advc.310>
	void updateBuildingDefense(); // advc.004c
	scaled defensiveGarrison(scaled stopCountingAt = -1) const; // advc.500b
	//int calculateMaintenanceDistance() const;
	// advc.004b: Replacing the above (which was public, but is only used internally)
	static int calculateMaintenanceDistance(CvPlot const* cityPlot, PlayerTypes owner);
	void damageGarrison(PlayerTypes eRevoltSource);
	// advc.123f:
	void failProduction(int iOrderData, int iInvestedProduction, bool bProject = false);
	// <advc.064b>
	void handleOverflow(int iRawOverflow, int iProductionModifier, OrderTypes eOrderType);
	int failGoldPercent(OrderTypes eOrder) const; // also used by 123f
	void payOverflowGold(int iLostProduction, int iGoldChange);
	int getProductionTurnsLeft(int iProductionNeeded, int iProduction,
			int iProductionModifier, bool bFoodProduction, int iNum) const;
	// </advc.064b
	void doPopOrder(CLLNode<OrderData>* pOrder); // advc.064d
	// advc.901:
	std::pair<int,int> calculateSurroundingHealth(int iExtraGoodPercent = 0, int iExtraBadPercent = 0) const;
};

#endif
