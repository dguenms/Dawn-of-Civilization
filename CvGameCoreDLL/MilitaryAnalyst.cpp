#include "CvGameCoreDLL.h"
#include "MilitaryAnalyst.h"
#include "WarEvalParameters.h"
#include "UWAIAgent.h"
#include "InvasionGraph.h"
#include "CoreAI.h"
#include "CvCity.h"
#include "CvPlot.h"
#include "CvInfo_GameOption.h"

using std::ostringstream;


// empty sets (static)
CitySet MilitaryAnalyst::m_emptyCitySet;
PlyrSet MilitaryAnalyst::m_emptyPlayerSet;

namespace
{
	scaled nukeChanceToHit(TeamTypes eTeam)
	{
		scaled const rInterceptionProb = per100(std::max(
				GET_TEAM(eTeam).getNukeInterception(),
				// advc.143b:
				GET_TEAM(GET_TEAM(eTeam).getMasterTeam()).getNukeInterception()));
		scaled const rEvasionProb = fixp(0.5); // Fixme: Shouldn't hardcode this
		// Percentage of Tactical Nukes
		scaled rTactRatio = (GET_TEAM(eTeam).isHuman() ? fixp(0.5) : fixp(1/3.));
		scaled rHitProb = 1 - (rInterceptionProb *
				((1 - rTactRatio) + rTactRatio * (1 - rEvasionProb)));
		rHitProb.clamp(0, 1);
		return rHitProb;
	}

	// Known to be at war with anyone. If no observer, all wars are checked.
	bool isKnownToBeAtWar(TeamTypes eTeam, TeamTypes eObserver)
	{
		for (TeamIter<MAJOR_CIV,ENEMY_OF> it(eTeam); it.hasNext(); ++it)
		{
			if (eObserver == NO_TEAM || GET_TEAM(eObserver).isHasMet(it->getID()))
				return true;
		}
		return false;
	}
}


MilitaryAnalyst::MilitaryAnalyst(PlayerTypes eAgentPlayer,
	WarEvalParameters& kWarEvalParams, bool bPeaceScenario)
