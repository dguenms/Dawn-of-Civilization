#include "CvGameCoreDLL.h"
#include "UWAIAgent.h"
#include "WarEvaluator.h"
#include "UWAIReport.h"
#include "WarEvalParameters.h"
#include "MilitaryBranch.h"
#include "CvInfo_GameOption.h"
#include "CvInfo_Building.h" // Just for vote-related info
#include "CoreAI.h"
#include "CvCityAI.h"
#include "CvDiploParameters.h"
#include "TeamPathFinder.h"
#include "CvArea.h"
#include "RiseFall.h" // advc.705

using std::vector;
using std::set;

namespace
{
	int const iMaxReparationUtility = 25;
	int const iWarTradeUtilityThresh = -37;
	// AI payments for peace (with human or AI enemy)
	scaled const rReparationsModifierAI = fixp(0.5);
	/*  Modifier for human payments for peace, i.e what the AI asks a human to pay
		(no modifier for brokering, i.e. 100%). */
	scaled const rReparationsModifierHuman = fixp(0.75);
}


UWAI::Team::Team()
:	m_eAgent (NO_TEAM), m_bInBackground(false),
	m_pReport(NULL), m_bForceReport(false)
{}


UWAI::Team::~Team()
{
	SAFE_DELETE(m_pReport);
}


void UWAI::Team::reset()
{
	m_bInBackground = getUWAI().isEnabled(true);
}


void UWAI::Team::init(TeamTypes eTeam)
{
	m_eAgent = eTeam;
	reset();
}


void UWAI::Team::write(FDataStreamBase* pStream) const
{
	pStream->Write(m_eAgent);
}


void UWAI::Team::read(FDataStreamBase* pStream)
{
	pStream->Read((int*)&m_eAgent);
	reset();
}


void UWAI::Team::addTeam(PlayerTypes eOtherLeader)
{
	for (MemberAIIter it(m_eAgent); it.hasNext(); ++it)
		it->uwai().getCache().addTeam(eOtherLeader);
}


void UWAI::Team::reportWarEnding(TeamTypes eEnemy,
	CLinkList<TradeData> const* pWeReceive,
	CLinkList<TradeData> const* pWeGive)
{
	/*  This isn't team-level data b/c each member can have its
		own interpretation of whether the war was successful. */
	for (MemberAIIter it(m_eAgent); it.hasNext(); ++it)
		it->uwai().getCache().reportWarEnding(eEnemy, pWeReceive, pWeGive);
}


void UWAI::Team::turnPre()
{
	/*  Causes Player::turnPre to be called before CvPlayerAI::AI_turnPre.
		That's OK b/c AI_turnPre doesn't do anything crucial for UWAI::Player.
		Need to call Player::turnPre already during the team turn b/c
		the update to UWAICache is important for war planning. */
	for (MemberAIIter it(m_eAgent); it.hasNext(); ++it)
		it->uwai().turnPre();
}


void UWAI::Team::doWar()
{
	if (!getUWAI().isReady())
		return;
	CvTeamAI& kAgent = GET_TEAM(m_eAgent);
	if (!kAgent.isAlive() || !kAgent.isMajorCiv())
		return;
	FAssertMsg(!kAgent.isAVassal() || kAgent.getNumWars() > 0 ||
			kAgent.AI_getNumWarPlans(WARPLAN_DOGPILE) +
			kAgent.AI_getNumWarPlans(WARPLAN_LIMITED) +
			kAgent.AI_getNumWarPlans(WARPLAN_TOTAL) <= 0,
			"Vassals shouldn't have non-preparatory war plans unless at war");
	startReport();
	if (kAgent.isHuman() || kAgent.isAVassal())
	{
		m_pReport->log("%s is %s", m_pReport->teamName(kAgent.getID()),
				(kAgent.isHuman() ? "human" : "a vassal"));
		for (TeamIter<MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> it(kAgent.getID());
			it.hasNext(); ++it)
		{
			TeamTypes const eTarget = it->getID();
			WarPlanTypes const eWP = kAgent.AI_getWarPlan(eTarget);
			if (eWP == WARPLAN_ATTACKED_RECENT)
				considerPlanTypeChange(eTarget, 0);
			/*  Non-human vassals abandon human-instructed war prep. after 20 turns.
				Humans can have war preparations from AI Auto Play that they should
				also abandon (but not immediately b/c AI Auto Play could resume.) */
			if ((eWP == WARPLAN_PREPARING_LIMITED || eWP == WARPLAN_PREPARING_TOTAL) &&
				(kAgent.isHuman() || !GET_TEAM(kAgent.getMasterTeam()).isHuman()) &&
				kAgent.AI_getWarPlanStateCounter(eTarget) > 20)
			{
				considerAbandonPreparations(eTarget, -1, 0);
			}
			if (kAgent.isAVassal())
			{
				/*  Make sure we match our master's war plan.
					CvTeamAI::AI_setWarPlan mostly handles this, but
					doesn't align vassal's plans after signing the vassal agreement.
					(Could do that in CvTeam::setVassal I guess.) */
				CvTeamAI const& kMaster = GET_TEAM(kAgent.getMasterTeam());
				if (kMaster.getID() == eTarget)
					continue;
				if (kMaster.isAtWar(eTarget))
					kAgent.AI_setWarPlan(eTarget, WARPLAN_DOGPILE);
				else if (kMaster.AI_getWarPlan(eTarget) != NO_WARPLAN &&
					!kMaster.isHuman()) // Human master will have to instruct us
				{
					kAgent.AI_setWarPlan(eTarget, WARPLAN_PREPARING_LIMITED);
				}
			}
		}
		m_pReport->log("Nothing more to do for this team");
		closeReport();
		return;
	}
	UWAICache& kCache = leaderCache();
	if (reviewWarPlans())
	{
		scheme();
		for (TeamIter<CIV_ALIVE,KNOWN_POTENTIAL_ENEMY_OF> itTarget(kAgent.getID());
			itTarget.hasNext(); ++itTarget)
		{
			if (kAgent.AI_isSneakAttackPreparing(itTarget->getID()))
				kCache.setCanBeHiredAgainst(itTarget->getID(), true);
		}
	}
	else
	{
		m_pReport->log("No scheming b/c clearly busy with current wars");
		for (TeamIter<CIV_ALIVE> it; it.hasNext(); ++it)
			kCache.setCanBeHiredAgainst(it->getID(), false);
	}
	closeReport();
}


UWAI::Player const& UWAI::Team::leaderUWAI() const
{
	return GET_PLAYER(GET_TEAM(m_eAgent).getLeaderID()).uwai();
}

UWAI::Player& UWAI::Team::leaderUWAI()
{
	return GET_PLAYER(GET_TEAM(m_eAgent).getLeaderID()).uwai();
}


scaled UWAI::Team::utilityToTradeVal(scaled rUtility) const
{
	scaled r;
	MemberAIIter itMember(m_eAgent);
	for(; itMember.hasNext(); ++itMember)
		r += itMember->uwai().utilityToTradeVal(rUtility);
	return r / itMember.nextIndex();
}


scaled UWAI::Team::tradeValToUtility(scaled rTradeVal) const
{
	scaled r;
	MemberAIIter itMember(m_eAgent);
	for(; itMember.hasNext(); ++itMember)
		r += itMember->uwai().tradeValToUtility(rTradeVal);
	return r / itMember.nextIndex();
}


namespace
{
	struct PlanData
	{
		PlanData(int iU, TeamTypes eTarget, int iPrepTurns, bool bNaval)
		:	iU(iU), eTarget(eTarget), iPrepTurns(iPrepTurns), bNaval(bNaval)
		{}
		bool operator<(PlanData const& kOther) { return iU < kOther.iU; }
		int iU;
		TeamTypes eTarget;
		int iPrepTurns;
		bool bNaval;
	};
}

bool UWAI::Team::reviewWarPlans()
{
	CvTeamAI& kAgent = GET_TEAM(m_eAgent);
	if (!kAgent.AI_isAnyWarPlan())
	{
		m_pReport->log("%s has no war plans to review",
				m_pReport->teamName(kAgent.getID()));
		return true;
	}
	bool bScheme = true;
	m_pReport->log("%s reviews its war plans",
			m_pReport->teamName(kAgent.getID()));
	EagerEnumMap<TeamTypes,bool> abTargetDone;
	bool bPlanChanged = false;
	bool bAllNaval = true, bAnyNaval = false;
	bool bAllLand = true, bAnyLand = false;
	do
	{
		vector<PlanData> aPlans;
		for (TeamAIIter<MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> itTarget(kAgent.getID());
			itTarget.hasNext(); ++itTarget)
		{
			CvTeamAI const& kTarget = *itTarget;
			TeamTypes const eTarget = kTarget.getID();
			if (abTargetDone.get(eTarget))
				continue;
			if (kTarget.isHuman()) // considerCapitulation may set ReadyToCapitulate
				leaderCache().setReadyToCapitulate(eTarget, false);
			WarPlanTypes const eWP = kAgent.AI_getWarPlan(eTarget);
			if (eWP == NO_WARPLAN)
			{
				// As good a place as any to make sure of this
				FAssert(kAgent.AI_getWarPlanStateCounter(eTarget) == 0);
				continue;
			}
			if (kTarget.isAVassal())
				continue;
			WarEvalParameters params(kAgent.getID(), eTarget, *m_pReport);
			WarEvaluator eval(params);
			int iU = eval.evaluate(eWP);
			// 'evaluate' sets preparation time and isNaval in params
			aPlans.push_back(PlanData(iU, eTarget, params.getPreparationTime(),
					params.isNaval()));
			/*  Skip scheming when in a very bad war. Very unlikely that another war
				could help then. And I worry that, in rare situations, when the
				outcome of a war is close, but potentially disastrous, that an
				additional war could produce a more favorable simulation outcome. */
			if (iU < -100 && kAgent.isAtWar(eTarget))
				bScheme = false;
		}
		std::sort(aPlans.begin(), aPlans.end());
		bPlanChanged = false;

		for (size_t i = 0; i < aPlans.size(); i++)
		{
			bPlanChanged = !reviewPlan(aPlans[i].eTarget, aPlans[i].iU,
					aPlans[i].iPrepTurns);
			if (bPlanChanged)
			{
				abTargetDone.set(aPlans[i].eTarget, true);
				if (abTargetDone.numNonDefault() < (int)aPlans.size())
				{
					m_pReport->log("War plan against %s has changed, repeating review",
							m_pReport->teamName(aPlans[i].eTarget));
				}
				break;
			}
			// Ignore isNaval if we're not sure about the war (low utility)
			else if (aPlans[i].iU > 5)
			{
				if (aPlans[i].bNaval)
				{
					bAnyNaval = true;
					bAllLand = false;
				}
				else
				{
					bAnyLand = true;
					bAllNaval = false;
				}
			}
		}
	} while(bPlanChanged);
	/*  As CvTeamAI::AI_updateAreaStrategies is called before CvTeamAI::AI_doWar,
		this is going to be the last word on AreaAI. */
	if (bAllNaval && bAnyNaval)
		alignAreaAI(true);
	if (bAllLand && bAnyLand)
		alignAreaAI(false);
	return bScheme;
}


void UWAI::Team::alignAreaAI(bool bNaval)
{
	PROFILE_FUNC();
	set<int> areasToAlign;
	set<int> areasNotToAlign;
	for (MemberAIIter itMember(m_eAgent); itMember.hasNext(); ++itMember)
	{
		CvPlayerAI const& kMember = *itMember;
		CvCity const* pCapital = kMember.getCapital();
		if (pCapital == NULL)
			continue;
		CvArea& kArea = pCapital->getArea();
		CvCity const* pTargetCity = kArea.AI_getTargetCity(kMember.getID());
		bool bAlign = true;
		if (bNaval)
		{
			if (pTargetCity!= NULL &&
				(GET_TEAM(pTargetCity->getTeam()).AI_isPrimaryArea(kArea) ||
				3 * kArea.getCitiesPerPlayer(pTargetCity->getOwner()) >
				kArea.getCitiesPerPlayer(kMember.getID())))
			{
				WarPlanTypes eWP = GET_TEAM(m_eAgent).AI_getWarPlan(
						pTargetCity->getTeam());
				if (!GET_TEAM(m_eAgent).AI_isPushover(pTargetCity->getTeam()) ||
					(eWP != WARPLAN_TOTAL && eWP != WARPLAN_PREPARING_TOTAL))
				{
					// Make sure there isn't an easily reachable target in the capital area
					TeamPathFinder<TeamPath::LAND> pf(GET_TEAM(m_eAgent),
							&GET_TEAM(pTargetCity->getTeam()), 8);
					if (pf.generatePath(pCapital->getPlot(), pTargetCity->getPlot()))
						bAlign = false;
				}
			}
		}
		else
		{
			// Make sure some city can be attacked in the capital area
			if (pTargetCity == NULL)
			{
				// Target city is sometimes (randomly) set to NULL
				pTargetCity = kMember.AI_findTargetCity(kArea);
			}
			if (pTargetCity == NULL)
				bAlign = false;
			else
			{
				UWAICache::City* pCacheCity = kMember.uwai().getCache().
						lookupCity(pTargetCity->plotNum());
				if (pCacheCity == NULL || !pCacheCity->canReachByLandFromCapital())
					bAlign = false;
			}
		}
		if (bAlign)
			areasToAlign.insert(kArea.getID());
		else areasNotToAlign.insert(kArea.getID());
	}
	set<int> diff;
	std::set_difference(
			areasToAlign.begin(), areasToAlign.end(),
			areasNotToAlign.begin(), areasNotToAlign.end(),
			std::inserter(diff, diff.begin()));
	CvMap& kMap = GC.getMap();
	for(set<int>::const_iterator it = diff.begin(); it != diff.end(); ++it)
	{
		CvArea& kArea = *kMap.getArea(*it);
		AreaAITypes const eOldAreaAI = kArea.getAreaAIType(m_eAgent);
		AreaAITypes eNewAreaAI = eOldAreaAI;
		if (bNaval)
		{
			if (eOldAreaAI == AREAAI_MASSING)
				eNewAreaAI = AREAAI_ASSAULT_MASSING;
			else if (eOldAreaAI == AREAAI_OFFENSIVE)
				eNewAreaAI = AREAAI_ASSAULT;
		}
		else
		{
			if (eOldAreaAI == AREAAI_ASSAULT_MASSING)
				eNewAreaAI = AREAAI_MASSING;
			else if (eOldAreaAI == AREAAI_ASSAULT)
				eNewAreaAI = AREAAI_OFFENSIVE;
		}
		if (eNewAreaAI != eOldAreaAI)
			kArea.setAreaAIType(m_eAgent, eNewAreaAI);
	}
}


