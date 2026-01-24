#include "CvGameCoreDLL.h"
#include "ArmamentForecast.h"
#include "UWAIAgent.h"
#include "MilitaryAnalyst.h"
#include "WarEvalParameters.h"
#include "UWAIReport.h"
#include "CoreAI.h"
#include "CvCity.h"
#include "CvMap.h"
#include "CvArea.h"
#include "CvInfo_GameOption.h"

using std::vector;
using std::ostringstream;
#include "CvInfo_City.h"

ArmamentForecast::ArmamentForecast(PlayerTypes ePlayer, MilitaryAnalyst const& kMA,
	std::vector<MilitaryBranch*>& kMilitary, int iTimeHorizon,
	bool bPeaceScenario, bool bNoUpgrading,
	bool bPartyAddedRecently, bool bAllPartiesKnown,
	UWAICache::City const* pTargetCity, scaled rProductionPortion)
:	m_kMA(kMA), m_kReport(kMA.evaluationParams().getReport()),
	m_eAnalyst(kMA.getAgentPlayer()), m_ePlayer(ePlayer),
	m_kMilitary(kMilitary), m_iTimeHorizon(iTimeHorizon)
{
#define bLOG_AI false // Clogs up the log too much
	if (!bLOG_AI && !GET_PLAYER(ePlayer).isHuman())
	  m_kReport.setMute(true);
	m_kReport.log("Armament forecast for *%s*", m_kReport.leaderName(ePlayer));
	WarEvalParameters const& kParams = kMA.evaluationParams();
	/*	The current production rate. It's probably going to increase a bit
		over the planning interval, but not much since the forecast doesn't
		reach far into the future; ignore that increase. */
	scaled rProductionEstimate = GET_TEAM(m_eAnalyst).AI_estimateYieldRate(
			ePlayer, YIELD_PRODUCTION);
	int iHurryProductionPerCity = 0;
	FOR_EACH_ENUM2(Hurry, eHurry)
	{
		if (GET_PLAYER(ePlayer).canHurry(eHurry))
		{
			CvHurryInfo const& kHurry = GC.getInfo(eHurry);
			int iLoopProduction = (kHurry.getGoldPerProduction() * 2) / 3 +
					kHurry.getProductionPerPopulation() / std::max(5,
					GC.getGame().getHurryAngerLength());
			iHurryProductionPerCity = std::max(iHurryProductionPerCity, iLoopProduction);
		}
	}
	rProductionEstimate += iHurryProductionPerCity * GET_PLAYER(ePlayer).getNumCities();
	/*	Civs will often change civics when war is declared. For now, the AI makes
		no effort to anticipate this. Will have to adapt once it happens. */
	m_kReport.log("Production per turn: %d", rProductionEstimate.round());
	rProductionEstimate *= rProductionPortion;
	if (rProductionPortion != 1)
	{
		m_kReport.log("Production considering lost cities: %d",
				rProductionEstimate.uround());
	}
	// Express upgrades in terms of differences in production costs
	scaled rProductionFromUpgrades = 0;
	if (!bNoUpgrading)
		rProductionFromUpgrades = productionFromUpgrades();
	if (rProductionFromUpgrades > 0)
		m_kReport.log("Production from upgrades: %d", rProductionFromUpgrades.uround());

	CvPlayerAI const& kPlayer = GET_PLAYER(ePlayer);
	TeamTypes const eTeam = kPlayer.getTeam();
	CvTeamAI const& kTeam = GET_TEAM(eTeam);
	TeamTypes const eMaster = kTeam.getMasterTeam();
	Intensity eIntensity = NORMAL;
	if (kPlayer.AI_isDoStrategy(AI_STRATEGY_ALERT1))
		eIntensity = INCREASED;
	bool bNavalArmament = false;
	if (pTargetCity != NULL)
	{
		if (!pTargetCity->canReachByLandFromCapital() ||
			pTargetCity->getDistance() > getUWAI().maxLandDist())
		{
			bNavalArmament = true;
		}
		m_kReport.log("Target city: %s%s", m_kReport.cityName(pTargetCity->city()),
				(bNavalArmament ? " (naval target)": ""));
	}
	TeamTypes const eTargetTeam = kParams.getTarget();
	int iTotalWars = 0, iWars = 0;
	// Whether simulation assumes peace between ePlayer and any other player
	bool bPeaceAssumed = false;
	// Whether simulation assumes ePlayer to have been recently attacked by anyone
	bool bAttackedRecently = false;
	// Any war or peace assumed that involves ePlayer, or war preparations by ePlayer.
	bool bFictionalScenario = false;
	TeamTypes eSingleWarEnemy = NO_TEAM; // Only relevant if there is just one enemy
	bool const bNoWarVsExtra = (bPeaceScenario && kParams.isNoWarVsExtra());
	for (TeamAIIter<MAJOR_CIV,KNOWN_TO> itOther(TEAMID(m_eAnalyst));
		itOther.hasNext(); ++itOther)
	{
		CvTeamAI const& kOther = *itOther;
		if (kOther.getID() == eTeam)
			continue;
		TeamTypes const eOther = kOther.getID();
		// Whether the simulation assumes peace between eTeam and eOther
		bool bPeaceAssumedLoop = (bPeaceScenario &&
				((kMA.isOnOurSide(eTeam) && kMA.isOnTheirSide(eOther)) ||
				(kMA.isOnOurSide(eOther) && kMA.isOnTheirSide(eTeam))) &&
				(eTeam != TEAMID(m_eAnalyst) || !bNoWarVsExtra ||
				eOther != kParams.getTarget()));
		/*	Important to check warplan (not just war) when
			second-guessing preparations underway */
		if (bPeaceAssumedLoop && kTeam.AI_getWarPlan(eOther) != NO_WARPLAN)
			bPeaceAssumed = true;
		/*	True if simulation assumes a war between eOther and eTeam
			to have already started, or if simulation assumes a war plan.
			Not true if already at war in the actual game
			(outside the simulation).*/
		bool bWarAssumed = (bAllPartiesKnown || eTeam == TEAMID(m_eAnalyst)) &&
				((kMA.isOnOurSide(eOther) && kMA.isOnTheirSide(eTeam, true)) ||
				(kMA.isOnOurSide(eTeam) && kMA.isOnTheirSide(eOther, true)));
		if (bPeaceAssumedLoop || kOther.isAtWar(eTeam))
			bWarAssumed = false;
		bool const bReachEither = canReachEither(eOther, eTeam);
		if (bReachEither && (bWarAssumed || bPeaceAssumed))
			bFictionalScenario = true;
		if ((kOther.isAtWar(eTeam) || bWarAssumed) && !bPeaceAssumedLoop &&
			/* If neither side can reach the other, the war doesn't count
			   because it doesn't (or shouldn't) lead to additional buildup. */
			bReachEither)
		{
			if (!kOther.isAVassal())
			{
				iWars++;
				if (iWars <= 1)
					eSingleWarEnemy = kOther.getID();
				else eSingleWarEnemy = NO_TEAM;
			}
			if (eIntensity == NORMAL)
				eIntensity = INCREASED;
			// eTeam recently attacked by eOther
			bool const bAttackedRecentlyLoop = (bWarAssumed && bPartyAddedRecently &&
					kMA.isOnTheirSide(eTeam, true));
			if (bAttackedRecentlyLoop && kOther.uwai().canReach(eTeam))
				bAttackedRecently = true;
			/*	Vassals only get dragged along into limited wars; however,
				an attacked vassal may build up as if in total war. */
			bool const bTotalWarAssumed = (bWarAssumed &&
					((TEAMID(m_eAnalyst) == eTeam &&
					eOther == eTargetTeam && kParams.isTotal()) ||
					bAttackedRecentlyLoop) &&
					// Only assume total war if eTeam can go on the attack too
					kTeam.uwai().canReach(eOther));
			if ((kTeam.AI_getWarPlan(eOther) == WARPLAN_TOTAL &&
				/* If we already have a (total) war plan against the target,
				   that plan is going to be replaced by the war plan
				   under consideration if adopted. */
				(TEAMID(m_eAnalyst) != eTeam || eOther != eTargetTeam)) ||
				bTotalWarAssumed)
			{
				iTotalWars++;
			}
		}
	}
	int iWarPlans = kTeam.AI_countWarPlans();
	/*  Assume that we (the analyst) don't pursue any (aggressive) war preparations
		in the peace scenario. (This should only be relevant when considering
		an immediate DoW, e.g. at the request of another civ, while already
		planning war. I think the baseline should then be a scenario
		without war preparations.)
		UWAI::Agent::scheme should compare the utility of the immediate war
		with that of the war in preparation. */
	if (bPeaceScenario && ePlayer == m_eAnalyst)
		iWarPlans = iWars;
	m_kReport.log("War plans: %d; assuming %d wars, %d total wars%s%s",
				iWarPlans, iWars, iTotalWars,
				(bPeaceAssumed ? ", peace assumed" : ""),
				(bAttackedRecently ? ", attacked recently" : ""));
	if (iTotalWars > 0 ||
		/*	When planning for limited war while being alert2 or dagger,
			the strategies take precedence. However, shouldn't trust
			alert2 when assuming peace b/c alert2 may well be caused
			by the ongoing war.
			(alert2 now treated separately farther below.)
			In contrast, ongoing war doesn't have much of an impact on dagger. */
		/*	Assume that human is alert about impending attacks, but doesn't
			adopt a dagger strategy (at least not under the same circumstances
			as an AI would). [Check obsolete now that Dagger is disabled.] */
		(kPlayer.AI_isDoStrategy(AI_STRATEGY_DAGGER) && !kPlayer.isHuman()) ||
		/*	Concurrent war preparations: probably shouldn't be possible anyway.
			Must definitely be disregarded for the analyst b/c the war preparations
			currently under consideration may lead to abandonment of
			concurrent war preparations. */
		(kTeam.AI_getNumWarPlans(WARPLAN_PREPARING_TOTAL) > 0 &&
		eMaster != GET_TEAM(m_eAnalyst).getMasterTeam()))
	{
		eIntensity = FULL;
	}
	bool const bAttackedUnprepared = (bAttackedRecently && iWarPlans == 0);
			// Count preparing limited as unprepared?
			//iWarPlans <= kTeam.getWarPlanCount(WARPLAN_PREPARING_LIMITED);
	bool bDefensive = false;
	/*	Trust defensive AreaAI even when assuming peace b/c defensive build-up will
		(or should) continue despite peace. */
	if ((getAreaAI(ePlayer) == AREAAI_DEFENSIVE &&
		/*	Trust AreaAI for the first phase of simulation; for the second phase,
			if doing increased or full build-up (always the case when
			defensive AreaAI?), assume that kTeam will be able to get on the
			offensive, or that defenses reach a saturation point. */
		(eIntensity == NORMAL || !bAllPartiesKnown)) ||
		bAttackedUnprepared || (iWars == 0 && iWarPlans == 0 &&
		(kPlayer.AI_isDoStrategy(AI_STRATEGY_ALERT1) ||
		kPlayer.AI_isDoStrategy(AI_STRATEGY_ALERT2))))
	{
		bDefensive = true;
	}
	/*	alert2 implies full build-up, but if build-up otherwise wouldn't be full,
		then alert2 makes it defensive. */
	if (kPlayer.AI_isDoStrategy(AI_STRATEGY_ALERT2) && !bPeaceAssumed &&
		eIntensity != FULL)
	{
		eIntensity = FULL;
		bDefensive = true;
	}
	/*	Humans build few dedicated defensive units; there are exceptions to this,
		but the AI can't easily identify those. */
	if (kPlayer.isHuman())
		bDefensive = false;
	/*	Should assume that our other preparations are abandoned
		in the peace scenario. In the military analysis, the comparison should
		be between war and (attempted) peace.
		Can't trust Area AI when war preparations are supposed to be abandoned. */
	if (kMA.isOnOurSide(eTeam) && bPeaceScenario && iWarPlans > iWars)
		bFictionalScenario = true;
	// During war preparations, params take precedence when it comes to naval armament.
	if (!bPeaceScenario && bFictionalScenario && kPlayer.getID() == m_eAnalyst &&
		!kTeam.isAtWar(eTargetTeam))
	{
		bNavalArmament = kParams.isNaval();
	}
	/*	Assume that war against a single small enemy doesn't increase the
		build-up intensity. Otherwise, the AI will tend to leave 1 or 2 cities alive.
		Consistent with CvPlayerAI::AI_isFocusWar. Would be cleaner to assume
		a shorter time horizon, but that's a can of worms. */
	if (eSingleWarEnemy != NO_TEAM && !bNavalArmament &&
		iTotalWars <= 0 && iWarPlans <= 1 &&
		!kPlayer.AI_isDoStrategy(AI_STRATEGY_ALERT1 | AI_STRATEGY_ALERT2) &&
		kTeam.AI_isPushover(eSingleWarEnemy))
	{
		eIntensity = NORMAL;
		bFictionalScenario = true; // Don't check AreAI either
	}
	// Rely on Area AI (only) if there is no hypothetical war or peace
	if (bFictionalScenario)
	{
		predictArmament(iTimeHorizon, rProductionEstimate, rProductionFromUpgrades,
				eIntensity, bDefensive, bNavalArmament);
	}
	else
	{
		m_kReport.log("Checking AreaAI");
		AreaAITypes const eAreaAI = getAreaAI(ePlayer);
		// Offensive Area AI builds fewer units than 'massing' and 'defensive'
		if (eAreaAI == AREAAI_OFFENSIVE || eAreaAI == AREAAI_ASSAULT_ASSIST ||
			eAreaAI == AREAAI_ASSAULT ||
			((eAreaAI == AREAAI_MASSING || eAreaAI == AREAAI_ASSAULT_MASSING ||
			eAreaAI == AREAAI_DEFENSIVE) &&
			iTotalWars == 0 && iWars > 0) ||
			kPlayer.AI_isDoStrategy(AI_STRATEGY_ALERT1) ||
			// advc.018: Crush now actually trains fewer units
			kPlayer.AI_isDoStrategy(AI_STRATEGY_CRUSH))
		{
			eIntensity = INCREASED;
		}
		if (kPlayer.AI_isFocusWar() &&
			(eAreaAI == AREAAI_MASSING || eAreaAI == AREAAI_ASSAULT_MASSING ||
			(eAreaAI == AREAAI_DEFENSIVE && iTotalWars > 0) ||
			kPlayer.AI_isDoStrategy(AI_STRATEGY_ALERT2) ||
			// [Obsolete check; Dagger disabled.]
			(kPlayer.AI_isDoStrategy(AI_STRATEGY_DAGGER) && !kPlayer.isHuman() &&
			/*	AI assumes that human players don't use the dagger strat., and
				are also unable to notice when an AI uses dagger. */
			!GET_PLAYER(m_eAnalyst).isHuman()) ||
			kPlayer.AI_isDoStrategy(AI_STRATEGY_TURTLE) ||
			kPlayer.AI_isDoStrategy(AI_STRATEGY_LAST_STAND) ||
			kPlayer.AI_isDoStrategy(AI_STRATEGY_FINAL_WAR)))
		{
			eIntensity = FULL;
		}
		if (ePlayer != m_eAnalyst) // Trust our own AreaAI more than our power curve
		{
			/*	Humans only have a war plan when they're actually at war
				(total or attacked). Even then, the human build-up doesn't have to
				match the war plan. Make a projection based on the human power curve. */
			scaled const rBuildUpRate = GET_PLAYER(m_eAnalyst).uwai().
					estimateBuildUpRate(ePlayer);
			Intensity eBasedOnCurve = INCREASED;
			if (rBuildUpRate > fixp(0.25))
				eBasedOnCurve = FULL;
			else if (rBuildUpRate < fixp(0.18))
				eBasedOnCurve = NORMAL;
			m_kReport.log("Build-up intensity based on power curve: %d", (int)
					eBasedOnCurve);
			if (kPlayer.isHuman())
			{
				eIntensity = eBasedOnCurve;
				m_kReport.log("Using estimated intensity for forecast");
				if (eIntensity <= NORMAL && kTeam.isAtWar(TEAMID(m_eAnalyst)) &&
					!kTeam.AI_isPushover(TEAMID(m_eAnalyst)))
				{
					// Have to expect that human will increase build-up as necessary
					eIntensity = INCREASED;
					m_kReport.log("Increased intensity for human at war with us");
				}
			}
			/*	For AI civs, only use the projection as a sanity check for now.
				Would be nice to not look at the Area AI of other civs at all (b/c it's
				a cheat), but I think the estimate may not be reliable enough b/c losses
				can hide build-up in the power curve. Less of a problem against humans
				b/c they don't tend to have high losses. */
			else if ((eBasedOnCurve == FULL && eIntensity == NORMAL) ||
				(eBasedOnCurve == NORMAL && eIntensity == FULL))
			{
				m_kReport.log("Estimates based on power curve and area differ widely,"
						" assuming increased build-up");
				eIntensity = INCREASED;
			}
		}
		bNavalArmament = (eAreaAI == AREAAI_ASSAULT ||
				eAreaAI == AREAAI_ASSAULT_MASSING || eAreaAI == AREAAI_ASSAULT_ASSIST);
		bDefensive = (kPlayer.AI_isDoStrategy(AI_STRATEGY_ALERT1) ||
				kPlayer.AI_isDoStrategy(AI_STRATEGY_ALERT2) ||
				eAreaAI == AREAAI_DEFENSIVE);
		predictArmament(iTimeHorizon, rProductionEstimate, rProductionFromUpgrades,
				eIntensity, bDefensive, bNavalArmament);
	}
	if (!bLOG_AI && !kPlayer.isHuman())
		m_kReport.setMute(false); // advc.test
#undef bLOG_AI
}


