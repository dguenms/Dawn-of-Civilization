//
// Python wrapper class for CySelectionGroup
// 
//
#include "CvGameCoreDLL.h"
#include "CySelectionGroup.h"
#include "CvSelectionGroup.h"
#include "CvPlot.h"
#include "CyPlot.h"
#include "CvArea.h"
#include "CyArea.h"
#include "CyUnit.h"
//#include "CvStructs.h"

CySelectionGroup::CySelectionGroup() : m_pSelectionGroup(NULL)
{

}

CySelectionGroup::CySelectionGroup(CvSelectionGroup* pSelectionGroup) : m_pSelectionGroup(pSelectionGroup)
{

}

void CySelectionGroup::pushMission(MissionTypes eMission, int iData1, int iData2, int iFlags, bool bAppend, bool bManual, MissionAITypes eMissionAI, CyPlot* pMissionAIPlot, CyUnit* pMissionAIUnit)
{
	if (m_pSelectionGroup)
		return m_pSelectionGroup->pushMission(eMission, iData1, iData2, iFlags, bAppend, bManual, eMissionAI, pMissionAIPlot->getPlot(), pMissionAIUnit->getUnit());
}

void CySelectionGroup::pushMoveToMission(int iX, int iY)
{
	if (m_pSelectionGroup)
		return m_pSelectionGroup->pushMission(MISSION_MOVE_TO, iX, iY);
}

void CySelectionGroup::popMission()
{
	if (m_pSelectionGroup)
		return m_pSelectionGroup->popMission();
}

CyPlot* CySelectionGroup::lastMissionPlot()
{
	return m_pSelectionGroup ? new CyPlot(m_pSelectionGroup->lastMissionPlot()) : NULL;
}

bool CySelectionGroup::canStartMission(int iMission, int iData1, int iData2, CyPlot* pPlot, bool bTestVisible)
{
	return m_pSelectionGroup ? m_pSelectionGroup->canStartMission(iMission, iData1, iData2, pPlot->getPlot(), bTestVisible) : false;
}

bool CySelectionGroup::canDoInterfaceMode(InterfaceModeTypes eInterfaceMode)
{
	return m_pSelectionGroup ? m_pSelectionGroup->canDoInterfaceMode(eInterfaceMode) : false;
}

bool CySelectionGroup::canDoInterfaceModeAt(InterfaceModeTypes eInterfaceMode, CyPlot* pPlot)
{
	return m_pSelectionGroup ? m_pSelectionGroup->canDoInterfaceModeAt(eInterfaceMode, pPlot->getPlot()) : false;
}

bool CySelectionGroup::canDoCommand(CommandTypes eCommand, int iData1, int iData2, bool bTestVisible)
{
	return m_pSelectionGroup ? m_pSelectionGroup->canDoCommand(eCommand, iData1, iData2, bTestVisible) : false;
}

bool CySelectionGroup::isHuman()
{
	return m_pSelectionGroup ? m_pSelectionGroup->isHuman() : false;
}

int CySelectionGroup::baseMoves()
{
	return m_pSelectionGroup ? m_pSelectionGroup->baseMoves() : -1;
}

bool CySelectionGroup::canAllMove()
{
	return m_pSelectionGroup ? m_pSelectionGroup->canAllMove() : false;
}

bool CySelectionGroup::isWaiting()
{
	return m_pSelectionGroup ? m_pSelectionGroup->isWaiting() : false;
}

bool CySelectionGroup::isFull()
{
	return m_pSelectionGroup ? m_pSelectionGroup->isFull() : false;
}

bool CySelectionGroup::hasCargo()
{
	return m_pSelectionGroup ? m_pSelectionGroup->hasCargo() : false;
}

bool CySelectionGroup::canAnyMove()
{
	return m_pSelectionGroup ? m_pSelectionGroup->canAnyMove() : false;
}

bool CySelectionGroup::hasMoved()
{
	return m_pSelectionGroup ? m_pSelectionGroup->hasMoved() : false;
}

