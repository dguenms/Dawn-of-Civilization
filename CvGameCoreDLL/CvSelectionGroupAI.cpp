#include "CvGameCoreDLL.h"
#include "CvSelectionGroupAI.h"
#include "CvUnitAI.h"
// <advc.004c> for AI_bestUnitForMission
#include "CvUnit.h"
#include "CvCityAI.h" // </advc.004c>
#include "CvPlayerAI.h"
#include "CvTeamAI.h"
#include "AgentIterator.h"
#include "CvMap.h"


CvSelectionGroupAI::CvSelectionGroupAI()
{
	AI_reset();
}


CvSelectionGroupAI::~CvSelectionGroupAI()
{
	AI_uninit();
}


void CvSelectionGroupAI::AI_init()
{
	AI_reset();
}


void CvSelectionGroupAI::AI_uninit() {}


void CvSelectionGroupAI::AI_reset()
{
	AI_uninit();

	m_iMissionAIX = INVALID_PLOT_COORD;
	m_iMissionAIY = INVALID_PLOT_COORD;

	m_bForceSeparate = false;

	m_eMissionAIType = NO_MISSIONAI;

	m_missionAIUnit.reset();

	m_bGroupAttack = false;
	m_iGroupAttackX = -1;
	m_iGroupAttackY = -1;
}

// these separate function have been tweaked by K-Mod and bbai.
void CvSelectionGroupAI::AI_separate()
{
	FOR_EACH_UNIT_VAR_IN(pUnit, *this)
	{
		pUnit->joinGroup(NULL);
	}
}


void CvSelectionGroupAI::AI_separateNonAI(UnitAITypes eUnitAI)
{
	FOR_EACH_UNIT_VAR_IN(pUnit, *this)
	{
		if (pUnit->AI_getUnitAIType() != eUnitAI)
			pUnit->joinGroup(NULL);
	}
}


void CvSelectionGroupAI::AI_separateAI(UnitAITypes eUnitAI)
{
	FOR_EACH_UNIT_VAR_IN(pUnit, *this)
	{
		if (pUnit->AI_getUnitAIType() == eUnitAI)
			pUnit->joinGroup(NULL);
	}
}


bool CvSelectionGroupAI::AI_separateImpassable()
{
	CvPlayerAI& kPlayer = GET_PLAYER(getOwner());
	bool bSeparated = false;
	FOR_EACH_UNIT_VAR_IN(pUnit, *this)
	{
		if (kPlayer.AI_isAnyImpassable(pUnit->getUnitType()))
		{
			pUnit->joinGroup(NULL);
			bSeparated = true;
		}
	}
	return bSeparated;
}


bool CvSelectionGroupAI::AI_separateEmptyTransports()
{
	bool bSeparated = false;
	FOR_EACH_UNIT_VAR_IN(pUnit, *this)
	{
		if (pUnit->AI_getUnitAIType() == UNITAI_ASSAULT_SEA &&
			!pUnit->hasCargo())
		{
			pUnit->joinGroup(NULL);
			bSeparated = true;
		}
	}
	return bSeparated;
} // bbai / K-Mod end

