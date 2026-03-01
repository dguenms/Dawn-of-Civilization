#pragma once

// teamAI.h

#ifndef CIV4_TEAM_AI_H
#define CIV4_TEAM_AI_H // advc.003u (caveat): This guard gets referenced in CvTeam.h

#include "CvTeam.h"
#include "UWAI.h" // advc.104
#include "AIStrengthMemoryMap.h" // advc.158
#include "AIStrategies.h" // advc.enum

// <advc.003u> Let the more powerful macros take precedence
#if !defined(CIV4_GAME_PLAY_H) && !defined(COREAI_H)
	#undef GET_TEAM
	#define GET_TEAM(x) CvTeamAI::AI_getTeam(x)
#endif // </advc.003u>

class CvTeamAI : public CvTeam
{
public:

#ifdef _DEBUG
	__forceinline // Annoying to step into by accident
#endif
	// advc.003u: Renamed from getTeam
	static CvTeamAI& AI_getTeam(TeamTypes eTeam)
	{
		FAssertBounds(0, MAX_TEAMS, eTeam);
		return *m_aTeams[eTeam];
	}
	DllExport static CvTeamAI& getTeamNonInl(TeamTypes eTeam); // Only for the EXE

	static bool AI_isChosenWarPlan(WarPlanTypes eWarPlanType); // advc.105
	// advc.opt:
	static bool AI_isImminentWarPlan(WarPlanTypes eWarPlanType)
	{
		return (eWarPlanType == WARPLAN_LIMITED || eWarPlanType == WARPLAN_TOTAL ||
				eWarPlanType == WARPLAN_DOGPILE);
	}

	explicit CvTeamAI(TeamTypes eID);
	~CvTeamAI();
	void AI_init();
	void AI_uninit();
	void AI_reset(bool bConstructor);

	void AI_doTurnPre();
	void AI_doTurnPost();

	void AI_makeAssignWorkDirty();

	int AI_chooseElection(const VoteSelectionData& kVoteSelectionData) const;

	void AI_updateAreaStrategies(bool bTargets = true); // advc: "Stragies"->"Strategies"
	void AI_updateAreaTargets();

	int AI_countFinancialTrouble() const; // addvc.003j (comment): unused
	int AI_countMilitaryWeight(CvArea const* pArea = NULL) const;
	// <advc.104>, advc.038, advc.132:
	scaled AI_estimateDemographic(PlayerTypes ePlayer, PlayerHistoryTypes eDemographic,
			int iSamples = 5) const;
	scaled AI_estimateYieldRate(PlayerTypes ePlayer, YieldTypes eYield, // (exposed to Python)
			 int iSamples = 5) const; // </advc.104>
	int AI_estimateTotalYieldRate(YieldTypes eYield) const; // K-Mod
	bool AI_deduceCitySite(CvCity const& kCity) const; // K-Mod
	// <advc.erai>
	scaled AI_getCurrEraFactor() const;
	int AI_getCurrEra() const { return AI_getCurrEraFactor().round(); }
	// </advc.erai>

	bool AI_isAnyCapitalAreaAlone() const;
	bool AI_isPrimaryArea(CvArea const& kArea) const;
	bool AI_hasCitiesInPrimaryArea(TeamTypes eTeam) const;
	bool AI_hasSharedPrimaryArea(TeamTypes eTeam) const; // K-Mod
	AreaAITypes AI_calculateAreaAIType(CvArea const& kArea, bool bPreparingTotal = false) const;
	bool AI_isLonely() const { return m_bLonely; } // advc.109

	int AI_calculateAdjacentLandPlots(TeamTypes eTeam) const;
	int AI_calculateCapitalProximity(TeamTypes eTeam) const;
	int AI_calculatePlotWarValue(TeamTypes eTeam) const;

	// BETTER_BTS_AI_MOD, General AI, 07/10/08, jdog5000:
	int AI_calculateBonusWarValue(TeamTypes eTeam) const;

