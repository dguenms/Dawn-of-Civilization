#include "CvGameCoreDLL.h"
#include "CyPlayer.h"
#include "CyUnit.h"
#include "CyCity.h"
#include "CyPlot.h"
#include "CySelectionGroup.h"
#include "CyArea.h"
//# include <boost/python/manage_new_object.hpp>
//# include <boost/python/return_value_policy.hpp>
//# include <boost/python/scope.hpp>

//
// published python interface for CyPlayer
//

void CyPlayerPythonInterface2(python::class_<CyPlayer>& x)
{
	OutputDebugString("Python Extension Module - CyPlayerPythonInterface2\n");

	// set the docstring of the current module scope 
	python::scope().attr("__doc__") = "Civilization IV Player Class"; 
	x
		.def("AI_updateFoundValues", &CyPlayer::AI_updateFoundValues, "void (bool bStartingLoc)")
		.def("AI_foundValue", &CyPlayer::AI_foundValue, "int (int, int, int, bool)")
		.def("AI_isFinancialTrouble", &CyPlayer::AI_isFinancialTrouble, "bool ()")
		.def("AI_demandRebukedWar", &CyPlayer::AI_demandRebukedWar, "bool (int /*PlayerTypes*/)")
		.def("AI_getAttitude", &CyPlayer::AI_getAttitude, "AttitudeTypes (int /*PlayerTypes*/) - Gets the attitude of the player towards the player passed in")
		.def("AI_unitValue", &CyPlayer::AI_unitValue, "int (int /*UnitTypes*/ eUnit, int /*UnitAITypes*/ eUnitAI, CyArea* pArea)")
		.def("AI_civicValue", &CyPlayer::AI_civicValue, "int (int /*CivicTypes*/ eCivic)")
		.def("AI_totalUnitAIs", &CyPlayer::AI_totalUnitAIs, "int (int /*UnitAITypes*/ eUnitAI)")
		.def("AI_totalAreaUnitAIs", &CyPlayer::AI_totalAreaUnitAIs, "int (CyArea* pArea, int /*UnitAITypes*/ eUnitAI)")
		.def("AI_totalWaterAreaUnitAIs", &CyPlayer::AI_totalWaterAreaUnitAIs, "int (CyArea* pArea, int /*UnitAITypes*/ eUnitAI)")
		.def("AI_getNumAIUnits", &CyPlayer::AI_getNumAIUnits, "int (UnitAIType) - Returns # of UnitAITypes the player current has of UnitAIType")
		.def("AI_getAttitudeExtra", &CyPlayer::AI_getAttitudeExtra, "int (int /*PlayerTypes*/ eIndex) - Returns the extra attitude for this player - usually scenario specific")
		.def("AI_setAttitudeExtra", &CyPlayer::AI_setAttitudeExtra, "void (int /*PlayerTypes*/ eIndex, int iNewValue) - Sets the extra attitude for this player - usually scenario specific")
		.def("AI_changeAttitudeExtra", &CyPlayer::AI_changeAttitudeExtra, "void (int /*PlayerTypes*/ eIndex, int iChange) - Changes the extra attitude for this player - usually scenario specific")
		.def("AI_getMemoryCount", &CyPlayer::AI_getMemoryCount, "int (/*PlayerTypes*/ eIndex1, /*MemoryTypes*/ eIndex2)")
		.def("AI_changeMemoryCount", &CyPlayer::AI_changeMemoryCount, "void (/*PlayerTypes*/ eIndex1, /*MemoryTypes*/ eIndex2, int iChange)")
		.def("AI_getExtraGoldTarget", &CyPlayer::AI_getExtraGoldTarget, "int ()")
		.def("AI_setExtraGoldTarget", &CyPlayer::AI_setExtraGoldTarget, "void (int)")
// BUG - Refuses to Talk - start
		.def("AI_isWillingToTalk", &CyPlayer::AI_isWillingToTalk, "bool (int /*PlayerTypes*/)")
// BUG - Refuses to Talk - end

		.def("getScriptData", &CyPlayer::getScriptData, "str () - Get stored custom data (via pickle)")
		.def("setScriptData", &CyPlayer::setScriptData, "void (str) - Set stored custom data (via pickle)")

		.def("chooseTech", &CyPlayer::chooseTech, "void (int iDiscover, wstring szText, bool bFront)")

		.def("AI_maxGoldTrade", &CyPlayer::AI_maxGoldTrade, "int (int)")
		.def("AI_maxGoldPerTurnTrade", &CyPlayer::AI_maxGoldPerTurnTrade, "int (int)")

		.def("splitEmpire", &CyPlayer::splitEmpire, "bool (int iAreaId)")
		.def("canSplitEmpire", &CyPlayer::canSplitEmpire, "bool ()")
		.def("canSplitArea", &CyPlayer::canSplitArea, "bool (int)")
		.def("canHaveTradeRoutesWith", &CyPlayer::canHaveTradeRoutesWith, "bool (int)")
		.def("forcePeace", &CyPlayer::forcePeace, "void (int)")
		
// BUG - Reminder Mod - start
		.def("addReminder", &CyPlayer::addReminder, "void (int iGameTurn, string szMessage)")
// BUG - Reminder Mod - end

		.def("setFlag", &CyPlayer::setFlag, "void (str s)") //Rhye
		.def("setLeader", &CyPlayer::setLeader, "void (int i)") //Rhye
		.def("getLeader", &CyPlayer::getLeader, "int /*LeaderHeadTypes*/ ()") //Rhye

		//Leoreth
		.def("updateTradeRoutes", &CyPlayer::updateTradeRoutes, "void ()")
		.def("updateMaintenance", &CyPlayer::updateMaintenance, "void ()")
		.def("AI_reset", &CyPlayer::AI_reset, "void ()")
		.def("hasCivic", &CyPlayer::hasCivic, "bool (int iCivic)")
		.def("getWorstEnemy", &CyPlayer::getWorstEnemy, "int ()")
		.def("getInitialBirthTurn", &CyPlayer::getInitialBirthTurn, "int ()")
		.def("setInitialBirthTurn", &CyPlayer::setInitialBirthTurn, "void (int iNewValue)")
		.def("getLastBirthTurn", &CyPlayer::getLastBirthTurn, "int ()")
		.def("setLastBirthTurn", &CyPlayer::setLastBirthTurn, "void (int iNewValue)")
		.def("isSlaveTrade", &CyPlayer::isSlaveTrade, "bool (int iPlayer)")
		.def("isHasBuilding", &CyPlayer::isHasBuilding, "bool (int eBuildingType)")
		.def("isHasBuildingEffect", &CyPlayer::isHasBuildingEffect, "bool (int eBuildingType)")
		.def("setStabilityParameter", &CyPlayer::setStabilityParameter, "void (int iParameter, int iNewValue)")
		.def("countRequiredSlaves", &CyPlayer::countRequiredSlaves, "int ()")
		.def("getEspionageExperience", &CyPlayer::getEspionageExperience, "int ()")
		.def("setEspionageExperience", &CyPlayer::setEspionageExperience, "void (int iNewValue)")
		.def("greatSpyThreshold", &CyPlayer::greatSpyThreshold, "int ()")
		.def("setLeaderName", &CyPlayer::setLeaderName, "void (str name)")
		.def("getSettlerValue", &CyPlayer::getSettlerValue, "int (int x, int y)")
		.def("getWarValue", &CyPlayer::getWarValue, "int (int x, int y)")
		.def("getModifier", &CyPlayer::getModifier, "int (int iModifierType)")
		.def("setModifier", &CyPlayer::setModifier, "void (int iModifierType, int iNewValue)")
		.def("getTechPreference", &CyPlayer::getTechPreference, "int (int eTech)")
		.def("setTechPreference", &CyPlayer::setTechPreference, "void (int eTech, int iNewValue)")
		.def("resetTechPreferences", &CyPlayer::resetTechPreferences, "void ()")
		.def("getStartingEra", &CyPlayer::getStartingEra, "int ()")
		.def("setStartingEra", &CyPlayer::setStartingEra, "void (int iNewValue)")
		.def("setTakenTilesThreshold", &CyPlayer::setTakenTilesThreshold, "void (int iNewValue)")
		.def("setDistanceSubtrahend", &CyPlayer::setDistanceSubtrahend, "void (int iNewValue)")
		.def("setDistanceFactor", &CyPlayer::setDistanceFactor, "void (int iNewValue)")
		.def("setCompactnessModifier", &CyPlayer::setCompactnessModifier, "void (int iNewValue)")
		.def("setTargetDistanceValueModifier", &CyPlayer::setTargetDistanceValueModifier, "void (int iNewValue)")
		.def("setReligiousTolerance", &CyPlayer::setReligiousTolerance, "void (int iNewValue)")
		.def("getSpreadType", &CyPlayer::getSpreadType, "int (CyPlot* pPlot, int iReligion)")
		.def("AI_chooseFreeTech", &CyPlayer::AI_chooseFreeTech, "void ()")
		.def("isSlavery", &CyPlayer::isSlavery, "bool ()")
		.def("isColonialSlavery", &CyPlayer::isColonialSlavery, "bool ()")
		.def("getLastStateReligion", &CyPlayer::getLastStateReligion, "int ()")
		.def("AI_bestCivic", &CyPlayer::AI_bestCivic, "int (int iCivicOptionType)")
		.def("setFreeTechsOnDiscovery", &CyPlayer::setFreeTechsOnDiscovery, "void (int iNewValue)")
		.def("AI_getNumCitySites", &CyPlayer::AI_getNumCitySites, "int ()")
		.def("AI_getCitySite", &CyPlayer::AI_getCitySite, python::return_value_policy<python::manage_new_object>(), "CyPlot* (int iPlayer)")
		.def("AI_getMemoryAttitude", &CyPlayer::AI_getMemoryAttitude, "int (int iPlayer, int iMemory)")
		.def("restoreGeneralThreshold", &CyPlayer::restoreGeneralThreshold, "void ()")
		.def("canResearchGiven", &CyPlayer::canResearchGiven, "bool (int eTech, bool bTrade, int eGivenTech)")
		.def("resetGreatPeopleCreated", &CyPlayer::resetGreatPeopleCreated, "void ()")
		.def("canUseSlaves", &CyPlayer::canUseSlaves, "bool ()")
		.def("changeYieldRateModifier", &CyPlayer::changeYieldRateModifier, "void (int iYieldType, int iChange)")
		.def("setBuildingClassPreference", &CyPlayer::setBuildingClassPreference, "void (int iBuildingClass, int iNewValue)")
		.def("getBuildingClassPreference", &CyPlayer::getBuildingClassPreference, "int (int iBuildingClass)")
		.def("resetBuildingClassPreferences", &CyPlayer::resetBuildingClassPreferences, "void ()")
		.def("changeGreatPeopleCreated", &CyPlayer::changeGreatPeopleCreated, "void (int iChange)")
		.def("changeGreatGeneralsCreated", &CyPlayer::changeGreatGeneralsCreated, "void (int iChange)")
		.def("changeGreatSpiesCreated", &CyPlayer::changeGreatSpiesCreated, "void (int iChange)")
		.def("launch", &CyPlayer::launch, "void (int iVictory)")
		.def("isNoTemporaryUnhappiness", &CyPlayer::isNoTemporaryUnhappiness, "bool ()")
		.def("AI_getAttitudeVal", &CyPlayer::AI_getAttitudeVal, "int (int iPlayer)")
		.def("AI_getSameReligionAttitude", &CyPlayer::AI_getSameReligionAttitude, "int (int iPlayer)")
		.def("AI_getDifferentReligionAttitude", &CyPlayer::AI_getDifferentReligionAttitude, "int (int iPlayer)")
		.def("AI_getFirstImpressionAttitude", &CyPlayer::AI_getFirstImpressionAttitude, "int (int iPlayer)")
		.def("setAlive", &CyPlayer::setAlive, "void (bool bNewValue, bool bTurnActive)")
		.def("getPeriod", &CyPlayer::getPeriod, "int ()")
		.def("getDomainFreeExperience", &CyPlayer::getDomainFreeExperience, "int (int iDomainType)")
		.def("changeGoldPerTurnByPlayer", &CyPlayer::changeGoldPerTurnByPlayer, "void (int iPlayer, int iChange)")
		.def("getUnhappinessDecayModifier", &CyPlayer::getUnhappinessDecayModifier, "int ()")
		.def("isUnstableCivic", &CyPlayer::isUnstableCivic, "bool (int iCivic)")
		.def("setBirthProtected", &CyPlayer::setBirthProtected, "void (bool bNewValue)")
		.def("isBirthProtected", &CyPlayer::isBirthProtected, "bool ()")
		.def("changeNoAnarchyTurns", &CyPlayer::changeNoAnarchyTurns, "void (int iChange)")
		.def("AI_doAdvancedStart", &CyPlayer::AI_doAdvancedStart, "void ()")
		.def("setMinorCiv", &CyPlayer::setMinorCiv, "void (bool bNewValue)")
		.def("verifyAlive", &CyPlayer::verifyAlive, "void ()")
		.def("getReligionPopulation", &CyPlayer::getReligionPopulation, "int (int iReligion)")

		.def("getScoreHistory", &CyPlayer::getScoreHistory, "int (int iTurn)")
		.def("getEconomyHistory", &CyPlayer::getEconomyHistory, "int (int iTurn)")
		.def("getIndustryHistory", &CyPlayer::getIndustryHistory, "int (int iTurn)")
		.def("getAgricultureHistory", &CyPlayer::getAgricultureHistory, "int (int iTurn)")
		.def("getPowerHistory", &CyPlayer::getPowerHistory, "int (int iTurn)")
		.def("getCultureHistory", &CyPlayer::getCultureHistory, "int (int iTurn)")
		.def("getEspionageHistory", &CyPlayer::getEspionageHistory, "int (int iTurn)")
		.def("getTechnologyHistory", &CyPlayer::getTechnologyHistory, "int (int iTurn)")
		.def("getPopulationHistory", &CyPlayer::getPopulationHistory, "int (int iTurn)")
		.def("getLandHistory", &CyPlayer::getLandHistory, "int (int iTurn)")

		.def("isExisting", &CyPlayer::isExisting, "bool ()")
		;
}