:	m_kWarEvalParams(kWarEvalParams), m_kReport(kWarEvalParams.getReport()),
	m_eWe(eAgentPlayer), m_eTarget(kWarEvalParams.getTarget()),
	m_bPeaceScenario(bPeaceScenario), m_iTurnsSimulated(0)
{
	PROFILE_FUNC();
	m_playerResults.resize(MAX_CIV_PLAYERS, NULL);
	m_warTable.resize(MAX_CIV_PLAYERS, std::vector<bool>(MAX_CIV_PLAYERS, false));
	m_nukedCities.resize(MAX_CIV_PLAYERS, std::vector<scaled>(MAX_CIV_PLAYERS, 0));
	m_capitulationsAcceptedPerTeam.resize(MAX_CIV_TEAMS);
	m_kReport.log("Military analysis from the pov of %s", m_kReport.leaderName(m_eWe));
	CvTeamAI const& kAgent = GET_TEAM(m_eWe);
	PlyrSet currentlyAtWar; // ("atWar" is already a name of a global function)
	PlyrSet ourFutureOpponents;
	PlyrSet ourSide;
	PlyrSet theirSide;
	PlyrSet weAndOurVassals;
	PlyrSet ourAllies;
	PlyrSet theyAndTheirVassals;
	// Exclude unknown civs from analysis
	for (PlayerIter<MAJOR_CIV,KNOWN_TO> it(kAgent.getID()); it.hasNext(); ++it)
	{
		PlayerTypes const ePlayer = it->getID();
		/*	Civs already at war (not necessarily with us).
			If we are at war, our vassals are covered here as well. */
		if (isKnownToBeAtWar(TEAMID(ePlayer), kAgent.getID()))
			currentlyAtWar.insert(ePlayer);
		TeamTypes eMaster = GET_TEAM(ePlayer).getMasterTeam();
		if (eMaster == kAgent.getMasterTeam())
			weAndOurVassals.insert(ePlayer);
		if (eMaster == GET_TEAM(m_eTarget).getMasterTeam())
			theyAndTheirVassals.insert(ePlayer);
		if (m_kWarEvalParams.isWarAlly(GET_TEAM(ePlayer).getMasterTeam()))
			ourAllies.insert(ePlayer);
		if (m_kWarEvalParams.isExtraTarget(GET_TEAM(ePlayer).getMasterTeam()))
			theirSide.insert(ePlayer);
		// Civs soon to be at war with us or an ally that we bring in
		if (doWePlanToDeclWar(ePlayer) || (m_kWarEvalParams.isAnyWarAlly() &&
			kAgent.isAtWar(TEAMID(ePlayer))))
		{
			// doWePlanToDeclWar checks if ePlayer is part of the enemy team
			ourFutureOpponents.insert(ePlayer);
			theirSide.insert(ePlayer);
			// Defensive pacts that our war plans will trigger
			for(PlayerIter<MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> itAlly(kAgent.getID());
				itAlly.hasNext(); ++itAlly)
			{
				// Can happen b/c of the kekm.3 change
				if (kAgent.isAtWar(itAlly->getTeam()))
					continue;
				if (isDefactoDefensivePact(TEAMID(ePlayer), itAlly->getTeam()))
					ourFutureOpponents.insert(itAlly->getID());
			}
		}
	}
	ourSide.insert(weAndOurVassals.begin(), weAndOurVassals.end());
	ourSide.insert(ourAllies.begin(), ourAllies.end());
	theirSide.insert(theyAndTheirVassals.begin(), theyAndTheirVassals.end());
	bool const bNoWarVsExtra = (m_bPeaceScenario && m_kWarEvalParams.isNoWarVsExtra());
	PlyrSet& declaringWar = ((kAgent.isAtWar(m_eTarget) &&
			!m_kWarEvalParams.isConsideringPeace()) ? ourAllies : ourSide);
	if ((!m_bPeaceScenario && !m_kWarEvalParams.isConsideringPeace()) || bNoWarVsExtra)
	{
		// Store war-scenario DoW for getWarsDeclaredOn/By
		for (PlyrSetIter it1 = declaringWar.begin();
			it1 != declaringWar.end(); ++it1)
		{
			for (PlyrSetIter it2 = theirSide.begin();
				it2 != theirSide.end(); ++it2)
			{
				if (!GET_TEAM(*it1).isAtWar(TEAMID(*it2)))
				{
					playerResult(*it1).setDoWBy(*it2);
					playerResult(*it2).setDoWOn(*it1);
				}
			}
		}
		PlyrSet theirDPAllies;
		for(PlayerIter<MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> it(kAgent.getID());
			it.hasNext(); ++it)
		{
			PlayerTypes const ePlayer = it->getID();
			if (kAgent.isAtWar(TEAMID(ePlayer)))
				continue;
			if (isOnTheirSide(TEAMID(ePlayer), true) &&
				theirSide.count(ePlayer) <= 0)
			{
				theirDPAllies.insert(ePlayer);
			}
		}
		#ifdef _DEBUG
		{
			PlyrSet isect;
			set_intersection(theirSide.begin(), theirSide.end(),
					theirDPAllies.begin(), theirDPAllies.end(), std::inserter(
					 isect, isect.begin()));
			FAssert(isect.empty());
		}
		#endif
		for (PlyrSetIter it = theirDPAllies.begin(); it != theirDPAllies.end(); ++it)
			playerResult(*it).setDoWBy(declaringWar.begin(), declaringWar.end());
		for (PlyrSetIter it = declaringWar.begin(); it != declaringWar.end(); ++it)
			playerResult(*it).setDoWOn(theirDPAllies.begin(), theirDPAllies.end());
	}
	// Wars continued
	for (PlayerIter<MAJOR_CIV> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		PlayerTypes const ePlayer = itPlayer->getID();
		for(PlayerIter<MAJOR_CIV,ENEMY_OF> itEnemy(TEAMID(ePlayer));
			itEnemy.hasNext(); ++itEnemy)
		{
			PlayerTypes const eEnemy = itEnemy->getID();
			if ((declaringWar.count(ePlayer) <= 0 || !m_bPeaceScenario ||
				theirSide.count(eEnemy) <= 0) &&
				(declaringWar.count(eEnemy) <= 0 || !m_bPeaceScenario ||
				theirSide.count(ePlayer) <= 0))
			{
				playerResult(ePlayer).setWarContinued(eEnemy);
				FAssert(getWarsDeclaredBy(ePlayer).count(eEnemy) <= 0);
				FAssert(getWarsDeclaredBy(eEnemy).count(ePlayer) <= 0);
				FAssert(getWarsDeclaredOn(ePlayer).count(eEnemy) <= 0);
				FAssert(getWarsDeclaredOn(eEnemy).count(ePlayer) <= 0);
			}
		}
	}
	// Need ArmamentForecasts for initially uninvolved parties (if any)
	PlyrSet uninvolved;
	uninvolved.insert(declaringWar.begin(), declaringWar.end());
	uninvolved.insert(ourFutureOpponents.begin(), ourFutureOpponents.end());
	m_partOfAnalysis.insert(currentlyAtWar.begin(), currentlyAtWar.end());
	m_partOfAnalysis.insert(uninvolved.begin(), uninvolved.end());
	m_pInvGraph = new InvasionGraph(*this, currentlyAtWar, m_bPeaceScenario);
	m_pInvGraph->addUninvolvedParties(uninvolved);
	/*	Simulation in two phases: The first phase lasts until we have finished
		our war preparations (NB: we may already be in a war while preparing
		for another); the second phase lasts for a set number of turns. */
	int iPrepTime = m_kWarEvalParams.getPreparationTime();
	/*	Above, uninvolved parties are added and preparation time is set
		regardless of peace scenario; otherwise, the results for the
		war and peace scenario wouldn't be fully comparable. */
	if (m_bPeaceScenario)
	{
		// Master isn't included in the removed war opponents (theirSide) then
		FAssert(!kAgent.isAtWar(m_eTarget) || !GET_TEAM(m_eTarget).isAVassal());
		if (bNoWarVsExtra)
		{
			PlyrSet diff; // diff = theirSide minus theyAndTheirVassals
			std::set_difference(theirSide.begin(), theirSide.end(),
					theyAndTheirVassals.begin(), theyAndTheirVassals.end(),
					std::inserter(diff, diff.begin()));
			m_pInvGraph->removeWar(declaringWar, diff);
		}
		/*	Capitulation: Not fully implemented; misses the wars that we need
			to declare on the enemies of theyId. */
		else if (m_kWarEvalParams.getCapitulationTeam() == m_eTarget)
			m_pInvGraph->removeWar(declaringWar, currentlyAtWar);
		else m_pInvGraph->removeWar(declaringWar, theirSide);
	}
	int iTimeHorizon = 25;
	// Look a bit farther into the future when in a total war
	if (iPrepTime <= 0 && m_kWarEvalParams.isTotal())
		iTimeHorizon += 5;
	// Look a bit farther on Marathon speed
	if(GC.getInfo(GC.getGame().getGameSpeedType()).getGoldenAgePercent() >= 150)
		iTimeHorizon += 5;
	/*  Skip phase 1 if it would be short (InvasionGraph::Node::isSneakAttack
		will still read the actual prep time from the WarEvalParameters) */
	if (iPrepTime < 4)
	{
		if (iPrepTime > 0)
			m_kReport.log("Skipping short prep. time (%d turns):", iPrepTime);
		iTimeHorizon += iPrepTime; // Prolong 2nd phase instead
		iPrepTime = 0;
	}
	else
	{
		m_kReport.log("Phase 1%s%s%s (%d turns)",
				m_bPeaceScenario ? "" : ": Prolog of simulation; ",
				m_bPeaceScenario ? "" : m_kReport.leaderName(m_eWe),
				m_bPeaceScenario ? "": " is preparing war",
				iPrepTime);
		m_pInvGraph->simulate(iPrepTime);
		m_iTurnsSimulated += iPrepTime;
	}
	if (!m_bPeaceScenario || bNoWarVsExtra)
		m_pInvGraph->addFutureWarParties(declaringWar, ourFutureOpponents);
	/*  Force update of targets (needed even if no parties were added b/c of
		defeats in phase I. */
	if (m_bPeaceScenario)
		m_pInvGraph->updateTargets();
	m_kReport.log("Phase 2%s%s (%d turns)",
			(!m_bPeaceScenario && !kAgent.isAtWar(m_eTarget) ?
			": Simulation assuming DoW by " : ""),
			(!m_bPeaceScenario && !kAgent.isAtWar(m_eTarget) ?
			m_kReport.leaderName(m_eWe) : ""), iTimeHorizon);
	m_pInvGraph->simulate(iTimeHorizon);
	m_iTurnsSimulated += iTimeHorizon;
	prepareResults(); // ... of conventional war
	simulateNuclearWar();
}


