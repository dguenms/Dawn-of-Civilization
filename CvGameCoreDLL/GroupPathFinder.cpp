#include "CvGameCoreDLL.h"
#include "GroupPathFinder.h"
#include "CvSelectionGroupAI.h"
#include "CvUnit.h"
#include "CoreAI.h"
#include "CvInfo_Terrain.h"
#include "FAStarNode.h" // for linking updatePathData

// advc.pf: New implementation file; see comment in header.


bool GroupStepMetric::canReuseInitialPathData(GroupPathNode const& kStart) const
{
	/*	K-Mod (note): This condition isn't actually enough to catch all
		significant changes. We really need to check max moves _and_ moves left
		_and_ base moves. but I don't feel like doing all that at the moment.
		^advc: I don't think max moves _and_ base moves need to be checked(?),
		but, in order to check, max moves will have to be stored in GroupPathNode.
		Or units will have to call invalidateGroup on CvSelectionGroup::m_pPathFinder
		when their base moves change. Either way, this will take a bit of work. */
	return (initialMoves(*m_pGroup, m_eFlags) == kStart.getMoves());
}

// "pathValid_join" in K-Mod
bool GroupStepMetric::isValidStep(CvPlot const& kFrom, CvPlot const& kTo,
	CvSelectionGroup const& kGroup, MovementFlags eFlags)
{
	return (kGroup.getDomainType() != DOMAIN_SEA ||
			!GC.getMap().isSeparatedByIsthmus(kFrom, kTo) ||
			kGroup.canMoveAllTerrain());
}

// "pathValid_source" in K-Mod
bool GroupStepMetric::canStepThrough(CvPlot const& kPlot, CvSelectionGroup const& kGroup,
	MovementFlags eFlags)
{
	//PROFILE_FUNC(); // advc.003o

	if (kGroup.atPlot(&kPlot))
		return true;

	if (eFlags & MOVE_SAFE_TERRITORY)
	{
		if (kPlot.isOwned() && kPlot.getTeam() != kGroup.getHeadTeam())
			return false;

		if (!kPlot.isRevealed(kGroup.getHeadTeam()))
			return false;
	}

	if ((eFlags & MOVE_NO_ENEMY_TERRITORY) && kPlot.isOwned() &&
		GET_TEAM(kPlot.getTeam()).isAtWar(kGroup.getHeadTeam()))
	{
		return false;
	}

	/*	(advc.pf: Danger checks based on path data moved into a
		separate function) */

	if (kGroup.isAIControlled() || kPlot.isRevealed(kGroup.getHeadTeam()))
	{
		if (eFlags & (MOVE_THROUGH_ENEMY /* K-Mod: */ | MOVE_ATTACK_STACK))
		{
			if (!kGroup.canMoveOrAttackInto(kPlot,
				(eFlags & MOVE_DECLARE_WAR) && !kGroup.isHuman())) // K-Mod
			{
				return false;
			}
		}
		else if (!kGroup.canMoveThrough(kPlot,
			// K-Mod
			(eFlags & MOVE_DECLARE_WAR) && !kGroup.isHuman(),
			(eFlags & MOVE_ASSUME_VISIBLE) || !kGroup.isHuman()))
			// K-Mod end
		{
			return false;
		}
	}
	/*	K-Mod. Note: it's currently difficult to extract the
		vision-cheating part of this AI, because the AI needs to cheat
		inside canMoveOrAttackInto for its other cheating parts to work...
		.. anyway, here is the beginnings of what the code
		might look like without the cheats. (it's unfinished) */
	/*if (kPlot.isRevealed(kGroup.getHeadTeam(), false))
	{
		PROFILE("pathValid move through");
		CvTeamAI& kTeam = GET_TEAM(kGroup.getHeadTeam());
		int iEnemyDefence;
		if (kPlot.isVisible(kGroup.getHeadTeam(), false))
		{
			iEnemyDefence = GET_PLAYER(kGroup.getOwner()).
					AI_localDefenceStrength(pToPlot, NO_TEAM,
					kGroup.getDomainType(), 0, true, false, kGroup.isHuman());
		}
		else iEnemyDefence = kTeam.AI_getStrengthMemory(&kPlot);

		if (kTeam.AI_getStrengthMemory(&kPlot) > 0 &&
			(eFlags & (MOVE_THROUGH_ENEMY | MOVE_ATTACK_STACK)))
		{
			if (!kGroup.canMoveOrAttackInto(kPlot) ||
				((eFlags & MOVE_ATTACK_STACK) &&
				kGroup.AI_sumStrength(&kPlot) < iEnemyDefence))
			{
				return false;
			}
		}
		else if (!kGroup.canMoveThrough(kPlot))
			return false;
	}*/

	return true;
}

