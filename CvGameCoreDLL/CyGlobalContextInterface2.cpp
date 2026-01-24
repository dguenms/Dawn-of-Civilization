//
// published python interface for CyGlobalContext
// Author - Mustafa Thamer
//

#include "CvGameCoreDLL.h"
#include "CyMap.h"
#include "CyPlayer.h"
#include "CyGame.h"
#include "CyTeam.h"


void CyGlobalContextPythonInterface2(python::class_<CyGlobalContext>& x)
{
	printToConsole("Python Extension Module - CyGlobalContextPythonInterface2\n");

	x
		// global defines.xml
		.def("getDefineINT", &CyGlobalContext::getDefineINT, "int ( string szName )" )
		.def("getDefineFLOAT", &CyGlobalContext::getDefineFLOAT, "float ( string szName )" )
		.def("getDefineSTRING", &CyGlobalContext::getDefineSTRING, "string getDefineSTRING( string szName )" )
		.def("setDefineINT", &CyGlobalContext::setDefineINT, "void ( string szName, int iValue )" )
		.def("setDefineFLOAT", &CyGlobalContext::setDefineFLOAT, "void setDefineFLOAT( string szName, float fValue )" )
		.def("setDefineSTRING", &CyGlobalContext::setDefineSTRING, "void ( string szName, string szValue )" )
		// advc.003t: Rearranged these and removed about a dozen unused getters
		.def("getMOVE_DENOMINATOR", &CyGlobalContext::getMOVE_DENOMINATOR, "int ()")
		.def("getFOOD_CONSUMPTION_PER_POPULATION", &CyGlobalContext::getFOOD_CONSUMPTION_PER_POPULATION, "int ()")
		.def("getMAX_HIT_POINTS", &CyGlobalContext::getMAX_HIT_POINTS, "int ()")
		.def("getMAX_PLOT_LIST_ROWS", &CyGlobalContext::getMAX_PLOT_LIST_ROWS, "int ()")
		.def("getUNIT_MULTISELECT_MAX", &CyGlobalContext::getUNIT_MULTISELECT_MAX, "int ()")
		.def("getEVENT_MESSAGE_TIME", &CyGlobalContext::getEVENT_MESSAGE_TIME, "int ()")
		.def("getPERCENT_ANGER_DIVISOR", &CyGlobalContext::getPERCENT_ANGER_DIVISOR, "int ()")
		.def("getMIN_WATER_SIZE_FOR_OCEAN", &CyGlobalContext::getMIN_WATER_SIZE_FOR_OCEAN, "int ()")
		.def("getMAX_CITY_DEFENSE_DAMAGE", &CyGlobalContext::getMAX_CITY_DEFENSE_DAMAGE, "int ()")

		.def("getNUM_UNIT_PREREQ_OR_BONUSES", &CyGlobalContext::getNUM_UNIT_PREREQ_OR_BONUSES, "int ()")
		.def("getNUM_BUILDING_PREREQ_OR_BONUSES", &CyGlobalContext::getNUM_BUILDING_PREREQ_OR_BONUSES, "int ()")
		.def("getNUM_AND_TECH_PREREQS", &CyGlobalContext::getNUM_AND_TECH_PREREQS, "int ()")
		.def("getNUM_OR_TECH_PREREQS", &CyGlobalContext::getNUM_OR_TECH_PREREQS, "int ()")
		.def("getNUM_UNIT_AND_TECH_PREREQS", &CyGlobalContext::getNUM_UNIT_AND_TECH_PREREQS, "int ()")
		.def("getNUM_ROUTE_PREREQ_OR_BONUSES", &CyGlobalContext::getNUM_ROUTE_PREREQ_OR_BONUSES, "int ()")
		.def("getNUM_BUILDING_AND_TECH_PREREQS", &CyGlobalContext::getNUM_BUILDING_AND_TECH_PREREQS, "int ()")
		.def("getNUM_CORPORATION_PREREQ_BONUSES", &CyGlobalContext::getNUM_CORPORATION_PREREQ_BONUSES, "int ()")

		.def("getCAMERA_MIN_YAW", &CyGlobalContext::getCAMERA_MIN_YAW, "float ()")
		.def("getCAMERA_MAX_YAW", &CyGlobalContext::getCAMERA_MAX_YAW, "float ()")
		.def("getCAMERA_FAR_CLIP_Z_HEIGHT", &CyGlobalContext::getCAMERA_FAR_CLIP_Z_HEIGHT, "float ()")
		.def("getCAMERA_MAX_TRAVEL_DISTANCE", &CyGlobalContext::getCAMERA_MAX_TRAVEL_DISTANCE, "float ()")
		.def("getCAMERA_START_DISTANCE", &CyGlobalContext::getCAMERA_START_DISTANCE, "float ()")
		.def("getAIR_BOMB_HEIGHT", &CyGlobalContext::getAIR_BOMB_HEIGHT, "float ()")
		.def("getPLOT_SIZE", &CyGlobalContext::getPLOT_SIZE, "float ()")
		.def("getCAMERA_SPECIAL_PITCH", &CyGlobalContext::getCAMERA_SPECIAL_PITCH, "float ()")
		.def("getCAMERA_MAX_TURN_OFFSET", &CyGlobalContext::getCAMERA_MAX_TURN_OFFSET, "float ()")
		.def("getCAMERA_MIN_DISTANCE", &CyGlobalContext::getCAMERA_MIN_DISTANCE, "float ()")
		.def("getCAMERA_UPPER_PITCH", &CyGlobalContext::getCAMERA_UPPER_PITCH, "float ()")
		.def("getCAMERA_LOWER_PITCH", &CyGlobalContext::getCAMERA_LOWER_PITCH, "float ()")
		.def("getFIELD_OF_VIEW", &CyGlobalContext::getFIELD_OF_VIEW, "float ()")
		.def("getSHADOW_SCALE", &CyGlobalContext::getSHADOW_SCALE, "float ()")
		.def("getUNIT_MULTISELECT_DISTANCE", &CyGlobalContext::getUNIT_MULTISELECT_DISTANCE, "float ()")
		// advc.004m:
		.def("updateCameraStartDistance", &CyGlobalContext::updateCameraStartDistance, "void (bReset)")

		.def("getMAX_CIV_PLAYERS", &CyGlobalContext::getMAX_CIV_PLAYERS, "int ()")
		.def("getMAX_PLAYERS", &CyGlobalContext::getMAX_PLAYERS, "int ()")
		.def("getMAX_CIV_TEAMS", &CyGlobalContext::getMAX_CIV_TEAMS, "int ()")
		.def("getMAX_TEAMS", &CyGlobalContext::getMAX_TEAMS, "int ()")
		.def("getBARBARIAN_PLAYER", &CyGlobalContext::getBARBARIAN_PLAYER, "int ()")
		.def("getBARBARIAN_TEAM", &CyGlobalContext::getBARBARIAN_TEAM, "int ()")
		.def("getINVALID_PLOT_COORD", &CyGlobalContext::getINVALID_PLOT_COORD, "int ()")
		.def("getNUM_CITY_PLOTS", &CyGlobalContext::getNUM_CITY_PLOTS, "int ()")
		.def("getCITY_HOME_PLOT", &CyGlobalContext::getCITY_HOME_PLOT, "int ()")
		;
}
