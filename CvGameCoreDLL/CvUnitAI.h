#pragma once

// unitAI.h

#ifndef CIV4_UNIT_AI_H
#define CIV4_UNIT_AI_H

#include "CvUnit.h"

class CvCity;
class CvSelectionGroupAI; // advc.003u

class CvUnitAI : public CvUnit
{
public:

	CvUnitAI();
	~CvUnitAI();
	// advc.003u: Override replacing AI_init. Parameter list copied from CvUnit::init.
	void init(int iID, UnitTypes eUnit, UnitAITypes eUnitAI, PlayerTypes eOwner,
			int iX, int iY, DirectionTypes eFacingDirection);

	bool AI_update();
	bool AI_follow(/* K-Mod: */ bool bFirst = true);
	void AI_upgrade();
	void AI_promote();

	int AI_groupFirstVal() const;
	int AI_groupSecondVal() const;

	int AI_attackOdds(const CvPlot* pPlot, bool bPotentialEnemy) const;
	int AI_opportuneOdds(int iActualOdds, CvUnit const& kDefender) const; // advc

	bool AI_bestCityBuild(CvCityAI const& kCity, CvPlot** ppBestPlot = NULL, BuildTypes* peBestBuild = NULL,
			CvPlot* pIgnorePlot = NULL, CvUnit* pUnit = NULL) const;
	bool AI_isCityAIType() const;
	// <advc>
	bool AI_mayAttack(TeamTypes eTeam, CvPlot const& kPlot) const; // Renamed from AI_potentialEnemy
	bool AI_mayAttack(CvPlot const& kPlot) const; // Replacing CvUnit::potentialWarAction
	bool AI_isPotentialEnemyOf(TeamTypes eTeam, CvPlot const& kPlot) const; // Moved from CvUnit
	int AI_countEnemyDefenders(CvPlot const& kPlot) const; // Replacing CvPlot::getNumVisiblePotentialEnemyDefenders
	bool AI_isAnyEnemyDefender(CvPlot const& kPlot) const;
	// </advc>
	int AI_getBirthmark() const { return m_iBirthmark; }
	void AI_setBirthmark(int iNewValue);

	UnitAITypes AI_getUnitAIType() const { return m_eUnitAIType; } 									// Exposed to Python
	void AI_setUnitAIType(UnitAITypes eNewValue);
	CvSelectionGroupAI const* AI_getGroup() const; // advc.003u
	CvSelectionGroupAI* AI_getGroup(); // advc.003u

	// <advc.159>
	int AI_currEffectiveStr(CvPlot const* pPlot = NULL, CvUnit const* pOther = NULL,
			bool bCountCollateral = false, int iBaseCollateral = 0,
			bool bCheckCanAttack = false,
			int iCurrentHP = -1, bool bAssumePromotion = false) const; // advc.139
	/*	collateralDamage no longer includes promotions since BtS 3.17, but
		the AI should take promotions into account when estimating coll. damage.
		Not currently used for deciding whether a unit deals _any_ coll. damage. */
	int AI_collateralDmgFactor() const
	{	/*	Multiplication would be closer to how collateralCombat works, but,
			for most units, it won't matter much, and addition is faster. */
		return collateralDamage() + getExtraCollateralDamage();
	}
	// </advc.159>
	int AI_sacrificeValue(const CvPlot* pPlot) const;
	// Lead From Behind by UncutDragon (edited for K-Mod):
	void LFBgetBetterAttacker(CvUnitAI** ppAttacker, const CvPlot* pPlot, bool bPotentialEnemy, int& iAIAttackOdds, int& iAttackerValue);

	std::pair<CvPlot*, CvPlot*> AI_spreadTarget(ReligionTypes eReligion, bool bGreatMission = false); // doc
	CvCity* AI_persecutionTarget(); // doc

	void read(FDataStreamBase* pStream);
	void write(FDataStreamBase* pStream);

	static CvUnitAI* fromIDInfo(IDInfo id); // advc

protected:

	void finalizeInit(); // advc.003u: override

	int m_iBirthmark;

	UnitAITypes m_eUnitAIType;

