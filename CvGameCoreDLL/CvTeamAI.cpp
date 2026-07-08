#include "CvGameCoreDLL.h"
#include "CvTeamAI.h"
#include "CvPlayerAI.h"
#include "CoreAI.h"
#include "CvCityAI.h"
#include "TeamPathFinder.h"
#include "PlotRange.h"
#include "CvArea.h"
#include "CvInfo_City.h"
#include "CvInfo_Terrain.h"
#include "CvInfo_GameOption.h"
#include "BBAILog.h"
#include "UWAIAgent.h" // advc.104
#include <numeric> // K-Mod. used in AI_warSpoilsValue

// statics: (advc.003u: Mostly moved to CvTeam)
DllExport CvTeamAI& CvTeamAI::getTeamNonInl(TeamTypes eTeam)
{
	return AI_getTeam(eTeam);
}


CvTeamAI::CvTeamAI(/* advc.003u: */ TeamTypes eID) : CvTeam(eID)
{
	m_pUWAI = new UWAI::Team(); // advc.104
	AI_reset(true);
}


CvTeamAI::~CvTeamAI()
{
	AI_uninit();
	SAFE_DELETE(m_pUWAI); // advc.104
}


void CvTeamAI::AI_init()
{
	AI_reset(false);
}


void CvTeamAI::AI_uninit()
{
	/*	K-Mod. Clearing the memory will cause problems
		if the game is still in progress. */
	//m_aiStrengthMemory.clear();
	/*	advc.158 (note): I'm not seeing a problem with clearing strength memory here,
		but reset and destructor will handle it. */
}


void CvTeamAI::AI_reset(bool bConstructor)
{
	AI_uninit();

	m_eWorstEnemy = NO_TEAM;

	m_aiWarPlanStateCounter.reset();
	m_aiAtWarCounter.reset();
	m_aiAtPeaceCounter.reset();
	m_aiHasMetCounter.reset();
	m_aiOpenBordersCounter.reset();
	m_aiDefensivePactCounter.reset();
	m_aiShareWarCounter.reset();
	m_arWarSuccess.reset();
	m_aiSharedWarSuccess.reset(); // advc.130m
	m_aiEnemyPeacetimeTradeValue.reset();
	m_aiEnemyPeacetimeGrantValue.reset();
	m_aeWarPlan.reset();
	if (!bConstructor && getID() != NO_TEAM)
	{
		for (int i = 0; i < MAX_TEAMS; i++)
		{
			CvTeamAI& kLoopTeam = GET_TEAM((TeamTypes)i);
			kLoopTeam.m_aiWarPlanStateCounter.set(getID(), 0);
			kLoopTeam.m_aiAtWarCounter.set(getID(), 0);
			kLoopTeam.m_aiAtPeaceCounter.set(getID(), 0);
			kLoopTeam.m_aiHasMetCounter.set(getID(), 0);
			kLoopTeam.m_aiOpenBordersCounter.set(getID(), 0);
			kLoopTeam.m_aiDefensivePactCounter.set(getID(), 0);
			kLoopTeam.m_aiShareWarCounter.set(getID(), 0);
			kLoopTeam.m_arWarSuccess.set(getID(), 0);
			kLoopTeam.m_aiSharedWarSuccess.set(getID(), 0); // advc.130m
			kLoopTeam.m_aiEnemyPeacetimeTradeValue.set(getID(), 0);
			kLoopTeam.m_aiEnemyPeacetimeGrantValue.set(getID(), 0);
			kLoopTeam.m_aeWarPlan.set(getID(), NO_WARPLAN);
		}
	}
	m_aiWarPlanCounts.reset(); // advc.opt
	m_bAnyWarPlan = false; // advc.opt
	m_bLonely = false; // advc.109
	m_aeNukeExplosions.clear(); // advc.650
	m_strengthMemory.reset(); // advc.158
}


void CvTeamAI::AI_doTurnPre()
{
	AI_doCounter();
	// <advc.104>
	if ((getUWAI().isEnabled() || getUWAI().isEnabled(true)) && isMajorCiv())
	{
		/*  Calls turnPre on the team members, i.e. UWAI::Civ::turnPre
			happens before CvPlayerAI::AI_turnPre. Needs to be this way b/c
			UWAI::Team::doWar requires the members to be up-to-date. */
		m_pUWAI->turnPre();
	} // </advc.104>
}


void CvTeamAI::AI_doTurnPost()
{
	//AI_updateStrengthMemory(); // K-Mod
	m_strengthMemory.decay(); // advc.158
	// advc.650: Only remembered over the course of one game turn
	m_aeNukeExplosions.clear();

	if (isMajorCiv()) // advc.003n
	{
		/*	K-Mod. Update the attitude cache for all team members.
			(Note: attitude use to be updated near the start of CvGame::doTurn.
			I've moved it here for various reasons.) */
		for (MemberAIIter itMember(getID()); itMember.hasNext(); ++itMember)
		{
			itMember->AI_updateCloseBorderAttitude();
			itMember->AI_updateAttitude();
		} // K-Mod end
		// <advc.109>
		if (getCurrentEra() > GC.getGame().getStartEra())
		{
			// Civs who haven't met half their competitors (rounded down) are lonely
			int iHasMet = getHasMetCivCount(false);
			int iYetToMeet = GC.getGame().countCivTeamsAlive() - iHasMet;
			m_bLonely = (iYetToMeet > iHasMet + 1 && iHasMet <= 2);
		} // </advc.109>
	}

	//AI_updateWorstEnemy(); // advc.130e: Covered by AI_updateAttitude now

	AI_updateAreaStrategies(false);

	/* if (isHuman() || !isMajorCiv())
		return;*/
	/*	disabled by K-Mod. There are some basic things inside AI_doWar
		which are important for all players. */

	AI_doWar();
}


void CvTeamAI::AI_makeAssignWorkDirty()
{
	for (MemberIter it(getID()); it.hasNext(); ++it)
		it->AI_makeAssignWorkDirty();
}

void CvTeamAI::AI_updateAreaStrategies(bool bTargets)
{
	PROFILE_FUNC();

	if (!GC.getGame().isFinalInitialized())
		return;

	FOR_EACH_AREA_VAR(pLoopArea)
		pLoopArea->setAreaAIType(getID(), AI_calculateAreaAIType(*pLoopArea));

	if (bTargets)
		AI_updateAreaTargets();
}


void CvTeamAI::AI_updateAreaTargets()
{
	for (MemberAIIter it(getID()); it.hasNext(); ++it)
	{
		if (it->AI_getCityTargetTimer() == 0) // K-Mod
			it->AI_updateAreaTargets();
	}
}


int CvTeamAI::AI_countFinancialTrouble() const
{
	int iCount = 0;
	for (MemberAIIter it(getID()); it.hasNext(); ++it)
	{
		if (it->AI_isFinancialTrouble())
			iCount++;
	}
	return iCount;
}


int CvTeamAI::AI_countMilitaryWeight(CvArea const* pArea) const
{
	int iCount = 0;
	for (MemberAIIter it(getID()); it.hasNext(); ++it)
		iCount += it->AI_militaryWeight(pArea);
	return iCount;
}

scaled CvTeamAI::AI_estimateDemographic(PlayerTypes ePlayer,
	PlayerHistoryTypes eDemographic, int iSamples) const
{
	//PROFILE_FUNC(); // Called very frequently; about 1.5% of the turn times (July 2019).
	CvPlayer const& kPlayer = GET_PLAYER(ePlayer);
	CvGame const& kGame = GC.getGame();
	int const iGameTurn = kGame.getGameTurn();
	int const iTurnsPlayed = iGameTurn - kGame.getStartTurn();
	iSamples = std::max(0, std::min(iSamples, iTurnsPlayed - 1));
	std::vector<scaled> arSamples;
	arSamples.reserve(iSamples);
	/*	When anarchy lasts several turns, the sample may not contain a single
		non-revolution turn. In this case, increase the sample size gradually. */
	while (arSamples.empty() && iSamples < iTurnsPlayed)
	{
		for (int i = 1; i <= iSamples; i++)
		{
			int iSampleIndex = iGameTurn - i;
			int iHist = kPlayer.getHistory(eDemographic, iSampleIndex);
			if (iHist > 0) // Omit revolution turns
				arSamples.push_back(iHist);
		}
		iSamples++;
	}
	if (arSamples.empty())
		return 0;
	return stats::median(arSamples);
}

/*	advc.104: Replacing AI_estimateTotalYieldRate. This is a team function
	so that we could check for visible demographics. (But we don't b/c the AI
	routinely cheats in that respect.) */
scaled CvTeamAI::AI_estimateYieldRate(PlayerTypes ePlayer,
	YieldTypes eYield, int iSamples) const
{
	PlayerHistoryTypes eHistory = NO_PLAYER_HISTORY;
	switch (eYield)
	{
	case YIELD_COMMERCE:
		eHistory = PLAYER_HISTORY_ECONOMY;
		break;
	case YIELD_PRODUCTION:
		eHistory = PLAYER_HISTORY_INDUSTRY;
		break;
	case YIELD_FOOD:
		eHistory = PLAYER_HISTORY_AGRICULTURE;
		break;
	}
	FAssert(eHistory != NO_PLAYER_HISTORY);
	return AI_estimateDemographic(ePlayer, eHistory, iSamples);
}

/*	K-Mod: return the total yield of the team, estimated by averaging
	over the last few turns of the yield's history graph. */
// (advc.104: Supplanted by AI_estimateYieldRate when UWAI is enabled)
int CvTeamAI::AI_estimateTotalYieldRate(YieldTypes eYield) const
{
	PROFILE_FUNC();
	int const iSampleSize = 5;
	/*	number of turns to use in weighted average.
		Ignore turns with 0 production, because they are probably anarchy.
		Bias towards most recent turns. */
	int const iTurn = GC.getGame().getGameTurn();
	int iTotal = 0;
	for (MemberAIIter it(getID()); it.hasNext(); ++it)
	{
		CvPlayerAI const& kMember = *it;
		int iSubTotal = 0;
		int iBase = 0;
		// advc.004s: Out-of-bounds accesses no longer allowed
		for (int j = 0; j < std::min(iSampleSize, iTurn); j++)
		{
			int iSample = 0;
			switch (eYield)
			{
			case YIELD_PRODUCTION:
				iSample = kMember.getHistory(PLAYER_HISTORY_INDUSTRY,
						iTurn - (j + 1));
				break;
			case YIELD_COMMERCE:
				iSample = kMember.getHistory(PLAYER_HISTORY_ECONOMY,
						iTurn - (j + 1));
				break;
			case YIELD_FOOD:
				iSample = kMember.getHistory(PLAYER_HISTORY_AGRICULTURE,
						iTurn - (j + 1));
				break;
			default: FErrorMsg("unknown yield type");
			}
			if (iSample > 0)
			{
				iSubTotal += (iSampleSize - j) * iSample;
				iBase += iSampleSize - j;
			}
		}
		iTotal += iSubTotal / std::max(1, iBase);
	}
	return iTotal;
}

// K-Mod: return true if is fair enough for the AI to know there is a city here
bool CvTeamAI::AI_deduceCitySite(CvCity const& kCity) const
{
	PROFILE_FUNC();

	if (kCity.isRevealed(getID()))
		return true;

	/*	The rule is this: if we can see more than n plots of the nth culture ring,
		we can deduce where the city is. */

	int iPoints = 0;
	int const iLevel = kCity.getCultureLevel();
	for (SquareIter itPlot(kCity.getPlot(), iLevel, false); itPlot.hasNext(); ++itPlot)
	{
		int iDist = CvCity::cultureDistance(itPlot.currXDist(), itPlot.currYDist());
		if (iDist > iLevel)
			continue;
		if (itPlot->getRevealedOwner(getID()) == kCity.getOwner())
		{
			/*	if multiple cities have their plot in their range,
				then that will make it harder to deduce the precise city location. */
			iPoints += 1 + std::max(0, 1 + iLevel
					- iDist - itPlot->getNumCultureRangeCities(kCity.getOwner()));
			if (iPoints > iLevel)
				return true;
		}
	}
	return false;
}

// advc.erai (based on CvTeam::getCurrentEra):
scaled CvTeamAI::AI_getCurrEraFactor() const
{
	scaled rSum;
	MemberAIIter it(getID());
	for (; it.hasNext(); ++it)
		rSum += it->AI_getCurrEraFactor();
	int const iDiv = it.nextIndex();
	if (iDiv <= 0)
	{
		FAssertMsg(iDiv > 0, "Shouldn't calculate AI era of dead team");
		return -1;
	}
	return rSum / iDiv;
}


bool CvTeamAI::AI_isAnyCapitalAreaAlone() const
{
	for (MemberAIIter it(getID()); it.hasNext(); ++it)
	{
		if (it->AI_isCapitalAreaAlone())
			return true;
	}
	return false;
}


bool CvTeamAI::AI_isPrimaryArea(CvArea const& kArea) const
{
	for (MemberAIIter it(getID()); it.hasNext(); ++it)
	{
		if (it->AI_isPrimaryArea(kArea))
			return true;
	}
	return false;
}


bool CvTeamAI::AI_hasCitiesInPrimaryArea(TeamTypes eTeam) const
{
	FAssert(eTeam != getID());
	FOR_EACH_AREA(pLoopArea)
	{
		if (AI_isPrimaryArea(*pLoopArea))
		{
			if (GET_TEAM(eTeam).countNumCitiesByArea(*pLoopArea))
				return true;
		}
	}
	return false;
}

/*	K-Mod: Return true if this team and eTeam have at least one primary area in common.
	advc: K-Mod code moved into new function CvPlayerAI::AI_hasSharedPrimaryArea
	because I need this at the player level. */
bool CvTeamAI::AI_hasSharedPrimaryArea(TeamTypes eTeam) const
{
	FAssert(eTeam != getID());
	for (MemberAIIter itOurMember(getID()); itOurMember.hasNext(); ++itOurMember)
	{
		for (MemberIter itTheirMember(eTeam); itTheirMember.hasNext(); ++itTheirMember)
		{
			if (itOurMember->AI_hasSharedPrimaryArea(itTheirMember->getID()))
				return true;
		}
	}
	return false;
}

/*  advc.104s (note): If UWAI is enabled, AI_doWar may adjust (i.e. overwrite) the
	result of this calculation through UWAI::Team::alignAreaAI. */
AreaAITypes CvTeamAI::AI_calculateAreaAIType(CvArea const& kArea, bool bPreparingTotal) const
{
	PROFILE_FUNC();

	if (kArea.isWater())
		return AREAAI_NEUTRAL; // K-Mod (no functional change)

	if (isBarbarian())
	{
		if (//kArea.getNumCities() == kArea.getCitiesPerPlayer(BARBARIAN_PLAYER)
			// advc.300: Relatively peaceable (New World) Barbarians until outnumbered
			kArea.getTotalPopulation() <= kArea.getPopulationPerPlayer(BARBARIAN_PLAYER) * 2)
		{
			return AREAAI_ASSAULT;
		}
		if (countNumAIUnitsByArea(kArea, UNITAI_ATTACK) +
			countNumAIUnitsByArea(kArea, UNITAI_ATTACK_CITY) +
			countNumAIUnitsByArea(kArea, UNITAI_PILLAGE) +
			countNumAIUnitsByArea(kArea, UNITAI_ATTACK_AIR) >
			1 + (AI_countMilitaryWeight(&kArea) * 20) / 100)
		{
			return AREAAI_OFFENSIVE; // XXX does this ever happen?
			/*  advc (comment): Does this ever NOT happen? Only once a continent
				is almost entirely owned by civs. */
		}
		return AREAAI_MASSING;
	}

	bool bRecentAttack = false;
	bool bTargets = false;
	bool bChosenTargets = false;
	bool bDeclaredTargets = false;

	bool bAssault = false;
	bool bPreparingAssault = false;

	// int iOffensiveThreshold = (bPreparingTotal ? 25 : 20); // K-Mod, I don't use this.
	int iAreaCities = countNumCitiesByArea(kArea);
	int iWarSuccessRating = AI_getWarSuccessRating(); // K-Mod

	for (TeamIter<MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> it(getID()); it.hasNext(); ++it)
	{
		CvTeam const& kTarget = *it;
		TeamTypes const eTarget = kTarget.getID();
		if (AI_getWarPlan(eTarget) == NO_WARPLAN)
			continue;

		if (AI_getWarPlan(eTarget) == WARPLAN_ATTACKED_RECENT)
		{
			FAssert(isAtWar(eTarget));
			bRecentAttack = true;
		}

		if (kTarget.countNumCitiesByArea(kArea) > 0 &&
				//|| GET_TEAM((TeamTypes)iI).countNumUnitsByArea(kArea) > 4)
			/*  advc.104s: Replacing the above. Setting AreaAI to ASSAULT won't stop
				the AI from fighting any landed units. Need to focus on cities.
				isLandTarget makes sure that there are reachable cities. Still check
				city count for efficiency (there can be a lot of land areas to
				calculate AI types for). */
			AI_isLandTarget(eTarget))
		{
			bTargets = true;
			if (AI_isChosenWar(eTarget))
			{
				bChosenTargets = true;

				if (isAtWar(eTarget) ?
					(AI_getAtWarCounter(eTarget) < 10) :
					AI_isSneakAttackReady(eTarget))
				{
					bDeclaredTargets = true;
				}
			}
		}
		else
		{
			bAssault = true;
			if (AI_isSneakAttackPreparing(eTarget))
				bPreparingAssault = true;
		}
	}

	// K-Mod - based on idea from BBAI
	if (bTargets && iAreaCities > 0 && getNumWars() > 0)
	{
		int iPower = countPowerByArea(kArea);
		int iEnemyPower = AI_countEnemyPowerByArea(kArea);
		iPower *=
				AI_limitedWarPowerRatio() + // advc.107: was 100 flat
							   // (addressing the K-Mod comment below)
				iWarSuccessRating + //(bChosenTargets ? 100 : 50)
				(bChosenTargets || !bRecentAttack ? 100 : 70); // advc.107
		iEnemyPower *= 100;
		/*  it would be nice to put some personality modifiers into this.
			But this is a Team function. :( */
		if (iPower < iEnemyPower)
			return AREAAI_DEFENSIVE;
	} // K-Mod end

	if (bDeclaredTargets)
		return AREAAI_OFFENSIVE;

	if (bTargets)
	{
		/* BBAI code. -- This code has two major problems.
		* Firstly, it makes offense more likely when we are in more wars.
		* Secondly, it chooses offense based on how many offense units we have --
		* but offense units are built for offense areas!
		*
		// AI_countMilitaryWeight is based on this team's pop and cities ...
		// if this team is the biggest, it will over estimate needed units
		int iMilitaryWeight = AI_countMilitaryWeight(&kArea);
		int iCount = 1;
		for (int iJ = 0; iJ < MAX_CIV_TEAMS; iJ++) {
			if (iJ != getID() && GET_TEAM((TeamTypes)iJ).isAlive()) {
				if (!(GET_TEAM((TeamTypes)iJ).isBarbarian() ||
						GET_TEAM((TeamTypes)iJ).isMinorCiv())) {
					if (AI_getWarPlan((TeamTypes)iJ) != NO_WARPLAN) {
						iMilitaryWeight += GET_TEAM((TeamTypes)iJ).
								AI_countMilitaryWeight(&kArea);
						iCount++;
						if (GET_TEAM((TeamTypes)iJ).isAVassal()) {
							for (int iK = 0; iK < MAX_CIV_TEAMS; iK++) {
								if (iK != getID() && GET_TEAM((TeamTypes)iK).isAlive()) {
									if (GET_TEAM((TeamTypes)iJ).isVassal((TeamTypes)iK)) {
										iMilitaryWeight += GET_TEAM((TeamTypes)iK).
												AI_countMilitaryWeight(&kArea);
		} } } } } } } }
		iMilitaryWeight /= iCount;
		if (countNumAIUnitsByArea(kArea, UNITAI_ATTACK) +
				countNumAIUnitsByArea(kArea, UNITAI_ATTACK_CITY) +
				countNumAIUnitsByArea(kArea, UNITAI_PILLAGE) +
				countNumAIUnitsByArea(kArea, UNITAI_ATTACK_AIR) >
				(iMilitaryWeight * iOffensiveThreshold) / 100 + 1)
			return AREAAI_OFFENSIVE;*/
		/*  K-Mod. I'm not sure how best to do this yet. Let me just try a rough
			idea for now. I'm using AI_countMilitaryWeight; but what I really
			want is "border territory which needs defending" */
		int iOurRelativeStrength = 100 * countPowerByArea(kArea) /
				(AI_countMilitaryWeight(&kArea) + 20);
		iOurRelativeStrength *= 100 + (bDeclaredTargets ? 30 : 0) +
				(bPreparingTotal ? -20 : 0) + iWarSuccessRating/2;
		iOurRelativeStrength /= 100;
		int iEnemyRelativeStrength = 0;
		bool bEnemyCities = false;

		for (TeamAIIter<CIV_ALIVE,KNOWN_POTENTIAL_ENEMY_OF> it(getID()); it.hasNext(); ++it)
		{
			CvTeamAI const& kLoopTeam = *it;
			if (AI_getWarPlan(kLoopTeam.getID()) == NO_WARPLAN)
				continue;

			int iPower = 100 * kLoopTeam.countPowerByArea(kArea);
			int iCommitment = (bPreparingTotal ? 30 : 20) +
					kLoopTeam.AI_countMilitaryWeight(&kArea) *
					((isAtWar(kLoopTeam.getID()) ? 1 : 2) +
					kLoopTeam.getNumWars(true, true)) / 2;
			iPower /= iCommitment;
			iEnemyRelativeStrength += iPower;
			if (kLoopTeam.countNumCitiesByArea(kArea) > 0)
				bEnemyCities = true;
		}
		if (bEnemyCities && iOurRelativeStrength > iEnemyRelativeStrength)
			return AREAAI_OFFENSIVE;
		// K-Mod end
	}

	if (bTargets)
	{
		for (MemberAIIter itMember(getID()); itMember.hasNext(); ++itMember)
		{
			if (itMember->AI_isDoStrategy(AI_STRATEGY_DAGGER) ||
				itMember->AI_isDoStrategy(AI_STRATEGY_FINAL_WAR))
			{
				if (kArea.getCitiesPerPlayer(itMember->getID()) > 0)
					return AREAAI_MASSING;
			}
		}
		if (bRecentAttack)
		{
			int iPower = countPowerByArea(kArea);
			int iEnemyPower = AI_countEnemyPowerByArea(kArea);
			if (iPower > iEnemyPower)
				return AREAAI_MASSING;
			return AREAAI_DEFENSIVE;
		}
	}
	// advc.107: 2*iAreaCities (from MNAI)
	if (iAreaCities > 0 && AI_countEnemyDangerByArea(kArea) > 2 * iAreaCities)
		return AREAAI_DEFENSIVE;

	if (bChosenTargets)
		return AREAAI_MASSING;

	if (bTargets)
	{
		if (iAreaCities > getNumMembers() * 3)
		{
			if (GC.getGame().isOption(GAMEOPTION_AGGRESSIVE_AI) ||
				GC.getGame().isOption(GAMEOPTION_ALWAYS_WAR) ||
				(countPowerByArea(kArea) * 2 >
				AI_countEnemyPowerByArea(kArea) * 3))
			{
				return AREAAI_MASSING;
			}
		}
		return AREAAI_DEFENSIVE;
	}
	else if (bAssault)
	{
		if (AI_isPrimaryArea(kArea))
		{
			if (bPreparingAssault)
				return AREAAI_ASSAULT_MASSING;
		}
		else if (countNumCitiesByArea(kArea) > 0)
			return AREAAI_ASSAULT_ASSIST;
		return AREAAI_ASSAULT;
	}
	return AREAAI_NEUTRAL;
}


int CvTeamAI::AI_calculateAdjacentLandPlots(TeamTypes eTeam) const
{
	PROFILE_FUNC();

	FAssertMsg(eTeam != getID(), "shouldn't call this function on ourselves");

	int iCount = 0;
	for (int iI = 0; iI < GC.getMap().numPlots(); iI++)
	{
		CvPlot const& kPlot = GC.getMap().getPlotByIndex(iI);
		if (!kPlot.isWater())
		{
			if (kPlot.getTeam() == eTeam && kPlot.isAdjacentTeam(getID(), true))
				iCount++;
		}
	}
	return iCount;
}

/*  advc.003j: These three functions were obsoleted by K-Mod
	(used to be called from CvTeamAI::AI_startWarVal).
	Bodies deleted on 2 Dec 2019. */
/*int CvTeamAI::AI_calculatePlotWarValue(TeamTypes eTeam) const { ... }
// BETTER_BTS_AI_MOD, War Strategy AI, 07/21/08, jdog5000:
int CvTeamAI::AI_calculateBonusWarValue(TeamTypes eTeam) const { ... }
int CvTeamAI::AI_calculateCapitalProximity(TeamTypes eTeam) const { ... }*/

// K-Mod: Return true if we can deduce the location of at least 'iMiniumum' cities belonging to eTeam.
bool CvTeamAI::AI_haveSeenCities(TeamTypes eTeam, bool bPrimaryAreaOnly, int iMinimum) const
{
	int iCount = 0;
	for (MemberIter it(getID()); it.hasNext(); ++it)
	{
		CvPlayer const& kMember = *it;
		FOR_EACH_CITY(pLoopCity, kMember)
		{
			if (AI_deduceCitySite(*pLoopCity))
			{
				if (!bPrimaryAreaOnly || AI_isPrimaryArea(pLoopCity->getArea()))
				{
					if (++iCount >= iMinimum)
						return true;
				}
			}
		}
	}
	return false;
}


bool CvTeamAI::AI_isWarPossible() const
{
	if (getNumWars(false) > 0)
		return true;
	/*  advc (comment): The option applies only to humans but still implies that
		all the non-human civs will have a (human) war enemy. */
	if (GC.getGame().isOption(GAMEOPTION_ALWAYS_WAR))
		return true;
	return (!GC.getGame().isOption(GAMEOPTION_ALWAYS_PEACE) &&
			!GC.getGame().isOption(GAMEOPTION_NO_CHANGING_WAR_PEACE));
}

/*	This function has been completely rewritten for K-Mod.
	The original BtS and BBAI code have been deleted. */
bool CvTeamAI::AI_isLandTarget(TeamTypes eTarget,
	bool bCheckAlliesOfTarget) const // advc
{
	PROFILE_FUNC();

	FAssert(eTarget != BARBARIAN_TEAM);
	CvTeamAI const& kTarget = GET_TEAM(eTarget);
	// <advc.104s>
	if(getUWAI().isEnabled() && isMajorCiv() && kTarget.isMajorCiv())
		return uwai().isLandTarget(eTarget);
	// </advc.104s>
	FOR_EACH_AREA(pLoopArea)
	{
		if (AI_isPrimaryArea(*pLoopArea) && kTarget.AI_isPrimaryArea(*pLoopArea))
			return true;
	}
	// advc.pf: Replacing BBAI instantiation of FAStar
	TeamPathFinder<TeamPath::LAND> pathFinder(*this, &GET_TEAM(eTarget), 18);
	for (MemberAIIter itOur(getID()); itOur.hasNext(); ++itOur)
	{
		CvPlayerAI const& kOurMember = *itOur;
		FOR_EACH_CITY(pOurCity, kOurMember)
		{
			if (!kOurMember.AI_isPrimaryArea(pOurCity->getArea()))
				continue;
			// city in a primary area.
			for (MemberAIIter itTheirMember(eTarget);
				itTheirMember.hasNext(); ++itTheirMember)
			{
				if (!itTheirMember->AI_isPrimaryArea(pOurCity->getArea()))
					continue;
				FOR_EACH_CITY(pTheirCity, *itTheirMember)
				{
					if (pathFinder.generatePath(pOurCity->getPlot(), pTheirCity->getPlot()))
						return true;
				}
			}
		}
	}
	// advc: Cut from deleted AI_isAllyLandTarget
	if (bCheckAlliesOfTarget)
	{
		/*  advc.001: I don't think the K-Mod code worked when eTarget was a vassal
			whose master has a DP */
		TeamTypes const eTargetMaster = GET_TEAM(eTarget).getMasterTeam();
		for (TeamIter<CIV_ALIVE,KNOWN_POTENTIAL_ENEMY_OF> it(getID()); it.hasNext(); ++it)
		{
			CvTeam& kLoopTeam = *it;
			if (kLoopTeam.getID() == eTarget)
				continue; // Already checked above
			if (kLoopTeam.getMasterTeam() == eTargetMaster ||
				kLoopTeam.isDefensivePact(eTargetMaster))
			{
				// Recursion with bCheckAlliesOfTarget=false
				if (AI_isLandTarget(kLoopTeam.getID()))
					return true;
			}
		}
	}
	return false;
}

/*	BETTER_BTS_AI_MOD, General AI, 01/10/10, jdog5000: START
	advc.pf: Moved from CvPlot. At least the first one cares about war plans and
	is therefore AI code. The second one doesn't have a plausible use for
	human players either, and I want to keep them together. */
bool CvTeamAI::AI_isHasPathToEnemyCity(CvPlot const& kFrom, bool bIgnoreBarb) const
{
	PROFILE_FUNC();

	// Imitate instatiation of irrigated finder ...
	/*std::vector<TeamTypes> teamVec;
	teamVec.push_back(getID());
	teamVec.push_back(NO_TEAM);*/
	/*	advc.001: This is wrong - we need to set a target team. (Thx to spqkfk
		for making me aware.) Checking all enemy capitals upfront (to save time)
		is then (if we do it correctly) also a bad idea. Typically, there
		won't be a high number of enemy capitals anyway. */
	// advc.pf: Deleted remaining BBAI code on 21 Oct 2020. Replacement:
	for (TeamIter<ALIVE,KNOWN_POTENTIAL_ENEMY_OF> itEnemy(getID());
		itEnemy.hasNext(); ++itEnemy)
	{
		if (bIgnoreBarb && (itEnemy->isBarbarian() || itEnemy->isMinorCiv()))
			continue;
		if (AI_getWarPlan(itEnemy->getID()) != NO_WARPLAN &&
			AI_isHasPathToEnemyCity(kFrom, *itEnemy))
		{
			return true;
		}
	}
	return false;
}

// advc: Was "isHasPathToPlayerCity" and was only used for debug info
bool CvTeamAI::AI_isHasPathToEnemyCity(CvPlot const& kFrom,
	CvTeam const& kEnemy) const
{
	PROFILE_FUNC();
	// Imitate instatiation of irrigated finder ...
	// advc.pf: Deleted on 21 Oct 2020, replaced with TeamStepfinder.
	TeamPathFinder<TeamPath::LAND> pathFinder(*this, &kEnemy, 18);
	for (MemberIter itMember(kEnemy.getID()); itMember.hasNext(); ++itMember)
	{
		if (kFrom.getArea().getCitiesPerPlayer(itMember->getID()) <= 0)
			continue;
		FOR_EACH_CITY(pCity, *itMember)
		{
			if (pathFinder.generatePath(kFrom, pCity->getPlot()))
				return true;
		}
	}
	return false;
} // BETTER_BTS_AI_MOD: END


bool CvTeamAI::AI_shareWar(TeamTypes eTeam) const
{
	for (TeamIter<MAJOR_CIV,ENEMY_OF> it(getID()); it.hasNext(); ++it)
	{
		if (it->isAtWar(eTeam))
			return true;
	}
	return false;
}

// advc:
void CvTeamAI::AI_updateAttitude(TeamTypes eTeam, /* advc.130e: */ bool bUpdateWorstEnemy)
{
	if(!GC.getGame().isFinalInitialized() || eTeam == getID())
		return;
	for (MemberAIIter itOurMember(getID()); itOurMember.hasNext(); ++itOurMember)
	{
		for (MemberIter itTheirMember(eTeam); itTheirMember.hasNext(); ++itTheirMember)
		{
			itOurMember->AI_updateAttitude(itTheirMember->getID(),
					bUpdateWorstEnemy); // advc.130e
		}
	}
}


AttitudeTypes CvTeamAI::AI_getAttitude(TeamTypes eTeam, bool bForced) const
{
	// bbai. Average values rather than attitudes directly.
	// K-Mod. Removed attitude averaging between vassals and masters
	// advc: ... so we can just call AI_getAttitudeVal
	return CvPlayerAI::AI_getAttitudeFromValue(AI_getAttitudeVal(eTeam, bForced));
}


int CvTeamAI::AI_getAttitudeVal(TeamTypes eTeam, bool bForced, bool bAssert) const
{
	//PROFILE_FUNC(); // advc: almost negligible
	//FAssertMsg(eTeam != getID(), "shouldn't call this function on ourselves");
	// <advc> (K-Mod had returned FRIENDLY from AI_getAttitude instead)
	if (eTeam == getID())
		return 100; // </advc>

	int iAttitudeVal = 0;
	int iCount = 0;
	for (MemberAIIter itOurMember(getID()); itOurMember.hasNext(); ++itOurMember)
	{
		for (MemberIter itTheirMember(eTeam); itTheirMember.hasNext(); ++itTheirMember)
		{
			iAttitudeVal += itOurMember->AI_getAttitudeVal(itTheirMember->getID(), bForced);
			iCount++;
		}
	}
	if (iCount > 0)
		return iAttitudeVal / iCount; // bbai / K-Mod
	// <advc>
	FAssert(!bAssert || iCount > 0); // (OK when loading from very old savegames or when defeated during Auto Play)
	// K-Mod had returned ATTITUDE_CAUTIOUS from AI_getAttitude
	return 0; // </advc>
}


int CvTeamAI::AI_getMemoryCount(TeamTypes eTeam, MemoryTypes eMemory) const
{
	FAssert(eTeam != getID());

	int iMemoryCount = 0;
	int iCount = 0;
	for (MemberAIIter itOurMember(getID()); itOurMember.hasNext(); ++itOurMember)
	{
		for (MemberIter itTheirMember(eTeam); itTheirMember.hasNext(); ++itTheirMember)
		{
			iMemoryCount += itOurMember->AI_getMemoryCount(itTheirMember->getID(), eMemory);
			iCount++;
		}
	}
	if (iCount > 0)
		return iMemoryCount / iCount;
	FAssert(iCount > 0);
	return 0;
}


int CvTeamAI::AI_chooseElection(VoteSelectionData const& kVoteSelectionData) const
{
	VoteSourceTypes eVoteSource = kVoteSelectionData.eVoteSource;

	FAssert(!isHuman());
	FAssert(GC.getGame().getSecretaryGeneral(eVoteSource) == getID());

	int iBestVote = -1;
	int iBestValue = 0;
	for (size_t i = 0; i < kVoteSelectionData.aVoteOptions.size(); i++)
	{
		VoteSelectionSubData const& kVoteData = kVoteSelectionData.aVoteOptions[i];
		VoteTypes const eVote = kVoteData.eVote;
		FAssert(GC.getInfo(eVote).isVoteSourceType(eVoteSource));
		FAssert(GC.getGame().isChooseElection(eVote));
		bool bValid = true;
		bool bCanWinDiplo = false; // advc.115b
		if (!GC.getGame().isTeamVote(eVote))
		{
			for (MemberAIIter it(getID()); it.hasNext(); ++it)
			{
				PlayerVoteTypes ePlayerVote = // kekm.25: was eVote (name clash)
						it->AI_diploVote(kVoteData, eVoteSource, true);
				//if (eVote != PLAYER_VOTE_YES || eVote == GC.getGame().getVoteOutcome((VoteTypes)iI))
				/*  <kekm.25> "AI can choose to repeal an already passed resolution
					if all team members agree" (Tagging advc.001 b/c the BtS check was incorrect) */
				bool bVoteYes = (ePlayerVote == PLAYER_VOTE_YES);
				bool bAlreadyPassed = (GC.getGame().getVoteOutcome(eVote) == PLAYER_VOTE_YES);
				if((bVoteYes && bAlreadyPassed) || (!bVoteYes && !bAlreadyPassed)) // </kekm.25>
				{
					bValid = false;
					break;
				}
			}
		}  // <advc.115b>
		else if(!isAVassal())
			bCanWinDiplo = AI_anyMemberAtVictoryStage(AI_VICTORY_DIPLOMACY4);
		// </advc.115b>
		if (bValid)
		{
			int iValue = 1 + SyncRandNum(10000);
			/*  <advc.115b> Always pick victory. Probabilistically instead? 8000
				would be an 80% chance if there's one other proposal. */
			if(bCanWinDiplo)
				iValue += 20000; // </advc.115b>
			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				iBestVote = i;
			}
		}
	}

	return iBestVote;
}

