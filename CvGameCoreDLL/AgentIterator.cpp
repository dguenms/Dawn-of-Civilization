// advc.agent: New file; see comment in header.

#include "CvGameCoreDLL.h"
#include "AgentIterator.h"
#include "CvPlayerAI.h"
#include "CvTeamAI.h"


CvAgents const* AgentIteratorBase::m_pAgents = NULL;

void AgentIteratorBase::setAgentsCache(CvAgents const* pAgents)
{
	m_pAgents = pAgents;
}


namespace
{
	__inline TeamTypes getTeam(CvPlayerAI const& kPlayer)
	{
		return kPlayer.getTeam();
	}
	__inline TeamTypes getTeam(CvTeamAI const& kTeam)
	{
		return kTeam.getID();
	}

	// Helper functions that check eCACHE to save time

	template<class AgentType,AgentStatusPredicate eSTATUS,AgentRelationPredicate eRELATION,
	CvAgents::AgentSeqCache eCACHE>
	__inline bool isBarbarian(AgentType const& kAgent)
	{
		return (eCACHE == CvAgents::ALL && kAgent.isBarbarian());
	}
	template<class AgentType,AgentStatusPredicate eSTATUS,AgentRelationPredicate eRELATION,
	CvAgents::AgentSeqCache eCACHE>
	__inline bool isEverAlive(AgentType const& kAgent)
	{
		return (eCACHE != CvAgents::ALL || kAgent.isEverAlive());
	}
	template<class AgentType,AgentStatusPredicate eSTATUS,AgentRelationPredicate eRELATION,
	CvAgents::AgentSeqCache eCACHE>
	__inline bool isAlive(AgentType const& kAgent)
	{
		return ((eCACHE != CvAgents::ALL && eCACHE != CvAgents::CIV_EVER_ALIVE) ||
				kAgent.isAlive());
	}
	template<class AgentType,AgentStatusPredicate eSTATUS,AgentRelationPredicate eRELATION,
	CvAgents::AgentSeqCache eCACHE>
	__inline bool isMinorCiv(AgentType const& kAgent)
	{
		return (eCACHE != CvAgents::MAJOR_ALIVE && kAgent.isMinorCiv());
	}
	template<class AgentType,AgentStatusPredicate eSTATUS,AgentRelationPredicate eRELATION,
	CvAgents::AgentSeqCache eCACHE>
	__inline bool isAVassal(AgentType const& kAgent)
	{
		return GET_TEAM(getTeam(kAgent)).isAVassal();
	}
	template<class AgentType,AgentStatusPredicate eSTATUS,AgentRelationPredicate eRELATION,
	CvAgents::AgentSeqCache eCACHE>
	__inline bool isSameMaster(AgentType const& kAgent, TeamTypes eTeam)
	{
		return (GET_TEAM(getTeam(kAgent)).getMasterTeam() == GET_TEAM(eTeam).getMasterTeam());
	}
}


