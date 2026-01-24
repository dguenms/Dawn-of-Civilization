#pragma once

// unit.h

#ifndef CIV4_UNIT_H
#define CIV4_UNIT_H

#include "CvDLLEntity.h"
//#include "CvEnums.h"
//#include "CvStructs.h"

#pragma warning( disable: 4251 )		// needs to have dll-interface to be used by clients of class

class CvPlot;
class CvArea;
class CvUnitInfo;
class CvSelectionGroup;
class FAStarNode;
class CvArtInfoUnit;

struct DllExport CombatDetails					// Exposed to Python
{
	int iExtraCombatPercent;
	int iAnimalCombatModifierTA;
	int iAIAnimalCombatModifierTA;
	int iAnimalCombatModifierAA;
	int iAIAnimalCombatModifierAA;
	int iBarbarianCombatModifierTB;
	int iAIBarbarianCombatModifierTB;
	int iBarbarianCombatModifierAB;
	int iAIBarbarianCombatModifierAB;
	int iPlotDefenseModifier;
	int iFortifyModifier;
	int iCityDefenseModifier;
	int iHillsAttackModifier;
	int iHillsDefenseModifier;
	int iFeatureAttackModifier;
	int iFeatureDefenseModifier;
	int iTerrainAttackModifier;
	int iTerrainDefenseModifier;
	int iCityAttackModifier;
	int iDomainDefenseModifier;
	int iCityBarbarianDefenseModifier;
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
};

class CvUnit : public CvDLLEntity
{

public:

	CvUnit();
	virtual ~CvUnit();
	
	void reloadEntity();
	void init(int iID, UnitTypes eUnit, UnitAITypes eUnitAI, PlayerTypes eOwner, int iX, int iY, DirectionTypes eFacingDirection);
	void uninit();
	void reset(int iID = 0, UnitTypes eUnit = NO_UNIT, PlayerTypes eOwner = NO_PLAYER, bool bConstructorCall = false);
	void setupGraphical();

	void convert(CvUnit* pUnit);																																	// Exposed to Python
	void kill(bool bDelay, PlayerTypes ePlayer = NO_PLAYER);														// Exposed to Python

	DllExport void NotifyEntity(MissionTypes eMission);

	void doTurn();

	void updateCombat(bool bQuick = false);
	void updateAirCombat(bool bQuick = false);
	void updateAirStrike(CvPlot* pPlot, bool bQuick, bool bFinish);

	bool isActionRecommended(int iAction);

	bool isBetterDefenderThan(const CvUnit* pDefender, const CvUnit* pAttacker) const;						// Exposed to Python 

	bool canDoCommand(CommandTypes eCommand, int iData1, int iData2, bool bTestVisible = false, bool bTestBusy = true);	// Exposed to Python
	void doCommand(CommandTypes eCommand, int iData1, int iData2);																// Exposed to Python

	FAStarNode* getPathLastNode() const;
	CvPlot* getPathEndTurnPlot() const;																																						// Exposed to Python
	bool generatePath(const CvPlot* pToPlot, int iFlags = 0, bool bReuse = false, int* piPathTurns = NULL) const;	// Exposed to Python

	bool canEnterTerritory(TeamTypes eTeam, bool bIgnoreRightOfPassage = false) const;						// Exposed to Python
	bool canEnterArea(TeamTypes eTeam, const CvArea* pArea, bool bIgnoreRightOfPassage = false) const;						// Exposed to Python
	TeamTypes getDeclareWarMove(const CvPlot* pPlot) const;															// Exposed to Python
	bool canMoveInto(const CvPlot* pPlot, bool bAttack = false, bool bDeclareWar = false, bool bIgnoreLoad = false) const;	// Exposed to Python
	bool canMoveOrAttackInto(const CvPlot* pPlot, bool bDeclareWar = false) const;								// Exposed to Python
	bool canMoveThrough(const CvPlot* pPlot) const;																								// Exposed to Python
	void attack(CvPlot* pPlot, bool bQuick);
	void attackForDamage(CvUnit *pDefender, int attackerDamageChange, int defenderDamageChange);
	void fightInterceptor(const CvPlot* pPlot, bool bQuick);
	void move(CvPlot* pPlot, bool bShow);
	bool jumpToNearestValidPlot();																																// Exposed to Python

	bool canAutomate(AutomateTypes eAutomate) const;																							// Exposed to Python
	void automate(AutomateTypes eAutomate);

	bool canScrap() const;																																				// Exposed to Python
	void scrap();

	bool canGift(bool bTestVisible = false, bool bTestTransport = true);																											// Exposed to Python 
	void gift(bool bTestTransport = true);

	bool canLoadUnit(const CvUnit* pUnit, const CvPlot* pPlot) const;															// Exposed to Python
	void loadUnit(CvUnit* pUnit);

	bool canLoad(const CvPlot* pPlot) const;																											// Exposed to Python
	void load();
	bool shouldLoadOnMove(const CvPlot* pPlot) const;

	bool canUnload() const;																																				// Exposed to Python
	void unload();

	bool canUnloadAll() const;																																		// Exposed to Python
	void unloadAll();

	bool canHold(const CvPlot* pPlot) const;																											// Exposed to Python
	bool canSleep(const CvPlot* pPlot) const;																						// Exposed to Python
	bool canFortify(const CvPlot* pPlot) const;																					// Exposed to Python
	bool canAirPatrol(const CvPlot* pPlot) const;																									// Exposed to Python
	void airCircle(bool bStart);

