#pragma once

#ifndef WAR_UTILITY_ASPECT_H
#define WAR_UTILITY_ASPECT_H

#include "UWAI.h"
#include "AIStrategies.h"

class MilitaryAnalyst;
class WarEvalParameters;
class UWAIReport;
class UWAI::Player;
class UWAI::Team;
class UWAICache;

/*	advc.104: New class hierarchy. Each class represents an aspect of the
	evaluation of an ongoing or hypothetical war as carried out by an instance
	of the WarEvaluator class. */
class WarUtilityAspect
{
public:
	/*	Returns the computed utility (same as calling the utility accessor
		afterwards). Sets some protected data members that derived classes should
		find useful; concrete derived classes should override evaluate(void) instead. */
	virtual int evaluate(MilitaryAnalyst const& kMilitaryAnalyst);
	char const* aspectName() const;
	int utility() const { return m_iU; }

protected:
	WarUtilityAspect(WarEvalParameters const& kParams);
	// Class to enum mapping
	virtual UWAI::AspectTypes xmlID() const=0;
	// Just for convenience (replacing m_kReport.log)
	void log(char const* fmt, ...) const
	#if DISABLE_UWAI_REPORT
		{}
	#else
		;
	#endif
	/*	What can m_pAgentPlayer gain from or lose to m_pRivalPlayer
		(both set by evaluate(MilitaryAnalyst const&)). Note that m_kRivalPlayer
		is not necessarily a war enemy of the m_kAgentPlayer; it can be
		any rival that is directly or indirectly affected by the evaluated war.
		Computed from the pov of the agent.
		After computing the aspect utility, derived classes should add
		(not assign!) their result to WarUtilityAspect::m_iU */
	virtual void evaluate()=0;
	/*	Pre-computations not specific to a particular rival player.
		Most derived classes shouldn't need this.
		If (partial) war utility is computed, it should be returned (otherwise 0).
		This function should not modify WarUtilityAspect::m_iU. */
	virtual int preEvaluate();
	// See WarUtilityBroaderAspect. Concrete derived classes shouldn't overwrite this.
	virtual bool concernsOnlyWarParties() const;

	/*	Caveat: The order of declaration here determines the order
		of initialization in the constructor. Improper order will
		result in faulty initialization, and, for lack of a WReorder option,
		the compiler won't warn about it. */
	WarEvalParameters const& m_kParams;
	int m_iU;
	mutable UWAIReport& m_kReport;
	CvGameAI const& m_kGame;
	EraTypes const m_eGameEra;
	scaled const m_rGameEraAIFactor;
	CvGameSpeedInfo const& m_kSpeed;

	// To be called by derived classes only from evaluate or preEvaluate.
	// Eval helpers - start
	// Between the agent team and eOther - or m_kRivalTeam if eOther=NO_TEAM.
	scaled normalizeUtility(scaled rUtilityTeamOnTeam, TeamTypes eOther = NO_TEAM) const;
	/*	Score for assets of m_pRivalPlayer gained from and/or lost to eTo,
		or to any player (eTo=NO_PLAYER). If eIgnoreGainsFrom is used, then assets
		gained from that team are ignored.
		Always computed based on the agent's knowledge.
		The score total for all of the rival's present assets (lost or not)
		can be obtained by passing a scaled pointer.
		(Shouldn't call totalAssetScore() on the rival cache instead b/c that
		includes data about cities that the agent may not know of.)
		Update: Now also subtracts score for assets conquered by them from eTo
		(or from any player); i.e. calculates a net loss (or gain) of assets.
		Gains from team eIgnoreGains aren't counted. */
	 scaled netLostRivalAssetScore(PlayerTypes eTo = NO_PLAYER,
			scaled* prTotalScore = NULL, // out-param
			TeamTypes eIgnoreGainsFrom = NO_TEAM) const;
	 scaled lossesFromBlockade(PlayerTypes eVictim, PlayerTypes eTo) const;
	 scaled lossesFromNukes(PlayerTypes eVictim, PlayerTypes eSource) const;
	 // <advc.035>
	 scaled lossesFromFlippedTiles(PlayerTypes eVictim,
			PlayerTypes eTo = NO_PLAYER) const; // </advc.035>
	 /* Score for assets conquered by the agent player from the rival player
		(as set by evaluate(void)). bMute disables logging within the function body. */
	 scaled conqAssetScore(bool bMute = true) const;
	 // Portion of cities of ePlayer that aren't lost in the war
	 scaled remainingCityRatio(PlayerTypes ePlayer) const; 
	 template<bool bCHECK_HAS_MET>
	 int countFreeRivals() const
	 {
		 return PlayerIter<FREE_MAJOR_CIV, bCHECK_HAS_MET ?
				KNOWN_POTENTIAL_ENEMY_OF : POTENTIAL_ENEMY_OF>::
				count(m_kAgentTeam.getID());
	 }
	/*	Evaluation of m_pRivalPlayer's usefulness as m_pAgentPlayer's trade partner.
		Would prefer this to be computed just once by UWAICache (the computations
		aren't totally cheap), but I also want the log output. They're not called
		frequently. */
	scaled partnerUtilFromTech() const;
	scaled partnerUtilFromTrade() const;
	scaled partnerUtilFromMilitary() const;
	// Eval helpers - end