// advc: Body cut from CvTeam::declareWar in order to reduce entanglement of AI and game rule code
void CvTeamAI::AI_preDeclareWar(TeamTypes eTarget, WarPlanTypes eWarPlan, bool bPrimaryDoW,
	PlayerTypes eSponsor) // advc.100
{
	CvTeamAI& kTarget = GET_TEAM(eTarget);
	/*  <advc.104q> At this point, the state counter says how long war has been
		imminent - that's no longer important once war is declared. Should instead
		count the war duration. (Note that AI_getAtWarCounter isn't an accurate counter.) */
	AI_setWarPlanStateCounter(eTarget, 0);
	kTarget.AI_setWarPlanStateCounter(getID(), 0);
	// </advc.104q>
	if (!isMajorCiv())
		return;
	/*  advc.130h: Moved this loop into AI_preDeclareWar b/c I'm adding code that
		depends on the atWarWithPartner status before the DoW. */
	for (MemberAIIter itOur(getID()); itOur.hasNext(); ++itOur)
	{
		CvPlayerAI& kOurMember = *itOur;
		for (PlayerAIIter<MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> itEnemy(getID());
			itEnemy.hasNext(); ++itEnemy)
		{
			CvPlayerAI& kPlayer = *itEnemy;
			// <advc.130o>
			if (bPrimaryDoW && kOurMember.isHuman() && !kPlayer.isHuman() &&
				kTarget.AI_getMemoryCount(getID(), MEMORY_MADE_DEMAND) > 0)
			{
				// Raise it to 8 (or what XML says)
				int iMemory = kPlayer.AI_getMemoryCount(kOurMember.getID(),
						MEMORY_MADE_DEMAND_RECENT);
				static int const iWAR_DESPITE_TRIBUTE_MEMORY = GC.getDefineINT(
						"WAR_DESPITE_TRIBUTE_MEMORY");
				int iDelta = iWAR_DESPITE_TRIBUTE_MEMORY;
				iDelta = std::max(iMemory, iDelta) - iMemory;
				kPlayer.AI_changeMemoryCount(kOurMember.getID(),
						MEMORY_MADE_DEMAND_RECENT, iDelta);
			}
			if (bPrimaryDoW)
				kOurMember.AI_setMemoryCount(kPlayer.getID(), MEMORY_MADE_DEMAND, 0);
			// </advc.130o>
			if (kPlayer.getTeam() == eTarget)
			{
				if(bPrimaryDoW) // advc.130y
				{
					// advc.130j:
					kPlayer.AI_rememberEvent(kOurMember.getID(), MEMORY_DECLARED_WAR);
				}
				// advc.130y:
				else kPlayer.AI_changeMemoryCount(kOurMember.getID(), MEMORY_DECLARED_WAR, 2);
			} // advc.130h:
			if (kPlayer.AI_disapprovesOfDoW(getID(), eTarget)) // advc.130j:
				kPlayer.AI_rememberEvent(kOurMember.getID(), MEMORY_DECLARED_WAR_ON_FRIEND);
		}
	}  // <advc.104i>
	if (eSponsor != NO_PLAYER)
	{
		AI_makeUnwillingToTalk(eTarget);
		if (GET_TEAM(eSponsor).isAtWar(eTarget))
			GET_TEAM(eSponsor).AI_makeUnwillingToTalk(eTarget);
	} // </advc.104i>
}

// advc: Body cut from CvTeam::declareWar
void CvTeamAI::AI_postDeclareWar(TeamTypes eTarget, WarPlanTypes eWarPlan)
{
	CvTeamAI& kTarget = GET_TEAM(eTarget);

	AI_setAtPeaceCounter(eTarget, 0);
	kTarget.AI_setAtPeaceCounter(getID(), 0);
	AI_setShareWarCounter(eTarget, 0);
	kTarget.AI_setShareWarCounter(getID(), 0);
	kTarget.AI_setWarPlan(getID(), (isBarbarian() || isMinorCiv()) ?
			WARPLAN_ATTACKED : WARPLAN_ATTACKED_RECENT);
	if (!getUWAI().isEnabled()) // advc.104
	{
		for (TeamIter<MAJOR_CIV> it; it.hasNext(); ++it)
		{
			TeamTypes eTargetOfTarget = it->getID();
			if (!kTarget.isAtWar(eTargetOfTarget) &&
					kTarget.AI_isChosenWar(eTargetOfTarget))
				kTarget.AI_setWarPlan(eTargetOfTarget, NO_WARPLAN);
		}
	}
	if (eWarPlan != NO_WARPLAN)
		AI_setWarPlan(eTarget, eWarPlan);

	FAssert(!AI_isSneakAttackPreparing(eTarget) ||
		/*  advc.104o: Can happen when hired to declare war while preparing.
			BtS/K-Mod doesn't allow hired war while preparing, but UWAI does.
			The K-Mod code below already handles WARPLAN_PREPARING_..., so, no problem. */
			getUWAI().isEnabled());
	if (AI_getWarPlan(eTarget) == NO_WARPLAN || AI_isSneakAttackPreparing(eTarget))
	{
		if (isHuman() ||
			// K-Mod. (for vassals that have been told to prepare for war)
			AI_getWarPlan(eTarget) == WARPLAN_PREPARING_TOTAL)
		{
			AI_setWarPlan(eTarget, WARPLAN_TOTAL);
		}
		else if (isMinorCiv() || isBarbarian() || kTarget.getNumWars() == 1)
			AI_setWarPlan(eTarget, WARPLAN_LIMITED);
		else AI_setWarPlan(eTarget, WARPLAN_DOGPILE);
	}
}

// advc: Body cut from CvTeam::makePeace
void CvTeamAI::AI_preMakePeace(TeamTypes eTarget, CLinkList<TradeData> const* pReparations)
{
	CvTeamAI& kTarget = GET_TEAM(eTarget);
	// <advc.104> Report who won the war before war success is reset
	if (getUWAI().isEnabled() && getUWAI().isReady())
	{
		uwai().reportWarEnding(eTarget, pReparations, NULL);
		kTarget.uwai().reportWarEnding(getID(), NULL, pReparations);
	} // </advc.104>
	/*  <advc.130y> Don't know if they started the war, but, if we did and they had
		started a war against us some time earlier, we may as well forgive them for
		that. (If there's no declared-war-on-us memory, then this call has no effect.) */
	AI_forgiveEnemy(eTarget, isCapitulated(), false);
	kTarget.AI_forgiveEnemy(getID(), kTarget.isCapitulated(), false);
	// </advc.130y>  <advc.130i>
	if (getUWAI().isEnabled() && !isAVassal() && !kTarget.isAVassal())
	{
		for (PlayerAIIter<FREE_MAJOR_CIV> itDP; itDP.hasNext(); ++itDP)
		{
			CvPlayerAI& kDPPlayer = *itDP;
			for (TeamTypes eTeam = getID(); eTeam != NO_TEAM;
				eTeam = (eTeam == eTarget ? NO_TEAM : eTarget))
			{
				if (!GET_TEAM(kDPPlayer.getTeam()).isDefensivePact(eTeam))
					continue;
				for (MemberAIIter itMember(eTeam); itMember.hasNext(); ++itMember)
				{
					kDPPlayer.AI_setMemoryCount(itMember->getID(), MEMORY_DECLARED_WAR_RECENT, 0);
					itMember->AI_setMemoryCount(kDPPlayer.getID(), MEMORY_DECLARED_WAR_RECENT, 0);
				}
			}
		}
	} // </advc.130i>
}

// advc: Body cut from CvTeam::makePeace
void CvTeamAI::AI_postMakePeace(TeamTypes eTarget)
{
	CvTeamAI& kTarget = GET_TEAM(eTarget);
	AI_setAtWarCounter(eTarget, 0);
	kTarget.AI_setAtWarCounter(getID(), 0);

	AI_setWarSuccess(eTarget, 0);
	kTarget.AI_setWarSuccess(getID(), 0);

	AI_setWarPlan(eTarget, NO_WARPLAN);
	kTarget.AI_setWarPlan(getID(), NO_WARPLAN);

	// K-Mod. update attitude
	if (!GC.getGame().isFinalInitialized())
		return;

	for (PlayerAIIter<MAJOR_CIV> itWar; itWar.hasNext(); ++itWar)
	{
		CvPlayerAI& kWarPlayer = *itWar;
		CvTeam const& kWarTeam = GET_TEAM(kWarPlayer.getTeam());
		if (kWarTeam.getID() == eTarget || kWarTeam.getID() == getID() ||
			kWarTeam.isAtWar(eTarget) || kWarTeam.isAtWar(getID()))
		{
			for (PlayerIter<MAJOR_CIV> itMember; itMember.hasNext(); ++itMember)
			{
				PlayerTypes eMember = itMember->getID();
				// <advc.001>
				if(eMember == kWarPlayer.getID())
					continue; // </advc.001>
				if (TEAMID(eMember) == eTarget || TEAMID(eMember) == getID())
					kWarPlayer.AI_updateAttitude(eMember);
			}
		}
	} // K-Mod end
}

// K-Mod. New war evaluation functions. WIP
// Very rough estimate of what would be gained by conquering the target - in units of Gold/turn (kind of).
int CvTeamAI::AI_warSpoilsValue(TeamTypes eTarget, WarPlanTypes eWarPlan,
	bool bConstCache) const // advc.001n
{
	PROFILE_FUNC();

	FAssert(eTarget != getID());
	const CvTeamAI& kTargetTeam = GET_TEAM(eTarget);
	bool bAggresive = GC.getGame().isOption(GAMEOPTION_AGGRESSIVE_AI);

	// Deny factor: the percieved value of denying the enemy team of its resources (generally)
	int iDenyFactor = bAggresive
		? 40 - AI_getAttitudeWeight(eTarget)/3
		: 20 - AI_getAttitudeWeight(eTarget)/2;

	iDenyFactor += AI_getWorstEnemy() == eTarget ? 20 : 0; // (in addition to attitude pentalities)

	if (kTargetTeam.AI_anyMemberAtVictoryStage3())
	{
		if (kTargetTeam.AI_anyMemberAtVictoryStage4())
		{
			iDenyFactor += AI_anyMemberAtVictoryStage4() ? 50 : 30;
		}

		if (bAggresive || AI_anyMemberAtVictoryStage(AI_VICTORY_CONQUEST3))
		{
			iDenyFactor += 20;
		}

		if (GC.getGame().getTeamRank(eTarget) < GC.getGame().getTeamRank(getID()))
		{
			iDenyFactor += 10;
		}
	}
	if (AI_anyMemberAtVictoryStage(AI_VICTORY_MILITARY4))
	{
		iDenyFactor += 20;
	}

	int iRankDelta = GC.getGame().getTeamRank(getID()) - GC.getGame().getTeamRank(eTarget);
	if (iRankDelta > 0)
	{
		int iRankHate = 0;
		for (int i = 0; i < MAX_CIV_PLAYERS; i++)
		{
			const CvPlayerAI& kLoopPlayer = GET_PLAYER((PlayerTypes)i);
			if (kLoopPlayer.getTeam() == getID() && kLoopPlayer.isAlive())
				iRankHate += GC.getInfo(kLoopPlayer.getPersonalityType()).getWorseRankDifferenceAttitudeChange(); // generally around 0-3
		}

		if (iRankHate > 0)
		{
			int iTotalTeams = GC.getGame().getCivTeamsEverAlive();
			iDenyFactor += (100 - AI_getAttitudeWeight(eTarget)) *
					(iRankHate * iRankDelta + (iTotalTeams+1)/2) /
					std::max(1, 8*(iTotalTeams + 1)*getAliveCount());
			// that's a max of around 200 * 3 / 8. ~ 75
		}
	}

	bool bImminentVictory = kTargetTeam.AI_getLowestVictoryCountdown() >= 0;

	bool bTotalWar = eWarPlan == WARPLAN_TOTAL || eWarPlan == WARPLAN_PREPARING_TOTAL;
	bool bOverseasWar = !AI_hasSharedPrimaryArea(eTarget);

	int iGainedValue = 0;
	int iDeniedValue = 0;

	// Cities & Land
	int iPopCap = 2 + getTotalPopulation(false) / std::max(1, getNumCities()); // max number of plots to consider the value of.
	int iYieldMultiplier = 0; // multiplier for the value of plot yields.
	for (int i = 0; i < MAX_PLAYERS; i++)
	{
		CvPlayerAI const& kLoopPlayer = GET_PLAYER((PlayerTypes)i);
		if (kLoopPlayer.getTeam() != getID() || !kLoopPlayer.isAlive())
			continue;
		int iFoodMulti = kLoopPlayer.AI_averageYieldMultiplier(YIELD_FOOD);
		iYieldMultiplier += kLoopPlayer.AI_averageYieldMultiplier(YIELD_PRODUCTION) * iFoodMulti / 100;
		iYieldMultiplier += kLoopPlayer.AI_averageYieldMultiplier(YIELD_COMMERCE) * iFoodMulti / 100;
	}
	iYieldMultiplier /= std::max(1, 2 * getAliveCount());
	iYieldMultiplier = iYieldMultiplier *
			/*	now.. here's a bit of ad-hoccery.
				the actual yield multiplayer is not the only thing that goes up
				as the game progresses. the raw produce of land also tends to increase
				as improvements become more powerful. Therefore... */
			(1 + GET_PLAYER(getLeaderID()).getCurrentEra() + GC.getNumEraInfos()) /
			std::max(1, GC.getNumEraInfos());

	std::set<int> close_areas; // IDs of areas in which the enemy has cities close to ours
	for (MemberAIIter itMember(eTarget); itMember.hasNext(); ++itMember)
	{
		CvPlayerAI const& kLoopPlayer = *itMember;
		FOR_EACH_CITYAI(pLoopCity, kLoopPlayer)
		{
			if (!AI_deduceCitySite(*pLoopCity))
				continue;

			int iCityValue = pLoopCity->getPopulation();

			bool bCoastal = pLoopCity->isCoastal();
			iCityValue += bCoastal ? 2 : 0;

			// plots
			std::vector<int> plot_values;
			for (CityPlotIter itPlot(*pLoopCity, false); itPlot.hasNext(); ++itPlot)
			{
				CvPlot const& kPlot = *itPlot;
				if (!kPlot.isRevealed(getID()) || kPlot.getWorkingCity() != pLoopCity)
					continue;
				if (kPlot.isWater() &&
					!(bCoastal && kPlot.calculateNatureYield(YIELD_FOOD, getID()) >=
					GC.getFOOD_CONSUMPTION_PER_POPULATION()))
				{
					continue;
				}
				/*	This is a very rough estimate of the value of the plot.
					It's a bit ad-hoc. I'm sorry about that, but I want it to be fast. */
				//BonusTypes eBonus = pLoopPlot->getBonusType(getID());
				int iPlotValue = 0;
				// don't ignore floodplains
				iPlotValue += 3 * kPlot.calculateBestNatureYield(YIELD_FOOD, getID());
				// ignore forest
				iPlotValue += 2 * kPlot.calculateNatureYield(YIELD_PRODUCTION, getID(), true);
				iPlotValue += (GC.getInfo(kPlot.getTerrainType()).getYield(YIELD_FOOD) >=
						GC.getFOOD_CONSUMPTION_PER_POPULATION() ? 1 : 0); // bonus for grassland
				iPlotValue += kPlot.isRiver() ? 1 : 0;
				if (kPlot.getBonusType(getID()) != NO_BONUS)
					iPlotValue = iPlotValue * 3/2;
				iPlotValue += kPlot.getYield(YIELD_COMMERCE) / 2; // include some value for existing towns.

				plot_values.push_back(iPlotValue);
			}
			std::partial_sort(
					plot_values.begin(),
					plot_values.begin() + std::min<int>(iPopCap, plot_values.size()),
					plot_values.end(),
					std::greater<int>());
			iCityValue = std::accumulate(
					plot_values.begin(),
					plot_values.begin() + std::min<int>(iPopCap, plot_values.size()),
					iCityValue);
			iCityValue = iCityValue * iYieldMultiplier / 100;

			// holy city value
			FOR_EACH_ENUM(Religion)
			{
				if (pLoopCity->isHolyCity(eLoopReligion))
				{
					iCityValue += std::max(0, GC.getGame().countReligionLevels(eLoopReligion) /
							(pLoopCity->hasShrine(eLoopReligion) ? 1 : 2) - 4);
				}
				/*	note: the -4 at the end is mostly there to
					offset the 'wonder' value that will be added later.
					I don't want to double-count the value of the shrine,
					and the religion without the shrine isn't worth much anyway. */
			}

			// corp HQ value
			FOR_EACH_ENUM(Corporation)
			{
				if (pLoopCity->isHeadquarters(eLoopCorporation))
				{
					iCityValue += std::max(0, 2 *
							GC.getGame().countCorporationLevels(eLoopCorporation) - 4);
				}
			}

			// wonders
			iCityValue += 4 * pLoopCity->getNumActiveWorldWonders();

			// denied
			iDeniedValue += iCityValue * iDenyFactor / 100;
			if (2*pLoopCity->getCulture(kLoopPlayer.getID()) >
				pLoopCity->getCultureThreshold(GC.getGame().culturalVictoryCultureLevel()))
			{
				iDeniedValue += ((kLoopPlayer.AI_atVictoryStage(AI_VICTORY_CULTURE4) ? 100 : 30) *
						iDenyFactor) / 100;
			}
			if (bImminentVictory && pLoopCity->isCapital())
			{
				iDeniedValue += 200 * iDenyFactor / 100;
			}

			// gained
			int iGainFactor = 0;
			if (bTotalWar)
			{
				if (AI_isPrimaryArea(pLoopCity->getArea()))
					iGainFactor = 70;
				else
				{
					if (bOverseasWar &&
						GET_PLAYER(pLoopCity->getOwner()).
						AI_isPrimaryArea(pLoopCity->getArea()))
					{
						iGainFactor = 45;
					}
					else iGainFactor = 30;

					iGainFactor += AI_anyMemberAtVictoryStage(
							AI_VICTORY_CONQUEST3 | AI_VICTORY_DOMINATION2) ? 10 : 0;
				}
			}
			else
			{
				if (AI_isPrimaryArea(pLoopCity->getArea()))
					iGainFactor = 40;
				else
					iGainFactor = 25;
			}
			if (pLoopCity->AI_highestTeamCloseness(getID(), bConstCache) > 0)
			{
				iGainFactor += 30;
				close_areas.insert(pLoopCity->getArea().getID());
			}

			iGainedValue += iCityValue * iGainFactor / 100;
		}
	}

	// Resources
	std::vector<int> bonuses(GC.getNumBonusInfos(), 0); // percentage points
	for (int i = 0; i < GC.getMap().numPlots(); i++)
	{
		CvPlot* pLoopPlot = GC.getMap().plotByIndex(i);
		if (pLoopPlot->getTeam() == eTarget)
		{
			/*	note: There are ways of knowning that the team has resources even
				if the plot cannot be seen; so my handling of isRevealed is a bit ad-hoc. */
			BonusTypes eBonus = pLoopPlot->getNonObsoleteBonusType(getID());
			if (eBonus != NO_BONUS)
			{
				if (pLoopPlot->isRevealed(getID()) && AI_isPrimaryArea(pLoopPlot->getArea()))
					bonuses[eBonus] += bTotalWar ? 60 : 20;
				else bonuses[eBonus] += bTotalWar ? 20 : 0;
			}
		}
	}
	FOR_EACH_ENUM(Bonus)
	{
		if (bonuses[eLoopBonus] <= 0)
			continue;

		int iBonusValue = 0;
		int iMissing = 0;
		for (MemberAIIter it(getID()); it.hasNext(); ++it)
		{
			iBonusValue += it->AI_bonusVal(eLoopBonus, 0, true);
			if (it->getNumAvailableBonuses(eLoopBonus) == 0)
				iMissing++;
		}
		iBonusValue += GC.getInfo(eLoopBonus).getAIObjective(); // (support for mods.)
		iBonusValue = iBonusValue * getNumCities() *
				(std::min(100*iMissing, bonuses[eLoopBonus]) +
				std::max(0, bonuses[eLoopBonus] - 100*iMissing)/8) /
				std::max(1, 400 * getAliveCount());
		//
		iGainedValue += iBonusValue;
		// ignore denied value.
	}

	/*	magnify the gained value based on how many of the target's cities
		are in close areas */
	int iCloseCities = 0;
	for (std::set<int>::iterator it = close_areas.begin(); it != close_areas.end(); ++it)
	{
		CvArea* pLoopArea = GC.getMap().getArea(*it);
		if (AI_isPrimaryArea(*pLoopArea))
		{
			for (int i = 0; i < MAX_PLAYERS; i++)
			{
				const CvPlayerAI& kLoopPlayer = GET_PLAYER((PlayerTypes)i);
				if (kLoopPlayer.getTeam() == eTarget)
					iCloseCities += pLoopArea->getCitiesPerPlayer(kLoopPlayer.getID());
			}
		}
	}
	iGainedValue *= 75 + 50 * iCloseCities / std::max(1, kTargetTeam.getNumCities());
	iGainedValue /= 100;

	// amplify the gained value if we are aiming for a military victory
	if (AI_anyMemberAtVictoryStage(AI_VICTORY_MILITARY2))
		iGainedValue = iGainedValue * 4/3;

	// reduce the gained value based on how many other teams are at war with the target
	// similar to the way the target's strength estimate is reduced.
	iGainedValue *= 2;
	iGainedValue /= (isAtWar(eTarget) ? 1 : 2) + kTargetTeam.getNumWars(true, true);

	return iGainedValue + iDeniedValue;
}

/*  advc: Auxiliary function for AI_warCommitmentCost. Also addresses open issues
	with counting sibling vassals and vassals whose master has a DP with the target.
	(All only relevant when UWAI is disabled.) */
bool CvTeamAI::isFutureWarEnemy(TeamTypes eTeam, TeamTypes eTarget, bool bDefensivePacts) const
{
	CvTeam const& kEnemy = GET_TEAM(eTeam);
	TeamTypes eTargetMaster = GET_TEAM(eTarget).getMasterTeam();
	return (kEnemy.getMasterTeam() == eTargetMaster || isAtWar(kEnemy.getID()) ||
			(bDefensivePacts &&
			GET_TEAM(kEnemy.getMasterTeam()).isDefensivePact(eTargetMaster)));
}

int CvTeamAI::AI_warCommitmentCost(TeamTypes eTarget, WarPlanTypes eWarPlan,
	bool bConstCache) const // advc.001n
{
	PROFILE_FUNC();
	// Things to consider:
	//
	// risk of losing cities
	// relative unit strength
	// relative current power
	// productivity
	// war weariness
	// diplomacy
	// opportunity cost (need for expansion, research, etc.)

	/*	For most parts of the calculation, it is actually more important to
		consider the master of the target rather than the target itself.
		(this is important for defensive pacts; and it also affects
		relative power, relative productivity, and so on.) */
	TeamTypes eTargetMaster = GET_TEAM(eTarget).getMasterTeam();
	FAssert(eTargetMaster == eTarget || GET_TEAM(eTarget).isAVassal());

	const CvTeamAI& kTargetMasterTeam = GET_TEAM(eTargetMaster);

	bool const bTotalWar = (eWarPlan == WARPLAN_TOTAL || eWarPlan == WARPLAN_PREPARING_TOTAL);
	bool const bAttackWar = (bTotalWar ||
			(eWarPlan == WARPLAN_DOGPILE &&
			kTargetMasterTeam.getNumWars() + (isAtWar(eTarget) ? 0 : 1) > 1));
	bool const bPendingDoW = (!isAtWar(eTarget) &&
			eWarPlan != WARPLAN_ATTACKED && eWarPlan != WARPLAN_ATTACKED_RECENT);

	int iTotalCost = 0;

	// Estimate of military production costs
	{
		// Base commitment for a war of this type.
		int iCommitmentPerMil = bTotalWar ? 540 : 250;
		// this value will be added to iCommitmentPerMil at the end of the calculation.
		int const iBaseline = -25;

		// scale based on our current strength relative to our enemies.
		// cf. with code in AI_calculateAreaAIType
		{
			// whether to include vassals is a tricky issue...
			int iOurRelativeStrength = 100 * getPower(true) / (AI_countMilitaryWeight(0) + 20);
			/*	Sum the relative strength for all enemies, including existing wars
				and wars with civs attached to the target team. */
			int iEnemyRelativeStrength = 0;
			int iFreePowerBonus = GC.getInfo(GC.getGame().getBestLandUnit()).getPowerValue() * 2;
			for (TeamAIIter<MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> it(getID());
				it.hasNext(); ++it)
			{
				CvTeamAI const& kEnemy = *it;
				TeamTypes eEnemy = kEnemy.getID();
				/*	note: this still doesn't count vassal siblings. (ie. if the
					target is a vassal, this will not count the master's other vassals.)
					also, the vassals of defensive pact civs are
					currently not counted either. */
				if (isFutureWarEnemy(eEnemy, eTarget, bPendingDoW)) // advc: Will count sibling and DP vassals
				{
					/*	the + power is meant to account for the fact that the target
						may get stronger while we are planning for war -
						especially early in the game.
						use a slightly reduced value if we're actually not intending
						to attack this target. (full weight to all enemies in defensive wars) */
					int iWeight = (!bAttackWar || isAtWar(eEnemy) || eEnemy == eTarget ? 100 : 80);
					iEnemyRelativeStrength += iWeight *
							((isAtWar(eEnemy) ? 0 : iFreePowerBonus) + kEnemy.getPower(false)) /
							(((isAtWar(eEnemy) ? 1 : 2) +
							kEnemy.getNumWars(true, true))*kEnemy.AI_countMilitaryWeight(0)/2 + 20);
				}
			}
			//

			/*int iWarSuccessRating = (isAtWar(eTarget) ? AI_getWarSuccessRating() : 0);
			iCommitmentPerMil = iCommitmentPerMil * (100 * iEnemyRelativeStrength) / std::max(1, iOurRelativeStrength * (100+iWarSuccessRating/2));*/
			iCommitmentPerMil = iCommitmentPerMil * iEnemyRelativeStrength / std::max(1, iOurRelativeStrength);
		}

		// scale based on the relative size of our civilizations.
		// (note: this is separate from our total production, because I use it again a bit later.)
		int iOurProduction = AI_estimateTotalYieldRate(YIELD_PRODUCTION);
		{
			int iOurTotalProduction = iOurProduction * 100;
			int iEnemyTotalProduction = 0;
			const int iVassalFactor = 60; // only count some reduced percentage of vassal production.
			// Note: I've chosen not to count the production of the target's other enemies.

			// our team is already counted.
			for (TeamAIIter<ALIVE,VASSAL_OF> it(getID()); it.hasNext(); ++it)
				iOurTotalProduction += it->AI_estimateTotalYieldRate(YIELD_PRODUCTION) * iVassalFactor;

			for (TeamAIIter<MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> it(getID()); it.hasNext(); ++it)
			{
				CvTeamAI const& kEnemy = *it;
				// <advc.001> Revised so that vassals with DP are counted
				if (isFutureWarEnemy(kEnemy.getID(), eTarget, bPendingDoW))
				{
					iEnemyTotalProduction += kEnemy.AI_estimateTotalYieldRate(YIELD_PRODUCTION) *
							(kEnemy.isAVassal() ? iVassalFactor : 100);
				} // </advc.001>
			}

			iCommitmentPerMil *= 6 * iEnemyTotalProduction + iOurTotalProduction;
			iCommitmentPerMil /= std::max(1, iEnemyTotalProduction + 6 * iOurTotalProduction);
		}

		// scale based on the relative strengths of our units
		{
			int iEnemyUnit = std::max(30, kTargetMasterTeam.getTypicalUnitValue(NO_UNITAI, DOMAIN_LAND));
			int iOurAttackUnit = std::max(30, getTypicalUnitValue(UNITAI_ATTACK, DOMAIN_LAND));
			int iOurDefenceUnit = std::max(30, getTypicalUnitValue(UNITAI_CITY_DEFENSE, DOMAIN_LAND));
			int iHighScale = 30 + 70 * std::max(iOurAttackUnit, iOurDefenceUnit) / iEnemyUnit;
			int iLowScale = 10 + 90 * std::min(iOurAttackUnit, iOurDefenceUnit) / iEnemyUnit;

			iCommitmentPerMil = std::min(iCommitmentPerMil, 300) * 100 /
					iHighScale + std::max(0, iCommitmentPerMil - 300) * 100 / iLowScale;

			// Adjust for overseas wars
			if (!AI_hasSharedPrimaryArea(eTarget))
			{
				int iOurNavy = getTypicalUnitValue(NO_UNITAI, DOMAIN_SEA);
				// (using max here to avoid div-by-zero later on)
				int iEnemyNavy = std::max(1,
						kTargetMasterTeam.getTypicalUnitValue(NO_UNITAI, DOMAIN_SEA));

				// rescale (unused)
				/* {
					int x = std::max(2, iOurNavy + iEnemyNavy) / 2;
					iOurNavy = iOurNavy * 100 / x;
					iEnemyNavy = iEnemyNavy * 100 / x;
				} */

				// Note: Commitment cost is currently meant to take into account risk as well as resource requirements.
				// But with overseas wars, the relative strength of navy units effects these things differently.
				// If our navy is much stronger than theirs, then our risk is low but we still need to commit a
				// just as much resources to win the land-war for an invasion.
				// If their navy is stronger than ours, our risk is high and our resources will be higher too.
				//
				// The current calculations are too simplistic to explicitly specify all that stuff.
				if (bTotalWar)
				{
					//iCommitmentPerMil = iCommitmentPerMil * (4*iOurNavy + 5*iEnemyNavy) / (8*iOurNavy + 1*iEnemyNavy);
					//iCommitmentPerMil = iCommitmentPerMil * 200 / std::min(200, iLowScale + iHighScale);
					//
					iCommitmentPerMil = iCommitmentPerMil * 200 /
							std::min(240, (iLowScale + iHighScale) * (9*iOurNavy + 1*iEnemyNavy) / (6*iOurNavy + 4*iEnemyNavy));
				}
				else iCommitmentPerMil = iCommitmentPerMil * (1*iOurNavy + 4*iEnemyNavy) / (4*iOurNavy + 1*iEnemyNavy);
			}
		}

		// increase the cost for distant targets...
		if (0 == AI_teamCloseness(eTarget,
			DEFAULT_PLAYER_CLOSENESS, false, bConstCache)) // advc.001n
		{
			// ... in the early game.
			if (getNumCities() < GC.getInfo(GC.getMap().getWorldSize()).getTargetNumCities() * getAliveCount())
				iCommitmentPerMil = iCommitmentPerMil * 3/2;
			/* else
				iCommitmentPerMil = iCommitmentPerMil * 5/4; */

			// ... and for total war
			if (bTotalWar)
				iCommitmentPerMil = iCommitmentPerMil * 5/4;
		}

		iCommitmentPerMil += iBaseline; // The baseline should be a negative value which represents some amount of "free" commitment.

		if (iCommitmentPerMil > 0)
		{
			// iCommitmentPerMil will be multiplied by a rough estimate of the total resources this team could devote to war.
			int iCommitmentPool = iOurProduction * 3 + AI_estimateTotalYieldRate(YIELD_COMMERCE); // cf. AI_yieldWeight
			// Note: it would probably be good to take into account the expected increase in unit spending - but that's a bit tricky.

			// sometimes are resources are more in demand than other times...
			int iPoolMultiplier = 0;
			for (MemberAIIter it(getID()); it.hasNext(); ++it)
			{
				CvPlayerAI const& kMember = *it;
				iPoolMultiplier += 100;
				// increase value if we are still trying to expand peacefully. Now, the minimum site value is pretty arbitrary...
				// note, there's a small cap on the number of sites, around 3.
				int iSites = kMember.AI_getNumPrimaryAreaCitySites(kMember.AI_getMinFoundValue()*2);
				if (iSites > 0)
				{
					iPoolMultiplier += (50 + 50 * range(GC.getInfo(GC.getMap().getWorldSize()).getTargetNumCities() -
							kMember.getNumCities(), 0, iSites)) / (bTotalWar ? 2 : 1);
				}
			}
			iPoolMultiplier /= std::max(1, getAliveCount());
			iCommitmentPool = iCommitmentPool * iPoolMultiplier / 100;

			// Don't pick a fight if we're expecting to beat them to a peaceful victory.
			if (!AI_anyMemberAtVictoryStage(AI_VICTORY_MILITARY4))
			{
				if (AI_anyMemberAtVictoryStage(AI_VICTORY_CULTURE4) ||
					(AI_anyMemberAtVictoryStage(AI_VICTORY_SPACE4) &&
					!GET_TEAM(eTarget).AI_anyMemberAtVictoryStage(AI_VICTORY_CULTURE4 | AI_VICTORY_SPACE4)) ||
					(AI_getLowestVictoryCountdown() > 0 &&
					(GET_TEAM(eTarget).AI_getLowestVictoryCountdown() < 0 ||
					AI_getLowestVictoryCountdown() < GET_TEAM(eTarget).AI_getLowestVictoryCountdown())))
				{
					iCommitmentPool *= 2;
				}
			}

			iTotalCost += iCommitmentPerMil * iCommitmentPool / 1000;
		}
	}

	// war weariness
	int iTotalWW = 0;
	for (TeamIter<CIV_ALIVE,KNOWN_POTENTIAL_ENEMY_OF> it(getID()); it.hasNext(); ++it)
	{
		TeamTypes eEnemy = it->getID();
		// (advc: Or should current war enemies be counted here? The K-Mod code didn't.)
		if (isFutureWarEnemy(eEnemy, eTarget, bPendingDoW) && !isAtWar(eEnemy))
			iTotalWW += getWarWeariness(eEnemy, true) / 100;
	}
	// note: getWarWeariness has units of anger per 100,000 population, and it is customary to divide it by 100 immediately
	if (iTotalWW > 50)
	{
		int iS = isAtWar(eTarget) ? -1 : 1;
		int iWWCost = 0;
		for (MemberAIIter it(getID()); it.hasNext(); ++it)
		{
			CvPlayerAI const& kMember = *it;
			 // (ugly, I know. But that's just how it's done.)
			int iEstimatedPercentAnger = kMember.getModifiedWarWearinessPercentAnger(iWWCost) / 10;
			// note. Unfortunately, we haven't taken the effect of jails into account.
			iWWCost += iS * kMember.getNumCities() * kMember.AI_getHappinessWeight(iS * iEstimatedPercentAnger *
					(100 + kMember.getWarWearinessModifier()) / 100, 0, true) / 20;
		}
		iTotalCost += iWWCost;
	}

	// doc: avoid birth protected
	if (GET_PLAYER(getLeaderID()).isBirthProtected())
		iTotalCost *= 4;

	return iTotalCost;
}

/*	diplomatic costs for declaring war (somewhat arbitrary -
	to encourage the AI to attack its enemies, and the enemies of its friends.) */
int CvTeamAI::AI_warDiplomacyCost(TeamTypes eTarget) const
{
	if (isAtWar(eTarget))
	{
		//FErrorMsg("AI_warDiplomacyCost called when already at war."); // sometimes we call this function for debug purposes.
		return 0;
	}

	if (AI_anyMemberAtVictoryStage(AI_VICTORY_CONQUEST4))
		return 0;

	const CvTeamAI& kTargetTeam = GET_TEAM(eTarget);

	// first, the cost of upsetting the team we are declaring war on.
	int iDiploPopulation = kTargetTeam.getTotalPopulation(false);
	int iDiploCost = 3 * iDiploPopulation * (100 + AI_getAttitudeWeight(eTarget)) / 200;

	// cost of upsetting their friends
	// advc: Loop over players so that AI_disapprovesOfDoW can be used
	for (PlayerAIIter<MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> it(getID()); it.hasNext(); ++it)
	{
		CvPlayerAI const& kLoopPlayer = *it;
		TeamTypes eLoopTeam = kLoopPlayer.getTeam();
		if (eLoopTeam == eTarget || !kTargetTeam.isHasMet(eLoopTeam) ||
				GET_TEAM(eLoopTeam).isCapitulated())
			continue;

		int iPop = kLoopPlayer.getTotalPopulation();
		//iDiploPopulation += iPop; // advc: commented out; value never read
		if (kLoopPlayer.AI_disapprovesOfDoW(getID(), GET_TEAM(eTarget).getMasterTeam()) &&
			AI_getAttitude(eLoopTeam) >= ATTITUDE_PLEASED)
		//if (kLoopTeam.AI_getAttitude(eTarget) >= ATTITUDE_PLEASED && AI_getAttitude(i) >= ATTITUDE_PLEASED)
		{
			iDiploCost += iPop * (100 + AI_getAttitudeWeight(eLoopTeam)) / 200;
		}
		else if (kTargetTeam.isAtWar(eLoopTeam))
		{
			iDiploCost -= iPop * (100 + AI_getAttitudeWeight(eLoopTeam)) / 400;
		}
	}

	// scale the diplo cost based the personality of the team.
	{
		int iPeaceWeight = 0;
		for (MemberAIIter it(getID()); it.hasNext(); ++it)
			iPeaceWeight += it->AI_getPeaceWeight(); // usually between 0-10.

		int iDiploWeight = 40;
		iDiploWeight += 10 * iPeaceWeight / getAliveCount();
		// This puts iDiploWeight somewhere around 50 - 250.
		if (GC.getGame().isOption(GAMEOPTION_AGGRESSIVE_AI))
			iDiploWeight /= 2;
		if (AI_anyMemberAtVictoryStage(AI_VICTORY_DIPLOMACY3))
			iDiploWeight += 50;
		if (AI_anyMemberAtVictoryStage(AI_VICTORY_DIPLOMACY4))
			iDiploWeight += 50;
		if (AI_anyMemberAtVictoryStage(AI_VICTORY_CONQUEST3)) // note: conquest4 ignores diplo completely.
			iDiploWeight /= 2;

		iDiploCost *= iDiploWeight;
		iDiploCost /= 100;
	}

	// Finally, reduce the value for large maps;
	// so that this diplomacy stuff doesn't become huge relative to other parts of the war evaluation.
	iDiploCost *= 3;
	iDiploCost /= std::max(5,
			GC.getGame().getRecommendedPlayers() // advc.137
			//GC.getInfo((WorldSizeTypes)GC.getMap().getWorldSize()).getDefaultPlayers()
		);

	return iDiploCost;
}
// K-Mod end.

/*  Relative value of starting a war against eTeam.
	This function computes the value of starting a war against eTeam.
	The returned value should be compared against other possible targets
	to pick the best target. */ // advc.104: UWAI bypasses this function
