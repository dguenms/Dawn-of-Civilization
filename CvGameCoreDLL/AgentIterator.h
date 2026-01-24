#pragma once

#ifndef AGENT_ITERATOR_H
#define AGENT_ITERATOR_H

/*  advc.agent: New file. Iterators over sequences of CvTeam or CvPlayer instances.
	The concrete iterator classes are defined at the end of the file.
	Caveat: Can't use agent iterators before CvAgents::gameStart has been called -
	which currently happens in CvGame::initDiplomacy and allGameDataRead. */

#include "AgentPredicates.h"
#include "CvAgents.h"

class CvTeam;
class CvPlayer;


/*  Base class that allows all instantiations of the AgentIterator template
	to share static variables */
class AgentIteratorBase
{
public:
	static void setAgentsCache(CvAgents const* pAgents);
protected:
	static CvAgents const* m_pAgents;
};

/*  This helper base class gets explicitly instantiated for all combinations
	of parameters in AgentIterator.cpp. This allows me to implement the
	passFilters function outside of the header file. passFilters requires
	CvPlayerAI.h and CvTeamAI.h; I don't want to include these in AgentIterator.h. */
template<class AgentType, AgentStatusPredicate eSTATUS, AgentRelationPredicate eRELATION,
	/*	The iterator should be able to provide non-AI agent instances, but it still needs
		to know the AI agent type b/c that's what's stored in the cached sequences. */
	class AgentAIType>
class ExplicitAgentIterator : protected AgentIteratorBase
{
protected:
	ExplicitAgentIterator(TeamTypes eTeam = NO_TEAM) : m_eTeam(eTeam) {}
	bool passFilters(AgentAIType const& kAgent) const;
	TeamTypes m_eTeam;

	// These two variables are needed in passFilters:

	/*  Cache that is either an exact match for the required predicates or
		(Barbarians to be added) a subset. (Named after the LaTeX command /subseteq.) */
	static CvAgents::AgentSeqCache const eCACHE_SUBSETEQ = (
			(eSTATUS == ANY_AGENT_STATUS && eRELATION == ANY_AGENT_RELATION) ?
			CvAgents::ALL :
			(eSTATUS == ANY_AGENT_STATUS && eRELATION == MEMBER_OF) ?
			CvAgents::MEMBER :
			(eSTATUS == EVER_ALIVE && eRELATION == ANY_AGENT_RELATION) ?
			CvAgents::CIV_EVER_ALIVE :
			((eSTATUS == ALIVE || eSTATUS == CIV_ALIVE) && eRELATION == ANY_AGENT_RELATION) ?
			CvAgents::CIV_ALIVE :
			(eSTATUS == ALIVE && eRELATION == MEMBER_OF) ?
			CvAgents::MEMBER_ALIVE :
			(eSTATUS == MAJOR_CIV && eRELATION == ANY_AGENT_RELATION) ?
			CvAgents::MAJOR_ALIVE :
			(eSTATUS >= ALIVE && eSTATUS <= MAJOR_CIV && eRELATION == VASSAL_OF) ?
			CvAgents::VASSAL_ALIVE :
			CvAgents::NO_CACHE);
	/*  Cache that is a superset of the required agents. Will have to filter out those
		that don't match the predicates. */
	static CvAgents::AgentSeqCache const eCACHE_SUPER = (
			eRELATION == ANY_AGENT_RELATION ?
			CvAgents::MAJOR_ALIVE : // Subseteq cache will handle non-majors
			eRELATION == MEMBER_OF ?
				(eSTATUS == EVER_ALIVE ? CvAgents::MEMBER : CvAgents::MEMBER_ALIVE) :
			eRELATION == VASSAL_OF ?
				(eSTATUS == ANY_AGENT_STATUS ? CvAgents::ALL :
				(eSTATUS == EVER_ALIVE ? CvAgents::CIV_EVER_ALIVE : CvAgents::VASSAL_ALIVE)) :
			// These four can apply to non-major agents
			(eRELATION == POTENTIAL_ENEMY_OF || eRELATION == KNOWN_TO ||
			eRELATION == KNOWN_POTENTIAL_ENEMY_OF || eRELATION == ENEMY_OF) ?
				(eSTATUS >= MAJOR_CIV ? CvAgents::MAJOR_ALIVE :
				(eSTATUS >= CIV_ALIVE ? CvAgents::CIV_ALIVE : CvAgents::ALL)) :
			((eRELATION == NOT_A_RIVAL_OF || eRELATION == NOT_SAME_TEAM_AS) && eSTATUS < MAJOR_CIV) ?
				(eSTATUS == CIV_ALIVE ? CvAgents::CIV_ALIVE : CvAgents::ALL) :
			CvAgents::MAJOR_ALIVE);
};

