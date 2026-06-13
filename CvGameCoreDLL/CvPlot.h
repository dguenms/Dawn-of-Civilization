#pragma once

#ifndef CIV4_PLOT_H
#define CIV4_PLOT_H

#include "PlotAdjListTraversal.h" // advc.003s

class CvArea;
class CvMap;
class CvPlotBuilder;
class CvRoute;
class CvRiver;
class CvCity;
class CvPlotGroup;
class CvFeature;
class CvUnit;
class CvSymbol;
class CvFlagEntity;

typedef bool (*ConstPlotUnitFunc)(const CvUnit* pUnit, int iData1, int iData2);
typedef bool (*PlotUnitFunc)(CvUnit* pUnit, int iData1, int iData2);

class CvPlot
{
public:

	CvPlot();
	~CvPlot();

	void init(int iX, int iY);
	void initAdjList(); // advc.003s
	void setupGraphical();
	void updateGraphicEra();

	void erase();																					// Exposed to Python
	void eraseAIDevelopment(); // rfc

	DllExport float getPointX() const;
	DllExport float getPointY() const;
	DllExport NiPoint3 getPoint() const;															// Exposed to Python

	float getSymbolSize() const;
	DllExport float getSymbolOffsetX(int iID) const;
	DllExport float getSymbolOffsetY(int iID) const;

	void doTurn();
	void doImprovement();

	void updateCulture(bool bBumpUnits, bool bUpdatePlotGroups);
	void updateFog();
	void updateVisibility();
	void updateSymbolDisplay();
	void updateSymbolVisibility();
	void updateSymbols();
	void updateMinimapColor();
	void updateCenterUnit();

	void verifyUnitValidPlot();
	void forceBumpUnits(); // K-Mod

	void nukeExplosion(int iRange, CvUnit* pNukeUnit = NULL,
			bool bBomb = true); //  K-Mod added bBomb, Exposed to Python

	bool isConnectedTo(CvCity const& kCity) const;													// Exposed to Python
	bool isConnectedToCapital(PlayerTypes ePlayer = NO_PLAYER) const;								// Exposed to Python
	int getPlotGroupConnectedBonus(PlayerTypes ePlayer, BonusTypes eBonus) const;					// Exposed to Python
	bool isPlotGroupConnectedBonus(PlayerTypes ePlayer, BonusTypes eBonus) const					// Exposed to Python
	{
		return (getPlotGroupConnectedBonus(ePlayer, eBonus) > 0);
	}
	bool isAdjacentPlotGroupConnectedBonus(PlayerTypes ePlayer, BonusTypes eBonus) const;			// Exposed to Python
	void updatePlotGroupBonus(bool bAdd, /* advc.064d: */ bool bVerifyProduction = true);

	//bool isAdjacentToArea(int iAreaID) const; // advc: use the one below instead
	bool isAdjacentToArea(CvArea const& kArea) const;												// Exposed to Python
	bool shareAdjacentArea(const CvPlot* pPlot) const;												// Exposed to Python
	bool isAdjacentToLand() const;																	// Exposed to Python
	// advc.003t: Default was -1, which now means MIN_WATER_SIZE_FOR_OCEAN.
	bool isCoastalLand(int iMinWaterSize = 0) const;												// Exposed to Python

	bool isVisibleWorked() const;
	bool isWithinTeamCityRadius(TeamTypes eTeam, PlayerTypes eIgnorePlayer = NO_PLAYER) const;		// Exposed to Python

	DllExport bool isLake() const;																	// Exposed to Python
	bool isFreshWater() const;																		// Exposed to Python
	bool isAdjacentFreshWater() const; // advc.108
	bool isAdjacentSaltWater() const; // advc.041
	bool isPotentialIrrigation(/* advc: */ bool bIgnoreTech = false) const;							// Exposed to Python
	bool canHavePotentialIrrigation() const;														// Exposed to Python
	DllExport bool isIrrigationAvailable(bool bIgnoreSelf = false) const;							// Exposed to Python

	bool isRiverMask() const;
	DllExport bool isRiverCrossingFlowClockwise(DirectionTypes eDirection) const;
	bool isRiverSide() const;																		// Exposed to Python
	bool isRiver() const { return (getRiverCrossingCount() > 0); }									// Exposed to Python
	bool isRiverConnection(DirectionTypes eDir) const;												// Exposed to Python
	bool isRiverToRiverConnection(CvPlot const& kOther) const; // advc.124b
	// advc.500:
	bool isConnectRiverSegments() const;
	// advc.121: A kind of canal detection
	bool isConnectSea() const;

	CvPlot* getNearestLandPlotInternal(int iDistance) const;
	CvArea* getNearestLandArea() const;																// Exposed to Python
	CvPlot* getNearestLandPlot() const { return getNearestLandPlotInternal(0); }					// Exposed to Python

	int seeFromLevel(TeamTypes eTeam) const;														// Exposed to Python
	int seeThroughLevel() const;																	// Exposed to Python
	void changeAdjacentSight(TeamTypes eTeam, int iRange, bool bIncrement,
			CvUnit const* pUnit, bool bUpdatePlotGroups);
	bool canSeePlot(CvPlot const* pPlot, TeamTypes eTeam, int iRange,
			DirectionTypes eFacingDirection /* advc: */ = NO_DIRECTION) const;
	bool canSeeDisplacementPlot(TeamTypes eTeam, int iDX, int iDY,
			int iOriginalDX, int iOriginalDY, bool bFirstPlot, bool bOuterRing) const;
	bool shouldProcessDisplacementPlot(int iDX, int iDY,// int range, // advc: unused
			DirectionTypes eFacingDirection) const;
	void updateSight(bool bIncrement, bool bUpdatePlotGroups);
	void updateSeeFromSight(bool bIncrement, bool bUpdatePlotGroups);

	bool canHaveBonus(BonusTypes eBonus, bool bIgnoreLatitude = false,								// Exposed to Python
			bool bIgnoreFeature = false, // advc.129
			bool bIgnoreCurrentBonus = false) const; // advc.tsl
	bool canHaveImprovement(ImprovementTypes eImprovement,											// Exposed to Python
			TeamTypes eTeam = NO_TEAM, bool bPotential = false,
			BuildTypes eBuild = NO_BUILD, bool bAnyBuild = true) const; // kekm.9
	bool canBuild(BuildTypes eBuild, PlayerTypes ePlayer = NO_PLAYER,								// Exposed to Python
			bool bTestVisible = false,
			bool bIgnoreFoW = true) const; // advc.181
	int getBuildTime(BuildTypes eBuild,																// Exposed to Python
			PlayerTypes ePlayer) const; // advc.251
	int getBuildTurnsLeft(BuildTypes eBuild, /* advc.251: */ PlayerTypes ePlayer,
			int iNowExtra, int iThenExtra,															// Exposed to Python
			// <advc.011c>
			bool bIncludeUnits = true) const;
	int getBuildTurnsLeft(BuildTypes eBuild, PlayerTypes ePlayer) const;
	// </advc.011c>
	int getFeatureProduction(BuildTypes eBuild, TeamTypes eTeam, CvCity** ppCity,					// Exposed to Python
			CvPlot const* pCityPlot = NULL, PlayerTypes eCityOwner = NO_PLAYER) const; // advc.031

