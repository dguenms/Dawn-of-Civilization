#pragma once

#ifndef MILITARY_ANALYST_H
#define MILITARY_ANALYST_H

#include "MilitaryBranch.h"
#include "UWAISets.h"

class InvasionGraph;
class WarEvalParameters;
class UWAIReport;
class InvasionGraph;

/*  advc.104: New class. Handles the military assessment of a war between
	two teams (agent, target) from the pov of a particular member of the agent team.
	The analysis considers the present situation, but, more so, the
	medium-term prospects (~25 turns).
	The computations happen in the constructor, meaning that all other
	public functions are for accessing the results. */
class MilitaryAnalyst
{
public:
	/*	bPeaceScenario=false - "war" scenario:
		War against the target is assumed to be declared immediately or,
		depending on the war eval parameters, after some preparation time,
		or war is continued (if already at war).
		bPeaceScenario=true - "peace" scenario:
		No war is declared or, if agent and target are at war, the war
		is ended immediately. */
	MilitaryAnalyst(PlayerTypes eAgentPlayer, WarEvalParameters& kWarEvalParams,
			bool bPeaceScenario);
	~MilitaryAnalyst();
	WarEvalParameters& evaluationParams() { return m_kWarEvalParams; }
	WarEvalParameters const& evaluationParams() const { return m_kWarEvalParams; }
	PlayerTypes getAgentPlayer() const { return m_eWe; }
	bool isPeaceScenario() const { return m_bPeaceScenario; }

	bool isOnOurSide(TeamTypes eTeam) const;
	/*  The parameter only refers to proper defensive pacts;
		vassal-master is always checked. */
	bool isOnTheirSide(TeamTypes eTeam, bool bDefensivePacts = false) const;
	bool isEliminated(PlayerTypes ePlayer) const;
	bool hasCapitulated(TeamTypes ePlayer) const;
	// From units lost at war
	scaled lostPower(PlayerTypes ePlayer, MilitaryBranchTypes eBranch) const;
	// Net gain, i.e. build-up minus losses; can be negative.
	scaled gainedPower(PlayerTypes ePlayer, MilitaryBranchTypes eBranch) const;
	// Production invested in military build-up
	scaled militaryProduction(PlayerTypes ePlayer) const;
	TeamSet const& getCapitulationsAccepted(TeamTypes eMaster) const
	{
		FAssertBounds(0, MAX_CIV_TEAMS, eMaster);
		return m_capitulationsAcceptedPerTeam[eMaster];
	}
	scaled getNukedCities(PlayerTypes eNukeOwner, PlayerTypes eCityOwner) const
	{
		FAssertBounds(0, MAX_CIV_PLAYERS, eNukeOwner);
		FAssertBounds(0, MAX_CIV_PLAYERS, eCityOwner);
		return m_nukedCities[eNukeOwner][eCityOwner];
	}
	bool isWar(PlayerTypes eFirst, PlayerTypes eSecond) const // After simulated DoWs
	{
		FAssertBounds(0, MAX_CIV_PLAYERS, eFirst);
		FAssertBounds(0, MAX_CIV_PLAYERS, eSecond);
		return m_warTable[eFirst][eSecond];
	}
	bool isWar(TeamTypes eFirst, TeamTypes eSecond) const;
	// Prep. time, if any, plus time horizon
	int turnsSimulated() const { return m_iTurnsSimulated; }
	// Does ePlayer have a node in the InvasionGraph?
	bool isPartOfAnalysis(PlayerTypes ePlayer) const
	{
		return (m_partOfAnalysis.count(ePlayer) > 0);
	}
	void logResults(PlayerTypes ePlayer); // for debugging
	// (There's another public and private section below)
private:
	PlayerTypes m_eWe;
	WarEvalParameters& m_kWarEvalParams;
	TeamTypes m_eTarget;
	UWAIReport& m_kReport;
	bool m_bPeaceScenario;

	InvasionGraph* m_pInvGraph;
	int m_iTurnsSimulated;

	std::vector<TeamSet> m_capitulationsAcceptedPerTeam;
	PlyrSet m_partOfAnalysis;
	std::vector<std::vector<bool> > m_warTable;
	std::vector<std::vector<scaled> > m_nukedCities;

