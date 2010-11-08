#include "CvGameCoreDLL.h"
#include "CyReplayInfo.h"
#include "CyHallOfFameInfo.h"
#include "CyMap.h"

//
// published python interface for CyReplayInfo
//

void CyHallOfFameInterface()
{
	OutputDebugString("Python Extension Module - CyReplayInterface\n");

	python::class_<CyReplayInfo>("CyReplayInfo")
		.def("isNone", &CyReplayInfo::isNone, "bool () - Returns whether or not this is a valid object")

		.def("createInfo", &CyReplayInfo::createInfo, "void ()")

		.def("getActivePlayer", &CyReplayInfo::getActivePlayer, "int ()")
		.def("getLeader", &CyReplayInfo::getLeader, "int (int iPlayer)")
		.def("getColor", &CyReplayInfo::getColor, "int (int iPlayer)")
		.def("getDifficulty", &CyReplayInfo::getDifficulty, "int ()")
		.def("getLeaderName", &CyReplayInfo::getLeaderName, "wstring ()")
		.def("getCivDescription", &CyReplayInfo::getCivDescription, "wstring ()")
		.def("getShortCivDescription", &CyReplayInfo::getShortCivDescription, "wstring ()")
		.def("getCivAdjective", &CyReplayInfo::getCivAdjective, "wstring ()")
		.def("getMapScriptName", &CyReplayInfo::getMapScriptName, "wstring ()")
		.def("getWorldSize", &CyReplayInfo::getWorldSize, "int ()")
		.def("getClimate", &CyReplayInfo::getClimate, "int ()")
		.def("getSeaLevel", &CyReplayInfo::getSeaLevel, "int ()")
		.def("getEra", &CyReplayInfo::getEra, "int ()")
		.def("getGameSpeed", &CyReplayInfo::getGameSpeed, "int ()")
		.def("isGameOption", &CyReplayInfo::isGameOption, "bool (int iOption)")
		.def("isVictoryCondition", &CyReplayInfo::isVictoryCondition, "bool (int iVictory)")
		.def("getVictoryType", &CyReplayInfo::getVictoryType, "int ()")
		.def("isMultiplayer", &CyReplayInfo::isMultiplayer, "bool ()")

		.def("getNumPlayers", &CyReplayInfo::getNumPlayers, "int ()")
		.def("getPlayerScore", &CyReplayInfo::getPlayerScore, "int (int iPlayer, int iTurn)")
		.def("getPlayerEconomy", &CyReplayInfo::getPlayerEconomy, "int (int iPlayer, int iTurn)")
		.def("getPlayerIndustry", &CyReplayInfo::getPlayerIndustry, "int (int iPlayer, int iTurn)")
		.def("getPlayerAgriculture", &CyReplayInfo::getPlayerAgriculture, "int (int iPlayer, int iTurn)")
		
		.def("getNormalizedScore", &CyReplayInfo::getNormalizedScore, "int ()")
		
		.def("getReplayMessageTurn", &CyReplayInfo::getReplayMessageTurn, "int (int i)")
		.def("getReplayMessageType", &CyReplayInfo::getReplayMessageType, "int (int i)")
		.def("getReplayMessagePlotX", &CyReplayInfo::getReplayMessagePlotX, "int (int i)")
		.def("getReplayMessagePlotY", &CyReplayInfo::getReplayMessagePlotY, "int (int i)")
		.def("getReplayMessagePlayer", &CyReplayInfo::getReplayMessagePlayer, "int (int i)")
		.def("getReplayMessageText", &CyReplayInfo::getReplayMessageText, "wstring (int i)")
		.def("getNumReplayMessages", &CyReplayInfo::getNumReplayMessages, "int ()")
		.def("getReplayMessageColor", &CyReplayInfo::getReplayMessageColor, "int (int i)")

		.def("getInitialTurn", &CyReplayInfo::getInitialTurn, "int ()")
		.def("getStartYear", &CyReplayInfo::getStartYear, "int ()")
		.def("getFinalTurn", &CyReplayInfo::getFinalTurn, "int ()")
		.def("getFinalDate", &CyReplayInfo::getFinalDate, "wstring ()")
		.def("getCalendar", &CyReplayInfo::getCalendar, "int ()")

		.def("getFinalScore", &CyReplayInfo::getFinalScore, "int ()")
		.def("getFinalEconomy", &CyReplayInfo::getFinalEconomy, "int ()")
		.def("getFinalIndustry", &CyReplayInfo::getFinalIndustry, "int ()")
		.def("getFinalAgriculture", &CyReplayInfo::getFinalAgriculture, "int ()")

		.def("getMapWidth", &CyReplayInfo::getMapWidth, "int ()")
		.def("getMapHeight", &CyReplayInfo::getMapHeight, "int ()")

		.def("getModName", &CyReplayInfo::getModName, "std::wstring ()")
		;
		
	python::class_<CyHallOfFameInfo>("CyHallOfFameInfo")
		.def("loadReplays", &CyHallOfFameInfo::loadReplays, "void ()")
		.def("getNumGames", &CyHallOfFameInfo::getNumGames, "int ()")
		.def("getReplayInfo", &CyHallOfFameInfo::getReplayInfo, python::return_value_policy<python::manage_new_object>(), "CyReplayInfo* (int i)")
		;
}
