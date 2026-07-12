#pragma once

#ifndef CIV4_UNIT_H
#define CIV4_UNIT_H

#include "CvDLLEntity.h"

class CvPlot;
class CvArea;
class CvUnitInfo;
class CvSelectionGroup;
class CvArtInfoUnit;
class GroupPathFinder;
class CvUnitAI; // advc.003u
struct CombatDetails;

class CvUnit : public CvDLLUnitEntity
{
public:
	virtual ~CvUnit();

	void setupGraphical();
	void reloadEntity();

	void convert(CvUnit* pUnit);																			// Exposed to Python
	void kill(bool bDelay, PlayerTypes ePlayer = NO_PLAYER);												// Exposed to Python

	DllExport void NotifyEntity(MissionTypes eMission);

	void doTurn();
	void doTurnPost(); // advc.029
	void updateCombat(bool bQuick = false, /* advc.004c: */ bool* pbIntercepted = NULL,
			bool bSeaPatrol = false); // advc.004k
	void updateAirCombat(bool bQuick = false);
	bool updateAirStrike(CvPlot& kPlot, bool bQuick, bool bFinish);

	bool isActionRecommended(int iAction);
	void onActiveSelection(); // advc
	void updateFoundingBorder(bool bForceClear = false) const; // advc.004h

	bool isUnowned() const; // advc.061

	bool canDoCommand(CommandTypes eCommand, int iData1, int iData2,										// Exposed to Python
			bool bTestVisible = false, bool bTestBusy = true) const;
	void doCommand(CommandTypes eCommand, int iData1, int iData2);											// Exposed to Python

	//FAStarNode* getPathLastNode() const; // disabled by K-Mod
	CvPlot& getPathEndTurnPlot() const;																		// Exposed to Python
	bool generatePath(CvPlot const& kTo, MovementFlags eFlags = NO_MOVEMENT_FLAGS,							// Exposed to Python
			bool bReuse = false,
			int* piPathTurns = NULL,
			int iMaxPath = -1, // K-Mod
			bool bUseTempFinder = false) const; // advc.128
	GroupPathFinder& getPathFinder() const; // K-Mod
	// <advc>
	void pushGroupMoveTo(CvPlot const& kTo, MovementFlags eFlags = NO_MOVEMENT_FLAGS,
			bool bAppend = false, bool bManual = false, MissionAITypes eMissionAI = NO_MISSIONAI,
			CvPlot const* pMissionAIPlot = NULL, CvUnit const* pMissionAIUnit = NULL,
			bool bModified = false); // </advc>

	bool canEnterTerritory(TeamTypes eTeam, bool bIgnoreRightOfPassage = false,								// Exposed to Python
			CvArea const* pArea = NULL) const; // advc: canEnterArea merged into canEnterTerritory
	TeamTypes getDeclareWarMove(const CvPlot* pPlot) const;													// Exposed to Python
	bool canMoveInto(CvPlot const& kPlot, bool bAttack = false, bool bDeclareWar = false,					// Exposed to Python
			bool bIgnoreLoad = false,
			bool bAssumeVisible = true, // K-Mod
			bool bDangerCheck = false) const; // advc.001k
	bool canMoveOrAttackInto(CvPlot const& kPlot, bool bDeclareWar = false,									// Exposed to Python
			bool bDangerCheck = false) const; // advc.001k
	// bool canMoveThrough(const CvPlot* pPlot, bool bDeclareWar = false) const; // disabled by K-Mod (was exposed to Python)
	bool canEnterArea(CvArea const& kArea) const; // advc.030
	// <advc>
	bool isEnemyCity(CvPlot const& kPlot) const;											// Exposed to Python /via CyPlot)
	// was CvPlot::isValidDomainForLocation
	bool isValidDomain(CvPlot const& kPlot) const;											// Exposed to Python (via CyPlot)
	bool isRevealedValidDomain(CvPlot const& kPlot) const;
	// was CvPlot::isValidDomainForAction
	bool isValidDomain(bool bWater) const													// Exposed to Python (via CyPlot)
	{
		switch (getDomainType())
		{
			case DOMAIN_SEA: return (bWater || canMoveAllTerrain());
			case DOMAIN_AIR: return false;
			case DOMAIN_LAND: // fall through
			case DOMAIN_IMMOBILE: return (!bWater || canMoveAllTerrain());
			default: FAssert(false); return false;
		}
	}
	// Replacing CvPlot::isFriendlyCity
	bool isPlotValid(CvPlot const& kPlot) const;											// Exposed to Python (via CyPlot::isFriendlyCity)
	bool isRevealedPlotValid(CvPlot const& kPlot) const; // </advc>
	bool isInvasionMove(CvPlot const& kFrom, CvPlot const& kTo) const; // advc.162
	void attack(CvPlot* pPlot, bool bQuick, /* advc.004c: */ bool* pbIntercepted = NULL,
			bool bSeaPatrol = false); // advc
	void attackForDamage(CvUnit *pDefender, int attackerDamageChange, int defenderDamageChange);
	void fightInterceptor(CvPlot const& kPlot, bool bQuick);
	void move(CvPlot& kPlot, bool bShow, // advc: 1st param was CvPlot* (not const b/c of possible feature change)
			bool bJump = false, bool bGroup = true); // advc.163
	// K-Mod added bForceMove and bGroup
	bool jumpToNearestValidPlot(bool bGroup = false, bool bForceMove = false,								// Exposed to Python
			bool bFreeMove = false); // advc.163

	bool canAutomate(AutomateTypes eAutomate) const;														// Exposed to Python
	void automate(AutomateTypes eAutomate);

	bool canScrap() const;																					// Exposed to Python
	void scrap();

	bool canGift(bool bTestVisible = false, bool bTestTransport = true) const;								// Exposed to Python
	void gift(bool bTestTransport = true);

	bool canLoadOnto(CvUnit const& kUnit, CvPlot const& kPlot,	 											// Exposed to Python
			bool bCheckMoves = false) const; // advc.123c
	void loadOnto(CvUnit& kUnit);
	bool canLoadOntoAnyUnit(CvPlot const& kPlot,															// Exposed to Python
			bool bCheckMoves = false) const; // advc.123c
	void load();
	bool shouldLoadOnMove(const CvPlot* pPlot) const;

	bool canUnload() const;																					// Exposed to Python
	void unload();

	bool canUnloadAll() const;																				// Exposed to Python
	void unloadAll();

	bool canHold(const CvPlot* pPlot) const { return true; }												// Exposed to Python
	bool canSleep(const CvPlot* pPlot) const;																// Exposed to Python
	bool canFortify(const CvPlot* pPlot) const;																// Exposed to Python
	bool canAirPatrol(const CvPlot* pPlot) const;															// Exposed to Python
	void airCircle(bool bStart);

	bool canSeaPatrol(CvPlot const* pPlot																	// Exposed to Python
			= NULL, bool bCheckActivity = false) const; // advc
	bool isSeaPatrolling() const; // advc
	bool canReachBySeaPatrol(CvPlot const& kDest, CvPlot const* pFrom = NULL) const; // advc.004k

	bool canHeal(const CvPlot* pPlot) const;																// Exposed to Python
	bool canSentryHeal(const CvPlot* pPlot) const; // advc.004l
	bool canSentry(const CvPlot* pPlot) const;																// Exposed to Python

	int healRate(/* K-Mod: */ bool bLocation = true, bool bUnits = true,
			CvPlot const* pAt /* advc: */ = NULL) const;
	int healTurns(CvPlot const* pAt /* advc: */ = NULL) const;
	void doHeal();

		// advc (tbd.): Change the iX,iY params to a CvPlot const& kTarget (x10)
	bool canAirlift(const CvPlot* pPlot) const;																// Exposed to Python
	bool canAirliftAt(const CvPlot* pPlot, int iX, int iY) const;											// Exposed to Python
	bool airlift(int iX, int iY);