	bool AI_haveSeenCities(TeamTypes eTeam, bool bPrimaryAreaOnly = false, int iMinimum = 1) const; // K-Mod
	bool AI_isWarPossible() const;
	bool AI_isLandTarget(TeamTypes eTarget, /* advc: */ bool bCheckAlliesOfTarget = false) const;
	//bool AI_isAllyLandTarget(TeamTypes eTeam) const; // advc: Merged into the above
	// BETTER_BTS_AI_MOD, General AI, 11/30/08, jdog5000: START  advc.pf: Moved from CvPlot
	bool AI_isHasPathToEnemyCity(CvPlot const& kFrom, bool bIgnoreBarb = true) const;
	bool AI_isHasPathToEnemyCity(CvPlot const& kFrom, CvTeam const& kEnemy) const;
	// BETTER_BTS_AI_MOD: END
	bool AI_shareWar(TeamTypes eTeam) const;								// Exposed to Python
	 // advc, advc.130e:
	void AI_updateAttitude(TeamTypes eTeam, bool bUpdateWorstEnemy = true);
	AttitudeTypes AI_getAttitude(TeamTypes eTeam, bool bForced = true) const;
	int AI_getAttitudeVal(TeamTypes eTeam, bool bForced = true,
			bool bAssert = true) const; // advc
	int AI_getMemoryCount(TeamTypes eTeam, MemoryTypes eMemory) const;
	// <advc>
	void AI_preDeclareWar(TeamTypes eTarget, WarPlanTypes eWarPlan, bool bPrimaryDoW,
			PlayerTypes eSponsor); // advc.100
	void AI_postDeclareWar(TeamTypes eTarget, WarPlanTypes eWarPlan);
	void AI_preMakePeace(TeamTypes eTarget, CLinkList<TradeData> const* pReparations);
	void AI_postMakePeace(TeamTypes eTarget);
	//int AI_startWarVal(TeamTypes eTeam) const;
	int AI_startWarVal(TeamTypes eTarget, WarPlanTypes eWarPlan, // K-Mod
			bool bConstCache = false) const; // advc.001n
	int AI_endWarVal(TeamTypes eTeam) const;

	scaled CvTeamAI::AI_knownTechValModifier(TechTypes eTech) const; // K-Mod

	int AI_techTradeVal(TechTypes eTech, TeamTypes eFromTeam,
			bool bIgnoreDiscount = false, // advc.550a
			bool bPeaceDeal = false) const; // advc.140h
	DenialTypes AI_techTrade(TechTypes eTech, TeamTypes eToTeam) const;

	int AI_mapTradeVal(TeamTypes eFromTeam) const;
	DenialTypes AI_mapTrade(TeamTypes eToTeam) const;

	int AI_vassalTradeVal(TeamTypes eTeam) const;
	DenialTypes AI_vassalTrade(TeamTypes eMasterTeam) const;

	int AI_surrenderTradeVal(TeamTypes eTeam) const;
	DenialTypes AI_surrenderTrade(TeamTypes eTeam, int iPowerMultiplier = 100,
			bool bCheckAccept = true) const; // advc.104o
	/*  advc.104o: Previously a magic number in CvPlayer::getTradeDenial; needed
		in additional places now. */
	static int const VASSAL_POWER_MOD_SURRENDER = 140;

	int AI_getLowestVictoryCountdown() const;

	int AI_countMembersWithStrategy(AIStrategy eStrategy) const; // K-Mod
	// bbai start  // advc.enum: Renamed the victory strategy functions
	bool AI_anyMemberAtVictoryStage(AIVictoryStage eStage) const;
	bool AI_anyMemberAtVictoryStage4() const;
	bool AI_anyMemberAtVictoryStage3() const;

	int AI_getWarSuccessRating() const; // K-Mod
	int AI_getEnemyPowerPercent(bool bConsiderOthers = false) const;
	bool AI_isPushover(TeamTypes ePotentialEnemy) const; // advc.105
	int AI_getAirPower() const; // K-Mod
	int AI_getRivalAirPower() const;
	// K-Mod. (refuse peace when we need war for conquest victory.)
	bool AI_refusePeace(TeamTypes ePeaceTeam) const;
	// K-Mod. (is war an acceptable side effect for event choices, vassal deals, etc)
	bool AI_refuseWar(TeamTypes eWarTeam) const;
	bool AI_acceptSurrender(TeamTypes eSurrenderTeam) const;
	bool AI_isOkayVassalTarget(TeamTypes eTeam) const;

