#pragma once

#ifndef CIV4_PLAYER_AI_H
#define CIV4_PLAYER_AI_H

#include "CvPlayer.h"
#include "UWAI.h" // advc.104
#include "AIStrategies.h" // advc.enum

class CvDeal;
class CvCityAI;
class CvUnitAI;
class CvSelectionGroupAI;
class UWAICity; // advc.104d

/*	<advc.003u> Overwrite definition in CvPlayer.h (should perhaps instead define a
	new macro "PLAYERAI" - a lot of call locations to change though ...) */
#undef GET_PLAYER
#define GET_PLAYER(x) CvPlayerAI::AI_getPlayer(x)
// </advc.003u>

class CvPlayerAI : public CvPlayer
{
public:

#ifdef _DEBUG
	__forceinline // Annoying to step into by accident
#endif
	// advc.003u: Renamed from getPlayer
	static CvPlayerAI& AI_getPlayer(PlayerTypes ePlayer)
	{
		FAssertBounds(0, MAX_PLAYERS, ePlayer);
		return *m_aPlayers[ePlayer];
	}
	// Only for the EXE:
	DllExport static CvPlayerAI& getPlayerNonInl(PlayerTypes ePlayer);
	DllExport static bool areStaticsInitialized();
	static void AI_updateAttitudes(); // advc
	// <advc> Moved from CvDefines
	static int const DANGER_RANGE = 4;
	static int const BORDER_DANGER_RANGE = 2; // </advc>

	explicit CvPlayerAI(PlayerTypes eID);
	~CvPlayerAI();
	void AI_init();
	void AI_uninit();
	void AI_reset(bool bConstructor);
	void AI_updatePersonality(); // advc.104

	// <advc.003u> Access to AI-type members. Code mostly duplicated from CvPlayer.
	CvCityAI* AI_getCapital() const {
		return AI_getCity(m_iCapitalCityID);
	}
	CvCityAI* AI_firstCity(int *pIterIdx) const {
		return m_cities.AI_beginIter(pIterIdx);
	}
	CvCityAI* AI_nextCity(int *pIterIdx) const {
		return m_cities.AI_nextIter(pIterIdx);
	}
	CvCityAI* AI_getCity(int iID) const {
		return m_cities.AI_getAt(iID);
	}
	CvUnitAI* AI_firstUnit(int *pIterIdx) const {
		return m_units.AI_beginIter(pIterIdx);
	}
	CvUnitAI* AI_nextUnit(int *pIterIdx) const {
		return m_units.AI_nextIter(pIterIdx);
	}
	CvUnitAI* AI_getUnit(int iID) const {
		return m_units.AI_getAt(iID);
	}
	CvSelectionGroupAI* AI_firstSelectionGroup(int *pIterIdx) const {
		return m_selectionGroups.AI_beginIter(pIterIdx);
	}
	CvSelectionGroupAI* AI_nextSelectionGroup(int *pIterIdx) const {
		return m_selectionGroups.AI_nextIter(pIterIdx);
	}
	CvSelectionGroupAI* AI_getSelectionGroup(int iID) const {
		return m_selectionGroups.AI_getAt(iID);
	}
	// </advc.003u>
	int AI_getFlavorValue(FlavorTypes eFlavor) const;

	void AI_doTurnPre();
	void AI_doTurnPost();
	void AI_doTurnUnitsPre();
	void AI_doTurnUnitsPost();

	void AI_doPeace();
	// advc.134a:
	bool AI_upholdPeaceOffer(PlayerTypes eHuman, CvDiploParameters const& kOffer) const;

	void AI_updateFoundValues(bool bStarting = false);
	void AI_updateAreaTargets();

	int AI_movementPriority(CvSelectionGroupAI const& kGroup) const;
	void AI_unitUpdate();

	void AI_makeAssignWorkDirty();
	void AI_assignWorkingPlots();
	void AI_updateAssignWork();

	void AI_makeProductionDirty();
	#if 0 // advc
	void AI_doCentralizedProduction(); // K-Mod. (not used)
	#endif
	void AI_conquerCity(CvCityAI& kCity, /* advc.ctr: */ bool bEverOwned = false);
	scaled AI_razeMemoryScore(CvCity const& kCity) const; // advc.130q
	bool AI_acceptUnit(CvUnit const& kUnit) const;
	bool AI_captureUnit(UnitTypes eUnit, CvPlot const& kPlot) const;

	DomainTypes AI_unitAIDomainType(UnitAITypes eUnitAI) const;

	int AI_yieldWeight(YieldTypes eYield, CvCity const* pCity = 0) const; // K-Mod added city argument
	int AI_commerceWeight(CommerceTypes eCommerce, CvCityAI const* pCity = NULL) const;
	void AI_updateCommerceWeights(); // K-Mod

	// <advc.035>
	bool AI_isPlotContestedByRival(CvPlot const& kPlot,
			PlayerTypes eRival = NO_PLAYER) const; // </advc.035>
	short AI_foundValue(int iX, int iY, int iMinRivalRange = -1, bool bStartingLoc = false,			// Exposed to Python
			bool bNormalize = false) const; // advc.031e
	// advc: Replaced by the CitySiteEvaluator class
	//struct CvFoundSettings { ... } // K-Mod
	//short AI_foundValue_bulk(int iX, int iY, const CvFoundSettings& kSet) const; // K-Mod
	//int AI_countDeadlockedBonuses(CvPlot const* pPlot) const;
	// Obsoleted by K-Mod:
	/*int AI_getOurPlotStrength(CvPlot* pPlot, int iRange, bool bDefensiveBonuses, bool bTestMoves) const;
	int AI_getEnemyPlotStrength(CvPlot* pPlot, int iRange, bool bDefensiveBonuses, bool bTestMoves) const;*/ // BtS
	bool AI_isEasyCulture(bool* pbFromTrait = NULL) const; // advc

	bool AI_isAreaAlone(CvArea const& kArea) const;
	bool AI_isCapitalAreaAlone() const;
	bool AI_isPrimaryArea(CvArea const& kArea) const;
	int AI_militaryWeight(CvArea const* pArea = NULL) const;
	bool AI_feelsSafe() const; // advc.109

	int AI_targetCityValue(CvCity const& kCity, bool bRandomize,
			bool bIgnoreAttackers = false,
			UWAICity const* pUWAICity = NULL) const; // advc.104d
	CvCityAI* AI_findTargetCity(CvArea const& kArea) const;
	int AI_cityWonderVal(CvCity const& c) const; // advc.104d
	scaled AI_assetVal(CvCityAI const& c, bool bConquest) const; // advc

	// BETTER_BTS_AI_MOD, 08/20/09, jdog5000: START
	bool isSafeRangeCacheValid() const; // K-Mod
	int AI_getPlotDanger(CvPlot const& kPlot, int iRange = -1, bool bTestMoves = true,
			int iLimit = MAX_INT, // advc  <advc.104>
			bool bCheckBorder = true, PlayerTypes eAttackPlayer = NO_PLAYER) const;
			// </advc.104>
	bool AI_isAnyPlotDanger(CvPlot const& kPlot, int iRange = -1, bool bTestMoves = true,
		bool bCheckBorder = true) const // K-Mod
	{	// advc: Merged with the plot danger counting function
		return (AI_getPlotDanger(kPlot, iRange, bTestMoves, 1, bCheckBorder) > 0);
	}
	//int AI_getUnitDanger(CvUnit* pUnit, int iRange = -1, bool bTestMoves = true, bool bAnyDanger = true) const;
	// BETTER_BTS_AI_MOD: END
	int AI_getWaterDanger(CvPlot const& kPlot, int iRange = DANGER_RANGE,
			/* <advc.opt> */ int iMaxCount = MAX_INT) const;
	bool AI_isAnyWaterDanger(CvPlot const& kPlot, int iRange = DANGER_RANGE) const
	{
		return (AI_getWaterDanger(kPlot, iRange, 1) >= 1);
	} // </advc.opt>