// K-Mod: Complete remake of the function.
int CvTeamAI::AI_startWarVal(TeamTypes eTarget, WarPlanTypes eWarPlan,
	bool bConstCache) const // advc.001n
{
	PROFILE_FUNC(); // advc.opt
	TeamTypes eTargetMaster = GET_TEAM(eTarget).getMasterTeam(); // we need this for checking defensive pacts.
	bool bPendingDoW = !isAtWar(eTarget) && eWarPlan != WARPLAN_ATTACKED && eWarPlan != WARPLAN_ATTACKED_RECENT;
	/*  advc.001n: These subroutines call the (cached) AI closeness funtions.
		Pass along bConstCache. */
	int iTotalValue = AI_warSpoilsValue(eTarget, eWarPlan, bConstCache) -
			AI_warCommitmentCost(eTarget, eWarPlan, bConstCache) -
			(bPendingDoW ? AI_warDiplomacyCost(eTarget) : 0);

	// Call AI_warSpoilsValue for each additional enemy team involved in this war.
	// NOTE: a single call to AI_warCommitmentCost should include the cost of fighting all of these enemies.
	for (TeamIter<MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> it(getID()); it.hasNext(); ++it)
	{
		CvTeam const& kEnemy = *it;
		if (kEnemy.getID() == eTarget || kEnemy.isAtWar(getID()))
			continue; // advc (comment): only _additional_ enemies

		TeamTypes eEnemyMaster = kEnemy.getMasterTeam();
		if (eEnemyMaster == eTargetMaster)
		{
			iTotalValue += AI_warSpoilsValue(kEnemy.getID(), WARPLAN_DOGPILE, /* advc.001n: */ bConstCache)
					- (bPendingDoW ? AI_warDiplomacyCost(kEnemy.getID()) : 0);
		}
		// advc.001: Count vassals with a DP
		else if (bPendingDoW && GET_TEAM(eEnemyMaster).isDefensivePact(eTargetMaster))
		{
			FAssert(!isAtWar(eTarget));
			// note: no diplo cost for this b/c it isn't us declaring war.
			iTotalValue += AI_warSpoilsValue(kEnemy.getID(), WARPLAN_ATTACKED, /* advc.001n: */ bConstCache);
		}
	}
	return iTotalValue;
}


int CvTeamAI::AI_endWarVal(TeamTypes eTeam) const // XXX this should consider area power...
{
	FAssert(eTeam != getID());
	FAssert(isAtWar(eTeam));

	CvTeamAI const& kWarTeam = GET_TEAM(eTeam); // K-Mod

	int iValue = 100;
	iValue += getNumCities() * 3;
	iValue += kWarTeam.getNumCities() * 3;
	iValue += getTotalPopulation();
	iValue += kWarTeam.getTotalPopulation();
	iValue += (kWarTeam.AI_getWarSuccess(getID()) * 20).uround();

	int const iOurPower = std::max(1, getPower(true));
	int const iTheirPower = std::max(1, kWarTeam.getDefensivePower(getID()));
	{	// <kekm.39> Multiplying by iTheirPower can overflow
		scaled rPowMult(iTheirPower + 10, iOurPower + iTheirPower + 10);
		iValue = (iValue * rPowMult).uround(); // </kekm.39>
	}
	WarPlanTypes const eWarPlan = AI_getWarPlan(eTeam);
	/*	if we are not human, do we want to continue war for strategic reasons?
		only check if our power is at least 120% of theirs */
	if (!isHuman() && iOurPower > 120 * iTheirPower / 100)
	{
		bool bDagger = false;
		bool bAnyFinancialTrouble = false;
		for (MemberAIIter it(getID()); it.hasNext(); ++it)
		{
			CvPlayerAI const& kMember = *it;
			if (kMember.AI_isDoStrategy(AI_STRATEGY_DAGGER))
				bDagger = true;
			if (kMember.AI_isFinancialTrouble())
				bAnyFinancialTrouble = true;
		}
		if (bDagger)
		{
			iValue *= 9 * iTheirPower;
			iValue /= 10 * iOurPower;
		}

		/*	for now, we will always do the land mass check for domination
			if we have more than half the land, then value peace at 90% * land ratio */
		int iLandRatio = getTotalLand(true) * 100 / std::max(1, kWarTeam.getTotalLand(true));
		if (iLandRatio > 120)
		{
			iValue *= 9 * 100;
			iValue /= 10 * iLandRatio;
		}

		// if in financial trouble, warmongers will continue the fight to make more money
		if (bAnyFinancialTrouble)
		{
			switch (eWarPlan)
			{
				case WARPLAN_TOTAL:
					// if we total warmonger, value peace at 70% * power ratio factor
					if (bDagger || AI_maxWarRand() < 100)
					{
						iValue *= 7 * (5 * iTheirPower);
						iValue /= 10 * (iOurPower + (4 * iTheirPower));
					}
					break;

				case WARPLAN_LIMITED:
					// if we limited warmonger, value peace at 70% * power ratio factor
					if (AI_limitedWarRand() < 100)
					{
						iValue *= 7 * (5 * iTheirPower);
						iValue /= 10 * (iOurPower + (4 * iTheirPower));
					}
					break;

				case WARPLAN_DOGPILE:
					// if we dogpile warmonger, value peace at 70% * power ratio factor
					if (AI_dogpileWarRand() < 100)
					{
						iValue *= 7 * (5 * iTheirPower);
						iValue /= 10 * (iOurPower + (4 * iTheirPower));
					}
					break;

			}
		}
	}

	// BETTER_BTS_AI_MOD, War strategy AI, Victory Strategy AI, 05/19/10, jdog5000: START
	/* BBAI code
	if (AI_anyMemberAtVictoryStage(AI_VICTORY_CULTURE4))
		iValue *= 4;
	else if (AI_anyMemberAtVictoryStage(AI_VICTORY_CULTURE3) || AI_anyMemberAtVictoryStage(AI_VICTORY_SPACE4))
		iValue *= 2;*/
	// K-Mod
	if (AI_anyMemberAtVictoryStage(AI_VICTORY_CULTURE4))
		iValue *= 3;
	else if (AI_anyMemberAtVictoryStage(AI_VICTORY_SPACE4))
		iValue *= 2;
	else if (AI_anyMemberAtVictoryStage(AI_VICTORY_CULTURE3 | AI_VICTORY_SPACE3))
	{
		iValue *= 4;
		iValue /= 3;
	} // K-Mod end

	if ((!isHuman() && eWarPlan == WARPLAN_TOTAL) ||
		(!kWarTeam.isHuman() && kWarTeam.AI_getWarPlan(getID()) == WARPLAN_TOTAL))
	{
		iValue *= 2;
	}
	else if ((!isHuman() && eWarPlan == WARPLAN_DOGPILE && kWarTeam.getNumWars() > 1) ||
		(!kWarTeam.isHuman() &&
		kWarTeam.AI_getWarPlan(getID()) == WARPLAN_DOGPILE && getNumWars() > 1))
	{
		iValue *= 3;
		iValue /= 2;
	}

	// Do we have a big stack en route?
	int iOurAttackers = 0;
	for (MemberAIIter it(getID()); it.hasNext(); ++it)
		iOurAttackers += it->AI_enemyTargetMissions(eTeam);
	int iTheirAttackers = 0;
	FOR_EACH_AREA(pLoopArea)
		iTheirAttackers += AI_countEnemyDangerByArea(*pLoopArea, eTeam);

	int iAttackerRatio = (100 * iOurAttackers) /
			std::max(1 + GC.getGame().getCurrentEra(), iTheirAttackers);

	if (GC.getGame().isOption(GAMEOPTION_AGGRESSIVE_AI))
	{
		iValue *= 150;
		iValue /= range(iAttackerRatio, 150, 900);
	}
	else
	{
		iValue *= 200;
		iValue /= range(iAttackerRatio, 200, 600);
	}
	// BETTER_BTS_AI_MOD: END
	return AI_roundTradeVal(iValue);
}

/*	K-Mod: This is the tech value modifier for devaluing techs that are
	known by other civs. Based on BtS code from AI_techTradeVal. */
scaled CvTeamAI::AI_knownTechValModifier(TechTypes eTech) const
{
	int iTechCivs = 0;
	int iCivsMet = 0;
	// advc (note): Minor civs not excluded; perhaps should be.
	for (TeamIter<CIV_ALIVE,OTHER_KNOWN_TO> it(getID()); it.hasNext(); ++it)
	{
		CvTeam const& kOther = *it;
		if (kOther.isHasTech(eTech) /* advc.551: */ && !kOther.isCapitulated())
			iTechCivs++;
		iCivsMet++;
	}
	//return 50 * (iCivsMet - iTechCivs) / std::max(1, iCivsMet);
	// <advc.551>
	scaled r(iCivsMet - iTechCivs, std::max(1, iCivsMet));
	// doc: keep full impact
	//scaled const rMax = fixp(1/3.); // Lower impact than the 50% in BtS/K-Mod
	//r *= rMax;
	/*	Decrease modifier below 100% if more than half know the tech? No -
		generally, 1 research point should have a trade value greater than 1. */
	//r -= rMax / 2;
	// (In K-Mod, the caller had added 1.)

	// doc: Hermitage effect
	if (GET_PLAYER(getLeaderID()).isHasBuildingEffect(HERMITAGE))
		r *= fixp(3/4.);

	return 1 + r; // </advc.551>
}

// advc (comment): How much this CvTeam is willing to pay to eFromTeam for eTech
int CvTeamAI::AI_techTradeVal(TechTypes eTech, TeamTypes eFromTeam,
	bool bIgnoreDiscount, // advc.550a
	bool bPeaceDeal) const // advc.140h
{
	PROFILE_FUNC(); // advc.550: Still seems completely harmless wrt. performance
	FAssert(eFromTeam != getID());

	CvTechInfo const& kTech = GC.getInfo(eTech);
	scaled rValue = (fixp(0.25) + // advc.551: was 0.5
			/*	K-Mod. Standardized the modifier for # of teams with the tech;
				and removed the effect of team size. */
			AI_knownTechValModifier(eTech)) *
			/*	advc.551, advc.001: Revert the 2nd part of the K-Mod change.
				A correct implementation would have to take the team size modifier
				out of the research progress; but I think it'd still be a bad idea.*/
			std::max(0, getResearchCost(eTech/*, ..., false*/) -
			getResearchProgress(eTech)); // K-Mod end
	/*  <advc.104h> Peace for tech isn't that attractive for the receiving side
		b/c they could continue the war and still get the tech when making peace
		later on. Doesn't work the same way with gold b/c the losing side may well
		spend the gold if the war continues */
	if(bPeaceDeal)
		rValue *= fixp(0.7); // </advc.104h>
	rValue *= scaled::max(0, 1 + per100(kTech.getAITradeModifier()));
	// <advc.550a>
	if(!bIgnoreDiscount &&  // No discounts for vassals:
		!isVassal(eFromTeam) && !GET_TEAM(eFromTeam).isVassal(getID()))
	{	/*  If they're more advanced/powerful, they shouldn't mind giving us
			a tech, so we lower our tech value, assuming/hoping that we'll be
			able to get it cheap.
			Handle this here instead of CvPlayer::AI_tradeAcceptabilityThreshold
			b/c tech is shared rather than given away. Giving away e.g. gold is bad
			even if we don't think the other side is a threat. */
		scaled rPowRatio(getPower(true),
				std::max(1, GET_TEAM(eFromTeam).getPower(true)));
		/*  Don't use CvTeam::getBestKnownTechScorePercent b/c that's based on
			the teams that the callee has met. This team shouldn't have that info
			about eTeam. */
		scaled rTechRatio(GET_PLAYER(getLeaderID()).getTechScore(),
				/*	(Scores are computed per player, but the tech score is actually
					the same for all members of a team.) */
				std::max(1, GET_PLAYER(GET_TEAM(eFromTeam).getLeaderID()).getTechScore()));
		CvGame const& kGame = GC.getGame();
		scaled rGameProgress(kGame.getGameTurn() - kGame.getStartTurn(),
				std::max(1, kGame.getEstimateEndTurn() - kGame.getStartTurn()));
		// Too big a discount too early this way? Let's try this:
		if (rGameProgress.isPositive())
			rGameProgress = 1 / (1 + 1 / rGameProgress);
		rGameProgress.clamp(0, fixp(0.5));
		rPowRatio.clamp(1 - rGameProgress, 1 + rGameProgress);
		rTechRatio.clamp(1 - rGameProgress, 1 + rGameProgress);
		// Powerful civs shouldn't grant large discounts to advanced civs
		if(rTechRatio < 1 && rPowRatio > 1)
		{
			rPowRatio *= SQR(rTechRatio);
			rPowRatio.increaseTo(1);
		}
		else if(rTechRatio > 1 && rPowRatio < 1)
		{
			rPowRatio *= SQR(rTechRatio);
			rPowRatio.decreaseTo(1);
		}
		scaled rDiscountModifier = (rPowRatio + 2 * rTechRatio) / 3;
		/*  Not sure about this guard: Should weak civs charge more for their techs?
			In tech-vs-tech trades, the modifier would then take effect twice,
			resulting in one side demanding up to twice as much as the other;
			too much I think. */
		if(rDiscountModifier < 1)
			rValue *= rDiscountModifier;
	} // </advc.550a>
	// <advc.550g>
	if (!isHuman()) // Don't let the AI gauge the human tech value
	{
		scaled rTeamRank;
		int iValidMembers = 0;
		for (MemberAIIter itMember(getID()); itMember.hasNext(); ++itMember)
		{
			/*	Unfortunately, these ranks are biased toward cheap techs.
				Still better than nothing (perhaps). */
			scaled rRank = itMember->AI_getTechRank(eTech);
			if (!rRank.isNegative())
			{
				rTeamRank += rRank;
				iValidMembers++;
			}
		}
		if (iValidMembers > 0)
		{
			rTeamRank /= iValidMembers;
			FAssert(!rTeamRank.isNegative() && rTeamRank <= 1);
			scaled rModifier = 1;
			if (rTeamRank < scaled(1, 2))
			{	// Add at most 0.275
				rModifier += (11 * rTeamRank) / 20;
			}
			else if (rTeamRank > scaled(1, 2))
			{	// Subtract at most 5/12
				rModifier -= (5 * (rTeamRank - scaled(1, 2))) / 6;
			}
			rValue *= rModifier;
		}
	} // </advc.550g>
	return AI_roundTradeVal(rValue.round());
}


DenialTypes CvTeamAI::AI_techTrade(TechTypes eTech, TeamTypes eToTeam) const
{
	//PROFILE_FUNC(); // advc.003o

	FAssertMsg(eToTeam != getID(), "shouldn't call this function on ourselves");
	// advc.550e: No longer needed
	//if (GC.getGame().isOption(GAMEOPTION_NO_TECH_BROKERING)) { ... }

	if(isHuman() /*|| isVassal(eToTeam)*/ || isAtWar(eToTeam)) // rfc: no free vassal trade
		return NO_DENIAL; // advc

	if (AI_getWorstEnemy() == eToTeam)
		return DENIAL_WORST_ENEMY;

	AttitudeTypes eAttitude = AI_getAttitude(eToTeam);

	for (MemberIter it(getID()); it.hasNext(); ++it)
	{
		if (eAttitude <= GC.getInfo(it->getPersonalityType()).getTechRefuseAttitudeThreshold())
			return DENIAL_ATTITUDE;
	}

	if (eAttitude < ATTITUDE_FRIENDLY)
	{
		// doc: use tech rank, increase threshold to 2/3, use current teams alive
		//if ((GC.getGame().getTeamRank(getID()) < (GC.getGame().getCivTeamsEverAlive() / 2)) ||
		//(GC.getGame().getTeamRank(eToTeam) < (GC.getGame().getCivTeamsEverAlive() / 2)))
		if (GC.getGame().getTechRank(eToTeam) < GC.getGame().countCivTeamsAlive() * 2 / 3)
		{
			int iNoTechTradeThreshold = AI_noTechTradeThreshold();

			iNoTechTradeThreshold *= std::max(0, GC.getInfo(GET_TEAM(eToTeam).getHandicapType()).
					getNoTechTradeModifier() + 100);
			iNoTechTradeThreshold /= 100;

			if (AI_getMemoryCount(eToTeam, MEMORY_RECEIVED_TECH_FROM_ANY) > iNoTechTradeThreshold)
				return DENIAL_TECH_WHORE;
		}
	// K-Mod. Generic tech trade test
	}
	if (eTech == NO_TECH)
		return NO_DENIAL;

	if (eAttitude < ATTITUDE_FRIENDLY)
	{
	// K-Mod end
		int iKnownCount = 0;
		int iPossibleKnownCount = 0;
		int iNotMet = 0; // advc.550c
		// advc.550c: Exclude minor civs (b/c they can't be traded with)
		for (TeamIter<MAJOR_CIV> it; it.hasNext(); ++it)
		{
			CvTeam const& kOther = *it;
			if (kOther.getID() == getID() || kOther.getID() == eToTeam)
				continue;
			if (isHasMet(kOther.getID()))
			{
				if (kOther.isHasTech(eTech))
					iKnownCount++;
				iPossibleKnownCount++;
			}
			else iNotMet++; // advc.550c
		}

		int iTechTradeKnownPercent = AI_techTradeKnownPercent();
		/*  <advc.550c>
			Don't want the threshold to change everytime this function is called.
			Therefore, can't use a random number. Just hashing eTech would lead
			to the same per-tech adjustment each game. Hash in the position of our
			leader's capital, which is different every game, but doesn't change
			from turn to turn. */
		// Between -15 and +15; put it in a variable only for debugging.
		int iRandomAdjustment = (scaled::hash(eTech, getLeaderID()) * 30 - 15).round();
		iTechTradeKnownPercent += iRandomAdjustment;
		// </advc.550c>

		iTechTradeKnownPercent *= std::max(0, GC.getInfo(GET_TEAM(eToTeam).
				getHandicapType()).getTechTradeKnownModifier() + 100);
		iTechTradeKnownPercent /= 100;

		iTechTradeKnownPercent *= AI_getTechMonopolyValue(eTech, eToTeam);
		iTechTradeKnownPercent /= 100;

		// <advc.550c>
		int iKnownPercent = (iPossibleKnownCount == 0 ? 0 :
				(iKnownCount * 100) / iPossibleKnownCount);
		// No functional change so far
		/*  Make AI more willing to trade if it hasn't met most teams yet,
			especially if it has met just one or two. */
		if(iNotMet > iPossibleKnownCount)
		{
			iKnownPercent = std::max(iKnownPercent,
					/*  If just one team to trade with, that's 40%;
						two teams (neither knowing eTech): 28.6%. */
					(100 / (iPossibleKnownCount + fixp(1.5))).round());
		}
		if(iKnownPercent < iTechTradeKnownPercent) // No functional change
		// </advc.550c>
		{
			return DENIAL_TECH_MONOPOLY;
		}
	}
	FOR_EACH_ENUM(Unit)
	{
		if (!GC.getInfo(eLoopUnit).isTechRequired(eTech))
			continue;
		if (GC.getInfo(eLoopUnit).isWorldUnit() &&
			getUnitClassMaking(GC.getInfo(eLoopUnit).getUnitClassType()) > 0)
		{
			return DENIAL_MYSTERY;
		}
	}
	FOR_EACH_ENUM(Building)
	{
		if (!GC.getInfo(eLoopBuilding).isTechRequired(eTech))
			continue;
		if (GC.getInfo(eLoopBuilding).isWorldWonder() &&
			getBuildingClassMaking(GC.getInfo(eLoopBuilding).getBuildingClassType()) > 0)
		{
			return DENIAL_MYSTERY;
		}
	}
	FOR_EACH_ENUM(Project)
	{
		CvProjectInfo const& kLoopProject = GC.getInfo(eLoopProject);
		if (kLoopProject.getTechPrereq() != eTech)
			continue;
		if (kLoopProject.isWorldProject() && getProjectMaking(eLoopProject) > 0)
			return DENIAL_MYSTERY;
		FOR_EACH_NON_DEFAULT_KEY(kLoopProject.getVictoryThreshold(), Victory)
		{
			if (GC.getGame().isVictoryValid(eLoopVictory))
				return DENIAL_VICTORY;
		}
	}
	return NO_DENIAL;
}

// advc (comment): How much this CvTeam is willing to pay to eFromTeam for its map
int CvTeamAI::AI_mapTradeVal(TeamTypes eFromTeam) const
{
	FAssertMsg(eFromTeam != getID(), "shouldn't call this function on ourselves");

	int iValue = 0;
	CvMap const& kMap = GC.getMap();
	for (int iI = 0; iI < kMap.numPlots(); iI++)
	{
		CvPlot const& kPlot = kMap.getPlotByIndex(iI);
		if (!kPlot.isRevealed(getID(), false) && kPlot.isRevealed(eFromTeam))
		{
			if (kPlot.isWater())
				iValue++;
			else iValue += 5;
		}
	}

	//iValue /= 10;
	iValue /= 25; // doc: make maps less valuable
	// <advc.136a>
	if(AI_isPursuingCircumnavigation())
		iValue *= 2; // </advc.136a>

	if (GET_TEAM(eFromTeam).isVassal(getID()))
		iValue /= 2;

	return AI_roundTradeVal(iValue);
}


DenialTypes CvTeamAI::AI_mapTrade(TeamTypes eToTeam) const
{
	//PROFILE_FUNC(); // advc.003o
	FAssertMsg(eToTeam != getID(), "shouldn't call this function on ourselves");

	if (isHuman() || isVassal(eToTeam) || isAtWar(eToTeam))
		return NO_DENIAL;

	if (AI_getWorstEnemy() == eToTeam)
		return DENIAL_WORST_ENEMY;

	AttitudeTypes eOurAttitude = AI_getAttitude(eToTeam);
	for (MemberIter it(getID()); it.hasNext(); ++it)
	{
		if (eOurAttitude <= GC.getInfo(it->getPersonalityType()).
			getMapRefuseAttitudeThreshold())
		{
			return DENIAL_ATTITUDE;
		}
	}
	// <advc.136a>
	if(AI_isPursuingCircumnavigation())
		return DENIAL_MYSTERY; // </advc.136a>

	return NO_DENIAL;
}


int CvTeamAI::AI_vassalTradeVal(TeamTypes eTeam) const
{
	return AI_surrenderTradeVal(eTeam);
}

/*  advc: Refactored. In BtS/K-Mod, the ...NOT_POSSIBLE_YOU answers
	took precedence over ...NOT_POSSIBLE_US and DENIAL_ATTITUDE came last.
	The code is easier to read without these constraints, and I don't really
	think it matters. */
DenialTypes CvTeamAI::AI_vassalTrade(TeamTypes eMasterTeam) const
{
	FAssert(eMasterTeam != getID());
	FAssertMsg(!isAtWar(eMasterTeam), "Shouldn't consider capitulation here");
	FAssertMsg(!isAVassal(), "Shouldn't consider cancellation here");

	CvTeamAI& kMasterTeam = GET_TEAM(eMasterTeam);
	bool bMasterNeedsToDeclareWar = false; // advc.104o
	// Master refuses on account of vassal's enemies
	for (TeamIter<FREE_MAJOR_CIV,ENEMY_OF> it(getID()); it.hasNext(); ++it)
	{
		CvTeam& kEnemy = *it;
		if (kEnemy.isAtWar(eMasterTeam))
			continue;
		TeamTypes eEnemy = kEnemy.getID();
		if (kMasterTeam.isForcePeace(eEnemy) ||
			!kMasterTeam.canChangeWarPeace(eEnemy) ||
			!kMasterTeam.isHasMet(eEnemy)) // advc.112
		{
			return DENIAL_WAR_NOT_POSSIBLE_YOU;
		}
		if (!kMasterTeam.isHuman() && /* advc.104o: */ !getUWAI().isEnabled())
		{
			DenialTypes eWarDenial = kMasterTeam.AI_declareWarTrade(eEnemy, getID(), true);
			if (eWarDenial != NO_DENIAL)
				return DENIAL_WAR_NOT_POSSIBLE_YOU;
		}
		/*  K-Mod. New rule: AI civs won't accept a vassal if it would
			mean joining a war they would never otherwise join.
			Note: the denial actually comes from kMasterTeam, not this team. */
		if (kMasterTeam.AI_refuseWar(kEnemy.getID()))
			return DENIAL_ATTITUDE_THEM;
		/*  (K-Mod: if we're concerned about AI_startWarVal, then that should be checked
			in the trade value part; not the trade denial part.) */
		/*  ^advc.104o: Letting the vassal pay to be accepted doesn't make sense to me.
			The master will mostly get everything from the vassal anyway.
			I.e. the master should decide on its own whether a vassal is worth a war.
			Will do that after all other checks - to avoid polluting the UWAI report. */
		bMasterNeedsToDeclareWar = true;
	}
	// Vassal refuses on account of master's enemies
	for (TeamIter<FREE_MAJOR_CIV,ENEMY_OF> it(eMasterTeam); it.hasNext(); ++it)
	{
		CvTeam& kEnemy = *it;
		if (kEnemy.isAtWar(getID()))
			continue;
		TeamTypes eEnemy = kEnemy.getID();
		if (!kMasterTeam.canChangeWarPeace(eEnemy))
			return DENIAL_PEACE_NOT_POSSIBLE_YOU;
		if (!kMasterTeam.isHuman())
		{
			DenialTypes ePeaceDenial = kMasterTeam.AI_makePeaceTrade(eEnemy, getID());
			if (ePeaceDenial != NO_DENIAL)
				return DENIAL_PEACE_NOT_POSSIBLE_YOU;
		}
		if (isForcePeace(eEnemy) || !canChangeWarPeace(eEnemy))
			return DENIAL_WAR_NOT_POSSIBLE_US;
	}
	// <advc.143>
	if (AI_getMemoryCount(eMasterTeam, MEMORY_CANCELLED_VASSAL_AGREEMENT) > 0 ||
		kMasterTeam.AI_getMemoryCount(getID(), MEMORY_CANCELLED_VASSAL_AGREEMENT) > 0)
	{
		return DENIAL_RECENT_CANCEL;
	} // </advc.143>
	// <advc.112> Master refuses if vassal too insignificant
	if (!kMasterTeam.isHuman() &&
		!kMasterTeam.AI_anyMemberAtVictoryStage(AI_VICTORY_CONQUEST2) &&
		kMasterTeam.getTotalPopulation() > 6 * getTotalPopulation())
	{
		int iAttitudeThresh = ATTITUDE_FRIENDLY;
		/*  Those that don't start wars when Pleased are "nice" leaders that will
			protect a small vassal at Pleased */
		if(GC.getInfo(GET_PLAYER(kMasterTeam.getLeaderID()).
				getPersonalityType()).getNoWarAttitudeProb(ATTITUDE_PLEASED) >= 100)
			iAttitudeThresh = ATTITUDE_PLEASED;
		if(kMasterTeam.AI_getAttitude(getID()) < iAttitudeThresh)
			return DENIAL_POWER_US;
	} // </advc.112>
	DenialTypes eDenial = AI_surrenderTrade(eMasterTeam);
	if (eDenial != NO_DENIAL)
		return eDenial;
	// <advc.104o>
	if (getUWAI().isEnabled() && bMasterNeedsToDeclareWar && !kMasterTeam.isHuman())
		return kMasterTeam.uwai().acceptVassal(getID()); // </advc.104o>
	return NO_DENIAL;
}


int CvTeamAI::AI_surrenderTradeVal(TeamTypes eTeam) const
{
	FAssert(eTeam != getID());
	return 0;
}

/*  advc (note): This function is called for both voluntary vassal agreements and capitulation.
	In the latter case, this team and eMasterTeam will be at war.
	It's also called when considering to cancel a vassal agreement. */