// Returns true if the group has become busy
bool CvSelectionGroupAI::AI_update()
{
	PROFILE_FUNC();

	FAssert(getOwner() != NO_PLAYER);

	if (!isAIControlled())
		return false;

	if (getNumUnits() == 0)
		return false;

	// K-Mod. (replacing the original "isForceUpdate" stuff.)
	if (isForceUpdate())
	{
		// note: we haven't toggled the update flag, nor woken the group from sleep.
		AI_cancelGroupAttack();
	} // K-Mod end

	//FAssert(!(GET_PLAYER(getOwner()).isAutoMoves())); // (no longer true in K-Mod)

	//int iTempHack = 0; // XXX
	// <advc.001y> Will keep this permanently as a fallback
	int iAttempts = 0;
	int iMaxAttempts = 6 * (GET_PLAYER(getOwner()).getCurrentEra() + 1) +
			std::max(getNumUnits(), 4);
#ifdef _DEBUG
	iMaxAttempts += 4; // Extra iterations for debugging
#endif
	// </advc.001y>
	bool bDead = false;
	bool bFailedAlreadyFighting = false;
	//while ((m_bGroupAttack && !bFailedAlreadyFighting) || readyToMove())
	while ((AI_isGroupAttack() && !isBusy()) || readyToMove()) // K-Mod
	{
		// K-Mod. Force update just means we should get into this loop at least once.
		setForceUpdate(false);
		iAttempts++;
		/*  <advc.001y> Moved out of the block below so I can see what the loop does
			before it terminates. Debugger stops in CvSelectionGroup::pushMission,
			startMission and in CvUnitAI::AI_update have been helpful to me. */
	#ifdef _DEBUG
		iMaxAttempts -= 4; // Trigger assert early
	#endif
		FAssertMsg(iAttempts != iMaxAttempts, "Unit stuck in a loop");
	#ifdef _DEBUG
		iMaxAttempts += 4; // Restore extra iterations
	#endif
		if (iAttempts >= iMaxAttempts) // was > 100 </advc.001y>
		{
			CvUnit* pHeadUnit = getHeadUnit();
			if (pHeadUnit != NULL)
			{	// <advc.001y>
			#ifndef _DEBUG
				if (iAttempts == iMaxAttempts) // Don't spam the log </advc.004y>
					GC.getLogger().logUnitStuck(*pHeadUnit); // advc.003t
			#endif
				pHeadUnit->finishMoves();
			}
			break;
		}

		// if we want to force the group to attack, force another attack
		if (AI_isGroupAttack())
		{
			AI_cancelGroupAttack();
			groupAttack(m_iGroupAttackX, m_iGroupAttackY,
					MOVE_DIRECT_ATTACK, bFailedAlreadyFighting);
		}
		// else pick AI action
		else
		{
			CvUnitAI* pHeadUnit = AI_getHeadUnit();
			//if (pHeadUnit == NULL || pHeadUnit->isDelayedDeath())
			if (pHeadUnit == NULL || pHeadUnit->doDelayedDeath()) // K-Mod
				break;

			//resetPath();
			if (pHeadUnit->AI_update())
			{	// AI_update returns true when we should abort the loop and wait until next slice
				FAssert(!pHeadUnit->isDelayedDeath());
				break;
			}
		}

		if (doDelayedDeath())
		{
			bDead = true;
			break;
		}

		/*	if no longer group attacking, and force separate is true,
			then bail, decide what to do after group is split up */
		// (UnitAI of head unit may have changed)
		if (!AI_isGroupAttack() && AI_isForceSeparate())
		{
			AI_separate();	// pointers could become invalid...
			//return true;
			return false; // K-Mod
		}
	}

	if (!bDead)
	{
		// K-Mod. this is how we deal with force update when some group members can't move.
		if (isForceUpdate())
		{
			setForceUpdate(false);
			AI_cancelGroupAttack();
			setActivityType(ACTIVITY_AWAKE);
		}
		// K-Mod end
		if (!isHuman())
		{
			bool bFollow = false;
			// <k146>
			// if we're not group attacking, then check for 'follow' action
			if (!AI_isGroupAttack() && readyToMove(true))
			{
				/*  What we do here might split the group. So to avoid problems,
					lets make a list of our units. */
				std::vector<IDInfo> originalGroup;
				for(CLLNode<IDInfo> const* pUnitNode = headUnitNode(); pUnitNode != NULL;
					pUnitNode = nextUnitNode(pUnitNode))
 				{
					originalGroup.push_back(pUnitNode->m_data);
				}
				FAssert(originalGroup.size() == getNumUnits());
				bool bFirst = true;
				resetPath();
				for (std::vector<IDInfo>::iterator it = originalGroup.begin();
					it != originalGroup.end(); ++it)
				{
					CvUnitAI* pLoopUnit = ::AI_getUnit(*it);
					if (pLoopUnit && pLoopUnit->getGroupID() == getID() &&
						pLoopUnit->canMove())
					{
						if (pLoopUnit->AI_follow(bFirst))
						{
							bFollow = true;
							bFirst = true; // let the next unit start fresh.
							resetPath();
							if (!readyToMove(true))
								break;
						}
						else bFirst = false;
					}
				} // </k146>
			}

			if (doDelayedDeath())
				bDead = true;

			if (!bDead)
			{
				if (!bFollow && readyToMove(true))
					pushMission(MISSION_SKIP);
			}
		}
	}
	// <advc.test>
	/*if(GC.getRandLogging() && !GC.getGame().checkInSync()) {
		CvUnit* pHeadUnit = getHeadUnit(); // for inspection in debugger
		FAssert(false);
	}*/ // </advc.test>

	if (bDead)
	{	//return true;
		return false; // K-Mod
	}

	return (isBusy() || isCargoBusy());
}

// Returns attack odds out of 100 (the higher, the better...)
int CvSelectionGroupAI::AI_attackOdds(const CvPlot* pPlot, bool bPotentialEnemy) const
{
	PROFILE_FUNC();

	FAssert(getOwner() != NO_PLAYER);
	//if (pPlot->getBestDefender(NO_PLAYER, getOwner(), NULL, !bPotentialEnemy, bPotentialEnemy) == NULL)
	// BETTER_BTS_AI_MOD, Efficiency, Lead From Behind (UncutDragon), 02/21/10, jdog5000:
	if (!pPlot->hasDefender(false, NO_PLAYER, getOwner(),
		NULL, !bPotentialEnemy, bPotentialEnemy))
	{
		return 100;
	}
	int iOdds=-1; // (advc: Was 0. Shouldn't matter.)
	CvUnit* pAttacker = AI_getBestGroupAttacker(pPlot, bPotentialEnemy, iOdds);
	if (pAttacker == NULL)
		return 0;

	return iOdds;
}

/*	K-Mod. A new odds-adjusting function to replace CvUnitAI::AI_finalOddsThreshold.
	(note: I would like to put this in CvSelectionGroupAI ... but - well -
	I don't need to say it, right?)
	advc.003u: I think CvUnitAI::AI_getGroup solves karadoc's problem; so - moved. */
int CvSelectionGroupAI::AI_getWeightedOdds(CvPlot const* pPlot, bool bPotentialEnemy)
{
	PROFILE_FUNC();
	int iOdds=-1;
	CvUnitAI const* pAttacker = AI_getBestGroupAttacker(pPlot, bPotentialEnemy, iOdds);
	if (pAttacker == NULL)
		return 0;
	CvPlot::DefenderFilters defFilters(getOwner(), pAttacker,
			!bPotentialEnemy, bPotentialEnemy,
			true, false); // advc.028, advc.089 (same as in CvUnitAI::AI_attackOdds)
	CvUnit const* pDefender = pPlot->getBestDefender(NO_PLAYER, defFilters);
	if (pDefender == NULL)
		return 100;

	/*	<advc.114b> We shouldn't adjust the odds based on an optimistic estimate
		(increased by AttackOddsChange) b/c that leads to Warriors attacking Tanks -
		high difference in production cost and non-negligible optimistic odds.
		I'm subtracting the AttackOddsChange temporarily;
		adding them back in after the adjustments are done.
		(A more elaborate fix would avoid adding them in the first place.) */
	int const iAttackOddsChange = GET_PLAYER(getOwner()).AI_getAttackOddsChange();
	iOdds -= iAttackOddsChange;
	/*	Require a stack of at least 3 if actual odds are below 1%. Should
		matter mostly for Barbarians, hence only this primitive condition
		(not checking if the other units could actually attack etc.). */
	if(iOdds == 0 && getNumUnits() < 3)
		return 0;
	// </advc.114b>
	// advc: The bulk of the computation is still in CvUnitAI
	int iAdjustedOdds = pAttacker->AI_opportuneOdds(iOdds, *pDefender);

	/*  one more thing... unfortunately, the sea AI isn't evolved enough
		to do without something as painful as this... */
	if (getDomainType() == DOMAIN_SEA && !hasCargo())
	{
		// I'm sorry about this. I really am. I'll try to make it better one day...
		int iDefenders = pAttacker->AI_countEnemyDefenders(*pPlot);
		iAdjustedOdds *= 2 + getNumUnits();
		iAdjustedOdds /= 3 + std::min(iDefenders / 2, getNumUnits());
	}

	iAdjustedOdds += iAttackOddsChange; // advc.114b
	return range(iAdjustedOdds, 1, 99);
}


