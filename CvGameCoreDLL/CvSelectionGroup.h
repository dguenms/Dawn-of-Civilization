#pragma once

// selectionGroup.h

#ifndef CIV4_GROUP_H
#define CIV4_GROUP_H

//#include "CvStructs.h"
#include "LinkedList.h"

class CvPlot;
class CvArea;
class FAStarNode;

class CvSelectionGroup
{

public:

	CvSelectionGroup();
	virtual ~CvSelectionGroup();

	DllExport void init(int iID, PlayerTypes eOwner);
	DllExport void uninit();			
	DllExport void reset(int iID = 0, PlayerTypes eOwner = NO_PLAYER, bool bConstructorCall = false);

	void kill();

	void doTurn();

	bool showMoves() const;

	void updateTimers();
	bool doDelayedDeath();

	void playActionSound();

	DllExport void pushMission(MissionTypes eMission, int iData1 = -1, int iData2 = -1, int iFlags = 0, bool bAppend = false, bool bManual = false, MissionAITypes eMissionAI = NO_MISSIONAI, CvPlot* pMissionAIPlot = NULL, CvUnit* pMissionAIUnit = NULL);		// Exposed to Python
	void popMission();																																										// Exposed to Python
	DllExport void autoMission();
	void updateMission();
	DllExport CvPlot* lastMissionPlot();																																					// Exposed to Python

	DllExport bool canStartMission(int iMission, int iData1, int iData2, CvPlot* pPlot = NULL, bool bTestVisible = false, bool bUseCache = false);		// Exposed to Python
	void startMission();
	void continueMission(int iSteps = 0);

	DllExport bool canDoInterfaceMode(InterfaceModeTypes eInterfaceMode);													// Exposed to Python
	DllExport bool canDoInterfaceModeAt(InterfaceModeTypes eInterfaceMode, CvPlot* pPlot);				// Exposed to Python

	DllExport bool canDoCommand(CommandTypes eCommand, int iData1, int iData2, bool bTestVisible = false, bool bUseCache = false);		// Exposed to Python
	bool canEverDoCommand(CommandTypes eCommand, int iData1, int iData2, bool bTestVisible, bool bUseCache);
	void setupActionCache();

	bool isHuman();																																											// Exposed to Python
	DllExport bool isBusy();
	bool isCargoBusy();
	int baseMoves();																																										// Exposed to Python 
	bool isWaiting() const;																																							// Exposed to Python
	bool isFull();																																											// Exposed to Python
	bool hasCargo();																																										// Exposed to Python
	int getCargo() const;
	DllExport bool canAllMove();																																				// Exposed to Python
	bool canAnyMove();																																									// Exposed to Python
	bool hasMoved();																																										// Exposed to Python
	bool canEnterTerritory(TeamTypes eTeam, bool bIgnoreRightOfPassage = false) const;									// Exposed to Python
	bool canEnterArea(TeamTypes eTeam, const CvArea* pArea, bool bIgnoreRightOfPassage = false) const;									// Exposed to Python
	DllExport bool canMoveInto(CvPlot* pPlot, bool bAttack = false);																		// Exposed to Python
	DllExport bool canMoveOrAttackInto(CvPlot* pPlot, bool bDeclareWar = false);												// Exposed to Python
	bool canMoveThrough(CvPlot* pPlot);																																	// Exposed to Python
	bool canFight();																																										// Exposed to Python 
	bool canDefend();																																										// Exposed to Python
	bool canBombard(const CvPlot* pPlot);
	bool visibilityRange();

	void unloadAll();
	bool alwaysInvisible() const;																																							// Exposed to Python
	bool isInvisible(TeamTypes eTeam) const;																								// Exposed to Python
	int countNumUnitAIType(UnitAITypes eUnitAI);																												// Exposed to Python
	bool hasWorker();																																										// Exposed to Python
	bool IsSelected();
	DllExport void NotifyEntity(MissionTypes eMission);
	void airCircle(bool bStart);
	void setBlockading(bool bStart);

	int getX() const;
	int getY() const;
	bool at(int iX, int iY) const;																																								// Exposed to Python
	bool atPlot(const CvPlot* pPlot) const;																																				// Exposed to Python
	DllExport CvPlot* plot() const;																																								// Exposed to Python
	int getArea() const;
	CvArea* area() const;																																													// Exposed to Python
	DomainTypes getDomainType() const;