	int m_iAutomatedAbortTurn;
	int m_iSearchRangeRandPercent; // advc.128

	bool AI_considerDOW(CvPlot const& kPlot); // K-Mod
	bool AI_considerPathDOW(CvPlot const& kPlot, MovementFlags eFlags); // K-Mod
	// K-Mod
	CvUnit* AI_findTransport(UnitAITypes eUnitAI, MovementFlags eFlags = NO_MOVEMENT_FLAGS,
			int iMaxPath = MAX_INT, UnitAITypes ePassengerAI = NO_UNITAI,
			int iMinCargo = -1, int iMinCargoSpace = -1, int iMaxCargoSpace = -1,
			int iMaxCargoOurUnitAI = -1);
	// K-Mod end
	void AI_animalMove();
	void AI_settleMove();
	void AI_workerMove(/* advc.113b: */ bool bUpdateWorkersHave = true);
	void AI_barbAttackMove();
	void AI_attackMove();
	void AI_attackCityMove();
	void AI_attackCityLemmingMove();
	void AI_collateralMove();
	void AI_pillageMove();
	void AI_reserveMove();
	void AI_counterMove();
	void AI_paratrooperMove();
	void AI_cityDefenseMove();
	void AI_cityDefenseExtraMove();
	void AI_exploreMove();
	void AI_missionaryMove();
	void AI_generalMove();
	void AI_greatPersonMove(); // K-Mod
	void AI_spyMove();
	void AI_ICBMMove();
	void AI_workerSeaMove();
	void AI_barbAttackSeaMove();
	void AI_pirateSeaMove();
	void AI_attackSeaMove();
	void AI_reserveSeaMove();
	void AI_escortSeaMove();
	void AI_exploreSeaMove();
	void AI_assaultSeaMove();
	void AI_settlerSeaMove();
	void AI_missionarySeaMove();
	void AI_spySeaMove();
	void AI_carrierSeaMove();
	void AI_missileCarrierSeaMove();
	void AI_attackAirMove();
	void AI_defenseAirMove();
	void AI_carrierAirMove();
	void AI_missileAirMove();
	void AI_persecutorMove(); // doc
	void AI_satelliteMove(); // doc

	void AI_networkAutomated();
	void AI_cityAutomated();

	int AI_promotionValue(PromotionTypes ePromotion);

// advc (comment): The boolean functions below return true iff a mission was pushed
	bool AI_shadow(UnitAITypes eUnitAI, int iMax = -1, int iMaxRatio = -1, bool bWithCargoOnly = true,
	// BETTER_BTS_AI_MOD (Unit AI), 04/01/10, jdog5000:
			bool bOutsideCityOnly = false, int iMaxPath = MAX_INT);
	// K-Mod. I've created AI_omniGroup with the intention of using it to phase out AI_group and AI_groupMergeRange.
	bool AI_omniGroup(UnitAITypes eUnitAI, int iMaxGroup = -1, int iMaxOwnUnitAI = -1,
			bool bStackOfDoom = false, MovementFlags eFlags = NO_MOVEMENT_FLAGS,
			int iMaxPath = -1, bool bMergeGroups = true, bool bSafeOnly = true,
			bool bIgnoreFaster = false, bool bIgnoreOwnUnitType = false,
			bool bBiggerOnly = true, int iMinUnitAI = -1, bool bWithCargoOnly = false,
			bool bIgnoreBusyTransports = false);
	bool AI_group(UnitAITypes eUnitAI, int iMaxGroup = -1, int iMaxOwnUnitAI = -1,
			int iMinUnitAI = -1, bool bIgnoreFaster = false, bool bIgnoreOwnUnitType = false,
			bool bStackOfDoom = false, int iMaxPath = MAX_INT, bool bAllowRegrouping = false,
			bool bWithCargoOnly = false, bool bInCityOnly = false,
			MissionAITypes eIgnoreMissionAIType = NO_MISSIONAI);
	bool AI_load(UnitAITypes eUnitAI, MissionAITypes eMissionAI,
			UnitAITypes eTransportedUnitAI = NO_UNITAI, int iMinCargo = -1,
			int iMinCargoSpace = -1, int iMaxCargoSpace = -1,
			int iMaxCargoOurUnitAI = -1, MovementFlags eFlags = NO_MOVEMENT_FLAGS, int iMaxPath = MAX_INT,
			// BETTER_BTS_AI_MOD, War tactics AI, Unit AI, 04/18/10, jdog5000:
			int iMaxTransportPath = MAX_INT);