CvUnitAI* CvSelectionGroupAI::AI_getBestGroupAttacker(const CvPlot* pPlot,
	bool bPotentialEnemy, int& iUnitOdds, bool bForce, bool bNoBlitz,
	// <advc.048>
	bool bSacrifice, bool bMaxSurvival) const
{
	int const iOddsThresh = 68; // Should this be lower if bHuman?
	FAssert(!bMaxSurvival || !bSacrifice); // </advc.048>
	PROFILE_FUNC();

	int iBestValue = 0;
	int iBestOdds = 0;
	CvUnitAI* pBestUnit = NULL;
	CLLNode<IDInfo> const* pUnitNode = headUnitNode();
	bool const bHuman = (pUnitNode == NULL ? true :
			GET_PLAYER(::getUnit(pUnitNode->m_data)->getOwner()).isHuman());
	FAssert(!bMaxSurvival || bHuman); // advc.048
	while (pUnitNode != NULL)
	{
		CvUnitAI& kLoopUnit = *::AI_getUnit(pUnitNode->m_data);
		pUnitNode = nextUnitNode(pUnitNode);

		if (kLoopUnit.isDead())
			continue;

		bool bCanAttack = false;
		if (kLoopUnit.getDomainType() == DOMAIN_AIR)
			bCanAttack = kLoopUnit.canAirAttack();
		else
		{
			bCanAttack = kLoopUnit.canAttack();
			if (bCanAttack && bNoBlitz && kLoopUnit.isBlitz() &&
				kLoopUnit.isMadeAttack())
			{
				bCanAttack = false;
			}
		}
		if (!bCanAttack || (!bForce && !kLoopUnit.canMove()))
			continue;

		if (!bForce && !kLoopUnit.canMoveInto(*pPlot, true, bPotentialEnemy))
			continue;

		// BETTER_BTS_AI_MOD, Lead From Behind (UncutDragon), 02/21/10, jdog5000: START
		if (GC.getDefineBOOL(CvGlobals::LFB_ENABLE) &&
			GC.getDefineBOOL(CvGlobals::LFB_USECOMBATODDS) &&
			!bMaxSurvival) // advc.048
		{
			kLoopUnit.LFBgetBetterAttacker(&pBestUnit, pPlot, bPotentialEnemy, iBestOdds,
					iBestValue); // K-Mod.
		}
		else
		{
			int iOdds = kLoopUnit.AI_attackOdds(pPlot, bPotentialEnemy);
			int iValue = iOdds;
			FAssert(iValue > 0);
			if (kLoopUnit.collateralDamage() > 0 && /* advc.048: */ !bMaxSurvival)
			{
				int iPossibleTargets = std::min(
						pPlot->getNumVisibleEnemyDefenders(&kLoopUnit) - 1,
						kLoopUnit.collateralDamageMaxUnits());
				if (iPossibleTargets > 0)
				{
					iValue *= 100 + ((kLoopUnit.//collateralDamage()
							AI_collateralDmgFactor() * // advc.159
							iPossibleTargets)) / 5;
					iValue /= 100;
				}
			}
			/*  if non-human, prefer the last unit that has the best value
				(so as to avoid splitting the group) */
			if (iValue > iBestValue ||
				(!bHuman && iValue > 0 && iValue == iBestValue) ||
				/*  <advc.048> For human, use sacrifice value to break ties
					in order to match the choice made in the !bMaxSurvival branch above
					and the bSacrifice branch below. */
				(bHuman && iValue == iBestValue &&
				(pBestUnit == NULL || kLoopUnit.AI_sacrificeValue(pPlot) >
				pBestUnit->AI_sacrificeValue(pPlot)))) // </advc.048>
			{
				iBestValue = iValue;
				iBestOdds = iOdds;
				pBestUnit = &kLoopUnit;
			}
		}
		// BETTER_BTS_AI_MOD: END
	}
	iUnitOdds = iBestOdds;
	// <advc.048> Cut from CvSelectionGroup::groupAttack
	if(bSacrifice && iUnitOdds < iOddsThresh)
	{
		CvUnitAI* pBestSacrifice = AI_getBestGroupSacrifice(pPlot,
				bPotentialEnemy, bForce, /* advc.164: */ bNoBlitz);
		if(pBestSacrifice != NULL)
		{
			pBestUnit = pBestSacrifice;
			/*  I.e. caller mustn't use these odds. Don't want to compute them here
				if the caller doesn't need them. */
			iUnitOdds = -1;
		}
	} // </advc.048>
	return pBestUnit;
}