MilitaryAnalyst::~MilitaryAnalyst()
{
	delete m_pInvGraph;
	for (size_t i = 0; i < m_playerResults.size(); i++)
		SAFE_DELETE(m_playerResults[i]);
}


MilitaryAnalyst::PlayerResult& MilitaryAnalyst::playerResult(PlayerTypes ePlayer)
{
	/*	Lazy creation of playerResults means that NULL needs to be checked when accessing
		a PlayerResult and that memory needs to be allocated dynamically. Based on a test,
		this is still faster than creating a PlayerResult for every player upfront and
		accessing the empty sets of the dummy entries. */
	FAssertBounds(0, MAX_CIV_PLAYERS, ePlayer);
	if (m_playerResults[ePlayer] == NULL)
		m_playerResults[ePlayer] = new PlayerResult();
	return *m_playerResults[ePlayer];
}


bool MilitaryAnalyst::isOnOurSide(TeamTypes eTeam) const
{
	return (GET_TEAM(eTeam).getMasterTeam() == GET_TEAM(m_eWe).getMasterTeam() ||
			m_kWarEvalParams.isWarAlly(eTeam));
}


bool MilitaryAnalyst::isOnTheirSide(TeamTypes eTeam, bool bDefensivePacts) const
{
	bool bR = (GET_TEAM(eTeam).getMasterTeam() ==
			GET_TEAM(m_kWarEvalParams.getTarget()).getMasterTeam() ||
			m_kWarEvalParams.isExtraTarget(eTeam));
	if (!bDefensivePacts || bR)
		return bR;
	for (TeamIter<MAJOR_CIV> it; it.hasNext(); ++it)
	{
		if (GET_TEAM(eTeam).isDefensivePact(it->getID()) &&
			isOnTheirSide(it->getID()))
		{
			return true;
		}
	}
	return false;
}


