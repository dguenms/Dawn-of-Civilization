#include "CvGameCoreDLL.h"
#include "CyPlayer.h"
#include "CvPlayer.h" // advc.enum: for PollutionFlags
#include "CySelectionGroup.h"
#include "CyArea.h"

//
// published python interface for CyPlayer
//

void CyPlayerPythonInterface2(python::class_<CyPlayer>& x)
{
	printToConsole("Python Extension Module - CyPlayerPythonInterface2\n");

	// set the docstring of the current module scope
	python::scope().attr("__doc__") = "Civilization IV Player Class";
	x
		// (kekm.34: Moved this block from CyPlayerInterface1.cpp)
		.def("trigger", &CyPlayer::trigger, "void (/*EventTriggerTypes*/int eEventTrigger)")
		.def("getEventOccured", &CyPlayer::getEventOccured, python::return_value_policy<python::reference_existing_object>(), "EventTriggeredData* (int /*EventTypes*/ eEvent)")
		.def("resetEventOccured", &CyPlayer::resetEventOccured, "void (int /*EventTypes*/ eEvent)")
		.def("getEventTriggered", &CyPlayer::getEventTriggered, python::return_value_policy<python::reference_existing_object>(), "EventTriggeredData* (int iID)")
		.def("initTriggeredData", &CyPlayer::initTriggeredData, python::return_value_policy<python::reference_existing_object>(), "EventTriggeredData* (int eEventTrigger, bool bFire, int iCityId, int iPlotX, int iPlotY, PlayerTypes eOtherPlayer, int iOtherPlayerCityId, ReligionTypes eReligion, CorporationTypes eCorporation, int iUnitId, BuildingTypes eBuilding)")
		.def("getEventTriggerWeight", &CyPlayer::getEventTriggerWeight, "int getEventTriggerWeight(int eEventTrigger)")

		.def("AI_updateFoundValues", &CyPlayer::AI_updateFoundValues, "void (bool bStartingLoc)")
		.def("AI_foundValue", &CyPlayer::AI_foundValue, "int (int, int, int, bool)")
		.def("AI_isFinancialTrouble", &CyPlayer::AI_isFinancialTrouble, "bool ()")
		.def("AI_isWillingToTalk", &CyPlayer::AI_isWillingToTalk, "bool (int /*PlayerTypes*/)") // K-Mod
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
		// advc.210:
		.def("checkAlert", &CyPlayer::checkAlert, "void (int alertId, bool silent)")
		// advc.210e:
		.def("AI_corporationBonusVal", &CyPlayer::AI_corporationBonusVal, "int (int)")
		// <advc.085>
		.def("setScoreboardExpanded", &CyPlayer::setScoreboardExpanded, "void (bool)")
		.def("isScoreboardExpanded", &CyPlayer::isScoreboardExpanded, "bool ()")
		// </advc.085> <advc.190c>
		.def("wasCivRandomlyChosen", &CyPlayer::wasCivRandomlyChosen, "bool ()")
		.def("wasLeaderRandomlyChosen", &CyPlayer::wasLeaderRandomlyChosen, "bool ()")
		// </advc.190c>

		.def("setFlag", &CyPlayer::setFlag, "void (str s)") // rfc
		.def("setLeader", &CyPlayer::setLeader, "void (int i)") // rfc
		.def("getLeader", &CyPlayer::getLeader, "int /*LeaderHeadTypes*/ ()") // rfc

		.def("updateTradeRoutes", &CyPlayer::updateTradeRoutes, "void ()") // doc
		.def("updateMaintenance", &CyPlayer::updateMaintenance, "void ()") // doc
		.def("AI_reset", &CyPlayer::AI_reset, "void ()") // doc
		.def("hasCivic", &CyPlayer::hasCivic, "bool (int iCivic)") // doc
		.def("getWorstEnemy", &CyPlayer::getWorstEnemy, "int ()") // doc
		.def("getInitialBirthTurn", &CyPlayer::getInitialBirthTurn, "int ()") // doc
		.def("setInitialBirthTurn", &CyPlayer::setInitialBirthTurn, "void (int iNewValue)") // doc
		.def("getLastBirthTurn", &CyPlayer::getLastBirthTurn, "int ()") // doc
		.def("setLastBirthTurn", &CyPlayer::setLastBirthTurn, "void (int iNewValue)") // doc
		.def("isSlaveTrade", &CyPlayer::isSlaveTrade, "bool (int iPlayer)") // doc
		.def("isHasBuilding", &CyPlayer::isHasBuilding, "bool (int eBuildingType)") // doc
		.def("isHasBuildingEffect", &CyPlayer::isHasBuildingEffect, "bool (int eBuildingType)") // doc
		.def("setStabilityParameter", &CyPlayer::setStabilityParameter, "void (int iParameter, int iNewValue)") // doc
		.def("countRequiredSlaves", &CyPlayer::countRequiredSlaves, "int ()") // doc
		.def("getEspionageExperience", &CyPlayer::getEspionageExperience, "int ()") // doc
		.def("setEspionageExperience", &CyPlayer::setEspionageExperience, "void (int iNewValue)") // doc
		.def("greatSpyThreshold", &CyPlayer::greatSpyThreshold, "int ()") // doc
		.def("setLeaderName", &CyPlayer::setLeaderName, "void (str name)") // doc
		.def("getModifier", &CyPlayer::getModifier, "int (int iModifierType)") // doc
		.def("setModifier", &CyPlayer::setModifier, "void (int iModifierType, int iNewValue)") // doc
		.def("getTechPreference", &CyPlayer::getTechPreference, "int (int eTech)") // doc
		.def("setTechPreference", &CyPlayer::setTechPreference, "void (int eTech, int iNewValue)") // doc
		.def("resetTechPreferences", &CyPlayer::resetTechPreferences, "void ()") // doc
		.def("getStartingEra", &CyPlayer::getStartingEra, "int ()") // doc
		.def("setStartingEra", &CyPlayer::setStartingEra, "void (int iNewValue)") // doc
		.def("setTargetDistanceValueModifier", &CyPlayer::setTargetDistanceValueModifier, "void (int iNewValue)") // doc
		.def("setReligiousTolerance", &CyPlayer::setReligiousTolerance, "void (int iNewValue)") // doc
		.def("getSpreadType", &CyPlayer::getSpreadType, "int (CyPlot* pPlot, int iReligion)") // doc
		.def("AI_chooseFreeTech", &CyPlayer::AI_chooseFreeTech, "void ()") // doc
		.def("isSlavery", &CyPlayer::isSlavery, "bool ()") // doc
		.def("isColonialSlavery", &CyPlayer::isColonialSlavery, "bool ()") // doc
		.def("getLastStateReligion", &CyPlayer::getLastStateReligion, "int ()") // doc
		.def("AI_bestCivic", &CyPlayer::AI_bestCivic, "int (int iCivicOptionType)") // doc
		.def("setFreeTechsOnDiscovery", &CyPlayer::setFreeTechsOnDiscovery, "void (int iNewValue)") // doc
		.def("AI_getNumCitySites", &CyPlayer::AI_getNumCitySites, "int ()") // doc
		.def("AI_getCitySite", &CyPlayer::AI_getCitySite, python::return_value_policy<python::manage_new_object>(), "CyPlot* (int iPlayer)") // doc
		.def("AI_getMemoryAttitude", &CyPlayer::AI_getMemoryAttitude, "int (int iPlayer, int iMemory)") // doc
		.def("restoreGeneralThreshold", &CyPlayer::restoreGeneralThreshold, "void ()") // doc
		.def("canResearchGiven", &CyPlayer::canResearchGiven, "bool (int eTech, bool bTrade, int eGivenTech)") // doc
		.def("resetGreatPeopleCreated", &CyPlayer::resetGreatPeopleCreated, "void ()") // doc
		.def("canUseSlaves", &CyPlayer::canUseSlaves, "bool ()") // doc
		.def("changeYieldRateModifier", &CyPlayer::changeYieldRateModifier, "void (int iYieldType, int iChange)") // doc
		.def("setBuildingClassPreference", &CyPlayer::setBuildingClassPreference, "void (int iBuildingClass, int iNewValue)") // doc
		.def("getBuildingClassPreference", &CyPlayer::getBuildingClassPreference, "int (int iBuildingClass)") // doc
		.def("resetBuildingClassPreferences", &CyPlayer::resetBuildingClassPreferences, "void ()") // doc
		.def("changeGreatPeopleCreated", &CyPlayer::changeGreatPeopleCreated, "void (int iChange)") // doc
		.def("changeGreatGeneralsCreated", &CyPlayer::changeGreatGeneralsCreated, "void (int iChange)") // doc
		.def("changeGreatSpiesCreated", &CyPlayer::changeGreatSpiesCreated, "void (int iChange)") // doc
		.def("launch", &CyPlayer::launch, "void (int iVictory)") // doc
		.def("AI_getAttitudeVal", &CyPlayer::AI_getAttitudeVal, "int (int iPlayer)") // doc
		.def("AI_getSameReligionAttitude", &CyPlayer::AI_getSameReligionAttitude, "int (int iPlayer)") // doc
		.def("AI_getDifferentReligionAttitude", &CyPlayer::AI_getDifferentReligionAttitude, "int (int iPlayer)") // doc
		.def("AI_getFirstImpressionAttitude", &CyPlayer::AI_getFirstImpressionAttitude, "int (int iPlayer)") // doc
		.def("setAlive", &CyPlayer::setAlive, "void (bool bNewValue, bool bTurnActive)") // doc
		.def("getPeriod", &CyPlayer::getPeriod, "int ()") // doc
		.def("getDomainFreeExperience", &CyPlayer::getDomainFreeExperience, "int (int iDomainType)") // doc
		.def("changeGoldPerTurnByPlayer", &CyPlayer::changeGoldPerTurnByPlayer, "void (int iPlayer, int iChange)") // doc
		.def("isUnstableCivic", &CyPlayer::isUnstableCivic, "bool (int iCivic)") // doc
		.def("setBirthProtected", &CyPlayer::setBirthProtected, "void (bool bNewValue)") // doc
		.def("isBirthProtected", &CyPlayer::isBirthProtected, "bool ()") // doc
		.def("changeNoAnarchyTurns", &CyPlayer::changeNoAnarchyTurns, "void (int iChange)") // doc
		.def("AI_doAdvancedStart", &CyPlayer::AI_doAdvancedStart, "void ()") // doc
		.def("setMinorCiv", &CyPlayer::setMinorCiv, "void (bool bNewValue)") // doc
		.def("verifyAlive", &CyPlayer::verifyAlive, "void ()") // doc
		.def("getReligionPopulation", &CyPlayer::getReligionPopulation, "int (int iReligion)") // doc

		.def("getScoreHistory", &CyPlayer::getScoreHistory, "int (int iTurn)") // doc
		.def("getEconomyHistory", &CyPlayer::getEconomyHistory, "int (int iTurn)") // doc
		.def("getIndustryHistory", &CyPlayer::getIndustryHistory, "int (int iTurn)") // doc
		.def("getAgricultureHistory", &CyPlayer::getAgricultureHistory, "int (int iTurn)") // doc
		.def("getPowerHistory", &CyPlayer::getPowerHistory, "int (int iTurn)") // doc
		.def("getCultureHistory", &CyPlayer::getCultureHistory, "int (int iTurn)") // doc
		.def("getEspionageHistory", &CyPlayer::getEspionageHistory, "int (int iTurn)") // doc
		.def("getTechnologyHistory", &CyPlayer::getTechnologyHistory, "int (int iTurn)") // doc
		.def("getPopulationHistory", &CyPlayer::getPopulationHistory, "int (int iTurn)") // doc
		.def("getLandHistory", &CyPlayer::getLandHistory, "int (int iTurn)") // doc

		.def("isExisting", &CyPlayer::isExisting, "bool ()") // doc
		.def("changeBonusImport", &CyPlayer::changeBonusImport, "void (int eBonus, int iChange)") // doc
		.def("AI_unitUpdate", &CyPlayer::AI_unitUpdate, "void ()") // doc
		.def("getModifiedCommerceRate", &CyPlayer::getModifiedCommerceRate, "int (CommerceTypes eCommerce)") // doc
		.def("canBuySlaves", &CyPlayer::canBuySlaves, "bool ()") // doc
		;

	/*	K-Mod, 5/jan/11: pollution flags (advc.enum: Moved from CyEnumsInterface
		b/c it's no longer a global type within the DLL) */
	// (advc.enum: Keep the name "Types" in Python although it's now "Flags" in the DLL)
	python::enum_<int>("PollutionTypes")
		.value("POLLUTION_POPULATION", CvPlayer::POLLUTION_POPULATION)
		.value("POLLUTION_BUILDINGS", CvPlayer::POLLUTION_BUILDINGS)
		.value("POLLUTION_BONUSES", CvPlayer::POLLUTION_BONUSES)
		.value("POLLUTION_POWER", CvPlayer::POLLUTION_POWER)
		.value("POLLUTION_ALL", CvPlayer::POLLUTION_ALL)
		;
}