	DllExport CvUnit* getBestDefender(PlayerTypes eOwner, PlayerTypes eAttackingPlayer = NO_PLAYER,	// Exposed to Python
		CvUnit const* pAttacker = NULL, bool bTestAtWar = false, bool bTestPotentialEnemy = false,
		/*  advc.028: Replacing bTestCanMove. False by default b/c invisible units are generally
			able to defend - they just choose not to (CvUnit::isBetterDefenderThan). */
		bool bTestVisible = false) const
	// <advc> Need some more params
	{
		DefenderFilters defFilters(eAttackingPlayer, pAttacker,
				bTestAtWar, bTestPotentialEnemy,
				bTestVisible); // advc.028
		return getBestDefender(eOwner, defFilters);
	}
	struct DefenderFilters
	{
		DefenderFilters(
			PlayerTypes eAttackingPlayer = NO_PLAYER, CvUnit const* pAttacker = NULL,
			bool bTestEnemy = false, bool bTestPotentialEnemy = false,
			bool bTestVisible = false, // advc.028
			/*	advc: New params to allow hasDefender checks.
				advc.089: bTestCanAttack=true by default. */
			bool bTestCanAttack = true, bool bTestAny = false,
			/*	(Ideally, this should be swapped with bTestVisible to stay closer
				to the original code. bTestCanMove had been unused for a while.
				Not going to change this now, too error-prone.) */
			bool bTestCanMove = false)
		:	m_eAttackingPlayer(eAttackingPlayer), m_pAttacker(pAttacker),
			m_bTestEnemy(bTestEnemy), m_bTestPotentialEnemy(bTestPotentialEnemy),
			m_bTestVisible(bTestVisible), // advc.028
			m_bTestCanAttack(bTestCanAttack), m_bTestAny(bTestAny), // advc
			m_bTestCanMove(bTestCanMove)
		{}
		PlayerTypes m_eAttackingPlayer;
		CvUnit const* m_pAttacker;
		bool m_bTestEnemy, m_bTestPotentialEnemy,
			 m_bTestVisible, // advc.028
			 m_bTestCanAttack, m_bTestAny, // advc
			 m_bTestCanMove;
	};
	CvUnit* getBestDefender(PlayerTypes eOwner, DefenderFilters& kFilters) const;
	// </advc>
	// BETTER_BTS_AI_MOD, Lead From Behind (UncutDragon), 02/21/10, jdog5000:
	bool hasDefender(bool bTestCanAttack, PlayerTypes eOwner,
			PlayerTypes eAttackingPlayer = NO_PLAYER, const CvUnit* pAttacker = NULL,
			bool bTestAtWar = false, bool bTestPotentialEnemy = false
			/*,bool bTestCanMove = false*/) const; // advc: param unused (and doesn't make sense to me)
	// disabled by K-Mod:
	//int AI_sumStrength(PlayerTypes eOwner, PlayerTypes eAttackingPlayer = NO_PLAYER, DomainTypes eDomainType = NO_DOMAIN, bool bDefensiveBonuses = true, bool bTestAtWar = false, bool bTestPotentialEnemy = false) const;
	CvUnit* getSelectedUnit() const;																// Exposed to Python
	int getUnitPower(PlayerTypes eOwner = NO_PLAYER) const;											// Exposed to Python

	int defenseModifier(TeamTypes eDefender, bool bIgnoreBuilding,									// Exposed to Python
		/*  advc.012: NO_TEAM means rival defense applies; moved bHelp to the
			end b/c that parameter is rarely set */
			TeamTypes eAttacker = NO_TEAM, bool bHelp = false,
			bool bGarrisonStrength = false) const; // advc.500b
	int movementCost(CvUnit const& kUnit, CvPlot const& kFrom,										// Exposed to Python
			bool bAssumeRevealed = true) const; // advc.001i
	// advc.enum: Still exposed to Python, obsolete within the DLL.
	/*int getExtraMovePathCost() const;																// Exposed to Python
	void changeExtraMovePathCost(int iChange);*/													// Exposed to Python

	bool isAdjacentOwned() const;																	// Exposed to Python
	bool isAdjacentPlayer(PlayerTypes ePlayer, bool bLandOnly = false) const;						// Exposed to Python
	bool isAdjacentTeam(TeamTypes eTeam, bool bLandOnly = false) const;								// Exposed to Python
	bool isWithinCultureRange(PlayerTypes ePlayer) const;											// Exposed to Python
	int getNumCultureRangeCities(PlayerTypes ePlayer) const;										// Exposed to Python

	/*	(advc.pf: BBAI path distance functions moved to CvTeamAI.
		calculatePathDistanceToPlot first turned into CvMap::calculateTeamPathDistance,
		then deleted on 21 Oct 2020 and replaced with TeamPathFinder.) */
	/*	BETTER_BTS_AI_MOD, Efficiency, 08/21/09, jdog5000: START
		Plot danger cache (rewritten for K-Mod to fix bugs and improvement performance) */
	int getActivePlayerSafeRangeCache() const
	{
		return m_iActivePlayerSafeRangeCache;
	}
	void setActivePlayerSafeRangeCache(int iRange) const
	{
		// advc.opt: char (Probably OK to do nothing here if indeed iRange > MAX_CHAR.)
		m_iActivePlayerSafeRangeCache = safeIntCast<char>(iRange);
	}
	bool getBorderDangerCache(TeamTypes eTeam) const
	{
		return m_abBorderDangerCache.get(eTeam);
	}
	void setBorderDangerCache(TeamTypes eTeam, bool bNewValue) const
	{
		m_abBorderDangerCache.set(eTeam, bNewValue);
	}
	void invalidateBorderDangerCache();
	// BETTER_BTS_AI_MOD: END
	PlayerTypes calculateCulturalOwner(
			bool bIgnoreCultureRange = false, // advc.099c
			bool bOwnExclusiveRadius = false) const; // advc.035

	void plotAction(PlotUnitFunc func, int iData1 = -1, int iData2 = -1,
			PlayerTypes eOwner = NO_PLAYER, TeamTypes eTeam = NO_TEAM);
	int plotCount(ConstPlotUnitFunc funcA, int iData1A = -1, int iData2A = -1,
			PlayerTypes eOwner = NO_PLAYER, TeamTypes eTeam = NO_TEAM,
			ConstPlotUnitFunc funcB = NULL, int iData1B = -1, int iData2B = -1) const;
	CvUnit* plotCheck(ConstPlotUnitFunc funcA, int iData1A = -1, int iData2A = -1,
			PlayerTypes eOwner = NO_PLAYER, TeamTypes eTeam = NO_TEAM,
			ConstPlotUnitFunc funcB = NULL, int iData1B = -1, int iData2B = -1) const;

	bool isOwned() const																			// Exposed to Python
	{
		return (getOwner() != NO_PLAYER);
	}
	bool isBarbarian() const { return (getOwner() == BARBARIAN_PLAYER); }							// Exposed to Python
	bool isRevealedBarbarian() const;																// Exposed to Python