CvUnitAI* CvSelectionGroupAI::AI_getBestGroupSacrifice(const CvPlot* pPlot,
	bool bPotentialEnemy, bool bForce, bool bNoBlitz) const
{
	int iBestValue = -1; // advc.048: was 0
	CvUnitAI* pBestUnit = NULL;

	CLLNode<IDInfo> const* pUnitNode = headUnitNode();
	// <advc.048> Copied from AI_getBestGroupAttacker
	bool bHuman = (pUnitNode == NULL ? true :
			GET_PLAYER(::getUnit(pUnitNode->m_data)->getOwner()).isHuman());
	// </advc.048>
	while (pUnitNode != NULL)
	{
		CvUnitAI* pLoopUnit = ::AI_getUnit(pUnitNode->m_data);
		pUnitNode = nextUnitNode(pUnitNode);

		if (!pLoopUnit->isDead())
		{
			bool bCanAttack = false;
			if (pLoopUnit->getDomainType() == DOMAIN_AIR)
				bCanAttack = pLoopUnit->canAirAttack();
			else
			{
				bCanAttack = pLoopUnit->canAttack();
				if (bCanAttack && bNoBlitz && pLoopUnit->isBlitz() &&
					pLoopUnit->isMadeAttack())
				{
					bCanAttack = false;
				}
			}
			if (bCanAttack)
			{
				if (bForce || pLoopUnit->canMove())
				{
					if (bForce || pLoopUnit->canMoveInto(*pPlot, true))
					{
						int iValue = pLoopUnit->AI_sacrificeValue(pPlot);
						/* advc.006: > 0 not guaranteed if unit has no
						   production cost; changed to >= 0. */
						FAssert(iValue >= 0);

						/*	we want to pick the last unit of highest value,
							so pick the last unit with a good value */
						//if (iValue >= iBestValue)
						// advc.048: As in AI_getBestGroupAttacker
						if (iValue > iBestValue || (!bHuman && iValue == iBestValue))
						{
							iBestValue = iValue;
							pBestUnit = pLoopUnit;
						}
					}
				}
			}
		}
	}
	return pBestUnit;
}

/*	Returns ratio of strengths of stacks times 100
	(so 100 is an even ratio, numbers over 100 mean that
	this group is more powerful than the stack on a plot) */
int CvSelectionGroupAI::AI_compareStacks(const CvPlot* pPlot, bool bCheckCanAttack,
	bool bConstCache) const // advc.001n
{
	FAssert(pPlot != NULL);

	DomainTypes eDomainType = getDomainType();
	/*	if not aircraft, then choose based on the plot,
		not the head unit (mainly for transport carried units) */
	if (eDomainType != DOMAIN_AIR)
	{
		if (pPlot->isWater())
			eDomainType = DOMAIN_SEA;
		else eDomainType = DOMAIN_LAND;
	}

	int iCompareRatio = AI_sumStrength(pPlot, eDomainType, bCheckCanAttack);
	iCompareRatio *= 100;

	PlayerTypes eOwner = getOwner();
	if (eOwner == NO_PLAYER)
		eOwner = getHeadOwner();

	FAssert(eOwner != NO_PLAYER);

	// K-Mod. Note. This function currently does not support bPotentialEnemy == false.
	//FAssert(bPotentialEnemy);
	int iDefenderSum = pPlot->isVisible(getHeadTeam()) ?
			GET_PLAYER(eOwner).AI_localDefenceStrength(pPlot, NO_TEAM, eDomainType, 0,
			true, false, bConstCache) : // advc.001n
			GET_TEAM(getHeadTeam()).AI_strengthMemory().get(*pPlot);
	// K-Mod end
	iCompareRatio /= std::max(1, iDefenderSum);

	/*	K-Mod. If there are more defenders than we have attacks,
		but yet the ratio is still greater than 100,
		then inflate the ratio futher to account for the fact that we
		are going to do significantly more damage to them than they to us.
		The purpose of this is to give the AI extra encouragement
		to attack when its units are better than the defender's units. */
	/*if (compareRatio > 100) {
		FAssert(getHeadUnit() && getNumUnits() > 0);
		int iDefenders = pPlot->getNumVisibleEnemyDefenders(getHeadUnit());
		if (iDefenders > getNumUnits())
			compareRatio += (compareRatio - 100) * (iDefenders - getNumUnits()) / getNumUnits();
	}*/ // (currently disabled)
	// K-Mod end

	return iCompareRatio;
}

/*  K-Mod. I've removed bCheckMove, and changed bCheckCanAttack to include checks
	for moves, and for hasAlreadyAttacked / blitz */
/*  advc.159: No longer simply a sum of combat strength values; see the comment
	above CvPlayerAI::AI_localDefenceStrength. */