	bool canSeaPatrol(const CvPlot* pPlot) const;																									// Exposed to Python

	bool canHeal(const CvPlot* pPlot) const;																											// Exposed to Python
	bool canSentry(const CvPlot* pPlot) const;																										// Exposed to Python

	int healRate(const CvPlot* pPlot) const;
	int healTurns(const CvPlot* pPlot) const;
	void doHeal();

	bool canAirlift(const CvPlot* pPlot) const;																										// Exposed to Python
	bool canAirliftAt(const CvPlot* pPlot, int iX, int iY) const;																	// Exposed to Python
	bool airlift(int iX, int iY);

	bool isNukeVictim(const CvPlot* pPlot, TeamTypes eTeam) const;																// Exposed to Python
	bool canNuke(const CvPlot* pPlot) const;																											// Exposed to Python
	bool canNukeAt(const CvPlot* pPlot, int iX, int iY) const;																		// Exposed to Python
	bool nuke(int iX, int iY);

	bool canRecon(const CvPlot* pPlot) const;																											// Exposed to Python
	bool canReconAt(const CvPlot* pPlot, int iX, int iY) const;																		// Exposed to Python
	bool recon(int iX, int iY);

	bool canAirBomb(const CvPlot* pPlot) const;																										// Exposed to Python
	bool canAirBombAt(const CvPlot* pPlot, int iX, int iY) const;																	// Exposed to Python
	bool airBomb(int iX, int iY);

	CvCity* bombardTarget(const CvPlot* pPlot) const;																							// Exposed to Python
	bool canBombard(const CvPlot* pPlot) const;																										// Exposed to Python
	bool bombard();

	bool canParadrop(const CvPlot* pPlot) const;																											// Exposed to Python
	bool canParadropAt(const CvPlot* pPlot, int iX, int iY) const;																		// Exposed to Python
	bool paradrop(int iX, int iY);

	bool canPillage(const CvPlot* pPlot) const;																										// Exposed to Python
	bool pillage();

	bool canPlunder(const CvPlot* pPlot, bool bTestVisible = false) const;																					// Exposed to Python
	bool plunder();
	void updatePlunder(int iChange, bool bUpdatePlotGroups);

	int sabotageCost(const CvPlot* pPlot) const;																									// Exposed to Python
	int sabotageProb(const CvPlot* pPlot, ProbabilityTypes eProbStyle = PROBABILITY_REAL) const;	// Exposed to Python
	bool canSabotage(const CvPlot* pPlot, bool bTestVisible = false) const;												// Exposed to Python
	bool sabotage();

	int destroyCost(const CvPlot* pPlot) const;																										// Exposed to Python
	int destroyProb(const CvPlot* pPlot, ProbabilityTypes eProbStyle = PROBABILITY_REAL) const;		// Exposed to Python
	bool canDestroy(const CvPlot* pPlot, bool bTestVisible = false) const;												// Exposed to Python
	bool destroy();

	int stealPlansCost(const CvPlot* pPlot) const;																									// Exposed to Python
	int stealPlansProb(const CvPlot* pPlot, ProbabilityTypes eProbStyle = PROBABILITY_REAL) const;	// Exposed to Python
	bool canStealPlans(const CvPlot* pPlot, bool bTestVisible = false) const;												// Exposed to Python
	bool stealPlans();

	bool canFound(const CvPlot* pPlot, bool bTestVisible = false) const;																		// Exposed to Python
	bool found();

	bool canSpread(const CvPlot* pPlot, ReligionTypes eReligion, bool bTestVisible = false) const;					// Exposed to Python
	bool spread(ReligionTypes eReligion);

	bool canSpreadCorporation(const CvPlot* pPlot, CorporationTypes eCorporation, bool bTestVisible = false) const;					// Exposed to Python
	bool spreadCorporation(CorporationTypes eCorporation);
	int spreadCorporationCost(CorporationTypes eCorporation, CvCity* pCity) const;

	bool canJoin(const CvPlot* pPlot, SpecialistTypes eSpecialist) const;																		// Exposed to Python
	bool join(SpecialistTypes eSpecialist);

	bool canConstruct(const CvPlot* pPlot, BuildingTypes eBuilding, bool bTestVisible = false) const;				// Exposed to Python
	bool construct(BuildingTypes eBuilding);

	TechTypes getDiscoveryTech() const;																														// Exposed to Python
	int getDiscoverResearch(TechTypes eTech) const;																								// Exposed to Python
	bool canDiscover(const CvPlot* pPlot) const;																									// Exposed to Python
	bool discover();

	int getMaxHurryProduction(CvCity* pCity) const;																													// Exposed to Python
	int getHurryProduction(const CvPlot* pPlot) const;																						// Exposed to Python
	bool canHurry(const CvPlot* pPlot, bool bTestVisible = false) const;													// Exposed to Python
	bool hurry();

	int getTradeGold(const CvPlot* pPlot) const;																									// Exposed to Python
	bool canTrade(const CvPlot* pPlot, bool bTestVisible = false) const;													// Exposed to Python
	bool trade();