	bool isVisible(TeamTypes eTeam, bool bDebug) const;												// Exposed to Python
	// advc: Make bDebug=false the default
	bool isVisible(TeamTypes eTeam) const
	{
		return isVisible(eTeam, false);
	}
	DllExport bool isActiveVisible(bool bDebug) const;												// Exposed to Python
	bool isVisibleToCivTeam() const;																// Exposed to Python
	// <advc.706>
	static bool isAllFog() { return m_bAllFog; }
	static void setAllFog(bool b) { m_bAllFog = b; } // </advc.706>
	// <advc.300>
	bool isCivUnitNearby(int iRadius) const;
	CvPlot const* nearestInvisiblePlot(bool bOnlyLand, int iMaxPlotDist, TeamTypes eObserver) const;
	// </advc.300>
	bool isVisibleToWatchingHuman() const;															// Exposed to Python
	bool isAdjacentVisible(TeamTypes eTeam, bool bDebug) const;										// Exposed to Python
	bool isAdjacentNonvisible(TeamTypes eTeam) const;												// Exposed to Python

	DllExport bool isGoody(TeamTypes eTeam = NO_TEAM) const;										// Exposed to Python
	bool isRevealedGoody(TeamTypes eTeam = NO_TEAM) const;											// Exposed to Python
	void removeGoody();																				// Exposed to Python

	// advc.inl:
	bool isCity() const
	{
		return m_plotCity.isIDSet(); // avoid ::getCity call
	}
	/*	advc: Deprecated; exported through .def file. Should use more specific checks
		such as isCity (inline) or (CvTeam) isBase, isCityTrade, isCityDefense, isCityHeal. */
	bool isCityExternal(bool bCheckImprovement, TeamTypes eForTeam = NO_TEAM) const;				// Exposed to Python
	/*	advc: isFriendlyCity replaced with CvUnit::isPlotValid;
		isEnemyCity also moved to CvUnit. */

	bool isOccupation() const;																		// Exposed to Python
	bool isBeingWorked() const;																		// Exposed to Python

	bool isUnit() const { return (getNumUnits() > 0); }												// Exposed to Python
	bool isInvestigate(TeamTypes eTeam) const														// Exposed to Python
	{
		return (plotCheck(PUF_isInvestigate, -1, -1, NO_PLAYER, eTeam) != NULL);
	}
	bool isVisibleEnemyDefender(const CvUnit* pUnit) const;											// Exposed to Python
	CvUnit *getVisibleEnemyDefender(PlayerTypes ePlayer) const
	{
		return plotCheck(PUF_canDefendEnemy, ePlayer, false,
				NO_PLAYER, NO_TEAM, PUF_isVisible, ePlayer);
	}
	int getNumDefenders(PlayerTypes ePlayer) const													// Exposed to Python
	{
		return plotCount(PUF_canDefend, -1, -1, ePlayer);
	}
	int getNumVisibleEnemyDefenders(const CvUnit* pUnit) const;										// Exposed to Python
	// (advc: getNumVisiblePotentialEnemyDefenders has become CvUnitAI::AI_countEnemyDefenders)
	DllExport bool isVisibleEnemyUnit(PlayerTypes ePlayer) const									// Exposed to Python
	{
		return (plotCheck(PUF_isEnemy, ePlayer, false,
				NO_PLAYER, NO_TEAM, PUF_isVisible, ePlayer) != NULL);
	}
	// <advc.ctr>
	bool isVisibleEnemyCityAttacker(PlayerTypes eDefender, TeamTypes eAssumePeace = NO_TEAM,
			int iRange = 0) const; // </advc.ctr>
	// (advc: isVisiblePotentialEnemyUnit has become CvTeamAI::AI_mayAttack(CvPlot const&))
	DllExport int getNumVisibleUnits(PlayerTypes ePlayer) const;
	bool isVisibleEnemyUnit(const CvUnit* pUnit) const;
	// advc.004l:
	bool isVisibleEnemyUnit(CvUnit const* pUnit, CvUnit const* pPotentialEnemy) const;
	bool isVisibleOtherUnit(PlayerTypes ePlayer) const												// Exposed to Python
	{
		return (plotCheck(PUF_isOtherTeam, ePlayer, -1,
				NO_PLAYER, NO_TEAM, PUF_isVisible, ePlayer) != NULL);
	}
	DllExport bool isFighting() const																// Exposed to Python
	{
		return (plotCheck(PUF_isFighting) != NULL);
	}

	bool canHaveFeature(FeatureTypes eFeature,														// Exposed to Python
			bool bIgnoreCurrentFeature = false) const; // advc.055
	DllExport bool isRoute() const																	// Exposed to Python
	{
		return (getRouteType() != NO_ROUTE);
	}
	bool isValidRoute(const CvUnit* pUnit, /* advc.001i: */ bool bAssumeRevealed) const;			// Exposed to Python
	bool isTradeNetworkImpassable(TeamTypes eTeam) const											// Exposed to Python
	{
		return (isImpassable() && !isRiverNetwork(eTeam));
	}
	bool isNetworkTerrain(TeamTypes eTeam) const;													// Exposed to Python
	bool isBonusNetwork(TeamTypes eTeam) const;														// Exposed to Python
	bool isTradeNetwork(TeamTypes eTeam) const;														// Exposed to Python
	bool isTradeNetworkConnected(CvPlot const& kOther, TeamTypes eTeam) const; // advc: param was CvPlot const*								// Exposed to Python
	bool isRiverNetwork(TeamTypes eTeam) const;
	// advc: isValidDomain... functions moved to CvUnit
	// <advc.opt>
	bool isImpassable() const { return m_bImpassable; } // cached									// Exposed to Python
	bool isAnyIsthmus() const { return m_bAnyIsthmus; } // Note: always false for land plots
	void updateAnyIsthmus(); // </advc.opt>

	DllExport int getX() const { return m_iX; } // advc.inl: was "getX_INLINE"						// Exposed to Python
	DllExport int getY() const { return m_iY; } // advc.inl: was "getY_INLINE"						// Exposed to Python
	bool at(int iX, int iY) const {  return (getX() == iX && getY() == iY); }						// Exposed to Python
	PlotNumTypes plotNum() const { return (PlotNumTypes)m_iPlotNum; } // advc.opt
	int getLatitude() const;																																					// Exposed to Python
	void setLatitude(int iLatitude); // advc.tsl	(exposed to Python)
	void updateLatitude(); // advc.tsl (public for testing)
	int getFOWIndex() const;

	//int getArea() const;
	// <advc>
	CvArea& getArea() const { return *m_pArea; }
	// (This had called CvMap::getArea in BtS)
	CvArea* area() const { return m_pArea; }														// Exposed to Python
	bool isArea(CvArea const& kArea) const { return (area() == &kArea); }
	bool sameArea(CvPlot const& kPlot) const { return isArea(kPlot.getArea()); }
	void initArea(); // </advc>
	CvArea* waterArea(
			// BETTER_BTS_AI_MOD, General AI, 01/02/09, jdog5000
			bool bNoImpassable = false) const;
	CvArea* secondWaterArea() const;
	void setArea(CvArea* pArea = NULL, /* advc.310: */ bool bProcess = true);

	// doc
	CvArea* continentArea() const { return m_pContinentArea != NULL ? m_pContinentArea : m_pArea; }
	CvArea& getContinentArea() const { return m_pContinentArea != NULL ? *m_pContinentArea : *m_pArea; }
	void setContinentArea(CvArea* pContinentArea) { m_pContinentArea = pContinentArea; }
	bool isContinentArea(CvArea const& kArea) const { return (continentArea() == &kArea); }
	bool sameContinentArea(CvPlot const& kPlot) const { return isArea(kPlot.getArea()); }