bool MilitaryAnalyst::doWePlanToDeclWar(PlayerTypes ePlayer) const
{
	CvTeamAI const& kAgent = GET_TEAM(m_eWe);
	TeamTypes const eTeam = TEAMID(ePlayer);
	/*	Ongoing war preparations will be replaced by the war plan under
		consideration if adopted; disregard those. */
	return (//kAgent.AI_getWarPlan(eTeam) != NO_WARPLAN ||
			eTeam == m_kWarEvalParams.getTarget()) &&
			!kAgent.isAtWar(eTeam);
}


void MilitaryAnalyst::simulateNuclearWar()
{
	// Only simulates nukes fired by or on us
	PlayerTypes const eWe = m_eWe; // abbreviate
	CvPlayerAI const& kWe = GET_PLAYER(eWe);
	if (isEliminated(eWe) || kWe.getNumCities() <= 0)
		return; // Who cares then
	CvTeamAI const& kAgent = GET_TEAM(eWe);
	UWAICache const& kOurCache = kWe.uwai().getCache();
	/*	Counts the number of nukes. Assume no further build-up of nukes throughout
		the military analysis. (They take long to build.) */
	int const iOurNukes = kOurCache.getPowerValues()[NUCLEAR]->numUnits();
	scaled rOurTargets;
	for (PlayerIter<MAJOR_CIV> itEnemy; itEnemy.hasNext(); ++itEnemy)
	{
		if (isWar(eWe, itEnemy->getID()))
			rOurTargets += (itEnemy->isAVassal() ? fixp(0.5) : 1);
	}
	for (PlayerAIIter<MAJOR_CIV> itEnemy; itEnemy.hasNext(); ++itEnemy)
	{
		CvPlayerAI const& kEnemy = *itEnemy;
		if (!isWar(eWe, kEnemy.getID()))
			continue;
		int iEnemyNukes = kEnemy.uwai().getCache().
				getPowerValues()[NUCLEAR]->numUnits();
		if (iOurNukes + iEnemyNukes <= 0)
			continue;
		// The AI is (much) more willing to fire nukes in total war than in limited war
		WarPlanTypes const eOurWP = kAgent.AI_getWarPlan(kEnemy.getTeam());
		WarPlanTypes const eEnemyWP = GET_TEAM(kEnemy.getTeam()).AI_getWarPlan(
				kAgent.getID());
		// If one side goes total, the other will follow suit.
		bool bTotal = false;
		if (eOurWP == WARPLAN_PREPARING_TOTAL || eOurWP == WARPLAN_TOTAL ||
			eEnemyWP == WARPLAN_PREPARING_TOTAL || eEnemyWP == WARPLAN_TOTAL)
		{
			bTotal = true;
		}
		// (Human: let's trust the war plan type of the human proxy AI)
		if (m_kWarEvalParams.getTarget() == kEnemy.getTeam())
			bTotal = m_kWarEvalParams.isTotal();
		scaled rPortionFired = (bTotal ? fixp(0.75) : fixp(0.25));
		// Assume that vassals are hit by fewer nukes, and fire fewer nukes.
		scaled rOurVassalMult = 1;
		if (kAgent.isAVassal())
			rOurVassalMult /= 2;
		scaled rEnemyVassalMult = 1;
		if (kAgent.isAVassal())
			rEnemyVassalMult /= 2;
		scaled rEnemyTargets;
		for (PlayerIter<MAJOR_CIV> it; it.hasNext(); ++it)
		{
			CvPlayer const& kEnemyOfEnemy = *it;
			if (isWar(kEnemyOfEnemy.getID(), kEnemyOfEnemy.getID()))
				rEnemyTargets += (kEnemyOfEnemy.isAVassal() ? fixp(0.5) : 1);
		}
		scaled rFiredOnUs = rPortionFired * rOurVassalMult * rEnemyVassalMult *
				/*  sqrt for pessimism - we may get hit worse than the
					average target, and that worries us. */
				(iEnemyNukes / rEnemyTargets.sqrt());
		rFiredOnUs.decreaseTo(fixp(1.5) * kWe.getNumCities());
		scaled rFiredByUs;
		if (rOurTargets > 0)
		{
			rFiredByUs = rPortionFired * rOurVassalMult * rEnemyVassalMult * iOurNukes *
					(kWe.AI_isDoStrategy(AI_STRATEGY_OWABWNW) ? fixp(1.1) : fixp(0.9)) /
					rOurTargets;
		}
		rFiredByUs.decreaseTo(fixp(1.5) * kEnemy.getNumCities());
		scaled rHittingUs = rFiredOnUs * nukeChanceToHit(kAgent.getID());
		scaled rHittingEnemy = rFiredByUs * nukeChanceToHit(kEnemy.getTeam());
		// Make sure not to allocate PlayerResult unnecessarily
		if (rHittingUs > 0)
		{
			playerResult(eWe).addNukesSuffered(rHittingUs);
			m_nukedCities[kEnemy.getID()][eWe] += rHittingUs;
		}
		if (rHittingEnemy > 0)
		{
			playerResult(kEnemy.getID()).addNukesSuffered(rHittingEnemy);
			m_nukedCities[eWe][kEnemy.getID()] += rHittingEnemy;
		}
		if (rFiredByUs > 0)
			playerResult(eWe).addNukesFired(rFiredByUs);
		if (rFiredOnUs > 0)
			playerResult(kEnemy.getID()).addNukesFired(rFiredOnUs);
	}
}


