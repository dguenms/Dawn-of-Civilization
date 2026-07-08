#include "CvGameCoreDLL.h"
#include "CvSelectionGroup.h"
#include "CvSelectionGroupAI.h"
#include "GroupPathFinder.h"
#include "PlotRadiusIterator.h"
#include "CvUnitAI.h"
#include "CvPlayerAI.h"
#include "CvGamePlay.h"
#include "CvCity.h"
#include "BBAILog.h"
#include "CvBugOptions.h" // advc.002m
#include "CvInfo_Command.h"
#include "CvInfo_Terrain.h" // for getBestBuildRoute
//#include "CvInfo_Unit.h" // for canAnyMoveAllTerrain (now in PCH)
#include "CySelectionGroup.h"

// K-Mod:
GroupPathFinder* CvSelectionGroup::m_pPathFinder = NULL; // advc.pf: pointer
GroupPathFinder* CvSelectionGroup::m_pAltPathFinder = NULL; // advc.opt
// <advc.pf>
void CvSelectionGroup::initPathFinder()
{
	if (m_pPathFinder != NULL)
	{
		FAssert(m_pPathFinder == NULL);
		delete m_pPathFinder;
	}
	m_pPathFinder = new GroupPathFinder();
	m_pAltPathFinder = new GroupPathFinder();
}
void CvSelectionGroup::uninitPathFinder()
{
	SAFE_DELETE(m_pPathFinder);
	SAFE_DELETE(m_pAltPathFinder);
}
/*	Restored this BtS function for callers that
	otherwise don't need the GroupPathFinder header.
	Made it static. */
void CvSelectionGroup::resetPath()
{
	//gDLL->getFAStarIFace()->ForceReset(&GC.getPathFinder());
	pathFinder().reset();
}

GroupPathFinder& CvSelectionGroup::getClearPathFinder() // advc.opt
{
	/*	(Will use this in a place where cached data could cause OOS issues.
		The point is only to avoid repeated memory allocation.) */
	m_pAltPathFinder->reset();
	return *m_pAltPathFinder;
} // </advc.pf>


CvSelectionGroup::CvSelectionGroup()
{
	m = new Data(); // advc.003k
	reset(0, NO_PLAYER, true);
}


CvSelectionGroup::~CvSelectionGroup()
{
	uninit();
	SAFE_DELETE(m); // advc.003k
}


void CvSelectionGroup::init(int iID, PlayerTypes eOwner)
{
	reset(iID, eOwner); // Reset serialized data
	AI().AI_init();
}


void CvSelectionGroup::uninit()
{
	m_units.clear();
	m->knownEnemies.clear(); // advc.004l
	m_missionQueue.clear();
}


// Initializes data members that are serialized.
void CvSelectionGroup::reset(int iID, PlayerTypes eOwner, bool bConstructorCall)
{
	uninit();

	m_iID = iID;
	m_iMissionTimer = 0;

	m_bForceUpdate = false;

	m_eOwner = eOwner;

	m_eActivityType = ACTIVITY_AWAKE;
	m->eAutomateType = NO_AUTOMATE;
	m->bInitiallyVisible = true; // advc.102
	m_bIsBusyCache = false;

	if (!bConstructorCall)
		AI().AI_reset();
}


void CvSelectionGroup::kill()
{
	FAssert(getOwner() != NO_PLAYER);
	FAssert(getID() != FFreeList::INVALID_INDEX);
	FAssert(getNumUnits() == 0);

	invalidateGroupPaths(); // advc.pf
	GET_PLAYER(getOwner()).removeGroupCycle(getID());
	GET_PLAYER(getOwner()).deleteSelectionGroup(getID());
}

// advc.pf:
void CvSelectionGroup::invalidateGroupPaths()
{
	m_pPathFinder->invalidateGroup(*this);
	m_pAltPathFinder->invalidateGroup(*this);
}


bool CvSelectionGroup::sentryAlert(/* advc.004l: */ bool bUpdateKnownEnemies)
{
	CvUnit const* pHeadUnit = NULL;
	int iMaxRange = 0;
	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		int iRange = pUnit->visibilityRange() + 1;
		if (iRange > iMaxRange)
		{
			iMaxRange = iRange;
			pHeadUnit = pUnit;
		}
	}
	if(pHeadUnit == NULL)
		return false;

	bool bAlert = false; // advc.004l
	for (SquareIter it(pHeadUnit->getPlot(), iMaxRange); it.hasNext(); ++it)
	{
		CvPlot& kPlot = *it;
		if(!pHeadUnit->getPlot().canSeePlot(
			&kPlot, pHeadUnit->getTeam(), iMaxRange - 1))
		{
			continue;
		}
		// <advc.004l>
		for (CLLNode<IDInfo> const* pNode = kPlot.headUnitNode(); pNode != NULL;
			pNode = kPlot.nextUnitNode(pNode))
		{
			CvUnit const* pLoopUnit = ::getUnit(pNode->m_data);
			if(!kPlot.isVisibleEnemyUnit(pHeadUnit, pLoopUnit))
				continue;
			if(bUpdateKnownEnemies)
			{
				bAlert = true;
				m->knownEnemies.insertAtEnd(pNode->m_data);
			}
			else
			{
				bool bKnown = false;
				// Linear search
				for(CLLNode<IDInfo>* pKnownNode = m->knownEnemies.head();
					pKnownNode != NULL; pKnownNode = m->knownEnemies.next(pKnownNode))
				{
					if(pKnownNode->m_data.eOwner == pNode->m_data.eOwner &&
						pKnownNode->m_data.iID == pNode->m_data.iID)
					{
						bKnown = true;
						break;
					}
				}
				if(!bKnown)
					return true;
			}
		}
	}
	return bAlert; // </advc.004l>
}

/*	Note: this function has had some editting and restructuring for K-Mod.
	There are some unmarked changes. */
void CvSelectionGroup::doTurn()
{
	PROFILE_FUNC();

	FAssert(getOwner() != NO_PLAYER);
	// <advc>
	if(getNumUnits() <= 0)
	{
		doDelayedDeath();
		return;
	} // </advc>

	bool const bCouldAnyMove = canAnyMove(); // advc.153: was AllMove in K-Mod
	CvUnit* pHeadUnit = getHeadUnit(); // advc
	/*	K-Mod. Wake spies when they reach max fortify turns in foreign territory.
		I'm only checking the head unit.
		Note: We only want to wake once. So this needs to be done
		before the fortify counter is increased. */
	if (isHuman() && getActivityType() == ACTIVITY_SLEEP)
	{
		if (pHeadUnit->isSpy() && pHeadUnit->getPlot().getTeam() != getTeam())
		{
			if (pHeadUnit->getFortifyTurns() ==
				GC.getDefineINT(CvGlobals::MAX_FORTIFY_TURNS) - 1)
			{
				setActivityType(ACTIVITY_AWAKE); // time to wake up!
			}
		}
	} // K-Mod end

	// do unit's turns (checking for damage)
	bool bHurt = false;
	{
		FOR_EACH_UNIT_VAR_IN(pUnit, *this)
		{
			pUnit->doTurn();
			if (pUnit->isHurt())
				bHurt = true;
		}
	}

	ActivityTypes eActivityType = getActivityType();

	/*	wake unit if skipped last turn
		or healing and automated
		or no longer hurt (automated healing is one turn at a time)
		or on sentry and there is danger */
	// <advc.004l> Also wake the unit if healing outside of a city and danger
	bool bSentryAlert = // Just for performance:
			((eActivityType == ACTIVITY_HEAL || eActivityType == ACTIVITY_SENTRY) &&
			isHuman() && sentryAlert()); // </advc.004l>
	if (eActivityType == ACTIVITY_HOLD ||
		(eActivityType == ACTIVITY_HEAL && (isAIControlled() || !bHurt ||
		(bSentryAlert && pHeadUnit->canSentryHeal(plot())) // advc.004l
		)) ||
		(eActivityType == ACTIVITY_SENTRY && bSentryAlert))
	{
		setActivityType(ACTIVITY_AWAKE);
	}

	if (isAIControlled())
	{
		if (getActivityType() != ACTIVITY_MISSION ||
			(!canFight() && GET_PLAYER(getOwner()).AI_isAnyPlotDanger(getPlot(), 2)))
		{
			setForceUpdate(true);
			// K-Mod. (This stuff use to be part force update's job. Now it isn't.)
			clearMissionQueue();
			AI().AI_cancelGroupAttack();
			// K-Mod end
		}
	}
	else
	{
		// K-Mod. (should do nothing, unless we're coming out of autoplay or something.)
		setForceUpdate(false);

		if (getActivityType() == ACTIVITY_MISSION)
		{
			bool bNonSpy = false;
			FOR_EACH_UNIT_IN(pUnit, *this)
			{
				if (!pUnit->isSpy())
				{
					bNonSpy = true;
					break;
				}
			}

			// K-Mod
			bool bBrave = (headMissionQueueNode() != NULL &&
					(headMissionQueueNode()->m_data.eFlags & MOVE_IGNORE_DANGER));
			/*	Originally I used MOVE_IGNORE_DANGER to skip the danger tests completely,
				but I've found that produces unintuitive results in some situations.
				So now MOVE_IGNORE_DANGER only ignores iRange==2. */

			//if (bNonSpy && GET_PLAYER(getOwner()).AI_getPlotDanger(plot(), 2) > 0)
			if (bNonSpy && GET_PLAYER(getOwner()).AI_isAnyPlotDanger(
				getPlot(), bBrave ? 1 : 2, true, false))
			{
				clearMissionQueue();
			} // K-Mod end
		}
	}

	if (isHuman())
	{
		if (GC.getGame().isMPOption(MPOPTION_SIMULTANEOUS_TURNS)
			&& GET_TEAM(getTeam()).hasMetHuman()) // K-Mod
		{
			int iBestWaitTurns = 0;
			FOR_EACH_UNIT_IN(pUnit, *this)
			{
				int iWaitTurns = (GC.getDefineINT("MIN_TIMER_UNIT_DOUBLE_MOVES") -
						(GC.getGame().getTurnSlice() - pUnit->getLastMoveTurn()));
				if (iWaitTurns > iBestWaitTurns)
					iBestWaitTurns = iWaitTurns;
			}
			setMissionTimer(std::max(iBestWaitTurns, getMissionTimer()));
			if (iBestWaitTurns > 0)
			{
				// Cycle selection if the current group is selected
				CvUnit* pSelectedUnit = gDLL->UI().getHeadSelectedUnit();
				if (pSelectedUnit != NULL && pSelectedUnit->getGroup() == this)
					gDLL->UI().selectGroup(pSelectedUnit, false, false, false);
			}
		}
	}
	// K-Mod
	if (!bCouldAnyMove && isCycleGroup())
		GET_PLAYER(getOwner()).updateGroupCycle(*this);
	// K-Mod end

	doDelayedDeath();
}

// advc.004l:
void CvSelectionGroup::doTurnPost()
{
	/*  In particular: If an enemy unit moves out of range and returns, it's
		no longer a known enemy. */
	m->knownEnemies.clear();
	ActivityTypes eActivity = getActivityType();
	if(eActivity == ACTIVITY_HEAL || eActivity == ACTIVITY_SENTRY)
		sentryAlert(true);
}


bool CvSelectionGroup::showMoves(/* advc.102: */ CvPlot const& kFromPlot) const
{
	if (isNeverShowMoves()) // advc: Moved into new function
		return false;
	// <advc.102>
	static bool const bShowWorkers = GC.getDefineBOOL("SHOW_FRIENDLY_WORKER_MOVES");
	static bool const bShowShips = GC.getDefineBOOL("SHOW_FRIENDLY_SEA_MOVES");
	// Also refers to Executives; those have the same Unit AI.
	static bool const bShowMissionaries = GC.getDefineBOOL("SHOW_FRIENDLY_MISSIONARY_MOVES");
	CvPlot const& kToPlot = getPlot();
	PlayerTypes const eFromOwner = kFromPlot.getOwner();
	PlayerTypes const eToOwner = kToPlot.getOwner();
	PlayerTypes const eGroupOwner = getOwner();
	DomainTypes const eGroupDomain = getDomainType();
	bool const bAwayFromHome = (eGroupOwner != eToOwner ||
			eGroupOwner != eFromOwner);
	bool const bWaterPatrol = (getDomainType() == DOMAIN_SEA &&
			AI().AI_getMissionAIType() == MISSIONAI_PATROL);
	// </advc.102>  <advc.102b>
	int const iFriendlyStackThresh = BUGOption::getValue(
			"MainInterface__ShowFriendlyMovesThresh", 0); // </advc.102b>
	for (PlayerIter<HUMAN> itHuman; itHuman.hasNext(); ++itHuman)
	{
		CvUnit const* pHeadUnit = getHeadUnit();
		if(pHeadUnit == NULL)
			continue;
		if (pHeadUnit->isEnemy(itHuman->getTeam()))
		{
			if (itHuman->isOption(PLAYEROPTION_SHOW_ENEMY_MOVES))
				return true;
			continue;
		}
		if(!itHuman->isOption(PLAYEROPTION_SHOW_FRIENDLY_MOVES))
			continue;
		// <advc.102b>
		if (iFriendlyStackThresh > 0)
		{
			int iPlotCount = 0;
			if (kToPlot.isVisible(itHuman->getTeam()))
			{
				iPlotCount += kToPlot.plotCount(
						PUF_isVisible, itHuman->getID(), -1, eGroupOwner, NO_TEAM,
						PUF_canDefend);
			}
			// Treat all but one unit as having already arrived
			if (canDefend())
				iPlotCount += getNumUnits() - 1;
			// Assume that cargo is full
			if (eGroupDomain == DOMAIN_SEA) // just to save time
				iPlotCount += getCargoSpace();
			if (iPlotCount < iFriendlyStackThresh)
				continue;
		} // </advc.102b>
		// <advc.102> Hide uninteresting friendly moves
		TeamTypes const eObs = itHuman->getTeam();
		bool const bInSpectatorsBorders = ((eFromOwner != NO_PLAYER &&
				eObs == TEAMID(eFromOwner)) || (eToOwner != NO_PLAYER &&
				eObs == TEAMID(eToOwner)));
		bool const bEnteringOrLeaving = (getPlot().isVisible(eObs) !=
				kFromPlot.isVisible(eObs));
		// Just to avoid cycling through the units
		if(bInSpectatorsBorders && (bEnteringOrLeaving || !bWaterPatrol))
			return true;
		if(bShowWorkers && bShowShips && bShowMissionaries)
			return true;
		FOR_EACH_UNIT_IN(pLoopUnit, *this)
		{
			if(pLoopUnit == NULL)
			{
				FAssert(false); // An invalid unit id while the stack is moving would be strange
				continue;
			}
			CvUnit const& u = *pLoopUnit;
			bool bSeaUnit = u.getDomainType() == DOMAIN_SEA;
			bool bCombatant = u.getUnitCombatType() != NO_UNITCOMBAT;
			if(!bSeaUnit && bCombatant && !bAwayFromHome && getPlot().getNumUnits() == 1)
				break;
			bool bWorker = (u.AI_getUnitAIType() == UNITAI_WORKER ||
					u.AI_getUnitAIType() == UNITAI_WORKER_SEA);
			bool bNonTransportShip = (bSeaUnit && !u.isHuman() &&
					(u.cargoSpace() <= 1 || bWaterPatrol));
			bool bMissionary = (u.AI_getUnitAIType() == UNITAI_MISSIONARY);
			if(!bMissionary && bAwayFromHome && (!bSeaUnit ||
				!bNonTransportShip || bShowShips || bEnteringOrLeaving))
			{
				return true;
			}
			if((bWorker && bShowWorkers) || (bNonTransportShip && bShowShips &&
				bEnteringOrLeaving) || (bMissionary && bShowMissionaries))
			{
				return true;
			}
			if(!bWorker && !bNonTransportShip && !bMissionary)
				return true;
			// </advc.102>
		}
	}
	return false;
}

// advc: Cut from showMoves
bool CvSelectionGroup::isNeverShowMoves() const
{
	return (GC.getGame().isMPOption(MPOPTION_SIMULTANEOUS_TURNS) ||
			GC.getGame().isSimultaneousTeamTurns());
}

// advc.002m:
int CvSelectionGroup::nukeMissionTime() const
{
	int const iFull = GC.getInfo(MISSION_NUKE).getTime(); // cut from startMission
	int const iShortened = iFull / 4;
	if (isNeverShowMoves())
		return iShortened / 2;
	enum NukeMissionTimeChoices
	{
		FULL, SHORTENED, ZERO // These match the BUG config in XML
	};
	int const iBUGChoice = BUGOption::getValue("MainInterface__NukeMissionTime", 0);
	if (iBUGChoice == ZERO)
		return 0;
	if (!isActiveOwned())
		return iShortened / 2;
	// Nothing to see when particle effects aren't enabled
	if (gDLL->getGraphicOption(GRAPHICOPTION_EFFECTS_DISABLED) ||
		iBUGChoice == SHORTENED)
	{
		return iShortened;
	}
	return iFull;
}

// advc.102:
void CvSelectionGroup::setInitiallyVisible(bool b)
{
	m->bInitiallyVisible = b;
}


void CvSelectionGroup::updateTimers()
{
	FAssert(getOwner() != NO_PLAYER);
	// <advc>
	if (getNumUnits() <= 0)
	{
		doDelayedDeath();
		return;
	} // </advc>
	bool bCombat = false;
	FOR_EACH_UNIT_VAR_IN(pUnit, *this)
	{
		if (pUnit->isInCombat())
		{
			if (pUnit->isInAirCombat())
				pUnit->updateAirCombat();
			else pUnit->updateCombat();
			bCombat = true;
			//break; // disabled by K-Mod.
			/*	(I've changed groupAttack to fix a problem, and now
				multiple units in a single group can be queued for combat.
				So this break can cause an infinite loop, as the
				currently fighting unit might not get updated.) */
		}
	}
	if (!bCombat)
		updateMission();
	doDelayedDeath();
}

// Returns true if group was killed...
bool CvSelectionGroup::doDelayedDeath()
{
	FAssert(getOwner() != NO_PLAYER);

	if (isBusy())
		return false;

	FOR_EACH_UNIT_VAR_IN(pUnit, *this)
	{
		pUnit->doDelayedDeath();
	}

	if (getNumUnits() <= 0)
	{
		kill();
		return true;
	}

	return false;
}


void CvSelectionGroup::playActionSound()  // advc: refactored
{
	#ifndef PITBOSS // Pitboss should not be playing sounds!
	CvUnit const* pHeadUnit = getHeadUnit();
	if (pHeadUnit == NULL)
		return;

	int iScriptId = pHeadUnit->getArtInfo(0,
				GET_PLAYER(getOwner()).getCurrentEra())->getActionSoundScriptId();
	if (iScriptId == -1)
	{
		iScriptId = GC.getInfo(pHeadUnit->getCivilizationType()).
				getActionSoundScriptId();
	}
	if (iScriptId != -1)
	{
		CvPlot const* pPlot = GC.getMap().plot(pHeadUnit->getX(), pHeadUnit->getY());
		if (pPlot != NULL)
			gDLL->Do3DSound(iScriptId, pPlot->getPoint());
	}
	#endif
}


void CvSelectionGroup::pushMission(MissionTypes eMission, int iData1, int iData2,
	MovementFlags eFlags, bool bAppend, bool bManual, MissionAITypes eMissionAI,
	CvPlot const* pMissionAIPlot, CvUnit const* pMissionAIUnit, // advc: 2x const
	bool bModified) // advc.011b
{
	PROFILE_FUNC();

	FAssert(getOwner() != NO_PLAYER);

	if (!bAppend)
	{
		if (isBusy())
			return;
		clearMissionQueue();
	}

	if (bManual)
		setAutomateType(NO_AUTOMATE);

	MissionData mission;
	mission.eMissionType = eMission;
	mission.iData1 = iData1;
	mission.iData2 = iData2;
	mission.eFlags = eFlags;
	mission.iPushTurn = GC.getGame().getGameTurn();
	mission.bModified = bModified; // advc.011b

	if (canAllMove()) // K-Mod. Do not set the AI mission type if this is just a "follow" command!
		AI().AI_setMissionAI(eMissionAI, pMissionAIPlot, pMissionAIUnit);

	insertAtEndMissionQueue(mission, !bAppend ||
			isAIControlled()); // K-Mod (AI commands should execute immediately)

	if (bManual)
	{
		if (isActiveOwned())
		{
			if (isBusy() && GC.getInfo(eMission).isSound())
				playActionSound();

			gDLL->UI().setHasMovedUnit(true);
			/*  advc.001w: Prevent help text and mouse focus from lingering after
				a command button is clicked */
			GC.getGame().setUpdateTimer(CvGame::UPDATE_MOUSE_FOCUS, 2);
		}
		CvEventReporter::getInstance().selectionGroupPushMission(this, eMission);

		doDelayedDeath();
	}
}