/*	advc.pf: Cut from pathValid_source. Given how the pathfinder uses that function
	(that is: to close off plots entirely after visiting from only one neighbor),
	it mustn't take into account path data. Doing so had lead to rare pathfinding
	failures in K-Mod. */
bool GroupStepMetric::canStepThrough(CvPlot const& kPlot, CvSelectionGroup const& kGroup,
	MovementFlags eFlags, int iMoves, int iPathTurns)
{
	if ((iPathTurns > 1 || iMoves == 0) &&
		kGroup.isAIControlled() &&
		!(eFlags & MOVE_IGNORE_DANGER) &&
		(!kGroup.canFight() || /* advc.031d: */ (eFlags & MOVE_AVOID_DANGER)) &&
		!kGroup.alwaysInvisible() &&
		GET_PLAYER(kGroup.getHeadOwner()).AI_isAnyPlotDanger(kPlot))
	{
		return false;
	}
	return true;
}

// "pathDestValid" in BtS/ K-Mod
bool GroupStepMetric::isValidDest(CvPlot const& kPlot, CvSelectionGroup const& kGroup,
	MovementFlags eFlags)
{
	PROFILE_FUNC();

	if (kGroup.at(kPlot))
		return true;

	DomainTypes const eDomain = kGroup.getDomainType();
	if (eDomain == DOMAIN_IMMOBILE)
		return false;

	bool const bAIControl = kGroup.isAIControlled();

	if (bAIControl)
	{	/*  BETTER_BTS_AI_MOD, Efficiency, 11/04/09, jdog5000: START
			switch order as AI_isAnyPlotDanger is more expensive */
		if (eDomain == DOMAIN_LAND)
		{
			CvArea const& kGroupArea = *kGroup.area();
			if (!kPlot.isArea(kGroupArea) &&
				!kGroup.canMoveAllTerrain() &&
				!kPlot.isAdjacentToArea(kGroupArea))
			{
				return false;
			}
		}
		if (!(eFlags & MOVE_IGNORE_DANGER) &&
			(!kGroup.canFight() ||
			(eFlags & MOVE_AVOID_DANGER)) && // advc.031d
			!kGroup.alwaysInvisible() &&
			GET_PLAYER(kGroup.getHeadOwner()).AI_isAnyPlotDanger(kPlot))
		{
			return false;
		}
		// BETTER_BTS_AI_MOD: END
	}

	if (bAIControl || kPlot.isRevealed(kGroup.getHeadTeam()))
	{
		if (kGroup.isAmphibPlot(&kPlot))
		{
			/*	advc.opt: Might be faster to go through kGroup.getPlot() directly
				but only once (as in CvSelectionGroup::canCargoAllMove).
				However, the profiler suggests that this branch executes quite rarely. */
			PROFILE("GroupStepMetric::isValidDest - AmphibPlot");
			FOR_EACH_UNIT_IN(pTransport, kGroup)
			{
				if (!pTransport->hasCargo() ||
					pTransport->domainCargo() != DOMAIN_LAND)
				{
					continue;
				}
				bool bValid = false;
				FOR_EACH_UNIT_IN(pCargoUnit, pTransport->getPlot())
				{
					if (pCargoUnit->getTransportUnit() == pTransport &&
						pCargoUnit->isGroupHead() &&
						pCargoUnit->getGroup()->canMoveOrAttackInto(kPlot,
						//(kGroup.AI().AI_isDeclareWar(kPlot) || (eFlags & MOVE_DECLARE_WAR)))
						// K-Mod. The new AI must be explicit about declaring war.
						eFlags & MOVE_DECLARE_WAR, false, //bAIControl
						!kGroup.isHuman())) // advc.001 (see below)
					{
						bValid = true;
						break;
					}
				}
				if (bValid)
					return true;
			}

			return false;
		}
		else
		{
			if (!kGroup.canMoveOrAttackInto(kPlot,
				//pSelectionGroup->AI_isDeclareWar(pToPlot) || (eFlags & MOVE_DECLARE_WAR))
				// K-Mod. The new AI must be explicit about declaring war.
				eFlags & MOVE_DECLARE_WAR, false, //bAIControl
				// advc.001: Automated human units shouldn't be all-seeing
				!kGroup.isHuman()))
			{
				return false;
			}
		}
	}

	return true;
}

/*	advc.pf: I've mainly wanted to increase PATH_STEP_WEIGHT.
	Symmetry breaking and PATH_STRAIGHT_WEIGHT can add up to a total of 6 per step.
	STEP_WEIGHT 7 still isn't always enough to trump that,
	so I'm adding 1 more later on for human units.
	Don't want to scale everything up too much, i.e. not too close to 1024.
	(Though I guess one could just increase PATH_MOVEMENT_WEIGHT as well, e.g. to 2048.) */