	bool AI_avoidScience() const;
	int AI_financialTroubleMargin() const; // advc.110
	bool AI_isFinancialTrouble() const;							// Exposed to Python
	//int AI_goldTarget() const;
	int AI_goldTarget(bool bUpgradeBudgetOnly = false) const; // K-Mod

	TechTypes AI_bestTech(int iMaxPathLength = 1, bool bFreeTech = false, bool bAsync = false,
			TechTypes eIgnoreTech = NO_TECH, AdvisorTypes eIgnoreAdvisor = NO_ADVISOR,
			PlayerTypes eFromPlayer = NO_PLAYER) const; // advc.144
	scaled AI_getTechRank(TechTypes eTech) const; // advc.550g
	// advc:
	void AI_calculateTechRevealBonuses(
			EagerEnumMap<BonusClassTypes,int>& kBonusClassRevealed,
			EagerEnumMap<BonusClassTypes,int>& viBonusClassUnrevealed,
			EagerEnumMap<BonusClassTypes,int>& viBonusClassHave) const;
	// BETTER_BTS_AI_MOD, Tech AI, 03/18/10, jdog5000: START
	int AI_techValue(TechTypes eTech, int iPathLength, bool bFreeTech, bool bAsync,
			EagerEnumMap<BonusClassTypes,int> const& kBonusClassRevealed,
			EagerEnumMap<BonusClassTypes,int> const& viBonusClassUnrevealed,
			EagerEnumMap<BonusClassTypes,int> const& viBonusClassHave,
			PlayerTypes eFromPlayer = NO_PLAYER, // advc.144
			bool bRandomize = true) const; // advc
	int AI_obsoleteBuildingPenalty(TechTypes eTech, bool bConstCache) const; // K-Mod
	int AI_techBuildingValue(TechTypes eTech, bool bConstCache, bool& bEnablesWonder) const;
	int AI_techUnitValue(TechTypes eTech, int iPathLength, bool &bEnablesUnitWonder) const;
	// BETTER_BTS_AI_MOD: END
	// k146:
	int AI_techProjectValue(TechTypes eTech, int iPathLength, bool &bEnablesProjectWonder) const;
	// <advc>
	int AI_techReligionValue(TechTypes eTech, int iPathLength,
			int iRaceModifier, int iCityTarget,
			CvRandom& kRand, int& iRandomMax, bool bRandomize) const; // </advc>
	int AI_cultureVictoryTechValue(TechTypes eTech) const;

	void AI_chooseFreeTech(/* advc.121: */ bool bEndOfTurn = false);
	void AI_chooseResearch();

	DllExport DiploCommentTypes AI_getGreeting(PlayerTypes ePlayer) const;
	bool AI_isWillingToTalk(PlayerTypes ePlayer,
			bool bAsync = false) const; // advc.104l
	int AI_refuseToTalkTurns(PlayerTypes ePlayer) const; // advc.104i
	bool AI_demandRebukedSneak(PlayerTypes ePlayer) const;
	bool AI_demandRebukedWar(PlayerTypes ePlayer) const;
	bool AI_hasTradedWithTeam(TeamTypes eTeam) const;

	void AI_updateAttitude(); // K-Mod (toward all other players)
	void AI_updateAttitude(PlayerTypes ePlayer,		// K-Mod
			bool bUpdateWorstEnemy = true); // advc.130e
	void AI_changeCachedAttitude(PlayerTypes ePlayer, int iChange); // K-Mod
	AttitudeTypes AI_getAttitude(PlayerTypes ePlayer, bool bForced = true) const		// Exposed to Python
	{
		FAssert(ePlayer != getID());
		return (AI_getAttitudeFromValue(AI_getAttitudeVal(ePlayer, bForced)));
	}
	int AI_getAttitudeVal(PlayerTypes ePlayer, bool bForced = true) const;
	static AttitudeTypes AI_getAttitudeFromValue(int iAttitudeVal);
	void AI_updateExpansionistHate(); // advc.130w

	int AI_calculateStolenCityRadiusPlots(PlayerTypes ePlayer,
			bool bOnlyNonWorkable = false) const; // advc.147
	void AI_updateCloseBorderAttitude(); // K-Mod
	void AI_updateCloseBorderAttitude(PlayerTypes ePlayer); // K-Mod
	int AI_getCloseBordersAttitude(PlayerTypes ePlayer) const;
	int warSuccessAttitudeDivisor() const; // advc.130y, advc.sha
	int AI_getWarAttitude(PlayerTypes ePlayer,
			int iPartialSum = MIN_INT) const; // advc.sha
	int AI_getPeaceAttitude(PlayerTypes ePlayer) const;
	int AI_getSameReligionAttitude(PlayerTypes ePlayer) const;
	int AI_getDifferentReligionAttitude(PlayerTypes ePlayer) const;
	int AI_getBonusTradeAttitude(PlayerTypes ePlayer) const;
	int AI_getOpenBordersAttitude(PlayerTypes ePlayer) const;
	int AI_getDefensivePactAttitude(PlayerTypes ePlayer) const;
	int AI_getRivalDefensivePactAttitude(PlayerTypes ePlayer) const;
	int AI_getRivalVassalAttitude(PlayerTypes ePlayer) const;
	int AI_getShareWarAttitude(PlayerTypes ePlayer) const;
	int AI_getFavoriteCivicAttitude(PlayerTypes ePlayer) const;
	int AI_getTradeAttitude(PlayerTypes ePlayer) const;
	int AI_getRivalTradeAttitude(PlayerTypes ePlayer) const;
	int AI_getBonusTradeCounter(TeamTypes eTo) const; // advc.130p
	int AI_getMemoryAttitude(PlayerTypes ePlayer, MemoryTypes eMemory) const;
	//int AI_getColonyAttitude(PlayerTypes ePlayer) const; // advc.130r
	// BEGIN: Show Hidden Attitude Mod 01/22/2010
	int AI_getFirstImpressionAttitude(PlayerTypes ePlayer) const;
	int AI_getTeamSizeAttitude(PlayerTypes ePlayer) const;
	// advc.sha: One function for both BetterRank and WorseRank
	int AI_getRankDifferenceAttitude(PlayerTypes ePlayer) const;
	/*int AI_getLowRankAttitude(PlayerTypes ePlayer) const;
	int AI_getLostWarAttitude(PlayerTypes ePlayer) const;
	int AI_getKnownPlayerRank(PlayerTypes ePlayer) const;*/ // advc.sha
	// END: Show Hidden Attitude Mod
	int AI_getExpansionistAttitude(PlayerTypes ePlayer) const; // advc.130w
	void AI_updateIdeologyAttitude(int iChange, CvCity const& kCity); // advc.130n

	PlayerVoteTypes AI_diploVote(const VoteSelectionSubData& kVoteData, VoteSourceTypes eVoteSource, bool bPropose);