void CvSelectionGroup::popMission()
{
	CLLNode<MissionData>* pTailNode = tailMissionQueueNode();
	if (pTailNode != NULL)
		deleteMissionQueueNode(pTailNode);
}


bool CvSelectionGroup::autoMission() // K-Mod changed this from void to bool.
{
	FAssert(getOwner() != NO_PLAYER);
	// <advc>
	if (getNumUnits() <= 0 || headMissionQueueNode() == NULL || isBusy())
		return doDelayedDeath(); // </advc>

	bool bVisibleHuman = false;
	//if (isHuman())
	/*	K-Mod. (otherwise the automation will just reissue commands
		immediately after they are cleared, resulting in an infinite loop.) */
	if (!isAIControlled())
	{
		FOR_EACH_UNIT_IN(pUnit, *this)
		{
			if (!pUnit->alwaysInvisible())
			{
				bVisibleHuman = true;
				break;
			}
		}
	}

	//if (bVisibleHuman && GET_PLAYER(getOwner()).AI_getPlotDanger(plot(), 1) > 0)
	/*	K-Mod. I want to allow players to queue actions when in danger
		without being overruled by this clause. */
	if (bVisibleHuman &&
		headMissionQueueNode()->m_data.iPushTurn != GC.getGame().getGameTurn() &&
		!(headMissionQueueNode()->m_data.eFlags & MOVE_IGNORE_DANGER) &&
		GET_PLAYER(getOwner()).AI_isAnyPlotDanger(*plot(), 1, true, false))
		// K-Mod end
	{
		clearMissionQueue();
	}
	else
	{
		/*if (getActivityType() == ACTIVITY_MISSION)
		continueMission();
		else startMission();*/ // BtS
		// K-Mod
		if (getActivityType() != ACTIVITY_MISSION)
			startMission();
		else if (readyForMission())
			continueMission();
		// K-Mod end
	}

	return doDelayedDeath();
}


void CvSelectionGroup::updateMission()
{
	FAssert(getOwner() != NO_PLAYER);
	if (getMissionTimer() > 0)
	{
		changeMissionTimer(-1);
		if (getMissionTimer() == 0)
		{
			if (getActivityType() == ACTIVITY_MISSION)
				continueMission();
			else
			{
				if (isActiveOwned())
				{
					if (gDLL->UI().getHeadSelectedUnit() == NULL)
						GC.getGame().cycleSelectionGroups_delayed(1, true);
				}
			}
		}
	}
}


CvPlot* CvSelectionGroup::lastMissionPlot() const
{
	CLLNode<MissionData>* pMissionNode = tailMissionQueueNode();
	while (pMissionNode != NULL)
	{
		switch (pMissionNode->m_data.eMissionType)
		{
		case MISSION_MOVE_TO:
		case MISSION_ROUTE_TO:
			return GC.getMap().plot(pMissionNode->m_data.iData1, pMissionNode->m_data.iData2);
		case MISSION_MOVE_TO_UNIT:
		{
			CvUnit* pTargetUnit = GET_PLAYER((PlayerTypes)pMissionNode->m_data.iData1).
					getUnit(pMissionNode->m_data.iData2);
			if (pTargetUnit != NULL)
				return pTargetUnit->plot();
			break;
		}
		}
		pMissionNode = prevMissionQueueNode(pMissionNode);
	}
	return plot();
}


bool CvSelectionGroup::canStartMission(
	MissionTypes eMission, // advc: was int
	int iData1, int iData2,
	CvPlot const* pPlot, bool bTestVisible, bool bUseCache) /* advc: */ const
{
	if (bUseCache)
	{
		if (m_bIsBusyCache)
			return false;
	}
	else
	{
		if (isBusy())
			return false;
	}
	// K-Mod: (original code merged into CvSelectionGroup::canDoMission
	return canDoMission(eMission, iData1, iData2, pPlot, bTestVisible, false);
}


void CvSelectionGroup::startMission()
{
	//PROFILE_FUNC();

	FAssert(!isBusy());
	FAssert(headMissionQueueNode() != NULL);

	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());

	if (!GC.getGame().isMPOption(MPOPTION_SIMULTANEOUS_TURNS) && !kOwner.isTurnActive())
	{
		if (isActiveOwned())
		{
			if (IsSelected())
				GC.getGame().cycleSelectionGroups_delayed(1, true);
		}
		return;
	}

	/*if (canAllMove())
		setActivityType(ACTIVITY_MISSION);
	else setActivityType(ACTIVITY_HOLD);*/ // BtS
	// moved & changed by K-Mod.

	bool bDelete = false;
	bool bAction = false;
	bool bNuke = false;

	if (!canStartMission(headMissionQueueNode()->m_data.eMissionType,
		headMissionQueueNode()->m_data.iData1,
		headMissionQueueNode()->m_data.iData2, plot()))
	{
		bDelete = true;
	}
	else
	{
		FAssert(kOwner.isTurnActive() || kOwner.isHuman());
		// K-Mod. Moved from outside.
		if (readyForMission())
		{
			setActivityType(ACTIVITY_MISSION);
			// <advc.029> (Not sure if this is the best place for this)
			if (getHeadUnit() != NULL && getDomainType() == DOMAIN_AIR)
			{
				MissionData data = headMissionQueueNode()->m_data;
				CvPlot* pDest = GC.getMap().plot(data.iData1, data.iData2);
				/*  Both air attack and rebase are MOVE_TO missions. Want to
					clear the recon-plot only for rebase. */
				if (data.eMissionType == MISSION_MOVE_TO && pDest != NULL &&
					GET_TEAM(getTeam()).isRevealedAirBase(*pDest))
				{
					getHeadUnit()->setReconPlot(NULL);
				}
			} // </advc.029>
		}
		else setActivityType(ACTIVITY_HOLD);
		// K-Mod end
		resetBoarded(); // advc.075
		std::vector<CvUnit*> apUnitsLeftBehind; // K-Mod (advc.004c: moved up)
		bool bNotify = false;
		// Whole group effects (advc.004c: incl. mission start in a special order)
		// <advc.004c>
		bool const bStackAttack = (!isHuman() ||
				GET_PLAYER(getOwner()).isOption(PLAYEROPTION_STACK_ATTACK)); // </advc.004c>
		switch (headMissionQueueNode()->m_data.eMissionType)
		{
		case MISSION_MOVE_TO:
			/*	K-Mod. Prevent human players from accidentally
				attacking units that they can't see. */
			if (isHuman() && !GC.getMap().getPlot(
				headMissionQueueNode()->m_data.iData1,
				headMissionQueueNode()->m_data.iData2).isVisible(getTeam()) &&
				/*	<advc> Future-proofing. OK to accidentally run into an
					unseen enemy in an adjacent plot. */
				stepDistance(getX(), getY(),
				headMissionQueueNode()->m_data.iData1,
				headMissionQueueNode()->m_data.iData2) > 1) // </advc>
			{
				headMissionQueueNode()->m_data.eFlags |= MOVE_NO_ATTACK;
			}
			// also, we should allow an amphibious landing even if we are out of moves.
			if (!canAllMove())
			{
				if (groupAmphibMove(GC.getMap().getPlot(
					headMissionQueueNode()->m_data.iData1,
					headMissionQueueNode()->m_data.iData2),
					headMissionQueueNode()->m_data.eFlags))
				{
					bDelete = true;
				}
			}
			// K-Mod end
		case MISSION_ROUTE_TO:
		case MISSION_MOVE_TO_UNIT:
			break;

		case MISSION_SKIP:
			setActivityType(ACTIVITY_HOLD);
			bDelete = true;
			break;

		case MISSION_SLEEP:
			setActivityType(ACTIVITY_SLEEP);
			bNotify = true;
			bDelete = true;
			break;

		case MISSION_FORTIFY:
			setActivityType(ACTIVITY_SLEEP);
			bNotify = true;
			bDelete = true;
			break;

		case MISSION_PLUNDER:
			setActivityType(ACTIVITY_PLUNDER);
			bNotify = true;
			bDelete = true;
			break;

		case MISSION_AIRPATROL:
			setActivityType(ACTIVITY_INTERCEPT);
			bDelete = true;
			break;

		case MISSION_SEAPATROL:
			setActivityType(ACTIVITY_PATROL);
			bDelete = true;
			break;

		case MISSION_HEAL:
		/*  advc.004l: No separate sentry heal activity. Instead, units in
			ACTIVITY_HEAL are going to apply sentry behavior whenever it makes sense.
			The sentry heal mission is only needed for the proper help text. */
		case MISSION_SENTRY_HEAL:
			setActivityType(ACTIVITY_HEAL);
			bNotify = true;
			bDelete = true;
			break;

		case MISSION_SENTRY:
			setActivityType(ACTIVITY_SENTRY);
			bNotify = true;
			bDelete = true;
			break;

		case MISSION_AIRLIFT:
		case MISSION_NUKE:
		case MISSION_RECON:
		case MISSION_RANGE_ATTACK:
		case MISSION_SABOTAGE:
		case MISSION_DESTROY:
		case MISSION_STEAL_PLANS:
		case MISSION_FOUND:
		case MISSION_SPREAD:
		case MISSION_SPREAD_CORPORATION:
		case MISSION_JOIN:
		case MISSION_CONSTRUCT:
		case MISSION_DISCOVER:
		case MISSION_HURRY:
		case MISSION_TRADE:
		case MISSION_GREAT_WORK:
		case MISSION_INFILTRATE:
		case MISSION_GOLDEN_AGE:
			break;
		case MISSION_PILLAGE:
		{	// <advc> K-Mod code moved into subroutine
			CvUnit* pUnit;
			// Human units should pillage at most once per command
			std::vector<int> aiHasPillaged;
			while ((pUnit = AI().AI_bestUnitForMission(MISSION_PILLAGE,
				NULL, &aiHasPillaged)) != NULL) // </advc>
			{	// <K-Mod>
				if (pUnit->pillage(
					headMissionQueueNode()->m_data.bModified)) // advc.111
				{
					bAction = true;
					if (!isAIControlled())
						aiHasPillaged.push_back(pUnit->getID());
					// AI groups might want to reconsider their action after pillaging
					if (!isHuman() && canAllMove())
						break;
				} // </K-Mod>
				/*if (kUnit.isAttacking())
					break;*/ // Sea patrol intercept
				/*  <kekm.37> "If this selection group survives sea patrol battle
					then the game crashes because combat clears the mission queue [...].
					Since post-combat code clears the mission queue (and this sets
					activity to ACTIVITY_AWAKE) and also deals with unit selection
					for the active player, we can just skip rest of the function here." */
				if (headMissionQueueNode() == NULL || pUnit->isAttacking())
					return; // </kekm.37>
			}
			break;
		}
		case MISSION_BOMBARD:
		// <advc.004c>
		{
			CvUnit* pUnit;
			while ((pUnit = AI().AI_bestUnitForMission(MISSION_BOMBARD)) != NULL &&
				pUnit->bombard())
			{
				bAction = true;
			}
			break;
		}
		case MISSION_AIRBOMB:
		{
			CvPlot& kMissionPlot = GC.getMap().getPlot(
					headMissionQueueNode()->m_data.iData1,
					headMissionQueueNode()->m_data.iData2);
			bool bIntercepted = false;
			CvUnit* pUnit;
			while ((pUnit = AI().AI_bestUnitForMission(MISSION_AIRBOMB, &kMissionPlot)) != NULL &&
				pUnit->airBomb(kMissionPlot, &bIntercepted,
				headMissionQueueNode()->m_data.bModified)) // advc.111
			{
				bAction = true;
				if (bIntercepted && !bStackAttack)
					break;
			}
			break;
		}
		case MISSION_PARADROP:
		{
			CvPlot const& kMissionPlot = GC.getMap().getPlot(
					headMissionQueueNode()->m_data.iData1,
					headMissionQueueNode()->m_data.iData2);
			FOR_EACH_UNIT_VAR_IN(pLoopUnit, *this) // Based on K-Mod
			{
				if (!pLoopUnit->canMove())
					apUnitsLeftBehind.push_back(pLoopUnit);
			}
			IDInfo idLatestInterceptor;
			CvUnit* pUnit;
			while ((pUnit = AI().AI_bestUnitForMission(MISSION_PARADROP, &kMissionPlot)) != NULL)
			{
				IDInfo idInterceptor;
				if (pUnit->paradrop(kMissionPlot.getX(), kMissionPlot.getY(),
					&idInterceptor))
				{
					bAction = true;
				}
				else apUnitsLeftBehind.push_back(pUnit); // K-Mod
				CvUnit const* pInterceptor = ::getUnit(idInterceptor);
				if (!bStackAttack &&
					// First-time interceptor from fog of war ...
					((pInterceptor != NULL && idInterceptor != idLatestInterceptor &&
					!pInterceptor->isDead() && // future-proofing
					!pInterceptor->getPlot().isVisible(getTeam())) ||
					// ... or paratrooper killed
					pUnit == NULL || pUnit->isDead()))
				{
					break;
				}
				if (pInterceptor != NULL)
					idLatestInterceptor = idInterceptor;
			}
			break;
		} // </advc.004c>
		/*	K-Mod. If the worker is already in danger when the command is issued,
			use the MOVE_IGNORE_DANGER flag. */
		case MISSION_BUILD:
			if (!isAIControlled() &&
				headMissionQueueNode()->m_data.iPushTurn == GC.getGame().getGameTurn() &&
				// cf. condition used in CvSelectionGroup::doTurn.
				kOwner.AI_isAnyPlotDanger(*plot(), 2, true, false))
			{
				headMissionQueueNode()->m_data.eFlags |= MOVE_IGNORE_DANGER;
			}
			break;
		// K-Mod end
		case MISSION_LEAD:
		case MISSION_ESPIONAGE:
		case MISSION_RESOLVE_CRISIS: // doc
		case MISSION_REFORM_GOVERNMENT: // doc
		case MISSION_DIPLOMATIC_MISSION: // doc
		case MISSION_PERSECUTE: // doc
		case MISSION_GREAT_MISSION: // doc
		case MISSION_SATELLITE_ATTACK: // doc
		case MISSION_REBUILD: // doc
		case MISSION_DIE_ANIMATION:
			break;

		default:
			FAssert(false);
		}

		if (bNotify)
			NotifyEntity(headMissionQueueNode()->m_data.eMissionType);

		// Individual unit effects
		// (advc.004c: K-Mod abandonMoveless code deleted; handled in the paradrop case above.)
		FOR_EACH_UNIT_VAR_IN(pUnit, *this)
		{
			if (!pUnit->canMove())
				continue;
			int iData1 = headMissionQueueNode()->m_data.iData1;
			int iData2 = headMissionQueueNode()->m_data.iData2;
			switch (headMissionQueueNode()->m_data.eMissionType)
			{
			// K-Mod
			case MISSION_SKIP:
				/*	If the unit has some particular purpose for its 'skip' mission,
					automatically unload it. (eg. if a unit in a boat wants to do
					MISSIONAI_GUARD_CITY, we should unload it here.) */
				switch (AI().AI_getMissionAIType())
				{
				case NO_MISSIONAI:
				case MISSIONAI_LOAD_ASSAULT:
				case MISSIONAI_LOAD_SETTLER:
				case MISSIONAI_LOAD_SPECIAL:
					goto exit_unit_loop; // don't auto-unload. Just do nothing.
				default:
					FAssert(isAIControlled());
					pUnit->unload(); // this checks canUnload internally
					break;
				}
				break;
			// K-Mod end
			case MISSION_MOVE_TO:
			case MISSION_ROUTE_TO:
			case MISSION_MOVE_TO_UNIT:
			case MISSION_SLEEP:
			case MISSION_FORTIFY:
			case MISSION_SEAPATROL:
			case MISSION_HEAL:
			case MISSION_SENTRY_HEAL: // advc.004l
			case MISSION_SENTRY:
			case MISSION_PILLAGE:
			// <advc.004c> Already handled above
			case MISSION_BOMBARD:
			case MISSION_AIRBOMB:
			case MISSION_PARADROP: // </advc.004c>
			case MISSION_BUILD:
				// K-Mod. Nothing to do, so we might as well abort the unit loop.
				goto exit_unit_loop;
			// K-Mod. (this used to be a "do nothing" case.)
			case MISSION_AIRPATROL:
				// (We can't use 'canAirPatrol', because that checks 'isWaiting'.)
				if (!pUnit->canAirDefend(plot()))
					apUnitsLeftBehind.push_back(pUnit);
				break;
			// K-Mod end
			case MISSION_AIRLIFT:
				if (pUnit->airlift(iData1, iData2))
					bAction = true;
				break;
			case MISSION_NUKE:
				if (pUnit->nuke(iData1, iData2))
				{
					bAction = true;
					if (GC.getMap().getPlot(iData1, iData2).
						isVisibleToWatchingHuman())
					{
						bNuke = true;
					}
				}
				break;
			case MISSION_RECON:
				if (pUnit->recon(iData1, iData2))
					bAction = true;
				break;
			/*case MISSION_PARADROP:
				if (pUnit->paradrop(iData1, iData2))
					bAction = true;
				else apUnitsLeftBehind.push_back(pUnit); // K-Mod
				break;
			case MISSION_AIRBOMB:
				if (pUnit->airBomb(iData1, iData2))
					bAction = true;
				break;
			case MISSION_BOMBARD:
				if (pUnit->bombard())
					bAction = true;
				break;*/ // advc.004c: Moved up
			case MISSION_RANGE_ATTACK:
				if (pUnit->rangeStrike(iData1, iData2))
					bAction = true;
				break;
			case MISSION_PLUNDER:
				if (pUnit->plunder())
					bAction = true;
				break;
			case MISSION_SABOTAGE:
				if (pUnit->sabotage())
					bAction = true;
				break;
			case MISSION_DESTROY:
				if (pUnit->destroy())
					bAction = true;
				break;
			case MISSION_STEAL_PLANS:
				if (pUnit->stealPlans())
					bAction = true;
				break;
			case MISSION_FOUND:
				if (pUnit->found())
					bAction = true;
				break;
			case MISSION_SPREAD:
				if (pUnit->spread((ReligionTypes)iData1))
					bAction = true;
				break;
			case MISSION_SPREAD_CORPORATION:
				if (pUnit->spreadCorporation((CorporationTypes)iData1))
					bAction = true;
				break;
			case MISSION_JOIN:
				if (pUnit->join((SpecialistTypes)iData1))
					bAction = true;
				break;
			case MISSION_CONSTRUCT:
				if (pUnit->construct((BuildingTypes)iData1))
					bAction = true;
				break;
			case MISSION_DISCOVER:
				if (pUnit->discover())
					bAction = true;
				break;
			case MISSION_HURRY:
				if (pUnit->hurry())
					bAction = true;
				break;
			case MISSION_TRADE:
				if (pUnit->trade())
					bAction = true;
				break;
			case MISSION_GREAT_WORK:
				if (pUnit->greatWork())
					bAction = true;
				break;
			case MISSION_INFILTRATE:
				if (pUnit->infiltrate())
					bAction = true;
				break;
			case MISSION_GOLDEN_AGE:
				//just play animation, not golden age - JW
				if (iData1 != -1)
				{
					CvMissionDefinition kMission;
					kMission.setMissionTime(GC.getInfo(MISSION_GOLDEN_AGE).getTime() *
							gDLL->getSecsPerTurn());
					kMission.setUnit(BATTLE_UNIT_ATTACKER, pUnit);
					kMission.setUnit(BATTLE_UNIT_DEFENDER, NULL);
					kMission.setPlot(pUnit->plot());
					kMission.setMissionType(MISSION_GOLDEN_AGE);
					gDLL->getEntityIFace()->AddMission(&kMission);
					pUnit->NotifyEntity(MISSION_GOLDEN_AGE);
					bAction = true;
				}
				else if (pUnit->goldenAge())
					bAction = true;
				break;
			case MISSION_LEAD:
				if (pUnit->lead(iData1))
					bAction = true;
				break;
			case MISSION_RESOLVE_CRISIS: // doc
				if (pUnit->resolveCrisis())
					bAction = true;
				break;
			case MISSION_REFORM_GOVERNMENT: // doc
				if (pUnit->reformGovernment())
					bAction = true;
				break;
			case MISSION_DIPLOMATIC_MISSION: // doc
				if (pUnit->diplomaticMission())
					bAction = true;
				break;
			case MISSION_PERSECUTE: // doc
				if (pUnit->persecute(NO_RELIGION))
					bAction = true;
				break;
			case MISSION_GREAT_MISSION: // doc
				if (pUnit->greatMission())
					bAction = true;
				break;
			case MISSION_SATELLITE_ATTACK: // doc
				if (pUnit->satelliteAttack())
					bAction = true;
				break;
			case MISSION_REBUILD: // doc
				if (pUnit->rebuild())
					bAction = true;
				break;
			case MISSION_ESPIONAGE:
				if (pUnit->espionage((EspionageMissionTypes)iData1, iData2))
					bAction = true;
				goto exit_unit_loop; // allow one unit at a time to do espionage
			case MISSION_DIE_ANIMATION:
				bAction = true;
				break;
			default:
				FAssert(false);
			}
			if (getNumUnits() == 0 || headMissionQueueNode() == NULL)
				break;
		} exit_unit_loop: // advc (had been accomplished through pUnitNode=NULL before)
		// K-Mod
		if (!apUnitsLeftBehind.empty())
		{
			FAssert(isHuman()); // Not a problem but don't want the AI to choose missions that cause the group to separate.
			FAssert(((int)apUnitsLeftBehind.size()) < getNumUnits()); // we should never leave _everyone_ behind!
			apUnitsLeftBehind[0]->joinGroup(NULL, true);
			CvSelectionGroup* pNewGroup = apUnitsLeftBehind[0]->getGroup();
			for (size_t i = 1; i < apUnitsLeftBehind.size(); i++)
			{
				apUnitsLeftBehind[i]->joinGroup(pNewGroup, true);
			}
		} // K-Mod end
	} // end if (can start mission)

	if (getNumUnits() > 0 && headMissionQueueNode() != NULL)
	{
		if (bAction && isHuman() && getPlot().isVisibleToWatchingHuman())
			updateMissionTimer();
		if (bNuke)
			setMissionTimer(nukeMissionTime()); // advc.002m: Moved into new function
		if (!isBusy())
		{
			if (bDelete)
			{
				deleteMissionQueueNode(headMissionQueueNode());
				// K-Mod
				if (headMissionQueueNode() != NULL)
					activateHeadMission();
				// K-Mod end
				if (isActiveOwned() && IsSelected())
				{
					GC.getGame().cycleSelectionGroups_delayed(
							kOwner.isOption(PLAYEROPTION_QUICK_MOVES) ?
							1 : 2, true, readyToSelect(true));
				}
			}
			else if (getActivityType() == ACTIVITY_MISSION)
				continueMission();
			// K-Mod
			else if (isActiveOwned() && IsSelected() && //!canAnyMove()
				/*	advc.001: Mission won't start unless all can move.
					Need to cycle if mission not started. BtS already
					gets this wrong. */
				!canAllMove())
			{
				GC.getGame().cycleSelectionGroups_delayed(kOwner.
						isOption(PLAYEROPTION_QUICK_MOVES) ? 1 : 2, true);
			} // K-Mod end
		}
	}
}

