#pragma once

#ifndef CIV4_SELECTION_GROUP_H
#define CIV4_SELECTION_GROUP_H

class GroupPathFinder;
class CvMap;
class CvPlot;
class CvArea;
class FAStarNode;
class CvSelectionGroupAI; // advc.003u


class CvSelectionGroup /* advc.003k: */ : private boost::noncopyable
{
public:
	// <advc.pf>
	static GroupPathFinder& pathFinder()
	{
		return *m_pPathFinder;
	}
	static GroupPathFinder& getClearPathFinder(); // advc.opt
	static void initPathFinder();
	static void uninitPathFinder(); // </advc.pf>
	/*	(disabled by K-mod. Use pathFinder().Reset instead. was exposed to Python.
		note: the K-Mod finder doesn't need resetting in all the same places.)
		advc: I'm not going to expose it to Python again, but, in the DLL, it's helpful
		as a (static) wrapper for avoiding inclusion of the GroupPathFinder header. */
	static void resetPath();

	CvSelectionGroup();
	virtual ~CvSelectionGroup();

	DllExport void init(int iID, PlayerTypes eOwner);
	DllExport void uninit();
	DllExport void reset(int iID = 0, PlayerTypes eOwner = NO_PLAYER, bool bConstructorCall = false);
	void kill();
	void invalidateGroupPaths(); // advc.pf

	void doTurn();
	void doTurnPost(); // advc.004l
	bool showMoves( /* <advc.102> */ CvPlot const& kFromPlot) const;
	int nukeMissionTime() const; // advc.002m
	void setInitiallyVisible(bool b); // </advc.102>

	void updateTimers();
	bool doDelayedDeath();

	void playActionSound();

	void pushMission(MissionTypes eMission, int iData1 = -1, int iData2 = -1,							// Exposed to Python
			MovementFlags eFlags = NO_MOVEMENT_FLAGS,
			bool bAppend = false, bool bManual = false, MissionAITypes eMissionAI = NO_MISSIONAI,
			CvPlot const* pMissionAIPlot = NULL, CvUnit const* pMissionAIUnit = NULL,
			bool bModified = false); // advc.011b
	void popMission();																																										// Exposed to Python
	//DllExport void autoMission();
	bool autoMission(); // K-Mod. (No 'DllExport'? Are you serious!?)
	void updateMission();
	DllExport CvPlot* lastMissionPlot()																	// Exposed to Python
	{	// <advc>
		CvSelectionGroup const& kThis = *this;
		return kThis.lastMissionPlot();
	}
	CvPlot* lastMissionPlot() const; // </advc>

	bool canStartMission(MissionTypes eMission, int iData1, int iData2,									// Exposed to Python
			CvPlot const* pPlot = NULL, bool bTestVisible = false,
			bool bUseCache = false) const;
	void startMission();
	//void continueMission(int iSteps = 0);
	// K-Mod: Split continueMission into two functions to remove the recursion.
	void continueMission();

	DllExport bool canDoInterfaceMode(InterfaceModeTypes eInterfaceMode);													// Exposed to Python
	DllExport bool canDoInterfaceModeAt(InterfaceModeTypes eInterfaceMode, CvPlot* pPlot);				// Exposed to Python

	bool canDoCommand(CommandTypes eCommand, int iData1, int iData2, bool bTestVisible = false, bool bUseCache = false);		// Exposed to Python
	bool canEverDoCommand(CommandTypes eCommand, int iData1, int iData2, bool bTestVisible, bool bUseCache);
	void setupActionCache();

	bool isHuman() const; // advc.002i: const																																									// Exposed to Python