	bool AI_guardCityBestDefender();
	bool AI_guardCityOnlyDefender(); // K-Mod
	bool AI_guardCityMinDefender(bool bSearch = true);
	bool AI_guardCity(bool bLeave = false, bool bSearch = false, int iMaxPath = MAX_INT,
			MovementFlags eFlags = NO_MOVEMENT_FLAGS,
			int iExtraDefenders = 0); // advc.300
	bool AI_guardCityAirlift();
	// <K-Mod>
	bool AI_guardCoast(bool bPrimaryOnly = false,
			MovementFlags eFlags = NO_MOVEMENT_FLAGS, int iMaxPath = -1); // </K-Mod>
	bool AI_guardBonus(int iMinValue = 0);
	// advc.028b:
	void AI_getGuardedPlots(CvPlot const& kFrom, std::vector<CvPlot*>& kResult) const;
	bool AI_guardYield(); // advc.300
	bool AI_barbAmphibiousCapture(); // advc.306
	int AI_getPlotDefendersNeeded(CvPlot const& kPlot, int iExtra /* advc: */ = 0);
	bool AI_guardFort(bool bSearch = true);
	bool AI_guardCitySite();
	bool AI_guardSpy(int iRandomPercent);
	bool AI_destroySpy();
	bool AI_sabotageSpy();
	bool AI_pickupTargetSpy();
	bool AI_chokeDefend();
	bool AI_heal(int iDamagePercent = 0, int iMaxPath = MAX_INT);
	// advc.299:
	bool AI_singleUnitHeal(int iMaxTurnsExposed = 1, int iMaxTurnsOutsideCity = 3);
	ProbabilityTypes AI_isThreatenedFromLand() const; // advc.139
	bool AI_afterAttack();
	bool AI_goldenAge();
	bool AI_spreadReligion();
	bool AI_spreadCorporation();
	bool AI_spreadReligionAirlift();
	bool AI_spreadCorporationAirlift();
	bool AI_discover(bool bThisTurnOnly = false, bool bFirstResearchOnly = false);
	bool AI_lead(std::vector<UnitAITypes>& aeAIUnitTypes);
	bool AI_join(int iMaxCount = MAX_INT);
	bool AI_construct(int iMaxCount = MAX_INT, int iMaxSingleBuildingCount = MAX_INT,
			int iThreshold = 15);
	/*bool AI_switchHurry(); // advc.003j
	bool AI_hurry();*/
	//bool AI_greatWork(); // disabled by K-Mod
	bool AI_offensiveAirlift();
	bool AI_paradrop(int iRange);
	#if 0 // advc: unused
	bool AI_protect(int iOddsThreshold, MovementFlags eFlags = NO_MOVEMENT_FLAGS, int iMaxPathTurns = MAX_INT);
	#endif
	bool AI_patrol();
	bool AI_defend();
	bool AI_safety();
	bool AI_hide();
	bool AI_goody(int iRange);
	MovementFlags AI_exploreFlags() const; // advc.255
	bool AI_explore();
	bool AI_exploreRange(int iRange);
    bool AI_foundFirstCity(); // advc.108
    bool AI_exploreCoasts(); // doc
    bool AI_exploreCircumnavigate(); // doc
    bool AI_isTargetableCity(CvCity* pCity); // doc