int CvSelectionGroupAI::AI_sumStrength(const CvPlot* pAttackedPlot,
	DomainTypes eDomainType, bool bCheckCanAttack) const
{
	FAssert(eDomainType != DOMAIN_AIR && eDomainType != DOMAIN_IMMOBILE); // advc: Air combat strength isn't counted
	// <K-Mod>
	bool const bDefenders = (pAttackedPlot ?
			pAttackedPlot->isVisibleEnemyUnit(getHeadOwner()) : false);
	bool const bCountCollateral = (pAttackedPlot && pAttackedPlot != plot()); // </K-Mod>
	int const iBaseCollateral = (bCountCollateral ?
			estimateCollateralWeight(pAttackedPlot, getTeam()) : 0);
	int	iSum = 0;
	FOR_EACH_UNITAI_IN(pUnit, *this)
	{
		if (pUnit->isDead() ||
			// advc.opt: (If we want to count air units, then this'll have to be removed.)
			!pUnit->canFight())
		{
			continue;
		}
		if (eDomainType != NO_DOMAIN && pUnit->getDomainType() != eDomainType)
			continue; // advc: Moved up
		// K-Mod. (original checks deleted.)
		if (bCheckCanAttack)
		{
			// advc.opt: currEffectiveStr is 0 for air units anyway
			/*if (pUnit->getDomainType() == DOMAIN_AIR)
			{
				if (!pUnit->canAirAttack() || !pUnit->canMove() ||
					(pAttackedPlot != NULL && bDefenders &&
					!pUnit->canMoveInto(*pAttackedPlot, true, true)))
				{
					continue; // can't attack.
				}
			}
			else*/
			if (!pUnit->canAttack() || !pUnit->canMove() ||
				(pAttackedPlot && bDefenders &&
				!pUnit->canMoveInto(*pAttackedPlot, true, true)) ||
				//(!pUnit->isBlitz() && pUnit->isMadeAttack())
				pUnit->isMadeAllAttacks()) // advc.164
			{
				continue; // can't attack.
			}
		} // K-Mod end

		// iSum += pLoopUnit->currEffectiveStr(pAttackedPlot, pLoopUnit);
		/*	K-Mod estimate the value of first strike
			and the attack power of collateral units.
			(cf with calculation in CvPlayerAI::AI_localAttackStrength) */
		/*  <advc.159> Call AI_currEffectiveStr instead of currEffectiveStr.
			Adjustments for first strikes and collateral damage moved into
			that new function. */
		int const iUnitStr = pUnit->AI_currEffectiveStr(pAttackedPlot, pUnit,
				bCountCollateral, iBaseCollateral, bCheckCanAttack);
		// </advc.159>
		iSum += iUnitStr;
		// K-Mod end
	}
	return iSum;
}

// advc.004c: Auxiliary function for AI_bestUnitForMission
namespace
{
	scaled overallUnitValue(CvUnit const& kUnit)
	{	// Crude ...
		return kUnit.getUnitInfo().getProductionCost() *
				(1 + per100(6) * kUnit.getExperience());
	}
}

/*	advc.004c: (Not const b/c it needs to return a non-const unit.
	Ideally, there would be a const version returning a const unit,
	but that would lead to a lot of duplicate code.) */
CvUnit* CvSelectionGroupAI::AI_bestUnitForMission(MissionTypes eMission,
	CvPlot const* pMissionPlot, std::vector<int> const* pUnitsToSkip)
{
	PROFILE_FUNC(); // advc (neither frequently called nor expensive)
	CvPlot const& kAt = getPlot();
	bool bEasyCityCapture = false;
	CvCity const* pTargetCity = (pMissionPlot == NULL ? NULL :
			pMissionPlot->getPlotCity());
	int iDefenders = -1;
	if (eMission == MISSION_BOMBARD)
	{
		FOR_EACH_UNIT_IN(pUnit, *this)
		{
			pTargetCity = pUnit->bombardTarget(kAt);
			if (pTargetCity != NULL)
				break;
		}
		if (pTargetCity != NULL)
		{
			pMissionPlot = pTargetCity->plot();
			iDefenders = pMissionPlot->plotCount(
					PUF_canDefendEnemy, getOwner(), false);
			if (!isHuman())
			{	// Visibility cheat, but saves time.
				bEasyCityCapture = pTargetCity->AI().AI_isEvacuating();
			}
			else
			{
				FAssertMsg(iDefenders > 0, "AI bombards undefended city");
				int iAttackers = 0;
				FOR_EACH_UNIT_IN(pUnit, kAt)
				{
					if (!pUnit->canBombard(kAt) &&
						pUnit->canMoveOrAttackInto(*pMissionPlot))
					{
						iAttackers++;
						if (iAttackers >= 2 * iDefenders)
							break;
					}
				}
				if (iAttackers >= iDefenders)
				{
					scaled rStackCmp = per100(AI_compareStacks(pMissionPlot, true, true));
					if (rStackCmp > fixp(1.5) &&
						/*	NB: If iAtt==iDef, odds needs to be very favorable
							for an immediate conquest. */
						scaled(iAttackers, std::max(iDefenders, 1)) * rStackCmp > fixp(2.5))
					{	// (Assuming that the city gets bombarded to 0)
						bEasyCityCapture = true;
					}
				}
			}
		}
	}
	CvUnit* pBestUnit = NULL;
	scaled rMaxPriority = scaled::MIN;
	FOR_EACH_UNITAI_VAR_IN(pUnit, *this)
	{
		if (!pUnit->canMove() ||
			(pUnitsToSkip != NULL &&
			std::find(pUnitsToSkip->begin(), pUnitsToSkip->end(),
			pUnit->getID()) != pUnitsToSkip->end()))
		{
			continue;
		}
		scaled rPriority;
		switch (eMission)
		{
		case MISSION_PILLAGE:
		{	// K-Mod code cut from startMission
			/*	K-Mod. Let fast units carry out the pillage action first.
				(This is based on the idea from BBAI, which had a buggy implementation.) */
			if (!pUnit->canPillage(kAt))
				continue;
			rPriority = 3;
			if (pUnit->bombardRate() > 0)
				rPriority--;
			if (pUnit->isMadeAttack())
				rPriority++;
			if (pUnit->isHurt() && !pUnit->hasMoved())
				rPriority--;
			// <advc.004c>
			rPriority *= 10000;
			rPriority -= overallUnitValue(*pUnit).round();
			// </advc.004c>
			//iPriority = (3 + iPriority) * pUnit->movesLeft() / 3;
			// advc.004c: Add 3 upfront. Don't see what good the division would do.
			rPriority *= pUnit->movesLeft();
			break;
		}
		case MISSION_BOMBARD:
		{
			if (!pUnit->canBombard(kAt))
				continue;
			/*	Some baseline to avoid precision problem when getting
				too close to 0 through divisions and multiplications */
			rPriority = 1000;
			if (bEasyCityCapture)
				rPriority *= per100(pUnit->currHitPoints());
			int const iBombard = pUnit->damageToBombardTarget(kAt);
			// bIgnoreBuilding=false b/c iBombard already reflects that
			int const iCurrDefense = pTargetCity->getDefenseModifier(false);
			int const iWaste = std::max(0, iBombard - iCurrDefense);
			if (isHuman())
			{	// Derive human intent from promotions
				scaled rDeltaBombard = (pUnit->getExtraBombardRate() - iWaste) -
						(pUnit->getExtraCollateralDamage() +
						pUnit->getExtraCityAttackPercent()) / 5;
				rPriority *= 1 + scaled::clamp(5 * rDeltaBombard, -90, 100) / 100;
			}
			rPriority *= std::max(1, 15 + iBombard - iWaste);
			scaled rOdds = per100(pUnit->AI_attackOdds(pMissionPlot, false));
			rPriority *= (1 - rOdds);
			rPriority /= 1 + per100(pUnit->AI_collateralDmgFactor());
			rPriority /= 15 + std::min(iDefenders, pUnit->collateralDamageMaxUnits());
			/*	(CollateralDamageLimit gets ignored by all AI code so far,
				so I'm not going to bother with it here either.) */
			break;
		}
		case MISSION_AIRBOMB:
		{
			if (pMissionPlot->isCity())
			{
				if (!pUnit->canAirBomb(pMissionPlot))
					continue;
				int iWasted = 0;
				int const iDamage = pUnit->airBombDefenseDamage(*pTargetCity);
				if (iDamage > 0)
				{
					iWasted = iDamage - pTargetCity->getDefenseModifier(false);
					iWasted = std::max(0, iWasted);
				}
				rPriority = std::max(0, iDamage - iWasted) * 1000 - iWasted * 100;
				rPriority -= overallUnitValue(*pUnit);
			}
			else
			{
				rPriority = pUnit->airBombCurrRate();
				rPriority *= 10000;
				rPriority -= overallUnitValue(*pUnit);
			}
			break;
		}
		case MISSION_PARADROP:
		{	/*	The group can be split between two plots here.
				Therefore don't check kAt. */
			if (!pUnit->canParadropAt(pUnit->plot(),
				pMissionPlot->getX(), pMissionPlot->getY()))
			{
				continue;
			}
			/*	I don't think it makes sense to maximize the evasion chance.
				When moving a stack of paratroopers, getting just one through
				isn't usually the goal. Want to send in the least valuable units
				first to draw out interceptors. */
			rPriority = -overallUnitValue(*pUnit);
			break;
		}
		default: FErrorMsg("Mission type not supported by bestUnitForMission");
		}
		if (rPriority > rMaxPriority)
		{
			rMaxPriority = rPriority;
			pBestUnit = pUnit;
		}
	}
	return pBestUnit;
}


