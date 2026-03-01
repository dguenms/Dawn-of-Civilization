/*	advc.agent: Test code for the AgentIterator class.
	Only speed tests (profiling) at this point. */

#include "CvGameCoreDLL.h"
#include "CvAgents.h"
#include "CoreAI.h"

//#define AGENT_ITERATOR_TEST

#ifdef AGENT_ITERATOR_TEST
#include "TSCProfiler.h"
#endif

/*  To be called once the agent sequence cache at CvAgents is updated at game start
	or after loading a savegame.
	The caller should use the return value in some way; just to make sure that the
	compiler doesn't somehow skip the function call or the computation of the
	return value in the function body. */
int TestAgentIterator(int iSamples = 1)
{
	int r = 0;
#ifdef AGENT_ITERATOR_TEST
	/*  Caveat: Running all these tests in succession seems to lead to
		some inaccuracies in the time measurements; maybe due to the
		profiling code; or some other side-effect. */
	TeamTypes eTeam = (TeamTypes)1;
	for (int iSample = 0; iSample < iSamples; iSample++)
	{
		{
			TSC_PROFILE("MAJOR_CIV TeamIter");
			for (TeamIter<MAJOR_CIV> it; it.hasNext(); ++it)
			{
				CvTeam& kTeam = *it;
				r += kTeam.getID();
			}
		}
		{
			TSC_PROFILE("MAJOR_CIV MAX_CIV_TEAMS");
			for (int i = 0; i < MAX_CIV_TEAMS; i++)
			{
				CvTeam& kTeam = GET_TEAM((TeamTypes)i);
				if (!kTeam.isAlive() || kTeam.isMinorCiv())
					continue;
				r += kTeam.getID();
			}
		}
		{
			TSC_PROFILE("MAJOR_CIV vector<CvTeamAI*>");
			CvAgents const& kAgents = GC.getAgents();
			for (int i = 0; i < kAgents.teamCacheSize(CvAgents::MAJOR_ALIVE); i++)
			{
				CvTeam& kTeam = kAgents.teamCacheAt(CvAgents::MAJOR_ALIVE, i);
				r += kTeam.getID();
			}
		}

		{
			TSC_PROFILE("NON_BARBARIAN PlayerIter");
			for (PlayerIter<CIV_ALIVE> it; it.hasNext(); ++it)
			{
				CvPlayer const& kPlayer = *it;
				r += kPlayer.getID();
			}
		}
		{
			TSC_PROFILE("NON_BARBARIAN MAX_CIV_PLAYERS");
			for (int i = 0; i < MAX_CIV_PLAYERS; i++)
			{
				CvPlayer const& kPlayer = GET_PLAYER((PlayerTypes)i);
				if (!kPlayer.isAlive())
					continue;
				r += kPlayer.getID();
			}
		}
		{
			TSC_PROFILE("NON_BARBARIAN vector<CvPlayerAI*>");
			CvAgents const& kAgents = GC.getAgents();
			for (int i = 0; i < kAgents.playerCacheSize(CvAgents::CIV_ALIVE); i++)
			{
				CvPlayer const& kPlayer = kAgents.playerCacheAt(CvAgents::CIV_ALIVE, i);
				r += kPlayer.getID();
			}
		}

		{
			TSC_PROFILE("ALIVE PlayerIter");
			for (PlayerIter<ALIVE> it; it.hasNext(); ++it)
			{
				CvPlayer const& kPlayer = *it;
				r += kPlayer.getID();
			}
		}
		{
			TSC_PROFILE("ALIVE MAX_PLAYERS");
			for (int i = 0; i < MAX_PLAYERS; i++)
			{
				CvPlayer const& kPlayer = GET_PLAYER((PlayerTypes)i);
				if (!kPlayer.isAlive())
					continue;
				r += kPlayer.getID();
			}
		}
		{
			TSC_PROFILE("ALIVE vector<CvPlayerAI*>");
			CvAgents const& kAgents = GC.getAgents();
			for (int i = 0; i < kAgents.playerCacheSize(CvAgents::CIV_ALIVE); i++)
			{
				CvPlayer const& kPlayer = kAgents.playerCacheAt(CvAgents::CIV_ALIVE, i);
				r += kPlayer.getID();
			}
			r += GET_PLAYER(BARBARIAN_PLAYER).getID();
		}

		{
			TSC_PROFILE("FREE_MAJOR TeamIter");
			for (TeamIter<FREE_MAJOR_CIV> it; it.hasNext(); ++it)
			{
				CvTeam& kTeam = *it;
				r += kTeam.getID();
			}
		}
		{
			TSC_PROFILE("FREE_MAJOR MAX_CIV_TEAMS");
			for (int i = 0; i < MAX_CIV_TEAMS; i++)
			{
				CvTeam& kTeam = GET_TEAM((TeamTypes)i);
				if (!kTeam.isAlive() || kTeam.isMinorCiv() || kTeam.isAVassal())
					continue;
				r += kTeam.getID();
			}
		}
		{
			TSC_PROFILE("FREE_MAJOR vector<CvTeamAI*>");
			CvAgents const& kAgents = GC.getAgents();
			for (int i = 0; i < kAgents.teamCacheSize(CvAgents::MAJOR_ALIVE); i++)
			{
				CvTeam& kTeam = kAgents.teamCacheAt(CvAgents::MAJOR_ALIVE, i);
				if (kTeam.isAVassal())
					continue;
				r += kTeam.getID();
			}
		}

		{
			TSC_PROFILE("Members MemberIter");
			for (MemberIter<> it(eTeam); it.hasNext(); ++it)
			{
				CvPlayerAI const& kPlayer = *it;
				r += kPlayer.getID();
			}
		}
		{
			TSC_PROFILE("Members MAX_CIV_PLAYERS");
			for (int i = 0; i < MAX_CIV_PLAYERS; i++)
			{
				CvPlayerAI const& kPlayer = GET_PLAYER((PlayerTypes)i);
				if (!kPlayer.isAlive() || kPlayer.getTeam() != 1)
					continue;
				r += kPlayer.getID();
			}
		}
		{
			TSC_PROFILE("Members vector<CvPlayerAI*>");
			CvAgents const& kAgents = GC.getAgents();
			for (int i = 0; i < kAgents.memberCacheSize(CvAgents::MEMBER_ALIVE, eTeam); i++)
			{
				CvPlayerAI const& kPlayer = kAgents.memberCacheAt(CvAgents::MEMBER_ALIVE, eTeam, i);
				r += kPlayer.getID();
			}
		}

		/*{
			TSC_PROFILE("ANY_AGENT_STATUS PlayerIter");
			for (PlayerIter<ANY_AGENT_STATUS> it; it.hasNext(); ++it)
			{
				CvPlayerAI& kPlayer = *it;
				r += kPlayer.getID();
			}
		}
		{
			TSC_PROFILE("EVER_ALIVE PlayerIter");
			for (PlayerIter<EVER_ALIVE> it; it.hasNext(); ++it)
			{
				CvPlayer const& kPlayer = *it;
				r += kPlayer.getID();
			}
		}
		{
			TSC_PROFILE("FREE_MAJOR_AI PlayerIter");
			for (PlayerIter<FREE_MAJOR_AI> it; it.hasNext(); ++it)
			{
				CvPlayer const& kPlayer = *it;
				r += kPlayer.getID();
			}
		}
		{
			TSC_PROFILE("HUMAN PlayerIter");
			for (PlayerIter<HUMAN> it; it.hasNext(); ++it)
			{
				CvPlayer const& kPlayer = *it;
				r += kPlayer.getID();
			}
		}

		{
			TSC_PROFILE("NOT_SAME_TEAM_AS PlayerIter");
			for (PlayerIter<ALIVE,NOT_SAME_TEAM_AS> it(eTeam); it.hasNext(); ++it)
			{
				CvPlayer const& kPlayer = *it;
				r += kPlayer.getID();
			}
		}
		{
			TSC_PROFILE("VASSAL_OF PlayerIter");
			for (PlayerIter<ALIVE,VASSAL_OF> it(eTeam); it.hasNext(); ++it)
			{
				CvPlayer const& kPlayer = *it;
				r += kPlayer.getID();
			}
		}
		{
			TSC_PROFILE("NOT_A_RIVAL_OF PlayerIter");
			for (PlayerIter<ALIVE,NOT_A_RIVAL_OF> it(eTeam); it.hasNext(); ++it)
			{
				CvPlayer const& kPlayer = *it;
				r += kPlayer.getID();
			}
		}
		{
			TSC_PROFILE("HUMAN ENEMY PlayerIter");
			for (PlayerIter<HUMAN,ENEMY_OF> it(BARBARIAN_TEAM); it.hasNext(); ++it)
			{
				CvPlayer const& kPlayer = *it;
				r += kPlayer.getID();
			}
		}*/
	}
#endif
	return r;
}
