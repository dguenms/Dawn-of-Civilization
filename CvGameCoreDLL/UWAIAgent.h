#pragma once

#ifndef UWAI_AGENT_H
#define UWAI_AGENT_H

// advc.104: See comment at the start of UWAI.h

#include "UWAI.h"
#include "UWAICache.h"

class FDataStreamBase;
class UWAIReport;

// This class makes decisions about war and peace at the level of CvTeams
class UWAI::Team
{
public:
	Team();
	~Team();
	// See UWAICache.h about the call order during initialization
	void init(TeamTypes eTeam);
	void write(FDataStreamBase* pStream) const;
	void read(FDataStreamBase* pStream);
	void addTeam(PlayerTypes eOtherLeader); // When forming a Permanent Alliance
	void reportWarEnding(TeamTypes eEnemy,
			CLinkList<TradeData> const* pWeReceive = NULL,
			CLinkList<TradeData> const* pWeGive = NULL);
	void turnPre();
	void doWar(); // replacement for CvTeamAI::doWar
	bool canSchemeAgainst(TeamTypes eTarget, bool bAssumeNoWarPlan,
			bool bCheckDefensivePacts = true) const;
	// Replacing parts of CvTeamAI::AI_declareWarTrade
	DenialTypes declareWarTrade(TeamTypes eTeam, TeamTypes eSponsor) const;
	/*	Replacing CvTeamAI::AI_declareWarTradeVal. However, that function is
		called on the sponsor, whereas this one is called on the hireling
		(consistent with declareWarTrade). */
	int declareWarTradeVal(TeamTypes eTarget, TeamTypes eSponsor) const;
	// Replacing parts of CvTeamAI::AI_makePeaceTrade
	DenialTypes makePeaceTrade(TeamTypes eEnemy, TeamTypes eBroker) const;
	/*	Replacing CvTeamAI::AI_makePeaceTradeVal. However, that function is
		called on the broker, whereas this one is called on the team that gets
		payed for peace (consistent with makePeaceTrade). */
	int makePeaceTradeVal(TeamTypes eEnemy, TeamTypes eBroker) const;
	/*	Replacing some calls to CvTeamAI::AI_endWarVal.
		How much we value ending the war with eEnemy. */
	int endWarVal(TeamTypes eEnemy) const;
	/*	Utility of ending all our wars (through diplo vote).
		Positive if we want to end the war.
		If eVS is set, only wars with members of that vote source are considered. */
	int uEndAllWars(VoteSourceTypes eVS = NO_VOTESOURCE) const;
	// Utility of ending the war against eEnemy
	int uEndWar(TeamTypes eEnemy) const;
	// Joint war through a diplo vote. We mustn't be at war yet.
	int uJointWar(TeamTypes eTarget, VoteSourceTypes eVS) const;
	/*	If we're at war with eTarget, then compute and return our
		utility of convincing eAlly to join the war against eTarget
		(compared with a scenario where we continue the war by ourselves).
		Otherwise, return our utility of a joint war together with eAlly
		against eTarget (compared with a scenario where neither we
		nor eAlly declare war on eTarget). */
	int uJointWar(TeamTypes eTarget, TeamTypes eAlly) const;
	// How much we're willing to pay to eAlly for declaring war on eTarget
	int tradeValJointWar(TeamTypes eTarget, TeamTypes eAlly) const;
	/*	Based on war utility and the utility threshold for peace.
		At least 0 unless bNonNegative=false, in which case a negative
		return value indicates a willingness for peace. */
	int reluctanceToPeace(TeamTypes eEnemy, bool bNonNegative = true) const;
	/*	Trade value that we're willing to pay to any human player for peace
		if peace has a utility of rUtility for us */
	scaled reparationsToHuman(scaled rUtility) const;
	// Replacing CvPlayerAI::AI_demandRebukedSneak (bPrepare=true) and AI_demandRebukedWar
	void respondToRebuke(TeamTypes eTarget, bool bPrepare);
	/*	Taking over parts of CvTeamAI::AI_vassalTrade; only called when
		accepting eVassal will require us (the would-be master) to declare a war. */
	DenialTypes acceptVassal(TeamTypes eVassal) const;
	// Replacing CvTeamAI::AI_isLandTarget
	bool isLandTarget(TeamTypes eTeam) const;
	/*	Whether this team can reach any city of eTarget with military units;
		based on cached info. */
	bool canReach(TeamTypes eTarget) const;
	bool isCloseToAdoptingAnyWarPlan() const;
	UWAI::Player const& leaderUWAI() const;
	// E.g. never need to (directly) evaluate war against vassals
	bool isWarEvalNeeded(TeamTypes eTeam) const;
	/*	Runs 'scheme' as if UWAI was running in the background and writes a
		report file regardless of the REPORT_INTERVAL set in XML.
		Intended for debugging. Could insert a call like
		GET_TEAM((TeamTypes)1).uwai().doWarReport()
		in e.g. CvUnit::kill, load the savegame to be debugged, disband a unit,
		read the report and remove the doWarReport call again. */
	void doWarReport();

private:
	UWAI::Player& leaderUWAI(); // Only make the const version public
	UWAICache& leaderCache();
	UWAICache const& leaderCache() const;
	void reset();
	/*	Abandon wars in preparation, switch plans or targets and consider peace.
		Returns false if scheming should be skipped this turn. */
	bool reviewWarPlans();
	/*	Review plan vs. eTarget. Returns true if plan continues unchanged,
		false if any change (abandoned, peace made, target changed). */
	bool reviewPlan(TeamTypes eTarget, int iU, int iPrepTurns);
	// All these return true if the war plan remains unchanged, false otherwise.
	bool considerPeace(TeamTypes eTarget, int iU);
	bool considerCapitulation(TeamTypes eMaster, int iAgentWarUtility,
			int iMasterReluctancePeace);
	bool tryFindingMaster(TeamTypes eEnemy);
	bool considerPlanTypeChange(TeamTypes eTarget, int iU);
	bool considerAbandonPreparations(TeamTypes eTarget, int iU, int iTurnsRemaining);
	bool considerSwitchTarget(TeamTypes eTarget, int iU, int iTurnsRemaining);
	bool considerConcludePreparations(TeamTypes eTarget, int iU, int iTurnsRemaining);