/*	K-Mod. CvSelectionGroup::continueMission used to be a recursive function.
	I've moved the bulk of the function into a new function, and
	turned continueMission into just a simple loop to remove the recursion. */
void CvSelectionGroup::continueMission()
{
	int iSteps = 0;
	while (continueMission_bulk(iSteps))
	{
		iSteps++;
	}
}

// return true if we are ready to take another step
bool CvSelectionGroup::continueMission_bulk(int iSteps)
{
	PROFILE_FUNC(); // advc (This covers more ground than pushMission)
	FAssert(!isBusy());
	FAssert(getOwner() != NO_PLAYER);
	FAssert(getActivityType() == ACTIVITY_MISSION);

	CLLNode<MissionData>* pHeadMission = headMissionQueueNode();
	if (pHeadMission == NULL)
	{
		FAssert(pHeadMission != NULL);
		// just in case...
		setActivityType(ACTIVITY_AWAKE);
		return false;
	}
	MissionData missionData = pHeadMission->m_data;
	CvGame& kGame = GC.getGame();
	CvPlot* pFromPlot = plot(); // advc.102
	bool bDone = false;
	bool bAction = false;

	if (!(missionData.eFlags & MOVE_NO_ATTACK) && // K-Mod
		(missionData.iPushTurn == kGame.getGameTurn() ||
		missionData.eFlags & MOVE_THROUGH_ENEMY))
	{
		if (missionData.eMissionType == MISSION_MOVE_TO)
		{
			bool bFailedAlreadyFighting/*advc:*/=false; // (safer)
			if (groupAttack(missionData.iData1, missionData.iData2,
				missionData.eFlags, bFailedAlreadyFighting,
				/* advc.048: */ missionData.bModified))
			{
				bDone = true;
			}
		}
		/*	K-Mod. We need to do a similar check for MISSION_MOVE_TO_UNIT,
			because with the MOVE_ATTACK_STACK flag,
			MOVE_TO_UNIT might actually want to attack something!
			Note: the "else" is not just for efficiency.
			The code above may have actually killed "this" unit! */
		else if (missionData.eMissionType == MISSION_MOVE_TO_UNIT &&
			(missionData.eFlags & MOVE_ATTACK_STACK))
		{	bool bDummy=false;
			CvUnit* pTargetUnit = GET_PLAYER((PlayerTypes)missionData.iData1).
					getUnit(missionData.iData2);
			if (pTargetUnit && groupAttack(pTargetUnit->getX(), pTargetUnit->getY(),
				missionData.eFlags, bDummy, /* advc.048: */ false))
			{
				bDone = true;
			}
		} // K-Mod end
	}
	/*	extra crash protection, should never happen
		(but a previous bug in groupAttack was causing a NULL here)
		while that bug is fixed, no reason to not be a little more careful
		K-Mod note: Actually, the mission queue is always cleared after combat.
		So this is required regardless of any bugs. */
	pHeadMission = headMissionQueueNode();
	if (pHeadMission == NULL)
	{
		setActivityType(ACTIVITY_AWAKE);
		/*	K-Mod. Since I removed the cycle trigger from deactivateHeadMission,
			we need it here. */
		if (isActiveOwned() && IsSelected())
			kGame.cycleSelectionGroups_delayed(1, true, canAnyMove());
		return false;
	}
	missionData = pHeadMission->m_data;

	/*	K-Mod. 'direct attack' should be used for attack commands only.
		(But in simultaneous turns mode, the defenders might have already left.) */
	FAssert(bDone || !(missionData.eFlags & MOVE_DIRECT_ATTACK) || kGame.isMPOption(MPOPTION_SIMULTANEOUS_TURNS));

	if (!bDone && getNumUnits() > 0 && /* K-Mod: */ readyForMission()) //canAllMove()
	{
		switch (missionData.eMissionType)
		{
		case MISSION_MOVE_TO:
			if (getDomainType() == DOMAIN_AIR)
			{
				groupPathTo(missionData.iData1, missionData.iData2, missionData.eFlags);
				bDone = true;
			}
			else if (groupPathTo(missionData.iData1, missionData.iData2, missionData.eFlags))
			{
				bAction = true;
				/*  advc: Not sure if groupPathTo can pop the head mission;
					safer to update pHeadMission. */
				pHeadMission = headMissionQueueNode();
				if (getNumUnits() > 0 && !canAllMove() && pHeadMission != NULL)
				{
					missionData = pHeadMission->m_data;
					if (groupAmphibMove(GC.getMap().getPlot(
						missionData.iData1, missionData.iData2), missionData.eFlags))
					{
						bAction = false;
						bDone = true;
					}
				}
			}
			else
			{
				bDone = true;
				/*	<advc.pf> Failure to find a path here can be normal if the move
					was scheduled on an earlier turn; it's probably also normal for
					units ready to defend. If the unit doesn't get stuck in a loop
					subsequently (separate assertion), it's probably fine anyway.
					If it does get stuck, then this earlier assertion should help
					diagnose the problem. There might still be rare cases in which
					the use of path data by GroupStepMetric causes the pathfinder
					to fail, specifically when a worker retreats from enemy units.
					If indeed very rare, then probably not worth trying to fix. */
				if (missionData.iPushTurn >= GC.getGame().getGameTurn() &&
					(!canFight() || (missionData.eFlags & MOVE_AVOID_DANGER)) &&
					!hasMoved())
				{
				#ifdef FASSERT_ENABLE
					// Ad-hoc cache to avoid repeating the assertion popup
					static int iLastGroupID = FFreeList::INVALID_INDEX;
					if (iLastGroupID != getID())
					{
						FErrorMsg("Danger-averse unit failed to move?");
						iLastGroupID = getID();
					}
				#endif
					if (isAIControlled())
						pushMission(MISSION_SKIP);
				}
				// </advc.pf>
			}
			break;

		case MISSION_ROUTE_TO:
			if (groupRoadTo(missionData.iData1, missionData.iData2, missionData.eFlags))
				bAction = true;
			else bDone = true;
			break;

		case MISSION_MOVE_TO_UNIT:
		{
			CvPlot const& kPlot = getPlot();
			if (getHeadUnitAIType() == UNITAI_CITY_DEFENSE && kPlot.isCity() &&
				kPlot.getTeam() == getTeam())
			{
				if (kPlot.getBestDefender(getOwner())->getGroup() == this)
				{	/*	<advc.001> UNITAI_CITY_DEFENSE unit may be passing through
						the city of a teammate. Should only have to stay there
						if no other team member can defend. */
					bool bStay = (kPlot.getOwner() == getOwner());
					if (!bStay)
					{
						FAssert(GET_TEAM(getTeam()).getNumMembers() > 1);
						bStay = true;
						for (MemberIter itMember(getTeam()); itMember.hasNext(); ++itMember)
						{
							if (itMember->getID() != getOwner() &&
								kPlot.getBestDefender(itMember->getID()) != NULL)
							{
								bStay = false;
								break;
							}
						}
						FAssertMsg(!bStay, "Can probably happen; will it get this group stuck in a loop?");
					}
					if (bStay) // </advc.001>
					{
						// (advc: Does this always get units stuck? Doesn't appear to ...)
						bAction = false;
						bDone = true;
						break;
					}
				}
			}
			CvUnitAI const* pTargetUnit = GET_PLAYER((PlayerTypes)missionData.iData1).
					AI_getUnit(missionData.iData2);
			if (pTargetUnit == NULL)
			{
				bDone = true;
				break;
			}
			/*	(BETTER_BTS_AI_MOD 12/07/08, 08/08/09, Maniac & jdog5000, General AI
				pickup of stranded units - deleted by K-Mod.) */

			MissionAITypes eMissionAI = AI().AI_getMissionAIType(); // advc.003u
			if (eMissionAI != MISSIONAI_SHADOW && eMissionAI != MISSIONAI_GROUP)
			{
				if (!kPlot.isOwned() || kPlot.getOwner() == getOwner())
				{
					CvPlot* pMissionPlot = pTargetUnit->AI_getGroup()->AI_getMissionAIPlot();
					if (pMissionPlot != NULL && NO_TEAM != pMissionPlot->getTeam())
					{
						if (pMissionPlot->isOwned() && pTargetUnit->AI_isPotentialEnemyOf(
							pMissionPlot->getTeam(), *pMissionPlot))
						{
							bAction = false;
							bDone = true;
							break;
						}
					}
				}
			}
			if (groupPathTo(pTargetUnit->getX(), pTargetUnit->getY(), missionData.eFlags))
				bAction = true;
			else bDone = true;
			break;
		}

		case MISSION_SKIP:
		case MISSION_SLEEP:
		case MISSION_FORTIFY:
		case MISSION_PLUNDER:
		case MISSION_AIRPATROL:
		case MISSION_SEAPATROL:
		case MISSION_HEAL:
		case MISSION_SENTRY_HEAL: // advc.004l
		case MISSION_SENTRY:
			FAssert(false);
			break;

		case MISSION_AIRLIFT:
		case MISSION_NUKE:
		case MISSION_RECON:
		case MISSION_PARADROP:
		case MISSION_AIRBOMB:
		case MISSION_BOMBARD:
		case MISSION_RANGE_ATTACK:
		case MISSION_PILLAGE:
		case MISSION_SABOTAGE:
		case MISSION_DESTROY:
		case MISSION_STEAL_PLANS:
		case MISSION_FOUND:
		case MISSION_SPREAD:
		case MISSION_SPREAD_CORPORATION:
		case MISSION_JOIN:
		case MISSION_CONSTRUCT:
		case MISSION_DISCOVER:
		case MISSION_HURRY:
		case MISSION_TRADE:
		case MISSION_GREAT_WORK:
		case MISSION_INFILTRATE:
		case MISSION_GOLDEN_AGE:
		case MISSION_LEAD:
		case MISSION_ESPIONAGE:
		case MISSION_RESOLVE_CRISIS: // doc
		case MISSION_REFORM_GOVERNMENT: // doc
		case MISSION_DIPLOMATIC_MISSION: // doc
		case MISSION_PERSECUTE: // doc
		case MISSION_GREAT_MISSION: // doc
		case MISSION_SATELLITE_ATTACK: // doc
		case MISSION_REBUILD: // doc
		case MISSION_DIE_ANIMATION:
			break;

		case MISSION_BUILD:
			if(!groupBuild((BuildTypes)missionData.iData1,
				!missionData.bModified)) // advc.011b
			{
				bDone = true;
			}
			break;

		default: FAssert(false);
		}
	}

	pHeadMission = headMissionQueueNode();
	if (pHeadMission == NULL || getNumUnits() <= 0)
		return false;
	missionData = pHeadMission->m_data;

	if (!bDone)
	{
		switch (missionData.eMissionType)
		{
		case MISSION_MOVE_TO:
			missionData.eFlags |= MOVE_HAS_STEPPED; // K-Mod
			if (at(missionData.iData1, missionData.iData2))
			{
				bDone = true;
				handleBoarded(); // advc.075
			}
			break;

		case MISSION_ROUTE_TO:
			if (at(missionData.iData1, missionData.iData2))
			{
				if (getBestBuildRoute(getPlot()) == NO_ROUTE)
					bDone = true;
			}
			break;

		case MISSION_MOVE_TO_UNIT: {
			CvUnit* pTargetUnit = GET_PLAYER((PlayerTypes)missionData.iData1).
					getUnit(missionData.iData2);
			if (pTargetUnit == NULL || atPlot(pTargetUnit->plot()))
				bDone = true;
			break;
		}
		case MISSION_SKIP:
		case MISSION_SLEEP:
		case MISSION_FORTIFY:
		case MISSION_PLUNDER:
		case MISSION_AIRPATROL:
		case MISSION_SEAPATROL:
		case MISSION_HEAL:
		case MISSION_SENTRY_HEAL: // advc.004l
		case MISSION_SENTRY:
			FAssert(false);
			break;

		case MISSION_AIRLIFT:
		case MISSION_NUKE:
		case MISSION_RECON:
		case MISSION_PARADROP:
		case MISSION_AIRBOMB:
		case MISSION_BOMBARD:
		case MISSION_RANGE_ATTACK:
		case MISSION_PILLAGE:
		case MISSION_SABOTAGE:
		case MISSION_DESTROY:
		case MISSION_STEAL_PLANS:
		case MISSION_FOUND:
		case MISSION_SPREAD:
		case MISSION_SPREAD_CORPORATION:
		case MISSION_JOIN:
		case MISSION_CONSTRUCT:
		case MISSION_DISCOVER:
		case MISSION_HURRY:
		case MISSION_TRADE:
		case MISSION_GREAT_WORK:
		case MISSION_INFILTRATE:
		case MISSION_GOLDEN_AGE:
		case MISSION_LEAD:
		case MISSION_ESPIONAGE:
		case MISSION_RESOLVE_CRISIS: // doc
		case MISSION_REFORM_GOVERNMENT: // doc
		case MISSION_DIPLOMATIC_MISSION: // doc
		case MISSION_PERSECUTE: // doc
		case MISSION_GREAT_MISSION: // doc
		case MISSION_SATELLITE_ATTACK: // doc
		case MISSION_REBUILD: // doc
		case MISSION_DIE_ANIMATION:
			bDone = true;
			break;

		case MISSION_BUILD:
			// XXX what happens if two separate worker groups are both building the mine...
			/*if (getPlot().getBuildType() != ((BuildTypes)(headMissionQueueNode()->m_data.iData1)))
					bDone = true; */
			break;

		default:
			FAssert(false);
			break;
		}
	}

	if (bAction &&
		//(bDone || !canAllMove())
		(bDone || !readyForMission())) // K-Mod (I don't think this actually matters)
	{	// <advc.102>
		bool bDestVisible = getPlot().isVisibleToWatchingHuman();
		bool bStartVisible = pFromPlot->isVisibleToWatchingHuman();
		// Previously only DestVisible was checked
		if (bDestVisible || (bStartVisible && m->bInitiallyVisible))
		{
			// Pass pFromPlot
			updateMissionTimer(iSteps, pFromPlot);
			if (kGame.getActivePlayer() != NO_PLAYER && !isActiveOwned())
			{
				bool bDestActiveVisible = !isInvisible(kGame.getActiveTeam());
				CvDLLInterfaceIFaceBase* pInterface = gDLL->getInterfaceIFace();
				if (gDLL->getEngineIFace()->isGlobeviewUp())
				{
					if (bDestActiveVisible && kGame.getCurrentLayer() == GLOBE_LAYER_UNIT &&
						getPlot().isActiveVisible(true))
					{
						pInterface->setDirty(GlobeLayer_DIRTY_BIT, true);
					}
				}
				else if (showMoves(*pFromPlot))
				{
					// Show FromPlot when moving out of sight
					bool bStartActiveVisible = (bDestActiveVisible &&
							pFromPlot->isActiveVisible(false));
					bDestActiveVisible = (bDestActiveVisible &&
							getPlot().isActiveVisible(false));
					if (bDestActiveVisible && bDestVisible)
						pInterface->lookAt(getPlot().getPoint(), CAMERALOOKAT_NORMAL);
					else if (bStartActiveVisible && bStartVisible)
						pInterface->lookAt(pFromPlot->getPoint(), CAMERALOOKAT_NORMAL);
					// </advc.102>
				}
			}
		}
	}

	if (bDone)
	{	/*if (!isBusy()) {
			if (isActiveOwned()) {
				if (IsSelected()) {
					if ((headMissionQueueNode()->m_data.eMissionType == MISSION_MOVE_TO) ||
						(headMissionQueueNode()->m_data.eMissionType == MISSION_ROUTE_TO) ||
						(headMissionQueueNode()->m_data.eMissionType == MISSION_MOVE_TO_UNIT))
						kGame.cycleSelectionGroups_delayed(GET_PLAYER(getOwner()).isOption(PLAYEROPTION_QUICK_MOVES) ? 1 : 2, true, true);
				}
			}
			deleteMissionQueueNode(headMissionQueueNode());
		}*/ // BtS
		/*	K-Mod. If rapid-unit-cycling is enabled, I want to cycle as soon a possible.
			Otherwise, I want to mimic the original behaviour.
			Note: I've removed cycleSelectionGroups_delayed(1, true, canAnyMove())
			from inside CvSelectionGroup::deactivateHeadMission */
		if (isActiveOwned() && IsSelected())
		{
			if ((missionData.eMissionType == MISSION_MOVE_TO ||
				missionData.eMissionType == MISSION_ROUTE_TO ||
				missionData.eMissionType == MISSION_MOVE_TO_UNIT) && !isBusy())
			{
				kGame.cycleSelectionGroups_delayed(GET_PLAYER(getOwner()).
						isOption(PLAYEROPTION_QUICK_MOVES) ?
						2 : 3, true, canAnyMove()); // (? 1 : 2) + 1
			}
			else kGame.cycleSelectionGroups_delayed(1, true, canAnyMove());
		}

		if (!isBusy())
		{	/*	If this was a build mission, end the mission
				for all of our workers groups with the same job.
				(this isn't strictly neccessary, because the workers will
				know to end their own mission anyway, but ending it now
				helps give a better unit cycling order.) */
			if (missionData.eMissionType == MISSION_BUILD)
			{
				// (the head mission will be deleted soon)
				BuildTypes const eBuildType = (BuildTypes)missionData.iData1;
				FOR_EACH_UNIT_VAR_IN(pLoopUnit, getPlot())
				{
					if (pLoopUnit->isGroupHead() &&
						pLoopUnit->getOwner() == getHeadOwner())
					{
						CvSelectionGroup* pLoopGroup = pLoopUnit->getGroup();
						if (pLoopGroup->getMissionType(0) == MISSION_BUILD &&
							pLoopGroup->getMissionData1(0) == eBuildType)
						{
							pLoopGroup->deleteMissionQueueNode(
									pLoopGroup->headMissionQueueNode());
						}
					}
				}
			}
			else deleteMissionQueueNode(pHeadMission);

			// start the next mission
			if (headMissionQueueNode() != NULL)
				activateHeadMission();
			// <advc.153>
			else if (!isAIControlled() &&
				(missionData.eMissionType == MISSION_BUILD ||
				// Too annoying?
				//missionData.eMissionType == MISSION_MOVE_TO ||
				missionData.eMissionType == MISSION_PILLAGE ||
				missionData.eMissionType == MISSION_BOMBARD ||
				missionData.eMissionType == MISSION_AIRBOMB) &&
				canAnyMove() && !canAllMove())
			{
				if (IsSelected())
				{
					CvUnit* pSelectedUnit = NULL;
					int iSelIndex = 0;
					while ((pSelectedUnit = gDLL->UI().getSelectionUnit(iSelIndex++)) != NULL)
					{
						if (!pSelectedUnit->canMove())
						{
							gDLL->UI().removeFromSelectionList(pSelectedUnit);
							iSelIndex--;
						}
					}
				}
				/*	Don't want to split the group if currently selected by a player.
					But how can we tell in network games? We know only the selection
					of the active player. Let's decide based on mission type. */
				if ((kGame.isNetworkMultiPlayer() ?
					missionData.eMissionType == MISSION_BUILD :
					!IsSelected()) &&
					!GET_PLAYER(getOwner()).isEndTurn())
				{	// Based on K-Mod code in startMission
					std::vector<CvUnit*> apCanMove;
					FOR_EACH_UNIT_VAR_IN(pUnit, *this)
					{
						if (pUnit->canMove())
							apCanMove.push_back(pUnit);
					}
					apCanMove[0]->joinGroup(NULL);
					CvSelectionGroup* pNewGroup = apCanMove[0]->getGroup();
					for (size_t i = 1; i < apCanMove.size(); i++)
						apCanMove[i]->joinGroup(pNewGroup);
				}
			} // </advc.153>
		} // K-Mod end
	}
	else
	{	//if (canAllMove())
		if (readyForMission()) // K-Mod
		{
			//continueMission(iSteps + 1);
			return true;
		}
		else if (!isBusy() && isActiveOwned())
		{
			if (IsSelected())
				kGame.cycleSelectionGroups_delayed(1, true);
		}
	}
	return false;
}


