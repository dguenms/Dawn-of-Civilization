#include "CvGameCoreDLL.h"
#include "WarEvaluator.h"
#include "UWAIAgent.h"
#include "WarUtilityAspect.h"
#include "MilitaryAnalyst.h"
#include "UWAIReport.h"
#include "WarEvalParameters.h"
#include "CoreAI.h"
#include "CvInfo_GameOption.h"

using std::vector;
using std::string;
using std::ostringstream;

/*	When a player trades with the AI, the EXE asks the DLL to compute trade values
	several times in a row (usually about a dozen times), which is enough to cause
	a noticeable delay. Therefore this primitive caching mechanism. The cache is
	always used on the Trade screen; in other (async) UI contexts, it has to be enabled
	explicitly through the bUseCache param of the constructor, or the static
	enableCache function. As for the latter, it's important to call disableCache
	before returning to a synchronized context b/c the cache doesn't work in all
	situations (see WarEvalParameters::getID) and isn't stored in savegames. */
bool WarEvaluator::m_bCheckCache = false;
bool WarEvaluator::m_bCacheCleared = true;
/*	Cache size: Calls alternate between naval/ non-naval,
	limited/ total or mutual war utility of two civs,
	so caching just the last result isn't effective. */
#define iCACHE_SZ 16
namespace
{
	WarEvalParamID aiLastCallParams[iCACHE_SZ];
	int aiLastCallResult[iCACHE_SZ];
	int iLastIndex;
}

void WarEvaluator::enableCache()
{
	m_bCheckCache = true;
	m_bCacheCleared = false;
}

void WarEvaluator::disableCache()
{
	m_bCheckCache = false;
}

void WarEvaluator::clearCache()
{
	if (m_bCacheCleared) // Just to make sure that repeated clears don't waste time
		return;
	m_bCacheCleared = true;
	for (int i = 0; i < iCACHE_SZ; i++)
		aiLastCallResult[i] = MIN_INT;
}


WarEvaluator::WarEvaluator(WarEvalParameters& kWarEvalParams, bool bUseCache)
:	m_kParams(kWarEvalParams), m_kReport(m_kParams.getReport()),
	m_kAgent(GET_TEAM(m_kParams.getAgent())),
	m_kTarget(GET_TEAM(m_kParams.getTarget())),
	m_bUseCache(bUseCache), m_bPeaceScenario(false)
{
	static bool bInitCache = true;
	if (bInitCache)
	{
		for (int i = 0; i < iCACHE_SZ; i++)
		{
			aiLastCallParams[i] = 0;
			aiLastCallResult[i] = MIN_INT;
		}
		iLastIndex = 0;
		bInitCache = false;
	}
	FAssert(m_kAgent.getID() != m_kTarget.getID());
	FAssert(!m_kTarget.isAVassal());
	FAssert(m_kAgent.isHasMet(m_kTarget.getID()));
}