	void scheme(); // Consider new war plans
	void alignAreaAI(bool bNaval);
	int peaceThreshold(TeamTypes eTarget) const;
	scaled limitedWarWeight() const;
	
	scaled utilityToTradeVal(scaled rUtility) const;
	/*	tradeVal should roughly correspond to gold per turn; converted into
		war utility based on our current commerce rate. */
	scaled tradeValToUtility(scaled rTradeVal) const;

	bool isInBackground() const { return m_bInBackground; }
	void startReport();
	void closeReport();
	void setForceReport(bool b);
	bool isReportTurn() const;
	void showWarPrepStartedMsg(TeamTypes eTarget);
	void showWarPlanAbandonedMsg(TeamTypes eTarget);
	void showWarPlanMsg(TeamTypes eTarget, char const* szKey);

	TeamTypes m_eAgent;
	bool m_bInBackground; // Cache for UWAI::m_bInBackground
	bool m_bForceReport;
	UWAIReport* m_pReport; // Only to be used in doWar and its subroutines
};

// This class makes decisions about war and peace on the level of CvPlayers
class UWAI::Player
{
public:
	Player();
	// See UWAICache.h about the call order during initialization
	void init(PlayerTypes ePlayer);
	void uninit();
	void turnPre();
	// m_cache handles all the persistent data, these two only relay the calls.
	void write(FDataStreamBase* pStream) const;
	void read(FDataStreamBase* pStream);
	UWAICache const& getCache() const { return m_cache; }
	UWAICache& getCache() { return m_cache; }
	// Demands and pleas. Augment BtS code in CvPlayerAI::AI_considerOffer.
	bool considerDemand(PlayerTypes eDemandPlayer, int iTradeVal) const;
	bool considerPlea(PlayerTypes ePleaPlayer, int iTradeVal) const;
	bool amendTensions(PlayerTypes eHuman);
	/*	Returns -1 if unwilling, 1 if willing and 0 to leave the decision to the
		BtS AI */
	int willTalk(PlayerTypes eToPlayer, int iAtWarCounter, bool bUseCache) const;
	// False if all assets of the human civ wouldn't nearly be enough
	bool isPeaceDealPossible(PlayerTypes eHuman) const;
	/*	Can eHuman trade assets to us with a total value of at least
		iTargetTradeVal? */
	bool canTradeAssets(int iTargetTradeVal, PlayerTypes eHuman,
			/*	If this is not NULL, then it is used to return the trade value of
				all assets that the human can trade, but only up to targetTradeVal. */
			int* piAvailableTradeVal = NULL, bool bIgnoreCities = false) const;
	scaled utilityToTradeVal(scaled rUtility) const;
	scaled tradeValToUtility(scaled rTradeVal) const;
	scaled tradeValUtilityConversionRate() const;
	scaled amortizationMultiplier() const;
	scaled buildUnitProb() const;
	/*	iTurns: Build-up over how many turns?
		Will be adjusted to game speed by this function! */
	scaled estimateBuildUpRate(PlayerTypes ePlayer, int iTurns = 10) const;
	scaled estimateDemographicGrowthRate(PlayerTypes ePlayer,
			PlayerHistoryTypes eDemographic, int iTurns = 10) const;
	/*	Whether this player can reach any city of eTarget with military units;
		based on cached info. */
	bool canReach(PlayerTypes eTarget) const;