	bool isNukeVictim(const CvPlot* pPlot, TeamTypes eTeam,													// Exposed to Python
			TeamTypes eObs = NO_TEAM) const; // kekm.7 (advc)
	bool canNuke(CvPlot const* pFrom) const { return (nukeRange() != -1); }									// Exposed to Python
	bool canNukeAt(CvPlot const& kFrom, int iX, int iY,														// Exposed to Python
			TeamTypes eObs = NO_TEAM) const; // kekm.7 (advc)
	bool nuke(int iX, int iY);
	// <advc.650>
	int nukeInterceptionChance(CvPlot const& kTarget, TeamTypes eObs = NO_TEAM,
			CvUnit* pInterceptUnit = NULL,
			TeamTypes* eBestTeam = NULL,
			EagerEnumMap<TeamTypes,bool> const* pTeamsAffected = NULL) const;
	// <advc.650>
	bool canRecon(const CvPlot* pPlot) const;																// Exposed to Python
	bool canReconAt(const CvPlot* pPlot, int iX, int iY) const;												// Exposed to Python
	bool recon(int iX, int iY);
	// <advc> Param lists changed for these two
	bool canAirBomb(CvPlot const* pFrom = NULL) const;														// Exposed to Python
	bool canAirBombAt(CvPlot const& kTarget, CvPlot const* pFrom = NULL) const; // </advc>					// Exposed to Python
	// <advc.255>
	enum StructureTypes { NO_STRUCTURE, STRUCTURE_IMPROVEMENT, STRUCTURE_ROUTE };
	StructureTypes getDestructibleStructureAt(CvPlot const& kTarget,
			bool bTestVisibility, // </advc.255>
			bool bForceImprovement = false) const; // advc.111
	int airBombDefenseDamage(CvCity const& kCity) const; // advc
	bool airBomb(CvPlot& kTarget, /* advc.004c: */ bool* pbIntercepted = NULL,
			bool bForceImprovement = false); // advc.111

	bool canAirStrike(CvPlot const& kPlot) const; // (advc.004c: was protected)

	CvCity* bombardTarget(CvPlot const& kFrom) const;														// Exposed to Python
	bool canBombard(CvPlot const& kFrom) const;																// Exposed to Python
	int damageToBombardTarget(CvPlot const& kFrom) const; // advc
	bool bombard();

	bool canParadrop(const CvPlot* pPlot) const;															// Exposed to Python
	bool canParadropAt(const CvPlot* pPlot, int iX, int iY) const;											// Exposed to Python
	bool paradrop(int iX, int iY, /* advc.004c: */ IDInfo* pInterceptor = NULL);

	bool canPillage(CvPlot const& kPlot) const;																// Exposed to Python
	bool pillage(/* advc.111: */ bool bForceImprovement = false);

	bool canAssassin(const CvPlot* pPlot, bool bTestVisible) const; // SuperSpies (TSHEEP)																										// Exposed to Python
	bool awardSpyExperience(TeamTypes eTargetTeam, EspionageMissionTypes eMission, int iCostModifier); // SuperSpies (TSHEEP)
	bool canBribe(const CvPlot* pPlot, bool bTestVisible) const; // SuperSpies (glider1)

	bool canPlunder(CvPlot const& kPlot, bool bTestVisible = false) const;									// Exposed to Python
	bool plunder();
	void updatePlunder(int iChange, bool bUpdatePlotGroups);
	void blockadeRange(std::vector<CvPlot*>& r, int iExtra = 0, // advc
			bool bCheckCanPlunder = true) const; // advc.033

	int sabotageCost(const CvPlot* pPlot) const;															// Exposed to Python
	int sabotageProb(const CvPlot* pPlot, ProbabilityTypes eProbStyle = PROBABILITY_REAL) const;			// Exposed to Python
	bool canSabotage(const CvPlot* pPlot, bool bTestVisible = false) const;									// Exposed to Python
	bool sabotage();

	int destroyCost(const CvPlot* pPlot) const;																// Exposed to Python
	int destroyProb(const CvPlot* pPlot, ProbabilityTypes eProbStyle = PROBABILITY_REAL) const;				// Exposed to Python
	bool canDestroy(const CvPlot* pPlot, bool bTestVisible = false) const;									// Exposed to Python
	bool destroy();

	int stealPlansCost(const CvPlot* pPlot) const;															// Exposed to Python
	int stealPlansProb(const CvPlot* pPlot, ProbabilityTypes eProbStyle = PROBABILITY_REAL) const;			// Exposed to Python
	bool canStealPlans(const CvPlot* pPlot, bool bTestVisible = false) const;								// Exposed to Python
	bool stealPlans();

	bool canFound(const CvPlot* pPlot, bool bTestVisible = false) const;									// Exposed to Python
	bool found();

	bool canSpread(const CvPlot* pPlot, ReligionTypes eReligion, bool bTestVisible = false, bool bAI = false) const;			// Exposed to Python
	bool spread(ReligionTypes eReligion);
	int getSpreadChance(ReligionTypes eReligion) const;

	bool canSpreadCorporation(const CvPlot* pPlot, CorporationTypes eCorporation,							// Exposed to Python
			bool bTestVisible = false) const;
	bool spreadCorporation(CorporationTypes eCorporation);
	int spreadCorporationCost(CorporationTypes eCorporation, CvCity const* pCity) const;

	bool canJoin(const CvPlot* pPlot, SpecialistTypes eSpecialist) const;									// Exposed to Python
	bool join(SpecialistTypes eSpecialist);

	bool canConstruct(const CvPlot* pPlot, BuildingTypes eBuilding, bool bTestVisible = false) const;		// Exposed to Python
	bool construct(BuildingTypes eBuilding);

	TechTypes getDiscoveryTech(TechTypes eIgnoreTech = NO_TECH) const;																		// Exposed to Python
	int getDiscoverResearch(TechTypes eTech) const;															// Exposed to Python
	bool canDiscover(const CvPlot* pPlot) const;															// Exposed to Python
	bool discover();

	int getMaxHurryProduction(CvCity const* pCity) const;													// Exposed to Python
	int getHurryProduction(const CvPlot* pPlot) const;														// Exposed to Python
	bool canHurry(const CvPlot* pPlot, bool bTestVisible = false) const;									// Exposed to Python
	bool hurry();

	int getTradeGold(const CvPlot* pPlot) const;															// Exposed to Python
	bool canTrade(const CvPlot* pPlot, bool bTestVisible = false) const;									// Exposed to Python
	bool trade();

	int getGreatWorkCulture(const CvPlot* pPlot,															// Exposed to Python
			int* piPerEra = NULL) const; // advc.251
	bool canGreatWork(const CvPlot* pPlot) const;															// Exposed to Python
	bool greatWork();

	int getEspionagePoints(const CvPlot* pPlot) const;														// Exposed to Python
	bool canInfiltrate(const CvPlot* pPlot, bool bTestVisible = false) const;								// Exposed to Python
	bool infiltrate();

	bool canEspionage(const CvPlot* pPlot, bool bTestVisible = false) const;
	bool espionage(EspionageMissionTypes eMission, int iData);
	bool testSpyIntercepted(PlayerTypes eTargetPlayer, bool bMission, int iModifier); // (K-Mod added bMission)
	int getSpyInterceptPercent(TeamTypes eTargetTeam, bool bMission) const; // (K-Mod added bMission)
	bool isIntruding() const;

	bool canGoldenAge(const CvPlot* pPlot, bool bTestVisible = false) const;								// Exposed to Python
	bool goldenAge();

	bool canBuild(CvPlot const& pPlot, BuildTypes eBuild,													// Exposed to Python
			bool bTestVisible = false, /* advc.181: */ bool bIgnoreFoW = true) const;
	bool build(BuildTypes eBuild);

	bool canPromote(PromotionTypes ePromotion,																// Exposed to Python
			int iLeaderUnitId /* advc: */ = FFreeList::INVALID_INDEX) const;
	void promote(PromotionTypes ePromotion,																	// Exposed to Python
			int iLeaderUnitId /* advc: */ = FFreeList::INVALID_INDEX);
	int promotionHeal(PromotionTypes ePromotion = NO_PROMOTION) const; // advc

	int canLead(const CvPlot* pPlot, int iUnitId) const;
	bool lead(int iUnitId);

	int canGiveExperience(const CvPlot* pPlot) const;														// Exposed to Python
	bool giveExperience();																					// Exposed to Python
	int getStackExperienceToGive(int iNumUnits) const;

	bool canResolveCrisis(CvPlot const& kPlot) const; // doc
	bool resolveCrisis(); // doc

	bool canReformGovernment(CvPlot const& kPlot) const; // doc
	bool reformGovernment(); // doc

	bool canDiplomaticMission(CvPlot const& kPlot) const; // doc
	bool diplomaticMission(); // doc

	bool canPersecute(CvPlot const& kPlot) const; // doc
	bool persecute(ReligionTypes eReligion); // doc

	bool canGreatMission(CvPlot const& kPlot) const; // doc
	bool greatMission(); // doc

	bool canSatelliteAttack(CvPlot const& kPlot) const; // doc
	bool satelliteAttack(); // doc

	bool canRebuild(CvPlot const& kPlot) const; // doc
	bool rebuild(); // doc