bool CvSelectionGroup::canDoCommand(CommandTypes eCommand, int iData1, int iData2,
	bool bTestVisible, bool bUseCache)
{
	PROFILE_FUNC();

	if (bUseCache)
	{
		if(m_bIsBusyCache)
			return false;
	}
	else
	{
		if (isBusy())
			return false;
	}

	if(!canEverDoCommand(eCommand, iData1, iData2, bTestVisible, bUseCache))
		return false;

	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		if (pUnit->canDoCommand(eCommand, iData1, iData2, bTestVisible, false))
		{
			if(eCommand != COMMAND_LOAD) // advc.123c
				return true;
		} /*  <advc.123c> Normally, a group can do a command if any unit can do it,
			  but in the case of loading, it seems easier to make an exception than
			  to have the load command fail for some of the selected units. */
		else if(eCommand == COMMAND_LOAD)
			return false; // </advc.123c>
	}

	return (eCommand == COMMAND_LOAD); // advc.123c: instead of false
}

bool CvSelectionGroup::canEverDoCommand(CommandTypes eCommand, int iData1, int iData2,
	bool bTestVisible, bool bUseCache)
{
	if(eCommand == COMMAND_LOAD)
	{
		FOR_EACH_UNIT_IN(pUnit, getPlot())
		{
			if (!pUnit->isFull())
				return true;
		}
		return false; // no cargo space on this plot
	}
	else if(eCommand == COMMAND_UNLOAD)
	{
		FOR_EACH_UNIT_IN(pUnit, *this)
		{
			if (pUnit->isCargo())
				return true;
		}
		return false; // no loaded unit
	}
	else if(eCommand == COMMAND_UPGRADE)
	{
		if(bUseCache)
		{
			// see if any of the different units can upgrade to this unit type
			for (size_t i = 0; i < m_aDifferentUnitCache.size(); i++)
			{
				CvUnit const* pUnit = m_aDifferentUnitCache[i];
				if(pUnit->canDoCommand(eCommand, iData1, iData2, bTestVisible, false))
					return true;
			}
			return false;
		}
	}
	return true;
}

void CvSelectionGroup::setupActionCache()
{
	m_bIsBusyCache = isBusy(); // cache busy calculation

	// cache different unit types
	m_aDifferentUnitCache.erase(m_aDifferentUnitCache.begin(), m_aDifferentUnitCache.end());
	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		if (pUnit->isReadyForUpgrade())
		{
			UnitTypes eUnitType = pUnit->getUnitType();
			bool bFound = false;
			for(size_t i = 0; i < m_aDifferentUnitCache.size(); i++)
			{
				if (eUnitType == m_aDifferentUnitCache[i]->getUnitType())
				{
					bFound = true;
					break;
				}
			}
			if (!bFound)
				m_aDifferentUnitCache.push_back(pUnit);
		}
	}
}

// Returns true if one of the units can support the interface mode...
bool CvSelectionGroup::canDoInterfaceMode(InterfaceModeTypes eInterfaceMode)
{
	PROFILE_FUNC();

	FAssert(eInterfaceMode != NO_INTERFACEMODE);

	if (isBusy())
		return false;

	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		switch (eInterfaceMode)
		{
		case INTERFACEMODE_GO_TO:
			if (getDomainType() != DOMAIN_AIR && getDomainType() != DOMAIN_IMMOBILE)
				return true;
			break;

		case INTERFACEMODE_GO_TO_TYPE:
			if (getDomainType() != DOMAIN_AIR && getDomainType() != DOMAIN_IMMOBILE)
			{
				if (pUnit->getPlot().plotCount(PUF_isUnitType, pUnit->getUnitType(),
					-1, pUnit->getOwner()) > 1)
				{
					return true;
				}
			}
			break;

		case INTERFACEMODE_GO_TO_ALL:
			if (getDomainType() != DOMAIN_AIR && getDomainType() != DOMAIN_IMMOBILE)
			{
				if (pUnit->getPlot().plotCount(NULL, -1, -1, pUnit->getOwner()) > 1)
					return true;
			}
			break;

		case INTERFACEMODE_ROUTE_TO:
			if (pUnit->AI_getUnitAIType() == UNITAI_WORKER)
			{
				if (pUnit->canBuildRoute())
					return true;
			}
			break;

		case INTERFACEMODE_AIRLIFT:
			if (pUnit->canAirlift(pUnit->plot()))
				return true;
			break;

		case INTERFACEMODE_NUKE:
			if (pUnit->canNuke(pUnit->plot()))
				return true;
			break;

		case INTERFACEMODE_RECON:
			if (pUnit->canRecon(pUnit->plot()))
				return true;
			break;

		case INTERFACEMODE_PARADROP:
			if (pUnit->canParadrop(pUnit->plot()))
				return true;
			break;

		case INTERFACEMODE_AIRBOMB:
			if (pUnit->canAirBomb())
				return true;
			break;

		case INTERFACEMODE_RANGE_ATTACK:
			if (pUnit->canRangeStrike())
				return true;
			break;

		case INTERFACEMODE_AIRSTRIKE:
			if (pUnit->getDomainType() == DOMAIN_AIR)
			{
				if (pUnit->canAirAttack())
					return true;
			}
			break;

		case INTERFACEMODE_REBASE:
			if (pUnit->getDomainType() == DOMAIN_AIR)
				return true;
			break;
		}
	}

	return false;
}

// Returns true if one of the units can execute the interface mode at the specified plot...
bool CvSelectionGroup::canDoInterfaceModeAt(InterfaceModeTypes eInterfaceMode, CvPlot* pPlot)
{
	FAssert(eInterfaceMode != NO_INTERFACEMODE);
	// <advc> Upfront treatment of modes that don't require any unit
	switch (eInterfaceMode)
	{
	case INTERFACEMODE_AIRLIFT:
	case INTERFACEMODE_NUKE:
	case INTERFACEMODE_RECON:
	case INTERFACEMODE_PARADROP:
	case INTERFACEMODE_AIRBOMB:
	case INTERFACEMODE_RANGE_ATTACK:
	case INTERFACEMODE_AIRSTRIKE:
	case INTERFACEMODE_REBASE:
		break;
	default: return true;
	} // </advc>
	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		if (pUnit == NULL)
			continue;
		switch (eInterfaceMode)
		{
		case INTERFACEMODE_AIRLIFT:
			if (pUnit->canAirliftAt(pUnit->plot(), pPlot->getX(), pPlot->getY()))
				return true;
			break;
		case INTERFACEMODE_NUKE:
			if (pUnit->canNukeAt(pUnit->getPlot(), pPlot->getX(), pPlot->getY(),
				pUnit->getTeam())) // kekm.7 (advc)
			{
				return true;
			}
			break;
		case INTERFACEMODE_RECON:
			if (pUnit->canReconAt(pUnit->plot(), pPlot->getX(), pPlot->getY()))
				return true;
			break;
		case INTERFACEMODE_PARADROP:
			if (pUnit->canParadropAt(pUnit->plot(), pPlot->getX(), pPlot->getY()))
				return true;
			break;
		case INTERFACEMODE_AIRBOMB:
			if (pUnit->canAirBombAt(*pPlot))
				return true;
			break;
		case INTERFACEMODE_RANGE_ATTACK:
			if (pUnit->canRangeStrikeAt(pUnit->plot(), pPlot->getX(), pPlot->getY()))
				return true;
			break;
		case INTERFACEMODE_AIRSTRIKE:
			if (pUnit->canMoveInto(*pPlot, true, false, false, false))
				return true;
			break;
		case INTERFACEMODE_REBASE:
			if (pUnit->canMoveInto(*pPlot))
				return true;
			break;
		}
	}
	return false;
}


bool CvSelectionGroup::isHuman() const
{
	if (getOwner() != NO_PLAYER)
		return GET_PLAYER(getOwner()).isHuman();
	return true;
}


bool CvSelectionGroup::isBusy() const
{
	if (getNumUnits() <= 0)
		return false;

	if (getMissionTimer() > 0)
		return true;

	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		if (pUnit != NULL && pUnit->isInCombat())
			return true;
	}
	return false;
}


bool CvSelectionGroup::isCargoBusy() const
{
	if (getNumUnits() <= 0)
		return false;
	// advc.opt: Replacing a nested loop. Now the same logic as in canCargoAllMove.
	FOR_EACH_UNIT_IN(pLoadedUnit, getPlot())
	{
		if (pLoadedUnit->isCargo() &&
			pLoadedUnit->getTransportUnit()->getGroup() == this &&
			pLoadedUnit->getGroup()->isBusy())
		{
			return true;
		}
	}
	return false;
}


int CvSelectionGroup::baseMoves() const
{
	int iBestValue = MAX_INT;
	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		iBestValue = std::min(iBestValue, pUnit->baseMoves());
	}
	return iBestValue;
}

// K-Mod
int CvSelectionGroup::maxMoves() const
{
	int iMoves = MAX_INT; // (was 0 - see comment below)
	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		iMoves = std::min(iMoves, pUnit->maxMoves());
		/*	note: originally this used std::max -- pretty sure that was just a mistake.
			I don't know why they'd want to use that. */
	}
	return iMoves;
}

int CvSelectionGroup::movesLeft() const
{
	int iMoves = MAX_INT;
	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		iMoves = std::min(iMoves, pUnit->movesLeft());
	}
	return iMoves;
} // K-Mod end


bool CvSelectionGroup::isWaiting() const
{
	/*return (getActivityType() == ACTIVITY_HOLD ||
			getActivityType() == ACTIVITY_SLEEP ||
			getActivityType() == ACTIVITY_HEAL ||
			getActivityType() == ACTIVITY_SENTRY ||
			getActivityType() == ACTIVITY_PATROL ||
			getActivityType() == ACTIVITY_PLUNDER ||
			getActivityType() == ACTIVITY_INTERCEPT);*/ // BtS
	// K-Mod. (same functionality)
	return !(getActivityType() == ACTIVITY_AWAKE || getActivityType() == ACTIVITY_MISSION);
	// K-Mod end
}

/*	K-Mod: return true if the first unit in the first group
	comes before the first unit in the second group.
	(note: the purpose of this function is to return _false_
	when the groupCycleDistance should include a penalty.) */
bool CvSelectionGroup::isBeforeGroupOnPlot(CvSelectionGroup const& kOther)const
{
	FAssert(this != &kOther);
	FAssert(at(kOther.getPlot()));

	//int iOtherUnits = kOther.getNumUnits();
	FOR_EACH_UNIT_IN(pUnit, getPlot())
	{
		if (pUnit->getGroup() == this)
			return true;
		if (pUnit->getGroup() == &kOther)
			return false;
		/*iOtherUnits--;
		if (iOtherUnits <= 0)
			break;*/
	}
	FAssert(false);
	return false;
}

/*	K-Mod: return the 'cost' of cycling from pFirstGroup to pSecondGroup.
	(eg. a big jump to a different type of unit, then it should be a high cost.) */
int CvSelectionGroup::groupCycleDistance(CvSelectionGroup const& kOther) const
{
	FAssert(this != &kOther);

	CvUnit const& kHead = *getHeadUnit();
	CvUnit const& kOtherHead = *kOther.getHeadUnit();

	const int iBaseScale = 4;
	int iPenalty = 0;
	if (kHead.getUnitType() != kOtherHead.getUnitType())
	{	/*  <advc.075> When a unit in cargo is told to skip its turn, we want
			the ship to be selected before its cargo on the next turn.
			(Or would it be better to do this through isBeforeGroupOnPlot?) */
		if (kHead.isHuman() && kHead.isCargo() != kOtherHead.isCargo())
			iPenalty += 5;
		else /* </advc.075> */ if (kHead.canFight() != kOtherHead.canFight())
			iPenalty += 4;
		else
		{
			if (kHead.canFight())
			{
				if (kHead.getUnitCombatType() != kOtherHead.getUnitCombatType())
					iPenalty += 2;
				if (kHead.canAttack() != kOtherHead.canAttack() ||
					// <advc.315>
					kHead.getUnitInfo().isMostlyDefensive() !=
					kOtherHead.getUnitInfo().isMostlyDefensive()) // </advc.315>
				{
					iPenalty += 1;
				}
			}
			//else iPenalty += 2;
			// <advc.004c> Distinguish civilians from military (air) units
			else if (kHead.canCombat() != kOtherHead.canCombat())
				iPenalty += 3;
			else if (kHead.canCombat())
				iPenalty += 1;
			else iPenalty += 2; // </advc.004c>
		}
	}

	int iDistance = plotDistance(kHead.plot(), kOtherHead.plot());
	iPenalty = std::min(5, iPenalty * (1+iDistance) / iBaseScale);

	/*	For human players, use the unit order that the plot actually has,
		not the order it _should_ have.
		For AI players, use the preferred ordering, because it's slightly faster. */
	if (iDistance == 0 && !(kHead.isHuman() ?
		isBeforeGroupOnPlot(kOther) : kHead.isBeforeUnitCycle(kOtherHead)))
	{
		iPenalty += iPenalty > 0 ? 1 : 5;
	}
	return iDistance + iPenalty;
}


bool CvSelectionGroup::isFull() /* advc: */ const
{
	if(getNumUnits() <= 0)
		return false;

	// do two passes, the first pass, we ignore units with special cargo
	int iSpecialCargoCount = 0;
	int iCargoCount = 0;

	// first pass, count but ignore special cargo units
	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		if (pUnit->cargoSpace() > 0)
			iCargoCount++;
		if (pUnit->specialCargo() != NO_SPECIALUNIT)
			iSpecialCargoCount++;
		else if (!pUnit->isFull())
			return false;
	}

	/*	if every unit in the group has special cargo, then check those,
		otherwise, consider ourselves full */
	if (iSpecialCargoCount >= iCargoCount)
	{
		FOR_EACH_UNIT_IN(pUnit, *this)
		{
			if (!pUnit->isFull())
				return false;
		}
	}
	return true;
}


bool CvSelectionGroup::hasCargo() const
{
	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		if (pUnit->hasCargo())
			return true;
	}
	return false;
}

int CvSelectionGroup::getCargo() const
{
	int iCargoCount = 0;
	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		iCargoCount += pUnit->getCargo();
	}
	return iCargoCount;
}

// advc.102b: Cargo capacity, whether used or not.
int CvSelectionGroup::getCargoSpace() const
{
	int iSpace = 0;
	FOR_EACH_UNIT_IN(pUnit, *this)
		iSpace += pUnit->cargoSpace();
	return iSpace;
}

// K-Mod:
int CvSelectionGroup::cargoSpaceAvailable(SpecialUnitTypes eSpecialCargo,
	DomainTypes eDomainCargo) const
{
	int iSpace = 0;
	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		iSpace += pUnit->cargoSpaceAvailable(eSpecialCargo, eDomainCargo);
	}
	return iSpace;
}


bool CvSelectionGroup::canAllMove() const
{
	if(getNumUnits() <= 0)
		return false;
	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		if (!pUnit->canMove())
			return false;
	}
	return true;
}


bool CvSelectionGroup::canAnyMove() const
{
	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		if (pUnit->canMove())
			return true;
	}
	return false;
}

/*	K-Mod. Originally, there there was a function called CvUnit::canCargoAllMove,
	which only checked the cargo of that particular unit.
	I've removed that function and replaced it with this one,
	which checks the cargo of the entire group. */
bool CvSelectionGroup::canCargoAllMove() const
{
	FOR_EACH_UNIT_IN(pUnit, getPlot())
	{
		if (pUnit->isCargo() && pUnit->getTransportUnit()->getGroup() == this &&
			pUnit->getDomainType() == DOMAIN_LAND && !pUnit->canMove())
		{
			return false;
		}
	}
	return true;
}


bool CvSelectionGroup::hasMoved() const
{
	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		if (pUnit->hasMoved())
			return true;
	}
	return false;
}


bool CvSelectionGroup::canEnterTerritory(TeamTypes eTeam, bool bIgnoreRightOfPassage) const
{
	if(getNumUnits() <= 0)
		return false;
	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		if (!pUnit->canEnterTerritory(eTeam, bIgnoreRightOfPassage))
			return false;
	}
	return true;
}

bool CvSelectionGroup::canEnterArea(TeamTypes eTeam, CvArea const& kArea,
	bool bIgnoreRightOfPassage) const
{
	if(getNumUnits() <= 0)
		return false;
	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		if (!pUnit->canEnterTerritory(eTeam, bIgnoreRightOfPassage, &kArea))
			return false;
	}
	return true;
}


bool CvSelectionGroup::canMoveInto(CvPlot const& kPlot, bool bAttack) const
{
	if(getNumUnits() <= 0)
		return false;
	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		if (pUnit->canMoveInto(kPlot, bAttack))
			return true;
	}
	return false;
}