	DllExport int getFeatureVariety() const;														// Exposed to Python

	int getOwnershipDuration() const { return m_iOwnershipDuration; }								// Exposed to Python
	bool isOwnershipScore() const;																	// Exposed to Python
	void setOwnershipDuration(int iNewValue);														// Exposed to Python
	void changeOwnershipDuration(int iChange);														// Exposed to Python

	int getImprovementDuration() const { return m_iImprovementDuration; }							// Exposed to Python
	void setImprovementDuration(int iNewValue);														// Exposed to Python
	void changeImprovementDuration(int iChange);													// Exposed to Python

	int getUpgradeProgress() const																	// Exposed to Python
	{	// advc.912f (note): Now times 100, divisions at call locations not commented.
		return m_iUpgradeProgress;
	}
	int getUpgradeTimeLeft(ImprovementTypes eImprovement, PlayerTypes ePlayer) const;				// Exposed to Python
	void setUpgradeProgress(int iNewValue);															// Exposed to Python
	void changeUpgradeProgress(int iChange);														// Exposed to Python

	int getForceUnownedTimer() const { return m_iForceUnownedTimer; }								// Exposed to Python
	bool isForceUnowned() const;																	// Exposed to Python
	void setForceUnownedTimer(int iNewValue);														// Exposed to Python
	void changeForceUnownedTimer(int iChange);														// Exposed to Python

	int getCityRadiusCount() const																	// Exposed to Python
	{
		return m_iCityRadiusCount;
	}
	bool isCityRadius() const												// Exposed to Python (K-Mod: changed to bool)
	{
		return (getCityRadiusCount() > 0);
	}
	void changeCityRadiusCount(int iChange);

	bool isStartingPlot() const;																	// Exposed to Python
	void setStartingPlot(bool bNewValue);															// Exposed to Python

	DllExport bool isNOfRiver() const;																// Exposed to Python
	void setNOfRiver(bool bNewValue, CardinalDirectionTypes eRiverDir);								// Exposed to Python

	DllExport bool isWOfRiver() const;																// Exposed to Python
	void setWOfRiver(bool bNewValue, CardinalDirectionTypes eRiverDir);								// Exposed to Python

	DllExport CardinalDirectionTypes getRiverNSDirection() const;									// Exposed to Python
	DllExport CardinalDirectionTypes getRiverWEDirection() const;									// Exposed to Python

	CvPlot* getInlandCorner() const;																// Exposed to Python
	bool hasCoastAtSECorner() const;

	bool isIrrigated() const { return m_bIrrigated; }												// Exposed to Python
	void setIrrigated(bool bNewValue);
	void updateIrrigated();

	bool isPotentialCityWork() const { return m_bPotentialCityWork; }								// Exposed to Python
	bool isPotentialCityWorkForArea(CvArea const& kArea) const;										// Exposed to Python
	void updatePotentialCityWork();

	bool isShowCitySymbols() const;
	void updateShowCitySymbols();

	bool isFlagDirty() const;																		// Exposed to Python
	void setFlagDirty(bool bNewValue);																// Exposed to Python

	TeamTypes getTeam() const																																	// Exposed to Python
	{	// <advc.opt> Now cached
		return (TeamTypes)m_eTeam;
	}
	void updateTeam(); // </advc.opt>
	DllExport PlayerTypes getOwner() const // advc.inl: was "getOwnerINLINE"						// Exposed to Python
	{
		return (PlayerTypes)m_eOwner;
	}
	void setOwner(PlayerTypes eNewValue, bool bCheckUnits, bool bUpdatePlotGroup);
	// <advc>
	bool isActiveOwned() const { return (GC.getInitCore().getActivePlayer() == getOwner()); }
	bool isActiveTeam() const { return (GC.getInitCore().getActiveTeam() == getTeam()); } // </advc>
	/*  <advc.035> The returned player becomes the owner if war/peace changes
		between that player and the current owner */
	PlayerTypes getSecondOwner() const;
	void setSecondOwner(PlayerTypes eNewValue); // </advc.035>
	int exclusiveRadius(PlayerTypes ePlayer) const; // advc.099b

	bool isPlains() const; // doc

	PlotTypes getPlotType() const																	// Exposed to Python
	{
		return (PlotTypes)m_ePlotType;
	}
	DllExport bool isWater() const																	// Exposed to Python
	{
		return (getPlotType() == PLOT_OCEAN);
	}
	bool isFlatlands() const																		// Exposed to Python
	{
		return (getPlotType() == PLOT_LAND);
	}
	DllExport bool isHills() const																	// Exposed to Python
	{
		return (getPlotType() == PLOT_HILLS);
	}
	DllExport bool isPeak() const																	// Exposed to Python
	{
		return (getPlotType() == PLOT_PEAK);
	}
	void setPlotType(PlotTypes eNewValue, bool bRecalculate = true,									// Exposed to Python
			bool bRebuildGraphics = true);
	DllExport TerrainTypes getTerrainType() const													// Exposed to Python
	{
		return (TerrainTypes)m_eTerrainType;
	}
	void setTerrainType(TerrainTypes eNewValue, bool bRecalculate = true,							// Exposed to Python
			bool bRebuildGraphics = true);
	DllExport FeatureTypes getFeatureType() const													// Exposed to Python
	{
		return (FeatureTypes)m_eFeatureType;
	}  // <advc>
	bool isFeature() const
	{
		return (getFeatureType() != NO_FEATURE);
	} // </advc>
	void setFeatureType(FeatureTypes eNewValue, int iVariety = -1);									// Exposed to Python
	void setFeatureDummyVisibility(const char *dummyTag, bool show);								// Exposed to Python
	void addFeatureDummyModel(const char *dummyTag, const char *modelTag);
	void setFeatureDummyTexture(const char *dummyTag, const char *textureTag);
	CvString pickFeatureDummyTag(int mouseX, int mouseY);
	void resetFeatureModel();

	int determineVariety(FeatureTypes eFeature = NO_FEATURE) const; // doc

	DllExport BonusTypes getBonusType(TeamTypes eTeam = NO_TEAM) const;								// Exposed to Python
	BonusTypes getNonObsoleteBonusType(TeamTypes eTeam = NO_TEAM,									// Exposed to Python
			bool bCheckConnected = false) const;
	void setBonusType(BonusTypes eNewValue);														// Exposed to Python

	BonusTypes getBonusVarietyType(TeamTypes eTeam = NO_TEAM) const; // doc // TODO: implement
	void setBonusVarietyType(BonusTypes eNewValue); // doc

	DllExport ImprovementTypes getImprovementType() const											// Exposed to Python
	{
		return (ImprovementTypes)m_eImprovementType;
	}  // <advc>
	bool isImproved() const
	{
		return (getImprovementType() != NO_IMPROVEMENT);
	} // </advc>
	void setImprovementType(ImprovementTypes eNewValue,												// Exposed to Python
			bool bUpdateInFoW = false); // advc.055
	RouteTypes getRouteType() const																	// Exposed to Python
	{
		return (RouteTypes)m_eRouteType;
	}
	void setRouteType(RouteTypes eNewValue, bool bUpdatePlotGroup /*advc:*/= true);					// Exposed to Python
	void updateCityRoute(bool bUpdatePlotGroup);