	void AI_getWarRands(int &iMaxWarRand, int &iLimitedWarRand, int &iDogpileWarRand) const;
	void AI_getWarThresholds(int &iMaxWarThreshold, int &iLimitedWarThreshold, int &iDogpileWarThreshold) const;
	int AI_getTotalWarOddsTimes100() const;
	// bbai end
	// <advc.115b> <advc.104>
	VoteSourceTypes AI_getLatestVictoryVoteSource() const;
	int AI_countVSNonMembers(VoteSourceTypes eVS) const; // </advc.104>
	bool AI_isAnyCloseToReligiousVictory() const;
	int AI_votesToGoForVictory(int* piVoteTarget = NULL, bool bForceSecular = false) const;
	// </advc.115b>

	int AI_makePeaceTradeVal(TeamTypes ePeaceTeam, TeamTypes eTeam) const;
	DenialTypes AI_makePeaceTrade(TeamTypes ePeaceTeam, TeamTypes eBroker) const;

	int AI_declareWarTradeVal(TeamTypes eTarget, TeamTypes eSponsor) const;
	DenialTypes AI_declareWarTrade(TeamTypes eTarget, TeamTypes eSponsor, bool bConsiderPower = true) const;

	int AI_openBordersTradeVal(TeamTypes eTeam) const;
	DenialTypes AI_openBordersTrade(TeamTypes eWithTeam) const;

	int AI_defensivePactTradeVal(TeamTypes eTeam) const;
	DenialTypes AI_defensivePactTrade(TeamTypes eWithsTeam) const;

	DenialTypes AI_permanentAllianceTrade(TeamTypes eWithTeam) const;

	int AI_roundTradeVal(int iVal) const; // advc.104k
	void AI_makeUnwillingToTalk(TeamTypes eOther); // advc.104i
	// <advc.130y>
	void AI_forgiveEnemy(TeamTypes eEnemyTeam, bool bCapitulated, bool bFreed);
	void AI_thankLiberator(TeamTypes eLiberator);
	// </advc.130y>
	TeamTypes AI_getWorstEnemy() const { return m_eWorstEnemy; }
	void AI_updateWorstEnemy(/* advc.130p: */ bool bUpdateTradeMemory = true);
	// <advc.130p>
	scaled AI_enemyTradeResentmentFactor(TeamTypes eTo, TeamTypes eFrom,
			TeamTypes eWarTradeTarget = NO_TEAM, TeamTypes ePeaceTradeTarget = NO_TEAM,
			bool bPeaceDeal = false) const;
	// 0 or less if eEnemy isn't an enemy at all
	int AI_enmityValue(TeamTypes eEnemy) const;
	scaled AI_getDiploDecay() const;
	scaled AI_recentlyMetMultiplier(TeamTypes eOther) const;
	// </advc.130p>
	// advc.130k: Public b/c CvPlayerAI needs it too
	int AI_randomCounterChange(int iUpperCap = -1, scaled rProb = scaled(1, 2)) const;
	int AI_getWarPlanStateCounter(TeamTypes eIndex) const
	{
		return m_aiWarPlanStateCounter.get(eIndex);
	}
	void AI_setWarPlanStateCounter(TeamTypes eIndex, int iNewValue);
	void AI_changeWarPlanStateCounter(TeamTypes eIndex, int iChange);

	int AI_getAtWarCounter(TeamTypes eIndex) const											// Exposed to Python
	{
		return m_aiAtWarCounter.get(eIndex);
	}
	void AI_setAtWarCounter(TeamTypes eIndex, int iNewValue);
	void AI_changeAtWarCounter(TeamTypes eIndex, int iChange);

	int AI_getAtPeaceCounter(TeamTypes eIndex) const
	{
		return m_aiAtPeaceCounter.get(eIndex);
	}
	void AI_setAtPeaceCounter(TeamTypes eIndex, int iNewValue);
	void AI_changeAtPeaceCounter(TeamTypes eIndex, int iChange);