bool CvSelectionGroup::canMoveOrAttackInto(CvPlot const& kPlot, bool bDeclareWar,
	bool bCheckMoves, bool bAssumeVisible) const // K-Mod
{
	if (getNumUnits() <= 0)
		return false;
	bool const bVisible = (bAssumeVisible || kPlot.isVisible(getHeadTeam())); // K-Mod
	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		//if (pUnit->canMoveOrAttackInto(pPlot, bDeclareWar))
		if ((!bCheckMoves || pUnit->canMove()) && // K-Mod
			(bVisible ? pUnit->canMoveOrAttackInto(kPlot, bDeclareWar) :
			pUnit->canMoveInto(kPlot, false, bDeclareWar, false, false)))
		{
			return true;
		}
	}
	return false;
}


bool CvSelectionGroup::canMoveThrough(CvPlot const& kPlot, bool bDeclareWar, bool bAssumeVisible) const
{
	if (getNumUnits() <= 0)
		return false;
	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		//if (!pUnit->canMoveThrough(kPlot))
		if (!pUnit->canMoveInto(kPlot, false, bDeclareWar, true, bAssumeVisible)) // K-Mod
			return false;
	}
	return true;
}


bool CvSelectionGroup::canFight() /* advc: */ const
{
	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		if (pUnit->canFight())
			return true;
	}
	return false;
}


bool CvSelectionGroup::canDefend() /* advc: */ const
{
	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		if (pUnit->canDefend())
			return true;
	}
	return false;
}

bool CvSelectionGroup::canBombard(CvPlot const& kPlot) const
{
	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		if (pUnit->canBombard(kPlot))
			return true;
	}
	return false;
}

int CvSelectionGroup::visibilityRange() const // advc: const; return type was bool
{
	int iMaxRange = 0;
	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		iMaxRange = std::max(iMaxRange, pUnit->visibilityRange());
	}
	return iMaxRange;
}

// BETTER_BTS_AI_MOD, 08/19/09, jdog5000 (General AI):
bool CvSelectionGroup::canMoveAllTerrain() const
{
	//PROFILE_FUNC();
	/*  <advc.opt> This function doesn't get called often, but I guess that could
		change. Make sure not to waste time checking for an unused ability. */
	if (!CvUnitInfo::canAnyMoveAllTerrain())
		return false; // </advc.opt>
	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		if (!pUnit->canMoveAllTerrain())
			return false;
	}
	return true;
}


void CvSelectionGroup::unloadAll()
{
	FOR_EACH_UNIT_VAR_IN(pUnit, *this)
	{
		if (pUnit != NULL)
			pUnit->unloadAll();
		else FAssertMsg(pUnit != NULL, "Can this happen?"); // advc.test
	}
}


bool CvSelectionGroup::alwaysInvisible() const
{
	//PROFILE_FUNC(); // advc.003o
	if(getNumUnits() <= 0)
		return false;
	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		if (!pUnit->alwaysInvisible())
			return false;
	}
	return true;
}


bool CvSelectionGroup::isInvisible(TeamTypes eTeam) const
{
	if(getNumUnits() <= 0)
		return false;
	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		if (!pUnit->isInvisible(eTeam, false))
			return false;
	}
	return true;
}


int CvSelectionGroup::countNumUnitAIType(UnitAITypes eUnitAI) const
{
	FAssert(headUnitNode() != NULL);
	// count all units if NO_UNITAI passed in
	if (eUnitAI == NO_UNITAI) // advc.opt: Don't need a loop for that
		return getNumUnits();
	int iCount = 0;
	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		if (pUnit->AI_getUnitAIType() == eUnitAI)
			iCount++;
	}
	return iCount;
}


bool CvSelectionGroup::hasWorker() const
{
	return (countNumUnitAIType(UNITAI_WORKER) > 0 ||
			countNumUnitAIType(UNITAI_WORKER_SEA) > 0);
}

// advc.153: Essentially replacing the above, which remains exposed to Python.
bool CvSelectionGroup::hasWorkerWithMoves() const
{
	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		if (pUnit->isWorker() && pUnit->canMove())
			return true;
	}
	return false;
}


bool CvSelectionGroup::IsSelected() const
{
	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		if (pUnit->IsSelected())
			return true;
	}
	return false;
}


void CvSelectionGroup::NotifyEntity(MissionTypes eMission)
{
	FOR_EACH_UNIT_VAR_IN(pUnit, *this)
	{
		pUnit->NotifyEntity(eMission);
	}
}


void CvSelectionGroup::airCircle(bool bStart)
{
	FOR_EACH_UNIT_VAR_IN(pUnit, *this)
	{
		pUnit->airCircle(bStart);
	}
}


void CvSelectionGroup::setBlockading(bool bStart)
{
	FOR_EACH_UNIT_VAR_IN(pUnit, *this)
	{
		pUnit->setBlockading(bStart);
	}
}


int CvSelectionGroup::getX() const
{
	CvUnit const* pHeadUnit = getHeadUnit();
	if (pHeadUnit != NULL)
		return pHeadUnit->getX();
	return INVALID_PLOT_COORD;
}


int CvSelectionGroup::getY() const
{
	CvUnit const* pHeadUnit = getHeadUnit();
	if (pHeadUnit != NULL)
		return pHeadUnit->getY();
	return INVALID_PLOT_COORD;
}


CvPlot* CvSelectionGroup::plot() const
{
	CvUnit const* pHeadUnit = getHeadUnit();
	if (pHeadUnit != NULL)
		return pHeadUnit->plot();
	return NULL;
}

// advc: Shouldn't be needed
/*CvArea const& CvSelectionGroup::getArea() const
{
	CvUnit* pHeadUnit = getHeadUnit();
	if (pHeadUnit != NULL)
		return pHeadUnit->getArea().getID();
	return FFreeList::INVALID_INDEX; // advc.001: was NULL
}*/

CvArea* CvSelectionGroup::area() const
{
	CvUnit const* pHeadUnit = getHeadUnit();
	if (pHeadUnit != NULL)
		return pHeadUnit->area();
	return NULL;
}


DomainTypes CvSelectionGroup::getDomainType() const
{
	CvUnit const* pHeadUnit = getHeadUnit();
	if (pHeadUnit != NULL)
		return pHeadUnit->getDomainType();
	return NO_DOMAIN;
}


RouteTypes CvSelectionGroup::getBestBuildRoute(CvPlot const& kPlot,
	BuildTypes* peBestBuild) const
{
	PROFILE_FUNC();

	if (peBestBuild != NULL)
		*peBestBuild = NO_BUILD;

	int iBestValue = 0;
	RouteTypes eBestRoute = NO_ROUTE;

	// doc: keep existing routes
	if (kPlot.getRouteType() != NO_ROUTE)
	{
		eBestRoute = kPlot.getRouteType();
		iBestValue = GC.getInfo(eBestRoute).getValue();
	}

	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		FOR_EACH_ENUM(Build)
		{
			RouteTypes const eRoute = GC.getInfo(eLoopBuild).getRoute();
			if (eRoute == NO_ROUTE)
				continue;
			if (pUnit->canBuild(kPlot, eLoopBuild))
			{
				int iValue = GC.getInfo(eRoute).getValue();
				if (iValue > iBestValue)
				{
					iBestValue = iValue;
					eBestRoute = eRoute;
					if (peBestBuild != NULL)
						*peBestBuild = eLoopBuild;
				}
			}
		}
	}
	return eBestRoute;
}

// Returns true if attack was made...
bool CvSelectionGroup::groupAttack(int iX, int iY, MovementFlags eFlags,
	bool& bFailedAlreadyFighting, // advc (note): out-parameter
	bool bMaxSurvival) // advc.048
{
	PROFILE_FUNC();

	CvPlot* pDestPlot = &GC.getMap().getPlot(iX, iY); // (advc: plot has to exist)

	FAssert(!isBusy()); // K-Mod

	// K-Mod. Rather than clearing the existing path data; use a temporary pathfinder.
	//GroupPathFinder finalPath;
	GroupPathFinder& kFinalPath = getClearPathFinder(); // advc.opt
	kFinalPath.setGroup(*this, eFlags & ~MOVE_DECLARE_WAR);
	/*if (eFlags & MOVE_THROUGH_ENEMY) {
		if (generatePath(plot(), pDestPlot, eFlags))
			pDestPlot = getPathFirstPlot();
	}*/ // BtS
	// K-Mod
	if (eFlags & (MOVE_THROUGH_ENEMY | MOVE_ATTACK_STACK) && !(eFlags & MOVE_DIRECT_ATTACK))
	{
		if (kFinalPath.generatePath(*pDestPlot))
			pDestPlot = &kFinalPath.getPathFirstPlot();
	} // K-Mod end

	if (getNumUnits() <= 0)
		return false; // advc
	if(getDomainType() != DOMAIN_AIR && stepDistance(plot(), pDestPlot) != 1)
		return false; // advc
	bool bAttack = false;
	//if ((eFlags & MOVE_DIRECT_ATTACK) || (getDomainType() == DOMAIN_AIR) || (eFlags & MOVE_THROUGH_ENEMY) || (generatePath(plot(), pDestPlot, eFlags) && (getPathFirstPlot() == pDestPlot)))
	// K-Mod.
	if (eFlags & (MOVE_THROUGH_ENEMY | MOVE_ATTACK_STACK | MOVE_DIRECT_ATTACK) ||
		getDomainType() == DOMAIN_AIR || (kFinalPath.generatePath(*pDestPlot) &&
		&kFinalPath.getPathFirstPlot() == pDestPlot)) // K-Mod end
	{
		int iAttackOdds;
		CvUnit* pBestAttackUnit = AI().AI_getBestGroupAttacker(pDestPlot, true, iAttackOdds);
		if (pBestAttackUnit == NULL)
			return false; // advc
		/*	K-Mod, bugfix. This needs to happen before hasDefender,
			since hasDefender tests for war..
			(note: this check is no longer going to be important at all
			once my new AI DOW code is complete.) */
		/*if (groupDeclareWar(pDestPlot))
			return true;*/
		// K-Mod end

		// if there are no defenders, do not attack
		/*CvUnit* pBestDefender = pDestPlot->getBestDefender(NO_PLAYER, getOwner(), pBestAttackUnit, true);
		if (NULL == pBestDefender)
			return false;*/ // BtS
		// Lead From Behind by UncutDragon
		if (!pDestPlot->hasDefender(false, NO_PLAYER, getOwner(), pBestAttackUnit, true))
			return false;

		//bool bNoBlitz = (!pBestAttackUnit->isBlitz() || !pBestAttackUnit->isMadeAttack());
		/*  advc.164: This looks OK - exclude units that have made
			at least 1 attack. Just for clarity: */
		bool bBlitz = (pBestAttackUnit->isBlitz() && pBestAttackUnit->isMadeAttack());
		/*if (groupDeclareWar(pDestPlot))
			return true; */ // K-Mod, moved up.
		while (true)
		{
			pBestAttackUnit = AI().AI_getBestGroupAttacker(pDestPlot, false,
					iAttackOdds, false, /* advc.164: */ !bBlitz,
					!bMaxSurvival, bMaxSurvival); // advc.048
			if (pBestAttackUnit == NULL)
				break;

			// advc.048: AI_getBestGroupSacrifice moved into AI_getBestGroupAttacker

			bAttack = true;

			if (GC.getPythonCaller()->doCombat(*this, *pDestPlot))
				break;
			// advc.004c: Don't always treat air attacks like stack attacks
			bool bStack = //getDomainType() == DOMAIN_AIR ||
					GET_PLAYER(getOwner()).isHumanOption(PLAYEROPTION_STACK_ATTACK);
			bFailedAlreadyFighting = false;
			if (getNumUnits() > 1)
			{	/*if (pBestAttackUnit->getPlot().isFighting() || pDestPlot->isFighting())
					bFailedAlreadyFighting = true;
				else pBestAttackUnit->attack(pDestPlot, bStack);*/ // BtS
				// K-Mod
				if (pBestAttackUnit->getPlot().isFighting() || pDestPlot->isFighting())
					bFailedAlreadyFighting = true;
				//if (!pBestAttackUnit->isInCombat())
				FAssert(!pBestAttackUnit->isInCombat());
				// we need to issue the attack order to start the attack
				bool bIntercepted=false; // advc.004c
				pBestAttackUnit->attack(pDestPlot, bStack ||
						// advc.004c: Set bQuick for air attacks - as in Bts/K-Mod.
						getDomainType() == DOMAIN_AIR, &bIntercepted);
				// K-Mod end
				// <advc.004c> Treat air combat like stack attack unless intercepted
				if (!bStack && isHuman() && getDomainType() == DOMAIN_AIR && !bIntercepted &&
					/*	(Works when playing w/o quick combat. Perhaps superfluous now
						that I've implemented the bIntercepted param for quick combat.) */
					!pBestAttackUnit->isInAirCombat())
				{
					bStack = true;
				} // </advc.004c>
			}
			else
			{	// K-Mod note. We should do this even if the fight can't happen right away.
				pBestAttackUnit->attack(pDestPlot, false);
				break;
			}
			if (bFailedAlreadyFighting || !bStack)
			{
				if (!isHuman() && getNumUnits() > 1 &&
					// K-Mod: AI stack: follow through with the attack to the end
					!(eFlags & MOVE_SINGLE_ATTACK))
				{	//AI_queueGroupAttack(iX, iY);
					AI().AI_queueGroupAttack(pDestPlot->getX(), pDestPlot->getY()); // K-Mod
				}
				break;
			}
		}
	}
	return bAttack;
}


void CvSelectionGroup::groupMove(CvPlot* pPlot, bool bCombat, CvUnit* pCombatUnit, bool bEndMove)
{
	//PROFILE_FUNC();

	FAssert(!isBusy()); // K-Mod
	CvPlot const& kFrom = getPlot(); // advc.139

	// K-Mod. Some variables to help us regroup appropriately if not everyone can move.
	CvSelectionGroup* pBehindGroup = NULL;
	CvSelectionGroup* pBehindGroupCannotMove = NULL; // advc.153
	UnitAITypes eHeadAI = getHeadUnitAIType();
	// <advc.153>
	bool const bAIControl = isAIControlled();
	/*	True forces the join-pBehindGroup branch in the loop below to be taken.
		Caveat: A player option for this will probably work in multiplayer, but
		a BUG option won't unless a parameter is added to CvNetPushMission and
		passed along through a bunch of function calls. */
	bool const bGroupAdvance = (!bCombat || bAIControl);
	// </advc.153>

	/*	Move the combat unit first, so that no-capture units
		don't get unnecessarily left behind. */
	if (pCombatUnit != NULL)
		pCombatUnit->move(*pPlot, true);
	// K-Mod end

	/*  advc.001: Units that can't capture cities move in stage 1 (i.e. always last).
		This allows other units to capture an empty city, and then all units can
		advance as one group. Relevant when attacking with a Gunship grouped
		together with weaker units. (pCombatUnit is then NULL.)
		CvUnit::updateCombat may still unselect the no-capture unit through
		checkRemoveSelectionAfterAttack. This could be fixed, but doesn't seem worth
		the trouble.
		K-Mod 1.45 has rewritten this function, which may fix the problem (and some others too),
		but then I'd also have to merge the K-Mod fix for the Gunship city capture bug ... */
	for (int iStage = 0; iStage < 2; iStage++)
	{	// <advc.153>
		if (!bGroupAdvance && iStage >= 1)
			break; // </advc.153>
		FOR_EACH_UNIT_VAR_IN(pUnit, *this)
		{
			//if ((pUnit->canMove() && ((bCombat && (!pUnit->isNoCapture() || !pPlot->isEnemyCity(*pUnit))) ? pUnit->canMoveOrAttackInto(pPlot) : pUnit->canMoveInto(pPlot))) || pUnit == pCombatUnit)
			// K-Mod
			if (pUnit == pCombatUnit)
				continue; // this unit is moved before the loop
			// <advc.001>
			if (pUnit->isNoCityCapture() == (iStage == 0))
				continue; // </advc.001>
			if (/* advc.153: */ bGroupAdvance &&
				pUnit->canMove() &&
				/*  advc.001: This condition was removed in K-Mod 1.44 but is needed
					b/c canMoveOrAttackInto doesn't cover it (perhaps it should). */
				!(pUnit->isNoCityCapture() && pUnit->isEnemyCity(*pPlot)) &&
				(bCombat ? pUnit->canMoveOrAttackInto(*pPlot) : pUnit->canMoveInto(*pPlot)))
			{
				pUnit->move(*pPlot, true);
			}
			else
			{
				/*pUnit->joinGroup(NULL, true);
				pUnit->ExecuteMove(((float)(GC.getInfo(MISSION_MOVE_TO).getTime() * gDLL->getMillisecsPerTurn())) / 1000.0f, false);*/ // BtS

				/*	K-Mod. all units left behind should stay in the same group.
					(unless it would mean a change of group AI)
					(Note: it is important that units left behind are not in the original group.
					The later code assumes that the original group has moved,
					and if it hasn't, there will be an infinite loop.) */
				if (pBehindGroup != NULL &&
					(bGroupAdvance || bAIControl || pUnit->canMove()) && // advc.153
					(!bAIControl || pBehindGroup->getHeadUnitAIType() == eHeadAI))
				{
					pUnit->joinGroup(pBehindGroup, true);
				}  // <advc.153>
				else if (!bGroupAdvance &&
					pBehindGroupCannotMove != NULL && !bAIControl && !pUnit->canMove())
				{
					pUnit->joinGroup(pBehindGroupCannotMove, true);
				}
				else if (!bGroupAdvance &&
					pBehindGroupCannotMove == NULL && !bAIControl && !pUnit->canMove())
				{
					pUnit->joinGroup(NULL, true);
					pBehindGroupCannotMove = pUnit->getGroup();
				} // </advc.153>
				else
				{
					pUnit->joinGroup(NULL, true);
					pBehindGroup = pUnit->getGroup();
				}
				// K-Mod end
			}
			/*	K-Mod. If the unit is no longer in the original group;
				then display it's movement animation now.
				(this replaces the ExecuteMove line commented out in the above block,
				and it also handles the case of loading units onto boats.) */
			if (pUnit->getGroupID() != getID())
			{
				pUnit->ExecuteMove((GC.getInfo(MISSION_MOVE_TO).getTime() *
						gDLL->getMillisecsPerTurn()) / 1000.0f, false);
			} // K-Mod end
		}
	}

	//execute move
	if (bEndMove || !canAllMove())
	{
		// <advc.139>
		if (isHuman() && getNumUnits() > 1)
		{
			PlayerTypes const eGroupOwner = getOwner();
			PlayerTypes const eFromOwner = kFrom.getOwner();
			PlayerTypes const eToOwner = pPlot->getOwner();
			if (eFromOwner != NO_PLAYER &&
				GET_TEAM(eFromOwner).isAtWar(TEAMID(eGroupOwner)))
				GET_PLAYER(eFromOwner).AI_humanEnemyStackMovedInTerritory(kFrom, *pPlot);
			if (eToOwner != NO_PLAYER &&
				GET_TEAM(eToOwner).isAtWar(TEAMID(eGroupOwner)) &&
				eToOwner != eFromOwner)
			{
				GET_PLAYER(eToOwner).AI_humanEnemyStackMovedInTerritory(kFrom, *pPlot);
			}
		} // </advc.139>
		FOR_EACH_UNIT_VAR_IN(pUnit, *this)
		{
			pUnit->ExecuteMove((GC.getInfo(MISSION_MOVE_TO).getTime() *
					gDLL->getMillisecsPerTurn()) / 1000.0f, false);
		}
	}
}