	DllExport CvCity* getPlotCity() const;															// Exposed to Python
	CvCityAI* AI_getPlotCity() const;
	void setPlotCity(CvCity* pNewCity);
	void setRuinsName(CvWString const& szName); // advc.005c
	const wchar* getRuinsName() const; // advc.005c (NULL if none)
	CvCity* getWorkingCity() const;																	// Exposed to Python
	void updateWorkingCity();
	CvCity const* defaultWorkingCity() const; // advc
	CvCity* getWorkingCityOverride() const;															// Exposed to Python
	void setWorkingCityOverride(CvCity* pNewValue);
	// <advc.003u>
	CvCityAI* AI_getWorkingCity() const;
	CvCityAI* AI_getWorkingCityOverrideAI() const; // </advc.003u>

	short getRiverID() const;																		// Exposed to Python
	void setRiverID(short iNewValue);																// Exposed to Python

	int getMinOriginalStartDist() const;															// Exposed to Python
	void setMinOriginalStartDist(int iNewValue);

	int getReconCount() const;																		// Exposed to Python
	void changeReconCount(int iChange);

	int getRiverCrossingCount() const;																// Exposed to Python
	void changeRiverCrossingCount(int iChange);

	bool isHabitable(bool bIgnoreSea = false) const; // advc.300
	//short* getYield() { return m_aiYield; } // advc.enum: now an enum map
	DllExport int getYield(YieldTypes eIndex) const													// Exposed to Python
	{
		return m_aiYield.get(eIndex);
	}
	int calculateNatureYield(YieldTypes eIndex, TeamTypes eTeam /* advc: */ = NO_TEAM,				// Exposed to Python
			bool bIgnoreFeature = false, /* advc.300: */ bool bIgnoreHills = false) const;
	int calculateBestNatureYield(YieldTypes eIndex, TeamTypes eTeam) const;							// Exposed to Python
	int calculateTotalBestNatureYield(TeamTypes eTeam) const;										// Exposed to Python
	int calculateImprovementYieldChange(ImprovementTypes eImprovement,								// Exposed to Python
			 YieldTypes eYield, PlayerTypes ePlayer) const;
	int calculateYield(YieldTypes eIndex, bool bDisplay = false) const;								// Exposed to Python
	bool hasYield() const { return m_aiYield.isAnyNonDefault(); } // advc.enum							// Exposed to Python
	void updateYield();
	int calculateCityPlotYieldChange(YieldTypes eYield,
			int iYield, int iCityPopulation) const;
	// int calculateMaxYield(YieldTypes eYield) const; // disabled by K-Mod
	int getYieldWithBuild(BuildTypes eBuild, YieldTypes eYield, bool bWithUpgrade) const;

	int getCulture(CivilizationTypes eCivilization) const; // doc
	int getCulture(PlayerTypes eIndex) const { return m_aiCulture.get(eIndex); } // TODO: replace					// Exposed to Python
	int getActualCulture(CivilizationTypes eCivilization) const; // doc
	int getActualCulture(PlayerTypes ePlayer) const; // doc
	int getActualTotalCulture() const; // doc
	int getTotalCulture() const { return m_iTotalCulture; } // advc.opt
	int countTotalCulture(bool bIncludeDeadCivilizations = false) const; // TODO: resolve conflict with getTotalCulture
	int countFriendlyCulture(TeamTypes eTeam) const;
	TeamTypes findHighestCultureTeam() const;														// Exposed to Python
	PlayerTypes findHighestCulturePlayer(
			bool bAlive = false) const; // advc.035
	int calculateCulturePercent(CivilizationTypes eCivilization) const; // doc
	int calculateCulturePercent(PlayerTypes ePlayer) const;											// Exposed to Python
	int calculateOverallCulturePercent(CivilizationTypes eCivilization) const; // doc
	int calculateOverallCulturePercent(PlayerTypes ePlayer) const; // doc
	int calculateTeamCulturePercent(TeamTypes eTeam) const;											// Exposed to Python
	int calculateFriendlyCulturePercent(TeamTypes eTeam) const; // advc (for kekm.7)
	void setCulture(CivilizationTypes eCivilization, int iNewValue, bool bUpdate, bool bUpdatePlotGroup); // doc
	void setCulture(PlayerTypes eIndex, int iNewValue, bool bUpdate,								// Exposed to Python
			bool bUpdatePlotGroups);
	void changeCulture(PlayerTypes eIndex, int iChange, bool bUpdate);								// Exposed to Python

	CivilizationTypes getCultureConversionCivilization() const; // doc
	bool isCultureConversionPlayer(PlayerTypes ePlayer) const; // doc
	bool isDifferentCultureConversionPlayer(PlayerTypes ePlayer) const; // doc
	int getCultureConversionRate() const; // doc
	void changeCultureConversionRate(int iChange); // doc
	void setCultureConversion(CivilizationTypes eCivilization, int iRate); // doc
	void setCultureConversion(PlayerTypes ePlayer, int iRate); // doc
	void resetCultureConversion(); // doc

	int countNumAirUnits(TeamTypes eTeam) const;													// Exposed to Python
	int airUnitSpaceAvailable(TeamTypes eTeam) const;
	// <advc.081>
	int countHostileUnits(PlayerTypes ePlayer, bool bPlayer, bool bTeam,
			bool bNeutral, bool bHostile) const; // </advc.081>
	int getFoundValue(PlayerTypes eIndex,															// Exposed to Python
			bool bRandomize = false) const; // advc.052
	bool isBestAdjacentFound(PlayerTypes eIndex) const;												// Exposed to Python
	void setFoundValue(PlayerTypes eIndex, short iNewValue); // K-Mod (was int iNewValue)
	bool canFound(bool bTestVisible = false, TeamTypes eTeam = NO_TEAM) const; // advc
	bool canEverFound() const; // advc.129d

	int getPlayerCityRadiusCount(PlayerTypes eIndex) const											// Exposed to Python
	{
		return m_aiPlayerCityRadiusCount.get(eIndex);
	}
	bool isPlayerCityRadius(PlayerTypes eIndex) const												// Exposed to Python
	{
		return (getPlayerCityRadiusCount(eIndex) > 0);
	}
	void changePlayerCityRadiusCount(PlayerTypes eIndex, int iChange);

	CvPlotGroup* getPlotGroup(PlayerTypes ePlayer) const;
	// advc.inl: New function. Can't inline the above w/o including CvPlayer.h.
	bool isSamePlotGroup(CvPlot const& kOther, PlayerTypes ePlayer) const
	{
		return (m_aiPlotGroup.get(ePlayer) == kOther.m_aiPlotGroup.get(ePlayer));
	}
	CvPlotGroup* getOwnerPlotGroup() const;
	void setPlotGroup(PlayerTypes ePlayer, CvPlotGroup* pNewValue,
			bool bVerifyProduction = true); // advc.064d
	void updatePlotGroup(/* advc.064d: */ bool bVerifyProduction = false);
	void updatePlotGroup(PlayerTypes ePlayer, bool bRecalculate = true,
			bool bVerifyProduction = true); // advc.064d

