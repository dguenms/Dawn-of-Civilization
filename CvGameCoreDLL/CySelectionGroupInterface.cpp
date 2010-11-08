#include "CvGameCoreDLL.h"
#include "CySelectionGroup.h"
#include "CyPlot.h"
#include "CyArea.h"
#include "CyUnit.h"
//#include "CvStructs.h"
//# include <boost/python/manage_new_object.hpp>
//# include <boost/python/return_value_policy.hpp>

//
// published python interface for CySelectionGroup
//

void CySelectionGroupInterface()
{
	OutputDebugString("Python Extension Module - CySelectionGroupInterface\n");

	python::class_<CySelectionGroup>("CySelectionGroup")
		.def("isNone", &CySelectionGroup::isNone, "bool () - is this CySelectionGroup instance valid?")
		.def("pushMission", &CySelectionGroup::pushMission, "void (eMission, iData1, iData2, iFlags, bAppend, bManual, eMissionAI, pMissionAIPlot, pMissionAIUnit)")
		.def("pushMoveToMission", &CySelectionGroup::pushMoveToMission, "void (plotX, plotY)")
		.def("popMission", &CySelectionGroup::popMission, "void () - removes mission from queue")
		.def("lastMissionPlot", &CySelectionGroup::lastMissionPlot, python::return_value_policy<python::manage_new_object>(), "CvPlot* ()")
		.def("canStartMission", &CySelectionGroup::canStartMission, "bool (int iMission, int iData1, int iData2, CyPlot* pPlot, bool bTestVisible)")

		.def("canDoInterfaceMode", &CySelectionGroup::canDoInterfaceMode, "bool (int (InterfaceModeTypes) eInterfaceMode)")
		.def("canDoInterfaceModeAt", &CySelectionGroup::canDoInterfaceModeAt, "bool (int (InterfaceModeTypes) eInterfaceMode, CyPlot* pPlot)")

		.def("canDoCommand", &CySelectionGroup::canDoCommand, "bool (eCommand, iData1, iData2, bTestVisible = False) - can the group perform eCommand?")

		.def("isHuman", &CySelectionGroup::isHuman, "bool ()")
		.def("baseMoves", &CySelectionGroup::baseMoves, "int ()")
		.def("isWaiting", &CySelectionGroup::isWaiting, "bool ()")
		.def("isFull", &CySelectionGroup::isFull, "bool ()")
		.def("hasCargo", &CySelectionGroup::hasCargo, "bool ()")
		.def("canAllMove", &CySelectionGroup::canAllMove, "bool ()")
		.def("canAnyMove", &CySelectionGroup::canAnyMove, "bool ()")
		.def("hasMoved", &CySelectionGroup::hasMoved, "bool ()")
		.def("canEnterTerritory", &CySelectionGroup::canEnterTerritory, "bool (int /*TeamTypes*/ eTeam, bool bIgnoreRightOfPassage)")
		.def("canEnterArea", &CySelectionGroup::canEnterArea, "bool (int /*TeamTypes*/ eTeam, CyArea* pArea, bool bIgnoreRightOfPassage)")
		.def("canMoveInto", &CySelectionGroup::canMoveInto, "bool (CyPlot* pPlot, bool bAttack) - can the group move into pPlot?")
		.def("canMoveOrAttackInto", &CySelectionGroup::canMoveOrAttackInto, "bool (CyPlot* pPlot, bool bDeclareWar) - can the group move or attack into pPlot?")
		.def("canMoveThrough", &CySelectionGroup::canMoveThrough, "bool (CyPlot* pPlot)")
		.def("canFight", &CySelectionGroup::canFight, "bool ()")
		.def("canDefend", &CySelectionGroup::canDefend, "bool ()")
		.def("alwaysInvisible", &CySelectionGroup::alwaysInvisible, "bool ()")
		.def("isInvisible", &CySelectionGroup::isInvisible, "bool (int eTeam)")
		.def("countNumUnitAIType", &CySelectionGroup::countNumUnitAIType, "int (int (UnitAITypes) eUnitAI")
		.def("hasWorker", &CySelectionGroup::hasWorker, "bool ()")

		.def("at", &CySelectionGroup::at, "bool (iX, iY) - is the group at plot iX, iY?")
		.def("atPlot", &CySelectionGroup::atPlot, "bool (CyPlot* pPlot) - is the group at pPlot?")
		.def("plot", &CySelectionGroup::plot, python::return_value_policy<python::manage_new_object>(), "CyPlot () - get plot that the group is on")
		.def("area", &CySelectionGroup::area, python::return_value_policy<python::manage_new_object>(), "CyArea ()*")
		.def("getBestBuildRoute", &CySelectionGroup::getBestBuildRoute, "int (RouteTypes) (CyPlot* pPlot, BuildTypes* peBestBuild)")

		.def("isAmphibPlot", &CySelectionGroup::isAmphibPlot, "bool (CyPlot* pPlot)")

		.def("readyToSelect", &CySelectionGroup::readyToSelect, "bool (bool bAny) - is the group able to be selected?")
		.def("readyToMove", &CySelectionGroup::readyToMove, "bool (bool bAny) - is the group awake and ready to move?")
		.def("readyToAuto", &CySelectionGroup::readyToAuto, "bool ()")

		.def("getID", &CySelectionGroup::getID, "int () - the ID for the SelectionGroup")
		.def("getOwner", &CySelectionGroup::getOwner, "int (PlayerTypes) () - ID for owner of the group")
		.def("getTeam", &CySelectionGroup::getTeam, "int (TeamTypes) () - ID for team owner of the group")
		.def("getActivityType", &CySelectionGroup::getActivityType, "int /*ActivityTypes*/ () - ActivityTypes the group is engaging in")
		.def("setActivityType", &CySelectionGroup::setActivityType, "void (int /*ActivityTypes*/ eNewValue) - set the group to this ActivityTypes")
		.def("getAutomateType", &CySelectionGroup::getAutomateType, "int /*AutomateTypes*/ () - AutomateTypes the group is engaging in")
		.def("isAutomated", &CySelectionGroup::isAutomated, "bool () - Is the group automated?")
		.def("setAutomateType", &CySelectionGroup::setAutomateType, "void (int /*AutomateTypes*/ eNewValue) - get the group to perform this AutomateTypes")
		.def("getPathFirstPlot", &CySelectionGroup::getPathFirstPlot, python::return_value_policy<python::manage_new_object>(), "CyPlot* ()")
		.def("getPathEndTurnPlot", &CySelectionGroup::getPathEndTurnPlot, python::return_value_policy<python::manage_new_object>(), "CyPlot* ()")
		.def("generatePath", &CySelectionGroup::generatePath, "bool (CyPlot* pFromPlot, CyPlot* pToPlot, int iFlags, bool bReuse, int* piPathTurns)")
		.def("resetPath", &CySelectionGroup::resetPath, "void ()")

		.def("getNumUnits", &CySelectionGroup::getNumUnits, "int ()")			// JS Help!
		.def("clearMissionQueue", &CySelectionGroup::clearMissionQueue, "void ()")
		.def("getLengthMissionQueue", &CySelectionGroup::getLengthMissionQueue, "int ()")
		.def("getMissionFromQueue", &CySelectionGroup::getMissionFromQueue, python::return_value_policy<python::manage_new_object>(), "MissionData* (int iIndex)")
		.def("getHeadUnit", &CySelectionGroup::getHeadUnit, python::return_value_policy<python::manage_new_object>(), "CyUnit* ()")
		.def("getUnitAt", &CySelectionGroup::getUnitAt, python::return_value_policy<python::manage_new_object>(), "CyUnit* (int index)")
		.def("getMissionType", &CySelectionGroup::getMissionType, "int (int iNode)")
		.def("getMissionData1", &CySelectionGroup::getMissionData1, "int (int iNode)")
		.def("getMissionData2", &CySelectionGroup::getMissionData2, "int (int iNode)")
		;
}