	int upgradePrice(UnitTypes eUnit) const;																// Exposed to Python
	int upgradeXPChange(UnitTypes eUnit) const; // advc.080
	bool upgradeAvailable(UnitTypes eFromUnit, UnitClassTypes eToUnitClass, int iCount = 0) const;			// Exposed to Python
	bool canUpgrade(UnitTypes eUnit, bool bTestVisible = false) const;										// Exposed to Python
	bool isReadyForUpgrade() const;
	/*	has upgrade is used to determine if an upgrade is possible,
		it specifically does not check whether the unit can move, whether the current plot is owned, enough gold
		those are checked in canUpgrade()
		does not search all cities, only checks the closest one */
	bool hasUpgrade(bool bSearch = false) const																// Exposed to Python
	{
		return (getUpgradeCity(bSearch) != NULL);
	}
	bool hasUpgrade(UnitTypes eUnit, bool bSearch = false) const
	{
		return (getUpgradeCity(eUnit, bSearch) != NULL);
	}
	CvCity* getUpgradeCity(bool bSearch = false) const;
	CvCity* getUpgradeCity(UnitTypes eUnit, bool bSearch = false, int* iSearchValue = NULL) const;
	//void upgrade(UnitTypes eUnit);
	CvUnit* upgrade(UnitTypes eUnit); // K-Mod

	HandicapTypes getHandicapType() const;																	// Exposed to Python
	CivilizationTypes getCivilizationType() const;															// Exposed to Python
	const wchar* getVisualCivAdjective(TeamTypes eForTeam) const;
	SpecialUnitTypes getSpecialUnitType() const																// Exposed to Python
	{
		return m_pUnitInfo->getSpecialUnitType();
	}
	UnitTypes getCaptureUnitType(CivilizationTypes eCivilization) const;									// Exposed to Python
	int getCaptureOdds(CvUnit const& kDefender) const; // advc.010
	UnitCombatTypes getUnitCombatType() const																// Exposed to Python
	{
		return m_pUnitInfo->getUnitCombatType();
	}
	DllExport DomainTypes getDomainType() const																// Exposed to Python
	{
		return m_pUnitInfo->getDomainType();
	}
	InvisibleTypes getInvisibleType() const																	// Exposed to Python
	{
		return m_pUnitInfo->getInvisibleType();
	}
	int getNumSeeInvisibleTypes() const																		// Exposed to Python
	{
		return m_pUnitInfo->getNumSeeInvisibleTypes();
	}
	InvisibleTypes getSeeInvisibleType(int i) const															// Exposed to Python
	{
		return m_pUnitInfo->getSeeInvisibleType(i);
	}

	int flavorValue(FlavorTypes eFlavor) const																// Exposed to Python
	{
		return m_pUnitInfo->getFlavorValue(eFlavor);
	}

	bool isBarbarian() const;																				// Exposed to Python
	// advc.313:
	bool isKnownSeaBarbarian() const
	{
		return (isBarbarian() && getDomainType() == DOMAIN_SEA &&
				// Future-proof for Barbarian Privateers
				!m_pUnitInfo->isHiddenNationality());
	}
	bool isHuman() const;																					// Exposed to Python
	bool isIndependent() const;
	bool isNative() const;
	bool isMinorCiv() const;

	int visibilityRange() const;																			// Exposed to Python

	int baseMoves() const;																					// Exposed to Python
	int maxMoves() const																					// Exposed to Python
	{
		return (baseMoves() * GC.getMOVE_DENOMINATOR());
	}
	int movesLeft() const																					// Exposed to Python
	{
		return std::max(0, maxMoves() - getMoves());
	}
	DllExport bool canMove() const;																			// Exposed to Python
	DllExport bool hasMoved() const																			// Exposed to Python
	{
		return (getMoves() > 0);
	}

	int airRange() const																					// Exposed to Python
	{
		return (m_pUnitInfo->getAirRange() + getExtraAirRange());
	}
	int nukeRange() const																					// Exposed to Python
	{
		return m_pUnitInfo->getNukeRange();
	}
	bool isNuke() const { return m_pUnitInfo->isNuke(); } // advc

	bool canBuildRoute() const;																				// Exposed to Python
	DllExport BuildTypes getBuildType() const;																// Exposed to Python
	int workRate(bool bMax) const;																			// Exposed to Python

	bool isAnimal() const																					// Exposed to Python
	{
		return m_pUnitInfo->isAnimal();
	}
	bool isNoBadGoodies() const																				// Exposed to Python
	{
		return m_pUnitInfo->isNoBadGoodies();
	}
	bool isOnlyDefensive() const																			// Exposed to Python
	{
		return m_pUnitInfo->isOnlyDefensive();
	}
	bool isNoCityCapture() const;																			// Exposed to Python
	bool isNoUnitCapture() const; // advc.315b
	bool isRivalTerritory() const																			// Exposed to Python
	{
		return m_pUnitInfo->isRivalTerritory();
	}
	bool isMilitaryHappiness() const;																		// Exposed to Python
	bool isGarrisonInTeamCity() const; // advc.184
	int garrisonStrength() const; // advc.101
	bool isInvestigate() const																				// Exposed to Python
	{
		return m_pUnitInfo->isInvestigate();
	}
	bool isCounterSpy() const																				// Exposed to Python
	{
		return m_pUnitInfo->isCounterSpy();
	}
	bool isSpy() const
	{
		return m_pUnitInfo->isSpy();
	}
	bool isFound() const																					// Exposed to Python
	{
		return m_pUnitInfo->isFound();
	}
	bool isGoldenAge() const;																				// Exposed to Python
	bool canCoexistWithEnemyUnit(TeamTypes eTeam) const;													// Exposed to Python

	DllExport bool isFighting() const																		// Exposed to Python
	{
		return (getCombatUnit() != NULL);
	}
	DllExport bool isAttacking() const;																		// Exposed to Python
	DllExport bool isDefending() const;																		// Exposed to Python
	bool isInCombat() const;																				// Exposed to Python

	DllExport int maxHitPoints() const																		// Exposed to Python
	{
		return GC.getMAX_HIT_POINTS();
	}
	int currHitPoints() const																				// Exposed to Python
	{
		return (maxHitPoints() - getDamage());
	}
	bool isHurt() const																						// Exposed to Python
	{
		return (getDamage() > 0);
	}
	DllExport bool isDead() const																			// Exposed to Python
	{
		return (getDamage() >= maxHitPoints());
	}
	// advc:
	bool isLethalDamage(int iDamage)
	{
		return (currHitPoints() - iDamage <= 0);
	}

	bool isExisting() const { return getX() >= 0 && getY() >= 0; }; // doc

	void setBaseCombatStr(int iCombat);																		// Exposed to Python
	int baseCombatStr() const																				// Exposed to Python
	{
		return m_iBaseCombat;
	}  // advc: Default values - to make clear that these can be NULL.
	int maxCombatStr(CvPlot const* pPlot = NULL, CvUnit const* pAttacker = NULL,							// Exposed to Python
			CombatDetails* pCombatDetails = NULL,
			bool bGarrisonStrength = false) const; // advc.500b
	int currCombatStr(CvPlot const* pPlot = NULL, CvUnit const* pAttacker = NULL,							// Exposed to Python
		CombatDetails* pCombatDetails = NULL) const
	{
		return ((maxCombatStr(pPlot, pAttacker, pCombatDetails) * currHitPoints()) / maxHitPoints());
	}
	int currFirepower(const CvPlot* pPlot = NULL, const CvUnit* pAttacker = NULL) const						// Exposed to Python
	{
		return ((maxCombatStr(pPlot, pAttacker) + currCombatStr(pPlot, pAttacker) + 1) / 2);
	}
	int currEffectiveStr(CvPlot const* pPlot = NULL, CvUnit const* pAttacker = NULL,
			CombatDetails* pCombatDetails = NULL,
			int iCurrentHP = -1) const; // advc.139
	DllExport float maxCombatStrFloat(const CvPlot* pPlot, const CvUnit* pAttacker) const;					// Exposed to Python
	DllExport float currCombatStrFloat(const CvPlot* pPlot, const CvUnit* pAttacker) const;					// Exposed to Python
	// advc: was protected
	void getDefenderCombatValues(CvUnit const& kDefender, const CvPlot* pPlot,
			int iOurStrength, int iOurFirepower, int& iTheirOdds, int& iTheirStrength,
			int& iOurDamage, int& iTheirDamage, CombatDetails* pTheirDetails = NULL) const;