	DllExport bool isBusy()
	// <advc> Need a const version of this
	{	CvSelectionGroup const& kThis = *this;
		return kThis.isBusy();
	} bool isBusy() const; // </advc>
	bool isCargoBusy() const;
	int baseMoves() const;																																										// Exposed to Python
	int maxMoves() const; // K-Mod
	int movesLeft() const; // K-Mod
	bool isWaiting() const;																																							// Exposed to Python
	// <advc> K-Mod functions moved from CvGameCoreUtils. (Kept isCycleGroup inlined as in K-Mod.)
	bool isCycleGroup() const { return getNumUnits() > 0 && !isWaiting() && !isAutomated(); }
	bool isBeforeGroupOnPlot(CvSelectionGroup const& kOther) const;
	int groupCycleDistance(CvSelectionGroup const& kOther) const; // </advc>
	bool isFull() const;																																											// Exposed to Python
	bool hasCargo() const;																																										// Exposed to Python
	int getCargo() const;
	int getCargoSpace() const; // advc.102b
	int cargoSpaceAvailable(SpecialUnitTypes eSpecialCargo = NO_SPECIALUNIT, DomainTypes eDomainCargo = NO_DOMAIN) const; // K-Mod
	DllExport bool canAllMove()																																				// Exposed to Python
	// <advc> Need a const version fo this
	{	CvSelectionGroup const& kThis = *this;
		return kThis.canAllMove();
	} bool canAllMove() const; // </advc>
	bool canAnyMove() const; // Exposed to Python
	bool canCargoAllMove() const; // K-Mod (moved from CvUnit)
	bool hasMoved() const; // Exposed to Python
	bool canEnterTerritory(TeamTypes eTeam, bool bIgnoreRightOfPassage = false) const;									// Exposed to Python
	bool canEnterArea(TeamTypes eTeam, CvArea const& kArea, bool bIgnoreRightOfPassage = false) const;					// Exposed to Python
	DllExport bool canMoveInto(CvPlot* pPlot, bool bAttack = false)														// Exposed to Python
	{	// <advc>
		return canMoveInto(*pPlot, bAttack);
	}
	bool canMoveInto(CvPlot const& kPlot, bool bAttack = false) const; // </advc>
	DllExport bool canMoveOrAttackInto(CvPlot* pPlot, bool bDeclareWar = false)											// Exposed to Python
	{
		return canMoveOrAttackInto(*pPlot, bDeclareWar, false);
	} // K-Mod. (Avoid breaking the DllExport; EXE calls the above for NumPad help.)
	bool canMoveOrAttackInto(CvPlot const& kPlot, bool bDeclareWar = false,
			bool bCheckMoves = false, bool bAssumeVisible = true) const;
	bool canMoveThrough(CvPlot const& kPlot,																			// Exposed to Python
			bool bDeclareWar = false, bool bAssumeVisible = true) const; // K-Mod
	bool canFight() const;																																										// Exposed to Python
	bool canDefend() const;																																										// Exposed to Python
	bool canBombard(CvPlot const& kPlot) const;
	int visibilityRange() const;
	// (advc: Other BBAI functions from same date moved to CvSelectionGroupAI)
	bool canMoveAllTerrain() const; // BETTER_BTS_AI_MOD, General AI, 08/19/09, jdog5000

	void unloadAll();
	bool alwaysInvisible() const;																											// Exposed to Python
	bool isInvisible(TeamTypes eTeam) const;																								// Exposed to Python
	int countNumUnitAIType(UnitAITypes eUnitAI) const;																						// Exposed to Python
	bool hasWorker() const;																														// Exposed to Python
	bool hasWorkerWithMoves() const; // advc.153
	bool IsSelected() const;
	DllExport void NotifyEntity(MissionTypes eMission);
	void airCircle(bool bStart);
	void setBlockading(bool bStart);

	int getX() const;
	int getY() const;
	bool at(int iX, int iY) const																											// Exposed to Python
	{
		return(getX() == iX && getY() == iY);
	}
	bool atPlot(CvPlot const* pPlot) const																									// Exposed to Python
	{
		return (plot() == pPlot);
	}  // advc.inl:
	bool at(CvPlot const& kPlot) const
	{
		return atPlot(&kPlot);
	}
	DllExport CvPlot* plot() const;																											// Exposed to Python
	CvPlot& getPlot() const { return *plot(); } // advc
	//int getArea() const; // advc: removed
	CvArea* area() const;																													// Exposed to Python
	DomainTypes getDomainType() const;

	RouteTypes getBestBuildRoute(CvPlot const& kPlot, BuildTypes* peBestBuild = NULL) const;	// Exposed to Python

	//bool groupDeclareWar(CvPlot* pPlot, bool bForce = false); // deleted by K-Mod
	bool groupAttack(int iX, int iY, MovementFlags eFlags, bool& bFailedAlreadyFighting,
			bool bMaxSurvival = false); // advc.048
	void groupMove(CvPlot* pPlot, bool bCombat, CvUnit* pCombatUnit = NULL, bool bEndMove = false);
	bool groupPathTo(int iX, int iY, MovementFlags eFlags);
	bool groupRoadTo(int iX, int iY, MovementFlags eFlags);
	bool groupBuild(BuildTypes eBuild, /* advc.011b: */ bool bFinish = true);