bool UWAI::Team::reviewPlan(TeamTypes eTarget, int iU, int iPrepTurns)
{
	CvTeamAI& kAgent = GET_TEAM(m_eAgent);
	WarPlanTypes const eWP = kAgent.AI_getWarPlan(eTarget);
	FAssert(eWP != NO_WARPLAN);
	bool bAtWar = kAgent.isAtWar(eTarget);
	int iWPAge = kAgent.AI_getWarPlanStateCounter(eTarget);
	FAssert(iWPAge >= 0);
	m_pReport->log("Reviewing war plan \"%s\" (age: %d turns) against %s (%su=%d)",
			m_pReport->warPlanName(eWP), iWPAge, m_pReport->teamName(eTarget),
			(bAtWar ? "at war; " : ""), iU);
	if (bAtWar)
	{
		FAssert(eWP != WARPLAN_PREPARING_LIMITED && eWP != WARPLAN_PREPARING_TOTAL);
		if (!considerPeace(eTarget, iU))
			return false;
		considerPlanTypeChange(eTarget, iU);
		/*  Changing between attacked_recent, limited and total is unlikely
			to affect our other war plans, so ignore the return value of
			considerPlanTypeChange and report "no changes" to the caller. */
		return true;
	}
	else
	{
		if (!canSchemeAgainst(eTarget, true))
		{
			m_pReport->log("War plan \"%s\" canceled b/c %s is no longer a legal target",
					m_pReport->warPlanName(eWP), m_pReport->teamName(eTarget));
			if (!isInBackground())
			{
				kAgent.AI_setWarPlan(eTarget, NO_WARPLAN);
				showWarPlanAbandonedMsg(eTarget);
			}
			return false;
		}
		if (eWP != WARPLAN_PREPARING_LIMITED && eWP != WARPLAN_PREPARING_TOTAL)
		{
			FAssert(eWP == WARPLAN_LIMITED || eWP == WARPLAN_TOTAL ||
					// UWAI doesn't use dogpile war plans
					(isInBackground() && eWP == WARPLAN_DOGPILE));
			if (iU < 0)
			{
				m_pReport->log("Imminent war canceled; no longer worthwhile");
				if (!isInBackground())
				{
					kAgent.AI_setWarPlan(eTarget, NO_WARPLAN);
					showWarPlanAbandonedMsg(eTarget);
				}
				return false;
			}
			else
			{
				// Consider switching when war remains imminent for a long time
				scaled rSwitchProb = std::min(fixp(1/3.), iWPAge * fixp(0.04));
				m_pReport->log("pr of considering to switch target: %d",
						rSwitchProb.getPercent());
				if (SyncRandSuccess(rSwitchProb))
				{
					/*  Hack: considerSwitchTarget was written under the assumption
						that no war is imminent. Might be difficult to rectify;
						change the war plan temporarily instead. */
					kAgent.AI_setWarPlanNoUpdate(eTarget, WARPLAN_PREPARING_LIMITED);
					bool const bSwitch = !considerSwitchTarget(eTarget, iU, 0);
					/*  If we do switch, then considerSwitchTarget has
						already reset the war plan against targetId --
						except when running in the background. */
					if (!bSwitch || isInBackground())
						kAgent.AI_setWarPlanNoUpdate(eTarget, eWP);
					if (bSwitch)
						return false;
				}
			}
			CvMap const& kMap = GC.getMap();
			// 12 turns for a (AdvCiv) Standard-size map, 9 on Small.
			int iTimeout = std::max(kMap.getGridWidth(), kMap.getGridHeight()) / 7;
			// Checking missions is a bit costly, don't do it if timeout isn't near.
			if (iWPAge > iTimeout)
			{
				// Akin to code in CvTeamAI::AI_endWarVal
				for(MemberAIIter itMember(kAgent.getID()); itMember.hasNext(); ++itMember)
				{
					if (itMember->AI_isAnyEnemyTargetMission(eTarget))
					{
						iTimeout *= 2;
						break;
					}
				}
			}
			if (iWPAge > iTimeout)
			{
				m_pReport->log("Imminent war canceled b/c of timeout (%d turns)",
						iTimeout);
				if (!isInBackground())
				{
					kAgent.AI_setWarPlan(eTarget, NO_WARPLAN);
					showWarPlanAbandonedMsg(eTarget);
				}
				return false;
			}
			m_pReport->log("War remains imminent (%d turns until timeout)",
					1 + iTimeout - iWPAge);
		}
		else
		{
			if (!considerConcludePreparations(eTarget, iU, iPrepTurns))
				return false;
			if (!considerAbandonPreparations(eTarget, iU, iPrepTurns))
				return false;
			if (!considerSwitchTarget(eTarget, iU, iPrepTurns))
				return false;
		}
	}
	return true;
}


bool UWAI::Team::considerPeace(TeamTypes eTarget, int iU)
{
	CvTeamAI& kAgent = GET_TEAM(m_eAgent);
	if (!kAgent.canChangeWarPeace(eTarget))
		return true;
	CvTeamAI& kTarget = GET_TEAM(eTarget);
	scaled rPeaceThresh = peaceThreshold(eTarget);
	bool const bHuman = kTarget.isHuman();
	if (bHuman)
	{
		/*	They might pay us for peace (whereas, for AI-AI deals, the side
			that expects to be paid waits for the other side to sue for peace). */
		rPeaceThresh += 10;
	}
	m_pReport->log("Threshold for seeking peace: %d", rPeaceThresh.round());
	if (iU >= rPeaceThresh)
	{
		/*  Peace so we can free our hands for a different war.
			(The "distraction" war utility aspect also deals with this,
			but it's normally not enough to get the AI to stop a successful
			war before starting one that looks even more worthwhile.) */
		for (TeamIter<FREE_MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> itOther(kAgent.getID());
			itOther.hasNext(); ++itOther)
		{
			TeamTypes const eOther = itOther->getID();
			if (!kAgent.AI_isSneakAttackReady(eOther))
				continue;
			FAssert(eOther != eTarget);
			m_pReport->log("Considering peace with %s to focus on"
					" imminent war against %s; evaluating two-front war:",
					m_pReport->teamName(eTarget), m_pReport->teamName(eOther));
			WarEvalParameters params(kAgent.getID(), eOther, *m_pReport, true);
			params.addExtraTarget(eTarget);
			/*  We're sure that we want to attack otherId.
				Only consider peace with the ExtraTarget. */
			params.setNotConsideringPeace();
			WarEvaluator eval(params);
			static int const iUWAI_MULTI_WAR_RELUCTANCE = GC.getDefineINT("UWAI_MULTI_WAR_RELUCTANCE");
			/*  Check both limited and total war instead of kAgent.AI_getWarPlan(eOther)
				-- to avoid a preference for the two-front case on account of
				greater military build-up. */
			int uLim = eval.evaluate(WARPLAN_LIMITED, 0) - iUWAI_MULTI_WAR_RELUCTANCE;
			int uTot = eval.evaluate(WARPLAN_TOTAL, 0) - iUWAI_MULTI_WAR_RELUCTANCE;
			iU = std::min(uLim, uTot);
			// Tbd.: If the war plan against otherId is TOTAL ...
			m_pReport->log("Utility of a two-front war compared with a war "
					"only against %s: %d", m_pReport->teamName(eOther), iU);
			break; // Only one war can be imminent at a time
		}
		if (iU >= rPeaceThresh)
		{
			m_pReport->log("No peace sought b/c war utility is above the peace threshold");
			return true;
		}
	}
	// We refuse to talk for 1 turn
	if (kAgent.AI_getAtWarCounter(eTarget) <= 1)
	{
		m_pReport->log("Too early to consider peace");
		return true;
	}
	CvPlayerAI& kTargetPlayer = GET_PLAYER(kTarget.getRandomMemberAlive(true));
	CvPlayerAI& kAgentPlayer = GET_PLAYER(kAgent.getRandomMemberAlive(false));
	if (!kAgentPlayer.canContact(kTargetPlayer.getID(), true))
	{
		m_pReport->log("Can't talk to %s about peace",
				m_pReport->leaderName(kTargetPlayer.getID()));
		return true; // Can't contact them for capitulation either
	}
	scaled rPeaceProb;
	bool bOfferPeace = true;
	int iTheirReluct = MIN_INT; // Costly, don't compute this sooner than necessary.
	if (bHuman)
	{
		int const iContactDelay = kAgentPlayer.
				AI_getContactTimer(kTargetPlayer.getID(), CONTACT_PEACE_TREATY);
		int const iContactRand = GC.getInfo(kAgentPlayer.
				getPersonalityType()).getContactRand(CONTACT_PEACE_TREATY);
		int iAtWarCounter = kAgent.AI_getAtWarCounter(eTarget);
		if (iContactDelay > 0 || iContactRand <= 0 ||
			kAgent.AI_getWarPlan(eTarget) == WARPLAN_ATTACKED_RECENT ||
			kAgentPlayer.AI_refuseToTalkTurns(kTargetPlayer.getID()) > iAtWarCounter)
		{
			if (iContactDelay > 0)
			{
				m_pReport->log("No peace with human sought b/c of contact delay: %d",
						iContactDelay);
			}
			else if (iContactRand <= 0)
			{
				m_pReport->log("No peace sought b/c %s never seeks peace",
						m_pReport->leaderName(kAgentPlayer.getID()));
			}
			else m_pReport->log("No peace sought b/c war too recent: %d turns", iAtWarCounter);
			rPeaceProb = 0; // Don't return; capitulation always needs to be checked.
			bOfferPeace = false;
		}
		else
		{
			/*	(Going through CvPlayerAI::AI_contactRoll gets too complicated here,
				and wouldn't matter b/c we don't speed-adjust peace rolls.) */
			rPeaceProb = scaled(1, iContactRand); // 5 to 10%
			// Adjust probability based on whether peace looks like win-win or zero-sum
			iTheirReluct = kTarget.uwai().reluctanceToPeace(kAgent.getID(), false);
			scaled rWinWinFactor = scaled(iTheirReluct + iU, -15);
			if (rWinWinFactor < 0)
			{
				rWinWinFactor.flipSign();
				rWinWinFactor.decreaseTo(fixp(2.5));
				rWinWinFactor.flipFraction();
			}
			else rWinWinFactor.decreaseTo(fixp(2.5));
			/*  Tbd.: (5*2.5)% seems a bit much for leaders that should be reluctant
				to sue for peace. Exponentiate rPeaceProb? Subtract a percentage point
				or two before applying the rWinWinFactor? */
			rPeaceProb *= rWinWinFactor;
			m_pReport->log("Win-win factor: %d percent", rWinWinFactor.getPercent());
		}
	}
	else
	{
		FAssert(iU < rPeaceThresh);
		rPeaceProb = (rPeaceThresh - iU).sqrt() * fixp(0.03);
	}
	if (bOfferPeace)
	{
		m_pReport->log("Probability for peace negotiation: %d percent",
				rPeaceProb.getPercent());
		if (SyncRandSuccess(1 - rPeaceProb))
		{
			m_pReport->log("Peace negotiation randomly skipped");
			if (!bHuman)
			{
				// Don't consider capitulation to AI w/o having tried peace negotiation
				return true;
			}
			bOfferPeace = false;
		}
	}
	if (iTheirReluct == MIN_INT)
		iTheirReluct = kTarget.uwai().reluctanceToPeace(kAgent.getID(), false);
	m_pReport->log("Their reluctance to peace: %d", iTheirReluct);
	if (bOfferPeace)
	{
		if (iTheirReluct <= iMaxReparationUtility)
		{
			int iTradeVal = 0;
			int iDemandVal = 0; // (Demand only from humans)
			if (bHuman)
			{
				iTradeVal = endWarVal(eTarget) - kTarget.uwai().endWarVal(kAgent.getID());
				// A bit higher than the K-Mod discounts (advc.134a)
				scaled const rDiscountFactor = fixp(1.3);
				if (iTradeVal < 0)
				{
					iDemandVal = -iTradeVal;
					// Offer a square deal when it's close
					if (iDemandVal < kTargetPlayer.uwai().utilityToTradeVal(fixp(4.25)))
						iDemandVal = 0;
					else iDemandVal = (iDemandVal / rDiscountFactor).uround();
					m_pReport->log("Seeking reparations with a trade value of %d", iDemandVal);
					iTradeVal = 0;
				}
				else iTradeVal = (iTradeVal * rDiscountFactor).uround();
			}
			else
			{
				// Base the reparations they demand on their economy
				iTradeVal = (kTarget.uwai().utilityToTradeVal(
						std::max(0, iTheirReluct))).uround();
				/*  Reduce the trade value b/c the war isn't completely off the table;
					could continue after 10 turns. */
				iTradeVal = (iTradeVal * rReparationsModifierAI).uround();
			}
			if (iTradeVal > 0 || iDemandVal == 0)
			{
				m_pReport->log("Trying to offer reparations with a trade value of %d",
						iTradeVal);
			}
			bool bPeace = false;
			if (!isInBackground())
			{
				bPeace = kAgentPlayer.AI_negotiatePeace(kTargetPlayer.getID(),
						iDemandVal, iTradeVal);
			}
			if (bHuman)
			{
				if (bPeace)
					m_pReport->log("Peace offer sent");
				else m_pReport->log("Failed to find a peace offer");
			}
			else m_pReport->log("Peace negotiation %s", (bPeace ? "succeeded" : "failed"));
			return !bPeace;
		}
		else m_pReport->log("No peace negotiation attempted; they're too reluctant");
	}
	if (considerCapitulation(eTarget, iU, iTheirReluct))
		return true; // No surrender
	int const iCities = kAgent.getNumCities();
	/*  Otherwise, considerCapitulation guarantees that surrender (to AI)
		is possible; before we do it, one last attempt to find help: */
	if (iCities > 1 && !tryFindingMaster(eTarget))
		return false; // Have become a vassal, or awaiting human response.
	// Liberate any colonies (to leave sth. behind, or just to spite the enemy)
	if (!isInBackground())
	{
		for (MemberAIIter it(kAgent.getID()); it.hasNext(); ++it)
			it->AI_doSplit(true);
	}
	if (kAgent.getNumCities() != iCities)
	{
		m_pReport->log("Empire split");
		return false; // Leads to re-evaluation of war plans; may yet capitulate.
	}
	if (kAgentPlayer.AI_getContactTimer(kTargetPlayer.getID(), CONTACT_PEACE_TREATY) <= 0)
	{
		m_pReport->log("%s capitulation to %s", bHuman ? "Offering" : "Implementing",
				m_pReport->leaderName(kTargetPlayer.getID()));
		if (!isInBackground())
		{
			kAgentPlayer.AI_offerCapitulation(kTargetPlayer.getID());
			return false;
		}
	}
	return true;
}


bool UWAI::Team::considerCapitulation(TeamTypes eMaster, int iAgentWarUtility,
	int iMasterReluctancePeace)
{
	{
		int const iUtilityThresh = -75;
		if (iAgentWarUtility * 4 > iUtilityThresh)
		{
			m_pReport->log("Don't compute capitulation utility b/c probably"
					" not low enough (%d>%d)", iAgentWarUtility, iUtilityThresh / 4);
			return true;
		}
		if (iAgentWarUtility > iUtilityThresh)
		{
			int iCapitulationUtility = iAgentWarUtility;
			if (GET_TEAM(m_eAgent).getNumWars(true, true) > 1)
			{
				/*	Looks like war utility is low, but not low enough. Perhaps
					this is b/c we haven't yet accounted for the protection that
					the master grants us from third parties.
					NB: Ideally, considerCapitulation should not rely on iAgentWarUtility
					at all when there are multiple (free) war enemies, but that's
					now difficult to change at the call site. */
				m_pReport->log("Computing war utility of capitulation (%d>%d)",
						iAgentWarUtility, iUtilityThresh);
				WarEvalParameters params(m_eAgent, eMaster, *m_pReport, false,
						NO_PLAYER, eMaster);
				WarEvaluator eval(params);
				iCapitulationUtility = eval.evaluate(GET_TEAM(m_eAgent).AI_getWarPlan(eMaster));
			}
			if (iCapitulationUtility > iUtilityThresh)
			{
				m_pReport->log("No capitulation b/c utility not low enough (%d>%d)",
						iCapitulationUtility, iUtilityThresh);
				return true;
			}
		}
	}
	/*  Low reluctance to peace can just mean that there isn't much left for
		them to conquer; doesn't have to mean that they'll soon offer peace.
		Probability test to ensure that we eventually capitulate even if
		master's reluctance remains low. */
	scaled rSkipProb = 1 - (iMasterReluctancePeace * fixp(0.015) + fixp(0.3));
	int const iAgentCities = GET_TEAM(m_eAgent).getNumCities();
	rSkipProb.clamp(0,
			// Reduce maximal waiting time in the late game
			fixp(0.87) - fixp(0.04) * GET_TEAM(eMaster).AI_getCurrEraFactor());
	// If few cities remain, we can't afford to wait.
	if (iAgentCities <= 2)
		rSkipProb -= fixp(0.2);
	if (iAgentCities <= 1)
		rSkipProb -= fixp(0.1);
	m_pReport->log("%d percent probability to delay capitulation based on master's "
			"reluctance to peace (%d)", rSkipProb.getPercent(), iMasterReluctancePeace);
	if (SyncRandSuccess(rSkipProb))
	{
		m_pReport->log("No capitulation this turn");
		return true;
	}
	if (rSkipProb.isPositive())
		m_pReport->log("Not skipped");
	/*  Since capitulation trade denial is decided at the team level, it doesn't matter
		which team members are used. */
	CvPlayerAI const& kAgentLeader = GET_PLAYER(GET_TEAM(m_eAgent).getLeaderID());
	CvTeamAI const& kMaster = GET_TEAM(eMaster);
	if (!kAgentLeader.canTradeItem(kMaster.getLeaderID(), TradeData(TRADE_SURRENDER)))
	{
		m_pReport->log("Capitulation to %s impossible", m_pReport->teamName(eMaster));
		return true;
	}
	bool const bHumanMaster = GET_TEAM(eMaster).isHuman();
	/*  Make master team accept if it's not sure about continuing the war. Note that,
		due to change advc.130v, gaining a vassal can't really hurt the master. */
	bool const bCheckAccept = (!bHumanMaster && iMasterReluctancePeace >= 15);
	if (!bCheckAccept && !bHumanMaster)
	{
		m_pReport->log("Master accepts capitulation b/c of low reluctance to peace (%d)",
				iMasterReluctancePeace);
	}
	if (bHumanMaster)
	{
		// This allows AI_surrenderTrade to return true (for a human master)
		leaderCache().setReadyToCapitulate(eMaster, true);
	}
	// Checks our willingness and that of the master
	DenialTypes eDenial = GET_TEAM(m_eAgent).AI_surrenderTrade(
			eMaster, CvTeamAI::VASSAL_POWER_MOD_SURRENDER, bCheckAccept);
	if (eDenial != NO_DENIAL)
	{
		m_pReport->log("Not ready to capitulate%s; denial code: %d",
				bCheckAccept ? " (or master refuses)" : "", (int)eDenial);
		if (bHumanMaster)
		{
			/*  To ensure that the capitulation decision is made on an AI turn;
				so that tryFindingMaster and AI_doSplit are called by considerPeace. */
			leaderCache().setReadyToCapitulate(eMaster, false);
		}
		return true;
	}
	m_pReport->log("%s ready to capitulate to %s", m_pReport->teamName(m_eAgent),
			m_pReport->teamName(eMaster));
	return false;
}