	class PlayerResult // Per-player results of analysis
	{
	public:
		PlayerResult() : m_rGameScore(-1) {}
		void setGameScore(scaled rScore) { m_rGameScore = rScore; }
		scaled getGameScore() const { return m_rGameScore; }
		void addNukesSuffered(scaled rNukes) { m_rNukesSuffered += rNukes; }
		scaled getNukesSuffered() const { return m_rNukesSuffered; }
		void addNukesFired(scaled rNukes) { m_rNukesFired += rNukes; }
		scaled getNukesFired() const { return m_rNukesFired; }
		void setDoWOn(PlayerTypes eAggressor) { m_DoWOn.insert(eAggressor); }
		void setDoWOn(PlyrSetIter const& itFirst, PlyrSetIter const& itLast)
		{
			m_DoWOn.insert(itFirst, itLast);
		}
		PlyrSet const& getDoWOn() const { return m_DoWOn; }
		void setDoWBy(PlayerTypes eTarget) { m_DoWBy.insert(eTarget); }
		void setDoWBy(PlyrSetIter const& itFirst, PlyrSetIter const& itLast)
		{
			m_DoWBy.insert(itFirst, itLast);
		}
		PlyrSet const& getDoWBy() const { return m_DoWBy; }
		void setWarContinued(PlayerTypes eEnemy) { m_warsCont.insert(eEnemy); }
		PlyrSet const& getWarsContinued() const { return m_warsCont; }
		void setCityLost(PlotNumTypes eCityPlot) { m_lostCities.insert(eCityPlot); }
		CitySet const& getLostCities() const { return m_lostCities; }
		CitySet& getLostCities() { return m_lostCities; }
		void setCityConquered(PlotNumTypes eCityPlot) { m_conqueredCities.insert(eCityPlot); }
		CitySet const& getConqueredCities() const { return m_conqueredCities; }
		CitySet& getConqueredCities() { return m_conqueredCities; }
	private:
		scaled m_rGameScore;
		scaled m_rNukesSuffered;
		scaled m_rNukesFired;
		PlyrSet m_DoWOn;
		PlyrSet m_DoWBy;
		PlyrSet m_warsCont;
		CitySet m_lostCities;
		CitySet m_conqueredCities;
	};
	std::vector<PlayerResult*> m_playerResults;
	static CitySet m_emptyCitySet;
	static PlyrSet m_emptyPlayerSet;
	PlayerResult& playerResult(PlayerTypes ePlayer);
// (There's another private section below)
public:
	CitySet const& lostCities(PlayerTypes eOldOwner) const
	{
		FAssertBounds(0, MAX_CIV_PLAYERS, eOldOwner);
		PlayerResult* pR = m_playerResults[eOldOwner];
		return (pR == NULL ? m_emptyCitySet : pR->getLostCities());
	}
	CitySet const& conqueredCities(PlayerTypes eNewOwner) const
	{
		FAssertBounds(0, MAX_CIV_PLAYERS, eNewOwner);
		PlayerResult* pR = m_playerResults[eNewOwner];
		return (pR == NULL ? m_emptyCitySet : pR->getConqueredCities());
	}
	/*  Only for the war scenario. No DoW are anticipated in the peace scenario;
		will return false then. */
	PlyrSet const& getWarsDeclaredBy(PlayerTypes eAggressor) const
	{
		 FAssertBounds(0, MAX_CIV_PLAYERS, eAggressor);
		 PlayerResult* pR = m_playerResults[eAggressor];
		 return (pR == NULL ? m_emptyPlayerSet : pR->getDoWBy());
	}
	PlyrSet const& getWarsDeclaredOn(PlayerTypes eTarget) const
	{
		 FAssertBounds(0, MAX_CIV_PLAYERS, eTarget);
		 PlayerResult* pR = m_playerResults[eTarget];
		 return (pR == NULL ? m_emptyPlayerSet : pR->getDoWOn());
	}
	// Empty unless considering peace
	PlyrSet const& getWarsContinued(PlayerTypes ePlayer) const
	{
		FAssertBounds(0, MAX_CIV_PLAYERS, ePlayer);
		PlayerResult* pR = m_playerResults[ePlayer];
		return (pR == NULL ? m_emptyPlayerSet : pR->getWarsContinued());
	}
	/*	Only those that aren't expected to be intercepted.
		Fired by someone (shouldn't matter who). */
	scaled getNukesSufferedBy(PlayerTypes ePlayer) const
	{
		FAssertBounds(0, MAX_CIV_PLAYERS, ePlayer);
		PlayerResult* pR = m_playerResults[ePlayer];
		return (pR == NULL ? 0 : pR->getNukesSuffered());
	}
	scaled getNukesFiredBy(PlayerTypes ePlayer) const
	{
		FAssertBounds(0, MAX_CIV_PLAYERS, ePlayer);
		PlayerResult* pR = m_playerResults[ePlayer];
		return (pR == NULL ? 0 : pR->getNukesFired());
	}
	// Based on conquered and lost cities
	scaled predictedGameScore(PlayerTypes ePlayer) const;
private:
	// True if we are preparing war against ePlayer or considering a war plan
	bool doWePlanToDeclWar(PlayerTypes ePlayer) const;
	void prepareResults();
	void simulateNuclearWar();
	/*  Also checks vassal agreements, including other vassals of
		the same master. */
	bool isDefactoDefensivePact(TeamTypes eFirst, TeamTypes eSecond) const;
	// Logs either conquests or losses
	void logCities(PlayerTypes ePlayer, bool bConquests);
	// Logs either gained or lost power
	void logPower(PlayerTypes ePlayer, bool bGains);
	void logCapitulations(PlayerTypes ePlayer);
	// Wars declared on and by (the team of) ePlayer
	void logDoW(PlayerTypes ePlayer);
};

#endif