	int getGreatWorkCulture(const CvPlot* pPlot) const;																						// Exposed to Python
	bool canGreatWork(const CvPlot* pPlot) const;																									// Exposed to Python
	bool greatWork();

	int getEspionagePoints(const CvPlot* pPlot) const;																									// Exposed to Python
	bool canInfiltrate(const CvPlot* pPlot, bool bTestVisible = false) const;													// Exposed to Python
	bool infiltrate();

	bool canEspionage(const CvPlot* pPlot, bool bTestVisible = false) const;
	bool espionage(EspionageMissionTypes eMission, int iData);
	bool testSpyIntercepted(PlayerTypes eTargetPlayer, int iModifier = 0);
	int getSpyInterceptPercent(TeamTypes eTargetTeam) const;
	bool isIntruding() const;

	bool canGoldenAge(const CvPlot* pPlot, bool bTestVisible = false) const;																// Exposed to Python
	bool goldenAge();

	bool canBuild(const CvPlot* pPlot, BuildTypes eBuild, bool bTestVisible = false) const;				// Exposed to Python
	bool build(BuildTypes eBuild);

	bool canPromote(PromotionTypes ePromotion, int iLeaderUnitId) const;																												// Exposed to Python 
	void promote(PromotionTypes ePromotion, int iLeaderUnitId);																																// Exposed to Python 

	int canLead(const CvPlot* pPlot, int iUnitId) const;
	bool lead(int iUnitId);

	int canGiveExperience(const CvPlot* pPlot) const;																												// Exposed to Python 
	bool giveExperience();																																// Exposed to Python 
	int getStackExperienceToGive(int iNumUnits) const;

	int upgradePrice(UnitTypes eUnit) const;																											// Exposed to Python
	bool upgradeAvailable(UnitTypes eFromUnit, UnitClassTypes eToUnitClass, int iCount = 0) const;					// Exposed to Python
	bool canUpgrade(UnitTypes eUnit, bool bTestVisible = false) const;														// Exposed to Python
	bool isReadyForUpgrade() const;
	bool hasUpgrade(bool bSearch = false) const;																											// Exposed to Python
	bool hasUpgrade(UnitTypes eUnit, bool bSearch = false) const;
	CvCity* getUpgradeCity(bool bSearch = false) const;
	CvCity* getUpgradeCity(UnitTypes eUnit, bool bSearch = false, int* iSearchValue = NULL) const;
	void upgrade(UnitTypes eUnit);

	HandicapTypes getHandicapType() const;																// Exposed to Python		
	CivilizationTypes getCivilizationType() const;							// Exposed to Python								
	const wchar* getVisualCivAdjective(TeamTypes eForTeam) const;
	SpecialUnitTypes getSpecialUnitType() const;								// Exposed to Python								 
	UnitTypes getCaptureUnitType(CivilizationTypes eCivilization) const;	// Exposed to Python								
	UnitCombatTypes getUnitCombatType() const;									// Exposed to Python								
	DllExport DomainTypes getDomainType() const;													// Exposed to Python								
	InvisibleTypes getInvisibleType() const;										// Exposed to Python								
	int getNumSeeInvisibleTypes() const;									// Exposed to Python
	InvisibleTypes getSeeInvisibleType(int i) const;									// Exposed to Python
																																				
	int flavorValue(FlavorTypes eFlavor) const;														// Exposed to Python		

	bool isBarbarian() const;																							// Exposed to Python
	bool isHuman() const;																									// Exposed to Python

	int visibilityRange() const;																					// Exposed to Python

	int baseMoves() const;																			// Exposed to Python
	int maxMoves() const;																									// Exposed to Python
	int movesLeft() const;																			// Exposed to Python			
	DllExport bool canMove() const;																				// Exposed to Python			
	DllExport bool hasMoved() const;																			// Exposed to Python			
																																				
	int airRange() const;																				// Exposed to Python			
	int nukeRange() const;																			// Exposed to Python			 

	bool canBuildRoute() const;																						// Exposed to Python
	DllExport BuildTypes getBuildType() const;														// Exposed to Python
	int workRate(bool bMax) const;															// Exposed to Python

	bool isAnimal() const;																								// Exposed to Python
	bool isNoBadGoodies() const;																					// Exposed to Python
	bool isOnlyDefensive() const;																					// Exposed to Python
	bool isNoCapture() const;																							// Exposed to Python 
	bool isRivalTerritory() const;																				// Exposed to Python 
	bool isMilitaryHappiness() const;																			// Exposed to Python
	bool isInvestigate() const;																						// Exposed to Python
	bool isCounterSpy() const;																						// Exposed to Python
	bool isSpy() const;
	bool isFound() const;																				// Exposed to Python
	bool isGoldenAge() const;																							// Exposed to Python
	bool canCoexistWithEnemyUnit(TeamTypes eTeam) const;																				// Exposed to Python

	DllExport bool isFighting() const;																		// Exposed to Python						
	DllExport bool isAttacking() const;																		// Exposed to Python						
	DllExport bool isDefending() const;																		// Exposed to Python						
	bool isCombat() const;																								// Exposed to Python						
																																				
	DllExport int maxHitPoints() const;																		// Exposed to Python						
	DllExport int currHitPoints() const;																	// Exposed to Python						
	bool isHurt() const;																				// Exposed to Python						
	DllExport bool isDead() const;																				// Exposed to Python						