bool UWAI::Team::tryFindingMaster(TeamTypes eEnemy)
{
	CvPlayerAI& kAgentPlayer = GET_PLAYER(GET_TEAM(m_eAgent).getRandomMemberAlive(false));
	for (TeamAIRandIter<FREE_MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> itMaster(syncRand(), m_eAgent);
		itMaster.hasNext(); ++itMaster)
	{
		CvTeamAI& kMaster = *itMaster;
		if (kMaster.isAtWar(m_eAgent) ||
			kMaster.isAtWar(eEnemy)) // No point if they're already our ally
		{
			continue;
		}
		CvPlayerAI& kMasterPlayer = GET_PLAYER(kMaster.getRandomMemberAlive(true));
		if (!kAgentPlayer.canContact(kMasterPlayer.getID(), true))
			continue;
		// Based on code in CvPlayerAI::AI_doDiplo
		TradeData item(TRADE_VASSAL);
		/*  Test Denial separately b/c it can cause the master to evaluate war
			against enemyId, which is costly. */
		if (!kAgentPlayer.canTradeItem(kMasterPlayer.getID(), item))
			continue;
		// Don't nag them (especially not humans)
		if (kAgentPlayer.AI_getContactTimer(kMasterPlayer.getID(),
			// Same contact memory for alliance and vassal agreement
			CONTACT_PERMANENT_ALLIANCE) != 0)
		{
			m_pReport->log("%s not asked for protection b/c recently contacted",
					m_pReport->leaderName(kMasterPlayer.getID()));
			continue;
		}
		// Checks both our and master's willingness
		if (kAgentPlayer.getTradeDenial(kMasterPlayer.getID(), item) != NO_DENIAL)
			continue;
		if (kMaster.isHuman())
		{
			m_pReport->log("Asking human %s for vassal agreement",
					m_pReport->leaderName(kMasterPlayer.getID()));
		}
		else m_pReport->log("Signing vassal agreement with %s",
				m_pReport->teamName(kMaster.getID()));
		if (!isInBackground())
{
			CLinkList<TradeData> ourList, theirList;
			ourList.insertAtEnd(item);
			if (kMaster.isHuman())
			{
				kAgentPlayer.AI_changeContactTimer(kMasterPlayer.getID(),
						CONTACT_PERMANENT_ALLIANCE,
						kAgentPlayer.AI_getContactDelay(CONTACT_PERMANENT_ALLIANCE));
				CvDiploParameters* pDiplo = new CvDiploParameters(kAgentPlayer.getID());
				pDiplo->setDiploComment(GC.getAIDiploCommentType("OFFER_VASSAL"));
				pDiplo->setAIContact(true);
				pDiplo->setOurOfferList(theirList);
				pDiplo->setTheirOfferList(ourList);
				gDLL->beginDiplomacy(pDiplo, kMasterPlayer.getID());
			}
			else
			{
				GC.getGame().implementDeal(kAgentPlayer.getID(),
						kMasterPlayer.getID(), ourList, theirList);
			}
		}
		return false;
	}
	m_pReport->log("No partner for a voluntary vassal agreement found");
	return true;
}


bool UWAI::Team::considerPlanTypeChange(TeamTypes eTarget, int iU)
{
	CvTeamAI& kAgent = GET_TEAM(m_eAgent);
	FAssert(kAgent.isAtWar(eTarget));
	WarPlanTypes const eWP = kAgent.AI_getWarPlan(eTarget);
	int const iWPAge = kAgent.AI_getWarPlanStateCounter(eTarget);
	WarPlanTypes eAltWP = NO_WARPLAN;
	switch (eWP)
	{
	case WARPLAN_ATTACKED_RECENT:
		// Same as BBAI in CvTeamAI::AI_doWar, but switch after 8 turns (not 10).
		if (iWPAge >= 4)
		{
			if (!GET_TEAM(eTarget).AI_isLandTarget(kAgent.getID()) || iWPAge >= 8)
			{
				m_pReport->log("Switching to war plan \"attacked\" after %d turns", iWPAge);
				if (!isInBackground())
				{
					kAgent.AI_setWarPlan(eTarget, WARPLAN_ATTACKED);
					// Don't reset wpAge
					kAgent.AI_setWarPlanStateCounter(eTarget, iWPAge);
				}
				return false;
			}
		}
		m_pReport->log("Too early to switch to \"attacked\" war plan");
		break;
	// Treat these three as limited wars, and consider switching to total.
	case WARPLAN_ATTACKED:
	case WARPLAN_DOGPILE:
	case WARPLAN_LIMITED:
		eAltWP = WARPLAN_TOTAL;
		break;
	case WARPLAN_TOTAL:
		eAltWP = WARPLAN_LIMITED;
		break;
	default: FErrorMsg("Unsuitable war plan type");
	}
	if (eAltWP == NO_WARPLAN)
		return true;
	UWAIReport silentReport(true);
	WarEvalParameters params(kAgent.getID(), eTarget, silentReport);
	WarEvaluator eval(params);
	int iAltU = eval.evaluate(eAltWP);
	m_pReport->log("Utility of alt. war plan (%s): %d",
			m_pReport->warPlanName(eAltWP), iAltU);
	scaled rSwitchProb;
	if (iAltU > iU)
	{
		// Increase both utility values if iU is close to 0
		int iPadding = 0;
		if (iU < 20)
			iPadding += 20 - iU;
		rSwitchProb = scaled(iAltU + iPadding, 4 * (iU + iPadding));
	}
	if (rSwitchProb.isPositive())
	{
		scaled const rLimitedWarWeight = limitedWarWeight();
		if (eAltWP == WARPLAN_LIMITED)
			rSwitchProb *= rLimitedWarWeight;
		else
		{
			rSwitchProb = (rLimitedWarWeight.isPositive() ?
					rSwitchProb / rLimitedWarWeight : 1);
		}
		if (rLimitedWarWeight != 1)
		{
			m_pReport->log("Bias for/against limited war: %d percent",
					rLimitedWarWeight.getPercent());
		}
	}
	m_pReport->log("Probability of switching: %d percent", rSwitchProb.getPercent());
	if (!rSwitchProb.isPositive())
		return true;
	if (SyncRandSuccess(rSwitchProb))
	{
		m_pReport->log("Switching to war plan \"%s\"", m_pReport->warPlanName(eAltWP));
		if (!isInBackground())
		{
			kAgent.AI_setWarPlan(eTarget, eAltWP);
			kAgent.AI_setWarPlanStateCounter(eTarget, iWPAge); // Don't reset wpAge
		}
		return false;
	}
	m_pReport->log("War plan not switched; still \"%s\"", m_pReport->warPlanName(eWP));
	return true;
}


bool UWAI::Team::considerAbandonPreparations(TeamTypes eTarget, int iU,
	int iTurnsRemaining)
{
	CvTeamAI& kAgent = GET_TEAM(m_eAgent);
	if (kAgent.AI_countWarPlans() > kAgent.getNumWars(true, true) + 1)
	{
		/*  Only one war should be imminent or in preparation at a time.
			(Otherwise WarEvaluator will ignore all but one plan).
			Too many plans can occur here only if UWAI was running
			in the background at some point. */
		if (!isInBackground())
		{
			kAgent.AI_setWarPlan(eTarget, NO_WARPLAN);
			showWarPlanAbandonedMsg(eTarget);
		}
		m_pReport->log("More than one war in preparation, canceling the one against %s",
				m_pReport->teamName(eTarget));
		return false;
	}
	if (iU >= 0)
		return true;
	if (iTurnsRemaining <= 0)
	{
		m_pReport->log("Time limit for preparations reached; plan abandoned");
		if (!isInBackground())
		{
			kAgent.AI_setWarPlan(eTarget, NO_WARPLAN);
			showWarPlanAbandonedMsg(eTarget);
		}
		return false;
	}
	WarPlanTypes eWP = kAgent.AI_getWarPlan(eTarget);
	if (isInBackground() && eWP == WARPLAN_DOGPILE)
		eWP = WARPLAN_PREPARING_LIMITED;
	int iWarRand = -1;
	if (eWP == WARPLAN_PREPARING_LIMITED)
		iWarRand = kAgent.AI_limitedWarRand();
	if (eWP == WARPLAN_PREPARING_TOTAL)
		iWarRand = kAgent.AI_maxWarRand();
	FAssert(iWarRand >= 0);
	// WarRand is between 40 (aggro) and 400 (chilled)
	scaled rAbandonProb(-iU * iWarRand, 7500);
	// Slight adjustment to training speed
	rAbandonProb *= 2;
	rAbandonProb /= per100(GC.getInfo(GC.getGame().getGameSpeedType()).
			getTrainPercent()) + 1;
	rAbandonProb.decreaseTo(1);
	m_pReport->log("Abandoning preparations with probability %d percent (warRand=%d)",
			rAbandonProb.getPercent(), iWarRand);
	if (SyncRandSuccess(rAbandonProb))
	{
		m_pReport->log("Preparations abandoned");
		if (!isInBackground())
		{
			kAgent.AI_setWarPlan(eTarget, NO_WARPLAN);
			showWarPlanAbandonedMsg(eTarget);
		}
		return false;
	}
	else m_pReport->log("Preparations not abandoned");
	return true;
}


bool UWAI::Team::considerSwitchTarget(TeamTypes eTarget, int iU,
	int iTurnsRemaining)
{
	CvTeamAI& kAgent = GET_TEAM(m_eAgent);
	WarPlanTypes const eWP = kAgent.AI_getWarPlan(eTarget);
	TeamTypes eBestAltTarget = NO_TEAM;
	int iBestUtility = 0;
	bool const bQualms = (iTurnsRemaining > 0 && kAgent.AI_isAvoidWar(eTarget, true));
	bool bAltQualms = false; // Qualms about attacking the alt. target
	for (TeamIter<FREE_MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> itAlt(kAgent.getID());
		itAlt.hasNext(); ++itAlt)
	{
		TeamTypes const eAltTarget = itAlt->getID();
		if (!canSchemeAgainst(eAltTarget, false) ||
			kAgent.turnsOfForcedPeaceRemaining(eAltTarget) > iTurnsRemaining)
		{
			continue;
		}
		bool bLoopQualms = kAgent.AI_isAvoidWar(eAltTarget, true);
		if (bLoopQualms && !bQualms)
			continue;
		UWAIReport silentReport(true);
		WarEvalParameters params(kAgent.getID(), eAltTarget, silentReport, true);
		WarEvaluator eval(params);
		int iAltU = eval.evaluate(eWP, iTurnsRemaining);
		if (iAltU > std::max(iBestUtility, bQualms ? 0 : iU))
		{
			eBestAltTarget = eAltTarget;
			iBestUtility = iAltU;
			bAltQualms = bLoopQualms;
		}
	}
	if (eBestAltTarget == NO_TEAM)
	{
		m_pReport->log("No other promising target for war preparations found");
		return true;
	}
	int iPadding = 0;
	if (std::min(iU, iBestUtility) < 20)
		iPadding += 20 - std::min(iU, iBestUtility);
	scaled rSwitchProb = fixp(0.75) * (1 - scaled(iU + iPadding, iBestUtility + iPadding));
	// Slight adjustment to training speed
	if (rSwitchProb.isPositive())
	{
		rSwitchProb *= 2;
		rSwitchProb /= per100(GC.getInfo(GC.getGame().getGameSpeedType()).
				getTrainPercent()) + 1;
	}
	if (bQualms && !bAltQualms)
		rSwitchProb += fixp(1.8);
	m_pReport->log("Switching target for war preparations to %s (u=%d) with pr=%d percent",
			m_pReport->teamName(eBestAltTarget), iBestUtility, rSwitchProb.getPercent());
	if (!SyncRandSuccess(rSwitchProb))
	{
		m_pReport->log("Target not switched");
		return true;
	}
	m_pReport->log("Target switched");
	if (!isInBackground())
	{
		int iWPAge = kAgent.AI_getWarPlanStateCounter(eTarget);
		kAgent.AI_setWarPlan(eTarget, NO_WARPLAN);
		showWarPlanAbandonedMsg(eTarget);
		kAgent.AI_setWarPlan(eBestAltTarget, eWP);
		showWarPrepStartedMsg(eBestAltTarget);
		kAgent.AI_setWarPlanStateCounter(eBestAltTarget, iWPAge);
	}
	return false;
}


bool UWAI::Team::considerConcludePreparations(TeamTypes eTarget, int iU,
	int iTurnsRemaining)
{
	CvTeamAI& kAgent = GET_TEAM(m_eAgent);
	if (kAgent.AI_countWarPlans() > kAgent.getNumWars(true, true) + 1)
	{
		// More than 1 war in preparation; let considerAbandonPreparations handle it.
		return true;
	}
	int const iTurnsOfPeace = kAgent.turnsOfForcedPeaceRemaining(eTarget);
	if (iTurnsOfPeace > 3)
	{
		m_pReport->log("Can't finish preparations b/c of peace treaty (%d turns"
				" to cancel)", iTurnsOfPeace);
		return true;
	}
	WarPlanTypes const eWP = kAgent.AI_getWarPlan(eTarget);
	WarPlanTypes eDirectWP = WARPLAN_LIMITED;
	if (eWP == WARPLAN_PREPARING_TOTAL)
		eDirectWP = WARPLAN_TOTAL;
	bool bConclude = false;
	if (iTurnsRemaining <= 0)
	{
		if (iU < 0)
			return true; // Let considerAbandonPreparations handle it
		m_pReport->log("Time limit for preparation reached; adopting direct war plan");
		bConclude = true;
	}
	else
	{
		UWAIReport silentReport(true);
		WarEvalParameters params(kAgent.getID(), eTarget, silentReport);
		WarEvaluator eval(params);
		int iDirectU = eval.evaluate(eDirectWP);
		m_pReport->log("Utility of immediate switch to direct war plan: %d", iDirectU);
		if (iDirectU > 0)
		{
			scaled rRandWeight = SyncRandFract(scaled);
			/*  The more time remains, the longer we'd still have to wait in order
				to achieve utility iU. Therefore use a low threshold
				if iTurnsRemaining is high.
				Example: 10 turns remaining, iU=80: thresh between 32 and 80.
						 8 turns later, if still iU=80: thresh between 64 and 80. */
			scaled rRandPortion(iTurnsRemaining, 10); 
			rRandPortion.decreaseTo(fixp(0.4));
			scaled rThresh = iU * ((1 - rRandPortion) + rRandWeight * rRandPortion);
			m_pReport->log("Utility threshold for direct war plan randomly set to %d",
					rThresh.round());
			if (iDirectU >= rThresh)
				bConclude = true;
			m_pReport->log("%sirect war plan adopted", (bConclude ? "D" : "No d"));
		}
	}
	if (bConclude)
	{
		if (!isInBackground())
		{
			// Don't AI_setWarPlanStateCounter, i.e. let CvTeamAI reset it to 0.
			kAgent.AI_setWarPlan(eTarget, eDirectWP);
		}
		return false;
	}
	return true;
}