//#define PATH_MOVEMENT_WEIGHT    (1024) // advc: moved to the header (for inline function)
// advc.pf: Was 20 in K-Mod, 100 in BtS.
#define PATH_RIVER_WEIGHT	(32) // river crossing penalty
// advc.pf: Was 200 in K-Mod, 100 in BtS.
#define PATH_CITY_WEIGHT			(225) // K-Mod
// advc.pf: Was 4 in K-Mod, 10 in BtS.
#define PATH_DEFENSE_WEIGHT			(7) // defence bonus
// advc.pf: Was 5 in K-Mod, 3 in BtS.
#define PATH_TERRITORY_WEIGHT		(9)
#define PATH_DOW_WEIGHT				(7) // advc.082
// advc.pf: Was 4 in K-Mod, 2 in BtS.
#define PATH_STEP_WEIGHT			(7)
#define PATH_STRAIGHT_WEIGHT		(2) // K-Mod: was 1
#define PATH_NOROUTE_WEIGHT			(2) // advc.pf
//#define PATH_ASYMMETRY_WEIGHT		(1) // K-Mod

// #define PATH_DAMAGE_WEIGHT      (500) // K-Mod (gets loaded from XML)
// advc.pf: Was 300 in K-Mod
#define PATH_COMBAT_WEIGHT         (350) // K-Mod. penalty for having to fight along the way.
// Note: there will also be other combat penalties added, for example from defence weight and city weight.

// "pathCost" in BtS/ K-Mod
/*	This function has been completely rewritten for K-Mod.
	(the rewrite includes some bug fixes as well as some new features) */
