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
#define OPTION_XML_PREFIX "BULL__"

void logMsg(const char* format, ...);

bool isBug();
void setIsBug(bool bIsBug);

bool getDefineBOOL(const char* xmlKey, bool bDefault = false);
int getDefineINT(const char* xmlKey, int iDefault = 0);

bool getBugOptionBOOL(const char* id, bool bDefault = true, const char* xmlKey = NULL);
int getBugOptionINT(const char* id, int iDefault = 0, const char* xmlKey = NULL);

#endif