	/*	Confidence based on experience in the current war with eTarget.
		Between 0.5 (low confidence) and 1.5 (high confidence);
		-1 if not at war. */
	scaled confidenceFromWarSuccess(TeamTypes eTarget) const;
	/*	Confidence based on experience from past wars with eTarget.
		1 if none, otherwise between 0.5 and 1.5. */
	scaled confidenceFromPastWars(TeamTypes eTarget) const;
	// LeaderHead-derived personality values that aren't cached. More in UWAICache.
	/*	A measure of how paranoid our leader is, based on EspionageWeight and
		protective trait. EspionageWeight is between 50 (Gandhi) and 140 (Stalin).
		Return value is between 0.5 and 1.6.
		"Paranoia" would be a better name, but that already means sth. else
		(related to the Alert AI strategy). */
	scaled distrustRating() const;
	/*	A measure of optimism (above 1) or pessimism (between 0 and 1) of our
		leader about conducting war against eTarget. (It's not clear
		whether bTotal should matter.) */
	scaled warConfidencePersonal(bool bNaval, bool bTotal, PlayerTypes eTarget) const;
	/*	Confidence based on experience in the current war or past wars.
		Between 0.5 (low confidence) and 1.5 (high confidence).
		bIgnoreDefOnly: Don't count factors that only make us confident about
		defending ourselves. */
	scaled warConfidenceLearned(PlayerTypes eTarget, bool bIgnoreDefOnly) const;
	/*	How much our leader is (generally) willing to rely on war allies.
		0 to 1 means that the leader is rather self-reliant, above means
		he or she likes dogpile wars. */
	scaled warConfidenceAllies() const;
	scaled confidenceAgainstHuman() const
	{
		/*  Doesn't seem necessary so far; AI rather too reluctant to attack humans
			due to human diplomacy, and other special treatment of humans; e.g.
			can't get a capitulation from human.
			(I've left an older implementation commented out in the .cpp file.) */
		return 1;
	}
	/*	How willing our leader is to go after players that he or she really dislikes.
		Between 0 (Gandhi) and 10 (Montezuma). */
	int vengefulness() const;
	/*	Willingness to come to the aid of partners. "Interventionism" might
		also fit. Between 1.3 (Roosevelt) and 0.7 (Qin). */
	scaled protectiveInstinct() const;
	/*	Between 0.25 (Tokugawa) and 1.75 (Mansa Musa, Zara Yaqob). A measure
		of how much a leader cares about being generally liked in the world. */
	scaled diploWeight() const;
	/*	Between 0 (Pacal and several others) and 1 (Sitting Bull). How much a
		leader insists on reparations to end a war. Based on MakePeaceRand
		(from our leader's personality unless another value is given by the caller). */
	scaled prideRating(int iMakePeaceRand = -1) const;

private:
	// Probability assumed by the AI if this player is human
	scaled humanBuildUnitProb() const;
	// (See public wrapper)
	int willTalk(PlayerTypes eToPlayer, int iAtWarCounter) const;

	PlayerTypes m_eAgent;
	UWAICache m_cache;
};

/*	advc.test: Disables the checks for DP, the PA prereq. tech and the game option;
	refusal based on attitude only if worse than Cautious.
	(Could define this in any header included by both CvTeamAI.cpp and CvPlayer.cpp.
	This one isn't included very frequently elsewhere, i.e. not too slow to recompile.) */
#define TEST_PERMANENT_ALLIANCES 0

#endif