// Returns true if move was made...
bool CvSelectionGroup::groupPathTo(int iX, int iY, MovementFlags eFlags)
{
	//GroupPathFinder finalPath; // K-Mod
	// advc.opt: Avoid allocating new memory
	GroupPathFinder& kFinalPath = getClearPathFinder();
	CvPlot const* pOriginPlot = plot(); // K-Mod

	if (at(iX, iY))
	{	// XXX is this necessary? - advc: Yes, for route-to and move-to-unit missions.
		return false;
	}
	FAssert(!isBusy());
	FAssert(getOwner() != NO_PLAYER);
	FAssert(headMissionQueueNode() != NULL);

	CvPlot& kDestPlot = GC.getMap().getPlot(iX, iY);

	//FAssertMsg(canAllMove(), "canAllMove is expected to be true");
	FAssert(getDomainType() == DOMAIN_AIR ? canAnyMove() : canAllMove()); // K-Mod

	CvPlot* pPathPlot=NULL;
	if (getDomainType() == DOMAIN_AIR)
	{
		if (!canMoveInto(kDestPlot))
			return false;
		pPathPlot = &kDestPlot;
	}
	else
	{
		/*if (!generatePath(plot(), pDestPlot, eFlags & ~MOVE_DECLARE_WAR))
			return false;
		pPathPlot = getPathFirstPlot();*/ // BtS
		/*	K-Mod. I've added & ~MOVE_DECLARE_WAR so that,
			if we need to declare war at this point and haven't yet done so,
			the move will fail here rather than splitting the group inside groupMove.
			Also, I've changed it to use a different pathfinder,
			to avoid clearing the path data - and to avoid OOS errors. */
		kFinalPath.setGroup(*this, eFlags & ~MOVE_DECLARE_WAR);
		if (!kFinalPath.generatePath(kDestPlot))
			return false;

		pPathPlot = &kFinalPath.getPathFirstPlot();
		// K-Mod end
		if (groupAmphibMove(*pPathPlot, eFlags))
			return false;
	}

	/*bool bForce = false;
	MissionAITypes eMissionAI = AI_getMissionAIType();
	if (eMissionAI == MISSIONAI_BLOCKADE || eMissionAI == MISSIONAI_PILLAGE)
		bForce = true;
	if (groupDeclareWar(pPathPlot, bForce))
		return false;*/ // BtS
	// Disabled by K-Mod. AI war decisions have no business being here.

	bool bEndMove = false;
	if(pPathPlot == &kDestPlot)
		bEndMove = true;

	//groupMove(pPathPlot, eFlags & MOVE_THROUGH_ENEMY, NULL, bEndMove);
	groupMove(pPathPlot, false, NULL, bEndMove); // K-Mod

	FAssert(getNumUnits() == 0 || atPlot(pPathPlot)); // K-Mod

	// K-Mod.
	if (!isAIControlled() && !bEndMove)
	{
		/*	If the step we just took will make us change our path to something longer,
			then cancel the move. This prevents units from wasting all their moves by
			trying to walk around enemy units. */
		FAssert(kFinalPath.isPathComplete());
		std::pair<int,int> iiOldMoves = std::make_pair(
				kFinalPath.getPathTurns(), -kFinalPath.getFinalMoves());
		if (!kFinalPath.generatePath(kDestPlot) || std::make_pair(
			kFinalPath.getPathTurns(), -kFinalPath.getFinalMoves()) > iiOldMoves)
		{
			clearMissionQueue();
		}
		/*	Also, if the step we just took causes us to backtrack -
			it's probably because we've lost vision of a unit that was blocking the path.
			Apply the MOVE_ASSUME_VISIBLE flag, so that we remember
			to go the long way around. */
		else if (&kFinalPath.getPathFirstPlot() == pOriginPlot)
			headMissionQueueNode()->m_data.eFlags |= MOVE_ASSUME_VISIBLE;
	}
	// K-Mod end

	return true;
}

// Returns true if move was made...
bool CvSelectionGroup::groupRoadTo(int iX, int iY, MovementFlags eFlags)
{
	if (!isAIControlled() || !at(iX, iY) || getLengthMissionQueue() == 1)
	{
		BuildTypes eBestBuild = NO_BUILD;
		//RouteTypes eBestRoute = // advc: unused
		getBestBuildRoute(getPlot(), &eBestBuild);
		if (eBestBuild != NO_BUILD)
		{
			groupBuild(eBestBuild);
			return true;
		}
	}
	// advc.pf: Don't want the AI to route through foreign territory
	FAssert(eFlags & MOVE_SAFE_TERRITORY);
	return groupPathTo(iX, iY, eFlags);
}


// Returns true if build should continue...
bool CvSelectionGroup::groupBuild(BuildTypes eBuild, /* advc.011b: */ bool bFinish)
{
	FAssert(getOwner() != NO_PLAYER);
	FAssertMsg(eBuild < GC.getNumBuildInfos(), "Invalid Build");

	bool bContinue = false;
	/*CvPlot* pPlot = plot();
	ImprovementTypes eImprovement = (ImprovementTypes)GC.getInfo(eBuild).getImprovement();
	if (eImprovement != NO_IMPROVEMENT) {
		if (isAIControlled()) {
			if (GET_PLAYER(getOwner()).isAutomationSafe(*pPlot)) {
					BonusTypes eBonus = (BonusTypes)pPlot->getNonObsoleteBonusType(GET_PLAYER(getOwner()).getTeam());
					if ((eBonus == NO_BONUS) || !GC.getInfo(eImprovement).isImprovementBonusTrade(eBonus)) {
						if (GC.getInfo(eImprovement).getImprovementPillage() != NO_IMPROVEMENT)
							return false;
	}}}}*/ // BtS
	/*  K-Mod. Leave old improvements should mean _all_ improvements,
		not 'unless it will connect a resource'.
		Note. The only time this bit of code might matter is if the automated unit has orders queued.
		Ideally, the AI should never issue orders which violate the leave old improvements rule. */
	CvPlot const& kPlot = getPlot();
	if (isAutomated() && GET_PLAYER(getOwner()).isAutomationSafe(kPlot) &&
		GC.getInfo(eBuild).getImprovement() != NO_IMPROVEMENT &&
		// <advc.121> Forts on unworkable tiles are OK despite SAFE_AUTOMATION.
		(!GC.getInfo(GC.getInfo(eBuild).getImprovement()).isActsAsCity() ||
		kPlot.getWorkingCity() == NULL)) // </advc.121>
	{
		FErrorMsg("AI has issued an order which violates PLAYEROPTION_SAFE_AUTOMATION");
		return false;
	}
	// K-Mod end
	bool bStopOtherWorkers = false; // advc.011c
	FOR_EACH_UNIT_VAR_IN(pUnit, *this)
	{
		FAssertMsg(pUnit->at(kPlot), "pLoopUnit is expected to be at pPlot");
		if(!pUnit->canBuild(kPlot, eBuild))
			continue;
		bContinue = true;
		if (pUnit->build(eBuild))
		{
			bContinue = false;
			break;
		}
		// advc.011c:
		if (!bFinish && isHuman() && kPlot.getBuildTurnsLeft(eBuild, getOwner()) == 1)
		{
			// <advc.011b>
			CvWString szBuild = GC.getInfo(eBuild).getDescription();
			// Get rid of the LINK tags b/c these result in an underscore
			for (int i = 0; i < 2; i++)
			{
				int posOpening = szBuild.find(L'<');
				if (posOpening == CvWString::npos)
					continue;
				int posClosing = szBuild.find(L'>');
				if (posClosing == CvWString::npos || posClosing < posOpening)
					continue;
				szBuild = (szBuild.substr(0, posOpening) +
						szBuild.substr(posClosing + 1, szBuild.length() - posClosing - 1));
			}
			CvWString szBuffer = gDLL->getText("TXT_KEY_BUILD_NOT_FINISHED", szBuild.c_str());
			gDLL->UI().addMessage(getOwner(), false, -1, szBuffer, NULL, MESSAGE_TYPE_INFO,
					GC.getInfo(eBuild).getButton()/*getHeadUnit()->getButton()*/,
					GC.getColorType("WHITE"/*"COLOR_BUILDING_TEXT"*/),
					getX(), getY(), true, false);
			// </advc.011b>
			// <advc.011c>
			bContinue = false;
			bStopOtherWorkers = true;
			break;
		}
	}
	if (bStopOtherWorkers)
	{
		FOR_EACH_UNIT_VAR_IN(pUnit, kPlot)
		{
			CvSelectionGroup* pGroup = pUnit->getGroup();
			if (pGroup != this &&
				pGroup->getOwner() == getOwner() &&
				pGroup->getActivityType() == ACTIVITY_MISSION &&
				pGroup->getLengthMissionQueue() > 0 &&
				pGroup->getMissionType(0) == GC.getInfo(eBuild).getMissionType() &&
				pGroup->getMissionData1(0) == eBuild)
			{
				pGroup->deleteMissionQueueNode(pGroup->headMissionQueueNode());
			}
		}
	} // </advc.001c>

	return bContinue;
}


void CvSelectionGroup::setTransportUnit(CvUnit* pTransportUnit,
	CvSelectionGroup** pOtherGroup) // BETTER_BTS_AI_MOD, General AI, 04/18/10, jdog5000
{
	if (pTransportUnit != NULL) // if we are loading
	{
		CvUnit* pHeadUnit = getHeadUnit();
		FAssertMsg(pHeadUnit != NULL, "non-zero group without head unit");

		int iCargoSpaceAvailable = pTransportUnit->cargoSpaceAvailable(
				pHeadUnit->getSpecialUnitType(), pHeadUnit->getDomainType());

		// if no space at all, give up
		if (iCargoSpaceAvailable < 1)
			return;

		/*	if there is space, but not enough to fit whole group,
			then split us, and set on the new group */
		if (iCargoSpaceAvailable < getNumUnits())
		{
			CvSelectionGroup* pSplitGroup = splitGroup(iCargoSpaceAvailable, NULL,
					pOtherGroup); // BETTER_BTS_AI_MOD, General AI, 04/18/10, jdog5000
			if (pSplitGroup != NULL)
				pSplitGroup->setTransportUnit(pTransportUnit);
			/*	advc.test: We shouldn't have split the group then; not sure how to
				guard against that though. Cf. issue #329 on the C2C GitHub page.
				Let's first of all see if this even occurs in AdvCiv. */
			FAssertMsg(pSplitGroup != NULL, "Probably no error but sth. to investigate");
			return;
		}

		FAssertMsg(iCargoSpaceAvailable >= getNumUnits(), "cargo size too small");

		/*	setTransportUnit removes the unit from the current group (at least currently),
			so we have to be careful in the loop here.
			so, loop until we do not load one. */
		bool bLoadedOne;
		do
		{
			bLoadedOne = false;
			// loop over all the units, finding one to load
			FOR_EACH_UNIT_VAR_IN(pLoopUnit, *this)
			{
				/*if (pLoopUnit == NULL)
					continue; */ // advc: Don't think this can (or should) happen
				/*	just in case implementation of setTransportUnit changes,
					check to make sure this unit is not already loaded */
				if (pLoopUnit->getTransportUnit() != pTransportUnit)
				{
					/*	if there is room, load the unit and stop the loop
						(since setTransportUnit ungroups this unit currently) */
					if (pTransportUnit->cargoSpaceAvailable(pLoopUnit->getSpecialUnitType(),
						pLoopUnit->getDomainType()) > 0)
					{
						pLoopUnit->setTransportUnit(pTransportUnit);
						bLoadedOne = true;
						break;
					}
				}
			}
		}
		while (bLoadedOne);
	}
	else // otherwise we are unloading
	{
		FOR_EACH_UNIT_VAR_IN(pLoopUnit, *this)
		{
			/*if (pLoopUnit == NULL)
				continue; */ // advc: Don't think this can (or should) happen
			pLoopUnit->setTransportUnit(NULL); // unload unit
		}
	}
}

bool CvSelectionGroup::isAmphibPlot(CvPlot const* pPlot) const
{
	//PROFILE_FUNC(); // advc (Not called all that frequently)
	CvUnit const* pUnit = getHeadUnit();
	if (pUnit == NULL)
		return false;
	if (pUnit->getDomainType() != DOMAIN_SEA)
		return false;
	//if (pPlot->isFriendlyCity(*pUnit, true))
	if (pUnit->isRevealedPlotValid(*pPlot)) // advc
		return false;
	// BETTER_BTS_AI_MOD, General AI, 04/18/10, jdog5000: START
	if (pPlot->isCity() &&
		(pPlot->isCoastalLand() || pPlot->isWater() || canMoveAllTerrain()))
	{
		return true;
	} // BETTER_BTS_AI_MOD: END
	return (pPlot->isCoastalLand() && !canMoveAllTerrain());
}

// Returns true if attempted an amphib landing...
bool CvSelectionGroup::groupAmphibMove(CvPlot const& kPlot, MovementFlags eFlags)
{
	bool bLanding = false;

	FAssert(getOwner() != NO_PLAYER);

	/*if (groupDeclareWar(pPlot))
		return true;*/
	/*	K-Mod. I've disabled this BtS groupDeclareWar for a bunch of reasons.
		Suffice to say, it shouldn't be here. */

	if (isAmphibPlot(&kPlot))
	{
		if (stepDistance(getX(), getY(), kPlot.getX(), kPlot.getY()) == 1)
		{
			/*	K-Mod: I've rearranged some stuff in the following section to fix a bug.
				originally, the cargo groups loop was done for each cargo-carrying unit -
				which is incorrect. */
			std::vector<CvSelectionGroup*> apCargoGroups;
			FOR_EACH_UNIT_IN(pTransport, *this)
			{
				if (!pTransport->hasCargo() || pTransport->domainCargo() != DOMAIN_LAND)
					continue;
				std::vector<CvUnit*> apCargoUnits;
				pTransport->getCargoUnits(apCargoUnits);
				for (size_t i = 0; i < apCargoUnits.size(); ++i)
				{
					CvSelectionGroup* pGroup = apCargoUnits[i]->getGroup();
					if (std::find(apCargoGroups.begin(), apCargoGroups.end(), pGroup) ==
						apCargoGroups.end())
					{
						apCargoGroups.push_back(apCargoUnits[i]->getGroup());
					}
				}
			}
			for (size_t i = 0; i < apCargoGroups.size(); ++i)
			{
				CvSelectionGroup& kCargoGroup = *apCargoGroups[i];
				if (kCargoGroup.canAllMove())
				{
					FAssert(!kCargoGroup.at(kPlot));
					kCargoGroup.pushMission(MISSION_MOVE_TO, kPlot.getX(), kPlot.getY(),
							MOVE_IGNORE_DANGER | eFlags);
					bLanding = true;
				}
			}
			// K-Mod end
		}
	}

	return bLanding;
}


bool CvSelectionGroup::readyToSelect(bool bAny)
{
	return (readyToMove(bAny) && !isAutomated());
}


bool CvSelectionGroup::readyToMove(bool bAny) /* advc: */ const
{
	//return (((bAny) ? canAnyMove() : canAllMove()) && (headMissionQueueNode() == NULL) && (getActivityType() == ACTIVITY_AWAKE) && !isBusy() && !isCargoBusy());
	// K-Mod:
	return (bAny ? canAnyMove() : canAllMove()) &&
			(isForceUpdate() ||
			(headMissionQueueNode() == NULL && getActivityType() == ACTIVITY_AWAKE)) &&
			!isBusy() && !isCargoBusy();
}


bool CvSelectionGroup::readyToAuto() /* advc: */ const
{
	//return (canAllMove() && (headMissionQueueNode() != NULL));
	return (readyForMission() ||
			(isAutomated() && getActivityType() == ACTIVITY_AWAKE && canAllMove()));
}

/*	K-Mod. In the original code, there was an implicit assumption
	that all missions required "canAllMove".
	I've removed that assumption by creating a pair of new functions:
	CvSelectionGroup::canDoMission, which returns true if the group is capable of
	executing a particular mission - including an optional movement points check.
	CvSelectionGroup::readyForMission, which basically just calls canDoMission
	for the current mission, as direct replacement for the canAllMove condition.
	(canStartMission now calls canDoMission.) */
bool CvSelectionGroup::readyForMission() const
{
	if (headMissionQueueNode() == NULL)
		return false;

	MissionData& kData = headMissionQueueNode()->m_data;

	// direct attack is a special case...    sorry about that.
	bool bCheckMoves = true;

	if (kData.eMissionType == MISSION_MOVE_TO && (kData.eFlags & MOVE_DIRECT_ATTACK))
	{
		if (canAnyMove())
			bCheckMoves = false;
		else return false;
	}

	return (canDoMission(kData.eMissionType, kData.iData1, kData.iData2, plot(),
			false, bCheckMoves) || canAllMove());
	/*	note: if the whole group can move, but they can't do the mission,
		then the mission will be canceled inside CvSelectionGroup::continueMission. */
}