	int AI_dealVal(PlayerTypes eFromPlayer, CLinkList<TradeData> const& kList,
			bool bIgnoreAnnual = false,
			int iChange = 1, /* advc: was called iExtra, which didn't make sense
								and differed from the parameter name in CvPlayerAI.cpp. */
			bool bIgnoreDiscount = false, // advc.550a
			bool bIgnorePeace = false, // advc.130p  <advc.ctr>
			bool bCountLiberation = false, bool bAIRequest = false,
			bool bDiploVal = false) const; // </advc.ctr>
	//bool AI_goldDeal(CLinkList<TradeData> const* pList) const; // advc: See goldDeal in implementation file
	bool AI_considerOffer(PlayerTypes ePlayer, CLinkList<TradeData> const& kTheyGive,
			CLinkList<TradeData> const& kWeGive, int iChange = 1, /* advc.133: */ int iDealAge = 0,
			// <advc.130o> May change diplo memory if true; const qualifier removed.
			bool bHypothetical = false);
	// const wrapper
	bool AI_considerHypotheticalOffer(PlayerTypes ePlayer, CLinkList<TradeData> const& kTheyGive,
			CLinkList<TradeData> const& kWeGive, int iChange = 1, /* advc.133: */ int iDealAge = 0) const
	{
		return const_cast<CvPlayerAI*>(this)->AI_considerOffer(ePlayer, kTheyGive, kWeGive, iChange, iDealAge, true);
	} // </advc.130o>
	scaled AI_prDenyHelp() const; // advc.144
	int AI_tradeAcceptabilityThreshold(PlayerTypes eTrader) const; // K-Mod
	int AI_maxGoldTrade(PlayerTypes ePlayer, /* advc.134a: */ bool bTeamTrade = false) const;
	int AI_maxGoldPerTurnTrade(PlayerTypes ePlayer,										// Exposed to Python
			bool bCheckOverdraft = false) const; // advc.133
	int AI_goldPerTurnTradeVal(int iGoldPerTurn) const;
	int AI_bonusVal(BonusTypes eBonus, int iChange,
			bool bAssumeEnabled = false, // K-Mod
			// advc.036: Whether baseBonusVal is computed for a resource trade
			bool bTrade = false) const;
	int AI_baseBonusVal(BonusTypes eBonus, /* advc.036: */ bool bTrade = false) const;
	int AI_bonusTradeVal(BonusTypes eBonus, PlayerTypes eFromPlayer, int iChange,
			bool bExtraHappyOrHealth = false) const; // advc.036
	DenialTypes AI_bonusTrade(BonusTypes eBonus, PlayerTypes eToPlayer,
			int iChange = 0) const; // advc.133
	// advc.210e: Exposed to Python
	int AI_corporationBonusVal(BonusTypes eBonus, /* advc.036: */ bool bTrade = false) const;
	int AI_goldForBonus(BonusTypes eBonus, PlayerTypes eBonusOwner) const; // advc.036
	// <advc.ctr>
    int AI_bonusEffectVal(BonusTypes eBonus, int iChange) const; // doc
    int AI_bonusHappinessChange(BonusTypes eBonus, int iChange) const; // doc
    int AI_bonusHealthChange(BonusTypes eBonus, int iChange) const; // doc
    int AI_bonusBuildingHappinessChange(BonusTypes eBonus, int iChange) const; // doc
    int AI_bonusBuildingHealthChange(BonusTypes eBonus, int iChange) const; // doc
    int AI_bonusAffectedCitiesChange(BonusTypes eBonus, int iChange) const; // doc
    int AI_bonusActualHappinessChange(BonusTypes eBonus, int iChange) const; // doc
    int AI_bonusActualHealthChange(BonusTypes eBonus, int iChange) const; // doc
	enum LiberationWeightTypes
	{
		LIBERATION_WEIGHT_ZERO, // 0 trade value when eToPlayer is the liberation player
		LIBERATION_WEIGHT_REDUCED,
		LIBERATION_WEIGHT_FULL
	}; // </advc.ctr>
	int AI_cityTradeVal(CvCityAI const& kCity,  // <advc.ctr>
			PlayerTypes eToPlayer = NO_PLAYER,
			// (The function will ignore this in some situations)
			LiberationWeightTypes eLibWeight = LIBERATION_WEIGHT_ZERO,
			bool bConquest = false, bool bAIRequest = false,
			bool bDiploVal = false) const; // </advc.ctr>
	DenialTypes AI_cityTrade(CvCityAI const& kCity, PlayerTypes ePlayer) const;

	int AI_stopTradingTradeVal(TeamTypes eTradeTeam, PlayerTypes ePlayer,
			bool bWarTrade = false) const; // advc.104o
	DenialTypes AI_stopTradingTrade(TeamTypes eTradeTeam, PlayerTypes ePlayer) const;

	int AI_civicTradeVal(CivicTypes eCivic, PlayerTypes ePlayer) const;
	DenialTypes AI_civicTrade(CivicTypes eCivic, PlayerTypes ePlayer) const;

	int AI_religionTradeVal(ReligionTypes eReligion, PlayerTypes ePlayer) const;
	DenialTypes AI_religionTrade(ReligionTypes eReligion, PlayerTypes ePlayer) const;

	uint AI_unitImpassables(UnitTypes eUnit) const;
	// advc.057:
	bool AI_isAnyImpassable(UnitTypes eUnit) const
	{
		/*	BBAI note [moved from some call location]: For galleys, triremes, ironclads ...
			unit types which are limited in what terrain they can operate in. */
		return (AI_unitImpassables(eUnit) != 0u);
	}

	int AI_unitValue(UnitTypes eUnit, UnitAITypes eUnitAI, CvArea const* pArea = NULL) const;			// Exposed to Python
	int AI_totalUnitAIs(UnitAITypes eUnitAI) const;														// Exposed to Python
	int AI_totalAreaUnitAIs(CvArea const& kArea, UnitAITypes eUnitAI) const;							// Exposed to Python
	int AI_totalWaterAreaUnitAIs(CvArea const& kArea, UnitAITypes eUnitAI) const;						// Exposed to Python
	// advc.081:
	int AI_totalWaterAreaUnitAIs(CvArea const& kArea, std::vector<UnitAITypes> const& aeUnitAI) const;
	int AI_countCargoSpace(UnitAITypes eUnitAI) const;

	int AI_neededExplorers(CvArea const& kArea) const;
	void AI_updateNeededExplorers(); // advc.opt
	// <advc.017b>
	bool AI_isExcessSeaExplorers(CvArea const& kWaterArea, int iChange = 0) const;
	bool AI_isOutdatedUnit(UnitTypes eUnit, UnitAITypes eRole, CvArea const* pArea = NULL) const;
	// </advc.017b>
	// <advc.042> Moved from CvPlayer and iLookAhead param added
	int AI_countUnimprovedBonuses(CvArea const& kArea,													// Exposed to Python
			CvPlot const* pFromPlot = NULL, int iLookAhead = 0) const;
	int AI_countOwnedBonuses(BonusTypes eBonus, // </advc.042>											// Exposed to Python
			/* <advc.opt> */ int iMaxCount = MAX_INT) const;
	int AI_countCityFeatures(FeatureTypes eFeature) const; // advc.042									// Exposed to Python
	bool AI_isAnyOwnedBonus(BonusTypes eBonus) const
	{
		return (AI_countOwnedBonuses(eBonus, 1) > 0);
	} // </advc.opt>
	int AI_neededWorkers(CvArea const& kArea) const;
	int AI_neededMissionaries(CvArea const& kArea, ReligionTypes eReligion) const;
	int AI_neededExecutives(CvArea const& kArea, CorporationTypes eCorporation) const;
	int AI_unitCostPerMil() const; // K-Mod
	int AI_maxUnitCostPerMil(CvArea const* pArea = NULL, int iBuildProb = -1) const; // K-Mod
	bool AI_isLandWar(CvArea const& kArea) const; // K-Mod
	bool AI_isFocusWar(CvArea const* pArea = NULL) const; // advc.105
	int AI_nukeWeight() const; // K-Mod
	int AI_nukeDangerDivisor() const; // kekm.16
	int AI_nukePlotValue(CvPlot const& kPlot, int iCivilianTargetWeight) const; // advc
	// <advc.650>
	int AI_nukeBaseDestructionWeight() const;
	int AI_nukeExtraDestructionWeight(PlayerTypes eTarget,
			int iTheirNukes, bool bLimited) const;
	int AI_estimateNukeCount(PlayerTypes eOwner) const;
	scaled AI_nukeChanceToKillUnit(int iHP, int iNukeModifier = 0) const; // </advc.650>

