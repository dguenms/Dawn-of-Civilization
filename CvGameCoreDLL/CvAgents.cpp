// advc.agent: New file; see comment in header file.

#include "CvGameCoreDLL.h"
#include "CvAgents.h"
#include "CoreAI.h"

CvAgents::CvAgents(int iMaxPlayers, int iMaxTeams)
{
	// Tbd.: Instead create the CvPlayerAI and CvTeamAI instances here

	m_playerSeqCache.resize(NUM_STATUS_CACHES);
	m_teamSeqCache.resize(NUM_STATUS_CACHES);
	m_memberSeqCache.resize(NUM_RELATION_CACHES);
	m_teamPerTeamSeqCache.resize(NUM_RELATION_CACHES);
	for (int i = 0; i < NUM_RELATION_CACHES; i++)
	{
		m_memberSeqCache[i].resize(iMaxTeams);
		m_teamPerTeamSeqCache[i].resize(iMaxTeams);
	}
	for (int i = 0; i < iMaxTeams; i++)
	{
		CvTeamAI* pTeam = &GET_TEAM((TeamTypes)i);
		teamSeqCache(ALL).push_back(pTeam);
	}
	for (int i = 0; i < iMaxPlayers; i++)
	{
		CvPlayerAI* pPlayer = &GET_PLAYER((PlayerTypes)i);
		playerSeqCache(ALL).push_back(pPlayer);
	}
	AgentIteratorBase::setAgentsCache(this);
}


void CvAgents::gameStart(bool bFromSaveGame)
{
	updateAllCachedSequences();
	// <advc.test>
	if (bFromSaveGame)
	{
		int TestAgentIterator(int);
		int iNonsense = TestAgentIterator(100);
		if (iNonsense == -1) // Just to make sure that the whole thing doesn't somehow get optimized away
		{
			FAssert(false);
			updateAllCachedSequences();
		}
	} // </advc.test>
}

void CvAgents::updateAllCachedSequences()
{
	for (int i = ALL + 1; i < NUM_STATUS_CACHES; i++)
	{
		AgentSeqCache eCacheID = (AgentSeqCache)i;
		playerSeqCache(eCacheID).clear();
		teamSeqCache(eCacheID).clear();
	}
	int const iTeams =  (int)teamSeqCache(ALL).size();
	for (int i = NUM_STATUS_CACHES; i < NUM_CACHES; i++)
	{
		AgentSeqCache eCacheID = (AgentSeqCache)i;
		for (int j = 0; j < iTeams; j++)
		{
			TeamTypes eTeam = (TeamTypes)j;
			memberSeqCache(eCacheID, eTeam).clear();
			teamPerTeamSeqCache(eCacheID, eTeam).clear();
		}
	}
	for (int i = 0; i < iTeams; i++)
	{
		CvTeamAI* pTeam = teamSeqCache(ALL)[i];
		if (pTeam->isBarbarian() || !pTeam->isEverAlive())
			continue;
		teamSeqCache(CIV_EVER_ALIVE).push_back(pTeam);
		if (!pTeam->isAlive())
			continue;
		teamSeqCache(CIV_ALIVE).push_back(pTeam);
		if (pTeam->isMinorCiv())
			continue;
		teamSeqCache(MAJOR_ALIVE).push_back(pTeam);
		if (pTeam->isAVassal())
			teamPerTeamSeqCache(VASSAL_ALIVE, pTeam->getMasterTeam()).push_back(pTeam);
	}
	int const iPlayers = (int)playerSeqCache(ALL).size();
	for (int i = 0; i < iPlayers; i++)
	{
		CvPlayerAI* pPlayer = playerSeqCache(ALL)[i];
		TeamTypes eTeam = pPlayer->getTeam();
		memberSeqCache(MEMBER, eTeam).push_back(pPlayer);
		if (!pPlayer->isEverAlive())
			continue;
		if (!pPlayer->isBarbarian())
			playerSeqCache(CIV_EVER_ALIVE).push_back(pPlayer);
		if (!pPlayer->isAlive())
			continue;
		memberSeqCache(MEMBER_ALIVE, eTeam).push_back(pPlayer);
		if (pPlayer->isBarbarian())
			continue;
		playerSeqCache(CIV_ALIVE).push_back(pPlayer);
		if (pPlayer->isMinorCiv())
			continue;
		playerSeqCache(MAJOR_ALIVE).push_back(pPlayer);
		if (pPlayer->isAVassal())
			memberSeqCache(VASSAL_ALIVE, pPlayer->getMasterTeam()).push_back(pPlayer);
	}
	FAssert(!playerSeqCache(CIV_EVER_ALIVE).empty());
	FAssert(!playerSeqCache(CIV_ALIVE).empty());
	FAssert(!teamSeqCache(CIV_EVER_ALIVE).empty());
	FAssert(!teamSeqCache(CIV_ALIVE).empty());
}

namespace // These functions aren't frequently called; don't need to be fast.
{
	template<class AgentType>
	void eraseFromSeqCache(std::vector<AgentType*>& v, int iAgentID, bool bAssertSuccess = true)
	{
		for (std::vector<AgentType*>::iterator it = v.begin(); it != v.end(); ++it)
		{
			if ((*it)->getID() == iAgentID)
			{
				v.erase(it);
				return;
			}
		}
		FAssert(!bAssertSuccess);
	}