void ArmamentForecast::predictArmament(int iTurnsBuildUp, scaled rPerTurnProduction,
	scaled rAdditionalProduction, Intensity eIntensity, bool bDefensive,
	bool bNavalArmament)
{
	PROFILE_FUNC();
	CvPlayerAI const& kPlayer = GET_PLAYER(m_ePlayer);
	if (!bDefensive)
	{
		// Space and culture victory tend to divert production away from the military
		bool const bPeacefulVictory = kPlayer.uwai().getCache().isFocusOnPeacefulVictory();
		if (bPeacefulVictory)
		{
			m_kReport.log("Build-up reduced b/c pursuing peaceful victory");
			if (eIntensity == FULL)
				eIntensity = INCREASED;
			else if (eIntensity == INCREASED)
				eIntensity = NORMAL;
			else if (eIntensity == NORMAL)
				eIntensity = DECREASED;
		}
	}

	m_kReport.log("Forecast for the next %d turns", iTurnsBuildUp);
	m_kReport.log("Defensive: %s, naval: %s, intensity: %s", bDefensive ? "yes" : "no",
			bNavalArmament ? "yes" : "no", strIntensity(eIntensity));

	// Armament portion of the total production; based on intensity.
	scaled rArmamentPortion = kPlayer.uwai().buildUnitProb();
	scaled const rPlayerEra = kPlayer.AI_getCurrEraFactor();
	{	/*	Don't know if there are really especially few distractions in era 1.
			Could be - still few buildings available and early expansion is over.
			Anyway, buildUnitProb (unadjusted) has been working well for getting some
			warfare going in the early Classical era; want to keep it that way, mostly. */
		scaled rEraAdjust = (1 - rPlayerEra).abs() / 10;
		if (rPlayerEra == 0)
			rEraAdjust *= 2;
		rEraAdjust.decreaseTo(fixp(0.2));
		rArmamentPortion *= 1 - rEraAdjust;
	}
	/*  Total vs. limited war mostly affects pre-war build-up, but there are also
		a few lines of (mostly K-Mod) code that make the AI focus more on production
		when in a total war. The computation of the intensity doesn't cover this
		behavior.
		Doesn't matter much if I increase rPerTurnProduction or rArmamentPortion;
		they're multiplied in the end. */
	scaled rAtWarAdjustment;
	WarEvalParameters const& kParams = m_kMA.evaluationParams();
	if (kParams.isConsideringPeace())
	{
		if (kParams.isTotal())
		{
			rAtWarAdjustment = fixp(0.05);
			/*  If considering to switch from limited to total war, assume that
				total war will bring full build-up. Switching to total war may
				not actually have this effect on the AreaAI, but UWAI assumes
				that preparations for total war always result in full build-up.
				Starting war preparations against some additional opponent mustn't,
				as a side-effect, lead to a better war outcome against the current
				opponent. */
			if (GET_TEAM(kParams.getAgent()).AI_getWarPlan(kParams.getTarget()) !=
				WARPLAN_TOTAL)
			{
				eIntensity = FULL;
			}
		}
		else rAtWarAdjustment -= fixp(0.05);
	}
	if (eIntensity == DECREASED)
		rArmamentPortion -= fixp(0.1);
	else if (eIntensity == INCREASED)
		rArmamentPortion += fixp(0.18);
	else if (eIntensity == FULL)
		rArmamentPortion += fixp(0.3);
	rArmamentPortion += rAtWarAdjustment;
	rArmamentPortion.decreaseTo(fixp(0.7));
	if (kPlayer.getMaxConscript() > 0 && eIntensity >= INCREASED)
	{
		if (eIntensity == INCREASED)
			rArmamentPortion += fixp(0.04);
		else if (eIntensity == FULL)
			rArmamentPortion += fixp(0.08);
		m_kReport.log("Armament portion increased b/c of conscription");
	}
	rArmamentPortion.clamp(0, fixp(0.75));
	// Portions of the military branches
	scaled rBranchPortions[NUM_BRANCHES] = { 0 };
	// Little defense by default
	rBranchPortions[HOME_GUARD] = fixp(0.18);
	if (bNavalArmament)
	{
		rBranchPortions[FLEET] = fixp(0.2);
		int iRevealed = 0;
		int iRevealedCoast = 0;
		FOR_EACH_CITY(pCity, kPlayer)
		{
			if (pCity->isRevealed(kPlayer.getTeam()))
			{
				iRevealed++;
				if (pCity->isCoastal())
					iRevealedCoast++;
			}
		}
		if (iRevealed > 0)
		{
			if (iRevealed >= kPlayer.getNumCities() && iRevealedCoast <= 0)
				rBranchPortions[FLEET] = 0;
			// Assume little defensive build-up when attacking across the sea
			else if (!bDefensive)
				rBranchPortions[HOME_GUARD] = fixp(0.12);
			scaled rCoastPortion(iRevealedCoast, iRevealed);
			rBranchPortions[FLEET] = std::min(fixp(0.35),
					fixp(0.08) + rCoastPortion / fixp(2.8));
		}
		TeamTypes const eAgentTeam = TEAMID(m_kMA.getAgentPlayer());
		scaled rTypicalCargo = m_kMilitary[LOGISTICS]->getTypicalPower(eAgentTeam);
		if (rTypicalCargo > 0 && m_kMilitary[LOGISTICS]->getTypicalUnit() != NO_UNIT)
		{
			rBranchPortions[LOGISTICS] = std::min(rBranchPortions[FLEET],
					/*  As the game progresses, the production portion needed
						for transports decreases. */
					1 / rTypicalCargo);
			if (!bDefensive && eIntensity > NORMAL && kPlayer.getCurrentEra() > 0)
			{
				/*  Need to assume more naval build-up if kPlayer hardly has any navy;
					otherwise, the AI may conclude that a naval assault is hopeless. */
				scaled rMultCargo = 2 -
						m_kMilitary[LOGISTICS]->power() /
						(rTypicalCargo * scaled::max(kPlayer.AI_getCurrEraFactor(), 1));
				rMultCargo.clamp(1, fixp(1.5));
				rMultCargo = (rMultCargo + 1) / 2; // dilute
				rBranchPortions[LOGISTICS] *= rMultCargo;
				scaled rTypicalFleetPow = m_kMilitary[FLEET]->getTypicalPower(eAgentTeam);
				if (rTypicalFleetPow > 0)
				{
					scaled rMultFleet = 2 -
							m_kMilitary[FLEET]->power() /
							(rTypicalFleetPow * kPlayer.AI_getCurrEraFactor());
					rMultFleet.clamp(1, fixp(1.5));
					rMultFleet = (rMultFleet + 1) / 2;
					rBranchPortions[FLEET] *= rMultFleet;
				}
			}
		}
	}
	rBranchPortions[ARMY] = 1 -
			(rBranchPortions[HOME_GUARD] +
			rBranchPortions[FLEET] +
			rBranchPortions[LOGISTICS]);
	FAssert(rBranchPortions[ARMY] >= 0);
	if (bDefensive || eIntensity == NORMAL)
	{
		// No cargo in defensive naval wars
		rBranchPortions[FLEET] += rBranchPortions[LOGISTICS];
		rBranchPortions[LOGISTICS] = 0;
		// Shift half of the fleet budget to home guard
		rBranchPortions[FLEET] /= 2;
		rBranchPortions[HOME_GUARD] += rBranchPortions[FLEET];
		if (!kPlayer.isHuman() && bDefensive)
		{
			// Shift half of the army budget to home guard
			rBranchPortions[ARMY] /= 2;
			rBranchPortions[HOME_GUARD] += rBranchPortions[ARMY];
		}
		else // Shift 1/3 for humans -- they build fewer garrisons
		{
			rBranchPortions[ARMY] *= fixp(2/3.);
			rBranchPortions[HOME_GUARD] += rBranchPortions[ARMY] / 2;
		}
	}
	if (!bDefensive)
	{
		// Undone below if unable to build nukes
		scaled rNukePortion = fixp(0.2);
		if (kPlayer.isHuman())
			rNukePortion += fixp(0.05);
		rBranchPortions[NUCLEAR] = rNukePortion;
		for (int i = 0; i < NUM_BRANCHES; i++)
		{
			if (i == NUCLEAR)
				continue;
			rBranchPortions[i] *= (1 - rNukePortion);
		}
	}
	// Shift weights away from milit. branches that kPlayer can't build units for
	scaled rSurplus;
	for (int i = 0; i < NUM_BRANCHES; i++)
	{
		if (m_kMilitary[i]->getTypicalUnit() == NO_UNIT)
		{
			rSurplus += rBranchPortions[i];
			rBranchPortions[i] = 0;
		}
	}
	if (rSurplus.approxEquals(1, fixp(0.001)))
	{
		m_kReport.log("Armament forecast canceled b/c no units can be trained");
		return;
	}
	for (int i = 0; i < NUM_BRANCHES; i++)
	{
		if (m_kMilitary[i]->getTypicalUnit() != NO_UNIT)
			rBranchPortions[i] += rSurplus * rBranchPortions[i] / (1 - rSurplus);
	}
	#ifdef FASSERT_ENABLE
		scaled rChecksum;
		for (int i = 0; i < NUM_BRANCHES; i++)
			rChecksum += rBranchPortions[i];
		FAssert(rChecksum.approxEquals(1, fixp(0.01)));
	#endif
	// Assume no deliberate build-up of Cavalry. Army can happen to be mounted though.
	{
		UnitTypes const eTypicalArmyUnit = m_kMilitary[ARMY]->getTypicalUnit();
		if (eTypicalArmyUnit != NO_UNIT &&
			m_kMilitary[CAVALRY]->canEmploy(eTypicalArmyUnit))
		{
			rBranchPortions[CAVALRY] = rBranchPortions[ARMY];
		}
	}
	if (!m_kReport.isMute()) // Logging
	{
		ostringstream msg;
		msg << "Branch portions for ";
		bool bFirstItemDone = false; // for commas
		for (int i = 0; i < NUM_BRANCHES; i++)
		{
			if (i == NUCLEAR || rBranchPortions[i].getPercent() < 1)
				continue;
			MilitaryBranch const& kBranch = *m_kMilitary[i];
			if (bFirstItemDone)
				msg << ", ";
			msg << kBranch;
			bFirstItemDone = true;
		}
		msg << ": ";
		bFirstItemDone = false;
		for (int i = 0; i < NUM_BRANCHES; i++)
		{
			if (i == NUCLEAR || rBranchPortions[i].getPercent() < 1)
				continue;
			if (bFirstItemDone)
				msg << ", ";
			msg << rBranchPortions[i].getPercent();
			bFirstItemDone = true;
		}
		m_kReport.log("%s", msg.str().c_str());
	}
	// Compute total production for armament
	scaled rTotalProductionForBuildUp = rAdditionalProduction;
	rTotalProductionForBuildUp += iTurnsBuildUp * rArmamentPortion * rPerTurnProduction;
	m_kReport.log("Total production for build-up: %d hammers",
			rTotalProductionForBuildUp.uround());
	m_rProductionInvested = rTotalProductionForBuildUp;

	// Increase military power
	//m_kReport.log("\nbq."); // Textile block quote (takes up too much space)
	TeamTypes const eAgentTeam = TEAMID(m_kMA.getAgentPlayer());
	for (int i = 0; i < NUM_BRANCHES; i++)
	{
		MilitaryBranch& kBranch = *m_kMilitary[i];
		scaled const rTypicalCost = kBranch.getTypicalCost(eAgentTeam);
		if (rTypicalCost <= 0)
			continue;
		scaled const rTypicalPower = kBranch.getTypicalPower(eAgentTeam);
		scaled rIncrease = rBranchPortions[i] * rTotalProductionForBuildUp *
				(rTypicalPower / rTypicalCost);
		kBranch.changePower(rIncrease);
		if (rIncrease.uround() > 0)
		{
			FAssertMsg(kBranch.power() >= 0, "overflow in predicted power?");
			m_kReport.log("Predicted power increase in %s by %d",
					kBranch.str(), rIncrease.uround());
		}
	}
	m_kReport.logNewline();
}