	DllExport bool canFight() const																			// Exposed to Python
	{
		return (baseCombatStr() > 0);
	}
	bool canSiege(TeamTypes eTeam) const;																	// Exposed to Python
	bool canCombat() const; // kekm.8
	bool canAttack() const;																					// Exposed to Python
	bool canAttack(const CvUnit& kDefender) const;
	bool canDefend(const CvPlot* pPlot = NULL) const;														// Exposed to Python
	// <advc>
	bool canBeAttackedBy(PlayerTypes eAttackingPlayer,
			CvUnit const* pAttacker, bool bTestEnemy, bool bTestPotentialEnemy,
			bool bTestVisible, bool bTestCanAttack) const; // </advc>
	bool isBetterDefenderThan(const CvUnit* pDefender, const CvUnit* pAttacker) const;						// Exposed to Python
	bool canDefendAgainst(const CvUnit* pAttacker, const CvPlot* pPlot = NULL) const; // doc

	int airBaseCombatStr() const																			// Exposed to Python
	{
		return m_pUnitInfo->getAirCombat();
	}
	int airMaxCombatStr(const CvUnit* pOther) const;														// Exposed to Python
	int airCurrCombatStr(const CvUnit* pOther) const														// Exposed to Python
	{
		return ((airMaxCombatStr(pOther) * currHitPoints()) / maxHitPoints());
	}
	DllExport float airMaxCombatStrFloat(const CvUnit* pOther) const;										// Exposed to Python
	DllExport float airCurrCombatStrFloat(const CvUnit* pOther) const;										// Exposed to Python
	int combatLimit() const																					// Exposed to Python
	{
		return m_pUnitInfo->getCombatLimit();
	}
	int combatLimitAgainst(const CvUnit* pUnit) const; // doc
	int airCombatLimit() const																				// Exposed to Python
	{
		return m_pUnitInfo->getAirCombatLimit();
	}
	DllExport bool canAirAttack() const																		// Exposed to Python
	{
		return (airBaseCombatStr() > 0);
	}
	bool canAirDefend(CvPlot const* pPlot = NULL) const;													// Exposed to Python
	int airCombatDamage(const CvUnit* pDefender) const;														// Exposed to Python
	int rangeCombatDamage(const CvUnit* pDefender) const;													// Exposed to Python
	CvUnit* bestInterceptor(CvPlot const& kPlot,															// Exposed to Python
			bool bOdds = false) const; // advc.004c
	CvUnit* bestSeaPillageInterceptor(CvUnit* pPillager, int iMinOdds) const;								// Exposed to Python

	bool isAutomated() const;																				// Exposed to Python
	DllExport bool isWaiting() const;																		// Exposed to Python
	bool isFortifyable() const;																				// Exposed to Python
	int fortifyModifier() const;																			// Exposed to Python

	int experienceNeeded() const;																			// Exposed to Python
	int attackXPValue() const;																				// Exposed to Python
	int defenseXPValue() const;																				// Exposed to Python
	int maxXPValue() const;																					// Exposed to Python

	int firstStrikes() const																				// Exposed to Python
	{
		return std::max(0, m_pUnitInfo->getFirstStrikes() + getExtraFirstStrikes());
	}
	int chanceFirstStrikes() const																			// Exposed to Python
	{
		return std::max(0, m_pUnitInfo->getChanceFirstStrikes() + getExtraChanceFirstStrikes());
	}
	int maxFirstStrikes() const { return firstStrikes() + chanceFirstStrikes(); }							// Exposed to Python
	DllExport bool isRanged() const;																		// Exposed to Python

	bool alwaysInvisible() const																			// Exposed to Python
	{
		return m_pUnitInfo->isInvisible();
	}
	bool immuneToFirstStrikes() const;																		// Exposed to Python
	bool noDefensiveBonus() const																			// Exposed to Python
	{
		return m_pUnitInfo->isNoDefensiveBonus();
	}
	bool ignoreBuildingDefense() const																		// Exposed to Python
	{
		return m_pUnitInfo->isIgnoreBuildingDefense();
	}
	bool canMoveImpassable() const																			// Exposed to Python
	{
		return m_pUnitInfo->canMoveImpassable();
	}
	bool canMoveAllTerrain() const																			// Exposed to Python
	{
		return m_pUnitInfo->isCanMoveAllTerrain();
	}
	bool flatMovementCost() const																			// Exposed to Python
	{	// advc.opt: Now also true for all air units
		return m_bFlatMovement;
	}
	bool ignoreTerrainCost() const																			// Exposed to Python
	{
		return m_pUnitInfo->isIgnoreTerrainCost();
	}
	bool isNeverInvisible() const;																			// Exposed to Python
	DllExport bool isInvisible(TeamTypes eTeam, bool bDebug, bool bCheckCargo = true) const;				// Exposed to Python
	bool isNukeImmune() const																				// Exposed to Python
	{
		return m_pUnitInfo->isNukeImmune();
	}

	int maxInterceptionProbability() const;																	// Exposed to Python
	int currInterceptionProbability() const;																// Exposed to Python
	int evasionProbability() const																			// Exposed to Python
	{
		return std::max(0, m_pUnitInfo->getEvasionProbability() + getExtraEvasion());
	}
	int withdrawalProbability() const;																		// Exposed to Python

	int collateralDamage() const																			// Exposed to Python
	{	// advc.159 (note): getExtraCollateralDamage works multiplicatively since BtS 3.17
		return std::max(0, m_pUnitInfo->getCollateralDamage());
	}
	int collateralDamageLimit() const																		// Exposed to Python
	{
		return std::max(0, m_pUnitInfo->getCollateralDamageLimit() * GC.getMAX_HIT_POINTS() / 100);
	}
	int collateralDamageMaxUnits() const																	// Exposed to Python
	{	// advc: Never negative in XML
		return /*std::max(0,*/m_pUnitInfo->getCollateralDamageMaxUnits();
	}

	int cityAttackModifier() const																			// Exposed to Python
	{
		return (m_pUnitInfo->getCityAttackModifier() + getExtraCityAttackPercent());
	}
	int cityDefenseModifier() const																			// Exposed to Python
	{
		return (m_pUnitInfo->getCityDefenseModifier() + getExtraCityDefensePercent());
	}
	int animalCombatModifier() const;																		// Exposed to Python
	int barbarianCombatModifier() const; // advc.315c
	int hillsAttackModifier() const;																		// Exposed to Python
	int hillsDefenseModifier() const;																		// Exposed to Python
	int plainsAttackModifier() const; // doc
	int plainsDefenseModifier() const; // doc
	int riverAttackModifier() const; // doc
	int terrainAttackModifier(TerrainTypes eTerrain) const;													// Exposed to Python
	int terrainDefenseModifier(TerrainTypes eTerrain) const;												// Exposed to Python
	int featureAttackModifier(FeatureTypes eFeature) const;													// Exposed to Python
	int featureDefenseModifier(FeatureTypes eFeature) const;												// Exposed to Python
	int unitClassAttackModifier(UnitClassTypes eUnitClass) const;											// Exposed to Python
	int unitClassDefenseModifier(UnitClassTypes eUnitClass) const;											// Exposed to Python
	int unitCombatModifier(UnitCombatTypes eUnitCombat) const;												// Exposed to Python
	int domainModifier(DomainTypes eDomain) const;															// Exposed to Python

	int bombardRate() const;																				// Exposed to Python
	int airBombBaseRate() const;																			// Exposed to Python
	int airBombCurrRate() const;																			// Exposed to Python

	SpecialUnitTypes specialCargo() const;																	// Exposed to Python
	DomainTypes domainCargo() const;																		// Exposed to Python
	int cargoSpace() const { return m_iCargoCapacity; }														// Exposed to Python
	void changeCargoSpace(int iChange);																		// Exposed to Python
	bool isFull() const { return (getCargo() >= cargoSpace()); }											// Exposed to Python
	int cargoSpaceAvailable(SpecialUnitTypes eSpecialCargo = NO_SPECIALUNIT,								// Exposed to Python
			DomainTypes eDomainCargo = NO_DOMAIN) const;
	bool hasCargo() const { return (getCargo() > 0); }														// Exposed to Python
	//bool canCargoAllMove() const; // disabled by K-Mod (was exposed to Python)
	bool canCargoEnterTerritory(TeamTypes eTeam, bool bIgnoreRightOfPassage,
			CvArea const& kArea) const;
	int getUnitAICargo(UnitAITypes eUnitAI) const;															// Exposed to Python