void WarEvaluator::reportPreamble()
{
	if (m_kReport.isMute())
		return;
	/* Show members in one column per team. Use spaces for alignment, table
	   markers ('|') for Textile. */
	m_kReport.log("Evaluating *%s%s war* between %s%s and %s%s", m_kParams.isTotal() ?
			m_kReport.warPlanName(WARPLAN_TOTAL) : m_kReport.warPlanName(WARPLAN_LIMITED),
			m_kParams.isNaval() ? " naval" : "",
			m_kReport.teamName(m_kAgent.getID()), m_kAgent.isHuman() ? " (human)" : "",
			m_kReport.teamName(m_kTarget.getID()), m_kTarget.isHuman() ? " (human)" : "");
	m_kReport.logNewline();
	for (MemberIter agentIt(m_kAgent.getID()), targetIt(m_kTarget.getID());
		agentIt.hasNext() || targetIt.hasNext(); ++agentIt, ++targetIt)
	{
		ostringstream os;
		os << "| " << (agentIt.hasNext()
				? m_kReport.leaderName(agentIt->getID(), 16)
				: "");
		string msg = os.str().substr(0, 17);
		msg += " |";
		while (msg.length() < 20)
			msg += " ";
		if (targetIt.hasNext())
			msg += m_kReport.leaderName(targetIt->getID(), 16);
		msg += "|\n";
		m_kReport.log(msg.c_str());
	}
	m_kReport.log("Current actual war plan: %s",
			m_kReport.warPlanName(m_kAgent.AI_getWarPlan(m_kTarget.getID())));
	if (m_kParams.isConsideringPeace())
		m_kReport.log("(considering peace)");
	m_kReport.log("Preparation time vs. target: %d",
			m_kParams.getPreparationTime());
	if (m_kParams.isImmediateDoW())
		m_kReport.log("Immediate DoW assumed");
	if (m_kAgent.isAVassal())
	{
		m_kReport.log("Agent is a vassal of %s",
				m_kReport.masterName(m_kAgent.getMasterTeam()));
	}
	if (m_kTarget.isAVassal())
	{
		m_kReport.log("Target is a vassal of %s",
				m_kReport.masterName(m_kTarget.getMasterTeam()));
	}
	FOR_EACH_ENUM2(Team, eAlly)
	{
		if (m_kParams.isWarAlly(eAlly))
			m_kReport.log("Joint DoW by %s assumed", m_kReport.teamName(eAlly));
	}
	FOR_EACH_ENUM2(Team, eExtraTarget)
	{
		if (m_kParams.isExtraTarget(eExtraTarget))
			m_kReport.log("Extra target: %s", m_kReport.teamName(eExtraTarget));
	}
	if (m_kParams.getSponsor() != NO_PLAYER)
	{
		m_kReport.log("Sponsored by %s",
				m_kReport.leaderName(m_kParams.getSponsor()));
		FAssert(m_kParams.isImmediateDoW());
	}
	if (m_kParams.isIgnoreDistraction())
		m_kReport.log("Computation ignoring Distraction cost");
}


int WarEvaluator::defaultPreparationTime(WarPlanTypes eWarPlan)
{
	int iWPAge = 0;
	if (eWarPlan == NO_WARPLAN)
		eWarPlan = m_kAgent.AI_getWarPlan(m_kTarget.getID());
	else iWPAge = m_kAgent.AI_getWarPlanStateCounter(m_kTarget.getID());
	// Agent is past preparations
	if (eWarPlan == WARPLAN_LIMITED || eWarPlan == WARPLAN_TOTAL)
		return 0;
	int iBaseTime = -1;
	if (m_kParams.isTotal())
	{
		if (m_kParams.isNaval())
			iBaseTime = getUWAI().preparationTimeTotalNaval();
		else iBaseTime = getUWAI().preparationTimeTotal();
	}
	else
	{
		if (m_kParams.isNaval())
			iBaseTime = getUWAI().preparationTimeLimitedNaval();
		else iBaseTime = getUWAI().preparationTimeLimited();
	}
	int iR = std::max(iBaseTime - iWPAge, 0);
	iR *= GC.getInfo(GC.getGame().getGameSpeedType()).getTrainPercent();
	iR = intdiv::uround(iR, 100);
	return iR;
}