bool MilitaryAnalyst::isDefactoDefensivePact(TeamTypes eFirst, TeamTypes eSecond) const
{
	CvTeam const& kFirst = GET_TEAM(eFirst);
	return (kFirst.isDefensivePact(eSecond) ||
			kFirst.isVassal(eSecond) || GET_TEAM(eSecond).isVassal(eFirst) ||
			(kFirst.getMasterTeam() == GET_TEAM(eSecond).getMasterTeam() &&
			eFirst != eSecond));
}


void MilitaryAnalyst::prepareResults()
{
	PROFILE_FUNC();
	for (PlayerIter<MAJOR_CIV> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		PlayerTypes const ePlayer = itPlayer->getID();
		InvasionGraph::Node const* pNode = m_pInvGraph->getNode(ePlayer);
		if (pNode == NULL)
			continue;
		// Allocate PlayerResult only if necessary
		if (pNode->anyConquests())
			pNode->getConquests(playerResult(ePlayer).getConqueredCities());
		if (pNode->anyCityLosses())
			pNode->getCityLosses(playerResult(ePlayer).getLostCities());
		pNode->getCapitulationsAccepted(m_capitulationsAcceptedPerTeam[ePlayer]);
	}
	// Predict scores as current game score modified based on gained/ lost population
	CvGame const& kGame = GC.getGame();
	UWAICache const& kOurCache = GET_PLAYER(m_eWe).uwai().getCache();
	for (PlayerIter<MAJOR_CIV> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		PlayerTypes const ePlayer = itPlayer->getID();
		int const iCurrTotalPop = GET_PLAYER(ePlayer).getTotalPopulation();
		if (iCurrTotalPop <= 0)
			continue;
		scaled rPopIncrease;
		CitySet const& kConq = conqueredCities(ePlayer);
		for (CitySetIter it = kConq.begin(); it != kConq.end(); ++it)
		{
			CvCity const& kCity = kOurCache.lookupCity(*it)->city();
			rPopIncrease += kCity.getPopulation() *
					// Likely to lose population in the short and medium term
					(2 + per100(kCity.getPlot().calculateCulturePercent(ePlayer))) / 3;
		}
		CitySet const& kLost = lostCities(ePlayer);
		for (CitySetIter it = kLost.begin(); it != kLost.end(); ++it)
		{
			rPopIncrease -= kOurCache.lookupCity(*it)->city().getPopulation();
		}
		rPopIncrease /= std::max(1, iCurrTotalPop);
		// This is just a (poor) starting point for predictedGameScore
		playerResult(ePlayer).setGameScore(kGame.getPlayerScore(ePlayer) *
				scaled::max(0, 1 + rPopIncrease));
	}
	// Precompute a table for isWar b/c it's frequently used
	for (PlayerIter<MAJOR_CIV> it1; it1.hasNext(); ++it1)
	{
		PlayerTypes const eFirst = it1->getID();
		for (PlayerIter<MAJOR_CIV> it2; it2.hasNext(); ++it2)
		{
			PlayerTypes const eSecond = it2->getID();
			m_warTable[eFirst][eSecond] = (
					getWarsContinued(eFirst).count(eSecond) > 0 ||
					getWarsDeclaredBy(eFirst).count(eSecond) > 0 ||
					getWarsDeclaredOn(eFirst).count(eSecond) > 0);
		}
	}
}