	/*	Must not call these functions until evaluate(MilitaryAnalyst const&)
		has been called ... */
	MilitaryAnalyst const& militAnalyst() const { return *m_pMilitaryAnalyst; }
	/*	For brevity, these function names refer to the agent as "we"/ "us"
		and to the rival player as "them". */
	UWAICache const& ourCache() const { return *m_pAgentCache; }
	std::vector<PlotNumTypes> const& ourConquestsFromThem() const
	{
		return m_aeAgentConquersFromRival;
	}
	// Agent player's current attitude toward the rival player and vice versa
	AttitudeTypes towardThem() const { return m_eTowardRival; }
	AttitudeTypes towardUs() const { return m_eTowardAgent; }
	int diploTowardThem() const { return m_iDiploTowardRival; }
	int diploTowardUs() const { return m_iDiploTowardAgent; }
	/*	These three get wrapped into briefer macros (see implementation file)
		and shouldn't be used directly */
	CvTeamAI const& getAgentTeam() const { return m_kAgentTeam; }
	CvPlayerAI const& getAgentPlayer() const { return *m_pAgentPlayer; }
	CvPlayerAI const& getRivalPlayer() const { return *m_pRivalPlayer; }

private:
	/*	These data members should be accessed through protected functions and
		macros (defined in the implementation file) ... */
	CvTeamAI const& m_kAgentTeam;
	CvPlayerAI const* m_pAgentPlayer;
	CvPlayerAI const* m_pRivalPlayer;
	MilitaryAnalyst const* m_pMilitaryAnalyst;
	UWAICache const* m_pAgentCache;
	std::vector<PlotNumTypes> m_aeAgentConquersFromRival;
	AttitudeTypes m_eTowardRival, m_eTowardAgent;
	int m_iDiploTowardRival, m_iDiploTowardAgent; // Relations values

	int evaluate(PlayerTypes ePlayer);
	AttitudeTypes techRefuseThresh(PlayerTypes ePlayer) const;
	// In between evaluate calls ...
	void reset();
	void resetRival();
};

/*	Not a nice name. Derive from this class rather than WarUtilityAspect
	if evaluate(void) should be called also for parties that aren't part of the
	military analysis. */
class WarUtilityBroaderAspect : public WarUtilityAspect
{
protected:
	WarUtilityBroaderAspect(WarEvalParameters const& kParams)
	:	WarUtilityAspect(kParams) {}
	bool concernsOnlyWarParties() const { return false; } // virtual
};


class GreedForAssets : public WarUtilityAspect
{
public:
	GreedForAssets(WarEvalParameters const& kParams)
	:	WarUtilityAspect(kParams) {}
	void evaluate();
	UWAI::AspectTypes xmlID() const { return UWAI::GREED_FOR_ASSETS; }
private:
	scaled overextensionMult() const;
	scaled defensibilityMult() const;
	scaled medianDistFromOurConquests(PlayerTypes ePlayer) const;
	scaled threatToCities(PlayerTypes ePlayer, scaled rRemoteness) const;
	scaled competitionMultiplier() const;
	scaled teamSizeMultiplier() const;	
};


class GreedForVassals : public WarUtilityAspect
{
public:
	GreedForVassals(WarEvalParameters const& kParams)
	:	WarUtilityAspect(kParams) {}
	void evaluate();
	UWAI::AspectTypes xmlID() const { return UWAI::GREED_FOR_VASSALS; }
};


class GreedForSpace : public WarUtilityAspect
{
public:
	GreedForSpace(WarEvalParameters const& kParams)
	:	WarUtilityAspect(kParams) {}
	void evaluate();
	UWAI::AspectTypes xmlID() const { return UWAI::GREED_FOR_SPACE; }
};


class GreedForCash : public WarUtilityAspect
{
public:
	GreedForCash(WarEvalParameters const& kParams)
	:	WarUtilityAspect(kParams) {}
	void evaluate();
	UWAI::AspectTypes xmlID() const { return UWAI::GREED_FOR_CASH; }
};