int UWAI::Team::peaceThreshold(TeamTypes eTarget) const
{
	// Computation is similar to BtS CvPlayerAI::AI_isWillingToTalk
	CvTeamAI const& kAgent = GET_TEAM(m_eAgent);
	if (kAgent.isHuman())
		return 0;
	CvTeamAI const& kTarget = GET_TEAM(eTarget);
	scaled r = fixp(-7.5); // To give it time
	// Give it more time then; also more bitterness I guess.
	if (kAgent.AI_getWarPlan(eTarget) == WARPLAN_TOTAL)
		r -= 5;
	// If they're attacked or att. recent (they could switch to total war eventually)
	if (!kTarget.AI_isChosenWar(kAgent.getID()))
		r -= 5;
	{
		/*	Personality is handled at the player level, but all members
			need to count here. Therefore pass the team's MakePeaceRand. */
		scaled rPrideRating = leaderUWAI().prideRating(kAgent.AI_makePeaceRand());
		// (This puts the addend between -30 and 10)
		r += (1 - rPrideRating) * 40 - 30;
	}
	r += scaled::min(15, kAgent.AI_getAtWarCounter(eTarget) +
				(2 * kAgent.AI_getWarSuccess(eTarget) +
				4 * kTarget.AI_getWarSuccess(eTarget)) /
				GC.getWAR_SUCCESS_CITY_CAPTURING());
	int iR = r.round();
	if (!kTarget.isHuman())
	{
		/* Never set the threshold above 0 for inter-AI peace
			(let _them_ sue for peace instead) */
		iR = std::min(0, iR);
	}
	return iR;
}


int UWAI::Team::uJointWar(TeamTypes eTarget, TeamTypes eAlly) const
{
	// Only log about inter-AI war trades
	bool bSilent = (GET_TEAM(m_eAgent).isHuman() || GET_TEAM(eAlly).isHuman() ||
			!isReportTurn());
	/*  Joint war against vassal/ master: This function then gets called twice.
		The war evaluation is the same though; so disable logging for one of the calls. */
	if (GET_TEAM(eTarget).isAVassal())
	{
		bSilent = true;
		eTarget = GET_TEAM(eTarget).getMasterTeam();
	}
	UWAIReport report(bSilent);
	if (!bSilent)
	{
		report.log("h3.\nNegotiation of joint war\n");
		report.log("%s is evaluating the utility of %s joining the war"
				" against %s\n", report.teamName(m_eAgent),
				report.teamName(eAlly), report.teamName(eTarget));
	}
	WarEvalParameters params(m_eAgent, eTarget, report);
	params.addWarAlly(eAlly);
	params.setImmediateDoW(true);
	WarPlanTypes eWP = WARPLAN_LIMITED;
	if (GET_TEAM(m_eAgent).isAtWar(eTarget)) // (Currently always guarenteed by caller)
	{
		params.setNotConsideringPeace();
		eWP = NO_WARPLAN; // Evaluate the current plan
	}
	WarEvaluator eval(params);
	int iU = eval.evaluate(eWP);
	report.logNewline();
	/*  Military analysis might conclude that the ally is going to send some ships,
		enough to tip the scales. Highly unlikely to actually happen in the
		first half of the game. */
	if (!GET_TEAM(eAlly).uwai().isLandTarget(eTarget) &&
		GET_TEAM(eAlly).getCurrentEra() < CvEraInfo::AI_getAgeOfExploration())
	{
		iU = std::min(0, iU);
	}
	return iU;
}

int UWAI::Team::tradeValJointWar(TeamTypes eTarget, TeamTypes eAlly) const
{
	PROFILE_FUNC();
	/*  This function could handle a human ally, but the AI isn't supposed to
		pay humans for war (and I've no plans for changing that). */
	FAssert(!GET_TEAM(eAlly).isHuman());
	int iU = uJointWar(eTarget, eAlly); // Compares joint war with solo war
	/*  Low u suggests that we're not sure that we'll need help. Also,
		war evaluation doesn't account for MEMORY_HIRED_WAR_ALLY and
		CvTeam::makeUnwillingToTalk (advc.104o). */
	if (iU < 5 + 9 * scaled::hash(GC.getGame().getGameTurn(),
		GET_TEAM(m_eAgent).getLeaderID()))
	{
		return 0;
	}
	// NB: declareWarTrade applies an additional threshold
	return utilityToTradeVal(std::min(iU, -iWarTradeUtilityThresh)).uround();
}


int UWAI::Team::reluctanceToPeace(TeamTypes eEnemy, bool bNonNegative) const
{
	int iR = -uEndWar(eEnemy) - std::min(0, peaceThreshold(eEnemy));
	if (bNonNegative)
		return std::max(0, iR);
	return iR;
}


bool UWAI::Team::canSchemeAgainst(TeamTypes eTarget, bool bAssumeNoWarPlan,
	bool bCheckDefensivePacts) const
{
	CvTeamAI const& kAgent = GET_TEAM(m_eAgent);
	if (eTarget == NO_TEAM || eTarget == BARBARIAN_TEAM || eTarget == kAgent.getID())
		return false;
	// Vassals don't scheme
	if (kAgent.isAVassal())
		return false;
	CvTeam const& kTarget = GET_TEAM(eTarget);
	/*  advc.130o: Shouldn't attack right after peace from demand; therefore
		don't plan war during the peace treaty. */
	if (kAgent.isForcePeace(eTarget) &&
		kAgent.AI_getMemoryCount(eTarget, MEMORY_ACCEPT_DEMAND) > 0)
	{
		return false;
	}
	if (!(kTarget.isAlive() && !kTarget.isMinorCiv() && kAgent.isHasMet(eTarget) &&
		!kTarget.isAVassal() && kTarget.getNumCities() > 0 &&
		(bAssumeNoWarPlan || kAgent.AI_getWarPlan(eTarget) == NO_WARPLAN) &&
		kAgent.canEventuallyDeclareWar(eTarget)))
	{
		return false;
	}
	/*	Important not to scheme against a faraway member of a DP b/c that
		may delay our DoW considerably, may even require transports. CvUnitAI
		is only going to target cities of the target team and its vassals.
		The initial DoW matters for diplo penalties, but that's a less important
		consideration. */
	if (bCheckDefensivePacts)
	{
		for (TeamIter<FREE_MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> itAlly(eTarget);
			itAlly.hasNext(); ++itAlly)
		{
			if (itAlly->isDefensivePact(eTarget) &&
				/*	(Should come up rarely, so the performance of these checks
					shouldn't matter much. Closeness also gets cached, however,
					we may not be in a synchronized context, so we can't
					necessarily benefit from caching.) */
				canSchemeAgainst(itAlly->getID(), bAssumeNoWarPlan, false))
			{
				int iAllyCloseness = kAgent.AI_teamCloseness(itAlly->getID(),
						DEFAULT_PLAYER_CLOSENESS, false, true);
				for (TeamIter<MAJOR_CIV,VASSAL_OF> itVassal(itAlly->getID());
					itVassal.hasNext(); ++itVassal)
				{
					iAllyCloseness = std::max(iAllyCloseness,
							kAgent.AI_teamCloseness(itVassal->getID(),
							DEFAULT_PLAYER_CLOSENESS, false, true));
				}
				int iTargetCloseness = kAgent.AI_teamCloseness(eTarget,
						DEFAULT_PLAYER_CLOSENESS, false, true);
				for (TeamIter<MAJOR_CIV,VASSAL_OF> itVassal(eTarget);
					itVassal.hasNext(); ++itVassal)
				{
					iTargetCloseness = std::max(iTargetCloseness,
							kAgent.AI_teamCloseness(itVassal->getID(),
							DEFAULT_PLAYER_CLOSENESS, false, true));
				}
				if (2 * iAllyCloseness > 3 * iTargetCloseness)
					return false;
			}
		}
	}
	return true;
}


scaled UWAI::Team::limitedWarWeight() const
{
	int const iLimitedWarRand = GET_TEAM(m_eAgent).AI_limitedWarRand();
	if (iLimitedWarRand <= 0)
		return 0;
	/*  The higher rExp, the greater the impact of personal preference for
		limited or total war. */
	scaled const rExp = fixp(0.75);
	// Bias for total war b/c the WarRand values are biased toward limited war
	scaled const rBase = fixp(0.8) * GET_TEAM(m_eAgent).AI_maxWarRand() / iLimitedWarRand;
	FAssert(rBase >= 0);
	return rBase.pow(rExp);
}


namespace
{
	struct TargetData
	{
		TargetData(scaled rDrive, TeamTypes eTeam, bool bTotal, int iU)
		:	rDrive(rDrive), eTeam(eTeam), bTotal(bTotal), iU(iU)
		{}
		bool operator<(TargetData const& kOther) { return rDrive < kOther.rDrive; }
		scaled rDrive;
		TeamTypes eTeam;
		bool bTotal;
		int iU;
	};
}

void UWAI::Team::scheme()
{
	CvTeamAI& kAgent = GET_TEAM(m_eAgent);
	if (kAgent.AI_countWarPlans() > kAgent.getNumWars(true, true))
	{
		m_pReport->log("No scheming b/c already a war in preparation");
		return;
	}
	for (TeamAIIter<CIV_ALIVE> itMinor; itMinor.hasNext(); ++itMinor)
	{
		if (!itMinor->isMinorCiv())
			continue;
		int iCloseness = kAgent.AI_teamCloseness(itMinor->getID());
		if (iCloseness >= 40 && itMinor->getPower(false) * 3 > kAgent.getPower(true) &&
			itMinor->AI_isLandTarget(kAgent.getID()) &&
			kAgent.AI_isLandTarget(itMinor->getID()))
		{
			m_pReport->log("No scheming b/c busy fighting minor civ %s at closeness %d",
					m_pReport->teamName(itMinor->getID()), iCloseness);
			return;
		}
	}
	vector<TargetData> aTargets;
	scaled rTotalDrive;
	UWAICache& kCache = leaderCache();
	for (TeamIter<FREE_MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> itTarget(kAgent.getID());
		itTarget.hasNext(); ++itTarget)
	{
		TeamTypes const eTarget = itTarget->getID();
		if (!canSchemeAgainst(eTarget, true, false))
			kCache.setCanBeHiredAgainst(eTarget, false);
		if (!canSchemeAgainst(eTarget, false))
			continue;
		m_pReport->log("Scheming against %s", m_pReport->teamName(eTarget));
		bool bShortWork = kAgent.AI_isPushover(eTarget);
		if (bShortWork)
			m_pReport->log("Target assumed to be short work");
		bool bSkipTotal = (kAgent.AI_isAnyWarPlan() || bShortWork);
		/*  Skip scheming entirely if already in a total war? Probably too
			restrictive in the lategame. Perhaps have reviewWarPlans compute the
			smallest utility among current war plans, and skip scheming if that
			minimum is, say, -55 or less. */
		m_pReport->setMute(true);
		WarEvalParameters params(kAgent.getID(), eTarget, *m_pReport);
		WarEvaluator eval(params);
		int iTotalU = INT_MIN;
		bool bTotalNaval = false;
		int iTotalPrepTime = -1;
		if (!bSkipTotal)
		{
			iTotalU = eval.evaluate(WARPLAN_PREPARING_TOTAL);
			bTotalNaval = params.isNaval();
			iTotalPrepTime = params.getPreparationTime();
		}
		int const iLimitedU = eval.evaluate(WARPLAN_PREPARING_LIMITED, bShortWork ? 0 : -1);
		bool const bLimitedNaval = params.isNaval();
		int const iLimitedPrepTime = params.getPreparationTime();
		bool bTotal = false;
		if (iLimitedU < 0 && iTotalU > 0)
			bTotal = true;
		if (iLimitedU < 0 && iTotalU < 0) // Only relevant for logging
			bTotal = (iTotalU > iLimitedU);
		if (iLimitedU > 0 && iTotalU > 0)
		{
			scaled const rLimitedWarWeight = limitedWarWeight();
			if (rLimitedWarWeight != 1)
			{
				m_pReport->log("Bias for/against limited war: %d percent",
						rLimitedWarWeight.uround());
			}
			int const iPadding = SyncRandNum(40);
			bTotal = (iTotalU + iPadding > (iPadding + iLimitedU) * rLimitedWarWeight);
		}
		int iU = std::max(iLimitedU, iTotalU);
		m_pReport->setMute(false);
		static int const UWAI_REPORT_THRESH = GC.getDefineINT("UWAI_REPORT_THRESH");
		static int const UWAI_REPORT_THRESH_HUMAN = GC.getDefineINT("UWAI_REPORT_THRESH_HUMAN");
		int iReportThresh = (GET_TEAM(eTarget).isHuman() ?
				UWAI_REPORT_THRESH_HUMAN : UWAI_REPORT_THRESH);
		// Extra evaluation just for logging
		if (!m_pReport->isMute() && iU > iReportThresh)
		{
			if (bTotal)
				eval.evaluate(WARPLAN_PREPARING_TOTAL, bTotalNaval, iTotalPrepTime);
			else eval.evaluate(WARPLAN_PREPARING_LIMITED, bLimitedNaval, iLimitedPrepTime);
		}
		else
		{
			m_pReport->log("%s %s war has %d utility", bTotal ? "total" : "limited",
					((bTotal && bTotalNaval) || (!bTotal && bLimitedNaval)) ?
					"naval" : "", iU);
		}
		bool const bCanHireOld = kCache.canBeHiredAgainst(eTarget);
		kCache.updateCanBeHiredAgainst(eTarget, iU, iWarTradeUtilityThresh);
		bool const bCanHireNew = kCache.canBeHiredAgainst(eTarget);
		if (bCanHireOld != bCanHireNew)
		{
			if (bCanHireNew)
				m_pReport->log("Can now (possibly) be hired for war");
			else m_pReport->log("Can no longer be hired for war");
		}
		if (iU <= 0)
			continue;
		scaled rDrive = iU;
		/*  WarRand of e.g. Alexander and Montezuma 50 for total war, else 40;
			Gandhi and Mansa Musa 400 for total, else 200.
			I.e. peaceful leaders hesitate longer before starting war preparations;
			warlike leaders have more drive.
			(Could easily use DogpileWarRand here when the target is already
			in a war, but I think I've found a better use for DogpileWarRand
			in warConfidenceAllies. Less dogpiling on weak targets that way.) */
		scaled rDiv = (bTotal ? kAgent.AI_maxWarRand() : kAgent.AI_limitedWarRand());
		FAssert(rDiv >= 0);
		// Let's make the AI a bit less patient
		// Especially the peaceful types; this maps e.g. 400 to 296 and 40 to 33.
		//rDiv.exponentiate(fixp(0.95));
		/*	Not a good idea after all. Overall, UWAI tends to make peaceful leaders
			rather too utilitarian with their war plans, I've come to think.
			So let's adjust only linearly. */
		rDiv *= fixp(0.85);
		if (rDiv <= 0)
			rDrive = 0;
		else rDrive /= rDiv;
		/*  Delay preparations probabilistically (by lowering drive) when there's
			still a peace treaty */
		scaled rPeacePortionRemaining(kAgent.turnsOfForcedPeaceRemaining(eTarget),
				// +1.0 b/c I don't want 0 drive at this point
				GC.getDefineINT(CvGlobals::PEACE_TREATY_LENGTH) + 1);
		rPeacePortionRemaining.decreaseTo(fixp(0.95));
		// (Let's try it w/o exponentiation)
		rDrive *= (1 - rPeacePortionRemaining)/*.pow(fixp(1.5))*/;
		aTargets.push_back(TargetData(rDrive, eTarget, bTotal, iU));
		rTotalDrive += rDrive;
	}
	// Descending by drive
	std::sort(aTargets.rbegin(), aTargets.rend());
	for (size_t i = 0; i < aTargets.size(); i++)
	{
		TeamTypes const eTarget = aTargets[i].eTeam;
		scaled rDrive = aTargets[i].rDrive;
		// Conscientious hesitation
		if (kAgent.AI_isAvoidWar(eTarget, true))
		{
			rDrive -= rTotalDrive / 2;
			if (rDrive <= 0)
				continue;
		}
		WarPlanTypes const eWP = (aTargets[i].bTotal ? WARPLAN_PREPARING_TOTAL :
				WARPLAN_PREPARING_LIMITED);
		m_pReport->log("Drive for war preparations against %s: %d percent",
				m_pReport->teamName(eTarget), rDrive.getPercent());
		if (SyncRandSuccess(rDrive))
		{
			if (!isInBackground())
			{
				kAgent.AI_setWarPlan(eTarget, eWP);
				showWarPrepStartedMsg(eTarget);
			}
			m_pReport->log("War plan initiated (%s)", m_pReport->warPlanName(eWP));
			break; // Prepare only one war at a time
		}
		m_pReport->log("No preparations begun this turn");
		if (GET_TEAM(eTarget).isHuman() && aTargets[i].iU <= 23)
		{
			PlayerTypes eTargetPlayer = GET_TEAM(eTarget).getRandomMemberAlive(true);
			CvPlayerAI& kAgentPlayer = GET_PLAYER(kAgent.getRandomMemberAlive(false));
			if (kAgentPlayer.canContact(eTargetPlayer, true))
			{
				m_pReport->log("Trying to amend tensions with human %s",
						m_pReport->teamName(eTarget));
				if (!isInBackground())
				{
					if (kAgentPlayer.uwai().amendTensions(eTargetPlayer))
						m_pReport->log("Diplo message sent");
					else m_pReport->log("No diplo message sent");
				}
			}
			else
			{
				m_pReport->log("Can't amend tension b/c can't contact %s",
						m_pReport->leaderName(eTargetPlayer));
			}
		}
	}
}