	int getVisibilityCount(TeamTypes eTeam) const													// Exposed to Python
	{
		return m_aiVisibilityCount.get(eTeam);
	}
	void changeVisibilityCount(TeamTypes eTeam, int iChange,										// Exposed to Python
			InvisibleTypes eSeeInvisible, bool bUpdatePlotGroups,
			CvUnit const* pUnit = NULL); // advc.071
	int getStolenVisibilityCount(TeamTypes eTeam) const												// Exposed to Python
	{
		return m_aiStolenVisibilityCount.get(eTeam);
	}
	void changeStolenVisibilityCount(TeamTypes eTeam, int iChange);
	int getBlockadedCount(TeamTypes eTeam) const													// Exposed to Python
	{
		return m_aiBlockadedCount.get(eTeam);
	}
	void changeBlockadedCount(TeamTypes eTeam, int iChange);

	DllExport PlayerTypes getRevealedOwner(TeamTypes eTeam, bool bDebug) const;						// Exposed to Python
	// advc.inl: Faster implementation for non-UI code
	PlayerTypes getRevealedOwner(TeamTypes eTeam) const
	{
		return m_aiRevealedOwner.get(eTeam);
	}
	TeamTypes getRevealedTeam(TeamTypes eTeam, bool bDebug) const;									// Exposed to Python
	void setRevealedOwner(TeamTypes eTeam, PlayerTypes eNewValue);
	void updateRevealedOwner(TeamTypes eTeam);
	CvPlot* plotThatRevealsOwner(TeamTypes eTeam) const; // advc.071

	DllExport bool isRiverCrossing(DirectionTypes eDirection) const									// Exposed to Python+
	{
		/*if (eDirection == NO_DIRECTION)
			return false;*/ // advc.opt: Apparently not needed, so:
		FAssertBounds(0, NUM_DIRECTION_TYPES, eDirection);
		return m_abRiverCrossing.get(eDirection);
	}
	void updateRiverCrossing(DirectionTypes eDirection);
	void updateRiverCrossing();

	DllExport bool isRevealed(TeamTypes eTeam, bool bDebug) const;									// Exposed to Python
	// advc.inl: Faster implementation for non-UI code
	bool isRevealed(TeamTypes eTeam) const
	{
		return m_abRevealed.get(eTeam);
	}
	void setRevealed(TeamTypes eTeam, bool bNewValue, bool bTerrainOnly,							// Exposed to Python
			TeamTypes eFromTeam, bool bUpdatePlotGroup);
	bool isAdjacentRevealed(TeamTypes eTeam,														// Exposed to Python
			bool bSkipOcean = false) const; // advc.250c
	bool isAdjacentNonrevealed(TeamTypes eTeam) const;												// Exposed to Python

	ImprovementTypes getRevealedImprovementType(TeamTypes eTeam, bool bDebug) const;				// Exposed to Python
	// advc.inl: Faster implementation for non-UI code
	ImprovementTypes getRevealedImprovementType(TeamTypes eTeam) const
	{
		return m_aeRevealedImprovementType.get(eTeam);
	}
	void setRevealedImprovementType(TeamTypes eTeam, ImprovementTypes eNewValue);
	RouteTypes getRevealedRouteType(TeamTypes eTeam, bool bDebug) const;							// Exposed to Python
	// advc.inl: Faster implementation for non-UI code
	RouteTypes getRevealedRouteType(TeamTypes eTeam) const
	{
		return m_aeRevealedRouteType.get(eTeam);
	}
	void setRevealedRouteType(TeamTypes eTeam, RouteTypes eNewValue);
	// advc.inl:
	int getBuildProgress(BuildTypes eBuild) const													// Exposed to Python
	{
		return m_aiBuildProgress.get(eBuild);
	}
	bool changeBuildProgress(BuildTypes eBuild, int iChange,										// Exposed to Python
			//TeamTypes eTeam = NO_TEAM
			PlayerTypes ePlayer); // advc.251
	bool isBuildProgressDecaying(bool bWarn = false) const; // advc.011
	void decayBuildProgress(); // advc.011

	void updateFeatureSymbolVisibility();
	void updateFeatureSymbol(bool bForce = false);

	DllExport bool isLayoutDirty() const;
	DllExport void setLayoutDirty(bool bDirty);
	DllExport bool isLayoutStateDifferent() const;
	DllExport void setLayoutStateToCurrent();
	bool updatePlotBuilder();

	DllExport void getVisibleImprovementState(ImprovementTypes& eType, bool& bWorked);
	DllExport void getVisibleBonusState(BonusTypes& eType, bool& bImproved, bool& bWorked);
	bool shouldUsePlotBuilder();
	CvPlotBuilder* getPlotBuilder() { return m_pPlotBuilder; }

	DllExport CvRoute* getRouteSymbol() const;
	void updateRouteSymbol(bool bForce = false, bool bAdjacent = false);

	DllExport CvRiver* getRiverSymbol() const;
	void updateRiverSymbol(bool bForce = false, bool bAdjacent = false);
	void updateRiverSymbolArt(bool bAdjacent = true);

	CvFeature* getFeatureSymbol() const;

	DllExport CvFlagEntity* getFlagSymbol() const;
	CvFlagEntity* getFlagSymbolOffset() const;
	DllExport void updateFlagSymbol();
	void clearFlagSymbol(); // advc.127c

	DllExport CvUnit* getCenterUnit() const { return m_pCenterUnit; }
	DllExport CvUnit* getDebugCenterUnit() const;
	bool setCenterUnit(CvUnit* pNewValue);

	int getCultureRangeCities(PlayerTypes eOwnerIndex,												// Exposed to Python
		CultureLevelTypes eRangeIndex) const // advc.enum
	{
		return m_aaiCultureRangeCities.get(eOwnerIndex, eRangeIndex);
	}
	bool isCultureRangeCity(PlayerTypes eOwnerIndex,												// Exposed to Python
		CultureLevelTypes eRangeIndex) const // advc.enum
	{
		return (getCultureRangeCities(eOwnerIndex, eRangeIndex) > 0);
	}
	void changeCultureRangeCities(PlayerTypes eOwnerIndex, CultureLevelTypes eRangeIndex,
			int iChange, bool bUpdatePlotGroups);
	int getInvisibleVisibilityCount(TeamTypes eTeam,												// Exposed to Python
		InvisibleTypes eInvisible) const
	{
		return m_aaiInvisibleVisibilityCount.get(eTeam, eInvisible);
	}
	bool isInvisibleVisible(TeamTypes eTeam,														// Exposed to Python
		InvisibleTypes eInvisible) const
	{
		return (getInvisibleVisibilityCount(eTeam, eInvisible) > 0);
	}
	void changeInvisibleVisibilityCount(TeamTypes eTeam,											// Exposed to Python
			InvisibleTypes eInvisible, int iChange);