scaled MilitaryAnalyst::predictedGameScore(PlayerTypes ePlayer) const
{
	FAssertBounds(0, MAX_CIV_PLAYERS, ePlayer);
	int const iCurrScore = GC.getGame().getPlayerScore(ePlayer);
	scaled r = iCurrScore *
			(1 + GET_PLAYER(m_eWe).uwai().estimateDemographicGrowthRate(
			ePlayer, PLAYER_HISTORY_SCORE, turnsSimulated()));
	PlayerResult* pR = m_playerResults[ePlayer];
	if (pR == NULL || pR->getGameScore() < 0)
		return r;
	if (isEliminated(ePlayer))
		return 0;
	scaled rFromSim = pR->getGameScore();
	TeamSet const& kCap = getCapitulationsAccepted(TEAMID(ePlayer));
	for (TeamSetIter itVassal = kCap.begin(); itVassal != kCap.end(); ++itVassal)
	{	// Use a fraction of the vassal's current score to keep it simple
		rFromSim += fixp(0.4) * GC.getGame().getTeamScore(*itVassal);
	}
	if (rFromSim < iCurrScore)
		r = (r + rFromSim) / 2;
	else r.increaseTo(rFromSim);
	if (hasCapitulated(TEAMID(ePlayer)))
		r /= 2;
	return r;
}