void CvSelectionGroupAI::AI_queueGroupAttack(int iX, int iY)
{
	m_bGroupAttack = true;

	m_iGroupAttackX = iX;
	m_iGroupAttackY = iY;
}


bool CvSelectionGroupAI::AI_isDeclareWar(
	CvPlot const& kPlot) const // advc: param no longer optional
{
	FAssert(getHeadUnit() != NULL);

	if (isHuman())
		return false;
	// K-Mod
	if (AI_getMissionAIType() == MISSIONAI_EXPLORE)
		return false;
	// K-Mod end

	bool bLimitedWar = false;
	TeamTypes ePlotTeam = kPlot.getTeam();
	if (ePlotTeam != NO_TEAM)
	{
		WarPlanTypes eWarplan = GET_TEAM(getTeam()).AI_getWarPlan(
				GET_TEAM(ePlotTeam).getMasterTeam()); // advc.104j
		if (eWarplan == WARPLAN_LIMITED)
			bLimitedWar = true;
	}

	CvUnit const* pHeadUnit = getHeadUnit();
	if (pHeadUnit == NULL)
		return false;

	switch (pHeadUnit->AI_getUnitAIType())
	{
	case UNITAI_UNKNOWN:
	case UNITAI_ANIMAL:
	case UNITAI_SETTLE:
	case UNITAI_WORKER:
		return false;
	case UNITAI_ATTACK_CITY:
	case UNITAI_ATTACK_CITY_LEMMING:
		return true;
	case UNITAI_ATTACK:
	case UNITAI_COLLATERAL:
	case UNITAI_PILLAGE:
		return bLimitedWar;
	case UNITAI_PARADROP:
	case UNITAI_RESERVE:
	case UNITAI_COUNTER:
	case UNITAI_CITY_DEFENSE:
	case UNITAI_CITY_COUNTER:
	case UNITAI_CITY_SPECIAL:
	case UNITAI_EXPLORE:
	case UNITAI_MISSIONARY:
	case UNITAI_PERSECUTOR: // doc
	case UNITAI_PROPHET:
	case UNITAI_ARTIST:
	case UNITAI_SCIENTIST:
	case UNITAI_GENERAL:
	case UNITAI_MERCHANT:
	case UNITAI_ENGINEER:
	case UNITAI_STATESMAN: // doc
	case UNITAI_GREAT_SPY: // K-Mod
	case UNITAI_SPY:
	case UNITAI_ICBM:
	case UNITAI_WORKER_SEA:
		return false;
	case UNITAI_ATTACK_SEA:
	case UNITAI_RESERVE_SEA:
	case UNITAI_ESCORT_SEA:
		return bLimitedWar;
	case UNITAI_EXPLORE_SEA:
		return false;
	case UNITAI_ASSAULT_SEA:
		return hasCargo();
	case UNITAI_SETTLER_SEA:
	case UNITAI_MISSIONARY_SEA:
	case UNITAI_SPY_SEA:
	case UNITAI_CARRIER_SEA:
	case UNITAI_MISSILE_CARRIER_SEA:
	case UNITAI_PIRATE_SEA:
	case UNITAI_ATTACK_AIR:
	case UNITAI_DEFENSE_AIR:
	case UNITAI_CARRIER_AIR:
	case UNITAI_MISSILE_AIR:
	case UNITAI_SATELLITE: // doc
	// TODO: circumnavigate?
		return false;
	default:
		FAssert(false);
		return false;
	}
}