	int getNumUnits() const { return m_units.getLength(); }											// Exposed to Python
	void addUnit(CvUnit const& kUnit, bool bUpdate = true);
	void removeUnit(CvUnit* pUnit, bool bUpdate = true);
	DllExport CLLNode<IDInfo>* headUnitNode() const
	{
		return m_units.head();
	}
	CLLNode<IDInfo>* tailUnitNode() const
	{
		return m_units.tail();
	}
	CvUnit* headUnit() const { return getUnitByIndex(0); }
	// <advc.003s>
	// Exported through .def file ...
	CLLNode<IDInfo>* nextUnitNodeExternal(CLLNode<IDInfo>* pNode) const;
	// Safer to use const/ non-const pairs of functions
	CLLNode<IDInfo> const* nextUnitNode(CLLNode<IDInfo> const* pNode) const
	{
		return m_units.next(pNode);
	}
	CLLNode<IDInfo>* nextUnitNode(CLLNode<IDInfo>* pNode) const
	{
		return m_units.next(pNode);
	}
	CLLNode<IDInfo> const* prevUnitNode(CLLNode<IDInfo> const* pNode) const
	{
		return m_units.prev(pNode);
	}
	CLLNode<IDInfo>* prevUnitNode(CLLNode<IDInfo>* pNode) const
	{
		return m_units.prev(pNode);
	}
	// </advc.003s>

	int getNumSymbols() const { return m_symbols.size(); }
	CvSymbol* getSymbol(int iID) const;
	CvSymbol* addSymbol();

	void deleteSymbol(int iID);
	void deleteAllSymbols();

	// Script data needs to be a narrow string for pickling in Python
	CvString getScriptData() const;																	// Exposed to Python
	void setScriptData(const char* szNewValue);														// Exposed to Python

	bool canTrigger(EventTriggerTypes eTrigger, PlayerTypes ePlayer) const;
	bool canApplyEvent(EventTypes eEvent) const;
	void applyEvent(EventTypes eEvent);

	bool canTrain(UnitTypes eUnit, bool bContinue, bool bTestVisible,
			bool bCheckAirUnitCap = true, // advc.001b
			BonusTypes eAssumeAvailable = NO_BONUS) const; // advc.001u
	bool canConstruct(BuildingTypes eBuilding) const; // advc
	bool isEspionageCounterSpy(TeamTypes eTeam) const;

	DllExport int getAreaIdForGreatWall() const;
	DllExport int getSoundScriptId() const;
	DllExport int get3DAudioScriptFootstepIndex(int iFootstepTag) const;
	DllExport float getAqueductSourceWeight() const;  // used to place aqueducts on the map
	DllExport bool shouldDisplayBridge(CvPlot* pToPlot, PlayerTypes ePlayer) const;
	DllExport bool checkLateEra() const;
	void killRandomUnit(PlayerTypes eOwner, DomainTypes eDomain); // advc.300

	/*	<advc.003s> No assertion of iAt being within array bounds; should
		call this only via a FOR_EACH_ADJ_PLOT macro (PlotAdjListTraversal.h). */
	CvPlot* getAdjacentPlotUnchecked(int iAt) const
	{
		//FAssertBounds(0, numAdjacentPlots(), iAt);
		return m_paAdjList[iAt];
	}
	int numAdjacentPlots() const { return m_iAdjPlots; }
	// </advc.003s>

	wchar const* debugStr() const; // advc.031c

	void read(FDataStreamBase* pStream);
	void write(FDataStreamBase* pStream);
	// advc.003h: Adopted from We The People mod (devolution)
	static void setMaxVisibilityRangeCache();

	int getRegionID() const; // doc // TODO: implement
	void setRegionID(int iNewValue); // doc
	CvWString getRegionName() const; // doc

	bool isCore(CivilizationTypes eCivilization) const; // doc // TODO: implement
	bool isCore(PlayerTypes ePlayer) const; // doc
	bool isCore() const; // doc
	void setCore(CivilizationTypes eCivilization, bool bNewValue); // doc

	int getSettlerValue(CivilizationTypes eCivilization) const; // doc // TODO: implement
	int getSettlerValue(PlayerTypes ePlayer) const; // doc
	void setSettlerValue(CivilizationTypes eCivilization, int iNewValue); // doc

	int getWarValue(CivilizationTypes eCivilization) const; // doc // TODO: implement
	int getWarValue(PlayerTypes ePlayer) const; // doc
	void setWarValue(CivilizationTypes eCivilization, int iNewValue); // doc

	int getSpreadFactor(ReligionTypes eReligion) const; // doc // TODO: implement
	void setSpreadFactor(ReligionTypes eReligion, int iNewValue); // doc

	bool isWithinGreatWall() const; // doc // TODO: implement
	void setWithinGreatWall(bool bNewValue); // doc
	void cameraLookAt(); // doc
	bool canUseSlave(PlayerTypes ePlayer) const; // doc
	int calculateCultureCost() const; // doc

	int getReligionInfluence(ReligionTypes eReligion) const; // doc // TODO: implement
	void setReligionInfluence(ReligionTypes eReligion, int iNewValue); // doc
	void changeReligionInfluence(ReligionTypes eReligion, int iChange); // doc

	bool canSpread(ReligionTypes eReligion) const; // doc

	bool isOverseas(CvPlot const& pPlot) const; // doc

	void setBirthProtected(PlayerTypes ePlayer); // doc
	void resetBirthProtected(); // doc
	PlayerTypes getBirthProtected() const; // doc // TODO: implement
	bool isBirthProtected() const; // doc // TODO: implement

	void setExpansion(PlayerTypes ePlayer); // doc
	void resetExpansion(); // doc
	PlayerTypes getExpansion() const; // doc // TODO: implement
	bool isExpansion() const; // doc // TODO: implement
	bool isExpansionEffect(PlayerTypes ePlayer) const; // doc

	int getContinentID() const; // doc
	int getRegionGroup() const; // doc
	bool isNewWorld() const; // doc

	static int getRegionGroupForRegion(int iRegion); // doc

	bool isSlaveImprovement() const; // doc

protected:
	/*	advc (note): Should keep the data members in an order that optimizes
		the memory layout (packing, locality). While enum types can be declared
		as bitfields (:8 or :16), it seems that e.g. a short int and a 16-bit enum
		won't get packed without padding by the compiler; so I think it's better
		to stick to char and short. */
	short m_iX;
	short m_iY;
	PlotNumInt m_iPlotNum; // advc.opt: worth caching
	short m_iFeatureVariety;
	short m_iOwnershipDuration;
	short m_iImprovementDuration;
	short m_iForceUnownedTimer;
	short m_iTurnsBuildsInterrupted; // advc.011
	short m_iReconCount;
	short /*BonusTypes*/ m_eBonusType;
	short /*BonusTypes*/ m_eBonusVarietyType; // doc
	short m_iRiverID; // advc.opt: Was int. Only used during map gen.
	/*	advc (note): Only Boreal, Highlands and Rainforest use this value
		(during map gen). Could probably save 4 byte here by placing this
		and m_iRiverID in unions with e.g. m_iReconCount, m_iForceUnownedTimer. */
	short m_iMinOriginalStartDist;

	// BETTER_BTS_AI_MOD, Efficiency (plot danger cache), 08/21/09, jdog5000:
	//bool m_bActivePlayerNoDangerCache;
	// K-Mod (the bbai implementation was flawed):
	// advc.opt: char. It's also unused now, but since there would be padding here anyway ...
	mutable char m_iActivePlayerSafeRangeCache;

	// advc.opt: These two were short int
	char m_iCityRadiusCount;
	char m_iRiverCrossingCount;

