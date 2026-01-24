#pragma once

#ifndef CY_INFO_WRAPPER_H
#define CY_INFO_WRAPPER_H

/*  advc.003x: Macros for defining Python wrappers (adapters) for member functions
	of CvInfo classes. Specifically for functions that take an enum type parameter
	and therefore can't (or shouldn't) be directly exposed to Python.
	The PY_WRAP macro can be placed right after the declaration of a public CvInfo
	member function. It defines an in-line wrapper with private accessibility.
	A pointer to the wrapper needs to be inserted into the proper .def call in
	CyInfoInterface[1-4].cpp. That's just a matter of prepending 'py_' to the existing
	call argument.

	Additionally, the CvInfo class needs to declare the global
	CyInfoPythonInterface[1-4] function that contains the def call as a friend.
	^Actually, let's just insert that into the macro; redundant declarations do no harm.

	For convenience, there are macros that take fewer parameters:
	iPY_WRAP: Takes the name of an XML tag and prepends "get" to generate the
			function name. Return type is 'int'.
	bPY_WRAP: Prepends "is", return type is 'bool'. */

#define FRIEND_CY_INFO_PYTHON_INTERFACE \
	friend void CyInfoPythonInterface1(); \
	friend void CyInfoPythonInterface2(); \
	friend void CyInfoPythonInterface3(); \
	friend void CyInfoPythonInterface4()

#define PY_WRAP(ReturnType, fnName, enumName) \
	private: \
		FRIEND_CY_INFO_PYTHON_INTERFACE; \
		ReturnType py_##fnName(int i) const \
		{ \
			return fnName((enumName##Types)i); \
		} \
	public:

#define iPY_WRAP(tagName, enumName) PY_WRAP(int, get##tagName, enumName)
#define bPY_WRAP(tagName, enumName) PY_WRAP(bool, is##tagName, enumName)

#define PY_WRAP_2D(ReturnType, fnName, firstEnumName, secondEnumName) \
	private: \
		FRIEND_CY_INFO_PYTHON_INTERFACE; \
		ReturnType py_##fnName(int iFirst, int iSecond) const \
		{ \
			return fnName( \
					(firstEnumName##Types)iFirst, \
					(secondEnumName##Types)iSecond); \
		} \
	public:

#endif