	RouteTypes getBestBuildRoute(CvPlot* pPlot, BuildTypes* peBestBuild = NULL) const;	// Exposed to Python

	bool groupDeclareWar(CvPlot* pPlot, bool bForce = false);
	bool groupAttack(int iX, int iY, int iFlags, bool& bFailedAlreadyFighting);
	void groupMove(CvPlot* pPlot, bool bCombat, CvUnit* pCombatUnit = NULL, bool bEndMove = false);
	bool groupPathTo(int iX, int iY, int iFlags);
	bool groupRoadTo(int iX, int iY, int iFlags);
	bool groupBuild(BuildTypes eBuild);
	void setTransportUnit(CvUnit* pTransportUnit);

	bool isAmphibPlot(const CvPlot* pPlot) const;																																		// Exposed to Python
	bool groupAmphibMove(CvPlot* pPlot, int iFlags);

	DllExport bool readyToSelect(bool bAny = false);																										// Exposed to Python
	bool readyToMove(bool bAny = false);																																// Exposed to Python
	bool readyToAuto();																																									// Exposed to Python 

	int getID() const;																																												// Exposed to Python
	void setID(int iID);																			

	int getMissionTimer() const;
	void setMissionTimer(int iNewValue);
	void changeMissionTimer(int iChange);
	void updateMissionTimer(int iSteps = 0);

	bool isForceUpdate();
	void setForceUpdate(bool bNewValue);

	DllExport PlayerTypes getOwner() const;																															// Exposed to Python
#ifdef _USRDLL
	inline PlayerTypes getOwnerINLINE() const
	{
		return m_eOwner;
	}
#endif
	TeamTypes getTeam() const;																																					// Exposed to Python

	ActivityTypes getActivityType() const;																															// Exposed to Python
	void setActivityType(ActivityTypes eNewValue);																											// Exposed to Python

	AutomateTypes getAutomateType() const;																																		// Exposed to Python
	bool isAutomated();																																									// Exposed to Python
	void setAutomateType(AutomateTypes eNewValue);																											// Exposed to Python

	FAStarNode* getPathLastNode() const;
	CvPlot* getPathFirstPlot() const;																																		// Exposed to Python
	CvPlot* getPathEndTurnPlot() const;																																	// Exposed to Python
	bool generatePath( const CvPlot* pFromPlot, const CvPlot* pToPlot, int iFlags = 0, bool bReuse = false, int* piPathTurns = NULL) const;	// Exposed to Python
	void resetPath();																																										// Exposed to Python

	DllExport void clearUnits();
	DllExport bool addUnit(CvUnit* pUnit, bool bMinimalChange);
	void removeUnit(CvUnit* pUnit);
	void mergeIntoGroup(CvSelectionGroup* pSelectionGroup);
	CvSelectionGroup* splitGroup(int iSplitSize, CvUnit* pNewHeadUnit = NULL, CvSelectionGroup** ppOtherGroup = NULL);

	DllExport CLLNode<IDInfo>* deleteUnitNode(CLLNode<IDInfo>* pNode);
	DllExport CLLNode<IDInfo>* nextUnitNode(CLLNode<IDInfo>* pNode) const;
	DllExport int getNumUnits() const;																												// Exposed to Python
	DllExport int getUnitIndex(CvUnit* pUnit, int maxIndex = -1) const;
	DllExport CLLNode<IDInfo>* headUnitNode() const;
	DllExport CvUnit* getHeadUnit() const;
	DllExport CvUnit* getUnitAt(int index) const;
	UnitAITypes getHeadUnitAI() const;
	PlayerTypes getHeadOwner() const;
	TeamTypes getHeadTeam() const;