bool CySelectionGroup::canEnterTerritory(int /*TeamTypes*/ eTeam, bool bIgnoreRightOfPassage)
{
	return m_pSelectionGroup ? m_pSelectionGroup->canEnterTerritory((TeamTypes) eTeam, bIgnoreRightOfPassage) : false;
}

bool CySelectionGroup::canEnterArea(int /*TeamTypes*/ eTeam, CyArea* pArea, bool bIgnoreRightOfPassage)
{
	return m_pSelectionGroup ? m_pSelectionGroup->canEnterArea((TeamTypes) eTeam, pArea->getArea(), bIgnoreRightOfPassage) : false;
}

bool CySelectionGroup::canMoveInto(CyPlot* pPlot, bool bAttack)
{
	return m_pSelectionGroup ? m_pSelectionGroup->canMoveInto(pPlot->getPlot(), bAttack) : false;
}

bool CySelectionGroup::canMoveOrAttackInto(CyPlot* pPlot, bool bDeclareWar)
{
	return m_pSelectionGroup ? m_pSelectionGroup->canMoveOrAttackInto(pPlot->getPlot(), bDeclareWar) : false;
}

bool CySelectionGroup::canMoveThrough(CyPlot* pPlot)
{
	return m_pSelectionGroup ? m_pSelectionGroup->canMoveThrough(pPlot->getPlot()) : false;
}

bool CySelectionGroup::canFight()
{
	return m_pSelectionGroup ? m_pSelectionGroup->canFight() : false;
}

bool CySelectionGroup::canDefend()
{
	return m_pSelectionGroup ? m_pSelectionGroup->canDefend() : false;
}

bool CySelectionGroup::alwaysInvisible()
{
	return m_pSelectionGroup ? m_pSelectionGroup->alwaysInvisible() : false;
}

bool CySelectionGroup::isInvisible(int /*TeamTypes*/ eTeam)
{
	return m_pSelectionGroup ? m_pSelectionGroup->isInvisible((TeamTypes) eTeam) : false;
}

int CySelectionGroup::countNumUnitAIType(UnitAITypes eUnitAI)
{
	return m_pSelectionGroup ? m_pSelectionGroup->countNumUnitAIType(eUnitAI) : -1;
}

bool CySelectionGroup::hasWorker()
{
	return m_pSelectionGroup ? m_pSelectionGroup->hasWorker() : false;
}

bool CySelectionGroup::at(int iX, int iY)
{
	return m_pSelectionGroup ? m_pSelectionGroup->at(iX, iY) : false;
}

bool CySelectionGroup::atPlot(CyPlot* pPlot)
{
	return m_pSelectionGroup ? m_pSelectionGroup->atPlot(pPlot->getPlot()) : false;
}

CyPlot* CySelectionGroup::plot()
{
	return m_pSelectionGroup ? new CyPlot( m_pSelectionGroup->plot() ) : NULL;
}

CyArea* CySelectionGroup::area()
{
	return m_pSelectionGroup ? new CyArea( m_pSelectionGroup->area() ) : NULL;
}

int /*RouteTypes*/ CySelectionGroup::getBestBuildRoute(CyPlot* pPlot, BuildTypes* peBestBuild)
{
	return m_pSelectionGroup ? m_pSelectionGroup->getBestBuildRoute(pPlot->getPlot(), peBestBuild) : -1;
}

bool CySelectionGroup::isAmphibPlot(CyPlot* pPlot)
{
	return m_pSelectionGroup ? m_pSelectionGroup->isAmphibPlot(pPlot->getPlot()) : false;
}
bool CySelectionGroup::readyToSelect(bool bAny)
{
	return m_pSelectionGroup ? m_pSelectionGroup->readyToSelect(bAny) : false;
}

bool CySelectionGroup::readyToMove(bool bAny)
{
	return m_pSelectionGroup ? m_pSelectionGroup->readyToMove(bAny) : false;
}

bool CySelectionGroup::readyToAuto()
{
	return m_pSelectionGroup ? m_pSelectionGroup->readyToAuto() : false;
}