	static CvUnit* fromIDInfo(IDInfo id); // advc
	DllExport int getID() const { return m_iID; }															// Exposed to Python
	int getIndex() const { return (getID() & FLTA_INDEX_MASK); }
	DllExport IDInfo getIDInfo() const { return IDInfo(getOwner(), getID()); }
	void setID(int iID);

	int getGroupID() const { return m_iGroupID; }															// Exposed to Python
	// advc: I don't think a unit is ever supposed to not be in a group
	//bool isInGroup() const; // Exposed to Python ( advc: still available to Python; see CyUnit.cpp.)
	bool isGroupHead() const;																				// Exposed to Python
	CvSelectionGroup* getGroupExternal() const; // advc.003s: exported through .def file
	// <advc.003s> Should make loops over units in a group less hazardous
	CvSelectionGroup const* getGroup() const;
	CvSelectionGroup* getGroup();																			// Exposed to Python
	// </advc.003s>
	bool isBeforeUnitCycle(CvUnit const& kOther) const; // advc: Moved from CvGameCoreUtils
	bool canJoinGroup(const CvPlot* pPlot, CvSelectionGroup const* pSelectionGroup) const;
	void joinGroup(CvSelectionGroup* pSelectionGroup, bool bRemoveSelected = false, bool bRejoin = true);

	DllExport int getHotKeyNumber();																													// Exposed to Python
	void setHotKeyNumber(int iNewValue);																											// Exposed to Python

	DllExport int getX() const { return m_iX; } // advc.inl: was "getX_INLINE"								// Exposed to Python
	DllExport int getY() const { return m_iY; } // advc.inl: was "getY_INLINE"								// Exposed to Python
	void setXY(int iX, int iY, bool bGroup = false, bool bUpdate = true, bool bShow = false,				// Exposed to Python
			bool bCheckPlotVisible = false);

	bool at(int iX, int iY) const { return (getX() == iX && getY() == iY); }								// Exposed to Python
	bool at(CvPlot const& kPlot) const { return atPlot(&kPlot); }
	DllExport bool atPlot(const CvPlot* pPlot) const { return (plot() == pPlot); }							// Exposed to Python
	DllExport CvPlot* plot() const { return m_pPlot; } // advc.opt: cached									// Exposed to Python
	CvPlot& getPlot() const { return *m_pPlot; } // advc
	void updatePlot(); // advc.opt
	//int getArea() const;																					// Exposed to Python
	// <advc>
	CvArea& getArea() const { return *m_pArea; }
	CvArea* area() const { return m_pArea; }																// Exposed to Python
	bool isArea(CvArea const& kArea) const { return (area() == &kArea); }
	bool sameArea(CvUnit const& kOther) const { return (area() == kOther.area()); }
	void updateArea();
	// </advc>
	int getLastMoveTurn() const;
	void setLastMoveTurn(int iNewValue);

	CvPlot* getReconPlot() const;																			// Exposed to Python
	void setReconPlot(CvPlot* pNewValue);																	// Exposed to Python

	int getGameTurnCreated() const { return m_iGameTurnCreated; }											// Exposed to Python
	void setGameTurnCreated(int iNewValue);

	DllExport int getDamage() const { return m_iDamage; }													// Exposed to Python
	void setDamage(int iNewValue, PlayerTypes ePlayer = NO_PLAYER, bool bNotifyEntity = true);				// Exposed to Python
	void changeDamage(int iChange, PlayerTypes ePlayer = NO_PLAYER);										// Exposed to Python

	int getMoves() const { return m_iMoves; } // advc (note): Moves spent, not remaining.					// Exposed to Python
	void setMoves(int iNewValue);																			// Exposed to Python
	void changeMoves(int iChange);																			// Exposed to Python
	void finishMoves();																						// Exposed to Python

	int getExperience() const { return m_iExperience; }														// Exposed to Python
	void setExperience(int iNewValue, int iMax = -1);														// Exposed to Python
	void changeExperience(int iChange, int iMax = -1, bool bFromCombat = false,								// Exposed to Python
			bool bInBorders = false, //bool bUpdateGlobal = false
			int iGlobalPercent = 0); // advc.312
	int getGlobalXPPercent() const; // advc.312

	int getLevel() const { return m_iLevel; }																// Exposed to Python
	void setLevel(int iNewValue);
	void changeLevel(int iChange);

	int getCargo() const { return m_iCargo; }																// Exposed to Python
	void changeCargo(int iChange);
	void getCargoUnits(std::vector<CvUnit*>& aUnits) const;

	CvPlot* getAttackPlot() const;
	void setAttackPlot(const CvPlot* pNewValue, bool bAirCombat);
	bool isInAirCombat() const;

	DllExport int getCombatTimer() const;
	void setCombatTimer(int iNewValue);
	void changeCombatTimer(int iChange);

	int getCombatFirstStrikes() const;
	void setCombatFirstStrikes(int iNewValue);
	void changeCombatFirstStrikes(int iChange);

	int getFortifyTurns() const;																			// Exposed to Python
	void setFortifyTurns(int iNewValue);
	void changeFortifyTurns(int iChange);

	int getBlitzCount() const { return m_iBlitzCount; }
	bool isBlitz() const																					// Exposed to Python
	{
		return (getBlitzCount() != 0); // advc.164: was > 0
	}
	void changeBlitzCount(int iChange);

	int getAmphibCount() const { return m_iAmphibCount; }
	bool isAmphib() const { return (getAmphibCount() > 0); }												// Exposed to Python
	void changeAmphibCount(int iChange);

	int getRiverCount() const { return m_iRiverCount; }
	bool isRiver() const { return (getRiverCount() > 0); }													// Exposed to Python
	void changeRiverCount(int iChange);

	int getEnemyRouteCount() const { return m_iEnemyRouteCount; }
	bool isEnemyRoute() const { return (getEnemyRouteCount() > 0); }										// Exposed to Python
	void changeEnemyRouteCount(int iChange);

	int getAlwaysHealCount() const { return m_iAlwaysHealCount; }
	bool isAlwaysHeal() const;																				// Exposed to Python
	void changeAlwaysHealCount(int iChange);

	int getHillsDoubleMoveCount() const { return m_iHillsDoubleMoveCount; }
	bool isHillsDoubleMove() const { return (getHillsDoubleMoveCount() > 0); }								// Exposed to Python
	void changeHillsDoubleMoveCount(int iChange);

	int getImmuneToFirstStrikesCount() const { return m_iImmuneToFirstStrikesCount; }
	void changeImmuneToFirstStrikesCount(int iChange);

	int getNoUpgradeCount() const { return m_iNoUpgradeCount; } // doc
	bool isNoUpgrade() const { return getNoUpgradeCount() > 0; } // doc
	void changeNoUpgradeCount(int iChange); // doc

	int getExtraVisibilityRange() const { return m_iExtraVisibilityRange; }									// Exposed to Python
	void changeExtraVisibilityRange(int iChange);

	int getExtraMoves() const { return m_iExtraMoves; }														// Exposed to Python
	void changeExtraMoves(int iChange);

	int getExtraMoveDiscount() const { return m_iExtraMoveDiscount; }										// Exposed to Python
	void changeExtraMoveDiscount(int iChange);

	int getExtraAirRange() const;																			// Exposed to Python
	void changeExtraAirRange(int iChange);

	int getExtraIntercept() const;																			// Exposed to Python
	void changeExtraIntercept(int iChange);

	int getExtraEvasion() const;																			// Exposed to Python
	void changeExtraEvasion(int iChange);

	int getExtraFirstStrikes() const { return m_iExtraFirstStrikes; }										// Exposed to Python
	void changeExtraFirstStrikes(int iChange);

	int getExtraChanceFirstStrikes() const { return m_iExtraChanceFirstStrikes; }							// Exposed to Python
	void changeExtraChanceFirstStrikes(int iChange);

	int getExtraWithdrawal() const { return m_iExtraWithdrawal; }											// Exposed to Python
	void changeExtraWithdrawal(int iChange);

	int getExtraCollateralDamage() const { return m_iExtraCollateralDamage; }								// Exposed to Python
	void changeExtraCollateralDamage(int iChange);

	int getExtraBombardRate() const { return m_iExtraBombardRate; }											// Exposed to Python
	void changeExtraBombardRate(int iChange);

	int getExtraEnemyHeal() const;																			// Exposed to Python
	void changeExtraEnemyHeal(int iChange);

	int getExtraNeutralHeal() const;																		// Exposed to Python
	void changeExtraNeutralHeal(int iChange);

	int getExtraFriendlyHeal() const;																		// Exposed to Python
	void changeExtraFriendlyHeal(int iChange);

	int getSameTileHeal() const;																			// Exposed to Python
	void changeSameTileHeal(int iChange);

