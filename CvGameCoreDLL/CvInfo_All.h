#pragma once

#ifndef CV_INFO_ALL_H
#define CV_INFO_ALL_H

/*  advc.003x: Wrapper; intended for the XML loading classes that need to deal with
	all types of info objects. */

/*  I'm not including anything that is already in CvGameCoreDLL.h - that header
	should always be included before this one. */
#include "CvInfo_City.h" // Another wrapper
#include "CvInfo_GameOption.h"
#include "CvInfo_Terrain.h"
#include "CvInfo_Command.h"
#include "CvInfo_Civics.h"
#include "CvInfo_TrueStarts.h" // advc.tsl
#include "CvInfo_Misc.h"
// Note: CvPopupInfo, CvReplayInfo and CvHallOfFameInfo don't belong here; contain no XML data.

#endif