int WarEvaluator::evaluate(WarPlanTypes eWarPlan, int iPreparationTime)
{
	if (m_kParams.isImmediateDoW())
		iPreparationTime = 0;
	// Plan for war scenario
	if (eWarPlan == NO_WARPLAN)
		eWarPlan = m_kAgent.AI_getWarPlan(m_kParams.getTarget());
	if(eWarPlan == NO_WARPLAN)
	{
		if (iPreparationTime == 0)
			eWarPlan = WARPLAN_LIMITED;
		else eWarPlan = WARPLAN_PREPARING_LIMITED;
	}
	bool const bTotal = (eWarPlan == WARPLAN_TOTAL ||
			eWarPlan == WARPLAN_PREPARING_TOTAL);
	if (m_kAgent.isAtWar(m_kTarget.getID()))
	{
		/*	If already at war, MilitaryAnalyst determines whether it should be naval.
			(Doesn't currently write this into params though - should it?)
			Might as well not bother with the land target check then? */
		bool const bNaval = !m_kAgent.AI_isLandTarget(m_kTarget.getID());
		int iU = evaluate(eWarPlan, bNaval, 0);
		m_kParams.setNaval(bNaval);
		m_kParams.setTotal(bTotal);
		m_kParams.setPreparationTime(0);
		return iU;
	}
	/*	Just for performance: Don't compute naval war utility if we have
		no transports. Do compute utility of limited naval war. May not give
		us enough time to produce transports; then war utility will be low.
		But could also already have transports e.g. from earlier wars.
		(BtS/K-Mod only considers total naval war.) */
	bool bSkipNaval = true;
	for (MemberAIIter itMember(m_kAgent.getID()); itMember.hasNext(); ++itMember)
	{
		if (itMember->AI_totalUnitAIs(UNITAI_ASSAULT_SEA) +
			itMember->AI_totalUnitAIs(UNITAI_SETTLER_SEA) > 0)
		{
			bSkipNaval = false;
		}
	}
	/*  If the report isn't mute anyway, and we're doing two runs, rather than
		flooding the report with logs for both naval and non-naval utility, mute
		the report in both runs, and do an additional run just for logging
		once we know if naval or non-naval war is better. */
	bool bExtraRun = (!m_kReport.isMute() && !bSkipNaval);
	if (bExtraRun)
		m_kReport.setMute(true);
	int iNonNavalU = evaluate(eWarPlan, false, iPreparationTime);
	// Assume non-naval war if it hardly makes a difference
	int const iAntiNavalBias = 3;
	int iNavalU = MIN_INT;
	if (!bSkipNaval)
		iNavalU = evaluate(eWarPlan, true, iPreparationTime);
	int iU=MIN_INT;
	if (bExtraRun)
	{
		m_kReport.setMute(false);
		iU = evaluate(eWarPlan,
				iNavalU > iNonNavalU + iAntiNavalBias, iPreparationTime);
	}
	else
	{
		if (iNavalU > iNonNavalU + iAntiNavalBias)
			iU = iNavalU;
		else iU = iNonNavalU;
	}
	/*  Calls to evaluate(WarPlanTypes,bool,int) change some members of m_kParams
		that the caller may read */
	m_kParams.setNaval(iNavalU > iNonNavalU + iAntiNavalBias);
	m_kParams.setTotal(bTotal);
	m_kParams.setPreparationTime(defaultPreparationTime(eWarPlan));
	return iU;
}


int WarEvaluator::evaluate(WarPlanTypes eWarPlan, bool bNaval, int iPreparationTime)
{
	PROFILE_FUNC(); // All war evaluation goes through here
	m_bPeaceScenario = (eWarPlan == NO_WARPLAN); // Should only happen in recursive call
	m_kParams.setNaval(bNaval);
	/*  The original cause of war (dogpile, attacked etc.) has no bearing
		on war utility. */
	m_kParams.setTotal(eWarPlan == WARPLAN_TOTAL || eWarPlan == WARPLAN_PREPARING_TOTAL);
	if (iPreparationTime < 0)
	{
		FAssert(!m_bPeaceScenario); // Needs to be set in the war scenario call
		iPreparationTime = defaultPreparationTime(eWarPlan);
	}
	m_kParams.setPreparationTime(iPreparationTime);
	// Don't check cache in recursive calls (peaceScenario=true)
	if (!m_bPeaceScenario && (m_bCheckCache || m_bUseCache || gDLL->isDiplomacy()))
	{
		WarEvalParamID iParamID = m_kParams.getID();
		for (int i = 0; i < iCACHE_SZ; i++)
		{
			if (iParamID == aiLastCallParams[i] && aiLastCallResult[i] != MIN_INT)
				return aiLastCallResult[i];
		}
	}
	if (m_bPeaceScenario)
		m_kReport.log("*Peace scenario*\n");
	else
	{
		/*  Normally, both are evaluated, and war goes first. Logging the preamble
			once is enough. */
		reportPreamble();
		m_kReport.log("*War scenario*\n");
	}
	vector<WarUtilityAspect*> apAspects;
	fillWithAspects(apAspects);
	for (MemberIter itMember(m_kAgent.getID()); itMember.hasNext(); ++itMember)
		evaluate(itMember->getID(), apAspects);
	int iU = 0;
	for (size_t i = 0; i < apAspects.size(); i++)
	{
		int iDelta = apAspects[i]->utility();
		iU += iDelta;
		if (iDelta != 0)
			m_kReport.log("%s total: %d", apAspects[i]->aspectName(), iDelta);
		delete apAspects[i];
	}
	m_kReport.log("Bottom line: %d\n", iU);
	if (!m_bPeaceScenario)
	{
		iU -= evaluate(NO_WARPLAN, false, iPreparationTime);
		m_kReport.log("Utility war minus peace: %d\n", iU);
		// Restore params (changed by recursive call)
		m_kParams.setNaval(bNaval);
		m_kParams.setTotal(eWarPlan == WARPLAN_TOTAL ||
				eWarPlan == WARPLAN_PREPARING_TOTAL);
		m_kParams.setPreparationTime(iPreparationTime);
		/*  Could update cache even when !m_bCheckCache, but this might
			push out just the values that are needed ... */
		if (m_bCheckCache || m_bUseCache)
		{
			// Cache the total result after returning from the recursive call
			WarEvalParamID iParamID = m_kParams.getID();
			aiLastCallParams[iLastIndex] = iParamID;
			aiLastCallResult[iLastIndex] = iU;
			iLastIndex = (iLastIndex + 1) % iCACHE_SZ;
		}
	}
	return iU;
}