	// BETTER_BTS_AI_MOD, War tactics AI, 03/29/10, jdog5000: START
	CvCity* AI_pickTargetCity(MovementFlags eFlags = NO_MOVEMENT_FLAGS,
			int iMaxPathTurns = MAX_INT, bool bHuntBarbs = false);
	bool AI_goToTargetCity(MovementFlags eFlags = NO_MOVEMENT_FLAGS,
			int iMaxPathTurns = MAX_INT, CvCity* pTargetCity = NULL);
	//bool AI_goToTargetBarbCity(int iMaxPathTurns = 10); // disabled by K-Mod. (duplicate code ftl)
	bool AI_pillageAroundCity(CvCity* pTargetCity, int iBonusValueThreshold = 0,
			MovementFlags eFlags = NO_MOVEMENT_FLAGS, int iMaxPathTurns = MAX_INT);
	bool AI_bombardCity();
	bool AI_cityAttack(int iRange, int iOddsThreshold,
			MovementFlags eFlags = NO_MOVEMENT_FLAGS, bool bFollow = false);
	bool AI_anyAttack(int iRange, int iOddsThreshold,
			MovementFlags eFlags = NO_MOVEMENT_FLAGS, int iMinStack = 0,
			bool bAllowCities = true, bool bFollow = false);
	// BETTER_BTS_AI_MOD: END
	bool AI_rangeAttack(int iRange);
	bool AI_leaveAttack(int iRange, int iThreshold, int iStrengthThreshold);
	bool AI_defensiveCollateral(int iThreshold, int iSearchRange); // K-Mod
	bool AI_evacuateCity(); // advc.139
	// <K-Mod>
	bool AI_defendTerritory(int iThreshold, MovementFlags eFlags, int iMaxPathTurns,
			bool bLocal = false);
	bool AI_stackVsStack(int iSearchRange, int iAttackThreshold, int iRiskThreshold,
			MovementFlags eFlags /* advc: */ = NO_MOVEMENT_FLAGS); // </K-Mod>
	bool AI_blockade();
	bool AI_pirateBlockade();
	bool AI_seaBombardRange(int iMaxRange);
	bool AI_pillage(int iBonusValueThreshold = 0, MovementFlags eFlags = NO_MOVEMENT_FLAGS);
	bool AI_pillageRange(int iRange, int iBonusValueThreshold = 0,
			MovementFlags eFlags = NO_MOVEMENT_FLAGS);
	bool AI_found(MovementFlags eFlags = MOVE_NO_ENEMY_TERRITORY); // K-Mod added flags
	//bool AI_foundRange(int iRange, bool bFollow = false); // disabled by K-Mod
	bool AI_foundFollow(); // K-Mod
	bool AI_assaultSeaTransport(bool bAttackBarbs = false, /* K-Mod: */ bool bLocal = false,
			int iMaxAreaCities = MAX_INT); // advc.082
	bool AI_assaultSeaReinforce(bool bAttackBarbs = false); // BBAI
	// <K-Mod>
	bool AI_transportGoTo(CvPlot const& kEndTurnPlot, CvPlot const& kTargetPlot,
			MovementFlags eFlags, MissionAITypes eMissionAI); // </K-Mod>

	bool AI_settlerSeaTransport();
	bool AI_ferryWorkers();
	bool AI_specialSeaTransportMissionary();
	bool AI_specialSeaTransportSpy();
	bool AI_carrierSeaTransport();
	bool AI_connectPlot(CvPlot const& kPlot, int iRange = 0);
	CvCityAI* AI_getCityToImprove() const; // advc.113b
	bool AI_improveCity(CvCityAI const& kCity);
	bool AI_improveLocalPlot(int iRange, CvCity const* pIgnoreCity,
			int iMissingWorkersInArea = 0); // advc.117
	bool AI_nextCityToImprove(CvCity const* pCity);
	bool AI_nextCityToImproveAirlift();
	bool AI_irrigateTerritory();
	bool AI_fortTerritory(bool bCanal, bool bAirbase);
	//bool AI_improveBonus(int iMinValue = 0, CvPlot** ppBestPlot = NULL, BuildTypes* peBestBuild = NULL, int* piBestValue = NULL);
	bool AI_improveBonus( // K-Mod
			int iMissingWorkersInArea = 0); // advc.121
	bool AI_improvePlot(CvPlot const& kPlot, BuildTypes eBuild);
	BuildTypes AI_betterPlotBuild(CvPlot const& kPlot, BuildTypes eBuild);
	bool AI_connectBonus(bool bTestTrade = true);
	bool AI_connectCity();
	bool AI_routeCity();
	bool AI_routeTerritory(bool bImprovementOnly = false);
	bool AI_travelToUpgradeCity();
	bool AI_retreatToCity(bool bPrimary = false, bool bPrioritiseAirlift = false, int iMaxPath = MAX_INT);
	bool AI_handleStranded(MovementFlags eFlags = NO_MOVEMENT_FLAGS); // K-Mod
	// BETTER_BTS_AI_MOD, Naval AI, 01/15/09, jdog5000: START
	bool AI_pickup(UnitAITypes eUnitAI, bool bCountProduction = false, int iMaxPath = MAX_INT);
	bool AI_pickupStranded(UnitAITypes eUnitAI = NO_UNITAI, int iMaxPath = MAX_INT);
	// advc: New auxiliary function
	bool AI_considerPickup(UnitAITypes eUnitAI, CvCityAI const& kCity) const;
	// BETTER_BTS_AI_MOD: END
	bool AI_airOffensiveCity();
	bool AI_airDefensiveCity();
	bool AI_airCarrier();
	bool AI_missileLoad(UnitAITypes eTargetUnitAI, int iMaxOwnUnitAI = -1, bool bStealthOnly = false);
	bool AI_airStrike(int iThreshold = 0); // K-Mod note. this function now handles bombing defences, and defensive strikes.
	int AI_airStrikeValue(CvPlot const& kPlot, int iCurrentBest, bool& bBombard) const; // advc

