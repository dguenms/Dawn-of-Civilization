#pragma once

#ifndef UWAI_REPORT_H
#define UWAI_REPORT_H

#include "UWAI.h"

/* advc.104: New class. A report about the war planning of a single team
   (cf. UWAI::Team::doWar). Also some string handling.
   Calls to 'log' have no effect when in silent or mute mode.
   However, DEBUG mode is not a prerequisite for logging output,
   meaning also that logging through this class isn't completely "free"
   in terms of overhead in release builds. There's a compile-time flag
   in UWAI.h, however, that should pretty much eliminate the overhead.
   Each 'log' call is written to the log file separately (flushed). */
class UWAIReport
{
public:
	explicit UWAIReport(bool bSilent = false);
	~UWAIReport();
	// No effect when set to silent or mute
	void log(char const* fmt, ...)
	#if DISABLE_UWAI_REPORT
		{}
	#else
		;
	#endif
	void logNewline()
	#if DISABLE_UWAI_REPORT
		{}
	#else
		{ log(""); }
	#endif
	/*	leaderName and the next four functions use dynamically allocated
		memory in order to narrow wstrings. Therefore not const.
		All the functions returning char const* return an empty string when
		in silent mode (for performance rasons). */
	char const* leaderName(PlayerTypes ePlayer, int iCharLimit = 8)
	#if DISABLE_UWAI_REPORT
		{ return ""; }
	#else
		;
	#endif
	// Leader name if the master team has only 1 member, otherwise team name.
	char const* masterName(TeamTypes eMaster, int iCharLimit = 8)
	#if DISABLE_UWAI_REPORT
		{ return ""; }
	#else
		;
	#endif
	char const* teamName(TeamTypes eTeam)
	#if DISABLE_UWAI_REPORT
		{ return ""; }
	#else
		;
	#endif
	char const* techName(TechTypes eTeam, int iCharLimit = 8)
	#if DISABLE_UWAI_REPORT
		{ return ""; }
	#else
		;
	#endif
	char const* unitName(UnitTypes eUnit, int iCharLimit = 8)
	#if DISABLE_UWAI_REPORT
		{ return ""; }
	#else
		;
	#endif
	char const* cityName(CvCity const& kCity, int iCharLimit = 12)
	#if DISABLE_UWAI_REPORT
		{ return ""; }
	#else
		;
	#endif
	char const* warPlanName(WarPlanTypes eWarPlan) const
	#if DISABLE_UWAI_REPORT
		{ return ""; }
	#else
		;
	#endif
	// No effect on a silent report
	void setMute(bool b);
	// True if muted or if silent to begin with
	bool isMute() const { return (m_iMuted > 0); }
	void setSilent(bool b);

private:
	void writeToFile();
	void deleteBuffer();
	char const* narrow(wchar const* ws, int iCharLimit);

	CvString m_report;
	bool m_bSilent;
	int m_iMuted;
	std::vector<CvString*> m_aStringBuffer;
};

#endif