/*  It seems that the compiler doesn't remove unreachable branches if I define
	bAPPLY_FILTERS as a static bool const member. For 'eCACHE_... == CvAgents::NO_CACHE',
	it seems to work. */
#define bAPPLY_FILTERS (eCACHE_SUBSETEQ == CvAgents::NO_CACHE)
#define _bADD_BARBARIANS(eCACHE) (eCACHE != CvAgents::ALL && eCACHE != CvAgents::MEMBER && \
		eCACHE != CvAgents::MEMBER_ALIVE && eCACHE != CvAgents::VASSAL_ALIVE)
#define bADD_BARBARIANS (eSTATUS < CIV_ALIVE && eRELATION != VASSAL_OF && \
		eRELATION != NOT_A_RIVAL_OF && ((bAPPLY_FILTERS && _bADD_BARBARIANS(eCACHE_SUPER)) || \
		(!bAPPLY_FILTERS && _bADD_BARBARIANS(eCACHE_SUBSETEQ))))

template<class Derived, // CRT pattern (just for the setNextFromCache function)
	class AgentType, AgentStatusPredicate eSTATUS, AgentRelationPredicate eRELATION, class AgentAIType>
class AgentIterator : ExplicitAgentIterator<AgentType, eSTATUS, eRELATION, AgentAIType>
{
public:
	bool hasNext() const
	{
		return (m_pNext != NULL);
	}

	AgentType& operator*() const
	{
		/*	This is, at worst, an up-cast. But the compiler doesn't know this
			b/c the AI headers aren't included here. */
		return *(AgentType*)m_pNext;
	}

	AgentType* operator->() const
	{	// See above
		return (AgentType*)m_pNext;
	}

	/*  Like ListIterator.nextIndex in Java: "The index of the element that would be
		returned by a subsequent call to next [i.e. computeNext], or
		list size [sequence length] if the list iterator [AgentIterator] is at the end
		of the list [sequence]" */
	int nextIndex() const
	{
		return (bAPPLY_FILTERS ? m_iPos - m_iSkipped : m_iPos);
	}

	static int count(TeamTypes eTeam = NO_TEAM)
	{
		Derived it(eTeam);
		if (bAPPLY_FILTERS)
		{
			while (it.hasNext())
				it.generateNext();
			return it.nextIndex();
		}
		int iCount = it.m_iCacheSize;
		if (bADD_BARBARIANS)
		{
			if (eRELATION == ANY_AGENT_RELATION || it.passFilters(*getBarbarianAgent()))
				iCount++;
		}
		return iCount;
	}

protected:
	void setNextFromCache()
	{	// static polymorphism
		static_cast<Derived*>(this)->setNextFromCache();
	}

	AgentIterator(TeamTypes eTeam = NO_TEAM)
	:	ExplicitAgentIterator<AgentType,eSTATUS,eRELATION,AgentAIType>(eTeam)
	{
		/*  ExplicitAgentIterator gets instantiated for all combinations of template parameters,
			so these static assertions would fail in that class. In this derived class, they'll
			only fail when an offending AgentIterator object is declared.
			See comments in AgentPredicates.h about the specific assertions. */
		BOOST_STATIC_ASSERT(eSTATUS != ANY_AGENT_STATUS || eRELATION <= NOT_SAME_TEAM_AS);
		BOOST_STATIC_ASSERT(eRELATION != VASSAL_OF || eSTATUS != FREE_MAJOR_CIV);
		FAssert(eRELATION == ANY_AGENT_RELATION || (eTeam > NO_TEAM && eTeam < MAX_TEAMS));

		if (bAPPLY_FILTERS)
		{
			if (eCACHE_SUPER < CvAgents::NUM_STATUS_CACHES)
				m_pCache = m_pAgents->getAgentSeqCache<AgentAIType>(eCACHE_SUPER);
			else m_pCache = m_pAgents->getPerTeamSeqCache<AgentAIType>(eCACHE_SUPER, eTeam);
		}
		else
		{
			if (eCACHE_SUBSETEQ < CvAgents::NUM_STATUS_CACHES)
				m_pCache = m_pAgents->getAgentSeqCache<AgentAIType>(eCACHE_SUBSETEQ);
			else m_pCache = m_pAgents->getPerTeamSeqCache<AgentAIType>(eCACHE_SUBSETEQ, eTeam);
		}
		m_iSkipped = 0;
		m_iPos = 0;
		// Cache the cache size (std::vector computes it as 'end' minus 'begin')
		m_iCacheSize = static_cast<short>(m_pCache->size());
		m_pNext = NULL; //= generateNext() (No, leave this up to the ctor of Derived.)
	}