	void setBaseCombatStr(int iCombat);																																										// Exposed to Python
	int baseCombatStr() const;																																										// Exposed to Python
	int maxCombatStr(const CvPlot* pPlot, const CvUnit* pAttacker, CombatDetails* pCombatDetails = NULL) const;		// Exposed to Python
	int currCombatStr(const CvPlot* pPlot, const CvUnit* pAttacker, CombatDetails* pCombatDetails = NULL) const;	// Exposed to Python
	int currFirepower(const CvPlot* pPlot, const CvUnit* pAttacker) const;																				// Exposed to Python
	int currEffectiveStr(const CvPlot* pPlot, const CvUnit* pAttacker, CombatDetails* pCombatDetails = NULL) const;
	DllExport float maxCombatStrFloat(const CvPlot* pPlot, const CvUnit* pAttacker) const;																	// Exposed to Python
	DllExport float currCombatStrFloat(const CvPlot* pPlot, const CvUnit* pAttacker) const;																	// Exposed to Python

	DllExport bool canFight() const;																									// Exposed to Python
	bool canAttack() const;																														// Exposed to Python
	bool canAttack(const CvUnit& defender) const;
	bool canDefend(const CvPlot* pPlot = NULL) const;																	// Exposed to Python
	bool canSiege(TeamTypes eTeam) const;																							// Exposed to Python

	int airBaseCombatStr() const;																						// Exposed to Python
	int airMaxCombatStr(const CvUnit* pOther) const;																						// Exposed to Python
	int airCurrCombatStr(const CvUnit* pOther) const;																						// Exposed to Python
	DllExport float airMaxCombatStrFloat(const CvUnit* pOther) const;																			// Exposed to Python
	DllExport float airCurrCombatStrFloat(const CvUnit* pOther) const;																		// Exposed to Python
	int combatLimit() const;																												// Exposed to Python
	int airCombatLimit() const;																												// Exposed to Python
	DllExport bool canAirAttack() const;																							// Exposed to Python
	DllExport bool canAirDefend(const CvPlot* pPlot = NULL) const;										// Exposed to Python
	int airCombatDamage(const CvUnit* pDefender) const;																// Exposed to Python
	int rangeCombatDamage(const CvUnit* pDefender) const;																// Exposed to Python
	CvUnit* bestInterceptor(const CvPlot* pPlot) const;																// Exposed to Python
	CvUnit* bestSeaPillageInterceptor(CvUnit* pPillager, int iMinOdds) const;																// Exposed to Python

	bool isAutomated() const;																								// Exposed to Python
	DllExport bool isWaiting() const;																									// Exposed to Python 
	bool isFortifyable() const;																							// Exposed to Python
	int fortifyModifier() const;																						// Exposed to Python

	int experienceNeeded() const;																						// Exposed to Python
	int attackXPValue() const;																												// Exposed to Python	
	int defenseXPValue() const;																												// Exposed to Python	
	int maxXPValue() const;																														// Exposed to Python	

	int firstStrikes() const;																								// Exposed to Python
	int chanceFirstStrikes() const;																					// Exposed to Python 
	int maxFirstStrikes() const;																						// Exposed to Python 
	DllExport bool isRanged() const;																									// Exposed to Python

	bool alwaysInvisible() const;																						// Exposed to Python
	bool immuneToFirstStrikes() const;																			// Exposed to Python
	bool noDefensiveBonus() const;																					// Exposed to Python
	bool ignoreBuildingDefense() const;																								// Exposed to Python
	bool canMoveImpassable() const;																										// Exposed to Python
	bool canMoveAllTerrain() const;																										// Exposed to Python
	bool flatMovementCost() const;																										// Exposed to Python
	bool ignoreTerrainCost() const;																										// Exposed to Python
	bool isNeverInvisible() const;																										// Exposed to Python
	DllExport bool isInvisible(TeamTypes eTeam, bool bDebug, bool bCheckCargo = true) const;										// Exposed to Python
	bool isNukeImmune() const;																												// Exposed to Python

	int maxInterceptionProbability() const;																	// Exposed to Python
	int currInterceptionProbability() const;																// Exposed to Python
	int evasionProbability() const;																										// Exposed to Python
	int withdrawalProbability() const;																			// Exposed to Python

	int collateralDamage() const;																						// Exposed to Python
	int collateralDamageLimit() const;																								// Exposed to Python
	int collateralDamageMaxUnits() const;																							// Exposed to Python

	int cityAttackModifier() const;																					// Exposed to Python
	int cityDefenseModifier() const;																				// Exposed to Python
	int animalCombatModifier() const;																				// Exposed to Python
	int hillsAttackModifier() const;																				// Exposed to Python
	int hillsDefenseModifier() const;																				// Exposed to Python
	int terrainAttackModifier(TerrainTypes eTerrain) const;								// Exposed to Python
	int terrainDefenseModifier(TerrainTypes eTerrain) const;								// Exposed to Python
	int featureAttackModifier(FeatureTypes eFeature) const;								// Exposed to Python
	int featureDefenseModifier(FeatureTypes eFeature) const;								// Exposed to Python
	int unitClassAttackModifier(UnitClassTypes eUnitClass) const;						// Exposed to Python
	int unitClassDefenseModifier(UnitClassTypes eUnitClass) const;					// Exposed to Python
	int unitCombatModifier(UnitCombatTypes eUnitCombat) const;							// Exposed to Python
	int domainModifier(DomainTypes eDomain) const;													// Exposed to Python