void WarEvaluator::fillWithAspects(vector<WarUtilityAspect*>& kAspects)
{
	// Abbreviate ...
	vector<WarUtilityAspect*>& v = kAspects;
	WarEvalParameters const& params = m_kParams;

	v.push_back(new GreedForAssets(params));
	v.push_back(new GreedForVassals(params));
	v.push_back(new GreedForSpace(params));
	v.push_back(new GreedForCash(params));
	v.push_back(new Loathing(params));
	v.push_back(new MilitaryVictory(params));
	v.push_back(new Assistance(params));
	v.push_back(new Reconquista(params));
	v.push_back(new Rebuke(params));
	v.push_back(new Fidelity(params));
	v.push_back(new HiredHand(params));
	v.push_back(new BorderDisputes(params));
	v.push_back(new SuckingUp(params));
	v.push_back(new PreEmptiveWar(params));
	v.push_back(new KingMaking(params));
	v.push_back(new Effort(params));
	v.push_back(new Risk(params));
	v.push_back(new IllWill(params));
	v.push_back(new Affection(params));
	if(!params.isIgnoreDistraction())
		v.push_back(new Distraction(params));
	v.push_back(new PublicOpposition(params));
	v.push_back(new Revolts(params));
	v.push_back(new UlteriorMotives(params));
	v.push_back(new TacticalSituation(params));
	v.push_back(new Bellicosity(params));
	v.push_back(new FairPlay(params));
	v.push_back(new LoveOfPeace(params));
	v.push_back(new ThirdPartyIntervention(params));
	v.push_back(new DramaticArc(params));
	FAssert(UWAI::NUM_ASPECTS - (params.isIgnoreDistraction() ? 1 : 0) == (int)v.size());
}


void WarEvaluator::evaluate(PlayerTypes eAgentPlayer, vector<WarUtilityAspect*>& kAspects)
{
	MilitaryAnalyst militaryAnalyst(eAgentPlayer, m_kParams, m_bPeaceScenario);
	for (PlayerIter<MAJOR_CIV,KNOWN_TO> it(m_kAgent.getID()); it.hasNext(); ++it)
	{
		if (!GET_TEAM(it->getID()).isCapitulated())
			militaryAnalyst.logResults(it->getID());
	}
	m_kReport.log("\nh4.\nComputing utility of %s\n",
			m_kReport.leaderName(eAgentPlayer, 16));
	int iU = 0;
	for (size_t i = 0; i < kAspects.size(); i++)
		iU += kAspects[i]->evaluate(militaryAnalyst);
	m_kReport.log("--\nTotal utility for %s: %d",
			m_kReport.leaderName(eAgentPlayer, 16), iU);
}