bool MilitaryAnalyst::isWar(TeamTypes eFirst, TeamTypes eSecond) const
{
	return isWar(GET_TEAM(eFirst).getLeaderID(), GET_TEAM(eSecond).getLeaderID());
}


bool MilitaryAnalyst::hasCapitulated(TeamTypes eTeam) const
{
	for (MemberIter it(eTeam); it.hasNext(); ++it)
	{
		PlayerTypes const ePlayer = it->getID();
		InvasionGraph::Node const* pNode = m_pInvGraph->getNode(ePlayer);
		if (pNode != NULL && pNode->hasCapitulated())
		{
			FAssert(!GET_TEAM(eTeam).isAVassal());
			return true;
		}
	}
	return false;
}


bool MilitaryAnalyst::isEliminated(PlayerTypes ePlayer) const
{
	InvasionGraph::Node const* pNode = m_pInvGraph->getNode(ePlayer);
	if (pNode == NULL)
		return false;
	CitySet lost;
	pNode->getCityLosses(lost);
	return (((int)lost.size()) == GET_PLAYER(ePlayer).getNumCities());
}


scaled MilitaryAnalyst::lostPower(PlayerTypes ePlayer,
	MilitaryBranchTypes eBranch) const
{
	InvasionGraph::Node const* pNode = m_pInvGraph->getNode(ePlayer);
	if (pNode == NULL)
		return 0;
	return pNode->getLostPower(eBranch);
}


scaled MilitaryAnalyst::gainedPower(PlayerTypes ePlayer,
	MilitaryBranchTypes eBranch) const
{
	InvasionGraph::Node const* pNode = m_pInvGraph->getNode(ePlayer);
	if (pNode == NULL)
		return 0;
	return pNode->getGainedPower(eBranch);
}


scaled MilitaryAnalyst::militaryProduction(PlayerTypes ePlayer) const
{
	InvasionGraph::Node const* pNode = m_pInvGraph->getNode(ePlayer);
	if (pNode == NULL)
		return 0;
	return pNode->getProductionInvested();
}


void MilitaryAnalyst::logResults(PlayerTypes ePlayer)
{
	if (m_kReport.isMute())
		return;
	// Not the best way to identify civs that weren't part of the simulation ...
	if (militaryProduction(ePlayer).uround() == 0)
		return;
	m_kReport.log("Results about %s", m_kReport.leaderName(ePlayer));
	m_kReport.log("\nbq.");
	logCapitulations(ePlayer);
	logCities(ePlayer, true);
	logCities(ePlayer, false);
	logPower(ePlayer, false);
	logPower(ePlayer, true);
	m_kReport.log("Invested production: %d", militaryProduction(ePlayer).uround());
	logDoW(ePlayer);
	m_kReport.log("");
}