class Loathing : public WarUtilityAspect
{
public:
	Loathing(WarEvalParameters const& kParams)
	:	WarUtilityAspect(kParams) {}
	void evaluate();
	UWAI::AspectTypes xmlID() const { return UWAI::LOATHING; }
private:
	scaled lossRating() const;
};


class MilitaryVictory : public WarUtilityAspect
{
public:
	MilitaryVictory(WarEvalParameters const& kParams)
	:	WarUtilityAspect(kParams), m_iVotesToGo(-1), m_bEnoughVotes(false) {}
	int preEvaluate();
	void evaluate();
	UWAI::AspectTypes xmlID() const { return UWAI::MILITARY_VICTORY; }
private:
	int m_iVotesToGo;
	bool m_bEnoughVotes;
	scaled progressRatingConquest() const;
	scaled progressRatingDomination() const;
	scaled progressRatingDiplomacy() const;
	void addConquestsByPartner(std::map<PlotNumTypes,scaled>& kWeightedConquests,
			AttitudeTypes eAttitudeThresh, scaled rWeight) const;
};


class Assistance : public WarUtilityAspect
{
public:
	Assistance(WarEvalParameters const& kParams)
	:	WarUtilityAspect(kParams) {}
	void evaluate();
	UWAI::AspectTypes xmlID() const { return UWAI::PRESERVATION_OF_PARTNERS; }
private:
	scaled assistanceRatio() const;
};


class Reconquista : public WarUtilityAspect
{
public:
	Reconquista(WarEvalParameters const& kParams)
		:	WarUtilityAspect(kParams) {}
	void evaluate();
	UWAI::AspectTypes xmlID() const { return UWAI::RECONQUISTA; }
};


class Rebuke : public WarUtilityAspect
{
public:
	Rebuke(WarEvalParameters const& kParams)
	:	WarUtilityAspect(kParams) {}
	void evaluate();
	UWAI::AspectTypes xmlID() const { return UWAI::REBUKE; }
};


class Fidelity : public WarUtilityAspect
{
public:
	Fidelity(WarEvalParameters const& kParams)
	:	WarUtilityAspect(kParams) {}
	void evaluate();
	UWAI::AspectTypes xmlID() const { return UWAI::FIDELITY; }
};


class HiredHand : public WarUtilityAspect
{
public:
	HiredHand(WarEvalParameters const& kParams)
	:	WarUtilityAspect(kParams) {}
	void evaluate();
	UWAI::AspectTypes xmlID() const { return UWAI::HIRED_HAND; }
private:
	scaled eval(PlayerTypes eAlly, int iOriginalUtility, int iObligationThresh) const;
};


class BorderDisputes : public WarUtilityAspect
{
public:
	BorderDisputes(WarEvalParameters const& kParams)
	:	WarUtilityAspect(kParams) {}
	void evaluate();
	UWAI::AspectTypes xmlID() const { return UWAI::BORDER_DISPUTES; }
};


class SuckingUp : public WarUtilityAspect
{
public:
	SuckingUp(WarEvalParameters const& kParams)
	:	WarUtilityAspect(kParams) {}
	void evaluate();
	UWAI::AspectTypes xmlID() const { return UWAI::SUCKING_UP; }
};


class PreEmptiveWar : public WarUtilityBroaderAspect
{
public:
	PreEmptiveWar(WarEvalParameters const& kParams)
	:	WarUtilityBroaderAspect(kParams) {}
	void evaluate();
	UWAI::AspectTypes xmlID() const { return UWAI::PREEMPTIVE_WAR; }
};


class KingMaking : public WarUtilityBroaderAspect
{
public:
	KingMaking(WarEvalParameters const& kParams)
	:	WarUtilityBroaderAspect(kParams) {}
	int preEvaluate();
	void evaluate();
	UWAI::AspectTypes xmlID() const { return UWAI::KING_MAKING; }
private:
	static scaled const m_rScoreMargin;
	std::set<PlayerTypes> m_winningFuture;
	std::set<PlayerTypes> m_winningPresent;
	void addWinning(std::set<PlayerTypes>& kWinning, bool bPredict) const;
	bool anyVictory(PlayerTypes ePlayer, AIVictoryStage eFlags, int iStage,
			bool bPredict = true) const;
	void addLeadingPlayers(std::set<PlayerTypes>& kLeading, scaled rMargin,
			bool bPredict = true) const;
	scaled theirRelativeLoss() const;
};


class Effort : public WarUtilityAspect
{
public:
	Effort(WarEvalParameters const& kParams)
	:	WarUtilityAspect(kParams) {}
	int preEvaluate();
	void evaluate();
	UWAI::AspectTypes xmlID() const { return UWAI::EFFORT; }
};


