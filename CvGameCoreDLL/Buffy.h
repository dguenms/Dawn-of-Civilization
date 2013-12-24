/**********************************************************************

File:		Buffy.h
Author:		EmperorFool
Created:	2010-01-23

Defines common constants and functions for use throughout BUFFY.

		Copyright (c) 2010 The BUG Mod. All rights reserved.

**********************************************************************/

#pragma once

#ifndef BUFFY_H
#define BUFFY_H

// name of the Python module where all the BUFFY functions that the DLL calls must live
// MUST BE A BUILT-IN MODULE IN THE ENTRYPOINTS FOLDER
// currently CvAppInterface
#define PYBuffyModule			PYCivModule

// Increment this by 1 each time you commit new/changed functions in the Python API.
#define BUFFY_DLL_API_VERSION		1

// Used to signal the BULL saved game format is used
#define BUFFY_DLL_SAVE_FORMAT		64

// These are display-only values; the version and build should be changed for each release.
#define BUFFY_DLL_NAME			L"BUFFY"
#define BUFFY_DLL_VERSION		L"3.19.003"
#define BUFFY_DLL_BUILD			L"100"

#endif