	AgentIterator& operator++()
	{
		FErrorMsg("Derived classes should define their own operator++ function");
		// This is what (non-abstract) derived classes should do
		generateNext();
		return *this;
	}

	/*  Tbd.(?): In the !bAPPLY_FILTERS&&!bADD_BARBARIANS case, it could be more efficient
		to split generateNext between hasNext (check bounds), operator++ (increment m_iPos)
		and operator* (access m_pCache). */
	void generateNext()
	{
		if (bADD_BARBARIANS)
		{
			int const iRemaining = m_iCacheSize - m_iPos;
			switch(iRemaining)
			{
			case 0:
				m_pNext = getBarbarianAgent();
				m_iPos++;
				// Currently all status predicates are already handled by bADD_BARBARIANS
				if (eRELATION != ANY_AGENT_RELATION && !passFilters(*m_pNext))
				{
					m_pNext = NULL;
					m_iSkipped++;
				}
				return;
			case -1:
				m_pNext = NULL;
				return;
			default:
				setNextFromCache();
			}
		}
		else
		{
			if (m_iPos < m_iCacheSize)
				setNextFromCache();
			else
			{
				m_pNext = NULL;
				return;
			}
		}
		m_iPos++;
		if (bAPPLY_FILTERS)
		{
			if (!passFilters(*m_pNext))
			{
				m_pNext = NULL;
				m_iSkipped++;
				generateNext(); // tail recursion
			}
		}
	}

	std::vector<AgentAIType*> const* m_pCache;
	AgentAIType* m_pNext;
	short m_iCacheSize;
	short m_iPos;
private:
	short m_iSkipped;

	// Don't want to assume that BARBARIAN_PLAYER==BARBARIAN_TEAM
	static AgentAIType* getBarbarianAgent()
	{
		return _getBarbarianAgent<AgentAIType>();
	}
	// Don't want to include an AI header for GET_PLAYER
	template<class T>
	static T* _getBarbarianAgent();
	template<>
	static CvPlayerAI* _getBarbarianAgent<CvPlayerAI>()
	{
		return (*m_pAgents->getAgentSeqCache<CvPlayerAI>(CvAgents::ALL))[BARBARIAN_PLAYER];
	}
	template<>
	static CvTeamAI* _getBarbarianAgent<CvTeamAI>()
	{
		return (*m_pAgents->getAgentSeqCache<CvTeamAI>(CvAgents::ALL))[BARBARIAN_TEAM];
	}
};
#undef bAPPLY_FILTERS
#undef bADD_BARBARIANS
#undef _bADD_BARBARIANS

// Traversal in random order
#define RandAgentIteratorBase \
	AgentIterator<RandAgentIterator<AgentType,eSTATUS,eRELATION,AgentAIType>, \
	AgentType, eSTATUS, eRELATION, AgentAIType>
template<class AgentType, AgentStatusPredicate eSTATUS, AgentRelationPredicate eRELATION, class AgentAIType>
class RandAgentIterator : public RandAgentIteratorBase
{
	friend class RandAgentIteratorBase;
protected:
	int* m_aiShuffledIndices;

	RandAgentIterator(CvRandom& kRand, TeamTypes eTeam = NO_TEAM)
	:	RandAgentIteratorBase(eTeam)
	{
		m_aiShuffledIndices = kRand.shuffle(m_iCacheSize);
		generateNext();
	}

	~RandAgentIterator()
	{
		delete[] m_aiShuffledIndices;
	}
	
	void setNextFromCache() // override
	{
		m_pNext = (*m_pCache)[m_aiShuffledIndices[m_iPos]];
	}
};
#undef RandAgentIteratorBase

// Normal (non-randomized) traversal
#define FwdAgentIteratorBase \
	AgentIterator<FwdAgentIterator<AgentType,eSTATUS,eRELATION,AgentAIType>, \
	AgentType, eSTATUS, eRELATION, AgentAIType>
template<class AgentType, AgentStatusPredicate eSTATUS, AgentRelationPredicate eRELATION, class AgentAIType>
class FwdAgentIterator : public FwdAgentIteratorBase
{
	friend class FwdAgentIteratorBase;
protected:
	FwdAgentIterator(TeamTypes eTeam = NO_TEAM) : FwdAgentIteratorBase(eTeam)
	{
		generateNext();
	}
	
	void setNextFromCache() // override
	{
		m_pNext = (*m_pCache)[m_iPos];
	}
};
#undef FwdAgentIteratorBase