	int getAdjacentTileHeal() const;																		// Exposed to Python
	void changeAdjacentTileHeal(int iChange);

	int getExtraCombatPercent() const { return m_iExtraCombatPercent; }										// Exposed to Python
	void changeExtraCombatPercent(int iChange);

	int getExtraCityAttackPercent() const { return m_iExtraCityAttackPercent; }								// Exposed to Python
	void changeExtraCityAttackPercent(int iChange);

	int getExtraCityDefensePercent() const { return m_iExtraCityDefensePercent; }							// Exposed to Python
	void changeExtraCityDefensePercent(int iChange);

	int getExtraHillsAttackPercent() const { return m_iExtraHillsAttackPercent; }							// Exposed to Python
	void changeExtraHillsAttackPercent(int iChange);

	int getExtraHillsDefensePercent() const { return m_iExtraHillsDefensePercent; }							// Exposed to Python
	void changeExtraHillsDefensePercent(int iChange);

	int getExtraPlainsAttackPercent() const; // doc
	void changeExtraPlainsAttackPercent(int iChange); // doc

	int getExtraPlainsDefensePercent() const; // doc
	void changeExtraPlainsDefensePercent(int iChange); // doc

	int getExtraRiverAttackPercent() const; // doc
	void changeExtraRiverAttackPercent(int iChange); // doc

	int getRevoltProtection() const;																		// Exposed to Python
	void changeRevoltProtection(int iChange);

	int getCollateralDamageProtection() const;																// Exposed to Python
	void changeCollateralDamageProtection(int iChange);

	int getPillageChange() const;																			// Exposed to Python
	void changePillageChange(int iChange);

	int getUpgradeDiscount() const;																			// Exposed to Python
	void changeUpgradeDiscount(int iChange);

	int getExperiencePercent() const;																		// Exposed to Python
	void changeExperiencePercent(int iChange);

	int getKamikazePercent() const;																			// Exposed to Python
	void changeKamikazePercent(int iChange);

	int getExtraUpkeep() const; // doc
	void changeExtraUpkeep(int iChange); // doc

	DllExport DirectionTypes getFacingDirection(bool bCheckLineOfSightProperty) const;
	void setFacingDirection(DirectionTypes facingDirection);
	void rotateFacingDirectionClockwise();
	void rotateFacingDirectionCounterClockwise();

	DllExport bool isSuicide() const;																		// Exposed to Python
	int getDropRange() const { return m_pUnitInfo->getDropRange(); }

	bool isMadeAttack() const																				// Exposed to Python
	{
		//return m_bMadeAttack;
		// advc.164: Keep the boolean interface in place
		return (m_iMadeAttacks > 0);
	}
	void setMadeAttack(bool bNewValue);																		// Exposed to Python
	bool isMadeAllAttacks() const; // advc.164

	bool isMadeInterception() const																			// Exposed to Python
	{
		return m_bMadeInterception;
	}
	void setMadeInterception(bool bNewValue);																// Exposed to Python

	bool isPromotionReadyExternal() const; // advc.002e: exported through .def file
	bool isPromotionReady() const { return m_bPromotionReady; }												// Exposed to Python
	void setPromotionReady(bool bNewValue);																	// Exposed to Python
	void testPromotionReady();

	bool isDelayedDeath() const { return m_bDeathDelay; }
	void startDelayedDeath();
	bool doDelayedDeath();

	bool isCombatFocus() const;

	DllExport bool isInfoBarDirty() const;
	DllExport void setInfoBarDirty(bool bNewValue);

	bool isBlockading() const
	{
		return m_bBlockading;
	}
	void setBlockading(bool bNewValue);
	void collectBlockadeGold();

	DllExport PlayerTypes getOwner() const // advc.inl: was "getOwnerINLINE"								// Exposed to Python
	{
		return m_eOwner;
	}
	DllExport PlayerTypes getVisualOwner(TeamTypes eForTeam = NO_TEAM) const;								// Exposed to Python
	PlayerTypes getCombatOwner(TeamTypes eForTeam, CvPlot const& kPlot) const								// Exposed to Python
	{
		// advc.inl: Split this function up so that part of it can be inlined
		return (isAlwaysHostile() ? getCombatOwner_bulk(eForTeam, kPlot) : getOwner());
	}
	// advc (for convenience)
	PlayerTypes getCombatOwner(TeamTypes eForTeam) const
	{
		return getCombatOwner(eForTeam, getPlot());
	}
	DllExport TeamTypes getTeam() const;																	// Exposed to Python
	// <advc>
	bool isActiveOwned() const { return (GC.getInitCore().getActivePlayer() == getOwner()); }
	bool isActiveTeam() const { return (GC.getInitCore().getActiveTeam() == getTeam()); } // </advc>

	PlayerTypes getCapturingPlayer() const;
	void setCapturingPlayer(PlayerTypes eNewValue);

	DllExport const UnitTypes getUnitType() const { return m_eUnitType; }									// Exposed to Python
	CvUnitInfo& getUnitInfo() const { return *m_pUnitInfo; }
	UnitClassTypes getUnitClassType() const	// Exposed to Python
	{
		return m_pUnitInfo->getUnitClassType();
	}

	DllExport const UnitTypes getLeaderUnitType() const
	{
		return m_eLeaderUnitType;
	}
	void setLeaderUnitType(UnitTypes leaderUnitType);

	DllExport CvUnit* getCombatUnit() const;
	void setCombatUnit(CvUnit* pUnit, bool bAttacking = false);
	bool showSiegeTower(CvUnit* pDefender) const; // K-Mod

	CvUnit const* getTransportUnit() const;																	// Exposed to Python
	CvUnit* getTransportUnit(); // advc
	bool isCargo() const																					// Exposed to Python
	{	// advc.test: (Should perhaps simply turn m_transportUnit into a CvUnit pointer.)
		//FAssert((getTransportUnit() == NULL) == (m_transportUnit.iID == NO_PLAYER));
		return (m_transportUnit.iID != NO_PLAYER); // advc.opt: avoid ::getUnit call
	}
	void setTransportUnit(CvUnit* pTransportUnit);															// Exposed to Python

	int getExtraDomainModifier(DomainTypes eDomain) const													// Exposed to Python
	{
		return m_aiExtraDomainModifier.get(eDomain);
	}
	void changeExtraDomainModifier(DomainTypes eDomain, int iChange);

	DllExport const CvWString getName(uint uiForm = 0) const;												// Exposed to Python
	CvWString const getReplayName() const; // advc.106
	const wchar* getNameKey() const;																		// Exposed to Python
	wchar const* getNameKeyNoGG() const; // advc.004u
	const CvWString& getNameNoDesc() const;																	// Exposed to Python
	void setName(const CvWString szNewValue);																// Exposed to Python

	// Script data needs to be a narrow string for pickling in Python
	std::string getScriptData() const;																		// Exposed to Python
	void setScriptData(std::string szNewValue);																// Exposed to Python

	int getTerrainDoubleMoveCount(TerrainTypes eTerrain) const
	{
		return m_aiTerrainDoubleMoveCount.get(eTerrain);
	}
	bool isTerrainDoubleMove(TerrainTypes eTerrain) const													// Exposed to Python
	{
		return (getTerrainDoubleMoveCount(eTerrain) > 0);
	}
	void changeTerrainDoubleMoveCount(TerrainTypes eTerrain, int iChange);

	int getFeatureDoubleMoveCount(FeatureTypes eFeature) const
	{
		return m_aiFeatureDoubleMoveCount.get(eFeature);
	}
	bool isFeatureDoubleMove(FeatureTypes eFeature) const													// Exposed to Python
	{
		return (getFeatureDoubleMoveCount(eFeature) > 0);
	}
	void changeFeatureDoubleMoveCount(FeatureTypes eFeature, int iChange);

	int getExtraTerrainAttackPercent(TerrainTypes eTerrain) const											// Exposed to Python
	{
		return m_aiExtraTerrainAttackPercent.get(eTerrain);
	}
	void changeExtraTerrainAttackPercent(TerrainTypes eTerrain, int iChange);
	int getExtraTerrainDefensePercent(TerrainTypes eTerrain) const											// Exposed to Python
	{
		return m_aiExtraTerrainDefensePercent.get(eTerrain);
	}
	void changeExtraTerrainDefensePercent(TerrainTypes eTerrain, int iChange);
	int getExtraFeatureAttackPercent(FeatureTypes eFeature) const											// Exposed to Python
	{
		return m_aiExtraFeatureAttackPercent.get(eFeature);
	}
	void changeExtraFeatureAttackPercent(FeatureTypes eFeature, int iChange);
	int getExtraFeatureDefensePercent(FeatureTypes eFeature) const											// Exposed to Python
	{
		return m_aiExtraFeatureDefensePercent.get(eFeature);
	}
	void changeExtraFeatureDefensePercent(FeatureTypes eFeature, int iChange);