	void clearMissionQueue();																																	// Exposed to Python
	DllExport int getLengthMissionQueue() const;																											// Exposed to Python
	MissionData* getMissionFromQueue(int iIndex) const;																							// Exposed to Python
	void insertAtEndMissionQueue(MissionData mission, bool bStart = true);
	CLLNode<MissionData>* deleteMissionQueueNode(CLLNode<MissionData>* pNode);
	DllExport CLLNode<MissionData>* nextMissionQueueNode(CLLNode<MissionData>* pNode) const;
	CLLNode<MissionData>* prevMissionQueueNode(CLLNode<MissionData>* pNode) const;
	DllExport CLLNode<MissionData>* headMissionQueueNode() const;
	CLLNode<MissionData>* tailMissionQueueNode() const;
	int getMissionType(int iNode) const;																														// Exposed to Python
	int getMissionData1(int iNode) const;																														// Exposed to Python
	int getMissionData2(int iNode) const;																														// Exposed to Python

// BUG - All Units Actions - start
	bool allMatch(UnitTypes eUnit) const;
// BUG - All Units Actions - end

	// for serialization
	virtual void read(FDataStreamBase* pStream);
	virtual void write(FDataStreamBase* pStream);

	virtual void AI_init() = 0;
	virtual void AI_reset() = 0;
	virtual void AI_separate() = 0;
	virtual bool AI_update() = 0;
	virtual int AI_attackOdds(const CvPlot* pPlot, bool bPotentialEnemy) const = 0;
	virtual CvUnit* AI_getBestGroupAttacker(const CvPlot* pPlot, bool bPotentialEnemy, int& iUnitOdds, bool bForce = false, bool bNoBlitz = false) const = 0;
	virtual CvUnit* AI_getBestGroupSacrifice(const CvPlot* pPlot, bool bPotentialEnemy, bool bForce = false, bool bNoBlitz = false) const = 0;
	virtual int AI_compareStacks(const CvPlot* pPlot, bool bPotentialEnemy, bool bCheckCanAttack = false, bool bCheckCanMove = false) const = 0;
	virtual int AI_sumStrength(const CvPlot* pAttackedPlot = NULL, DomainTypes eDomainType = NO_DOMAIN, bool bCheckCanAttack = false, bool bCheckCanMove = false) const = 0;
	virtual void AI_queueGroupAttack(int iX, int iY) = 0;
	virtual void AI_cancelGroupAttack() = 0;
	virtual bool AI_isGroupAttack() = 0;

	virtual bool AI_isControlled() = 0;
	virtual bool AI_isDeclareWar(const CvPlot* pPlot = NULL) = 0;
	virtual CvPlot* AI_getMissionAIPlot() = 0;
	virtual bool AI_isForceSeparate() = 0;
	virtual void AI_makeForceSeparate() = 0;
	virtual MissionAITypes AI_getMissionAIType() = 0;
	virtual void AI_setMissionAI(MissionAITypes eNewMissionAI, CvPlot* pNewPlot, CvUnit* pNewUnit) = 0;
	virtual CvUnit* AI_getMissionAIUnit() = 0;
	virtual CvUnit* AI_ejectBestDefender(CvPlot* pTargetPlot) = 0;
	virtual void AI_seperateNonAI(UnitAITypes eUnitAI) = 0;
	virtual void AI_seperateAI(UnitAITypes eUnitAI) = 0;
	virtual bool AI_isFull() = 0;

protected:
	// WARNING: adding to this class will cause the civ4 exe to crash

	int m_iID;
	int m_iMissionTimer;

	bool m_bForceUpdate;

	PlayerTypes m_eOwner;
	ActivityTypes m_eActivityType;
	AutomateTypes m_eAutomateType;

	CLinkList<IDInfo> m_units;

	CLinkList<MissionData> m_missionQueue;
	std::vector<CvUnit *> m_aDifferentUnitCache;
	bool m_bIsBusyCache;

// BUG - Safe Move - start
	bool m_bLastPathPlotChecked;
	bool m_bLastPlotVisible;
	bool m_bLastPlotRevealed;

	void checkLastPathPlot(CvPlot* pPlot);
	void clearLastPathPlot();
	bool isLastPathPlotChecked() const;
	bool isLastPathPlotVisible() const;
	bool isLastPathPlotRevealed() const;
// BUG - Safe Move - end

	void activateHeadMission();
	void deactivateHeadMission();
	
	bool sentryAlert() const;

// BUG - Sentry Actions - start
#ifdef _MOD_SENTRY
	bool sentryAlertSameDomainType() const;
#endif
// BUG - Sentry Actions - end
};

#endif