	int AI_missionaryValue(ReligionTypes eReligion, CvArea const* pArea = NULL/*, PlayerTypes* peBestPlayer = NULL*/) const;
	int AI_executiveValue(CorporationTypes eCorporation, CvArea const* pArea = NULL,
			PlayerTypes* peBestPlayer = NULL, bool bSpreadOnly = false) const;
	// advc.171:
	bool AI_isTargetForMissionaries(PlayerTypes eTarget, ReligionTypes eReligion) const;
	int AI_corporationValue(CorporationTypes eCorporation, CvCityAI const* pCity = NULL) const;
	void AI_processNewBuild(BuildTypes eBuild); // advc.121

	int AI_adjacentPotentialAttackers(CvPlot const& kPlot, bool bTestCanMove = false) const;
	//int AI_totalMissionAIs(MissionAITypes eMissionAI, CvSelectionGroup* pSkipSelectionGroup = NULL) const; // advc.003j
	int AI_areaMissionAIs(CvArea const& kArea, MissionAITypes eMissionAI,
			CvSelectionGroup* pSkipSelectionGroup = NULL, /* <advc.opt> */ int iMaxCount = MAX_INT) const;
	bool AI_isAnyAreaMissionAI(CvArea const& kArea, MissionAITypes eMissionAI,
		CvSelectionGroup* pSkipSelectionGroup = NULL) const
	{
		return (AI_areaMissionAIs(kArea, eMissionAI, pSkipSelectionGroup, 1) >= 1);
	} // </advc.opt>
	// advc: TargetMissionAI counting: const CvPlot&. advc.opt: iMaxCount params added.
	int AI_plotTargetMissionAIs(CvPlot const& kPlot, MissionAITypes eMissionAI,
		CvSelectionGroup const* pSkipSelectionGroup = NULL, int iRange = 0, int iMaxCount = MAX_INT) const
	{
		return AI_plotTargetMissionAIs(kPlot, &eMissionAI, 1, pSkipSelectionGroup,
				iRange, iMaxCount);
	}
	// advc: Unused (out-)param iClosestTargetRange removed
	int AI_plotTargetMissionAIs(CvPlot const& kPlot, MissionAITypes* aeMissionAI,
			int iMissionAICount, CvSelectionGroup const* pSkipSelectionGroup = NULL,
			int iRange = 0, int iMaxCount = MAX_INT) const;
	// <advc.opt>
	bool AI_isAnyPlotTargetMissionAI(CvPlot const& kPlot, MissionAITypes eMissionAI,
		CvSelectionGroup* pSkipSelectionGroup = NULL, int iRange = 0) const
	{
		return (AI_plotTargetMissionAIs(kPlot, eMissionAI, pSkipSelectionGroup, iRange, 1) >= 1);
	}
	bool AI_isAnyUnitTargetMissionAI(CvUnit const& kUnit, MissionAITypes eMissionAI,
		CvSelectionGroup* pSkipSelectionGroup = NULL) const
	{
		return (AI_unitTargetMissionAIs(kUnit, eMissionAI, pSkipSelectionGroup, 1) >= 1);
	}
	bool AI_isAnyUnitTargetMissionAI(CvUnit const& kUnit, MissionAITypes* aeMissionAI,
		int iMissionAICount, CvSelectionGroup* pSkipSelectionGroup = NULL,
		int iMaxPathTurns = -1) const
	{
		return (AI_unitTargetMissionAIs(kUnit, aeMissionAI, iMissionAICount,
				pSkipSelectionGroup, iMaxPathTurns, 1) >= 1);
	} // </advc.opt>
	int AI_unitTargetMissionAIs(CvUnit const& kUnit, MissionAITypes eMissionAI,
		CvSelectionGroup* pSkipSelectionGroup = NULL, int iMaxCount = MAX_INT) const
	{
		return AI_unitTargetMissionAIs(kUnit, &eMissionAI, 1, pSkipSelectionGroup,
				-1, iMaxCount);
	}
	int AI_unitTargetMissionAIs(CvUnit const& kUnit, MissionAITypes* aeMissionAI,
			int iMissionAICount, CvSelectionGroup* pSkipSelectionGroup = NULL,
			int iMaxPathTurns = -1, // BBAI (advc: merged into the BtS function)
			int iMaxCount = MAX_INT) const;
	// BBAI start
	int AI_enemyTargetMissions(TeamTypes eTargetTeam, CvSelectionGroup* pSkipSelectionGroup = NULL,
			// <advc.opt>
			int iMaxCount = MAX_INT) const; // BBAI end
	bool AI_isAnyEnemyTargetMission(TeamTypes eTargetTeam,
		CvSelectionGroup* pSkipSelectionGroup = NULL) const
	{
		return (AI_enemyTargetMissions(eTargetTeam, pSkipSelectionGroup, 1) >= 1);
	} // </advc.opt>
	// advc.003j: unused
	/*int AI_enemyTargetMissionAIs(MissionAITypes eMissionAI,
			CvSelectionGroup* pSkipSelectionGroup = NULL, int iMaxCount = MAX_INT) const;
	int AI_enemyTargetMissionAIs(MissionAITypes* aeMissionAI,
			int iMissionAICount, CvSelectionGroup* pSkipSelectionGroup = NULL, int iMaxCount = MAX_INT) const;*/
	int AI_wakePlotTargetMissionAIs(CvPlot const& kPlot, MissionAITypes eMissionAI,
			CvSelectionGroup* pSkipSelectionGroup = NULL) const;
	// K-Mod start
	int AI_localDefenceStrength(const CvPlot* pDefencePlot,
			TeamTypes eDefenceTeam = NO_TEAM, DomainTypes eDomainType = DOMAIN_LAND,
			int iRange = 0, bool bMoveToTarget = true, bool bCheckMoves = false, bool bNoCache = false,
			bool bPredictPromotions = false) const; // advc.139
	int AI_localAttackStrength(const CvPlot* pTargetPlot,
			TeamTypes eAttackTeam = NO_TEAM, DomainTypes eDomainType = DOMAIN_LAND,
			int iRange = 2, bool bUseTarget = true, bool bCheckMoves = false, bool bCheckCanAttack = false,
			int* piAttackerCount = NULL) const; // advc.139
	int AI_cityTargetStrengthByPath(CvCity const* pCity, CvSelectionGroup* pSkipSelectionGroup, int iMaxPathTurns) const;
	// K-Mod end
	// <advc.139>
	void AI_attackMadeAgainst(CvUnit const& kDefender);
	void AI_humanEnemyStackMovedInTerritory(CvPlot const& kFrom, CvPlot const& kTo);
	// </advc.139>  advc:
	int AI_neededCityAttackers(/* advc.104p: */ CvArea const& kArea,
			int iHash = -1) const;
	// <advc.300>
	scaled AI_neededCityAttackersVsBarbarians() const;
	int AI_estimateBarbarianGarrisonSize() const;
	scaled AI_barbarianTargetCityScore(CvArea const& kArea) const; // </advc.300>

	CivicTypes AI_bestCivic(CivicOptionTypes eCivicOption, int* iBestValue = 0) const;
	int AI_civicValue(CivicTypes eCivic) const;						// Exposed to Python

	ReligionTypes AI_bestReligion() const;
	int AI_religionValue(ReligionTypes eReligion) const;
	// K-Mod: moved to CvUnitAI
	//EspionageMissionTypes AI_bestPlotEspionage(CvPlot* pSpyPlot, PlayerTypes& eTargetPlayer, CvPlot*& pPlot, int& iData) const;
	int AI_espionageVal(PlayerTypes eTargetPlayer, EspionageMissionTypes eMission,
			CvPlot const& kPlot, int iData) const;
	bool AI_isMaliciousEspionageTarget(PlayerTypes eTarget) const; // K-Mod

