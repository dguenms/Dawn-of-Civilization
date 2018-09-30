#pragma component (mintypeinfo, on)

#include "CvGameCoreDLL.h"
#include "CyCity.h"
#include "CyPlot.h"
#include "CyArea.h"
#include "CvInfos.h"

//# include <boost/python/manage_new_object.hpp>
//# include <boost/python/return_value_policy.hpp>

//
// published python interface for CyCity
//

void CyCityPythonInterface2(python::class_<CyCity>& x)
{
	OutputDebugString("Python Extension Module - CyCityPythonInterface2\n");

	x
// BUG - Production Decay - start
		.def("getUnitProductionTime", &CyCity::getUnitProductionTime, "int (int /*UnitTypes*/ eIndex)")
		.def("setUnitProductionTime", &CyCity::setUnitProductionTime, "int (int /*UnitTypes*/ eIndex, int iNewValue)")
		.def("changeUnitProductionTime", &CyCity::changeUnitProductionTime, "int (int /*UnitTypes*/ eIndex, int iChange)")
		.def("isUnitProductionDecay", &CyCity::isUnitProductionDecay, "bool (int /*UnitTypes*/ eIndex)")
		.def("getUnitProductionDecay", &CyCity::getUnitProductionDecay, "int (int /*UnitTypes*/ eIndex)")
		.def("getUnitProductionDecayTurns", &CyCity::getUnitProductionDecayTurns, "int (int /*UnitTypes*/ eIndex)")
// BUG - Production Decay - end
// BUG - Project Production - start
		.def("getProjectProduction", &CyCity::getProjectProduction, "int (int /*ProjectTypes*/ eIndex)")
		.def("setProjectProduction", &CyCity::setProjectProduction, "void (int /*ProjectTypes*/ eIndex, int iNewValue)")
		.def("changeProjectProduction", &CyCity::changeProjectProduction, "void (int /*ProjectTypes*/ eIndex, int iChange)")
// BUG - Project Production - end
		.def("getGreatPeopleUnitRate", &CyCity::getGreatPeopleUnitRate, "int (int /*UnitTypes*/ iIndex)")
		.def("getGreatPeopleUnitProgress", &CyCity::getGreatPeopleUnitProgress, "int (int /*UnitTypes*/ iIndex)")
		.def("setGreatPeopleUnitProgress", &CyCity::setGreatPeopleUnitProgress, "int (int /*UnitTypes*/ iIndex, int iNewValue)")
		.def("changeGreatPeopleUnitProgress", &CyCity::changeGreatPeopleUnitProgress, "int (int /*UnitTypes*/ iIndex, int iChange)")
		.def("getSpecialistCount", &CyCity::getSpecialistCount, "int (int /*SpecialistTypes*/ eIndex)")
		.def("alterSpecialistCount", &CyCity::alterSpecialistCount, "int (int /*SpecialistTypes*/ eIndex, int iChange)")
		.def("getMaxSpecialistCount", &CyCity::getMaxSpecialistCount, "int (int /*SpecialistTypes*/ eIndex)")
		.def("isSpecialistValid", &CyCity::isSpecialistValid, "bool (int /*SpecialistTypes*/ eIndex, int iExtra)")
		.def("getForceSpecialistCount", &CyCity::getForceSpecialistCount, "int (int /*SpecialistTypes*/ eIndex)")
		.def("isSpecialistForced", &CyCity::isSpecialistForced, "bool ()")
		.def("setForceSpecialistCount", &CyCity::setForceSpecialistCount, "int (int /*SpecialistTypes*/ eIndex, int iNewValue")
		.def("changeForceSpecialistCount", &CyCity::changeForceSpecialistCount, "int (int /*SpecialistTypes*/ eIndex, int iChange")
		.def("getFreeSpecialistCount", &CyCity::getFreeSpecialistCount, "int (int /*SpecialistTypes*/ eIndex")
		.def("setFreeSpecialistCount", &CyCity::setFreeSpecialistCount, "int (int /*SpecialistTypes*/ eIndex, iNewValue")
		.def("changeFreeSpecialistCount", &CyCity::changeFreeSpecialistCount, "int (int /*SpecialistTypes*/ eIndex, iChange")
		.def("getAddedFreeSpecialistCount", &CyCity::getAddedFreeSpecialistCount, "int (int /*SpecialistTypes*/ eIndex")
		.def("getImprovementFreeSpecialists", &CyCity::getImprovementFreeSpecialists, "int (ImprovementID)")
		.def("changeImprovementFreeSpecialists", &CyCity::changeImprovementFreeSpecialists, "void (ImprovementID, iChange) - adjust ImprovementID free specialists by iChange")
		.def("getReligionInfluence", &CyCity::getReligionInfluence, "int (ReligionID) - value of influence from ReligionID")
		.def("changeReligionInfluence", &CyCity::changeReligionInfluence, "void (ReligionID, iChange) - adjust ReligionID influence by iChange")

		.def("getCurrentStateReligionHappiness", &CyCity::getCurrentStateReligionHappiness, "int ()")
		.def("getStateReligionHappiness", &CyCity::getStateReligionHappiness, "int (int /*ReligionTypes*/ ReligionID)")
		.def("changeStateReligionHappiness", &CyCity::changeStateReligionHappiness, "void (int /*ReligionTypes*/ ReligionID, iChange)")

		.def("getUnitCombatFreeExperience", &CyCity::getUnitCombatFreeExperience, "int (int /*UnitCombatTypes*/ eIndex)")
		.def("getFreePromotionCount", &CyCity::getFreePromotionCount, "int (int /*PromotionTypes*/ eIndex)")
		.def("isFreePromotion", &CyCity::isFreePromotion, "bool (int /*PromotionTypes*/ eIndex)")
		.def("getSpecialistFreeExperience", &CyCity::getSpecialistFreeExperience, "int ()")
		.def("getEspionageDefenseModifier", &CyCity::getEspionageDefenseModifier, "int ()")

		.def("isWorkingPlotByIndex", &CyCity::isWorkingPlotByIndex, "bool (iIndex) - true if a worker is working this city's plot iIndex")
		.def("isWorkingPlot", &CyCity::isWorkingPlot, "bool (iIndex) - true if a worker is working this city's pPlot")
		.def("alterWorkingPlot", &CyCity::alterWorkingPlot, "void (iIndex)")	
		.def("isHasRealBuilding", &CyCity::isHasRealBuilding, "bool (BuildingID) - real building or a free one?") //Rhye
		.def("setHasRealBuilding", &CyCity::setHasRealBuilding, "(BuildingID, bAdd) - if bAdd = 1 the building is Added, 0 it is removed") //Rhye
		.def("getNumRealBuilding", &CyCity::getNumRealBuilding, "int (BuildingID) - get # real building of this type")
		.def("setNumRealBuilding", &CyCity::setNumRealBuilding, "(BuildingID, iNum) - Sets number of buildings in this city of BuildingID type")
		.def("getNumFreeBuilding", &CyCity::getNumFreeBuilding, "int (BuildingID) - # of free Building ID (ie: from a Wonder)")
		.def("isHasReligion", &CyCity::isHasReligion, "bool (ReligionID) - does city have ReligionID?")
		.def("setHasReligion", &CyCity::setHasReligion, "void (ReligionID, bool bNewValue, bool bAnnounce, bool bArrows) - religion begins to spread")
		.def("isHasCorporation", &CyCity::isHasCorporation, "bool (CorporationID) - does city have CorporationID?")
		.def("setHasCorporation", &CyCity::setHasCorporation, "void (CorporationID, bool bNewValue, bool bAnnounce, bool bArrows) - corporation begins to spread")
		.def("isActiveCorporation", &CyCity::isActiveCorporation, "bool (CorporationID) - does city have active CorporationID?")
		.def("getTradeCity", &CyCity::getTradeCity, python::return_value_policy<python::manage_new_object>(), "CyCity (int iIndex) - remove SpecialistType[iIndex]")
		.def("getTradeRoutes", &CyCity::getTradeRoutes, "int ()")
		.def("getReligionCount", &CyCity::getReligionCount, "int ()") // edead

		.def("clearOrderQueue", &CyCity::clearOrderQueue, "void ()")
		.def("pushOrder", &CyCity::pushOrder, "void (OrderTypes eOrder, int iData1, int iData2, bool bSave, bool bPop, bool bAppend, bool bForce)")
		.def("popOrder", &CyCity::popOrder, "int (int iNum, bool bFinish, bool bChoose)")
		.def("getOrderQueueLength", &CyCity::getOrderQueueLength, "void ()")
		.def("getOrderFromQueue", &CyCity::getOrderFromQueue, python::return_value_policy<python::manage_new_object>(), "OrderData* (int iIndex)")

		.def("setWallOverridePoints", &CyCity::setWallOverridePoints, "setWallOverridePoints(const python::tuple& kPoints)")
		.def("getWallOverridePoints", &CyCity::getWallOverridePoints, "python::tuple getWallOverridePoints()")

		.def("AI_avoidGrowth", &CyCity::AI_avoidGrowth, "bool ()")
		.def("AI_isEmphasize", &CyCity::AI_isEmphasize, "bool (int iEmphasizeType)")
		.def("AI_countBestBuilds", &CyCity::AI_countBestBuilds, "int (CyArea* pArea)")
		.def("AI_cityValue", &CyCity::AI_cityValue, "int ()")

		.def("getScriptData", &CyCity::getScriptData, "str () - Get stored custom data (via pickle)")
		.def("setScriptData", &CyCity::setScriptData, "void (str) - Set stored custom data (via pickle)")

		.def("visiblePopulation", &CyCity::visiblePopulation, "int ()")

		.def("getBuildingYieldChange", &CyCity::getBuildingYieldChange, "int (int /*BuildingClassTypes*/ eBuildingClass, int /*YieldTypes*/ eYield)")
		.def("setBuildingYieldChange", &CyCity::setBuildingYieldChange, "void (int /*BuildingClassTypes*/ eBuildingClass, int /*YieldTypes*/ eYield, int iChange)")
		.def("changeBuildingYieldChange", &CyCity::changeBuildingYieldChange, "void (int /*BuildingClassTypes*/ eBuildingClass, int /*YieldTypes*/ eYield, int iChange)")
		.def("getBuildingCommerceChange", &CyCity::getBuildingCommerceChange, "int (int /*BuildingClassTypes*/ eBuildingClass, int /*CommerceTypes*/ eCommerce)")
		.def("setBuildingCommerceChange", &CyCity::setBuildingCommerceChange, "void (int /*BuildingClassTypes*/ eBuildingClass, int /*CommerceTypes*/ eCommerce, int iChange)")
		.def("getBuildingHappyChange", &CyCity::getBuildingHappyChange, "int (int /*BuildingClassTypes*/ eBuildingClass)")
		.def("setBuildingHappyChange", &CyCity::setBuildingHappyChange, "void (int /*BuildingClassTypes*/ eBuildingClass, int iChange)")
		.def("getBuildingHealthChange", &CyCity::getBuildingHealthChange, "int (int /*BuildingClassTypes*/ eBuildingClass)")
		.def("setBuildingHealthChange", &CyCity::setBuildingHealthChange, "void (int /*BuildingClassTypes*/ eBuildingClass, int iChange)")

		// Leoreth
		.def("getLiberationPlayer", &CyCity::getLiberationPlayer, "int ()")
		.def("liberate", &CyCity::liberate, "void ()")

		.def("changeBuildingCommerceChange", &CyCity::changeBuildingCommerceChange, "void (int eBuildingClass, int eCommerce, int iChange)")
		.def("updateBuildingCommerce", &CyCity::updateBuildingCommerce, "void ()")

		.def("getRegionID", &CyCity::getRegionID, "int ()")
		.def("setWeLoveTheKingDay", &CyCity::setWeLoveTheKingDay, "void (bool bNewValue)")
		.def("isMongolUP", &CyCity::isMongolUP, "bool ()")
		.def("setMongolUP", &CyCity::setMongolUP, "void (bool bNewValue)")
		.def("getGameTurnPlayerLost", &CyCity::getGameTurnPlayerLost, "int (int ePlayer)")
		.def("calculateOverallCulturePercent", &CyCity::calculateOverallCulturePercent, "int (int ePlayer)")
		.def("getNextCoveredPlot", &CyCity::getNextCoveredPlot, "int ()")
		.def("getCulturePlotIndex", &CyCity::getCulturePlotIndex, "int (int i)")
		.def("getCulturePlot", &CyCity::getCulturePlot, python::return_value_policy<python::manage_new_object>(), "CyPlot* (int i)")
		.def("getCultureCost", &CyCity::getCultureCost, "int (int i)")
		.def("getEffectiveNextCoveredPlot", &CyCity::getEffectiveNextCoveredPlot, "int ()")
		.def("isCoveredBeforeExpansion", &CyCity::isCoveredBeforeExpansion, "bool (int i)")
		.def("updateCultureCosts", &CyCity::updateCultureCosts, "void ()")
		.def("updateCoveredPlots", &CyCity::updateCoveredPlots, "void ()")
		.def("updateGreatWall", &CyCity::updateGreatWall, "void ()")
		.def("replaceReligion", &CyCity::replaceReligion, "void (int eOldReligion, int eNewReligion)")
		.def("removeReligion", &CyCity::removeReligion, "void (int eReligion)")
		.def("spreadReligion", &CyCity::spreadReligion, "void (int eReligion)")
		.def("setBuildingOriginalOwner", &CyCity::setBuildingOriginalOwner, "void (int eBuilding, int ePlayer)")
		.def("getHappinessYield", &CyCity::getHappinessYield, "int (int eCommerce)")
		.def("triggerMeltdown", &CyCity::triggerMeltdown, "void (int eBuilding)")
		.def("isColony", &CyCity::isColony, "bool ()")
		.def("hasBonusEffect", &CyCity::hasBonusEffect, "bool ()")
		.def("getCultureRank", &CyCity::getCultureRank, "int ()")
		.def("isHasBuildingEffect", &CyCity::isHasBuildingEffect, "bool (int eBuilding)")
		.def("getStabilityPopulation", &CyCity::getStabilityPopulation, "int ()")
		.def("setStabilityPopulation", &CyCity::setStabilityPopulation, "void (int iNewValue)")
		;
}