DenialTypes UWAI::Team::declareWarTrade(TeamTypes eTarget, TeamTypes eSponsor) const
{
	if (!canReach(eTarget))
		return DENIAL_NO_GAIN;
	CvTeamAI const& kAgent = GET_TEAM(m_eAgent);
	CvTeam const& kSponsor = GET_TEAM(eSponsor);
	/*  Check canBeHiredAgainst only in large games (to reduce the number of
		war trade alerts seen by humans) */
	bool bInsufficientPayment = false;
	if (!kSponsor.isHuman() || kSponsor.getHasMetCivCount() < 8 ||
		leaderCache().canBeHiredAgainst(eTarget))
	{
		int iUtilityThresh = iWarTradeUtilityThresh + 2;
		UWAIReport silentReport(true);
		WarEvalParameters params(kAgent.getID(), eTarget, silentReport,
				false, kSponsor.getLeaderID());
		WarEvaluator eval(params, true);
		// Has to be negative; we can't be hired for free.
		int iU = std::min(-1, eval.evaluate(WARPLAN_LIMITED));
		if (iU > iUtilityThresh)
		{
			if (GET_TEAM(eSponsor).isHuman())
			{
				// Don't return NO_DENIAL if human can't pay enough
				int iHumanTradeVal = -1;
				/*	Would be nice if eSponsor were a player, but that seems
					difficult to change ... */
				for (MemberIter itSponsorMember(eSponsor);
					itSponsorMember.hasNext(); ++itSponsorMember)
				{
					for (MemberAIIter itAgentMember(kAgent.getID());
						itAgentMember.hasNext(); ++itAgentMember)
					{
						int iMemberTradeVal=-1;
						itAgentMember->uwai().canTradeAssets(
								utilityToTradeVal(-iUtilityThresh).round(),
								itSponsorMember->getID(), &iMemberTradeVal);
						iHumanTradeVal = std::max(iHumanTradeVal, iMemberTradeVal);
					}
				}
				iUtilityThresh = std::max(iUtilityThresh,
						- (tradeValToUtility(iHumanTradeVal) +
						// For gold that the human might be able to procure
						((GET_TEAM(eSponsor).isGoldTrading() ||
						kAgent.isGoldTrading() ||
						// Or they could ask nicely
						(GET_TEAM(eSponsor).isAtWar(eTarget) &&
						kAgent.AI_getAttitude(eSponsor) >= ATTITUDE_PLEASED)) ?
						(GC.getGame().isOption(GAMEOPTION_NO_TECH_TRADING) ? 6 : 4) : 0) +
						// For tech that the human might get access to soon
						(GET_TEAM(eSponsor).isTechTrading() ||
						kAgent.isTechTrading() ? 4 : 0)).round());
			}
			if (iU > iUtilityThresh)
				return NO_DENIAL;
			else bInsufficientPayment = true;
		}
		/* "Maybe we'll change our mind" when it's (very) close?
			No, don't provide this info after all. */
		/*if (iU > utilityThresh - 5)
			return DENIAL_RECENT_CANCEL;*/
	}
	// We don't know why utility is so small; can only guess.
	if (!bInsufficientPayment &&
		4 * kAgent.getPower(true) +
		(kSponsor.isAtWar(eTarget) ? 2 * kSponsor.getPower(true) : 0) <
		3 * GET_TEAM(eTarget).getPower(true))
	{
		return DENIAL_POWER_THEM;
	}
	if (kAgent.AI_anyMemberAtVictoryStage(AI_VICTORY_CULTURE4 | AI_VICTORY_SPACE4))
		return DENIAL_VICTORY;
	// "Too much on our hands" can mean anything
	return DENIAL_TOO_MANY_WARS;
}


int UWAI::Team::declareWarTradeVal(TeamTypes eTarget, TeamTypes eSponsor) const
{
	CvTeamAI const& kAgent = GET_TEAM(m_eAgent);
	bool const bSilent = (GET_TEAM(eSponsor).isHuman() || !isReportTurn());
	UWAIReport report(bSilent);
	if (!bSilent)
	{
		report.log("*Considering sponsored war*");
		report.log("%s is considering to declare war on %s at the request of %s",
				report.teamName(kAgent.getID()), report.teamName(eTarget),
				report.teamName(eSponsor));
		/*  Will see the above lines multiple times in the log when this team
			agrees to declare war b/c CvGame::implementDeal causes the dealValue
			to be recomputed twice for diplomatic consequences ("traded with enemy",
			"fair and forthright"). */
	}
	CvTeamAI const& kSponsor = GET_TEAM(eSponsor);
	// Don't log details of war evaluation
	UWAIReport silentReport(true);
	WarEvalParameters params(kAgent.getID(), eTarget, silentReport, false,
			kSponsor.getLeaderID());
	WarEvaluator eval(params);
	int iU = eval.evaluate(WARPLAN_LIMITED);
	/*  Sponsored war results in a peace treaty with the sponsor. Don't check if
		we're planning war against the sponsor - too easy to read (b/c there are
		just two possibilities). Instead check war utility against the sponsor. */
	if (canSchemeAgainst(eSponsor, true, false))
	{
		WarEvalParameters paramsVsSponsor(kAgent.getID(), eSponsor, silentReport);
		WarEvaluator evalVsSponsor(paramsVsSponsor);
		int iUtilityVsSponsor = evalVsSponsor.evaluate(WARPLAN_LIMITED, 3);
		if (iUtilityVsSponsor > 0)
			iU -= (fixp(2/3.) * iUtilityVsSponsor).round();
	}
	/*  Don't trust utility completely; human sponsor will try to pick the time
		when we're most willing. Need to be conservative. Also, apparently the
		sponsor gets sth. out of the DoW, and therefore we should always ask for
		a decent price, even if we don't mind declaring war. */
	int iLowerBound = -2;
	if (!kSponsor.isAtWar(eTarget))
		iLowerBound -= 4;
	// War utility is especially unreliable when things get desperate
	{
		int iWarSuccessRating = kAgent.AI_getWarSuccessRating();
		if (iWarSuccessRating < 0)
			iLowerBound += iWarSuccessRating / 10;
	}
	iU = std::min(iLowerBound, iU);
	scaled rPriceOurEconomy = utilityToTradeVal(-iU);
	scaled rPriceSponsorEconomy = kSponsor.uwai().utilityToTradeVal(-iU);
	/*  If the sponsor has the bigger economy, use the mean of the price based on
		our economy and his, otherwise, base it only on our economy. */
	scaled rPrice = (rPriceOurEconomy +
			std::max(rPriceOurEconomy, rPriceSponsorEconomy)) / 2;
	report.log("War utility: %d, base price: %d", iU, rPrice.round());
	/*  Adjust the price based on our attitude and obscure it so that humans
		can't learn how willing we are exactly */
	AttitudeTypes const eTowardSponsor = kAgent.AI_getAttitude(eSponsor);
	// 0.25 if pleased, 0.5 cautious, 1 furious
	scaled rAttitudeModifier(ATTITUDE_FRIENDLY - eTowardSponsor,
			ATTITUDE_FRIENDLY);
	// Mates' rates, but will still obscure the price (modifier != 0).
	if (eTowardSponsor == ATTITUDE_FRIENDLY)
		rAttitudeModifier = fixp(-0.25);
	/*  Put our money where our mouth is: discount for war on our worst enemy.
		(Other than that, our attitude toward the target is sufficiently reflected
		by war utility.) */
	if (kAgent.AI_getWorstEnemy() == eTarget)
	{
		rAttitudeModifier -= fixp(0.25);
		if (rAttitudeModifier == 0) // Avoid 0 for the sake of obscurity
			rAttitudeModifier -= fixp(0.25);
	}
	vector<int> aiInputs;
	/*  Allow hash to change w/e the target's rank or our attitude toward the
		sponsor changes */
	aiInputs.push_back(GC.getGame().getRankTeam(eTarget));
	aiInputs.push_back(eTowardSponsor);
	scaled rModifierWeight = fixp(0.6) * scaled::hash(aiInputs, kAgent.getLeaderID());
	scaled rObscuredPrice = rPrice * (1 + rAttitudeModifier * rModifierWeight);
	int iR = rObscuredPrice.roundToMultiple(10); // Makes gold cost a multiple of 5
	report.log("Obscured price: %d (attitude modifier: %d percent)\n", iR,
			rAttitudeModifier.getPercent());
	return iR;
}


DenialTypes UWAI::Team::makePeaceTrade(TeamTypes eEnemy, TeamTypes eBroker) const
{
	// Broker can't be involved in the war (not checked by caller; BtS allows it).
	if (GET_TEAM(eBroker).isAtWar(eEnemy))
		return DENIAL_JOKING;
	// (Willingness to talk is essentially a team-level decision; can use any members.)
	bool const bEnemyWillTalk = GET_PLAYER(GET_TEAM(m_eAgent).getLeaderID()).
			canContact(GET_TEAM(eEnemy).getLeaderID(), true);
	if (!bEnemyWillTalk && !gDLL->isDiplomacy())
	{
		// Don't waste time with a more specific answer if human won't read it anyway
		return DENIAL_RECENT_CANCEL;
	}
	int const iAgentReluct = reluctanceToPeace(eEnemy);
	int const iEnemyReluct = GET_TEAM(eEnemy).uwai().reluctanceToPeace(m_eAgent);
	bool bNoDenial = false; // Will still have to check bEnemyWillTalk then
	if (iEnemyReluct <= 0)
	{
		if (iAgentReluct < 55)
			bNoDenial = true;
		else
		{
			CvGameAI const& kGame = GC.AI_getGame();
			scaled rScoreRatio(kGame.getTeamScore(m_eAgent),
					kGame.getTeamScore(kGame.getRankTeam((TeamTypes)0)));
			scaled const rGameEra = kGame.AI_getCurrEraFactor();
			if (rGameEra > 0 &&
				rScoreRatio < ((rGameEra - 1) / rGameEra + fixp(2/3.)) / 2)
			{
				// We're not doing well in score; the broker might be doing much better.
				if (iAgentReluct < 70)
					bNoDenial = true;
				else return DENIAL_TOO_MUCH;
			}
			return DENIAL_VICTORY;
		}
	}
	if (!bEnemyWillTalk)
	{
		if (iAgentReluct <= 0 && iEnemyReluct > 0 && iEnemyReluct - iAgentReluct >= 15)
		{
			/*	They'll refuse with "not right now", so it's a bit pointless to
				"contact them", but if _we_ say "not right now" it'll be misleading
				b/c we probably won't be able to make peace even once they become
				willing to talk. */
			return DENIAL_CONTACT_THEM;
		}
		return DENIAL_RECENT_CANCEL;
	}
	if (bNoDenial)
		return NO_DENIAL;
	/*  Unusual case: both sides want to continue, so both would have to be paid
		by the broker, which is too complicated. "Not right now" is true enough -
		will probably change soon. */
	if (iAgentReluct > 0)
		return DENIAL_RECENT_CANCEL;
	return DENIAL_CONTACT_THEM;
}


int UWAI::Team::makePeaceTradeVal(TeamTypes eEnemy, TeamTypes eBroker) const
{
	int const iAgentReluct = reluctanceToPeace(eEnemy);
	// Demand at least a token payment
	scaled r = utilityToTradeVal(std::max(3, iAgentReluct));
	CvTeamAI const& kAgent = GET_TEAM(m_eAgent);
	AttitudeTypes eTowardBroker = kAgent.AI_getAttitude(eBroker);
	// Make it a bit easier to broker peace as part of a peace treaty
	if (kAgent.isAtWar(eBroker) && eTowardBroker < ATTITUDE_CAUTIOUS)
		eTowardBroker = ATTITUDE_CAUTIOUS;
	/*  Between 400% and 77%. 100% when we're pleased with both.
		We prefer to get even with our enemy, so letting the broker pay 1 for 1 is
		already a concession. */
	scaled rAttitudeModifier(10, 1 + 2 * eTowardBroker +
			GET_TEAM(eEnemy).AI_getAttitude(eBroker));
	rAttitudeModifier.decreaseTo(4);
	int iWarDuration = kAgent.AI_getAtWarCounter(eEnemy);
	FAssert(iWarDuration > 0);
	/*  warDuration could be as small as 1 I think. Then the mark-up is
		+175% in the Ancient era. None for a Renaissance war after 15 turns. */
	scaled rTimeModifier = (fixp(5.5) - kAgent.AI_getCurrEraFactor() / 2) /
			scaled(iWarDuration + 1).sqrt();
	rTimeModifier.increaseTo(fixp(0.75));
	r *= rAttitudeModifier * rTimeModifier;
	return kAgent.AI_roundTradeVal(r.round());
}


