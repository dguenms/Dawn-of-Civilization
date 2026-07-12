#include "CvGameCoreDLL.h"
#include "CvUnit.h"
#include "CvUnitAI.h"
#include "CombatOdds.h"
#include "CvSelectionGroupAI.h"
#include "CoreAI.h"
#include "CvCityAI.h"
#include "TeamPathFinder.h"
#include "UWAIAgent.h"
#include "RiseFall.h" // advc.705
#include "PlotRange.h"
#include "CvArea.h"
#include "BarbarianWeightMap.h" // advc.304
#include "CvGameTextMgr.h" // advc.048c
#include "CvInfo_Command.h"
#include "CvInfo_Terrain.h"
#include "CvInfo_GameOption.h"
#include "CvPopupInfo.h"
#include "BBAILog.h" // BETTER_BTS_AI_MOD, AI logging, 02/24/10, jdog5000
#include "CvBugOptions.h" // advc.002e
#include "CvDLLPythonIFaceBase.h" // for CvEventReporter::genericEvent


CvUnit::CvUnit() // advc.003u: Body cut from the deleted reset function
{
	createEntity(this);

	m_iID = 0;
	m_iGroupID = FFreeList::INVALID_INDEX;
	m_iHotKeyNumber = -1;
	m_iX = INVALID_PLOT_COORD;
	m_iY = INVALID_PLOT_COORD;
	updatePlot(); // advc.opt
	m_iLastMoveTurn = 0;
	m_iReconX = INVALID_PLOT_COORD;
	m_iReconY = INVALID_PLOT_COORD;
	m_iGameTurnCreated = 0;
	m_iDamage = 0;
	m_iMoves = 0;
	m_iExperience = 0;
	m_iLevel = 1;
	m_iCargo = 0;
	m_iAttackPlotX = INVALID_PLOT_COORD;
	m_iAttackPlotY = INVALID_PLOT_COORD;
	// <advc.048c>
	m_iAttackOdds = -1;
	m_iPreCombatHP = -1; // </advc.048c>
	m_iCombatTimer = 0;
	m_iCombatFirstStrikes = 0;
	m_iFortifyTurns = 0;
	m_iBlitzCount = 0;
	m_iAmphibCount = 0;
	m_iRiverCount = 0;
	m_iEnemyRouteCount = 0;
	m_iAlwaysHealCount = 0;
	m_iHillsDoubleMoveCount = 0;
	m_iImmuneToFirstStrikesCount = 0;
	m_iNoUpgradeCount = 0; // doc
	m_iExtraVisibilityRange = 0;
	m_iExtraMoves = 0;
	m_iExtraMoveDiscount = 0;
	m_iExtraAirRange = 0;
	m_iExtraIntercept = 0;
	m_iExtraEvasion = 0;
	m_iExtraFirstStrikes = 0;
	m_iExtraChanceFirstStrikes = 0;
	m_iExtraWithdrawal = 0;
	m_iExtraCollateralDamage = 0;
	m_iExtraBombardRate = 0;
	m_iExtraEnemyHeal = 0;
	m_iExtraNeutralHeal = 0;
	m_iExtraFriendlyHeal = 0;
	m_iSameTileHeal = 0;
	m_iAdjacentTileHeal = 0;
	m_iExtraCombatPercent = 0;
	m_iExtraCityAttackPercent = 0;
	m_iExtraCityDefensePercent = 0;
	m_iExtraHillsAttackPercent = 0;
	m_iExtraHillsDefensePercent = 0;
	m_iExtraPlainsAttackPercent = 0; // doc
	m_iExtraPlainsDefensePercent = 0; // doc
	m_iExtraRiverAttackPercent = 0; // doc
	m_iRevoltProtection = 0;
	m_iCollateralDamageProtection = 0;
	m_iPillageChange = 0;
	m_iUpgradeDiscount = 0;
	m_iExperiencePercent = 0;
	m_iKamikazePercent = 0;
	m_iExtraUpkeep = 0; // doc
	m_eFacingDirection = DIRECTION_SOUTH;
	m_iImmobileTimer = 0;
	m_eOriginalRegion = NO_REGION; // doc

	//m_bMadeAttack = false;
	m_iMadeAttacks = 0; // advc.164
	m_bMadeInterception = false;
	m_bPromotionReady = false;
	m_bDeathDelay = false;
	m_bCombatFocus = false;
	m_bInfoBarDirty = false;
	m_bBlockading = false;
	m_bAirCombat = false;
	m_bFlatMovement = false; // advc.opt

	m_eOwner = NO_PLAYER;
	m_eCapturingPlayer = NO_PLAYER;
	m_eUnitType = NO_UNIT;
	m_pUnitInfo = NULL;
	m_eLeaderUnitType = NO_UNIT;

	m_iBaseCombat = 0;
	m_iCargoCapacity = 0;
	m_iLastReconTurn = -1; // advc.029
}

// advc.003u: Param eUnitAI moved to CvUnitAI::init
void CvUnit::init(int iID, UnitTypes eUnit, PlayerTypes eOwner, int iX, int iY,
	DirectionTypes eFacingDirection)
{
	FAssert(NO_UNIT != eUnit);

	m_iID = iID;
	m_eUnitType = eUnit;
	m_eOwner = eOwner;
	m_eFacingDirection = eFacingDirection;
	m_pUnitInfo = &GC.getInfo(m_eUnitType);
	m_iBaseCombat = m_pUnitInfo->getCombat();
	// <advc.313>
	if (isKnownSeaBarbarian())
	{
		changeExtraMoves(GC.getInfo(GC.getGame().getHandicapType()).get(
				CvHandicapInfo::SeaBarbarianExtraMoves));
	} // </advc.313>
	updateFlatMovement(); // advc.opt
	m_iCargoCapacity = m_pUnitInfo->getCargoSpace();
	setXY(iX, iY, false, false);
	/*  advc.003u: Rest of the body moved into finalizeInit so that subclasses
		can do their init code in between */
}

// advc.opt:
void CvUnit::updateFlatMovement()
{
	m_bFlatMovement = (m_pUnitInfo->isFlatMovementCost() || getDomainType() == DOMAIN_AIR);
}


CvUnit::~CvUnit()
{
	uninitEntity();
}


void CvUnit::reloadEntity()
{
	uninitEntity();
	createEntity(this); // create and attach entity to unit
	setupGraphical();
}

// advc.003u: Body moved from reloadEntity. Comments are by Firaxis.
void CvUnit::uninitEntity()
{
	// don't need to remove entity when the app is shutting down, or crash can occur
	if (!gDLL->GetDone() && GC.IsGraphicsInitialized())
	{
		gDLL->getEntityIFace()->RemoveUnitFromBattle(this);
		removeEntity(); // remove entity from engine
	}
	destroyEntity(); // delete CvUnitEntity and detach from us
}


void CvUnit::finalizeInit() // advc.003u: Body cut from init
{
	setupGraphical();

	getPlot().updateCenterUnit();
	getPlot().setFlagDirty(true);

	CvGame& kGame = GC.getGame();
	CvPlayerAI& kOwner = GET_PLAYER(getOwner());
	/*int iCreated = kGame.getUnitCreatedCount(getUnitType()); // advc: was called "iUnitName"
	int iNumNames = m_pUnitInfo->getNumUnitNames();
	if (iCreated < iNumNames)
	{	// <advc.005b>
		//  Skip every iStep'th name on average. Basic assumption: About half of
		//	the names are used in a long (space-race) game with 7 civs; therefore,
		//	skip every iStep=2 then. Adjust this to the (current) number of civs.
		int iAlive = kGame.countCivPlayersAlive();
		if (iAlive <= 0)
		{
			FAssert(iAlive > 0);
			iAlive = 7;
		}
		int const iStep = std::max(1, intdiv::uround(14, iAlive));
		// This gives iRand an expected value of iStep
		int iRand = SyncRandNum(2 * iStep + 1);
		//	The index of the most recently used name isn't available; instead,
		//	take iStep times the number of previously used names in order to
		//	pick up roughly where we left off.
		int iOffset = iStep * iCreated + iRand;
		// That's +8 in Medieval, +16 in Renaissance and +24 in Industrial or later.
		iOffset += std::min(24, 8 * std::max(0, kGame.getStartEra() - 1));
		bool bNameSet = false;
		// If we run out of names, search backward.
		if (iOffset >= iNumNames)
		{
			//  The first couple are still somewhat random, but then just
			//	pick them chronologically.
			for (int i = iNumNames - 1 - iRand; i >= 0; i--)
			{
				CvWString szName = gDLL->getText(m_pUnitInfo->getUnitNames(i));
				// Copied from below
				if (!kGame.isGreatPersonBorn(szName))
				{
					setName(szName);
					bNameSet = true;
					kGame.addGreatPersonBornName(szName);
					break;
				}
			} // Otherwise, search forward.
		}
		if (!bNameSet) // </advc.005b>
		{
			for (int i = 0; i < iNumNames; i++)
			{
				int iIndex = (i + iOffset) % iNumNames;
				CvWString szName = gDLL->getText(m_pUnitInfo->getUnitNames(iIndex));
				if (!kGame.isGreatPersonBorn(szName))
				{
					setName(szName);
					kGame.addGreatPersonBornName(szName);
					break;
				}
			}
		}
	}*/

	setGameTurnCreated(kGame.getGameTurn());
	kGame.incrementUnitCreatedCount(getUnitType());
	UnitClassTypes eUnitClass = getUnitClassType();
	kGame.incrementUnitClassCreatedCount(eUnitClass);
	GET_TEAM(getTeam()).changeUnitClassCount(eUnitClass, 1);
	kOwner.changeUnitClassCount(eUnitClass, 1);
	kOwner.changeExtraUnitCost(m_pUnitInfo->getExtraCost());

    // doc: extra unit cost or free upkeep
    if (getExtraUpkeep() >= 0)
        kOwner.changeExtraUnitCost(getExtraUpkeep());
    else
        kOwner.changeBaseFreeMilitaryUnits(-getExtraUpkeep());

	if (isNuke())
		kOwner.changeNumNukeUnits(1);
	if (m_pUnitInfo->isMilitarySupport())
		kOwner.changeNumMilitaryUnits(1);
	kOwner.changeAssets(m_pUnitInfo->getAssetValue());
	kOwner.changePower(m_pUnitInfo->getPowerValue() /
			(getDomainType() == DOMAIN_SEA ? 2 : 1)); // advc.104e
	// advc.104: To enable more differentiated tracking of power values
	kOwner.uwai().getCache().reportUnitCreated(getUnitType());

	if (m_pUnitInfo->isAnyFreePromotions()) // advc.003t
	{
		FOR_EACH_ENUM(Promotion)
		{
			if (m_pUnitInfo->getFreePromotions(eLoopPromotion))
				setHasPromotion(eLoopPromotion, true);
		}
	}
	FAssert(GC.getNumTraitInfos() > 0);
	FOR_EACH_ENUM2(Trait, eTrait)
	{
		if (!kOwner.hasTrait(eTrait))
			continue;
		CvTraitInfo const& kTrait = GC.getInfo(eTrait);
		if (kTrait.isAnyFreePromotion()) // advc.003t
		{
			FOR_EACH_ENUM(Promotion)
			{
				if (kTrait.isFreePromotion(eLoopPromotion))
				{
					if (getUnitCombatType() != NO_UNITCOMBAT &&
						kTrait.isFreePromotionUnitCombat(getUnitCombatType()))
					{
						setHasPromotion(eLoopPromotion, true);
					}
				}
			}
		}
	}
	if (getUnitCombatType() != NO_UNITCOMBAT)
	{
		FOR_EACH_ENUM(Promotion)
		{
			if (kOwner.isFreePromotion(getUnitCombatType(), eLoopPromotion))
				setHasPromotion(eLoopPromotion, true);
		}
	}

	if (getUnitClassType() != NO_UNITCLASS)
	{
		FOR_EACH_ENUM(Promotion)
		{
			if (kOwner.isFreePromotion(getUnitClassType(), eLoopPromotion))
				setHasPromotion(eLoopPromotion, true);
		}
	}
    // doc: Spanish UP
    // TODO: setFreePromotion for player
    if (getCivilizationType() == SPAIN)
    {
        if (getUnitCombatType() == UNITCOMBAT_NAVAL)
        {
            setHasPromotion(PROMOTION_NAVIGATION1, true);
            setHasPromotion(PROMOTION_NAVIGATION2, true);
        }
    }
	if (getDomainType() == DOMAIN_LAND && baseCombatStr() > 0)
	{
		if (kGame.getBestLandUnit() == NO_UNIT || baseCombatStr() >
			kGame.getBestLandUnitCombat())
		{
			kGame.setBestLandUnit(getUnitType());
		}
	}

	if (isActiveOwned())
		gDLL->UI().setDirty(GameData_DIRTY_BIT, true);

	if (m_pUnitInfo->isWorldUnit())
	{
		for (int i = 0; i < MAX_PLAYERS; i++)
		{
			CvPlayer const& kObs = GET_PLAYER((PlayerTypes)i);
			if(!kObs.isAlive())
				continue;

			CvWString szBuffer;
			if (GET_TEAM(getTeam()).isHasMet(kObs.getTeam()) ||
				kObs.isSpectator()) // advc.127
			{
				// <advc.127b>
				int iFlashX = -1,
					iFlashY = -1;
				if(getPlot().isRevealed(kObs.getTeam(), true))
				{
					iFlashX = getX();
					iFlashY = getY();
				} // </advc.127b>
				szBuffer = gDLL->getText("TXT_KEY_MISC_SOMEONE_CREATED_UNIT",
						kOwner.getCivilizationShortDescription(), getNameKey()); // rfc
				gDLL->UI().addMessage(kObs.getID(), false, -1, szBuffer,
						"AS2D_WONDER_UNIT_BUILD", MESSAGE_TYPE_MAJOR_EVENT, getButton(),
						GC.getColorType("UNIT_TEXT"), iFlashX, iFlashY, true, true);
			}
			else
			{
				szBuffer = gDLL->getText("TXT_KEY_MISC_UNKNOWN_CREATED_UNIT", getNameKey());
				gDLL->UI().addMessage(kObs.getID(), false, -1, szBuffer,
						"AS2D_WONDER_UNIT_BUILD", MESSAGE_TYPE_MAJOR_EVENT, getButton(),
						GC.getColorType("UNIT_TEXT"));
			}
		}

		CvWString szBuffer(gDLL->getText("TXT_KEY_MISC_SOMEONE_CREATED_UNIT",
				kOwner.getCivilizationShortDescription(), getNameKey())); // rfc
		GC.getGame().addReplayMessage(getPlot(), REPLAY_MESSAGE_MAJOR_EVENT,
				kOwner.getID(), szBuffer, GC.getColorType("UNIT_TEXT"));
	}

	CvEventReporter::getInstance().unitCreated(this);
}


void CvUnit::setupGraphical() // graphical-only setup
{
	if (!GC.IsGraphicsInitialized())
		return;

	CvDLLEntity::setup();

	if (getGroup()->getActivityType() == ACTIVITY_INTERCEPT)
		airCircle(true);
}


void CvUnit::convert(CvUnit* pUnit)
{
	FOR_EACH_ENUM(Promotion)
	{
        // doc: only receives base promotions, free promotions from unit type, and leader promotion, but not other promotions from original unit
		setHasPromotion(eLoopPromotion, getUnitInfo().getFreePromotions(eLoopPromotion) ||
			isHasPromotion(eLoopPromotion) ||
			(pUnit->isHasPromotion(eLoopPromotion) && GC.getPromotionInfo(eLoopPromotion).isLeader()));
	}

	setGameTurnCreated(pUnit->getGameTurnCreated());
	setDamage(pUnit->getDamage());
	setMoves(pUnit->getMoves());
    setLeaderUnitType(pUnit->getLeaderUnitType());

    // doc: receives starting experience from previous unit relative to power difference
    int iNewExperience = pUnit->getExperience();
    int iOldModifier = std::max(1, 100 + GET_PLAYER(pUnit->getOwner()).getLevelExperienceModifier());
    int iOurModifier = std::max(1, 100 + GET_PLAYER(getOwner()).getLevelExperienceModifier());

    iNewExperience *= iOurModifier;
    iNewExperience /= iOldModifier;

    // doc: German UP and not for leaders
    if (getLeaderUnitType() == NO_UNIT && getCivilizationType() != GERMANY)
    {
        int iOldCombat = pUnit->getUnitInfo().getCombat();
        int iNewCombat = getUnitInfo().getCombat();

        if (iNewCombat > iOldCombat)
        {
            iNewExperience *= iOldCombat;
            iNewExperience /= iNewCombat;
        }
    }

    if (iNewExperience > 0)
        setExperience(iNewExperience);

	setName(pUnit->getNameNoDesc());
	setLeaderUnitType(pUnit->getLeaderUnitType());

	CvUnit* pTransportUnit = pUnit->getTransportUnit();
	/* if (pTransportUnit != NULL) {
		pUnit->setTransportUnit(NULL);
		setTransportUnit(pTransportUnit);
	} */
	// K-Mod
	if (pTransportUnit != NULL)
		pUnit->setTransportUnit(NULL);
	setTransportUnit(pTransportUnit);
	// K-Mod end

	std::vector<CvUnit*> aCargoUnits;
	pUnit->getCargoUnits(aCargoUnits);
	for (uint i = 0; i < aCargoUnits.size(); ++i)
	{	//aCargoUnits[i]->setTransportUnit(this);
		/*  UNOFFICIAL_PATCH, Bugfix, 10/30/09, Mongoose & jdog5000: START
			Check cargo types and capacity when upgrading transports (from Mongoose SDK) */
		if (cargoSpaceAvailable(aCargoUnits[i]->getSpecialUnitType(), aCargoUnits[i]->getDomainType()) > 0)
		{
			aCargoUnits[i]->setTransportUnit(this);
		}
		else
		{
			aCargoUnits[i]->setTransportUnit(NULL);
			aCargoUnits[i]->jumpToNearestValidPlot();
		}
		// UNOFFICIAL_PATCH: END
	}

	pUnit->kill(true);
}

// K-Mod. I've made some structural change to this function, for efficiency, clarity, and sanity.
void CvUnit::kill(bool bDelay, PlayerTypes ePlayer)
{
	PROFILE_FUNC();

	CvPlot const& kPlot = getPlot();
	// <advc.004h>
	if(isFound() && isHuman())
		updateFoundingBorder(true); // </advc.004h>

	FOR_EACH_UNIT_VAR_IN(pLoopUnit, kPlot)
	{
		if (pLoopUnit->getTransportUnit() == this)
		{
			//if (kPlot.isValidDomainForLocation(*pLoopUnit))
			if (pLoopUnit->isRevealedValidDomain(kPlot)) // advc
				pLoopUnit->setCapturingPlayer(NO_PLAYER);
			pLoopUnit->kill(false, ePlayer);
		}
	}
	/*	advc (note - known issue): We're not checking whether this unit was set
		as the m_missionAIUnit of a CvSelectionGroup. This becomes a problem
		only if our FFreeList ID gets assigned to a new unit. Unknown if this
		ever actually happens. Don't want to loop through all groups just in case. */

	CvPlayerAI& kOwner = GET_PLAYER(getOwner()); // advc
	if (ePlayer != NO_PLAYER)
	{
		CvEventReporter::getInstance().unitKilled(this, ePlayer);
		if (NO_UNIT != getLeaderUnitType() ||
			// <advc.004u> Treat unattached GP here too
			m_pUnitInfo->getDefaultUnitAIType() == UNITAI_GENERAL ||
			isGoldenAge()) // </advc.004u>
		{
			CvWString szBuffer;
			// advc.004u: szBuffer now set inside the loop
			//szBuffer = gDLL->getText("TXT_KEY_MISC_GENERAL_KILLED", getNameKey());
			for (PlayerIter<MAJOR_CIV> it; it.hasNext(); ++it)
			{
				CvPlayer const& kObs = *it;

                // doc: notification settings
                if (GC.getGame().isGreatPeopleNotification(kObs.getID(), getOwner()) ||
                    GC.getGame().isGreatPeopleNotification(kObs.getID(), ePlayer))
                    continue;

				ColorTypes eColor = NO_COLOR;
				TCHAR const* szSound = NULL;
				// <advc.004u>
				FAssert(kOwner.getID() != ePlayer);
				if(kObs.getID() == kOwner.getID())
				{
					szBuffer = gDLL->getText("TXT_KEY_MISC_YOUR_GENERAL_KILLED", getNameKey(),
								GET_PLAYER(ePlayer).getCivilizationShortDescription());
					eColor = GC.getColorType("RED");
					szSound = GC.getInfo(kObs.getCurrentEra()).getAudioUnitDefeatScript();
				}
				else if(kObs.getID() == ePlayer)
				{
					szBuffer = gDLL->getText("TXT_KEY_MISC_GENERAL_KILLED_BY_YOU", getNameKey(),
							kOwner.getCivilizationShortDescription());
					eColor = GC.getColorType("GREEN");
					szSound = GC.getInfo(kObs.getCurrentEra()).getAudioUnitVictoryScript();
				}
				else if(GET_TEAM(kOwner.getTeam()).isHasMet(kObs.getTeam()) || // advc.004u
					kObs.isSpectator()) // advc.127
				{
					szBuffer = gDLL->getText("TXT_KEY_MISC_GENERAL_KILLED", getNameKey(),
							kOwner.getCivilizationShortDescription(),
							GET_PLAYER(ePlayer).getCivilizationShortDescription());
					eColor = GC.getColorType("UNIT_TEXT");
					// K-Mod (the other sound is not appropriate for most civs receiving the message.)
					szSound = "AS2D_INTERCEPTED";
				}
				else continue;
				bool bRev = kPlot.isRevealed(kObs.getTeam(), true);
				// </advc.004u>
				gDLL->UI().addMessage(kObs.getID(), false, -1, szBuffer,
						szSound, // advc.004u
						MESSAGE_TYPE_MAJOR_EVENT,
						// <advc.004u> Indicate location on map
						getButton(), eColor,
						bRev ? getX() : -1, bRev ? getY() : -1, bRev, bRev);
						// </advc.004u>
			}
		}
	}

	finishMoves();

	if (bDelay)
	{
		startDelayedDeath();
		return;
	}

	if (isMadeAttack() && isNuke())
	{
		CvPlot* pTarget = getAttackPlot();
		if (pTarget != NULL)
		{
			pTarget->nukeExplosion(nukeRange(), this);
			setAttackPlot(NULL, false);
		}
	}

	if (IsSelected())
	{
		if (gDLL->UI().getLengthSelectionList() == 1)
		{
			if (!gDLL->UI().isFocused() &&
				!gDLL->UI().isCitySelection() &&
				!gDLL->UI().isDiploOrPopupWaiting())
			{
				GC.getGame().updateSelectionList();
			}
			if (IsSelected())
				GC.getGame().cycleSelectionGroups_delayed(1, false);
			else gDLL->UI().setDirty(SelectionCamera_DIRTY_BIT, true);
		}
		// advc.001: Expenses for units may change
		gDLL->UI().setDirty(GameData_DIRTY_BIT, true);
	}
	gDLL->UI().removeFromSelectionList(this);
	// XXX this is NOT a hack, without it, the game crashes.
	gDLL->getEntityIFace()->RemoveUnitFromBattle(this);

	//FAssert(!isCombat());
	/*	K-Mod. With simultaneous turns, a unit can be captured while
		trying to execute an attack order. (eg. a bomber) */
	FAssert(!isFighting());
	//FAssert(getAttackPlot() == NULL);
	FAssert(getCombatUnit() == NULL); // advc: moved up

	setTransportUnit(NULL);
	setBlockading(false);
	setReconPlot(NULL);

	UnitClassTypes eUnitClass = getUnitClassType();
	GET_TEAM(getTeam()).changeUnitClassCount(eUnitClass, -1);
	kOwner.changeUnitClassCount(eUnitClass, -1);
	kOwner.changeExtraUnitCost(-m_pUnitInfo->getExtraCost());

    // doc: extra unit cost or free upkeep
    if (getExtraUpkeep() >= 0)
        kOwner.changeExtraUnitCost(-getExtraUpkeep());
    else
        kOwner.changeBaseFreeMilitaryUnits(getExtraUpkeep());

	if (isNuke())
		kOwner.changeNumNukeUnits(-1);

	if (m_pUnitInfo->isMilitarySupport())
		kOwner.changeNumMilitaryUnits(-1);

	kOwner.changeAssets(-(m_pUnitInfo->getAssetValue()));
	kOwner.changePower(-(m_pUnitInfo->getPowerValue()
			/ (getDomainType() == DOMAIN_SEA ? 2 : 1))); // advc.104e

	// advc.104: To enable more differentiated tracking of power values
	kOwner.uwai().getCache().reportUnitDestroyed(getUnitType());

	kOwner.AI_changeNumAIUnits(AI_getUnitAIType(), -1);
	PlayerTypes const eCapturingPlayer = getCapturingPlayer();
    CivilizationTypes eCapturingCivilization = (eCapturingPlayer != NO_PLAYER) ? GET_PLAYER(eCapturingPlayer).getCivilizationType() : NO_CIVILIZATION;
	UnitTypes eCaptureUnitType = (eCapturingPlayer == NO_PLAYER ? NO_UNIT :
			getCaptureUnitType(GET_PLAYER(eCapturingPlayer).getCivilizationType()));

    // doc: Turkic UP
    if (isBarbarian() && eCapturingCivilization == TURKS && GET_TEAM(GET_PLAYER(eCapturingPlayer).getTeam()).isAtWarWithMajorPlayer())
    {
        // mounted units
        if (getUnitCombatType() == UNITCOMBAT_LIGHT_CAVALRY || getUnitCombatType() == UNITCOMBAT_HEAVY_CAVALRY)
        {
            eCaptureUnitType = getUnitType();
        }
    }

	setXY(INVALID_PLOT_COORD, INVALID_PLOT_COORD, true);
	joinGroup(NULL, false, false);
	CvEventReporter::getInstance().unitLost(this);
	kOwner.deleteUnit(getID());

    CvPlayerAI& kCaptor = GET_PLAYER(eCapturingPlayer);
	bool bCanCapture = eCapturingPlayer != NO_PLAYER &&
		eCapturingPlayer != BARBARIAN_PLAYER &&
		eCaptureUnitType != NO_UNIT;
    // doc: must be able to train captured unit
    if (bCanCapture)
    {
        UnitTypes eOwnCaptureUnitType = GC.getInfo(eCapturingCivilization).getCivilizationUnits(GC.getInfo(eCaptureUnitType).getUnitClassType());
        if (!kOwner.canTrain(eOwnCaptureUnitType))
            bCanCapture = false;
    }
    // doc: capturing civilian units requires slavery
    if (bCanCapture && GC.getInfo(eCaptureUnitType).getCombat() == 0 && !kOwner.isSlavery())
        bCanCapture = false;
    if (bCanCapture && !kCaptor.isHuman() &&
            !GC.getDefineBOOL("AI_CAN_DISBAND_UNITS") &&
            !kCaptor.AI_captureUnit(eCaptureUnitType, kPlot))
        bCanCapture = false;


	if (bCanCapture)
	{
		CvPlayerAI& kCaptor = GET_PLAYER(eCapturingPlayer);
		if (kCaptor.isHuman() ||
			kCaptor.AI_captureUnit(eCaptureUnitType, kPlot) ||
			!GC.getDefineBOOL("AI_CAN_DISBAND_UNITS"))
		{
			CvUnit* pCapturedUnit = kCaptor.initUnit(
				eCaptureUnitType, kPlot.getX(), kPlot.getY());
			if (pCapturedUnit != NULL)
			{
				CvWString szBuffer;
				if (GC.getInfo(eCaptureUnitType).getCombat() == 0)
					szBuffer = gDLL->getText("TXT_KEY_MISC_YOU_CAPTURED_UNIT",
						GC.getInfo(eCaptureUnitType).getTextKeyWide());
				// doc: Turkic UP
				else
					szBuffer = gDLL->getText("TXT_KEY_MISC_UNIT_JOINED_YOU",
						GC.getUnitInfo(eCaptureUnitType).getTextKeyWide());
				gDLL->UI().addMessage(eCapturingPlayer, true, -1, szBuffer,
					"AS2D_UNITCAPTURE", MESSAGE_TYPE_INFO, pCapturedUnit->getButton(),
					GC.getColorType("GREEN"), kPlot.getX(), kPlot.getY());
				// Add a captured mission
				if (kPlot.isActiveVisible(false)) // K-Mod
				{
					CvMissionDefinition kMission;
					kMission.setMissionTime(GC.getInfo(MISSION_CAPTURED).getTime() *
						gDLL->getSecsPerTurn());
					kMission.setUnit(BATTLE_UNIT_ATTACKER, pCapturedUnit);
					kMission.setUnit(BATTLE_UNIT_DEFENDER, NULL);
					kMission.setPlot(&kPlot);
					kMission.setMissionType(MISSION_CAPTURED);
					gDLL->getEntityIFace()->AddMission(&kMission);
				}
				pCapturedUnit->finishMoves();
				// <advc.010> AI checks moved into AI_captureUnit. Rather than ...
				/*//pkCapturedUnit->kill(false);
				// K-Mod. roughly the same thing, but this is more appropriate.
				pCapturedUnit->scrap();*/
				// ... let's just not init the unit. </advc.010>
			}
		}
	}
}


void CvUnit::NotifyEntity(MissionTypes eMission)
{
	gDLL->getEntityIFace()->NotifyEntity(getEntity(), eMission);
}


void CvUnit::doTurn()
{
	PROFILE("CvUnit::doTurn()");

	FAssertMsg(!isDead(), "isDead did not return false as expected");
	FAssertMsg(getGroup() != NULL, "getGroup() is not expected to be equal with NULL");

	testPromotionReady();

	if (isBlockading())
	{
		if(canPlunder(getPlot())) // advc.033
			collectBlockadeGold();
		// <advc.033>
		else
		{
			setBlockading(false);
			getGroup()->setActivityType(ACTIVITY_AWAKE);
		} // </advc.033>
	}
	// <advc.004k>
	if (isSeaPatrolling() && !canSeaPatrol())
		getGroup()->setActivityType(ACTIVITY_AWAKE); // </advc.004k>
	if (isSpy() && isIntruding() && !isCargo())
	{
		TeamTypes eTeam = getPlot().getTeam();
		if (NO_TEAM != eTeam)
		{
			if (GET_TEAM(getTeam()).isOpenBorders(eTeam))
			{
				testSpyIntercepted(getPlot().getOwner(), false,
						GC.getDefineINT(CvGlobals::ESPIONAGE_SPY_NO_INTRUDE_INTERCEPT_MOD));
			}
			else
			{
				testSpyIntercepted(getPlot().getOwner(), false,
						GC.getDefineINT(CvGlobals::ESPIONAGE_SPY_INTERCEPT_MOD));
			}
		}
	}

	if (baseCombatStr() > 0)
	{
		FeatureTypes eFeature = getPlot().getFeatureType();
		if (eFeature != NO_FEATURE && GC.getInfo(eFeature).getTurnDamage() != 0)
		{
			// (advc, note: Should show an on-screen message here.)
			changeDamage(GC.getInfo(eFeature).getTurnDamage(), NO_PLAYER);
		}
	}

	if (hasMoved())
	{
		if (isAlwaysHeal())
		{
			doHeal();
		}
	}
	else
	{
		if (isHurt())
		{
			doHeal();
		}

		if (!isCargo())
		{
			changeFortifyTurns(1);
		}
	}

	changeImmobileTimer(-1);

	setMadeAttack(false);
	setMadeInterception(false);

	//setReconPlot(NULL); // advc.029: Handled at end of turn now
	// <advc.001b> Allow double spent moves to carry over to the next turn
	if (getMoves() >= 2 * maxMoves())
		finishMoves(); // </advc.001b>
	else setMoves(0);

    // doc: Turkic UP for the AI
    if (isBarbarian() && plot()->getOwner() != NO_PLAYER && GET_PLAYER(plot()->getOwner()).getCivilizationType() == TURKS && GC.getGame().getActiveCivilizationType() != TURKS)
    {
        setCapturingPlayer(plot()->getOwner());
        kill(false);
    }
}

// advc.029:
void CvUnit::doTurnPost()
{
	if(GC.getGame().getGameTurn() > m_iLastReconTurn)
		setReconPlot(NULL);
}

// advc.004c: Return type was void. Now returns false when intercepted.
bool CvUnit::updateAirStrike(CvPlot& kPlot, bool bQuick, bool bFinish)
{
	if (!bFinish)
	{
		if (isFighting())
			return true;

        // doc (Dale): nuclear bomber
        if (canNuke(&kPlot))
        {
            kill(true);
            return true;
        }

		bool const bVisible = (bQuick ? false : isCombatVisible(NULL));
		{
			bool bIntercepted=false; // advc.004c
			if (!airStrike(kPlot, &bIntercepted))
				return !bIntercepted; // advc.004c
		}
		if (bVisible)
		{
			CvAirMissionDefinition kAirMission;
			kAirMission.setMissionType(MISSION_AIRSTRIKE);
			kAirMission.setUnit(BATTLE_UNIT_ATTACKER, this);
			kAirMission.setUnit(BATTLE_UNIT_DEFENDER, NULL);
			kAirMission.setDamage(BATTLE_UNIT_DEFENDER, 0);
			kAirMission.setDamage(BATTLE_UNIT_ATTACKER, 0);
			kAirMission.setPlot(&kPlot);
			setCombatTimer(GC.getInfo(MISSION_AIRSTRIKE).getTime());
			GC.getGame().incrementTurnTimer(getCombatTimer());
			kAirMission.setMissionTime(getCombatTimer() * gDLL->getSecsPerTurn());
			if (kPlot.isActiveVisible(false))
				gDLL->getEntityIFace()->AddMission(&kAirMission);
			return true;
		}
	}
	CvUnit *pDefender = getCombatUnit();
	if (pDefender != NULL)
		pDefender->setCombatUnit(NULL);
	setCombatUnit(NULL);
	setAttackPlot(NULL, false);
	getGroup()->clearMissionQueue();
	if (isSuicide() && !isDead())
		kill(true);
	return true;
}

void CvUnit::resolveAirCombat(CvUnit* pInterceptor, CvPlot* pPlot, CvAirMissionDefinition& kBattle)
{
	CvWString szBuffer;

	int iTheirStrength = (DOMAIN_AIR == pInterceptor->getDomainType() ? pInterceptor->airCurrCombatStr(this) : pInterceptor->currCombatStr(NULL, NULL));
	int iOurStrength = (DOMAIN_AIR == getDomainType() ? airCurrCombatStr(pInterceptor) : currCombatStr(NULL, NULL));
	int iTotalStrength = iOurStrength + iTheirStrength;
	if (iTotalStrength == 0)
	{
		FAssert(false);
		return;
	}

	/*int iOurOdds = (100 * iOurStrength) / std::max(1, iTotalStrength);
	int iOurRoundDamage = (pInterceptor->currInterceptionProbability() * GC.getDefineINT("MAX_INTERCEPTION_DAMAGE")) / 100;
	int iTheirRoundDamage = (currInterceptionProbability() * GC.getDefineINT("MAX_INTERCEPTION_DAMAGE")) / 100;
	if (getDomainType() == DOMAIN_AIR)
		iTheirRoundDamage = std::max(GC.getDefineINT("MIN_INTERCEPTION_DAMAGE"), iTheirRoundDamage);
	int iTheirDamage = 0;
	int iOurDamage = 0;
	for (int iRound = 0; iRound < GC.getDefineINT("INTERCEPTION_MAX_ROUNDS"); ++iRound)*/ // BtS
	/*  BETTER_BTS_AI_MOD (Combat mechanics), 10/19/08, Roland J & jdog5000: START
		For air v air, more rounds and factor in strength for per round damage */
	int iOurOdds = (100 * iOurStrength) / std::max(1, iTotalStrength);
	int iMaxRounds = 0;
	int iOurRoundDamage = 0;
	int iTheirRoundDamage = 0;

	/*	Air v air is more like standard combat
		Round damage in this case will now depend on strength and interception probability */
	// <advc.opt>
	static bool const bBBAI_AIR_COMBAT = GC.getDefineBOOL("BBAI_AIR_COMBAT");
	static int const iINTERCEPTION_MAX_ROUNDS = GC.getDefineINT("INTERCEPTION_MAX_ROUNDS");
	static int const iMIN_INTERCEPTION_DAMAGE = GC.getDefineINT("MIN_INTERCEPTION_DAMAGE");
	static int const iMAX_INTERCEPTION_DAMAGE = GC.getDefineINT("MAX_INTERCEPTION_DAMAGE"); // </advc.opt>
	if (bBBAI_AIR_COMBAT && DOMAIN_AIR == pInterceptor->getDomainType() && DOMAIN_AIR == getDomainType())
	{
		int iBaseDamage = GC.getDefineINT(CvGlobals::AIR_COMBAT_DAMAGE);
		int iOurFirepower = ((airMaxCombatStr(pInterceptor) + iOurStrength + 1) / 2);
		int iTheirFirepower = ((pInterceptor->airMaxCombatStr(this) + iTheirStrength + 1) / 2);

		int iStrengthFactor = ((iOurFirepower + iTheirFirepower + 1) / 2);

		int iTheirInterception = std::max(pInterceptor->maxInterceptionProbability(),2*iMIN_INTERCEPTION_DAMAGE);
		int iOurInterception = std::max(maxInterceptionProbability(),2*iMIN_INTERCEPTION_DAMAGE);

		iOurRoundDamage = std::max(1, ((iBaseDamage * (iTheirFirepower + iStrengthFactor) * iTheirInterception) / ((iOurFirepower + iStrengthFactor) * 100)));
		iTheirRoundDamage = std::max(1, ((iBaseDamage * (iOurFirepower + iStrengthFactor) * iOurInterception) / ((iTheirFirepower + iStrengthFactor) * 100)));

		iMaxRounds = 2 * iINTERCEPTION_MAX_ROUNDS - 1;
	}
	else
	{
		iOurRoundDamage = (pInterceptor->currInterceptionProbability() * iMAX_INTERCEPTION_DAMAGE) / 100;
		iTheirRoundDamage = (currInterceptionProbability() * iMAX_INTERCEPTION_DAMAGE) / 100;
		if (getDomainType() == DOMAIN_AIR)
		{
			iTheirRoundDamage = std::max(iMIN_INTERCEPTION_DAMAGE, iTheirRoundDamage);
		}

		iMaxRounds = iINTERCEPTION_MAX_ROUNDS;
	}

	int iTheirDamage = 0;
	int iOurDamage = 0;

	for (int iRound = 0; iRound < iMaxRounds; ++iRound)
	// BETTER_BTS_AI_MOD: END
	{
		if (SyncRandSuccess100(iOurOdds))
		{
			if (DOMAIN_AIR == pInterceptor->getDomainType())
			{
				iTheirDamage += iTheirRoundDamage;
				pInterceptor->changeDamage(iTheirRoundDamage, getOwner());
				if (pInterceptor->isDead())
					break;
			}
		}
		else
		{
			iOurDamage += iOurRoundDamage;
			changeDamage(iOurRoundDamage, pInterceptor->getOwner());
			if (isDead())
			{
				break;
			}
		}
	}

	if (isDead())
	{
		if (iTheirRoundDamage > 0)
		{
			int iExperience = attackXPValue();
			iExperience = (iExperience * iOurStrength) / std::max(1, iTheirStrength);
			iExperience = range(iExperience, GC.getDefineINT(CvGlobals::MIN_EXPERIENCE_PER_COMBAT),
					GC.getDefineINT(CvGlobals::MAX_EXPERIENCE_PER_COMBAT));
			pInterceptor->changeExperience(iExperience, maxXPValue(), true,
					pPlot->getOwner() == pInterceptor->getOwner(), //!isBarbarian()
					getGlobalXPPercent()); // advc.312
		}
	}
	else if (pInterceptor->isDead())
	{
		int iExperience = pInterceptor->defenseXPValue();
		iExperience = (iExperience * iTheirStrength) / std::max(1, iOurStrength);
		iExperience = range(iExperience, GC.getDefineINT(CvGlobals::MIN_EXPERIENCE_PER_COMBAT),
				GC.getDefineINT(CvGlobals::MAX_EXPERIENCE_PER_COMBAT));
		changeExperience(iExperience, pInterceptor->maxXPValue(), true,
				pPlot->getOwner() == getOwner(), //!pInterceptor->isBarbarian()
				pInterceptor->getGlobalXPPercent()); // advc.312
	}
	else if (iOurDamage > 0)
	{
		if (iTheirRoundDamage > 0)
		{
			pInterceptor->changeExperience(GC.getDefineINT(CvGlobals::EXPERIENCE_FROM_WITHDRAWL),
					maxXPValue(), true,
					pPlot->getOwner() == pInterceptor->getOwner(), //!isBarbarian()
					getGlobalXPPercent()); // advc.312
		}
	}
	else if (iTheirDamage > 0)
	{
		changeExperience(GC.getDefineINT(CvGlobals::EXPERIENCE_FROM_WITHDRAWL),
				pInterceptor->maxXPValue(), true,
				pPlot->getOwner() == getOwner(), //!pInterceptor->isBarbarian()
				pInterceptor->getGlobalXPPercent()); // advc.312
	}

	kBattle.setDamage(BATTLE_UNIT_ATTACKER, iOurDamage);
	kBattle.setDamage(BATTLE_UNIT_DEFENDER, iTheirDamage);
}


void CvUnit::updateAirCombat(bool bQuick)
{
	FAssert(getDomainType() == DOMAIN_AIR || getDropRange() > 0);

	bool bFinish = false;
	if (getCombatTimer() > 0)
	{
		changeCombatTimer(-1);
		if (getCombatTimer() > 0)
			return;
		else bFinish = true;
	}

	CvPlot* const pPlot = getAttackPlot();
	if (pPlot == NULL)
		return;

	CvUnit* const pInterceptor = (bFinish ? getCombatUnit() : bestInterceptor(*pPlot));
	if (pInterceptor == NULL)
	{
		setAttackPlot(NULL, false);
		setCombatUnit(NULL);
		getGroup()->clearMissionQueue();
		return;
	}

	//check if quick combat
	bool const bVisible = (bQuick ? false : isCombatVisible(pInterceptor));

	//if not finished and not fighting yet, set up combat damage and mission
	if (!bFinish)
	{
		if (!isFighting())
		{
			//if (getPlot().isFighting() || pPlot->isFighting())
			/*	K-Mod. I don't think it matters if the plot we're on is fighting already
				- but the interceptor needs to be available to fight! */
			if (pPlot->isFighting() || pInterceptor->isFighting())
				return;
			setMadeAttack(true);
			setCombatUnit(pInterceptor, true);
			pInterceptor->setCombatUnit(this, false);
		}

		FAssert(getPlot().isFighting());
		FAssert(pInterceptor->getPlot().isFighting());

		CvAirMissionDefinition kAirMission;
		if (DOMAIN_AIR != getDomainType())
			kAirMission.setMissionType(MISSION_PARADROP);
		else kAirMission.setMissionType(MISSION_AIRSTRIKE);
		kAirMission.setUnit(BATTLE_UNIT_ATTACKER, this);
		kAirMission.setUnit(BATTLE_UNIT_DEFENDER, pInterceptor);

		resolveAirCombat(pInterceptor, pPlot, kAirMission);

		if (!bVisible)
			bFinish = true;
		else
		{
			kAirMission.setPlot(pPlot);
			kAirMission.setMissionTime(GC.getInfo(MISSION_AIRSTRIKE).getTime() * gDLL->getSecsPerTurn());
			setCombatTimer(GC.getInfo(MISSION_AIRSTRIKE).getTime());
			GC.getGame().incrementTurnTimer(getCombatTimer());
			if (pPlot->isActiveVisible(false))
				gDLL->getEntityIFace()->AddMission(&kAirMission);
		}

		changeMoves(GC.getMOVE_DENOMINATOR());
		if (pInterceptor->getDomainType() != DOMAIN_AIR)
			pInterceptor->setMadeInterception(true);

		if (isDead())
		{
			CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_YOU_SHOT_DOWN_ENEMY",
					pInterceptor->getNameKey(), getNameKey(), getVisualCivAdjective(pInterceptor->getTeam()));
			gDLL->UI().addMessage(pInterceptor->getOwner(), false, -1, szBuffer, *pPlot,
					"AS2D_INTERCEPT", MESSAGE_TYPE_INFO, getButton(), GC.getColorType("GREEN"));

			szBuffer = gDLL->getText("TXT_KEY_MISC_YOU_UNIT_SHOT_DOWN",
					getNameKey(), pInterceptor->getNameKey());
			gDLL->UI().addMessage(getOwner(), true, -1, szBuffer,
					"AS2D_INTERCEPTED", MESSAGE_TYPE_INFO, pInterceptor->getButton(), GC.getColorType("RED"),
					pPlot->getX(), pPlot->getY());
		}
		else if (kAirMission.getDamage(BATTLE_UNIT_ATTACKER) > 0)
		{
			CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_YOU_HURT_ENEMY_AIR",
					pInterceptor->getNameKey(), getNameKey(),
					kAirMission.getDamage(BATTLE_UNIT_ATTACKER), // advc.004g
					getVisualCivAdjective(pInterceptor->getTeam()));
			gDLL->UI().addMessage(pInterceptor->getOwner(), false, -1, szBuffer, *pPlot,
					"AS2D_INTERCEPT", MESSAGE_TYPE_INFO, getButton(), GC.getColorType("GREEN"));

			szBuffer = gDLL->getText("TXT_KEY_MISC_YOU_AIR_UNIT_HURT",
					getNameKey(), pInterceptor->getNameKey(),
					kAirMission.getDamage(BATTLE_UNIT_ATTACKER)); // advc.004g
			gDLL->UI().addMessage(getOwner(), true, -1, szBuffer,
					"AS2D_INTERCEPTED", MESSAGE_TYPE_INFO, pInterceptor->getButton(), GC.getColorType("RED"),
					pPlot->getX(), pPlot->getY());
		}

		if (pInterceptor->isDead())
		{
			CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_YOU_SHOT_DOWN_ENEMY",
					getNameKey(), pInterceptor->getNameKey(), pInterceptor->getVisualCivAdjective(getTeam()));
			gDLL->UI().addMessage(getOwner(), true, -1, szBuffer, *pPlot,
					"AS2D_INTERCEPT", MESSAGE_TYPE_INFO, pInterceptor->getButton(), GC.getColorType("GREEN"));

			szBuffer = gDLL->getText("TXT_KEY_MISC_YOU_UNIT_SHOT_DOWN",
					pInterceptor->getNameKey(), getNameKey());
			gDLL->UI().addMessage(pInterceptor->getOwner(), false, -1, szBuffer,
					"AS2D_INTERCEPTED", MESSAGE_TYPE_INFO, getButton(), GC.getColorType("RED"),
					pPlot->getX(), pPlot->getY());
		}
		else if (kAirMission.getDamage(BATTLE_UNIT_DEFENDER) > 0)
		{
			CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_YOU_DAMAGED_ENEMY_AIR",
					getNameKey(), pInterceptor->getNameKey(),
					kAirMission.getDamage(BATTLE_UNIT_DEFENDER), // advc.004g
					pInterceptor->getVisualCivAdjective(getTeam()));
			gDLL->UI().addMessage(getOwner(), true, -1, szBuffer, *pPlot,
					"AS2D_INTERCEPT", MESSAGE_TYPE_INFO, pInterceptor->getButton(), GC.getColorType("GREEN"));

			szBuffer = gDLL->getText("TXT_KEY_MISC_YOUR_AIR_UNIT_DAMAGED",
					pInterceptor->getNameKey(), getNameKey(),
					kAirMission.getDamage(BATTLE_UNIT_DEFENDER)); // advc.004g
			gDLL->UI().addMessage(pInterceptor->getOwner(), false, -1, szBuffer,
					"AS2D_INTERCEPTED", MESSAGE_TYPE_INFO, getButton(), GC.getColorType("RED"),
					pPlot->getX(), pPlot->getY());
		}

		if (kAirMission.getDamage(BATTLE_UNIT_ATTACKER) + kAirMission.getDamage(BATTLE_UNIT_DEFENDER) == 0)
		{
			CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_YOU_ABORTED_ENEMY_AIR",
					pInterceptor->getNameKey(), getNameKey(), getVisualCivAdjective(getTeam()));
			gDLL->UI().addMessage(pInterceptor->getOwner(), true, -1, szBuffer, *pPlot,
					"AS2D_INTERCEPT", MESSAGE_TYPE_INFO, pInterceptor->getButton(), GC.getColorType("GREEN"));

			szBuffer = gDLL->getText("TXT_KEY_MISC_YOUR_AIR_UNIT_ABORTED",
					getNameKey(), pInterceptor->getNameKey());
			gDLL->UI().addMessage(getOwner(), false, -1, szBuffer,
					"AS2D_INTERCEPTED", MESSAGE_TYPE_INFO, getButton(), GC.getColorType("RED"),
					pPlot->getX(), pPlot->getY());
		}
	}

	if (bFinish)
	{
		setAttackPlot(NULL, false);
		setCombatUnit(NULL);
		pInterceptor->setCombatUnit(NULL);
		if (!isDead() && isSuicide())
			kill(true);
	}
}

/*	K-Mod -- this makes the game log the odds and outcomes of every battle,
	to help verify the accuracy of the odds calculation. */
//#define LOG_COMBAT_OUTCOMES

/*	K-Mod. I've edited this function so that it handles the battle planning internally
	rather than feeding details back to the caller. */
/*	advc (note): Much of CombatOdds.cpp is based on this function and may have to
	be changed if the combat resolution rules are changed. */
void CvUnit::resolveCombat(CvUnit* pDefender, CvPlot* pPlot, bool bVisible)
{
	// <advc.048c> Preserve info for interface message (based on K-Mod code)
	m_iAttackOdds = -1;
#ifndef LOG_COMBAT_OUTCOMES
	if (GC.getDefineBOOL(CvGlobals::SHOW_ODDS_IN_COMBAT_MESSAGES) &&
		/*	To save time. addMessage will sometimes deliver messages to AI players,
			but it's OK (with me) to omit odds from those messages. */
		(isHuman() || pDefender->isHuman()))
	{
#endif
		m_iAttackOdds = calculateCombatOdds(*this, *pDefender,
				false); // Do reveal free wins vs. Barbarians
		m_iAttackOdds += ((GC.getCOMBAT_DIE_SIDES() - m_iAttackOdds) *
				withdrawalProbability()) / 100;
		m_iPreCombatHP = currHitPoints();
		pDefender->m_iPreCombatHP = pDefender->currHitPoints();
#ifndef LOG_COMBAT_OUTCOMES
	}
#endif
	// </advc.048c>

	// K-Mod. Initialize battle info.
	// Note: kBattle is only relevant if we are going to show the battle animation.
	CvBattleDefinition kBattle;
	if (bVisible)
	{
		kBattle.setUnit(BATTLE_UNIT_ATTACKER, this);
		kBattle.setUnit(BATTLE_UNIT_DEFENDER, pDefender);
		kBattle.setDamage(BATTLE_UNIT_ATTACKER, BATTLE_TIME_BEGIN, getDamage());
		kBattle.setDamage(BATTLE_UNIT_DEFENDER, BATTLE_TIME_BEGIN, pDefender->getDamage());
	}
	/*	positive number for attacker hitting the defender,
		negative numbers for defender hitting the attacker. */
	std::vector<int> combat_log;
	// K-Mod end

	CombatDetails cdAttackerDetails;
	CombatDetails cdDefenderDetails;

	int iAttackerStrength = currCombatStr(NULL, NULL, &cdAttackerDetails);
	int iAttackerFirepower = currFirepower();

	int iDefenderStrength=0, iAttackerDamage=0, iDefenderDamage=0, iDefenderOdds=0;
	getDefenderCombatValues(*pDefender, pPlot, iAttackerStrength, iAttackerFirepower,
			iDefenderOdds, iDefenderStrength, iAttackerDamage, iDefenderDamage,
			&cdDefenderDetails);
	int iAttackerKillOdds = iDefenderOdds * (100 - withdrawalProbability()) / 100;
	// advc.001: Replacing isHuman checks
	if (isActiveOwned() || pDefender->isActiveOwned())
	{
		CyArgsList pyArgsCD;
		pyArgsCD.add(gDLL->getPythonIFace()->makePythonObject(&cdAttackerDetails));
		pyArgsCD.add(gDLL->getPythonIFace()->makePythonObject(&cdDefenderDetails));
		pyArgsCD.add(calculateCombatOdds(*this, *pDefender));
		CvEventReporter::getInstance().genericEvent("combatLogCalc", pyArgsCD.makeFunctionArgs());
	}

	collateralCombat(pPlot, pDefender);

	while (true)
	{
		if (SyncRandNum(GC.getCOMBAT_DIE_SIDES()) < iDefenderOdds)
		{
			if (getCombatFirstStrikes() == 0)
			{
				if (getDamage() + iAttackerDamage >= maxHitPoints() &&
					SyncRandSuccess100(withdrawalProbability()))
				{
					flankingStrikeCombat(pPlot, iAttackerStrength, iAttackerFirepower,
							iAttackerKillOdds, iDefenderDamage, pDefender);
					changeExperience(GC.getDefineINT(CvGlobals::EXPERIENCE_FROM_WITHDRAWL),
							pDefender->maxXPValue(), true,
							pPlot->getOwner() == getOwner(), //!pDefender->isBarbarian()
							pDefender->getGlobalXPPercent()); // advc.312
					combat_log.push_back(0); // K-Mod
					break;
				}
				changeDamage(iAttackerDamage, pDefender->getOwner());
				combat_log.push_back(-iAttackerDamage); // K-Mod
				/* if (pDefender->getCombatFirstStrikes() > 0 && pDefender->isRanged()) {
					kBattle.addFirstStrikes(BATTLE_UNIT_DEFENDER, 1);
					kBattle.addDamage(BATTLE_UNIT_ATTACKER, BATTLE_TIME_RANGED, iAttackerDamage);
				} */
				// K-Mod. (I don't think this stuff is actually used, but I want to do it my way, just in case.)
				if (pDefender->getCombatFirstStrikes() > 0)
					kBattle.addFirstStrikes(BATTLE_UNIT_DEFENDER, 1);
				// K-Mod end
				cdAttackerDetails.iCurrHitPoints = currHitPoints();
				if (isHuman() || pDefender->isHuman())
				{	// advc: Moved into new function
					CvEventReporter::getInstance().combatLogHit(
							cdAttackerDetails, cdDefenderDetails, iAttackerDamage, true);
				}
			}
			// K-Mod. Track the free-strike misses, to use for choreographing the battle animation.
			else if (bVisible && !combat_log.empty())
				combat_log.push_back(0);
			// K-Mod end
		}
		else
		{
			if (pDefender->getCombatFirstStrikes() == 0)
			{	// <advc.001l>
				int iDamage = iDefenderDamage;
				//if (std::min(GC.getMAX_HIT_POINTS(), pDefender->getDamage() + iDefenderDamage) > combatLimit())
				/*	The above lets combat continue when the limit is
					reached exactly. This means, if the attacker lands another hit,
					it'll deal 0 damage (weird). Also inconsistent w/ caclulateCombatOdds. */
				// Minus one b/c reaching MAX_HIT_POINTS mustn't be treated as a withdrawal
				bool const bLimitReached = (std::min(GC.getMAX_HIT_POINTS() - 1,
						pDefender->getDamage() + iDamage) >= combatLimit());
				if (bLimitReached)
				{
					iDamage = combatLimit() - pDefender->getDamage();
					/*	Don't break right after the XP change; want to log the hit -
						now that it's guaranteed to be a proper hit (positive damage). */
					// </advc.001l>
					changeExperience(GC.getDefineINT(CvGlobals::EXPERIENCE_FROM_WITHDRAWL),
							pDefender->maxXPValue(), true,
							pPlot->getOwner() == getOwner(), //!pDefender->isBarbarian()
							pDefender->getGlobalXPPercent()); // advc.312
				}

			    // doc: Krak des Chevaliers effect
				if (pDefender->getDamage() + iDefenderDamage >= pDefender->maxHitPoints())
				{
					if (GET_PLAYER(pDefender->getOwner()).isHasBuildingEffect(KRAK_DES_CHEVALIERS))
					{
						if (pPlot->isCity())
						{
							CvCity* pCity = pPlot->getPlotCity();
							if (pCity->getOwner() == pDefender->getOwner() && !pCity->isCapital())
							{
								CvCity* pCapital = GET_PLAYER(pDefender->getOwner()).getCapitalCity();
								if (pCapital != NULL)
								{
									changeExperience(GC.getDefineINT("EXPERIENCE_FROM_WITHDRAWL"),
										pDefender->maxXPValue(),
										true,
										pPlot->getOwner() == getOwner(),
										!pDefender->isBarbarian());
									break;
								}
							}
						}
					}
				}

				pDefender->changeDamage(iDamage, getOwner());
				combat_log.push_back(iDamage); // K-Mod
				/* if (getCombatFirstStrikes() > 0 && isRanged()) {
					kBattle.addFirstStrikes(BATTLE_UNIT_ATTACKER, 1);
					kBattle.addDamage(BATTLE_UNIT_DEFENDER, BATTLE_TIME_RANGED, iDamage);
				} */
				// K-Mod
				if (getCombatFirstStrikes() > 0 && isRanged()) // doc
					kBattle.addFirstStrikes(BATTLE_UNIT_ATTACKER, 1);
				// K-Mod end
				cdDefenderDetails.iCurrHitPoints = pDefender->currHitPoints();
				if (isHuman() || pDefender->isHuman())
				{	// advc: Moved into new function
					CvEventReporter::getInstance().combatLogHit(
							cdAttackerDetails, cdDefenderDetails, iDamage, false);
				}
				// <advc.001l>
				if (bLimitReached)
					break; // </advc.001l>
			}
			// K-Mod
			else if (bVisible && !combat_log.empty())
				combat_log.push_back(0);
			// K-Mod end
		}

		if (getCombatFirstStrikes() > 0)
			changeCombatFirstStrikes(-1);
		if (pDefender->getCombatFirstStrikes() > 0)
			pDefender->changeCombatFirstStrikes(-1);

		if (isDead() || pDefender->isDead())
		{
			if (isDead())
			{
				int iExperience = defenseXPValue();
				iExperience = ((iExperience * iAttackerStrength) / iDefenderStrength);
				iExperience = range(iExperience,
						GC.getDefineINT(CvGlobals::MIN_EXPERIENCE_PER_COMBAT),
						GC.getDefineINT(CvGlobals::MAX_EXPERIENCE_PER_COMBAT)
						- (isBarbarian() && !isAnimal() ? 4 : 0)); // advc.312
				pDefender->changeExperience(iExperience, maxXPValue(), true,
						pPlot->getOwner() == pDefender->getOwner(), //!isBarbarian()
						getGlobalXPPercent()); // advc.312
			}
			else
			{
				flankingStrikeCombat(pPlot, iAttackerStrength, iAttackerFirepower,
						iAttackerKillOdds, iDefenderDamage, pDefender);

				int iExperience = pDefender->attackXPValue();
				iExperience = ((iExperience * iDefenderStrength) / iAttackerStrength);
				iExperience = range(iExperience,
						GC.getDefineINT(CvGlobals::MIN_EXPERIENCE_PER_COMBAT),
						GC.getDefineINT(CvGlobals::MAX_EXPERIENCE_PER_COMBAT)
						// advc.312:
						/ (pDefender->isBarbarian() && !pDefender->isAnimal() ? 2 : 1));
				changeExperience(iExperience, pDefender->maxXPValue(), true,
						pPlot->getOwner() == getOwner(), //!pDefender->isBarbarian()
						pDefender->getGlobalXPPercent());
			}
			GET_PLAYER(getOwner()).AI_attackMadeAgainst(*pDefender); // advc.139
			break;
		}
	}

	// K-Mod. Finalize battle info and start the animation.
	if (bVisible)
	{
		kBattle.setDamage(BATTLE_UNIT_ATTACKER, BATTLE_TIME_END, getDamage());
		kBattle.setDamage(BATTLE_UNIT_DEFENDER, BATTLE_TIME_END, pDefender->getDamage());
		kBattle.setAdvanceSquare(canAdvance(pPlot, 1));

		// note: BATTLE_TIME_RANGED damage is now set inside planBattle; (not that it actually does anything...)

		int iTurns = planBattle(kBattle, combat_log);
		kBattle.setMissionTime(iTurns * gDLL->getSecsPerTurn());
		setCombatTimer(iTurns);

		GC.getGame().incrementTurnTimer(getCombatTimer()); // additional time for multiplayer turn timer.

		if (pPlot->isActiveVisible(false))
		{
			ExecuteMove(0.5f, true);
			gDLL->getEntityIFace()->AddMission(&kBattle);
		}
	}
#ifdef LOG_COMBAT_OUTCOMES
	// (don't log barb battles, because they have special rules.)
	if (!isBarbarian() && !pDefender->isBarbarian())
	{
		TCHAR message[20];
		_snprintf(message, 20, "%.2f\t%d\n",
				m_iAttackOdds / (float)GC.getCOMBAT_DIE_SIDES(),
				isDead() ? 0 : 1);
		gDLL->logMsg("combat.txt", message ,false, false);
	}
#endif
}


void CvUnit::updateCombat(bool bQuick, /* <advc.004c> */ bool* pbIntercepted,
	bool bSeaPatrol) // advc.004k
{
	if (pbIntercepted != NULL)
		*pbIntercepted = false; // </advc.004c>
	bool bFinish = false;
	if (getCombatTimer() > 0)
	{	/*  advc.006: Assertion
			getCombatUnit() && ...
			fails for air strikes when "Quick Combat (Offense)" is disabled,
			but I don't think there's a problem. */
		FAssert(getCombatUnit() == NULL ||
				getCombatUnit()->getAttackPlot() == NULL); // K-Mod
		changeCombatTimer(-1);
		if (getCombatTimer() > 0)
			return;
		bFinish = true;
	}

	CvPlot* pPlot = getAttackPlot();
	if (pPlot == NULL)
		return;

	if (getDomainType() == DOMAIN_AIR)
	{
		if (!updateAirStrike(*pPlot, bQuick, bFinish) &&
			// <advc.004c>
			pbIntercepted != NULL)
		{
			*pbIntercepted = true; // </advc.004c>
		}
		return;
	}

	CvUnit* pDefender = NULL;
	if (bFinish)
		pDefender = getCombatUnit();
	else
	{
		FAssert(!isFighting());
		if (getPlot().isFighting() || pPlot->isFighting())
		{	/*	K-Mod. we need to wait for our turn to attack -
				so don't bother looking for a defender yet. */
			return;
		}
		pDefender = pPlot->getBestDefender(NO_PLAYER, getOwner(), this, true);
	}

	if (pDefender == NULL)
	{
		setAttackPlot(NULL, false);
		setCombatUnit(NULL);

		//getGroup()->groupMove(pPlot, true, ((canAdvance(pPlot, 0)) ? this : NULL));
		// K-Mod
		if (bFinish)
		{
			FErrorMsg("Cannot 'finish' combat with NULL defender");
			return;
		}
		else getGroup()->groupMove(pPlot, true, canAdvance(pPlot, 0) ? this : NULL, true);
		// K-Mod end

		getGroup()->clearMissionQueue();
		return;
	}

	//check if quick combat
	bool const bVisible = (bQuick ? false : isCombatVisible(pDefender,
			bSeaPatrol)); // advc.004k

	//FAssertMsg((pPlot == pDefender->plot()), "There is not expected to be a defender or the defender's plot is expected to be pPlot (the attack plot)");

	//if not finished and not fighting yet, set up combat damage and mission
	if (!bFinish)
	{
		if (!isFighting())
		{
			if (getPlot().isFighting() || pPlot->isFighting())
				return;

			setMadeAttack(true);

			//rotate to face plot
			DirectionTypes newDirection = estimateDirection(this->plot(), pDefender->plot());
			if (newDirection != NO_DIRECTION)
				setFacingDirection(newDirection);

			//rotate enemy to face us
			newDirection = estimateDirection(pDefender->plot(), this->plot());
			if (newDirection != NO_DIRECTION)
				pDefender->setFacingDirection(newDirection);

			setCombatUnit(pDefender, true);
			pDefender->setCombatUnit(this, false);

			// K-Mod (to prevent weirdness from simultaneous attacks)
			pDefender->setAttackPlot(NULL, false);
			pDefender->getGroup()->clearMissionQueue();

			bool bFocused = (bVisible && isCombatFocus() &&
					gDLL->UI().isCombatFocus());
			if (bFocused)
			{
				DirectionTypes directionType = directionXY(getPlot(), *pPlot);
				//								N			NE				E				SE
				NiPoint2 directions[8] = {NiPoint2(0, 1), NiPoint2(1, 1), NiPoint2(1, 0), NiPoint2(1, -1),
							// 		S				SW					W				NW
							NiPoint2(0, -1), NiPoint2(-1, -1), NiPoint2(-1, 0), NiPoint2(-1, 1)};
				NiPoint3 attackDirection = NiPoint3(directions[directionType].x, directions[directionType].y, 0);
				float plotSize = GC.getPLOT_SIZE();
				NiPoint3 lookAtPoint(getPlot().getPoint().x + plotSize / 2 * attackDirection.x,
						getPlot().getPoint().y + plotSize / 2 * attackDirection.y,
						(getPlot().getPoint().z + pPlot->getPoint().z) / 2);
				attackDirection.Unitize();
				gDLL->UI().lookAt(lookAtPoint,
						(!isActiveOwned() ||
						gDLL->getGraphicOption(GRAPHICOPTION_NO_COMBAT_ZOOM)) ?
						CAMERALOOKAT_BATTLE : CAMERALOOKAT_BATTLE_ZOOM_IN,
						attackDirection);
			}
			else
			{
				PlayerTypes eAttacker = getVisualOwner(pDefender->getTeam());
				CvWString szMessage;
				if (BARBARIAN_PLAYER != eAttacker)
				{
					szMessage = gDLL->getText("TXT_KEY_MISC_YOU_UNITS_UNDER_ATTACK",
							GET_PLAYER(getOwner()).getCivilizationShortDescription()); // rfc
				}
				else szMessage = gDLL->getText("TXT_KEY_MISC_YOU_UNITS_UNDER_ATTACK_UNKNOWN");

				gDLL->UI().addMessage(pDefender->getOwner(), true, -1, szMessage,
						"AS2D_COMBAT", MESSAGE_TYPE_DISPLAY_ONLY, getButton(),
						GC.getColorType("RED"), pPlot->getX(), pPlot->getY(), true);
			}
		}

		FAssert(getPlot().isFighting());
		FAssert(pPlot->isFighting());

		// doc: includes Turkic UP
		if (!pDefender->canDefendAgainst(this))
		{
			if (!bVisible)
				bFinish = true;
			else
			{
				CvMissionDefinition kMission;
				kMission.setMissionTime(getCombatTimer() * gDLL->getSecsPerTurn());
				kMission.setMissionType(MISSION_SURRENDER);
				kMission.setUnit(BATTLE_UNIT_ATTACKER, this);
				kMission.setUnit(BATTLE_UNIT_DEFENDER, pDefender);
				kMission.setPlot(pPlot);
				gDLL->getEntityIFace()->AddMission(&kMission);

				// Surrender mission
				setCombatTimer(GC.getInfo(MISSION_SURRENDER).getTime());

				GC.getGame().incrementTurnTimer(getCombatTimer());
			}

			// Kill them!
			pDefender->setDamage(GC.getMAX_HIT_POINTS(),
					// advc.004u: Pass along killer's identity
					getVisualOwner(pDefender->getTeam()));
		}
		else
		{
			resolveCombat(pDefender, pPlot, bVisible);
			FAssert(!bVisible || getCombatTimer() > 0);
			if (!bVisible)
				bFinish = true;

			// Note: K-Mod has moved the bulk of this block into resolveCombat.
		}
	}

	if (!bFinish)
		return; // advc

	if (bVisible)
	{
		if (isCombatFocus() && gDLL->UI().isCombatFocus())
		{
			if (isActiveOwned())
				gDLL->UI().releaseLockedCamera();
		}
	}

	//end the combat mission if this code executes first
	gDLL->getEntityIFace()->RemoveUnitFromBattle(this);
	gDLL->getEntityIFace()->RemoveUnitFromBattle(pDefender);
	setAttackPlot(NULL, false);
	setCombatUnit(NULL);
	pDefender->setCombatUnit(NULL);
	NotifyEntity(MISSION_DAMAGE);
	pDefender->NotifyEntity(MISSION_DAMAGE);
	PlayerTypes const ePlotOwner = pPlot->getOwner(); // advc.130m
	if (isDead())
	{
		if (isBarbarian())
		{
			GET_PLAYER(pDefender->getOwner()).changeWinsVsBarbs(1);
			// <advc.304>
			if (!isAnimal())
			{
				GC.getGame().getBarbarianWeightMap().getActivityMap().change(
						getPlot());
			} // </advc.304>
		}
		if (!m_pUnitInfo->isHiddenNationality() &&
			!pDefender->getUnitInfo().isHiddenNationality())
		{
			GET_TEAM(getTeam()).changeWarWeariness(pDefender->getTeam(), *pPlot,
					GC.getDefineINT("WW_UNIT_KILLED_ATTACKING"));
			GET_TEAM(pDefender->getTeam()).changeWarWeariness(getTeam(), *pPlot,
					GC.getDefineINT("WW_KILLED_UNIT_DEFENDING"));
		}
		// <advc.130m>
		int const iWS = GC.getDefineINT(CvGlobals::WAR_SUCCESS_DEFENDING);
		GET_TEAM(pDefender->getTeam()).AI_changeWarSuccess(getTeam(), iWS);
		if (ePlotOwner != NO_PLAYER)
		{
			TeamTypes ePlotMaster = GET_PLAYER(ePlotOwner).getMasterTeam();
			/*  Success vs. Barbarians isn't normally counted. Do count it if
				it happens in another civ's borders. Also Privateers.
				Success within their borders against a shared war enemy is
				already counted by changeWarSuccess, but count it again
				for added weight. */
			if (ePlotMaster != GET_TEAM(pDefender->getTeam()).getMasterTeam() &&
				// Plot owner not happy if his own Privateer killed
				ePlotMaster != GET_TEAM(getTeam()).getMasterTeam() &&
				(isBarbarian() || m_pUnitInfo->isHiddenNationality() ||
				GET_TEAM(getTeam()).isAtWar(pPlot->getTeam())))
			{
				GET_TEAM(ePlotOwner).AI_reportSharedWarSuccess(
						iWS, pDefender->getTeam(), getTeam(), true);
			}
			// Same for the owner of the dead unit
			if (ePlotMaster != GET_TEAM(pDefender->getTeam()).getMasterTeam() &&
				ePlotMaster != GET_TEAM(getTeam()).getMasterTeam() &&
				(pDefender->isBarbarian() ||
				pDefender->m_pUnitInfo->isHiddenNationality() ||
				GET_TEAM(pDefender->getTeam()).isAtWar(pPlot->getTeam())))
			{
				GET_TEAM(ePlotOwner).AI_reportSharedWarSuccess(
						iWS, getTeam(), pDefender->getTeam(), true);
			}
		} // <advc.130m>

		addDefenseSuccessMessages(*pDefender); // advc: Moved into new function
		// report event to Python, along with some other key state
		CvEventReporter::getInstance().combatResult(pDefender, this);
	}
	else if (pDefender->isDead())
	{
		if (pDefender->isBarbarian())
		{
			GET_PLAYER(getOwner()).changeWinsVsBarbs(1);
			// <advc.304>
			if (!pDefender->isAnimal())
			{
				GC.getGame().getBarbarianWeightMap().getActivityMap().change(
						pDefender->getPlot());
			} // </advc.304>
		}
		if (!m_pUnitInfo->isHiddenNationality() &&
			!pDefender->getUnitInfo().isHiddenNationality())
		{
			GET_TEAM(pDefender->getTeam()).changeWarWeariness(getTeam(), *pPlot,
					GC.getDefineINT("WW_UNIT_KILLED_DEFENDING"));
			GET_TEAM(getTeam()).changeWarWeariness(pDefender->getTeam(), *pPlot,
					GC.getDefineINT("WW_KILLED_UNIT_ATTACKING"));
		}
		// <advc.130m>
		int const iWS = GC.getDefineINT(CvGlobals::WAR_SUCCESS_ATTACKING);
		GET_TEAM(getTeam()).AI_changeWarSuccess(pDefender->getTeam(), iWS);
		if(ePlotOwner != NO_PLAYER) // As above
		{
			TeamTypes ePlotMaster = GET_PLAYER(ePlotOwner).getMasterTeam();
			if(ePlotMaster != GET_TEAM(pDefender->getTeam()).getMasterTeam() &&
				ePlotMaster != GET_TEAM(getTeam()).getMasterTeam() &&
				(isBarbarian() || m_pUnitInfo->isHiddenNationality() ||
				GET_TEAM(getTeam()).isAtWar(pPlot->getTeam())))
			{
				GET_TEAM(ePlotOwner).AI_reportSharedWarSuccess(
					iWS, pDefender->getTeam(), getTeam(), true);
			}
			if(ePlotMaster != GET_TEAM(pDefender->getTeam()).getMasterTeam() &&
				ePlotMaster != GET_TEAM(getTeam()).getMasterTeam() &&
				(pDefender->isBarbarian() ||
				pDefender->m_pUnitInfo->isHiddenNationality() ||
				GET_TEAM(pDefender->getTeam()).isAtWar(pPlot->getTeam())))
			{
				GET_TEAM(ePlotOwner).AI_reportSharedWarSuccess(
					iWS, getTeam(), pDefender->getTeam(), true);
			}
		} // <advc.130m>
		// report event to Python, along with some other key state
		CvEventReporter::getInstance().combatResult(this, pDefender);
		bool bAdvance = false;
		bool bCapture = false; // advc.010
		if (isSuicide())
		{	// advc.010: Moved into new function
			addAttackSuccessMessages(*pDefender, true);
			kill(true);
			pDefender->kill(false);
			pDefender = NULL;
		}
		else
		{
			bAdvance = canAdvance(pPlot, pDefender->canDefendAgainst(this) ? 1 : 0); // doc: includes Turkish UP
			if (bAdvance)
			{
				if (!isNoUnitCapture())
				{
					pDefender->setCapturingPlayer(getOwner());
					bCapture = true; // advc.010
				}
			}
			/*	<advc.010> BtS had shown "destroyed" and then "captured" (I think).
				We want to show only the captured message. */
			if (!bCapture)
				addAttackSuccessMessages(*pDefender, true); // </advc.010>
			pDefender->kill(false);
			pDefender = NULL;
			if (!bAdvance)
			{
				changeMoves(std::max(GC.getMOVE_DENOMINATOR(),
						pPlot->movementCost(*this, getPlot())));
				checkRemoveSelectionAfterAttack();
			}
		}

		if (pPlot->getNumVisibleEnemyDefenders(this) == 0)
		{
			getGroup()->groupMove(pPlot, true, bAdvance ? this : NULL,
					true); // K-Mod
		}

		// This is is put before the plot advancement, the unit will always try to walk back
		// to the square that they came from, before advancing.
		getGroup()->clearMissionQueue();
	}
    // TODO: use addWithdrawalMessage
	else if (GET_PLAYER(pDefender->getOwner()).isHasBuildingEffect(KRAK_DES_CHEVALIERS) && pDefender->plot()->isCity() && pDefender->getDomainType() == DOMAIN_LAND && pDefender->maxHitPoints() - pDefender->getDamage() < maxHitPoints() - getDamage())
	{
		CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_ENEMY_UNIT_WITHDRAW", pDefender->getNameKey(), getNameKey());
		gDLL->getInterfaceIFace()->addMessage(getOwner(), true, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_OUR_WITHDRAWL", MESSAGE_TYPE_INFO, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_GREEN"), pPlot->getX(), pPlot->getY());

		bool bAdvance = canAdvance(pPlot, ((pDefender->canDefendAgainst(this)) ? 1 : 0));

		CvCity* pCapital = GET_PLAYER(pDefender->getOwner()).getCapitalCity();
		if (pCapital != NULL && !pDefender->atPlot(pCapital->plot()))
		{
			szBuffer = gDLL->getText("TXT_KEY_MISC_YOU_DEFENDER_UNIT_WITHDRAW", pDefender->getNameKey(), getNameKey(), pCapital->getName().c_str());
			gDLL->getInterfaceIFace()->addMessage(pDefender->getOwner(), true, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_THEIR_WITHDRAWL", MESSAGE_TYPE_INFO, pDefender->getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_RED"), pCapital->getX(), pCapital->getY());

			pDefender->setXY(pCapital->getX(), pCapital->getY());
		}
		else
		{
			szBuffer = gDLL->getText("TXT_KEY_MISC_YOU_UNIT_WITHDRAW", pDefender->getNameKey(), getNameKey());
			gDLL->getInterfaceIFace()->addMessage(pDefender->getOwner(), true, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_THEIR_WITHDRAWL", MESSAGE_TYPE_INFO, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_RED"), pPlot->getX(), pPlot->getY());
		}

		if (!bAdvance)
		{
			changeMoves(std::max(GC.getMOVE_DENOMINATOR(), pPlot->movementCost(*this, getPlot())));
			checkRemoveSelectionAfterAttack();
		}

		if (pPlot->getNumVisibleEnemyDefenders(this) == 0)
		{
			getGroup()->groupMove(pPlot, true, ((bAdvance) ? this : NULL));
		}

		getGroup()->clearMissionQueue();
	}
	else
	{
		addWithdrawalMessages(*pDefender); // advc: Moved into new function
		changeMoves(std::max(GC.getMOVE_DENOMINATOR(),
				pPlot->movementCost(*this, getPlot())));
		checkRemoveSelectionAfterAttack();
		getGroup()->clearMissionQueue();
	}
}

// advc.010: Cut from resolveCombat. Used for killed noncombatants with bFought=false.
void CvUnit::addAttackSuccessMessages(CvUnit const& kDefender, bool bFought) const
{
	bool const bSound = !suppressStackAttackSound(kDefender); // advc.002l
	CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_YOU_UNIT_DESTROYED_ENEMY",
			getNameKey(), /* advc.004u: */ kDefender.getNameKeyNoGG());
	CvPlot const& kPlot = kDefender.getPlot();
	gDLL->UI().addMessage(getOwner(), bFought, -1, szBuffer, bFought &&
			bSound ? GC.getInfo(GET_PLAYER(getOwner()) // advc.002l
			.getCurrentEra()).getAudioUnitVictoryScript()
			: NULL, // advc.010: No victory sound for killing noncombatant
			MESSAGE_TYPE_INFO, NULL,
			GC.getColorType("GREEN"), kPlot.getX(), kPlot.getY());
	setHasBeenDefendedAgainstMessage(szBuffer, kDefender, 1); // advc.048c
	gDLL->UI().addMessage(kDefender.getOwner(), bFought, -1, szBuffer,
			bSound ? GC.getInfo(GET_PLAYER(kDefender.getOwner()) // advc.002l
			.getCurrentEra()).getAudioUnitDefeatScript() /* advc.002l: */ : NULL,
			MESSAGE_TYPE_INFO, NULL, GC.getColorType("RED"), kPlot.getX(), kPlot.getY());
}

// <advc> Cut from resolveCombat - just to be consistent with addAttackSuccessMessages.
void CvUnit::addDefenseSuccessMessages(CvUnit const& kDefender) const
{
	bool const bSound = !suppressStackAttackSound(kDefender);
	CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_YOU_UNIT_DIED_ATTACKING",
			getNameKeyNoGG(), // advc.004u
			kDefender.getNameKey());
	CvPlot const& kPlot = kDefender.getPlot();
	gDLL->UI().addMessage(getOwner(), true, -1, szBuffer,
			bSound ? GC.getInfo(GET_PLAYER(getOwner()) // advc.002l
			.getCurrentEra()).getAudioUnitDefeatScript() /* 002l: */ : NULL,
			MESSAGE_TYPE_INFO, NULL, GC.getColorType("RED"),
			kPlot.getX(), kPlot.getY());
	setHasBeenDefendedAgainstMessage(szBuffer, kDefender, -1); // advc.048c
	gDLL->UI().addMessage(kDefender.getOwner(),
			true, -1, szBuffer,
			bSound ? GC.getInfo(GET_PLAYER(kDefender.getOwner()) // advc.002l
			.getCurrentEra()).getAudioUnitVictoryScript() /* advc.002l: */ : NULL,
			MESSAGE_TYPE_INFO, NULL, GC.getColorType("GREEN"),
			kPlot.getX(), kPlot.getY());
}


void CvUnit::addWithdrawalMessages(CvUnit const& kDefender) const
{
	bool const bSea = (getDomainType() == DOMAIN_SEA); // advc.002l
	CvPlot const& kPlot = kDefender.getPlot();
	CvWString szBuffer(gDLL->getText("TXT_KEY_MISC_YOU_UNIT_WITHDRAW",
			getNameKey(), kDefender.getNameKey()));
	gDLL->UI().addMessage(getOwner(), true, -1, szBuffer,
			bSea ? "AS2D_OUR_SEA_WITHDRAWL" : // advc.002l
			"AS2D_OUR_WITHDRAWL", MESSAGE_TYPE_INFO, NULL,
			GC.getColorType("GREEN"), kPlot.getX(), kPlot.getY());
	setHasBeenDefendedAgainstMessage(szBuffer, kDefender, 0); // advc.048c
	gDLL->UI().addMessage(kDefender.getOwner(), true, -1, szBuffer,
			bSea ? "AS2D_THEIR_SEA_WITHDRAWL" : // advc.002l
			"AS2D_THEIR_WITHDRAWL", MESSAGE_TYPE_INFO, NULL,
			GC.getColorType("RED"), kPlot.getX(), kPlot.getY());
} // </advc>

/*	advc.048c: Based on code originally in resolveCombat.
	iAttackSuccess:
	1 for defender destroyed, -1 for attacker destroyed, 0 for withdrawal. */
void CvUnit::setHasBeenDefendedAgainstMessage(CvWString& kBuffer,
	CvUnit const& kDefender, int iAttackSuccess) const
{
	bool const bOdds = (GC.getDefineBOOL(CvGlobals::SHOW_ODDS_IN_COMBAT_MESSAGES) &&
			m_iAttackOdds >= 0 && kDefender.canDefend());
	CvWString szOdds, szDefStrength;
	if (bOdds)
	{
		szOdds.Format(L"%.1f", (std::min(
				GC.getCOMBAT_DIE_SIDES() - 1, // Don't claim that the odds were 100%
				m_iAttackOdds) * 100.f) / GC.getCOMBAT_DIE_SIDES());
		if (kDefender.m_iPreCombatHP < kDefender.maxHitPoints())
		{
			CvWString szHurtStr;
			GAMETEXT.setHurtUnitStrength(szHurtStr, kDefender,
					kDefender.m_iPreCombatHP);
			szDefStrength.append(L" (");
			szDefStrength.append(szHurtStr);
			szDefStrength.append(L")");
		}
	}
	if (iAttackSuccess < 0)
	{
		if (bOdds)
		{
			kBuffer = gDLL->getText("TXT_KEY_MISC_YOU_KILLED_ENEMY_UNIT_ODDS",
					kDefender.getNameKey(),
					getNameKeyNoGG(), // advc.004u
					getVisualCivAdjective(kDefender.getTeam()),
					szDefStrength.c_str(), szOdds.c_str());
		}
		else
		{
			kBuffer = gDLL->getText("TXT_KEY_MISC_YOU_KILLED_ENEMY_UNIT",
					kDefender.getNameKey(),
					getNameKeyNoGG(), // advc.004u
					getVisualCivAdjective(kDefender.getTeam()));
		}
	}
	else if (iAttackSuccess > 0)
	{
		if (getVisualOwner(kDefender.getTeam()) != getOwner())
		{
			if (bOdds)
			{
				kBuffer = gDLL->getText("TXT_KEY_MISC_YOU_UNIT_WAS_DESTROYED_UNKNOWN_ODDS",
						kDefender.getNameKeyNoGG(), // advc.004u
						getNameKey(),
						szDefStrength.c_str(), szOdds.c_str());
			}
			else
			{
				kBuffer = gDLL->getText("TXT_KEY_MISC_YOU_UNIT_WAS_DESTROYED_UNKNOWN",
						kDefender.getNameKeyNoGG(), // advc.004u
						getNameKey());
			}
		}
		else
		{
			if (bOdds)
			{
				kBuffer = gDLL->getText("TXT_KEY_MISC_YOU_UNIT_WAS_DESTROYED_ODDS",
						kDefender.getNameKeyNoGG(), // advc.004u
						getNameKey(),
						getVisualCivAdjective(kDefender.getTeam()),
						szDefStrength.c_str(), szOdds.c_str());
			}
			else
			{
				kBuffer = gDLL->getText("TXT_KEY_MISC_YOU_UNIT_WAS_DESTROYED",
						kDefender.getNameKeyNoGG(), // advc.004u
						getNameKey(),
						getVisualCivAdjective(kDefender.getTeam()));
			}
		}
	}
	else
	{
		if (bOdds)
		{
			kBuffer = gDLL->getText("TXT_KEY_MISC_ENEMY_UNIT_WITHDRAW_ODDS",
					getNameKey(),
					kDefender.getNameKeyNoGG(), // advc.004u
					szDefStrength.c_str(), szOdds.c_str());
		}
		else
		{
			kBuffer = gDLL->getText("TXT_KEY_MISC_ENEMY_UNIT_WITHDRAW",
					getNameKey(),
					kDefender.getNameKeyNoGG()); // advc.004u
		}
	}
}

// advc.002l:
bool CvUnit::suppressStackAttackSound(CvUnit const& kDefender) const
{
	if (!isActiveOwned())
		return false;
	CvSelectionGroup const* pAttackGroup = gDLL->UI().getSelectionList();
	if (pAttackGroup == NULL ||
		!GET_PLAYER(getOwner()).isHumanOption(PLAYEROPTION_STACK_ATTACK))
	{
		return false;
	}
	/*	Play sound for final attack. (Apparently, 2 units remain selected
		at that point - don't know why. */
	if (pAttackGroup->getNumUnits() <= 2)
		return false;
	// Also the final attack if we're running out of defenders
	return (kDefender.getPlot().getNumVisibleEnemyDefenders(this) > 1);
}


void CvUnit::checkRemoveSelectionAfterAttack()
{
	if (!canMove() ||/*!isBlitz()*/ /* advc.164:*/ isMadeAllAttacks())
	{
		if (IsSelected())
		{
			if (gDLL->UI().getLengthSelectionList() > 1)
				gDLL->UI().removeFromSelectionList(this);
		}
	}
}


bool CvUnit::isActionRecommended(int iAction)
{
	if (!isActiveOwned() || /* advc.127: */ !isHuman())
		return false;

	bool bUpdateFoundBorder = false; // advc.004h
	// <advc> (Don't know how else the DLL could tell)
	static int iLastAction = MAX_INT;
	if (iAction < iLastAction)
	{
		onActiveSelection();
		bUpdateFoundBorder = true; // advc.004h
	}
	iLastAction = iAction;
	// </advc>  <advc.004h>
	{	// Update founding border also when go-to plot changes
		static CvPlot const* pLastGoToPlot = NULL;
		CvPlot const* pGoToPlot = gDLL->UI().getGotoPlot();
		if (pGoToPlot != NULL && pGoToPlot != pLastGoToPlot)
		{
			bUpdateFoundBorder = true;
			pLastGoToPlot = pGoToPlot;
		}
	}
	if (bUpdateFoundBorder && isFound())
		updateFoundingBorder();
	// </advc.004h>
	if (GET_PLAYER(getOwner()).isOption(PLAYEROPTION_NO_UNIT_RECOMMENDATIONS))
		return false;

	if (GC.getPythonCaller()->isActionRecommended(*this, iAction))
		return true;

	// advc: Moved up
	if (GC.getActionInfo(iAction).getCommandType() == COMMAND_PROMOTION)
		return true;
	// <advc>
	CvPlot const* pTmpPlot = gDLL->UI().getGotoPlot();
	if (pTmpPlot == NULL && GC.shiftKey())
		pTmpPlot = getGroup()->lastMissionPlot();
	CvPlot const& kPlot = (pTmpPlot == NULL ? getPlot() : *pTmpPlot); // </advc>
	// <advc.181>
	if (!kPlot.isRevealed(getTeam()))
		return false; // </advc.181>
	switch (GC.getActionInfo(iAction).getMissionType()) // advc
	{
	case MISSION_FORTIFY:
		if (kPlot.getOwner() == getOwner() && // advc.004
			GET_TEAM(getTeam()).isCityDefense(kPlot) && // advc (was isCity(true,getTeam())
			canDefend(&kPlot) &&
			kPlot.getNumDefenders(getOwner()) < (at(kPlot) ? 2 : 1))
		{
			return true;
		}
		break;
	case MISSION_SENTRY_HEAL: // advc.004l
	case MISSION_HEAL:
		if (isHurt() && !hasMoved())
		{
			if (kPlot.getTeam() == getTeam() || healTurns(&kPlot) < 4)
				return true;
		}
		break;
	case MISSION_FOUND:
	{
		if (canFound(&kPlot) && kPlot.isBestAdjacentFound(getOwner()))
			return true;
		break;
	}
	case MISSION_BUILD:
	{
		if (kPlot.getOwner() != getOwner())
			break;

		BuildTypes eBuild = (BuildTypes)GC.getActionInfo(iAction).getMissionData();
		FAssert(eBuild != NO_BUILD);
		FAssertMsg(eBuild < GC.getNumBuildInfos(), "Invalid Build");

		if (!canBuild(kPlot, eBuild, /* advc.181: */ false, false))
			break;
		// <K-Mod>
		if (kPlot.getBuildProgress(eBuild) > 0)
			return true; // </K-Mod>

		ImprovementTypes const eImprovement = GC.getInfo(eBuild).getImprovement();
		RouteTypes const eRoute = GC.getInfo(eBuild).getRoute();
		// K-Mod: was getBonusType
		BonusTypes const eBonus = kPlot.getNonObsoleteBonusType(getTeam());
		CvCityAI const* pWorkingCity = kPlot.AI_getWorkingCity();
		// Disabled by K-Mod (this looks like a bug to me)
		// if (kPlot.getImprovementType() == NO_IMPROVEMENT) {
		BuildTypes eBestBuild = NO_BUILD; // K-Mod. (I use this again later.)
		if (pWorkingCity != NULL)
		{
			CityPlotTypes ePlot = pWorkingCity->getCityPlotIndex(kPlot);
			FAssert(ePlot != NO_CITYPLOT); // K-Mod. this use to be an if statement in the release code

			eBestBuild = pWorkingCity->AI_getBestBuild(ePlot);
			if (eBestBuild == eBuild)
				return true;
		}
		if (eImprovement != NO_IMPROVEMENT)
		{
			/*if (eBonus != NO_BONUS) {
				if (GC.getInfo(eImprovement).isImprovementBonusTrade(eBonus))
					return true;
			}*/ // BtS
			// K-Mod
			if (eBonus != NO_BONUS &&
				!GET_PLAYER(getOwner()).doesImprovementConnectBonus(
				kPlot.getImprovementType(), eBonus) &&
				GET_PLAYER(getOwner()).doesImprovementConnectBonus(eImprovement, eBonus) &&
				(eBestBuild == NO_BUILD ||
				!GET_PLAYER(getOwner()).doesImprovementConnectBonus(
				GC.getInfo(eBestBuild).getImprovement(), eBonus)))
			{
				return true;
			}
			if (!kPlot.isImproved() && eBonus == NO_BONUS && pWorkingCity == NULL)
			{
				if (!kPlot.isFeature() || !GC.getInfo(eBuild).isFeatureRemove(
					kPlot.getFeatureType()))
				{
					if (GC.getInfo(eImprovement).isCarriesIrrigation() &&
						!kPlot.isIrrigated() && kPlot.isIrrigationAvailable(true))
					{
						return true;
					}
					if (kPlot.isFeature() &&
						GC.getInfo(eImprovement).getFeatureGrowthProbability() > 0)
					{
						return true;
					}
				}
			} // K-Mod end
			/*if (kPlot.getImprovementType() == NO_IMPROVEMENT) {
				if (!kPlot.isIrrigated() && kPlot.isIrrigationAvailable(true)) {
					if (GC.getInfo(eImprovement).isCarriesIrrigation())
						return true;
				}
				if (pWorkingCity != NULL) {
					if (GC.getInfo(eImprovement).getYieldChange(YIELD_FOOD) > 0)
						return true;
					if (kPlot.isHills()) {
						if (GC.getInfo(eImprovement).getYieldChange(YIELD_PRODUCTION) > 0)
							return true;
					}
					else if (GC.getInfo(eImprovement).getYieldChange(YIELD_COMMERCE) > 0)
						return true;
				}
			}*/ // BtS
		}

		if (eRoute != NO_ROUTE)
		{
			if (!kPlot.isRoute())
			{
				if (eBonus != NO_BONUS)
					return true;
				if (pWorkingCity != NULL)
				{
					if (kPlot.isRiver())
						return true;
				}
			}

			/*eFinalImprovement = eImprovement;
			if(eFinalImprovement == NO_IMPROVEMENT)
				eFinalImprovement = kPlot.getImprovementType();*/ // BtS
			// K-Mod
			ImprovementTypes const eFinalImprovement = CvImprovementInfo::finalUpgrade(
					eImprovement != NO_IMPROVEMENT ? eImprovement :
					kPlot.getImprovementType());
			// K-Mod end
			if (eFinalImprovement != NO_IMPROVEMENT)
			{
				CvImprovementInfo const& kFinal = GC.getInfo(eFinalImprovement);
				if (kFinal.getRouteYieldChanges(eRoute, YIELD_FOOD) > 0 ||
					kFinal.getRouteYieldChanges(eRoute, YIELD_PRODUCTION) > 0 ||
					kFinal.getRouteYieldChanges(eRoute, YIELD_COMMERCE) > 0)
				{
					return true;
				}
			}
		}
		break;
	}
	}

	return false;
}

// advc: Called when a unit of the active player becomes selected
void CvUnit::onActiveSelection()
{
	/*  <advc.002e> This needs to happen in some CvUnit function that gets called
		by the EXE after read, after isPromotionReady and late enough for IsSelected
		to work. (E.g. setupGraphical and shouldShowEnemyGlow are too early.) */
	if (!BUGOption::isEnabled("PLE__ShowPromotionGlow", false))
	{
		FOR_EACH_UNIT_VAR_IN(pUnit, *getGroup())
		{
			if (pUnit != NULL)
			{
				gDLL->getEntityIFace()->showPromotionGlow(pUnit->getEntity(),
						pUnit->isPromotionReady());
			}
		}
	} // </advc.002e>
	GC.getGame().updateSeaPatrolColors(*this); // advc.004k
}

// advc.004h:
void CvUnit::updateFoundingBorder(bool bForceClear) const
{
	if (!GC.getGame().isFinalInitialized())
		return;
	int iMode = BUGOption::getValue("MainInterface__FoundingBorder", 2);
	if(BUGOption::isEnabled("MainInterface__FoundingYields", false) && iMode == 1)
		return; // BtS behavior
	gDLL->getEngineIFace()->clearAreaBorderPlots(AREA_BORDER_LAYER_FOUNDING_BORDER);
	if(bForceClear || iMode <= 0 || !isFound())
		return;
	FOR_EACH_UNIT_IN(pUnit, *getGroup())
	{
		if(pUnit == NULL || (pUnit->IsSelected() && !pUnit->isFound()))
			return;
	}
	CvPlot* pGoToPlot = gDLL->UI().getGotoPlot();
	CvPlot* pCenter;
	if(pGoToPlot == NULL)
		pCenter = plot();
	else pCenter = pGoToPlot;
	if(pCenter == NULL || !pCenter->isRevealed(TEAMID(getOwner())) ||
		(!atPlot(pCenter) && !canMoveInto(*pCenter)) || !canFound(pCenter))
	{
		return;
	}
	ColorTypes eColor = GC.getInfo(GET_PLAYER(getOwner()).
			getPlayerColor()).getColorTypePrimary();
	NiColorA const& kColor = GC.getInfo(eColor).getColor();
	for (PlotCircleIter itPlot(*pCenter, iMode == 1 ? 1 : CITY_PLOTS_RADIUS);
		itPlot.hasNext(); ++itPlot)

	{
		gDLL->getEngineIFace()->fillAreaBorderPlot(itPlot->getX(), itPlot->getY(),
				kColor, AREA_BORDER_LAYER_FOUNDING_BORDER);
	}
}

/*  advc.061: See comment at call location in CvGameTextMgr::setPlotListHelpPerOwner.
	Doesn't check isVisible. */
bool CvUnit::isUnowned() const
{
	PlayerTypes eVisualOwner = getVisualOwner(GC.getGame().getActiveTeam());
	if (eVisualOwner == NO_PLAYER)
	{
		FAssert(eVisualOwner != NO_PLAYER);
		return true;
	}
	if (eVisualOwner != BARBARIAN_PLAYER)
		return false;
	if (isAnimal() || m_pUnitInfo->isHiddenNationality())
		return true;
	// The way this function is used, I guess it's possible that the unit has just died, so:
	// Erik: bugfix, the current plot could be NULL
	CvPlot* pPlot = plot();
	if (pPlot == NULL)
		return false; // (end of bugfix)
	CvCity* pPlotCity = pPlot->getPlotCity();
	if (pPlotCity != NULL && pPlotCity->isBarbarian())
		return true;
	return false;
}

bool CvUnit::canDoCommand(CommandTypes eCommand, int iData1, int iData2,
	bool bTestVisible, bool bTestBusy) /* advc: */ const
{
	if (bTestBusy && getGroup()->isBusy())
		return false;

	switch (eCommand)
	{
	case COMMAND_PROMOTION:
		if (canPromote((PromotionTypes)iData1, iData2))
			return true;
		break;

	case COMMAND_UPGRADE:
		if (canUpgrade(((UnitTypes)iData1), bTestVisible))
			return true;
		break;

	case COMMAND_AUTOMATE:
		if (canAutomate((AutomateTypes)iData1))
			return true;
		break;

	case COMMAND_WAKE:
		if (!isAutomated() && isWaiting())
			return true;
		break;

	case COMMAND_CANCEL:
	case COMMAND_CANCEL_ALL:
		if (!isAutomated() && getGroup()->getLengthMissionQueue() > 0)
			return true;
		break;

	case COMMAND_STOP_AUTOMATION:
		if (isAutomated())
			return true;
		break;

	case COMMAND_DELETE:
		if (canScrap())
			return true;
		break;

	case COMMAND_GIFT:
		if (canGift(bTestVisible))
			return true;
		break;

	case COMMAND_LOAD:
		if (canLoadOntoAnyUnit(getPlot(),
			/*  advc.123c: If a unit is moved onto a transport, canLoad gets
				checked before the command can be issued, and again after the unit
				has moved. Want to check whether the unit has moves left only in
				the first check (otherwise the unit moves onto the water tile,
				but isn't actually loaded).
				bTestVisible is (apparently...) true before the command gets issued
				and false afterwards. */
			bTestVisible))
		{
			return true;
		}
		break;

	case COMMAND_LOAD_UNIT:
	{
		CvUnit const* pUnit = ::getUnit(IDInfo(((PlayerTypes)iData1), iData2));
		if (pUnit != NULL && canLoadOnto(*pUnit, getPlot()))
			return true;
		break;
	}
	case COMMAND_UNLOAD:
		if (canUnload())
			return true;
		break;

	case COMMAND_UNLOAD_ALL:
		if (canUnloadAll())
			return true;
		break;

	case COMMAND_HOTKEY:
		if (isGroupHead())
			return true;
		break;

	default:
		FAssert(false);
	}

	return false;
}


void CvUnit::doCommand(CommandTypes eCommand, int iData1, int iData2)
{
	FAssert(getOwner() != NO_PLAYER);

	bool bCycle = false;

	if (canDoCommand(eCommand, iData1, iData2))
	{
		switch (eCommand)
		{
		case COMMAND_PROMOTION:
			promote((PromotionTypes)iData1, iData2);
			break;

		case COMMAND_UPGRADE:
			upgrade((UnitTypes)iData1);
			bCycle = true;
			break;

		case COMMAND_AUTOMATE:
			automate((AutomateTypes)iData1);
			bCycle = true;
			break;

		case COMMAND_WAKE:
			getGroup()->setActivityType(ACTIVITY_AWAKE);
			break;

		case COMMAND_CANCEL:
			getGroup()->popMission();
			break;

		case COMMAND_CANCEL_ALL:
			getGroup()->clearMissionQueue();
			break;

		case COMMAND_STOP_AUTOMATION:
			getGroup()->setAutomateType(NO_AUTOMATE);
			break;

		case COMMAND_DELETE:
			scrap();
			bCycle = true;
			break;

		case COMMAND_GIFT:
			gift();
			bCycle = true;
			break;

		case COMMAND_LOAD:
			load();
			bCycle = true;
			break;

		case COMMAND_LOAD_UNIT: {
			CvUnit* pUnit = ::getUnit(IDInfo(((PlayerTypes)iData1), iData2));
			if (pUnit != NULL)
			{
				loadOnto(*pUnit);
				bCycle = true;
			}
			break;
		}
		case COMMAND_UNLOAD:
			unload();
			bCycle = true;
			break;

		case COMMAND_UNLOAD_ALL:
			unloadAll();
			bCycle = true;
			break;

		case COMMAND_HOTKEY:
			setHotKeyNumber(iData1);
			break;

		default:
			FAssert(false);
			break;
		}
	}

	if (bCycle && IsSelected())
		GC.getGame().cycleSelectionGroups_delayed(1, false);

	getGroup()->doDelayedDeath();
}

// Disabled by K-Mod. (This function is deprecated.)
/* FAStarNode* CvUnit::getPathLastNode() const
{
	return getGroup()->getPathLastNode();
} */


CvPlot& CvUnit::getPathEndTurnPlot() const
{
	return getGroup()->getPathEndTurnPlot();
}


bool CvUnit::generatePath(CvPlot const& kTo, MovementFlags eFlags, bool bReuse,
	int* piPathTurns, int iMaxPath, /* <advc.128> */ bool bUseTempFinder) const
{
	return getGroup()->generatePath(getPlot(), kTo, eFlags, bReuse, piPathTurns,
			iMaxPath, bUseTempFinder);
}

// K-Mod: Return the standard pathfinder, for extracting path information.
GroupPathFinder& CvUnit::getPathFinder() const
{
	return CvSelectionGroup::pathFinder();
}

// advc: Wrapper for brevity
void CvUnit::pushGroupMoveTo(CvPlot const& kTo, MovementFlags eFlags,
	bool bAppend, bool bManual, MissionAITypes eMissionAI,
	CvPlot const* pMissionAIPlot, CvUnit const* pMissionAIUnit,
	bool bModified)
{
	FAssert(!at(kTo));
	getGroup()->pushMission(MISSION_MOVE_TO, kTo.getX(), kTo.getY(), eFlags,
			bAppend, bManual, eMissionAI, pMissionAIPlot, pMissionAIUnit, bModified);
}


bool CvUnit::canEnterTerritory(TeamTypes eTeam, bool bIgnoreRightOfPassage,
	CvArea const* pArea) const // advc.030
{
	// <advc.030> Moved from deleted function "canEnterArea" (that name was confusing)
	if (pArea != NULL && isBarbarian() && DOMAIN_LAND == getDomainType() &&
		eTeam != NO_TEAM && eTeam != getTeam() && pArea->isBorderObstacle(eTeam))
	{
		return false;
	} // </advc.030>

	// doc: can always enter territory while having no cities to facilitate spawns
	if (!GET_PLAYER(getOwner()).isBarbarian() && GET_PLAYER(getOwner()).getNumCities() == 0)
	    return true;

	// doc: Turkic UP
	if (isBarbarian() && GET_PLAYER(GET_TEAM(eTeam).getLeaderID()).getCivilizationType() == TURKS)
	{
	    if (!GET_TEAM(eTeam).isAtWarWithMajorPlayer())
	        return false;
	}

	if (GET_TEAM(getTeam()).isFriendlyTerritory(eTeam) || eTeam == NO_TEAM ||
		isEnemy(eTeam) || isRivalTerritory() ||
		alwaysInvisible() || m_pUnitInfo->isHiddenNationality())
	{
		return true;
	}

	if (!bIgnoreRightOfPassage)
	{
		if (GET_TEAM(getTeam()).isOpenBorders(eTeam) ||
			GET_TEAM(getTeam()).isDisengage(eTeam)) // advc.034
		{
			return true;
		}
	}

	// doc: explorer, civilian and naval units can enter independent territory
	if (GET_TEAM(eTeam).isMinorCiv())
	{
	    if (isNoBadGoodies())
	        return true;
	    if (!canFight())
	        return true;
	    if (getDomainType() == DOMAIN_SEA)
	        return true;
	}

	return false;
}

// Returns the ID of the team to declare war against
TeamTypes CvUnit::getDeclareWarMove(const CvPlot* pPlot) const
{
	FAssert(isHuman());

	if(getDomainType() == DOMAIN_AIR)
		return NO_TEAM;

	TeamTypes eRevealedTeam = pPlot->getRevealedTeam(getTeam(), false);

	if (eRevealedTeam != NO_TEAM)
	{
		if (!canEnterTerritory(eRevealedTeam, false, pPlot->area()) ||
			(getDomainType() == DOMAIN_SEA && /* advc.opt: */ hasCargo() &&
			!canCargoEnterTerritory(eRevealedTeam, false, pPlot->getArea()) &&
			getGroup()->isAmphibPlot(pPlot)))
		{
			if (GET_TEAM(getTeam()).canDeclareWar(pPlot->getTeam()))
				return eRevealedTeam;
		}
	}
	else
	{
		if (pPlot->isActiveVisible(false))
		{
			//if (canMoveInto(pPlot, true, true, true))
			/*	K-Mod. Don't give the "declare war" popup unless we
				need war to move into the plot */
			if (canMoveInto(*pPlot, true, true, true, false) &&
				!canMoveInto(*pPlot, false, false, false, false))
			// K-Mod end
			{
				CvUnit const* pUnit = pPlot->plotCheck(PUF_canDeclareWar,
						getOwner(), isAlwaysHostile(*pPlot),
						NO_PLAYER, NO_TEAM, PUF_isVisible, getOwner());
				if (pUnit != NULL)
					return pUnit->getTeam();
			}
		}
	}
	return NO_TEAM;
}

// advc: Renamed from "willRevealByMove" (misleading). Param changed to reference.
bool CvUnit::willRevealAnyPlotFrom(CvPlot const& kFrom) const
{
	for (SquareIter it(kFrom, visibilityRange() + 1); it.hasNext(); ++it)
	{
		CvPlot const& kLoopPlot = *it;
		if (!kLoopPlot.isRevealed(getTeam()) && kFrom.canSeePlot(
			&kLoopPlot, getTeam(), visibilityRange()))
		{
			return true;
		}
	}
	return false;
}

/*  K-Mod. I've rearranged a few things to make the function slightly faster
	(advc.opt: reverted a little of that), and added "bAssumeVisible" which
	signals that we should check for units on the plot regardless of whether we
	can actually see. */
bool CvUnit::canMoveInto(CvPlot const& kPlot, bool bAttack, bool bDeclareWar,
	bool bIgnoreLoad, bool bAssumeVisible,
	bool bDangerCheck) const // advc.001k
{
	//PROFILE_FUNC(); // advc.003o

	if (atPlot(&kPlot))
		return false;
	if (kPlot.isImpassable() && !canMoveImpassable())
		return false;
	if (m_pUnitInfo->isNoRevealMap() && willRevealAnyPlotFrom(kPlot))
		return false;

	if (isSpy() && GC.getDefineBOOL(CvGlobals::USE_SPIES_NO_ENTER_BORDERS))
	{
		if (kPlot.getOwner() != NO_PLAYER &&
			!GET_PLAYER(getOwner()).canSpiesEnterBorders(kPlot.getOwner()))
		{
			return false;
		}
	}

	// doc: protect newborn civilizations from barbarians
	if (isBarbarian() || GET_PLAYER(getOwner()).isMinorCiv())
	{
	    if (kPlot.isBirthProtected() && !(kPlot.isCity() && kPlot.getPlotCity()->getOwner() == getOwner()))
	        return false;
	}

	TeamTypes ePlotTeam = kPlot.getTeam();
	CvTeamAI const& kOurTeam = GET_TEAM(getTeam());
	bool bCanEnterTerritory = canEnterTerritory(ePlotTeam, false, kPlot.area());
	if (bCanEnterTerritory)
	{
		if (kPlot.isFeature() &&
			m_pUnitInfo->getFeatureImpassable(kPlot.getFeatureType()) &&
            !kPlot.isImproved() && // doc: can enter improved impassable feature
            !bAttack) // doc: can attack into impassable feature
		{
			TechTypes eTech = m_pUnitInfo->getFeaturePassableTech(kPlot.getFeatureType());
			if (eTech == NO_TECH || !kOurTeam.isHasTech(eTech))
			{
				// sea units can enter impassable in own cultural borders
				// advc.057: Make this exception for units of all domains
				if (//DOMAIN_SEA != getDomainType() ||
					ePlotTeam != kOurTeam.getID())
				{
					return false;
				}
			}
		}
		if (m_pUnitInfo->getTerrainImpassable(kPlot.getTerrainType()) &&
            (!kPlot.isFeature() || !GC.getInfo(kPlot.getFeatureType()).isMakesPassable())) // doc: feature makes terrain passable
		{
			TechTypes eTech = m_pUnitInfo->getTerrainPassableTech(kPlot.getTerrainType());
			if (eTech == NO_TECH || !kOurTeam.isHasTech(eTech))
			{
				if (/*DOMAIN_SEA != getDomainType() ||*/ // advc.057
					(kPlot.getTeam() != kOurTeam.getID() && !canFound(&kPlot)) || // doc: settlers can enter plots they can found on
                    (!bAttack && !canEnterTerritory(kPlot.getTeam()))) // doc: can enter passable territory controlled by enemy
				{
					if (bIgnoreLoad || !canLoadOntoAnyUnit(kPlot))
						return false;
				}
			}
		}
	}

	switch (getDomainType())
	{
	case DOMAIN_SEA:
		/*if (!kPlot.isWater() && !canMoveAllTerrain()) {
			if (!kPlot.isFriendlyCity(*this, true) || !kPlot.isCoastalLand())
				return false;
		}*/
		// <advc.183>
		if (!kPlot.isWater() && // for performance
			/*	Check visibility even if bAssumeVisible; otherwise info about
				fogged forts is leaked. */
			(!isRevealedPlotValid(kPlot) || !kPlot.isCoastalLand())) // </advc.183>
		{
			return false;
		} // </advc>
		break;

	case DOMAIN_AIR:
	{
		if (bAttack)
			break;
		bool bValid = false;
		//if (kPlot.isFriendlyCity(*this, true))
		// advc.183: (see previous comment)
        // TODO: adjust CvTeam::isKnownAirbase to check isAlliedCity or isRivalTerritory and city
		if (!kPlot.isWater() && isRevealedPlotValid(kPlot))
		{
			bValid = true;
			// <advc.001b> Support AirUnitCap > 1
			if (kPlot.airUnitSpaceAvailable(kOurTeam.getID()) <
				m_pUnitInfo->getAirUnitCap()) // </advc.001b>
			{
				bValid = false;
			}
		}
		if (!bValid)
		{
			if (bIgnoreLoad || !canLoadOntoAnyUnit(kPlot))
				return false;
		}
		break;
	}
	case DOMAIN_LAND:
		//if (kPlot.isWater() && !canMoveAllTerrain())
		if (!isValidDomain(kPlot.isWater())) // advc
		{
			if (!kPlot.isCity() || !GC.getDefineBOOL(CvGlobals::LAND_UNITS_CAN_ATTACK_WATER_CITIES))
			{
				//if (bIgnoreLoad || !isHuman() || kPlot.isWater() || !canLoad(&kPlot))
				// K-Mod. (AI might want to load into a boat on the coast)
				if (bIgnoreLoad || getPlot().isWater() || !canLoadOntoAnyUnit(kPlot))
					return false;
			}
		}

        // doc: hidden nationality units on land
		if (!bAttack && kPlot.isCity() && isAlwaysHostile(kPlot) && !atWar(getTeam(), kPlot.getTeam()))
			return false;
		break;

	case DOMAIN_IMMOBILE:
		return false;

	default:
		FAssert(false);
	}

	if (isAnimal())
	{
		if (kPlot.isOwned())
			return false;

		if (!bAttack)
		{
			if(kPlot.getBonusType() != NO_BONUS &&
				GC.getInfo(kPlot.getBonusType()).getTechReveal() == NO_TECH) // advc.309
			{
				return false;
			}
			if(kPlot.isImproved() &&
				GC.getInfo(kPlot.getImprovementType()).isGoody()) // advc.309
			{
				return false;
			}
			if (kPlot.getNumUnits() > 0)
				return false;
		}
	}

	if (isNoCityCapture())
	{
		if (!bAttack && isEnemyCity(kPlot))
			return false;
		// K-Mod. Don't let noCapture units attack defenseless cities. (eg. cities with a worker in them)
		/*if (pPlot->isEnemyCity(*this)) {
			if (!bAttack || !pPlot->isVisibleEnemyDefender(this))
				return false;
 		} */
		// K-Mod end
		/* advc.001: I think my (pre-K-Mod 1.45) fix in CvSelectionGroup::groupMove
		   might be better - at least I know it (mostly) works. */
	}

	// doc: cannot capture last city of recently born civilization
	if (!bAttack && kPlot.getBirthProtected() == kPlot.getOwner())
	{
	    if (isEnemyCity(kPlot) && GET_PLAYER(kPlot.getOwner()).getNumCities() == 1)
	        return false;
	}

	// UNOFFICIAL_PATCH, Consistency, 07/23/09, jdog5000: START
	/*if (bAttack) {
		if (isMadeAttack() && !isBlitz())
			return false;
	}*/ // BtS
	// The following change makes capturing an undefended city like a attack action, it
	// cannot be done after another attack or a paradrop
	/*
	if (bAttack || (kPlot.isEnemyCity(*this) && !canCoexistWithEnemyUnit(NO_TEAM))) {
		if (//isMadeAttack() && !isBlitz()
				isMadeAllAttacks()) // advc.164
			return false;
	}*/
	// The following change makes it possible to capture defenseless units after having
	// made a previous attack or paradrop
	if (bAttack &&
		/*  advc.001k: When checking for danger, we want to know whether the
			unit will be able to attack on its next turn. Whether it has attacked
			on its most recent turn doesn't matter. */
		!bDangerCheck)
	{
		if (//isMadeAttack() && !isBlitz()
			isMadeAllAttacks() && // advc.164
			/*	advc.004: If the move won't happen until the next turn,
				then made attacks shouldn't matter - and shouldn't result
				in a red waypoint. */
			movesLeft() > 0 &&
			kPlot.isVisibleEnemyDefender(this))
		{
			return false;
		}
	}
	// UNOFFICIAL_PATCH: END

	if (getDomainType() == DOMAIN_AIR)
	{
		if (bAttack)
		{
			if (!canAirStrike(kPlot))
				return false;
		}
	}
	else
	{
		if (canAttack())
		{
			if (bAttack || !canCoexistWithEnemyUnit(NO_TEAM))
			{
				//if (!isHuman() || (kPlot.isVisible(kOurTeam.getID())))
				if (bAssumeVisible || kPlot.isVisible(kOurTeam.getID())) // K-Mod
				{
					if (kPlot.isVisibleEnemyUnit(this) != bAttack)
					{
						//FAssertMsg(isHuman() || (!bDeclareWar || (pPlot->isVisibleOtherUnit(getOwner()) != bAttack)), "hopefully not an issue, but tracking how often this is the case when we dont want to really declare war");
						/*if (!bDeclareWar || (pPlot->isVisibleOtherUnit(getOwner()) != bAttack && !(bAttack && pPlot->getPlotCity() && !isNoCityCapture())))*/ // BtS
						// K-Mod. I'm not entirely sure I understand what they were trying to do here. But I'm pretty sure it's wrong.
						// I think the rule should be that bAttack means we have to actually fight an enemy unit. Capturing an undefended city doesn't count.
						// (there is no "isVisiblePotentialEnemyUnit" function, so I just wrote the code directly.)
						if (!bAttack || !bDeclareWar || !kOurTeam.AI_mayAttack(kPlot))
						// K-Mod end
						{
							return false;
						}
					} // <advc.315>
					else if(bAttack && ( // <advc.315b>
						(m_pUnitInfo->isOnlyAttackBarbarians() &&
						kPlot.plotCheck(PUF_isPlayer, BARBARIAN_PLAYER) == NULL) ||
						// </advc.315b> <advc.315a>
						(m_pUnitInfo->isOnlyAttackAnimals() &&
						kPlot.plotCheck(PUF_isAnimal) == NULL))) // </advc.315a>
					{
						return false;
					} // </advc.315>
				}
			}

			if (bAttack)
			{
				/* CvUnit* pDefender = pPlot->getBestDefender(NO_PLAYER, getOwner(), this, true);
				if (NULL != pDefender) {
					if (!canAttack(*pDefender))
						return false;
				} */
				// K-Mod. (this is much faster.)
				if (!kPlot.hasDefender(true, NO_PLAYER, getOwner(), this, true))
					return false;
				// K-Mod end
			}
		}
		else
		{
			if (bAttack)
				return false;

			if (!canCoexistWithEnemyUnit(NO_TEAM))
			{
				//if (!isHuman() || kPlot.isVisible(getTeam()))
				if (bAssumeVisible || kPlot.isVisible(getTeam())) // K-Mod
				{
					if (isEnemyCity(kPlot))
						return false;
					if (kPlot.isVisibleEnemyUnit(this))
						return false;
				}
			}
		}

		if (isHuman()) // (should this be !bAssumeVisible? It's a bit different to the other isHuman() checks)
		{
			ePlotTeam = kPlot.getRevealedTeam(getTeam(), false);
			bCanEnterTerritory = canEnterTerritory(ePlotTeam, false, kPlot.area());
		}

		if (!bCanEnterTerritory)
		{
			FAssert(ePlotTeam != NO_TEAM);
			if (!GET_TEAM(getTeam()).canDeclareWar(ePlotTeam))
				return false;
			/*if (isHuman()) {
				if (!bDeclareWar)
					return false;
			}
			else {
				if (GET_TEAM(getTeam()).AI_isSneakAttackReady(ePlotTeam)) {
					if (!(getGroup()->AI_isDeclareWar(pPlot)))
						return false;
				}
				else return false;
			}*/
			// K-Mod. Rather than allowing the AI to move in forbidden territory when it is planning war.
			// I'm going to disallow it from doing so when _not_ planning war.
			if (!bDeclareWar)
				return false;
			else if (!isHuman())
			{
				if (!GET_TEAM(getTeam()).AI_isSneakAttackReady(ePlotTeam) ||
					!AI().AI_getGroup()->AI_isDeclareWar(kPlot))
				{
					return false;
				}
			} // K-Mod end
		}
	}
	if (GC.getPythonCaller()->cannotMoveIntoOverride(*this, kPlot))
		return false;

	return true;
}


bool CvUnit::canMoveOrAttackInto(CvPlot const& kPlot, bool bDeclareWar, // advc: 1st param was a pointer
	bool bDangerCheck) const // advc.001k
{
	return (canMoveInto(kPlot, false, bDeclareWar) || canMoveInto(kPlot, true, bDeclareWar,
			false, true, bDangerCheck)); // advc.001k
}

/* bool CvUnit::canMoveThrough(const CvPlot* pPlot, bool bDeclareWar) const
{
	return canMoveInto(pPlot, false, bDeclareWar, true);
}*/

// advc.030:
bool CvUnit::canEnterArea(CvArea const& kArea) const
{
	return kArea.canBeEntered(getArea(), this);
}

/*	advc: Replacing CvPlot::isEnemyCity(CvUnit const&).
	Just to be consistent with similar functions moved from CvPlot (see below). */
bool CvUnit::isEnemyCity(CvPlot const& kPlot) const
{
	CvCity const* pCity = kPlot.getPlotCity();
	if (pCity != NULL)
		return isEnemy(pCity->getTeam(), kPlot);
	return false;
}

/*	advc: Body from CvPlot::isValidDomainForLocation, but the combat owner part
	is from CvPlot::isFriendlyCity. Not sure if that needs to be checked here;
	it makes isPlotValid easier to implement. */
bool CvUnit::isValidDomain(CvPlot const& kPlot) const
{
	if (isValidDomain(kPlot.isWater()))
		return true;
	//return kPlot.isCity(true, getTeam());
	if (!kPlot.isOwned())
		return false; // Can't get the combat owner then
	CvTeam const& kCombatTeam = GET_TEAM(getCombatOwner(kPlot.getTeam(), kPlot));
	// Allow different rules for air bases
	switch(getDomainType())
	{
	case DOMAIN_SEA:
		return kCombatTeam.isBase(kPlot);
	case DOMAIN_AIR:
		return kCombatTeam.isAirBase(kPlot);
	}
	return false;
}

// advc:
bool CvUnit::isRevealedValidDomain(CvPlot const& kPlot) const
{
	TeamTypes const eTeam = getTeam();
	if (!kPlot.isRevealed(eTeam))
		return false;
	if (isValidDomain(kPlot.isWater()))
		return true;
	TeamTypes eRevealedPlotTeam = kPlot.getRevealedTeam(eTeam, false);
	if (eRevealedPlotTeam == NO_TEAM)
		return false;
	CvTeam const& kCombatTeam = GET_TEAM(getCombatOwner(eRevealedPlotTeam, kPlot));
	switch (getDomainType())
	{
	case DOMAIN_SEA:
		return kCombatTeam.isRevealedBase(kPlot);
	case DOMAIN_AIR:
		return kCombatTeam.isRevealedAirBase(kPlot);
	}
	return false;
}

/*	advc: Replacing CvPlot::isFriendlyCity
	(which was always being called with bCheckImprovement=true).
	Despite the name, isFriendlyCity had not required
	CvTeam::isFriendlyTerritory, and neither does isPlotValid. */
bool CvUnit::isPlotValid(CvPlot const& kPlot) const
{
	PROFILE_FUNC(); // (currently not called at all)
	if (!isValidDomain(kPlot))
		return false;
	if (isValidDomain(kPlot.isWater()))
		return true;
	// Can't attack into plots that don't match the unit's domain
	if (kPlot.isVisibleEnemyUnit(this))
		return false;
	if (kPlot.isOwned() && isEnemy(kPlot.getTeam()))
		return false;
	return true;
}

// advc:
bool CvUnit::isRevealedPlotValid(CvPlot const& kPlot) const
{
	//PROFILE_FUNC(); // Called frequently, but not frequently enough to be a concern.
	if (!isRevealedValidDomain(kPlot))
		return false;
	if (isValidDomain(kPlot.isWater()))
		return true;
	TeamTypes const eTeam = getTeam();
	if (kPlot.isVisible(eTeam) && kPlot.isVisibleEnemyUnit(this))
		return false;
	TeamTypes eRevealedPlotTeam = kPlot.getRevealedTeam(eTeam, false);
	return (eRevealedPlotTeam == NO_TEAM || !isEnemy(eRevealedPlotTeam));
}

// advc.162:
bool CvUnit::isInvasionMove(CvPlot const& kFrom, CvPlot const& kTo) const
{
	// Redundant; only to save time when it's disabled.
	if (!GC.getDefineBOOL(CvGlobals::SPEND_ALL_MOVES_ON_INVASION))
		return false;
	TeamTypes eToTeam = kTo.getTeam();
	if(eToTeam == NO_TEAM || eToTeam == kFrom.getTeam() || isRivalTerritory())
		return false;
	DomainTypes eDomain = getDomainType();
	if(eDomain != DOMAIN_LAND && eDomain != DOMAIN_SEA)
		return false;
	if(GET_TEAM(getTeam()).hasJustDeclaredWar(eToTeam))
		return true;
	return !canEnterTerritory(eToTeam);
}


void CvUnit::attack(CvPlot* pPlot, bool bQuick, /* advc.004c: */ bool* pbIntercepted,
	bool bSeaPatrol) // advc
{
	FAssert(canMoveInto(*pPlot, true)
			// K-Mod (note): could fail in certain situations involving sea-patrol
			|| bSeaPatrol); // advc
	FAssert(getCombatTimer() == 0);
	setAttackPlot(pPlot, false);
	updateCombat(bQuick, pbIntercepted, /* advc: */ bSeaPatrol);
}

void CvUnit::fightInterceptor(CvPlot const& kPlot, bool bQuick) // advc: was CvPlot const*
{
	FAssert(getCombatTimer() == 0);
	setAttackPlot(&kPlot, true);
	updateAirCombat(bQuick);
}

void CvUnit::attackForDamage(CvUnit *pDefender,
	int attackerDamageChange, int defenderDamageChange)
{
	FAssert(getCombatTimer() == 0);
	FAssert(pDefender != NULL);
	FAssert(!isFighting());

	if(pDefender == NULL)
		return;

	setAttackPlot(pDefender->plot(), false);

	CvPlot* pPlot = getAttackPlot();
	if (pPlot == NULL)
		return;

	//rotate to face plot
	DirectionTypes newDirection = estimateDirection(this->plot(), pDefender->plot());
	if(newDirection != NO_DIRECTION)
		setFacingDirection(newDirection);

	//rotate enemy to face us
	newDirection = estimateDirection(pDefender->plot(), this->plot());
	if(newDirection != NO_DIRECTION)
		pDefender->setFacingDirection(newDirection);

	//check if quick combat
	bool bVisible = isCombatVisible(pDefender);

	//if not finished and not fighting yet, set up combat damage and mission
	if (!isFighting())
	{
		if (getPlot().isFighting() || pPlot->isFighting())
			return;

		setCombatUnit(pDefender, true);
		pDefender->setCombatUnit(this, false);
		pDefender->getGroup()->clearMissionQueue();
		bool bFocused = (bVisible && isCombatFocus() && gDLL->UI().isCombatFocus());
		if (bFocused)
		{
			DirectionTypes directionType = directionXY(getPlot(), *pPlot);
			//								N			NE				E
			NiPoint2 directions[8] = {NiPoint2(0, 1), NiPoint2(1, 1), NiPoint2(1, 0),
					// SE					S				SW					W				NW
					NiPoint2(1, -1), NiPoint2(0, -1), NiPoint2(-1, -1), NiPoint2(-1, 0), NiPoint2(-1, 1)};
			NiPoint3 attackDirection = NiPoint3(directions[directionType].x, directions[directionType].y, 0);
			float plotSize = GC.getPLOT_SIZE();
			NiPoint3 lookAtPoint(getPlot().getPoint().x + plotSize / 2 * attackDirection.x,
					getPlot().getPoint().y + plotSize / 2 * attackDirection.y,
					(getPlot().getPoint().z + pPlot->getPoint().z) / 2);
			attackDirection.Unitize();
			gDLL->UI().lookAt(lookAtPoint,
					!isActiveOwned() ||
					gDLL->getGraphicOption(GRAPHICOPTION_NO_COMBAT_ZOOM) ?
					CAMERALOOKAT_BATTLE : CAMERALOOKAT_BATTLE_ZOOM_IN,
					attackDirection);
		}
		else
		{
			PlayerTypes eAttacker = getVisualOwner(pDefender->getTeam());
			CvWString szMessage;
			if (BARBARIAN_PLAYER != eAttacker)
			{
				szMessage = gDLL->getText("TXT_KEY_MISC_YOU_UNITS_UNDER_ATTACK",
						GET_PLAYER(getOwner()).getCivilizationShortDescription()); // rfc
			}
			else
			{
				szMessage = gDLL->getText("TXT_KEY_MISC_YOU_UNITS_UNDER_ATTACK_UNKNOWN");
			}

			gDLL->UI().addMessage(pDefender->getOwner(), true, -1, szMessage, "AS2D_COMBAT",
					MESSAGE_TYPE_DISPLAY_ONLY, getButton(), GC.getColorType("RED"),
					pPlot->getX(), pPlot->getY(), true);
		}
	}

	FAssert(getPlot().isFighting());
	FAssert(pPlot->isFighting());

	//setup battle object
	CvBattleDefinition kBattle;
	kBattle.setUnit(BATTLE_UNIT_ATTACKER, this);
	kBattle.setUnit(BATTLE_UNIT_DEFENDER, pDefender);
	kBattle.setDamage(BATTLE_UNIT_ATTACKER, BATTLE_TIME_BEGIN, getDamage());
	kBattle.setDamage(BATTLE_UNIT_DEFENDER, BATTLE_TIME_BEGIN, pDefender->getDamage());

	changeDamage(attackerDamageChange, pDefender->getOwner());
	pDefender->changeDamage(defenderDamageChange, getOwner());

	if (!bVisible)
	{
		setCombatTimer(1);
		return; // advc
	}
	kBattle.setDamage(BATTLE_UNIT_ATTACKER, BATTLE_TIME_END, getDamage());
	kBattle.setDamage(BATTLE_UNIT_DEFENDER, BATTLE_TIME_END, pDefender->getDamage());
	kBattle.setAdvanceSquare(canAdvance(pPlot, 1));

	/*kBattle.addDamage(BATTLE_UNIT_ATTACKER, BATTLE_TIME_RANGED, kBattle.getDamage(BATTLE_UNIT_ATTACKER, BATTLE_TIME_BEGIN));
	kBattle.addDamage(BATTLE_UNIT_DEFENDER, BATTLE_TIME_RANGED, kBattle.getDamage(BATTLE_UNIT_DEFENDER, BATTLE_TIME_BEGIN)); */
	// K-Mod. (the original code looks wrong to me.)
	kBattle.setDamage(BATTLE_UNIT_ATTACKER, BATTLE_TIME_RANGED, kBattle.getDamage(BATTLE_UNIT_ATTACKER, BATTLE_TIME_BEGIN));
	kBattle.setDamage(BATTLE_UNIT_DEFENDER, BATTLE_TIME_RANGED, kBattle.getDamage(BATTLE_UNIT_DEFENDER, BATTLE_TIME_BEGIN));
	// K-Mod end

	//int iTurns = planBattle( kBattle);
	// K-Mod
	std::vector<int> combat_log;
	combat_log.push_back(defenderDamageChange);
	combat_log.push_back(-attackerDamageChange);
	int iTurns = planBattle(kBattle, combat_log);
	// K-Mod end
	kBattle.setMissionTime(iTurns * gDLL->getSecsPerTurn());
	setCombatTimer(iTurns);

	GC.getGame().incrementTurnTimer(getCombatTimer());

	if (pPlot->isActiveVisible(false))
	{
		ExecuteMove(0.5f, true);
		gDLL->getEntityIFace()->AddMission(&kBattle);
	}
}


void CvUnit::move(CvPlot& kPlot, bool bShow, /* advc.163: */ bool bJump, bool bGroup)
{
	FAssert(/* advc.163: */ bJump ||
			canMoveOrAttackInto(kPlot) || isMadeAttack());

	CvPlot& kOldPlot = *plot();
	// <advc.163>
	if (bJump)
		finishMoves(); // </advc.163>
	else changeMoves(kPlot.movementCost(*this, kOldPlot));
	// <advc.162>
	if (isInvasionMove(kOldPlot, kPlot))
	{
		std::vector<CvUnit*> aCargoUnits;
		getCargoUnits(aCargoUnits);
		for (size_t i = 0; i < aCargoUnits.size(); i++)
		{
			if (!aCargoUnits[i]->isRivalTerritory() &&
				aCargoUnits[i]->getDomainType() != DOMAIN_AIR)
			{
				aCargoUnits[i]->changeMoves(aCargoUnits[i]->movesLeft());
			}
		}
	} // </advc.162>
	setXY(kPlot.getX(), kPlot.getY(), /* advc.163 (was 'true'): */ bGroup,
			true, bShow && kPlot.isVisibleToWatchingHuman(), bShow);

	FeatureTypes eFeature = kPlot.getFeatureType();
	if (eFeature != NO_FEATURE)
	{
		CvFeatureInfo const& kFeature = GC.getInfo(eFeature);
		/*	change feature
			(advc note: This mechanism was apparently added for the bundled
			Afterworld mod) */
		CvString szFeature(kFeature.getOnUnitChangeTo());
		if (!szFeature.IsEmpty())
		{
			FeatureTypes eNewFeature = (FeatureTypes)GC.getInfoTypeForString(szFeature);
			kPlot.setFeatureType(eNewFeature);
		}
		// spawn birds if trees present - JW
		if (isActiveOwned() && !kPlot.isOwned() &&
			GC.getASyncRand().get(100) < kFeature.getEffectProbability())
		{
			EffectTypes eEffect = (EffectTypes)
					GC.getInfoTypeForString(kFeature.getEffectType());
			NiPoint3 pt = kPlot.getPoint();
			gDLL->getEngineIFace()->TriggerEffect(eEffect, pt, (float)
					GC.getASyncRand().get(360));
			gDLL->UI().playGeneralSound("AS3D_UN_BIRDS_SCATTER", pt);
		}
	}
	CvEventReporter::getInstance().unitMove(&kPlot, this, &kOldPlot);
}

// returns false if unit is killed
bool CvUnit::jumpToNearestValidPlot(/* K-Mod: */ bool bGroup, bool bForceMove,
	bool bFreeMove) // advc.163
{
	FAssert(!isAttacking());
	FAssert(!isFighting());

	CvCity* pNearestCity = GC.getMap().findCity(getX(), getY(), getOwner());
	CvPlot* pBestPlot = NULL;
	int iBestValue = MAX_INT;
	for (int i = 0; i < GC.getMap().numPlots(); i++)
	{
		CvPlot& kLoopPlot = GC.getMap().getPlotByIndex(i);
		if (//kLoopPlot.isValidDomainForLocation(*this)
			isRevealedValidDomain(kLoopPlot) && // advc
			canEnterTerritory(kLoopPlot.getTeam(), false, kLoopPlot.area()) &&
			canMoveInto(kLoopPlot) &&
			!isEnemy(kLoopPlot))
		{
			FAssert(!atPlot(&kLoopPlot));
			if (!kLoopPlot.isRevealed(getTeam())) // advc.opt: Moved up
				continue;
			/*if (getDomainType() == DOMAIN_AIR &&
				//!kLoopPlot.isFriendlyCity(*this, true))
				!GET_TEAM(getTeam()).isRevealedAirBase(kLoopPlot))
			{
				continue;
			}*/ // advc: canMoveInto already checks thats
			int iValue = (plotDistance(plot(), &kLoopPlot) * 2);
			// K-Mod, 2/jan/11 - bForceMove functionality
			if (bForceMove && iValue == 0)
				continue; // K-Mod end
			if (pNearestCity != NULL)
				iValue += ::plotDistance(&kLoopPlot, pNearestCity->plot());
			// <advc.opt>
			if(iValue >= iBestValue)
				continue; // </advc.opt>
			if (getDomainType() == DOMAIN_SEA && !getPlot().isWater())
			{
				if (!kLoopPlot.isWater() || !kLoopPlot.isAdjacentToArea(getArea()))
					iValue *= 3;
			}
			else
			{
				if (!kLoopPlot.isArea(getArea()))
				{
					//iValue *= 3;
					// <advc.046>
					int iMult = 3;
					if(kLoopPlot.getArea().getCitiesPerPlayer(getOwner()) <= 0)
					{
						iValue += 4;
						iMult += 1;
						if(kLoopPlot.getArea().getNumCities() == 0)
							iValue += 6;
					}
					iValue *= iMult; // </advc.046>
				}
			} // <advc.046> Perhaps not really needed, but can't hurt.
			if(kLoopPlot.isLake() && !getPlot().isLake())
				iValue *= 2; // </advc.046>
			if (iValue < iBestValue)
			{
				iBestValue = iValue;
				pBestPlot = &kLoopPlot;
			}
		}
	}
	bool bValid = true;
	if (pBestPlot != NULL)
	{
		// K-Mod. If a unit is bumped, we should clear their mission queue
		if(!atPlot(pBestPlot))
		{
			CvSelectionGroup* pGroup = getGroup();
			//pGroup->splitGroup(1); // advc.163: Safer to split? Hopefully no need.
			pGroup->clearMissionQueue();
			// K-Mod end
			// <advc.163>
			if(!isHuman())
				pGroup->AI().AI_cancelGroupAttack(); // Maybe not needed, but doesn't hurt.
			pGroup->setAutomateType(NO_AUTOMATE);
			pGroup->setActivityType(ACTIVITY_AWAKE); // </advc.163>
		}
		if (bFreeMove) // advc.163
			setXY(pBestPlot->getX(), pBestPlot->getY(), bGroup);
		else move(*pBestPlot, true, true, bGroup); // advc.163
	}
	else
	{
		kill(false);
		bValid = false;
	}
	return bValid;
}


bool CvUnit::canAutomate(AutomateTypes eAutomate) const
{
	if (eAutomate == NO_AUTOMATE)
		return false;

	/*if (!isGroupHead())
		return false; */ // disabled by K-Mod

	switch (eAutomate)
	{
	case AUTOMATE_BUILD:
		if (!isWorker())
			return false;
		break;
	case AUTOMATE_NETWORK:
		if (AI_getUnitAIType() != UNITAI_WORKER || !canBuildRoute())
			return false;
		break;
	case AUTOMATE_CITY:
		if (AI_getUnitAIType() != UNITAI_WORKER)
			return false;
		break;
	case AUTOMATE_EXPLORE:
		/*if ((!canFight() && (getDomainType() != DOMAIN_SEA)) || (getDomainType() == DOMAIN_AIR) || (getDomainType() == DOMAIN_IMMOBILE))
			return false;
		break;*/ // BtS
		switch (getDomainType())
		{
		case DOMAIN_IMMOBILE:
			return false;
		case DOMAIN_LAND:
			return canFight() || isSpy() || alwaysInvisible();
		case DOMAIN_AIR:
			return canRecon(NULL);
		default: // sea
			return true;
		}
		break;
	case AUTOMATE_RELIGION:
		if (AI_getUnitAIType() != UNITAI_MISSIONARY)
			return false;
		break;
	default:
		FAssert(false);
	}
	return true;
}


void CvUnit::automate(AutomateTypes eAutomate)
{
	if (!canAutomate(eAutomate))
		return;

	getGroup()->setAutomateType(eAutomate);
	// K-Mod. I'd like for the unit to automate immediately after the command is given, just so that the UI seems responsive. But doing so is potentially problematic.
	if (isGroupHead() && GET_PLAYER(getOwner()).isTurnActive() && getGroup()->readyToMove())
	{
		// unfortunately, CvSelectionGroup::AI_update can kill the unit, and CvUnit::automate currently isn't allowed to kill the unit.
		// CvUnit::AI_update should be ok; but using it here makes me a bit uncomfortable because it doesn't include all the checks and conditions of the group update.
		// ...too bad.
		AI().AI_update();
	}
	// K-Mod end
}


bool CvUnit::canScrap() const
{
	if (getPlot().isFighting())
		return false;
	return true;
}


void CvUnit::scrap()
{
	if (!canScrap())
		return;
	kill(true);
}


bool CvUnit::canGift(bool bTestVisible, bool bTestTransport) /* advc: */ const
{
	CvPlot const& kPlot = getPlot();
	if (!kPlot.isOwned())
		return false;

	CvPlayerAI const& kRecipient = GET_PLAYER(kPlot.getOwner());
	if (kRecipient.getID() == getOwner())
	    return false;
	// doc: can only gift units to vassals and defensive pact partners
	if (!GET_TEAM(kPlot.getTeam()).isVassal(getTeam()) && !GET_TEAM(kPlot.getTeam()).isDefensivePact(getTeam()))
	    return false;
	// <advc.143b>
	if (isNuke())
		return false; // </advc.143b>
	// <advc.034>
	if(!GET_TEAM(getTeam()).canPeacefullyEnter(kRecipient.getTeam()))
		return false; // </advc.034>
	if (!bTestVisible && // advc.093
		(kPlot.isVisibleEnemyUnit(kRecipient.getID()) ||
		kPlot.isVisibleEnemyUnit(this)))
	{
		return false;
	}
	{
		CvUnit const* pTransport = getTransportUnit();
		if (pTransport == NULL)
		{
			//if (!kPlot.isValidDomainForLocation(*this))
			if (!isRevealedValidDomain(kPlot)) // advc
				return false;
		}
		else if (bTestTransport)
		{
			//if (pTransport->getTeam() != kRecipient.getTeam())
			if (!pTransport->isRevealedValidDomain(kPlot)) // advc
				return false;
		}
	}
	/*	advc.093: UnitClassMaking checks moved into AI_acceptUnit,
		i.e human recipients are exempted from that. */
	if (GET_TEAM(kRecipient.getTeam()).isUnitClassMaxedOut(getUnitClassType()) ||
		kRecipient.isUnitClassMaxedOut(getUnitClassType()) ||
		// <advc.001b> Enforce limit
		kPlot.airUnitSpaceAvailable(kRecipient.getTeam()) <
		m_pUnitInfo->getAirUnitCap()) // </advc.001b>
	{
		if (!bTestVisible)
			return false;
	}

	// doc: cannot gift missionaries
	FOR_EACH_ENUM(Religion)
	{
	    if (m_pUnitInfo->getReligionSpreads(eLoopReligion) > 0)
	        return false;
	}

	/* <advc.123a> Disallow gifting of missionaries that don't match the
	   (intolerant) state religion. */
	if (AI_getUnitAIType() == UNITAI_MISSIONARY &&
		!bTestVisible && kRecipient.isNoNonStateReligionSpread())
	{
		ReligionTypes eRecipientReligion = kRecipient.getStateReligion();
		FOR_EACH_ENUM(Religion)
		{
			if (m_pUnitInfo->getReligionSpreads(eLoopReligion) <= 0)
				continue;
			if (eRecipientReligion != NO_RELIGION &&
				eRecipientReligion != eLoopReligion)
			{
				return false;
			}
		}
	} // <kekm.4>
	std::vector<CvUnit*> apCargoUnits;
	getCargoUnits(apCargoUnits);
	for(size_t i = 0; i < apCargoUnits.size(); i++)
	{
		if(!apCargoUnits[i]->canGift(false, false))
			return false; // </kekm.4>
	} // </advc.123a>
	if (!bTestVisible) // advc.093
	{	// advc.opt: Moved down
		FOR_EACH_ENUM(Corporation)
		{
			if (m_pUnitInfo->getCorporationSpreads(eLoopCorporation) > 0)
				return false;
		}
	}
	// <advc.705>
	if (GC.getGame().isOption(GAMEOPTION_RISE_FALL) && !bTestVisible && isHuman() &&
		GC.getGame().getRiseFall().isCooperationRestricted(kRecipient.getID()))
	{
		return false;
	} // </advc.705>
	// advc.093: Moved down - give away AI internals last.
	if (!bTestVisible && !kRecipient.AI_acceptUnit(*this))
		return false;
	//return !::atWar(kRecipient.getTeam(), getTeam());
	return true; // advc.034: OB implies no war
}


void CvUnit::gift(bool bTestTransport)
{
	if (!canGift(false, bTestTransport))
		return;

	std::vector<CvUnit*> aCargoUnits;
	getCargoUnits(aCargoUnits);
	for (uint i = 0; i < aCargoUnits.size(); ++i)
	{
		aCargoUnits[i]->gift(false);
	}

	CvPlayerAI& kRecievingPlayer = GET_PLAYER(getPlot().getOwner()); // K-Mod
	CvUnit* pGiftUnit = kRecievingPlayer.initUnit(getUnitType(), getX(), getY(), AI_getUnitAIType());

	pGiftUnit->convert(this);

	//GET_PLAYER(pGiftUnit->getOwner()).AI_changePeacetimeGrantValue(eOwner, (pGiftUnit->getUnitInfo().getProductionCost() / 5));
	// K-Mod
	// advc.141 (commented out):
	/*if (pGiftUnit->isGoldenAge())
		kRecievingPlayer.AI_changeMemoryCount(eOwner, MEMORY_GIVE_HELP, 1);*/
	// Note: I'm not currently considering special units with < 0 production cost.
	if (pGiftUnit->canCombat()) // kekm.8: was isCombat
	{
		int iEffectiveWarRating =
				getPlot().getArea().getAreaAIType(kRecievingPlayer.getTeam()) != AREAAI_NEUTRAL ?
				GET_TEAM(kRecievingPlayer.getTeam()).AI_getWarSuccessRating() :
				(60 - (kRecievingPlayer.AI_isDoStrategy(AI_STRATEGY_ALERT1) ? 20 : 0) -
				(kRecievingPlayer.AI_isDoStrategy(AI_STRATEGY_ALERT2) ? 20 : 0));

		int iUnitValue = std::max(0, kRecievingPlayer.AI_unitValue(pGiftUnit->getUnitType(),
				pGiftUnit->AI_getUnitAIType(), getPlot().area()));
		int iBestValue = kRecievingPlayer.AI_bestAreaUnitAIValue(
				pGiftUnit->AI_getUnitAIType(), getPlot().area());

		int iGiftValue = pGiftUnit->getUnitInfo().getProductionCost() * 4 *
				std::min(300, 100*iUnitValue/std::max(1, iBestValue)) / 100;
		iGiftValue *= 100;
		iGiftValue /= std::max(20, 110 + 3*iEffectiveWarRating);

		if (iUnitValue <= iBestValue && kRecievingPlayer.AI_unitCostPerMil() >
			kRecievingPlayer.AI_maxUnitCostPerMil(getPlot().area()))
		{
			iGiftValue /= 2;
		}
		kRecievingPlayer.AI_processPeacetimeGrantValue(getOwner(), iGiftValue);
		// TODO: It would nice if there was some way this could also reduce "you refused to help us during war time", and stuff like that.
		// But I think that would probably require some additional AI memory.
	}
	else
	{
		kRecievingPlayer.AI_processPeacetimeGrantValue(
				getOwner(), pGiftUnit->getUnitInfo().getProductionCost() / 2);
	}
	// K-Mod end

	CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_GIFTED_UNIT_TO_YOU",
			GET_PLAYER(getOwner()).getNameKey(), pGiftUnit->getNameKey());
	gDLL->UI().addMessage(pGiftUnit->getOwner(), false, -1, szBuffer,
			pGiftUnit->getPlot(), "AS2D_UNITGIFTED", MESSAGE_TYPE_INFO,
			pGiftUnit->getButton());

	// Python Event
	CvEventReporter::getInstance().unitGifted(pGiftUnit, getOwner(), plot());
}

// advc: Renamed from canLoadUnit, params changed to references.
bool CvUnit::canLoadOnto(CvUnit const& kUnit, CvPlot const& kPlot,
	bool bCheckMoves) const // advc.123c
{
	if (&kUnit == this)
		return false;

	if (kUnit.getTeam() != getTeam())
		return false;

	/*  UNOFFICIAL_PATCH, Bugfix, 06/23/10, Mongoose & jdog5000: START
		(from Mongoose SDK) */
	if (isCargo() && getTransportUnit() == &kUnit)
		return false;
	// UNOFFICIAL_PATCH: END
	if (getCargo() > 0)
		return false;

	if (kUnit.isCargo())
		return false;

	if (!kUnit.cargoSpaceAvailable(getSpecialUnitType(), getDomainType()))
		return false;

	if (!kUnit.atPlot(&kPlot))
		return false;

	if (!m_pUnitInfo->isHiddenNationality() &&
		kUnit.getUnitInfo().isHiddenNationality())
	{
		return false;
	}
	if (getSpecialUnitType() != NO_SPECIALUNIT &&
		GC.getInfo(getSpecialUnitType()).isCityLoad() &&
		//!kPlot.isCity(true, getTeam)
		!GET_TEAM(getTeam()).isRevealedBase(kPlot)) // advc
	{
		return false;
	}  // <advc.123c>
	if(bCheckMoves && getDomainType() != DOMAIN_AIR && movesLeft() <= 0)
		return false; // </advc.123>
	return true;
}

// advc: Renamed from loadUnit
void CvUnit::loadOnto(CvUnit& kUnit)
{
	if (!canLoadOnto(kUnit, getPlot()))
		return;
	setTransportUnit(&kUnit);
}

bool CvUnit::shouldLoadOnMove(const CvPlot* pPlot) const
{
	if (isCargo())
		return false;

	switch (getDomainType())
	{
	case DOMAIN_LAND:
		if (pPlot->isWater() &&
			// UNOFFICIAL_PATCH, Bugfix, 10/30/09, Mongoose & jdog5000:
			!canMoveAllTerrain())
		{
			return true;
		}
		break;
	case DOMAIN_AIR:
		//if (!pPlot->isFriendlyCity(*this, true))
		if (!GET_TEAM(getTeam()).isRevealedAirBase(*pPlot)) // advc
			return true;
		// advc.001b: Support AirUnitCap > 1
		if (pPlot->airUnitSpaceAvailable(getTeam()) < m_pUnitInfo->getAirUnitCap())
			return true;
		break;
	}

	if (m_pUnitInfo->getTerrainImpassable(pPlot->getTerrainType()))
	{
		TechTypes eTech = m_pUnitInfo->getTerrainPassableTech(pPlot->getTerrainType());
		if (NO_TECH == eTech || !GET_TEAM(getTeam()).isHasTech(eTech))
			return true;
	}

	return false;
}

// advc: Renamed from "canLoad"; param changed to reference.
bool CvUnit::canLoadOntoAnyUnit(CvPlot const& kPlot, /* advc.123c: */ bool bCheckMoves) const
{
	//PROFILE_FUNC(); // advc.003o
	FOR_EACH_UNIT_IN(pTransport, kPlot)
	{
		if(canLoadOnto(*pTransport, kPlot, /* advc.123c: */ bCheckMoves))
			return true;
	}
	return false;
}


void CvUnit::load()
{
	if (!canLoadOntoAnyUnit(getPlot()))
		return;

	for (int iPass = 0; iPass < 2; iPass++)
	{
		FOR_EACH_UNIT_VAR_IN(pUnit, getPlot())
		{
			if (canLoadOnto(*pUnit, getPlot()))
			{
				if (iPass == 0 ?
					(pUnit->getOwner() == getOwner()) :
					(pUnit->getTeam() == getTeam()))
				{
					setTransportUnit(pUnit);
					break;
				}
			}
		}
		if (isCargo())
			break;
	}
}


bool CvUnit::canUnload() const
{
	if (getTransportUnit() == NULL)
		return false;
	//if (!kPlot.isValidDomainForLocation(*this))
	if (!isRevealedValidDomain(getPlot())) // advc
		return false;

	if (getDomainType() == DOMAIN_AIR /*&&
		kPlot.isFriendlyCity(*this, true)*/) // advc: Ensured by the check above
	{
		int iNumAirUnits = getPlot().countNumAirUnits(getTeam());
		CvCity* pCity = getPlot().getPlotCity();
		if (pCity != NULL)
		{
			if (iNumAirUnits >= pCity->getAirUnitCapacity(getTeam()))
				return false;
		}
		else
		{
			if (iNumAirUnits >= GC.getDefineINT(CvGlobals::CITY_AIR_UNIT_CAPACITY))
				return false;
		}
	}
	return true;
}


void CvUnit::unload()
{
	if (!canUnload())
		return;
	setTransportUnit(NULL);
}


bool CvUnit::canUnloadAll() const
{
	if (getCargo() == 0)
		return false;
	//return true;
	/*  advc.123c: Not sure if unloading at sea causes problems, but doesn't
		accomplish anything (at least not with the change to canLoadUnit) */
	return !getPlot().isWater();
}


void CvUnit::unloadAll()
{
	if (!canUnloadAll())
		return;

	std::vector<CvUnit*> aCargoUnits;
	getCargoUnits(aCargoUnits);
	for (uint i = 0; i < aCargoUnits.size(); ++i)
	{
		CvUnit* pCargo = aCargoUnits[i];
		if (pCargo->canUnload())
			pCargo->setTransportUnit(NULL);
		else
		{
			FAssert(isHuman() || pCargo->getDomainType() == DOMAIN_AIR);
			pCargo->getGroup()->setActivityType(ACTIVITY_AWAKE);
		}
	}
}


bool CvUnit::canSleep(const CvPlot* pPlot) const
{
	if (isFortifyable())
		return false;

	//if (isWaiting())
	if (getGroup()->getActivityType() == ACTIVITY_SLEEP) // K-Mod
		return false;

	return true;
}


bool CvUnit::canFortify(const CvPlot* pPlot) const
{
	if (!isFortifyable())
		return false;

	//if (isWaiting())
	if (getGroup()->getActivityType() == ACTIVITY_SLEEP) // K-Mod
		return false;

	return true;
}


bool CvUnit::canAirPatrol(const CvPlot* pPlot) const
{
	if (getDomainType() != DOMAIN_AIR)
		return false;

	if (!canAirDefend(pPlot))
		return false;

	//if (isWaiting())
	if (getGroup()->getActivityType() == ACTIVITY_INTERCEPT) // K-Mod
		return false;

	return true;
}


bool CvUnit::canSeaPatrol(CvPlot const* pPlot, /* advc: */ bool bCheckActivity) const
{
	CvPlot const& kPlot = (pPlot == NULL ? getPlot() : *pPlot); // advc
	if (!kPlot.isWater())
		return false;
	if (getDomainType() != DOMAIN_SEA)
		return false;
	if (!canFight() || isOnlyDefensive())
		return false;
	// <advc.004k>
	// Will need pillager to attack us, unlikely to work under Ice.
	if (kPlot.isImpassable())
		return false;
	bool bValid = false;
	for (SquareIter itOther(kPlot, GC.getMAX_SEA_PATROL_RANGE(), false);
		!bValid && itOther.hasNext(); ++itOther)
	{
		if (canReachBySeaPatrol(*itOther, &kPlot))
			bValid = true;
	}
	if (!bValid)
		return false; // </advc.004k>
	if (bCheckActivity && isSeaPatrolling()) // advc
		return false;
	return true;
}

// advc:
bool CvUnit::isSeaPatrolling() const
{
	return (//isWaiting() // BtS
			// K-Mod: (advc - cut from canSeaPatrol)
			getGroup()->getActivityType() == ACTIVITY_PATROL &&
			getDomainType() == DOMAIN_SEA);
}

// advc.004k:
bool CvUnit::canReachBySeaPatrol(CvPlot const& kDest, CvPlot const* pFrom) const
{
	CvPlot const& kFrom = (pFrom == NULL ? getPlot() : *pFrom);
	int iDist = stepDistance(&kFrom, &kDest);
	return (iDist <= GC.getMAX_SEA_PATROL_RANGE() && iDist > 0 &&
			kDest.isWater() && kDest.getTeam() == getTeam() &&
			kDest.getRevealedImprovementType(getTeam()) != NO_IMPROVEMENT &&
			!GC.getMap().isSeparatedByIsthmus(kFrom, kDest));
}


void CvUnit::airCircle(bool bStart)
{
	if (!GC.IsGraphicsInitialized())
		return;

	if (getDomainType() != DOMAIN_AIR || maxInterceptionProbability() == 0)
		return;

	//cancel previos missions
	gDLL->getEntityIFace()->RemoveUnitFromBattle(this);

	// doc: option to hide air circling
	if (GET_PLAYER(getOwner()).isOption(PLAYEROPTION_HIDE_AIR_CIRCLING))
		return;

	if (bStart)
	{
		CvAirMissionDefinition kDefinition;
		kDefinition.setPlot(plot());
		kDefinition.setUnit(BATTLE_UNIT_ATTACKER, this);
		kDefinition.setUnit(BATTLE_UNIT_DEFENDER, NULL);
		kDefinition.setMissionType(MISSION_AIRPATROL);
		kDefinition.setMissionTime(1.0f); // patrol is indefinite - time is ignored

		gDLL->getEntityIFace()->AddMission(&kDefinition);
	}
}


bool CvUnit::canHeal(const CvPlot* pPlot) const
{
	if (!isHurt())
		return false;

	//if (isWaiting())
	if (getGroup()->getActivityType() == ACTIVITY_HEAL) // K-Mod
		return false;
	// UNOFFICIAL_PATCH, 06/30/10, LunarMongoose: FeatureDamageFix
	if (healTurns(pPlot) == MAX_INT)
		return false;

	return true;
}

// advc.004l: Assumes that caller ensures canHeal
bool CvUnit::canSentryHeal(CvPlot const* pPlot) const
{
	return !GET_TEAM(getTeam()).isRevealedCityHeal(*pPlot);
}


bool CvUnit::canSentry(const CvPlot* pPlot) const
{
	if (!canDefend(pPlot))
		return false;

	//if (isWaiting())
	if (getGroup()->getActivityType() == ACTIVITY_SENTRY) // K-Mod
		return false;

	return true;
}


int CvUnit::healRate(bool bLocation, bool bUnits, CvPlot const* pAt) const
{
	PROFILE_FUNC();
	CvPlot const& kPlot = (pAt == NULL ? getPlot() : *pAt);
	// <advc.opt>
	static int const iCITY_HEAL_RATE = GC.getDefineINT("CITY_HEAL_RATE");
	static int const iFRIENDLY_HEAL_RATE = GC.getDefineINT("FRIENDLY_HEAL_RATE");
	static int const iNEUTRAL_HEAL_RATE = GC.getDefineINT("NEUTRAL_HEAL_RATE");
	static int const iENEMY_HEAL_RATE = GC.getDefineINT("ENEMY_HEAL_RATE");
	// </advc.opt>
	int iTotalHeal = 0;

	if (bLocation) // K-Mod
	{
		bool bFriendly = GET_TEAM(getTeam()).isFriendlyTerritory(kPlot.getTeam()); // advc
		//if (kPlot.isCity(true, getTeam()))
		if (GET_TEAM(getTeam()).isCityHeal(kPlot)) // advc
		{
			iTotalHeal += //iCITY_HEAL_RATE + // advc.023: Moved
					(bFriendly ? getExtraFriendlyHeal() : getExtraNeutralHeal());
			CvCity const* pCity = kPlot.getPlotCity();
			if (pCity == NULL) // fort
				iTotalHeal += iCITY_HEAL_RATE; // advc.023
			else if (!pCity->isOccupation())
				iTotalHeal += pCity->getHealRate() /* <advc.023> */ + iCITY_HEAL_RATE;
			else iTotalHeal += (bFriendly ? iFRIENDLY_HEAL_RATE : iNEUTRAL_HEAL_RATE);
			// </advc.023>
		}
	    // Leoreth: Celtic UP
	    else if (getCivilizationType() == CELTS && kPlot.getFeatureType() == FEATURE_FOREST)
	        iTotalHeal += iCITY_HEAL_RATE + getExtraFriendlyHeal();
		else
		{
			if (!bFriendly)
			{
				if (isEnemy(kPlot))
					iTotalHeal += iENEMY_HEAL_RATE + getExtraEnemyHeal();
				else iTotalHeal += iNEUTRAL_HEAL_RATE + getExtraNeutralHeal();
			}
			else iTotalHeal += iFRIENDLY_HEAL_RATE + getExtraFriendlyHeal();
		}
	}

	// doc: additional healing in birth protected territory
	if (kPlot.getBirthProtected() == getOwner())
	    iTotalHeal += iCITY_HEAL_RATE;

	if (bUnits) // K-Mod
	{
		// <XXX> optimize this (save it?)
		int iBestHeal = 0;
		FOR_EACH_UNIT_IN(pUnit, kPlot)
		{
			if (pUnit->getTeam() == getTeam()) // XXX what about alliances?
			{
				int iHeal = pUnit->getSameTileHeal();
				if (iHeal > iBestHeal)
					iBestHeal = iHeal;
			}
		}
		FOR_EACH_ADJ_PLOT(kPlot)
		{
			// advc.030: Instead check domain type below
			//if (pLoopPlot->sameArea(*pPlot)) {
			FOR_EACH_UNIT_IN(pUnit, *pAdj)
			{
				if ( // <advc.030>
					pUnit->getDomainType() == getDomainType() &&
					!pUnit->isCargo() && // </advc.030>
					pUnit->getTeam() == getTeam()) // XXX what about alliances?
					{
						int iHeal = pUnit->getAdjacentTileHeal();
						if (iHeal > iBestHeal)
							iBestHeal = iHeal;
					}
			}
		}

		iTotalHeal += iBestHeal;
		// </XXX>
	}

	return iTotalHeal;
}


int CvUnit::healTurns(CvPlot const* pAt) const
{
	if (!isHurt())
		return 0;
	int iHeal = healRate(true, true, pAt);
	// UNOFFICIAL_PATCH, Bugfix (FeatureDamageFix), 06/02/10, LunarMongoose: START
	FeatureTypes eFeature = (pAt == NULL ? getPlot() : *pAt).getFeatureType();
	if (eFeature != NO_FEATURE)
		iHeal -= GC.getInfo(eFeature).getTurnDamage();
	// UNOFFICIAL_PATCH: END
	return (iHeal > 0 ? intdiv::uceil(getDamage(), iHeal) : MAX_INT); // K-Mod/advc
}


void CvUnit::doHeal()
{
	changeDamage(-healRate());
}


bool CvUnit::canAirlift(const CvPlot* pPlot) const
{
	if (getDomainType() != DOMAIN_LAND)
		return false;
	if (hasMoved())
		return false;
	{
		CvCity* pCity = pPlot->getPlotCity();
		if (pCity == NULL)
			return false;
		if (pCity->getCurrAirlift() >= pCity->getMaxAirlift())
			return false;
		if (pCity->getTeam() != getTeam())
			return false;
	}
	return true;
}


bool CvUnit::canAirliftAt(const CvPlot* pPlot, int iX, int iY) const
{
	if (!canAirlift(pPlot))
		return false;

	CvPlot const& kTargetPlot = GC.getMap().getPlot(iX, iY);

	// canMoveInto use to be here

	CvCity* pTargetCity = kTargetPlot.getPlotCity();
	if (pTargetCity == NULL)
		return false;
	if (pTargetCity->isAirliftTargeted())
		return false;
	if (pTargetCity->getTeam() != getTeam() && !GET_TEAM(pTargetCity->getTeam()).isVassal(getTeam()))
		return false;

	if (!canMoveInto(kTargetPlot)) // moved by K-Mod
		return false;

	return true;
}


bool CvUnit::airlift(int iX, int iY)
{
	if (!canAirliftAt(plot(), iX, iY))
		return false;

	CvCity* pCity = getPlot().getPlotCity();
	FAssert(pCity != NULL);
	CvPlot* pTargetPlot = GC.getMap().plot(iX, iY);
	FAssert(pTargetPlot != NULL);
	CvCity* pTargetCity = pTargetPlot->getPlotCity();
	FAssert(pTargetCity != NULL);
	FAssert(pCity != pTargetCity);

	pCity->changeCurrAirlift(1);
	if (pTargetCity->getMaxAirlift() == 0)
		pTargetCity->setAirliftTargeted(true);

	finishMoves();

	AutomateTypes eAuto = getGroup()->getAutomateType(); // K-Mod
	setXY(pTargetPlot->getX(), pTargetPlot->getY());
	getGroup()->setAutomateType(eAuto); // K-Mod. (automated workers sometimes airlift themselves. They should stay automated.)

	return true;
}

// advc (comment): Says whether eTeam is a victim of this (nuke) unit if it nukes pPlot
bool CvUnit::isNukeVictim(const CvPlot* pPlot, TeamTypes eTeam,
	TeamTypes eObs) const // kekm.7 (advc)
{
	// kekm.7 (advc): Not OK to nuke our own cities or units
	if (!GET_TEAM(eTeam).isAlive()/* || eTeam == getTeam()*/)
		return false;

	for (SquareIter it(*pPlot, nukeRange()); it.hasNext(); ++it)
	{
		CvPlot const& kLoopPlot	= *it;
		// <kekm.7> (advc): Respect the fog of war
		TeamTypes const ePlotTeam = (eObs == NO_TEAM ? kLoopPlot.getTeam() :
				kLoopPlot.getRevealedTeam(eObs, false)); // </kekm.7>
		if (ePlotTeam == eTeam &&
			// kekm.7 (advc): OK to nuke our own land
			(eTeam != getTeam() || kLoopPlot.isCity()))
		{
			return true;
		}
		// <kekm.7> (advc)
		// Can't nuke too much non-enemy population
		if (kLoopPlot.isCity() && !isEnemy(eTeam) &&
			((eTeam == getTeam() &&
			kLoopPlot.calculateFriendlyCulturePercent(eTeam) >=
			GC.getDefineINT(CvGlobals::CITY_NUKE_CULTURE_THRESH)) ||
			eTeam == TEAMID(kLoopPlot.calculateCulturalOwner(true))))
		{
			return true;
		}
		// Not OK to nuke our own units
		if (eTeam == getTeam() && kLoopPlot.plotCheck(NULL, -1, -1, NO_PLAYER, getTeam()))
			return true; // </kekm.7>
		if (kLoopPlot.plotCheck(PUF_isCombatTeam, eTeam, getTeam()) != NULL &&
			isEnemy(eTeam)) // kekm.7
		{
			return true;
		}
	}
	return false;
}


bool CvUnit::canNukeAt(CvPlot const& kFrom, int iX, int iY,
	TeamTypes eObs) const // kekm.7 (advc)
{
	if (!canNuke(&kFrom))
		return false;

	int iDistance = plotDistance(kFrom.getX(), kFrom.getY(), iX, iY);
	if (iDistance <= nukeRange())
		return false;

	if (airRange() > 0 && iDistance > airRange())
		return false;
	// <kekm.7> (advc) Can't nuke blindly
	for (SquareIter itPlot(iX, iY, nukeRange()); itPlot.hasNext(); ++itPlot)
	{
		if (!itPlot->isRevealed(getTeam()))
			return false;
	} // </kekm.7>

	CvPlot* pTargetPlot = GC.getMap().plot(iX, iY);
	for (TeamIter<MAJOR_CIV> itTeam; itTeam.hasNext(); ++itTeam)
	{
		if (isNukeVictim(pTargetPlot, itTeam->getID(), eObs) &&
			!isEnemy(itTeam->getID(), kFrom))
		{
			return false;
		}
	}
	return true;
}


bool CvUnit::nuke(int iX, int iY)
{
	if (!canNukeAt(getPlot(), iX, iY,
		getTeam())) // kekm.7 (advc)
	{
		return false;
	}
	CvWString szBuffer;
	CvPlot& kPlot = GC.getMap().getPlot(iX, iY);

	EagerEnumMap<TeamTypes,bool> abTeamsAffected;
	for (TeamIter<ALIVE> it; it.hasNext(); ++it)
		abTeamsAffected.set(it->getID(), isNukeVictim(&kPlot, it->getID()));

	for (TeamIter<MAJOR_CIV> it; it.hasNext(); ++it) // advc.003n: Only major civs
	{
		if (abTeamsAffected.get(it->getID()) && !isEnemy(it->getID()))
		{
			//GET_TEAM(getTeam()).declareWar(it->getID(), false, WARPLAN_LIMITED);
			CvTeam::queueWar(getTeam(), it->getID(), false, WARPLAN_LIMITED); // kekm.26
		}
		CvTeam::triggerWars(); // kekm.26
	}

	// doc (Dale): nuclear bomber
	if (airBaseCombatStr() != 0)
	{
	    if (interceptTest(kPlot))
	    {
	        return true;
	    }
	}

	// <advc.650> Moved into subroutine
	CvUnit* pInterceptUnit = NULL;
	TeamTypes eBestTeam = NO_TEAM;
	int iBestInterception = nukeInterceptionChance(kPlot, NO_TEAM,
			pInterceptUnit, &eBestTeam, &abTeamsAffected);
	// </advc.650>
	setReconPlot(&kPlot);
	// <advc.002m>
	int const iMissionTime = getGroup()->nukeMissionTime();
	bool const bShortAnimation = (iMissionTime <= 8); // </advc.002m>

	if (SyncRandSuccess100(iBestInterception))
	{
		for (PlayerIter<MAJOR_CIV> it; it.hasNext(); ++it) // advc.003n: Only major civs
		{
			CvPlayer const& kObs = *it;
			// K-Mod. Only show the message to players who have met the teams involved!
			if (((GET_TEAM(getTeam()).isHasMet(kObs.getTeam()) &&
				GET_TEAM(eBestTeam).isHasMet(kObs.getTeam())) || // K-Mod end
				kObs.isSpectator())) // advc.127
			{
				szBuffer = gDLL->getText("TXT_KEY_MISC_NUKE_INTERCEPTED",
						GET_PLAYER(getOwner()).getNameKey(), getNameKey(),
						GET_TEAM(eBestTeam).getName().GetCString());
				gDLL->UI().addMessage(kObs.getID(), kObs.getID() == getOwner() ||
						!bShortAnimation, // advc.002m
						-1, szBuffer, kPlot, "AS2D_NUKE_INTERCEPTED",
						MESSAGE_TYPE_MAJOR_EVENT, getButton(), GC.getColorType("RED"));
			}
		}
		if (kPlot.isActiveVisible(false))
		{	// advc: Moved into helper class (was duplicated below)
			NukeMissionDef kMissionDef(kPlot, *this, true, iMissionTime);
			gDLL->getEntityIFace()->AddMission(&kMissionDef);
		}
        // doc: intercepting satellite is destroyed
        if (pInterceptUnit != NULL && pInterceptUnit->getSpecialUnitType() == SPECIALUNIT_SATELLITE)
            pInterceptUnit->kill(true);
		kill(true);
		// Intercepted!!! (XXX need special event for this...)
		/*	<advc.130q> The XXX comment might be trying to say that a new memory type
			should be added for intercepted nukes. Since advc.130j counts memory
			at times-2 precision, that's not really necessary; we just count the
			intercepted nuke as half a hit. */
		for (PlayerAIIter<MAJOR_CIV> itAffected; itAffected.hasNext(); ++itAffected)
		{
			if (abTeamsAffected.get(itAffected->getTeam()))
				itAffected->AI_changeMemoryCount(getOwner(), MEMORY_NUKED_US, 1);
		} // </advc.130q>
		return true;
	}

	if (kPlot.isActiveVisible(false))
	{
        // doc (Dale): nuclear bomber
		if (airBaseCombatStr() != 0)
		{
			CvAirMissionDefinition kAirMission;
			kAirMission.setMissionType(MISSION_AIRBOMB);
			kAirMission.setUnit(BATTLE_UNIT_ATTACKER, this);
			kAirMission.setUnit(BATTLE_UNIT_DEFENDER, NULL);
			kAirMission.setDamage(BATTLE_UNIT_DEFENDER, 0);
			kAirMission.setDamage(BATTLE_UNIT_ATTACKER, 0);
			kAirMission.setPlot(&kPlot);
			kAirMission.setMissionTime(GC.getInfo(MISSION_AIRBOMB).getTime() *
				gDLL->getSecsPerTurn());
			gDLL->getEntityIFace()->AddMission(&kAirMission);
		}
		else
		{
			// advc: Moved into helper class
			NukeMissionDef kMissionDef(kPlot, *this, false, iMissionTime);
			gDLL->getEntityIFace()->AddMission(&kMissionDef);
		}
	}

	setMadeAttack(true);
	setAttackPlot(&kPlot, false);

	for (TeamIter<> it; it.hasNext(); ++it)
	{
		if (!abTeamsAffected.get(it->getID()))
			continue;
		it->changeWarWeariness(getTeam(),
				100 * GC.getDefineINT("WW_HIT_BY_NUKE"));
		GET_TEAM(getTeam()).changeWarWeariness(it->getID(),
				100 * GC.getDefineINT("WW_ATTACKED_WITH_NUKE"));
		GET_TEAM(getTeam()).AI_changeWarSuccess(it->getID(),
				GC.getDefineINT("WAR_SUCCESS_NUKE"));
	}
	CvCity const* pReplayCity = NULL; // advc.106
	// <advc.130q>
	EagerEnumMap<TeamTypes,int> aiDamageScore;
	for (TeamIter<> it; it.hasNext(); ++it)
	{
		// We already know if the team is affected at all
		if (!abTeamsAffected.get(it->getID()))
			continue;
		aiDamageScore.set(it->getID(), 1);
		// How badly is it affected?
		scaled rScore = 0;
		for (SquareIter itPlot(kPlot, nukeRange()); itPlot.hasNext(); ++itPlot)
		{
			CvPlot const& kAffectedPlot = *itPlot;
			if (kAffectedPlot.getTeam() != it->getID() || !kAffectedPlot.isCity())
				continue;
			CvCity const& kAffectedCity = *kAffectedPlot.getPlotCity();
			// <advc.106>
			if (pReplayCity == NULL ||
				pReplayCity->getPopulation() < kAffectedCity.getPopulation())
			{
				pReplayCity = &kAffectedCity;
			} // </advc.106>
			rScore += GET_PLAYER(kAffectedCity.getOwner()).
					AI_razeMemoryScore(kAffectedCity);
		}
		if (rScore >= 1)
			aiDamageScore.set(it->getID(), 2);
		if (rScore > 8)
			aiDamageScore.set(it->getID(), 3);
	} // </advc.130q> // The nuked-friend loop (refactored)
	// advc.003n: Only major civs (both loops)
	for (TeamAIIter<MAJOR_CIV,NOT_SAME_TEAM_AS> itOther(getTeam());
		itOther.hasNext(); ++itOther)
	{
		CvTeamAI& kOther = *itOther;
		//if (abTeamsAffected.get(kOther.getID()))
		/*  advc.130q: Moved the is-affected case to a separate loop b/c it's now
			important to process the nuked-friend penalties first */

		for (TeamAIIter<MAJOR_CIV,NOT_SAME_TEAM_AS> itAffected(kOther.getID());
			itAffected.hasNext(); ++itAffected)
		{
			CvTeamAI const& kAffected = *itAffected;
			// <advc.130q>
			if (aiDamageScore.get(kAffected.getID()) > 1 && // was abAffected
				// Don't hate them for striking back
				GET_TEAM(getTeam()).AI_getMemoryCount(kAffected.getID(), MEMORY_NUKED_US)
				<= kAffected.AI_getMemoryCount(getTeam(), MEMORY_NUKED_US) &&
				// </advc.130q>
				kOther.isHasMet(kAffected.getID()) &&
				// advc.130h: bForced=false
				kOther.AI_getAttitude(kAffected.getID(), false) >= ATTITUDE_CAUTIOUS)
			{
				for (MemberAIIter itOtherMember(kOther.getID());
					itOtherMember.hasNext(); ++itOtherMember)
				{	// advc.130j:
					itOtherMember->AI_rememberEvent(getOwner(), MEMORY_NUKED_FRIEND);
				}
				/*  advc.130q: Don't break. If cities are just two tiles apart
					(scenario map or on different landmasses), a nuke can hit
					multiple cities of different teams. Stack the diplo penalties
					in such a case. */
				//break;
				// XXX some AI should declare war here...
				/*  advc.104: ^Moved this Firaxis comment b/c I think the DoW
					should happen here if it's implemented. Though I don't think it's
					wise to declare war on a civ that's in the process of firing nukes. */
			}
		}
	}
	// <advc.130q> The nuked-us loop (refactored)
	for (PlayerAIIter<ALIVE,NOT_SAME_TEAM_AS> itAffected(getTeam());
		itAffected.hasNext(); ++itAffected)
	{
		TeamTypes const eAffectedTeam = itAffected->getTeam();
		if (!abTeamsAffected.get(eAffectedTeam))
			continue;
		// <advc.130v>
		if (GET_TEAM(getTeam()).isCapitulated())
		{
			aiDamageScore.set(eAffectedTeam,
					scaled(aiDamageScore.get(eAffectedTeam), 2).ceil());
			itAffected->AI_changeMemoryCount(
					GET_TEAM(GET_TEAM(getTeam()).getMasterTeam()).getLeaderID(),
					MEMORY_NUKED_US, aiDamageScore.get(eAffectedTeam));
		} // </advc.130v>
		// <advc.130j>
		itAffected->AI_changeMemoryCount(getOwner(), MEMORY_NUKED_US,
				aiDamageScore.get(eAffectedTeam)); // </advc.130j>
	} // </advc.130q>

	for (PlayerIter<MAJOR_CIV> it; it.hasNext(); ++it)
	{
		CvPlayer const& kObs = *it;
		if ((GET_TEAM(kObs.getTeam()).isHasMet(getTeam()) || // K-Mod
			kObs.isSpectator())) // advc.127
		{
			szBuffer = gDLL->getText("TXT_KEY_MISC_NUKE_LAUNCHED",
					GET_PLAYER(getOwner()).getNameKey(), getNameKey());
			gDLL->UI().addMessage(kObs.getID(), kObs.getID() == getOwner() ||
					!bShortAnimation, // advc.002m
					-1, szBuffer, kPlot, "AS2D_NUKE_EXPLODES",
					MESSAGE_TYPE_MAJOR_EVENT, getButton(), GC.getColorType("RED"));
		}
	}
	// <advc.106>
	if (pReplayCity != NULL)
	{
		szBuffer = gDLL->getText("TXT_KEY_MISC_CITY_NUKED",
				pReplayCity->getNameKey(), GET_PLAYER(
				pReplayCity->getOwner()).getNameKey(),
				GET_PLAYER(getOwner()).getNameKey());
		GC.getGame().addReplayMessage(getPlot(), REPLAY_MESSAGE_MAJOR_EVENT,
				getOwner(), szBuffer, GC.getColorType("WARNING_TEXT"));
	} // </advc.106>

	if (isSuicide())
		kill(true);

	return true;
}

// advc.650:
int CvUnit::nukeInterceptionChance(CvPlot const& kTarget, TeamTypes eObs,
	CvUnit* pInterceptUnit, // Optional out-param
	TeamTypes* pBestTeam, // Optional out-param
	// Allow caller to provide set of affected teams (just to save time)
	EagerEnumMap<TeamTypes,bool> const* pTeamsAffected) const
{
	LOCAL_REF(TeamTypes, eBestTeam, pBestTeam, NO_TEAM);
	EagerEnumMap<TeamTypes,bool> abTeamsAffected_local;
	if (pTeamsAffected == NULL)
	{
		for (TeamIter<ALIVE> it; it.hasNext(); ++it)
			abTeamsAffected_local.set(it->getID(), isNukeVictim(&kTarget, it->getID(), eObs));
	}
	EagerEnumMap<TeamTypes,bool> const& abTeamsAffected = (pTeamsAffected == NULL ?
			abTeamsAffected_local : *pTeamsAffected);

	// Rest of the body cut from nuke(int,int) ...
	int iBestInterception = 0;
	FOR_EACH_ENUM(Team)
	{
		CvTeam const& kInterceptTeam = GET_TEAM(eLoopTeam);
		if (!abTeamsAffected.get(kInterceptTeam.getID()))
			continue;

        // doc: satellite interception
	    if (kInterceptTeam.canSatelliteIntercept())
	    {
	        FOR_EACH_ADJ_PLOT(kTarget)
            {
	            FOR_EACH_UNIT_VAR_IN(pUnit, *pAdj)
                {
                    if (pUnit != this && pUnit->getTeam() == eLoopTeam && pUnit->getSpecialUnitType() == SPECIALUNIT_SATELLITE)
                    {
                        pInterceptUnit = pUnit;
						eBestTeam = pUnit->getTeam();
						return 100;
                    }
                }
            }
	    }

		if (kInterceptTeam.getNukeInterception() > iBestInterception)
		{
			iBestInterception = kInterceptTeam.getNukeInterception();
			eBestTeam = kInterceptTeam.getID();
		} // <advc.143b>
		if (kInterceptTeam.isAVassal())
		{
			int iMasterChance = GET_TEAM(kInterceptTeam.getMasterTeam()).
					getNukeInterception();
			if (iMasterChance > iBestInterception)
			{
				iBestInterception = iMasterChance;
				eBestTeam = kInterceptTeam.getMasterTeam();
			}
		} // </advc.143b>
	}
	iBestInterception *= 100 - m_pUnitInfo->getEvasionProbability();
	iBestInterception /= 100;
	return range(iBestInterception, 0, 100);
}


bool CvUnit::canRecon(const CvPlot* pPlot) const
{
	if (getDomainType() != DOMAIN_AIR)
		return false;
	if (airRange() == 0)
		return false;
	if (m_pUnitInfo->isSuicide())
		return false;
	return true;
}



bool CvUnit::canReconAt(const CvPlot* pPlot, int iX, int iY) const
{
	if (!canRecon(pPlot))
		return false;
	// <advc.029> (from Dawn of Civilization)
	if (airRange() == -1)
		return true; // </advc.029>
	int iDistance = plotDistance(pPlot->getX(), pPlot->getY(), iX, iY);
	if (iDistance > airRange() || iDistance == 0)
		return false;
	return true;
}


bool CvUnit::recon(int iX, int iY)
{
	if (!canReconAt(plot(), iX, iY))
		return false;

	CvPlot* pPlot = GC.getMap().plot(iX, iY);
	setReconPlot(pPlot);
	finishMoves();

	if (pPlot->isActiveVisible(false))
	{
		CvAirMissionDefinition kAirMission;
		kAirMission.setMissionType(MISSION_RECON);
		kAirMission.setUnit(BATTLE_UNIT_ATTACKER, this);
		kAirMission.setUnit(BATTLE_UNIT_DEFENDER, NULL);
		kAirMission.setDamage(BATTLE_UNIT_DEFENDER, 0);
		kAirMission.setDamage(BATTLE_UNIT_ATTACKER, 0);
		kAirMission.setPlot(pPlot);
		kAirMission.setMissionTime(GC.getInfo((MissionTypes)MISSION_RECON).getTime() * gDLL->getSecsPerTurn());
		gDLL->getEntityIFace()->AddMission(&kAirMission);
	}

	return true;
}


bool CvUnit::canParadrop(const CvPlot* pPlot) const
{
	if (getDropRange() <= 0)
		return false;
	if (hasMoved())
		return false;
	//if (!pPlot->isFriendlyCity(*this, true))
	if (!GET_TEAM(getTeam()).isRevealedAirBase(*pPlot)) // advc
		return false;
	return true;
}



bool CvUnit::canParadropAt(const CvPlot* pPlot, int iX, int iY) const
{
	if (!canParadrop(pPlot))
		return false;

	CvPlot* pTargetPlot = GC.getMap().plot(iX, iY);

	if (pTargetPlot == NULL || pTargetPlot == pPlot)
		return false;
	if (!pTargetPlot->isVisible(getTeam()))
		return false;
	if (!canMoveInto(*pTargetPlot, false, false, true))
		return false;
	if (plotDistance(pPlot->getX(), pPlot->getY(), iX, iY) > getDropRange())
		return false;

	if (!canCoexistWithEnemyUnit(NO_TEAM))
	{
		if (isEnemyCity(*pTargetPlot))
			return false;
		if (pTargetPlot->isVisibleEnemyUnit(this))
			return false;
	}
	return true;
}


bool CvUnit::paradrop(int iX, int iY, /* <advc.004c> */ IDInfo* pInterceptor)
{
	if (pInterceptor != NULL)
		*pInterceptor = IDInfo(); // </advc.004c>
	if (!canParadropAt(plot(), iX, iY))
		return false;

	CvPlot const& kPlot = GC.getMap().getPlot(iX, iY);
	changeMoves(GC.getMOVE_DENOMINATOR() / 2);
	setMadeAttack(true);
	setXY(kPlot.getX(), kPlot.getY(), /* K-Mod: */ true);

	//check if intercepted
	if(interceptTest(kPlot, /* advc.004c: */ pInterceptor))
		return true;

	//play paradrop animation by itself
	if (kPlot.isActiveVisible(false))
	{
		CvAirMissionDefinition kAirMission;
		kAirMission.setMissionType(MISSION_PARADROP);
		kAirMission.setUnit(BATTLE_UNIT_ATTACKER, this);
		kAirMission.setUnit(BATTLE_UNIT_DEFENDER, NULL);
		kAirMission.setDamage(BATTLE_UNIT_DEFENDER, 0);
		kAirMission.setDamage(BATTLE_UNIT_ATTACKER, 0);
		kAirMission.setPlot(&kPlot);
		kAirMission.setMissionTime(GC.getInfo(MISSION_PARADROP).getTime() *
				gDLL->getSecsPerTurn());
		gDLL->getEntityIFace()->AddMission(&kAirMission);
	}

	return true;
}


bool CvUnit::canAirBomb(CvPlot const* pFrom) const
{
	// (advc: Should uncomment this if the param is ever actually used)
	/*if (pFrom == NULL)
		pFrom = plot();*/
	if (getDomainType() != DOMAIN_AIR)
		return false;
	if (airBombBaseRate() == 0)
		return false;
	if (//isMadeAttack()
		/*  advc.164: In case aircraft are ever allowed to have Blitz
			(there'd probably be other issues though) */
		isMadeAllAttacks())
	{
		return false;
	}
	return true;
}

// advc: Params swapped, 2nd one optional
bool CvUnit::canAirBombAt(CvPlot const& kTarget, CvPlot const* pFrom) const
{
	if (!canAirBomb(pFrom))
		return false;
	// <advc>
	if (pFrom == NULL)
		pFrom = plot(); // </advc>
	if (plotDistance(pFrom, &kTarget) > airRange())
		return false;
	// <advc.004c> Don't give away revealed owner to humans
	if (isHuman())
	{
		TeamTypes eRevealedTeam = kTarget.getRevealedTeam(getTeam(), false);
		if (eRevealedTeam != NO_TEAM &&
			// <advc.255> Allow bombing own routes
			(kTarget.getOwner() != getOwner() ||
			getDestructibleStructureAt(kTarget, true) != STRUCTURE_ROUTE) &&
			// </advc.255>
			!isEnemy(eRevealedTeam, kTarget))
		{
			return false;
		}
	}
	else // </advc.004c>
	{
		if (kTarget.isOwned() && !AI().AI_mayAttack(kTarget))
			return false;
	}
	{
		CvCity const* pCity = kTarget.getPlotCity();
		if (pCity != NULL &&
			// advc.004c: Don't give away unrevealed cities to humans
			(!isHuman() || pCity->isRevealed(getTeam())))
		{
			return (pCity->isBombardable(this) &&
					pCity->isRevealed(getTeam())); // K-Mod
		}
	}
	// K-Mod. Don't allow the player to bomb improvements that they don't know exist.
	// <advc.255> Moved into new function
	return (getDestructibleStructureAt(kTarget,
			/*	advc.004c: The K-Mod code still gave away improvements that have
				been removed. Instead, allow humans to make futile attacks against
				structures that no longer exist. */
			isHuman()) != NO_STRUCTURE); // </advc.255>
}

/*	advc.255: Whether the first structure that this unit could destroy in the
	target plot would be an improvement, a route or none - assuming that the unit
	has the ability to pillage or air bomb the plot (not checked). */
CvUnit::StructureTypes CvUnit::getDestructibleStructureAt(CvPlot const& kTarget,
	bool bTestVisibility,
	bool bForceImprovement) const // advc.111
{
	ImprovementTypes eImprov = (bTestVisibility ?
			kTarget.getRevealedImprovementType(getTeam()) :
			kTarget.getImprovementType());
	if (eImprov != NO_IMPROVEMENT && GC.getInfo(eImprov).isPermanent())
		eImprov = NO_IMPROVEMENT;
	RouteTypes eRoute = (bTestVisibility ?
			kTarget.getRevealedRouteType(getTeam()) :
			kTarget.getRouteType());
	if (getDomainType() == DOMAIN_AIR)
	{
		if (eImprov != NO_IMPROVEMENT && GC.getInfo(eImprov).getAirBombDefense() < 0)
			eImprov = NO_IMPROVEMENT;
		if (eRoute != NO_ROUTE && GC.getInfo(eRoute).get(CvRouteInfo::AirBombDefense) < 0)
			eRoute = NO_ROUTE;
	}
	if (eImprov == NO_IMPROVEMENT && eRoute == NO_ROUTE)
		return NO_STRUCTURE;
	// <advc.111>
	if (bForceImprovement && eImprov != NO_IMPROVEMENT)
		eRoute = NO_ROUTE; // </advc.111>
	if (getTeam() == (bTestVisibility ?
		kTarget.getRevealedTeam(getTeam(), false) : kTarget.getTeam()))
	{
		return (eRoute == NO_ROUTE ? STRUCTURE_IMPROVEMENT : STRUCTURE_ROUTE);
	}
	return (eRoute != NO_ROUTE &&
			(eImprov == NO_IMPROVEMENT || eImprov == GC.getRUINS_IMPROVEMENT()) ?
			STRUCTURE_ROUTE : STRUCTURE_IMPROVEMENT);
}

// advc: Moved out of CvUnit::airBomb
int CvUnit::airBombDefenseDamage(CvCity const& kCity) const
{
	/*  <advc.004c> Same as in damageToBombardTarget except that IgnoreBuildingDefense
		doesn't have to be checked here b/c all air units have that */
	int iDefWithBuildings = kCity.getDefenseModifier(false);
	int iDefSansBuildings = kCity.getDefenseModifier(true);
	FAssertMsg(iDefSansBuildings > 0 || isHuman(),
			"The AI shoudn't bombard cities whose def is already 0");
	return (airBombCurrRate() * scaled(iDefWithBuildings, iDefSansBuildings)).round();
}

// advc: Target plot was given as coordinates
bool CvUnit::airBomb(CvPlot& kTarget, /* advc.004c: */ bool* pbIntercepted,
	bool bForceImprovement) // advc.111
{	// <advc.004c>
	if (pbIntercepted != NULL)
		*pbIntercepted = false; // </advc.004c>
	if (!canAirBombAt(kTarget))
		return false;
	/* if (!isEnemy(kPlot.getTeam()))
		getGroup()->groupDeclareWar(pPlot, true);*/ // Disabled by K-Mod
	// advc.004c: Move this down; don't want it to fail silently.
	/*if (!isEnemy(kTarget))
		return false;*/
	if (interceptTest(kTarget))
	{	// <advc.004c>
		if (pbIntercepted != NULL)
			*pbIntercepted = true; // </advc.004c>
		return true;
	}
	CvWString szBuffer;

	CvCity* pCity = kTarget.getPlotCity();
	if (pCity != NULL)
	{
		//pCity->changeDefenseModifier(-airBombCurrRate());
		// advc.004c:
		pCity->changeDefenseModifier(-std::max(0, airBombDefenseDamage(*pCity)));
		szBuffer = gDLL->getText("TXT_KEY_MISC_YOU_DEFENSES_REDUCED_TO",
				pCity->getNameKey(), pCity->getDefenseModifier(false), getNameKey());
		gDLL->UI().addMessage(pCity->getOwner(), true, // advc.004g: was false
				-1, szBuffer, pCity->getPlot(),
				"AS2D_BOMBARDED", MESSAGE_TYPE_INFO, getButton(), GC.getColorType("RED"));
		szBuffer = gDLL->getText("TXT_KEY_MISC_ENEMY_DEFENSES_REDUCED_TO", getNameKey(),
				pCity->getNameKey(), pCity->getDefenseModifier(false));
		gDLL->UI().addMessage(getOwner(), true, -1, szBuffer, pCity->getPlot(),
				"AS2D_BOMBARD", MESSAGE_TYPE_INFO, NULL, GC.getColorType("GREEN"));
	}
	else
	{	// <advc.255>
		bool const bValidOwner = (!kTarget.isOwned() || isEnemy(kTarget) || // advc.004c
				kTarget.getOwner() == getOwner());
		StructureTypes const eStructure = getDestructibleStructureAt(kTarget, false,
				bForceImprovement); // advc.111
		if (bValidOwner && eStructure != NO_STRUCTURE)
		{
			bool const bRoute = (eStructure == STRUCTURE_ROUTE);
			wchar const* szStructure = (bRoute ?
					GC.getInfo(kTarget.getRouteType()).getTextKeyWide() :
					GC.getInfo(kTarget.getImprovementType()).getTextKeyWide());
			int const iDefense = (bRoute ?
					GC.getInfo(kTarget.getRouteType()).get(CvRouteInfo::AirBombDefense) :
					GC.getInfo(kTarget.getImprovementType()).getAirBombDefense());
			// </advc.255>
			/*	advc.004c (note): Changes to this dice roll should be matched with changes
				to the probability display in CvGameTextMgr::getAirBombPlotHelp */
			if (SyncRandNum(airBombCurrRate()) >= SyncRandNum(iDefense))
			{
				szBuffer = gDLL->getText("TXT_KEY_MISC_YOU_UNIT_DESTROYED_IMP",
						getNameKey(), szStructure);
				gDLL->UI().addMessage(getOwner(), true, -1, szBuffer, "AS2D_PILLAGE",
						MESSAGE_TYPE_INFO, getButton(), GC.getColorType("GREEN"),
						kTarget.getX(), kTarget.getY());
				if (kTarget.isOwned() &&
					kTarget.getOwner() != getOwner()) // advc.004c
				{
					szBuffer = gDLL->getText("TXT_KEY_MISC_YOU_IMP_WAS_DESTROYED",
							szStructure, getNameKey(),
							getVisualCivAdjective(kTarget.getTeam()));
					gDLL->UI().addMessage(kTarget.getOwner(), true, // advc.004g: was false
							-1, szBuffer, kTarget, "AS2D_PILLAGED", MESSAGE_TYPE_INFO,
							getButton(), GC.getColorType("RED"));
				}
				// <advc.255>
				if (bRoute)
				{
					kTarget.setRouteType(GC.getInfo(kTarget.getRouteType()).
							getRoutePillage());
				}
				else // </advc.255>
				{
					kTarget.setImprovementType(GC.getInfo(kTarget.getImprovementType()).
							getImprovementPillage());
				}
			}
			else
			{
				szBuffer = gDLL->getText("TXT_KEY_MISC_YOU_UNIT_FAIL_DESTROY_IMP",
						getNameKey(), szStructure);
				gDLL->UI().addMessage(getOwner(), true, -1, szBuffer,
						"AS2D_BOMB_FAILS", MESSAGE_TYPE_INFO, getButton(),
						GC.getColorType("RED"), kTarget.getX(), kTarget.getY());
			}
		}
		/*	<advc.004c> Can now fail when the improvement only existed in the FoW
			or when plot owner in FoW was out of date */
		else
		{
			szBuffer = gDLL->getText("TXT_KEY_MISC_AIR_BOMB_FAIL_IMP_GONE", getNameKey());
			gDLL->UI().addMessage(getOwner(), true, -1, szBuffer,
					"AS2D_BOMB_FAILS", MESSAGE_TYPE_INFO, getButton(),
					NO_COLOR, kTarget.getX(), kTarget.getY());
		} // </advc.004c>
	}

	setReconPlot(&kTarget);
	setMadeAttack(true);
	changeMoves(GC.getMOVE_DENOMINATOR());

	if (kTarget.isActiveVisible(false))
	{
		CvAirMissionDefinition kAirMission;
		kAirMission.setMissionType(MISSION_AIRBOMB);
		kAirMission.setUnit(BATTLE_UNIT_ATTACKER, this);
		kAirMission.setUnit(BATTLE_UNIT_DEFENDER, NULL);
		kAirMission.setDamage(BATTLE_UNIT_DEFENDER, 0);
		kAirMission.setDamage(BATTLE_UNIT_ATTACKER, 0);
		kAirMission.setPlot(&kTarget);
		kAirMission.setMissionTime(GC.getInfo(MISSION_AIRBOMB).getTime() *
				gDLL->getSecsPerTurn());
		gDLL->getEntityIFace()->AddMission(&kAirMission);
	}

	if (isSuicide())
		kill(true);

	return true;
}


CvCity* CvUnit::bombardTarget(CvPlot const& kFrom) const
{
	CvCity* pBestCity = NULL;
	int iBestValue = MAX_INT;
	FOR_EACH_ADJ_PLOT(kFrom)
	{
		CvCity* pLoopCity = pAdj->getPlotCity();
		if (pLoopCity == NULL || !pLoopCity->isBombardable(this))
			continue;
		int iValue = pLoopCity->getDefenseDamage();
		// always prefer cities we are at war with
		/*	advc (note): Was added in BtS. Not sure if it's correct - or necessary.
			iValue is non-negative. We're computing an argmin. CvCity::isBombardable
			already checks isEnemy - but only for this unit's current plot. */
		if (isEnemy(pLoopCity->getTeam(), kFrom))
			iValue *= 128;
		if (iValue < iBestValue)
		{
			iBestValue = iValue;
			pBestCity = pLoopCity;
		}
	}
	return pBestCity;
}


bool CvUnit::canBombard(CvPlot const& kFrom) const
{
	if (bombardRate() <= 0)
		return false;

	if (/*isMadeAttack()*/ isMadeAllAttacks()) // advc.164
		return false;

	// doc: amphibious artillery can bombard from cargo
	if (isCargo() && !isAmphib())
		return false;

	if (bombardTarget(kFrom) == NULL)
		return false;

	return true;
}

// Moved out of CvUnit::bombard (note: may exceed the target's defensive modifier)
int CvUnit::damageToBombardTarget(CvPlot const& kFrom) const
{
	CvCity const* pBombardCity = bombardTarget(kFrom);
	if (pBombardCity == NULL)
		return 0;
	// <advc.004c>
	int iDefWithBuildings = pBombardCity->getDefenseModifier(false);
	FAssertMsg(iDefWithBuildings > 0 || isHuman(),
			"The AI shoudn't bombard cities whose def is already 0");
	int iDefSansBuildings = pBombardCity->getDefenseModifier(true);
	bool const bIgnore = ignoreBuildingDefense();
	// </advc.004c>
	int iBombardModifier = 0;
	if (!bIgnore) // advc.004c
	    iBombardModifier -= pBombardCity->getBuildingBombardDefense();
	// doc: additional bombard damage if birth protected or expansion target
	if (pBombardCity->getBirthProtected() == getOwner() || pBombardCity->isExpansionEffect(getOwner()))
	    iBombardModifier += 100;
	// doc: reduced bombard damage against other birth protected target
	if (pBombardCity->isBirthProtected() && pBombardCity->getBirthProtected() != getOwner())
	    iBombardModifier -= 50;
	// <advc.004c> Same formula as in BtS (except for rounding)
	scaled rDamage = bombardRate();
	rDamage *= 1 + per100(iBombardModifier);
	rDamage.increaseTo(0);
	if (bIgnore && iDefSansBuildings > 0) /*  bIgnore doesn't just ignore
			BombardDefense, also need to decrease DefenseModifier proportional
			to the effect of buildings in order to properly ignore BuildingDefense. */
		rDamage *= scaled(iDefWithBuildings, iDefSansBuildings);
	return rDamage.round(); // </advc.004c>
}


bool CvUnit::bombard()
{
	if (!canBombard(getPlot()))
		return false;

	CvCity* pBombardCity = bombardTarget(getPlot());
	if (!isEnemy(pBombardCity->getTeam())) // (advc: simplified)
	{
		//getGroup()->groupDeclareWar(pTargetPlot, true); // Disabled by K-Mod
		return false;
	}

	bool bFirstBombardment = !pBombardCity->isBombarded(); // advc.004g
	// advc: Moved into subroutine
	pBombardCity->changeDefenseModifier(-std::max(0, damageToBombardTarget(getPlot())));
	setMadeAttack(true);
	changeMoves(GC.getMOVE_DENOMINATOR());

	CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_DEFENSES_IN_CITY_REDUCED_TO",
			getNameKey(), // advc.004g: Show unit name (idea from MNAI)
			pBombardCity->getDefenseModifier(false),
			GET_PLAYER(getOwner())./*getNameKey()*/getCivilizationAdjectiveKey(), // advc.004g
			pBombardCity->getNameKey());
	gDLL->UI().addMessage(pBombardCity->getOwner(), /* advc.004g: */ true,
			-1, szBuffer, pBombardCity->getPlot(),
			!bFirstBombardment ? NULL : // advc.004g: Don't bombard the owner with sound
			"AS2D_BOMBARDED", MESSAGE_TYPE_INFO, getButton(), GC.getColorType("RED"));
	szBuffer = gDLL->getText("TXT_KEY_MISC_YOU_REDUCE_CITY_DEFENSES",
			getNameKey(), pBombardCity->getNameKey(),
			pBombardCity->getDefenseModifier(//false
			ignoreBuildingDefense())); // advc.004g
	gDLL->UI().addMessage(getOwner(), true,
			-1, szBuffer, "AS2D_BOMBARD",
			MESSAGE_TYPE_INFO, getButton(), GC.getColorType("GREEN"),
			pBombardCity->getX(), pBombardCity->getY());

	if (getPlot().isActiveVisible(false))
	{
		CvUnit *pDefender = pBombardCity->getPlot().getBestDefender(NO_PLAYER, getOwner(), this, true);
		// Bombard entity mission
		CvMissionDefinition kDefiniton;
		kDefiniton.setMissionTime(GC.getInfo(MISSION_BOMBARD).getTime() * gDLL->getSecsPerTurn());
		kDefiniton.setMissionType(MISSION_BOMBARD);
		kDefiniton.setPlot(pBombardCity->plot());
		kDefiniton.setUnit(BATTLE_UNIT_ATTACKER, this);
		kDefiniton.setUnit(BATTLE_UNIT_DEFENDER, pDefender);
		gDLL->getEntityIFace()->AddMission(&kDefiniton);
	}
	return true;
}


bool CvUnit::canPillage(CvPlot const& kPlot) const
{
	if (!m_pUnitInfo->isPillage())
		return false;
	if (kPlot.isCity())
		return false;
	/*  UNOFFICIAL_PATCH (Bugfix), 06/23/10, Mongoose & jdog5000: START
		(from Mongoose SDK) */
	if (isCargo())
		return false;
	// UNOFFICIAL_PATCH: END
	if (!kPlot.isImproved())
	{
		if(!kPlot.isRoute())
			return false;
		// <advc.111>
		if(kPlot.getOwner() == NO_PLAYER &&
			kPlot.isVisibleOtherUnit(getOwner()))
		{
			return false;
		} // </advc.111>
	}
	else
	{
		if (GC.getInfo(kPlot.getImprovementType()).isPermanent())
			return false;
		/*  <advc.005c> Builds on top of Ruins are OK; hence don't want to set
			Ruins to bPermanent in XML. */
		if (kPlot.getImprovementType() == GC.getRUINS_IMPROVEMENT())
			return false; // </advc.005c>
	}

	if (kPlot.isOwned())
	{
		/*	advc: There should be no AI code here, but that's not my doing. I've only
			moved (and renamed) CvUnit::potentialWarAction. See also canAirBombAt. */
		if (!AI().AI_mayAttack(kPlot))
		{	//if ((pPlot->getImprovementType() == NO_IMPROVEMENT) || (pPlot->getOwner() != getOwner())) // BtS
			/*  K-Mod, 16/dec/10, karadoc
				enabled the pillaging of own roads */
			if (kPlot.getOwner() != getOwner() ||
				(!kPlot.isImproved() && !kPlot.isRoute()))
			{
				return false;
			}
		} // <advc.033>
		if(GET_TEAM(kPlot.getTeam()).isVassal(getTeam()) ||
			GET_TEAM(getTeam()).isVassal(kPlot.getTeam()))
		{
			return false;
		} // </advc.033>
	}

	if (!isValidDomain(kPlot.isWater()))
		return false;

	return true;
}


bool CvUnit::pillage(/* advc.111: */ bool bForceImprovement)
{
	CvPlot& kPlot = getPlot();
	if (!canPillage(kPlot))
		return false;

	if (kPlot.isOwned())
	{
		// we should not be calling this without declaring war first, so do not declare war here
		if (!isEnemy(kPlot))
		{	//if ((kPlot.getImprovementType() == NO_IMPROVEMENT) || (kPlot.getOwner() != getOwner())) // BtS
			// K-Mod, 16/dec/10: enabled the pillaging of own roads
			if (kPlot.getOwner() != getOwner() || (!kPlot.isImproved() && !kPlot.isRoute()))
				return false;
		}
	}
	if (kPlot.isWater())
	{
		CvUnit* pInterceptor = bestSeaPillageInterceptor(this, GC.getCOMBAT_DIE_SIDES() / 2);
		if (pInterceptor != NULL)
		{
			setMadeAttack(false);
			int iWithdrawal = withdrawalProbability();
			changeExtraWithdrawal(-iWithdrawal); // no withdrawal since we are really the defender
			attack(pInterceptor->plot(), false, /* advc: */ NULL, true);
			changeExtraWithdrawal(iWithdrawal);
			return false;
		}
	}
	ImprovementTypes const eOldImprovement = kPlot.getImprovementType();
	RouteTypes const eOldRoute = kPlot.getRouteType();
	// <advc.111>
	bool bPillaged = false;
    // TODO: apply Norse UP: *= 5 if middle ages or earlier
	if (getDestructibleStructureAt(kPlot, false, bForceImprovement) == STRUCTURE_ROUTE)
		bPillaged = pillageRoute();
	else bPillaged = pillageImprovement(); // </advc.111>
	changeMoves(GC.getMOVE_DENOMINATOR());
	if (kPlot.isActiveVisible(false))
	{
		// Pillage entity mission
		CvMissionDefinition kDefiniton;
		kDefiniton.setMissionTime(GC.getInfo(MISSION_PILLAGE).getTime() * gDLL->getSecsPerTurn());
		kDefiniton.setMissionType(MISSION_PILLAGE);
		kDefiniton.setPlot(&kPlot);
		kDefiniton.setUnit(BATTLE_UNIT_ATTACKER, this);
		kDefiniton.setUnit(BATTLE_UNIT_DEFENDER, NULL);
		gDLL->getEntityIFace()->AddMission(&kDefiniton);
	}
	/*	advc.111: (Could just compare old with current, but that wouldn't catch
		improvements that replace themselves upon being pillaged.) */
    // TODO: add pillage gold
	if (bPillaged)
		CvEventReporter::getInstance().unitPillage(this, eOldImprovement, eOldRoute, getOwner(), 0);
	return true;
}

// adv.111: Cut from pillage()
bool CvUnit::pillageImprovement()
{
	CvPlot& kPlot = getPlot();
	if (!kPlot.isImproved())
		return false;
	if (kPlot.getTeam() != getTeam())
	{
		int iPillageGold = 0;
		if (!GC.getPythonCaller()->doPillageGold(*this, kPlot, iPillageGold))
		{	// K-Mod. C version of the original python code (CvGameUtils.doPillageGold)
			int const iPillageBase = GC.getInfo(kPlot.getImprovementType()).
					getPillageGold();
			if (iPillageBase > 0) // advc
			{
				iPillageGold += SyncRandNum(iPillageBase);
				/*	<advc.004> Add 1, and subtract 1 from the upper bound of the 2nd roll.
					To guarantee that at least 1 gold is pillaged -
					so that a message gets shown. */
				iPillageGold++;
				iPillageGold += SyncRandNum(iPillageBase - 1); // </advc.004>
				iPillageGold += (getPillageChange() * iPillageGold) / 100;
				// K-Mod end
			}
		}
		if (iPillageGold > 0)
		{
			GET_PLAYER(getOwner()).changeGold(iPillageGold);
			CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_PLUNDERED_GOLD_FROM_IMP",
					iPillageGold, GC.getInfo(kPlot.getImprovementType()).getTextKeyWide());
			gDLL->UI().addMessage(getOwner(), true, -1, szBuffer,
					"AS2D_PILLAGE", MESSAGE_TYPE_INFO, getButton(),
					GC.getColorType("GREEN"), kPlot.getX(), kPlot.getY());
			if (kPlot.isOwned())
			{
				szBuffer = gDLL->getText("TXT_KEY_MISC_IMP_DESTROYED",
						GC.getInfo(kPlot.getImprovementType()).getTextKeyWide(),
						getNameKey(), getVisualCivAdjective(kPlot.getTeam()));
				gDLL->UI().addMessage(kPlot.getOwner(), /* advc.106j: */ true,
						-1, szBuffer, kPlot, "AS2D_PILLAGED",
						MESSAGE_TYPE_INFO, getButton(), GC.getColorType("RED"));
			}
		}
	}
	kPlot.setImprovementType(GC.getInfo(kPlot.getImprovementType()).
			getImprovementPillage());
	return true;
}

// adv.111: Cut from pillage()
bool CvUnit::pillageRoute()
{
	if (!getPlot().isRoute())
		return false;
	getPlot().setRouteType(//NO_ROUTE // XXX downgrade rail???
			// advc.255: Indeed, we shall.
			GC.getInfo(getPlot().getRouteType()).getRoutePillage());
	return true;
}


bool CvUnit::canPlunder(CvPlot const& kPlot, bool bTestVisible) const
{
	if (getDomainType() != DOMAIN_SEA)
		return false;
	if (!m_pUnitInfo->isPillage())
		return false;
	if (!kPlot.isWater())
		return false;
	if (kPlot.isFreshWater())
		return false;
	if (!isValidDomain(kPlot.isWater()))
		return false;
	// <advc.033>
	if(!kPlot.isRevealed(getTeam()) ||
		(!at(kPlot) && !canMoveInto(kPlot) && !canMoveInto(kPlot, true)))
	{
		return false;
	} // </advc.033>
	// advc:
	bool bPirate = (isAlwaysHostile(kPlot) || m_pUnitInfo->isHiddenNationality());
	if (!bTestVisible)
	{
		if (kPlot.getTeam() == getTeam())
			return false;
		// <advc.033>
		if(kPlot.isOwned() && (GET_TEAM(kPlot.getTeam()).isVassal(getTeam()) ||
			GET_TEAM(getTeam()).isVassal(kPlot.getTeam()) ||
			(GET_TEAM(kPlot.getTeam()).isOpenBorders(getTeam()) && !bPirate)))
		{
			return false;
		} // </advc.033>
	}
	// <advc.033>
	if(!bPirate && GET_TEAM(getTeam()).getNumWars(false, true) <= 0)
		return false; // </advc.033>

	return true;
}


bool CvUnit::plunder()
{
	if (!canPlunder(getPlot()))
		return false;
	setBlockading(true);
	finishMoves();
	return true;
}

/*  advc.033: For code shared by updatePlunder, collectBlockadeGold and
	CvGame::updateColoredPlots.
	See BBAI notes below about the iExtra param; disused for now. */
void CvUnit::blockadeRange(std::vector<CvPlot*>& r, int iExtra, /* advc.033: */ bool bCheckCanPlunder) const
{
	if(bCheckCanPlunder && !canPlunder(getPlot()))
		return;
	// advc: From an old BBAI bugfix; apparently obsolete.
	//gDLL->getFAStarIFace()->ForceReset(&GC.getStepFinder());
	// See comment in UWAICache::updateTrainCargo
	bool bImpassables = (getDomainType() == DOMAIN_SEA && GET_PLAYER(getOwner()).
			AI_isAnyImpassable(getUnitType()));
	int const iRange = GC.getDefineINT(CvGlobals::SHIP_BLOCKADE_RANGE);
	// advc.033:
	TeamWaterPathFinder pathFinder(GET_TEAM(BARBARIAN_TEAM), NULL, iRange/* + iExtra*/);
	for (SquareIter it(*this, iRange); it.hasNext(); ++it)
	{
		CvPlot& kLoopPlot = *it;
		if (!kLoopPlot.isArea(getArea()) ||
			(bCheckCanPlunder && !canPlunder(kLoopPlot))) // advc.033
		{
			continue;
		}
		// BBAI (jdog5000, 12/11/08): No blockading on other side of an isthmus
		int iPathDist = -1;
				//= GC.getMap().calculatePathDistance(plot(), &kLoopPlot);
		// <advc.033> (Slightly ugly)
		if (bImpassables)
		{
			if (pathFinder.shallowWaterFinder().generatePath(getPlot(), kLoopPlot))
				iPathDist = pathFinder.shallowWaterFinder().getPathLength();
		}
		else
		{
			if (pathFinder.anyWaterFinder().generatePath(getPlot(), kLoopPlot))
				iPathDist = pathFinder.anyWaterFinder().getPathLength();
		} // </advc.033>
		/*	BBAI NOTES (jdog5000, 06/01/09):
			There are rare issues where the pathfinder will return incorrect results.
			for unknown reasons.  Seems to find a suboptimal path sometimes
			in partially repeatable circumstances.  The fix below is a hack
			to address the permanent one or two tile blockades which would
			appear randomly, it should cause extra blockade clearing only very rarely. */
		/*	advc.033: Workaround disabled. Let's see if KmodPathFinder has the same
			defect as FAStar in the EXE. Could well be; perhaps it can be fixed then. */
		if(iPathDist >= 0 && iPathDist <= iRange/* + iExtra*/)
			r.push_back(&kLoopPlot);
	}
}


void CvUnit::updatePlunder(int iChange, bool bUpdatePlotGroups)
{
	// <advc.033> Code moved into new function blockadeRange
	std::vector<CvPlot*> apRange;
	blockadeRange(apRange, iChange == -1 ? 2 : 0, iChange >= 0);
	// To avoid updating plot groups unnecessarily
	EagerEnumMap<TeamTypes,bool> abChanged;
	for(size_t i = 0; i < apRange.size(); i++)
	{
		CvPlot* pLoopPlot = apRange[i];
		// Not our vassals, master
		for (TeamIter<ALIVE,KNOWN_POTENTIAL_ENEMY_OF> it(getTeam());
			it.hasNext(); ++it) // </advc.033>
		{
			CvTeam const& t = *it;
			if (!isEnemy(t.getID()))
				continue;
			if(iChange == -1 && pLoopPlot->getBlockadedCount(t.getID()) <= 0)
				continue;
			bool bOldTradeNet = false;
			if(!abChanged.get(t.getID()))
				bOldTradeNet = pLoopPlot->isTradeNetwork(t.getID());
			pLoopPlot->changeBlockadedCount(t.getID(), iChange);
			if(!abChanged.get(t.getID()))
			{
				abChanged.set(t.getID(),
						bOldTradeNet != pLoopPlot->isTradeNetwork(t.getID()));
			}
		}
	}
	/*if (bChanged) {
		gDLL->UI().setDirty(BlockadedPlots_DIRTY_BIT, true);
		if (bUpdatePlotGroups)
			GC.getGame().updatePlotGroups();
	}*/
	// <advc.033>
	// Update colors -- unless we're about to unit-cycle
	if (isHuman() && ((iChange == -1 && gDLL->UI().getHeadSelectedUnit() == this) ||
		GC.suppressCycling()))
	{
		GC.getGame().updateColoredPlots();
	}
	gDLL->UI().setDirty(BlockadedPlots_DIRTY_BIT, true);
	if(bUpdatePlotGroups)
	{
		FOR_EACH_ENUM(Team)
		{
			if (abChanged.get(eLoopTeam))
			{
				for (MemberIter itMember(eLoopTeam); itMember.hasNext(); ++itMember)
					itMember->updatePlotGroups();
			}
		}
	} // </advc.033>
}


int CvUnit::sabotageCost(const CvPlot* pPlot) const
{
	static int const iBASE_SPY_SABOTAGE_COST = GC.getDefineINT("BASE_SPY_SABOTAGE_COST"); // advc.opt
	return iBASE_SPY_SABOTAGE_COST;
}

// XXX compare with destroy prob...
int CvUnit::sabotageProb(const CvPlot* pPlot, ProbabilityTypes eProbStyle) const
{
	int iDefenseCount = 0;
	int iCounterSpyCount = 0;
	if (pPlot->isOwned())
	{
		iDefenseCount = pPlot->plotCount(
				PUF_canDefend, -1, -1, NO_PLAYER, pPlot->getTeam());
		iCounterSpyCount = pPlot->plotCount(
				PUF_isCounterSpy, -1, -1, NO_PLAYER, pPlot->getTeam());
		FOR_EACH_ADJ_PLOT(*pPlot)
		{
			iCounterSpyCount += pAdj->plotCount(
					PUF_isCounterSpy, -1, -1, NO_PLAYER, pPlot->getTeam());
		}
	}
	if (eProbStyle == PROBABILITY_HIGH)
		iCounterSpyCount = 0;
	int iProb = (40 / (iDefenseCount + 1)); // XXX
	if (eProbStyle != PROBABILITY_LOW)
		iProb += (50 / (iCounterSpyCount + 1)); // XXX
	return iProb;
}

/*	advc (note): This function cheats with visibility, but I won't fix that
	b/c it's disused since the BtS expansion. */
bool CvUnit::canSabotage(const CvPlot* pPlot, bool bTestVisible) const
{
	if (!m_pUnitInfo->isSabotage())
		return false;

	if (!pPlot->isImproved()) // advc.opt: Moved up
		return false;

	if (pPlot->getTeam() == getTeam())
		return false;

	if (pPlot->isCity())
		return false;
	// <advc.001>
	if (GC.getInfo(pPlot->getImprovementType()).isPermanent())
		return false; // </advc.001>
	if (!bTestVisible)
	{
		if (GET_PLAYER(getOwner()).getGold() < sabotageCost(pPlot))
			return false;
	}

	return true;
}


bool CvUnit::sabotage()
{
	if (!canSabotage(plot()))
		return false;

	CvPlot& kPlot = getPlot();
	bool const bCaught = !SyncRandSuccess100(sabotageProb(&kPlot));
	GET_PLAYER(getOwner()).changeGold(-sabotageCost(&kPlot));
	CvWString szBuffer;
	if (!bCaught)
	{
		kPlot.setImprovementType(GC.getInfo(kPlot.getImprovementType()).
				getImprovementPillage());
		finishMoves();
		CvCity* pNearestCity = GC.getMap().findCity(kPlot.getX(), kPlot.getY(),
				kPlot.getOwner(), NO_TEAM, false);
		if (pNearestCity != NULL)
		{
			szBuffer = gDLL->getText("TXT_KEY_MISC_SPY_SABOTAGED",
					getNameKey(), pNearestCity->getNameKey());
			gDLL->UI().addMessage(getOwner(), true, -1, szBuffer, "AS2D_SABOTAGE",
					MESSAGE_TYPE_INFO, getButton(), GC.getColorType("GREEN"),
					kPlot.getX(), kPlot.getY());

			if (kPlot.isOwned())
			{
				szBuffer = gDLL->getText("TXT_KEY_MISC_SABOTAGE_NEAR", pNearestCity->getNameKey());
				gDLL->UI().addMessage(kPlot.getOwner(), false, -1, szBuffer, kPlot,
						"AS2D_SABOTAGE", MESSAGE_TYPE_INFO, getButton(), GC.getColorType("RED"));
			}
		}
		if (kPlot.isActiveVisible(false))
			NotifyEntity(MISSION_SABOTAGE);
	}
	else
	{
		if (kPlot.isOwned())
		{
			szBuffer = gDLL->getText("TXT_KEY_MISC_SPY_CAUGHT_AND_KILLED",
					GET_PLAYER(getOwner()).getCivilizationAdjective(), getNameKey());
			gDLL->UI().addMessage(kPlot.getOwner(), false, -1, szBuffer, "AS2D_EXPOSE", MESSAGE_TYPE_INFO);
		}
		szBuffer = gDLL->getText("TXT_KEY_MISC_YOUR_SPY_CAUGHT", getNameKey());
		gDLL->UI().addMessage(getOwner(), true, -1, szBuffer, "AS2D_EXPOSED", MESSAGE_TYPE_INFO);
		if (kPlot.isActiveVisible(false))
			NotifyEntity(MISSION_SURRENDER);

		if (kPlot.isOwned())
		{
			if (!isEnemy(kPlot))
			{   // advc.130j:
				GET_PLAYER(kPlot.getOwner()).AI_rememberEvent(getOwner(), MEMORY_SPY_CAUGHT);
			}
		}

		kill(true, kPlot.getOwner());
	}

	return true;
}


int CvUnit::destroyCost(const CvPlot* pPlot) const
{
	CvCity const* pCity = pPlot->getPlotCity();
	if (pCity == NULL)
		return 0;
	// <advc.opt>
	static int const iBASE_SPY_DESTROY_COST = GC.getDefineINT("BASE_SPY_DESTROY_COST");
	static int const iSPY_DESTROY_COST_MULTIPLIER_LIMITED = GC.getDefineINT("SPY_DESTROY_COST_MULTIPLIER_LIMITED");
	static int const iSPY_DESTROY_COST_MULTIPLIER = GC.getDefineINT("SPY_DESTROY_COST_MULTIPLIER"); // </advc.opt>
	// advc: bLimited... code deleted - CvCity::isProductionLimited does exactly what we need.
	return iBASE_SPY_DESTROY_COST + (pCity->getProduction() * (pCity->isProductionLimited() ?
			iSPY_DESTROY_COST_MULTIPLIER_LIMITED : iSPY_DESTROY_COST_MULTIPLIER));
}


int CvUnit::destroyProb(const CvPlot* pPlot, ProbabilityTypes eProbStyle) const
{
	CvCity const* pCity = pPlot->getPlotCity();
	if (pCity == NULL)
		return 0;

	int iDefenseCount = pPlot->plotCount(
			PUF_canDefend, -1, -1, NO_PLAYER, pPlot->getTeam());
	int iCounterSpyCount = pPlot->plotCount(
			PUF_isCounterSpy, -1, -1, NO_PLAYER, pPlot->getTeam());
	FOR_EACH_ADJ_PLOT(*pPlot)
	{
		iCounterSpyCount += pAdj->plotCount(
				PUF_isCounterSpy, -1, -1, NO_PLAYER, pPlot->getTeam());
	}
	if (eProbStyle == PROBABILITY_HIGH)
		iCounterSpyCount = 0;
	int iProb = (25 / (iDefenseCount + 1)); // XXX
	if (eProbStyle != PROBABILITY_LOW)
		iProb += (50 / (iCounterSpyCount + 1)); // XXX
	iProb += std::min(25, pCity->getProductionTurnsLeft()); // XXX
	return iProb;
}


bool CvUnit::canDestroy(const CvPlot* pPlot, bool bTestVisible) const
{
	if (!m_pUnitInfo->isDestroy())
		return false;
	if (pPlot->getTeam() == getTeam())
		return false;

	CvCity const* pCity = pPlot->getPlotCity();

	if (pCity == NULL)
		return false;
	if (pCity->getProduction() == 0)
		return false;

	if (!bTestVisible)
	{
		if (GET_PLAYER(getOwner()).getGold() < destroyCost(pPlot))
			return false;
	}

	return true;
}


bool CvUnit::destroy()
{
	if (!canDestroy(plot()))
		return false;

	bool const bCaught = !SyncRandSuccess100(destroyProb(plot()));

	CvCity* pCity = getPlot().getPlotCity();
	FAssert(pCity != NULL);

	GET_PLAYER(getOwner()).changeGold(-destroyCost(plot()));

	if (!bCaught)
	{
		pCity->setProduction(pCity->getProduction() / 2);

		finishMoves();

		CvWString szBuffer(gDLL->getText("TXT_KEY_MISC_SPY_DESTROYED_PRODUCTION",
				getNameKey(), pCity->getProductionNameKey(), pCity->getNameKey()));
		gDLL->UI().addMessage(getOwner(), true, -1, szBuffer, "AS2D_DESTROY",
				MESSAGE_TYPE_INFO, getButton(), GC.getColorType("GREEN"),
				pCity->getX(), pCity->getY());

		szBuffer = gDLL->getText("TXT_KEY_MISC_CITY_PRODUCTION_DESTROYED",
				pCity->getProductionNameKey(), pCity->getNameKey());
		gDLL->UI().addMessage(pCity->getOwner(), false, -1, szBuffer, pCity->getPlot(),
				"AS2D_DESTROY", MESSAGE_TYPE_INFO, getButton(), GC.getColorType("RED"));

		if (getPlot().isActiveVisible(false))
			NotifyEntity(MISSION_DESTROY);
	}
	else
	{
		CvWString szBuffer(gDLL->getText("TXT_KEY_MISC_SPY_CAUGHT_AND_KILLED",
				GET_PLAYER(getOwner()).getCivilizationAdjective(), getNameKey()));
		gDLL->UI().addMessage(pCity->getOwner(), false, -1, szBuffer,
				"AS2D_EXPOSE", MESSAGE_TYPE_INFO,
				NULL, NO_COLOR, getX(), getY()); // advc.127b

		szBuffer = gDLL->getText("TXT_KEY_MISC_YOUR_SPY_CAUGHT", getNameKey());
		gDLL->UI().addMessage(getOwner(), true, -1, szBuffer,
				"AS2D_EXPOSED", MESSAGE_TYPE_INFO,
				NULL, NO_COLOR, getX(), getY()); // advc.127b

		if (getPlot().isActiveVisible(false))
			NotifyEntity(MISSION_SURRENDER);

		if (!isEnemy(pCity->getTeam()))
		{   // advc.130j:
			GET_PLAYER(pCity->getOwner()).AI_rememberEvent(getOwner(), MEMORY_SPY_CAUGHT);
		}

		kill(true, pCity->getOwner());
	}

	return true;
}


int CvUnit::stealPlansCost(const CvPlot* pPlot) const
{
	CvCity const* pCity = pPlot->getPlotCity();
	if (pCity == NULL)
		return 0;

	static int const iBASE_SPY_STEAL_PLANS_COST = GC.getDefineINT("BASE_SPY_STEAL_PLANS_COST"); // advc.opt
	static int const iSPY_STEAL_PLANS_COST_MULTIPLIER = GC.getDefineINT("SPY_STEAL_PLANS_COST_MULTIPLIER"); // advc.opt
	return iBASE_SPY_STEAL_PLANS_COST + (GET_TEAM(pCity->getTeam()).getTotalLand() +
			GET_TEAM(pCity->getTeam()).getTotalPopulation()) * iSPY_STEAL_PLANS_COST_MULTIPLIER;
}


// XXX compare with destroy prob...
int CvUnit::stealPlansProb(const CvPlot* pPlot, ProbabilityTypes eProbStyle) const
{
	CvCity const* pCity = pPlot->getPlotCity();
	if (pCity == NULL)
		return 0;

	int iDefenseCount = pPlot->plotCount(
			PUF_canDefend, -1, -1, NO_PLAYER, pPlot->getTeam());
	int iCounterSpyCount = pPlot->plotCount(
			PUF_isCounterSpy, -1, -1, NO_PLAYER, pPlot->getTeam());
	FOR_EACH_ADJ_PLOT(*pPlot)
	{
		iCounterSpyCount += pAdj->plotCount(
				PUF_isCounterSpy, -1, -1, NO_PLAYER, pPlot->getTeam());
	}
	if (eProbStyle == PROBABILITY_HIGH)
		iCounterSpyCount = 0;
	int iProb = (pCity->isGovernmentCenter() ? 20 : 0); // XXX
	iProb += (20 / (iDefenseCount + 1)); // XXX
	if (eProbStyle != PROBABILITY_LOW)
		iProb += (50 / (iCounterSpyCount + 1)); // XXX
	return iProb;
}


bool CvUnit::canStealPlans(const CvPlot* pPlot, bool bTestVisible) const
{
	if (!m_pUnitInfo->isStealPlans())
		return false;
	if (pPlot->getTeam() == getTeam())
		return false;
	{
		CvCity* pCity = pPlot->getPlotCity();
		if (pCity == NULL)
			return false;
	}
	if (!bTestVisible)
	{
		if (GET_PLAYER(getOwner()).getGold() < stealPlansCost(pPlot))
			return false;
	}

	return true;
}


bool CvUnit::stealPlans()
{
	if (!canStealPlans(plot()))
		return false;

	bool const bCaught = !SyncRandSuccess100(stealPlansProb(plot()));

	CvCity* pCity = getPlot().getPlotCity();
	FAssertMsg(pCity != NULL, "City is not assigned a valid value");

	GET_PLAYER(getOwner()).changeGold(-(stealPlansCost(plot())));

	CvWString szBuffer;
	if (!bCaught)
	{
		GET_TEAM(getTeam()).changeStolenVisibilityTimer(pCity->getTeam(), 2);

		finishMoves();

		szBuffer = gDLL->getText("TXT_KEY_MISC_SPY_STOLE_PLANS", getNameKey(), pCity->getNameKey());
		gDLL->UI().addMessage(getOwner(), true, -1, szBuffer, "AS2D_STEALPLANS",
				MESSAGE_TYPE_INFO, getButton(), GC.getColorType("GREEN"),
				pCity->getX(), pCity->getY());

		szBuffer = gDLL->getText("TXT_KEY_MISC_PLANS_STOLEN", pCity->getNameKey());
		gDLL->UI().addMessage(pCity->getOwner(), false, -1, szBuffer, getPlot(),
				"AS2D_STEALPLANS", MESSAGE_TYPE_INFO, getButton(), GC.getColorType("RED"));

		if (getPlot().isActiveVisible(false))
			NotifyEntity(MISSION_STEAL_PLANS);
	}
	else
	{
		szBuffer = gDLL->getText("TXT_KEY_MISC_SPY_CAUGHT_AND_KILLED",
				GET_PLAYER(getOwner()).getCivilizationAdjective(), getNameKey());
		gDLL->UI().addMessage(pCity->getOwner(), false, -1, szBuffer, "AS2D_EXPOSE", MESSAGE_TYPE_INFO);

		szBuffer = gDLL->getText("TXT_KEY_MISC_YOUR_SPY_CAUGHT", getNameKey());
		gDLL->UI().addMessage(getOwner(), true, -1, szBuffer, "AS2D_EXPOSED", MESSAGE_TYPE_INFO);

		if (getPlot().isActiveVisible(false))
			NotifyEntity(MISSION_SURRENDER);

		if (!isEnemy(pCity->getTeam()))
		{   // advc.130j:
			GET_PLAYER(pCity->getOwner()).AI_rememberEvent(getOwner(), MEMORY_SPY_CAUGHT);
		}

		kill(true, pCity->getOwner());
	}

	return true;
}


bool CvUnit::canFound(const CvPlot* pPlot, bool bTestVisible) const
{
	if (!isFound())
		return false;
	if (!GET_PLAYER(getOwner()).canFound(*pPlot, bTestVisible,
		// advc.181: Don't give away fogged cities when inspecting go-to plot
		(at(*pPlot) || !isHuman())))
	{
		return false;
	}
	return true;
}


bool CvUnit::found()
{
	if (!canFound(plot()))
		return false;
	if (isActiveOwned() &&
		isHuman()) // advc.127, advc.706
	{
		gDLL->UI().lookAt(getPlot().getPoint(), CAMERALOOKAT_NORMAL);
	}
	GET_PLAYER(getOwner()).found(getX(), getY());
	if (getPlot().isActiveVisible(false))
		NotifyEntity(MISSION_FOUND);
	kill(true);
	return true;
}


bool CvUnit::canSpread(const CvPlot* pPlot, ReligionTypes eReligion, bool bTestVisible, bool bAI) const
{
	// UNOFFICIAL_PATCH, Efficiency, 08/19/09, jdog5000: Moved below faster calls
	//if (GC.getUSE_USE_CANNOT_SPREAD_RELIGION_CALLBACK()) { ... }
	if (eReligion == NO_RELIGION)
		return false;
	if (m_pUnitInfo->getReligionSpreads(eReligion) <= 0 && (!bAI || !m_pUnitInfo->isGreatMission())) // doc
		return false;

	CvCity const* pCity = pPlot->getPlotCity();

	if (pCity == NULL)
		return false;
    if (!pCity->canSpread(eReligion, true)) // doc: use canSpread
		return false;
	// <advc.099d>
	if(pCity->isOccupation())
	    return false; // </advc.099d>
    // doc: if not proselytizing religion, only if own city or owner shares state religion
	if (!GC.getInfo(eReligion).isProselytizing())
	{
	    if (getOwner() != pCity->getOwner() && GET_PLAYER(pCity->getOwner()).getStateReligion() != eReligion)
	        return false;
	}
	if (!canEnterTerritory(pPlot->getTeam(), false, pPlot->area()))
		return false;

	if (!bTestVisible)
	{
		/* advc.123a (no change made): Could remove this line to disallow
		   spreading non-state religion while in Theocracy. I've disallowed
		   gifting of Missionaries (of a non-state religion) instead.
		   Both are ways to stop players from bypassing the Theocracy restriction
		   through gifting. */
		if (pCity->getTeam() != getTeam())
		{
			if (GET_PLAYER(pCity->getOwner()).isNoNonStateReligionSpread())
			{
				if (eReligion != GET_PLAYER(pCity->getOwner()).getStateReligion())
					return false;
			}
		}
	}
	// UNOFFICIAL_PATCH, Efficiency, 08/19/09, jdog5000: Moved from above (advc: only matters if the callback is re-enabled)
	if (GC.getPythonCaller()->cannotSpreadOverride(*this, *pPlot, eReligion))
		return false;

	return true;
}


bool CvUnit::spread(ReligionTypes eReligion)
{
	if (!canSpread(plot(), eReligion))
		return false;

	CvCity* pCity = getPlot().getPlotCity();
	if (pCity != NULL)
	{	/*int iSpreadProb = m_pUnitInfo->getReligionSpreads(eReligion);
		if (pCity->getTeam() != getTeam())
			iSpreadProb /= 2;
		bool bSuccess;
		iSpreadProb += ((100 - iSpreadProb)*(GC.getNumReligionInfos() - pCity->getReligionCount())) /
				GC.getNumReligionInfos();*/ // BtS
		// K-Mod. A more dynamic formula
		// TODO: not used by doc implementation, but check if reusable
		//int const iPresentReligions = pCity->getReligionCount();
		//int const iMissingReligions = GC.getNumReligionInfos() - iPresentReligions;
		/*	advc.173: Don't take into account population. Meaning, along with the
			unfixed bug below, that the formula really works like in BtS again. */
		//int const iPopulation = 10;//pCity->getPopulation();
		int iSpreadProb = getSpreadChance(eReligion); // doc

		bool bSuccess;
		// K-Mod end

		if (SyncRandSuccess100(iSpreadProb))
		{
		    pCity->spreadReligion(eReligion, true); // doc
			bSuccess = true;
		}
		else
		{	/*szBuffer = gDLL->getText("TXT_KEY_MISC_RELIGION_FAILED_TO_SPREAD", getNameKey(), GC.getInfo(eReligion).getChar(), pCity->getNameKey());
			gDLL->UI().addMessage(getOwner(), true, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_NOSPREAD", MESSAGE_TYPE_INFO, getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_RED"), pCity->getX(), pCity->getY());
			bSuccess = false;*/ // BtS
			/*	K-Mod. Instead of simply failing, give some chance of
				removing one of the existing religions. */
			std::vector<std::pair<int,ReligionTypes> > aieRankedReligions;
			int iRandomWeight = GC.getDefineINT("RELIGION_INFLUENCE_RANDOM_WEIGHT");
			FOR_EACH_ENUM(Religion)
			{
				if (pCity->isHasReligion(eLoopReligion) || eLoopReligion == eReligion)
				{
					// holy city can't lose its religion!
					if (pCity != GC.getGame().getHolyCity(eLoopReligion))
					{
						int iInfluence = pCity->getReligionGrip(eLoopReligion);
						iInfluence += SyncRandNum(iRandomWeight);
						if (eLoopReligion == eReligion)
							iInfluence += m_pUnitInfo->getReligionSpreads(eReligion) / 2;
						aieRankedReligions.push_back(std::make_pair(
								iInfluence, eLoopReligion));
					}
				}
			}
			std::partial_sort(aieRankedReligions.begin(), aieRankedReligions.begin() + 1,
					aieRankedReligions.end());
			ReligionTypes eFailedReligion = aieRankedReligions[0].second;
			if (eFailedReligion == eReligion)
			{
				CvWString szBuffer(gDLL->getText("TXT_KEY_MISC_RELIGION_FAILED_TO_SPREAD",
						getNameKey(), GC.getInfo(eReligion).getChar(), pCity->getNameKey()));
				gDLL->UI().addMessage(getOwner(), true, -1, szBuffer, "AS2D_NOSPREAD",
						MESSAGE_TYPE_INFO, getButton(), GC.getColorType("RED"),
						pCity->getX(), pCity->getY());
				bSuccess = false;
			}
			else
			{
				pCity->setHasReligion(eReligion, true, true, false,
						getOwner()); // advc.106e
				pCity->setHasReligion(eFailedReligion, false, true, false,
						getOwner()); // advc.106e
				bSuccess = true;
			}
			// K-Mod
		}

		// Python Event
		CvEventReporter::getInstance().unitSpreadReligionAttempt(this, eReligion, bSuccess);
	}
	if (getPlot().isActiveVisible(false))
		NotifyEntity(MISSION_SPREAD);
	kill(true);
	return true;
}


// doc
int CvUnit::getSpreadChance(ReligionTypes eReligion) const
{
	if (!plot()->isCity())
        return 0;

	CvCity const& kCity = *(getPlot().getPlotCity());
    CvPlayer const& kOwner = GET_PLAYER(kCity.getOwner());
	bool bDistant = kOwner.isDistantSpread(kCity, eReligion);
	ReligionSpreadTypes eSpreadFactor = kOwner.getSpreadType(getPlot(), eReligion, bDistant);

	if (eSpreadFactor == RELIGION_SPREAD_FAST)
        return 100;

	int iSpreadChance = m_pUnitInfo->getReligionSpreads(eReligion);

	int iOtherReligions = 0;
    FOR_EACH_ENUM(Religion)
	{
		if (kCity.isHasReligion(eLoopReligion) && !kOwner.isTolerating(eLoopReligion))
			iOtherReligions++;
	}

	iSpreadChance += (NUM_RELIGION_TYPES - iOtherReligions) * (100 - iSpreadChance) / NUM_RELIGION_TYPES;

	if (eSpreadFactor == RELIGION_SPREAD_NONE)
        iSpreadChance /= 2;

	return iSpreadChance;
}


bool CvUnit::canSpreadCorporation(const CvPlot* pPlot, CorporationTypes eCorporation, bool bTestVisible) const
{
	if (eCorporation == NO_CORPORATION)
		return false;
	if (!GET_PLAYER(getOwner()).isActiveCorporation(eCorporation))
		return false;
	if (m_pUnitInfo->getCorporationSpreads(eCorporation) <= 0)
		return false;

	CvCity const* pCity = pPlot->getPlotCity();
	if (pCity == NULL)
		return false;
	if (pCity->isHasCorporation(eCorporation))
		return false;
	 // <advc.099d>
	if(pCity->isDisorder())
		return false; // </advc.099d>
	if (!canEnterTerritory(pPlot->getTeam(), false, pPlot->area()))
		return false;

	if (!bTestVisible)
	{
		if (!GET_PLAYER(pCity->getOwner()).isActiveCorporation(eCorporation))
			return false;

		FOR_EACH_ENUM(Corporation)
		{
			if (pCity->isHeadquarters(eLoopCorporation))
			{
				if (GC.getGame().isCompetingCorporation(eLoopCorporation, eCorporation))
					return false;
			}
		}
		bool bValid = false;
		for (int i = 0; i < GC.getInfo(eCorporation).getNumPrereqBonuses(); ++i)
		{
			if (pCity->hasBonus(GC.getInfo(eCorporation).getPrereqBonus(i)))
			{
				bValid = true;
				break;
			}
		}
		if (!bValid)
			return false;
		if (GET_PLAYER(getOwner()).getGold() < spreadCorporationCost(eCorporation, pCity))
			return false;
	}
	return true;
}

int CvUnit::spreadCorporationCost(CorporationTypes eCorporation, CvCity const* pCity) const
{
	int iCost = std::max(0, GC.getInfo(eCorporation).getSpreadCost() *
			(100 + GET_PLAYER(getOwner()).calculateInflationRate()));
	iCost /= 100;
	if (pCity == NULL)
		return iCost; // advc

	if (getTeam() != pCity->getTeam() &&
		!GET_TEAM(pCity->getTeam()).isVassal(getTeam()))
	{
		static int const iCORPORATION_FOREIGN_SPREAD_COST_PERCENT = GC.getDefineINT("CORPORATION_FOREIGN_SPREAD_COST_PERCENT"); // advc.opt
		iCost *= iCORPORATION_FOREIGN_SPREAD_COST_PERCENT;
		iCost /= 100;
	}
	FOR_EACH_ENUM2(Corporation, eLoopCorp)
	{
		if (eLoopCorp != eCorporation && pCity->isActiveCorporation(eLoopCorp) &&
			GC.getGame().isCompetingCorporation(eCorporation, eLoopCorp))
		{
			iCost *= 100 + GC.getInfo(eLoopCorp).getSpreadFactor();
			iCost /= 100;
		}
	}
	return iCost;
}

bool CvUnit::spreadCorporation(CorporationTypes eCorporation)
{
	if (!canSpreadCorporation(plot(), eCorporation))
		return false;

	CvCity* pCity = getPlot().getPlotCity();
	if (pCity != NULL)
	{
		GET_PLAYER(getOwner()).changeGold(-spreadCorporationCost(eCorporation, pCity));
		int iSpreadProb = m_pUnitInfo->getCorporationSpreads(eCorporation);
		if (pCity->getTeam() != getTeam())
			iSpreadProb /= 2;

		iSpreadProb += (((GC.getNumCorporationInfos() - pCity->getCorporationCount()) *
				(100 - iSpreadProb)) / GC.getNumCorporationInfos());
		if (SyncRandSuccess100(iSpreadProb))
			pCity->setHasCorporation(eCorporation, true, true, false);
		else
		{
			CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_CORPORATION_FAILED_TO_SPREAD",
					getNameKey(), GC.getInfo(eCorporation).getChar(), pCity->getNameKey());
			gDLL->UI().addMessage(getOwner(), true, -1, szBuffer, "AS2D_NOSPREAD",
					MESSAGE_TYPE_INFO, getButton(), GC.getColorType("RED"),
					pCity->getX(), pCity->getY());
		}
	}
	if (getPlot().isActiveVisible(false))
		NotifyEntity(MISSION_SPREAD_CORPORATION);
	kill(true);
	return true;
}


bool CvUnit::canJoin(const CvPlot* pPlot, SpecialistTypes eSpecialist) const
{
	if (eSpecialist == NO_SPECIALIST)
		return false;
	if (!m_pUnitInfo->getGreatPeoples(eSpecialist))
		return false;
	CvCity* pCity = pPlot->getPlotCity();
	if (pCity == NULL)
		return false;
	if (!pCity->canJoin())
		return false;
	if (pCity->getTeam() != getTeam())
		return false;
	if (isDelayedDeath())
		return false;

	// doc: slave join condition
	if (getUnitInfo().isSlave())
	{
		if (!pCity->canSlaveJoin())
			return false;
	}
    // doc: satellite join condition
	if (GC.getInfo(eSpecialist).isSatellite())
	{
		if (!pCity->canSatelliteJoin())
			return false;
	}

	return true;
}


bool CvUnit::join(SpecialistTypes eSpecialist)
{
	if (!canJoin(plot(), eSpecialist))
		return false;
	CvCity* pCity = getPlot().getPlotCity();
	if (pCity != NULL)
    {
	    pCity->changeFreeSpecialistCount(eSpecialist, 1);

	    // doc: House of Wisdom effect
        if (!GC.getInfo(eSpecialist).isNoGlobalEffects())
        {
	        if (GET_PLAYER(getOwner()).isHasBuildingEffect(HOUSE_OF_WISDOM))
	        {
	            discover();
	        }

	        // doc: Neuschwanstein Castle effect
	        if (GET_PLAYER(getOwner()).isHasBuildingEffect(NEUSCHWANSTEIN))
	        {
	            pCity->changeGreatPeopleProgress(GET_PLAYER(getOwner()).greatPeopleThreshold(false) / 4);
	        }
        }
    }
	if (getPlot().isActiveVisible(false))
		NotifyEntity(MISSION_JOIN);
	kill(true);
	return true;
}


bool CvUnit::canConstruct(const CvPlot* pPlot, BuildingTypes eBuilding, bool bTestVisible) const
{
	if (eBuilding == NO_BUILDING)
		return false;

	CvCity* pCity = pPlot->getPlotCity();
	if (pCity == NULL)
		return false;

	if (getTeam() != pCity->getTeam())
		return false;

	if (pCity->getNumRealBuilding(eBuilding) > 0)
		return false;

	//if (!m_pUnitInfo->getForceBuildings(eBuilding)) { // advc.003t
	if (!m_pUnitInfo->getBuildings(eBuilding))
		return false;

	if (!pCity->canConstruct(eBuilding, false, bTestVisible, true))
		return false;
	//}
	if (isDelayedDeath())
		return false;

	return true;
}


bool CvUnit::construct(BuildingTypes eBuilding)
{
	if (!canConstruct(plot(), eBuilding))
		return false;
	CvCity* pCity = getPlot().getPlotCity();
	if (pCity != NULL)
	{
		pCity->setNumRealBuilding(eBuilding, pCity->getNumRealBuilding(eBuilding) + 1);
		CvEventReporter::getInstance().buildingBuilt(pCity, eBuilding);
	}
	if (getPlot().isActiveVisible(false))
		NotifyEntity(MISSION_CONSTRUCT);
	kill(true);
	return true;
}


TechTypes CvUnit::getDiscoveryTech(TechTypes eIgnoreTech) const
{
	return GET_PLAYER(getOwner()).getDiscoveryTech(getUnitType(), eIgnoreTech); // doc: great people can discover two technologies
}


int CvUnit::getDiscoverResearch(TechTypes eTech) const
{
    // TODO: compare with ::getDiscoverResearch
	int iResearch = (m_pUnitInfo->getBaseDiscover() + (m_pUnitInfo->getDiscoverMultiplier() * GET_TEAM(getTeam()).getTotalPopulation()));
	iResearch *= GC.getInfo(GC.getGame().getGameSpeedType()).getUnitDiscoverPercent();
	iResearch /= 100;
	if (eTech != NO_TECH)
		iResearch = std::min(GET_TEAM(getTeam()).getResearchLeft(eTech), iResearch);
	return std::max(0, iResearch);
}


bool CvUnit::canDiscover(const CvPlot* pPlot) const
{
	TechTypes eTech = getDiscoveryTech();
	if (eTech == NO_TECH)
		return false;
	if (getDiscoverResearch(eTech) == 0)
		return false;
	if (isDelayedDeath())
		return false;
	return true;
}


bool CvUnit::discover()
{
	if (!canDiscover(plot()))
		return false;

	TechTypes eFirstDiscoveryTech = getDiscoveryTech();
	FAssertMsg(eDiscoveryTech != NO_TECH, "DiscoveryTech is not assigned a valid value");

    TechTypes eSecondDiscoveryTech = getDiscoveryTech(eFirstDiscoveryTech);
    FAssert(eSecondDiscoveryTech != NO_TECH);

	if (eFirstDiscoveryTech != NO_TECH)
	{
	    int iFirstResearchLeft = GET_TEAM(getTeam()).getResearchLeft(eFirstDiscoveryTech);
	    int iFirstResearch = getDiscoverResearch(eFirstDiscoveryTech);

	    GET_TEAM(getTeam()).changeResearchProgress(eFirstDiscoveryTech, std::min(iFirstResearch, iFirstResearchLeft), getOwner());

	    if (eSecondDiscoveryTech != NO_TECH)
	    {
	        int iSecondResearchLeft = GET_TEAM(getTeam()).getResearchLeft(eSecondDiscoveryTech);
	        int iSecondResearch = std::max(0, getDiscoverResearch(eSecondDiscoveryTech) - iFirstResearchLeft);

	        if (iSecondResearch > 0)
	        {
	            GET_TEAM(getTeam()).changeResearchProgress(eSecondDiscoveryTech, std::min(iSecondResearch, iSecondResearchLeft), getOwner());
	        }
	    }
	}

	// K-Mod. If the AI bulbs something, let them reconsider their current research.
	CvPlayerAI& kOwner = GET_PLAYER(getOwner());
	if (!kOwner.isHuman() && kOwner.getCurrentResearch() != eFirstDiscoveryTech && kOwner.getCurrentResearch() != eSecondDiscoveryTech)
		kOwner.clearResearchQueue();
	// K-Mod end

	if (getPlot().isActiveVisible(false))
		NotifyEntity(MISSION_DISCOVER);

	kill(true);

	return true;
}


int CvUnit::getMaxHurryProduction(CvCity const* pCity) const
{
	int iProduction = m_pUnitInfo->getBaseHurry() +
			m_pUnitInfo->getHurryMultiplier() * pCity->getPopulation();
	iProduction *= GC.getInfo(GC.getGame().getGameSpeedType()).getUnitHurryPercent();
	iProduction /= 100;
	return std::max(0, iProduction);
}


int CvUnit::getHurryProduction(const CvPlot* pPlot) const
{
	CvCity const* pCity = pPlot->getPlotCity();
	if (pCity == NULL)
		return 0;

	int iProduction = getMaxHurryProduction(pCity);
	iProduction = std::min(pCity->productionLeft(), iProduction);

	return std::max(0, iProduction);
}


bool CvUnit::canHurry(const CvPlot* pPlot, bool bTestVisible) const
{
	if (isDelayedDeath())
		return false;
	if (getHurryProduction(pPlot) == 0)
		return false;
	CvCity* pCity = pPlot->getPlotCity();
	if (pCity == NULL)
		return false;
	if (pCity->getProductionTurnsLeft() == 1)
		return false;
	if (!bTestVisible)
	{
		if (!pCity->isProductionBuilding())
			return false;
	}
	return true;
}


bool CvUnit::hurry()
{
	if (!canHurry(plot()))
		return false;
	CvCity* pCity = getPlot().getPlotCity();
	if (pCity != NULL)
		pCity->changeProduction(getHurryProduction(plot()));
	if (getPlot().isActiveVisible(false))
		NotifyEntity(MISSION_HURRY);
	kill(true);
	return true;
}


int CvUnit::getTradeGold(const CvPlot* pPlot) const
{
	CvCity const* pCity = pPlot->getPlotCity();
	if (pCity == NULL)
		return 0;
	CvCity const* pCapital = GET_PLAYER(getOwner()).getCapital();
	int iGold = (m_pUnitInfo->getBaseTrade() + (m_pUnitInfo->getTradeMultiplier() *
			(pCapital != NULL ? pCity->calculateTradeProfit(pCapital) : 0)));
	iGold *= GC.getInfo(GC.getGame().getGameSpeedType()).getUnitTradePercent();
	iGold /= 100;
	return std::max(0, iGold);
}


bool CvUnit::canTrade(const CvPlot* pPlot, bool bTestVisible) const
{
	if (isDelayedDeath())
		return false;
	CvCity const* pCity = pPlot->getPlotCity();
	if (pCity == NULL)
		return false;

	// K-Mod. if (getTradeGold(pPlot) == 0) use to be here. I've moved it to the bottom, for efficiency.

	if (!canEnterTerritory(pPlot->getTeam(), false, pPlot->area()))
		return false;
	if (!bTestVisible)
	{
		if (pCity->getTeam() == getTeam())
			return false;
	}
	if (getTradeGold(pPlot) == 0)
		return false;
	return true;
}


bool CvUnit::trade()
{
	if (!canTrade(plot()))
		return false;
	GET_PLAYER(getOwner()).changeGold(getTradeGold(plot()));

    // doc: trade mission event
    CvEventReporter::getInstance().tradeMission(getUnitType(), getOwner(), getX(), getY(), getTradeGold(plot()));

	if (getPlot().isActiveVisible(false))
		NotifyEntity(MISSION_TRADE);
	kill(true);
	return true;
}


int CvUnit::getGreatWorkCulture(const CvPlot* pPlot,
	// <advc.251> For help text
	int* piPerEra) const
{
	LOCAL_REF(int, iPerEra, piPerEra, m_pUnitInfo->getGreatWorkCulture());
	int iCulture = iPerEra; // </advc.251>
	/*  <K-Mod> (7/dec/10)
		culture from great works now scales linearly with the era of the player.
		(the base number has been reduced in the xml accordingly) */
	iCulture *= (GET_PLAYER(getOwner()).getCurrentEra() /* advc.251: */ + 1);
	iCulture *= GC.getInfo(GC.getGame().getGameSpeedType()).getUnitGreatWorkPercent();
	iCulture /= 100; // </K-Mod>

	// doc: Harbour Opera effect
	if (GET_PLAYER(getOwner()).isHasBuildingEffect(HARBOUR_OPERA))
	    iCulture *= 2;

	return std::max(0, iCulture);
}


bool CvUnit::canGreatWork(const CvPlot* pPlot) const
{
	if (isDelayedDeath())
		return false;
	CvCity* pCity = pPlot->getPlotCity();
	if (pCity == NULL)
		return false;
	if (pCity->getOwner() != getOwner())
		return false;
	if (getGreatWorkCulture(pPlot) == 0)
		return false;
	return true;
}


bool CvUnit::greatWork()
{
	if (!canGreatWork(plot()))
		return false;
	CvCity* pCity = getPlot().getPlotCity();
	if (pCity != NULL)
	{
		pCity->setCultureUpdateTimer(0);
		//pCity->setOccupationTimer(0); // doc: artists no longer resolve unrest

		int iCultureToAdd = 100 * getGreatWorkCulture(plot());
		/*int iNumTurnsApplied = (GC.getDefineINT("GREAT_WORKS_CULTURE_TURNS") * GC.getInfo(GC.getGame().getGameSpeedType()).getUnitGreatWorkPercent()) / 100;
		for (int i = 0; i < iNumTurnsApplied; ++i)
			pCity->changeCultureTimes100(getOwner(), iCultureToAdd / iNumTurnsApplied, true, true);
		if (iNumTurnsApplied > 0)
			pCity->changeCultureTimes100(getOwner(), iCultureToAdd % iNumTurnsApplied, false, true);*/ // BtS
		/*  K-Mod, 6/dec/10, Karadoc
			apply culture in one hit. We don't need fake 'free city culture' anymore. */
		pCity->changeCultureTimes100(getOwner(), iCultureToAdd, true, true);
        GET_PLAYER(getOwner()).AI_updateCommerceWeights(); // significant culture change may cause signficant weight changes.
		// K-Mod end
	}
	if (getPlot().isActiveVisible(false))
		NotifyEntity(MISSION_GREAT_WORK);
	kill(true);
	return true;
}


int CvUnit::getEspionagePoints(const CvPlot* pPlot) const
{
	int iEspionagePoints = m_pUnitInfo->getEspionagePoints();
	iEspionagePoints *= GC.getInfo(GC.getGame().getGameSpeedType()).getUnitGreatWorkPercent();
	iEspionagePoints /= 100;
	return std::max(0, iEspionagePoints);
}

bool CvUnit::canInfiltrate(const CvPlot* pPlot, bool bTestVisible) const
{
	if (isDelayedDeath())
		return false;
	if (GC.getGame().isOption(GAMEOPTION_NO_ESPIONAGE))
		return false;
	if (getEspionagePoints(NULL) == 0)
		return false;
	CvCity const* pCity = pPlot->getPlotCity();
	if (pCity == NULL || pCity->isBarbarian() || pCity->isMinorCiv()) // doc: exclude minors
		return false;
	if (!bTestVisible)
	{
		if (NULL != pCity && pCity->getTeam() == getTeam())
			return false;
	}
	return true;
}


bool CvUnit::infiltrate()
{
	if (!canInfiltrate(plot()))
		return false;
	int iPoints = getEspionagePoints(NULL);
	GET_TEAM(getTeam()).changeEspionagePointsAgainstTeam(TEAMID(getPlot().getOwner()), iPoints);
	GET_TEAM(getTeam()).changeEspionagePointsEver(iPoints);
	if (getPlot().isActiveVisible(false))
		NotifyEntity(MISSION_INFILTRATE);
	kill(true);
	return true;
}


bool CvUnit::canEspionage(const CvPlot* pPlot, bool bTestVisible) const
{
	if (isDelayedDeath())
		return false;
	if (!isSpy())
		return false;
	if (GC.getGame().isOption(GAMEOPTION_NO_ESPIONAGE))
		return false;
	PlayerTypes ePlotOwner = pPlot->getOwner();
	if (NO_PLAYER == ePlotOwner)
		return false;
	CvPlayer& kTarget = GET_PLAYER(ePlotOwner);
	if (kTarget.isBarbarian())
		return false;
	if (kTarget.getTeam() == getTeam())
		return false;
	if (GET_TEAM(getTeam()).isVassal(kTarget.getTeam()))
		return false;
	if (!bTestVisible)
	{
		if (isMadeAttack())
			return false;
		if (hasMoved())
			return false;
		if (//kTarget.getTeam() != getTeam() && // advc: Already guaranteed
				!isInvisible(kTarget.getTeam(), false))
			return false;
	}
	return true;
}

bool CvUnit::espionage(EspionageMissionTypes eMission, int iData)
{
	if (!canEspionage(plot()))
		return false;

	PlayerTypes eTargetPlayer = getPlot().getOwner();

	if (eMission == NO_ESPIONAGEMISSION)
	{
		FAssert(GET_PLAYER(getOwner()).isHuman());
		CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_DOESPIONAGE);
		if (pInfo != NULL)
			gDLL->UI().addPopup(pInfo, getOwner(), true);
	}
	else if (GC.getInfo(eMission).isTwoPhases() && -1 == iData)
	{
		FAssert(GET_PLAYER(getOwner()).isHuman());
		CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_DOESPIONAGE_TARGET);
		if (pInfo != NULL)
		{
			pInfo->setData1(eMission);
			gDLL->UI().addPopup(pInfo, getOwner(), true);
		}
	}
	else
	{
		CvEspionageMissionInfo const& kMission = GC.getInfo(eMission);
		if (testSpyIntercepted(eTargetPlayer, true, kMission.getDifficultyMod()))
		{
			return false;
		}

	    int iMissionCostModifier = GET_PLAYER(getOwner()).getEspionageMissionCostModifier(eMission,
            eTargetPlayer, plot(), iData, this);
		if (GET_PLAYER(getOwner()).doEspionageMission(eMission, eTargetPlayer,
			plot(), iData, this))
		{
			if (getPlot().isActiveVisible(false))
				NotifyEntity(MISSION_ESPIONAGE);

			if (!testSpyIntercepted(eTargetPlayer, true, GC.getDefineINT("ESPIONAGE_SPY_MISSION_ESCAPE_MOD")))
			{
				setFortifyTurns(0);
				setMadeAttack(true);
				finishMoves();

                // doc: spies retreat to closest city
				CvCity* pClosestCity = GC.getMap().findCity(getX(), getY(), getOwner(), getTeam(), false);
				if (pClosestCity != NULL &&
					kMission.isReturnToCapital()) // advc.103
				{
					setXY(pClosestCity->getX(), pClosestCity->getY(), false, false, false);

					CvWString szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_SPY_SUCCESS",
							getNameKey(), pClosestCity->getNameKey());
					gDLL->UI().addMessage(getOwner(),
							/*  advc.103: Don't show message before the
								city screen has been exited */
							!GC.getInfo(eMission).isInvestigateCity(),
							-1, szBuffer, pClosestCity->getPlot(), "AS2D_POSITIVE_DINK",
							MESSAGE_TYPE_INFO, getButton());
				}

				// SuperSpies (TSHEEP): give spies xp for successful missions
				awardSpyExperience(GET_PLAYER(eTargetPlayer).getTeam(), eMission, iMissionCostModifier);
			}
			// K-Mod
			if (isActiveTeam())
				gDLL->UI().setDirty(CityInfo_DIRTY_BIT, true);
			// K-Mod end
			return true;
		}
	}

	return false;
}

bool CvUnit::testSpyIntercepted(PlayerTypes eTargetPlayer, bool bMission, int iModifier)
{
	CvPlayer& kTargetPlayer = GET_PLAYER(eTargetPlayer);
	if (kTargetPlayer.isBarbarian() || kTargetPlayer.isMinorCiv()) // rfc
	    return false;

	// doc: Bletchley Park effect
	if (GET_PLAYER(getOwner()).isHasBuildingEffect(BLETCHLEY_PARK))
	    iModifier += 50;
	if (GET_PLAYER(eTargetPlayer).isHasBuildingEffect(BLETCHLEY_PARK))
	    iModifier -= 50;

	if (!SyncRandSuccess10000((100 + iModifier) *
		getSpyInterceptPercent(kTargetPlayer.getTeam(), bMission)))
	{
		return false;
	}

	CvString szFormatNoReveal;
	CvString szFormatReveal;

	if (GET_TEAM(kTargetPlayer.getTeam()).getCounterespionageModAgainstTeam(getTeam()) > 0)
	{
		szFormatNoReveal = "TXT_KEY_SPY_INTERCEPTED_MISSION";
		szFormatReveal = "TXT_KEY_SPY_INTERCEPTED_MISSION_REVEAL";
	}
	else if (getPlot().isEspionageCounterSpy(kTargetPlayer.getTeam()))
	{
		szFormatNoReveal = "TXT_KEY_SPY_INTERCEPTED_SPY";
		szFormatReveal = "TXT_KEY_SPY_INTERCEPTED_SPY_REVEAL";
	}
	else
	{
		szFormatNoReveal = "TXT_KEY_SPY_INTERCEPTED";
		szFormatReveal = "TXT_KEY_SPY_INTERCEPTED_REVEAL";
	}

	CvWString szCityName = kTargetPlayer.getCivilizationShortDescription();
	CvCity* pClosestCity = GC.getMap().findCity(getX(), getY(), eTargetPlayer, kTargetPlayer.getTeam(), true, false);
	if (pClosestCity != NULL)
		szCityName = pClosestCity->getName();

	CvWString szBuffer = gDLL->getText(szFormatReveal.GetCString(),
			GET_PLAYER(getOwner()).getCivilizationAdjectiveKey(), getNameKey(),
			kTargetPlayer.getCivilizationAdjectiveKey(), szCityName.GetCString());
	gDLL->UI().addMessage(getOwner(), true, -1, szBuffer, getPlot(),
			"AS2D_EXPOSED", MESSAGE_TYPE_INFO, getButton(), GC.getColorType("RED"));

	static int const iESPIONAGE_SPY_REVEAL_IDENTITY_PERCENT = GC.getDefineINT("ESPIONAGE_SPY_REVEAL_IDENTITY_PERCENT"); // advc.opt
	if (!isAlwaysHeal() && SyncRandSuccess100(iESPIONAGE_SPY_REVEAL_IDENTITY_PERCENT)) // SuperSpies (TSHEEP): Loyalty promotion
	{
		if (!isEnemy(kTargetPlayer.getTeam()))
		{   // advc.130j:
			GET_PLAYER(eTargetPlayer).AI_rememberEvent(getOwner(), MEMORY_SPY_CAUGHT);
		}
		gDLL->UI().addMessage(eTargetPlayer, true, -1, szBuffer, getPlot(),
				"AS2D_EXPOSE", MESSAGE_TYPE_INFO, getButton(), GC.getColorType("GREEN"));
	}
	else
	{
		szBuffer = gDLL->getText(szFormatNoReveal.GetCString(), getNameKey(),
				kTargetPlayer.getCivilizationAdjectiveKey(), szCityName.GetCString());
		gDLL->UI().addMessage(eTargetPlayer, true, -1, szBuffer, getPlot(),
			"AS2D_EXPOSE", MESSAGE_TYPE_INFO, getButton(), GC.getColorType("GREEN"));
	}

	if (getPlot().isActiveVisible(false))
		NotifyEntity(MISSION_SURRENDER);

    // SuperSpies (TSHEEP): counterespionage experience
	CvUnit* pCounterUnit = plot()->plotCheck(PUF_isCounterSpy, -1, -1, NO_PLAYER, kTargetPlayer.getTeam());
	if (pCounterUnit != NULL)
	{
		pCounterUnit->changeExperience(1);
	}

	// SuperSpies: TSHEEP Implement Escape Promotion
	if(GC.getGame().getSorenRandNum(100, "Spy Reveal identity") < withdrawalProbability())
	{
		setFortifyTurns(0);
		setMadeAttack(true);
		finishMoves();

		CvCity* pCapital = GET_PLAYER(getOwner()).getCapitalCity();
		if (NULL != pCapital)
		{
			setXY(pCapital->getX(), pCapital->getY(), false, false, false);
		}
		szFormatReveal = "TXT_KEY_SPY_ESCAPED_REVEAL";
		szFormatNoReveal = "TXT_KEY_SPY_ESCAPED";
		szBuffer = gDLL->getText(szFormatReveal.GetCString(), GET_PLAYER(getOwner()).getCivilizationAdjectiveKey(), getNameKey(), kTargetPlayer.getCivilizationAdjectiveKey(), szCityName.GetCString());
		gDLL->getInterfaceIFace()->addMessage(getOwner(), true, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_EXPOSED", MESSAGE_TYPE_INFO, getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_GREEN"), getX(), getY(), true, true);
		szBuffer = gDLL->getText(szFormatNoReveal.GetCString(), getNameKey(), kTargetPlayer.getCivilizationAdjectiveKey(), szCityName.GetCString());
		gDLL->getInterfaceIFace()->addMessage(eTargetPlayer, true, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_EXPOSE", MESSAGE_TYPE_INFO, getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_RED"), getX(), getY(), true, true);

		changeExperience(1);
		testPromotionReady();

		return true;
	}
	//SuperSpies: TSHEEP End

	kill(true);
	return true;
}

int CvUnit::getSpyInterceptPercent(TeamTypes eTargetTeam, bool bMission) const
{
	FAssert(isSpy());
	FAssert(getTeam() != eTargetTeam);
	// <advc.opt>
	static int const iESPIONAGE_INTERCEPT_SPENDING_MAX = GC.getDefineINT("ESPIONAGE_INTERCEPT_SPENDING_MAX");
	static int const iESPIONAGE_INTERCEPT_COUNTERSPY = GC.getDefineINT("ESPIONAGE_INTERCEPT_COUNTERSPY");
	static int const iESPIONAGE_INTERCEPT_COUNTERESPIONAGE_MISSION = GC.getDefineINT("ESPIONAGE_INTERCEPT_COUNTERESPIONAGE_MISSION");
	static int const iESPIONAGE_INTERCEPT_RECENT_MISSION = GC.getDefineINT("ESPIONAGE_INTERCEPT_RECENT_MISSION");
	 // </advc.opt>
	int iSuccess = 0;

	/*int iTargetPoints = GET_TEAM(eTargetTeam).getEspionagePointsEver();
	int iOurPoints = GET_TEAM(getTeam()).getEspionagePointsEver();
	iSuccess += (iESPIONAGE_INTERCEPT_SPENDING_MAX * iTargetPoints) /
			std::max(1, iTargetPoints + iOurPoints);*/ // BtS
	// K-Mod. Scale based on the teams' population.
	{
		const CvTeam& kTeam = GET_TEAM(getTeam());
		const CvTeam& kTargetTeam = GET_TEAM(eTargetTeam);

		int iPopScale = 5 * GC.getInfo(GC.getMap().getWorldSize()).getTargetNumCities();
		int iTargetPoints = 10 * kTargetTeam.getEspionagePointsEver() /
				std::max(1, iPopScale + kTargetTeam.getTotalPopulation(false));
		int iOurPoints = 10 * kTeam.getEspionagePointsEver() /
				std::max(1, iPopScale + kTeam.getTotalPopulation(false));
		iSuccess += iESPIONAGE_INTERCEPT_SPENDING_MAX * iTargetPoints / std::max(1, iTargetPoints + iOurPoints);
	}
	// K-Mod end

	// SuperSpies (TSHEEP): add evasion attribute to spy chances
	if (getExtraEvasion() != 0)
	    iSuccess -= getExtraEvasion();

	if (getPlot().isEspionageCounterSpy(eTargetTeam))
    {
		iSuccess += iESPIONAGE_INTERCEPT_COUNTERSPY;

	    // SuperSpies (TSHEEP): add intercept attribute of any enemy spies present to chances
	    if (plot()->plotCheck(PUF_isCounterSpy, -1, -1, NO_PLAYER, eTargetTeam))
	    {
	        CvUnit* pCounterUnit = plot()->plotCheck(PUF_isCounterSpy, -1, -1, NO_PLAYER, eTargetTeam);
	        if (pCounterUnit->getExtraIntercept() != 0)
	            iSuccess += pCounterUnit->getExtraIntercept();
	    }
    }

	if (GET_TEAM(eTargetTeam).getCounterespionageModAgainstTeam(getTeam()) > 0)
		iSuccess += iESPIONAGE_INTERCEPT_COUNTERESPIONAGE_MISSION;

	// K-Mod. I've added the following condition for the recent mission bonus, to make spies less likely to be caught while exploring during peace time.
	if (bMission || atWar(getTeam(), eTargetTeam) ||
		GET_TEAM(eTargetTeam).getCounterespionageModAgainstTeam(getTeam()) > 1 || // SuperSpies (TSHEEP): this check was always returning true since there is always at least one friendly spy in the tile
		getPlot().isEspionageCounterSpy(eTargetTeam)) // K-Mod
	{
		if (getFortifyTurns() == 0 || getPlot().plotCount(PUF_isSpy, -1, -1, NO_PLAYER, getTeam()) > 1)
			iSuccess += iESPIONAGE_INTERCEPT_RECENT_MISSION;
	}

	return std::min(100, std::max(0, iSuccess));
}

bool CvUnit::isIntruding() const
{
	TeamTypes eLocalTeam = getPlot().getTeam();

	if (NO_TEAM == eLocalTeam || eLocalTeam == getTeam())
		return false;

	if (GET_TEAM(eLocalTeam).isVassal(getTeam()) ||
			// UNOFFICIAL_PATCH: Vassal's spies no longer caught in master's territory
			GET_TEAM(getTeam()).isVassal(eLocalTeam))
		return false;
	// <advc.034>
	if(GET_TEAM(eLocalTeam).isDisengage(getTeam()))
		return false; // </advc.034>
	return true;
}

bool CvUnit::canGoldenAge(const CvPlot* pPlot, bool bTestVisible) const
{
	if (!isGoldenAge())
		return false;
	if (!bTestVisible)
	{
		if (GET_PLAYER(getOwner()).unitsRequiredForGoldenAge() > GET_PLAYER(getOwner()).unitsGoldenAgeReady())
			return false;
	}
	return true;
}


bool CvUnit::goldenAge()
{
	if (!canGoldenAge(plot()))
		return false;

	GET_PLAYER(getOwner()).killGoldenAgeUnits(this);
	GET_PLAYER(getOwner()).changeGoldenAgeTurns(GET_PLAYER(getOwner()).getGoldenAgeLength());
	GET_PLAYER(getOwner()).changeNumUnitGoldenAges(1);

	if (getPlot().isActiveVisible(false))
		NotifyEntity(MISSION_GOLDEN_AGE);

	kill(true);
	return true;
}


bool CvUnit::canBuild(CvPlot const& kPlot, BuildTypes eBuild, bool bTestVisible,
	bool bIgnoreFoW) const // advc.181
{
    // doc: Hittite UP
    bool bHittiteUP = (getCivilizationType() == HITTITES && getUnitCombatType() == UNITCOMBAT_MELEE && eBuild != NO_BUILD && GC.getInfo(eBuild).isFeatureRemove(FEATURE_FOREST));
	if (!m_pUnitInfo->getBuilds(eBuild) && !bHittiteUP)
		return false;
	if (!GET_PLAYER(getOwner()).canBuild(kPlot, eBuild, false, bTestVisible,
		bIgnoreFoW)) // advc.181
		return false;
	if (!isValidDomain(kPlot.isWater()))
		return false;
    // doc: ability to use slaves
	if (getUnitInfo().isSlave() && GC.getInfo(eBuild).isKill() && !kPlot.canUseSlave(getOwner()))
        return false;

	return true;
}

// Returns true if build finished...
bool CvUnit::build(BuildTypes eBuild)
{
	if (!canBuild(getPlot(), eBuild))
		return false;
	// Note: notify entity must come before changeBuildProgress - because once the unit is done building,
	// that function will notify the entity to stop building.
	NotifyEntity((MissionTypes)GC.getInfo(eBuild).getMissionType());
	GET_PLAYER(getOwner()).changeGold(-(GET_PLAYER(getOwner()).getBuildCost(getPlot(), eBuild)));

	int iWorkRate = workRate(false);

	// doc: Chateau Frontenac effect
	if (GET_PLAYER(getOwner()).isHasBuildingEffect(FRONTENAC))
	{
	    if (GC.getInfo(eBuild).getTechPrereq() == RAILROAD)
	    {
	        iWorkRate *= 150;
	        iWorkRate /= 100;
	    }
	}

	bool bFinished = getPlot().changeBuildProgress(eBuild, iWorkRate,
			/*getTeam()*/ getOwner()); // advc.251
	finishMoves(); // needs to be at bottom because movesLeft() can affect workRate()...
	if (bFinished)
	{
		if (GC.getInfo(eBuild).isKill())
			kill(true);
	}
	CvEventReporter::getInstance().unitBuildImprovement(this, eBuild, bFinished);
	return bFinished;
}


bool CvUnit::canPromote(PromotionTypes ePromotion, int iLeaderUnitId) const
{
	if (iLeaderUnitId /* advc (was >=0): */ != FFreeList::INVALID_INDEX)
	{
		if (iLeaderUnitId == getID())
			return false;

		// The command is always possible if it's coming from a Warlord unit that gives just experience points
		CvUnit* pWarlord = GET_PLAYER(getOwner()).getUnit(iLeaderUnitId);
		if (pWarlord &&
			NO_UNIT != pWarlord->getUnitType() &&
			pWarlord->getUnitInfo().getLeaderExperience() > 0 &&
			NO_PROMOTION == pWarlord->getUnitInfo().getLeaderPromotion() &&
			canAcquirePromotionAny())
		{
			return true;
		}
	}

	if (ePromotion == NO_PROMOTION)
		return false;
	if (!canAcquirePromotion(ePromotion))
		return false;

	if (GC.getInfo(ePromotion).isLeader())
	{
		if (iLeaderUnitId >= 0)
		{
			CvUnit* pWarlord = GET_PLAYER(getOwner()).getUnit(iLeaderUnitId);
			if (pWarlord && NO_UNIT != pWarlord->getUnitType())
				return (pWarlord->getUnitInfo().getLeaderPromotion() == ePromotion);
		}
		return false;
	}
	return isPromotionReady();
}

void CvUnit::promote(PromotionTypes ePromotion, int iLeaderUnitId)
{
	if (!canPromote(ePromotion, iLeaderUnitId))
		return;
	// <advc.002l>
	bool bSound = true;
	bool const bSelected = IsSelected();
	// </advc.002l>
	if (iLeaderUnitId /* advc (was >=0): */ != FFreeList::INVALID_INDEX)
	{
		CvUnit* pWarlord = GET_PLAYER(getOwner()).getUnit(iLeaderUnitId);
		if (pWarlord != NULL)
		{
			pWarlord->giveExperience();
			if (!pWarlord->getNameNoDesc().empty())
				setName(pWarlord->getNameKey());
			//update graphics models
			m_eLeaderUnitType = pWarlord->getUnitType();
			reloadEntity();
		}
	}  // <advc.002l>
	else if (bSelected)
	{
		int iSelectedCanPromote = 0;
		for (CLLNode<IDInfo> const* pNode = gDLL->UI().headSelectionListNode();
			pNode != NULL; pNode = gDLL->UI().nextSelectionListNode(pNode))
		{
			CvUnit const* pUnit = ::getUnit(pNode->m_data);
			if (pUnit != NULL && pUnit->canPromote(ePromotion, iLeaderUnitId))
			{
				iSelectedCanPromote++;
				// Play sound only for the last promoted unit in a selected stack
				if (iSelectedCanPromote > 1)
				{
					bSound = false;
					break;
				}
			}
		}
	} // </advc.002l>

	if (!GC.getInfo(ePromotion).isLeader())
	{
		changeLevel(1);
		changeDamage(-promotionHeal(ePromotion)); // advc: Heal moved into new function
	}

	setHasPromotion(ePromotion, true);
	testPromotionReady();
	/*	K-Mod. (This currently isn't important because
		the AI doesn't use promotions mid-turn anyway.) */
	CvSelectionGroup::resetPath();

	if (bSelected)
	{
		if (bSound) // advc.002l
			gDLL->UI().playGeneralSound(GC.getInfo(ePromotion).getSound());

		gDLL->UI().setDirty(UnitInfo_DIRTY_BIT, true);
		gDLL->getFAStarIFace()->ForceReset(&GC.getInterfacePathFinder()); // K-Mod.
	}
	else setInfoBarDirty(true);

	CvEventReporter::getInstance().unitPromoted(this, ePromotion);
}
/*  <advc> Extracted from 'promote' above.
	Tbd.: Have any AI code that assumes HP from promotions call this.
	Also: Should set the percentage through XML. */
int CvUnit::promotionHeal(PromotionTypes ePromotion) const
{
    int iHealPercent = 50;
    if (ePromotion != NO_PROMOTION && GC.getInfo(ePromotion).isLeader())
        iHealPercent = 0;
    // doc: Triumphal Arch effect
    else if (GET_PLAYER(getOwner()).isHasBuildingEffect(TRIUMPHAL_ARCH))
        iHealPercent = 75;
	return (getDamage() * iHealPercent) / 100;
} // </advc>

bool CvUnit::lead(int iUnitId)
{
	if (!canLead(plot(), iUnitId))
		return false;

	PromotionTypes eLeaderPromotion = (PromotionTypes)m_pUnitInfo->getLeaderPromotion();

	if (iUnitId == -1)
	{
		CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_LEADUNIT, eLeaderPromotion, getID());
		if (pInfo)
			gDLL->UI().addPopup(pInfo, getOwner(), true);
		return false;
	}
	else
	{
		CvUnit* pUnit = GET_PLAYER(getOwner()).getUnit(iUnitId);
		if (!pUnit || !pUnit->canPromote(eLeaderPromotion, getID()))
			return false;

		pUnit->joinGroup(NULL, true, true);
		pUnit->promote(eLeaderPromotion, getID());

		if (getPlot().isActiveVisible(false))
			NotifyEntity(MISSION_LEAD);

		kill(true);
		return true;
	}
}


int CvUnit::canLead(CvPlot const* pPlot, int iUnitId) const
{
	PROFILE_FUNC();

	if (isDelayedDeath())
		return 0;

	if (getUnitType() == NO_UNIT)
		return 0;

	int iUnits = 0;

	if (iUnitId == -1)
	{
		FOR_EACH_UNIT_IN(pUnit, *pPlot)
		{
			if (pUnit == NULL)
			{
				FAssertMsg(pUnit != NULL, "Can this happen?"); // advc.test
				continue;
			}
			if (pUnit != this && pUnit->getOwner() == getOwner() &&
				pUnit->canPromote((PromotionTypes)m_pUnitInfo->getLeaderPromotion(), getID()))
			{
				iUnits++;
			}
		}
	}
	else
	{
		CvUnit* pUnit = GET_PLAYER(getOwner()).getUnit(iUnitId);
		if (pUnit != NULL && pUnit != this && pUnit->canPromote((PromotionTypes)
			m_pUnitInfo->getLeaderPromotion(), getID()))
		{
			iUnits = 1;
		}
	}
	return iUnits;
}


int CvUnit::canGiveExperience(CvPlot const* pPlot) const
{
	int iUnits = 0;
	if (getUnitType() != NO_UNIT && m_pUnitInfo->getLeaderExperience() > 0)
	{
		FOR_EACH_UNIT_IN(pUnit, *pPlot)
		{
			if (pUnit == NULL)
			{
				FAssertMsg(pUnit != NULL, "Can this happen?"); // advc.test
				continue;
			}
			if (pUnit != this && pUnit->getOwner() == getOwner() &&
				pUnit->canAcquirePromotionAny())
			{
				iUnits++;
			}
		}
	}
	return iUnits;
}

bool CvUnit::giveExperience()
{
	CvPlot* pPlot = plot();
	if(pPlot == NULL)
		return false;
	int iNumUnits = canGiveExperience(pPlot);
	if (iNumUnits <= 0)
		return false;

	int iTotalExperience = getStackExperienceToGive(iNumUnits);
	int iMinExperiencePerUnit = iTotalExperience / iNumUnits;
	int iRemainder = iTotalExperience % iNumUnits;

	int i = 0;
	FOR_EACH_UNIT_VAR_IN(pUnit, *pPlot)
	{
		// advc: NULL check removed
		if (pUnit != this && pUnit->getOwner() == getOwner() &&
			pUnit->canAcquirePromotionAny())
		{
			pUnit->changeExperience(i < iRemainder ?
					iMinExperiencePerUnit + 1 : iMinExperiencePerUnit);
			pUnit->testPromotionReady();
		}
		i++;
	}
	return true;
}

int CvUnit::getStackExperienceToGive(int iNumUnits) const
{
	return (m_pUnitInfo->getLeaderExperience() * (100 + std::min(
			//50 // K-Mod: +50% is too low as a maximum.
			GC.getDefineINT("WARLORD_MAXIMUM_EXTRA_EXPERIENCE_PERCENT"),
			(iNumUnits - 1) *
			GC.getDefineINT("WARLORD_EXTRA_EXPERIENCE_PER_UNIT_PERCENT")))) / 100;
}

int CvUnit::upgradePrice(UnitTypes eUnit) const
{
	{
		int iR = GC.getPythonCaller()->upgradePrice(*this, eUnit);
		if (iR >= 0)
			return iR;
	}
	if (isBarbarian())
		return 0;

	CvUnitInfo const& kUpgradeUnit = GC.getInfo(eUnit);

	int iPrice = GC.getDefineINT(CvGlobals::BASE_UNIT_UPGRADE_COST);
	iPrice += std::max(0, (GET_PLAYER(getOwner()).getProductionNeeded(eUnit) -
			GET_PLAYER(getOwner()).getProductionNeeded(getUnitType()))) *
			GC.getDefineINT(CvGlobals::UNIT_UPGRADE_COST_PER_PRODUCTION);

    // doc: work rate determines worker upgrade cost
	if (!canFight() && kUpgradeUnit.getWorkRate() > 0)
	{
		iPrice *= kUpgradeUnit.getWorkRate() - m_pUnitInfo->getWorkRate();
		iPrice /= 10;
	}

    // doc: siege units have low strength but high modifiers so factor it into the upgrade cost
	if (kUpgradeUnit.getCityAttackModifier() > 0 && m_pUnitInfo->getCityAttackModifier() > 0)
	{
		iPrice *= (100 + std::max(kUpgradeUnit.getCityAttackModifier(), m_pUnitInfo->getCityAttackModifier()));
		iPrice /= 100;
	}

    // doc: naval units have low strength so increase their upgrade cost
	if (kUpgradeUnit.getDomainType() == DOMAIN_SEA)
	{
		iPrice *= 2;
	}

	if (!isHuman() && !isBarbarian())
	{
		iPrice *= GC.getInfo(GC.getGame().getHandicapType()).getAIUnitUpgradePercent();
		iPrice /= 100;
		// advc.250d: Commented out
		/*iPrice *= std::max(0, ((GC.getInfo(GC.getGame().getHandicapType()).getAIPerEraModifier() * GET_PLAYER(getOwner()).getCurrentEra()) + 100));
		iPrice /= 100;*/
	}
	iPrice -= (iPrice * getUpgradeDiscount()) / 100;

	return std::max(0, iPrice); // advc.mnai: max (future-proofing)
}

// advc.080: Based on code cut from CvUnit::upgrade. The param is (so far) unused.
int CvUnit::upgradeXPChange(UnitTypes eUnit) const
{
	if(getLeaderUnitType() != NO_UNIT)
		return 0;

	static int const iMAX_EXPERIENCE_AFTER_UPGRADE = GC.getDefineINT("MAX_EXPERIENCE_AFTER_UPGRADE");
	return std::min(0, iMAX_EXPERIENCE_AFTER_UPGRADE - getExperience());
}


bool CvUnit::upgradeAvailable(UnitTypes eFromUnit, UnitClassTypes eToUnitClass,
	int iCount) const
{
	if (iCount > GC.getNumUnitClassInfos())
		return false;

	CvUnitInfo const& kFromUnit = GC.getInfo(eFromUnit);

	if (kFromUnit.getUpgradeUnitClass(eToUnitClass))
		return true;

	if (!kFromUnit.isAnyUpgradeUnitClass()) // advc.003t
		return false;

	FOR_EACH_ENUM(UnitClass)
	{
		if (!kFromUnit.getUpgradeUnitClass(eLoopUnitClass))
			continue;

		UnitTypes eLoopUnit = GC.getInfo(getCivilizationType()).
				getCivilizationUnits(eLoopUnitClass);
		if (eLoopUnit != NO_UNIT && upgradeAvailable(eLoopUnit, eToUnitClass, iCount + 1))
			return true;
	}
	return false;
}


bool CvUnit::canUpgrade(UnitTypes eUnit, bool bTestVisible) const
{
	if (eUnit == NO_UNIT)
		return false;

	if(!isReadyForUpgrade())
	    return false;
	if (isNoUpgrade()) // doc
	    return false;

	if (!bTestVisible)
	{
		if (GET_PLAYER(getOwner()).getGold() < upgradePrice(eUnit))
			return false;
	}

	if (hasUpgrade(eUnit))
		return true;

	return false;
}

bool CvUnit::isReadyForUpgrade() const
{
	if (!canMove())
		return false;

	if (getPlot().getTeam() != getTeam())
		return false;

	return true;
}

/*	finds the 'best' city which has a valid upgrade for the unit,
	it specifically does not check whether the unit can move, or if the player has enough gold to upgrade
	those are checked in canUpgrade()
	if bSearch is true, it will check every city, if not, it will only check the closest valid city
	NULL result means the upgrade is not possible */
CvCity* CvUnit::getUpgradeCity(bool bSearch) const
{
	CvPlayerAI& kPlayer = GET_PLAYER(getOwner());
	UnitAITypes eUnitAI = AI_getUnitAIType();

	int iCurrentValue = kPlayer.AI_unitValue(getUnitType(), eUnitAI, area());

	int iBestSearchValue = MAX_INT;
	CvCity* pBestUpgradeCity = NULL;

	FOR_EACH_ENUM(Unit)
	{
		int iNewValue = kPlayer.AI_unitValue(eLoopUnit, eUnitAI, area());
		if (iNewValue > iCurrentValue)
		{
			int iSearchValue;
			CvCity* pUpgradeCity = getUpgradeCity(eLoopUnit, bSearch, &iSearchValue);
			if (pUpgradeCity != NULL)
			{
				// if not searching or close enough, then this match will do
				if (!bSearch || iSearchValue < 16)
				{
					return pUpgradeCity;
				}

				if (iSearchValue < iBestSearchValue)
				{
					iBestSearchValue = iSearchValue;
					pBestUpgradeCity = pUpgradeCity;
				}
			}
		}
	}

	return pBestUpgradeCity;
}

/*	Finds the 'best' city which has a valid upgrade for the unit, to eUnit type.
	Specifically does not check whether the unit can move,
	or if the player has enough gold to upgrade; those are checked in canUpgrade().
	If bSearch is true, it will check every city, if not, it will
	only check the closest valid city.
	If iSearchValue is not NULL, then, on return, it will be the city's proximity value,
	lower is better.
	NULL result means the upgrade is not possible. */
CvCity* CvUnit::getUpgradeCity(UnitTypes eUnit, bool bSearch, int* iSearchValue) const
{
	//PROFILE_FUNC(); // advc (Not called all that frequently)
	if (eUnit == NO_UNIT)
		return NULL; // kmodx: was "false"; five more occurrences of that error in this function

	CvPlayerAI const& kOwner = GET_PLAYER(getOwner());
	CvUnitInfo const& kToUnit = GC.getInfo(eUnit);

	if (GC.getInfo(kOwner.getCivilizationType()).
		getCivilizationUnits(kToUnit.getUnitClassType()) != eUnit)
	{
		return NULL;
	}
	if (!upgradeAvailable(getUnitType(), kToUnit.getUnitClassType()))
		return NULL;

	if (kToUnit.getCargoSpace() < getCargo())
		return NULL;

	/*if (getCargo() > 0) { // K-Mod. (no point looping through everything if there is no cargo anyway.)
		FOR_EACH_UNIT_IN(pLoopUnit, getPlot()) {
			if (pLoopUnit->getTransportUnit() == this) { ... }
		}
	}*/ // <advc> Let's just use getCargoUnits (although it's potentially slower)
	std::vector<CvUnit*> apCargoUnits;
	getCargoUnits(apCargoUnits);
	for (size_t i = 0; i < apCargoUnits.size(); i++)
	{
		CvUnit const& kLoopUnit = *apCargoUnits[i]; // </advc>
		if (kToUnit.getSpecialCargo() != NO_SPECIALUNIT &&
			kToUnit.getSpecialCargo() != kLoopUnit.getSpecialUnitType())
		{
			return NULL;
		}
		if (kToUnit.getDomainCargo() != NO_DOMAIN &&
			kToUnit.getDomainCargo() != kLoopUnit.getDomainType())
		{
			return NULL;
		}
	}

	// sea units must be built on the coast
	bool const bCoastalOnly = (getDomainType() == DOMAIN_SEA);

	CvCity* pBestCity = NULL;
	int iBestValue = MAX_INT;

	if (bSearch) // check every city for our team
	{
		// air units can travel any distance
		bool bIgnoreDistance = (getDomainType() == DOMAIN_AIR);
		// check every player on our team's cities
		for (MemberAIIter itMember(getTeam()); itMember.hasNext(); ++itMember)
		{
			FOR_EACH_CITYAI_VAR(pCity, *itMember)
			{
				// if coastal only, then make sure we are coast
				CvArea const* pWaterArea = NULL;
				if (bCoastalOnly)
				{
					pWaterArea = pCity->waterArea();
					if (pWaterArea == NULL || pWaterArea->isLake())
						continue;
				}
				// can this city train this unit?
				//if (pLoopCity->canTrain(eUnit, false, false, true))
				if(pCity->canUpgradeTo(eUnit)) // advc.001b
				{
					// if we do not care about distance, then the first match will do.
					if (bIgnoreDistance)
					{
						// if we do not care about distance, then return 1 for value.
						if (iSearchValue != NULL)
							*iSearchValue = 1;
						return pCity;
					}
					int iValue = plotDistance(plot(), pCity->plot());
					// if not same area, not as good (lower numbers are better).
					if (!isArea(pCity->getArea()) &&
						(pWaterArea == NULL || !isArea(*pWaterArea)))
					{
						iValue *= 16;
					}
					// if we cannot path there, not as good.
					if (!generatePath(pCity->getPlot(), NO_MOVEMENT_FLAGS, true))
						iValue *= 16;
					/*	<advc.139> This should really be checked in a CvUnitAI function.
						That said, the whole search part of this function is really
						AI code; I don't think it's ever used for human units. */
					if((!canFight() || getDomainType() != DOMAIN_LAND) &&
						!pCity->AI_isSafe())
					{
						iValue *= (pCity->AI_isEvacuating() ? 12 : 6);
					} // </advc.139>
					if (iValue < iBestValue)
					{
						iBestValue = iValue;
						pBestCity = pCity;
					}
				}
			}
		}
	}
	else
	{
		// find the closest city
		CvCity* pClosestCity = GC.getMap().findCity(getX(), getY(),
				NO_PLAYER, getTeam(), true, bCoastalOnly);
		if (pClosestCity != NULL)
		{
			// if we can train, then return this city (otherwise it will return NULL)
			//if (pClosestCity->canTrain(eUnit, false, false, true))
			if (pClosestCity->canUpgradeTo(eUnit)) // advc.001b
			{
				// did not search, always return 1 for search value.
				iBestValue = 1;
				pBestCity = pClosestCity;
			}
		}
	}

	if (iSearchValue != NULL) // return the best value
		*iSearchValue = iBestValue;

	return pBestCity;
}


CvUnit* CvUnit::upgrade(UnitTypes eUnit) // K-Mod: this now returns the new unit.
{
	if (!canUpgrade(eUnit))
		return this;

	CvPlayerAI& kOwner = GET_PLAYER(getOwner());
	kOwner.changeGold(-upgradePrice(eUnit));

	// doc: make sure that upgrading to sea explore units actually makes a sea explore unit
	UnitAITypes eUnitAIType = AI_getUnitAIType();
    if (!isHuman() && GC.getInfo(eUnit).getDefaultUnitAIType() == UNITAI_EXPLORE_SEA && GET_PLAYER(getOwner()).AI_totalUnitAIs(UNITAI_EXPLORE_SEA) == 0)
	    eUnitAIType = UNITAI_EXPLORE_SEA;

	CvUnit* pUpgradeUnit = kOwner.initUnit(eUnit, getX(), getY(), eUnitAIType);
	FAssert(pUpgradeUnit != NULL);

	pUpgradeUnit->convert(this);
	/*	<advc.057> Crude; don't want to spend too much effort on this for now
		b/c it's only relevant for mod-mods. */
	if (!isHuman() && getGroup()->getNumUnits() > 1 &&
		AI_getUnitAIType() != UNITAI_ASSAULT_SEA &&
		(kOwner.AI_isAnyImpassable(eUnit) ||
		kOwner.AI_isAnyImpassable(getGroup()->getHeadUnit()->getUnitType())))
	{
		pUpgradeUnit->joinGroup(NULL);
	}
	else // </advc.057>
	{
		// K-Mod, swapped order with convert. (otherwise units on boats would be ungrouped.)
		pUpgradeUnit->joinGroup(getGroup());
	}
	pUpgradeUnit->finishMoves();
	// advc.080: Moved into subroutine
	pUpgradeUnit->changeExperience(pUpgradeUnit->upgradeXPChange(eUnit));
	if (gUnitLogLevel > 2)
	{
		CvWString szString;
		getUnitAIString(szString, AI_getUnitAIType());
		logBBAI("    %S spends %d to upgrade %S to %S, unit AI %S", kOwner.getCivilizationDescription(0), upgradePrice(eUnit), getName(0).GetCString(), pUpgradeUnit->getName(0).GetCString(), szString.GetCString());
	}

	return pUpgradeUnit; // K-Mod
}


HandicapTypes CvUnit::getHandicapType() const
{
	return GET_PLAYER(getOwner()).getHandicapType();
}


CivilizationTypes CvUnit::getCivilizationType() const
{
	return GET_PLAYER(getOwner()).getCivilizationType();
}


const wchar* CvUnit::getVisualCivAdjective(TeamTypes eForTeam) const
{
	if (getVisualOwner(eForTeam) == getOwner())
		return GC.getInfo(getCivilizationType()).getAdjectiveKey();
	return L"";
}


UnitTypes CvUnit::getCaptureUnitType(CivilizationTypes eCivilization) const
{
	FAssert(eCivilization != NO_CIVILIZATION);
	return (m_pUnitInfo->getUnitCaptureClassType() == NO_UNITCLASS ? NO_UNIT :
			GC.getInfo(eCivilization).getCivilizationUnits(
			m_pUnitInfo->getUnitCaptureClassType()));
}

// advc.010:
int CvUnit::getCaptureOdds(CvUnit const& kDefender) const
{
	if (isNoUnitCapture() || kDefender.getCaptureUnitType(
		GET_PLAYER(kDefender.getOwner()).getCivilizationType()) == NO_UNIT)
	{
		return 0;
	}
	if (!isAlwaysHostile())
	{
		if (GET_TEAM(getTeam()).hasJustDeclaredWar(kDefender.getTeam()) ||
			!GET_TEAM(getTeam()).isAtWar(kDefender.getTeam()))
		{
			return GC.getDefineINT(CvGlobals::DOW_UNIT_CAPTURE_CHANCE);
		}
	}
	return GC.getDefineINT(CvGlobals::BASE_UNIT_CAPTURE_CHANCE);
}


bool CvUnit::isBarbarian() const
{
	return GET_PLAYER(getOwner()).isBarbarian();
}


bool CvUnit::isHuman() const
{
	return GET_PLAYER(getOwner()).isHuman();
}


bool CvUnit::isIndependent() const
{
	return GET_PLAYER(getOwner()).isIndependent();
}


bool CvUnit::isNative() const
{
	return GET_PLAYER(getOwner()).isNative();
}


bool CvUnit::isMinorCiv() const
{
	return GET_PLAYER(getOwner()).isMinorCiv();
}


int CvUnit::visibilityRange() const
{
	return (GC.getDefineINT(CvGlobals::UNIT_VISIBILITY_RANGE) + getExtraVisibilityRange());
}


int CvUnit::baseMoves() const
{
	//return (m_pUnitInfo->getMoves() + getExtraMoves() + GET_TEAM(getTeam()).getExtraMoves(getDomainType()));
	// <advc.905b>
	int iR = m_pUnitInfo->getMoves() + getExtraMoves() +
			GET_TEAM(getTeam()).getExtraMoves(getDomainType());
	for(int i = 0; i < m_pUnitInfo->getNumSpeedBonuses(); i++)
	{
		if (GET_PLAYER(getOwner()).isSpeedBonusAvailable(
			m_pUnitInfo->getSpeedBonuses(i), getPlot()))
		{
			iR += m_pUnitInfo->getExtraMoves(i);
		}
	}
	return iR; // </advc.905b>
}


bool CvUnit::canMove() const
{
	if (isDead())
		return false;
	if (getMoves() >= maxMoves())
		return false;
	if (getImmobileTimer() > 0)
		return false;
	return true;
}

// XXX should this test for coal?
bool CvUnit::canBuildRoute() const
{	// <advc.003t>
	if (!m_pUnitInfo->isAnyBuilds())
		return false; // </advc.003t>
	FOR_EACH_ENUM(Build)
	{
		if (GC.getInfo(eLoopBuild).getRoute() != NO_ROUTE)
		{
			if (m_pUnitInfo->getBuilds(eLoopBuild))
			{
				if (GET_TEAM(getTeam()).isHasTech(GC.getInfo(eLoopBuild).getTechPrereq()))
					return true;
			}
		}
	}

	return false;
}

BuildTypes CvUnit::getBuildType() const
{
	if (getGroup()->headMissionQueueNode() != NULL)
	{
		switch (getGroup()->headMissionQueueNode()->m_data.eMissionType)
		{
		case MISSION_MOVE_TO:
			break;

		case MISSION_ROUTE_TO:
		{
			BuildTypes eBuild;
			if (getGroup()->getBestBuildRoute(getPlot(), &eBuild) != NO_ROUTE)
				return eBuild;
			break;
		}
		case MISSION_MOVE_TO_UNIT:
		case MISSION_SKIP:
		case MISSION_SLEEP:
		case MISSION_FORTIFY:
		case MISSION_PLUNDER:
		case MISSION_AIRPATROL:
		case MISSION_SEAPATROL:
		case MISSION_HEAL:
		case MISSION_SENTRY_HEAL: // advc.004l
		case MISSION_SENTRY:
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
			return (BuildTypes)getGroup()->headMissionQueueNode()->m_data.iData1;

		default:
			FAssert(false);
		}
	}

	return NO_BUILD;
}


int CvUnit::workRate(bool bMax) const
{
	if (!bMax && !canMove())
	    return 0;
    // doc: Hittite UP
	if (getCivilizationType() == HITTITES && getUnitCombatType() == UNITCOMBAT_MELEE)
	    return 100;
	int iRate = m_pUnitInfo->getWorkRate();
	iRate *= std::max(0, GET_PLAYER(getOwner()).getWorkerSpeedModifier() + 100);
	iRate /= 100;
	if (!isHuman() && !isBarbarian())
	{
		iRate *= std::max(0, GC.getInfo(GC.getGame().getHandicapType()).
				getAIWorkRateModifier() + 100);
		iRate /= 100;
	}
	return iRate;
}

// advc.315b: Renamed from "isNoCityCapture" b/c no-unit-capture is no longer implied
bool CvUnit::isNoCityCapture() const
{
	return (m_pUnitInfo->isNoCapture() ||
			m_pUnitInfo->isOnlyAttackAnimals()); // advc.315a
}

// advc.315b: Allow Explorers to capture units
bool CvUnit::isNoUnitCapture() const
{
	return (isNoCityCapture() && !m_pUnitInfo->isOnlyAttackBarbarians());
}


bool CvUnit::isMilitaryHappiness() const
{
	return (m_pUnitInfo->isMilitaryHappiness() &&
			isGarrisonInTeamCity()); // advc.184
}

// advc.184: Whether it is available for suppressing unhappiness and revolts
bool CvUnit::isGarrisonInTeamCity() const
{
	if (!getPlot().isCity())
		return false;
	CvTeam const& kCityTeam = GET_TEAM(getPlot().getTeam());
	if (isInvisible(kCityTeam.getID(), false))
		return false;
	return (kCityTeam.getID() == getTeam() ||
			kCityTeam.getMasterTeam() == getTeam() ||
			kCityTeam.getID() == GET_TEAM(getTeam()).getMasterTeam());
}

/*	advc.101: Replacing iCultureGarrison in XML, which increases too slowly
	over the course of the game. Note that CvCity::cultureStrength now also
	increases faster than in BtS. */
int CvUnit::garrisonStrength() const
{
	if (getDomainType() != DOMAIN_LAND || !canFight() ||
		m_pUnitInfo->getCultureGarrisonValue() <= 0)
	{
		return 0;
	}
	int r = baseCombatStr();
	int iModifier = (combatLimit() >= 100 ? 100 : 50);
	iModifier += cityDefenseModifier() + getExtraCombatPercent();
	// <advc.023>
	iModifier *= currHitPoints();
	iModifier /= 100; // </advc.023>
	return r * iModifier;
}


bool CvUnit::isGoldenAge() const
{
	if (isDelayedDeath())
		return false;
	return m_pUnitInfo->isGoldenAge();
}


bool CvUnit::canCoexistWithEnemyUnit(TeamTypes eTeam) const
{
	if (NO_TEAM == eTeam)
		return alwaysInvisible() || getUnitInfo().isDiplomaticMission();
	if (isInvisible(eTeam, false))
		return true;
	return false;
}


bool CvUnit::isAttacking() const
{
	return (getAttackPlot() != NULL && !isDelayedDeath());
}


bool CvUnit::isDefending() const
{
	return (isFighting() && !isAttacking());
}

// advc: Renamed from "isCombat"
bool CvUnit::isInCombat() const
{
	return (isFighting() || isAttacking());
}

void CvUnit::setBaseCombatStr(int iCombat)
{
	m_iBaseCombat = iCombat;
}

/*	maxCombatStr can be called in four different configurations
	+	pPlot == NULL, pAttacker == NULL for combat when this is the attacker;
	+	pPlot valid, pAttacker valid for combat when this is the defender;
	+	pPlot valid, pAttacker == NULL (new case), when this is the defender and
		the attacker is unknown;
	+	pPlot valid, pAttacker == this (new case), when the defender is unknown
		but we want to calc approx str.
		Note, in this last case, it is expected pCombatDetails == NULL,
		it does not have to be, but some values may be unexpectedly
		reversed in this case (iModifierTotal will be the negative sum). */
int CvUnit::maxCombatStr(CvPlot const* pPlot, CvUnit const* pAttacker,
	CombatDetails* pCombatDetails,
	bool bGarrisonStrength) const // advc.500b
{
	PROFILE_FUNC(); // advc: This does get called a lot. Not all that slow though.
	FAssert(pPlot == NULL || pPlot->getTerrainType() != NO_TERRAIN);

	// handle our new special case
	CvPlot const* pAttackedPlot = NULL;
	bool bAttackingUnknownDefender = false;
	if (pAttacker == this)
	{
		bAttackingUnknownDefender = true;
		pAttackedPlot = pPlot;

		// reset these values, we will fiddle with them below
		pPlot = NULL;
		pAttacker = NULL;
	}
	// otherwise, attack plot is the plot of us (the defender)
	else if (pAttacker != NULL)
		pAttackedPlot = plot();

	if (pCombatDetails != NULL)
		pCombatDetails->reset(getOwner(), getVisualOwner(), getName().c_str()); // advc

	if (baseCombatStr() == 0)
		return 0;

	int iModifier = 0;
	int iExtraModifier;

	iExtraModifier = getExtraCombatPercent();
	iModifier += iExtraModifier;
	if (pCombatDetails != NULL)
		pCombatDetails->iExtraCombatPercent = iExtraModifier;

	/*	do modifiers for animals and barbarians
		(leaving these out for bAttackingUnknownDefender case) */
	if (pAttacker != NULL)
	{
		if (isAnimal())
		{
			if (pAttacker->isHuman())
			{
				iExtraModifier = GC.getInfo(
						// K-Mod. Based on player's difficulty, not game difficulty.
						GET_PLAYER(pAttacker->getOwner()).getHandicapType()).
						getAnimalCombatModifier();
				iModifier += iExtraModifier;
				if (pCombatDetails != NULL)
					pCombatDetails->iAnimalCombatModifierTA = iExtraModifier;
			}
			else
			{
				iExtraModifier = GC.getInfo(GC.getGame().getHandicapType()).
						getAIAnimalCombatModifier();
				iModifier += iExtraModifier;
				if (pCombatDetails != NULL)
					pCombatDetails->iAIAnimalCombatModifierTA = iExtraModifier;
			}
		}

		if (pAttacker->isAnimal())
		{
			if (isHuman())
			{
				iExtraModifier = -GC.getInfo(
						GET_PLAYER(getOwner()).getHandicapType()). // K-Mod
						getAnimalCombatModifier();
				iModifier += iExtraModifier;
				if (pCombatDetails != NULL)
					pCombatDetails->iAnimalCombatModifierAA = iExtraModifier;
			}
			else
			{
				iExtraModifier = -GC.getInfo(GC.getGame().getHandicapType()).
						getAIAnimalCombatModifier();
				iModifier += iExtraModifier;
				if (pCombatDetails != NULL)
					pCombatDetails->iAIAnimalCombatModifierAA = iExtraModifier;
			}
		}

		if (isBarbarian())
		{	// advc.315c: And changed the iExtraModifier assignments below to +=
			iExtraModifier = -pAttacker->barbarianCombatModifier();
			if (pAttacker->isHuman())
			{
				iExtraModifier += GC.getInfo(
						GET_PLAYER(pAttacker->getOwner()).getHandicapType()). // K-Mod
						getBarbarianCombatModifier();
				iModifier += iExtraModifier;
				if (pCombatDetails != NULL)
					pCombatDetails->iBarbarianCombatModifierTB = iExtraModifier;
			}
			else
			{
				iExtraModifier += GC.getInfo(GC.getGame().getHandicapType()).
						getAIBarbarianCombatModifier();
				iModifier += iExtraModifier;
				if (pCombatDetails != NULL)
					pCombatDetails->iAIBarbarianCombatModifierTB = iExtraModifier;
			}
			// <advc.313>
			if (isKnownSeaBarbarian())
			{
				iExtraModifier = GC.getInfo(
						GET_PLAYER(pAttacker->getOwner()).getHandicapType()).
						get(CvHandicapInfo::SeaBarbarianBonus);
				iModifier += iExtraModifier;
				if (pCombatDetails != NULL)
					pCombatDetails->iSeaBarbarianModifierTB = iExtraModifier;
			} // </advc.313>
		}

		if (pAttacker->isBarbarian())
		{	// advc.315c: And changed the iExtraModifier assignments below to -=
			iExtraModifier = barbarianCombatModifier();
			if (isHuman())
			{
				iExtraModifier -= GC.getInfo(
						GET_PLAYER(getOwner()).getHandicapType()). // K-Mod
						getBarbarianCombatModifier();
				iModifier += iExtraModifier;
				if (pCombatDetails != NULL)
					pCombatDetails->iBarbarianCombatModifierAB = iExtraModifier;
			}
			else
			{
				iExtraModifier -= GC.getInfo(GC.getGame().getHandicapType()).
						getAIBarbarianCombatModifier();
				iModifier += iExtraModifier;
				if (pCombatDetails != NULL)
					pCombatDetails->iAIBarbarianCombatModifierTB = iExtraModifier;
			}
			// <advc.313>
			if (pAttacker->isKnownSeaBarbarian())
			{
				iExtraModifier = -GC.getInfo(
						GC.getGame().getHandicapType()).
						get(CvHandicapInfo::SeaBarbarianBonus);
				iModifier += iExtraModifier;
				if (pCombatDetails != NULL)
					pCombatDetails->iSeaBarbarianModifierAB = iExtraModifier;
			} // </advc.313>
		}
	}

	// add defensive bonuses (leaving these out for bAttackingUnknownDefender case)
	if (pPlot != NULL)
	{
		if (!noDefensiveBonus())
		{
			/*	BETTER_BTS_AI_MOD, General AI, 03/30/10, jdog5000:
				When pAttacker is NULL but pPlot is not, this is a computation
				for this units defensive value against an unknown attacker.
				Always ignoring building defense in this case is a conservative estimate,
				but causes AI to suicide against castle walls of low-culture cities
				in the early game. Using this unit's ignoreBuildingDefense does
				a little better ... in early game it corrects undervalue of castles.
				One downside is when medieval unit is defending a walled city
				against gunpowder. Here, the overvalue makes attacker a little more cautious,
				but with their tech lead it shouldn't matter too much. Also makes vulnerable units
				(ships, etc) feel safer in this case and potentially not leave, but ships leave
				when ratio is pretty low anyway. */
			//iExtraModifier = pPlot->defenseModifier(getTeam(), (pAttacker != NULL) ? pAttacker->ignoreBuildingDefense() : true);
			/*  <advc.012> Only functional change to the BBAI line: feature defense
				is counted based on AI_plotDefense if the attacker is unknown */
			bool bIgnoreBuildings = (pAttacker != NULL ?
					pAttacker->ignoreBuildingDefense() :
					ignoreBuildingDefense());
			if (pAttacker == NULL)
			{
				iExtraModifier = GET_TEAM(getTeam()).AI_plotDefense(*pPlot, bIgnoreBuildings,
						bGarrisonStrength); // advc.500b
			}
			else
			{
				iExtraModifier = pPlot->defenseModifier(getTeam(),
						bIgnoreBuildings, pAttacker->getTeam());
			} // </advc.012>
			iModifier += iExtraModifier;
			if (pCombatDetails != NULL)
				pCombatDetails->iPlotDefenseModifier = iExtraModifier;
		}
		if (!bGarrisonStrength) // advc.500b
			iExtraModifier = fortifyModifier();
		iModifier += iExtraModifier;
		if (pCombatDetails != NULL)
			pCombatDetails->iFortifyModifier = iExtraModifier;
		//if (pPlot->isCity(true, getTeam()))
		if (GET_TEAM(getTeam()).isCityDefense(*pPlot, // advc
			pAttacker == NULL ? NO_TEAM : pAttacker->getTeam())) // advc.183
		{
			iExtraModifier = cityDefenseModifier();
			iModifier += iExtraModifier;
			if (pCombatDetails != NULL)
				pCombatDetails->iCityDefenseModifier = iExtraModifier;
		}
		if (pPlot->isHills())
		{
			iExtraModifier = hillsDefenseModifier();
			iModifier += iExtraModifier;
			if (pCombatDetails != NULL)
				pCombatDetails->iHillsDefenseModifier = iExtraModifier;
		}
	    if (pPlot->isPlains()) // doc
	    {
	        iExtraModifier = plainsDefenseModifier();
	        iModifier += iExtraModifier;
	        if (pCombatDetails != NULL)
	        {
	            pCombatDetails->iPlainsDefenseModifier = iExtraModifier;
	        }
	    }
		if (pPlot->isFeature())
		{
			iExtraModifier = featureDefenseModifier(pPlot->getFeatureType());
			iModifier += iExtraModifier;
			if (pCombatDetails != NULL)
				pCombatDetails->iFeatureDefenseModifier = iExtraModifier;
		}
		// doc: terrain defense requires no feature or no feature with its own defense modifier
		if (!pPlot->isFeature() || GC.getInfo(pPlot->getFeatureType()).getDefenseModifier() == 0)
		{
			iExtraModifier = terrainDefenseModifier(pPlot->getTerrainType());
			iModifier += iExtraModifier;
			if (pCombatDetails != NULL)
				pCombatDetails->iTerrainDefenseModifier = iExtraModifier;
		}
	}

	// if we are attacking to an plot with an unknown defender, the calc the modifier in reverse
	if (bAttackingUnknownDefender)
		pAttacker = this;

	// calc attacker's modifiers
	if (pAttacker != NULL && pAttackedPlot != NULL)
	{
		int iTempModifier = 0;
		//if (pAttackedPlot->isCity(true, getTeam()))
		if (GET_TEAM(getTeam()).isCityDefense(*pAttackedPlot, // advc
			pAttacker->getTeam())) // advc.183
		{
			iExtraModifier = -pAttacker->cityAttackModifier();
			iTempModifier += iExtraModifier;
			if (pCombatDetails != NULL)
				pCombatDetails->iCityAttackModifier = iExtraModifier;
			if (pAttacker->isBarbarian())
			{
				iExtraModifier = //GC.getDefineINT("CITY_BARBARIAN_DEFENSE_MODIFIER")
						// <advc.313>
						-GC.getInfo(GC.getGame().getHandicapType()).
						get(CvHandicapInfo::BarbarianCityAttackBonus); // </advc.313>
				iTempModifier += iExtraModifier;
				if (pCombatDetails != NULL)
				{
					pCombatDetails->//iCityBarbarianDefenseModifier
							iBarbarianCityAttackModifier = iExtraModifier; // advc.313
				}
			}
		}
		if (pAttackedPlot->isHills())
		{
			iExtraModifier = -pAttacker->hillsAttackModifier();
			iTempModifier += iExtraModifier;
			if (pCombatDetails != NULL)
				pCombatDetails->iHillsAttackModifier = iExtraModifier;
		}
	    if (pAttackedPlot->isPlains()) // doc
	    {
	        iExtraModifier = -pAttacker->plainsAttackModifier();
	        iTempModifier += iExtraModifier;
	        if (pCombatDetails != NULL)
	        {
	            pCombatDetails->iPlainsAttackModifier = iExtraModifier;
	        }
	    }
	    // doc: river attack modifier
	    if (!pAttackedPlot->isCity() && pAttackedPlot->isRiver() && pAttacker->plot()->isRiver())
	    {
	        iExtraModifier = -pAttacker->riverAttackModifier();
	        iTempModifier += iExtraModifier;
	        if (pCombatDetails != NULL)
	        {
	            pCombatDetails->iRiverAttackModifier = iExtraModifier;
	        }
	    }
		if (pAttackedPlot->isFeature())
		{
			iExtraModifier = -pAttacker->featureAttackModifier(pAttackedPlot->getFeatureType());
			iTempModifier += iExtraModifier;
			if (pCombatDetails != NULL)
				pCombatDetails->iFeatureAttackModifier = iExtraModifier;
		}
		// doc: no feature or feature without defense modifier
		if (!pAttackedPlot->isFeature() || GC.getInfo(pAttackedPlot->getFeatureType()).getDefenseModifier() == 0)
		{
			iExtraModifier = -pAttacker->terrainAttackModifier(pAttackedPlot->getTerrainType());
			iTempModifier += iExtraModifier;
			if (pCombatDetails != NULL)
				pCombatDetails->iTerrainAttackModifier = iExtraModifier;
		}
		// doc: Vietnamese UP
		if (pAttacker->getCivilizationType() == VIETNAM && pAttacker->getOwner() == pAttackedPlot->getOwner())
		{
			if (!pAttacker->noDefensiveBonus())
			{
				iExtraModifier = -pAttacker->plot()->defenseModifier(pAttacker->getTeam(), ignoreBuildingDefense());

				iTempModifier += iExtraModifier;
				if (pCombatDetails != NULL)
				{
					pCombatDetails->iPlotDefenseModifier = iExtraModifier;
				}
			}
			iExtraModifier = -pAttacker->fortifyModifier();
			iTempModifier += iExtraModifier;
			if (pCombatDetails != NULL)
			{
				pCombatDetails->iFortifyModifier = iExtraModifier;
			}
			if (GET_TEAM(pAttacker->getTeam()).isCityDefense(*pPlot, getTeam()))
			{
				iExtraModifier = -pAttacker->cityDefenseModifier();
				iTempModifier += iExtraModifier;
				if (pCombatDetails != NULL)
				{
					pCombatDetails->iCityDefenseModifier = iExtraModifier;
				}
			}
			if (pAttacker->plot()->isHills())
			{
				iExtraModifier = -pAttacker->hillsDefenseModifier();
				iTempModifier += iExtraModifier;
				if (pCombatDetails != NULL)
				{
					pCombatDetails->iHillsDefenseModifier = iExtraModifier;
				}
			}
			if (pAttacker->plot()->isPlains()) // doc
			{
				iExtraModifier = -pAttacker->plainsDefenseModifier();
				iTempModifier += iExtraModifier;
				if (pCombatDetails != NULL)
				{
					pCombatDetails->iPlainsDefenseModifier = iExtraModifier;
				}
			}
			if (pAttacker->plot()->isFeature())
			{
				iExtraModifier = -pAttacker->featureDefenseModifier(pAttacker->plot()->getFeatureType());
				iTempModifier += iExtraModifier;
				if (pCombatDetails != NULL)
				{
					pCombatDetails->iFeatureDefenseModifier = iExtraModifier;
				}
			}

			if (!pAttacker->plot()->isFeature() || GC.getInfo(pAttacker->plot()->getFeatureType()).getDefenseModifier() == 0)
			{
				iExtraModifier = -pAttacker->terrainDefenseModifier(pAttacker->plot()->getTerrainType());
				iTempModifier += iExtraModifier;
				if (pCombatDetails != NULL)
				{
					pCombatDetails->iTerrainDefenseModifier = iExtraModifier;
				}
			}
		}

		// only compute comparisons if we are the defender with a known attacker
		if (!bAttackingUnknownDefender)
		{
			FAssertMsg(pAttacker != this, "pAttacker is not expected to be equal with this");

			iExtraModifier = unitClassDefenseModifier(pAttacker->getUnitClassType());
			iTempModifier += iExtraModifier;
			if (pCombatDetails != NULL)
				pCombatDetails->iClassDefenseModifier = iExtraModifier;

			iExtraModifier = -pAttacker->unitClassAttackModifier(getUnitClassType());
			iTempModifier += iExtraModifier;
			if (pCombatDetails != NULL)
				pCombatDetails->iClassAttackModifier = iExtraModifier;

			if (pAttacker->getUnitCombatType() != NO_UNITCOMBAT)
			{
				iExtraModifier = unitCombatModifier(pAttacker->getUnitCombatType());
				iTempModifier += iExtraModifier;
				if (pCombatDetails != NULL)
					pCombatDetails->iCombatModifierA = iExtraModifier;
			}
			if (getUnitCombatType() != NO_UNITCOMBAT)
			{
				iExtraModifier = -pAttacker->unitCombatModifier(getUnitCombatType());
				iTempModifier += iExtraModifier;
				if (pCombatDetails != NULL)
					pCombatDetails->iCombatModifierT = iExtraModifier;
			}
			iExtraModifier = domainModifier(pAttacker->getDomainType());
			iTempModifier += iExtraModifier;
			if (pCombatDetails != NULL)
				pCombatDetails->iDomainModifierA = iExtraModifier;

			iExtraModifier = -pAttacker->domainModifier(getDomainType());
			iTempModifier += iExtraModifier;
			if (pCombatDetails != NULL)
				pCombatDetails->iDomainModifierT = iExtraModifier;

			if (pAttacker->isAnimal())
			{
				iExtraModifier = animalCombatModifier();
				iTempModifier += iExtraModifier;
				if (pCombatDetails != NULL)
					pCombatDetails->iAnimalCombatModifierA = iExtraModifier;
			}
			if (isAnimal())
			{
				iExtraModifier = -pAttacker->animalCombatModifier();
				iTempModifier += iExtraModifier;
				if (pCombatDetails != NULL)
					pCombatDetails->iAnimalCombatModifierT = iExtraModifier;
			}
		}
		if (!pAttacker->isRiver() &&
			// advc.opt: isRiverCrossing is no longer supposed to handle non-adjacent tiles
			stepDistance(pAttacker->plot(), pAttackedPlot) == 1)
		{
			if (pAttacker->getPlot().isRiverCrossing(
				directionXY(pAttacker->getPlot(), *pAttackedPlot)))
			{
				iExtraModifier = -GC.getDefineINT(CvGlobals::RIVER_ATTACK_MODIFIER);
				iTempModifier += iExtraModifier;
				if (pCombatDetails != NULL)
					pCombatDetails->iRiverAttackModifier = iExtraModifier;
			}
		}
		if (!pAttacker->isAmphib())
		{
			if (!pAttackedPlot->isWater() && pAttacker->getPlot().isWater())
			{
				iExtraModifier = -GC.getDefineINT(CvGlobals::AMPHIB_ATTACK_MODIFIER);
				iTempModifier += iExtraModifier;
				if (pCombatDetails != NULL)
					pCombatDetails->iAmphibAttackModifier = iExtraModifier;
			}
		}
		if (pAttacker->getKamikazePercent() != 0)
		{
			iExtraModifier = pAttacker->getKamikazePercent();
			iTempModifier += iExtraModifier;
			if (pCombatDetails != NULL)
				pCombatDetails->iKamikazeModifier = iExtraModifier;
		}

		// if we are attacking an unknown defender, then use the reverse of the modifier
		if (bAttackingUnknownDefender)
			iModifier -= iTempModifier;
		else iModifier += iTempModifier;
	}

	if (pCombatDetails != NULL)
	{
		pCombatDetails->iModifierTotal = iModifier;
		pCombatDetails->iBaseCombatStr = baseCombatStr();
	}
	int iCombat;
	if (iModifier > 0)
		iCombat = (baseCombatStr() * (iModifier + 100));
	else iCombat = ((baseCombatStr() * 10000) / (100 - iModifier));

	if (pCombatDetails != NULL)
	{
		pCombatDetails->iCombat = iCombat;
		pCombatDetails->iMaxCombatStr = std::max(1, iCombat);
		pCombatDetails->iCurrHitPoints = currHitPoints();
		pCombatDetails->iMaxHitPoints = maxHitPoints();
		pCombatDetails->iCurrCombatStr = (pCombatDetails->iMaxCombatStr *
				pCombatDetails->iCurrHitPoints) / pCombatDetails->iMaxHitPoints;
	}

	return std::max(1, iCombat);
}

// this nomalizes str by firepower, useful for quick odds calcs
// the effect is that a damaged unit will have an effective str lowered by firepower/maxFirepower
// doing the algebra, this means we mulitply by 1/2(1 + currHP)/maxHP = (maxHP + currHP) / (2 * maxHP)
int CvUnit::currEffectiveStr(CvPlot const* pPlot, CvUnit const* pAttacker,
	CombatDetails* pCombatDetails,
	int iCurrentHP) const // advc.139
{
	int iCurrStr = currCombatStr(pPlot, pAttacker, pCombatDetails);

	iCurrStr *= (maxHitPoints() + /* advc.139: */ (iCurrentHP > 0 ? iCurrentHP :
			currHitPoints()));
	iCurrStr /= (2 * maxHitPoints());

	return iCurrStr;
}

float CvUnit::maxCombatStrFloat(const CvPlot* pPlot, const CvUnit* pAttacker) const
{
	return (((float)(maxCombatStr(pPlot, pAttacker))) / 100.0f);
}


float CvUnit::currCombatStrFloat(const CvPlot* pPlot, const CvUnit* pAttacker) const
{
	return (((float)(currCombatStr(pPlot, pAttacker))) / 100.0f);
}


bool CvUnit::canSiege(TeamTypes eTeam) const
{
	if (!canDefend())
		return false;

	if (!isEnemy(eTeam))
		return false;

	if (!isNeverInvisible())
		return false;
	// <advc.033> (for AlwaysHostile units, which pass the isEnemy check)
	if(GET_TEAM(eTeam).isVassal(getTeam()) ||
		GET_TEAM(getTeam()).isVassal(eTeam))
	{
		return false;
	} // </advc.033>
	return true;
}

// kekm.8: "Added function for checking whether a unit is a combat unit."
bool CvUnit::canCombat() const
{
	// avdc: Check m_pUnitInfo->isMilitaryProduction() instead?
	return (baseCombatStr() > 0 || airBaseCombatStr() > 0 || isNuke());
}


bool CvUnit::canAttack() const
{
	if (!canFight())
		return false;
	if (isOnlyDefensive())
		return false;
	return true;
}

/*	advc.089 (comment): Help text for these checks is handled by
	CvGameTextMgr::setCannotAttackHelp (some code duplication) */
bool CvUnit::canAttack(const CvUnit& kDefender) const
{
	//PROFILE_FUNC(); // advc: Called "only" a few hundred thousand times per turn; pretty fast.
	//if (!canAttack())
	if (!canCombat() || isOnlyDefensive()) // advc.089: Need to handle air units
		return false;
	// <advc.315a>
	if (m_pUnitInfo->isOnlyAttackAnimals() && !kDefender.isAnimal())
		return false; // </advc.315a>
	// <advc.315b>
	if (m_pUnitInfo->isOnlyAttackBarbarians() && !kDefender.isBarbarian())
		return false; // </advc.315b>
	/*  <advc.089> Previously, the air combat limit was checked in CvPlot::hasDefender.
		If either limit isn't reached, then some form of attack is possible.
		(For units that have both a ranged attack and regular attack ability,
		the mode of attack would have to be known in order to check the proper
		damage limit here. So such units aren't supported.) */
	if (kDefender.getDamage() >= std::max(combatLimit(), airCombatLimit()))
		return false; // </advc.089>
	// Artillery can't amphibious attack
	if (combatLimit() < 100 && /* advc.089: */ getDomainType() == DOMAIN_LAND &&
		getPlot().isWater() && !kDefender.getPlot().isWater() && !isAmphib()) // doc: amphibious promotion
	{
		return false;
	} /* <advc.089> This prevents combat odds from being shown when pressing
		 ALT while hovering over one's own units */
	if(getTeam() == kDefender.getTeam())
		return false;
	/*  Can't attack defenseless units that are stacked
		with a defender whose damage limit is reached. */
	if (combatLimit() < 100 &&
		(!kDefender.canFight() ||
		(kDefender.getDomainType() != DOMAIN_LAND && getDomainType() == DOMAIN_LAND)) &&
		/*  Won't handle invisible defenders correctly
			(there are none currently that can defend) */
		kDefender.getPlot().plotCheck(PUF_isEnemy, getOwner(), false,
		NO_PLAYER, NO_TEAM, PUF_canDefend) != NULL)
	{
		return false;
	} // </advc.089>
	return true;
}

/*  advc (clarification): "defend" as in: fight back when attacked. May still
	get chosen as a defender when canDefend returns false. */
bool CvUnit::canDefend(const CvPlot* pPlot) const
{
	if(!canFight())
		return false;

	if(pPlot == NULL)
		pPlot = plot();

	if (!isValidDomain(pPlot->isWater()))
	{
		if (!GC.getDefineBOOL(CvGlobals::LAND_UNITS_CAN_ATTACK_WATER_CITIES))
			return false;
	}

	return true;
}

// advc: Based on code removed from CvPlot::getBestDefender and CvPlot::hasDefender
bool CvUnit::canBeAttackedBy(PlayerTypes eAttackingPlayer,
	CvUnit const* pAttacker, bool bTestEnemy, bool bTestPotentialEnemy,
	/* <advc.028> */ bool bTestVisible, /* </advc.028> */ bool bTestCanAttack) const
{
	FAssert(eAttackingPlayer != NO_PLAYER);
	if (/* advc.028: */ bTestVisible &&
		isInvisible(TEAMID(eAttackingPlayer), /* advc.028: */ false))
	{
		return false;
	}
	if (bTestEnemy)
	{
		if (!isEnemy(TEAMID(eAttackingPlayer)) &&
			/*	Need to check both if pAttacker is given, otherwise attacks
				_against_ Privateers aren't possible (cf. comment above isEnemy). */
			(pAttacker == NULL || !pAttacker->isEnemy(getTeam(), getPlot())))
		{
			return false;
		}
	}
	if (bTestPotentialEnemy)
	{
		//if (!isPotentialEnemy(TEAMID(eAttackingPlayer), plot()))
		// <advc>
		if (!AI().AI_isPotentialEnemyOf(TEAMID(eAttackingPlayer), getPlot()) &&
			(pAttacker == NULL ||
			//if (!pAttacker->isPotentialEnemy(getTeam(), plot()))
			!pAttacker->AI().AI_isPotentialEnemyOf(getTeam(), getPlot()))) // </advc>
		{
			return false;
		}
	}
	// <advc>
	if (pAttacker != NULL)
	{
		// Moved from CvPlot::hasDefender
		if (bTestCanAttack && !pAttacker->canAttack(*this))
			return false;
	} // </advc>
	return true;
}


// doc
bool CvUnit::canDefendAgainst(const CvUnit* pAttacker, const CvPlot* pPlot) const
{
	// doc: Turkic UP
	if (isBarbarian() && pAttacker->getCivilizationType() == TURKS && GET_TEAM(pAttacker->getTeam()).isAtWarWithMajorPlayer())
	{
	    if (getUnitCombatType() == UNITCOMBAT_LIGHT_CAVALRY || getUnitCombatType() == UNITCOMBAT_HEAVY_CAVALRY)
	        return false;
	}

	return canDefend(pPlot);
}


bool CvUnit::isBetterDefenderThan(const CvUnit* pDefender, const CvUnit* pAttacker,
	int* pBestDefenderRank, // Lead From Behind by UncutDragon
	bool bPreferUnowned) const // advc.061
{
	TeamTypes eAttackerTeam = NO_TEAM;
	if (pAttacker != NULL)
		eAttackerTeam = pAttacker->getTeam();

	// <advc.028>
	bool bInvisible = (eAttackerTeam != NO_TEAM && isInvisible(eAttackerTeam, false));
	// Only pick invisible unit as defender once attack is underway ...
	if (bInvisible && (pAttacker->getAttackPlot() == NULL ||
		pAttacker->getDomainType() == DOMAIN_AIR)) // And don't defend against air attack
	{
		return false;
	}
	/*  ... and if there is some visible team unit that could get attacked otherwise
		(better: check if our team has the best visible defender; tbd.) ... */
	if (bInvisible &&
		!isSeaPatrolling()) // ... or when we're sea patrolling.
	{
		bool bFound = false;
		FOR_EACH_UNIT_IN(pUnit, getPlot())
		{
			if (pUnit->getTeam() == getTeam() && !pUnit->isInvisible(eAttackerTeam, false))
				bFound = true;
		}
		if (!bFound)
			return false;
	}
	// Moved down: // </advc.028>
	if (pDefender == NULL)
		return true;
	// <advc.028>
	if(pDefender->getTeam() != getTeam() && bInvisible)
		return false; // </advc.028>
	if (canCoexistWithEnemyUnit(eAttackerTeam))
		return false;

	if (!canDefend())
		return false;

	if (canDefend() && !pDefender->canDefend())
		return true;

	// <advc.061>
	if(bPreferUnowned)
	{
		bool bUnowned = isUnowned();
		if(bUnowned != pDefender->isUnowned())
			return bUnowned;
	} // </advc.061>

	if (pAttacker != NULL)
	{
		if (isTargetOf(*pAttacker) && !pDefender->isTargetOf(*pAttacker))
			return true;
		if (!isTargetOf(*pAttacker) && pDefender->isTargetOf(*pAttacker))
			return false;
		if (pAttacker->canAttack(*pDefender) && !pAttacker->canAttack(*this))
			return false;
		if (pAttacker->canAttack(*this) && !pAttacker->canAttack(*pDefender))
			return true;
	}

	// UncutDragon
	// To cut down on changes to existing code, we just short-circuit the method
	// and this point and call our own version instead
	if (GC.getDefineBOOL(CvGlobals::LFB_ENABLE))
		return LFBisBetterDefenderThan(pDefender, pAttacker, pBestDefenderRank);
	// /UncutDragon

// advc (comment): Start of legacy BtS code
	int iOurDefense = currCombatStr(plot(), pAttacker);
	if (m_pUnitInfo->isWorldUnit())
		iOurDefense /= 2;

	if (pAttacker == NULL)
	{
		if (pDefender->collateralDamage() > 0)
		{
			iOurDefense *= 100 + pDefender->collateralDamage();
			iOurDefense /= 100;
		}

		if (pDefender->currInterceptionProbability() > 0)
		{
			iOurDefense *= 100 + pDefender->currInterceptionProbability();
			iOurDefense /= 100;
		}
	}
	else
	{
		if (!pAttacker->immuneToFirstStrikes())
		{
			iOurDefense *= 100 +
					((firstStrikes() * 2 + chanceFirstStrikes()) *
					GC.getCOMBAT_DAMAGE() * 2) / 5;
			iOurDefense /= 100;
		}

		if (immuneToFirstStrikes())
		{
			iOurDefense *= 100 +
					((pAttacker->firstStrikes() * 2 +
					pAttacker->chanceFirstStrikes()) *
					GC.getCOMBAT_DAMAGE() * 2) / 5;
			iOurDefense /= 100;
		}
	}

	int iAssetValue = std::max(1, m_pUnitInfo->getAssetValue());
	int iCargoAssetValue = 0;
	std::vector<CvUnit*> aCargoUnits;
	getCargoUnits(aCargoUnits);
	for (uint i = 0; i < aCargoUnits.size(); ++i)
	{
		iCargoAssetValue += aCargoUnits[i]->getUnitInfo().getAssetValue();
	}
	iOurDefense = iOurDefense * iAssetValue / std::max(1, iAssetValue + iCargoAssetValue);

	int iTheirDefense = pDefender->currCombatStr(plot(), pAttacker);
	if (pDefender->m_pUnitInfo->isWorldUnit())
		iTheirDefense /= 2;

	if (pAttacker == NULL)
	{
		if (collateralDamage() > 0)
		{
			iTheirDefense *= (100 + collateralDamage());
			iTheirDefense /= 100;
		}

		if (currInterceptionProbability() > 0)
		{
			iTheirDefense *= (100 + currInterceptionProbability());
			iTheirDefense /= 100;
		}
	}
	else
	{
		if (!(pAttacker->immuneToFirstStrikes()))
		{
			iTheirDefense *= 100 + (pDefender->firstStrikes() * 2 + pDefender->chanceFirstStrikes()) * GC.getCOMBAT_DAMAGE() * 2 / 5;
			iTheirDefense /= 100;
		}

		if (pDefender->immuneToFirstStrikes())
		{
			iTheirDefense *= 100 + (pAttacker->firstStrikes() * 2 + pAttacker->chanceFirstStrikes()) * GC.getCOMBAT_DAMAGE() * 2 / 5;
			iTheirDefense /= 100;
		}
	}

	iAssetValue = std::max(1, pDefender->getUnitInfo().getAssetValue());
	iCargoAssetValue = 0;
	pDefender->getCargoUnits(aCargoUnits);
	for (uint i = 0; i < aCargoUnits.size(); ++i)
	{
		iCargoAssetValue += aCargoUnits[i]->getUnitInfo().getAssetValue();
	}
	iTheirDefense = iTheirDefense * iAssetValue / std::max(1, iAssetValue + iCargoAssetValue);

	if (iOurDefense == iTheirDefense)
	{
		if (NO_UNIT == getLeaderUnitType() && NO_UNIT != pDefender->getLeaderUnitType())
			++iOurDefense;
		else if (NO_UNIT != getLeaderUnitType() && NO_UNIT == pDefender->getLeaderUnitType())
			++iTheirDefense;
		else if (isBeforeUnitCycle(*pDefender))
			++iOurDefense;
	}

	return (iOurDefense > iTheirDefense);
// advc (comment): End of legacy BtS code
}


int CvUnit::airMaxCombatStr(const CvUnit* pOther) const
{
	if (airBaseCombatStr() == 0)
		return 0;

	int iModifier = getExtraCombatPercent();

	if (getKamikazePercent() != 0)
		iModifier += getKamikazePercent();
	/*  BETTER_BTS_AI_MOD, Bugfix, 8/16/08, DanF5771 & jdog5000:
		(ExtraCombatPercent already counted above) */
	/*if (getExtraCombatPercent() != 0)
		iModifier += getExtraCombatPercent();*/ // BtS
	if (pOther != NULL)
	{
		if (pOther->getUnitCombatType() != NO_UNITCOMBAT)
			iModifier += unitCombatModifier(pOther->getUnitCombatType());
		iModifier += domainModifier(pOther->getDomainType());
		if (pOther->isAnimal())
		{
			iModifier += animalCombatModifier();
		} // <advc.315c>
		if(pOther->isBarbarian())
			iModifier += barbarianCombatModifier(); // </advc.315c>
	}
	int iCombat;
	if (iModifier > 0)
		iCombat = (airBaseCombatStr() * (iModifier + 100));
	else iCombat = ((airBaseCombatStr() * 10000) / (100 - iModifier));

	return std::max(1, iCombat);
}


float CvUnit::airMaxCombatStrFloat(const CvUnit* pOther) const
{
	return (((float)(airMaxCombatStr(pOther))) / 100.0f);
}


float CvUnit::airCurrCombatStrFloat(const CvUnit* pOther) const
{
	return (((float)(airCurrCombatStr(pOther))) / 100.0f);
}


// doc
int CvUnit::combatLimitAgainst(const CvUnit* pUnit) const
{
	int iCombatLimit = combatLimit();

    // doc: combat limit determined by city defense modifier
	if (iCombatLimit < 100)
	{
	    if (pUnit != NULL && pUnit->plot()->isCity())
	    {
	        int iCityDefense = std::max(0, 100 - pUnit->plot()->getPlotCity()->getDefenseModifier(ignoreBuildingDefense()));
	        iCombatLimit = std::min(iCombatLimit, iCityDefense);
	    }
	}

	return iCombatLimit;
}


bool CvUnit::canAirDefend(CvPlot const* pPlot) const
{
	if (pPlot == NULL)
		pPlot = plot();

	// SuperSpies (TSHEEP): no spy air defense
	if (isSpy())
	    return false;

	if (maxInterceptionProbability() == 0)
		return false;

	if (getDomainType() != DOMAIN_AIR)
	{
		//if (!pPlot->isValidDomainForLocation(*this) ||
		if (!isRevealedValidDomain(*pPlot) || // advc
			/*  UNOFFICIAL_PATCH, Bugfix, 10/30/09, Mongoose & jdog5000
			Land units which are cargo cannot intercept (from Mongoose SDK) */
			isCargo())
		{
			return false;
		}
	}

	return true;
}


int CvUnit::airCombatDamage(const CvUnit* pDefender) const
{
	int iOurStrength = airCurrCombatStr(pDefender);
	FAssertMsg(iOurStrength > 0, "Air combat strength is expected to be greater than zero");
	int iTheirStrength = pDefender->maxCombatStr(plot(), this);

	int iStrengthFactor = (iOurStrength + iTheirStrength + 1) / 2;

	int iDamage = std::max(1, ((GC.getDefineINT(CvGlobals::AIR_COMBAT_DAMAGE) *
		(iOurStrength + iStrengthFactor)) / (iTheirStrength + iStrengthFactor)));

	CvCity const* pCity = getPlot().getPlotCity();
	if (pCity != NULL)
	{
		iDamage *= std::max(0, (pCity->getAirModifier() + 100));
		iDamage /= 100;
	}

	return iDamage;
}


int CvUnit::rangeCombatDamage(const CvUnit* pDefender) const
{
	int iOurStrength = airCurrCombatStr(pDefender);
	FAssertMsg(iOurStrength > 0, "Combat strength is expected to be greater than zero");
	int iTheirStrength = pDefender->maxCombatStr(plot(), this);

	int iStrengthFactor = (iOurStrength + iTheirStrength + 1) / 2;
	static int const iRANGE_COMBAT_DAMAGE = GC.getDefineINT("RANGE_COMBAT_DAMAGE"); // advc.opt
	int iDamage = std::max(1, ((iRANGE_COMBAT_DAMAGE * (iOurStrength + iStrengthFactor)) /
			(iTheirStrength + iStrengthFactor)));

	return iDamage;
}


CvUnit* CvUnit::bestInterceptor(CvPlot const& kPlot,
	bool bOdds) const // advc.004c
{
	/*	advc: (Could do this through a plot range, or at least go through
		selection groups before individual units. But seems to be a nonissue.) */
	PROFILE_FUNC();
	TeamTypes const eOurTeam = getTeam(); // advc.004c
	CvUnit* pBestUnit = NULL;
	int iBestValue = 0;
	for (PlayerIter<ALIVE,ENEMY_OF> it(getTeam()); it.hasNext(); ++it)
	{
		CvPlayer const& kEnemy = *it;
		if (isInvisible(kEnemy.getTeam(), false, false))
			continue;
		FOR_EACH_UNIT_VAR(pLoopUnit, kEnemy)
		{	// <advc.004c>
			if (bOdds && !pLoopUnit->getPlot().isVisible(eOurTeam))
				continue; // </advc.004c>
			if (pLoopUnit->canAirDefend() &&
				!pLoopUnit->isMadeInterception() &&
				(pLoopUnit->getDomainType() != DOMAIN_AIR || !pLoopUnit->hasMoved()) &&
				(pLoopUnit->getDomainType() != DOMAIN_AIR ||
				pLoopUnit->getGroup()->getActivityType() == ACTIVITY_INTERCEPT) &&
				plotDistance(pLoopUnit->plot(), &kPlot) <= pLoopUnit->airRange())
			{
				int iValue = pLoopUnit->currInterceptionProbability();
				if (iValue > iBestValue)
				{
					iBestValue = iValue;
					pBestUnit = pLoopUnit;
				}
			}
		}
	}
	return pBestUnit;
}


CvUnit* CvUnit::bestSeaPillageInterceptor(CvUnit* pPillager, int iMinOdds) const
{
	CvUnit* pBestUnit = NULL;
	int iBestUnitRank = -1; // BETTER_BTS_AI_MOD, Lead From Behind (UncutDragon), 02/21/10, jdog5000
	for (SquareIter it(*pPillager, GC.getMAX_SEA_PATROL_RANGE(), false);
		it.hasNext(); ++it)
	{
		CvPlot const& kLoopPlot = *it;
		FOR_EACH_UNIT_VAR_IN(pLoopUnit, kLoopPlot)
		{
			if (pLoopUnit == NULL)
			{
				FAssertMsg(pLoopUnit != NULL, "Can this happen?"); // advc.test
				continue;
			}
			// <advc>
			if (pLoopUnit->isSeaPatrolling() &&
				pLoopUnit->canSeaPatrol(pLoopUnit->plot()) && // <advc>
				pLoopUnit->canReachBySeaPatrol(getPlot()) && // advc.004k
				// advc.028: Allow submarines to patrol. What could go wrong?
				//!pLoopUnit->isInvisible(getTeam(), false) &&
				isEnemy(pLoopUnit->getTeam()))
			{
				if (pBestUnit == NULL || pLoopUnit->isBetterDefenderThan(pBestUnit, this,
					// BETTER_BTS_AI_MOD, Lead From Behind (UncutDragon), 02/21/10, jdog5000:
					&iBestUnitRank))
				{
					if (calculateCombatOdds(*pPillager, *pLoopUnit) < iMinOdds)
						pBestUnit = pLoopUnit;
				}
			}
		}
	}
	return pBestUnit;
}


bool CvUnit::isAutomated() const
{
	return getGroup()->isAutomated();
}


bool CvUnit::isWaiting() const
{
	return getGroup()->isWaiting();
}


bool CvUnit::isFortifyable() const
{
	return (canFight() && !noDefensiveBonus() &&
		(getDomainType() == DOMAIN_LAND || getDomainType() == DOMAIN_IMMOBILE));
}


int CvUnit::fortifyModifier() const
{
	if (!isFortifyable())
		return 0;
	static int const iFORTIFY_MODIFIER_PER_TURN = GC.getDefineINT("FORTIFY_MODIFIER_PER_TURN");
	// doc: recently born civilizations fortify immediately in their territory
	if (plot()->getBirthProtected() == getOwner() && getFortifyTurns() > 0)
    {
        static int const iMAX_FORTIFY_TURNS = GC.getDefineINT("MAX_FORTIFY_TURNS");
	    return iMAX_FORTIFY_TURNS * iFORTIFY_MODIFIER_PER_TURN;
    }
	return (getFortifyTurns() * iFORTIFY_MODIFIER_PER_TURN);
}


int CvUnit::experienceNeeded() const
{
	{
		int iR = GC.getPythonCaller()->experienceNeeded(*this);
		if (iR >= 0)
			return iR;
	}
	/*	K-Mod. C version of the original python code.
		Note: python rounds towards negative infinity, but C++ rounds towards 0.
		So the code needs to be slightly different to achieve the same effect. */
	int iExperienceNeeded = SQR(getLevel()) + 1;
	int iModifier = GET_PLAYER(getOwner()).getLevelExperienceModifier();
	if (iModifier != 0)
		iExperienceNeeded = (iExperienceNeeded * (100 + iModifier) + 99) / 100;
	return iExperienceNeeded;
	// K-Mod end
}


int CvUnit::attackXPValue() const
{
	return m_pUnitInfo->getXPValueAttack()
			- (isBarbarian() && !isAnimal() ? 1 : 0); // advc.312
}


int CvUnit::defenseXPValue() const
{
	return m_pUnitInfo->getXPValueDefense();
}


int CvUnit::maxXPValue() const
{
	int iMaxValue = MAX_INT;
	if (isAnimal())
		iMaxValue = std::min(iMaxValue, GC.getDefineINT("ANIMAL_MAX_XP_VALUE"));
	if (isBarbarian())
		iMaxValue = std::min(iMaxValue, GC.getDefineINT("BARBARIAN_MAX_XP_VALUE"));
	return iMaxValue;
}


bool CvUnit::isRanged() const
{
	for (int i = 0; i < m_pUnitInfo->getGroupDefinitions(); i++)
	{
		if (!getArtInfo(i, GET_PLAYER(getOwner()).getCurrentEra())->getActAsRanged())
			return false;
	}
	return true;
}


bool CvUnit::immuneToFirstStrikes() const
{
	return (m_pUnitInfo->isFirstStrikeImmune() || getImmuneToFirstStrikesCount() > 0);
}


bool CvUnit::isNeverInvisible() const
{
	return (!alwaysInvisible() && getInvisibleType() == NO_INVISIBLE);
}


bool CvUnit::isInvisible(TeamTypes eTeam, bool bDebug, bool bCheckCargo) const
{
	if (bDebug && GC.getGame().isDebugMode())
		return false;
	if (getTeam() == eTeam)
		return false;
	if (alwaysInvisible())
		return true;
	if (bCheckCargo && isCargo())
		return true;
	if (getInvisibleType() == NO_INVISIBLE)
		return false;
	return !getPlot().isInvisibleVisible(eTeam, getInvisibleType());
}


int CvUnit::maxInterceptionProbability() const
{
	return std::max(0, m_pUnitInfo->getInterceptionProbability() + getExtraIntercept());
}


int CvUnit::currInterceptionProbability() const
{
	if (getDomainType() != DOMAIN_AIR)
	    return maxInterceptionProbability();

	int iInterceptProbability = maxInterceptionProbability();

	// doc: Iron Dome effect
	if (GET_PLAYER(getOwner()).isHasBuildingEffect(IRON_DOME))
	{
	    if (plot()->getOwner() == getOwner())
	    {
	        iInterceptProbability *= 3;
	        iInterceptProbability /= 2;
	    }
	}

	return (iInterceptProbability * currHitPoints()) / maxHitPoints();
}


int CvUnit::withdrawalProbability() const
{
	if (getDomainType() == DOMAIN_LAND && getPlot().isWater() && !isAmphib()) // doc: amphibious promotion
		return 0;
	return std::max(0, m_pUnitInfo->getWithdrawalProbability() + getExtraWithdrawal());
}


int CvUnit::animalCombatModifier() const
{
	return m_pUnitInfo->getAnimalCombatModifier();
}

// <advc.315c>
int CvUnit::barbarianCombatModifier() const
{
	return m_pUnitInfo->getBarbarianCombatModifier();
} // </advc.315c>


int CvUnit::hillsAttackModifier() const
{
	return (m_pUnitInfo->getHillsAttackModifier() + getExtraHillsAttackPercent());
}


int CvUnit::hillsDefenseModifier() const
{
	return (m_pUnitInfo->getHillsDefenseModifier() + getExtraHillsDefensePercent());
}


// doc
int CvUnit::plainsAttackModifier() const
{
	return m_pUnitInfo->getPlainsAttackModifier() + getExtraPlainsAttackPercent();
}


// doc
int CvUnit::plainsDefenseModifier() const
{
	return m_pUnitInfo->getPlainsDefenseModifier() + getExtraPlainsDefensePercent();
}


// doc
int CvUnit::riverAttackModifier() const
{
	return getExtraRiverAttackPercent();
}


int CvUnit::terrainAttackModifier(TerrainTypes eTerrain) const
{
	FAssertMsg(eTerrain >= 0, "eTerrain is expected to be non-negative (invalid Index)");
	FAssertMsg(eTerrain < GC.getNumTerrainInfos(), "eTerrain is expected to be within maximum bounds (invalid Index)");
	return (m_pUnitInfo->getTerrainAttackModifier(eTerrain) + getExtraTerrainAttackPercent(eTerrain));
}


int CvUnit::terrainDefenseModifier(TerrainTypes eTerrain) const
{
	FAssertMsg(eTerrain >= 0, "eTerrain is expected to be non-negative (invalid Index)");
	FAssertMsg(eTerrain < GC.getNumTerrainInfos(), "eTerrain is expected to be within maximum bounds (invalid Index)");
	return (m_pUnitInfo->getTerrainDefenseModifier(eTerrain) + getExtraTerrainDefensePercent(eTerrain));
}


int CvUnit::featureAttackModifier(FeatureTypes eFeature) const
{
	FAssertMsg(eFeature >= 0, "eFeature is expected to be non-negative (invalid Index)");
	FAssertMsg(eFeature < GC.getNumFeatureInfos(), "eFeature is expected to be within maximum bounds (invalid Index)");
	return (m_pUnitInfo->getFeatureAttackModifier(eFeature) + getExtraFeatureAttackPercent(eFeature));
}

int CvUnit::featureDefenseModifier(FeatureTypes eFeature) const
{
	FAssertMsg(eFeature >= 0, "eFeature is expected to be non-negative (invalid Index)");
	FAssertMsg(eFeature < GC.getNumFeatureInfos(), "eFeature is expected to be within maximum bounds (invalid Index)");
	return (m_pUnitInfo->getFeatureDefenseModifier(eFeature) + getExtraFeatureDefensePercent(eFeature));
}

int CvUnit::unitClassAttackModifier(UnitClassTypes eUnitClass) const
{
	FAssertMsg(eUnitClass >= 0, "eUnitClass is expected to be non-negative (invalid Index)");
	FAssertMsg(eUnitClass < GC.getNumUnitClassInfos(), "eUnitClass is expected to be within maximum bounds (invalid Index)");
	return m_pUnitInfo->getUnitClassAttackModifier(eUnitClass);
}


int CvUnit::unitClassDefenseModifier(UnitClassTypes eUnitClass) const
{
	FAssertMsg(eUnitClass >= 0, "eUnitClass is expected to be non-negative (invalid Index)");
	FAssertMsg(eUnitClass < GC.getNumUnitClassInfos(), "eUnitClass is expected to be within maximum bounds (invalid Index)");
	return m_pUnitInfo->getUnitClassDefenseModifier(eUnitClass);
}


int CvUnit::unitCombatModifier(UnitCombatTypes eUnitCombat) const
{
	FAssertMsg(eUnitCombat >= 0, "eUnitCombat is expected to be non-negative (invalid Index)");
	FAssertMsg(eUnitCombat < GC.getNumUnitCombatInfos(), "eUnitCombat is expected to be within maximum bounds (invalid Index)");
	return (m_pUnitInfo->getUnitCombatModifier(eUnitCombat) + getExtraUnitCombatModifier(eUnitCombat));
}


int CvUnit::domainModifier(DomainTypes eDomain) const
{
	FAssertMsg(eDomain >= 0, "eDomain is expected to be non-negative (invalid Index)");
	FAssertMsg(eDomain < NUM_DOMAIN_TYPES, "eDomain is expected to be within maximum bounds (invalid Index)");
	return (m_pUnitInfo->getDomainModifier(eDomain) + getExtraDomainModifier(eDomain));
}


int CvUnit::bombardRate() const
{
	return (m_pUnitInfo->getBombardRate() + getExtraBombardRate());
}


int CvUnit::airBombBaseRate() const
{
	return m_pUnitInfo->getBombRate();
}


int CvUnit::airBombCurrRate() const
{
	return (airBombBaseRate() * currHitPoints()) / maxHitPoints();
}


SpecialUnitTypes CvUnit::specialCargo() const
{
	return m_pUnitInfo->getSpecialCargo();
}


DomainTypes CvUnit::domainCargo() const
{
	return m_pUnitInfo->getDomainCargo();
}


void CvUnit::changeCargoSpace(int iChange)
{
	if (iChange != 0)
	{
		m_iCargoCapacity += iChange;
		FAssert(m_iCargoCapacity >= 0);
		setInfoBarDirty(true);
	}
}


int CvUnit::cargoSpaceAvailable(SpecialUnitTypes eSpecialCargo, DomainTypes eDomainCargo) const
{
	if (specialCargo() != NO_SPECIALUNIT)
	{
		if (specialCargo() != eSpecialCargo)
			return 0;
	}

	if (domainCargo() != NO_DOMAIN)
	{
		if (domainCargo() != eDomainCargo)
			return 0;
	}

	return std::max(0, cargoSpace() - getCargo());
}

/*	advc.030: Renamed from "canCargoEnterArea" to avoid confusion with canEnterArea
	(wrapper for CvArea::canBeEntered) */
bool CvUnit::canCargoEnterTerritory(TeamTypes eTeam, bool bIgnoreRightOfPassage,
	CvArea const& kArea) const
{
	FAssert(hasCargo()); // advc.opt
	// advc (note): getCargoUnits would be slower
	FOR_EACH_UNIT_IN(pLoopUnit, getPlot())
	{
		if (pLoopUnit->getTransportUnit() == this &&
			!pLoopUnit->canEnterTerritory(eTeam, bIgnoreRightOfPassage, &kArea))
		{
			return false;
		}
	}
	return true;
}


int CvUnit::getUnitAICargo(UnitAITypes eUnitAI) const
{
	int iCount = 0;
	std::vector<CvUnit*> aCargoUnits;
	getCargoUnits(aCargoUnits);
	for (uint i = 0; i < aCargoUnits.size(); ++i)
	{
		if (aCargoUnits[i]->AI_getUnitAIType() == eUnitAI)
			iCount++;
	}
	return iCount;
}

// advc:
CvUnit* CvUnit::fromIDInfo(IDInfo id)
{
	return ::getUnit(id);
}


void CvUnit::setID(int iID)
{
	m_iID = iID;
}


bool CvUnit::isGroupHead() const // XXX is this used???
{
	return (getGroup()->getHeadUnit() == this);
}


CvSelectionGroup* CvUnit::getGroupExternal() const
{
	return GET_PLAYER(getOwner()).getSelectionGroup(getGroupID());
}

// <advc.003s>
// advc.003u (note): Duplicated twice more in CvUnitAI::AI_getGroup
CvSelectionGroup const* CvUnit::getGroup() const
{
	return GET_PLAYER(getOwner()).getSelectionGroup(getGroupID());
}


CvSelectionGroup* CvUnit::getGroup()
{
	return GET_PLAYER(getOwner()).getSelectionGroup(getGroupID());
} // </advc.003s>


bool CvUnit::isBeforeUnitCycle(CvUnit const& kOther) const
{
	FAssert(this != &kOther);

	if (getOwner() != kOther.getOwner())
		return (getOwner() < kOther.getOwner());
	if (getDomainType() != kOther.getDomainType())
		return (getDomainType() < kOther.getDomainType());
	/* if (baseCombatStr() != kOther.baseCombatStr())
		return (baseCombatStr() > kOther.baseCombatStr());*/ // disabled by K-Mod
	if (getUnitType() != kOther.getUnitType())
		return (getUnitType() > kOther.getUnitType());
	if (getLevel() != kOther.getLevel())
		return (getLevel() > kOther.getLevel());
	if (getExperience() != kOther.getExperience())
		return (getExperience() > kOther.getExperience());
	return (getID() < kOther.getID());
}


bool CvUnit::canJoinGroup(const CvPlot* pPlot, CvSelectionGroup const* pSelectionGroup) const
{
	// do not allow someone to join a group that is about to be split apart
	// this prevents a case of a never-ending turn
	if (pSelectionGroup->AI().AI_isForceSeparate())
		return false;

	if (pSelectionGroup->getOwner() == NO_PLAYER)
	{
		CvUnit const* pHeadUnit = pSelectionGroup->getHeadUnit();
		if (pHeadUnit != NULL)
		{
			if (pHeadUnit->getOwner() != getOwner())
				return false;
		}
	}
	else
	{
		if (pSelectionGroup->getOwner() != getOwner())
			return false;
	}

	if (pSelectionGroup->getNumUnits() > 0)
	{
		if (!pSelectionGroup->atPlot(pPlot))
			return false;
		if (pSelectionGroup->getDomainType() != getDomainType())
			return false;
	}

	return true;
}

// K-Mod has edited this function to increase readability and robustness
void CvUnit::joinGroup(CvSelectionGroup* pSelectionGroup, bool bRemoveSelected, bool bRejoin)
{
	CvSelectionGroup* pOldSelectionGroup = GET_PLAYER(getOwner()).getSelectionGroup(getGroupID());

	if (pOldSelectionGroup != NULL && pSelectionGroup == pOldSelectionGroup)
		return; // attempting to join the group we are already in

	CvPlot* pPlot = plot(); // advc (comment): I suppose this could be NULL(?)
	CvSelectionGroup* pNewSelectionGroup = pSelectionGroup;

	if (pNewSelectionGroup == NULL && bRejoin)
	{
		pNewSelectionGroup = GET_PLAYER(getOwner()).addSelectionGroup();
		pNewSelectionGroup->init(pNewSelectionGroup->getID(), getOwner());
	}

	if (pNewSelectionGroup == NULL || canJoinGroup(pPlot, pNewSelectionGroup))
	{
		if (pOldSelectionGroup != NULL)
		{
			bool bWasHead = false;
			if (!isHuman())
			{
				if (pOldSelectionGroup->getNumUnits() > 1)
				{
					if (pOldSelectionGroup->getHeadUnit() == this)
						bWasHead = true;
				}
			}

			pOldSelectionGroup->removeUnit(this);

			// if we were the head, if the head unitAI changed, then force the group to separate (non-humans)
			if (bWasHead)
			{
				FAssert(pOldSelectionGroup->getHeadUnit() != NULL);
				if (pOldSelectionGroup->getHeadUnit()->AI_getUnitAIType() != AI_getUnitAIType())
					pOldSelectionGroup->AI().AI_setForceSeparate();
			}
		}

		if (pNewSelectionGroup != NULL && pNewSelectionGroup->addUnit(this, false))
			m_iGroupID = pNewSelectionGroup->getID();
		else m_iGroupID = FFreeList::INVALID_INDEX;

		if (getGroup() != NULL)
		{
			// K-Mod
			if (isGroupHead())
				GET_PLAYER(getOwner()).updateGroupCycle(*getGroup());
			// K-Mod end
			if (getGroup()->getNumUnits() > 1)
			{
				//getGroup()->setActivityType(ACTIVITY_AWAKE); // BtS
				/*	K-Mod
					For the AI, only wake the group in particular circumstances.
					This is to avoid AI deadlocks where they just keep grouping
					and ungroup indefinitely.
					If the activity type is not changed at all, then that would
					enable exploits such as adding new units to air patrol groups
					to bypass the movement conditions. */
				if (isHuman())
				{
					getGroup()->setAutomateType(NO_AUTOMATE);
					getGroup()->setActivityType(ACTIVITY_AWAKE);
					getGroup()->clearMissionQueue();
					/*	K-Mod note. the mission queue has to be cleared because,
						when the shift key is released, the exe automatically
						sends the autoMission net message.
						(if the mission queue isn't cleared, the units will immediately
						begin their message whenever units are added using shift.) */
				}
				else if (getGroup()->AI().AI_getMissionAIType() == MISSIONAI_GROUP ||
					getLastMoveTurn() == GC.getGame().getTurnSlice())
				{
					getGroup()->setActivityType(ACTIVITY_AWAKE);
				}
				else if (getGroup()->getActivityType() != ACTIVITY_AWAKE)
					getGroup()->setActivityType(ACTIVITY_HOLD); // don't let them cheat.
				// K-Mod end
			}
			//else GET_PLAYER(getOwner()).updateGroupCycle(this); // BtS
		}

		if (isActiveTeam())
		{
			if (pPlot != NULL)
				pPlot->setFlagDirty(true);
		}

		if (pPlot == gDLL->UI().getSelectionPlot())
			gDLL->UI().setDirty(PlotListButtons_DIRTY_BIT, true);
	}

	if (bRemoveSelected && IsSelected())
		gDLL->UI().removeFromSelectionList(this);
}


int CvUnit::getHotKeyNumber()
{
	return m_iHotKeyNumber;
}


void CvUnit::setHotKeyNumber(int iNewValue)
{
	FAssert(getOwner() != NO_PLAYER);

	if (getHotKeyNumber() == iNewValue)
		return;

	if (iNewValue != -1)
	{
		FOR_EACH_UNIT_VAR(pLoopUnit, GET_PLAYER(getOwner()))
		{
			if (pLoopUnit->getHotKeyNumber() == iNewValue)
				pLoopUnit->setHotKeyNumber(-1);
		}
	}

	m_iHotKeyNumber = iNewValue;

	if (IsSelected())
		gDLL->UI().setDirty(InfoPane_DIRTY_BIT, true);
}


void CvUnit::setXY(int iX, int iY, bool bGroup, bool bUpdate, bool bShow, bool bCheckPlotVisible)
{
	// OOS!! Temporary for Out-of-Sync madness debugging...
	/*if (GC.getLogging()) {
		if (gDLL->getChtLvl() > 0) {
			char szOut[1024];
			sprintf(szOut, "Player %d Unit %d (%S's %S) moving from %d:%d to %d:%d\n", getOwner(), getID(), GET_PLAYER(getOwner()).getNameKey(), getName().GetCString(), getX(), getY(), iX, iY);
			gDLL->messageControlLog(szOut);
		}
	}*/
	PROFILE_FUNC(); // advc

	FAssert(!at(iX, iY));
	FAssert(!isFighting());
	FAssert(iX == INVALID_PLOT_COORD || GC.getMap().plot(iX, iY)->getX() == iX);
	FAssert(iY == INVALID_PLOT_COORD || GC.getMap().plot(iX, iY)->getY() == iY);

	/* if (getGroup() != NULL)
		eOldActivityType = getGroup()->getActivityType();
	else eOldActivityType = NO_ACTIVITY;*/

	setBlockading(false);

	/*if (!bGroup || isCargo()) {
		joinGroup(NULL, true);
		bShow = false;
	}*/ // BtS
	// K-Mod. I've adjusted the code to allow cargo units to stay in their groups when possible.
	bShow = bShow && bGroup && !isCargo();
	if (!bGroup)
		joinGroup(0, true);
	// K-Mod end

	CvPlot* pNewPlot = GC.getMap().plot(iX, iY);
	if (pNewPlot != NULL)
	{
		CvUnit* pTransportUnit = getTransportUnit();
		if (pTransportUnit != NULL)
		{
			if (!pTransportUnit->atPlot(pNewPlot))
				setTransportUnit(NULL);
		}

		if (canFight())
		{
			CLinkList<IDInfo> oldUnits;
			for (CLLNode<IDInfo> const* pNode = pNewPlot->headUnitNode(); pNode != NULL;
				pNode = pNewPlot->nextUnitNode(pNode))
			{
				oldUnits.insertAtEnd(pNode->m_data);
			}
			CLLNode<IDInfo>* pUnitNode = oldUnits.head();
			while (pUnitNode != NULL)
			{
				CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
				pUnitNode = oldUnits.next(pUnitNode);
				if (pLoopUnit == NULL)
					continue;
				/*  advc.001, advc.300: Otherwise, a Barbarian city can land
					on top of an animal and trap it. */
				if(pLoopUnit->isAnimal())
				{
					pLoopUnit->kill(false);
					continue;
				}
				CvTeamAI& kUnitTeam = GET_TEAM(pLoopUnit->getTeam()); // advc
				if ((isEnemy(kUnitTeam.getID(), *pNewPlot) ||
					pLoopUnit->isEnemy(getTeam())) &&
					!pLoopUnit->canCoexistWithEnemyUnit(getTeam()))
				{
					if (pLoopUnit->getUnitInfo().getUnitCaptureClassType() == NO_UNITCLASS &&
						pLoopUnit->canDefendAgainst(this, pNewPlot)) // doc
					{
						pLoopUnit->jumpToNearestValidPlot(); // can kill unit
					}
					else
					{
						if (!m_pUnitInfo->isHiddenNationality() &&
							!pLoopUnit->getUnitInfo().isHiddenNationality())
						{
							kUnitTeam.changeWarWeariness(getTeam(),
									*pNewPlot, GC.getDefineINT("WW_UNIT_CAPTURED"));
							GET_TEAM(getTeam()).changeWarWeariness(pLoopUnit->getTeam(),
									*pNewPlot, GC.getDefineINT("WW_CAPTURED_UNIT"));
							GET_TEAM(getTeam()).AI_changeWarSuccess(pLoopUnit->getTeam(),
									GC.getDefineINT("WAR_SUCCESS_UNIT_CAPTURING"));
						}
						if (//!isNoUnitCapture()
							SyncRandSuccess100(getCaptureOdds(*pLoopUnit))) // advc.010
						{
							pLoopUnit->setCapturingPlayer(getOwner());
						}
						// advc.010: Report death
						else addAttackSuccessMessages(*pLoopUnit, false);
						pLoopUnit->kill(false, getOwner());
					}
				}
			}
		}

		if (pNewPlot->isGoody(getTeam()))
			GET_PLAYER(getOwner()).doGoody(pNewPlot, this);
	}

	CvPlot* pOldPlot = plot();
	if (pOldPlot != NULL)
	{
		pOldPlot->removeUnit(this, bUpdate && !hasCargo());
		pOldPlot->changeAdjacentSight(getTeam(), visibilityRange(), false, this, true);
		pOldPlot->getArea().changeUnitsPerPlayer(getOwner(), -1);
		pOldPlot->getArea().changePower(getOwner(), -m_pUnitInfo->getPowerValue());

		if (AI_getUnitAIType() != NO_UNITAI)
			pOldPlot->getArea().changeNumAIUnits(getOwner(), AI_getUnitAIType(), -1);

		/*if (isAnimal()) // advc: No longer tracked
			pOldPlot->getArea().changeAnimalsPerPlayer(getOwner(), -1);*/

		if (pOldPlot->getTeam() != getTeam() && (pOldPlot->getTeam() == NO_TEAM ||
			!GET_TEAM(pOldPlot->getTeam()).isVassal(getTeam())))
		{
			GET_PLAYER(getOwner()).changeNumOutsideUnits(-1);
		}

		setLastMoveTurn(GC.getGame().getTurnSlice());

		CvCity* pOldCity = pOldPlot->getPlotCity();
		if (pOldCity != NULL)
		{
			if (isMilitaryHappiness() && pOldCity->getOwner() == getOwner()) // doc: military happiness only from same player
				pOldCity->changeMilitaryHappinessUnits(-1);
		}
		{
			CvCity* pWorkingCity = pOldPlot->getWorkingCity();
			if (pWorkingCity != NULL)
			{
				if (canSiege(pWorkingCity->getTeam()))
					pWorkingCity->AI_setAssignWorkDirty(true);
			}
		}
		if (pOldPlot->isWater())
		{
			FOR_EACH_ADJ_PLOT(*pOldPlot)
			{
				if (!pAdj->isWater())
					continue;
				CvCity* pWorkingCity = pAdj->getWorkingCity();
				if (pWorkingCity != NULL && canSiege(pWorkingCity->getTeam()))
					pWorkingCity->AI_setAssignWorkDirty(true);
			}
		}

		if (pOldPlot->isActiveVisible(true))
			pOldPlot->updateMinimapColor();

		if (pOldPlot == gDLL->UI().getSelectionPlot())
		{
			gDLL->UI().verifyPlotListColumn();
			gDLL->UI().setDirty(PlotListButtons_DIRTY_BIT, true);
		}
	}

	if (pNewPlot != NULL)
	{
		m_iX = pNewPlot->getX();
		m_iY = pNewPlot->getY();
	}
	else
	{
		m_iX = INVALID_PLOT_COORD;
		m_iY = INVALID_PLOT_COORD;
	}
	updatePlot(); // advc.opt

	FAssert(atPlot(pNewPlot));

	if (pNewPlot != NULL)
	{
		CvCity* pNewCity = pNewPlot->getPlotCity();
		if (pNewCity != NULL)
		{
			if (isEnemy(pNewCity->getTeam()) &&
				!canCoexistWithEnemyUnit(pNewCity->getTeam()) && canFight())
			{
				GET_TEAM(getTeam()).changeWarWeariness(pNewCity->getTeam(), *pNewPlot,
						GC.getDefineINT("WW_CAPTURED_CITY"));
				/*GET_TEAM(getTeam()).AI_changeWarSuccess(pNewCity->getTeam(), GC.getDefineINT("WAR_SUCCESS_CITY_CAPTURING"));*/ // BtS
				// BETTER_BTS_AI_MOD, General AI, 06/14/09, jdog5000
				// Double war success if capturing capital city, always a significant blow to enemy
				// pNewCity still points to old city here, hasn't been acquired yet
				/*  advc.123d: Make it only +150% for capital. (Tbd.: Check if
					it's the original capital - but how to check?) */
				GET_TEAM(getTeam()).AI_changeWarSuccess(pNewCity->getTeam(),
						(pNewCity->isCapital() ? 3 : 2) *
						scaled(GC.getWAR_SUCCESS_CITY_CAPTURING(), 2));

				PlayerTypes eNewOwner = GET_PLAYER(getOwner()).pickConqueredCityOwner(*pNewCity);
				if (eNewOwner != NO_PLAYER)
				{
					GET_PLAYER(eNewOwner).acquireCity(pNewCity, true, false, true);
					pNewCity = NULL; // (deleted by acquireCity)
				}
			}
		}
		//update facing direction
		if (pOldPlot != NULL)
		{
			DirectionTypes newDirection = estimateDirection(pOldPlot, pNewPlot);
			if(newDirection != NO_DIRECTION)
				m_eFacingDirection = newDirection;
		}
		//update cargo mission animations
		/*if (isCargo()) {
			if (eOldActivityType != ACTIVITY_MISSION)
				getGroup()->setActivityType(eOldActivityType);
		} */ // BtS - disabled by K-Mod (obsolete)

		setFortifyTurns(0);
		// needs to be here so that the square is considered visible when we move into it...
		pNewPlot->changeAdjacentSight(getTeam(), visibilityRange(), true, this, true);

		pNewPlot->addUnit(*this, bUpdate && !hasCargo());

		pNewPlot->getArea().changeUnitsPerPlayer(getOwner(), 1);
		pNewPlot->getArea().changePower(getOwner(), m_pUnitInfo->getPowerValue());

		if (AI_getUnitAIType() != NO_UNITAI)
			pNewPlot->getArea().changeNumAIUnits(getOwner(), AI_getUnitAIType(), 1);
		/*if (isAnimal()) // advc: No longer tracked
			pNewPlot->getArea().changeAnimalsPerPlayer(getOwner(), 1);*/
		if (pNewPlot->getTeam() != getTeam() && (pNewPlot->getTeam() == NO_TEAM ||
			!GET_TEAM(pNewPlot->getTeam()).isVassal(getTeam())))
		{
			GET_PLAYER(getOwner()).changeNumOutsideUnits(1);
		}
		if (shouldLoadOnMove(pNewPlot))
			load();

		if (!alwaysInvisible() && !m_pUnitInfo->isHiddenNationality()) // K-Mod
		{
			for (TeamIter<CIV_ALIVE> itContact; itContact.hasNext(); ++itContact)
			{
				if (!isInvisible(itContact->getID(), false) &&
					pNewPlot->isVisible(itContact->getID()))
				{
					FirstContactData fcData(pNewPlot, NULL, this); // advc.071
					itContact->meet(getTeam(), true, /* advc.071: */ &fcData);
				}
			}
		}
		pNewCity = pNewPlot->getPlotCity();
		if (pNewCity != NULL)
		{
			if (isMilitaryHappiness() && pNewCity->getOwner() == getOwner()) // doc: military happiness only for same owner
				pNewCity->changeMilitaryHappinessUnits(1);
			  // <advc.001b>
			if (GC.getDefineBOOL(CvGlobals::CAN_TRAIN_CHECKS_AIR_UNIT_CAP) &&
				m_pUnitInfo->getAirUnitCap() > 0 && pNewCity->getOwner() == getOwner())
			{
				pNewCity->verifyProduction();
			} // </advc.001b>
		}
		{
			CvCity* pWorkingCity = pNewPlot->getWorkingCity();
			if (pWorkingCity != NULL)
			{
				if (canSiege(pWorkingCity->getTeam()))
				{
					pWorkingCity->verifyWorkingPlot(
							pWorkingCity->getCityPlotIndex(*pNewPlot));
				}
			}
		}
		/*if (pNewPlot->isWater()) {
			FOR_EACH_ADJ_PLOT(*pNewPlot) {
				if (pAdj->isWater()) {
					pWorkingCity = pAdj->getWorkingCity();
					if (pWorkingCity != NULL && canSiege(pWorkingCity->getTeam()))
								pWorkingCity->verifyWorkingPlot(pWorkingCity->getCityPlotIndex(*pAdj));
		} } }*/ // BtS
		// disabled by K-Mod. The game mechanics that this was meant to handle are no longer used. (Nothing to do with K-Mod.)

		if (pNewPlot->isActiveVisible(true))
			pNewPlot->updateMinimapColor();

		if (GC.IsGraphicsInitialized())
		{
			//override bShow if check plot visible
			if(bCheckPlotVisible && pNewPlot->isVisibleToWatchingHuman())
				bShow = true;

			if (bShow)
				QueueMove(pNewPlot);
			else SetPosition(pNewPlot);
		}

		if (pNewPlot == gDLL->UI().getSelectionPlot())
		{
			gDLL->UI().verifyPlotListColumn();
			gDLL->UI().setDirty(PlotListButtons_DIRTY_BIT, true);
		}
	}

	if (pOldPlot != NULL)
	{
		if (hasCargo())
		{
			std::vector<IDInfo> aCargoGroups; // K-Mod (advc: was vector<pair<>>)
			{
				FOR_EACH_UNIT_VAR_IN(pLoopUnit, *pOldPlot)
				{
					if (pLoopUnit->getTransportUnit() == this)
					{
						pLoopUnit->setXY(iX, iY, bGroup, false);
						aCargoGroups.push_back(pLoopUnit->getGroup()->getIDInfo()); // K-Mod
					}
				}
			}
			// K-Mod
			/*	If the group of the cargo units we just moved includes units that are
				not transported by this transport group, then we need to separate them. */

			// first remove duplicate group numbers
			std::sort(aCargoGroups.begin(), aCargoGroups.end());
			aCargoGroups.erase(std::unique(aCargoGroups.begin(), aCargoGroups.end()),
					aCargoGroups.end());

			// now check the units in each group
			for (size_t i = 0; i < aCargoGroups.size(); i++)
			{
				CvSelectionGroup& kCargoGroup = *GET_PLAYER(aCargoGroups[i].eOwner).
						getSelectionGroup(aCargoGroups[i].iID);
				ActivityTypes eOldActivityType = kCargoGroup.getActivityType();
				FOR_EACH_UNIT_VAR_IN(pLoopUnit, kCargoGroup)
				{
					if (pLoopUnit->getTransportUnit() == NULL ||
						pLoopUnit->getTransportUnit()->getGroup() != getGroup())
					{
						pLoopUnit->joinGroup(NULL, true);
						if (eOldActivityType != ACTIVITY_MISSION)
							pLoopUnit->getGroup()->setActivityType(eOldActivityType);
					}
					// while we're here, update the air-circling animation for fighter-planes.
					else if (eOldActivityType == ACTIVITY_INTERCEPT)
						pLoopUnit->airCircle(true);
				}
			}
			// K-Mod end
		}
	}

	if (bUpdate && hasCargo())
	{
		if (pOldPlot != NULL)
		{
			pOldPlot->updateCenterUnit();
			pOldPlot->setFlagDirty(true);
		}

		if (pNewPlot != NULL)
		{
			pNewPlot->updateCenterUnit();
			pNewPlot->setFlagDirty(true);
		}
	}

	FAssert(pOldPlot != pNewPlot);
	//GET_PLAYER(getOwner()).updateGroupCycle(this);
	// K-Mod. Only update the group cycle here if we are placing this unit on the map for the first time.
	if (!pOldPlot)
		GET_PLAYER(getOwner()).updateGroupCycle(*getGroup());
	// K-Mod end

	setInfoBarDirty(true);

	if (IsSelected())
	{
		if (isFound())
		{
			gDLL->UI().setDirty(GlobeLayer_DIRTY_BIT, true);
			gDLL->getEngineIFace()->updateFoundingBorder();
			// advc.004h (comment): No need to call CvUnit::updateFoundingBorder here
		}

		gDLL->UI().setDirty(ColoredPlots_DIRTY_BIT, true);
	}
	//update glow
	if (pNewPlot != NULL)
		gDLL->getEntityIFace()->updateEnemyGlow(getEntity());

	// report event to Python, along with some other key state
	CvEventReporter::getInstance().unitSetXY(pNewPlot, this);
}

// advc.opt: Update cached CvPlot and CvArea pointer
void CvUnit::updatePlot()
{
	m_pPlot = GC.getMap().plotSoren(getX(), getY());
	updateArea();
}


/*int CvUnit::getArea() const
{
	return plot()->getArea().getID();
}*/
// advc:
void CvUnit::updateArea()
{
	CvPlot* pPlot = plot();
	if (pPlot == NULL) // Unit dying or areas being recalculated
		m_pArea = NULL;
	else m_pArea = pPlot->area();
}


int CvUnit::getLastMoveTurn() const
{
	return m_iLastMoveTurn;
}


void CvUnit::setLastMoveTurn(int iNewValue)
{
	m_iLastMoveTurn = iNewValue;
	FAssert(getLastMoveTurn() >= 0);
}


CvPlot* CvUnit::getReconPlot() const
{
	return GC.getMap().plotSoren(m_iReconX, m_iReconY);
}


void CvUnit::setReconPlot(CvPlot* pNewValue)
{
	CvPlot* pOldPlot = getReconPlot();
	if (pOldPlot != pNewValue)
	{
		if (pOldPlot != NULL)
		{
			pOldPlot->changeAdjacentSight(getTeam(), GC.getDefineINT(CvGlobals::RECON_VISIBILITY_RANGE), false, this, true);
			pOldPlot->changeReconCount(-1); // changeAdjacentSight() tests for getReconCount()
		}

		if (pNewValue == NULL)
		{
			m_iReconX = INVALID_PLOT_COORD;
			m_iReconY = INVALID_PLOT_COORD;
		}
		else
		{
			m_iReconX = pNewValue->getX();
			m_iReconY = pNewValue->getY();

			pNewValue->changeReconCount(1); // changeAdjacentSight() tests for getReconCount()
			pNewValue->changeAdjacentSight(getTeam(), GC.getDefineINT(CvGlobals::RECON_VISIBILITY_RANGE), true, this, true);
			m_iLastReconTurn = GC.getGame().getGameTurn(); // advc.029
		}
	}
}


void CvUnit::setGameTurnCreated(int iNewValue)
{
	m_iGameTurnCreated = iNewValue;
	FAssert(getGameTurnCreated() >= 0);
}


void CvUnit::setDamage(int iNewValue, PlayerTypes ePlayer, bool bNotifyEntity)
{
	int iOldValue = getDamage();
	m_iDamage = range(iNewValue, 0, maxHitPoints());

	FAssertMsg(currHitPoints() >= 0, "currHitPoints() is expected to be non-negative (invalid Index)");

	if (iOldValue != getDamage())
	{
		if (GC.getGame().isFinalInitialized() && bNotifyEntity)
			NotifyEntity(MISSION_DAMAGE);

		setInfoBarDirty(true);

		if (IsSelected())
			gDLL->UI().setDirty(InfoPane_DIRTY_BIT, true);

		if (plot() == gDLL->UI().getSelectionPlot())
			gDLL->UI().setDirty(PlotListButtons_DIRTY_BIT, true);
	}

	if (isDead())
		kill(true, ePlayer);
}


void CvUnit::changeDamage(int iChange, PlayerTypes ePlayer)
{
	setDamage((getDamage() + iChange), ePlayer);
}


void CvUnit::setMoves(int iNewValue)
{
	if(getMoves() == iNewValue)
		return;

	m_iMoves = iNewValue;
	FAssert(getMoves() >= 0);

	CvPlot* pPlot = plot();
	if (isActiveTeam())
	{
		if (pPlot != NULL)
			pPlot->setFlagDirty(true);
	}

	if (IsSelected())
	{
		gDLL->getFAStarIFace()->ForceReset(&GC.getInterfacePathFinder());
		gDLL->UI().setDirty(InfoPane_DIRTY_BIT, true);
	}

	if (pPlot == gDLL->UI().getSelectionPlot())
		gDLL->UI().setDirty(PlotListButtons_DIRTY_BIT, true);
}


void CvUnit::changeMoves(int iChange)
{
	setMoves(getMoves() + iChange);
}


void CvUnit::finishMoves()
{
	setMoves(maxMoves());
}


void CvUnit::setExperience(int iNewValue, int iMax)
{
	if ((getExperience() != iNewValue) && (getExperience() < ((iMax == -1) ? MAX_INT : iMax)))
	{
		m_iExperience = std::min(((iMax == -1) ? MAX_INT : iMax), iNewValue);
		FAssert(getExperience() >= 0);
		if (IsSelected())
			gDLL->UI().setDirty(InfoPane_DIRTY_BIT, true);
	}
}

void CvUnit::changeExperience(int iChange, int iMax, bool bFromCombat, bool bInBorders,
	int iGlobalPercent) // advc.312: was bUpdateGlobal
{
	int iUnitExperience = iChange;

	// doc: Terracotta Army effect
	if (GET_PLAYER(getOwner()).isHasBuildingEffect(TERRACOTTA_ARMY) && iMax != GC.getDefineINT("ANIMAL_MAX_XP_VALUE"))
    {
		iMax = MAX_INT;
        iGlobalPercent = 100;
    }

	if (bFromCombat)
	{
		CvPlayer& kPlayer = GET_PLAYER(getOwner());
		int iCombatExperienceMod = 100 + kPlayer.getGreatGeneralRateModifier();
		if (bInBorders)
		{
			iCombatExperienceMod += kPlayer.getDomesticGreatGeneralRateModifier() +
					kPlayer.getExpInBorderModifier();
			// advc (comment): ExpInBorderModifier is a currently unused Civic effect
			iUnitExperience += (iChange * kPlayer.getExpInBorderModifier()) / 100;
		}
		//if (bUpdateGlobal)
		kPlayer.changeCombatExperience((iChange * iCombatExperienceMod
				* iGlobalPercent) / SQR( // advc.312
				100));

		if (getExperiencePercent() != 0)
		{
			iUnitExperience *= std::max(0, 100 + getExperiencePercent());
			iUnitExperience /= 100;
		}
	}
	setExperience((getExperience() + iUnitExperience), iMax);
}

// advc.312:
int CvUnit::getGlobalXPPercent() const
{
	if (isAnimal())
		return 0;
	if (isBarbarian())
		return 50;
	return 100;
}


void CvUnit::setLevel(int iNewValue)
{
	if (getLevel() != iNewValue)
	{
		m_iLevel = iNewValue;
		FAssert(getLevel() >= 0);

		if (getLevel() > GET_PLAYER(getOwner()).getHighestUnitLevel())
			GET_PLAYER(getOwner()).setHighestUnitLevel(getLevel());

		// doc: highest naval unit level
		if (getDomainType() == DOMAIN_SEA)
		{
			if (getLevel() > GET_PLAYER(getOwner()).getHighestNavalUnitLevel())
				GET_PLAYER(getOwner()).setHighestNavalUnitLevel(getLevel());
		}

		if (IsSelected())
			gDLL->UI().setDirty(InfoPane_DIRTY_BIT, true);
	}
}

void CvUnit::changeLevel(int iChange)
{
	setLevel(getLevel() + iChange);
}

void CvUnit::changeCargo(int iChange)
{
	m_iCargo += iChange;
	FAssert(getCargo() >= 0);
}

void CvUnit::getCargoUnits(std::vector<CvUnit*>& aUnits) const
{
	aUnits.clear();
	if (hasCargo())
	{
		FOR_EACH_UNIT_VAR_IN(pLoopUnit, getPlot())
		{
			if (pLoopUnit->getTransportUnit() == this)
				aUnits.push_back(pLoopUnit);
		}
	}
	FAssert(getCargo() == aUnits.size());
}

CvPlot* CvUnit::getAttackPlot() const
{
	return GC.getMap().plotSoren(m_iAttackPlotX, m_iAttackPlotY);
}

void CvUnit::setAttackPlot(const CvPlot* pNewValue, bool bAirCombat)
{
	if (getAttackPlot() != pNewValue)
	{
		if (pNewValue != NULL)
		{
			m_iAttackPlotX = pNewValue->getX();
			m_iAttackPlotY = pNewValue->getY();
		}
		else
		{
			m_iAttackPlotX = INVALID_PLOT_COORD;
			m_iAttackPlotY = INVALID_PLOT_COORD;
		}
	}

	m_bAirCombat = bAirCombat;
}

// advc: Renamed from "isAirCombat"
bool CvUnit::isInAirCombat() const
{
	return m_bAirCombat;
}

int CvUnit::getCombatTimer() const
{
	return m_iCombatTimer;
}

void CvUnit::setCombatTimer(int iNewValue)
{
	m_iCombatTimer = iNewValue;
	FAssert(getCombatTimer() >= 0);
}

void CvUnit::changeCombatTimer(int iChange)
{
	setCombatTimer(getCombatTimer() + iChange);
}

int CvUnit::getCombatFirstStrikes() const
{
	return m_iCombatFirstStrikes;
}

void CvUnit::setCombatFirstStrikes(int iNewValue)
{
	m_iCombatFirstStrikes = iNewValue;
	FAssert(getCombatFirstStrikes() >= 0);
}

void CvUnit::changeCombatFirstStrikes(int iChange)
{
	setCombatFirstStrikes(getCombatFirstStrikes() + iChange);
}

int CvUnit::getFortifyTurns() const
{
	return m_iFortifyTurns;
}

void CvUnit::setFortifyTurns(int iNewValue)
{
	iNewValue = range(iNewValue, 0, GC.getDefineINT(CvGlobals::MAX_FORTIFY_TURNS));
	if (iNewValue != getFortifyTurns())
	{
		m_iFortifyTurns = iNewValue;
		setInfoBarDirty(true);
	}
}

void CvUnit::changeFortifyTurns(int iChange)
{
	setFortifyTurns(getFortifyTurns() + iChange);
}

void CvUnit::changeBlitzCount(int iChange)
{
	m_iBlitzCount += iChange;
	// advc.164: Negative values now used for unlimited Blitz
	//FAssert(getBlitzCount() >= 0);
}

void CvUnit::changeAmphibCount(int iChange)
{
	m_iAmphibCount += iChange;
	FAssert(getAmphibCount() >= 0);
}

void CvUnit::changeRiverCount(int iChange)
{
	m_iRiverCount += iChange;
	FAssert(getRiverCount() >= 0);
}

void CvUnit::changeEnemyRouteCount(int iChange)
{
	m_iEnemyRouteCount += iChange;
	FAssert(getEnemyRouteCount() >= 0);
}

// TODO: header conflict
bool CvUnit::isAlwaysHeal() const
{
	// doc: recently spawned can always heal in their territory, or in expansion territory
	return (getAlwaysHealCount() > 0 || getPlot().getBirthProtected() == getOwner() || plot()->isExpansionEffect(getOwner()));
}

void CvUnit::changeAlwaysHealCount(int iChange)
{
	m_iAlwaysHealCount += iChange;
	FAssert(getAlwaysHealCount() >= 0);
}

void CvUnit::changeHillsDoubleMoveCount(int iChange)
{
	m_iHillsDoubleMoveCount += iChange;
	FAssert(getHillsDoubleMoveCount() >= 0);
}

void CvUnit::changeImmuneToFirstStrikesCount(int iChange)
{
	m_iImmuneToFirstStrikesCount += iChange;
	FAssert(getImmuneToFirstStrikesCount() >= 0);
}

// doc
void CvUnit::changeNoUpgradeCount(int iChange)
{
	m_iNoUpgradeCount += iChange;
}

void CvUnit::changeExtraVisibilityRange(int iChange)
{
	if (iChange == 0)
		return;

	getPlot().changeAdjacentSight(getTeam(), visibilityRange(), false, this, true);
	m_iExtraVisibilityRange += iChange;
	FAssert(getExtraVisibilityRange() >= 0);
	getPlot().changeAdjacentSight(getTeam(), visibilityRange(), true, this, true);
}

void CvUnit::changeExtraMoves(int iChange)
{
	m_iExtraMoves += iChange;
	FAssert(getExtraMoves() >= 0 ||
			getExtraMoves() == -1 && isBarbarian()); // advc.905a
}

void CvUnit::changeExtraMoveDiscount(int iChange)
{
	m_iExtraMoveDiscount += iChange;
	FAssert(getExtraMoveDiscount() >= 0);
}

int CvUnit::getExtraAirRange() const
{
	return m_iExtraAirRange;
}

void CvUnit::changeExtraAirRange(int iChange)
{
	m_iExtraAirRange += iChange;
}

int CvUnit::getExtraIntercept() const
{
	return m_iExtraIntercept;
}

void CvUnit::changeExtraIntercept(int iChange)
{
	m_iExtraIntercept += iChange;
}

int CvUnit::getExtraEvasion() const
{
	return m_iExtraEvasion;
}

void CvUnit::changeExtraEvasion(int iChange)
{
	m_iExtraEvasion += iChange;
}

void CvUnit::changeExtraFirstStrikes(int iChange)
{
	m_iExtraFirstStrikes += iChange;
	FAssert(getExtraFirstStrikes() >= 0);
}

void CvUnit::changeExtraChanceFirstStrikes(int iChange)
{
	m_iExtraChanceFirstStrikes += iChange;
	FAssert(getExtraChanceFirstStrikes() >= 0);
}

void CvUnit::changeExtraWithdrawal(int iChange)
{
	m_iExtraWithdrawal += iChange;
	//FAssert(getExtraWithdrawal() >= 0);
	FAssert(withdrawalProbability() >= 0); // K-Mod. (the 'extra' can be negative during sea-patrol battles.)
}

void CvUnit::changeExtraCollateralDamage(int iChange)
{
	m_iExtraCollateralDamage += iChange;
	FAssert(getExtraCollateralDamage() >= 0);
}

void CvUnit::changeExtraBombardRate(int iChange)
{
	m_iExtraBombardRate += iChange;
	FAssert(getExtraBombardRate() >= 0);
}

int CvUnit::getExtraEnemyHeal() const
{
	return m_iExtraEnemyHeal;
}

void CvUnit::changeExtraEnemyHeal(int iChange)
{
	m_iExtraEnemyHeal += iChange;
	FAssert(getExtraEnemyHeal() >= 0);
}

int CvUnit::getExtraNeutralHeal() const
{
	return m_iExtraNeutralHeal;
}

void CvUnit::changeExtraNeutralHeal(int iChange)
{
	m_iExtraNeutralHeal += iChange;
	FAssert(getExtraNeutralHeal() >= 0);
}

int CvUnit::getExtraFriendlyHeal() const
{
	return m_iExtraFriendlyHeal;
}

void CvUnit::changeExtraFriendlyHeal(int iChange)
{
	m_iExtraFriendlyHeal += iChange;
	FAssert(getExtraFriendlyHeal() >= 0);
}

int CvUnit::getSameTileHeal() const
{
	return m_iSameTileHeal;
}

void CvUnit::changeSameTileHeal(int iChange)
{
	m_iSameTileHeal += iChange;
	FAssert(getSameTileHeal() >= 0);
}

int CvUnit::getAdjacentTileHeal() const
{
	return m_iAdjacentTileHeal;
}

void CvUnit::changeAdjacentTileHeal(int iChange)
{
	m_iAdjacentTileHeal += iChange;
	FAssert(getAdjacentTileHeal() >= 0);
}

void CvUnit::changeExtraCombatPercent(int iChange)
{
	if (iChange != 0)
	{
		m_iExtraCombatPercent += iChange;

		setInfoBarDirty(true);
	}
}

void CvUnit::changeExtraCityAttackPercent(int iChange)
{
	if (iChange != 0)
	{
		m_iExtraCityAttackPercent += iChange;
		setInfoBarDirty(true);
	}
}

void CvUnit::changeExtraCityDefensePercent(int iChange)
{
	if (iChange != 0)
	{
		m_iExtraCityDefensePercent += iChange;
		setInfoBarDirty(true);
	}
}

void CvUnit::changeExtraHillsAttackPercent(int iChange)
{
	if (iChange != 0)
	{
		m_iExtraHillsAttackPercent += iChange;
		setInfoBarDirty(true);
	}
}

void CvUnit::changeExtraHillsDefensePercent(int iChange)
{
	if (iChange != 0)
	{
		m_iExtraHillsDefensePercent += iChange;
		setInfoBarDirty(true);
	}
}

// doc
// TODO: header
int CvUnit::getExtraPlainsAttackPercent() const
{
	return m_iExtraPlainsAttackPercent;
}

// doc
void CvUnit::changeExtraPlainsAttackPercent(int iChange)
{
	if (iChange != 0)
	{
		m_iExtraPlainsAttackPercent += iChange;
		setInfoBarDirty(true);
	}
}

// doc
// TODO: header
int CvUnit::getExtraPlainsDefensePercent() const
{
	return m_iExtraPlainsDefensePercent;
}

// doc
void CvUnit::changeExtraPlainsDefensePercent(int iChange)
{
	if (iChange != 0)
	{
		m_iExtraPlainsDefensePercent += iChange;
		setInfoBarDirty(true);
	}
}

// doc
// TODO: header
int CvUnit::getExtraRiverAttackPercent() const
{
	return m_iExtraRiverAttackPercent;
}

// doc
void CvUnit::changeExtraRiverAttackPercent(int iChange)
{
	if (iChange != 0)
	{
		m_iExtraRiverAttackPercent += iChange;
		setInfoBarDirty(true);
	}
}

int CvUnit::getRevoltProtection() const
{
	return m_iRevoltProtection;
}

void CvUnit::changeRevoltProtection(int iChange)
{
	if (iChange != 0)
	{
		m_iRevoltProtection += iChange;
		setInfoBarDirty(true);
	}
}

int CvUnit::getCollateralDamageProtection() const
{
	return m_iCollateralDamageProtection;
}

void CvUnit::changeCollateralDamageProtection(int iChange)
{
	if (iChange != 0)
	{
		m_iCollateralDamageProtection += iChange;
		setInfoBarDirty(true);
	}
}

int CvUnit::getPillageChange() const
{
	return m_iPillageChange;
}

void CvUnit::changePillageChange(int iChange)
{
	if (iChange != 0)
	{
		m_iPillageChange += iChange;
		setInfoBarDirty(true);
	}
}

int CvUnit::getUpgradeDiscount() const
{
	return m_iUpgradeDiscount;
}

void CvUnit::changeUpgradeDiscount(int iChange)
{
	if (iChange != 0)
	{
		m_iUpgradeDiscount += iChange;
		setInfoBarDirty(true);
	}
}

int CvUnit::getExperiencePercent() const
{
	return m_iExperiencePercent;
}

void CvUnit::changeExperiencePercent(int iChange)
{
	if (iChange != 0)
	{
		m_iExperiencePercent += iChange;
		setInfoBarDirty(true);
	}
}

int CvUnit::getKamikazePercent() const
{
	return m_iKamikazePercent;
}

void CvUnit::changeKamikazePercent(int iChange)
{
	if (iChange != 0)
	{
		m_iKamikazePercent += iChange;
		setInfoBarDirty(true);
	}
}

// doc
// TODO: header
int CvUnit::getExtraUpkeep() const
{
	return m_iExtraUpkeep;
}

// doc
void CvUnit::changeExtraUpkeep(int iChange)
{
    if (iChange == 0)
        return;

	if (m_iExtraUpkeep > 0)
	    GET_PLAYER(getOwner()).changeExtraUnitCost(-m_iExtraUpkeep);
	else
	    GET_PLAYER(getOwner()).changeBaseFreeMilitaryUnits(m_iExtraUpkeep);

	m_iExtraUpkeep += iChange;

	if (m_iExtraUpkeep > 0)
	    GET_PLAYER(getOwner()).changeExtraUnitCost(m_iExtraUpkeep);
	else
	    GET_PLAYER(getOwner()).changeBaseFreeMilitaryUnits(-m_iExtraUpkeep);
}

DirectionTypes CvUnit::getFacingDirection(bool bCheckLineOfSightProperty) const
{
	if (bCheckLineOfSightProperty)
	{
		if (m_pUnitInfo->isLineOfSight())
			return m_eFacingDirection; //only look in facing direction
		return NO_DIRECTION; //look in all directions
	}
	return m_eFacingDirection;
}

void CvUnit::setFacingDirection(DirectionTypes eFacingDirection)
{
	if (eFacingDirection != m_eFacingDirection)
	{
		if (m_pUnitInfo->isLineOfSight())
		{
			//remove old fog
			getPlot().changeAdjacentSight(getTeam(), visibilityRange(), false, this, true);

			//change direction
			m_eFacingDirection = eFacingDirection;

			//clear new fog
			getPlot().changeAdjacentSight(getTeam(), visibilityRange(), true, this, true);

			gDLL->UI().setDirty(ColoredPlots_DIRTY_BIT, true);
		}
		else m_eFacingDirection = eFacingDirection;

		//update formation
		NotifyEntity(NO_MISSION);
	}
}

void CvUnit::rotateFacingDirectionClockwise()
{
	//change direction
	DirectionTypes eNewDirection = (DirectionTypes) ((m_eFacingDirection + 1) % NUM_DIRECTION_TYPES);
	setFacingDirection(eNewDirection);
}

void CvUnit::rotateFacingDirectionCounterClockwise()
{
	//change direction
	DirectionTypes eNewDirection = (DirectionTypes) ((m_eFacingDirection + NUM_DIRECTION_TYPES - 1) % NUM_DIRECTION_TYPES);
	setFacingDirection(eNewDirection);
}

int CvUnit::getImmobileTimer() const
{
	return m_iImmobileTimer;
}

void CvUnit::setImmobileTimer(int iNewValue)
{
	if (iNewValue != getImmobileTimer())
	{
		m_iImmobileTimer = iNewValue;
		setInfoBarDirty(true);
	}
}

void CvUnit::changeImmobileTimer(int iChange)
{
	if (iChange != 0)
		setImmobileTimer(std::max(0, getImmobileTimer() + iChange));
}

void CvUnit::setMadeAttack(bool bNewValue)
{
	//m_bMadeAttack = bNewValue;
	// <advc.164>
	if(bNewValue)
		m_iMadeAttacks++;
	else m_iMadeAttacks = 0;
}

bool CvUnit::isMadeAllAttacks() const
{
	return (getBlitzCount() >= 0 && m_iMadeAttacks > getBlitzCount());
} // </advc.164>


void CvUnit::setMadeInterception(bool bNewValue)
{
	m_bMadeInterception = bNewValue;
}

/*  <advc.002e> Lying to the EXE seems to be the only way to stop it from
	showing promotion glow after loading a savegame.
	The EXE also calls isPromotionReady when showing enemy moves. Should be OK
	to show the glow on those only once the human turn starts (in CvPlayer::doWarnings). */
bool CvUnit::isPromotionReadyExternal() const
{
	return isPromotionReady() && BUGOption::isEnabled("PLE__ShowPromotionGlow", false);
} // </advc.002e>


void CvUnit::setPromotionReady(bool bNewValue)
{
	if(isPromotionReady() == bNewValue)
		return;

	m_bPromotionReady = bNewValue;

	if (m_bPromotionReady)
	{
		getGroup()->setAutomateType(NO_AUTOMATE);
		getGroup()->clearMissionQueue();
		getGroup()->setActivityType(ACTIVITY_AWAKE);
	}

	if(BUGOption::isEnabled("PLE__ShowPromotionGlow", false)) // advc.002e:
		gDLL->getEntityIFace()->showPromotionGlow(getEntity(), bNewValue);

	if(IsSelected())
		gDLL->UI().setDirty(SelectionButtons_DIRTY_BIT, true);
}


void CvUnit::testPromotionReady()
{
	setPromotionReady((getExperience() >= experienceNeeded()) && canAcquirePromotionAny());
}


void CvUnit::startDelayedDeath()
{
	m_bDeathDelay = true;
}

// Returns true if killed...
bool CvUnit::doDelayedDeath()
{
	if (m_bDeathDelay && !isFighting())
	{
		kill(false);
		return true;
	}
	return false;
}


bool CvUnit::isCombatFocus() const
{
	return m_bCombatFocus;
}


bool CvUnit::isInfoBarDirty() const
{
	return m_bInfoBarDirty;
}


void CvUnit::setInfoBarDirty(bool bNewValue)
{
	m_bInfoBarDirty = bNewValue;
}


void CvUnit::setBlockading(bool bNewValue)
{
	if (bNewValue != isBlockading())
	{
		m_bBlockading = bNewValue;
		updatePlunder(isBlockading() ? 1 : -1, true);
	}
}


void CvUnit::collectBlockadeGold()
{
	//if(getPlot().getTeam() == getTeam()) return; // advc.033: Handled by caller

	/*  <advc.033> Rewritten based on the new blockadeRange function.
		(This also fixes an issue with gold getting plundered across land.) */
	std::vector<CvPlot*> apRange;
	/*  Path range shortened by 1 b/c this only returns water tiles; adjacent cities
		are going to be one tile farther away. */
	blockadeRange(apRange, -1);
	for(size_t i = 0; i < apRange.size(); i++)
	{
		FOR_EACH_ADJ_PLOT(*apRange[i])
		{
			CvCity* pCity = pAdj->getPlotCity();
			if(pCity == NULL || apRange[i]->getBlockadedCount(pCity->getTeam()) <= 0)
				continue; // </advc.033>
			if(!pCity->isPlundered() && isEnemy(pCity->getTeam()) &&
				!::atWar(pCity->getTeam(), getTeam()))
			{
				int iGold = pCity->calculateTradeProfit(pCity) * pCity->getTradeRoutes();
				if(iGold <= 0)
					continue;
				pCity->setPlundered(true);
				GET_PLAYER(getOwner()).changeGold(iGold);
				GET_PLAYER(pCity->getOwner()).changeGold(-iGold);

                // doc: blockade event
			    CvEventReporter::getInstance().blockade(getOwner(), pCity, iGold);

				CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_TRADE_ROUTE_PLUNDERED",
						getNameKey(), pCity->getNameKey(), iGold);
				gDLL->UI().addMessage(getOwner(), false, -1, szBuffer,
						"AS2D_BUILD_BANK", MESSAGE_TYPE_INFO, getButton(),
						GC.getColorType("GREEN"), getX(), getY());
				szBuffer = gDLL->getText("TXT_KEY_MISC_TRADE_ROUTE_PLUNDER",
						getNameKey(), pCity->getNameKey(), iGold);
				gDLL->UI().addMessage(pCity->getOwner(), false, -1, szBuffer,
						"AS2D_BUILD_BANK", MESSAGE_TYPE_INFO, getButton(),
						GC.getColorType("RED"), pCity->getX(), pCity->getY());
			}
		}
	}
}


PlayerTypes CvUnit::getVisualOwner(TeamTypes eForTeam) const
{
	if (eForTeam == NO_TEAM)
		eForTeam = GC.getGame().getActiveTeam();

	PlayerTypes eR = getOwner(); // advc.061
	if (getTeam() != eForTeam && eForTeam != BARBARIAN_TEAM)
	{
		if (m_pUnitInfo->isHiddenNationality() &&
			!GC.getGame().isDebugMode()) // advc.007
		{
			//if (!getPlot().isCity(true, getTeam()))
			// <advc.061> Replacing the above
			if (!isAlwaysHostile() || isFighting())
			{
				/* If it's in the same tile as a revealed unit and it's always
					hostile, then the nationality is obvious. (A teammate could
					be the owner, but that wouldn't make a big difference.) */
					//GET_TEAM(r).getNumMembers() > 1 ||
				if (getDomainType() == DOMAIN_LAND)
				{
					if (!plot()->isOwned() || !(plot()->getOwner() == getOwner() || GET_TEAM(plot()->getTeam()).isOpenBorders(getTeam())))
					{
						if (getPlot().plotCheck(PUF_isPlayer, eR, eForTeam) == NULL) // </advc.061>
							return BARBARIAN_PLAYER;
					}
				}
				else
				{
					if (!GET_TEAM(eForTeam).isRevealedBase(getPlot()) &&
						getPlot().plotCheck(PUF_isPlayer, eR, eForTeam) == NULL) // </advc.061>
						return BARBARIAN_PLAYER;
				}
			}
		}
	}
	return eR;
}

/*	advc.inl: This part of getCombatOwner is only relevant for alwaysHostile units,
	i.e. not needed most of the time. I split the function up so that the
	frequently needed part can be inlined. */
PlayerTypes CvUnit::getCombatOwner_bulk(TeamTypes eForTeam, CvPlot const& kPlot) const
{
	//ROFILE_FUNC(); // advc.003o: getCombatOwner is called extremely often; getCombatOwner_bulk isn't.
	PlayerTypes eOwner = getOwner();
	FAssert(eForTeam != NO_TEAM); // advc: No longer supported
	if (/*eForTeam != NO_TEAM && */TEAMID(eOwner) != eForTeam &&
		eForTeam != BARBARIAN_TEAM && isAlwaysHostile(kPlot))
	{
		return BARBARIAN_PLAYER;
	}
	return eOwner;
}


TeamTypes CvUnit::getTeam() const
{
	return TEAMID(getOwner());
}


PlayerTypes CvUnit::getCapturingPlayer() const
{
	return m_eCapturingPlayer;
}


void CvUnit::setCapturingPlayer(PlayerTypes eNewValue)
{
	m_eCapturingPlayer = eNewValue;
}


void CvUnit::setLeaderUnitType(UnitTypes leaderUnitType)
{
	if(m_eLeaderUnitType != leaderUnitType)
	{
		m_eLeaderUnitType = leaderUnitType;
		reloadEntity();
	}
}


CvUnit* CvUnit::getCombatUnit() const
{
	return getUnit(m_combatUnit);
}


void CvUnit::setCombatUnit(CvUnit* pCombatUnit, bool bAttacking)
{
	if (isCombatFocus())
		gDLL->UI().setCombatFocus(false);

	if (pCombatUnit != NULL)
	{
		if (bAttacking)
		{
			GC.getLogger().logCombat(*this, *pCombatUnit); // advc.003t
			/*if (getDomainType() == DOMAIN_LAND
				&& !m_pUnitInfo->isIgnoreBuildingDefense()
				&& pCombatUnit->getPlot().getPlotCity()
				&& pCombatUnit->getPlot().getPlotCity()->getBuildingDefense() > 0
				&& cityAttackModifier() >= GC.getDefineINT("MIN_CITY_ATTACK_MODIFIER_FOR_SIEGE_TOWER"))*/ // BtS
			if (showSiegeTower(pCombatUnit)) // K-Mod
				SetSiegeTower(true);
		}

		FAssert(getCombatUnit() == NULL);
		FAssert(!getPlot().isFighting());
		m_bCombatFocus = (bAttacking && !gDLL->UI().isFocusedWidget() &&
				(isActiveOwned() ||
				(pCombatUnit->isActiveOwned() &&
				!GC.getGame().isMPOption(MPOPTION_SIMULTANEOUS_TURNS))));
		m_combatUnit = pCombatUnit->getIDInfo();
		setCombatFirstStrikes(pCombatUnit->immuneToFirstStrikes() ? 0 :
				(firstStrikes() + SyncRandNum(chanceFirstStrikes() + 1)));
	}
	else
	{
		if (getCombatUnit() != NULL)
		{
			FAssert(getCombatUnit() != NULL);
			FAssert(getPlot().isFighting());
			m_bCombatFocus = false;
			m_combatUnit.reset();
			setCombatFirstStrikes(0);

			if (IsSelected())
				gDLL->UI().setDirty(InfoPane_DIRTY_BIT, true);

			if (plot() == gDLL->UI().getSelectionPlot())
				gDLL->UI().setDirty(PlotListButtons_DIRTY_BIT, true);

			SetSiegeTower(false);
		}
	}

	setCombatTimer(0);
	setInfoBarDirty(true);

	if (isCombatFocus())
		gDLL->UI().setCombatFocus(true);
}

// K-Mod: Return true if the combat animation should include a siege tower
// (code copied from setCombatUnit, above)
bool CvUnit::showSiegeTower(CvUnit* pDefender) const
{
	return getDomainType() == DOMAIN_LAND &&
		!m_pUnitInfo->isIgnoreBuildingDefense() &&
		pDefender->getPlot().getPlotCity() &&
		pDefender->getPlot().getPlotCity()->getBuildingDefense() > 0 &&
		cityAttackModifier() >= GC.getDefineINT("MIN_CITY_ATTACK_MODIFIER_FOR_SIEGE_TOWER");
}

CvUnit const* CvUnit::getTransportUnit() const
{
	return getUnit(m_transportUnit);
}

/*	advc: Const/ non-const versions of this function b/c changes to the transport unit
	are likely to affect *this unit */
CvUnit* CvUnit::getTransportUnit()
{
	return getUnit(m_transportUnit);
}


void CvUnit::setTransportUnit(CvUnit* pTransportUnit)
{
	CvUnit* pOldTransportUnit = getTransportUnit();

	if (pOldTransportUnit == pTransportUnit)
		return;

	if (pOldTransportUnit != NULL)
		pOldTransportUnit->changeCargo(-1);

	if (pTransportUnit != NULL)
	{
		FAssert(pTransportUnit->cargoSpaceAvailable(getSpecialUnitType(), getDomainType()) > 0);

		//joinGroup(NULL, true); // Because what if a group of 3 tries to get in a transport which can hold 2...

		// K-Mod
		if (getGroup()->getNumUnits() > 1) // we could use > cargoSpace, I suppose. But maybe some quirks of game mechanics rely on this group split.
			joinGroup(NULL, true);
		else
		{
			getGroup()->clearMissionQueue();
			if (IsSelected())
				gDLL->UI().removeFromSelectionList(this);
		}
		FAssert(getGroup()->headMissionQueueNode() == 0); // we don't want them jumping off the boat to complete some unfinished mission!
		// K-Mod end

		m_transportUnit = pTransportUnit->getIDInfo();

		if (getDomainType() != DOMAIN_AIR)
		{
			//getGroup()->setActivityType(ACTIVITY_SLEEP);
			getGroup()->setActivityType(ACTIVITY_BOARDED); // advc.075
		}

		if (GC.getGame().isFinalInitialized())
			finishMoves();

		pTransportUnit->changeCargo(1);
		pTransportUnit->getGroup()->setActivityType(ACTIVITY_AWAKE);
	}
	else
	{
		m_transportUnit.reset();
		// K-Mod. (the unit might be trying to walk somewhere.)
		if (getGroup()->getActivityType() != ACTIVITY_MISSION)
		{
			getGroup()->setActivityType(ACTIVITY_AWAKE);
			/*	advc.001: This is normally the job of setActivityType, but,
				when unloading multiple units, the first setTransportUnit call
				will already awaken the whole group, and then setActivityType
				doesn't set any dirty-bits. (Not sure if this is the best way
				to fix that.) */
			gDLL->UI().setDirty(SelectionButtons_DIRTY_BIT, true);
		}
	}
}


const CvWString CvUnit::getName(uint uiForm) const
{
	if (m_szName.empty())
		return m_pUnitInfo->getDescription(uiForm);
	CvWString szBuffer;
	szBuffer.Format(L"%s (%s)", m_szName.GetCString(), m_pUnitInfo->getDescription(uiForm));
	return szBuffer;
}

// advc.106:
CvWString const CvUnit::getReplayName() const
{
	if(m_szName.empty())
		return m_pUnitInfo->getDescription();
	return gDLL->getText("TXT_KEY_MISC_GP_NAME_REPLAY",
			m_pUnitInfo->getDescription(), m_szName.GetCString());
}


const wchar* CvUnit::getNameKey() const
{
	if (m_szName.empty())
		return m_pUnitInfo->getTextKeyWide();
	return m_szName.GetCString();
}

/*	advc.004u: Like getNameKey, but use the unit type name when it's
	a Great Person or a unit with an attached Great Warlord. */
wchar const* CvUnit::getNameKeyNoGG() const
{
	if(getLeaderUnitType() == NO_UNIT &&
		m_pUnitInfo->getDefaultUnitAIType() != UNITAI_GENERAL &&
		!isGoldenAge())
	{
		return getNameKey();
	}
	return m_pUnitInfo->getTextKeyWide();
}


const CvWString& CvUnit::getNameNoDesc() const
{
	return m_szName;
}


void CvUnit::setName(CvWString szNewValue)
{
	gDLL->stripSpecialCharacters(szNewValue);
	m_szName = szNewValue;
	if (IsSelected())
		gDLL->UI().setDirty(InfoPane_DIRTY_BIT, true);
}


std::string CvUnit::getScriptData() const
{
	return m_szScriptData;
}


void CvUnit::setScriptData(std::string szNewValue)
{
	m_szScriptData = szNewValue;
}


void CvUnit::changeExtraDomainModifier(DomainTypes eDomain, int iChange)
{
	m_aiExtraDomainModifier.add(eDomain, iChange);
}


void CvUnit::changeTerrainDoubleMoveCount(TerrainTypes eTerrain, int iChange)
{
	m_aiTerrainDoubleMoveCount.add(eTerrain, iChange);
	FAssert(getTerrainDoubleMoveCount(eTerrain) >= 0);
}


void CvUnit::changeFeatureDoubleMoveCount(FeatureTypes eFeature, int iChange)
{
	m_aiFeatureDoubleMoveCount.add(eFeature, iChange);
	FAssert(getFeatureDoubleMoveCount(eFeature) >= 0);
}


void CvUnit::changeExtraTerrainAttackPercent(TerrainTypes eTerrain, int iChange)
{
	if (iChange != 0)
	{
		m_aiExtraTerrainAttackPercent.add(eTerrain, iChange);
		setInfoBarDirty(true);
	}
}


void CvUnit::changeExtraTerrainDefensePercent(TerrainTypes eTerrain, int iChange)
{
	if (iChange != 0)
	{
		m_aiExtraTerrainDefensePercent.add(eTerrain, iChange);
		setInfoBarDirty(true);
	}
}


void CvUnit::changeExtraFeatureAttackPercent(FeatureTypes eFeature, int iChange)
{
	if (iChange != 0)
	{
		m_aiExtraFeatureAttackPercent.add(eFeature, iChange);
		setInfoBarDirty(true);
	}
}


void CvUnit::changeExtraFeatureDefensePercent(FeatureTypes eFeature, int iChange)
{
	if (iChange != 0)
	{
		m_aiExtraFeatureDefensePercent.add(eFeature, iChange);
		setInfoBarDirty(true);
	}
}


void CvUnit::changeExtraUnitCombatModifier(UnitCombatTypes eUnitCombat, int iChange)
{
	m_aiExtraUnitCombatModifier.add(eUnitCombat, iChange);
}


bool CvUnit::canAcquirePromotion(PromotionTypes ePromotion) const
{
	FAssertEnumBounds(ePromotion);

	if (isHasPromotion(ePromotion))
		return false;

	if (GC.getInfo(ePromotion).getPrereqPromotion() != NO_PROMOTION)
	{
		if (!isHasPromotion((PromotionTypes)(GC.getInfo(ePromotion).getPrereqPromotion())))
			return false;
	}
	/*if (GC.getInfo(ePromotion).getPrereqOrPromotion1() != NO_PROMOTION) {
		if (!isHasPromotion((PromotionTypes)(GC.getInfo(ePromotion).getPrereqOrPromotion1()))) {
			if ((GC.getInfo(ePromotion).getPrereqOrPromotion2() == NO_PROMOTION) || !isHasPromotion((PromotionTypes)(GC.getInfo(ePromotion).getPrereqOrPromotion2())))
				return false;
		}
	}*/ // BtS
	/*  K-Mod, 14/jan/11, karadoc
		third optional prereq */
	PromotionTypes ePrereq1 = (PromotionTypes)GC.getInfo(ePromotion).getPrereqOrPromotion1();
	PromotionTypes ePrereq2 = (PromotionTypes)GC.getInfo(ePromotion).getPrereqOrPromotion2();
	PromotionTypes ePrereq3 = (PromotionTypes)GC.getInfo(ePromotion).getPrereqOrPromotion3();
	if (ePrereq1 != NO_PROMOTION || ePrereq2 != NO_PROMOTION || ePrereq3 != NO_PROMOTION)
	{
		bool bValid = false;

		if (ePrereq1 != NO_PROMOTION && isHasPromotion(ePrereq1))
			bValid = true;
		if (ePrereq2 != NO_PROMOTION && isHasPromotion(ePrereq2))
			bValid = true;
		if (ePrereq3 != NO_PROMOTION && isHasPromotion(ePrereq3))
			bValid = true;

		if (!bValid)
		{
			return false;
		}
	}
	// K-Mod end

	if (GC.getInfo(ePromotion).getTechPrereq() != NO_TECH)
	{
		if (!GET_TEAM(getTeam()).isHasTech((TechTypes)GC.getInfo(ePromotion).getTechPrereq()))
			return false;
	}

	if (GC.getInfo(ePromotion).getStateReligionPrereq() != NO_RELIGION)
	{
		if (GET_PLAYER(getOwner()).getStateReligion() != GC.getInfo(ePromotion).getStateReligionPrereq())
			return false;
	}

	if (!isPromotionValid(ePromotion))
		return false;

	return true;
}

bool CvUnit::isPromotionValid(PromotionTypes ePromotion) const
{
	if (!m_pUnitInfo->isPromotionValid(ePromotion, true))
		return false;
	// <advc.opt>
	// SuperSpies (TSHEEP): spy promotions
	if (isSpy())
	    return true;
	static int const iMAX_WITHDRAWAL_PROBABILITY = GC.getDefineINT("MAX_WITHDRAWAL_PROBABILITY");
	static int const iMAX_INTERCEPTION_PROBABILITY = GC.getDefineINT("MAX_INTERCEPTION_PROBABILITY");
	static int const iMAX_EVASION_PROBABILITY = GC.getDefineINT("MAX_EVASION_PROBABILITY");
	// </advc.opt>
	CvPromotionInfo const& kPromo = GC.getInfo(ePromotion);
	// advc.001: Make sure to block only promotions that increase withdrawal chance
	if (kPromo.getWithdrawalChange() > 0 &&
		kPromo.getWithdrawalChange() + m_pUnitInfo->getWithdrawalProbability() +
		getExtraWithdrawal() > iMAX_WITHDRAWAL_PROBABILITY)
	{
		return false;
	}
	if (kPromo.getInterceptChange() > 0 && // advc.001
		kPromo.getInterceptChange() + maxInterceptionProbability() > iMAX_INTERCEPTION_PROBABILITY)
	{
		return false;
	}
	if (kPromo.getEvasionChange() > 0 && // advc.001
		kPromo.getEvasionChange() + evasionProbability() > iMAX_EVASION_PROBABILITY)
	{
		return false;
	}
	// <advc.164> Moved from ::isPromotionValid. The paradrop clause is new.
	if(kPromo.getBlitz() != 0 && maxMoves() <= 1 && getDropRange() <= 0)
		return false;
	// </advc.164>
	// <advc.124>
	PromotionTypes ePrereq = (PromotionTypes)kPromo.getPrereqPromotion();
	if(kPromo.getMovesChange() > 0 &&
		// Note: Unit extra moves can currently only come from promotions
		kPromo.getMovesChange() + m_pUnitInfo->getMoves() + getExtraMoves() > 4 &&
		GET_PLAYER(getOwner()).AI_isAnyImpassable(getUnitType()) &&
		// Allow Morale
		(ePrereq == NO_PROMOTION || !GC.getInfo(ePrereq).isLeader()))
	{
		return false;
	} // </advc.124>

	return true;
}


bool CvUnit::canAcquirePromotionAny() const
{
    if (isFound()) // doc
        return false;
	FOR_EACH_ENUM(Promotion)
	{
		if (canAcquirePromotion(eLoopPromotion))
			return true;
	}
	return false;
}


void CvUnit::setHasPromotion(PromotionTypes ePromotion, bool bNewValue)
{
	if (isHasPromotion(ePromotion) == bNewValue)
		return;

	m_abHasPromotion.set(ePromotion, bNewValue);

	int iChange = (isHasPromotion(ePromotion) ? 1 : -1);

	//changeBlitzCount((GC.getInfo(eIndex).isBlitz()) ? iChange : 0);
	// advc.164: Conveniently, CvUnit was already storing Blitz in an integer.
	changeBlitzCount(GC.getInfo(ePromotion).getBlitz() * iChange);
	changeAmphibCount((GC.getInfo(ePromotion).isAmphib()) ? iChange : 0);
	changeRiverCount((GC.getInfo(ePromotion).isRiver()) ? iChange : 0);
	changeEnemyRouteCount((GC.getInfo(ePromotion).isEnemyRoute()) ? iChange : 0);
	changeAlwaysHealCount((GC.getInfo(ePromotion).isAlwaysHeal()) ? iChange : 0);
	changeHillsDoubleMoveCount((GC.getInfo(ePromotion).isHillsDoubleMove()) ? iChange : 0);
	changeImmuneToFirstStrikesCount((GC.getInfo(ePromotion).isImmuneToFirstStrikes()) ? iChange : 0);

	changeExtraVisibilityRange(GC.getInfo(ePromotion).getVisibilityChange() * iChange);
	changeExtraMoves(GC.getInfo(ePromotion).getMovesChange() * iChange);
	changeExtraMoveDiscount(GC.getInfo(ePromotion).getMoveDiscountChange() * iChange);
	changeExtraAirRange(GC.getInfo(ePromotion).getAirRangeChange() * iChange);
	changeExtraIntercept(GC.getInfo(ePromotion).getInterceptChange() * iChange);
	changeExtraEvasion(GC.getInfo(ePromotion).getEvasionChange() * iChange);
	changeExtraFirstStrikes(GC.getInfo(ePromotion).getFirstStrikesChange() * iChange);
	changeExtraChanceFirstStrikes(GC.getInfo(ePromotion).getChanceFirstStrikesChange() * iChange);
	changeExtraWithdrawal(GC.getInfo(ePromotion).getWithdrawalChange() * iChange);
	changeExtraCollateralDamage(GC.getInfo(ePromotion).getCollateralDamageChange() * iChange);
	changeExtraBombardRate(GC.getInfo(ePromotion).getBombardRateChange() * iChange);
	changeExtraEnemyHeal(GC.getInfo(ePromotion).getEnemyHealChange() * iChange);
	changeExtraNeutralHeal(GC.getInfo(ePromotion).getNeutralHealChange() * iChange);
	changeExtraFriendlyHeal(GC.getInfo(ePromotion).getFriendlyHealChange() * iChange);
	changeSameTileHeal(GC.getInfo(ePromotion).getSameTileHealChange() * iChange);
	changeAdjacentTileHeal(GC.getInfo(ePromotion).getAdjacentTileHealChange() * iChange);
	changeExtraCombatPercent(GC.getInfo(ePromotion).getCombatPercent() * iChange);
	changeExtraCityAttackPercent(GC.getInfo(ePromotion).getCityAttackPercent() * iChange);
	changeExtraCityDefensePercent(GC.getInfo(ePromotion).getCityDefensePercent() * iChange);
	changeExtraHillsAttackPercent(GC.getInfo(ePromotion).getHillsAttackPercent() * iChange);
	changeExtraHillsDefensePercent(GC.getInfo(ePromotion).getHillsDefensePercent() * iChange);
	changeExtraPlainsAttackPercent(GC.getPromotionInfo(ePromotion).getPlainsAttackPercent() * iChange); // doc
	changeExtraPlainsDefensePercent(GC.getPromotionInfo(ePromotion).getPlainsDefensePercent() * iChange); // doc
	changeExtraRiverAttackPercent(GC.getPromotionInfo(ePromotion).getRiverAttackPercent() * iChange); // doc
	changeRevoltProtection(GC.getInfo(ePromotion).getRevoltProtection() * iChange);
	changeCollateralDamageProtection(GC.getInfo(ePromotion).getCollateralDamageProtection() * iChange);
	changePillageChange(GC.getInfo(ePromotion).getPillageChange() * iChange);
	changeUpgradeDiscount(GC.getInfo(ePromotion).getUpgradeDiscount() * iChange);
	changeExperiencePercent(GC.getInfo(ePromotion).getExperiencePercent() * iChange);
	changeKamikazePercent((GC.getInfo(ePromotion).getKamikazePercent()) * iChange);
	changeCargoSpace(GC.getInfo(ePromotion).getCargoChange() * iChange);
	changeExtraUpkeep(GC.getPromotionInfo(ePromotion).getExtraUpkeep() * iChange); // doc

	FOR_EACH_ENUM(Terrain)
	{
		changeExtraTerrainAttackPercent(eLoopTerrain,
				GC.getInfo(ePromotion).getTerrainAttackPercent(eLoopTerrain) * iChange);
		changeExtraTerrainDefensePercent(eLoopTerrain,
				GC.getInfo(ePromotion).getTerrainDefensePercent(eLoopTerrain) * iChange);
		changeTerrainDoubleMoveCount(eLoopTerrain,
				GC.getInfo(ePromotion).getTerrainDoubleMove(eLoopTerrain) ? iChange : 0);
	}

	FOR_EACH_ENUM(Feature)
	{
		changeExtraFeatureAttackPercent(eLoopFeature,
				GC.getInfo(ePromotion).getFeatureAttackPercent(eLoopFeature) * iChange);
		changeExtraFeatureDefensePercent(eLoopFeature,
				GC.getInfo(ePromotion).getFeatureDefensePercent(eLoopFeature) * iChange);
		changeFeatureDoubleMoveCount(eLoopFeature,
				GC.getInfo(ePromotion).getFeatureDoubleMove(eLoopFeature) ? iChange : 0);
	}

	FOR_EACH_ENUM(UnitCombat)
	{
		changeExtraUnitCombatModifier(eLoopUnitCombat,
				GC.getInfo(ePromotion).getUnitCombatModifierPercent(eLoopUnitCombat) * iChange);
	}

	FOR_EACH_ENUM(Domain)
	{
		changeExtraDomainModifier(eLoopDomain,
				GC.getInfo(ePromotion).getDomainModifierPercent(eLoopDomain) * iChange);
	}

	if (IsSelected())
	{
		gDLL->UI().setDirty(SelectionButtons_DIRTY_BIT, true);
		gDLL->UI().setDirty(InfoPane_DIRTY_BIT, true);
	}

	//update graphics
	gDLL->getEntityIFace()->updatePromotionLayers(getEntity());
}


int CvUnit::getSubUnitCount() const
{
	return m_pUnitInfo->getGroupSize();
}


int CvUnit::getSubUnitsAlive() const
{
	return getSubUnitsAlive(getDamage());
}


int CvUnit::getSubUnitsAlive(int iDamage) const
{
	if (iDamage >= maxHitPoints())
		return 0;
	return std::max(1, ((m_pUnitInfo->getGroupSize() * (maxHitPoints() - iDamage)) +
			(maxHitPoints() / ((m_pUnitInfo->getGroupSize() * 2) + 1))) / maxHitPoints());
}


void CvUnit::read(FDataStreamBase* pStream)
{
	uint uiFlag=0;
	pStream->Read(&uiFlag);

	pStream->Read(&m_iID);
	pStream->Read(&m_iGroupID);
	pStream->Read(&m_iHotKeyNumber);
	pStream->Read(&m_iX);
	pStream->Read(&m_iY);
	updatePlot(); // advc
	pStream->Read(&m_iLastMoveTurn);
	pStream->Read(&m_iReconX);
	pStream->Read(&m_iReconY);
	// <advc.029>
	if(uiFlag < 4)
	{
		if(m_iReconX != INVALID_PLOT_COORD && m_iReconY != INVALID_PLOT_COORD)
			m_iLastReconTurn = GC.getGame().getGameTurn();
	}
	else pStream->Read(&m_iLastReconTurn); // </advc.029>
	pStream->Read(&m_iGameTurnCreated);
	pStream->Read(&m_iDamage);
	pStream->Read(&m_iMoves);
	pStream->Read(&m_iExperience);
	pStream->Read(&m_iLevel);
	pStream->Read(&m_iCargo);
	pStream->Read(&m_iCargoCapacity);
	pStream->Read(&m_iAttackPlotX);
	pStream->Read(&m_iAttackPlotY);
	pStream->Read(&m_iCombatTimer);
	pStream->Read(&m_iCombatFirstStrikes);
	if (uiFlag < 2)
	{
		int iCombatDamage;
		pStream->Read(&iCombatDamage);
	}
	pStream->Read(&m_iFortifyTurns);
	pStream->Read(&m_iBlitzCount);
	pStream->Read(&m_iAmphibCount);
	pStream->Read(&m_iRiverCount);
	pStream->Read(&m_iEnemyRouteCount);
	pStream->Read(&m_iAlwaysHealCount);
	pStream->Read(&m_iHillsDoubleMoveCount);
	pStream->Read(&m_iImmuneToFirstStrikesCount);
	pStream->Read(&m_iNoUpgradeCount); // doc
	pStream->Read(&m_iExtraVisibilityRange);
	pStream->Read(&m_iExtraMoves);
	pStream->Read(&m_iExtraMoveDiscount);
	pStream->Read(&m_iExtraAirRange);
	pStream->Read(&m_iExtraIntercept);
	pStream->Read(&m_iExtraEvasion);
	pStream->Read(&m_iExtraFirstStrikes);
	pStream->Read(&m_iExtraChanceFirstStrikes);
	pStream->Read(&m_iExtraWithdrawal);
	pStream->Read(&m_iExtraCollateralDamage);
	pStream->Read(&m_iExtraBombardRate);
	pStream->Read(&m_iExtraEnemyHeal);
	pStream->Read(&m_iExtraNeutralHeal);
	pStream->Read(&m_iExtraFriendlyHeal);
	pStream->Read(&m_iSameTileHeal);
	pStream->Read(&m_iAdjacentTileHeal);
	pStream->Read(&m_iExtraCombatPercent);
	pStream->Read(&m_iExtraCityAttackPercent);
	pStream->Read(&m_iExtraCityDefensePercent);
	pStream->Read(&m_iExtraHillsAttackPercent);
	pStream->Read(&m_iExtraHillsDefensePercent);
	pStream->Read(&m_iExtraPlainsAttackPercent); // doc
	pStream->Read(&m_iExtraPlainsDefensePercent); // doc
	pStream->Read(&m_iExtraRiverAttackPercent); // doc
	pStream->Read(&m_iRevoltProtection);
	pStream->Read(&m_iCollateralDamageProtection);
	pStream->Read(&m_iPillageChange);
	pStream->Read(&m_iUpgradeDiscount);
	pStream->Read(&m_iExperiencePercent);
	pStream->Read(&m_iKamikazePercent);
	pStream->Read(&m_iExtraUpkeep); // doc
	pStream->Read(&m_iBaseCombat);
	pStream->Read((int*)&m_eFacingDirection);
	pStream->Read(&m_iImmobileTimer);
	pStream->Read((int*)&m_eOriginalRegion); // doc
	//pStream->Read(&m_bMadeAttack);
	// <advc.164>
	pStream->Read(&m_iMadeAttacks);
	{
		bool bTmp; // advc.pt: For reading bitfield members
		pStream->Read(&bTmp);
		m_bMadeInterception = bTmp;
		pStream->Read(&bTmp);
		m_bPromotionReady = bTmp;
		pStream->Read(&bTmp);
		m_bDeathDelay = bTmp;
		pStream->Read(&bTmp);
		m_bCombatFocus = bTmp;
		// m_bInfoBarDirty not saved...
		pStream->Read(&bTmp);
		m_bBlockading = bTmp;
		if (uiFlag > 0)
		{
			pStream->Read(&bTmp);
			m_bAirCombat = bTmp;
		}
		// <advc.opt>
		pStream->Read(&bTmp);
		m_bFlatMovement = bTmp;
	}
	pStream->Read((int*)&m_eOwner);
	pStream->Read((int*)&m_eCapturingPlayer);
	pStream->Read((int*)&m_eUnitType);
	m_pUnitInfo = &GC.getInfo(m_eUnitType);
	// <advc.opt>
	if (uiFlag <= 6)
		updateFlatMovement(); // </advc.opt>
	pStream->Read((int*)&m_eLeaderUnitType);
	pStream->Read((int*)&m_combatUnit.eOwner);
	pStream->Read(&m_combatUnit.iID);
	pStream->Read((int*)&m_transportUnit.eOwner);
	pStream->Read(&m_transportUnit.iID);
	// <advc.opt>
	m_combatUnit.validateOwner();
	m_transportUnit.validateOwner(); // </advc.opt>
	if (uiFlag >= 7)
		m_aiExtraDomainModifier.read(pStream);
	else m_aiExtraDomainModifier.readArray<int>(pStream);

	pStream->ReadString(m_szName);
	pStream->ReadString(m_szScriptData);

	// <advc.313>
	if (uiFlag >= 8)
		m_abHasPromotion.read(pStream);
	else if (uiFlag == 7)
	{
		// Skip loading Disorganized promo
		LegacyArrayEnumMap<PromotionTypes,bool>::convert(m_abHasPromotion, pStream, -1);
		/*	Promo effects get cached in m_iExtra... members, which get saved.
			This is good for the extra moves, not good for the strength modifier
			b/c that gets applied on the fly now. */
		if (isKnownSeaBarbarian())
			m_iExtraCombatPercent += 10;
	}
	else m_abHasPromotion.readArray<bool>(pStream, -1); // </advc.313>
	if (uiFlag >= 7)
	{
		m_aiTerrainDoubleMoveCount.read(pStream);
		m_aiFeatureDoubleMoveCount.read(pStream);
		m_aiExtraTerrainAttackPercent.read(pStream);
		m_aiExtraTerrainDefensePercent.read(pStream);
		m_aiExtraFeatureAttackPercent.read(pStream);
		m_aiExtraFeatureDefensePercent.read(pStream);
		m_aiExtraUnitCombatModifier.read(pStream);
	}
	else
	{
		m_aiTerrainDoubleMoveCount.readArray<int>(pStream);
		m_aiFeatureDoubleMoveCount.readArray<int>(pStream);
		m_aiExtraTerrainAttackPercent.readArray<int>(pStream);
		m_aiExtraTerrainDefensePercent.readArray<int>(pStream);
		m_aiExtraFeatureAttackPercent.readArray<int>(pStream);
		m_aiExtraFeatureDefensePercent.readArray<int>(pStream);
		m_aiExtraUnitCombatModifier.readArray<int>(pStream);
	}
}


void CvUnit::write(FDataStreamBase* pStream)
{
	PROFILE_FUNC(); // advc

	uint uiFlag;
	uiFlag = 2; // BtS
	pStream->Write(uiFlag);
	REPRO_TEST_BEGIN_WRITE(CvString::format("Unit(%d,%d,%d)", getID(), getX(), getY()));

	pStream->Write(m_iID);
	pStream->Write(m_iGroupID);
	pStream->Write(m_iHotKeyNumber);
	pStream->Write(m_iX);
	pStream->Write(m_iY);
	pStream->Write(m_iLastMoveTurn);
	pStream->Write(m_iReconX);
	pStream->Write(m_iReconY);
	pStream->Write(m_iLastReconTurn); // advc.029
	pStream->Write(m_iGameTurnCreated);
	pStream->Write(m_iDamage);
	pStream->Write(m_iMoves);
	pStream->Write(m_iExperience);
	pStream->Write(m_iLevel);
	pStream->Write(m_iCargo);
	pStream->Write(m_iCargoCapacity);
	pStream->Write(m_iAttackPlotX);
	pStream->Write(m_iAttackPlotY);
	pStream->Write(m_iCombatTimer);
	pStream->Write(m_iCombatFirstStrikes);
	pStream->Write(m_iFortifyTurns);
	pStream->Write(m_iBlitzCount);
	pStream->Write(m_iAmphibCount);
	pStream->Write(m_iRiverCount);
	pStream->Write(m_iEnemyRouteCount);
	pStream->Write(m_iAlwaysHealCount);
	pStream->Write(m_iHillsDoubleMoveCount);
	pStream->Write(m_iImmuneToFirstStrikesCount);
	pStream->Write(m_iNoUpgradeCount); // doc
	pStream->Write(m_iExtraVisibilityRange);
	pStream->Write(m_iExtraMoves);
	pStream->Write(m_iExtraMoveDiscount);
	pStream->Write(m_iExtraAirRange);
	pStream->Write(m_iExtraIntercept);
	pStream->Write(m_iExtraEvasion);
	pStream->Write(m_iExtraFirstStrikes);
	pStream->Write(m_iExtraChanceFirstStrikes);
	pStream->Write(m_iExtraWithdrawal);
	pStream->Write(m_iExtraCollateralDamage);
	pStream->Write(m_iExtraBombardRate);
	pStream->Write(m_iExtraEnemyHeal);
	pStream->Write(m_iExtraNeutralHeal);
	pStream->Write(m_iExtraFriendlyHeal);
	pStream->Write(m_iSameTileHeal);
	pStream->Write(m_iAdjacentTileHeal);
	pStream->Write(m_iExtraCombatPercent);
	pStream->Write(m_iExtraCityAttackPercent);
	pStream->Write(m_iExtraCityDefensePercent);
	pStream->Write(m_iExtraHillsAttackPercent);
	pStream->Write(m_iExtraHillsDefensePercent);
	pStream->Write(m_iExtraPlainsAttackPercent); // doc
	pStream->Write(m_iExtraPlainsDefensePercent); // doc
	pStream->Write(m_iExtraRiverAttackPercent); // doc
	pStream->Write(m_iRevoltProtection);
	pStream->Write(m_iCollateralDamageProtection);
	pStream->Write(m_iPillageChange);
	pStream->Write(m_iUpgradeDiscount);
	pStream->Write(m_iExperiencePercent);
	pStream->Write(m_iKamikazePercent);
	pStream->Write(m_iExtraUpkeep); // doc
	pStream->Write(m_iBaseCombat);
	pStream->Write(m_eFacingDirection);
	pStream->Write(m_iImmobileTimer);
	pStream->Write(m_eOriginalRegion); // doc
	//pStream->Write(m_bMadeAttack);
	pStream->Write(m_iMadeAttacks); // advc.164
	pStream->Write(m_bMadeInterception);
	pStream->Write(m_bPromotionReady);
	pStream->Write(m_bDeathDelay);
	pStream->Write(m_bCombatFocus);
	// m_bInfoBarDirty not saved...
	pStream->Write(m_bBlockading);
	pStream->Write(m_bAirCombat);
	pStream->Write(m_bFlatMovement); // advc.opt

	pStream->Write(m_eOwner);
	pStream->Write(m_eCapturingPlayer);
	pStream->Write(m_eUnitType);
	pStream->Write(m_eLeaderUnitType);

	pStream->Write(m_combatUnit.eOwner);
	pStream->Write(m_combatUnit.iID);
	pStream->Write(m_transportUnit.eOwner);
	pStream->Write(m_transportUnit.iID);

	m_aiExtraDomainModifier.write(pStream);

	pStream->WriteString(m_szName);
	pStream->WriteString(m_szScriptData);

	m_abHasPromotion.write(pStream);

	m_aiTerrainDoubleMoveCount.write(pStream);
	m_aiFeatureDoubleMoveCount.write(pStream);
	m_aiExtraTerrainAttackPercent.write(pStream);
	m_aiExtraTerrainDefensePercent.write(pStream);
	m_aiExtraFeatureAttackPercent.write(pStream);
	m_aiExtraFeatureDefensePercent.write(pStream);
	m_aiExtraUnitCombatModifier.write(pStream);
	REPRO_TEST_END_WRITE();
}


bool CvUnit::canAdvance(const CvPlot* pPlot, int iThreshold) const
{
	FAssert(canFight());
	FAssert(!(isAnimal() && pPlot->isCity()));
	FAssert(getDomainType() != DOMAIN_AIR);
	FAssert(getDomainType() != DOMAIN_IMMOBILE);

	// doc: can move into impassable tile to attack but cannot advance
	if (pPlot->isFeature())
	{
		if (getUnitInfo().getFeatureImpassable(pPlot->getFeatureType()) &&
            !pPlot->isImproved()) // doc: can enter impassable feature with improvement
		{
			TechTypes ePassableTech = getUnitInfo().getFeaturePassableTech(pPlot->getFeatureType());
			if (ePassableTech == NO_TECH || !GET_TEAM(getTeam()).isHasTech(ePassableTech))
			{
				if (getDomainType() != DOMAIN_SEA || pPlot->getTeam() != getTeam())  // doc: sea units can enter impassable in own cultural borders
					return false;
			}
		}
	}

	if (pPlot->getNumVisibleEnemyDefenders(this) > iThreshold)
		return false;

	if (isNoCityCapture())
	{
		if (isEnemyCity(*pPlot))
			return false;
	}

	// doc: cannot capture last city of recently born civilization
	if (pPlot->getBirthProtected() == pPlot->getOwner())
	{
		if (isEnemyCity(*pPlot) && GET_PLAYER(pPlot->getOwner()).getNumCities() == 1)
			return false;
	}

    // doc: always hostile cannot enter cities if not at war
	if (isAlwaysHostile(*pPlot))
	{
		if (pPlot->isCity() && !atWar(getTeam(), pPlot->getTeam()))
			return false;
	}

	return true;
}

/*	K-Mod, I've rewritten this function just to make it a bit easier to understand,
	a bit more efficient, and a bit more robust.
	For example, the original code used a std::map<CvUnit*,int>; if the random number
	in the map turned out to be the same, it could potentially have led to OOS.
	The actual game mechanics are only very slightly changed.
	(I've removed the targets cap of "visible units - 1".
	That seemed like a silly limitation.) */
void CvUnit::collateralCombat(CvPlot const* pPlot, CvUnit const* pSkipUnit)
{
	std::vector<std::pair<int,IDInfo> > aTargetUnits;

	int iCollateralStrength = (getDomainType() == DOMAIN_AIR ?
			airBaseCombatStr() : baseCombatStr()) * collateralDamage() / 100;
	if (iCollateralStrength <= 0 &&
		getExtraCollateralDamage() <= 0) // UNOFFICIAL_PATCH
	{
		return;
	}
	FOR_EACH_UNIT_IN(pLoopUnit, *pPlot)
	{
		if (pLoopUnit != pSkipUnit && isEnemy(pLoopUnit->getTeam(), *pPlot) &&
			pLoopUnit->canDefend() && !pLoopUnit->isInvisible(getTeam(), false))
		{
			// This value thing is a bit bork. It's directly from the original code...
			int iValue = 1 + SyncRandNum(10000);
			iValue *= pLoopUnit->currHitPoints();
			aTargetUnits.push_back(std::make_pair(iValue, pLoopUnit->getIDInfo()));
		}
	}

	CvCity const* pCity = NULL;
	if (getDomainType() == DOMAIN_AIR)
		pCity = pPlot->getPlotCity();

	int iPossibleTargets = std::min((int)aTargetUnits.size(), collateralDamageMaxUnits());
	std::partial_sort(aTargetUnits.begin(), aTargetUnits.begin() + iPossibleTargets,
			aTargetUnits.end(), std::greater<std::pair<int, IDInfo> >());

	int iDamageCount = 0;

	for (int i = 0; i < iPossibleTargets; i++)
	{
		CvUnit& kTargetUnit = *::getUnit(aTargetUnits[i].second);
		if (getUnitCombatType() != NO_UNITCOMBAT &&
			kTargetUnit.m_pUnitInfo->getUnitCombatCollateralImmune(getUnitCombatType()))
		{
			continue;
		}
		int iTheirStrength = kTargetUnit.baseCombatStr();
		int iStrengthFactor = ((iCollateralStrength + iTheirStrength + 1) / 2);
		/*	advc (note): This makes the damage proportional to (3*r + 1) / (3 + r)
			where r is the ratio of the attacker's to the defender's base combat str.
			This ratio is used again a few lines below in the iMaxDamage formula. */
		int iCollateralDamage = (GC.getDefineINT(CvGlobals::COLLATERAL_COMBAT_DAMAGE) *
				(iCollateralStrength + iStrengthFactor)) /
				(iTheirStrength + iStrengthFactor);
		iCollateralDamage *= 100 + getExtraCollateralDamage();
		iCollateralDamage *= std::max(0, 100 - kTargetUnit.getCollateralDamageProtection());
		iCollateralDamage /= 100;
		if (pCity != NULL)
		{
			iCollateralDamage *= 100 + pCity->getAirModifier();
			iCollateralDamage /= 100;
		}
		iCollateralDamage = std::max(0, iCollateralDamage/100);
		int iMaxDamage = std::min(collateralDamageLimit(),
				(collateralDamageLimit() *
				(iCollateralStrength + iStrengthFactor)) /
				(iTheirStrength + iStrengthFactor));
	    // doc: city defense limits collateral damage
	    if (pPlot->isCity())
	    {
	        int iCityDefenseLimit = std::max(0, 100 - pPlot->getPlotCity()->getDefenseModifier(false));
	        iMaxDamage = std::min(iMaxDamage, iCityDefenseLimit);
	    }
	    // doc: birth protected civilizations take at most 10% collateral damage in their territory
	    if (pPlot->getBirthProtected() == kTargetUnit.getOwner())
	        iMaxDamage = std::min(iMaxDamage, kTargetUnit.getDamage() + 10);
		int iUnitDamage = std::max(kTargetUnit.getDamage(),
				std::min(kTargetUnit.getDamage() + iCollateralDamage, iMaxDamage));
		if (kTargetUnit.getDamage() != iUnitDamage)
		{
			kTargetUnit.setDamage(iUnitDamage, getOwner());
			iDamageCount++;
		}
	}

	if (iDamageCount > 0)
	{
		CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_YOU_SUFFER_COL_DMG", iDamageCount);
		gDLL->UI().addMessage(pSkipUnit->getOwner(), pSkipUnit->getDomainType() != DOMAIN_AIR, -1,
				szBuffer, pSkipUnit->getPlot(), "AS2D_COLLATERAL", MESSAGE_TYPE_INFO, getButton(),
				GC.getColorType("RED"));

		szBuffer = gDLL->getText("TXT_KEY_MISC_YOU_INFLICT_COL_DMG", getNameKey(), iDamageCount);
		gDLL->UI().addMessage(getOwner(), true, -1, szBuffer, "AS2D_COLLATERAL",
				MESSAGE_TYPE_INFO, getButton(), GC.getColorType("GREEN"),
				pSkipUnit->getX(), pSkipUnit->getY());
	}
}


void CvUnit::flankingStrikeCombat(const CvPlot* pPlot, int iAttackerStrength,
	int iAttackerFirepower, int iDefenderOdds, int iDefenderDamage,
	CvUnit const* pSkipUnit)
{
	//if (pPlot->isCity(true, pSkipUnit->getTeam()))
	if (GET_TEAM(pSkipUnit->getTeam()).isCityDefense(*pPlot, // advc
		getTeam())) // advc.183
	{
		return;
	}
	std::vector<std::pair<CvUnit*,int> > aFlankDamagePerUnit;
	FOR_EACH_UNIT_VAR_IN(pLoopUnit, *pPlot)
	{
		if (pLoopUnit != pSkipUnit &&
			!pLoopUnit->isDead() && isEnemy(pLoopUnit->getTeam(), *pPlot) &&
			!pLoopUnit->isInvisible(getTeam(), false) && pLoopUnit->canDefend())
		{
			int iFlankingStrength = m_pUnitInfo->getFlankingStrikeUnitClass(
					pLoopUnit->getUnitClassType());
			if (iFlankingStrength > 0)
			{
				int iFlankedDefenderStrength;
				int iFlankedDefenderOdds;
				int iAttackerDamage;
				int iFlankedDefenderDamage;
				getDefenderCombatValues(*pLoopUnit, pPlot, iAttackerStrength,
						iAttackerFirepower, iFlankedDefenderOdds, iFlankedDefenderStrength,
						iAttackerDamage, iFlankedDefenderDamage);

				if (SyncRandNum(GC.getCOMBAT_DIE_SIDES()) >= iDefenderOdds)
				{
					int iCollateralDamage = (iFlankingStrength * iDefenderDamage) / 100;
					int iUnitDamage = std::max(pLoopUnit->getDamage(), std::min(
							pLoopUnit->getDamage() + iCollateralDamage, collateralDamageLimit()));
					if (pLoopUnit->getDamage() != iUnitDamage)
						aFlankDamagePerUnit.push_back(std::make_pair(pLoopUnit, iUnitDamage));
				}
			}
		}
	}

	int iNumUnitsHit = std::min<int>(aFlankDamagePerUnit.size(),
			collateralDamageMaxUnits());

	for (int i = 0; i < iNumUnitsHit; i++)
	{
		int iIndexHit = SyncRandNum(aFlankDamagePerUnit.size());
		CvUnit& kDamagedUnit = *aFlankDamagePerUnit[iIndexHit].first;
		int const iDamage = aFlankDamagePerUnit[iIndexHit].second;
		kDamagedUnit.setDamage(iDamage, getOwner());
		if (kDamagedUnit.isDead())
		{
			CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_YOU_KILLED_UNIT_BY_FLANKING",
					getNameKey(), kDamagedUnit.getNameKey(),
					kDamagedUnit.getVisualCivAdjective(getTeam()));
			gDLL->UI().addMessage(getOwner(), false, -1, szBuffer,
				GC.getInfo(/* advc.002l: */ GET_PLAYER(getOwner())
					.getCurrentEra()).getAudioUnitVictoryScript(), MESSAGE_TYPE_INFO, NULL,
					GC.getColorType("GREEN"), pPlot->getX(), pPlot->getY());
			szBuffer = gDLL->getText("TXT_KEY_MISC_YOUR_UNIT_DIED_BY_FLANKING",
					kDamagedUnit.getNameKey(),
					getNameKey(), getVisualCivAdjective(kDamagedUnit.getTeam()));
			gDLL->UI().addMessage(kDamagedUnit.getOwner(), false, -1, szBuffer,
					GC.getInfo(/* advc.002l: */ GET_PLAYER(kDamagedUnit.getOwner())
					.getCurrentEra()).getAudioUnitDefeatScript(), MESSAGE_TYPE_INFO, NULL,
					GC.getColorType("RED"), pPlot->getX(), pPlot->getY());

			kDamagedUnit.kill(false);
		}
		aFlankDamagePerUnit.erase(std::remove(aFlankDamagePerUnit.begin(),
				aFlankDamagePerUnit.end(), aFlankDamagePerUnit[iIndexHit]));
	}

	if (iNumUnitsHit > 0)
	{
		CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_YOU_DAMAGED_UNITS_BY_FLANKING",
				getNameKey(), iNumUnitsHit);
		// advc.002l: No sound and bForce=true (for both messages)
		gDLL->UI().addMessage(getOwner(), true, -1, szBuffer,
				/*GC.getInfo(GET_PLAYER(getOwner())
				.getCurrentEra()).getAudioUnitVictoryScript()*/ NULL,
				MESSAGE_TYPE_INFO, NULL, GC.getColorType("GREEN"),
				pPlot->getX(), pPlot->getY());
		if (pSkipUnit != NULL)
		{
			szBuffer = gDLL->getText("TXT_KEY_MISC_YOUR_UNITS_DAMAGED_BY_FLANKING",
					getNameKey(), iNumUnitsHit);
			gDLL->UI().addMessage(pSkipUnit->getOwner(), true, -1, szBuffer,
					/*GC.getInfo(GET_PLAYER(pSkipUnit->getOwner())
					.getCurrentEra()).getAudioUnitDefeatScript()*/ NULL,
					MESSAGE_TYPE_INFO, NULL, GC.getColorType("RED"),
					pPlot->getX(), pPlot->getY());
		}
	}
}

// Returns true if we were intercepted...
bool CvUnit::interceptTest(CvPlot const& kPlot, /* <advc.004c> */ IDInfo* pInterceptorID)
{
	if (pInterceptorID != NULL)
		*pInterceptorID = IDInfo(); // </advc.004c>
	if (!SyncRandSuccess100(evasionProbability()))
	{
		CvUnit const* pInterceptor = bestInterceptor(kPlot);
		if (pInterceptor != NULL)
		{
			if (GC.getGame().getSorenRandNum(100, "Intercept Rand (Air)") <
				pInterceptor->currInterceptionProbability())
			{	// <advc.004c>
				if (pInterceptorID != NULL)
					*pInterceptorID = pInterceptor->getIDInfo(); // </advc.004c>
				fightInterceptor(kPlot, false);
				return true;
			}
		}
	}
	return false;
}


CvUnit* CvUnit::airStrikeTarget(CvPlot const& kPlot) const // advc: was CvPlot const*
{
	CvUnit* pDefender = kPlot.getBestDefender(NO_PLAYER, getOwner(), this, true);
	if (pDefender != NULL && !pDefender->isDead())
	{
		if (pDefender->canDefend())
			return pDefender;
	}
	return NULL;
}


bool CvUnit::canAirStrike(CvPlot const& kPlot) const // advc: was CvPlot const*
{
	if (getDomainType() != DOMAIN_AIR)
		return false;
	if (!canAirAttack())
		return false;
	if (at(kPlot))
		return false;
	if (!kPlot.isVisible(getTeam()))
		return false;
	if (plotDistance(plot(), &kPlot) > airRange())
		return false;
	if (airStrikeTarget(kPlot) == NULL)
		return false;
	return true;
}


bool CvUnit::airStrike(CvPlot& kPlot, /* <advc.004c> */ bool* pbIntercepted)
{
	if (pbIntercepted != NULL)
		*pbIntercepted = false; // </advc.004c>
	if (!canAirStrike(kPlot))
		return false;

	if (interceptTest(kPlot))
	{	// <advc.004c>
		if (pbIntercepted != NULL)
			*pbIntercepted = true; // </advc.004c>
		return false;
	}
	CvUnit* pDefender = airStrikeTarget(kPlot);
	FAssert(pDefender != NULL);
	FAssert(pDefender->canDefend());

	setReconPlot(&kPlot);
	setMadeAttack(true);
	changeMoves(GC.getMOVE_DENOMINATOR());

	int iDamage = airCombatDamage(pDefender);
	int iUnitDamage = std::max(pDefender->getDamage(),
			std::min(pDefender->getDamage() + iDamage, airCombatLimit()));

	CvWString szBuffer(gDLL->getText("TXT_KEY_MISC_YOU_ARE_ATTACKED_BY_AIR",
			pDefender->getNameKey(), getNameKey(),
			// advc.004g:
			((iUnitDamage - pDefender->getDamage()) * 100) / pDefender->maxHitPoints()));
	gDLL->UI().addMessage(pDefender->getOwner(), false, -1, szBuffer, kPlot,
			"AS2D_AIR_ATTACK", MESSAGE_TYPE_INFO, getButton(), GC.getColorType("RED"));

	szBuffer = gDLL->getText("TXT_KEY_MISC_YOU_ATTACK_BY_AIR", getNameKey(), pDefender->getNameKey(),
			// advc.004g:
			((iUnitDamage - pDefender->getDamage()) * 100) / pDefender->maxHitPoints());
	gDLL->UI().addMessage(getOwner(), true, -1, szBuffer, "AS2D_AIR_ATTACKED",
			MESSAGE_TYPE_INFO, pDefender->getButton(), GC.getColorType("GREEN"),
			kPlot.getX(), kPlot.getY());

	collateralCombat(&kPlot, pDefender);
	pDefender->setDamage(iUnitDamage, getOwner());

	return true;
}

bool CvUnit::canRangeStrike() const
{
	if (getDomainType() == DOMAIN_AIR)
		return false;
	if (airRange() <= 0)
		return false;
	if (airBaseCombatStr() <= 0)
		return false;
	if (!canFight())
		return false;
	if (//isMadeAttack() && !isBlitz()
		isMadeAllAttacks()) // advc.164
	{
		return false;
	}
	if (!canMove() && getMoves() > 0)
		return false;
	return true;
}

bool CvUnit::canRangeStrikeAt(const CvPlot* pPlot, int iX, int iY) const
{
	if (!canRangeStrike())
		return false;

	CvPlot* pTargetPlot = GC.getMap().plot(iX, iY);
	if (pTargetPlot == NULL)
		return false;

	if (!pPlot->isVisible(getTeam()))
		return false;
	/*  UNOFFICIAL_PATCH (Bugfix), 05/10/10, jdog5000: START
		Need to check target plot too */
	if (!pTargetPlot->isVisible(getTeam()))
		return false;
	// UNOFFICIAL_PATCH: END
	if (plotDistance(pPlot, pTargetPlot) > airRange())
		return false;

	CvUnit* pDefender = airStrikeTarget(*pTargetPlot);
	if (pDefender == NULL)
		return false;

	/*	advc.rstr: The facing direction shouldn't matter. If we want to check for
		obstacles in the line of sight, GC.getMap().directionXY(*pPlot, *pTargetPlot)
		could be used instead of getFacingDirection, but a strike at range 2 should
		arguably represent indirect fire. */
	/*if (!pPlot->canSeePlot(pTargetPlot, getTeam(), airRange(), getFacingDirection(true)))
		return false;*/

	return true;
}


bool CvUnit::rangeStrike(int iX, int iY)
{
	CvPlot* pPlot = GC.getMap().plot(iX, iY);
	if (pPlot == NULL)
	{
		FAssertMsg(pPlot != NULL, "Range strike off the map"); // advc
		return false;
	}
	/*if (!canRangeStrikeAt(pPlot, iX, iY))
		return false;*/ // BtS
	// UNOFFICIAL_PATCH (Bugfix), 05/10/10, jdog5000
	if (!canRangeStrikeAt(plot(), iX, iY))
	{
		return false;
	} // UNOFFICIAL_PATCH: END

	CvUnit* pDefender = airStrikeTarget(*pPlot);

	FAssert(pDefender != NULL);
	FAssert(pDefender->canDefend());

	if (GC.getDefineINT("RANGED_ATTACKS_USE_MOVES") == 0)
	{
		setMadeAttack(true);
	}
	changeMoves(GC.getMOVE_DENOMINATOR());

	int iDamage = rangeCombatDamage(pDefender);

	int iUnitDamage = std::max(pDefender->getDamage(),
			std::min(pDefender->getDamage() + iDamage, airCombatLimit()));

	CvWString szBuffer(gDLL->getText("TXT_KEY_MISC_YOU_ARE_ATTACKED_BY_AIR",
			pDefender->getNameKey(), getNameKey(),
			// advc.004g:
			((iUnitDamage - pDefender->getDamage()) * 100) / pDefender->maxHitPoints()));
	//red icon over attacking unit
	gDLL->UI().addMessage(pDefender->getOwner(), false, -1, szBuffer, getPlot(),
			"AS2D_COMBAT", MESSAGE_TYPE_INFO, getButton(), GC.getColorType("RED"));
	//white icon over defending unit
	gDLL->UI().addMessage(pDefender->getOwner(), false, 0, L"", pDefender->getPlot(),
			"AS2D_COMBAT", MESSAGE_TYPE_DISPLAY_ONLY, pDefender->getButton());

	szBuffer = gDLL->getText("TXT_KEY_MISC_YOU_ATTACK_BY_AIR", getNameKey(), pDefender->getNameKey(),
			// advc.004g:
			((iUnitDamage - pDefender->getDamage()) * 100) / pDefender->maxHitPoints());
	gDLL->UI().addMessage(getOwner(), true, -1, szBuffer, *pPlot,
			"AS2D_COMBAT", MESSAGE_TYPE_INFO, pDefender->getButton(), GC.getColorType("GREEN"));

	collateralCombat(pPlot, pDefender);

	//set damage but don't update entity damage visibility
	pDefender->setDamage(iUnitDamage, getOwner(), false);

	if (pPlot->isActiveVisible(false))
	{
		// Range strike entity mission
		CvMissionDefinition kDefiniton;
		kDefiniton.setMissionTime(GC.getInfo(MISSION_RANGE_ATTACK).getTime() * gDLL->getSecsPerTurn());
		kDefiniton.setMissionType(MISSION_RANGE_ATTACK);
		kDefiniton.setPlot(pDefender->plot());
		kDefiniton.setUnit(BATTLE_UNIT_ATTACKER, this);
		kDefiniton.setUnit(BATTLE_UNIT_DEFENDER, pDefender);
		gDLL->getEntityIFace()->AddMission(&kDefiniton);

		//delay death
		// UNOFFICIAL_PATCH (Bugfix), 05/10/10, jdog5000
		// mission timer is not used like this in any other part of code, so it might cause OOS
		// issues ... at worst I think unit dies before animation is complete, so no real
		// harm in commenting it out.
		//pDefender->getGroup()->setMissionTimer(GC.getInfo(MISSION_RANGE_ATTACK).getTime()); // BtS
	}

	return true;
}

//------------------------------------------------------------------------------------------------
// FUNCTION:    CvUnit::planBattle
//! \brief      Determines in general how a battle will progress.
//!
//!				Note that the outcome of the battle is not determined here. This function plans
//!				how many sub-units die and in which 'rounds' of battle.
//! \param      kBattle The battle definition, which receives the battle plan.
//! \param		combat_log The order and amplitude of damage taken by the units (K-Mod)
//! \retval     The number of game turns that the battle should be given.
//------------------------------------------------------------------------------------------------

// Rewritten for K-Mod!
int CvUnit::planBattle(CvBattleDefinition& kBattle, const std::vector<int>& combat_log_argument) const
{
	const int BATTLE_TURNS_SETUP = 4;
	const int BATTLE_TURNS_ENDING = 4;
	const int BATTLE_TURNS_MELEE = 6;
	/*const int BATTLE_TURNS_RANGED = 6;
	const int BATTLE_TURN_RECHECK = 4;*/ // advc: unused

	CvUnit* pAttackUnit = kBattle.getUnit(BATTLE_UNIT_ATTACKER);
	CvUnit* pDefenceUnit = kBattle.getUnit(BATTLE_UNIT_DEFENDER);

	int iAttackerDamage = kBattle.getDamage(BATTLE_UNIT_ATTACKER, BATTLE_TIME_BEGIN);
	int iDefenderDamage = kBattle.getDamage(BATTLE_UNIT_DEFENDER, BATTLE_TIME_BEGIN);

	int iAttackerUnits = pAttackUnit->getSubUnitsAlive(iAttackerDamage);
	int iDefenderUnits = pDefenceUnit->getSubUnitsAlive(iDefenderDamage);
	int iAttackerUnitsKilled = 0;
	int iDefenderUnitsKilled = 0;

	// some hackery to ensure that we don't have to deal with an empty combat log...
	const std::vector<int> dummy_log(1, 0);
	const std::vector<int>& combat_log = combat_log_argument.size() == 0 ? dummy_log : combat_log_argument;
	FAssert(combat_log.size() > 0);
	// now we can just use 'combat_log' without having to worry about it being empty.

	//
	kBattle.setNumRangedRounds(0);
	kBattle.setNumMeleeRounds(0);
	kBattle.setDamage(BATTLE_UNIT_ATTACKER, BATTLE_TIME_RANGED, iAttackerDamage);
	kBattle.setDamage(BATTLE_UNIT_DEFENDER, BATTLE_TIME_RANGED, iDefenderDamage);
	kBattle.clearBattleRounds();
	// kBattle.setNumRangedRounds(iFirstStrikeRounds); // originally max(iFirstStrikesDelta, iKills / iFirstStrikesDelta)
	// int iFirstStrikeRounds = kBattle.getFirstStrikes(BATTLE_UNIT_ATTACKER) + kBattle.getFirstStrikes(BATTLE_UNIT_DEFENDER);
	bool bRanged = true;

	static const int iStandardNumRounds = GC.getDefineINT("STANDARD_BATTLE_ANIMATION_ROUNDS", 6);
	// <advc.002m>
	static const int iPerEraNumRounds = GC.getDefineINT("PER_ERA_BATTLE_ANIMATION_ROUNDS");
	CvGame const& kGame = GC.getGame();
	bool const bNetworkedMP = kGame.isNetworkMultiPlayer();
	/*  I prefer using the player era, but karadoc's comment at the end of
		this function suggests that this could cause OOS problems. */
	int const iEra = (bNetworkedMP ? kGame.getCurrentEra() :
			GET_PLAYER(kGame.getActivePlayer()).getCurrentEra());
	int iBaseRounds = iStandardNumRounds + iPerEraNumRounds * iEra;
	iBaseRounds = std::max(2, iBaseRounds);
	if(!bNetworkedMP && gDLL->getGraphicOption(GRAPHICOPTION_SINGLE_UNIT_GRAPHICS))
		iBaseRounds /= 2;
	int iTotalBattleRounds = (iBaseRounds * // </advc.002m>
		   (int)combat_log.size() * GC.getCOMBAT_DAMAGE() + GC.getMAX_HIT_POINTS()) /
		   (2*GC.getMAX_HIT_POINTS());

	// Reduce number of rounds if both units have groupSize == 1, because nothing much happens in those battles.
	if (pAttackUnit->getGroupSize() == 1 && pDefenceUnit->getGroupSize() == 1)
		iTotalBattleRounds = (2*iTotalBattleRounds+1)/3;

	// apparently, there is a hardcoded minimum of 2 rounds. (game will crash if there less than 2 rounds.)
	iTotalBattleRounds = range(iTotalBattleRounds, 2, 10);

	int iBattleRound = 0;
	for (int i = 0; i < (int)combat_log.size(); i++)
	{
		// The combat animator can't handle rounds where there are more deaths on one side than survivers on the other.
		// therefore, we must sometimes end the round early to avoid violating that rule.
		if (combat_log[i] > 0)
		{
			iDefenderDamage = std::min(GC.getMAX_HIT_POINTS(), iDefenderDamage + combat_log[i]);
			iDefenderUnitsKilled = std::min(iAttackerUnits - iAttackerUnitsKilled, iDefenderUnits - pDefenceUnit->getSubUnitsAlive(iDefenderDamage));
			bRanged = bRanged && pAttackUnit->isRanged();
			if (bRanged)
				kBattle.addDamage(BATTLE_UNIT_DEFENDER, BATTLE_TIME_RANGED, combat_log[i]); // I'm not sure if this is actually used for the animation...
		}
		else if (combat_log[i] < 0)
		{
			iAttackerDamage = std::min(GC.getMAX_HIT_POINTS(), iAttackerDamage - combat_log[i]);
			iAttackerUnitsKilled = std::min(iDefenderUnits - iDefenderUnitsKilled, iAttackerUnits - pAttackUnit->getSubUnitsAlive(iAttackerDamage));
			bRanged = bRanged && pDefenceUnit->isRanged();
			if (bRanged)
				kBattle.addDamage(BATTLE_UNIT_DEFENDER, BATTLE_TIME_RANGED, combat_log[i]);
		}

		// Sometimes we may need to end more than one round at a time...
		bool bNextRound = false;
		do
		{
			bNextRound = iBattleRound < (i+1) * iTotalBattleRounds / (int)combat_log.size();

			// force the round to end if we are already at the deaths limit for whomever will take the next damage.
			if (!bNextRound && (iDefenderUnitsKilled > 0 || iAttackerUnitsKilled > 0))
			{
				if (i+1 == combat_log.size() ||
					// kmodx: Added parentheses
					(iDefenderUnitsKilled >= iAttackerUnits - iAttackerUnitsKilled && combat_log[i] > 0) ||
					(iAttackerUnitsKilled >= iDefenderUnits - iDefenderUnitsKilled && combat_log[i] < 0))
				{
					bNextRound = true;
				}
			}

			if (bNextRound)
			{
				//bRanged = bRanged && (i < iFirstStrikeRounds || (pAttackUnit->isRanged() && pDefenceUnit->isRanged()));

				if (bRanged)
					kBattle.addNumRangedRounds(1);
				else
					kBattle.addNumMeleeRounds(1);

				//
				CvBattleRound kRound;

				kRound.setRangedRound(bRanged);
				kRound.setWaveSize(computeWaveSize(bRanged, iAttackerUnits, iDefenderUnits));

				iAttackerUnits -= iAttackerUnitsKilled;
				iDefenderUnits -= iDefenderUnitsKilled;

				kRound.setNumAlive(BATTLE_UNIT_ATTACKER, iAttackerUnits);
				kRound.setNumAlive(BATTLE_UNIT_DEFENDER, iDefenderUnits);
				kRound.setNumKilled(BATTLE_UNIT_ATTACKER, iAttackerUnitsKilled);
				kRound.setNumKilled(BATTLE_UNIT_DEFENDER, iDefenderUnitsKilled);
				//

				kBattle.addBattleRound(kRound);

				iBattleRound++;
				// there may be some spillover kills if the round was forced...
				iDefenderUnitsKilled = iDefenderUnits - pDefenceUnit->getSubUnitsAlive(iDefenderDamage);
				iAttackerUnitsKilled = iAttackerUnits - pAttackUnit->getSubUnitsAlive(iAttackerDamage);
				// and if there are, we should increase the total number of rounds so that we can fit them in.
				if (iDefenderUnitsKilled > 0 || iAttackerUnitsKilled > 0)
					iTotalBattleRounds++;
			}
		} while (bNextRound);
	}
	//FAssert(iBattleRound == iTotalBattleRounds);
	FAssert(iAttackerDamage == kBattle.getDamage(BATTLE_UNIT_ATTACKER, BATTLE_TIME_END));
	FAssert(iDefenderDamage == kBattle.getDamage(BATTLE_UNIT_DEFENDER, BATTLE_TIME_END));

	FAssert(kBattle.getNumBattleRounds() >= 2);
	FAssert(verifyRoundsValid(kBattle));

	int extraTime = 0;

	// extra time for siege towers and surrendering leaders.
	if ((pAttackUnit->getLeaderUnitType() != NO_UNIT && pAttackUnit->isDead()) ||
		(pDefenceUnit->getLeaderUnitType() != NO_UNIT && pDefenceUnit->isDead()) ||
		pAttackUnit->showSiegeTower(pDefenceUnit))
	{
		extraTime = BATTLE_TURNS_MELEE;
	}

	// K-Mod note: the original code used:
	//   gDLL->getEntityIFace()->GetSiegeTower(pAttackUnit->getUnitEntity()) || gDLL->getEntityIFace()->GetSiegeTower(pDefenceUnit->getUnitEntity())
	// I've changed that to use showSiegeTower, because GetSiegeTower does not work for the Pitboss host, and therefore can cause OOS errors.

	int r = BATTLE_TURNS_SETUP + BATTLE_TURNS_ENDING +
			kBattle.getNumMeleeRounds() * BATTLE_TURNS_MELEE +
			kBattle.getNumRangedRounds() * BATTLE_TURNS_MELEE +
			extraTime;
	// <advc.002m>
	static int const iTruncate = GC.getDefineINT("TRUNCATE_ANIMATIONS");
	static int const iTruncateEra = GC.getDefineINT("TRUNCATE_ANIMATIONS_ERA");
	static int const iTruncateTurns = std::max(2, GC.getDefineINT("TRUNCATE_ANIMATION_TURNS"));
	if(iTruncate <= 0 || iEra < iTruncateEra)
		return r;
	bool bHumanDefense = pDefenceUnit->isHuman();
	if(iTruncate < 3 && (iTruncate == 1 != bHumanDefense))
		return r;
	return std::min(iTruncateTurns, r);
	// </advc.002m>
}

//------------------------------------------------------------------------------------------------
// FUNCTION:	CvBattleManager::computeDeadUnits
//! \brief		Computes the number of units dead, for either the ranged or melee portion of combat.
//! \param		kDefinition The battle definition.
//! \param		bRanged true if computing the number of units that die during the ranged portion of combat,
//!					false if computing the number of units that die during the melee portion of combat.
//! \param		iUnit The index of the unit to compute (BATTLE_UNIT_ATTACKER or BATTLE_UNIT_DEFENDER).
//! \retval		The number of units that should die for the given unit in the given portion of combat
//------------------------------------------------------------------------------------------------
// advc.003j (comment): Obsolete b/c of the K-Mod rewrite of planBattle
int CvUnit::computeUnitsToDie(const CvBattleDefinition & kDefinition, bool bRanged, BattleUnitTypes iUnit) const
{
	FAssertMsg( iUnit == BATTLE_UNIT_ATTACKER || iUnit == BATTLE_UNIT_DEFENDER, "Invalid unit index");

	BattleTimeTypes iBeginIndex = bRanged ? BATTLE_TIME_BEGIN : BATTLE_TIME_RANGED;
	BattleTimeTypes iEndIndex = bRanged ? BATTLE_TIME_RANGED : BATTLE_TIME_END;
	return kDefinition.getUnit(iUnit)->getSubUnitsAlive(kDefinition.getDamage(iUnit, iBeginIndex)) -
		kDefinition.getUnit(iUnit)->getSubUnitsAlive( kDefinition.getDamage(iUnit, iEndIndex));
}

//------------------------------------------------------------------------------------------------
// FUNCTION:    CvUnit::verifyRoundsValid
//! \brief      Verifies that all rounds in the battle plan are valid
//! \param      vctBattlePlan The battle plan
//! \retval     true if the battle plan (seems) valid, false otherwise
//------------------------------------------------------------------------------------------------
bool CvUnit::verifyRoundsValid(const CvBattleDefinition & battleDefinition) const
{
	for(int i = 0; i < battleDefinition.getNumBattleRounds(); i++)
	{
		if(!battleDefinition.getBattleRound(i).isValid())
			return false;
	}
	return true;
}

//------------------------------------------------------------------------------------------------
// FUNCTION:    CvUnit::increaseBattleRounds
//! \brief      Increases the number of rounds in the battle.
//! \param      kBattleDefinition The definition of the battle
//------------------------------------------------------------------------------------------------
// advc.003j (comment): Obsolete b/c of the K-Mod rewrite of planBattle
void CvUnit::increaseBattleRounds(CvBattleDefinition & kBattleDefinition) const
{
	if (kBattleDefinition.getUnit(BATTLE_UNIT_ATTACKER)->isRanged() && kBattleDefinition.getUnit(BATTLE_UNIT_DEFENDER)->isRanged())
	{
		kBattleDefinition.addNumRangedRounds(1);
	}
	else
	{
		kBattleDefinition.addNumMeleeRounds(1);
	}
}

//------------------------------------------------------------------------------------------------
// FUNCTION:    CvUnit::computeWaveSize
//! \brief      Computes the wave size for the round.
//! \param      bRangedRound true if the round is a ranged round
//! \param		iAttackerMax The maximum number of attackers that can participate in a wave (alive)
//! \param		iDefenderMax The maximum number of Defenders that can participate in a wave (alive)
//! \retval     The desired wave size for the given parameters
//------------------------------------------------------------------------------------------------
int CvUnit::computeWaveSize(bool bRangedRound, int iAttackerMax, int iDefenderMax) const
{
	FAssertMsg(getCombatUnit() != NULL, "You must be fighting somebody!");
	int aiDesiredSize[BATTLE_UNIT_COUNT];
	if (bRangedRound)
	{
		aiDesiredSize[BATTLE_UNIT_ATTACKER] = m_pUnitInfo->getRangedWaveSize();
		aiDesiredSize[BATTLE_UNIT_DEFENDER] = getCombatUnit()->getUnitInfo().getRangedWaveSize();
	}
	else
	{
		aiDesiredSize[BATTLE_UNIT_ATTACKER] = m_pUnitInfo->getMeleeWaveSize();
		aiDesiredSize[BATTLE_UNIT_DEFENDER] = getCombatUnit()->getUnitInfo().getMeleeWaveSize();
	}

	aiDesiredSize[BATTLE_UNIT_DEFENDER] = aiDesiredSize[BATTLE_UNIT_DEFENDER] <= 0 ? iDefenderMax : aiDesiredSize[BATTLE_UNIT_DEFENDER];
	aiDesiredSize[BATTLE_UNIT_ATTACKER] = aiDesiredSize[BATTLE_UNIT_ATTACKER] <= 0 ? iDefenderMax : aiDesiredSize[BATTLE_UNIT_ATTACKER];
	return std::min(std::min( aiDesiredSize[BATTLE_UNIT_ATTACKER], iAttackerMax), std::min(aiDesiredSize[BATTLE_UNIT_DEFENDER],
		iDefenderMax));
}

bool CvUnit::isTargetOf(CvUnit const& kAttacker) const
{
	CvUnitInfo const& kAttackerInfo = kAttacker.getUnitInfo();
	//if (!getPlot().isCity(true, getTeam()))
	if (!GET_TEAM(getTeam()).isCityDefense(getPlot(), // advc
		kAttacker.getTeam())) // advc.183
	{
		if (getUnitClassType() != NO_UNITCLASS &&
			kAttackerInfo.getTargetUnitClass(getUnitClassType()))
		{
			return true;
		}
		if (getUnitCombatType() != NO_UNITCOMBAT &&
			kAttackerInfo.getTargetUnitCombat(getUnitCombatType()))
		{
			return true;
		}
	}

	if (kAttackerInfo.getUnitClassType() != NO_UNITCLASS &&
		m_pUnitInfo->getDefenderUnitClass(kAttackerInfo.getUnitClassType()))
	{
		return true;
	}
	if (kAttackerInfo.getUnitCombatType() != NO_UNITCOMBAT &&
		m_pUnitInfo->getDefenderUnitCombat(kAttackerInfo.getUnitCombatType()))
	{
		return true;
	}

	return false;
}

/*	advc (note): Says whether this unit's combat owner in kPlot
	as viewed by eTeam is hostile to eTeam (same as in BtS).
	advc.opt: This needs to be faster. So pPlot==NULL and eTeam==NO_TEAM
	are no longer allowed. */
bool CvUnit::isEnemy(TeamTypes eTeam, CvPlot const& kPlot) const
{
	return GET_TEAM(eTeam).isAtWar(TEAMID(getCombatOwner(eTeam, kPlot)));
}

// advc.opt: Separate function for potentially unowned plot
bool CvUnit::isEnemy(CvPlot const& kPlot) const
{
	TeamTypes const ePlotTeam = kPlot.getTeam();
	return (ePlotTeam != NO_TEAM && isEnemy(ePlotTeam, kPlot));
}


bool CvUnit::isSuicide() const
{
	return (m_pUnitInfo->isSuicide() || getKamikazePercent() != 0);
}


void CvUnit::getDefenderCombatValues(CvUnit const& kDefender, CvPlot const* pPlot,
	int iOurStrength, int iOurFirepower,
	int& iTheirOdds, int& iTheirStrength, int& iOurDamage, int& iTheirDamage,
	CombatDetails* pTheirDetails) const
{
	iTheirStrength = kDefender.currCombatStr(pPlot, this, pTheirDetails);
	int iTheirFirepower = kDefender.currFirepower(pPlot, this);

	FAssert(iOurStrength + iTheirStrength > 0);
	FAssert(iOurFirepower + iTheirFirepower > 0);

	iTheirOdds = (GC.getCOMBAT_DIE_SIDES() * iTheirStrength) / (iOurStrength + iTheirStrength);
	if (kDefender.isBarbarian())
	{
		if (GET_PLAYER(getOwner()).getWinsVsBarbs() <
			GET_PLAYER(getOwner()).getFreeWinsVsBarbs())
		{
			iTheirOdds = std::min((10 * GC.getCOMBAT_DIE_SIDES()) / 100, iTheirOdds);
		}
	}
	if (isBarbarian())
	{
		if (GET_PLAYER(kDefender.getOwner()).getWinsVsBarbs() <
			GET_PLAYER(kDefender.getOwner()).getFreeWinsVsBarbs())
		{
			iTheirOdds =  std::max((90 * GC.getCOMBAT_DIE_SIDES()) / 100, iTheirOdds);
		}
	}

	int iStrengthFactor = (iOurFirepower + iTheirFirepower + 1) / 2;

	iOurDamage = std::max(1, ((GC.getCOMBAT_DAMAGE() * (iTheirFirepower + iStrengthFactor)) /
			(iOurFirepower + iStrengthFactor)));
	iTheirDamage = std::max(1, ((GC.getCOMBAT_DAMAGE() * (iOurFirepower + iStrengthFactor)) /
			(iTheirFirepower + iStrengthFactor)));
}


int CvUnit::getTriggerValue(EventTriggerTypes eTrigger, const CvPlot* pPlot, bool bCheckPlot) const
{
	CvEventTriggerInfo& kTrigger = GC.getInfo(eTrigger);
	if (kTrigger.getNumUnits() <= 0 || isDead() ||
		!GC.getPythonCaller()->canTriggerEvent(*this, eTrigger))
	{
		return MIN_INT;
	}
	if (kTrigger.getNumUnitsRequired() > 0)
	{
		bool bFoundValid = false;
		for (int i = 0; i < kTrigger.getNumUnitsRequired(); ++i)
		{
			if (getUnitClassType() == kTrigger.getUnitRequired(i))
			{
				bFoundValid = true;
				break;
			}
		}

		if (!bFoundValid)
			return MIN_INT;
	}

	if (bCheckPlot)
	{
		if (kTrigger.isUnitsOnPlot())
		{
			if (!getPlot().canTrigger(eTrigger, getOwner()))
				return MIN_INT;
		}
	}

	int iValue = 0;

	if (getDamage() == 0 && kTrigger.getUnitDamagedWeight() > 0)
		return MIN_INT;

	iValue += getDamage() * kTrigger.getUnitDamagedWeight();
	iValue += getExperience() * kTrigger.getUnitExperienceWeight();

	if (pPlot != NULL)
	{
		iValue += plotDistance(getX(), getY(), pPlot->getX(), pPlot->getY()) *
				kTrigger.getUnitDistanceWeight();
	}

	return iValue;
}


bool CvUnit::canApplyEvent(EventTypes eEvent) const
{
	CvEventInfo& kEvent = GC.getInfo(eEvent);

	if (kEvent.getUnitExperience() != 0)
	{
		if (!canAcquirePromotionAny())
			return false;
	}

	if (NO_PROMOTION != kEvent.getUnitPromotion())
	{
		if (!canAcquirePromotion((PromotionTypes)kEvent.getUnitPromotion()))
			return false;
	}

	if (kEvent.getUnitImmobileTurns() > 0)
	{
		if (!canAttack() ||
			m_pUnitInfo->isMostlyDefensive()) // advc.315: Farm Bandits and Toxcatl random events
		{
			return false;
		}
	}

	return true;
}


void CvUnit::applyEvent(EventTypes eEvent)
{
	if (!canApplyEvent(eEvent))
		return;

	CvEventInfo& kEvent = GC.getInfo(eEvent);

	if (kEvent.getUnitExperience() != 0)
	{
		setDamage(0);
		changeExperience(kEvent.getUnitExperience());
	}

	if (kEvent.getUnitPromotion() != NO_PROMOTION)
		setHasPromotion((PromotionTypes)kEvent.getUnitPromotion(), true);

	if (kEvent.getUnitImmobileTurns() > 0)
	{
		changeImmobileTimer(kEvent.getUnitImmobileTurns());
		CvWString szText = gDLL->getText("TXT_KEY_EVENT_UNIT_IMMOBILE",
				getNameKey(), kEvent.getUnitImmobileTurns());
		gDLL->UI().addMessage(getOwner(), false, -1, szText, getPlot(), "AS2D_UNITGIFTED",
				MESSAGE_TYPE_INFO, getButton(), GC.getColorType("UNIT_TEXT"));
	}

	CvWString szNameKey(kEvent.getUnitNameKey());

	if (!szNameKey.empty())
		setName(gDLL->getText(kEvent.getUnitNameKey()));

	if (kEvent.isDisbandUnit())
		kill(false);
}


const CvArtInfoUnit* CvUnit::getArtInfo(int i, EraTypes eEra) const
{
    // doc: dynamic art style for minors based on origin region
	if (isIndependent() || isNative() || isBarbarian())
	    return getUnitInfo().getArtInfo(i, eEra, getOriginalArtStyle());
	return m_pUnitInfo->getArtInfo(i, eEra, (UnitArtStyleTypes)
			GC.getInfo(getCivilizationType()).getUnitArtStyleType());
}


const TCHAR* CvUnit::getButton() const
{
	const CvArtInfoUnit* pArtInfo = getArtInfo(0, GET_PLAYER(getOwner()).getCurrentEra());
	if (NULL != pArtInfo)
		return pArtInfo->getButton();
	return m_pUnitInfo->getButton();
}


int CvUnit::getGroupSize() const
{
	return m_pUnitInfo->getGroupSize();
}


int CvUnit::getGroupDefinitions() const
{
	return m_pUnitInfo->getGroupDefinitions();
}


int CvUnit::getUnitGroupRequired(int i) const
{
	return m_pUnitInfo->getUnitGroupRequired(i);
}


bool CvUnit::isRenderAlways() const
{
	return m_pUnitInfo->isRenderAlways();
}


float CvUnit::getAnimationMaxSpeed() const
{
	return m_pUnitInfo->getUnitMaxSpeed();
}


float CvUnit::getAnimationPadTime() const
{
	return m_pUnitInfo->getUnitPadTime();
}


const char* CvUnit::getFormationType() const
{
	return m_pUnitInfo->getFormationType();
}


bool CvUnit::isMechUnit() const
{
	return m_pUnitInfo->isMechUnit();
}


bool CvUnit::isRenderBelowWater() const
{
	return m_pUnitInfo->isRenderBelowWater();
}


int CvUnit::getRenderPriority(UnitSubEntityTypes eUnitSubEntity, int iMeshGroupType, int UNIT_MAX_SUB_TYPES) const
{
	if (eUnitSubEntity == UNIT_SUB_ENTITY_SIEGE_TOWER)
		return (getOwner() * (GC.getNumUnitInfos() + 2) * UNIT_MAX_SUB_TYPES) + iMeshGroupType;
	return (getOwner() * (GC.getNumUnitInfos() + 2) * UNIT_MAX_SUB_TYPES) + m_eUnitType * UNIT_MAX_SUB_TYPES + iMeshGroupType;
}

/*	advc: NULL argument no longer allowed; should call the inline version when the
	plot isn't known. */
bool CvUnit::isAlwaysHostile(CvPlot const& kPlot) const
{
	if (!m_pUnitInfo->isAlwaysHostile())
	    return false;

    // doc: different rules for land units
	if (kPlot.isOwned())
	{
	    if (getOwner() == kPlot.getOwner())
	        return false;

	    if (getDomainType() == DOMAIN_LAND && GET_TEAM(getTeam()).isOpenBorders(kPlot.getTeam()))
	        return false;
	}

	// advc (note): This prevents always-hostile units from attacking into friendly cities
	if (//pPlot != NULL && // advc.opt
		//kPlot.isCity(true, getTeam())
        getDomainType() != DOMAIN_LAND && // doc: different rules for land units
		GET_TEAM(getTeam()).isBase(kPlot)) // advc
	{
		return false;
	}
	return true;
}


bool CvUnit::verifyStackValid()
{
	if (!alwaysInvisible())
	{
		if (getPlot().isVisibleEnemyUnit(this))
			return jumpToNearestValidPlot();
	}
	return true;
}

//check if quick combat (in which case false is returned)
bool CvUnit::isCombatVisible(CvUnit const* pDefender,
	bool bSeaPatrol) const // advc.004k
{
	bool bVisible = false;
	if (!m_pUnitInfo->isQuickCombat())
	{
		if (pDefender == NULL || !pDefender->getUnitInfo().isQuickCombat())
		{
			if (isHuman())
			{
				if (!GET_PLAYER(getOwner()).isOption(PLAYEROPTION_QUICK_ATTACK) ||
					/*	<advc.004k> Attacker/ defender role is a bit jumbled when
						a sea patrol is triggered. Err on the side of slow combat. */
					(bSeaPatrol &&
					!GET_PLAYER(getOwner()).isOption(PLAYEROPTION_QUICK_DEFENSE)))
					// </advc.004k>
				{
					bVisible = true;
				}
			}
			else if (pDefender != NULL && pDefender->isHuman())
			{
				if (!GET_PLAYER(pDefender->getOwner()).isOption(PLAYEROPTION_QUICK_DEFENSE) &&
					!gDLL->getEngineIFace()->isGlobeviewUp() && // advc.102
					// advc.001: Camera won't catch AI-vs-human combat in Hotseat
					(isHuman() || !GC.getGame().isHotSeat()))
				{
					bVisible = true;
				}
			}
		}
	}
	return bVisible;
}

// used by the executable for the red glow and plot indicators
bool CvUnit::shouldShowEnemyGlow(TeamTypes eForTeam) const
{
	if (isDelayedDeath())
		return false;
	if (getDomainType() == DOMAIN_AIR)
		return false;
	if (!canFight())
		return false;

	CvPlot* pPlot = plot();
	if (pPlot == NULL)
		return false;

	TeamTypes ePlotTeam = pPlot->getTeam();
	if (ePlotTeam != eForTeam)
		return false;
	if (!isEnemy(ePlotTeam))
		return false;
	return true;
}


bool CvUnit::shouldShowFoundBorders() const
{
	//return isFound();
	// <advc.004h>
	if (BUGOption::isEnabled("MainInterface__FoundingYields", false))
		return isFound();
	return false; // </advc.004h>
}


void CvUnit::cheat(bool bCtrl, bool bAlt, bool bShift)
{
	//if (gDLL->getChtLvl() > 0)
	{
		if (bCtrl /* advc.007b: */ && GC.getGame().isDebugMode())
			setPromotionReady(true);
	}
}


float CvUnit::getHealthBarModifier() const
{
	return (GC.getDefineFLOAT("HEALTH_BAR_WIDTH") /
			(GC.getGame().getBestLandUnitCombat() * 2));
}


void CvUnit::getLayerAnimationPaths(std::vector<AnimationPathTypes>& aAnimationPaths) const
{
	FOR_EACH_ENUM(Promotion)
	{
		if (isHasPromotion(eLoopPromotion))
		{
			AnimationPathTypes eAnimationPath = (AnimationPathTypes)
					GC.getInfo(eLoopPromotion).getLayerAnimationPath();
			if(eAnimationPath != ANIMATIONPATH_NONE)
				aAnimationPaths.push_back(eAnimationPath);
		}
	}
}


int CvUnit::getSelectionSoundScript() const
{
	int iScriptId = getArtInfo(0, GET_PLAYER(getOwner()).getCurrentEra())->
			getSelectionSoundScriptId();
	if (iScriptId == -1)
		iScriptId = GC.getInfo(getCivilizationType()).getSelectionSoundScriptId();
	return iScriptId;
}

/*	BETTER_BTS_AI_MOD, Lead From Behind (UncutDragon), 02/21/10, jdog5000: START
	Original isBetterDefenderThan call (without the extra parameter) -
	now just a pass-through */
bool CvUnit::isBetterDefenderThan(const CvUnit* pDefender, const CvUnit* pAttacker) const
{
	return isBetterDefenderThan(pDefender, pAttacker, NULL);
}

/*	Modified version of best defender code (minus the initial boolean tests,
	which we still check in the original method) */
bool CvUnit::LFBisBetterDefenderThan(const CvUnit* pDefender, const CvUnit* pAttacker,
	int* pBestDefenderRank) const
{
	/*	We adjust ranking based on ratio of our adjusted strength compared to
		twice that of attacker. Effect is if we're over twice as strong as attacker,
		we increase our ranking (more likely to be picked as defender) -
		otherwise, we reduce our ranking (less likely) */
	// Get our adjusted rankings based on combat odds
	int iOurRanking = LFBgetDefenderRank(pAttacker);
	int iTheirRanking = -1;
	if (pBestDefenderRank != NULL)
		iTheirRanking = *pBestDefenderRank;
	if (iTheirRanking == -1)
		iTheirRanking = pDefender->LFBgetDefenderRank(pAttacker);
	/*	In case of equal value, fall back on unit cycle order
		(K-Mod. _reversed_ unit cycle order, so that inexperienced units defend first.) */
	if (iOurRanking == iTheirRanking)
	{
		if (isBeforeUnitCycle(*pDefender))
			iTheirRanking++;
		else iTheirRanking--;
	}
	// Retain the basic rank (before value adjustment) for the best defender
	if (pBestDefenderRank != NULL)
	{
		if (iOurRanking > iTheirRanking)
			(*pBestDefenderRank) = iOurRanking;
	}
	return (iOurRanking > iTheirRanking);
}

// Get the (adjusted) odds of attacker winning to use in deciding best attacker
int CvUnit::LFBgetAttackerRank(const CvUnit* pDefender, int& iUnadjustedRank) const
{
	if (pDefender != NULL)
	{
		int iDefOdds = pDefender->LFBgetDefenderOdds(this);
		iUnadjustedRank = 1000 - iDefOdds;
		// If attacker has a chance to withdraw, factor that in as well
		if (withdrawalProbability() > 0)
			iUnadjustedRank += ((iDefOdds * withdrawalProbability()) / 100);
	}
	else
	{
		// No defender ... just use strength, but try to make it a number out of 1000
		iUnadjustedRank = currCombatStr(NULL, NULL) / 5;
	}
	return LFBgetValueAdjustedOdds(iUnadjustedRank, false);
}

// Get the (adjusted) odds of defender winning to use in deciding best defender
int CvUnit::LFBgetDefenderRank(const CvUnit* pAttacker) const
{
	int iRank = LFBgetDefenderOdds(pAttacker);
	// Don't adjust odds for value if attacker is limited in their damage (i.e: no risk of death)
	if (pAttacker != NULL && maxHitPoints() <= pAttacker->combatLimit())
		iRank = LFBgetValueAdjustedOdds(iRank, true);
	return iRank;
}

// Get the unadjusted odds of defender winning (used for both best defender and best attacker)
int CvUnit::LFBgetDefenderOdds(const CvUnit* pAttacker) const
{
	// Check if we have a valid attacker
	bool bUseAttacker = false;
	int iAttStrength = 0;
	if (pAttacker != NULL)
		iAttStrength = pAttacker->currCombatStr();
	if (iAttStrength > 0)
		bUseAttacker = true;

	int iDefense = 0;

	if (bUseAttacker && GC.getDefineBOOL(CvGlobals::LFB_USECOMBATODDS))
	{
		// We start with straight combat odds
		// advc: Replacing call to deleted (and redundant) LFBgetDefenderCombatOdds
		iDefense = 1000 - calculateCombatOdds(*pAttacker, *this);
	}
	else
	{
		// Lacking a real opponent (or if combat odds turned off) fall back on just using strength
		iDefense = currCombatStr(plot(), pAttacker);
		if (bUseAttacker)
		{
			// Similiar to the standard method, except I reduced the affect (cut it in half) handle attacker
			// and defender together (instead of applying one on top of the other) and substract the
			// attacker first strikes (instead of adding attacker first strikes when defender is immune)
			int iFirstStrikes = 0;

			if (!pAttacker->immuneToFirstStrikes())
				iFirstStrikes += firstStrikes() * 2 + chanceFirstStrikes();
			if (!immuneToFirstStrikes())
				iFirstStrikes -= pAttacker->firstStrikes() * 2 + pAttacker->chanceFirstStrikes();

			if (iFirstStrikes != 0)
			{
				// With COMBAT_DAMAGE=20, this makes each first strike worth 8% (and each chance worth 4%)
				iDefense *= (iFirstStrikes * GC.getCOMBAT_DAMAGE()) / 5 + 100;
				iDefense /= 100;
			}

			// Make it a number out of 1000, taking attacker into consideration
			iDefense = (iDefense * 1000) / (iDefense + iAttStrength);
		}
	}
	/*	This part is taken directly from the standard method
		Reduces value if a unit is carrying other units */
	/*if (hasCargo()) {
		int iAssetValue = std::max(1, m_pUnitInfo->getAssetValue());
		int iCargoAssetValue = 0;
		std::vector<CvUnit*> aCargoUnits;
		getCargoUnits(aCargoUnits);
		for (uint i = 0; i < aCargoUnits.size(); ++i)
			iCargoAssetValue += aCargoUnits[i]->getUnitInfo().getAssetValue();
		iDefense = iDefense * iAssetValue / std::max(1, iAssetValue + iCargoAssetValue);
	}*/
	/*	K-Mod. The above code does not achieve the goal, which is to
		protect cargo-carrying ships from being killed first.
		The problem with the code is that when the odds of winning are very small,
		the artificial reduction is also very small; on the other hand,
		when the odds of winning are very great, the artificial reduction is huge.
		This is the opposite of what we want! We want to let the boats fight
		if they are going to win anyway, but give them protection if they would lose.
		I've added my own version of the value adjustment to LFBgetValueAdjustedOdds. */
	return iDefense;
}

// Take the unadjusted odds and adjust them based on unit value
int CvUnit::LFBgetValueAdjustedOdds(int iOdds, bool bDefender) const
{
	// Adjust odds based on value
	int iValue = LFBgetRelativeValueRating();
	// K-Mod: if we are defending, then let those with defensive promotions fight!
	if (bDefender)
	{
		int iDef = LFGgetDefensiveValueAdjustment();
		// I'm a little bit concerned that if a unit gets a bunch of promotions with an xp discount,
		// that unit may end up being valued less than a completely inexperienced unit.
		// Thus the experienced unit may end up being sacrificed to protect the rookie.

		iValue -= iDef;
		iValue = std::max(0, iValue);
	}
	// K-Mod end
	int iAdjustment = -250; // advc: Was long, which is pointless. Seems like long long isn't needed.
	if (GC.getDefineBOOL(CvGlobals::LFB_USESLIDINGSCALE))
		iAdjustment = (iOdds - 990);
	// Value Adjustment = (odds-990)*(value*num/denom)^2
	//long iValueAdj = (long)(iValue * GC.getDefineINT(CvGlobals::LFBAdjustNumerator));
	int iValueAdj = iValue * GC.getDefineINT(CvGlobals::LFB_ADJUSTNUMERATOR); // advc
	//iValueAdj *= iValueAdj;
	iValueAdj *= iAdjustment;
	FAssertMsg(iValueAdj < MAX_INT / 100, "Dangerously close to overflow"); // advc.test
	//iValueAdj /= (long)(GC.getLFBAdjustDenominator() * GC.getLFBAdjustDenominator());
	iValueAdj /= GC.getDefineINT(CvGlobals::LFB_ADJUSTDENOMINATOR);
	int iRank = iOdds + iValueAdj + 10000;
	// Note that the +10000 is just to try keeping it > 0 - doesn't really matter, other than that -1
	// would be interpreted later as not computed yet, which would cause us to compute it again each time

	// K-Mod. If this unit is a transport, reduce the value based on the risk of losing the cargo.
	// (This replaces the adjustment from LFBgetDefenderOdds. For more info, see the comments in that function.)
	if (hasCargo())
	{
		int iAssetValue = std::max(1, m_pUnitInfo->getAssetValue());
		int iCargoAssetValue = 0;
		std::vector<CvUnit*> aCargoUnits;
		getCargoUnits(aCargoUnits);
		for (uint i = 0; i < aCargoUnits.size(); ++i)
		{
			iCargoAssetValue += aCargoUnits[i]->getUnitInfo().getAssetValue();
		}
		iRank -= 2 * (1000 - iOdds) * iCargoAssetValue / std::max(1, iAssetValue + iCargoAssetValue);
	}
	// K-Mod end

	return iRank;
}

// Method to evaluate the value of a unit relative to another
int CvUnit::LFBgetRelativeValueRating() const
{
	int iValueRating = 0;

	// Check if led by a Great General
	if (GC.getDefineINT(CvGlobals::LFB_BASEDONGENERAL) > 0)
		if (NO_UNIT != getLeaderUnitType())
			iValueRating += GC.getDefineINT(CvGlobals::LFB_BASEDONGENERAL);

	// Assign experience value in tiers
	// (formula changed for K-Mod)
	if (GC.getDefineINT(CvGlobals::LFB_BASEDONEXPERIENCE) > 0)
	{
		//int iTier = 10;
		int iTier = getLevel();
		//while (getExperience() >= iTier)
		while (getExperience() >= iTier*iTier+1)
		{
			//iValueRating += GC.getLFBBasedOnExperience();
			//iTier *= 2;
			iTier++;
		}
		//iValueRating += std::max(getLevel(), iTier) * GC.getLFBBasedOnExperience();
		iValueRating += iTier * GC.getDefineINT(CvGlobals::LFB_BASEDONEXPERIENCE);
	}

	// Check if unit is limited in how many can exist
	if (GC.getDefineINT(CvGlobals::LFB_BASEDONLIMITED) > 0)
	{
		if (m_pUnitInfo->isLimited())
			iValueRating += GC.getDefineINT(CvGlobals::LFB_BASEDONLIMITED);
	}
	// Check if unit has ability to heal
	if (GC.getDefineINT(CvGlobals::LFB_BASEDONHEALER) > 0)
	{
		if (getSameTileHeal() > 0)
			iValueRating += GC.getDefineINT(CvGlobals::LFB_BASEDONHEALER);
	}
	return iValueRating;
} // BETTER_BTS_AI_MOD: END

/*	K-Mod: unit value adjustment based on how many defensive promotions are active on this plot.
	(The purpose of this is to encourage experienced units to fight when their promotions
	are especially suited to the plot they are defending.) */
int CvUnit::LFGgetDefensiveValueAdjustment() const
{
	int iValue = 0;

	FOR_EACH_ENUM2(Promotion, ePromo)
	{
		if (!isHasPromotion(ePromo))
			continue;
		CvPromotionInfo const& kPromo = GC.getInfo(ePromo);
		bool bDefensive = false;
		// Cities and hills
		if ((kPromo.getCityDefensePercent() > 0 && getPlot().isCity()) ||
			(kPromo.getHillsDefensePercent() > 0 && getPlot().isHills()))
		{
			bDefensive = true;
		}
		// Features
		if (!bDefensive)
		{
			FOR_EACH_ENUM(Feature)
			{
				if (kPromo.getFeatureDefensePercent(eLoopFeature) > 0 &&
					getPlot().getFeatureType() == eLoopFeature)
				{
					bDefensive = true;
					break;
				}
			}
		}
		// Terrain
		if (!bDefensive)
		{
			FOR_EACH_ENUM(Terrain)
			{
				if (kPromo.getTerrainDefensePercent(eLoopTerrain) > 0 &&
					getPlot().getTerrainType() == eLoopTerrain)
				{
					bDefensive = true;
					break;
				}
			}
		}
		if (bDefensive)
			iValue += GC.getDefineINT(CvGlobals::LFB_DEFENSIVEADJUSTMENT);
	}

	return iValue;
}

// doc
UnitArtStyleTypes CvUnit::getOriginalArtStyle() const
{
	switch (getOriginalRegion())
	{
	case REGION_BRITAIN:
	case REGION_IRELAND:
		return GC.getInfo(ENGLAND).getUnitArtStyleType();
	case REGION_ARIDOAMERICA:
	case REGION_CARIBBEAN:
	case REGION_MESOAMERICA:
	case REGION_CENTRAL_AMERICA:
		return GC.getInfo(AZTECS).getUnitArtStyleType();
	case REGION_NUBIA:
		return GC.getInfo(NUBIA).getUnitArtStyleType();
	case REGION_IBERIA:
		return GC.getInfo(SPAIN).getUnitArtStyleType();
	case REGION_ITALY:
	case REGION_BALKANS:
		if (GC.getGame().getGameTurnYear() > GC.getInfo(ITALY).getStartingYear())
			return GC.getInfo(ITALY).getUnitArtStyleType();
		return GC.getInfo(ROME).getUnitArtStyleType();
	case REGION_MAGHREB:
	case REGION_SAHARA:
		if (GC.getGame().getGameTurnYear() > GC.getInfo(ARABIA).getStartingYear())
			return GC.getCivilizationInfo(ARABIA).getUnitArtStyleType();
		return GC.getCivilizationInfo(CARTHAGE).getUnitArtStyleType();
	case REGION_FRANCE:
	case REGION_QUEBEC:
		return GC.getInfo(FRANCE).getUnitArtStyleType();
	case REGION_LOWER_GERMANY:
	case REGION_CENTRAL_EUROPE:
	case REGION_POLAND:
		return GC.getInfo(HOLY_ROME).getUnitArtStyleType();
	case REGION_SCANDINAVIA:
	case REGION_BALTICS:
		return GC.getInfo(NORSE).getUnitArtStyleType();
	case REGION_RUSSIA:
	case REGION_RUTHENIA:
	case REGION_EUROPEAN_ARCTIC:
	case REGION_VOLGA:
	case REGION_URALS:
	case REGION_SIBERIA:
		return GC.getInfo(RUSSIA).getUnitArtStyleType();
	case REGION_GREECE:
		return GC.getInfo(GREECE).getUnitArtStyleType();
	case REGION_ANATOLIA:
	case REGION_CAUCASUS:
		if (GC.getGame().getGameTurnYear() > GC.getInfo(OTTOMANS).getStartingYear())
		{
			return GC.getInfo(OTTOMANS).getUnitArtStyleType();
		}
		else if (GC.getGame().getGameTurnYear() > GC.getInfo(BYZANTIUM).getStartingYear())
		{
			return GC.getInfo(BYZANTIUM).getUnitArtStyleType();
		}
		return GC.getInfo(HITTITES).getUnitArtStyleType();
	case REGION_PERSIA:
	case REGION_KHORASAN:
	case REGION_TRANSOXIANA:
		return GC.getInfo(PERSIA).getUnitArtStyleType();
	case REGION_MESOPOTAMIA:
		if (GC.getGame().getGameTurnYear() > GC.getInfo(ARABIA).getStartingYear())
			return GC.getInfo(ARABIA).getUnitArtStyleType();
		return GC.getInfo(BABYLONIA).getUnitArtStyleType();
	case REGION_LEVANT:
		if (GC.getGame().getGameTurnYear() > GC.getInfo(ARABIA).getStartingYear())
			return GC.getInfo(ARABIA).getUnitArtStyleType();
		return GC.getInfo(CARTHAGE).getUnitArtStyleType();
	case REGION_ARABIA:
		return GC.getInfo(ARABIA).getUnitArtStyleType();
	case REGION_EGYPT:
		if (GC.getGame().getGameTurnYear() > GC.getInfo(ARABIA).getStartingYear())
			return GC.getInfo(ARABIA).getUnitArtStyleType();
		return GC.getInfo(EGYPT).getUnitArtStyleType();
	case REGION_SINDH:
	case REGION_PUNJAB:
	case REGION_HINDU_KUSH:
	case REGION_RAJPUTANA:
	case REGION_HINDUSTAN:
	case REGION_BENGAL:
		if (GC.getGame().getGameTurnYear() >= GC.getInfo(MUGHALS).getStartingYear())
			return GC.getInfo(MUGHALS).getUnitArtStyleType();
		return GC.getInfo(INDIA).getUnitArtStyleType();
	case REGION_DECCAN:
		return GC.getInfo(INDIA).getUnitArtStyleType();
	case REGION_DRAVIDA:
		return GC.getInfo(DRAVIDIA).getUnitArtStyleType();
	case REGION_INDOCHINA:
		return GC.getInfo(KHMER).getUnitArtStyleType();
	case REGION_INDONESIA:
	case REGION_PHILIPPINES:
		return GC.getInfo(JAVA).getUnitArtStyleType();
	case REGION_SOUTH_CHINA:
	case REGION_NORTH_CHINA:
	case REGION_TARIM_BASIN:
	case REGION_TIBET:
		return GC.getInfo(CHINA).getUnitArtStyleType();
	case REGION_KOREA:
		return GC.getInfo(KOREA).getUnitArtStyleType();
	case REGION_JAPAN:
		return GC.getInfo(JAPAN).getUnitArtStyleType();
	case REGION_MONGOLIA:
	case REGION_MANCHURIA:
	case REGION_AMUR:
	case REGION_CENTRAL_ASIAN_STEPPE:
		return GC.getInfo(MONGOLS).getUnitArtStyleType();
	case REGION_ETHIOPIA:
		return GC.getInfo(ETHIOPIA).getUnitArtStyleType();
	case REGION_HORN_OF_AFRICA:
	case REGION_SWAHILI_COAST:
	case REGION_GREAT_LAKES:
	case REGION_ZAMBEZI:
		return GC.getInfo(SWAHILI).getUnitArtStyleType();
	case REGION_MADAGASCAR:
		return GC.getInfo(POLYNESIA).getUnitArtStyleType();
	case REGION_CAPE:
	case REGION_KALAHARI:
	case REGION_CONGO:
		return GC.getInfo(CONGO).getUnitArtStyleType();
	case REGION_GUINEA:
	case REGION_SAHEL:
		return GC.getInfo(MALI).getUnitArtStyleType();
	}

	switch (CvPlot::getRegionGroupForRegion(getOriginalRegion()))
	{
	case REGION_GROUP_NORTH_AMERICA:
		if (isNative())
			return GC.getInfo(NATIVE).getUnitArtStyleType();
		return GC.getInfo(ENGLAND).getUnitArtStyleType();
	case REGION_GROUP_SOUTH_AMERICA:
		return GC.getInfo(INCA).getUnitArtStyleType();
	case REGION_GROUP_SUB_SAHARAN_AFRICA:
		return GC.getInfo(ZULU).getUnitArtStyleType();
	case REGION_GROUP_OCEANIA:
		return GC.getInfo(POLYNESIA).getUnitArtStyleType();
	}

	return GC.getInfo(INDEPENDENT).getUnitArtStyleType();
}

// doc (edead): slave trade
bool CvUnit::canTradeUnit(PlayerTypes eReceivingPlayer)
{
	if (eReceivingPlayer == NO_PLAYER || GET_PLAYER(eReceivingPlayer).isMinorCiv() || GET_PLAYER(eReceivingPlayer).isBarbarian() || isMinorCiv() || isBarbarian())
		return false;

	CvCity* pFirstCapital = GET_PLAYER(eReceivingPlayer).getCapitalCity();
	CvCity* pSecondCapital = GET_PLAYER(getOwner()).getCapitalCity();
	if (pFirstCapital == NULL || pSecondCapital == NULL)
		return false;

	return true;
}

// doc (edead): slave trade
void CvUnit::tradeUnit(PlayerTypes eReceivingPlayer)
{
	PlayerTypes eOwner = getOwner();
	if (eReceivingPlayer != NO_PLAYER)
	{
		CvCity const* pSpawnCity = GET_PLAYER(eReceivingPlayer).findSlaveCity();
		UnitTypes eUnitType = GC.getInfo(GET_PLAYER(eReceivingPlayer).getCivilizationType()).getCivilizationUnits(getUnitClassType());

		CvUnit* pTradeUnit = GET_PLAYER(eReceivingPlayer).initUnit(eUnitType, pSpawnCity->getX(), pSpawnCity->getY(), AI_getUnitAIType());
		pTradeUnit->convert(this);

		CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_TRADED_UNIT_TO_YOU", GET_PLAYER(eOwner).getCivilizationShortDescription(), pTradeUnit->getNameKey());
		gDLL->getInterfaceIFace()->addMessage(pTradeUnit->getOwner(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_UNITGIFTED",
                MESSAGE_TYPE_INFO, pTradeUnit->getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"),
                pTradeUnit->getX(), pTradeUnit->getY(), true, true);
	 }
}

// doc
bool CvUnit::canResolveCrisis(CvPlot const& kPlot) const
{
	if (!getUnitInfo().isResolveCrisis())
        return false;
	if (kPlot.getOwner() != getOwner())
        return false;
	if (GET_PLAYER(getOwner()).isAnarchy())
        return true;

    FOR_EACH_CITY(pLoopCity, GET_PLAYER(getOwner()))
	{
		if (pLoopCity->getOccupationTimer() > 0)
            return true;
	}

	return false;
}

// doc
bool CvUnit::resolveCrisis()
{
	if (!canResolveCrisis(getPlot()))
		return false;

	GET_PLAYER(getOwner()).changeAnarchyTurns(-GET_PLAYER(getOwner()).getAnarchyTurns());

    FOR_EACH_CITY_VAR(pLoopCity, GET_PLAYER(getOwner()))
	{
		pLoopCity->setOccupationTimer(0);
		if (pLoopCity->getPopulation() == 0)
			pLoopCity->completeRaze();
	}

	if (plot()->isActiveVisible(false))
	{
		NotifyEntity(MISSION_RESOLVE_CRISIS);
	}

	kill(true);
	return true;
}

// doc
bool CvUnit::canReformGovernment(CvPlot const& kPlot) const
{
	if (!getUnitInfo().isReformGovernment())
        return false;
	if (kPlot.getOwner() != getOwner())
        return false;
	return true;
}

// doc
bool CvUnit::reformGovernment()
{
	if (!canReformGovernment(getPlot()))
		return false;

	GET_PLAYER(getOwner()).setNoAnarchyTurns(1);
	GET_PLAYER(getOwner()).setRevolutionTimer(0);

	if (plot()->isActiveVisible(false))
	{
		NotifyEntity(MISSION_REFORM_GOVERNMENT);
	}

	// show a popup
	if (getOwner() == GC.getGame().getActivePlayer())
	{
		CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_CHANGECIVIC);
		if (NULL != pInfo)
		{
			gDLL->getInterfaceIFace()->addPopup(pInfo, getOwner());
		}
	}

	kill(true);
	return true;
}

// doc
bool CvUnit::canDiplomaticMission(CvPlot const& kPlot) const
{
	if (!getUnitInfo().isDiplomaticMission())
        return false;
	if (!kPlot.isCity())
        return false;

	CvCity* pCity = kPlot.getPlotCity();
	if (pCity->getOwner() == GC.getGame().getActivePlayer() &&
        !GET_TEAM(GET_PLAYER(getOwner()).getTeam()).isAtWar(GET_PLAYER(GC.getGame().getActivePlayer()).getTeam()))
        return false;

	return pCity->isCapital() && pCity->getOwner() != getOwner();
}

// doc
bool CvUnit::diplomaticMission()
{
	if (!canDiplomaticMission(getPlot()))
		return false;

	PlayerTypes ePlayer = getPlot().getOwner();
	TeamTypes eTeam = GET_PLAYER(ePlayer).getTeam();
	TeamTypes eOwnerTeam = GET_PLAYER(getOwner()).getTeam();

	if (GET_TEAM(eTeam).isAtWar(eOwnerTeam))
	{
		GET_TEAM(eTeam).makePeace(eOwnerTeam);
	}
	else
	{
        FOR_EACH_ENUM(Memory)
		{
			if (GET_PLAYER(ePlayer).AI_getMemoryAttitude(getOwner(), eLoopMemory) < 0)
			{
				GET_PLAYER(ePlayer).AI_changeMemoryCount(getOwner(), eLoopMemory, -GET_PLAYER(ePlayer).AI_getMemoryCount(getOwner(), eLoopMemory));
			}
		}

		GET_PLAYER(ePlayer).AI_changeAttitudeExtra(getOwner(), 4);
	}

	if (plot()->isActiveVisible(false))
	{
		NotifyEntity(MISSION_DIPLOMATIC_MISSION);
	}

	kill(true);
	return true;
}

// doc
bool CvUnit::canPersecute(CvPlot const& kPlot) const
{
	if (!getUnitInfo().isPersecute())
        return false;
	if (!kPlot.isCity())
        return false;

	CvCity* pCity = kPlot.getPlotCity();
	if (pCity->getOwner() != getOwner())
        return false;

	ReligionTypes eStateReligion = GET_PLAYER(getOwner()).getStateReligion();
    FOR_EACH_ENUM(Religion)
	{
		if (eLoopReligion != eStateReligion)
		{
			if (pCity->isHasReligion(eLoopReligion) && !pCity->isHolyCity(eLoopReligion))
				return true;
		}
	}

	return false;
}

// doc
bool CvUnit::persecute(ReligionTypes eReligion)
{
	if (!canPersecute(getPlot()))
		return false;

	if (eReligion == NO_RELIGION)
	{
		CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_PERSECUTION, getOwner(), getID());
		if (pInfo)
		{
			gDLL->getInterfaceIFace()->addPopup(pInfo, getOwner(), true);
		}
		return false;
	}

	CvCity* pCity = plot()->getPlotCity();
	int iChance = 65;

	if (GET_PLAYER(getOwner()).isStateReligion())
		iChance += std::min(25, std::max(0, 50 * GET_PLAYER(getOwner()).getHasReligionCount(GET_PLAYER(getOwner()).getStateReligion()) / GET_PLAYER(getOwner()).getNumCities() - 25));

	if (SyncRandSuccess100(iChance))
	{
		int iLootModifier = 1 + pCity->getPopulation() / pCity->getReligionCount();
		int iLoot = 1 + iLootModifier;

        FOR_EACH_ENUM(Building)
		{
			if (pCity->isHasRealBuilding(eLoopBuilding) && GC.getBuildingInfo(eLoopBuilding).getPrereqReligion() == eReligion)
			{
				iLoot += iLootModifier;
				if (GC.getInfo(GC.getInfo(eLoopBuilding).getBuildingClassType()).getMaxGlobalInstances() > 1)
					pCity->setHasRealBuilding(eLoopBuilding, false);
			}
		}

		if (pCity->getPopulation() > 1)
			pCity->changePopulation(-pCity->getPopulation() / 5);

		iLoot += SyncRandNum(iLoot);
		GET_PLAYER(getOwner()).changeGold(iLoot);

		for (PlayerIter<MAJOR_CIV,NOT_SAME_TEAM_AS> it(getTeam()); it.hasNext(); ++it)
		{
			if (it->getStateReligion() == eReligion)
				it->AI().AI_changeAttitudeExtra(getOwner(), -1);
		}

		if (pCity != NULL)
			pCity->setHasReligion(eReligion, false, true);

		pCity->changeCultureUpdateTimer(1);
		pCity->changeOccupationTimer(1);

		gDLL->getInterfaceIFace()->addMessage(getOwner(), false, GC.getEVENT_MESSAGE_TIME(),
                gDLL->getText("TXT_KEY_MESSAGE_PERSECUTION", pCity->getName().c_str(), GC.getReligionInfo(eReligion).getDescription(), iLoot),
                "AS2D_PLAGUE", MESSAGE_TYPE_INFO, getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_GREEN"), getX(), getY(), true, true);
	}
	else
	{
		gDLL->getInterfaceIFace()->addMessage(getOwner(), false, GC.getEVENT_MESSAGE_TIME(),
                gDLL->getText("TXT_KEY_MESSAGE_PERSECUTION_FAIL", pCity->getName().c_str()), "AS2D_PLAGUE", MESSAGE_TYPE_INFO, getButton(),
                (ColorTypes)GC.getInfoTypeForString("COLOR_RED"), getX(), getY(), true, true);
	}

	pCity->changeHurryAngerTimer(pCity->flatHurryAngerLength());

	if (plot()->isActiveVisible(false))
	{
		NotifyEntity(MISSION_PERSECUTE);
	}

	kill(true);
	return true;
}

// doc
bool CvUnit::canGreatMission(CvPlot const& kPlot) const
{
	if (!getUnitInfo().isGreatMission())
		return false;
	if (!kPlot.isCity())
		return false;

	if (GET_PLAYER(getOwner()).getStateReligion() != NO_RELIGION)
		return true;

    FOR_EACH_ENUM(Religion)
	{
		if (GC.getGame().isReligionFounded(eLoopReligion) &&
            getPlot().getSpreadFactor(eLoopReligion) == REGION_SPREAD_CORE &&
            !GC.getInfo(eLoopReligion).isLocal())
			return true;
	}

	return false;
}

// doc
bool CvUnit::greatMission()
{
	if (!canGreatMission(getPlot()))
		return false;

	int iNumCities = 4 + SyncRandNum(3);
	iNumCities = std::max(iNumCities, getArea().getCitiesPerPlayer(getOwner()));
	ReligionTypes eReligion = GET_PLAYER(getOwner()).getStateReligion();

	if (eReligion == NO_RELIGION)
	{
        FOR_EACH_ENUM(Religion)
		{
			if (!GC.getInfo(eLoopReligion).isLocal() &&
                getPlot().getSpreadFactor(eLoopReligion) == REGION_SPREAD_CORE)
			{
				eReligion = eLoopReligion;
				break;
			}
		}
	}

	CvPlot* pSpreadPlot;
	CvCity* pSpreadCity;
	ReligionTypes eRemovedReligion;
	int iSpreads = 0;

	// spread to eligible cities
	for (iSpreads; iSpreads < iNumCities; iSpreads++)
	{
		pSpreadPlot = AI().AI_spreadTarget(eReligion, true).second;
		if (pSpreadPlot == NULL || !pSpreadPlot->isCity())
            break;

		pSpreadPlot->getPlotCity()->spreadReligion(eReligion, false);

		// spread religion attempt event
		CvEventReporter::getInstance().unitSpreadReligionAttempt(this, eReligion, true);
	}

	// remove from eligible cities
	for (; iSpreads < iNumCities; iSpreads++)
	{
		pSpreadCity = AI().AI_persecutionTarget();
		if (pSpreadCity == NULL)
            break;

		eRemovedReligion = pSpreadCity->AI().AI_getPersecutionReligion(eReligion);
		if (eRemovedReligion == NO_RELIGION)
            continue;

		pSpreadCity->removeReligion(eRemovedReligion);
	}

	if (plot()->isActiveVisible(false))
	{
		NotifyEntity(MISSION_GREAT_MISSION);
	}

	kill(true);
	return true;
}

// doc
bool CvUnit::canSatelliteAttack(CvPlot const& kPlot) const
{
	if (getSpecialUnitType() != SPECIALUNIT_SATELLITE)
		return false;
	if (!GET_TEAM(getTeam()).canSatelliteAttack())
		return false;

    FOR_EACH_UNIT_IN(pUnit, kPlot)
	{
        if (pUnit == this)
            continue;
        if (pUnit->getSpecialUnitType() != SPECIALUNIT_SATELLITE)
            continue;

        if (atWar(getTeam(), pUnit->getTeam()))
            return true;
	}

	return false;
}

// doc
bool CvUnit::satelliteAttack()
{
	if (!canSatelliteAttack(getPlot()))
		return false;

    FOR_EACH_UNIT_VAR_IN(pUnit, getPlot())
	{
        if (pUnit == this)
            continue;
        if (pUnit->getSpecialUnitType() != SPECIALUNIT_SATELLITE)
            continue;
        if (!atWar(getTeam(), pUnit->getTeam()))
            continue;

        pUnit->kill(true, getOwner());
        if (getPlot().isActiveVisible(false))
        {
            NotifyEntity(MISSION_SATELLITE_ATTACK);
        }

        finishMoves();
        return true;
	}

	return false;
}

// doc
SpecialistTypes CvUnit::getSettledSpecialist() const
{
    FOR_EACH_ENUM(Specialist)
	{
		if (getUnitInfo().getGreatPeoples(eLoopSpecialist))
			return eLoopSpecialist;
	}
	return NO_SPECIALIST;
}

// doc
bool CvUnit::isWorker() const
{
	return getUnitInfo().isWorker();
}

// doc
bool CvUnit::canRebuild(CvPlot const& kPlot) const
{
	if (!getUnitInfo().isFound())
		return false;
	if (!kPlot.isCity())
		return false;

	CvCity* pCity = kPlot.getPlotCity();
	if (pCity->getOwner() != getOwner())
		return false;

    FOR_EACH_ENUM(BuildingClass)
	{
		BuildingTypes eBuilding = GC.getInfo(getCivilizationType()).getCivilizationBuildings(eLoopBuildingClass);
        if (eBuilding == NO_BUILDING)
            continue;

        CvBuildingInfo const& kBuilding = GC.getInfo(eBuilding);
        if (kBuilding.getFreeStartEra() == NO_ERA)
            continue;
        if (pCity->isHasRealBuilding(eBuilding))
            continue;
        if (!pCity->canConstruct(eBuilding, true))
            continue;

        if (GET_PLAYER(getOwner()).getCurrentEra() >= kBuilding.getFreeStartEra())
            return true;
	}

	return false;
}

bool CvUnit::rebuild()
{
	if (!canRebuild(getPlot()))
		return false;

	bool bBuilt = getPlot().getPlotCity()->rebuild();
    if (!bBuilt)
        return false;

	if (getPlot().isActiveVisible(false))
	{
		NotifyEntity(MISSION_REBUILD);
	}

	kill(true);
	return true;
}
