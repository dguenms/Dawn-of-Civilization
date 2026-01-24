#include "CvGameCoreDLL.h"

using namespace boost::python;

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(CvRandom_get_overloads, CvRandom::get, 2, 2)

//
// published python interface for CvRandom
//
void CyRandomPythonInterface()
{
	printToConsole("Python Extension Module - CyRandomPythonInterface\n");

	python::class_<CvRandom>("CyRandom")
		.def("get", &CvRandom::get, CvRandom_get_overloads( args("usNum", "pszLog"), "returns a random number"))
		// kekm.27:
		.def("getSeed", &CvRandom::getSeed,  "int () current seed")
		.def("init", &CvRandom::init, "void (unsigned long int ulSeed)")
		;
}