	// BETTER_BTS_AI_MOD, Air AI, 9/26/08, jdog5000: START
	int AI_airOffenseBaseValue(CvPlot const& kPlot);
	//bool AI_defensiveAirStrike(); // disabled by K-Mod
	bool AI_defendBaseAirStrike();
	// BETTER_BTS_AI_MOD: END
	bool AI_airBombPlots();
	//bool AI_airBombDefenses(); // disabled by K-Mod
	bool AI_exploreAirCities();

	// BETTER_BTS_AI_MOD, Player Interface, 01/12/09, jdog5000: START
	int AI_exploreAirPlotValue(CvPlot const* pPlot);
	bool AI_exploreAirRange(/* advc.029: */ bool bExcludeVisible = true);
	void AI_exploreAirMove();
	// BETTER_BTS_AI_MOD: END

	bool AI_nuke(); // advc.650: Merged AI_nukeRange into this
	//bool AI_trade(int iValueThreshold); // deleted by K-Mod
	int AI_tradeMissionValue(CvPlot*& pBestPlot, int iThreshold = 0); // K-Mod
	bool AI_doTradeMission(CvPlot* pTradePlot); // K-Mod
	int AI_greatWorkValue(CvPlot*& pBestPlot, int iThreshold = 0); // K-Mod
	bool AI_doGreatWork(CvPlot* pCulturePlot); // K-Mod
	bool AI_infiltrate();
	bool AI_reconSpy(int iRange);
	// BETTER_BTS_AI_MOD, Espionage AI, 10/20/09, jdog5000: START
	bool AI_revoltCitySpy();
	bool AI_bonusOffenseSpy(int iMaxPath);
	bool AI_cityOffenseSpy(int iRange, CvCity* pSkipCity = NULL);
	// BETTER_BTS_AI_MOD: END
	bool AI_espionageSpy();
	EspionageMissionTypes AI_bestPlotEspionage(int& iData) const; // K-Mod
	bool AI_moveToStagingCity();
	bool AI_seaRetreatFromCityDanger();
	bool AI_airRetreatFromCityDanger();
	bool AI_airAttackDamagedSkip();

	bool AI_resolveCrisis(int iTurns); // doc
	bool AI_reformGovernment(int iNumChanges); // doc
	bool AI_diplomaticMission(int iPowerMultiplier); // doc
	bool AI_persecute(); // doc
	bool AI_greatMission(int iCityPercent); // doc
	bool AI_satelliteDefendMove(); // doc
	bool AI_satelliteAttackMove(); // doc
	bool AI_rebuildMove(int iMinimumCost); // doc

	bool AI_followBombard();