	int AI_getPeaceWeight() const;
	void AI_setPeaceWeight(int iNewValue);

	int AI_getEspionageWeight() const;
	void AI_setEspionageWeight(int iNewValue);

	int AI_getAttackOddsChange() const;
	void AI_setAttackOddsChange(int iNewValue);

	int AI_getCivicTimer() const;
	void AI_setCivicTimer(int iNewValue);
	void AI_changeCivicTimer(int iChange);

	int AI_getReligionTimer() const;
	void AI_setReligionTimer(int iNewValue);
	void AI_changeReligionTimer(int iChange);

	int AI_getExtraGoldTarget() const;
	void AI_setExtraGoldTarget(int iNewValue);

	int AI_getNumTrainAIUnits(UnitAITypes eIndex) const;
	void AI_changeNumTrainAIUnits(UnitAITypes eIndex, int iChange);

	int AI_getNumAIUnits(UnitAITypes eIndex) const;							// Exposed to Python
	void AI_changeNumAIUnits(UnitAITypes eIndex, int iChange);

	int AI_getSameReligionCounter(PlayerTypes eIndex) const;
	void AI_changeSameReligionCounter(PlayerTypes eIndex, int iChange);

	int AI_getDifferentReligionCounter(PlayerTypes eIndex) const;
	void AI_changeDifferentReligionCounter(PlayerTypes eIndex, int iChange);

	int AI_getFavoriteCivicCounter(PlayerTypes eIndex) const;
	void AI_changeFavoriteCivicCounter(PlayerTypes eIndex, int iChange);

	int AI_getBonusTradeCounter(PlayerTypes eIndex) const;
	void AI_changeBonusTradeCounter(PlayerTypes eIndex, int iChange);
	/*	<advc.130p> For code shared by AI_processPeacetimeTradeValue and
		AI_processPeacetimeGrantValue. The third parameter says which of the two
		should be changed. */
	void AI_processPeacetimeValue(PlayerTypes eFromPlayer, int iChange,
			bool bGrant, bool bPeace = false, TeamTypes ePeaceTradeTarget = NO_TEAM,
			TeamTypes eWarTradeTarget = NO_TEAM, bool bUpdateAttitude = true);
	// </advc.130p>
	int AI_getPeacetimeTradeValue(PlayerTypes eIndex) const;
	// advc.130p: Renamed from changePeacetimeTradeValue
	void AI_processPeacetimeTradeValue(PlayerTypes eIndex, int iChange,
			bool bUpdateAttitude = true); // advc.130p
	int AI_getPeacetimeGrantValue(PlayerTypes eIndex) const;
	// advc.130p: Renamed from changePeacetimeTradeValue
	void AI_processPeacetimeGrantValue(PlayerTypes eIndex, int iChange,
			bool bUpdateAttitude = true); // advc.130p
	// <advc.130k> To make exponential decay more convenient
	void AI_setSameReligionCounter(PlayerTypes eIndex, int iValue);
	void AI_setDifferentReligionCounter(PlayerTypes eIndex, int iValue);
	void AI_setFavoriteCivicCounter(PlayerTypes eIndex, int iValue);
	void AI_setBonusTradeCounter(PlayerTypes eIndex, int iValue);
	// </advc.130k>
	int AI_getGoldTradedTo(PlayerTypes eIndex) const;
	void AI_changeGoldTradedTo(PlayerTypes eIndex, int iChange);

	int AI_getAttitudeExtra(PlayerTypes eIndex) const;							// Exposed to Python
	void AI_setAttitudeExtra(PlayerTypes eIndex, int iNewValue);				// Exposed to Python
	void AI_changeAttitudeExtra(PlayerTypes eIndex, int iChange);				// Exposed to Python

	bool AI_isFirstContact(PlayerTypes eIndex) const;
	void AI_setFirstContact(PlayerTypes eIndex, bool bNewValue);

	int AI_getContactTimer(PlayerTypes eIndex1, ContactTypes eIndex2) const;
	void AI_changeContactTimer(PlayerTypes eIndex1, ContactTypes eIndex2, int iChange);

	int AI_getMemoryCount(PlayerTypes eIndex1, MemoryTypes eIndex2) const;
	void AI_changeMemoryCount(PlayerTypes eIndex1, MemoryTypes eIndex2, int iChange);
	// advc: setter added
	void AI_setMemoryCount(PlayerTypes eAboutPlayer, MemoryTypes eMemoryType, int iValue);
	// advc.130j: Increases memory count according to (hardcoded) granularity
	void AI_rememberEvent(PlayerTypes ePlayer, MemoryTypes eMemoryType);
	void AI_rememberLiberation(CvCity const& kCity, bool bConquest); // advc.ctr
	// <advc.130p>
	bool AI_processTradeValue(CLinkList<TradeData> const& kItems,
			PlayerTypes eFromPlayer, bool bGift, bool bPeace,
			TeamTypes ePeaceTradeTarget = NO_TEAM,
			TeamTypes eWarTradeTarget = NO_TEAM, // </advc.130p>
			bool bAIRequest = false); // advc.ctr
	void AI_processRazeMemory(CvCity const& kCity); // advc.003n

	// K-Mod
	int AI_getCityTargetTimer() const;
	void AI_setCityTargetTimer(int iTurns);
	// K-Mod end

	int AI_calculateGoldenAgeValue(bool bConsiderRevolution = true) const;

	void AI_doCommerce();

	EventTypes AI_chooseEvent(int iTriggeredId) const;
	void AI_launch(VictoryTypes eVictory);

	int AI_calculateCultureVictoryStage(
			int iCountdownThresh = -1) const; // advc.115
	// BETTER_BTS_AI_MOD, Victory Strategy AI, 03/17/10, jdog5000: START
	/* (functions renamed and edited for K-Mod;
		advc: 'calculate' functions moved to protected section;
		advc.enum: Renamed to emphasize distinction between victory and non-victory strats) */
	bool AI_atVictoryStage(AIVictoryStage eStage) const;
	bool AI_atVictoryStage4() const;
	bool AI_atVictoryStage3() const;
	AIVictoryStage AI_getVictoryStageHash() const { return m_eVictoryStageHash; }
	// advc.115f:
	int AI_getVictoryWeight(VictoryTypes eVictory) const
	{
		return m_aiVictoryWeights.get(eVictory);
	}
	void AI_updateVictoryWeights(); // advc.115f
	void AI_updateVictoryStageHash(); // K-Mod
	void AI_initStrategyRand(); // K-Mod
	int AI_getStrategyRand(int iShift) const;
	// BETTER_BTS_AI_MOD: END
	bool isCloseToReligiousVictory() const;
	bool AI_isDoStrategy(AIStrategy eStrategy, /* advc.007: */ bool bDebug = false) const;
	// <advc.erai>
	void AI_updateEraFactor();
	/*	Call locations of this function and similar functions at CvTeamAI, CvGameAI
		aren't tagged with "advc.erai" comments. Note: Should not replace all uses of
		era numbers in AI code with these functions. For example, a mod with only
		3 eras won't necessarily have more techs per era than BtS. */
	scaled AI_getCurrEraFactor() const { return m_rCurrEraFactor; }
	int AI_getCurrEra() const { return AI_getCurrEraFactor().uround(); }
	// </advc.erai>

	void AI_updateGreatPersonWeights(); // K-Mod
	int AI_getGreatPersonWeight(UnitClassTypes eGreatPerson) const; // K-Mod

	void AI_nowHasTech(TechTypes eTech);