	void setTransportUnit(CvUnit* pTransportUnit,
			CvSelectionGroup** pOtherGroup = NULL); // BBAI
	//void setRemoteTransportUnit(CvUnit* pTransportUnit); // BBAI; deleted by K-Mod.

	bool isAmphibPlot(CvPlot const* pPlot) const;																																		// Exposed to Python
	bool groupAmphibMove(CvPlot const& kPlot, MovementFlags eFlags);

	DllExport bool readyToSelect(bool bAny = false);														// Exposed to Python
	bool readyToMove(bool bAny = false) const; // Exposed to Python
	bool readyToAuto() const; // Exposed to Python
	// K-Mod.
	bool readyForMission() const;
	bool canDoMission(MissionTypes eMission, int iData1, int iData2, CvPlot const* pPlot,
			bool bTestVisible, bool bCheckMoves) /* advc.002i: */ const;
	// K-Mod end

	int getID() const { return m_iID; }															// Exposed to Python
	void setID(int iID);
	IDInfo getIDInfo() const { return IDInfo(getOwner(), getID()); } // advc

	int getMissionTimer() const;
	void setMissionTimer(int iNewValue);
	void changeMissionTimer(int iChange);
	void updateMissionTimer(int iSteps = 0, /* advc.102: */ CvPlot* pFromPlot = NULL);

	bool isForceUpdate() const { return m_bForceUpdate; } // K-Mod made inline // advc: const
	void setForceUpdate(bool bNewValue) { m_bForceUpdate = bNewValue; } // K-Mod made inline
	// void doForceUpdate(); // K-Mod. (disabled. force update doesn't work the same way anymore.)

	//DllExport PlayerTypes getOwner() const; // advc.inl: Not called externally
	PlayerTypes getOwner() const { return m_eOwner; } // advc.inl: was "getOwnerINLINE"
	TeamTypes getTeam() const;																				// Exposed to Python
	// <advc>
	bool isActiveOwned() const { return (GC.getInitCore().getActivePlayer() == getOwner()); }
	bool isActiveTeam() const { return (GC.getInitCore().getActiveTeam() == getTeam()); } // </advc>

	ActivityTypes getActivityType() const { return m_eActivityType; } 										// Exposed to Python
	void setActivityType(ActivityTypes eNewValue);																											// Exposed to Python

	AutomateTypes getAutomateType() const { return m->eAutomateType; }																									// Exposed to Python
	bool isAutomated() const { return (getAutomateType() != NO_AUTOMATE); }							// Exposed to Python
	void setAutomateType(AutomateTypes eNewValue);																											// Exposed to Python

	// FAStarNode* getPathLastNode() const; // disabled by K-Mod. Use pathFinder() instead.
	CvPlot& getPathFirstPlot() const;																																		// Exposed to Python
	CvPlot& getPathEndTurnPlot() const;																																	// Exposed to Python
	bool generatePath(CvPlot const& kFrom, CvPlot const& kTo,										// Exposed to Python
			MovementFlags eFlags = NO_MOVEMENT_FLAGS,
			bool bReuse = false, int* piPathTurns = NULL,
			int iMaxPath = -1, // K-Mod
			bool bUseTempFinder = false) const; // advc.128

	DllExport void clearUnits();
	DllExport bool addUnit(CvUnit* pUnit, bool bMinimalChange);
	void removeUnit(CvUnit* pUnit);
	void mergeIntoGroup(CvSelectionGroup* pSelectionGroup);
	CvSelectionGroup* splitGroup(int iSplitSize, CvUnit* pNewHeadUnit = NULL, CvSelectionGroup** ppOtherGroup = NULL);
	void regroupSeparatedUnits(); // K-Mod