class Risk : public WarUtilityAspect
{
public:
	Risk(WarEvalParameters const& kParams)
	:	WarUtilityAspect(kParams) {}
	int preEvaluate();
	void evaluate();
	UWAI::AspectTypes xmlID() const { return UWAI::RISK; }
};


class IllWill : public WarUtilityBroaderAspect
{
public:
	IllWill(WarEvalParameters const& kParams)
	:	WarUtilityBroaderAspect(kParams) {}
	int preEvaluate();
	void evaluate();
	UWAI::AspectTypes xmlID() const { return UWAI::ILL_WILL; }
private:
	scaled m_rCost; // For use by subroutines (instead of m_iU)
	scaled m_rAltPartnerFactor;
	void evalLostPartner();
	void evalRevenge();
	scaled theirToOurPowerRatio() const;
	void evalAngeredPartners();
	scaled nukeCost(scaled rCitiesWeNuked) const;
};


class Affection : public WarUtilityAspect
{
public:
	Affection(WarEvalParameters const& kParams);
	void evaluate();
	UWAI::AspectTypes xmlID() const { return UWAI::AFFECTION; }
private:
	scaled m_rGameProgressFactor;
};


class Distraction : public WarUtilityAspect
{
public:
	Distraction(WarEvalParameters const& kParams)
	:	WarUtilityAspect(kParams) {}
	void evaluate();
	UWAI::AspectTypes xmlID() const { return UWAI::DISTRACTION; }
};


class PublicOpposition : public WarUtilityAspect
{
public:
	PublicOpposition(WarEvalParameters const& kParams)
	:	WarUtilityAspect(kParams) {}
	void evaluate();
	UWAI::AspectTypes xmlID() const { return UWAI::PUBLIC_OPPOSITION; }
};


class Revolts : public WarUtilityAspect
{
public:
	Revolts(WarEvalParameters const& kParams)
	:	WarUtilityAspect(kParams) {}
	void evaluate();
	UWAI::AspectTypes xmlID() const { return UWAI::REVOLTS; }
private:
	std::set<PlotNumTypes> m_countedCities;
};

// BroaderAspect: Need to cover the sponsor, which may not be a war party.
class UlteriorMotives : public WarUtilityBroaderAspect
{
public:
	UlteriorMotives(WarEvalParameters const& kParams)
	:	WarUtilityBroaderAspect(kParams) {}
	void evaluate();
	UWAI::AspectTypes xmlID() const { return UWAI::ULTERIOR_MOTIVES; }
};


class FairPlay : public WarUtilityAspect
{
public:
	FairPlay(WarEvalParameters const& kParams)
	:	WarUtilityAspect(kParams) {}
	void evaluate();
	UWAI::AspectTypes xmlID() const { return UWAI::FAIR_PLAY; }
private:
	int initialMilitaryUnits(PlayerTypes ePlayer) const;
};


class Bellicosity : public WarUtilityAspect
{
public:
	Bellicosity(WarEvalParameters const& kParams)
	:	WarUtilityAspect(kParams) {}
	void evaluate();
	UWAI::AspectTypes xmlID() const { return UWAI::BELLICOSITY; }
};


class TacticalSituation : public WarUtilityAspect
{
public:
	TacticalSituation(WarEvalParameters const& kParams)
	:	WarUtilityAspect(kParams) {}
	void evaluate();
	UWAI::AspectTypes xmlID() const { return UWAI::TACTICAL_SITUATION; }
private:
	void evalEngagement();
	void evalOperational();
	int evacPop(PlayerTypes eOwner, PlayerTypes eInvader) const;
};


class LoveOfPeace : public WarUtilityAspect
{
public:
	LoveOfPeace(WarEvalParameters const& kParams)
	:	WarUtilityAspect(kParams) {}
	void evaluate();
	UWAI::AspectTypes xmlID() const { return UWAI::LOVE_OF_PEACE; }
};

class ThirdPartyIntervention : public WarUtilityBroaderAspect
{
public:
	ThirdPartyIntervention(WarEvalParameters const& kParams)
	:	WarUtilityBroaderAspect(kParams) {}
	int preEvaluate();
	void evaluate();
	UWAI::AspectTypes xmlID() const { return UWAI::THIRD_PARTY_INTERVENTION; }
private:
	scaled m_rDefPow;
	scaled m_rLostDefPowRatio;
};

class DramaticArc : public WarUtilityAspect
{
public:
	DramaticArc(WarEvalParameters const& kParams)
	:	WarUtilityAspect(kParams) {}
	int preEvaluate();
	void evaluate();
	UWAI::AspectTypes xmlID() const { return UWAI::DRAMATIC_ARC; }
private:
	scaled m_rTensionIncrease;
};

#endif
