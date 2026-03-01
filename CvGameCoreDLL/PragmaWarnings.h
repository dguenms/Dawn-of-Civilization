#pragma once

#ifndef PRAGMA_WARNINGS_H
#define PRAGMA_WARNINGS_H

/*	advc.make: Header for custom compiler warnings through pragma.
	(I'm using a shorthand that allows subtracting 4000 from warning numbers;
	e.g. 251 corresponds to c4251 in compiler output and documentation.)
	BtS had disabled numbers 251 (redundantly in several headers),
	100 (through CvDLLEntityIFaceBase.h) and 127 (through CvInfo.h).
	I'm not sure if it was necessary to disable those explicitly in BtS,
	but I do need to disable them now b/c of the /W4 compiler option.
	I'm not disabling number 530 ("C++ exception handler used,
	but unwind semantics are not enabled") b/c I'm not getting any such
	warnings. BtS had disabled that one through the PCH. */

/*	These should remain enabled even if the global level is dialed back down to 3.
	But I'm not sure how disable them in the std headers etc.
	May need to put them into a separate header for that, to be included in the PCH
	after loading the non-conforming headers. */
/*
// "there is no warning with number..."
#pragma warning(3: 619)

// "local variable may be used without having been initialized"
#pragma warning(3: 701)

// "conversion from signed to unsigned"
#pragma warning(3: 245)

#ifndef _DEBUG
	// "local variable is initialized but not referenced"
	#pragma warning(3: 189)
#endif
// "type conversion - possible loss of data"
#pragma warning(3: 244) // (disabled locally in CvPlot.cpp, FDialogTemplate.cpp)
*/

/*	Level 4 warnings that are too strict ...
	(at least for day-to-day builds) */

#pragma warning(disable: 100) // "unreferenced formal parameter"
#pragma warning(disable: 127) // "conditional expression is constant"
#pragma warning(disable: 702) // "unreachable code"

/*	"operator signed/unsigned mismatch"
	This is only for operator== as far as I can tell.
	c4018 (level 3) is still enabled for other (more hazardous) comparisons. */
#pragma warning(disable: 389)

/*	"... needs to have dll-interface to be used by clients of struct"
	Prevents exporting of entire structs. */
#pragma warning(disable: 251)

/*	"implicit conversion to bool"
	Need those conversions in logic involving bit masks. */
#pragma warning(disable: 800)

/*	"assignment operator could not be generated"
	Don't want to be forced to make every class with reference members
	explicitly noncopyable. */
#pragma warning(disable: 512)

/*	"copy constructor could not be generated"
	Gets in the way of deriving base classes from boost::noncopyable. */
#pragma warning(disable: 511)

/*	"assignment within conditional expression"
	A little annoying, but rarely so; perhaps worth having. */
//#pragma warning(disable: 706)

/*	"local variable is initialized but not referenced"
	Helpful, but still want to be able to define variables
	temporarily just for inspecting them in the debugger. */
#ifdef _DEBUG
	#pragma warning(disable: 189)
#endif


/*	The 'suppress' warning specifier was introduced in MSVC05. I guess this is the
	best that we can do:
	^Nope, in header files, this crashes fastdep.exe. Will have to spell it out. */
/*#define PRAGMA_SUPPRESS_START(iWarningType) \
	__pragma(warning(push)) \
	__pragma(warning(disable: iWarningType))
#define PRAGMA_SUPPRESS_END \
	__pragma(warning(pop))*/

#endif