	int getExtraUnitCombatModifier(UnitCombatTypes eUnitCombat) const										// Exposed to Python
	{
		return m_aiExtraUnitCombatModifier.get(eUnitCombat);
	}
	void changeExtraUnitCombatModifier(UnitCombatTypes eUnitCombat, int iChange);

	bool canAcquirePromotion(PromotionTypes ePromotion) const;												// Exposed to Python
	bool canAcquirePromotionAny() const;																	// Exposed to Python
	bool isPromotionValid(PromotionTypes ePromotion) const;													// Exposed to Python
	bool isHasPromotion(PromotionTypes ePromotion) const													// Exposed to Python
	{
		return m_abHasPromotion.get(ePromotion);
	}
	void setHasPromotion(PromotionTypes ePromotion, bool bNewValue);										// Exposed to Python

	int getSubUnitCount() const;
	DllExport int getSubUnitsAlive() const;
	int getSubUnitsAlive(int iDamage) const;

	bool isTargetOf(CvUnit const& kAttacker) const;
	bool isEnemy(TeamTypes eTeam, CvPlot const& kPlot) const;
	// advc.opt: Instead of allowing pPlot==NULL
	__inline bool isEnemy(TeamTypes eTeam) const
	{
		return isEnemy(eTeam, getPlot());
	}
	// advc.opt: Instead of allowing eTeam==NO_TEAM above
	bool isEnemy(CvPlot const& kPlot) const;
	// (advc: isPotentialEnemy moved to CvUnitAI)

	bool canRangeStrike() const;
	bool canRangeStrikeAt(const CvPlot* pPlot, int iX, int iY) const;
	bool rangeStrike(int iX, int iY);

	int getTriggerValue(EventTriggerTypes eTrigger, const CvPlot* pPlot, bool bCheckPlot) const;
	bool canApplyEvent(EventTypes eEvent) const;
	void applyEvent(EventTypes eEvent);

	int getImmobileTimer() const;																			// Exposed to Python
	void setImmobileTimer(int iNewValue);																	// Exposed to Python
	void changeImmobileTimer(int iChange);

	// (advc: potentialWarAction has become CvUnitAI::AI_mayAttack(CvPlot const&))
	bool willRevealAnyPlotFrom(CvPlot const& kFrom) const;
	bool isAlwaysHostile(CvPlot const& kPlot) const;
	// advc.opt: Faster version for unknown plot
	bool isAlwaysHostile() const
	{
		return m_pUnitInfo->isAlwaysHostile();
	}

	bool verifyStackValid();

	bool canTradeUnit(PlayerTypes eReceivingPlayer); // doc (edead, Afforess)
	void tradeUnit(PlayerTypes eReceivingPlayer); // doc (edead, Afforess)

	SpecialistTypes getSettledSpecialist() const; // doc

	RegionTypes getOriginalRegion() const { return m_eOriginalRegion; } // doc

	DllExport const CvArtInfoUnit* getArtInfo(int i, EraTypes eEra) const;									// Exposed to Python
	DllExport const TCHAR* getButton() const;																// Exposed to Python
	DllExport int getGroupSize() const;
	DllExport int getGroupDefinitions() const;
	DllExport int getUnitGroupRequired(int i) const;
	DllExport bool isRenderAlways() const;
	DllExport float getAnimationMaxSpeed() const;
	DllExport float getAnimationPadTime() const;
	DllExport const char* getFormationType() const;
	DllExport bool isMechUnit() const;
	DllExport bool isRenderBelowWater() const;
	DllExport int getRenderPriority(UnitSubEntityTypes eUnitSubEntity, int iMeshGroupType, int UNIT_MAX_SUB_TYPES) const;

	DllExport bool shouldShowEnemyGlow(TeamTypes eForTeam) const;
	DllExport bool shouldShowFoundBorders() const;

	DllExport void cheat(bool bCtrl, bool bAlt, bool bShift);
	DllExport float getHealthBarModifier() const;
	DllExport void getLayerAnimationPaths(std::vector<AnimationPathTypes>& aAnimationPaths) const;
	DllExport int getSelectionSoundScript() const;

	bool isWorker() const; // advc.154  (Exposed to Python)

	bool isBetterDefenderThan(const CvUnit* pDefender, const CvUnit* pAttacker,
	// Lead From Behind (UncutDragon, edited for K-Mod): START
			int* pBestDefenderRank,
			bool bPreferUnowned = false) const; // advc.061
	int LFBgetAttackerRank(const CvUnit* pDefender, int& iUnadjustedRank) const;
	int LFBgetDefenderRank(const CvUnit* pAttacker) const;
	// unprotected by K-Mod. (I want to use the LFB value for some AI stuff)
	int LFBgetDefenderOdds(const CvUnit* pAttacker) const;
	int LFBgetValueAdjustedOdds(int iOdds, bool bDefender) const;
	int LFBgetRelativeValueRating() const;
	int LFGgetDefensiveValueAdjustment() const; // K-Mod
	bool LFBisBetterDefenderThan(const CvUnit* pDefender, const CvUnit* pAttacker, int* pBestDefenderRank) const;
	// (advc: LFBgetDefenderCombatOdds deleted, use 1000 minus calculateCombatOdds instead.)
	// Lead From Behind: END

	// <advc.003u>
	// virtual for FFreeListTrashArray
	virtual void read(FDataStreamBase* pStream);
	virtual void write(FDataStreamBase* pStream);
	CvUnitAI& AI()
	{	//return *static_cast<CvUnitAI*>(const_cast<CvUnit*>(this));
		/*  The above won't work in an inline function b/c the compiler doesn't know
			that CvUnitAI is derived from CvUnit */
		return *reinterpret_cast<CvUnitAI*>(this);
	}
	CvUnitAI const& AI() const
	{	//return *static_cast<CvUnitAI const*>(this);
		return *reinterpret_cast<CvUnitAI const*>(this);
	}
	/*  Keep one pure virtual function to make the class abstract; remove all
		the others - the EXE doesn't call them. */ // </advc.003u>
	virtual UnitAITypes AI_getUnitAIType() const = 0;

protected:
	// <advc.003u>
	CvUnit();
	/*  Subclasses need to call these two init functions; not called by base.
		May also want to override them. */
	virtual void init(int iID, UnitTypes eUnit, PlayerTypes eOwner, int iX, int iY,
			DirectionTypes eFacingDirection);
	virtual void finalizeInit(); // </advc.003u>

	int m_iID;
	int m_iGroupID;
	// <advc> Moved up for easier access in debugger
	PlayerTypes m_eOwner;
	CvUnitInfo *m_pUnitInfo; // </advc>
	int m_iX;
	int m_iY;
	int m_iLastMoveTurn;
	int m_iReconX;
	int m_iReconY;
	int m_iLastReconTurn; // advc.029
	int m_iGameTurnCreated;
	int m_iHotKeyNumber;
	int m_iDamage;
	int m_iMoves;
	int m_iExperience;
	int m_iLevel;
	int m_iCargo;
	int m_iCargoCapacity;
	int m_iAttackPlotX;
	int m_iAttackPlotY;
	// <advc.048c>
	int m_iAttackOdds;
	int m_iPreCombatHP; // </advc.048c>
	int m_iCombatTimer;
	int m_iCombatFirstStrikes;
	//int m_iCombatDamage; // advc.003j: unused
	int m_iFortifyTurns;
	int m_iBlitzCount;
	int m_iAmphibCount;
	int m_iRiverCount;
	int m_iEnemyRouteCount;
	int m_iAlwaysHealCount;
	int m_iHillsDoubleMoveCount;
	int m_iImmuneToFirstStrikesCount;
	int m_iNoUpgradeCount; // doc
	int m_iExtraVisibilityRange;
	int m_iExtraMoves;
	int m_iExtraMoveDiscount;
	int m_iExtraAirRange;
	int m_iExtraIntercept;
	int m_iExtraEvasion;
	int m_iExtraFirstStrikes;
	int m_iExtraChanceFirstStrikes;
	int m_iExtraWithdrawal;
	int m_iExtraCollateralDamage;
	int m_iExtraBombardRate;
	int m_iExtraEnemyHeal;
	int m_iExtraNeutralHeal;
	int m_iExtraFriendlyHeal;
	int m_iSameTileHeal;
	int m_iAdjacentTileHeal;
	int m_iExtraCombatPercent;
	int m_iExtraCityAttackPercent;
	int m_iExtraCityDefensePercent;
	int m_iExtraHillsAttackPercent;
	int m_iExtraHillsDefensePercent;
	int m_iExtraPlainsAttackPercent; // doc
	int m_iExtraPlainsDefensePercent; // doc
	int m_iExtraRiverAttackPercent; // doc
	int m_iRevoltProtection;
	int m_iCollateralDamageProtection;
	int m_iPillageChange;
	int m_iUpgradeDiscount;
	int m_iExperiencePercent;
	int m_iKamikazePercent;
	int m_iBaseCombat;
	DirectionTypes m_eFacingDirection;
	int m_iImmobileTimer;
	int m_iExtraUpkeep; // doc
	RegionTypes m_eOriginalRegion; // doc