	template<class AgentType>
	void insertIntoVector(std::vector<AgentType*>& v, AgentType* pAgent, bool bAssertSuccess = true)
	{
		int iAgentID = pAgent->getID();
		std::vector<AgentType*>::iterator pos;
		for (pos = v.begin(); pos != v.end(); ++pos)
		{
			int const iPosID = (*pos)->getID();
			FAssert (!bAssertSuccess || iPosID != iAgentID);
			if (iPosID > iAgentID)
				break;
		}
		v.insert(pos, pAgent);
	}
}


void CvAgents::playerDefeated(PlayerTypes eDeadPlayer)
{
	eraseFromSeqCache(playerSeqCache(CIV_ALIVE), eDeadPlayer);
	if (!GET_PLAYER(eDeadPlayer).isMinorCiv())
		eraseFromSeqCache(playerSeqCache(MAJOR_ALIVE), eDeadPlayer);
	TeamTypes eTeam = TEAMID(eDeadPlayer);
	eraseFromSeqCache(memberSeqCache(MEMBER_ALIVE, eTeam), eDeadPlayer);
	TeamTypes eMasterTeam = GET_TEAM(eTeam).getMasterTeam();
	if (eMasterTeam != eTeam)
		eraseFromSeqCache(memberSeqCache(VASSAL_ALIVE, eMasterTeam), eDeadPlayer);
	if (!GET_TEAM(eTeam).isAlive())
	{
		eraseFromSeqCache(teamSeqCache(CIV_ALIVE), eTeam);
		if (!GET_TEAM(eTeam).isMinorCiv())
			eraseFromSeqCache(teamSeqCache(MAJOR_ALIVE), eTeam);
		if (eMasterTeam != eTeam)
			eraseFromSeqCache(teamPerTeamSeqCache(VASSAL_ALIVE, eMasterTeam), eTeam);
	}
}


void CvAgents::playerSetAliveInGame(PlayerTypes ePlayer, bool bRevive)
{
	CvPlayerAI* pPlayer = &GET_PLAYER(ePlayer);
	CvTeamAI* pTeam = &GET_TEAM(ePlayer);
	if (!bRevive)
		insertIntoVector(teamSeqCache(CIV_EVER_ALIVE), pTeam, false);
	insertIntoVector(teamSeqCache(CIV_ALIVE), pTeam);
	insertIntoVector(teamSeqCache(MAJOR_ALIVE), pTeam);
	if (!bRevive)
		insertIntoVector(playerSeqCache(CIV_EVER_ALIVE), pPlayer, false);
	insertIntoVector(playerSeqCache(CIV_ALIVE), pPlayer);
	insertIntoVector(playerSeqCache(MAJOR_ALIVE), pPlayer);
	#ifdef FASSERT_ENABLE
	PlayerVector const& members =
	#endif
	memberSeqCache(MEMBER, pTeam->getID());
	FAssert(std::find(members.begin(), members.end(), pPlayer) != members.end());
	PlayerVector& membersAlive = memberSeqCache(MEMBER_ALIVE, pTeam->getID());
	insertIntoVector(membersAlive, pPlayer);
}


void CvAgents::colonyCreated(PlayerTypes eNewPlayer)
{
	// Normally, players shouldn't be reused; if reuse does occur, call should still succeed.
	playerSetAliveInGame(eNewPlayer, false);
}


void CvAgents::playerRevived(PlayerTypes ePlayer)
{
	playerSetAliveInGame(ePlayer, true);
}


void CvAgents::updateVassal(TeamTypes eVassal, TeamTypes eMaster, bool bVassal)
{
	FAssertBounds(0, playerSeqCache(ALL).size(), eMaster);
	TeamVector& vassalTeams = teamPerTeamSeqCache(VASSAL_ALIVE, eMaster);
	PlayerVector& vassalPlayers = memberSeqCache(VASSAL_ALIVE, eMaster);
	for (size_t i = 0; i < memberSeqCache(MEMBER, eVassal).size(); i++)
	{
		CvPlayerAI* pMember = memberSeqCache(MEMBER, eVassal)[i];
		if (bVassal)
		{	// Members of eVassal may have been defeated at an earlier time
			if (pMember->isAlive())
				insertIntoVector(vassalPlayers, pMember);
		}
		else
		{
			/*  When a vassal dies, playerDefeated removes it from the cache.
				The vassal agreement gets canceled afterwards, resulting in
				a call to updateVassal. */
			if (pMember->isAlive())
				eraseFromSeqCache(vassalPlayers, pMember->getID());
			FAssert(std::find(vassalPlayers.begin(), vassalPlayers.end(), pMember) ==
					vassalPlayers.end());
		}
	}
	CvTeamAI* pVassalTeam = &GET_TEAM(eVassal);
	if (bVassal)
		insertIntoVector(vassalTeams, pVassalTeam);
	else
	{
		if (pVassalTeam->isAlive())
			eraseFromSeqCache(vassalTeams, pVassalTeam->getID());
		FAssert(std::find(vassalTeams.begin(), vassalTeams.end(), pVassalTeam) ==
				vassalTeams.end());
	}
}


#define NO_GENERIC_IMPLEMENTATION() \
	FErrorMsg("No generic implementation"); \
	return NULL

template<class AgentType>
std::vector<AgentType*> const* CvAgents::getAgentSeqCache(AgentSeqCache eCacheID) const
{
	NO_GENERIC_IMPLEMENTATION();
}

template<class AgentType>
std::vector<AgentType*> const* CvAgents::getPerTeamSeqCache(AgentSeqCache eCacheID, TeamTypes) const
{
	NO_GENERIC_IMPLEMENTATION();
}

template<class AgentType>
std::vector<AgentType*> const* CvAgents::getNoAgents() const
{
	NO_GENERIC_IMPLEMENTATION();
}