int UWAI::Team::endWarVal(TeamTypes eEnemy) const
{
	bool const bAgentHuman = GET_TEAM(m_eAgent).isHuman();
	FAssertMsg(bAgentHuman || GET_TEAM(eEnemy).isHuman(),
			"This should only be called for human-AI peace");
	CvTeamAI const& kHuman = (bAgentHuman ? GET_TEAM(m_eAgent) : GET_TEAM(eEnemy));
	CvTeamAI const& kAI =  (bAgentHuman ? GET_TEAM(eEnemy) : GET_TEAM(m_eAgent));
	int iAIReluct = kAI.uwai().reluctanceToPeace(kHuman.getID(), false);
	if (iAIReluct <= 0)
	{
		// If no payment is possible, human utility shouldn't matter.
		bool bCanTrade = false;
		for (MemberIter itHumanMember(kHuman.getID());
			itHumanMember.hasNext(); ++itHumanMember)
		{
			for (MemberIter itAIMember(kAI.getID());
				itAIMember.hasNext(); ++itAIMember)
			{
				if (itHumanMember->canPossiblyTradeItem(
					itAIMember->getID(), TRADE_GOLD) ||
					itHumanMember->canPossiblyTradeItem(
					itAIMember->getID(), TRADE_TECHNOLOGIES))
				{
					bCanTrade = true;
					break;
				}
			}
		}
		if (!bCanTrade)
			return 0;
	}
	// Really just utility given how peaceThreshold is computed for humans
	int iHumanUtility = kHuman.uwai().reluctanceToPeace(kAI.getID(), false);
	/*	Neither side pays if both want peace and the AI wants it
		more badly than the human - but not far more badly. */
	if (iHumanUtility <= 0 && iAIReluct < iHumanUtility &&
		iAIReluct >= 2 * iHumanUtility)
	{
		return 0;
	}
	scaled r;
	// Only AI wants to end the war or AI wants to end it much more badly
	if (iAIReluct < 0 && (iHumanUtility >= 0 || iAIReluct < 2 * iHumanUtility))
	{
		// Human pays nothing if AI pays
		if (bAgentHuman)
			return 0;
		if (iHumanUtility >= 0)
		{
			// Rely more on war utility of the AI side than on human war utility
			r = fixp(0.5) * (std::min(-iAIReluct, iHumanUtility) - iAIReluct);
		}
		/*	Both negative: A rather symbolic payment -
			unless the war is disastrous for the AI. */
		else r = iHumanUtility - fixp(0.5) * iAIReluct;
		/*  What if human declares war, but never sends units, although we believe
			that it would hurt us and benefit them (all things considered)?
			Then we're probably wrong somewhere and shouldn't trust our
			utility computations. */
		if (kAI.AI_getMemoryCount(kHuman.getID(), MEMORY_DECLARED_WAR) > 0 &&
			kAI.getNumCities() > 0)
		{
			scaled rWSDelta = scaled::max(0,
					kHuman.AI_getWarSuccess(kAI.getID())
					-kAI.AI_getWarSuccess(kHuman.getID()));
			scaled rWSAdjustment = (4 * rWSDelta) /
					(GC.getWAR_SUCCESS_CITY_CAPTURING() * kAI.getNumCities());
			rWSAdjustment.decreaseTo(1);
			r *= rWSAdjustment;
		}
		r = kAI.uwai().reparationsToHuman(r) * rReparationsModifierAI;
	}
	else
	{
		// AI pays nothing if human pays
		if (!bAgentHuman)
			return 0;
		// Don't demand payment if willing to capitulate to human
		if (kAI.AI_surrenderTrade(
			kHuman.getID(), CvTeamAI::VASSAL_POWER_MOD_SURRENDER, false) == NO_DENIAL)
		{
			return 0;
		}
		// (No limit on human reparations)
		if (iAIReluct > 0) // This is enough to make peace worthwhile for the AI
			r = kAI.uwai().utilityToTradeVal(iAIReluct);
		/*  But if human wants to end the war more badly than AI, AI also tries
			to take advantage of that. */
		if (iHumanUtility < 0)
		{
			/*  How much we try to squeeze the human. Not much b/c trade values
				go a lot higher now than they do in BtS. 5 utility can easily
				correspond to 1000 gold in the midgame. The AI evaluation of human
				utility isn't too reliable (may well assume that the human starts
				some costly but futile offensive) and fluctuates a lot from turn
				to turn, whereas peace terms mustn't fluctuate too much.
				And at least if iAIReluct < 0, we do want peace negotiations to
				succeed. */
			scaled rGreedFactor = fixp(0.05);
			if (iAIReluct > 0)
				rGreedFactor += fixp(0.1);
			int const iDelta = std::min(0, iAIReluct) - iHumanUtility;
			if (iDelta == 0)
				return 0;
			FAssert(iDelta > 0);
			// Conversion based on human's economy
			r += rGreedFactor * kHuman.uwai().utilityToTradeVal(iDelta);
			r *= rReparationsModifierHuman;
			/*  Demand less if human has too little. Akin to the
				tech/gold trading clause higher up.
				(Too lazy to implement this check properly for team games.) */
			if (iAIReluct < 0 && kHuman.getNumMembers() == 1)
			{
				int iMaxHumanCanPay = -1;
				kAI.uwai().leaderUWAI().canTradeAssets(
						r.round(), kHuman.getLeaderID(),
						&iMaxHumanCanPay);
				if (iMaxHumanCanPay < r)
				{
					/*  This means that the human player may want to make peace
						right away when the AI becomes willing to talk b/c the
						AI could change its mind again on the next turn. */
					if (scaled::hash(
						/*  Integer division to avoid flickering when the right side
							of the inequality is near 0.5. Don't just hash the
							game turn b/c that would mean that the AI can change its mind
							only every so many turns - too predictable. */
						(GC.getGame().getGameTurn() - kAI.AI_getWarSuccessRating()) / 8,
						kAI.getLeaderID()) < scaled(iAIReluct, -40))
					{
						r = iMaxHumanCanPay;
					}
				}
			}
		}
	}
	return r.round();
}


int UWAI::Team::uEndAllWars(VoteSourceTypes eVS) const
{
	vector<TeamTypes> aeWarEnemies;
	for (TeamIter<FREE_MAJOR_CIV,ENEMY_OF> itEnemy(m_eAgent);
		itEnemy.hasNext(); ++itEnemy)
	{
		if (eVS == NO_VOTESOURCE || itEnemy->isVotingMember(eVS))
			aeWarEnemies.push_back(itEnemy->getID());
	}
	if (aeWarEnemies.empty())
	{
		FAssert(!aeWarEnemies.empty());
		return 0;
	}
	bool const bSilent = !isReportTurn();
	UWAIReport report(bSilent);
	if (!bSilent)
	{
		report.log("h3.\nPeace vote\n");
		report.log("%s is evaluating the utility of war against %s in order to "
				"decide whether to vote for peace between self and everyone",
				report.teamName(m_eAgent), report.teamName(aeWarEnemies[0]));
	}
	WarEvalParameters params(m_eAgent, aeWarEnemies[0], report);
	for (size_t i = 1; i < aeWarEnemies.size(); i++)
	{
		params.addExtraTarget(aeWarEnemies[i]);
		report.log("War enemy: %s", report.teamName(aeWarEnemies[i]));
	}
	WarEvaluator eval(params);
	int iR = -eval.evaluate();
	report.logNewline();
	return iR;
}


int UWAI::Team::uJointWar(TeamTypes eTarget, VoteSourceTypes eVS) const
{
	bool const bSilent = !isReportTurn();
	UWAIReport report(bSilent);
	if (!bSilent)
	{
		report.log("h3.\nWar vote\n");
		report.log("%s is evaluating the utility of war against %s through diplo vote",
				report.teamName(m_eAgent), report.teamName(eTarget));
	}
	vector<TeamTypes> aeAllies;
	for(PlayerIter<FREE_MAJOR_CIV,POTENTIAL_ENEMY_OF> itAlly(eTarget);
		itAlly.hasNext(); ++itAlly)
	{
		if (itAlly->isVotingMember(eVS) && itAlly->getTeam() != m_eAgent &&
			!GET_TEAM(itAlly->getTeam()).isAtWar(eTarget))
		{
			report.log("%s would join as a war ally",
					report.leaderName(itAlly->getID()));
			aeAllies.push_back(itAlly->getTeam());
		}
	}
	WarEvalParameters params(m_eAgent, eTarget, report);
	for (size_t i = 0; i < aeAllies.size(); i++)
		params.addWarAlly(aeAllies[i]);
	params.setImmediateDoW(true);
	WarPlanTypes eWP = WARPLAN_LIMITED;
	// (CvPlayerAI::AI_diploVote actually rules this out)
	if (GET_TEAM(m_eAgent).isAtWar(eTarget))
	{
		params.setNotConsideringPeace();
		eWP = NO_WARPLAN; // evaluate the current plan
	}
	WarEvaluator eval(params);
	int iR = eval.evaluate(eWP);
	report.logNewline();
	return iR;
}


int UWAI::Team::uEndWar(TeamTypes eEnemy) const
{
	UWAIReport silentReport(true);
	WarEvalParameters params(m_eAgent, eEnemy, silentReport);
	WarEvaluator eval(params);
	return -eval.evaluate();
}


scaled UWAI::Team::reparationsToHuman(scaled rUtility) const
{
	/*  iMaxReparationUtility is the upper limit for inter-AI peace;
		be less generous with humans */
	scaled const rTop(4 * iMaxReparationUtility, 5);
	/*  If utility for reparations is above the cap, we become less
		willing to pay b/c we don't believe that the peace can last. */
	if (rUtility > rTop)
	{
		scaled const rBottom = rTop / 4;
		scaled const rGradient(-1, 6);
		scaled rDelta = (rUtility - rTop);
		/*	Decreasing linearly from top to bottom seems a bit too
			steep for small delta. Choose an exponent and divisor
			so that the delta for which rUtility reaches the bottom
			remains unchanged (fixpoint). */
		scaled const rDeltaBottom = (-1 / rGradient) * (rTop - rBottom);
		int const iDiv = 3;
		// Tbd.: Add a logarithm function to ScaledNum
		double const dDeltaBottom = rDeltaBottom.getDouble();
		double const dExponent = std::log(dDeltaBottom * iDiv) /
				std::log(dDeltaBottom);
		scaled const rExponent = scaled::fromDouble(dExponent);
		rDelta.exponentiate(rExponent);
		rDelta /= iDiv;
		rUtility = std::max(rBottom, rTop + rDelta * rGradient);
	}
	return utilityToTradeVal(rUtility); // Trade value based on our economy
}


void UWAI::Team::respondToRebuke(TeamTypes eTarget, bool bPrepare)
{
	/*  Caveat: Mustn't use RNG here b/c this is called from both async (bPrepare=false)
		and sync (bPrepare=true) contexts */
	CvTeamAI& kAgent = GET_TEAM(m_eAgent);
	if (!canSchemeAgainst(eTarget, true) || (bPrepare ?
		kAgent.AI_isSneakAttackPreparing(eTarget) :
		kAgent.AI_isSneakAttackReady(eTarget)))
	{
		return;
	}
	if (!bPrepare && !kAgent.canDeclareWar(eTarget))
		return;
	FAssert(GET_TEAM(eTarget).isHuman());
	UWAIReport silentReport(true);
	WarEvalParameters params(kAgent.getID(), eTarget, silentReport);
	WarEvaluator eval(params);
	int const iU = eval.evaluate(bPrepare ? WARPLAN_PREPARING_LIMITED : WARPLAN_LIMITED);
	if (iU < 0)
		return;
	if (bPrepare)
		kAgent.AI_setWarPlan(eTarget, WARPLAN_PREPARING_LIMITED);
	else kAgent.AI_setWarPlan(eTarget, WARPLAN_LIMITED);
}


DenialTypes UWAI::Team::acceptVassal(TeamTypes eVassal) const
{
	CvTeamAI const& kAgent = GET_TEAM(m_eAgent);
	vector<TeamTypes> aeWarEnemies; // Just the new ones
	for (TeamIter<FREE_MAJOR_CIV,ENEMY_OF> itEnemy(eVassal);
		itEnemy.hasNext(); ++itEnemy)
	{
		if (!itEnemy->isAtWar(kAgent.getID()))
		{
			aeWarEnemies.push_back(itEnemy->getID());
			FAssert(kAgent.isHasMet(itEnemy->getID())); // eVassal shouldn't ask us then
		}
	}
	if (aeWarEnemies.empty())
	{
		FAssert(!aeWarEnemies.empty());
		return NO_DENIAL;
	}
	/*  Ideally, WarEvaluator would have a mode for assuming a vassal agreement,
		and would do everything this function needs. I didn't think of this early
		enough. As it is, WarEvaluator can handle the resulting wars well enough,
		but won't account for the utility of us gaining a vassal, nor for any
		altruistic desire to protect the vassal. (Assistance::evaluate isn't
		altruistic.)
		GreedForVassals::evaluate has quite sophisticated code for evaluating
		vassals, but can't be easily separated from the context of WarEvaluator.
		I'm using only the cached part of that computation. */
	bool const bSilent = (kAgent.isHuman() || !isReportTurn());
	UWAIReport report(bSilent);
	if (!bSilent)
	{
		report.log("h3.\nConsidering war to accept vassal\n");
		report.log("%s is considering to accept %s as its vassal; implied DoW on:",
				report.teamName(kAgent.getID()), report.teamName(eVassal));
		for (size_t i = 0; i < aeWarEnemies.size(); i++)
			report.log("%s", report.teamName(aeWarEnemies[i]));
	}
	int iResourceScore = 0;
	int iTechScore = 0;
	for (MemberIter itVassalMember(eVassal);
		itVassalMember.hasNext(); ++itVassalMember)
	{
		iResourceScore += leaderCache().vassalResourceScore(
				itVassalMember->getID());
		iTechScore += leaderCache().vassalTechScore(
				itVassalMember->getID());
	}
	// resourceScore is already utility
	scaled rVassalUtility = tradeValToUtility(iTechScore) + iResourceScore;
	report.log("%d utility from vassal resources, %d from tech", iResourceScore,
			(rVassalUtility - iResourceScore).round());
	rVassalUtility += scaled(GET_TEAM(eVassal).getNumCities() * 30,
			kAgent.getNumCities() + 1);
	if (kAgent.AI_anyMemberAtVictoryStage(
		AI_VICTORY_DIPLOMACY4 | AI_VICTORY_CONQUEST4))
	{
		rVassalUtility *= 2;
	}
	else if (kAgent.AI_anyMemberAtVictoryStage(
		AI_VICTORY_DIPLOMACY3 | AI_VICTORY_CONQUEST3))
	{
		rVassalUtility *= fixp(1.4);
	}
	/*  If the war will go badly for us, we'll likely not be able to protect
		the vassal. rVassalUtility therefore mustn't be so high that it could
		compensate for a lost war; should only compensate for bad diplo and
		military build-up.
		Except, maybe, if we're Friendly toward the vassal (see below). */
	rVassalUtility.decreaseTo(25);
	report.log("Utility after adding vassal cities: %d", rVassalUtility.round());
	/*  CvTeamAI::AI_vassalTrade already does an attitude check - we know we don't
		_dislike_ the vassal */
	if (kAgent.AI_getAttitude(eVassal) >= ATTITUDE_FRIENDLY)
	{
		rVassalUtility += 5;
		report.log("Utility increased b/c of attitude");
	}
	//UWAIReport silentReport(true); // use this one for fewer details
	WarEvalParameters params(kAgent.getID(), aeWarEnemies[0], report);
	for (size_t i = 1; i < aeWarEnemies.size(); i++)
		params.addExtraTarget(aeWarEnemies[i]);
	params.setImmediateDoW(true);
	WarEvaluator eval(params);
	int iWarUtility = eval.evaluate(WARPLAN_LIMITED);
	report.log("War utility: %d", iWarUtility);
	int iTotalUtility = rVassalUtility.round() + iWarUtility;
	if (iTotalUtility > 0)
	{
		report.log("Accepting vassal\n");
		return NO_DENIAL;
	}
	report.log("Vassal not accepted\n");
	// Doesn't matter which denial; no one gets to read this.
	return DENIAL_POWER_THEM;
}


bool UWAI::Team::isLandTarget(TeamTypes eTeam) const
{
	PROFILE_FUNC();
	bool bHasCoastalCity = false;
	bool bCanReachAnyByLand = false;
	int iDistLimit = getUWAI().maxLandDist();
	for (MemberAIIter itMember(m_eAgent); itMember.hasNext(); ++itMember)
	{
		UWAICache const& kCache = itMember->uwai().getCache();
		// Sea route then unlikely to be much slower
		if (!kCache.canTrainDeepSeaCargo())
			iDistLimit = MAX_INT;
		for (int j = 0; j < kCache.numCities(); j++)
		{
			UWAICache::City& kCacheCity = kCache.cityAt(j);
			if (kCacheCity.city().getTeam() != eTeam)
				continue;
			if (kCacheCity.city().isCoastal())
				bHasCoastalCity = true;
			if (kCacheCity.canReachByLand())
			{
				bCanReachAnyByLand = true;
				if (kCacheCity.getDistance() <= iDistLimit)
					return true;
			}
		}
	}
	/*  Tactical AI can't do naval assaults on inland cities. Assume that landlocked
		civs are land targets even if they're too far away; better than treating
		them as entirely unreachable. */
	return (!bHasCoastalCity && bCanReachAnyByLand);
}


