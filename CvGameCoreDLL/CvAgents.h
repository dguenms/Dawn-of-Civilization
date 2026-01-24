#pragma once

#ifndef CV_AGENTS_H
#define CV_AGENTS_H

/*  advc.agent: New class for access (via AgentIterator) to sequences of
	agent (CvTeam, CvPlayer) instances. Caches frequently needed sequences. */

class CvPlayerAI;
class CvTeamAI;


class CvAgents
{
public:

	enum AgentSeqCache
	{	// Since the enum is nested in CvAgents, don't repeat the word "AGENT".
		NO_CACHE = -1,
		ALL,
		CIV_EVER_ALIVE,
		CIV_ALIVE,
		MAJOR_ALIVE,
		NUM_STATUS_CACHES,
		MEMBER = NUM_STATUS_CACHES,
		MEMBER_ALIVE,
		VASSAL_ALIVE,
		NUM_CACHES,
		NUM_RELATION_CACHES = NUM_CACHES - NUM_STATUS_CACHES
	};

	/*  To be initialized from CvGame (eventually replacing the initStatics calls
		in CvGlobals::init) */
	CvAgents(int iMaxPlayers, int iMaxTeams);
	void gameStart(bool bFromSaveGame);
	void playerDefeated(PlayerTypes ePlayer);
	void colonyCreated(PlayerTypes eNewPlayer);
	void playerRevived(PlayerTypes ePlayer);
	void teamCapitulated(TeamTypes eVassal, TeamTypes eMaster)
	{
		updateVassal(eVassal, eMaster, true); // sufficient for now
	}
	void voluntaryVassalAgreementSigned(TeamTypes eVassal, TeamTypes eMaster)
	{
		updateVassal(eVassal, eMaster, true);
	}
	void vassalFreed(TeamTypes eVassal, TeamTypes eMaster)
	{
		updateVassal(eVassal, eMaster, false);
	}
	void allianceFormed()
	{
		updateAllCachedSequences();
	}

	// Might be needed in the future
	//void bordersOpened(TeamTypes eFirst, TeamTypes eSecond);
	//void bordersClosed(TeamTypes eFirst, TeamTypes eSecond);
	//void warDeclared(TeamTypes eFirst, TeamTypes eSecond);
	//void peaceMade(TeamTypes eFirst, TeamTypes eSecond);
	//void teamsMet(TeamTypes eFirst, TeamTypes eSecond);
	//void setHuman(PlayerTypes ePlayer, bool bNewValue);

	/*  Tbd.: Remove functions like CvGame::countCivPlayersAlive. AgentIterator::count
		should be used instead. CvAgents could have wrappers for frequently needed counts. */

	// Access to agent vectors from function templates
	template<class AgentType> std::vector<AgentType*> const* getAgentSeqCache(AgentSeqCache eCacheID) const;
	template<class AgentType> std::vector<AgentType*> const* getPerTeamSeqCache(AgentSeqCache eCacheID, TeamTypes) const;
	template<class AgentType> std::vector<AgentType*> const* getNoAgents() const; // Currently unused
	typedef std::vector<CvPlayerAI*> PlayerVector;
	typedef std::vector<CvTeamAI*> TeamVector;
	template<>
	PlayerVector const* getAgentSeqCache<CvPlayerAI>(AgentSeqCache eCacheID) const
	{
		return &playerSeqCache(eCacheID);
	}
	template<>
	PlayerVector const* getPerTeamSeqCache<CvPlayerAI>(AgentSeqCache eCacheID, TeamTypes eTeam) const
	{
		return &memberSeqCache(eCacheID, eTeam);
	}
	template<>
	PlayerVector const* getNoAgents<CvPlayerAI>() const
	{
		return &m_noPlayers;
	}
	template<>
	TeamVector const* getAgentSeqCache<CvTeamAI>(AgentSeqCache eCacheID) const
	{
		return &teamSeqCache(eCacheID);
	}
	template<>
	TeamVector const* getPerTeamSeqCache<CvTeamAI>(AgentSeqCache eCacheID, TeamTypes eTeam) const
	{
		return &teamPerTeamSeqCache(eCacheID, eTeam);
	}
	template<>
	TeamVector const* getNoAgents<CvTeamAI>() const
	{
		return &m_noTeams;
	}


	// For testing (see AgentIteratorTest) and other purposes perhaps ...

