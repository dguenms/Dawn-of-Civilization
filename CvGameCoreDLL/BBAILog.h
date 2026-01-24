#pragma once

#ifndef BBAI_LOG_H
#define BBAI_LOG_H

// AI decision making logging

// advc: Uncomment to enable BBAI logging
//#define LOG_AI
// Log levels:
// 0 - None
// 1 - Important decisions only
// 2 - Many decisions
// 3 - All logging
#ifdef LOG_AI
#define gLogBBAI true // advc.007: So that LOG_AI can be checked in FAssert
#define gPlayerLogLevel		3
#define gScoreLogInterval	100 // advc.007: was hardcoded to 25 in CvPlayer::onTurnLogging
#define gTeamLogLevel		3
#define gCityLogLevel		3
#define gUnitLogLevel		3
#define gMapLogLevel		3 // K-Mod
#define gDealCancelLogLevel 1 // advc.133
#else
#define gLogBBAI false // advc.007
#define gPlayerLogLevel		0
#define gScoreLogInterval	10000
#define gTeamLogLevel		0
#define gCityLogLevel		0
#define gUnitLogLevel		0
#define gMapLogLevel		0 // K-Mod
#define gDealCancelLogLevel 0 // advc.133
#endif

// <advc.031c>
//#define LOG_FOUND_VALUE
#ifdef LOG_FOUND_VALUE
#define LOG_AI
#define gFoundLogLevel 1
#undef gMapLogLevel
#define gMapLogLevel 1 // (for starting site normalization)
#else
#define gFoundLogLevel 0
#endif // </advc.031c>

void logBBAI(TCHAR* format, ... );
// <advc.133>
class CvDeal;
void logBBAICancel(CvDeal const& d, PlayerTypes eCancelPlayer, wchar const* szReason);
// </advc.133>

#endif  //BBAI_LOG_H