	DllExport CLLNode<IDInfo>* deleteUnitNode(CLLNode<IDInfo>* pNode);
	// <advc.003s>
	// Exported through .def file ...
	CLLNode<IDInfo>* nextUnitNodeExternal(CLLNode<IDInfo>* pNode) const;
	CLLNode<IDInfo>* headUnitNodeExternal() const;
	CvUnit* getHeadUnitExternal() const;
	// Safer to use const/ non-const pairs of functions
	CLLNode<IDInfo> const* nextUnitNode(CLLNode<IDInfo> const* pNode) const
	{
		return m_units.next(pNode);
	}
	CLLNode<IDInfo>* nextUnitNode(CLLNode<IDInfo>* pNode)
	{
		return m_units.next(pNode);
	}
	CLLNode<IDInfo> const* headUnitNode() const
	{
		return m_units.head();
	}
	CLLNode<IDInfo>* headUnitNode()
	{
		return m_units.head();
	}
	CvUnit const* getHeadUnit() const;
	CvUnit* getHeadUnit();
	// </advc.003s>
	DllExport int getNumUnits() const														// Exposed to Python
	{
		return m_units.getLength();
	}
	DllExport int getUnitIndex(CvUnit* pUnit, int iMaxIndex = -1) const;
	UnitAITypes getHeadUnitAIType() const; // advc.003u: renamed from "getHeadUnitAI"
	PlayerTypes getHeadOwner() const;
	TeamTypes getHeadTeam() const;

	void clearMissionQueue();																																	// Exposed to Python
	int getLengthMissionQueue() const { return m_missionQueue.getLength(); }						// Exposed to Python
	MissionData* getMissionFromQueue(int iIndex) const;												// Exposed to Python
	void insertAtEndMissionQueue(MissionData mission, bool bStart = true);
	CLLNode<MissionData>* deleteMissionQueueNode(CLLNode<MissionData>* pNode);
	DllExport CLLNode<MissionData>* nextMissionQueueNode(CLLNode<MissionData>* pNode) const
	{
		return m_missionQueue.next(pNode);
	}
	CLLNode<MissionData>* prevMissionQueueNode(CLLNode<MissionData>* pNode) const
	{
		return m_missionQueue.prev(pNode);
	}
	DllExport CLLNode<MissionData>* headMissionQueueNode() const { return m_missionQueue.head(); }
	CLLNode<MissionData>* tailMissionQueueNode() const { return m_missionQueue.tail(); }
	MissionTypes getMissionType(int iNode) const;																														// Exposed to Python
	int getMissionData1(int iNode) const;																														// Exposed to Python
	int getMissionData2(int iNode) const;																														// Exposed to Python
	// <advc.003u>
	/*	Was CvSelectionGroupAI::AI_isControlled. Makes at least as much sense at
		the base class, and non-virtual will be faster (frequently called). */
	bool isAIControlled() const { return (!isHuman() || isAutomated()); }
	CvSelectionGroupAI& AI()
	{	//return *static_cast<CvSelectionGroupAI*>(const_cast<CvSelectionGroup*>(this));
		/*  The above won't work in an inline function b/c the compiler doesn't know
			that CvSelectionGroupAI is derived from CvSelectionGroup */
		return *reinterpret_cast<CvSelectionGroupAI*>(this);
	}
	CvSelectionGroupAI const& AI() const
	{	//return *static_cast<CvSelectionGroupAI const*>(this);
		return *reinterpret_cast<CvSelectionGroupAI const*>(this);
	} // </advc.003u>

	virtual void read(FDataStreamBase* pStream);
	virtual void write(FDataStreamBase* pStream);
	// advc.003u: Keep one pure virtual function so that this class is abstract
	virtual bool AI_update() = 0;

protected:
	// K-Mod! I'd rather this not be static, but I can't do that here.
	//public: static KmodPathFinder path_finder; protected:
	/*	advc.pf: We can make it a non-static member of CvSelectionGroup::Data,
		and that would indeed make the code much cleaner, but would also
		preclude the sharing of path data between groups in the future
		and would make it difficult to reuse path data when looping over
		units that may or may not belong to the same group (e.g. CvPlot::m_units).
		Just make it a static pointer so that we can at least delay initialization
		until the map has been initialized. */
	static GroupPathFinder* m_pPathFinder;
	/*	advc.opt: When we want to avoid resetting the path finder above,
		and also want to avoid allocating memory. */
	static GroupPathFinder* m_pAltPathFinder;

	// WARNING: adding to this class will cause the civ4 exe to crash

	/*	K-Mod: I've done some basic tests of the above warning.
		I've found that it does indeed crash during startup if I add int[30]
		but it does not crash if I only add int[2]. (I haven't tested inbetween.)
		The game also crashes if I add int[30] to CvSelectionGroupAI. */

