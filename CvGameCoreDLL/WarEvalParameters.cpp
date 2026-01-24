#include "CvGameCoreDLL.h"
#include "WarEvalParameters.h"
#include "CvGameAI.h"
#include "CvTeamAI.h"
#include "AgentIterator.h"


WarEvalParameters::WarEvalParameters(TeamTypes eAgent,
	TeamTypes eTarget, UWAIReport& kReport,
	bool bIgnoreDistraction, PlayerTypes eSponsor,
	TeamTypes eCapitulationTeam)
:	m_eAgent(eAgent), m_eTarget(eTarget), m_kReport(kReport),
	m_eSponsor(eSponsor), m_eCapitulationTeam(eCapitulationTeam),
	m_bIgnoreDistraction(bIgnoreDistraction),
	// To be set by WarEvaluator:
	m_bTotal(false), m_bNaval(false), m_iPreparationTime(-1)
{
	m_bConsideringPeace = GET_TEAM(m_eAgent).isAtWar(m_eTarget);
	FAssert(m_eCapitulationTeam == NO_TEAM || m_bConsideringPeace);
	m_bImmediateDoW = (m_eSponsor != NO_PLAYER);
}


void WarEvalParameters::addWarAlly(TeamTypes eTeam)
{
	m_warAllies.insert(eTeam);
	m_warAllies.insert(GET_TEAM(eTeam).getMasterTeam());
	for (TeamIter<MAJOR_CIV,VASSAL_OF> itVassal(eTeam); itVassal.hasNext(); ++itVassal)
		m_warAllies.insert(itVassal->getID());
}


void WarEvalParameters::addExtraTarget(TeamTypes eTeam)
{
	m_extraTargets.insert(eTeam);
	m_extraTargets.insert(GET_TEAM(eTeam).getMasterTeam());
	for (TeamIter<MAJOR_CIV,VASSAL_OF> itVassal(eTeam); itVassal.hasNext(); ++itVassal)
		m_extraTargets.insert(itVassal->getID());
}


bool WarEvalParameters::isNoWarVsExtra() const
{	// (see header)
	return (!m_extraTargets.empty() && !isConsideringPeace() &&
			!isImmediateDoW() && !GET_TEAM(getAgent()).isAtWar(getTarget()));
}


void WarEvalParameters::setSponsor(PlayerTypes ePlayer)
{
	m_eSponsor = ePlayer;
	if (ePlayer != NO_PLAYER)
		setImmediateDoW(true);
}


WarEvalParamID WarEvalParameters::getID() const
{
	/*  Some 500 mio. possible combinations; fits into 32 bit.
		Ensure uniqueness through a mixed-base positional system: */
	WarEvalParamID i = m_eTarget + 1; i *= MAX_CIV_PLAYERS + 1;
	i += m_eAgent + 1; i *= MAX_CIV_PLAYERS + 1;
	i += m_bConsideringPeace; i *= 2;
	i += m_bIgnoreDistraction; i *= 2;
	i += m_bTotal; i *= 2;
	i += m_bNaval; i *= 2;
	FAssert(m_iPreparationTime + 1 < 50);
	i += m_iPreparationTime + 1; i *= 50;
	i += m_eSponsor + 1; i *= MAX_CIV_PLAYERS + 1;
	i += m_eCapitulationTeam + 1; i *= MAX_CIV_TEAMS + 1;
	i += m_bImmediateDoW;
	/*  WarAllies and ExtraTargets matter only in situations where the cache
		should be disabled. (Also wouldn't fit into a single int; would have
		to use 64 bit regardless of MAX_CIV_PLAYERS.) */
	FAssert(m_warAllies.empty() && m_extraTargets.empty());
	return i;
}
