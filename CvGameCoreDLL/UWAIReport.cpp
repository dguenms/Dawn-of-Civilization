#include "CvGameCoreDLL.h"
#include "UWAIReport.h"
#include "CvGamePlay.h"
#include "CvCity.h"

using std::ostringstream;
using std::string;


UWAIReport::UWAIReport(bool bSilent)
{
	/*  The log could be used to cheat in multiplayer. It's OK if MessageLog
		is enabled; the game will warn the other player about that. */
	if (GC.getGame().isNetworkMultiPlayer() && !GC.isLogging())
		bSilent = true;
	setSilent(bSilent);
}


UWAIReport::~UWAIReport()
{
	if (!m_report.IsEmpty())
	{
		log("_This logfile is formatted in Textile. Paste its content "
			"into the web converter on "
			"http://borgar.github.io/textile-js/#text_preview"
			" for HTML output that is easier to read. "
			"(You can download the web converter by saving the web page.)_");
		writeToFile();
	}
	deleteBuffer();
}

#if !DISABLE_UWAI_REPORT
void UWAIReport::log(char const* fmt, ...)
{
	if (m_iMuted > 0)
		return;
	va_list args;
	va_start(args, fmt);
	m_report += CvString::formatv(fmt, args);
	va_end(args);
	m_report += CvString::format("\n");
	writeToFile();
}
#endif

void UWAIReport::writeToFile()
{
	if (m_iMuted > 0)
		return;
	ostringstream logFileName;
	/*if(GC.getGame().isNetworkMultiPlayer()) // For OOS debugging on a single PC
		logFileName << (int)GC.getGame().getActivePlayer() << "_";*/
	logFileName << "uwai" << GC.getGame().getGameTurn() << ".log";
	gDLL->logMsg(logFileName.str().c_str(), m_report, false, false);
	m_report.clear();
}


void UWAIReport::deleteBuffer()
{
	for (size_t i = 0; i < m_aStringBuffer.size(); i++)
		delete m_aStringBuffer[i];
}

#if !DISABLE_UWAI_REPORT
char const* UWAIReport::leaderName(PlayerTypes ePlayer, int iCharLimit)
{
	if (m_iMuted > 0)
		return "";
	return narrow(GC.getInfo(GET_PLAYER(ePlayer).getLeaderType()).getDescription(),
			iCharLimit);
}

char const* UWAIReport::unitName(UnitTypes eUnit, int iCharLimit)
{
	if (m_iMuted > 0)
		return "";
	return narrow(GC.getInfo(eUnit).getDescription(), iCharLimit);
}

char const* UWAIReport::cityName(CvCity const& kCity, int iCharLimit)
{
	if (m_iMuted > 0)
		return "";
	return narrow(kCity.getName(), iCharLimit);
}
#endif

char const* UWAIReport::narrow(wchar const* ws, int iCharLimit)
{
	// This is probably a bit more complicated than it needs to be ...
	CvString cvs(ws);
	string s = cvs.substr(0, iCharLimit);
	/*	Trailing (or leading for that matter) spaces in names of units, leaders
		etc. mess up the Textile formatting. Such spaces don't normally occur,
		but char limit can leave a space at the end. */
	while (s[s.length() - 1] == ' ')
		s = s.substr(0, s.length() - 1);
	CvString* pNewString = new CvString(s.c_str());
	m_aStringBuffer.push_back(pNewString);
	return pNewString->c_str();
}

#if !DISABLE_UWAI_REPORT
char const* UWAIReport::masterName(TeamTypes eMaster, int iCharLimit)
{
	if (m_iMuted > 0)
		return "";
	CvTeam const& kMaster = GET_TEAM(eMaster);
	if (kMaster.getNumMembers() > 1)
		return teamName(eMaster);
	return leaderName(kMaster.getLeaderID());
}

char const* UWAIReport::teamName(TeamTypes eTeam)
{
	if (m_iMuted > 0)
		return "";
	ostringstream ss;
	/*  Textile turns this into a tooltip showing the team leader's name.
		I guess 'T' followed by a number has that effect. OK ... */
	ss << "T" << (int)eTeam << "(" <<
			leaderName(GET_TEAM(eTeam).getLeaderID()) << ")";
	string s = ss.str();
	CvString* pNewString = new CvString(s.c_str());
	m_aStringBuffer.push_back(pNewString);
	return pNewString->c_str();
}

char const* UWAIReport::techName(TechTypes eTech, int iCharLimit)
{
	if (m_iMuted > 0)
		return "";
	return narrow(GC.getInfo(eTech).getDescription(), iCharLimit);
}

char const* UWAIReport::warPlanName(WarPlanTypes eWarPlan) const
{
	if (m_iMuted > 0)
		return "";
	switch (eWarPlan)
	{
	case NO_WARPLAN: return "none";
	case WARPLAN_ATTACKED_RECENT: return "attacked recent";
	case WARPLAN_ATTACKED: return "attacked";
	case WARPLAN_PREPARING_LIMITED: return "preparing limited";
	case WARPLAN_PREPARING_TOTAL: return "preparing total";
	case WARPLAN_LIMITED: return "limited";
	case WARPLAN_TOTAL: return "total";
	case WARPLAN_DOGPILE: return "dogpile";
	default: return "unrecognized";
	}
}
#endif

void UWAIReport::setMute(bool b)
{
	if (m_bSilent)
		return;
	/*  This way, a subroutine can mute and unmute the report w/o checking
		if the report has already been muted. */
	if(b)
		m_iMuted++;
	else m_iMuted--;
}


void UWAIReport::setSilent(bool b)
{
	m_bSilent = b;
	if (m_bSilent)
		m_iMuted = 1;
	else m_iMuted = 0;
}