DenialTypes CvTeamAI::AI_surrenderTrade(TeamTypes eMasterTeam, int iPowerMultiplier,
	bool bCheckAccept) const // advc.104o
{
	//PROFILE_FUNC(); // advc.003o (Not called often and tends to return early)

	FAssert(eMasterTeam != getID());

	CvTeamAI const& kMasterTeam = GET_TEAM(eMasterTeam);
	bool const bWar = isAtWar(eMasterTeam);
	/*  <advc.112> Colonies are more loyal than other peace vassals, but not more
		likely to come back once broken away (isVassal is checked). */
	bool const bColony = (isVassal(eMasterTeam) &&
	!isCapitulated() && kMasterTeam.isParent(getID())); // </advc.112>

	// doc: no vassals that recently spawned
	if (GC.getGame().getGameTurn() < GET_PLAYER(getLeaderID()).getLastBirthTurn() + getTurns(10))
		return DENIAL_NO_GAIN;

	// doc: no vassals if either of them is birth protected
	if (GET_PLAYER(getLeaderID()).isBirthProtected())
		return DENIAL_POWER_US;
	if (GET_PLAYER(kMasterTeam.getLeaderID()).isBirthProtected())
		return DENIAL_NO_GAIN;

	// doc: no vassals that are expansion targets for anyone
	FOR_EACH_CITY(pLoopCity, GET_PLAYER(getLeaderID()))
	{
		PlayerTypes eExpansionPlayer = pLoopCity->plot()->getExpansion();
		if (eExpansionPlayer != NO_PLAYER)
		{
			if (eExpansionPlayer == kMasterTeam.getLeaderID())
				return DENIAL_PEACE_NOT_POSSIBLE_YOU;
			if (!isAtWar(GET_PLAYER(eExpansionPlayer).getTeam()))
				return DENIAL_POWER_YOUR_ENEMIES;
		}
	}

	/*	K-Mod. I've disabled the denial for "war not possible"
		In K-Mod, surrendering overrules existing peace treaties -
		just like defensive pacts overrule peace treaties.
		For voluntary vassals, the treaties still apply. [advc: see AI_vassalTrade]
		K-Mod. However, "peace not possible" should still be checked here --
		but only if this is a not a peace-vassal deal! */
	if (bWar)
	{
		for (TeamIter<FREE_MAJOR_CIV,ENEMY_OF> it(getID()); it.hasNext(); ++it)
		{
			TeamTypes const eEnemy = it->getID();
			if (eEnemy == eMasterTeam || kMasterTeam.isAtWar(eEnemy))
				continue;
			if (!canChangeWarPeace(eEnemy))
				return DENIAL_PEACE_NOT_POSSIBLE_US;
		}
	} // K-Mod end
	// BETTER_BTS_AI_MOD (12/07/09,  jdog5000, Diplomacy);
	if (isHuman() && kMasterTeam.isHuman())
		return NO_DENIAL; // BETTER_BTS_AI_MOD: END
	// <advc.112>
	if(AI_anyMemberAtVictoryStage3())
		return DENIAL_VICTORY;
	FOR_EACH_ENUM(VoteSource)
	{
		// (Doesn't imply stage 3 of diplo victory)
		if(GC.getGame().getSecretaryGeneral(eLoopVoteSource) == getID())
			return DENIAL_VICTORY;
	}  // <advc>
	CvGame const& kGame = GC.getGame();
	AttitudeTypes const eTowardMaster = AI_getAttitude(eMasterTeam, false); // </advc>
	if(isVassal(eMasterTeam) && eTowardMaster >= ATTITUDE_PLEASED)
	{
		// Moved up // </advc.112>
		FOR_EACH_ENUM(Victory) // advc: Refactored
		{
			bool bPopulationThreat = true;
			if(kGame.getAdjustedPopulationPercent(eLoopVictory) > 0)
			{
				bPopulationThreat = false;
				int iThreshold = kGame.getTotalPopulation() *
						kGame.getAdjustedPopulationPercent(eLoopVictory);
				// advc.112: The DENIAL_VICTORY check above should cover this
				/*if(400 * getTotalPopulation(!isAVassal()) > 3 * iThreshold)
					return DENIAL_VICTORY;*/
				if(400 * (getTotalPopulation() + kMasterTeam.getTotalPopulation()) >
					3 * iThreshold)
				{
					bPopulationThreat = true;
				}
			}
			bool bLandThreat = true;
			if(kGame.getAdjustedLandPercent(eLoopVictory) > 0)
			{
				bLandThreat = false;
				int iThreshold = GC.getMap().getLandPlots() *
						kGame.getAdjustedLandPercent(eLoopVictory);
				/*if(400 * getTotalLand(!isAVassal()) > 3 * iThreshold)
					return DENIAL_VICTORY;*/ // advc.112
				if(400 * (getTotalLand() + kMasterTeam.getTotalLand()) > 3 * iThreshold)
					bLandThreat = true;
			}
			if(bLandThreat && bPopulationThreat &&
				(kGame.getAdjustedPopulationPercent(eLoopVictory) > 0 ||
				kGame.getAdjustedLandPercent(eLoopVictory) > 0))
			{
				//return DENIAL_POWER_YOU;
				/*  advc.112: On the contrary, when the master is close (75%) to
					a military victory, we're not breaking away. */
				return NO_DENIAL;
			}
		}
	}

	bool bFaraway = false;
	/*  Moved this block up b/c these checks are cheap, and the primary-area
		condition is something the player can't easily change, so the AI should
		mention it right away instead of suggesting that a change in power ratios
		or diplo could lead to a vassal agreement. */
	if (!bWar)
	{	// advc.112: Removed !isParent check
		if(AI_getWorstEnemy() == eMasterTeam)
			return DENIAL_WORST_ENEMY;
		// <advc.112> This used to be checked later
		if(eTowardMaster <= ATTITUDE_FURIOUS)
			return DENIAL_ATTITUDE; // </advc.112>
		if (!bColony && // advc.112
			!AI_hasCitiesInPrimaryArea(eMasterTeam) &&
			AI_calculateAdjacentLandPlots(eMasterTeam) == 0 &&
			GET_PLAYER(getLeaderID()).getCurrentEra() <= ERA_MEDIEVAL) // rfc: different era vassals allowed after the medieval era
		{
			// <advc.112>
			bFaraway = true;
			if (kMasterTeam.getCurrentEra() < CvEraInfo::AI_getAgeOfExploration() + 1)
			{	// </advc.112>
				return DENIAL_TOO_FAR;
			}
            // doc (edead): do not allow far away vassals before Exploration
			if (!kMasterTeam.isHasTech(EXPLORATION) && GET_PLAYER(kMasterTeam.getLeaderID()).isDistant(getLeaderID()))
			{
				return DENIAL_TOO_FAR;
			}
		}
	}
	// <advc.112>
	/*  NB: When this team is human (i.e. BBAI_HUMAN_AS_VASSAL_OPTION enabled
		-- which is not currently supported by AdvCiv/K-Mod), then
		DENIAL_POWER_US and DENIAL_POWER_YOU seem to become swapped outside the SDK. */
	// Don't vassal while we still have plans to expand
	if(!isAVassal() && AI_isSneakAttackPreparing())
		return DENIAL_POWER_US;
	//int iAttitudeModifier = 0; // Computation rewritten further down this function
	// !isParent check removed
	// Computation of iPersonalityModifier moved down
	// Commented-out BBAI code (06/03/09, jdog) deleted
	if(getNumWars() <= 0 && getDefensivePactCount() > 0 && !isAVassal())
	{
		// "We" (= this team and its partners) "are doing fine on our own"
		return DENIAL_POWER_US;
	} // </advc.112>  <advc.143b>
	if(!bWar && getNumNukeUnits() > 0 &&
		getNukeInterception() >= kMasterTeam.getNukeInterception())
	{
		return DENIAL_POWER_US;
	}// </advc.143b>
	int iTotalPower = 0;
	int iNumNonVassals = 0;
	std::vector<scaled> arPowerValues; // advc.112
	for (TeamIter<MAJOR_CIV> it; it.hasNext(); ++it)
	{
		CvTeam& kTeam = *it;
		// advc.112: Put this in a variable
		int iPow = kTeam.getPower(false);
		if (kTeam.isCapitulated())
			iTotalPower += (2 * iPow) / 5;
		else
		{
			// <advc.112> For median computation
			arPowerValues.push_back(iPow);
			iTotalPower += iPow;
			// </advc.112>
			iNumNonVassals++;
		}
	}
	// The default precision looks a bit precarious here wrt. overflow
	typedef ScaledNum<128> scaled128_t;
	// advc.112: Probably not much of an improvement over using the mean
	scaled128_t rMedianPow = stats::median(arPowerValues);
	scaled128_t rAveragePower(iTotalPower, std::max(1, iNumNonVassals));
	scaled128_t rMasterPower = kMasterTeam.getPower(false);
	// <advc.112>
	if(bFaraway ||
		(getNumWars() <= 0 &&
		AI_teamCloseness(eMasterTeam, DEFAULT_PLAYER_CLOSENESS, false, true) <= 0))
	{
		rMasterPower *= fixp(0.7); // </advc.112>
	}
	int const iOurPower = getPower(true); // K-Mod (this value is used a bunch of times separately)
	/*  <advc.143> Reluctant to sign voluntary vassal agreement if we recently
		canceled one */

	// doc: vassal power limit
	if (rMasterPower + iOurPower > iTotalPower / 3)
		return DENIAL_POWER_YOU;
	// doc: vassal population limit
	if (kMasterTeam.getTotalPopulation() + getTotalPopulation() > getTotalPopulation() / 3)
		return DENIAL_POWER_YOU;

	if(!bWar && !isVassal(eMasterTeam))
	{
		CvPlayerAI const& kOurLeader = GET_PLAYER(getLeaderID());
		int iCancelMem = 0;
		for (PlayerAIIter<MAJOR_CIV,NOT_SAME_TEAM_AS> it(eMasterTeam); it.hasNext(); ++it)
		{
			CvPlayerAI const& kFormerMaster = *it;
			/*  If we have memory, then we canceled due to lack of protection;
				doesn't count here. */
			if(kOurLeader.AI_getMemoryCount(kFormerMaster.getID(),
				MEMORY_CANCELLED_VASSAL_AGREEMENT) <= 0)
			{
				iCancelMem = std::max(iCancelMem, kFormerMaster.AI_getMemoryCount(
						kOurLeader.getID(), MEMORY_CANCELLED_VASSAL_AGREEMENT));
			}
		}
		/*  iCancelMem is normally no more than 4, which results in the same
			iPowerMultiplier as for capitulation. */
		iPowerMultiplier += 10 * iCancelMem;
	} // </advc.143>
	/*  <advc.112> Once signed, show some constancy (previously handled by
		CvPlayerAI::AI_considerOffer) */
	if(isAVassal() && !isCapitulated())
	{
		// Obscured; don't want player to aim for a very specific power ratio
		std::vector<int> hashInput;
		hashInput.push_back(kGame.getTeamRank(getID()));
		hashInput.push_back(kGame.getTeamRank(eMasterTeam));
		hashInput.push_back(getNumWars());
		scaled rHash = scaled::hash(hashInput, getLeaderID());
		iPowerMultiplier -= (10 + rHash * 30).round();
	}
	// iPersonalityModifier: moved here from farther up
	// </advc.112>
	int iPersonalityModifier = 0;
	MemberIter itMember(getID());
	for (; itMember.hasNext(); ++itMember)
	{
		iPersonalityModifier += GC.getInfo(itMember->getPersonalityType()).
				getVassalPowerModifier();
	}
	// <advc.112>
	if (bColony)
	{
		iPersonalityModifier /= 2;
		iPersonalityModifier -= 10;
	} // </advc.112>
	scaled128_t rVassalPower = per100(iOurPower * (iPowerMultiplier + iPersonalityModifier /
			std::max(1, itMember.nextIndex())));
	if (bWar)
	{
		scaled rTheirSuccess = scaled::max(10, kMasterTeam.AI_getWarSuccess(getID()));
		scaled rOurSuccess = scaled::max(10, AI_getWarSuccess(eMasterTeam));
		scaled rOthersBestSuccess;
		for (TeamAIIter<MAJOR_CIV,ENEMY_OF> it(getID()); it.hasNext(); ++it)
		{
			CvTeamAI const& kEnemy = *it;
			/*  advc.112: War success of a vassal shouldn't spoil its
				master's chances of winning another vassal. */
			if (kEnemy.getMasterTeam() != eMasterTeam)
				rOthersBestSuccess.increaseTo(kEnemy.AI_getWarSuccess(getID()));
		}

		// Discourage capitulation to a team that has not done the most damage
		if (rTheirSuccess < rOthersBestSuccess)
			rOurSuccess += rOthersBestSuccess - rTheirSuccess;
		// <advc.112> Instead multiply VassalPower by the inverse factor
		//rMasterPower = (2 * rMasterPower * iTheirSuccess) / (iTheirSuccess + iOurSuccess);
		rVassalPower *= (rTheirSuccess + rOurSuccess) /
				(fixp(1.8) * rTheirSuccess); // Slightly reduce the coefficient
		// FURIOUS clause added; WorstEnemy doesn't say much when at war.
		if (AI_getWorstEnemy() == eMasterTeam && eTowardMaster <= ATTITUDE_FURIOUS)
			rMasterPower *= per100(90); // was 75%
		// </advc.112>
	}
	else if (/* advc.112: */ !bColony &&
		// BETTER_BTS_AI_MOD (06/12/10, jdog5000): START
		!kMasterTeam.AI_isLandTarget(getID()))
	{
		rMasterPower /= 2;
	} // BETTER_BTS_AI_MOD: END
	// K-Mod. (condition moved here from lower down; for efficiency.)
	// <advc.112> Special treatment of vassal-master power ratio if colony
	if ((!bColony && 3 * rVassalPower > 2 * rMasterPower) ||
		(bColony && 13 * getPower(true) > 10 * rMasterPower)) // </advc.112>
	{
		return DENIAL_POWER_US;
	} // K-Mod end
	/*	<advc.112b> Don't surrender if there isn't an acute threat.
		(Had used DENIAL_NEVER until v0.99.) */
	if(bWar)
	{
		int iNukes = 0;
		for (PlayerAIIter<EVER_ALIVE,MEMBER_OF> itOurMember(getID());
			itOurMember.hasNext(); ++itOurMember)
		{
			for (MemberIter itMasterMember(eMasterTeam);
				itMasterMember.hasNext(); ++itMasterMember)
			{
				iNukes += itOurMember->AI_getMemoryCount(
						itMasterMember->getID(), MEMORY_NUKED_US);
			}
		}
		if(iNukes == 0)
		{
			int iSafePopulation = 0;
			// Based on code in AI_endWarVal:
			int iTheirAttackers = 0;
			FOR_EACH_AREA(pLoopArea)
			{
				int iAreaCities = countNumCitiesByArea(*pLoopArea);
				if(iAreaCities <= 0)
					continue;
				int iAreaDanger = AI_countEnemyDangerByArea(*pLoopArea, eMasterTeam);
				int iAreaPop = countTotalPopulationByArea(*pLoopArea);
				if(iAreaDanger < iAreaPop / 3)
					iSafePopulation += iAreaPop;
				if(iAreaCities > getNumCities() / 3)
					iTheirAttackers += iAreaDanger;
			}
			/*  Randomly between these two bounds; randomness from a hash of the
				turn number */
			scaled rBound1 = (fixp(0.5) * getCurrentEra() + fixp(1.5)) *
					fixp(0.75) * getNumCities();
			scaled rBound2 = (fixp(0.5) * getCurrentEra() + fixp(1.5)) *
					getNumCities();
			if (iTheirAttackers < rBound1 + scaled::hash(kGame.getGameTurn()) *
				(rBound2 - rBound1))
			{
				return DENIAL_NO_CURRENT_THREAT;
			}
			if(iSafePopulation / (getTotalPopulation() + fixp(0.1)) > fixp(0.3))
				return DENIAL_NO_CURRENT_THREAT;
		}
	} // </advc.112b>
	if (!bWar) // advc: Moved out of the loop below
	{
		for (TeamAIIter<MAJOR_CIV,ENEMY_OF> itEnemy(eMasterTeam);
			itEnemy.hasNext(); ++itEnemy)
		{
			if (!itEnemy->isAtWar(getID()))
			{
				DenialTypes eDenial = AI_declareWarTrade(itEnemy->getID(), eMasterTeam, false);
				if (eDenial != NO_DENIAL)
					return eDenial;
			}
		}
	}
	for (TeamAIIter<MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> itEnemy(getID());
		itEnemy.hasNext(); ++itEnemy)
	{
		CvTeamAI& kEnemy = *itEnemy;
		if (kEnemy.getMasterTeam() == eMasterTeam || !kEnemy.AI_isLandTarget(getID()))
			continue;

		int iEnemyPower = kEnemy.getPower(true); // K-Mod
		if (iEnemyPower > iOurPower)
		{
			if (kEnemy.isAtWar(eMasterTeam) && !kEnemy.isAtWar(getID()) &&
				(!bWar || rMasterPower < 2 * iEnemyPower)) // K-Mod
			{
				return DENIAL_POWER_YOUR_ENEMIES;
			}
			scaled128_t rMult(2 * iEnemyPower, std::max(1, iEnemyPower + iOurPower));
			rAveragePower *= rMult;
			// advc.112: The same threat adjustment for the median
			rMedianPow *= rMult;
			//iAttitudeModifier += (3 * kEnemy.getPower(true)) / std::max(1, getPower(true)) - 2;
			/*  advc.112: Commented out K-Mod's replacement as well.
				Attitude is handled later. */
			//iAttitudeModifier += (6 * iEnemyPower / std::max(1, iOurPower) - 5)/2; // K-Mod. (effectively -2.5 instead of 2)
		}
		if (!kEnemy.isAtWar(eMasterTeam) && kEnemy.isAtWar(getID()))
		{	// <K-Mod>
			rAveragePower *= (iOurPower + rMasterPower) /
					std::max(1, iOurPower + std::max(iOurPower, iEnemyPower)); // </K-Mod>
			// <advc.112>
			rMedianPow *= (iOurPower + rMasterPower) /
					std::max(1, iOurPower + std::max(iOurPower, iEnemyPower)); // </advc.112>
		}
	}

	if (!isVassal(eMasterTeam) && canVassalRevolt(eMasterTeam))
		return DENIAL_POWER_US;

	if(!bColony) // advc.112
	{
		// if (iVassalPower > iAveragePower || 3 * iVassalPower > 2 * iMasterPower)
		// advc.112: Changed coefficients from 5/4 (BBAI, K-Mod) to 1/0.76
		if (rVassalPower > fixp(0.76) * rAveragePower || // K-Mod. (second condition already checked)
			// <advc.112> Median condition; randomization when breaking free
			(!bWar && rVassalPower > fixp(0.76) * rMedianPow))
		{
			if(!isAVassal() ||
				scaled::hash(kGame.getGameTurn(), getLeaderID()) < fixp(0.1))
			{ // </advc.112>
				return DENIAL_POWER_US;
			}
		}
	}

	if (!bWar)
	{	// <advc.112> (code block about DENIAL_TOO_FAR moved up)
		/*  Calculation rewritten with a different goal in mind:
			Prospective vassal evaluates prospective master based on ow threatened
			the vassal feels. (Originally more based on what chances the vassal
			still has to win the game). */
		int iAttitudeModifier = -2;
		int iLosingWarModifier = 0;
		for (TeamAIIter<FREE_MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> itThreat(getID());
			itThreat.hasNext(); ++itThreat)
		{
			CvTeamAI const& kThreat = *itThreat;
			if (!kThreat.AI_isLandTarget(getID()) ||
				6 * getPower(true) > (isAVassal() ? 5 : 4) * kThreat.getPower(true))
			{
				continue;
			}
			bool const bMasterAtWar = kMasterTeam.isAtWar(kThreat.getID());
			// Immediate threat from ongoing wars
			if (isAtWar(kThreat.getID()))
			{
				WarPlanTypes eWarPlan = AI_getWarPlan(kThreat.getID());
				if (kThreat.getID() != eMasterTeam &&
					(eWarPlan == WARPLAN_ATTACKED_RECENT ||
					eWarPlan == WARPLAN_ATTACKED ||
					AI_getWarSuccessRating() <= -30))
				{
					/*	Ensuring that kMaster doesn't drop out of the war
						ought to be worth something */
					iLosingWarModifier += (bMasterAtWar ? 2 : 4);
				}
				continue;
			}
			if (bMasterAtWar)
				continue;
			// Threat from future wars. kMasterTeam can contribute to this.
			AttitudeTypes eTowardUs = NO_ATTITUDE;
			if (kThreat.isHuman()) // Assume that human likes or hates us back
			{
				eTowardUs = AI_getAttitude(kThreat.getID(), false);
				iAttitudeModifier++; // They're always a threat though
			}
			else
			{
				eTowardUs = kThreat.AI_getAttitude(getID(), false);
				/*  Potentially dangerous AI team pleased w/ us or currently busy
					harassing someone else => probably not an immediate threat */
				if(eTowardUs >= ATTITUDE_PLEASED || kThreat.getNumWars() > 0)
					continue;
			}
			iAttitudeModifier += std::max(0, (int)(ATTITUDE_PLEASED - eTowardUs));
		}
		// Adjust to the number of potential alt. war targets
		iAttitudeModifier = (iAttitudeModifier * scaled(4, std::max(1,
				TeamIter<CIV_ALIVE,OTHER_KNOWN_TO>::count(getID()))).sqrt()).round();
		iAttitudeModifier += std::min(iLosingWarModifier, 5);
		/*	No matter how much we like kMasterTeam, when we can safely go it alone,
			we do. Master might not like it (and need sth. to prevent oscillation). */
		if (isAVassal()) // (should perhaps check master's NoWarProb at Pleased)
			iAttitudeModifier += 3;
		if (iAttitudeModifier <= 2 &&
			4 * rVassalPower > 3 * rAveragePower &&
			4 * rVassalPower > 3 * rMedianPow &&
			// Exception: stick to our colonial master
			(!isAVassal() || !kMasterTeam.isParent(getID())))
		{
			return DENIAL_POWER_US;
		}
		// Moved this line down:
		//AttitudeTypes eModifiedAttitude = CvPlayerAI::AI_getAttitudeFromValue(AI_getAttitudeVal(eTeam, false) + iAttitudeModifier);
		// </advc.112>

		for (MemberAIIter itOurMember(getID());
			itOurMember.hasNext(); ++itOurMember)
		{
			CvPlayerAI const& kOurMember = *itOurMember;
			// <advc.112> Handled higher up
			int iAttitudeThresh = GC.getInfo(kOurMember.getPersonalityType()).
					getVassalRefuseAttitudeThreshold();
			if (bColony)
				iAttitudeThresh -= 3;
			/*  Don't apply thresh worse than Cautious, only increase the
				relations modifier. */
			if(iAttitudeThresh < ATTITUDE_CAUTIOUS)
			{
				iAttitudeModifier += (ATTITUDE_CAUTIOUS - iAttitudeThresh);
				iAttitudeThresh = ATTITUDE_CAUTIOUS;
			}
			AttitudeTypes eModifiedAttitude = CvPlayerAI::AI_getAttitudeFromValue(
					AI_getAttitudeVal(eMasterTeam, false) + iAttitudeModifier);
			if(eModifiedAttitude <= iAttitudeThresh) // </advc.112>
				return DENIAL_ATTITUDE;
		}
	}
	else
	{
		/*if (AI_getWarSuccess(eTeam) + 4 * GC.getDefineINT("WAR_SUCCESS_CITY_CAPTURING") > GET_TEAM(eTeam).AI_getWarSuccess(getID()))
			return DENIAL_JOKING;*/ // BtS
		/*  BETTER_BTS_AI_MOD, Diplomacy AI, 12/07/09, jdog5000: START
			Scale better for small empires, particularly necessary if WAR_SUCCESS_CITY_CAPTURING > 10 */
		// <advc> For debugger:
		scaled rVassalSuccess = AI_getWarSuccess(eMasterTeam);
		scaled rMasterSuccess = kMasterTeam.AI_getWarSuccess(getID());
		int iTargetDelta = std::min(getNumCities(), 4) *
				GC.getWAR_SUCCESS_CITY_CAPTURING(); // </advc>
		// <advc.104>
		if (getUWAI().isEnabled())
		{	/*	Try not to be too inconsistent with UWAI::Team::considerCapitulation
				(to avoid answering "not right now" when in fact not close).
				The cached utility values don't account for the peace with 3rd parties
				(implied by capitulation), and it's out of date on a human master's turn,
				so this is all a bit fuzzy. */
			if (uwai().leaderUWAI().getCache().
				warUtilityIgnoringDistraction(eMasterTeam) > -40 ||
				// Expect to tire master out
				kMasterTeam.uwai().leaderUWAI().getCache().
				warUtilityIgnoringDistraction(getID()) < -25)
			{
				return DENIAL_POWER_US;
			}
			// </advc.104>  <advc.104o> Take into account past wars
			int iPastWarScore = GET_PLAYER(getLeaderID()).uwai().getCache().
					pastWarScore(eMasterTeam);
			if (iPastWarScore < 0)
				iTargetDelta = fmath::round(iTargetDelta * 2 / 3.0);
		} // </advc.104o>
		if (rVassalSuccess + iTargetDelta > rMasterSuccess)
			return DENIAL_POWER_US;
		if(!kMasterTeam.isHuman())
		{
			if(!bCheckAccept || // advc.104o
				!kMasterTeam.AI_acceptSurrender(getID()))
			{
				return DENIAL_JOKING;
			}
		}
		// BETTER_BTS_AI_MOD: END
		/*  <advc.112> Based on code in endWarVal. Don't capitulate during
			counteroffensive. AI_enemyTargetMissions is kind of costly, therefore
			check this last of all.*/
		int iOurMissions = 0;
		for (MemberAIIter itOurMember(getID()); itOurMember.hasNext(); ++itOurMember)
			iOurMissions += itOurMember->AI_enemyTargetMissions(eMasterTeam);
		if(iOurMissions > kMasterTeam.getNumCities())
			return DENIAL_JOKING; // </advc.112>
		/*  <advc.104o> Make sure that UWAI::Team::considerPeace has been
			called before surrendering. */
		if(getUWAI().isEnabled() && kMasterTeam.isHuman() &&
			!uwai().leaderUWAI().getCache().isReadyToCapitulate(eMasterTeam))
		{
			return DENIAL_RECENT_CANCEL;
		} // </advc.104o>
	}
	// <advc.143>
	if(!isVassal(eMasterTeam) || isCapitulated())
		return NO_DENIAL;
	/*  When there is already a voluntary vassal agreement, then we're deciding
		whether to cancel the agreement. (VVA is normally handled by AI_vassalTrade,
		which then calls AI_surrenderTrade. However, when it comes to canceling trades,
		AI_surrenderTrade is called directly, so cancellation has to be handled here.)
		Cancel if we have lost much territory. BtS has similar code for
		capitulated vassals in CvTeam::canVassalRevolt. Tiles lost b/c of culture
		can also trigger cancellation; I guess that's OK (and can't be helped). */
	// VassalPower is the land at the time of signing the vassal agreement
	// <advc.112> Lower bound: 10
	scaled rLandRatio(std::max(10, getTotalLand(false)),
			std::max(10, getVassalPower())); // </advc.112>
	static scaled const rLossesThresh = per100(GC.getDefineINT("VASSAL_DENY_OWN_LOSSES_FACTOR"));
	if(rLandRatio < fixp(0.85) * rLossesThresh || (rLandRatio < rLossesThresh &&
		scaled::hash(kGame.getGameTurn(), getLeaderID()) < fixp(0.15)))
	{
		return DENIAL_POWER_YOUR_ENEMIES; // Denial type doesn't matter
	} // </advc.143>  <advc.143b>
	scaled rNuked = 0;
	for (TeamIter<CIV_ALIVE,ENEMY_OF> it(getID()); it.hasNext(); ++it)
	{
		CvTeam const& kEnemy = *it;
		if(kEnemy.getCurrentEra() < CvEraInfo::AI_getAtomicAge()) // for performance
			continue;
		// advc.130q: The average nuke adds 2 to memory
		rNuked += fixp(0.5) * AI_getMemoryCount(kEnemy.getID(), MEMORY_NUKED_US);
	}
	int iCities = getNumCities();
	scaled rNukeThresh = scaled::max(2,
			(fixp(0.4) + fixp(0.6) * scaled::hash(eMasterTeam, getLeaderID())) * iCities);
	if(rNuked > rNukeThresh && kMasterTeam.getNukeInterception() <= getNukeInterception())
		return DENIAL_POWER_YOUR_ENEMIES;
	// </advc.143b>
	return NO_DENIAL;
}

// K-Mod
int CvTeamAI::AI_countMembersWithStrategy(AIStrategy eStrategy) const
{
	int iCount = 0;
	for (MemberAIIter it(getID()); it.hasNext(); ++it)
	{
		if (it->AI_isDoStrategy(eStrategy))
			iCount++;
	}
	return iCount;
} // K-Mod end

// BETTER_BTS_AI_MOD, Victory Strategy AI, 03/20/10, jdog5000: START
bool CvTeamAI::AI_anyMemberAtVictoryStage(AIVictoryStage eStage) const
{
	for (MemberAIIter it(getID()); it.hasNext(); ++it)
	{
		if (it->AI_atVictoryStage(eStage))
			return true;
	}
	return false;
}

bool CvTeamAI::AI_anyMemberAtVictoryStage4() const
{
	for (MemberAIIter it(getID()); it.hasNext(); ++it)
	{
		if (it->AI_atVictoryStage4())
			return true;
	}
	return false;
}

bool CvTeamAI::AI_anyMemberAtVictoryStage3() const
{
	for (MemberAIIter it(getID()); it.hasNext(); ++it)
	{
		if (it->AI_atVictoryStage3())
			return true;
	}
	return false;
} // BETTER_BTS_AI_MOD: END

/*	K-Mod: return a rating of our war success between -99 and 99.
	-99 means we losing and have very little hope of surviving.
	99 means we are soundly defeating our enemies.
	Zero is neutral (eg. no wars being fought).
	(Based on K-Mod code for Force Peace diplomacy voting.)
	Replacing AI_getWarSuccessCapitulationRatio
	(BETTER_BTS_AI_MOD, 03/20/10, jdog5000: War Strategy AI). */
int CvTeamAI::AI_getWarSuccessRating() const
{
	PROFILE_FUNC();

	int iMilitaryUnits = 0;
	for (MemberIter it(getID()); it.hasNext(); ++it)
		iMilitaryUnits += it->getNumMilitaryUnits();

	int iSuccessScale = iMilitaryUnits * GC.getDefineINT(CvGlobals::WAR_SUCCESS_ATTACKING) / 5;

	int iThisTeamPower = getPower(true);
	int iScore = 0;

	for (TeamAIIter<FREE_MAJOR_CIV,ENEMY_OF> itEnemy(getID()); itEnemy.hasNext(); ++itEnemy)
	{
		scaled rThisTeamSuccess = AI_getWarSuccess(itEnemy->getID());
		scaled rOtherTeamSuccess = itEnemy->AI_getWarSuccess(getID());
		int iOtherTeamPower = itEnemy->getPower(true);
		iScore += (rThisTeamSuccess + iSuccessScale).uround() * iThisTeamPower;
		iScore -= (rOtherTeamSuccess + iSuccessScale).uround() * iOtherTeamPower;
	}
	iScore = range((100 * iScore) / std::max(1, iThisTeamPower * iSuccessScale * 5),
			-99, 99);
	return iScore;
}

/*  BETTER_BTS_AI_MOD, War Strategy AI, 03/20/10, jdog5000: START
	Compute power of enemies as percentage of our power */
int CvTeamAI::AI_getEnemyPowerPercent(bool bConsiderOthers) const
{
	int iEnemyPower = 0;
	for (TeamAIIter<CIV_ALIVE,KNOWN_POTENTIAL_ENEMY_OF> itEnemy(getID());
		itEnemy.hasNext(); ++itEnemy)
	{
		CvTeamAI const& kEnemy = *itEnemy;
		if(isAtWar(kEnemy.getID()))
		{
			int iTempPower = 220 * kEnemy.getPower(false);
			iTempPower /= (AI_hasCitiesInPrimaryArea(kEnemy.getID()) ? 2 : 3);
			iTempPower /= (kEnemy.isMinorCiv() ? 3 : 1);
			iTempPower /= std::max(1, (bConsiderOthers ?
					kEnemy.getNumWars(true, true) : 1));
			iEnemyPower += iTempPower;
		}
		else if(AI_isChosenWar(kEnemy.getID()) && // Haven't declared war yet
			/*  advc.104j: getDefensivePower counts vassals already.
				If planning war against multiple civs, DP allies could also be
				double counted (fixme). Could collect the war enemies in a std::set
				in a first pass; though it sucks to implement the vassal/DP logic
				multiple times (already in getDefensivePower and MilitaryAnalyst).
				Also, the computation for bConsiderOthers above can be way off. */
			!kEnemy.isAVassal())
		{
			int iTempPower = 240 * kEnemy.getDefensivePower(getID());
			iTempPower /= (AI_hasCitiesInPrimaryArea(kEnemy.getID()) ? 2 : 3);
			iTempPower /= 1 + (bConsiderOthers ? kEnemy.getNumWars(true, true) : 0);
			iEnemyPower += iTempPower;
		}
	}
	//return (iEnemyPower/std::max(1, (isAVassal() ? getCurrentMasterPower(true) : getPower(true))));
	// K-Mod - Lets not rely too much on our vassals...
	int iOurPower = getPower(false);
	const CvTeam& kMasterTeam = GET_TEAM(getMasterTeam());
	iOurPower += kMasterTeam.getPower(true);
	iOurPower /= 2;
	return iEnemyPower/std::max(1, iOurPower);
	// K-Mod end
}

// advc.105, advc.104:
bool CvTeamAI::AI_isPushover(TeamTypes ePotentialEnemy) const
{
	/*	Stricter checks for human potential enemy? But there's already
		some code for dealing with humans at some of the call sites ... */
	CvTeam const& kPotentialEnemy = GET_TEAM(ePotentialEnemy);
	int iTheirCities = kPotentialEnemy.getNumCities();
	int iOurCities = getNumCities();
	return (((iTheirCities <= 1 && iOurCities >= 3) ||
			4 * iTheirCities < iOurCities) &&
			10 * kPotentialEnemy.getPower(true) < 4 * getPower(false));
}

// K-Mod
int CvTeamAI::AI_getAirPower() const
{
	int iTotalPower = 0;
	FOR_EACH_ENUM(UnitClass)
	{
		/*  Since units of each class are counted per team rather than units of each type,
			just assume the default unit type. */
		UnitTypes eLoopUnit = GC.getInfo(eLoopUnitClass).getDefaultUnit();
		if (eLoopUnit == NO_UNIT)
			continue;

		const CvUnitInfo& kUnitInfo = GC.getInfo(eLoopUnit);
		if (kUnitInfo.getDomainType() == DOMAIN_AIR && kUnitInfo.getAirCombat() > 0)
			iTotalPower += getUnitClassCount(eLoopUnitClass) * kUnitInfo.getPowerValue();
	}
	return iTotalPower;
}

/*	Sum up air power of enemies plus average of other civs we've met
	K-Mod: I've rewritten this BBAI function to loop over unit classes
	rather than unit types. This is because a loop over unit types will double-count
	if there are two units in the same class. */
int CvTeamAI::AI_getRivalAirPower() const
{
	std::vector<UnitTypes> aeAirUnitTypes; // advc.opt: Compute these upfront
	FOR_EACH_ENUM(UnitClass)
	{
		// (See comment in AI_getAirPower)
		UnitTypes eLoopUnit = GC.getInfo(eLoopUnitClass).getDefaultUnit();
		if (eLoopUnit == NO_UNIT)
			continue;
		if (GC.getInfo(eLoopUnit).getDomainType() == DOMAIN_AIR &&
			GC.getInfo(eLoopUnit).getAirCombat() > 0)
		{
			aeAirUnitTypes.push_back(eLoopUnit); // advc.opt
		}
	}

	// Count enemy air units, not just those visible to us
	int iRivalAirPower = 0;
	int iEnemyAirPower = 0;
	int iTeamCount = 0;
	for (size_t i = 0; i < aeAirUnitTypes.size(); i++) // advc.opt
	{
		CvUnitInfo const& kUnit = GC.getInfo(aeAirUnitTypes[i]);
		UnitClassTypes eUnitClass = kUnit.getUnitClassType();
		// advc.001: Surely our vassals shouldn't count for rival air power
		TeamAIIter<MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> itRival(getID());
		for (; itRival.hasNext(); ++itRival)
		{
			// <advc.131>
			if (!isBarbarian() && itRival->AI_isAvoidWar(getID()))
				continue; // </advc.131>
			int iUnitPower = kUnit.getPowerValue() *
					// advc (note): This is cheating
					itRival->getUnitClassCount(eUnitClass);
			iRivalAirPower += iUnitPower;
			if (AI_getWarPlan(itRival->getID()) != NO_WARPLAN)
				iEnemyAirPower += iUnitPower;
		}
		iTeamCount += itRival.nextIndex();
	}
	return iEnemyAirPower + iRivalAirPower / std::max(1, iTeamCount);
}

// K-Mod:
bool CvTeamAI::AI_refusePeace(TeamTypes ePeaceTeam) const
{
	// Refuse peace if we need the war for our conquest / domination victory.
	return (!isHuman() && AI_anyMemberAtVictoryStage(AI_VICTORY_MILITARY4) &&
			((AI_isChosenWar(ePeaceTeam) &&
			// advc.115:
			GET_TEAM(ePeaceTeam).AI_getWarPlan(getID()) == WARPLAN_ATTACKED_RECENT) ||
			getNumWars(true, true) == 1) && AI_getWarSuccessRating() > 0);
}

bool CvTeamAI::AI_refuseWar(TeamTypes eWarTeam) const
{
	if (isHuman())
		return false;
	// <advc.104y>
	if (AI_isAvoidWar(eWarTeam, true))
	{
		AttitudeTypes eAttitude = AI_getAttitude(eWarTeam); // </advc.104y>
		// ok, so we wouldn't independently choose this war, but could we be bought into it?
		// If any of our team would refuse, then the team refuses. (cf. AI_declareWarTrade)
		for (MemberIter it(getID()); it.hasNext(); ++it)
		{
			if (eAttitude > GC.getInfo(it->getPersonalityType()).
				getDeclareWarThemRefuseAttitudeThreshold())
			{
				return true;
			}
		}
	}
	return false; // otherwise, war is acceptable
} // K-Mod end

// BBAI function, edited for K-Mod (most of the K-Mod changes are unmarked).
bool CvTeamAI::AI_acceptSurrender(TeamTypes eSurrenderTeam) const
{
	//PROFILE_FUNC(); // advc.003o
	const CvTeamAI& kSurrenderTeam = GET_TEAM(eSurrenderTeam);

	if (isHuman())
		return true;

	if (!isAtWar(eSurrenderTeam))
		return true;

	// advc.112: Now handled by the vassal
	/*if (kSurrenderTeam.AI_anyMemberAtVictoryStage(AI_VICTORY_SPACE3 | AI_VICTORY_CULTURE3)) {
		// Capturing capital or Apollo city will stop space
		// Capturing top culture cities will stop culture
		return false;
	}*/

	// Check for whether another team has won enough to cause capitulation
	bool bMightCapToOther = false; // K-Mod
	// advc.112: Exclude all vassals (not just ours) and minor civs
	for (TeamAIIter<FREE_MAJOR_CIV,ENEMY_OF> itOther(eSurrenderTeam);
		itOther.hasNext(); ++itOther)
	{
		if (itOther->getID() == getID())
			continue;
		if (kSurrenderTeam.AI_getAtWarCounter(itOther->getID()) <
			12 - itOther->AI_getCurrEraFactor() && // advc.112: was 10 flat
			kSurrenderTeam.AI_getWarSuccess(itOther->getID()) +
			std::min(kSurrenderTeam.getNumCities(), 4) *
			GC.getWAR_SUCCESS_CITY_CAPTURING() <
			itOther->AI_getWarSuccess(eSurrenderTeam))
		{	//return true;
			/*  K-Mod: that's not the only capitulation condition. I might revise it later,
				but in the mean time I'll just relax the effect. */
			bMightCapToOther = true;
			break;
		}
	}

	int iValuableCities = 0;
	int iCitiesThreatenedByUs = 0;
	int iValuableCitiesThreatenedByUs = 0;
	int iCitiesThreatenedByOthers = 0;
	int iValuablesWithOurCulture = 0; // advc.099c
	for (MemberAIIter itSurr(eSurrenderTeam); itSurr.hasNext(); ++itSurr)
	{
		CvPlayerAI const& kSurrenderMember = *itSurr;
		FOR_EACH_CITYAI(pLoopCity, kSurrenderMember)
		{
			CvCityAI const& kCity = *pLoopCity;
			bool bValuable = (kCity.isHolyCity() || kCity.isHeadquarters() ||
					kCity.hasActiveWorldWonder() ||
					(AI_isPrimaryArea(kCity.getArea()) &&
					kSurrenderTeam.countNumCitiesByArea(kCity.getArea()) < 3) ||
					(kCity.isCapital() &&
					(kSurrenderTeam.getNumCities() > kSurrenderTeam.getNumMembers() ||
					countNumCitiesByArea(kCity.getArea()) > 0)));
			if(!bValuable)
			{
				// Valuable terrain bonuses
				for (CityPlotIter itPlot(kCity); itPlot.hasNext(); ++itPlot)
				{
					BonusTypes eBonus = itPlot->getNonObsoleteBonusType(getID());
					if (eBonus == NO_BONUS)
						continue;
					if(GET_PLAYER(getLeaderID()).AI_bonusVal(eBonus, 1) > 15)
					{
						bValuable = true;
						break;
					}
				}
			}
			// <advc.099c>
			if(bValuable && pLoopCity->getPlot().calculateTeamCulturePercent(getID()) > 25)
				iValuablesWithOurCulture++; // </advc.099c>
			/*int iOwnerPower = kSurrenderMember.AI_getOurPlotStrength(kCity.plot(), 2, true, false);
			int iOurPower = AI_getOurPlotStrength(kCity.plot(), 2, false, false, true);
			int iOtherPower = kSurrenderMember.AI_getEnemyPlotStrength(pkCity.plot(), 2, false, false) - iOurPower; */
			// K-Mod. Note. my new functions are not quite the same as the old.
			// a) this will not count vassals in "our power". b) it will only count forces that can been seen by the player calling the function.
			int iOwnerPower = kSurrenderMember.AI_localDefenceStrength(kCity.plot(),
					kSurrenderMember.getTeam(), DOMAIN_LAND, 2, true, false, true);
			int iOurPower = GET_PLAYER(getLeaderID()).AI_localAttackStrength(
					kCity.plot(), getID());
			int iOtherPower = kSurrenderMember.AI_localAttackStrength(kCity.plot())
					- iOurPower;
			// K-Mod end
			if (iOtherPower > iOwnerPower)
				iCitiesThreatenedByOthers++;

			/*  advc.130v: Added the coefficients. Now that capitulated vassals
				have fewer downsides, the AI should be quicker to accept them,
				at least if they put up a fight. */
			if (2 * iOurPower > 3 * iOwnerPower)
			{
				iCitiesThreatenedByUs++;
				if (bValuable)
				{
					iValuableCities++;
					iValuableCitiesThreatenedByUs++;
					continue;
				}
			}

			if (bValuable && kCity.getHighestPopulation() < 5)
				bValuable = false;

			if (!bValuable)
				continue;

			if (AI_isPrimaryArea(kCity.getArea()))
			{
				iValuableCities++;
				continue;
			}

			for (MemberIter itOurMember(getID()); itOurMember.hasNext(); ++itOurMember)
			{
				if (kCity.AI_playerCloseness(itOurMember->getID(),
					/* <advc.001n> */ DEFAULT_PLAYER_CLOSENESS, true /* </advc.001n> */) > 5)
				{
					iValuableCities++;
					break;
				}
			}
		}
	}

	int iOurWarSuccessRating = AI_getWarSuccessRating();
	if (iOurWarSuccessRating < -30)
	{	// We're doing badly overall, need to be done with this war and gain an ally
		return true;
	}
	/*  advc.099c: Was > 0. Should be less keen on conquering large cities b/c
		the foreign culture will cause problems. maxWarRand is between 50 and 400 (Gandhi). */
	if(iValuableCitiesThreatenedByUs > AI_maxWarRand() / 100)
	{	// Press for capture of valuable city
		return false;
	}
	// K-Mod.
	if (iCitiesThreatenedByOthers > (1 + iCitiesThreatenedByUs/2) &&
			(bMightCapToOther || iCitiesThreatenedByOthers >= iValuableCities)) //
	{	// Keep others from capturing spoils, but let it go if surrender civ is too small to care about
		/*if (6 * (iValuableCities + kSurrenderTeam.getNumCities()) > getNumCities())
			return true;*/ // BBAI
		// K-Mod
		if (5*iValuableCities + 3*(kSurrenderTeam.getNumCities()-iCitiesThreatenedByUs) > getNumCities())
			return true;
		// K-Mod end
	}

	// If we're low on the totem pole, accept so enemies don't drag anyone else into war with us
	// Top rank is 0, second is 1, etc.
	if ((bMightCapToOther || iOurWarSuccessRating < 60) &&
			GC.getGame().getTeamRank(getID()) >
			1 + GC.getGame().countCivTeamsAlive()/3)
		return true;

	if (iOurWarSuccessRating < 50)
	{
		// Accept if we have other wars to fight
		/*  advc (comment): Don't consider wars in preparation; if we didn't think that
			we can handle both enemies at once, we wouldn't have started preparations. */
		for (TeamAIIter<MAJOR_CIV,ENEMY_OF> itEnemy(getID());
			itEnemy.hasNext(); ++itEnemy)
		{
			if (itEnemy->getMasterTeam() != eSurrenderTeam)
			{
				if (itEnemy->AI_getWarSuccess(getID()) >
					5 * GC.getDefineINT(CvGlobals::WAR_SUCCESS_ATTACKING))
				{
					return true;
				}
			}
		}
	}

	// War weariness
	int iWearinessThreshold = (GC.getGame().isOption(GAMEOPTION_AGGRESSIVE_AI) ? 300 : 240);
	if (!bMightCapToOther)
	{
		iWearinessThreshold += 20*iValuableCities + 30*iCitiesThreatenedByUs;
		iWearinessThreshold += 10*std::max(0, GC.getInfo(GC.getMap().getWorldSize()).getTargetNumCities() - kSurrenderTeam.getNumCities()); // (to help finish off small civs)
	}

	for (MemberIter it(getID()); it.hasNext(); ++it)
	{
		CvPlayer const& kOurMember = *it;
		// K-Mod note: it isn't really "percent". The API lies.
		if (kOurMember.getWarWearinessPercentAnger() > iWearinessThreshold)
		{
			int iWWPerMil = kOurMember.getModifiedWarWearinessPercentAnger(
					getWarWeariness(eSurrenderTeam, true) / 100);
			if (iWWPerMil > iWearinessThreshold/2)
				return true;
		}
	}
	/*  advc.099c: Was iCitiesThreatenedByUs+iValuableCities.
		Note that most cities are considered valuable. Added the >0 clause. */
	if(iCitiesThreatenedByUs > 0 && iCitiesThreatenedByUs >= AI_maxWarRand() / 100)
	{	// Continue conquest
		return false;
	}
	/*  <advc.099c> Instead keep fighting if they have cities with our culture, or
		if we still have relatively few cities. */
	if(iValuablesWithOurCulture > 0 || getNumCities() <
			(GC.getInfo(GC.getMap().getWorldSize()).getTargetNumCities() *
			7 * getNumMembers()) / 5)
		return false;
	// </advc.099c>
	if (kSurrenderTeam.getNumCities() < (getNumCities()/4 - (AI_maxWarRand()/100)))
	{	// Too small to bother leaving alive
		return false;
	}

	return true;
}