	int bombardRate() const;																								// Exposed to Python
	int airBombBaseRate() const;																											// Exposed to Python
	int airBombCurrRate() const;																											// Exposed to Python

	SpecialUnitTypes specialCargo() const;																	// Exposed to Python
	DomainTypes domainCargo() const;																									// Exposed to Python
	int cargoSpace() const;																									// Exposed to Python
	void changeCargoSpace(int iChange);																									// Exposed to Python
	bool isFull() const;																															// Exposed to Python
	int cargoSpaceAvailable(SpecialUnitTypes eSpecialCargo = NO_SPECIALUNIT, DomainTypes eDomainCargo = NO_DOMAIN) const;	// Exposed to Python
	bool hasCargo() const;																									// Exposed to Python
	bool canCargoAllMove() const;																											// Exposed to Python
	bool canCargoEnterArea(TeamTypes eTeam, const CvArea* pArea, bool bIgnoreRightOfPassage) const;
	int getUnitAICargo(UnitAITypes eUnitAI) const;																		// Exposed to Python

	DllExport int getID() const;																											// Exposed to Python
	int getIndex() const;
	DllExport IDInfo getIDInfo() const;
	void setID(int iID);

	int getGroupID() const;																														// Exposed to Python
	bool isInGroup() const;																														// Exposed to Python
	bool isGroupHead() const;																								// Exposed to Python
	DllExport CvSelectionGroup* getGroup() const;																			// Exposed to Python
	bool canJoinGroup(const CvPlot* pPlot, CvSelectionGroup* pSelectionGroup) const;
	DllExport void joinGroup(CvSelectionGroup* pSelectionGroup, bool bRemoveSelected = false, bool bRejoin = true);

	DllExport int getHotKeyNumber();																													// Exposed to Python
	void setHotKeyNumber(int iNewValue);																											// Exposed to Python

	DllExport int getX() const;																																// Exposed to Python
#ifdef _USRDLL
	inline int getX_INLINE() const
	{
		return m_iX;
	}
#endif
	DllExport int getY() const;																																// Exposed to Python
#ifdef _USRDLL
	inline int getY_INLINE() const
	{
		return m_iY;
	}
#endif
	void setXY(int iX, int iY, bool bGroup = false, bool bUpdate = true, bool bShow = false, bool bCheckPlotVisible = false);	// Exposed to Python
	bool at(int iX, int iY) const;																														// Exposed to Python
	DllExport bool atPlot(const CvPlot* pPlot) const;																					// Exposed to Python
	DllExport CvPlot* plot() const;																														// Exposed to Python
	int getArea() const;																																			// Exposed to Python
	CvArea* area() const;																																			// Exposed to Python
	bool onMap() const;

	int getLastMoveTurn() const;
	void setLastMoveTurn(int iNewValue);

	CvPlot* getReconPlot() const;																															// Exposed to Python 
	void setReconPlot(CvPlot* pNewValue);																			// Exposed to Python

	int getGameTurnCreated() const;																														// Exposed to Python
	void setGameTurnCreated(int iNewValue);

	DllExport int getDamage() const;																													// Exposed to Python
	void setDamage(int iNewValue, PlayerTypes ePlayer = NO_PLAYER, bool bNotifyEntity = true);														// Exposed to Python
	void changeDamage(int iChange, PlayerTypes ePlayer = NO_PLAYER);													// Exposed to Python

	int getMoves() const;																																			// Exposed to Python
	void setMoves(int iNewValue);																										// Exposed to Python
	void changeMoves(int iChange);																														// Exposed to Python
	void finishMoves();																																				// Exposed to Python

	int getExperience() const;																											// Exposed to Python
	void setExperience(int iNewValue, int iMax = -1);																// Exposed to Python
	void changeExperience(int iChange, int iMax = -1, bool bFromCombat = false, bool bInBorders = false, bool bUpdateGlobal = false);																				// Exposed to Python

	int getLevel() const;																														// Exposed to Python					
	void setLevel(int iNewValue);
	void changeLevel(int iChange);

	int getCargo() const;																														// Exposed to Python					
	void changeCargo(int iChange);
	void getCargoUnits(std::vector<CvUnit*>& aUnits) const;

	CvPlot* getAttackPlot() const;
	void setAttackPlot(const CvPlot* pNewValue, bool bAirCombat);
	bool isAirCombat() const;

	DllExport int getCombatTimer() const;
	void setCombatTimer(int iNewValue);
	void changeCombatTimer(int iChange);

	int getCombatFirstStrikes() const;			
	void setCombatFirstStrikes(int iNewValue);			
	void changeCombatFirstStrikes(int iChange);			

	int getFortifyTurns() const;																															// Exposed to Python
	void setFortifyTurns(int iNewValue);
	void changeFortifyTurns(int iChange);

	int getBlitzCount() const;			
	bool isBlitz() const;																														// Exposed to Python					
	void changeBlitzCount(int iChange);																												
																																														
	int getAmphibCount() const;																																
	bool isAmphib() const;																													// Exposed to Python					
	void changeAmphibCount(int iChange);																											
																																														