	int AI_getHasMetCounter(TeamTypes eIndex) const
	{
		return m_aiHasMetCounter.get(eIndex);
	}
	void AI_setHasMetCounter(TeamTypes eIndex, int iNewValue);
	void AI_changeHasMetCounter(TeamTypes eIndex, int iChange);

	int AI_getOpenBordersCounter(TeamTypes eIndex) const
	{
		return m_aiOpenBordersCounter.get(eIndex);
	}
	void AI_setOpenBordersCounter(TeamTypes eIndex, int iNewValue);
	void AI_changeOpenBordersCounter(TeamTypes eIndex, int iChange);

	int AI_getDefensivePactCounter(TeamTypes eIndex) const
	{
		return m_aiDefensivePactCounter.get(eIndex);
	}
	void AI_setDefensivePactCounter(TeamTypes eIndex, int iNewValue);
	void AI_changeDefensivePactCounter(TeamTypes eIndex, int iChange);

	int AI_getShareWarCounter(TeamTypes eIndex) const
	{
		return m_aiShareWarCounter.get(eIndex);
	}
	void AI_setShareWarCounter(TeamTypes eIndex, int iNewValue);
	void AI_changeShareWarCounter(TeamTypes eIndex, int iChange);

	// advc.130r: Use scaled for increased precision
	scaled AI_getWarSuccess(TeamTypes eIndex) const											// Exposed to Python
	{
		return m_arWarSuccess.get(eIndex);
	}
	void AI_setWarSuccess(TeamTypes eTeam, scaled rNewValue);
	void AI_changeWarSuccess(TeamTypes eITeam, scaled rChange);
	scaled AI_countEnemyWarSuccess() const; // advc
	// <advc.130m>
	void AI_reportSharedWarSuccess(scaled rIntensity, TeamTypes eWarAlly,
			TeamTypes eEnemy, bool bIgnoreDistress = false);
	/*  The war success of our war ally against a shared enemy, plus the war success
		of shared enemies against our war ally. This is quite different from AI_getWarSuccess,
		which counts our success against team eIndex. Also on a different scale. */
	int AI_getSharedWarSuccess(TeamTypes eWarAlly) const
	{
		return m_aiSharedWarSuccess.get(eWarAlly);
	}
	void AI_setSharedWarSuccess(TeamTypes eWarAlly, int iWS); // </advc.130m>
	int AI_getEnemyPeacetimeTradeValue(TeamTypes eIndex) const
	{
		return m_aiEnemyPeacetimeTradeValue.get(eIndex);
	}
	void AI_setEnemyPeacetimeTradeValue(TeamTypes eIndex, int iNewValue,
			bool bUpdateAttitude = true); // advc.130p
	void AI_changeEnemyPeacetimeTradeValue(TeamTypes eIndex, int iChange,
			bool bUpdateAttitude = true); // advc.130p
	int AI_getEnemyPeacetimeGrantValue(TeamTypes eIndex) const
	{
		return m_aiEnemyPeacetimeGrantValue.get(eIndex);
	}
	void AI_setEnemyPeacetimeGrantValue(TeamTypes eIndex, int iNewValue,
			bool bUpdateAttitude = true); // advc.130p
	void AI_changeEnemyPeacetimeGrantValue(TeamTypes eIndex, int iChange,
			bool bUpdateAttitude = true); // advc.130p