bool UWAI::Team::canReach(TeamTypes eTarget) const
{
	for (MemberIter itTarget(eTarget); itTarget.hasNext(); ++itTarget)
	{
		for (MemberAIIter itAgent(m_eAgent); itAgent.hasNext(); ++itAgent)
		{	// (Don't call UWAI::Player::canReach - to avoid the call overhead.)
			if (itAgent->uwai().getCache().
				numReachableCities(itTarget->getID()) > 0)
			{
				return true;
			}
		}
	}
	return false;
}


bool UWAI::Team::isCloseToAdoptingAnyWarPlan() const
{
	for (TeamIter<MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> itRival(m_eAgent);
		itRival.hasNext(); ++itRival)
	{
		if (canSchemeAgainst(itRival->getID(), false) &&
			leaderCache().warUtilityIgnoringDistraction(itRival->getID()) >= -20)
		{
			return true;
		}
	}
	return false;
}


void UWAI::Team::startReport()
{
	bool bDoReport = isReportTurn();
	m_pReport = new UWAIReport(!bDoReport);
	if (!bDoReport)
		return;
	int iYear = GC.getGame().getGameTurnYear();
	m_pReport->log("h3.");
	m_pReport->log("Year %d, %s:", iYear, m_pReport->teamName(m_eAgent));
	for (MemberIter itMember(m_eAgent); itMember.hasNext(); ++itMember)
		m_pReport->log(m_pReport->leaderName(itMember->getID(), 16));
	m_pReport->logNewline();
}


void UWAI::Team::closeReport()
{
	m_pReport->logNewline();
	m_pReport->logNewline();
	SAFE_DELETE(m_pReport);
}


void UWAI::Team::setForceReport(bool b)
{
	m_bForceReport = b;
}


bool UWAI::Team::isReportTurn() const
{
	if (m_bForceReport)
		return true;
	int iTurnNumber = GC.getGame().getGameTurn();
	static int const iReportInterval = GC.getDefineINT("REPORT_INTERVAL");
	return (iReportInterval > 0 && iTurnNumber % iReportInterval == 0);
}


void UWAI::Team::showWarPrepStartedMsg(TeamTypes eTarget)
{
	showWarPlanMsg(eTarget, "TXT_KEY_WAR_PREPARATION_STARTED");
}


void UWAI::Team::showWarPlanAbandonedMsg(TeamTypes eTarget)
{
	showWarPlanMsg(eTarget, "TXT_KEY_WAR_PLAN_ABANDONED");
}


void UWAI::Team::showWarPlanMsg(TeamTypes eTarget, char const* szKey)
{

	CvPlayer& kActivePlayer = GET_PLAYER(GC.getGame().getActivePlayer());
	if (!kActivePlayer.isSpectator() || !GC.getDefineBOOL("UWAI_SPECTATOR_ENABLED"))
		return;
	CvWString szBuffer = gDLL->getText(szKey,
			GET_TEAM(m_eAgent).getName().GetCString(),
			GET_TEAM(eTarget).getName().GetCString());
	gDLL->UI().addMessage(kActivePlayer.getID(), false, -1, szBuffer,
			0, MESSAGE_TYPE_MAJOR_EVENT,
			/* <advc.127b> */ NULL, NO_COLOR,
			GET_TEAM(m_eAgent).getCapitalX(kActivePlayer.getTeam(), true),
			GET_TEAM(m_eAgent).getCapitalY(kActivePlayer.getTeam(), true));
			// </advc.127b>
}

UWAICache& UWAI::Team::leaderCache()
{
	return GET_PLAYER(GET_TEAM(m_eAgent).getLeaderID()).uwai().getCache();
}

UWAICache const& UWAI::Team::leaderCache() const
{
	// Duplicate code; see also UWAICache::leaderCache.
	return GET_PLAYER(GET_TEAM(m_eAgent).getLeaderID()).uwai().getCache();
}


bool UWAI::Team::isWarEvalNeeded(TeamTypes eTeam) const
{
	return canSchemeAgainst(eTeam, true) || (!GET_TEAM(eTeam).isAVassal() &&
			!GET_TEAM(m_eAgent).isAVassal() && GET_TEAM(eTeam).isAtWar(m_eAgent));
}


void UWAI::Team::doWarReport()
{
	if (!getUWAI().isEnabled())
		return;
	bool bInBackground = getUWAI().isEnabled(true); // To be restored in the end
	getUWAI().setInBackground(true);
	setForceReport(true);
	doWar();
	setForceReport(false);
	getUWAI().setInBackground(bInBackground);
}


UWAI::Player::Player() : m_eAgent(NO_PLAYER) {}


void UWAI::Player::init(PlayerTypes ePlayer)
{
	m_eAgent = ePlayer;
	m_cache.init(ePlayer);
}


void UWAI::Player::uninit()
{
	m_cache.uninit();
}


void UWAI::Player::turnPre()
{
	m_cache.update();
}


void UWAI::Player::write(FDataStreamBase* pStream) const
{
	pStream->Write(GET_PLAYER(m_eAgent).getID());
	m_cache.write(pStream);
}


void UWAI::Player::read(FDataStreamBase* pStream)
{
	pStream->Read((int*)&m_eAgent);
	m_cache.read(pStream);
}


bool UWAI::Player::considerDemand(PlayerTypes eDemandPlayer, int iTradeVal) const
{
	// When furious, they'll have to take it from our cold dead hands.
	if (GET_PLAYER(m_eAgent).AI_getAttitude(eDemandPlayer) <= ATTITUDE_FURIOUS)
		return false;
	/*  (I don't think the interface even allows demanding tribute when there's
		a peace treaty) */
	if (!GET_TEAM(eDemandPlayer).canDeclareWar(TEAMID(m_eAgent)))
		return false;
	UWAIReport silentReport(true);
	WarEvalParameters ourParams(TEAMID(m_eAgent), TEAMID(eDemandPlayer), silentReport);
	WarEvaluator ourEval(ourParams);
	scaled rOurUtility = ourEval.evaluate(WARPLAN_LIMITED);
	// Add -5 to 40 for self-assertion
	rOurUtility += 45 * prideRating() - 5;
	/*  The more prior demands we remember, the more recalcitrant we become
		(does not count the current demand). */
	int const iMemoryDemand = GET_PLAYER(m_eAgent).AI_getMemoryCount(eDemandPlayer,
			MEMORY_MADE_DEMAND);
	if (iMemoryDemand > 0)
		rOurUtility += SQR(iMemoryDemand);
	if (rOurUtility >= 0) // Bring it on!
		return false;
	WarEvalParameters theirParams(TEAMID(eDemandPlayer),
			TEAMID(m_eAgent), silentReport);
	WarEvaluator theirEval(theirParams);
	/*  If they don't intend to attack soon, the peace treaty from tribute
		won't help us. Total war scares us more than limited. */
	int iTheirUtility = theirEval.evaluate(WARPLAN_TOTAL);
	if (iTheirUtility < 0)
		return false; // Call their bluff
	// Willing to pay at most this much
	scaled rMaxTradeVal = GET_TEAM(m_eAgent).uwai().reparationsToHuman(
			// Interpret theirUtility as a probability of attack
			(-rOurUtility * 2 * (4 + iTheirUtility)) / 100);
	return (iTradeVal <= rMaxTradeVal);
	/*  Some randomness? None in the BtS code (AI_considerOffer) either.
		Would have to use scaled::hash. */
}


bool UWAI::Player::considerPlea(PlayerTypes ePleaPlayer, int iTradeVal) const
{
	/*  Check only war utility and peace treaty here; all other preconditions
		are handled by CvPlayerAI::AI_considerOffer. */
	if (GET_TEAM(m_eAgent).isForcePeace(TEAMID(ePleaPlayer)) &&
		GET_PLAYER(m_eAgent).AI_getMemoryAttitude(ePleaPlayer, MEMORY_GIVE_HELP) <= 0)
	{
		return false;
	}
	// If war not possible, might as well sign a peace treaty.
	if (!GET_TEAM(m_eAgent).canDeclareWar(TEAMID(ePleaPlayer)) ||
		!GET_TEAM(ePleaPlayer).canDeclareWar(TEAMID(m_eAgent)))
	{
		return true;
	}
	/*  Accept probabilistically regardless of war utility (so long
		as we're not planning war yet, which the caller ensures).
		Probability to accept is 45% for Gandhi, 0% for Tokugawa. */
	scaled rAcceptProb = fixp(0.5) - GET_PLAYER(m_eAgent).AI_prDenyHelp();
	// Can't use sync'd RNG here, but don't want the outcome to change after reload.
	vector<int> aiInputs;
	aiInputs.push_back(GC.getGame().getGameTurn());
	aiInputs.push_back(iTradeVal);
	if (scaled::hash(aiInputs, m_eAgent) < rAcceptProb)
		return true;
	// Probably won't want to attack ePleaPlayer then
	if (GET_TEAM(m_eAgent).AI_isSneakAttackReady())
	{	// (Ruled out by caller)
		FAssert(!GET_TEAM(m_eAgent).AI_isSneakAttackReady(TEAMID(ePleaPlayer)));
		return true;
	}
	UWAIReport silentReport(true);
	WarEvalParameters params(TEAMID(m_eAgent), TEAMID(ePleaPlayer), silentReport);
	WarEvaluator eval(params);
	int iU = eval.evaluate(WARPLAN_LIMITED, 5) - 5; // minus 5 for goodwill
	if (iU >= 0)
		return false;
	scaled rThresh = utilityToTradeVal(-iU);
	return (rThresh >= iTradeVal);
}


bool UWAI::Player::amendTensions(PlayerTypes eHuman)
{
	FAssert(GET_PLAYER(eHuman).isHuman());
	FAssert(GET_TEAM(m_eAgent).getLeaderID() == m_eAgent);
	// Lower contact probabilities in later eras
	scaled const rEra = GET_PLAYER(m_eAgent).AI_getCurrEraFactor();
	CvLeaderHeadInfo const& kPersonality = GC.getInfo(GET_PLAYER(m_eAgent).
			getPersonalityType());
	if (GET_PLAYER(m_eAgent).AI_getAttitude(eHuman) <=
		kPersonality.getDemandTributeAttitudeThreshold())
	{
		FOR_EACH_ENUM(AIDemand)
		{
			if (GET_PLAYER(m_eAgent).AI_contactRoll(CONTACT_DEMAND_TRIBUTE,
				(fixp(8.5) - rEra) / 2) &&
				GET_PLAYER(m_eAgent).AI_demandTribute(eHuman, eLoopAIDemand))
			{
				return true;
			}
		}
	}
	else
	{
		if (GET_PLAYER(m_eAgent).AI_contactRoll(CONTACT_ASK_FOR_HELP,
			(fixp(5.5) - rEra) / fixp(1.25)) &&
			GET_PLAYER(m_eAgent).AI_askHelp(eHuman))
		{
			return true;
		}
	}
	if (kPersonality.getContactRand(CONTACT_RELIGION_PRESSURE) <=
		kPersonality.getContactRand(CONTACT_CIVIC_PRESSURE))
	{
		if (GET_PLAYER(m_eAgent).AI_contactRoll(CONTACT_RELIGION_PRESSURE,
			8 - rEra) &&
			GET_PLAYER(m_eAgent).AI_contactReligion(eHuman))
		{
			return true;
		}
	} 
	else
	{
		if (GET_PLAYER(m_eAgent).AI_contactRoll(CONTACT_CIVIC_PRESSURE,
			fixp(2.5)) &&
			GET_PLAYER(m_eAgent).AI_contactCivics(eHuman))
		{
			return true;
		}
	}
	// Embargo request - too unlikely to succeed I think.
	/*if (GET_PLAYER(m_eAgent).AI_contactRoll(CONTACT_STOP_TRADING, ?) &&
		GET_PLAYER(m_eAgent).AI_proposeEmbargo(eHuman))
	{
		return true;
	}*/
	return false;
}

// Wrapper that handles the war evaluator cache
int UWAI::Player::willTalk(PlayerTypes eToPlayer, int iAtWarCounter, bool bUseCache) const
{
	if (bUseCache)
		WarEvaluator::enableCache();
	int iR = willTalk(eToPlayer, iAtWarCounter);
	if (bUseCache)
		WarEvaluator::disableCache();
	return iR;
}


int UWAI::Player::willTalk(PlayerTypes eToPlayer, int iAtWarCounter) const
{
	if (GET_TEAM(m_eAgent).AI_surrenderTrade(TEAMID(eToPlayer)) == NO_DENIAL)
		return 1;
	// 1 turn RTT and let the team leader handle peace negotiation
	if (iAtWarCounter <= 1 || GET_TEAM(m_eAgent).getLeaderID() != m_eAgent)
		return -1;
	// bValid=true: want to return 1, but still need to check for DECLARED_WAR_RECENT.
	bool bValid = false;
	/*  Checking for a possible peace deal only serves as a convenience for
		human players; no need to do it for AI-AI peace. */
	if (!GET_PLAYER(eToPlayer).isHuman())
		bValid = true;
	else
	{
		bValid = (GET_TEAM(m_eAgent).AI_surrenderTrade(TEAMID(eToPlayer)) == NO_DENIAL ||
				isPeaceDealPossible(eToPlayer));
	}
	if (GET_PLAYER(m_eAgent).AI_getMemoryCount(eToPlayer, MEMORY_DECLARED_WAR_RECENT) > 0)
	{
		if (bValid)
			return 0;
		return -1;
	}
	return (bValid ? 1 : -1);
}


bool UWAI::Player::isPeaceDealPossible(PlayerTypes eHuman) const
{
	/*  Could simply call CvPlayerAI::AI_counterPropose, but I think there are rare
		situations when a deal is possible but AI_counterPropose doesn't find it.
		It would also be slower. */
	// <advc.705>
	CvGame const& kGame = GC.getGame();
	if (kGame.isOption(GAMEOPTION_RISE_FALL) &&
		kGame.getRiseFall().isCooperationRestricted(m_eAgent) &&
		GET_TEAM(m_eAgent).uwai().reluctanceToPeace(TEAMID(eHuman)) >= 20)
	{
		return false;
	} // </advc.705>
	int iTargetTradeVal = GET_TEAM(eHuman).uwai().endWarVal(TEAMID(m_eAgent));
	if (iTargetTradeVal <= 0)
		return true;
	return canTradeAssets(iTargetTradeVal, eHuman);
}


bool UWAI::Player::canTradeAssets(int iTargetTradeVal, PlayerTypes eHuman,
	int* piAvailableTradeVal,
	// (advc.ctr: Now unused b/c the AI will always accept cities as payment)
	bool bIgnoreCities) const
{
	if (piAvailableTradeVal != NULL)
		*piAvailableTradeVal = iTargetTradeVal;
	int iTotalTradeVal = 0;
	CvPlayerAI const& kHuman = GET_PLAYER(eHuman);
	if (kHuman.canTradeItem(m_eAgent, TradeData(TRADE_GOLD, kHuman.getGold()), true))
		iTotalTradeVal += kHuman.getGold();
	if (iTotalTradeVal >= iTargetTradeVal)
		return true;
	FOR_EACH_ENUM(Tech)
	{
		if (kHuman.canTradeItem(m_eAgent, TradeData(TRADE_TECHNOLOGIES, eLoopTech), true))
		{
			iTotalTradeVal += GET_TEAM(m_eAgent).AI_techTradeVal(eLoopTech,
					kHuman.getTeam(), true, true);
			if (iTotalTradeVal >= iTargetTradeVal)
				return true;
		}
	}
	if (!bIgnoreCities)
	{
		int const iCityLimit = intdiv::uceil(kHuman.getNumCities(), 6);
		int iCities = 0;
		FOR_EACH_CITYAI(pCity, kHuman)
		{
			if (iCities >= iCityLimit)
				break;
			// Tbd.: Shouldn't check the cities in an arbitrary order
			if(kHuman.canTradeItem(
				m_eAgent, TradeData(TRADE_CITIES, pCity->getID()), true))
			{
				iCities++;
				iTotalTradeVal += GET_PLAYER(m_eAgent).AI_cityTradeVal(*pCity);
				if (iTotalTradeVal >= iTargetTradeVal)
					return true;
			}
		}
	}
	FAssert(iTotalTradeVal < iTargetTradeVal);
	if (piAvailableTradeVal != NULL)
		*piAvailableTradeVal = iTotalTradeVal;
	return false;
}