/*	BETTER_BTS_AI_MOD, 08/19/09 and 03/30/10, jdog5000 (General AI): START
	(advc: Moved from CvSelectionGroup) */
// Approximate how many turns this group would take to reduce pCity's defense to zero
int CvSelectionGroupAI::AI_getBombardTurns(CvCity const* pCity) const
{
	PROFILE_FUNC();
	bool const bHasBomber = (getOwner() != NO_PLAYER ?
			GET_PLAYER(getOwner()).AI_isDomainBombard(DOMAIN_AIR) : false);
	int iTotalBombardRate = (bHasBomber ? 16 : 0);
	bool bIgnoreBuildingDefense = bHasBomber;
	int iUnitBombardRate = 0;
	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		if (pUnit->bombardRate() <= 0)
			continue;
		iUnitBombardRate = pUnit->bombardRate();
		if (pUnit->ignoreBuildingDefense())
			bIgnoreBuildingDefense = true;
		else
		{
			iUnitBombardRate *= std::max(25, 100 - pCity->getBuildingBombardDefense());
			iUnitBombardRate /= 100;
		}
		iTotalBombardRate += iUnitBombardRate;
	}
	// advc (minor bugfix?): BBAI had not passed bIgnoreBuildingDefense consistently
	int const iTotalDefense = pCity->getTotalDefense(bIgnoreBuildingDefense);
	if (iTotalDefense <= 0)
		return 0;
	int const iHP = GC.getMAX_CITY_DEFENSE_DAMAGE() - pCity->getDefenseDamage();
	if (iHP <= 0)
		return 0;
	int iBombardTurns = intdiv::uceil(iHP * iTotalDefense,
			std::max(1, GC.getMAX_CITY_DEFENSE_DAMAGE() * iTotalBombardRate));
	//if (gUnitLogLevel > 2) logBBAI("      Bombard of %S will take %d turns at rate %d and current damage %d with bombard def %d", pCity->getName().GetCString(), iBombardTurns, iTotalBombardRate, pCity->getDefenseDamage(), (bIgnoreBuildingDefense ? 0 : pCity->getBuildingBombardDefense()));
	return iBombardTurns;
}

// advc: Param renamed from bIgnoreMinors b/c it also causes Barbarians to be ignored
bool CvSelectionGroupAI::AI_isHasPathToAreaEnemyCity(bool bMajorOnly,
	MovementFlags eFlags, int iMaxPathTurns) const
{
	PROFILE_FUNC();
	//int iPass = 0; // advc: unused
	for (PlayerIter<ALIVE> it; it.hasNext(); ++it)
	{
		if (bMajorOnly && !it->isMajorCiv())
			continue;
		if (GET_TEAM(getTeam()).AI_mayAttack(it->getTeam()) &&
			AI_isHasPathToAreaPlayerCity(it->getID(), eFlags, iMaxPathTurns))
		{
			return true;
		}
	}
	return false;
}


bool CvSelectionGroupAI::AI_isHasPathToAreaPlayerCity(PlayerTypes ePlayer,
	MovementFlags eFlags, int iMaxPathTurns) const
{
	PROFILE_FUNC();
	// <advc> Instead of relying on the area checks to fail when the group has no area
	if (getNumUnits() <= 0)
		return false; // </advc>
	FOR_EACH_CITY(pLoopCity, GET_PLAYER(ePlayer))
	{
		if (pLoopCity->isArea(*area()))
		{
			int iPathTurns;
			if (generatePath(getPlot(), pLoopCity->getPlot(), eFlags, true,
				&iPathTurns, iMaxPathTurns))
			{
				if (iMaxPathTurns < 0 || iPathTurns <= iMaxPathTurns)
					return true;
			}
		}
	}
	return false;
}


bool CvSelectionGroupAI::AI_isStranded() const
{
	/*PROFILE_FUNC();
	if (!m_bIsStrandedCacheValid){
		m_bIsStrandedCache = calculateIsStranded();
		m_bIsStrandedCacheValid = true;
	}
	return m_bIsStrandedCache; */
	return (AI_getMissionAIType() == MISSIONAI_STRANDED); // K-Mod
} // BETTER_BTS_AI_MOD: END


CvPlot* CvSelectionGroupAI::AI_getMissionAIPlot() const
{
	return GC.getMap().plotSoren(m_iMissionAIX, m_iMissionAIY);
}


bool CvSelectionGroupAI::AI_isForceSeparate() const
{
	return m_bForceSeparate;
}


void CvSelectionGroupAI::AI_setMissionAI(MissionAITypes eNewMissionAI,
	CvPlot const* pNewPlot, CvUnit const* pNewUnit)
{
	//PROFILE_FUNC();

	m_eMissionAIType = eNewMissionAI;

	if (pNewPlot != NULL)
	{
		m_iMissionAIX = pNewPlot->getX();
		m_iMissionAIY = pNewPlot->getY();
	}
	else
	{
		m_iMissionAIX = INVALID_PLOT_COORD;
		m_iMissionAIY = INVALID_PLOT_COORD;
	}

	if (pNewUnit != NULL)
		m_missionAIUnit = pNewUnit->getIDInfo();
	else m_missionAIUnit.reset();
}