bool CvSelectionGroup::canDoMission(MissionTypes eMission, int iData1, int iData2,
	CvPlot const* pPlot, bool bTestVisible, bool bCheckMoves) const
{
	if (pPlot == NULL)
		pPlot = plot();
	bool bValid = false;

	FOR_EACH_UNIT_IN(pUnit, *this)
	{
		switch (eMission)
		{
		case MISSION_MOVE_TO:
			if (!bValid)
			{
				if (pPlot->at(iData1, iData2))
					return false;
				if (!bCheckMoves)
					return true;
				if (pUnit->getDomainType() != DOMAIN_AIR)
					bValid = true; // air units don't have to move as a group
			}
			if (pUnit->canMove() != bValid)
				return !bValid; // huh?
			break;

		case MISSION_ROUTE_TO:
			if (!bValid)
			{
				if (pPlot->at(iData1, iData2) &&
					getBestBuildRoute(*pPlot) == NO_ROUTE)
				{
					return false;
				}
				if (!bCheckMoves)
					return true;
				bValid = true;
			}
			if (!pUnit->canMove())
				return false;
			break;

		case MISSION_MOVE_TO_UNIT:
		{
			FAssert(iData1 > NO_PLAYER);
			CvUnit* pTargetUnit = GET_PLAYER((PlayerTypes)iData1).getUnit(iData2);
			if (!bValid)
			{
				if (!pTargetUnit || pTargetUnit->atPlot(pPlot))
					return false;
				if (!bCheckMoves)
					return true;
				bValid = true;
			}
			if (!pUnit->canMove())
				return false;
			break;
		}

		case MISSION_SKIP:
			if (pUnit->canHold(pPlot))
				return true;
			break;

		case MISSION_SLEEP:
			if (pUnit->canSleep(pPlot))
				return true;
			break;

		case MISSION_FORTIFY:
			if (pUnit->canFortify(pPlot))
				return true;
			break;

		case MISSION_AIRPATROL:
			if (pUnit->canAirPatrol(pPlot) &&
				(!bCheckMoves || pUnit->canMove()))
			{
				// note: this mission will automatically ungroup any unsuitable units.
				return true;
			}
			break;

		case MISSION_SEAPATROL:
			if (!bValid && pUnit->canSeaPatrol(pPlot, true))
			{
				if (!bCheckMoves)
					return true;
				bValid = true;
			}
			if (!pUnit->canMove())
				return false;
			break;
		case MISSION_HEAL:
			if (pUnit->canHeal(pPlot) &&
				// advc.004l: AI control check only for performance
				(isAIControlled() || !pUnit->canSentryHeal(pPlot)))
			{
				return true;
			}
			break;
		// <advc.004l> Make the two heal missions mutually exclusive (for humans)
		case MISSION_SENTRY_HEAL:
			if(pUnit->canHeal(pPlot) && pUnit->canSentryHeal(pPlot))
				return true;
			break;
		// </advc.004l>
		case MISSION_SENTRY:
			if (pUnit->canSentry(pPlot))
				return true;
			break;

		case MISSION_AIRLIFT:
			if (pUnit->canAirliftAt(pPlot, iData1, iData2) &&
				(!bCheckMoves || pUnit->canMove()))
			{
				return true;
			}
			break;

		case MISSION_NUKE:
			if (pUnit->canNukeAt(*pPlot, iData1, iData2,
				pUnit->getTeam()) && // kekm.7 (advc)
				(!bCheckMoves || pUnit->canMove()))
			{
				return true;
			}
			break;

		case MISSION_RECON:
			if (pUnit->canReconAt(pPlot, iData1, iData2) &&
				(!bCheckMoves || pUnit->canMove()))
			{
				return true;
			}
			break;

		case MISSION_PARADROP:
			if (pUnit->canParadropAt(pPlot, iData1, iData2) &&
				(!bCheckMoves || pUnit->canMove()))
			{
				// note: this mission will automatically ungroup any unsuitable units.
				return true;
			}
			break;

		case MISSION_AIRBOMB:
			if (pUnit->canAirBombAt(GC.getMap().getPlot(iData1, iData2), pPlot) &&
				(!bCheckMoves || pUnit->canMove()))
			{
				return true;
			}
			break;

		case MISSION_BOMBARD:
			if (pUnit->canBombard(*pPlot) &&
				(!bCheckMoves || pUnit->canMove()))
			{
				return true;
			}
			break;

		case MISSION_RANGE_ATTACK:
			if (pUnit->canRangeStrikeAt(pPlot, iData1, iData2) &&
				(!bCheckMoves || pUnit->canMove()))
			{
				return true;
			}
			break;

		case MISSION_PLUNDER:
			if (pUnit->canPlunder(*pPlot, bTestVisible) &&
				/*  advc.001: Replacing the clause below. The bug occurred when
					a player set a unit to Blockade (=plunder), spending all its
					movement points, and then clicking on the Blockade button
					again. The unit then stopped blockading. Not sure if this
					is the best way to fix it, but it least it works: Hides the
					Blockade button when a unit has no moves left. */
				pUnit->canMove())
				//(!bCheckMoves || pLoopUnit->canMove()))
			{
				return true;
			}
			break;

		case MISSION_PILLAGE:
			if (pUnit->canPillage(*pPlot) &&
				(!bCheckMoves || pUnit->canMove()))
			{
				return true;
			}
			break;

		case MISSION_SABOTAGE:
			if (pUnit->canSabotage(pPlot, bTestVisible) &&
				(!bCheckMoves || pUnit->canMove()))
			{
				return true;
			}
			break;

		case MISSION_DESTROY:
			if (pUnit->canDestroy(pPlot, bTestVisible) &&
				(!bCheckMoves || pUnit->canMove()))
			{
				return true;
			}
			break;

		case MISSION_STEAL_PLANS:
			if (pUnit->canStealPlans(pPlot, bTestVisible) &&
				(!bCheckMoves || pUnit->canMove()))
			{
				return true;
			}
			break;

		case MISSION_FOUND:
			if (pUnit->canFound(pPlot, bTestVisible) &&
				(!bCheckMoves || pUnit->canMove()))
			{
				return true;
			}
			break;

		case MISSION_SPREAD:
			if (pUnit->canSpread(pPlot, (ReligionTypes)iData1, bTestVisible) &&
				(!bCheckMoves || pUnit->canMove()))
			{
				return true;
			}
			break;

		case MISSION_SPREAD_CORPORATION:
			if (pUnit->canSpreadCorporation(
				pPlot, (CorporationTypes)iData1, bTestVisible) &&
				(!bCheckMoves || pUnit->canMove()))
			{
				return true;
			}
			break;

		case MISSION_JOIN:
			if (pUnit->canJoin(pPlot, (SpecialistTypes)iData1) &&
				(!bCheckMoves || pUnit->canMove()))
			{
				return true;
			}
			break;

		case MISSION_CONSTRUCT:
			if (pUnit->canConstruct(
				pPlot, (BuildingTypes)iData1, bTestVisible) &&
				(!bCheckMoves || pUnit->canMove()))
			{
				return true;
			}
			break;

		case MISSION_DISCOVER:
			if (pUnit->canDiscover(pPlot) &&
				(!bCheckMoves || pUnit->canMove()))
			{
				return true;
			}
			break;

		case MISSION_HURRY:
			if (pUnit->canHurry(pPlot, bTestVisible) &&
				(!bCheckMoves || pUnit->canMove()))
			{
				return true;
			}
			break;

		case MISSION_TRADE:
			if (pUnit->canTrade(pPlot, bTestVisible) &&
				(!bCheckMoves || pUnit->canMove()))
			{
				return true;
			}
			break;

		case MISSION_GREAT_WORK:
			if (pUnit->canGreatWork(pPlot) &&
				(!bCheckMoves || pUnit->canMove()))
			{
				return true;
			}
			break;

		case MISSION_INFILTRATE:
			if (pUnit->canInfiltrate(pPlot, bTestVisible) &&
				(!bCheckMoves || pUnit->canMove()))
			{
				return true;
			}
			break;

		case MISSION_GOLDEN_AGE:
			if (iData1 != -1) // this means to play the animation only
				return true;
			if (pUnit->canGoldenAge(pPlot, bTestVisible) &&
				(!bCheckMoves || pUnit->canMove()))
			{
				return true;
			}
			break;

		case MISSION_BUILD:
		{
			BuildTypes eBuild = (BuildTypes)iData1;
			FAssertEnumBounds(eBuild);
			if (pUnit->canBuild(*pPlot, eBuild, bTestVisible) &&
				(!bCheckMoves || pUnit->canMove()))
			{
				return true;
			}
			break;
		}
		case MISSION_LEAD:
			if (pUnit->canLead(pPlot, iData1) &&
				(!bCheckMoves || pUnit->canMove()))
			{
				return true;
			}
			break;

		case MISSION_ESPIONAGE:
			if (pUnit->canEspionage(pPlot, bTestVisible) &&
				(!bCheckMoves || pUnit->canMove()))
			{
				return true;
			}
			break;

		case MISSION_DIE_ANIMATION:
			return false;
			break;

		case MISSION_BEGIN_COMBAT:
		case MISSION_END_COMBAT:
		case MISSION_AIRSTRIKE:
			/*	note: airstrike missions are actually done using MISSION_MOVE_TO.
				This mission is apparently only used for graphics. */
		case MISSION_SURRENDER:
		case MISSION_IDLE:
		case MISSION_DIE:
		case MISSION_DAMAGE:
		case MISSION_MULTI_SELECT:
		case MISSION_MULTI_DESELECT:
			break;

		default:
			FAssert(false);
			break;
		}
	}

	return bValid;
}
// K-Mod end

void CvSelectionGroup::setID(int iID)
{
	m_iID = iID;
}


TeamTypes CvSelectionGroup::getTeam() const
{
	if (getOwner() != NO_PLAYER)
		return GET_PLAYER(getOwner()).getTeam();
	return NO_TEAM;
}


int CvSelectionGroup::getMissionTimer() const
{
	return m_iMissionTimer;
}


void CvSelectionGroup::setMissionTimer(int iNewValue)
{
	FAssert(getOwner() != NO_PLAYER);

	m_iMissionTimer = iNewValue;
	FAssert(getMissionTimer() >= 0);
}


void CvSelectionGroup::changeMissionTimer(int iChange)
{
	setMissionTimer(getMissionTimer() + iChange);
}


void CvSelectionGroup::updateMissionTimer(int iSteps,  // advc: refactored
	CvPlot* pFromPlot) // advc.102
{
	CvGame const& kGame = GC.getGame();
	if (headMissionQueueNode() == NULL ||
		(!isHuman() && (!showMoves( // <advc.102>
		pFromPlot == NULL ? getPlot() : *pFromPlot) ||
		/*	(showMoves returning true means that simultaneous turns
			aren't a concern) */
		gDLL->getEngineIFace()->isGlobeviewUp()))) // </advc.102>
	{
		setMissionTimer(0);
		return;
	}
	int iTime = GC.getInfo((MissionTypes)
			headMissionQueueNode()->m_data.eMissionType).getTime();
	if ((headMissionQueueNode()->m_data.eMissionType == MISSION_MOVE_TO) ||
		(headMissionQueueNode()->m_data.eMissionType == MISSION_ROUTE_TO) ||
		(headMissionQueueNode()->m_data.eMissionType == MISSION_MOVE_TO_UNIT))
	{
		CvPlot* pTargetPlot = NULL;
		if (headMissionQueueNode()->m_data.eMissionType == MISSION_MOVE_TO_UNIT)
		{
			CvUnit* pTargetUnit = GET_PLAYER((PlayerTypes)headMissionQueueNode()->m_data.iData1).
					getUnit(headMissionQueueNode()->m_data.iData2);
			if (pTargetUnit != NULL)
				pTargetPlot = pTargetUnit->plot();
		}
		else
		{
			pTargetPlot = GC.getMap().plot(headMissionQueueNode()->m_data.iData1,
					headMissionQueueNode()->m_data.iData2);
		}
		if (atPlot(pTargetPlot))
			iTime += iSteps;
		else iTime = std::min(iTime, 2);
	}
	if (isHuman() &&
		(isAutomated() ||
		GET_PLAYER(kGame.isNetworkMultiPlayer() ? getOwner() : kGame.getActivePlayer()).
		isOption(PLAYEROPTION_QUICK_MOVES)))
	{
		iTime = std::min(iTime, 1);
	}
	setMissionTimer(iTime);
}

// K-Mod. this is what force update use to do - but I don't use it like this anymore.
/*void CvSelectionGroup::doForceUpdate() {
	if (isForceUpdate()) {
		setForceUpdate(false);
		clearMissionQueue();
		setActivityType(ACTIVITY_AWAKE);
		// if we are in the middle of attacking with a stack, cancel it
		AI_cancelGroupAttack();
	}
}*/ // K-Mod end

void CvSelectionGroup::setActivityType(ActivityTypes eNewValue)
{
	FAssert(getOwner() != NO_PLAYER);

	ActivityTypes const eOldActivity = getActivityType();
	if(eOldActivity == eNewValue)
		return;

	if (eOldActivity == ACTIVITY_INTERCEPT)
		airCircle(false);

	setBlockading(false);
	bool bWasWaiting = isWaiting(); // K-Mod
	m_eActivityType = eNewValue;

	// K-Mod
	if (bWasWaiting && !isWaiting())
		GET_PLAYER(getOwner()).updateGroupCycle(*this);
	// K-Mod end

	if (getActivityType() == ACTIVITY_INTERCEPT)
		airCircle(true);

	CvPlot* pPlot = plot();
	if (getActivityType() != ACTIVITY_MISSION)
	{
		if (getActivityType() != ACTIVITY_INTERCEPT)
		{
			FOR_EACH_UNIT_VAR_IN(pUnit, *this)
			{
				pUnit->NotifyEntity(MISSION_IDLE); // don't idle intercept animation
			}
		}
		if (isActiveTeam())
		{
			if (pPlot != NULL) // advc (note): This can occur
				pPlot->setFlagDirty(true);
		}
	}
	if (pPlot == gDLL->UI().getSelectionPlot() /* advc.opt: (?) */ && pPlot != NULL)
	{
		gDLL->UI().setDirty(PlotListButtons_DIRTY_BIT, true);
		gDLL->UI().setDirty(SelectionButtons_DIRTY_BIT, true);
	}
}


void CvSelectionGroup::setAutomateType(AutomateTypes eNewValue)
{
	FAssert(getOwner() != NO_PLAYER);
	FAssertMsg(isHuman() || eNewValue == NO_AUTOMATE, "AI shouldn't use automation");

	if (getAutomateType() == eNewValue)
		return;

	m->eAutomateType = eNewValue;
	clearMissionQueue();
	setActivityType(ACTIVITY_AWAKE);

	if (eNewValue != NO_AUTOMATE)
		return;
	CvPlot* pPlot = plot();
	if (pPlot == NULL) // advc (note): This can occur
		return;

	// If canceling automation, cancel on cargo as well.
	FOR_EACH_UNIT_VAR_IN(pCargoUnit, *pPlot)
	{
		CvUnit* pTransportUnit = pCargoUnit->getTransportUnit();
		if (pTransportUnit != NULL && pTransportUnit->getGroup() == this)
		{
			pCargoUnit->getGroup()->setAutomateType(NO_AUTOMATE);
			pCargoUnit->getGroup()->setActivityType(ACTIVITY_AWAKE);
		}
	}
}

// Disabled by K-Mod. (This function is deprecated.)
/*FAStarNode* CvSelectionGroup::getPathLastNode() const {
	//return pathFinder().GetEndNode();
	//return gDLL->getFAStarIFace()->GetLastNode(&GC.getPathFinder());
}*/


CvPlot& CvSelectionGroup::getPathFirstPlot() const
{
	return pathFinder().getPathFirstPlot();
}


CvPlot& CvSelectionGroup::getPathEndTurnPlot() const
{
	return pathFinder().getPathEndTurnPlot();
}


bool CvSelectionGroup::generatePath(CvPlot const& kFrom, CvPlot const& kTo,
	MovementFlags eFlags, bool bReuse, int* piPathTurns, int iMaxPath,
	bool bUseTempFinder) const // advc.128
{
	PROFILE_FUNC();
	/*	K-Mod - if I can stop the UI from messing with this pathfinder,
		I might be able to reduce OOS bugs.
		advc.706 (note): Can trigger after defeat of active player in R&F game.
		advc.128: MAX_MOVES: The AI may use this function to anticipate human moves. */
	FAssert(isAIControlled() || (eFlags & MOVE_MAX_MOVES));
	// <advc.128>
	FAssert(!bUseTempFinder || !bReuse);
	/*	Not getClearPathFinder -- want bTempFinder to work correctly even when called
		while generating a path. */
	GroupPathFinder tempFinder;
	GroupPathFinder& kPathFinder = (bUseTempFinder ? tempFinder : pathFinder());
	// </advc.128>
	/*if (!bReuse)
		pathFinder().Reset();*/
	kPathFinder.setGroup(*this, eFlags, iMaxPath);
	bool bSuccess = kPathFinder.generatePath(kFrom, kTo);
	/*if (!bUseTempFinder && bSuccess != gDLL->getFAStarIFace()->GeneratePath(&GC.getPathFinder(), pFromPlot->getX(), pFromPlot->getY(), pToPlot->getX(), pToPlot->getY(), false, eFlags, bReuse)) {
		pNode = gDLL->getFAStarIFace()->GetLastNode(&GC.getPathFinder());
		if (bSuccess || iMaxPath < 0 || !pNode || pNode->m_iData2 <= iMaxPath) {
			//::MessageBoxA(NULL,"pathfind mismatch","CvGameCore",MB_OK);
			FAssert(false);
		}
	}*/ // test (K-Mod)

	if (piPathTurns != NULL)
	{
		*piPathTurns = MAX_INT;
		if (bSuccess)
			*piPathTurns = kPathFinder.getPathTurns();
	}

	return bSuccess;
}


void CvSelectionGroup::clearUnits()
{
	for (CLLNode<IDInfo>* pNode = headUnitNode(); pNode != NULL;
		pNode = deleteUnitNode(pNode))
	{} // advc
}


// Returns true if the unit is added...
bool CvSelectionGroup::addUnit(CvUnit* pUnit, bool bMinimalChange)
{
	//PROFILE_FUNC();
	if (!pUnit->canJoinGroup(pUnit->plot(), this))
		return false;

	bool bAdded = false;

	/*	K-Mod. Start the air circling animation if required.
		(CvSelectionGroup::joinGroup will interupt the air patrol mission anyway.) */
	/*if (getActivityType() == ACTIVITY_INTERCEPT)
		pUnit->airCircle(true);*/ // disabled for now b/c it results in jerky animations.
	// K-Mod end
	{
		CLLNode<IDInfo>* pUnitNode = headUnitNode();
		while (pUnitNode != NULL)
		{
			CvUnitAI const& kLoopUnit = *::AI_getUnit(pUnitNode->m_data);
			CvUnitAI const& kUnit = pUnit->AI(); // advc.003u

			if (kUnit.AI_groupFirstVal() > kLoopUnit.AI_groupFirstVal() ||
				(kUnit.AI_groupFirstVal() == kLoopUnit.AI_groupFirstVal() &&
				kUnit.AI_groupSecondVal() > kLoopUnit.AI_groupSecondVal()))
			{
				m_units.insertBefore(pUnit->getIDInfo(), pUnitNode);
				bAdded = true;
				break;
			}
			pUnitNode = nextUnitNode(pUnitNode);
		}
	}
	if (!bAdded)
		m_units.insertAtEnd(pUnit->getIDInfo());

	if(!bMinimalChange && getOwner() == NO_PLAYER && getNumUnits() > 0)
	{
		FOR_EACH_UNIT_VAR_IN(pLoopUnit, *this)
		{	//if (pUnitNode != headUnitNode()) // (advc: commented out by the BtS expansion)
			pLoopUnit->NotifyEntity(MISSION_MULTI_SELECT);
		}
	}

	return true;
}


void CvSelectionGroup::removeUnit(CvUnit* pUnit)
{
	CLLNode<IDInfo>* pUnitNode;
	pUnitNode = headUnitNode();
	while (pUnitNode != NULL)
	{
		if (::getUnit(pUnitNode->m_data) == pUnit)
		{
			// K-Mod. Cancel the air circling animation.
			if (getActivityType() == ACTIVITY_INTERCEPT)
				pUnit->airCircle(false);
			// K-Mod end
			deleteUnitNode(pUnitNode);
			break;
		}
		else pUnitNode = nextUnitNode(pUnitNode);
	}
}


CLLNode<IDInfo>* CvSelectionGroup::deleteUnitNode(CLLNode<IDInfo>* pNode)
{
	CLLNode<IDInfo>* pNextUnitNode;
	if (getOwner() != NO_PLAYER)
	{
		setAutomateType(NO_AUTOMATE);
		clearMissionQueue();

		switch (getActivityType())
		{
		case ACTIVITY_SLEEP:
		case ACTIVITY_INTERCEPT:
		case ACTIVITY_PATROL:
		case ACTIVITY_PLUNDER:
		case ACTIVITY_BOARDED: // advc.075
			break;
		default:
			setActivityType(ACTIVITY_AWAKE);
			break;
		}
	}
	pNextUnitNode = m_units.deleteNode(pNode);
	return pNextUnitNode;
}


void CvSelectionGroup::mergeIntoGroup(CvSelectionGroup* pSelectionGroup)
{
	/*	merge groups, but make sure we do not change the head unit AI
		this means that if a new unit is going to become the head,
		change its AI to match, if possible.
		AI_setUnitAIType removes the unit from the current group (at least currently),
		so we have to be careful in the loop here.
		so loop until we have not changed unit AIs. */
	bool bChangedUnitAI;
	do
	{
		bChangedUnitAI = false;
		/*	loop over all the units, moving them to the new group,
			stopping if we had to change a unit AI, because doing so
			removes that unit from our group, so we have to start over. */
		FOR_EACH_UNITAI_VAR_IN(pUnit, *this)
		{
			if (pUnit == NULL)
				continue;
			UnitAITypes const eUnitAI = pUnit->AI_getUnitAIType();
			/*	if the unitAIs are different, and the loop unit has a higher val,
				then the group unitAI would change.
				change this UnitAI to the old group UnitAI if possible. */
			CvUnit const* pNewHeadUnit = pSelectionGroup->getHeadUnit();
			UnitAITypes eNewHeadUnitAI = pSelectionGroup->getHeadUnitAIType();
			if (pNewHeadUnit!= NULL && eUnitAI != eNewHeadUnitAI &&
				pUnit->AI_groupFirstVal() > pNewHeadUnit->AI().AI_groupFirstVal())
			{
				/*	non-zero AI_unitValue means that this UnitAI is valid for this unit
					(that is the check used everywhere) */
				if (GET_PLAYER(getOwner()).AI_unitValue(
					pUnit->getUnitType(), eNewHeadUnitAI, NULL) > 0)
				{
					// this will remove pLoopUnit from the current group
					pUnit->AI_setUnitAIType(eNewHeadUnitAI);
					bChangedUnitAI = true;
					break;
				}
			}
			pUnit->joinGroup(pSelectionGroup);
		}
	}
	while (bChangedUnitAI);
}

/*  split this group into two new groups, one of iSplitSize,
	the other the remaining units.
	split up each unit AI type as evenly as possible. */
/*  K-Mod. I've rewritten most of this function. The new version is faster,
	gives a more even split, and does not create a dummy group.
	(unless I've made a mistake.) */