	//int AI_goldToUpgradeAllUnits(int iExpThreshold = 0) const;
	// K-Mod
	int AI_getGoldToUpgradeAllUnits() const { return m_iUpgradeUnitsCachedGold; }
	void AI_updateGoldToUpgradeAllUnits();
	int AI_getAvailableIncome() const { return m_iAvailableIncome; }
	void AI_updateAvailableIncome();
	int AI_estimateBreakEvenGoldPercent() const;
	// K-Mod end

	int AI_goldTradeValuePercent() const;

	int AI_averageYieldMultiplier(YieldTypes eYield) const;
	int AI_averageCommerceMultiplier(CommerceTypes eCommerce) const;
	int AI_averageGreatPeopleMultiplier() const;
	int AI_averageTradeMultiplier() const; // doc
	int AI_averageCulturePressure() const; // K-Mod
	int AI_averageCommerceExchange(CommerceTypes eCommerce) const;

	int AI_playerCloseness(PlayerTypes eIndex,
			int iMaxDistance /* advc: */ = DEFAULT_PLAYER_CLOSENESS,
			bool bConstCache = false) const; // advc.001n
	int AI_paranoiaRating(PlayerTypes eRival, int iOurDefPow, // advc
			// advc.104:
			bool bReduceWhenHopeless = true, bool bConstCache = false) const;

	int AI_getTotalCityThreat() const;
	int AI_getTotalFloatingDefenseNeeded() const;


	int AI_getTotalAreaCityThreat(CvArea const& kArea) const;
	int AI_getAreaCultureDefendersNeeded(CvArea const& kArea) const; // advc.099c
	int AI_countNumAreaHostileUnits(CvArea const& kArea, bool bPlayer, bool bTeam, bool bNeutral, bool bHostile,
			CvPlot const* pCenter = NULL) const; // advc.081
	int AI_getTotalFloatingDefendersNeeded(CvArea const& kArea,
			bool bDebug = false) const; // advc.007
	int AI_getTotalFloatingDefenders(CvArea const& kArea) const;
	int AI_getTotalAirDefendersNeeded() const; // K-Mod

	RouteTypes AI_bestAdvancedStartRoute(CvPlot* pPlot, int* piYieldValue = NULL) const;
	UnitTypes AI_bestAdvancedStartUnitAI(CvPlot const& kPlot, UnitAITypes eUnitAI) const;
	CvPlot* AI_advancedStartFindCapitalPlot();

	bool AI_advancedStartPlaceExploreUnits(bool bLand);
	void AI_advancedStartRevealRadius(CvPlot* pPlot, int iRadius);
	bool AI_advancedStartPlaceCity(CvPlot* pPlot);
	bool AI_advancedStartImproveCity(CvCity* pCity); // doc?? // TODO: check if this is used
	bool AI_advancedStartDoRoute(CvPlot* pFromPlot, CvPlot* pToPlot);
	void AI_advancedStartRouteTerritory();
	void AI_doAdvancedStart(bool bNoExit = false);

	int AI_getMinFoundValue() const;
	void AI_recalculateFoundValues(int iX, int iY, int iInnerRadius, int iOuterRadius) const;
	void AI_updateCitySites(int iMinFoundValueThreshold = -1, int iMaxSites = 4); // advc: default values
	void AI_invalidateCitySites(int iMinFoundValueThreshold);
	int AI_getNumCitySites() const { return m_aeAICitySites.size(); }
	bool AI_isPlotCitySite(CvPlot const& kPlot) const; // advc: Made plot param const
	int AI_getNumAreaCitySites(CvArea const& kArea, int& iBestValue) const;
	int AI_getNumAdjacentAreaCitySites(int& iBestValue, CvArea const& kWaterArea,
			CvArea const* pExcludeArea = NULL) const;
	int AI_getNumPrimaryAreaCitySites(int iMinimumValue = 0) const; // K-Mod
    CvPlot& AI_getCitySite(int iIndex) const;
    int AI_bestCitySiteSettlerValue(int iAreaID = -1) const; // doc
    int AI_bestAdjacentCitySiteSettlerValue(int iAreaID = -1) const; // doc
	// advc.117, advc.121:
	bool AI_isAdjacentCitySite(CvPlot const& p, bool bCheckCenter) const;
	bool AI_isAwfulSite(CvCity const& kCity, bool bConquest = false) const; // advc.ctr
	bool AI_deduceCitySite(CvCity const& pCity) const; // K-Mod
	void AI_cityKilled(CvCity const& kCity); // advc.104
	void AI_cityCreated(CvCity& kCity); // advc.104
	// K-Mod:
	int AI_countPotentialForeignTradeCities(bool bCheckConnected = true,
			bool bCheckForeignTradePolicy = true, CvArea const* pIgnoreArea = 0) const;

	int AI_bestAreaUnitAIValue(UnitAITypes eUnitAI, CvArea const* pArea = NULL, UnitTypes* peBestUnitType = NULL) const;
	int AI_bestCityUnitAIValue(UnitAITypes eUnitAI, CvCity const* pCity, UnitTypes* peBestUnitType = NULL) const;
	// advc.opt:
	bool AI_isDomainBombard(DomainTypes eDomain) const
	{
		return (AI_calculateTotalBombard(eDomain, 1) > 0);
	}
	int AI_calculateTotalBombard(DomainTypes eDomain,
			int iMaxCount = MAX_INT) const; // advc.opt

	void AI_updateBonusValue(BonusTypes eBonus);
	void AI_updateBonusValue();

	int AI_getUnitClassWeight(UnitClassTypes eUnitClass) const;
	int AI_getUnitCombatWeight(UnitCombatTypes eUnitCombat) const;
	int AI_calculateUnitAIViability(UnitAITypes eUnitAI, DomainTypes eDomain) const;

	int AI_disbandValue(CvUnitAI const& kUnit, bool bMilitaryOnly = true) const; // K-Mod

	int AI_getAttitudeWeight(PlayerTypes ePlayer) const;

	ReligionTypes AI_chooseReligion();

	int AI_getPlotAirbaseValue(CvPlot const& kPlot) const;
	int AI_getPlotCanalValue(CvPlot const& kPlot) const;

	int AI_getHappinessWeight(int iHappy, int iExtraPop, bool bPercent=false) const;
	int AI_getHealthWeight(int iHealth, int iExtraPop, bool bPercent=false) const;

	bool AI_isPlotThreatened(CvPlot* pPlot, int iRange = -1, bool bTestMoves = true) const;

	bool AI_isFirstTech(TechTypes eTech) const;

	void AI_ClearConstructionValueCache(); // K-Mod
	// k146: Used in conjuction with canTrain
	bool AI_haveResourcesToTrain(UnitTypes eUnit) const;
	UnitTypes AI_getBestAttackUnit() const; // advc.079
	scaled AI_trainUnitSpeedAdustment() const; // advc.253

