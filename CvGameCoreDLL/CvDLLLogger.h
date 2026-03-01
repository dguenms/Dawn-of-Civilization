#pragma once

#ifndef CV_DLL_LOGGER_H
#define CV_DLL_LOGGER_H

/*  advc: New class. Encapsulates calls to messageControlLog (CvDLLUtilityIFaceBase).
	The log is enabled through "MessageLog" in CivilizationIV.ini. "LoggingEnabled"
	doesn't matter -- and this probably can't be changed b/c the DLL can't check if
	LoggingEnabled is set. (CvGlobals::m_bLogging only says whether MessageLog is set.) */
class CvDLLLogger : private boost::noncopyable
{
public:
	CvDLLLogger(bool bEnabled, bool bRandEnabled);
	// Requires "RandLog" to be set in addition to "MessageLog"
	void logRandomNumber(const TCHAR* szMsg, unsigned short usNum, unsigned int uiSeed,
			int iData1, int iData2, /* advc.007b: */ CvString const* pszFileName = NULL);
	void logTurnActive(PlayerTypes ePlayer);
	void logCityBuilt(CvCity const& kCity);
	void logCombat(CvUnit const& kAttacker, CvUnit const& kDefender);
	void logUnitStuck(CvUnit const& kUnit);
	void logMapStats(bool bAfterNormalization = false); // advc.mapstat
	void logCivLeaders(); // advc.tsl

private:
	bool m_bEnabled;
	bool m_bRandEnabled;

	/*	Generally, the public log... functions should handle the is-enabled checks,
		but, for CvRandom, I'd like to avoid the overhead of calling a non-inline
		function when the RandLog is disabled. */
	friend class CvRandom;

	bool isEnabled() const
	{
		return m_bEnabled;
	}
	bool isEnabledRand() const
	{
		return m_bRandEnabled;
	}
};

#endif