	// advc: countEnemy... functions moved from CvTeam
	int AI_countEnemyPowerByArea(CvArea const& kArea) const;												// Exposed to Python
	int AI_countEnemyCitiesByArea(CvArea const& kArea) const; // K-Mod
	int AI_countEnemyDangerByArea(CvArea const& kArea, TeamTypes eEnemyTeam = NO_TEAM) const; // bbai		// Exposed to Python
	int AI_countEnemyPopulationByArea(CvArea const& kArea) const; // bbai (advc: unused)
	WarPlanTypes AI_getWarPlan(TeamTypes eIndex) const
	{
		return m_aeWarPlan.get(eIndex);
	}
	bool AI_isChosenWar(TeamTypes eIndex) const;
	bool AI_isAnyChosenWar() const; // advc.105
	int AI_countChosenWars(bool bIgnoreMinors = true) const; // advc: Moved from CvTeam; unused.			// Exposed to Python
	// <advc> Replacing the deleted CvTeam::getWarPlanCount and getAnyWarPlanCount
	int AI_countWarPlans(WarPlanTypes eWarPlanType = NUM_WARPLAN_TYPES, bool bIgnoreMinors = true,			// Exposed to Python (through getWarPlanCount, getAnyWarPlanCount)
			unsigned int iMaxCount = MAX_PLAYERS) const; // </advc>
	// <advc.opt> Less flexible (ignores minors, vassals) but much faster
	int AI_getNumWarPlans(WarPlanTypes eWarPlanType) const
	{
		return m_aiWarPlanCounts.get(eWarPlanType);
	}
	bool AI_isAnyWarPlan() const { return m_bAnyWarPlan; } // </advc.opt>
	bool AI_isSneakAttackReady(TeamTypes eIndex /* K-Mod (any team): */ = NO_TEAM) const;
	bool AI_isSneakAttackPreparing(TeamTypes eIndex /* advc: */= NO_TEAM) const;
	void AI_setWarPlan(TeamTypes eTarget, WarPlanTypes eNewValue, bool bWar = true);
	// <advc.opt>
	bool AI_mayAttack(TeamTypes eDefender) const;
	bool AI_mayAttack(CvPlot const& kPlot) const; // </advc.opt>
	// BETTER_BTS_AI_MOD, 01/10/09, jdog5000: START  (advc: moved from CvTeam; const)
	bool AI_isMasterPlanningLandWar(CvArea const& kArea) const;
	bool AI_isMasterPlanningSeaWar(CvArea const& kArea) const;
	// BETTER_BTS_AI_MOD: END
	void AI_setWarPlanNoUpdate(TeamTypes eIndex, WarPlanTypes eNewValue);
	// <advc.650>
	void AI_rememberNukeExplosion(CvPlot const& kPlot);
	bool AI_wasRecentlyNuked(CvPlot const& kPlot) const; // </advc.650>
	// advc.158:
	AIStrengthMemoryMap& AI_strengthMemory() const { return m_strengthMemory; }
	// advc.104:
	int AI_teamCloseness(TeamTypes eIndex,
			int iMaxDistance = DEFAULT_PLAYER_CLOSENESS,
			bool bConsiderLandTarget = false, // advc.104o
			bool bConstCache = false) const; // advc.001n

	// <advc.104>
	UWAI::Team& uwai() { return *m_pUWAI; }
	UWAI::Team const& uwai() const { return *m_pUWAI; }
	int AI_refuseToTalkWarThreshold() const;
	// These 9 were protected </advc.104>
	int AI_maxWarRand() const;
	int AI_maxWarNearbyPowerRatio() const;
	int AI_maxWarDistantPowerRatio() const;
	int AI_maxWarMinAdjacentLandPercent() const;
	int AI_limitedWarRand() const;
	int AI_limitedWarPowerRatio() const;
	int AI_dogpileWarRand() const;
	int AI_makePeaceRand() const;
	int AI_noWarAttitudeProb(AttitudeTypes eAttitude) const;
	// <advc.104y>
	int AI_noWarProbAdjusted(TeamTypes eOther) const;
	bool AI_isAvoidWar(TeamTypes eOther, bool bPersonalityKnown = false) const;
	// </advc.104y>
	bool AI_performNoWarRolls(TeamTypes eTeam);
	// advc.012:
	int AI_plotDefense(CvPlot const& kPlot, bool bIgnoreBuilding = false,
			bool bGarrisonStrength = false) const; // advc.500b
	// advc.104, advc.651:
	bool AI_isExpectingToTrain(PlayerTypes eTrainPlayer, UnitTypes eUnit) const;

	int AI_getAttitudeWeight(TeamTypes eTeam) const;
	int AI_getTechMonopolyValue(TechTypes eTech, TeamTypes eTeam) const;
	bool AI_isWaterAreaRelevant(CvArea const& kArea) /* advc: */ const;
	void AI_finalizeInit(); // advc.opt