	// <advc.104>
	UWAI::Player& uwai() { return *m_pUWAI; }
	UWAI::Player const& uwai() const { return *m_pUWAI; } // </advc.104>
	// <advc.104h>
	// Returns true if peace deal implemented (or offered to human)
	bool AI_negotiatePeace(PlayerTypes eOther, int iTheirBenefit, int iOurBenefit);
	void AI_offerCapitulation(PlayerTypes eTo);
	// </advc.104h>
	bool AI_willOfferPeace(PlayerTypes eTo) const; // advc
	// advc.130h:
	bool AI_disapprovesOfDoW(TeamTypes eAggressor, TeamTypes eVictim) const;
	bool AI_isDangerFromSubmarines() const; // advc.651
	bool AI_isPiracyTarget(PlayerTypes eTarget) const; // advc.033
	bool AI_isUnitNeedingOpenBorders(TeamTypes eTarget) const; // advc.124
	bool AI_isDefenseFocusOnBarbarians(CvArea const& kArea) const; // advc.300
	bool AI_hasSharedPrimaryArea(PlayerTypes eOther) const; // advc
	// <advc.130r>
	int AI_getContactDelay(ContactTypes eContact) const;
	bool AI_contactRoll(ContactTypes eContact, scaled rMult = 1); // </advc.130r>
	// <advc.104m>
	bool AI_proposeEmbargo(PlayerTypes eHuman);
	bool AI_contactReligion(PlayerTypes eHuman);
	bool AI_contactCivics(PlayerTypes eHuman);
	bool AI_askHelp(PlayerTypes eHuman);
	bool AI_demandTribute(PlayerTypes eHuman, AIDemandTypes eDemand);
	// </advc.104m>  <advc.ctr>
	CvCityAI const* AI_bestRequestCity(PlayerTypes eOwner, scaled rMinVal = 1,
			scaled rMinRatio = -1) const;
	bool AI_proposeCityTrade(PlayerTypes eToPlayer);
	bool AI_intendsToCede(CvCityAI const& kCity, PlayerTypes eToPlayer,
			bool bLiberateForFree = false, int* piTradeVal = NULL) const;
	scaled AI_totalYieldVal() const;
	scaled AI_targetAmortizationTurns() const; // </advc.ctr>
	scaled AI_amortizationMultiplier(int iDelay) const; // advc.104, advc.031
	// advc.104r: Made public and param added
	void AI_doSplit(bool bForce = false);

    int AI_slaveTradeVal(CvUnit* pUnit) const; // doc (edead)
    int AI_getPersecutionValue(ReligionTypes eReligion) const; // doc
    int AI_neededPersecutors(CvArea* pArea) const; // doc
    bool AI_enablesUnitWonder(UnitClassTypes eUnitClass, int iPathLength) const; // doc // TODO: used?
    bool AI_willUseNukes(PlayerTypes eTarget, bool bOffensive) const; // doc // TODO: used?
    int AI_getEnemyPower(bool bIncludeMinors = false) const; // doc

	// for serialization
	void read(FDataStreamBase* pStream);
	void write(FDataStreamBase* pStream);

protected:
	int m_iPeaceWeight;
	int m_iEspionageWeight;
	int m_iAttackOddsChange;
	int m_iCivicTimer;
	int m_iReligionTimer;
	int m_iExtraGoldTarget;
	int m_iCityTargetTimer; // K-Mod
	scaled m_rCurrEraFactor; // advc.erai
	bool m_bDangerFromSubmarines; // advc.651
	UWAI::Player* m_pUWAI; // advc.104

	/*mutable int m_iStrategyHash;
	mutable int m_iStrategyHashCacheTurn;
	mutable int m_iAveragesCacheTurn;
	mutable int m_iAverageGreatPeopleMultiplier;
	mutable int *m_aiAverageYieldMultiplier;
	mutable int *m_aiAverageCommerceMultiplier;
	mutable int *m_aiAverageCommerceExchange;
	mutable int m_iUpgradeUnitsCacheTurn;
	mutable int m_iUpgradeUnitsCachedExpThreshold;
	mutable int m_iUpgradeUnitsCachedGold;*/ // BtS
	// K-Mod. The original caching method was just begging for OOS bugs.
	AIStrategy m_eStrategyHash;
	// BBAI variables (adjusted for K-Mod)
	unsigned m_iStrategyRand;
	AIVictoryStage m_eVictoryStageHash;
	// end BBAI

	int m_iAverageGreatPeopleMultiplier;
    int m_iAverageTradeMultiplier; // doc

	int m_iAverageCulturePressure; // K-Mod culture pressure

	int *m_aiAverageYieldMultiplier;
	int *m_aiAverageCommerceMultiplier;
	int *m_aiAverageCommerceExchange;

	int m_iUpgradeUnitsCachedGold;
	int m_iAvailableIncome;
	// K-Mod end

	int *m_aiNumTrainAIUnits;
	int *m_aiNumAIUnits;
	int* m_aiSameReligionCounter;
	int* m_aiDifferentReligionCounter;
	int* m_aiFavoriteCivicCounter;
	int* m_aiBonusTradeCounter;
	int* m_aiPeacetimeTradeValue;
	int* m_aiPeacetimeGrantValue;
	int* m_aiGoldTradedTo;
	int* m_aiAttitudeExtra;
	ArrayEnumMap<PlayerTypes,scaled> m_arExpansionistHate; // advc.130w
	// <advc.079>
	mutable UnitTypes m_aeLastBrag[MAX_CIV_PLAYERS];
	mutable TeamTypes m_aeLastWarn[MAX_CIV_PLAYERS]; // </advc.079>
	int* m_aiBonusValue;
	int* m_aiLastBonusValueChange; // doc // TODO: improve caching
	int* m_aiBonusValueTrade; // advc.036
	int* m_aiUnitClassWeights;
	int* m_aiUnitCombatWeights;
	ArrayEnumMap<VictoryTypes,short> m_aiVictoryWeights; // advc.115f

	std::map<UnitClassTypes, int> m_GreatPersonWeights; // K-Mod
	std::map<int,int> m_neededExplorersByArea; // advc.opt

	mutable std::vector<TechTypes> m_aeBestTechs; // advc.550g
	//mutable int* m_aiCloseBordersAttitude;
	// K-Mod: (the original system was prone to mistakes.)
	std::vector<int> m_aiCloseBordersAttitude;
	std::vector<int> m_aiAttitude; // K-Mod

	bool* m_abFirstContact; // advc.003j: Now unused

	int** m_aaiContactTimer;
	int** m_aaiMemoryCount;

	std::vector<PlotNumTypes> m_aeAICitySites;

	bool m_bWasFinancialTrouble;
	int m_iTurnLastProductionDirty;

	void AI_doCounter();
	void AI_doMilitary();
	void AI_doResearch();
	void AI_doCivics();
	void AI_doReligion();
	void AI_doDiplo();
	void AI_doCheckFinancialTrouble();
	int AI_GPModifierCivicVal(std::vector<int>& kBaseRates, int iModifier) const; // advc
	// <advc.026>
	void AI_roundTradeValBounds(int& iTradeVal, bool bPreferRoundingUp = false,
			int iLower = MIN_INT, int iUpper = MAX_INT) const; // </advc.026>
	/*  <advc> Overlaps with CvTeamAI::roundTradeVal. Could call that function,
		but don't want to include CvTeamAI.h here. (And want inlining.) */
	void AI_roundTradeVal(int& iTradeVal) const
	{
		iTradeVal -= iTradeVal % GC.getDefineINT(CvGlobals::DIPLOMACY_VALUE_REMAINDER);
	}
	bool AI_proposeJointWar(PlayerTypes eHuman);
	void AI_proposeWarTrade(PlayerTypes eAIPlayer); // </advc>

	int AI_rivalPactAttitude(PlayerTypes ePlayer, bool bVassalPacts) const; // advc.130t

	bool AI_canBeAttackedBy(CvUnit const& u) const; // advc.315