int GroupStepMetric::cost(CvPlot const& kFrom, CvPlot const& kTo,
	CvSelectionGroup const& kGroup, MovementFlags eFlags,
	int iCurrMoves, // (advc: Moves left when at kFrom)
	bool bAtStart) // (advc: True if kFrom is the start of the path)
{
	//PROFILE_FUNC(); // advc.003o

	TeamTypes const eTeam = kGroup.getHeadTeam();
	// <advc.035>
	int const iFlipModifierDiv = 7;
	int iFlipModifier = iFlipModifierDiv;
	// </advc.035>
	// K-Mod
	int iExploreModifier = 3; // (in thirds)
	if (!kTo.isRevealed(eTeam))
	{
		if (kGroup.getAutomateType() == AUTOMATE_EXPLORE ||
			(!kGroup.isHuman() &&
			(kGroup.getHeadUnitAIType() == UNITAI_EXPLORE ||
			kGroup.getHeadUnitAIType() == UNITAI_EXPLORE_SEA)))
		{
			// lower cost to encourage exploring unrevealed areas
			iExploreModifier = 2;
		}
		else if (!kFrom.isRevealed(eTeam))
		{
			// higher cost to discourage pathfinding deep into the unknown
			iExploreModifier = 4;
		}
	}
	// K-Mod end
	// <advc.035>
	else if (GC.getDefineBOOL(CvGlobals::OWN_EXCLUSIVE_RADIUS) &&
		(eFlags & MOVE_DECLARE_WAR) && eTeam != BARBARIAN_TEAM)
	{
		PlayerTypes const eSecondOwner = kTo.getSecondOwner();
		PlayerTypes const eFirstOwner = kTo.getOwner();
		if (eSecondOwner != NO_PLAYER && eFirstOwner != NO_PLAYER &&
			((kGroup.getDomainType() == DOMAIN_SEA) == kTo.isWater()))
		{	// Avoid tiles that flip from us to the enemy upon DoW
			if (TEAMID(eFirstOwner) == eTeam && (GET_TEAM(eTeam).isHuman() ?
				(!GET_TEAM(eTeam).isFriendlyTerritory(TEAMID(eSecondOwner)) &&
				!GET_TEAM(eTeam).isAtWar(TEAMID(eSecondOwner))) :
				GET_TEAM(eTeam).AI_isSneakAttackReady(TEAMID(eSecondOwner))))
			{
				iFlipModifier++;
			}
			// Seek out enemy tiles that will flip to us upon DoW
			if (TEAMID(eSecondOwner) == eTeam && (GET_TEAM(eTeam).isHuman() ?
				(!GET_TEAM(eTeam).isFriendlyTerritory(TEAMID(eFirstOwner)) &&
				!GET_TEAM(eTeam).isAtWar(TEAMID(eFirstOwner))) :
				GET_TEAM(eTeam).AI_isSneakAttackReady(TEAMID(eFirstOwner))))
			{
				iFlipModifier--;
			}
			/*  This could be done much more accurately, taking into account
				vassal agreements, defensive pacts, and going through the entire
				selection group, but I worry about the performance, and it's OK
				if it doesn't always work correctly. */
		}
	} // </advc.035>
	int iWorstCost = 0;
	int iWorstMovesLeft = MAX_INT;
	//int iWorstMaxMoves = MAX_INT; // advc: unused
	FOR_EACH_UNIT_IN(pGroupUnit, kGroup)
	{
		FAssert(pGroupUnit->getDomainType() != DOMAIN_AIR);
		int const iMaxMoves = (iCurrMoves > 0 ? iCurrMoves : pGroupUnit->maxMoves());
		int const iMoveCost = kTo.movementCost(*pGroupUnit, kFrom,
				false); // advc.001i
		int const iMovesLeft = std::max(0, iMaxMoves - iMoveCost);

		iWorstMovesLeft = std::min(iWorstMovesLeft, iMovesLeft);
		//iWorstMaxMoves = std::min(iWorstMaxMoves, iMaxMoves);

		int iCost = PATH_MOVEMENT_WEIGHT * (iMovesLeft == 0 ? iMaxMoves : iMoveCost);
		iCost = (iCost * iExploreModifier) / 3;
		iCost = (iCost * iFlipModifier) / iFlipModifierDiv; // advc.035
		if (iCost > iWorstCost)
		{
			iWorstCost = iCost;
			iWorstMovesLeft = iMovesLeft;
			//iWorstMaxMoves = iMaxMoves;
		}
	}
	iWorstCost += PATH_STEP_WEIGHT;

	/*	symmetry breaking. This is meant to prevent two paths from having equal cost.
		(If two paths have equal cost, sometimes the interface shows one path
		and the units follow the other. This is bad.) */
	/* original K-Mod symmetry breaking. (extra cost for turning a corner)
	if (parent->m_pParent)
	{
		const int map_width = GC.getMap().getGridWidth();
		const int map_height = GC.getMap().getGridHeight();
		#define WRAP_X(x) ((x) - ((x) > map_width/2 ? map_width : 0) + ((x) < -map_width/2 ? map_width : 0))
		#define WRAP_Y(y) ((y) - ((y) > map_height/2 ? map_height : 0) + ((y) < -map_height/2 ? map_height : 0))
		int start_x = parent->m_pParent->m_iX;
		int start_y = parent->m_pParent->m_iY;
		int dx1 = WRAP_X(pFromPlot->getX() - start_x);
		int dy1 = WRAP_Y(pFromPlot->getY() - start_y);
		int dx2 = WRAP_X(pToPlot->getX() - start_x);
		int dy2 = WRAP_Y(pToPlot->getY() - start_y);
		// cross product. (greater than zero => sin(angle) > 0 => angle > 0)
		int cross = dx1 * dy2 - dx2 * dy1;
		if (cross > 0)
			iWorstCost += PATH_ASYMMETRY_WEIGHT; // turning left
		else if (cross < 0)
			iWorstCost -= PATH_ASYMMETRY_WEIGHT; // turning right
		// woah - hang on. Does that say /minus/ asym weight?
		// Doesn't this guy know that bad things happen if the total weight is negative?
		// ...
		// take a breath.*/
		//#if PATH_STEP_WEIGHT < PATH_ASYMMETRY_WEIGHT
		//#error "I'm sorry, but I must demand that step weight be greater than asym weight."
		//#endif  // I think we're going to be ok.
		//#undef WRAP_X
		//#undef WRAP_Y
	//}
	/*	Unfortunately, the above code is not sufficient to fix the symmetry problem.
		Here's a new method, which combines symmetry breaking
		with the old "straight path" effect.
		Note: symmetry breaking is not important for AI controlled units. */

	/*	It's actually marginally better strategy to move diagonally - for mapping reasons.
		So let the AI prefer diagonal movement.
		However, diagonal zig-zags will probably seem unnatural and weird to humans
		who are just trying to move in a straight line.
		So let the pathfinding for human groups prefer cardinal movement. */
	bool const bAIControl = kGroup.isAIControlled();
	/*	advc.pf: AI map visibility is generally unimportant and a relatively
		high weight makes it harder to give routes the proper weight (see below). */
	if (/*bAIControl*/ iExploreModifier < 3)
	{
		if (kFrom.getX() == kTo.getX() || kFrom.getY() == kTo.getY())
			iWorstCost += PATH_STRAIGHT_WEIGHT;
	}
	else
	{
		if (kFrom.getX() != kTo.getX() && kFrom.getY() != kTo.getY())
		{
			iWorstCost += PATH_STRAIGHT_WEIGHT *
					(1 + ((kTo.getX() + kTo.getY()) % 2));
		}
		iWorstCost += (kTo.getX() + kTo.getY() + 1) % 3;
		/*	advc.pf: Essentially 1 extra step weight for humans
			(and now also for non-exploring AI) */
		iWorstCost++;
	}
	/*	unfortunately, this simple method may have problems at the world-wrap boundaries.
		It's difficult to tell when to correct for wrap effects and when not to,
		because as soon as the unit starts moving, the start position of the path changes,
		and so it's no longer possible to tell whether or not the unit started
		on the other side of the boundary. Drat. */

	/*	<advc.pf> A route at kTo may or may not have decreased our movementCost;
		either way, it'll likely help on subsequent turns. Preferring routes should
		also help the pathfinder process the nodes in an order that is efficient and
		safe (see comment about "dead end" nodes in KmodPathFinder::processChild).*/
	if (kTo.getRevealedRouteType(eTeam) == NO_ROUTE)
		iWorstCost += PATH_NOROUTE_WEIGHT; // </advc.pf>
	// end symmetry breaking.

	if (!kTo.isRevealed(eTeam))
		return iWorstCost;

	// the cost of battle...
	if (eFlags & MOVE_ATTACK_STACK)
	{
		FAssert(bAIControl); // only the AI uses MOVE_ATTACK_STACK
		FAssert(kGroup.getDomainType() == DOMAIN_LAND);

		int iEnemyDefence = 0;

		if (kTo.isVisible(eTeam))
		{	/*  <advc.001> In the rare case that the AI plans war while animals
				still roam the map, the DefenceStrength computation will crash
				when it gets to the point where the UnitCombatType is accessed.
				(Actually, not so exotic b/c advc.300 allows animals to survive
				in continents w/o civ cities.) */
			CvUnit* pUnit = kTo.headUnit();
			if (pUnit != NULL && !pUnit->isAnimal()) // </advc.001>
			{
				iEnemyDefence = GET_PLAYER(kGroup.getOwner()).
						AI_localDefenceStrength(&kTo, NO_TEAM,
						kGroup.getDomainType(), 0, true, false,
						kGroup.isHuman());
			}
		}
		else
		{	// plot not visible. use memory
			iEnemyDefence = GET_TEAM(eTeam).AI_strengthMemory().get(kTo.plotNum());
		}

		if (iEnemyDefence > 0)
		{
			iWorstCost += PATH_COMBAT_WEIGHT;
			int iAttackRatio = std::max(10,
					100 * kGroup.AI().AI_sumStrength(&kTo) / iEnemyDefence);
			/*	Note. I half intend to have pathValid return false whenever the
				above ratio is less than 100. I just haven't done that yet,
				mostly because I'm worried about performance. */
			if (iAttackRatio < 400)
			{
				iWorstCost += PATH_MOVEMENT_WEIGHT * GC.getMOVE_DENOMINATOR() *
						(400-iAttackRatio) / std::min(150, iAttackRatio);
			}
			// else, don't worry about it too much.
		}
	} //

	// <advc.082>
	TeamTypes eToPlotTeam = kTo.getTeam();
	/*  The AVOID_ENEMY code in the no-moves-left branch below doesn't stop the AI
		from trying to move _through_ enemy territory and thus declaring war
		earlier than necessary */
	if (bAIControl && (eFlags & MOVE_DECLARE_WAR) && eToPlotTeam != NO_TEAM &&
		eToPlotTeam != eTeam && GET_TEAM(eTeam).AI_isSneakAttackReady(eToPlotTeam))
	{
		iWorstCost += PATH_DOW_WEIGHT;
	} // </advc.082>
	if (iWorstMovesLeft <= 0)
	{
		if (eToPlotTeam != eTeam)
			iWorstCost += PATH_TERRITORY_WEIGHT;

		// Damage caused by features (for mods)
		if (GC.getDefineINT(CvGlobals::PATH_DAMAGE_WEIGHT) != 0)
		{
			if (kTo.isFeature())
			{
				iWorstCost += (GC.getDefineINT(CvGlobals::PATH_DAMAGE_WEIGHT) *
						std::max(0, GC.getInfo(kTo.getFeatureType()).getTurnDamage())) /
						GC.getMAX_HIT_POINTS();
			}
			if (GC.getMap().getPlotExtraCost(kTo) > 0)
				iWorstCost += (PATH_MOVEMENT_WEIGHT * GC.getMap().getPlotExtraCost(kTo));
		}

		// defence modifiers
		int iDefenceMod = 0;
		int iDefenceCount = 0;
		int iFromDefenceMod = 0; // defence bonus for our attacking units left behind
		int iAttackWeight = 0;
		int iAttackCount = 0;
		int const iEnemies = kTo.getNumVisibleEnemyDefenders(kGroup.getHeadUnit());

		FOR_EACH_UNIT_IN(pGroupUnit, kGroup)
		{
			if (!pGroupUnit->canFight())
				continue;
			iDefenceCount++;
			if (pGroupUnit->canDefend(&kTo))
			{
				iDefenceMod += pGroupUnit->noDefensiveBonus() ? 0 :
						//pToPlot->defenseModifier(eTeam, false);
						GET_TEAM(eTeam).AI_plotDefense(kTo); // advc.012
			}
			else iDefenceMod -= 100; // we don't want to be here.

			// K-Mod note. the above code doesn't count all defensive bonuses, unfortunately.
			// We could count everything like this:
			/*CombatDetails combat_details;
			pLoopUnit->maxCombatStr(pToPlot, NULL, &combat_details);
			iDefenceMod += combat_details.iModifierTotal;*/
			// but that seems like overkill. I'm worried it would be too slow.

			// defence for units who stay behind after attacking an enemy.
			if (iEnemies > 0)
			{
				/*	For human-controlled units, only apply the following effects
					for multi-step moves. (otherwise this might prevent the user
					from attacking from where they want to attack from.) */
				if (bAIControl || !bAtStart || (eFlags & MOVE_HAS_STEPPED))
				{
					iAttackCount++;
					if (!pGroupUnit->noDefensiveBonus())
						iFromDefenceMod += kFrom.defenseModifier(eTeam, false);

					if (!kFrom.isCity())
					{
						iAttackWeight += PATH_CITY_WEIGHT;
						/*	it's done this way around rather than subtracting when in a city
							so that the overall adjustment can't be negative. */
					}
					if (pGroupUnit->canAttack() && !pGroupUnit->isRiver() &&
						kFrom.isRiverCrossing(directionXY(kFrom, kTo)))
					{
						iAttackWeight -= PATH_RIVER_WEIGHT *
								// Note, river modifier will be negative.
								GC.getDefineINT(CvGlobals::RIVER_ATTACK_MODIFIER);
						//iAttackMod -= (PATH_MOVEMENT_WEIGHT * iMovesLeft);
					}
				}
				/*	If this is a direct attack move from a human player,
					make sure it is the best value move possible.
					(This allows humans to choose which plot they attack from.)
					(note: humans have no way of ordering units to attack units en-route,
					so the fact that this is an attack move means we are at the destination.) */
				else if (pGroupUnit->canAttack()) // iKnownCost == 0 && !(eFlags & MOVE_HAS_STEPPED) && !bAIControl
					return PATH_STEP_WEIGHT; // DONE!
			}
		}
		//
		if (iAttackCount > 0)
		{
			// scale attack weights down if not all our units will need to fight.
			iAttackWeight *= std::min(iAttackCount, iEnemies);
			iAttackWeight /= iAttackCount;
			iFromDefenceMod *= std::min(iAttackCount, iEnemies);
			iFromDefenceMod /= iAttackCount;
			iAttackCount = std::min(iAttackCount, iEnemies);
		}
		//
		iWorstCost += PATH_DEFENSE_WEIGHT * std::max(0,
				(iDefenceCount * 200 - iDefenceMod) / std::max(1, iDefenceCount));
		iWorstCost += PATH_DEFENSE_WEIGHT * std::max(0,
				(iAttackCount * 200 - iFromDefenceMod) / std::max(1, iAttackCount));
		iWorstCost += std::max(0, iAttackWeight) / std::max(1, iAttackCount);
		/*	if we're in enemy territory, consider
			the sum of our defensive bonuses as well as the average */
		if (kTo.isOwned() && atWar(eToPlotTeam, eTeam))
		{
			iWorstCost += PATH_DEFENSE_WEIGHT * std::max(0,
					(iDefenceCount * 200 - iDefenceMod) / 5);
			iWorstCost += PATH_DEFENSE_WEIGHT * std::max(0,
					(iAttackCount * 200 - iFromDefenceMod) / 5);
			iWorstCost += std::max(0, iAttackWeight) / 5;
		}

		// additional cost for ending turn in or adjacent to enemy territory based on flags (based on BBAI)
		if (eFlags & (MOVE_AVOID_ENEMY_WEIGHT_2 | MOVE_AVOID_ENEMY_WEIGHT_3))
		{
			if (kTo.isOwned() && GET_TEAM(eTeam).AI_getWarPlan(eToPlotTeam) != NO_WARPLAN)
				iWorstCost *= ((eFlags & MOVE_AVOID_ENEMY_WEIGHT_3) ? 3 : 2);
			else
			{
				FOR_EACH_ADJ_PLOT(kTo)
				{
					if (pAdj->isOwned() &&
						GET_TEAM(pAdj->getTeam()).isAtWar(kGroup.getHeadTeam()))
					{
						if (eFlags & MOVE_AVOID_ENEMY_WEIGHT_3)
						{
							iWorstCost *= 3;
							iWorstCost /= 2;
						}
						else
						{
							iWorstCost *= 4;
							iWorstCost /= 3;
						}
					}
				}
			}
		}
	}

	FAssert(iWorstCost > 0);

	return iWorstCost;
}