	//bool m_bMadeAttack;
	int m_iMadeAttacks; // advc.164
	// advc.opt: Bitfields - since we have exactly 8 booleans ...
	bool m_bMadeInterception:1;
	bool m_bPromotionReady:1;
	bool m_bDeathDelay:1;
	bool m_bCombatFocus:1;
	bool m_bInfoBarDirty:1;
	bool m_bBlockading:1;
	bool m_bAirCombat:1;
	bool m_bFlatMovement:1; // advc.opt

	PlayerTypes m_eCapturingPlayer;
	UnitTypes m_eUnitType;
	UnitTypes m_eLeaderUnitType;
	// <advc.opt>
	CvArea* m_pArea;
	CvPlot* m_pPlot; // </advc.opt>
	// advc (note): These aren't CvUnit pointers b/c of the order of deserialization
	IDInfo m_combatUnit;
	IDInfo m_transportUnit;
	/*	advc.opt (tbd.): string objects take up 28 byte each; replace with pointers.
		May also want to replace most of the ints with short. That would cut
		the total size of this class in half. */
	CvWString m_szName;
	CvString m_szScriptData;

	// <advc.enum>
	ArrayEnumMap<PromotionTypes,bool> m_abHasPromotion;
	ArrayEnumMap<DomainTypes,int,short> m_aiExtraDomainModifier;
	ArrayEnumMap<TerrainTypes,int,short> m_aiTerrainDoubleMoveCount;
	ArrayEnumMap<TerrainTypes,int,short> m_aiExtraTerrainAttackPercent;
	ArrayEnumMap<TerrainTypes,int,short> m_aiExtraTerrainDefensePercent;
	ArrayEnumMap<FeatureTypes,int,short> m_aiFeatureDoubleMoveCount;
	ArrayEnumMap<FeatureTypes,int,short> m_aiExtraFeatureAttackPercent;
	ArrayEnumMap<FeatureTypes,int,short> m_aiExtraFeatureDefensePercent;
	ArrayEnumMap<UnitCombatTypes,int,short> m_aiExtraUnitCombatModifier;
	// </advc.enum>

	PlayerTypes getCombatOwner_bulk(TeamTypes eForTeam, CvPlot const& kPlot) const; // advc
	// <advc.111>
	bool pillageImprovement();
	bool pillageRoute();
	// </advc.111>
	bool canAdvance(const CvPlot* pPlot, int iThreshold) const;
	void collateralCombat(const CvPlot* pPlot, CvUnit const* pSkipUnit = NULL);
	void flankingStrikeCombat(const CvPlot* pPlot, int iAttackerStrength,
			int iAttackerFirepower, int iDefenderOdds, int iDefenderDamage,
			CvUnit const* pSkipUnit = NULL);

	bool interceptTest(CvPlot const& kPlot, /* advc.004c: */ IDInfo* pInterceptorID = NULL);
	CvUnit* airStrikeTarget(CvPlot const& kPlot) const;
	bool airStrike(CvPlot& kPlot, /* advc.004c: */ bool* pbIntercepted = NULL);

	int planBattle(CvBattleDefinition& kBattle,
			const std::vector<int>& combat_log) const; // K-Mod
	int computeUnitsToDie(const CvBattleDefinition & kDefinition, bool bRanged,
			BattleUnitTypes iUnit) const;
	bool verifyRoundsValid(const CvBattleDefinition & battleDefinition) const;
	void increaseBattleRounds(CvBattleDefinition & battleDefinition) const;
	int computeWaveSize(bool bRangedRound, int iAttackerMax, int iDefenderMax) const;
	bool isCombatVisible(const CvUnit* pDefender,
			bool bSeaPatrol = false) const; // advc.004k
	//void resolveCombat(CvUnit* pDefender, CvPlot* pPlot, CvBattleDefinition& kBattle);
	void resolveCombat(CvUnit* pDefender, CvPlot* pPlot, bool bVisible); // K-Mod
	void addAttackSuccessMessages(CvUnit const& kDefender, bool bFought) const; // advc.010
	void addDefenseSuccessMessages(CvUnit const& kDefender) const; // advc
	void addWithdrawalMessages(CvUnit const& kDefender) const; // advc
	// <advc.048c>
	void setHasBeenDefendedAgainstMessage(CvWString& kBuffer, CvUnit const& kDefender,
			int iAttackSuccess) const; // </advc.048c>
	bool suppressStackAttackSound(CvUnit const& kDefender) const; // advc.002l
	void resolveAirCombat(CvUnit* pInterceptor, CvPlot* pPlot, CvAirMissionDefinition& kBattle);
	void checkRemoveSelectionAfterAttack();
	void updateFlatMovement();
// <advc.003u>

	UnitArtStyleTypes getOriginalArtStyle() const; // doc
private:
	void uninitEntity(); // I don't think subclasses should ever call this
	// </advc.003u>
};

// advc: Moved from the beginning of the file
struct CombatDetails											// Exposed to Python
{
	int iExtraCombatPercent;
	/*	advc.313 (note): Not sure what these suffixes are supposed to abbreviate.
		I'll be assuming "T" for "This", meaning the defender, and then:
		"TA" = "This is Animal", "AA" = "Attacker is Animal",
		"TB" = "This is Barbarian", "AB" = "Attacker is Barbarian". */
	int iAnimalCombatModifierTA;
	int iAIAnimalCombatModifierTA;
	int iAnimalCombatModifierAA;
	int iAIAnimalCombatModifierAA;
	int iBarbarianCombatModifierTB;
	int iAIBarbarianCombatModifierTB;
	int iBarbarianCombatModifierAB;
	int iAIBarbarianCombatModifierAB;
	// <advc.313>
	int iBarbarianCityAttackModifier;
	int iSeaBarbarianModifierTB;
	int iSeaBarbarianModifierAB; // </advc.313>
	int iPlotDefenseModifier;
	int iFortifyModifier;
	int iCityDefenseModifier;
	int iHillsAttackModifier;
	int iHillsDefenseModifier;
	int iPlainsAttackModifier; // doc
	int iPlainsDefenseModifier; // doc
	int iFeatureAttackModifier;
	int iFeatureDefenseModifier;
	int iTerrainAttackModifier;
	int iTerrainDefenseModifier;
	int iCityAttackModifier;
	int iDomainDefenseModifier;
	//int iCityBarbarianDefenseModifier; // advc.313: replaced above
	int iClassDefenseModifier;
	int iClassAttackModifier;
	int iCombatModifierT;
	int iCombatModifierA;
	int iDomainModifierA;
	int iDomainModifierT;
	int iAnimalCombatModifierA;
	int iAnimalCombatModifierT;
	int iRiverAttackModifier;
	int iAmphibAttackModifier;
	int iKamikazeModifier;
	int iModifierTotal;
	int iBaseCombatStr;
	int iCombat;
	int iMaxCombatStr;
	int iCurrHitPoints;
	int iMaxHitPoints;
	int iCurrCombatStr;
	PlayerTypes eOwner;
	PlayerTypes eVisualOwner;
	std::wstring sUnitName;
	// advc:
	void reset(PlayerTypes eOwner, PlayerTypes eVisualOwner, std::wstring sUnitName)
	{
		/*	Not nice - but we mustn't zero the string, and we don't want to
			repeat all the int members. */
		ZeroMemory(this, 41 * sizeof(int));
		//BOOST_STATIC_ASSERT(sizeof(CombatDetails) == 41 * sizeof(int) + 2 * sizeof(PlayerTypes) + sizeof(std::wstring));
		this->eOwner = eOwner;
		this->eVisualOwner = eVisualOwner;
		this->sUnitName = sUnitName;
	}
};

#endif