	// <advc.130p>
	scaled AI_peacetimeTradeMultiplier(PlayerTypes eOtherPlayer,
			TeamTypes eOtherTeam = NO_TEAM) const;
	int AI_peacetimeTradeValDivisor(bool bRival) const;
	/*  The change-value functions (now called 'process', e.g. AI_processPeacetimeValue)
		apply adjustments and have a side-effect on EnemyTrade and EnemyGrant values.
		These here are simple setters. */
	void AI_setPeacetimeTradeValue(PlayerTypes eIndex, int iVal);
	void AI_setPeacetimeGrantValue(PlayerTypes eIndex, int iVal);
	// </advc.130p>
	// <advc.130n>
	enum IdeologicMarker { SAME_RELIGION, DIFFERENT_RELIGION, SAME_CIVIC };
	int AI_ideologyAttitudeChange(PlayerTypes eOther, IdeologicMarker eMarker,
			int iCounter, int iDivisor, int iLimit) const; // </advc.130n>
	// advc.130r: Are they at war with a partner of ours?
	bool AI_atWarWithPartner(TeamTypes eOtherTeam,
			/*  advc.130h: If CheckPartnerAttacked==true, then only partners with
				war plan "attacked" or "attacked recent" count. */
			bool bCheckPartnerAttacked = false) const;
	// <advc.104h>
	int AI_negotiatePeace(PlayerTypes eRecipient, PlayerTypes eGiver, int iDelta,
			int* iGold, TechTypes* eBestTech, CvCity const** pBestCity); // </advc.104h>
	bool AI_counterPropose(PlayerTypes ePlayer, // advc: was public
			CLinkList<TradeData> const& kTheyGive, CLinkList<TradeData> const& kWeGive,
			CLinkList<TradeData> const& kTheirInventory, CLinkList<TradeData> const& kOurInventory,
			CLinkList<TradeData>& kTheyAlsoGive, CLinkList<TradeData>& kWeAlsoGive,
			scaled rLeniency = 1) const; // advc.705
	// <advc>
	// Variant that writes the proposal into pTheirList and pOurList
	bool AI_counterPropose(PlayerTypes ePlayer, CLinkList<TradeData>& kTheyGive,
			CLinkList<TradeData>& kWeGive, bool bTheyMayGiveMore, bool bWeMayGiveMore,
			scaled rLeniency = 1) const;
	bool AI_balanceDeal(bool bGoldDeal, CLinkList<TradeData> const& kTheirInventory,
			PlayerTypes ePlayer, int iTheyReceive, int& iWeReceive,
			CLinkList<TradeData>& kWeWant, CLinkList<TradeData> const& kWeGive,
			scaled rLeniency, // advc.705
			bool bTheyGenerous,
			int iHappyLeft, int iHealthLeft, int iOtherListLength) const; // advc.036
	int AI_tradeValToGold(int iTradeVal, bool bOverpay, int iMaxGold = MAX_INT,
			bool* bEnough = NULL) const;
	// <advc.ctr>
	AttitudeTypes AI_cityTradeAttitudeThresh(CvCity const& kCity, PlayerTypes eToPlayer, bool bLiberate) const;
	scaled AI_peaceTreatyAversion(TeamTypes eTarget) const;
	// </advc.ctr>
	enum CancelCode { NO_CANCEL = -1, RENEGOTIATE, DO_CANCEL };
	CancelCode AI_checkCancel(CvDeal const& d, PlayerTypes ePlayer);
	bool AI_doDeals(PlayerTypes eOther);
	// </advc>
	bool AI_proposeResourceTrade(PlayerTypes eTo); // advc.133
	// advc.132:
	bool AI_checkCivicReligionConsistency(CLinkList<TradeData> const& kTradeItems) const;
	// <advc.036>
	bool AI_checkResourceLimits(CLinkList<TradeData> const& kWeGive,
			CLinkList<TradeData> const& kTheyGive, PlayerTypes eThey,
			int iChange) const; // </advc.036>
	// <advc.026>
	int AI_maxGoldTradeGenerous(PlayerTypes eTo) const;
	int AI_maxGoldPerTurnTradeGenerous(PlayerTypes eTo) const;
	bool AI_checkMaxGold(CLinkList<TradeData> const& kItems, PlayerTypes eTo) const;
	// </advc.026>
	int AI_adjustTradeGoldToDiplo(int iGold, PlayerTypes eTo) const;
	void AI_foldDeals() const;
	void AI_foldDeals(CvDeal& d1, CvDeal& d2) const; // </advc.036>
	scaled AI_bonusImportValue(PlayerTypes eFrom) const; // advc.149
	int AI_anarchyTradeVal(CivicTypes eCivic = NO_CIVIC) const; // advc.132
	int AI_defianceAngerCost(VoteSourceTypes eVS) const; // advc.118b

	void AI_updateCacheData(); // K-Mod
	int AI_calculateEspionageWeight() const; // advc.001

	bool AI_isThreatFromMinorCiv() const; // advc.109
	void AI_updateDangerFromSubmarines(); // advc.651
	bool AI_cheatDangerVisibility(CvPlot const& kAt) const; // advc.128
	// <advc>
	int AI_countDangerousUnits(CvPlot const& kAttackerPlot, CvPlot const& kDefenderPlot,
			bool bTestMoves, int iLimit = MAX_INT,
			PlayerTypes eAttackPlayer = NO_PLAYER) const; // </advc>
	// advc.130c:
	int AI_knownRankDifference(PlayerTypes eOther, scaled& rOutrankingBothRatio) const;
	// advc.042: Relies on caller to reset GC.getBorderFinder()
	bool AI_isUnimprovedBonus(CvPlot const& p, CvPlot const* pFromPlot, bool bCheckPath) const;
	int AI_neededExplorers_bulk(CvArea const& kArea) const; // advc.opt
	// BETTER_BTS_AI_MOD, Victory Strategy AI, 03/17/10, jdog5000: START
	// (advc: moved here from the public section)
	int AI_calculateSpaceVictoryStage() const;
	int AI_calculateConquestVictoryStage() const;
	int AI_calculateDominationVictoryStage() const;
	int AI_calculateDiplomacyVictoryStage() const;
	// BETTER_BTS_AI_MOD: END
	bool AI_isVictoryValid(VictoryTypes eVictory, int& iWeight) const; // advc.115f
	// K-Mod. I've moved the bulk of AI_getStrategyHash into a new function: AI_updateStrategyHash.
	AIStrategy AI_getStrategyHash() const { return m_eStrategyHash; }
	void AI_updateStrategyHash();
	void AI_calculateAverages();

	void AI_convertUnitAITypesForCrush();
	int AI_eventValue(EventTypes eEvent, const EventTriggeredData& kTriggeredData) const;

	void AI_doEnemyUnitData();
	//void AI_invalidateCloseBordersAttitude(); // disabled by K-Mod
	bool AI_isCommercePlot(CvPlot* pPlot) const; // advc: Was public; deprecated.
	// <advc>
	scaled AI_estimateYieldRate(YieldTypes eYield) const; // advc
	int AI_baseBonusUnitVal(BonusTypes eBonus, UnitTypes eUnit, CvCity const* pCapital,
			CvCity const* pCoastalCity, bool bTrade) const;
	int AI_baseBonusBuildingVal(BonusTypes eBonus, BuildingTypes eBuilding, int iCities,
			int iCoastalCities, bool bTrade) const;
	int AI_baseBonusProjectVal(BonusTypes eBonus, ProjectTypes eProject, bool bTrade) const;
	int AI_baseBonusRouteVal(BonusTypes eBonus, RouteTypes eRoute,
			RouteTypes eBestRoute, TechTypes eBuildTech, bool bTrade) const;
	// </advc>
	void AI_setHuman(bool b); // advc.127
	void logFoundValue(CvPlot const& kPlot, bool bStartingLoc = false) const; // advc.031c

	friend class CvGameTextMgr;
	friend class CvPlayer; // advc.003u: So that protected functions can be called through CvPlayer::AI
};

// <advc.003u> (Counterparts to global functions in CvPlayer.h)
inline CvCityAI* AI_getCity(IDInfo city)
{
	FAssertBounds(0, MAX_PLAYERS, city.eOwner);
	return GET_PLAYER(city.eOwner).AI_getCity(city.iID);
}
inline CvUnitAI* AI_getUnit(IDInfo unit)
{
	FAssertBounds(0, MAX_PLAYERS, unit.eOwner);
	return GET_PLAYER(unit.eOwner).AI_getUnit(unit.iID);
} // </advc.003u>

#endif