// Part of "branchAdd" in BtS/ K-Mod
int GroupStepMetric::initialMoves(CvSelectionGroup const& kGroup, MovementFlags eFlags)
{
	FAssert(kGroup.getNumUnits() > 0);
	// K-Mod: Moved into separate functions
	return ((eFlags & MOVE_MAX_MOVES) ? kGroup.maxMoves() : kGroup.movesLeft());
}

// "pathAdd" in BtS/ K-Mod
template<class Node>
bool GroupStepMetric::updatePathData(Node& kNode, Node const& kParent,
	CvSelectionGroup const& kGroup, MovementFlags eFlags)
{
	//PROFILE_FUNC(); // advc.003o
	FAssert(kGroup.getNumUnits() > 0);

	int iPathTurns = kParent.getPathTurns();
	int iMoves = MAX_INT;
	{
		CvPlot const& kFrom = kParent.getPlot();
		CvPlot const& kTo = kNode.getPlot();
		/*if (iStartMoves == 0)
			iPathTurns++;
		for (CLLNode<IDInfo>* pUnitNode = kGroup.headUnitNode(); pUnitNode != NULL;
				pUnitNode = kGroup.nextUnitNode(pUnitNode)) {
			CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
			int iUnitMoves = (iStartMoves == 0 ? pLoopUnit->maxMoves() : iStartMoves);
			iUnitMoves -= kTo.movementCost(pLoopUnit, &kFrom);
			iUnitMoves = std::max(iUnitMoves, 0);
			iMoves = std::min(iMoves, iUnitMoves);
		}*/ // BtS
		/*	K-Mod. The original code would give incorrect results for groups
			where one unit had more moves but also had higher move cost.
			(the most obvious example is when a group with 1-move units and 2-move units
			is moving on a railroad. - In this situation, the original code would consistently
			underestimate the remaining moves at every step.) */
		int iParentMoves = kParent.getMoves();
		{
			bool bNewTurn = (iParentMoves == 0);
			if (bNewTurn)
			{
				iPathTurns++;
				iParentMoves = kGroup.maxMoves();
			}
		}
		CLLNode<IDInfo> const* pUnitNode = kGroup.headUnitNode();
		int iMoveCost = kTo.movementCost(*::getUnit(pUnitNode->m_data), kFrom,
				false); // advc.001i
		bool bUniformCost = true;
		for (pUnitNode = kGroup.nextUnitNode(pUnitNode);
			bUniformCost && pUnitNode != NULL; pUnitNode = kGroup.nextUnitNode(pUnitNode))
		{
			CvUnit const* pLoopUnit = ::getUnit(pUnitNode->m_data);
			int iLoopCost = kTo.movementCost(*pLoopUnit, kFrom,
					false); // advc.001i
			if (iLoopCost != iMoveCost)
				bUniformCost = false;
		}
		if (bUniformCost)
		{
			// the simple, normal case
			iMoves = std::max(0, iParentMoves - iMoveCost);
		}
		else
		{
			//PROFILE("pathAdd - non-uniform cost"); // advc.003o
			/*	Move costs are uneven for units in this group.
				To be sure of the true movement cost for the group,
				we need to calculate the movement cost for each unit
				for every step in this turn. */
			std::vector<CvPlot const*> plotList; // will be traversed in reverse order
			plotList.push_back(&kTo);
			plotList.push_back(&kFrom);
			Node const* pStartNode = &kParent;
			while (pStartNode->getPathTurns() == iPathTurns &&
				pStartNode->m_pParent != NULL)
			{
				pStartNode = pStartNode->m_pParent;
				plotList.push_back(&pStartNode->getPlot());
			}
			iMoves = MAX_INT;
			bool const bMaxMoves = (pStartNode->getMoves() == 0 || (eFlags & MOVE_MAX_MOVES));
			for (pUnitNode = kGroup.headUnitNode(); pUnitNode != NULL;
				pUnitNode = kGroup.nextUnitNode(pUnitNode))
			{
				CvUnit const* pLoopUnit = ::getUnit(pUnitNode->m_data);
				int iUnitMoves = (bMaxMoves ? pLoopUnit->maxMoves() : pLoopUnit->movesLeft());
				for (size_t i = plotList.size() - 1; i > 0; i--)
				{
					iUnitMoves -= plotList[i-1]->movementCost(*pLoopUnit, *plotList[i],
							false); // advc.001i
					FAssert(iUnitMoves > 0 || i == 1);
				}
				iUnitMoves = std::max(iUnitMoves, 0);
				iMoves = std::min(iMoves, iUnitMoves);
			}
		}
		// K-Mod end
	}
	FAssertBounds(0, MAX_INT, iMoves);
	if (kNode.getMoves() != iMoves || kNode.getPathTurns() != iPathTurns)
	{
		kNode.setMoves(iMoves);
		kNode.setPathTurns(iPathTurns);
		return true;
	}
	return false;
}
// explicit instantiation:
template bool GroupStepMetric::updatePathData<FAStarNode>(FAStarNode&, FAStarNode const&,
		CvSelectionGroup const&, MovementFlags);