template<class AgentType, AgentStatusPredicate eSTATUS, AgentRelationPredicate eRELATION, class AgentAIType>
bool ExplicitAgentIterator<AgentType,eSTATUS,eRELATION,AgentAIType>::passFilters(AgentAIType const& kAgent) const
{
	#define args AgentAIType,eSTATUS,eRELATION,eCACHE_SUPER
	switch(eSTATUS)
	{
	case ANY_AGENT_STATUS:
		break;
	case CIV_ALIVE:
		if (isBarbarian<args>(kAgent) || !isAlive<args>(kAgent))
			return false;
		break;
	case EVER_ALIVE:
		if (!isEverAlive<args>(kAgent))
			return false;
		break;
	case ALIVE:
		if (!isAlive<args>(kAgent))
			return false;
		break;
	case MAJOR_CIV:
		if (isMinorCiv<args>(kAgent) || !isAlive<args>(kAgent) || isBarbarian<args>(kAgent))
			return false;
		break;
	/*case VASSAL:
		if (!isAVassal<args>(kAgent) || !isAlive<args>(kAgent)
			return false;
		break;*/
	case FREE_MAJOR_CIV:
		if (isMinorCiv<args>(kAgent) || !isAlive<args>(kAgent) ||
			isAVassal<args>(kAgent))
		{
			return false;
		}
		break;
	/*case FREE_MAJOR_AI_CIV:
		if (kAgent.isHuman() || isMinorCiv<args>(kAgent) ||
				!isAlive<args>(kAgent) || isAVassal<args>(kAgent))
			return false;
		break;*/
	case HUMAN:
		if (!kAgent.isHuman() || !isAlive<args>(kAgent))
			return false;
		break;
	default:
		FErrorMsg("Unknown agent status type");
		return false;
	}
	switch(eRELATION)
	{
	case ANY_AGENT_RELATION:
		return true;
	case MEMBER_OF:
		return (eCACHE_SUPER == CvAgents::MEMBER || getTeam(kAgent) == m_eTeam);
	case NOT_SAME_TEAM_AS:
		return (getTeam(kAgent) != m_eTeam);
	case VASSAL_OF:
		return (eCACHE_SUPER == CvAgents::VASSAL_ALIVE || GET_TEAM(getTeam(kAgent)).isVassal(m_eTeam));
	case NOT_A_RIVAL_OF:
		return (getTeam(kAgent) == m_eTeam || isSameMaster<args>(kAgent, m_eTeam));
	case POTENTIAL_ENEMY_OF:
		return (getTeam(kAgent) != m_eTeam && !isSameMaster<args>(kAgent, m_eTeam));
	case KNOWN_TO:
		return GET_TEAM(getTeam(kAgent)).isHasMet(m_eTeam);
	case OTHER_KNOWN_TO:
		return (GET_TEAM(getTeam(kAgent)).isHasMet(m_eTeam) && getTeam(kAgent) != m_eTeam);
	case KNOWN_POTENTIAL_ENEMY_OF:
		return (GET_TEAM(getTeam(kAgent)).isHasMet(m_eTeam) && !isSameMaster<args>(kAgent, m_eTeam));
	case ENEMY_OF:
		return GET_TEAM(getTeam(kAgent)).isAtWar(m_eTeam);
	default:
		FErrorMsg("Unknown agent relation type");
		return false;
	}
	#undef args
}

/*  All possible instantiations; needed by the linker. See comment above
	ExplicitAgentIterator in the header file.
	Some combinations of predicates don't actually make sense; I don't
	know how to skip those here. Instead, nonsensical combinations are
	addressed through static assertions in the AgentIterator constructor. */

#define INSTANTIATE_AGENT_ITERATOR(S, R) \
	template class ExplicitAgentIterator<CvPlayer,S,R,CvPlayerAI>; \
	template class ExplicitAgentIterator<CvTeam,S,R,CvTeamAI>; \
	template class ExplicitAgentIterator<CvPlayerAI,S,R,CvPlayerAI>; \
	template class ExplicitAgentIterator<CvTeamAI,S,R,CvTeamAI>;

/*	(To avoid listing the predicates in two places, one could move these
	definitions to AgentPredicates.h and generate the enums through a macro.) */
#define DO_FOR_EACH_STATUS(DO) \
	DO(ANY_AGENT_STATUS) \
	DO(EVER_ALIVE) \
	DO(ALIVE) \
	DO(CIV_ALIVE) \
	DO(MAJOR_CIV) \
	/*DO(VASSAL)*/ \
	DO(FREE_MAJOR_CIV) \
	/*DO(FREE_MAJOR_AI_CIV)*/ \
	DO(HUMAN)

#define DO_FOR_EACH_RELATION(S, DO) \
	DO(S, ANY_AGENT_RELATION) \
	DO(S, MEMBER_OF) \
	DO(S, NOT_SAME_TEAM_AS) \
	DO(S, VASSAL_OF) \
	DO(S, NOT_A_RIVAL_OF) \
	DO(S, POTENTIAL_ENEMY_OF) \
	DO(S, KNOWN_TO) \
	DO(S, OTHER_KNOWN_TO) \
	DO(S, KNOWN_POTENTIAL_ENEMY_OF) \
	DO(S, ENEMY_OF)

#define INSTANTIATE_FOR_EACH_RELATION(S) DO_FOR_EACH_RELATION(S, INSTANTIATE_AGENT_ITERATOR)

DO_FOR_EACH_STATUS(INSTANTIATE_FOR_EACH_RELATION);
