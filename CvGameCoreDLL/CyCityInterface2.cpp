#include "CvGameCoreDLL.h"

// kekm.34/advc: Added in order to reduce the size of CyCityInterface1.cpp

void CyCityPythonInterface2(python::class_<CyCity>& x)
{
	printToConsole("Python Extension Module - CyCityPythonInterface2\n");

	x	/*  advc: Arbitrarily moved these from CyCityInterface1.cpp so
			that nothing breaks if a few more functions are added there. */
		.def("getGreatPeopleUnitRate", &CyCity::getGreatPeopleUnitRate, "int (int /*UnitTypes*/ iIndex)")
		.def("getGreatPeopleUnitProgress", &CyCity::getGreatPeopleUnitProgress, "int (int /*UnitTypes*/ iIndex)")
		.def("setGreatPeopleUnitProgress", &CyCity::setGreatPeopleUnitProgress, "int (int /*UnitTypes*/ iIndex, int iNewValue)")
		.def("changeGreatPeopleUnitProgress", &CyCity::changeGreatPeopleUnitProgress, "int (int /*UnitTypes*/ iIndex, int iChange)")
		// advc.001c:
		.def("GPProjection", &CyCity::GPProjection, "int (int /*UnitTypes*/ iIndex)")
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
		.def("isHasRealBuilding", &CyCity::isHasRealBuilding, "bool (BuildingID) - real building or a free one?") // rfc
		.def("setHasRealBuilding", &CyCity::setHasRealBuilding, "(BuildingID, bAdd) - if bAdd = 1 the building is Added, 0 it is removed") // rfc
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
		.def("getReligionCount", &CyCity::getReligionCount, "int ()") // doc (edead)

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
		.def("changeBuildingYieldChange", &CyCity::changeBuildingYieldChange, "void (int /*BuildingClassTypes*/ eBuildingClass, int /*YieldTypes*/ eYield, int iChange)") // doc
		.def("getBuildingCommerceChange", &CyCity::getBuildingCommerceChange, "int (int /*BuildingClassTypes*/ eBuildingClass, int /*CommerceTypes*/ eCommerce)")
		.def("setBuildingCommerceChange", &CyCity::setBuildingCommerceChange, "void (int /*BuildingClassTypes*/ eBuildingClass, int /*CommerceTypes*/ eCommerce, int iChange)")
		.def("getBuildingHappyChange", &CyCity::getBuildingHappyChange, "int (int /*BuildingClassTypes*/ eBuildingClass)")
		.def("setBuildingHappyChange", &CyCity::setBuildingHappyChange, "void (int /*BuildingClassTypes*/ eBuildingClass, int iChange)")
		.def("getBuildingHealthChange", &CyCity::getBuildingHealthChange, "int (int /*BuildingClassTypes*/ eBuildingClass)")
		.def("setBuildingHealthChange", &CyCity::setBuildingHealthChange, "void (int /*BuildingClassTypes*/ eBuildingClass, int iChange)")

		.def("getLiberationPlayer", &CyCity::getLiberationPlayer, "int ()")
		.def("liberate", &CyCity::liberate, "void ()")

		.def("changeBuildingCommerceChange", &CyCity::changeBuildingCommerceChange, "void (int eBuildingClass, int eCommerce, int iChange)") // doc
		.def("updateBuildingCommerce", &CyCity::updateBuildingCommerce, "void ()") // doc

		.def("getRegionID", &CyCity::getRegionID, "int ()") // doc
		.def("setWeLoveTheKingDay", &CyCity::setWeLoveTheKingDay, "void (bool bNewValue)") // doc
		.def("isMongolUP", &CyCity::isMongolUP, "bool ()") // doc
		.def("setMongolUP", &CyCity::setMongolUP, "void (bool bNewValue)") // doc
		.def("getGameTurnPlayerLost", &CyCity::getGameTurnPlayerLost, "int (int ePlayer)") // doc
		.def("getGameTurnCivLost", &CyCity::getGameTurnCivLost, "int (int iCivilizations)") // doc
		.def("calculateOverallCulturePercent", &CyCity::calculateOverallCulturePercent, "int (int ePlayer)") // doc
		.def("getNextCoveredPlot", &CyCity::getNextCoveredPlot, "int ()") // doc
		.def("getCulturePlotIndex", &CyCity::getCulturePlotIndex, "int (int i)") // doc
		.def("getCulturePlot", &CyCity::getCulturePlot, python::return_value_policy<python::manage_new_object>(), "CyPlot* (int i)") // doc
		.def("getCultureCost", &CyCity::getCultureCost, "int (int i)") // doc
		.def("getEffectiveNextCoveredPlot", &CyCity::getEffectiveNextCoveredPlot, "int ()") // doc
		.def("isCoveredBeforeExpansion", &CyCity::isCoveredBeforeExpansion, "bool (int i)") // doc
		.def("updateCultureCosts", &CyCity::updateCultureCosts, "void ()") // doc
		.def("updateCoveredPlots", &CyCity::updateCoveredPlots, "void ()") // doc
		.def("updateGreatWall", &CyCity::updateGreatWall, "void ()") // doc
		.def("replaceReligion", &CyCity::replaceReligion, "void (int eOldReligion, int eNewReligion)") // doc
		.def("removeReligion", &CyCity::removeReligion, "void (int eReligion)") // doc
		.def("spreadReligion", &CyCity::spreadReligion, "void (int eReligion)") // doc
		.def("setBuildingOriginalOwner", &CyCity::setBuildingOriginalOwner, "void (int eBuilding, int eCivilization)") // doc
		.def("setBuildingOriginalTime", &CyCity::setBuildingOriginalTime, "void (int eBuilding, int iYear)") // doc
		.def("triggerMeltdown", &CyCity::triggerMeltdown, "void (int eBuilding)") // doc
		.def("isColony", &CyCity::isColony, "bool ()") // doc
		.def("hasBonusEffect", &CyCity::hasBonusEffect, "bool ()") // doc
		.def("getCultureRank", &CyCity::getCultureRank, "int ()") // doc
		.def("isHasBuildingEffect", &CyCity::isHasBuildingEffect, "bool (int eBuilding)") // doc
		.def("getStabilityPopulation", &CyCity::getStabilityPopulation, "int ()") // doc
		.def("setStabilityPopulation", &CyCity::setStabilityPopulation, "void (int iNewValue)") // doc
		.def("getModifiedCultureRate", &CyCity::getModifiedCultureRate, "int ()") // doc
		.def("getModifiedCultureRateTimes100", &CyCity::getModifiedCultureRateTimes100, "int ()") // doc
		.def("getNumActiveWorldWonders", &CyCity::getNumActiveWorldWonders, "int ()") // doc
		.def("isCore", &CyCity::isCore, "bool (int iCivilization)") // doc
		.def("isPlayerCore", &CyCity::isPlayerCore, "bool (int iPlayer)") // doc
		.def("isOwnerCore", &CyCity::isOwnerCore, "bool ()") // doc
		.def("getActualCulture", &CyCity::getActualCulture, "int (int iPlayer)") // doc
		.def("getTotalPopulationLoss", &CyCity::getTotalPopulationLoss, "int ()") // doc
		.def("countSatellites", &CyCity::countSatellites, "int ()") // doc
		.def("getSatelliteSlots", &CyCity::getSatelliteSlots, "int ()") // doc
		.def("getArea", &CyCity::getArea, "int ()") // doc
		.def("rebuild", &CyCity::rebuild, "bool (int iEra)") // doc
		.def("isValidBuildingLocation", &CyCity::isValidBuildingLocation, "bool (int eBuilding)") // doc
		.def("getArea", &CyCity::getArea, "int ()") // doc
		.def("rebuild", &CyCity::rebuild, "bool ()") // doc
		.def("isValidBuildingLocation", &CyCity::isValidBuildingLocation, "bool (int eBuilding)") // doc
		.def("getPreviousCiv", &CyCity::getPreviousCiv, "int ()") // doc
		.def("getOriginalCiv", &CyCity::getOriginalCiv, "int ()") // doc
		.def("setOriginalCiv", &CyCity::setOriginalCiv, "void (int iCivilization)") // doc
		.def("setEverOwned", &CyCity::setEverOwned, "void (int iCivilization, bool bNewValue)") // doc
		.def("setGameTurnFounded", &CyCity::setGameTurnFounded, "void (int iNewValue)") // doc
		.def("setGameTurnAcquired", &CyCity::setGameTurnAcquired, "void (int iNewValue)") // doc
		.def("isEverOwnedCiv", &CyCity::isEverOwnedCiv, "bool (int iCivilization)") // doc
		.def("setCivCulture", &CyCity::setCivCulture, "void (int iCivilization, int iNewValue)") // doc
		.def("isOriginalOwner", &CyCity::isOriginalOwner, "bool (int iPlayer)") // doc
		.def("getCorporationBadHappiness", &CyCity::getCorporationBadHappiness, "int ()") // doc
		.def("getCorporationCount", &CyCity::getCorporationCount, "int ()") // doc
		.def("doPlotCulture", &CyCity::doPlotCulture, "void (bool bUpdate, int ePlayer, int iCultureRate, bool bOwned)") // doc
		.def("AI_updateAssignWork", &CyCity::AI_updateAssignWork, "void ()") // doc
		.def("getHurryPercentAnger", &CyCity::getHurryPercentAnger, "int ()") // doc
		.def("getConscriptPercentAnger", &CyCity::getConscriptPercentAnger, "int ()") // doc
		.def("canBeSelected", &CyCity::canBeSelected, "bool ()") // doc
		;
}