bool ArmamentForecast::canReachEither(TeamTypes eFirst, TeamTypes eSecond) const
{
	return (GET_TEAM(eFirst).uwai().canReach(eSecond) ||
			GET_TEAM(eSecond).uwai().canReach(eFirst));
}


char const* ArmamentForecast::strIntensity(Intensity eIntensity)
{
	switch(eIntensity)
	{
	case DECREASED: return "decreased";
	case NORMAL: return "normal";
	case INCREASED: return "increased";
	case FULL: return "full";
	default: return "(unknown intensity)";
	}
}

scaled ArmamentForecast::productionFromUpgrades()
{
	/*	Going through all the units and checking for possible upgrades would be
		somewhat expensive and complicated: Which upgrades would be prioritized
		if upgrading them all is too costly?
		Failed attempt: Predict the power of a fully upgraded army based on
		unit counts and typical units -- the resulting power value turned out to
		be a poor estimate of an army's upgrade potential.
		Actual approach: Rely on CvPlayerAI::AI_updateGoldToUpgradeAllUnits,
		convert the result into hammers, and (later) the hammers into power. */
	CvPlayerAI const& kPlayer = GET_PLAYER(m_ePlayer);
	scaled r = kPlayer.AI_getGoldToUpgradeAllUnits();
	if (2 * r >= 1)
		m_kReport.log("Total gold needed for upgrades: %d", r.uround());
	/*	kPlayer may not have the funds to make all the upgrades in the medium term.
		Think of a human player keeping stacks of Warriors around, or a vassal
		receiving tech quickly from its master. Spend at most iIncomeTurns turns
		worth of income on upgrades. The subtrahend will be 0 during anarchy --
		not a big problem I think. */
	int const iIncomeTurns = 4;
	scaled const rIncome = GET_TEAM(m_eAnalyst).AI_estimateYieldRate(
			kPlayer.getID(), YIELD_COMMERCE, 3) - kPlayer.calculateInflatedCosts();
	scaled rIncomeBound = iIncomeTurns * rIncome;
	// Also take into account current gold stockpile
	int const iGold = kPlayer.getGold();
	rIncomeBound = std::max((2 * rIncomeBound + iGold) / 3,
			(2 * iGold + rIncomeBound) / 3);
	if (rIncomeBound < r)
		m_kReport.log("Upgrades bounded by income (%d gpt)", rIncome.round());
	r.decreaseTo(rIncomeBound);
	// An approximate inversion of CvUnit::upgradePrice
	scaled rUpgrCostPerProd = GC.getDefineINT(CvGlobals::UNIT_UPGRADE_COST_PER_PRODUCTION);
	r /= rUpgrCostPerProd;
	/*	The base upgrade cost is paid per unit, but CvPlayerAI doesn't track
		how many units need an upgrade. Assuming a mean training cost difference
		of 30 hammers, one can look at the base cost as a multiplicative modifier. */
	scaled rTypicalGoldForProdDiff = rUpgrCostPerProd * 30;
	scaled rBaseCostModifier = rTypicalGoldForProdDiff /
			(rTypicalGoldForProdDiff + GC.getDefineINT(CvGlobals::BASE_UNIT_UPGRADE_COST));
	r *= rBaseCostModifier;
	if (!kPlayer.isHuman())
	{
		CvHandicapInfo const& kGameHandicap = GC.getInfo(GC.getGame().getHandicapType());
		scaled rAIUpgradeFactor = per100(kGameHandicap.getAIUnitUpgradePercent());
				// advc.250d: The per-era modifier no longer applies to upgrade cost
				// + kGameHandicap.getAIPerEraModifier() * kPlayer.getCurrentEra();
		/*	Shouldn't draw conclusions from AI_getGoldToUpgradeAllUnits when
			AI upgrades are (modded to be) free or almost free. */
		if (rAIUpgradeFactor > fixp(0.1))
			r /= rAIUpgradeFactor;
	}
	r.increaseTo(0);
	return r;
}


AreaAITypes ArmamentForecast::getAreaAI(PlayerTypes ePlayer) const
{
	CvCity const* pCapital = GET_PLAYER(ePlayer).getCapital();
	if (pCapital == NULL)
		return NO_AREAAI;
	return pCapital->getArea().getAreaAIType(TEAMID(ePlayer));
}