scaled UWAI::Player::utilityToTradeVal(scaled rUtility) const
{
	return rUtility / tradeValUtilityConversionRate();
}


scaled UWAI::Player::tradeValToUtility(scaled rTradeVal) const
{
	return rTradeVal * tradeValUtilityConversionRate();
}


scaled UWAI::Player::tradeValUtilityConversionRate() const
{
	// Based on how long it would take us to produce as much trade value
	scaled rSpeedFactor = 1;
	int const iTrainPercent = GC.getInfo(GC.getGame().getGameSpeedType()).
			getTrainPercent();
	if (iTrainPercent > 0)
		rSpeedFactor = scaled(100, iTrainPercent);
	return std::max(scaled::epsilon(), (3 * rSpeedFactor) /
			(scaled::max(10,
			GET_TEAM(m_eAgent).AI_estimateYieldRate(m_eAgent, YIELD_COMMERCE))
			+ 2 * scaled::max(1,
			GET_TEAM(m_eAgent).AI_estimateYieldRate(m_eAgent, YIELD_PRODUCTION))));
	/*  Note that change advc.004s excludes espionage and culture from the
		Economy history, and estimateYieldRate(YIELD_COMMERCE) doesn't account
		for these yields either. Not a problem for culture, I think, which is
		usually produced in addition to gold and research, but the economic output
		of civs running the Big Espionage strategy will be underestimated.
		Still better than just adding up all commerce types. */
}


scaled UWAI::Player::amortizationMultiplier() const
{
	// 25 turns delay b/c war planning is generally about a medium-term future
	return GET_PLAYER(m_eAgent).AI_amortizationMultiplier(25);
}


scaled UWAI::Player::buildUnitProb() const
{
	scaled r;
	if (GET_PLAYER(m_eAgent).isHuman())
		r = humanBuildUnitProb();
	else r = per100(GC.getInfo(GET_PLAYER(m_eAgent).getPersonalityType()).
			getBuildUnitProb());
	// Accounting for advc.253
	r *= GET_PLAYER(m_eAgent).AI_trainUnitSpeedAdustment();
	return r;
}

// (Sort of duplicated in UWAI::Team::canReach)
bool UWAI::Player::canReach(PlayerTypes eTarget) const
{
	return (getCache().numReachableCities(eTarget) > 0);
}

/*	This player makes the prediction; the prediction is _about_ ePlayer.
	Like CvTeamAI::AI_estimateYieldRate (and other AI code), this function
	currently cheats by not checking whether demographics are visible.
	Would, in any case, make more sense as a team-level function,
	but I want to keep it together with buildUnitProb for now. */
scaled UWAI::Player::estimateBuildUpRate(PlayerTypes ePlayer, int iTurns) const
{
	iTurns *= GC.getInfo(GC.getGame().getGameSpeedType()).getTrainPercent();
	iTurns /= 100;
	return estimateDemographicGrowthRate(ePlayer, PLAYER_HISTORY_POWER, iTurns);
}


scaled UWAI::Player::estimateDemographicGrowthRate(PlayerTypes ePlayer,
	PlayerHistoryTypes eDemographic, int iTurns) const
{
	if (GC.getGame().getElapsedGameTurns() < iTurns + 1)
		return 0;
	int iGameTurn = GC.getGame().getGameTurn();
	int iPastValue = std::max(1, GET_PLAYER(ePlayer).getHistory(
			eDemographic, iGameTurn - 1 - iTurns));
	int iDelta = GET_PLAYER(ePlayer).getHistory(eDemographic, iGameTurn - 1)
			- iPastValue;
	return scaled::max(0, scaled(iDelta, iPastValue));
}


scaled UWAI::Player::humanBuildUnitProb() const
{
	scaled r = fixp(0.25); // 30 is about average, Gandhi 15
	if (GET_PLAYER(m_eAgent).getCurrentEra() == 0)
		r += fixp(0.1);
	if(GC.getGame().isOption(GAMEOPTION_RAGING_BARBARIANS) &&
		GET_PLAYER(m_eAgent).AI_getCurrEraFactor() <= 2)
	{
		r += fixp(0.05);
	}
	return r;
}


scaled UWAI::Player::confidenceFromWarSuccess(TeamTypes eTarget) const
{
	/*	Currently this function works entirely at the team level,
		but it could take into account the personality of this UWAI::Player
		in the future. */
	/*  Need to be careful not to overestimate
		early successes (often from a surprise attack). Bound the war success
		ratio based on how long the war lasts and the extent of successes. */
	CvTeamAI const& kAgent = GET_TEAM(m_eAgent);
	CvTeamAI const& kTarget = GET_TEAM(eTarget);
	int const iTurnsAtWar = kAgent.AI_getAtWarCounter(eTarget);
	/*  Can differ by 1 b/c of turn difference. Can apparently also differ by 2
		somehow, which I don't understand, but it's not a problem really. */
	FAssert(std::abs(iTurnsAtWar - kTarget.AI_getAtWarCounter(kAgent.getID())) <= 2);
	if (iTurnsAtWar <= 0)
		return -1;
	scaled const rAgentSuccess = std::max(scaled::epsilon(),
			kAgent.AI_getWarSuccess(eTarget));
	scaled const rTargetSuccess = std::max(scaled::epsilon(),
			kTarget.AI_getWarSuccess(kAgent.getID()));
	scaled rSuccessRatio = rAgentSuccess / rTargetSuccess;
	scaled const rFixedBound = fixp(0.5);
	// Reaches rFixedBound after 20 turns
	scaled rTimeBasedBound = (100 - fixp(2.5) * iTurnsAtWar) / 100;
	/*  Bound based on total war success: Becomes relevant once a war lasts long; e.g.
		after 25 turns, in the Industrial era, will need a total war success of 250
		in order to reach fixedBound. Neither side should feel confident if there
		isn't much action. */
	scaled rTotalBasedBound;
	{
		scaled rProgressFactor = 11 - kAgent.AI_getCurrEraFactor() * fixp(1.5);
		rProgressFactor.increaseTo(3);
		rTotalBasedBound = (100 - (rProgressFactor *
				(rAgentSuccess + rTargetSuccess)) / iTurnsAtWar) / 100;
	}
	scaled r = rSuccessRatio;
	r.clamp(rFixedBound, 2 - rFixedBound);
	r.clamp(rTimeBasedBound, 2 - rTimeBasedBound);
	r.clamp(rTotalBasedBound, 2 - rTotalBasedBound);
	return r;
}


scaled UWAI::Player::confidenceFromPastWars(TeamTypes eTarget) const
{
	scaled rPastWarScore = per100(m_cache.pastWarScore(eTarget));
	int iSign = (rPastWarScore < 0 ? -1 : 1);
	// -15% for the first lost war, less from further wars.
	scaled r = 1 + iSign * rPastWarScore.abs().sqrt() * fixp(0.15);
	r.clamp(fixp(0.5), fixp(1.5));
	return r;
}


scaled UWAI::Player::distrustRating() const
{
	if (GET_PLAYER(m_eAgent).isHuman())
		return 1;
	int iR = GC.getInfo(GET_PLAYER(m_eAgent).getPersonalityType()).
			getEspionageWeight() - 10;
	if (m_cache.hasDefensiveTrait())
		iR += 30;
	return scaled(std::max(0, iR), 100);
}


scaled UWAI::Player::warConfidencePersonal(bool bNaval, bool bTotal,
	PlayerTypes eTarget) const
{
	/*	AI assumes that human confidence depends on difficulty. NB: This doesn't
		mean that the AI thinks that humans are good at warfare - this is handled
		by confidenceAgainstHuman. Here, the AI thinks that humans think that
		humans are good at war, and that humans may therefore attack despite
		having little power. */
	if (GET_PLAYER(m_eAgent).isHuman())
	{
		// e.g. 0.62 at Settler, 1.59 at Deity
		return GET_PLAYER(m_eAgent).trainingModifierFromHandicap() /
				GET_PLAYER(eTarget).trainingModifierFromHandicap();
	}
	CvLeaderHeadInfo const& kPersonality = GC.getInfo(GET_PLAYER(m_eAgent).
			getPersonalityType());
	int const iMaxWarNearbyPR = kPersonality.getMaxWarNearbyPowerRatio();
	int const iMaxWarDistPR = kPersonality.getMaxWarDistantPowerRatio();
	int const iLimWarPR = kPersonality.getLimitedWarPowerRatio();
	scaled r = // Montezuma: 1.3; Elizabeth: 0.85
			//scaled(iMaxWarNearbyPR + iLimWarPR, 200);
		/*	Limited and total mostly affect the military build-up, not how the war
			is conducted. So it may not make much sense for a leader to be e.g.
			more optimistic about limited than total war. But the difference between
			the PowerRatio values should somehow matter. Perhaps some leaders think
			e.g. that they can't use large stacks so effectively ... */
			(bTotal ? iMaxWarNearbyPR : iLimWarPR);
			// (Or perhaps use a weighted mean as a compromise?)
	if (bNaval)
	{
		/*  distantWar refers to intercontinental war. The values in LeaderHead are
			between 0 (Sitting Bull) and 100 (Isabella), i.e. almost everyone is
			reluctant to fight cross-ocean wars. That reluctance is now covered
			elsewhere (e.g. army power reduced based on cargo capacity in
			simulations); hence the +35. This puts the return value between 0.35 and
			1.35. Exceeding the PR for land war is dangerous though; could cause
			the AI to plan for naval war when ships aren't needed at all. */
		r = scaled::min(r + 3, iMaxWarDistPR + 35);
	}
	return r / 100;
}


scaled UWAI::Player::warConfidenceLearned(PlayerTypes eTarget,
	bool bIgnoreDefOnly) const
{

	scaled rFromWarSuccess = confidenceFromWarSuccess(TEAMID(eTarget));
	scaled rFromPastWars = confidenceFromPastWars(TEAMID(eTarget));
	if (bIgnoreDefOnly == (rFromPastWars > 1))
		rFromPastWars = 1;
	scaled r = 1;
	if (rFromWarSuccess > 0)
		r += rFromWarSuccess - 1;
	/*  Very high/low rFromWarSuccess suggests relatively high reliability
		(long war and high total war successes); disregard the experience
		from past wars in this case. */
	if (rFromPastWars > 0 && r > fixp(0.6) && r < fixp(1.4))
		r += rFromPastWars - 1;
	r.decreaseTo(fixp(1.5));
	return r;
	// Tbd.: Consider using statistics (e.g. units killed/ lost) in addition
}


scaled UWAI::Player::warConfidenceAllies() const
{
	// AI assumes that humans have normal confidence
	if (GET_PLAYER(m_eAgent).isHuman())
		return fixp(0.8);
	int const iDogpileWarRand = GC.getInfo(GET_PLAYER(m_eAgent).
			getPersonalityType()).getDogpileWarRand();
	if (iDogpileWarRand <= 0)
		return 0;
	/*	iDogpileWarRand is between 20 (DeGaulle, high confidence) and
		150 (Lincoln, low confidence). These values are too far apart to convert
		them proportionally. Hence the square root. The result is normally between
		1 and 0.23. */
	scaled r(30, iDogpileWarRand);
	r = r.sqrt() - fixp(0.22);
	r.clamp(0, fixp(1.8));
	/*  Should have much greater confidence in civs on our team, but
		can't tell in this function who the ally is. Hard to rewrite
		InvasionGraph such that each ally is evaluated individually; wasn't
		written with team games in mind. As a kludge, just generally
		increase confidence when part of a team: */
	if (GET_TEAM(m_eAgent).getNumMembers() > 1)
	{
		scaled rConfTeam = r * 2;
		rConfTeam.clamp(fixp(0.6), fixp(1.2));
		r.increaseTo(rConfTeam);
	}
	return r;
}

// (See comment in header)
//scaled UWAI::Player::confidenceAgainstHuman() const {
	/*  How hesitant should the AI be to engage humans?
		This will have to be set based on experimentation. 90% is moderate
		discouragement against wars vs. humans. Perhaps unneeded, perhaps needs to
		be lower than 90%. Could set it based on the difficulty setting, however,
		while a Settler player can be expected to be easy prey, the AI arguably
		shouldn't exploit this, and while a Deity player will be difficult to
		defeat, the AI should arguably still try.
		The learning-which-civs-are-dangerous approach in warConfidenceLearned
		is more elgant, but won't prevent an AI-on-human dogpile in the early game. */
	//return (GET_PLAYER(m_eAgent).isHuman() ? 1 : fixp(0.9));
//}


int UWAI::Player::vengefulness() const
{
	CvPlayerAI const& kAgent = GET_PLAYER(m_eAgent);
	/*	AI assumes that humans are mostly calculating.
		But player feedback has shown that most humans are at least
		a little bit vengeful, casual players a bit more so.
		On the bottom line, this is relevant mainly for the reparations
		that the AI is willing to pay. */
	if (kAgent.isHuman())
	{
		if (GC.getGame().isOption(GAMEOPTION_RISE_FALL))
			return 1; // Difficulty not so telling in R&F
		int const iDifficulty = GC.getInfo(kAgent.getHandicapType()).getDifficulty();
		if (iDifficulty >= 50)
			return 1;
		if (iDifficulty > 20)
			return 2;
		return 3;
	}
	/*  RefuseToTalkWarThreshold loses its original meaning because UWAI
		doesn't sulk. It fits pretty well for carrying a grudge. Sitting Bull
		has the highest value (12) and De Gaulle the lowest (5).
		BasePeaceWeight (between 0 and 10) now has a dual use; continues to be
		used for inter-AI diplo modifiers. */
	CvLeaderHeadInfo const& kPersonality = GC.getInfo(kAgent.getPersonalityType());
	return std::max(0, kPersonality.getRefuseToTalkWarThreshold()
			- kPersonality.getBasePeaceWeight());
}


scaled UWAI::Player::protectiveInstinct() const
{
	if (GET_PLAYER(m_eAgent).isHuman())
		return 1;
	/*  DogPileWarRand is not a good indicator; that's more about backstabbing.
		Willingness to sign DP makes some sense. E.g. Roosevelt and the
		Persian leaders do that at Cautious, while Pleased is generally more common.
		Subtract WarMongerRespect to sort out the ones that just like DP
		because they're fearful, e.g. Boudica or de Gaulle. */
	CvLeaderHeadInfo const& kPersonality = GC.getInfo(GET_PLAYER(m_eAgent).
			getPersonalityType());
	int iDPVal = 2 * (ATTITUDE_FRIENDLY - kPersonality.
			getDefensivePactRefuseAttitudeThreshold());
	int iWarmongerRespect = kPersonality.getWarmongerRespect();
	return fixp(0.9) + scaled(iDPVal - SQR(iWarmongerRespect), 10);
}


scaled UWAI::Player::diploWeight() const
{
	if (GET_PLAYER(m_eAgent).isHuman())
		return 0;
	CvLeaderHeadInfo const& kPersonality = GC.getInfo(GET_PLAYER(m_eAgent).
			getPersonalityType());
	int const iCR = kPersonality.getContactRand(CONTACT_TRADE_TECH);
	if (iCR <= 0 || iCR > 15)
		return fixp(0.25);
	if (iCR <= 1)
		return fixp(1.75);
	if (iCR <= 3)
		return fixp(1.5);
	if (iCR <= 7)
		return 1;
	return fixp(0.5);
}


scaled UWAI::Player::prideRating(int iMakePeaceRand) const
{
	if (GET_PLAYER(m_eAgent).isHuman())
		return 0;
	if (iMakePeaceRand < 0)
	{
		iMakePeaceRand = GC.getInfo(GET_PLAYER(m_eAgent).getPersonalityType()).
				getMakePeaceRand();
	}
	scaled r(iMakePeaceRand, 110);
	r -= fixp(0.09);
	r.clamp(0, 1);
	return r;
}