void MilitaryAnalyst::logCities(PlayerTypes ePlayer, bool bConquests)
{
	PlayerResult const* pResult = m_playerResults[ePlayer];
	if (pResult == NULL)
		return;
	CitySet const& kCities = (bConquests ? pResult->getConqueredCities() :
			pResult->getLostCities());
	if (kCities.empty())
		return;
	m_kReport.log("Cities %s:", bConquests ? "conquered" : "lost");
	for (CitySetIter it = kCities.begin(); it != kCities.end(); ++it)
	{
		m_kReport.log("%s", m_kReport.cityName(UWAICache::cvCityById(*it)));
	}
}


void MilitaryAnalyst::logCapitulations(PlayerTypes ePlayer)
{
	if (isEliminated(ePlayer))
	{
		m_kReport.log("Eliminated");
		return;
	}
	TeamTypes const eTeam = TEAMID(ePlayer);
	if (hasCapitulated(eTeam))
	{
		m_kReport.log("Team has capitulated");
		return;
	}
	TeamSet const& kCaps = m_capitulationsAcceptedPerTeam[eTeam];
	if (kCaps.empty())
		return;
	m_kReport.log("Capitulation accepted from:");
	for (TeamSetIter it = kCaps.begin(); it != kCaps.end(); ++it)
	{
		// The team name (e.g. Team1) would not be helpful
		for (MemberIter itMember(*it); itMember.hasNext(); ++itMember)
			m_kReport.log("%s", m_kReport.leaderName(itMember->getID()));
	}
}


void MilitaryAnalyst::logDoW(PlayerTypes ePlayer)
{
	PlayerResult const* pResult = m_playerResults[ePlayer];
	if (pResult == NULL)
		return;
	PlyrSet const& DoWBy = pResult->getDoWBy();
	if (!DoWBy.empty())
	{
		m_kReport.log("Wars declared by %s:",
				m_kReport.leaderName(ePlayer));
		for (PlyrSetIter it = DoWBy.begin(); it != DoWBy.end(); ++it)
			m_kReport.log("%s", m_kReport.leaderName(*it));
	}
	PlyrSet const& DoWOn = pResult->getDoWOn();
	if (!DoWOn.empty())
	{
		m_kReport.log("Wars declared on %s:", m_kReport.leaderName(ePlayer));
		for (PlyrSetIter it = DoWOn.begin(); it != DoWOn.end(); ++it)
			m_kReport.log("%s", m_kReport.leaderName(*it));
	}
	PlyrSet const& kWarsCont = pResult->getWarsContinued();
	if (!kWarsCont.empty())
	{
		m_kReport.log("Wars continued:");
		for (PlyrSetIter it = kWarsCont.begin(); it != kWarsCont.end(); ++it)
			m_kReport.log("%s", m_kReport.leaderName(*it));
	}
}


void MilitaryAnalyst::logPower(PlayerTypes ePlayer, bool bGained)
{
	// Some overlap with InvasionGraph::Node::logPower
	ostringstream out;
	if (bGained)
		out << "Net power gain (build-up minus losses): ";
	else out << "Lost power from casualties: ";
	int iLogged = 0;
	for (int i = 0; i < NUM_BRANCHES; i++)
	{
		MilitaryBranchTypes eBranch = (MilitaryBranchTypes)i;
		int iPowChange = (bGained ?
				gainedPower(ePlayer, eBranch) - lostPower(ePlayer, eBranch) :
				lostPower(ePlayer, eBranch)).round();
		if (iPowChange == 0)
			continue;
		if (iLogged > 0)
			out << ", ";
		out << MilitaryBranch::str(eBranch) << " " << iPowChange;
		iLogged++;
	}
	if (iLogged == 0)
		out << "none";
	m_kReport.log("%s", out.str().c_str());
}
