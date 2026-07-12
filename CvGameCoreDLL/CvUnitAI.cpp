#include "CvGameCoreDLL.h"
#include "CvUnitAI.h"
#include "CombatOdds.h"
#include "CvSelectionGroupAI.h"
#include "GroupPathFinder.h"
#include "FAStarNode.h"
#include "CoreAI.h"
#include "CvCityAI.h"
#include "CvPlotGroup.h" // (just for AI_betterPlotBuild
#include "PlotRange.h"
#include "CvArea.h"
#include "BarbarianWeightMap.h" // advc.304
#include "CvInfo_Terrain.h"
#include "CvInfo_GameOption.h"
#include "CvInfo_Building.h" // advc.003x: Only needed for the special buildings that GP can construct
#include "BBAILog.h" // BETTER_BTS_AI_MOD, AI logging, 10/02/09, jdog5000

//#define FOUND_RANGE (7) // advc: unused

// <advc.003u>
CvUnitAI::CvUnitAI() // Body cut from AI_reset
{
	m_eUnitAIType = NO_UNITAI;
	m_iBirthmark = 0;
	m_iAutomatedAbortTurn = -1;
	m_iSearchRangeRandPercent = 100; // advc.128
}


CvUnitAI::~CvUnitAI()
{
	//AI_uninit(); // Delete member pointers right here (but there are none)
}

// Instead of having CvUnit::init call CvUnitAI::AI_init. finalizeInit split off.
void CvUnitAI::init(int iID, UnitTypes eUnit, UnitAITypes eUnitAI,
	PlayerTypes eOwner, int iX, int iY, DirectionTypes eFacingDirection)
{
	CvUnit::init(iID, eUnit, eOwner, iX, iY, eFacingDirection);
	m_eUnitAIType = eUnitAI;
	FAssert(AI_getUnitAIType() != NO_UNITAI);
	AI_setBirthmark(SyncRandNum(10000));
	finalizeInit();
}


void CvUnitAI::finalizeInit() // Counter updates moved out of the init function above
{
	getArea().changeNumAIUnits(getOwner(), AI_getUnitAIType(), 1);
	GET_PLAYER(getOwner()).AI_changeNumAIUnits(AI_getUnitAIType(), 1);
	CvUnit::finalizeInit(); // Important to let CvUnit have the last word
}

//void CvUnitAI::uninit() { CvUnit::uninit(); }
// </advc.003u>

// AI_update returns true when we should abort the loop and wait until next slice
bool CvUnitAI::AI_update()
{
	PROFILE_FUNC();

	FAssert(canMove());
	FAssert(isGroupHead()); // XXX is this a good idea???

	if (GC.getPythonCaller()->AI_update(*this))
		return false;
	// <advc.128>
	m_iSearchRangeRandPercent = syncRand().get(101, "SearchRangeRand",
			getX() * 1000 + getY(), getID()); // </advc.128>
	if (getDomainType() == DOMAIN_LAND)
	{
		if (getPlot().isWater() && !canMoveAllTerrain())
		{
			getGroup()->pushMission(MISSION_SKIP);
			return false;
		}
		else
		{
			CvUnit* pTransportUnit = getTransportUnit();
			if (pTransportUnit != NULL)
			{
				CvSelectionGroupAI const* pTransportGroup =
						pTransportUnit->AI().AI_getGroup();
				//if (pTransportGroup->hasMoved() || (pTransportGroup->headMissionQueueNode() != NULL))
				/*	K-Mod. Note: transport units with cargo always have their turn
					before the cargo does - so... I've changed the skip condition. */
				if (pTransportGroup->headMissionQueueNode() != NULL ||
					(pTransportGroup->AI_getMissionAIPlot() &&
					!atPlot(pTransportGroup->AI_getMissionAIPlot())))
				// K-Mod end
				{
					getGroup()->pushMission(MISSION_SKIP);
					return false;
				}
			}
		}
	}

	if (AI_afterAttack())
		return false;

	if (getGroup()->isAutomated() &&
		isHuman()) // K-Mod: for AI Auto Play
	{
		switch (getGroup()->getAutomateType())
		{
		case AUTOMATE_BUILD:
			if (AI_getUnitAIType() == UNITAI_WORKER)
				AI_workerMove();
			else if (AI_getUnitAIType() == UNITAI_WORKER_SEA)
				AI_workerSeaMove();
			else FAssert(false);
			break;
		case AUTOMATE_NETWORK:
			AI_networkAutomated();
			// XXX else wake up???
			break;
		case AUTOMATE_CITY:
			AI_cityAutomated();
			// XXX else wake up???
			break;
		case AUTOMATE_EXPLORE:
			switch (getDomainType())
			{
			case DOMAIN_SEA:
				AI_exploreSeaMove();
				break;
			case DOMAIN_AIR:
			{
				// If we are cargo, hold if the carrier is not done moving yet.
				CvUnit* pTransportUnit = getTransportUnit();
				if (pTransportUnit != NULL)
				{
					if (pTransportUnit->isAutomated() && pTransportUnit->canMove() &&
						pTransportUnit->getGroup()->getActivityType() != ACTIVITY_HOLD)
					{
						getGroup()->pushMission(MISSION_SKIP);
						break;
					}
				}
				/*  BETTER_BTS_AI_MOD, Player Interface, 01/12/09, jdog5000:
					Have air units explore like AI units do */
				AI_exploreAirMove();
				break;
			}
			case DOMAIN_LAND:
				AI_exploreMove();
				break;
			default:
				FAssert(false);
				break;
			}
			/*	If we have air cargo (we are a carrier), and we done moving,
				explore with the aircraft as well */
			if (hasCargo() && domainCargo() == DOMAIN_AIR &&
				(!canMove() || getGroup()->getActivityType() == ACTIVITY_HOLD))
			{
				std::vector<CvUnit*> aCargoUnits;
				getCargoUnits(aCargoUnits);
				for (size_t i = 0; i < aCargoUnits.size() && isAutomated(); i++)
				{
					CvUnit* pCargoUnit = aCargoUnits[i];
					if (pCargoUnit->getDomainType() == DOMAIN_AIR &&
						pCargoUnit->canMove())
					{
						pCargoUnit->getGroup()->setAutomateType(AUTOMATE_EXPLORE);
						pCargoUnit->getGroup()->setActivityType(ACTIVITY_AWAKE);
					}
				}
			}
			break;
		case AUTOMATE_RELIGION:
			if (AI_getUnitAIType() == UNITAI_MISSIONARY)
				AI_missionaryMove();
			break;
		default:
			FAssert(false);
			break;
		}
		// if no longer automated, then we want to bail
		return !getGroup()->isAutomated();
	}
	// <advc.139>
	UnitAITypes const eUnitAI = AI_getUnitAIType();
	if (getPlot().isCity() && getPlot().getTeam() == getTeam() && !isBarbarian())
	{
		bool bEvacAI = false;
		switch(eUnitAI)
		{
		case UNITAI_ATTACK:
		case UNITAI_ATTACK_CITY:
		case UNITAI_COLLATERAL:
		case UNITAI_PILLAGE:
		case UNITAI_RESERVE:
		case UNITAI_COUNTER:
		case UNITAI_CITY_DEFENSE:
		case UNITAI_CITY_COUNTER:
		case UNITAI_CITY_SPECIAL:
			bEvacAI = true;
			break;
		/*  The other AI types are obscure or already have routines for
			escaping untenable cities. */
		}
		if (bEvacAI)
		{
			if (AI_evacuateCity())
				return false;
		}
	} // </advc.139>

	switch (eUnitAI)
	{
	case UNITAI_UNKNOWN:
		getGroup()->pushMission(MISSION_SKIP);
		break;
	case UNITAI_ANIMAL:
		AI_animalMove();
		break;
	case UNITAI_SETTLE:
		AI_settleMove();
		break;
	case UNITAI_WORKER:
		AI_workerMove();
		break;
	case UNITAI_ATTACK:
		if (isBarbarian() || isNative()) // rfc
			AI_barbAttackMove();
		else AI_attackMove();
		break;
	case UNITAI_ATTACK_CITY:
		AI_attackCityMove();
		break;
	case UNITAI_COLLATERAL:
		AI_collateralMove();
		break;
	case UNITAI_PILLAGE:
		AI_pillageMove();
		break;
	case UNITAI_RESERVE:
		AI_reserveMove();
		break;
	case UNITAI_COUNTER:
		AI_counterMove();
		break;
	case UNITAI_PARADROP:
		AI_paratrooperMove();
		break;
	case UNITAI_CITY_DEFENSE:
		AI_cityDefenseMove();
		break;
	case UNITAI_CITY_COUNTER:
	case UNITAI_CITY_SPECIAL:
		AI_cityDefenseExtraMove();
		break;
	case UNITAI_EXPLORE:
		AI_exploreMove();
		break;
	case UNITAI_MISSIONARY:
		AI_missionaryMove();
		break;
	case UNITAI_GENERAL:
		AI_generalMove();
		break;
	case UNITAI_PROPHET:
	case UNITAI_ARTIST:
	case UNITAI_SCIENTIST:
	case UNITAI_MERCHANT:
	case UNITAI_ENGINEER:
	case UNITAI_STATESMAN: // doc
	// K-Mod
	case UNITAI_GREAT_SPY:
		//AI_greatSpyMove();
		AI_greatPersonMove(); // advc
		break; // K-Mod end
	case UNITAI_SPY:
		AI_spyMove();
		break;
	case UNITAI_ICBM:
		AI_ICBMMove();
		break;
	case UNITAI_WORKER_SEA:
		AI_workerSeaMove();
		break;
	case UNITAI_ATTACK_SEA:
		if (isBarbarian())
			AI_barbAttackSeaMove();
		else AI_attackSeaMove();
		break;
	case UNITAI_RESERVE_SEA:
		AI_reserveSeaMove();
		break;
	case UNITAI_ESCORT_SEA:
		AI_escortSeaMove();
		break;
	case UNITAI_EXPLORE_SEA:
		AI_exploreSeaMove();
		break;
	case UNITAI_ASSAULT_SEA:
		AI_assaultSeaMove();
		break;
	case UNITAI_SETTLER_SEA:
		AI_settlerSeaMove();
		break;
	case UNITAI_MISSIONARY_SEA:
		AI_missionarySeaMove();
		break;
	case UNITAI_SPY_SEA:
		AI_spySeaMove();
		break;
	case UNITAI_CARRIER_SEA:
		AI_carrierSeaMove();
		break;
	case UNITAI_MISSILE_CARRIER_SEA:
		AI_missileCarrierSeaMove();
		break;
	case UNITAI_PIRATE_SEA:
		AI_pirateSeaMove();
		break;
	case UNITAI_ATTACK_AIR:
		AI_attackAirMove();
		break;
	case UNITAI_DEFENSE_AIR:
		AI_defenseAirMove();
		break;
	case UNITAI_CARRIER_AIR:
		AI_carrierAirMove();
		break;
	case UNITAI_MISSILE_AIR:
		AI_missileAirMove();
		break;
	case UNITAI_ATTACK_CITY_LEMMING:
		AI_attackCityLemmingMove();
		break;
	case UNITAI_PERSECUTOR: // doc
		AI_persecutorMove();
		break;
	case UNITAI_SATELLITE: // doc
		AI_satelliteMove();
		break;
	default: FErrorMsg("Unknown Unit AI type");
	}

	return false;
}

// Returns true if took an action or should wait to move later...
/*	K-Mod. I've basically rewritten this function.
	bFirst should be "true" if this is the first unit in the group to use this follow function.
	the point is that there are some calculations and checks in here
	which only depend on the group, not the unit,
	so for efficiency we should only check them once. */
bool CvUnitAI::AI_follow(bool bFirst)
{
	FAssert(getDomainType() != DOMAIN_AIR);

	if (AI_followBombard())
		return true;

	if (bFirst && getGroup()->getHeadUnitAIType() == UNITAI_ATTACK_CITY)
	{
		/*	note: AI_stackAttackCity will check which of our units can attack
			when comparing stacks; and it will issue the attack order using
			MOVE_DIRECT ATTACK, which will execute without waiting for
			the entire group to have movement points. */
		if (AI_stackAttackCity()) // automatic threshold
			return true;
	}

	/*	I've changed attack-follow code so that it will
		only attack with a single unit, not the whole group. */
	if (bFirst && AI_cityAttack(1, 65, NO_MOVEMENT_FLAGS, true))
		return true;
	if (bFirst)
	{
		bool bMoveGroup = false; // to large groups to leave some units behind.
		if (getGroup()->getNumUnits() >= 16)
		{
			int iCanMove = 0;
			FOR_EACH_UNIT_IN(pLoopUnit, *getGroup())
			{
				if (pLoopUnit->canMove())
					iCanMove++;
			}
			// if 4/5 of our group can still move.
			bMoveGroup = (5 * iCanMove >= 4 * getGroup()->getNumUnits() || iCanMove >= 20);
		}
		if (AI_anyAttack(1, isEnemy(getPlot()) ? 65 : 70, NO_MOVEMENT_FLAGS,
			bMoveGroup ? 0 : 2, true, true))
		{
			return true;
		}
	}

	if (isEnemy(getPlot()))
	{
		if (canPillage(getPlot()))
		{
			getGroup()->pushMission(MISSION_PILLAGE);
			return true;
		}
	}

	/*	K-Mod. AI_foundRange is bad AI. It doesn't always found when we want to,
		and it has the potential to found when we don't! So I've replaced it. */
	if (AI_foundFollow())
		return true;

	return false;
}

// K-Mod. This function has been completely rewritten to improve efficiency and intelligence.
void CvUnitAI::AI_upgrade()
{
	PROFILE_FUNC();

	FAssert(!isHuman());
	FAssert(AI_getUnitAIType() != NO_UNITAI);

	if (!isReadyForUpgrade())
		return;

	const CvPlayerAI& kOwner = GET_PLAYER(getOwner());
	UnitAITypes eUnitAI = AI_getUnitAIType();
	CvArea* pArea = area();

	int iBestValue = kOwner.AI_unitValue(getUnitType(), eUnitAI, pArea) * 100;
	UnitTypes eBestUnit = NO_UNIT;

	/*	Note: the original code did two passes, presumably for speed reasons.
		In the first pass, they checked only units which were flagged with the right unitAI.
		Then, only if no such units were found, they checked all other units.

		I'm just jumping straight to the second (slower) pass, because most of the time
		no upgrades are available at all and so both passes would be used anyway.

		I've reversed the order of iteration because
		the stronger units are typically later in the list. */
	bool bFirst = true; // advc.007
	CvCivilization const& kCiv = kOwner.getCivilization(); // advc.003w
	for (int i = kCiv.getNumUnits() - 1; i >= 0; i--)
	{
		UnitTypes eLoopUnit = kCiv.unitAt(i);
		int iValue = kOwner.AI_unitValue(eLoopUnit, eUnitAI, pArea);
		/*	use a random factor. less than 100, so that
			the upgrade must be better than the current unit. */
		iValue *= 80 + syncRand().get(21,
				// <advc.007> Don't pollute the MPLog
				bFirst ? "AI Upgrade" : NULL);
		bFirst = false; // </advc.007>
		// (believe it or not, AI_unitValue is faster than canUpgrade.)
		if (iValue > iBestValue && canUpgrade(eLoopUnit))
		{
			iBestValue = iValue;
			eBestUnit = eLoopUnit;
		}
	}

	if (eBestUnit != NO_UNIT)
	{
		if (gUnitLogLevel > 0) logBBAI("    %S (unit %d - %S) upgrading to %S (value: %d)", getName().GetCString(), getID(), GC.getUnitAIInfo(AI_getUnitAIType()).getDescription(), GC.getInfo(eBestUnit).getDescription(), iBestValue); // advc.mnai
		/*upgrade(eBestUnit);
		doDelayedDeath(); */ // BtS
		// K-Mod. Ungroup the unit, so that we don't cause the whole group to miss their turn.
		CvUnit* pUpgradeUnit = upgrade(eBestUnit);
		doDelayedDeath();

		if (pUpgradeUnit != this)
		{
			CvSelectionGroup* pGroup = pUpgradeUnit->getGroup();
			if (pGroup->getHeadUnit() != pUpgradeUnit)
			{
				pUpgradeUnit->joinGroup(NULL);
				/*	indicate that the unit intends to rejoin the old group
					(although it might not actually do so...) */
				pUpgradeUnit->getGroup()->AI().AI_setMissionAI(MISSIONAI_GROUP, NULL,
						pGroup->getHeadUnit());
			}
		}
	}
}


void CvUnitAI::AI_promote()
{
	PROFILE_FUNC();

	/*	K-Mod. A quick check to see if we can rule out all promotions in one hit,
		before we go through them one by one. */
	if (!isPromotionReady())
		return; // can't get any normal promotions. (see CvUnit::canPromote)
	// K-Mod end
	int iBestValue = 0;
	PromotionTypes eBestPromotion = NO_PROMOTION;
	FOR_EACH_ENUM(Promotion)
	{
		if (canPromote(eLoopPromotion))
		{
			int iValue = AI_promotionValue(eLoopPromotion);
			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				eBestPromotion = eLoopPromotion;
			}
		}
	}
	if (eBestPromotion != NO_PROMOTION)
	{
		promote(eBestPromotion);
		AI_promote();
	}
}

// <advc.003u>, advc.003s
CvSelectionGroupAI const* CvUnitAI::AI_getGroup() const
{
	return GET_PLAYER(getOwner()).AI_getSelectionGroup(getGroupID());
}


CvSelectionGroupAI* CvUnitAI::AI_getGroup()
{
	return GET_PLAYER(getOwner()).AI_getSelectionGroup(getGroupID());
} // </advc.003u>


int CvUnitAI::AI_groupFirstVal() /* advc: */ const
{
	switch (AI_getUnitAIType())
	{
	case UNITAI_UNKNOWN:
	case UNITAI_ANIMAL:
		FAssert(false);
		break;

	case UNITAI_SETTLE:
		return 21;

	case UNITAI_WORKER:
		return 20;

	case UNITAI_ATTACK:
		if (collateralDamage() > 0)
			return 15; // was 17
		if (withdrawalProbability() > 0)
			return 14; // was 15
		return 13;

	case UNITAI_ATTACK_CITY:
		if (bombardRate() > 0)
			return 19;
		if (collateralDamage() > 0)
			return 18;
		if (withdrawalProbability() > 0)
			return 17; // was 16
		return 16; // was 14

	case UNITAI_COLLATERAL:
		return 7;

	case UNITAI_PILLAGE:
		return 12;

	case UNITAI_RESERVE:
		return 6;

	case UNITAI_COUNTER:
		return 5;

	case UNITAI_CITY_DEFENSE:
		return 3;

	case UNITAI_CITY_COUNTER:
		return 2;

	case UNITAI_CITY_SPECIAL:
		return 1;

	case UNITAI_PARADROP:
		return 4;

	case UNITAI_EXPLORE:
		return 8;

	case UNITAI_MISSIONARY:
		return 10;

	case UNITAI_PROPHET:
	case UNITAI_ARTIST:
	case UNITAI_SCIENTIST:
	case UNITAI_GENERAL:
	case UNITAI_MERCHANT:
	case UNITAI_ENGINEER:
	case UNITAI_GREAT_SPY: // K-Mod
		return 11;

	case UNITAI_SPY:
		return 9;

	case UNITAI_ICBM:
		break;

	case UNITAI_WORKER_SEA:
		return 8;

	case UNITAI_ATTACK_SEA:
		return 3;

	case UNITAI_RESERVE_SEA:
		return 2;

	case UNITAI_ESCORT_SEA:
		return 1;

	case UNITAI_EXPLORE_SEA:
		return 5;

	case UNITAI_ASSAULT_SEA:
		return 11;

	case UNITAI_SETTLER_SEA:
		return 9;

	case UNITAI_MISSIONARY_SEA:
		return 9;

	case UNITAI_SPY_SEA:
		return 10;

	case UNITAI_CARRIER_SEA:
		return 7;

	case UNITAI_MISSILE_CARRIER_SEA:
		return 6;

	case UNITAI_PIRATE_SEA:
		return 4;

	case UNITAI_ATTACK_AIR:
	case UNITAI_DEFENSE_AIR:
	case UNITAI_CARRIER_AIR:
	case UNITAI_MISSILE_AIR:
		return 0;

	case UNITAI_ATTACK_CITY_LEMMING:
		return 1;

	default:
		FAssert(false);
	}

	return 0;
}


int CvUnitAI::AI_groupSecondVal() /* advc: */ const
{
	return (getDomainType() == DOMAIN_AIR ? airBaseCombatStr() : baseCombatStr());
}

/*	Returns attack odds out of 100 (the higher, the better...)
	Withdrawal odds included in returned value
	advc (note): Mostly supplanted by LFBgetBetterAttacker and AI_getWeightedOdds -
	though the latter calls AI_attackOdds indirectly. I think only AI_paradrop
	still uses CvUnitAI::AI_attackOdds directly. */
int CvUnitAI::AI_attackOdds(const CvPlot* pPlot, bool bPotentialEnemy) const
{
	PROFILE_FUNC();

	CvPlot::DefenderFilters defFilters(getOwner(), this,
			!bPotentialEnemy, bPotentialEnemy,
			true, // advc.028: bTestVisible
			false); // advc.089: bTestCanAttack - attack isn't necessarily imminent here
	CvUnit* pDefender = pPlot->getBestDefender(NO_PLAYER, defFilters);
	if (pDefender == NULL)
		return 100;

	// BETTER_BTS_AI_MOD, Efficiency, Lead From Behind (UncutDragon), jdog5000: START
	if (GC.getDefineBOOL(CvGlobals::LFB_ENABLE) &&
		GC.getDefineBOOL(CvGlobals::LFB_USECOMBATODDS))
	{
		// Combat odds are out of 1000 - we need odds out of 100
		int iOdds = (calculateCombatOdds(*this, *pDefender) + 5) / 10;
		iOdds += GET_PLAYER(getOwner()).AI_getAttackOddsChange();
		return std::max(1, std::min(iOdds, 99));
	}

	int iOurStrength = (getDomainType() == DOMAIN_AIR ?
			airCurrCombatStr(NULL) : currCombatStr());
	int iOurFirepower = (getDomainType() == DOMAIN_AIR ?
			iOurStrength : currFirepower());

	if (iOurStrength == 0)
		return 1;

	int iTheirStrength = pDefender->currCombatStr(pPlot, this);
	int iTheirFirepower = pDefender->currFirepower(pPlot, this);


	FAssert((iOurStrength + iTheirStrength) > 0);
	FAssert((iOurFirepower + iTheirFirepower) > 0);

	int iBaseOdds = (100 * iOurStrength) / (iOurStrength + iTheirStrength);
	if (iBaseOdds == 0)
		return 1;

	int iStrengthFactor = (iOurFirepower + iTheirFirepower + 1) / 2;
	int iDamageToUs = std::max(1, (GC.getCOMBAT_DAMAGE() *
			(iTheirFirepower + iStrengthFactor)) /
			(iOurFirepower + iStrengthFactor));
	int iDamageToThem = std::max(1, (GC.getCOMBAT_DAMAGE() *
			(iOurFirepower + iStrengthFactor)) /
			(iTheirFirepower + iStrengthFactor));
	int iHitLimitThem = pDefender->maxHitPoints() - combatLimitAgainst(pDefender); // doc
	int iNeededRoundsUs = intdiv::uceil(
			std::max(0, pDefender->currHitPoints() - iHitLimitThem), iDamageToThem);
	int iNeededRoundsThem = intdiv::uceil(
			std::max(0, currHitPoints()), iDamageToUs);

	if (getDomainType() != DOMAIN_AIR)
	{
		/*  BETTER_BTS_AI_MOD, Unit AI, 10/30/09, Mongoose & jdog5000: START
			(from Mongoose SDK) */
		if (!pDefender->immuneToFirstStrikes())
		{
			iNeededRoundsUs -= (iBaseOdds * firstStrikes() +
					(iBaseOdds * chanceFirstStrikes()) / 2) / 100;
		}
		if (!immuneToFirstStrikes())
		{
			iNeededRoundsThem -= ((100 - iBaseOdds) * pDefender->firstStrikes() +
					((100 - iBaseOdds) * pDefender->chanceFirstStrikes()) / 2) / 100;
		}
		iNeededRoundsUs   = std::max(1, iNeededRoundsUs);
		iNeededRoundsThem = std::max(1, iNeededRoundsThem);
		// BETTER_BTS_AI_MOD: END
	}

	int iRoundsDiff = iNeededRoundsUs - iNeededRoundsThem;
	if (iRoundsDiff > 0)
		iTheirStrength *= (1 + iRoundsDiff);
	else iOurStrength *= (1 - iRoundsDiff);

	int iOdds = (iOurStrength * 100) / (iOurStrength + iTheirStrength);
	iOdds += ((100 - iOdds) * withdrawalProbability()) / 100;
	iOdds += GET_PLAYER(getOwner()).AI_getAttackOddsChange();
	/*  BETTER_BTS_AI_MOD, Unit AI, 10/30/09, Mongoose & jdog5000
		(from Mongoose SDK): */
	return range(iOdds, 1, 99);
}

// Returns true if the unit found a build for this city...
bool CvUnitAI::AI_bestCityBuild(CvCityAI const& kCity,
	CvPlot** ppBestPlot, BuildTypes* peBestBuild,
	CvPlot* pIgnorePlot, CvUnit* pUnit) const
{
	PROFILE_FUNC();

	int iBestValue = 0;
	BuildTypes eBestBuild = NO_BUILD;
	CvPlot* pBestPlot = NULL;

	/*	K-Mod. hack: For the AI, I want to use the standard pathfinder, CvUnit::generatePath.
		but this function is also used to give action recommendations for the player
		- and for that I do not want to disrupt the standard pathfinder.
		(because I'm paranoid about OOS bugs.) */
	//GroupPathFinder altFinder;
	GroupPathFinder& pathFinder = (getGroup()->isAIControlled() ?
			CvSelectionGroup::pathFinder() :
			CvSelectionGroup::getClearPathFinder()); // advc.opt
	if (getGroup()->isAIControlled())
	{
		// standard settings. cf. CvUnit::generatePath
		pathFinder.setGroup(*getGroup(), NO_MOVEMENT_FLAGS);
	}
	else
	{
		// like I said - this is only for action recommendations. It can be rough.
		pathFinder.setGroup(*getGroup(), NO_MOVEMENT_FLAGS, 5, GC.getMOVE_DENOMINATOR());
	} // K-Mod end

	for (int iPass = 0; iPass < 2; iPass++)
	{
		// K-Mod: only workable tiles
		for (WorkablePlotIter it(kCity); it.hasNext(); ++it)
		{
			CvPlot& kPlot = *it;
			CityPlotTypes ePlot = it.currID();
			if (&kPlot == pIgnorePlot || /*!AI_plotValid(kPlot)*/kPlot.isWater()) // advc.opt
				continue;
			if (GET_PLAYER(getOwner()).isAutomationSafe(kPlot))
				continue;
			int iValue = kCity.AI_getBestBuildValue(ePlot);
			if (iValue <= iBestValue)
				continue;
			BuildTypes eBuild = kCity.AI_getBestBuild(ePlot);
			if (eBuild == NO_BUILD || /* K-Mod: */ !canBuild(kPlot, eBuild))
				continue;
			if (iPass == 0)
			{
				iBestValue = iValue;
				pBestPlot = &kPlot;
				eBestBuild = eBuild;
				continue;
			}
			//if (canBuild(pLoopPlot, eBuild))
			if (kPlot.isVisibleEnemyUnit(this))
				continue;
			/*int iPathTurns;
			if (generatePath(pLoopPlot, 0, true, &iPathTurns)) {
				// XXX take advantage of range (warning... this could lead to some units doing nothing...)
				int iMaxWorkers = 1;
				if (getPathLastNode()->m_iData1 == 0)
					iPathTurns++;
				else if (iPathTurns <= 1)
					iMaxWorkers = AI_calculatePlotWorkersNeeded(pLoopPlot, eBuild);
				if (pUnit != NULL) {
					if (pUnit->getPlot().isCity() && iPathTurns == 1 && getPathLastNode()->m_iData1 > 0)
					iMaxWorkers += 10;
				} }*/ // BtS
			// K-Mod. basically the same thing, but using pathFinder.
			if (!pathFinder.generatePath(kPlot))
				continue;
			int iPathTurns = pathFinder.getPathTurns() + (pathFinder.getFinalMoves() == 0 ? 1 : 0);
			int iMaxWorkers = (iPathTurns > 1 ? 1 : AI_calculatePlotWorkersNeeded(kPlot, eBuild));
			if (pUnit != NULL && pUnit->getPlot().isCity() && iPathTurns == 1)
				iMaxWorkers += 10;
			// K-Mod end
			if (GET_PLAYER(getOwner()).AI_plotTargetMissionAIs(kPlot, MISSIONAI_BUILD, getGroup(),
				/* <advc.opt> */ 0, iMaxWorkers /* </advc.opt> */) < iMaxWorkers)
			{
				//XXX this could be improved greatly by
				//looking at the real build time and other factors
				//when deciding whether to stack.
				iValue /= iPathTurns;

				iBestValue = iValue;
				pBestPlot = &kPlot;
				eBestBuild = eBuild;
			}
		}
		if (iPass > 0 || eBestBuild == NO_BUILD)
			continue;

		FAssert(pBestPlot != NULL);
		/*int iPathTurns;
		if (generatePath(pBestPlot, 0, true, &iPathTurns) && canBuild(pBestPlot, eBestBuild) &&
				!pBestPlot->isVisibleEnemyUnit(this)) {
			int iMaxWorkers = 1;
			if (pUnit != NULL) {
				if (pUnit->getPlot().isCity())
					iMaxWorkers += 10;
			}
			if (getPathLastNode()->m_iData1 == 0)
				iPathTurns++;
			else if (iPathTurns <= 1)
				iMaxWorkers = AI_calculatePlotWorkersNeeded(pBestPlot, eBestBuild);
		} */ // BtS
		// K-Mod. basically the same thing, but using pathFinder.
		if (pathFinder.generatePath(*pBestPlot))
		{
			int iPathTurns = pathFinder.getPathTurns() +
					(pathFinder.getFinalMoves() == 0 ? 1 : 0);
			int iMaxWorkers = iPathTurns > 1 ? 1 :
					AI_calculatePlotWorkersNeeded(*pBestPlot, eBestBuild);
			if (pUnit != NULL && pUnit->getPlot().isCity() && iPathTurns == 1)
				iMaxWorkers += 10;
		// K-Mod end
			int iWorkerCount = GET_PLAYER(getOwner()).AI_plotTargetMissionAIs(
					*pBestPlot, MISSIONAI_BUILD, getGroup());
			if (iWorkerCount < iMaxWorkers)
				break; //Good to go.
		}
		eBestBuild = NO_BUILD;
		iBestValue = 0;
	}

	if (eBestBuild != NO_BUILD)
	{
		FAssert(NULL != pBestPlot);
		if (ppBestPlot != NULL)
			*ppBestPlot = pBestPlot;
		if (peBestBuild != NULL)
			*peBestBuild = eBestBuild;
	}
	return (eBestBuild != NO_BUILD);
}


bool CvUnitAI::AI_isCityAIType() const
{	// advc.104 (note): There's a similar list in MilitaryBranch::HomeGuard::initUnitsTrained
	return (AI_getUnitAIType() == UNITAI_CITY_DEFENSE ||
			AI_getUnitAIType() == UNITAI_CITY_COUNTER ||
			AI_getUnitAIType() == UNITAI_CITY_SPECIAL ||
			AI_getUnitAIType() == UNITAI_RESERVE ||
			//advc.rom (Afforess): count units on guard mission as city defenders
			AI_getGroup()->AI_getMissionAIType() == MISSIONAI_GUARD_CITY);
}

/*	advc: Renamed from AI_potentialEnemy. Says whether this unit is allowed to
	attack units owned by eTeam, starting a war if necessary. */
bool CvUnitAI::AI_mayAttack(TeamTypes eTeam, CvPlot const& kPlot) const
{
	PROFILE_FUNC();

    // doc: do not attack minors outside of war map
    if (GET_TEAM(eTeam).isMinorCiv() && kPlot.getWarValue(getOwner()) == 0)
        return false;
	if (isEnemy(eTeam, kPlot))
		return true;
	if (AI_getGroup()->AI_isDeclareWar(kPlot))
	{
		//return isPotentialEnemy(eTeam, pPlot);
		return GET_TEAM(getTeam()).AI_mayAttack(eTeam); // advc
	}
	return false;
}

/*	advc: Replaces CvUnit::potentialWarAction, which did almost the same thing as
	CvUnitAI::AI_potentialEnemy (see above). I'm including the BtS implementation
	as a comment. */
bool CvUnitAI::AI_mayAttack(CvPlot const& kPlot) const
{
	if (!kPlot.isOwned())
		return false;
	return AI_mayAttack(kPlot.getTeam(), kPlot);
	// "returns true if unit can initiate a war action with plot (possibly by declaring war)"
	/*if (!kPlot.isOwned())
		return false;
	if (isEnemy(kPlot))
		return true;
	if (AI_getGroup()->AI_isDeclareWar(&kPlot) &&
		GET_TEAM(getTeam()).AI_getWarPlan(kPlot.getTeam()) != NO_WARPLAN)
	{
		return true;
	}
	return false;*/
}

/*	advc: Moved from CvUnit b/c this function eventually checks
	the war plans of the unit owner. Renamed from "isPotentialEnemy".
	The caller wants to know if this unit can currently be attacked
	in kPlot by units of eTeam or if it could soon be attacked (war imminent). */
bool CvUnitAI::AI_isPotentialEnemyOf(TeamTypes eTeam, CvPlot const& kPlot) const
{
	/*	This can be the BARBARIAN_TEAM is this unit isAlwaysHostile.
		Normally, it's the unit owner. */
	TeamTypes eCombatTeam = TEAMID(getCombatOwner(eTeam, kPlot));
	return GET_TEAM(eCombatTeam).AI_mayAttack(eTeam);
}

/*	advc: Moved from CvPlot::getNumVisiblePotentialEnemyDefenders.
	Counts current enemies of this unit and those on whom war is imminent. */
int CvUnitAI::AI_countEnemyDefenders(CvPlot const& kPlot) const
{
	return kPlot.plotCount(PUF_canDefendPotentialEnemy, getOwner(), isAlwaysHostile(kPlot),
			NO_PLAYER, NO_TEAM, PUF_isVisible, getOwner());
}
// advc.opt: (plotCheck, apart from that, copy-pasted from above)
bool CvUnitAI::AI_isAnyEnemyDefender(CvPlot const& kPlot) const
{
	return (kPlot.plotCheck(PUF_canDefendPotentialEnemy, getOwner(), isAlwaysHostile(kPlot),
			NO_PLAYER, NO_TEAM, PUF_isVisible, getOwner()) != NULL);
}


void CvUnitAI::AI_setBirthmark(int iNewValue)
{
	m_iBirthmark = iNewValue;
	if (AI_getUnitAIType() == UNITAI_EXPLORE_SEA)
	{
		if (GC.getGame().circumnavigationAvailable())
		{
			m_iBirthmark -= m_iBirthmark % 4;
			int iExplorerCount = GET_PLAYER(getOwner()).AI_getNumAIUnits(UNITAI_EXPLORE_SEA);
			iExplorerCount += getOwner() % 4;
			if (GC.getMap().isWrapX())
			{
				if ((iExplorerCount % 2) == 1)
				{
					m_iBirthmark += 1;
				}
			}
			if (GC.getMap().isWrapY())
			{
				if (!GC.getMap().isWrapX())
				{
					iExplorerCount *= 2;
				}

				if (((iExplorerCount >> 1) % 2) == 1)
				{
					m_iBirthmark += 2;
				}
			}
		}
	}
}

// XXX make sure this gets called...
void CvUnitAI::AI_setUnitAIType(UnitAITypes eNewValue)
{
	FAssertMsg(eNewValue != NO_UNITAI, "NewValue is not assigned a valid value");

	if (AI_getUnitAIType() != eNewValue)
	{
		getArea().changeNumAIUnits(getOwner(), AI_getUnitAIType(), -1);
		GET_PLAYER(getOwner()).AI_changeNumAIUnits(AI_getUnitAIType(), -1);

		m_eUnitAIType = eNewValue;

		getArea().changeNumAIUnits(getOwner(), AI_getUnitAIType(), 1);
		GET_PLAYER(getOwner()).AI_changeNumAIUnits(AI_getUnitAIType(), 1);

		joinGroup(NULL);
	}
}

/*  advc.159: Like CvUnit::currEffectiveStr, but takes into account first strikes,
	collateral damage and that combat odds increase superlinearly with combat strength.
	The scale is arbitrary, i.e. one should only compare the returned values with each other. */
int CvUnitAI::AI_currEffectiveStr(CvPlot const* pPlot, CvUnit const* pOther,
	bool bCountCollateral, int iBaseCollateral, bool bCheckCanAttack,
	int iCurrentHP, bool bAssumePromotion) const // advc.139
{
	PROFILE_FUNC(); // Called frequently but not extremely so; fine as it is.
	int iCombatStrengthPercent = currEffectiveStr(pPlot, pOther, NULL, iCurrentHP);
	FAssertMsg(iCombatStrengthPercent > 0, "Non-combat unit?");
	/*  <K-Mod> (Moved from CvSelectionGroupAI::AI_sumStrength. Some of the code
		had been duplicated in CvPlayerAI::AI_localDefenceStrength, AI_localAttackStrength). */
	/*  first strikes are not counted in currEffectiveStr.
		actually, the value of first strikes is non-trivial to calculate...
		but we should do /something/ to take them into account. */
	/*  note. Most other parts of the code use 5% per first strike, but I figure
		we should go lower because this unit may get clobbered by collateral damage
		before fighting. */
	// (bCountCollateral means that we're the ones dealing collateral damage)
	int const iFirstStrikeMultiplier = (bCountCollateral ? 5 : 4);
	iCombatStrengthPercent *= 100 + iFirstStrikeMultiplier * firstStrikes() +
			(iFirstStrikeMultiplier / 2) * chanceFirstStrikes()
			+ (bAssumePromotion ? 7 : 0); // advc.139
	iCombatStrengthPercent /= 100;
	if (bCountCollateral && collateralDamage() > 0)
	{
		int iPossibleTargets = collateralDamageMaxUnits();
		if (bCheckCanAttack && pPlot != NULL && pPlot->isVisible(getTeam()))
		{
			iPossibleTargets = std::min(iPossibleTargets,
					pPlot->getNumVisibleEnemyDefenders(this) - 1);
		}
		// If !bCheckCanAttack, then lets not assume kPlot won't get more units on it.
		// advc: But let's put some cap on the number of targets
		else iPossibleTargets = std::min(10, iPossibleTargets);
		if (iPossibleTargets > 0)
		{
			/*	collateral damage is not trivial to calculate. This estimate is pretty rough.
				(Note: collateralDamage() and iBaseCollateral both include factors of 100.) */
			iCombatStrengthPercent += (baseCombatStr() * iBaseCollateral *
					iPossibleTargets * //collateralDamage()
					AI_collateralDmgFactor()) // advc.159
					/ 10000;
		}
	} // </K-Mod>
	FAssert(iCombatStrengthPercent < 100000); // A conservative guard against overflow
	/*  Generally, there's a good chance that a strong unit can kill a weak unit
		and then heal ("defeat in detail"). However, this function is used for
		evaluating imminent stack-on-stack combat. When we already know that
		a stack of stronger units is facing a larger stack of weaker units
		we need to assume a high chance of having to fight multiple enemies in a row. */
	static scaled const rExponent = scaled::max(1,
			fixp(3/4.) * per100(GC.getDefineINT(CvGlobals::POWER_CORRECTION)));
	static scaled const rNormalizationFactor = (rExponent < fixp(1.05) ? 1 :
			// Pretty arbitrary; only need to weigh rounding errors against the danger of overflow.
			25000 / scaled(10000).pow(rExponent));
	/*  Make the AI overestimate weak units a little bit on the low and medium difficulty settings.
		(Not static b/c difficulty can change through load/ new game.) */
	scaled rExponentAdjusted = rExponent - scaled(std::max(0,
			50 - GC.getInfo(GC.getGame().getHandicapType()).getDifficulty()), 250);
	int iR = std::min(25000, // Guard against overflow problems for caller
			(scaled(iCombatStrengthPercent).pow(rExponentAdjusted) *
			rNormalizationFactor).round());
	return std::max(1, iR); // Don't round down to 0
}


int CvUnitAI::AI_sacrificeValue(const CvPlot* pPlot) const
{
	int iCollateralDamageValue = 0;
	if (pPlot != NULL)
	{
		const int iPossibleTargets = std::min(
				(pPlot->getNumVisibleEnemyDefenders(this) - 1),
				collateralDamageMaxUnits());
		if (iPossibleTargets > 0)
		{
			iCollateralDamageValue = collateralDamage();
			iCollateralDamageValue += std::max(0, iCollateralDamageValue - 100);
			iCollateralDamageValue *= iPossibleTargets;
			iCollateralDamageValue /= 5;
		}
	}

	//long iValue; // K-Mod. (the int will overflow)
	/*  Erik (BUG1): Based on his comment he probably meant to use
		a 64 bit integer here since sizeof(int) == sizeof(long) hence a long long is needed */
	long long iValue = 0;

	if (getDomainType() == DOMAIN_AIR)
	{
		iValue = 128 * (100 + currInterceptionProbability());
		if (isNuke())
			iValue += 25000;
		//iValue /= std::max(1, (1 + getUnitInfo().getProductionCost()));
		// <K-Mod>
		iValue /= getUnitInfo().getProductionCost() > 0 ?
				getUnitInfo().getProductionCost() : 180; // </K-Mod>
		iValue *= (maxHitPoints() - getDamage());
		iValue /= 100;
	}
	else
	{
		iValue = 128 * currEffectiveStr(pPlot, pPlot == NULL ? NULL : this);
		iValue *= (100 + iCollateralDamageValue);

		//iValue /= (100 + cityDefenseModifier());
		/*  <advc.001> The above doesn't handle negative modifiers well
			(especially not -100 ...). Bug found by keldath. */
		int iCityDefenseModifier = cityDefenseModifier();
		if(iCityDefenseModifier < 0)
		{
			iCityDefenseModifier = (iCityDefenseModifier * 2) / 5;
			FAssert(iCityDefenseModifier > -100);
		}
		iValue /= std::max(1, 100 + iCityDefenseModifier); // </advc.001>
		iValue *= 100 + withdrawalProbability();
		// BETTER_BTS_AI_MOD, General AI, 05/14/10, jdog5000: START
		/*iValue /= std::max(1, (1 + getUnitInfo().getProductionCost()));
		iValue /= (10 + getExperience());*/ // BtS code
		iValue /= 100; // K-Mod

		// Experience and medics now better handled in LFB
		if (!GC.getDefineBOOL(CvGlobals::LFB_ENABLE))
		{
			iValue *= 10; // K-Mod
			iValue /= 10 + getExperience(); // K-Mod - moved from out of the if.
			iValue *= 10;
			iValue /= 10 + getSameTileHeal() + getAdjacentTileHeal();
		}

		// Value units which can't kill units later, also combat limits mean higher survival odds
		/*if (combatLimit() < 100) {
			iValue *= 150;
			iValue /= 100;
			iValue *= 100;
			iValue /= std::max(1, combatLimit());
		}*/ // BtS
		// K-Mod. The above code is way too extreme.
		// I'm going to replace it with something more meaningful, and less severe.
		iValue *= 100 + 5 * (2 * firstStrikes() + chanceFirstStrikes()) /
				2 + (immuneToFirstStrikes() ? 20 : 0) +
				(combatLimit() < 100 ? 20 : 0);
		iValue /= 100;
		// K-Mod end

		//iValue /= std::max(1, (1 + getUnitInfo().getProductionCost()));
		// <K-Mod>
		iValue /= getUnitInfo().getProductionCost() > 0 ?
				getUnitInfo().getProductionCost() : 180; // </K-Mod>
		// BETTER_BTS_AI_MOD: END
	}

	// From Lead From Behind by UncutDragon
	if (GC.getDefineBOOL(CvGlobals::LFB_ENABLE))
	{	// Reduce the value of sacrificing 'valuable' units - based on great general, limited, healer, experience
		/* bbai code
		iValue *= 100;
		int iRating = LFBgetRelativeValueRating();
		if (iRating > 0)
			iValue /= (1 + 3*iRating);*/
		// K-Mod. cf. LFBgetValueAdjustedOdds
		iValue *= 1000;
		iValue /= std::max(1, 1000 + 1000 * LFBgetRelativeValueRating() *
				GC.getDefineINT(CvGlobals::LFB_ADJUSTNUMERATOR) /
				GC.getDefineINT(CvGlobals::LFB_ADJUSTDENOMINATOR));
		/*	roughly speaking, the second part of the denominator
			is the odds adjustment from LFBgetValueAdjustedOdds.
			It might be more natural to subtract it from the numerator,
			but then we can't guarantee a positive value. */ // K-Mod end
		/*  <advc.048> LFBgetRelativeValueRating is too coarse to account for
			small XP differences. Make sure that XP will at least break ties. */
		const int iXP = getExperience();
		if(iValue > 100 * iXP)
			iValue -= iXP; // </advc.048>
	}
	return truncIntCast<int>(iValue); // advc.001
}

// Lead From Behind, by UncutDragon, edited for K-Mod
void CvUnitAI::LFBgetBetterAttacker(CvUnitAI** ppAttacker, // advc.003u: param was CvUnit**
	CvPlot const* pPlot, bool bPotentialEnemy, int& iAIAttackOdds, int& iAttackerValue)
{
	CvUnit const* pDefender = pPlot->getBestDefender(NO_PLAYER, getOwner(), this,
			!bPotentialEnemy, bPotentialEnemy);

	int iOdds=0;
	int iValue = LFBgetAttackerRank(pDefender, iOdds);

	/*	Combat odds are out of 1000, but the AI routines need odds out of 100,
		and when called from AI_getBestGroupAttacker we return this value.
		Note that I'm not entirely sure if/how that return value is actually used ...
		but just in case I want to make sure I'm returning something consistent
		with what was there before */
	int iAIOdds = (iOdds + 5) / 10;
	iAIOdds += GET_PLAYER(getOwner()).AI_getAttackOddsChange();
	iAIOdds = std::max(1, std::min(iAIOdds, 99));

	if (collateralDamage() > 0)
	{
		int iPossibleTargets = std::min(pPlot->getNumVisibleEnemyDefenders(this) - 1,
				collateralDamageMaxUnits());
		if (iPossibleTargets > 0)
		{
			iValue *= 100 + (//collateralDamage()
					AI_collateralDmgFactor() // advc.159
					* iPossibleTargets) / 5;
			iValue /= 100;
		}
	}
	if (*ppAttacker == NULL || // Nothing to compare against - we're obviously better
		iValue > iAttackerValue) // Compare our adjusted value with the current best
	{
		*ppAttacker = this;
		iAIAttackOdds = iAIOdds;
		iAttackerValue = iValue;
	}
}

/*  K-Mod - test if we should declare war before moving to the target plot.
	(originally, DOW were made inside the unit movement mechanics.
	To me, that seems like a really dumb idea.) */
bool CvUnitAI::AI_considerDOW(CvPlot const& kPlot)
{
	CvTeamAI& kOurTeam = GET_TEAM(getTeam());
	TeamTypes ePlotTeam = kPlot.getTeam();

	//if (!canEnterArea(ePlotTeam, pPlot->area(), true))
	/*  Note: We might be a transport ship which ignores borders, but with escorts
		and cargo who don't ignore borders.
		So, we should check that the whole group can enter the borders.
		(There are faster ways to check, but this is good enough.)
		If it's an amphibious landing, lets just assume that our cargo will need a DoW! */
	if (!getGroup()->canEnterArea(ePlotTeam, kPlot.getArea(), true) ||
		getGroup()->isAmphibPlot(&kPlot))
	{
		if (ePlotTeam != NO_TEAM && kOurTeam.AI_isSneakAttackReady(ePlotTeam))
		{	/*  advc.163: If the tile that we're on has flipped to the war target,
				the DoW is going to bump us out. Could catch this in AI_attackCityMove
				and other functions, and compute a new path. However, bumping ourselves
				may actually be the fastest way to reach the target, so I'm just
				going to go through with the DoW. */
			/*FAssert(!getPlot().isOwned() || GET_TEAM(getPlot().getTeam()).
					getMasterTeam() != ePlotTeam)*/
			if (kOurTeam.canDeclareWar(ePlotTeam))
			{
				if (gUnitLogLevel > 0) logBBAI("    %S declares war on %S with AI_considerDOW (%S - %S).", kOurTeam.getName().GetCString(), GET_TEAM(ePlotTeam).getName().GetCString(), getName(0).GetCString(), GC.getInfo(AI_getUnitAIType()).getDescription());
				kOurTeam.declareWar(ePlotTeam, true, NO_WARPLAN);
				getPathFinder().reset();
				return true;
			}
		}
	}
	return false;
}

/*  AI_considerPathDOW checks each plot on the path until the end of the turn.
	Sometimes the end plot is in friendly territory, but we need to declare war
	to actually get there. This situation is very rare, but unfortunately we
	have to check for it every time - because otherwise, when it happens,
	the AI will just get stuck. */
bool CvUnitAI::AI_considerPathDOW(CvPlot const& kPlot, MovementFlags eFlags)
{
	PROFILE_FUNC();

	if (!(eFlags & MOVE_DECLARE_WAR))
		return false;

	if (!generatePath(kPlot, eFlags, true))
	{
		FErrorMsg("AI_considerPathDOW didn't find a path.");
		return false;
	}

	bool bDOW = false;
	GroupPathNode* pNode = getPathFinder().getEndNode(); // TODO: rewrite so that getEndNode isn't used.
	while (!bDOW && pNode != NULL)
	{
		CvPlot const& kLoopPlot = pNode->getPlot(); // advc
		/*  we need to check DOW even for moves several turns away -
			otherwise the actual move mission may fail to find a path.
			however, I would consider it irresponsible to call this function for multi-move missions.
			(note: amphibious landings may say 2 turns, even though it is really only 1...) */
		FAssert(pNode->getPathTurns() <= 1 ||
				(pNode->getPathTurns() == 2 && getGroup()->isAmphibPlot(&kLoopPlot)));
		bDOW = AI_considerDOW(kLoopPlot);
		pNode = pNode->m_pParent;
	}

	return bDOW;
}
// K-Mod end

void CvUnitAI::AI_animalMove()
{
	PROFILE_FUNC();
	bool bAttackAttempted = false; // advc.309
	{
		int iAttackPer1000 = GC.getInfo(GC.getGame().getHandicapType()).
				getAnimalAttackProb() * 10;
		// <advc.309> Times fraction of remaining hitpoints
		iAttackPer1000 *= std::max(currHitPoints(), maxHitPoints() / 3);
		iAttackPer1000 /= maxHitPoints(); // </advc.309>
		if (SyncRandSuccess1000(iAttackPer1000))
		{
			if (AI_anyAttack(1, 0))
			{
				return;
			}
			bAttackAttempted = true; // advc.309
		}
	}
	// advc.309: Animals shouldn't heal so readily
	if (SyncRandSuccessRatio(getDamage(), maxHitPoints()))
	{
		if (AI_heal())
		{
			return;
		}
	}
	if (AI_patrol())
	{
		return;
	}
	// <advc.309> Cornered animal will attack
	if (!bAttackAttempted)
	{
		if (AI_anyAttack(1, 0))
		{
			return;
		}
	} // </advc.309>
	getGroup()->pushMission(MISSION_SKIP);
}


void CvUnitAI::AI_settleMove()
{
	PROFILE_FUNC();

	CvPlayerAI const& kOwner = GET_PLAYER(getOwner()); // K-Mod
	/*	advc (note): This was MOVE_SAFE_TERRITORY in BtS, which had prevented
		passage through foreign (open) borders. */
	MovementFlags const eMoveFlags = MOVE_NO_ENEMY_TERRITORY; // K-Mod

	if (kOwner.getNumCities() == 0)
	{
		if (AI_foundFirstCity()) // advc.108: Moved into new function
			return;
	}
	/*int iDanger = kOwner.AI_getPlotDanger(plot(), 3);
	if (iDanger > 0) {
		if ((getPlot().getOwner() == getOwner()) || (iDanger > 2))*/ // BtS
	bool const bDanger = kOwner.AI_isAnyPlotDanger(getPlot()); // advc.opt
	// K-Mod
	if (bDanger)
	{
		//int iOurDefence = getGroup()->AI_sumStrength(0); // not counting defensive bonuses
		//int iEnemyAttack = kOwner.AI_localAttackStrength(plot(), NO_TEAM, getDomainType(), 2, true);
		if (!getGroup()->canDefend() ||
			100 * kOwner.AI_localAttackStrength(plot()) >
			80 * AI_getGroup()->AI_sumStrength(0))
	// K-Mod end
		{	// flee
			joinGroup(NULL);
			if(AI_retreatToCity())
				return;
			/*if(AI_safety())
				return;
			getGroup()->pushMission(MISSION_SKIP);*/ // BtS
			// fallthrough. There might be something useful we can do. eg. AI_handleStranded!
		}
	}

	// doc: rebuild ability used if there are no settlement targets
	if (GET_PLAYER(getOwner()).AI_getNumCitySites() == 0)
	{
		if (AI_rebuildMove(2 * GET_PLAYER(getOwner()).getProductionNeeded(getUnitType())))
		{
			return;
		}
	}

	int iAreaBestFoundValue = 0;
	int iOtherBestFoundValue = 0;

	for (int i = 0; i < kOwner.AI_getNumCitySites(); i++)
	{
		CvPlot& kSite = kOwner.AI_getCitySite(i);
		if ((kSite.isArea(getArea()) || canMoveAllTerrain()) &&
			// UNOFFICIAL_PATCH: Only count city sites we can get to
			generatePath(kSite, eMoveFlags, true))
		{
			if (at(kSite) && canFound(plot()))
			{
				if (gUnitLogLevel >= 2) logBBAI("    Settler founding in place since it's at a city site %d, %d", getX(), getY());
				getGroup()->pushMission(MISSION_FOUND);
				return;
			}
			// K-Mod. If we are already heading to this site, then keep going.
			// (disabled. This is no longer required - I hope.)
			/*else {
				CvPlot* pMissionPlot = getGroup()->AI_getMissionAIPlot();
				if (pMissionPlot == pCitySitePlot && getGroup()->AI_getMissionAIType() == MISSIONAI_FOUND) {
					// safety check. (cf. conditions in AI_found)
					if (getGroup()->canDefend() || kOwner.AI_plotTargetMissionAIs(pMissionPlot, MISSIONAI_GUARD_CITY) > 0) {
						if (gUnitLogLevel >= 2) logBBAI("    Settler continuing mission to %d, %d", pCitySitePlot->getX(), pCitySitePlot->getY());
						CvPlot& kEndTurnPlot = getPathEndTurnPlot();
						pushGroupMoveTo(kEndTurnPlot, MOVE_SAFE_TERRITORY, false, false, MISSIONAI_FOUND, pCitySitePlot);
						return;
					}
				}
			}*/
			// K-Mod end
			iAreaBestFoundValue = std::max(iAreaBestFoundValue,
					kSite.getFoundValue(getOwner()));

		}
		else
		{
			iOtherBestFoundValue = std::max(iOtherBestFoundValue,
					kSite.getFoundValue(getOwner()));
		}
	}

	/*  BETTER_BTS_AI_MOD, Gold AI, 01/16/09, jdog5000: START
		No new settling of colonies when AI is in financial trouble */
	if (getPlot().isCity() && getPlot().getOwner() == getOwner())
	{
		if (kOwner.AI_isFinancialTrouble())
			iOtherBestFoundValue = 0;
	} // BETTER_BTS_AI_MOD: END

	if (iAreaBestFoundValue == 0 && iOtherBestFoundValue == 0)
	{
		if (GC.getGame().getGameTurn() - getGameTurnCreated() > 20)
		{
			if (getTransportUnit() != NULL)
				getTransportUnit()->unloadAll();
			if (getTransportUnit() == NULL)
			{
				// BETTER_BTS_AI_MOD, Unit AI, 11/30/08, jdog5000: guard added
				if (!kOwner.AI_isAnyUnitTargetMissionAI(*getGroup()->getHeadUnit(), MISSIONAI_PICKUP))
				{
					// doc: use for rebuilding before scrapping them
					if (AI_rebuildMove(GET_PLAYER(getOwner()).getProductionNeeded(getUnitType())))
						return;

					//FErrorMsg("advc.test: Just to see how frequently the AI scraps settlers"); // hardly ever
					scrap(); //may seem wasteful, but settlers confuse the AI.
					return;
				}
			}
		}
	}
	bool bMoveToCoast = false; // advc.040
	if (iOtherBestFoundValue * 100 > iAreaBestFoundValue * 110)
	{
		if (getPlot().getOwner() == getOwner())
		{
			if (AI_load(UNITAI_SETTLER_SEA, MISSIONAI_LOAD_SETTLER, NO_UNITAI,
				-1, -1, -1, 0, eMoveFlags))
			{
				return;
			}  // <advc.040>
			else
			{
				CvCity* pCity = getPlot().getPlotCity();
				if(pCity != NULL && !pCity->isCoastal() &&
					getGroup()->getNumUnits() <= 3 && getArea().getNumAIUnits(
					getOwner(), UNITAI_SETTLER_SEA) > 0)
				{
					bMoveToCoast = true; // Check MaxCityElimination first
				}
			} // </advc.040>
		}
	}

	/*if ((iAreaBestFoundValue > 0) && getPlot().isBestAdjacentFound(getOwner())) {
		if (canFound(plot())) {
			if (gUnitLogLevel >= 2) logBBAI("    Settler founding in place due to best adjacent found");
			getGroup()->pushMission(MISSION_FOUND);
			return;
		}
	}*/ // BtS - disabled by K-Mod. We go to a lot of trouble to pick good city sites. Don't let this mess it up for us!

	/*if (!GC.getGame().isOption(GAMEOPTION_ALWAYS_PEACE) && !GC.getGame().isOption(GAMEOPTION_AGGRESSIVE_AI) && !getGroup()->canDefend()) {
		if (AI_retreatToCity())
			return;
	} */ /* BtS - disabled by K-Mod. Let them risk moving an undefended settler..
			there are other checks in place to help them. */

	if (getPlot().isCity() && getPlot().getOwner() == getOwner() &&
		bDanger && GC.getGame().getMaxCityElimination() > 0 &&
		getGroup()->getNumUnits() < 3)
	{
		getGroup()->pushMission(MISSION_SKIP);
		return;
	}
	if (iAreaBestFoundValue > 0)
	{
		if (AI_found(eMoveFlags))
			return;
	}
	// <advc.040>
	if(bMoveToCoast && AI_moveSettlerToCoast())
		return; // </advc.040>
	if (getPlot().getOwner() == getOwner() &&
		// advc.040: Don't clog up a transport that might be needed for Worker movement
		iOtherBestFoundValue > 0)
	{
		if (AI_load(UNITAI_SETTLER_SEA, MISSIONAI_LOAD_SETTLER, NO_UNITAI,
			-1, -1, -1, 0, eMoveFlags))
		{
			return;
		}
		// BBAI TODO: Go to a good city (like one with a transport) ...
		// (advc.040: ^Now adressed in AI_moveSettlerToCoast)
	}

	// K-Mod: sometimes an unescorted settler will join up with an escort mid-mission..
	if(iAreaBestFoundValue + iOtherBestFoundValue > 0) // advc.040: But surely not if we have nowhere to settle
	{
		FOR_EACH_GROUPAI_VAR(pLoopGroup, kOwner)
		{
			if (pLoopGroup == getGroup() || pLoopGroup->getNumUnits() <= 0)
				continue;
			if (pLoopGroup->AI_getMissionAIUnit() == this &&
				pLoopGroup->AI_getMissionAIType() == MISSIONAI_GROUP)
			{
				int iPathTurns = MAX_INT;
				generatePath(pLoopGroup->getPlot(), eMoveFlags, true, &iPathTurns, 2);
				if (iPathTurns > 2)
					continue;
				CvPlot& kEndTurnPlot = getPathEndTurnPlot();
				if (at(kEndTurnPlot))
				{
					//getGroup()->pushMission(MISSION_SKIP, 0, 0, 0, false, false, MISSIONAI_GROUP, pEndTurnPlot);
					pLoopGroup->mergeIntoGroup(getGroup());
					FAssert(getGroup()->getNumUnits() > 1);
					FAssert(getGroup()->getHeadUnitAIType() == UNITAI_SETTLE);
				}
				else
				{
					CvSelectionGroupAI* pGroup = AI_getGroup(); // advc
					// if we were on our way to a site, keep the current mission plot.
					if (pGroup->AI_getMissionAIType() == MISSIONAI_FOUND &&
						pGroup->AI_getMissionAIPlot() != NULL)
					{
						pushGroupMoveTo(kEndTurnPlot, eMoveFlags, false, false,
								MISSIONAI_FOUND, pGroup->AI_getMissionAIPlot());
					}
					else
					{
						pushGroupMoveTo(kEndTurnPlot, eMoveFlags, false, false,
								MISSIONAI_GROUP, NULL, pLoopGroup->getHeadUnit());
					}
				}
				return;
			}
		}
	} // K-Mod end

	if(AI_retreatToCity())
		return;
	// K-Mod
	if (AI_handleStranded())
		return;
	// K-Mod end
	if (AI_safety())
		return;
	// doc: rebuild
	if (AI_rebuildMove(2 * GET_PLAYER(getOwner()).getProductionNeeded(getUnitType())))
		return;
	getGroup()->pushMission(MISSION_SKIP);
}

// advc.108: New function for code merged from the Better BUG AI mod
bool CvUnitAI::AI_foundFirstCity()
{
	// Afforess & Fuyu, Check for Good City Sites Near Starting Location, 09/18/10, START:
	// <advc>
	CvGame const& kGame = GC.getGame();
	CvPlayerAI& kOwner = GET_PLAYER(getOwner());
	CvGameSpeedInfo const& kSpeed = GC.getInfo(kGame.getGameSpeedType());
	/*  Earlier exploreMove may have revealed more tiles. Don't set bStartingLoc;
		that setting rules out e.g. plots with a goody hut or at the edge of a
		flat map. I've added some getNumCities()<=0 checks to AI_foundValue. */
	kOwner.AI_updateFoundValues(false); // </advc>
	int iGameSpeedPercent = (2 * kSpeed.getTrainPercent()
			+ kSpeed.getConstructPercent() + kSpeed.getResearchPercent()) / 4;
	int iMaxFoundTurn = (iGameSpeedPercent + 50) / 150; //quick 0, normal/epic 1, marathon 2
	if(!kGame.isScenario() && // advc: Let the creator of the scenario decide where the AI settles
		canMove() && !kOwner.AI_isPlotCitySite(getPlot()) &&
		kGame.getElapsedGameTurns() <= iMaxFoundTurn)
	{
		CvPlot* pBestPlot = NULL;
		int iBestValue = 0;
		int iBestFoundTurn = 0;
		for (int iCitySite = 0; iCitySite < kOwner.AI_getNumCitySites(); iCitySite++)
		{
			CvPlot& kSite = kOwner.AI_getCitySite(iCitySite);
			if(!AI_canEnterByLand(kSite.getArea()) && // advc.030 (replacing same-area check)
				!canMoveAllTerrain())
			{
				continue;
			}
			//int iPlotValue = kOwner.AI_foundValue(pCitySite->getX(), pCitySite->getY());
			int iPlotValue = kSite.getFoundValue(kOwner.getID());
			if(iPlotValue <= iBestValue)
				continue;
			//Can this unit reach the plot this turn? (getPathLastNode()->m_iData2 == 1)
			//Will this unit still have movement points left to found the city the same turn? (getPathLastNode()->m_iData1 > 0))
			if (generatePath(kSite))
			{
				int iFoundTurn = kGame.getElapsedGameTurns() +
						/*getPathLastNode()->m_iData2 -
						(getPathLastNode()->m_iData1 > 0 ? 1 : 0);*/
						// advc: Adapted to K-Mod pathfinder
						getPathFinder().getPathTurns() -
						(getPathFinder().getFinalMoves() > 0 ? 1 : 0);
				if (iFoundTurn <= iMaxFoundTurn)
				{
					iPlotValue *= 100; //more precision
					/*  the slower the game speed, the less penality the plotvalue
						gets for long walks towards it.
						On normal it's -18% per turn */
					/*  advc: 18% seems a bit much; try 15%. K-Mod found values
						aren't quite on the same scale as BBAI. */
					iPlotValue *= 100 - std::min(100, ((1500/
							std::max(1, iGameSpeedPercent)) * iFoundTurn));
					iPlotValue /= 100;
					if (iPlotValue > iBestValue)
					{
						iBestValue = iPlotValue;
						iBestFoundTurn = iFoundTurn;
						pBestPlot = &kSite;
					}
				}
			}
		}
		if (pBestPlot != NULL)
		{
			//Don't give up coast or river, don't settle on bonus with food
			/*if ((getPlot().isRiver() && !pBestPlot->isRiver())
				|| (getPlot().isCoastalLand(GC.getMIN_WATER_SIZE_FOR_OCEAN()) && !pBestPlot->isCoastalLand(GC.getMIN_WATER_SIZE_FOR_OCEAN()))
				|| (pBestPlot->getBonusType(NO_TEAM) != NO_BONUS && pBestPlot->calculateNatureYield(YIELD_FOOD, getTeam(), true) > 0))*/
			// advc: I think AI_foundValue can handle the other stuff
			if (getPlot().isFreshWater() && !pBestPlot->isFreshWater())
				pBestPlot = NULL;
		}
		if (pBestPlot != NULL)
		{
			if (gUnitLogLevel >= 2) logBBAI("    Settler not founding in place but moving %d, %d to nearby city site at %d, %d (%d turns away) with value %d)", (pBestPlot->getX() - getX()), (pBestPlot->getY() - getY()), pBestPlot->getX(), pBestPlot->getY(), iBestFoundTurn, iBestValue);
			pushGroupMoveTo(*pBestPlot, MOVE_SAFE_TERRITORY, false, false,
					MISSIONAI_FOUND, pBestPlot);
			return true;
		}
	}
	// Afforess & Fuyu: END
	if (canFound(plot()))
	{
		if (gUnitLogLevel >= 2) logBBAI("    Settler founding in place");
		getGroup()->pushMission(MISSION_FOUND);
		return true;
	}
	return false;
}

// advc.113b: Cut from AI_workerMove
CvCityAI* CvUnitAI::AI_getCityToImprove() const
{
	if (getPlot().getOwner() != getOwner() /* advc.113b: */ || isCargo())
		return NULL;
	CvCityAI* pCity = getPlot().AI_getPlotCity();
	if (pCity == NULL)
		pCity = getPlot().AI_getWorkingCity();
	return pCity;
}


void CvUnitAI::AI_workerMove(/* advc.113b: */ bool bUpdateWorkersHave)
{
	PROFILE_FUNC();

	// <advc.113b>
	if (bUpdateWorkersHave)
	{
		CvCityAI* pOldCity = AI_getCityToImprove();
		AI_workerMove(false); // Recursive call
		CvCityAI* pNewCity = NULL;
		if (plot() != NULL) // May have been scrapped
		{
			CvPlot* pNewMissionPlot = AI_getGroup()->AI_getMissionAIPlot();
			if (pNewMissionPlot != NULL)
				pNewCity = pNewMissionPlot->AI_getWorkingCity();
			if (pNewCity == NULL)
				pNewCity = AI_getCityToImprove();
		}
		if (pOldCity != pNewCity)
		{
			if (pOldCity != NULL)
				pOldCity->AI_changeWorkersHave(-1);
			if (pNewCity != NULL)
				pNewCity->AI_changeWorkersHave(1);
		}
		return;
	} // </advc.113b>

	bool bCanRoute = canBuildRoute();
	bool bNextCity = false;
	bool bCanRetreat = true; // advc.opt: Try only once (uses of this variable not marked with comments)
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());

	// XXX could be trouble...
	if (getPlot().getOwner() != getOwner())
	{
		if (AI_retreatToCity())
			return;
		bCanRetreat = false;
	}

	if (!isHuman())
	{
		if (getPlot().getOwner() == getOwner())
		{
			if (AI_load(UNITAI_SETTLER_SEA, MISSIONAI_LOAD_SETTLER, UNITAI_SETTLE,
				2, -1, -1, 0, MOVE_SAFE_TERRITORY))
			{
				return;
			}
		}
	}

	if (bCanRetreat && !getGroup()->canDefend())
	{
		if (kOwner.AI_isPlotThreatened(plot(), 2))
		{
			// XXX maybe not do this??? could be working productively somewhere else...
			if (AI_retreatToCity())
				return;
			bCanRetreat = false;
		}
	}

	if (bCanRoute && getPlot().getOwner() == getOwner()) // XXX team???
	{
		BonusTypes eNonObsoleteBonus = getPlot().getNonObsoleteBonusType(getTeam());
		if (eNonObsoleteBonus != NO_BONUS)
		{
			if (!getPlot().isConnectedToCapital())
			{
				ImprovementTypes eImprovement = getPlot().getImprovementType();
				//if (NO_IMPROVEMENT != eImprovement && GC.getInfo(eImprovement).isImprovementBonusTrade(eNonObsoleteBonus))
				if (kOwner.doesImprovementConnectBonus(eImprovement, eNonObsoleteBonus))
				{
					if (AI_connectPlot(getPlot()))
						return;
				}
			}
		}
	}
	/*  <advc.117>, advc.121: A measure of how busy we are. Compute it here and pass
		it to subroutines in order to avoid computing it multiple times. */
	int iNeededWorkersInArea = kOwner.AI_neededWorkers(getArea());
	int iMissingWorkersInArea = iNeededWorkersInArea -
			kOwner.AI_totalAreaUnitAIs(getArea(), UNITAI_WORKER);
	// </advc.117>

	/*CvPlot* pBestBonusPlot = NULL;
	BuildTypes eBestBonusBuild = NO_BUILD;
	int iBestBonusValue = 0;
	if (AI_improveBonus(25, &pBestBonusPlot, &eBestBonusBuild, &iBestBonusValue)) */
	if (AI_improveBonus( // K-Mod
		iMissingWorkersInArea)) // advc.121
	{
		return;
	}
	if (bCanRoute && !isBarbarian())
	{
		if (AI_connectCity())
			return;
	}

	CvCityAI const* pCity = AI_getCityToImprove(); // advc.113b: Moved into auxiliary function

	/*if (pCity != NULL) {
		bool bMoreBuilds = false;
		for (WorkingPlotIter it(getPlot(), false); it.hasNext(); ++it) {
			if (it->getImprovementType() == NO_IMPROVEMENT &&
					pCity->AI_getBestBuildValue(it.currID()) > 0) {
				ImprovementTypes eImprovement = (ImprovementTypes)GC.getInfo((BuildTypes)
						pCity->AI_getBestBuild(iI)).getImprovement();
				if (eImprovement != NO_IMPROVEMENT) {
					bMoreBuilds = true;
					break;
		} } }
		if (bMoreBuilds) {
			if (AI_improveCity(*pCity))
				return;
	} }*/
	if (pCity != NULL)
	{
		int const iNeed = pCity->AI_getWorkersNeeded();
		int const iHave = pCity->AI_getWorkersHave();
		/* bts code
		if (iNeed > 0 && (getPlot().isCity() || iNeed < (1 + iHave * 2) / 3)) */
		/*  K-Mod. Is it just me, or did they get this backwards?
			Note: this worker is currently at pCity, and so it's probably counted in AI_getWorkersHave. */
		//if (iNeed > 0 && (getPlot().isCity() || iHave - 1 <= (1 + iNeed * 2) / 3))
		/*  <advc.113> The above makes the worker leave its city even if the remaining
			workers will only be 2/3 of what's needed, e.g. when iHave=iNeed=3.
			I think the intention was, on the contrary, to let more workers improve
			a city than are needed. iHave=3, iNeed=2 seems like the only relevant
			example. (Note that iNeed will eventually decrease when too many workers
			improve a city.)
			The bigger issue is that the K-Mod (and BtS) code won't let a worker
			leave when iHave=2, iNeed=1, which happens all the time. Also, I
			don't think newly trained workers (isCity) should unconditionally stay.
			It would be nice if CvCityAI::AI_updateWorkersNeededHere used
			times-100 precision, but it rounds values in several places, so that's
			difficult to change. */
		if (iNeed > 0 && ((getPlot().isCity() && iHave - 1 < 2 * iNeed) ||
			iHave - 1 < (1 + iNeed * 4) / 3)) // </advc.113>
		{
			if (AI_improveCity(*pCity))
				return;
		}
	}

	/*if (AI_improveLocalPlot(2, pCity))
		return;*/ // BtS - Moved by K-Mod

	bool bBuildFort = false;
	//if (GC.getGame().getSorenRandNum(5, "AI Worker build Fort with Priority"))
	/*	advc.001: The above tests !=0. Why should a Fort be given priority
		80% of the time? */
	if (SyncRandSuccess100(20))
	{
		//bool bCanal = ((100 * getArea().getNumCities()) / std::max(1, GC.getGame().getNumCities()) < 85);
		/*	K-Mod. The current AI for canals doesn't work anyway;
			so lets skip it to save time. */
		bool const bCanal = false;
		bool bAirbase = false;
		bAirbase = (kOwner.AI_totalUnitAIs(UNITAI_PARADROP) ||
				kOwner.AI_totalUnitAIs(UNITAI_ATTACK_AIR) ||
				kOwner.AI_totalUnitAIs(UNITAI_MISSILE_AIR));
		if (bCanal || bAirbase)
		{
			if (AI_fortTerritory(bCanal, bAirbase))
				return;
		}
		bBuildFort = true;
	}

	if (bCanRoute && isBarbarian())
	{
		if (AI_connectCity())
			return;
	}

	if (!isBarbarian() // advc.300
		// advc.113: This has already been decided: we want to improve another city.
		/*&& (pCity == NULL || iNeed == 0 || iHave > iNeed + 1)*/)
	{	/*if (pBestBonusPlot != NULL && iBestBonusValue >= 15) {
			if (AI_improvePlot(pBestBonusPlot, eBestBonusBuild))
				return;
		}*/ // disabled by K-Mod. (this did nothing - ever - because of a bug.)

		/*if (pCity == NULL)
			pCity = GC.getMap().findCity(getX(), getY(), getOwner());*/ // XXX do team???
		if (AI_nextCityToImprove(pCity))
			return;
		bNextCity = true;
	}
	/*if (pBestBonusPlot != NULL) {
		if (AI_improvePlot(pBestBonusPlot, eBestBonusBuild))
			return;
	}*/ // K-Mod

	if (pCity != NULL)
	{
		if (AI_improveCity(*pCity))
			return;
	}
	// K-Mod. (moved from higher up)
	if (AI_improveLocalPlot(2, pCity, /* advc.117: */ iMissingWorkersInArea))
		return;

	// <advc.300> None of the stuff below seems relevant for Barbarian workers
	if (isBarbarian())
	{
		if (!bCanRetreat || !AI_retreatToCity(false, true))
		{
			if (SyncRandOneChanceIn(6))
				scrap(); // Don't let it stand around indefinitely
			else getGroup()->pushMission(MISSION_SKIP);
		}
		return;
	} // </advc.300>

	if (!bNextCity)
	{
		if (AI_nextCityToImprove(pCity))
			return;
	}

	if (bCanRoute)
	{
		if (AI_routeTerritory(true))
			return;

		if (AI_connectBonus(false))
			return;

		if (AI_routeCity())
			return;
		bCanRoute = false; // advc.opt: Don't try again
	}

	if (AI_irrigateTerritory())
		return;

	if (!bBuildFort)
	{
		//bool bCanal = ((100 * getArea().getNumCities()) / std::max(1, GC.getGame().getNumCities()) < 85);
		bool const bCanal = false; // K-Mod. The current AI for canals doesn't work anyway; so lets skip it to save time.
		bool bAirbase = false;
		bAirbase = (kOwner.AI_totalUnitAIs(UNITAI_PARADROP) ||
				kOwner.AI_totalUnitAIs(UNITAI_ATTACK_AIR) ||
				kOwner.AI_totalUnitAIs(UNITAI_MISSILE_AIR));
		if (bCanal || bAirbase)
		{
			if (AI_fortTerritory(bCanal, bAirbase))
				return;
		}
	}

	// rfc: disabled
	/*if (bCanRoute &&
		// advc.113: If there is more than 1 worker too many, try AI_load first.
		iMissingWorkersInArea >= -1)
	{
		if (AI_routeTerritory())
			return;
		bCanRoute = false; // advc.113: Don't try again
	}*/
	scaled rLoadProb = 0; // advc.113: Needed for the scrap decision
	if (!isHuman() || (isAutomated() && GET_TEAM(getTeam()).getNumWars() <= 0))
	{
		if (!isHuman() || getGameTurnCreated() < GC.getGame().getGameTurn())
		{
			if (AI_nextCityToImproveAirlift())
				return;
		}

		if (!isHuman())
		{	/*  <advc.113> Collision avoidance: Load probabilistically to avoid
				shipping out too many workers at once. (There is no cheap function
				to check how many of the area's workers have already been loaded
				into transports.) */
			int const iAreaWorkers = kOwner.AI_totalAreaUnitAIs(getArea(), UNITAI_WORKER);
			int const iAreaCities = getArea().getCitiesPerPlayer(getOwner());
			rLoadProb = scaled(3 * iAreaWorkers - 2 * iAreaCities, 24);
			if (pCity != NULL)
			{
				int iLocalMissing = pCity->AI_getWorkersNeeded() - pCity->AI_getWorkersHave();
				if (iLocalMissing > 0)
					rLoadProb /= 1 + iLocalMissing;
			}
			if (iAreaCities <= 0 ||
				(iMissingWorkersInArea <= 0 && iAreaWorkers > 1 &&
				SyncRandSuccess(rLoadProb)))
			{ // </advc.113>
				/*if (AI_load(UNITAI_SETTLER_SEA, MISSIONAI_LOAD_SETTLER, NO_UNITAI, -1, -1, -1, -1, MOVE_SAFE_TERRITORY))
					return; */
				// BETTER_BTS_AI_MOD, Worker AI, 01/14/09, jdog5000: START
				if (AI_load(UNITAI_SETTLER_SEA, MISSIONAI_LOAD_SETTLER,
					UNITAI_WORKER, // Fill up boats which already have workers
					-1, -1, -1, -1, MOVE_SAFE_TERRITORY))
				{
					return;
				}
				// Avoid filling a galley which has just a settler in it, reduce chances for other ships
				if (AI_load(UNITAI_SETTLER_SEA, MISSIONAI_LOAD_SETTLER, NO_UNITAI,
					-1, 2, -1, -1, MOVE_SAFE_TERRITORY))
				{
					return;
				} // BETTER_BTS_AI_MOD: END
				rLoadProb = 0; // advc.113: OK to scrap
			}
		}
	}

	// <advc.113> Second route-territory attempt
	if (bCanRoute && AI_routeTerritory())
		return; // </advc.113>

	if (AI_improveLocalPlot(3, NULL, /* advc.117: */ iMissingWorkersInArea))
		return;
	/*  <advc.113> Want to base the scrap decision on the working city. Try retreating
		before scrapping if there is none. */
	if (pCity == NULL && bCanRetreat)
	{
		if (AI_retreatToCity(false, true))
			return;
		bCanRetreat = false;
	} // </advc.113>
	if (!isHuman() && AI_getUnitAIType() == UNITAI_WORKER)
	{	/*if (GC.getGame().getElapsedGameTurns() > 10) {
			if (GET_PLAYER(getOwner()).AI_totalUnitAIs(UNITAI_WORKER) > GET_PLAYER(getOwner()).getNumCities()) */
		// K-Mod
		if (6 * GC.getGame().getElapsedGameTurns() >
			GC.getInfo(GC.getGame().getGameSpeedType()).getResearchPercent() &&
			iMissingWorkersInArea < 0) // advc.113: Cheap initial check
		{
			int iTotalThresh = std::max(GC.getInfo(GC.getMap().getWorldSize()).
					/*  advc (comment): 3/2 * NumCities is fine and, in itself,
						not at all a reason to scrap. But having way too many
						workers in the area is a problem. */
					getTargetNumCities(), (kOwner.getNumCities() * 3) / 2);
			int const iOwnerEra = kOwner.getCurrentEra();
			// Higher threshold if climate is tropical
			if (iOwnerEra == GC.getGame().getStartEra() || kOwner.AI_getCurrEra() <= 3)
			{	// Between 2 (Tropical) and 6 (Arid, Cold). Temperate: 5
				int iJungleLatitude = ::range(GC.getInfo(GC.getMap().getClimate()).
						getJungleLatitude(), 0, 9);
				iTotalThresh = (iTotalThresh * (32 - iJungleLatitude)) / 27;
			}
			/*  advc.113: Don't use AI_totalUnitAIs here; if we're training workers,
				then we probably don't have too many. */
			int iTotalHave = kOwner.AI_getNumAIUnits(UNITAI_WORKER);
			if (iTotalHave > iTotalThresh &&
				getArea().getNumAIUnits(getOwner(), UNITAI_WORKER) >
				// advc.113: Add 1 b/c e.g. 2 have, 1 needed shouldn't lead to scrapping
				(iNeededWorkersInArea * 3 + 1) / 2 &&
		// K-Mod end
				kOwner.calculateUnitCost() > 0)
			{	// <advc.113>
				if (pCity == NULL || pCity->AI_getWorkersNeeded() < pCity->AI_getWorkersHave() + 1)
				{	/*  Scrap eventually b/c the worker could be stuck in this area,
						but there's no hurry. */
					scaled rScrapProb(iTotalHave, std::max(1, iTotalThresh));
					rScrapProb -= 1;
					rScrapProb *= rScrapProb;
					// Don't scrap if waiting to load
					rScrapProb *= scaled::max(0, 1 - 3 * rLoadProb);
					if (rScrapProb > 0) // to save time
					{
						int iFinancialTroubleMargin = kOwner.AI_financialTroubleMargin();
						rScrapProb *= per100(100 - std::min(iFinancialTroubleMargin, 85));
					}
					if (SyncRandSuccess(rScrapProb))
					{ // </advc.113>
						scrap();
						return;
					}
				}
			}
		}
	}

	if (bCanRetreat && AI_retreatToCity(false, true))
		return;

	/*if (AI_retreatToCity())
		return; */ // disabled by K-Mod (redundant)

	// K-Mod
	if(AI_handleStranded())
		return;
	// K-Mod end

	if (AI_safety())
		return;

	getGroup()->pushMission(MISSION_SKIP);
}

// advc.300:
namespace
{
	scaled barbarianAggressionChance(scaled rCitiesPerCiv, scaled rTargetCitiesPerCiv)
	{
		FAssert(rTargetCitiesPerCiv >= 1);
		scaled rError = rTargetCitiesPerCiv - rCitiesPerCiv;
		if (rError <= 0)
			return 1;
		/*	Chance not to act aggressively proportional to the relative square error
			(relative to the target city count minus 1 b/c we really care how many
			settlers have been trained). Tbd.: Shouldn't hardcode the number of
			starting settlers like this. */
		scaled r = 1 - fixp(2.4) * SQR(rError / (rTargetCitiesPerCiv - 1));
		return r;
	}
}


void CvUnitAI::AI_barbAttackMove()
{
	PROFILE_FUNC();
	CvGame const& kGame = GC.getGame();
	if (AI_guardCity(false, true, 1))
	{
		return;
	}

	if (getPlot().isGoody() &&
		!isAnimal()) // doc: animals don't defend goody huts
	{
		// BETTER_BTS_AI_MOD, Barbarian AI, 05/15/10, jdog5000: START
		if (AI_anyAttack(1, 90))
		{
			return;
		} // BETTER_BTS_AI_MOD: END

		if (getPlot().plotCount(PUF_isUnitAIType, UNITAI_ATTACK, -1, getOwner()) <= 2 && // doc: increased from 1 to 2
			// BETTER_BTS_AI_MOD, Barbarian AI, 05/15/10, jdog5000:
			getGroup()->getNumUnits() == 1)
		{
			getGroup()->pushMission(MISSION_SKIP);
			return;
		}
	}

	if (SyncRandOneChanceIn(2))
	{
		if (AI_pillageRange(1))
		{
			return;
		}
	}

	if (AI_anyAttack(1, 20))
	{
		return;
	}

	// <advc.300> See also CvTeamAI::AI_calculateAreaAIType
	if (getArea().getAreaAIType(getTeam()) != AREAAI_ASSAULT)
	{
		int iCivsInArea = 0;
		for (PlayerIter<CIV_ALIVE> itCivPlayer; itCivPlayer.hasNext(); ++itCivPlayer)
		{
			/*	Perhaps an owned tile (across the sea) should suffice, but tiles
				per player aren't cached. */
			if (getArea().getCitiesPerPlayer(itCivPlayer->getID()) > 0 &&
				!itCivPlayer->isOneCityChallenge())
			{
				iCivsInArea++;
			}
		}
		int const iCivCitiesInArea = getArea().getNumCivCities();
		// No longer includes Barbarian cities
		int const iCivCities = kGame.getNumCivCities();
		int const iCivs = kGame.countCivPlayersAlive();
		scaled rCitiesPerCiv(iCivCities, iCivs);
		/*	Don't want an isolated human to deliberately curb Barbarian activity
			by expanding slowly */
		if (iCivsInArea > 1)
			rCitiesPerCiv = scaled(iCivCitiesInArea, iCivsInArea);
		else rCitiesPerCiv.mulDiv(9, 11);
		scaled const rAggressionRoll = scaled::hash(AI_getBirthmark());
		// </advc.300>
		if (kGame.isOption(GAMEOPTION_RAGING_BARBARIANS) &&
			/*	advc.300: Don't rage right away. (Don't recall why I had originally
				only wanted this on slower game speed.) */
			(//GC.getInfo(kGame.getGameSpeedType()).getBarbPercent() < 125 ||
			rAggressionRoll < barbarianAggressionChance(rCitiesPerCiv, 2)))
		{
			if (AI_pillageRange(4))
			{
				return;
			}

			if (AI_cityAttack(3, 10))
			{
				return;
			}

			if (getArea().getAreaAIType(getTeam()) == AREAAI_OFFENSIVE)
			{
				// BETTER_BTS_AI_MOD, Barbarian AI, 05/15/10, jdog5000: START
				if (AI_groupMergeRange(UNITAI_ATTACK, 1, true, true, true))
				{
					return;
				}

				if (AI_groupMergeRange(UNITAI_ATTACK_CITY, 3, true, true, true))
				{
					return;
				}

				if (AI_goToTargetCity(MOVE_ATTACK_STACK, 12))
				{
					return;
				}
				// BETTER_BTS_AI_MOD: END
			}
		}
		else if (//iCivCities > iCivs * 3
			// <advc.300>
			rAggressionRoll < barbarianAggressionChance(rCitiesPerCiv,
			kGame.isOption(GAMEOPTION_RAGING_BARBARIANS) ? fixp(1.6) : 3)) // </advc.300>
		{
			if (AI_cityAttack(1, 15))
			{
				return;
			}

			if (AI_pillageRange(3))
			{
				return;
			}

			if (AI_cityAttack(2, 10))
			{
				return;
			}

			if (getArea().getAreaAIType(getTeam()) == AREAAI_OFFENSIVE)
			{
				// BETTER_BTS_AI_MOD, Barbarian AI, 05/15/10, jdog5000: START
				if (AI_groupMergeRange(UNITAI_ATTACK, 1, true, true, true))
				{
					return;
				}

				if (AI_groupMergeRange(UNITAI_ATTACK_CITY, 3, true, true, true))
				{
					return;
				}

				if (AI_goToTargetCity(MOVE_ATTACK_STACK, 12))
				{
					return;
				}
				// BETTER_BTS_AI_MOD: END
			}
		}
		else if (//iCivCities > iCivs * 2
			// <advc.300>
			rAggressionRoll < barbarianAggressionChance(rCitiesPerCiv,
			kGame.isOption(GAMEOPTION_RAGING_BARBARIANS) ? fixp(1.25) : 2)) // </advc.300>
		{
			if (AI_pillageRange(2))
				return;
			if (AI_cityAttack(1, 10))
				return;
		}
	}

	if (AI_load(UNITAI_ASSAULT_SEA, MISSIONAI_LOAD_ASSAULT, NO_UNITAI, -1, -1, -1, -1, MOVE_SAFE_TERRITORY, 1))
	{
		return;
	}

	if (AI_heal())
	{
		return;
	}

	if (AI_guardCity(false, true, 2))
	{
		return;
	}

	if (AI_patrol())
	{
		return;
	}

	if (AI_retreatToCity())
	{
		return;
	}

	if (AI_safety())
	{
		return;
	}

	getGroup()->pushMission(MISSION_SKIP);
}

// This function has been heavily edited by K-Mod
void CvUnitAI::AI_attackMove()
{
	PROFILE_FUNC();
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner()); // K-Mod
	bool const bDanger = (kOwner.AI_isAnyPlotDanger(getPlot(), 3));
	bool const bLandWar = kOwner.AI_isLandWar(getArea()); // K-Mod

	// K-Mod note. We'll split the group up later if we need to. (bbai group splitting code deleted.)
	FAssert(getGroup()->countNumUnitAIType(UNITAI_ATTACK_CITY) == 0); // K-Mod. (I'm pretty sure this can't happen.)

	// Attack choking units
	// K-Mod (bbai code deleted)
	if (getPlot().getTeam() == getTeam() &&
		(bDanger || getArea().getAreaAIType(getTeam()) != AREAAI_NEUTRAL))
	{
		if (bDanger && getPlot().isCity())
		{
			if (AI_leaveAttack(2, 55, 105))
				return;
		}
		else
		{
			if (AI_defendTerritory(70, NO_MOVEMENT_FLAGS, 2, true))
				return;
		}
	}
	// K-Mod end

	{
		PROFILE("CvUnitAI::AI_attackMove() 1");

		// Guard a city we're in if it needs it
		if (AI_guardCity(true))
		{
			return;
		}

		/* if (!getPlot().isOwned()) {
			// Group with settler after naval drop
			if (AI_groupMergeRange(UNITAI_SETTLE, 2, true, false, false))
				return;
		} */ // disabled by K-Mod. This is redundant.

		if (!getPlot().isOwned() || getPlot().getOwner() == getOwner())
		{
			if (getArea().getCitiesPerPlayer(getOwner()) >
				kOwner.AI_totalAreaUnitAIs(getArea(), UNITAI_CITY_DEFENSE))
			{
				// Defend colonies in new world
				//if (AI_guardCity(true, true, 3))
				// <K-Mod>
				if (getGroup()->getNumUnits() == 1 ?
					AI_guardCityMinDefender(true) :
					AI_guardCity(true, true, 3)) // </K-Mod>
				{
					return;
				}
			}
		}

		if (AI_heal(30, 1))
		{
			return;
		}

		/* bts code (with omniGroup subbed in.)
		if (!bDanger) {
			//if (AI_group(UNITAI_SETTLE, 1, -1, -1, false, false, false, 3, true))
			if (AI_omniGroup(UNITAI_SETTLE, 1, -1, false, 0, 3, true, false))
				return;
			//if (AI_group(UNITAI_SETTLE, 2, -1, -1, false, false, false, 3, true))
			if (AI_omniGroup(UNITAI_SETTLE, 2, -1, false, 0, 3, false, false))
				return;
		}*/
		// K-Mod
		if (AI_omniGroup(UNITAI_SETTLE, 2, -1, false, NO_MOVEMENT_FLAGS,
			3, false, false, false, false, false))
		{
			return;
		} // K-Mod end

		if (AI_guardCityAirlift())
		{
			return;
		}

		if (AI_guardCity(false, true, 1))
		{
			return;
		}

		//join any city attacks in progress
		/*if (getPlot().isOwned() && getPlot().getOwner() != getOwner()) {
			if (AI_groupMergeRange(UNITAI_ATTACK_CITY, 1, true, true))
				return;
		}*/ // BtS
		// K-Mod
		if (isEnemy(getPlot()))
		{
			if (AI_omniGroup(UNITAI_ATTACK_CITY, -1, -1, true, NO_MOVEMENT_FLAGS,
				2, true, false))
			{
				return;
			}
		} // K-Mod end

		AreaAITypes eAreaAIType = getArea().getAreaAIType(getTeam());
		if (getPlot().isCity() &&
			getPlot().getTeam() == getTeam()) // cdtw.9
		{
			if (eAreaAIType == AREAAI_ASSAULT || eAreaAIType == AREAAI_ASSAULT_ASSIST)
			{
				if (AI_offensiveAirlift())
				{
					return;
				}
			}
		}

		if (bDanger)
		{
			// K-Mod
			if (getGroup()->getNumUnits() > 1 &&
				AI_stackVsStack(3, 110, 65, NO_MOVEMENT_FLAGS))
			{
				return;
			} // K-Mod end

			/*if (AI_cityAttack(1, 55))
				return;
			if (AI_anyAttack(1, 65))
				return;*/ // BtS

			if (collateralDamage() > 0)
			{
				if (AI_anyAttack(1, 45, NO_MOVEMENT_FLAGS, 3))
				{
					return;
				}
			}
		}
		// K-Mod (moved from below, and replacing the disabled stuff above)
		if (AI_anyAttack(1, 70))
		{
			return;
		}
		// K-Mod end

		if (!noDefensiveBonus())
		{
			if (AI_guardCity(false, false))
			{
				return;
			}
		}

		if (!bDanger)
		{
			if (getPlot().getTeam() == getTeam()) // cdtw.9
			{
				bool bAssault = ((eAreaAIType == AREAAI_ASSAULT) || (eAreaAIType == AREAAI_ASSAULT_MASSING) || (eAreaAIType == AREAAI_ASSAULT_ASSIST));
				if (bAssault)
				{
					if (AI_load(UNITAI_ASSAULT_SEA, MISSIONAI_LOAD_ASSAULT, UNITAI_ATTACK_CITY, -1, -1, -1, -1, MOVE_SAFE_TERRITORY, 4))
					{
						return;
					}
				}

				if (AI_load(UNITAI_SETTLER_SEA, MISSIONAI_LOAD_SETTLER, UNITAI_SETTLE, -1, -1, -1, 1, MOVE_SAFE_TERRITORY, 3))
				{
					return;
				}

				//bool bLandWar = ((eAreaAIType == AREAAI_OFFENSIVE) || (eAreaAIType == AREAAI_DEFENSIVE) || (eAreaAIType == AREAAI_MASSING));
				if (!bLandWar)
				{
					// Fill transports before starting new one, but not just full of our unit ai
					if (AI_load(UNITAI_ASSAULT_SEA, MISSIONAI_LOAD_ASSAULT, NO_UNITAI, 1, -1, -1, 1, MOVE_SAFE_TERRITORY, 4))
					{
						return;
					}

					// Pick new transport which has space for other unit ai types to join
					if (AI_load(UNITAI_ASSAULT_SEA, MISSIONAI_LOAD_ASSAULT, NO_UNITAI, -1, 2, -1, -1, MOVE_SAFE_TERRITORY, 4))
					{
						return;
					}
				}

				if (kOwner.AI_isAnyUnitTargetMissionAI(*this, MISSIONAI_GROUP))
				{
					getGroup()->pushMission(MISSION_SKIP);
					return;
				}
			}
		}

		// Allow larger groups if outside territory
		if (getGroup()->getNumUnits() < 3)
		{
			if (getPlot().isOwned() && GET_TEAM(getTeam()).isAtWar(getPlot().getTeam()))
			{
				//if (AI_groupMergeRange(UNITAI_ATTACK, 1, true, true, true))
				if (AI_omniGroup(UNITAI_ATTACK, 3, -1, false, NO_MOVEMENT_FLAGS,
					1, true, false, true, false, false))
				{
					return;
				}
			}
		}

		if (AI_goody(3))
		{
			return;
		}

		/* moved up
		if (AI_anyAttack(1, 70))
			return;*/
	}

	// doc: Roman Legions
	if (!bDanger)
	{
		if (canBuildRoute())
		{
			if (AI_connectCity())
			{
				return;
			}
		}
	}

	{
		PROFILE("CvUnitAI::AI_attackMove() 2");

		if (bDanger)
		{
			// K-Mod. This block has been rewritten. (original code deleted)

			// slightly more reckless than last time
			if (getGroup()->getNumUnits() > 1 &&
				AI_stackVsStack(3, 90, 40, NO_MOVEMENT_FLAGS))
			{
				return;
			}
			bool bAggressive = (getArea().getAreaAIType(getTeam()) != AREAAI_DEFENSIVE ||
					getGroup()->getNumUnits() > 1 || getPlot().getTeam() != getTeam());

			if (bAggressive && AI_pillageRange(1, 10))
				return;

			if (getPlot().getTeam() == getTeam())
			{
				if (AI_defendTerritory(55, NO_MOVEMENT_FLAGS, 2, true))
				{
					return;
				}
			}
			else if (AI_anyAttack(1, 45))
			{
				return;
			}

			if (bAggressive && AI_pillageRange(3, 10))
			{
				return;
			}

			if (getGroup()->getNumUnits() < 4 && isEnemy(getPlot()))
			{
				if (AI_choke(1))
				{
					return;
				}
			}

			if (bAggressive && AI_anyAttack(3, 40))
				return;
		}

		if (!isEnemy(getPlot()))
		{
			if (AI_heal())
			{
				return;
			}
		}

		//if ((kOwner.AI_getNumAIUnits(UNITAI_CITY_DEFENSE) > 0) || (GET_TEAM(getTeam()).getAtWarCount(true) > 0))
		// <K-Mod>
		if (!getPlot().isCity() ||
			getPlot().plotCount(PUF_isUnitAIType, UNITAI_CITY_DEFENSE, -1, getOwner()) > 0)
			// </K-Mod>
		{
			// BBAI TODO: If we're fast, maybe shadow an attack city stack and pillage off of it

			bool bIgnoreFaster = false;
			if (kOwner.AI_isDoStrategy(AI_STRATEGY_LAND_BLITZ))
			{
				if (getArea().getAreaAIType(getTeam()) != AREAAI_ASSAULT)
				{
					bIgnoreFaster = true;
				}
			}

			//if (AI_group(UNITAI_ATTACK_CITY, 1, 1, -1, bIgnoreFaster, true, true, 5))
			// K-Mod
			bool bAttackCity = (bLandWar &&
					(getArea().getAreaAIType(getTeam()) == AREAAI_OFFENSIVE ||
					(AI_getBirthmark() + GC.getGame().getGameTurn() / 8) % 5 <= 1));
			if (bAttackCity)
			{
				// strong merge strategy
				if (AI_omniGroup(UNITAI_ATTACK_CITY, -1, -1, true, NO_MOVEMENT_FLAGS,
					5, true, getGroup()->getNumUnits() < 2, bIgnoreFaster, false, false))
				{
					return;
				}
			}
			else
			{
				// weak merge strategy
				if (AI_omniGroup(UNITAI_ATTACK_CITY, -1, 2, true, NO_MOVEMENT_FLAGS,
					5, true, false, bIgnoreFaster, false, false))
				{
					return;
				}
			}
			// K-Mod end

			//if (AI_group(UNITAI_ATTACK, 1, 1, -1, true, true, false, 4))
			if (AI_omniGroup(UNITAI_ATTACK, 2, -1, false, NO_MOVEMENT_FLAGS,
				4, true, true, true, true, false))
			{
				return;
			}

			// BBAI TODO: Need group to be fast, need to ignore slower groups
			//if (GET_PLAYER(getOwner()).AI_isDoStrategy(AI_STRATEGY_FASTMOVERS))
			//{
			//	if (AI_group(UNITAI_ATTACK, /*iMaxGroup*/ 4, /*iMaxOwnUnitAI*/ 1, -1, true, false, false, /*iMaxPath*/ 3))
			//	{
			//		return;
			//	}
			//}

			//if (AI_group(UNITAI_ATTACK, 1, 1, -1, true, false, false, 1))
			if (AI_omniGroup(UNITAI_ATTACK, 1, 1, false, NO_MOVEMENT_FLAGS,
				1, true, true, false, false, false))
			{
				return;
			}

			// K-Mod. If we're feeling aggressive, then try to get closer to the enemy.
			if (bAttackCity && getGroup()->getNumUnits() > 1)
			{
				/*  advc.001t (Tbd.?): Maybe check CvSelectionGroupAI::AI_isDeclareWar
					and pass MOVE_DECLARE_WAR if true */
				if (AI_goToTargetCity(NO_MOVEMENT_FLAGS, 12))
					return;
			}
			// K-Mod end
		}

		/*if (getArea().getAreaAIType(getTeam()) == AREAAI_OFFENSIVE) {
			if (getGroup()->getNumUnits() > 1) {
				//if (AI_targetCity())
				if (AI_goToTargetCity(0, 12))
					return;
			}
		}*/ // BtS - disabled by K-Mod. (moved / changed)
		/* BBAI code
		else if (getArea().getAreaAIType(getTeam()) != AREAAI_DEFENSIVE) {
			if (getArea().getCitiesPerPlayer(BARBARIAN_PLAYER) > 0) {
				if (getGroup()->getNumUnits() >= GC.getInfo(GC.getGame().getHandicapType()).getBarbarianInitialDefenders()) {
					if (AI_goToTargetBarbCity(10))
						return;
				}
			}
		} */ // disabled by K-Mod. attack groups are currently limited to 2 units anyway. This test will never pass.

		if (AI_guardCity(false, true, 3))
		{
			return;
		}

		if (kOwner.getNumCities() > 1 && getGroup()->getNumUnits() == 1)
		{
			if (getArea().getAreaAIType(getTeam()) != AREAAI_DEFENSIVE)
			{
				if (getArea().getNumUnrevealedTiles(getTeam()) > 0)
				{
					// doc: only if there is no other explorer
					//if (kOwner.AI_areaMissionAIs(getArea(), MISSIONAI_EXPLORE, getGroup()) <
					//	kOwner.AI_neededExplorers(getArea()) + 1)
					if (kOwner.AI_areaMissionAIs(getArea(), MISSIONAI_EXPLORE, getGroup()) == 0)
					{
						// doc: increase range
						//if (AI_exploreRange(3))
						if (AI_exploreRange(4))
						{
							return;
						}

						// doc: disabled
						/*if (AI_explore())
						{
							return;
						}*/
					}
				}
			}
		}

		//if (AI_protect(35, NO_MOVEMENT_FLAGS, 5))
		if (AI_defendTerritory(45, NO_MOVEMENT_FLAGS, 7)) // K-Mod
		{
			return;
		}

		if (AI_offensiveAirlift())
		{
			return;
		}

		if (!bDanger && getArea().getAreaAIType(getTeam()) != AREAAI_DEFENSIVE)
		{
			if (getPlot().getTeam() == getTeam()) // cdtw.9
			{
				if (AI_load(UNITAI_ASSAULT_SEA, MISSIONAI_LOAD_ASSAULT, NO_UNITAI, 1, -1, -1, 1, MOVE_SAFE_TERRITORY, 4))
				{
					return;
				}

				if (GET_TEAM(getTeam()).getNumWars() > 0 && !AI_getGroup()->AI_isHasPathToAreaEnemyCity())
				{
					if (AI_load(UNITAI_ASSAULT_SEA, MISSIONAI_LOAD_ASSAULT, NO_UNITAI, -1, -1, -1, -1, MOVE_SAFE_TERRITORY, 4))
					{
						return;
					}
				}
			}
		}

		// K-Mod
		if (getGroup()->getNumUnits() >= 4 && getPlot().getTeam() == getTeam())
		{
			CvSelectionGroup* pRemainderGroup=NULL;
			CvSelectionGroup* pSplitGroup = getGroup()->splitGroup(2, 0, &pRemainderGroup);
			if (pSplitGroup != NULL)
				pSplitGroup->pushMission(MISSION_SKIP);
			if (pRemainderGroup != NULL)
			{
				CvSelectionGroupAI& kRemainderGroup = pRemainderGroup->AI(); // advc.003u
				if (kRemainderGroup.AI_isForceSeparate())
					kRemainderGroup.AI_separate();
				else kRemainderGroup.pushMission(MISSION_SKIP);
			}
			return;
		}
		// K-Mod end

		if (AI_defend())
		{
			return;
		}

		if (AI_travelToUpgradeCity())
		{
			return;
		}

		// K-Mod
		if (AI_handleStranded())
			return;
		// K-Mod end

		/* if (!bDanger && !isHuman() && getPlot().isCoastalLand() && kOwner.AI_unitTargetMissionAIs(this, MISSIONAI_PICKUP) > 0) {
			// If no other desirable actions, wait for pickup
			getGroup()->pushMission(MISSION_SKIP);
			return;
		} */ // disabled by K-Mod. We don't need this.

		if (AI_patrol())
		{
			return;
		}

		if (AI_retreatToCity())
		{
			return;
		}

		if (AI_safety())
		{
			return;
		}
	}

	getGroup()->pushMission(MISSION_SKIP);
}


void CvUnitAI::AI_paratrooperMove()
{
	PROFILE_FUNC();

	//bool bHostile = (getPlot().isOwned() && isPotentialEnemy(getPlot().getTeam()));
	// advc: I don't see why we would enter an enemy tile before declaring war
	bool const bHostile = ::atWar(getTeam(), getPlot().getTeam());
	if (!bHostile)
	{
		if (AI_guardCity(true))
		{
			return;
		}

		if (getPlot().getTeam() == getTeam())
		{
			if (getPlot().isCity())
			{
				if (AI_heal(30, 1))
				{
					return;
				}
			}

			//AreaAITypes eAreaAIType = getArea().getAreaAIType(getTeam());
			//bool bLandWar = ((eAreaAIType == AREAAI_OFFENSIVE) || (eAreaAIType == AREAAI_DEFENSIVE) || (eAreaAIType == AREAAI_MASSING));
			bool bLandWar = GET_PLAYER(getOwner()).AI_isLandWar(getArea()); // K-Mod
			if (!bLandWar)
			{
				if (AI_load(UNITAI_ASSAULT_SEA, MISSIONAI_LOAD_ASSAULT, NO_UNITAI,
					-1, -1, -1, 0, MOVE_SAFE_TERRITORY, 4))
				{
					return;
				}
			}
		}

		if (AI_guardCity(false, true, 1))
		{
			return;
		}
	}

	if (AI_cityAttack(1, 45))
	{
		return;
	}

	if (AI_anyAttack(1, 55))
	{
		return;
	}

	if (!bHostile)
	{
		if (AI_paradrop(getDropRange()))
		{
			return;
		}

		if (AI_offensiveAirlift())
		{
			return;
		}

		if (AI_moveToStagingCity())
		{
			return;
		}

		if (AI_guardFort(true))
		{
			return;
		}

		if (AI_guardCityAirlift())
		{
			return;
		}
	}
	/*if (collateralDamage() > 0) {
		if (AI_anyAttack(1, 45, 0, 3))
			return;
	}*/ // disabled by K-Mod. (redundant)
	if (AI_pillageRange(1, 15))
	{
		return;
	}

	if (bHostile)
	{
		if (AI_choke(1))
		{
			return;
		}
	}

	if (AI_heal())
	{
		return;
	}

	if (AI_retreatToCity())
	{
		return;
	}

	if (AI_defendTerritory(55, NO_MOVEMENT_FLAGS, 5)) // K-Mod
	{
		return;
	}
	// K-Mod
	if (AI_handleStranded())
		return;
	// K-Mod end
	if (AI_safety())
	{
		return;
	}

	getGroup()->pushMission(MISSION_SKIP);
}

// This function has been heavily edited by K-Mod and by BBAI
void CvUnitAI::AI_attackCityMove()
{
	PROFILE_FUNC();

	AreaAITypes const eAreaAI = getArea().getAreaAIType(getTeam());
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner()); // K-Mod
	//bool bLandWar = !isBarbarian() && ((eAreaAIType == AREAAI_OFFENSIVE) || (eAreaAIType == AREAAI_DEFENSIVE) || (eAreaAIType == AREAAI_MASSING));
	bool const bLandWar = (isBarbarian() ?
			// advc: moved up
			(getArea().getNumCities() > getArea().getCitiesPerPlayer(BARBARIAN_PLAYER)) :
			kOwner.AI_isLandWar(getArea())); // K-Mod
	bool const bAssault = !isBarbarian() && (eAreaAI == AREAAI_ASSAULT ||
			eAreaAI == AREAAI_ASSAULT_ASSIST || eAreaAI == AREAAI_ASSAULT_MASSING);
	bool const bTurtle = kOwner.AI_isDoStrategy(AI_STRATEGY_TURTLE);
	bool const bAlert1 = kOwner.AI_isDoStrategy(AI_STRATEGY_ALERT1);
	bool const bIgnoreFaster = (kOwner.AI_isDoStrategy(AI_STRATEGY_LAND_BLITZ) &&
			!bAssault && getArea().getCitiesPerPlayer(getOwner()) > 0);
	bool const bInCity = getPlot().isCity();

	if (bInCity && /* cdtw.9: */ getPlot().getTeam() == getTeam())
	{
		// force heal if we in our own city and damaged
		/*if (getGroup()->getNumUnits() == 1 && getDamage() > 0) {
			getGroup()->pushMission(MISSION_HEAL);
			return;
		}*/ // <advc.299>
		if (AI_singleUnitHeal(0, 0))
			return; // </advc.299>
		// <advc.114e> (from MNAI)
		if (AI_leaveAttack(1, 70, 150))
			return; // </advc.114e>
		/*if (bIgnoreFaster) {
			// BBAI TODO: split out slow units ... will need to test to make sure this doesn't cause loops
		}*/
		if ((GC.getGame().getGameTurn() - getPlot().getPlotCity()->getGameTurnAcquired()) <= 1 &&
			// cdtw.9: (comment from Dave_uk) only do this in our own cities though
			getPlot().getOwner() == getOwner())
		{
			CvSelectionGroupAI* pOldGroup = AI_getGroup();
			pOldGroup->AI_separateNonAI(UNITAI_ATTACK_CITY);
			if (pOldGroup != getGroup())
				return;
		}
		// note. this will eject a unit to defend the city rather than using the whole group
		if (AI_guardCity(false))
			return;
		//if ((eAreaAIType == AREAAI_ASSAULT) || (eAreaAIType == AREAAI_ASSAULT_ASSIST))
		if (bAssault) // K-Mod
		{
			if (AI_offensiveAirlift())
				return;
		}
	}

	bool const bEnemyTerritory = isEnemy(getPlot()); // advc: renamed from "bAtWar"

	bool bHuntBarbs = false;
	ListEnumMap<PlayerTypes, bool> bHuntPlayer;
	bool bReadyToAttack = false;

	if (isBarbarian())
		bReadyToAttack = (getGroup()->getNumUnits() >= 3);
	// <advc.300>
	else if (!bTurtle)
	{
		int const iGroupSz = getGroup()->getNumUnits();
		int iBarbarianGarrison = kOwner.AI_estimateBarbarianGarrisonSize();
		if ((eAreaAI != AREAAI_DEFENSIVE && eAreaAI != AREAAI_OFFENSIVE && !bAlert1) ||
			iBarbarianGarrison < 2 * kOwner.AI_getCurrEraFactor())
		{
			bHuntBarbs = true;
		}

		// doc: select minor targets dynamically
		bool bHuntMinors = bHuntBarbs;
		if ((area()->getAreaAIType(getTeam()) != AREAAI_OFFENSIVE && area()->getAreaAIType(getTeam()) != AREAAI_DEFENSIVE) || !GET_TEAM(getTeam()).isAtWarWithMajorPlayer())
		{
			for (PlayerIter<CIV_ALIVE> it; it.hasNext(); ++it)
			{
				if (!it->isIndependent() && !it->isNative())
					continue;
				if (area()->getCitiesPerPlayer(it->getID()) == 0)
					continue;

				bHuntPlayer.set(it->getID(), true);
				if (it->isNative())
					bHuntMinors = true;
			}
		}

		//bReadyToAttack = (iGroupSz >= (bHuntBarbs ? 3 : AI_stackOfDoomExtra())); // BtS
		/*  Don't yet know if we'll actually target a Barbarian city, so it's hard to
			decide on the proper size of the attack stack. But if there is nothing else
			to attack, it's easy. */
		bool bHuntOnlyMinors = (bHuntMinors &&
				!GET_TEAM(getTeam()).AI_isSneakAttackReady() &&
				GET_TEAM(getTeam()).getNumWars() <= 0);
		if (!bHuntOnlyMinors && iGroupSz >= AI_stackOfDoomExtra())
			bReadyToAttack = true;
		else if (bHuntOnlyMinors &&
			iGroupSz >= kOwner.AI_neededCityAttackersVsBarbarians() &&
			// Don't send a giant stack. (Tbd.: Should perhaps split the group up then.)
			iGroupSz < 3 * iBarbarianGarrison)
		{
			bReadyToAttack = true;
		}
	} // </advc.300>

	if (bReadyToAttack)
	{
		/*	Check that stack has units which can capture cities
			(K-Mod, I've edited this section to distinguish between
			'no capture' and 'combat limit < 100') */
		bReadyToAttack = false;
		int iNoCombatLimit = 0;
		int iCityCapture = 0;
		CvSelectionGroup const& kGroup = *getGroup();
		FOR_EACH_UNIT_IN(pLoopUnit, kGroup)
		{
			//if (!pLoopUnit->isOnlyDefensive())
			if (pLoopUnit->canAttack() && // K-Mod
				!pLoopUnit->getUnitInfo().isMostlyDefensive()) // advc.315
			{
				if (!pLoopUnit->isNoCityCapture())
					iCityCapture++;
				if (pLoopUnit->combatLimit() >= 100)
					iNoCombatLimit++;
				//if (iCityCapture > 5 || 3 * iCityCapture > kGroup.getNumUnits())
				if ((iCityCapture >= 3 || 2 * iCityCapture > kGroup.getNumUnits()) &&
					(iNoCombatLimit >= 6 || 3 * iNoCombatLimit > kGroup.getNumUnits()))
				{
					bReadyToAttack = true;
					break;
				}
			}
		}
	}

	/*	K-Mod. Try to be consistent in our usage of move flags,
		so that we don't cause unnecessary pathfinder resets.
		advc (note): There are a couple of exceptions where NO_MOVEMENT_FLAGS
		is used. I guess this was done on purpose(?). */
	MovementFlags const eMoveFlags = (MOVE_AVOID_ENEMY_WEIGHT_2 |
			(bReadyToAttack ? MOVE_ATTACK_STACK | MOVE_DECLARE_WAR : NO_MOVEMENT_FLAGS));

	// K-Mod. Barbarian stacks should be reckless and unpredictable.
	if (isBarbarian())
	{
		int iThreshold = SyncRandNum(150) + 20;
		if (AI_stackVsStack(1, iThreshold, 0, eMoveFlags))
			return;
	}

	//if (AI_groupMergeRange(UNITAI_ATTACK_CITY, 0, true, true, bIgnoreFaster))
	if (AI_omniGroup(UNITAI_ATTACK_CITY, -1, -1, true, eMoveFlags,
		0, true, false, bIgnoreFaster))
	{
		return;
	}

	CvCity* pTargetCity = NULL;
	if (isBarbarian())
		pTargetCity = AI_pickTargetCity(eMoveFlags, 10); // was 12 (K-Mod)
	else
	{
		//pTargetCity = AI_pickTargetCity(eMoveFlags, MAX_INT, bHuntBarbs);
		/*	K-Mod. Try to avoid picking a target city in cases where we
			clearly aren't ready. (just for efficiency.) */
		if (bReadyToAttack || bEnemyTerritory ||
			(!bInCity && getGroup()->getNumUnits() > 1))
		{
			pTargetCity = AI_pickTargetCity(eMoveFlags, MAX_INT, bHuntBarbs, bHuntPlayer); // TODO: extend API
		}
	}

	/*	K-Mod. This is used to prevent the AI from oscillating
		between moving to attack moving to pillage. */
	bool bTargetTooStrong = false;
	// advc.114c: Moved up. Target strength ratio for city attack.
	int iAttackRatio = -1;

	int iStepDistToTarget = MAX_INT;
	// K-Mod note.: I've rearranged some parts of the code below, sometimes without comment.
	if (pTargetCity != NULL)
	{
		int iComparePostBombard =
				/*	advc.159: Avoid overflow when applying the modifier below.
					Will only get compared with attack ratio percentages, which
					should be 3-digit numbers. So 10k is a huge ceiling. */
				std::min(10000,
				AI_getGroup()->AI_compareStacks(pTargetCity->plot(), true));
		int iBombardTurns = AI_getGroup()->AI_getBombardTurns(pTargetCity);
		// K-Mod note: AI_compareStacks will try to use the AI memory if it can't see.
		{
			// K-Mod
			/*	The defense modifier is counted in AI_compareStacks.
				So if we add it again, we'd be double counting.
				I'm going to subtract defence, but unfortunately this will
				reduce based on the total rather than the base. */
			int iDefenseModifier = pTargetCity->getDefenseModifier(false);
			int iReducedModifier = iDefenseModifier;
			iReducedModifier *= std::min(20, iBombardTurns);
			iReducedModifier /= 20;
			int iBase = 210;
			if (pTargetCity->getPlot().isHills())
				iBase += GC.getDefineINT(CvGlobals::HILLS_EXTRA_DEFENSE);
			iComparePostBombard *= iBase;
			iComparePostBombard /= std::max(1,
					// def. mod. < 200. I promise.
					iBase + iReducedModifier - iDefenseModifier);
			/*	iBase > 100 is to offset the over-reduction from compounding.
				With iBase == 200, bombarding a defence bonus of 100% will
				reduce effective defence by 50% */
		}

		iAttackRatio = GC.getDefineINT(CvGlobals::BBAI_ATTACK_CITY_STACK_RATIO);
		int iAttackRatioSkipBombard = GC.getDefineINT(CvGlobals::BBAI_SKIP_BOMBARD_MIN_STACK_RATIO);
		iStepDistToTarget = stepDistance(pTargetCity->plot(), plot());
		// K-Mod - I'm going to scale the attack ratio based on our war strategy
		if (isBarbarian())
			iAttackRatio = 80;
		else
		{
			int iAdjustment = 5;
			int iExtraAdjustBombard = 0; // advc.114c
			if (GET_TEAM(getTeam()).AI_getWarPlan(pTargetCity->getTeam()) == WARPLAN_LIMITED)
			{
				iAdjustment += 10;
				/*	advc.114c: Shouldn't be too unwilling to sacrifice siege units
					when fighting a limited war. Not crucial to conquer more. */
				iExtraAdjustBombard -= 5;
			}
			if (kOwner.AI_isDoStrategy(AI_STRATEGY_CRUSH))
				iAdjustment -= 10;
			if (iAdjustment >= 0 && pTargetCity == getArea().AI_getTargetCity(getOwner()))
				iAdjustment -= 10;
			iAdjustment += range(
					(GET_TEAM(getTeam()).AI_getEnemyPowerPercent(true) - 100) / 12,
					-10, 0);
			if (iStepDistToTarget <= 1 && pTargetCity->isOccupation())
				iAdjustment += range(111 - (iAttackRatio + iAdjustment), -10, 0); // k146
			iAttackRatio += iAdjustment;
			iAttackRatioSkipBombard += iAdjustment + /* advc.114c: */ iExtraAdjustBombard;
			FAssert(iAttackRatioSkipBombard >= iAttackRatio);
			FAssert(iAttackRatio >= 100);
		} // K-Mod end

		bTargetTooStrong = (iComparePostBombard < iAttackRatio);
		if (iStepDistToTarget <= 2)
		{	// K-Mod. I've rearranged and rewritten most of this block - removing the bbai code.

			if (bTargetTooStrong)
			{
				if (AI_stackVsStack(2, iAttackRatio, 80, eMoveFlags))
					return;

				FAssert(getDomainType() == DOMAIN_LAND);
				int iOurOffense = kOwner.AI_localAttackStrength(
						plot(), getTeam(), DOMAIN_LAND, 1, false);
				int iEnemyOffense = kOwner.AI_localAttackStrength(
						plot(), NO_TEAM, DOMAIN_LAND, 2, false);

				// If in danger, seek defensive ground
				if (4 * iOurOffense < 3 * iEnemyOffense)
				{
					// including smaller groups
					if (AI_omniGroup(UNITAI_ATTACK_CITY, -1, -1, true, eMoveFlags,
						3, true, false, bIgnoreFaster, false, /*bBiggerOnly=*/false))
					{
						return;
					}
					if (iAttackRatio > 2 * iComparePostBombard &&
						4 * iEnemyOffense > 5 * kOwner.AI_localDefenceStrength(plot(), getTeam()))
					{
						/*	we don't have anywhere near enough attack power,
							and we are in serious danger.
							unfortunately, if we are "bReadyToAttack", we'll probably end up
							coming straight back here... */
						if (!bReadyToAttack && AI_retreatToCity())
							return;
					}
					if (AI_getGroup()->AI_getMissionAIType() == MISSIONAI_PILLAGE &&
						AI_plotDefense() > 0) // advc.012
						//getPlot().defenseModifier(getTeam(), false) > 0)
					{
						if (isEnemy(getPlot()) && canPillage(getPlot()))
						{
							getGroup()->pushMission(MISSION_PILLAGE, -1, -1, NO_MOVEMENT_FLAGS,
									false, false, MISSIONAI_PILLAGE, plot());
							return;
						}
					}
					if (AI_choke(2, true, eMoveFlags))
						return;
				}
				else
				{
					if (AI_omniGroup(UNITAI_ATTACK_CITY, -1, -1, true, eMoveFlags,
						3, true, false, bIgnoreFaster)) // bigger groups only
					{
						return;
					}
					if (canBombard(getPlot()))
					{
						getGroup()->pushMission(MISSION_BOMBARD, -1, -1, NO_MOVEMENT_FLAGS,
								false, false, MISSIONAI_ASSAULT, pTargetCity->plot());
						return;
					}

					if (AI_omniGroup(UNITAI_ATTACK_CITY, -1, -1, true, eMoveFlags, 3,
						true, false, bIgnoreFaster, false, /*bBiggerOnly=*/false)) // any size
					{
						return;
					}
				}
			}

			if (iStepDistToTarget == 1)
			{
				/*	Consider getting into a better position for attack.
					only if we don't already have overwhelming force */
				if (iComparePostBombard < GC.getDefineINT(
					CvGlobals::BBAI_SKIP_BOMBARD_BASE_STACK_RATIO) &&
					(iComparePostBombard < iAttackRatioSkipBombard ||
					2 * pTargetCity->getDefenseDamage() < GC.getMAX_CITY_DEFENSE_DAMAGE() ||
					getPlot().isRiverCrossing(directionXY(getPlot(), pTargetCity->getPlot()))))
				{
					/*	Only move into attack position if we have a chance.
						Without this check, the AI can get stuck alternating
						between this, and pillage.
						I've tried to roughly take into account how much our ratio
						would improve by removing a river penalty. */
					if ((getGroup()->canBombard(getPlot()) && iBombardTurns > 2) ||
						(getPlot().isRiverCrossing(directionXY(getPlot(), pTargetCity->getPlot())) &&
						150 * iComparePostBombard >=
						(150 + GC.getDefineINT(CvGlobals::RIVER_ATTACK_MODIFIER)) * iAttackRatio))
					{
						if (AI_goToTargetCity(eMoveFlags, 2, pTargetCity))
							return;
					}
					// Note: bombard may skip if stack is powerful enough
					if (AI_bombardCity())
						return;
				}
				// we're satisfied with our position already. But we still want to consider bombarding.
				else if (iComparePostBombard >= iAttackRatio && AI_bombardCity())
					return;

				if (iComparePostBombard >= iAttackRatio)
				{
					// in position; and no desire to bombard.  So attack!
					if (AI_stackAttackCity(iAttackRatio))
						return;
				}
			}

			if (iComparePostBombard >= iAttackRatio &&
				AI_goToTargetCity(eMoveFlags, 4, pTargetCity))
			{
				return;
			}
		}
	}

	/*	K-Mod. Lets have some slightly smarter stack vs. stack AI.
		it would be nice to have some personality effection here...
		eg. protective leaders have a lower risk threshold.   -- Maybe later.
		Note. This stackVsStack stuff used to be a bit lower,
		after the group and the heal stuff. */
	if (getGroup()->getNumUnits() > 1)
	{
		if (bEnemyTerritory)
		{
			// note. if we are 2 steps from the target city, this check here is redundant. (see code above)
			if (AI_stackVsStack(1, 160, 95, eMoveFlags))
				return;
		}
		else
		{
			int const iSearchRange = 4;
			if (eAreaAI == AREAAI_DEFENSIVE && getPlot().getOwner() == getOwner())
			{
				if (AI_stackVsStack(iSearchRange, 110, 55, eMoveFlags))
					return;
				if (AI_stackVsStack(iSearchRange, 180, 30, eMoveFlags))
					return;
			}
			else if (AI_stackVsStack(iSearchRange, 130, 60, eMoveFlags))
				return;
		}
	}

	/*  K-Mod. The loading of units for assault needs to be before the following
		omnigroup - otherwise the units may leave the boat to join their friends. */
	if (bAssault && (pTargetCity == NULL || !pTargetCity->isArea(getArea())))
	{
		if (AI_load(UNITAI_ASSAULT_SEA, MISSIONAI_LOAD_ASSAULT, NO_UNITAI,
			-1, -1, -1, -1, eMoveFlags, /*iMaxPath=*/6)) // was 4
		{
			return;
		}
	} // K-Mod end
	{
		int iMaxGroupPath = 2;
		/*	<advc.083> Increase the range for joining another group when
			getting ready to attack takes long. Might be that everyone else
			is gathering at a different staging city. */
		if (getPlot().isCity() && GET_TEAM(getTeam()).AI_isAnyChosenWar() &&
			!isBarbarian() &&
			(eAreaAI == AREAAI_OFFENSIVE || eAreaAI == AREAAI_MASSING))
		{
			int iMaxWPAge = 0;
			for (TeamIter<MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> itEnemy(getTeam());
				itEnemy.hasNext(); ++itEnemy)
			{
				iMaxWPAge = std::max(iMaxWPAge,
						GET_TEAM(getTeam()).AI_getWarPlanStateCounter(itEnemy->getID()));
			}
			if (iMaxWPAge > 0)
			{
				/*	I think we want to check this periodically, not totally
					at random. */
				int iIntervalRand = (scaled::hash(getGroup()->getID(), getOwner()) * 5).
						floor();
				if (iMaxWPAge % (iIntervalRand + 8) == 0)
					iMaxGroupPath += 1 + SyncRandNum(3);
			}
		} // </advc.083>
		//if (AI_groupMergeRange(UNITAI_ATTACK_CITY, iMaxGroupPath, true, true, bIgnoreFaster))
		if (AI_omniGroup(UNITAI_ATTACK_CITY, -1, -1, true, eMoveFlags, iMaxGroupPath,
			true, false, bIgnoreFaster))
		{
			return;
		}
	}
	if (AI_heal(30, 1))
		return;

	/*if (collateralDamage() > 0 && getPlot().getOwner() == getOwner()) {
		if (AI_anyAttack(1, 45, eMoveFlags, 3, false, false))
			return;
		if (!bReadyToAttack) {
			if (AI_anyAttack(1, 25, eMoveFlags, 5, false))
				return;
		}
	}*/ // BtS

	//if (AI_anyAttack(1, 60, eMoveFlags, 0, false))
	/*	K-Mod (changed to allow cities, and to only use a single unit,
		but it is still a questionable move) */
	if (AI_anyAttack(1, 60, eMoveFlags | MOVE_SINGLE_ATTACK))
		return;

	// K-Mod - replacing some stuff I moved / removed from the BBAI code
	if (pTargetCity != NULL && bTargetTooStrong &&
		iStepDistToTarget <= (bReadyToAttack ? 3 : 2))
	{
		/*	<advc.114c> Attrition warfare is miserable for both sides,
			rather take our chances if they're not terrible. */
		if (getGroup()->getNumUnits() > 3 + kOwner.AI_getCurrEraFactor() / 2 &&
			iAttackRatio > 100)
		{
			if (AI_stackAttackCity((iAttackRatio + 100) / 2))
				return;
		} // </advc.114c>
		// Pillage around enemy city
		if (generatePath(pTargetCity->getPlot(), eMoveFlags, true, 0, 5))
		{
			/*	the above path check is just for efficiency.
				Otherwise we'd be checking every surrounding tile. */
			if (AI_pillageAroundCity(pTargetCity, 11, eMoveFlags, 2)) // was 3 turns
				return;

			if (AI_pillageAroundCity(pTargetCity, 0, eMoveFlags, 4)) // was 5 turns
				return;
		}
		// choke the city.
		if (iStepDistToTarget <= 2 && AI_choke(1, false, eMoveFlags))
			return;
		/*	if we're already standing right next to the city, then goToTargetCity can fail
			- and we might end up doing something stupid instead. So try again to choke. */
		if (iStepDistToTarget <= 1 && AI_choke(3, false, eMoveFlags))
			return;
	}

	/*	one more thing. Sometimes a single step can cause the AI to change its target city;
		and when it changes the target - and so sometimes they can get stuck in a loop where
		they step towards their target, change their mind, step back to pillage something, ...
		Here I've made a kludge to break that cycle: */
	if (AI_getGroup()->AI_getMissionAIType() == MISSIONAI_PILLAGE)
	{
		CvPlot* pMissionPlot = AI_getGroup()->AI_getMissionAIPlot();
		if (pMissionPlot != NULL && canPillage(*pMissionPlot) &&
			isEnemy(*pMissionPlot))
		{
			if (at(*pMissionPlot))
			{
				getGroup()->pushMission(MISSION_PILLAGE, -1, -1, NO_MOVEMENT_FLAGS,
						false, false, MISSIONAI_PILLAGE, pMissionPlot);
				return;
			}
			if (generatePath(*pMissionPlot, eMoveFlags, true, 0, 6))
			{
				/*  the max path turns is arbitrary, but it should be at least as
					big as the pillage sections higher up. */
				CvPlot& kEndTurnPlot = getPathEndTurnPlot();
				// warning: this command may attack something. We haven't checked!
				pushGroupMoveTo(kEndTurnPlot, eMoveFlags, false, false,
						MISSIONAI_PILLAGE, pMissionPlot);
				return;
			}
		}
	}
	// K-Mod end

	if (bEnemyTerritory && (bTargetTooStrong || getGroup()->getNumUnits() <= 2))
	{
		if (AI_pillageRange(3, 11, eMoveFlags))
			return;
		if (AI_pillageRange(1, 0, eMoveFlags))
			return;
	}

	if (getPlot().getOwner() == getOwner())
	{
		/*if (!bLandWar) {
			if (AI_load(UNITAI_ASSAULT_SEA, MISSIONAI_LOAD_ASSAULT, NO_UNITAI, -1, -1, -1, -1, eMoveFlags, 4))
				return;
		}*/ // BtS - K-Mod: I've moved this to be above the omniGroup stuff, otherwise it just causes AI confusion.

		if (bReadyToAttack)
		{
			// Wait for units about to join our group
			/*MissionAITypes eMissionAIType = MISSIONAI_GROUP;
			int iJoiners = kOwner.AI_unitTargetMissionAIs(this, &eMissionAIType, 1, getGroup(), 2);
			if (iJoiners * 5 > getGroup()->getNumUnits()) {
				getGroup()->pushMission(MISSION_SKIP);
				return;
			}*/ // BBAI
			// K-Mod. If the target city is close, be less likely to wait for backup.
			int iPathTurns = 10;
			int iMaxWaitTurns = 3;
			if (pTargetCity != NULL &&
				generatePath(pTargetCity->getPlot(), eMoveFlags, true,
				&iPathTurns, iPathTurns))
			{
				iMaxWaitTurns = (iPathTurns+1) / 3;
			}
			MissionAITypes eMissionAIType = MISSIONAI_GROUP;
			int iJoiners = (iMaxWaitTurns > 0 ? kOwner.AI_unitTargetMissionAIs(
					*this, &eMissionAIType, 1, getGroup(), iMaxWaitTurns) : 0);

			if (iJoiners * range(iPathTurns-1, 2, 5) > getGroup()->getNumUnits())
			{	// (the mission is just for debug feedback)
				getGroup()->pushMission(MISSION_SKIP, -1, -1, NO_MOVEMENT_FLAGS,
						false, false, MISSIONAI_GROUP);
				return;
			}
			// K-Mod end
		}
		else
		{
			if (bTurtle)
			{
				// K-Mod
				if (AI_leaveAttack(1, 51, 100))
					return;
				if (AI_defendTerritory(70, eMoveFlags, 3))
					return;
				// K-Mod end
				if (AI_guardCity(false, true, 7, eMoveFlags))
					return;
			}
			else if (!isBarbarian() && eAreaAI == AREAAI_DEFENSIVE)
			{
				// Use smaller attack city stacks on defense
				// K-Mod
				if (AI_defendTerritory(65, eMoveFlags, 3))
					return;
				// K-Mod end
				if (AI_guardCity(false, true, 3, eMoveFlags))
					return;
			}

			int iTargetCount = kOwner.AI_unitTargetMissionAIs(*this, MISSIONAI_GROUP);
			if (iTargetCount * 5 > getGroup()->getNumUnits())
			{
				MissionAITypes eMissionAIType = MISSIONAI_GROUP;
				int iJoiners = kOwner.AI_unitTargetMissionAIs(
						*this, &eMissionAIType, 1, getGroup(), 2);
				if (iJoiners * 5 > getGroup()->getNumUnits())
				{	// K-Mod (for debug feedback)
					getGroup()->pushMission(MISSION_SKIP, -1, -1, NO_MOVEMENT_FLAGS,
							false, false, MISSIONAI_GROUP);
					return;
				}
				if (AI_moveToStagingCity())
					return;
			}
		}
	}

	if (AI_heal(50, 3))
		return;

	if (!bEnemyTerritory)
	{
		if (AI_heal())
			return;
		if (getGroup()->getNumUnits() == 1 && getTeam() != getPlot().getTeam())
		{
			if (AI_retreatToCity())
				return;
		}
	}

	if (!bReadyToAttack && !noDefensiveBonus())
	{
		if (AI_guardCity(false, false, MAX_INT, eMoveFlags))
			return;
	}

	if (bReadyToAttack /* advc.083: */ && !bTargetTooStrong)
	{	// advc.opt: Moved into the bReadyToAttack branch
		bool bAnyWarPlan = GET_TEAM(getTeam()).AI_isAnyWarPlan();
		/* BBAI code
		if (isBarbarian()) {
			if (AI_goToTargetCity(eMoveFlags, 12))
				return;
			if (AI_pillageRange(3, 11, eMoveFlags))
				return;
			if (AI_pillageRange(1, 0, eMoveFlags))
				return;
		}
		else if (bHuntBarbs && AI_goToTargetBarbCity((bAnyWarPlan ? 7 : 12)))
			return;
		else if (bLandWar && pTargetCity != NULL)*/
		// K-Mod
		if (isBarbarian())
		{
			// target city has already been calculated.
			if (pTargetCity != NULL && AI_goToTargetCity(eMoveFlags, 12, pTargetCity))
				return;
			// <advc.300>
			int iSearchRange = 3;
			if (getArea().getAreaAIType(getTeam()) == AREAAI_ASSAULT)
				iSearchRange = 1; // </advc.300>
			if (AI_pillageRange(iSearchRange, 0, eMoveFlags))
				return;
		}
		else if (pTargetCity != NULL)
		// K-Mod end
		{
			// Before heading out, check whether to wait to allow unit upgrades
			if (bInCity && getPlot().getOwner() == getOwner() &&
				//!GET_PLAYER(getOwner()).AI_isFinancialTrouble()
				!kOwner.AI_isFinancialTrouble() && !pTargetCity->isBarbarian())
			{
				// Check if stack has units which can upgrade
				int iNeedUpgradeCount = 0;
				CvSelectionGroup const& kGroup = *getGroup();
				FOR_EACH_UNIT_IN(pLoopUnit, kGroup)
				{
					if (pLoopUnit->getUpgradeCity(false) == NULL)
						continue;
					iNeedUpgradeCount++;
					if (5 * iNeedUpgradeCount > kGroup.getNumUnits()) // was 8*
					{
						getGroup()->pushMission(MISSION_SKIP);
						return;
					}
				}
			}

			// K-Mod. (original bloated code deleted)
			// Estimate the number of turns required.
			int iPathTurns;
			if (!generatePath(pTargetCity->getPlot(), eMoveFlags, true, &iPathTurns))
			{	// AI_pickTargetCity now allows boat-only paths, so this assertion no longer holds.
				//FErrorMsg("failed to find path to target city.");
				iPathTurns = 100;
			}
			if (!pTargetCity->isBarbarian() ||
				// don't bother with long-distance barb attacks
				iPathTurns < (bAnyWarPlan ? 7 : 12))
			{
				// See if we can get there faster by boat..
				if (iPathTurns > 5)// && !pTargetCity->isBarbarian())
				{
					/*  note: if the only land path to our target happens to go
						through a tough line of defence...
						we probably want to take the boat even if our iPathTurns is
						low. Here's one way to account for that:
						iPathTurns = std::max(iPathTurns, getPathLastNode()->
						m_iTotalCost / (2000*GC.getMOVE_DENOMINATOR()));
						Unfortunately, that "2000"... well I think you know what the
						problem is. So maybe next time. */
					int iLoadTurns = std::max(3, iPathTurns/3 - 1); // k146
					int iMaxTransportTurns = iPathTurns - iLoadTurns - 2;
					if (AI_load(UNITAI_ASSAULT_SEA, MISSIONAI_LOAD_ASSAULT, NO_UNITAI,
						-1, -1, -1, -1, eMoveFlags, iLoadTurns, iMaxTransportTurns))
					{
						return;
					}
				}
				// We have to walk.
				if (AI_goToTargetCity(eMoveFlags, MAX_INT, pTargetCity))
					return;

				if (bAnyWarPlan)
				{
					/*	advc.083: This can no longer occur. We shouldn't
						"just wait for reinforcements" paying supply costs and
						possibly leaving our own cities exposed. */
				#if 0
					/*	We're at war, but we failed to walk to the target.
						Before we start wigging out, lets just check one more thing... */
					if (bTargetTooStrong && iStepDistToTarget == 1)
					{
						/*	we're standing outside the city already, but we can't capture it
							and we can't pillage or choke it.
							I guess we'll just wait for reinforcements to arrive. */
						if (AI_safety())
							return;
						getGroup()->pushMission(MISSION_SKIP);
						return;
					}
				#endif

					//CvCity* pTargetCity =
					/*  advc: Don't shadow the pTargetCity variable that the rest of
						this function cares about (and which isn't necessarily in this
						unit's area).
						Note: In the code below, only airlifts care about pTargetCity,
						and that'll fail b/c AI_safety has already failed. */
					CvCity* pAreaTargetCity = getArea().AI_getTargetCity(getOwner());
					if (pAreaTargetCity != NULL &&
						!pAreaTargetCity->isMinorCiv()) // doc: do not start wars just to target a minor
					{	/*  advc: One way that this can happen: Owner is at war with a civ that
							it can only reach through the territory of a third party (no OB) and
							is preparing war against the third party.
							AI_pickTargetCity will then pick a city of the current war enemy, but
							the Area AI will be set to a non-ASSAULT type, meaning that AI_attackCityMove
							will (in vain) look for a land path. AI_solveBlockageProblem will then (always?)
							fail, and the unit won't move at all. This is probably for the best -- wait
							until the preparations are through. Difficult to avoid the assertions below. */
						/*  this is a last resort. I don't expect that we'll ever actually need it.
							(it's a pretty ugly function, so I /hope/ we don't need it.) */
						FErrorMsg("AI_attackCityMove is resorting to AI_solveBlockageProblem");
						if (AI_solveBlockageProblem(pAreaTargetCity->plot(),
							(GET_TEAM(getTeam()).getNumWars() <= 0)))
						{
							return;
						}  // advc.006:
						FErrorMsg("AI_solveBlockageProblem returned false");
					}
				}
			}
			// K-Mod end
		}
	}
	else
	{
		/*int iTargetCount = kOwner.AI_unitTargetMissionAIs(this, MISSIONAI_GROUP);
		if (iTargetCount * 4 > getGroup()->getNumUnits() || getGroup()->getNumUnits() + iTargetCount >= (bHuntBarbs ? 3 : AI_stackOfDoomExtra())) {
			MissionAITypes eMissionAIType = MISSIONAI_GROUP;
			int iJoiners = kOwner.AI_unitTargetMissionAIs(this, &eMissionAIType, 1, getGroup(), 2);
			if (6*iJoiners > getGroup()->getNumUnits()) {
				getGroup()->pushMission(MISSION_SKIP);
				return;
			}
			if (AI_safety())
				return;
		}*/ // BtS
		// K-Mod
		int iTargetCount = kOwner.AI_unitTargetMissionAIs(*this, MISSIONAI_GROUP);
		if (6 * iTargetCount > getGroup()->getNumUnits())
		{
			MissionAITypes eMissionAIType = MISSIONAI_GROUP;
			int iNearbyJoiners = kOwner.AI_unitTargetMissionAIs(
					*this, &eMissionAIType, 1, getGroup(), 2);
			if (4*iNearbyJoiners > getGroup()->getNumUnits())
			{
				getGroup()->pushMission(MISSION_SKIP);
				return;
			}
			if (AI_safety())
				return;
		} // K-Mod end

		if (bombardRate() > 0 && noDefensiveBonus())
		{
			/*	BBAI Notes: Add this stack lead by a bombard unit
				to a stack probably not lead by a bombard unit */
			/*	BBAI TODO: Some sense of minimum stack size?
				Can have big stack moving 10 turns to merge with tiny stacks */
			//if (AI_group(UNITAI_ATTACK_CITY, -1, -1, -1, bIgnoreFaster, true, true, /*iMaxPath*/ 10, /*bAllowRegrouping*/ true))
			if (AI_omniGroup(UNITAI_ATTACK_CITY, -1, -1, true, eMoveFlags, 10,
				true, getGroup()->getNumUnits() < 2, bIgnoreFaster, true, true))
			{
				return;
			}
		}
		else
		{
			//if (AI_group(UNITAI_ATTACK_CITY, AI_stackOfDoomExtra() * 2, -1, -1, bIgnoreFaster, true, true, /*iMaxPath*/ 10, /*bAllowRegrouping*/ false))
			if (AI_omniGroup(UNITAI_ATTACK_CITY, AI_stackOfDoomExtra() * 2,
				-1, true, eMoveFlags, 10,
				true, getGroup()->getNumUnits() < 2, bIgnoreFaster, false, true))
			{
				return;
			}
		}
	}

	if (getPlot().getOwner() == getOwner() && bLandWar)
	{
		if (GET_TEAM(getTeam()).getNumWars() > 0)
		{
			// if no land path to enemy cities, try getting there another way
			if (AI_offensiveAirlift())
				return;
			if (pTargetCity == NULL)
			{
				if (AI_load(UNITAI_ASSAULT_SEA, MISSIONAI_LOAD_ASSAULT,
					NO_UNITAI, -1, -1, -1, -1, eMoveFlags, 4))
				{
					return;
				}
			}
		}
	}

	// K-Mod
	if (AI_defendTerritory(70, eMoveFlags, 1, true))
		return;
	// K-Mod end
	// <advc.300> Rather guard cities better than staging in arbitrary places
	if (isBarbarian() && pTargetCity == NULL)
	{
		if (AI_guardCity(false, true, 7, eMoveFlags, 2))
			return;
	} // </advc.300>
	if (AI_moveToStagingCity())
		return;
	if (AI_offensiveAirlift())
		return;
	// doc: Roman Legions
	if (!GET_TEAM(getTeam()).isAtWarWithMajorPlayer())
	{
		if (canBuildRoute())
		{
			if (AI_connectCity())
				return;
			if (AI_routeCity())
				return;
		}
	}
	if (AI_retreatToCity())
		return;
	// K-Mod
	if (AI_handleStranded())
		return;
	// K-Mod end
	if (AI_safety())
		return;
	getGroup()->pushMission(MISSION_SKIP);
}

void CvUnitAI::AI_attackCityLemmingMove()
{
	if (AI_cityAttack(1, 80))
	{
		return;
	}

	if (AI_bombardCity())
	{
		return;
	}

	if (AI_cityAttack(1, 40))
	{
		return;
	}
	// BETTER_BTS_AI_MOD, Unit AI, 03/29/10, jdog5000: was AI_targetCity
	if (AI_goToTargetCity(MOVE_THROUGH_ENEMY))
	{
		return;
	}

	if (AI_anyAttack(1, 70))
	{
		return;
	}

	if (AI_anyAttack(1, 0))
	{
		return;
	}

	getGroup()->pushMission(MISSION_SKIP);
}


void CvUnitAI::AI_collateralMove()
{
	PROFILE_FUNC();

	// K-Mod!
	if (AI_defensiveCollateral(51, 3))
		return;
	// K-Mod end

	if (AI_leaveAttack(1, 30, 100)) // was 20
	{
		return;
	}

	if (AI_guardCity(false, true, 1))
	{
		return;
	}

	if (AI_heal(30, 1))
	{
		return;
	}

	if (AI_cityAttack(1, 35))
	{
		return;
	}

	/*if (AI_anyAttack(1, 45, 0, 3))
		return;*/

	if (AI_anyAttack(1, 55, NO_MOVEMENT_FLAGS, 2))
	{
		return;
	}

	if (AI_anyAttack(1, 35, NO_MOVEMENT_FLAGS, 3))
	{
		return;
	}

	/*if (AI_anyAttack(1, 30, 0, 4))
		return;
	if (AI_anyAttack(1, 20, 5))
		return;*/ // BtS
	// K-Mod
	{
		// count our collateral damage units on this plot
		int iTally = 0;
		FOR_EACH_UNIT_IN(pLoopUnit, getPlot())
		{
			if (DOMAIN_LAND == pLoopUnit->getDomainType() &&
				pLoopUnit->getOwner() == getOwner() &&
				pLoopUnit->canMove() && pLoopUnit->collateralDamage() > 0)
			{
				iTally++;
			}
		}
		FAssert(iTally > 0);
		FAssert(collateralDamageMaxUnits() > 0);

		//int iDangerModifier = 100;
		do
		{
			int iMinOdds = 80 / (3 + iTally);
			/*iMinOdds *= 100;
			iMinOdds /= iDangerModifier;*/ // advc: was always 100 ...
			if (AI_anyAttack(1, iMinOdds, NO_MOVEMENT_FLAGS, std::min(
				2*collateralDamageMaxUnits(), collateralDamageMaxUnits() + iTally - 1)))
			{
				return;
			}
			/*	Try again with just half the units, just in case our only problem is
				that we can't find a big enough target stack. */
			iTally = (iTally - 1) / 2;
		} while (iTally > 1);
	}
	// K-Mod end

	if (AI_heal())
	{
		return;
	}

	/*if (!noDefensiveBonus()) {
		if (AI_guardCity(false, false))
			return;
	}*/ // redundant

	if (AI_anyAttack(2, 55, NO_MOVEMENT_FLAGS, 3))
	{
		return;
	}

	if (AI_cityAttack(2, 50))
	{
		return;
	}

	/*if (AI_anyAttack(2, 60))
		return;*/ // BtS (check again with a stricter threshold -> a waste of time)
	// K-Mod
	if (getArea().getAreaAIType(getTeam()) == AREAAI_OFFENSIVE)
	{
		const CvPlayerAI& kOwner = GET_PLAYER(getOwner());
		// if more than a third of our floating defenders are collateral units, convert this one to city attack
		if (3 * kOwner.AI_totalAreaUnitAIs(getArea(), UNITAI_COLLATERAL) >
			kOwner.AI_getTotalFloatingDefenders(getArea()))
		{
			if (kOwner.AI_unitValue(getUnitType(), UNITAI_ATTACK_CITY, area()) > 0)
			{
				AI_setUnitAIType(UNITAI_ATTACK_CITY);
				return; // no mission pushed.
			}
		}
	} // K-Mod end

	//if (AI_protect(50))
	if (AI_defendTerritory(55, NO_MOVEMENT_FLAGS, 6)) // K-Mod
	{
		return;
	}

	if (AI_guardCity(false, true, 8)) // was 3
	{
		return;
	}

	if (AI_retreatToCity())
	{
		return;
	}

	// K-Mod
	if (AI_handleStranded())
		return;
	// K-Mod end

	if (AI_safety())
	{
		return;
	}

	getGroup()->pushMission(MISSION_SKIP);
}


void CvUnitAI::AI_pillageMove()
{
	PROFILE_FUNC();

	if (AI_guardCity(false, true, 2)) // was 1
	{
		return;
	}

	if (AI_heal(30, 1))
	{
		return;
	}

	// BBAI TODO: Shadow ATTACK_CITY stacks and pillage

	//join any city attacks in progress
	if (getPlot().isOwned() && getPlot().getOwner() != getOwner())
	{
		if (AI_groupMergeRange(UNITAI_ATTACK_CITY, 1, true, true))
		{
			return;
		}
	}

	/*if (AI_cityAttack(1, 55))
		return;*/

	/*	K-Mod. Pillage units should focus on pillaging, when possible.
		note: having 2 moves doesn't necessarily mean we can
		move & pillage in the same turn, but it's a good enough approximation. */
	if (AI_pillageRange(getGroup()->baseMoves() > 1 ? 1 : 0, 11))
	{
		return;
	}
	// K-Mod end

	if (AI_anyAttack(1, 65))
	{
		return;
	}

	if (!noDefensiveBonus())
	{
		if (AI_guardCity(false, false))
		{
			return;
		}
	}

	if (AI_pillageRange(3, 11))
	{
		return;
	}

	if (AI_choke(1))
	{
		return;
	}

	if (AI_pillageRange(1))
	{
		return;
	}

	if (getPlot().getOwner() == getOwner())
	{
		if (AI_load(UNITAI_ASSAULT_SEA, MISSIONAI_LOAD_ASSAULT, UNITAI_ATTACK,
			-1, -1, -1, -1, MOVE_SAFE_TERRITORY, 4))
		{
			return;
		}
	}

	if (AI_heal(50, 3))
	{
		return;
	}

	if (!isEnemy(getPlot()))
	{
		if (AI_heal())
		{
			return;
		}
	}
	/*  K-Mod: iMaxGroup was 1
		(later, I might tell counter units to join up.) */
	if (AI_group(UNITAI_PILLAGE, /*iMaxGroup*/ 2, /*iMaxOwnUnitAI*/ 1, -1,
		/*bIgnoreFaster*/ true, false, false, /*iMaxPath*/ 3))
	{
		return;
	}

	if (getArea().getAreaAIType(getTeam()) == AREAAI_OFFENSIVE || isEnemy(getPlot()))
	{
		if (AI_pillage(20))
		{
			return;
		}
	}

	if (AI_heal())
	{
		return;
	}

	if (AI_guardCity(false, true, 3))
	{
		return;
	}

	if (AI_offensiveAirlift())
	{
		return;
	}

	if (AI_travelToUpgradeCity())
	{
		return;
	}

	if (!isHuman() && getPlot().isCoastalLand() &&
		/*  advc.046: SKIP w/o setting eMissionAI would make the group forget
			that it's stranded, and then AI_pickupStranded won't find it. */
		!AI_getGroup()->AI_isStranded() &&
		GET_PLAYER(getOwner()).AI_isAnyUnitTargetMissionAI(*this, MISSIONAI_PICKUP))
	{
		getGroup()->pushMission(MISSION_SKIP);
		return;
	}

	// K-Mod
	if (getPlot().getTeam() == getTeam() &&
		AI_defendTerritory(55, NO_MOVEMENT_FLAGS, 3, true))
	{
		return;
	}
	if (AI_handleStranded())
		return;
	// K-Mod end

	if (AI_retreatToCity())
	{
		return;
	}
	/*  advc.102: Moved down. Don't generally patrol with pillagers; they're fast
		and therefore extra annoying to watch. */
	if (AI_patrol())
	{
		return;
	}

	if (AI_safety())
	{
		return;
	}

	getGroup()->pushMission(MISSION_SKIP);
}


void CvUnitAI::AI_reserveMove()
{
	PROFILE_FUNC();

	// K-Mod
	if (AI_guardCityOnlyDefender())
		return; // K-Mod end

	bool const bDanger = (GET_PLAYER(getOwner()).AI_isAnyPlotDanger(getPlot(), 3));

	/*if (bDanger && AI_leaveAttack(2, 55, 130))
		return;*/ // BtS
	// K-Mod
	if (getPlot().getTeam() == getTeam() &&
		(bDanger || getArea().getAreaAIType(getTeam()) != AREAAI_NEUTRAL))
	{
		if (bDanger && getPlot().isCity())
		{
			if (AI_leaveAttack(1, 55, 110))
				return;
		}
		else
		{
			if (AI_defendTerritory(65, NO_MOVEMENT_FLAGS, 2, true))
				return;
		}
	}
	else
	{
		if (AI_anyAttack(1, 65))
			return;
	}
	// K-Mod end

	if (getPlot().getOwner() == getOwner())
	{
		if (!noDefensiveBonus() && // advc.040: No Catapults
			AI_load(UNITAI_SETTLER_SEA, MISSIONAI_LOAD_SETTLER, UNITAI_SETTLE,
			-1, -1, 1, -1, MOVE_SAFE_TERRITORY))
		{
			return;
		}
		if (AI_load(UNITAI_SETTLER_SEA, MISSIONAI_LOAD_SETTLER, UNITAI_WORKER,
			-1, -1, 1, -1, MOVE_SAFE_TERRITORY))
		{
			return;
		}
	}

	if (!bDanger || !getPlot().isOwned()) // K-Mod
	{
		if (AI_group(UNITAI_SETTLE, 2, -1, -1, false, false, false, 3, true))
		{
			return;
		}
	}
	// <advc.314> Can be important for huts near colonies
	if(!bDanger && AI_goody(3))
		return; // </advc.314>
	if (AI_guardCity(true))
	{
		return;
	}

	if (!noDefensiveBonus())
	{
		if (AI_guardFort(false))
		{
			return;
		}
	}

	if (AI_guardCityAirlift())
	{
		return;
	}

	if (AI_guardCity(false, true, 2)) // was 1
	{
		return;
	}

	// <advc.300> Protect high-yield tiles from Barbarians
	if(GET_PLAYER(getOwner()).AI_isDefenseFocusOnBarbarians(getArea()) &&
		AI_guardYield())
	{
		return;
	}
	// Moved up. Shouldn't travel to future city site while badly injured.
	if(AI_heal(30, 1))
		return;
	// </advc.300>

	if (AI_guardCitySite())
	{
		return;
	}

	if (!noDefensiveBonus())
	{
		if (AI_guardFort(true))
		{
			return;
		}

		if (AI_guardBonus(15))
		{
			return;
		}
	}

	// advc.300: Moved up
	/*if (AI_heal(30, 1))
		return;*/

	/*if (bDanger) {
		if (AI_cityAttack(1, 55))
			return;
		if (AI_anyAttack(1, 60))
			return;
	}
	if (!noDefensiveBonus()) {
		if (AI_guardCity(false, false))
			return;
	}*/ // disabled by K-Mod. (redundant)

	// doc: Roman Legions
	if (!bDanger)
	{
		if (canBuildRoute())
		{
			if (AI_connectCity())
				return;
			if (AI_routeCity())
				return;
		}
	}

	if (bDanger)
	{
		/*if (AI_cityAttack(3, 45))
			return;*/
		if (AI_anyAttack(3, 50))
		{
			return;
		}
	}

	//if (AI_protect(45))
	if (AI_defendTerritory(45, NO_MOVEMENT_FLAGS, 8)) // K-Mod
	{
		return;
	}

	//if (AI_guardCity(false, true, 3))
	if (AI_guardCity(false, true)) // K-Mod
	{
		return;
	}

	if (AI_defend())
	{
		return;
	}

	if (AI_retreatToCity())
	{
		return;
	}

	// K-Mod
	if (AI_handleStranded())
		return;
	// K-Mod end

	if (AI_safety())
	{
		return;
	}

	getGroup()->pushMission(MISSION_SKIP);
}


void CvUnitAI::AI_counterMove()
{
	PROFILE_FUNC();
	// BETTER_BTS_AI_MOD, Unit AI, Settler AI, 03/03/10, jdog5000: START
	// Should never have group lead by counter unit
	if (getGroup()->getNumUnits() > 1)
	{
		UnitAITypes eGroupAI = getGroup()->getHeadUnitAIType();
		if (eGroupAI == AI_getUnitAIType())
		{
			if (getPlot().isCity() && getPlot().getOwner() == getOwner())
			{
				AI_getGroup()->AI_separate(); // will change group
				return;
			}
		}
	}

	if (!getPlot().isOwned())
	{
		if (AI_groupMergeRange(UNITAI_SETTLE, 2, true, false, false))
		{
			return;
		}
	}

	// K-Mod
	bool const bDanger = GET_PLAYER(getOwner()).AI_isAnyPlotDanger(getPlot(), 3);
	if (bDanger && getPlot().getTeam() == getTeam())
	{
		if (getPlot().isCity())
		{
			if (AI_leaveAttack(1, 65, 115))
				return;
		}
		else
		{
			if (AI_defendTerritory(70, NO_MOVEMENT_FLAGS, 2, true))
				return;
		}
	}
	// K-Mod end

	//if (AI_guardCity(false, true, 1))
	if (AI_guardCity(false, true, 2)) // K-Mod
	{
		return;
	}

	if (getSameTileHeal() > 0)
	{
		if (!canAttack())
		{
			/*	Don't restrict to groups carrying cargo ...
				does this apply to any units in standard bts anyway? */
			if (AI_shadow(UNITAI_ATTACK_CITY, -1, 21, false, false, 4))
			{
				return;
			}
		}
	}

	AreaAITypes const eAreaAIType = getArea().getAreaAIType(getTeam());

	if (getPlot().getOwner() == getOwner())
	{
		if (!bDanger)
		{
			if (getPlot().isCity())
			{
				if (eAreaAIType == AREAAI_ASSAULT || eAreaAIType == AREAAI_ASSAULT_ASSIST)
				{
					if (AI_offensiveAirlift())
					{
						return;
					}
				}
			}

			if (eAreaAIType == AREAAI_ASSAULT || eAreaAIType == AREAAI_ASSAULT_ASSIST ||
				eAreaAIType == AREAAI_ASSAULT_MASSING)
			{
				if (AI_load(UNITAI_ASSAULT_SEA, MISSIONAI_LOAD_ASSAULT, UNITAI_ATTACK_CITY,
					-1, -1, -1, -1, MOVE_SAFE_TERRITORY, 4))
				{
					return;
				}

				if (AI_load(UNITAI_ASSAULT_SEA, MISSIONAI_LOAD_ASSAULT, UNITAI_ATTACK,
					-1, -1, -1, -1, MOVE_SAFE_TERRITORY, 4))
				{
					return;
				}
			}
		}

		/*if (!noDefensiveBonus()) {
			if (AI_guardCity(false, false))
				return;
		} */ // disabled by K-Mod. This is redundant.
	}

	//join any city attacks in progress
	if (getPlot().getOwner() != getOwner())
	{
		if (AI_groupMergeRange(UNITAI_ATTACK_CITY, 1, true, true))
		{
			return;
		}
	}

	if (bDanger)
	{
		/*if (AI_cityAttack(1, 35))
			return;*/ // disabled by K-Mod

		if (AI_anyAttack(1, 40))
		{
			return;
		}
	}

	bool bIgnoreFasterStacks = false;
	if (GET_PLAYER(getOwner()).AI_isDoStrategy(AI_STRATEGY_LAND_BLITZ))
	{
		if (getArea().getAreaAIType(getTeam()) != AREAAI_ASSAULT)
			bIgnoreFasterStacks = true;
	}

	if (AI_group(UNITAI_ATTACK_CITY, /*iMaxGroup*/ -1, 2, -1, bIgnoreFasterStacks,
		/*bIgnoreOwnUnitType*/ true, /*bStackOfDoom*/ true, /*iMaxPath*/ 6))
	{
		return;
	}

	bool bFastMovers = (GET_PLAYER(getOwner()).AI_isDoStrategy(AI_STRATEGY_FASTMOVERS));
	if (AI_group(UNITAI_ATTACK, /*iMaxGroup*/ 2, -1, -1, bFastMovers,
		/*bIgnoreOwnUnitType*/ true, /*bStackOfDoom*/ true, /*iMaxPath*/ 5))
	{
		return;
	}

	// BBAI TODO: merge with nearby pillage

	//if (AI_guardCity(false, true, 3))
	if (AI_guardCity(true, true, 5)) // K-Mod
	{
		return;
	}

	if (getPlot().getOwner() == getOwner())
	{
		if (!bDanger)
		{
			if (eAreaAIType != AREAAI_DEFENSIVE)
			{
				if (AI_load(UNITAI_ASSAULT_SEA, MISSIONAI_LOAD_ASSAULT, UNITAI_ATTACK_CITY,
					-1, -1, -1, -1, MOVE_SAFE_TERRITORY, 4))
				{
					return;
				}

				if (AI_load(UNITAI_ASSAULT_SEA, MISSIONAI_LOAD_ASSAULT, UNITAI_ATTACK,
					-1, -1, -1, -1, MOVE_SAFE_TERRITORY, 4))
				{
					return;
				}
			}
		}
	}
	// BETTER_BTS_AI_MOD: END
	if (AI_heal())
	{
		return;
	}

	if (AI_offensiveAirlift())
	{
		return;
	}

	if (AI_retreatToCity())
	{
		return;
	}

	// K-Mod
	if (AI_handleStranded())
		return;
	// K-Mod end

	if (AI_safety())
	{
		return;
	}

	getGroup()->pushMission(MISSION_SKIP);
}


void CvUnitAI::AI_cityDefenseMove()
{
	PROFILE_FUNC();
	// BETTER_BTS_AI_MOD, Unit AI, Efficiency, 08/20/09, jdog5000: was AI_getPlotDanger
	bool const bDanger = (GET_PLAYER(getOwner()).AI_isAnyPlotDanger(getPlot(), 3));

	// BETTER_BTS_AI_MOD, Settler AI, 09/18/09, jdog5000: START
	if (!getPlot().isOwned())
	{
		if (AI_group(UNITAI_SETTLE, 1, -1, -1, false, false, false, 2, true))
		{
			return;
		}
	} // BETTER_BTS_AI_MOD: END

	if (bDanger)
	{
		if (AI_leaveAttack(1, 70, 140)) // was ,,175
		{
			return;
		}

		if (AI_chokeDefend())
		{
			return;
		}
	}

	if (AI_guardCityBestDefender())
	{
		return;
	}

	if (!bDanger)
	{
		if (getPlot().getOwner() == getOwner())
		{
			if (AI_load(UNITAI_SETTLER_SEA, MISSIONAI_LOAD_SETTLER, UNITAI_SETTLE,
				-1, -1, 1, -1, MOVE_SAFE_TERRITORY, 1))
			{
				return;
			}
		}
	}

	if (AI_guardCityMinDefender(true))
	{
		return;
	}

	if (AI_guardCity(true))
	{
		return;
	}

	if (!bDanger)
	{
		if (AI_group(UNITAI_SETTLE, /*iMaxGroup*/ 1, -1, -1, false, false, false,
			/*iMaxPath*/ 2, /*bAllowRegrouping*/ true))
		{
			return;
		}

		if (AI_group(UNITAI_SETTLE, /*iMaxGroup*/ 2, -1, -1, false, false, false,
			/*iMaxPath*/ 2, /*bAllowRegrouping*/ true))
		{
			return;
		}

		if (getPlot().getOwner() == getOwner())
		{
			if (AI_load(UNITAI_SETTLER_SEA, MISSIONAI_LOAD_SETTLER, UNITAI_SETTLE,
				-1, -1, 1, -1, MOVE_SAFE_TERRITORY))
			{
				return;
			}
		}
	}

	AreaAITypes eAreaAI = getArea().getAreaAIType(getTeam());
	if (eAreaAI == AREAAI_ASSAULT || eAreaAI == AREAAI_ASSAULT_MASSING ||
		eAreaAI == AREAAI_ASSAULT_ASSIST)
	{
		if (AI_load(UNITAI_ASSAULT_SEA, MISSIONAI_LOAD_ASSAULT, UNITAI_ATTACK_CITY,
			-1, -1, -1, 0, MOVE_SAFE_TERRITORY))
		{
			return;
		}
	}

	if ((AI_getBirthmark() % 4) == 0)
	{
		if (AI_guardFort())
		{
			return;
		}
	}

	if (AI_guardCityAirlift())
	{
		return;
	}

	if (AI_guardCity(false, true, 1))
	{
		return;
	}

	if (getPlot().getOwner() == getOwner())
	{
		if (AI_load(UNITAI_SETTLER_SEA, MISSIONAI_LOAD_SETTLER, UNITAI_SETTLE,
			3, -1, -1, -1, MOVE_SAFE_TERRITORY))
		{
			// will enter here if in danger
			return;
		}
	}
	// BETTER_BTS_AI_MOD, City AI, 04/02/10, jdog5000: join any city attacks in progress
	/*if (getPlot().getOwner() != getOwner()) {
		if (AI_groupMergeRange(UNITAI_ATTACK_CITY, 1, true, true))
			return;
	}*/ // disabled by K-Mod (how often do you think this is going to help us?)

	if (AI_guardCity(false, true))
	{
		return;
	}
	// BETTER_BTS_AI_MOD, Unit AI, 03/04/10, jdog5000: START
	if (!isBarbarian() && (getArea().getAreaAIType(getTeam()) == AREAAI_OFFENSIVE ||
		getArea().getAreaAIType(getTeam()) == AREAAI_MASSING))
	{
		bool bIgnoreFaster = false;
		if (GET_PLAYER(getOwner()).AI_isDoStrategy(AI_STRATEGY_LAND_BLITZ))
		{
			if (getArea().getAreaAIType(getTeam()) != AREAAI_ASSAULT)
			{
				bIgnoreFaster = true;
			}
		}

		if (AI_group(UNITAI_ATTACK_CITY, -1, 2, 4, bIgnoreFaster))
		{
			return;
		}
	}

	if (getArea().getAreaAIType(getTeam()) == AREAAI_ASSAULT)
	{
		if (AI_load(UNITAI_ASSAULT_SEA, MISSIONAI_LOAD_ASSAULT, UNITAI_ATTACK_CITY,
			2, -1, -1, 1, MOVE_SAFE_TERRITORY))
		{
			return;
		}
	}
	// BETTER_BTS_AI_MOD: END

	if (AI_retreatToCity())
	{
		return;
	}

	// K-Mod
	if (AI_handleStranded())
		return;
	// K-Mod end

	if (AI_safety())
	{
		return;
	}

	getGroup()->pushMission(MISSION_SKIP);
}


void CvUnitAI::AI_cityDefenseExtraMove()
{
	PROFILE_FUNC();

	// BETTER_BTS_AI_MOD, Settler AI, 09/18/09, jdog5000: START
	if (!getPlot().isOwned())
	{
		if (AI_group(UNITAI_SETTLE, 1, -1, -1, false, false, false, 1, true))
		{
			return;
		}
	} // BETTER_BTS_AI_MOD: END

	if (AI_leaveAttack(2, 55, 150))
	{
		return;
	}

	if (AI_chokeDefend())
	{
		return;
	}

	if (AI_guardCityBestDefender())
	{
		return;
	}

	if (AI_guardCity(true))
	{
		return;
	}

	if (AI_group(UNITAI_SETTLE, /*iMaxGroup*/ 1, -1, -1, false, false, false,
		/*iMaxPath*/ 2, /*bAllowRegrouping*/ true))
	{
		return;
	}

	if (AI_group(UNITAI_SETTLE, /*iMaxGroup*/ 2, -1, -1, false, false, false,
		/*iMaxPath*/ 2, /*bAllowRegrouping*/ true))
	{
		return;
	}

	CvCity* pCity = getPlot().getPlotCity();

	if (pCity != NULL && pCity->getOwner() == getOwner()) // XXX check for other team?
	{
		if (getPlot().plotCount(PUF_canDefendGroupHead, -1, -1, getOwner(),
			NO_TEAM, PUF_isUnitAIType, AI_getUnitAIType()) == 1)
		{
			getGroup()->pushMission(MISSION_SKIP);
			return;
		}
	}

	if (AI_guardCityAirlift())
	{
		return;
	}

	if (AI_guardCity(false, true, 1))
	{
		return;
	}

	if (getPlot().getOwner() == getOwner())
	{
		if (AI_load(UNITAI_SETTLER_SEA, MISSIONAI_LOAD_SETTLER,
			UNITAI_SETTLE, 3, -1, -1, -1, MOVE_SAFE_TERRITORY, 3))
		{
			return;
		}
	}

	if (AI_guardCity(false, true))
	{
		return;
	}

	if (AI_retreatToCity())
	{
		return;
	}

	if (AI_safety())
	{
		return;
	}

	getGroup()->pushMission(MISSION_SKIP);
}


void CvUnitAI::AI_exploreMove()
{
	PROFILE_FUNC();

	if (!isHuman() && canAttack())
	{
		/*if (AI_cityAttack(1, 60))
			return;*/ // disabled by K-Mod

		if (AI_anyAttack(1, 70))
		{
			return;
		}
	}
	// <advc.299> Instead of simply healing while getDamage() > 0
	if (AI_singleUnitHeal(2, 5))
		return; // </advc.299>

	if (!isHuman())
	{
		//if (AI_pillageRange(1))
		if (AI_pillageRange(3, 10)) // K-Mod
		{
			return;
		}

		if (AI_cityAttack(3, 80))
		{
			return;
		}
	}

	if (AI_goody(4))
	{
		return;
	}

	if (AI_exploreRange(3))
	{
		return;
	}

	if (!isHuman())
	{
		if (AI_pillageRange(3))
		{
			return;
		}
	}

	if (AI_explore())
	{
		return;
	}

	if (!isHuman())
	{
		if (AI_pillage())
		{
			return;
		}
	}

	if (!isHuman())
	{
		if (AI_travelToUpgradeCity())
		{
			return;
		}
	} // <advc.315> Idle explorers can help guard city sites
	if(!isHuman() && !GC.getGame().isOption(GAMEOPTION_NO_BARBARIANS) &&
		(getUnitInfo().getCombat() * (100 + barbarianCombatModifier())) / 100 >=
		(GET_PLAYER(BARBARIAN_PLAYER).getCurrentEra() + 1) * 2)
	{
		if(AI_guardCitySite())
			return;
	} // </advc.315>
	if (!isHuman() && (AI_getUnitAIType() == UNITAI_EXPLORE))
	{
		if (GET_PLAYER(getOwner()).AI_totalAreaUnitAIs(getArea(), UNITAI_EXPLORE) >
			GET_PLAYER(getOwner()).AI_neededExplorers(getArea()))
		{
			if (GET_PLAYER(getOwner()).calculateUnitCost() > 0)
			{
				// K-Mod. Maybe we can still use this unit.
				if (GET_PLAYER(getOwner()).AI_unitValue(getUnitType(), UNITAI_ATTACK, area()) > 0)
					AI_setUnitAIType(UNITAI_ATTACK);
				else // K-Mod end
					scrap();
				return;
			}
		}
	}
	// K-Mod
	if (AI_handleStranded())
		return;
	// K-Mod end

	if (AI_patrol())
	{
		return;
	}

	if (AI_retreatToCity())
	{
		return;
	}

	if (AI_safety())
	{
		return;
	}

	getGroup()->pushMission(MISSION_SKIP);
}


void CvUnitAI::AI_missionaryMove()
{
	PROFILE_FUNC();

	// K-Mod. Split up groups of automated missionaries - automate them individually.
	if (getGroup()->getNumUnits() > 1)
	{
		AutomateTypes eAutomate = getGroup()->getAutomateType();
		FAssert(isHuman() && eAutomate != NO_AUTOMATE);
		FOR_EACH_UNIT_VAR_IN(pLoopUnit, *getGroup())
		{
			if (pLoopUnit->canAutomate(eAutomate))
			{
				pLoopUnit->joinGroup(NULL, true);
				pLoopUnit->automate(eAutomate);
			}
		}
		return;
	} // K-Mod end

	if (AI_spreadReligion())
	{
		return;
	}

	if (AI_spreadCorporation())
	{
		return;
	}

	if (!isHuman() || (isAutomated() && GET_TEAM(getTeam()).getNumWars() <= 0))
	{
		if (!isHuman() || (getGameTurnCreated() < GC.getGame().getGameTurn()))
		{
			if (AI_spreadReligionAirlift())
			{
				return;
			}
			if (AI_spreadCorporationAirlift())
			{
				return;
			}
		}

		if (!isHuman())
		{
			// advc (note): BtS had first tried MOVE_SAFE_TERRITORY; K-Mod removed that.
			if (AI_load(UNITAI_MISSIONARY_SEA, MISSIONAI_LOAD_SPECIAL, NO_UNITAI,
				-1, -1, -1, 0, MOVE_NO_ENEMY_TERRITORY))
			{
				return;
			}
		}
	}

	if (AI_retreatToCity(/* K-Mod */ false, true))
	{
		return;
	}
	// K-Mod
	if (AI_handleStranded())
		return;
	// K-Mod end
	if (AI_safety())
	{
		return;
	}

	getGroup()->pushMission(MISSION_SKIP);
}


void CvUnitAI::AI_generalMove()
{
	PROFILE_FUNC();

	std::vector<UnitAITypes> aeUnitAITypes;
	bool const bOffenseWar = (getArea().getAreaAIType(getTeam()) == AREAAI_OFFENSIVE);

	if (GET_PLAYER(getOwner()).AI_isAnyPlotDanger(getPlot(), 2))
	{
		aeUnitAITypes.clear();
		aeUnitAITypes.push_back(UNITAI_ATTACK);
		aeUnitAITypes.push_back(UNITAI_COUNTER);
		if (AI_lead(aeUnitAITypes))
		{
			return;
		}
	}

	if (AI_construct(1))
	{
		return;
	}

	if (AI_join(1))
	{
		return;
	}
	// BETTER_BTS_AI_MOD, Unit AI, 05/14/10, jdog5000: START
	if (bOffenseWar && (AI_getBirthmark() % 2 == 0))
	{
		aeUnitAITypes.clear();
		aeUnitAITypes.push_back(UNITAI_ATTACK_CITY);
		if (AI_lead(aeUnitAITypes))
		{
			return;
		}

		aeUnitAITypes.clear();
		aeUnitAITypes.push_back(UNITAI_ATTACK);
		if (AI_lead(aeUnitAITypes))
		{
			return;
		}
	} // BETTER_BTS_AI_MOD: END

	if (AI_join(2))
	{
		return;
	}

	if (AI_construct(2))
	{
		return;
	}

	if (AI_join(4))
	{
		return;
	}

	if (SyncRandOneChanceIn(3))
	{
		if (AI_construct())
		{
			return;
		}
	}

	if (AI_join())
	{
		return;
	}

	if (AI_retreatToCity())
	{
		return;
	}

	// K-Mod
	if (AI_handleStranded())
		return;
	// K-Mod end

	if (AI_safety())
	{
		return;
	}

	getGroup()->pushMission(MISSION_SKIP);
}

/*	K-Mod. For most great people, the AI needs to do similar checks and calculations.
	I've made this general function to do those calculations for all types of GP.
	advc: Now handles the entire GP move (except Great General). */
// TODO: implement:
// Great Prophet: Great Mission
// Great Statesman: Diplomatic Mission
// Great Statesman: Resolve Crisis
// Great Statesman: Diplomatc Mission
void CvUnitAI::AI_greatPersonMove()
{
	const CvPlayerAI& kOwner = GET_PLAYER(getOwner());

	enum
	{
		GP_SLOW,
		GP_DISCOVER,
		GP_GOLDENAGE,
		GP_TRADE,
		GP_CULTURE
	};
	std::vector<std::pair<int, int> > missions; // (value, mission)
	// 1) Add possible missions to the mission vector.
	// 2) Sort them.
	// 3) Attempt to carry out missions, starting with the highest value.

	CvPlot* pBestPlot = NULL;
	SpecialistTypes eBestSpecialist = NO_SPECIALIST;
	BuildingTypes eBestBuilding = NO_BUILDING;
	int iBestValue = 1;
	int iBestPathTurns = MAX_INT; // just used as a tie-breaker.
	MovementFlags const eMoveFlags = (alwaysInvisible() ?
			NO_MOVEMENT_FLAGS : MOVE_NO_ENEMY_TERRITORY);
	bool bCanHurry = (getUnitInfo().getBaseHurry() > 0 ||
			getUnitInfo().getHurryMultiplier() > 0);

	FOR_EACH_CITYAI(pLoopCity, kOwner)
	{	// <advc.139>
		if (!pLoopCity->AI_isSafe())
			continue; // </advc.139>
		int iPathTurns;
		if (!AI_canEnterByLand(pLoopCity->getArea()) || // advc.030 (replacing same-area check)
			!generatePath(pLoopCity->getPlot(), eMoveFlags, true, &iPathTurns))
		{
			continue;
		}
		// Join
		FOR_EACH_ENUM(Specialist)
		{
			if (canJoin(pLoopCity->plot(), eLoopSpecialist))
			{
				// Note, specialistValue is roughly 400x the commerce it provides. So /= 4 to make it 100x.
				int iValue = pLoopCity->AI_permanentSpecialistValue(eLoopSpecialist)/4;
				if (iValue > iBestValue || (iValue == iBestValue && iPathTurns < iBestPathTurns))
				{
					iBestValue = iValue;
					pBestPlot = &getPathEndTurnPlot();
					eBestSpecialist = eLoopSpecialist;
					eBestBuilding = NO_BUILDING;
				}
			}
		}
		// Construct
		CvCivilization const& kCiv = GET_PLAYER(getOwner()).getCivilization(); // advc.003w
		for (int i = 0; i < kCiv.getNumBuildings(); i++)
		{
			BuildingTypes eBuilding = kCiv.buildingAt(i);
			if ((//getUnitInfo().getForceBuildings(eBuilding) || // advc.003t
				getUnitInfo().getBuildings(eBuilding)) &&
				canConstruct(pLoopCity->plot(), eBuilding))
			{
				// Note, building value is roughly 4x the value of the commerce it provides.
				// so we * 25 to match the scale of specialist value.
				int iValue = pLoopCity->AI_buildingValue(eBuilding) * 25;
				if (iValue > iBestValue || (iValue == iBestValue && iPathTurns < iBestPathTurns))
				{
					iBestValue = iValue;
					pBestPlot = &getPathEndTurnPlot();
					eBestBuilding = eBuilding;
					eBestSpecialist = NO_SPECIALIST;
				}
				continue;
			}
			if (!bCanHurry || !GC.getInfo(eBuilding).isWorldWonder() ||
				!pLoopCity->canConstruct(eBuilding))
			{
				continue;
			}
			// maybe we can hurry a wonder...
			int iCost = pLoopCity->getProductionNeeded(eBuilding);
			int iHurryProduction = getMaxHurryProduction(pLoopCity);
			int iProgress = pLoopCity->getBuildingProduction(eBuilding);
			int iProductionRate = (iCost <= iHurryProduction + iProgress) ? 0 :
					pLoopCity->getProductionDifference(iCost, iProgress,
					pLoopCity->getProductionModifier(eBuilding), false, 0);
			// note: currently, it is impossible for a building to be "food production".
			/*  also note that iProductionRate will return 0 if the city is in disorder.
				This may mess up our great person's decision - but it's a
				non-trivial problem to fix. */
			if (pLoopCity->getProductionBuilding() == eBuilding)
				iProgress += iProductionRate * iPathTurns;
			FAssert(iHurryProduction > 0);

			int iFraction = 100 * std::min(iHurryProduction, iCost-iProgress) /
					std::max(1, iCost);
			if (iFraction > 40) // arbitary, and somewhat unneccessary.
			{
				FAssert(iFraction <= 100);
				int iValue = pLoopCity->AI_buildingValue(eBuilding) * 25 * iFraction / 100;
				if (iProgress + iHurryProduction < iCost)
				{
					// decrease the value, because we might still miss out!
					FAssert(iProductionRate > 0 || pLoopCity->isDisorder());
					iValue *= 12;
					iValue /= 12 + std::min(30, pLoopCity->getProductionTurnsLeft(
							iCost, iProgress, iProductionRate, iProductionRate));
				}

				if (iValue > iBestValue || (iValue == iBestValue && iPathTurns < iBestPathTurns))
				{
					iBestValue = iValue;
					pBestPlot = &getPathEndTurnPlot();
					iBestPathTurns = iPathTurns;
					eBestBuilding = eBuilding;
					eBestSpecialist = NO_SPECIALIST;
				}
			}
		}
	} // end city loop.

	// Golden age
	int iGoldenAgeValue = 0;
	if (isGoldenAge())
	{
		iGoldenAgeValue = GET_PLAYER(getOwner()).AI_calculateGoldenAgeValue() /
				GET_PLAYER(getOwner()).unitsRequiredForGoldenAge();
		iGoldenAgeValue *= (75 + kOwner.AI_getStrategyRand(0) % 51);
		iGoldenAgeValue /= 100;
		missions.push_back(std::pair<int, int>(iGoldenAgeValue, GP_GOLDENAGE));
	}
	//

	// Discover ("bulb tech")
	scaled rDiscoverValue;
	TechTypes eDiscoverTech = getDiscoveryTech();
	if (eDiscoverTech != NO_TECH)
	{
		rDiscoverValue = getDiscoverResearch(eDiscoverTech);
		// if this isn't going to immediately help our research, it isn't worth as much.
		if (rDiscoverValue < GET_TEAM(getTeam()).getResearchLeft(eDiscoverTech) &&
			kOwner.getCurrentResearch() != eDiscoverTech)
		{
			rDiscoverValue.mulDiv(2, 3);
		}
		// founding religions / free techs / free great people
		if (kOwner.AI_isFirstTech(eDiscoverTech))
			rDiscoverValue *= 2;
		// amplify the 'undiscovered' bonus based on how likely we are to try to trade the tech.
		rDiscoverValue *= 1 +
				((2 - per100(GC.getInfo(kOwner.getPersonalityType()).getTechTradeKnownPercent())) *
				(GET_TEAM(getTeam()).AI_knownTechValModifier(eDiscoverTech)
				-1)); // advc: AI_knownTechValModifier now 1 higher than in K-Mod
		if(GET_PLAYER(getOwner()).AI_isFocusWar()) // advc.105
		//if (GET_TEAM(getTeam()).getAnyWarPlanCount(true) || kOwner.AI_isDoStrategy(AI_STRATEGY_ALERT2))
		{
			rDiscoverValue *= (getArea().getAreaAIType(getTeam()) == AREAAI_DEFENSIVE ? 5 : 4);
			rDiscoverValue /= 3;
		}
		rDiscoverValue *= per100(75 + kOwner.AI_getStrategyRand(3) % 51);
		missions.push_back(std::pair<int, int>(rDiscoverValue.round(), GP_DISCOVER));
	}

	CvGame const& kGame = GC.getGame();
	/*	SlowValue is meant to be a rough estimation of how much value we'll get
		from doing the best join / build mission. To give this estimate,
		I'm going to do a rough personality-based calculation of how many turns
		to count. Note that "iBestValue" is roughly 100x commerce per turn for
		our best join or build mission. Also note that the commerce per turn is
		likely to increase as we improve our city infrastructure and so on. */
	int iSlowValue = iBestValue;
	if (iSlowValue > 0)
	{
		// multiply by the full number of turns remaining
		iSlowValue *= kGame.getEstimateEndTurn() - kGame.getGameTurn();

		// construct a modifier based on what victory we might like to aim for with our personality & situation
		int iModifier = 0;
		/*	<advc.115f> Had used weights from kOwner's personality directly.
			I don't think the weights should count when the respective
			victory is unavailable (debatable ...). */
		FOR_EACH_ENUM(Victory)
		{
			int const iWeight = kOwner.AI_getVictoryWeight(eLoopVictory);
			if (eLoopVictory == kGame.getSpaceVictory())
			{
				iModifier += 2 * std::max(iWeight,
						kOwner.AI_atVictoryStage(AI_VICTORY_SPACE1) ? 35 : 0);
			}
			if (GC.getInfo(eLoopVictory).getCityCulture() > 0)
			{
				iModifier += 1 * std::max(iWeight,
						kOwner.AI_atVictoryStage(AI_VICTORY_CULTURE1) ? 35 : 0);
			}
			if (eLoopVictory == kGame.getDominationVictory())
			{
				iModifier -= std::max(iWeight,
						kOwner.AI_atVictoryStage(AI_VICTORY_DOMINATION1) ? 35 : 0);
			}
			if (GC.getInfo(eLoopVictory).isConquest())
			{
				iModifier -= 2 * std::max(iWeight,
						kOwner.AI_atVictoryStage(AI_VICTORY_CONQUEST1) ? 35 : 0);
			}
			//if (GC.getInfo(eLoopVictory).isDiploVote()) {}
		} // </advc.115f>
		/*	If we're small, then slow & steady progress might be our best hope
			to keep up. So increase the modifier for small civs.
			(think avg. cities / our cities) */
		iModifier += range(40 * kGame.getNumCivCities() / std::max(1,
				kGame.countCivPlayersAlive() * kOwner.getNumCities()) - 50,
				0, 50);

		// convert the modifier into some percentage of the remaining turns
		iModifier = range(30 + iModifier/2, 20, 80);
		// apply it
		iSlowValue *= iModifier;
		iSlowValue /= 10000; // (also removing excess factor of 100)

		// half the value if anyone we know is up to stage 4. (including us)
		for (PlayerTypes i = (PlayerTypes)0; i < MAX_CIV_PLAYERS; i=(PlayerTypes)(i+1))
		{
			const CvPlayerAI& kLoopPlayer = GET_PLAYER(i);
			if (kLoopPlayer.isAlive() && kLoopPlayer.AI_atVictoryStage4() && GET_TEAM(getTeam()).isHasMet(kLoopPlayer.getTeam()))
			{
				iSlowValue /= 2;
				break; // just once.
			}
		}
		//if (gUnitLogLevel > 2) logBBAI("    %S GP slow modifier: %d, value: %d", GET_PLAYER(getOwner()).getCivilizationDescription(0), range(30 + iModifier/2, 20, 80), iSlowValue);
		iSlowValue *= (75 + kOwner.AI_getStrategyRand(6) % 51);
		iSlowValue /= 100;
		missions.push_back(std::pair<int, int>(iSlowValue, GP_SLOW));
	}

	// Trade mission
	CvPlot* pBestTradePlot;
	int iTradeValue = AI_tradeMissionValue(pBestTradePlot, (rDiscoverValue / 2).round());
	// make it roughly comparable to research points
	if (pBestTradePlot != NULL)
	{
		iTradeValue *= kOwner.AI_commerceWeight(COMMERCE_GOLD);
		iTradeValue /= 100;
		iTradeValue *= kOwner.AI_averageCommerceMultiplier(COMMERCE_RESEARCH);
		iTradeValue /= kOwner.AI_averageCommerceMultiplier(COMMERCE_GOLD);
		// gold can be targeted where it is needed, but it's benefits typically aren't instant. (cf AI_knownTechValModifier)
		iTradeValue *= 130;
		iTradeValue /= 100;
		if (AI_getGroup()->AI_getMissionAIType() == MISSIONAI_TRADE &&
			getPlot().getOwner() != getOwner())
		{
			// if we are part way through a trade mission, prefer not to turn back.
			iTradeValue *= 120;
			iTradeValue /= 100;
		}
		iTradeValue *= (75 + kOwner.AI_getStrategyRand(9) % 51);
		iTradeValue /= 100;
		missions.push_back(std::pair<int, int>(iTradeValue, GP_TRADE));
	}

	// Great works (culture bomb)
	CvPlot* pBestCulturePlot;
	int iCultureValue = AI_greatWorkValue(pBestCulturePlot, (rDiscoverValue / 2).round());
	if (pBestCulturePlot != 0)
	{
		missions.push_back(std::pair<int, int>(iCultureValue, GP_CULTURE));
	}

	// Sort the list!
	std::sort(missions.begin(), missions.end(), std::greater<std::pair<int, int> >());
	std::vector<std::pair<int, int> >::iterator it;

	int iChoice = 1;
	int iScoreThreshold = 0;
	for (it = missions.begin(); it != missions.end(); ++it)
	{
		if (it->first < iScoreThreshold)
			break;

		switch (it->second)
		{
		case GP_DISCOVER:
			if (canDiscover(plot()))
			{
				getGroup()->pushMission(MISSION_DISCOVER);
				if (gUnitLogLevel > 2) logBBAI("    %S chooses 'discover' (%S) with their %S (value: %d, choice #%d)", GET_PLAYER(getOwner()).getCivilizationDescription(0), GC.getInfo(eDiscoverTech).getDescription(), getName(0).GetCString(), rDiscoverValue.round(), iChoice);
				return;
			}
			break;

		case GP_TRADE:
			{
				MissionAITypes eOldMission = AI_getGroup()->AI_getMissionAIType(); // just used for the log message below
				if (AI_doTradeMission(pBestTradePlot))
				{
					if (gUnitLogLevel > 2) logBBAI("    %S %s 'trade mission' with their %S (value: %d, choice #%d)", GET_PLAYER(getOwner()).getCivilizationDescription(0), eOldMission == MISSIONAI_TRADE?"continues" :"chooses", getName(0).GetCString(), iTradeValue, iChoice);
					return;
				}
				break;
			}

		case GP_CULTURE:
			{
				MissionAITypes eOldMission = AI_getGroup()->AI_getMissionAIType(); // just used for the log message below
				if (AI_doGreatWork(pBestCulturePlot))
				{
					if (gUnitLogLevel > 2) logBBAI("    %S %s 'great work' with their %S (value: %d, choice #%d)", GET_PLAYER(getOwner()).getCivilizationDescription(0), eOldMission == MISSIONAI_TRADE?"continues" :"chooses", getName(0).GetCString(), iCultureValue, iChoice);
					return;
				}
				break;
			}

		case GP_GOLDENAGE:
			if (AI_goldenAge())
			{
				if (gUnitLogLevel > 2) logBBAI("    %S chooses 'golden age' with their %S (value: %d, choice #%d)", GET_PLAYER(getOwner()).getCivilizationDescription(0), getName(0).GetCString(), iGoldenAgeValue, iChoice);
				return;
			}
			else if (kOwner.AI_totalUnitAIs(AI_getUnitAIType()) < 2)
			{
				// Do we want to wait for another great person? How long will it take?
				int iGpThreshold = kOwner.greatPeopleThreshold();
				int iMinTurns = MAX_INT;
				//int iPercentOther; // chance of it being a different GP.
				// unfortunately, it's non-trivial to calculate the GP type probabilies. So I'm leaving it out.
				FOR_EACH_CITY(pLoopCity, kOwner)
				{
					int iGpRate = pLoopCity->getGreatPeopleRate();
					if (iGpRate > 0)
					{
						int iGpProgress = pLoopCity->getGreatPeopleProgress();
						int iTurns = (iGpThreshold - iGpProgress + iGpRate - 1) / iGpRate;
						if (iTurns < iMinTurns)
							iMinTurns = iTurns;
					}
				}

				if (iMinTurns != MAX_INT)
				{
					int iRelativeWaitTime = iMinTurns + (kGame.getGameTurn() - getGameTurnCreated());
					iRelativeWaitTime *= 100;
					iRelativeWaitTime /= kGame.getSpeedPercent();
					// lets say 1% per turn.
					iScoreThreshold = std::max(iScoreThreshold, it->first * (100 - iRelativeWaitTime) / 100);
				}
			}
			break;

		case GP_SLOW:
			// no dedicated function for this.
			if (pBestPlot == NULL)
				break;
			if (eBestSpecialist != NO_SPECIALIST)
			{
				if (gUnitLogLevel > 2) logBBAI("    %S %s 'join' with their %S (value: %d, choice #%d)", GET_PLAYER(getOwner()).getCivilizationDescription(0), AI_getGroup()->AI_getMissionAIType() == MISSIONAI_JOIN_CITY?"continues" :"chooses", getName(0).GetCString(), iSlowValue, iChoice);
				if (at(*pBestPlot))
				{
					getGroup()->pushMission(MISSION_JOIN, eBestSpecialist);
					return;
				}
				else
				{
					pushGroupMoveTo(*pBestPlot, eMoveFlags, false, false, MISSIONAI_JOIN_CITY);
					return;
				}
			}
			if (eBestBuilding != NO_BUILDING)
			{
				MissionAITypes eMissionAI = canConstruct(pBestPlot, eBestBuilding) ? MISSIONAI_CONSTRUCT : MISSIONAI_HURRY;
				if (gUnitLogLevel > 2) logBBAI("    %S %s 'build' (%S) with their %S (value: %d, choice #%d)", GET_PLAYER(getOwner()).getCivilizationDescription(0), AI_getGroup()->AI_getMissionAIType() == eMissionAI?"continues" :"chooses", GC.getInfo(eBestBuilding).getDescription(), getName(0).GetCString(), iSlowValue, iChoice);
				if (at(*pBestPlot))
				{
					if (eMissionAI == MISSIONAI_CONSTRUCT)
						getGroup()->pushMission(MISSION_CONSTRUCT, eBestBuilding);
					else
					{
						// switch and hurry.
						CvCity* pCity = pBestPlot->getPlotCity();
						if (pCity->getProductionBuilding() != eBestBuilding)
							pCity->pushOrder(ORDER_CONSTRUCT, eBestBuilding);
						if (pCity->getProductionBuilding() == eBestBuilding && canHurry(plot()))
							getGroup()->pushMission(MISSION_HURRY);
						else
						{
							FErrorMsg("great person cannot hurry what it intended to hurry.");
							break;
						}
					}
					return;
				}
				else
				{
					pushGroupMoveTo(*pBestPlot, eMoveFlags, false, false, eMissionAI);
					return;
				}
			}
			break;
		default:
			FErrorMsg("Unhandled great person mission");
			break;
		}
		iChoice++;
	}
	// advc: Can be 0 when no city has a positive GP rate. I don't think that's a problem.
	//FAssert(iScoreThreshold > 0);
	// advc: Branch for Great Spy - cut from the deleted AI_greatSpyMove.
	if (alwaysInvisible())
	{	// K-Mod note: spies can't be seen, and can't be attacked. So we don't need to worry about retreating to safety.
		if (getArea().getNumCities() > getArea().getCitiesPerPlayer(getOwner()))
		{
			if (AI_reconSpy(5))
				return;
		}
		if (AI_handleStranded())
			return;

		getGroup()->pushMission(MISSION_SKIP);
		return;
	}
	/*  advc: I've cut and pasted the rest of this function from AI_greatEngineerMove;
		the exact same thing was being done for Prophet, Merchant, Artist and Scientist. */
	/*if ((GET_PLAYER(getOwner()).AI_getAnyPlotDanger(plot(), 2)) ||
		(getGameTurnCreated() < (kGame.getGameTurn() - 25)))*/ // BtS
	if (GET_PLAYER(getOwner()).AI_isAnyPlotDanger(getPlot(), 2)) // K-Mod (there are good reasons for saving a great person)
	{
		if (AI_discover())
			return;
	}
	if (gUnitLogLevel > 2) logBBAI("    %S chooses 'wait' with their %S (value: %d, dead time: %d)", GET_PLAYER(getOwner()).getCivilizationDescription(0), getName(0).GetCString(), iScoreThreshold, kGame.getGameTurn() - getGameTurnCreated());
	if (AI_retreatToCity())
		return;
	// K-Mod
	if (AI_handleStranded())
		return;
	// K-Mod end
	if (AI_safety())
		return;

	getGroup()->pushMission(MISSION_SKIP);
} // K-Mod end

// Edited heavily for K-Mod
void CvUnitAI::AI_spyMove()
{
	PROFILE_FUNC();

	const CvTeamAI& kTeam = GET_TEAM(getTeam());
	const CvPlayerAI& kOwner = GET_PLAYER(getOwner());

	// First, let us finish any missions that we were part way through doing
	{
		CvPlot* pMissionPlot = AI_getGroup()->AI_getMissionAIPlot();
		if (pMissionPlot != NULL)
		{
			switch (AI_getGroup()->AI_getMissionAIType())
			{
			case MISSIONAI_GUARD_SPY:
				if (pMissionPlot->getOwner() == getOwner())
				{
					if (at(*pMissionPlot))
					{
						// stay here for a few turns.
						if (hasMoved())
						{
							getGroup()->pushMission(MISSION_SKIP, -1, -1, NO_MOVEMENT_FLAGS,
									false, false, MISSIONAI_GUARD_SPY, pMissionPlot);
							return;
						}
						if (SyncRandSuccessRatio(5, 6))
						{
							getGroup()->pushMission(MISSION_SKIP, -1, -1, NO_MOVEMENT_FLAGS,
									false, false, MISSIONAI_GUARD_SPY, pMissionPlot);
							return;
						}
					}
					else
					{
						// continue to the destination
						if (generatePath(*pMissionPlot, NO_MOVEMENT_FLAGS, true))
						{
							pushGroupMoveTo(getPathEndTurnPlot(),
									NO_MOVEMENT_FLAGS, false, false,
									MISSIONAI_GUARD_SPY, pMissionPlot);
							return;
						}
					}
				}
				break;
			case MISSIONAI_ATTACK_SPY:
				if (pMissionPlot->getTeam() != getTeam())
				{
					if (!at(*pMissionPlot))
					{
						// continue to the destination
						if (generatePath(*pMissionPlot, NO_MOVEMENT_FLAGS, true))
						{
							pushGroupMoveTo(getPathEndTurnPlot(),
									NO_MOVEMENT_FLAGS, false, false,
									MISSIONAI_ATTACK_SPY, pMissionPlot);
							return;
						}
					}
					else if (hasMoved())
					{
						getGroup()->pushMission(MISSION_SKIP, -1, -1, NO_MOVEMENT_FLAGS,
								false, false, MISSIONAI_ATTACK_SPY);
						return;
					}
				}
				break;
			case MISSIONAI_EXPLORE:
				/*if (atPlot(pMissionPlot))
					getGroup()->AI_setMissionAI(NO_MISSIONAI, NULL, NULL);*/
				break;
			case MISSIONAI_LOAD_SPECIAL:
				if (AI_load(UNITAI_SPY_SEA, MISSIONAI_LOAD_SPECIAL))
					return;

			default:
				break;
			}
		}
	}

	if (getPlot().isOwned() && getPlot().getTeam() != getTeam() &&
		GET_PLAYER(getPlot().getOwner()).isMajorCiv()) // advc.003n
	{
		int iSpontaneousChance = 0;
		switch (GET_PLAYER(getOwner()).AI_getAttitude(getPlot().getOwner()))
		{
		case ATTITUDE_FURIOUS:
			iSpontaneousChance = 100;
			break;

		case ATTITUDE_ANNOYED:
			iSpontaneousChance = 50;
			break;

		case ATTITUDE_CAUTIOUS: // advc.019: was ?30:10
			iSpontaneousChance = (GC.getGame().isOption(GAMEOPTION_AGGRESSIVE_AI) ? 20 : 10);
			break;

		case ATTITUDE_PLEASED: // advc.019: was ?20:0
			iSpontaneousChance = (GC.getGame().isOption(GAMEOPTION_AGGRESSIVE_AI) ? 15 : 0);
			break;

		case ATTITUDE_FRIENDLY:
			iSpontaneousChance = 0;
			break;

		default:
			FAssert(false);
			break;
		}

		WarPlanTypes eWarPlan = kTeam.AI_getWarPlan(getPlot().getTeam());
		if (eWarPlan != NO_WARPLAN)
		{
			if (eWarPlan == WARPLAN_LIMITED)
			{
				iSpontaneousChance += 50;
			}
			else
			{
				iSpontaneousChance += 20;
			}
		}

		if (getPlot().isCity())
		{
			bool bTargetCity = false;

			// would we have more power if enemy defenses were down?
			/*int iOurPower = kOwner.AI_getOurPlotStrength(plot(),1,false,true);
			int iEnemyPower = kOwner.AI_getEnemyPlotStrength(plot(),0,false,false);*/ // BBAI
			// K-Mod note: telling AI_getEnemyPlotStrength to not count defensive bonuses is not what we want.
			// That would make it not count hills and city defence promotions; and instead count collateral damage power.
			// Instead, I'm going to count the defensive bonuses, and then try to approximately remove the city part.
			int iOurPower = kOwner.AI_localAttackStrength(plot(), getTeam(), DOMAIN_LAND, 1, true, true);
			int iEnemyPower = kOwner.AI_localDefenceStrength(plot(), NO_TEAM, DOMAIN_LAND, 0);
			{
				int iBase = 235 + (getPlot().isHills() ? GC.getDefineINT(CvGlobals::HILLS_EXTRA_DEFENSE) : 0);
				iEnemyPower *= iBase - getPlot().getPlotCity()->getDefenseModifier(false);
				iEnemyPower /= iBase;
			}
			// cf. approximation used in AI_attackCityMove. (here we are slightly more pessimistic)

			//if (5 * iOurPower > 6 * iEnemyPower && eWarPlan != NO_WARPLAN)
			if (95*iOurPower > GC.getDefineINT(CvGlobals::BBAI_ATTACK_CITY_STACK_RATIO)*iEnemyPower && eWarPlan != NO_WARPLAN
					&& iOurPower < 8 * iEnemyPower) // advc.120b
			{
				bTargetCity = true;

				if (AI_revoltCitySpy())
				{
					return;
				}
				if (SyncRandSuccessRatio(5, 6))
				{
					getGroup()->pushMission(MISSION_SKIP, -1, -1, NO_MOVEMENT_FLAGS,
							false, false, MISSIONAI_ATTACK_SPY, plot());
					return;
				}
				if (getPlot().plotCount(PUF_isSpy, -1, -1, getOwner()) > 2)
				{
					if (AI_cityOffenseSpy(5, getPlot().getPlotCity()))
					{
						return;
					}
				}
			}

			/*	I think this spontaneous thing is bad. I'm leaving it in,
				but with greatly diminished probability. */
			// scale for game speed
			iSpontaneousChance *= 100;
			iSpontaneousChance /= GC.getGame().getSpeedPercent();
			if (SyncRandNum(1500) < iSpontaneousChance)
			{
				if (AI_espionageSpy())
				{
					return;
				}
			}

			if (kOwner.AI_isAnyPlotTargetMissionAI(getPlot(), MISSIONAI_ASSAULT, getGroup()))
			{
				bTargetCity = true;

				getGroup()->pushMission(MISSION_SKIP, -1, -1, NO_MOVEMENT_FLAGS,
						false, false, MISSIONAI_ATTACK_SPY, plot());
				return;
			}

			if (!bTargetCity)
			{
				// normal city handling

				if (getFortifyTurns() >= GC.getDefineINT(CvGlobals::MAX_FORTIFY_TURNS))
				{
					if (AI_espionageSpy())
					{
						return;
					}
				}
				// advc.034: Can take our time during disengagement
				else if(isIntruding())
				{
					// If we think we'll get caught soon, then do the mission early.
					int iInterceptChance = getSpyInterceptPercent(getPlot().getTeam(), false);
					iInterceptChance *= 100 +
							(GET_TEAM(getTeam()).isOpenBorders(getPlot().getTeam()) ?
							GC.getDefineINT(CvGlobals::ESPIONAGE_SPY_NO_INTRUDE_INTERCEPT_MOD) :
							GC.getDefineINT(CvGlobals::ESPIONAGE_SPY_INTERCEPT_MOD));
					iInterceptChance /= 100;
					if (SyncRandSuccess100(iInterceptChance + getFortifyTurns()))
					{
						if (AI_espionageSpy())
							return;
					}
				}
				//if (GC.getGame().getSorenRandNum(100, "AI Spy Skip Turn") > 5)
				// (advc: 95% may have been intended, but w/e ...)
				if (SyncRandSuccess100(94)) // don't wait forever
				{
					getGroup()->pushMission(MISSION_SKIP, -1, -1, NO_MOVEMENT_FLAGS,
							false, false, MISSIONAI_ATTACK_SPY, plot());
					return;
				}
			}
		}
	}

	// Do we have enough points on anyone for an attack mission to be useful?
	int iAttackChance = 0;
	int iTransportChance = 0;
	{
		int iScale = 100 * (kOwner.getCurrentEra() + 1);
		int iAttackSpies = kOwner.AI_areaMissionAIs(getArea(), MISSIONAI_ATTACK_SPY);
		int iLocalPoints = 0;
		int iTotalPoints = 0;

		if (kOwner.AI_isDoStrategy(AI_STRATEGY_ESPIONAGE_ECONOMY))
		{	// advc.120b: was 50*
			iScale += 80 * kOwner.getCurrentEra() * (kOwner.getCurrentEra() + 1);
		}

		for (int iI = 0; iI < MAX_CIV_TEAMS; iI++)
		{
			int iPoints = kTeam.getEspionagePointsAgainstTeam((TeamTypes)iI);
			iTotalPoints += iPoints;

			if (iI != getTeam() && GET_TEAM((TeamTypes)iI).isAlive() && kTeam.isHasMet((TeamTypes)iI) &&
				GET_TEAM((TeamTypes)iI).countNumCitiesByArea(getArea()) > 0)
			{
				int x = 100 * iPoints + iScale;
				x /= iPoints + (1 + iAttackSpies) * iScale;
				iAttackChance = std::max(iAttackChance, x);

				iLocalPoints += iPoints;
			}
		}
		if (//kTeam.getAnyWarPlanCount(true) == 0
			!GET_PLAYER(getOwner()).AI_isFocusWar(area())) // advc.105
		{
			iAttackChance /= 3;
		}
		if (getPlot().getArea().getAreaAIType(getTeam()) == AREAAI_DEFENSIVE)
			iAttackChance /= 2;
		if (kOwner.AI_atVictoryStage(AI_VICTORY_SPACE4) ||
			kOwner.AI_atVictoryStage(AI_VICTORY_CULTURE3))
		{
			iAttackChance /= 2;
		}
		iAttackChance *= GC.getInfo(kOwner.getPersonalityType()).getEspionageWeight();
		iAttackChance /= 100;
		// scale for game speed
		iAttackChance *= 100;
		iAttackChance /= GC.getGame().getSpeedPercent();

		iTransportChance = (100 * iTotalPoints - 130 * iLocalPoints) / std::max(1, iTotalPoints);
	}

	if (getPlot().getTeam() == getTeam())
	{
		if (!SyncRandSuccess100(iAttackChance))
		{
			if (SyncRandSuccess100(iTransportChance))
			{
				if (AI_load(UNITAI_SPY_SEA, MISSIONAI_LOAD_SPECIAL, NO_UNITAI,
					-1, -1, -1, 0, NO_MOVEMENT_FLAGS, 8))
				{
					return;
				}
			}
			if (AI_guardSpy(0))
			{
				return;
			}
		}

		if (!kOwner.AI_isDoStrategy(AI_STRATEGY_BIG_ESPIONAGE) &&
			//GET_TEAM(getTeam()).getAtWarCount(true) > 0 &&
			GET_PLAYER(getOwner()).AI_isFocusWar(area()) && // advc.105
			//SyncRandSuccess100(25)
			/*	advc (note): I guess the idea is to attack resources with a
				consistently high or low probability for as long as the
				strategies remain the same. */
			SyncRandSuccess100(kOwner.AI_getStrategyRand(5) % 36)) // K-Mod
		{
			if (AI_bonusOffenseSpy(6))
			{
				return;
			}
		}
		else
		{
			if (AI_cityOffenseSpy(10))
			{
				return;
			}
		}
	}

	if (AI_getGroup()->AI_getMissionAIType() == MISSIONAI_ATTACK_SPY &&
		getPlot().getNonObsoleteBonusType(getTeam(), true) != NO_BONUS &&
		getPlot().isOwned() && /* advc.003n: */ !getPlot().isBarbarian() &&
		kOwner.AI_isMaliciousEspionageTarget(getPlot().getOwner()))
	{
		// assume this is the target of our destroy improvement mission.
		if (getFortifyTurns() >= GC.getDefineINT(CvGlobals::MAX_FORTIFY_TURNS))
		{
			if (AI_espionageSpy())
			{
				return;
			}
		}
		if (SyncRandSuccess100(90))
		{
			getGroup()->pushMission(MISSION_SKIP, -1, -1, NO_MOVEMENT_FLAGS,
					false, false, MISSIONAI_ATTACK_SPY, plot());
			return;
		}
	}

	if (getArea().getNumCities() > getArea().getCitiesPerPlayer(getOwner()))
	{
		if (kOwner.AI_areaMissionAIs(getArea(), MISSIONAI_RECON_SPY) <=
			kOwner.AI_areaMissionAIs(getArea(), MISSIONAI_GUARD_SPY) + 1 &&
			(AI_getGroup()->AI_getMissionAIType() == MISSIONAI_RECON_SPY ||
			SyncRandSuccessRatio(2, 3)))
		{
			if (AI_reconSpy(3))
			{
				return;
			}
		}
		else
		{
			if (!SyncRandSuccess100(iAttackChance))
			{
				if (AI_guardSpy(0))
				{
					return;
				}
			}

			if (AI_cityOffenseSpy(20))
			{
				return;
			}
		}
	}

	//if (AI_load(UNITAI_SPY_SEA, MISSIONAI_LOAD_SPECIAL, NO_UNITAI, -1, -1, -1, 0, MOVE_NO_ENEMY_TERRITORY))
	if (AI_load(UNITAI_SPY_SEA, MISSIONAI_LOAD_SPECIAL))
		return;

	if (AI_retreatToCity())
	{
		return;
	}

	if (AI_safety())
	{
		return;
	}

	getGroup()->pushMission(MISSION_SKIP);
}


// doc
void CvUnitAI::AI_persecutorMove()
{
	CvCity* pTargetCity = AI_persecutionTarget();
	if (pTargetCity == NULL)
	{
		getGroup()->pushMission(MISSION_SKIP);
		return;
	}

	if (atPlot(pTargetCity->plot()) && canPersecute(getPlot()))
	{
		persecute(pTargetCity->AI().AI_getPersecutionReligion());
		return;
	}

	getGroup()->pushMission(MISSION_MOVE_TO, pTargetCity->getX(), pTargetCity->getY(), MOVE_SAFE_TERRITORY, false, true, NO_MISSIONAI, plot(), this);
}

// doc
CvCity* CvUnitAI::AI_persecutionTarget() const
{
	CvCity* pTargetCity = NULL;
	int iTargetDistance = MAX_INT;
	int iTargetValue = -1;

	FOR_EACH_CITY_VAR(pLoopCity, GET_PLAYER(getOwner()))
	{
		if (area() == pLoopCity->area() && generatePath(pLoopCity->getPlot()))
		{
			int iCurrentDistance = stepDistance(getX(), getY(), pLoopCity->getX(), pLoopCity->getY());
			int iCurrentValue = GET_PLAYER(getOwner()).AI_getPersecutionValue(pLoopCity->AI().AI_getPersecutionReligion());

			if (iCurrentValue > iTargetValue || (iCurrentValue >= 0 && iCurrentValue == iTargetValue && iCurrentDistance < iTargetDistance))
			{
				pTargetCity = pLoopCity;
				iTargetDistance = iCurrentDistance;
				iTargetValue = iCurrentValue;
			}
		}
	}

	return pTargetCity;
}

void CvUnitAI::AI_ICBMMove()
{
	PROFILE_FUNC();

	/*CvCity* pCity = getPlot().getPlotCity();
	if (pCity != NULL) {
		if (pCity->AI_isDanger()) {
			if (!pCity->AI_isDefended()) {
				if (AI_airCarrier())
					return;
			}
		}
	}*/

	if (AI_nuke()) // advc.650: Merged AI_nukeRange into a AI_nuke
	{
		return;
	}

	if (isCargo())
	{
		getGroup()->pushMission(MISSION_SKIP);
		return;
	}

	if (airRange() > 0)
	{
		// BETTER_BTS_AI_MOD, 04/25/10, jdog5000: Unit AI
		/*	(advc: Had been deleted entirely by K-Mod upon introducing
			AI_localDefenceStrength and AI_localAttackStrength. The BBAI code does
			seem unnecessary seeing that rebasing is considered in any case.) */
		/*if (GET_TEAM(getTeam()).isAirBase(getPlot())) {
			int iOurDefense = GET_TEAM(getTeam()).AI_getOurPlotStrength(plot(),0,true,false,true);
			int iEnemyOffense = GET_PLAYER(getOwner()).AI_getEnemyPlotStrength(plot(),2,false,false);
			if (4*iEnemyOffense > iOurDefense || iOurDefense == 0) {
				if (AI_airOffensiveCity())
					return; // Too risky, pull back.
			}
		}*/

		if (AI_missileLoad(UNITAI_MISSILE_CARRIER_SEA, 2, true))
		{
			return;
		}

		if (AI_missileLoad(UNITAI_MISSILE_CARRIER_SEA, 1, false))
		{
			return;
		}

		if (AI_getBirthmark() % 3 == 0)
		{
			if (AI_missileLoad(UNITAI_ATTACK_SEA, 0, false))
			{
				return;
			}
		}

		if (AI_airOffensiveCity())
		{
			return;
		}
	}

	getGroup()->pushMission(MISSION_SKIP);
}


void CvUnitAI::AI_workerSeaMove()
{
	PROFILE_FUNC();

	if (!getGroup()->canDefend())
	{
		// BETTER_BTS_AI_MOD, Unit AI, Efficiency, 08/20/09, jdog5000: was AI_getPlotDanger
		//if (GET_PLAYER(getOwner()).AI_isAnyPlotDanger(getPlot()))
		/*	advc.mnai (for performance, arguably; tagging advc.opt)
			Tbd.: Maybe plot danger should really be used; it's more accurate. */
		if (GET_PLAYER(getOwner()).AI_isAnyWaterDanger(getPlot()))
		{
			if (AI_retreatToCity())
			{
				return;
			}
		}
	}

	/* if (AI_improveBonus(0,20))
		return;
	if (AI_improveBonus(0,10))
		return;*/
	// disabled by K-Mod. .. obviously redundant.

	if (AI_improveBonus())
	{
		return;
	}

	if (isHuman())
	{
		FAssert(isAutomated());
		if (getPlot().getBonusType() != NO_BONUS)
		{
			if (getPlot().getOwner() == getOwner() || !getPlot().isOwned())
			{
				getGroup()->pushMission(MISSION_SKIP);
				return;
			}
		}
		FOR_EACH_ADJ_PLOT(getPlot())
		{
			if (pAdj->getBonusType() != NO_BONUS)
			{
				//if (pLoopPlot->isValidDomainForLocation(*this))
				if (isRevealedValidDomain(*pAdj)) // advc
				{
					getGroup()->pushMission(MISSION_SKIP);
					return;
				}
			}
		}
	}
	if (!isHuman() && AI_getUnitAIType() == UNITAI_WORKER_SEA)
	{
		CvCityAI const* pCity = getPlot().AI_getPlotCity();
		if (pCity != NULL && pCity->getOwner() == getOwner())
		{
			if (pCity->AI_neededSeaWorkers() == 0)
			{
				if (GC.getGame().getElapsedGameTurns() > 10 &&
					GET_PLAYER(getOwner()).calculateUnitCost() > 0)
				{
					scrap();
					return;
				}
			}
			else
			{	// Probably ice-locked since we can't perform any actions
				scrap();
				return;
			}
		}
	}

	if (AI_retreatToCity())
	{
		return;
	}

	if (AI_safety())
	{
		return;
	}

	getGroup()->pushMission(MISSION_SKIP);
}


void CvUnitAI::AI_barbAttackSeaMove()
{
	PROFILE_FUNC();
	// <advc.306> Assault mode until cargo delivered
	if (hasCargo())
	{
		// Opportunistic attack on Worker or empty city
		if (AI_barbAmphibiousCapture())
			return;
		if (AI_assaultSeaTransport())
			return;
		// Dump cargo anywhere if no assault target
		if (getPlot().isAdjacentToLand())
		{
			CvPlot* pDest = getPlot().getNearestLandPlot();
			if (pDest != NULL && generatePath(*pDest) && // pDest could be blocked
				AI_transportGoTo(getPathEndTurnPlot(), *pDest,
				NO_MOVEMENT_FLAGS, MISSIONAI_ASSAULT))
			{
				return;
			}
		}
	} // </advc.306>

	/*if (SyncRandOneChanceIn(2)) {
		if (AI_pillageRange(1))
			return;
	}
	if (AI_anyAttack(2, 25))
		return;
	if (AI_pillageRange(4))
		return;
	if (AI_heal())
		return;*/ // BtS
	// K-Mod
	if (AI_anyAttack(1, 51)) // safe attack
		return;

	if (AI_pillageRange(1)) // near pillage
		return;

	if (AI_heal())
		return;

	if (AI_anyAttack(1, 30)) // reckless attack
		return;

	if (SyncRandSuccess100(40) && AI_pillageRange(3)) // long pillage
		return;

	if (SyncRandSuccessRatio(15, 16) && AI_anyAttack(2, 45)) // chase
		return;

	// Barb ships will often blockade for a little while before moving on (BBAI)
	if ((GC.getGame().getGameTurn() + AI_getBirthmark()) % 12 > 5)
	{
		if (AI_pirateBlockade())
		{
			return;
		}
	}
	if (SyncRandOneChanceIn(3)) // (trap checking from BBAI)
	{
		// If trapped in small hole in ice or around tiny island, disband to allow other units to be generated
		bool bScrap = true;
		for (SquareIter it(*this, baseMoves() + 2); it.hasNext(); ++it)
		{
			CvPlot const& kLoopPlot = *it;
			//if (AI_plotValid(kLoopPlot)) { // advc: pathDestValid will handle it
			int iPathTurns;
			if (generatePath(kLoopPlot, NO_MOVEMENT_FLAGS, true, &iPathTurns) &&
				iPathTurns > 1)
			{
				bScrap = false;
				break;
			}
		}
		if (bScrap)
		{
			scrap();
			return;
		}
	}
	// K-Mod / BBAI end

	/*	<advc.306> Have ships retreat more often, so that they can receive cargo.
		Should also resolve an issue where Barbarian ships are indefinitely stuck
		patrolling an unowned stretch surrounded by borders. (Patrolling Barbarians
		avoid borders.) */
	bool const bMovingToSafety = (getGroup()->getMissionType(0) == MISSION_MOVE_TO);
	bool bAwaitCargo = (!bMovingToSafety && getPlot().isWater() &&
			!hasCargo() && !getPlot().isVisibleToCivTeam());
	if (bAwaitCargo)
	{
		bAwaitCargo = false;
		FOR_EACH_ADJ_PLOT(getPlot())
		{
			if (pAdj->isHabitable())
			{
				bAwaitCargo = true;
				break;
			}
		}
		/*	(Could consider suicide here if bAwaitCargo has become false.
			Unlikely to ever receive cargo. But we should also make sure
			that there are no resources we might want to go back to pillaging;
			that's no so easy to check ...) */
	}
	if (bMovingToSafety ||
		/*	May want to wait an extra turn or two if we think that we're
			ready for cargo. AI_safety will then skip since we're already safe. */
		SyncRandSuccess100(bAwaitCargo ? 53 : 24))
	{
		if (AI_safety())
		{
			return;
		}
	} // </advc.306>
	if (AI_patrol())
	{
		return;
	}

	if (AI_retreatToCity())
	{
		return;
	}

	if (AI_safety())
	{
		return;
	}

	getGroup()->pushMission(MISSION_SKIP);
	return;
}

// BETTER_BTS_AI_MOD, Pirate AI several changes, 02/23/10, jdog5000:
void CvUnitAI::AI_pirateSeaMove()
{
	PROFILE_FUNC();

	// heal in defended, unthreatened forts and cities
	CvPlot const& kPlot = getPlot();
	/*if ((kPlot.isCity() && kPlot.AI_getPlotCity()->AI_isSafe()) ||
		(kPlot.isCity(true) && GET_PLAYER(getOwner()).
		AI_localDefenceStrength(&kPlot, getTeam()) > 0 &&
		!GET_PLAYER(getOwner()).AI_isAnyPlotDanger(kPlot, 2, false)))*/
	// advc.139: Probably better than the above (which I had already tweaked)
	if (AI_isThreatenedFromLand() <= PROBABILITY_LOW)
	{
		if (AI_heal())
		{
			return;
		}
	}

	if (kPlot.isOwned() && kPlot.getTeam() == getTeam())
	{
		if (AI_anyAttack(2, 40))
		{
			return;
		}

		//if (AI_protect(30))
		if (AI_defendTerritory(45, NO_MOVEMENT_FLAGS, 3, true)) // K-Mod
		{
			return;
		}

		if (((AI_getBirthmark() / 8) % 2) == 0)
		{
			// Previously code actually blocked grouping
			if (AI_group(UNITAI_PIRATE_SEA, -1, 1, -1, true, false, false, 8))
			// BETTER_BTS_AI_MOD: END
			{
				return;
			}
		}
	}
	else
	{
		if (AI_anyAttack(2, 51))
		{
			return;
		}
	}

	if (SyncRandOneChanceIn(10))
	{
		CvArea* pWaterArea = kPlot.waterArea();
		if (pWaterArea != NULL)
		{
			if (pWaterArea->getNumUnrevealedTiles(getTeam()) > 0)
			{
				if (GET_PLAYER(getOwner()).AI_areaMissionAIs(
					*pWaterArea, MISSIONAI_EXPLORE, getGroup()) <
					GET_PLAYER(getOwner()).AI_neededExplorers(*pWaterArea))
				{
					if (AI_exploreRange(2))
					{
						return;
					}
				}
			}
		}
	}

	if (SyncRandOneChanceIn(11))
	{
		if (AI_pillageRange(1))
		{
			return;
		}
	}

	//Includes heal and retreat to sea routines.
	if (AI_pirateBlockade())
	{
		return;
	}

	if (AI_retreatToCity())
	{
		return;
	}

	if (AI_safety())
	{
		return;
	}

	getGroup()->pushMission(MISSION_SKIP);
}


void CvUnitAI::AI_attackSeaMove()
{
	PROFILE_FUNC();
	const CvPlayerAI& kOwner = GET_PLAYER(getOwner()); // K-Mod
	// BETTER_BTS_AI_MOD, Naval AI, 06/14/09, Solver & jdog5000: START
	if (AI_isThreatenedFromLand() >= PROBABILITY_REAL) // advc.139: Moved into subroutine
	{
		if (AI_anyAttack(2, 50))
		{
			return;
		}
		if (AI_shadow(UNITAI_ASSAULT_SEA, 4, 34, false, true, baseMoves()))
		{
			return;
		}
		//if (AI_protect(35, 0, 3))
		if (AI_defendTerritory(45, NO_MOVEMENT_FLAGS, 3, true)) // K-Mod
		{
			return;
		}
		// <advc.017b>
		CvArea* pWaterArea = getPlot().waterArea();
		if (pWaterArea != NULL)
		{
			if(getUnitInfo().getDefaultUnitAIType() == UNITAI_EXPLORE_SEA &&
				kOwner.AI_totalWaterAreaUnitAIs(*pWaterArea, UNITAI_EXPLORE_SEA) <
				kOwner.AI_neededExplorers(*pWaterArea))
			{
				AI_setUnitAIType(UNITAI_EXPLORE_SEA);
			}
		} // </advc.017b>
		if (AI_retreatToCity())
		{
			return;
		}
		if (AI_safety())
		{
			return;
		}
	} // BETTER_BTS_AI_MOD: END

	if (AI_heal(30, 1))
	{
		return;
	}

	if (AI_anyAttack(1, 35))
	{
		return;
	}

	if (AI_anyAttack(2, 40))
	{
		return;
	}

	if (AI_seaBombardRange(6))
	{
		return;
	}

	if (AI_heal(50, 3))
	{
		return;
	}

	if (AI_heal())
	{
		return;
	}
	// BETTER_BTS_AI_MOD, Naval AI, 08/10/09, jdog5000: START
	// BBAI TODO: Turn this into a function, have docked escort ships do it too
	CvCity* pCity = getPlot().getPlotCity();
	if (pCity != NULL)
	{
		if (pCity->isBlockaded())
		{
			// City under blockade
			// Attacker has low odds since anyAttack checks above passed, try to break if sufficient numbers

			int iAttackers = getPlot().plotCount(PUF_isUnitAIType, UNITAI_ATTACK_SEA, -1, NO_PLAYER, getTeam());
			// advc.114a: Why count only group heads? Need to count all attackers!
					//PUF_isGroupHead, -1, -1);
			// advc (tbd.): Use AI_getPlotDanger? It's more accurate but slower.
			int iBlockaders = kOwner.AI_getWaterDanger(getPlot(), 4);
			//if (iAttackers > iBlockaders + 2)
			// advc.114a: Replacing the above
			if (2 * iAttackers >= 3 * iBlockaders && iBlockaders > 0)
			{
				if (iAttackers > SyncRandNum(2 * iBlockaders + 1))
				{	// BBAI TODO: Make odds scale by # of blockaders vs number of attackers
					/*  <advc.114a>: Exactly. Attack regardless of odds when
						outnumbering them 5:1; 1% at 3:1; 22% at 2:1; 33% at 1.5:1.
						Those are chancy odds, but don't want CvCityAI to build any
						more (outdated) ships than necessary; they won't have much
						of a future use. Also, blockading units can't usually heal;
						not imperative to destroy them in one turn. In fact, damaging
						them may be enough to drive them off. */
					scaled rAttackerRatio(iAttackers, iBlockaders);
					scaled rOddsThresh;
					if (rAttackerRatio < 5 && rAttackerRatio >= 3)
						rOddsThresh = 1;
					if (rAttackerRatio < 3)
						rOddsThresh = (5 - rAttackerRatio).pow(fixp(2.8));
					if (AI_anyAttack(1, rOddsThresh.round()))
					//if (AI_anyAttack(1, 15)) // </advc.114a>
					{
						return;
					}
				}
			}
		}
	} // BETTER_BTS_AI_MOD: END

	if (AI_group(UNITAI_CARRIER_SEA, /*iMaxGroup*/ 4, 1, -1, true, false, false, /*iMaxPath*/ 5))
	{
		return;
	}

	if (AI_group(UNITAI_ATTACK_SEA, /*iMaxGroup*/ 1, -1, -1, true, false, false, /*iMaxPath*/ 3))
	{
		return;
	}

	if (!getPlot().isOwned() || !isEnemy(getPlot()))
	{
		/*if (AI_shadow(UNITAI_ASSAULT_SEA, 4, 34))
			return;
		if (AI_shadow(UNITAI_CARRIER_SEA, 4, 51))
			return;
		if (AI_group(UNITAI_ASSAULT_SEA, -1, 4, -1, false, false, false))
			return;
	}
	if (AI_group(UNITAI_CARRIER_SEA, -1, 1, -1, false, false, false))
		return;*/ // BtS
		// K-Mod / BBAI. I've changed the order of group / shadow.
		// What I'd really like is to join the assault group if the group needs escorts, but shadow if it doesn't.

		// Get at least one shadow per assault group.
		if (AI_shadow(UNITAI_ASSAULT_SEA, 1, -1, true, false, 4))
		{
			return;
		}

		// Allow several attack_sea with large flotillas
		if (AI_group(UNITAI_ASSAULT_SEA, -1, 4, 4, false, false, false, 4, false, true, false))
		{
			return;
		}

		// allow just a couple with small asault teams
		if (AI_group(UNITAI_ASSAULT_SEA, -1, 2, -1, false, false, false, 5, false, true, false))
		{
			return;
		}

		// Otherwise, try to shadow.
		if (AI_shadow(UNITAI_ASSAULT_SEA, 4, 34, true, false, 4))
		{
			return;
		}

		if (AI_shadow(UNITAI_CARRIER_SEA, 4, 51, true, false, 5))
		{
			return;
		}
	}

	if (AI_group(UNITAI_CARRIER_SEA, -1, 1, -1, false, false, false, 10))
	{
		return;
	}
	// K-Mod / BBAI end

	if (getPlot().isOwned() && isEnemy(getPlot()) &&
		// advc.033: Don't blockade Barbarian cities
		getPlot().getTeam() != BARBARIAN_TEAM)
	{
		if (AI_blockade())
		{
			return;
		}
	}

	if (AI_pillageRange(4))
	{
		return;
	}

	//if (AI_protect(35))
	if (AI_defendTerritory(40, NO_MOVEMENT_FLAGS, 8)) // K-Mod
	{
		return;
	}

	if (AI_travelToUpgradeCity())
	{
		return;
	}

	// K-Mod
	if (AI_guardBonus(10))
		return;

	if (AI_getBirthmark()%2 == 0 && AI_guardCoast()) // I want some attackSea units to just patrol the area.
		return;
	// K-Mod end

	if (AI_patrol())
	{
		return;
	}

	if (AI_retreatToCity())
	{
		return;
	}

	if (AI_safety())
	{
		return;
	}

	getGroup()->pushMission(MISSION_SKIP);
}


void CvUnitAI::AI_reserveSeaMove()
{
	PROFILE_FUNC();
	const CvPlayerAI& kOwner = GET_PLAYER(getOwner()); // K-Mod
	// BETTER_BTS_AI_MOD, Naval AI, 06/14/09, Solver & jdog5000: START
	if(AI_isThreatenedFromLand() >= PROBABILITY_REAL) // advc.139: Moved into subroutine
	{
		if (AI_anyAttack(2, 60))
		{
			return;
		}
		//if (AI_protect(40))
		if (AI_defendTerritory(45, NO_MOVEMENT_FLAGS, 3, true)) // K-Mod
		{
			return;
		}
		if (AI_shadow(UNITAI_SETTLER_SEA, 2, -1, false, true, baseMoves()))
		{
			return;
		}
		if (AI_retreatToCity())
		{
			return;
		}
		if (AI_safety())
		{
			return;
		}
	} // BETTER_BTS_AI_MOD: END

	/*  <advc.017b> Defend bonus if it's threatened, otherwise, consider a bunch of
		other activities first. (K-Mod's AI_guardBonus(15) moved down instead.)
		Tbd.: Use PlotDanger instead? More accurate but slower. */
	if(kOwner.AI_isAnyWaterDanger(
		getPlot(), std::min(maxMoves(), CvPlayerAI::DANGER_RANGE)) &&
		AI_guardBonus(10))
	{
		return;
	} // </advc.017b>
	if (AI_heal(30, 1))
	{
		return;
	}

	if (AI_anyAttack(1, 55))
	{
		return;
	}

	if (AI_seaBombardRange(6))
	{
		return;
	}

	//if (AI_protect(40))
	if (AI_defendTerritory(45, NO_MOVEMENT_FLAGS, 5)) // K-Mod
	{
		return;
	}

	/*if (AI_shadow(UNITAI_SETTLER_SEA, 1, -1, true))
		return;
	if (AI_group(UNITAI_RESERVE_SEA, 1))
		return;
	if (bombardRate() > 0) {
		if (AI_shadow(UNITAI_ASSAULT_SEA, 2, 30, true))
			return;
	}*/ // BtS
	// Shadow any nearby settler sea transport out at sea
	if (AI_shadow(UNITAI_SETTLER_SEA, 2, -1, false, true, 5))
	{
		return;
	}

	if (AI_group(UNITAI_RESERVE_SEA, 1, -1, -1, false, false, false, 8))
	{
		return;
	}

	if (bombardRate() > 0)
	{
		if (AI_shadow(UNITAI_ASSAULT_SEA, 2, 30, true, false, 8))
		{
			return;
		}
	}

	if (AI_heal(50, 3))
	{
		return;
	}

	//if (AI_protect(40))
	if (AI_defendTerritory(45, NO_MOVEMENT_FLAGS, -1)) // K-Mod
	{
		return;
	}

	if (AI_anyAttack(3, 45))
	{
		return;
	}

	if (AI_heal())
	{
		return;
	}

	if (!isNeverInvisible())
	{
		if (AI_anyAttack(5, 35))
		{
			return;
		}
	}
	/*  BETTER_BTS_AI_MOD, Naval AI, 01/03/09, jdog5000: START
		Shadow settler transport with cargo */
	if (AI_shadow(UNITAI_SETTLER_SEA, 1, -1, true, false, 10))
	{
		return;
	} // BETTER_BTS_AI_MOD: END
	// advc.017b: Moved this down
	if (AI_guardBonus(15)) // K-Mod (note: this will defend seafood when we have exactly 1 of them)
	{
		return;
	}

	if (AI_travelToUpgradeCity())
	{
		return;
	}

	// K-Mod
	if (AI_guardBonus(10))
		return;

	if (AI_guardCoast())
		return;
	// K-Mod end

	if (AI_patrol())
	{
		return;
	}

	if (AI_retreatToCity())
	{
		return;
	}

	if (AI_safety())
	{
		return;
	}

	getGroup()->pushMission(MISSION_SKIP);
}


void CvUnitAI::AI_escortSeaMove()
{
	PROFILE_FUNC();

	/*//if we have cargo, possibly convert to UNITAI_ASSAULT_SEA (this will most often happen with galleons)
	//note, this should not happen when we are not the group head, so escort galleons are fine joining a group, just not as head
	if (hasCargo() && (getUnitAICargo(UNITAI_ATTACK_CITY) > 0 || getUnitAICargo(UNITAI_ATTACK) > 0))
	{ ... }*/ /* advc: Deleted the rest. The BtS expansion had added this
		fragment, already commented out (unfinished?). I think the BBAI code below
		(from 9/14/08) handles this. */
	const CvPlayerAI& kOwner = GET_PLAYER(getOwner()); // K-Mod

	// BETTER_BTS_AI_MOD, Naval AI, 06/14/09, Solver & jdog5000
	if (AI_isThreatenedFromLand() >= PROBABILITY_REAL) // advc.139: Moved into subroutine
	{
		if (AI_anyAttack(1, 60))
		{
			return;
		}
		if (AI_group(UNITAI_ASSAULT_SEA, -1, 1, -1, true, false, false, getMoves()))
		{
			return;
		}
		if (AI_retreatToCity())
		{
			return;
		}
		if (AI_safety())
		{
			return;
		}
	} // BETTER_BTS_AI_MOD: END

	if (AI_heal(30, 1))
	{
		return;
	}

	if (AI_anyAttack(1, 55))
	{
		return;
	}
	// BETTER_BTS_AI_MOD, Naval AI, 9/14/08, jdog5000: START
	// Galleons can get stuck with this AI type since they don't upgrade to any escort unit
	// Galleon escorts are much less useful once Frigates or later are available
	if (!isHuman() && !isBarbarian())
	{
		if (getCargo() > 0 && GC.getInfo(getUnitType()).getSpecialCargo() == NO_SPECIALUNIT)
		{
			//Obsolete?
			int iValue = kOwner.AI_unitValue(getUnitType(), AI_getUnitAIType(), area());
			int iBestValue = kOwner.AI_bestAreaUnitAIValue(AI_getUnitAIType(), area());

			if (iValue < iBestValue)
			{
				if (kOwner.AI_unitValue(getUnitType(), UNITAI_ASSAULT_SEA, area()) > 0)
				{
					AI_setUnitAIType(UNITAI_ASSAULT_SEA);
					return;
				}

				if (kOwner.AI_unitValue(getUnitType(), UNITAI_SETTLER_SEA, area()) > 0)
				{
					AI_setUnitAIType(UNITAI_SETTLER_SEA);
					return;
				}

				scrap();
				return; // advc.001: Always return after scrap
			}
		}
	} // BETTER_BTS_AI_MOD: END

	if (AI_group(UNITAI_CARRIER_SEA, -1, /*iMaxOwnUnitAI*/ 0, -1, /*bIgnoreFaster*/ true))
	{
		return;
	}

	if (AI_group(UNITAI_ASSAULT_SEA, -1, /*iMaxOwnUnitAI*/ 0, -1, /*bIgnoreFaster*/ true, false, false, /*iMaxPath*/ 3))
	{
		return;
	}

	if (AI_heal(50, 3))
	{
		return;
	}

	if (AI_pillageRange(2))
	{
		return;
	}

	//if (AI_group(UNITAI_MISSILE_CARRIER_SEA, 1, 1, true))
	if (AI_group(UNITAI_MISSILE_CARRIER_SEA, 1, 1, -1, true)) // K-Mod. (presumably this is what they meant)
	{
		return;
	}

	if (AI_group(UNITAI_ASSAULT_SEA, 1, /*iMaxOwnUnitAI*/ 0, /*iMinUnitAI*/ -1, /*bIgnoreFaster*/ true))
	{
		return;
	}

	if (AI_group(UNITAI_ASSAULT_SEA, -1, /*iMaxOwnUnitAI*/ 2, /*iMinUnitAI*/ -1, /*bIgnoreFaster*/ true))
	{
		return;
	}

	if (AI_group(UNITAI_CARRIER_SEA, -1, /*iMaxOwnUnitAI*/ 2, /*iMinUnitAI*/ -1, /*bIgnoreFaster*/ true))
	{
		return;
	}
	/*if (AI_group(UNITAI_ASSAULT_SEA, -1, 4, -1, true))
		return;*/ // BtS
	// BETTER_BTS_AI_MOD, Naval AI, 01/01/09, jdog5000: START
	// Group only with large flotillas first
	if (AI_group(UNITAI_ASSAULT_SEA, -1, /*iMaxOwnUnitAI*/ 4, /*iMinUnitAI*/ 3, /*bIgnoreFaster*/ true))
	{
		return;
	}

	if (AI_shadow(UNITAI_SETTLER_SEA, 2, -1, false, true, 4))
	{
		return;
	}
	// BETTER_BTS_AI_MOD: END
	if (AI_heal())
	{
		return;
	}

	if (AI_travelToUpgradeCity())
	{
		return;
	}
	// BETTER_BTS_AI_MOD, Naval AI, 04/18/10, jdog5000: START
	// If nothing else useful to do, escort nearby large flotillas even if they're faster
	// Gives Caravel escorts something to do during the Galleon/pre-Frigate era
	if (AI_group(UNITAI_ASSAULT_SEA, -1, /*iMaxOwnUnitAI*/ 4, /*iMinUnitAI*/ 3, /*bIgnoreFaster*/ false, false, false, 4, false, true))
	{
		return;
	}

	if (AI_group(UNITAI_ASSAULT_SEA, -1, /*iMaxOwnUnitAI*/ 2, /*iMinUnitAI*/ -1, /*bIgnoreFaster*/ false, false, false, 1, false, true))
	{
		return;
	}

	// Pull back to primary area if it's not too far so primary area cities know you exist
	// and don't build more, unnecessary escorts
	/*if (AI_retreatToCity(true,false,6))
		return;*/ // BtS
	// K-Mod. We don't want to actually end our turn inside the city...
	if (AI_guardCoast(true))
		return;
	// K-Mod end
	// BETTER_BTS_AI_MOD: END
	if (AI_retreatToCity())
	{
		return;
	}

	if (AI_safety())
	{
		return;
	}

	getGroup()->pushMission(MISSION_SKIP);
}


void CvUnitAI::AI_exploreSeaMove()
{
	PROFILE_FUNC();
	const CvPlayerAI& kOwner = GET_PLAYER(getOwner()); // K-Mod
	// BETTER_BTS_AI_MOD, Naval AI, 10/21/08, Solver & jdog5000: START
	if (AI_isThreatenedFromLand() >= PROBABILITY_REAL) // advc.139: Moved into subroutine
	{
		if (!isHuman())
		{
			if (AI_anyAttack(1, 60))
				return;
		}
		if (AI_retreatToCity())
			return;
		if (AI_safety())
			return;
	} // BETTER_BTS_AI_MOD: END

	if (!isHuman())
	{
		if (AI_anyAttack(1, 60))
			return;
	}

	// (advc.017b: Moved the transform/ scrap block down; try nearby exploration first.)

	// <advc.299> Instead of simply healing while getDamage() > 0
	if (AI_singleUnitHeal(3, 5))
		return; // </advc.299>

	if (!isHuman())
	{
		if (AI_pillageRange(1))
			return;
	}

	// doc: proactive coastline exploration
	if (AI_exploreCoasts())
		return;
    // doc: proactive circumnavigation
	if (AI_exploreCircumnavigate())
		return;

	if (AI_exploreRange(4))
		return;

	if (!isHuman())
	{
		if (AI_pillageRange(4))
			return;
	}
	// advc.017b: Moved this chunk of code down (and rewrote much of it)
	bool bExcessExplorers = false;
	// (Would be nice to check getPlot().secondWaterArea as well, but that takes extra time.)
	CvArea* pWaterArea = getPlot().waterArea();
	if (!isHuman() && !isBarbarian()) //XXX move some of this into a function? maybe useful elsewhere
	{	// <advc.017b>
		bool bTransform = false;
		// Don't be too quick to decide that there are too many explorers
		if (SyncRandSuccess100(13))
		{
			bTransform = kOwner.AI_isExcessSeaExplorers(*pWaterArea);
			bExcessExplorers = bTransform;
		}
		if (!bTransform &&
			/*  In the early game, it'll often take a better explorer (Galley
				vs Work Boat) too long to reach an unexplored area; better to
				let the outdated explorer continue. */
			kOwner.AI_getCurrEraFactor() > 1 &&
			kOwner.AI_isOutdatedUnit(getUnitType(), UNITAI_EXPLORE_SEA, pWaterArea))
		{
			bTransform = true;
		}
		// Moved the obsoletion test; now only required for scrapping
		if (bTransform) // </advc.017b>
		{
			// <advc> Made this more concise (original code deleted)
			std::vector<UnitAITypes> transformTypes;
			transformTypes.push_back(UNITAI_WORKER_SEA);
			transformTypes.push_back(UNITAI_PIRATE_SEA);
			AreaAITypes eAreaAI = getArea().getAreaAIType(getTeam());
			if(eAreaAI == AREAAI_ASSAULT || eAreaAI == AREAAI_ASSAULT_ASSIST ||
				eAreaAI == AREAAI_ASSAULT_MASSING ||
				kOwner.AI_totalUnitAIs(UNITAI_SETTLE) <= 0 ||
				kOwner.AI_totalUnitAIs(UNITAI_SETTLER_SEA) >
				kOwner.AI_getCurrEraFactor() / 2)
			{
				transformTypes.push_back(UNITAI_ASSAULT_SEA);
				transformTypes.push_back(UNITAI_SETTLER_SEA);
			}
			else
			{
				transformTypes.push_back(UNITAI_SETTLER_SEA);
				transformTypes.push_back(UNITAI_ASSAULT_SEA);
			}
			// <advc.017b> Instead of always trying MISSIONARY_SEA before RESERVE_SEA
			if ((kOwner.AI_totalUnitAIs(UNITAI_MISSIONARY) > 0 ||
					kOwner.AI_isDoStrategy(AI_STRATEGY_MISSIONARY)) &&
					kOwner.AI_totalUnitAIs(UNITAI_MISSIONARY_SEA) <= 1)
			{
				transformTypes.push_back(UNITAI_MISSIONARY_SEA);
				transformTypes.push_back(UNITAI_RESERVE_SEA);
			}
			else
			{
				transformTypes.push_back(UNITAI_RESERVE_SEA);
				transformTypes.push_back(UNITAI_MISSIONARY_SEA);
			} // </advc.017b>
			for (size_t i = 0; i < transformTypes.size(); i++)
			{
				if (getUnitInfo().getUnitAIType(transformTypes[i]) &&
					kOwner.AI_unitValue(getUnitType(), transformTypes[i], pWaterArea) > 0)
				{
					// Before transforming a Work Boat, check if there is sth. to improve.
					if(transformTypes[i] == UNITAI_WORKER_SEA &&
						/*  Costly (checks all tiles on the map), but this is the
							last check before changing the AI type. And exploring
							Work Boats are an early-game thing. */
						kOwner.AI_countUnimprovedBonuses(*pWaterArea, plot(), 5) <= 0)
					{
						continue;
					}
					AI_setUnitAIType(transformTypes[i]);
					AI_update();
					return;
				}
			} // </advc>
			// <advc.017b>
			int iValue = kOwner.AI_unitValue(getUnitType(), AI_getUnitAIType(), pWaterArea);
			int iBestValue = kOwner.AI_bestAreaUnitAIValue(AI_getUnitAIType(), pWaterArea);
			if (iValue < iBestValue)
			{
				scrap();
				return;
			}
		} // </advc.017b>
	}

	if (AI_explore())
		return;

	if (!isHuman())
	{
		if (AI_pillage())
			return;
	}

	if (!isHuman())
	{
		if (AI_travelToUpgradeCity())
			return;
	}

	if (!isHuman() && AI_getUnitAIType() == UNITAI_EXPLORE_SEA &&
		pWaterArea != NULL && bExcessExplorers) // advc.017b
	{
		if (kOwner.calculateUnitCost() > 0)
		{
			scrap();
			return;
		}
	}

	if (AI_patrol())
		return;

	if (AI_retreatToCity())
		return;

	if (AI_safety())
		return;

	getGroup()->pushMission(MISSION_SKIP);
}


void CvUnitAI::AI_assaultSeaMove()
{
	PROFILE_FUNC();
	FAssert(AI_getUnitAIType() == UNITAI_ASSAULT_SEA);

	CvPlayerAI const& kOwner = GET_PLAYER(getOwner()); // K-Mod
	bool bEmpty = !getGroup()->hasCargo();
	// BETTER_BTS_AI_MOD, Naval AI, 04/18/10, jdog5000: START
	bool bFull = getGroup()->getCargo() > 0 && AI_getGroup()->AI_isFull();
	// advc.139: Moved into subroutine
	ProbabilityTypes eThreatFromLand = AI_isThreatenedFromLand();
	//if (4 * iEnemyOffense > iOurDefense) // was 8 vs 1
	if (eThreatFromLand >= PROBABILITY_LOW)
	{
		//if (2 * iEnemyOffense > iOurDefense) // was 4 vs 1
		if (eThreatFromLand >= PROBABILITY_REAL)
		{
			if (!bEmpty)
				getGroup()->unloadAll();
			if (AI_anyAttack(1, 65))
				return;
			// Retreat to primary area first
			if (AI_retreatToCity(true))
				return;
			if (AI_retreatToCity())
				return;
			if (AI_safety())
				return;
		}
		if (!bFull && !bEmpty)
		{
			getGroup()->unloadAll();
			getGroup()->pushMission(MISSION_SKIP);
			return;
		}
	}

	if (bEmpty)
	{
		if (AI_anyAttack(1, 65))
			return;
		/*if (AI_anyAttack(1, 45))
			return;*/ // disabled by K-Mod. (redundant)
	}

	bool bReinforce = false;
	bool bAttack = false;
	bool const bNoWarPlans = !GET_TEAM(getTeam()).AI_isAnyWarPlan();
	//bool bLandWar = false;
	bool const bBarbarian = isBarbarian();

	// Cargo if already at war
	//int iTargetReinforcementSize = (bBarbarian ? AI_stackOfDoomExtra() : 2); // BBAI
	scaled rTargetReinforcementSize = (bBarbarian ? 2 : AI_stackOfDoomExtra()); // K-Mod. =\
	// K-Mod. If we are already en route for invasion, decrease the threshold.
	// (One reason for this decrease is that the threshold may actually increase midway through the journey. We don't want to turn back because of that!)
	if (AI_getGroup()->AI_getMissionAIType() == MISSIONAI_ASSAULT)
		rTargetReinforcementSize *= fixp(2/3.);
	// K-Mod end
	// Cargo to launch a new invasion
	scaled rTargetInvasionSize = 2 * rTargetReinforcementSize;
	// <advc>
	int iTargetReinforcementSize = rTargetReinforcementSize.round();
	int iTargetInvasionSize = rTargetInvasionSize.round(); // </advc>

	int iCargo = getGroup()->getCargo();
	int iEscorts = getGroup()->countNumUnitAIType(UNITAI_ESCORT_SEA) +
			getGroup()->countNumUnitAIType(UNITAI_ATTACK_SEA);

	AreaAITypes eAreaAIType = getArea().getAreaAIType(getTeam());
	//bLandWar = !bBarbarian && ((eAreaAIType == AREAAI_OFFENSIVE) || (eAreaAIType == AREAAI_DEFENSIVE) || (eAreaAIType == AREAAI_MASSING));
	bool bLandWar = !bBarbarian && kOwner.AI_isLandWar(getArea()); // K-Mod
	bool const bInPort = GET_TEAM(getTeam()).isBase(getPlot()); // advc (was bCity)

	// Plot danger case handled above

	if (hasCargo() && (getUnitAICargo(UNITAI_SETTLE) > 0 || getUnitAICargo(UNITAI_WORKER) > 0))
	{
		// Dump inappropriate load at first opportunity after pick up
		if (bInPort && getPlot().getOwner() == getOwner())
		{
			getGroup()->unloadAll();
			/*getGroup()->pushMission(MISSION_SKIP);
			return;*/ // BtS
			iCargo = 0; // K-Mod. I see no need to skip.
		}
		else
		{
			if (!isFull())
			{
				if(AI_pickupStranded(NO_UNITAI, 1))
					return;
			}
			if (AI_retreatToCity(true))
				return;
			if (AI_retreatToCity())
				return;
		}
	}

	if (bInPort)
	{
		CvCityAI const* pCity = getPlot().AI_getPlotCity();
		if (pCity != NULL && getPlot().getOwner() == getOwner())
		{
			// split out galleys from stack of ocean capable ships
			if (getGroup()->getNumUnits() > 1 &&
				!kOwner.AI_isAnyImpassable(getUnitType()))
			{
				//AI_getGroup()->AI_separateImpassable();
				// K-Mod
				if (AI_getGroup()->AI_separateImpassable())
				{
					// recalculate cached variables.
					bEmpty = !getGroup()->hasCargo();
					bFull = getGroup()->getCargo() > 0 && AI_getGroup()->AI_isFull();
					iCargo = getGroup()->getCargo();
					iEscorts = getGroup()->countNumUnitAIType(UNITAI_ESCORT_SEA) +
							getGroup()->countNumUnitAIType(UNITAI_ATTACK_SEA);
				}
				// K-Mod end
			}

			// galleys with upgrade available should get that ASAP
			if (kOwner.AI_isAnyImpassable(getUnitType()))
			{
				CvCity* pUpgradeCity = getUpgradeCity(false);
				if (pUpgradeCity != NULL && pUpgradeCity == pCity)
				{
					// Wait for upgrade, this unit is top upgrade priority
					getGroup()->pushMission(MISSION_SKIP);
					return;
				}
			}
		}

		if (iCargo > 0 && pCity != NULL &&
			GC.getGame().getGameTurn() - pCity->getGameTurnAcquired() <= 1 &&
			pCity->getPreviousCiv() != NO_CIVILIZATION)
		{
			/*	Just captured city, probably from naval invasion.
				If area targets, drop cargo and leave so as to not to be lost in quick counter attack */
			if (GET_TEAM(getTeam()).AI_countEnemyPowerByArea(getPlot().getArea()) > 0)
			{
				getGroup()->unloadAll();
				if (iEscorts > 2)
				{
					if (getGroup()->countNumUnitAIType(UNITAI_ESCORT_SEA) > 1 &&
						getGroup()->countNumUnitAIType(UNITAI_ATTACK_SEA) > 0)
					{
						AI_getGroup()->AI_separateAI(UNITAI_ATTACK_SEA);
						AI_getGroup()->AI_separateAI(UNITAI_RESERVE_SEA);
						iEscorts = getGroup()->countNumUnitAIType(UNITAI_ESCORT_SEA);
					}
				}
				iCargo = getGroup()->getCargo();
			}
		}

		if (iCargo > 0 && iEscorts == 0)
		{
			if (AI_group(UNITAI_ASSAULT_SEA,-1,-1,-1,
				/*bIgnoreFaster*/true,false,false,
				/*iMaxPath*/1,false,
				/*bCargoOnly*/true,false,MISSIONAI_ASSAULT))
			{
				return;
			}

			if (getPlot().plotCount(PUF_isUnitAIType, UNITAI_ESCORT_SEA, -1,
				getOwner(), NO_TEAM, PUF_isGroupHead, -1, -1) > 0)
			{
				// Loaded but with no escort, wait for escorts in plot to join us
				getGroup()->pushMission(MISSION_SKIP);
				return;
			}

			MissionAITypes eMissionAIType = MISSIONAI_GROUP;
			if (kOwner.AI_isAnyUnitTargetMissionAI(*this, &eMissionAIType, 1, getGroup(), 3) ||
				// advc (tbd.): Use PlotDanger instead? More accurate but slower.
				kOwner.AI_isAnyWaterDanger(getPlot(), 4))
			{
				// Loaded but with no escort, wait for others joining us soon or avoid dangerous waters
				getGroup()->pushMission(MISSION_SKIP);
				return;
			}
		}
		/*	<advc.082> One fewer will do if we're full.
			(Duplicated in the !bInPort branch below.) */
		if (bFull && iCargo >= 3)
		{
			if (iCargo == iTargetReinforcementSize - 1)
				iTargetReinforcementSize--;
			if (iCargo == iTargetInvasionSize - 1)
				iTargetInvasionSize--;
		} // </advc.082>

		if (bLandWar)
		{
			if (iCargo > 0)
			{
				if (eAreaAIType == AREAAI_DEFENSIVE ||
					(pCity != NULL && pCity->AI_isDanger()))
				{
					/*	Unload cargo when on defense or if small load of troops
						and can reach enemy city over land (generally less risky) */
					getGroup()->unloadAll();
					getGroup()->pushMission(MISSION_SKIP);
					return;
				}
			}

			if (iCargo >= iTargetReinforcementSize)
			{
				AI_getGroup()->AI_separateEmptyTransports();
				if (!getGroup()->hasCargo())
				{
					// this unit was empty group leader
					//getGroup()->pushMission(MISSION_SKIP);
					//return;
					// K-Mod. (and I've made a second if iCargo > thing)
					FAssert(getGroup()->getNumUnits() == 1);
					iCargo = 0;
					iEscorts = 0;
				}
			}
			if (iCargo >= iTargetReinforcementSize)
			{
				// Send ready transports
				if (AI_assaultSeaReinforce(false))
					return;
				// if(iCargo >= iTargetInvasionSize)
				// Disabled by K-Mod. (otherwise groups trying to take a short-cut by boat will get stuck.)
				{
					if (AI_assaultSeaTransport(false, true))
						return;
				}
			}
		}
		else
		{
			if (eAreaAIType == AREAAI_ASSAULT && iCargo >= iTargetInvasionSize)
				bAttack = true;
			if (eAreaAIType == AREAAI_ASSAULT || eAreaAIType == AREAAI_ASSAULT_ASSIST)
			{
				if ((bFull && iCargo > cargoSpace()) ||
					iCargo >= iTargetReinforcementSize)
				{
					bReinforce = true;
				}
			}
		}

		/*if (!bAttack && !bReinforce && getPlot().getTeam() == getTeam()) {
			if (iEscorts > 3 && iEscorts > 2 * getGroup()->countNumUnitAIType(UNITAI_ASSAULT_SEA)) {
				// If we have too many escorts, try freeing some for others
				getGroup()->AI_separateAI(UNITAI_ATTACK_SEA);
				getGroup()->AI_separateAI(UNITAI_RESERVE_SEA);
				iEscorts = getGroup()->countNumUnitAIType(UNITAI_ESCORT_SEA);
				if (iEscorts > 3 && iEscorts > 2 * getGroup()->countNumUnitAIType(UNITAI_ASSAULT_SEA))
					getGroup()->AI_separateAI(UNITAI_ESCORT_SEA);
			}
		}*/ // BBAI
		/*	K-Mod, same purpose, different implementation.
			Keep ungrouping escort units until we don't have too many. */
		if (!bAttack && !bReinforce && getPlot().getTeam() == getTeam())
		{
			int iAssaultUnits = getGroup()->countNumUnitAIType(UNITAI_ASSAULT_SEA);
			CLLNode<IDInfo>* pNode = getGroup()->headUnitNode();
			while (iEscorts > 3 && iEscorts > 2*iAssaultUnits &&
				iEscorts > 2*iCargo && pNode != NULL)
			{
				CvUnit* pLoopUnit = ::getUnit(pNode->m_data);
				pNode = getGroup()->nextUnitNode(pNode);
				// (maybe we should adjust this to ungroup "escorts" last?)
				if (!pLoopUnit->hasCargo())
				{
					switch (pLoopUnit->AI_getUnitAIType())
					{
					case UNITAI_ATTACK_SEA:
					case UNITAI_RESERVE_SEA:
					case UNITAI_ESCORT_SEA:
						pLoopUnit->joinGroup(NULL);
						iEscorts--;
						break;
					default:
						break;
					}
				}
			}
			FAssert(!(iEscorts > 3 && iEscorts > 2 * iAssaultUnits && iEscorts > 2 * iCargo));
		} // K-Mod end

		MissionAITypes eMissionAIType = MISSIONAI_GROUP;
		if (kOwner.AI_isAnyUnitTargetMissionAI(*this, &eMissionAIType, 1, getGroup(), 1))
		{
			// Wait for units which are joining our group this turn
			getGroup()->pushMission(MISSION_SKIP);
			return;
		}

		if (!bFull)
		{
			if (bAttack)
			{
				eMissionAIType = MISSIONAI_LOAD_ASSAULT;
				if (kOwner.AI_isAnyUnitTargetMissionAI(*this, &eMissionAIType, 1, getGroup(), 1))
				{
					// Wait for cargo which will load this turn
					getGroup()->pushMission(MISSION_SKIP);
					return;
				}
			}
			else if (kOwner.AI_isAnyUnitTargetMissionAI(*this, MISSIONAI_LOAD_ASSAULT))
			{
				// Wait for cargo which is on the way
				getGroup()->pushMission(MISSION_SKIP);
				return;
			}
		}

		if (!bAttack && !bReinforce)
		{
			if (iCargo > 0)
			{
				if (AI_group(UNITAI_ASSAULT_SEA,-1,-1,-1,
					/*bIgnoreFaster*/true,false,false,
					/*iMaxPath*/5,false,
					/*bCargoOnly*/true,false,MISSIONAI_ASSAULT))
				{
					return;
				}
			}
			/*else if (getPlot().getTeam() == getTeam() && getGroup()->getNumUnits() > 1) {
				CvCity* pCity = getPlot().getPlotCity();
				if (pCity != NULL && (GC.getGame().getGameTurn() - pCity->getGameTurnAcquired()) > 10) {
					if (pCity->getPlot().plotCount(PUF_isAvailableUnitAITypeGroupie, UNITAI_ATTACK_CITY, -1, getOwner()) < iTargetReinforcementSize) {
						// Not attacking, no cargo so release any escorts, attack ships, etc and split transports
						getGroup()->AI_makeForceSeparate();
					}
				}
			}*/ // BtS - moved by K-Mod
		}
	}

	if (!bInPort)
	{
		// <advc.082> (duplicated in the bInPort branch above)
		if (bFull && iCargo >= 3)
		{
			if (iCargo == iTargetReinforcementSize - 1)
				iTargetReinforcementSize--;
			if (iCargo == iTargetInvasionSize - 1)
				iTargetInvasionSize--;
		} // </advc.082>
		if (iCargo >= iTargetInvasionSize)
			bAttack = true;

		if (iCargo >= iTargetReinforcementSize ||
			(bFull && iCargo > cargoSpace()))
		{
			bReinforce = true;
		}

		FOR_EACH_ADJ_PLOT(getPlot())
		{
			if (iCargo > 0)
			{
				CvCity const* pAdjCity = pAdj->getPlotCity();
				if (pAdjCity != NULL &&
					pAdjCity->getOwner() == getOwner() &&
					pAdjCity->getPreviousCiv() != NO_CIVILIZATION)
				{
					if (GC.getGame().getGameTurn() -
						pAdjCity->getGameTurnAcquired() < 5)
					{
						// If just captured city and we have some cargo, dump units in city
						pushGroupMoveTo(*pAdj, NO_MOVEMENT_FLAGS, false, false,
								NO_MISSIONAI, pAdj);
						/*	K-Mod note: this use to use missionAI_assault.
							I've changed it because assault would suggest to the troops
							that they should stay onboard. */
						return;
					}
				}
			}
			else if (isEnemy(*pAdj) && // advc (simplified)
				pAdj->getNumDefenders(getOwner()) > 2)
			{
				/*	if we just made a dropoff in enemy territory,
					release sea bombard units to support invaders */
				if (getGroup()->countNumUnitAIType(UNITAI_ATTACK_SEA) +
					getGroup()->countNumUnitAIType(UNITAI_RESERVE_SEA) > 0)
				{
					bool bMissionPushed = false;
					if (AI_seaBombardRange(1))
						bMissionPushed = true;
					CvSelectionGroup const* pOldGroup = getGroup();
					//Release any Warships to finish the job.
					AI_getGroup()->AI_separateAI(UNITAI_ATTACK_SEA);
					AI_getGroup()->AI_separateAI(UNITAI_RESERVE_SEA);
					// Fixed bug in next line with checking unit type instead of unit AI
					if (pOldGroup == getGroup() && AI_getUnitAIType() == UNITAI_ASSAULT_SEA)
					{
						// Need to be sure all units can move
						if (getGroup()->canAllMove())
						{
							if (AI_retreatToCity(true))
								bMissionPushed = true;
						}
					}
					if (bMissionPushed)
						return;
				}
			}
		}
		if(iCargo > 0)
		{
			MissionAITypes eMissionAIType = MISSIONAI_GROUP;
			if (kOwner.AI_isAnyUnitTargetMissionAI(
				*this, &eMissionAIType, 1, getGroup(), 1))
			{	// advc (tbd.): Use PlotDanger instead? More accurate but slower.
				if (iEscorts < kOwner.AI_getWaterDanger(getPlot(), 2))
				{
					// Wait for units which are joining our group this turn (hopefully escorts)
					getGroup()->pushMission(MISSION_SKIP);
					return;
				}
			}
		}
	}

	if (bBarbarian || isMinorCiv()) // rfc
	{
		if (getGroup()->isFull() || iCargo > iTargetInvasionSize)
		{
			if (AI_assaultSeaTransport(false))
				return;
		}
		else
		{
			if (AI_pickup(UNITAI_ATTACK_CITY, true, 5))
				return;
			if (AI_pickup(UNITAI_ATTACK, true, 5))
				return;
			if (AI_retreatToCity())
				return;
			if (!getGroup()->getCargo())
			{
				AI_barbAttackSeaMove();
				return;
			}
			if (AI_safety())
				return;
			getGroup()->pushMission(MISSION_SKIP);
			return;
		}
	}
	else
	{
		if (bAttack || bReinforce)
		{
			if (bInPort)
				AI_getGroup()->AI_separateEmptyTransports();
			if (!getGroup()->hasCargo())
			{
				// this unit was empty group leader
				//getGroup()->pushMission(MISSION_SKIP);
				//return;
				bAttack = bReinforce = false; // K-Mod
				iCargo = 0;
			}
		}
		if (bAttack || bReinforce) // K-Mod
		{
			FAssert(getGroup()->hasCargo());

			//BBAI TODO: Check that group has escorts, otherwise usually wait

			if (bAttack)
			{
				if (bReinforce && (AI_getBirthmark()%2 == 0))
				{
					if (AI_assaultSeaReinforce())
						return;
					bReinforce = false;
				}
				if (AI_assaultSeaTransport())
					return;
			}
			// If not enough troops for own invasion
			if (bReinforce)
			{
				if (AI_assaultSeaReinforce())
					return;
				/*	<advc.082> Limited war: See if we can invade a colony
					with a smaller stack */
				if (!bAttack && bFull &&
					GET_TEAM(getTeam()).AI_getNumWarPlans(WARPLAN_TOTAL) +
					GET_TEAM(getTeam()).AI_getNumWarPlans(WARPLAN_PREPARING_TOTAL) <= 0)
				{
					if (AI_assaultSeaTransport(false, false, 2))
						return;
				} // </advc.082>
			}
		}
		if (bNoWarPlans && iCargo >= iTargetReinforcementSize)
		{
			AI_getGroup()->AI_separateEmptyTransports();
			if (!getGroup()->hasCargo())
			{
				// this unit was empty group leader
				getGroup()->pushMission(MISSION_SKIP);
				return;
			}
			FAssert(getGroup()->hasCargo());
			if (AI_assaultSeaReinforce(true))
				return;

			FAssert(getGroup()->hasCargo());
			if (AI_assaultSeaTransport(true))
				return;
		}
	}  // <advc.046>
	bool bHasCargo = getGroup()->hasCargo(); // Moved up
	/*  If we have room, or are in a city where we could unload, check if there is
		a good stranded target. This is more important than drawing units together
		when no naval attack is planned (!bAttack). */
	bool const bGoodCity = (getPlot().isCity() && getPlot().getTeam() == getTeam() &&
			GET_TEAM(getTeam()).AI_isPrimaryArea(getPlot().getArea()));
	if((bGoodCity || !bHasCargo) && !bAttack &&
		AI_pickupStranded())
	{
		return;
	} // </advc.046>
	if ((bFull || bReinforce) && !bAttack)
	{
		// Group with nearby transports with units on board
		/*if (AI_group(UNITAI_ASSAULT_SEA, -1, -1, -1, true, false, false, 2, false, true, false, MISSIONAI_ASSAULT))
			return;*/ // BtS
		// disabled by K-Mod. This is redundant.

		//if (AI_group(UNITAI_ASSAULT_SEA, -1, -1, -1, true, false, false, 10, false, true, false, MISSIONAI_ASSAULT))
		if (AI_omniGroup(UNITAI_ASSAULT_SEA, -1, -1, false,
			NO_MOVEMENT_FLAGS, 10, true, true, true, false, false, -1, true, true))
		{
			return;
		}
	}
	else if (!bFull)
	{
		bool bHasOneLoad = (getGroup()->getCargo() >= cargoSpace());
		if (AI_pickup(UNITAI_ATTACK_CITY, !bHasCargo, bHasOneLoad ? 3 : 7))
			return;
		if (AI_pickup(UNITAI_ATTACK, !bHasCargo, bHasOneLoad ? 3 : 7))
			return;
		if (AI_pickup(UNITAI_COUNTER, !bHasCargo, bHasOneLoad ? 3 : 7))
			return;
		if (AI_pickup(UNITAI_ATTACK_CITY, !bHasCargo))
			return;
		if (!bHasCargo)
		{
			if(AI_pickupStranded(UNITAI_ATTACK_CITY))
				return;
			if(AI_pickupStranded(UNITAI_ATTACK))
				return;
			if(AI_pickupStranded(UNITAI_COUNTER))
				return;
			if (getGroup()->countNumUnitAIType(AI_getUnitAIType()) == 1)
			{
				// Try picking up anything
				if(AI_pickupStranded())
					return;
			}
		}
	}

	//if (bInPort && bLandWar && getGroup()->hasCargo())
	if (bInPort)
	{
		FAssert(iCargo == getGroup()->getCargo());
		if (bLandWar && iCargo > 0)
		{
			// Enemy units in this player's territory
			if (2 * kOwner.AI_countNumAreaHostileUnits(getArea(),
				true, false, false, false,
				/* <advc.opt> */ plot() /* </advc.opt> */) > iCargo)
			{
				getGroup()->unloadAll();
				getGroup()->pushMission(MISSION_SKIP);
				return;
			}
		}
		// K-Mod. (moved from way higher up)
		if (iCargo == 0 && getPlot().getTeam() == getTeam() &&
			getGroup()->getNumUnits() > 1)
		{
			AI_getGroup()->AI_separate();
			getGroup()->pushMission(MISSION_SKIP);
			return;
		}
	}
	// BETTER_BTS_AI_MOD: END

	if (AI_retreatToCity(true))
		return;
	if (AI_retreatToCity())
		return;
	if (AI_safety())
		return;
	getGroup()->pushMission(MISSION_SKIP);
}


void CvUnitAI::AI_settlerSeaMove()
{
	PROFILE_FUNC();
    CvPlayerAI const& kOwner = GET_PLAYER(getOwner());

    // doc: initial settler at sea should not attempt to found the capital
    if (kOwner.getNumCities() == 0)
        return;

	bool const bEmpty = !getGroup()->hasCargo();

	// BETTER_BTS_AI_MOD, Naval AI, 10/21/08, Solver & jdog5000: START
	if (AI_isThreatenedFromLand() >= PROBABILITY_REAL) // advc.139: Moved into subroutine
	{
		if (bEmpty)
		{
			if (AI_anyAttack(1, 65))
			{
				return;
			}
		}
		// Retreat to primary area first
		if (AI_retreatToCity(true))
		{
			return;
		}
		if (AI_retreatToCity())
		{
			return;
		}
		if (AI_safety())
		{
			return;
		}
	} // BETTER_BTS_AI_MOD: END

	if (bEmpty)
	{
		if (AI_anyAttack(1, 65))
		{
			return;
		}
		if (AI_anyAttack(1, 40))
		{
			return;
		}
	}

	int iSettlerCount = getUnitAICargo(UNITAI_SETTLE);
	int iWorkerCount = getUnitAICargo(UNITAI_WORKER);

	// BETTER_BTS_AI_MOD, Naval AI, 12/07/08, jdog5000: START
	if (hasCargo() && iSettlerCount == 0 && iWorkerCount == 0)
	{
		// Dump troop load at first oppurtunity after pick up
		if (getPlot().isCity() && getPlot().getOwner() == getOwner())
		{
			getGroup()->unloadAll();
			getGroup()->pushMission(MISSION_SKIP);
			return;
		}
		else
		{
			if (!isFull())
			{
				if(AI_pickupStranded(NO_UNITAI, 1))
				{
					return;
				}
			}

			if (AI_retreatToCity(true))
			{
				return;
			}

			if (AI_retreatToCity())
			{
				return;
			}
		}
	} // BETTER_BTS_AI_MOD: END


	// BETTER_BTS_AI_MOD, Settler AI, 06/02/09, jdog5000: START
	// Don't send transport with settler and no defense
	if (iSettlerCount > 0 && iSettlerCount + iWorkerCount == cargoSpace())
	{
		// No defenders for settler
		if (getPlot().isCity() && getPlot().getOwner() == getOwner())
		{
			getGroup()->unloadAll();
			getGroup()->pushMission(MISSION_SKIP);
			return;
		}
	}

	if (iSettlerCount > 0 && (isFull() ||
		(getUnitAICargo(UNITAI_CITY_DEFENSE) > 0 &&
		!kOwner.AI_isAnyUnitTargetMissionAI(*this, MISSIONAI_LOAD_SETTLER))))
	// BETTER_BTS_AI_MOD: END
	{
		if (AI_settlerSeaTransport())
		{
			return;
		}
	}
	else if (getTeam() != getPlot().getTeam() && bEmpty)
	{
		if (AI_pillageRange(3))
		{
			return;
		}
	}
	//if (getPlot().isCity() && !hasCargo())
	// BETTER_BTS_AI_MOD, Naval AI, 09/18/09, jdog5000:
	if (getPlot().isCity() && getPlot().getOwner() == getOwner() && !hasCargo())
	{
		AreaAITypes eAreaAI = getArea().getAreaAIType(getTeam());
		if (eAreaAI == AREAAI_ASSAULT || eAreaAI == AREAAI_ASSAULT_MASSING)
		{
			CvArea* pWaterArea = getPlot().waterArea();
			FAssert(pWaterArea != NULL);
			if (pWaterArea != NULL)
			{
				if (kOwner.AI_totalWaterAreaUnitAIs(*pWaterArea, UNITAI_SETTLER_SEA) >
					1 + /* <advc.017b> */ kOwner.getCurrentEra() / 2 ||
					/*  Also convert if no colonies (which may need Workers)
						- check matches w/ a check in CvPlayerAI::AI_chooseProduction -
						and no Settler on the horizon. */
					(kOwner.getCurrentEra() < CvEraInfo::AI_getAgeOfExploration() &&
					kOwner.AI_totalUnitAIs(UNITAI_SETTLE) <= 0 &&
					// </advc.017b>
					kOwner.getNumCities() == getArea().getCitiesPerPlayer(getOwner()) &&
					kOwner.AI_totalUnitAIs(UNITAI_ASSAULT_SEA) <= 5))
				{
					if (kOwner.AI_unitValue(getUnitType(), UNITAI_ASSAULT_SEA, pWaterArea) > 0)
					{
						AI_setUnitAIType(UNITAI_ASSAULT_SEA);
						//AI_assaultSeaMove();
						AI_update(); // advc.003u
						return;
					}
				}
			}
		}
	}

	if (iWorkerCount > 0 &&
		!kOwner.AI_isAnyUnitTargetMissionAI(*this, MISSIONAI_LOAD_SETTLER))
	{
		if (isFull() || (iSettlerCount == 0))
		{
			if (AI_ferryWorkers())
			{
				return;
			}
		}
	}
	/*if (AI_pickup(UNITAI_SETTLE))
		return;*/ // BtS
	// BETTER_BTS_AI_MOD, Settler AI, 09/18/09, jdog5000: START
	if (!getGroup()->hasCargo())
	{
		if(AI_pickupStranded(UNITAI_SETTLE))
		{
			return;
		}
	}

	if (!getGroup()->isFull())
	{
		if (kOwner.AI_isAnyUnitTargetMissionAI(*this, MISSIONAI_LOAD_SETTLER))
		{
			// Wait for units on the way
			getGroup()->pushMission(MISSION_SKIP);
			return;
		}

		if (iSettlerCount > 0 &&
            getCivilizationType() != AMERICA) // doc: Pioneer can defend itself
		{
			if (AI_pickup(UNITAI_CITY_DEFENSE))
			{
				return;
			}
		}
		else if (cargoSpace() - 2 >= getCargo() + iWorkerCount)
		{
			if (AI_pickup(UNITAI_SETTLE, true))
			{
				return;
			}
		}
	}
	// BETTER_BTS_AI_MOD: END

	if (GC.getGame().getGameTurn() - getGameTurnCreated() < 8 &&
		// <K-Mod>
		getPlot().waterArea() && kOwner.AI_areaMissionAIs(
		*getPlot().waterArea(), MISSIONAI_EXPLORE, getGroup()) <
		kOwner.AI_neededExplorers(*getPlot().waterArea())) // </K-Mod>
	{
		if (getPlot().getPlotCity() == NULL ||
			kOwner.AI_totalAreaUnitAIs(getPlot().getArea(), UNITAI_SETTLE) == 0)
		{
			if (AI_explore())
			{
				return;
			}
		}
	}
	/*if (AI_pickup(UNITAI_WORKER))
		return;*/ // BtS
	// BETTER_BTS_AI_MOD, Naval AI, 09/18/09, jdog5000: START
	if (!getGroup()->hasCargo())
	{
		// Rescue stranded non-settlers
		if (AI_pickupStranded())
		{
			return;
		}
	}

	//if (cargoSpace() - 2 < getCargo() + iWorkerCount)
	// advc.rom: (Koshling); relevant excerpt of his comment:
	/*	old condition here was broken for transports with a max capacity of 1 [...],
		and (after reading the old code) I think more generally anyway. [...] */
	if (iWorkerCount > 0 && cargoSpace() > 1 && cargoSpace() - getCargo() < 2)
	{
		// If full of workers and not going anywhere, dump them if a settler is available
		if (iSettlerCount == 0 &&
			getPlot().plotCount(PUF_isAvailableUnitAITypeGroupie,
			UNITAI_SETTLE, -1, getOwner(), NO_TEAM, PUF_isFiniteRange) > 0)
		{
			getGroup()->unloadAll();

			if (AI_pickup(UNITAI_SETTLE, true))
			{
				return;
			}

			return;
		}
	}

	if (!getGroup()->isFull()
			&& iWorkerCount < 2) // advc.113: Don't pick up even more workers
	{
		if (AI_pickup(UNITAI_WORKER))
		{
			return;
		}
	}

	// Carracks cause problems for transport upgrades, galleys can't upgrade to them and they can't
	// upgrade to galleons. Scrap galleys, switch unit AI for stuck Carracks.
	if (getPlot().isCity() && getPlot().getOwner() == getOwner())
	{
		UnitTypes eBestSettlerTransport = NO_UNIT;
		kOwner.AI_bestCityUnitAIValue(AI_getUnitAIType(), NULL, &eBestSettlerTransport);
		if (eBestSettlerTransport != NO_UNIT)
		{
			if (eBestSettlerTransport != getUnitType() &&
				!kOwner.AI_isAnyImpassable(eBestSettlerTransport))
			{
				UnitClassTypes ePotentialUpgradeClass = GC.getInfo(eBestSettlerTransport).getUnitClassType();
				if (!upgradeAvailable(getUnitType(), ePotentialUpgradeClass))
				{
					getGroup()->unloadAll();

					if (kOwner.AI_isAnyImpassable(getUnitType()))
					{
						scrap();
						return;
					}
					else
					{
						CvArea* pWaterArea = getPlot().waterArea();
						FAssert(pWaterArea != NULL);
						if (pWaterArea != NULL)
						{
							if (kOwner.AI_totalUnitAIs(UNITAI_EXPLORE_SEA) <= 0 &&
								// <advc.017b>
								!kOwner.AI_isExcessSeaExplorers(*pWaterArea, 1) &&
								!kOwner.AI_isOutdatedUnit(getUnitType(), UNITAI_EXPLORE_SEA, pWaterArea))
								// </advc.017b>
							{
								if (kOwner.AI_unitValue(getUnitType(), UNITAI_EXPLORE_SEA, pWaterArea) > 0)
								{
									AI_setUnitAIType(UNITAI_EXPLORE_SEA);
									//AI_exploreSeaMove();
									AI_update(); // advc.003u
									return;
								}
							}

							if (kOwner.AI_totalUnitAIs(UNITAI_SPY_SEA) == 0)
							{
								if (kOwner.AI_unitValue(getUnitType(), UNITAI_SPY_SEA, area()) > 0)
								{
									AI_setUnitAIType(UNITAI_SPY_SEA);
									//AI_spySeaMove();
									AI_update(); // advc.003u
									return;
								}
							}

							if (kOwner.AI_totalUnitAIs(UNITAI_MISSIONARY_SEA) == 0)
							{
								if (kOwner.AI_unitValue(getUnitType(), UNITAI_MISSIONARY_SEA, area()) > 0)
								{
									AI_setUnitAIType(UNITAI_MISSIONARY_SEA);
									//AI_missionarySeaMove();
									AI_update(); // advc.003u
									return;
								}
							}

							if (kOwner.AI_unitValue(getUnitType(), UNITAI_ATTACK_SEA, pWaterArea) > 0)
							{
								AI_setUnitAIType(UNITAI_ATTACK_SEA);
								//AI_attackSeaMove();
								AI_update(); // advc.003u
								return;
							}
						}
					}
				}
			}
		}
	}
	// BETTER_BTS_AI_MOD: END

	if (AI_retreatToCity(true))
	{
		return;
	}

	if (AI_retreatToCity())
	{
		return;
	}

	if (AI_safety())
	{
		return;
	}

	getGroup()->pushMission(MISSION_SKIP);
}


void CvUnitAI::AI_missionarySeaMove()
{
	PROFILE_FUNC();
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner()); // K-Mod
	/*	<advc.mnai> (I think this could be relevant when a Caravel
		upgrades to a Destroyer) */
	if (cargoSpace() <= 0)
	{
		AI_setUnitAIType(UNITAI_EXPLORE_SEA);
		getGroup()->pushMission(MISSION_SKIP);
		return;
	} // </advc.mnai>

	// BETTER_BTS_AI_MOD, Naval AI, 10/21/08, Solver & jdog5000: START
	if (AI_isThreatenedFromLand() >= PROBABILITY_REAL) // advc.139: Moved into subroutine
	{
		// Retreat to primary area first
		if (AI_retreatToCity(true))
		{
			return;
		}
		if (AI_retreatToCity())
		{
			return;
		}
		if (AI_safety())
		{
			return;
		}
	} // BETTER_BTS_AI_MOD: END

	if (getUnitAICargo(UNITAI_MISSIONARY) > 0)
	{
		if (AI_specialSeaTransportMissionary())
		{
			return;
		}
	}
	else if (!getGroup()->hasCargo())
	{
		if (AI_pillageRange(4))
		{
			return;
		}
	}
	// BETTER_BTS_AI_MOD, Naval AI, 01/14/09, jdog5000: START
	if (!getGroup()->isFull())
	{
		if (kOwner.AI_isAnyUnitTargetMissionAI(*this, MISSIONAI_LOAD_SPECIAL))
		{
			// Wait for units on the way
			getGroup()->pushMission(MISSION_SKIP);
			return;
		}
	}

	if (AI_pickup(UNITAI_MISSIONARY, true))
	{
		return;
	}
	// BETTER_BTS_AI_MOD: END
	// <K-Mod>
	if (getPlot().waterArea() && kOwner.AI_areaMissionAIs(
		*getPlot().waterArea(), MISSIONAI_EXPLORE, getGroup()) <
		kOwner.AI_neededExplorers(*getPlot().waterArea())) // </K-Mod>
	{
		if (AI_explore())
			return;
	}

	if (AI_retreatToCity(true))
	{
		return;
	}

	if (AI_retreatToCity())
	{
		return;
	}

	if (AI_safety())
	{
		return;
	}

	getGroup()->pushMission(MISSION_SKIP);
}


void CvUnitAI::AI_spySeaMove()
{
	PROFILE_FUNC();
	const CvPlayerAI& kOwner = GET_PLAYER(getOwner()); // K-Mod
	// BETTER_BTS_AI_MOD, Naval AI, 10/21/08, Solver & jdog5000: START
	if (AI_isThreatenedFromLand() >= PROBABILITY_REAL) // advc.139: Moved into subroutine
	{
		// Retreat to primary area first
		if (AI_retreatToCity(true))
		{
			return;
		}
		if (AI_retreatToCity())
		{
			return;
		}
		if (AI_safety())
		{
			return;
		}
	} // BETTER_BTS_AI_MOD: END

	if (getUnitAICargo(UNITAI_SPY) > 0)
	{
		if (AI_specialSeaTransportSpy())
		{
			return;
		}

		CvCity* pCity = getPlot().getPlotCity();

		if (pCity != NULL)
		{
			if (pCity->getOwner() == getOwner())
			{
				getGroup()->pushMission(MISSION_SKIP, -1, -1, NO_MOVEMENT_FLAGS,
						false, false, MISSIONAI_ATTACK_SPY, pCity->plot());
				return;
			}
		}
	}
	else if (!(getGroup()->hasCargo()))
	{
		if (AI_pillageRange(5))
		{
			return;
		}
	}
	// BETTER_BTS_AI_MOD, Naval AI, 01/14/09, jdog5000: START
	if (!getGroup()->isFull())
	{
		if (kOwner.AI_isAnyUnitTargetMissionAI(*this, MISSIONAI_LOAD_SPECIAL))
		{
			// Wait for units on the way
			getGroup()->pushMission(MISSION_SKIP);
			return;
		}
	}

	if (AI_pickup(UNITAI_SPY, true))
	{
		return;
	}
	// BETTER_BTS_AI_MOD: END
	if (AI_retreatToCity(true))
	{
		return;
	}

	if (AI_retreatToCity())
	{
		return;
	}

	if (AI_safety())
	{
		return;
	}

	getGroup()->pushMission(MISSION_SKIP);
}


void CvUnitAI::AI_carrierSeaMove()
{
	PROFILE_FUNC();
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner()); // K-Mod
	// BETTER_BTS_AI_MOD, Naval AI, 10/21/08, Solver & jdog5000: START
	if (AI_isThreatenedFromLand() != PROBABILITY_REAL) // advc.139: Moved into subroutine
	{
		if (AI_retreatToCity(true))
		{
			return;
		}
		if (AI_retreatToCity())
		{
			return;
		}
		if (AI_safety())
		{
			return;
		}
	} // BETTER_BTS_AI_MOD: END
	if (AI_heal(50))
	{
		return;
	}

	if (!isEnemy(getPlot()))
	{
		if (kOwner.AI_isAnyUnitTargetMissionAI(*this, MISSIONAI_GROUP))
		{
			getGroup()->pushMission(MISSION_SKIP);
			return;
		}
	}
	else
	{
		if (AI_seaBombardRange(1))
		{
			return;
		}
	}

	if (AI_group(UNITAI_CARRIER_SEA, -1, /*iMaxOwnUnitAI*/ 1))
	{
		return;
	}

	if (getGroup()->countNumUnitAIType(UNITAI_ATTACK_SEA) + getGroup()->countNumUnitAIType(UNITAI_ESCORT_SEA) == 0)
	{
		if (getPlot().isCity() && getPlot().getOwner() == getOwner())
		{
			getGroup()->pushMission(MISSION_SKIP);
			return;
		}
		if (AI_retreatToCity())
		{
			return;
		}
	}

	if (getCargo() > 0)
	{
		if (AI_carrierSeaTransport())
		{
			return;
		}

		if (AI_blockade())
		{
			return;
		}

		if (AI_shadow(UNITAI_ASSAULT_SEA))
		{
			return;
		}
	}

	if (AI_travelToUpgradeCity())
	{
		return;
	}

	if (AI_retreatToCity(true))
	{
		return;
	}

	if (AI_retreatToCity())
	{
		return;
	}

	if (AI_safety())
	{
		return;
	}

	getGroup()->pushMission(MISSION_SKIP);
}


void CvUnitAI::AI_missileCarrierSeaMove()
{
	PROFILE_FUNC();

	bool bStealth = (getInvisibleType() != NO_INVISIBLE);

	// BETTER_BTS_AI_MOD, Naval AI, 06/14/09, Solver & jdog5000: START
	if(AI_isThreatenedFromLand() >= PROBABILITY_REAL) // advc.139: Moved into subroutine
	{
		if (AI_shadow(UNITAI_ASSAULT_SEA, 1, 50, false, true, baseMoves()))
		{
			return;
		}
		if (AI_retreatToCity())
		{
			return;
		}
		if (AI_safety())
		{
			return;
		}
	} // BETTER_BTS_AI_MOD: END

	if (getPlot().isCity() && getPlot().getTeam() == getTeam())
	{
		if (AI_heal())
		{
			return;
		}
	}

	if ((getPlot().getTeam() != getTeam() && getGroup()->hasCargo()) ||
		AI_getGroup()->AI_isFull())
	{
		if (bStealth)
		{
			if (AI_carrierSeaTransport())
			{
				return;
			}
		}
		else
		{
			// BETTER_BTS_AI_MOD, Naval AI, 06/14/09, jdog5000: START
			if (AI_shadow(UNITAI_ASSAULT_SEA, 1, 50, true, false, 12))
			{
				return;
			} // BETTER_BTS_AI_MOD: END

			if (AI_carrierSeaTransport())
			{
				return;
			}
		}
	}
	// advc (comment): The BtS expansion added these two, already commented out.
	/*if (AI_pickup(UNITAI_ICBM))
		return;
	if (AI_pickup(UNITAI_MISSILE_AIR))
		return;*/
	if (AI_retreatToCity())
	{
		return;
	}

	getGroup()->pushMission(MISSION_SKIP);
}


void CvUnitAI::AI_attackAirMove()
{
	PROFILE_FUNC();
	const CvPlayerAI& kOwner = GET_PLAYER(getOwner()); // K-Mod

	// BETTER_BTS_AI_MOD, Air AI, 10/21/08, Solver & jdog5000: START
	CvCityAI const* pCity = getPlot().AI_getPlotCity();
	//bool bSkiesClear = true;
	//int iDX, iDY;

	// Check for sufficient defenders to stay
	int iDefenders = getPlot().plotCount(PUF_canDefend, -1, -1, getPlot().getOwner(),
			NO_TEAM, PUF_isDomainType, DOMAIN_LAND); // advc.001s

	int iAttackAirCount = getPlot().plotCount(PUF_canAirAttack, -1, -1, NO_PLAYER, getTeam());
	iAttackAirCount += 2 * getPlot().plotCount(PUF_isUnitAIType, UNITAI_ICBM, -1, NO_PLAYER, getTeam());

	if (getPlot().isCoastalLand(-1))
		iDefenders -= 1;

	if (pCity != NULL)
	{
		if (pCity->getDefenseModifier(true) < 40)
			iDefenders -= 1;
		if (pCity->getOccupationTimer() > 1)
			iDefenders -= 1;
	}

	if (iAttackAirCount > iDefenders)
	{
		if (AI_airOffensiveCity())
		{
			return;
		}
	}

	// Check for direct threat to current base
	//if (getPlot().isCity(true))
	if (!getPlot().isWater()) // advc.opt
	{
		// K-Mod
		int iOurDefense = kOwner.AI_localDefenceStrength(plot(), getTeam(), DOMAIN_LAND, 0);
		int iEnemyOffense = kOwner.AI_localAttackStrength(plot(), NO_TEAM, DOMAIN_LAND, 2);
		// K-Mod end

		if (iEnemyOffense > iOurDefense || iOurDefense == 0)
		{
			// Too risky, pull back
			if (AI_airOffensiveCity())
			{
				return;
			}

			if (canAirDefend())
			{
				if (AI_airDefensiveCity())
				{
					return;
				}
			}
		}
		else if (iEnemyOffense > iOurDefense / 3)
		{
			if (getDamage() == 0)
			{
				if (collateralDamage() == 0 && canAirDefend())
				{
					if (pCity != NULL)
					{
						// Check for whether city needs this unit to air defend
						if (!pCity->AI_isAirDefended(true, -1))
						{
							getGroup()->pushMission(MISSION_AIRPATROL);
							return;
						}
					}
				}

				// Attack the invaders!
				if (AI_defendBaseAirStrike())
				{
					return;
				}

				/*if (AI_defensiveAirStrike())
					return;*/

				if (AI_airStrike())
				{
					return;
				}

				// If no targets, no sense staying in risky place
				if (AI_airOffensiveCity())
				{
					return;
				}

				if (canAirDefend())
				{
					if (AI_airDefensiveCity())
					{
						return;
					}
				}
			}

			if (healTurns() > 1)
			{
				// If very damaged, no sense staying in risky place
				if (AI_airOffensiveCity())
				{
					return;
				}

				if (canAirDefend())
				{
					if (AI_airDefensiveCity())
					{
						return;
					}
				}
			}

		}
	}

	if (getDamage() > 0)
	{
		//if (((100*currHitPoints()) / maxHitPoints()) < 40)
		{
			getGroup()->pushMission(MISSION_SKIP);
			return;
		}
		/*else {
			for (SquareIter it(*this, airRange()); it.hasNext(); ++it) {
				if (bestInterceptor(&(*it)) != NULL) {
					bSkiesClear = false;
					break;
				}
			}
			if (!bSkiesClear){
				getGroup()->pushMission(MISSION_SKIP);
				return;
			}
		}*/ // BtS/ BBAI - Disabled by K-Mod because it's time consuming and doesn't help much
	}
	// BETTER_BTS_AI_MOD: END

	CvPlayerAI& kPlayer = GET_PLAYER(getOwner());
	int iAttackValue = kPlayer.AI_unitValue(getUnitType(), UNITAI_ATTACK_AIR, area());
	int iCarrierValue = kPlayer.AI_unitValue(getUnitType(), UNITAI_CARRIER_AIR, area());
	if (iCarrierValue > 0)
	{
		int iCarriers = kPlayer.AI_totalUnitAIs(UNITAI_CARRIER_SEA);
		if (iCarriers > 0)
		{
			UnitTypes eBestCarrierUnit = NO_UNIT;
			kPlayer.AI_bestAreaUnitAIValue(UNITAI_CARRIER_SEA, NULL, &eBestCarrierUnit);
			if (eBestCarrierUnit != NO_UNIT)
			{
				int iCarrierAirNeeded = iCarriers * GC.getInfo(eBestCarrierUnit).getCargoSpace();
				if (kPlayer.AI_totalUnitAIs(UNITAI_CARRIER_AIR) < iCarrierAirNeeded)
				{
					AI_setUnitAIType(UNITAI_CARRIER_AIR);
					getGroup()->pushMission(MISSION_SKIP);
					return;
				}
			}
		}
	}

	int iDefenseValue = kPlayer.AI_unitValue(getUnitType(), UNITAI_DEFENSE_AIR, area());
	if (iDefenseValue > iAttackValue)
	{
		if (kPlayer.AI_bestAreaUnitAIValue(UNITAI_ATTACK_AIR, area()) > iAttackValue)
		{
			AI_setUnitAIType(UNITAI_DEFENSE_AIR);
			getGroup()->pushMission(MISSION_SKIP);
			return;
		}
	}
	/*if (AI_airBombDefenses())
		return;
	... // advc: deleted most of it
	if (canAirDefend()) {
		getGroup()->pushMission(MISSION_AIRPATROL);
		return;
	}*/ // BtS (replaced by BBAI/K-Mod)
	// BETTER_BTS_AI_MOD, Air AI, 10/6/08, jdog5000: START
	bool const bDefensive = (getArea().getAreaAIType(getTeam()) == AREAAI_DEFENSIVE);

	/*if (SyncRandOneChanceIn(bDefensive ? 3 : 6)) {
		if (AI_defensiveAirStrike())
			return;
	}*/ // disabled by K-Mod

	if (SyncRandOneChanceIn(4))
	{
		if (AI_travelToUpgradeCity()) // only moves unit in a fort
		{
			return;
		}
	}

	// Support ground attacks
	/*if (AI_airBombDefenses())
		return;
	if (SyncRandOneChanceIn(bDefensive ? 6 : 4)) {
		if (AI_airBombPlots())
			return;
	}
	if (AI_airStrike())
		return;*/ // BtS
	// K-Mod
	if (AI_airStrike())
	{
		return;
	}
	/*	switched probabilities from original bts. If we're on the offense,
		we don't want to smash up too many improvements...
		soon they will be _our_ improvements. */
	if (SyncRandOneChanceIn(bDefensive ? 4 : 6))
	{
		if (AI_airBombPlots())
		{
			return;
		}
	}

	if (canAirAttack())
	{
		if (AI_airOffensiveCity())
		{
			return;
		}
	}
	else
	{
		if (canAirDefend())
		{
			if (AI_airDefensiveCity())
			{
				return;
			}
		}
	}

	// BBAI TODO: Support friendly attacks on common enemies, if low risk?

	if (canAirDefend())
	{
		if (bDefensive || SyncRandOneChanceIn(2))
		{
			getGroup()->pushMission(MISSION_AIRPATROL);
			return;
		}
	}

	if (canRecon(plot()))
	{
		if (AI_exploreAirCities())
		{
			return;
		}
	}
	// BETTER_BTS_AI_MOD: END

	getGroup()->pushMission(MISSION_SKIP);
}

// This function has been rewritten for K-Mod. (The new version is much simpler.)
void CvUnitAI::AI_defenseAirMove()
{
	PROFILE_FUNC();
	//if (!getPlot().isCity(true))
	if (!isValidDomain(getPlot())) // advc
	{
		//FAssertMsg(GC.getGame().getGameTurn() - getGameTurnCreated() > 1, "defenseAir units are expected to stay in cities/forts");
		if (AI_airDefensiveCity())
			return;
	}

	int const iEnemyOffense = GET_PLAYER(getOwner()).AI_localAttackStrength(plot());
	int const iOurDefense = GET_PLAYER(getOwner()).AI_localDefenceStrength(plot(), getTeam());

	if (iEnemyOffense > 2*iOurDefense || iOurDefense == 0)
	{
		// Too risky, pull out
		if (AI_airDefensiveCity())
		{
			return;
		}
	}

	CvCityAI const* pCity = getPlot().AI_getPlotCity();
	int iDefNeeded = (pCity == NULL ? 0 : pCity->AI_neededAirDefenders());
	int iDefHere = getPlot().plotCount(PUF_isAirIntercept, -1, -1, NO_PLAYER, getTeam()) -
			(PUF_isAirIntercept(this, -1, -1) ? 1 : 0);
	FAssert(iDefHere >= 0);

	if (canAirDefend() && iEnemyOffense < iOurDefense && iDefHere < iDefNeeded/2)
	{
		getGroup()->pushMission(MISSION_AIRPATROL);
		return;
	}

	if (iEnemyOffense > (getDamage() == 0 ? iOurDefense/3 : iOurDefense))
	{
		// Attack the invaders!
		if (AI_defendBaseAirStrike())
		{
			return;
		}
	}

	if (getDamage() > maxHitPoints()/3)
	{
		getGroup()->pushMission(MISSION_SKIP);
		return;
	}

	if (iEnemyOffense == 0 && SyncRandOneChanceIn(4))
	{
		if (AI_travelToUpgradeCity())
		{
			return;
		}
	}

	bool const bDefensive = (getArea().getAreaAIType(getTeam()) == AREAAI_DEFENSIVE);
	bool const bOffensive = (getArea().getAreaAIType(getTeam()) == AREAAI_OFFENSIVE);

	bool bTriedAirStrike = false;
	if (SyncRandNum(3) <= (bOffensive ? 1 : 0) - (bDefensive ? 1 : 0))
	{
		if (AI_airStrike())
			return;
		bTriedAirStrike = true;
	}

	if (canAirDefend() && iDefHere < iDefNeeded*2/3)
	{
		getGroup()->pushMission(MISSION_AIRPATROL);
		return;
	}

	if (!bTriedAirStrike &&
		SyncRandNum(3) <= (bOffensive ? 1 : 0) - (bDefensive ? 1 : 0))
	{
		if (AI_airStrike())
			return;
		bTriedAirStrike = true;
	}

	// <advc.650>
	if (GET_PLAYER(getOwner()).AI_isDangerFromSubmarines() &&
		getPlot().isCoastalLand(-1) && SyncRandSuccess100(38))
	{
		/*	Would be better to check for matching Invisible Types (modded aircraft
			may not be able to see invisible units). Also, isCoastalLand is a bit
			narrow -- can often scout the seas from landlocked cities. */
		if (AI_exploreAirRange())
			return;
	} // </advc.650>

	if (AI_airDefensiveCity()) // check if there's a better city to be in
	{
		return;
	}

	if (canAirDefend() && iDefHere < iDefNeeded)
	{
		getGroup()->pushMission(MISSION_AIRPATROL);
		return;
	}

	if (canRecon(plot()))
	{
		if (SyncRandOneChanceIn(bDefensive ? 6 : 3))
		{
			if (AI_exploreAirCities())
			{
				return;
			}
		}
	}

	if (canAirDefend())
	{
		getGroup()->pushMission(MISSION_AIRPATROL);
		return;
	}

	getGroup()->pushMission(MISSION_SKIP);
}


void CvUnitAI::AI_carrierAirMove()
{
	PROFILE_FUNC();

	// XXX maybe protect land troops?

	if (getDamage() > 0)
	{
		getGroup()->pushMission(MISSION_SKIP);
		return;
	}

	if (isCargo())
	{
		/*int iRand = SyncRandNum(3);
		if (iRand == 2 && canAirDefend()) {
			getGroup()->pushMission(MISSION_AIRPATROL);
			return;
		}
		else if (AI_airBombDefenses())
			return;
		else if (iRand == 1) {
			if (AI_airBombPlots())
				return;
			if (AI_airStrike())
				return;
		}
		else {
			if (AI_airStrike())
				return;
			if (AI_airBombPlots())
				return;
		}*/ // BtS
		// K-Mod
		if (canAirDefend())
		{
			int iActiveInterceptors = getPlot().plotCount(
					PUF_isAirIntercept, -1, -1, getOwner());
			if (SyncRandNum(16) < 4 - std::min(3, iActiveInterceptors))
			{
				getGroup()->pushMission(MISSION_AIRPATROL);
				return;
			}
		}
		if (AI_airStrike())
		{
			return;
		}
		if (AI_airBombPlots())
		{
			return;
		}
		// K-Mod end

		if (AI_travelToUpgradeCity())
		{
			return;
		}

		if (canAirDefend())
		{
			getGroup()->pushMission(MISSION_AIRPATROL);
			return;
		}
		getGroup()->pushMission(MISSION_SKIP);
		return;
	}

	if (AI_airCarrier())
	{
		return;
	}

	if (AI_airDefensiveCity())
	{
		return;
	}

	if (canAirDefend())
	{
		getGroup()->pushMission(MISSION_AIRPATROL);
		return;
	}

	getGroup()->pushMission(MISSION_SKIP);
}


void CvUnitAI::AI_missileAirMove()
{
	PROFILE_FUNC();

	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());
	// BETTER_BTS_AI_MOD, Air AI, 10/21/08, Solver & jdog5000: START
	//if (!isCargo() && getPlot().isCity(true))
	if (!getPlot().isWater()) // advc.opt
	{
		// K-Mod
		int iOurDefense = kOwner.AI_localDefenceStrength(plot(), getTeam(), DOMAIN_LAND, 0);
		int iEnemyOffense = kOwner.AI_localAttackStrength(plot(), NO_TEAM, DOMAIN_LAND, 2);
		// K-Mod end

		if (2 * iEnemyOffense > iOurDefense || iOurDefense == 0)
		{
			if (AI_airOffensiveCity())
			{
				return;
			}
		}
	} // BETTER_BTS_AI_MOD: END

	if (isCargo())
	{
		int iRand = SyncRandNum(3);
		if (iRand != 0)
		{
			if (AI_airBombPlots())
			{
				return;
			}
		}

		/*iRand = SyncRandNum(3);
		if (iRand == 0) {
			if (AI_airBombDefenses())
				return;
			if (AI_airStrike())
				return;
		}
		else {
			if (AI_airStrike())
				return;
			if (AI_airBombDefenses())
				return;
		}*/ // BtS
		// K-Mod
		if (AI_airStrike())
		{
			return;
		}
		// K-Mod end

		if (AI_airBombPlots())
		{
			return;
		}

		getGroup()->pushMission(MISSION_SKIP);
		return;
	}

	if (AI_airStrike())
	{
		return;
	}

	if (AI_missileLoad(UNITAI_MISSILE_CARRIER_SEA))
	{
		return;
	}

	if (AI_missileLoad(UNITAI_RESERVE_SEA, 1))
	{
		return;
	}

	if (AI_missileLoad(UNITAI_ATTACK_SEA, 1))
	{
		return;
	}

	/* if (AI_airBombDefenses())
		return;*/ // disabled by K-Mod

	if (!isCargo())
	{
		if (AI_airOffensiveCity())
		{
			return;
		}
	}

	getGroup()->pushMission(MISSION_SKIP);
}


void CvUnitAI::AI_networkAutomated()
{
	FAssertMsg(canBuildRoute(), "canBuildRoute is expected to be true");

	if (!getGroup()->canDefend())
	{
		// BETTER_BTS_AI_MOD, Unit AI, Efficiency, 08/20/09, jdog5000: was AI_getPlotDanger
		if (GET_PLAYER(getOwner()).AI_isAnyPlotDanger(getPlot()))
		{
			if (AI_retreatToCity()) // XXX maybe not do this??? could be working productively somewhere else...
			{
				return;
			}
		}
	}

	/* if (AI_improveBonus(0,20))
		return;
	if (AI_improveBonus(o,10))
		return;*/
	// K-Mod
	if (AI_improveBonus())
		return;
	// K-Mod end. (I don't think AI_connectBonus() is useful either, but I haven't looked closely enough to remove it.)

	if (AI_connectBonus())
	{
		return;
	}

	if (AI_connectCity())
	{
		return;
	}

	/* if (AI_improveBonus())
		return; */ // disabled by K-Mod

	if (AI_routeTerritory(true))
	{
		return;
	}

	if (AI_connectBonus(false))
	{
		return;
	}

	if (AI_routeCity())
	{
		return;
	}

    // rfc: disabled
	/*if (AI_routeTerritory())
	{
		return;
	}*/

	if (AI_retreatToCity())
	{
		return;
	}

	if (AI_safety())
	{
		return;
	}

	getGroup()->pushMission(MISSION_SKIP);
}


void CvUnitAI::AI_cityAutomated()
{
	if (!getGroup()->canDefend())
	{
		// BETTER_BTS_AI_MOD, Unit AI, Efficiency, 08/20/09, jdog5000: was AI_getPlotDanger
		if (GET_PLAYER(getOwner()).AI_isAnyPlotDanger(getPlot()))
		{
			if (AI_retreatToCity()) // XXX maybe not do this??? could be working productively somewhere else...
			{
				return;
			}
		}
	}

	CvCityAI const* pCity = NULL;

	if (getPlot().getOwner() == getOwner())
	{
		pCity = getPlot().AI_getWorkingCity();
	}

	if (pCity == NULL)
	{
		CvCity* pMapCity = GC.getMap().findCity(getX(), getY(), getOwner()); // XXX do team???
		pCity = (pMapCity == NULL ? NULL : &pMapCity->AI()); // advc.003u
	}

	if (pCity != NULL)
	{
		if (AI_improveCity(*pCity))
		{
			return;
		}
	}

	if (AI_retreatToCity())
	{
		return;
	}

	if (AI_safety())
	{
		return;
	}

	getGroup()->pushMission(MISSION_SKIP);
}

// SuperSpies (TSHEEP): spy promotion value
// TODO: header
int CvUnitAI::AI_spyPromotionValue(PromotionTypes ePromotion)
{
    CvPromotionInfo const& kPromo = GC.getInfo(ePromotion);
    int iValue = 0;

    if (kPromo.isAlwaysHeal()) //Loyalty Promotion
        iValue += (5 + withdrawalProbability()); // Favor spies that have a chance to escape

    //Security
    iValue += kPromo.getInterceptChange() + currInterceptionProbability(); //Lean towards more security if security is already present

    //Deception
    iValue += kPromo.getEvasionChange() * 3 + evasionProbability(); //Lean towards more deception if deception is already present

    if (kPromo.isEnemyRoute())
        iValue += 4;

    iValue += kPromo.getVisibilityChange() * 5;
    iValue += kPromo.getMovesChange() * 20;
    iValue += kPromo.getMoveDiscountChange() * 5;
    iValue += kPromo.getWithdrawalChange() / 2;

    if (kPromo.getEnemyHealChange() > 0)
        iValue += kPromo.getEnemyHealChange() / 2 + getExtraEnemyHeal();
    if (kPromo.getNeutralHealChange() > 0)
        iValue += kPromo.getNeutralHealChange() + getExtraNeutralHeal();
    if (kPromo.getFriendlyHealChange() > 0)
        iValue += kPromo.getFriendlyHealChange() / 2 + getExtraFriendlyHeal();

    iValue += kPromo.getUpgradeDiscount() * 2;

    if (iValue > 0)
        iValue += SyncRandNum(15);

    return iValue;
}

// XXX make sure we include any new UnitAITypes...
int CvUnitAI::AI_promotionValue(PromotionTypes ePromotion)
{
	if (GC.getInfo(ePromotion).isLeader())
	{
		// Don't consume the leader as a regular promotion
		return 0;
	}

    // SuperSpies (TSHEEP): spy promotion value
    if (isSpy())
        return AI_spyPromotionValue(ePromotion);

	int iValue = 0;
	//if (GC.getInfo(ePromotion).isBlitz())
	// <advc.164>
	int iBlitz = GC.getInfo(ePromotion).getBlitz();
	if(iBlitz != 0)
	{
		if(iBlitz < 0)
			iBlitz = 3;
		int iExtraAttacks = std::min(iBlitz, baseMoves() - 1 +
				(getDropRange() > 0 ? 1 : 0));
		if(iExtraAttacks > 0) // </advc.164>
		{
			if ((AI_getUnitAIType() == UNITAI_RESERVE  && baseMoves() > 1) ||
				AI_getUnitAIType() == UNITAI_PARADROP)
			{
				//iValue += 10;
				iValue += 8 * iExtraAttacks; // advc.164
			}
			else
			{
				//iValue += 2;
				iValue += iExtraAttacks; // advc.164
			}
		}
	}

	if (GC.getInfo(ePromotion).isAmphib())
	{
		if (AI_getUnitAIType() == UNITAI_ATTACK ||
			AI_getUnitAIType() == UNITAI_ATTACK_CITY)
		{
			iValue += 5;
		}
		else iValue++;
	}

	if (GC.getInfo(ePromotion).isRiver())
	{
		if (AI_getUnitAIType() == UNITAI_ATTACK ||
			AI_getUnitAIType() == UNITAI_ATTACK_CITY)
		{
			iValue += 5;
		}
		else iValue++;
	}

	if (GC.getInfo(ePromotion).isEnemyRoute())
	{
		if (AI_getUnitAIType() == UNITAI_PILLAGE)
			iValue += 40;
		else if (AI_getUnitAIType() == UNITAI_ATTACK ||
			AI_getUnitAIType() == UNITAI_ATTACK_CITY)
		{
			iValue += 20;
		}
		else if (AI_getUnitAIType() == UNITAI_PARADROP)
			iValue += 10;
		else iValue += 4;
	}

	if (GC.getInfo(ePromotion).isAlwaysHeal())
	{
		if (AI_getUnitAIType() == UNITAI_ATTACK ||
			AI_getUnitAIType() == UNITAI_ATTACK_CITY ||
			AI_getUnitAIType() == UNITAI_PILLAGE ||
			AI_getUnitAIType() == UNITAI_COUNTER ||
			AI_getUnitAIType() == UNITAI_ATTACK_SEA ||
			AI_getUnitAIType() == UNITAI_PIRATE_SEA ||
			AI_getUnitAIType() == UNITAI_ESCORT_SEA ||
			AI_getUnitAIType() == UNITAI_PARADROP)
		{
			iValue += 10;
		}
		else iValue += 8;
	}

	if (GC.getInfo(ePromotion).isHillsDoubleMove())
	{
		if (AI_getUnitAIType() == UNITAI_EXPLORE)
			iValue += 20;
		else iValue += 10;
	}

	if (GC.getInfo(ePromotion).isImmuneToFirstStrikes() &&
		!immuneToFirstStrikes())
	{
		if (AI_getUnitAIType() == UNITAI_ATTACK_CITY)
			iValue += 12;
		else if (AI_getUnitAIType() == UNITAI_ATTACK)
			iValue += 8;
		else iValue += 4;
	}

	int iExtra = 0;
	int iTemp;
	iTemp = GC.getInfo(ePromotion).getVisibilityChange();
	if (AI_getUnitAIType() == UNITAI_EXPLORE_SEA ||
		AI_getUnitAIType() == UNITAI_EXPLORE)
	{
		iValue += (iTemp * 40);
	}
	else if (AI_getUnitAIType() == UNITAI_PIRATE_SEA)
		iValue += (iTemp * 20);

	iTemp = GC.getInfo(ePromotion).getMovesChange();
	if (AI_getUnitAIType() == UNITAI_ATTACK_SEA ||
		AI_getUnitAIType() == UNITAI_PIRATE_SEA ||
		AI_getUnitAIType() == UNITAI_RESERVE_SEA ||
		AI_getUnitAIType() == UNITAI_ESCORT_SEA ||
		AI_getUnitAIType() == UNITAI_EXPLORE_SEA ||
		AI_getUnitAIType() == UNITAI_ASSAULT_SEA ||
		AI_getUnitAIType() == UNITAI_SETTLER_SEA ||
		AI_getUnitAIType() == UNITAI_PILLAGE ||
		AI_getUnitAIType() == UNITAI_ATTACK ||
		AI_getUnitAIType() == UNITAI_PARADROP)
	{
		iValue += (iTemp * 20);
	}
	else iValue += (iTemp * 4);

	iTemp = GC.getInfo(ePromotion).getMoveDiscountChange();
	if (AI_getUnitAIType() == UNITAI_PILLAGE)
		iValue += (iTemp * 10);
	else iValue += (iTemp * 2);

	iTemp = GC.getInfo(ePromotion).getAirRangeChange();
	if (AI_getUnitAIType() == UNITAI_ATTACK_AIR ||
		AI_getUnitAIType() == UNITAI_CARRIER_AIR)
	{
		iValue += (iTemp * 20);
	}
	else if (AI_getUnitAIType() == UNITAI_DEFENSE_AIR)
		iValue += (iTemp * 10);

	iTemp = GC.getInfo(ePromotion).getInterceptChange();
	if (AI_getUnitAIType() == UNITAI_DEFENSE_AIR)
		iValue += (iTemp * 3);
	else if (AI_getUnitAIType() == UNITAI_CITY_SPECIAL ||
		AI_getUnitAIType() == UNITAI_CARRIER_AIR)
	{
		iValue += (iTemp * 2);
	}
	else iValue += (iTemp / 10);

	iTemp = GC.getInfo(ePromotion).getEvasionChange();
	if (AI_getUnitAIType() == UNITAI_ATTACK_AIR ||
		AI_getUnitAIType() == UNITAI_CARRIER_AIR)
	{
		iValue += (iTemp * 3);
	}
	else iValue += (iTemp / 10);

	iTemp = GC.getInfo(ePromotion).getFirstStrikesChange() * 2;
	iTemp += GC.getInfo(ePromotion).getChanceFirstStrikesChange();
	if (AI_getUnitAIType() == UNITAI_RESERVE ||
		AI_getUnitAIType() == UNITAI_COUNTER ||
		AI_getUnitAIType() == UNITAI_CITY_DEFENSE ||
		AI_getUnitAIType() == UNITAI_CITY_COUNTER ||
		AI_getUnitAIType() == UNITAI_CITY_SPECIAL ||
		AI_getUnitAIType() == UNITAI_ATTACK)
	{
		iTemp *= 8;
		iExtra = getExtraChanceFirstStrikes() + getExtraFirstStrikes() * 2;
		iTemp *= 100 + iExtra * 15;
		iTemp /= 100;
		iValue += iTemp;
	}
	else iValue += (iTemp * 5);

	iTemp = GC.getInfo(ePromotion).getWithdrawalChange();
	if (iTemp != 0)
	{
		iExtra = (getUnitInfo().getWithdrawalProbability() + (getExtraWithdrawal() * 4));
		iTemp *= (100 + iExtra);
		iTemp /= 100;
		if (AI_getUnitAIType() == UNITAI_ATTACK_CITY)
		{
			iValue += (iTemp * 4) / 3;
		}
		else if (AI_getUnitAIType() == UNITAI_COLLATERAL ||
			AI_getUnitAIType() == UNITAI_RESERVE ||
			AI_getUnitAIType() == UNITAI_RESERVE_SEA ||
			getLeaderUnitType() != NO_UNIT)
		{
			iValue += iTemp * 1;
		}
		else iValue += (iTemp / 4);
	}

	iTemp = GC.getInfo(ePromotion).getCollateralDamageChange();
	if (iTemp != 0)
	{
		iExtra = (getExtraCollateralDamage());//collateral has no strong synergy (not like retreat)
		iTemp *= (100 + iExtra);
		iTemp /= 100;

		if (AI_getUnitAIType() == UNITAI_COLLATERAL)
			iValue += (iTemp * 1);
		else if (AI_getUnitAIType() == UNITAI_ATTACK_CITY)
			iValue += ((iTemp * 2) / 3);
		else iValue += (iTemp / 8);
	}

	iTemp = GC.getInfo(ePromotion).getBombardRateChange();
	if (AI_getUnitAIType() == UNITAI_ATTACK_CITY)
	{
		iValue += (iTemp * 2);
	}
	else iValue += (iTemp / 8);
	// BETTER_BTS_AI_MOD, Unit AI, 04/26/10, jdog5000: START
	iTemp = GC.getInfo(ePromotion).getEnemyHealChange();
	if (AI_getUnitAIType() == UNITAI_ATTACK ||
		AI_getUnitAIType() == UNITAI_PILLAGE ||
		AI_getUnitAIType() == UNITAI_ATTACK_SEA ||
		AI_getUnitAIType() == UNITAI_PARADROP ||
		AI_getUnitAIType() == UNITAI_PIRATE_SEA)
	// BETTER_BTS_AI_MOD: END
	{
		iValue += (iTemp / 4);
	}
	else iValue += (iTemp / 8);

	iTemp = GC.getInfo(ePromotion).getNeutralHealChange();
	iValue += (iTemp / 8);

	iTemp = GC.getInfo(ePromotion).getFriendlyHealChange();
	if ((AI_getUnitAIType() == UNITAI_CITY_DEFENSE) ||
		  (AI_getUnitAIType() == UNITAI_CITY_COUNTER) ||
		  (AI_getUnitAIType() == UNITAI_CITY_SPECIAL))
	{
		iValue += (iTemp / 4);
	}
	else iValue += (iTemp / 8);

	// BBAI / K-Mod
	if (getDamage() > 0 || ((AI_getBirthmark() % 8 == 0) &&
		(AI_getUnitAIType() == UNITAI_COUNTER ||
		AI_getUnitAIType() == UNITAI_PILLAGE ||
		AI_getUnitAIType() == UNITAI_ATTACK_CITY ||
		AI_getUnitAIType() == UNITAI_RESERVE ||
		AI_getUnitAIType() == UNITAI_PIRATE_SEA ||
		AI_getUnitAIType() == UNITAI_RESERVE_SEA ||
		AI_getUnitAIType() == UNITAI_ASSAULT_SEA)))
	{
	// BBAI / K-Mod
		iTemp = GC.getInfo(ePromotion).getSameTileHealChange() + getSameTileHeal();
		iExtra = getSameTileHeal();

		iTemp *= (100 + iExtra * 5);
		iTemp /= 100;

		if (iTemp > 0)
		{
			if (healRate(false, true) < iTemp)
				iValue += iTemp * (getGroup()->getNumUnits() > 4 ? 4 : 2);
			else iValue += (iTemp / 8);
		}

		iTemp = GC.getInfo(ePromotion).getAdjacentTileHealChange();
		iExtra = getAdjacentTileHeal();
		iTemp *= (100 + iExtra * 5);
		iTemp /= 100;
		if (getSameTileHeal() >= iTemp)
		{
			iValue += (iTemp * (getGroup()->getNumUnits() > 9 ? 4 : 2));
		}
		else iValue += (iTemp / 4);
	}

	// try to use Warlords to create super-medic units
	if (GC.getInfo(ePromotion).getAdjacentTileHealChange() > 0 || GC.getInfo(ePromotion).getSameTileHealChange() > 0)
	{
		/*PromotionTypes eLeader = NO_PROMOTION;
		for (iI = 0; iI < GC.getNumPromotionInfos(); iI++) {
			if (GC.getInfo((PromotionTypes)iI).isLeader())
				eLeader = (PromotionTypes)iI;
		}
		if (isHasPromotion(eLeader) && eLeader != NO_PROMOTION) {
			iValue += GC.getInfo(ePromotion).getAdjacentTileHealChange() + GC.getInfo(ePromotion).getSameTileHealChange();
		}*/ // BtS
		// K-Mod, I've changed the way we work out if we are a leader or not.
		// The original method would break if there was more than one "leader" promotion)
		for (int iI = 0; iI < GC.getNumPromotionInfos(); iI++)
		{
			if (GC.getInfo((PromotionTypes)iI).isLeader() && isHasPromotion((PromotionTypes)iI))
			{
				iValue += GC.getInfo(ePromotion).getAdjacentTileHealChange() + GC.getInfo(ePromotion).getSameTileHealChange();
				break;
			}
		}
		// K-Mod end
	}

	iTemp = GC.getInfo(ePromotion).getCombatPercent();
	UnitAITypes const eAI = AI_getUnitAIType();
	// kmodx: Removed redundant clauses
	if (eAI == UNITAI_ATTACK || eAI == UNITAI_COUNTER ||
		eAI == UNITAI_CITY_COUNTER || eAI == UNITAI_ATTACK_SEA ||
		eAI == UNITAI_PARADROP ||  eAI == UNITAI_PIRATE_SEA ||
		eAI == UNITAI_RESERVE_SEA || eAI == UNITAI_ESCORT_SEA ||
		eAI == UNITAI_CARRIER_SEA || eAI == UNITAI_ATTACK_AIR ||
		eAI == UNITAI_CARRIER_AIR)
	{
		iValue += (iTemp * 2);
	}
	else iValue += (iTemp * 1);

	iTemp = GC.getInfo(ePromotion).getCityAttackPercent();
	if (iTemp != 0)
	{
		if (getUnitInfo().getUnitAIType(UNITAI_ATTACK) || getUnitInfo().getUnitAIType(UNITAI_ATTACK_CITY) || getUnitInfo().getUnitAIType(UNITAI_ATTACK_CITY_LEMMING))
		{
			iExtra = (getUnitInfo().getCityAttackModifier() + (getExtraCityAttackPercent() * 2));
			iTemp *= (100 + iExtra);
			iTemp /= 100;
			if (AI_getUnitAIType() == UNITAI_ATTACK_CITY)
			{
				iValue += (iTemp * 1);
			}
			else iValue -= iTemp / 4;
		}
	}

	iTemp = GC.getInfo(ePromotion).getCityDefensePercent();
	if (iTemp != 0)
	{
		if ((AI_getUnitAIType() == UNITAI_CITY_DEFENSE) ||
			  (AI_getUnitAIType() == UNITAI_CITY_SPECIAL))
		{
			iExtra = getUnitInfo().getCityDefenseModifier() + (getExtraCityDefensePercent() * 2);
			iValue += ((iTemp * (100 + iExtra)) / 100);
		}
		else iValue += (iTemp / 4);
	}

	iTemp = GC.getInfo(ePromotion).getHillsAttackPercent();
	if (iTemp != 0)
	{
		iExtra = getExtraHillsAttackPercent();
		iTemp *= (100 + iExtra * 2);
		iTemp /= 100;
		if ((AI_getUnitAIType() == UNITAI_ATTACK) ||
			(AI_getUnitAIType() == UNITAI_COUNTER))
		{
			iValue += (iTemp / 4);
		}
		else iValue += (iTemp / 16);
	}

	iTemp = GC.getInfo(ePromotion).getHillsDefensePercent();
	if (iTemp != 0)
	{
		iExtra = (getUnitInfo().getHillsDefenseModifier() + (getExtraHillsDefensePercent() * 2));
		iTemp *= (100 + iExtra);
		iTemp /= 100;
		if (AI_getUnitAIType() == UNITAI_CITY_DEFENSE)
		{
			if (getPlot().isCity() && getPlot().isHills())
				iValue += (iTemp * 4) / 3;
		}
		else if (AI_getUnitAIType() == UNITAI_COUNTER)
		{
			if (getPlot().isHills())
				iValue += (iTemp / 4);
			else iValue++;
		}
		else iValue += (iTemp / 16);
	}

    // doc: open terrain attack
    iTemp = GC.getInfo(ePromotion).getPlainsAttackPercent();
    if (iTemp != 0)
    {
        iExtra = getExtraPlainsAttackPercent();
        iTemp *= (100 + iExtra * 2);
        iTemp /= 100;
        if ((AI_getUnitAIType() == UNITAI_ATTACK) ||
            (AI_getUnitAIType() == UNITAI_COUNTER))
        {
            iValue += (iTemp / 5);
        }
        else
        {
            iValue += (iTemp / 20);
        }
    }

    // doc: open terrain defense
    iTemp = GC.getInfo(ePromotion).getPlainsDefensePercent();
    if (iTemp != 0)
    {
        iExtra = getExtraPlainsDefensePercent();
        iTemp *= (100 + iExtra * 2);
        iTemp /= 100;
        if ((AI_getUnitAIType() == UNITAI_ATTACK) ||
            (AI_getUnitAIType() == UNITAI_COUNTER))
        {
            iValue += (iTemp / 5);
        }
        else
        {
            iValue += (iTemp / 20);
        }
    }

    // doc: river attack percent
    iTemp = GC.getInfo(ePromotion).getRiverAttackPercent();
    if (iTemp != 0)
    {
        iExtra = getExtraRiverAttackPercent();
        iTemp *= (100 + iExtra * 2);
        iTemp /= 100;
        if ((AI_getUnitAIType() == UNITAI_ATTACK) ||
            (AI_getUnitAIType() == UNITAI_COUNTER))
        {
            iValue += (iTemp / 5);
        }
        else
        {
            iValue += (iTemp / 20);
        }
    }

	// advc.099e: Commented out
	/*iTemp = GC.getInfo(ePromotion).getRevoltProtection();
	if ((AI_getUnitAIType() == UNITAI_CITY_DEFENSE) ||
		(AI_getUnitAIType() == UNITAI_CITY_COUNTER) ||
		(AI_getUnitAIType() == UNITAI_CITY_SPECIAL)) {
		if (iTemp > 0) {
			PlayerTypes eOwner = getPlot().calculateCulturalOwner();
			if (eOwner != NO_PLAYER && GET_PLAYER(eOwner).getTeam() != GET_PLAYER(getOwner()).getTeam())
				iValue += (iTemp / 2);
		}
	}*/

	iTemp = GC.getInfo(ePromotion).getCollateralDamageProtection();
	if (AI_getUnitAIType() == UNITAI_CITY_DEFENSE ||
		AI_getUnitAIType() == UNITAI_CITY_COUNTER ||
		AI_getUnitAIType() == UNITAI_CITY_SPECIAL)
	{
		iValue += (iTemp / 3);
	}
	else if ((AI_getUnitAIType() == UNITAI_ATTACK) ||
		(AI_getUnitAIType() == UNITAI_COUNTER))
	{
		iValue += (iTemp / 4);
	}
	else iValue += (iTemp / 8);

	iTemp = GC.getInfo(ePromotion).getPillageChange();
	if (AI_getUnitAIType() == UNITAI_PILLAGE ||
		AI_getUnitAIType() == UNITAI_ATTACK_SEA ||
		AI_getUnitAIType() == UNITAI_PIRATE_SEA)
	{
		iValue += (iTemp / 4);
	}
	else iValue += (iTemp / 16);

	iTemp = GC.getInfo(ePromotion).getUpgradeDiscount();
	iValue += (iTemp / 16);

	iTemp = GC.getInfo(ePromotion).getExperiencePercent();
	if (AI_getUnitAIType() == UNITAI_ATTACK ||
		AI_getUnitAIType() == UNITAI_ATTACK_SEA ||
		AI_getUnitAIType() == UNITAI_PIRATE_SEA ||
		AI_getUnitAIType() == UNITAI_RESERVE_SEA ||
		AI_getUnitAIType() == UNITAI_ESCORT_SEA ||
		AI_getUnitAIType() == UNITAI_CARRIER_SEA ||
		AI_getUnitAIType() == UNITAI_MISSILE_CARRIER_SEA)
	{
		iValue += (iTemp * 1);
	}
	else iValue += (iTemp / 2);

	iTemp = GC.getInfo(ePromotion).getKamikazePercent();
	if (AI_getUnitAIType() == UNITAI_ATTACK_CITY)
		iValue += (iTemp / 16);
	else iValue += (iTemp / 64);

	FOR_EACH_ENUM(Terrain)
	{
		iTemp = GC.getInfo(ePromotion).getTerrainAttackPercent(eLoopTerrain);
		if (iTemp != 0)
		{
			iExtra = getExtraTerrainAttackPercent(eLoopTerrain);
			iTemp *= (100 + iExtra * 2);
			iTemp /= 100;
			if ((AI_getUnitAIType() == UNITAI_ATTACK) ||
				(AI_getUnitAIType() == UNITAI_COUNTER))
			{
				iValue += (iTemp / 4);
			}
			else iValue += (iTemp / 16);
		}

		iTemp = GC.getInfo(ePromotion).getTerrainDefensePercent(eLoopTerrain);
		if (iTemp != 0)
		{
			iExtra =  getExtraTerrainDefensePercent(eLoopTerrain);
			iTemp *= (100 + iExtra);
			iTemp /= 100;
			if (AI_getUnitAIType() == UNITAI_COUNTER)
			{
				if (getPlot().getTerrainType() == eLoopTerrain)
					iValue += (iTemp / 4);
				else iValue++;
			}
			else iValue += (iTemp / 16);
		}

		if (GC.getInfo(ePromotion).getTerrainDoubleMove(eLoopTerrain))
		{
			if (AI_getUnitAIType() == UNITAI_EXPLORE)
				iValue += 20;
			else if (AI_getUnitAIType() == UNITAI_ATTACK ||
				AI_getUnitAIType() == UNITAI_PILLAGE)
			{
				iValue += 10;
			}
			else iValue += 1;
		}
	}

	FOR_EACH_ENUM(Feature)
	{
		iTemp = GC.getInfo(ePromotion).getFeatureAttackPercent(eLoopFeature);
		if (iTemp != 0)
		{
			iExtra = getExtraFeatureAttackPercent(eLoopFeature);
			iTemp *= (100 + iExtra * 2);
			iTemp /= 100;
			if ((AI_getUnitAIType() == UNITAI_ATTACK) ||
				(AI_getUnitAIType() == UNITAI_COUNTER))
			{
				iValue += (iTemp / 4);
			}
			else iValue += (iTemp / 16);
		}

		iTemp = GC.getInfo(ePromotion).getFeatureDefensePercent(eLoopFeature);
		if (iTemp != 0)
		{
			iExtra = getExtraFeatureDefensePercent(eLoopFeature);
			iTemp *= (100 + iExtra * 2);
			iTemp /= 100;

			if (!noDefensiveBonus())
			{
				if (AI_getUnitAIType() == UNITAI_COUNTER)
				{
					if (getPlot().getFeatureType() == eLoopFeature)
						iValue += (iTemp / 4);
					else iValue++;
				}
				else iValue += (iTemp / 16);
			}
		}

		if (GC.getInfo(ePromotion).getFeatureDoubleMove(eLoopFeature))
		{
			if (AI_getUnitAIType() == UNITAI_EXPLORE)
				iValue += 20;
			else if (AI_getUnitAIType() == UNITAI_ATTACK ||
				AI_getUnitAIType() == UNITAI_PILLAGE)
			{
				iValue += 10;
			}
			else iValue += 1;
		}
	}

	int iOtherCombat = 0;
	int iSameCombat = 0;

	FOR_EACH_ENUM(UnitCombat)
	{
		if (eLoopUnitCombat == getUnitCombatType())
			iSameCombat += unitCombatModifier(eLoopUnitCombat);
		else iOtherCombat += unitCombatModifier(eLoopUnitCombat);
	}
	FOR_EACH_ENUM(UnitCombat)
	{
		iTemp = GC.getInfo(ePromotion).getUnitCombatModifierPercent(eLoopUnitCombat);
		int iCombatWeight = 0;
		//Fighting their own kind
		if (eLoopUnitCombat== getUnitCombatType())
		{
			if (iSameCombat >= iOtherCombat)
				iCombatWeight = 70;//"axeman takes formation"
			else iCombatWeight = 30;
		}
		else
		{
			//fighting other kinds
			if (unitCombatModifier(eLoopUnitCombat) > 10)
				iCombatWeight = 70;//"spearman takes formation"
			else iCombatWeight = 30;
		}

		iCombatWeight *= GET_PLAYER(getOwner()).AI_getUnitCombatWeight(eLoopUnitCombat);
		iCombatWeight /= 100;

		if (AI_getUnitAIType() == UNITAI_COUNTER ||
			AI_getUnitAIType() == UNITAI_CITY_COUNTER)
		{
			iValue += (iTemp * iCombatWeight) / 50;
		}
		else if (AI_getUnitAIType() == UNITAI_ATTACK ||
				AI_getUnitAIType() == UNITAI_RESERVE)
		{
			iValue += (iTemp * iCombatWeight) / 100;
		}
		else iValue += (iTemp * iCombatWeight) / 200;
	}

	FOR_EACH_ENUM(Domain)
	{
		//WTF? why float and cast to int?
		//iTemp = (int)((GC.getInfo(ePromotion).getDomainModifierPercent(eLoopDomain) + getExtraDomainModifier(eLoopDomain) * 100.0f);
		iTemp = GC.getInfo(ePromotion).getDomainModifierPercent(eLoopDomain);
		if (AI_getUnitAIType() == UNITAI_COUNTER)
			iValue += (iTemp * 1);
		else if (AI_getUnitAIType() == UNITAI_ATTACK ||
			AI_getUnitAIType() == UNITAI_RESERVE)
		{
			iValue += (iTemp / 2);
		}
		else iValue += (iTemp / 8);
	}
	if (iValue > 0)
		iValue += SyncRandNum(15);
	return iValue;
}


bool CvUnitAI::AI_shadow(UnitAITypes eUnitAI, int iMax, int iMaxRatio,
	bool bWithCargoOnly, bool bOutsideCityOnly, int iMaxPath)
{
	PROFILE_FUNC();

	int iBestValue = 0;
	CvUnit const* pBestUnit = NULL;
	FOR_EACH_UNIT(pLoopUnit, GET_PLAYER(getOwner()))
	{	// advc: Reduce indentation
		if (pLoopUnit != this && AI_plotValid(pLoopUnit->plot()) &&
			pLoopUnit->isGroupHead() && !pLoopUnit->isCargo() &&
			pLoopUnit->AI_getUnitAIType() == eUnitAI &&
			pLoopUnit->getGroup()->baseMoves() <= getGroup()->baseMoves())
		{
			if (!bWithCargoOnly || pLoopUnit->getGroup()->hasCargo())
			{
				// BETTER_BTS_AI_MOD, Naval AI, 12/08/08, jdog5000: START
				if (bOutsideCityOnly && pLoopUnit->getPlot().isCity())
					continue;
				// BETTER_BTS_AI_MOD: END
				int iShadowerCount = GET_PLAYER(getOwner()).AI_unitTargetMissionAIs(
						*pLoopUnit, MISSIONAI_SHADOW, getGroup());
				if ((iMax == -1 || iShadowerCount < iMax) &&
					 (iMaxRatio == -1 || iShadowerCount == 0 ||
					 iMaxRatio >= (100 * iShadowerCount) /
					 std::max(1, pLoopUnit->getGroup()->countNumUnitAIType(eUnitAI)) ))
				{
					//if (!pLoopUnit->getPlot().isVisibleEnemyUnit(this)) { // advc.opt: pLoopUnit is our unit; can't coexist with any enemies.
					int iPathTurns;
					if (generatePath(pLoopUnit->getPlot(), NO_MOVEMENT_FLAGS,
						true, &iPathTurns, iMaxPath))
					{
						//if (iPathTurns <= iMaxPath) //XXX
						// BETTER_BTS_AI_MOD, Naval AI, 12/08/08, jdog5000: (uncommented)
						if (iPathTurns <= iMaxPath)
						{
							int iValue = 1 + pLoopUnit->getGroup()->getCargo();
							iValue *= 1000;
							iValue /= 1 + iPathTurns;
							if (iValue > iBestValue)
							{
								iBestValue = iValue;
								pBestUnit = pLoopUnit;
							}
						}
					}
				}
			}
		}
	}

	if (pBestUnit != NULL)
	{
		if (atPlot(pBestUnit->plot()))
		{
			getGroup()->pushMission(MISSION_SKIP, -1, -1, NO_MOVEMENT_FLAGS,
					false, false, MISSIONAI_SHADOW, NULL, pBestUnit);
			return true;
		}
		else
		{
			getGroup()->pushMission(MISSION_MOVE_TO_UNIT, pBestUnit->getOwner(),
					pBestUnit->getID(), NO_MOVEMENT_FLAGS, false, false,
					MISSIONAI_SHADOW, NULL, pBestUnit);
			return true;
		}
	}

	return false;
}

// K-Mod. One group function to rule them all.
bool CvUnitAI::AI_omniGroup(UnitAITypes eUnitAI, int iMaxGroup, int iMaxOwnUnitAI,
	bool bStackOfDoom, MovementFlags eFlags, int iMaxPath, bool bMergeGroups, bool bSafeOnly,
	bool bIgnoreFaster, bool bIgnoreOwnUnitType, bool bBiggerOnly, int iMinUnitAI,
	bool bWithCargoOnly, bool bIgnoreBusyTransports)
{
	PROFILE_FUNC();

	eFlags &= ~MOVE_DECLARE_WAR; // Don't consider war when we just want to group

	if (isCargo())
		return false;

	if (!AI_canGroupWithAIType(eUnitAI))
		return false;

	if (getDomainType() == DOMAIN_LAND && !canMoveAllTerrain() &&
		getArea().getNumAIUnits(getOwner(), eUnitAI) <= 0)
	{
		return false;
	}
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());
	/*	<advc.057> Except for assault groups, the head unit should have the
		most restrictive impassable types. */
	int const iOurGroupFirstVal = AI_groupFirstVal();
	uint uiOurMaxImpassables = kOwner.AI_unitImpassables(getUnitType());
	if (AI_getUnitAIType() == UNITAI_ASSAULT_SEA)
	{
		for (CLLNode<IDInfo> const* pUnitNode = // We're the head; already done.
			getGroup()->nextUnitNode(getGroup()->headUnitNode()); // </advc.057>
			pUnitNode != NULL; pUnitNode = getGroup()->nextUnitNode(pUnitNode))
		{
			CvUnit const& kImpassUnit = *::getUnit(pUnitNode->m_data);
			uiOurMaxImpassables = std::max(uiOurMaxImpassables,
					kOwner.AI_unitImpassables(kImpassUnit.getUnitType()));
		}
	}
	CvUnit* pBestUnit = NULL;
	int iBestValue = MAX_INT;
	FOR_EACH_GROUPAI_VAR(pLoopGroup, kOwner)
	{
		CvUnitAI* pLoopUnit = pLoopGroup->AI_getHeadUnit();
		if (pLoopUnit == NULL)
			continue;
		CvPlot const& kLoopPlot = pLoopUnit->getPlot();
		if (!AI_plotValid(kLoopPlot))
			continue;
		if (iMaxPath == 0 && !at(kLoopPlot)) // advc.opt (tbd.): Should arguably treat iMaxPath==0 upfront
			continue;
		/*if (getDomainType() != DOMAIN_LAND || canMoveAllTerrain() ||
			kPlot.isArea(getArea())) {*/ // advc.opt: Redundant after AI_plotValid
		if (!AI_allowGroup(*pLoopUnit, eUnitAI))
			continue;

		/*	K-Mod. I've restructed this wad of conditions so that it is easier for me to read.
				advc: Made a few more edits - parts of it were still off-screen ...
			((removed ((heaps) of parentheses) (etc)).)
			also, I've rearranged the order to be slightly faster for failed checks.
			Note: the iMaxGroups & OwnUnitAI check is apparently off-by-one.
			This is for backwards compatibility for the original code. */
		if ((!bSafeOnly || !isEnemy(kLoopPlot))
			&&
			(!bWithCargoOnly || pLoopUnit->getGroup()->hasCargo())
			&&
			(!bBiggerOnly || !bMergeGroups ||
			pLoopGroup->getNumUnits() >= getGroup()->getNumUnits())
			&&
			(!bIgnoreFaster || pLoopGroup->baseMoves() <= baseMoves())
			&&
			(!bIgnoreOwnUnitType || pLoopUnit->getUnitType() != getUnitType())
			&&
			(!bIgnoreBusyTransports || !pLoopGroup->hasCargo() ||
			(pLoopGroup->AI_getMissionAIType() != MISSIONAI_ASSAULT &&
			pLoopGroup->AI_getMissionAIType() != MISSIONAI_REINFORCE))
			&&
			(iMinUnitAI == -1 || pLoopGroup->countNumUnitAIType(eUnitAI) >= iMinUnitAI)
			&&
			(iMaxOwnUnitAI == -1 ||
			(bMergeGroups ? std::max(0, getGroup()->countNumUnitAIType(AI_getUnitAIType()) - 1) : 0) +
			pLoopGroup->countNumUnitAIType(AI_getUnitAIType()) <=
			iMaxOwnUnitAI + (bStackOfDoom ? AI_stackOfDoomExtra() : 0))
			&&
			(iMaxGroup == -1 || (bMergeGroups ? getGroup()->getNumUnits() - 1 : 0) +
			pLoopGroup->getNumUnits() +
			kOwner.AI_unitTargetMissionAIs(*pLoopUnit, MISSIONAI_GROUP, getGroup()) <=
			iMaxGroup + (bStackOfDoom ? AI_stackOfDoomExtra() : 0))
			&&
			(pLoopGroup->AI_getMissionAIType() != MISSIONAI_GUARD_CITY ||
			!pLoopGroup->getPlot().isCity() ||
			pLoopGroup->getPlot().plotCount(PUF_isMissionAIType, MISSIONAI_GUARD_CITY, -1, getOwner()) >
			pLoopGroup->getPlot().AI_getPlotCity()->AI_minDefenders())
			)
		{
			FAssert(!kLoopPlot.isVisibleEnemyUnit(this));
			//if (iOurMaxImpassableCount > 0 || AI_getUnitAIType() == UNITAI_ASSAULT_SEA) { ...
			{	// <advc.057> Check their impassable count even if ours is 0
				CLLNode<IDInfo> const* pUnitNode = pLoopGroup->headUnitNode();
				CvUnitAI const& kHeadUnit = *::AI_getUnit(pUnitNode->m_data);
				uint uiTheirMaxImpassables = kOwner.AI_unitImpassables(
						kHeadUnit.getUnitType());
				/*	Assault groups aren't always formed through this function;
					can't rely on head having the most impassable types. */
				if (kHeadUnit.AI_getUnitAIType() == UNITAI_ASSAULT_SEA)
				{
					for (pUnitNode = getGroup()->nextUnitNode(pUnitNode);
						pUnitNode != NULL; pUnitNode = getGroup()->nextUnitNode(pUnitNode))
					{
						CvUnit const& kUnit = *::getUnit(pUnitNode->m_data);
						uiTheirMaxImpassables = std::max(uiTheirMaxImpassables,
								kOwner.AI_unitImpassables(kUnit.getUnitType()));
					}
				}
				int const iTheirGroupFirstValue = kHeadUnit.AI_groupFirstVal();
				/*	Disallow the group if we can't rule out that the impassable count
					of the head will decrease. (Should really check for set inclusion,
					i.e. the set of impassables of the leader needs to include all
					impassables of the group.) */
				if ((iTheirGroupFirstValue >= iOurGroupFirstVal &&
					uiTheirMaxImpassables < uiOurMaxImpassables) ||
					(iTheirGroupFirstValue <= iOurGroupFirstVal &&
					uiTheirMaxImpassables > uiOurMaxImpassables))
				{
					continue;
				}
			} // </advc.057>
			int iPathTurns = 0;
			if (at(kLoopPlot) ||
				generatePath(kLoopPlot, eFlags, true, &iPathTurns, iMaxPath))
			{
				int iCost = 100 * (iPathTurns * iPathTurns + 1);
				iCost *= 4 + pLoopGroup->getCargo();
				iCost /= 2 + pLoopGroup->getNumUnits();
				/*int iSizeMod = 10*std::max(getGroup()->getNumUnits(), pLoopGroup->getNumUnits());
				iSizeMod /= std::min(getGroup()->getNumUnits(), pLoopGroup->getNumUnits());
				iCost *= iSizeMod * iSizeMod;
				iCost /= 1000; */
				if (iCost < iBestValue)
				{
					iBestValue = iCost;
					pBestUnit = pLoopUnit;
				}
			}
		}
	}
	if (pBestUnit == NULL)
		return false; // advc

	if (!atPlot(pBestUnit->plot()))
	{
		if (!bMergeGroups && getGroup()->getNumUnits() > 1)
		{	/*	might as well leave our current group behind
				since they won't be merging anyway. */
			joinGroup(NULL);
		}
		getGroup()->pushMission(MISSION_MOVE_TO_UNIT, pBestUnit->getOwner(),
				pBestUnit->getID(), eFlags, false, false, MISSIONAI_GROUP, NULL, pBestUnit);
	}
	if (atPlot(pBestUnit->plot()))
	{
		if (bMergeGroups)
			getGroup()->mergeIntoGroup(pBestUnit->getGroup());
		else joinGroup(pBestUnit->getGroup());
	}
	return true;
} // K-Mod end

// Returns true if a group was joined or a mission was pushed...
bool CvUnitAI::AI_group(UnitAITypes eUnitAI, int iMaxGroup, int iMaxOwnUnitAI,
	int iMinUnitAI, bool bIgnoreFaster, bool bIgnoreOwnUnitType, bool bStackOfDoom,
	int iMaxPath, bool bAllowRegrouping,
	/*  BETTER_BTS_AI_MOD, Unit AI, 02/22/10, jdog5000:
		Added new options to aid transport grouping */
	bool bWithCargoOnly, bool bInCityOnly, MissionAITypes eIgnoreMissionAIType)
{
	// K-Mod. I've completely gutted this function. It's now basically just a wrapper for AI_omniGroup.
	// This is part of the process of phasing the function out.

	// unsupported features:
	FAssert(!bInCityOnly);
	FAssert(eIgnoreMissionAIType == NO_MISSIONAI || (eUnitAI == UNITAI_ASSAULT_SEA && eIgnoreMissionAIType == MISSIONAI_ASSAULT));
	// .. and now the function.

	if (!bAllowRegrouping && getGroup()->getNumUnits() > 1)
		return false;

	return AI_omniGroup(eUnitAI, iMaxGroup, iMaxOwnUnitAI, bStackOfDoom, NO_MOVEMENT_FLAGS,
			iMaxPath, true, true, bIgnoreFaster, bIgnoreOwnUnitType, false, iMinUnitAI,
			bWithCargoOnly, eIgnoreMissionAIType == MISSIONAI_ASSAULT);
}


bool CvUnitAI::AI_groupMergeRange(UnitAITypes eUnitAI, int iMaxRange, bool bBiggerOnly, bool bAllowRegrouping, bool bIgnoreFaster)
{
	// K-Mod. I've completely gutted this function. It's now basically just a wrapper for AI_omniGroup.
	// This is part of the process of phasing the function out.

	if (isCargo())
	{
		return false;
	}

	if (!bAllowRegrouping)
	{
		if (getGroup()->getNumUnits() > 1)
		{
			return false;
		}
	}

	// approximate max path based on range.
	int iMaxPath = 1;
	while (AI_searchRange(iMaxPath) < iMaxRange)
		iMaxPath++;

	return AI_omniGroup(eUnitAI, -1, -1, false, NO_MOVEMENT_FLAGS,
			iMaxPath, true, false, bIgnoreFaster, false, bBiggerOnly);
}

/*  K-Mod
	Look for the nearest suitable transport. Return a pointer to the transport unit.
	(the bulk of this function was moved straight out of AI_load.
	I've fixed it up a bit, but I didn't write most of it.) */
CvUnit* CvUnitAI::AI_findTransport(UnitAITypes eUnitAI, MovementFlags eFlags,
	int iMaxPath, UnitAITypes ePassengerAI, int iMinCargo, int iMinCargoSpace,
	int iMaxCargoSpace, int iMaxCargoOurUnitAI)
{
	PROFILE_FUNC(); // advc.opt
	/*if (getDomainType() == DOMAIN_LAND && !canMoveAllTerrain()) {
		if (getArea().getNumAIUnits(getOwner(), eUnitAI) == 0)
			return false;
	}*/ // disabled, because this would exclude boats sailing on the coast.

	// K-Mod
	if (eUnitAI != NO_UNITAI && GET_PLAYER(getOwner()).AI_getNumAIUnits(eUnitAI) == 0)
		return NULL; // kmodx: was "false"
	// K-Mod end

	int iBestValue = MAX_INT;
	CvUnit* pBestUnit = 0;
	const int iLoadMissionAICount = 4;
	MissionAITypes aeLoadMissionAI[iLoadMissionAICount] = {
			MISSIONAI_LOAD_ASSAULT, MISSIONAI_LOAD_SETTLER,
			MISSIONAI_LOAD_SPECIAL, MISSIONAI_ATTACK_SPY };
	int iCurrentGroupSize = getGroup()->getNumUnits();
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());
	FOR_EACH_UNITAI_VAR(pTransport, kOwner)
	{	// <K-Mod>
		if (pTransport->cargoSpace() <= 0 || (!sameArea(*pTransport) &&
			!pTransport->getPlot().isAdjacentToArea(getArea())) ||
			!canLoadOnto(*pTransport, pTransport->getPlot()))
		{
			continue;
		} // </K-Mod>
		UnitAITypes eTransportAI = pTransport->AI_getUnitAIType();
		if (eUnitAI != NO_UNITAI && eTransportAI != eUnitAI)
			continue;

		int iCargoSpaceAvailable = pTransport->cargoSpaceAvailable(
				getSpecialUnitType(), getDomainType());
		// advc.opt: Check for 0 space before counting TargetMissionAIs
		if (iCargoSpaceAvailable <= 0)
			continue;
		iCargoSpaceAvailable -= kOwner.AI_unitTargetMissionAIs(
				*pTransport, aeLoadMissionAI, iLoadMissionAICount, getGroup());
		if (iCargoSpaceAvailable <= 0)
			continue;
		if ((ePassengerAI == NO_UNITAI ||
			pTransport->getUnitAICargo(ePassengerAI) > 0) &&
			(iMinCargo == -1 || pTransport->getCargo() >= iMinCargo))
		{	// <advc.040> Leave space for Settler and protection
			if(eTransportAI == UNITAI_SETTLER_SEA && eUnitAI == UNITAI_SETTLER_SEA &&
				(ePassengerAI == UNITAI_WORKER ||
				AI_getUnitAIType() == UNITAI_WORKER) &&
				pTransport->cargoSpace() -
				pTransport->getUnitAICargo(UNITAI_WORKER) <= 2)
			{
				continue;
			} // </advc.040>
			// Use existing count of cargo space available
			if ((iMinCargoSpace == -1 || iCargoSpaceAvailable >= iMinCargoSpace) &&
				(iMaxCargoSpace == -1 || iCargoSpaceAvailable <= iMaxCargoSpace))
			{
				if (iMaxCargoOurUnitAI == -1 ||
					pTransport->getUnitAICargo(AI_getUnitAIType()) <= iMaxCargoOurUnitAI)
				{	// <advc.046> Don't join a pickup-stranded mission
					CvUnit* u = pTransport->AI_getGroup()->AI_getMissionAIUnit();
					if(u != NULL && u->getPlot().getTeam() != getTeam() && !at(u->getPlot()))
					{
						continue;
					} // </advc.046>
					//if (!pLoopUnit->getPlot().isVisibleEnemyUnit(this)) { // advc.opt: It's our unit; enemies can't coexist.
					CvPlot* pUnitTargetPlot = pTransport->AI_getGroup()->AI_getMissionAIPlot();
					if (pUnitTargetPlot == NULL || pUnitTargetPlot->getTeam() == getTeam() ||
						(!pUnitTargetPlot->isOwned() ||
						!AI_isPotentialEnemyOf(pUnitTargetPlot->getTeam(), *pUnitTargetPlot)))
					{
						int iPathTurns = 0;
						if (at(pTransport->getPlot()) ||
							generatePath(pTransport->getPlot(), eFlags, true,
							&iPathTurns, iMaxPath))
						{
							// prefer a transport that can hold as much of our group as possible
							int iValue = 5 * std::max(0,
									iCurrentGroupSize - iCargoSpaceAvailable) + iPathTurns;
							if (iValue < iBestValue)
							{
								iBestValue = iValue;
								pBestUnit = pTransport;
							}
						}
					}
				}
			}
		}
	}
	return pBestUnit;
} // K-Mod end

// Returns true if we loaded onto a transport or a mission was pushed...
bool CvUnitAI::AI_load(UnitAITypes eUnitAI, MissionAITypes eMissionAI,
	UnitAITypes eTransportedUnitAI, int iMinCargo, int iMinCargoSpace,
	int iMaxCargoSpace, int iMaxCargoOurUnitAI, MovementFlags eFlags,
	int iMaxPath,
	/*  BETTER_BTS_AI_MOD, War tactics AI, Unit AI, 04/18/10, jdog5000
		(and various changes in the body) */  // advc: Restructured (untangled) the body a bit
	int iMaxTransportPath)
{
	PROFILE_FUNC();

	if (getCargo() > 0)
		return false;

	if (isCargo())
	{
		getGroup()->pushMission(MISSION_SKIP);
		return true;
	}
	// K-Mod
	CvUnit* pBestUnit = AI_findTransport(eUnitAI, eFlags, iMaxPath,
			eTransportedUnitAI, iMinCargo, iMinCargoSpace, iMaxCargoSpace,
			iMaxCargoOurUnitAI); // K-Mod end
	if (pBestUnit == NULL)
		return false;

	if (iMaxTransportPath < MAX_INT &&
		(eUnitAI == UNITAI_ASSAULT_SEA || eUnitAI == UNITAI_SPY_SEA)) // K-Mod
	{
		if(isBarbarian())
		{	// advc: I don't think iMaxTransportPath is ever set for Barbarians anyway
			FAssert(!isBarbarian());
			return false;
		}
		// Can transport reach enemy in requested time
		bool bFoundEnemyPlotInRange = false;
		/*	K-Mod. use a separate pathfinder for the transports,
			so that we don't reset our current path data. */
		//GroupPathFinder tempFinder;
		GroupPathFinder& tempFinder = CvSelectionGroup::getClearPathFinder(); // advc.opt
		tempFinder.setGroup(*pBestUnit->getGroup(),
				eFlags & MOVE_DECLARE_WAR, iMaxTransportPath, GC.getMOVE_DENOMINATOR());
		// K-Mod end
		CvTeamAI const& kOurTeam = GET_TEAM(getTeam()); // advc
		for (SquareIter it(*pBestUnit, iMaxTransportPath * pBestUnit->baseMoves());
			!bFoundEnemyPlotInRange && it.hasNext(); ++it)
		{
			// (BtS had used plotXY(getX(), getY(), iDX, iDY) here - a bug that K-Mod fixed)
			CvPlot const& p = *it;
			if (p.isCoastalLand() && p.isOwned() &&
				//isPotentialEnemy(p.getTeam(), &p) &&
				kOurTeam.AI_mayAttack(p.getTeam()) && // advc
				p.getArea().getCitiesPerPlayer(p.getOwner()) > 0)
			{
				/*  Transport cannot enter land plot without cargo, so
					generatePath only works properly if land units are already loaded */
				FOR_EACH_ADJ_PLOT(getPlot())
				{
					if (!pAdj->isWater())
						continue;
					//if (pBestUnit->generatePath(pAdjacentPlot, 0, true, &iPathTurns, iMaxTransportPath))
					if (tempFinder.generatePath(*pAdj)) // K-Mod
					{
						/*if (pBestUnit->getPathLastNode()->m_iData1 == 0)
							iPathTurns++;*/  // <K-Mod>
						int iPathTurns = tempFinder.getPathTurns();
						if (tempFinder.getFinalMoves() == 0)
							iPathTurns++; // </K-Mod>
						if (iPathTurns <= iMaxTransportPath)
						{
							bFoundEnemyPlotInRange = true;
							break;
						}
					}
				}
			}
		}
		if (!bFoundEnemyPlotInRange)
			return false;
	}

	if (atPlot(pBestUnit->plot()))
	{
		CvSelectionGroup* pRemainderGroup = NULL; // K-Mod renamed from 'pOtherGroup'
		getGroup()->setTransportUnit(pBestUnit, &pRemainderGroup); // XXX is this dangerous (not pushing a mission...) XXX air units?
		// <advc.003u>
		if (pRemainderGroup == NULL || pRemainderGroup->getNumUnits() <= 0)
			return true;
		CvSelectionGroupAI& kRemainderGroup = pRemainderGroup->AI(); // </advc.003u>
		// If part of large group loaded, then try to keep loading the rest
		if (eUnitAI == UNITAI_ASSAULT_SEA && eMissionAI == MISSIONAI_LOAD_ASSAULT)
		{
			CvUnitAI& kRemainderHead = *kRemainderGroup.AI_getHeadUnit(); // advc
			if (kRemainderGroup.getHeadUnitAIType() == AI_getUnitAIType())
			{
				if (kRemainderHead.AI_load(eUnitAI, eMissionAI, eTransportedUnitAI,
					iMinCargo, iMinCargoSpace, iMaxCargoSpace, iMaxCargoOurUnitAI,
					eFlags, 0, iMaxTransportPath))
				{
					kRemainderGroup.AI_setForceSeparate(false); // K-Mod
				}
			}
			else if (eTransportedUnitAI == NO_UNITAI && iMinCargo < 0 &&
				iMinCargoSpace < 0 && iMaxCargoSpace < 0 && iMaxCargoOurUnitAI < 0)
			{
				if (kRemainderHead.AI_load(eUnitAI, eMissionAI, NO_UNITAI,
					-1, -1, -1, -1, eFlags, 0, iMaxTransportPath))
				{
					kRemainderGroup.AI_setForceSeparate(false); // K-Mod
				}
			}
		}
		// K-Mod - just for efficiency, I'll take care of the force separate stuff here.
		if (kRemainderGroup.AI_isForceSeparate())
			kRemainderGroup.AI_separate();
		// K-Mod end
		return true;
	}
	// BBAI TODO: To split or not to split?
	// K-Mod. How about this:
	// Split the group only if it is going to take more than 1 turn to get to the transport.
	if (generatePath(pBestUnit->getPlot(), eFlags, true, NULL, 1))
	{
		// only 1 turn. Don't split.
		getGroup()->pushMission(MISSION_MOVE_TO_UNIT,
				pBestUnit->getOwner(), pBestUnit->getID(),
				eFlags, false, false, eMissionAI, NULL, pBestUnit);
		return true;
	} // K-Mod end
	// (bbai code. split the group)
	int iCargoSpaceAvailable = pBestUnit->cargoSpaceAvailable(
			getSpecialUnitType(), getDomainType());
	FAssertMsg(iCargoSpaceAvailable > 0, "best unit has no space");

	// split our group to fit on the transport
	CvSelectionGroup* pRemainderGroup = NULL;
	CvSelectionGroup* pSplitGroup = getGroup()->splitGroup(
			iCargoSpaceAvailable, this, &pRemainderGroup);
	FAssertMsg(getGroupID() == pSplitGroup->getID(), "splitGroup failed to put head unit in the new group");
	if (pSplitGroup == NULL)
	{
		FAssertMsg(pSplitGroup != NULL, "splitGroup failed");
		return false;
	}
	//CvPlot* pOldPlot = pSplitGroup->plot();
	pSplitGroup->pushMission(MISSION_MOVE_TO_UNIT,
			pBestUnit->getOwner(), pBestUnit->getID(),
			eFlags, false, false, eMissionAI, NULL, pBestUnit);
	/* bool bMoved = (pSplitGroup->plot() != pOldPlot);
	if (!bMoved && pOtherGroup != NULL)
		joinGroup(pOtherGroup);
	return bMoved;
	*/ // K-Mod. (obsolete)

	// K-Mod - just for efficiency, I'll take care of the force separate stuff here.
	if (pRemainderGroup != NULL)
	{
		CvSelectionGroupAI& kRemainderGroup = pRemainderGroup->AI(); // advc.003u
		if (kRemainderGroup.AI_isForceSeparate())
			kRemainderGroup.AI_separate();
	} // K-Mod end
	return true;
}


bool CvUnitAI::AI_guardCityBestDefender()
{
	CvCity* pCity = getPlot().getPlotCity();
	if (pCity != NULL && pCity->getOwner() == getOwner())
	{
		if (getPlot().getBestDefender(getOwner()) == this)
		{
			getGroup()->pushMission(isFortifyable() ? MISSION_FORTIFY : MISSION_SKIP,
					-1, -1, NO_MOVEMENT_FLAGS, false, false, MISSIONAI_GUARD_CITY, NULL);
			return true;
		}
	}
	return false;
}

// K-Mod:
bool CvUnitAI::AI_guardCityOnlyDefender()
{
	FAssert(getGroup()->getNumUnits() == 1);

	CvCity* pPlotCity = getPlot().getPlotCity();
	if (pPlotCity && pPlotCity->getOwner() == getOwner())
	{
		if (getPlot().plotCount(PUF_isMissionAIType, MISSIONAI_GUARD_CITY, -1, getOwner()) <=
			(AI_getGroup()->AI_getMissionAIType() == MISSIONAI_GUARD_CITY ? 1 : 0))
		{
			getGroup()->pushMission(isFortifyable() ? MISSION_FORTIFY : MISSION_SKIP,
					-1, -1, NO_MOVEMENT_FLAGS, false, false,
					noDefensiveBonus() ? NO_MISSIONAI : MISSIONAI_GUARD_CITY, 0);
			return true;
		}
	}
	return false;
}


bool CvUnitAI::AI_guardCityMinDefender(bool bSearch)
{
	PROFILE_FUNC();

	CvCityAI const* pPlotCity = getPlot().AI_getPlotCity();
	if (pPlotCity != NULL && pPlotCity->getOwner() == getOwner())
	{
		/*int iCityDefenderCount = pPlotCity->getPlot().plotCount(PUF_isUnitAIType, UNITAI_CITY_DEFENSE, -1, getOwner());
		if ((iCityDefenderCount - 1) < pPlotCity->AI_minDefenders()) {
			if ((iCityDefenderCount <= 2) || (SyncRandSuccessRatio(4, 5))) {
				getGroup()->pushMission(MISSION_SKIP, -1, -1, 0, false, false, MISSIONAI_GUARD_CITY, NULL);
				return true;
			}
		}*/ // BtS
		// K-Mod
		// Note. For this check, we only count UNITAI_CITY_DEFENSE. But in the bSearch case, we count all guard_city units.
		int iDefendersHave = getPlot().plotCount(PUF_isMissionAIType, MISSIONAI_GUARD_CITY,
				-1, getOwner(), NO_TEAM, AI_getUnitAIType() == UNITAI_CITY_DEFENSE ?
				PUF_isUnitAIType : 0, UNITAI_CITY_DEFENSE);

		if (AI_getGroup()->AI_getMissionAIType() == MISSIONAI_GUARD_CITY)
			iDefendersHave--;

		if (iDefendersHave < pPlotCity->AI_minDefenders())
		{
			if (iDefendersHave <= 1 ||
				SyncRandNum(getArea().getNumAIUnits(getOwner(), UNITAI_CITY_DEFENSE) + 5) > 1)
			{
				getGroup()->pushMission(isFortifyable() ? MISSION_FORTIFY : MISSION_SKIP,
						-1, -1, NO_MOVEMENT_FLAGS, false, false, MISSIONAI_GUARD_CITY, NULL);
				return true;
			}
		}
		// K-Mod end
	}

	if (bSearch)
	{
		int iBestValue = 0;
		CvPlot* pBestPlot = NULL;
		CvPlot* pBestGuardPlot = NULL;
		FOR_EACH_CITYAI(pLoopCity, GET_PLAYER(getOwner()))
		{
			//if (!AI_plotValid(pLoopCity->plot()))
			if (!AI_canEnterByLand(pLoopCity->getArea())) // advc.opt (see comment in guardCity)
				continue;

			//int iDefendersHave = pLoopCity->getPlot().plotCount(PUF_isUnitAIType, UNITAI_CITY_DEFENSE, -1, getOwner());
			// K-Mod
			int iDefendersHave = pLoopCity->getPlot().plotCount(
					PUF_isMissionAIType, MISSIONAI_GUARD_CITY, -1, getOwner());
			if (pPlotCity == pLoopCity &&
				AI_getGroup()->AI_getMissionAIType() == MISSIONAI_GUARD_CITY)
			{
				iDefendersHave--;
			}
			// K-Mod end
			int iDefendersNeed = pLoopCity->AI_minDefenders();

			if (iDefendersHave < iDefendersNeed)
			{
				//if (!pLoopCity->getPlot().isVisibleEnemyUnit(this)) // advc.opt: It's our city
				if (!pLoopCity->AI_isEvacuating()) // advc.139
				{
					iDefendersHave += GET_PLAYER(getOwner()).AI_plotTargetMissionAIs(
							pLoopCity->getPlot(), MISSIONAI_GUARD_CITY, getGroup());
					if (iDefendersHave < iDefendersNeed + 1)
					{
						int iPathTurns;
						//if (!atPlot(pLoopCity->plot()) && generatePath(pLoopCity->plot(), 0, true, &iPathTurns))
						// <K-Mod> (also deleted "if (iPathTurns < 10)")
						if (generatePath(pLoopCity->getPlot(),
							NO_MOVEMENT_FLAGS, true, &iPathTurns, 10)) // </K-Mod>
						{
							/*int iValue = (iDefendersNeed - iDefendersHave) * 20;
							iValue += 2 * std::min(15, iCurrentTurn - pLoopCity->getGameTurnAcquired());
							if (pLoopCity->isOccupation())
							iValue += 5;
							iValue -= iPathTurns;*/ // BtS
							// K-Mod
							int iValue = (iDefendersNeed - iDefendersHave) * 10;
							iValue += iDefendersHave <= 0 ? 10 : 0;

							iValue += 2 * pLoopCity->getCultureLevel();
							iValue += pLoopCity->getPopulation() / 3;
							iValue += pLoopCity->isOccupation() ? 8 : 0;
							iValue -= iPathTurns;
							// K-Mod end

							if (iValue > iBestValue)
							{
								iBestValue = iValue;
								pBestPlot = &getPathEndTurnPlot();
								pBestGuardPlot = pLoopCity->plot();
							}
						}
					}
				}
			}
		}
		if (pBestPlot != NULL)
		{
			if (at(*pBestGuardPlot))
			{
				FAssert(pBestGuardPlot == pBestPlot);
				getGroup()->pushMission(isFortifyable() ? MISSION_FORTIFY : MISSION_SKIP,
						-1, -1, NO_MOVEMENT_FLAGS, false, false, MISSIONAI_GUARD_CITY, NULL);
				return true;
			}
			pushGroupMoveTo(*pBestPlot, NO_MOVEMENT_FLAGS, false, false,
					MISSIONAI_GUARD_CITY, pBestGuardPlot);
			return true;
		}
	}

	return false;
}

/*	K-Mod. This function was so full of useless cruft
	and duplicated code and double-counting mistakes...
	I've deleted the bulk of the old code, and rewritten it
	to be much much simpler - and also better. */
bool CvUnitAI::AI_guardCity(bool bLeave, bool bSearch, int iMaxPath, MovementFlags eFlags,
	// <advc.300> Go up to this much beyond defensive needs if no city needs defenders
	int iExtraDefenders)
{
	// Only affects the city search
	FAssert(iExtraDefenders >= 0 && bSearch || iExtraDefenders == 0); // </advc.300>

	PROFILE_FUNC();

	FAssert(getDomainType() == DOMAIN_LAND);
	FAssert(canDefend());

	CvPlot const* pEndTurnPlot = NULL;
	CvPlot const* pBestGuardPlot = NULL;

	CvPlot const& kPlot = getPlot();
	CvCityAI const* pCity = kPlot.AI_getPlotCity();
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());
	if (pCity != NULL && pCity->getOwner() == getOwner())
	{
		int iExtra = -1; // additional defenders needed.
		if (!bLeave || pCity->AI_isDanger())
			iExtra = (bSearch ? 0 : kOwner.AI_getPlotDanger(kPlot, 2));

		int const iHave = kPlot.plotCount(PUF_canDefendGroupHead, -1, -1, kOwner.getID(),
				// -1 because this unit is being counted as a defender
				NO_TEAM, AI_isCityAIType() ? PUF_isCityAIType : NULL) - 1;

		/*	<advc.052> Code added to CvCityAI allows a settler at size 2, but the
			AI often doesn't have an escort available that early. Let's say that
			one defender in the first city is OK if we haven't met a human yet. */
		if (iExtra < 0 && iHave > 0 && kOwner.getNumCities() == 1 &&
			TeamIter<HUMAN,OTHER_KNOWN_TO>::count(getTeam()) <= 0)
		{
			if (AI_group(UNITAI_SETTLE, /*iMaxGroup*/ 1, -1, -1, false, false, false,
				/*iMaxPath*/ 0, /*bAllowRegrouping*/ true))
			{
				return true;
			}
		} // </advc.052>

		int iNeed = pCity->AI_neededDefenders() + iExtra;
		if (iHave < iNeed)
		{	// don't bother searching. We're staying here.
			bSearch = false;
			pEndTurnPlot = &kPlot;
			pBestGuardPlot = &kPlot;
		}
	}

	if (bSearch)
	{
		int iBestValue = 0;
		//bool const bMoveAllTerrain = getGroup()->canMoveAllTerrain(); // advc
		FOR_EACH_CITYAI(pLoopCity, kOwner)
		{
			/*if (!AI_plotValid(pLoopCity->plot()))
				continue;*/
			// advc.opt: This function is only called for land units; the BBAI check suffices.
			// BBAI efficiency: check area for land units
			/*if(getDomainType() == DOMAIN_LAND)
			if (!isArea(pLoopCity->getArea()) && !bMoveAllTerrain)*/
			// advc.030: Replacing the BBAI check
			if (!AI_canEnterByLand(pLoopCity->getArea()))
				continue;

			//if (!pLoopCity->AI_isDefended((!AI_isCityAIType() ? pLoopCity->getPlot().plotCount(PUF_canDefendGroupHead, -1, -1, getOwner(), NO_TEAM, PUF_isNotCityAIType) : 0)))
			// K-Mod
			int iDefendersNeeded = pLoopCity->AI_neededDefenders(true);
			int iDefendersHave = pLoopCity->getPlot().plotCount(
					PUF_canDefendGroupHead, -1, -1, getOwner(),
					NO_TEAM, AI_isCityAIType() ? PUF_isCityAIType : NULL);
			if (pCity == pLoopCity)
				iDefendersHave -= getGroup()->getNumUnits();
			// K-Mod end
			/*  <advc.139> Reinforce city despite evac if group large enough.
				Don't want cities to be abandoned unnecessarily just b/c few units
				were garrisoned when the enemy stack arrived, but don't want them
				to move in and out either.
				CvCityAI::AI_updateSafety already checks for potential defenders
				within 3 tiles of the city. If this stack is farther away than that,
				it'll probably not arrive in time to save the city, but it might,
				or could quickly retake the city. */
			int const iDefendersWant = iDefendersNeeded - iDefendersHave
					+ iExtraDefenders; // advc.300
			bool const bMoreNeeded = (iDefendersNeeded > iDefendersHave); // advc.300
			if (iDefendersWant <= 0) // No functional change from BtS
				continue;
			if (pLoopCity->AI_isEvacuating() &&
				iDefendersWant > fixp(0.75) * getGroup()->getNumUnits())
			{
				continue;
			} // </advc.139>
			/*if (pLoopCity->getPlot().isVisibleEnemyUnit(this)) // advc.opt: It's our city
				continue;*/

			if (GC.getGame().getGameTurn() - pLoopCity->getGameTurnAcquired() >= 10 &&
				kOwner.AI_plotTargetMissionAIs(pLoopCity->getPlot(),
				MISSIONAI_GUARD_CITY, getGroup(), /*<advc.opt>*/ 0, 2 /*</advc.opt>*/) >= 2)
			{
				continue;
			}
			int iPathTurns;
			/*	advc.300 (note): Ideally we'd check bMoreNeeded here in case that
				another city truly needs more, but this gets too fiddly to implement. */
			if (at(pLoopCity->getPlot()) || !generatePath(pLoopCity->getPlot(),
				eFlags, true, &iPathTurns, iMaxPath))
			{
				continue;
			}
			if (iPathTurns > iMaxPath)
				continue;

			int iValue = //1000 *
					(bMoreNeeded ? 1000 : 500) * // advc.300
					(1 + iDefendersWant);
			iValue /= 1 + iPathTurns + iDefendersHave;
			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				pEndTurnPlot = &getPathEndTurnPlot();
				pBestGuardPlot = pLoopCity->plot();
				FAssert(!atPlot(pEndTurnPlot));
				if (iMaxPath == 1 || iBestValue >= 500)
					break; // we found a good city. No need to waste any more time looking.
			}
		}
	}

	if (pEndTurnPlot == NULL || pBestGuardPlot == NULL)
		return false;

	CvSelectionGroup* pOldGroup = getGroup();
	CvUnit* pEjectedUnit = AI_getGroup()->AI_ejectBestDefender(plot());
	if (pEjectedUnit == NULL)
	{
		FErrorMsg("AI_ejectBestDefender failed to choose a candidate for AI_guardCity.");
		pEjectedUnit = this;
		if (getGroup()->getNumUnits() > 0)
			joinGroup(NULL);
	}
	FAssert(pEjectedUnit != NULL);
	// If the unit is not suited for defense, do not use MISSIONAI_GUARD_CITY.
	MissionAITypes eMissionAI = (pEjectedUnit->noDefensiveBonus() ?
			NO_MISSIONAI : MISSIONAI_GUARD_CITY);
	if (at(*pBestGuardPlot))
	{
		pEjectedUnit->getGroup()->pushMission(MISSION_SKIP, -1, -1, NO_MOVEMENT_FLAGS,
				false, false, eMissionAI, 0);
	}
	else
	{
		FAssert(bSearch);
		FAssert(!at(*pEndTurnPlot));
		pEjectedUnit->pushGroupMoveTo(*pEndTurnPlot, eFlags, false, false,
				eMissionAI, pBestGuardPlot);
	}
	return (pEjectedUnit->getGroup() == pOldGroup || pEjectedUnit == this);
}


bool CvUnitAI::AI_guardCityAirlift()
{
	PROFILE_FUNC();

	if (getGroup()->getNumUnits() > 1)
		return false;

	CvCity* pCity = getPlot().getPlotCity();
	if (pCity == NULL)
		return false;

	if (pCity->getMaxAirlift() == 0)
		return false;

	int iBestValue = 0;
	CvPlot* pBestPlot = NULL;
	FOR_EACH_CITYAI(pLoopCity, GET_PLAYER(getOwner()))
	{
		if (pLoopCity == pCity)
			continue;

		if (canAirliftAt(pCity->plot(), pLoopCity->getX(), pLoopCity->getY()))
		{
			if (!pLoopCity->AI_isDefended(AI_isCityAIType() ? 0 :
				pLoopCity->getPlot().plotCount(PUF_canDefendGroupHead, -1, -1,
				getOwner(), NO_TEAM, PUF_isNotCityAIType)))	// XXX check for other team's units?
			{
				int iValue = pLoopCity->getPopulation();
				if (pLoopCity->AI_isDanger())
					iValue *= 2;

				if (iValue > iBestValue)
				{
					iBestValue = iValue;
					pBestPlot = pLoopCity->plot();
					FAssert(pLoopCity != pCity);
				}
			}
		}
	}

	if (pBestPlot != NULL)
	{
		getGroup()->pushMission(MISSION_AIRLIFT, pBestPlot->getX(), pBestPlot->getY());
		return true;
	}

	return false;
}

// K-Mod:
// This function will use our naval unit to block the coast outside our cities.
bool CvUnitAI::AI_guardCoast(bool bPrimaryOnly, MovementFlags eFlags, int iMaxPath)
{
	PROFILE_FUNC();

	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());

	CvPlot const* pBestCityPlot = 0;
	CvPlot const* pEndTurnPlot = 0;
	int iBestValue = 0;
	FOR_EACH_CITYAI(pLoopCity, kOwner)
	{
		if (!pLoopCity->isCoastal() ||
			(bPrimaryOnly && !kOwner.AI_isPrimaryArea(pLoopCity->getArea())))
		{
			continue;
		}
		int iCoastPlots = 0;
		FOR_EACH_ADJ_PLOT(pLoopCity->getPlot())
		{
			if (pAdj->isWater() &&
				pAdj->getArea().getNumTiles() >=
				GC.getDefineINT(CvGlobals::MIN_WATER_SIZE_FOR_OCEAN))
			{
				iCoastPlots++;
			}
		}

		int iBaseValue = (iCoastPlots <= 0 ? 0 :
				// arbitrary units (AI_cityValue is a bit slower)
				1000 * pLoopCity->AI_neededDefenders() / (iCoastPlots + 3));
		iBaseValue /= (kOwner.AI_isLandWar(pLoopCity->getArea()) ? 2 : 1);

		if (iBaseValue <= iBestValue)
			continue;

		iBaseValue *= 4;
		iBaseValue /= 4 + kOwner.AI_plotTargetMissionAIs(
				pLoopCity->getPlot(), MISSIONAI_GUARD_COAST, getGroup(), 1);

		if (iBaseValue <= iBestValue)
			continue;

		FOR_EACH_ADJ_PLOT(pLoopCity->getPlot())
		{
			if (!pAdj->isWater() ||
				pAdj->getArea().getNumTiles() <
				GC.getDefineINT(CvGlobals::MIN_WATER_SIZE_FOR_OCEAN) ||
				pAdj->getTeam() != getTeam())
			{
				continue;
			}
			int iValue = iBaseValue;
			iValue *= 2;
			//iValue /= (pAdj->getBonusType(getTeam()) == NO_BONUS ? 3 : 2);
			// <advc.028b>
			bool bAnyBonus = false;
			std::vector<CvPlot*> apGuardPlots;
			AI_getGuardedPlots(*pAdj, apGuardPlots);
			for (size_t i = 0;
				!bAnyBonus && i < apGuardPlots.size(); i++)
			{
				if (apGuardPlots[i]->getBonusType(getTeam()) != NO_BONUS)
					bAnyBonus = true;
			}
			iValue /= (bAnyBonus ? 2 : 3);
			// </advc.028b>
			iValue *= 3;
			iValue /= std::max(3, (at(*pAdj) ? 1 - getGroup()->getNumUnits() : 1) +
					pAdj->plotCount(PUF_isMissionAIType,
					MISSIONAI_GUARD_COAST, -1, getOwner()));

			int iPathTurns;
			if (iValue > iBestValue &&
				generatePath(*pAdj, eFlags, true, &iPathTurns, iMaxPath))
			{
				iValue *= 4;
				iValue /= 3 + iPathTurns;
				// <advc.028b> Break ties in favor of sea patrolling
				if (bAnyBonus && pAdj->getBonusType(getTeam()) == NO_BONUS)
					iValue++; // </advc.028b>
				if (iValue > iBestValue)
				{
					iBestValue = iValue;
					pBestCityPlot = pLoopCity->plot();
					pEndTurnPlot = &getPathEndTurnPlot();
				}
			}
		}
	}

	if (pEndTurnPlot != NULL)
	{
		if (at(*pEndTurnPlot))
		{
			getGroup()->pushMission(
					canSeaPatrol(pEndTurnPlot) ? MISSION_SEAPATROL : MISSION_SKIP,
					-1, -1, NO_MOVEMENT_FLAGS, false, false, MISSIONAI_GUARD_COAST,
					pBestCityPlot);
		}
		else
		{
			pushGroupMoveTo(*pEndTurnPlot, eFlags, false, false,
					MISSIONAI_GUARD_COAST, pBestCityPlot);
		}
		return true;
	}

	return false;
}


bool CvUnitAI::AI_guardBonus(int iMinValue)
{
	PROFILE_FUNC();
	// <advc.107> No defenders to spare for bonuses
	if(GET_PLAYER(getOwner()).AI_isDoStrategy(AI_STRATEGY_TURTLE) ||
		(getArea().getAreaAIType(getTeam()) == AREAAI_DEFENSIVE &&
		GET_TEAM(getTeam()).AI_getWarSuccessRating() < -80))
	{
		return false;
	} // </advc.107>
	CvPlot const* pBestPlot = NULL;
	CvPlot const* pBestGuardPlot = NULL;
	int iBestValue = 0;
	for (int iI = 0; iI < GC.getMap().numPlots(); iI++)
	{
		CvPlot const& kPlot = GC.getMap().getPlotByIndex(iI);
		// <advc.opt> Moved up
		if (kPlot.getOwner() != getOwner() ||
			!isValidDomain(kPlot.isWater()) || // K-Mod. (boats shouldn't defend forts!)
			/* </advc.opt> */ !AI_plotValid(kPlot))
		{
			continue;
		}
		// <advc.028b>
		int iValue = 0;
		std::vector<CvPlot*> apGuardPlots;
		AI_getGuardedPlots(kPlot, apGuardPlots);
		for (size_t i = 0; i < apGuardPlots.size(); i++)
		{
			BonusTypes eBonus = apGuardPlots[i]->getNonObsoleteBonusType(getTeam(), true);
			if (eBonus == NO_BONUS ||
				(apGuardPlots[i]->isWater() &&
				apGuardPlots[i]->defenseModifier(getTeam(), true) <= 0))
			{
				continue;
			}
			int iTmpVal = // </advc.028b>
					GET_PLAYER(getOwner()).AI_bonusVal(eBonus, /* K-Mod: */ 0);
			iTmpVal += std::max(0, 200 * GC.getInfo(eBonus).getAIObjective());
			if (apGuardPlots[i]->getPlotGroupConnectedBonus(getOwner(), eBonus) == 1)
				iTmpVal *= 2;
			iValue += iTmpVal; // advc.028b
		}
		if (iValue > iMinValue && !kPlot.isVisibleEnemyUnit(this))
		{
			int const iPlotTargetMissionAIs = GET_PLAYER(getOwner()).
					AI_plotTargetMissionAIs(kPlot, MISSIONAI_GUARD_BONUS, getGroup());
			// K-Mod
			iValue *= 2;
			iValue /= 2 + iPlotTargetMissionAIs;
			if (iValue > iMinValue) // K-Mod end
			{
				int iPathTurns;
				if (generatePath(kPlot, NO_MOVEMENT_FLAGS, true, &iPathTurns))
				{
					iValue *= 1000;
					iValue /= iPathTurns + 4; // K-Mod: was +1
					if (iValue > iBestValue)
					{
						iBestValue = iValue;
						pBestPlot = &getPathEndTurnPlot();
						pBestGuardPlot = &kPlot;
					}
				}
			}
		}
	}
	if (pBestPlot != NULL && pBestGuardPlot != NULL)
	{
		if (at(*pBestGuardPlot))
		{
			getGroup()->pushMission(
					// <K-Mod>
					canSeaPatrol(pBestGuardPlot) ? MISSION_SEAPATROL :
					(isFortifyable() ? MISSION_FORTIFY : MISSION_SKIP), // </K-Mod>
					-1, -1, NO_MOVEMENT_FLAGS, false, false, MISSIONAI_GUARD_BONUS,
					pBestGuardPlot);
			return true;
		}
		else
		{
			pushGroupMoveTo(*pBestPlot, NO_MOVEMENT_FLAGS, false, false,
					MISSIONAI_GUARD_BONUS, pBestGuardPlot);
			return true;
		}
	}

	return false;
}

// advc.028b:
void CvUnitAI::AI_getGuardedPlots(CvPlot const& kFrom,
	std::vector<CvPlot*>& kResult) const
{
	for (SquareIter itGuardPlot(kFrom,
		canSeaPatrol(&kFrom) ? GC.getMAX_SEA_PATROL_RANGE() : 0);
		itGuardPlot.hasNext(); ++itGuardPlot)
	{
		if (&*itGuardPlot == &kFrom || canReachBySeaPatrol(*itGuardPlot, &kFrom))
			kResult.push_back(&*itGuardPlot);
	}
}

// advc.300: Structure adopted from AI_guardBonus
bool CvUnitAI::AI_guardYield()
{
	// <advc.107>
	if(GET_PLAYER(getOwner()).AI_isDoStrategy(AI_STRATEGY_TURTLE))
		return false; // </advc.107>
	CvCity const* pCity = getPlot().getPlotCity();
	// For now, only consider nearby city if already guarding bonus.
	MissionTypes eStayPut = isFortifyable() ? MISSION_FORTIFY : MISSION_SKIP;
	if(pCity == NULL && AI_getGroup()->AI_getMissionAIType() == MISSIONAI_GUARD_BONUS)
		pCity = getPlot().getWorkingCity();
	if(pCity == NULL || pCity->getOwner() != getOwner())
		return false;
	int iBestValue = 6;
	if(!GC.getGame().isOption(GAMEOPTION_RAGING_BARBARIANS))
		iBestValue = 8;
	CvPlot* pBestPlot = NULL;
	for (CityPlotIter it(getPlot()); it.hasNext(); ++it)
	{
		CvPlot& kLoopPlot = *it;
		if(kLoopPlot.getOwner() != getOwner() ||
			!kLoopPlot.isImproved() || kLoopPlot.isWater() ||
			kLoopPlot.getPlotCity() != NULL || kLoopPlot.isUnit())
		{
			continue;
		}
		int iPathTurns;
		/*  Must be reachable in one hop, so that we can hurry back to the city
			when it's in danger. */
		if(!generatePath(kLoopPlot, NO_MOVEMENT_FLAGS, true, &iPathTurns) ||
			iPathTurns > 1)
		{
			continue;
		}
		int iValue = 0;
		// Example: Plains Hill Mine in the outer ring gets a value of 8
		FOR_EACH_ENUM(Yield)
		{
			int iYieldValue = kLoopPlot.getYield(eLoopYield);
			if(eLoopYield != YIELD_COMMERCE)
				iYieldValue *= 2;
			iValue += iYieldValue;
		}
		/*  BARBARIAN_TEAM: It's more about the defense that Barbarians will have if
			allowed to enter the tile than our unit's defense. */
		/*  Example cont.: +2 from the Hill (25/10 rounded down);
			i.e. it's worth protecting (barely). */
		iValue += kLoopPlot.defenseModifier(BARBARIAN_TEAM, true,
				/* <advc.012> */ getTeam() /* </advc.012> */) / 10;
		if(iValue <= iBestValue) // Will only decrease from here
			continue;
		// Guard only tiles near invisible regions (where Barbarians might appear)
		CvPlot const* pNearestInvis = kLoopPlot.nearestInvisiblePlot(true, 5, getTeam());
		if(pNearestInvis == NULL)
			continue;
		iValue -= ::plotDistance(pNearestInvis, &kLoopPlot);
		if(iValue > iBestValue)
		{
			iBestValue = iValue;
			pBestPlot = &kLoopPlot;
		}
	}
	if(pBestPlot == NULL)
		return false;
	if(at(*pBestPlot))
	{
		 getGroup()->pushMission(eStayPut, -1, -1, NO_MOVEMENT_FLAGS,
				false, false, MISSIONAI_GUARD_BONUS, pBestPlot);
	}
	else
	{
		pushGroupMoveTo(*pBestPlot, NO_MOVEMENT_FLAGS, false, false,
				MISSIONAI_GUARD_BONUS, pBestPlot);
	}
	return true;
}

// advc.306:
bool CvUnitAI::AI_barbAmphibiousCapture()
{
	bool bTargetWithinOwnBorders = true;
	CvPlot* pDest = NULL;
	MissionAITypes eMissionAI = MISSIONAI_PILLAGE;
	FOR_EACH_ADJ_PLOT_VAR(getPlot())
	{
		// <advc.306>
		if(pAdj->isOwned() &&
			pAdj->getArea().isBorderObstacle(pAdj->getTeam()))
		{
			continue;
		} // </advc.306>
		/*  Undefended city (perhaps unnecessary; not sure if the assault routine
			gets this right, or if it would drop units next to the city) */
		CvCity const* pCity = pAdj->getPlotCity();
		if (pCity != NULL && pCity->getTeam() != getTeam() &&
			!pAdj->isVisibleEnemyDefender(this))
		{
			pDest = pAdj;
			// Sudden attacks on undefended cities are OK (see below)
			bTargetWithinOwnBorders = false; // Not a good variable name
			eMissionAI = MISSIONAI_ASSAULT;
			break;
		}
		if(!pAdj->isUnit() || pAdj->isWater())
			continue;
		/*  Don't attack stacks of AI civilians. Can't be so lenient with humans;
			could be exploited by having threatened Workers huddle together. */
		if(pAdj->getNumUnits() > 2 && pAdj->isOwned() &&
			!GET_PLAYER(pAdj->getOwner()).isHuman())
		{
			continue;
		}
		CvUnit const* pHead = pAdj->headUnit();
		if(pHead->getTeam() != getTeam() && !pHead->canFight())
		{
			bool bPlotWithinOwnBorders = (pAdj->getOwner() == pHead->getOwner());
			// Prefer target outside its borders (see below)
			if(pDest == NULL || (bTargetWithinOwnBorders && !bPlotWithinOwnBorders))
			{
				pDest = pAdj;
				bTargetWithinOwnBorders = bPlotWithinOwnBorders;
				if(!bTargetWithinOwnBorders)
					break;
			}
		}
	}
	if(pDest == NULL)
		return false;
	/*  When borders don't reach out onto sea, it's possible that Barbarians enter
		visibility with enough moves left to kill a Worker.
		Don't want such attacks "out of the blue".
		Exception: Undefended non-combatants outside their owner's borders
		are always fair game. */
	if(bTargetWithinOwnBorders && getPlot().getOwner() != getOwner() &&
		getPlot().getOwner() != pDest->getOwner())
	{
		return false;
	}
	return (AI_transportGoTo(getPlot(), *pDest, NO_MOVEMENT_FLAGS, eMissionAI));
}


int CvUnitAI::AI_getPlotDefendersNeeded(CvPlot const& kPlot, int iExtra)
{
	int iNeeded = iExtra;
	BonusTypes eNonObsoleteBonus = kPlot.getNonObsoleteBonusType(getTeam());
	if (eNonObsoleteBonus != NO_BONUS)
		iNeeded += (GET_PLAYER(getOwner()).AI_bonusVal(eNonObsoleteBonus, 1) + 10) / 19;

	int iDefense = kPlot.defenseModifier(getTeam(), true);
	iNeeded += (iDefense + 25) / 50;
	if (iNeeded == 0)
		return 0;

	iNeeded += GET_PLAYER(getOwner()).AI_getPlotAirbaseValue(kPlot) / 50;

	int iNumHostiles = 0;
	int iNumPlots = 0;

	for (SquareIter it(kPlot, 2); it.hasNext(); ++it)
	{
		CvPlot const& kLoopPlot = *it;
		iNumHostiles += kLoopPlot.getNumVisibleEnemyDefenders(this);
		if (kLoopPlot.getTeam() != getTeam() || kLoopPlot.isCoastalLand())
		{
			iNumPlots++;
			if (isEnemy(kLoopPlot))
				iNumPlots += 4;
		}
	}

	if (iNumHostiles == 0 && iNumPlots < 4)
	{
		if (iNeeded > 1)
			iNeeded = 1;
		else iNeeded = 0;
	}

	return iNeeded;
}

bool CvUnitAI::AI_guardFort(bool bSearch)
{
	PROFILE_FUNC();
	// <advc.107> Don't guard forts when cities are falling
	if(GET_PLAYER(getOwner()).AI_isDoStrategy(AI_STRATEGY_TURTLE))
		return false; // </advc.107>
	if (getPlot().getOwner() == getOwner() &&
		// advc: Replacing custom acts-as-city check
		!getPlot().isCity() && GET_TEAM(getTeam()).isCityDefense(getPlot()))
	{
		if (getPlot().plotCount(PUF_isCityAIType, -1, -1, getOwner()) <=
			AI_getPlotDefendersNeeded(getPlot()))
		{
			getGroup()->pushMission(isFortifyable() ? MISSION_FORTIFY : MISSION_SKIP,
				-1, -1, NO_MOVEMENT_FLAGS, false, false, MISSIONAI_GUARD_BONUS, plot());
			{
				return true;
			}
		}
	}

	if (!bSearch)
		return false;

	CvPlot const* pBestPlot = NULL;
	CvPlot const* pBestGuardPlot = NULL;
	int iBestValue = 0;
	for (int i = 0; i < GC.getMap().numPlots(); i++)
	{
		CvPlot const& kPlot = GC.getMap().getPlotByIndex(i);
		if (kPlot.getOwner() != getOwner() || kPlot.isCity() || at(kPlot) ||
			//!AI_plotValid(kPlot)
			// advc.opt: Check only area
			!AI_canEnterByLand(kPlot.getArea()) ||
			// advc: Replacing custom acts-as-city check
			!GET_TEAM(getTeam()).isCityDefense(kPlot))
		{
			continue;
		}
		int iNeeded = AI_getPlotDefendersNeeded(kPlot);
		if (iNeeded <= 0 || kPlot.isVisibleEnemyUnit(this))
			continue;
		if (GET_PLAYER(getOwner()).AI_plotTargetMissionAIs(kPlot, MISSIONAI_GUARD_BONUS,
			getGroup(), /*<advc.opt>*/0, iNeeded/*</advc.opt>*/) < iNeeded)
		{
			int iPathTurns;
			if (generatePath(kPlot, NO_MOVEMENT_FLAGS, true, &iPathTurns))
			{
				int iValue = iNeeded;
				iValue *= 1000;
				iValue /= (iPathTurns + 2);
				if (iValue > iBestValue)
				{
					iBestValue = iValue;
					pBestPlot = &getPathEndTurnPlot();
					pBestGuardPlot = &kPlot;
				}
			}
		}
	}
	if (pBestPlot != NULL && pBestGuardPlot != NULL)
	{
		if (at(*pBestGuardPlot))
		{
			FErrorMsg("Current guard plot doesn't need defenders"); // advc
			getGroup()->pushMission(
					isFortifyable() ? MISSION_FORTIFY : MISSION_SKIP,
					-1, -1, NO_MOVEMENT_FLAGS, false, false,
					MISSIONAI_GUARD_BONUS, pBestGuardPlot);
			return true;
		}
		else
		{
			pushGroupMoveTo(*pBestPlot, NO_MOVEMENT_FLAGS, false, false,
					MISSIONAI_GUARD_BONUS, pBestGuardPlot);
			return true;
		}
	}

	return false;
}


bool CvUnitAI::AI_guardCitySite()
{
	PROFILE_FUNC();

	int iPathTurns;
	CvPlot* pBestPlot = NULL;
	CvPlot* pBestGuardPlot = NULL;
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner()); // advc
	/*	advc.300: Don't guard any ole tile with a positive found value;
		only actual city sites. */
	int iBestValue = kOwner.AI_getMinFoundValue() - 1;
	for (int i = 0; i < kOwner.AI_getNumCitySites(); i++)
	{
		CvPlot& kLoopPlot = kOwner.AI_getCitySite(i);
		//if (owner.AI_plotTargetMissionAIs(pLoopPlot, MISSIONAI_GUARD_CITY, getGroup()) == 0)
		// <advc.300> Need to check the adjacent tiles too
		bool bValid = true;
		FOR_EACH_ADJ_PLOT(kLoopPlot)
		{
			if (AI_canEnterByLand(pAdj->getArea()) &&
				kOwner.AI_isAnyPlotTargetMissionAI(*pAdj, MISSIONAI_GUARD_CITY, getGroup()))
			{
				bValid = false;
				break;
			}
		}
		if (bValid) // </advc.300>
		{
			// K-Mod. I've switched the order of the following two if statements, for efficiency.
			int iValue = kLoopPlot.getFoundValue(kOwner.getID());
			if (iValue > iBestValue)
			{
				if (generatePath(kLoopPlot, NO_MOVEMENT_FLAGS, true, &iPathTurns))
				{
					iBestValue = iValue;
					pBestPlot = &getPathEndTurnPlot();
					pBestGuardPlot = &kLoopPlot;
				}
			}
		}
	}
	// <advc.300> Guard an adjacent plot if it's better for fogbusting
	if(pBestGuardPlot != NULL)
	{
		int iBestGuardVal = 0;
		CvPlot* pBetterGuardPlot = pBestGuardPlot;
		FOR_EACH_ADJ_PLOT_VAR(*pBestGuardPlot)
		{
			if(!pAdj->isRevealed(getTeam()))
				continue;
			int iGuardValue = pAdj->defenseModifier(getTeam(), true);
			if (noDefensiveBonus())
			{	// Still useful to deny approaching enemies a defensive bonus
				iGuardValue *= 3;
				iGuardValue /= 5;
			}
			iGuardValue += pAdj->seeFromLevel(getTeam()) * 30;
			if(at(*pAdj))
				iGuardValue += 3; // inertia
			if(pAdj == pBestGuardPlot)
				iGuardValue += 1; // tie-breaker
			if(iGuardValue > iBestGuardVal && (at(*pAdj) || canMoveInto(*pAdj)))
			{
				iBestGuardVal = iGuardValue;
				pBetterGuardPlot = pAdj;
			}
		}
		if(pBetterGuardPlot != pBestGuardPlot &&
			generatePath(*pBetterGuardPlot, NO_MOVEMENT_FLAGS, true, &iPathTurns))
		{
			pBestPlot = &getPathEndTurnPlot();
			pBestGuardPlot = pBetterGuardPlot;
		}
	} // </advc.300>
	if (pBestPlot != NULL && pBestGuardPlot != NULL)
	{

		if (at(*pBestGuardPlot))
		{
			getGroup()->pushMission(
					isFortifyable() ? MISSION_FORTIFY : MISSION_SKIP,
					-1, -1, NO_MOVEMENT_FLAGS, false, false,
					MISSIONAI_GUARD_CITY, pBestGuardPlot);
			return true;
		}
		else
		{
			pushGroupMoveTo(*pBestPlot, NO_MOVEMENT_FLAGS, false, false,
					MISSIONAI_GUARD_CITY, pBestGuardPlot);
			return true;
		}
	}

	return false;
}


bool CvUnitAI::AI_guardSpy(int iRandomPercent)
{
	PROFILE_FUNC();

	int iBestValue = 0;
	CvPlot* pBestPlot = NULL;
	CvPlot* pBestGuardPlot = NULL;
	FOR_EACH_CITY(pLoopCity, GET_PLAYER(getOwner()))
	{
		//if (!AI_plotValid(pLoopCity->plot()))
		if (!AI_canEnterByLand(pLoopCity->getArea())) // advc.opt (see comment in AI_guardCity)
			continue;
		// if (!pLoopCity->getPlot().isVisibleEnemyUnit(this)) { // disabled by K-Mod. This isn't required for spies...

		// BETTER_BTS_AI_MOD, Unit AI, Efficiency, 08/19/09, jdog5000: START
		// BBAI efficiency: check area for land units
		if (getDomainType() == DOMAIN_LAND && !pLoopCity->isArea(getArea()) &&
			!getGroup()->canMoveAllTerrain())
		{
			continue;
		}
		int iValue = 0;
		if (GET_PLAYER(getOwner()).AI_atVictoryStage(AI_VICTORY_SPACE4))
		{
			if (pLoopCity->isCapital())
				iValue += 30;
			else if (pLoopCity->isProductionProject())
				iValue += 5;
		}
		if (GET_PLAYER(getOwner()).AI_atVictoryStage(AI_VICTORY_CULTURE3))
		{
			if (pLoopCity->getCultureLevel() >= GC.getNumCultureLevelInfos() - 2)
				iValue += 10;
		}
		if (pLoopCity->isProductionUnit())
		{
			if (GC.getInfo(pLoopCity->getProductionUnit()).isLimited())
				iValue += 4;
		}
		else if (pLoopCity->isProductionBuilding())
		{
			if (GC.getInfo(pLoopCity->getProductionBuilding()).isLimited())
				iValue += 5;
		}
		else if (pLoopCity->isProductionProject())
		{
			if (GC.getInfo(pLoopCity->getProductionProject()).isLimited())
				iValue += 6;
		}
		// BETTER_BTS_AI_MOD: END
		if (iValue <= 0)
			continue;

		if (!GET_PLAYER(getOwner()).AI_isAnyPlotTargetMissionAI(
			pLoopCity->getPlot(), MISSIONAI_GUARD_SPY, getGroup()))
		{
			int iPathTurns;
			if (generatePath(pLoopCity->getPlot(), NO_MOVEMENT_FLAGS, true, &iPathTurns))
			{
				iValue *= 100 + SyncRandNum(iRandomPercent);
				//iValue /= 100;
				iValue /= iPathTurns + 1;
				if (iValue > iBestValue)
				{
					iBestValue = iValue;
					pBestPlot = &getPathEndTurnPlot();
					pBestGuardPlot = pLoopCity->plot();
				}
			}
		}
	}

	if (pBestPlot != NULL && pBestGuardPlot != NULL)
	{
		if (at(*pBestGuardPlot))
		{
			getGroup()->pushMission(MISSION_SKIP,
					-1, -1, NO_MOVEMENT_FLAGS, false, false,
					MISSIONAI_GUARD_SPY, pBestGuardPlot);
			return true;
		}
		else
		{
			pushGroupMoveTo(*pBestPlot, NO_MOVEMENT_FLAGS, false, false,
					MISSIONAI_GUARD_SPY, pBestGuardPlot);
			return true;
		}
	}

	return false;
}


/*  BETTER_BTS_AI_MOD, Espionage AI, 10/25/09, jdog5000:
	Never used BTS functions commented out */
/* // advc: Deleted the bodies (didn't check if there's sth. to scavenge)
bool CvUnitAI::AI_destroySpy()
{
 ...
}
bool CvUnitAI::AI_sabotageSpy()
{
 ...
}
bool CvUnitAI::AI_pickupTargetSpy()
{
 ...
}*/


bool CvUnitAI::AI_chokeDefend()
{
	FAssert(AI_isCityAIType());
	// XXX what about amphib invasions?

	CvCityAI const* pCity = getPlot().AI_getPlotCity();
	if (pCity != NULL && pCity->getOwner() == getOwner() &&
		pCity->AI_neededDefenders() > 1 &&
		pCity->AI_isDefended(pCity->getPlot().plotCount(
		PUF_canDefendGroupHead, -1, -1, getOwner(), NO_TEAM, PUF_isNotCityAIType)))
	{
		int const iDangerThresh = 4;
		int iPlotDanger = GET_PLAYER(getOwner()).AI_getPlotDanger(getPlot(), 3, true,
				iDangerThresh + 1); // advc.opt: Stop counting at thresh
		if (iPlotDanger <= iDangerThresh)
		{
			if (AI_anyAttack(1, 65, NO_MOVEMENT_FLAGS,
				//std::max(0, (iPlotDanger - 1))
				iPlotDanger > 1 ? 2 : 0)) // K-Mod
			{
				return true;
			}
		}
	}
	return false;
}

// advc.299: Cut from AI_heal
bool CvUnitAI::AI_singleUnitHeal(int iMaxTurnsExposed, int iMaxTurnsOutsideCity)
{
	CvSelectionGroup& kGroup = *getGroup();

	if (isAlwaysHeal() || getDamage() <= 0 || kGroup.getNumUnits() != 1)
		return false;
	bool bHeal = false;
	if (GET_TEAM(getTeam()).isCityHeal(getPlot())) // advc.299: was getPlot().isCity()
		bHeal = true;
	else if (!isBarbarian())
	{
		int const iHealTurns = healTurns();
		if (iHealTurns >= 20) // advc: Feature damage
			return false;
		if (iHealTurns <= iMaxTurnsExposed ||
			// <advc.299>
			(iHealTurns <= iMaxTurnsOutsideCity &&
			getPlot().defenseModifier(getTeam(), true) > 0) ||
			// If the group had urgent business, it probably wouldn't be automated.
			isAutomated()) // </advc.299>
		{
			bHeal = true;
		}
	}
	// <advc.306>
	if (!bHeal && isBarbarian())
	{
		int iHeal = healRate();
		if (iHeal >= 5 && SyncRandSuccess(scaled(2 * iHeal,
			getDomainType() == DOMAIN_SEA ? 35 : 45)))
		{
			bHeal = true;
		}
	} // </advc.306>
	if (bHeal)
	{
		kGroup.pushMission(MISSION_HEAL, -1, -1, NO_MOVEMENT_FLAGS,
				false, false, MISSIONAI_HEAL);
		return true;
	}
	return false;
}


bool CvUnitAI::AI_heal(int iDamagePercent, int iMaxPath)
{
	PROFILE_FUNC();

	CvSelectionGroup& kGroup = *getGroup();

	if (kGroup.getNumUnits() == 1)
	{
		// advc.299: Moved into new function
		return AI_singleUnitHeal();
	}

	FeatureTypes const eFeature = getPlot().getFeatureType();
	if (eFeature != NO_FEATURE && GC.getInfo(eFeature).getTurnDamage() > 0)
	{
		//Pass through (actively seeking a safe spot may result in unit getting stuck)
		return false;
	}

	if (iDamagePercent == 0)
		iDamagePercent = 10;
	iMaxPath = std::min(iMaxPath, 2); // advc (note): MNAI increases this to ...,4)

	int iTotalDamage = 0;
	int iTotalHitpoints = 0;
	int iHurtUnitCount = 0;
	std::vector<CvUnit*> apDamagedUnits;
	FOR_EACH_UNIT_VAR_IN(pLoopUnit, *getGroup())
	{
		int iDamageThreshold = (pLoopUnit->maxHitPoints() * iDamagePercent) / 100;
		if (NO_UNIT != getLeaderUnitType())
			iDamageThreshold /= 2;

		if (pLoopUnit->getDamage() > 0)
			iHurtUnitCount++;

		iTotalDamage += pLoopUnit->getDamage();
		iTotalHitpoints += pLoopUnit->maxHitPoints();
		if (pLoopUnit->getDamage() > iDamageThreshold && !pLoopUnit->hasMoved() &&
			!pLoopUnit->isAlwaysHeal() &&
			pLoopUnit->healTurns(pLoopUnit->plot()) <= iMaxPath)
		{
			apDamagedUnits.push_back(pLoopUnit);
		}
	}
	if (iHurtUnitCount == 0)
		return false;

	bool bPushedMission = false;
	if (getPlot().getOwner() == getOwner() && //getPlot().isCity()
		GET_TEAM(getTeam()).isCityHeal(getPlot())) // advc.299
	{
		FAssert(iHurtUnitCount >= (int)apDamagedUnits.size());
		for (size_t i = 0; i < apDamagedUnits.size(); i++)
		{
			CvUnit* pUnitToHeal = apDamagedUnits[i];
			pUnitToHeal->joinGroup(NULL);
			pUnitToHeal->getGroup()->pushMission(MISSION_HEAL, -1, -1,
					NO_MOVEMENT_FLAGS, false, false, MISSIONAI_HEAL);
			/*	note, removing the head unit from a group will force the group
				to be completely split if non-human */
			if (pUnitToHeal == this)
				bPushedMission = true;
			iHurtUnitCount--;
		}
	}

	if (iHurtUnitCount * 2 > getGroup()->getNumUnits())
	{
		FAssert(getGroup()->getNumUnits() > 0);
		if (AI_moveIntoCity(2))
			return true;
		if (healRate() > 10)
		{
			getGroup()->pushMission(MISSION_HEAL, -1, -1, NO_MOVEMENT_FLAGS,
					false, false, MISSIONAI_HEAL);
			return true;
		}
	}

	return bPushedMission;
}

/*  advc.139: Mostly cut and pasted from AI_assaultSeaMove, AI_pirateSeaMove,
	AI_escortSeaMove, AI_attackSeaMove, AI_reserveSeaMove, AI_exploreSeaMove,
	AI_settlerSeaMove, AI_missionarySeaMove, AI_spySeaMove and
	AI_missileCarrierSeaMove (duplicate code).
	AI_attackAirMove, AI_defenseAirMove and AI_missileAirMove
	still contain similar code. */
ProbabilityTypes CvUnitAI::AI_isThreatenedFromLand() const
{
	PROFILE_FUNC(); // advc: Not called frequently at all (currently)
	FAssert(getDomainType() != DOMAIN_LAND);
	if (getPlot().isWater())
		return NO_PROBABILITY;
	bool const bDamaged = (getDamage() > 0);
	CvCityAI const* pPlotCity = getPlot().AI_getPlotCity();
	if(pPlotCity != NULL)
	{
		if (pPlotCity->AI_isEvacuating())
			return PROBABILITY_HIGH;
		if (pPlotCity->AI_isSafe())
			return NO_PROBABILITY;
		return (bDamaged ? PROBABILITY_LOW : PROBABILITY_REAL);
	}
	// BETTER_BTS_AI_MOD, Naval AI, 06/14/09, Solver & jdog5000: START
	// (with K-Mod adjustments)
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());
	int iOurDefense = kOwner.AI_localDefenceStrength(plot(), getTeam(), DOMAIN_LAND, 0);
	int iEnemyOffense = kOwner.AI_localAttackStrength(plot(), NO_TEAM, DOMAIN_LAND, 2);
	// (was based on AI_getOurPlotStrength in BBAI)
	if (bDamaged) // extra risk to leaving when wounded
		iOurDefense *= 2;
	if (iEnemyOffense * 4 > iOurDefense) // (was 8 vs 1 in BBAI)
	{
		if (iEnemyOffense * 2 > iOurDefense) // (was 4 vs 1 in BBAI)
			return PROBABILITY_REAL;
		return PROBABILITY_LOW;
	}
	return NO_PROBABILITY;
	// BETTER_BTS_AI_MOD: END
}


bool CvUnitAI::AI_afterAttack()
{
	if (!canFight() || !isMadeAttack() || /* advc.164: */ !isMadeAllAttacks())
		return false;

	// K-Mod. Large groups may still have important stuff to do!
	if (getGroup()->getNumUnits() > 2)
		return false;
	// K-Mod end

	if (getDomainType() == DOMAIN_LAND)
	{
		if (AI_guardCity(false, true, 1))
		{
			return true;
		}

		// K-Mod. We might be able to capture an undefended city, or at least a worker. (think paratrooper)
		// (note: it's also possible that we are asking our group partner to attack something.)
		// (also, note that AI_anyAttack will favour undefended cities over workers.)
		if (AI_anyAttack(1, 65))
		{
			return true;
		}
		// K-Mod end
	}

	if (AI_pillageRange(1))
	{
		return true;
	}

	if (AI_retreatToCity(false, false, 1))
	{
		return true;
	}

	if (AI_hide())
	{
		return true;
	}

	if (AI_goody(1))
	{
		return true;
	}

	if (AI_pillageRange(2))
	{
		return true;
	}

	if (AI_defend())
	{
		return true;
	}

	if (AI_safety())
	{
		return true;
	}

	return false;
}


bool CvUnitAI::AI_goldenAge()
{
	if (canGoldenAge(plot()))
	{
		getGroup()->pushMission(MISSION_GOLDEN_AGE);
		return true;
	}

	return false;
}

// This function has been edited for K-Mod
bool CvUnitAI::AI_spreadReligion()
{
	PROFILE_FUNC();

	const CvPlayerAI& kOwner = GET_PLAYER(getOwner()); // K-Mod

	ReligionTypes eReligion = NO_RELIGION;
	if (kOwner.getStateReligion() != NO_RELIGION)
	{
		if (getUnitInfo().getReligionSpreads(kOwner.getStateReligion()) > 0)
			eReligion = kOwner.getStateReligion();
	}

	if (eReligion == NO_RELIGION)
	{
		for (int iI = 0; iI < GC.getNumReligionInfos(); iI++)
		{
			//if (bCultureVictory || GET_TEAM(getTeam()).hasHolyCity((ReligionTypes)iI))
			if (getUnitInfo().getReligionSpreads((ReligionTypes)iI) > 0)
			{
				eReligion = ((ReligionTypes)iI);
				break;
			}
		}
	}

	if (eReligion == NO_RELIGION)
		return false;

	// doc: factored out spread target for other AI evaluations
	std::pair<CvPlot*, CvPlot*> spreadPlots = AI_spreadTarget(eReligion);
	CvPlot* pBestPlot = spreadPlots.first;
	CvPlot* pBestSpreadPlot = spreadPlots.second;

	if (pBestPlot == NULL || pBestSpreadPlot == NULL)
		return false;

	if (at(*pBestSpreadPlot))
		getGroup()->pushMission(MISSION_SPREAD, eReligion);
	else
	{
		pushGroupMoveTo(*pBestPlot, MOVE_NO_ENEMY_TERRITORY, false, false,
			MISSIONAI_SPREAD, pBestSpreadPlot);
	}
	return true;
}

std::pair<CvPlot*, CvPlot*> CvUnitAI::AI_spreadTarget(ReligionTypes eReligion, bool bGreatMission) const
{
    CvPlayer const& kOwner = GET_PLAYER(getOwner());

    bool bCultureVictory = kOwner.AI().AI_atVictoryStage(AI_VICTORY_CULTURE2 | AI_VICTORY_CULTURE3 | AI_VICTORY_CULTURE4);
	bool bHasHolyCity = GET_TEAM(getTeam()).hasHolyCity(eReligion);
	bool bHasAnyHolyCity = bHasHolyCity;
	if (!bHasAnyHolyCity)
	{
		for (int iI = 0; !bHasAnyHolyCity && iI < GC.getNumReligionInfos(); iI++)
			bHasAnyHolyCity = GET_TEAM(getTeam()).hasHolyCity((ReligionTypes)iI);
	}

	int iBestValue = 0;
	CvPlot* pBestPlot = NULL;
	CvPlot* pBestSpreadPlot = NULL;

	// BBAI TODO: Could also use CvPlayerAI::AI_missionaryValue to determine which player to target ...
	for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		const CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iI);
		if (!kLoopPlayer.isAlive())
			continue;

		int iPlayerMultiplierPercent = 0;

		if (kLoopPlayer.getTeam() != getTeam() && canEnterTerritory(kLoopPlayer.getTeam()))
		{
			if ((bHasHolyCity || bGreatMission) // doc
				&& kOwner.AI().AI_isTargetForMissionaries(kLoopPlayer.getID(), eReligion)) // advc.171:
			{
				iPlayerMultiplierPercent = 100;
				if (!bCultureVictory || eReligion == kOwner.getStateReligion())
				{
					if (kLoopPlayer.getStateReligion() == NO_RELIGION)
					{
						if (kLoopPlayer.getNonStateReligionHappiness() == 0)
							iPlayerMultiplierPercent += 600;
					}
					else if (kLoopPlayer.getStateReligion() == eReligion)
						iPlayerMultiplierPercent += 300;
					else
					{
						if (kLoopPlayer.hasHolyCity(kLoopPlayer.getStateReligion()))
							iPlayerMultiplierPercent += 50;
						else
							iPlayerMultiplierPercent += 300;
					}
					// <advc.171>
					if(GET_TEAM(getTeam()).AI_isSneakAttackPreparing(kLoopPlayer.getTeam()))
						iPlayerMultiplierPercent /= 2;
					// </advc.171>
					int iReligionCount = kLoopPlayer.countTotalHasReligion();
					//int iCityCount = kOwner.getNumCities();
					int iCityCount = kLoopPlayer.getNumCities(); // K-Mod!
					//magic formula to produce normalized adjustment factor based on religious infusion
					int iAdjustment = 100 * (iCityCount + 1);
					iAdjustment /= iCityCount + 1 + iReligionCount;
					iAdjustment = ((iAdjustment - 25) * 4) / 3;

					iAdjustment = std::max(10, iAdjustment);

					iPlayerMultiplierPercent *= iAdjustment;
					iPlayerMultiplierPercent /= 100;
				}
			}
		}
		else if (iI == getOwner())
		{
			iPlayerMultiplierPercent = (bCultureVictory ? 1600 : 400) +
					(kOwner.getStateReligion() == eReligion ? 100 : 0);
		}
		else if (bHasHolyCity && kLoopPlayer.getTeam() == getTeam())
			iPlayerMultiplierPercent = (kLoopPlayer.getStateReligion() == eReligion ? 600 : 300);

		if (iPlayerMultiplierPercent > 0)
		{
			FOR_EACH_CITY(pLoopCity, kLoopPlayer)
			{
				if (!AI_canEnterByLand(pLoopCity->getArea())/* || // advc.030 (replacing same-area check)
					!AI_plotValid(pLoopCity->plot())*/) // advc.opt: Mostly redundant
				{
					continue;
				}
				if (!kOwner.AI().AI_deduceCitySite(*pLoopCity) || // K-Mod
					!canSpread(pLoopCity->plot(), eReligion) ||
					pLoopCity->getPlot().isVisibleEnemyUnit(this) ||
					kOwner.AI().AI_isAnyPlotTargetMissionAI(
					pLoopCity->getPlot(), MISSIONAI_SPREAD, kOwner.getSelectionGroup(getGroupID())))
				{
					continue;
				}
				int iPathTurns;
				if (generatePath(pLoopCity->getPlot(), MOVE_NO_ENEMY_TERRITORY, true, &iPathTurns))
				{
					int iValue = 16 + pLoopCity->getPopulation() * 4; // was 7 +

					iValue *= iPlayerMultiplierPercent;
					iValue /= 100;

					int iCityReligionCount = pLoopCity->getReligionCount();
					int iReligionCountFactor = iCityReligionCount;

					if (kLoopPlayer.getTeam() == kOwner.getTeam())
					{
						// count cities with no religion the same as cities with 2 religions
						// prefer a city with exactly 1 religion already
						if (iCityReligionCount == 0)
							iReligionCountFactor = 2;
						else if (iCityReligionCount == 1)
							iValue *= 2;
					}
					else
					{
						// absolutely prefer cities with zero religions
						if (iCityReligionCount == 0)
							iValue *= 2;
						// not our city, so prefer the lowest number of religions (increment so no divide by zero)
						iReligionCountFactor++;
					}
					iValue /= iReligionCountFactor;

					FAssert(iPathTurns > 0);
					bool bForceMove = false;

					if (isHuman())
					{	//If human, prefer to spread to the player where automated from.
						if (getPlot().getOwner() == pLoopCity->getOwner())
						{
							iValue *= 10;
							if (pLoopCity->isRevealed(getTeam()))
								bForceMove = true;
						}
					}

				    // doc: AI prefers spreading in core areas
				    if (!isHuman())
				    {
				        if (pLoopCity->getSpreadFactor(eReligion) == REGION_SPREAD_CORE)
                            iValue *= 10;
				        else if (pLoopCity->getSpreadFactor(eReligion) == REGION_SPREAD_HISTORICAL)
                            iValue *= 2;
				    }

					iValue *= 1000;

					if (iPathTurns > 0)
						iValue /= (iPathTurns + 2);

					if (iValue > iBestValue)
					{
						iBestValue = iValue;
						pBestPlot = &(bForceMove ?
								pLoopCity->getPlot() : getPathEndTurnPlot());
						pBestSpreadPlot = pLoopCity->plot();
					}
				}
			}
		}
	}

    return std::make_pair(pBestPlot, pBestSpreadPlot);
}

// K-Mod: I've basically rewritten this whole function.
bool CvUnitAI::AI_spreadCorporation()
{
	PROFILE_FUNC();

	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());

	CorporationTypes eCorporation = NO_CORPORATION;
	FOR_EACH_ENUM(Corporation)
	{
		if (getUnitInfo().getCorporationSpreads(eLoopCorporation) > 0)
		{
			eCorporation = eLoopCorporation;
			break;
		}
	}

	if (eCorporation == NO_CORPORATION ||
		!kOwner.isActiveCorporation(eCorporation)) // K-Mod
	{
		return false;
	}
	bool bHasHQ = GET_TEAM(getTeam()).hasHeadquarters(eCorporation);

	CvPlot* pBestPlot = NULL;
	CvPlot* pBestSpreadPlot = NULL;
	// K-Mod
	// first, if we are already doing a spread mission, continue that.
	if (AI_getGroup()->AI_getMissionAIType() == MISSIONAI_SPREAD_CORPORATION)
	{
		CvPlot* pMissionPlot = AI_getGroup()->AI_getMissionAIPlot();
		if (pMissionPlot != NULL &&
			pMissionPlot->getPlotCity() != NULL &&
			canSpreadCorporation(pMissionPlot, eCorporation, true) && // don't check gold here
			!pMissionPlot->isVisibleEnemyUnit(this) &&
			generatePath(*pMissionPlot, MOVE_NO_ENEMY_TERRITORY, true))
		{
			pBestPlot = &getPathEndTurnPlot();
			pBestSpreadPlot = pMissionPlot;
		}
	}

	if (pBestSpreadPlot == NULL)
	{
		PlayerTypes eTargetPlayer = NO_PLAYER;

		if (isHuman())
			eTargetPlayer = getPlot().isOwned() ? getPlot().getOwner() : getOwner();

		if (eTargetPlayer == NO_PLAYER ||
			GET_PLAYER(eTargetPlayer).isNoCorporations() ||
			GET_PLAYER(eTargetPlayer).isNoForeignCorporations() ||
			GET_PLAYER(eTargetPlayer).countCorporations(eCorporation, area()) >=
			getArea().getCitiesPerPlayer(eTargetPlayer))
		{
			if (kOwner.AI_executiveValue(eCorporation, area(), &eTargetPlayer, true) <= 0)
				return false; // corp is not worth spreading in this region.
		}
		int iBestValue = 0;
		for (PlayerAIIter<MAJOR_CIV> it; it.hasNext(); ++it)
		{
			CvPlayerAI const& kLoopPlayer = *it;
			if (canEnterTerritory(kLoopPlayer.getTeam()) &&
				getArea().getCitiesPerPlayer(kLoopPlayer.getID()) > 0)
			{	// advc: Unused. Attitude should matter though ... tbd.
				//AttitudeTypes eAttitude = GET_TEAM(getTeam()).AI_getAttitude(kLoopPlayer.getTeam());
				if (kLoopPlayer.getID() != eTargetPlayer && kLoopPlayer.getTeam() != getTeam())
					continue;
				FOR_EACH_CITYAI(pLoopCity, kLoopPlayer)
				{
					if (AI_canEnterByLand(pLoopCity->getArea()) && // advc.030 (replacing same-area check)
						//AI_plotValid(pLoopCity->plot()) && // advc.opt: Mostly redundant
						kOwner.AI_deduceCitySite(*pLoopCity) &&
						canSpreadCorporation(pLoopCity->plot(), eCorporation) &&
						!pLoopCity->getPlot().isVisibleEnemyUnit(this) &&
						!kOwner.AI_isAnyPlotTargetMissionAI(
						pLoopCity->getPlot(), MISSIONAI_SPREAD_CORPORATION, getGroup()))
					{
						int iPathTurns;
						if (!generatePath(pLoopCity->getPlot(), MOVE_NO_ENEMY_TERRITORY, true, &iPathTurns))
							continue;
						int iValue = 0;
						// we should probably calculate the true HqValue, but I couldn't be bothered right now.
						iValue += bHasHQ ? 1000 : 0;
						if (pLoopCity->getTeam() == getTeam())
						{
							//CvPlayerAI const& kCityOwner = GET_PLAYER(pLoopCity->getOwner()); // advc: That's kLoopPlayer
							iValue += kLoopPlayer.AI_corporationValue(eCorporation, pLoopCity);
							FOR_EACH_ENUM(Corporation)
							{
								if (pLoopCity->isHasCorporation(eLoopCorporation) &&
									GC.getGame().isCompetingCorporation(eLoopCorporation, eCorporation))
								{
									iValue -= kLoopPlayer.AI_corporationValue(eLoopCorporation, pLoopCity) +
											(GET_TEAM(getTeam()).hasHeadquarters(eLoopCorporation) ? 1100 : 100);
									// cf. iValue before AI_corporationValue is added.
								}
							}
						}
						if (iValue < 0)
							continue;
						iValue += 10 + pLoopCity->getPopulation() * 2;
						if (kLoopPlayer.getID() == eTargetPlayer)
							iValue *= 2;
						iValue *= 1000;
						iValue /= (iPathTurns + 1);
						if (iValue > iBestValue)
						{
							iBestValue = iValue;
							pBestPlot = &(isHuman() ?
									pLoopCity->getPlot() : getPathEndTurnPlot());
							pBestSpreadPlot = pLoopCity->plot();
						}
					}
				}
			}
		}
	}
	// K-Mod end

	// (original code deleted)

	if (pBestPlot != NULL && pBestSpreadPlot != NULL)
	{
		if (at(*pBestSpreadPlot))
		{
			if (canSpreadCorporation(pBestSpreadPlot, eCorporation))
			{
				getGroup()->pushMission(MISSION_SPREAD_CORPORATION, eCorporation);
				return true;
			}
			//else
			else if (GET_PLAYER(getOwner()).getGold() <
				spreadCorporationCost(eCorporation, pBestSpreadPlot->getPlotCity()))
			{
				// wait for more money
				getGroup()->pushMission(MISSION_SKIP, -1, -1, NO_MOVEMENT_FLAGS,
						false, false, MISSIONAI_SPREAD_CORPORATION, pBestSpreadPlot);
				return true;
			}
			// FErrorMsg("AI_spreadCorporation has taken us to a bogus pBestSpreadPlot");
			// this can happen from time to time. For example, when the player loses their only corp resources while the exec is en route.
		}
		else
		{
			pushGroupMoveTo(*pBestPlot, MOVE_NO_ENEMY_TERRITORY, false, false,
					MISSIONAI_SPREAD_CORPORATION, pBestSpreadPlot);
			return true;
		}
	}

	return false;
}

bool CvUnitAI::AI_spreadReligionAirlift()
{
	PROFILE_FUNC();

	if (getGroup()->getNumUnits() > 1)
		return false;

	CvCity* pCity = getPlot().getPlotCity();

	if (pCity == NULL)
		return false;

	if (pCity->getMaxAirlift() == 0)
		return false;

	//bool bCultureVictory = GET_PLAYER(getOwner()).AI_isDoStrategy(AI_STRATEGY_CULTURE2);
	ReligionTypes eReligion = NO_RELIGION;
	//if (eReligion == NO_RELIGION) { // advc: redundant
	if (GET_PLAYER(getOwner()).getStateReligion() != NO_RELIGION &&
		getUnitInfo().getReligionSpreads(GET_PLAYER(getOwner()).getStateReligion()) > 0)
	{
		eReligion = GET_PLAYER(getOwner()).getStateReligion();
	}

	if (eReligion == NO_RELIGION)
	{
		FOR_EACH_ENUM(Religion)
		{
			//if (bCultureVictory || GET_TEAM(getTeam()).hasHolyCity(eLoopReligion)) {
			if (getUnitInfo().getReligionSpreads(eLoopReligion) > 0)
			{
				eReligion = eLoopReligion;
				break;
			}
		}
	}

	if (eReligion == NO_RELIGION)
		return false;

	int iBestValue = 0;
	CvPlot* pBestPlot = NULL;

	for (MemberIter it(getTeam()); it.hasNext(); ++it)
	{
		CvPlayer const& kMember = *it;
		FOR_EACH_CITY(pLoopCity, kMember)
		{
			if (!canAirliftAt(pCity->plot(), pLoopCity->getX(), pLoopCity->getY()) ||
				!canSpread(pLoopCity->plot(), eReligion) ||
				GET_PLAYER(getOwner()).AI_isAnyPlotTargetMissionAI(
				pLoopCity->getPlot(), MISSIONAI_SPREAD, getGroup()))
			{
				continue;
			}
			/*  UNOFFICIAL_PATCH, Unit AI, 08/04/09, jdog5000 START
				Don't airlift where there's already one of our unit types (probably just airlifted) */
			if (pLoopCity->getPlot().plotCount(PUF_isUnitType, getUnitType(), -1, getOwner()) > 0)
				continue;
			// UNOFFICIAL_PATCH: END
			int iValue = (7 + (pLoopCity->getPopulation() * 4));

			int iCityReligionCount = pLoopCity->getReligionCount();
			int iReligionCountFactor = iCityReligionCount;

			/*	count cities with no religion the same as cities with 2 religions
				prefer a city with exactly 1 religion already */
			if (iCityReligionCount == 0)
				iReligionCountFactor = 2;
			else if (iCityReligionCount == 1)
				iValue *= 2;
			iValue /= iReligionCountFactor;
			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				pBestPlot = pLoopCity->plot();
			}
		}
	}
	if (pBestPlot != NULL)
	{
		getGroup()->pushMission(MISSION_AIRLIFT, pBestPlot->getX(), pBestPlot->getY(),
				NO_MOVEMENT_FLAGS, false, false, MISSIONAI_SPREAD, pBestPlot);
		return true;
	}
	return false;
}

bool CvUnitAI::AI_spreadCorporationAirlift()
{
	PROFILE_FUNC();

	if (getGroup()->getNumUnits() > 1)
		return false;

	CvCity* pCity = getPlot().getPlotCity();

	if (pCity == NULL)
		return false;

	if (pCity->getMaxAirlift() == 0)
		return false;

	CorporationTypes eCorporation = NO_CORPORATION;
	FOR_EACH_ENUM(Corporation)
	{
		if (getUnitInfo().getCorporationSpreads(eLoopCorporation) > 0)
		{
			eCorporation = (eLoopCorporation);
			break;
		}
	}
	if (eCorporation == NO_CORPORATION)
		return false;

	int iBestValue = 0;
	CvPlot* pBestPlot = NULL;
	for (MemberIter it(getTeam()); it.hasNext(); ++it)
	{
		CvPlayer const& kMember = *it;
		FOR_EACH_CITY(pLoopCity, kMember)
		{
			if (!canAirliftAt(pCity->plot(), pLoopCity->getX(), pLoopCity->getY()) ||
				!canSpreadCorporation(pLoopCity->plot(), eCorporation) ||
				GET_PLAYER(getOwner()).AI_isAnyPlotTargetMissionAI(
				pLoopCity->getPlot(),MISSIONAI_SPREAD_CORPORATION, getGroup()))
			{
				continue;
			}
			/*  UNOFFICIAL_PATCH, Unit AI, 08/04/09, jdog5000: START
				Don't airlift where there's already one of our unit types (probably just airlifted) */
			if (pLoopCity->getPlot().plotCount(PUF_isUnitType, getUnitType(), -1, getOwner()) > 0)
				continue;
			// UNOFFICIAL_PATCH: END
			int iValue = (pLoopCity->getPopulation() * 4);
			if (pLoopCity->getOwner() == getOwner())
				iValue *= 4;
			else iValue *= 3;
			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				pBestPlot = pLoopCity->plot();
			}
		}
	}

	if (pBestPlot != NULL)
	{
		getGroup()->pushMission(MISSION_AIRLIFT,
				pBestPlot->getX(), pBestPlot->getY(),
				NO_MOVEMENT_FLAGS, false, false,
				MISSIONAI_SPREAD, pBestPlot);
		return true;
	}

	return false;
}


bool CvUnitAI::AI_discover(bool bThisTurnOnly, bool bFirstResearchOnly)
{
    // doc: House of Wisdom: settling the unit is preferable
    if (GET_PLAYER(getOwner()).isHasBuildingEffect(HOUSE_OF_WISDOM) && AI_join())
        return true;

	if(!canDiscover(plot()))
		return false;

	TechTypes const eFirstDiscoverTech = getDiscoveryTech();
    TechTypes const eSecondDiscoverTech = getDiscoveryTech(eFirstDiscoverTech); // doc: can discover two techs
	bool const bFirstFirstTech = GET_PLAYER(getOwner()).AI_isFirstTech(eFirstDiscoverTech);
	bool const bSecondFirstTech = GET_PLAYER(getOwner()).AI_isFirstTech(eSecondDiscoverTech);

	if (bFirstResearchOnly && !bFirstFirstTech && !bSecondFirstTech)
		return false;

    // doc: can discover two techs
    int iFirstResearch = 0;
    int iSecondResearch = 0;
	int iFirstLeft = 0;
	int iSecondLeft = 0;
    if (eFirstDiscoverTech != NO_TECH)
    {
        iFirstLeft = GET_TEAM(getTeam()).getResearchLeft(eFirstDiscoverTech);
        iFirstResearch = std::min(getDiscoverResearch(eFirstDiscoverTech), iFirstLeft);

        if (eSecondDiscoverTech != NO_TECH)
        {
            iSecondLeft = GET_TEAM(getTeam()).getResearchLeft(eSecondDiscoverTech);
            iSecondResearch = std::max(0, std::min(getDiscoverResearch(eSecondDiscoverTech) - iFirstLeft, iSecondLeft));
        }
    }

	int iPercentWasted = (100 - (((iFirstResearch + iSecondResearch) * 100) / getDiscoverResearch(NO_TECH))); // doc
	FAssert((iPercentWasted >= 0 && iPercentWasted <= 100));

	if (iFirstResearch >= iFirstLeft)
	{
		if (iPercentWasted < 51 && bFirstResearchOnly && (bFirstFirstTech || bSecondFirstTech))
		{
			getGroup()->pushMission(MISSION_DISCOVER);
			return true;
		}

		if (iPercentWasted < ((bFirstFirstTech || bSecondFirstTech) ? 31 : 11))
		{
			/*	I need a good way to assess if the tech is actually valuable...
				but don't have one. */
			getGroup()->pushMission(MISSION_DISCOVER);
			return true;
		}
	}
	else if (bThisTurnOnly)
		return false;

	if (iPercentWasted <= 11)
	{
		if (GET_PLAYER(getOwner()).getCurrentResearch() == eFirstDiscoverTech ||
            (GET_PLAYER(getOwner()).getCurrentResearch() == eSecondDiscoverTech && iSecondResearch > 0)) // doc: can discover two techs
		{
			getGroup()->pushMission(MISSION_DISCOVER);
			return true;
		}
	}

	return false;
}


bool CvUnitAI::AI_lead(std::vector<UnitAITypes>& aeUnitAITypes)
{
	PROFILE_FUNC();

	FAssert(!isHuman());
	FAssert(AI_getUnitAIType() != NO_UNITAI);

	bool bNeedLeader = false;
	for (TeamIter<CIV_ALIVE,ENEMY_OF> it(getTeam()); it.hasNext(); ++it)
	{
		if (it->countNumUnitsByArea(getArea()) > 0)
		{
			bNeedLeader = true;
			break;
		}
	}

	CvUnit const* pBestUnit = NULL;
	CvPlot* pBestPlot = NULL;

	// AI may use Warlords to create super-medic units
	CvUnit const* pBestStrUnit = NULL;
	CvPlot* pBestStrPlot = NULL;

	CvUnit const* pBestHealUnit = NULL;
	CvPlot* pBestHealPlot = NULL;
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());
	// BETTER_BTS_AI_MOD, Great People AI, Unit AI, 05/14/10, jdog5000: START
	if (bNeedLeader)
	{
		int iBestStrength = 0;
		int iBestHealing = 0;
		FOR_EACH_UNITAI(pLoopUnit, kOwner)
		{
			bool bValid = GC.getInfo(pLoopUnit->getUnitClassType()).isWorldUnit();
			if (!bValid)
			{
				for (size_t i = 0; i < aeUnitAITypes.size(); i++)
				{
					if (pLoopUnit->AI_getUnitAIType() == aeUnitAITypes[i] ||
						aeUnitAITypes[i] == NO_UNITAI)
					{
						bValid = true;
						break;
					}
				}
			}
			if (!bValid)
				continue;
			if (canLead(pLoopUnit->plot(), pLoopUnit->getID()) > 0 &&
				AI_plotValid(pLoopUnit->plot()) &&
				// advc.opt: It's our unit; enemies can't coexist.
				//!pLoopUnit->getPlot().isVisibleEnemyUnit(this))
				pLoopUnit->combatLimit() == 100 &&
                !pLoopUnit->isHasPromotion(PROMOTION_MERCENARY)) // doc: mercenaries cannot become generals // TODO: should be in canLead?
			{
				if (!generatePath(pLoopUnit->getPlot(), MOVE_AVOID_ENEMY_WEIGHT_3, true))
					continue;
				// pick the unit with the highest current strength
				int iCombatStrength = pLoopUnit->currCombatStr(NULL, NULL);
				iCombatStrength *= 30 + pLoopUnit->getExperience();
				iCombatStrength /= 30;
				{
					int const iMaxGlobal = GC.getInfo(pLoopUnit->getUnitClassType()).
							getMaxGlobalInstances();
					if (iMaxGlobal > 0)
					{
						iCombatStrength *= 1 + iMaxGlobal;
						iCombatStrength /= std::max(1, iMaxGlobal);
					}
				}
				if (iCombatStrength > iBestStrength)
				{
					iBestStrength = iCombatStrength;
					pBestStrUnit = pLoopUnit;
					pBestStrPlot = &getPathEndTurnPlot();
				}
				// or the unit with the best healing ability
				int iHealing = pLoopUnit->getSameTileHeal() + pLoopUnit->getAdjacentTileHeal();
				if (iHealing > iBestHealing)
				{
					iBestHealing = iHealing;
					pBestHealUnit = pLoopUnit;
					pBestHealPlot = &getPathEndTurnPlot();
				}
			}
		}
	}

	if (AI_getBirthmark() % 3 == 0 && pBestHealUnit != NULL)
	{
		pBestPlot = pBestHealPlot;
		pBestUnit = pBestHealUnit;
	}
	else
	{
		pBestPlot = pBestStrPlot;
		pBestUnit = pBestStrUnit;
	}

	if (pBestPlot != NULL)
	{
		if (at(*pBestPlot) && pBestUnit != NULL)
		{
			if (gUnitLogLevel > 2)
			{
				CvWString szString; getUnitAIString(szString, pBestUnit->AI_getUnitAIType());
				logBBAI("      Great general %d for %S chooses to lead %S with UNITAI %S", getID(), kOwner.getCivilizationDescription(0), pBestUnit->getName(0).GetCString(), szString.GetCString());
			}
			getGroup()->pushMission(MISSION_LEAD, pBestUnit->getID());
			return true;
		}
		else
		{
			pushGroupMoveTo(*pBestPlot, MOVE_AVOID_ENEMY_WEIGHT_3);
			return true;
		}
	}
	// BETTER_BTS_AI_MOD: END

	return false;
}

// iMaxCounts = 1 would mean join a city if there's no existing joined GP of that type.
/*  advc (note): This function has been replaced by K-Mod's AI_greatPersonMove for
	all GP except GG. Should probably also use the K-Mod code for GG. (Tbd.) */
bool CvUnitAI::AI_join(int iMaxCount)
{
	PROFILE_FUNC();

	int iBestValue = 0;
	CvPlot* pBestPlot = NULL;
	SpecialistTypes eBestSpecialist = NO_SPECIALIST;
	int iCount = 0;
	FOR_EACH_CITYAI(pLoopCity, GET_PLAYER(getOwner()))
	{
		// BETTER_BTS_AI_MOD, Unit AI, Efficiency, 08/19/09, jdog5000: START
		// BBAI efficiency: check same area
		if (!AI_canEnterByLand(pLoopCity->getArea()) // advc.030 (replacing same-area check)
			/*|| AI_plotValid(pLoopCity->plot())*/) // advc.opt: Mostly redundant
		{
			continue;
		}
		//if (pLoopCity->getPlot().isVisibleEnemyUnit(this))
		if (!pLoopCity->AI_isSafe()) // advc.139: Replacing the above
			continue;
		if (!generatePath(pLoopCity->getPlot(), MOVE_SAFE_TERRITORY, true))
			continue;
		// BETTER_BTS_AI_MOD: END
		FOR_EACH_ENUM(Specialist)
		{
			bool bDoesJoin = false;
			if (getUnitInfo().getGreatPeoples(eLoopSpecialist))
				bDoesJoin = true;
			if (bDoesJoin)
			{
				iCount += pLoopCity->getSpecialistCount(eLoopSpecialist);
				if (iCount >= iMaxCount)
					return false;
			}
			if (canJoin(pLoopCity->plot(), eLoopSpecialist))
			{
				// BETTER_BTS_AI_MOD, Unit AI, Efficiency, 08/20/09, jdog5000: was AI_getPlotDanger
				if (!GET_PLAYER(getOwner()).AI_isAnyPlotDanger(*pLoopCity->plot(), 2))
				{
					//iValue = pLoopCity->AI_specialistValue(eLoopSpecialist, pLoopCity->AI_avoidGrowth(), false);
					int iValue = pLoopCity->AI_permanentSpecialistValue(eLoopSpecialist); // K-Mod
					if (iValue > iBestValue)
					{
						iBestValue = iValue;
						pBestPlot = &getPathEndTurnPlot();
						eBestSpecialist = eLoopSpecialist;
					}
				}
			}
		}
	}

	if (pBestPlot != NULL && eBestSpecialist != NO_SPECIALIST)
	{
		if (at(*pBestPlot))
		{
			getGroup()->pushMission(MISSION_JOIN, eBestSpecialist);
			return true;
		}
		else
		{
			// BETTER_BTS_AI_MOD, Unit AI, 03/09/09, jdog5000:
			pushGroupMoveTo(*pBestPlot, MOVE_SAFE_TERRITORY);
			return true;
		}
	}

	return false;
}

// iMaxCount = 1 would mean construct only if there are no existing buildings constructed by this GP type.
// advc (note): Only used for Great General; see comment above AI_join.
bool CvUnitAI::AI_construct(int iMaxCount, int iMaxSingleBuildingCount, int iThreshold)
{
	PROFILE_FUNC();
	// <advc.003t>
	if (!getUnitInfo().isAnyBuildings())
		return false; // </advc.003t>
	int iBestValue = 0;
	CvPlot* pBestPlot = NULL;
	CvPlot* pBestConstructPlot = NULL;
	BuildingTypes eBestBuilding = NO_BUILDING;
	int iCount = 0;
	FOR_EACH_CITYAI(pLoopCity, GET_PLAYER(getOwner()))
	{
		if (!AI_canEnterByLand(pLoopCity->getArea()) || // advc.030 (replacing same-area check)
			//!AI_plotValid(pLoopCity->plot()) || // advc.opt: Mostly redundant
			//pLoopCity->getPlot().isVisibleEnemyUnit(this))
			pLoopCity->AI_isSafe()) // advc.139: Replacing the above
		{
			continue;
		}
		//if (GET_PLAYER(getOwner()).AI_plotTargetMissionAIs(pLoopCity->plot(), MISSIONAI_CONSTRUCT, getGroup()) == 0)
		// above line disabled by K-Mod, because there are different types of buildings to construct...
		CvCivilization const& kCiv = GET_PLAYER(getOwner()).getCivilization(); // advc.003w
		for (int i = 0; i < kCiv.getNumBuildings(); i++)
		{
			BuildingTypes eBuilding = kCiv.buildingAt(i);
			bool bDoesBuild = false;
			if (//getUnitInfo().getForceBuildings(eBuilding) || // advc.003t
					getUnitInfo().getBuildings(eBuilding))
				bDoesBuild = true;
			if (bDoesBuild && (pLoopCity->getNumBuilding(eBuilding) > 0))
			{
				iCount++;
				if (iCount >= iMaxCount)
					return false;
			}
			if (bDoesBuild && GET_PLAYER(getOwner()).getBuildingClassCount(
				kCiv.buildingClassAt(i)) < iMaxSingleBuildingCount)
			{
				if (canConstruct(pLoopCity->plot(), eBuilding) &&
					generatePath(pLoopCity->getPlot(), MOVE_NO_ENEMY_TERRITORY, true)) // K-Mod
				{
					int iValue = pLoopCity->AI_buildingValue(eBuilding);

					if (iValue > iThreshold && iValue > iBestValue)
					{
						iBestValue = iValue;
						pBestPlot = &getPathEndTurnPlot();
						pBestConstructPlot = pLoopCity->plot();
						eBestBuilding = eBuilding;
					}
				}
			}
		}
	}

	if (pBestPlot != NULL && pBestConstructPlot != NULL && eBestBuilding != NO_BUILDING)
	{
		if (at(*pBestConstructPlot))
		{
			getGroup()->pushMission(MISSION_CONSTRUCT, eBestBuilding);
			return true;
		}
		else
		{
			// BETTER_BTS_AI_MOD, Unit AI, 03/09/09, jdog5000:
			pushGroupMoveTo(*pBestPlot, MOVE_NO_ENEMY_TERRITORY, false, false,
					MISSIONAI_CONSTRUCT, pBestConstructPlot);
			return true;
		}
	}

	return false;
}

// advc.003j: Obsoleted by K-Mod (AI_greatPersonMove)
#if 0
bool CvUnitAI::AI_switchHurry()
{
	CvCity* pCity = getPlot().getPlotCity();

	if ((pCity == NULL) || (pCity->getOwner() != getOwner()))
	{
		return false;
	}

	int iBestValue = 0;
	BuildingTypes eBestBuilding = NO_BUILDING;

	for (int iI = 0; iI < GC.getNumBuildingClassInfos(); iI++)
	{
		if (GC.getInfo((BuildingClassTypes)iI).isWorldWonder())
		{
			BuildingTypes eBuilding = (BuildingTypes)GC.getInfo(getCivilizationType()).getCivilizationBuildings(iI);

			if (NO_BUILDING != eBuilding)
			{
				if (pCity->canConstruct(eBuilding))
				{
					if (pCity->getBuildingProduction(eBuilding) == 0)
					{
						if (getMaxHurryProduction(pCity) >= pCity->getProductionNeeded(eBuilding))
						{
                            int iBuildingPreference = GET_PLAYER(getOwner()).getBuildingClassPreference(eBuilding);
                            if (iBuildingPreference != MAX_INT && iBuildingPreference <= 0)
                                continue;

							int iValue = pCity->AI_buildingValue(eBuilding);

							if (iValue > iBestValue)
							{
								iBestValue = iValue;
								eBestBuilding = eBuilding;
							}
						}
					}
				}
			}
		}
	}

	if (eBestBuilding != NO_BUILDING)
	{
		pCity->pushOrder(ORDER_CONSTRUCT, eBestBuilding);

		if (pCity->getProductionBuilding() == eBestBuilding)
		{
			if (canHurry(plot()))
			{
				getGroup()->pushMission(MISSION_HURRY);
				return true;
			}
		}

		FAssert(false);
	}

	return false;
}


bool CvUnitAI::AI_hurry()
{
	PROFILE_FUNC();

	int iBestValue = 0;
	CvPlot* pBestPlot = NULL;
	CvPlot* pBestHurryPlot = NULL;
	FOR_EACH_CITY(pLoopCity, GET_PLAYER(getOwner()))
	{	// BETTER_BTS_AI_MOD, Unit AI, Efficiency, 08/19/09, jdog5000: check same area
		if (AI_canEnterByLand(pLoopCity->getArea()) && // advc.030
			/*AI_plotValid(pLoopCity->plot())*/) // advc.opt: Mostly redundant
		{
			if (canHurry(pLoopCity->plot()))
			{
				if (!pLoopCity->getPlot().isVisibleEnemyUnit(this))
				{
					if (GET_PLAYER(getOwner()).AI_plotTargetMissionAIs(pLoopCity->plot(), MISSIONAI_HURRY, getGroup()) == 0)
					{
						int iPathTurns;
						// BETTER_BTS_AI_MOD, Unit AI, 04/03/09, jdog5000: flag was 0
						if (generatePath(pLoopCity->plot(), MOVE_NO_ENEMY_TERRITORY, true, &iPathTurns))
						{
							bool bHurry = false;

							if (pLoopCity->isProductionBuilding())
							{
								if (GC.getInfo(pLoopCity->getProductionBuilding()).isWorldWonder())
									bHurry = true;
							}

							if (bHurry)
							{
								int iTurnsLeft = pLoopCity->getProductionTurnsLeft();
								// <advc.004x>
								if(iTurnsLeft == MAX_INT)
									continue; // </advc.004x>
								iTurnsLeft -= iPathTurns;

								if (iTurnsLeft > 8)
								{
									int iValue = iTurnsLeft;

									if (iValue > iBestValue)
									{
										iBestValue = iValue;
										pBestPlot = &getPathEndTurnPlot();
										pBestHurryPlot = pLoopCity->plot();
									}
								}
							}
						}
					}
				}
			}
		}
	}

	if (pBestPlot != NULL && pBestHurryPlot != NULL)
	{
		if (at(*pBestHurryPlot))
		{
			getGroup()->pushMission(MISSION_HURRY);
			return true;
		}
		else
		{
			pushGroupMoveTo(*pBestPlot,
					MOVE_NO_ENEMY_TERRITORY, // BETTER_BTS_AI_MOD, Unit AI, 03/09/09, jdog5000
					false, false, MISSIONAI_HURRY, pBestHurryPlot);
			return true;
		}
	}

	return false;
}
#endif // advc.003j

/* disabled by K-Mod. obsolete.
bool CvUnitAI::AI_greatWork()
{ ... } */ // advc: deleted


bool CvUnitAI::AI_offensiveAirlift()
{
	PROFILE_FUNC();

	if (getGroup()->getNumUnits() > 1)
		return false;

	if (getArea().AI_getTargetCity(getOwner()) != NULL)
		return false;

	CvCity* pCity = getPlot().getPlotCity();
	if (pCity == NULL)
		return false;

	if (pCity->getMaxAirlift() == 0)
		return false;

	CvPlot* pBestPlot = NULL;
	int iBestValue = 0;
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());
	FOR_EACH_CITY(pLoopCity, kOwner)
	{
		if (pLoopCity->sameArea(*pCity))
			continue;
		if (!canAirliftAt(pCity->plot(), pLoopCity->getX(), pLoopCity->getY()))
			continue;
		CvCityAI const* pTargetCity = pLoopCity->getArea().AI_getTargetCity(kOwner.getID());
		if (pTargetCity == NULL)
			continue;
		/* AreaAITypes eAreaAIType = pTargetCity->getArea().getAreaAIType(getTeam());
		if ((eAreaAIType == AREAAI_OFFENSIVE || eAreaAIType == AREAAI_DEFENSIVE || eAreaAIType == AREAAI_MASSING)
			|| pTargetCity->AI_isDanger()) */
		if (!kOwner.AI_isLandWar(pTargetCity->getArea()) // K-Mod
			&& !pTargetCity->AI_isDanger())
		{
			continue;
		}
		int iValue = 10000;
		iValue *= kOwner.AI_militaryWeight(pLoopCity->area()) + 10;
		iValue /= kOwner.AI_totalAreaUnitAIs(pLoopCity->getArea(), AI_getUnitAIType()) + 10;
		iValue += std::max(1, GC.getMap().maxStepDistance() * 2 -
				GC.getMap().calculatePathDistance(pLoopCity->plot(), pTargetCity->plot()));
		if (AI_getUnitAIType() == UNITAI_PARADROP)
		{
			CvCity* pNearestEnemyCity = GC.getMap().findCity(pLoopCity->getX(), pLoopCity->getY(),
					NO_PLAYER, NO_TEAM, false, false, getTeam());
			if (pNearestEnemyCity != NULL)
			{
				int iDistance = plotDistance(pLoopCity->plot(), pNearestEnemyCity->plot());
				if (iDistance <= getDropRange())
					iValue *= 5;
			}
		}
		if (iValue > iBestValue)
		{
			iBestValue = iValue;
			pBestPlot = pLoopCity->plot();
			FAssert(pLoopCity != pCity);
		}
	}
	if (pBestPlot != NULL)
	{
		getGroup()->pushMission(MISSION_AIRLIFT, pBestPlot->getX(), pBestPlot->getY());
		return true;
	}
	return false;
}


bool CvUnitAI::AI_paradrop(int iRange)
{
	PROFILE_FUNC();

	if (getGroup()->getNumUnits() > 1)
		return false;

	int iParatrooperCount = getPlot().plotCount(PUF_isUnitAIType, UNITAI_PARADROP, -1, getOwner());
	FAssert(iParatrooperCount > 0);

	if (!canParadrop(plot()))
		return false;

	CvPlot const* pBestPlot = NULL;
	int iBestValue = 0;
	CvTeamAI const& kOurTeam = GET_TEAM(getTeam()); // advc
	for (SquareIter it(*this, AI_searchRange(iRange)); it.hasNext(); ++it)
	{
		CvPlot& p = *it;
		PlayerTypes const eTargetPlayer = p.getOwner();
		if (//!isPotentialEnemy(p.getTeam(), &p) ||
			// advc:
			eTargetPlayer == NO_PLAYER || !kOurTeam.AI_mayAttack(TEAMID(eTargetPlayer)) ||
			!canParadropAt(plot(), p.getX(), p.getY()))
		{
			continue;
		}
		int iValue = 0;
		/*if (NO_BONUS != p.getBonusType())
			iValue += GET_PLAYER(eTargetPlayer).AI_bonusVal(p.getBonusType()) - 10;*/ // BtS
		/*	UNOFFICIAL_PATCH, Bugfix, 08/01/08, jdog5000: START
			Bonus values for bonuses the AI has are less than 10 for non-strategic resources.
			Since this is in the AI territory they probably have it. */
		if (p.getNonObsoleteBonusType(getTeam()) != NO_BONUS)
		{
			iValue += std::max(1,GET_PLAYER(eTargetPlayer).AI_bonusVal(
					p.getBonusType(), 0) - 10);
		}
		// UNOFFICIAL_PATCH: END
		FOR_EACH_ADJ_PLOT(p)
		{
			CvCity* pAdjCity = pAdj->getPlotCity();
			if (pAdjCity == NULL || pAdjCity->getOwner() != eTargetPlayer)
				continue;
			int iAttackerCount = GET_PLAYER(getOwner()).
					AI_adjacentPotentialAttackers(*pAdj, true);
			int iDefenderCount = pAdj->getNumVisibleEnemyDefenders(this);
			iValue += 20 * (AI_attackOdds(pAdj, true) -
					((50 * iDefenderCount) / (iParatrooperCount + iAttackerCount)));
		}
		if (iValue <= 0)
			continue;
		//iValue += pLoopPlot->defenseModifier(getTeam(), ignoreBuildingDefense());
		/*  advc.012: Whether our unit ignores building defense shouldn't matter
			b/c we can't drop into an enemy city. */
		iValue += AI_plotDefense(&p);
		CvUnit* pInterceptor = bestInterceptor(p,
				// advc.128: Don't always cheat with visibility (only 90% of the time)
				m_iSearchRangeRandPercent > 10);
		if (pInterceptor != NULL)
		{
			int iInterceptProb = (isSuicide() ? 100 :
					pInterceptor->currInterceptionProbability());
			iInterceptProb *= std::max(0, 100 - evasionProbability());
			iInterceptProb /= 100;
			iValue *= std::max(0, 100 - iInterceptProb / 2);
			iValue /= 100;
		}
		if (iValue > iBestValue)
		{
			iBestValue = iValue;
			pBestPlot = &p;
			FAssert(!atPlot(pBestPlot));
		}
	}

	if (pBestPlot != NULL)
	{
		getGroup()->pushMission(MISSION_PARADROP, pBestPlot->getX(), pBestPlot->getY());
		return true;
	}

	return false;
}

#if 0
/*  advc.003j: This function was replaced by K-Mod's AI_defendTerritory.
	The eFlags and iMaxPathTurns parameters of AI_protect were switched in
	this file; I've corrected this although the function is unused; also in
	the commented-out code at the call locations. */
bool CvUnitAI::AI_protect(int iOddsThreshold, MovementFlags eFlags, int iMaxPathTurns)
{
	PROFILE_FUNC();

	int iBestValue = 0;
	CvPlot* pBestPlot = NULL;

	for (int iI = 0; iI < GC.getMap().numPlots(); iI++)
	{
		CvPlot* pLoopPlot = GC.getMap().plotByIndex(iI);

		if (pLoopPlot->getOwner() == getOwner())
		{
			if (AI_plotValid(pLoopPlot))
			{
				if (pLoopPlot->isVisibleEnemyUnit(this))
				{
					if (!atPlot(pLoopPlot))
					{
						// BBAI efficiency: Check area for land units
						if (getDomainType() != DOMAIN_LAND || pLoopPlot->isArea(getArea()) || getGroup()->canMoveAllTerrain())
						{
							// BBAI efficiency: Most of the time, path will exist and odds will be checked anyway.  When path doesn't exist, checking path
							// takes longer.  Therefore, check odds first.
							//iValue = getGroup()->AI_attackOdds(pLoopPlot, true);
							int iValue = AI_getWeightedOdds(pLoopPlot, false); // K-Mod
							BonusTypes eBonus = pLoopPlot->getNonObsoleteBonusType(getTeam()); // K-Mod

							//if ((iValue >= AI_finalOddsThreshold(pLoopPlot, iOddsThreshold)) && (iValue*50 > iBestValue))
							if (iValue >= iOddsThreshold && (eBonus != NO_BONUS || iValue*50 > iBestValue)) // K-Mod
							{
								int iPathTurns;
								if (generatePath(pLoopPlot, eFlags, true, &iPathTurns, iMaxPathTurns))
								{
									// BBAI TODO: Other units targeting this already (if path turns > 1 or 0)?
									if (iPathTurns <= iMaxPathTurns)
									{
										iValue *= 100;

										iValue /= (2 + iPathTurns);

										// K-Mod
										if (eBonus != NO_BONUS)
										{
											iValue *= 10 + GET_PLAYER(getOwner()).AI_bonusVal(eBonus, 0);
											iValue /= 10;
										}
										// K-Mod end

										if (iValue > iBestValue)
										{
											iBestValue = iValue;
											pBestPlot = &getPathEndTurnPlot();
											FAssert(!at(*pBestPlot));
										}
									}
								}
							}
						}
					}
				}
			}
		}
	}

	if (pBestPlot != NULL)
	{
		pushGroupMoveTo(*pBestPlot, eFlags);
		return true;
	}

	return false;
}
#endif // advc.003j


bool CvUnitAI::AI_patrol() // advc: refactored
{
	PROFILE_FUNC();
	// <advc.102> Only patrol near own territory
	if (!isBarbarian())
	{
		bool bFound = false;
		CvPlayer const& kOwner = GET_PLAYER(getOwner());
		FOR_EACH_CITY(pCity, kOwner)
		{
			if(::plotDistance(pCity->plot(), plot()) <= 10)
			{
				bFound = true;
				break;
			}
		}
		if(!bFound)
			return false;
	}
	int iFacedX = -100, iFacedY = -100;
	{
		CvPlot* pFacedPlot = plotDirection(getX(), getY(), getFacingDirection(true));
		if(pFacedPlot != NULL)
		{
			iFacedX = pFacedPlot->getX();
			iFacedY = pFacedPlot->getY();
		}
	} // </advc.102>

	int iBestValue = 0;
	CvPlot* pBestPlot = NULL;
	int iFirst = 0; // advc.007
	FOR_EACH_ADJ_PLOT2(pAdjacentPlot, getPlot())
	{
		CvPlot const& kAdj = *pAdjacentPlot;
		if (!AI_plotValid(kAdj) ||
			kAdj.isVisibleEnemyUnit(this) ||
			!generatePath(kAdj, NO_MOVEMENT_FLAGS, true))
		{
			continue;
		}
		/*  <advc.102> Non-Barbarian AI should only patrol tiles it doesn't own b/c
			owned tiles have visibility anyway. In order to get to unowned tiles,
			however, units may have to traverse owned tiles, so they need to be
			allowed to patrol into owned tiles at least under some circumstances. */
		if (!isBarbarian() && kAdj.getOwner() == getOwner() &&
			// Make sure not to hamper early exploration (perhaps not an issue)
			GC.getGame().getElapsedGameTurns() >= 25 &&
			(kAdj.isUnit() || fixp(0.9).randSuccess(syncRand(),
			iFirst++ <= 0 ? "AI_patrol (first)" : NULL))) // advc.007: Don't pollute MPLog
		{
			continue;
		}
		// </advc.102>
		int iValue = 1 + SyncRandNum(10000);
		// advc.309: Moved this if/else up
		if (isBarbarian() &&
			/*  advc.306: (Patrolling Barbarian ships should pretty much
				move about randomly, neither seeking nor avoiding owned tiles.) */
			!getPlot().isWater())
		{
			if (!kAdj.isOwned())
				iValue += 20000;
			if (!kAdj.isAdjacentOwned())
				iValue += 10000;
			// <advc.304>
			if (!isAnimal() && getPlot().isHabitable())
				iValue += GC.getGame().getBarbarianWeightMap().get(kAdj) * 50;
			// </advc.304>
		}
		else
		{
			if (kAdj.isRevealedGoody(getTeam()))
				iValue += 100000;
			/* advc.102: Don't prefer own tiles
			if (pAdjacentPlot->getOwner() == getOwner())
				iValue += 10000;*/
		}
		// <advc.309>
		if (isAnimal())
		{
			// Same check as in CvGame::createAnimals
			if ((kAdj.isFeature()) ?
				getUnitInfo().getFeatureNative(kAdj.getFeatureType()) :
				getUnitInfo().getTerrainNative(kAdj.getTerrainType()))
			{
				iValue += SyncRandNum(10000);
			}
			/*	Neither a native terrain nor at least adjacent to
				a native feature: probably avoid */
			if (!getUnitInfo().getTerrainNative(kAdj.getTerrainType()) &&
				(!kAdj.isFeature() ||
				!getUnitInfo().getFeatureNative(kAdj.getFeatureType())))
			{
				bool bNativeFeatureFound = false;
				FOR_EACH_ADJ_PLOT2(pAdjAdj, kAdj)
				{
					if (pAdjAdj->isFeature() &&
						getUnitInfo().getFeatureNative(pAdjAdj->getFeatureType()))
					{
						bNativeFeatureFound = true;
						break;
					}
				}
				if (!bNativeFeatureFound)
					iValue /= 2;
			}
		}
		else // (Animals shouldn't follow a consistent direction)
		{ // </advc.309>
			/*  <advc.102> Prefer faced plot or a plot that's
				orthogonally adjacent to faced plot. */
			int iX = kAdj.getX();
			int iY = kAdj.getY();
			int iDelta = ::abs(iFacedX - iX) + ::abs(iFacedY - iY);
			if (iDelta <= 1)
				iValue += SyncRandNum(10000);
			/*  Prefer to stay/get out of foreign borders: AI patrols inside
				human borders are annoying */
			PlayerTypes const eAdjOwner = kAdj.getOwner();
			if (eAdjOwner != NO_PLAYER && eAdjOwner != getOwner() &&
				!isEnemy(TEAMID(eAdjOwner), kAdj))
			{
				iValue -= 4000;
			} // </advc.102>
		}
		if (iValue > iBestValue)
		{
			iBestValue = iValue;
			pBestPlot = &getPathEndTurnPlot();
			FAssert(!atPlot(pBestPlot));
		}
	}
	if (pBestPlot == NULL)
		return false;

	pushGroupMoveTo(*pBestPlot, NO_MOVEMENT_FLAGS, false, false, MISSIONAI_PATROL);
	return true;
}


bool CvUnitAI::AI_defend()
{
	PROFILE_FUNC();

	if (AI_defendPlot(plot()))
	{
		getGroup()->pushMission(MISSION_SKIP);
		return true;
	}

	CvPlot* pBestPlot = NULL;
	int iBestValue = 0;
	for (SquareIter it(*this, AI_searchRange(1), false); it.hasNext(); ++it)
	{
		CvPlot& p = *it;
		if (!AI_plotValid(p) || !AI_defendPlot(&p) || p.isVisibleEnemyUnit(this))
			continue;
		int iPathTurns;
		if (!generatePath(p, NO_MOVEMENT_FLAGS, true, &iPathTurns, 1))
			continue;
		/*if (iPathTurns != 1)
			continue;*/ // advc: redundant
		int iValue = 1 + SyncRandNum(10000);
		if (iValue > iBestValue)
		{
			iBestValue = iValue;
			pBestPlot = &p;
		}
	}

	if (pBestPlot == NULL)
		return false;

	// BETTER_BTS_AI_MOD, Unit AI, 12/06/08, jdog5000: START
	if (!pBestPlot->isCity() && getGroup()->getNumUnits() > 1)
	{	//getGroup()->AI_makeForceSeparate();
		joinGroup(NULL); // K-Mod. (AI_makeForceSeparate is a complete waste of time here.)
	} // BETTER_BTS_AI_MOD: END

	pushGroupMoveTo(*pBestPlot, NO_MOVEMENT_FLAGS, false, false, MISSIONAI_DEFEND);
	return true;
}

// This function has been edited for K-Mod
bool CvUnitAI::AI_safety()
{
	PROFILE_FUNC();

	CvPlot* pBestPlot = 0;
	int iBestValue = 0;
	bool bIgnoreDanger = false;
	// <advc.306>
	bool const bBarbarianSeaUnit = (isBarbarian() && getDomainType() == DOMAIN_SEA);
	int const iSearchTurns = (bBarbarianSeaUnit ? 3  : 1); // </advc.306>
	int const iSearchRange = AI_searchRange(iSearchTurns);
	bool const bEnemyTerritory = isEnemy(getPlot());
	//for (iPass = 0; iPass < 2; iPass++)
	do // K-Mod. What's the point of the first pass if it is just ignored? (see break condition at the end)
	{
		for (SquareIter it(*this, iSearchRange); it.hasNext(); ++it)
		{
			CvPlot& p = *it;
			if (!AI_plotValid(p) || p.isVisibleEnemyUnit(this))
				continue;
			int iPathTurns;
			if (!generatePath(p,
				bIgnoreDanger ? MOVE_IGNORE_DANGER : NO_MOVEMENT_FLAGS,
				true, &iPathTurns, iSearchTurns))
			{
				continue;
			}
			/*  <advc.306> Consider only unobserved plots (and cities) safe for
				Barbarian sea units. This should help them receive spawned cargo. */
			if (bBarbarianSeaUnit && p.isWater() && p.isVisibleToCivTeam())
				continue; // </advc.306>
			int iCount = 0;
			FOR_EACH_UNIT_IN(pLoopUnit, p)
			{
				if (pLoopUnit->getOwner() != getOwner() || !pLoopUnit->canDefend())
					continue;
				CvUnit const* pHeadUnit = pLoopUnit->getGroup()->getHeadUnit();
				FAssert(pHeadUnit != NULL);
				FAssert(getGroup()->getHeadUnit() == this);
				if (pHeadUnit != this)
				{
					if (pHeadUnit->isWaiting() || !pHeadUnit->canMove())
					{
						FAssert(pLoopUnit != this);
						FAssert(pHeadUnit != getGroup()->getHeadUnit());
						iCount++;
					}
				}
			}
			int iValue = iCount * 100;
			//iValue += p.defenseModifier(getTeam(), false);
			iValue += AI_plotDefense(&p); // advc.012
			// K-Mod
			if (bEnemyTerritory ? !isEnemy(p) : (p.getTeam() == getTeam()))
				iValue += 30;
			if (p.isValidRoute(this, /* advc.001i: */ false))
				iValue += 25; // K-Mod end
			if (at(p))
				iValue += 50;
			else iValue += SyncRandNum(50);
			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				pBestPlot = &p;
			}
		}
		// K-Mod
		if (pBestPlot == NULL)
		{
			if (bIgnoreDanger)
				break; // no suitable plot, even when ignoring danger
			else bIgnoreDanger = true; // try harder next time
		} // K-Mod end
	} while (pBestPlot == NULL);

	if (pBestPlot != NULL)
	{
		if (at(*pBestPlot))
		{
			getGroup()->pushMission(MISSION_SKIP);
			return true;
		}
		else
		{
			pushGroupMoveTo(*pBestPlot,
					bIgnoreDanger ? MOVE_IGNORE_DANGER : NO_MOVEMENT_FLAGS);
			return true;
		}
	}

	return false;
}


bool CvUnitAI::AI_hide()
{
	PROFILE_FUNC();

	if (getInvisibleType() == NO_INVISIBLE)
		return false;

	CvPlot* pBestPlot = NULL;
	int iBestValue = 0;
	for (SquareIter itPlot(*this, AI_searchRange(1)); itPlot.hasNext(); ++itPlot)
	{
		CvPlot& p = *itPlot;
		if (!AI_plotValid(p))
			continue;
		if (p.isVisibleEnemyUnit(this)) // advc.opt: Moved up
			continue;

		bool bValid = true;
		// advc.001: BtS hadn't excluded friendly teams
		for (TeamIter<ALIVE,KNOWN_POTENTIAL_ENEMY_OF> itTeam(getTeam());
			itTeam.hasNext(); ++itTeam)
		{
			if (p.isInvisibleVisible(itTeam->getID(), getInvisibleType()))
			{
				bValid = false;
				break;
			}
		}
		if (!bValid)
			continue;

		int iPathTurns;
		if (!generatePath(p, NO_MOVEMENT_FLAGS, true, &iPathTurns, 1))
			continue;
		if (iPathTurns > 1)
			continue;

		int iCount = 1;
		FOR_EACH_UNIT_IN(pLoopUnit, p)
		{
			// advc (tbd.): Should units of a teammate count as well?
			if (pLoopUnit->getOwner() != getOwner() || !pLoopUnit->canDefend())
				continue;
			CvUnit const* pHeadUnit = pLoopUnit->getGroup()->getHeadUnit();
			FAssert(pHeadUnit != NULL);
			FAssert(getGroup()->getHeadUnit() == this);
			if (pHeadUnit != this)
			{
				if (pHeadUnit->isWaiting() || !pHeadUnit->canMove())
				{
					FAssert(pLoopUnit != this);
					FAssert(pHeadUnit != getGroup()->getHeadUnit());
					iCount++;
				}
			}
		}
		int iValue = iCount * 100;
		//iValue += p.defenseModifier(getTeam(), false);
		iValue += AI_plotDefense(&p); // advc.012
		if (at(p))
			iValue += 50;
		else iValue += SyncRandNum(50);
		if (iValue > iBestValue)
		{
			iBestValue = iValue;
			pBestPlot = &p;
		}
	}

	if (pBestPlot != NULL)
	{
		if (at(*pBestPlot))
		{
			getGroup()->pushMission(MISSION_SKIP);
			return true;
		}
		else
		{
			pushGroupMoveTo(*pBestPlot);
			return true;
		}
	}

	return false;
}


bool CvUnitAI::AI_goody(int iRange)
{
	PROFILE_FUNC();

	if (isBarbarian() || isMinorCiv()) // rfc
		return false;

	CvPlot* pBestPlot = NULL;
	int iBestValue = 0;
	for (SquareIter it(*this, AI_searchRange(iRange), false); it.hasNext(); ++it)
	{
		CvPlot const& p =*it;
		if (/*!AI_plotValid(p)*/!AI_canEnterByLand(p.getArea())) // advc.opt
			continue;
		if (!p.isRevealedGoody(getTeam()) || p.isVisibleEnemyUnit(this))
			continue;
		int iPathTurns;
		if (!generatePath(p, NO_MOVEMENT_FLAGS, true, &iPathTurns, iRange))
			continue;
		if (iPathTurns > iRange)
			continue;

		int iValue = 1 + SyncRandNum(10000);
		iValue /= iPathTurns + 1;
		if (iValue > iBestValue)
		{
			iBestValue = iValue;
			pBestPlot = &getPathEndTurnPlot();
		}
	}

	if (pBestPlot != NULL)
	{
		pushGroupMoveTo(*pBestPlot);
		return true;
	}

	return false;
}


// advc.031d:
MovementFlags CvUnitAI::AI_exploreFlags() const
{
	MovementFlags eFlags = MOVE_NO_ENEMY_TERRITORY; // as in BtS
	if (currHitPoints() * 10 < maxHitPoints() * 7)
		return eFlags | MOVE_AVOID_DANGER;
	CvGame const& kGame = GC.getGame();
	/*	Would be better to let the pathfinder decide what units are dangerous,
		but that's harder to implement. */
	bool bAnimals = (kGame.getGameTurn() < kGame.getBarbarianStartTurn() &&
			!kGame.isOption(GAMEOPTION_NO_BARBARIANS) &&
			!kGame.isOption(GAMEOPTION_NO_ANIMALS));
	bool bExplore = (m_pUnitInfo->getDefaultUnitAIType() == UNITAI_EXPLORE);
	int iPower = m_pUnitInfo->getPowerValue();
	if (bExplore && !bAnimals && iPower <= 1)
		return eFlags | MOVE_AVOID_DANGER;
	if (isHuman())
	{	/*	Scouts on auto-explore always avoid danger,
			Warriors do when no animals are expected. */
		if (bExplore || (!bAnimals && iPower < 3))
			return eFlags | MOVE_AVOID_DANGER;
	}
	return eFlags;
}


bool CvUnitAI::AI_explore()
{
	PROFILE_FUNC();

	CvPlot const* pBestPlot = NULL;
	CvPlot const* pBestExplorePlot = NULL;

	bool bNoContact = (GC.getGame().countCivTeamsAlive() > GET_TEAM(getTeam()).getHasMetCivCount(true));
	const CvTeam& kTeam = GET_TEAM(getTeam()); // K-Mod
	bool bFirst = false; // advc.007
	CvMap const& kMap = GC.getMap();
	MovementFlags const eFlags = AI_exploreFlags(); // advc.031d
	int iBestValue = 0;
	for (int iI = 0; iI < kMap.numPlots(); iI++)
	{
		PROFILE("AI_explore 1");

		CvPlot const& kPlot = kMap.getPlotByIndex(iI);
		if (!AI_plotValid(kPlot))
			continue;

		int iValue = 0;

		if (kPlot.isRevealedGoody(getTeam()))
			iValue += 100000;

		if (iValue <= 0)
		{	// <advc.007> Stop these messages from polluting the MPLog
			int iRand = syncRand().get(4, bFirst ? "AI explore 1" : NULL);
			bFirst = false;
			if (iRand > 0) // </advc.007>
				continue;
		}

		if (!kPlot.isRevealed(getTeam()))
			iValue += 10000;

		FOR_EACH_ADJ_PLOT(kPlot)
		{
			PROFILE("AI_explore 2"); // XXX is this too slow?

			if (!pAdj->isRevealed(getTeam()))
				iValue += 1000;

			/*else if (bNoContact) {
				if (pAdj->getRevealedTeam(getTeam(), false) != pAdj->getTeam())
					iValue += 100;
			}*/ // BtS
			// K-Mod. Not only is the original code cheating, it also doesn't help us meet anyone!
			// The goal here is to try to meet teams which we have already seen through map trading.
			if (bNoContact &&
				// note: revealed owner can be set before the plot is actually revealed.
				pAdj->getRevealedOwner(kTeam.getID()) != NO_PLAYER)
			{
				if (!kTeam.isHasMet(pAdj->getRevealedTeam(kTeam.getID(), false)))
					iValue += 100;
			} // K-Mod end
		}

		if (iValue <= 0 || kPlot.isVisibleEnemyUnit(this) ||
			GET_PLAYER(getOwner()).AI_isAnyPlotTargetMissionAI(
			kPlot, MISSIONAI_EXPLORE, getGroup(), 3))
		{
			continue;
		}
		int iPathTurns;
		if (at(kPlot) || !generatePath(kPlot, eFlags, true, &iPathTurns))
			continue;

		iValue += SyncRandNum(250 *
				abs(kMap.xDistance(getX(), kPlot.getX())) +
				abs(kMap.yDistance(getY(), kPlot.getY())));

		if (kPlot.isAdjacentToLand())
			iValue += 10000;
		if (kPlot.isOwned())
			iValue += 5000;
		iValue /= 3 + std::max(1, iPathTurns);

		if (iValue > iBestValue)
		{
			iBestValue = iValue;
			pBestPlot = &(kPlot.isRevealedGoody(getTeam()) ?
					getPathEndTurnPlot() : kPlot);
			pBestExplorePlot = &kPlot;
		}
	}

	if (pBestPlot != NULL && pBestExplorePlot != NULL)
	{
		pushGroupMoveTo(*pBestPlot, eFlags, false, false,
				MISSIONAI_EXPLORE, pBestExplorePlot);
		return true;
	}

	return false;
}


bool CvUnitAI::AI_exploreRange(int iRange)
{
	PROFILE_FUNC();

	CvPlot* pBestPlot = NULL;
	int iBestValue = 0;
	CvPlot* pBestExplorePlot = NULL;

	bool const bAnyImpassable = GET_PLAYER(getOwner()).AI_isAnyImpassable(getUnitType());
	CvTeamAI const& kTeam = GET_TEAM(getTeam()); // K-Mod
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());
	CvMap const& kMap = GC.getMap();
	MovementFlags const eFlags = AI_exploreFlags(); // advc.031d
	int const iSearchRange = AI_searchRange(iRange);
	for (SquareIter it(*this, iSearchRange, false); it.hasNext(); ++it)
	{
		PROFILE("AI_exploreRange loop");

		CvPlot& p = *it;
		if (!AI_plotValid(p))
			continue;

		int iValue = 0;

		if (p.isRevealedGoody(getTeam()))
			iValue += 100000;
		// <advc.031d>
		int iNearestCityDist = GC.getMap().maxTypicalDistance();
		int iValFromCitySites = 0;
		for (int i = 0; i < kOwner.AI_getNumCitySites(); i++)
		{
			int iDist = kMap.plotDistance(&kOwner.AI_getCitySite(i), &p);
			iNearestCityDist = std::min(iNearestCityDist, iDist);
			iValFromCitySites += 1600 * std::max(0, 4 - iDist);
		} // </advc.031d>
		if (!p.isRevealed(getTeam()))
			iValue += 10000 /* advc.031d: */ + iValFromCitySites;
		// K-Mod. Try to meet teams that we have seen through map trading
		if (p.getRevealedOwner(kTeam.getID()) != NO_PLAYER &&
			!kTeam.isHasMet(p.getRevealedTeam(kTeam.getID(), false)))
		{
			iValue += 1000;
		} // K-Mod end

		FOR_EACH_ADJ_PLOT(p)
		{
			if (!pAdj->isRevealed(getTeam()))
				iValue += 1000;
		}

		if (iValue <= 0)
			continue;

		if (p.isVisibleEnemyUnit(this))
			continue;
		{
			PROFILE("AI_exploreRange AnyPlotTargetMissionAI");
			if (kOwner.AI_isAnyPlotTargetMissionAI(
				p, MISSIONAI_EXPLORE, getGroup(), 3))
			{
				continue;
			}
		}
		int iPathTurns;
		{
			PROFILE("AI_exploreRange Path");
			if (!generatePath(p, eFlags, true, &iPathTurns, iRange))
				continue;
			if (iPathTurns > iRange)
				continue;
		}
		iValue += SyncRandNum(10000);

		if (p.isAdjacentToLand())
			iValue += 10000;

		if (p.isOwned())
			iValue += 5000;
		// <advc.031d> Discourage roaming too far too early
		if (getDomainType() == DOMAIN_LAND &&
			getArea().getCitiesPerPlayer(getOwner()) > 0)
		{
			// City sites already done; not as good an anchor as actual cities.
			iNearestCityDist *= 2;
			int const iDistSoftCap = (3 * (kOwner.AI_getCurrEraFactor() + 2)).uround();
			if (iNearestCityDist > iDistSoftCap && iDistSoftCap < 15) // save time
			{
				FOR_EACH_CITY(pCity, kOwner)
				{
					iNearestCityDist = std::min(iNearestCityDist,
							kMap.plotDistance(pCity->plot(), &p));
					if (iNearestCityDist <= iDistSoftCap) // save time
						break;
				}
				if (iNearestCityDist > iDistSoftCap)
				{
					scaled rMult(iDistSoftCap, iNearestCityDist);
					rMult.exponentiate(fixp(0.5));
					iValue = (iValue * rMult).uround();
				}
			}
		} // </advc.031d>
		if (!isHuman() && AI_getUnitAIType() == UNITAI_EXPLORE_SEA && !bAnyImpassable)
		{
			// <advc.plotr>
			int const iDX = p.getX() - getX();
			int const iDY = p.getY() - getY(); // </advc.plotr>
			int iDirectionModifier = 100 +
					(50 * (abs(iDX) + abs(iDY))) / std::max(1, iSearchRange);
			if (GC.getGame().circumnavigationAvailable())
			{
				if (kMap.isWrapX())
				{
					if ((iDX * ((AI_getBirthmark() % 2 == 0) ? 1 : -1)) > 0)
						iDirectionModifier *= 150 + ((iDX * 100) / std::max(1, iSearchRange));
					else iDirectionModifier /= 2;
				}
				if (kMap.isWrapY())
				{
					if ((iDY * (((AI_getBirthmark() >> 1) % 2 == 0) ? 1 : -1)) > 0)
						iDirectionModifier *= 150 + ((iDY * 100) / std::max(1, iSearchRange));
					else iDirectionModifier /= 2;
				}
			}
			iValue *= iDirectionModifier;
			iValue /= 100;
		}
		/*	advc.pf: It's much better not to rely on the pathfinder for our
			immediate move. The pathfinder won't optimize exploration at all. */
		iValue /= iPathTurns + 1;
		if (iValue > iBestValue)
		{
			iBestValue = iValue;
			if (getDomainType() == DOMAIN_LAND)
				pBestPlot = &getPathEndTurnPlot();
			else pBestPlot = &p;
			pBestExplorePlot = &p;
		}
	}

	if (pBestPlot != NULL && pBestExplorePlot != NULL)
	{
		PROFILE("AI_exploreRange push");
		pushGroupMoveTo(*pBestPlot, eFlags, false, false,
				MISSIONAI_EXPLORE, pBestExplorePlot);
		return true;
	}

	return false;
}

// doc
// TODO: refactor
bool CvUnitAI::AI_exploreCoasts()
{
	if (!plot()->isAdjacentToLand())
		return false;

	int iPathLength;
	int iSearchRange = 4;
	int iBestValue = MAX_INT;
	CvPlot* pBestPlot = NULL;

	for (int iDX = -iSearchRange; iDX <= iSearchRange; iDX++)
	{
		for (int iDY = -iSearchRange; iDY <= iSearchRange; iDY++)
		{
			CvPlot* pLoopPlot = plotXY(getX(), getY(), iDX, iDY);

			if (pLoopPlot != NULL && !atPlot(pLoopPlot) && pLoopPlot->isAdjacentToLand() && !pLoopPlot->isRevealed(getTeam(), false) && generatePath(*pLoopPlot, MOVE_NO_ENEMY_TERRITORY, false, &iPathLength))
			{
				int iValue = 2 * iPathLength - (plot()->shareAdjacentArea(pLoopPlot) ? 1 : 0);
				if (iValue < iBestValue)
				{
					if (GET_PLAYER(getOwner()).AI_plotTargetMissionAIs(*pLoopPlot, MISSIONAI_EXPLORE, getGroup(), 3) == 0)
					{
						iBestValue = iValue;
						pBestPlot = pLoopPlot;
					}
				}
			}
		}
	}

	if (pBestPlot != NULL)
	{
		getGroup()->pushMission(MISSION_MOVE_TO, pBestPlot->getX(), pBestPlot->getY(), MOVE_NO_ENEMY_TERRITORY, false, false, MISSIONAI_EXPLORE);
		return true;
	}

	return false;
}


bool CvUnitAI::AI_exploreCircumnavigate()
{
	if (!GC.getGame().circumnavigationAvailable())
		return false;
	if (getUnitInfo().getTerrainImpassable(TERRAIN_OCEAN))
		return false;
	if (GET_PLAYER(getOwner()).AI().AI_areaMissionAIs(getArea(), MISSIONAI_CIRCUMNAVIGATE) > 1)
		return false;

    int iX;
    bool bAnyRevealed;
    int iBestValue;
    int iPathLength;
	CvPlot* pLoopPlot;
	CvPlot* pBestPlot;
	for (int iDX = 0; iDX < GC.getMap().getGridWidth(); iDX++)
	{
		iX = GC.getMap().dxWrap(getX() - iDX); // westward bias
		bAnyRevealed = false;

		for (int iY = 0; !bAnyRevealed && iY < GC.getMap().getGridHeight(); iY++)
		{
			if (GC.getMap().plot(iX, iY)->isRevealed(getTeam(), false))
				bAnyRevealed = true;
		}

        if (bAnyRevealed)
            continue;

		iBestValue = MAX_INT;
		pBestPlot = NULL;
		for (int iY = 0; iY < GC.getMap().getGridHeight(); iY++)
		{
			pLoopPlot = GC.getMap().plot(iX, iY);
            if (atPlot(pLoopPlot))
                continue;
            if (pLoopPlot->isRevealed(getTeam(), false))
                continue;
            if (!generatePath(*pLoopPlot, MOVE_NO_ENEMY_TERRITORY, false, &iPathLength))
                continue;

		    int iValue = GC.getMap().getGridHeight() * iPathLength + abs(getY() - iY);
		    if (iValue < iBestValue)
		    {
		        if (GET_PLAYER(getOwner()).AI_plotTargetMissionAIs(*pLoopPlot, MISSIONAI_EXPLORE, getGroup(), 3) == 0)
		        {
		            iBestValue = iValue;
		            pBestPlot = pLoopPlot;
		        }
		    }
		}

		if (pBestPlot != NULL)
		{
			getGroup()->pushMission(MISSION_MOVE_TO, pBestPlot->getX(), pBestPlot->getY(), MOVE_NO_ENEMY_TERRITORY, false, false, MISSIONAI_CIRCUMNAVIGATE);
			return true;
		}

		return false;
	}

	return false;
}

/*	BETTER_BTS_AI_MOD, 03/29/10, jdog5000 (War tactics AI, Efficiency):
	Returns target city. K-Mod: heavily edited */
CvCity* CvUnitAI::AI_pickTargetCity(MovementFlags eFlags, int iMaxPathTurns,
	bool bHuntBarbs,
	ListEnumMap<PlayerTypes, bool> abHuntPlayer)
{
	PROFILE_FUNC();

	CvCity* pBestCity = NULL;
	int iBestValue = 0;
	CvTeamAI const& kOurTeam = GET_TEAM(getTeam()); // advc
	// K-Mod
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());
	int iOurOffence = -1; // We calculate this for the first city only.
	CvUnit* pBestTransport = NULL;
	/*	iLoadTurns < 0 implies we should look for a transport;
		otherwise, it is the number of turns to reach the transport.
		Also, we only consider using transports if we aren't in enemy territory. */
	int iLoadTurns = (isEnemy(getPlot()) ? MAX_INT : -1);
	//GroupPathFinder transportPath;
	GroupPathFinder& kTransportPath = CvSelectionGroup::getClearPathFinder(); // advc.opt
	// K-Mod end

	CvCity* pTargetCity =  // advc.300:
			(isBarbarian() && getArea().getCitiesPerPlayer(BARBARIAN_PLAYER) <= 0 ? NULL :
			getArea().AI_getTargetCity(getOwner()));

	for (int i = 0; i < MAX_CIV_PLAYERS; i++) // doc: always consider barbarians
	{
		CvPlayer const& kTargetPlayer = GET_PLAYER((PlayerTypes)i);
		if (!kTargetPlayer.isAlive() ||
			!kOurTeam.AI_mayAttack(kTargetPlayer.getTeam()))
		{
			continue;
		}
        // doc: target minors
        if (kTargetPlayer.isMinorCiv() && !abHuntPlayer[kTargetPlayer.getID()])
            continue;
		FOR_EACH_CITY_VAR(pLoopCity, kTargetPlayer)
		{
			if (!pLoopCity->isArea(getArea()))
				//|| !AI_plotValid(pLoopCity->plot()) // advc.opt: area check suffices
			{
				continue;
			}
			if (!AI_mayAttack(kTargetPlayer.getTeam(), pLoopCity->getPlot()))
				continue;
            // doc: barbarian conditions
            if (pLoopCity->isBarbarian())
            {
                if (!bHuntBarbs && pLoopCity->getExpansion() != getOwner())
                    continue;
            }
            // doc: minor civ conditions
            if (pLoopCity->isMinorCiv())
            {
                if (!abHuntPlayer.get(pLoopCity->getOwner()) && pLoopCity->getExpansion() != getOwner())
                    continue;
                if (!AI_isTargetableCity(pLoopCity))
                    continue;
            }
			if (kOwner.AI_deduceCitySite(*pLoopCity))
			{
				// K-Mod. Look for either a direct land path, or a sea transport path.
				int iPathTurns = MAX_INT;
				bool const bLandPath = generatePath(pLoopCity->getPlot(), eFlags, true,
						&iPathTurns, iMaxPathTurns);
				if (pLoopCity->isCoastal() && (pBestTransport != NULL || iLoadTurns < 0))
				{
					// add a random bias in favour of land paths, so that not all stacks try to use boats.
					//int iLandBias =AI_getBirthmark()%6 +(AI_getBirthmark() % (bLandPath ? 3 : 6) ? 6 : 1);
					/*	<advc.001> I guess the intention is to roll a 6-sided die
						(birthmark%6 plus at least 1 in the end) with another 5 added for
						some portion of units - depending on whether there is a land path. */
					int iLandBias = (AI_getBirthmark() % 6) + 1;
					/*	Now, should 2 in 3 units have increased land bias
						when there is a land path and otherwise 5 in 6?
						You'd think that there should be more land bias
						when there is a land path. So I'm going to flip the condition,
						i.e. 1 in 3 units have increased land bias
						when there is a land path and otherwise 1 in 6. */
					if ((AI_getBirthmark() % (bLandPath ? 3 : 6)) == 0)
						iLandBias += 5;
					/*  (I also wonder if such randomization would fit better near the
						"we have to walk" comment in AI_attackCityMove. AI_pickTargetCity
						only decides which units target which city, not how they
						ultimately move there.) */ // </advc.001>
					if (pBestTransport != NULL && iPathTurns > iLandBias + 2)
					{
						pBestTransport = AI_findTransport(UNITAI_ASSAULT_SEA, eFlags,
								std::min(iMaxPathTurns, iPathTurns));
						if (pBestTransport != NULL)
						{
							generatePath(pBestTransport->getPlot(), eFlags, true, &iLoadTurns);
							FAssert(iLoadTurns > 0 && iLoadTurns < MAX_INT);
							iLoadTurns += iLandBias;
							FAssert(iLoadTurns > 0);
						}
						// just to indicate the we shouldn't look for a transport again.
						else iLoadTurns = MAX_INT;
					}
					int iMaxTransportTurns = std::min(iMaxPathTurns, iPathTurns) - iLoadTurns;
					if (pBestTransport != NULL && iMaxTransportTurns > 0)
					{
						kTransportPath.setGroup(*pBestTransport->getGroup(),
								eFlags & MOVE_DECLARE_WAR, iMaxTransportTurns,
								GC.getMOVE_DENOMINATOR());
						if (kTransportPath.generatePath(pLoopCity->getPlot()))
						{
							// faster by boat
							FAssert(kTransportPath.getPathTurns() + iLoadTurns <= iPathTurns);
							iPathTurns = kTransportPath.getPathTurns() + iLoadTurns;
						}
					}
				}

				if (iPathTurns >= iMaxPathTurns)
					continue;
				/*	If city is visible and our force already in position
					is dominantly powerful or we have a huge force
					already on the way, pick a different target */
				int iEnemyDefence = -1; // used later.
				int iOffenceEnRoute = kOwner.AI_cityTargetStrengthByPath(
						pLoopCity, getGroup(), iPathTurns);
				if (pLoopCity->isVisible(kOurTeam.getID()))
				{
					iEnemyDefence = kOwner.AI_localDefenceStrength(
							pLoopCity->plot(), NO_TEAM, DOMAIN_LAND,
							/*	advc.001: Probably a remnant of bDefensiveBonuses=true
								in BBAI's AI_getEnemyPlotStrength. */
							//true,
							iPathTurns > 1 ? 2 : 0);
					if (iPathTurns > 2)
					{
						int iAttackRatio = ((GC.getMAX_CITY_DEFENSE_DAMAGE() -
								pLoopCity->getDefenseDamage()) *
								GC.getDefineINT(CvGlobals::BBAI_SKIP_BOMBARD_BASE_STACK_RATIO) +
								pLoopCity->getDefenseDamage() *
								GC.getDefineINT(CvGlobals::BBAI_SKIP_BOMBARD_MIN_STACK_RATIO)) /
								std::max(1, GC.getMAX_CITY_DEFENSE_DAMAGE());
						if (100 * iOffenceEnRoute > iAttackRatio * iEnemyDefence)
							continue;
					}
				}
				if (iOurOffence == -1)
				{
					/*  note: with bCheckCanAttack=false, AI_sumStrength should be
						roughly the same regardless of which city we are targeting.
						... except if lots of our units have a hills-attack promotion
						or something like that. */
					iOurOffence = AI_getGroup()->AI_sumStrength(pLoopCity->plot());
				}
				FAssert(iOurOffence > 0);
				int iTotalOffence = iOurOffence + iOffenceEnRoute;

				int iValue = 0;
				if (AI_getUnitAIType() == UNITAI_ATTACK_CITY) //lemming?
					iValue = kOwner.AI_targetCityValue(*pLoopCity, false, false);
				else iValue = kOwner.AI_targetCityValue(*pLoopCity, true, true);
				// adjust value based on defensive bonuses
				{
					int iMod = std::min(8, AI_getGroup()->AI_getBombardTurns(pLoopCity)) *
							pLoopCity->getDefenseModifier(false) / 8
							+ (pLoopCity->getPlot().isHills() ?
							GC.getDefineINT(CvGlobals::HILLS_EXTRA_DEFENSE) : 0);
					iValue *= std::max(25, 125 - iMod);
					iValue /= 25; // the denominator is arbitrary, and unimportant.
					/*  note: the value reduction from high defences
						which are bombardable should not be more than
						the value reduction from simply having higher iPathTurns. */
				}
				// prefer cities which are close to the main target.
				if (pLoopCity == pTargetCity)
					iValue *= 2;
				else if (pTargetCity != NULL)
				{
					int iStepsFromTarget = stepDistance(pLoopCity->getX(), pLoopCity->getY(),
							pTargetCity->getX(), pTargetCity->getY());
					iValue *= 124 - 2 * std::min(12, iStepsFromTarget);
					iValue /= 100;
				}
				if (getArea().getAreaAIType(kOurTeam.getID()) == AREAAI_DEFENSIVE)
				{
					iValue *= 100 + pLoopCity->calculateCulturePercent(getOwner()); // was 50
					iValue /= 125; // was 50 (unimportant)
				}
				/*  boost value if we can see that the city is poorly defended,
					or if our existing armies need help there */
				if (pLoopCity->isVisible(kOurTeam.getID()) && iPathTurns < 6)
				{
					FAssert(iEnemyDefence != -1);
					if (iOffenceEnRoute * 3 > iEnemyDefence && iOffenceEnRoute < iEnemyDefence)
					{
						iValue *= 100 + (9 * iTotalOffence > 10 * iEnemyDefence ? 30 : 15);
						iValue /= 100;
					}
					else if (iOurOffence > iEnemyDefence)
					{
						// don't boost it by too much, otherwise human players will exploit us. :(
						int iCap = 100 + 100 * (6 - iPathTurns) / 5;
						iValue *= std::min(iCap, 100 * iOurOffence / std::max(1, iEnemyDefence));
						iValue /= 100;
						/*	an additional bonus if we're already adjacent
							(we can afford to be generous with this bonus,
							because the enemy has no time to bring in reinforcements) */
						if (iPathTurns <= 1)
						{
							iValue *= std::min(300, 150 * iOurOffence / std::max(1, iEnemyDefence));
							iValue /= 100;
						}
					}
				}
				/*	Reduce the value if we can see, or remember,
					that the city is well defended.
					Note. This adjustment can be more heavy-handed
					because it is harder to feign strong defence than weak defence.
					advc (note): Barbarians are never dissuaded (no strength memory). */
				iEnemyDefence = kOurTeam.AI_strengthMemory().get(pLoopCity->getPlot());
				if (iEnemyDefence > iTotalOffence)
				{
					/*	a more sensitive adjustment than usual
						(w/ modifier on the denominator),
						so as not to be too deterred before bombarding. */
					iEnemyDefence *= 130;
					iEnemyDefence /= 130 + (bombardRate() > 0 ? pLoopCity->getDefenseModifier(false) : 0);
					WarPlanTypes eWarPlan = kOurTeam.AI_getWarPlan(pLoopCity->getTeam());
					/*	If we aren't fully committed to the war, then focus on
						taking easy cities - but try not to be completely predictable. */
					bool bCherryPick = (eWarPlan == WARPLAN_LIMITED ||
							eWarPlan == WARPLAN_PREPARING_LIMITED ||
							eWarPlan == WARPLAN_DOGPILE);
					bCherryPick = bCherryPick && (AI_unitBirthmarkHash(
							GC.getGame().getElapsedGameTurns() / 4) % 4 != 0);

					int iBase = (bCherryPick ? 100 : 110);
					/*	an uneven comparison, just in case we can get
						some air support or other help somehow. */
					if (100 * iEnemyDefence > iBase * iTotalOffence)
					{
						iValue *= bCherryPick ?
								std::max(20, (3 * iBase * iTotalOffence - iEnemyDefence) /
								(2 * iEnemyDefence)) :
								std::max(33, iBase * iTotalOffence / iEnemyDefence);
						iValue /= 100;
					}
				}
				/*	A const-random component, so that the AI
					doesn't always go for the same city. */
				iValue *= 80 + AI_unitPlotHash(pLoopCity->plot()) % 41;
				iValue /= 100;
				iValue *= 1000;
				// If city is minor civ, less interesting
				if (GET_PLAYER(pLoopCity->getOwner()).isMinorCiv() ||
					GET_PLAYER(pLoopCity->getOwner()).isBarbarian())
				{
					//iValue /= 2;
					iValue /= 3; // K-Mod
				}
				// If stack has poor bombard, direct towards lower defense cities
				//iPathTurns += std::min(12, getGroup()->getBombardTurns(pLoopCity)/4);
				//iPathTurns += bombardRate() > 0 ? std::min(5, getGroup()->getBombardTurns(pLoopCity)/3) : 0; // K-Mod
			    // (already taken into account.)

			    // doc: barbarians focus on their own region group
			    if (isBarbarian())
			    {
			        int iRegionGroup = CvPlot::getRegionGroupForRegion(getOriginalRegion());
			        if (pLoopCity->getRegionGroup() == iRegionGroup)
			            iValue *= 2;

			        // doc: Asian barbarians focus on China
			        if (iRegionGroup == REGION_GROUP_EAST_ASIA || iRegionGroup == REGION_GROUP_NORTH_ASIA)
			        {
			            if (pLoopCity->getRegionGroup() == REGION_GROUP_EAST_ASIA)
			                iValue *= 5;
			        }
			    }

				//iValue /= 8 + SQR(iPathTurns); // was 4+
                iValue /= 4 + (iPathTurns * iPathTurns) / 2; // rfc
				if (iValue > iBestValue)
				{
					iBestValue = iValue;
					pBestCity = pLoopCity;
				}
			} // end if revealed.
			/*	K-Mod. If no city in the area is revealed,
				then assume the AI is able to deduce the position of the closest city. */
			else if (iBestValue == 0 && !pLoopCity->isBarbarian() && (pBestCity == NULL ||
				stepDistance(getX(), getY(), pBestCity->getX(), pBestCity->getY()) >
				stepDistance(getX(), getY(), pLoopCity->getX(), pLoopCity->getY())))
			{
				if (generatePath(pLoopCity->getPlot(), eFlags, true, 0, iMaxPathTurns))
					pBestCity = pLoopCity;
			}
			// K-Mod end
		}
	}

	return pBestCity;
}

/*	BETTER_BTS_AI_MOD, 03/29/10, jdog5000 (War tactics AI, Efficiency):
	(K-Mod has apparently merged BBAI's AI_goToTargetBarbCity into this) */
bool CvUnitAI::AI_goToTargetCity(MovementFlags eFlags,  // advc: some refactoring
	int iMaxPathTurns, CvCity* pTargetCity)
{
	PROFILE_FUNC();

	if (pTargetCity == NULL)
		pTargetCity = AI_pickTargetCity(eFlags, iMaxPathTurns);
	if (pTargetCity == NULL)
		return false;
	FAssert(pTargetCity->isArea(getArea())); // advc: This function isn't for naval assault

	CvPlot* pEndTurnPlot = NULL; // K-Mod
	CvPlot* pBestPlot = NULL;
	if (!(eFlags & MOVE_THROUGH_ENEMY))
	{
		int iBestValue = 0;
		FOR_EACH_ADJ_PLOT_VAR(pTargetCity->getPlot())
		{
			if (//!AI_plotValid(pAdjacentPlot)
				!isArea(pAdj->getArea())) // advc.opt
			{
				continue;
			}
			// K-Mod TODO: consider fighting for the best plot.
			// <advc.083> For a start, let's check for EnemyDefender instead of EnemyUnit.
			if (pAdj->isVisibleEnemyDefender(this) &&
				/*  Make sure that Barbarians can't be staved off by surrounding
					cities with units. AI civs don't seem to have that problem. */
				!isBarbarian())
			{
				continue; // </advc.083>
			}
			int iPathTurns;
			if (!generatePath(*pAdj, eFlags, true, &iPathTurns, iMaxPathTurns))
				continue;
			if(iPathTurns <= iMaxPathTurns &&
				/*  advc.083: This was previously asserted after the loop ("no suicide missions...")
					but not actually guaranteed by the loop. If the pathfinder thinks
					that it's OK to move through the city, then we might as well
					pick a suboptimal (but nearby) plot to attack from. */
				!pTargetCity->at(getPathEndTurnPlot()))
			{
				int iValue = std::max(0, 100 +
						//pAdjacentPlot->defenseModifier(getTeam(), false)
						AI_plotDefense(pAdj)); // advc.012
				if (!pAdj->isRiverCrossing(
					directionXY(*pAdj, pTargetCity->getPlot())))
				{
					iValue += (-12 * GC.getDefineINT(CvGlobals::RIVER_ATTACK_MODIFIER));
				}
				if (!isEnemy(*pAdj))
					iValue += 100;
				if (at(*pAdj))
					iValue += 50;
				iValue = std::max(1, iValue);
				iValue *= 1000;
				iValue /= iPathTurns + 1;
				if (iValue > iBestValue)
				{
					iBestValue = iValue;
					//pBestPlot = &getPathEndTurnPlot();
					// K-Mod
					pBestPlot = pAdj;
					pEndTurnPlot = &getPathEndTurnPlot();
					// K-Mod end
				}
			}
		}
	}
	else
	{
		pBestPlot = &pTargetCity->getPlot();
		/*	K-Mod. As far as I know, nothing actually uses MOVE_THROUGH_ENEMY here..
			but that doesn't mean we should let the code be wrong. */
		int iPathTurns;
		if (!generatePath(*pBestPlot, eFlags, true, &iPathTurns, iMaxPathTurns) ||
				iPathTurns > iMaxPathTurns)
		{
			return false;
		}
		pEndTurnPlot = &getPathEndTurnPlot();
		// K-mod end
	}

	if (pBestPlot == NULL || at(*pEndTurnPlot))
		return false;

	/*  <advc.001t> Needed when called from AI_attackMove. Attack stacks aren't supposed
		to declare war, and they shouldn't move into enemy cities when war is imminent. */
	if(!(eFlags & MOVE_DECLARE_WAR) && GET_TEAM(getTeam()).
		AI_isSneakAttackReady(pTargetCity->getTeam()))
	{
		TeamTypes eBestPlotTeam = pBestPlot->getTeam();
		if(eBestPlotTeam != NO_TEAM && GET_TEAM(eBestPlotTeam).getMasterTeam() ==
			GET_TEAM(pTargetCity->getTeam()).getMasterTeam())
		{
			return false;
		}
	} // </advc.001t>

	//pushGroupMoveTo(*pBestPlot, eFlags);
	// K-Mod start
	if (AI_considerPathDOW(*pEndTurnPlot, eFlags))
	{	// <advc.163>
		if(!canMove())
			return true; // </advc.163>
		/*  regenerate the path, just in case we want to take a different route after the DOW
			(but don't bother recalculating the best destination)
			Note. if the best destination happens to be on the border,
			and has a stack of defenders on it, this will make us attack them.
			That's bad. I'll try to fix that in the future. */
		if (!generatePath(*pBestPlot, eFlags, false))
			return false;
		CvPlot* pEnemyPlot = pEndTurnPlot; // advc.001t
		pEndTurnPlot = &getPathEndTurnPlot();
		// <advc.139> Don't move through city that is about to be lost
		CvCityAI const* pPlotCity = pEndTurnPlot->AI_getPlotCity();
		if(pPlotCity != NULL && pPlotCity->AI_isEvacuating())
			return false; // </advc.139>
		// <advc.001t>
		if(!isEnemy(*pEndTurnPlot))
		{
			// This will trigger a few times in most games
			/*FAssertMsg(isEnemy(pEndTurnPlot->getTeam()),
				"Known issue: AI may change its mind about the path to the target city "
				"after declaring war; temporary fix: stick to the original path.");*/
			if(isEnemy(*pEnemyPlot))
				pEndTurnPlot = pEnemyPlot;
			else FAssert(isEnemy(pEnemyPlot->getTeam()));
			/*  If the else... assert fails, it's probably b/c the stack has multiple
				moves and there is an intermediate tile that requires a DoW. So this
				can be fine. Could check this through getPathFinder().GetEndNode()
				like it's done in AI_considerPathDOW -- tbd.? */
		} // </advc.001t>
	}
	pushGroupMoveTo(*pEndTurnPlot,
			// I'm going to use MISSIONAI_ASSAULT signal to our spies and other units that we're attacking this city.
			eFlags, false, false, MISSIONAI_ASSAULT, pTargetCity->plot());
	// K-Mod end
	return true;
}

bool CvUnitAI::AI_pillageAroundCity(CvCity* pTargetCity, int iBonusValueThreshold,
	MovementFlags eFlags, int iMaxPathTurns)
{
	PROFILE_FUNC();
	// K-Mod
	if (!isEnemy(pTargetCity->getTeam()) &&
		!AI_getGroup()->AI_isDeclareWar(pTargetCity->getPlot()))
	{
		return false;
	} // K-Mod end
	CvPlot* pBestPlot = NULL;
	CvPlot* pBestPillagePlot = NULL;
	int iBestValue = 0;
	for (CityPlotIter it(*pTargetCity); it.hasNext(); ++it)
	{
		CvPlot& kPlot = *it;
		if (/*AI_plotValid(kPlot)*/AI_canEnterByLand(kPlot.getArea()) && // advc.opt
			kPlot.getTeam() == pTargetCity->getTeam() && // advc.opt: Moved up
			!kPlot.isBarbarian() && AI_mayAttack(kPlot) &&
			canPillage(kPlot) && !kPlot.isVisibleEnemyUnit(this) &&
			!GET_PLAYER(getOwner()).AI_isAnyPlotTargetMissionAI(
			kPlot, MISSIONAI_PILLAGE, getGroup()))
		{
			int iPathTurns;
			if (generatePath(kPlot, eFlags, true, &iPathTurns, iMaxPathTurns))
			{
				if (getPathFinder().getFinalMoves() == 0)
					iPathTurns++;
				if (iPathTurns <= iMaxPathTurns)
				{
					int iValue = AI_pillageValue(kPlot, iBonusValueThreshold);
					// <advc.083> Don't use a big stack to pillage every road
					if (iValue <= getGroup()->getNumUnits() * 4)
						continue; // </advc.083>
					iValue *= (1000 + 30 *
							/*  advc.012: This seems to be about a single unit, so
								noDefensiveBonus should be checked.
								A hill bias might make sense b/c of Iron and Copper,
								but that's for AI_pillageValue to decide. */
							(noDefensiveBonus() ? 0 : AI_plotDefense(&kPlot)));
							//(pLoopPlot->defenseModifier(getTeam(),false));
							//iValue /= (iPathTurns + 1);
							iValue /= std::max(1, iPathTurns); // K-Mod

					/*	if not at war with this plot owner, then devalue plot
						if we are already inside this owner's borders
						(because declaring war will pop us some unknown distance away) */
					if (!isEnemy(kPlot) && getPlot().getTeam() == kPlot.getTeam())
						iValue /= 10;
					if (iValue > iBestValue)
					{
						iBestValue = iValue;
						pBestPlot = &getPathEndTurnPlot();
						pBestPillagePlot = &kPlot;
					}
				}
			}
		}
	}

	if (pBestPlot != NULL && pBestPillagePlot != NULL)
	{
		/*if (atPlot(pBestPillagePlot) && !isEnemy(pBestPillagePlot->getTeam())) {
			//getGroup()->groupDeclareWar(pBestPillagePlot, true);
			// rather than declare war, just find something else to do, since we may already be deep in enemy territory
			return false;
		}*/ // BtS - disabled by K-Mod. (also see new code at top.)
		// K-Mod
		FAssert(AI_getGroup()->AI_isDeclareWar(/* advc: */ *pBestPillagePlot));
		if (AI_considerPathDOW(*pBestPlot, eFlags))
		{	// <advc.163>
			if(!canMove())
				return true; // </advc.163>
			int iPathTurns;
			if (!generatePath(*pBestPillagePlot, eFlags, true, &iPathTurns))
				return false;
			pBestPlot = &getPathEndTurnPlot();
		} // K-Mod end
		if (at(*pBestPillagePlot))
		{
			/*	advc.083: K-Mod had turned this check into an assertion.
				Seems that it can fail in rare situations when passing through
				foreign borders while war is (becomes?) imminent, and then it's
				better to keep moving and delay the DoW. */
			if (isEnemy(*pBestPillagePlot))
			{
				getGroup()->pushMission(MISSION_PILLAGE, -1, -1, NO_MOVEMENT_FLAGS,
						false, false, MISSIONAI_PILLAGE, pBestPillagePlot);
				return true;
			}
		}
		else
		{
			pushGroupMoveTo(*pBestPlot, eFlags, false, false,
					MISSIONAI_PILLAGE, pBestPillagePlot);
			return true;
		}
	}

	return false;
}

// doc
bool CvUnitAI::AI_isTargetableCity(const CvCity* pCity) const
{
    if (getPlot().getArea().AI_getTargetCity(getOwner()) == pCity)
        return true;
    if (pCity->isMinorCiv() && pCity->getWarValue(getOwner()) == 0)
        return false;
    return true;
}

/*	This function has been completely rewritten (and greatly simplified) for K-Mod
	(previously revised by BBAI) */
bool CvUnitAI::AI_bombardCity()
{
	// check if we need to declare war before bombarding!
	FOR_EACH_ADJ_PLOT(getPlot())
	{
		if (!pAdj->isCity())
			continue;
		if (AI_considerDOW(*pAdj))
		{	// <advc.163>
			if(!canMove())
				return true; // </advc.163>
		}
		break; // assume there can only be one city adjacent to us
	}

	if (!canBombard(getPlot()))
		return false;

	CvCity* pBombardCity = bombardTarget(getPlot());
    if (!AI_isTargetableCity(pBombardCity)) // doc: avoid minor targets outside of war map
        return false;

	FAssert(pBombardCity != NULL);

	int const iAttackOdds = AI_getGroup()->AI_attackOdds(pBombardCity->plot(), true);
	int iBase = GC.getDefineINT(CvGlobals::BBAI_SKIP_BOMBARD_BASE_STACK_RATIO);
	int iMin = GC.getDefineINT(CvGlobals::BBAI_SKIP_BOMBARD_MIN_STACK_RATIO);
	int const iBombardTurns = AI_getGroup()->AI_getBombardTurns(pBombardCity);
	// <advc.004c>
	if(iBombardTurns <= 0)
		return false; // </advc.004c>
	iBase = (iBase * (GC.getMAX_CITY_DEFENSE_DAMAGE() - pBombardCity->getDefenseDamage()) +
			iMin * pBombardCity->getDefenseDamage()) /
			std::max(1, GC.getMAX_CITY_DEFENSE_DAMAGE());
	int iThreshold = (iBase * (100 - iAttackOdds) +
			(1 + iBombardTurns/2) * iMin * iAttackOdds) /
			(100 + (iBombardTurns/2) * iAttackOdds);
	int iComparison = AI_getGroup()->AI_compareStacks(pBombardCity->plot(), true);
	if (iComparison > iThreshold)
	{
		if (gUnitLogLevel > 2) logBBAI("      Stack skipping bombard of %S with compare %d, starting odds %d, bombard turns %d, threshold %d", pBombardCity->getName().GetCString(), iComparison, iAttackOdds, iBombardTurns, iThreshold);
		return false;
	}
	// <advc.004c>
	CvUnit* pBombardUnit = AI_getGroup()->AI_bestUnitForMission(MISSION_BOMBARD);
	if (pBombardUnit == NULL)
	{
		FErrorMsg("canBombard but no bombard unit found");
		return false;
	}
	// (Not sure if other types of groups would manage to reunite)
	if (AI_getUnitAIType() == UNITAI_ATTACK_CITY)
		pBombardUnit->joinGroup(NULL);
	pBombardUnit-> // </advc.004c>
			getGroup()->pushMission(MISSION_BOMBARD,
			/* <K-Mod> */ -1, -1, NO_MOVEMENT_FLAGS, false, false,
			MISSIONAI_ASSAULT, pBombardCity->plot()); // </K-Mod>
	return true;
}

// This function has been been heavily edited for K-Mod.
bool CvUnitAI::AI_cityAttack(int iRange, int iOddsThreshold,
	// advc (comment): No caller uses eFlags anymore (not since K-Mod 1.15)
	MovementFlags eFlags, bool bFollow)
{
	PROFILE_FUNC();

	FAssert(canMove());

	CvPlot* pBestPlot = NULL;
	int iBestValue = 0;
	bool const bDeclareWar = (eFlags & MOVE_DECLARE_WAR);
	for (SquareIter it(*this, bFollow ? 1 : AI_searchRange(iRange), false);
		it.hasNext(); ++it)
	{
		CvPlot& p = *it;
		//if (!AI_plotValid(p)) continue; // advc.opt
		if (p.isCity() && /* advc.opt: */ AI_canEnterByLand(p.getArea()) &&
			(bDeclareWar ? AI_mayAttack(p.getTeam(), p) : isEnemy(p)))
		{
			int iPathTurns;
			if ((bFollow ? canMoveOrAttackInto(p, bDeclareWar) :
				generatePath(p, eFlags, true, &iPathTurns, iRange)))
			{
			    // doc: protect from barbarians
			    if (isBarbarian() && p.isOwned())
			    {
			        if (p.isMinorCiv())
			            continue;
			        if (GC.getGame().getGameTurn() < GET_PLAYER(p.getOwner()).getInitialBirthTurn() + getTurns(20))
			            continue;
			    }

			    // doc: never attack independent cities outside of war map
			    if (p.isOwned() && p.isIndependent() && !isMinorCiv() && !isBarbarian())
			    {
			        if (iRange > 1 && p.getWarValue(getOwner()) == 0)
			            continue;
			    }

				int iValue = (!AI_isAnyEnemyDefender(p) ? 100 :
						AI_getGroup()->AI_getWeightedOdds(&p, true));
				if (iValue >= iOddsThreshold)
				{
					if (iValue > iBestValue)
					{
						iBestValue = iValue;
						pBestPlot = &(bFollow ? p : getPathEndTurnPlot());
					}
				}
			}
		}
	}

	if (pBestPlot != NULL)
	{
		FAssert(!at(*pBestPlot));
		// K-Mod
		if (AI_considerPathDOW(*pBestPlot, eFlags))
		{	// <advc.163>
			if(!canMove())
				return true; // </advc.163>
			// after DOW, we might not be able to get to our target this turn... but try anyway.
			if (!generatePath(*pBestPlot, eFlags, false))
				return false;
			if (bFollow && pBestPlot != &getPathEndTurnPlot())
				return false;
			pBestPlot = &getPathEndTurnPlot();
		}
		if (bFollow && !AI_isAnyEnemyDefender(*pBestPlot))
		{
			FAssert(pBestPlot->getPlotCity() != 0);
			// we need to ungroup this unit so that we can move into the city.
			joinGroup(NULL);
			bFollow = false;
		}
		// K-Mod end
		pushGroupMoveTo(*pBestPlot, eFlags | (bFollow ?
				MOVE_DIRECT_ATTACK | MOVE_SINGLE_ATTACK : NO_MOVEMENT_FLAGS));
		return true;
	}

	return false;
}

/*	This function has been been written for K-Mod.
	(it started getting messy, so I deleted most of the old code)
	bFollow implies AI_follow conditions - ie. not everyone in the group can move,
	and this unit might not be the group leader. */
bool CvUnitAI::AI_anyAttack(int iRange, int iOddsThreshold, MovementFlags eFlags,
	int iMinStack, bool bAllowCities, bool bFollow)
{
	PROFILE_FUNC();

	FAssert(canMove());

	if (AI_rangeAttack(iRange))
	{
		return true;
	}

	int const iSearchRange = (bFollow ? 1 : AI_searchRange(iRange));
	// <advc.128> Within this range, the AI is able see to units on hidden tiles.
	int const iSearchRangeRand = std::max(1,
			intdiv::round(iSearchRange * m_iSearchRangeRandPercent, 100)); // </advc.128>
	bool const bDeclareWar = (eFlags & MOVE_DECLARE_WAR);
	CvPlot* pBestPlot = NULL;
	int iBestOdds = iOddsThreshold - 1; // advc
	CvTeamAI const& kOurTeam = GET_TEAM(getTeam());
	for (SquareIter it(*this, iSearchRange, false); it.hasNext(); ++it)
	{
		CvPlot& p = *it;
		if (!AI_plotValid(p))
			continue;
		if (!bAllowCities && p.isCity())
			continue;
		// <advc.128>
		if (it.currStepDist() > iSearchRangeRand && !p.isVisible(getTeam()))
		{
			continue;
		} // </advc.128>
		if (bDeclareWar ? (!kOurTeam.AI_mayAttack(p) &&
			(!p.isCity() || !AI_mayAttack(p.getPlotCity()->getTeam(), p))) :
			(!p.isVisibleEnemyUnit(this) && !isEnemyCity(p)))
		{
			continue;
		}

		int iEnemyDefenders = (bDeclareWar ?
				AI_countEnemyDefenders(p) :
				p.getNumVisibleEnemyDefenders(this));
		// <advc.033>
		if (isAlwaysHostile(p))
		{
			std::pair<int,int> iiDefendersAll = AI_countPiracyTargets(p);
			if(iiDefendersAll.second <= 0)
				continue;
			iEnemyDefenders = iiDefendersAll.first;
		} // </advc.033>
		if (iEnemyDefenders < iMinStack)
			continue;
		// <advc.314> Give civ unit a chance to run away after bad hut outcome
		if (isBarbarian() && AI_getUnitAIType() == UNITAI_ATTACK &&
			p.getNumVisibleUnits(getOwner()) == 1 &&
			getGameTurnCreated() >= GC.getGame().getGameTurn() &&
			// Don't impede units produced in Barbarian cities
			getPlot().getOwner() != getOwner())
		{
			bool bValid = true;
			FOR_EACH_UNIT_IN(pEnemyUnit, p)
			{
				if (pEnemyUnit->isHurt()) // One attack is fair enough
				{
					bValid = false;
					break;
				}
			}
			if (!bValid)
				continue;
		} // </advc.314>
		if (bFollow ?
			getGroup()->canMoveOrAttackInto(p, bDeclareWar, true) :
			generatePath(p, eFlags, true, 0, iRange))
		{
			// 101 for cities, because that's a better thing to capture.
			int iOdds = (iEnemyDefenders == 0 ? (p.isCity() ? 101 : 100) :
					AI_getGroup()->AI_getWeightedOdds(&p, false));
			if (iOdds > iBestOdds)
			{
				/*	<advc.298> Non-lethal units should make random attacks only
					when there is a lethal unit nearby */
				bool bValid = true;
				if (combatLimit() < 100 && !bFollow && iEnemyDefenders > 0 &&
					&getPathEndTurnPlot() != &p)
				{
					bValid = false;
					// Look for a lethal attacker in our group
					FOR_EACH_UNIT_IN(pGroupUnit, *getGroup())
					{
						if (PUF_isLethal(pGroupUnit))
						{
							bValid = true;
							break;
						}
					}
					// Look for a lethal attacker near p
					TeamTypes const eOurTeam = getTeam();
					for (SquareIter itInner(p, std::min(it.currStepDist(), 2), false);
						!bValid && itInner.hasNext(); ++itInner)
					{
						if (itInner->plotCheck(PUF_isLethal, -1, -1,
							NO_PLAYER, eOurTeam) != NULL)
						{
							bValid = true;
						}
					}
				}
				if (bValid)
				{	// </advc.298>
					iBestOdds = iOdds;
					pBestPlot = &(bFollow ? p : getPathEndTurnPlot());
				}
			}
		}
	}

	if (pBestPlot == NULL)
		return false;

	FAssert(!at(*pBestPlot));
	// K-Mod
	if (AI_considerPathDOW(*pBestPlot, eFlags))
	{	// <advc.163>
		if(!canMove())
			return true; // </advc.163>
		/*	after DOW, we might not be able to get to our target this turn...
			but try anyway. */
		if (!generatePath(*pBestPlot, eFlags))
			return false;
		if (bFollow && pBestPlot != &getPathEndTurnPlot())
			return false;
		pBestPlot = &getPathEndTurnPlot();
	}
	if (bFollow && AI_isAnyEnemyDefender(*pBestPlot))
	{
		/*	we need to ungroup to capture the undefended unit / city.
			(because not everyone in our group can move) */
		joinGroup(NULL);
		bFollow = false;
	}
	// K-Mod end
	pushGroupMoveTo(*pBestPlot, eFlags | (bFollow ?
			MOVE_DIRECT_ATTACK | MOVE_SINGLE_ATTACK : NO_MOVEMENT_FLAGS));
	return true;
}


bool CvUnitAI::AI_rangeAttack(int iRange)
{
	PROFILE_FUNC();
	FAssert(canMove());
	if (!canRangeStrike())
		return false;

	CvPlot* pBestPlot = NULL;
	int iBestValue = 0;
	//int iSearchRange = AI_searchRange(iRange);
	/*  advc.rstr: MISSION_RANGE_ATTACK doesn't currently cause the unit to
		move toward the target. AI_searchRange and iRange are no help then. */
	for (SquareIter it(*this, airRange(), false);
		it.hasNext(); ++it)
	{
		CvPlot& kLoopPlot = *it;
		if (kLoopPlot.isVisibleEnemyUnit(this) /*|| // K-Mod: disabled
			(kLoopPlot.isCity() && AI_potentialEnemy(kLoopPlot.getTeam()))*/)
		{
			if (canRangeStrikeAt(plot(), kLoopPlot.getX(), kLoopPlot.getY()))
			{	//int iValue = AI_getGroup()->AI_attackOdds(&kLoopPlot, true);
				/*	advc.rstr: A bit better? Still pretty dumb to always shoot
					the softest target ... */
				int iValue = AI_getGroup()->AI_getWeightedOdds(&kLoopPlot, false);
				if (iValue > iBestValue)
				{
					iBestValue = iValue;
					pBestPlot = &kLoopPlot;
				}
			}
		}
	}
	if (pBestPlot != NULL)
	{
		// K-Mod note: no AI_considerDOW here.
		getGroup()->pushMission(MISSION_RANGE_ATTACK, pBestPlot->getX(), pBestPlot->getY());
		return true;
	}
	return false;
}

// (heavily edited for K-Mod)
bool CvUnitAI::AI_leaveAttack(int iRange, int iOddsThreshold, int iStrengthThreshold)
{
	FAssert(canMove());
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner()); // K-Mod
	// <advc.300>
	if (isBarbarian() && iOddsThreshold > 1)
		iOddsThreshold /= 2; // </advc.300>

	CvPlot* pBestPlot = NULL;
	int iBestValue = 0;
	CvCity const* pCity = getPlot().getPlotCity();
	if (pCity != NULL && pCity->getOwner() == getOwner())
	{
		/*int iOurStrength = GET_PLAYER(getOwner()).AI_getOurPlotStrength(plot(), 0, false, false);
		int iEnemyStrength = GET_PLAYER(getOwner()).AI_getEnemyPlotStrength(plot(), 2, false, false);*/
		// K-Mod
		int iOurDefence = kOwner.AI_localDefenceStrength(plot(), getTeam());
		int iEnemyStrength = kOwner.AI_localAttackStrength(plot(), NO_TEAM, DOMAIN_LAND, 2);
		// K-Mod end
		if (iEnemyStrength > 0)
		{
			if (iOurDefence * 100 / iEnemyStrength < iStrengthThreshold)
			{
				/*	K-Mod.
					We should only heed to the threshold if we
					either have enough defence to hold the city,
					or we don't have enough attack force to wipe the enemy out.
					(otherwise, we are better off attacking than defending.) */
				if (iEnemyStrength < iOurDefence ||
					kOwner.AI_localAttackStrength(
					plot(), getTeam(), DOMAIN_LAND, 0, false, false, true)
					< kOwner.AI_localDefenceStrength(
					plot(), NO_TEAM, DOMAIN_LAND, 2, false)) // K-Mod end
				{
					return false;
				}
			}
			if (getPlot().plotCount(PUF_canDefendGroupHead, -1, -1, getOwner(),
				NO_TEAM, PUF_isDomainType, DOMAIN_LAND) // advc.001s
				<= getGroup()->getNumUnits())
			{
				return false;
			}
		}
	}
	for (SquareIter it(*this, iRange, false); it.hasNext(); ++it)
	{
		CvPlot const& p = *it;
		if (/*!AI_plotValid(p)*/!isArea(p.getArea())) // advc.opt
			continue;

		/*if (p.isVisibleEnemyUnit(this) || (p.isCity() && AI_potentialEnemy(p.getTeam(), &p))) {
			if (p.getNumVisibleEnemyDefenders(this) > 0)*/ // BtS
		if (!p.isVisibleEnemyDefender(this)) // K-Mod
			continue;
		if (!generatePath(p, NO_MOVEMENT_FLAGS, true, 0, iRange))
			continue;
		/*	<advc.114f> Enter hostile territory only if we can attack straight away
			or if we'll have moves left for seeking safety */
		if (getPathFinder().getPathTurns() > 1 &&
			getPathFinder().getFinalMoves() <= 0)
		{
			if (p.isOwned() && GET_TEAM(p.getTeam()).isAtWar(getTeam()))
				continue;
			/*	Don't make multi-turn moves in non-hostile territory either
				if this is a non-lethal group. Can still damage them if and when
				they come closer. */
			bool bAnyLethal = false;
			FOR_EACH_UNIT_IN(pGroupUnit, *getGroup())
			{
				if (pGroupUnit->combatLimit() >= 100)
				{
					bAnyLethal = true;
					break;
				}
			}
			if (!bAnyLethal)
				continue;
		} // </advc.114f>
		//iValue = getGroup()->AI_attackOdds(&p, true);
		int iValue = AI_getGroup()->AI_getWeightedOdds(&p, false); // K-Mod
		//if (iValue >= AI_finalOddsThreshold(&p, iOddsThreshold))
		if (iValue >= iOddsThreshold && // K-Mod
			iValue > iBestValue)
		{
			iBestValue = iValue;
			pBestPlot = &getPathEndTurnPlot();
		}
	}

	if (pBestPlot != NULL)
	{
		// K-Mod note: no AI_considerDOW here.
		pushGroupMoveTo(*pBestPlot, NO_MOVEMENT_FLAGS, false, false,
				MISSIONAI_COUNTER_ATTACK);
		return true;
	}

	return false;
}

// K-Mod. Defend nearest city against invading attack stacks.
bool CvUnitAI::AI_defensiveCollateral(int iThreshold, int iSearchRange)
{
	PROFILE_FUNC();
	FAssert(collateralDamage() > 0);

	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());

	CvPlot const* pDefencePlot = NULL;
	//if (getPlot().isCity(false, getTeam()))
	// advc.001: Looks like karadoc misinterpreted the eForTeam parameter
	if (getPlot().isCity() && getPlot().getOwner() == getOwner())
		pDefencePlot = plot();
	else
	{
		int iClosest = MAX_INT;
		for (SquareIter it(*this, iSearchRange); it.hasNext(); ++it)
		{
			CvPlot const& p = *it;
			//if (p.isCity(false, getTeam()))
			// advc.001: (see comment above)
			if (p.isCity() && p.getOwner() == getOwner())
			{
				if (kOwner.AI_isAnyPlotDanger(p))
				{
					pDefencePlot = &p;
					break;
				}
				int iDist = it.currStepDist();
				if (iDist < iClosest)
				{
					iClosest = iDist;
					pDefencePlot = &p;
				}
			}
		}
	}

	if (pDefencePlot == NULL)
		return false;

	int const iEnemyAttack = kOwner.AI_localAttackStrength(pDefencePlot, NO_TEAM,
			getDomainType(), iSearchRange);
	int const iOurDefence = kOwner.AI_localDefenceStrength(pDefencePlot, getTeam(),
			getDomainType(), 0);
	bool const bDanger = (iEnemyAttack > iOurDefence);

	CvPlot* pBestPlot = NULL; // advc (note): Maximizing iThreshold
	for (SquareIter it(*this, iSearchRange, false); it.hasNext(); ++it)
	{
		CvPlot const& p = *it;
		if (/*!AI_plotValid(p)*/ !isArea(p.getArea())) // advc.opt
			continue;
		int const iEnemies = p.getNumVisibleEnemyDefenders(this);
		int iPathTurns;
		if (iEnemies > 0 && generatePath(p, NO_MOVEMENT_FLAGS, true, &iPathTurns, 1))
		{
			//int iValue = getGroup()->AI_attackOdds(pLoopPlot, false);
			int iValue = AI_getGroup()->AI_getWeightedOdds(&p);
			if (iValue > 0 && iEnemies >= std::min(4, collateralDamageMaxUnits()))
			{
				int iOurAttack = kOwner.AI_localAttackStrength(&p, getTeam(),
						getDomainType(), iSearchRange, true, true, true);
				int iEnemyDefence = kOwner.AI_localDefenceStrength(&p, NO_TEAM,
						getDomainType(), 0);
				iValue += std::max(0, (bDanger ? 75 : 45) * (3 * iOurAttack - iEnemyDefence) /
						std::max(1, 3*iEnemyDefence));
				// note: the scale is choosen to be around +50% when attack == defence, while in danger.
				if (bDanger && it.currStepDist() <= 1)
				{
					// enemy is ready to attack, and strong enough to win. We might as well hit them.
					iValue += 20;
				}
			}
			if (iValue >= iThreshold)
			{
				iThreshold = iValue;
				pBestPlot = &getPathEndTurnPlot();
			}
		}
	}

	if (pBestPlot != NULL)
	{
		pushGroupMoveTo(*pBestPlot);
		return true;
	}

	return false;
}

// advc.139:
bool CvUnitAI::AI_evacuateCity()
{
	if(!getPlot().AI_getPlotCity()->AI_isEvacuating())
		return false;
	scaled rEvacProb = 1;
	/*  Units that don't receive def. modifiers should always evacuate.
		AI_defensiveCollateral can still happen, but not when the threat ratio is
		this high. */
	if (getUnitInfo().getCombat() > 0 && !getUnitInfo().isNoDefensiveBonus())
	{
		rEvacProb = fixp(0.8);
		rEvacProb -= scaled(currHitPoints(), std::max(1, maxHitPoints()));
		int iDefenseMod = fortifyModifier() +
				getPlot().defenseModifier(getTeam(),
				GC.getGame().getCurrentEra() >= CvEraInfo::AI_getAgeOfGuns()) +
				cityDefenseModifier() +
				(getPlot().isHills() ? hillsDefenseModifier() : 0);
		if (AI_getUnitAIType() == UNITAI_CITY_DEFENSE)
			iDefenseMod = std::max(iDefenseMod, 100);
		rEvacProb -= per100(iDefenseMod);
		/*	Don't leave too many units behind. 3 or 4 can be a headache for
			enemy siege units, 6 or 7 are too many to sacrifice. */
		if (rEvacProb < 1)
		{
			int iStayingBehind = 0;
			FOR_EACH_UNIT_IN(pLoopUnit, getPlot())
			{
				CvSelectionGroup const& kGroup = *pLoopUnit->getGroup();
				if (&kGroup == getGroup())
					continue;
				if (!kGroup.isForceUpdate()) // i.e. if AI_update already called
					iStayingBehind++;
			}
			if (iStayingBehind > 2)
				rEvacProb += scaled(iStayingBehind + getGroup()->getNumUnits() - 3, 6);
		}
	}
	/*  retreatToCity isn't perfect for this; selects the city based on plot danger.
		Hopefully sufficient most of the time. */
	if (SyncRandSuccess(rEvacProb))
		return AI_retreatToCity();
	return false;
}


// K-Mod.
/*	bLocal is just to help with the efficiency of this function for short-range checks.
	It means that we should look only in nearby plots.
	the default (bLocal == false) is to look at every plot on the map! */
bool CvUnitAI::AI_defendTerritory(int iThreshold, MovementFlags eFlags,
	int iMaxPathTurns, bool bLocal)
{
	PROFILE_FUNC();

	const CvPlayerAI& kOwner = GET_PLAYER(getOwner());

	CvPlot* pEndTurnPlot = NULL;
	int iBestValue = 0;

	//for (int iI = 0; iI < GC.getMap().numPlots(); iI++)
	// I'm going to use a loop equivalent to the above when !bLocal; and a loop in a square around our unit if bLocal.
	int i = 0;
	int iRange = bLocal ? AI_searchRange(iMaxPathTurns) : 0;
	int iPlots = bLocal ? (2*iRange+1)*(2*iRange+1) : GC.getMap().numPlots();
	if (bLocal && iPlots >= GC.getMap().numPlots())
	{
		bLocal = false;
		iRange = 0;
		iPlots = GC.getMap().numPlots();
		// otherwise it's just silly.
	}
	FAssert(!bLocal || iRange > 0);
	TeamTypes const eTeam = getTeam(); // advc.opt
	while (i < iPlots)
	{
		CvPlot* pLoopPlot = (bLocal
			? plotXY(getX(), getY(), -iRange + i % (2*iRange+1), -iRange + i / (2*iRange+1))
			: GC.getMap().plotByIndex(i));
		i++; // for next cycle.

		if (pLoopPlot == NULL || pLoopPlot->getTeam() != eTeam ||
			!AI_plotValid(pLoopPlot) || !pLoopPlot->isVisibleEnemyUnit(this))
		{
			continue;
		}
		// <advc.033>
		if (isAlwaysHostile(*pLoopPlot) && !AI_isAnyPiracyTarget(*pLoopPlot))
			continue;
		/*  This doesn't guarantee that the best defender will be a PiracyTarget,
			but at least we're going to attack a unit that is hanging out
			with a target. */ // </advc.033>
		int iPathTurns;
		if (generatePath(*pLoopPlot, eFlags, true, &iPathTurns, iMaxPathTurns))
		{
			int iOdds = AI_getGroup()->AI_getWeightedOdds(pLoopPlot);
			int iValue = iOdds;
			if (iOdds > 0 && iOdds < 100 && iThreshold > 0)
			{
				int iOurAttack = kOwner.AI_localAttackStrength(pLoopPlot, eTeam,
						getDomainType(), 2, true, true, true);
				int iEnemyDefence = kOwner.AI_localDefenceStrength(pLoopPlot, NO_TEAM,
						getDomainType(), 0);
				if (iOurAttack > iEnemyDefence && iEnemyDefence > 0)
				{
					/*int iBonus = 100 - iOdds;
					iBonus -= iBonus * 4*iBonus / (4*iBonus + 100*(iOurAttack-iEnemyDefence)/iEnemyDefence);
					FAssert(iBonus >= 0 && iBonus <= 100 - iOdds);
					iValue += iBonus;*/
					iValue += 100 * (iOdds + 15) * (iOurAttack - iEnemyDefence)/
							((iThreshold + 100) * iEnemyDefence);
				}
			}
			if (iValue >= iThreshold)
			{
				BonusTypes eBonus = pLoopPlot->getNonObsoleteBonusType(eTeam);
				iValue *= 100 + (eBonus == NO_BONUS ? 0 :
						3*kOwner.AI_bonusVal(eBonus, 0)/2) +
						(pLoopPlot->getWorkingCity() ? 20 : 0);

				if (pLoopPlot->getOwner() != getOwner())
					iValue = 2*iValue/3;

				if (iPathTurns > 1)
					iValue /= iPathTurns + 2;

				if (iOdds >= iThreshold)
					iValue = 4*iValue/3;

				if (iValue > iBestValue)
				{
					iBestValue = iValue;
					pEndTurnPlot = &getPathEndTurnPlot();
				}
			}
		}
	}

	if (pEndTurnPlot != NULL)
	{
		pushGroupMoveTo(*pEndTurnPlot, eFlags, false, false, MISSIONAI_DEFEND);
		return true;
	}

	return false;
}

/*	iAttackThreshold is the minimum ratio for
	our attack / their defence.
	iRiskThreshold is the minimum ratio for
	their attack / our defence adjusted for stack size
	note: iSearchRange is /not/ the number of turns.
	It is the number of steps. iSearchRange < 1 means 'automatic'
	Only 1-turn moves are considered here. */
bool CvUnitAI::AI_stackVsStack(int iSearchRange, int iAttackThreshold, int iRiskThreshold,
	MovementFlags eFlags)
{
	PROFILE_FUNC();

	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());

	//int iOurDefence = kOwner.AI_localDefenceStrength(plot(), getTeam());
	int const iOurDefence = AI_getGroup()->AI_sumStrength(NULL); // not counting defensive bonuses

	CvPlot* pBestPlot = NULL;
	int iBestValue = 0;
	for (SquareIter it(*this, iSearchRange < 1 ? AI_searchRange(1) : iSearchRange, false);
		it.hasNext(); ++it)
	{
		CvPlot& p = *it;
		if (!AI_plotValid(p))
			continue;
		int iEnemies = p.getNumVisibleEnemyDefenders(this);
		int iPathTurns;
		if (iEnemies > 0 && generatePath(p, eFlags, true, &iPathTurns, 1))
		{
			int iEnemyAttack = kOwner.AI_localAttackStrength(&p, NO_TEAM,
					getDomainType(), 0, false);
			int iRiskRatio = 100 * iEnemyAttack / std::max(1, iOurDefence);
			// adjust risk ratio based on the relative numbers of units.
			iRiskRatio *= 50 + 50 * (getGroup()->getNumUnits()+3) /
					std::min(iEnemies+3, getGroup()->getNumUnits()+3);
			iRiskRatio /= 100;
			//
			if (iRiskRatio < iRiskThreshold)
				continue;

			int iAttackRatio = AI_getGroup()->AI_compareStacks(&p, true);
			if (iAttackRatio < iAttackThreshold)
				continue;

			int iValue = iAttackRatio * iRiskRatio;
			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				pBestPlot = &p;
				FAssert(pBestPlot == &getPathEndTurnPlot());
			}
		}
	}

	if (pBestPlot != NULL)
	{
		if (gUnitLogLevel >= 2) logBBAI("    Stack for player %d (%S) uses StackVsStack attack with value %d", getOwner(), GET_PLAYER(getOwner()).getCivilizationDescription(0), iBestValue);
		pushGroupMoveTo(*pBestPlot, eFlags, false, false,
				MISSIONAI_COUNTER_ATTACK, pBestPlot);
		return true;
	}

	return false;
} // K-Mod end


bool CvUnitAI::AI_blockade()
{
	PROFILE_FUNC(); /* advc (note): To speed it up, one could go through
			PlayerIter -> FOR_EACH_CITY -> WorkablePlotIter. But seems like a nonissue anyway. */
	int iBestValue = 0;
	CvPlot const* pBestPlot = NULL;
	CvPlot const* pBestBlockadePlot = NULL;
	MovementFlags eFlags = MOVE_DECLARE_WAR; // K-Mod
	for (int i = 0; i < GC.getMap().numPlots(); i++)
	{
		CvPlot const& kPlot = GC.getMap().getPlotByIndex(i);
		if (!AI_plotValid(kPlot))
			continue;
		CvCity* pCity = kPlot.getWorkingCity();
		if (pCity == NULL || pCity->isBarbarian() || !pCity->isCoastal())
			continue;
		if (!AI_mayAttack(kPlot)) // advc.opt: Moved down
			continue;
		if (kPlot.isVisibleEnemyUnit(this) || !canPlunder(kPlot))
			continue;
		if (GET_PLAYER(getOwner()).AI_isAnyPlotTargetMissionAI(
			kPlot, MISSIONAI_BLOCKADE, getGroup(), 2))
		{
			continue;
		}
		int iPathTurns;
		if (!generatePath(kPlot, eFlags, true, &iPathTurns))
			continue;
		FAssert(isEnemy(pCity->getTeam()) || GET_TEAM(getTeam()).AI_getWarPlan(
				GET_TEAM(pCity->getTeam()).getMasterTeam()) != NO_WARPLAN); // advc.104j

		int iValue = 1;
		iValue += std::min(pCity->getPopulation(), pCity->countNumWaterPlots());
		iValue += GET_PLAYER(getOwner()).AI_adjacentPotentialAttackers(pCity->getPlot());
		iValue += 3 * GET_PLAYER(getOwner()).AI_plotTargetMissionAIs(
				pCity->getPlot(), MISSIONAI_ASSAULT, getGroup(), 2);
		if (canBombard(kPlot))
			iValue *= 2;
		iValue *= 1000;
		iValue /= (iPathTurns + 1);
		if (iPathTurns == 1)
		{
			//Prefer to have movement remaining to Bombard + Plunder
			iValue *= 1 + std::min(2, getPathFinder().getFinalMoves());
		}

		/*	if not at war with this plot owner,
			then devalue plot if we already inside this owner's borders
			(because declaring war will pop us some unknown distance away) */
		if (!isEnemy(kPlot) && getPlot().getTeam() == kPlot.getTeam())
			iValue /= 10;
		if (iValue > iBestValue)
		{
			iBestValue = iValue;
			pBestPlot = &getPathEndTurnPlot();
			pBestBlockadePlot = &kPlot;
		}
	}

	if (pBestPlot == NULL || pBestBlockadePlot == NULL)
		return false;

	FAssert(canPlunder(*pBestBlockadePlot));
	if (atPlot(pBestBlockadePlot) && !isEnemy(*pBestBlockadePlot))
	{
		//getGroup()->groupDeclareWar(pBestBlockadePlot, true);
		if(AI_considerPathDOW(*pBestBlockadePlot, eFlags)) // K-Mod
		{
			// <advc.163>
			if(!canMove())
				return true;
		} // </advc.163>
	}

	if (at(*pBestBlockadePlot))
	{
		if (canBombard(getPlot()))
		{
			getGroup()->pushMission(MISSION_BOMBARD, -1, -1, NO_MOVEMENT_FLAGS,
					false, false, MISSIONAI_BLOCKADE, pBestBlockadePlot);
		}
		getGroup()->pushMission(MISSION_PLUNDER, -1, -1, NO_MOVEMENT_FLAGS,
				//(getGroup()->getLengthMissionQueue() > 0), false, MISSIONAI_BLOCKADE, pBestBlockadePlot);
				true, false, MISSIONAI_BLOCKADE, pBestBlockadePlot); // K-Mod

		return true;
	}
	else
	{
		pushGroupMoveTo(*pBestPlot, eFlags, false, false,
				MISSIONAI_BLOCKADE, pBestBlockadePlot);
		return true;
	}

	return false;
}

// K-Mod todo: this function is very slow on large maps. Consider rewriting it!
// k146, advc.opt (comment): Performance might be OK now
bool CvUnitAI::AI_pirateBlockade()
{
	PROFILE_FUNC();

	/*  <k146> Removed the loop that computed the vector 'aiDeathZone'
		("computationally expensive, and not particularly effective").
		advc: I'm re-using parts of the body of that loop for a more limited
		danger check. */
	int const iCurrEffStr = currEffectiveStr(plot(), NULL, NULL);
	bool bInDanger = false;
	for (SquareIter it(*this, baseMoves(), false); it.hasNext(); ++it)
	{
		CvPlot const& p = *it;
		if(!p.isVisible(getTeam()) || (!p.isArea(getArea()) && !p.isCity()))
			continue;
		if(p.getNumUnits() > 20) // Make sure we're not spending too much time
			continue;
		FOR_EACH_UNIT_IN(pLoopUnit, p)
		{
			CvUnit const& u = *pLoopUnit;
			if(u.getDomainType() == DOMAIN_SEA && u.canFight() &&
				!u.getUnitInfo().isMostlyDefensive() &&
				isEnemy(u.getTeam()) &&
				!u.isInvisible(getTeam(), false) &&
				u.currEffectiveStr(NULL, NULL, NULL) > iCurrEffStr + 50)
			{
				bInDanger = true;
				goto terminate_outer;
			}
		}
	} terminate_outer:
	// </k146>
	if (!bInDanger && getDamage() > 0 &&
		!getPlot().isOwned() && !getPlot().isAdjacentOwned())
	{
		if (AI_retreatToCity(false, false, 1 + getDamage() / 20))
		{
			return true;
		}
		getGroup()->pushMission(MISSION_SKIP);
		return true;
	}

	CvPlot const* pBestPlot = NULL;
	CvPlot const* pBestBlockadePlot = NULL;
	bool bBestIsForceMove = false;
	bool bBestIsMove = false;
	int const iTurnNumberSalt = GC.getGame().getGameTurn() % 7; // advc.opt
	int iBestValue = 0;
	for (int i = 0; i < GC.getMap().numPlots(); i++)
	{
		CvPlot const& kPlot = GC.getMap().getPlotByIndex(i);
		// advc: Reduce indentation
		if(!kPlot.isRevealed(getTeam()) || // advc.opt
			!AI_plotValid(kPlot) ||
			kPlot.isVisibleEnemyUnit(this) || !canPlunder(kPlot) ||
			//SyncRandSuccessRatio(3, 4) ||
			/*  advc.033: Replacing the above. Should make Privateers a bit
				more stationary. */
			scaled::hash(i + iTurnNumberSalt, getOwner()) > fixp(0.25) ||
			GET_PLAYER(getOwner()).AI_isAnyPlotTargetMissionAI(
			kPlot, MISSIONAI_BLOCKADE, getGroup(), 3) ||
			(!kPlot.isOwned() && kPlot.isAdjacentOwned())) // advc.opt
		{
			continue;
		}
		// BETTER_BTS_AI_MOD, Pirate AI, 01/17/09, jdog5000: MOVE_AVOID_ENEMY_WEIGHT_3
		int iPathTurns;
		if(!generatePath(kPlot, MOVE_AVOID_ENEMY_WEIGHT_3, true, &iPathTurns))
			continue;

		int iBlockadedCount = 0;
		int iPopulationValue = 0;
		int iRange = GC.getDefineINT(CvGlobals::SHIP_BLOCKADE_RANGE) - 1;
		for (int iX = -iRange; iX <= iRange; iX++)
		{
			for (int iY = -iRange; iY <= iRange; iY++)
			{
				CvPlot* pRangePlot = plotXY(kPlot.getX(), kPlot.getY(), iX, iY);
				if(pRangePlot == NULL /* advc.033: */ || pRangePlot->isBarbarian())
					continue;
				bool bPlotBlockaded = false;
				if (pRangePlot->isWater() && pRangePlot->isOwned() &&
					isEnemy(pRangePlot->getTeam(), kPlot))
				{
					bPlotBlockaded = true;
					iBlockadedCount += pRangePlot->getBlockadedCount(pRangePlot->getTeam());
				}
				if(bPlotBlockaded)
					continue;
				CvCity* pPlotCity = pRangePlot->getPlotCity();
				if (pPlotCity != NULL &&
				/*  advc (note): isEnemy checks isAlwaysHostile; so the owner
					of pPlotCity does not have to be a war enemy of this unit.
					In fact, plundering war enemies is discouraged below; doesn't yield gold. */
					isEnemy(pPlotCity->getTeam(), kPlot) &&
					!pPlotCity->isBarbarian()) // advc.123e
				{
					int iCityValue = 3 + pPlotCity->getPopulation();
					// <advc.033>
					if(GET_TEAM(pPlotCity->getTeam()).isVassal(getTeam()) ||
						GET_TEAM(getTeam()).isVassal(pPlotCity->getTeam()))
					{
						iCityValue = 0;
					}
					if(!isBarbarian())
					{
						int iAttitudeFactor = 10;
						int iAttitudeLevel = GET_PLAYER(getOwner()).
								AI_getAttitude(pPlotCity->getOwner());
						if (iAttitudeLevel > 0)
						{
							iAttitudeFactor = std::max(1,
									iAttitudeFactor -
									scaled(iAttitudeLevel).pow(fixp(1.5)).round());
						}
						iCityValue *= iAttitudeFactor;
						TechTypes eTechReq = getUnitInfo().getPrereqAndTech();
						int iOurEra = (eTechReq == NO_TECH ?
								GET_PLAYER(getOwner()).getCurrentEra() :
								GC.getInfo(eTechReq).getEra());
						int iTheirEra = GET_PLAYER(pPlotCity->getOwner()).getCurrentEra();
						scaled rEraFactor = fixp(1.5);
						if(iTheirEra > iOurEra)
							rEraFactor = fixp(0.5);
						if(iOurEra > iTheirEra)
							rEraFactor = fixp(2.5);
						/*  Era alone is too coarse. A civ in early Renaissance
							is a fine target for Privateers.
							Tbd.: Should check sth. like isTechTrading first --
							we might not know whether they have the tech. */
						if(eTechReq != NO_TECH && GET_TEAM(pPlotCity->getTeam()).
							isHasTech(eTechReq))
						{
							rEraFactor /= 2;
						}
						iCityValue = (iCityValue * rEraFactor).round();
					} // </advc.033>
					iCityValue *= (atWar(getTeam(), pPlotCity->getTeam()) ? 1 : 3);
					if (GET_PLAYER(pPlotCity->getOwner()).isNoForeignTrade())
						iCityValue /= 2;
					iPopulationValue += intdiv::uround(iCityValue,
							/*  advc.033: Normalize to keep the scale as it was
								and avoid overflows */
							isBarbarian() ? 1 : 7);
				}
			}
		}
		int iValue = iPopulationValue;
		iValue *= 1000;
		iValue /= 16 + iBlockadedCount;

		bool bMove = getPathFinder().getPathTurns() == 1 && getPathFinder().getFinalMoves() > 0;
		if (at(kPlot))
			iValue *= 3;
		else if (bMove)
			iValue *= 2;
		bool bForceMove = false;
		// k146: Some bInDanger code deleted
		if (bInDanger && iPathTurns <= 2 && iPopulationValue == 0 &&
			getPathFinder().getFinalMoves() == 0) // advc
			// advc.opt: AdjacentOwned now guaranteed
			//&& !pLoopPlot->isAdjacentOwned()
		{
			int iRand = SyncRandNum(2500);
			iValue += iRand;
			if (iRand > 1000)
			{
				iValue += SyncRandNum(2500);
				bForceMove = true;
			}
		}

		if (!bForceMove)
			iValue /= iPathTurns + 1;

		if (iValue > iBestValue)
		{
			iBestValue = iValue;
			pBestPlot = &(bForceMove ? kPlot : getPathEndTurnPlot());
			pBestBlockadePlot = &kPlot;
			bBestIsForceMove = bForceMove;
			bBestIsMove = bMove;
		}
	}

	if (pBestPlot != NULL && pBestBlockadePlot != NULL)
	{
		FAssert(canPlunder(*pBestBlockadePlot));
		if (atPlot(pBestBlockadePlot))
		{
			getGroup()->pushMission(MISSION_PLUNDER, -1, -1, NO_MOVEMENT_FLAGS,
				/*(getGroup()->getLengthMissionQueue() > 0)*/ true, // K-Mod
				false, MISSIONAI_BLOCKADE, pBestBlockadePlot);
			{
				return true;
			}
		}
		else
		{
			if (bBestIsForceMove)
			{
				pushGroupMoveTo(*pBestPlot, MOVE_AVOID_ENEMY_WEIGHT_3);
				return true;
			}
			else
			{
				pushGroupMoveTo(*pBestPlot, MOVE_AVOID_ENEMY_WEIGHT_3,
						false, false, MISSIONAI_BLOCKADE, pBestBlockadePlot);
				if (bBestIsMove)
				{
					getGroup()->pushMission(MISSION_PLUNDER, -1, -1, NO_MOVEMENT_FLAGS,
							/*(getGroup()->getLengthMissionQueue() > 0)*/ true, // K-Mod
							false, MISSIONAI_BLOCKADE, pBestBlockadePlot);
				}
				return true;
			}
		}
	}
	return false;
}


bool CvUnitAI::AI_seaBombardRange(int iMaxRange)
{
	PROFILE_FUNC();

	bool bBombardUnitCanBombardNow = false;
	{
		bool bHasAnyBombardUnit = false;
		FOR_EACH_UNIT_IN(pLoopUnit, *getGroup())
		{
			if (pLoopUnit->bombardRate() > 0)
			{
				bHasAnyBombardUnit = true;
				if (pLoopUnit->canMove() && !pLoopUnit->isMadeAttack())
				{
					bBombardUnitCanBombardNow = true;
					break;
				}
			}
		}
		if (!bHasAnyBombardUnit)
			return false;
	}
	CvPlot* pBestPlot = NULL;
	CvPlot* pBestBombardPlot = NULL;
	int iBestValue = 0;
	for (SquareIter it(getPlot(), iMaxRange); it.hasNext(); ++it)
	{
		CvPlot& p = *it;
		if (!AI_plotValid(p))
			continue;
		CvCity const* pBombardCity = bombardTarget(p);
		/*  <advc.004c> Don't bombard cities at 0 (even if there is nothing
			better to do b/c it spams the message log) */
		if (pBombardCity != NULL && (pBombardCity->getDefenseModifier(false) <= 0 ||
			// advc.033:
			(pBombardCity->isBarbarian() && pBombardCity->getDefenseModifier(true) <= 0)))
		{
			pBombardCity = NULL;
		} // </advc.004c>
		if (pBombardCity != NULL && isEnemy(pBombardCity->getTeam(), p) &&
			pBombardCity->getDefenseDamage() < GC.getMAX_CITY_DEFENSE_DAMAGE())
		{
			int iPathTurns;
			if (generatePath(p, NO_MOVEMENT_FLAGS,
				true, &iPathTurns, 1 + iMaxRange / baseMoves()))
			{
				/*  BETTER_BTS_AI_MOD, Naval AI, 6/24/08 and 7/5/10, jdog5000: START
					Loop construction doesn't guarantee we can get there anytime soon,
					could be on other side of narrow continent */
				if (iPathTurns <= 1 + iMaxRange / std::max(baseMoves(), 1))
				{
					/*	Check only for supporting our own ground troops first
						if none will look for another target */
					int iValue = 3 * GET_PLAYER(getOwner()).AI_plotTargetMissionAIs(
							pBombardCity->getPlot(), MISSIONAI_ASSAULT, NULL, 2);
					iValue += (GET_PLAYER(getOwner()).AI_adjacentPotentialAttackers(
							pBombardCity->getPlot(), true));
					if (iValue > 0)
					{
						iValue *= 1000;
						iValue /= (iPathTurns + 1);
						if (iPathTurns == 1)
						{
							//Prefer to have movement remaining to Bombard + Plunder
							iValue *= 1 + std::min(2, getPathFinder().getFinalMoves());
						}
						if (iValue > iBestValue)
						{
							iBestValue = iValue;
							pBestPlot = &getPathEndTurnPlot();
							pBestBombardPlot = &p;
						}
					}
				} // BETTER_BTS_AI_MOD: END
			}
		}
	}
	/*  BETTER_BTS_AI_MOD, Naval AI, 6/24/08, jdog5000: START
		If no troops of ours to support, check for other bombard targets */
	if (pBestPlot == NULL && pBestBombardPlot == NULL &&
		AI_getUnitAIType() != UNITAI_ASSAULT_SEA)
	{
		for (SquareIter it(getPlot(), iMaxRange); it.hasNext(); ++it)
		{
			CvPlot& p = *it;
			if (!AI_plotValid(p))
				continue;
			CvCity* pBombardCity = bombardTarget(p);
			/*	Consider city even if fully bombarded, causes ship to camp outside
				blockading instead of twitching between cities after bombarding to 0 */
			if (pBombardCity != NULL && isEnemy(pBombardCity->getTeam(), p) &&
				pBombardCity->getTotalDefense(false) > 0 &&
				/*  advc.033: Barbarians normally have only building defense.
					If that's the case, don't sea-bombard them. */
				(!pBombardCity->isBarbarian() || pBombardCity->getTotalDefense(true) > 0))
			{
				int iPathTurns;
				if (!generatePath(p, NO_MOVEMENT_FLAGS, true,
					&iPathTurns, 1 + iMaxRange / baseMoves()))
				{
					continue;
				}
				/*	Loop construction doesn't guarantee we can get there anytime soon,
					could be on other side of narrow continent */
				if (iPathTurns <= 1 + iMaxRange / baseMoves())
				{
					int iValue = std::min(20,pBombardCity->getDefenseModifier(false) / 2);

					// Inclination to support attacks by others
					// BETTER_BTS_AI_MOD, Unit AI, Efficiency, 08/20/09, jdog5000: was AI_getPlotDanger
					if (GET_PLAYER(pBombardCity->getOwner()).AI_isAnyPlotDanger(
						*pBombardCity->plot(), 2, false))
					{
						iValue += 60;
					}

					// Inclination to bombard a different nearby city to extend the reach of blockade
					if (!GET_PLAYER(getOwner()).AI_isAnyPlotTargetMissionAI(
						pBombardCity->getPlot(), MISSIONAI_BLOCKADE, getGroup(), 3))
					{
						iValue += 35 + pBombardCity->getPopulation();
					}
					// Small inclination to bombard area target, not too large so as not to tip our hand
					if (pBombardCity == pBombardCity->getArea().AI_getTargetCity(getOwner()))
						iValue += 10;

					if (iValue > 0)
					{
						iValue *= 1000;
						iValue /= (iPathTurns + 1);
						if (iPathTurns == 1)
						{
							//Prefer to have movement remaining to Bombard + Plunder
							iValue *= 1 + std::min(2, getPathFinder().getFinalMoves());
						}
						if (iValue > iBestValue)
						{
							iBestValue = iValue;
							pBestPlot = &getPathEndTurnPlot();
							pBestBombardPlot = &p;
						}
					}
				}
			}
		}
	} // BETTER_BTS_AI_MOD: END

	if (pBestPlot == NULL || pBestBombardPlot == NULL)
		return false;
	if (!atPlot(pBestBombardPlot))
	{
		pushGroupMoveTo(*pBestPlot, NO_MOVEMENT_FLAGS, false, false,
				MISSIONAI_BLOCKADE, pBestBombardPlot);
		return true;
	}
	if (bBombardUnitCanBombardNow && // we have a unit that can bombard this turn
		// we are at the plot from which to bombard
		getGroup()->canBombard(*pBestBombardPlot))
	{
		getGroup()->pushMission(MISSION_BOMBARD,
				-1, -1, NO_MOVEMENT_FLAGS, false, false,
				MISSIONAI_BLOCKADE, pBestBombardPlot);
		// if city not bombarded enough, wake up any units waiting to bombard this city.
		CvCity* pBombardCity = bombardTarget(*pBestBombardPlot);
		if (pBombardCity == NULL || // city cannot be bombarded further
			pBombardCity->getDefenseDamage() * 6 < GC.getMAX_CITY_DEFENSE_DAMAGE() * 5)
		{
			GET_PLAYER(getOwner()).AI_wakePlotTargetMissionAIs(
					*pBestBombardPlot, MISSIONAI_BLOCKADE, getGroup());
		}
		return true;
	}
	// (next turn we will surely bombard)
	if (canPlunder(*pBestBombardPlot))
	{
		getGroup()->pushMission(MISSION_PLUNDER, -1, -1, NO_MOVEMENT_FLAGS,
				false, false, MISSIONAI_BLOCKADE, pBestBombardPlot);
		return true;
	}
	getGroup()->pushMission(MISSION_SKIP);
	return true;
}


bool CvUnitAI::AI_pillage(int iBonusValueThreshold, MovementFlags eFlags)
{
	PROFILE_FUNC();

	CvPlot const* pBestPlot = NULL;
	CvPlot const* pBestPillagePlot = NULL;
	int iBestValue = 0;
	for (int i = 0; i < GC.getMap().numPlots(); i++)
	{
		CvPlot const& kPlot = GC.getMap().getPlotByIndex(i);
		if (!AI_plotValid(kPlot) || kPlot.isBarbarian() || kPlot.isMinorCiv()) // doc
			continue;

		// BETTER_BTS_AI_MOD, Unit AI, Efficiency, 02/22/10, jdog5000: START
		//if (AI_mayAttack(*pLoopPlot))
		if (kPlot.isOwned() && isEnemy(kPlot))
		{
			CvCity* pWorkingCity = kPlot.getWorkingCity();
			if (pWorkingCity == NULL)
				continue;

			if (pWorkingCity != getArea().AI_getTargetCity(getOwner()) &&
				canPillage(kPlot))
			{
				if (!kPlot.isVisibleEnemyUnit(this))
				{
					if (!GET_PLAYER(getOwner()).AI_isAnyPlotTargetMissionAI(
						kPlot, MISSIONAI_PILLAGE, getGroup(), 1))
					{
						int iValue = AI_pillageValue(kPlot, iBonusValueThreshold);
						iValue *= 1000;
						/*	if not at war with kPlot's owner, then devalue kPlot
							if we are already inside the owner's borders
							(because declaring war will pop us some unknown distance away) */
						/*if (getPlot().getTeam() == kPlot.getTeam() && !isEnemy(kPlot))
							iValue /= 10;*/ // advc: Never true b/c of initial isEnemy(kPlot) check
						if (iValue > iBestValue)
						{
							int iPathTurns;
							if (generatePath(kPlot, eFlags, true, &iPathTurns))
							{
								iValue /= (iPathTurns + 1);
								if (iValue > iBestValue)
								{
									iBestValue = iValue;
									pBestPlot = &getPathEndTurnPlot();
									pBestPillagePlot = &kPlot;
								}
							}
						}
					}
				}
			}
		} // BETTER_BTS_AI_MOD: END
	}

	if (pBestPlot != NULL && pBestPillagePlot != NULL)
	{
		if (at(*pBestPillagePlot))
		{
			if (isEnemy(*pBestPillagePlot))
			{
				getGroup()->pushMission(MISSION_PILLAGE, -1, -1, NO_MOVEMENT_FLAGS,
						false, false, MISSIONAI_PILLAGE, pBestPillagePlot);
				return true;
			}
			else // (advc: simplified)
			{
				//getGroup()->groupDeclareWar(pBestPillagePlot, true);
				/*	rather than declare war, just find something else to do
					since we may already be deep in enemy territory */
				return false;
			}
		}
		else
		{
			pushGroupMoveTo(*pBestPlot, eFlags, false, false,
					MISSIONAI_PILLAGE, pBestPillagePlot);
			return true;
		}
	}

	return false;
}

/*  advc.003j: This Vanilla Civ 4 function was, apparently, never used.
	I think it says that it's OK to pillage unowned tiles when they don't
	belong to the trade network of a non-hostile civ. Seems sensible.
	The current AI code (see AI_pillage above) never pillages unowned tiles. */
/*bool CvUnitAI::AI_canPillage(CvPlot& kPlot) const {
	if (isEnemy(kPlot))
		return true;
	if (!kPlot.isOwned()) {
		bool bPillageUnowned = true;
		for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS &&
				bPillageUnowned; iPlayer++) {
			CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iPlayer);
			if (!isEnemy(kLoopPlayer.getTeam(), &kPlot)) {
				FOR_EACH_CITY(pCity, kLoopPlayer) {
					if (kPlot.getPlotGroup(kLoopPlayer.getID()) == pCity->getPlot().getPlotGroup(kLoopPlayer.getID())) {
						bPillageUnowned = false;
						break;
					}
				}
			}
		}
		if (bPillageUnowned)
			return true;
	}
	return false;
}*/


bool CvUnitAI::AI_pillageRange(int iRange, int iBonusValueThreshold, MovementFlags eFlags)
{
	PROFILE_FUNC();

	CvPlot* pBestPlot = NULL;
	CvPlot* pBestPillagePlot = NULL;
	int iBestValue = 0;
	for (SquareIter it(*this, AI_searchRange(iRange)); it.hasNext(); ++it)
	{
		CvPlot& p = *it;
		if (!AI_plotValid(p) || p.isBarbarian())
		{
			continue; // advc (and some other shortcuts below)
		}
		// <advc.033>
		if (isAlwaysHostile() && p.isOwned() &&
			!GET_PLAYER(getOwner()).AI_isPiracyTarget(p.getOwner()))
		{
			continue;
		} // </advc.033>

	    // doc: protect from barbarians
	    if (isBarbarian() && p.isOwned())
	    {
	        if (p.isMinorCiv())
	            continue;
	        if (GC.getGame().getGameTurn() < GET_PLAYER(p.getOwner()).getInitialBirthTurn() + getTurns(20))
	            continue;
	    }

		CvCity* pWorkingCity = p.getWorkingCity();
		if(pWorkingCity == NULL || !AI_mayAttack(p)) // advc.opt: Attack check moved down
			continue;
		if ((pWorkingCity != getArea().AI_getTargetCity(getOwner()) ||
			/*  advc.001: Barbarians should not exclude any city from pillaging.
				(Bugfix obsolete b/c Barbarians no longer have a target city.) */
			isBarbarian()) &&
			canPillage(p))
		{
			int iPathTurns;
			if(p.isVisibleEnemyUnit(this) ||
				GET_PLAYER(getOwner()).AI_isAnyPlotTargetMissionAI(
				p, MISSIONAI_PILLAGE, getGroup()) ||
				!generatePath(p, eFlags, true, &iPathTurns, iRange))
			{
				continue;
			}
			if (getPathFinder().getFinalMoves() == 0)
				iPathTurns++;

			if (iPathTurns <= iRange)
			{
				int iValue = AI_pillageValue(p, iBonusValueThreshold);
				iValue *= 1000;
				iValue /= (iPathTurns + 1);

				// if not at war with this plot owner, then devalue plot if we already inside this owner's borders
				// (because declaring war will pop us some unknown distance away)
				if (!isEnemy(p) && getPlot().getTeam() == p.getTeam())
					iValue /= 10;
				if (iValue > iBestValue)
				{
					iBestValue = iValue;
					pBestPlot = &getPathEndTurnPlot();
					pBestPillagePlot = &p;
				}
			}
		}
	}

	if (pBestPlot != NULL && pBestPillagePlot != NULL)
	{
		if (atPlot(pBestPillagePlot) && !isEnemy(*pBestPillagePlot))
		{
			//getGroup()->groupDeclareWar(pBestPillagePlot, true);
			// rather than declare war, just find something else to do, since we may already be deep in enemy territory
			return false;
		}

		if (at(*pBestPillagePlot))
		{
			if (isEnemy(*pBestPillagePlot))
			{
				getGroup()->pushMission(MISSION_PILLAGE, -1, -1, NO_MOVEMENT_FLAGS,
						false, false, MISSIONAI_PILLAGE, pBestPillagePlot);
				return true;
			}
		}
		else
		{
			pushGroupMoveTo(*pBestPlot, eFlags, false, false,
					MISSIONAI_PILLAGE, pBestPillagePlot);
			return true;
		}
	}

	return false;
}


bool CvUnitAI::AI_found(MovementFlags eFlags)
{
	PROFILE_FUNC();
//	advc: Most of the original code deleted
//	CvPlot* pLoopPlot;
//	...
//	for (iI = 0; iI < GC.getMap().numPlots(); iI++)
//	{
//		pLoopPlot = GC.getMap().plotByIndex(iI);
//		...
//	}

	CvPlot* pBestPlot = NULL;
	CvPlot* pBestFoundPlot = NULL;
	int iBestFoundValue = 0;
	bool const bRandomize = (!isHuman() && GC.getGame().isScenario()); // advc.052
	bool const bSafe = (getGroup()->canDefend() ||
			getInvisibleType() != NO_INVISIBLE); // advc.057b
	for (int i = 0; i < GET_PLAYER(getOwner()).AI_getNumCitySites(); i++)
	{
		CvPlot& kSite = GET_PLAYER(getOwner()).AI_getCitySite(i);

        // doc: never found if settler value is 0
	    if (kSite.getSettlerValue(getOwner()) == 0)
	        return false;

		if (AI_canEnterByLand(kSite.getArea()) || // advc.030 (replacing same-area check)
			// BETTER_BTS_AI_MOD, Settler AI, 10/23/09, jdog5000:
			canMoveAllTerrain())
		{
			if (canFound(&kSite) &&
				!GET_PLAYER(getOwner()).AI_isAnyPlotTargetMissionAI(
				kSite, MISSIONAI_FOUND, getGroup()))
			{
				if (bSafe ||
					GET_PLAYER(getOwner()).AI_isAnyPlotTargetMissionAI(
					kSite, MISSIONAI_GUARD_CITY))
				{
					int iPathTurns;
					if (generatePath(kSite, eFlags, true, &iPathTurns))
					{
						if (!kSite.isVisible(getTeam()) || // K-Mod
							!kSite.isVisibleEnemyUnit(this) ||
							(iPathTurns > 1 && bSafe)) // K-Mod
						{
							int iValue = kSite.getFoundValue(getOwner());
							// <advc.052>
							if (bRandomize)
							{
								scaled rPlusMinus = fixp(0.04);
								scaled rRandMult = 1 - rPlusMinus + 2 * rPlusMinus *
										scaled::hash(m_iBirthmark);
								iValue = (iValue * rRandMult).round();
							} // </advc.052>
							iValue *= 1000;
							//iValue /= (iPathTurns + 1);
							iValue /= iPathTurns + (bSafe ? 4 : 1); // K-Mod
							if (iValue > iBestFoundValue)
							{
								iBestFoundValue = iValue;
								pBestPlot = &getPathEndTurnPlot();
								pBestFoundPlot = &kSite;
							}
						}
					}
				}
			}
		}
	}
	if (pBestPlot == NULL || pBestFoundPlot == NULL)
		return false;
	if (at(*pBestFoundPlot))
	{
		if (gUnitLogLevel >= 2) logBBAI("    Settler founding at site %d, %d", pBestFoundPlot->getX(), pBestFoundPlot->getY());
		getGroup()->pushMission(MISSION_FOUND, -1, -1, NO_MOVEMENT_FLAGS,
				false, false, MISSIONAI_FOUND, pBestFoundPlot);
		return true;
	}
	else
	{
		if (gUnitLogLevel >= 2)logBBAI("    Settler heading for site %d, %d", pBestFoundPlot->getX(), pBestFoundPlot->getY());
		pushGroupMoveTo(*pBestPlot, eFlags, false, false,
				MISSIONAI_FOUND, pBestFoundPlot);
		return true;
	}
}


/*bool CvUnitAI::AI_foundRange(int iRange, bool bFollow)
{
	... // advc: Body deleted
}*/ // BtS - disabled by K-Mod

/*	K-Mod: this function simply checks if we are standing at our target destination
	and if we are, we issue the found command and return true.
	I've disabled (badly flawed) AI_foundRange, which was previously used for 'follow' AI. */
bool CvUnitAI::AI_foundFollow()
{
	if (canFound(plot()) && atPlot(AI_getGroup()->AI_getMissionAIPlot()) &&
		AI_getGroup()->AI_getMissionAIType() == MISSIONAI_FOUND)
	{
		if (gUnitLogLevel >= 2) logBBAI("    Settler founding at plot %d, %d (follow)", getX(), getY());
		getGroup()->pushMission(MISSION_FOUND);
		return true;
	}

	return false;
}

namespace
{
	// K-Mod. helper function for AI_assaultSeaTransport. (just to avoid code duplication)
	int estimateAndCacheCityDefence(CvPlayerAI& kPlayer, CvCityAI const* pCity, // advc.003u: was CvCity*
		std::map<CvCityAI const*, int>& city_defence_cache)
	{
		// calculate the city's defences, or read from the cache if we've already done it.
		std::map<CvCityAI const*,int>::iterator city_it = city_defence_cache.find(pCity);
		int iDefenceStrength = -1;
		if (city_it == city_defence_cache.end())
		{
			if (pCity->getPlot().isVisible(kPlayer.getTeam()))
				iDefenceStrength = kPlayer.AI_localDefenceStrength(pCity->plot());
			else
			{
				/*	If we don't have vision of the city, we should try to
					estimate its strength based the expected number of defenders. */
				int iUnitStr = GET_PLAYER(pCity->getOwner()).
						getTypicalUnitValue(UNITAI_CITY_DEFENSE, DOMAIN_LAND) *
						GC.getGame().getBestLandUnitCombat() / 100;
				iDefenceStrength = std::max(GET_TEAM(kPlayer.getTeam()).
						AI_strengthMemory().get(pCity->getPlot()),
						pCity->AI_neededDefenders()*iUnitStr);
			}
			city_defence_cache[pCity] = iDefenceStrength;
		}
		else
		{
			// use the cached value
			iDefenceStrength = city_it->second;
		}
		return iDefenceStrength;
	} // K-Mod end
}

// This function has been mostly rewritten for K-Mod.
bool CvUnitAI::AI_assaultSeaTransport(bool bAttackBarbs, bool bLocal,
	int iMaxAreaCities) // advc.082
{
	PROFILE_FUNC();

	//bool bAttackCity = (getUnitAICargo(UNITAI_ATTACK_CITY) > 0);

	FAssert(getGroup()->hasCargo());
	//FAssert(bAttackCity || getGroup()->getUnitAICargo(UNITAI_ATTACK) > 0);

	/*if (!canCargoAllMove())
		return false;*/ // BtS - disabled by K-Mod. (this is now checked in AI_assaultGoTo)

	CvPlayerAI& kOwner = GET_PLAYER(getOwner());
	CvTeamAI const& kOurTeam = GET_TEAM(getTeam()); // advc

	int iLimitedAttackers = 0;
	int iAmphibiousAttackers = 0;
	int iAmphibiousAttackStrength = 0;
	int iLandedAttackStrength = 0;
	int iCollateralDamageScale = estimateCollateralWeight(0, kOurTeam.getID());
	std::map<CvCityAI const*, int> city_defence_cache; // advc: const

	//std::vector<CvUnit const*> apGroupCargo; // advc: unused
	FOR_EACH_UNITAI_IN(pLoopUnit, getPlot())
	{
		CvUnit const* pTransport = pLoopUnit->getTransportUnit();
		if (pTransport == NULL || pTransport->getGroup() != getGroup())
			continue;

		//apGroupCargo.push_back(&kLoopUnit);
		// K-Mod. Gather some data for later...
		if (pLoopUnit->combatLimit() < 100)
			iLimitedAttackers++;
		if (pLoopUnit->isAmphib())
			iAmphibiousAttackers++;

		// Estimate attack strength, both for landed assaults and amphibious assaults.
		//
		/*  Unfortunately, we can't use AI_localAttackStrength because that may miscount
			depending on whether there is another group on this plot and things like that,
			and we can't use AI_sumStrength because that currently only works for groups.
			What we have here is a list of cargo units rather than a group. */
		if (!pLoopUnit->canAttack() || /* advc: */ pLoopUnit->isDead())
			continue;
		//int iUnitStr = pLoopUnit->currEffectiveStr(NULL, NULL);
		// advc.159: Also handles first strikes and coll. damage (code here deleted)
		int iUnitStr = pLoopUnit->AI_currEffectiveStr(
				NULL, NULL, true, iCollateralDamageScale);
		iLandedAttackStrength += iUnitStr;
		if (pLoopUnit->combatLimit() >= 100 && pLoopUnit->canMove() &&
			!pLoopUnit->isMadeAllAttacks()) // advc.164
		{
			if (!pLoopUnit->isAmphib())
			{
				// advc (note): The (BtS) modifier is negative
				iUnitStr += iUnitStr * GC.getDefineINT(CvGlobals::AMPHIB_ATTACK_MODIFIER) / 100;
			}
			iAmphibiousAttackStrength += iUnitStr;
		}
		// K-Mod end
	}

	MovementFlags const eFlags = (MOVE_AVOID_ENEMY_WEIGHT_3 | MOVE_DECLARE_WAR); // K-Mod
	int iCargo = getGroup()->getCargo();
	FAssert(iCargo > 0);
	CvPlot const* pBestPlot = NULL;
	CvPlot const* pBestAssaultPlot = NULL;
	int iBestValue = 0;
	/*	K-Mod note: I've restructured and rewritten this section for efficiency, clarity,
		and sometimes even to improve the AI! Most of the original code has been deleted. */
	for (int i = 0; i < GC.getMap().numPlots(); i++)
	{
		CvPlot const& kPlot = GC.getMap().getPlotByIndex(i);
		if (!kPlot.isRevealed(kOurTeam.getID()))
			continue;
		if (!kPlot.isOwned())
			continue;
		if (!bAttackBarbs && kPlot.isBarbarian() && !kOwner.isMinorCiv())
			continue;
		if (!kPlot.isCoastalLand(-1)) // advc.opt: -1: skip lakes too
			continue;
        // doc: only target war map targets
        if (kPlot.getWarValue(getOwner()) <= 1)
            continue;
		//if (!isPotentialEnemy(kPlot.getTeam(), &kPlot))
		if (!kOurTeam.AI_mayAttack(kPlot.getTeam())) // advc
			continue;
		// <advc.306>
		if(isBarbarian() && kPlot.getTeam() != NO_TEAM &&
			kPlot.getArea().isBorderObstacle(kPlot.getTeam()))
		{
			continue;
		} // </advc.306>
		// Note: currently these condtions mean we will never land to invade land-locked enemies

		int const iTargetCities = kPlot.getArea().getCitiesPerPlayer(kPlot.getOwner());
		if (iTargetCities == 0 ||
			// advc.082: (Would be better to count revealed cities of all enemy civs)
			iTargetCities > iMaxAreaCities)
		{
			continue;
		}
		int iPathTurns;
		if (!generatePath(kPlot, eFlags, true, &iPathTurns))
			continue;

		CvCityAI const* pCity = kPlot.AI_getPlotCity();
		// <advc.001> kPlot is revealed, but pCity might not be.
		if (pCity != NULL && !kOurTeam.AI_deduceCitySite(*pCity))
			pCity = NULL; // </advc.001>
		/*	If the plot can't be seen, then just roughly estimate
			what the AI might think is there... */
		int iEnemyDefenders = ((kPlot.isVisible(kOurTeam.getID()) ||
				kOurTeam.AI_strengthMemory().get(kPlot) > 0) ?
				AI_countEnemyDefenders(kPlot) :
				(pCity != NULL ? pCity->AI_neededDefenders() : 0));

		int iBaseValue = 10 + std::min(9, 3*iTargetCities);
		int iValueMultiplier = 100;

		/*	if there are defenders, we should decide whether or not it is
			worth attacking them amphibiously. */
		if (iEnemyDefenders > 0)
		{
			if ((iLimitedAttackers > 0 || 2 * iAmphibiousAttackers < iCargo) &&
				3 * iEnemyDefenders > 2 * (iCargo - iLimitedAttackers))
			{
				continue;
			}
			int iDefenceStrength=-1;
			if (pCity != NULL)
				iDefenceStrength = estimateAndCacheCityDefence(kOwner, pCity, city_defence_cache);
			else
			{
				iDefenceStrength = (kPlot.isVisible(kOurTeam.getID()) ?
						kOwner.AI_localDefenceStrength(&kPlot) :
						kOurTeam.AI_strengthMemory().get(kPlot));
			}
			/*	Note: the amphibious attack modifier is already taken into account by
				AI_localAttackStrength, but I'm going to apply a similar penality again
				just to discourage the AI from attacking amphibiously when they don't need to. */
			iDefenceStrength -= iDefenceStrength * GC.getDefineINT(CvGlobals::AMPHIB_ATTACK_MODIFIER) *
					(iCargo - iAmphibiousAttackers) / (100*iCargo);

			if (iAmphibiousAttackStrength * 100 <
				iDefenceStrength * GC.getDefineINT(CvGlobals::BBAI_ATTACK_CITY_STACK_RATIO))
			{
				continue;
			}
			if (pCity == NULL)
			{
				iValueMultiplier = iValueMultiplier *
						(iAmphibiousAttackStrength - iDefenceStrength *
						std::min(iCargo-iLimitedAttackers, iEnemyDefenders) / iEnemyDefenders) /
						iAmphibiousAttackStrength;
			}
		}

		if (pCity == NULL)
		{
			// consider landing on strategic resources
			iBaseValue += AI_pillageValue(kPlot, 15);

			int iModifier = 0;
			// prefer to land on a defensive plot, but not with a river between us and the city
			// advc.001: Moved. That's a consideration for an adjacent city.
			/*if (pCity && pLoopPlot->isRiverCrossing(directionXY(pLoopPlot, pCity->plot())))
				iModifier += GC.getRIVER_ATTACK_MODIFIER()/10;*/

			//iModifier += pLoopPlot->defenseModifier(kOurTeam.getID(), false) / 10;
			// advc.012: Replacing the above
			iModifier += AI_plotDefense(&kPlot) / 10;
			// advc.001: See the comment above. This will have to move too.
			//iValueMultiplier = (100+iModifier)*iValueMultiplier / 100;

			// Look for adjacent cities.
			// advc.001: Better to use a separate variable for this
			CvCityAI const* pAdjCity = NULL;
			FOR_EACH_ADJ_PLOT(kPlot)
			{
				pAdjCity = pAdj->AI_getPlotCity();
				if (pAdjCity != NULL)
				{
					if (pAdjCity->getOwner() == kPlot.getOwner())
						break;
					pAdjCity = NULL;
				}
			}  // <advc.001>
			if(pAdjCity != NULL && kOurTeam.AI_deduceCitySite(*pAdjCity))
			{
				pCity = pAdjCity;
				// Copied from above
				if(kPlot.isRiverCrossing(directionXY(kPlot, pCity->getPlot())))
					iModifier += GC.getDefineINT(CvGlobals::RIVER_ATTACK_MODIFIER)/10;
			} // Also copied from above
			iValueMultiplier *= (100 + iModifier);
			iValueMultiplier /= 100;
			// </advc.001>
		}

		if (pCity != NULL)
		{
			int iDefenceStrength = estimateAndCacheCityDefence(kOwner, pCity, city_defence_cache);
			FAssert(AI_isPotentialEnemyOf(pCity->getTeam(), kPlot));
			iBaseValue += kOwner.AI_targetCityValue(*pCity, false, false); // maybe false, true?

			if (pCity->plot() == &kPlot)
			{
				// apparently we can take the city amphibiously
				iValueMultiplier *= (kPlot.isVisible(kOurTeam.getID()) ? 5 : 2);
			}
			else
			{
				/*	prefer to join existing assaults.
					(maybe we should calculate the actual attack strength here and roll it
					into the strength comparison modifier below) */
				int iModifier = std::min(kOwner.AI_plotTargetMissionAIs(
						kPlot, MISSIONAI_ASSAULT, getGroup()) +
						kOwner.AI_adjacentPotentialAttackers(pCity->getPlot()), 2 * iCargo) *
						100 / iCargo;
				iValueMultiplier = (100+iModifier)*iValueMultiplier / 100;

				/*	Prefer to target cities that we can defeat.
					However, keep in mind that if we often won't be able to
					see the city to gauge their defenses. */

				if (iDefenceStrength > 0 || kPlot.isVisible(kOurTeam.getID()))
				{
					if (kPlot.isVisible(kOurTeam.getID()))
					{
						iModifier = (125 * iLandedAttackStrength) /
								std::max(1, iDefenceStrength);
						iModifier -= 25;
						iModifier = std::min(iModifier, 100);
					}
					else
					{
						iModifier = (75 * iLandedAttackStrength) /
								std::max(1, iDefenceStrength);
						iModifier -= 25;
						iModifier = std::min(iModifier, 50);
					}
				} // otherwise, assume we have no idea what's there.
				iValueMultiplier = (100 + iModifier) * iValueMultiplier / 100;
			}
		}

		// Continue attacking in area we have already captured cities
		if (kPlot.getArea().getCitiesPerPlayer(getOwner()) > 0)
		{
			if (pCity != NULL && (bLocal || pCity->AI_playerCloseness(getOwner()) > 5))
				iValueMultiplier = iValueMultiplier*3/2;
		}
		else if (bLocal)
			iValueMultiplier = iValueMultiplier*2/3;

		/*	K-Mod note: It would be nice to use the pathfinder again here
			to make sure we aren't landing a long way from any enemy cities;
			otherwise the AI might get into a loop of contantly dropping
			off units which just walk back to the city to be dropped off again.
			(maybe some other time) */

		FAssert(iPathTurns > 0);

		/*	some old bts code. The ideas here are worth remembering,
			but the execution is not suitable. */
		/*if (iPathTurns == 1) {
			if (pCity != NULL) {
				if (pCity->getArea().getNumCities() > 1)
					iValue *= 2;
			}
		}
		iValue *= 1000;
		if (iTargetCities <= iAssaultsHere)
			iValue /= 2;
		if (iTargetCities == 1) {
			if (iCargo > 7) {
				iValue *= 3;
				iValue /= iCargo - 4;
			}
		}
		if (pLoopPlot->isCity()) {
			if (iEnemyDefenders * 3 > iCargo)
				iValue /= 10;
			else {
				iValue *= iCargo;
				iValue /= std::max(1, (iEnemyDefenders * 3));
			}
		}
		else {
			if (iEnemyDefenders == 0) {
				iValue *= 4;
				iValue /= 3;
			}
			else iValue /= iEnemyDefenders;
		}
		// if more than 3 turns to get there, then put some randomness into our preference of distance
		// +/- 33%
		if (iPathTurns > 3) {
			int iPathAdjustment = SyncRandNum(67);
			iPathTurns *= 66 + iPathAdjustment;
			iPathTurns /= 100;
		}
		iValue /= (iPathTurns + 1);*/
		/*	K-Mod. A bit of randomness is good, but if it's random every turn
			then it will lead to inconsistent decisions.
			So.. if we're already en-route somewhere, try to keep going there. */
		if (pCity != NULL && AI_getGroup()->AI_getMissionAIPlot() &&
			stepDistance(AI_getGroup()->AI_getMissionAIPlot(), pCity->plot()) <= 1)
		{
			iValueMultiplier *= 150;
			iValueMultiplier /= 100;
		}
		else if (iPathTurns > 2)
		{
			//iValue *= 60 + SyncRandNum(81);
			iValueMultiplier *= 60 +
					(AI_unitPlotHash(&kPlot, getGroup()->getNumUnits()) % 81);
			iValueMultiplier /= 100;
		}
		int iValue = iBaseValue * iValueMultiplier / (iPathTurns +2);
		// K-Mod end

		if (iValue > iBestValue)
		{
			iBestValue = iValue;
			pBestPlot = &getPathEndTurnPlot();
			pBestAssaultPlot = &kPlot;
		}
	}

	if (pBestPlot != NULL && pBestAssaultPlot != NULL)
		return AI_transportGoTo(*pBestPlot, *pBestAssaultPlot, eFlags, MISSIONAI_ASSAULT);

	return false;
}

// This function has been heavily edited and restructured by K-Mod. It includes some bbai changes.
bool CvUnitAI::AI_assaultSeaReinforce(bool bAttackBarbs)
{
	PROFILE_FUNC();

	FAssert(getGroup()->hasCargo());
	FAssert(getGroup()->canAllMove()); // K-Mod (replacing a BBAI check that I'm sure is unnecessary.)

	std::vector<CvUnit const*> apGroupCargo;
	FOR_EACH_UNIT_IN(pLoopUnit, getPlot())
	{
		CvUnit const* pTransport = pLoopUnit->getTransportUnit();
		if (pTransport != NULL && pTransport->getGroup() == getGroup())
			apGroupCargo.push_back(pLoopUnit);
	}

	//bool bAttackCity = (getUnitAICargo(UNITAI_ATTACK_CITY) > 0); // advc: unused

	// bool bCity = getPlot().isCity(true, getTeam());
	/*	K-Mod note: bCity was used in a few places, but it should not be.
		If we make a decision based on being in a city,
		then we'll just change our mind as soon as we leave the city! */

	// Loop over nearby plots for groups in enemy territory to reinforce
	CvPlot const* pBestPlot = NULL;
	CvPlot const* pBestAssaultPlot = NULL;
	CvArea const* pWaterArea = getPlot().waterArea();
	bool const bCanMoveAllTerrain = getGroup()->canMoveAllTerrain();
	MovementFlags const eFlags = MOVE_AVOID_ENEMY_WEIGHT_3; // K-Mod. (no declare war)
	int iBestValue = 0;
	// advc: (from BBAI 1.02; was 2*maxMoves() previously)
	for (SquareIter it(*this, 2 * baseMoves()); it.hasNext(); ++it)
	{
		CvPlot const& p = *it;
		if (!isEnemy(p))
			continue;
		if (bCanMoveAllTerrain ||
			(pWaterArea != NULL && p.isAdjacentToArea(*pWaterArea)))
		{
			int iTargetCities = p.getArea().getCitiesPerPlayer(p.getOwner());
			if (iTargetCities > 0)
			{
				int iOurFightersHere = p.getNumDefenders(getOwner());
				if (iOurFightersHere > 2)
				{
					int iPathTurns;
					if (generatePath(p, eFlags, true, &iPathTurns, 2))
					{
						int iValue = 10*iTargetCities;
						iValue += 8*iOurFightersHere;
						iValue += 3*GET_PLAYER(getOwner()).AI_adjacentPotentialAttackers(p);
						iValue *= 100;
						iValue /= (iPathTurns + 1);
						if (iValue > iBestValue)
						{
							iBestValue = iValue;
							pBestPlot = &getPathEndTurnPlot();
							pBestAssaultPlot = &p;
						}
					}
				}
			}
		}
	}

	if (pBestPlot != NULL && pBestAssaultPlot != NULL)
		return AI_transportGoTo(*pBestPlot, *pBestAssaultPlot, eFlags, MISSIONAI_REINFORCE);

	// Loop over other transport groups, looking for synchronized landing
	CvTeamAI const& kOurTeam = GET_TEAM(getTeam());
	FOR_EACH_GROUPAI(pLoopSelectionGroup, GET_PLAYER(getOwner()))
	{
		if (pLoopSelectionGroup == getGroup())
			continue;

		if (pLoopSelectionGroup->AI_getMissionAIType() == MISSIONAI_ASSAULT &&
			// K-Mod. (b/c assault is also used for ground units)
			pLoopSelectionGroup->getHeadUnitAIType() == UNITAI_ASSAULT_SEA)
		{
			CvPlot* pLoopPlot = pLoopSelectionGroup->AI_getMissionAIPlot();
			if (pLoopPlot != NULL && //isPotentialEnemy(pLoopPlot->getTeam(), pLoopPlot)
				pLoopPlot->isOwned() && kOurTeam.AI_mayAttack(pLoopPlot->getTeam())) // advc
			{
				CvPlot const& p = *pLoopPlot; // advc: abbreviate
				if (bCanMoveAllTerrain ||
					(pWaterArea != NULL && p.isAdjacentToArea(*pWaterArea)))
				{
					int iTargetCities = p.getArea().getCitiesPerPlayer(p.getOwner());
					if (iTargetCities <= 0)
						continue;

					int iAssaultsHere = pLoopSelectionGroup->getCargo();
					if (iAssaultsHere < 3)
						continue;

					int iPathTurns;
					if (generatePath(p, eFlags, true, &iPathTurns))
					{
						CvPlot& kEndTurnPlot = getPathEndTurnPlot();
						int iOtherPathTurns = MAX_INT;
						//if (pLoopSelectionGroup->generatePath(pLoopSelectionGroup->plot(), pLoopPlot, eFlags, true, &iOtherPathTurns))
						/*	K-Mod. Use a different pathfinder
							so that we don't clear our path data. */
						//GroupPathFinder loopPath;
						GroupPathFinder& kLoopPath = CvSelectionGroup::getClearPathFinder();
						kLoopPath.setGroup(*pLoopSelectionGroup, eFlags, iPathTurns);
						if (kLoopPath.generatePath(p)) // K-Mod end
						{
							//iOtherPathTurns += 1;
							// (K-Mod note: I'm not convinced the +1 thing is a good idea.)
							iOtherPathTurns = kLoopPath.getPathTurns();
						}
						else continue;

						FAssert(iOtherPathTurns <= iPathTurns);
						if (iPathTurns >= iOtherPathTurns + 5)
							continue;

						int iValue = iAssaultsHere * 5;
						iValue += iTargetCities * 10;
						{
							bool const bCity = p.isCity();
							if (bCity ||
								//p.getNumVisibleEnemyDefenders(this) > 0
								p.isVisibleEnemyDefender(this)) // advc.opt
							{
								//bool bCanCargoAllUnload = true;
								int iCannotUnload = 0; // advc.082
								for (size_t i = 0; i < apGroupCargo.size(); ++i)
								{
									CvUnit const* pAttacker = apGroupCargo[i];
									if (p.isVisible(getTeam()) && // advc.082
										!p.hasDefender(true, NO_PLAYER,
										pAttacker->getOwner(), pAttacker, true))
									{
										iCannotUnload++;
										//break;
									}
									else if (bCity
										/*	advc.082: Doesn't make sense to me.
											If there's a city, then units w/ a combat limit
											can't attack it. Visibility shouldn't matter.
											It should matter for the hasDefender check above. */
										/*&& !p.isVisible(getTeam())*/)
									{
										// Artillery can't naval invade, so don't try
										if (pAttacker->combatLimit() < 100)
										{
											iCannotUnload++;
											//break;
										}
									}
								}
								/*	<advc.082> BtS had disregarded pLoopPlot
									if !bCanCargoAllUnload. This has gotten lost in BBAI. */
								/*	For a start, if pLoopSelectionGroup is headed directly
									for a city, it'll likely not need reinforcements. */
								if (bCity)
									iValue /= 2;
								// Additional discouragement for units that can't unload
								if (iCannotUnload > 0)
								{
									if (iCannotUnload * 3 >= (int)apGroupCargo.size())
										continue;
									iValue *= SQR(apGroupCargo.size() - iCannotUnload);
									iValue /= SQR(apGroupCargo.size());
								} // </advc.081>
							}
						}
						iValue *= 100;
						/*
						// if more than 3 turns to get there, then put some randomness into our preference of distance
						if (iPathTurns > 3) {
							int iPathAdjustment = SyncRandNum(67);
							iPathTurns *= 66 + iPathAdjustment; // +/- 33%
							iPathTurns /= 100;
						}
						iValue /= (iPathTurns + 1);*/ // BtS
						// K-Mod. More consistent randomness, to prevent decisions from oscillating.
						iValue *= 70 + (AI_unitPlotHash(&p, getGroup()->getNumUnits()) % 61);
						iValue /= 100;

						iValue /= (iPathTurns + 2);
						// K-Mod end

						if (iValue > iBestValue)
						{
							iBestValue = iValue;
							pBestPlot = &kEndTurnPlot;
							pBestAssaultPlot = &p;
						}
					}
				}
			}
		}
	}

	if (pBestPlot != NULL && pBestAssaultPlot != NULL)
		return AI_transportGoTo(*pBestPlot, *pBestAssaultPlot, eFlags, MISSIONAI_REINFORCE);

	// Reinforce our cities in need
	FOR_EACH_CITYAI(pLoopCity, GET_PLAYER(getOwner()))
	{
		if (!bCanMoveAllTerrain && (pWaterArea == NULL ||
			(pLoopCity->waterArea(true) != pWaterArea &&
			pLoopCity->secondWaterArea() != pWaterArea)))
		{
			continue;
		}
		int iValue = 0;
		// advc: if/else replaced with switch
		switch (pLoopCity->getArea().getAreaAIType(getTeam()))
		{
		case AREAAI_DEFENSIVE: iValue = 3; break;
		case AREAAI_OFFENSIVE: iValue = 2; break;
		case AREAAI_MASSING:   iValue = 1; break;
		default:
			if (bAttackBarbs && (pLoopCity->getArea().getCitiesPerPlayer(BARBARIAN_PLAYER) > 0))
				iValue = 1;
			else continue;
		}

		bool bCityDanger = pLoopCity->AI_isDanger();
		//if ((bCity && !pLoopCity->isArea(getArea())) || bCityDanger || ((GC.getGame().getGameTurn() - pLoopCity->getGameTurnAcquired()) < 10 && pLoopCity->getPreviousOwner() != NO_PLAYER))
		// <K-Mod>
		if (pLoopCity->getArea().getAreaAIType(getTeam()) == AREAAI_DEFENSIVE || bCityDanger ||
			(GC.getGame().getGameTurn() - pLoopCity->getGameTurnAcquired() < 10 &&
			pLoopCity->getPreviousCiv() != NO_CIVILIZATION)) // </K-Mod>
		{
			int iOurPower = std::max(1, pLoopCity->getArea().getPower(getOwner()));
			// Enemy power includes barb power
			int iEnemyPower = GET_TEAM(getTeam()).AI_countEnemyPowerByArea(pLoopCity->getArea());

			// Don't send troops to areas we are dominating already
			// Don't require presence of enemy cities, just a dangerous force
			if (iOurPower < 3 * iEnemyPower)
			{
				int iPathTurns;
				if (generatePath(pLoopCity->getPlot(), eFlags, true, &iPathTurns))
				{
					iValue *= 10*pLoopCity->AI_cityThreat();
					iValue += 20 * GET_PLAYER(getOwner()).AI_plotTargetMissionAIs(
							pLoopCity->getPlot(), MISSIONAI_ASSAULT, getGroup());
					iValue *= std::min(iEnemyPower, 3*iOurPower);
					iValue /= iOurPower;
					iValue *= 100;
					// if more than 3 turns to get there, then put some randomness into our preference of distance
					// +/- 33%
					if (iPathTurns > 3)
					{
						int iPathAdjustment = SyncRandNum(67);
						iPathTurns *= 66 + iPathAdjustment;
						iPathTurns /= 100;
					}
					iValue /= (iPathTurns + 6);
					if (iValue > iBestValue)
					{
						iBestValue = iValue;
						//pBestPlot = &(bCityDanger ? getPathEndTurnPlot() : pLoopCity->getPlot());
						pBestPlot = &getPathEndTurnPlot(); // K-Mod (why did they have that other stuff?)
						pBestAssaultPlot = pLoopCity->plot();
					}
				}
			}
		}
	}

	if (pBestPlot != NULL && pBestAssaultPlot != NULL)
		return AI_transportGoTo(*pBestPlot, *pBestAssaultPlot, eFlags, MISSIONAI_REINFORCE);

	// assist master in attacking
	TeamTypes eMasterTeam = GET_TEAM(getTeam()).getMasterTeam(); // advc.opt: Replacing a loop
	if (eMasterTeam != NO_TEAM && GET_TEAM(getTeam()).isOpenBorders(eMasterTeam))
	{
		for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
		{
			CvPlayerAI const& kMasterMember = GET_PLAYER((PlayerTypes)iI);
			if (kMasterMember.getTeam() != eMasterTeam)
				continue;

			FOR_EACH_CITYAI(pLoopCity, kMasterMember)
			{
				if (pLoopCity->isArea(getArea()))
					continue; // we can probably walk.

				int iValue = 0;
				switch (pLoopCity->getArea().getAreaAIType(eMasterTeam))
				{
				case AREAAI_OFFENSIVE:
					iValue = 2;
					break;

				case AREAAI_MASSING:
					iValue = 1;
					break;

				default:
					continue; // not an appropriate area.
				}

				if (bCanMoveAllTerrain ||
					(pWaterArea != NULL &&
					(pLoopCity->waterArea(true) == pWaterArea ||
					pLoopCity->secondWaterArea() == pWaterArea)))
				{
					int iOurPower = std::max(1, pLoopCity->getArea().getPower(getOwner()));
					iOurPower += GET_TEAM(eMasterTeam).countPowerByArea(pLoopCity->getArea());
					// Enemy power includes barb power
					int iEnemyPower = GET_TEAM(eMasterTeam).AI_countEnemyPowerByArea(pLoopCity->getArea());

					// Don't send troops to areas we are dominating already
					// Don't require presence of enemy cities, just a dangerous force
					if (iOurPower < 2 * iEnemyPower)
					{
						int iPathTurns;
						if (generatePath(pLoopCity->getPlot(), eFlags, true, &iPathTurns))
						{
							iValue *= pLoopCity->AI_cityThreat();

							iValue += 10 * GET_PLAYER(getOwner()).AI_plotTargetMissionAIs(
									pLoopCity->getPlot(), MISSIONAI_ASSAULT, getGroup());
							iValue *= std::min(iEnemyPower, 3*iOurPower);
							iValue /= iOurPower;

							iValue *= 100;
							/*	if more than 3 turns to get there, then put some randomness
								into our preference of distance: +/- 33% */
							if (iPathTurns > 3)
							{
								int iPathAdjustment = SyncRandNum(67);
								iPathTurns *= 66 + iPathAdjustment;
								iPathTurns /= 100;
							}
							iValue /= (iPathTurns + 1);
							if (iValue > iBestValue)
							{
								iBestValue = iValue;
								pBestPlot = &getPathEndTurnPlot();
								pBestAssaultPlot = pLoopCity->plot();
							}
						}
					}
				}
			}
		}
	}

	if (pBestPlot != NULL && pBestAssaultPlot != NULL)
		return AI_transportGoTo(*pBestPlot, *pBestAssaultPlot, eFlags, MISSIONAI_REINFORCE);

	return false;
}

// K-Mod. General function for moving assault groups - to reduce code duplication.
bool CvUnitAI::AI_transportGoTo(CvPlot const& kEndTurnPlot, CvPlot const& kTargetPlot,
	MovementFlags eFlags, MissionAITypes eMissionAI)
{
	FAssert(!kEndTurnPlot.isImpassable());
	CvPlot const* pNewEndTurnPlot = &kEndTurnPlot; // advc (Take param by reference)

	if (AI_getGroup()->AI_getMissionAIType() != eMissionAI)
	{
		// Cancel missions of all those coming to join departing transport
		CvPlayerAI& kOwner = GET_PLAYER(getOwner());
		FOR_EACH_GROUPAI_VAR(pLoopGroup, kOwner)
		{
			if (pLoopGroup != getGroup())
			{
				if (pLoopGroup->AI_getMissionAIType() == MISSIONAI_GROUP)
				{
					CvUnit* pMissionUnit = pLoopGroup->AI_getMissionAIUnit();
					if (pMissionUnit && pMissionUnit->getGroup() == getGroup() &&
						!pLoopGroup->isFull())
					{
						pLoopGroup->clearMissionQueue();
						pLoopGroup->AI_setMissionAI(NO_MISSIONAI, NULL, NULL);
					}
				}
			}
		}
	}

	if (at(kTargetPlot))
	{
		getGroup()->unloadAll(); // XXX is this dangerous (not pushing a mission...) XXX air units?
		getGroup()->setActivityType(ACTIVITY_AWAKE); // K-Mod
		return true;
	}
	else
	{
		if (getGroup()->isAmphibPlot(&kTargetPlot) ||
			/*  advc.306: Allow Barbarians to unload in their own cities when
				they're unable to reach any civs. */
			(isBarbarian() && AI_getUnitAIType() == UNITAI_ATTACK_SEA))
		{
			/*	If target is actually an amphibious landing from pEndTurnPlot,
				then set pEndTurnPlot = pTargetPlot so that we can land this turn. */
			if (&kTargetPlot != pNewEndTurnPlot &&
				stepDistance(&kTargetPlot, &kEndTurnPlot) == 1)
			{
				pNewEndTurnPlot = &kTargetPlot;
			}

			// if our cargo isn't going to be ready to land, just wait.
			if (&kTargetPlot == pNewEndTurnPlot && !getGroup()->canCargoAllMove())
			{
				getGroup()->pushMission(MISSION_SKIP, -1, -1,
						eFlags, false, false, eMissionAI, &kTargetPlot);
				return true;
			}
		}

		/*	declare war if we need to.
			(Note: AI_considerPathDOW checks for the declare war flag.) */
		if (AI_considerPathDOW(*pNewEndTurnPlot, eFlags))
		{	// <advc.163>
			if(!canMove())
				return true; // </advc.163>
			if (!generatePath(kTargetPlot, eFlags, false))
				return false;
			pNewEndTurnPlot = &getPathEndTurnPlot();
		}

		/*	Group all moveable land units together before landing. This will
			help the AI to think more clearly about attacking on the next turn. */
		if (pNewEndTurnPlot == &kTargetPlot &&
			!kTargetPlot.isWater() && !kTargetPlot.isCity())
		{
			CvSelectionGroup* pCargoGroup = NULL;
			FOR_EACH_UNIT_VAR_IN(pLoopUnit, *getGroup())
			{
				std::vector<CvUnit*> apCargoUnits;
				pLoopUnit->getCargoUnits(apCargoUnits);
				for (size_t i = 0; i < apCargoUnits.size(); i++)
				{
					if (apCargoUnits[i]->getGroup() != pCargoGroup &&
						apCargoUnits[i]->getDomainType() == DOMAIN_LAND &&
						apCargoUnits[i]->canMove())
					{
						if (pCargoGroup != NULL)
							apCargoUnits[i]->joinGroup(pCargoGroup);
						else
						{
							if (!apCargoUnits[i]->getGroup()->canAllMove())
							{
								// separate from units that can't move
								apCargoUnits[i]->joinGroup(NULL);
							}
							pCargoGroup = apCargoUnits[i]->getGroup();
						}
					}
				}
			}
		}
		//
		pushGroupMoveTo(*pNewEndTurnPlot, eFlags, false, false,
				eMissionAI, &kTargetPlot);
		return true;
	}
}


bool CvUnitAI::AI_settlerSeaTransport()
{
	PROFILE_FUNC();

	FAssert(getCargo() > 0);
	FAssert(getUnitAICargo(UNITAI_SETTLE) > 0);

	if (!getGroup()->canCargoAllMove())
		return false;

	/*	New logic should allow some new tricks like
		unloading settlers when a better site opens up locally
		and delivering settlers	to inland sites */

	FAssertMsg(getPlot().waterArea() != NULL, "Ship out of water?");
	CvUnit const* pSettlerUnit = NULL;
	FOR_EACH_UNIT_IN(pLoopUnit, getPlot())
	{
		if (pLoopUnit->getTransportUnit() == this &&
			pLoopUnit->AI_getUnitAIType() == UNITAI_SETTLE)
		{
			pSettlerUnit = pLoopUnit;
			break;
		}
	}

	FAssert(pSettlerUnit != NULL);

	int iAreaBestFoundValue = 0;
	CvPlot* pAreaBestPlot = NULL;

	int iOtherAreaBestFoundValue = 0;
	CvPlot* pOtherAreaBestPlot = NULL;

	//GroupPathFinder landPath;
	GroupPathFinder& landPath = CvSelectionGroup::getClearPathFinder(); // advc.opt
	landPath.setGroup(*pSettlerUnit->getGroup(), MOVE_SAFE_TERRITORY);

	for (int i = 0; i < GET_PLAYER(getOwner()).AI_getNumCitySites(); i++)
	{
		CvPlot& kCitySitePlot = GET_PLAYER(getOwner()).AI_getCitySite(i);
		if (!GET_PLAYER(getOwner()).AI_isAnyPlotTargetMissionAI(
			kCitySitePlot, MISSIONAI_FOUND, getGroup()))
		{
			int iValue = kCitySitePlot.getFoundValue(getOwner());
			if (kCitySitePlot.isArea(getArea()) &&
				landPath.generatePath(kCitySitePlot)) // K-Mod
			{
				if (iValue > iAreaBestFoundValue)
				{
					iAreaBestFoundValue = iValue;
					pAreaBestPlot = &kCitySitePlot;
				}
			}
			else
			{
				if (iValue > iOtherAreaBestFoundValue)
				{
					iOtherAreaBestFoundValue = iValue;
					pOtherAreaBestPlot = &kCitySitePlot;
				}
			}
		}
	}
	if (iAreaBestFoundValue == 0 && iOtherAreaBestFoundValue == 0)
		return false;

	if (iAreaBestFoundValue > iOtherAreaBestFoundValue)
	{
		//let the settler walk.
		getGroup()->unloadAll();
		getGroup()->pushMission(MISSION_SKIP);
		return true;
	}
	{ // advc: scope for pBest...
		CvPlot const* pBestPlot = NULL;
		CvPlot const* pBestFoundPlot = NULL;
		int iBestValue = 0;
		for (int i = 0; i < GET_PLAYER(getOwner()).AI_getNumCitySites(); i++)
		{
			CvPlot& kCitySitePlot = GET_PLAYER(getOwner()).AI_getCitySite(i);
			if (!kCitySitePlot.isVisibleEnemyUnit(this) &&
				!GET_PLAYER(getOwner()).AI_isAnyPlotTargetMissionAI(
				kCitySitePlot, MISSIONAI_FOUND, getGroup(), 4))
			{
				int iPathTurns;
				/*	BBAI TODO: Nearby plots too if much shorter (settler walk from there)
					also, if plots are in an area where player already has cities,
					then may not be coastal ... (see Earth 1000 AD map for Inca) */
				if (generatePath(kCitySitePlot, NO_MOVEMENT_FLAGS, true, &iPathTurns))
				{
					int iValue = kCitySitePlot.getFoundValue(getOwner());
					iValue *= 1000;
					iValue /= (2 + iPathTurns);
					if (iValue > iBestValue)
					{
						iBestValue = iValue;
						pBestPlot = &getPathEndTurnPlot();
						pBestFoundPlot = &kCitySitePlot;
					}
				}
			}
		}

		if (pBestPlot != NULL && pBestFoundPlot != NULL)
		{
			FAssert(!pBestPlot->isImpassable());

            // doc: opportunistically load defenders or workers
		    if (!isFull() &&
                getCivilizationType() != AMERICA) // doc: pioneer can defend and generates workers
		    {
		        if (getUnitAICargo(UNITAI_CITY_DEFENSE) == 0 && pBestFoundPlot->area()->getNumOwnedTiles() > 0)
		        {
		            return false;
		        }

		        if (getUnitAICargo(UNITAI_WORKER) == 0 && pBestFoundPlot->area()->getNumAIUnits(getOwner(), UNITAI_WORKER) < pBestFoundPlot->area()->getCitiesPerPlayer(getOwner()))
		        {
		            return false;
		        }
		    }

			if (pBestPlot == pBestFoundPlot || stepDistance(pBestPlot, pBestFoundPlot) == 1)
			{
				if (at(*pBestFoundPlot))
				{
					unloadAll(); // XXX is this dangerous (not pushing a mission...) XXX air units?
					getGroup()->setActivityType(ACTIVITY_AWAKE); // K-Mod
					return true;
				}
				else
				{
					pushGroupMoveTo(*pBestFoundPlot, NO_MOVEMENT_FLAGS, false, false,
							MISSIONAI_FOUND, pBestFoundPlot);
					return true;
				}
			}
			else
			{
				pushGroupMoveTo(*pBestPlot, NO_MOVEMENT_FLAGS, false, false,
						MISSIONAI_FOUND, pBestFoundPlot);
				return true;
			}
		}
	}
	/*	Try original logic
		(sometimes new logic breaks) */
	CvPlot const* pBestPlot = NULL;
	CvPlot const* pBestFoundPlot = NULL;
	int iMinFoundValue = GET_PLAYER(getOwner()).AI_getMinFoundValue();
	int iBestValue = 0;
	for (int i = 0; i < GC.getMap().numPlots(); i++)
	{
		CvPlot const& kLoopPlot = GC.getMap().getPlotByIndex(i);

		//if (pLoopPlot->isCoastalLand())
		/*	K-Mod. Only consider areas we have explored,
			and only land if we know there is something we want to settle. */
		int iAreaBest; // (currently unused)
		if (kLoopPlot.isCoastalLand() && kLoopPlot.isRevealed(getTeam()) &&
			GET_PLAYER(getOwner()).AI_getNumAreaCitySites(kLoopPlot.getArea(), iAreaBest) > 0)
		// K-Mod end
		{
			int iValue = kLoopPlot.getFoundValue(getOwner());
			if (iValue > iBestValue && iValue >= iMinFoundValue)
			{
				bool bValid = false;
				FOR_EACH_UNIT_IN(pLoopUnit, getPlot())
				{
					if (pLoopUnit->getTransportUnit() == this &&
						pLoopUnit->canFound(&kLoopPlot))
					{
						bValid = true;
						break;
					}
				}
				if (bValid)
				{
					if (!kLoopPlot.isVisibleEnemyUnit(this) &&
						!GET_PLAYER(getOwner()).AI_isAnyPlotTargetMissionAI(
						kLoopPlot, MISSIONAI_FOUND, getGroup(), 4) &&
						generatePath(kLoopPlot, NO_MOVEMENT_FLAGS, true))
					{
						iBestValue = iValue;
						pBestPlot = &getPathEndTurnPlot();
						pBestFoundPlot = &kLoopPlot;
					}
				}
			}
		}
	}

	if (pBestPlot != NULL && pBestFoundPlot != NULL)
	{
		FAssert(!pBestPlot->isImpassable());

        // doc: wait for defender or worker, unless city site is on small island
	    if (pBestFoundPlot->area()->getNumTiles() > 1)
	    {
	        if ((getUnitAICargo(UNITAI_CITY_DEFENSE) == 0 || getUnitAICargo(UNITAI_WORKER) == 0) &&
                getCivilizationType() != AMERICA) // doc: pioneer can defend itself and generates workers
	            return false;
	    }

		if (pBestPlot == pBestFoundPlot ||
			stepDistance(pBestPlot->getX(), pBestPlot->getY(),
			pBestFoundPlot->getX(), pBestFoundPlot->getY()) == 1)
		{
			if (at(*pBestFoundPlot))
			{
				unloadAll(); // XXX is this dangerous (not pushing a mission...) XXX air units?
				getGroup()->setActivityType(ACTIVITY_AWAKE); // K-Mod
				return true;
			}
			else
			{
				pushGroupMoveTo(*pBestFoundPlot, NO_MOVEMENT_FLAGS, false, false,
						MISSIONAI_FOUND, pBestFoundPlot);
				return true;
			}
		}
		else
		{
			pushGroupMoveTo(*pBestPlot, NO_MOVEMENT_FLAGS, false, false,
					MISSIONAI_FOUND, pBestFoundPlot);
			return true;
		}
	}
	return false;
}

/*  advc: Renamed. This function is currently only used by UNITAI_SETTLER_SEA,
	but "AI_settlerSeaFerry" is still a misleading name for a function that transports
	only workers. */
bool CvUnitAI::AI_ferryWorkers()
{
	PROFILE_FUNC();

	FAssert(getCargo() > 0);
	int iWorkers = getUnitAICargo(UNITAI_WORKER); // advc.113
	FAssert(iWorkers > 0);

	if (!getGroup()->canCargoAllMove())
		return false;

	/*CvArea* pWaterArea = getPlot().waterArea(); // advc: unused, always was.
	FAssertMsg(pWaterArea != NULL, "Ship out of water?");*/
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());

	int iBestValue = 0;
	CvPlot* pBestPlot = NULL;
	FOR_EACH_CITYAI(pLoopCity, kOwner)
	{	// <advc> Be explicit about this. May also save the pathfinder time.
		if (!pLoopCity->isCoastal())
			continue; // </advc>

		//int iValue = pLoopCity->AI_getWorkersNeeded();
		/*  <advc.113b> Tagging advc.001 b/c disregarding the available workers
			entirely is probably a bug */
		int iHave = pLoopCity->AI_getWorkersHave();
		/*  If this transport is headed for pLoopCity, then the workers onboard
			are already counted by AI_getWorkersHave. (Tbd.: Check plotDistance
			here as in CvCityAI::AI_updateWorkersHaveAndNeeded?) */
		CvPlot* pOldMissionPlot = AI_getGroup()->AI_getMissionAIPlot();
		if (pOldMissionPlot != NULL && pOldMissionPlot == pLoopCity->plot())
			iHave -= iWorkers;
		int iValue = pLoopCity->AI_getWorkersNeeded() - (2 * iHave + 1) / 3;
		// </advc.113b>
		if (iValue <= 0)
			continue;

		iValue -= kOwner.AI_plotTargetMissionAIs(
				pLoopCity->getPlot(), MISSIONAI_FOUND, getGroup());
		if (iValue <= 0)
			continue;

		int iPathTurns;
		if (!generatePath(pLoopCity->getPlot(), NO_MOVEMENT_FLAGS, true, &iPathTurns))
			continue;

		int iAreaHave = kOwner.AI_totalAreaUnitAIs(pLoopCity->getArea(), UNITAI_WORKER);
		// <advc.113> Don't count the workers in cargo as available
		if (!getPlot().isWater() && pLoopCity->isArea(getArea()))
		{
			iAreaHave -= (2 * iWorkers) / 3;
			FAssert(iAreaHave >= 0);
		} // </advc.113>
		iValue += std::max(0, kOwner.AI_neededWorkers(pLoopCity->getArea()) - iAreaHave);
		iValue *= 1000;
		iValue /= 4 + iPathTurns;
		if (atPlot(pLoopCity->plot()))
			iValue += 100;
		else iValue += SyncRandNum(100);
		if (iValue > iBestValue)
		{
			iBestValue = iValue;
			pBestPlot = pLoopCity->plot();
		}
	}
	// <advc.040>
	// Need a handle to a Worker so we can check if any improvement can actually be built
	CvUnit* pWorker = NULL;
	std::vector<CvUnit*> aCargoUnits;
	getCargoUnits(aCargoUnits);
	for (size_t i = 0; i < aCargoUnits.size(); i++)
	{
		if (aCargoUnits[i]->AI_getUnitAIType() == UNITAI_WORKER)
		{
			pWorker = aCargoUnits[i];
			break;
		}
	}
	FAssert(pWorker != NULL);
	if (iBestValue < 500 && pWorker != NULL)
	{
		CvCity* pCurrentCity = getPlot().getPlotCity();
		CvUnitAI const& kWorker = pWorker->AI();
		scaled const rOwnerAIEraFactor = kOwner.AI_getCurrEraFactor();
		CvMap const& kMap = GC.getMap();
		for (int i = 0; i < kMap.numPlots(); i++)
		{
			CvPlot& kPlot = kMap.getPlotByIndex(i);
			if(kPlot.isWater() || kPlot.getOwner() != kOwner.getID())
				continue;
			CvCityAI* pWorkingCity = NULL;
			if (kPlot.getArea().getCitiesPerPlayer(kOwner.getID()) > 0 ||
				kOwner.AI_neededWorkers(kPlot.getArea()) <= 0 ||
				kOwner.AI_totalAreaUnitAIs(kPlot.getArea(), UNITAI_WORKER) > 0)
			{
				/*  A colony that is able to work tiles on the mainland will
					have to ship Workers b/c the mainland Workers aren't going
					to take care of those tiles. */
				bool bValid = (pCurrentCity != NULL && !kPlot.isArea(getArea()));
				if (bValid)
				{
					pWorkingCity = kPlot.AI_getWorkingCity();
					if (kPlot.getWorkingCity() != pCurrentCity)
						bValid = false;
				}
				if (!bValid)
					continue;
			}
			if (pWorkingCity == NULL)
				pWorkingCity = kPlot.AI_getWorkingCity();
			BonusTypes eBonus = kPlot.getNonObsoleteBonusType(kOwner.getTeam());
			if (pWorkingCity == NULL && eBonus == NO_BONUS)
				continue;
			// Do a computation similar to CvCityAI::AI_neededWorkers on the fly
			ImprovementTypes eImpr = kPlot.getImprovementType();
			// Don't bother sending a Worker if there's already a good improvement
			if (eImpr != NO_IMPROVEMENT && (eBonus == NO_BONUS ||
					kOwner.doesImprovementConnectBonus(eImpr, eBonus)))
				continue;
			if (pWorkingCity != NULL)
			{
				BuildTypes eBestBuild = pWorkingCity->AI_getBestBuild(pWorkingCity->
						getCityPlotIndex(kPlot));
				if (eBestBuild == NO_BUILD || !kWorker.canBuild(kPlot, eBestBuild))
					continue;
				ImprovementTypes eBestImpr = GC.getInfo(eBestBuild).getImprovement();
				if (eBestImpr == NO_IMPROVEMENT) // Don't go there just to chop
					continue;
				// Not going to build forts on workable tiles
				if (GC.getInfo(eBestImpr).isActsAsCity())
					continue;
			}
			else
			{
				bool bValid = false;
				for (int j = 0; j < GC.getNumBuildInfos(); j++)
				{
					BuildTypes eBuild = (BuildTypes)j;
					if (kWorker.AI_canConnectBonus(kPlot, eBuild))
					{
						bValid = true;
						break;
					}
				}
				if(!bValid)
					continue;
			}
			int iValue = 0;
			if (kPlot.getBonusType() != NO_BONUS) // Could be obsolete
			{
				iValue++;
				if(eBonus != NO_BONUS) // Non-obsolete
					iValue++;
			}
			if (pWorkingCity != NULL) // Can be worked
			{
				iValue++;
				if (kPlot.isBeingWorked())
					iValue++;
			}
			FAssert(iValue > 0);
			// Akin to the city loop above
			int iPathTurns;
			if (!generatePath(kPlot, NO_MOVEMENT_FLAGS, true, &iPathTurns, 8))
				continue;
			// Check this last b/c it goes through all selection groups
			if (kOwner.AI_isAnyAreaMissionAI(kPlot.getArea(), MISSIONAI_FOUND, getGroup()))
				continue;
			/*  For cities, it's 4+... in the divisor. 1 extra to deprioritize islands.
				(Or we could say it's the extra turn for unloading outside a city.) */
			iValue = (1000 * iValue) / (5 + iPathTurns);
			iValue += SyncRandNum(65 + (40 * rOwnerAIEraFactor).round());
 			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				pBestPlot = &kPlot;
			}
		}
	} // </advc.040>

	if (pBestPlot != NULL)
	{
		if (atPlot(pBestPlot))
		{
			unloadAll(); // XXX is this dangerous (not pushing a mission...) XXX air units?
			getGroup()->setActivityType(ACTIVITY_AWAKE); // K-Mod
			return true;
		}
		else
		{	// <advc.040> Unload all but 1 Worker before going to an island
			if(!pBestPlot->isCity())
			{
				int iWorkersFound = 0;
				for(size_t i = 0; i < aCargoUnits.size(); i++)
				{
					if(aCargoUnits[i]->AI_getUnitAIType() == UNITAI_WORKER)
					{
						iWorkersFound++;
						if(iWorkersFound > 1)
							aCargoUnits[i]->unload();
					}
					else aCargoUnits[i]->unload();
				}
			} // </advc.040>
			pushGroupMoveTo(*pBestPlot, NO_MOVEMENT_FLAGS, false, false,
					MISSIONAI_FOUND, pBestPlot);
			return true;
		}
	}
	return false;
}


bool CvUnitAI::AI_specialSeaTransportMissionary()
{
	//PROFILE_FUNC();
	FAssert(getCargo() > 0);
	FAssert(getUnitAICargo(UNITAI_MISSIONARY) > 0);

	if (!getGroup()->canCargoAllMove())
		return false;

	bool bExecutive = false;
	CvUnit const* pMissionaryUnit = NULL;
	FOR_EACH_UNIT_IN(pLoopUnit, getPlot())
	{
		if (pLoopUnit->getTransportUnit() == this &&
			pLoopUnit->AI_getUnitAIType() == UNITAI_MISSIONARY)
		{
			pMissionaryUnit = pLoopUnit;
			break;
		}
	}
	if (pMissionaryUnit == NULL)
		return false;

	CvPlot const* pBestPlot = NULL;
	CvPlot const* pBestSpreadPlot = NULL;
	int iBestValue = 0;
	// XXX what about non-coastal cities?
	for (int i = 0; i < GC.getMap().numPlots(); i++)
	{
		CvPlot const& kLoopPlot = GC.getMap().getPlotByIndex(i);

		if (!kLoopPlot.isCoastalLand(/* advc.opt: */ -1))
			continue;

		CvCity* pCity = kLoopPlot.getPlotCity();
		if (pCity == NULL)
			continue;

		int iValue = 0;
		int iCorpValue = 0;
		FOR_EACH_ENUM(Religion)
		{
			if (pMissionaryUnit->canSpread(&kLoopPlot, eLoopReligion))
			{
				if (GET_PLAYER(getOwner()).getStateReligion() == eLoopReligion)
					iValue += 3;
				if (GET_PLAYER(getOwner()).hasHolyCity(eLoopReligion))
					iValue++;
			}
		}
		FOR_EACH_ENUM2(Corporation, eLoopCorp)
		{
			if (pMissionaryUnit->canSpreadCorporation(&kLoopPlot, eLoopCorp) &&
				GET_PLAYER(getOwner()).hasHeadquarters(eLoopCorp))
			{
				iCorpValue += 3;
			}
		}

		if (iValue > 0)
		{
			if (!kLoopPlot.isVisibleEnemyUnit(this) &&
				!GET_PLAYER(getOwner()).AI_isAnyPlotTargetMissionAI(
				kLoopPlot, MISSIONAI_SPREAD, getGroup()))
			{
				int iPathTurns;
				if (generatePath(kLoopPlot, NO_MOVEMENT_FLAGS, true, &iPathTurns))
				{
					iValue *= pCity->getPopulation();
					if (pCity->getOwner() == getOwner())
						iValue *= 4;
					else if (pCity->getTeam() == getTeam())
						iValue *= 3;
					if (pCity->getReligionCount() == 0)
						iValue *= 2;
					iValue /= (pCity->getReligionCount() + 1);

					FAssert(iPathTurns > 0);
					if (iPathTurns == 1)
						iValue *= 2;

					iValue *= 1000;
					iValue /= (iPathTurns + 1);
					if (iValue > iBestValue)
					{
						iBestValue = iValue;
						pBestPlot = &getPathEndTurnPlot();
						pBestSpreadPlot = &kLoopPlot;
						bExecutive = false;
					}
				}
			}
		}

		if (iCorpValue > 0 && !kLoopPlot.isVisibleEnemyUnit(this) &&
			!GET_PLAYER(getOwner()).AI_isAnyPlotTargetMissionAI(
			kLoopPlot, MISSIONAI_SPREAD_CORPORATION, getGroup()))
		{
			int iPathTurns;
			if (generatePath(kLoopPlot, NO_MOVEMENT_FLAGS, true, &iPathTurns))
			{
				iCorpValue *= pCity->getPopulation();
				FAssert(iPathTurns > 0);
				if (iPathTurns == 1)
				{
					//iValue *= 2;
					// UNOFFICIAL_PATCH, Bugfix, 02/22/10, jdog5000:
					iCorpValue *= 2;
				}
				iCorpValue *= 1000;
				iCorpValue /= (iPathTurns + 1);
				if (iCorpValue > iBestValue)
				{
					iBestValue = iCorpValue;
					pBestPlot = &getPathEndTurnPlot();
					pBestSpreadPlot = &kLoopPlot;
					bExecutive = true;
				}
			}
		}
	}

	if (pBestPlot != NULL && pBestSpreadPlot != NULL)
	{
		FAssert(!pBestPlot->isImpassable() || canMoveImpassable());
		if (pBestPlot == pBestSpreadPlot || ::stepDistance(pBestPlot, pBestSpreadPlot) == 1)
		{
			if (at(*pBestSpreadPlot))
			{
				unloadAll(); // XXX is this dangerous (not pushing a mission...) XXX air units?
				getGroup()->setActivityType(ACTIVITY_AWAKE); // K-Mod
				return true;
			}
			else
			{
				pushGroupMoveTo(*pBestSpreadPlot, NO_MOVEMENT_FLAGS, false, false,
						bExecutive ? MISSIONAI_SPREAD_CORPORATION : MISSIONAI_SPREAD,
						pBestSpreadPlot);
				return true;
			}
		}
		else
		{
			pushGroupMoveTo(*pBestPlot, NO_MOVEMENT_FLAGS, false, false,
					bExecutive ? MISSIONAI_SPREAD_CORPORATION : MISSIONAI_SPREAD,
					pBestSpreadPlot);
			return true;
		}
	}

	return false;
}

// The body of this function has been completely deleted and rewritten for K-Mod
bool CvUnitAI::AI_specialSeaTransportSpy()
{
	CvTeamAI const& kOurTeam = GET_TEAM(getTeam());
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());

	int const iTotalPoints = kOurTeam.getTotalUnspentEspionage();

	EagerEnumMap<PlayerTypes,int> aiBaseValue;
	PlayerTypes eBestTarget = NO_PLAYER;
	int iBestValue = 0;
	// advc.opt: Exclude dead teams
	for (PlayerAIIter<CIV_ALIVE,OTHER_KNOWN_TO> it(getTeam()); it.hasNext(); ++it)
	{
		CvPlayerAI const& kTarget = *it;

		int iValue = 1000 * kOurTeam.getEspionagePointsAgainstTeam(kTarget.getTeam()) /
				std::max(1, iTotalPoints);

		if (kOwner.AI_isMaliciousEspionageTarget(kTarget.getID()))
			iValue = 3*iValue/2;

		if (kOurTeam.isAtWar(kTarget.getTeam()) &&
				!isInvisible(kTarget.getTeam(), false))
			iValue /= 3; // it might be too risky.

		if (kOurTeam.AI_hasCitiesInPrimaryArea(kTarget.getTeam()))
			iValue /= 6;

		iValue *= 100 - /* advc.003n: */ (kTarget.isMinorCiv() ? 0 :
				kOurTeam.AI_getAttitudeWeight(kTarget.getTeam()) / 2);
		// of order 1000 * percentage of espionage. (~20000)
		aiBaseValue.set(kTarget.getID(), iValue);
		if (iValue > iBestValue)
		{
			iBestValue = iValue;
			eBestTarget = kTarget.getID();
		}
	}

	if (eBestTarget == NO_PLAYER)
		return false;

	CvPlot const* pTargetPlot = 0;
	CvPlot const* pEndTurnPlot = 0;
	iBestValue = 0; // was best player value, now it is best plot value
	for (int i = 0; i < GC.getMap().numPlots(); i++)
	{
		CvPlot const& kPlot = GC.getMap().getPlotByIndex(i);
		PlayerTypes const ePlotOwner = kPlot.getRevealedOwner(getTeam());

		/*	only consider coast plots, owned by civ teams,
			with base value greater than the current best */
		if (ePlotOwner == NO_PLAYER || ePlotOwner >= MAX_CIV_PLAYERS ||
			!kPlot.isCoastalLand(/* advc.opt: */ -1) ||
			iBestValue >= aiBaseValue.get(ePlotOwner) ||
			kPlot.getArea().getCitiesPerPlayer(ePlotOwner) == 0)
		{
			continue;
		}
		//FAssert(pLoopPlot->isRevealed(getTeam(), false)); // otherwise, how do we have a revealed owner?
		/*	^Actually, the owner gets revealed when any of the adjacent plots are visable -
			so this assert is not always true. I think it's fair to consider this plot anyway. */

		int iValue = aiBaseValue.get(ePlotOwner);

		iValue *= 2;
		iValue /= 2 + kOwner.AI_totalAreaUnitAIs(kPlot.getArea(), UNITAI_SPY);

		CvCity* pPlotCity = kPlot.getPlotCity();
		if (pPlotCity && !kOurTeam.isAtWar(GET_PLAYER(ePlotOwner).getTeam())) // don't go directly to cities if we are at war.
		{
			iValue *= 100;
			iValue /= std::max(100, 3 * kOwner.getEspionageMissionCostModifier(NO_ESPIONAGEMISSION, ePlotOwner, &kPlot));
		}
		else iValue /= 5;

		if (GET_PLAYER(ePlotOwner).AI_atVictoryStage4() &&
			!GET_PLAYER(ePlotOwner).AI_isPrimaryArea(kPlot.getArea()))
		{
			iValue /= 4;
		}

		FAssert(iValue <= aiBaseValue.get(ePlotOwner));
		int iPathTurns;
		if (iValue > iBestValue &&
			generatePath(kPlot, NO_MOVEMENT_FLAGS, true, &iPathTurns))
		{
			iValue *= 10;
			iValue /= 3 + iPathTurns;
			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				pTargetPlot = &kPlot;
				pEndTurnPlot = &getPathEndTurnPlot();
			}
		}
	}

	if (pTargetPlot != NULL)
	{
		if (atPlot(pTargetPlot))
		{
			getGroup()->unloadAll();
			getGroup()->setActivityType(ACTIVITY_AWAKE);
			// no actual mission pushed, but we need to rethink our next move.
			return true;
		}
		else
		{
			// (without this, we could get into an infinite loop when the cargo isn't ready to move)
			if (canMoveInto(*pEndTurnPlot) || getGroup()->canCargoAllMove())
			{
				if (gUnitLogLevel > 2 && pTargetPlot->getOwner() != NO_PLAYER && generatePath(*pTargetPlot, NO_MOVEMENT_FLAGS, true, NULL, 1))
				{
					logBBAI("      %S lands sea-spy in %S territory. (%d percent of unspent points)", // apparently it's impossible to actually use a % sign in this Microsoft version of vsnprintf. madness
						kOurTeam.getName().GetCString(), GET_PLAYER(pTargetPlot->getOwner()).getCivilizationDescription(0), kOurTeam.getEspionagePointsAgainstTeam(pTargetPlot->getTeam())*100/iTotalPoints);
				}
				pushGroupMoveTo(*pEndTurnPlot, NO_MOVEMENT_FLAGS,
						false, false, MISSIONAI_ATTACK_SPY, pTargetPlot);
				return true;
			}
			else
			{
				// need to wait for our cargo to be ready
				getGroup()->pushMission(MISSION_SKIP, -1, -1, NO_MOVEMENT_FLAGS,
						false, false, MISSIONAI_ATTACK_SPY, pTargetPlot);
				return true;
			}
		}
	}
	return false;
}


bool CvUnitAI::AI_carrierSeaTransport()
{
	PROFILE_FUNC();

	int iMaxAirRange = 0;
	{
		std::vector<CvUnit*> apCargoUnits;
		getCargoUnits(apCargoUnits);
		for (size_t i = 0; i < apCargoUnits.size(); ++i)
			iMaxAirRange = std::max(iMaxAirRange, apCargoUnits[i]->airRange());
	}
	if (iMaxAirRange == 0)
		return false;

	CvPlot const* pBestPlot = NULL;
	CvPlot const* pBestCarrierPlot = NULL;
	int iBestValue = 0;
	// BETTER_BTS_AI_MOD, Naval AI, War tactics, Efficiency, 02/22/10, jdog5000: START
	for (int i = 0; i < GC.getMap().numPlots(); i++)
	{
		CvPlot const& kPlot = GC.getMap().getPlotByIndex(i);
		if (!AI_plotValid(kPlot) || !kPlot.isAdjacentToLand() ||
			kPlot.isVisibleEnemyUnit(this))
		{
			continue;
		}
		int iValue = 0;
		for (PlotCircleIter it(kPlot, iMaxAirRange); it.hasNext(); ++it)
		{
			CvPlot const& kAir = *it;
			int iAirDist = ::plotDistance(&kPlot, &kAir);
			if (!kAir.isBarbarian() && AI_mayAttack(kAir))
			{
				if (kAir.isCity())
				{
					iValue += 3;
					// BBAI: Support invasions
					iValue += (GET_PLAYER(getOwner()).AI_plotTargetMissionAIs(
							kAir, MISSIONAI_ASSAULT, getGroup(), 2) * 6);
				}
				if (kAir.isImproved())
					iValue += 2;
				if (iAirDist <= iMaxAirRange/2)
				{
					// BBAI: Support/air defense for land troops
					iValue += kAir.plotCount(PUF_canDefend, -1, -1, getOwner());
					// advc.001s (comment): Also counts ships, but I guess that's OK.
				}
			}
		}

		if (iValue > 0)
		{
			iValue *= 1000;
			FOR_EACH_ADJ_PLOT(kPlot)
			{
				if (pAdj->isCity() && isEnemy(pAdj->getTeam(), kPlot))
				{
					iValue /= 2;
					break;
				}
			}
			if (iValue > iBestValue)
			{
				bool bStealth = (getInvisibleType() != NO_INVISIBLE);
				if (GET_PLAYER(getOwner()).AI_plotTargetMissionAIs(
					kPlot, MISSIONAI_CARRIER, getGroup(), bStealth ? 5 : 3) <=
					(bStealth ? 0 : 3))
				{
					int iPathTurns;
					if (generatePath(kPlot, NO_MOVEMENT_FLAGS, true, &iPathTurns))
					{
						iValue /= (iPathTurns + 1);
						if (iValue > iBestValue)
						{
							iBestValue = iValue;
							pBestPlot = &getPathEndTurnPlot();
							pBestCarrierPlot = &kPlot;
						}
					}
				}
			}
		}
	} // BETTER_BTS_AI_MOD: END

	if (pBestPlot == NULL || pBestCarrierPlot == NULL)
		return false;

	if (atPlot(pBestCarrierPlot))
	{
		if (getGroup()->hasCargo())
		{
			int const iPlotUnits = getPlot().getNumUnits();
			for (int i = 0; i < iPlotUnits; ++i)
			{
				bool bDone = true;
				FOR_EACH_UNITAI_VAR_IN(pCargoUnit, getPlot())
				{
					if (!pCargoUnit->isCargo())
						continue;
					FAssert(pCargoUnit->getTransportUnit() != NULL);
					if (pCargoUnit->getOwner() == getOwner() &&
						pCargoUnit->getTransportUnit()->getGroup() == getGroup() &&
						pCargoUnit->getDomainType() == DOMAIN_AIR)
					{
						if (pCargoUnit->canMove() && pCargoUnit->isGroupHead())
						{
							// careful, this might kill the cargo group
							if (pCargoUnit->AI_getGroup()->AI_update())
							{
								bDone = false;
								break;
							}
						}
					}
				}
				if (bDone)
					break;
			}
		}
		if (canPlunder(*pBestCarrierPlot))
		{
			getGroup()->pushMission(MISSION_PLUNDER, -1, -1,
					NO_MOVEMENT_FLAGS, false, false,
					MISSIONAI_CARRIER, pBestCarrierPlot);
		}
		else getGroup()->pushMission(MISSION_SKIP);

		return true;
	}
	pushGroupMoveTo(*pBestPlot, NO_MOVEMENT_FLAGS, false, false,
			MISSIONAI_CARRIER, pBestCarrierPlot);
	return true;
}


bool CvUnitAI::AI_connectPlot(CvPlot const& kPlot, int iRange) // advc: 1st param was CvPlot*
{
	PROFILE_FUNC();

	FAssert(canBuildRoute());
	/*  BETTER_BTS_AI_MOD, Unit AI, Efficiency, 08/19/09, jdog5000: START
		BBAI efficiency: check area for land units before generating paths */
	/*if (getDomainType() == DOMAIN_LAND && !kPlot.isArea(getArea()) &&
		!getGroup()->canMoveAllTerrain())
	{
		return false;
	}*/ // advc.opt: Routes only exist on land. Caller should ensure same area.
	FAssert(kPlot.isArea(getArea()));

	if (!kPlot.isVisibleEnemyUnit(this))
	{
		if (!GET_PLAYER(getOwner()).AI_isAnyPlotTargetMissionAI(
			kPlot, MISSIONAI_BUILD, getGroup(), iRange) &&
			generatePath(kPlot, MOVE_SAFE_TERRITORY, true))
		{
			/* <advc.300> Barbarian behavior should just be to put roads on the
			  bonuses adjacent to their cities. */
			if(isBarbarian())
			{
				CvCity* c = kPlot.getWorkingCity();
				int iDummy;
				if(c == NULL || !at(kPlot) || kPlot.isConnectedTo(*c) ||
					/*	If Barbarians expand their borders somehow,
						then the city might not be adjacent. */
					!generatePath(c->getPlot(), MOVE_SAFE_TERRITORY, false, &iDummy, 2))
				{
					return false;
				}
				getGroup()->pushMission(MISSION_ROUTE_TO, c->getX(), c->getY(),
						MOVE_SAFE_TERRITORY, false, false, MISSIONAI_BUILD, &kPlot);
				return true;
			} // </advc.300>
			FOR_EACH_CITY(pLoopCity, GET_PLAYER(getOwner()))
			{
				if (!kPlot.isConnectedTo(*pLoopCity))
				{
					FAssert(kPlot.getPlotCity() != pLoopCity);
					if (getPlot().isSamePlotGroup(*pLoopCity->plot(), getOwner()))
					{
						getGroup()->pushMission(MISSION_ROUTE_TO, kPlot.getX(), kPlot.getY(),
								MOVE_SAFE_TERRITORY, false, false, MISSIONAI_BUILD, &kPlot);
						return true;
					}
				}
			}
			FOR_EACH_CITYAI(pLoopCity, GET_PLAYER(getOwner()))
			{
				/*  BETTER_BTS_AI_MOD, Unit AI, Efficiency, 08/19/09, jdog5000: START
					BBAI efficiency: check same area */
				if (!pLoopCity->isArea(kPlot.getArea()))
					continue;
				// BETTER_BTS_AI_MOD: END
				if (kPlot.isConnectedTo(*pLoopCity))
					continue;
				FAssert(kPlot.getPlotCity() != pLoopCity);
				//if (!pLoopCity->getPlot().isVisibleEnemyUnit(this)) { // advc.opt: It's our city
				// <advc.139>
				if (pLoopCity->AI_isEvacuating())
					continue; // </advc.139>
				if (generatePath(pLoopCity->getPlot(), MOVE_SAFE_TERRITORY, true))
				{
					if (at(kPlot)) // need to test before moving...
					{
						getGroup()->pushMission(MISSION_ROUTE_TO, pLoopCity->getX(), pLoopCity->getY(),
								MOVE_SAFE_TERRITORY, false, false, MISSIONAI_BUILD, &kPlot);
					}
					else
					{
						getGroup()->pushMission(MISSION_ROUTE_TO,
								pLoopCity->getX(), pLoopCity->getY(), MOVE_SAFE_TERRITORY,
								false, false, MISSIONAI_BUILD, &kPlot);
						getGroup()->pushMission(MISSION_ROUTE_TO,
								kPlot.getX(), kPlot.getY(), MOVE_SAFE_TERRITORY,
								true, false, MISSIONAI_BUILD, &kPlot); // K-Mod
					}
					return true;
				}
			}
		}
	}
	return false;
}

// advc: Cut from AI_improveCity to reduce code duplication
bool CvUnitAI::AI_shouldRouteWhileImproving(CvPlot const& kDest,
	MovementFlags& eFlags, // in-out param
	CvCity const* pDestCity) const
{
	bool bRoute = false;
	if (pDestCity != NULL && getPlot().getWorkingCity() != pDestCity /*||
		GC.getInfo(eBestBuild).getRoute() != NO_ROUTE*/) // advc.121: Walk don't route
	{
		bRoute = true;
	}
	else if (generatePath(kDest, eFlags, true) &&
		getPathFinder().getPathTurns() == 1 && getPathFinder().getFinalMoves() == 0)
	{
		if (kDest.isRoute())
			bRoute = true;
	}
	else if (!getPlot().isRoute())
	{
		int iPlotMoveCost = 0;
		iPlotMoveCost = (!getPlot().isFeature() ?
				GC.getInfo(getPlot().getTerrainType()).getMovementCost() :
				GC.getInfo(getPlot().getFeatureType()).getMovementCost());
		if (getPlot().isHills())
			iPlotMoveCost += GC.getDefineINT(CvGlobals::HILLS_EXTRA_MOVEMENT);
		if (iPlotMoveCost > 1)
			bRoute = true;
	}
	return (bRoute && AI_canRouteThroughSafeTerritory(kDest, eFlags));
}

// advc.pf: Don't route through foreign territory
bool CvUnitAI::AI_canRouteThroughSafeTerritory(CvPlot const& kDest,
	MovementFlags& eFlags) const // in-out param
{
	PROFILE_FUNC(); // (Should be just a few calls per turn or a few dozen)
	bool bRoute = true;
	int iOriginalPathTurns;
	generatePath(kDest, eFlags, true, &iOriginalPathTurns);
	int iPathTurns;
	if (!generatePath(kDest, eFlags | MOVE_SAFE_TERRITORY, false, &iPathTurns) ||
		iPathTurns > iOriginalPathTurns + 1)
	{
		bRoute = false;
	}
	else eFlags |= MOVE_SAFE_TERRITORY;
	return bRoute;
}


bool CvUnitAI::AI_improveCity(CvCityAI const& kCity)
{
	PROFILE_FUNC();

	CvPlot* pBestPlot=NULL;
	BuildTypes eBestBuild=NO_BUILD;
	if (!AI_bestCityBuild(kCity, &pBestPlot, &eBestBuild, NULL, this))
		return false; // advc
	FAssert(pBestPlot != NULL);
	FAssertEnumBounds(eBestBuild);
	MovementFlags eFlags = NO_MOVEMENT_FLAGS; // advc.pf
	// <advc> Moved into helper function
	MissionTypes eMission = (AI_shouldRouteWhileImproving(*pBestPlot, eFlags, &kCity) ?
			MISSION_ROUTE_TO : MISSION_MOVE_TO); // </advc>
	getGroup()->pushMission(eMission,
			pBestPlot->getX(), pBestPlot->getY(),
			eFlags, false, false,
			MISSIONAI_BUILD, pBestPlot);
	eBestBuild = AI_betterPlotBuild(*pBestPlot, eBestBuild);
	getGroup()->pushMission(MISSION_BUILD,
			eBestBuild, -1,
			eFlags, /*(getGroup()->getLengthMissionQueue() > 0)*/ true, // K-Mod
			false, MISSIONAI_BUILD, pBestPlot);
	return true;
}


bool CvUnitAI::AI_improveLocalPlot(int iRange, CvCity const* pIgnoreCity,
	int iMissingWorkersInArea) // advc.117
{
	PROFILE_FUNC();

	CvPlot* pBestPlot = NULL;
	BuildTypes eBestBuild = NO_BUILD;
	bool bChop = false; // advc.117
	int iBestValue = 0;
	for (SquareIter it(*this, iRange); it.hasNext(); ++it)
	{
		CvPlot& p = *it;
		if (/*!AI_plotValid(p)*/!isArea(p.getArea())) // advc.opt
			continue;
		// <advc.117> Chop plots outside of city radii
		int iValue = 0;
		CvPlayerAI& kOwner = GET_PLAYER(getOwner());
		if (!p.isCityRadius() && p.getWorkingCity() == NULL &&
			!isBarbarian() && iMissingWorkersInArea <= 0 &&
			!kOwner.isHumanOption(PLAYEROPTION_LEAVE_FORESTS) &&
			kOwner.getGwPercentAnger() <= 0 &&
			!p.isImproved() && p.isFeature() &&
			!kOwner.AI_isAdjacentCitySite(p, false)) // Don't chop near planned cities
		{
			FOR_EACH_ENUM(Build)
			{
				CvBuildInfo const& kBuild = GC.getInfo(eLoopBuild);
				if (kBuild.getImprovement() != NO_IMPROVEMENT)
					continue;
				iValue = kBuild.getFeatureProduction(p.getFeatureType());
				if (iValue <= iBestValue)
					continue;
				if (!canBuild(p, eLoopBuild)) // (advc.opt: moved down)
					continue;
				int iPathTurns;
				if (generatePath(p, NO_MOVEMENT_FLAGS, true, &iPathTurns, 5))
				{	/*  Doesn't need to be on the same scale as non-chop values;
						only want to chop when there is nothing else to do. */
					iBestValue = (iValue * 100) / (1 + iPathTurns);
					eBestBuild = eLoopBuild;
					pBestPlot = &p;
					bChop = true;
					break;
				}
			}
			if(bChop)
				continue;
		} // </advc.117>
		// K-Mod note: I've turn the all-encompassing if blocks into !if continues.
		if (!p.isCityRadius())
			continue;

		CvCityAI const* pCity = p.AI_getWorkingCity(); // advc.117
		if (pCity == NULL || pCity->getOwner() != getOwner())
			continue;
		if (pIgnoreCity != NULL && pCity == pIgnoreCity)
			continue;
		CityPlotTypes ePlot = pCity->getCityPlotIndex(p); // advc.117
		if (ePlot == CITY_HOME_PLOT || pCity->AI_getBestBuild(ePlot) == NO_BUILD)
			continue;
		if (pIgnoreCity != NULL && pCity->AI_getWorkersHave() -
			(getPlot().getWorkingCity() == pCity ? 1 : 0) >=
			(1 + pCity->AI_getWorkersNeeded() * 2) / 3)
		{
			continue;
		}
		// K-Mod note. This was the original condition for the rest of the block:
		//if ((NULL == pIgnoreCity || (pCity->AI_getWorkersNeeded() > 0 && (pCity->AI_getWorkersHave() < (1 + pCity->AI_getWorkersNeeded() * 2 / 3)))) && pCity->AI_getBestBuild(iIndex) != NO_BUILD)

		/*if (bAllowed) {
			if (p.isImproved() && GC.getInfo(pCity->AI_getBestBuild(iIndex)).getImprovement() != NO_IMPROVEMENT)
				bAllowed = false;
		} */ /* K-Mod. I don't think it's a good idea to disallow improvement changes here.
				So I'm changing it to have a cutoff value instead. */
		iValue = pCity->AI_getBestBuildValue(ePlot);
		if (iValue <= 1) // (advc.opt: moved up)
			continue;
		if (!canBuild(p, pCity->AI_getBestBuild(ePlot)))
			continue;
		if (GET_PLAYER(getOwner()).isAutomationSafe(p))
			continue;
		int iPathTurns;
		if (generatePath(p, NO_MOVEMENT_FLAGS, true, &iPathTurns))
		{
			int iMaxWorkers = 1;
			if (at(p))
			{
				iValue *= 3;
				iValue /= 2;
			}
			else if (getPathFinder().getFinalMoves() == 0)
				iPathTurns++;
			else if (iPathTurns <= 1)
				iMaxWorkers = AI_calculatePlotWorkersNeeded(p, pCity->AI_getBestBuild(ePlot));
			if (GET_PLAYER(getOwner()).AI_plotTargetMissionAIs(p, MISSIONAI_BUILD, getGroup(),
				/*<advc.opt>*/0, iMaxWorkers/*</advc.opt>*/) < iMaxWorkers)
			{
				iValue *= 1000;
				iValue /= 1 + iPathTurns;
				if (iValue > iBestValue)
				{
					iBestValue = iValue;
					pBestPlot = &p;
					eBestBuild = pCity->AI_getBestBuild(ePlot);
					bChop = false; // advc.117
				}
			}
		}
	}

	if (pBestPlot == NULL)
		return false;
	FAssertEnumBounds(eBestBuild);
	// advc.117: No longer guaranteed
	//FAssert(pBestPlot->getWorkingCity() != NULL);
	// advc.113b: Now handled by AI_workerMove
	/*if (NULL != pBestPlot->getWorkingCity()) {
		pBestPlot->getWorkingCity()->AI_changeWorkersHave(+1);
		if (getPlot().getWorkingCity() != NULL)
			getPlot().getWorkingCity()->AI_changeWorkersHave(-1);
	}*/
	MovementFlags eFlags = NO_MOVEMENT_FLAGS; // advc.pf
	// <advc> Moved into helper function
	MissionTypes eMission = (AI_shouldRouteWhileImproving(*pBestPlot, eFlags) ?
			MISSION_ROUTE_TO : MISSION_MOVE_TO); // </advc>
	getGroup()->pushMission(eMission,
			pBestPlot->getX(), pBestPlot->getY(),
			eFlags, false, false,
			MISSIONAI_BUILD, pBestPlot);
	/* advc.117: betterPlotBuild will only suggest Farms or Forts
		or who knows what -- stick to the chopping plan. */
	if (!bChop)
		eBestBuild = AI_betterPlotBuild(*pBestPlot, eBestBuild);
	getGroup()->pushMission(MISSION_BUILD,
			eBestBuild, -1,
			eFlags, true, false,
			MISSIONAI_BUILD, pBestPlot); // K-Mod
	return true;
}


bool CvUnitAI::AI_nextCityToImprove(CvCity const* pCity) // advc: const param
{
	PROFILE_FUNC();
	FAssert(getDomainType() == DOMAIN_LAND); // advc

	int iBestValue = 0;
	BuildTypes eBestBuild = NO_BUILD;
	CvPlot* pBestPlot = NULL;
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());
	//bool const bMoveAllTerrain = getGroup()->canMoveAllTerrain(); // advc
	FOR_EACH_CITYAI(pLoopCity, kOwner)
	{
		if (pLoopCity == pCity)
			continue;
		// BETTER_BTS_AI_MOD, Worker AI, Efficiency, 02/22/10, jdog5000: START
		// BBAI efficiency: check area for land units before path generation
		// advc.opt: This function is only called for land units
		if (/*getDomainType() == DOMAIN_LAND &&*/ !pLoopCity->isArea(getArea()) /*&&
			!bMoveAllTerrain*/)
		{
			continue;
		}
		//iValue = pLoopCity->AI_totalBestBuildValue(area());
		int iWorkersNeeded = pLoopCity->AI_getWorkersNeeded();
		// <advc.113>
		if (iWorkersNeeded <= 0)
			continue;
		/*  Don't want cities to produce that many workers, but don't be as strict
			when it comes to worker movement. */
		iWorkersNeeded++; // </advc.113>
		int iWorkersHave = pLoopCity->AI_getWorkersHave();
		int iValue = std::max(0, iWorkersNeeded - iWorkersHave) * 100;
		iValue += iWorkersNeeded * 10;
		iValue *= iWorkersNeeded + 1;
		iValue /= iWorkersHave + 1;
		if (iValue <= 0)
			continue;

		CvPlot* pPlot = NULL;
		BuildTypes eBuild = NO_BUILD;
		if (/* advc.opt: */ pLoopCity->AI_getBestBuild(NO_CITYPLOT) == NO_BUILD ||
			!AI_bestCityBuild(*pLoopCity, &pPlot, &eBuild, NULL, this))
		{
			continue;
		}
		FAssert(pPlot != NULL && eBuild != NO_BUILD);
		//if (!AI_plotValid(pPlot)) continue; // advc.opt: Area check suffices

		iValue *= 1000;
		if (pLoopCity->isCapital())
			iValue = (iValue * 170) / 100; // advc.113: Was *2, which seems a bit much.
		if (iValue <= iBestValue)
			continue;

		int iPathTurns;
		if (!generatePath(*pPlot, NO_MOVEMENT_FLAGS, true, &iPathTurns))
			continue;

		iValue /= (iPathTurns + 1);
		if (iValue > iBestValue)
		{
			iBestValue = iValue;
			eBestBuild = eBuild;
			pBestPlot = pPlot;
			//FAssert(!atPlot(pBestPlot) || NULL == pCity || pCity->AI_getWorkersNeeded() == 0 || pCity->AI_getWorkersHave() > pCity->AI_getWorkersNeeded() + 1);
		}
		// BETTER_BTS_AI_MOD: END
	}

	if (pBestPlot == NULL)
		return false;
	FAssertEnumBounds(eBestBuild);
	// advc.113b: Now handled by AI_workerMove
	/*if (getPlot().getWorkingCity() != NULL)
		getPlot().getWorkingCity()->AI_changeWorkersHave(-1);
	FAssert(pBestPlot->getWorkingCity() != NULL || GC.getInfo(eBestBuild).getImprovement() == NO_IMPROVEMENT);
	if (NULL != pBestPlot->getWorkingCity())
		pBestPlot->getWorkingCity()->AI_changeWorkersHave(+1);*/

	// <advc.121>
	MissionTypes eMission = MISSION_MOVE_TO;
	if (!getPlot().isSamePlotGroup(*pBestPlot, getOwner()) || !getPlot().isRoute() ||
		SyncRandOneChanceIn(stepDistance(plot(), pBestPlot) + 1))
	{
		if (generatePath(*pBestPlot, MOVE_SAFE_TERRITORY)) // advc.pf
			eMission = MISSION_ROUTE_TO;
	}
	getGroup()->pushMission(eMission, /* </advc.121> */
			pBestPlot->getX(), pBestPlot->getY(),
			eMission == MISSION_ROUTE_TO ? MOVE_SAFE_TERRITORY : NO_MOVEMENT_FLAGS, // advc.pf
			false, false, MISSIONAI_BUILD, pBestPlot);
	eBestBuild = AI_betterPlotBuild(*pBestPlot, eBestBuild);
	getGroup()->pushMission(MISSION_BUILD,
			eBestBuild, -1, NO_MOVEMENT_FLAGS,
			//(getGroup()->getLengthMissionQueue() > 0), false, MISSIONAI_BUILD, pBestPlot);
			true, false, MISSIONAI_BUILD, pBestPlot); // K-Mod
	return true;
}


bool CvUnitAI::AI_nextCityToImproveAirlift()
{
	PROFILE_FUNC();

	if (getGroup()->getNumUnits() > 1)
		return false;

	CvCity* pCity = getPlot().getPlotCity();
	if (pCity == NULL)
		return false;

	if (pCity->getMaxAirlift() <= 0)
		return false;

	int iBestValue = 0;
	CvPlot* pBestPlot = NULL;
	FOR_EACH_CITYAI(pLoopCity, GET_PLAYER(getOwner()))
	{
		if (pLoopCity == pCity)
			continue;

		if (canAirliftAt(pCity->plot(), pLoopCity->getX(), pLoopCity->getY()))
		{
			int iValue = pLoopCity->AI_totalBestBuildValue(pLoopCity->getArea());
			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				pBestPlot = pLoopCity->plot();
			}
		}
	}

	if (pBestPlot == NULL)
		return false;

	getGroup()->pushMission(MISSION_AIRLIFT, pBestPlot->getX(), pBestPlot->getY());
	return true;
}


bool CvUnitAI::AI_irrigateTerritory()
{
	PROFILE_FUNC();
	// <advc.300>
	if (isBarbarian())
		return false; // </advc.300>
	// Erik <OPT1> Cache the viable subset of builds so that we don't have to loop through all of them
	std::vector<BuildTypes> irrigationCarryingBuilds;
	FOR_EACH_ENUM(Build)
	{
		if (GC.getInfo(eLoopBuild).getImprovement() != NO_IMPROVEMENT)
		{
			ImprovementTypes eImprovement = GC.getInfo(eLoopBuild).getImprovement();
			if (GC.getInfo(eImprovement).isCarriesIrrigation())
				irrigationCarryingBuilds.push_back(eLoopBuild);
		}
	} // </OPT1>

	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());
	int const iGwEventTally = GC.getGame().getGwEventTally();

	CvPlot const* pBestPlot = NULL;
	BuildTypes eBestBuild = NO_BUILD;
	int iBestValue = 0;
	// advc.pf: Mainly to avoid placing routes along the way through foreign borders
	MovementFlags const eFlags = MOVE_SAFE_TERRITORY;
	for (int i = 0; i < GC.getMap().numPlots(); i++)
	{
		CvPlot const& kLoopPlot = GC.getMap().getPlotByIndex(i);
		if (!kLoopPlot.isArea(getArea()))
			continue;

		if (/*!AI_plotValid(&kLoopPlot) ||*/ // advc.opt: The area check is enough
			kLoopPlot.getOwner() != kOwner.getID() || // XXX team???
			kLoopPlot.getWorkingCity() != NULL)
		{
			continue;
		}
		ImprovementTypes const eCurrentImprov = kLoopPlot.getImprovementType();
		if (eCurrentImprov != NO_IMPROVEMENT)
		{
			if (kOwner.isAutomationSafe(kLoopPlot))
				continue;
			if (GC.getInfo(eCurrentImprov).isCarriesIrrigation())
				continue;
			BonusTypes const eBonus = kLoopPlot.getNonObsoleteBonusType(getTeam());
			if (eBonus != NO_BONUS &&
				// !(GC.getInfo(eImprovement).isImprovementBonusTrade(eBonus)))
				kOwner.doesImprovementConnectBonus(eCurrentImprov, eBonus)) // K-Mod
			{
				continue;
			}
		}
		if (!kLoopPlot.isIrrigationAvailable(true))
			continue;

		int iBestTempBuildValue = MAX_INT;
		BuildTypes eBestTempBuild = NO_BUILD;
		for (size_t iJ = 0; iJ < irrigationCarryingBuilds.size(); iJ++)
		{
			const BuildTypes eBuild = irrigationCarryingBuilds[iJ];
			if (!canBuild(kLoopPlot, eBuild))
				continue;
			/*  <advc.121> Was 10000/(...getTime()+1). Same problem as in
				AI_improveBonus (see there). */
			int iValue = GC.getInfo(eBuild).getTime();
			// XXX feature production???
			if (iValue < iBestTempBuildValue)
			{
				iBestTempBuildValue = iValue;
				eBestTempBuild = eBuild;
			}
		}
		if (eBestTempBuild == NO_BUILD)
			continue;

		FeatureTypes const eFeature = kLoopPlot.getFeatureType();
		if (eFeature != NO_FEATURE && GC.getInfo(eBestTempBuild).isFeatureRemove(eFeature))
		{
			CvFeatureInfo const& kFeatureInfo = GC.getInfo(kLoopPlot.getFeatureType());
			// K-Mod:
			if ((iGwEventTally >= 0 && kFeatureInfo.getWarmingDefense() > 0) ||
				(kOwner.isHumanOption(PLAYEROPTION_LEAVE_FORESTS) &&
				kFeatureInfo.getYieldChange(YIELD_PRODUCTION) > 0))
			{
				continue;
			}
		}

		if (kLoopPlot.isVisibleEnemyUnit(this) ||
			kOwner.AI_isAnyPlotTargetMissionAI(kLoopPlot, MISSIONAI_BUILD, getGroup(), 1))
		{
			continue;
		}
		int iPathTurns; // XXX should this actually be at the top of the loop? (with saved paths and all...)
		if (generatePath(kLoopPlot, eFlags, true, &iPathTurns))
		{
			const int iValue = 10000 - iPathTurns; // advc.opt: Instead of dividing by iPathTurns+1
			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				eBestBuild = eBestTempBuild;
				pBestPlot = &kLoopPlot;
			}
		}
	}

	if (pBestPlot == NULL)
		return false;

	FAssertBounds(NO_BUILD, GC.getNumBuildInfos(), eBestBuild);
	getGroup()->pushMission(MISSION_ROUTE_TO,
			pBestPlot->getX(), pBestPlot->getY(), eFlags, false,
			false, MISSIONAI_BUILD, pBestPlot);
	getGroup()->pushMission(MISSION_BUILD,
			eBestBuild, -1, eFlags,
			true, // K-Mod: was (getGroup()->getLengthMissionQueue() > 0)
			false, MISSIONAI_BUILD, pBestPlot);
	return true;
}


bool CvUnitAI::AI_fortTerritory(bool bCanal, bool bAirbase)
{
	PROFILE_FUNC();

	/*	K-Mod. This function currently only handles canals and airbases.
		So if we want neither, just abort. */
	if (!bCanal && !bAirbase)
		return false;
	// K-Mod end

	BuildTypes eBestBuild = NO_BUILD;
	CvPlot const* pBestPlot = NULL;
	int iBestValue = 0;
	// advc.pf: Mainly to avoid placing routes along the way through foreign borders
	MovementFlags const eFlags = MOVE_SAFE_TERRITORY;
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());
	for (int i = 0; i < GC.getMap().numPlots(); i++)
	{
		CvPlot const& kPlot = GC.getMap().getPlotByIndex(i);
		if(kPlot.getOwner() != getOwner() || // XXX team???
			/*!AI_plotValid(kPlot)*/ !isArea(kPlot.getArea())) // advc.opt
		{
			continue;
		}
		if (kPlot.isImproved())
			continue;
		int iValue = 0;
		iValue += (bCanal ? kOwner.AI_getPlotCanalValue(kPlot) : 0);
		iValue += (bAirbase ? kOwner.AI_getPlotAirbaseValue(kPlot) : 0);
		if(iValue <= 0)
			continue;
		int iBestTempBuildValue = MAX_INT;
		BuildTypes eBestTempBuild = NO_BUILD;
		FOR_EACH_ENUM(Build)
		{
			if (GC.getInfo(eLoopBuild).getImprovement() != NO_IMPROVEMENT)
			{ /* advc.121: Same problems as in AI_improveBonus, but there's
				 only one type of Fort anyway (K-Mod comment to that effect deleted). */
				ImprovementTypes eImprov = GC.getInfo(eLoopBuild).getImprovement();
				if(GC.getInfo(eImprov).isActsAsCity() &&
					GC.getInfo(eImprov).getDefenseModifier() > 0)
				{
					if (canBuild(kPlot, eLoopBuild) ||
						eImprov == kPlot.getImprovementType()) // advc.121
					{
						/*int iValue = 10000;
						iValue /= (GC.getInfo(eBuild).getTime() + 1);*/
						// <advc.121> Replacing the above
						int iTempBuildValue = (eImprov == kPlot.getImprovementType() ?
								0 : GC.getInfo(eLoopBuild).getTime()); // </advc.121>
						if (iTempBuildValue < iBestTempBuildValue)
						{
							iBestTempBuildValue = iTempBuildValue;
							eBestTempBuild = eLoopBuild;
						}
					}
				}
			}
		}
		// <advc.121>
		if (eBestTempBuild != NO_BUILD && !canBuild(kPlot, eBestTempBuild))
			eBestTempBuild = NO_BUILD; // </advc.121>
		if (eBestTempBuild != NO_BUILD)
		{
			if (!kPlot.isVisibleEnemyUnit(this))
			{
				bool bValid = true;
				if (GET_PLAYER(getOwner()).isHumanOption(PLAYEROPTION_LEAVE_FORESTS) &&
					kPlot.isFeature() &&
					GC.getInfo(eBestTempBuild).isFeatureRemove(kPlot.getFeatureType()) &&
					GC.getInfo(kPlot.getFeatureType()).getYieldChange(YIELD_PRODUCTION) > 0)
				{
					bValid = false;
				}
				if (bValid)
				{
					if (!GET_PLAYER(getOwner()).AI_isAnyPlotTargetMissionAI(
						kPlot, MISSIONAI_BUILD, getGroup(), 3))
					{
						int iPathTurns;
						if (generatePath(kPlot, eFlags, true, &iPathTurns))
						{
							iValue *= 1000;
							iValue /= (iPathTurns + 1);
							if (iValue > iBestValue)
							{
								iBestValue = iValue;
								eBestBuild = eBestTempBuild;
								pBestPlot = &kPlot;
							}
						}
					}
				}
			}
		}
	}
	if (pBestPlot != NULL)
	{
		FAssertEnumBounds(eBestBuild);
		getGroup()->pushMission(MISSION_ROUTE_TO,
				pBestPlot->getX(), pBestPlot->getY(),
				eFlags, false, false,
				MISSIONAI_BUILD, pBestPlot);
		getGroup()->pushMission(MISSION_BUILD, eBestBuild, -1, eFlags,
				//(getGroup()->getLengthMissionQueue() > 0), false, MISSIONAI_BUILD, pBestPlot);
				true, false, MISSIONAI_BUILD, pBestPlot); // K-Mod

		return true;
	}
	return false;
}

//bool CvUnitAI::AI_improveBonus(int iMinValue, CvPlot** ppBestPlot, BuildTypes* peBestBuild, int* piBestValue)
bool CvUnitAI::AI_improveBonus( // K-Mod. (all that junk wasn't being used anyway.)
	int iMissingWorkersInArea) // advc.121
{
	PROFILE_FUNC();

	const CvPlayerAI& kOwner = GET_PLAYER(getOwner());
	bool bBestBuildIsRoute = false;
	//int iBestResourceValue = 0; // advc: no longer used
	BuildTypes eBestBuild = NO_BUILD;
	CvPlot const* pBestPlot = NULL;
	int iBestValue = 0;
	bool bCanRoute = canBuildRoute();
	for (int iI = 0; iI < GC.getMap().numPlots(); iI++)
	{
		CvPlot const& kPlot = GC.getMap().getPlotByIndex(iI);
		if(kPlot.getOwner() != getOwner() || /*!AI_plotValid(kPlot)*/  // <advc.opt>
			(getDomainType() == DOMAIN_SEA ? !kPlot.isWater() :
			!isArea(kPlot.getArea()))) // </advc.opt>
		{
			continue;
		}

		bool bCanImprove = kPlot.isArea(getArea());
		if (!bCanImprove)
		{
			if (getDomainType() == DOMAIN_SEA && kPlot.isWater() &&
				getPlot().isAdjacentToArea(kPlot.getArea()))
			{
				bCanImprove = true;
			}
		}
		if(!bCanImprove)
			continue;

		BonusTypes eNonObsoleteBonus = kPlot.getNonObsoleteBonusType(getTeam());
		if(eNonObsoleteBonus == NO_BONUS)
			continue;

		bool bConnected = kPlot.isConnectedToCapital(getOwner());
		if(kPlot.getWorkingCity() == NULL && !bConnected && !bCanRoute)
			continue;

		// <advc.300> Barbarian workers shouldn't improve bonuses around remote cities
		if(isBarbarian() && (kPlot.getWorkingCity() == NULL ||
			kPlot.getWorkingCity() != getPlot().getWorkingCity()))
		{
			continue;
		} // </advc.300>


		/*ImprovementTypes eImprovement = kPlot.getImprovementType();
		bool bDoImprove = false;
		if (eImprovement == NO_IMPROVEMENT)
			bDoImprove = true;
		else if (GC.getInfo(eImprovement).isActsAsCity() || GC.getInfo(eImprovement).isImprovementBonusTrade(eNonObsoleteBonus))
			bDoImprove = false;
		else if (eImprovement == GC.getRUINS_IMPROVEMENT())
			bDoImprove = true;
		else if (!GET_PLAYER(getOwner()).isOption(PLAYEROPTION_SAFE_AUTOMATION))
			bDoImprove = true;
		int iBestTempBuildValue = MAX_INT;
		BuildTypes eBestTempBuild = NO_BUILD;*/ // BtS
		// K-Mod. Simpler, and better.
		bool bDoImprove = true;
		ImprovementTypes eImprovement = kPlot.getImprovementType();
		CvCityAI const* pWorkingCity = kPlot.AI_getWorkingCity();
		BuildTypes eBestTempBuild = NO_BUILD;
		if (eImprovement != NO_IMPROVEMENT &&
			((kOwner.isHumanOption(PLAYEROPTION_SAFE_AUTOMATION) &&
			eImprovement != GC.getRUINS_IMPROVEMENT()) ||
			(kOwner.doesImprovementConnectBonus(eImprovement, eNonObsoleteBonus) &&
			/*  advc.121: This should give replacement of Fort with another
				connecting improvement a higher priority when Workers have time. */
			pWorkingCity == NULL && iMissingWorkersInArea > 0)))
		{
			bDoImprove = false;
		}
		else if (pWorkingCity != NULL)
		{
			// Let "best build" handle improvement replacements near cities.
			BuildTypes eBuild = pWorkingCity->AI_getBestBuild(
					pWorkingCity->getCityPlotIndex(kPlot));
			if (eBuild != NO_BUILD && kOwner.doesImprovementConnectBonus(
				GC.getInfo(eBuild).getImprovement(), eNonObsoleteBonus) &&
				canBuild(kPlot, eBuild))
			{
				bDoImprove = true;
				eBestTempBuild = eBuild;
			}
			else bDoImprove = false;
		} // K-Mod end
		//if (bDoImprove)
		if (bDoImprove && eBestTempBuild == NO_BUILD) // K-Mod
		{
			int iBestTempBuildValue = MAX_INT; // K-Mod
			FOR_EACH_ENUM(Build)
			{
				// <advc.121> Moved into subroutines
				if(!AI_canConnectBonus(kPlot, eLoopBuild))
					continue;
				int iValue = AI_connectBonusCost(kPlot, eLoopBuild, iMissingWorkersInArea);
				// </advc.121>
				if (iValue < iBestTempBuildValue)
				{
					iBestTempBuildValue = iValue;
					eBestTempBuild = eLoopBuild;
				}
			}
		}
		/*  <advc.121> canBuild no longer guaranteed b/c eBestTempBuild could
			already be present. */
		if(eBestTempBuild != NO_BUILD && !canBuild(kPlot, eBestTempBuild))
			eBestTempBuild = NO_BUILD; // </advc.121>
		if(eBestTempBuild == NO_BUILD)
			bDoImprove = false;

		if(eBestTempBuild == NO_BUILD && (!bCanRoute || bConnected))
			continue;

		int iPathTurns;
		if(!generatePath(kPlot, NO_MOVEMENT_FLAGS, true, &iPathTurns))
			continue;

		int iValue = kOwner.AI_bonusVal(eNonObsoleteBonus, 1);
		if (bDoImprove)
		{
			eImprovement = GC.getInfo(eBestTempBuild).getImprovement();
			FAssert(eImprovement != NO_IMPROVEMENT);
			//iValue += (GC.getInfo(GC.getInfo(eBestTempBuild).getImprovement()))
			iValue += 5 * kPlot.calculateImprovementYieldChange(
					eImprovement, YIELD_FOOD, getOwner());
			iValue += 5 * kPlot.calculateNatureYield(YIELD_FOOD, getTeam(),
					!kPlot.isFeature() ? true :
					GC.getInfo(eBestTempBuild).isFeatureRemove(kPlot.getFeatureType()));
		}
		iValue += std::max(0, 100 * GC.getInfo(eNonObsoleteBonus).getAIObjective());

		if(kOwner.getNumTradeableBonuses(eNonObsoleteBonus) == 0)
			iValue *= 2;

		int iMaxWorkers = 1;
		if (eBestTempBuild != NO_BUILD && !GC.getInfo(eBestTempBuild).isKill())
		{ //allow teaming.
			iMaxWorkers = AI_calculatePlotWorkersNeeded(kPlot, eBestTempBuild);
			if (getPathFinder().getFinalMoves() == 0)
			{
				iMaxWorkers = std::min((iMaxWorkers + 1) / 2,
						1 + kOwner.AI_baseBonusVal(eNonObsoleteBonus, 1) / 20);
			}
		}
		if (kOwner.AI_plotTargetMissionAIs(kPlot, MISSIONAI_BUILD, getGroup(),
			/*<advc.opt>*/0, iMaxWorkers/*</advc.opt>*/) < iMaxWorkers &&
			(!bDoImprove || kPlot.getBuildTurnsLeft(eBestTempBuild,
			/* advc.251: */ kOwner.getID(), 0, 0) > iPathTurns * 2 - 1))
		{
			if (bDoImprove)
			{
				iValue *= 1000;
				if(iPathTurns == 1 && getPathFinder().getFinalMoves() != 0)
					iValue *= 2;
				iValue /= (iPathTurns + 1);
				if(kPlot.isCityRadius())
					iValue *= 2;
				if (iValue > iBestValue)
				{
					iBestValue = iValue;
					eBestBuild = eBestTempBuild;
					pBestPlot = &kPlot;
					bBestBuildIsRoute = false;
					//iBestResourceValue = iValue; // advc: no longer used
				}
			}
			else
			{
				FAssert(bCanRoute && !bConnected);
				eImprovement = kPlot.getImprovementType();
				//if ((eImprovement != NO_IMPROVEMENT) && (GC.getInfo(eImprovement).isImprovementBonusTrade(eNonObsoleteBonus)))
				if (kOwner.doesImprovementConnectBonus(eImprovement, eNonObsoleteBonus))
				{
					iValue *= 1000;
					iValue /= (iPathTurns + 1);
					if (iValue > iBestValue)
					{
						iBestValue = iValue;
						eBestBuild = NO_BUILD;
						pBestPlot = &kPlot;
						bBestBuildIsRoute = true;
					}
				}
			}
		}
	}
	/*if ((iBestValue < iMinValue) && (NULL != ppBestPlot))
	{
		FAssert(NULL != peBestBuild);
		FAssert(NULL != piBestValue);

		*ppBestPlot = pBestPlot;
		*peBestBuild = eBestBuild;
		*piBestValue = iBestResourceValue;
	} */ /* BtS - disabled by K-Mod. This is clearly wrong.
			But even if it was fixed it isn't useful anyway, so I'm removing it. */

	if (pBestPlot == NULL)
		return false;

	if (eBestBuild != NO_BUILD)
	{
		FAssert(!bBestBuildIsRoute);
		FAssert(eBestBuild < GC.getNumBuildInfos());
		MissionTypes eBestMission = MISSION_MOVE_TO;
		// advc.001y: Sea workers can't route
		if (getGroup()->canDoMission(MISSION_ROUTE_TO, getX(), getY(), plot(), false, false))
		{
			if (pBestPlot->getWorkingCity() == NULL ||
				!pBestPlot->getWorkingCity()->isConnectedToCapital())
			{
				eBestMission = MISSION_ROUTE_TO;
			}
			else
			{
				int iDistance = stepDistance(getX(), getY(), pBestPlot->getX(), pBestPlot->getY());
				int iPathTurns;
				if (generatePath(*pBestPlot, NO_MOVEMENT_FLAGS, //false,
					true, // advc.pf: Will want to reuse this (NB: obsolete param anyway)
					&iPathTurns))
				{
					if (iPathTurns >= iDistance)
						eBestMission = MISSION_ROUTE_TO;
				}
			}
		}
		// <advc.pf>
		MovementFlags eFlags = NO_MOVEMENT_FLAGS;
		if (!AI_canRouteThroughSafeTerritory(*pBestPlot, eFlags))
			eBestMission = MISSION_MOVE_TO; // </advc.pf>
		getGroup()->pushMission(eBestMission,
				pBestPlot->getX(), pBestPlot->getY(), eFlags, false,
				false, MISSIONAI_BUILD, pBestPlot);
		eBestBuild = AI_betterPlotBuild(*pBestPlot, eBestBuild);
		getGroup()->pushMission(MISSION_BUILD,
				eBestBuild, -1, eFlags,
				//(getGroup()->getLengthMissionQueue() > 0),
				true, // K-Mod
				false, MISSIONAI_BUILD, pBestPlot);
		return true;
	}
	else if (bBestBuildIsRoute)
	{
		if (AI_connectPlot(*pBestPlot))
		{
			return true;
		}
		/*else {
			// the plot may be connected, but not connected to capital, if capital is not on same area, or if civ has no capital (like barbarians)
			FErrorMsg("Expected that a route could be built to eBestPlot");
		}*/
	}
	else FAssert(false);
	return false;
}

//returns true if a mission is pushed
//if eBuild is NO_BUILD, assumes a route is desired.
// advc.003j (comment): Not currently used (b/c of K-Mod changes in this file)
bool CvUnitAI::AI_improvePlot(CvPlot const& kPlot, BuildTypes eBuild) // advc: param was CvPlot*
{
	if (eBuild != NO_BUILD)
	{
		FAssert(eBuild < GC.getNumBuildInfos());
		if (!at(kPlot))
		{
			pushGroupMoveTo(kPlot, NO_MOVEMENT_FLAGS, false, false,
					MISSIONAI_BUILD, &kPlot);
		}
		eBuild = AI_betterPlotBuild(kPlot, eBuild);
		getGroup()->pushMission(MISSION_BUILD, eBuild, -1, NO_MOVEMENT_FLAGS,
				//(getGroup()->getLengthMissionQueue() > 0), false, MISSIONAI_BUILD, pPlot);
				true, false, MISSIONAI_BUILD, &kPlot); // K-Mod

		return true;
	}
	else if (canBuildRoute())
	{
		if (AI_connectPlot(kPlot))
			return true;
	}

	return false;

}

BuildTypes CvUnitAI::AI_betterPlotBuild(CvPlot const& kPlot, BuildTypes eBuild) // advc: param was CvPlot*
{
	FAssert(eBuild != NO_BUILD);
	bool bBuildRoute = false;
	bool bClearFeature = false;
	FeatureTypes eFeature = kPlot.getFeatureType();

	CvBuildInfo& kOriginalBuildInfo = GC.getInfo(eBuild);
	if (kOriginalBuildInfo.getRoute() != NO_ROUTE)
		return eBuild;
	//int iWorkersNeeded // advc: It's more like a prediction of how many workers will attend to the task
	int iTargetWorkers = AI_calculatePlotWorkersNeeded(kPlot, eBuild);

	//if (pPlot->getBonusType() == NO_BONUS)
	// BETTER_BTS_AI_MOD, Bugfix, 7/31/08, jdog5000:
	if (kPlot.getNonObsoleteBonusType(getTeam()) == NO_BONUS)
	{
		CvCityAI const* pTargetCity =  kPlot.AI_getWorkingCity();
		if (pTargetCity != NULL)
		{
			int iCityWorkers = pTargetCity->AI_getWorkersHave();
			/*  <advc.113b> Count the current worker if it isn't already included
				(Previously, the caller took care of that by calling
				CvCity::AI_changeWorkersHave beforehand.) */
			if (AI_getCityToImprove() != pTargetCity)
				iCityWorkers++; // </advc.113b>
			iTargetWorkers = std::max(1, std::min(iTargetWorkers, iCityWorkers));
		}
	}
	if (eFeature != NO_FEATURE)
	{
		CvFeatureInfo& kFeatureInfo = GC.getInfo(eFeature);
		if (kOriginalBuildInfo.isFeatureRemove(eFeature))
		{
			if (kOriginalBuildInfo.getImprovement() == NO_IMPROVEMENT ||
					(!kPlot.isBeingWorked() ||
					kFeatureInfo.getYieldChange(YIELD_FOOD) +
					kFeatureInfo.getYieldChange(YIELD_PRODUCTION) <= 0))
				bClearFeature = true;
		}
		if (kFeatureInfo.getMovementCost() > 1 && iTargetWorkers > 1)
			bBuildRoute = true;
	}
	//if (pPlot->getBonusType() != NO_BONUS)
	// BETTER_BTS_AI_MOD, Bugfix, 7/31/08, jdog5000: START
	if (kPlot.getNonObsoleteBonusType(getTeam()) != NO_BONUS)
		bBuildRoute = true;
	else if (kPlot.isHills())
	{
		if (GC.getDefineINT(CvGlobals::HILLS_EXTRA_MOVEMENT) > 0 && iTargetWorkers > 1)
			bBuildRoute = true;
	} // BETTER_BTS_AI_MOD: END

	if (kPlot.isRoute())
		bBuildRoute = false;

	int const NO_PLOTGROUP = FFreeList::INVALID_INDEX; // advc
	BuildTypes eBestBuild = NO_BUILD;
	int iBestValue = 0;
	FOR_EACH_ENUM(Build)
	{
		CvBuildInfo const& kLoopBuild = GC.getInfo(eLoopBuild);
		RouteTypes eRoute = kLoopBuild.getRoute();
		if ((bBuildRoute && eRoute != NO_ROUTE) ||
			(bClearFeature && kLoopBuild.isFeatureRemove(eFeature)))
		{
			if (!canBuild(kPlot, eLoopBuild))
				continue;

			int iValue = 10000;
			if (bBuildRoute && eRoute != NO_ROUTE)
			{
				iValue *= (1 + GC.getInfo(eRoute).getValue());
				iValue /= 2;
				//if (pPlot->getBonusType() != NO_BONUS)
				// BETTER_BTS_AI_MOD, Bugfix, 7/31/08, jdog5000:
				if (kPlot.getNonObsoleteBonusType(getTeam()) != NO_BONUS)
					iValue *= 2;

				if (kPlot.getWorkingCity() != NULL)
				{
					iValue *= 2 + iTargetWorkers +
							((kPlot.isHills() && iTargetWorkers > 1) ?
							2 * GC.getDefineINT(CvGlobals::HILLS_EXTRA_MOVEMENT) : 0);
					iValue /= 3;
				}
				ImprovementTypes const eImprovement = kOriginalBuildInfo.getImprovement();
				if (eImprovement != NO_IMPROVEMENT)
				{
					CvImprovementInfo const& kImprov = GC.getInfo(eImprovement);
					int iRouteMultiplier =
							100 * kImprov.getRouteYieldChanges(eRoute, YIELD_FOOD) +
							100 * kImprov.getRouteYieldChanges(eRoute, YIELD_PRODUCTION) +
							 60 * kImprov.getRouteYieldChanges(eRoute, YIELD_COMMERCE);
					iValue *= 100 + iRouteMultiplier;
					iValue /= 100;
				}
				int iPlotGroupId = NO_PLOTGROUP;
				FOR_EACH_ADJ_PLOT(kPlot)
				{
					if (!kPlot.isRiver() && !pAdj->isRoute())
						continue;

					CvPlotGroup* pAdjPlotGroup = pAdj->getPlotGroup(getOwner());
					if (pAdjPlotGroup == NULL || pAdjPlotGroup->getID() == NO_PLOTGROUP)
						continue;

					if (pAdjPlotGroup->getID() != iPlotGroupId &&
						// advc.001: Based on Mongoose Mod changelog (12-14 Dec 2012)
						iPlotGroupId != NO_PLOTGROUP)
					{
						//This plot bridges plot groups, so route it.
						iValue *= 4;
						break;
					}
					else iPlotGroupId = pAdjPlotGroup->getID();
				}
			}
			iValue /= kLoopBuild.getTime() + 1;
			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				eBestBuild = eLoopBuild;
			}
		}
	}
	if (eBestBuild == NO_BUILD)
		return eBuild;
	return eBestBuild;
}


bool CvUnitAI::AI_connectBonus(bool bTestTrade)
{
	PROFILE_FUNC();

	// XXX how do we make sure that we can build roads???

	for (int iI = 0; iI < GC.getMap().numPlots(); iI++)
	{
		CvPlot const& kPlot = GC.getMap().getPlotByIndex(iI);
		if (kPlot.getOwner() != getOwner() || // XXX team???
			/*!AI_plotValid(kPlot)*/kPlot.isArea(kPlot.getArea())) // advc.opt
		{
			continue;
		}
		BonusTypes eNonObsoleteBonus = kPlot.getNonObsoleteBonusType(getTeam());
		if (eNonObsoleteBonus != NO_BONUS)
		{
			if (!kPlot.isConnectedToCapital())
			{
				//if (!bTestTrade || ((pLoopPlot->getImprovementType() != NO_IMPROVEMENT) && (GC.getInfo(kPlot.getImprovementType()).isImprovementBonusTrade(eNonObsoleteBonus))))
				if (!bTestTrade || GET_PLAYER(getOwner()).doesImprovementConnectBonus(kPlot.getImprovementType(), eNonObsoleteBonus))
				{
					if (AI_connectPlot(kPlot))
						return true;
				}
			}
		}
	}

	return false;
}


bool CvUnitAI::AI_connectCity()
{
	PROFILE_FUNC();

	// XXX how do we make sure that we can build roads???

	CvCity* pCity = getPlot().getWorkingCity(); // advc: Renamed from pLoopCity
	if (pCity != NULL && !pCity->isConnectedToCapital())
	{
		// (advc.003opt: AI_plotValid check removed)
		if (AI_connectPlot(*pCity->plot(), 1))
			return true;
	}
	// <advc.300>
	if(isBarbarian())
		return false; // </advc.300>

	FOR_EACH_CITYAI(pLoopCity, GET_PLAYER(getOwner()))
	{
		CvPlot const& kCityPlot = *pLoopCity->plot(); // advc
		if (//AI_plotValid(kCityPlot) &&
			isArea(kCityPlot.getArea()) && // advc.opt
			!pLoopCity->isConnectedToCapital() &&
			AI_connectPlot(kCityPlot, 1))
		{
			return true;
		}
	}

	return false;
}


bool CvUnitAI::AI_routeCity()
{
	PROFILE_FUNC();
	FAssert(canBuildRoute());

	std::vector<std::pair<int,IDInfo> > aCities; // advc.121
	FOR_EACH_CITYAI(pCity, GET_PLAYER(getOwner()))
	{
		/*if (!AI_plotValid(pCity->getPlot()))
			continue;*/ // advc: Taken care of by the BBAI code
		/*  BETTER_BTS_AI_MOD, Unit AI, Efficiency, 02/22/10, jdog5000: START
			check area for land units and generatePath call moved down */
		if(getDomainType() == DOMAIN_LAND && !pCity->isArea(getArea()) &&
			!getGroup()->canMoveAllTerrain())
		{
			continue;
		} // BETTER_BTS_AI_MOD: END
		// <advc.121> Try the cities in a sensible order
		aCities.push_back(std::make_pair(
				stepDistance(plot(), pCity->plot()) - pCity->getPopulation(),
				pCity->getIDInfo()));
	}
	std::sort(aCities.begin(), aCities.end());
	for (size_t i = 0; i < aCities.size(); i++)
	{
		CvCityAI const& kLoopCity = *GET_PLAYER(getOwner()).AI_getCity(aCities[i].second.iID);
		// </advc.121>
		CvCityAI* pRouteToCity = kLoopCity.AI_getRouteToCity();
		if (pRouteToCity != NULL &&
			/*!kLoopCity.getPlot().isVisibleEnemyUnit(this) && // advc.opt: These cities belong to our team
			!pRouteToCity->getPlot().isVisibleEnemyUnit(this) &&*/
			!kLoopCity.AI_isEvacuating() && !pRouteToCity->AI_isEvacuating() && // advc.139
			!GET_PLAYER(getOwner()).AI_isAnyPlotTargetMissionAI(
			pRouteToCity->getPlot(), MISSIONAI_BUILD, getGroup()))
		{
			bool const bRouteTo = (at(kLoopCity.getPlot()) ||
					!getPlot().isSamePlotGroup(kLoopCity.getPlot(), getOwner()) ||
					/*	We might already be in the middle of an incomplete route.
						Don't move to kLoopCity first then. */
					stepDistance(plot(), pRouteToCity->plot()) <=
					stepDistance(plot(), kLoopCity.plot()));
			if (generatePath(kLoopCity.getPlot(),
				MOVE_SAFE_TERRITORY, true, /* advc.opt: */ NULL, 7) &&
				generatePath(pRouteToCity->getPlot(),
				MOVE_SAFE_TERRITORY, true, /* advc.opt: */ NULL, 7))
			{	// <advc.121>
				if (!bRouteTo)
				{
					pushGroupMoveTo(kLoopCity.getPlot(),
							MOVE_SAFE_TERRITORY, false,
							false, MISSIONAI_BUILD, pRouteToCity->plot());
				} // </advc.121>
				getGroup()->pushMission(MISSION_ROUTE_TO,
						kLoopCity.getX(), kLoopCity.getY(),
						MOVE_SAFE_TERRITORY, /* advc.121: */ !bRouteTo,
						false, MISSIONAI_BUILD, pRouteToCity->plot());
				getGroup()->pushMission(MISSION_ROUTE_TO,
						pRouteToCity->getX(), pRouteToCity->getY(),
						MOVE_SAFE_TERRITORY, true,
						false, MISSIONAI_BUILD, pRouteToCity->plot()); // K-Mod
				return true;
			}
		}
	}
	return false;
}


bool CvUnitAI::AI_routeTerritory(bool bImprovementOnly)
{
	PROFILE_FUNC();

	// XXX how do we make sure that we can build roads???

	FAssert(canBuildRoute());

	CvPlot const* pBestPlot = NULL;
	int iBestValue = 0;
	BuildTypes eBestBuild = NO_BUILD; // advc.121
	for (int i = 0; i < GC.getMap().numPlots(); i++)
	{
		CvPlot const& kPlot = GC.getMap().getPlotByIndex(i);
		if (kPlot.getOwner() != getOwner() || // XXX team???
			/*!AI_plotValid(kPlot)*/ !isArea(kPlot.getArea())) // advc.opt
		{
			continue;
		}
		BuildTypes eBuild=NO_BUILD; // advc.121
		RouteTypes eBestRoute = GET_PLAYER(getOwner()).getBestRoute(&kPlot,
				&eBuild); // advc.121
		if (eBestRoute == NO_ROUTE || eBestRoute == kPlot.getRouteType())
			continue;

		int iValue = 1; // advc.121: Replacing bValid
		if (bImprovementOnly)
		{
			iValue = 0;
			ImprovementTypes eImprovement = kPlot.getImprovementType();
			if (eImprovement != NO_IMPROVEMENT)
			{
				FOR_EACH_ENUM(Yield)
				{
					iValue += GC.getInfo(eImprovement).getRouteYieldChanges(
							eBestRoute, eLoopYield);
					//break; // advc.121: Sum them all up
				}
				// <advc.121>
				if (kPlot.isBeingWorked())
					iValue *= 3; // </advc.121>
			}
		}
		if (iValue > 0 && !kPlot.isVisibleEnemyUnit(this))
		{	// <advc.121> was AI_isAnyPlotTargetMission
			int iMissions = GET_PLAYER(getOwner()).AI_plotTargetMissionAIs(
					kPlot, MISSIONAI_BUILD, getGroup(),
					// iRange: Don't count adjacent workers when trying to improve yield
					bImprovementOnly ? 0 : 1, 3);
			if (iMissions < 3) // </advc.121>
			{
				int iPathTurns;
				if (generatePath(kPlot, MOVE_SAFE_TERRITORY, true, &iPathTurns))
				{	// <advc.121> Allow teaming up (mostly just on slow speed settings)
					if (iMissions > 0)
					{
						int iBuildTurns = kPlot.getBuildTurnsLeft(
								eBuild, getOwner(), 0, workRate(true), false);
						FAssert(iBuildTurns > 0);
						if (2 * iMissions >= iBuildTurns - iPathTurns)
							continue;
					} // </advc.121>
					iValue *= 10000;
					iValue /= (iPathTurns + 1);
					if (iValue > iBestValue)
					{
						iBestValue = iValue;
						pBestPlot = &kPlot;
						eBestBuild = eBuild; // advc.121
					}
				}
			}
		}
	}
	if (pBestPlot == NULL)
		return false; // advc

	/*	<advc.121> If there are yields to be gained, don't lose time building
		routes along the way. (This is really the job of AI_improveCity, but
		there may not be enough workers assigned to cities to get it done fast.) */
	bool bRouteTo = (!bImprovementOnly || atPlot(pBestPlot) ||
			!getPlot().isSamePlotGroup(*pBestPlot, getOwner()));
	if (!bRouteTo)
	{
		pushGroupMoveTo(*pBestPlot, MOVE_SAFE_TERRITORY, false, false,
				MISSIONAI_BUILD, pBestPlot);
		/*	(Falling through to MISSION_ROUTE_TO would probably also be fine
			if bAppend is set to !bRouteTo) */
		getGroup()->pushMission(MISSION_BUILD, eBestBuild, -1,
				NO_MOVEMENT_FLAGS, true, false, MISSIONAI_BUILD, pBestPlot);
		return true;
	} // </advc.121>
	getGroup()->pushMission(MISSION_ROUTE_TO, pBestPlot->getX(), pBestPlot->getY(),
			MOVE_SAFE_TERRITORY, false, false, MISSIONAI_BUILD, pBestPlot);
	return true;
}


bool CvUnitAI::AI_travelToUpgradeCity()
{
	PROFILE_FUNC();

	// is there a city which can upgrade us?
	CvCity* pUpgradeCity = getUpgradeCity(/*bSearch*/ true);
	if (pUpgradeCity == NULL)
		return false; // advc

	// cache some stuff
	bool bSeaUnit = (getDomainType() == DOMAIN_SEA);
	bool bCanAirliftUnit = (getDomainType() == DOMAIN_LAND);
	bool bShouldSkipToUpgrade = (getDomainType() != DOMAIN_AIR);

	// if we are at the upgrade city, stop, wait to get upgraded
	if (at(pUpgradeCity->getPlot()))
	{
		if (!bShouldSkipToUpgrade)
		{
			return false;
		}
		getGroup()->pushMission(MISSION_SKIP);
		return true;
	}

	if (DOMAIN_AIR == getDomainType())
	{
		pushGroupMoveTo(pUpgradeCity->getPlot());
		return true;
	}

	// find the closest city
	CvCity* pClosestCity = getPlot().getPlotCity();
	bool bAtClosestCity = (pClosestCity != NULL);
	if (pClosestCity == NULL)
		pClosestCity = getPlot().getWorkingCity();
	if (pClosestCity == NULL)
		pClosestCity = GC.getMap().findCity(getX(), getY(), NO_PLAYER, getTeam(), true, bSeaUnit);

	// can we path to the upgrade city?
	int iUpgradeCityPathTurns;
	bool const bCanPathToUpgradeCity = generatePath(pUpgradeCity->getPlot(),
			NO_MOVEMENT_FLAGS, true, &iUpgradeCityPathTurns);
	CvPlot* pUpgradeCityEndTurnPlot = (bCanPathToUpgradeCity ? &getPathEndTurnPlot() : NULL);
	// if we close to upgrade city, head there
	if (pUpgradeCityEndTurnPlot != NULL && pClosestCity != NULL &&
		(pClosestCity == pUpgradeCity || iUpgradeCityPathTurns < 4))
	{
		pushGroupMoveTo(*pUpgradeCityEndTurnPlot);
		return true;
	}

	// check for better airlift choice
	if (bCanAirliftUnit && pClosestCity != NULL && pClosestCity->getMaxAirlift() > 0)
	{
		// if we at the closest city, then do the airlift, or wait
		if (bAtClosestCity)
		{
			// can we do the airlift this turn?
			if (canAirliftAt(pClosestCity->plot(), pUpgradeCity->getX(), pUpgradeCity->getY()))
			{
				getGroup()->pushMission(MISSION_AIRLIFT, pUpgradeCity->getX(), pUpgradeCity->getY());
				return true;
			}
			// wait to do it next turn
			else
			{
				getGroup()->pushMission(MISSION_SKIP);
				return true;
			}
		}

		int iClosestCityPathTurns;
		bool const bCanPathToClosestCity = generatePath(pClosestCity->getPlot(),
				NO_MOVEMENT_FLAGS, true, &iClosestCityPathTurns);

		// is the closest city closer pathing? If so, move toward closest city
		if (bCanPathToClosestCity &&
			(!bCanPathToUpgradeCity || iClosestCityPathTurns < iUpgradeCityPathTurns))
		{
			pushGroupMoveTo(getPathEndTurnPlot(), NO_MOVEMENT_FLAGS, false, false,
					MISSIONAI_UPGRADE);
			return true;
		}
	}

	// did not have better airlift choice, go ahead and path to the upgrade city
	if (pUpgradeCityEndTurnPlot != NULL)
	{
		pushGroupMoveTo(*pUpgradeCityEndTurnPlot, NO_MOVEMENT_FLAGS, false, false,
				MISSIONAI_UPGRADE);
		return true;
	}

	return false;
}

/*	K-Mod. The bAirlift parameter now means that airlift cities will be priotised,
	but other cities are still accepted. */
bool CvUnitAI::AI_retreatToCity(bool bPrimary, bool bPrioritiseAirlift, int iMaxPath)
{
	PROFILE_FUNC(); // (advc: iMaxPath mostly unused here; changing that could save time.)

	//int iCurrentDanger = GET_PLAYER(getOwner()).AI_getPlotDanger(plot());
	int const iCurrentDanger = (getGroup()->alwaysInvisible() ? 0 : // K-Mod
			GET_PLAYER(getOwner()).AI_getPlotDanger(getPlot()));

	CvCityAI const* pCity = getPlot().AI_getPlotCity();
	if (iCurrentDanger <= 0 && pCity != NULL &&
		pCity->getOwner() == getOwner())
	{
		if (!bPrimary || GET_PLAYER(getOwner()).AI_isPrimaryArea(pCity->getArea()))
		{
			if (!bPrioritiseAirlift || pCity->getMaxAirlift() > 0)
			{	//if (!pCity->getPlot().isVisibleEnemyUnit(this)) {
				getGroup()->pushMission(MISSION_SKIP);
				return true;
			}
		}
	}
	//for (iPass = 0; iPass < 4; iPass++)
	/*  K-Mod. originally; pass 0 required the dest to have less plot danger
		unless the unit could fight;
		pass 1 was just an ordinary move;
		pass 2 was a 1 turn move with "ignore plot danger" and
		pass 3 was the full iMaxPath with ignore plot danger.
		I've changed it so that if the unit can fight, the pass 0 just skipped
		(because it's the same as the pass 1) and
		pass 2 is always skipped because it's a useless test.
		-- and I've renumbered the passes. */
	CvPlot* pBestPlot = NULL;
	int iShortestPath = MAX_INT;
	// <advc.139>
	bool bEvac = (pCity != NULL && pCity->AI_isEvacuating());
	bool bSafe = (pCity != NULL && pCity->AI_isSafe());
	// </advc.139>
	// <advc>
	int iPass = 0; // Used after the loop
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner()); // </advc>
	for (iPass = ((getGroup()->canDefend() &&
		getDomainType() == DOMAIN_LAND) // advc.001s
		? 1 : 0); iPass < 3; iPass++)
	{
		bool bNeedsAirlift = false;
		FOR_EACH_CITYAI(pLoopCity, kOwner)
		{
			if (!AI_plotValid(pLoopCity->plot()))
				continue;
			if (bPrimary && !kOwner.AI_isPrimaryArea(pLoopCity->getArea()))
				continue;
			if (bNeedsAirlift && pLoopCity->getMaxAirlift() == 0)
				continue;
			// <advc.139>
			/*  When evacuating, exclude other cities that also evacuate
				(and exclude the current city). */
			if (bEvac && pLoopCity->AI_isEvacuating())
				continue;
			/*  Avoid path and danger computation if we already know that we're safer
				where we are. */
			if (!pLoopCity->AI_isSafe() && (bSafe || iCurrentDanger <= 0 ||
				/*  Even when threatened at sea, a ship won't seek refuge in
					an unsafe city. */
				getDomainType() != DOMAIN_LAND))
			{
				continue;
			} // </advc.139>
			int iPathTurns=-1;
			if (generatePath(pLoopCity->getPlot(),
				iPass >= 2 ? MOVE_IGNORE_DANGER : NO_MOVEMENT_FLAGS, // was iPass >= 3
				true, &iPathTurns, iMaxPath))
			{/* (comment by jdog5000, 08/19/09)
				Water units can't defend a city
				Any unthreatened city acceptable on 0th pass, solves problem where sea units
				would oscillate in and out of threatened city because they had iCurrentDanger = 0
				on turns outside city */
				if (iPass > 0 || kOwner.AI_getPlotDanger(*pLoopCity->plot()) <= iCurrentDanger)
				{
					// If this is the first viable air-lift city, then reset iShortestPath.
					if (bPrioritiseAirlift && !bNeedsAirlift && pLoopCity->getMaxAirlift() > 0)
					{
						bNeedsAirlift = true;
						iShortestPath = MAX_INT;
					}
					if (iPathTurns < iShortestPath &&
					/*  <advc.139> Don't want to be ambushed while evacuating.
						Since I'm handling evacuation on a per-unit basis,
						it's impossible to say how much danger along the path is tolerable.
						Don't just want to use MOVE_IGNORE_DANGER b/c then a single enemy could
						stop a dozen units from evacuating. Using era isn't much better ...
						Moreover, I'm only considering the fastest path, not any detours
						that could be safer. Adding a iMaxDanger parameter to generatePath
						(or generalizing MOVE_IGNORE_DANGER) could help. */
						(!bEvac ||
						kOwner.AI_getPlotDanger(getPathEndTurnPlot()) <=
						kOwner.AI_getCurrEraFactor()))
						// </advc.139>
					{
						iShortestPath = iPathTurns;
						pBestPlot = &getPathEndTurnPlot();
					}
				}
			}
		}

		if (pBestPlot != NULL)
			break;

		if (getGroup()->alwaysInvisible())
			break;
	}

	if (pBestPlot != NULL)
	{
		if (at(*pBestPlot))
		{
			getGroup()->pushMission(MISSION_SKIP, -1, -1, NO_MOVEMENT_FLAGS,
					false, false, MISSIONAI_RETREAT);
		}
		else
		{
			pushGroupMoveTo(*pBestPlot,
					/*	was iPass >= 3
						advc (caveat): Flags here need to be consistent with those in the loop */
					iPass >= 2 ? MOVE_IGNORE_DANGER : NO_MOVEMENT_FLAGS,
					false, false, MISSIONAI_RETREAT);
		}
		return true;
	}

	if (pCity != NULL && pCity->getTeam() == getTeam())
	{
		if (bEvac && at(pCity->getPlot()) && // scorched earth
			 // Let's not be a griefer if we'll be dead
			kOwner.getNumCities() > 1 &&
			m_pUnitInfo->getUnitCaptureClassType() != NO_UNITCLASS)
		{
			/*	(Would be nice to check which player is about to capture the city -
				e.g. Barbarians don't capture units - but that's not worth the
				implementation effort.) */
			scaled rScrapOdds = per100(GC.getDefineINT(CvGlobals::
					BASE_UNIT_CAPTURE_CHANCE)) / 2;
			// Be more reluctant to scrap expensive units
			rScrapOdds *= 50; // production cost baseline
			rScrapOdds /= kOwner.getProductionNeeded(getUnitType()) /
					per100(GC.getInfo(GC.getGame().getGameSpeedType()).getTrainPercent());
			if (SyncRandSuccess(rScrapOdds))
			{
				scrap();
				return true;
			}
		} // </advc.010>
		getGroup()->pushMission(MISSION_SKIP, -1, -1, NO_MOVEMENT_FLAGS,
				false, false, MISSIONAI_RETREAT);
		return true;
	}

	return false;
}

/*	K-Mod: Decide whether or not this group is stranded.
	If they are stranded, try to walk towards the coast.
	If we're on the coast, wait to be rescued! */
bool CvUnitAI::AI_handleStranded(MovementFlags eFlags)
{
	PROFILE_FUNC();

	// <advc.001> No place to go
	if(GET_PLAYER(getOwner()).getNumCities() <= 0)
	{
		getGroup()->pushMission(MISSION_SKIP);
		return true;
	} // </advc.001>

	if (isCargo())
	{	// This is possible, in some rare cases, but I'm currently trying to pin down precisely what those cases are.
		//FErrorMsg("AI_handleStranded: this unit is already cargo."); // advc.006
		getGroup()->pushMission(MISSION_SKIP);
		return true;
	}

	if (isHuman())
		return false;

	const CvPlayerAI& kOwner = GET_PLAYER(getOwner());

	// return false if the group is not stranded.
	int iDummy=-1;
	if (getArea().getNumAIUnits(getOwner(), UNITAI_SETTLE) > 0 &&
		kOwner.AI_getNumAreaCitySites(getArea(), iDummy) > 0)
	{
		return false;
	}

	if (getArea().getNumCities() > 0)
	{
		//if (getPlot().getTeam() == getTeam())
		/*  advc.046: Don't see what good ownership of a teammate will do.
			Really need a path to one of our own cities. But, to save time,
			let's check (though rival borders could block the path): */
		if (getPlot().getOwner() == getOwner() &&
			getArea().getCitiesPerPlayer(getOwner()) > 0)
		{
			return false;
		}
		if (AI_getGroup()->AI_isHasPathToAreaPlayerCity(getOwner(), eFlags))
			return false;
		if ((canFight() || isSpy()) &&
			AI_getGroup()->AI_isHasPathToAreaEnemyCity(true, eFlags))
		{
			return false;
		}
	}

	// ok.. so the group is stranded.
	// Try to get to the coast.
	/*  advc.001: iMinWaterSize argument added to all three isCoastalLand checks in
		this function. Reaching a lake isn't good enough. */
	if (!getPlot().isCoastalLand(-1))
	{
		// maybe we were already on our way?
		CvPlot const* pMissionPlot = NULL;
		CvPlot const* pEndTurnPlot = NULL;
		if (AI_getGroup()->AI_getMissionAIType() == MISSIONAI_STRANDED)
		{
			pMissionPlot = AI_getGroup()->AI_getMissionAIPlot();
			if (pMissionPlot != NULL && pMissionPlot->isCoastalLand(-1) &&
				!pMissionPlot->isVisibleEnemyUnit(this) &&
				generatePath(*pMissionPlot, eFlags, true))
			{
				// The current mission looks good enough. Don't bother searching for a better option.
				pEndTurnPlot = &getPathEndTurnPlot();
			}
			else
			{
				// the current mission plot is not suitable. We'll have to search.
				pMissionPlot = 0;
			}
		}
		if (!pMissionPlot)
		{
			// look for the clostest coastal plot in this area
			int iShortestPath = MAX_INT;

			for (int i = 0; i < GC.getMap().numPlots(); i++)
			{
				CvPlot const& kLoopPlot = GC.getMap().getPlotByIndex(i);
				if (kLoopPlot.isArea(getArea()) && kLoopPlot.isCoastalLand(-1))
				{
					// TODO: check that the water isnt' blocked by ice.
					// advc.030 (comment): ^Should be guaranteed by pLoopPlot->isArea(getArea()) now
					int iPathTurns;
					if (generatePath(kLoopPlot, eFlags, true, &iPathTurns, iShortestPath))
					{
						FAssert(iPathTurns <= iShortestPath);
						iShortestPath = iPathTurns;
						pEndTurnPlot = &getPathEndTurnPlot();
						pMissionPlot = &kLoopPlot;
						if (iPathTurns <= 1)
							break;
					}
				}
			}
		}

		if (pMissionPlot != NULL)
		{
			pushGroupMoveTo(*pEndTurnPlot, eFlags, false, false,
					MISSIONAI_STRANDED, pMissionPlot);
			return true;
		}
	}

	/*	Hopefully we're on the coast.
		(but we might not be - if we couldn't find a path to the coast)
		try to load into a passing boat
		Calling AI_load will check all of our boats; so before we do that,
		I'm going to just see if there are any boats on adjacent plots. */
	FOR_EACH_ADJ_PLOT(getPlot())
	{
		if (canLoadOntoAnyUnit(*pAdj))
		{
			/*	ok. there is something we can load into - but lets use the
				(slow) official function to actually issue the load command. */
			if (AI_load(NO_UNITAI, NO_MISSIONAI, NO_UNITAI, -1, -1, -1, -1, eFlags, 1))
				return true;
			else // if that didn't do it, nothing will
				break;
		}
	}

	// raise the 'stranded' flag, and wait to be rescued.
	getGroup()->pushMission(MISSION_SKIP, -1, -1, NO_MOVEMENT_FLAGS,
			false, false, MISSIONAI_STRANDED, plot());
	return true;
}


bool CvUnitAI::AI_pickup(UnitAITypes eUnitAI,
	// BETTER_BTS_AI_MOD, Naval AI, 01/15/09, jdog5000:
	bool bCountProduction, int iMaxPath)
{
	PROFILE_FUNC();

	if (cargoSpace() <= 0)
	{
		FAssert(cargoSpace() > 0);
		return false;
	}

	CvCityAI* pCity = getPlot().AI_getPlotCity();
	if (pCity != NULL && pCity->getOwner() == getOwner())
	{	/*if (pCity->getPlot().plotCount(PUF_isUnitAIType, eUnitAI, -1, getOwner()) > 0) {
			if ((AI_getUnitAIType() != UNITAI_ASSAULT_SEA) || pCity->AI_isDefended(-1)) {*/ // BtS
		// BETTER_BTS_AI_MOD, Naval AI, 01/23/09, jdog5000: START
		if (GC.getGame().getGameTurn() - pCity->getGameTurnAcquired() > 15 ||
			GET_TEAM(getTeam()).AI_countEnemyPowerByArea(pCity->getArea()) == 0)
		{
			if (AI_considerPickup(eUnitAI, *pCity)) // advc: Moved into subroutine
			{
				// only count units which are available to load
				int iCount = pCity->getPlot().plotCount(PUF_isAvailableUnitAITypeGroupie,
						eUnitAI, -1, getOwner(), NO_TEAM, PUF_isFiniteRange);

				if (bCountProduction && pCity->getProductionUnitAI() == eUnitAI)
				{
					if (pCity->getProductionTurnsLeft() < 4)
					{
						CvUnitInfo& kUnitInfo = GC.getInfo(pCity->getProductionUnit());
						if (kUnitInfo.getDomainType() != DOMAIN_AIR || kUnitInfo.getAirRange() > 0)
						{
							iCount++;
						}
					}
				}
				if (GET_PLAYER(getOwner()).AI_plotTargetMissionAIs(pCity->getPlot(), MISSIONAI_PICKUP, getGroup()) <
					(iCount + cargoSpace() - 1) / cargoSpace())
				{
					getGroup()->pushMission(MISSION_SKIP, -1, -1, NO_MOVEMENT_FLAGS,
							false, false, MISSIONAI_PICKUP, pCity->plot());
					return true;
				}
			}
		} // BETTER_BTS_AI_MOD: END
	}

	int iBestValue = 0;
	CvPlot* pBestPlot = NULL;
	CvPlot* pBestPickupPlot = NULL;
	FOR_EACH_CITYAI(pLoopCity, GET_PLAYER(getOwner()))
	{
		if (!AI_plotValid(pLoopCity->plot()))
			continue;

		// BETTER_BTS_AI_MOD, Naval AI, 01/23/09, jdog5000: START
		if (GC.getGame().getGameTurn() - pLoopCity->getGameTurnAcquired() <= 15 &&
			GET_TEAM(getTeam()).AI_countEnemyPowerByArea(pLoopCity->getArea()) > 0)
		{
			continue;
		}
		if (!AI_considerPickup(eUnitAI, *pLoopCity)) // advc: Moved into subroutine
			continue;

		// only count units which are available to load, have had a chance to move since being built
		int iCount = pLoopCity->getPlot().plotCount(PUF_isAvailableUnitAITypeGroupie,
				eUnitAI, -1, getOwner(), NO_TEAM, (bCountProduction ?
				PUF_isFiniteRange : PUF_isFiniteRangeAndNotJustProduced));
		int iValue = iCount * 10;

		if (bCountProduction && (pLoopCity->getProductionUnitAI() == eUnitAI))
		{
			CvUnitInfo& kUnitInfo = GC.getInfo(pLoopCity->getProductionUnit());
			if (kUnitInfo.getDomainType() != DOMAIN_AIR || kUnitInfo.getAirRange() > 0)
			{
				iValue++;
				iCount++;
			}
		}

		if (iValue <= 0)
			continue;

		iValue += pLoopCity->getPopulation();
		/*if (pLoopCity->getPlot().isVisibleEnemyUnit(this)) // advc.opt: It's our city
			continue;*/

		if (GET_PLAYER(getOwner()).AI_plotTargetMissionAIs(
			pLoopCity->getPlot(), MISSIONAI_PICKUP, getGroup()) <
			(iCount + cargoSpace() - 1) / cargoSpace())
		{
			if (!pLoopCity->AI_isDanger())
				continue;

			int iPathTurns;
			if (atPlot(pLoopCity->plot()) ||
				!generatePath(pLoopCity->getPlot(), MOVE_AVOID_ENEMY_WEIGHT_3,
				true, &iPathTurns))
			{
				continue;
			}
			if (AI_getUnitAIType() == UNITAI_ASSAULT_SEA)
			{
				if (pLoopCity->getArea().getAreaAIType(getTeam()) == AREAAI_ASSAULT)
					iValue *= 4;
				else if (pLoopCity->getArea().getAreaAIType(getTeam()) == AREAAI_ASSAULT_ASSIST)
					iValue *= 2;
			}
			iValue *= 1000;
			iValue /= (iPathTurns + 3);
			if (iValue > iBestValue && iPathTurns <= iMaxPath)
			{
				iBestValue = iValue;
				/*  Do one turn along path, then reevaluate
					Causes update of destination based on troop movement */
				//pBestPlot = pLoopCity->plot();
				pBestPlot = &getPathEndTurnPlot();
				pBestPickupPlot = pLoopCity->plot();
				if (pBestPlot == NULL || atPlot(pBestPlot))
				{
					//FAssert(false);
					pBestPlot = pBestPickupPlot;
				}
			}
		}
	} // BETTER_BTS_AI_MOD: END

	if (pBestPlot != NULL && pBestPickupPlot != NULL)
	{
		pushGroupMoveTo(*pBestPlot, MOVE_AVOID_ENEMY_WEIGHT_3, false, false,
				MISSIONAI_PICKUP, pBestPickupPlot);
		return true;
	}

	return false;
}

// advc: Duplicate code cut from CvUnitAI::AI_pickup
bool CvUnitAI::AI_considerPickup(UnitAITypes eUnitAI, CvCityAI const& kCity) const
{
	// BETTER_BTS_AI_MOD, Naval AI, 01/23/09, jdog5000: START
	bool bConsider = false;
	if(AI_getUnitAIType() == UNITAI_ASSAULT_SEA)
	{
		if(kCity.getArea().getAreaAIType(getTeam()) == AREAAI_DEFENSIVE)
			bConsider = false;
		else if(eUnitAI == UNITAI_ATTACK_CITY && !kCity.AI_isDanger())
		{	// Improve island hopping
			bConsider = (kCity.getPlot().plotCount(PUF_canDefend, -1, -1,
					getOwner(), NO_TEAM, PUF_isDomainType, DOMAIN_LAND) >
					kCity.AI_neededDefenders());
		}
		else bConsider = kCity.AI_isDefended(-1);
	}
	else if(AI_getUnitAIType() == UNITAI_SETTLER_SEA)
	{
		if(eUnitAI == UNITAI_CITY_DEFENSE)
		{
			bConsider = (kCity.getPlot().plotCount(PUF_canDefendGroupHead, -1, -1,
					getOwner(), NO_TEAM, PUF_isCityAIType) > 1);
		}
		else bConsider = true;
	}
	else bConsider = true;
	return bConsider;
	// BETTER_BTS_AI_MOD: END
}

/*	BETTER_BTS_AI_MOD, Naval AI, 02/22/10, jdog5000:
	(this function has been significantly edited for K-Mod) */
bool CvUnitAI::AI_pickupStranded(UnitAITypes eUnitAI, int iMaxPath)
{
	PROFILE_FUNC();
	FAssert(iMaxPath >= 0); // advc (use MAX_INT for infinity)

	FAssert(cargoSpace() > 0);
	if (cargoSpace() <= 0)
		return false;

	if (isBarbarian())
		return false;

	CvPlayerAI& kPlayer = GET_PLAYER(getOwner());

	int iBestValue = 0;
	CvUnit* pBestUnit = 0;
	CvPlot* pEndTurnPlot = 0;
	FOR_EACH_GROUPAI_VAR(pLoopGroup, kPlayer)
	{
		if (!pLoopGroup->AI_isStranded())
			continue;

		CvUnit* pHeadUnit = pLoopGroup->getHeadUnit();
		if (pHeadUnit == NULL)
			continue;

		if (eUnitAI != NO_UNITAI && pHeadUnit->AI_getUnitAIType() != eUnitAI)
			continue;

		//pLoopPlot = pHeadUnit->plot();
		CvPlot* pPickupPlot = pLoopGroup->AI_getMissionAIPlot(); // K-Mod
		if (pPickupPlot == NULL)
			continue;

		if (!pPickupPlot->isCoastalLand()  && !canMoveAllTerrain())
			continue;

		// Units are stranded, attempt rescue

		int iCount = pLoopGroup->getNumUnits();
		if (1000 * iCount > iBestValue)
		{
			CvPlot* pTargetPlot = NULL;
			int iPathTurns = MAX_INT;
			// <advc.001> This can happen, apparently.
			if (at(*pPickupPlot))
			{
				pTargetPlot = pPickupPlot;
				iPathTurns = 0;
			}
			else // </advc.001>
			{
				// advc.046: Don't choose an arbitrary adjacent plot
				int iBestAdjTurns = MAX_INT;
				FOR_EACH_ADJ_PLOT(*pPickupPlot)
				{
					if ((at(*pAdj) ||
						canMoveInto(*pAdj)) &&
						generatePath(*pAdj, NO_MOVEMENT_FLAGS, true, &iPathTurns, iMaxPath) &&
						iPathTurns < iBestAdjTurns) // advc.046
					{
						pTargetPlot = &getPathEndTurnPlot();
						//break;
						iBestAdjTurns = iPathTurns; // advc.046
					}
				}
				iPathTurns = iBestAdjTurns; // advc.046
			}
			if (pTargetPlot != NULL)
			{
				FAssert(iPathTurns <= iMaxPath);
				FAssert(iPathTurns >= 0); // advc
				MissionAITypes eMissionAIType = MISSIONAI_PICKUP;
				iCount -= cargoSpace() * kPlayer.AI_unitTargetMissionAIs( // estimate
						*pHeadUnit, &eMissionAIType, 1, getGroup(), iPathTurns);

				int iValue = 1000 * iCount;
				iValue /= iPathTurns + 1;
				if (iValue > iBestValue)
				{
					iBestValue = iValue;
					pBestUnit = pHeadUnit;
					pEndTurnPlot = pTargetPlot;
				}
			}
		}
	}

	if (pBestUnit == NULL)
		return false;
	// <advc.046>
	int iCargo = getGroup()->getCargo();
	if (iCargo > 0)
	{
		/*  Only unload the current cargo if the stranded units aren't too few
			or too far away. */
		if(iCargo * 150 > iBestValue || atPlot(pEndTurnPlot))
			return false;
		if(!getPlot().isCity() || getPlot().getOwner() != getOwner())
			return false;
		getGroup()->unloadAll();
		if(getGroup()->hasCargo())
			return false;
	} // </advc.046>
	if (at(*pEndTurnPlot))
	{
		getGroup()->pushMission(MISSION_SKIP, -1, -1, NO_MOVEMENT_FLAGS,
				false, false, MISSIONAI_PICKUP, 0, pBestUnit);
		return true;
	}
	else
	{
		FAssert(!at(pBestUnit->getPlot()));
		//getGroup()->pushMission(MISSION_MOVE_TO_UNIT, pBestUnit->getOwner(), pBestUnit->getID(), MOVE_AVOID_ENEMY_WEIGHT_3, false, false, MISSIONAI_PICKUP, NULL, pBestUnit);
		pushGroupMoveTo(*pEndTurnPlot, NO_MOVEMENT_FLAGS, false, false,
				MISSIONAI_PICKUP, 0, pBestUnit);
		return true;
	}
}


bool CvUnitAI::AI_airOffensiveCity()
{
	PROFILE_FUNC();

	FAssert(canAirAttack() || isNuke());

	int iBestValue = 0;
	CvPlot const* pBestPlot = NULL;
	for (int i = 0; i < GC.getMap().numPlots(); i++)
	{
		CvPlot const& kPlot = GC.getMap().getPlotByIndex(i);
		// BETTER_BTS_AI_MOD, Air AI, 04/25/08, jdog5000
		// Limit to cities and forts, true for any city but only this team's forts.
		/*if (kPlot.isCity(true, getTeam()) &&
			(kPlot.getTeam() == getTeam() || (kPlot.isOwned() &&
			GET_TEAM(kPlot.getTeam()).isVassal(getTeam())))) { ... }*/
		// <advc>
		if (!GET_TEAM(getTeam()).isRevealedAirBase(kPlot))
			continue; // </advc>
		if (at(kPlot) || canMoveInto(kPlot))
		{
			int iValue = AI_airOffenseBaseValue(kPlot);
			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				pBestPlot = &kPlot;
			}
		}
	}
	if (pBestPlot != NULL && !at(*pBestPlot))
	{
		pushGroupMoveTo(*pBestPlot, MOVE_SAFE_TERRITORY);
		return true;
	}
	// BETTER_BTS_AI_MOD: END
	return false;
}

/*  BETTER_BTS_AI_MOD, Air AI, 04/25/10, jdog5000:
	Function for ranking the value of a plot as a base for offensive air units */
int CvUnitAI::AI_airOffenseBaseValue(CvPlot const& kPlot) // advc: param was CvPlot*
{
	// (advc: some unused/ redundant code deleted)

	int iAttackAirCount = kPlot.plotCount(PUF_canAirAttack, -1, -1, NO_PLAYER, getTeam());
	iAttackAirCount += 2 * kPlot.plotCount(PUF_isUnitAIType, UNITAI_ICBM, -1, NO_PLAYER, getTeam());
	if (at(kPlot))
	{
		if (canAirAttack())
			iAttackAirCount -= 1;
		if (isNuke())
			iAttackAirCount -= 2;
	}
	int iDefenders = kPlot.plotCount(PUF_canDefend, -1, -1, kPlot.getOwner(),
			NO_TEAM, PUF_isDomainType, DOMAIN_LAND); // advc.001s
	if (kPlot.isCoastalLand(-1))
		iDefenders -= 1;

	CvCityAI const* pCity = kPlot.AI_getPlotCity();
	if (pCity != NULL)
	{
		if (pCity->getDefenseModifier(true) < 40)
			iDefenders -= 1;
		if (pCity->getOccupationTimer() > 1)
			iDefenders -= 1;
	}

	// Consider threat from nearby enemy territory
	int iBorderDanger = 0;
	for (SquareIter it(kPlot, 1); it.hasNext(); ++it)
	{
		CvPlot const& p = *it;
		if (p.sameArea(kPlot) && p.isOwned())
		{	// <advc.001i>
			if(!p.isRevealed(getTeam()))
				continue; // </advc.001i>
			if(p.getTeam() != getTeam() &&
				GET_TEAM(p.getTeam()).isVassal(getTeam()))
			{
				int const iDistance = it.currStepDist();
				if (iDistance == 1)
					iBorderDanger++;
				if (::atWar(p.getTeam(), getTeam()))
				{
					if (iDistance == 1)
						iBorderDanger += 2;
					else if (iDistance == 2 && p.//isRoute()
						getRevealedRouteType(getTeam())) // advc.001i
					{
						iBorderDanger += 2;
					}
				}
			}
		}
	}
	iDefenders -= std::min(2, (iBorderDanger + 1) / 3);

	// Don't put more attack air units on plot than effective land defenders ... too large a risk
	if (iAttackAirCount >= iDefenders || iDefenders <= 0)
		return 0;

	int iValue = 0;
	bool const bAnyWar = GET_TEAM(getTeam()).AI_isAnyWarPlan();
	if (bAnyWar)
	{
		/*	Don't count assault assist, don't want to weight
			defending colonial coasts when homeland might be under attack */
		bool const bAssault = (kPlot.getArea().getAreaAIType(getTeam()) == AREAAI_ASSAULT ||
				kPlot.getArea().getAreaAIType(getTeam()) == AREAAI_ASSAULT_MASSING);

		// Loop over operational range
		int const iRange = airRange();
		for (PlotCircleIter it(kPlot, iRange); it.hasNext(); ++it)
		{
			CvPlot const& p = *it;
			TeamTypes const eLoopTeam = p.getTeam(); // advc
			// Value system is based around 1 enemy military unit in our territory = 10 pts
			int iTempValue = 0;
			if (p.isWater())
			{
				if (p.isVisible(getTeam()) && !p.getArea().isLake())
				{
					// Defend ocean
					iTempValue = 1;
					if (eLoopTeam != NO_TEAM)
					{
						if (eLoopTeam == getTeam())
							iTempValue += 1;
						else if (eLoopTeam != getTeam() &&
							GET_TEAM(getTeam()).AI_getWarPlan(eLoopTeam) != NO_WARPLAN)
						{
							iTempValue += 1;
						}
					}
					// Low weight for visible ships cause they will probably move
					iTempValue += 2 * p.getNumVisibleEnemyDefenders(this);
					if (bAssault)
						iTempValue *= 2;
				}
			}
			else
			{
				int const iDistance = it.currPlotDist();
				if (eLoopTeam == NO_TEAM)
				{
					if (iDistance < iRange - 2)
					{
						// Target enemy troops in neutral territory
						iTempValue += 4 * p.getNumVisibleEnemyDefenders(this);
					}
				}
				else if (eLoopTeam == getTeam())
				{
					iTempValue = 0;
					if (iDistance < iRange - 2)
					{
						// Target enemy troops in our territory
						iTempValue += 5 * p.getNumVisibleEnemyDefenders(this);
						if (p.getOwner() == getOwner())
						{
							if (GET_PLAYER(getOwner()).AI_isPrimaryArea(p.getArea()))
								iTempValue *= 3;
							else iTempValue *= 2;
						}
						bool bDefensive = (p.getArea().
								getAreaAIType(getTeam()) == AREAAI_DEFENSIVE);
						if (bDefensive)
							iTempValue *= 2;
					}
				}
					else if (eLoopTeam != getTeam() && GET_TEAM(getTeam()).
						AI_getWarPlan(eLoopTeam) != NO_WARPLAN)
					{
					// Attack opponents land territory
					iTempValue = 3;
					CvCityAI const* pLoopCity = p.AI_getPlotCity();
					if (pLoopCity != NULL)
					{
						// Target enemy cities
						iTempValue += (3*pLoopCity->getPopulation() + 30);

						//if (canAirBomb(pPlot) && pLoopCity->isBombardable(this))
						if (canAirBombAt(pLoopCity->getPlot(), &kPlot)) // K-Mod
							iTempValue *= 2;
						if (p.getArea().AI_getTargetCity(getOwner()) == pLoopCity)
							iTempValue *= 2;
						if (pLoopCity->AI_isDanger())
						{
							/*	Multiplier for nearby troops, ours, teammate's,
								and any other enemy of city */
							iTempValue *= 3;
						}
					}
					else
					{
						if (iDistance < iRange - 2)
						{
							// Support our troops in enemy territory
							iTempValue += 15 * p.getNumDefenders(getOwner());

							// Target enemy troops adjacent to our territory
							if (p.isAdjacentTeam(getTeam(),true))
								iTempValue += 7 * p.getNumVisibleEnemyDefenders(this);
						}

						// Weight resources
						if (canAirBombAt(p, &kPlot))
						{
							if (p.getBonusType(getTeam()) != NO_BONUS)
							{
								iTempValue += 8 * std::max(2, GET_PLAYER(p.getOwner()).
										AI_bonusVal(p.getBonusType(getTeam()), 0) / 10);
							}
						}
					}

					if (p.getArea().getAreaAIType(getTeam()) == AREAAI_OFFENSIVE)
					{
						// Extra weight for enemy territory in offensive areas
						iTempValue *= 2;
					}

					if (GET_PLAYER(getOwner()).AI_isPrimaryArea(p.getArea()))
					{
						iTempValue *= 3;
						iTempValue /= 2;
					}

					if (p.isBarbarian())
						iTempValue /= 2;
				}
			}
			iValue += iTempValue;
		}

		// Consider available defense, direct threat to potential base
		// K-Mod
		int iOurDefense = GET_PLAYER(getOwner()).AI_localDefenceStrength(
				&kPlot, getTeam(), DOMAIN_LAND, 0);
		int iEnemyOffense = GET_PLAYER(getOwner()).AI_localAttackStrength(
				&kPlot, NO_TEAM, DOMAIN_LAND, 2);
		// K-Mod end

		if (3 * iEnemyOffense > iOurDefense || iOurDefense == 0)
		{
			iValue *= iOurDefense;
			iValue /= std::max(1,3*iEnemyOffense);
		}

		// Value forts less, they are generally riskier bases
		if (pCity == NULL)
		{
			iValue *= 2;
			iValue /= 3;
		}
	}
	else
	{
		if (kPlot.getOwner() != getOwner())
		{
			// Keep planes at home when not in real wars
			return 0;
		}

		// If no wars, use prior logic with added value to keeping planes safe from sneak attack
		if (pCity != NULL)
		{
			/*iValue = (pCity->getPopulation() + 20);
			iValue += pCity->AI_cityThreat();*/ // BtS

			/*	K-Mod. Try not to waste airspace which we need for air defenders;
				but use the needed air defenders as a proxy for good offense placement.
				AI_cityThreat has arbitrary scale, so it
				should not be added to population like that.
				(the rest of this function still needs some work,
				but this bit was particularly problematic.) */
			int iDefNeeded = pCity->AI_neededAirDefenders();
			int iDefHere = kPlot.plotCount(PUF_isAirIntercept, -1, -1, NO_PLAYER, getTeam()) -
					(at(kPlot) && PUF_isAirIntercept(this, -1, -1) ? 1 : 0);
			int iSpace = kPlot.airUnitSpaceAvailable(getTeam()) +
					(at(kPlot) ? 1 : 0);
			iValue = pCity->getPopulation() + 20;
			iValue *= std::min(iDefNeeded+1, iDefHere+iSpace);
			if (iDefNeeded > iSpace+iDefHere)
			{
				FAssert(iDefNeeded > 0);
				// drop value to zero if we can't even fit half of the air defenders we need here.
				iValue *= 2*(iSpace+iDefHere) - iDefNeeded;
				iValue /= iDefNeeded;
			}
			// K-Mod end
		}
		else
		{
			if (iDefenders > 0)
			{
				iValue = (pCity != NULL) ? 0 :
						GET_PLAYER(getOwner()).AI_getPlotAirbaseValue(kPlot);
				iValue /= 6;
			}
		}

		iValue += std::min(24, 3*(iDefenders - iAttackAirCount));

		if (GET_PLAYER(getOwner()).AI_isPrimaryArea(kPlot.getArea()))
		{
			iValue *= 4;
			iValue /= 3;
		}

		/*	No real enemies, check for minor civ or barbarian cities
			where attacks could be supported */
		CvCity* pNearestEnemyCity = GC.getMap().findCity(kPlot.getX(), kPlot.getY(),
				NO_PLAYER, NO_TEAM, false, false, getTeam());

		if (pNearestEnemyCity != NULL)
		{
			int iDistance = ::plotDistance(kPlot.getX(), kPlot.getY(),
					pNearestEnemyCity->getX(), pNearestEnemyCity->getY());
			if (iDistance > airRange())
				iValue /= 10 * (2 + airRange());
			else iValue /= 2 + iDistance;
		}
	}

	if (kPlot.getOwner() == getOwner())
	{
		// Bases in our territory better than teammate's
		iValue *= 2;
	}
	else if (kPlot.getTeam() == getTeam())
	{
		// Our team's bases are better than vassal plots
		iValue *= 3;
		iValue /= 2;
	}

	return iValue;
}

// Most of this function has been rewritten for K-Mod, using bbai as the base version. (old code deleted.)
bool CvUnitAI::AI_airDefensiveCity()
{
	PROFILE_FUNC();

	const CvPlayerAI& kOwner = GET_PLAYER(getOwner()); // K-Mod

	FAssert(getDomainType() == DOMAIN_AIR);
	FAssert(canAirDefend());

	if (canAirDefend() && getDamage() == 0)
	{
		CvCityAI* pCity = getPlot().AI_getPlotCity();
		if (pCity != NULL && pCity->getOwner() == getOwner())
		{
			int iExistingAirDefenders = getPlot().plotCount(PUF_isAirIntercept, -1, -1, getOwner());
			if (PUF_isAirIntercept(this, -1, -1))
				iExistingAirDefenders--;
			int iNeedAirDefenders = pCity->AI_neededAirDefenders();

			if (iExistingAirDefenders < iNeedAirDefenders/2 && iExistingAirDefenders < 3)
			{
				// Be willing to defend with a couple of planes even if it means their doom.
				getGroup()->pushMission(MISSION_AIRPATROL);
				return true;
			}

			if (iExistingAirDefenders < iNeedAirDefenders)
			{
				// Stay if city is threatened or if we're well short of our target, but not if capture is imminent.
				int iEnemyOffense = kOwner.AI_localAttackStrength(plot(), NO_TEAM, DOMAIN_LAND, 2);

				if (iEnemyOffense > 0 || iExistingAirDefenders < iNeedAirDefenders/2)
				{
					int iOurDefense = kOwner.AI_localDefenceStrength(plot(), getTeam());
					if (iEnemyOffense < iOurDefense)
					{
						getGroup()->pushMission(MISSION_AIRPATROL);
						return true;
					}
				}
			}
		}
	}

	int iBestValue = 0;
	CvPlot* pBestPlot = NULL;
	FOR_EACH_CITYAI(pLoopCity, kOwner)
	{
		if (!canAirDefend(pLoopCity->plot()))
			continue;

		if (!atPlot(pLoopCity->plot()) && !canMoveInto(*pLoopCity->plot()))
			continue;

		bool bCurrentPlot = atPlot(pLoopCity->plot());

		int iExistingAirDefenders = pLoopCity->getPlot().plotCount(PUF_isAirIntercept, -1, -1, pLoopCity->getOwner());
		if (bCurrentPlot && PUF_isAirIntercept(this, -1, -1))
			iExistingAirDefenders--;
		int iNeedAirDefenders = pLoopCity->AI_neededAirDefenders();
		int iAirSpaceAvailable = pLoopCity->getPlot().airUnitSpaceAvailable(kOwner.getTeam()) + (bCurrentPlot ? 1 : 0);

		if (iNeedAirDefenders > iExistingAirDefenders || iAirSpaceAvailable > 1)
		{
			/* int iValue = pLoopCity->getPopulation() + pLoopCity->AI_cityThreat();
			iValue *= 100;
			iValue *= std::max(1, 3 + iNeedAirDefenders - iExistingAirDefenders); */
			// K-Mod note: AI_cityThreat is too expensive for this stuff, and it's already taken into account by AI_neededAirDefenders anyway

			int iOurDefense = kOwner.AI_localDefenceStrength(pLoopCity->plot(), getTeam(), DOMAIN_LAND, 0);
			int iEnemyOffense = kOwner.AI_localAttackStrength(pLoopCity->plot(), NO_TEAM, DOMAIN_LAND, 2);

			int iValue = 10 + iAirSpaceAvailable;
			iValue *= 10 * std::max(0, iNeedAirDefenders - iExistingAirDefenders) + 1;

			if (bCurrentPlot && iAirSpaceAvailable > 1)
				iValue = iValue * 4/3;

			if (kOwner.AI_isPrimaryArea(pLoopCity->getArea()))
			{
				iValue *= 4;
				iValue /= 3;
			}

			if (!pLoopCity->isPreviousOwner(getOwner()))
			{
				iValue *= (GC.getGame().getGameTurn() - pLoopCity->getGameTurnAcquired() < 20 ? 3 : 4);
				iValue /= 5;
			}

			// Reduce value of endangered city, it may be too late to help
			if (iEnemyOffense > 0)
			{
				if (iOurDefense == 0)
					iValue = 0;
				else if (iEnemyOffense*4 > iOurDefense*3)
				{
					// note: this will drop to zero when iEnemyOffense = 1.5 * iOurDefence.
					iValue *= 6*iOurDefense - 4*iEnemyOffense;
					iValue /= 3*iOurDefense;
				}
			}

			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				pBestPlot = pLoopCity->plot();
			}
		}
	}

	if (pBestPlot != NULL && !at(*pBestPlot))
	{
		pushGroupMoveTo(*pBestPlot);
		return true;
	}

	return false;
}


bool CvUnitAI::AI_airCarrier()
{
	//PROFILE_FUNC();
	const CvPlayerAI& kOwner = GET_PLAYER(getOwner()); // K-Mod

	if (getCargo() > 0)
	{
		return false;
	}

	if (isCargo())
	{
		if (canAirDefend())
		{
			getGroup()->pushMission(MISSION_AIRPATROL);
			return true;
		}
		else
		{
			getGroup()->pushMission(MISSION_SKIP);
			return true;
		}
	}

	int iBestValue = 0;
	CvUnit* pBestUnit = NULL;
	FOR_EACH_UNIT_VAR(pLoopUnit, kOwner)
	{
		CvPlot const& kLoopPlot = pLoopUnit->getPlot();
		if (!canLoadOnto(*pLoopUnit, kLoopPlot))
			continue;
		int iValue = 10;
		if (!kLoopPlot.isCity())
			iValue += 20;
		if (kLoopPlot.isOwned())
		{
			if (isEnemy(kLoopPlot.getTeam()))
				iValue += 20;
		}
		else iValue += 10;
		iValue /= (pLoopUnit->getCargo() + 1);
		if (iValue > iBestValue)
		{
			iBestValue = iValue;
			pBestUnit = pLoopUnit;
		}
	}

	if (pBestUnit != NULL)
	{
		if (at(pBestUnit->getPlot()))
		{
			// XXX is this dangerous (not pushing a mission...) XXX air units?
			setTransportUnit(pBestUnit);
			return true;
		}
		else
		{
			pushGroupMoveTo(pBestUnit->getPlot());
			return true;
		}
	}

	return false;
}


bool CvUnitAI::AI_missileLoad(UnitAITypes eTargetUnitAI, int iMaxOwnUnitAI, bool bStealthOnly)
{
	//PROFILE_FUNC();

	CvUnit* pBestUnit = NULL;
	int iBestValue = 0;
	CvPlayer const& kOwner = GET_PLAYER(getOwner());
	FOR_EACH_UNIT_VAR(pLoopUnit, kOwner)
	{
		if ((!bStealthOnly || pLoopUnit->getInvisibleType() != NO_INVISIBLE) &&
			pLoopUnit->AI_getUnitAIType() == eTargetUnitAI &&
			(iMaxOwnUnitAI == -1 ||
			pLoopUnit->getUnitAICargo(AI_getUnitAIType()) <= iMaxOwnUnitAI) &&
			canLoadOnto(*pLoopUnit, pLoopUnit->getPlot()))
		{
			int iValue = 100;
			iValue += SyncRandNum(100);
			iValue *= 1 + pLoopUnit->getCargo();
			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				pBestUnit = pLoopUnit;
			}
		}
	}
	if (pBestUnit != NULL)
	{
		if (at(pBestUnit->getPlot()))
		{
			// XXX is this dangerous (not pushing a mission...) XXX air units?
			setTransportUnit(pBestUnit);
			return true;
		}
		else
		{
			pushGroupMoveTo(pBestUnit->getPlot());
			setTransportUnit(pBestUnit);
			return true;
		}
	}
	return false;
}

// BETTER_BTS_AI_MOD, Air AI, 9/16/08, jdog5000: START
/*	K-Mod. I'm rewritten this function so that it now considers
	bombarding city defences and bombing improvements as well as
	air strikes against enemy troops. Also, it now prefers to
	hit targets that are in our territory. */
// (advc: The BBAI function was called "AI_defensiveAirStrike")
bool CvUnitAI::AI_airStrike(int iThreshold)
{
	PROFILE_FUNC();

	int iBestValue = iThreshold + isSuicide() && getUnitInfo().getProductionCost() > 0 ?
			getUnitInfo().getProductionCost() * 5 / 6 : 0;
	CvPlot const* pBestPlot = NULL;
	bool bBombard = false; // K-Mod. bombard (city / improvement), rather than air strike (damage)
	for (SquareIter it(*this, airRange(), false); it.hasNext(); ++it)
	{
			CvPlot const& p = *it;
			// <advc.opt>
			if (!p.isRevealed(getTeam()))
				continue; // </advc.opt>
			// <advc>
			bool bBombardLoop=false;
			// Moved most of the loop body into a new function
			int iValue = AI_airStrikeValue(p, iBestValue, bBombardLoop);
			if (iValue > iBestValue)
			{
				bBombard = bBombardLoop;
				iBestValue = iValue; // </advc>
				pBestPlot = &p;
			}
	}
	if (pBestPlot != NULL)
	{
		if (bBombard)
			getGroup()->pushMission(MISSION_AIRBOMB, pBestPlot->getX(), pBestPlot->getY());
		else pushGroupMoveTo(*pBestPlot);
		return true;
	}

	return false;
}

/*  advc: Body cut from AI_airStrike in order to make the code easier to read.
	iCurrentBest is only for saving time. It's K-Mod code; comments are karadoc's. */
int CvUnitAI::AI_airStrikeValue(CvPlot const& kPlot, int iCurrentBest, bool& bBombard) const
{
	bBombard = false;

	int iStrikeValue = 0;
	int iBombValue = 0;
	int iAdjacentAttackers = 0; // (only count adjacent units if we can air-strike)
	int const iAssaultEnRoute = (!kPlot.isCity() ? 0 : GET_PLAYER(getOwner()).
			AI_plotTargetMissionAIs(kPlot, MISSIONAI_ASSAULT, getGroup(), 1));

	/*	TODO: consider changing the evaluation system so that
		instead of simply counting units, it counts attack / defence power. */

	// air strike (damage)
	if (canMoveInto(kPlot, true))
	{
		iAdjacentAttackers += GET_PLAYER(getOwner()).AI_adjacentPotentialAttackers(kPlot);
		//if (kPlot.isWater() || iPotentialAttackers > 0 || kPlot.isAdjacentTeam(getTeam()))
		{
			CvUnit* pDefender = kPlot.getBestDefender(NO_PLAYER, getOwner(), this, true);
			FAssert(pDefender != NULL);
			FAssert(pDefender->canDefend());

			int iDamage = airCombatDamage(pDefender);
			int iDefenders = kPlot.getNumVisibleEnemyDefenders(this);
			iStrikeValue = std::max(0,
					std::min(pDefender->getDamage() + iDamage, airCombatLimit())
					- pDefender->getDamage());
			iStrikeValue += iDamage * AI_collateralDmgFactor() *
					std::min(iDefenders - 1, collateralDamageMaxUnits()) / 200;
			iStrikeValue *= (3 + iAdjacentAttackers + iAssaultEnRoute / 2);
			iStrikeValue /= (iAdjacentAttackers + iAssaultEnRoute > 0 ? 4 : 6) +
					std::min(iAdjacentAttackers + iAssaultEnRoute / 2, iDefenders)/2;
			// Better not to strike units that heal easily
			//if (kPlot.isCity(true, pDefender->getTeam()))
			// <advc>
			if (GET_TEAM(pDefender->getTeam()).isCityHeal(kPlot))
			{	/*	(isRevealedCityHeal would use the same team
					for the heal and visibility checks) */
				ImprovementTypes eImprov = kPlot.getRevealedImprovementType(getTeam());
				if (eImprov != NO_IMPROVEMENT && GC.getInfo(eImprov).isActsAsCity())
				{	// </advc>
					iStrikeValue *= 3;
					iStrikeValue /= 4;
				}
			}
			if (kPlot.isWater() && (iAdjacentAttackers > 0 || kPlot.getTeam() == getTeam()))
				iStrikeValue *= 3;
			else if (kPlot.isAdjacentTeam(getTeam())) // prefer defensive strikes
				iStrikeValue *= 2;
		}
	}
	// bombard (destroy improvement / city defences)
	if (canAirBombAt(kPlot))
	{
		if (kPlot.isCity())
		{
			CvCity const* pCity = kPlot.getPlotCity();
			if(pCity->getDefenseModifier(true) > 0) // advc.004c
			{
				iBombValue = std::max(0, std::min(pCity->getDefenseDamage() +
						airBombCurrRate(), GC.getMAX_CITY_DEFENSE_DAMAGE()) -
						pCity->getDefenseDamage());
				iBombValue *= iAdjacentAttackers + 2*iAssaultEnRoute +
						(getArea().getAreaAIType(getTeam()) == AREAAI_OFFENSIVE ? 5 : 1);
				iBombValue /= 2;
			}
		}
		else
		{
			BonusTypes eBonus = kPlot.getNonObsoleteBonusType(getTeam(), true);
			if (eBonus != NO_BONUS && kPlot.isOwned() && canAirBombAt(kPlot))
			{
				iBombValue = GET_PLAYER(kPlot.getOwner()).AI_bonusVal(eBonus, -1);
				iBombValue += GET_PLAYER(kPlot.getOwner()).AI_bonusVal(eBonus, 0);
			}
		}
	}
	/*	factor in air defenses but try to avoid using bestInterceptor,
		because that's a slow function. */
	if (iBombValue <= iCurrentBest && iStrikeValue <= iCurrentBest)
		return 0; // values only decreased from here on.

	if (isSuicide())
	{
		iStrikeValue /= 2;
		iBombValue /= 2;
	}
	else if (!canAirDefend())
	{
		// assume that air defenders are strong.. and that they are willing to fight
		CvUnit* pInterceptor = bestInterceptor(kPlot,
				// advc.128: Don't always cheat with visibility (only 67% of the time)
				m_iSearchRangeRandPercent > 33);
		if (pInterceptor != NULL)
		{
			int iInterceptProb = pInterceptor->currInterceptionProbability();
			iInterceptProb *= std::max(0, (100 - evasionProbability()));
			iInterceptProb /= 100;

			iStrikeValue *= std::max(0, 100 - iInterceptProb / 2);
			iStrikeValue /= 100;

			iBombValue *= std::max(0, 100 - iInterceptProb / 2);
			iBombValue /= 100;
		}
	}
	bBombard = (iBombValue > iStrikeValue);
	return std::max(iBombValue, iStrikeValue);
}

// Air strike around base city
bool CvUnitAI::AI_defendBaseAirStrike()
{
	PROFILE_FUNC();

	CvPlot* pBestPlot = NULL;
	int iBestValue = (isSuicide() && getUnitInfo().getProductionCost() > 0) ?
			15 * getUnitInfo().getProductionCost() : 0;
	// Only search around base
	for (SquareIter it(*this, 2); it.hasNext(); ++it)
	{
		CvPlot& p = *it;
		if (!canMoveInto(p, true) || p.isWater() || !isArea(p.getArea()))
		{
			continue;
		}
		int iValue = 0;
		CvUnit const* pDefender = p.getBestDefender(NO_PLAYER, getOwner(), this, true);
		FAssert(pDefender != NULL);
		FAssert(pDefender->canDefend());

		int const iDamage = airCombatDamage(pDefender);
		iValue = std::max(0, (std::min((pDefender->getDamage() + iDamage),
				airCombatLimit()) - pDefender->getDamage()));
		iValue += ((iDamage * AI_collateralDmgFactor()) *
				std::min((p.getNumVisibleEnemyDefenders(this) - 1),
				collateralDamageMaxUnits())) / (2*100);

		// Weight towards stronger units
		iValue *= (pDefender->currCombatStr(NULL,NULL,NULL) + 2000);
		iValue /= 2000;

		// Weight towards adjacent stacks
		if (it.currStepDist() == 1)
		{
			iValue *= 5;
			iValue /= 4;
		}

		CvUnit const* pInterceptor = bestInterceptor(p,
				true); // advc.128: Don't need to cheat with visibility here I think
		if (pInterceptor != NULL)
		{
			int iInterceptProb = (isSuicide() ? 100 :
					pInterceptor->currInterceptionProbability());
			iInterceptProb *= std::max(0, (100 - evasionProbability()));
			iInterceptProb /= 100;
			iValue *= std::max(0, 100 - iInterceptProb / 2);
			iValue /= 100;
		}
		if (iValue > iBestValue)
		{
			iBestValue = iValue;
			pBestPlot = &p;
			FAssert(!atPlot(pBestPlot));
		}
	}

	if (pBestPlot != NULL)
	{
		pushGroupMoveTo(*pBestPlot);
		return true;
	}

	return false;
}
// BETTER_BTS_AI_MOD: END

bool CvUnitAI::AI_airBombPlots()
{
	//PROFILE_FUNC();
	CvPlot* pBestPlot = NULL;
	int iBestValue = 0;
	for (SquareIter it(*this, airRange(), false); it.hasNext(); ++it)
	{
		CvPlot& p = *it;
		if (p.isCity() || !p.isOwned() || !canAirBombAt(p))
			continue;
		int iValue = 0;
		if (p.getBonusType(p.getTeam()) != NO_BONUS &&
			p.isImproved()) // advc.255
		{
			iValue += AI_pillageValue(p, 15);
			iValue += SyncRandNum(10);
		}
		else if (isSuicide())
		{
			// AI_airBombPlots should only be reached when the unit is desperate to die
			iValue += AI_pillageValue(p);
			/*	Guided missiles lean towards destroying resource-producing tiles
				as opposed to improvements like Towns */
			if (p.getBonusType(p.getTeam()) != NO_BONUS)
			{
				iValue += GET_PLAYER(p.getOwner()).AI_bonusVal(
						p.getBonusType(p.getTeam()), 0);
			}
		}
		if (iValue <= 0)
			continue;
		/*pInterceptor = bestInterceptor(pLoopPlot);
		if (pInterceptor != NULL) {
			iInterceptProb = isSuicide() ? 100 : pInterceptor->currInterceptionProbability();
			iInterceptProb *= std::max(0, (100 - evasionProbability()));
			iInterceptProb /= 100;
			iValue *= std::max(0, 100 - iInterceptProb / 2);
			iValue /= 100;
		}*/ // BtS
		// K-Mod. Try to avoid using bestInterceptor... because that's a slow function.
		if (isSuicide())
			iValue /= 2;
		else if (!canAirDefend()) // assume that air defenders are strong.. and that they are willing to fight
		{
			CvUnit const* pInterceptor = bestInterceptor(p,
					// advc.128: Don't always cheat with visibility (only 67% of the time)
					m_iSearchRangeRandPercent > 33);
			if (pInterceptor != NULL)
			{
				int iInterceptProb = isSuicide() ? 100 : pInterceptor->currInterceptionProbability(); // doc: sacrificing interceptor always succeeds
				iInterceptProb *= std::max(0, (100 - evasionProbability()));
				iInterceptProb /= 100;
				iValue *= std::max(0, 100 - iInterceptProb / 2);
				iValue /= 100;
			}
		} // K-Mod end
		if (iValue > iBestValue)
		{
			iBestValue = iValue;
			pBestPlot = &p;
			FAssert(!atPlot(pBestPlot));
		}
	}

	if (pBestPlot != NULL)
	{
		getGroup()->pushMission(MISSION_AIRBOMB, pBestPlot->getX(), pBestPlot->getY());
		return true;
	}

	return false;
}

/* disabled by K-Mod - this is now handled in AI_airStrike.
bool CvUnitAI::AI_airBombDefenses()
{
	... // advc: Deleted the body of this unmodified BtS function
}*/

/*	advc: Renamed from AI_exploreAir in order to distinguish it from the BBAI function
	(see AI_exploreAirRange) */
bool CvUnitAI::AI_exploreAirCities()
{
	PROFILE_FUNC();

	CvPlayerAI const& kPlayer = GET_PLAYER(getOwner());
	CvPlot* pBestPlot = NULL;
	int iBestValue = 0;
	// advc.300: Don't explore Barbarian cities
	for (PlayerIter<CIV_ALIVE,NOT_SAME_TEAM_AS> it(getTeam()); it.hasNext(); ++it)
	{
		CvPlayer const& kLoopPlayer = *it;
		FOR_EACH_CITY(pLoopCity, kLoopPlayer)
		{
			if (pLoopCity->isVisible(getTeam()) ||
				!canReconAt(plot(), pLoopCity->getX(), pLoopCity->getY()))
			{
				continue;
			}
			int iValue = 1 + SyncRandNum(15);
			//if (isEnemy(kLoopPlayer.getTeam()))
			if (GET_TEAM(getTeam()).isAtWar(kLoopPlayer.getTeam())) // advc
			{
				iValue += 10;
				iValue += std::min(10, pLoopCity->getArea().getNumAIUnits(
						getOwner(), UNITAI_ATTACK_CITY));
				iValue += 10 * kPlayer.AI_plotTargetMissionAIs(
						pLoopCity->getPlot(), MISSIONAI_ASSAULT);
			}
			iValue *= plotDistance(getX(), getY(), pLoopCity->getX(), pLoopCity->getY());
			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				pBestPlot = pLoopCity->plot();
			}
		}
	}
	if (pBestPlot != NULL)
	{
		getGroup()->pushMission(MISSION_RECON, pBestPlot->getX(), pBestPlot->getY());
		return true;
	}
	return false;
}

// BETTER_BTS_AI_MOD, Player Interface, 06/02/09, jdog5000: START
int CvUnitAI::AI_exploreAirPlotValue(CvPlot const* pPlot)
{
	CvTeam const& kOurTeam = GET_TEAM(getTeam());
	//if (pPlot->isVisible(getTeam(), false)) {
	// <advc.001> The opposite needs to be true. The caller already checks that.
	FAssert(!pPlot->isVisible(kOurTeam.getID(), false));
	// And let's not cheat unnecessarily:
	if (!pPlot->isRevealed(kOurTeam.getID()))
		return 50; // </advc.001>

	int iValue = 1;

	if (!pPlot->isOwned() ||
		!kOurTeam.isFriendlyTerritory(pPlot->getTeam())) // advc.029
	{
		iValue++;
	}
	if (!pPlot->isImpassable())
	{
		iValue *= 4;
		/*if (pPlot->isWater() || pPlot->isArea(getArea()))
			iValue *= 2;*/
		/*	<advc.029> There tend to be more non-visible water tiles anyway.
			And why not explore other land areas?
			Let's rather incentivize sth. important: */
		if (::atWar(kOurTeam.getID(), pPlot->getTeam()) && !pPlot->isBarbarian())
			iValue *= 3;// </advc.029>
	}
	return iValue;
}

// advc: Renamed from "AI_exploreAir2"
bool CvUnitAI::AI_exploreAirRange(/* advc.029: */ bool bExcludeVisible)
{
	PROFILE_FUNC();
	// <advc.029>
	int const iOuterSearchRange = airRange(); // (as in BtS)
	int const iReconRange = GC.getDefineINT(CvGlobals::RECON_VISIBILITY_RANGE);
	int const iInnerSearchRange = (!isHuman() ? 1 :
			GC.getDefineINT(CvGlobals::RECON_VISIBILITY_RANGE));
	// </advc.029>
	CvPlot* pBestPlot = NULL;
	int iBestValue = 0;
	for (SquareIter it(*this, iOuterSearchRange); it.hasNext(); ++it)
	{
		CvPlot& p = *it;
		if ((bExcludeVisible && // advc.029
			p.isVisible(getTeam())) ||
			!canReconAt(plot(), p.getX(), p.getY()))
		{
			continue;
		}
		/*int iValue = AI_exploreAirPlotValue(&p);
		FOR_EACH_ENUM(Direction) {
			CvPlot* pAdjacentPlot = plotDirection( // advc.001: was getX(), getY()
					p.getX(), p.getY(), eLoopDirection);
			if (pAdjacentPlot != NULL) {
				if (!pAdjacentPlot->isVisible(getTeam(), false))
					iValue += AI_exploreAirPlotValue(pAdjacentPlot);
		} }*/
		// <advc.029>
		int iValue = 0;
		for (SquareIter itInner(p, iInnerSearchRange); itInner.hasNext(); ++itInner)
		{
			CvPlot const& kInnerLoopPlot = *itInner;
			if (!kInnerLoopPlot.isVisible(getTeam()))
				iValue += AI_exploreAirPlotValue(&kInnerLoopPlot);
		} // </advc.029>
		iValue += SyncRandNum(25);
		iValue *= std::min(it.currPlotDist(),
				/*	advc.029: Was 7. I guess we don't want to explore too close to plot(),
					but a shorter distance than 7 can certainly make sense. Try: */
				std::max(1, iOuterSearchRange - (iReconRange + 1) / 2));
		if (iValue > iBestValue)
		{
			iBestValue = iValue;
			pBestPlot = &p;
		}
	}
	if (pBestPlot != NULL)
	{
		getGroup()->pushMission(MISSION_RECON, pBestPlot->getX(), pBestPlot->getY());
		return true;
	}
	if (!bExcludeVisible || !isHuman()) // advc.029
		return false;
	/*	advc.029: A visible target plot may still reveal non-visible plots
		within the recon range */
	return AI_exploreAirRange(false);
}


void CvUnitAI::AI_exploreAirMove()
{
	if (AI_exploreAirCities())
	{
		return;
	}

	if (AI_exploreAirRange())
	{
		return;
	}

	if (canAirDefend())
	{
		getGroup()->pushMission(MISSION_AIRPATROL);
		return;
	}

	getGroup()->pushMission(MISSION_SKIP);
} // BETTER_BTS_AI_MOD: END

// This function has been completely rewritten for K-Mod.
bool CvUnitAI::AI_nuke()
{
	PROFILE_FUNC();

	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());
	CvTeamAI const& kTeam = GET_TEAM(kOwner.getTeam());
	// To save time. Don't need to nuke Barbarians.
	if (kTeam.getNumWars(false, true) <= 0)
		return false;
	// advc.650: Range limited nukes were previously handled by AI_nukeRange (deleted)
	int const iRange = airRange();
	bool const bRangeLimited = (iRange > 0);
	// consider changing this to something smarter
	/*	advc.650: ^Done for the in-city case; the plot-danger check comes from
		AI_nukeRange and still isn't smart. */
	bool const bDanger = (getPlot().isCity() ? !getPlot().AI_getPlotCity()->AI_isSafe() :
			kOwner.AI_isAnyPlotDanger(getPlot(), CvPlayerAI::DANGER_RANGE));
	int const iWarRating = kTeam.AI_getWarSuccessRating();
	int const iOurNukes = kOwner.getNumNukeUnits();
	int const iOurCities = kOwner.getNumCities();
	// Player-independent part of the weight for civilian damage evaluation
	// advc.650: Moved into new function
	int const iBaseDestrWeight = kOwner.AI_nukeBaseDestructionWeight();

	CvPlot* pBestTarget = NULL;
	/*	threshold for action (cf. units of AI_nukeValue)
		advc.650: K-Mod code from AI_nukeRange integrated (bRangeLimited branches);
		no functional change except for a removed Dagger strategy check. I guess
		it makes sense that range-limited nukes are more sensitive to danger -
		might not find a target at all if danger isn't responded to swiftly.
		(Well, I don't know ...)
		I've decreased the production cost multipliers by 1 (i.e. from 3:4 to 2:3)
		because the nuke value counted per unit and per building is now (much) smaller. */
	int iValueThresh = std::max(0, (bRangeLimited ? 2 : 3) *
			getUnitInfo().getProductionCost()) + (bRangeLimited ? 60 : 20);
	if (!bDanger)
	{
		if (bRangeLimited)
			iValueThresh = (iValueThresh * 3) / 2;
		else iValueThresh += 80;
	}
	/*	advc.650: All adjustments below had not previously (K-Mod) applied
		to range-limited nukes */

	// <advc.650>
	scaled rMeanInterceptChance;
	// Don't bother to stash away nukes if we don't need a deterrent
	bool bNeedDeterrent = kOwner.AI_isDoStrategy(AI_STRATEGY_ALERT1);
	{
		int iInterceptRivals = 0;
		for (PlayerIter<FREE_MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> itRival(kTeam.getID());
			itRival.hasNext(); ++itRival)
		{
			CvTeamAI const& kRivalTeam = GET_TEAM(itRival->getTeam());
			bool const bWar = kRivalTeam.isAtWar(kTeam.getID());
			if (!bWar && kRivalTeam.AI_isAvoidWar(kTeam.getID()))
				continue;
			rMeanInterceptChance += kRivalTeam.getNukeInterception();
			iInterceptRivals++;
			if (bNeedDeterrent)
				continue; // Save time
			if (itRival->getNumNukeUnits() > 0 ||
				(!bWar && itRival->getPower() > kOwner.getPower()))
			{
				bNeedDeterrent = true;
			}
		}
		if (iInterceptRivals > 0)
			rMeanInterceptChance /= 100 * iInterceptRivals;
	} // </advc.650>
	{
		int iDividend = std::max(1, iOurNukes + 2 * iOurCities);
		int iDivisor = std::max(1, 2 * iOurNukes + (bDanger ? 2 : 1) * iOurCities);
		if (bNeedDeterrent || iDivisor > iDividend) // advc.650
		{
			iValueThresh *= iDividend;
			iValueThresh /= iDivisor;
		}
	}
	/*	advc.650: max - Don't be too motivated by a hopeless war.
		Getting nuked back and losing is worse than just losing. */
	iValueThresh *= 150 + std::max(-50, iWarRating);
	iValueThresh /= 150;
	// advc.650: Need separate variables for threshold and argmax now
	int iBestValue = 0;
	for (PlayerIter<CIV_ALIVE,ENEMY_OF> itEnemy(kTeam.getID());
		itEnemy.hasNext(); ++itEnemy)
	{
		CvPlayer const& kEnemy = *itEnemy;
		// <advc.650>
		int const iTheirNukes = kOwner.AI_estimateNukeCount(kEnemy.getID());
		// Don't be too shy if we have far more nukes than they do
		int const iTheirNukesAdjusted = (iTheirNukes == 1 ? 1 :
				iTheirNukes - intdiv::uround(iOurNukes, 3));
		int const iNukedUsMemory = kOwner.AI_getMemoryCount(
				kEnemy.getID(), MEMORY_NUKED_US);
		WarPlanTypes const eWP = kTeam.AI_getWarPlan(kEnemy.getTeam());
		// Treat dogpile like limited war
		bool const bLimited = (eWP == WARPLAN_LIMITED || eWP == WARPLAN_DOGPILE);
		// Moved into new function
		int iDestructionWeight = iBaseDestrWeight + kOwner.AI_nukeExtraDestructionWeight(
				kEnemy.getID(), iTheirNukes, bLimited);
		// First collect the potential targets
		std::set<PlotNumTypes> aeTargetEvaluated; // to avoid duplicates
		std::vector<std::pair<CvPlot*,/*search range*/int> > apiPotentialTargets;
		// </advc.650>
		FOR_EACH_CITY(pLoopCity, kEnemy)
		{
			/*	we could use "AI_deduceCitySite" here, but, if we can't see
				the city, then we can't properly judge its target value. */
			if (pLoopCity->isRevealed(getTeam()) &&
				canNukeAt(getPlot(), pLoopCity->getX(), pLoopCity->getY(),
				getTeam())) // advc.kekm.7 (advc)
			{
				apiPotentialTargets.push_back(std::make_pair(
						/*	advc.650 (note): Not crucial anymore to search the
							nuke range around the city b/c we're now considering
							enemy stacks as independent targets. Still, let's try
							to maximize the damage to improvements too. */
						pLoopCity->plot(), nukeRange()));
				// Mark plots in search range as evaluated
				for (SquareIter itPlot(pLoopCity->getPlot(), nukeRange());
					itPlot.hasNext(); ++itPlot)
				{
					aeTargetEvaluated.insert(itPlot->plotNum());
				}
			}
		}
		/*	Also consider enemy stacks. This replaces the single call to
				AI_nukeValue(getPlot(), iRange, pTargetPlot)
			from AI_nukeRange and also allows nukes w/o a range limit to hit stacks. */
		FOR_EACH_GROUP(pLoopGroup, kEnemy)
		{
			if (pLoopGroup->getNumUnits() <= 4)
				continue;
			CvPlot& kLoopPlot = pLoopGroup->getPlot();
			if (kLoopPlot.isVisible(kTeam.getID()) &&
				// Units in or near cities are already taken care of
				aeTargetEvaluated.count(kLoopPlot.plotNum()) <= 0 &&
				canNukeAt(getPlot(), kLoopPlot.getX(), kLoopPlot.getY(), getTeam()))
			{
				apiPotentialTargets.push_back(std::make_pair(
						/*	0 search range - let's not bother with max damage to
							improvements here (see also comment in previous loop) */
						&kLoopPlot, 0));
				aeTargetEvaluated.insert(kLoopPlot.plotNum());
			}
		}
		for (size_t i = 0; i < apiPotentialTargets.size(); i++)
		{
			CvPlot& kCenter = *apiPotentialTargets[i].first;
			int iSearchRange = apiPotentialTargets[i].second;
			// </advc.650>
			CvPlot* pTarget;
			int iValue = AI_nukeValue(kCenter, iSearchRange, pTarget,
					iDestructionWeight);
			/*	<advc.650> Can happen that every potential target plot contains
				friendly units */
			if (pTarget == NULL)
				continue; // </advc.650>
			if (bLimited && iWarRating > -10)
				iValue /= 2;
			// <advc.650>
			scaled rInterceptChance = scaled::max(0,
					per100(nukeInterceptionChance(*pTarget, getTeam()))
					/*	If everyone can intercept, then there's no point in
						holding on to our nukes. */
					- fixp(0.75) * rMeanInterceptChance);
			iValue = (iValue * (1 - rInterceptChance)).uround();
			if (iTheirNukesAdjusted > 0) // Avoid escalation
			{
				scaled rEscalationMult = (1 + iNukedUsMemory) /
						(1 + scaled(iTheirNukesAdjusted).sqrt());
				rEscalationMult.decreaseTo(1);
				iValue = (iValue * rEscalationMult).uround();
			}
			// Hiroshima clause
			else if (GC.getGame().getNukesExploded() == 0)
			{
				iValue *= 5;
				iValue /= 3;
			}
			if (iValue > iBestValue)
			{
				int iLoopValueThresh = iValueThresh;
				/*	Lower threshold for hitting human unit stacks -
					b/c destroying human units is normally difficult to do
					for the AI; shouldn't let a chance pass. */
				if (!pTarget->isCity() && pTarget->isOwned() &&
					GET_PLAYER(pTarget->getOwner()).isHuman())
				{
					iLoopValueThresh *= 2;
					iLoopValueThresh /= 3;
				}
				if (iValue > iLoopValueThresh) // </advc.650>
				{
					iBestValue = iValue;
					pBestTarget = pTarget;
				}
			}
		}
	}
	if (pBestTarget != NULL)
	{
		FAssert(canNukeAt(getPlot(), pBestTarget->getX(), pBestTarget->getY()));
		getGroup()->pushMission(MISSION_NUKE, pBestTarget->getX(), pBestTarget->getY());
		return true;
	}
	return false;
}

// doc (currently unused - using advciv logic)
CvPlot* CvUnitAI::AI_defensiveNukeTarget() const
{
	CvPlot* pLoopPlot;
	CvPlot* pBestPlot;
	PlayerTypes eOtherPlayer;
	int iValue;
	int iBestValue;
	int iDX, iDY;

	pBestPlot = NULL;

	iBestValue = 10;

	FOR_EACH_CITY(pLoopCity, GET_PLAYER(getOwner()))
	{
		if (pLoopCity->isCore() && !pLoopCity->AI().AI_isDefended(10))
		{
			for (int iI = 0; iI < MAX_PLAYERS; iI++)
			{
				eOtherPlayer = (PlayerTypes)iI;

				if (GET_PLAYER(getOwner()).AI_willUseNukes(eOtherPlayer, false))
				{
					for (iDX = -2; iDX <= 2; iDX++)
					{
						for (iDY = -2; iDY <= 2; iDY++)
						{
							pLoopPlot = plotXY(pLoopCity->getX(), pLoopCity->getY(), iDX, iDY);

							if (pLoopPlot != NULL)
							{
								if (canNukeAt(getPlot(), pLoopPlot->getX(), pLoopPlot->getY()))
								{
									iValue = pLoopPlot->plotCount(PUF_isPlayer, iI);

									if (iValue > iBestValue)
									{
										iBestValue = iValue;
										pBestPlot = pLoopPlot;
										FAssert(pBestPlot->getTeam() != getTeam());
									}
								}
							}
						}
					}
				}
			}
		}
	}

	return pBestPlot;
}

// doc (currently unused - using advciv logic)
CvCity* CvUnitAI::AI_offensiveNukeTarget() const
{
	CvPlot* pBestTarget;
	CvCity* pBestCity = NULL;
	int iBestValue = 25; // Leoreth: threshold so we don't target useless cities

	for (PlayerIter<CIV_ALIVE, NOT_SAME_TEAM_AS> it(getTeam()); it.hasNext(); ++it)
	{
		CvPlayer const& kOtherPlayer = *it;
		if (GET_PLAYER(getOwner()).AI_willUseNukes(kOtherPlayer.getID(), true))
		{
			FOR_EACH_CITY_VAR(pLoopCity, kOtherPlayer)
			{
				if (canNukeAt(getPlot(), pLoopCity->getX(), pLoopCity->getY()))
				{
					int iValue = AI_nukeValue(pLoopCity->getPlot(), nukeRange(), pBestTarget);
					if (iValue > iBestValue)
					{
						iBestValue = iValue;
						pBestCity = pLoopCity;
						FAssert(pBestCity->getTeam() != getTeam());
					}
				}
			}
		}
	}

	return pBestCity;
}

// doc
CvCity* CvUnitAI::AI_offensiveSatelliteTarget() const
{
	CvCity* pBestCity = NULL;
	int iBestValue = 0;
    for (PlayerIter<CIV_ALIVE, ENEMY_OF> it(getTeam()); it.hasNext(); ++it)
	{
        FOR_EACH_CITY_VAR(pLoopCity, *it)
        {
            if (canSatelliteAttack(pLoopCity->getPlot()))
            {
                int iValue = pLoopCity->getPlot().plotCount(PUF_isUnitAIType, UNITAI_SATELLITE, -1, it->getID());
                if (iValue > iBestValue)
                {
                    iBestValue = iValue;
                    pBestCity = pLoopCity;
                }
            }
        }
    }

	return pBestCity;
}

// old nuke range code disabled by K-Mod  (advc: body deleted on 9 Jan 2020)
/*bool CvUnitAI::AI_nukeRange(int iRange)
{
	// ...
}*/

/*	K-Mod: Return the value of the best nuke target in the range specified,
	and set pBestTarget to be the specific target plot. The return value is
	roughly in units of production. */
int CvUnitAI::AI_nukeValue(CvPlot const& kCenterPlot, int iSearchRange,
	CvPlot const*& pBestTarget, int iCivilianTargetWeight) const
{
    PROFILE_FUNC();

    // doc
    if (kCenterPlot.isBarbarian())
        return 0;
    if (kCenterPlot.isMinorCiv())
        return 0;
    if (kCenterPlot.isCity() && kCenterPlot.getPlotCity()->calculateCulturePercent(getOwner()) >= 20)
        return 0;

	typedef std::map<CvPlot const*, int> plotMap_t;
	plotMap_t plotValueCache;
	pBestTarget = NULL;
	int iBestValue = 0; // note: value is divided by 100 at the end
	for (SquareIter itTarget(kCenterPlot, iSearchRange); itTarget.hasNext(); ++itTarget)
	{
		CvPlot& kLoopTarget = *itTarget;
		if (!canNukeAt(getPlot(), kLoopTarget.getX(), kLoopTarget.getY(),
			getTeam())) // advc.650
		{
			continue;
		}
		/*	Note: canNukeAt checks that we aren't hitting any 3rd party targets,
			so we don't have to worry about checking that elsewhere */

		int iTargetValue = 0;
		//bool bValid = true; // advc: Rewritten w/o this flag
		for (SquareIter itNuke(kLoopTarget, nukeRange()); itNuke.hasNext(); ++itNuke)
		{
			plotMap_t::iterator pos = plotValueCache.find(&*itNuke);
			if (pos != plotValueCache.end())
			{
				if (pos->second == MIN_INT)
					continue;
				iTargetValue += pos->second;
				continue;
			}
			// plot evaluation ... (advc: moved to CvPlayerAI)
			int iPlotValue = GET_PLAYER(getOwner()).AI_nukePlotValue(
					*itNuke, iCivilianTargetWeight); // TODO: include building value (number of buildings / 2)
			plotValueCache[&*itNuke] = iPlotValue;
			iTargetValue += iPlotValue;
		}
		if (iTargetValue > iBestValue)
		{
			pBestTarget = &kLoopTarget;
			iBestValue = iTargetValue;
		}
	}
	return iBestValue / 100;
}

// K-Mod. Get the best trade mission value.
// Note. The iThreshold parameter is only there to improve efficiency.
int CvUnitAI::AI_tradeMissionValue(CvPlot*& pBestPlot, int iThreshold)  // advc: refactoring
{
	pBestPlot = NULL;
	FAssert(getDomainType() == DOMAIN_LAND); // advc

	if (getUnitInfo().getBaseTrade() <= 0 && getUnitInfo().getTradeMultiplier() <= 0)
		return 0;

	int iBestValue = 0;
	int iBestPathTurns = MAX_INT;
	for (PlayerAIIter<MAJOR_CIV> it; it.hasNext(); ++it)
	{
		CvPlayerAI const& kPlayer = *it;
		// Erik <AI1>: Do not consider cities belonging to players that we have a war plan against
		if (GET_TEAM(getTeam()).AI_getWarPlan(kPlayer.getTeam()) != NO_WARPLAN)
			continue; // </AI1>
		FOR_EACH_CITY(pLoopCity, kPlayer)
		{
			if (//!AI_plotValid(pLoopCity->plot()) ||
				!AI_canEnterByLand(pLoopCity->getArea()) || // advc.opt (replacing the above)
				!pLoopCity->isRevealed(getTeam()) || // advc.001 (from MNAI)
				pLoopCity->getPlot().isVisibleEnemyUnit(this))
			{
				continue;
			}
			const int iValue = getTradeGold(pLoopCity->plot());
			if (iValue < iThreshold || !canTrade(pLoopCity->plot()))
				continue;

			int iPathTurns;
			if (generatePath(pLoopCity->getPlot(),
				MOVE_NO_ENEMY_TERRITORY, true, &iPathTurns))
			{
				if (iValue / (4 + iPathTurns) > iBestValue / (4 + iBestPathTurns))
				{
					iBestValue = iValue;
					iBestPathTurns = iPathTurns;
					pBestPlot = &getPathEndTurnPlot();
					iThreshold = std::max(iThreshold, iBestValue * 4 / (4 + iBestPathTurns));
				}
			}
		}
	}
	return iBestValue;
}

// K-Mod. Move to destination for a trade mission. (pTradePlot is either the target city, or the end-turn plot.)
bool CvUnitAI::AI_doTradeMission(CvPlot* pTradePlot)
{
	if (pTradePlot != NULL)
	{
		if (atPlot(pTradePlot))
		{
			FAssert(canTrade(pTradePlot));
			if (canTrade(pTradePlot))
			{
				getGroup()->pushMission(MISSION_TRADE);
				return true;
			}
		}
		else
		{
			pushGroupMoveTo(*pTradePlot, MOVE_NO_ENEMY_TERRITORY, false, false,
					MISSIONAI_TRADE);
			return true;
		}
	}

	return false;
}

// find the best place to do create a great work (culture bomb)
int CvUnitAI::AI_greatWorkValue(CvPlot*& pBestPlot, int iThreshold)
{
	pBestPlot = NULL;

	if (getUnitInfo().getGreatWorkCulture() == 0)
		return 0;

	int iBestValue = 0;
	int iBestPathTurns = MAX_INT;
	const CvPlayerAI& kOwner = GET_PLAYER(getOwner());
	FOR_EACH_CITYAI(pLoopCity, kOwner)
	{
		//if (!AI_plotValid(pLoopCity->plot()) || pLoopCity->getPlot().isVisibleEnemyUnit(this))
		// advc.opt: It's our city and our land unit
		if (!AI_canEnterByLand(pLoopCity->getArea())) // advc.030 (replacing same-area check)
			continue;
		// <advc.139>
		if (!pLoopCity->AI_isSafe())
			continue; // </advc.139>

		int iValue = getGreatWorkCulture(pLoopCity->plot()) * kOwner.AI_commerceWeight(COMMERCE_CULTURE, pLoopCity) / 100;
		// commerceWeight takes into account culture pressure and cultural victory strategy.
		// However, it is intended to be used for evaluating steady culture rates rather than bursts.
		// Therefore the culture-pressure side of it is probably under-rated, and the cultural
		// victory part is based on current culture rather than turns to legendary.
		// Also, it doesn't take into account the possibility of flipping enemy cities.
		// ... But it's a good start.

		if (iValue >= iThreshold && canGreatWork(pLoopCity->plot()))
		{
			int iPathTurns;
			if (generatePath(pLoopCity->getPlot(), MOVE_NO_ENEMY_TERRITORY, true, &iPathTurns))
			{
				if (iValue / (4 + iPathTurns) > iBestValue / (4 + iBestPathTurns))
				{
					iBestValue = iValue;
					iBestPathTurns = iPathTurns;
					pBestPlot = &getPathEndTurnPlot();
					iThreshold = std::max(iThreshold, iBestValue * 4 / (4 + iBestPathTurns));
				}
			}
		}
	}

	return iBestValue;
}

// create great work if we're at pCulturePlot, otherwise just move towards pCulturePlot.
bool CvUnitAI::AI_doGreatWork(CvPlot* pCulturePlot)
{
	if (pCulturePlot == NULL)
		return false;

	if (at(*pCulturePlot))
	{
		FAssert(canGreatWork(pCulturePlot));
		getGroup()->pushMission(MISSION_GREAT_WORK);
		return true;
	}

	pushGroupMoveTo(*pCulturePlot, MOVE_NO_ENEMY_TERRITORY, false, false,
			MISSIONAI_GREAT_WORK);
	return true;
}
// K-Mod end

/*  advc.003j (comment): Unused - i.e. the AI doesn't use the Infiltrate mission.
	There is a call commented out in the BtS version of this file (CvUnitAI::AI_spyMove). */
bool CvUnitAI::AI_infiltrate()
{
	PROFILE_FUNC();

	if (canInfiltrate(plot()))
	{
		getGroup()->pushMission(MISSION_INFILTRATE);
		return true;
	}

	int iBestValue = 0;
	CvPlot* pBestPlot = NULL;
	//bool const bMoveAllTerrain = getGroup()->canMoveAllTerrain(); // advc
	for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		CvPlayer const& kTargetPlayer = GET_PLAYER((PlayerTypes)iI);
		if (!kTargetPlayer.isAlive() || kTargetPlayer.getTeam() == getTeam())
			continue;

		FOR_EACH_CITY(pLoopCity, kTargetPlayer)
		{
			if (!canInfiltrate(pLoopCity->plot()))
				continue;

			/*  BETTER_BTS_AI_MOD, Unit AI, Efficiency, 02/22/10, jdog5000: START
			check area for land units before generating path */
			/*if (getDomainType() == DOMAIN_LAND && !pLoopCity->isArea(getArea()) &&
				!bMoveAllTerrain)*/
			if (!AI_canEnterByLand(pLoopCity->getArea())) // advc.030: same as in AI_guard
			{
				continue;
			}
			int iValue = getEspionagePoints(pLoopCity->plot());
			if (iValue > iBestValue) // BETTER_BTS_AI_MOD: END
			{
				int iPathTurns;
				if (generatePath(pLoopCity->getPlot(), NO_MOVEMENT_FLAGS, true, &iPathTurns))
				{
					FAssert(iPathTurns > 0);
					if (getPathFinder().getFinalMoves() == 0)
						iPathTurns++;
					iValue /= 1 + iPathTurns;
					if (iValue > iBestValue)
					{
						iBestValue = iValue;
						pBestPlot = pLoopCity->plot();
					}
				}
			}
		}
	}

	if (pBestPlot != NULL)
	{
		if (at(*pBestPlot))
		{
			getGroup()->pushMission(MISSION_INFILTRATE);
			return true;
		}
		else
		{
			pushGroupMoveTo(*pBestPlot);
			getGroup()->pushMission(MISSION_INFILTRATE, -1, -1, NO_MOVEMENT_FLAGS,
					//(getGroup()->getLengthMissionQueue() > 0));
					true); // K-Mod
			return true;
		}
	}

	return false;
}

bool CvUnitAI::AI_reconSpy(int iRange)
{
	PROFILE_FUNC();

	CvPlot* pBestPlot = NULL;
	CvPlot* pBestTargetPlot = NULL;
	int iBestValue = 0;
	CvTeamAI const& kOurTeam = GET_TEAM(getTeam());
	for (SquareIter it(*this, AI_searchRange(iRange), false); it.hasNext(); ++it)
	{
		CvPlot& p = *it;
		if (/*!AI_plotValid(p)*/ !AI_canEnterByLand(p.getArea())) // advc.opt
			continue;
		int iValue = 0;
		if (p.isCity())
			iValue += SyncRandNum(2400); // was 4000
		if (p.getBonusType(getTeam()) != NO_BONUS)
			iValue += SyncRandNum(800); // was 1000
		FOR_EACH_ADJ_PLOT(p)
		{
			if (!pAdj->isRevealed(getTeam()))
				iValue += 500;
			else if (!pAdj->isVisible(getTeam()))
				iValue += 200;
		}
		// K-Mod
		if (p.getTeam() == getTeam())
			iValue /= 4;
		//else if (isPotentialEnemy(p.getTeam(), &p))
		else if (p.isOwned() && kOurTeam.AI_mayAttack(p.getTeam())) // advc
			iValue *= 2;
		// K-Mod end
		if (iValue <= 0)
			continue;

		int iPathTurns;
		if (!generatePath(p, NO_MOVEMENT_FLAGS, true, &iPathTurns, iRange))
			continue;
		if (iPathTurns > iRange)
			continue;
		int const iDistance = it.currStepDist();
		// don't give each and every plot in range a value before generating the path (performance hit)
		// <advc.007> Let's see if this leads to less spam in the MPLog:
		if ((iValue + 250) * iDistance <= iBestValue)
			continue; // </advc.007>
		iValue += SyncRandNum(250);
		iValue *= iDistance;
		/* Can no longer perform missions after having moved
		if (getPathLastNode()->m_iData2 == 1) {
			if (getPathLastNode()->m_iData1 > 0) {
				//Prefer to move and have movement remaining to perform a kill action.
				iValue *= 2;
			}
		}*/
		if (iValue > iBestValue)
		{
			iBestValue = iValue;
			pBestTargetPlot = &getPathEndTurnPlot();
			pBestPlot = &p;
		}
	}
	if (pBestPlot == NULL || pBestTargetPlot == NULL)
		return false;
	if (at(*pBestTargetPlot))
	{
		getGroup()->pushMission(MISSION_SKIP);
		return true;
	}
	else
	{	/*pushGroupMoveTo(*pBestTargetPlot);
		getGroup()->pushMission(MISSION_SKIP);*/ // BtS
		// K-Mod. (skip turn after each step of a recon mission? strange)
		pushGroupMoveTo(*pBestTargetPlot, NO_MOVEMENT_FLAGS, false, false,
				MISSIONAI_RECON_SPY, pBestPlot);
		// K-Mod end
		return true;
	}
}

/*	BETTER_BTS_AI_MOD, Espionage AI, 10/25/09, jdog5000: START
	Spy decision on whether to cause revolt in besieged city.
	Have spy breakdown city defenses if we have troops
	in position to capture city this turn. */
bool CvUnitAI::AI_revoltCitySpy()
{
	//PROFILE_FUNC(); // advc.003o

	CvCity* pCity = getPlot().getPlotCity();
	if (pCity == NULL)
	{
		FAssert(pCity != NULL);
		return false;
	}
	if (!GET_TEAM(getTeam()).isAtWar(pCity->getTeam()))
		return false;

	if (pCity->isDisorder())
		return false;

	// K-Mod
	if (100 * (GC.getMAX_CITY_DEFENSE_DAMAGE() - pCity->getDefenseDamage()) /
		std::max(1, GC.getMAX_CITY_DEFENSE_DAMAGE()) < 15)
	{
		return false;
	} // K-Mod end

	/*int iOurPower = GET_PLAYER(getOwner()).AI_getOurPlotStrength(plot(),1,false,true);
	int iEnemyDefensePower = GET_PLAYER(getOwner()).AI_getEnemyPlotStrength(plot(),0,true,false);
	int iEnemyPostPower = GET_PLAYER(getOwner()).AI_getEnemyPlotStrength(plot(),0,false,false);
	if (iOurPower > 2*iEnemyDefensePower)
		return false;
	if (iOurPower < iEnemyPostPower)
		return false;
	if (10*iEnemyDefensePower < 11*iEnemyPostPower)
		return false;*/ // BBAI - Disabled by K-Mod. The power comparisons are done in AI_spyMove().

	FOR_EACH_ENUM(EspionageMission)
	{
		CvEspionageMissionInfo& kMission = GC.getInfo(eLoopEspionageMission);
		if (kMission.getCityRevoltCounter() > 0 || kMission.getPlayerAnarchyCounter() > 0)
		{
			// K-Mod
			if (GET_PLAYER(getOwner()).canDoEspionageMission(eLoopEspionageMission,
				pCity->getOwner(), pCity->plot(), -1, this))
			{
				if (gUnitLogLevel > 2) logBBAI("      %S uses city revolt at %S.", GET_PLAYER(getOwner()).getCivilizationDescription(0), pCity->getName().GetCString());
				getGroup()->pushMission(MISSION_ESPIONAGE, eLoopEspionageMission);
				return true;
			} // K-Mod end
		}
	}

	return false;
}

// K-Mod, I've moved the pathfinding check out of this function.
int CvUnitAI::AI_getEspionageTargetValue(CvPlot* pPlot/*, int iMaxPath*/)
{
	PROFILE_FUNC();

	if (!pPlot->isOwned() || pPlot->getTeam() == getTeam() ||
		GET_TEAM(getTeam()).isVassal(pPlot->getTeam()) || !AI_plotValid(pPlot))
	{
		return 0; // advc
	}
	int iValue = 0;
	CvCity const* pCity = pPlot->getPlotCity();
	if (pCity != NULL)
	{
		iValue += pCity->getPopulation();
		iValue += pCity->getPlot().calculateCulturePercent(getOwner())/8;
		int iRand = SyncRandNum(6);
		iValue += iRand * iRand;
		if (getArea().AI_getTargetCity(getOwner()) == pCity)
			iValue += 30;
		if (GET_PLAYER(getOwner()).AI_isAnyPlotTargetMissionAI(
			*pPlot, MISSIONAI_ASSAULT, getGroup()))
		{
			iValue += 30;
		}
		// K-Mod. Dilute the effect of population, and take cost modifiers into account.
		iValue += 10;
		iValue *= 100;
		iValue /= GET_PLAYER(getOwner()).getEspionageMissionCostModifier(
				NO_ESPIONAGEMISSION, pCity->getOwner(), pPlot);
		// K-Mod end.
	}
	else
	{
		BonusTypes eBonus = pPlot->getNonObsoleteBonusType(getTeam(), true);
		if (eBonus != NO_BONUS)
			iValue += GET_PLAYER(pPlot->getOwner()).AI_baseBonusVal(eBonus, 1) - 10;
	}
	/*int iPathTurns;
	if (generatePath(pPlot, 0, true, &iPathTurns)) {
		if (iPathTurns <= iMaxPath) {
			if (kTeam.AI_getWarPlan(pPlot->getTeam()) == NO_WARPLAN)
				iValue *= 1;
			else if (kTeam.AI_isSneakAttackPreparing(pPlot->getTeam()))
				iValue *= (pPlot->isCity()) ? 15 : 10;
			else iValue *= 3;
			iValue *= 3;
			iValue /= (3 + GET_PLAYER(getOwner()).AI_plotTargetMissionAIs(pPlot, MISSIONAI_ATTACK_SPY, getGroup()));
		}
	}*/ // BtS (K-Mod: moved out of this function)
	return iValue;
}

// heavily edited for K-Mod
bool CvUnitAI::AI_cityOffenseSpy(int iMaxPath, CvCity* pSkipCity)
{
	PROFILE_FUNC();

	int iBestValue = 0;
	CvPlot* pBestPlot = NULL;
	CvPlot* pEndTurnPlot = NULL;

	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());
	CvTeamAI const& kOurTeam = GET_TEAM(getTeam());

	// cf the "big espionage" minimum value. (AI_bestPlotEspionage)
	int iBaselinePoints = 50;
	{
		int iEra = kOwner.getCurrentEra();
		iBaselinePoints *= iEra * (iEra + 1);
	}
	int iAverageUnspentPoints=0;
	{
		int iTeamCount = 0;
		int iTotalUnspentPoints = 0;
		for (TeamIter<CIV_ALIVE,NOT_SAME_TEAM_AS> itTarget(getTeam());
			itTarget.hasNext(); ++itTarget)
		{
			if (kOurTeam.isVassal(itTarget->getID()))
				continue;
			iTotalUnspentPoints += kOurTeam.getEspionagePointsAgainstTeam(itTarget->getID());
			iTeamCount++;
		}
		iAverageUnspentPoints = iTotalUnspentPoints /= std::max(1, iTeamCount);
	}
	for (PlayerIter<CIV_ALIVE,NOT_SAME_TEAM_AS> itTarget(getTeam());
		itTarget.hasNext(); ++itTarget)
	{
		CvPlayer const& kLoopPlayer = *itTarget;
		if (kOurTeam.isVassal(kLoopPlayer.getTeam()))
			continue;

		int iTeamWeight = 1000;
		iTeamWeight *= kOurTeam.getEspionagePointsAgainstTeam(kLoopPlayer.getTeam());
		iTeamWeight /= std::max(1, iAverageUnspentPoints+iBaselinePoints);

		iTeamWeight *= 400 - kOurTeam.AI_getAttitudeWeight(kLoopPlayer.getTeam());
		iTeamWeight /= 500;
		if (kOurTeam.AI_getWarPlan(kLoopPlayer.getTeam()) != NO_WARPLAN)
			iTeamWeight *= 2;
		// advc.120: was AI_isSneakAttackPreparing
		if (kOurTeam.AI_isSneakAttackReady(kLoopPlayer.getTeam()))
			iTeamWeight *= 2;
		if (kOwner.AI_isMaliciousEspionageTarget(kLoopPlayer.getID()))
		{
			iTeamWeight *= 3;
			iTeamWeight /= 2;
		}
		// <advc.130v>
		if (GET_TEAM(kLoopPlayer.getTeam()).isCapitulated())
			iTeamWeight /= 2; // </advc.130v>
		if (iTeamWeight < 200 && SyncRandSuccess100(90))
		{	/*	low weight. Probably friendly attitude and below average points.
				don't target this team. */
			continue;
		}
		FOR_EACH_CITY(pLoopCity, kLoopPlayer)
		{
			if (pLoopCity == pSkipCity || !kOwner.AI_deduceCitySite(*pLoopCity) ||
				// advc.030: Replacing same-area and canMoveAllTerrain check
				!AI_canEnterByLand(pLoopCity->getArea()))
			{
				continue;
			}
			CvPlot* pLoopPlot = pLoopCity->plot();
			// advc.opt: Area check should suffice
			//if (!AI_plotValid(pLoopPlot)) continue;
			int iPathTurns;
			if (generatePath(*pLoopPlot, NO_MOVEMENT_FLAGS, true,
				&iPathTurns, iMaxPath) && iPathTurns <= iMaxPath)
			{
				int iValue = AI_getEspionageTargetValue(pLoopPlot);
				iValue *= 5;
				iValue /= 5 + GET_PLAYER(getOwner()).AI_plotTargetMissionAIs(
						*pLoopPlot, MISSIONAI_ATTACK_SPY, getGroup());
				iValue *= iTeamWeight;
				if (iValue > iBestValue)
				{
					iBestValue = iValue;
					pBestPlot = pLoopPlot;
					pEndTurnPlot = &getPathEndTurnPlot();
				}
			}
		}
	}
	if (pBestPlot != NULL)
	{
		if (at(*pBestPlot))
		{
			getGroup()->pushMission(MISSION_SKIP, -1, -1, NO_MOVEMENT_FLAGS,
					false, false, MISSIONAI_ATTACK_SPY);
		}
		else
		{
			pushGroupMoveTo(*pEndTurnPlot, NO_MOVEMENT_FLAGS,
					false, false, MISSIONAI_ATTACK_SPY, pBestPlot);
		}
		return true;
	}
	return false;
}


bool CvUnitAI::AI_bonusOffenseSpy(int iRange)
{
	PROFILE_FUNC();

	CvPlot* pBestPlot = NULL;
	CvPlot* pEndTurnPlot = NULL;
	int iBestValue = 10;
	for (SquareIter it(*this, AI_searchRange(iRange)); it.hasNext(); ++it)
	{
		CvPlot& p = *it;
		if (p.getNonObsoleteBonusType(getTeam(), true) != NO_BONUS &&
			p.isOwned() && p.getTeam() != getTeam())
		{
			/*Only move to plots where we will run missions
			if (GET_PLAYER(getOwner()).AI_getAttitudeWeight(pLoopPlot->getOwner()) < (GC.getGame().isOption(GAMEOPTION_AGGRESSIVE_AI) ? 51 : 1)
				|| GET_TEAM(getTeam()).AI_getWarPlan(pLoopPlot->getTeam()) != NO_WARPLAN) {
				int iValue = AI_getEspionageTargetValue(pLoopPlot, iRange);
				if (iValue > iBestValue) {
					iBestValue = iValue;
					pBestPlot = pLoopPlot;
				}
			}*/ // BtS
			// K-Mod. I think this is only worthwhile when at war...
			//if (kOwner.AI_isMaliciousEspionageTarget(pLoopPlot->getOwner()))
			if (GET_TEAM(getTeam()).isAtWar(p.getTeam()))
			{
				int iPathTurns;
				if (generatePath(p, NO_MOVEMENT_FLAGS, true, &iPathTurns, iRange) &&
					iPathTurns <= iRange)
				{
					int iValue = AI_getEspionageTargetValue(&p);
					//iValue *= GET_TEAM(getTeam()).AI_getWarPlan(pLoopPlot->getTeam()) != NO_WARPLAN ? 3: 1;
					//iValue *= GET_TEAM(getTeam()).AI_isSneakAttackPreparing(pLoopPlot->getTeam()) ? 2 : 1;
					iValue *= 4;
					iValue /= (4 + GET_PLAYER(getOwner()).AI_plotTargetMissionAIs(
							p, MISSIONAI_ATTACK_SPY, getGroup()));
					if (iValue > iBestValue)
					{
						iBestValue = iValue;
						pBestPlot = &p;
						pEndTurnPlot = &getPathEndTurnPlot();
					}
				}
			} // K-Mod end
		}
	}

	if (pBestPlot != NULL)
	{
		if (at(*pBestPlot))
		{
			getGroup()->pushMission(MISSION_SKIP, -1, -1,
					NO_MOVEMENT_FLAGS, false, false, MISSIONAI_ATTACK_SPY);
			return true;
		}
		else
		{
			/*pushGroupMoveTo(*pBestPlot, NO_MOVEMENT_FLAGS, false, false, MISSIONAI_ATTACK_SPY);
			getGroup()->pushMission(MISSION_SKIP, -1, -1, 0, false, false, MISSIONAI_ATTACK_SPY);*/ // BtS
			// K-Mod
			pushGroupMoveTo(*pEndTurnPlot, NO_MOVEMENT_FLAGS, false, false,
					MISSIONAI_ATTACK_SPY, pBestPlot);
			// K-Mod end
			return true;
		}
	}

	return false;
} // BETTER_BTS_AI_MOD: END (Espionage AI)

//Returns true if the spy performs espionage.
bool CvUnitAI::AI_espionageSpy()
{
	PROFILE_FUNC();

	if (!canEspionage(plot()))
		return false;

	EspionageMissionTypes eBestMission = NO_ESPIONAGEMISSION;
	/*CvPlot* pTargetPlot = NULL;
	PlayerTypes eTargetPlayer = NO_PLAYER;*/ // advc (not needed)
	int iExtraData = -1;

	//eBestMission = GET_PLAYER(getOwner()).AI_bestPlotEspionage(plot(), eTargetPlayer, pTargetPlot, iExtraData);
	eBestMission = AI_bestPlotEspionage(iExtraData);
	if (eBestMission == NO_ESPIONAGEMISSION)
		return false;

	if (!GET_PLAYER(getOwner()).canDoEspionageMission(eBestMission,
		getPlot().getOwner(), plot(), iExtraData, this))
	{
		return false;
	}

	/*if (!espionage(eBestMission, iExtraData))
		return false;*/ // BtS - diabled by K-Mod

	getGroup()->pushMission(MISSION_ESPIONAGE, eBestMission, iExtraData);
	return true;
}

/*	K-Mod edition (this use to be a CvPlayerAI:: function):
	advc: Removed out parameters for target plot and target player
	b/c it's always the plot of this unit and the owner of that plot. */
EspionageMissionTypes CvUnitAI::AI_bestPlotEspionage(int& iData) const
{
	PROFILE_FUNC();

	CvPlot& kSpyPlot = getPlot();
	// advc: Target checks moved up
	PlayerTypes const eTargetPlayer = kSpyPlot.getOwner();
	if (eTargetPlayer == NO_PLAYER)
		return NO_ESPIONAGEMISSION;
	TeamTypes const eTargetTeam = kSpyPlot.getTeam();
	if (eTargetTeam == getTeam())
		return NO_ESPIONAGEMISSION;

	EspionageMissionTypes eBestMission = NO_ESPIONAGEMISSION;
	iData = -1;
	int iBestValue = 0;

	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());
	bool const bBigEspionage = kOwner.AI_isDoStrategy(AI_STRATEGY_BIG_ESPIONAGE);
	int const iEspionageRate = kOwner.getCommerceRate(COMMERCE_ESPIONAGE);
	int const iEspPoints = GET_TEAM(getTeam()).getEspionagePointsAgainstTeam(eTargetTeam);

	int iSpyValue = 3 * kOwner.getProductionNeeded(getUnitType()) + 60;
	if (kOwner.hasCapital())
	{
		iSpyValue += stepDistance(getX(), getY(),
				kOwner.getCapital()->getX(), kOwner.getCapital()->getY()) / 2;
	}
	// estimate risk cost of losing the spy while trying to escape
	int iBaseIntercept = 0;
	{
		int iTargetTotal = GET_TEAM(eTargetTeam).getEspionagePointsEver();
		int iOurTotal = GET_TEAM(getTeam()).getEspionagePointsEver();
		iBaseIntercept += (GC.getDefineINT("ESPIONAGE_INTERCEPT_SPENDING_MAX") * iTargetTotal) /
				std::max(1, iTargetTotal + iOurTotal);
		if (GET_TEAM(eTargetTeam).getCounterespionageModAgainstTeam(getTeam()) > 0)
			iBaseIntercept += GC.getDefineINT("ESPIONAGE_INTERCEPT_COUNTERESPIONAGE_MISSION");
	}
	int const iEscapeCost = 2 * iSpyValue * iBaseIntercept *
			(100 + GC.getDefineINT("ESPIONAGE_SPY_MISSION_ESCAPE_MOD")) / 10000;

	// One espionage mission loop to rule them all.
	FOR_EACH_ENUM2(EspionageMission, eMission)
	{
		CvEspionageMissionInfo const& kMission = GC.getInfo(eMission);
		int iTestData = 1;
		if (kMission.getBuyTechCostFactor() > 0)
			iTestData = GC.getNumTechInfos();
		else if (kMission.getDestroyProjectCostFactor() > 0)
			iTestData = GC.getNumProjectInfos();
		else if (kMission.getDestroyBuildingCostFactor() > 0)
			iTestData = GC.getNumBuildingInfos();

		// estimate the risk cost of losing the spy.
		int iOverhead = iEscapeCost + iSpyValue * iBaseIntercept *
				(100 + kMission.getDifficultyMod()) / 10000;
		bool bFirst = true; // advc.007
		for (iTestData-- ; iTestData >= 0; iTestData--)
		{
			int iCost = kOwner.getEspionageMissionCost(
					eMission, eTargetPlayer, &kSpyPlot, iTestData, this);
			if (iCost < 0 || (iCost <= iEspPoints && !kOwner.canDoEspionageMission(
				eMission, eTargetPlayer, &kSpyPlot, iTestData, this)))
			{
				continue; // we can't do the mission, and cost is not the limiting factor.
			}
			int iValue = kOwner.AI_espionageVal(
					eTargetPlayer, eMission, kSpyPlot, iTestData);
			iValue *= 80 + syncRand().get(60,
					// <advc.007> Don't pollute the MPLog
					bFirst ? "AI best espionage mission" : NULL);
			bFirst = false; // </advc.007>
			iValue /= 100;
			iValue -= iOverhead;
			iValue -= iCost * (bBigEspionage ? 2 : 1) * iCost / std::max(1,
					iCost + GET_TEAM(getTeam()).getEspionagePointsAgainstTeam(eTargetTeam));

			/*	If we can't do the mission yet, don't completely give up.
				It might be worth saving points for. */
			if (!kOwner.canDoEspionageMission(eMission,
				eTargetPlayer, &kSpyPlot, iTestData, this))
			{
				// Is cost is the reason we can't do the mission?
				if (GET_TEAM(getTeam()).isHasTech((TechTypes)kMission.getTechPrereq()))
				{
					FAssert(iCost > iEspPoints); // (see condition at the top of the loop)

					/*	Scale the mission value based on
						how long we think it will take to get the points. */
					int iTurns = (iCost - iEspPoints) / std::max(1, iEspionageRate);
					iTurns *= bBigEspionage? 1 : 2;
					/*	The number of turns is approximated (poorly)
						by assuming our entire esp rate is targeting eTargetTeam. */
					iValue *= 3;
					iValue /= iTurns + 3;
					// eg, 1 turn left -> 3/4. 2 turns -> 3/5, 3 turns -> 3/6. Etc.
				}
				else
				{
					/*	Ok. Now it's time to give up.
						(Even if we're researching the prereq tech right now - too bad.) */
					iValue = 0;
				}
			}

			// Block small missions when using "big espionage", unless the mission is really good value.
			if (bBigEspionage &&
				// 100, 300, 600, 1000, 1500, ...
				iValue < 50 * kOwner.getCurrentEra() * (kOwner.getCurrentEra() + 1) &&
				iValue < (kOwner.AI_isDoStrategy(AI_STRATEGY_ESPIONAGE_ECONOMY)
				? 4 : 2) * iCost)
			{
				iValue = 0;
			}
			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				eBestMission = eMission;
				iData = iTestData;
			}
		}
	}
	if (gUnitLogLevel > 2 && eBestMission != NO_ESPIONAGEMISSION)
	{
		//FAssertMsg(!kOwner.AI_isDoStrategy(AI_STRATEGY_ESPIONAGE_ECONOMY) || GC.getInfo(eBestMission).getBuyTechCostFactor() > 0 || GC.getInfo(eBestMission).getDestroyProjectCostFactor() > 0, "Potentially wasteful AI use of espionage."); // Just for testing purposes
		logBBAI("      %S chooses %S as their best%s espionage mission (value: %d, cost: %d).", GET_PLAYER(getOwner()).getCivilizationDescription(0), GC.getInfo(eBestMission).getText(), bBigEspionage?" (big)":"", iBestValue, kOwner.getEspionageMissionCost(eBestMission, eTargetPlayer, plot(), iData, this));
	}

	return eBestMission;
}


bool CvUnitAI::AI_moveToStagingCity()
{
	PROFILE_FUNC();

	CvTeamAI const& kOurTeam = GET_TEAM(getTeam());
	// advc: Moved up
	bool const bNaval = (getArea().getAreaAIType(kOurTeam.getID()) == AREAAI_ASSAULT ||
			getArea().getAreaAIType(kOurTeam.getID()) == AREAAI_ASSAULT_MASSING);
	CvPlot* pStagingPlot = NULL;
	CvPlot* pEndTurnPlot = NULL;
	int iBestValue = 0;
	FOR_EACH_CITYAI(pLoopCity, GET_PLAYER(getOwner()))
	{
		// BETTER_BTS_AI_MOD, War tactics AI, Efficiency, 02/22/10, jdog5000, START:
		// BBAI efficiency: check same area  // advc.opt: Don't need AI_plotValid then
		if (!pLoopCity->isArea(getArea()) /*|| !AI_plotValid(pLoopCity->plot()*/)
			continue;
		/*	BBAI TODO: Need some knowledge of whether this is a good city to attack from ...
			only get that indirectly from threat. */
		int iValue = pLoopCity->AI_cityThreat();
		// Have attack stacks in assault areas move to coastal cities for faster loading
		if (bNaval)
		{
			CvArea* pWaterArea = pLoopCity->waterArea();
			if (pWaterArea != NULL && kOurTeam.AI_isWaterAreaRelevant(*pWaterArea))
			{
				/*	BBAI TODO: Need a better way to determine which cities should
					serve as invasion launch locations */
				// Inertia so units don't just chase transports around the map
				iValue = iValue / 2;
				if (pLoopCity->getArea().getAreaAIType(kOurTeam.getID()) == AREAAI_ASSAULT)
				{
					// If in assault, transports may be at sea ... tend to stay where they left from
					// to speed reinforcement
					iValue += pLoopCity->getPlot().plotCount(PUF_isAvailableUnitAITypeGroupie,
							UNITAI_ATTACK_CITY, -1, getOwner());
				}
				// Attraction to cities which are serving as launch/pickup points
				iValue += 3 * pLoopCity->getPlot().plotCount(PUF_isUnitAIType,
							UNITAI_ASSAULT_SEA, -1, getOwner());
				iValue += 2 * pLoopCity->getPlot().plotCount(PUF_isUnitAIType,
							UNITAI_ESCORT_SEA, -1, getOwner());
				iValue += 5 * GET_PLAYER(getOwner()).AI_plotTargetMissionAIs(
						pLoopCity->getPlot(), MISSIONAI_PICKUP);
			}
			else iValue /= 8;
		}
		if (iValue * 200 <= iBestValue)
			continue;
		// BETTER_BTS_AI_MOD: END
		int iPathTurns;
		if (generatePath(pLoopCity->getPlot(), MOVE_AVOID_ENEMY_WEIGHT_3, true,
			&iPathTurns))
		{
			iValue *= 1000;
			iValue /= 5 + iPathTurns;
			if (!at(pLoopCity->getPlot()))
			{
				/*	advc: Moved from the start of the function; don't need to cache this.
					Note that, while we should only prepare vs. 1 target at a time,
					SneakAttackPreparing is also true for the vassals of our target.*/
				for (TeamIter<MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> itTarget(kOurTeam.getID());
					itTarget.hasNext(); ++itTarget)
				{
					if (kOurTeam.AI_isSneakAttackPreparing(itTarget->getID()) &&
						pLoopCity->isVisible(itTarget->getID()))
					{
						iValue /= 2;
						break;
					}
				}
			}
			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				pStagingPlot = pLoopCity->plot();
				pEndTurnPlot = &getPathEndTurnPlot();
			}
		}
	}
	if (pStagingPlot != NULL)
	{
		if (at(*pStagingPlot))
		{
			getGroup()->pushMission(MISSION_SKIP);
			return true;
		}
		else
		{
			pushGroupMoveTo(*pEndTurnPlot,
					// K-Mod:
					MOVE_AVOID_ENEMY_WEIGHT_3, false, false, MISSIONAI_GROUP, pStagingPlot);
			return true;
		}
	}
	return false;
}

/*  advc: Functions added (and used) by the BtS expansion, commented out by BBAI;
	bodies now deleted. */
/*bool CvUnitAI::AI_seaRetreatFromCityDanger()
{
	...
}
bool CvUnitAI::AI_airRetreatFromCityDanger()
{
	...
}
bool CvUnitAI::AI_airAttackDamagedSkip()
{
	...
}*/

/*  Returns true if a mission was pushed
	-- or we should wait for another unit to bombard... */
bool CvUnitAI::AI_followBombard()
{
	if (canBombard(getPlot()))
	{
		getGroup()->pushMission(MISSION_BOMBARD);
		return true;
	}

	// K-Mod note: I've disabled the following code because it seems like a timewaster with very little benefit.
	// The code checks if we are standing next to a city, and then checks if we have any other readyToMove group
	// next to the same city which can bombard... if so, return true.
	// I suppose the point of the code is to block our units from issuing a follow-attack order if we still have
	// some bombarding to do. -- But in my opinion, such checks, if we want them, should be done by the attack code.
	/*if (getDomainType() == DOMAIN_LAND) {
		for (int iI = 0; iI < NUM_DIRECTION_TYPES; iI++) {
			CvPlot* pAdjacentPlot1 = plotDirection(getX(), getY(), ((DirectionTypes)iI));
			if (pAdjacentPlot1 != NULL) {
				if (pAdjacentPlot1->isCity()) {
					if (AI_potentialEnemy(pAdjacentPlot1->getTeam(), pAdjacentPlot1)) {
						for (int iJ = 0; iJ < NUM_DIRECTION_TYPES; iJ++) {
							pAdjacentPlot2 = plotDirection(pAdjacentPlot1->getX(), pAdjacentPlot1->getY(), ((DirectionTypes)iJ));
							if (pAdjacentPlot2 != NULL) {
								CLLNode<IDInfo>* pUnitNode = pAdjacentPlot2->headUnitNode();
								while (pUnitNode != NULL) {
									pLoopUnit = ::getUnit(pUnitNode->m_data);
									pUnitNode = pAdjacentPlot2->nextUnitNode(pUnitNode);
									if (pLoopUnit->getOwner() == getOwner()) {
										if (pLoopUnit->canBombard(pAdjacentPlot2)) {
											if (pLoopUnit->isGroupHead()) {
												if (pLoopUnit->getGroup() != getGroup()) {
													if (pLoopUnit->getGroup()->readyToMove())
														return true;
	} } } } } } } } } } } }*/ // BtS

	return false;
}

/*  <advc.033> Counts units in kPlot that this unit could attack and returns
	the defender count and total unit count as a pair (iDefenders,iUnits). */
std::pair<int,int> CvUnitAI::AI_countPiracyTargets(CvPlot const& kPlot,
	bool bStopIfAnyTarget) const
{
	std::pair<int,int> iiDefTotal(0, 0);
	if(!isAlwaysHostile(kPlot))
		//|| !kPlot.isVisible(getTeam(), false))// This is handled by searchRange
	{
		return iiDefTotal;
	}
	FOR_EACH_UNIT_IN(pLoopUnit, kPlot)
	{
		if (pLoopUnit->isInvisible(getTeam(), false))
			continue;
		if (!GET_PLAYER(getOwner()).AI_isPiracyTarget(pLoopUnit->getOwner()))
			continue;
		iiDefTotal.second++;
		if (bStopIfAnyTarget)
			return iiDefTotal;
		if (pLoopUnit->canDefend())
			iiDefTotal.first++;
	}
	return iiDefTotal;
}


bool CvUnitAI::AI_isAnyPiracyTarget(CvPlot const& p) const
{
	return (AI_countPiracyTargets(p, true).second > 0);
}// </advc.033>

// Returns true if this plot needs some defense...
bool CvUnitAI::AI_defendPlot(CvPlot* pPlot)
{
	if (!canDefend(pPlot))
		return false;

	CvCityAI const* pCity = pPlot->AI_getPlotCity();
	if (pCity != NULL)
	{
		if (pCity->getOwner() == getOwner())
		{
			if (pCity->AI_isDanger())
				return true;
		}
	}
	else
	{
		if (getGroupSize() == 1 && // advc.010
			pPlot->plotCount(PUF_canDefendGroupHead, -1, -1, getOwner(),
			// advc.001s: Want up to 1 defender per domain type
			NO_TEAM, PUF_isDomainType, getDomainType())
			<= (atPlot(pPlot) ? 1 : 0))
		{
			/*if (pPlot->plotCount(PUF_cannotDefend, -1, -1, getOwner()) > 0)
				return true*/
			// <advc.010>
			int iTotalProductionCost = 0;
			FOR_EACH_UNIT_IN(pUnit, *pPlot)
			{
				if (pUnit->getOwner() == getOwner() && !pUnit->canDefend() &&
					/*  advc.001s: A land unit can defend non-land units in a Fort,
						but not vice versa. */
					(getDomainType() == DOMAIN_LAND ||
					pUnit->getDomainType() == getDomainType()))
				{
					if (pUnit->hasCargo() || pUnit->isFound())
						return true;
					int iProduction = pUnit->getUnitInfo().getProductionCost();
					if (iProduction <= 0) // special unit
						return true;
					iTotalProductionCost += iProduction;
					if (iTotalProductionCost * 5 > m_pUnitInfo->getProductionCost() * 3)
						return true;
				}
			} // </advc.010>
			/*if (pPlot->defenseModifier(getTeam(), false) >= 50 && pPlot->isRoute() && pPlot->getTeam() == getTeam())
				return true;*/ // (commented out by the BtS expansion)
		}
	}

	return false;
}

int CvUnitAI::AI_pillageValue(CvPlot const& kPlot, int iBonusValueThreshold)
{
	FAssert(canPillage(kPlot) || canAirBombAt(kPlot) || (getGroup()->getCargo() > 0));

	if (!kPlot.isOwned())
		return 0;

	int iValue = 0;

	int iBonusValue = 0;
	BonusTypes eNonObsoleteBonus = kPlot.isRevealed(
			// K-Mod:
			getTeam()) ? kPlot.getNonObsoleteBonusType(kPlot.getTeam(), true) : NO_BONUS;
	if (eNonObsoleteBonus != NO_BONUS)
	{
		//iBonusValue = (GET_PLAYER(kPlot.getOwner()).AI_bonusVal(eNonObsoleteBonus));
		iBonusValue = GET_PLAYER(kPlot.getOwner()).AI_bonusVal(eNonObsoleteBonus, 0); // K-Mod
	}

	if (iBonusValueThreshold > 0)
	{
		if (eNonObsoleteBonus == NO_BONUS)
			return 0;
		else if (iBonusValue < iBonusValueThreshold)
			return 0;
	}

	if ((getDomainType() != DOMAIN_AIR ||
		// advc.255: (Though the AI will currently not air bomb routes)
		kPlot.getRevealedImprovementType(getTeam()) == NO_IMPROVEMENT) &&
		kPlot.//isRoute()
		getRevealedRouteType(getTeam()) != NO_ROUTE) // advc.001i
	{
		iValue++;
		if (eNonObsoleteBonus != NO_BONUS)
		{
			//iValue += iBonusValue * 4;
			// K-Mod. (many more iBonusValues will be added again later anyway)
			iValue += iBonusValue;
		}
		FOR_EACH_ADJ_PLOT(kPlot) // K-Mod (bugfix): was *this
		{
			if (pAdj->getTeam() != kPlot.getTeam())
				continue;
			if (pAdj->isCity())
				iValue += 10;
			//if (!pAdj->isRoute())
			// advc.001i:
			if (pAdj->getRevealedRouteType(getTeam()) == NO_ROUTE)
			{
				if (!pAdj->isWater() && !pAdj->isImpassable())
					iValue += 2;
			}
		}
	}

	/*if (kPlot.getImprovementDuration() > ((kPlot.isWater()) ? 20 : 5))
		eImprovement = kPlot.getImprovementType();
	else eImprovement = kPlot.getRevealedImprovementType(getTeam(), false);*/
	ImprovementTypes eImprovement = (kPlot.getImprovementDuration() > 20 ?
			kPlot.getImprovementType() : kPlot.getRevealedImprovementType(getTeam()));
	if (eImprovement != NO_IMPROVEMENT)
	{
		if (kPlot.getWorkingCity() != NULL)
		{
			iValue += (kPlot.calculateImprovementYieldChange(eImprovement,
					YIELD_FOOD, kPlot.getOwner()) * 5);
			iValue += (kPlot.calculateImprovementYieldChange(eImprovement,
					YIELD_PRODUCTION, kPlot.getOwner()) * 4);
			iValue += (kPlot.calculateImprovementYieldChange(eImprovement,
					YIELD_COMMERCE, kPlot.getOwner()) * 3);
		}

		if (getDomainType() != DOMAIN_AIR)
			iValue += GC.getInfo(eImprovement).getPillageGold();
		if (eNonObsoleteBonus != NO_BONUS)
		{
			//if (GC.getInfo(eImprovement).isImprovementBonusTrade(eNonObsoleteBonus))
			// <K-Mod>
			if (GET_PLAYER(kPlot.getOwner()).doesImprovementConnectBonus(
				eImprovement, eNonObsoleteBonus)) // </K-Mod>
			{
				int iTempValue = iBonusValue * 4;

				if (kPlot.isConnectedToCapital() && kPlot.getPlotGroupConnectedBonus(
					kPlot.getOwner(), eNonObsoleteBonus) == 1)
				{
					iTempValue *= 2;
				}

				iValue += iTempValue;
			}
		}
	}
	return iValue;
}

// <advc.121>
int CvUnitAI::AI_connectBonusCost(CvPlot const& p, BuildTypes eBuild, int iMissingWorkersInArea) const
{
	PROFILE_FUNC();
	/*int iValue = 10000;
	iValue /= (GC.getInfo(eBuild).getTime() + 1);*/ // BtS (originally in AI_improveBonus)
	/*  <advc.121> The above means that the longer a build takes, the smaller is
		its (cost) value. So Forts are always preferred over cheaper Plantations etc.
		(There are similar issues in AI_irrigateTerritory and AI_fortifyTerritory,
		but w/o harmful consequences. CvCityAI::AI_getImprovementValue also divides
		by the build time, but that function gets it right as it computes a maximum.) */

	// Ad-hoc heuristic for Fort building:  (overlaps with AI_getPlotDefendersNeeded; fixme?)
	ImprovementTypes const eImpr = GC.getInfo(eBuild).getImprovement();
	CvImprovementInfo const& kImpr = GC.getInfo(eImpr);
	int iDefenseValue = kImpr.getDefenseModifier();
	// The AI isn't going to station units on an island without cities
	if(p.getArea().getCitiesPerPlayer(getOwner()) <= 0 ||  /* <advc.035> */
		GET_PLAYER(getOwner()).AI_isPlotContestedByRival(p))
	{
		iDefenseValue = 0;
	} // </advc.035>
	/*  Prioritize Forts on tiles with high natural defense and on important
		resources that may later be guarded. */
	if(iDefenseValue > 0)
	{
		iDefenseValue += p.defenseModifier(getTeam(), true);
		BonusTypes eBonus = p.getBonusType(getTeam());
		if(eBonus == NO_BONUS)
		{
			FAssert(eBonus != NO_BONUS);
			return -1;
		}
		/*  bonusVal is usually just a single digit; small double digit if it's
			an important strategic resource. */
		iDefenseValue += GET_PLAYER(getOwner()).AI_bonusVal(eBonus, 0);
		/*  (Not much of a point in checking p.isAdjacentToPlayer for all rivals.
			This function is only called for unworkable tiles, which are usually
			near a border.) */
	}
	int iCost = GC.getInfo(eBuild).getTime();
	// No cost for leaving an existing improvement alone
	if(eImpr == p.getImprovementType())
		iCost = 0;
	// Time is more dear when workers are busy
	int iMultiplier = 2 * (std::max(0, iMissingWorkersInArea) + 1);
	// Halve the cost when there's nothing to do
	if(iMissingWorkersInArea == 0)
		iMultiplier = 1;
	// Account for having to replace a Fort later
	if(kImpr.isActsAsCity() && GET_PLAYER(getOwner()).AI_isAdjacentCitySite(p, true))
		iMultiplier++;
	iCost *= iMultiplier;
	iCost /= 2;
	int const iDefenseWeight = 20;
	int r = iCost - iDefenseWeight * iDefenseValue;
	if(kImpr.isActsAsCity() && (p.isConnectSea() ||
		/*  If no cities in area, only a Fort will connect the bonus.
			(Unless workable, see advc.124, but p isn't workable.) */
		GET_TEAM(getTeam()).countNumCitiesByArea(p.getArea()) <= 0))
	{
		/*  That means, eBuild is a very good build. But note that the build time
			component of iCost is on a times-100 scale, so -1000 doesn't guarantee
			that a Fort is built. */
		r -= 1000;
	}
	return r;
	// XXX feature production???
	/*  As for the Firaxis comment above:
		Feature production is handled elsewhere (see advc.117). That said, once
		a Fort is built, I'm not sure if Workers will still consider chopping.
		If they do, then the defense bonus from a Forest shouldn't be counted fully
		here. (Tbd. but not important.) */
}

/*  Function needed for advc.040. In part copied from AI_connectBonus.
	I guess taking into account safe automation makes this an AI function. */
bool CvUnitAI::AI_canConnectBonus(CvPlot const& p, BuildTypes eBuild) const
{	// Some old BtS code
	//if (GC.getInfo(eBuild).getImprovement() != NO_IMPROVEMENT)
	//if (GC.getInfo((ImprovementTypes) GC.getInfo(eBuild).getImprovement()).isImprovementBonusTrade(eNonObsoleteBonus) || (!pLoopPlot->isCityRadius() && GC.getInfo((ImprovementTypes) GC.getInfo(eBuild).getImprovement()).isActsAsCity()))

	CvPlayer const& kOwner = GET_PLAYER(getOwner());
	BonusTypes eBonus = p.getNonObsoleteBonusType(kOwner.getTeam());
	if(eBonus == NO_BONUS)
		return false;
	ImprovementTypes const eImpr = GC.getInfo(eBuild).getImprovement();
	if(eImpr == NO_IMPROVEMENT ||
		!kOwner.doesImprovementConnectBonus(eImpr, eBonus)) // K-Mod
	{
		return false;
	}
	/*  Important for AI_connectBonus that true is returned if the current improvement
		already connects the resource */
	if(p.getImprovementType() == eImpr)
		return true;
	if(!canBuild(p, eBuild))
		return false;
	if(p.isFeature() &&
		GC.getInfo(eBuild).isFeatureRemove(p.getFeatureType()) &&
		kOwner.isHumanOption(PLAYEROPTION_LEAVE_FORESTS))
	{
		return false;
	}
	return true;
} // </advc.121>


int CvUnitAI::AI_searchRange(int iRange)
{
	if (iRange == 0)
		return 0;
	/*	advc.opt (note): Flat-movement now also true for all air units.
		(Not sure if this function gets called for those ...) */
	if (flatMovementCost() || getDomainType() == DOMAIN_SEA)
		return iRange * baseMoves();
	return (iRange + 1) * (baseMoves() + 1);
}

// XXX at some point test the game with and without this function...
/*	advc (comment): This function performs some initial checks as to whether the unit
	can reach pPlot w/o first entering a transport.
	For land units not in cargo, a faster inline check can accomplish almost
	the same thing - except for the unused NoRevealMap and MoveAllTerrain tags.
	So I've replaced some AI_plotValid calls with same-area or AI_canEnterByLand checks.  */
bool CvUnitAI::AI_plotValid(CvPlot const* pPlot) /* advc: */ const
{
	/*  advc.003o: Called very often; though not nearly as often as in K-Mod.
		Still a couple of percentage points of the total turn time according
		to the internal profiler.
		Regarding the XXX comment above: It's difficult to imagine that
		removing this function entirely would improve performance. */
	//PROFILE_FUNC();
	if (getUnitInfo().isNoRevealMap() && willRevealAnyPlotFrom(*pPlot))
		return false;

	switch (getDomainType())
	{
	case DOMAIN_SEA:
		/*return (pPlot->isWater() || canMoveAllTerrain() ||
			pPlot->isFriendlyCity(*this, true) && pPlot->isCoastalLand());*/
		// advc.opt: This omits checks for enemy units; hopefully not needed.
		return isRevealedValidDomain(*pPlot);
	case DOMAIN_LAND:
		return (//pPlot->isArea(getArea())
				/*  advc.030: Replacing the above. Wouldn't hurt to do that for
					DOMAIN_SEA as well, but no need. For DOMAIN_LAND, the change is
					only important if a land unit is given canMoveImpassable. */
				pPlot->getArea().canBeEntered(getArea(), this) ||
				canMoveAllTerrain());
	default:
		FErrorMsg(/* advc: */"AI_plotValid is only for land and sea units");
		return false;
	}
}

/*int CvUnitAI::AI_finalOddsThreshold(CvPlot* pPlot, int iOddsThreshold)
{
// K-Mod note: This function is seriously flawed
// advc: Body deleted on 4 Dec 2019
}*/

/*	advc.003u: Extracted from K-Mod's AI_getWeightedOdds, which I've moved to CvSelectionGroupAI.
	Adjusts the combat odds based on opportunity. */
int CvUnitAI::AI_opportuneOdds(int iActualOdds, CvUnit const& kDefender) const
{
	int const iOdds = iActualOdds; // abbreviate
	int iR = iOdds;
	// adjust the values based on the relative production cost of the units.
	{
		int iOurCost = getUnitInfo().getProductionCost();
		int iTheirCost = kDefender.getUnitInfo().getProductionCost();
		if (iOurCost > 0 && iTheirCost > 0 && iOurCost != iTheirCost)
		{
			//iR += iOdds * (100 - iOdds) * 2 * iTheirCost / (iOurCost + iTheirCost) / 100;
			//iR -= iOdds * (100 - iOdds) * 2 * iOurCost / (iOurCost + iTheirCost) / 100;
			int x = iOdds * (100 - iOdds) * 2 / (iOurCost + iTheirCost + 20);
			iR += x * (iTheirCost - iOurCost) / 100;
		}
	}
	// similarly, adjust based on the LFB value (slightly diluted)
	{
		int iDilution = GC.getDefineINT(CvGlobals::LFB_BASEDONEXPERIENCE) +
				GC.getDefineINT(CvGlobals::LFB_BASEDONHEALER) +
				intdiv::round(10 * GC.getDefineINT(CvGlobals::LFB_BASEDONEXPERIENCE) *
				(GC.getGame().getCurrentEra() - GC.getGame().getStartEra() + 1),
				std::max(1, GC.getNumEraInfos() - GC.getGame().getStartEra()));
		int iOurValue = LFBgetRelativeValueRating() + iDilution;
		int iTheirValue = kDefender.LFBgetRelativeValueRating() + iDilution;

		int x = iOdds * (100 - iOdds) * 2 / std::max(1, iOurValue + iTheirValue);
		iR += x * (iTheirValue - iOurValue) / 100;
	}

	CvPlot const& kDefenderPlot = *kDefender.plot();

	// adjust down if the enemy is on a defensive tile - we'd prefer to attack them on open ground.
	if (!kDefender.noDefensiveBonus())
	{
		iR -= (100 - iOdds) * kDefenderPlot.defenseModifier(kDefender.getTeam(), false,
			getTeam()) // advc.012
			/ (getDomainType() == DOMAIN_SEA ? 100 : 300);
	}

	// adjust the odds up if the enemy is wounded. We want to attack them now before they heal.
	iR += iOdds * (100 - iOdds) * kDefender.getDamage() / (100 * kDefender.maxHitPoints());
	// adjust the odds down if our attacker is wounded - but only if healing is viable.
	if (isHurt() && healRate() > 10)
		iR -= iOdds * (100 - iOdds) * getDamage() / (100 * maxHitPoints());

	// We're extra keen to take cites when we can...
	if (kDefenderPlot.isCity() && AI_countEnemyDefenders(kDefenderPlot) == 1)
		iR += (100 - iOdds) / 3;

	return iR;
}

// K-Mod. A simple hash of the unit's birthmark.
/*	This is to be used for getting a 'random' number which depends on the unit
	but which does not vary from turn to turn. */
unsigned CvUnitAI::AI_unitBirthmarkHash(int iExtra) const
{
	unsigned iHash = AI_getBirthmark() + iExtra;
	iHash *= 2654435761; // golden ratio of 2^32;
	return iHash;
}

// another 'random' hash, but which depends on a particular plot
unsigned CvUnitAI::AI_unitPlotHash(const CvPlot* pPlot, int iExtra) const
{
	return AI_unitBirthmarkHash(pPlot->plotNum() + iExtra);
} // K-Mod end

/*	advc (note): The "Extra" in the function name refers to how the function is
	used in AI_omniGroup (originally AI_group). */
int CvUnitAI::AI_stackOfDoomExtra() const
{
	//return ((AI_getBirthmark() % (1 + GET_PLAYER(getOwner()).getCurrentEra())) + 4);
	// advc: K-Mod and AdvCiv code moved into new CvPlayerAI function
	return GET_PLAYER(getOwner()).AI_neededCityAttackers(
			getArea(), // advc.104p
			AI_getBirthmark());
}

// This function has been significantly modified for K-Mod
bool CvUnitAI::AI_stackAttackCity(int iPowerThreshold)
{
	PROFILE_FUNC();

	FAssert(canMove());

	CvPlot const* pCityPlot = NULL;
	FOR_EACH_ADJ_PLOT(getPlot())
	{
		CvPlot const& p = *pAdj;
		//if (!AI_plotValid(p)) continue; // advc.opt: We're a land unit looking for an adjacent city
		if (!p.isCity()) // K-Mod. We want to attack a city. We don't care about guarded forts!
			//|| (pLoopPlot->isCity(true) && pLoopPlot->isVisibleEnemyUnit(this)))
		{
			continue;
		}
		if (AI_mayAttack(p.getTeam(), p))
		{
			if (//!at(p) && // advc: Exclude this from the beginning
				//((bFollow) ? canMoveInto(pLoopPlot, /*bAttack*/ true, /*bDeclareWar*/ true) : (generatePath(pLoopPlot, 0, true, &iPathTurns) && (iPathTurns <= iRange))))
				getGroup()->canMoveOrAttackInto(p, true, true))
			{
				// K-Mod
				if (iPowerThreshold < 0)
				{
					// basic threshold calculation.
					CvCity* pCity = p.getPlotCity();
					/*	This automatic threshold calculation is used by AI_follow;
						and so we can't assume this unit is the head of the group.
						... But I think it's fair to assume that, if our group
						has any bombard, the head unit will have it. */
					if (getGroup()->getHeadUnit()->bombardRate() > 0)
					{
						/*	if we can bombard, then we should do a rough calculation
							to give us a 'skip bombard' threshold. */
						iPowerThreshold = ((GC.getMAX_CITY_DEFENSE_DAMAGE() - pCity->getDefenseDamage()) *
								GC.getDefineINT(CvGlobals::BBAI_SKIP_BOMBARD_BASE_STACK_RATIO) +
								pCity->getDefenseDamage() * GC.getDefineINT(CvGlobals::BBAI_SKIP_BOMBARD_MIN_STACK_RATIO)) /
								std::max(1, GC.getMAX_CITY_DEFENSE_DAMAGE());
					}
					else
					{
						// if we have no bombard ability - just use the minimum threshold
						iPowerThreshold = GC.getDefineINT(CvGlobals::BBAI_SKIP_BOMBARD_MIN_STACK_RATIO);
					}
					FAssert(iPowerThreshold >= GC.getDefineINT(CvGlobals::BBAI_ATTACK_CITY_STACK_RATIO));
				} // K-Mod end
				if (AI_getGroup()->AI_compareStacks(&p, true) >= iPowerThreshold)
					pCityPlot = &p;
			}
		}
		// there can only be one city. advc (tbd.): Not true if MIN_CITY_RANGE==1.
		break;
	}

	if (pCityPlot != NULL)
	{
		if (gUnitLogLevel >= 1 && pCityPlot->getPlotCity() != NULL)
		{
			logBBAI("    Stack for player %d (%S) decides to attack city %S with stack ratio %d", getOwner(), GET_PLAYER(getOwner()).getCivilizationDescription(0), pCityPlot->getPlotCity()->getName(0).GetCString(), AI_getGroup()->AI_compareStacks(pCityPlot, true));
			logBBAI("    City %S has defense modifier %d, %d with ignore building", pCityPlot->getPlotCity()->getName(0).GetCString(), pCityPlot->getPlotCity()->getDefenseModifier(false), pCityPlot->getPlotCity()->getDefenseModifier(true));
		}

		FAssert(!at(*pCityPlot));
		if (AI_considerDOW(*pCityPlot))
		{	// <advc.163>
			if (!canMove())
				return true;
		} // </advc.163>
		pushGroupMoveTo(*pCityPlot, pCityPlot->isVisibleEnemyDefender(this) ?
				MOVE_DIRECT_ATTACK : NO_MOVEMENT_FLAGS);
		return true;
	}

	return false;
}

// advc (comment): into a non-hostile city
bool CvUnitAI::AI_moveIntoCity(int iRange)
{
	PROFILE_FUNC();
	FAssert(canMove());
	if (getPlot().isCity())
		return false;

	CvPlot* pBestPlot = NULL;
	int iBestValue = 0;
	for (SquareIter it(*this, AI_searchRange(iRange), false); it.hasNext(); ++it)
	{
		CvPlot& p = *it;
		if (!p.isOwned() || // advc.opt
			!AI_plotValid(p) || isEnemy(p))
		{
			continue;
		}
		//if (!p.isCity() && !p.isCity(true))
		if (!GET_TEAM(getTeam()).isRevealedBase(p)) // advc
			continue;

		int iPathTurns;
		if (canMoveInto(p, false) &&
			generatePath(p, NO_MOVEMENT_FLAGS, true, &iPathTurns, 1) &&
			iPathTurns <= 1)
		{
			int iValue = 1;
			if (p.isCity())
				iValue += p.getPlotCity()->getPopulation();
			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				pBestPlot = &getPathEndTurnPlot();
			}
		}
	}

	if (pBestPlot != NULL)
	{
		pushGroupMoveTo(*pBestPlot);
		return true;
	}

	return false;
}

/*	bolsters the culture of the weakest city.
	returns true if a mission is pushed.
	disabled by K-Mod. (not currently used) */
//bool CvUnitAI::AI_artistCultureVictoryMove()
/*  advc: Body deleted. Some BBAI code was in there too; can always get
	it back from the K-Mod source code. */
//{  ... }

// advc.003j: This is never called (AI Worker stealing). Removed some clutter.
#if 0
bool CvUnitAI::AI_poach()
{
	int iBestPoachValue = 0;
	CvPlot* pBestPoachPlot = NULL;
	TeamTypes eBestPoachTeam = NO_TEAM;
	if (!GC.getGame().isOption(GAMEOPTION_AGGRESSIVE_AI))
		return false;
	if (GET_TEAM(getTeam()).getNumMembers() > 1)
		return false;
	int iNoPoachChance = GET_PLAYER(getOwner()).AI_totalUnitAIs(UNITAI_WORKER);
	iNoPoachChance += GET_PLAYER(getOwner()).getNumCities();
	iNoPoachChance = std::max(0, (iNoPoachChance - 1) / 2);
	if (!SyncRandOneChanceIn(iNoPoachChance))
		return false;
	//if (GET_TEAM(getTeam()).getAnyWarPlanCount(true) > 0)
	if(GET_PLAYER(getOwner()).AI_isFocusWar(area())) // advc.105
		return false;
	FAssert(canAttack());
	//Look for a unit which is non-combat and has a capture unit type
	for (SquareIter it(*this, 1, false); it.hasNext(); ++it) {
		//if (iX != 0 && iY != 0) // advc.001: Looks like an error; probably '||' intended.
		CvPlot* pLoopPlot = &(*it);
		if (pLoopPlot->getTeam() != getTeam() && pLoopPlot->isVisible(getTeam(), false)) {
			int iPoachCount = 0;
			int iDefenderCount = 0;
			CvUnit* pPoachUnit = NULL;
			CLLNode<IDInfo>* pUnitNode = pLoopPlot->headUnitNode();
			while (pUnitNode != NULL) {
				CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
				pUnitNode = pLoopPlot->nextUnitNode(pUnitNode);
				if ((pLoopUnit->getTeam() != getTeam()) &&
						GET_TEAM(getTeam()).canDeclareWar(pLoopUnit->getTeam())) {
				if (!pLoopUnit->canDefend()) {
						if (pLoopUnit->getCaptureUnitType(getCivilizationType()) != NO_UNIT) {
							iPoachCount++;
							pPoachUnit = pLoopUnit;
						}
					}
					else iDefenderCount++;
				}
			}
			if (pPoachUnit != NULL) {
				if (iDefenderCount == 0) {
					int iValue = iPoachCount * 100;
					iValue -= iNoPoachChance * 25;
					if (iValue > iBestPoachValue) {
						iBestPoachValue = iValue;
						pBestPoachPlot = pLoopPlot;
						eBestPoachTeam = pPoachUnit->getTeam();
					}
				}
			}
		}
	}
	if (pBestPoachPlot != NULL) { //No war roll.
		if (!GET_TEAM(getTeam()).AI_performNoWarRolls(eBestPoachTeam)) {
			GET_TEAM(getTeam()).declareWar(eBestPoachTeam, true, WARPLAN_LIMITED);
			FAssert(!at(*pBestPoachPlot));
			pushGroupMoveTo(*pBestPoachPlot, MOVE_DIRECT_ATTACK);
			return true;
		}
	}
	return false;
}
#endif

// K-Mod. I've rewritten most of this function.
bool CvUnitAI::AI_choke(int iRange, bool bDefensive, MovementFlags eFlags)
{
	PROFILE_FUNC();

	scaled rDefensive;
	FOR_EACH_UNIT_IN(pLoopUnit, *getGroup())
	{
		if (!pLoopUnit->noDefensiveBonus())
			rDefensive++;
	}
	rDefensive /= getGroup()->getNumUnits();

	CvPlot* pBestPlot = 0;
	CvPlot* pEndTurnPlot = 0;
	int iBestValue = //0
			// advc.083: Don't park a big stack for little gain
			(bDefensive ? 0 : 6 * getGroup()->getNumUnits());
	// <advc.300> Don't use more than a couple of units for choking Barbarians
	bool const bSmallGroup = (getGroup()->getNumUnits() <=
			GET_PLAYER(getOwner()).AI_getCurrEraFactor() + 1); // </advc.300>
	for (SquareIter it(*this, iRange); it.hasNext(); ++it)
	{
		CvPlot& p = *it;
		if (!p.isOwned() || !isEnemy(p.getTeam()) || p.isVisibleEnemyUnit(this))
			continue;
        // doc: don't choke different domain
        if (p.isWater() != plot()->isWater())
            continue;
        // doc: don't choke minors
        if (p.isMinorCiv())
            continue;
		// <advc.300>
		if (p.getOwner() == BARBARIAN_PLAYER && !bSmallGroup)
			continue; // </advc.300>

		int iPathTurns;
		if (p.getWorkingCity() == NULL ||
			!generatePath(p, eFlags, true, &iPathTurns, iRange))
		{
			continue;
		}
		FAssert(p.getWorkingCity()->getTeam() == p.getTeam());
				//pLoopPlot->defenseModifier(getTeam(), false) // K-Mod
		int iValue = (bDefensive ? /* advc.012: */ AI_plotDefense(&p) - 15 : 0);
		if (p.getBonusType(getTeam()) != NO_BONUS)
		{
			iValue = GET_PLAYER(p.getOwner()).AI_bonusVal(p.getBonusType(), 0);
		}
		iValue += p.getYield(YIELD_PRODUCTION) * 9; // was 10
		iValue += p.getYield(YIELD_FOOD) * 12; // was 10
		iValue += p.getYield(YIELD_COMMERCE) * 5;

		if (at(p) && canPillage(p))
			iValue += AI_pillageValue(p, 0) / (bDefensive ? 2 : 1);
		if (iValue <= 0)
			continue;

		scaled rDefFactor = per100(bDefensive ? 25 : 50) +
				rDefensive * //p.defenseModifier(getTeam(), false)
				per100(AI_plotDefense(&p)); // advc.012
		iValue = (iValue * rDefFactor).round();

		if (bDefensive)
		{
			// for defensive, we care a lot about path turns
			iValue *= 10;
			iValue /= std::max(1, iPathTurns);
		}
		else
		{
			// otherwise we just want to block as many tiles as possible
			iValue *= 10;
			iValue /= std::max(1, p.getNumDefenders(getOwner()) +
					(at(p) ? 0 : getGroup()->getNumUnits()));
		}
		if (iValue > iBestValue)
		{
			pBestPlot = &p;
			pEndTurnPlot = &getPathEndTurnPlot();
			iBestValue = iValue;
		}
	}
	if (pBestPlot == NULL)
		return false;

	FAssert(pBestPlot->getWorkingCity());
	CvPlot* pChokedCityPlot = pBestPlot->getWorkingCity()->plot();
	if (atPlot(pBestPlot))
	{
		FAssert(atPlot(pEndTurnPlot));
		if (canPillage(getPlot()))
		{
			getGroup()->pushMission(MISSION_PILLAGE, -1, -1,
					eFlags, false, false, MISSIONAI_CHOKE, pChokedCityPlot);
		}
		else
		{
			getGroup()->pushMission(MISSION_SKIP, -1, -1,
					eFlags, false, false, MISSIONAI_CHOKE, pChokedCityPlot);
		}
		return true;
	}
	pushGroupMoveTo(*pEndTurnPlot, eFlags, false, false,
			MISSIONAI_CHOKE, pChokedCityPlot);
	return true;
}

// advc.012:
int CvUnitAI::AI_plotDefense(CvPlot const* pPlot) const
{
	// Don't check noDefensiveBonus here b/c this unit can be part of a stack
	//if(noDefensiveBonus()) return 0;
	if(pPlot == NULL)
		pPlot = plot();
	return GET_TEAM(getTeam()).AI_plotDefense(*pPlot);
}


bool CvUnitAI::AI_solveBlockageProblem(CvPlot* pDestPlot, bool bDeclareWar)
{
	PROFILE_FUNC();

	if (pDestPlot == NULL)
	{
		FAssert(pDestPlot != NULL);
		return false;
	}
	if (!gDLL->getFAStarIFace()->GeneratePath(&GC.getStepFinder(),
		getX(), getY(), pDestPlot->getX(), pDestPlot->getY(), false, 0, true))
	{
		return false;
	}
	for (FAStarNode* pStepNode = gDLL->getFAStarIFace()->GetLastNode(&GC.getStepFinder());
		pStepNode != NULL; pStepNode = pStepNode->m_pParent) // advc: replacing while loop
	{
		CvPlot const& kStepPlot = GC.getMap().getPlot(pStepNode->m_iX, pStepNode->m_iY);
		if (!canMoveOrAttackInto(kStepPlot) ||
			!generatePath(kStepPlot, NO_MOVEMENT_FLAGS, true))
		{
			continue;
		}
		if (bDeclareWar && pStepNode->m_pPrev != NULL)
		{
			CvPlot const& kPlot = GC.getMap().getPlot(
					pStepNode->m_pPrev->m_iX, pStepNode->m_pPrev->m_iY);
			CvTeamAI& kTeam = GET_TEAM(getTeam());
			if (kPlot.isOwned() && !canMoveInto(kPlot, true, true))
			{
				//if (!isPotentialEnemy(kPlot.getTeam(), &kPlot))
				if (!kTeam.AI_mayAttack(kPlot.getTeam()) && // advc
					kTeam.canDeclareWar(kPlot.getTeam()))
				{
					WarPlanTypes eWarPlan = WARPLAN_LIMITED;
					WarPlanTypes eExistingWarPlan = kTeam.AI_getWarPlan(
							pDestPlot->getTeam());
					if (eExistingWarPlan != NO_WARPLAN)
					{
						if (eExistingWarPlan == WARPLAN_TOTAL ||
							eExistingWarPlan == WARPLAN_PREPARING_TOTAL)
						{
							eWarPlan = WARPLAN_TOTAL;
						}
						if (!kTeam.isAtWar(pDestPlot->getTeam()))
							kTeam.AI_setWarPlan(pDestPlot->getTeam(), NO_WARPLAN);
					}
					kTeam.AI_setWarPlan(kPlot.getTeam(), eWarPlan);
					//return (AI_targetCity());
					return AI_goToTargetCity(
							MOVE_AVOID_ENEMY_WEIGHT_2 | MOVE_DECLARE_WAR); // K-Mod / BBAI
				}
			}
		}
		if (kStepPlot.isVisibleEnemyUnit(this))
		{
			FAssert(canAttack());
			CvPlot const* pBestPlot = &kStepPlot;
			/*	To prevent puppeteering attempt to barge through
				if quite close */
			if (getPathFinder().getPathTurns() > 3)
				pBestPlot = &getPathEndTurnPlot();
			pushGroupMoveTo(*pBestPlot, MOVE_DIRECT_ATTACK);
			return true;
		}
	}

	return false;
}


int CvUnitAI::AI_calculatePlotWorkersNeeded(CvPlot const& kPlot, BuildTypes eBuild) const
{
	int const iWorkRate = workRate(true);
	if (iWorkRate <= 0)
	{
		FAssert(false);
		return 1;
	}

	int iBuildTime = kPlot.getBuildTime(eBuild, /* advc.251: */ getOwner())
			- kPlot.getBuildProgress(eBuild);
	int iTurns = iBuildTime / iWorkRate;
	if (iBuildTime > iTurns * iWorkRate)
		iTurns++;

	int iNeeded = std::max(1, (iTurns + 2) / 3);
	//if (pPlot->getBonusType() != NO_BONUS)
	// BETTER_BTS_AI_MOD, Bugfix, 7/31/08, jdog5000:
	if (kPlot.getNonObsoleteBonusType(getTeam()) != NO_BONUS)
		iNeeded *= 2;
	return iNeeded;
}

bool CvUnitAI::AI_canGroupWithAIType(UnitAITypes eUnitAI) const
{
	if (eUnitAI != AI_getUnitAIType())
	{
		switch (eUnitAI)
		{
		case (UNITAI_ATTACK_CITY):
			if (getPlot().isCity() &&
				GC.getGame().getGameTurn()
				- getPlot().getPlotCity()->getGameTurnAcquired() <= 1)
			{
				return false;
			}
			break;
		}
	}
	return true;
}


bool CvUnitAI::AI_allowGroup(CvUnitAI const& kUnit, UnitAITypes eUnitAI) const // advc.003u: 1st param was CvUnit
{
	CvSelectionGroupAI const* pGroup = kUnit.AI_getGroup();
	CvPlot* pPlot = kUnit.plot();

	if (&kUnit == this || !kUnit.isGroupHead() || pGroup == getGroup() ||
		kUnit.isCargo() || kUnit.AI_getUnitAIType() != eUnitAI)
	{
		return false;
	}
	switch (pGroup->AI_getMissionAIType())
	{
	case MISSIONAI_GUARD_CITY: // do not join groups that are guarding cities
	/*	do not join groups that are loading into transports
		(we might not fit and get stuck in loop forever) */
	case MISSIONAI_LOAD_SETTLER:
	case MISSIONAI_LOAD_ASSAULT:
	case MISSIONAI_LOAD_SPECIAL:
		return false;
	}

	if (pGroup->getActivityType() == ACTIVITY_HEAL)
	{
		/*	do not attempt to join groups which are healing this turn
			(healing is cleared every turn for automated groups,
			so we know we pushed a heal this turn) */
		return false;
	}

	if (!canJoinGroup(pPlot, pGroup))
		return false;

	// advc.001: There should be no harm in joining a threatened Settle group (from MNAI)
	/*if (eUnitAI == UNITAI_SETTLE)
	{
		// BETTER_BTS_AI_MOD, Unit AI, Efficiency, 08/20/09, jdog5000: was AI_getPlotDanger
		if (GET_PLAYER(getOwner()).AI_getAnyPlotDanger(*pPlot, 3))
			return false;
	}
	else*/ if (eUnitAI == UNITAI_ASSAULT_SEA)
	{
		if (!pGroup->hasCargo())
			return false;
	}

	if (getGroup()->getHeadUnitAIType() == UNITAI_CITY_DEFENSE)
	{
		if (getPlot().isCity() && getPlot().getTeam() == getTeam() &&
			getPlot().getBestDefender(getOwner())->getGroup() == getGroup())
		{
			return false;
		}
	}

	if (getPlot().getOwner() == getOwner())
	{
		CvPlot* pTargetPlot = pGroup->AI_getMissionAIPlot();
		if (pTargetPlot != NULL)
		{
			if (pTargetPlot->isOwned())
			{
				if (AI_isPotentialEnemyOf(pTargetPlot->getTeam(), *pTargetPlot))
				{
					//Do not join groups which have debarked on an offensive mission
					return false;
				}
			}
		}
	}

	if (kUnit.getInvisibleType() != NO_INVISIBLE &&
		getInvisibleType() == NO_INVISIBLE)
	{
		return false;
	}

	return true;
}

// advc.040:
bool CvUnitAI::AI_moveSettlerToCoast(int iMaxPathTurns)
{
	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());
	CvCity* pCurrentCity = getPlot().getPlotCity();
	if(pCurrentCity == NULL)
		return false;
	int const iGroupSz = getGroupSize();
	CvCity const* pBest = NULL;
	CvPlot* pEndPlot = NULL;
	int iBest = 0;
	FOR_EACH_CITYAI(c, kOwner)
	{
		CvPlot* pCityPlot = c->plot();
		if(c == pCurrentCity || !c->isArea(getArea()) || !c->isCoastal() ||
			c->AI_isEvacuating() ||
			kOwner.AI_getPlotDanger(*pCityPlot, 3, false, iGroupSz) > iGroupSz - 1)
		{
			continue;
		}
		int iPathTurns=-1;
		if(generatePath(*pCityPlot, NO_MOVEMENT_FLAGS, true, &iPathTurns, iMaxPathTurns))
		{
			int iValue = 5 + iMaxPathTurns - iPathTurns;
			if(pCityPlot->plotCheck(PUF_isUnitAIType, UNITAI_SETTLER_SEA, -1, kOwner.getID()) != NULL)
				iValue += 100;
			if(iValue > iBest)
			{
				iBest = iValue;
				pBest = c;
				pEndPlot = &getPathEndTurnPlot();
			}
		}
	}
	if(pBest == NULL)
		return false;
	pushGroupMoveTo(*pEndPlot,
			iGroupSz > 1 ? NO_MOVEMENT_FLAGS : MOVE_SAFE_TERRITORY, false, false,
			MISSIONAI_LOAD_SETTLER, pBest->plot());
	return true;
}

// doc
// TODO: include in great person move
bool CvUnitAI::AI_resolveCrisis(int iTurns)
{
	int iAnarchy = GET_PLAYER(getOwner()).getAnarchyTurns();
	int iOccupationTurns = 0;

    FOR_EACH_CITY(pCity, GET_PLAYER(getOwner()))
	{
		iOccupationTurns += pCity->getOccupationTimer();
	}

	if (iAnarchy + iOccupationTurns / 4 >= iTurns)
	{
		if (canResolveCrisis(getPlot()))
		{
			getGroup()->pushMission(MISSION_RESOLVE_CRISIS);
			return true;
		}

		CvCity* pClosestCity = GC.getMap().findCity(getX(), getY(), getOwner(), GET_PLAYER(getOwner()).getTeam());

		if (pClosestCity != NULL)
		{
			if (atPlot(pClosestCity->plot()))
			{
				getGroup()->pushMission(MISSION_RESOLVE_CRISIS);
				return true;
			}
			else
			{
				FAssert(!atPlot(pClosestCity->plot()));
				getGroup()->pushMission(MISSION_MOVE_TO, pClosestCity->getX(), pClosestCity->getY());
				getGroup()->pushMission(MISSION_RESOLVE_CRISIS, -1, -1, MOVE_SAFE_TERRITORY, (getGroup()->getLengthMissionQueue() > 0));
				return true;
			}
		}
	}

	return false;
}

// doc
// TODO: include in great person move
bool CvUnitAI::AI_reformGovernment(int iNumChanges)
{
	if (GET_PLAYER(getOwner()).getMaxAnarchyTurns() == 0)
		return false;

	int iChanges = 0;
    FOR_EACH_ENUM(CivicOption)
	{
		CivicTypes eCivic = GET_PLAYER(getOwner()).AI_bestCivic(eLoopCivicOption);
		if (eCivic != NO_CIVIC && eCivic != GET_PLAYER(getOwner()).getCivics(eLoopCivicOption))
			iChanges++;
	}

    if (iChanges < iNumChanges)
        return false;

	if (GET_PLAYER(getOwner()).AI_getCivicTimer() > 0)
	{
		getGroup()->pushMission(MISSION_SKIP);
		return true;
	}

	if (canReformGovernment(getPlot()))
	{
		getGroup()->pushMission(MISSION_REFORM_GOVERNMENT);
		return true;
	}

	return false;
}

// doc: AI only uses this mission to make peace in desparate situations
// TODO: include in great person move
bool CvUnitAI::AI_diplomaticMission(int iPowerMultiplier)
{
	CvCity* pEnemyCapital = NULL;
	int iEnemyPower = -MAX_INT;

	for (PlayerIter<MAJOR_CIV, NOT_SAME_TEAM_AS> it(getTeam()); it.hasNext(); ++it)
	{
        if (it->getID() == getOwner())
            continue;
		if (GET_TEAM(it->getTeam()).isVassal(getTeam()))
			continue;

		if (GET_TEAM(getTeam()).AI_surrenderTrade(it->getTeam(), iPowerMultiplier) == NO_DENIAL)
		{
			if (it->getPower() > iEnemyPower)
			{
				pEnemyCapital = it->getCapitalCity();
				iEnemyPower = it->getPower();
			}
		}
	}

	if (pEnemyCapital != NULL)
	{
		if (atPlot(pEnemyCapital->plot()))
		{
			getGroup()->pushMission(MISSION_DIPLOMATIC_MISSION);
			return true;
		}
		else
		{
			FAssert(!atPlot(pEnemyCapital->plot()));
			getGroup()->pushMission(MISSION_MOVE_TO, pEnemyCapital->getX(), pEnemyCapital->getY());
			getGroup()->pushMission(MISSION_DIPLOMATIC_MISSION, -1, -1, MOVE_SAFE_TERRITORY, (getGroup()->getLengthMissionQueue() > 0));
			return true;
		}

	}

	return false;
}

// doc
// TODO: include in great person move
bool CvUnitAI::AI_greatMission(int iCityPercent)
{
	ReligionTypes eReligion = GET_PLAYER(getOwner()).getStateReligion();
	if (eReligion == NO_RELIGION)
        return false;

	int iAreaCities = getArea().getCitiesPerPlayer(getOwner());
	int iSpreadCities = getArea().countCanSpread(eReligion, getOwner(), true);

	if (100 * iSpreadCities < iCityPercent * iAreaCities)
        return false;

	std::pair<CvPlot*, CvPlot*> spreadPlots = AI_spreadTarget(eReligion);
	CvPlot* pBestPlot = spreadPlots.first;
	CvPlot* pBestSpreadPlot = spreadPlots.second;

	if ((pBestPlot != NULL) && (pBestSpreadPlot != NULL))
	{
		if (atPlot(pBestSpreadPlot))
		{
			getGroup()->pushMission(MISSION_GREAT_MISSION);
			return true;
		}
		else
		{
			FAssert(!atPlot(pBestPlot));
			getGroup()->pushMission(MISSION_MOVE_TO, pBestPlot->getX(), pBestPlot->getY(), MOVE_SAFE_TERRITORY, false, false, MISSIONAI_SPREAD, pBestSpreadPlot);
			return true;
		}
	}

	return false;
}


// doc
void CvUnitAI::AI_satelliteMove()
{
	if (GET_TEAM(getTeam()).isAtWarWithMajorPlayer())
	{
		if (AI_satelliteDefendMove())
			return;
		if (AI_satelliteAttackMove())
			return;
	}

	if (AI_join(3))
		return;
	if (AI_satelliteDefendMove())
		return;
	if (AI_join())
		return;

	getGroup()->pushMission(MISSION_SKIP);
	return;
}

// doc
bool CvUnitAI::AI_satelliteDefendMove()
{
	if (!GC.getGame().isNukesValid())
		return false;
	if (!GET_TEAM(getTeam()).canSatelliteIntercept())
		return false;

	int iNukeValue = 8;
	CvCity* pDefendedCity = NULL;

    FOR_EACH_CITY_VAR(pCity, GET_PLAYER(getOwner()))
	{
		int iSatellites = pCity->plot()->plotCount(PUF_isUnitAIType, UNITAI_SATELLITE, -1, getOwner());

		if (iSatellites == 0 || (atPlot(pCity->plot()) && iSatellites == 1))
		{
			int iCurrentNukeValue = 1;

			iCurrentNukeValue += SyncRandNum(pCity->getPopulation() + 1);
			iCurrentNukeValue += std::max(0, pCity->getPopulation() - 10);

			iCurrentNukeValue += (pCity->getPopulation() * (100 + pCity->calculateCulturePercent(pCity->getOwner()))) / 100;

			if (iCurrentNukeValue > iNukeValue)
			{
				iNukeValue = iCurrentNukeValue;
				pDefendedCity = pCity;
			}
		}
	}

	if (pDefendedCity != NULL)
	{
		if (atPlot(pDefendedCity->plot()))
		{
			getGroup()->pushMission(MISSION_FORTIFY);
			return true;
		}

		getGroup()->pushMission(MISSION_MOVE_TO, pDefendedCity->getX(), pDefendedCity->getY());
		return true;
	}

	return false;
}

// doc
bool CvUnitAI::AI_satelliteAttackMove()
{
	if (!GC.getGame().isNukesValid())
		return false;
	if (!GET_TEAM(getTeam()).canSatelliteAttack())
		return false;

	CvCity* pNukeTarget = AI_offensiveSatelliteTarget();
	if (pNukeTarget != NULL)
	{
		if (!atPlot(pNukeTarget->plot()))
		{
			getGroup()->pushMission(MISSION_MOVE_TO, pNukeTarget->getX(), pNukeTarget->getY());
			return true;
		}

		getGroup()->pushMission(MISSION_SATELLITE_ATTACK);
		return true;
	}

	return false;
}

// doc
bool CvUnitAI::AI_rebuildMove(int iMinimumCost)
{
	CvCity* pBestCity = NULL;
	int iBestProduction = 0;
    FOR_EACH_CITY_VAR(pLoopCity, GET_PLAYER(getOwner()))
	{
		if (GET_PLAYER(getOwner()).AI_plotTargetMissionAIs(pLoopCity->getPlot(), MISSIONAI_REBUILD) == 0)
		{
			if (generatePath(pLoopCity->getPlot(), MOVE_SAFE_TERRITORY, true))
			{
				int iCurrentProduction = pLoopCity->getRebuildProduction();
				if (iCurrentProduction >= iMinimumCost && iCurrentProduction > iBestProduction)
				{
					pBestCity = pLoopCity;
					iBestProduction = iCurrentProduction;
				}
			}
		}
	}

	if (pBestCity != NULL)
	{
		if (!atPlot(pBestCity->plot()))
		{
			getGroup()->pushMission(MISSION_MOVE_TO, pBestCity->getX(), pBestCity->getY(), MOVE_SAFE_TERRITORY, false, false, MISSIONAI_REBUILD);
			return true;
		}

		getGroup()->pushMission(MISSION_REBUILD);
		return true;
	}

	return false;
}

void CvUnitAI::read(FDataStreamBase* pStream)
{
	CvUnit::read(pStream);

	uint uiFlag=0;
	pStream->Read(&uiFlag);	// flags for expansion

	pStream->Read(&m_iBirthmark);

	pStream->Read((int*)&m_eUnitAIType);
	pStream->Read(&m_iAutomatedAbortTurn);
}


void CvUnitAI::write(FDataStreamBase* pStream)
{
	REPRO_TEST_BEGIN_WRITE(CvString::format("Unit[AI](%d,%d,%d)", getID(), getX(), getY()));
	CvUnit::write(pStream);

	uint uiFlag=0;
	pStream->Write(uiFlag);

	pStream->Write(m_iBirthmark);

	pStream->Write(m_eUnitAIType);
	pStream->Write(m_iAutomatedAbortTurn);
	REPRO_TEST_END_WRITE();
}

// advc:
CvUnitAI* CvUnitAI::fromIDInfo(IDInfo id)
{
	return AI_getUnit(id);
}