	void read(FDataStreamBase* pStream);
	void write(FDataStreamBase* pStream);

protected:
	TeamTypes m_eWorstEnemy;
	/*	<advc.enum> (See comment in CvPlayer header about lazy allocation.)
		(Could exclude Barbarians from diplo counters and
		use CivTeamMaps, but I don't think it's worth the effort.) */
	ArrayEnumMap<TeamTypes,int,short> m_aiWarPlanStateCounter;
	ArrayEnumMap<TeamTypes,int,short> m_aiAtWarCounter;
	ArrayEnumMap<TeamTypes,int,short> m_aiAtPeaceCounter;
	ArrayEnumMap<TeamTypes,int,short> m_aiHasMetCounter;
	ArrayEnumMap<TeamTypes,int,short> m_aiOpenBordersCounter;
	ArrayEnumMap<TeamTypes,int,short> m_aiDefensivePactCounter;
	ArrayEnumMap<TeamTypes,int,short> m_aiShareWarCounter;
	ArrayEnumMap<TeamTypes,scaled> m_arWarSuccess; // advc.130r: was V=int
	ArrayEnumMap<TeamTypes,int> m_aiSharedWarSuccess; // advc.130m
	ArrayEnumMap<TeamTypes,int> m_aiEnemyPeacetimeTradeValue;
	ArrayEnumMap<TeamTypes,int> m_aiEnemyPeacetimeGrantValue;
	ArrayEnumMap<WarPlanTypes,int,char> m_aiWarPlanCounts; // advc.opt
	ArrayEnumMap<TeamTypes,WarPlanTypes> m_aeWarPlan;
	// </advc.enum>
	bool m_bAnyWarPlan; // advc.opt
	bool m_bLonely; // advc.109

	std::vector<PlotNumTypes> m_aeNukeExplosions; // advc.650
	mutable AIStrengthMemoryMap m_strengthMemory; // advc.158
	UWAI::Team* m_pUWAI; // advc.104

	int AI_noTechTradeThreshold() const;
	int AI_techTradeKnownPercent() const;

	void AI_doCounter();
	void AI_doWar();
	// K-Mod
	int AI_warSpoilsValue(TeamTypes eTarget, WarPlanTypes eWarPlan,
			bool bConstCache) const; // advc.001n
	int AI_warCommitmentCost(TeamTypes eTarget, WarPlanTypes eWarPlan,
			bool bConstCache) const; // advc.001n
	// advc:
	bool isFutureWarEnemy(TeamTypes eTeam, TeamTypes eTarget, bool bDefensivePacts) const;
	int AI_warDiplomacyCost(TeamTypes eTarget) const;
	// K-Mod end

	// advc: Chunk of code that occured twice in doWar
	void AI_abandonWarPlanIfTimedOut(int iAbandonTimeModifier, TeamTypes eTarget,
			bool bLimited, int iEnemyPowerPercent);
	// advc.opt:
	void AI_updateWarPlanCounts(TeamTypes eTarget, WarPlanTypes eOldPlan, WarPlanTypes eNewPlan);
	// advc.104o:
	int AI_declareWarTradeValLegacy(TeamTypes eWarTeam, TeamTypes eTeam) const;
	int AI_getOpenBordersAttitudeDivisor() const; // advc.130i
	scaled AI_getOpenBordersCounterIncrement(TeamTypes eOther) const; // advc.130z
	bool AI_isTerritoryAccessible(TeamTypes eOwner) const; // advc.124
	bool AI_isTerritoryAccessible(CvPlot const& kPlot) const; // advc.124
	bool AI_isPursuingCircumnavigation() const; // advc.136a
	TeamTypes AI_diploVoteCounterCandidate(VoteSourceTypes eVS) const; // advc.115b

	friend class CvTeam; // advc.003u: So that protected functions can be called through CvTeam::AI
	// added so under cheat mode we can call protected functions for testing
	friend class CvGameTextMgr;
	friend class CvDLLWidgetData;
};

#endif