	int getRiverCount() const;																																
	bool isRiver() const;																														// Exposed to Python					
	void changeRiverCount(int iChange);																												
																																														
	int getEnemyRouteCount() const;																									
	bool isEnemyRoute() const;																											// Exposed to Python					
	void changeEnemyRouteCount(int iChange);																									
																																														
	int getAlwaysHealCount() const;																														
	bool isAlwaysHeal() const;																											// Exposed to Python					
	void changeAlwaysHealCount(int iChange);																									
																																														
	int getHillsDoubleMoveCount() const;																											
	bool isHillsDoubleMove() const;																									// Exposed to Python					
	void changeHillsDoubleMoveCount(int iChange);																							
																																														
	int getImmuneToFirstStrikesCount() const;																									
	void changeImmuneToFirstStrikesCount(int iChange);																				
																																														
	int getExtraVisibilityRange() const;																						// Exposed to Python					
	void changeExtraVisibilityRange(int iChange);

	int getExtraMoves() const;																																// Exposed to Python
	void changeExtraMoves(int iChange);

	int getExtraMoveDiscount() const;																								// Exposed to Python
	void changeExtraMoveDiscount(int iChange);

	int getExtraAirRange() const;																																// Exposed to Python
	void changeExtraAirRange(int iChange);

	int getExtraIntercept() const;																																// Exposed to Python
	void changeExtraIntercept(int iChange);

	int getExtraEvasion() const;																																// Exposed to Python
	void changeExtraEvasion(int iChange);

	int getExtraFirstStrikes() const;																													// Exposed to Python
	void changeExtraFirstStrikes(int iChange);

	int getExtraChanceFirstStrikes() const;																										// Exposed to Python
	void changeExtraChanceFirstStrikes(int iChange);

	int getExtraWithdrawal() const;																														// Exposed to Python
	void changeExtraWithdrawal(int iChange);

	int getExtraCollateralDamage() const;																											// Exposed to Python
	void changeExtraCollateralDamage(int iChange);

	int getExtraBombardRate() const;																													// Exposed to Python
	void changeExtraBombardRate(int iChange);

	int getExtraEnemyHeal() const;																									// Exposed to Python					
	void changeExtraEnemyHeal(int iChange);																										
																																														
	int getExtraNeutralHeal() const;																								// Exposed to Python					
	void changeExtraNeutralHeal(int iChange);																									
																																														
	int getExtraFriendlyHeal() const;																								// Exposed to Python					
	void changeExtraFriendlyHeal(int iChange);																								
																																														
	int getSameTileHeal() const;																										// Exposed to Python					
	void changeSameTileHeal(int iChange);																											
																																														
	int getAdjacentTileHeal() const;																								// Exposed to Python					
	void changeAdjacentTileHeal(int iChange);																									
																																														
	int getExtraCombatPercent() const;																							// Exposed to Python					
	void changeExtraCombatPercent(int iChange);

	int getExtraCityAttackPercent() const;																										// Exposed to Python
	void changeExtraCityAttackPercent(int iChange);

	int getExtraCityDefensePercent() const;																										// Exposed to Python
	void changeExtraCityDefensePercent(int iChange);

	int getExtraHillsAttackPercent() const;																									// Exposed to Python
	void changeExtraHillsAttackPercent(int iChange);

	int getExtraHillsDefensePercent() const;																									// Exposed to Python
	void changeExtraHillsDefensePercent(int iChange);

	int getRevoltProtection() const;																									// Exposed to Python
	void changeRevoltProtection(int iChange);

	int getCollateralDamageProtection() const;																									// Exposed to Python
	void changeCollateralDamageProtection(int iChange);

	int getPillageChange() const;																									// Exposed to Python
	void changePillageChange(int iChange);

	int getUpgradeDiscount() const;																									// Exposed to Python
	void changeUpgradeDiscount(int iChange);

	int getExperiencePercent() const;																									// Exposed to Python
	void changeExperiencePercent(int iChange);

	int getKamikazePercent() const;																									// Exposed to Python
	void changeKamikazePercent(int iChange);

	DllExport DirectionTypes getFacingDirection(bool checkLineOfSightProperty) const;
	void setFacingDirection(DirectionTypes facingDirection);
	void rotateFacingDirectionClockwise();
	void rotateFacingDirectionCounterClockwise();

	DllExport bool isSuicide() const;																											// Exposed to Python
	int getDropRange() const;

	bool isMadeAttack() const;																																// Exposed to Python
	void setMadeAttack(bool bNewValue);																							// Exposed to Python

	bool isMadeInterception() const;																													// Exposed to Python
	void setMadeInterception(bool bNewValue);																				// Exposed to Python

	DllExport bool isPromotionReady() const;																									// Exposed to Python
	void setPromotionReady(bool bNewValue);																					// Exposed to Python
	void testPromotionReady();

	bool isDelayedDeath() const;
	void startDelayedDeath();
	bool doDelayedDeath();

	bool isCombatFocus() const;

	DllExport bool isInfoBarDirty() const;
	DllExport void setInfoBarDirty(bool bNewValue);

	bool isBlockading() const;
	void setBlockading(bool bNewValue);
	void collectBlockadeGold();