// BETTER_BTS_AI_MOD, War Strategy AI, 03/20/10, jdog5000: START
void CvTeamAI::AI_getWarRands(int &iMaxWarRand, int &iLimitedWarRand, int &iDogpileWarRand) const
{
	iMaxWarRand = AI_maxWarRand();
	iLimitedWarRand = AI_limitedWarRand();
	iDogpileWarRand = AI_dogpileWarRand();

	bool bCult4 = false;
	bool bSpace4 = false;
	bool bCult3 = false;
	bool bFinalWar = false;

	for (MemberAIIter it(getID()); it.hasNext(); ++it)
	{
		CvPlayerAI const& kMember = *it;
		if (kMember.AI_isDoStrategy(AI_STRATEGY_FINAL_WAR))
			bFinalWar = true;
		if (kMember.AI_atVictoryStage(AI_VICTORY_CULTURE4))
			bCult4 = true;
		if (kMember.AI_atVictoryStage(AI_VICTORY_CULTURE3))
			bCult3 = true;
		if (kMember.AI_atVictoryStage(AI_VICTORY_SPACE4))
			bSpace4 = true;
	}

	if (bCult4)
	{
		iMaxWarRand *= 4;
		iLimitedWarRand *= 3;
		iDogpileWarRand *= 2;
	}
	else if (bSpace4)
	{
		iMaxWarRand *= 3;

		iLimitedWarRand *= 2;

		iDogpileWarRand *= 3;
		iDogpileWarRand /= 2;
	}
	else if (bCult3)
	{
		iMaxWarRand *= 2;

		iLimitedWarRand *= 3;
		iLimitedWarRand /= 2;

		iDogpileWarRand *= 3;
		iDogpileWarRand /= 2;
	}

	int iNumMembers = getNumMembers();
	int iNumVassals = getVassalCount();

	iMaxWarRand *= (2 + iNumMembers);
	iMaxWarRand /= (2 + iNumMembers + iNumVassals);

	if (bFinalWar)
		iMaxWarRand /= 4;

	iLimitedWarRand *= (2 + iNumMembers);
	iLimitedWarRand /= (2 + iNumMembers + iNumVassals);

	iDogpileWarRand *= (2 + iNumMembers);
	iDogpileWarRand /= (2 + iNumMembers + iNumVassals);
}


void CvTeamAI::AI_getWarThresholds(int &iTotalWarThreshold, int &iLimitedWarThreshold, int &iDogpileWarThreshold) const
{
	iTotalWarThreshold = 0;
	iLimitedWarThreshold = 0;
	iDogpileWarThreshold = 0;

	//int iHighUnitSpendingPercent = 0;
	int iHighUnitSpending = 0; // K-Mod
	bool bConq2 = false;
	bool bDom3 = false;
	bool bAggressive = GC.getGame().isOption(GAMEOPTION_AGGRESSIVE_AI);
	for (MemberAIIter itMember(getID()); itMember.hasNext(); ++itMember)
	{
		CvPlayerAI const& kMember = *itMember;

		/* int iUnitSpendingPercent = (kMember.calculateUnitCost() * 100) / std::max(1, kMember.calculatePreInflatedCosts());
		iHighUnitSpendingPercent += (std::max(0, iUnitSpendingPercent - 7) / 2); */
		int iUnitSpendingPerMil = kMember.AI_unitCostPerMil(); // K-Mod
		iHighUnitSpending += (std::max(0, iUnitSpendingPerMil - 16) / 6); // K-Mod

		if (kMember.AI_isDoStrategy(AI_STRATEGY_DAGGER) ||
			kMember.AI_atVictoryStage(AI_VICTORY_MILITARY4))
		{
			bAggressive = true;
		}
		if (kMember.AI_atVictoryStage(AI_VICTORY_CONQUEST2))
			bConq2 = true;
		if (kMember.AI_atVictoryStage(AI_VICTORY_DOMINATION3))
			bDom3 = true;
	}

	iHighUnitSpending /= std::max(1, getNumMembers());
	iTotalWarThreshold = iHighUnitSpending *
			//(bAggressive ? 3 : 2);
			2; // advc.019: The '+=bAggressive?1:0' below should be enough aggro
	if (bDom3)
	{
		iTotalWarThreshold *= 3;
		iDogpileWarThreshold += 5;
	}
	else if (bConq2)
	{
		iTotalWarThreshold *= 2;
		iDogpileWarThreshold += 2;
	}
	iTotalWarThreshold /= 3;
	iTotalWarThreshold += bAggressive ? 1 : 0;

	if (bAggressive &&
		GET_PLAYER(getLeaderID()).getCurrentEra() < CvEraInfo::AI_getAgeOfExploration())
	{
		iLimitedWarThreshold += 2;
	}
}

// Returns odds of player declaring total war times 100
int CvTeamAI::AI_getTotalWarOddsTimes100() const
{
	int iTotalWarRand;
	int iLimitedWarRand;
	int iDogpileWarRand;
	AI_getWarRands(iTotalWarRand, iLimitedWarRand, iDogpileWarRand);

	/*  <advc.104> With UWAI, this function is only called for AI tech and civic
		decisions. Don't want unit spending (see AI_getWarThresholds) to matter
		for those decisions. */
	if(getUWAI().isEnabled())
	{
		// I don't see a fundamental difference between Domination and Conquest here
		int iMilitaryVictoryFactor = 0;
		if(AI_anyMemberAtVictoryStage(AI_VICTORY_MILITARY2))
			iMilitaryVictoryFactor = 3; // Don't care about 2 vs. 3 vs. 4 here
		else if(AI_anyMemberAtVictoryStage(AI_VICTORY_MILITARY1))
			iMilitaryVictoryFactor = 2;
		return 100 * iMilitaryVictoryFactor + 20000 / std::max(iTotalWarRand, 1);
	} // </advc.104>

	int iTotalWarThreshold;
	int iLimitedWarThreshold;
	int iDogpileWarThreshold;
	AI_getWarThresholds(iTotalWarThreshold, iLimitedWarThreshold, iDogpileWarThreshold);

	return ((100 * 100 * iTotalWarThreshold) / std::max(1, iTotalWarRand));
}
// BETTER_BTS_AI_MOD: END

int CvTeamAI::AI_makePeaceTradeVal(TeamTypes ePeaceTeam, TeamTypes eTeam) const
{
	FAssert(eTeam != getID());
	FAssert(ePeaceTeam != getID());
	FAssert(GET_TEAM(ePeaceTeam).isAlive());
	FAssert(atWar(ePeaceTeam, eTeam));
	// <advc.104>
	if(getUWAI().isEnabled())
		return GET_TEAM(eTeam).uwai().makePeaceTradeVal(ePeaceTeam, getID());
	// </advc.104>
	int iValue = (50 + GC.getGame().getGameTurn());
	iValue += ((GET_TEAM(eTeam).getNumCities() + GET_TEAM(ePeaceTeam).getNumCities()) * 8);

	int iModifier = 0;

	switch ((GET_TEAM(eTeam).AI_getAttitude(ePeaceTeam) + GET_TEAM(ePeaceTeam).AI_getAttitude(eTeam)) / 2)
	{
	case ATTITUDE_FURIOUS:
		iModifier += 400;
		break;

	case ATTITUDE_ANNOYED:
		iModifier += 200;
		break;

	case ATTITUDE_CAUTIOUS:
		iModifier += 100;
		break;

	case ATTITUDE_PLEASED:
		iModifier += 50;
		break;

	case ATTITUDE_FRIENDLY:
		break;

	default:
		FAssert(false);
		break;
	}

	iValue *= std::max(0, (iModifier + 100));
	iValue /= 100;

	iValue *= 40;
	iValue /= (GET_TEAM(eTeam).AI_getAtWarCounter(ePeaceTeam) + 10);
	return AI_roundTradeVal(iValue);
}

// advc.104k: Same procedure as in BtS mostly
int CvTeamAI::AI_roundTradeVal(int iVal) const
{
	int rem = GC.getDefineINT(CvGlobals::DIPLOMACY_VALUE_REMAINDER);
	iVal -= iVal % rem;
	/*  Not sure if this lower bound is really needed. The BtS code
		(see CvPlayerAI::AI_roundTradeVal) doesn't have it. */
	if (isHuman())
		return std::max(iVal, rem);
	return iVal;
}

// advc.104i:
void CvTeamAI::AI_makeUnwillingToTalk(TeamTypes eOther)
{
	if (!getUWAI().isEnabled())
		return;
	// No need to make vassals unwilling to talk; can't negotiate war/ peace anyway.
	if (eOther == NO_TEAM || isAVassal() || GET_TEAM(eOther).isAVassal())
		return;
	/*  Make each leading member i of our team unwilling to talk to every
		leading member j of the other team. "Leading": team leader or human;
		only these can make peace. */
	for (MemberAIIter itOur(getID()); itOur.hasNext(); ++itOur)
	{
		CvPlayerAI& kOurMember = *itOur;
		if(!kOurMember.isHuman() && kOurMember.getID() != getLeaderID())
			continue;
		for (MemberAIIter itTheir(eOther); itTheir.hasNext(); ++itTheir)
		{
			CvPlayerAI& kTheirMember = *itTheir;
			if(!kTheirMember.isHuman() && kTheirMember.getID() != GET_TEAM(eOther).getLeaderID())
				continue;
			if (!kOurMember.isHuman() &&
				kOurMember.AI_getMemoryCount(kTheirMember.getID(), MEMORY_DECLARED_WAR_RECENT) < 2)
			{
				kOurMember.AI_rememberEvent(kTheirMember.getID(),
						MEMORY_DECLARED_WAR_RECENT);
			}
			/*  Memory has no effect on humans. Make the other side unwilling then.
				Could simply always make both sides unwilling, but then, the
				expected RTT duration would become longer. */
			else if(kOurMember.isHuman() && kTheirMember.AI_getMemoryCount(
				kOurMember.getID(), MEMORY_DECLARED_WAR_RECENT) < 2)
			{
				kTheirMember.AI_rememberEvent(kOurMember.getID(),
						MEMORY_DECLARED_WAR_RECENT);
			}
		}
	}
}


DenialTypes CvTeamAI::AI_makePeaceTrade(TeamTypes ePeaceTeam, TeamTypes eBroker) const  // advc: eTeam renamed to eBroker
{
	FAssert(eBroker != getID());
	FAssert(ePeaceTeam != getID());
	FAssert(GET_TEAM(ePeaceTeam).isAlive());
	FAssert(isAtWar(ePeaceTeam));

	if (GET_TEAM(ePeaceTeam).isHuman())
	{	//return DENIAL_CONTACT_THEM;
		// advc.004d: Reserve "contact them" for when we'd like to end the war
		return DENIAL_PEACE_NOT_POSSIBLE_US;
	}

	if (GET_TEAM(ePeaceTeam).isAVassal())
		return DENIAL_VASSAL;

	if (isHuman())
		return NO_DENIAL;

	if (!canChangeWarPeace(ePeaceTeam))
		return DENIAL_VASSAL;

	// <advc.104>
	if(getUWAI().isEnabled())
		return uwai().makePeaceTrade(ePeaceTeam, eBroker);
	// </advc.104>

	int iOurPeaceValue = AI_endWarVal(ePeaceTeam);
	int iTheirPeaceValue = GET_TEAM(ePeaceTeam).AI_endWarVal(getID());

	if (iOurPeaceValue > iTheirPeaceValue * 2)
		return DENIAL_CONTACT_THEM;

	// doc: no peace if they are an expansion target and we are winning
	if (iTheirPeaceValue > iOurPeaceValue)
	{
		FOR_EACH_CITY(pLoopCity, GET_PLAYER(GET_TEAM(ePeaceTeam).getLeaderID()))
		{
			if (pLoopCity->getExpansion() == getLeaderID())
				return DENIAL_WORST_ENEMY;
		}
	}

	/*int iLandRatio = ((getTotalLand(true) * 100) / std::max(20, GET_TEAM(eTeam).getTotalLand(true)));
	if (iLandRatio > 250)
		return DENIAL_VICTORY;*/ // BtS
	// K-Mod
	if (AI_refusePeace(ePeaceTeam))
		return DENIAL_VICTORY;
	// <advc.004d>
	if(isAtWar(eBroker) && !GET_TEAM(ePeaceTeam).AI_refusePeace(getID()) &&
		GET_PLAYER(GET_TEAM(ePeaceTeam).getLeaderID()).AI_isWillingToTalk(getLeaderID()))
	{
		return NO_DENIAL;
	} // </advc.004d>
	if (!GET_PLAYER(getLeaderID()).canContact(GET_TEAM(ePeaceTeam).getLeaderID(), true))
	{	//return DENIAL_CONTACT_THEM;
		return DENIAL_RECENT_CANCEL; // advc.004d: Contacting them is not helpful
	}
	if (GET_TEAM(ePeaceTeam).AI_refusePeace(getID()))
		return DENIAL_CONTACT_THEM;
	// K-Mod end
	return NO_DENIAL;
}

// advc.104o: Moved the K-Mod/BtS code from AI_declareWarTradeVal here
int CvTeamAI::AI_declareWarTradeValLegacy(TeamTypes eWarTeam, TeamTypes eTeam) const
{
	PROFILE_FUNC();

	FAssert(eTeam != getID());
	FAssert(eWarTeam != getID());
	FAssert(GET_TEAM(eWarTeam).isAlive());
	FAssert(!atWar(eWarTeam, eTeam));

	int iValue = 0;
	iValue += (GET_TEAM(eWarTeam).getNumCities() * 10);
	iValue += (GET_TEAM(eWarTeam).getTotalPopulation(true) * 2);

	int iModifier = 0;

	switch (GET_TEAM(eTeam).AI_getAttitude(eWarTeam))
	{
	case ATTITUDE_FURIOUS:
		break;

	case ATTITUDE_ANNOYED:
		iModifier += 25;
		break;

	case ATTITUDE_CAUTIOUS:
		iModifier += 50;
		break;

	case ATTITUDE_PLEASED:
		iModifier += 150;
		break;

	case ATTITUDE_FRIENDLY:
		iModifier += 400;
		break;

	default:
		FErrorMsg("unknown attitude type");
	}

	iValue *= std::max(0, (iModifier + 100));
	iValue /= 100;

	int iTheirPower = GET_TEAM(eTeam).getPower(true);
	int iWarTeamPower = GET_TEAM(eWarTeam).getPower(true);

	static int const iWAR_TRADEVAL_POWER_WEIGHT = GC.getDefineINT("WAR_TRADEVAL_POWER_WEIGHT"); // advc.100
	iValue *= 50 + ((/* advc.100: */ iWAR_TRADEVAL_POWER_WEIGHT
			* iWarTeamPower) / (iTheirPower + iWarTeamPower + 1));
	iValue /= 100;

	if (!GET_TEAM(eTeam).AI_isLandTarget(eWarTeam, true))
		iValue *= 2;

	if (!isAtWar(eWarTeam))
		iValue *= 3;
	else
	{
		iValue *= 150;
		iValue /= 100 + (50 * std::min(100, AI_getWarSuccess(eWarTeam).getPercent() /
				(8 + getTotalPopulation(false)))) / 100;
	}

	iValue += GET_TEAM(eTeam).getNumCities() * 20;
	iValue += GET_TEAM(eTeam).getTotalPopulation(true) * 15;

	if (isAtWar(eWarTeam))
	{
		switch (GET_TEAM(eTeam).AI_getAttitude(getID()))
		{
		case ATTITUDE_FURIOUS:
		case ATTITUDE_ANNOYED:
		case ATTITUDE_CAUTIOUS:
			iValue *= 100;
			break;

		case ATTITUDE_PLEASED:
			iValue *= std::max(75, 100 - getNumWars() * 10);
			break;

		case ATTITUDE_FRIENDLY:
			iValue *= std::max(50, 100 - getNumWars() * 20);
			break;

		default:
			FAssert(false);
		}
		iValue /= 100;
	}

	iValue += GET_TEAM(eWarTeam).getNumNukeUnits() * 250;//Don't want to get nuked
	iValue += GET_TEAM(eTeam).getNumNukeUnits() * 150;//Don't want to use nukes on another's behalf

	if (GET_TEAM(eWarTeam).getNumWars(false) <= 0)
	{
		iValue *= 2;
		for (TeamIter<MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> it(eWarTeam); it.hasNext(); ++it)
		{
			CvTeam const& kDPTeam = *it;
			if (kDPTeam.getID() != getID() && kDPTeam.getID() != eTeam &&
				// advc.001: Check master's DP
				GET_TEAM(kDPTeam.getMasterTeam()).isDefensivePact(
				GET_TEAM(eWarTeam).getMasterTeam()))
			{
				iValue += kDPTeam.getNumCities() * 30;
				iValue += kDPTeam.getTotalPopulation(true) * 20;
			}
		}
	}

	iValue *= 60 + (140 * GC.getGame().getGameTurn()) /
			std::max(1, GC.getGame().getEstimateEndTurn());
	iValue /= 100;
	return iValue;
}

// advc.104o: Rewritten
int CvTeamAI::AI_declareWarTradeVal(TeamTypes eTarget, TeamTypes eSponsor) const
{
	PROFILE_FUNC();
	int iTradeVal=-1;
	if (getUWAI().isEnabled())
	{
		iTradeVal = GET_TEAM(eSponsor).uwai().declareWarTradeVal(
				// eWarTeam can be a (voluntary) vassal
				GET_TEAM(eTarget).getMasterTeam(), getID());
	}
	else iTradeVal = AI_declareWarTradeValLegacy(eTarget, eSponsor);
	/*	Don't charge much less than for an embargo. An embargo (weirdly)
		would only compel one player to stop trading with the (whole) target team,
		so we need to sum up the embargo trade values of the members of this team. */
	int iEmbargoTradeVal = 0;
	for (MemberIter itMember(getID()); itMember.hasNext(); ++itMember)
	{
		if (itMember->canStopTradingWithTeam(eTarget))
		{
			/*	AI_declareWarTradeVal gets called on the hireling, whereas
				AI_stopTradingTradeVal gets called on the sponsor. */
			iEmbargoTradeVal += GET_PLAYER(GET_TEAM(eSponsor).getLeaderID()).
					AI_stopTradingTradeVal(eTarget, itMember->getID(), true);
		}
	}
	iTradeVal = std::max(iTradeVal, (fixp(0.83) * iEmbargoTradeVal).round());
	return AI_roundTradeVal(iTradeVal);
}


DenialTypes CvTeamAI::AI_declareWarTrade(
	// advc: params renamed
	TeamTypes eTarget, TeamTypes eSponsor, bool bConsiderPower) const
{
	PROFILE_FUNC();

	FAssert(eSponsor != getID());
	FAssert(eTarget != getID());
	FAssert(GET_TEAM(eTarget).isAlive());
	FAssert(!isAtWar(eTarget));

	if (GET_TEAM(eTarget).isVassal(eSponsor) || GET_TEAM(eTarget).isDefensivePact(eSponsor))
		return DENIAL_JOKING;

	if (isHuman())
		return NO_DENIAL;

	if (!canDeclareWar(eTarget))
		return DENIAL_VASSAL;
	// <advc.104o> Provide no further info to an enemy (applies even when UWAI disabled)
	if(AI_getWorstEnemy() == eSponsor)
		return DENIAL_WORST_ENEMY;
	if(!getUWAI().isEnabled())
	{	// UWAI handles these DenialTypes later // </advc.104o>
		// BETTER_BTS_AI_MOD, Diplomacy, 12/06/09, jdog5000
		/*if (getAnyWarPlanCount(true) > 0)
			return DENIAL_TOO_MANY_WARS;*/ // BtS
		// Hide WHEOOHRN revealing war plans
		if (getNumWars() > 0)
			return DENIAL_TOO_MANY_WARS;
		// BETTER_BTS_AI_MOD: END
		if (bConsiderPower)
		{
			bool bLandTarget = AI_isLandTarget(eTarget, true);
			int iDefPower = GET_TEAM(eTarget).getDefensivePower(getID());
			int iPow = getPower(true);
			int iAggPower = iPow + ((::atWar(eTarget, eSponsor)) ? GET_TEAM(eSponsor).getPower(true) : 0);
			/*  <advc.100> Introduced variables iPow, iAggPower, iDefPower.
				Made the comparison stricter (more reluctant to declare war).
				Added a second clause: don't gang up on enemies with far greater power. */
			if (iDefPower / (bLandTarget ? 1.5 : 1.0) > iAggPower || // was 2 : 1
				(iDefPower > iAggPower && iPow * 2 < iDefPower)) // </advc.100>
			{
				if (bLandTarget)
					return DENIAL_POWER_THEM;
				return DENIAL_NO_GAIN;
			}
		}
	}

	AttitudeTypes eTowardSponsor = AI_getAttitude(eSponsor);
	for (MemberIter it(getID()); it.hasNext(); ++it)
	{
		if (eTowardSponsor <= GC.getInfo(it->getPersonalityType()).
			getDeclareWarRefuseAttitudeThreshold())
		{
			return DENIAL_ATTITUDE;
		}
	}

	AttitudeTypes eAttitudeThem = AI_getAttitude(eTarget);
	for (MemberIter it(getID()); it.hasNext(); ++it)
	{
		if (eAttitudeThem > GC.getInfo(it->getPersonalityType()).
			getDeclareWarThemRefuseAttitudeThreshold())
		{
			return DENIAL_ATTITUDE_THEM;
		}
	}

	if (!atWar(eTarget, eSponsor))
	{
		if (GET_TEAM(eTarget).getNumNukeUnits() > 0)
		{	//return DENIAL_JOKING;
			return DENIAL_POWER_THEM; // advc.004g: Easier to understand
		}
	} // <advc.104o>
	if(getUWAI().isEnabled()) // (ignore bConsiderPower)
	{	/*	Refuse to start wars that we'll probably not engage in b/c we're busy
			fighting a closer enemy. Unless eTeam is already at war with eWarTeam.
			The main goal is to reduce the amount of messages generated by the
			war trade alert (advc.210a). */
		TeamTypes eClosestWarEnemy = NO_TEAM;
		int iHighestCloseness = MIN_INT;
		if(!GET_TEAM(eTarget).isAtWar(eSponsor))
		{
			for (TeamIter<MAJOR_CIV,ENEMY_OF> itEnemy(getID());
				itEnemy.hasNext(); ++itEnemy)
			{
				int iCloseness = AI_teamCloseness(itEnemy->getID(),
						DEFAULT_PLAYER_CLOSENESS,
						true, true); // bConstCache!
				if(iCloseness > iHighestCloseness)
				{
					iHighestCloseness = iCloseness;
					eClosestWarEnemy = itEnemy->getID();
				}
			}
		}
		if (eClosestWarEnemy != NO_TEAM)
		{
			/*  If any fighting occurred or recently declared, don't treat closeness
				as 0. (And don't be willing to attack teams with 0 closeness.) */
			if (iHighestCloseness <= 0 && (GET_TEAM(eClosestWarEnemy).
				AI_getWarPlan(getID()) == WARPLAN_ATTACKED_RECENT ||
				AI_getWarPlan(eClosestWarEnemy) == WARPLAN_ATTACKED_RECENT ||
				AI_getWarSuccess(eClosestWarEnemy) +
				GET_TEAM(eClosestWarEnemy).AI_getWarSuccess(getID()) >= 1))
			{
				iHighestCloseness = 1;
			}
			int iCloseness = AI_teamCloseness(eTarget, DEFAULT_PLAYER_CLOSENESS,
					true, true);
			if (iCloseness < iHighestCloseness)
				return DENIAL_TOO_MANY_WARS;
		}
		return uwai().declareWarTrade(
				GET_TEAM(eTarget).getMasterTeam(), eSponsor); // eTarget can be a (voluntary) vassal
	} // </advc.104o>
	// BETTER_BTS_AI_MOD, Diplomacy, 12/06/09, jdog5000: START
	if (AI_isAnyWarPlan())
		return DENIAL_TOO_MANY_WARS;
	// BETTER_BTS_AI_MOD: END
	return NO_DENIAL;
}


int CvTeamAI::AI_openBordersTradeVal(TeamTypes eTeam) const
{
	return (getNumCities() + GET_TEAM(eTeam).getNumCities());
}


DenialTypes CvTeamAI::AI_openBordersTrade(TeamTypes eWithTeam) const
{
	//PROFILE_FUNC(); // advc.003o
	FAssertMsg(eWithTeam != getID(), "shouldn't call this function on ourselves");

	if (isHuman() || isVassal(eWithTeam))
		return NO_DENIAL;

	/*if (AI_shareWar(eTeam))
		return NO_DENIAL;*/ // advc.124: Handled below

	if (AI_getMemoryCount(eWithTeam, MEMORY_CANCELLED_OPEN_BORDERS) > 0 &&
		!AI_shareWar(eWithTeam)) // advc.124
	{
		return DENIAL_RECENT_CANCEL;
	}
	if (AI_getWorstEnemy() == eWithTeam)
		return DENIAL_WORST_ENEMY;
	/*	<advc.124> If personalities are hidden, then avoid giving away
		attitude thresholds in the early game (i.e. when territory not yet
		located). Attitude is typically Cautious at that point, which should
		mean that everyone (except Toku) accepts OB if located and refuses
		otherwise. */
	int const iAttitudeThreshFloor =
			(GC.getGame().isOption(GAMEOPTION_RANDOM_PERSONALITIES) &&
			!AI_isTerritoryAccessible(eWithTeam) ?
			ATTITUDE_ANNOYED : NO_ATTITUDE); // </advc.124>
	int const iOurAttitude = AI_getAttitude(eWithTeam);
	for (MemberIter it(getID()); it.hasNext(); ++it)
	{
		// <advc.124>
		int const iAttitudeThresh = std::max(
				GC.getInfo(it->getPersonalityType()).
				getOpenBordersRefuseAttitudeThreshold(),
				iAttitudeThreshFloor);
		if (iOurAttitude < iAttitudeThresh)
			return DENIAL_ATTITUDE;
		if (iOurAttitude > iAttitudeThresh + 1)
			continue;
		{	/*	Attitude not where it needs to be, and no shared war
				(with accessible territory) either to make up for it. */
			if (iOurAttitude == iAttitudeThresh &&
				(!AI_shareWar(eWithTeam) || !AI_isTerritoryAccessible(eWithTeam)))
			{
				return DENIAL_ATTITUDE;
			}
			// Attitude just where it needs to be, but no territorial access.
			if (iOurAttitude == iAttitudeThresh + 1 &&
				!AI_isTerritoryAccessible(eWithTeam))
			{
				return DENIAL_NO_GAIN;
			}
		} // </advc.124>
	}

	return NO_DENIAL;
}

// advc.124:
bool CvTeamAI::AI_isTerritoryAccessible(TeamTypes eOwner) const
{
	PROFILE_FUNC(); // Hardly has gotten called in profiler tests so far
	bool bLandFound = false;
	// Check cities first in order to save time
	for (MemberIter itOwnerMember(eOwner); itOwnerMember.hasNext(); ++itOwnerMember)
	{
		FOR_EACH_CITY(pCity, *itOwnerMember)
		{
			if (pCity->isRevealed(getID()))
			{
				bLandFound = true;
				if (AI_isTerritoryAccessible(pCity->getPlot()))
					return true;
			}
		}
	}
	for (int i = 0; i < GC.getMap().numPlots(); i++)
	{
		CvPlot const& kPlot = GC.getMap().getPlotByIndex(i);
		if (kPlot.getTeam() == eOwner && kPlot.isRevealed(getID()) && !kPlot.isWater())
		{
			bLandFound = true;
			if (AI_isTerritoryAccessible(kPlot))
				return true;
		}
	}
	if (bLandFound)
	{
		/*	No trade connection. With the BtS unit roster, that already implies that
			units can't reach foreign shores, but let's not rely on that. */
		for (MemberAIIter itOurMember(getID()); itOurMember.hasNext(); ++itOurMember)
		{
			if (itOurMember->AI_isUnitNeedingOpenBorders(eOwner))
				return true;
		}
	}
	return false;
}

// advc.124: Helper function for the above
bool CvTeamAI::AI_isTerritoryAccessible(CvPlot const& kPlot) const
{
	FAssert(kPlot.isOwned() && kPlot.getTeam() != getID());
	/*	If it's in another area, then we need to be able
		to trade across water. */
	for (MemberIter itOurMember(getID()); itOurMember.hasNext(); ++itOurMember)
	{
		PlayerTypes const eOurMember = itOurMember->getID();
		if (kPlot.getArea().getCitiesPerPlayer(eOurMember) > 0)
			return true;
		if (itOurMember->getCapital() != NULL &&
			kPlot.getPlotGroup(eOurMember) ==
			itOurMember->getCapital()->getPlot().getPlotGroup(eOurMember))
		{
			return true;
		}
	}
	return false;
}


int CvTeamAI::AI_defensivePactTradeVal(TeamTypes eTeam) const
{
	// rfc: more dynamic value
	int iModifier = 280;
	if (isHasTech(ELECTRICITY) || isHasTech(ASSEMBLY_LINE))
		iModifier = 200;
	else if (GC.getGame().getGameTurn() > getTurnForYear(1920))
		iModifier = 160;

	// discount if in a chain of alliances but not directly allied yet
	// TODO: refactor
	for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	for (TeamIter<MAJOR_CIV,NOT_SAME_TEAM_AS> it(getID()); it.hasNext(); ++it)
	{
		if (it->isDefensivePact(eTeam) && it->isDefensivePact(getID()))
			iModifier -= 70;
	}
	int iNumCities = getNumCities() + GET_TEAM(eTeam).getNumCities();

	// doc: Amber Room effect
	if (GET_TEAM(eTeam).isHasBuildingEffect(AMBER_ROOM))
	{
		iModifier -= 60;

		if (GET_TEAM(eTeam).getNumCities() > getNumCities())
			iNumCities = 2 * getNumCities();
	}

	return iNumCities * std::max(iModifier, 10) / 100;
}


DenialTypes CvTeamAI::AI_defensivePactTrade(TeamTypes eWithTeam) const
{
	//PROFILE_FUNC(); // advc.003o
	FAssertMsg(eWithTeam != getID(), "shouldn't call this function on ourselves");

	if (isHuman())
		return NO_DENIAL;

	// rfc: war with friend
	for (TeamIter<MAJOR_CIV,NOT_SAME_TEAM_AS> it(getID()); it.hasNext(); ++it)
	{
		if (it->isAtWar(getID()) && it->isDefensivePact(eWithTeam))
			return DENIAL_JOKING;
		if (it->isAtWar(eWithTeam) && it->isDefensivePact(getID()))
			return DENIAL_JOKING;
	}

	// rfc: no world alliances until industrial era
	if (!AI_hasCitiesInPrimaryArea(eWithTeam) &&
		AI_calculateAdjacentLandPlots(eWithTeam) == 0 &&
		GET_PLAYER(GET_TEAM(eWithTeam).getLeaderID()).getCurrentEra() <= ERA_RENAISSANCE)
	{
		return DENIAL_TOO_FAR;
	}

	// TODO: subfunctions?
	// doc: collect all defensive pact partners and vassals in the possible coalition
	std::set<TeamTypes> partners;
	std::set<TeamTypes> vassals;

	std::set<TeamTypes> ourPartners = determineDefensivePactPartners(std::set<TeamTypes>());
	std::set<TeamTypes> theirPartners = GET_TEAM(eWithTeam).determineDefensivePactPartners(std::set<TeamTypes>());

	for (std::set<TeamTypes>::iterator it = ourPartners.begin(); it != ourPartners.end(); ++it)
		partners.insert(*it);

	for (std::set<TeamTypes>::iterator it = theirPartners.begin(); it != theirPartners.end(); ++it)
		partners.insert(*it);

	bool bBerlaymont = false;
	EraTypes eMaxEra = NO_ERA;
	int iMaxVassals = 0;
	for (std::set<TeamTypes>::iterator it = partners.begin(); it != partners.end(); ++it)
	{
		EraTypes eCurrentEra = GET_PLAYER(GET_TEAM(*it).getLeaderID()).getCurrentEra();
		if (eCurrentEra > eMaxEra)
			eMaxEra = eCurrentEra;

		if (GET_PLAYER(GET_TEAM(*it).getLeaderID()).isHasBuildingEffect(BERLAYMONT))
			bBerlaymont = true;

		int iNumVassals = 0;
		for (TeamIter<MAJOR_CIV> other; other.hasNext(); ++other)
		{
			if (other->isVassal(*it))
			{
				iNumVassals += 1;
				vassals.insert(other->getID());
			}
		}

		if (iNumVassals > iMaxVassals)
			iMaxVassals = iNumVassals;
	}

	// TODO: subfunction?
	// doc: determine defensive pact limit
	size_t iDefensivePactLimit = 2;
	if (eMaxEra >= ERA_INDUSTRIAL)
		iDefensivePactLimit += 1;
	if (eMaxEra >= ERA_GLOBAL)
		iDefensivePactLimit += 1;
	if (bBerlaymont)
		iDefensivePactLimit += 2;

	// doc: never more defensive pact partners than limit
	if (partners.size() > iDefensivePactLimit)
		return DENIAL_NO_GAIN;

	// doc: defensive pact partners and member with highest vassal count may not exceed twice the limit
	if (partners.size() + iMaxVassals > 2 * iDefensivePactLimit)
		return DENIAL_NO_GAIN;

	// doc: sum of defensive pact partners and half of all their vassals may not exceed twice the limit
	if (partners.size() + vassals.size() / 2 > 2 * iDefensivePactLimit)
		return DENIAL_NO_GAIN;

	//if (GC.getGame().countCivTeamsAlive() == 2)
	if (TeamIter<FREE_MAJOR_CIV>::count() <= 2) // advc.130t
		return DENIAL_NO_GAIN;
	// <kekm.3> (actually an advc change): Refuses/ cancels DP when ally makes peace
	if(!allWarsShared(eWithTeam))
		return DENIAL_JOKING; // </kekm.3>
	// <advc.130p>
	if(AI_getMemoryCount(eWithTeam, MEMORY_CANCELLED_DEFENSIVE_PACT) > 0)
		return DENIAL_RECENT_CANCEL; // </advc.130p>
	// <advc.130t>
	if(!isOpenBorders(eWithTeam))
		return DENIAL_JOKING; // </advc.130t>
	if (AI_getWorstEnemy() == eWithTeam)
		return DENIAL_WORST_ENEMY;

	int iAttitude = AI_getAttitude(eWithTeam);
	for (MemberIter it(getID()); it.hasNext(); ++it)
	{
		if (iAttitude <= GC.getInfo(it->getPersonalityType()).
				getDefensivePactRefuseAttitudeThreshold())
			return DENIAL_ATTITUDE;
	}
	return NO_DENIAL;
}


DenialTypes CvTeamAI::AI_permanentAllianceTrade(TeamTypes eWithTeam) const
{
	//PROFILE_FUNC(); // advc.003o
	FAssert(eWithTeam != getID());

	if (isHuman())
		return NO_DENIAL;

	if (AI_getWorstEnemy() == eWithTeam)
		return DENIAL_WORST_ENEMY;

	if (getPower(true) + GET_TEAM(eWithTeam).getPower(true) > GC.getGame().countTotalCivPower() / 2)
	{
		if (getPower(true) > GET_TEAM(eWithTeam).getPower(true))
			return DENIAL_POWER_US;
		return DENIAL_POWER_YOU;
	} // <advc.test>
	#if TEST_PERMANENT_ALLIANCES
	if (AI_getAttitude(eWithTeam) >= ATTITUDE_CAUTIOUS)
		return NO_DENIAL;
	#endif // </advc.test>
	if (AI_getDefensivePactCounter(eWithTeam) + AI_getShareWarCounter(eWithTeam) < 40)
		return DENIAL_NOT_ALLIED;

	int iAttitude = AI_getAttitude(eWithTeam);
	for (MemberIter it(getID()); it.hasNext(); ++it)
	{
		if (iAttitude <= GC.getInfo(it->getPersonalityType()).
				getPermanentAllianceRefuseAttitudeThreshold())
			return DENIAL_ATTITUDE;
	}

	return NO_DENIAL;
}


