#pragma once

/**********************************************************************

File:		CvBugOptions.h
Author:		EmperorFool
Created:	2009-01-21

Calls out to the CvAppInterface Python module to check user options.

		Copyright (c) 2009 The BUG Mod. All rights reserved.

**********************************************************************/

#ifndef BUG_OPTIONS_H
#define BUG_OPTIONS_H

// Must use existing module because the DLL cannot see new modules in CustomAssets
#define PYBugOptionsModule PYCivModule

// Text prepended to option name if no XML key given
// advc: unused
//#define OPTION_XML_PREFIX "BULL__"

// advc: No implementation for these
/*void logMsg(const char* format, ...);
bool isBug();
void setIsBug(bool bIsBug);*/
// advc.003t: Replaced by functions in CvGlobals
/*bool getDefineBOOL(const char* xmlKey, bool bDefault = false);
int getDefineINT(const char* xmlKey, int iDefault = 0);*/

namespace BUGOption // advc: Functions renamed from getBugOptionBOOL/INT
{
	/*  szOptionId is e.g. "MainInterface__RapidUnitCycling"
		That is: The id of the enclosing option tag, two underscores and the id of
		the proper (inner) option tag. */
	/*  advc: Removed unused param char const* xmlKey = NULL
		bWarn added */
	bool isEnabled(const char* szOptionId, bool bDefault = true, bool bWarn = true);
	/*  For options with a list of choice strings, the returned number indicates
		the position of the selected choice starting at 0 for the topmost choice.
		That means, if the choices are reordered in the config file, the C++ code
		needs to be adapted. */
	int getValue(const char* szOptionId, int iDefault = 0, bool bWarn = true);
	CvString userDirPath(); // advc.003d
};

#endif