	DllExport PlayerTypes getOwner() const;																									// Exposed to Python
#ifdef _USRDLL
	inline PlayerTypes getOwnerINLINE() const
	{
		return m_eOwner;
	}
#endif
	DllExport PlayerTypes getVisualOwner(TeamTypes eForTeam = NO_TEAM) const;																									// Exposed to Python
	PlayerTypes getCombatOwner(TeamTypes eForTeam, const CvPlot* pPlot) const;																									// Exposed to Python
	DllExport TeamTypes getTeam() const;																										// Exposed to Python

	PlayerTypes getCapturingPlayer() const;
	void setCapturingPlayer(PlayerTypes eNewValue);

	DllExport const UnitTypes getUnitType() const;																					// Exposed to Python
	CvUnitInfo &getUnitInfo() const;
	UnitClassTypes getUnitClassType() const;	// Exposed to Python

	DllExport const UnitTypes getLeaderUnitType() const;
	void setLeaderUnitType(UnitTypes leaderUnitType);

	DllExport CvUnit* getCombatUnit() const;
	void setCombatUnit(CvUnit* pUnit, bool bAttacking = false);

	CvUnit* getTransportUnit() const;																							// Exposed to Python
	bool isCargo() const;																													// Exposed to Python
	void setTransportUnit(CvUnit* pTransportUnit);																							// Exposed to Python

	int getExtraDomainModifier(DomainTypes eIndex) const;																		// Exposed to Python
	void changeExtraDomainModifier(DomainTypes eIndex, int iChange);

	DllExport const CvWString getName(uint uiForm = 0) const;																// Exposed to Python
	DllExport const wchar* getNameKey() const;																							// Exposed to Python
	const CvWString& getNameNoDesc() const;																				// Exposed to Python
	void setName(const CvWString szNewValue);																			// Exposed to Python

	// Script data needs to be a narrow string for pickling in Python
	std::string getScriptData() const;																											// Exposed to Python
	void setScriptData(std::string szNewValue);																							// Exposed to Python

	int getTerrainDoubleMoveCount(TerrainTypes eIndex) const;
	bool isTerrainDoubleMove(TerrainTypes eIndex) const;													// Exposed to Python 
	void changeTerrainDoubleMoveCount(TerrainTypes eIndex, int iChange);

	int getFeatureDoubleMoveCount(FeatureTypes eIndex) const;
	bool isFeatureDoubleMove(FeatureTypes eIndex) const;													// Exposed to Python 
	void changeFeatureDoubleMoveCount(FeatureTypes eIndex, int iChange);

	int getExtraTerrainAttackPercent(TerrainTypes eIndex) const;														// Exposed to Python
	void changeExtraTerrainAttackPercent(TerrainTypes eIndex, int iChange);						
	int getExtraTerrainDefensePercent(TerrainTypes eIndex) const;														// Exposed to Python
	void changeExtraTerrainDefensePercent(TerrainTypes eIndex, int iChange);						
	int getExtraFeatureAttackPercent(FeatureTypes eIndex) const;														// Exposed to Python
	void changeExtraFeatureAttackPercent(FeatureTypes eIndex, int iChange);
	int getExtraFeatureDefensePercent(FeatureTypes eIndex) const;														// Exposed to Python
	void changeExtraFeatureDefensePercent(FeatureTypes eIndex, int iChange);

	int getExtraUnitCombatModifier(UnitCombatTypes eIndex) const;														// Exposed to Python
	void changeExtraUnitCombatModifier(UnitCombatTypes eIndex, int iChange);

	bool canAcquirePromotion(PromotionTypes ePromotion) const;															// Exposed to Python 
	bool canAcquirePromotionAny() const;																										// Exposed to Python
	bool isPromotionValid(PromotionTypes ePromotion) const;															// Exposed to Python 
	bool isHasPromotion(PromotionTypes eIndex) const;															// Exposed to Python
	void setHasPromotion(PromotionTypes eIndex, bool bNewValue);									// Exposed to Python

	DllExport int getSubUnitCount() const;
	DllExport int getSubUnitsAlive() const;
	int getSubUnitsAlive(int iDamage) const;

	bool isTargetOf(const CvUnit& attacker) const;

	bool isEnemy(TeamTypes eTeam, const CvPlot* pPlot = NULL) const;
	bool isPotentialEnemy(TeamTypes eTeam, const CvPlot* pPlot = NULL) const;

	bool canRangeStrike() const;
	bool canRangeStrikeAt(const CvPlot* pPlot, int iX, int iY) const;
	bool rangeStrike(int iX, int iY);

	int getTriggerValue(EventTriggerTypes eTrigger, const CvPlot* pPlot, bool bCheckPlot) const;
	bool canApplyEvent(EventTypes eEvent) const;
	void applyEvent(EventTypes eEvent);

	int getImmobileTimer() const;															// Exposed to Python
	void setImmobileTimer(int iNewValue);													// Exposed to Python
	void changeImmobileTimer(int iChange);

	bool potentialWarAction(const CvPlot* pPlot) const;
	bool willRevealByMove(const CvPlot* pPlot) const;

	bool isAlwaysHostile(const CvPlot* pPlot) const;

	bool verifyStackValid();

	DllExport const CvArtInfoUnit* getArtInfo(int i, EraTypes eEra) const;										// Exposed to Python
	DllExport const TCHAR* getButton() const;										// Exposed to Python
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

	void read(FDataStreamBase* pStream);
	void write(FDataStreamBase* pStream);