CvUnitAI* CvSelectionGroupAI::AI_getMissionAIUnit() const
{
	/*	advc (note): Could possibly return an incorrect unit if the correct
		one has been killed and the same FFreeList ID has gotten assigned to
		a new unit. I.e. this data member is not getting reset by CvUnit::kill. */
	return ::AI_getUnit(m_missionAIUnit);
}


bool CvSelectionGroupAI::AI_isFull()
{
	if(getNumUnits() <= 0)
		return false;

	UnitAITypes eUnitAI = getHeadUnitAIType();
	// do two passes, the first pass, we ignore units with speical cargo.
	int iSpecialCargoCount = 0;
	int iCargoCount = 0;

	// first pass, count but ignore special cargo units.
	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		if (pUnit->AI_getUnitAIType() != eUnitAI)
			continue;
		if (pUnit->cargoSpace() > 0)
			iCargoCount++;
		if (pUnit->specialCargo() != NO_SPECIALUNIT)
			iSpecialCargoCount++;
		else if (!pUnit->isFull())
			return false;
	}
	/*	if every unit in the group has special cargo, then check those,
		otherwise, consider ourselves full. */
	if (iSpecialCargoCount >= iCargoCount)
	{
		FOR_EACH_UNIT_IN(pUnit, *this)
		{
			if (pUnit->AI_getUnitAIType() != eUnitAI)
				continue;
			if (!pUnit->isFull())
				return false;
		}
	}
	return true;
}


CvUnitAI* CvSelectionGroupAI::AI_ejectBestDefender(CvPlot* pDefendPlot)
{
	CvUnitAI* pBestUnit = NULL;
	int iBestUnitValue = 0;
	FOR_EACH_UNITAI_VAR_IN(pUnit, *this)
	{
		//if (pUnit->noDefensiveBonus()) continue;
		// commented out by K-Mod. The noDefBonus thing is already taken into account.
		/*  advc.159: Call AI_currEffectiveStr instead of currEffectiveStr
			And reduce the precision multiplier from 100 to 10. */
		int iValue = pUnit->AI_currEffectiveStr(pDefendPlot) * 10;
		//if (pDefendPlot->isCity(true, getTeam())))
		if (GET_TEAM(getTeam()).isCityDefense(*pDefendPlot)) // advc
		{
			iValue *= 100 + pUnit->cityDefenseModifier();
			iValue /= 100;
		}

		iValue *= 100;
		//iValue /= (100 + pUnit->cityAttackModifier() + pUnit->getExtraCityAttackPercent());
		// advc.mnai: (Note that cityAttackModifier includes ExtraCityAttackPercent)
		iValue /= 100 + std::max(-50, 2 * pUnit->cityAttackModifier());

		iValue /= 2 + (pUnit->getLevel() *
				// advc.mnai:
				(pUnit->AI_getUnitAIType() == UNITAI_ATTACK_CITY ? 2 : 1));
		if (iValue > iBestUnitValue)
		{
			iBestUnitValue = iValue;
			pBestUnit = pUnit;
		}
	}
	if (pBestUnit != NULL && getNumUnits() > 1)
		pBestUnit->joinGroup(NULL);
	return pBestUnit;
}

// <advc.003u> Based on CvSelectionGroup::getHeadUnit
CvUnitAI const* CvSelectionGroupAI::AI_getHeadUnit() const
{
	CLLNode<IDInfo> const* pNode = headUnitNode();
	return (pNode != NULL ? ::AI_getUnit(pNode->m_data) : NULL);
}


CvUnitAI* CvSelectionGroupAI::AI_getHeadUnit()
{
	CLLNode<IDInfo>* pNode = headUnitNode();
	return (pNode != NULL ? ::AI_getUnit(pNode->m_data) : NULL);
} // </advc.003u>


void CvSelectionGroupAI::AI_makeForceSeparate()
{
	m_bForceSeparate = true;
}


void CvSelectionGroupAI::read(FDataStreamBase* pStream)
{
	CvSelectionGroup::read(pStream);

	uint uiFlag=0;
	pStream->Read(&uiFlag);

	pStream->Read(&m_iMissionAIX);
	pStream->Read(&m_iMissionAIY);

	pStream->Read(&m_bForceSeparate);

	pStream->Read((int*)&m_eMissionAIType);

	pStream->Read((int*)&m_missionAIUnit.eOwner);
	m_missionAIUnit.validateOwner(); // advc.opt
	pStream->Read(&m_missionAIUnit.iID);

	pStream->Read(&m_bGroupAttack);
	pStream->Read(&m_iGroupAttackX);
	pStream->Read(&m_iGroupAttackY);
}


void CvSelectionGroupAI::write(FDataStreamBase* pStream)
{
	CvSelectionGroup::write(pStream);

	uint uiFlag=0;
	pStream->Write(uiFlag);
	REPRO_TEST_BEGIN_WRITE(CvString::format("SelGroupAI(%d,%d,%d)", getID(), getX(), getY()));
	pStream->Write(m_iMissionAIX);
	pStream->Write(m_iMissionAIY);

	pStream->Write(m_bForceSeparate);

	pStream->Write(m_eMissionAIType);

	pStream->Write(m_missionAIUnit.eOwner);
	pStream->Write(m_missionAIUnit.iID);

	pStream->Write(m_bGroupAttack);
	pStream->Write(m_iGroupAttackX);
	pStream->Write(m_iGroupAttackY);
	REPRO_TEST_END_WRITE();
}