void CvTeamAI::AI_updateWorstEnemy(/* advc.130p: */ bool bUpdateTradeMemory)
{
	PROFILE_FUNC();

	// rfc
	if (isMinorCiv())
		return;

	// doc: limit power difference between worst enemies
	int iOurRank = GC.getGame().getTeamRank(getID());
	int iRankDifference = std::max(GC.getGame().countCivPlayersAlive() / 2, MAX_TEAMS / 5); // TODO: max teams?

	TeamTypes eBestTeam = NO_TEAM;
	int iBestValue = AI_enmityValue(m_eWorstEnemy);
	if(iBestValue > 0)
	{
		eBestTeam = m_eWorstEnemy;
		/*  advc.130p: Inertia; to reduce oscillation. New worst enemy has to be
			strictly worse than current minus 1.
			Oscillation is already a problem in BtS, but changes in CvPlayerAI::
			AI_getRivalTradeAttitude (penalty for OB) make it worse.
			Inertia could lead to a situation where we're only Annoyed against
			the worst enemy, but Furious towards another civ, but flip-flopping
			between the two would be even worse. */
		iBestValue++;
	}
	for (TeamIter<MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> it(getID()); it.hasNext(); ++it)
	{
		TeamTypes const eLoopTeam = it->getID();
		// <advc.130p>
		if(eLoopTeam == m_eWorstEnemy) // No need to evaluate this one twice
			continue;
		// doc: limit power difference between worst enemies
		if (std::abs(GC.getGame().getTeamRank(eLoopTeam) - iOurRank) > iRankDifference)
			continue;
		// Moved into new function
		int iValue = AI_enmityValue(eLoopTeam);

		// doc: distance impacts enmity value
		if (GET_PLAYER(it->getLeaderID()).isNeighbor(getLeaderID()))
			iValue *= 2;
		else if (GET_PLAYER(it->getLeaderID()).isDistant(getLeaderID()))
		{
			iValue *= 2;
			iValue /= 5;
		}

		if(iValue > iBestValue) // Now computes a maximum // </advc.130p>
		{
			iBestValue = iValue;
			eBestTeam = eLoopTeam;
		}
	}
	// <advc.130p>
	if (eBestTeam == m_eWorstEnemy)
		return;
	if (bUpdateTradeMemory && m_eWorstEnemy != NO_TEAM)
	{
		bool bUpdateWorstEnemyAgain = false;
		for (TeamIter<MAJOR_CIV,OTHER_KNOWN_TO> it(getID()); it.hasNext(); ++it)
		{
			TeamTypes const eOther = it->getID();
			if(eOther == m_eWorstEnemy) // The old enemy can't have traded with itself
				continue;
			int iOldGrantVal = AI_getEnemyPeacetimeGrantValue(eOther);
			int iOldTradeVal = AI_getEnemyPeacetimeTradeValue(eOther);
			if (iOldGrantVal == 0 && iOldTradeVal == 0)
				continue;
			// Relations with tentative new worst enemy may improve here
			bUpdateWorstEnemyAgain = (eOther == eBestTeam);
			AI_setEnemyPeacetimeGrantValue(eOther, (2 * iOldGrantVal) / 3);
			AI_setEnemyPeacetimeTradeValue(eOther, (2 * iOldTradeVal) / 3);
		}
		if (bUpdateWorstEnemyAgain)
		{
			AI_updateWorstEnemy(false);
			return;
		}
	}
	m_eWorstEnemy = eBestTeam;
	/*  Changing EnemyPeacetime values updates the attitude cache, but that's
		still based on the old worst enemy. Need another update vs. everyone
		(anyone could have OB with the new enemy).
		Don't update worst enemy again after that. */
	for (TeamIter<MAJOR_CIV,OTHER_KNOWN_TO> it(getID()); it.hasNext(); ++it)
		AI_updateAttitude(it->getID(), false);
	// </advc.130p>
}

// <advc.130p>
/*	Conditions for enemy trade moved into a separate function b/c they're getting
	more complicated and so that other AI code can anticipate enemy trade penalties
	(will use this for advc.ctr). */
scaled CvTeamAI::AI_enemyTradeResentmentFactor(TeamTypes eTo, TeamTypes eFrom,
	TeamTypes eWarTradeTarget, TeamTypes ePeaceTradeTarget, bool bPeaceDeal) const
{
	bool const bToWorstEnemy = (AI_getWorstEnemy() == eTo);
	// Special treatment for war enemies trading among each other
	bool const bWarWithFromTeam = (isAtWar(eFrom) || eWarTradeTarget == getID());
	bool const bWarWithToTeam = isAtWar(eTo);
	if(!bToWorstEnemy && !(bWarWithToTeam && !bWarWithFromTeam))
		return 0;
	// No anger among vassal-master when they make peace
	if (bPeaceDeal && GET_TEAM(eFrom).getMasterTeam() == getID())
		return 0;
	if (ePeaceTradeTarget == getMasterTeam() ||
		/*  Don't mind if our worst enemy is paid to make peace with a team
			that we like -- unless we're at war with our worst enemy because,
			then, the peace deals means that we lose a war ally. */
		(ePeaceTradeTarget != NO_TEAM && !bWarWithToTeam &&
		AI_getAttitude(ePeaceTradeTarget) >= ATTITUDE_PLEASED &&
		// Should be implied by attitude, but let's make sure.
		!isAtWar(ePeaceTradeTarget)))
	{
		return 0;
	}
	/*  Avoid oscillation of worst enemy, but still punish non-war party
		for helping a war enemy. */
	int iAttitudeDiff = ::range(
			AI_getAttitudeVal(eFrom) - (bWarWithFromTeam ? 2 : 0) -
			(AI_getAttitudeVal(AI_getWorstEnemy()) - (bWarWithToTeam ? 2 : 0)),
			0, 7);
	scaled r(iAttitudeDiff, 5);
	if (bPeaceDeal) // But count brokered peace in full
		r *= fixp(0.4);
	if (bWarWithToTeam && bToWorstEnemy && !bWarWithFromTeam)
		r *= fixp(4/3.);
	else if (bToWorstEnemy && !bWarWithFromTeam)
		r *= fixp(0.9);
	else r *= fixp(2/3.);
	return r;
}


int CvTeamAI::AI_enmityValue(TeamTypes eEnemy) const
{
	if(eEnemy == NO_TEAM)
		return 0;
	CvTeam const& kEnemy = GET_TEAM(eEnemy);
	FAssert(eEnemy != getID() && !kEnemy.isMinorCiv() && kEnemy.isHasMet(getID()));
	// advc.148: Rather than RELATIONS_THRESH_ANNOYED
	int const iAttitudeThresh = GC.getDefineINT(CvGlobals::RELATIONS_THRESH_WORST_ENEMY);
	if (!kEnemy.isAlive() ||
		kEnemy.isCapitulated() || // advc.130d
		((AI_getAttitudeVal(eEnemy) > iAttitudeThresh ||
		AI_getAttitudeVal(eEnemy, false) > iAttitudeThresh) && // advc.130d
		!isAtWar(eEnemy)))
	{
		return 0;
	}
	int iR = 100 - AI_getAttitudeVal(eEnemy);
	if(isAtWar(eEnemy) && AI_getWarPlan(eEnemy) != WARPLAN_DOGPILE)
		iR += 100;
	return iR;
} // </advc.130p>


void CvTeamAI::AI_setWarPlanStateCounter(TeamTypes eIndex, int iNewValue)
{
	m_aiWarPlanStateCounter.set(eIndex, iNewValue);
	FAssert(AI_getWarPlanStateCounter(eIndex) >= 0);
}


void CvTeamAI::AI_changeWarPlanStateCounter(TeamTypes eIndex, int iChange)
{
	AI_setWarPlanStateCounter(eIndex, (AI_getWarPlanStateCounter(eIndex) + iChange));
}


void CvTeamAI::AI_setAtWarCounter(TeamTypes eIndex, int iNewValue)
{
	m_aiAtWarCounter.set(eIndex, iNewValue);
	FAssert(AI_getAtWarCounter(eIndex) >= 0);
}


void CvTeamAI::AI_changeAtWarCounter(TeamTypes eIndex, int iChange)
{
	AI_setAtWarCounter(eIndex, (AI_getAtWarCounter(eIndex) + iChange));
}


void CvTeamAI::AI_setAtPeaceCounter(TeamTypes eIndex, int iNewValue)
{
	m_aiAtPeaceCounter.set(eIndex, iNewValue);
	FAssert(AI_getAtPeaceCounter(eIndex) >= 0);
}


void CvTeamAI::AI_changeAtPeaceCounter(TeamTypes eIndex, int iChange)
{
	AI_setAtPeaceCounter(eIndex, (AI_getAtPeaceCounter(eIndex) + iChange));
}


void CvTeamAI::AI_setHasMetCounter(TeamTypes eIndex, int iNewValue)
{
	m_aiHasMetCounter.set(eIndex, iNewValue);
	FAssert(AI_getHasMetCounter(eIndex) >= 0);
}


void CvTeamAI::AI_changeHasMetCounter(TeamTypes eIndex, int iChange)
{
	AI_setHasMetCounter(eIndex, (AI_getHasMetCounter(eIndex) + iChange));
}


void CvTeamAI::AI_setOpenBordersCounter(TeamTypes eIndex, int iNewValue)
{
	m_aiOpenBordersCounter.set(eIndex, iNewValue);
	FAssert(AI_getOpenBordersCounter(eIndex) >= 0);
}


void CvTeamAI::AI_changeOpenBordersCounter(TeamTypes eIndex, int iChange)
{
	AI_setOpenBordersCounter(eIndex, (AI_getOpenBordersCounter(eIndex) + iChange));
}


void CvTeamAI::AI_setDefensivePactCounter(TeamTypes eIndex, int iNewValue)
{
	m_aiDefensivePactCounter.set(eIndex, iNewValue);
	FAssert(AI_getDefensivePactCounter(eIndex) >= 0);
}


void CvTeamAI::AI_changeDefensivePactCounter(TeamTypes eIndex, int iChange)
{
	AI_setDefensivePactCounter(eIndex, (AI_getDefensivePactCounter(eIndex) + iChange));
}


void CvTeamAI::AI_setShareWarCounter(TeamTypes eIndex, int iNewValue)
{
	m_aiShareWarCounter.set(eIndex, iNewValue);
	FAssert(AI_getShareWarCounter(eIndex) >= 0);
}


void CvTeamAI::AI_changeShareWarCounter(TeamTypes eTeam, int iChange)
{
	AI_setShareWarCounter(eTeam, AI_getShareWarCounter(eTeam) + iChange);
}


void CvTeamAI::AI_setWarSuccess(TeamTypes eTeam, scaled rNewValue)
{
	m_arWarSuccess.set(eTeam, rNewValue);
	FAssert(AI_getWarSuccess(eTeam) >= 0);
}

// advc:
scaled CvTeamAI::AI_countEnemyWarSuccess() const
{
	scaled r;
	for (TeamAIIter<CIV_ALIVE,ENEMY_OF> itEnemy(getID());
		itEnemy.hasNext(); ++itEnemy)
	{
		r += itEnemy->AI_getWarSuccess(getID());
	}
	return r;
}


void CvTeamAI::AI_changeWarSuccess(TeamTypes eTeam, scaled rChange)
{
	AI_setWarSuccess(eTeam, AI_getWarSuccess(eTeam) + rChange);
	// <advc.130m>
	if (rChange <= 0 || eTeam == BARBARIAN_TEAM || isBarbarian())
		return;
	std::vector<CvTeamAI*> apAffectedTeams;
	for (TeamAIIter<MAJOR_CIV> it; it.hasNext(); ++it)
	{
		CvTeamAI& kWarAlly = *it;
		if (eTeam == kWarAlly.getID() || kWarAlly.getID() == getID())
			continue;
		// Let our allies know that we've had a war success
		if (kWarAlly.isAtWar(eTeam) && !kWarAlly.isAtWar(getID()))
		{
			kWarAlly.AI_reportSharedWarSuccess(rChange, getID(), eTeam);
			apAffectedTeams.push_back(&kWarAlly);
		}
		/*  Let the allies of our enemy know that their ally has suffered a loss
			from us, their shared enemy */
		if (!kWarAlly.isAtWar(eTeam) && kWarAlly.isAtWar(getID()))
		{
			kWarAlly.AI_reportSharedWarSuccess(rChange, eTeam, getID());
			apAffectedTeams.push_back(&kWarAlly);
		}
	}
	// Attitude cache update; also relevant for WarAttitude (advc.sha).
	/*	To save time. Not crucial to keep AI attitude up to date during AI turns.
		Note that network games are treated as never being in between turns. */
	if (!GC.getGame().isInBetweenTurns() &&
		(isHuman() || GET_TEAM(eTeam).isHuman()))
	{
		apAffectedTeams.push_back(&GET_TEAM(eTeam));
		apAffectedTeams.push_back(this);
		for (size_t i = 0; i < apAffectedTeams.size(); i++)
		{
			for (size_t j = 0; j < apAffectedTeams.size(); j++)
			{
				if (i != j)
					apAffectedTeams[i]->AI_updateAttitude(apAffectedTeams[j]->getID());
			}
		}
	}
}

/*  eEnemy is a war enemy that this team and eWarAlly have in common.
	Either eWarAlly has inflicted a war success on eEnemy or vice versa.
	This team is being informed about the war success, and
	rIntensity says how significant the war success was. */
void CvTeamAI::AI_reportSharedWarSuccess(scaled rIntensity, TeamTypes eWarAlly,
	TeamTypes eEnemy, // (doesn't currently matter)
	// True means: don't check if this team needs the assistance
	bool bIgnoreDistress)
{
	/*  War success against us as a measure of how distressed we are, i.e. how
		much we need the assistance from agentId. Counts all our enemies,
		not just enemyId. */
	scaled rDistress;
	scaled const rMaxDistress(GC.getWAR_SUCCESS_CITY_CAPTURING(), 5);
	if (getNumCities() > 0)
	{
		if (bIgnoreDistress) // Not "ignored", I guess, but computed differently.
			rDistress = rMaxDistress / scaled(getNumCities(), 2).ceil();
		else
		{
			for (TeamAIIter<MAJOR_CIV,ENEMY_OF> itEnemy(getID());
				itEnemy.hasNext(); ++itEnemy)
			{
				rDistress += itEnemy->AI_getWarSuccess(getID());
			}
			rDistress /= getNumCities();
		}
	}
	/*  Don't give distress too much weight. It's mostly there to discount
		unwelcome assistance when allies just snatch away our loot.
		Assuming that killing the defenders in a city results in about as much
		war success as taking the city itself, the highest possible distress is
		2 * WAR_SUCCESS_CITY_CAPTURING * NumCities. If our distress is just 10%
		of that, the distress multiplier already takes its maximal value. */
	rDistress = std::min(rDistress, rMaxDistress);
	int iOldValue = AI_getSharedWarSuccess(eWarAlly);
	// Asymptote at 5000
	scaled rBrakeFactor = scaled::max(0, 1 - scaled(iOldValue, 5000));
	int const iPrecision = 100; // Precision of what we'll store (in an int)
	int iNewValue = iOldValue +
			((rBrakeFactor * iPrecision * rDistress * rIntensity) /
			/*  Use number of cities as an indicator of how capable the war ally is
				militarily - how difficult was this war success to accomplish, or
				how big a sacrifice was the loss. */
			std::max(1, GET_TEAM(eWarAlly).getNumCities())).round();
	FAssert(iNewValue >= iOldValue);
	AI_setSharedWarSuccess(eWarAlly, iNewValue);
}


void CvTeamAI::AI_setSharedWarSuccess(TeamTypes eWarAlly, int iWS)
{
	m_aiSharedWarSuccess.set(eWarAlly, iWS);
} // </advc.130m>


void CvTeamAI::AI_setEnemyPeacetimeTradeValue(TeamTypes eIndex, int iNewValue,
	bool bUpdateAttitude) // advc.130p
{
	m_aiEnemyPeacetimeTradeValue.set(eIndex, iNewValue);
	FAssert(AI_getEnemyPeacetimeTradeValue(eIndex) >= 0);
	if (bUpdateAttitude) // advc.130p
		AI_updateAttitude(eIndex, /* advc.130e: */ false); // K-Mod
}


void CvTeamAI::AI_changeEnemyPeacetimeTradeValue(TeamTypes eIndex, int iChange,
	bool bUpdateAttitude) // advc.130p
{
	AI_setEnemyPeacetimeTradeValue(eIndex, AI_getEnemyPeacetimeTradeValue(eIndex) + iChange,
			bUpdateAttitude); // advc.130p
}

// <advc.130p>, advc.130m To keep the rate consistent between TeamAI and PlayerAI
scaled CvTeamAI::AI_getDiploDecay() const
{
	/*  On Normal speed, this decay rate halves a value in about 50 turns:
		0.9865^50 = 0.507 */
	return fixp(1.45) / GC.getInfo(GC.getGame().getGameSpeedType()).get(
			CvGameSpeedInfo::AIMemoryRandPercent); // advc.130r
}

// Needed for both RivalTrade and "fair trade"
scaled CvTeamAI::AI_recentlyMetMultiplier(TeamTypes eOther) const
{
	scaled rRecency = scaled::min(1, scaled(
			AI_getHasMetCounter(eOther),
			GC.getInfo(GC.getGame().getGameSpeedType()).getResearchPercent()));
	// +50% if just met, declining linearly to +0% if met 100 turns ago (Normal speed)
	return 1 + (1 - rRecency) / 2;
} // </advc.130p>


void CvTeamAI::AI_setEnemyPeacetimeGrantValue(TeamTypes eIndex, int iNewValue,
	bool bUpdateAttitude) // advc.130p
{
	m_aiEnemyPeacetimeGrantValue.set(eIndex, iNewValue);
	FAssert(AI_getEnemyPeacetimeGrantValue(eIndex) >= 0);
	if (bUpdateAttitude) // advc.130p
		AI_updateAttitude(eIndex, /* advc.130e: */ false); // K-Mod
}


void CvTeamAI::AI_changeEnemyPeacetimeGrantValue(TeamTypes eIndex, int iChange,
	bool bUpdateAttitude) // advc.130p
{
	AI_setEnemyPeacetimeGrantValue(eIndex, AI_getEnemyPeacetimeGrantValue(eIndex) + iChange,
			bUpdateAttitude); // advc.130p
}

// advc.003u: Moved from CvTeam
int CvTeamAI::AI_countEnemyPowerByArea(CvArea const& kArea) const
{
	int iCount = 0;
	for (PlayerIter<ALIVE,KNOWN_POTENTIAL_ENEMY_OF> it(getID()); it.hasNext(); ++it)
	{
		CvPlayer const& kEnemy = *it;
		//if (isAtWar(GET_PLAYER((PlayerTypes)iI).getTeam()))
		// BETTER_BTS_AI_MOD, General AI, 01/11/09, jdog5000: Count planned wars as well
		if (AI_getWarPlan(kEnemy.getTeam()) != NO_WARPLAN)
			iCount += kArea.getPower(kEnemy.getID());
	}
	return iCount;
}

// K-Mod: (Note: this includes barbarian cities.)
int CvTeamAI::AI_countEnemyCitiesByArea(CvArea const& kArea) const // advc.003u: Moved from CvTeam
{
	int iCount = 0;
	for (PlayerIter<ALIVE,KNOWN_POTENTIAL_ENEMY_OF> it(getID()); it.hasNext(); ++it)
	{
		CvPlayer const& kEnemy = *it;
		if (AI_getWarPlan(kEnemy.getTeam()) != NO_WARPLAN)
			iCount += kArea.getCitiesPerPlayer(kEnemy.getID());
	}
	return iCount; // advc.001: was 'return 0'
}

// BETTER_BTS_AI_MOD, War strategy AI, 05/19/10, jdog5000:
// advc: Moved from CvTeam
int CvTeamAI::AI_countEnemyDangerByArea(CvArea const& kArea, TeamTypes eEnemyTeam) const
{
	PROFILE_FUNC();
	int iCount = 0;
	FOR_EACH_ENUM(PlotNum)
	{
		CvPlot const& kPlot = GC.getMap().getPlotByIndex(eLoopPlotNum);
		if (kPlot.isArea(kArea) && kPlot.getTeam() == getID())
		{
			iCount += kPlot.plotCount(PUF_canDefendEnemy, getLeaderID(),
					false, NO_PLAYER, eEnemyTeam, PUF_isVisible, getLeaderID());
		}
	}
	return iCount;
}

// BETTER_BTS_AI_MOD, War strategy AI, 04/01/10, jdog5000: START
// advc.003j (comment): unused; advc: moved from CvTeam
int CvTeamAI::AI_countEnemyPopulationByArea(CvArea const& kArea) const
{
	int iCount = 0;
	for (PlayerIter<ALIVE,KNOWN_POTENTIAL_ENEMY_OF> it(getID()); it.hasNext(); ++it)
	{
		CvPlayer const& kEnemy = *it;
		if (AI_getWarPlan(kEnemy.getTeam()) != NO_WARPLAN)
			iCount += kArea.getPopulationPerPlayer(kEnemy.getID());
	}
	return iCount;
} // BETTER_BTS_AI_MOD: END

// advc: Body cut from the deleted CvTeam::getChosenWarCount. Never called, not from Python either.
int CvTeamAI::AI_countChosenWars(bool bIgnoreMinors) const
{
	int iCount = 0;
	for (TeamIter<CIV_ALIVE,KNOWN_POTENTIAL_ENEMY_OF> it(getID()); it.hasNext(); ++it)
	{
		CvTeam const& kEnemy = *it;
		if (bIgnoreMinors && kEnemy.isMinorCiv())
			continue;

		if (AI_isChosenWar(kEnemy.getID()))
			iCount++;
	}
	return iCount;
}


bool CvTeamAI::AI_isChosenWar(TeamTypes eIndex) const
{
	return (AI_isChosenWarPlan( // advc.105: Code moved into AI_isChosenWarPlan
			AI_getWarPlan(/* advc.104j: */ GET_TEAM(eIndex).getMasterTeam())));
}

// advc.105: Body cut from AI_isChosenWar
bool CvTeamAI::AI_isChosenWarPlan(WarPlanTypes eWarPlanType)
{
	switch(eWarPlanType)
	{
	case WARPLAN_ATTACKED_RECENT:
	case WARPLAN_ATTACKED:
		return false;
	case WARPLAN_PREPARING_LIMITED:
	case WARPLAN_PREPARING_TOTAL:
	case WARPLAN_LIMITED:
	case WARPLAN_TOTAL:
	case WARPLAN_DOGPILE:
		return true;
	default: return false; // NO_WARPLAN
	}
}

// advc.105:
bool CvTeamAI::AI_isAnyChosenWar() const
{
	FOR_EACH_ENUM(WarPlan)
	{
		if (AI_isChosenWarPlan(eLoopWarPlan) && AI_getNumWarPlans(eLoopWarPlan) > 0)
			return true;
	}
	return false;
}

/*  advc: Body based on the deleted CvTeam::getWarPlanCount. (War plans are an AI thing.)
	NUM_WARPLAN_TYPES causes all war plans (except NO_WARPLAN) to be counted.
	Barbarians and vassals are never counted. (BtS had counted vassals.) */
int CvTeamAI::AI_countWarPlans(WarPlanTypes eWarPlanType, bool bIgnoreMinors, unsigned int iMaxCount) const
{
	FAssertMsg(!bIgnoreMinors || eWarPlanType == NO_WARPLAN || iMaxCount != MAX_PLAYERS ||
			(eWarPlanType == NUM_WARPLAN_TYPES && iMaxCount > 1),
			"Should use getNumWarPlans or isAnyWarPlan instead (faster)");
	int r = 0;
	for (TeamIter<CIV_ALIVE> it; it.hasNext(); ++it)
	{
		CvTeam const& kTarget = *it;
		if (kTarget.isAVassal())
			continue;
		if (bIgnoreMinors && kTarget.isMinorCiv())
			continue;
		WarPlanTypes eLoopWarPlanType = AI_getWarPlan(kTarget.getID());
		if (eWarPlanType == NUM_WARPLAN_TYPES ?
				(eLoopWarPlanType != NO_WARPLAN) :
				(eLoopWarPlanType == eWarPlanType))
			r++;
		if (r >= (int)iMaxCount)
			return r;
	}
	FAssert(eWarPlanType != NUM_WARPLAN_TYPES || r >= getNumWars(bIgnoreMinors, true));
	return r;
}


bool CvTeamAI::AI_isSneakAttackReady(TeamTypes eIndex) const
{
	//return (AI_isChosenWar(eIndex) && !(AI_isSneakAttackPreparing(eIndex))); // BtS
	// K-Mod (advc: originally in an overloaded function)
	if(eIndex != NO_TEAM)
		return !isAtWar(eIndex) && AI_isChosenWar(eIndex) && !AI_isSneakAttackPreparing(eIndex); // K-Mod
	for (TeamIter<MAJOR_CIV> it; it.hasNext(); ++it)
	{
		if (AI_isSneakAttackReady(it->getID()))
			return true;
	}
	return false;
	// K-Mod end
}


bool CvTeamAI::AI_isSneakAttackPreparing(TeamTypes eIndex) const
{
	if(eIndex != NO_TEAM)
	{
		WarPlanTypes eWarPlan = AI_getWarPlan(GET_TEAM(eIndex).getMasterTeam()); // advc.104j
		return (eWarPlan == WARPLAN_PREPARING_LIMITED || eWarPlan == WARPLAN_PREPARING_TOTAL);
	}
	for (TeamIter<MAJOR_CIV> it; it.hasNext(); ++it)
	{
		if (AI_isSneakAttackPreparing(it->getID()))
			return true;
	}
	return false;
}


void CvTeamAI::AI_setWarPlan(TeamTypes eTarget, WarPlanTypes eNewValue, bool bWar)
{
	FAssertBounds(0, MAX_TEAMS, eTarget);
	FAssert(eTarget != getID() || eNewValue == NO_WARPLAN); // advc: Moved from AI_getWarPlan
	WarPlanTypes const eOldValue = AI_getWarPlan(eTarget);
	if (eOldValue == eNewValue || (!bWar && isAtWar(eTarget)))
		return;
	AI_updateWarPlanCounts(eTarget, m_aeWarPlan.get(eTarget), eNewValue); // advc.opt
	m_aeWarPlan.set(eTarget, eNewValue);
	AI_setWarPlanStateCounter(eTarget, 0);
	// <advc.104d> Make per-area targets dirty
	if (eNewValue != WARPLAN_PREPARING_LIMITED && eNewValue != WARPLAN_PREPARING_TOTAL &&
		(eNewValue != NO_WARPLAN ||
		eOldValue != WARPLAN_PREPARING_LIMITED && eOldValue != WARPLAN_PREPARING_TOTAL))
	{
		for (MemberAIIter itMember(getID()); itMember.hasNext(); ++itMember)
			itMember->AI_setCityTargetTimer(0);
	} // </advc.104d>
	AI_updateAreaStrategies();
	for (MemberAIIter itMember(getID()); itMember.hasNext(); ++itMember)
	{
		if (!itMember->isHuman())
			itMember->AI_makeProductionDirty();
	}
	// <advc.104j>
	if (isHuman()) // Human has to instruct vassals manually
		return;
	WarPlanTypes eVassalWP = NO_WARPLAN;
	if (eNewValue == NO_WARPLAN)
		eVassalWP = NO_WARPLAN;
	else if(eNewValue == WARPLAN_PREPARING_LIMITED || eNewValue == WARPLAN_PREPARING_TOTAL)
		eVassalWP = WARPLAN_PREPARING_LIMITED;
	else return;

	for (TeamAIIter<ALIVE,VASSAL_OF> it(getID()); it.hasNext(); ++it)
	{
		CvTeamAI& kOurAIVassal = *it;
		if (!kOurAIVassal.isHuman() &&
			// Don't set NO_WARPLAN before the vassal has been set to !isAtWar
			(eVassalWP != NO_WARPLAN || !kOurAIVassal.isAtWar(eTarget)))
		{
			kOurAIVassal.AI_setWarPlan(eTarget, eVassalWP);
		}
	} // </advc.104j>
}

/*	advc.opt: Replacing global isPotentialEnemy (CvGameCoreUtils). Not much faster here -
	mostly avoids some NO_TEAM checks -, but also makes more sense as a CvTeamAI member.
	I've also redirected some CvUnitAI::AI_isPotentialEnemy calls here. That function
	allows alwaysHostile units to attack w/o war plan; this function doesn't. */
bool CvTeamAI::AI_mayAttack(TeamTypes eDefender) const
{
	if (isAtWar(eDefender))
		return true;
	TeamTypes const eDefenderMaster = GET_TEAM(eDefender).getMasterTeam(); // advc.104j
	//if (!AI_isSneakAttackReady(eDefender))
	// advc.opt: Avoid isAtWar and NO_TEAM check
	if (!AI_isImminentWarPlan(AI_getWarPlan(/* advc.104j: */ eDefenderMaster)))
		return false;
	// (War w/ eDefenderMaster and peace w/ eDefender can happen while resolving DoW)
	FAssertMsg(!isAVassal() || isAtWar(eDefenderMaster), "Vassal shouldn't have imminent undeclared war plan");
	/*	UNOFFICIAL_PATCH, Bugfix, General AI, 05/05/09, jdog5000: START
		Fixes bug where AI would launch invasion while unable to declare war
		which caused units to be bumped once forced peace expired */
	//return canDeclareWar(eDefender);
	/*	advc.opt: Avoid the canEventuallyDeclareWar check - the war plan
		has to be abandoned if we can't ever declare. */
	return (!isForcePeace(eDefenderMaster) && // advc.104j
			!isForcePeace(eDefender));
}

// advc: Replacing K-Mod's CvPlot::isVisiblePotentialEnemyUnit
bool CvTeamAI::AI_mayAttack(CvPlot const& kPlot) const
{
	/*	Unfortunately, PUF_isPotentialEnemy requires a PlayerTypes argument.
		Would have to change several PUF... signatures to remedy that. */
	PlayerTypes const ePlayer = getLeaderID();
	// <K-Mod>
	return (kPlot.plotCheck(PUF_isPotentialEnemy, ePlayer, false,
			NO_PLAYER, NO_TEAM, PUF_isVisible, ePlayer) != NULL); // </K-Mod>
}

// BETTER_BTS_AI_MOD, General AI, 07/20/09, jdog5000: START
/*  advc: Moved these two functions from CvTeam and refactored them
	(they were using a loop instead of getMasterTeam) */
bool CvTeamAI::AI_isMasterPlanningLandWar(CvArea const& kArea) const
{
	if (!isAVassal())
		return false;
	AreaAITypes eAreaAI = kArea.getAreaAIType(getID());
	if (eAreaAI == AREAAI_OFFENSIVE || eAreaAI == AREAAI_DEFENSIVE || eAreaAI == AREAAI_MASSING)
		return true;

	CvTeamAI const& kMaster = GET_TEAM(getMasterTeam());
	if (kMaster.AI_isAnyWarPlan())
	{
		AreaAITypes eMasterAreaAI = kArea.getAreaAIType(kMaster.getID());
		if (eMasterAreaAI == AREAAI_OFFENSIVE || eMasterAreaAI == AREAAI_DEFENSIVE ||
			eMasterAreaAI == AREAAI_MASSING)
		{
			return true;
		}
		else if (eMasterAreaAI == AREAAI_NEUTRAL)
		{	// Master has no presence here
			if (kArea.getNumCities() - countNumCitiesByArea(kArea) > 2)
				return SyncRandOneChanceIn(isCapitulated() ? 6 : 4);
		}
	}
	else if (kMaster.isHuman())
	{
		static bool const bBBAI_HUMAN_VASSAL_WAR_BUILD = GC.getDefineBOOL("BBAI_HUMAN_VASSAL_WAR_BUILD");
		if (bBBAI_HUMAN_VASSAL_WAR_BUILD &&
			kArea.getNumCities() - countNumCitiesByArea(kArea) -
			kMaster.countNumCitiesByArea(kArea) > 2)
		{
			return SyncRandOneChanceIn(4);
		}
	}
	return false;
}


bool CvTeamAI::AI_isMasterPlanningSeaWar(CvArea const& kArea) const
{
	if (!isAVassal())
		return false;
	AreaAITypes eAreaAI = kArea.getAreaAIType(getID());
	if (eAreaAI == AREAAI_ASSAULT || eAreaAI == AREAAI_ASSAULT_ASSIST ||
		eAreaAI == AREAAI_ASSAULT_MASSING)
	{
		return true;
	}
	CvTeamAI const& kMaster = GET_TEAM(getMasterTeam());
	if (kMaster.AI_isAnyWarPlan())
	{
		AreaAITypes eMasterAreaAI = kArea.getAreaAIType(kMaster.getID());
		if (eMasterAreaAI == AREAAI_ASSAULT || eMasterAreaAI == AREAAI_ASSAULT_ASSIST ||
			eMasterAreaAI == AREAAI_ASSAULT_MASSING)
		{
			return SyncRandOneChanceIn(isCapitulated() ? 3 : 2);
		}
	}
	return false;
} // BETTER_BTS_AI_MOD: END

// advc.104:
void CvTeamAI::AI_setWarPlanNoUpdate(TeamTypes eIndex, WarPlanTypes eNewValue)
{
	FAssertBounds(0, MAX_TEAMS, eIndex);
	AI_updateWarPlanCounts(eIndex, m_aeWarPlan.get(eIndex), eNewValue); // advc.opt
	m_aeWarPlan.set(eIndex, eNewValue);
}

// advc.opt:
void CvTeamAI::AI_updateWarPlanCounts(TeamTypes eTarget, WarPlanTypes eOldPlan, WarPlanTypes eNewPlan)
{
	if (eTarget == BARBARIAN_TEAM || eOldPlan == eNewPlan)
		return;
	CvTeam const& kTarget = GET_TEAM(eTarget);
	// (Don't exclude dead teams - CvTeam::changeAliveCount will set NO_WARPLAN for those.)
	if (kTarget.isMinorCiv() || kTarget.isAVassal())
		return;
	if (eOldPlan != NO_WARPLAN)
		m_aiWarPlanCounts.add(eOldPlan, -1);
	if (eNewPlan != NO_WARPLAN)
	{
		m_aiWarPlanCounts.add(eNewPlan, 1);
		m_bAnyWarPlan = true;
		return;
	}
	FOR_EACH_ENUM(WarPlan)
	{
		if (m_aiWarPlanCounts.get(eLoopWarPlan) > 0)
		{
			m_bAnyWarPlan = true;
			return;
		}
	}
	m_bAnyWarPlan = false;
}

// <advc.650>
void CvTeamAI::AI_rememberNukeExplosion(CvPlot const& kPlot)
{
	m_aeNukeExplosions.push_back(kPlot.plotNum());
}


bool CvTeamAI::AI_wasRecentlyNuked(CvPlot const& kPlot) const
{
	return (std::find(
			m_aeNukeExplosions.begin(), m_aeNukeExplosions.end(), kPlot.plotNum()) !=
			m_aeNukeExplosions.end());
}  // </advc.650>

/*	if this number is over 0 the teams are "close"
	this may be expensive to run, kinda O(N^2)... */
int CvTeamAI::AI_teamCloseness(TeamTypes eIndex, int iMaxDistance,
	bool bConsiderLandTarget, // advc.104o
	bool bConstCache) const // advc.001n
{
	//PROFILE_FUNC(); // advc.003o (the cache seems to be very effective)
	FAssert(eIndex != getID());
	int iValue = 0;
	for (MemberAIIter itOurMember(getID()); itOurMember.hasNext(); ++itOurMember)
	{
		for (MemberIter itTheirMember(eIndex); itTheirMember.hasNext(); ++itTheirMember)
		{
			iValue += itOurMember->AI_playerCloseness(itTheirMember->getID(), iMaxDistance,
					bConstCache); // advc.001n
		}
	} /* <advc.104o> (Change disabled for now b/c advc.107 now factors
		land connection into AI_playerCloseness. Could increase iValue here
		in order to further increase the impact.) */
	/*if(bConsiderLandTarget && AI_isLandTarget(eIndex))
		iValue += 50; */ // </advc.104o>
	return iValue;
}


void CvTeamAI::read(FDataStreamBase* pStream)
{
	CvTeam::read(pStream);
	// <advc.104>
	if ((getUWAI().isEnabled() || getUWAI().isEnabled(true)) && isAlive() && isMajorCiv())
		uwai().init(getID()); // </advc.104>
	uint uiFlag=0;
	pStream->Read(&uiFlag);
	if (uiFlag >= 6)
	{
		m_aiWarPlanStateCounter.read(pStream);
		m_aiAtWarCounter.read(pStream);
		m_aiAtPeaceCounter.read(pStream);
		m_aiHasMetCounter.read(pStream);
		m_aiOpenBordersCounter.read(pStream);
		m_aiDefensivePactCounter.read(pStream);
		m_aiShareWarCounter.read(pStream);
		if (uiFlag >= 9) // advc.130r
			m_arWarSuccess.read(pStream);
		// <advc.130r>
		else
		{
			ArrayEnumMap<TeamTypes,int> aiWarSuccess;
			aiWarSuccess.read(pStream);
			FOR_EACH_ENUM(Team)
				m_arWarSuccess.set(eLoopTeam, aiWarSuccess.get(eLoopTeam));
		} // </advc.130r>
		m_aiSharedWarSuccess.read(pStream); // advc.130m
	}
	else
	{
		m_aiWarPlanStateCounter.readArray<int>(pStream);
		m_aiAtWarCounter.readArray<int>(pStream);
		m_aiAtPeaceCounter.readArray<int>(pStream);
		m_aiHasMetCounter.readArray<int>(pStream);
		m_aiOpenBordersCounter.readArray<int>(pStream);
		m_aiDefensivePactCounter.readArray<int>(pStream);
		m_aiShareWarCounter.readArray<int>(pStream);
		// <advc.130r>
		ArrayEnumMap<TeamTypes,int> aiWarSuccess;
		aiWarSuccess.readArray<int>(pStream);
		FOR_EACH_ENUM(Team)
			m_arWarSuccess.set(eLoopTeam, aiWarSuccess.get(eLoopTeam));
		// </advc.130r>
		m_aiSharedWarSuccess.readArray<int>(pStream); // advc.130m
	}
	/*	<advc.130k> CvTeam keeps an accurate count now, our count is randomized.
		Still, better than nothing when loading an old save. */
	if (uiFlag < 8)
	{
		FOR_EACH_ENUM(Team)
			m_aiTurnsAtPeace.set(eLoopTeam, m_aiAtPeaceCounter.get(eLoopTeam));
	} // </advc.130k>
	// <advc.130n>
	if (uiFlag < 7)
	{	// Discard data b/c obsolete
		int iReligions;
		pStream->Read(&iReligions);
		for(int i = 0; i < iReligions; i++)
		{
			int first; int second;
			pStream->Read(&first);
			pStream->Read(&second);
		}
	} // </advc.130n>
	if (uiFlag >= 6)
	{
		m_aiEnemyPeacetimeTradeValue.read(pStream);
		m_aiEnemyPeacetimeGrantValue.read(pStream);
	}
	else
	{
		m_aiEnemyPeacetimeTradeValue.readArray<int>(pStream);
		m_aiEnemyPeacetimeGrantValue.readArray<int>(pStream);
	}
	// <advc.opt>
	if (uiFlag >= 3)
	{
		if (uiFlag >= 6)
			m_aiWarPlanCounts.read(pStream);
		else m_aiWarPlanCounts.readArray<int>(pStream);
		pStream->Read(&m_bAnyWarPlan);
	}
	else
	{	/*	Can't compute war plan counts until alive status has been set for all teams.
			Set negative counts in order to signal to CvGAme::onAllGameDataRead that
			AI_finalizeInit needs to be called. */
		FOR_EACH_ENUM(WarPlan)
			m_aiWarPlanCounts.set(eLoopWarPlan, -1);
	} // </advc.opt>
	if (uiFlag >= 6)
		m_aeWarPlan.read(pStream);
	else m_aeWarPlan.readArray<int>(pStream);
	pStream->Read((int*)&m_eWorstEnemy);
	// <advc.109>
	if (uiFlag >= 2)
		pStream->Read(&m_bLonely); // </advc.109>
	// <advc.650>
	if (uiFlag >= 5)
	{
		size_t iSize;
		pStream->Read(&iSize);
		m_aeNukeExplosions.resize(iSize);
		if (iSize > 0)
			pStream->Read((int)iSize, (int*)&m_aeNukeExplosions[0]);
	} // </advc.650>
	m_strengthMemory.read(pStream, uiFlag, getID()); // advc.158
	// <advc.104>
	if (isEverAlive() && !isBarbarian() && !isMinorCiv())
		m_pUWAI->read(pStream); // </advc.104>
}