void GroupPathFinder::setGroup(CvSelectionGroup const& kGroup,
	MovementFlags eFlags, int iMaxPath, int iHeuristicWeight)
{	// <advc.test>
	#if VERIFY_PATHF
	kLegacyPathf.SetSettings(&kGroup, eFlags, iMaxPath, iHeuristicWeight);
	#endif //</advc.test>
	CvSelectionGroup const* pOldGroup = m_stepMetric.getGroup();
	if (pOldGroup != &kGroup)
		reset();
	else
	{
		/*	some flags are not relevant to pathfinder.
			We should try to strip those out to avoid unnecessary resets. */
		MovementFlags eRelevantFlags =  // any bar these:
				~(MOVE_DIRECT_ATTACK | MOVE_SINGLE_ATTACK | MOVE_NO_ATTACK);
		if ((m_stepMetric.getFlags() & eRelevantFlags) != (eFlags & eRelevantFlags))
		{
			// there's one more chance to avoid a reset..
			/*	If the war flag is the only difference, and we aren't sneakattack-ready anyway
				- then there is effectively no difference. */
			eRelevantFlags &= ~MOVE_DECLARE_WAR;
			if ((m_stepMetric.getFlags() & eRelevantFlags) != (eFlags & eRelevantFlags) ||
				GET_TEAM(pOldGroup->getHeadTeam()).AI_isSneakAttackReady())
			{
				reset();
			}
		}
	}
	if (iHeuristicWeight < 0)
	{
		if (kGroup.getDomainType() == DOMAIN_SEA)
		{
			/*	This assumes that there are no water routes,
				no promotions that reduce water movement cost. */
			iHeuristicWeight = GC.getMOVE_DENOMINATOR();
		}
		else iHeuristicWeight = minimumStepCost(kGroup.baseMoves());
	}
	// advc: Use implicitly declared copy assignment operator
	m_stepMetric = GroupStepMetric(&kGroup, eFlags, iMaxPath, iHeuristicWeight);
}