CvSelectionGroup* CvSelectionGroup::splitGroup(int iSplitSize,
	CvUnit* pNewHeadUnit, CvSelectionGroup** ppOtherGroup)
{
	FAssert(pNewHeadUnit == 0 || pNewHeadUnit->getGroup() == this);

	if (iSplitSize <= 0)
	{
		FErrorMsg("non-positive splitGroup size");
		return NULL;
	}

	// are we already small enough?
	if (getNumUnits() <= iSplitSize)
		return this;

	CvUnit* pOldHeadUnit = getHeadUnit();
	/*	if pNewHeadUnit NULL, then we will use our current head
		to head the new split group of target size */
	if (pNewHeadUnit == NULL)
		pNewHeadUnit = pOldHeadUnit;

	UnitAITypes eOldHeadAI = pOldHeadUnit->AI_getUnitAIType();
	UnitAITypes eNewHeadAI = pNewHeadUnit->AI_getUnitAIType();

	int iGroupSize = getNumUnits();

	EagerEnumMap<UnitAITypes,int> aiTotalAIs;
	EagerEnumMap<UnitAITypes,int> aiNewGroupAIs;
	FAssert(iGroupSize > 0);

	// populate 'aiTotalAIs' with the number of each AI type in the existing group.
	FOR_EACH_UNIT_IN(pLoopUnit, *this)
		aiTotalAIs.add(pLoopUnit->AI_getUnitAIType(), 1);

	/*	Next, from those numbers, work out how many of each unit type we need in new group.
		round evenly, and carry the rounding-error onto the next unit type
		so that we don't have an off-by-one error at the end. */
	int iCarry = 0;

	/*	There are a couple of special cases that we need to do first
		(so that iCarry can work correctly at the end) */
	{
		/*	reserve a unit of the old AI type to lead the remainder group
			and more importantly, reserve a unit of the new AI type to lead the new group! */
		int iNew = std::max(1, // advc: Renamed this variable from "x"
				(aiTotalAIs.get(eNewHeadAI) * iSplitSize + iGroupSize/2 + iCarry) / iGroupSize);
		if (eOldHeadAI == eNewHeadAI)
		{
			if (iNew > 1 && aiTotalAIs.get(eOldHeadAI) == iNew)
				iNew--;

			iCarry += aiTotalAIs.get(eNewHeadAI) * iSplitSize - iNew * iGroupSize;
			aiNewGroupAIs.set(eNewHeadAI, iNew);
		}
		else
		{
			iCarry += aiTotalAIs.get(eNewHeadAI) * iSplitSize - iNew * iGroupSize;
			aiNewGroupAIs.set(eNewHeadAI, iNew);

			iNew = (aiTotalAIs.get(eOldHeadAI) * iSplitSize +
					iGroupSize/2 + iCarry) / iGroupSize;
			if (iNew > 0 && aiTotalAIs.get(eOldHeadAI) == iNew)
				iNew--;

			iCarry += aiTotalAIs.get(eOldHeadAI) * iSplitSize - iNew * iGroupSize;
			aiNewGroupAIs.set(eOldHeadAI, iNew);
		}
	}

	FOR_EACH_ENUM2(UnitAI, eAI)
	{
		if (aiTotalAIs.get(eAI) == 0 || eAI == eNewHeadAI || eAI == eOldHeadAI)
			continue; // already done. (see above)

		int iNew = (aiTotalAIs.get(eAI) * iSplitSize + iGroupSize/2 + iCarry) / iGroupSize;
		/*	In rare situations iNew can be rounded up above the maximum,
			because iCarry may oversized if one of the original head units is reserved. */
		iNew = std::min(iNew, aiTotalAIs.get(eAI));
		FAssert(iNew >= 0 && iNew <= aiTotalAIs.get(eAI));

		iCarry += aiTotalAIs.get(eAI) * iSplitSize - iNew * iGroupSize;
		aiNewGroupAIs.set(eAI, iNew);
		FAssert(iCarry >= -iGroupSize && iCarry <= iGroupSize);
	}
	FAssert(iCarry == 0);

	// make the new group for the new head
	pNewHeadUnit->joinGroup(NULL);
	CvSelectionGroup* pSplitGroup = pNewHeadUnit->getGroup();
	aiNewGroupAIs.add(eNewHeadAI, -1);
	aiTotalAIs.add(eNewHeadAI, -1);
	CvSelectionGroup* pRemainderGroup = this;

	/*	Populate the new group with the quantity of AI types specified in aiNewGroupAIs.
		However, the units of each AI type should not simply be taken from the
		front of the list, because we always want to have an even distribution
		of unit types. (not just unitAI types) */
	FOR_EACH_UNIT_VAR_IN(pLoopUnit, *this)
	{
		UnitAITypes const eAI = pLoopUnit->AI_getUnitAIType();
		FAssert(eAI != NO_UNITAI);
		if (aiNewGroupAIs.get(eAI) > 0)
		{
			if (iGroupSize * aiNewGroupAIs.get(eAI) >= iSplitSize * aiTotalAIs.get(eAI))
			{
				pLoopUnit->joinGroup(pSplitGroup);
				aiNewGroupAIs.add(eAI, -1);
				FAssert(aiNewGroupAIs.get(eAI) >= 0);
			}
		}
		/*	(note. this isn't really important if aiNewGroupAIs[eAI] == 0;
			but we might as well keep it accurate anyway.) */
		aiTotalAIs.add(eAI, -1);
		FAssert(aiTotalAIs.get(eAI) >= 0);
	}

	FAssert(pSplitGroup->getNumUnits() == iSplitSize);

	/*	K-Mod. if the remainder group doesn't have the same unitAI,
		then it should be split up, so that we don't get any strange groups forming.
		Note: the force split can be overridden by the calling function if need be. */
	if (pRemainderGroup != NULL)
	{
		CvSelectionGroupAI& kRemainderGroup = pRemainderGroup->AI(); // advc.003u
		/*  <advc.706> Uncommented this old K-Mod code b/c my splitGroup(1) calls
			failed the FAssert below. */
		if (GC.getGame().isOption(GAMEOPTION_RISE_FALL) &&
			kRemainderGroup.getHeadUnitAIType() != eOldHeadAI)
		{
			kRemainderGroup.AI_setForceSeparate();
		} // </advc.706>
		// this should now be automatic, because of my other edits.
		FAssert(kRemainderGroup.getHeadUnitAIType() == eOldHeadAI || kRemainderGroup.AI_isForceSeparate());
	} // K-Mod end

	if (ppOtherGroup != NULL)
		*ppOtherGroup = pRemainderGroup;

	return pSplitGroup;
}

/*	K-Mod: If the group has units of different plots,
	this function will create one new group for each of those plots */
void CvSelectionGroup::regroupSeparatedUnits()
{
	CvUnit const* pHeadUnit = getHeadUnit();
	// the AI doesn't like to stay grouped when the group's AI type had changed.
	UnitAITypes eHeadUnitAI = getHeadUnitAIType();
	std::vector<CvSelectionGroup*> new_groups;

	FAssert(pHeadUnit != NULL || headUnitNode() == NULL);
	FOR_EACH_UNIT_VAR_IN(pLoopUnit, *this)
	{
		if (pLoopUnit->at(pHeadUnit->getPlot()))
			continue;
		bool bFoundGroup = false;
		for (size_t i = 0; !bFoundGroup && i < new_groups.size(); i++)
		{
			if (pLoopUnit->plot() == new_groups[i]->plot())
			{
				if (isHuman() || new_groups[i]->getHeadUnitAIType() == eHeadUnitAI)
					pLoopUnit->joinGroup(new_groups[i], true);
				else pLoopUnit->joinGroup(0, true);
				bFoundGroup = true;
			}
		}
		if (!bFoundGroup)
		{
			pLoopUnit->joinGroup(0, true);
			new_groups.push_back(pLoopUnit->getGroup());
		}
	}
}

/*	Returns the zero-based index of the unit within the group
	or -1 if it is not in the group */
int CvSelectionGroup::getUnitIndex(CvUnit* pUnit, int iMaxIndex) const
{
	int iIndex = 0;
	// <advc.opt> (I think the EXE only uses iMaxIndex>=0)
	if (iMaxIndex < 0)
	{
		FOR_EACH_UNIT_IN(pLoopUnit, *this)
		{
			if (pLoopUnit == pUnit)
				return iIndex;
			iIndex++;
		}
	}
	else // </advc.opt>
	{
		FOR_EACH_UNIT_IN(pLoopUnit, *this)
		{
			if (pLoopUnit == pUnit)
				return iIndex;
			iIndex++;
			// early out if not interested beyond maxIndex
			if (/*iMaxIndex >= 0 &&*/ iIndex >= iMaxIndex) // advc.opt
				return -1;
		}
	}
	return -1;
}

// <advc.003s>
// advc.003u (note): Two more duplicates of this in CvSelectionGroupAI (AI_getHeadUnit)
CvUnit const* CvSelectionGroup::getHeadUnit() const
{
	CLLNode<IDInfo> const* pNode = headUnitNode();
	return (pNode != NULL ? ::getUnit(pNode->m_data) : NULL);
}


CvUnit* CvSelectionGroup::getHeadUnit()
{
	CLLNode<IDInfo>* pNode = headUnitNode();
	return (pNode != NULL ? ::getUnit(pNode->m_data) : NULL);
}


CvUnit* CvSelectionGroup::getHeadUnitExternal() const
{
	CLLNode<IDInfo> const* pNode = headUnitNode();
	return (pNode != NULL ? ::getUnit(pNode->m_data) : NULL);
}


CLLNode<IDInfo>* CvSelectionGroup::headUnitNodeExternal() const
{
	return m_units.head();
}


CLLNode<IDInfo>* CvSelectionGroup::nextUnitNodeExternal(CLLNode<IDInfo>* pNode) const
{
	return m_units.next(pNode);
} // </advc.003s>


CvUnit* CvSelectionGroup::getUnitAt(int iIndex) const
{
	FAssertBounds(0, getNumUnits(), iIndex);
	CLLNode<IDInfo> const* pUnitNode = headUnitNode();
	for (int i = 0; i < iIndex; i++)
		pUnitNode = nextUnitNode(pUnitNode);
	return ::getUnit(pUnitNode->m_data);
}


UnitAITypes CvSelectionGroup::getHeadUnitAIType() const
{
	CvUnit const* pHeadUnit = getHeadUnit();
	if (pHeadUnit != NULL)
		return pHeadUnit->AI_getUnitAIType();
	return NO_UNITAI;
}


PlayerTypes CvSelectionGroup::getHeadOwner() const
{
	CvUnit const* pHeadUnit = getHeadUnit();
	if (pHeadUnit != NULL)
		return pHeadUnit->getOwner();
	return NO_PLAYER;
}


TeamTypes CvSelectionGroup::getHeadTeam() const
{
	CvUnit const* pHeadUnit = getHeadUnit();
	if (pHeadUnit != NULL)
	{
		//return pHeadUnit->getTeam();
		// advc.opt: Not nice, but avoids a function call.
		return TEAMID(pHeadUnit->getOwner());
	}
	return NO_TEAM;
}


void CvSelectionGroup::clearMissionQueue()
{
	FAssert(getOwner() != NO_PLAYER);

	deactivateHeadMission();
	m_missionQueue.clear();
	if (isActiveOwned() && IsSelected())
	{
		gDLL->UI().setDirty(Waypoints_DIRTY_BIT, true);
		gDLL->UI().setDirty(SelectionButtons_DIRTY_BIT, true);
		gDLL->UI().setDirty(InfoPane_DIRTY_BIT, true);
	}
}


MissionData* CvSelectionGroup::getMissionFromQueue(int iIndex) const
{
	CLLNode<MissionData>* pMissionNode;
	pMissionNode = m_missionQueue.nodeNum(iIndex);
	if (pMissionNode != NULL)
		return &(pMissionNode->m_data);
	return NULL;
}


void CvSelectionGroup::insertAtEndMissionQueue(MissionData mission, bool bStart)
{
	//PROFILE_FUNC();
	FAssert(getOwner() != NO_PLAYER);

	m_missionQueue.insertAtEnd(mission);
	if (getLengthMissionQueue() == 1 && bStart)
		activateHeadMission();

	if (isActiveOwned() && IsSelected())
	{
		gDLL->UI().setDirty(Waypoints_DIRTY_BIT, true);
		gDLL->UI().setDirty(SelectionButtons_DIRTY_BIT, true);
		gDLL->UI().setDirty(InfoPane_DIRTY_BIT, true);
	}
}


CLLNode<MissionData>* CvSelectionGroup::deleteMissionQueueNode(CLLNode<MissionData>* pNode)
{
	FAssert(pNode != NULL);
	FAssert(getOwner() != NO_PLAYER);

	if (pNode == headMissionQueueNode())
		deactivateHeadMission();

	CLLNode<MissionData>* pNextMissionNode = m_missionQueue.deleteNode(pNode);

	/*if (pNextMissionNode == headMissionQueueNode())
		activateHeadMission();*/ // BtS
	/*	Disabled by K-Mod. It should be possible to delete the head mission
		without immediately starting the next one! */

	if (isActiveOwned() && IsSelected())
	{
		gDLL->UI().setDirty(Waypoints_DIRTY_BIT, true);
		gDLL->UI().setDirty(SelectionButtons_DIRTY_BIT, true);
		gDLL->UI().setDirty(InfoPane_DIRTY_BIT, true);
	}

	return pNextMissionNode;
}


MissionTypes CvSelectionGroup::getMissionType(int iNode) const
{
	int iCount = 0;
	CLLNode<MissionData>* pMissionNode = headMissionQueueNode();
	while (pMissionNode != NULL)
	{
		if (iNode == iCount)
			return pMissionNode->m_data.eMissionType;
		iCount++;
		pMissionNode = nextMissionQueueNode(pMissionNode);
	}
	return NO_MISSION;
}


int CvSelectionGroup::getMissionData1(int iNode) const
{
	int iCount = 0;
	CLLNode<MissionData>* pMissionNode = headMissionQueueNode();
	while (pMissionNode != NULL)
	{
		if (iNode == iCount)
			return pMissionNode->m_data.iData1;
		iCount++;
		pMissionNode = nextMissionQueueNode(pMissionNode);
	}
	return -1;
}


int CvSelectionGroup::getMissionData2(int iNode) const
{
	int iCount = 0;
	CLLNode<MissionData>* pMissionNode = headMissionQueueNode();
	while (pMissionNode != NULL)
	{
		if (iNode == iCount)
			return pMissionNode->m_data.iData2;
		iCount++;
		pMissionNode = nextMissionQueueNode(pMissionNode);
	}
	return -1;
}

// <advc.075>
void CvSelectionGroup::handleBoarded()
{
	if (!isHuman() || getDomainType() != DOMAIN_SEA ||
		GET_PLAYER(getOwner()).isOption(PLAYEROPTION_NO_UNIT_CYCLING))
	{
		return;
	}
	CLLNode<MissionData>* pMissionNode = headMissionQueueNode();
	if (pMissionNode == NULL)
	{
		FAssert(pMissionNode != NULL); // MOVE_TO mission should still be queued
		return;
	}
	if (nextMissionQueueNode(pMissionNode) != NULL)
		return;
	if (movesLeft() || !hasMoved())
		return;
	CvPlot const& kAt = getPlot();
	if(kAt.isWater() && !kAt.isAdjacentToLand())
		return;

	std::vector<CvSelectionGroup*> apLandCargoGroups;
	getLandCargoGroups(apLandCargoGroups);
	std::vector<CvSelectionGroup*> aAwake;
	for (size_t i = 0; i < apLandCargoGroups.size(); i++)
	{
		CvSelectionGroup& kGroup = *apLandCargoGroups[i];
		if(kGroup.getActivityType() == ACTIVITY_BOARDED && kGroup.canDisembark())
			aAwake.push_back(&kGroup);
	} // Putting all awoken units in one group should be more convenient
	if (!aAwake.empty())
		aAwake[0]->setActivityType(ACTIVITY_AWAKE);
	for (size_t i = 1; i < aAwake.size(); i++) {
		if (aAwake[i]->getDomainType() == aAwake[0]->getDomainType())
			aAwake[i]->mergeIntoGroup(aAwake[0]);
		// One of the doDelayedDeath calls will clean the empty groups up
	}
}


bool CvSelectionGroup::canDisembark() const
{
	if (!getPlot().isWater() && movesLeft())
		return true;
	FOR_EACH_ADJ_PLOT(getPlot())
	{
		if (canMoveOrAttackInto(*pAdj, false, true, false))
			return true;
	}
	return false;
}


void CvSelectionGroup::resetBoarded()
{
	if (!isHuman() || getDomainType() != DOMAIN_SEA ||
		GET_PLAYER(getOwner()).isOption(PLAYEROPTION_NO_UNIT_CYCLING))
	{
		return;
	}
	std::vector<CvSelectionGroup*> apLandCargoGroups;
	getLandCargoGroups(apLandCargoGroups);
	for (size_t i = 0; i < apLandCargoGroups.size(); i++)
	{
		if(apLandCargoGroups[i]->getActivityType() == ACTIVITY_AWAKE)
			apLandCargoGroups[i]->setActivityType(ACTIVITY_BOARDED);
	}
}


void CvSelectionGroup::getLandCargoGroups(std::vector<CvSelectionGroup*>& kResult)
{
	// Akin to canCargoAllMove
	FOR_EACH_UNIT_VAR_IN(pUnit, getPlot())
	{
		if (pUnit->isCargo() && pUnit->getDomainType() == DOMAIN_LAND &&
			pUnit->getTransportUnit()->getGroup() == this)
		{
			kResult.push_back(pUnit->getGroup());
		}
	}
} // </advc.075>


void CvSelectionGroup::read(FDataStreamBase* pStream)
{
	reset(); // Init saved data

	uint uiFlag=0;
	pStream->Read(&uiFlag);

	pStream->Read(&m_iID);
	pStream->Read(&m_iMissionTimer);

	pStream->Read(&m_bForceUpdate);

	pStream->Read((int*)&m_eOwner);
	pStream->Read((int*)&m_eActivityType);
	pStream->Read((int*)&m->eAutomateType);

	m_units.Read(pStream);
	// <advc.004l>
	if(uiFlag >= 2)
		m->knownEnemies.Read(pStream); // </advc.004l>
	// <advc.011b>
	if(uiFlag <= 0)
	{
		CLinkList<MissionDataLegacy> tmp;
		tmp.Read(pStream);
		for(CLLNode<MissionDataLegacy>* pNode = tmp.head();
			pNode != NULL; pNode = tmp.next(pNode))
		{
			MissionDataLegacy tmpMission = pNode->m_data;
			MissionData mission;
			mission.bModified = false;
			mission.eMissionType = tmpMission.eMissionType;
			mission.iData1 = tmpMission.iData1;
			mission.iData2 = tmpMission.iData2;
			mission.eFlags = tmpMission.eFlags;
			mission.iPushTurn = tmpMission.iPushTurn;
			m_missionQueue.insertAtEnd(mission);
		}
	}
	else // </advc.011b>
		m_missionQueue.Read(pStream);
	// <advc.pf>
	if (uiFlag < 3)
	{	// Replace removed movement flag with SAFE_TERRITORY
		MovementFlags const MOVE_ROUTE_TO = static_cast<MovementFlags>(1 << 14);
		for (CLLNode<MissionData>* pNode = headMissionQueueNode(); pNode != NULL;
			pNode = nextMissionQueueNode(pNode))
		{
			MissionData& md = pNode->m_data;
			if (md.eMissionType == MISSION_ROUTE_TO || (md.eFlags & MOVE_ROUTE_TO))
			{
				md.eFlags |= MOVE_SAFE_TERRITORY;
				md.eFlags &= ~MOVE_ROUTE_TO;
			}
		}
	} // </advc.pf>
}


void CvSelectionGroup::write(FDataStreamBase* pStream)
{
	uint uiFlag;
	//uiFlag = 1; // advc.011b
	//uiFlag = 2; // advc.004l
	uiFlag = 3; // advc.pf (MOVE_ROUTE_TO removed)
	pStream->Write(uiFlag);
	REPRO_TEST_BEGIN_WRITE(CvString::format("SelGroup(%d,%d,%d)", getID(), getX(), getY()));
	pStream->Write(m_iID);
	pStream->Write(m_iMissionTimer);

	pStream->Write(m_bForceUpdate);

	pStream->Write(m_eOwner);
	pStream->Write(m_eActivityType);
	pStream->Write(m->eAutomateType);
	m_units.Write(pStream);
	m->knownEnemies.Write(pStream); // advc.004l
	m_missionQueue.Write(pStream);
	REPRO_TEST_END_WRITE();
}


void CvSelectionGroup::activateHeadMission()
{
	FAssert(getOwner() != NO_PLAYER);

	if (headMissionQueueNode() != NULL)
	{
		if (!isBusy())
			startMission();
	}
}


void CvSelectionGroup::deactivateHeadMission()
{
	FAssert(getOwner() != NO_PLAYER);

	if (headMissionQueueNode() != NULL)
	{
		if (getActivityType() == ACTIVITY_MISSION)
			setActivityType(ACTIVITY_AWAKE);

		setMissionTimer(0);
		/* if (isActiveOwned()) {
			if (IsSelected())
				GC.getGame().cycleSelectionGroups_delayed(1, true, canAnyMove());
		} */
	}
}