int CySelectionGroup::getID()
{
	return m_pSelectionGroup ? m_pSelectionGroup->getID() : -1;
}

int /*PlayerTypes*/ CySelectionGroup::getOwner()
{
	return m_pSelectionGroup ? m_pSelectionGroup->getOwnerINLINE() : -1;
}

int /*TeamTypes*/ CySelectionGroup::getTeam()
{
	return m_pSelectionGroup ? (TeamTypes) m_pSelectionGroup->getTeam() : -1;
}

int /*ActivityTypes*/ CySelectionGroup::getActivityType()
{
	return m_pSelectionGroup ? (ActivityTypes) m_pSelectionGroup->getActivityType() : -1;
}

void CySelectionGroup::setActivityType(int /*ActivityTypes*/ eNewValue)
{
	if (m_pSelectionGroup)
		m_pSelectionGroup->setActivityType((ActivityTypes) eNewValue);
}

int /*AutomateTypes*/ CySelectionGroup::getAutomateType() 
{
	return m_pSelectionGroup ? (AutomateTypes) m_pSelectionGroup->getAutomateType() : -1;
}

bool CySelectionGroup::isAutomated()
{
	return m_pSelectionGroup ? m_pSelectionGroup->isAutomated() : false;
}

void CySelectionGroup::setAutomateType(int /*AutomateTypes*/ eNewValue)
{
	if (m_pSelectionGroup)
		m_pSelectionGroup->setAutomateType((AutomateTypes) eNewValue);
}

CyPlot* CySelectionGroup::getPathFirstPlot()
{
	return m_pSelectionGroup ? new CyPlot(m_pSelectionGroup->getPathFirstPlot()) : NULL;
}

CyPlot* CySelectionGroup::getPathEndTurnPlot()
{
	return m_pSelectionGroup ? new CyPlot(m_pSelectionGroup->getPathEndTurnPlot()) : NULL;
}

bool CySelectionGroup::generatePath(CyPlot* pFromPlot, CyPlot* pToPlot, int iFlags, bool bReuse, int* piPathTurns)
{
	return m_pSelectionGroup ? m_pSelectionGroup->generatePath(pFromPlot->getPlot(), pToPlot->getPlot(), iFlags, bReuse, piPathTurns) : false;
}

void CySelectionGroup::resetPath()
{
	if (m_pSelectionGroup)
		m_pSelectionGroup->resetPath();
}

int CySelectionGroup::getNumUnits()
{
	return m_pSelectionGroup ? m_pSelectionGroup->getNumUnits() : -1;
}

void CySelectionGroup::clearMissionQueue()
{
	if (m_pSelectionGroup)
		m_pSelectionGroup->clearMissionQueue();
}

int CySelectionGroup::getLengthMissionQueue()
{
	return m_pSelectionGroup ? m_pSelectionGroup->getLengthMissionQueue() : -1;
}

MissionData* CySelectionGroup::getMissionFromQueue(int iIndex)
{
	return m_pSelectionGroup ? m_pSelectionGroup->getMissionFromQueue(iIndex) : NULL;
}

CyUnit* CySelectionGroup::getHeadUnit()
{
	return m_pSelectionGroup ? new CyUnit(m_pSelectionGroup->getHeadUnit()) : NULL;
}

CyUnit* CySelectionGroup::getUnitAt(int index)
{
	return m_pSelectionGroup ? new CyUnit(m_pSelectionGroup->getUnitAt(index)) : NULL;
}

int CySelectionGroup::getMissionType( int iNode )
{
	return m_pSelectionGroup ? m_pSelectionGroup->getMissionType(iNode) : -1;
}

int CySelectionGroup::getMissionData1( int iNode )
{
	return m_pSelectionGroup ? m_pSelectionGroup->getMissionData1( iNode ) : -1;
}

int CySelectionGroup::getMissionData2( int iNode )
{
	return m_pSelectionGroup ? m_pSelectionGroup->getMissionData2( iNode ) : -1;
}