	int m_iContinentArea; // doc
	short m_iCultureConversionRate; // doc

	bool m_bStartingPlot:1;
	bool m_bNOfRiver:1;
	bool m_bWOfRiver:1;
	bool m_bIrrigated:1;
	bool m_bImpassable:1; // advc.opt
	bool m_bAnyIsthmus:1; // advc.opt
	bool m_bPotentialCityWork:1;
	bool m_bShowCitySymbols:1;

	bool m_bFlagDirty:1;
	bool m_bPlotLayoutDirty:1;
	bool m_bLayoutStateWorked:1;

	char /*TeamTypes*/ m_eTeam; // advc.opt: cache the owner's team
	char m_iLatitude; // advc.tsl
	// advc.opt: These five were short int
	char /*PlayerTypes*/ m_eOwner;
	char /*CivilizationTypes*/ m_eCultureConversionCivilization; // doc
	char /*PlayerTypes*/ m_eBirthProtected; // doc
	char /*PlayerTypes*/ m_eExpansion; // doc
	char /*PlotTypes*/ m_ePlotType;
	char /*TerrainTypes*/ m_eTerrainType;
	char /*FeatureTypes*/ m_eFeatureType;
	char /*RouteTypes*/ m_eRouteType;
	char /*ImprovementTypes*/ m_eImprovementType;
	char /*CardinalDirectionTypes*/ m_eRiverNSDirection;
	char /*CardinalDirectionTypes*/ m_eRiverWEDirection;
	char /*PlayerTypes*/ m_eSecondOwner; // advc.035

	char m_iAdjPlots; // advc.opt

	// advc.912f: Was short - which would overflow too easily at times-100 precision.
	int m_iUpgradeProgress;
	int m_iTotalCulture; // advc.opt

	CvPlot** m_paAdjList; // advc.003s (a vector would take up 16 byte)
	// <advc> m_pArea is enough - except while loading a savegame.
	union
	{
		CvArea* m_pArea; // This acted as a cache in BtS (was mutable)
		int m_iArea;
	}; // </advc>
	CvArea* m_pContinentArea; // doc
	/*	advc (note): These aren't CvCity pointers b/c of the order of deserialization.
		Could use the same pattern as above (union) though. */
	IDInfo m_plotCity;
	IDInfo m_workingCity;
	IDInfo m_workingCityOverride;

	wchar const* m_szMostRecentCityName; // advc.005c (wstring takes up 28 byte!)
	char const* m_szScriptData; // advc: const
	// <advc.enum>
	// BETTER_BTS_AI_MOD, Efficiency (plot danger cache), 08/21/09, jdog5000:
	mutable ArrayEnumMap<TeamTypes,bool> m_abBorderDangerCache;

	YieldChangeMap m_aiYield;
	ArrayEnumMap<PlayerTypes,int> m_aiCulture;
	ArrayEnumMap<PlayerTypes,int,int,FFreeList::INVALID_INDEX> m_aiPlotGroup;
	mutable ArrayEnumMap<PlayerTypes,short> m_aiFoundValue; // advc: mutable
	ListEnumMap<PlayerTypes,int,char> m_aiPlayerCityRadiusCount;
	ArrayEnumMap<TeamTypes,int,short> m_aiVisibilityCount;
	ListEnumMap<TeamTypes,int,short> m_aiStolenVisibilityCount;
	ListEnumMap<TeamTypes,int,short> m_aiBlockadedCount;
	ArrayEnumMap<TeamTypes,PlayerTypes> m_aiRevealedOwner;
	ListEnumMap<TeamTypes,ImprovementTypes> m_aeRevealedImprovementType;
	ArrayEnumMap<TeamTypes,RouteTypes> m_aeRevealedRouteType;
	ArrayEnumMap<TeamTypes,bool> m_abRevealed;
	ArrayEnumMap<DirectionTypes,bool> m_abRiverCrossing;
	ArrayEnumMap<BuildTypes,short> m_aiBuildProgress;
	ListEnumMap2D<PlayerTypes,CultureLevelTypes,char> m_aaiCultureRangeCities;
	ListEnumMap2D<TeamTypes,InvisibleTypes,short> m_aaiInvisibleVisibilityCount;

	// doc: initialized by Python at the beginning of the game
	ListEnumMap<CivilizationTypes,bool,byte> m_abCore; // doc
	ListEnumMap<CivilizationTypes,int,byte> m_aiSettlerValue; // doc
	ListEnumMap<CivilizationTypes,int,byte> m_aiWarValue; // doc
	ListEnumMap<ReligionTypes,int,byte> m_aiReligionSpreadFactor; // doc
	ListEnumMap<ReligionTypes,int,short> m_aiReligionInfluence; // doc
	byte m_iRegionID; // doc
	byte m_bWithinGreatWall; // doc

	// </advc.enum>
	CvFeature* m_pFeatureSymbol;
	CvRoute* m_pRouteSymbol;
	CvRiver* m_pRiverSymbol;
	CvFlagEntity* m_pFlagSymbol;
	CvFlagEntity* m_pFlagSymbolOffset;
	CvUnit* m_pCenterUnit;
	CvPlotBuilder* m_pPlotBuilder; // builds bonus resources and improvements

	CLinkList<IDInfo> m_units;
	std::vector<CvSymbol*> m_symbols;

	static bool m_bAllFog; // advc.706
	static int m_iMaxVisibilityRangeCache; // advc.003h

	void doFeature();
	void doCulture();

	int areaID() const;
	void processArea(CvArea& kArea, int iChange);
	char calculateLatitude() const; // advc.tsl
	void doCultureDecay(); // advc.099b
	ColorTypes plotMinimapColor();
	void updateImpassable(); // advc.opt
	void updatePlotNum(); // advc.opt

	/*	advc: protected b/c iteration through headUnitNode/ nextUnitNode is faster.
		Iteration by index is needed for Python export though. */
	CvUnit* getUnitByIndex(int iIndex) const;															// Exposed to Python

	friend class CyPlot; // advc (see above)
	// added so under cheat mode we can access protected stuff
	friend class CvGameTextMgr;
};

// advc.opt: It's fine to change the size, but might want to double check if it can be avoided.
BOOST_STATIC_ASSERT(MAX_PLOT_NUM > MAX_SHORT || sizeof(CvPlot) <= 268);

/*	advc.enum: For functions that choose random plots.
	Moved from CvDefines, turned into an enum, exposed to Python. */
enum RandPlotFlags
{
	RANDPLOT_ANY = 0,
	RANDPLOT_LAND =						(1 << 0),
	RANDPLOT_UNOWNED =					(1 << 1),
	RANDPLOT_ADJACENT_UNOWNED =			(1 << 2),
	RANDPLOT_ADJACENT_LAND =			(1 << 3),
	RANDPLOT_PASSABLE =					(1 << 4),
	RANDPLOT_NOT_VISIBLE_TO_CIV =		(1 << 5),
	RANDPLOT_NOT_CITY =					(1 << 6),
	// <advc.300>
	RANDPLOT_HABITABLE =				(1 << 7),
	RANDPLOT_WATERSOURCE =				(1 << 8),
	// </advc.300>
};
OVERLOAD_BITWISE_OPERATORS(RandPlotFlags)

#endif