	// <advc.033>
	std::pair<int,int> AI_countPiracyTargets(CvPlot const& kPlot,
			bool bStopIfAnyTarget = false) const;
	bool AI_isAnyPiracyTarget(CvPlot const& p) const;
	// </advc.033>
	bool AI_defendPlot(CvPlot* pPlot);
	int AI_pillageValue(CvPlot const& kPlot, int iBonusValueThreshold = 0);
	//bool AI_canPillage(CvPlot& kPlot) const; // advc.003j
	//int AI_nukeValue(CvCity* pCity);
	// <K-Mod>
	int AI_nukeValue(CvPlot const& kCenterPlot, int iSearchRange,
			CvPlot const*& pBestTarget, int iCivilianTargetWeight = 50) const; // </K-Mod>
	// <advc.121>
	int AI_connectBonusCost(CvPlot const& p, BuildTypes eBuild,
			int iMissingWorkersInArea) const;
	bool AI_canConnectBonus(CvPlot const& p, BuildTypes eBuild) const;
	// </advc.121>
	int AI_searchRange(int iRange);
	bool AI_plotValid(CvPlot /* advc: */ const* pPlot) const;
	// <advc> Allow a reference to be used
	bool AI_plotValid(CvPlot const& kPlot) const
	{
		return AI_plotValid(&kPlot);
	} // </advc>
	// advc.030:
	bool AI_canEnterByLand(CvArea const& kArea) const
	{	// Not checked (to save time): unused canMoveAllTerrain
		return (isArea(kArea) || (canMoveImpassable() && canEnterArea(kArea)));
	}

	//int AI_finalOddsThreshold(CvPlot* pPlot, int iOddsThreshold); // disabled by K-Mod
	unsigned AI_unitBirthmarkHash(int iExtra = 0) const; // K-Mod
	unsigned AI_unitPlotHash(const CvPlot* pPlot, int iExtra = 0) const; // K-Mod

	int AI_stackOfDoomExtra() const;

	//bool AI_stackAttackCity(int iRange, int iPowerThreshold, bool bFollow = true);
	// K-Mod. used for adjacent cities only. Negative threshold means 'automatic'.
	bool AI_stackAttackCity(int iPowerThreshold = -1);
	bool AI_moveIntoCity(int iRange);

	bool AI_groupMergeRange(UnitAITypes eUnitAI, int iRange, bool bBiggerOnly = true,
			bool bAllowRegrouping = false, bool bIgnoreFaster = false);

	//bool AI_artistCultureVictoryMove(); // disabled by K-Mod
	bool AI_poach();
	bool AI_choke(int iRange = 1, bool bDefensive = false,
			MovementFlags eFlags = NO_MOVEMENT_FLAGS);
	// advc.012: CvUnit::plot if pPlot=NULL; cf. CvTeamAI::plotDefense.
	int AI_plotDefense(CvPlot const* pPlot = NULL) const;

	bool AI_solveBlockageProblem(CvPlot* pDestPlot, bool bDeclareWar);

	int AI_calculatePlotWorkersNeeded(CvPlot const& kPlot, BuildTypes eBuild) const;
	//int AI_getEspionageTargetValue(CvPlot* pPlot, int iMaxPath);
	int AI_getEspionageTargetValue(CvPlot* pPlot); // K-Mod

	bool AI_canGroupWithAIType(UnitAITypes eUnitAI) const;
	bool AI_allowGroup(CvUnitAI const& kUnit, UnitAITypes eUnitAI) const;
	// <advc>
	bool AI_shouldRouteWhileImproving(CvPlot const& kDest, MovementFlags& eFlags,
			CvCity const* pDestCity = NULL) const; // </advc>
	// advc.pf:
	bool AI_canRouteThroughSafeTerritory(CvPlot const& kDest, MovementFlags& eFlags) const;
	bool AI_moveSettlerToCoast(int iMaxPathTurns = 5); // advc.040

	CvCity* AI_offensiveSatelliteTarget() const; // doc
	CvCity* AI_offensiveNukeTarget() const; // doc
	CvPlot* AI_defensiveNukeTarget() const; // doc

	// added so under cheat mode we can call protected functions for testing
	friend class CvGameTextMgr;
};

#endif