	int playerCacheSize(AgentSeqCache eCacheID) const
	{
		FAssertBounds(0, m_playerSeqCache.size(), eCacheID);
		return (int)m_playerSeqCache[eCacheID].size();
	}
	CvPlayerAI& playerCacheAt(AgentSeqCache eCacheID, int iAt) const
	{
		FAssertBounds(0, playerCacheSize(eCacheID), iAt);
		return *m_playerSeqCache[eCacheID][iAt];
	}
	int memberCacheSize(AgentSeqCache eCacheID, TeamTypes eTeam) const
	{
		int const iCache = perTeamCacheIndex(eCacheID);
		FAssertBounds(0, m_memberSeqCache.size(), iCache);
		FAssertBounds(0, m_memberSeqCache[iCache].size(), eTeam);
		return (int)m_memberSeqCache[iCache][eTeam].size();
	}
	CvPlayerAI& memberCacheAt(AgentSeqCache eCacheID, TeamTypes eTeam, int iAt) const
	{
		int const iCache = perTeamCacheIndex(eCacheID);
		FAssertBounds(0, memberCacheSize(eCacheID, eTeam), iAt);
		return *m_memberSeqCache[iCache][eTeam][iAt];
	}
	int teamCacheSize(AgentSeqCache eCacheID) const
	{
		FAssertBounds(0, m_teamSeqCache.size(), eCacheID);
		return (int)m_teamSeqCache[eCacheID].size();
	}
	CvTeamAI& teamCacheAt(AgentSeqCache eCacheID, int iAt) const
	{
		FAssertBounds(0, teamCacheSize(eCacheID), iAt);
		return *m_teamSeqCache[eCacheID][iAt];
	}
	int teamPerTeamCacheSize(AgentSeqCache eCacheID, TeamTypes eTeam) const
	{
		int const iCache = perTeamCacheIndex(eCacheID);
		FAssertBounds(0, m_teamPerTeamSeqCache.size(), iCache);
		FAssertBounds(0, m_teamPerTeamSeqCache[iCache].size(), eTeam);
		return (int)m_teamPerTeamSeqCache[iCache][eTeam].size();
	}
	CvTeamAI& teamPerTeamCacheAt(AgentSeqCache eCacheID, TeamTypes eTeam, int iAt) const
	{
		int const iCache = perTeamCacheIndex(eCacheID);
		FAssertBounds(0, teamPerTeamCacheSize(eCacheID, eTeam), iAt);
		return *m_teamPerTeamSeqCache[iCache][eTeam][iAt];
	}

private:
	/*  Could avoid this mapping by using separate enums for agent status and agent relation caches.
		This would be awkward for AgentIterator though. */
	int perTeamCacheIndex(AgentSeqCache eCacheID) const
	{
		return eCacheID - NUM_STATUS_CACHES;
	}
	PlayerVector& playerSeqCache(AgentSeqCache eCacheID)
	{
		return m_playerSeqCache[eCacheID];
	}
	TeamVector& teamSeqCache(AgentSeqCache eCacheID)
	{
		return m_teamSeqCache[eCacheID];
	}
	PlayerVector& memberSeqCache(AgentSeqCache eCacheID, TeamTypes eTeam)
	{
		return m_memberSeqCache[perTeamCacheIndex(eCacheID)][eTeam];
	}
	TeamVector& teamPerTeamSeqCache(AgentSeqCache eCacheID, TeamTypes eTeam)
	{
		return m_teamPerTeamSeqCache[perTeamCacheIndex(eCacheID)][eTeam];
	}
	// The same with const
	PlayerVector const& playerSeqCache(AgentSeqCache eCacheID) const
	{
		return m_playerSeqCache[eCacheID];
	}
	TeamVector const& teamSeqCache(AgentSeqCache eCacheID) const
	{
		return m_teamSeqCache[eCacheID];
	}
	PlayerVector const& memberSeqCache(AgentSeqCache eCacheID, TeamTypes eTeam) const
	{
		return m_memberSeqCache[perTeamCacheIndex(eCacheID)][eTeam];
	}
	TeamVector const& teamPerTeamSeqCache(AgentSeqCache eCacheID, TeamTypes eTeam) const
	{
		return m_teamPerTeamSeqCache[perTeamCacheIndex(eCacheID)][eTeam];
	}

	void updateAllCachedSequences();
	void updateVassal(TeamTypes eVassal, TeamTypes eMaster, bool bVassal);
	void playerSetAliveInGame(PlayerTypes ePlayer, bool bRevive);

	PlayerVector m_noPlayers; // empty
	TeamVector m_noTeams; // empty

	std::vector<PlayerVector> m_playerSeqCache;
	std::vector<TeamVector> m_teamSeqCache;
	std::vector<std::vector<PlayerVector> > m_memberSeqCache;
	std::vector<std::vector<TeamVector> > m_teamPerTeamSeqCache;
};

#endif
