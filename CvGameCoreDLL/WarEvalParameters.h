#pragma once

#ifndef WAR_EVAL_PARAMETERS_H
#define WAR_EVAL_PARAMETERS_H

class WarUtilityAspect;
class UWAIReport;

/*	For WarEvalParameters::getID.
	(Could go a bit higher with 32 bit, but e.g. 30 civs won't fit.) */
#if MAX_CIV_PLAYERS < 20 && MAX_CIV_TEAMS < 20
	typedef int WarEvalParamID;
#else
	typedef __int64 WarEvalParamID;
#endif

/* advc.104: New class. Parameters that enter into the computation of
   war utility. These parameters need to be passed around quite a bit. */
class WarEvalParameters
{
public:
	WarEvalParameters(TeamTypes eTeam, TeamTypes eTarget, UWAIReport& kReport,
			bool bIgnoreDistraction = false,
			/*	Not clear if it should matter which player makes the deal.
				Can't hurt to store that player id. Can always use its team id
				later if appropriate. */
			PlayerTypes eSponsor = NO_PLAYER,
			TeamTypes eCapitulationTeam = NO_TEAM);
	TeamTypes getAgent() const { return m_eAgent; }
	TeamTypes getTarget() const { return m_eTarget; }
	UWAIReport& getReport() const {return m_kReport; }
	bool isConsideringPeace() const { return m_bConsideringPeace; }
	/*  For evaluating joint wars when the agent is already at war, but the ally
		is not. The agent does then not consider itself (and its vassals) to be
		at peace with the target in the peace scenario. */
	void setNotConsideringPeace() { m_bConsideringPeace = false; }
	bool isIgnoreDistraction() const { return m_bIgnoreDistraction; }
	// For joint wars
	void addWarAlly(TeamTypes eTeam);
	bool isWarAlly(TeamTypes eTeam) const { return (m_warAllies.count(eTeam) > 0); }
	bool isAnyWarAlly() const { return !m_warAllies.empty(); }
	// For peace votes (peace will be assumed in the peace scenario)
	void addExtraTarget(TeamTypes eTeam);
	bool isExtraTarget(TeamTypes eTeam) const { return (m_extraTargets.count(eTeam) > 0); }
	/*  If this returns true, then, in the peace scenario, war should be assumed
		against the main target and peace with the extra targets. Will return
		true only if the ConsideringPeace flag is not set. */
	bool isNoWarVsExtra() const;
	void setSponsor(PlayerTypes ePlayer); // Alternative to constructor arg
	PlayerTypes getSponsor() const { return m_eSponsor; }
	/*	Team we're considering to capitulate to (would-be master);
		NO_TEAM if we're not considering to capitulate. */
	TeamTypes getCapitulationTeam() const { return m_eCapitulationTeam; }
	// Set to true automatically when a sponsor is set
	void setImmediateDoW(bool b) { m_bImmediateDoW = b; }
	bool isImmediateDoW() const { return m_bImmediateDoW; }
	// Perfect hash function for WarEvaluator cache
	WarEvalParamID getID() const;
	// These three should be filled in by WarEvaluator
	void setTotal(bool b) { m_bTotal = b; }
	void setNaval(bool b) { m_bNaval = b; }
	void setPreparationTime(int iTurns) { m_iPreparationTime = iTurns; }
	bool isTotal() const { return m_bTotal; }
	bool isNaval() const { return m_bNaval; }
	int getPreparationTime() const { return m_iPreparationTime; }

private:
	TeamTypes m_eAgent;
	TeamTypes m_eTarget;
	UWAIReport& m_kReport;
	bool m_bConsideringPeace;
	bool m_bIgnoreDistraction;
	std::set<TeamTypes> m_warAllies;
	std::set<TeamTypes> m_extraTargets;
	bool m_bTotal;
	bool m_bNaval;
	int m_iPreparationTime;
	bool m_bImmediateDoW;
	PlayerTypes m_eSponsor;
	TeamTypes m_eCapitulationTeam;
	// Data members added to this class will have to be factored into getID!
};

#endif