	virtual void AI_init(UnitAITypes eUnitAI) = 0;
	virtual void AI_uninit() = 0;
	virtual void AI_reset(UnitAITypes eUnitAI = NO_UNITAI) = 0;
	virtual bool AI_update() = 0;
	virtual bool AI_follow() = 0;
	virtual void AI_upgrade() = 0;
	virtual void AI_promote() = 0;
	virtual int AI_groupFirstVal() = 0;
	virtual int AI_groupSecondVal() = 0;
	virtual int AI_attackOdds(const CvPlot* pPlot, bool bPotentialEnemy) const = 0;
	virtual bool AI_bestCityBuild(CvCity* pCity, CvPlot** ppBestPlot = NULL, BuildTypes* peBestBuild = NULL, CvPlot* pIgnorePlot = NULL, CvUnit* pUnit = NULL) = 0;
	virtual bool AI_isCityAIType() const = 0;
	virtual UnitAITypes AI_getUnitAIType() const = 0;																				// Exposed to Python
	virtual void AI_setUnitAIType(UnitAITypes eNewValue) = 0;
    virtual int AI_sacrificeValue(const CvPlot* pPlot) const = 0;

protected:

	int m_iID;
	int m_iGroupID;
	int m_iHotKeyNumber;
	int m_iX;
	int m_iY;
	int m_iLastMoveTurn;
	int m_iReconX;
	int m_iReconY;
	int m_iGameTurnCreated;
	int m_iDamage;
	int m_iMoves;
	int m_iExperience;
	int m_iLevel;
	int m_iCargo;
	int m_iCargoCapacity;
	int m_iAttackPlotX;
	int m_iAttackPlotY;
	int m_iCombatTimer;
	int m_iCombatFirstStrikes;
	int m_iCombatDamage;
	int m_iFortifyTurns;
	int m_iBlitzCount;
	int m_iAmphibCount;
	int m_iRiverCount;
	int m_iEnemyRouteCount;
	int m_iAlwaysHealCount;
	int m_iHillsDoubleMoveCount;
	int m_iImmuneToFirstStrikesCount;
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
	int m_iRevoltProtection;
	int m_iCollateralDamageProtection;
	int m_iPillageChange;
	int m_iUpgradeDiscount;
	int m_iExperiencePercent;
	int m_iKamikazePercent;
	int m_iBaseCombat;
	DirectionTypes m_eFacingDirection;
	int m_iImmobileTimer;

	bool m_bMadeAttack;
	bool m_bMadeInterception;
	bool m_bPromotionReady;
	bool m_bDeathDelay;
	bool m_bCombatFocus;
	bool m_bInfoBarDirty;
	bool m_bBlockading;
	bool m_bAirCombat;

	PlayerTypes m_eOwner;
	PlayerTypes m_eCapturingPlayer;
	UnitTypes m_eUnitType;
	UnitTypes m_eLeaderUnitType;
	CvUnitInfo *m_pUnitInfo;

	IDInfo m_combatUnit;
	IDInfo m_transportUnit;

	int* m_aiExtraDomainModifier;

	CvWString m_szName;
	CvString m_szScriptData;

	bool* m_pabHasPromotion;

	int* m_paiTerrainDoubleMoveCount;
	int* m_paiFeatureDoubleMoveCount;
	int* m_paiExtraTerrainAttackPercent;
	int* m_paiExtraTerrainDefensePercent;
	int* m_paiExtraFeatureAttackPercent;
	int* m_paiExtraFeatureDefensePercent;
	int* m_paiExtraUnitCombatModifier;

	bool canAdvance(const CvPlot* pPlot, int iThreshold) const;
	void collateralCombat(const CvPlot* pPlot, CvUnit* pSkipUnit = NULL);
	void flankingStrikeCombat(const CvPlot* pPlot, int iAttackerStrength, int iAttackerFirepower, int iDefenderOdds, int iDefenderDamage, CvUnit* pSkipUnit = NULL);

	bool interceptTest(const CvPlot* pPlot);
	CvUnit* airStrikeTarget(const CvPlot* pPlot) const;
	bool canAirStrike(const CvPlot* pPlot) const;
	bool airStrike(CvPlot* pPlot);

	int planBattle( CvBattleDefinition & kBattleDefinition ) const;
	int computeUnitsToDie( const CvBattleDefinition & kDefinition, bool bRanged, BattleUnitTypes iUnit ) const;
	bool verifyRoundsValid( const CvBattleDefinition & battleDefinition ) const;
	void increaseBattleRounds( CvBattleDefinition & battleDefinition ) const;
	int computeWaveSize( bool bRangedRound, int iAttackerMax, int iDefenderMax ) const;

	void getDefenderCombatValues(CvUnit& kDefender, const CvPlot* pPlot, int iOurStrength, int iOurFirepower, int& iTheirOdds, int& iTheirStrength, int& iOurDamage, int& iTheirDamage, CombatDetails* pTheirDetails = NULL) const;

	bool isCombatVisible(const CvUnit* pDefender) const;
	void resolveCombat(CvUnit* pDefender, CvPlot* pPlot, CvBattleDefinition& kBattle);
	void resolveAirCombat(CvUnit* pInterceptor, CvPlot* pPlot, CvAirMissionDefinition& kBattle);
	void checkRemoveSelectionAfterAttack();
};

#endif