// advc.opt: (for legacy savegames)
void CvTeamAI::AI_finalizeInit()
{
	m_aiWarPlanCounts.reset(); // De-allocate in case that the counts are all 0
	FOR_EACH_ENUM(WarPlan)
	{
		m_aiWarPlanCounts.set(eLoopWarPlan, AI_countWarPlans(eLoopWarPlan,
				true, MAX_CIV_PLAYERS)); // Last argument just to avoid a failed assertion
		if (m_aiWarPlanCounts.get(eLoopWarPlan) > 0)
			m_bAnyWarPlan = true;
	}
}


void CvTeamAI::write(FDataStreamBase* pStream)
{
	PROFILE_FUNC(); // advc
	CvTeam::write(pStream);

	REPRO_TEST_BEGIN_WRITE(CvString::format("TeamAI(%d)", getID()).GetCString());
	uint uiFlag;
	//uiFlag = 1; // K-Mod: StrengthMemory
	//uiFlag = 2; // advc.109
	//uiFlag = 3; // advc.opt: m_aiWarPlanCounts
	//uiFlag = 4; // advc.158
	//uiFlag = 5; // advc.650
	//uiFlag = 6; // advc.enum: new enum map save behavior
	//uiFlag = 7; // advc.130n (Now handled w/o extra data)
	//uiFlag = 8; // advc.130k: To support CvTeam::m_aiTurnsAtPeace
	uiFlag = 9; // advc.130r
	pStream->Write(uiFlag);

	m_aiWarPlanStateCounter.write(pStream);
	m_aiAtWarCounter.write(pStream);
	m_aiAtPeaceCounter.write(pStream);
	m_aiHasMetCounter.write(pStream);
	m_aiOpenBordersCounter.write(pStream);
	m_aiDefensivePactCounter.write(pStream);
	m_aiShareWarCounter.write(pStream);
	m_arWarSuccess.write(pStream);
	m_aiSharedWarSuccess.write(pStream); // advc.130m
	m_aiEnemyPeacetimeTradeValue.write(pStream);
	m_aiEnemyPeacetimeGrantValue.write(pStream);
	m_aiWarPlanCounts.write(pStream); // advc.opt
	pStream->Write(m_bAnyWarPlan); // advc.opt
	m_aeWarPlan.write(pStream);
	pStream->Write(m_eWorstEnemy);
	pStream->Write(m_bLonely); // advc.109
	// <advc.650>
	pStream->Write(m_aeNukeExplosions.size());
	if (!m_aeNukeExplosions.empty())
		pStream->Write((int)m_aeNukeExplosions.size(), (int*)&m_aeNukeExplosions[0]);
	// </advc.650>
	REPRO_TEST_END_WRITE();
	m_strengthMemory.write(pStream); // advc.158
	// <advc.104>
	if (isEverAlive() && !isBarbarian() && !isMinorCiv())
		uwai().write(pStream); // </advc.104>
}

// advc.012:
int CvTeamAI::AI_plotDefense(CvPlot const& kPlot, bool bIgnoreBuilding,
	bool bGarrisonStrength) const // advc.500b
{
	TeamTypes eAttacker = NO_TEAM;
	/*  We could also be attacked in p by a second war enemy that doesn't own the plot;
		impossible to predict. An attack by the plot owner is far more likely though. */
	if (kPlot.isOwned() && GET_TEAM(getID()).isAtWar(kPlot.getTeam()))
		eAttacker = kPlot.getTeam();
	return kPlot.defenseModifier(getID(), bIgnoreBuilding, eAttacker,
			bGarrisonStrength); // advc.500b
}

/*	advc.104, advc.651: Does this team expect eTrainPlayer (can be on the same team)
	to have cities with sufficient production to train a significant number of units
	of type eUnit? */
bool CvTeamAI::AI_isExpectingToTrain(PlayerTypes eTrainPlayer, UnitTypes eUnit) const
{
	PROFILE_FUNC();
	CvUnitInfo const& kUnit = GC.getInfo(eUnit);
	bool bSeaUnit = (kUnit.getDomainType() == DOMAIN_SEA);
	int iMinAreaSz = std::max(0, kUnit.getMinAreaSize());
	/*	Should be able to train at least two units in ten turns (i.e. one in five);
		otherwise, the unit probably won't be trained at all, or just 1 or 2. */
	int iTargetProduction = intdiv::round(GET_PLAYER(eTrainPlayer).
			getProductionNeeded(eUnit), 5);
	int iPartialSum = 0;
	FOR_EACH_CITY(c, GET_PLAYER(eTrainPlayer))
	{
		/*	Let's let the AI cheat for now; otherwise we'd have to take
			some sort of guess about the unknown cities. Most of the current calls
			have eTrainPlayer on the callee's team anyway. */
		/*if (!AI_deduceCitySite(*c))
			continue;*/
		if ((bSeaUnit && !c->isCoastal(iMinAreaSz)) || !c->canTrain(eUnit))
			continue;
		iPartialSum += c->getProduction();
		if (iPartialSum >= iTargetProduction)
			return true;
	}
	return false;
}

// <advc.130y> ('bFreed' is unused; not needed after all, I guess.)
void CvTeamAI::AI_forgiveEnemy(TeamTypes eEnemyTeam, bool bCapitulated, bool bFreed)
{
	/*  'capitulated' refers to us, the callee. This function is called when
		making peace but also when breaking free. Can therefore not rely on
		this->isCapitulated (but GET_TEAM(eEnemyTeam).isCapitulated() is fine).
		If we make peace after having broken free, it's called twice for each
		former enemy in total. */
	int iDelta = 0;
	bCapitulated = (bCapitulated || GET_TEAM(eEnemyTeam).isCapitulated());
	if(bCapitulated)
		iDelta--;
	scaled rWS = GET_TEAM(eEnemyTeam).AI_getWarSuccess(getID());
	for (MemberAIIter itMember(getID()); itMember.hasNext(); ++itMember)
	{
		CvPlayerAI& kMember = *itMember;
		// <advc.104i> Be willing to talk to everyone, not just 'enemyId'.
		for (PlayerIter<MAJOR_CIV,OTHER_KNOWN_TO> itOther(getID()); itOther.hasNext(); ++itOther)
		{
			PlayerTypes eOtherCiv = itOther->getID();
			kMember.AI_setMemoryCount(eOtherCiv, MEMORY_DECLARED_WAR_RECENT, 0);
			// <advc.130f> Cap at 1
			if(kMember.AI_getMemoryCount(eOtherCiv, MEMORY_STOPPED_TRADING_RECENT) > 1)
				kMember.AI_setMemoryCount(eOtherCiv, MEMORY_STOPPED_TRADING_RECENT, 1);
			// </advc.130f>
		} // </advc.104i>
		// No vassal-related forgiveness when war success high
		iDelta = std::min(0, iDelta +
				(rWS / kMember.warSuccessAttitudeDivisor()).round());
		for (MemberIter itEnemy(eEnemyTeam); itEnemy.hasNext(); ++itEnemy)
		{
			CvPlayer const& kEnemyMember = *itEnemy;
			int iLimit = -kMember.AI_getMemoryCount(kEnemyMember.getID(), MEMORY_DECLARED_WAR);
			int iDeltaLoop = iDelta;
			/*  Forgiveness if war success small, but only if memory high and
				no other forgiveness condition applies, and not (times 0) in the
				Ancient era (attacks on Workers and Settlers). */
			if (iLimit <= -3 && iDelta >= 0 &&
				rWS < fixp(0.3) * AI_getCurrEraFactor() * GC.getWAR_SUCCESS_CITY_CAPTURING())
			{
				iDeltaLoop--;
			}
			// No complete forgiveness unless capitulated
			if(!bCapitulated && iLimit < 0)
				iLimit++;
			int iChange = std::min(0, std::max(iDeltaLoop, iLimit));
			if(iChange != 0)
			{
				kMember.AI_changeMemoryCount(kEnemyMember.getID(),
						MEMORY_DECLARED_WAR, iChange);
			}
			if(bCapitulated) // Directly willing to sign OB
			{
				kMember.AI_setMemoryCount(kEnemyMember.getID(),
						MEMORY_CANCELLED_OPEN_BORDERS, 0);
			} // <advc.134a>
			int iContactPeace = kMember.AI_getContactTimer(
					kEnemyMember.getID(), CONTACT_PEACE_TREATY);
			if(iContactPeace != 0) // for debugger stop
			{
				kMember.AI_changeContactTimer(kEnemyMember.getID(),
						CONTACT_PEACE_TREATY, -iContactPeace);
			} // </advc.134a>
		}
	}
}

void CvTeamAI::AI_thankLiberator(TeamTypes eLiberator)
{
	for (MemberAIIter itOur(getID()); itOur.hasNext(); ++itOur)
	{
		CvPlayerAI& kOurMember = *itOur;
		int iWSDivisor = kOurMember.warSuccessAttitudeDivisor();
		for (MemberAIIter itLib(eLiberator); itLib.hasNext(); ++itLib)
		{
			CvPlayerAI& kLiberatorMember = *itLib;
			int iMemory = std::max(0, 2 -
					(GET_TEAM(eLiberator).AI_getWarSuccess(getID()) / iWSDivisor).round());
			kOurMember.AI_changeMemoryCount(kLiberatorMember.getID(), MEMORY_INDEPENDENCE,
					2 * iMemory); // advc.130j: doubled
		}
	}
} // </advc.130y>

// <advc.115b> <advc.104>
/*	NO_VOTESOURCE if none built yet, AP if AP built but not UN;
	otherwise UN. */
VoteSourceTypes CvTeamAI::AI_getLatestVictoryVoteSource() const
{
	CvGame const& kGame = GC.getGame();
	VoteSourceTypes eVS = NO_VOTESOURCE;
	int iBestValue = MIN_INT;
	FOR_EACH_ENUM(VoteSource)
	{
		if (!kGame.isDiploVote(eLoopVoteSource))
			continue;
		int iValue = 0;
		/*	Slightly more flexible than just saying that UN beats AP.
			But I doubt that it'll accomplish anything if a mod indeed adds
			a new vote source. */
		if (kGame.isTeamVoteEligible(getID(), eLoopVoteSource))
			iValue += 100;
		if (kGame.getVoteSourceReligion(eLoopVoteSource) == NO_RELIGION)
			iValue += 50;
		iValue -= GC.getInfo(eLoopVoteSource).getVoteInterval();
		if (iValue > iBestValue)
		{
			iBestValue = iValue;
			eVS = eLoopVoteSource;
		}
	}
	return eVS;
}


int CvTeamAI::AI_countVSNonMembers(VoteSourceTypes eVS) const
{
	int iCount = 0;
	for(PlayerIter<MAJOR_CIV> itPlayer(getID()); itPlayer.hasNext(); ++itPlayer)
	{
		if (!itPlayer->isVotingMember(eVS) || !isHasMet(itPlayer->getTeam()))
			iCount++;
	}
	return iCount;
}

// piVoteTarget (out param): Vote target for diplo victory; -1 if there is none.
int CvTeamAI::AI_votesToGoForVictory(int* piVoteTarget, bool bForceSecular) const
{
	CvGameAI const& kGame = GC.AI_getGame();
	VoteSourceTypes eVS = AI_getLatestVictoryVoteSource();
	bool bSecular = (eVS == NO_VOTESOURCE || bForceSecular);
	ReligionTypes eVSReligion = NO_RELIGION;
	if (!bSecular)
		eVSReligion = kGame.getVoteSourceReligion(eVS);
	if (eVSReligion == NO_RELIGION)
		bSecular = true;
	if (bSecular && getCurrentEra() + 1 < kGame.AI_getVoteSourceEra()) // not close to UN
	{
		if(piVoteTarget != NULL)
			*piVoteTarget = -1;
		return -1;
	}
	int iPopThresh = -1;
	VoteTypes eVictoryVote = NO_VOTE;
	FOR_EACH_ENUM(Vote)
	{
		CvVoteInfo const& kVote = GC.getInfo(eLoopVote);
		if ((kVote.getStateReligionVotePercent() == 0) == bSecular &&
			kVote.isVictory())
		{
			iPopThresh = kVote.getPopulationThreshold();
			eVictoryVote = eLoopVote;
			break;
		}
	}
	if (iPopThresh < 0)
	{
		// OK if a mod removes the UN victory vote
		FOR_EACH_ENUM(Vote)
		{
			CvVoteInfo const& kVote = GC.getInfo(eLoopVote);
			if (kVote.getStateReligionVotePercent() == 0 && kVote.isVictory())
			{
				FErrorMsg("Could not determine vote threshold");
				break;
			}
		}
		if(piVoteTarget != NULL)
			*piVoteTarget = -1;
		return -1;
	}
	scaled rTotalPop = kGame.getTotalPopulation();
	if (!bSecular)
		rTotalPop = rTotalPop * per100(kGame.calculateReligionPercent(eVSReligion, true));
	scaled rTargetPop = per100(iPopThresh) * rTotalPop;
	if (piVoteTarget != NULL)
		*piVoteTarget = rTargetPop.ceil();
	/*  rTargetPop assumes 1 vote per pop, but member cities actually
		cast 2 votes per pop. */
	scaled rReligionVoteNormalizer = 1;
	if(!bSecular)
	{
		rReligionVoteNormalizer = scaled(100,
				100 + GC.getInfo(eVictoryVote).getStateReligionVotePercent());
	}
	scaled rVotesToGo = rTargetPop;
	scaled rOurVotes = getTotalPopulation();
	if (eVS != NO_VOTESOURCE && !bForceSecular)
		rOurVotes = getVotes(eVictoryVote, eVS) * rReligionVoteNormalizer;
	rVotesToGo -= rOurVotes;
	scaled rVotesFromOthers = 0;
	/*  Will only work in obvious cases, otherwise we'll work with unknown
		candidates (NO_TEAM). */
	TeamTypes eCounterCandidate = (bSecular ? AI_diploVoteCounterCandidate(eVS) : NO_TEAM);
	// This team: already covered above
	for (TeamAIIter<MAJOR_CIV,NOT_SAME_TEAM_AS> itTeam(getID());
		itTeam.hasNext(); ++itTeam)
	{
		CvTeamAI const& kTeam = *itTeam;
		// No votes from human non-vassals
		if((kTeam.isHuman() && !kTeam.isVassal(getID())) ||
			kTeam.getMasterTeam() == eCounterCandidate)
		{
			continue;
		}
		scaled rPop = kTeam.getTotalPopulation();
		if (eVS != NO_VOTESOURCE && !bSecular)
			rPop = kTeam.getVotes(eVictoryVote, eVS) * rReligionVoteNormalizer;
		// Count our vassals as fully supportive
		if (kTeam.isVassal(getID()))
		{
			rVotesToGo -= rPop;
			continue;
		}
		/*  Count Friendly rivals as only partially supportive b/c relations may
			soon sour, and b/c the rival may like the counter candidate even better. */
		if(!kTeam.isHuman() && kTeam.AI_getAttitude(getID()) >= ATTITUDE_FRIENDLY)
		{
			rVotesFromOthers += rPop * fixp(0.8);
			continue;
		}
	}
	/*  To account for an unknown counter-candidate. This will usually neutralize
		our votes from friends, leaving only our own (and vassals') votes. */
	if (eCounterCandidate == NO_TEAM)
		rVotesFromOthers -= fixp(1.3) * rTotalPop / TeamIter<MAJOR_CIV>::count();
	if (rVotesFromOthers > 0)
		rVotesToGo -= rVotesFromOthers;
	return std::max(0, rVotesToGo.round());
}


TeamTypes CvTeamAI::AI_diploVoteCounterCandidate(VoteSourceTypes eVS) const
{
	/*  Only cover this obvious case: we're among the two teams with the
		most votes (clearly ahead of the third). Otherwise, don't hazard a guess. */
	TeamTypes eCounterCandidate = NO_TEAM;
	int iFirstMostVotes = -1, iSecondMostVotes = -1, iThirdMostVotes = -1;
	for (TeamIter<MAJOR_CIV> it; it.hasNext(); ++it)
	{
		CvTeam const& kTeam = *it;
		// Someone else already controls the UN. This gets too complicated.
		if (kTeam.getID() != getID() && eVS != NO_VOTESOURCE &&
			kTeam.isForceTeamVoteEligible(eVS))
		{
			return NO_TEAM;
		}
		if (kTeam.isAVassal())
			continue;
		int iVotes = kTeam.getTotalPopulation();
		if (iVotes > iThirdMostVotes)
		{
			if (iVotes > iSecondMostVotes)
			{
				if (iVotes > iFirstMostVotes)
				{
					iThirdMostVotes = iSecondMostVotes;
					iSecondMostVotes = iFirstMostVotes;
					iFirstMostVotes = iVotes;
					if (kTeam.getID() != getID())
						eCounterCandidate = kTeam.getID();
				}
				else
				{
					iThirdMostVotes = iSecondMostVotes;
					iSecondMostVotes = iVotes;
					if (iFirstMostVotes == getID())
						eCounterCandidate = kTeam.getID();
				}
			}
			else iThirdMostVotes = iVotes;
		}
	}
	// Too close to hazard a guess
	if(iThirdMostVotes * 5 >= iSecondMostVotes * 4 ||
		getTotalPopulation() < iSecondMostVotes)
	{
		return NO_TEAM;
	}
	return eCounterCandidate;
} // </advc.104>


bool CvTeamAI::AI_isAnyCloseToReligiousVictory() const
{
	for (MemberAIIter it(getID()); it.hasNext(); ++it)
	{
		if (it->isCloseToReligiousVictory())
			return true;
	}
	return false;
} //</advc.115b>


int CvTeamAI::AI_noTechTradeThreshold() const
{
	int r = 0;
	MemberIter it(getID());
	for (; it.hasNext(); ++it)
		r += GC.getInfo(it->getPersonalityType()).getNoTechTradeThreshold();
	return r / std::max(1, it.nextIndex());
}


int CvTeamAI::AI_techTradeKnownPercent() const
{
	int r = 0;
	MemberIter it(getID());
	for (; it.hasNext(); ++it)
		r += GC.getInfo(it->getPersonalityType()).getTechTradeKnownPercent();
	return r / std::max(1, it.nextIndex());
}

// advc.104: Members of the same team should refuse to talk in unison
int CvTeamAI::AI_refuseToTalkWarThreshold() const
{
	int iRTT = 0;
	MemberIter itMember(getID());
	for (; itMember.hasNext(); ++itMember)
		iRTT += GC.getInfo(itMember->getPersonalityType()).getRefuseToTalkWarThreshold();
	return intdiv::round(iRTT, itMember.nextIndex());
}


int CvTeamAI::AI_maxWarRand() const
{
	int r = 0;
	MemberIter it(getID());
	for (; it.hasNext(); ++it)
		r += GC.getInfo(it->getPersonalityType()).getMaxWarRand();
	return r / std::max(1, it.nextIndex());
}


int CvTeamAI::AI_maxWarNearbyPowerRatio() const
{
	int r = 0;
	MemberIter it(getID());
	for (; it.hasNext(); ++it)
		r += GC.getInfo(it->getPersonalityType()).getMaxWarNearbyPowerRatio();
	return r / std::max(1, it.nextIndex());
}


int CvTeamAI::AI_maxWarDistantPowerRatio() const
{
	int r = 0;
	MemberIter it(getID());
	for (; it.hasNext(); ++it)
		r += GC.getInfo(it->getPersonalityType()).getMaxWarDistantPowerRatio();
	return r / std::max(1, it.nextIndex());
}


int CvTeamAI::AI_maxWarMinAdjacentLandPercent() const
{
	int r = 0;
	MemberIter it(getID());
	for (; it.hasNext(); ++it)
		r += GC.getInfo(it->getPersonalityType()).getMaxWarMinAdjacentLandPercent();
	return r / std::max(1, it.nextIndex());
}


int CvTeamAI::AI_limitedWarRand() const
{
	int r = 0;
	MemberIter it(getID());
	for (; it.hasNext(); ++it)
		r += GC.getInfo(it->getPersonalityType()).getLimitedWarRand();
	return r / std::max(1, it.nextIndex());
}


int CvTeamAI::AI_limitedWarPowerRatio() const
{
	int r = 0;
	MemberIter it(getID());
	for (; it.hasNext(); ++it)
		r += GC.getInfo(it->getPersonalityType()).getLimitedWarPowerRatio();
	return r / std::max(1, it.nextIndex());
}


int CvTeamAI::AI_dogpileWarRand() const
{
	int r = 0;
	MemberIter it(getID());
	for (; it.hasNext(); ++it)
		r += GC.getInfo(it->getPersonalityType()).getDogpileWarRand();
	return r / std::max(1, it.nextIndex());
}


int CvTeamAI::AI_makePeaceRand() const
{
	int r = 0;
	MemberIter it(getID());
	for (; it.hasNext(); ++it)
		r += GC.getInfo(it->getPersonalityType()).getMakePeaceRand();
	return r / std::max(1, it.nextIndex());
}


int CvTeamAI::AI_noWarAttitudeProb(AttitudeTypes eAttitude) const
{
	int iR = 0;
	// BETTER_BTS_AI_MOD, War Strategy AI, 03/20/10, jdog5000: START
	int iVictoryStrategyAdjust = 0;
	MemberAIIter it(getID());
	for (; it.hasNext(); ++it)
	{
		CvPlayerAI const& kMember = *it;
		iR += GC.getInfo(kMember.getPersonalityType()).getNoWarAttitudeProb(eAttitude);
		// In final stages of miltaristic victory, AI may turn on its friends!
		if (kMember.AI_atVictoryStage(AI_VICTORY_CONQUEST4))
			iVictoryStrategyAdjust += 30;
		else if (kMember.AI_atVictoryStage(AI_VICTORY_DOMINATION4))
			iVictoryStrategyAdjust += 20;
	}
	int iCount = std::max(1, it.nextIndex());
	iR /= iCount;
	iVictoryStrategyAdjust /= iCount;
	return std::max(0, iR - iVictoryStrategyAdjust);
	// BETTER_BTS_AI_MOD: END
}

// <advc.104y>
int CvTeamAI::AI_noWarProbAdjusted(TeamTypes eOther) const
{
	AttitudeTypes eTowardThem = AI_getAttitude(eOther, true);
	int iR = AI_noWarAttitudeProb(eTowardThem);
	if (iR < 100 || isOpenBorders(eOther) || eTowardThem == 0)
		return iR;
	return AI_noWarAttitudeProb((AttitudeTypes)(eTowardThem - 1));
}


bool CvTeamAI::AI_isAvoidWar(TeamTypes eOther, bool bPersonalityKnown) const
{
	// <advc.130u>
	if (isHuman())
		return false; // </advc.130u>
	if (!bPersonalityKnown && GC.getGame().isOption(GAMEOPTION_RANDOM_PERSONALITIES))
		return (AI_getAttitude(eOther) == ATTITUDE_FRIENDLY);
	return (AI_noWarProbAdjusted(eOther) >= 100);
} // </advc.104y>


// <advc.130i>
int CvTeamAI::AI_getOpenBordersAttitudeDivisor() const
{
	int r = 0;
	for (MemberIter it(getID()); it.hasNext(); ++it)
		r = std::max(r, GC.getInfo(it->getPersonalityType()).getOpenBordersAttitudeDivisor());
	return r;
}

scaled CvTeamAI::AI_getOpenBordersCounterIncrement(TeamTypes eOther) const
{
	FAssert(eOther != getID() && eOther != NO_TEAM);

	int iTotalForeignTrade = 0;
	int iTradeFromThem = 0;
	for (MemberIter it(getID()); it.hasNext(); ++it)
	{
		// Based on calculateTradeRoutes in BUG's TradeUtil.py
		FOR_EACH_CITY(c, *it)
		{
			for (int i = 0; i < c->getTradeRoutes(); i++)
			{
				CvCity const* pPartnerCity = c->getTradeCity(i);
				if (pPartnerCity == NULL)
					continue;
				TeamTypes ePartnerTeam = pPartnerCity->getTeam();
				if (ePartnerTeam == NO_TEAM || ePartnerTeam == getID())
					continue;
				int iTradeCommerce = c->calculateTradeYield(YIELD_COMMERCE,
						c->calculateTradeProfit(pPartnerCity));
				iTotalForeignTrade += iTradeCommerce;
				if (ePartnerTeam == eOther)
					iTradeFromThem += iTradeCommerce;
			}
		}
	}
	scaled rFromTrade = 0;
	if (iTotalForeignTrade > 0 && iTradeFromThem > 0)
	{
		rFromTrade = scaled(iTradeFromThem, iTotalForeignTrade).sqrt();
		rFromTrade *= fixp(1.3);
	}
	scaled rFromCloseness = 0;
	int iOurCities = getNumCities();
	int iTheirCities = GET_TEAM(eOther).getNumCities();
	if (iOurCities > 0 && iTheirCities > 0)
	{
		rFromCloseness = AI_teamCloseness(eOther) /
				(scaled(iOurCities + iTheirCities).sqrt() * 20);
	}
	/*  Would be nice to add another, say, 0.25 if any of our units w/o
		isRivalTerritory is currently inside the borders of an eOther team member,
		but that's too costly to check here and too complicated to keep track of. */
	return scaled::clamp(rFromTrade + rFromCloseness, fixp(1/6.), fixp(8/6.));
} // </advc.130i>

/*  advc.130k: Random number to add or subtract from state counters
	(instead of just incrementing or decrementing). Binomial distribution
	with 2 trials and a probability of pr.
	Non-negative result, caller will have to multiply by -1 to decrease a counter.
	Result is capped at iUpperCap; -1: none. */
int CvTeamAI::AI_randomCounterChange(int iUpperCap, scaled rProb) const
{
	CvGame const& kGame = GC.getGame();
	int iSpeedPercent = GC.getInfo(kGame.getGameSpeedType()).get(
				CvGameSpeedInfo::AIMemoryRandPercent);
	scaled rOurEra = AI_getCurrEraFactor();
	if (rOurEra < fixp(0.5))
		iSpeedPercent = kGame.getSpeedPercent();
	else if (rOurEra < fixp(1.5))
		iSpeedPercent = (kGame.getSpeedPercent() + iSpeedPercent) / 2;
	rProb *= scaled(100, std::max(50, iSpeedPercent));
	int iR = 0;
	if (SyncRandSuccess(rProb))
		iR++;
	if (SyncRandSuccess(rProb))
		iR++;
	if (iUpperCap < 0)
		return iR;
	return std::min(iR, iUpperCap);
}


void CvTeamAI::AI_doCounter()
{
	// advc (note): Attitude isn't updated here. Should be soon enough in AI_doTurnPost.
	for (TeamIter<ALIVE> it(getID()); it.hasNext(); ++it)
	{
		TeamTypes const eOther = it->getID();
		if (eOther == getID())
			continue;
		/*  advc.001: Guard added. NO_WARPLAN should imply that the state counter
			is at 0, rather than some arbitrary value. advc.104 relies on this. */
		if (AI_getWarPlan(eOther) != NO_WARPLAN)
			AI_changeWarPlanStateCounter(eOther, 1);
		/*  No randomization for atWar and hasMet. These are used by the AI in
			several places that more or less assume an exact count. */
		if (isAtWar(eOther))
			AI_changeAtWarCounter(eOther, 1);
		else if (canContact(eOther)) // doc: peace counter requires contact
		{
			AI_changeAtPeaceCounter(eOther,  // <advc.130k>
					// Better count to 1 deterministically
					AI_getAtPeaceCounter(eOther) == 0 ? 1 : AI_randomCounterChange());
		}  // </advc.130k>
		if (!isHasMet(eOther) || isBarbarian() || GET_TEAM(eOther).isBarbarian())
			continue;
		AI_changeHasMetCounter(eOther, 1);
		// <advc>
		if (isMinorCiv() || GET_TEAM(eOther).isMinorCiv())
			continue; // </advc>
		scaled const rDecayFactor = 1 - AI_getDiploDecay(); // advc.130k
		// <advc.130i>
		// doc: open borders, defensive pact, shared war requires contact
		if (canContact(eOther))
		{
			if(isOpenBorders(eOther))
			{
				scaled rProb = AI_getOpenBordersCounterIncrement(eOther) / 2;
				int iMax = 2 * AI_getOpenBordersAttitudeDivisor() + 10;
				AI_changeOpenBordersCounter(eOther, AI_randomCounterChange(iMax, rProb));
			} // </advc.130i>  <advc.130k>
			else
			{
				AI_setOpenBordersCounter(eOther,
						(AI_getOpenBordersCounter(eOther) * rDecayFactor).floor());
			} // </advc.130k>
			if(isDefensivePact(eOther))
				AI_changeDefensivePactCounter(eOther, AI_randomCounterChange());
			// <advc.130k>
			else
			{
				AI_setDefensivePactCounter(eOther,
						(AI_getDefensivePactCounter(eOther) * rDecayFactor).floor());
			} // </advc.130k>
			if(AI_shareWar(eOther))
				AI_changeShareWarCounter(eOther, AI_randomCounterChange()); // </advc.130k>
			// <advc.130m> Decay by 1 with 10% probability
			else if(AI_getShareWarCounter(eOther) > 0 && SyncRandSuccess100(10))
				AI_changeShareWarCounter(eOther, -1);
			AI_setSharedWarSuccess(eOther,
					(AI_getSharedWarSuccess(eOther) * rDecayFactor).floor());
		}
		// </advc.130m>  <advc.130p>
		AI_setEnemyPeacetimeGrantValue(eOther,
				(AI_getEnemyPeacetimeGrantValue(eOther) * rDecayFactor).floor(),
				false);
		AI_setEnemyPeacetimeTradeValue(eOther,
				(AI_getEnemyPeacetimeTradeValue(eOther) * rDecayFactor).floor(),
				false);
		// </advc.130p>
		// <advc.130r>
		{	// Double decay rate for war success
			scaled rWSOld = AI_getWarSuccess(eOther);
			scaled rWSNew = rWSOld * std::max(fixp(0.5), 1 - 2 * AI_getDiploDecay());
			AI_setWarSuccess(eOther, rWSNew);
		} // </advc.130r>
	}
}

// BETTER_BTS_AI_MOD, War Strategy AI, 03/26/10, jdog5000:
// Block AI from declaring war on a distant vassal if it shares an area with the master
/*  advc.104j (comment): Since a war plan against a master implies a war plan
	against its vassal, I don't think this function is relevant anymore. */
bool CvTeamAI::AI_isOkayVassalTarget(TeamTypes eTeam) const
{
	// <advc.130v>
	if(GET_TEAM(eTeam).isCapitulated())
		return false; // </advc.130v>
	/*if (GET_TEAM(eTeam).isAVassal()) {
		if (!AI_hasCitiesInPrimaryArea(eTeam) || AI_calculateAdjacentLandPlots(eTeam) == 0) {
			for (int iI = 0; iI < MAX_CIV_TEAMS; iI++) {
				if (GET_TEAM(eTeam).isVassal((TeamTypes)iI)) {
					if (AI_hasCitiesInPrimaryArea((TeamTypes)iI) && AI_calculateAdjacentLandPlots((TeamTypes)iI) > 0)
						return false;
	} } } }
	return true;*/
	// K-Mod version. Same functionality (but without support for multiple masters)
	TeamTypes eMasterTeam = GET_TEAM(eTeam).getMasterTeam();
	if (eMasterTeam == eTeam)
		return true; // not a vassal.

	if ((!AI_hasCitiesInPrimaryArea(eTeam) || AI_calculateAdjacentLandPlots(eTeam) == 0) &&
		(AI_hasCitiesInPrimaryArea(eMasterTeam) && AI_calculateAdjacentLandPlots(eMasterTeam) > 0))
		return false;

	return true;
	// K-Mod end
}

// advc: Cut from doWar; only relevant if UWAI disabled.
void CvTeamAI::AI_abandonWarPlanIfTimedOut(int iAbandonTimeModifier,
	TeamTypes eTarget, bool bLimited, int iEnemyPowerPercent)
{
	FAssert(canEventuallyDeclareWar(eTarget));
	bool bActive = false;
	for (MemberAIIter it(getID()); it.hasNext(); ++it)
	{
		if (it->AI_isAnyEnemyTargetMission(eTarget))
		{
			bActive = true;
			break;
		}
	}
	if (!bActive)
	{
		if (AI_getWarPlanStateCounter(eTarget) > ((15 * iAbandonTimeModifier) / (100)))
		{
			if (gTeamLogLevel >= 1)
			{
				logBBAI("    Team %d (%S) abandoning WARPLAN_LIMITED or WARPLAN_DOGPILE against team %d (%S) after %d turns with enemy power percent %d",
						getID(), GET_PLAYER(getLeaderID()).getCivilizationDescription(0),
						eTarget, GET_PLAYER(GET_TEAM(eTarget).getLeaderID()).getCivilizationDescription(0),
						AI_getWarPlanStateCounter(eTarget), iEnemyPowerPercent);
			}
			AI_setWarPlan(eTarget, NO_WARPLAN);
		}
	}
	if(!bLimited)
		return;
	if (AI_getWarPlan(eTarget) == WARPLAN_DOGPILE)
	{
		if (GET_TEAM(eTarget).getNumWars() <= 0)
		{
			if (gTeamLogLevel >= 1)
			{
				logBBAI("    Team %d (%S) abandoning WARPLAN_DOGPILE against team %d (%S) after %d turns because enemy has no war",
						getID(), GET_PLAYER(getLeaderID()).getCivilizationDescription(0),
						eTarget, GET_PLAYER(GET_TEAM(eTarget).getLeaderID()).getCivilizationDescription(0),
						AI_getWarPlanStateCounter(eTarget));
			}
			AI_setWarPlan(eTarget, NO_WARPLAN);
		}
	}
}

// advc.136a:
bool CvTeamAI::AI_isPursuingCircumnavigation() const
{
	//PROFILE_FUNC(); // No problem at all
	if(!GC.getGame().circumnavigationAvailable())
		return false;
	for (MemberAIIter itMember(getID()); itMember.hasNext(); ++itMember)
	{
		CvCivilization const& kCiv = itMember->getCivilization();
		for (int i = 0; i < kCiv.getNumUnits(); i++)
		{
			UnitTypes eUnit = kCiv.unitAt(i);
			if(GC.getInfo(eUnit).getDomainType() != DOMAIN_SEA)
				continue;
			if(!itMember->AI_isAnyImpassable(eUnit) && itMember->canTrain(eUnit))
				return true;
		}
	}
	return false;
}

/*	Make war decisions, mainly for starting or switching war plans.
	This function has been tweaked throughout by BBAI and K-Mod,
	some changes marked, others not. (K-Mod has made several structural changes.) */
