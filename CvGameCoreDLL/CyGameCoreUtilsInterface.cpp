#pragma component (mintypeinfo, on)

#include "CvGameCoreDLL.h"
#include "CyGameCoreUtils.h"
#include "CyPlot.h"
#include "CyCity.h"
#include "CyUnit.h"

//
// Python interface for CvgameCoreUtils.h.
//

void CyGameCoreUtilsPythonInterface()
{
	OutputDebugString("Python Extension Module - CyGameCoreUtilsPythonInterface\n");

	python::def("cyIntRange", cyIntRange,"int (int iNum, int iLow, int iHigh)");
	python::def("cyFloatRange", cyFloatRange,"float (float fNum, float fLow, float fHigh)");
	python::def("dxWrap", cyDxWrap,"int (int iDX)");
	python::def("dyWrap", cyDyWrap,"int (int iDY)");
	python::def("plotDistance", cyPlotDistance,"int (int iX1, int iY1, int iX2, int iY2)");
	python::def("stepDistance", cyStepDistance,"int (int iX1, int iY1, int iX2, int iY2)");
	python::def("plotDirection", cyPlotDirection, python::return_value_policy<python::manage_new_object>(), "CyPlot* (int iX, int iY, DirectionTypes eDirection)");
	python::def("plotCardinalDirection", cyPlotCardinalDirection, python::return_value_policy<python::manage_new_object>(), "CyPlot* (int iX, int iY, CardinalDirectionTypes eCardDirection)");
	python::def("splotCardinalDirection", cysPlotCardinalDirection, python::return_value_policy<python::reference_existing_object>(), "CyPlot* (int iX, int iY, CardinalDirectionTypes eCardDirection)");
	python::def("plotXY", cyPlotXY, python::return_value_policy<python::manage_new_object>(), "CyPlot* (int iX, int iY, int iDX, int iDY)");
	python::def("splotXY", cysPlotXY, python::return_value_policy<python::reference_existing_object>(), "CyPlot* (int iX, int iY, int iDX, int iDY)");
	python::def("directionXY", cyDirectionXYFromInt,"DirectionTypes (int iDX, int iDY)");
	python::def("directionXYFromPlot", cyDirectionXYFromPlot,"DirectionTypes (CyPlot* pFromPlot, CyPlot* pToPlot)");
	python::def("plotCity", cyPlotCity, python::return_value_policy<python::manage_new_object>(), "CyPlot* (int iX, int iY, int iIndex)");
	python::def("plotCityXY", cyPlotCityXYFromInt,"int (int iDX, int iDY)");
	python::def("plotCityXYFromCity", cyPlotCityXYFromCity,"int (CyCity* pCity, CyPlot* pPlot)");
	python::def("getOppositeCardinalDirection", cyGetOppositeCardinalDirection,"CardinalDirectionTypes (CardinalDirectionTypes eDir)");
	python::def("cardinalDirectionToDirection", cyCardinalDirectionToDirection, "DirectionTypes (CardinalDirectionTypes eDir) - converts a CardinalDirectionType to the corresponding DirectionType");

	python::def("isCardinalDirection", cyIsCardinalDirection,"bool (DirectionTypes eDirection)");
	python::def("estimateDirection", cyEstimateDirection, "DirectionTypes (int iDX, int iDY)");

	python::def("atWar", cyAtWar,"bool (int eTeamA, int eTeamB)");
	python::def("isPotentialEnemy", cyIsPotentialEnemy,"bool (int eOurTeam, int eTheirTeam)");

	python::def("getCity", cyGetCity, python::return_value_policy<python::manage_new_object>(), "CyPlot* (IDInfo city)");
	python::def("getUnit", cyGetUnit, python::return_value_policy<python::manage_new_object>(), "CyUnit* (IDInfo unit)");

	python::def("isPromotionValid", cyIsPromotionValid, "bool (int /*PromotionTypes*/ ePromotion, int /*UnitTypes*/ eUnit, bool bLeader)");
	python::def("getPopulationAsset", cyGetPopulationAsset, "int (int iPopulation)");
	python::def("getLandPlotsAsset", cyGetLandPlotsAsset, "int (int iLandPlots)");
	python::def("getPopulationPower", cyGetPopulationPower, "int (int iPopulation)");
	python::def("getPopulationScore", cyGetPopulationScore, "int (int iPopulation)");
	python::def("getLandPlotsScore", cyGetLandPlotsScore, "int (int iPopulation)");
	python::def("getTechScore", cyGetTechScore, "int (int /*TechTypes*/ eTech)");
	python::def("getWonderScore", cyGetWonderScore, "int (int /*BuildingClassTypes*/ eWonderClass)");
	python::def("finalImprovementUpgrade", cyFinalImprovementUpgrade, "int /*ImprovementTypes*/ (int /*ImprovementTypes*/ eImprovement, int iCount)");

	python::def("getWorldSizeMaxConscript", cyGetWorldSizeMaxConscript, "int (int /*CivicTypes*/ eCivic)");
	python::def("isReligionTech", cyIsReligionTech, "int (int /*TechTypes*/ eTech)");

	python::def("isTechRequiredForUnit", cyIsTechRequiredForUnit, "bool (int /*TechTypes*/ eTech, int /*UnitTypes*/ eUnit)");
	python::def("isTechRequiredForBuilding", cyIsTechRequiredForBuilding, "bool (int /*TechTypes*/ eTech, int /*BuildingTypes*/ eBuilding)");
	python::def("isTechRequiredForProject", cyIsTechRequiredForProject, "bool (int /*TechTypes*/ eTech, int /*ProjectTypes*/ eProject)");
	python::def("isWorldUnitClass", cyIsWorldUnitClass, "bool (int /*UnitClassTypes*/ eUnitClass)");
	python::def("isTeamUnitClass", cyIsTeamUnitClass, "bool (int /*UnitClassTypes*/ eUnitClass)");
	python::def("isNationalUnitClass", cyIsNationalUnitClass, "bool (int /*UnitClassTypes*/ eUnitClass)");
	python::def("isLimitedUnitClass", cyIsLimitedUnitClass, "bool (int /*UnitClassTypes*/ eUnitClass)");
	python::def("isWorldWonderClass", cyIsWorldWonderClass, "bool (int /*BuildingClassTypes*/ eBuildingClass)");
	python::def("isTeamWonderClass", cyIsTeamWonderClass, "bool (int /*BuildingClassTypes*/ eBuildingClass)");
	python::def("isNationalWonderClass", cyIsNationalWonderClass, "bool (int /*BuildingClassTypes*/ eBuildingClass)");
	python::def("isLimitedWonderClass", cyIsLimitedWonderClass, "bool (int /*BuildingClassTypes*/ eBuildingClass)");
	python::def("isWorldProject", cyIsWorldProject, "bool (int /*ProjectTypes*/ eProject)");
	python::def("isTeamProject", cyIsTeamProject, "bool (int /*ProjectTypes*/ eProject)");
	python::def("isLimitedProject", cyIsLimitedProject, "bool (int /*ProjectTypes*/ eProject)");
	python::def("getCombatOdds", cyGetCombatOdds, "int (CyUnit* pAttacker, CyUnit* pDefender)");
	python::def("getEspionageModifier", cyGetEspionageModifier, "int (int /*TeamTypes*/ iOurTeam, int /*TeamTypes*/ iTargetTeam)");

// BUG - Unit Experience - start
	python::def("calculateExperience", cyCalculateExperience, "int (int iLevel, int /*PlayerTypes*/ iPlayer)");
	python::def("calculateLevel", cyCalculateLevel, "int (int iExperience, int /*PlayerTypes*/ iPlayer)");
// BUG - Unit Experience - end
	
	// edead: start
	python::def("getTurnForYear", cyGetTurnForYear, "int (int iTurnYear)");
	python::def("getGameTurnForYear", cyGetGameTurnForYear, "int (int iTurnYear, int iStartYear, int /*CalendarTypes*/ eCalendar, int /*GameSpeedTypes*/ eSpeed)");
	python::def("getGameTurnForMonth", cyGetGameTurnForMonth, "int (int iTurnMonth, int iStartYear, int /*CalendarTypes*/ eCalendar, int /*GameSpeedTypes*/ eSpeed)");
	python::def("getTurnYearForGame", cyGetTurnYearForGame, "int (int iGameTurn, int iStartYear, int /*CalendarTypes*/ eCalendar, int /*GameSpeedTypes*/ eSpeed)");
	python::def("getTurnMonthForGame", cyGetTurnMonthForGame, "int (int iGameTurn, int iStartYear, int /*CalendarTypes*/ eCalendar, int /*GameSpeedTypes*/ eSpeed)");
	// edead: end

	python::def("getSettlerValue", cyGetSettlerValue, "int (int iPlayer, int x, int y)");
	python::def("log", cyLog, "void (string logfile, string message)");
	python::def("setDirty", cySetDirty, "void (int iDirtyBit, bool bNewValue)");
}