/*	Want separate classes for AI and non-AI iterators - if only so that
	AI headers don't need to be included in non-AI code. Will need separate
	templates for randomization b/c they'll need a different constructor.
	(Or could specialize on a bRANDOMIZE parameter, but that wouldn't save me
	from typing the same redundant code either.) */
#define DEFINE_PLAYER_ITER(PlayerClassName) \
template<AgentStatusPredicate eSTATUS = ANY_AGENT_STATUS, AgentRelationPredicate eRELATION = ANY_AGENT_RELATION> \
class PlayerClassName##Iter : public FwdAgentIterator<Cv##PlayerClassName, eSTATUS, eRELATION, CvPlayerAI> \
{ \
public: \
	explicit PlayerClassName##Iter(TeamTypes eTeam = NO_TEAM) : \
	FwdAgentIterator<Cv##PlayerClassName,eSTATUS,eRELATION,CvPlayerAI>(eTeam) \
	{} \
	PlayerClassName##Iter& operator++() \
	{ \
		generateNext(); \
		return *this; \
	} \
}; \
template<AgentStatusPredicate eSTATUS = ANY_AGENT_STATUS, AgentRelationPredicate eRELATION = ANY_AGENT_RELATION> \
class PlayerClassName##RandIter : public RandAgentIterator<Cv##PlayerClassName, eSTATUS, eRELATION, CvPlayerAI> \
{ \
public: \
	explicit PlayerClassName##RandIter(CvRandom& kRand, TeamTypes eTeam = NO_TEAM) : \
	RandAgentIterator<Cv##PlayerClassName,eSTATUS,eRELATION,CvPlayerAI>(kRand, eTeam) \
	{} \
	PlayerClassName##RandIter& operator++() \
	{ \
		generateNext(); \
		return *this; \
	} \
};

DEFINE_PLAYER_ITER(Player)
DEFINE_PLAYER_ITER(PlayerAI)
#undef DEFINE_PLAYER_ITER

#define DEFINE_TEAM_ITER(TeamClassName) \
template<AgentStatusPredicate eSTATUS = ANY_AGENT_STATUS, AgentRelationPredicate eRELATION = ANY_AGENT_RELATION> \
class TeamClassName##Iter : public FwdAgentIterator<Cv##TeamClassName, eSTATUS, eRELATION, CvTeamAI> \
{ \
public: \
	explicit TeamClassName##Iter(TeamTypes eTeam = NO_TEAM) : \
	FwdAgentIterator<Cv##TeamClassName,eSTATUS,eRELATION,CvTeamAI>(eTeam) \
	{ \
		/* Can't loop over all "teams that are members of eTeam" */ \
		BOOST_STATIC_ASSERT(eRELATION != MEMBER_OF); \
	} \
	TeamClassName##Iter& operator++() \
	{ \
		generateNext(); \
		return *this; \
	} \
}; \
template<AgentStatusPredicate eSTATUS = ANY_AGENT_STATUS, AgentRelationPredicate eRELATION = ANY_AGENT_RELATION> \
class TeamClassName##RandIter : public RandAgentIterator<Cv##TeamClassName, eSTATUS, eRELATION, CvTeamAI> \
{ \
public: \
	explicit TeamClassName##RandIter(CvRandom& kRand, TeamTypes eTeam = NO_TEAM) : \
	RandAgentIterator<Cv##TeamClassName,eSTATUS,eRELATION,CvTeamAI>(kRand, eTeam) \
	{ \
		BOOST_STATIC_ASSERT(eRELATION != MEMBER_OF); \
	} \
	TeamClassName##RandIter& operator++() \
	{ \
		generateNext(); \
		return *this; \
	} \
};

DEFINE_TEAM_ITER(Team)
DEFINE_TEAM_ITER(TeamAI)
#undef DEFINE_TEAM_ITER

//template<AgentStatusPredicate eSTATUS = ALIVE>
/*  The above would require empty angle brackets for members alive.
	I expect that a status other than ALIVE will rarely be needed;
	will have to use PlayerIter for that. */
#define DEFINE_MEMBER_ITER(PlayerClassName, IterClassName) \
class IterClassName##Iter : public PlayerClassName##Iter<ALIVE, MEMBER_OF> \
{ \
public: \
	explicit IterClassName##Iter(TeamTypes eTeam) : PlayerClassName##Iter<ALIVE,MEMBER_OF>(eTeam) {} \
	IterClassName##Iter& operator++() \
	{ \
		generateNext(); \
		return *this; \
	} \
};

DEFINE_MEMBER_ITER(Player, Member)
DEFINE_MEMBER_ITER(PlayerAI, MemberAI)
#undef DEFINE_MEMBER_ITER

#endif