void CvTeamAI::AI_doWar()
{
	PROFILE_FUNC();

	CvGame& kGame = GC.getGame(); // K-Mod
	/* FAssert(!isHuman());
	FAssert(!isBarbarian());
	FAssert(!isMinorCiv());
	if (isAVassal())
		return;*/
	// disabled by K-Mod. All civs still need to do some basic updates.
	if (GC.getPythonCaller()->AI_doWar(getID()))
		return;
	// <advc.104>
	if(getUWAI().isEnabled() || getUWAI().isEnabled(true))
	{
		// Let the K-Mod code handle Barbarians and minors
		if(!isBarbarian() && !isMinorCiv() && getNumCities() > 0)
		{
			m_pUWAI->doWar();
			if(getUWAI().isEnabled())
				return;
		}
	} // </advc.104>

	int iEnemyPowerPercent = AI_getEnemyPowerPercent();

	// K-Mod note: This first section also used for vassals, and for human players.
	for (TeamIter<ALIVE,KNOWN_POTENTIAL_ENEMY_OF> it(getID()); it.hasNext(); ++it)
	{
		TeamTypes eLoopTeam = it->getID(); // advc
		if (AI_getWarPlan(eLoopTeam) == NO_WARPLAN)
			continue;

		int iTimeModifier = 100; // preperation time modifier
		int iAbandonTimeModifier = 100; // deadline for attack modifier
		iAbandonTimeModifier *= 50 + GC.getInfo(kGame.getGameSpeedType()).getTrainPercent();
		iAbandonTimeModifier /= 150;
		// (more adjustments to the time modifiers will come later)

		if (AI_getWarPlan(eLoopTeam) == WARPLAN_ATTACKED_RECENT)
		{
			FAssert(isAtWar(eLoopTeam));

			if (AI_getAtWarCounter(eLoopTeam) >
				(GET_TEAM(eLoopTeam).AI_isLandTarget(getID()) ? 9 : 3))
			{
				if (gTeamLogLevel >= 1) logBBAI("    Team %d (%S) switching WARPLANS against team %d (%S) from ATTACKED_RECENT to ATTACKED with enemy power percent %d", getID(), GET_PLAYER(getLeaderID()).getCivilizationDescription(0), eLoopTeam, GET_PLAYER(GET_TEAM(eLoopTeam).getLeaderID()).getCivilizationDescription(0), iEnemyPowerPercent);
				AI_setWarPlan(eLoopTeam, WARPLAN_ATTACKED);
			}
		}

		// K-Mod
		if (isHuman() || isAVassal())
		{
			CvTeamAI& kOurMaster = GET_TEAM(getMasterTeam());
			if (!isAtWar(eLoopTeam))
			{
				/* advc.006: The second clause was ==WARPLAN_LIMITED.
				   Breached in one of my (non-AIAutoPlay) games, and I don't think
				   it made sense either.
				   Actually, disabling it entirely. Not always true when returning
				   from AI Auto Play, and I don't think this is a problem. */
				//FAssert(AI_getWarPlan(eLoopTeam) == WARPLAN_PREPARING_TOTAL || AI_getWarPlan(eLoopTeam) == WARPLAN_PREPARING_LIMITED);
				if (isHuman() || kOurMaster.isHuman())
				{
					if (AI_getWarPlanStateCounter(eLoopTeam) > 20 * iAbandonTimeModifier / 100)
					{
						if (gTeamLogLevel >= 1) logBBAI("    Team %d (%S) abandoning WARPLANS against team %d (%S) due to human / vassal timeout", getID(), GET_PLAYER(getLeaderID()).getCivilizationDescription(0), eLoopTeam, GET_PLAYER(GET_TEAM(eLoopTeam).getLeaderID()).getCivilizationDescription(0));
						AI_setWarPlan(eLoopTeam, NO_WARPLAN);
					}
				}
				else
				{
					if (kOurMaster.AI_getWarPlan(eLoopTeam) == NO_WARPLAN)
					{
						if (gTeamLogLevel >= 1) logBBAI("    Team %d (%S) abandoning WARPLANS against team %d (%S) due to AI master's warplan cancelation", getID(), GET_PLAYER(getLeaderID()).getCivilizationDescription(0), eLoopTeam, GET_PLAYER(GET_TEAM(eLoopTeam).getLeaderID()).getCivilizationDescription(0));
						AI_setWarPlan(eLoopTeam, NO_WARPLAN);
					}
				}
			}

			continue; // Nothing else required for vassals and human players
		}
		// K-Mod

		if (!isAtWar(eLoopTeam)) // K-Mod. time / abandon modifiers are only relevant for war preparations. We don't need them if we are already at war.
		{
			int iThreshold = (80*AI_maxWarNearbyPowerRatio())/100;

			if (iEnemyPowerPercent < iThreshold)
			{
				iTimeModifier *= iEnemyPowerPercent;
				iTimeModifier /= iThreshold;
			}
			// K-Mod
			// intercontinental wars need more prep time
			if (!AI_hasCitiesInPrimaryArea(eLoopTeam))
			{
				iTimeModifier *= 5;
				iTimeModifier /= 4;
				iAbandonTimeModifier *= 5;
				iAbandonTimeModifier /= 4;
				// maybe in the future I'll count the number of local cities and the number of overseas cities
				// and use it to make a more appropriate modifier... but not now.
			}
			else
			{
				//with crush strategy, use just 2/3 of the prep time.
				int iCrushMembers = AI_countMembersWithStrategy(AI_STRATEGY_CRUSH);
				iTimeModifier *= 3 * (getNumMembers()-iCrushMembers) + 2 * iCrushMembers;
				iTimeModifier /= 3;
			}
			// K-Mod end

			iTimeModifier *= 50 + GC.getInfo(kGame.getGameSpeedType()).getTrainPercent();
			iTimeModifier /= 150;

			FAssert(iTimeModifier >= 0);
		}

		bool bEnemyVictoryLevel4 = GET_TEAM(eLoopTeam).AI_anyMemberAtVictoryStage4();

		if (AI_getWarPlan(eLoopTeam) == WARPLAN_PREPARING_LIMITED)
		{
			FAssert(canEventuallyDeclareWar(eLoopTeam));

			if (AI_getWarPlanStateCounter(eLoopTeam) > ((5 * iTimeModifier) / (bEnemyVictoryLevel4 ? 400 : 100)))
			{
				if (AI_startWarVal(eLoopTeam, WARPLAN_LIMITED) > 0) // K-Mod. Last chance to change our mind if circumstances have changed
				{
					AI_setWarPlan(eLoopTeam, WARPLAN_LIMITED);
					if (gTeamLogLevel >= 1) logBBAI("    Team %d (%S) switching WARPLANS against team %d (%S) from PREPARING_LIMITED to LIMITED after %d turns with enemy power percent %d", getID(), GET_PLAYER(getLeaderID()).getCivilizationDescription(0), eLoopTeam, GET_PLAYER(GET_TEAM(eLoopTeam).getLeaderID()).getCivilizationDescription(0), AI_getWarPlanStateCounter(eLoopTeam), iEnemyPowerPercent);
				}
				else
				{	// advc.001: Actually abandon the war plan
					AI_setWarPlan(eLoopTeam, NO_WARPLAN);
					if (gTeamLogLevel >= 1) logBBAI("    Team %d (%S) abandoning WARPLAN_LIMITED against team %d (%S) after %d turns with enemy power percent %d", getID(), GET_PLAYER(getLeaderID()).getCivilizationDescription(0), eLoopTeam, GET_PLAYER(GET_TEAM(eLoopTeam).getLeaderID()).getCivilizationDescription(0), AI_getWarPlanStateCounter(eLoopTeam), iEnemyPowerPercent);
				}
			}
		}
		else if (AI_getWarPlan(eLoopTeam) == WARPLAN_LIMITED || AI_getWarPlan(eLoopTeam) == WARPLAN_DOGPILE)
		{
			if (!isAtWar(eLoopTeam))
			{	// advc: Moved into a subroutine
				AI_abandonWarPlanIfTimedOut(iAbandonTimeModifier, eLoopTeam, true, iEnemyPowerPercent);
			}
		}
		else if (AI_getWarPlan(eLoopTeam) == WARPLAN_PREPARING_TOTAL)
		{
			FAssert(canEventuallyDeclareWar(eLoopTeam));
			if (AI_getWarPlanStateCounter(eLoopTeam) > ((10 * iTimeModifier) / (bEnemyVictoryLevel4 ? 400 : 100)))
			{
				bool bAreaValid = false;
				bool bShareValid = false;

				FOR_EACH_AREA(pLoopArea)
				{
					if (AI_isPrimaryArea(*pLoopArea))
					{
						if (GET_TEAM(eLoopTeam).countNumCitiesByArea(*pLoopArea) > 0)
						{
							bShareValid = true;

							AreaAITypes eAreaAI = AI_calculateAreaAIType(*pLoopArea, true);

							/* BBAI code
							if (eAreaAI == AREAAI_DEFENSIVE)
								bAreaValid = false;
							else if (eAreaAI == AREAAI_OFFENSIVE)
								bAreaValid = true;*/
							// K-Mod. Doing it that way means the order the areas are checked is somehow important...
							if (eAreaAI == AREAAI_OFFENSIVE)
							{
								bAreaValid = true; // require at least one offense area
							}
							else if (eAreaAI == AREAAI_DEFENSIVE)
							{
								bAreaValid = false;
								break; // false if there are _any_ defence areas
							}
							// K-Mod end
						}
					}
				}

				if (((bAreaValid && iEnemyPowerPercent < 140 ||
					!bShareValid && iEnemyPowerPercent < 110 ||
					GET_TEAM(eLoopTeam).AI_getLowestVictoryCountdown() >= 0) &&
					AI_startWarVal(eLoopTeam, WARPLAN_TOTAL) > 0)) // K-Mod. Last chance to change our mind if circumstances have changed
				{
					AI_setWarPlan(eLoopTeam, WARPLAN_TOTAL);
					if (gTeamLogLevel >= 1) logBBAI("    Team %d (%S) switching WARPLANS against team %d (%S) from PREPARING_TOTAL to TOTAL after %d turns with enemy power percent %d", getID(), GET_PLAYER(getLeaderID()).getCivilizationDescription(0), eLoopTeam, GET_PLAYER(GET_TEAM(eLoopTeam).getLeaderID()).getCivilizationDescription(0), AI_getWarPlanStateCounter(eLoopTeam), iEnemyPowerPercent);
				}
				else if (AI_getWarPlanStateCounter(eLoopTeam) > ((20 * iAbandonTimeModifier) / 100))
				{
					AI_setWarPlan(eLoopTeam, NO_WARPLAN);
					if (gTeamLogLevel >= 1) logBBAI("    Team %d (%S) abandoning WARPLAN_TOTAL_PREPARING against team %d (%S) after %d turns with enemy power percent %d", getID(), GET_PLAYER(getLeaderID()).getCivilizationDescription(0), eLoopTeam, GET_PLAYER(GET_TEAM(eLoopTeam).getLeaderID()).getCivilizationDescription(0), AI_getWarPlanStateCounter(eLoopTeam), iEnemyPowerPercent);
				}
			}
		}
		else if (AI_getWarPlan(eLoopTeam) == WARPLAN_TOTAL && !isAtWar(eLoopTeam))
		{	// advc: Moved into a subroutine
			AI_abandonWarPlanIfTimedOut(iAbandonTimeModifier, eLoopTeam, false, iEnemyPowerPercent);
		}
	}

	// K-Mod. This is the end of the basics updates.
	// The rest of the stuff is related to making peace deals, and planning future wars.
	if (isHuman() || !isMajorCiv() || isAVassal())
		return;
	// K-Mod end

	for (MemberAIIter it(getID()); it.hasNext(); ++it)
		it->AI_doPeace();

	int iNumMembers = getNumMembers();
	/*int iHighUnitSpendingPercent = 0;
	int iLowUnitSpendingPercent = 0;
	for (MemberIter it(getID()); it.hasNext(); ++it) {
		int iUnitSpendingPercent = (it->calculateUnitCost() * 100) / std::max(1, it->calculatePreInflatedCosts());
		iHighUnitSpendingPercent += (std::max(0, iUnitSpendingPercent - 7) / 2);
		iLowUnitSpendingPercent += iUnitSpendingPercent;
	}
	iHighUnitSpendingPercent /= iNumMembers;
	iLowUnitSpendingPercent /= iNumMembers;*/ // K-Mod: BtS code; was unused.

	// K-Mod. Gather some data...
	bool bAtWar = false;
	bool bTotalWarPlan = false;
	bool bAnyWarPlan = false;
	bool bLocalWarPlan = false;
	for (TeamIter<MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> it(getID()); it.hasNext(); ++it)
	{
		TeamTypes eEnemy = it->getID();

		bAtWar = (bAtWar || isAtWar(eEnemy));
		switch (AI_getWarPlan(eEnemy))
		{
		case NO_WARPLAN:
			break;
		case WARPLAN_PREPARING_TOTAL:
		case WARPLAN_TOTAL:
			bTotalWarPlan = true;
			// (advc: fallthrough probably deliberate)
		default: // all other warplans
			bLocalWarPlan = (bLocalWarPlan || AI_isLandTarget(eEnemy));
			bAnyWarPlan = true;
		}
	} // K-Mod end

	// if at war, check for making peace
	// Note: this section relates to automatic peace deals for inactive wars.
	if (bAtWar && SyncRandOneChanceIn(AI_makePeaceRand()))
	{
		for (TeamIter<MAJOR_CIV,ENEMY_OF> itEnemy(getID()); itEnemy.hasNext(); ++itEnemy)
		{
			TeamTypes eEnemy = itEnemy->getID();
			if (GET_TEAM(eEnemy).isHuman())
				continue;
			if (!AI_isChosenWar(eEnemy))
				continue;
			if (!canContact(eEnemy, true))
				continue;

			if (AI_getAtWarCounter(eEnemy) > std::max(10,
				// advc.252: Was VictoryDelay. I don't think we should be this patient.
				(14 * GC.getInfo(kGame.getGameSpeedType()).getTrainPercent()) / 100))
			{
				// If nothing is happening in war
				if (AI_getWarSuccess(eEnemy) + GET_TEAM(eEnemy).AI_getWarSuccess(getID()) <
					2 * GC.getDefineINT(CvGlobals::WAR_SUCCESS_ATTACKING))
				{
					if (SyncRandOneChanceIn(8))
					{
						bool bNoFighting = true;
						for (MemberAIIter itOurMember(getID());
							itOurMember.hasNext(); ++itOurMember)
						{
							if (itOurMember->AI_isAnyEnemyTargetMission(eEnemy))
							{
								bNoFighting = false;
								break;
							}
						}
						if (bNoFighting)
						{
							for (MemberAIIter itEnemyMember(eEnemy);
								itEnemyMember.hasNext(); ++itEnemyMember)
							{
								if (itEnemyMember->AI_isAnyEnemyTargetMission(getID()))
								{
									bNoFighting = false;
									break;
								}
							}
						}
						if (bNoFighting)
						{
							makePeace(eEnemy);
							if (gTeamLogLevel >= 1) logBBAI("  Team %d (%S) making peace due to time and no fighting", getID(), GET_PLAYER(getLeaderID()).getCivilizationDescription(0));
							continue;
						}
					}
				}

				// Fought to a long draw
				if (AI_getAtWarCounter(eEnemy) > ((AI_getWarPlan(eEnemy) == WARPLAN_TOTAL ? 40 : 30) *
					// advc.252: was VictoryDelay
					GC.getInfo(kGame.getGameSpeedType()).getTrainPercent()) / 100)
				{
					int iOurValue = AI_endWarVal(eEnemy);
					int iTheirValue = GET_TEAM(eEnemy).AI_endWarVal(getID());
					// advc: Took these inequations times 2 to reduce rounding errors
					if (2 * iOurValue > iTheirValue && 2 * iTheirValue > iOurValue)
					{
						if (gTeamLogLevel >= 1) logBBAI("  Team %d (%S) making peace due to time and endWarVal %d vs their %d", getID(), GET_PLAYER(getLeaderID()).getCivilizationDescription(0) , iOurValue, iTheirValue);
						makePeace(eEnemy);
						continue;
					}
				}

				// All alone in what we thought was a dogpile
				if (AI_getWarPlan(eEnemy) == WARPLAN_DOGPILE)
				{
					if (GET_TEAM(eEnemy).getNumWars(true) == 1)
					{
						int iOurValue = AI_endWarVal(eEnemy);
						int iTheirValue = GET_TEAM(eEnemy).AI_endWarVal(getID());
						if (2 * iTheirValue > iOurValue) // advc: *2 (see previous comment)
						{
							if (gTeamLogLevel >= 1) logBBAI("  Team %d (%S) making peace due to being only dog-piler left", getID(), GET_PLAYER(getLeaderID()).getCivilizationDescription(0));
							makePeace(eEnemy);
							continue;
						}
					}
				}
			}
		}
	}

	// if no war plans, consider starting one!

	//if (getAnyWarPlanCount(true) == 0 || iEnemyPowerPercent < 45)
	// K-Mod. Some more nuance to the conditions for considering war
	/*	First condition: only consider a new war if there are no current wars
		that need more attention. (local total war, or a war we aren't winning) */
	bool bConsiderWar = (!bAnyWarPlan ||
			(iEnemyPowerPercent < 45 && !(bLocalWarPlan && bTotalWarPlan) &&
			AI_getWarSuccessRating() > (bTotalWarPlan ? 40 : 15)));
	/*	Second condition: don't consider war very early in the game. It would be unfair
		on human players to rush them with our extra starting units and techs! */
	bConsiderWar = (bConsiderWar &&
			(kGame.isOption(GAMEOPTION_AGGRESSIVE_AI) ||
			 kGame.getElapsedGameTurns() * 100 >=
			 GC.getInfo(kGame.getGameSpeedType()).getBarbPercent() * 30 ||
			 kGame.getNumCivCities() * 2 >
			 GC.getInfo(GC.getMap().getWorldSize()).getTargetNumCities() *
			 kGame.countCivPlayersAlive()));
	/*	(Perhaps the no-war turn threshold should depend on the game difficulty level;
		but I don't think it would make much difference.) */

	if (bConsiderWar)
	// K-Mod end
	{
		bool bAggressive = kGame.isOption(GAMEOPTION_AGGRESSIVE_AI);

		int iFinancialTroubleCount = 0;
		int iDaggerCount = 0;
		int iGetBetterUnitsCount = 0;
		for (MemberAIIter it(getID()); it.hasNext(); ++it)
		{
			CvPlayerAI& kMember = *it;
			if (kMember.AI_isDoStrategy(AI_STRATEGY_DAGGER) ||
				// <BBAI>
				kMember.AI_atVictoryStage(AI_VICTORY_CONQUEST3) ||
				kMember.AI_atVictoryStage(AI_VICTORY_DOMINATION4)) // </BBAI>
			{
				iDaggerCount++;
				bAggressive = true;
			}
			if (kMember.AI_isDoStrategy(AI_STRATEGY_GET_BETTER_UNITS))
				iGetBetterUnitsCount++;

			if (kMember.AI_isFinancialTrouble())
				iFinancialTroubleCount++;
		}

		// if random in this range is 0, we go to war of this type (so lower numbers are higher probability)
		// average of everyone on our team
		int iTotalWarRand;
		int iLimitedWarRand;
		int iDogpileWarRand;
		AI_getWarRands(iTotalWarRand, iLimitedWarRand, iDogpileWarRand);

		int iTotalWarThreshold;
		int iLimitedWarThreshold;
		int iDogpileWarThreshold;
		AI_getWarThresholds(iTotalWarThreshold, iLimitedWarThreshold, iDogpileWarThreshold);

		// we oppose war if half the non-dagger teammates in financial trouble
		bool bFinancesOpposeWar = false;
		if (iFinancialTroubleCount - iDaggerCount >= std::max(1, getNumMembers() / 2))
		{
			// this can be overridden by by the pro-war booleans
			bFinancesOpposeWar = true;
		}

		// if aggressive, we may start a war to get money
		bool bFinancesProTotalWar = false;
		bool bFinancesProLimitedWar = false;
		bool bFinancesProDogpileWar = false;
		if (iFinancialTroubleCount > 0)
		{
			// do we like all out wars?
			if (iDaggerCount > 0 || iTotalWarRand < 100)
				bFinancesProTotalWar = true;

			// do we like limited wars?
			if (iLimitedWarRand < 100)
				bFinancesProLimitedWar = true;

			// do we like dogpile wars?
			if (iDogpileWarRand < 100)
				bFinancesProDogpileWar = true;
		}
		bool bFinancialProWar = (bFinancesProTotalWar || bFinancesProLimitedWar || bFinancesProDogpileWar);

		// overall war check (quite frequently true)
		bool bMakeWarChecks = false;
		if ((iGetBetterUnitsCount - iDaggerCount) * 3 < iNumMembers * 2)
		{
			if (bFinancialProWar || !bFinancesOpposeWar)
			{	// random overall war chance
				if (SyncRandSuccess100(GC.getInfo(kGame.getHandicapType()).
					getAIDeclareWarProb())) // (at noble+ difficulties this is 100%)
				{
					bMakeWarChecks = true;
				}
			}
		}

		if (bMakeWarChecks)
		{
			int iOurPower = getPower(true);

			if (bAggressive && !AI_isAnyWarPlan())
			{
				iOurPower *= 4;
				iOurPower /= 3;
			}

			iOurPower *= (100 - iEnemyPowerPercent);
			iOurPower /= 100;

			if ((bFinancesProTotalWar || !bFinancesOpposeWar) &&
				SyncRandNum(iTotalWarRand) <= iTotalWarThreshold)
			{
				int iNoWarRoll = SyncRandNum(100);
				iNoWarRoll = range(iNoWarRoll + (bAggressive ? 10 : 0) +
						(bFinancesProTotalWar ? 10 : 0)
						- (20*iGetBetterUnitsCount)/iNumMembers, 0, 99);
				// advc (note): This loop is mostly duplicated in the two "else if" branches below
				TeamTypes eBestTarget = NO_TEAM;
				/*	K-Mod. I've set the starting value above zero just as a buffer
					against close-calls which end up being negative value
					in the near future. */
				int iBestValue = 10;
				for (int iPass = 0; iPass < 3; iPass++)
				{
					for (TeamIter<MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> it(getID()); it.hasNext(); ++it)
					{
						TeamTypes eTarget = it->getID();
						if (!canEventuallyDeclareWar(eTarget) || !AI_haveSeenCities(eTarget))
							continue;
						// K-Mod (plus all changes which refer to this variable).
						TeamTypes const eLoopMasterTeam = GET_TEAM(eTarget).getMasterTeam();
						bool bVassal = (eLoopMasterTeam != eTarget);
						if (bVassal && !AI_isOkayVassalTarget(eTarget))
							continue;

						if (iNoWarRoll >= AI_noWarAttitudeProb(AI_getAttitude(eTarget)) &&
							(!bVassal || iNoWarRoll >= AI_noWarAttitudeProb(AI_getAttitude(eLoopMasterTeam))))
						{
							int iDefensivePower = (GET_TEAM(eTarget).getDefensivePower(getID()) * 2) / 3;
							if (iDefensivePower < ((iOurPower * (iPass > 1 ?
								AI_maxWarDistantPowerRatio() : AI_maxWarNearbyPowerRatio())) / 100))
							{
								// XXX make sure they share an area....
								if ((iPass > 1 && !bLocalWarPlan) || AI_isLandTarget(eTarget) ||
									AI_isAnyCapitalAreaAlone() ||
									GET_TEAM(eTarget).AI_anyMemberAtVictoryStage4())
								{
									if (iPass > 0 || AI_calculateAdjacentLandPlots(eTarget) >=
										(getTotalLand() * AI_maxWarMinAdjacentLandPercent()) / 100 ||
										GET_TEAM(eTarget).AI_anyMemberAtVictoryStage4())
									{
										int iValue = AI_startWarVal(eTarget, WARPLAN_TOTAL);
										if (gTeamLogLevel >= 2 && iValue > 0) logBBAI("    Team %d (%S) considering starting TOTAL warplan with team %d with value %d on pass %d with %d adjacent plots", getID(), GET_PLAYER(getLeaderID()).getCivilizationDescription(0), eTarget, iValue, iPass, AI_calculateAdjacentLandPlots(eTarget));

										if (iValue > iBestValue)
										{
											iBestValue = iValue;
											eBestTarget = eTarget;
										}
									}
								}
							}
						}
					}

					if (eBestTarget != NO_TEAM)
					{
						if (gTeamLogLevel >= 1) logBBAI("    Team %d (%S) starting TOTAL warplan preparations against team %d on pass %d", getID(), GET_PLAYER(getLeaderID()).getCivilizationDescription(0), eBestTarget, iPass);
						AI_setWarPlan(eBestTarget, iDaggerCount > 0 ?
								WARPLAN_TOTAL : WARPLAN_PREPARING_TOTAL);
						break;
					}
				}
			}
			else if ((bFinancesProLimitedWar || !bFinancesOpposeWar) &&
				// UNOFFICIAL_PATCH, Bugfix, 01/02/09, jdog5000: (right side was 0)
				SyncRandNum(iLimitedWarRand) <= iLimitedWarThreshold)
			{
				int iNoWarRoll = SyncRandNum(100) - 10;
				iNoWarRoll = range(iNoWarRoll + (bAggressive ? 10 : 0) +
						(bFinancesProLimitedWar ? 10 : 0), 0, 99);
				TeamTypes eBestTarget = NO_TEAM;
				int iBestValue = 0;
				for (TeamIter<MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> it(getID()); it.hasNext(); ++it)
				{
					TeamTypes eTarget = it->getID();
					if (!canEventuallyDeclareWar(eTarget) || !AI_haveSeenCities(eTarget))
						continue;

					TeamTypes eLoopMasterTeam = GET_TEAM(eTarget).getMasterTeam(); // K-Mod (plus all changes which refer to this variable).
					bool bVassal = (eLoopMasterTeam != eTarget);
					if (bVassal && !AI_isOkayVassalTarget(eTarget))
						continue;

					if (iNoWarRoll >= AI_noWarAttitudeProb(AI_getAttitude(eTarget)) &&
						(!bVassal || iNoWarRoll >= AI_noWarAttitudeProb(AI_getAttitude(eLoopMasterTeam))))
					{
						if (AI_isLandTarget(eTarget) || (AI_isAnyCapitalAreaAlone() &&
							GET_TEAM(eTarget).AI_isAnyCapitalAreaAlone()))
						{
							if (GET_TEAM(eTarget).getDefensivePower(getID()) <
								(iOurPower * AI_limitedWarPowerRatio()) / 100)
							{
								int iValue = AI_startWarVal(eTarget, WARPLAN_LIMITED);
								if (gTeamLogLevel >= 2 && iValue > 0) logBBAI("    Team %d (%S) considering starting LIMITED warplan with team %d with value %d", getID(), GET_PLAYER(getLeaderID()).getCivilizationDescription(0), eTarget, iValue);
								if (iValue > iBestValue)
								{
									//FAssert(!AI_shareWar(eTarget)); // disabled by K-Mod. (It isn't always true.)
									iBestValue = iValue;
									eBestTarget = eTarget;
								}
							}
						}
					}
				}

				if (eBestTarget != NO_TEAM)
				{
					if (gTeamLogLevel >= 1) logBBAI("    Team %d (%S) starting LIMITED warplan preparations against team %d", getID(), GET_PLAYER(getLeaderID()).getCivilizationDescription(0), eBestTarget);
					AI_setWarPlan(eBestTarget, iDaggerCount > 0 ?
							WARPLAN_LIMITED : WARPLAN_PREPARING_LIMITED);
				}
			}
			else if ((bFinancesProDogpileWar || !bFinancesOpposeWar) &&
				SyncRandNum(iDogpileWarRand) <= iDogpileWarThreshold)
			{
				int iNoWarRoll = SyncRandNum(100) - 20;
				iNoWarRoll = range(iNoWarRoll + (bAggressive ? 10 : 0) +
						(bFinancesProDogpileWar ? 10 : 0), 0, 99);
				TeamTypes eBestTarget = NO_TEAM;
				int iBestValue = 0;
				for (TeamIter<MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> itTarget(getID());
					itTarget.hasNext(); ++itTarget)
				{
					TeamTypes eTarget = itTarget->getID();
					if (!canDeclareWar(eTarget) || !AI_haveSeenCities(eTarget))
						continue;
					// K-Mod (plus all changes which refer to this variable).
					TeamTypes eLoopMasterTeam = GET_TEAM(eTarget).getMasterTeam();
					bool bVassal = (eLoopMasterTeam != eTarget);
					if (bVassal && !AI_isOkayVassalTarget(eTarget))
						continue;

					if (iNoWarRoll >= AI_noWarAttitudeProb(AI_getAttitude(eTarget)) &&
						(!bVassal || iNoWarRoll >= AI_noWarAttitudeProb(AI_getAttitude(eLoopMasterTeam))))
					{
						if (GET_TEAM(eTarget).getNumWars() <= 0)
							continue;

						if (AI_isLandTarget(eTarget) ||
							GET_TEAM(eTarget).AI_anyMemberAtVictoryStage4())
						{
							int iDogpilePower = iOurPower;
							// advc.001: Shouldn't count minor civs
							for (TeamIter<MAJOR_CIV,ENEMY_OF> itDog(eTarget); itDog.hasNext(); ++itDog)
							{
								// <advc.001> Don't cheat
								if (!isHasMet(itDog->getID()))
									continue; // </advc.001>
								iDogpilePower += itDog->getPower(false);
							}
							// kekm.3 (advc): No longer holds I think; the target could have a DP despite being at war
							//FAssert(bVassal || GET_TEAM(eTarget).getPower(true) == GET_TEAM(eTarget).getDefensivePower(getID()));
							if ((GET_TEAM(eTarget).getDefensivePower(getID()) * 3) / 2 < iDogpilePower)
							{
								int iValue = AI_startWarVal(eTarget, WARPLAN_DOGPILE);
								if (iValue > 0 && gTeamLogLevel >= 2) logBBAI("    Team %d (%S) considering starting DOGPILE warplan with team %d with value %d", getID(), GET_PLAYER(getLeaderID()).getCivilizationDescription(0), eTarget, iValue);
								if (iValue > iBestValue)
								{
									//FAssert(!AI_shareWar((TeamTypes)iI)); // disabled by K-Mod. (why is this even here?)
									iBestValue = iValue;
									eBestTarget = eTarget;
								}
							}
						}
					}
				}
				if (eBestTarget != NO_TEAM)
				{
					if (gTeamLogLevel >= 1) logBBAI("  Team %d (%S) starting DOGPILE warplan preparations with team %d", getID(), GET_PLAYER(getLeaderID()).getCivilizationDescription(0), eBestTarget);
					AI_setWarPlan(eBestTarget, WARPLAN_DOGPILE);
				}
			}
		}
	}
}

//returns true if war is veto'd by rolls.
bool CvTeamAI::AI_performNoWarRolls(TeamTypes eTeam)
{
	return (!SyncRandSuccess100(
			GC.getInfo(GC.getGame().getHandicapType()).getAIDeclareWarProb()) ||
			SyncRandSuccess100(
			AI_noWarAttitudeProb(AI_getAttitude(eTeam))));
}


int CvTeamAI::AI_getAttitudeWeight(TeamTypes eTeam) const
{
	switch (AI_getAttitude(eTeam))
	{
	case ATTITUDE_FURIOUS: return -100;
	case ATTITUDE_ANNOYED: return -40;
	case ATTITUDE_CAUTIOUS: return -5;
	case ATTITUDE_PLEASED: return 50;
	case ATTITUDE_FRIENDLY: return 100;
	default: FErrorMsg("unknown attitude type"); return 0;
	}
}

int CvTeamAI::AI_getLowestVictoryCountdown() const
{
	int iBestVictoryCountdown = MAX_INT;
	for (int iVictory = 0; iVictory < GC.getNumVictoryInfos(); iVictory++)
	{
		 int iCountdown = getVictoryCountdown((VictoryTypes)iVictory);
		 if (iCountdown > 0)
			iBestVictoryCountdown = std::min(iBestVictoryCountdown, iCountdown);
	}
	if (iBestVictoryCountdown == MAX_INT)
		iBestVictoryCountdown = -1;
	return iBestVictoryCountdown;
}


int CvTeamAI::AI_getTechMonopolyValue(TechTypes eTech, TeamTypes eTeam) const
{
	PROFILE_FUNC(); // advc: called not that infrequently
	//bool bWarPlan = (getAnyWarPlanCount(eTeam) > 0);
	bool const bWarPlan = (AI_getWarPlan(eTeam) != NO_WARPLAN); // advc.001
	int iValue = 0;
	// <advc.550c> Evaluate each team member so that UU and UB can be taken into account
	MemberIter it(eTeam);
	for (; it.hasNext(); ++it)
	{
		CvCivilization const& kRecipientCiv = it->getCivilization();
		for (int i = 0; i < kRecipientCiv.getNumUnits(); i++)
		{
			UnitTypes eUnit = kRecipientCiv.unitAt(i); // </advc.550c>
			CvUnitInfo const& kUnit = GC.getInfo(eUnit);
			if (!kUnit.isTechRequired(eTech))
				continue;

			if (kUnit.isWorldUnit())
				iValue += 50;

			/*  advc (comment): Relying only on the AndTech seems questionable. Anything
				that the canTrain functions check could be relevant here. */
			if (kUnit.getPrereqAndTech() != eTech)
				continue;

			int iNavalValue = 0;
			int iCombatRatio = (kUnit.getCombat() * 100) /
					std::max(1, GC.getGame().getBestLandUnitCombat());
			if (iCombatRatio > 50)
				iValue += (bWarPlan ? 2 : 1) * (iCombatRatio - 40);

			switch (kUnit.getDefaultUnitAIType())
			{
			case UNITAI_UNKNOWN:
			case UNITAI_ANIMAL:
			case UNITAI_SETTLE:
			case UNITAI_WORKER:
				break;
			case UNITAI_ATTACK:
			case UNITAI_ATTACK_CITY:
			case UNITAI_COLLATERAL:
				iValue += bWarPlan ? 50 : 20;
				break;
			case UNITAI_PILLAGE:
			case UNITAI_RESERVE:
			case UNITAI_COUNTER:
			case UNITAI_PARADROP:
			case UNITAI_CITY_DEFENSE:
			case UNITAI_CITY_COUNTER:
			case UNITAI_CITY_SPECIAL:
				iValue += bWarPlan ? 40 : 15;
				break;
			case UNITAI_EXPLORE:
			case UNITAI_MISSIONARY:
			case UNITAI_PERSECUTOR: // doc
				break;
			case UNITAI_PROPHET:
			case UNITAI_ARTIST:
			case UNITAI_SCIENTIST:
			case UNITAI_GENERAL:
			case UNITAI_MERCHANT:
			case UNITAI_ENGINEER:
			case UNITAI_STATESMAN: // doc
			case UNITAI_GREAT_SPY: // K-Mod
				break;
			case UNITAI_SPY:
				break;
			case UNITAI_ICBM:
				iValue += bWarPlan ? 80 : 40;
				break;
			case UNITAI_WORKER_SEA:
				break;
			case UNITAI_ATTACK_SEA:
				iNavalValue += 50;
				break;
			case UNITAI_RESERVE_SEA:
			case UNITAI_ESCORT_SEA:
				iNavalValue += 30;
				break;
			case UNITAI_EXPLORE_SEA:
				iValue += GC.getGame().circumnavigationAvailable() ? 100 : 0;
				break;
			case UNITAI_ASSAULT_SEA:
				iNavalValue += 60;
				break;
			case UNITAI_SETTLER_SEA:
			case UNITAI_MISSIONARY_SEA:
			case UNITAI_SPY_SEA:
				break;
			case UNITAI_CARRIER_SEA:
			case UNITAI_MISSILE_CARRIER_SEA:
				iNavalValue += 40;
				break;
			case UNITAI_PIRATE_SEA:
				iNavalValue += 20;
				break;
			case UNITAI_ATTACK_AIR:
			case UNITAI_DEFENSE_AIR:
				iValue += bWarPlan ? 60 : 30;
				break;
			case UNITAI_CARRIER_AIR:
				iNavalValue += 40;
				break;
			case UNITAI_MISSILE_AIR:
				iValue += bWarPlan ? 40 : 20;
				break;
			case UNITAI_SATELLITE:
				iValue += 50;
				break;
			default:
				FAssert(false);
				break;
			}
			if (iNavalValue > 0)
			{
				if (AI_isAnyCapitalAreaAlone())
					iValue += iNavalValue / 2;
				if (bWarPlan && !AI_isLandTarget(eTeam))
					iValue += iNavalValue / 2;
			}
		}
		// <advc.550c>
		for (int i = 0; i < kRecipientCiv.getNumBuildings(); i++)
		{
			BuildingTypes eBuilding = kRecipientCiv.buildingAt(i); // </advc.550c>
			CvBuildingInfo const& kBuilding = GC.getInfo(eBuilding);
			if (!kBuilding.isTechRequired(eTech))
				continue;
			if (kBuilding.getReligionType() == NO_RELIGION)
				iValue += 20; // advc.550c: was 30
			if (kBuilding.isWorldWonder() && !GC.getGame().isBuildingClassMaxedOut(
				CvCivilization::buildingClass(eBuilding)))
			{
				iValue += 40; // advc.550c: was 50
			}
		}
	}
	// advc.550c: Or perhaps divide by the sqrt?
	iValue /= std::max(1, it.nextIndex());
	FOR_EACH_ENUM(Project)
	{
		if (GC.getInfo(eLoopProject).getTechPrereq() != eTech)
			continue;
		if (GC.getInfo(eLoopProject).isWorldProject() &&
			!GC.getGame().isProjectMaxedOut(eLoopProject))
		{
			iValue += 80; // advc.550c: was 100
		}
		else iValue += 40; // advc.550c: was 50
	}
	return iValue;
}


bool CvTeamAI::AI_isWaterAreaRelevant(CvArea const& kArea) const
{
	//PROFILE_FUNC(); // advc: Not frequently called currently

	CvArea* pBiggestArea = GC.getMap().findBiggestArea(true);
	if (pBiggestArea == &kArea)
		return true;

	// An area is deemed relevant if it has at least 2 cities of our and different teams.

	// advc: Rewrote the rest of this function; hopefully clearer.
	int iTeamCities = 0;
	int iOtherTeamCities = 0;
	int const iTargetCities = 2;
	// advc.131: Count our vassals under iTeamCities
	for (PlayerIter<ALIVE,NOT_A_RIVAL_OF> it(getID()); it.hasNext(); ++it)
	{
		FOR_EACH_CITY(pLoopCity, *it)
		{
			if (!pLoopCity->getPlot().isAdjacentToArea(kArea))
				continue;
			/*  BETTER_BTS_AI_MOD, City AI, 01/15/09, jdog5000:
				Also count lakes which are connected to ocean by a bridge city */
			if (pLoopCity->waterArea() == pBiggestArea)
				return true;
			iTeamCities++;
			if (iTeamCities >= iTargetCities)
				goto afterAlliesLoop;
		}
	}
	afterAlliesLoop:
	for (PlayerIter<ALIVE,KNOWN_POTENTIAL_ENEMY_OF> it(getID()); it.hasNext(); ++it)
	{
		FOR_EACH_CITY(pLoopCity, *it)
		{
			if (!pLoopCity->getPlot().isAdjacentToArea(kArea))
				continue;
			// <advc.001> Don't cheat
			if (!AI_deduceCitySite(*pLoopCity))
				continue; // </advc.001>
			iOtherTeamCities++;
			if (iOtherTeamCities >= iTargetCities)
				goto afterRivalsLoop;
		}
	}
	afterRivalsLoop:
	return (std::min(iTeamCities, iOtherTeamCities) >= iTargetCities);
}