/*	advc: To make sure we don't end up with a dangling pointer.
	Seems highly unlikely that such a pointer would clash with the group
	passed in the next setGroup call, but better not to take that chance.
	(That said, I'm only going to call this function on
	CvSelectionGroup::m_pPathFinder, so things may still not be perfectly safe.
	The metric could store IDInfo about the group; that would prevent going
	OOS when a clash does occur, but I worry that group ids would be
	more likely to clash than pointers.) */
void GroupPathFinder::invalidateGroup(CvSelectionGroup const& kGroup)
{
	if (m_stepMetric.getGroup() == &kGroup)
	{
		PROFILE("GroupPathFinder::invalidateGroup - resetNodes");
		reset();
		m_stepMetric = GroupStepMetric();
		// <advc.test>
		#if VERIFY_PATHF
		kLegacyPathf.SetSettings(NULL, NO_MOVEMENT_FLAGS, -1, -1);
		#endif // </advc.test>
	}
}


bool GroupPathFinder::generatePath(CvPlot const& kTo)
{
	FAssertMsg(m_stepMetric.getGroup() != NULL, "Must call SetSettings before GeneratePath");
	return generatePath(m_stepMetric.getGroup()->getPlot(), kTo);
}


CvPlot& GroupPathFinder::getPathEndTurnPlot() const
{
	GroupPathNode* pNode = m_pEndNode;
	FAssert(pNode->getPathLength() == 1 || pNode->m_pParent != NULL);
	while (pNode != NULL && pNode->getPathLength() > 1)
	{
		pNode = pNode->m_pParent;
	}
	FAssert(pNode != NULL);
	#if VERIFY_PATHF == 0 // advc.test
	return pNode->getPlot();
	// <advc.test>
	#else
	CvPlot& kEndTurnPlot = pNode->getPlot();
	FAssert(&kEndTurnPlot == kLegacyPathf.GetPathEndTurnPlot());
	return kEndTurnPlot;
	#endif // </advc.test>
}

// <advc.test>
#if VERIFY_PATHF
bool GroupPathFinder::generatePath(CvPlot const& kFrom, CvPlot const& kTo)
{
	bool bSuccess = KmodPathFinder<GroupStepMetric,GroupPathNode>::generatePath(kFrom, kTo);
	FAssert(bSuccess == kLegacyPathf.GeneratePath(
			kFrom.getX(), kFrom.getY(), kTo.getX(), kTo.getY()));
	return bSuccess;
}
#endif // </advc.test>
