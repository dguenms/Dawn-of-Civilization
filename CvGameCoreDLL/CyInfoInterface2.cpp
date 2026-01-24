#include "CvGameCoreDLL.h"
#include "CvInfos.h"

//
// Python interface for info classes (formerly structs)
// These are simple enough to be exposed directly - no wrappers
//

void CyInfoPythonInterface2()
{
	OutputDebugString("Python Extension Module - CyInfoPythonInterface2\n");

	python::class_<CvBuildingClassInfo, python::bases<CvInfoBase> >("CvBuildingClassInfo")
		.def("getMaxGlobalInstances", &CvBuildingClassInfo::getMaxGlobalInstances, "int ()")
		.def("getMaxTeamInstances", &CvBuildingClassInfo::getMaxTeamInstances, "int ()")
		.def("getMaxPlayerInstances", &CvBuildingClassInfo::getMaxPlayerInstances, "int ()")
		.def("getExtraPlayerInstances", &CvBuildingClassInfo::getExtraPlayerInstances, "int ()")
		.def("getDefaultBuildingIndex", &CvBuildingClassInfo::getDefaultBuildingIndex, "int ()")

		.def("isNoLimit", &CvBuildingClassInfo::isNoLimit, "bool ()")
		.def("isMonument", &CvBuildingClassInfo::isMonument, "bool ()")

		// Arrays

		.def("getVictoryThreshold", &CvBuildingClassInfo::getVictoryThreshold, "int (int i)")
		;

	python::class_<CvRouteModelInfo, python::bases<CvInfoBase> >("CvRouteModelInfo")

		.def("getModelFile", &CvRouteModelInfo::getModelFile, "string ()")
		.def("setModelFile", &CvRouteModelInfo::setModelFile, "void (string)")
		.def("getModelFileKey", &CvRouteModelInfo::getModelFileKey, "string ()")
		.def("setModelFileKey", &CvRouteModelInfo::setModelFileKey, "void (string)")

		.def("getConnectString", &CvRouteModelInfo::getConnectString, "string ()")
		.def("getModelConnectString", &CvRouteModelInfo::getModelConnectString, "string ()")
		.def("getRotateString", &CvRouteModelInfo::getRotateString, "string ()")
		;

	python::class_<CvCivilizationInfo, python::bases<CvInfoBase> >("CvCivilizationInfo")
		.def("getDefaultPlayerColor", &CvCivilizationInfo::getDefaultPlayerColor, "int ()")
		.def("getArtStyleType", &CvCivilizationInfo::getArtStyleType, "int ()")
		.def("getNumCityNames", &CvCivilizationInfo::getNumCityNames, "int ()")
		.def("getNumLeaders", &CvCivilizationInfo::getNumLeaders, "int ()")

		.def("getSelectionSoundScriptId", &CvCivilizationInfo::getSelectionSoundScriptId)
		.def("getActionSoundScriptId", &CvCivilizationInfo::getActionSoundScriptId)

		.def("isAIPlayable", &CvCivilizationInfo::isAIPlayable, "bool ()")
		.def("isPlayable", &CvCivilizationInfo::isPlayable, "bool ()")

		.def("getShortDescription", &CvCivilizationInfo::pyGetShortDescription, "wstring ()")
		.def("getShortDescriptionKey", &CvCivilizationInfo::pyGetShortDescriptionKey, "wstring ()")
		.def("getAdjective", &CvCivilizationInfo::pyGetAdjective, "wstring ()")
		.def("getFlagTexture", &CvCivilizationInfo::getFlagTexture, "string ()")
		.def("getArtDefineTag", &CvCivilizationInfo::getArtDefineTag, "string ()")
		.def("getButton", &CvCivilizationInfo::getButton, "string ()")

		.def("getDerivativeCiv", &CvCivilizationInfo::getDerivativeCiv, "int ()")

		// Arrays

		.def("getCivilizationBuildings", &CvCivilizationInfo::getCivilizationBuildings, "int (int i)")
		.def("getCivilizationUnits", &CvCivilizationInfo::getCivilizationUnits, "int (int i)")
		.def("getCivilizationFreeUnitsClass", &CvCivilizationInfo::getCivilizationFreeUnitsClass, "int (int i)")
		.def("getCivilizationInitialCivics", &CvCivilizationInfo::getCivilizationInitialCivics, "int (int i)")

		.def("isLeaders", &CvCivilizationInfo::isLeaders, "bool (int i)")
		.def("isCivilizationFreeBuildingClass", &CvCivilizationInfo::isCivilizationFreeBuildingClass, "bool (int i)")
		.def("isCivilizationFreeTechs", &CvCivilizationInfo::isCivilizationFreeTechs, "bool (int i)")
		.def("isCivilizationDisableTechs", &CvCivilizationInfo::isCivilizationDisableTechs, "bool (int i)")

		.def("getCityNames", &CvCivilizationInfo::getCityNames, "string (int i)")
		;

	python::class_<CvVictoryInfo, python::bases<CvInfoBase> >("CvVictoryInfo")
		.def("getPopulationPercentLead", &CvVictoryInfo::getPopulationPercentLead, "int ()")
		.def("getLandPercent", &CvVictoryInfo::getLandPercent, "int ()")
		.def("getMinLandPercent", &CvVictoryInfo::getMinLandPercent, "int ()")
		.def("getReligionPercent", &CvVictoryInfo::getReligionPercent, "int ()")
		.def("getCityCulture", &CvVictoryInfo::getCityCulture, "int ()")
		.def("getNumCultureCities", &CvVictoryInfo::getNumCultureCities, "int ()")
		.def("getTotalCultureRatio", &CvVictoryInfo::getTotalCultureRatio, "int ()")
		.def("getVictoryDelayTurns", &CvVictoryInfo::getVictoryDelayTurns, "int ()")

		.def("isTargetScore", &CvVictoryInfo::isTargetScore, "bool ()")
		.def("isEndScore", &CvVictoryInfo::isEndScore, "bool ()")
		.def("isConquest", &CvVictoryInfo::isConquest, "bool ()")
		.def("isDiploVote", &CvVictoryInfo::isDiploVote, "bool ()")
		.def("isPermanent", &CvVictoryInfo::isPermanent, "bool ()")

		.def("getMovie", &CvVictoryInfo::getMovie, "string ()")
		;

	python::class_<CvHurryInfo, python::bases<CvInfoBase> >("CvHurryInfo")
		.def("getGoldPerProduction", &CvHurryInfo::getGoldPerProduction, "int ()")
		.def("getProductionPerPopulation", &CvHurryInfo::getProductionPerPopulation, "int ()")

		.def("isAnger", &CvHurryInfo::isAnger, "bool ()")
		;

	python::class_<CvHandicapInfo, python::bases<CvInfoBase> >("CvHandicapInfo")
		.def("getFreeWinsVsBarbs", &CvHandicapInfo::getFreeWinsVsBarbs, "int ()")
		.def("getAnimalAttackProb", &CvHandicapInfo::getAnimalAttackProb, "int ()")
		.def("getStartingLocationPercent", &CvHandicapInfo::getStartingLocationPercent, "int ()")
		.def("getStartingGold", &CvHandicapInfo::getStartingGold, "int ()")
		.def("getFreeUnits", &CvHandicapInfo::getFreeUnits, "int ()")
		.def("getUnitCostPercent", &CvHandicapInfo::getUnitCostPercent, "int ()")
		.def("getResearchPercent", &CvHandicapInfo::getResearchPercent, "int ()")
		.def("getDistanceMaintenancePercent", &CvHandicapInfo::getDistanceMaintenancePercent, "int ()")
		.def("getNumCitiesMaintenancePercent", &CvHandicapInfo::getNumCitiesMaintenancePercent, "int ()")
		.def("getMaxNumCitiesMaintenance", &CvHandicapInfo::getMaxNumCitiesMaintenance, "int ()")
		.def("getColonyMaintenancePercent", &CvHandicapInfo::getColonyMaintenancePercent, "int ()")
		.def("getMaxColonyMaintenance", &CvHandicapInfo::getMaxColonyMaintenance, "int ()")
		.def("getCorporationMaintenancePercent", &CvHandicapInfo::getCorporationMaintenancePercent, "int ()")
		.def("getCivicUpkeepPercent", &CvHandicapInfo::getCivicUpkeepPercent, "int ()")
		.def("getInflationPercent", &CvHandicapInfo::getInflationPercent, "int ()")
		.def("getHealthBonus", &CvHandicapInfo::getHealthBonus, "int ()")
		.def("getHappyBonus", &CvHandicapInfo::getHappyBonus, "int ()")
		.def("getAttitudeChange", &CvHandicapInfo::getAttitudeChange, "int ()")
		.def("getNoTechTradeModifier", &CvHandicapInfo::getNoTechTradeModifier, "int ()")
		.def("getTechTradeKnownModifier", &CvHandicapInfo::getTechTradeKnownModifier, "int ()")
		.def("getUnownedTilesPerGameAnimal", &CvHandicapInfo::getUnownedTilesPerGameAnimal, "int ()")
		.def("getUnownedTilesPerBarbarianUnit", &CvHandicapInfo::getUnownedTilesPerBarbarianUnit, "int ()")
		.def("getUnownedWaterTilesPerBarbarianUnit", &CvHandicapInfo::getUnownedWaterTilesPerBarbarianUnit, "int ()")
		.def("getUnownedTilesPerBarbarianCity", &CvHandicapInfo::getUnownedTilesPerBarbarianCity, "int ()")
		.def("getBarbarianCreationTurnsElapsed", &CvHandicapInfo::getBarbarianCreationTurnsElapsed, "int ()")
		.def("getBarbarianCityCreationTurnsElapsed", &CvHandicapInfo::getBarbarianCityCreationTurnsElapsed, "int ()")
		.def("getBarbarianCityCreationProb", &CvHandicapInfo::getBarbarianCityCreationProb, "int ()")
		.def("getAnimalCombatModifier", &CvHandicapInfo::getAnimalCombatModifier, "int ()")
		.def("getBarbarianCombatModifier", &CvHandicapInfo::getBarbarianCombatModifier, "int ()")
		.def("getAIAnimalCombatModifier", &CvHandicapInfo::getAIAnimalCombatModifier, "int ()")
		.def("getAIBarbarianCombatModifier", &CvHandicapInfo::getAIBarbarianCombatModifier, "int ()")

		.def("getStartingDefenseUnits", &CvHandicapInfo::getStartingDefenseUnits, "int ()")
		.def("getStartingWorkerUnits", &CvHandicapInfo::getStartingWorkerUnits, "int ()")
		.def("getStartingExploreUnits", &CvHandicapInfo::getStartingExploreUnits, "int ()")
		.def("getAIStartingUnitMultiplier", &CvHandicapInfo::getAIStartingUnitMultiplier, "int ()")
		.def("getAIStartingDefenseUnits", &CvHandicapInfo::getAIStartingDefenseUnits, "int ()")
		.def("getAIStartingWorkerUnits", &CvHandicapInfo::getAIStartingWorkerUnits, "int ()")
		.def("getAIStartingExploreUnits", &CvHandicapInfo::getAIStartingExploreUnits, "int ()")
		.def("getBarbarianInitialDefenders", &CvHandicapInfo::getBarbarianInitialDefenders, "int ()")
		.def("getAIDeclareWarProb", &CvHandicapInfo::getAIDeclareWarProb, "int ()")
		.def("getAIWorkRateModifier", &CvHandicapInfo::getAIWorkRateModifier, "int ()")
		.def("getAIGrowthPercent", &CvHandicapInfo::getAIGrowthPercent, "int ()")
		.def("getAITrainPercent", &CvHandicapInfo::getAITrainPercent, "int ()")
		.def("getAIWorldTrainPercent", &CvHandicapInfo::getAIWorldTrainPercent, "int ()")
		.def("getAIConstructPercent", &CvHandicapInfo::getAIConstructPercent, "int ()")
		.def("getAIWorldConstructPercent", &CvHandicapInfo::getAIWorldConstructPercent, "int ()")
		.def("getAICreatePercent", &CvHandicapInfo::getAICreatePercent, "int ()")
		.def("getAIWorldCreatePercent", &CvHandicapInfo::getAIWorldCreatePercent, "int ()")
		.def("getAICivicUpkeepPercent", &CvHandicapInfo::getAICivicUpkeepPercent, "int ()")
		.def("getAIUnitCostPercent", &CvHandicapInfo::getAIUnitCostPercent, "int ()")
		.def("getAIUnitSupplyPercent", &CvHandicapInfo::getAIUnitSupplyPercent, "int ()")
		.def("getAIUnitUpgradePercent", &CvHandicapInfo::getAIUnitUpgradePercent, "int ()")
		.def("getAIInflationPercent", &CvHandicapInfo::getAIInflationPercent, "int ()")
		.def("getAIWarWearinessPercent", &CvHandicapInfo::getAIWarWearinessPercent, "int ()")
		.def("getAIPerEraModifier", &CvHandicapInfo::getAIPerEraModifier, "int ()")
		.def("getAIAdvancedStartPercent", &CvHandicapInfo::getAIAdvancedStartPercent, "int ()")
		.def("getNumGoodies", &CvHandicapInfo::getNumGoodies, "int ()")

		// Arrays

		.def("getGoodies", &CvHandicapInfo::getGoodies, "int (int i)")
		.def("isFreeTechs", &CvHandicapInfo::isFreeTechs, "int (int i)")
		.def("isAIFreeTechs", &CvHandicapInfo::isAIFreeTechs, "int (int i)")
		;

	python::class_<CvGameSpeedInfo, python::bases<CvInfoBase> >("CvGameSpeedInfo")
		.def("getGrowthPercent", &CvGameSpeedInfo::getGrowthPercent, "int ()")
		.def("getTrainPercent", &CvGameSpeedInfo::getTrainPercent, "int ()")
		.def("getConstructPercent", &CvGameSpeedInfo::getConstructPercent, "int ()")
		.def("getCreatePercent", &CvGameSpeedInfo::getCreatePercent, "int ()")
		.def("getResearchPercent", &CvGameSpeedInfo::getResearchPercent, "int ()")
		.def("getBuildPercent", &CvGameSpeedInfo::getBuildPercent, "int ()")
		.def("getImprovementPercent", &CvGameSpeedInfo::getImprovementPercent, "int ()")
		.def("getGreatPeoplePercent", &CvGameSpeedInfo::getGreatPeoplePercent, "int ()")
		.def("getAnarchyPercent", &CvGameSpeedInfo::getAnarchyPercent, "int ()")
		.def("getBarbPercent", &CvGameSpeedInfo::getBarbPercent, "int ()")
		.def("getFeatureProductionPercent", &CvGameSpeedInfo::getFeatureProductionPercent, "int ()")
		.def("getUnitDiscoverPercent", &CvGameSpeedInfo::getUnitDiscoverPercent, "int ()")
		.def("getUnitHurryPercent", &CvGameSpeedInfo::getUnitHurryPercent, "int ()")
		.def("getUnitTradePercent", &CvGameSpeedInfo::getUnitTradePercent, "int ()")
		.def("getUnitGreatWorkPercent", &CvGameSpeedInfo::getUnitGreatWorkPercent, "int ()")
		.def("getGoldenAgePercent", &CvGameSpeedInfo::getGoldenAgePercent, "int ()")
		.def("getHurryPercent", &CvGameSpeedInfo::getHurryPercent, "int ()")
		.def("getHurryConscriptAngerPercent", &CvGameSpeedInfo::getHurryConscriptAngerPercent, "int ()")
		.def("getInflationOffset", &CvGameSpeedInfo::getInflationOffset, "int ()")
		.def("getInflationPercent", &CvGameSpeedInfo::getInflationPercent, "int ()")
		.def("getVictoryDelayPercent", &CvGameSpeedInfo::getVictoryDelayPercent, "int ()")
		.def("getNumTurnIncrements", &CvGameSpeedInfo::getNumTurnIncrements, "int ()")

		.def("getGameTurnInfo", &CvGameSpeedInfo::getGameTurnInfo, python::return_value_policy<python::reference_existing_object>(), "GameTurnInfo ()")
		;

	python::class_<CvTurnTimerInfo, python::bases<CvInfoBase> >("CvTurnTimerInfo")
		.def("getBaseTime", &CvTurnTimerInfo::getBaseTime, "int ()")
		.def("getCityBonus", &CvTurnTimerInfo::getCityBonus, "int ()")
		.def("getUnitBonus", &CvTurnTimerInfo::getUnitBonus, "int ()")
		.def("getFirstTurnMultiplier", &CvTurnTimerInfo::getFirstTurnMultiplier, "int ()")
		;

	python::class_<CvBuildInfo, python::bases<CvInfoBase> >("CvBuildInfo")
		.def("getTime", &CvBuildInfo::getTime, "int ()")
		.def("getCost", &CvBuildInfo::getCost, "int ()")
		.def("getTechPrereq", &CvBuildInfo::getTechPrereq, "int ()")
		.def("getImprovement", &CvBuildInfo::getImprovement, "int ()")
		.def("getRoute", &CvBuildInfo::getRoute, "int ()")
		.def("getEntityEvent", &CvBuildInfo::getEntityEvent, "int ()")
		.def("getMissionType", &CvBuildInfo::getMissionType, "int ()")

		.def("isKill", &CvBuildInfo::isKill, "bool ()")

		// Arrays

		.def("getFeatureTech", &CvBuildInfo::getFeatureTech, "int (int i)")
		.def("getFeatureTime", &CvBuildInfo::getFeatureTime, "int (int i)")
		.def("getFeatureProduction", &CvBuildInfo::getFeatureProduction, "int (int i)")

		.def("isFeatureRemove", &CvBuildInfo::isFeatureRemove, "bool (int i)")
		;

	python::class_<CvGoodyInfo, python::bases<CvInfoBase> >("CvGoodyInfo")
		.def("getGold", &CvGoodyInfo::getGold, "int ()")
		.def("getGoldRand1", &CvGoodyInfo::getGoldRand1, "int ()")
		.def("getGoldRand2", &CvGoodyInfo::getGoldRand2, "int ()")
		.def("getMapOffset", &CvGoodyInfo::getMapOffset, "int ()")
		.def("getMapRange", &CvGoodyInfo::getMapRange, "int ()")
		.def("getMapProb", &CvGoodyInfo::getMapProb, "int ()")
		.def("getExperience", &CvGoodyInfo::getExperience, "int ()")
		.def("getHealing", &CvGoodyInfo::getHealing, "int ()")
		.def("getDamagePrereq", &CvGoodyInfo::getDamagePrereq, "int ()")
		.def("getBarbarianUnitProb", &CvGoodyInfo::getBarbarianUnitProb, "int ()")
		.def("getMinBarbarians", &CvGoodyInfo::getMinBarbarians, "int ()")
		.def("getUnitClassType", &CvGoodyInfo::getUnitClassType, "int ()")
		.def("getBarbarianUnitClass", &CvGoodyInfo::getBarbarianUnitClass, "int ()")

		.def("isTech", &CvGoodyInfo::isTech, "bool ()")
		.def("isBad", &CvGoodyInfo::isBad, "bool ()")

		.def("getSound", &CvGoodyInfo::getSound, "string ()")
		;

	python::class_<CvRouteInfo, python::bases<CvInfoBase> >("CvRouteInfo")
		.def("getValue", &CvRouteInfo::getValue, "int ()")
		.def("getMovementCost", &CvRouteInfo::getMovementCost, "int ()")
		.def("getFlatMovementCost", &CvRouteInfo::getFlatMovementCost, "int ()")
		.def("getPrereqBonus", &CvRouteInfo::getPrereqBonus, "int ()")

		// Arrays

		.def("getYieldChange", &CvRouteInfo::getYieldChange, "int (int i)")
		.def("getTechMovementChange", &CvRouteInfo::getTechMovementChange, "int (int i)")
		.def("getPrereqOrBonus", &CvRouteInfo::getPrereqOrBonus, "int (int i)")
		;

	python::class_<CvImprovementBonusInfo, python::bases<CvInfoBase> >("CvImprovementBonusInfo")
		.def("getDiscoverRand", &CvImprovementBonusInfo::getDiscoverRand, "int ()")

		.def("isBonusMakesValid", &CvImprovementBonusInfo::isBonusMakesValid, "bool ()")
		.def("isBonusTrade", &CvImprovementBonusInfo::isBonusTrade, "bool ()")

		// Arrays

		.def("getYieldChange", &CvImprovementBonusInfo::getYieldChange, "int (int i)")
		;

	python::class_<CvImprovementInfo, python::bases<CvInfoBase> >("CvImprovementInfo")

		.def("getTilesPerGoody", &CvImprovementInfo::getTilesPerGoody, "int ()")
		.def("getGoodyUniqueRange", &CvImprovementInfo::getGoodyUniqueRange, "int ()")
		.def("getFeatureGrowthProbability", &CvImprovementInfo::getFeatureGrowthProbability, "int ()")
		.def("getUpgradeTime", &CvImprovementInfo::getUpgradeTime, "int ()")
		.def("getAirBombDefense", &CvImprovementInfo::getAirBombDefense, "int ()")
		.def("getDefenseModifier", &CvImprovementInfo::getDefenseModifier, "int ()")
		.def("getHappiness", &CvImprovementInfo::getDefenseModifier, "int ()")
		.def("getPillageGold", &CvImprovementInfo::getPillageGold, "int ()")
		.def("getImprovementPillage", &CvImprovementInfo::getImprovementPillage, "int ()")
		.def("getImprovementUpgrade", &CvImprovementInfo::getImprovementUpgrade, "int ()")

		.def("isActsAsCity", &CvImprovementInfo::isActsAsCity, "bool ()")
		.def("isHillsMakesValid", &CvImprovementInfo::isHillsMakesValid, "bool ()")
		.def("isFreshWaterMakesValid", &CvImprovementInfo::isFreshWaterMakesValid, "bool ()")
		.def("isRiverSideMakesValid", &CvImprovementInfo::isRiverSideMakesValid, "bool ()")
		.def("isNoFreshWater", &CvImprovementInfo::isNoFreshWater, "bool ()")
		.def("isRequiresFlatlands", &CvImprovementInfo::isRequiresFlatlands, "bool ()")
		.def("isRequiresRiverSide", &CvImprovementInfo::isRequiresRiverSide, "bool ()")
		.def("isRequiresIrrigation", &CvImprovementInfo::isRequiresIrrigation, "bool ()")
		.def("isCarriesIrrigation", &CvImprovementInfo::isCarriesIrrigation, "bool ()")
		.def("isRequiresFeature", &CvImprovementInfo::isRequiresFeature, "bool ()")
		.def("isWater", &CvImprovementInfo::isWater, "bool ()")
		.def("isGoody", &CvImprovementInfo::isGoody, "bool ()")
		.def("isPermanent", &CvImprovementInfo::isPermanent, "bool ()")
		.def("isOutsideBorders", &CvImprovementInfo::isOutsideBorders, "bool ()")

		.def("getArtDefineTag", &CvImprovementInfo::getArtDefineTag, "string ()")

		// Arrays

		.def("getPrereqNatureYield", &CvImprovementInfo::getPrereqNatureYield, "int (int i)")
		.def("getYieldChange", &CvImprovementInfo::getYieldChange, "int (int i)")
		.def("getRiverSideYieldChange", &CvImprovementInfo::getRiverSideYieldChange, "int (int i)")
		.def("getHillsYieldChange", &CvImprovementInfo::getHillsYieldChange, "int (int i)")
		.def("getIrrigatedYieldChange", &CvImprovementInfo::getIrrigatedYieldChange, "int (int i)")

		.def("getTerrainMakesValid", &CvImprovementInfo::getTerrainMakesValid, "bool (int i)")
		.def("getFeatureMakesValid", &CvImprovementInfo::getFeatureMakesValid, "bool (int i)")

		.def("getImprovementBonusYield", &CvImprovementInfo::getImprovementBonusYield, "int (int i, int j)")
		.def("isImprovementBonusMakesValid", &CvImprovementInfo::isImprovementBonusMakesValid, "bool (int i)")
		.def("isImprovementBonusTrade", &CvImprovementInfo::isImprovementBonusTrade, "bool (int i)")
		.def("getImprovementBonusDiscoverRand", &CvImprovementInfo::getImprovementBonusDiscoverRand, "int (int i)")

		.def("getTechYieldChanges", &CvImprovementInfo::getTechYieldChanges, "int (int i, int j)")
		.def("getRouteYieldChanges", &CvImprovementInfo::getRouteYieldChanges, "int (int i, int j)")
		;

	python::class_<CvBonusClassInfo, python::bases<CvInfoBase> >("CvBonusClassInfo")
		.def("getUniqueRange", &CvBonusClassInfo::getUniqueRange)
		;

	python::class_<CvBonusInfo, python::bases<CvInfoBase> >("CvBonusInfo")

		.def("getChar", &CvBonusInfo::getChar, "int ()")
		.def("getTechReveal", &CvBonusInfo::getTechReveal, "int ()")
		.def("getTechCityTrade", &CvBonusInfo::getTechCityTrade, "int ()")
		.def("getTechObsolete", &CvBonusInfo::getTechObsolete, "int ()")
		.def("getAITradeModifier", &CvBonusInfo::getAITradeModifier, "int ()")
		.def("getAIObjective", &CvBonusInfo::getAIObjective, "int ()")
		.def("getHealth", &CvBonusInfo::getHealth, "int ()")
		.def("getHappiness", &CvBonusInfo::getHappiness, "int ()")
		.def("getMinAreaSize", &CvBonusInfo::getMinAreaSize, "int ()")
		.def("getMinLatitude", &CvBonusInfo::getMinLatitude, "int ()")
		.def("getMaxLatitude", &CvBonusInfo::getMaxLatitude, "int ()")
		.def("getPlacementOrder", &CvBonusInfo::getPlacementOrder, "int ()")
		.def("getConstAppearance", &CvBonusInfo::getConstAppearance, "int ()")
		.def("getRandAppearance1", &CvBonusInfo::getRandAppearance1, "int ()")
		.def("getRandAppearance2", &CvBonusInfo::getRandAppearance2, "int ()")
		.def("getRandAppearance3", &CvBonusInfo::getRandAppearance3, "int ()")
		.def("getRandAppearance4", &CvBonusInfo::getRandAppearance4, "int ()")
		.def("getPercentPerPlayer", &CvBonusInfo::getPercentPerPlayer, "int ()")
		.def("getTilesPer", &CvBonusInfo::getTilesPer, "int ()")
		.def("getMinLandPercent", &CvBonusInfo::getMinLandPercent, "int ()")
		.def("getUniqueRange", &CvBonusInfo::getUniqueRange, "int ()")
		.def("getGroupRange", &CvBonusInfo::getGroupRange, "int ()")
		.def("getGroupRand", &CvBonusInfo::getGroupRand, "int ()")
		.def("getBonusClassType", &CvBonusInfo::getBonusClassType, "int ()")

		.def("isOneArea", &CvBonusInfo::isOneArea, "bool ()")
		.def("isHills", &CvBonusInfo::isHills, "bool ()")
		.def("isFlatlands", &CvBonusInfo::isFlatlands, "bool ()")
		.def("isNoRiverSide", &CvBonusInfo::isNoRiverSide, "bool ()")
		.def("isNormalize", &CvBonusInfo::isNormalize, "bool ()")

		.def("getArtDefineTag", &CvBonusInfo::getArtDefineTag, "string ()")

		// Arrays

		.def("getYieldChange", &CvBonusInfo::getYieldChange, "int (int i)")

		.def("isTerrain", &CvBonusInfo::isTerrain, "bool (int i)")
		.def("isFeature", &CvBonusInfo::isFeature, "bool (int i)")
		.def("isFeatureTerrain", &CvBonusInfo::isFeatureTerrain, "bool (int i)")

		.def("getButton", &CvBonusInfo::getButton, "string ()")
		.def("getArtInfo", &CvBonusInfo::getArtInfo,  python::return_value_policy<python::reference_existing_object>(), "CvArtInfoBonus ()")
		;

	python::class_<CvFeatureInfo, python::bases<CvInfoBase> >("CvFeatureInfo")

		.def("getMovementCost", &CvFeatureInfo::getMovementCost, "int ()")
		.def("getSeeThroughChange", &CvFeatureInfo::getSeeThroughChange, "int ()")
		.def("getHealthPercent", &CvFeatureInfo::getHealthPercent, "int ()")
		.def("getAppearanceProbability", &CvFeatureInfo::getAppearanceProbability, "int ()")
		.def("getDisappearanceProbability", &CvFeatureInfo::getDisappearanceProbability, "int ()")
		.def("getGrowthProbability", &CvFeatureInfo::getGrowthProbability, "int ()")
		.def("getDefenseModifier", &CvFeatureInfo::getDefenseModifier, "int ()")
		.def("getAdvancedStartRemoveCost", &CvFeatureInfo::getAdvancedStartRemoveCost, "int ()")
		.def("getTurnDamage", &CvFeatureInfo::getTurnDamage, "int ()")
		
		.def("isNoCoast", &CvFeatureInfo::isNoCoast, "bool ()")
		.def("isNoRiver", &CvFeatureInfo::isNoRiver, "bool ()")
		.def("isNoAdjacent", &CvFeatureInfo::isNoAdjacent, "bool ()")
		.def("isRequiresFlatlands", &CvFeatureInfo::isRequiresFlatlands, "bool ()")
		.def("isRequiresRiver", &CvFeatureInfo::isRequiresRiver, "bool ()")
		.def("isAddsFreshWater", &CvFeatureInfo::isAddsFreshWater, "bool ()")
		.def("isImpassable", &CvFeatureInfo::isImpassable, "bool ()")
		.def("isNoCity", &CvFeatureInfo::isNoCity, "bool ()")
		.def("isNoImprovement", &CvFeatureInfo::isNoImprovement, "bool ()")
		.def("isVisibleAlways", &CvFeatureInfo::isVisibleAlways, "bool ()")
		.def("isNukeImmune", &CvFeatureInfo::isNukeImmune, "bool ()")

		// Arrays

		.def("getYieldChange", &CvFeatureInfo::getYieldChange, "int (int i)")
		.def("getRiverYieldChange", &CvFeatureInfo::getRiverYieldChange, "int (int i)")
		.def("getHillsYieldChange", &CvFeatureInfo::getHillsYieldChange, "int (int i)")

		.def("isTerrain", &CvFeatureInfo::isTerrain, "bool (int i)")
		.def("getNumVarieties", &CvFeatureInfo::getNumVarieties, "int ()")
		;

	python::class_<CvCommerceInfo, python::bases<CvInfoBase> >("CvCommerceInfo")
		.def("getChar", &CvCommerceInfo::getChar, "int ()")
		.def("getInitialPercent", &CvCommerceInfo::getInitialPercent, "int ()")
		.def("getInitialHappiness", &CvCommerceInfo::getInitialHappiness, "int ()")
		.def("getAIWeightPercent", &CvCommerceInfo::getAIWeightPercent, "int ()")

		.def("isFlexiblePercent", &CvCommerceInfo::isFlexiblePercent, "bool ()")
		;
}