	/*	... I see that BBAI ignored the warning. They added some stuff below.
		[advc: That was the BBAI StrandedCache, removed by K-Mod.]
		Removing the BBAI bools from below does not change the size 80.
		Neither does removing the BBAI virtual functions.
		but adding another int increases the size to 84. Which is a shame,
		because I really want to add one more int...
		Although a single int doesn't cause a startup crash,
		I'd rather not risk instability. */
	/*	advc.003k: See nested class 'Data' below for a workaround.
		(Not right here b/c it's safer to keep the members in their original order.) */

	int m_iID;
	int m_iMissionTimer;
	bool m_bForceUpdate;
	PlayerTypes m_eOwner;
	ActivityTypes m_eActivityType;
	//AutomateTypes m_eAutomateType;
	// <advc.003k> Pointer to additional data members
	class Data
	{
		AutomateTypes eAutomateType;
		CLinkList<IDInfo> knownEnemies; // advc.004l
		bool bInitiallyVisible; // advc.102
		friend CvSelectionGroup;
	};
	Data* m; // dial m for members
	// </advc.003k>

	CLinkList<IDInfo> m_units;
	CLinkList<MissionData> m_missionQueue;
	std::vector<CvUnit const*> m_aDifferentUnitCache; // advc: const
	bool m_bIsBusyCache;

	bool continueMission_bulk(int iSteps); // K-Mod
	void activateHeadMission();
	void deactivateHeadMission();
	bool isNeverShowMoves() const; // advc
	// <advc.075>
	void handleBoarded();
	bool canDisembark() const;
	void resetBoarded();
	void getLandCargoGroups(std::vector<CvSelectionGroup*>& kResult);
	// </advc.075>
	bool sentryAlert(/* advc.004l: */ bool bUpdateKnownEnemies = false);
	// <advc> Was public. Should only be used by Python
	CvUnit* getUnitAt(int iIndex) const;
	friend class CySelectionGroup; // </advc>

private: // advc.003u: (See comments in the private section of CvPlayer.h)
	//virtual void AI_initExternal();
	virtual void AI_resetExternal();
	virtual void AI_separateExternal();
	virtual bool AI_updateExternal();
	virtual int AI_attackOddsExternal(CvPlot* pPlot, bool bPotentialEnemy);
	virtual CvUnit* AI_getBestGroupAttackerExternal(CvPlot* pPlot, bool bPotentialEnemy, int& iUnitOdds,
			bool bForce = false, bool bNoBlitz = false);
	virtual CvUnit* AI_getBestGroupSacrificeExternal(CvPlot* pPlot, bool bPotentialEnemy,
			bool bForce = false, bool bNoBlitz = false);
	virtual int AI_compareStacksExternal(CvPlot* pPlot, bool bPotentialEnemy,
			bool bCheckCanAttack = false, bool bCheckCanMove = false);
	virtual int AI_sumStrengthExternal(
			CvPlot* pAttackedPlot = NULL, DomainTypes eDomainType = NO_DOMAIN, bool bCheckCanAttack = false, bool bCheckCanMove = false);
	virtual void AI_queueGroupAttackExternal(int iX, int iY);
	virtual void AI_cancelGroupAttackExternal();
	virtual bool AI_isGroupAttackExternal();
	virtual bool AI_isControlledExternal();
	virtual bool AI_isDeclareWarExternal(
			CvPlot* pPlot = NULL);
	virtual CvPlot* AI_getMissionAIPlotExternal();
	virtual bool AI_isForceSeparateExternal();
	virtual void AI_makeForceSeparateExternal();
	virtual MissionAITypes AI_getMissionAITypeExternal();
	virtual void AI_setMissionAIExternal(MissionAITypes eNewMissionAI, CvPlot* pNewPlot, CvUnit* pNewUnit);
	virtual CvUnit* AI_getMissionAIUnitExternal();
	virtual CvUnit* AI_ejectBestDefenderExternal(CvPlot* pTargetPlot);
	virtual void AI_separateNonAIExternal(UnitAITypes eUnitAI);
	virtual void AI_separateAIExternal(UnitAITypes eUnitAI);
	// advc.003u: Not called; could probably remove more (up until the bottommost one that the EXE calls).
	//virtual bool AI_isFull();
};
/*  advc.003k: If this fails, then you've probably added a data member (directly)
	to CvSelectionGroup. */
BOOST_STATIC_ASSERT(sizeof(CvSelectionGroup) == 80);

#endif
