#include "CvGameCoreDLL.h"
#include "CyMapGenerator.h"
//#include "CvStructs.h"
//# include <boost/python/manage_new_object.hpp>
//# include <boost/python/return_value_policy.hpp>

//
// published python interface for CyMapGenerator
//

void CyMapGeneratorPythonInterface()
{
	OutputDebugString("Python Extension Module - CyMapGeneratorPythonInterface\n");

	python::class_<CyMapGenerator>("CyMapGenerator")
		.def("isNone", &CyMapGenerator::isNone, "bool () - valid CyMapGenerator() interface")

		.def("canPlaceBonusAt", &CyMapGenerator::canPlaceBonusAt, "bool (int /*BonusTypes*/ eBonus, int iX, int iY, bool bIgnoreLatitude)")
		.def("canPlaceGoodyAt", &CyMapGenerator::canPlaceGoodyAt, "bool (int /*ImprovementTypes*/ eImprovement, int iX, int iY)")

		.def("addGameElements", &CyMapGenerator::addGameElements, "void ()")

		.def("addLakes", &CyMapGenerator::addLakes, "void ()")
		.def("addRivers", &CyMapGenerator::addRivers, "void ()")
		.def("doRiver", &CyMapGenerator::doRiver, "void (CyPlot* pStartPlot, int /*CardinalDirectionTypes*/ eCardinalDirection)")
		.def("addFeatures", &CyMapGenerator::addFeatures, "void ()")
		.def("addBonuses", &CyMapGenerator::addBonuses, "void ()")
		.def("addUniqueBonusType", &CyMapGenerator::addUniqueBonusType, "void (int /*BonusTypes*/ eBonusType)")
		.def("addNonUniqueBonusType", &CyMapGenerator::addNonUniqueBonusType, "void (int /*BonusTypes*/ eBonusType)")
		.def("addGoodies", &CyMapGenerator::addGoodies, "void ()")

		.def("eraseRivers", &CyMapGenerator::eraseRivers, "void ()")
		.def("eraseFeatures", &CyMapGenerator::eraseFeatures, "void ()")
		.def("eraseBonuses", &CyMapGenerator::eraseBonuses, "void ()")
		.def("eraseGoodies", &CyMapGenerator::eraseGoodies, "void ()")

		.def("generateRandomMap", &CyMapGenerator::generateRandomMap, "void ()")

		.def("generatePlotTypes", &CyMapGenerator::generatePlotTypes, "void ()")
		.def("generateTerrain", &CyMapGenerator::generateTerrain, "void ()")

		.def("afterGeneration", &CyMapGenerator::afterGeneration, "void ()")

		.def("setPlotTypes", &CyMapGenerator::setPlotTypes, "void (list lPlotTypes) - set plot types to the contents of the given list")
		;
}
