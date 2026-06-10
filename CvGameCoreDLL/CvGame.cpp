#include "CvGameCoreDLL.h"
#include "CvGame.h"
#include "CvDeal.h"
#include "CvAgents.h" // advc.agent
#include "CoreAI.h"
#include "CvCityAI.h"
#include "CvUnit.h"
#include "CvSelectionGroupAI.h"
#include "CitySiteEvaluator.h"
#include "PlotRange.h"
#include "CvArea.h"
#include "CvMapGenerator.h"
#include "CvDiploParameters.h"
#include "CvReplayMessage.h"
#include "CvInfo_City.h"
#include "CvInfo_Terrain.h"
#include "CvInfo_GameOption.h"
#include "CvInfo_Civics.h"
#include "CvPopupInfo.h"
#include "CvReplayInfo.h"
#include "CvGameTextMgr.h"
#include "CvMessageControl.h"
#include "BarbarianWeightMap.h" // advc.304
#include "StartingPositionIteration.h" // advc.027
#include "TrueStarts.h" // advc.tsl
#include "StartPointsAsHandicap.h" // advc.250b
#include "RiseFall.h" // advc.700
#include "CvHallOfFameInfo.h" // advc.106i
#include "BBAILog.h" // BBAI
#include "CvBugOptions.h" // K-Mod

/*	<advc.007c> Use this CvGame instance instead of GC.getGame() for RNG calls.
	(Won't matter so long as CvGame is a singleton class.) */
#undef CVGAME_INSTANCE_FOR_RNG
#define CVGAME_INSTANCE_FOR_RNG (*this) // </advc.007c>


CvGame::CvGame() :
	m_pRiseFall(new RiseFall()), // advc.700
	m_pSpah(new StartPointsAsHandicap()), // advc.250b
	m_pBarbarianWeightMap(new BarbarianWeightMap()) // advc.304
{
	m_pReplayInfo = NULL;
	m_pHallOfFame = NULL; // advc.106i
	m_pLegacyOrgSeatData = NULL; // advc.enum
	reset(NO_HANDICAP, true);

    // TODO: declare and initialize
    // doc
    m_aiTechRankTeam = new int[MAX_TEAMS];
    m_aiCivPeriod = new char[NUM_CIVS];
    m_aiCivilizationHistory = new std::hash_map<int, std::hash_map<int, int> >[NUM_HISTORY_TYPES];
    m_aiFirstDiscovered = NULL;
    m_aiFirstDiscoveredTurn = NULL;
}


CvGame::~CvGame()
{
	uninit();
	SAFE_DELETE(m_pRiseFall); // advc.700
	SAFE_DELETE(m_pSpah); // advc.250b
	SAFE_DELETE(m_pBarbarianWeightMap); // advc.304
}


void CvGame::init(HandicapTypes eHandicap)
{
	CvInitCore& ic = GC.getInitCore();

	reset(eHandicap); // Reset serialized data

	// Init containers ...

	m_voteSelections.init();
	m_votesTriggered.init();

	/*m_mapRand.init(ic.getMapRandSeed() % 73637381);
	m_sorenRand.init(ic.getSyncRandSeed() % 52319761);*/
	/*	advc.027b: The modulo reductions get in the way of reproducing
		regenerated maps. It seems that, unless positive seeds are set
		in CivilizationIV.ini, CvInitCore receives the same seed for
		both RNGs. The modulo doesn't reliably prevent that. Shouldn't
		really matter, and actually makes it easier to reproduce maps
		as only one seed has to be read off the screen. */
	getMapRand().init(ic.getMapRandSeed());
	getSorenRand().init(ic.getSyncRandSeed());
	m_initialRandSeed.uiMap = getMapRand().getSeed();
	m_initialRandSeed.uiSync = getSorenRand().getSeed(); // <advc.027b>

	// Init non-serialized data ...

	m_bAllGameDataRead = true; // advc: Not loading from savegame

	// Turn off all MP options if it's a single player game
	if (ic.getType() == GAME_SP_NEW || ic.getType() == GAME_SP_SCENARIO)
	{
		FOR_EACH_ENUM(MPOption)
			setMPOption(eLoopMPOption, false);
	}

	// If this is a hot seat game, simultaneous turns is always off.
	if (isHotSeat() || isPbem())
		setMPOption(MPOPTION_SIMULTANEOUS_TURNS, false);
	// If we didn't set a time in the Pitboss, turn timer off.
	if (isPitboss() && getPitbossTurnTime() == 0)
		setMPOption(MPOPTION_TURN_TIMER, false);

	if (isMPOption(MPOPTION_SHUFFLE_TEAMS))
	{
		int aiTeams[MAX_CIV_PLAYERS];
		int iNumPlayers = 0;
		for (int i = 0; i < MAX_CIV_PLAYERS; i++)
		{
			if (ic.getSlotStatus((PlayerTypes)i) == SS_TAKEN)
			{
				aiTeams[iNumPlayers] = ic.getTeam((PlayerTypes)i);
				++iNumPlayers;
			}
		}

		for (int i = 0; i < iNumPlayers; i++)
		{
			int j = getSorenRand().get(iNumPlayers - i, NULL) + i;
			if (i != j)
			{
				int iTemp = aiTeams[i];
				aiTeams[i] = aiTeams[j];
				aiTeams[j] = iTemp;
			}
		}

		iNumPlayers = 0;
		for (int i = 0; i < MAX_CIV_PLAYERS; i++)
		{
			if (ic.getSlotStatus((PlayerTypes)i) == SS_TAKEN)
			{
				ic.setTeam((PlayerTypes)i, (TeamTypes)aiTeams[iNumPlayers]);
				++iNumPlayers;
			}
		}
	}

	if (isOption(GAMEOPTION_LOCK_MODS))
	{
		if (isGameMultiPlayer())
			setOption(GAMEOPTION_LOCK_MODS, false);
		else
		{
			static const int iPasswordSize = 8;
			char szRandomPassword[iPasswordSize];
			for (int i = 0; i < iPasswordSize-1; i++)
			{
				szRandomPassword[i] = /* advc: */ safeIntCast<char>(
						getSorenRandNum(CHAR_MAX + 1, NULL));
			}
			szRandomPassword[iPasswordSize-1] = 0;
			ic.setAdminPassword(szRandomPassword);
		}
	}

	/*	advc.250c: So far, no points from Advanced Start have been assigned.
		I want the start turn to be a function of the start points.
		I'm assigning the start turn preliminarily here to avoid problems with
		start turn being undefined (not sure if this would be an issue),
		and overwrite the value later. To this end, I've moved the
		start turn and start year computation into a new function: */
	setStartTurnYear();

	FOR_EACH_ENUM(SpecialUnit)
	{
		if (GC.getInfo(eLoopSpecialUnit).isValid())
			makeSpecialUnitValid(eLoopSpecialUnit);
	}
	FOR_EACH_ENUM(SpecialBuilding)
	{
		if (GC.getInfo(eLoopSpecialBuilding).isValid())
			makeSpecialBuildingValid(eLoopSpecialBuilding);
	}

	AI().AI_init();

	doUpdateCacheOnTurn();
}

// Set initial items (units, techs, etc...)
void CvGame::setInitialItems()
{
	PROFILE_FUNC();

	//initFreeState(); // doc: disabled
	// <advc.027> Keep data from starting plot assignment for normalization
	NormalizationTarget* pNormalizationTarget = assignStartingPlots();
	normalizeStartingPlots(pNormalizationTarget);
	SAFE_DELETE(pNormalizationTarget); // </advc.027>
	// <advc> River ids shouldn't be used after map generation
	FOR_EACH_ENUM(PlotNum)
		GC.getMap().plotByIndex(eLoopPlotNum)->setRiverID(-1); // </advc>
	// <advc.030> Now that ice has been placed and normalization is through
	if (GC.getDefineBOOL(CvGlobals::PASSABLE_AREAS))
		GC.getMap().recalculateAreas(false);
	// </advc.030>
	// <advc.tsl>
	if (isOption(GAMEOPTION_TRUE_STARTS))
	{
		TrueStarts ts;
		ts.changeCivs();
		if (GC.getDefineBOOL(CvGlobals::TRUE_STARTS_SANITIZE))
			ts.sanitize();
	}
	GC.getLogger().logCivLeaders(); // </advc.tsl>
	/*	<advc.190c> Letting CvInitCore do this would be misleading b/c
		net messages don't get delivered that early in game setup. */
	if (isNetworkMultiPlayer())
	{
		CvInitCore const& kInitCore = GC.getInitCore();
		FOR_EACH_ENUM(Player)
		{
			if (kInitCore.wasCivRandomlyChosen(eLoopPlayer) ||
				kInitCore.wasLeaderRandomlyChosen(eLoopPlayer))
			{	// We're the host
				CvMessageControl::getInstance().sendCivLeaderSetup(kInitCore);
				break;
			}
		}
	} // </advc.190c>
	// Delay part of the freebies until starting sites have been assigned
	initFreeCivState(); // </advc.tsl>
	initFreeUnits();
	// <advc.250c>
	if (GC.getDefineBOOL("INCREASE_START_TURN") && getStartEra() == 0)
	{
		int iStartTurn = getStartTurn();
		bool bAllHuman = (PlayerIter<HUMAN>::count() >= PlayerIter<CIV_ALIVE>::count());
		CvHandicapInfo const& kGameHandicap = GC.getInfo(getHandicapType());
		if (isOption(GAMEOPTION_ADVANCED_START))
		{
			std::vector<scaled> distr;
			for (PlayerIter<CIV_ALIVE> it; it.hasNext(); ++it)
			{
				if (!it->isHuman() || !isOption(GAMEOPTION_SPAH) || bAllHuman)
					distr.push_back(it->getAdvancedStartPoints());
			}
			/*	Start turn 0 is calibrated to the AI freebies from difficulty, which
				increase with every level (well, every level after Prince). */
			scaled rDifficultyVal = kGameHandicap.getDifficulty() * fixp(6.25);
			rDifficultyVal.increaseTo(175);
			scaled rMaxMean = (stats::max(distr) + stats::mean(distr)) / 2;
			if (rMaxMean > rDifficultyVal)
				iStartTurn += (rMaxMean - rDifficultyVal).pow(fixp(0.58)).roundToMultiple(5);
		} // </advc.250c>
		// <advc.251> Also set a later start turn if handicap grants lots of AI freebies
		else if (!bAllHuman)
		{
			iStartTurn += ((kGameHandicap.getAIStartingUnitMultiplier() * 10 +
					kGameHandicap.getAIStartingWorkerUnits() * 10) *
					getSpeedPercent()) / 100;
		} // <advc.250c>
		if (getStartTurn() != iStartTurn)
		{
			setStartTurnYear(iStartTurn);
			/*	initDiplomacy is called from outside the DLL between the first
				setStartTurnYear call and setInitialItems. The second setStartTurnYear
				causes any initial "universal" peace treaties to end after 1 turn.
				Need to inform all CvDeal objects about the changed start turn: */
			FOR_EACH_DEAL_VAR(d)
				d->setInitialGameTurn(getGameTurn());
		} // </advc.251>
	} // </advc.250c>
	for (PlayerAIIter<CIV_ALIVE> it; it.hasNext(); ++it)
		it->AI_updateFoundValues();
	// <advc.tsl>
	if (m_iMapRegens < GC.getDefineINT("AUTO_REGEN_MAP"))
		regenerateMap(true); // </advc.tsl>
}


void CvGame::regenerateMap(/* advc.tsl: */ bool bAutomated)
{
	if (GC.getInitCore().getWBMapScript())
		return;
	CvMap& kMap = GC.getMap();
	/*	<advc.004j> Not sure if the unmodded game or any mod included with AdvCiv
		uses script data, but can't hurt to reset it. CvDLLButtonPopup::
		launchMainMenuPopup wants to disallow map regeneration once script data
		has been set. */
	setScriptData("");
	FOR_EACH_ENUM(PlotNum)
	{
		CvPlot& kPlot = kMap.getPlotByIndex(eLoopPlotNum);
		kPlot.setScriptData("");
		/*	advc.021b: Otherwise, assignStartingPlots runs into trouble upon
			map regeneration when a script calls allowDefaultImpl after
			assigning starting plots. */
		kPlot.setStartingPlot(false);
	} // </advc.004j>

	setFinalInitialized(false);
	setDawnOfManShown(false); // advc.004x

	for (PlayerIter<> it; it.hasNext(); ++it)
		it->killUnits();
	for (PlayerIter<> it; it.hasNext(); ++it)
		it->killCities();
	for (PlayerIter<> it; it.hasNext(); ++it)
		it->killAllDeals();
	for (PlayerIter<> it; it.hasNext(); ++it)
	{
		it->setFoundedFirstCity(false);
		it->setStartingPlot(NULL);
		// <advc.004x>
		if (it->isHuman())
			it->killAll(BUTTONPOPUP_CHOOSETECH); // </advc.004x>
	}
	for (TeamIter<> it; it.hasNext(); ++it)
		kMap.setRevealedPlots(it->getID(), false);

	gDLL->getEngineIFace()->clearSigns();
	kMap.erasePlots();

	// <advc.001>
	if (m_iNumSessions > 1)
	{	// Will not have been called when regenerating from a savegame
		GC.getPythonCaller()->callMapFunction("beforeInit");
	} // </advc.001>
	/*	advc.027b: Mustn't overwrite m_initialRandSeed.uiSync if we want to
		preserve the civ selection when reproducing a map after a restart.
		normalizeStartingPlots now uses MapRand exclusively. */
	m_initialRandSeed.uiMap = getMapRand().getSeed();
	CvMapGenerator::GetInstance().generateRandomMap();
	CvMapGenerator::GetInstance().addGameElements();

	gDLL->getEngineIFace()->RebuildAllPlots();
	/*	<advc.001> Even if we call CvMap::setupGraphical before RebuildAllPlots,
		there are still artifacts in texture surfaces. I guess we need to give
		the EXE a little bit of time. I'm leaving the original call in place too
		(although it takes about a second) to avoid (overt) momentary glitches. */
	setUpdateTimer(UPDATE_REBUILD_PLOTS, 1);
	// Fix dark lines running through Flood Plains
	{
		FeatureTypes eFloodPlains = (FeatureTypes)GC.getInfoTypeForString(
				"FEATURE_FLOOD_PLAINS");
		FOR_EACH_ENUM(PlotNum)
		{
			CvPlot& kPlot = GC.getMap().getPlotByIndex(eLoopPlotNum);
			if (kPlot.isRiver() && kPlot.getFeatureType() == eFloodPlains)
				kPlot.updateRiverSymbol(true, true);
		}
	} // </advc.001>
	// <advc.251>
	setGameTurn(0);
	setStartTurn(0);
	setStartTurnYear();
	m_iElapsedGameTurns = 0;
	// </advc.251>
	/*	advc.001: Reset minutesPlayed to 0. Note: Would cause a (redundant)
		autosave in CvGame::update if I hadn't added a re-gen check there. */
	setTurnSlice(0);
	CvEventReporter::getInstance().resetStatistics();
	// <advc.tsl>
	m_iMapRegens++;
	if (isOption(GAMEOPTION_TRUE_STARTS))
	{	// Civ may have changed; don't accumulate starting techs.
		FOR_EACH_ENUM(Team)
		{
			FOR_EACH_ENUM(Tech)
				GET_TEAM(eLoopTeam).setHasTech(eLoopTech, false, NO_PLAYER, false, false);
		}
	} // </advc.tsl>
	m_eInitialActivePlayer = NO_PLAYER; // advc.106h
	setInitialItems();
	// <advc.tsl>
	if (bAutomated)
		return; // </advc.tsl>

	initScoreCalculation();
	setFinalInitialized(true);

	kMap.setupGraphical();
	gDLL->getEngineIFace()->SetDirty(GlobeTexture_DIRTY_BIT, true);
	gDLL->getEngineIFace()->SetDirty(MinimapTexture_DIRTY_BIT, true);
	gDLL->UI().setDirty(ColoredPlots_DIRTY_BIT, true);

    gDLL->getEngineIFace()->AutoSave(true); // doc

	cycleSelectionGroups_delayed(1, false);
	// <advc.004j>
	bool bShowDawn = (GC.getDefineBOOL("SHOW_DAWN_AFTER_REGEN") &&
			// Somehow doesn't work with Adv. Start; Dawn screen doesn't appear.
			(!isOption(GAMEOPTION_ADVANCED_START) || isOption(GAMEOPTION_SPAH)));
	// </advc.004j>
	// <advc.700>
	if (isOption(GAMEOPTION_RISE_FALL))
	{
		m_pRiseFall->reset();
		m_pRiseFall->init();
		bShowDawn = false;
	}
	else // </advc.700>
		autoSave(true); // advc.106l
	// <advc.004j>
	if (bShowDawn)
		showDawnOfMan(); // </advc.004j>
	if (getActivePlayer()!= NO_PLAYER)
	{
		CvPlot* pPlot = GET_PLAYER(getActivePlayer()).getStartingPlot();
		if (pPlot != NULL)
		{
			//gDLL->UI().lookAt(pPlot->getPoint(), CAMERALOOKAT_NORMAL);
			/*	<advc.004j> ^Comment by EmperorFool (from BULL):
				"This doesn't work until after the game has had time to update.
				 Centering on the starting location is now done by MapFinder using
				 BugUtil.delayCall()."
				I'm going to use setUpdateTimer instead. Unless the Dawn screen
				is shown b/c that focuses the camera anyway. */
			if (!bShowDawn)
				setUpdateTimer(UPDATE_LOOK_AT_STARTING_PLOT, 5); // </advc.004j>
		}
	}
}

// advc.004j:
void CvGame::showDawnOfMan()
{
	if (getActivePlayer() == NO_PLAYER)
		return;
	// Based on CvAllErasDawnOfManScreenEventManager.py
	CvPopupInfo* pDummyPopup = new CvPopupInfo();
	if (pDummyPopup != NULL)
	{
		pDummyPopup->setButtonPopupType(BUTTONPOPUP_PYTHON_SCREEN);
		pDummyPopup->setText(L"showDawnOfMan");
		GET_PLAYER(getActivePlayer()).addPopup(pDummyPopup);
	}
	setDawnOfManShown(true); // advc.004x
}


void CvGame::uninit()
{
	m_aszDestroyedCities.clear();
	m_aszGreatPeopleBorn.clear();

	m_deals.uninit();
	// <advc.072> This also frees dynamically allocated memory
	m_currentDeals.clear();
	m_currentDealsWidget.clear();
	// </advc.072>
	m_voteSelections.uninit();
	m_votesTriggered.uninit();
	// advc: Removed CvRandom::uninit; there was nothing to be done.
	/*m_mapRand.uninit();
	m_sorenRand.uninit();*/

	clearReplayMessageMap();
	SAFE_DELETE(m_pReplayInfo);

	m_aeVoteSourceReligion.reset();
	m_abInactiveTriggers.reset();
	applyOptionEffects(true); // advc.310
	/*	advc.700: Need to call this explicitly due to the unusual way that
		RiseFall is initialized (from updateBlockadedPlots) */
	m_pRiseFall->reset();
}

// advc: Cut from CvGame::init
void CvGame::setStartTurnYear(int iTurn)
{
	CvGameSpeedInfo const& kSpeed = GC.getInfo(getGameSpeedType());
	// <advc.250c>
	if (iTurn > 0)
		setGameTurn(iTurn);
	else // </advc.250c>
		if (getGameTurn() == 0)
	{
		int iStartTurn = 0;
		for (int i = 0; i < kSpeed.getNumTurnIncrements(); i++)
			iStartTurn += kSpeed.getGameTurnInfo(i).iNumGameTurnsPerIncrement;
		iStartTurn *= GC.getInfo(getStartEra()).getStartPercent();
		iStartTurn /= 100;
		setGameTurn(iStartTurn);
	}
	setStartTurn(getGameTurn());
	if (getMaxTurns() == 0 /* advc.250c: */ || iTurn > 0)
	{
		int iEstimateEndTurn = 0;
		for (int i = 0; i < kSpeed.getNumTurnIncrements(); i++)
			iEstimateEndTurn += kSpeed.getGameTurnInfo(i).iNumGameTurnsPerIncrement;
		setEstimateEndTurn(iEstimateEndTurn);
		if (getEstimateEndTurn() > getGameTurn())
		{
			FOR_EACH_ENUM(Victory)
			{
				if (isVictoryValid(eLoopVictory) &&
					GC.getInfo(eLoopVictory).isEndScore())
				{
					setMaxTurns(getEstimateEndTurn() - getGameTurn());
					break;
				}
			}
		}
	}
	else setEstimateEndTurn(getGameTurn() + getMaxTurns());

	setStartYear(GC.getDefineINT("START_YEAR"));
}

/*	Initialize data members that are serialized. (advc: I'm also initializing some
	non-serialized variables here. Most of these don't _have to_ be reset when
	loading a savegame, but it seems safer to do so.) */
void CvGame::reset(HandicapTypes eHandicap, bool bConstructorCall)
{
	uninit();

	m_bAllGameDataRead = false; // advc;
	// <advc.106i>
	if (m_pHallOfFame != NULL)
		m_pHallOfFame->uninit(); // Don't keep HoF in memory indefinitely
	// </advc.106i>
	m_iElapsedGameTurns = 0;
	m_iStartTurn = 0;
	m_iStartYear = 0;
	m_iEstimateEndTurn = 0;
	m_iTurnSlice = 0;
	m_iCutoffSlice = 0;
	m_iNumGameTurnActive = 0;
	m_iNumCities = 0;
	m_iTotalPopulation = 0;
	m_iTradeRoutes = 0;
	m_iFreeTradeCount = 0;
	m_iNoNukesCount = 0;
	m_iNukesExploded = 0;
	m_iMaxPopulation = 0;
	m_iMaxLand = 0;
	m_iMaxTech = 0;
	m_iMaxWonders = 0;
	m_iInitPopulation = 0;
	m_iInitLand = 0;
	m_iInitTech = 0;
	m_iInitWonders = 0;
	m_iAIAutoPlay = 0;
	m_iCircumnavigated = -1; // rfc // TODO: unused
	m_iMedianTechValue = 0; // doc
	m_iGlobalWarmingIndex = 0;// K-Mod
	m_iGwEventTally = -1; // K-Mod (-1 means Gw tally has not been activated yet)
	// <advc.opt>
	m_iStartingPlotRange = 0; // (not serialized)
	m_iCivPlayersEverAlive = 0;
	m_iCivTeamsEverAlive = 0;
	// </advc.opt>
	m_uiInitialTime = 0;
	m_uiSaveFlag = 0; // advc

	m_bScoreDirty = false;
	m_bCircumnavigated = false;
	m_bDebugMode = false;
	m_bDebugModeCache = false;
	m_bFinalInitialized = false;
	m_bPbemTurnSent = false;
	m_bHotPbemBetweenTurns = false;
	m_bPlayerOptionsSent = false;
	m_bNukesValid = false;
	m_bShowingCurrentDeals = false; // advc.072 (not serialized)
	m_iScreenWidth = m_iScreenHeight = 0; // advc.061
	// <advc.004n>
	m_iPlotListShift = 0;
	m_bCityScreenUp = false; // </advc.004n>

	m_eHandicap = eHandicap;
	// <advc.127>
	m_eAIHandicap = (bConstructorCall ? NO_HANDICAP :
			// (XML not loaded when constructor called)
			(HandicapTypes)GC.getDefineINT("STANDARD_HANDICAP")); // </advc.127>
	m_ePausePlayer = NO_PLAYER;
	m_eBestLandUnit = NO_UNIT;
	m_eWinner = NO_TEAM;
	m_eVictory = NO_VICTORY;
	m_eGameState = GAMESTATE_ON;
	m_eInitialActivePlayer = NO_PLAYER; // advc.106h
	m_eNormalizationLevel = NORMALIZE_DEFAULT; // advc.108

    m_eGreatPeopleNotifications = NOTIFICATIONS_ALL; // doc
    m_eReligionSpreadNotifications = NOTIFICATIONS_ALL; // doc
    m_eGreatPeopleNotifications = NOTIFICATIONS_ALL; // doc

	m_szScriptData = "";

    // TODO: declare and initialize
    for (iI = 0; iI < MAX_TEAMS; iI++)
    {
        m_aiTechRankTeam[iI] = 0; // Leoreth
    }
    for (iI = 0; iI < NUM_CIVS; iI++)
    {
        m_aiCivPeriod[iI] = NO_PERIOD;
    }
    for (iI = 0; iI < NUM_HISTORY_TYPES; iI++)
    {
        m_aiCivilizationHistory[iI].clear();
    }

	if (!bConstructorCall)
	{
		m_aeRankPlayer.reset();
		m_aePlayerRank.reset();
		m_aiPlayerScore.reset();
		m_aeRankTeam.reset();
		m_aeTeamRank.reset();
		m_aiTeamScore.reset();
		m_aiUnitCreatedCount.reset();
		m_aiUnitClassCreatedCount.reset();
		m_aiBuildingClassCreatedCount.reset();
		m_aiProjectCreatedCount.reset();
		m_aiForceCivicCount.reset();
		m_aiVoteOutcome.reset();
		m_aiDiploVote.reset();
		m_abSpecialUnitValid.reset();
		m_abSpecialBuildingValid.reset();
		m_aiReligionGameTurnFounded.reset();
		m_abReligionSlotTaken.reset();
		m_aeHolyCity.reset();
		m_aiCorporationGameTurnFounded.reset();
		m_aeHeadquarters.reset();
		m_aiSecretaryGeneralTimer.reset();
		m_aiVoteTimer.reset();
		getBarbarianWeightMap().getActivityMap().reset(); // advc.304
	}

	m_deals.removeAll();
	m_voteSelections.removeAll();
	m_votesTriggered.removeAll();

	m_mapRand.reset();
	m_sorenRand.reset();
	m_initialRandSeed.uiMap = m_initialRandSeed.uiSync = 0; // advc.027b

	m_iNumSessions = 1;
	m_iMapRegens = 0; // advc.tsl

	m_iNumCultureVictoryCities = 0;
	m_eCultureVictoryCultureLevel = NO_CULTURELEVEL;
	m_bScenario = false; // advc.052

	if (!bConstructorCall)
		AI().AI_reset();

	m_aiActivePlayerCycledGroups.clear(); // K-Mod
	m_bInBetweenTurns = false; // advc.106b
	m_iUnitUpdateAttempts = 0; // advc.001y
	m_iTurnLoadedFromSave = -1; // advc.044
	// <advc.004m>
	m_eCurrentLayer = GLOBE_LAYER_UNKNOWN;
	m_bLayerFromSavegame = false; // </advc.004m>
	m_bFeignSP = false; // advc.135c
	m_bDoMShown = false; // advc.004x
	m_bFPTestDone = false; // advc.003g
	// <advc.003r>
	for (int i = 0; i < NUM_UPDATE_TIMER_TYPES; i++)
		m_aiUpdateTimers[i] = -1; // </advc.003r>
	/*	<advc.003v> No need to read data from a savegame first; CvInitCore
		is responsible for the game options and is loaded before CvGame. */
	if (!bConstructorCall)
		CvGlobals::getInstance().loadOptionalXMLInfo(); // </advc.003v>
}

/*	The EXE calls this after generating the map but before initFreeState
	(i.e. also before assigning starting plots). Seems like a good place
	for various initializations as it gets called for all game types
	(unlike setInitialItems, which isn't called for scenarios with fixed
	civs and leaders). */
void CvGame::initDiplomacy()
{
	PROFILE_FUNC();

	GC.getAgents().gameStart(false); // advc.agent
	m_bFPTestDone = !isNetworkMultiPlayer(); // advc.003g
	// <advc.108>
	// Don't overwrite "Balanced" custom map option
	if (m_eNormalizationLevel != NORMALIZE_HIGH)
		setStartingPlotNormalizationLevel(); // </advc.108>
	setPlayerColors(); // advc.002i

	for (TeamIter<> itTeam; itTeam.hasNext(); ++itTeam)
	{
		itTeam->meet(itTeam->getID(), false);
		if (!itTeam->isMajorCiv())
		{
			for (TeamIter<CIV_ALIVE> itCiv; itCiv.hasNext(); ++itCiv) // advc.003m: ALIVE
			{
				if (itTeam->getID() != itCiv->getID())
					itTeam->declareWar(itCiv->getID(), false, NO_WARPLAN);
			}
		}
	}

	// Forced peace at the beginning of Advanced starts
	if (isOption(GAMEOPTION_ADVANCED_START) &&
		/*	advc.250b: No need to protect the AI from the player when human
			start is advanced, and AI won't start wars within 10 turns anyway. */
		!isOption(GAMEOPTION_SPAH))
	{
		CLinkList<TradeData> items1;
		CLinkList<TradeData> items2;
		{
			TradeData peaceTreaty(TRADE_PEACE_TREATY);
			items1.insertAtEnd(peaceTreaty);
			items2.insertAtEnd(peaceTreaty);
		}
		// advc.001: I don't think this should happen for minor civs
		for (PlayerIter<MAJOR_CIV> itFirst; itFirst.hasNext(); ++itFirst)
		{
			for (PlayerIter<MAJOR_CIV> itSecond; itSecond.hasNext(); ++itSecond)
			{
				if (itFirst->getID() <= itSecond->getID())
					continue;
				if (GET_TEAM(itFirst->getTeam()).canChangeWarPeace(itSecond->getTeam()))
					implementDeal(itFirst->getID(), itSecond->getID(), items2, items2);
			}
		}
	}
}

/*	advc.002i: Assign unique player colors in games where multiple players
	have the same civ type */
void CvGame::setPlayerColors()
{
	std::vector<std::pair<PlayerTypes,int> > aeiReassign;
	EagerEnumMap<CivilizationTypes,int> aiPlayersPerCiv;
	for (PlayerIter<ALIVE> it; it.hasNext(); ++it)
	{
		CivilizationTypes eCiv = it->getCivilizationType();
		aiPlayersPerCiv.add(eCiv, 1);
		int iPlayers = aiPlayersPerCiv.get(eCiv);
		if (iPlayers > 1)
			aeiReassign.push_back(std::make_pair(it->getID(), iPlayers));
	}
	for (size_t i = 0; i < aeiReassign.size(); i++)
	{
		PlayerTypes const eReassignPlayer = aeiReassign[i].first;
		bool const bMatchSecondary = (aeiReassign[i].second == 2);
		bool const bRandomize = (aeiReassign[i].second > 3);
		CivilizationTypes eBestCiv = NO_CIVILIZATION;
		float fSmallestDiff = FLT_MAX;
		CivilizationTypes const eCiv = GET_PLAYER(eReassignPlayer).
				getCivilizationType();
		CvPlayerColorInfo const& kDefaultColor = GC.getInfo(
				(PlayerColorTypes)GC.getInfo(eCiv).getDefaultPlayerColor());
		/*	Look for a color similar to the secondary color of eCiv.
			(If we try to match the primary color, it'll be difficult
			to distinguish from the first player of eCiv.) */
		NiColorA const& kTargetColor = GC.getInfo(kDefaultColor.
				getColorTypeSecondary()).getColor();
		/*	For the third player per civ, try matching a mix of primary
			and secondary color. For subsequent players, pick a random color. */
		NiColorA const* pTargetColor2 = (bMatchSecondary || bRandomize) ? NULL :
				&GC.getInfo(kDefaultColor.getColorTypePrimary()).getColor();
		FOR_EACH_ENUM2(Civilization, eLoopCiv)
		{
			if (aiPlayersPerCiv.get(eLoopCiv) > 0)
				continue;
			float fDiffValue = 0;
			if (bRandomize)
			{
				/*	Since RGB values are stored as float, it's conceivable
					that different colors could get chosen on different machines
					in multiplayer. That should be OK, but I'd very much prefer for
					everyone to use the same colors, so I'm not going to use
					GC.getASyncRand. */
				fDiffValue += SyncRandNum(10000);
			}
			else
			{
				// Candidate color: primary color of an unused civ
				NiColorA const& kLoopColor = GC.getInfo(GC.getInfo(
						(PlayerColorTypes)GC.getInfo(eLoopCiv).
						getDefaultPlayerColor()).getColorTypePrimary()).getColor();
				fDiffValue += ::colorDifference(kTargetColor, kLoopColor);
				if (pTargetColor2 != NULL)
					fDiffValue += ::colorDifference(*pTargetColor2, kLoopColor);
			}
			if (fDiffValue < fSmallestDiff)
			{
				fSmallestDiff = fDiffValue;
				eBestCiv = eLoopCiv;
			}
		}
		FAssert(eBestCiv != NO_CIVILIZATION || MAX_PLAYERS > GC.getNumCivilizationInfos());
		if (eBestCiv != NO_CIVILIZATION)
		{
			GC.getInitCore().setColor(eReassignPlayer, (PlayerColorTypes)
					GC.getInfo(eBestCiv).getDefaultPlayerColor());
			aiPlayersPerCiv.add(eBestCiv, 1);
		}
		/*	(Else keep the colors assigned by the EXE. They're picked from the back
			of Civ4PlayerColorInfos.xml. Not guaranteed to be unique.) */
	}
}

// advc.127:
void CvGame::initGameHandicap()
{
	/*	K-Mod: Adjust the game handicap level to be the average
		of all the human player's handicap. (Note: in the original bts rules,
		it would always set to Noble if the humans had different handicaps) */
	// advc: Moved from setInitialItems b/c that function isn't called in scenarios
	if (isGameMultiPlayer())
	{
		int iSum = 0;
		PlayerIter<HUMAN> it;
		for (; it.hasNext(); ++it)
			iSum += GC.getInfo(it->getHandicapType())./* advc.250a: */getDifficulty();
		int const iDiv = it.nextIndex();
		if (iDiv > 0)
		{
			/*	advc.250a: Relies on no strange new handicaps being placed
				between Settler and Deity. Same in CvTeam::getHandicapType. */
				setHandicapType((HandicapTypes) /* kekm.22: */ intdiv::round(
						iSum, 10 * iDiv));
		}
		FAssertMsg(iDiv > 0, "All-AI game. Not necessarily wrong, but unexpected.");
	} // K-Mod end
	updateAIHandicap();
	// <advc.708>
	if (isOption(GAMEOPTION_RISE_FALL))
	{
		for (PlayerIter<MAJOR_CIV> itPlayer; itPlayer.hasNext(); ++itPlayer)
		{
			m_pRiseFall->setPlayerHandicap(itPlayer->getID(), itPlayer->isHuman(), true);
		}
		updateAIHandicap(); // (again)
	} // </advc.708>
}

// advc.127: Set m_eAIHandicap to the average of AI handicaps
void CvGame::updateAIHandicap()
{
	int iHandicapSum = 0;
	int iDiv = 0;
	FOR_EACH_ENUM(Player) // Cache for PlayerIter not yet available here
	{
		CvPlayer const& kPlayer = GET_PLAYER(eLoopPlayer);
		if (kPlayer.isAlive() && !kPlayer.isHuman() && kPlayer.isMajorCiv())
		{
			iHandicapSum += kPlayer.getHandicapType();
			iDiv++;
		}
	}
	if (iDiv > 0) // Leaves it at STANDARD_HANDICAP in all-human games
		m_eAIHandicap = (HandicapTypes)intdiv::uround(iHandicapSum, iDiv);
}


void CvGame::initFreeState()
{
	// <advc.106h>
	if (m_eInitialActivePlayer != NO_PLAYER)
		return; // advc.051: Don't init twice
	m_eInitialActivePlayer = getActivePlayer(); // </advc.106h>
	initGameHandicap(); // advc.127
	// <advc.084>
	if (getCivTeamsEverAlive() == 1)
	{
		FOR_EACH_ENUM(Victory)
		{
			CvVictoryInfo const& kLoopVictory = GC.getInfo(eLoopVictory);
			if (kLoopVictory.isConquest() || kLoopVictory.isDiploVote()
				/*	Domination victory isn't going to be fun, but let's
					let the player decide whether to disable it. */
				/*|| kLoopVictory.getPopulationPercentLead() > 0*/)
			{
				setVictoryValid(eLoopVictory, false);
			}
		}
	} // </advc.084>
	// <advc.250b>
	if (!isOption(GAMEOPTION_ADVANCED_START) ||
		PlayerIter<HUMAN>::count() == PlayerIter<CIV_ALIVE>::count())
	{
		setOption(GAMEOPTION_SPAH, false);
	}
	if (isOption(GAMEOPTION_SPAH))
		m_pSpah->setInitialItems(); // </advc.250b>
	if (GC.getInitCore().getScenario())
	{
		setScenario(true); // advc.052
		AI().AI_initScenario(); // advc.104u
	}
	else // advc.051: (Moved up.) Don't force 0 gold in scenarios
	{
		for (PlayerIter<ALIVE> it; it.hasNext(); ++it)
			it->initFreeState();
	}
	applyOptionEffects(); // advc.310
	AI().AI_updateVictoryWeights(); // advc.115f
	FOR_EACH_ENUM(Tech)
	{
		if (GC.getInfo(eLoopTech).getEra() < getStartEra()
			// disabled by K-Mod. (moved & changed. See below)
			/*|| GC.getInfo(getHandicapType()).isFreeTechs(eLoopTech)*/)
		{
			for (TeamIter<ALIVE> itTeam; itTeam.hasNext(); ++itTeam)
			{
				itTeam->setHasTech(eLoopTech, true, NO_PLAYER, false, false);
			}
		}
		// advc.tsl: Free techs from other sources now handled by initFreeCivState
	}
}

/*	advc.tsl: Freebies that shouldn't be initialized until starting sites have
	been assigned. In particular, freebies that depend on the civilization types.
	Based on code cut from initFreeState. */
void CvGame::initFreeCivState()
{	// <advc.250b>
	if (isOption(GAMEOPTION_SPAH))
		m_pSpah->rearrangeStartingPlots(); // </advc.250b>
	FOR_EACH_ENUM(Tech)
	{
		// <advc.126> Later-era free tech only for later-era starts.
		if (GC.getInfo(eLoopTech).getEra() > getStartEra())
			continue; // </advc.126>
		for (TeamIter<ALIVE> itTeam; itTeam.hasNext(); ++itTeam)
		{
			CvTeam& kTeam = *itTeam;
			bool bValid = false;
			if (!kTeam.isHuman() && GC.getInfo(getHandicapType()).isAIFreeTechs(eLoopTech) &&
				// advc.001: Barbarians receiving free AI tech might be a bug
				!kTeam.isBarbarian() /* advc.250c: */ && !isOption(GAMEOPTION_ADVANCED_START))
			{
				bValid = true;
			}
			if (!bValid)
			{
				for (MemberIter itMember(kTeam.getID()); itMember.hasNext(); ++itMember)
				{
					/*	<advc.250b>, advc.250c: Always grant civ-specific tech,
						but not tech from handicap if in Advanced Start except to
						human civs that don't actually start Advanced (SPaH option). */
					if (GC.getInfo(itMember->getCivilizationType()).
						isCivilizationFreeTechs(eLoopTech))
					{
						bValid = true;
						break;
					}
					// K-Mod: Give techs based on player handicap, not game handicap.
					if (GC.getInfo(itMember->getHandicapType()).isFreeTechs(eLoopTech) &&
						(!isOption(GAMEOPTION_ADVANCED_START) ||
						(isOption(GAMEOPTION_SPAH) && kTeam.isHuman()))) // </advc.250b>
					{
						bValid = true;
						break;
					}
				}
			}
			if (bValid) // (advc.051: Don't take away techs granted by scenario)
			{
				kTeam.setHasTech(eLoopTech, true, NO_PLAYER, false, false);
				// (advc: Already handled by setHasTech)
				/*if (GC.getInfo(eLoopTech).isMapVisible())
					GC.getMap().setRevealedPlots(kTeam.getID(), true, true);*/
			}
		}
	}
	// <advc.051>
	if (isScenario() && getStartEra() <= 0) // Set start era based on player era
	{
		int iEraSum = 0;
		PlayerIter<MAJOR_CIV> it;
		for (; it.hasNext(); ++it)
			iEraSum += it->getCurrentEra();
		int iStartEra = iEraSum / std::max(it.nextIndex(), 1);
		if (iStartEra > getStartEra())
			GC.getInitCore().setEra((EraTypes)iStartEra);
	} // </advc.051>
}


void CvGame::initScenario()
{
	initFreeState(); // Tech from handicap
	// <advc.tsl>
	if (isOption(GAMEOPTION_TRUE_STARTS) &&
		/*	Replacing fixed players should actually be OK -
			just so long as the scenario doesn't define any cities. */
		//GC.getInitCore().getWBMapNoPlayers()
		getNumCities() <= 0)
	{
		TrueStarts ts;
		ts.changeCivs();
		if (GC.getDefineBOOL(CvGlobals::TRUE_STARTS_SANITIZE_SCENARIOS))
			ts.sanitize();
	} // </advc.tsl>
	// <advc.030>
	if (GC.getDefineBOOL(CvGlobals::PASSABLE_AREAS))
	{
		/*	recalculateAreas can't handle preplaced cities. Or perhaps it can
			(Barbarian cities are fine in most cases), but there's going to
			be other stuff, like free units, that'll cause problems. */
		bool bRecalc = true;
		for (int i = 0; bRecalc && i < MAX_CIV_PLAYERS; i++)
		{
			if (GET_PLAYER((PlayerTypes)i).getNumCities() > 0)
				bRecalc = false;
		}
		if (bRecalc)
			GC.getMap().recalculateAreas();
	} // </advc.030>
	initFreeCivState(); // advc.tsl
}


void CvGame::initFreeUnits()
{
	bool const bScenario = GC.getInitCore().getScenario();
	/*	In scenarios, neither setInitialItems nor initFreeState is called; the
		EXE only calls initFreeUnits, so the initialization of freebies needs to
		happen here. */
	if (bScenario)
		initScenario();
	// kekm.28: exclude Barbarians
	for (PlayerIter<CIV_ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		if (itPlayer->getNumUnits() == 0 && itPlayer->getNumCities() == 0)
			itPlayer->initFreeUnits();
	}
	if (!bScenario)
		return;
	/*	<advc.250b> Advanced Start is always visible on the Custom Scenario screen,
		but doesn't work properly unless Advanced Start is the scenario's
		default setting. Verify that start points have been assigned, or else
		disable Advanced Start. */
	bool bValid = false;
	for (int i = 0; i < MAX_CIV_PLAYERS; i++)
	{
		CvPlayer const& kPlayer = GET_PLAYER((PlayerTypes)i);
		if (kPlayer.isAlive() && kPlayer.getAdvancedStartPoints() > 0)
		{
			bValid = true;
			break;
		}
	}
	if (!bValid)
	{
		setOption(GAMEOPTION_SPAH, false);
		setOption(GAMEOPTION_ADVANCED_START, false);
	} // </advc.250b>
} // </advc.051>

/*	advc.310: For building (or other) effects that only apply when certain
	game options are set. */
void CvGame::applyOptionEffects(bool bEnableAll)
{
	CvBuildingInfo::setDomesticGreatGeneralRateModifierEnabled(bEnableAll ||
			isOption(GAMEOPTION_RAGING_BARBARIANS) || isOption(GAMEOPTION_NO_BARBARIANS));
	CvBuildingInfo::setAreaTradeRoutesEnabled(bEnableAll ||
			!isOption(GAMEOPTION_RAGING_BARBARIANS) || isOption(GAMEOPTION_NO_BARBARIANS));
	CvBuildingInfo::setAreaBorderObstacleEnabled(bEnableAll ||
			!isOption(GAMEOPTION_NO_BARBARIANS));
}

// advc.027: Return value added; to be (safe-)deleted by caller.
NormalizationTarget* CvGame::assignStartingPlots()
{
	PROFILE_FUNC();
	CvMap const& kMap = GC.getMap();
	bool const bScenario = GC.getInitCore().getWBMapScript();
	/*	(advc: BtS code for handling scenarios deleted)
		K-Mod. Same functionality, but much faster and easier to read. */
	{
		/*	First, make a list of all the pre-marked starting plots on the map.
			advc (note): Normally, only scenarios can have such marked plots. */
		std::vector<CvPlot*> apStartingPlots;
		FOR_EACH_ENUM(PlotNum)
		{	// advc.opt: Shouldn't be necessary; the loop body is very fast.
			//gDLL->callUpdater(); // allow window updates during launch
			CvPlot& kLoopPlot = kMap.getPlotByIndex(eLoopPlotNum);
			if (kLoopPlot.isStartingPlot())
				apStartingPlots.push_back(&kLoopPlot);
		}
		// Now, randomly assign a starting plot to each player.
		for (PlayerIter<CIV_ALIVE> itPlayer; itPlayer.hasNext() &&
			apStartingPlots.size() > 0; ++itPlayer)
		{
			if (itPlayer->getStartingPlot() != NULL || // Already got one
				/*	advc.027: Don't assign one of the marked plots when the
					scenario has set the RandomStartLocation flag for the player */
				itPlayer->isRandomWBStart())
			{
				continue;
			}
			// advc.027b: instead of SyncRandNum
			int iRandOffset = MapRandNum(apStartingPlots.size());
			itPlayer->setStartingPlot(apStartingPlots[iRandOffset]/*, true*/); // advc.opt
			// remove this plot from the list.
			apStartingPlots[iRandOffset] = apStartingPlots[apStartingPlots.size() - 1];
			apStartingPlots.pop_back();
		}
	} // K-Mod end

	if (GC.getPythonCaller()->callMapFunction("assignStartingPlots"))
		return /* <advc.027> */ NULL;

	NormalizationTarget* pNormalizationTarget = NULL;
	/*	If the map script allows it, StartingPositionIteration will
		set starting sites that the code below may then reassign among the civs. */
	StartingPositionIteration spi;
	pNormalizationTarget = spi.createNormalizationTarget();
	// Apply SPI team assignment (no effect if SPI hasn't actually been executed)
	std::vector<CvPlot*> apStartsPerPlayer(MAX_CIV_PLAYERS);
	for (TeamIter<CIV_ALIVE> itTeam; itTeam.hasNext(); ++itTeam)
	{
		for (MemberIter itMember(itTeam->getID()); itMember.hasNext(); ++itMember)
		{
			apStartsPerPlayer[itMember->getID()] = spi.getTeamSite(
					itTeam->getID(), itMember.nextIndex() - 1);
		}
	}
	bool const bTeamGame = isTeamGame();
	bool bTeamAssignmentDone = bTeamGame;
	for (PlayerIter<CIV_ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		if (apStartsPerPlayer[itPlayer->getID()] != NULL)
			itPlayer->setStartingPlot(apStartsPerPlayer[itPlayer->getID()]);
		else
		{
			bTeamAssignmentDone = false;
			// SPI should do all the work or none
			FAssert(itPlayer.nextIndex() == 1 && pNormalizationTarget == NULL);
			break;
		}
	}
	// Reassignment of starting sites makes debugging harder
	if (pNormalizationTarget != NULL && spi.isDebug())
		return pNormalizationTarget; // </advc.027>
	if (bTeamGame)
	{
		if (!bTeamAssignmentDone) // advc.027
		{
			EagerEnumMap<PlayerTypes,bool> abPlayerDone; // advc
			// BtS team assignment
			for (int iPass = 0; iPass < 2 * MAX_PLAYERS; iPass++)
			{
				bool bStartFound = false;
				// advc.027b: instead of SyncRandNum
				int const iRandOffset = MapRandNum(countCivTeamsAlive());
				gDLL->callUpdater(); // advc
				for (int i = 0; i < MAX_CIV_TEAMS; i++)
				{
					TeamTypes eLoopTeam = (TeamTypes)((i + iRandOffset) % MAX_CIV_TEAMS);
					if (!GET_TEAM(eLoopTeam).isAlive())
						continue;
					for (MemberIter itMember(eLoopTeam); itMember.hasNext(); ++itMember)
					{
						if (abPlayerDone.get(itMember->getID()))
							continue;
						if (itMember->getStartingPlot() == NULL)
						{
							itMember->setStartingPlot(itMember->findStartingPlot()/*, true*/); // advc.opt
							abPlayerDone.set(itMember->getID(), true);
						}
						if (itMember->getStartingPlot() != NULL)
						{
							bStartFound = true;
							break;
						}
					}
				}
				if (!bStartFound)
					break;
			}
			#ifdef FASSERT_ENABLE
			for (PlayerIter<CIV_ALIVE> it; it.hasNext(); ++it)
			{
				FAssert(it->getStartingPlot() != NULL);
			}
			#endif
		}
		bool bRearrange = !bTeamAssignmentDone;
		/*	<advc.027> Run the BtS rearrangement code on top of SPI
			(though not across areas) when the continents are relatively large.
			(On archipelagic maps, I think the BtS code would do more harm than good
			b/c it doesn't take into account shallow-water connections.) */
		if (!bRearrange)
		{
			std::set<int> startingAreas;
			PlayerIter<CIV_ALIVE> itPlayer;
			for (; itPlayer.hasNext(); ++itPlayer)
				startingAreas.insert(itPlayer->getStartingPlot()->getArea().getID());
			if (2 * itPlayer.nextIndex() >= 7 * (int)startingAreas.size())
				bRearrange = true;
		} // </advc.027>
		if (bRearrange)
		{
			/*	advc: assignStartingPlots shouldn't get called for scenarios with
				fixed civs and leaders. (As far as I can tell, a scenario can only
				have fixed civs and leaders for all players, or for none.) */
			FAssert(!bScenario || GC.getInitCore().getWBMapNoPlayers());
			// advc.108b: Moved from normalizeStartingPlots
			if (!GC.getPythonCaller()->callMapFunction("normalizeStartingPlotLocations"))
			{
				rearrangeTeamStarts(
						// advc.027:
						bTeamAssignmentDone, bTeamAssignmentDone ? per100(15) : 0);
			}
		}
	}
	else // If map script [advc.027: and SPI] haven't set a plot
	{
		for (PlayerIter<CIV_ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
		{
			if (itPlayer->getStartingPlot() == NULL)
			{
				gDLL->callUpdater();
				itPlayer->setStartingPlot(itPlayer->findStartingPlot()/*, true*/); // advc.opt
			}
			if (itPlayer->getStartingPlot() == NULL)
			{
				FErrorMsg("No starting plot found");
				continue;
			}
		}
	}
	/*	advc.108b: Code moved into subroutine.
		advc.027 (note): Would be better to do this _after_ normalization.
		But that would require a NormalizationTarget member function for
		updating the start values. */
	applyStartingLocHandicaps(pNormalizationTarget);
	return (bScenario ? NULL : pNormalizationTarget); // advc.027
}

/*	advc.108b: Based on code cut from assignStartingPlots.
	Easier to implement this in a comparator.
	For sorting players in descending order of their team start values
	and, within a team, in descending order of the player start values. */
namespace
{
	class StartingSiteComparator
	{
	public:
		StartingSiteComparator(NormalizationTarget const* pStartValues)
		:	m_pStartValues(pStartValues)
		{}
		bool operator()(PlayerTypes ePlayer1, PlayerTypes ePlayer2) const
		{
			TeamTypes const eTeam1 = TEAMID(ePlayer1);
			TeamTypes const eTeam2 = TEAMID(ePlayer2);
			if (eTeam1 == eTeam2)
			{
				scaled rValue1 = playerStartValue(ePlayer1);
				scaled rValue2 = playerStartValue(ePlayer2);
				if (rValue1 == rValue2)
					return (ePlayer1 < ePlayer2);
				return (rValue1 > rValue2);
			}
			scaled rValue1 = teamStartValue(eTeam1);
			scaled rValue2 = teamStartValue(eTeam2);
			if (rValue1 == rValue2)
				return (eTeam1 < eTeam2);
			return (rValue1 > rValue2);
		}
	private:
		NormalizationTarget const* m_pStartValues;
		scaled playerStartValue(PlayerTypes ePlayer) const
		{
			CvPlot const* pStartPlot = GET_PLAYER(ePlayer).getStartingPlot();
			scaled r = -1;
			if (pStartPlot == NULL)
				return r;
			if (m_pStartValues == NULL)
			{
				/*	pStartPlot->getFoundValue(ePlayer) would be faster,
					but CvPlot::setFoundValue may not have been called
					(and then it returns 0). */
				r = GET_PLAYER(ePlayer).AI_foundValue(
						pStartPlot->getX(), pStartPlot->getY(), -1,
						false, true); // advc.027: bNormalize instead of bStartingLoc
				FAssertMsg(r.isPositive(), "Starting site likely unplayable");
				return r;
			}
			return m_pStartValues->getStartValue(*pStartPlot); // advc.027
		}
		scaled teamStartValue(TeamTypes eTeam) const
		{
			scaled r;
			for (MemberIter itMember(eTeam); itMember.hasNext(); ++itMember)
			{
				r += playerStartValue(itMember->getID());
			}
			return r;
		}
	};
}

// advc.108b: Cut from assignStartingPlots
void CvGame::applyStartingLocHandicaps(
	NormalizationTarget const* pStartValues) // advc.027
{
	/*	Replace all this. Don't want to ignore StartingLocPercent
		in multiplayer games, and the BtS random assignment of human starts
		didn't really work - had favored player 0 when humans are in slots 0, 1 ... */
	/*else if (isGameMultiPlayer()) {
		int iRandOffset = MapRandNum(PlayerIter<CIV_ALIVE>::count());
		// ... (deleted on 14 June 2020)
	}
	else
	{	// advc (comment): The minus 1 prevents humans from getting the worst plot
		int const iUpperBound = PlayerIter<CIV_ALIVE>::count() - 1;
		// ...
	}
	//std::vector<PlayerTypes>::iterator itPlayerOrder; //iterate over the player starts in the original order and re-place them.
	for (itPlayerOrder = aePlayerOrder.begin(); itPlayerOrder != aePlayerOrder.end(); ++itPlayerOrder)
		GET_PLAYER(*itPlayerOrder).setStartingPlot(GET_PLAYER(*playerOrderIter).findStartingPlot(), true);*/

	if (GC.getMap().isCustomMapOption("Historical") || // for EarthEvolution3 script
		isOption(GAMEOPTION_SPAH)) // advc.250b
	{
		return;
	}
	/*	The basic approach, as in K-Mod, is to sort the players by handicap,
		starting with the least handicapped player, and to sort the starting sites
		by value, starting with the best site. In the end, the sorted sites are
		assigned to the sorted players. */
	std::vector<PlayerTypes> aePlayersByHandicap; // ("PlayerOrder" in K-Mod)
	/*	First, order the teams according to handicap, then the members of each team.
		This way, the same algorithm works for team games and non-team games.
		(BtS had not taken StartingLoc handicaps into account in team games.) */
	std::vector<CvTeam*> apTeamsByHandicap;
	std::vector<std::pair<CvTeam*,int> > aStartingLocPercentPerTeam;
	// I don't think my approach can work when the teams don't have a uniform size
	int iTeamSize = 0;
	for (TeamIter<CIV_ALIVE> itTeam; itTeam.hasNext(); ++itTeam)
	{
		if (iTeamSize == 0)
			iTeamSize = itTeam->getNumMembers();
		else if (iTeamSize != itTeam->getNumMembers())
			return;
		int iStartingLocPercent = 0;
		MemberIter itMember(itTeam->getID());
		for (; itMember.hasNext(); ++itMember)
		{
			iStartingLocPercent += GC.getInfo(itMember->getHandicapType()).
					getStartingLocationPercent();
		}
		aStartingLocPercentPerTeam.push_back(std::make_pair(
				&*itTeam, intdiv::round(iStartingLocPercent, itMember.nextIndex())));
	}
	sortByStartingLocHandicap(aStartingLocPercentPerTeam, apTeamsByHandicap);
	for (size_t i = 0; i < apTeamsByHandicap.size(); i++)
	{
		std::vector<CvPlayer*> apMembersByHandicap;
		std::vector<std::pair<CvPlayer*,int> > aStartingLocPercentPerMember;
		for (MemberIter itMember(apTeamsByHandicap[i]->getID());
			itMember.hasNext(); ++itMember)
		{
			aStartingLocPercentPerMember.push_back(std::make_pair(
					&*itMember, GC.getInfo(itMember->getHandicapType()).
					getStartingLocationPercent()));
		}
		sortByStartingLocHandicap(aStartingLocPercentPerMember, apMembersByHandicap);
		for (size_t j = 0; j < apMembersByHandicap.size(); j++)
		{
			aePlayersByHandicap.push_back(apMembersByHandicap[j]->getID());
		}
	}

	std::vector<PlayerTypes> aePlayersByStartValue;
	for (PlayerIter<CIV_ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
		aePlayersByStartValue.push_back(itPlayer->getID());
	if (aePlayersByStartValue.size() != aePlayersByHandicap.size())
	{
		FAssert(aePlayersByStartValue.size() == aePlayersByHandicap.size());
		return;
	}
	{
		StartingSiteComparator comp(/* advc.027: */ pStartValues);
		std::sort(aePlayersByStartValue.begin(), aePlayersByStartValue.end(), comp);
	}
	std::vector<CvPlot*> apStartingSitesByValue;
	apStartingSitesByValue.reserve(aePlayersByStartValue.size());
	for (size_t i = 0; i < aePlayersByStartValue.size(); i++)
	{
		apStartingSitesByValue.push_back(GET_PLAYER(aePlayersByStartValue[i]).
				getStartingPlot());
	}
	// <advc.027> Try to avoid giving human players high-volatility starts
	if (pStartValues != NULL && aePlayersByHandicap.size() > 5u &&
		!isTeamGame())
	{
		for (size_t i = 0; i < aePlayersByHandicap.size(); i++)
		{
			PlayerTypes const ePlayer = aePlayersByHandicap[i];
			if (ePlayer == NO_PLAYER || !GET_PLAYER(ePlayer).isHuman())
				continue;
			CvPlot const* pStart = GET_PLAYER(ePlayer).getStartingPlot();
			if (pStart == NULL)
				continue;
			scaled rVolatility = pStartValues->getVolatilityValue(*pStart);
			if (rVolatility < fixp(0.2))
				continue;
			/*	Don't want to undercut the handicap bias too much. Hence look for
				a less volatile start only one up and one down in aePlayersByHandicap. */
			std::vector<std::pair<int,PlayerTypes> > aieSwapPlayers;
			if (i > 0)
			{
				aieSwapPlayers.push_back(std::make_pair((int)
						(i - 1), aePlayersByHandicap[i - 1]));
			}
			if (i < aePlayersByHandicap.size() - 1)
			{
				aieSwapPlayers.push_back(std::make_pair((int)
						(i + 1), aePlayersByHandicap[i + 1]));
			}
			int iBestSwapIndex = -1;
			// Tiny improvements in volatility aren't worth swapping for
			scaled rBestSwapVal = fixp(0.1);
			for (size_t j = 0; j < aieSwapPlayers.size(); j++)
			{
				PlayerTypes const eSwapPlayer = aieSwapPlayers[j].second;
				if (eSwapPlayer == NO_PLAYER || GET_PLAYER(eSwapPlayer).isHuman())
					continue;
				int const iSwapPlayerIndex = aieSwapPlayers[j].first;
				CvPlot const* pSwapStart = apStartingSitesByValue[iSwapPlayerIndex];
				if (pSwapStart == NULL)
					continue;
				scaled rSwapVolatility = pStartValues->getVolatilityValue(*pSwapStart);
				scaled rSwapVal = rVolatility - rSwapVolatility;
				if (rSwapVal > rBestSwapVal)
				{
					rBestSwapVal = rSwapVal;
					iBestSwapIndex = iSwapPlayerIndex;
				}
			}
			if (iBestSwapIndex >= 0)
			{
				std::swap(aePlayersByHandicap[i], aePlayersByHandicap[iBestSwapIndex]);
				if (iBestSwapIndex == i + 1)
					i++; // Skip next iteration to make sure not to swap again
			}
		}
	} // </advc.027>
	for (size_t i = 0; i < aePlayersByHandicap.size(); i++)
	{
		if (aePlayersByHandicap[i] == NO_PLAYER ||
			apStartingSitesByValue[i] == NULL)
		{
			FErrorMsg("Failed to apply StartingLoc handicap");
			continue;
		}
		GET_PLAYER(aePlayersByHandicap[i]).setStartingPlot(apStartingSitesByValue[i]);
	}
}

/*	advc.108b: Based on BtS code cut from assignStartingPlots.
	The Agent type can be either CvPlayer or CvTeam. The agents have to be
	alive and non-Barbarian. kResult should be empty before the call. */
template<class Agent>
void CvGame::sortByStartingLocHandicap(
	std::vector<std::pair<Agent*,int> > const& kStartingLocPercentPerAgent,
	std::vector<Agent*>& kResult)
{
	int const iAgents = kStartingLocPercentPerAgent.size();
	int iHumanAgents = 0;
	for (int i = 0; i < iAgents; i++)
	{
		if (kStartingLocPercentPerAgent[i].first->isHuman())
			iHumanAgents++;
	}
	int const iAIAgents = iAgents - iHumanAgents;
	FAssert(kResult.empty());
	kResult.resize(iAgents, NULL);
	for (int iPass = 0; iPass < 2; iPass++)
	{
		bool bHuman = (iPass == 0);
		int iLoopAgents = (bHuman ? iHumanAgents : iAIAgents);
		int iRandOffset = MapRandNum(iLoopAgents);
		int iSkipped = 0;
		for (int i = 0; i < iAgents; i++)
		{
			if (kStartingLocPercentPerAgent[i].first->isHuman() == bHuman)
			{
				if (iSkipped < iRandOffset)
				{
					iSkipped++;
					continue;
				}
				/*	This sets iRandOffset to the index of a random human agent
					in the first pass, and a random AI agent in the second. */
				iRandOffset = i;
				break;
			}
		}
		for (int i = 0; i < iAgents; i++)
		{
			std::pair<Agent*,int> piLoopPair = kStartingLocPercentPerAgent[i];
			Agent& kAgent = *piLoopPair.first;
			if (kAgent.isHuman() != bHuman)
				continue;
			int iPos = ::range((iAgents * piLoopPair.second) / 100, 0, iAgents - 1);
			if (kResult[iPos] != NULL) // If pos already taken
			{
				for (int j = 1; j < std::max(iPos + 1, iAgents - iPos); j++)
				{
					// Alternate between better and worse positions
					if (iPos + j < iAgents && kResult[iPos + j] == NULL)
					{
						iPos += j;
						break;
					}
					if (iPos - j >= 0 && kResult[iPos - j] == NULL)
					{
						iPos -= j;
						break;
					}
				}
				FAssert(kResult[iPos] == NULL);
			}
			kResult[iPos] = &kAgent;
		}
	}
}

/*	Swaps starting locations until we have reached the
	optimal closeness between teams. (caveat: this isn't quite "optimal"
	because we could get stuck in local minima, but it's pretty good.)
	advc: Renamed from "normalizeStartingPlotLocations". No longer part of the
	normalization step. Refactored, but the code structure is still as in BtS. */
void CvGame::rearrangeTeamStarts(/* advc.027: */ bool bOnlyWithinArea, scaled rInertia)
{	// <advc.opt> This function is only for team games
	if (!isTeamGame())
		return; // </advc.opt>
	CvMap const& kMap = GC.getMap();
	// Precompute distances between all starting sites
	ArrayEnumMap2D<PlayerTypes,PlayerTypes,int> aaiDistances;
	for (PlayerIter<CIV_ALIVE> itFirstPlayer; itFirstPlayer.hasNext(); ++itFirstPlayer)
	{
		gDLL->callUpdater(); // allow window to update during launch
		CvPlot* pFirstStart = itFirstPlayer->getStartingPlot();
		if (pFirstStart == NULL)
			continue;
		PlayerTypes const eFirst = itFirstPlayer->getID();
		for (PlayerIter<CIV_ALIVE> itSecondPlayer; itSecondPlayer.hasNext();
			++itSecondPlayer)
		{
			CvPlot* pSecondStart = itSecondPlayer->getStartingPlot();
			if (pSecondStart == NULL)
				continue;
			PlayerTypes const eSecond = itSecondPlayer->getID();
			if (eSecond < eFirst)
				continue;
			int iDist = kMap.calculatePathDistance(pFirstStart, pSecondStart);
			if (iDist == -1)
			{
				iDist = kMap.plotDistance(pFirstStart, pSecondStart);
				/*	advc.027: The BtS penalty below is (presumably) mainly intended
					as an incentive for putting sites of the same team in the same area.
					But it also provides a strong incentive for minimizing distances
					between team sites in different areas when it's not possible
					to put them all in one area. (Especially) don't want this
					side-effect when swaps between areas aren't allowed. */
				if (!bOnlyWithinArea)
					iDist *= 5;
			}
			aaiDistances.set(eFirst, eSecond, iDist);
			aaiDistances.set(eSecond, eFirst, iDist);
		}
	}

	std::vector<PlayerTypes> aeStartingLocs(MAX_CIV_PLAYERS);
	// each player starting in own location
	std11::iota(aeStartingLocs.begin(), aeStartingLocs.end(), (PlayerTypes)0);

	int iBestScore = getTeamClosenessScore(aaiDistances, aeStartingLocs);
	bool bFoundSwap = true;
	while (bFoundSwap)
	{	/*	<advc.027> I worry that going through the players in turn order
			can lead to biases toward or against the (human) team of player 0.
			(Not using PlayerRandIter b/c I want the outer and inner loop
			to use the same order.) */
		int aiPlayersShuffled[MAX_CIV_PLAYERS];
		getMapRand().shuffle(aiPlayersShuffled, MAX_CIV_PLAYERS); // </advc.027>
		bFoundSwap = false;
		for (int i = 0; i < MAX_CIV_PLAYERS; i++)
		{
			CvPlayer& kFirst = GET_PLAYER((PlayerTypes)aiPlayersShuffled[i]); // advc.027
			if (!kFirst.isAlive())
				continue;
			for (int j = 0; j < /* advc.027: */ i; j++)
			{
				CvPlayer& kSecond = GET_PLAYER((PlayerTypes)aiPlayersShuffled[j]); // advc.027
				if (!kSecond.isAlive())
					continue;
				// <advc.027>
				if (bOnlyWithinArea &&
					// (The rest of this function also tolerates NULL starts)
					kFirst.getStartingPlot() != NULL && kSecond.getStartingPlot() != NULL &&
					!kFirst.getStartingPlot()->sameArea(*kSecond.getStartingPlot()))
				{
					continue;
				} // </advc.027>
				std::swap(aeStartingLocs[kFirst.getID()],
						aeStartingLocs[kSecond.getID()]);
				int iScore = getTeamClosenessScore(aaiDistances, aeStartingLocs);
				if (iScore * (1 + rInertia) < iBestScore) // advc.027: inertia
				{
					iBestScore = iScore;
					bFoundSwap = true;
				}
				else
				{	// undo
					std::swap(aeStartingLocs[kSecond.getID()],
							aeStartingLocs[kFirst.getID()]);
				}
			}
		}
	}

	std::vector<CvPlot*> apNewStartPlots(MAX_CIV_PLAYERS, NULL);
	for (PlayerIter<CIV_ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		PlayerTypes const ePlayer = itPlayer->getID();
		if (aeStartingLocs[ePlayer] != ePlayer)
		{
			apNewStartPlots[ePlayer] = GET_PLAYER(aeStartingLocs[ePlayer]).
					getStartingPlot();
		}
	}
	for (PlayerIter<CIV_ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		PlayerTypes const ePlayer = itPlayer->getID();
		if (apNewStartPlots[ePlayer] != NULL)
			GET_PLAYER(ePlayer).setStartingPlot(apNewStartPlots[ePlayer]);
	}
}

/*	For each of n teams, let the closeness score for that team be the
	average distance of an edge between two players on that team.
	This function calculates the closeness score for each team and
	returns the sum of those n scores. The lower the result, the better "clumped"
	the players' starting locations are.
	Note: for the purposes of this function, player i will be assumed to start
	in the location of player kStartingLocs[i] */
int CvGame::getTeamClosenessScore( // advc: params used to be arrays
	ArrayEnumMap2D<PlayerTypes,PlayerTypes,int> const& kDistances,
	std::vector<PlayerTypes> const& kStartingLocs)
{
	int iScore = 0;
	for (TeamIter<CIV_ALIVE> itTeam; itTeam.hasNext(); ++itTeam)
	{
		int iTeamTotalDist = 0;
		int iNumEdges = 0;
		for (MemberIter itFirstMember(itTeam->getID()); itFirstMember.hasNext();
			++itFirstMember)
		{
			for (MemberIter itSecondMember(itTeam->getID()); itSecondMember.hasNext();
				++itSecondMember)
			{
				PlayerTypes const eFirst = itFirstMember->getID();
				PlayerTypes const eSecond = itSecondMember->getID();
				if (eFirst <= eSecond)
					continue;
				// Add the edge between these two players that are on the same team
				iNumEdges++;
				PlayerTypes eFirstStart = kStartingLocs.at(eFirst);
				PlayerTypes eSecondStart = kStartingLocs.at(eSecond);
				if (eFirstStart < eSecondStart) // Ensure eFirstStart > eSecondStart
					std::swap(eFirstStart, eSecondStart);
				else FAssertMsg(eFirstStart != eSecondStart,
						"Two players are (hypothetically) assigned to the same starting location!");
				FAssertMsg(kDistances.get(eFirstStart, eSecondStart) > 0, "Distance not computed?"); // advc
				iTeamTotalDist += kDistances.get(eFirstStart, eSecondStart);
			}
		}
		int iTeamScore;
		if (iNumEdges == 0)
			iTeamScore = 0;
		else
		{
			// The avg distance between team edges is the team score
			iTeamScore = intdiv::uround(iTeamTotalDist, iNumEdges);
		}
		iScore += iTeamScore;
	}
	return iScore;
}

// <advc.108>
void CvGame::setStartingPlotNormalizationLevel(StartingPlotNormalizationLevel eLevel)
{
	if (eLevel == NORMALIZE_DEFAULT)
	{
		eLevel = (GC.getDefineBOOL("NORMALIZE_STARTPLOTS_AGGRESSIVELY") ?
				NORMALIZE_HIGH : NORMALIZE_LOW);
		if (eLevel == NORMALIZE_LOW && isGameMultiPlayer() &&
			TeamIter<HUMAN>::count() > 1)
		{
			eLevel = NORMALIZE_MEDIUM;
		}
	}
	m_eNormalizationLevel = eLevel;
}

/*	(Note: Only for external callers.
	Within CvGame, m_eNormalizationLevel gets accessed directly.) */
CvGame::StartingPlotNormalizationLevel CvGame::getStartingPlotNormalizationLevel() const
{
	return m_eNormalizationLevel;
} // </advc.108

// advc.opt: Replacing CvPlayer::startingPlotRange. Now cached.
int CvGame::getStartingPlotRange() const
{
	if (m_iStartingPlotRange <= 0)
		updateStartingPlotRange();
	return m_iStartingPlotRange;
}


void CvGame::normalizeAddRiver()
{
	CvMap const& kMap = GC.getMap();
	for (PlayerIter<CIV_ALIVE> it; it.hasNext(); ++it)
	{
		CvPlayer const& kLoopPlayer = *it;
		CvPlot* pStartingPlot = kLoopPlayer.getStartingPlot();
		if (pStartingPlot == NULL)
			continue;
		if (pStartingPlot->isFreshWater() ||
			// <advc.108>
			(m_eNormalizationLevel <= NORMALIZE_LOW &&
			pStartingPlot->isAdjacentFreshWater())) // </advc.108>
		{
			continue;
		}
		// if we will be able to add a lake, then use old river code
		if (normalizeFindLakePlot(kLoopPlayer.getID()) != NULL)
		{
			//CvMapGenerator::GetInstance().doRiver(pStartingPlot);
			/*	K-Mod. If we can have a lake then we don't always need a river.
				Also, the river shouldn't always start on the SE corner of our site. */
			if (//SyncRandNum(10) < (pStartingPlot->isCoastalLand() ? 5 : 7))
				/*	<advc.108> The above is a 50% lake chance when coastal, 30% otherwise.
					(Will also get a lake when no river possible or a lake already happens
					to be present.) Note that a coastal river normally has only one segment.
					Want to reduce the lake chance and coastal bias a bit. */
				MapRandSuccess(pStartingPlot->isCoastalLand() ? fixp(0.62) : fixp(0.74)))
			{	// </advc.108>
				CvPlot* pRiverPlot = pStartingPlot->getInlandCorner();
				if (pRiverPlot != NULL)
					CvMapGenerator::GetInstance().doRiver(pRiverPlot);
			} // K-Mod end.
		} // otherwise, use new river code which is much more likely to succeed
		else CvMapGenerator::GetInstance().addRiver(pStartingPlot);

		// add floodplains to any desert tiles the new river passes through
		FOR_EACH_ENUM(PlotNum)
		{
			CvPlot& kPlot = kMap.getPlotByIndex(eLoopPlotNum);
			// advc.108: Can't hurt to randomize the order
			FOR_EACH_ENUM_RAND(Feature, getMapRand())
			{
				if (!GC.getInfo(eLoopFeature).isRequiresRiver() ||
					!kPlot.canHaveFeature(eLoopFeature))
				{
					continue;
				}
				//if (GC.getInfo(eLoopFeature).getAppearanceProbability() == 10000)
				// <advc.108> Cleaner to do the proper dice roll
				if (MapRandSuccess(per10000(GC.getInfo(eLoopFeature).
					getAppearanceProbability())))
				{	// </advc.108>
					if (kPlot.getBonusType() != NO_BONUS)
						kPlot.setBonusType(NO_BONUS);
					kPlot.setFeatureType(eLoopFeature);
					break;
				}
			}
		}
	}
}


void CvGame::normalizeRemovePeaks()
{
	// <advc.108>
	scaled rRemovalProb = 1;
	if (m_eNormalizationLevel <= NORMALIZE_LOW)
		rRemovalProb = per100(GC.getDefineINT("REMOVAL_CHANCE_PEAK"));
	// </advc.108>

	for (PlayerIter<CIV_ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		CvPlot* pStartingPlot = itPlayer->getStartingPlot();
		if (pStartingPlot == NULL)
			continue;
		// advc 027 (note): Range corresponds to AIFoundValue::adjustToLandAreaBoundary
		for (SquareIter itPlot(*pStartingPlot, 3); itPlot.hasNext(); ++itPlot)
		{
			if (itPlot->isPeak() && /* advc.108: */ MapRandSuccess(rRemovalProb))
				itPlot->setPlotType(PLOT_HILLS);
		}
	}
}


void CvGame::normalizeAddLakes()
{
	for (PlayerIter<CIV_ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{	// <advc> (Moved out of normalizeFindLakePlot)
		CvPlot* pStartingPlot = itPlayer->getStartingPlot();
		if (pStartingPlot == NULL || pStartingPlot->isFreshWater() || // </advc>
			// <advc.108>
			(m_eNormalizationLevel <= NORMALIZE_LOW &&
			pStartingPlot->isAdjacentFreshWater())) // </advc.108>
		{
			continue;
		}
		CvPlot* pLakePlot = normalizeFindLakePlot(itPlayer->getID());
		if (pLakePlot != NULL)
			pLakePlot->setPlotType(PLOT_OCEAN);
	}
}

/*	K-Mod: Shuffle the plots - advc.108: Randomize, yes,
	but the inner ring has to take precedence. Rewritten.
	(The K-Mod behavior was intentional though according to a CFC post.) */
CvPlot* CvGame::normalizeFindLakePlot(PlayerTypes ePlayer)
{
	CvPlot const& kStart = *GET_PLAYER(ePlayer).getStartingPlot();
	FOR_EACH_ADJ_PLOT_VAR_RAND(kStart, getMapRand())
	{
		if (normalizeCanAddLakeTo(*pAdj))
			return pAdj;
	}
	if (kStart.isAdjacentFreshWater())
		return NULL;
	for (CityPlotRandIter itPlot(kStart, getMapRand(), false);
		itPlot.hasNext(); ++itPlot)
	{
		if (itPlot.currID() < NUM_INNER_PLOTS)
			continue;
		if (normalizeCanAddLakeTo(*itPlot))
			return &*itPlot;
	}
	return NULL;
}

// advc.108: Cut from normalizeFindLakePlot
bool CvGame::normalizeCanAddLakeTo(CvPlot const& kPlot) const
{
	if (kPlot.isWater() || kPlot.isCoastalLand() ||
		kPlot.isRiver() || kPlot.getBonusType() != NO_BONUS)
	{
		return false;
	}
	for (PlayerIter<CIV_ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		if (itPlayer->getStartingPlot() == &kPlot)
			return false;
	}
	return true;
}


void CvGame::normalizeRemoveBadFeatures()
{
	// advc.108:
	int const iThreshBadFeatPerCity = GC.getDefineINT("THRESH-BAD-FEAT-PER-CITY");

	for (PlayerIter<CIV_ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		CvPlot* pStartingPlot = itPlayer->getStartingPlot();
		if (pStartingPlot == NULL)
			continue;
		// <advc.108>
		int iBadFeatures = 0;
		for (CityPlotIter itPlot(*pStartingPlot); itPlot.hasNext(); ++itPlot)
		{
			// Disregard inner ring later
			if (itPlot.currID() < NUM_INNER_PLOTS || !itPlot->isFeature())
				continue;
			if (GC.getInfo(itPlot->getFeatureType()).getYieldChange(YIELD_FOOD) <= 0 &&
				GC.getInfo(itPlot->getFeatureType()).getYieldChange(YIELD_PRODUCTION) <= 0)
			{
				iBadFeatures++;
			}
		}
		{
			scaled rRemovalProb;
			if (iBadFeatures > iThreshBadFeatPerCity)
			{
				rRemovalProb = 1 - m_eNormalizationLevel *
						scaled(iThreshBadFeatPerCity, iBadFeatures);
			}
			if (m_eNormalizationLevel >= NORMALIZE_HIGH)
				rRemovalProb = 1;
			// </advc.108>
			for (CityPlotIter itPlot(*pStartingPlot); itPlot.hasNext(); ++itPlot)
			{
				CvPlot& p = *itPlot;
				if (!p.isFeature())
					continue;
				if (GC.getInfo(p.getFeatureType()).getYieldChange(YIELD_FOOD) <= 0 &&
					GC.getInfo(p.getFeatureType()).getYieldChange(YIELD_PRODUCTION) <= 0)
				{
					// <advc.108>
					if (itPlot.currID() < NUM_INNER_PLOTS ||
						(!isPowerfulStartingBonus(p, itPlayer->getID()) &&
						(MapRandSuccess(rRemovalProb) ||
						isWeakStartingFoodBonus(p, itPlayer->getID()))))
					{	// </advc.108>
						p.setFeatureType(NO_FEATURE);
					}
				}
			}
		}
		int const iCityRange = CITY_PLOTS_RADIUS;
		for (PlotCircleIter itPlot(*pStartingPlot, iCityRange + 2);
			itPlot.hasNext(); ++itPlot)
		{
			CvPlot& p = *itPlot;
			int iDistance = itPlot.currPlotDist();
			if (p.isFeature() &&
				GC.getInfo(p.getFeatureType()).getYieldChange(YIELD_FOOD) <= 0 &&
				GC.getInfo(p.getFeatureType()).getYieldChange(YIELD_PRODUCTION) <= 0)
			{
				if (p.isWater())
				{
					if (p.isAdjacentToLand() || (iDistance <= iCityRange + 1 &&
						// advc.027b: instead of SyncRandSuccess
						MapRandSuccess(fixp(0.5))))
					{
						p.setFeatureType(NO_FEATURE);
					}
				}
				else if (iDistance <= iCityRange + 1)
				{
					scaled rRemovalProb(1, 2);
					if (m_eNormalizationLevel > NORMALIZE_MEDIUM) // advc.108
					{	/*	Smaller pr when there is a resource. I wonder if that's
							really what the BtS programmer meant to do. */
						//SyncRandNum(2 + (p.getBonusType() == NO_BONUS ? 0 : 2)) == 0)
						if (p.getBonusType() != NO_BONUS)
							rRemovalProb = scaled(1, 4);
					}
					// <advc.108>
					else if (p.getBonusType() == NO_BONUS)
						rRemovalProb = scaled(1, 3); // </advc.108>
					// advc.027b: instead of SyncRandNum
					if (MapRandSuccess(rRemovalProb))
						p.setFeatureType(NO_FEATURE);
				}
			}
		}
	}
}


void CvGame::normalizeRemoveBadTerrain()
{
	// <advc.108>
	scaled rKeepProb;
	if (m_eNormalizationLevel <= NORMALIZE_LOW)
		rKeepProb = 1 - per100(GC.getDefineINT("REMOVAL_CHANCE_BAD_TERRAIN"));
	// </advc.108>
	int const iCityRange = CITY_PLOTS_RADIUS;
	for (PlayerIter<CIV_ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		CvPlot* pStartingPlot = itPlayer->getStartingPlot();
		if (pStartingPlot == NULL)
			continue;
		for (PlotCircleIter itPlot(*pStartingPlot, iCityRange + 1);
			itPlot.hasNext(); ++itPlot)
		{
			CvPlot& p = *itPlot;
			int iDistance = itPlot.currPlotDist();
			if (!p.isWater() && (iDistance <= iCityRange ||
				p.isCoastalLand() ||
				MapRandSuccess(scaled(1, 1 + iDistance - iCityRange))))
			{
				CvTerrainInfo const& kTerrain = GC.getInfo(p.getTerrainType());
				int iPlotFood = kTerrain.getYield(YIELD_FOOD);
				int iPlotProduction = kTerrain.getYield(YIELD_PRODUCTION);
				if (iPlotFood + iPlotProduction > 1)
					continue;
				// <advc.108>
				if (isPowerfulStartingBonus(p, itPlayer->getID()))
					continue;
				/*	I think the BtS code ends up replacing Desert with Desert when
					there's a feature, but let's rather handle Desert features explicitly. */
				if (p.isFeature() &&
					GC.getInfo(p.getFeatureType()).
					getYieldChange(YIELD_FOOD) + iPlotFood >= 2)
				{
					continue;
				}
				if (MapRandSuccess(rKeepProb))
				{
					if (iPlotFood > 0 ||
					/*	advc.129b: Two chances of removal for Snow river
						(BuildModifier=50), but not for Desert river. */
						(p.isRiver() && kTerrain.getBuildModifier() < 30) ||
						MapRandSuccess(rKeepProb))
					{
						if (!isWeakStartingFoodBonus(p, itPlayer->getID()))
							continue;
					}
				} // </advc.108>
				int const iTargetTotal = 2;
				int iTargetFood=0;
				if (p.getBonusType(itPlayer->getTeam()) != NO_BONUS)
					iTargetFood = 1;
				else if (iPlotFood == 1 || iDistance <= iCityRange)
				{	// advc.027b: instead of SyncRandNum
					iTargetFood = 1 + MapRandNum(2);
				}
				else iTargetFood = (p.isCoastalLand() ? 2 : 1);
				FOR_EACH_ENUM(Terrain)
				{
					CvTerrainInfo const& kRepl = GC.getInfo(eLoopTerrain);
					if (kRepl.isWater())
						continue;
					if (kRepl.getYield(YIELD_FOOD) == iTargetFood && // advc.108: was >=
						kRepl.getYield(YIELD_FOOD) +
						kRepl.getYield(YIELD_PRODUCTION) == iTargetTotal)
					{
						if (!p.isFeature() ||
							GC.getInfo(p.getFeatureType()).isTerrain(eLoopTerrain))
						{
							p.setTerrainType(eLoopTerrain);
							break; // advc.108
						}
					}
				}
			}
		}
	}
}


void CvGame::normalizeAddFoodBonuses(/* advc.027: */ NormalizationTarget const* pTarget)
{
	bool const bIgnoreLatitude = GC.getPythonCaller()->isBonusIgnoreLatitude();
	int const iFoodPerPop = GC.getFOOD_CONSUMPTION_PER_POPULATION(); // K-Mod

	for (PlayerIter<CIV_ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		CvPlayer const& kPlayer = *itPlayer;
		CvPlot const* pStartingPlot = kPlayer.getStartingPlot();
		if (pStartingPlot == NULL)
			continue;

		int iFoodBonus = 0;
		int iGoodNatureTileCount = 0;
		// K-Mod. Don't count the city plot.
		for (CityPlotIter itPlot(*pStartingPlot, false); itPlot.hasNext(); ++itPlot)
		{
			CvPlot& p = *itPlot;
			BonusTypes eBonus = p.getBonusType(kPlayer.getTeam());
			if (eBonus == NO_BONUS)
			{
				if (p.calculateBestNatureYield(YIELD_FOOD, kPlayer.getTeam()) >=
					iFoodPerPop + 1)
				{
					iGoodNatureTileCount++;
				}
				continue;
			}
			CvBonusInfo const& kBonus = GC.getInfo(eBonus);
			if (kBonus.getYieldChange(YIELD_FOOD) <= 0)
			{
				if (p.calculateBestNatureYield(YIELD_FOOD, kPlayer.getTeam()) >=
					iFoodPerPop)
				{
					iGoodNatureTileCount++;
				}
				continue;
			}
			if (kBonus.getTechCityTrade() != NO_TECH &&
				GC.getInfo(kBonus.getTechCityTrade()).getEra() > getStartEra())
			{
				continue;
			}
			// <advc.001> Whale
			TechTypes eTechImprove = kBonus.getTechImprove(p.isWater());
			if (eTechImprove != NO_TECH &&
				GC.getInfo(eTechImprove).getEra() > getStartEra())
			{
				continue;
			} // </advc.001>
			if (p.isWater())
			{
				iFoodBonus += 2;
				// <advc.108>
				if (p.isAdjacentToLand())
					iFoodBonus++; // </advc.108>
				continue;
			}
			//iFoodBonus += 3;
			/*	K-Mod. Bonus which only give 3 food with their improvement
				should not be worth 3 points.
				(ie. plains-cow should not be the only food resource.) */
			/* first attempt - this doesn't work, because "max yield"
				essentially means +2 food on any plot. That isn't what we want. */
			/*if (p.calculateMaxYield(YIELD_FOOD) >= 2*iFoodPerPop)
				iFoodBonus += 3;
			else iFoodBonus += 2;*/
			int const iHighFoodThreshold = 2 * iFoodPerPop;
			int const iNaturalFood = p.calculateBestNatureYield(YIELD_FOOD, kPlayer.getTeam());
			// (+1 just as a shortcut to save time for obvious cases.)
			bool bHighFood = (iNaturalFood + 1 >= iHighFoodThreshold);
			FOR_EACH_ENUM2(Improvement, eImp)
			{
				if (bHighFood)
					break;
				if (GC.getInfo(eImp).isImprovementBonusTrade(eBonus))
				{
					bHighFood = (iNaturalFood + p.calculateImprovementYieldChange(
							eImp, YIELD_FOOD, kPlayer.getID()) >=
							iHighFoodThreshold);
				}
			}
			iFoodBonus += (bHighFood ? 3 : 2);
			// K-Mod end
		}

		int iTargetFoodBonusCount = 3;
		// <advc.027>
		bool bTargetReached = (pTarget != NULL &&
				pTarget->isReached(*pStartingPlot)); // </advc.027>
		iTargetFoodBonusCount += std::max(0, 2 - iGoodNatureTileCount); // K-Mod
		// <advc.108> Randomize order of traversal but (much) prefer the inner ring
		for (int iOuterPass = 0; iOuterPass < 2; iOuterPass++)
		{
			bool const bInnerRingBias = (iOuterPass == 0);
			for (CityPlotRandIter itPlot(*pStartingPlot, getMapRand(), false);
				itPlot.hasNext() && // </advc.108>
			/*	K-Mod. I've rearranged a couple of things to make it a bit
				more efficient and easier to read. */
				iFoodBonus < iTargetFoodBonusCount - /* advc.027: */ (bTargetReached ? 1 : 0);
				++itPlot)
			{	// <advc.108>
				if (bInnerRingBias && itPlot.currID() >= NUM_INNER_PLOTS &&
					MapRandSuccess(fixp(0.63)))
				{
					continue;
				} // </advc.108>
				CvPlot& p = *itPlot;
				if (p.getBonusType() != NO_BONUS || /* advc.004z: */ p.isGoody() ||
					// advc.108 (from PerfectWorld 2)
					(!p.sameArea(*pStartingPlot) && !p.isWater()))
				{
					continue;
				}
				// <adcv.108>
				for (int iPass = 0; iPass < 2; iPass++)
				{
					bool const bInitialPass = (iPass == 0); // </advc.108>
					// advc.129: Randomize the order in which resources are considered
					FOR_EACH_ENUM_RAND(Bonus, getMapRand())
					{
						if (GC.getInfo(eLoopBonus).getYieldChange(YIELD_FOOD) <= 0)
							continue;
						/*	advc.108: Let map generator check canPlaceBonusAt in the
							initial pass (same as in normalizeAddExtras) */
						if (!isNormalizationBonus(eLoopBonus, kPlayer.getID(), p,
							bInitialPass, !bInitialPass || bIgnoreLatitude))
						{
							continue;
						}
						// <advc.108>
						// Don't place the food resource on a bad feature
						FeatureTypes const eFeature = p.getFeatureType();
						bool bValid = true;
						if (eFeature != NO_FEATURE)
						{
							CvFeatureInfo const& kFeature = GC.getInfo(eFeature);
							bValid = false;
							if (m_eNormalizationLevel >= NORMALIZE_HIGH ||
								kFeature.getYieldChange(YIELD_FOOD) > 0 ||
								kFeature.getYieldChange(YIELD_PRODUCTION) > 0)
							{
								bValid = true;
							}
						}
						if (!bValid)
							continue;
						if (bInitialPass &&
							skipDuplicateNormalizationBonus(*pStartingPlot, p, eLoopBonus))
						{	// </advc.108>
							continue;
						}
						p.setBonusType(eLoopBonus);
						if (gMapLogLevel > 0) logBBAI("	  Adding food bonus %S for player %d", GC.getInfo(eLoopBonus).getDescription(), itPlayer->getID()); // advc
						if (p.isWater())
							iFoodBonus += 2;
						else
						{
							//iFoodBonus += 3;
							// K-Mod
							int const iNaturalFood = p.calculateBestNatureYield(
									YIELD_FOOD, kPlayer.getTeam());
							int const iHighFoodThreshold = 2 * iFoodPerPop;
							// (+1 just as a shortcut to save time for obvious cases.)
							bool bHighFood = (iNaturalFood + 1 >= iHighFoodThreshold);
							FOR_EACH_ENUM(Improvement)
							{
								if (GC.getInfo(eLoopImprovement).
									isImprovementBonusTrade(eLoopBonus))
								{
									bHighFood = (iNaturalFood +
											p.calculateImprovementYieldChange(
											eLoopImprovement, YIELD_FOOD, kPlayer.getID()) >=
											iHighFoodThreshold);
								}
							}
							iFoodBonus += (bHighFood ? 3 : 2);
						} // K-Mod end
						// advc.027:
						bTargetReached = (pTarget != NULL && pTarget->isReached(*pStartingPlot));
						break;
					}  // <advc.108> Don't do 2nd pass if 1st pass has succeeded
					if (p.getBonusType() != NO_BONUS)
						break; // </advc.108>
				}
			}
		}
	}
}


void CvGame::normalizeAddGoodTerrain()
{
	// <advc.108>
	if (m_eNormalizationLevel <= NORMALIZE_LOW)
		return; // </advc.108>

	for (PlayerIter<CIV_ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		CvPlayer const& kPlayer = *itPlayer;
		CvPlot* pStartingPlot = kPlayer.getStartingPlot();
		if (pStartingPlot == NULL)
			continue;

		int iGoodPlot = 0;
		for (CityPlotIter itPlot(*pStartingPlot, false); itPlot.hasNext(); ++itPlot)
		{
			if ((itPlot->calculateNatureYield(YIELD_FOOD, kPlayer.getTeam()) >=
				GC.getFOOD_CONSUMPTION_PER_POPULATION()) &&
				(itPlot->calculateNatureYield(YIELD_PRODUCTION, kPlayer.getTeam()) > 0))
			{
				iGoodPlot++;
			}
		}
		for (CityPlotIter itPlot(*pStartingPlot, false); itPlot.hasNext() &&
			iGoodPlot < 4; ++itPlot)
		{
			CvPlot& kPlot = *itPlot;
			if (kPlot.isWater() || kPlot.isHills() || kPlot.getBonusType() != NO_BONUS)
				continue;

			bool bChanged = false;
			if (kPlot.calculateNatureYield(YIELD_FOOD, kPlayer.getTeam()) <
				GC.getFOOD_CONSUMPTION_PER_POPULATION())
			{
				FOR_EACH_ENUM(Terrain)
				{
					CvTerrainInfo const& kLoopTerrain = GC.getInfo(eLoopTerrain);
					if (!kLoopTerrain.isWater() && kLoopTerrain.getYield(YIELD_FOOD) >=
						GC.getFOOD_CONSUMPTION_PER_POPULATION())
					{
						kPlot.setTerrainType(eLoopTerrain);
						bChanged = true;
						break;
					}
				}
			}
			if (kPlot.calculateNatureYield(YIELD_PRODUCTION, kPlayer.getTeam()) == 0)
			{
				FOR_EACH_ENUM(Feature)
				{
					CvFeatureInfo const& kLoopFeature = GC.getInfo(eLoopFeature);
					if (kLoopFeature.getYieldChange(YIELD_FOOD) >= 0 &&
						kLoopFeature.getYieldChange(YIELD_PRODUCTION) > 0 &&
						kLoopFeature.isTerrain(kPlot.getTerrainType()))
					{
						kPlot.setFeatureType(eLoopFeature);
						bChanged = true;
						break;
					}
				}
			}
			if (bChanged)
				iGoodPlot++;
		}
	}
}


void CvGame::normalizeAddExtras(/* advc.027: */ NormalizationTarget const* pTarget)
{
	bool const bIgnoreLatitude = GC.getPythonCaller()->isBonusIgnoreLatitude();

	/*	advc.108: Moved up so that the code dependent on found value
		already takes the extra hills into account */
	for (PlayerIter<CIV_ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		CvPlayer const& kPlayer = *itPlayer;
		CvPlot* pStartingPlot = kPlayer.getStartingPlot();
		if (pStartingPlot == NULL)
			continue;
		int iHills = 0;
		for (CityPlotIter itPlot(*pStartingPlot); itPlot.hasNext(); ++itPlot)
		{
			if (itPlot->isHills())
				iHills++;
		}
		int iHillsAdded = 0; // advc.108
		// advc (comment): Starting plot not excluded. I guess that's OK.
		for (CityPlotRandIter it(*pStartingPlot, getMapRand(), true);
			iHills < 3 && /* advc.108: */ iHillsAdded < 2 &&
			it.hasNext(); ++it)
		{
			CvPlot& p = *it;
			if (p.isWater() || p.isHills() ||
				!p.sameArea(*pStartingPlot)) // advc.108 (from Perfect World 2)
			{
				continue;
			}
			if (!p.isFeature() ||
				!GC.getInfo(p.getFeatureType()).isRequiresFlatlands())
			{
				if (p.getBonusType() == NO_BONUS ||
					GC.getInfo(p.getBonusType()).isHills())
				{
					if (gMapLogLevel > 0) logBBAI("    Adding hills for player %d.", kPlayer.getID()); // K-Mod
					p.setPlotType(PLOT_HILLS, false, true);
					iHills++;
					// <advc.108>
					if (it.currID() != CITY_HOME_PLOT)
						iHillsAdded++; // </advc.108>
				}
			}
		}
	}

	scaled rTargetValue;
	if (pTarget == NULL) // advc.027
	{
		int iTotalValue = 0;
		int iBestValue = 0;
		int iWorstValue = MAX_INT;
		for (PlayerAIIter<CIV_ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
		{
			CvPlayerAI const& kPlayer = *itPlayer;
			CvPlot const* pStartingPlot = kPlayer.getStartingPlot();
			if (pStartingPlot == NULL)
				continue;
			int iValue = kPlayer.AI_foundValue(pStartingPlot->getX(), pStartingPlot->getY(),
					-1, /* advc.031e: */ false, true);
			iTotalValue += iValue;
			iBestValue = std::max(iValue, iBestValue);
			iWorstValue = std::min(iValue, iWorstValue);
		}
		//iTargetValue = (iTotalValue + iBestValue) / (itPlayer.nextIndex() + 1);
		rTargetValue = fixp(0.8) * iBestValue;
		// <advc.108>
		if (m_eNormalizationLevel <= NORMALIZE_LOW)
			rTargetValue = fixp(0.75) * iBestValue; // </advc.108>
		if (gMapLogLevel > 0) logBBAI("Adding extras to normalize starting positions. (target value: %d)", rTargetValue.round()); // K-Mod
	}

	for (PlayerAIIter<CIV_ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		CvPlayerAI const& kPlayer = *itPlayer;
		CvPlot* pStartingPlot = kPlayer.getStartingPlot();
		if (pStartingPlot == NULL)
			continue;

		gDLL->callUpdater(); // allow window to update during launch
		CitySiteEvaluator citySiteEval(kPlayer, -1, false, true);
		// <advc.031c>
		if (gFoundLogLevel > 0 && pTarget == NULL)
			citySiteEval.log(*pStartingPlot);
		// </advc.031c>
		// <advc.108> Treat desert features and forest separately
		int iFoodFeatures = 0;
		int iProductionFeatures = 0;
		for (CityPlotIter itPlot(*pStartingPlot, false); itPlot.hasNext(); ++itPlot)
		{
			if (itPlot->isFeature())
			{
				CvFeatureInfo const& kFeature = GC.getInfo(itPlot->getFeatureType());
				if (kFeature.getYieldChange(YIELD_FOOD) > 0)
					iFoodFeatures++;
				if (kFeature.getYieldChange(YIELD_PRODUCTION) > 0)
					iProductionFeatures++;
			}
		}
		bool bProductionFeatureDone = false;
		bool bFoodFeatureDone = false; // </advc.108>
		{
			for (CityPlotRandIter itPlot(*pStartingPlot, getMapRand(), false);
				itPlot.hasNext(); ++itPlot)
			{
				CvPlot& kLoopPlot = *itPlot;
				if (kLoopPlot.getBonusType() != NO_BONUS || kLoopPlot.isFeature())
					continue;
				/*if (SyncRandNum(iCount + 2) > 1)
					continue;*/ // advc.108: Replaced below
				/*	advc.129: Randomize - for mod-mods (for forest, oasis, flood plains
					the order doesn't matter b/c they have mutually exclusive prereqs) */
				FOR_EACH_ENUM_RAND(Feature, getMapRand())
				{
					if (!kLoopPlot.canHaveFeature(eLoopFeature))
						continue;
					// <advc.108> (Partly duplicated in the second extra feature loop)
					CvFeatureInfo const& kFeature = GC.getInfo(eLoopFeature);
					bool bFood = (kFeature.getYieldChange(YIELD_FOOD) > 0);
					bool bProduction = (kFeature.getYieldChange(YIELD_PRODUCTION) > 0);
					if ((!bFood && !bProduction) ||
						(bFood && (iFoodFeatures >= 4 || bFoodFeatureDone)) ||
						bProduction && (iProductionFeatures >= 6 || bProductionFeatureDone))
					{
						continue;
					} // </advc.108>
					// advc.opt: Moved down (do all other checks first)
					if (pTarget != NULL ? pTarget->isReached(*pStartingPlot) : // advc.027
						citySiteEval.evaluate(*pStartingPlot) >= rTargetValue)
					{
						if (gMapLogLevel > 0) logBBAI("    Player %d doesn't need any more features.", kPlayer.getID()); // K-Mod
						goto next_player; // advc
					}
					if (gMapLogLevel > 0) logBBAI("    Adding %S for player %d.", GC.getInfo(eLoopFeature).getDescription(), kPlayer.getID()); // K-Mod
					kLoopPlot.setFeatureType(eLoopFeature);
					// <advc.108>
					if (bFood)
					{
						iFoodFeatures++;
						// Add at most 1 food feature at first
						bFoodFeatureDone = true;
					}
					else
					{
						iProductionFeatures++;
						// Replacing a BtS clause higher up
						if (!SyncRandOneChanceIn(std::max(iProductionFeatures - 2, 1)))
							bProductionFeatureDone = true;
					}
					break;
				}
			}
			// For 2nd extra feature loop
			bProductionFeatureDone = false;
			bFoodFeatureDone = false; // </advc.108>
		}

		int iCoastBonus = 0;
		int iOceanBonus = 0;
		int iLandBonus = 0;
		int iLandFood = 0; // advc.108
		int iWater = 0;
		for (CityPlotIter itPlot(*pStartingPlot, false); itPlot.hasNext(); ++itPlot)
		{
			CvPlot const& p = *itPlot;
			BonusTypes eLoopBonus = p.getBonusType(
					// <advc.108> Don't count unrevealed bonuses
					m_eNormalizationLevel > NORMALIZE_LOW ? NO_TEAM :
					kPlayer.getTeam()); /* </advc.108> */
			if (p.isWater())
			{
				iWater++;
				if (eLoopBonus != NO_BONUS)
				{
					if (p.isAdjacentToLand())
						iCoastBonus++;
					else iOceanBonus++;
				}
			}
			else if (eLoopBonus != NO_BONUS)
			{
				iLandBonus++;
				// <advc.108>
				if (GC.getInfo(eLoopBonus).getYieldChange(YIELD_FOOD) > 0)
					iLandFood++; // </advc.108>
			}
		}
		// <advc.108>
		for (int iOuterPass = 0; iOuterPass < 2; iOuterPass++)
		{
			bool const bInnerRingBias = (iOuterPass == 0); // </advc.108>
			bool const bLandBias = (iWater > NUM_CITY_PLOTS / 2);
			for (CityPlotRandIter itPlot(*pStartingPlot, getMapRand(), false);
				itPlot.hasNext() &&
				//iLandBonus * 3 +
				// <advc.108>
				iLandFood * 4 + (iLandBonus - iLandFood) * 3 +
				// aiCoastBonus multiplier was 2
				iOceanBonus * 2 + iCoastBonus * 3 < 12; ++itPlot)
			{
				if (bInnerRingBias && itPlot.currID() >= NUM_INNER_PLOTS &&
					MapRandSuccess(fixp(0.47)))
				{
					continue;
				} // </advc.108>
				CvPlot& p = *itPlot;
				//if (SyncRandNum(bLandBias && p.isWater() ? 2 : 1) == 0) { // BtS
				// advc.027b: (note that SyncRandNum(1) is always 0)
				if (bLandBias && p.isWater() && MapRandOneChanceIn(2))
					continue;
				if (pTarget != NULL ? pTarget->isNearlyReached(*pStartingPlot) : // advc.027
					citySiteEval.evaluate(*pStartingPlot) >= rTargetValue)
				{
					if (gMapLogLevel > 0) logBBAI("    Player %d doesn't need any more bonuses.", kPlayer.getID()); // K-Mod
					goto done_placing_resources;
				}
				bool const bCoast = (p.isWater() && p.isAdjacentToLand());
				bool const bOcean = (p.isWater() && !bCoast);
				if (!(bCoast && iCoastBonus >= 2) && // advc.108: was >2
					!(bOcean && iOceanBonus >= 2) &&// advc.108: was >2
					// advc.108: At most 3 sea food
					!((bOcean || bCoast) && iOceanBonus + iCoastBonus >= 3))
				{
					for (int iPass = 0; iPass < 2; iPass++)
					{
						if (p.getBonusType() != NO_BONUS)
							continue;
						int iFoodBonuses = iLandFood + iCoastBonus + iOceanBonus; // advc.108
						// advc: Selection and placement moved into auxiliary function
						if (placeExtraBonus(kPlayer.getID(), p,
							iPass == 0, bIgnoreLatitude, false,
							iFoodBonuses > 2 - iPass)) // advc.108
						{
							if (p.isWater())
							{
								if (bCoast)
									iCoastBonus++;
								else if (bOcean)
									iOceanBonus++;
							}
							else
							{
								iLandBonus++;
								// <advc.108>
								if (GC.getInfo(p.getBonusType()).
									getYieldChange(YIELD_FOOD) > 0)
								{
									iLandFood++;
								} // </advc.108>
							}
							break;
						}
						if (!bLandBias || p.isWater() ||
							p.getBonusType() != NO_BONUS)
						{
							continue;
						}
						if (p.isFeature() &&
							//iFeatureCount > 4 &&
							// <advc.108> Don't clear food features
							GC.getInfo(p.getFeatureType()).
							getYieldChange(YIELD_FOOD) <= 0 &&
							(GC.getInfo(p.getFeatureType()).
							getYieldChange(YIELD_PRODUCTION) <= 0 ||
							// Don't clear production features if they're scarce
							iProductionFeatures >= 4) && // </advc.108>
							iCoastBonus + iOceanBonus > 2 && MapRandSuccess(fixp(0.5)))
						{
							// advc: Selection, clearing of feature and placement moved into auxiliary function.
							if (placeExtraBonus(kPlayer.getID(), p, iPass == 0,
								bIgnoreLatitude, true, iFoodBonuses >= 2))
							{
								iLandBonus++;
								// <advc.108>
								if (GC.getInfo(p.getBonusType()).getYieldChange(YIELD_FOOD) > 0)
									iLandFood++; // </advc.108>
							}
						}
					}
				}
			}
		} done_placing_resources:
		for (CityPlotRandIter itPlot(*pStartingPlot, getMapRand(), false);
			itPlot.hasNext(); ++itPlot)
		{
			CvPlot& p = *itPlot;
			if (p.getBonusType() != NO_BONUS || p.isFeature())
				continue;
			// advc.opt: Moved down
			if (pTarget != NULL ? pTarget->isReached(*pStartingPlot) : // advc.027
				citySiteEval.evaluate(*pStartingPlot) >= rTargetValue)
			{
				if (gMapLogLevel > 0) logBBAI("    Player %d doesn't need any more features (2).", kPlayer.getID()); // K-Mod
				break;
			}
			FOR_EACH_ENUM_RAND(Feature, getMapRand()) // advc.129: randomize
			{
				if (!p.canHaveFeature(eLoopFeature))
					continue;
				// <advc.108> (Similar to the first place-feature loop)
				CvFeatureInfo const& kFeature = GC.getInfo(eLoopFeature);
				bool bFood = (kFeature.getYieldChange(YIELD_FOOD) > 0);
				bool bProduction = (kFeature.getYieldChange(YIELD_PRODUCTION) > 0);
				if ((!bFood && !bProduction) ||
					(bFood && (iFoodFeatures >= 4 || bFoodFeatureDone)) ||
					(bProduction && bProductionFeatureDone))
				{
					continue;
				}
				// Too many river forests are unhelpful; they block improvements.
				if (p.isRiver() &&
					GC.getInfo(eLoopFeature).getRiverYieldChange(YIELD_COMMERCE) <
					GC.getInfo(p.getTerrainType()).getRiverYieldChange(YIELD_COMMERCE))
				{
					continue;
				}
				/*	BtS had placed features everywhere (unless found value became
					high enough - unlikely to happen) */
				if (bFood)
				{
					iFoodFeatures++;
					if (!SyncRandOneChanceIn(iFoodFeatures))
						bFoodFeatureDone = true;
				}
				else
				{
					iProductionFeatures++;
					if (!SyncRandOneChanceIn(std::max(iProductionFeatures - 2, 1)))
						bProductionFeatureDone = true;
				} // </advc.108>
				if (gMapLogLevel > 0) logBBAI("    Adding %S for player %d.", GC.getInfo(eLoopFeature).getDescription(), kPlayer.getID()); // K-Mod
				p.setFeatureType(eLoopFeature);
				break;
			}
		}
		next_player: continue; // advc
	}
}


void CvGame::normalizeStartingPlots(NormalizationTarget const* pTarget)
{
	PROFILE_FUNC();

	CvPythonCaller const& py = *GC.getPythonCaller(); // advc.003y

	// advc.108b: Team starts now reassigned already in assignStartingPlots

	if (GC.getInitCore().getWBMapScript())
		return;

	if (!py.callMapFunction("normalizeAddRiver"))
		normalizeAddRiver();

	if (!py.callMapFunction("normalizeRemovePeaks"))
		normalizeRemovePeaks();

	if (!py.callMapFunction("normalizeAddLakes"))
		normalizeAddLakes();

	if (!py.callMapFunction("normalizeRemoveBadFeatures"))
		normalizeRemoveBadFeatures();

	if (!py.callMapFunction("normalizeRemoveBadTerrain"))
		normalizeRemoveBadTerrain();

	if (!py.callMapFunction("normalizeAddFoodBonuses"))
		normalizeAddFoodBonuses(/* advc.027: */ pTarget);

	if (!py.callMapFunction("normalizeAddGoodTerrain"))
		normalizeAddGoodTerrain();

	if (!py.callMapFunction("normalizeAddExtras"))
		normalizeAddExtras(/* advc.027: */ pTarget);
	// <advc> K-Mod logging code moved out of normalizeAddExtras
	if (gMapLogLevel > 0)
	{
		for (PlayerAIIter<CIV_ALIVE> it; it.hasNext(); ++it)
		{
			if (it->getStartingPlot() != NULL)
				logBBAI("    Player %d final value: %d", it->getID(), it->AI_foundValue(it->getStartingPlot()->getX(), it->getStartingPlot()->getY(), -1, false, true));
		}
		logBBAI("normalizeAddExtras() complete");
	} // </advc>
	GC.getLogger().logMapStats(true); // advc.mapstat
}

/*	advc.opt: Body cut from CvPlayer::startingPlotRange. Not player-dependent,
	and there's no need to recompute it for every prospective starting plot.
	const b/c it only updates a mutable cache. */
void CvGame::updateStartingPlotRange() const
{
	CvMap const& kMap = GC.getMap();
	int iRange = kMap.maxStepDistance() + 10;
	iRange *= GC.getDefineINT("STARTING_DISTANCE_PERCENT");
	iRange /= 100;
	int const iAlive = countCivPlayersAlive();
	int const iLand = kMap.getLandPlots();
	iRange *= iLand / (std::max(GC.getInfo(kMap.getWorldSize()).
			getTargetNumCities(), 1) * iAlive);
	iRange /= NUM_CITY_PLOTS;
	// <advc.031> Replacing kMap.getNumAreas(). Tiny islands shouldn't matter.
	int iMajorAreas = 0;
	FOR_EACH_AREA(pArea)
	{
		if (pArea->getNumTiles() * iAlive > iLand)
			iMajorAreas++;
	}
	if (iMajorAreas == 0)
		iMajorAreas = iAlive;
	// </advc.031>
	iRange += std::min((iMajorAreas + 1) / 2, iAlive);
	iRange *= 100 + GC.getPythonCaller()->minStartingDistanceMod();
	iRange /= 100;
	m_iStartingPlotRange = std::max(iRange, GC.getDefineINT("MIN_CIV_STARTING_DISTANCE"));
}

// advc: Cut, refactored from normalizeAddExtras
bool CvGame::placeExtraBonus(PlayerTypes eStartPlayer, CvPlot& kPlot,
		bool bCheckCanPlace, bool bIgnoreLatitude, bool bRemoveFeature,
		bool bNoFood) // advc.108
{
	CvPlot const& kStartPlot = *GET_PLAYER(eStartPlayer).getStartingPlot();
	// <advc.108>
	if (bCheckCanPlace &&
		((!kPlot.sameArea(kStartPlot) && !kPlot.isWater()) || // </advc.108>
		kPlot.isGoody())) // advc.004z
	{
		return false;
	}
	if (bRemoveFeature && kPlot.isFeature())
	{
		if (gMapLogLevel > 0) logBBAI("    Removing %S to place bonus for player %d", GC.getInfo(kPlot.getFeatureType()).getDescription(), eStartPlayer); // K-Mod
		kPlot.setFeatureType(NO_FEATURE);
	}
	// advc.129: Try the resources in a random order
	FOR_EACH_ENUM_RAND(Bonus, getMapRand())
	{
		CvBonusInfo const& kLoopBonus = GC.getInfo(eLoopBonus);
		if (bNoFood && kLoopBonus.getYieldChange(YIELD_FOOD) > 0 || // advc.108
			kPlot.getBonusType() != NO_BONUS)
		{
			continue;
		}
		if (!isNormalizationBonus(eLoopBonus, eStartPlayer, kPlot, bCheckCanPlace, bIgnoreLatitude) ||
			skipDuplicateNormalizationBonus(kStartPlot, kPlot, eLoopBonus, !bCheckCanPlace) || // advc.108
			GC.getMap().isBonusBalanced(eLoopBonus)) // advc.108c
		{
			continue;
		}
		// <advc.004z>
		if (kPlot.isGoody())
			kPlot.setImprovementType(NO_IMPROVEMENT); // </advc.004z>
		if (gMapLogLevel > 0) logBBAI("    Adding %S for player %d", kLoopBonus.getDescription(), eStartPlayer); // K-Mod
		kPlot.setBonusType(eLoopBonus);
		return true;
	}
	return false;
}

/*	advc.108: May probabilistically return false when there is already a resource
	of type eBonus near kStartPlot */
bool CvGame::skipDuplicateNormalizationBonus(CvPlot const& kStartPlot, CvPlot const& kPlot,
	BonusTypes eBonus, bool bSecondPass)
{
	scaled rSkipPr = fixp(1/3.);
	CvBonusInfo const& kBonus = GC.getInfo(eBonus);
	if (kBonus.getGroupRange() <= 0)
		rSkipPr *= 2;
	if (bSecondPass)
		rSkipPr /= 2;
	for (CityPlotIter it(kStartPlot); it.hasNext(); ++it)
	{
		if (it->getBonusType() != eBonus)
			continue;
		// Adjacent duplicates look especially ugly
		int iDist = stepDistance(&*it, &kPlot);
		if (MapRandSuccess(2 * rSkipPr / iDist))
			return true;
	}
	return false;
}

// advc: Cut, pasted, refactored from normalizeAddExtras
bool CvGame::isNormalizationBonus(BonusTypes eBonus, PlayerTypes eStartPlayer,
	CvPlot const& kPlot, bool bCheckCanPlace, bool bIgnoreLatitude) const
{
	CvBonusInfo const& kBonus = GC.getInfo(eBonus);
	if (!kBonus.isNormalize())
		return false;

	if (kBonus.getYieldChange(YIELD_FOOD) < 0 ||
		kBonus.getYieldChange(YIELD_PRODUCTION) < 0)
	{
		return false;
	}
	if (kBonus.getTechCityTrade() != NO_TECH &&
		GC.getInfo(kBonus.getTechCityTrade()).getEra() > getStartEra())
	{
		return false;
	}
	/*	advc: BtS had checked this only for seafood; doesn't really matter though
		b/c all of the isNormalize resources are revealed from the start. */
	if (!GET_TEAM(eStartPlayer).isBonusRevealed(eBonus))
		return false;
	if (kPlot.getBonusType() == eBonus)
	{
		FAssert(!bCheckCanPlace);
		return true;
	}
	return (bCheckCanPlace ? CvMapGenerator::GetInstance().
			canPlaceBonusAt(eBonus, kPlot.getX(), kPlot.getY(), bIgnoreLatitude) :
			kPlot.canHaveBonus(eBonus, bIgnoreLatitude));
}

// <advc.108>
bool CvGame::isPowerfulStartingBonus(CvPlot const& kPlot, PlayerTypes eStartPlayer) const
{
	if (getStartEra() > 0)
		return false;
	BonusTypes eBonus = kPlot.getBonusType(TEAMID(eStartPlayer));
	if (eBonus == NO_BONUS)
		return false;
	return (GC.getInfo(eBonus).getBonusClassType() ==
			GC.getInfoTypeForString("BONUSCLASS_PRECIOUS"));
}

// Tailored for Tundra Deer, dry Jungle Rice
bool CvGame::isWeakStartingFoodBonus(CvPlot const& kPlot, PlayerTypes eStartPlayer) const
{
	BonusTypes eBonus = kPlot.getBonusType(TEAMID(eStartPlayer));
	if (eBonus == NO_BONUS ||
		// To filter out resources that normalizeAddFood doesn't care about
		!isNormalizationBonus(eBonus, eStartPlayer, kPlot, false, true))
	{
		return false;
	}
	int iBaseFood = GC.getInfo(eBonus).getYieldChange(YIELD_FOOD);
	if (iBaseFood <= 0)
		return false;
	 iBaseFood += GC.getInfo(kPlot.getTerrainType()).getYield(YIELD_FOOD);
	// (Some overlap with AIFoundValue::getBonusImprovement)
	int iBestImprovFood = 0;
	FOR_EACH_ENUM(Build)
	{
		CvBuildInfo const& kBuild = GC.getInfo(eLoopBuild);
		ImprovementTypes eImprov = kBuild.getImprovement();
		if (eImprov == NO_IMPROVEMENT)
			continue;
		CvImprovementInfo const& kImprov = GC.getInfo(eImprov);
		if (eImprov == NO_IMPROVEMENT ||
			!kImprov.isImprovementBonusMakesValid(eBonus) ||
			!kImprov.isImprovementBonusTrade(eBonus))
		{
			continue;
		}
		int iImprovFood = kPlot.calculateImprovementYieldChange(
				eImprov, YIELD_FOOD, eStartPlayer);
		iBestImprovFood = std::max(iBestImprovFood, iImprovFood);
	}
	return (iBaseFood + iBestImprovFood <= 4 &&
			// Not really a food resource if the improvement doesn't add food
			iBestImprovFood > 0);
} // </advc.108>


void CvGame::update()
{
	startProfilingDLL(false);
	PROFILE_BEGIN("CvGame::update");
	// <advc.256> Based on C2C, originally mostly from Rise of Mankind, I think.
	CvPlayer const& kActivePlayer = GET_PLAYER(getActivePlayer());
	int iSuccessiveUpdates = 1;
	if (getTurnSlice() > 0) // Wait for BUG initialization
	{
		// Needs to match the value range set in XML
		int const iDefaultGraphicsUpdateRate = 12;
		int iGraphicsUpdateRate = BUGOption::getValue("MainInterface__GraphicsUpdateRate",
				iDefaultGraphicsUpdateRate);
		if (iGraphicsUpdateRate <= 0)
			iSuccessiveUpdates = 128; // Not quite infinite, but a lot in a row.
		else iSuccessiveUpdates = iDefaultGraphicsUpdateRate / iGraphicsUpdateRate;
	}
	if (isGameMultiPlayer() || !kActivePlayer.isAlive())
		iSuccessiveUpdates = 1;
	if (kActivePlayer.isTurnActive() &&
		(!kActivePlayer.isAutoMoves() ||
		!kActivePlayer.isOption(PLAYEROPTION_QUICK_MOVES)))
	{
		iSuccessiveUpdates = 1;
	}
	if (gDLL->GetWorldBuilderMode() && !isInAdvancedStart()) // As in BtS
		iSuccessiveUpdates = 0;
	for (int i = 0; i < iSuccessiveUpdates; i++)
		updateUnprofiled(); // </advc.256>
	PROFILE_END();
	stopProfilingDLL(false);
}

// advc.256: Cut from update
void CvGame::updateUnprofiled()
{
	sendPlayerOptions();

	// sample generic event
	CyArgsList pyArgs;
	pyArgs.add(getTurnSlice());
	/*	advc.210: To prevent BUG alerts from being checked at the start of a
		game turn. I've tried doing that through BugEventManager.py, but soon
		gave up. Tagging advc.706 b/c it's especially important to supress
		the update when R&F is enabled. */
	if (!isInBetweenTurns())
	{
		CvEventReporter::getInstance().genericEvent("gameUpdate", pyArgs.makeFunctionArgs());
		// <advc.003r>
		for (int i = 0; i < NUM_UPDATE_TIMER_TYPES; i++)
			handleUpdateTimer((UpdateTimerTypes)i); // </advc.003r>
	}
	if (getTurnSlice() == 0) // advc (note): Implies 0 elapsed game turns
	{	// <advc.700> Delay initial auto-save until RiseFall is initialized
		if (!isOption(GAMEOPTION_RISE_FALL) && // </advc.700>
			m_iTurnLoadedFromSave != m_iElapsedGameTurns && // advc.044
			// advc: Necessary now that re-gen resets turn slice
			m_iMapRegens <= 0)
		{
            // doc (edead): disable autosave during autoplay
            // TODO: refactor
		    if (GC.getDefineINT("NO_AUTOSAVE_DURING_AUTOPLAY") == 0 || (getGameTurn() > 0 && getAIAutoPlay() == 0))
                autoSave(true); // advc.106l
		}
	}
	/*	<advc.004m> Slice 0 seems to be the earliest time when plot indicators
		can be enabled w/o crashing. But it appears that, for some players,
		the indicators do not actually appear then - race condition? Slice 1
		doesn't seem to help either. 4 was maybe an improvement. Try 7?
		(It's a continuous count.) At some point, the delay gets noticeable. */
	if (getTurnSlice() == 7 &&
		// Leave it up to the savegame when loading an initial autosave
		m_iTurnLoadedFromSave != m_iElapsedGameTurns)
	{
		if (BUGOption::isEnabled("MainInterface__StartWithResourceIcons", true))
			gDLL->getEngineIFace()->setResourceLayer(true);
	} // </advc.004m>
	if (getNumGameTurnActive() == 0)
	{
		if (!isPbem() || !getPbemTurnSent())
			doTurn();
	}
	updateScore();
	updateWar();
	updateMoves();
	updateTimers();
	updateTurnTimer();
	AI().AI_updateAssignWork();
	testAlive();
	if (getAIAutoPlay() == 0 && !gDLL->GetAutorun() &&
		getGameState() != GAMESTATE_EXTENDED)
	{
		if (countHumanPlayersAlive() == 0 &&
			!isOption(GAMEOPTION_RISE_FALL)) // advc.707
		{
			setGameState(GAMESTATE_OVER);
		}
	}
	changeTurnSlice(1);
	/*	<advc.104l> Make sure that UI (specifically willing-to-talk indicator)
		doesn't become outdated throughout a turn. Or at least not for long.
		advc.085: Invalidating on every turn slice might slightly hurt
		responsiveness when hovering over the scoreboard. (Not sure.) */
	if (getTurnSlice() % 4 == 0)
		AI().uwai().invalidateUICache(); // </advc.104l>
	/*	<advc.004n> (Disassembly suggests that the EXE caches this info,
		so this check is fast.) */
	bool bCityScreenUp = gDLL->UI().isCityScreenUp();
	if (bCityScreenUp != m_bCityScreenUp)
	{
		m_bCityScreenUp = bCityScreenUp;
		onCityScreenChange();
	} // </advc004n>
	if (getActivePlayer() != NO_PLAYER && GET_PLAYER(getActivePlayer()).getAdvancedStartPoints() >= 0 &&
		!gDLL->UI().isInAdvancedStart())
	{
		gDLL->UI().setInAdvancedStart(true);
		gDLL->UI().setWorldBuilder(true);
	} // <advc.705>
	if (isOption(GAMEOPTION_RISE_FALL))
		m_pRiseFall->restoreDiploText(); // </advc.705>
}

struct techRankCompare
{
	bool operator() (TeamTypes eTeam1, TeamTypes eTeam2)
	{
		return GET_TEAM(eTeam1).getTotalTechValue() > GET_TEAM(eTeam2).getTotalTechValue();
	}
};

void CvGame::updateTechRanks()
{
	std::vector<TeamTypes> techRankedTeams;
	for (int iI = 0; iI < MAX_TEAMS; iI++)
	{
		techRankedTeams.push_back((TeamTypes)iI);
	}

	techRankCompare cmp;
	std::sort(techRankedTeams.begin(), techRankedTeams.end(), cmp);

	int iIndex = 0;
	for (std::vector<TeamTypes>::iterator it = techRankedTeams.begin(); it != techRankedTeams.end(); ++it)
	{
		setTechRank(iIndex++, *it);

		if (iIndex == countCivTeamsAlive() / 3)
		{
			setMedianTechValue(GET_TEAM(*it).getTotalTechValue());
		}
	}
}

void CvGame::setTechRank(int iRank, TeamTypes eTeam)
{
	m_aiTechRankTeam[eTeam] = iRank;
}

int CvGame::getTechRank(TeamTypes eTeam) const
{
	return m_aiTechRankTeam[(int)eTeam];
}

void CvGame::setMedianTechValue(int iValue)
{
	m_iMedianTechValue = iValue;
}

int CvGame::getMedianTechValue() const
{
	return m_iMedianTechValue;
}


void CvGame::updateScore(bool bForce)
{
	PROFILE_FUNC(); // advc.test (Just a little worried about the attitude updates)
	if (!isScoreDirty() && !bForce)
		return;
	setScoreDirty(false);

	EagerEnumMap<PlayerTypes,bool> abPlayerScored;
	FOR_EACH_ENUM(CivPlayer)
	{
		PlayerTypes eRank = (PlayerTypes)eLoopCivPlayer;
		PlayerTypes eBestPlayer = NO_PLAYER;
		int iBestScore = MIN_INT;
		FOR_EACH_ENUM2(CivPlayer, ePlayer)
		{
			CvPlayer const& kPlayer = GET_PLAYER((PlayerTypes)ePlayer);
			if (abPlayerScored.get(kPlayer.getID()))
				continue;
			int iScore = kPlayer.calculateScore(false);
			if (iScore >= iBestScore)
			{
				iBestScore = iScore;
				eBestPlayer = kPlayer.getID();
			}
		}
		FAssert(iBestScore == 0 || GET_PLAYER(eBestPlayer).isAlive()); // advc
		abPlayerScored.set(eBestPlayer, true);
		setRankPlayer(eRank, eBestPlayer);
		setPlayerRank(eBestPlayer, eRank);
		setPlayerScore(eBestPlayer, iBestScore);
		setCivilizationHistory(HISTORY_SCORE, GET_PLAYER(eBestPlayer).getCivilizationType(), getGameTurn(), iBestScore); // doc
		// <advc.004s>
		if (GET_PLAYER(eBestPlayer).isAlive())
			GET_PLAYER(eBestPlayer).updateHistory(PLAYER_HISTORY_SCORE, getGameTurn());
		// </advc.004s>
	}
	EagerEnumMap<TeamTypes,bool> abTeamScored;
	FOR_EACH_ENUM(CivTeam)
	{
		TeamTypes eRank = (TeamTypes)eLoopCivTeam;
		TeamTypes eBestTeam = NO_TEAM;
		int iBestScore = MIN_INT;
		FOR_EACH_ENUM2(CivTeam, eTeam)
		{
			CvTeam const& kTeam = GET_TEAM((TeamTypes)eTeam);
			if (abTeamScored.get(kTeam.getID()))
				continue;
			int iScore = 0;
			FOR_EACH_ENUM(Player)
			{
				if (GET_PLAYER(eLoopPlayer).getTeam() == kTeam.getID())
					iScore += getPlayerScore(eLoopPlayer);
			}
			if (iScore >= iBestScore)
			{
				iBestScore = iScore;
				eBestTeam = kTeam.getID();
			}
		}
		abTeamScored.set(eBestTeam, true);
		setRankTeam(eRank, eBestTeam);
		setTeamRank(eBestTeam, eRank);
		setTeamScore(eBestTeam, iBestScore);
	}
	// advc.130c, advc.001: Difficult to narrow down which players need an update
	CvPlayerAI::AI_updateAttitudes();
}

// advc.003y: Ported from CvUtil.py
int CvGame::getScoreComponent(int iRawScore, int iInitial, int iMax,
	int iMultiplier, bool bExponential, bool bFinal, bool bVictory) const
{
	if (getEstimateEndTurn() <= 0)
		return 0;

	static scaled const rSCORE_FREE_PERCENT = per100(GC.getDefineINT(
			"SCORE_FREE_PERCENT"));
	static scaled const rSCORE_VICTORY_PERCENT = per100(GC.getDefineINT(
			"SCORE_VICTORY_PERCENT"));
	static scaled const rSCORE_HANDICAP_PERCENT_OFFSET = per100(GC.getDefineINT(
			"SCORE_HANDICAP_PERCENT_OFFSET"));
	static scaled const rSCORE_HANDICAP_PERCENT_PER = per100(GC.getDefineINT(
			"SCORE_HANDICAP_PERCENT_PER"));

	scaled rMax = iMax;
	if (bFinal && bVictory) // Not synchronized; floating point math is fine here.
	{
		scaled rTurnRatio(getGameTurn(), getEstimateEndTurn());
		if (bExponential && iInitial > 0)
			rMax = iInitial * (rMax / iInitial).pow(rTurnRatio);
		else rMax = iInitial + rTurnRatio * (rMax - iInitial);
	}
	scaled rFreeScore = rSCORE_FREE_PERCENT * rMax;
	scaled rScore = iMultiplier;
	scaled rDiv = rFreeScore + rMax;
	if (rDiv >= 1)
		rScore = (iRawScore + rFreeScore) * (iMultiplier / rDiv);
	if (!bVictory && !bFinal)
		return rScore.round();
	if (bVictory)
		rScore *= 1 + rSCORE_VICTORY_PERCENT;
	if (bFinal)
	{	// <advc.250a>
		rScore *= 1 + rSCORE_HANDICAP_PERCENT_OFFSET +
				scaled(getDifficultyForEndScore(), 10) * rSCORE_HANDICAP_PERCENT_PER;
		// </advc.250a>
	}
	return rScore.round();
}


void CvGame::updatePlotGroups()
{
	PROFILE_FUNC();

	for (PlayerIter<ALIVE> it; it.hasNext(); ++it)
		it->updatePlotGroups();
}


void CvGame::updateBuildingCommerce()
{
	for (PlayerIter<ALIVE> it; it.hasNext(); ++it)
		it->updateBuildingCommerce();
}


void CvGame::updateCitySight(bool bIncrement)
{
	for (PlayerIter<ALIVE> it; it.hasNext(); ++it)
		it->updateCitySight(bIncrement, false);
	updatePlotGroups();
}


void CvGame::updateTradeRoutes()
{
	for (PlayerIter<CIV_ALIVE> it; it.hasNext(); ++it) // advc: exclude Barbarians
		it->updateTradeRoutes();
}

// K-Mod: calculate unhappiness due to the state of global warming
void CvGame::updateGwPercentAnger()
{
	int iGlobalPollution;
	int iGwSeverityRating;
	int iGlobalDefence;

	int iGwIndex = getGlobalWarmingIndex();

	if (iGwIndex > 0)
	{
		iGlobalPollution = calculateGlobalPollution();
		iGwSeverityRating = calculateGwSeverityRating();
		iGlobalDefence = calculateGwLandDefence(NO_PLAYER);
	} // advc: Ensure initialization
	else iGlobalPollution = iGwSeverityRating = iGlobalDefence = -1;
	for (PlayerIter<MAJOR_CIV> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		int iAngerPercent = 0;
		if (iGwIndex > 0)
		{
			// player unhappiness = base rate * severity rating * responsibility factor

			int iLocalDefence = calculateGwLandDefence(itPlayer->getID());
			int iResponsibilityFactor =	100*(itPlayer->calculatePollution() - iLocalDefence);

			iResponsibilityFactor /= std::max(1,
					calculateGwSustainabilityThreshold(itPlayer->getID()));
			iResponsibilityFactor *= calculateGwSustainabilityThreshold();
			iResponsibilityFactor /= std::max(1, iGlobalPollution - iGlobalDefence);
			// amplify the affects of responsibility
			iResponsibilityFactor = std::max(0, 2*iResponsibilityFactor-100);

			static int const iGLOBAL_WARMING_BASE_ANGER_PERCENT = GC.getDefineINT("GLOBAL_WARMING_BASE_ANGER_PERCENT"); // advc.opt
			iAngerPercent = iGLOBAL_WARMING_BASE_ANGER_PERCENT * iGwSeverityRating * iResponsibilityFactor;
			iAngerPercent = intdiv::round(iAngerPercent, 100 * 100);
		}
		itPlayer->setGwPercentAnger(iAngerPercent);
	}
}

/*	advc.106l: Wrapper that reports the event. Everyone should call this
	instead of calling the CvEngine function directly. */
void CvGame::autoSave(bool bInitial)
{
	PROFILE_FUNC();
	/*	<advc.135c> Avoid overlapping auto-saves in test games played on a
		single machine. Don't know how to check this properly. */
	if (isNetworkMultiPlayer() && isDebugToolsAllowed(false) && getActivePlayer() % 2 == 0)
		return; // </advc.135c>
	CvEventReporter::getInstance().preAutoSave();
	gDLL->getEngineIFace()->AutoSave(bInitial);
	// BULL - AutoSave - start
	if (bInitial && BUGOption::isEnabled("AutoSave__CreateStartSave", false))
		GC.getPythonCaller()->call("gameStartSave", PYCivModule);
	// BULL - AutoSave - end
}


void CvGame::testExtendedGame()
{
	if (getGameState() != GAMESTATE_OVER)
		return;
	for (PlayerIter<HUMAN> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		if (itPlayer->isExtendedGame())
		{
			setGameState(GAMESTATE_EXTENDED);
			break;
		}
	}
}


void CvGame::cityPushOrder(CvCity* pCity, OrderTypes eOrder, int iData,
	bool bAlt, bool bShift, bool bCtrl) const
{
	if (pCity->getProduction() > 0)
	{
		CvMessageControl::getInstance().sendPushOrder(pCity->getID(), eOrder, iData, bAlt,
				/*bShift, !bShift*/false, bShift ? -1 : 0); // K-Mod
	}
	else if ((eOrder == ORDER_TRAIN) && (pCity->getProductionUnit() == iData))
	{
		CvMessageControl::getInstance().sendPushOrder(pCity->getID(), eOrder, iData, bAlt,
				/*!bCtrl, bCtrl*/false, bCtrl ? 0 : -1); // K-Mod
	}
	else
	{
		CvMessageControl::getInstance().sendPushOrder(pCity->getID(), eOrder, iData, bAlt,
				/*bShift, bCtrl*/!(bShift || bCtrl), bShift ? -1 : 0); // K-Mod
	}
}


void CvGame::selectUnit(CvUnit* pUnit, bool bClear, bool bToggle, bool bSound) const
{
	PROFILE_FUNC();
	/*if (gDLL->UI().getHeadSelectedUnit() == NULL)
		bSelectGroup = true;
	else if (gDLL->UI().getHeadSelectedUnit()->getGroup() != pUnit->getGroup())
		bSelectGroup = true;
	else if (pUnit->IsSelected() && !(gDLL->UI().mirrorsSelectionGroup()))
		bSelectGroup = !bToggle;
	else bSelectGroup = false;*/ // BtS
	// K-Mod. Redesigned to make selection more sensible and predictable
	// In 'simple mode', shift always groups and always targets only a single unit.
	// advc.001: Option id was SimpleSelectionMode here but SimpleSelection in XML
	bool bSimpleMode = BUGOption::isEnabled("MainInterface__SimpleSelection", true);

	bool bExplicitDeselect = false;
	bool bSelectGroup = false;
	if (gDLL->UI().getHeadSelectedUnit() == NULL)
		bSelectGroup = true;
	else if (bToggle)
	{
		if (pUnit->IsSelected())
		{
			bExplicitDeselect = true;
			bSelectGroup = false;
		}
		else
		{
			bSelectGroup = bSimpleMode ? false : gDLL->UI().mirrorsSelectionGroup();
		}
	}
	else
	{
		bSelectGroup = gDLL->UI().mirrorsSelectionGroup()
			? gDLL->UI().getHeadSelectedUnit()->getGroup() != pUnit->getGroup()
			: pUnit->IsSelected();
	} // K-Mod end

	gDLL->UI().clearSelectedCities();
	bool bGroup = false;
	if (bClear)
	{
		gDLL->UI().clearSelectionList();
		bGroup = false;
	}
	else
	{	//bGroup = gDLL->UI().mirrorsSelectionGroup();
		/*	K-Mod. If there is only one unit selected, and it is to be toggled,
			just degroup it rather than unselecting it. */
		if (bExplicitDeselect && gDLL->UI().getLengthSelectionList() == 1)
		{
			CvMessageControl::getInstance().sendJoinGroup(pUnit->getID(), FFreeList::INVALID_INDEX);
			return; // that's all.
		}
		bGroup = gDLL->UI().mirrorsSelectionGroup();
		/*	Note: bGroup will not clear away unselected units of the group.
			so if we want to do that, we'll have to do it explicitly. */
		if (!bGroup && bSimpleMode && bToggle)
		{	/*	'toggle' should be seen as explicitly adding / removing units from a group.
				so lets explicitly reform the group. */
			selectionListGameNetMessage(GAMEMESSAGE_JOIN_GROUP);
			/*	note: setting bGroup = true doesn't work here either,
				because the internals of insertIntoSelectionList apparently wants to
				go out of its way to make our lives difficult.
				(stuffed if I know what it actually does. Maybe it only sends the
				group signal if the units aren't already grouped or something.
				in any case, we have to do it explicitly or it won't work.) */
			CvUnit* pSelectionHead = gDLL->UI().getHeadSelectedUnit();
			if (pSelectionHead)
				CvMessageControl::getInstance().sendJoinGroup(pUnit->getID(), pSelectionHead->getID());
		} // K-Mod end
	}
	if (bSelectGroup)
	{
		gDLL->UI().selectionListPreChange();
		FOR_EACH_UNIT_VAR_IN(pUnit, *pUnit->getGroup())
		{
			FAssertMsg(pUnit != NULL, "null entity in selection group");
			gDLL->UI().insertIntoSelectionList(
					pUnit, false, bToggle, bGroup, bSound, true);
		}
		gDLL->UI().selectionListPostChange();
	}
	else
	{
		gDLL->UI().insertIntoSelectionList(pUnit, false, bToggle, bGroup, bSound);
		/*	K-Mod. Unfortunately, removing units from the group is not correctly handled
			by the interface functions. so we need to do it explicitly. */
		if (bExplicitDeselect && bGroup)
			CvMessageControl::getInstance().sendJoinGroup(pUnit->getID(), FFreeList::INVALID_INDEX);
		// K-Mod end
	}
	gDLL->UI().makeSelectionListDirty();
}

/*	K-Mod. I've made an ugly hack to change the functionality of double-click
	from select-all to wake-all. Here's how it works:
	If this function is called with only bAlt==true, but without the Alt key actually down,
	then wake-all is triggered rather than select-all.
	To achieve the select-all functionality without the Alt key,
	call the function with bCtrl && bAlt. */
void CvGame::selectGroup(CvUnit* pUnit, bool bShift, bool bCtrl, bool bAlt) const
{
	PROFILE_FUNC();

	FAssertMsg(pUnit != NULL, "pUnit == NULL unexpectedly");
	// <advc.002e> Show glow (only) on selected unit
	if (!BUGOption::isEnabled("PLE__ShowPromotionGlow", false))
	{
		CvPlayer const& kOwner = GET_PLAYER(pUnit->getOwner());
		FOR_EACH_UNIT_VAR(u, kOwner)
		{
			gDLL->getEntityIFace()->showPromotionGlow(u->getEntity(),
					u->atPlot(pUnit->plot()) && u->isPromotionReady());
		}
	} // </advc.002e>
	// K-Mod. the hack (see above)
	if (bAlt && !bShift && !bCtrl && !GC.altKey() &&
		!gDLL->altKey()) // (using gDLL->altKey, to better match the state of bAlt)
	{
		/*	The caller says alt is pressed, but the computer says otherwise.
			Lets assume this is a double-click. */
		CvPlot const& kUnitPlot = pUnit->getPlot();
		FOR_EACH_UNIT_VAR_IN(pLoopUnit, kUnitPlot)
		{
			if (pLoopUnit->getOwner() == getActivePlayer() &&
				pLoopUnit->isGroupHead() && pLoopUnit->isWaiting())
			{
				CvMessageControl::getInstance().sendDoCommand(
						pLoopUnit->getID(), COMMAND_WAKE, -1, -1, false);
			}
		}
		gDLL->UI().selectUnit(pUnit, true, false, true);
		return;
	} // K-Mod end

	if (bAlt || bCtrl)
	{
		gDLL->UI().clearSelectedCities();
		DomainTypes const eDomain = pUnit->getDomainType(); // K-Mod
		bool const bCheckMoves = pUnit->canMove() || pUnit->IsSelected(); // K-Mod.
		/*	(Note: The IsSelected check is to stop selected units with no moves
			from making it hard to select moveable units by clicking on the map.) */

		bool bGroup;
		if (!bShift)
		{
			gDLL->UI().clearSelectionList();
			bGroup = true;
		}
		else
		{
			//bGroup = gDLL->UI().mirrorsSelectionGroup();
			// K-Mod. Treat shift as meaning we should always form a group
			if (!gDLL->UI().mirrorsSelectionGroup())
				selectionListGameNetMessage(GAMEMESSAGE_JOIN_GROUP);
			/*	note: sometimes this won't work. (see comments in CvGame::selectUnit.)
				Unfortunately, it's too fiddly to fix. */
			bGroup = true;
			// K-Mod end
		}
		gDLL->getInterfaceIFace()->selectionListPreChange();
		CvPlot const& kUnitPlot = pUnit->getPlot();
		FOR_EACH_UNIT_VAR_IN(pLoopUnit, kUnitPlot)
		{
			if (pLoopUnit->getOwner() != getActivePlayer())
				continue;
			// K-Mod: added domain check and bCheckMoves
			if (pLoopUnit->getDomainType() == eDomain &&
				(!bCheckMoves || pLoopUnit->canMove()))
			{
				// disabled by K-Mod:
				//if (!isMPOption(MPOPTION_SIMULTANEOUS_TURNS) || getTurnSlice() - pLoopUnit->getLastMoveTurn() > GC.getDefineINT("MIN_TIMER_UNIT_DOUBLE_MOVES"))
				if (bAlt || pLoopUnit->getUnitType() == pUnit->getUnitType())
				{
					gDLL->getInterfaceIFace()->insertIntoSelectionList(
							pLoopUnit, false, false, bGroup, false, true);
				}
			}
		}
		gDLL->getInterfaceIFace()->selectionListPostChange();
	}
	else gDLL->getInterfaceIFace()->selectUnit(pUnit, !bShift, bShift, true);
}


void CvGame::selectAll(CvPlot* pPlot) const
{
	CvUnit* pSelectUnit = NULL;
	if (pPlot != NULL)
	{
		CvUnit* pCenterUnit = pPlot->getDebugCenterUnit();
		if (pCenterUnit != NULL && pCenterUnit->getOwner() == getActivePlayer())
			pSelectUnit = pCenterUnit;
	}
	if (pSelectUnit != NULL)
	{
		gDLL->getInterfaceIFace()->selectGroup(pSelectUnit,
				//false, false, true);
				false, true, true); // K-Mod
	}
}


bool CvGame::selectionListIgnoreBuildingDefense() const
{
	//PROFILE_FUNC(); // advc.003o
	bool bIgnoreBuilding = false;
	bool bAttackLandUnit = false;
	for (CLLNode<IDInfo> const* pNode = gDLL->UI().headSelectionListNode();
		pNode != NULL; pNode = gDLL->UI().nextSelectionListNode(pNode))
	{
		CvUnit* pSelectedUnit = ::getUnit(pNode->m_data);
		if (pSelectedUnit == NULL)
			continue;
		if (pSelectedUnit->ignoreBuildingDefense())
			bIgnoreBuilding = true;
		if (pSelectedUnit->getDomainType() == DOMAIN_LAND &&
			pSelectedUnit->canAttack())
		{
			bAttackLandUnit = true;
		}
	}
	if (!bIgnoreBuilding && !bAttackLandUnit && getBestLandUnit() != NO_UNIT)
		bIgnoreBuilding = GC.getInfo(getBestLandUnit()).isIgnoreBuildingDefense();
	return bIgnoreBuilding;
}


void CvGame::implementDeal(PlayerTypes eWho, PlayerTypes eOtherWho,
	CLinkList<TradeData>* pOurList, CLinkList<TradeData>* pTheirList,
	bool bForce)
{
	// <advc> Not sure if the EXE ever calls implementDeal with a NULL list
	CLinkList<TradeData> emptyList;
	implementDeal(eWho, eOtherWho,
			pOurList == NULL ? emptyList : *pOurList,
			pTheirList == NULL ? emptyList : *pTheirList,
			bForce);
}


void CvGame::implementDeal(PlayerTypes eWho, PlayerTypes eOtherWho,
	CLinkList<TradeData>& kOurList, CLinkList<TradeData>& kTheirList,
	bool bForce)
{
	// </advc>  <advc.036>
	implementAndReturnDeal(eWho, eOtherWho, kOurList, kTheirList, bForce);
}


CvDeal* CvGame::implementAndReturnDeal(PlayerTypes eWho, PlayerTypes eOtherWho,
	CLinkList<TradeData>& kOurList, CLinkList<TradeData>& kTheirList,
	bool bForce) // </advc.036>
{
	FAssert(eWho != NO_PLAYER);
	FAssert(eOtherWho != NO_PLAYER);
	FAssert(eWho != eOtherWho);

	CvDeal* pDeal = addDeal();
	pDeal->init(pDeal->getID(), eWho, eOtherWho);
	pDeal->addTradeItems(kOurList, kTheirList, !bForce);
	if (pDeal->getLengthFirst() <= 0 && pDeal->getLengthSecond() <= 0)
	{
		pDeal->kill();
		return NULL; // advc.036
	}
	return pDeal; // advc.036
}


void CvGame::verifyDeals()
{
	FOR_EACH_DEAL_VAR(pLoopDeal)
		pLoopDeal->verify();
}

/*	Globeview configuration control:
	If bStarsVisible, then there will be stars visible behind the globe when it is on.
	If bWorldIsRound, then the world will bend into a globe;
	otherwise, it will show up as a plane. */
void CvGame::getGlobeviewConfigurationParameters(TeamTypes eTeam,
	bool& bStarsVisible, bool& bWorldIsRound)
{
	if (GET_TEAM(eTeam).isMapCentering() || isCircumnavigated())
	{
		bStarsVisible = true;
		bWorldIsRound = true;
	}
	else
	{
		bStarsVisible = false;
		bWorldIsRound = false;
	}
}


int CvGame::getAdjustedPopulationPercent(VictoryTypes eVictory) const
{
	if (GC.getInfo(eVictory).getPopulationPercentLead() <= 0)
		return 0;
	if (getTotalPopulation() <= 0)
		return 100;

	int iBestPopulation = 0;
	int iNextBestPopulation = 0;
	for (TeamIter<CIV_ALIVE> itTeam; itTeam.hasNext(); ++itTeam)
	{
		int iPopulation = itTeam->getTotalPopulation();
		if (iPopulation > iBestPopulation)
		{
			iNextBestPopulation = iBestPopulation;
			iBestPopulation = iPopulation;
		}
		else if (iPopulation > iNextBestPopulation)
			iNextBestPopulation = iPopulation;
	}
	return std::min(100, (iNextBestPopulation * 100) / getTotalPopulation() +
			GC.getInfo(eVictory).getPopulationPercentLead());
}


int CvGame::getProductionPerPopulation(HurryTypes eHurry) const
{
	if (eHurry == NO_HURRY)
		return 0;
	return (GC.getInfo(eHurry).getProductionPerPopulation() * 100) /
			std::max(1, GC.getInfo(getGameSpeedType()).getHurryPercent());
}

// advc: Cut from CvCity::flatHurryAngerLength
int CvGame::getHurryAngerLength() const
{
	int iAnger = GC.getDefineINT(CvGlobals::HURRY_ANGER_DIVISOR);
	iAnger *= GC.getInfo(GC.getGame().getGameSpeedType()).getHurryConscriptAngerPercent();
	iAnger /= 100;
	return iAnger;
}


int CvGame::getAdjustedLandPercent(VictoryTypes eVictory) const
{
	if (GC.getInfo(eVictory).getLandPercent() <= 0)
		return 0;
	// <advc.254>
	int const iTotalLand = GC.getMap().getLandPlots();
	if (iTotalLand <= 0)
		return 0; // </advc.254>
	int iPercent = GC.getInfo(eVictory).getLandPercent();
	//iPercent -= getCivTeamsEverAlive() * 2;
    iPercent -= countCivTeamsAlive() * 2; // rfc
	iPercent = std::max(iPercent, GC.getInfo(eVictory).getMinLandPercent());
	// <advc.254> (Based on getAdjustedPopulationPercent)
	int iBestLand = 0;
	int iNextBestLand = 0;
	for (TeamIter<CIV_ALIVE> itTeam; itTeam.hasNext(); ++itTeam)
	{
		int iLand = itTeam->getTotalLand();
		if (iLand > iBestLand)
		{
			iNextBestLand = iBestLand;
			iBestLand = iLand;
		}
		else if (iLand > iNextBestLand)
			iNextBestLand = iLand;
	}
	iPercent = std::max(iPercent,
			std::min(100, (iNextBestLand * 100) / iTotalLand +
			GC.getInfo(eVictory).get(CvVictoryInfo::LandPercentLead)));
	// </advc.254>
	return iPercent;
}

// advc.178: Cut from CvPlayerAI::AI_calculateDiplomacyVictoryStage
bool CvGame::isDiploVictoryValid() const
{
	FOR_EACH_ENUM(Victory)
	{
		if (isVictoryValid(eLoopVictory) && GC.getInfo(eLoopVictory).isDiploVote())
			return true;
	}
	return false;
}

// advc.115f:
VictoryTypes CvGame::getDominationVictory() const
{
	FOR_EACH_ENUM(Victory)
	{
		if (GC.getInfo(eLoopVictory).getLandPercent() > 0 &&
			GC.getInfo(eLoopVictory).getPopulationPercentLead() > 0)
		{
			return eLoopVictory;
		}
	}
	return NO_VICTORY;
}

// advc: Moved from CvGameInterface.cpp
VictoryTypes CvGame::getSpaceVictory() const
{
	FOR_EACH_ENUM(Project)
	{
		if (GC.getInfo(eLoopProject).isSpaceship())
			return GC.getInfo(eLoopProject).getVictoryPrereq();
	}
	// (Could be fine in mods)
	//FErrorMsg("Invalid space victory type");
	return NO_VICTORY;
	/*	advc: Alternative check, cut from AI_calculateSpaceVictoryStage (BBAI),
		disused. */
	/*FOR_EACH_ENUM(Victory) {
		if (GC.getInfo(eLoopVictory).getVictoryDelayTurns() > 0)
			return eLoopVictory;
	}
	return NO_VICTORY;*/
}


bool CvGame::isTeamVote(VoteTypes eVote) const
{
	return (GC.getInfo(eVote).isSecretaryGeneral() || GC.getInfo(eVote).isVictory());
}


bool CvGame::isChooseElection(VoteTypes eVote) const
{
	return !GC.getInfo(eVote).isSecretaryGeneral();
}


bool CvGame::isTeamVoteEligible(TeamTypes eTeam, VoteSourceTypes eVoteSource) const
{
	CvTeam const& kTeam = GET_TEAM(eTeam);
    // doc: not for minors
    if (kTeam.isMinorCiv())
        return false;
	if (kTeam.isForceTeamVoteEligible(eVoteSource))
		return true;
	if (!kTeam.isFullMember(eVoteSource))
		return false;

	int iCount = 0;
	for (TeamIter<CIV_ALIVE> it; it.hasNext(); ++it)
	{
		if (it->isForceTeamVoteEligible(eVoteSource))
			iCount++;
	}
	int iExtraEligible = GC.getDefineINT("TEAM_VOTE_MIN_CANDIDATES") - iCount;
	if (iExtraEligible <= 0)
		return false;
	for (TeamIter<CIV_ALIVE,NOT_SAME_TEAM_AS> it(eTeam); it.hasNext(); ++it)
	{
		CvTeam const& kLoopTeam = *it;
		if (!kLoopTeam.isForceTeamVoteEligible(eVoteSource) &&
			kLoopTeam.isFullMember(eVoteSource))
		{
			int iLoopVotes = kLoopTeam.getVotes(NO_VOTE, eVoteSource);
			int iVotes = kTeam.getVotes(NO_VOTE, eVoteSource);
			// <advc.014>
			if (!kTeam.isCapitulated() || !kLoopTeam.isCapitulated())
			{
				if (kTeam.isCapitulated())
					iVotes = 0;
				if (kLoopTeam.isCapitulated())
					iLoopVotes = 0;
			} // </advc.014>
			if (iLoopVotes > iVotes ||
				(iLoopVotes == iVotes && kLoopTeam.getID() < eTeam))
			{
				iExtraEligible--;
			}
		}
	}
	return (iExtraEligible > 0);
}


int CvGame::countVote(VoteTriggeredData const& kData, PlayerVoteTypes eChoice) const
{
	int iCount = 0;
	for (PlayerIter<CIV_ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
        // doc
        // TODO: include in iterator
        if (itPlayer->isMinorCiv())
            continue;

		if (getPlayerVote(itPlayer->getID(), kData.getID()) == eChoice)
			iCount += itPlayer->getVotes(kData.kVoteOption.eVote, kData.eVoteSource);
	}
	return iCount;
}


int CvGame::countPossibleVote(VoteTypes eVote, VoteSourceTypes eVoteSource) const
{
	int iCount = 0;
    // doc: exclude minors
	for (PlayerIter<CIV_ALIVE,MAJOR_CIV> it; it.hasNext(); ++it)
		iCount += it->getVotes(eVote, eVoteSource);
	return iCount;
}



TeamTypes CvGame::findHighestVoteTeam(const VoteTriggeredData& kData) const
{
	if (!isTeamVote(kData.kVoteOption.eVote))
		return NO_TEAM;
	TeamTypes eBestTeam = NO_TEAM;
	int iBestCount = 0;
	for (TeamIter<CIV_ALIVE> itTeam; itTeam.hasNext(); ++itTeam)
	{
        // doc
        // TODO: filter
        if (itTeam->isMinorCiv())
            continue;

		int iCount = countVote(kData, (PlayerVoteTypes)itTeam->getID());
		if (iCount > iBestCount)
		{
			iBestCount = iCount;
			eBestTeam = itTeam->getID();
		}
	}
	return eBestTeam;
}


int CvGame::getVoteRequired(VoteTypes eVote, VoteSourceTypes eVoteSource) const
{
	return (countPossibleVote(eVote, eVoteSource) *
			GC.getInfo(eVote).getPopulationThreshold()) / 100;
}


TeamTypes CvGame::getSecretaryGeneral(VoteSourceTypes eVoteSource) const
{
	if (!canHaveSecretaryGeneral(eVoteSource))
	{
		FOR_EACH_ENUM(Building)
		{
			if (GC.getInfo(eLoopBuilding).getVoteSourceType() != eVoteSource)
				continue;
			for (PlayerIter<CIV_ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
			{
                // doc
                // TODO: filter
                if (itPlayer->isMinorCiv())
                    continue;

				if (itPlayer->getBuildingClassCount(
					GC.getInfo(eLoopBuilding).getBuildingClassType()) > 0)
				{
					ReligionTypes eReligion = getVoteSourceReligion(eVoteSource);
					if (eReligion == NO_RELIGION ||
						itPlayer->getStateReligion() == eReligion)
					{
						return itPlayer->getTeam();
					}
				}
			}
		}
		return NO_TEAM; // advc
	}
	FOR_EACH_ENUM(Vote)
	{
		if (GC.getInfo(eLoopVote).isVoteSourceType(eVoteSource) &&
			GC.getInfo(eLoopVote).isSecretaryGeneral() &&
			isVotePassed(eLoopVote))
		{
			TeamTypes eSecretary = (TeamTypes)getVoteOutcome(eLoopVote);
			if (GET_TEAM(eSecretary).isAlive()) // advc.001
				return eSecretary;
		}
	}
	return NO_TEAM;
}


bool CvGame::canHaveSecretaryGeneral(VoteSourceTypes eVoteSource) const
{
	FOR_EACH_ENUM(Vote)
	{
		if (GC.getInfo(eLoopVote).isVoteSourceType(eVoteSource) &&
			GC.getInfo(eLoopVote).isSecretaryGeneral())
		{
			return true;
		}
	}
	return false;
}


void CvGame::clearSecretaryGeneral(VoteSourceTypes eVoteSource)
{
	FOR_EACH_ENUM2(Vote, eVote)
	{
		CvVoteInfo& kVote = GC.getInfo(eVote);
		if (kVote.isVoteSourceType(eVoteSource) &&
			kVote.isSecretaryGeneral())
		{
			VoteTriggeredData kData;
			kData.eVoteSource = eVoteSource;
			kData.kVoteOption.eVote = eVote;
			kData.kVoteOption.iCityId = -1;
			kData.kVoteOption.szText.clear(); // kmodx
			kData.kVoteOption.ePlayer = NO_PLAYER;
			setVoteOutcome(kData, NO_PLAYER_VOTE);
			setSecretaryGeneralTimer(eVoteSource, 0);
		}
	}
}


void CvGame::updateSecretaryGeneral()
{
	FOR_EACH_ENUM(VoteSource)
	{
		TeamTypes eSecretary = getSecretaryGeneral(eLoopVoteSource);
		if (eSecretary != NO_TEAM &&
			(!GET_TEAM(eSecretary).isFullMember(eLoopVoteSource) ||
			GET_TEAM(eSecretary).isCapitulated())) // advc.014
		{
			clearSecretaryGeneral(eLoopVoteSource);
		}
	}
}


int CvGame::countCivPlayersAlive() const
{
	int iCount = 0;
	FOR_EACH_ENUM(CivPlayer)
	{
        // doc: exclude minors
		if (GET_PLAYER((PlayerTypes)eLoopCivPlayer).isAlive() && !GET_PLAYER((PlayerTypes)eLoopCivPlayer).isMinorCiv())
			iCount++;
	}
	return iCount;
}

// TODO: remove
int CvGame::countMajorPlayersAlive() const
{
    return countCivPlayersAlive();
}

int CvGame::countCivPlayersEverAlive() const
{	// advc.opt:
	FAssertMsg(!m_bAllGameDataRead, "Should use getCivPlayersEverAlive instead");
	int iCount = 0;
	FOR_EACH_ENUM(CivPlayer)
	{
		CvPlayer const& kPlayer = GET_PLAYER((PlayerTypes)eLoopCivPlayer);
		if (kPlayer.isEverAlive())
		{
			if (kPlayer.getParent() == NO_PLAYER)
				iCount++;
		}
	}
	return iCount;
}


int CvGame::countCivTeamsAlive() const
{
	int iCount = 0;
	FOR_EACH_ENUM(CivTeam)
	{
        // doc: exclude minors
		if (GET_TEAM((TeamTypes)eLoopCivTeam).isAlive() && !GET_TEAM((TeamTypes)eLoopCivTeam).isMinorCiv())
			iCount++;
	}
	return iCount;
}


int CvGame::countCivTeamsEverAlive() const
{	// advc.opt:
	FAssertMsg(!m_bAllGameDataRead, "Should use getCivTeamsEverAlive instead");
	std::set<int> teamsEverAlive;
	FOR_EACH_ENUM(CivPlayer)
	{
		CvPlayer& kPlayer = GET_PLAYER((PlayerTypes)eLoopCivPlayer);
		if (kPlayer.isEverAlive() &&
			kPlayer.getParent() == NO_PLAYER)
		{
			teamsEverAlive.insert(kPlayer.getTeam());
		}
	}
	return teamsEverAlive.size();
}


int CvGame::countHumanPlayersAlive() const
{
	int iCount = 0;
	FOR_EACH_ENUM(Player)
	{
		CvPlayer& kPlayer = GET_PLAYER(eLoopPlayer);
		if (kPlayer.isAlive() && (kPlayer.isHuman() ||
			/*	advc.127: To prevent CvGame::update from concluding that the
				game is over when human is still disabled at the start of a round. */
			kPlayer.isHumanDisabled()))
		{
			iCount++;
		}
	}
	return iCount;
}

// K-Mod:
int CvGame::countFreeTeamsAlive() const
{
	int iCount = 0;
	FOR_EACH_ENUM(CivTeam)
	{
		CvTeam const& kLoopTeam = GET_TEAM((TeamTypes)eLoopCivTeam);
		//if (kLoopTeam.isAlive() && !kLoopTeam.isCapitulated())
		// I'm in two minds about which of these to use here
		// advc.agent (note): Keep this as in K-Mod. Vassals aren't free.
		if (kLoopTeam.isAlive() && !kLoopTeam.isAVassal())
			iCount++;
	}
	return iCount;
}

// <advc.137>
int CvGame::getRecommendedPlayers() const
{
	CvWorldInfo const& kWorld = GC.getInfo(GC.getMap().getWorldSize());
	scaled r = kWorld.getDefaultPlayers();
	r *= per100(100 - 4 * getSeaLevelChange());
	r.clamp(2, PlayerIter<>::count());
	return r.round();
}

// advc.140:
int CvGame::getSeaLevelChange() const
{
	int iR = 0;
	SeaLevelTypes eSeaLevel = GC.getInitCore().getSeaLevel();
	if (eSeaLevel != NO_SEALEVEL)
		iR = GC.getInfo(eSeaLevel).getSeaLevelChange();
	return iR;
} // </advc.137>


int CvGame::countTotalCivPower() const
{
	int iCount = 0;
	for (PlayerIter<CIV_ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		iCount += itPlayer->getPower();
	}
	return iCount;
}


int CvGame::countTotalNukeUnits() const
{
	int iCount = 0;
	// advc.001: Don't exclude Barbarians
	for (PlayerIter<ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		iCount += itPlayer->getNumNukeUnits();
	}
	return iCount;
}


int CvGame::countKnownTechNumTeams(TechTypes eTech) const
{
	int iCount = 0;
	for (TeamIter<EVER_ALIVE> itTeam; itTeam.hasNext(); ++itTeam)
	{
		if (itTeam->isHasTech(eTech))
			iCount++;
	}
	return iCount;
}


int CvGame::getNumFreeBonuses(BuildingTypes eBuilding) const
{
	if (GC.getInfo(eBuilding).getNumFreeBonuses() == -1)
		return GC.getInfo(GC.getMap().getWorldSize()).getNumFreeBuildingBonuses();
	return GC.getInfo(eBuilding).getNumFreeBonuses();
}


int CvGame::countReligionLevels(ReligionTypes eReligion) const
{
	int iCount = 0;
	for (PlayerIter<ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		iCount += itPlayer->getHasReligionCount(eReligion);
	}
	return iCount;
}


int CvGame::countCorporationLevels(CorporationTypes eCorporation) const
{
	int iCount = 0;
	for (PlayerIter<ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		iCount += itPlayer->getHasCorporationCount(eCorporation);
	}
	return iCount;
}

void CvGame::replaceCorporation(CorporationTypes eOldCorp, CorporationTypes eNewCorp)
{
	for (PlayerIter<ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		FOR_EACH_CITY_VAR(pCity, *itPlayer)
		{
			if (pCity->isHasCorporation(eOldCorp))
			{
				pCity->setHasCorporation(eOldCorp, false, false, false);
				pCity->setHasCorporation(eNewCorp, true, true);
			}
		}
		FOR_EACH_UNIT_VAR(pUnit, *itPlayer)
		{
			if (pUnit->getUnitInfo().getCorporationSpreads(eOldCorp) > 0)
				pUnit->kill(false);
		}
	}
}


int CvGame::calculateReligionPercent(ReligionTypes eReligion,
	bool bIgnoreOtherReligions) const // advc.115b: Param added
{
	if (getTotalPopulation() == 0)
		return 0;

	int iCount = 0;
	for (PlayerIter<ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		FOR_EACH_CITY(pLoopCity, *itPlayer)
		{
			if (pLoopCity->isHasReligion(eReligion))
			{	// <advc.115b>
				if (bIgnoreOtherReligions)
					iCount += pLoopCity->getPopulation();
				else // </advc.115b>
				{
                    // doc: religion population
					iCount += pLoopCity->getReligionPopulation(eReligion);
				}
			}
		}
	}
	return (iCount * 100) / getTotalPopulation();
}


int CvGame::goldenAgeLength() const
{
	static int const iGOLDEN_AGE_LENGTH = GC.getDefineINT("GOLDEN_AGE_LENGTH"); // advc.opt
	int iLength = iGOLDEN_AGE_LENGTH;
	iLength *= GC.getInfo(getGameSpeedType()).getGoldenAgePercent();
	iLength /= 100;
	return iLength;
}


int CvGame::victoryDelay(VictoryTypes eVictory) const
{
	int iLength = GC.getInfo(eVictory).getVictoryDelayTurns();
	iLength *= GC.getInfo(getGameSpeedType()).getVictoryDelayPercent();
	iLength /= 100;
	return iLength;
}


int CvGame::getImprovementUpgradeTime(ImprovementTypes eImprovement) const
{
	int iTime = GC.getInfo(eImprovement).getUpgradeTime();
	iTime *= GC.getInfo(getGameSpeedType()).getImprovementPercent();
	iTime /= 100;
	iTime *= GC.getInfo(getStartEra()).getImprovementPercent();
	iTime /= 100;
	return iTime;
}

/*	advc.252: Default modifier for fully adjusting minor aspects of the rules or AI
	to the game speed setting (i.e. when adding an element to CvGameSpeedInfo isn't
	worth the trouble).
	Call locations not tagged with comments; had mostly used VictoryDelay before. */
int CvGame::getSpeedPercent() const
{
	/*	The relation of unit movement (not affected by game speed) to tech pace
		is what characterizes the game speed settings best in my book */
	return GC.getInfo(getGameSpeedType()).getResearchPercent();
}

bool CvGame::canTrainNukes() const
{
	for (PlayerIter<ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		CvCivilization const& kCiv = itPlayer->getCivilization(); // advc.003w
		for (int i = 0; i < kCiv.getNumUnits(); i++)
		{
			UnitTypes eUnit = kCiv.unitAt(i);
			if (GC.getInfo(eUnit).isNuke() && itPlayer->canTrain(eUnit))
				return true;
		}
	}
	return false;
}


EraTypes CvGame::getCurrentEra() const
{
	/*	advc.opt: OK - negligble. NB: Some call locations changed
		to CvGameAI::AI_getCurrEraFactor (computing time also negligible). */
	//PROFILE_FUNC();

	int iEra = 0;
	// K-Mod: don't count the barbarians
	PlayerIter<CIV_ALIVE> it;
	for (; it.hasNext(); ++it)
		iEra += it->getCurrentEra();
	int const iCount = it.nextIndex();
	if (iCount > 0)
	{
		//return (EraTypes)(iEra / iCount);
		return (EraTypes)intdiv::uround(iEra, iCount); // kekm.17
	}
	FAssert(iCount > 0); // advc
	return NO_ERA;
}

// advc:
EraTypes CvGame::getHighestEra() const
{
	EraTypes eMax = NO_ERA;
	for (PlayerIter<CIV_ALIVE> it; it.hasNext(); ++it)
		eMax = std::max(eMax, it->getCurrentEra());
	return eMax;
}

// advc.groundbr: Normalize tech costs when groundbreaking penalties are enabled
scaled CvGame::groundbreakingNormalizationModifier(TechTypes eTech) const
{
	if (!GC.getDefineBOOL(CvGlobals::AI_GROUNDBREAKING_PENALTY_ENABLE))
		return 0;
	EraTypes const eTechEra = GC.getInfo(eTech).getEra();
	if (eTechEra <= GC.getGame().getStartEra())
		return 0;
	return -per100(GC.getInfo(eTechEra).get(CvEraInfo::AIMaxGroundbreakingPenalty)) / 4;
}


CivilizationTypes CvGame::getActiveCivilizationType() const
{
	if (getActivePlayer() == NO_PLAYER)
		return NO_CIVILIZATION;
	return (CivilizationTypes)GET_PLAYER(getActivePlayer()).getCivilizationType();
}

// advc.003w:
CvCivilization const* CvGame::getActiveCivilization() const
{
	PlayerTypes eActivePlayer = getActivePlayer();
	if (eActivePlayer == NO_PLAYER)
		return NULL;
	return &GET_PLAYER(eActivePlayer).getCivilization();
}


bool CvGame::isGameMultiPlayer() const
{	// <advc.135c>
	if (m_bFeignSP)
		return false; // </advc.135c>
	return (isNetworkMultiPlayer() || isPbem() || isHotSeat());
}


bool CvGame::isTeamGame() const
{
	int iCivPlayersAlive = countCivPlayersAlive();
	int iCivTeamsAlive = countCivTeamsAlive();
	FAssert(iCivPlayersAlive >= iCivTeamsAlive);
	return (iCivPlayersAlive > iCivTeamsAlive);
}


bool CvGame::isModem() /* advc: */ const
{
	return gDLL->IsModem();
}


void CvGame::setModem(bool bModem)
{
	if (bModem)
		gDLL->ChangeINIKeyValue("CONFIG", "Bandwidth", "modem");
	else gDLL->ChangeINIKeyValue("CONFIG", "Bandwidth", "broadband");
	gDLL->SetModem(bModem);
}


void CvGame::reviveActivePlayer()
{
	if (GET_PLAYER(getActivePlayer()).isAlive())
		return;
	setAIAutoPlay(0);
	GC.getInitCore().setSlotStatus(getActivePlayer(), SS_TAKEN);
	// rfc: rise and fall mechanics
    //if (GC.getPythonCaller()->doReviveActivePlayer())
	//	return;
	//GET_PLAYER(getActivePlayer()).initUnit((UnitTypes)0, 0, 0);

    // doc
    GET_PLAYER(getActivePlayer()).verifyAlive();
    GET_PLAYER(getActivePlayer()).m_bTurnPlayed = false;
}


void CvGame::setGameTurn(int iNewValue)
{
	if (getGameTurn() == iNewValue)
		return;
	GC.getInitCore().setGameTurn(iNewValue);
	FAssert(getGameTurn() >= 0);
	updateBuildingCommerce();
	setScoreDirty(true);
	gDLL->getInterfaceIFace()->setDirty(TurnTimer_DIRTY_BIT, true);
	gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
}


void CvGame::incrementGameTurn()
{
	setGameTurn(getGameTurn() + 1);
}


int CvGame::getTurnYear(int iGameTurn) const
{
	/*	moved the body of this method to Game Core Utils so that we have
		access for other games than the current one (replay screen in HOF) */
	return getTurnYearForGame(iGameTurn, getStartYear(), getCalendar(), getGameSpeedType());
}


void CvGame::incrementElapsedGameTurns()
{
	m_iElapsedGameTurns++;
}

// advc.251:
int CvGame::AIHandicapAdjustment() const
{
	int iIncrementTurns = GC.getInfo(getHandicapType()).getAIHandicapIncrementTurns();
	if (iIncrementTurns == 0)
		return 0;
	/*	Flip sign b/c we're dealing with cost modifiers that are supposed to decrease.
		Only if a negative AIHandicapIncrement is set in XML, the modifiers are
		supposed to increase. */
	return (-getGameTurn() * 100) / (iIncrementTurns * getSpeedPercent());
}


void CvGame::setMaxTurns(int iNewValue)
{
	GC.getInitCore().setMaxTurns(iNewValue);
	FAssert(getMaxTurns() >= 0);
}


void CvGame::changeMaxTurns(int iChange)
{
	setMaxTurns(getMaxTurns() + iChange);
}


void CvGame::setMaxCityElimination(int iNewValue)
{
	GC.getInitCore().setMaxCityElimination(iNewValue);
	FAssert(getMaxCityElimination() >= 0);
}


void CvGame::setNumAdvancedStartPoints(int iNewValue)
{
	GC.getInitCore().setNumAdvancedStartPoints(iNewValue);
	FAssert(getNumAdvancedStartPoints() >= 0);
}


void CvGame::setStartTurn(int iNewValue)
{
	m_iStartTurn = iNewValue;
}


void CvGame::setStartYear(int iNewValue)
{
	m_iStartYear = iNewValue;
}


void CvGame::setEstimateEndTurn(int iNewValue)
{
	m_iEstimateEndTurn = iNewValue;
}

/*	advc: Ratio of turns played to total estimated game length; between 0 and 1.
	iDelay is added to the number of turns played. */
scaled CvGame::gameTurnProgress(int iDelay) const
{
	/*	Even with time victory disabled, we shouldn't expect the game to last
		beyond 2050. So, no need to check if it's disabled. */
	int iGameLength = getEstimateEndTurn() - getStartTurn();
	scaled r(getElapsedGameTurns() + iDelay, iGameLength);
	r.decreaseTo(1);
	return r;
}


int CvGame::getMinutesPlayed() const
{
	return getTurnSlice() / gDLL->getTurnsPerMinute();
}


int CvGame::getSecondsPlayed() const
{
	return getTurnSlice() / gDLL->getTurnsPerSecond();
}


void CvGame::setTurnSlice(int iNewValue)
{
	m_iTurnSlice = iNewValue;
}


void CvGame::changeTurnSlice(int iChange)
{
	setTurnSlice(getTurnSlice() + iChange);
}


int CvGame::getCutoffSlice() const
{
	return m_iCutoffSlice;
}


void CvGame::setCutoffSlice(int iNewValue)
{
	m_iCutoffSlice = iNewValue;
}


void CvGame::changeCutoffSlice(int iChange)
{
	setCutoffSlice(getCutoffSlice() + iChange);
}


void CvGame::resetTurnTimer()
{
	// We should only use the turn timer if we are in multiplayer
	if (isMPOption(MPOPTION_TURN_TIMER))
	{
		if (getElapsedGameTurns() > 0 || !isOption(GAMEOPTION_ADVANCED_START))
		{
			// Determine how much time we should allow
			int iTurnLen = getMaxTurnLen();
			if (getElapsedGameTurns() == 0 && !isPitboss())
			{
				// Let's allow more time for the initial turn
				TurnTimerTypes eTurnTimer = GC.getInitCore().getTurnTimer();
				FAssertMsg(eTurnTimer >= 0 && eTurnTimer < GC.getNumTurnTimerInfos(), "Invalid TurnTimer selection in InitCore");
				iTurnLen = (iTurnLen * GC.getInfo(eTurnTimer).getFirstTurnMultiplier());
			}
			// Set the current turn slice to start the 'timer'
			setCutoffSlice(getTurnSlice() + iTurnLen);
		}
	}
}


void CvGame::incrementTurnTimer(int iNumTurnSlices)
{
	if (isMPOption(MPOPTION_TURN_TIMER))
	{
		/*	If the turn timer has expired, we shouldn't increment it
			as we've sent our turn complete message. */
		if (getTurnSlice() <= getCutoffSlice())
			changeCutoffSlice(iNumTurnSlices);
	}
}


int CvGame::getMaxTurnLen()
{
	if (isPitboss())
	{	// Use the user-provided input. Turn time is in hours.
		return (getPitbossTurnTime() * 3600 * 4);
	}
	else
	{
		// Calculate the max turn time based on the max number of units and cities
		int iMaxUnits = 0;
		int iMaxCities = 0;
		for (PlayerIter<CIV_ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
		{
			iMaxUnits = std::max(iMaxUnits, itPlayer->getNumUnits());
			iMaxCities = std::max(iMaxCities, itPlayer->getNumCities());
		}
		// Now return turn len based on base len and unit and city bonuses
		TurnTimerTypes eTurnTimer = GC.getInitCore().getTurnTimer();
		return GC.getInfo(eTurnTimer).getBaseTime() +
				GC.getInfo(eTurnTimer).getCityBonus() * iMaxCities +
				GC.getInfo(eTurnTimer).getUnitBonus() * iMaxUnits;
	}
}


void CvGame::setTargetScore(int iNewValue)
{
	GC.getInitCore().setTargetScore(iNewValue);
	FAssert(getTargetScore() >= 0);
}


int CvGame::countNumHumanGameTurnActive() const
{
	int iCount = 0;
	for (PlayerIter<HUMAN> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		if (itPlayer->isTurnActive())
			iCount++;
	}
	return iCount;
}


void CvGame::changeNumGameTurnActive(int iChange)
{
	m_iNumGameTurnActive = (m_iNumGameTurnActive + iChange);
	FAssert(getNumGameTurnActive() >= 0);
	m_iUnitUpdateAttempts = 0; // advc.001y
}


int CvGame::getNumCivCities() const
{
	return getNumCities() - GET_PLAYER(BARBARIAN_PLAYER).getNumCities();
}


void CvGame::changeNumCities(int iChange)
{
	m_iNumCities += iChange;
	FAssert(getNumCities() >= 0);
}


void CvGame::changeTotalPopulation(int iChange)
{
	m_iTotalPopulation += iChange;
	FAssert(getTotalPopulation() >= 0);
}


void CvGame::changeTradeRoutes(int iChange)
{
	if (iChange != 0)
	{
		m_iTradeRoutes += iChange;
		FAssert(getTradeRoutes() >= 0);
		updateTradeRoutes();
	}
}


void CvGame::changeFreeTradeCount(int iChange)
{
	if (iChange == 0)
		return;
	bool const bOldFreeTrade = isFreeTrade();
	m_iFreeTradeCount += iChange;
	FAssert(getFreeTradeCount() >= 0);
	if (bOldFreeTrade != isFreeTrade())
		updateTradeRoutes();
}


void CvGame::changeNoNukesCount(int iChange)
{
	m_iNoNukesCount += iChange;
	FAssert(getNoNukesCount() >= 0);
}


void CvGame::setSecretaryGeneralTimer(VoteSourceTypes eVoteSource, int iNewValue)
{
	m_aiSecretaryGeneralTimer.set(eVoteSource, iNewValue);
	FAssert(getSecretaryGeneralTimer(eVoteSource) >= 0);
}


void CvGame::changeSecretaryGeneralTimer(VoteSourceTypes eVoteSource, int iChange)
{
	setSecretaryGeneralTimer(eVoteSource,
			getSecretaryGeneralTimer(eVoteSource) + iChange);
}


void CvGame::setVoteTimer(VoteSourceTypes eVoteSource, int iNewValue)
{
	m_aiVoteTimer.set(eVoteSource, iNewValue);
	FAssert(getVoteTimer(eVoteSource) >= 0);
}


void CvGame::changeVoteTimer(VoteSourceTypes eVoteSource, int iChange)
{
	setVoteTimer(eVoteSource, getVoteTimer(eVoteSource) + iChange);
}


void CvGame::changeNukesExploded(int iChange)
{
	m_iNukesExploded += iChange;
}

// advc: Moved from CvGameCoreUtils
int CvGame::getWonderScore(BuildingClassTypes eWonderClass) const
{
	if (GC.getInfo(eWonderClass).isLimited())
		return 5;
	return 0;
}

// initialize score calculation
void CvGame::initScoreCalculation()
{
	int iMaxFood = 0;
	FOR_EACH_ENUM(PlotNum)
	{
		CvPlot const& kPlot = GC.getMap().getPlotByIndex(eLoopPlotNum);
		if (!kPlot.isWater() || kPlot.isAdjacentToLand())
			iMaxFood += kPlot.calculateBestNatureYield(YIELD_FOOD, NO_TEAM);
	}
	m_iMaxPopulation = getPopulationScore(iMaxFood / std::max(1,
			GC.getFOOD_CONSUMPTION_PER_POPULATION()));
	m_iMaxLand = getLandPlotsScore(GC.getMap().getLandPlots());
	m_iMaxTech = 0;
	FOR_EACH_ENUM(Tech)
	{
		m_iMaxTech += getTechScore(eLoopTech);
	}
	m_iMaxWonders = 0;
	FOR_EACH_ENUM(BuildingClass)
	{
		m_iMaxWonders += getWonderScore(eLoopBuildingClass);
	}

	if (getStartEra() != NO_ERA)
	{
		int iNumSettlers = GC.getInfo(getStartEra()).getStartingUnitMultiplier();
		m_iInitPopulation = getPopulationScore(iNumSettlers *
				(GC.getInfo(getStartEra()).getFreePopulation() + 1));
		m_iInitLand = getLandPlotsScore(iNumSettlers * NUM_CITY_PLOTS);
	}
	else
	{
		m_iInitPopulation = 0;
		m_iInitLand = 0;
	}
	m_iInitTech = 0;
	FOR_EACH_ENUM(Tech)
	{
		if (GC.getInfo(eLoopTech).getEra() < getStartEra())
			m_iInitTech += getTechScore(eLoopTech);
		else
		{
			/*	count all possible free techs as initial to lower the score
				from immediate retirement */
			FOR_EACH_ENUM(Civilization)
			{
				if (GC.getInfo(eLoopCivilization).isPlayable())
				{
					if (GC.getInfo(eLoopCivilization).isCivilizationFreeTechs(
						eLoopCivilization))
					{
						m_iInitTech += getTechScore(eLoopTech);
						break;
					}
				}
			}
		}
	}
	m_iInitWonders = 0;
}


void CvGame::setAIAutoPlay(int iNewValue, /* <advc.127> */ bool bChangePlayerStatus)
{
	m_iAIAutoPlay = std::max(0, iNewValue);
	if (!bChangePlayerStatus)
		return; // </advc.127>
	// Erik <BM1>
	if (m_iAIAutoPlay == 0)
	{
		// Required by the benchmark to be informed when autoplay has completed
		CyArgsList pyArgs;
		pyArgs.add(getTurnSlice());
		CvEventReporter::getInstance().genericEvent("AutoPlayComplete", pyArgs.makeFunctionArgs());
	} // Erik </BM1>

	/*	AI_AUTO_PLAY_MOD, 07/09/08, jdog5000: START
		(Multiplayer compatibility idea from Jeckel) */
	// <advc.127> To make sure I'm not breaking anything in singleplayer
	if (!isGameMultiPlayer())
	{
		GET_PLAYER(getActivePlayer()).setHumanDisabled((getAIAutoPlay() != 0));
		return;
	} // </advc.127>
	for (PlayerIter<MAJOR_CIV> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		if (itPlayer->isHuman() || itPlayer->isHumanDisabled())
		{	/*	advc.127: Was GET_PLAYER(getActivePlayer()).
				Tagging advc.001 because that was probably a bug. */
			itPlayer->setHumanDisabled(getAIAutoPlay() != 0);
		}
	} // AI_AUTO_PLAY_MOD: END
}


void CvGame::changeAIAutoPlay(int iChange, /* advc.127: */ bool changePlayerStatus)
{
	setAIAutoPlay(getAIAutoPlay() + iChange, /* advc.127: */ changePlayerStatus);
}

// <advc.opt>
int CvGame::getCivPlayersEverAlive() const
{
	// Could pose a savegame compatibility problem (uiFlag<4)
	FAssert(m_bAllGameDataRead || m_iCivPlayersEverAlive > 0);
	if (!m_bAllGameDataRead)
		return countCivPlayersEverAlive();
	return m_iCivPlayersEverAlive;
}

void CvGame::changeCivPlayersEverAlive(int iChange)
{
	m_iCivPlayersEverAlive += iChange;
	//FAssert(iChange >= 0);
	/*	iChange normally shouldn't be negative, but liberated civs aren't supposed
		to count, and they're set to 'alive' before getting marked as liberated
		(CvPlayer::setParent), so they need to be subtracted once setParent is called. */
	FAssertBounds(0, MAX_CIV_PLAYERS + 1, m_iCivPlayersEverAlive);
}


int CvGame::getCivTeamsEverAlive() const
{
	// Could pose a savegame compatibility problem (uiFlag<4)
	FAssert(m_bAllGameDataRead || m_iCivTeamsEverAlive > 0);
	if (!m_bAllGameDataRead)
		return countCivTeamsEverAlive();
	return m_iCivTeamsEverAlive;
}

void CvGame::changeCivTeamsEverAlive(int iChange)
{
	m_iCivTeamsEverAlive += iChange;
	FAssertBounds(0, MAX_CIV_TEAMS + 1, m_iCivTeamsEverAlive);
} // </advc.opt>

// <K-Mod> 6/dec/10 (18/dec/10 - added Gw calc functions)
void CvGame::setGlobalWarmingIndex(int iNewValue)
{
	m_iGlobalWarmingIndex = std::max(0, iNewValue);
}


void CvGame::changeGlobalWarmingIndex(int iChange)
{
	setGlobalWarmingIndex(getGlobalWarmingIndex() + iChange);
}


int CvGame::getGlobalWarmingChances() const
{
	/*	Note: this is the number of chances global warming has to strike
		in the current turn. As you can see, I've scaled it by the game length.
		The probability per chance is also scaled like this. I estimate that
		the global warming index will actually be roughly proportional to the
		number of turns in the game, so, by scaling the chances, and the
		probability per chance, I hope to get roughly the same number of
		actual events per game. */
	scaled rIndexPerChance = GC.getDefineINT("GLOBAL_WARMING_INDEX_PER_CHANCE");
	rIndexPerChance *= per100(getSpeedPercent());
	/*	advc.055: The more teams there are, the less evenly the world tends to
		develop. GW causes the most damage when much of the world has a similar
		tech level in the middle of the Industrial era. */
	rIndexPerChance *= scaled(getCivTeamsEverAlive(), 8).pow(fixp(1/3.));
	rIndexPerChance.increaseTo(1);
	return (getGlobalWarmingIndex() / rIndexPerChance).round();
}


void CvGame::setGwEventTally(int iNewValue)
{
	m_iGwEventTally = iNewValue;
}


void CvGame::changeGwEventTally(int iChange)
{
	setGwEventTally(getGwEventTally() + iChange);
}

// worldwide pollution
int CvGame::calculateGlobalPollution() const
{
	int iGlobalPollution = 0;
	for (PlayerIter<ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
        // TODO: exclude plague from player pollution
		iGlobalPollution += itPlayer->calculatePollution();
	}
	return iGlobalPollution;
}

/*	if ePlayer == NO_PLAYER, all features are counted.
	Otherwise, only count features owned by the specified player. */
int CvGame::calculateGwLandDefence(PlayerTypes ePlayer) const
{
	int iTotal = 0;
	FOR_EACH_ENUM(PlotNum)
	{
		CvPlot const& kPlot = GC.getMap().getPlotByIndex(eLoopPlotNum);
		if (kPlot.isFeature())
		{
			if (ePlayer == NO_PLAYER || ePlayer == kPlot.getOwner())
			    iTotal += GC.getInfo(kPlot.getFeatureType()).getWarmingDefense();
		}
	}
	return iTotal;
}

// again, NO_PLAYER means everyone
int CvGame::calculateGwSustainabilityThreshold(PlayerTypes ePlayer) const
{
	/*	expect each pop to give ~10 pollution per turn at the time
		we cross the threshold, and ~1 pop per land tile...
		so default resistance should be around 10 per tile. */
	int iGlobalThreshold = GC.getMap().getLandPlots() *
			GC.getDefineINT("GLOBAL_WARMING_RESISTANCE");

	/*	maybe we should add some points for coastal tiles as well,
		so that watery maps don't get too much warming */

	if (ePlayer == NO_PLAYER)
		return iGlobalThreshold;

	/*	I have a few possible threshold distribution systems in mind:
		could be proportional to total natural food yield;
		or a combination of population, land size, total completed research,
		per player, etc.
		Currently, a player's share of the total threshold is just proportional
		to their land size (just like the threshold itself) */
	CvPlayer& kPlayer = GET_PLAYER(ePlayer);
	if (kPlayer.isAlive())
	{
		return iGlobalThreshold * kPlayer.getTotalLand() /
				std::max(1, GC.getMap().getLandPlots());
	}
	return 0;
}

int CvGame::calculateGwSeverityRating() const
{
	/*	Here are some of the properties I want from this function:
		- the severity should be a number between 0 and 100 (ie. a percentage value)
		- zero severity should mean zero global warming
		- the function should asymptote towards 100
		- It should be a function of the index divided by (total land area * game length).
	I recommend looking at the graph of this function to get a sense of how it works. */
	/*	advc: Was long, which is equivalent to int. Could use long long,
		but it looks like 32 bit should suffice. */
	int const x = GC.getDefineINT("GLOBAL_WARMING_PROB") * getGlobalWarmingIndex() /
			(GC.getMap().getLandPlots() * 4 * getSpeedPercent());
	// shape parameter. Lower values result in the function being steeper earlier.
	int const b = 55; // advc.055: was 70
	return 100 - (b * 100) / (b + SQR(x));
} // </K-Mod>

/*	advc.003j (comment): Both unused since the BtS expansion, though the EXE still
	calls setInitialTime at the start of a game. */
unsigned int CvGame::getInitialTime()
{
	return m_uiInitialTime;
}
void CvGame::setInitialTime(unsigned int uiNewValue)
{
	m_uiInitialTime = uiNewValue;
}


bool CvGame::isScoreDirty() const
{
	return m_bScoreDirty;
}


void CvGame::setScoreDirty(bool bNewValue)
{
	m_bScoreDirty = bNewValue;
}

// <advc.003r>
void CvGame::setUpdateTimer(UpdateTimerTypes eTimerType, int iDelay)
{
	FAssertBounds(0, NUM_UPDATE_TIMER_TYPES, eTimerType);
	// <advc.001w>
	if (eTimerType == UPDATE_MOUSE_FOCUS && BUGOption::isEnabled("MainInterface__RapidUnitCycling", false)) {
		// No need for this hack when there is no unit-cycling delay
		iDelay = -1;
	} // </advc.001w>
	m_aiUpdateTimers[eTimerType] = iDelay;
}


int CvGame::getUpdateTimer(UpdateTimerTypes eTimerType) const
{
	FAssertBounds(0, NUM_UPDATE_TIMER_TYPES, eTimerType);
	return m_aiUpdateTimers[eTimerType];
} // </advc.003r>


void CvGame::makeCircumnavigated()
{
	m_bCircumnavigated = true;
}


// rfc
// TODO: needed?
int CvGame::getCircumnavigated()
{
	return m_iCircumnavigated;
}


// rfc
// TODO: needed?
void CvGame::setCircumnavigated(int iNewValue)
{
	m_iCircumnavigated = iNewValue;
}


bool CvGame::circumnavigationAvailable() const
{
	static bool const bCIRCUMNAVIGATE_FREE_MOVES = GC.getDefineBOOL("CIRCUMNAVIGATE_FREE_MOVES"); // advc.opt
	if (!bCIRCUMNAVIGATE_FREE_MOVES)
		return false;
	}

	// doc: no circumnavigation in 1700 AD
	if (getScenario() == SCENARIO_1700AD)
		return false;

	if (isCircumnavigated())
		return false;

	CvMap& kMap = GC.getMap();

	if (!kMap.isWrapX() && !kMap.isWrapY())
		return false;

	if (kMap.getLandPlots() > (kMap.numPlots() * 2) / 3)
		return false;

	return true;
}


void CvGame::changeDiploVote(VoteSourceTypes eVoteSource, int iChange)
{
	if (iChange == 0)
		return;
	FOR_EACH_ENUM(Player)
	{
		GET_PLAYER(eLoopPlayer).processVoteSource(eVoteSource, false);
	}
	m_aiDiploVote.add(eVoteSource, iChange);
	FAssert(getDiploVoteCount(eVoteSource) >= 0);
	FOR_EACH_ENUM(Player)
	{
		GET_PLAYER(eLoopPlayer).processVoteSource(eVoteSource, true);
	}
}


bool CvGame::canDoResolution(VoteSourceTypes eVoteSource,
	VoteSelectionSubData const& kData) const
{
	CvVoteInfo const& kVote = GC.getInfo(kData.eVote);
	if (kVote.isVictory())
	{
		int iVotesRequired = getVoteRequired(kData.eVote, eVoteSource); // K-Mod
		for (TeamIter<MAJOR_CIV> itTeam; itTeam.hasNext(); ++itTeam)
		{
			if (itTeam->getVotes(kData.eVote, eVoteSource) >= iVotesRequired)
				return false; // K-Mod. same, but faster.
			/*if (itTeam->isVotingMember(eVoteSource)) {
				if (itTeam->getVotes(kData.eVote, eVoteSource) >= getVoteRequired(kData.eVote, eVoteSource)) {
					// Can't vote on a winner if one team already has all the votes necessary to win
					return false;
				}
			}*/ // BtS
		}
	}
	for (PlayerIter<MAJOR_CIV> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		if (itPlayer->isVotingMember(eVoteSource))
		{	// <kekm.25/advc>
			if (kVote.isForceWar())
			{
				if (GET_TEAM(itPlayer->getTeam()).isFullMember(eVoteSource) &&
					!itPlayer->canDoResolution(eVoteSource, kData))
				{
					return false;
				}
			}
			else // </kekm.25/advc>
			if (!itPlayer->canDoResolution(eVoteSource, kData))
				return false;
		}
		else
		{
			// all players need to be able to vote for a diplo victory
			if (kVote.isVictory())
				return false;
		}
	}
	return true;
}

// advc (note): Needs to be consistent with processVote
bool CvGame::isValidVoteSelection(VoteSourceTypes eVoteSource,
	VoteSelectionSubData const& kData) const
{
	if (kData.ePlayer!= NO_PLAYER)
	{
		CvPlayer& kPlayer = GET_PLAYER(kData.ePlayer);
		if (!kPlayer.isAlive() || !kPlayer.isMajorCiv())
			return false;
	}
	if (kData.eOtherPlayer != NO_PLAYER)
	{
		CvPlayer& kPlayer = GET_PLAYER(kData.eOtherPlayer);
		if (!kPlayer.isAlive() || !kPlayer.isMajorCiv())
			return false;
	}
	int iVoters = 0;
	for (TeamIter<MAJOR_CIV> itTeam; itTeam.hasNext(); ++itTeam)
	{
		//if (GET_TEAM((TeamTypes)iTeam).isVotingMember(eVoteSource))
		// K-Mod. to prevent "AP cheese", only count full members for victory votes.
		if (itTeam->isFullMember(eVoteSource) ||
			(!GC.getInfo(kData.eVote).isVictory() &&
			itTeam->isVotingMember(eVoteSource))) // K-Mod end
		{
			++iVoters;
		}
	}
	if (iVoters < GC.getInfo(kData.eVote).getMinVoters())
		return false;
	if (GC.getInfo(kData.eVote).isOpenBorders())
	{
		bool bOpenBordersWithEveryone = true;
		for (TeamIter<MAJOR_CIV> itFirst; itFirst.hasNext(); ++itFirst)
		{
			/*	advc (note): Applies to all members, but becomes unavailable if
				all full members already have OB. Not sure if that's sensible. */
			if (!itFirst->isFullMember(eVoteSource))
				continue;
			for (TeamIter<MAJOR_CIV> itSecond; itSecond.hasNext(); ++itSecond)
			{
				if (!itSecond->isFullMember(eVoteSource))
					continue;
				if (itSecond->getID() > itFirst->getID())
				{
					if (!itSecond->isOpenBorders(itFirst->getID()))
					{
						bOpenBordersWithEveryone = false;
						break;
					}
				}
			}
		}
		if (bOpenBordersWithEveryone)
			return false;
	}
	else if (GC.getInfo(kData.eVote).isDefensivePact())
	{
		bool bDefensivePactWithEveryone = true;
		// advc.001: Exclude vassals
		for (TeamIter<FREE_MAJOR_CIV> itFirst; itFirst.hasNext(); ++itFirst)
		{
			/*	advc (note): Applies to all members, but becomes unavailable if
				all full members already have DP. Not sure if that's sensible. */
			if (!itFirst->isFullMember(eVoteSource))
				continue;
			// advc.001: Exclude vassals
			for (TeamIter<FREE_MAJOR_CIV> itSecond; itSecond.hasNext(); ++itSecond)
			{
				if (!itSecond->isFullMember(eVoteSource))
					continue;
				if (itSecond->getID() > itFirst->getID())
				{
					if (!itFirst->isDefensivePact(itSecond->getID()))
					{
						bDefensivePactWithEveryone = false;
						break;
					}
				}
			}
		}
		if (bDefensivePactWithEveryone)
			return false;
	}
	else if (GC.getInfo(kData.eVote).isForcePeace())
	{
		CvPlayer const& kPlayer = GET_PLAYER(kData.ePlayer);
		if (kPlayer.isAVassal()) // advc
			return false;
		//if (!kPlayer.isFullMember(eVoteSource))
		// kekm.25: 'These are not necessarily the same.'
		if (!GET_TEAM(kPlayer.getTeam()).isFullMember(eVoteSource))
			return false;

		bool bValid = false;
		// advc.178: Exclude vassals
		for (TeamIter<FREE_MAJOR_CIV,ENEMY_OF> it(kPlayer.getTeam()); it.hasNext(); ++it)
		{
			if (it->isVotingMember(eVoteSource))
			{
				bValid = true;
				break;
			}
		}

		if (!bValid)
			return false;
	}
	else if (GC.getInfo(kData.eVote).isForceNoTrade())
	{
		CvPlayer const& kPlayer = GET_PLAYER(kData.ePlayer);
		//if (kPlayer.isFullMember(eVoteSource))
		// kekm.25: 'These are not necessarily the same.'
		if (GET_TEAM(kPlayer.getTeam()).isFullMember(eVoteSource))
			return false;

		bool bNoTradeWithEveryone = true;
		for (PlayerIter<MAJOR_CIV,NOT_SAME_TEAM_AS> itOther(kPlayer.getTeam());
			itOther.hasNext(); ++itOther)
		{
			//if (itOther->isFullMember(eVoteSource))
			// kekm.25: 'These are not necessarily the same.'
			if (GET_TEAM(itOther->getTeam()).isFullMember(eVoteSource) &&
				itOther->canStopTradingWithTeam(kPlayer.getTeam()))
			{
				bNoTradeWithEveryone = false;
				break;
			}
		}
		if (bNoTradeWithEveryone)
			return false;
	}
	else if (GC.getInfo(kData.eVote).isForceWar())
	{
		CvPlayer const& kPlayer = GET_PLAYER(kData.ePlayer);
		CvTeam const& kTeam = GET_TEAM(kPlayer.getTeam());
		if (kTeam.isAVassal())
			return false;
		//if (kPlayer.isFullMember(eVoteSource))
		// kekm.25: 'These are not necessarily the same.'
		if (GET_TEAM(kPlayer.getTeam()).isFullMember(eVoteSource))
			return false;

        // doc: cannot target the current leader
        if (kPlayer.getTeam() == getSecretaryGeneral(eVoteSource))
            return false;

	    // doc: crusade target if at war with a full member or controlling the holy city
        // TODO: refactor
	    if (eVoteSourceReligion != NO_RELIGION)
	    {
	        bool bDefensiveCrusade = false;
	        bool bOffensiveCrusade = false;

	        if (GC.getGame().getHolyCity(eVoteSourceReligion) != NULL && GC.getGame().getHolyCity(eVoteSourceReligion)->getOwner() == kPlayer.getID())
	        {
	            bOffensiveCrusade = true;
	        }

	        if (kPlayer.countNumBuildings((BuildingTypes)GC.getInfoTypeForString("BUILDING_CATHOLIC_SHRINE")) > 0)
	        {
	            bOffensiveCrusade = true;
	        }

	        for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; iPlayer++)
	        {
	            if (GET_PLAYER((PlayerTypes)iPlayer).isMinorCiv())
	            {
	                continue;
	            }

	            if (GET_PLAYER((PlayerTypes)iPlayer).isFullMember(eVoteSource))
	            {
	                if (GET_TEAM(GET_PLAYER((PlayerTypes)iPlayer).getTeam()).isAtWar(kPlayer.getTeam()))
	                {
	                    bDefensiveCrusade = true;
	                    break;
	                }
	            }
	        }

	        if (!bDefensiveCrusade && !bOffensiveCrusade)
	        {
	            return false;
	        }
	    }

        // doc: skip old logic
		/*bool bAtWarWithEveryone = true;
		for (TeamIter<MAJOR_CIV,NOT_SAME_TEAM_AS> itOther(kPlayer.getTeam());
			itOther.hasNext(); ++itOther)
		{
			if (itOther->isFullMember(eVoteSource) &&
				!itOther->isAtWar(kPlayer.getTeam()) &&
				itOther->canChangeWarPeace(kPlayer.getTeam()))
			{
				bAtWarWithEveryone = false;
				break;
			}
		}
		// Not an option if already at war with everyone
		if (bAtWarWithEveryone)
			return false;

		//if (!kPlayer.isVotingMember(eVoteSource))
		// kekm.25:
		if (!GET_TEAM(kPlayer.getTeam()).isFullMember(eVoteSource))
		{
			// Can be passed only if already at war with a member
			bool bValid = false;
			for (TeamIter<MAJOR_CIV,ENEMY_OF> itEnemy(kPlayer.getTeam());
				itEnemy.hasNext(); ++itEnemy)
			{
				if (itEnemy->isFullMember(eVoteSource))
				{
					bValid = true;
					break;
				}
			}
			if (!bValid)
				return false;
		}*/
	}
	else if (GC.getInfo(kData.eVote).isAssignCity())
	{
		CvPlayer const& kPlayer = GET_PLAYER(kData.ePlayer);
		//if (kPlayer.isFullMember(eVoteSource) || !kPlayer.isVotingMember(eVoteSource))
		// kekm.25: 'These are not necessarily the same'
		if (GET_TEAM(kPlayer.getTeam()).isFullMember(eVoteSource) ||
			!GET_TEAM(kPlayer.getTeam()).isVotingMember(eVoteSource))
		{
			return false;
		}
		CvCity const* pCity = kPlayer.getCity(kData.iCityId);
		if (pCity == NULL)
		{
			FAssert(pCity != NULL);
			return false;
		}
        // doc: cannot vote away last city
        if (kPlayer.getNumCities() == 1)
            return false;
		if (kData.eOtherPlayer == NO_PLAYER)
			return false;
		CvPlayer& kOtherPlayer = GET_PLAYER(kData.eOtherPlayer);
		if (kOtherPlayer.getTeam() == kPlayer.getTeam())
			return false;
		if (atWar(kPlayer.getTeam(), TEAMID(kData.eOtherPlayer)))
			return false;
		//if (!kOtherPlayer.isFullMember(eVoteSource))
		// kekm.25: 'These are not necessarily the same'
		if (!GET_TEAM(kOtherPlayer.getTeam()).isFullMember(eVoteSource))
			return false;
		if (kOtherPlayer.isOneCityChallenge())
			return false;
	}
    // doc: espionage resolution
	else if (GC.getVoteInfo(kData.eVote).getEspionage() > 0)
	{
		CvPlayer const& kPlayer = GET_PLAYER(kData.ePlayer);
		CvPlayer const& kOtherPlayer = GET_PLAYER(kData.eOtherPlayer);

		if (kOtherPlayer.getTeam() == getSecretaryGeneral(eVoteSource))
			return false;
		if (!kOtherPlayer.isFullMember(eVoteSource))
			return false;
		if (GET_TEAM(kOtherPlayer.getTeam()).isVassal(kPlayer.getTeam()))
			return false;
	}
    // doc: gold resolution
    // TODO: refactor
	else if (GC.getVoteInfo(kData.eVote).getGoldPercent() > 0)
	{
		// impossible if there is a war between full members
		for (int iTeam1 = 0; iTeam1 < MAX_CIV_TEAMS; ++iTeam1)
		{
			CvTeam& kTeam1 = GET_TEAM((TeamTypes)iTeam1);
			if (kTeam1.isFullMember(eVoteSource))
			{
				for (int iTeam2 = iTeam1+1; iTeam2 < MAX_CIV_TEAMS; ++iTeam2)
				{
					CvTeam& kTeam2 = GET_TEAM((TeamTypes)iTeam2);
					if (kTeam2.isFullMember(eVoteSource))
					{
						if (kTeam1.isAtWar((TeamTypes)iTeam2)) return false;
					}
				}
			}
		}
	}
    // doc: revoke membership resolution
	else if (GC.getVoteInfo(kData.eVote).isRevokeMembership())
	{
	    CvPlayer const& kPlayer = GET_PLAYER(kData.ePlayer);

		if (kPlayer.getTeam() == getSecretaryGeneral(eVoteSource))
			return false;
		if (!kPlayer.isFullMember(eVoteSource))
			return false;
		if (GET_TEAM(kPlayer.getTeam()).isVassal(getSecretaryGeneral(eVoteSource)))
			return false;
	}
    // doc: decolonize resolution
    // TODO: refactor
	else if (GC.getVoteInfo(kData.eVote).isDecolonize())
	{
	    CvPlayer const& kPlayer = GET_PLAYER(kData.ePlayer);
		CvCity* pCity = kPlayer.getCity(kData.iCityId);

		// only civs at peace can be forced to decolonize
		CvTeam& kTeam = GET_TEAM(kPlayer.getTeam());
		for (int iI = 0; iI < MAX_CIV_TEAMS; iI++)
		{
			if (GET_TEAM((TeamTypes)iI).isMinorCiv())
				continue;

			if (kTeam.isAtWar((TeamTypes)iI))
				return false;
		}
	}
    // doc: release civilization
	else if (GC.getVoteInfo(kData.eVote).isReleaseCivilization())
	{
	    CvPlayer const& kPlayer = GET_PLAYER(kData.ePlayer);

		if (GET_TEAM(kPlayer.getTeam()).isVassal(getSecretaryGeneral(eVoteSource)))
			return false;
	}

	return canDoResolution(eVoteSource, kData);
}


void CvGame::toggleDebugMode()
{	// <advc.135c>
	if (!m_bDebugMode && !isDebugToolsAllowed(false))
		return; // </advc.135c>
	m_bDebugMode = (m_bDebugMode ? false : true);
	updateDebugModeCache();

	GC.getMap().updateVisibility();
	GC.getMap().updateSymbols();
	GC.getMap().updateMinimapColor();
	/*	advc.001w (note): updateVisibility does this more selectively
		-- too selectively, unfortunately, in the special case of foreign spies. */
	GC.getMap().setFlagsDirty(); // K-Mod
	updateColoredPlots(); // K-Mod

	gDLL->UI().setDirty(GameData_DIRTY_BIT, true);
	gDLL->UI().setDirty(Score_DIRTY_BIT, true);
	gDLL->UI().setDirty(MinimapSection_DIRTY_BIT, true);
	gDLL->UI().setDirty(UnitInfo_DIRTY_BIT, true);
	gDLL->UI().setDirty(CityInfo_DIRTY_BIT, true);
	gDLL->UI().setDirty(GlobeLayer_DIRTY_BIT, true);

	//gDLL->getEngineIFace()->SetDirty(GlobeTexture_DIRTY_BIT, true);
	gDLL->getEngineIFace()->SetDirty(MinimapTexture_DIRTY_BIT, true);
	gDLL->getEngineIFace()->SetDirty(CultureBorders_DIRTY_BIT, true);

	if (m_bDebugMode)
		gDLL->getEngineIFace()->PushFogOfWar(FOGOFWARMODE_OFF);
	else gDLL->getEngineIFace()->PopFogOfWar();

	gDLL->getEngineIFace()->setFogOfWarFromStack();
	// <advc.045>
	// (Seems to add a noticeable delay; not worth it I think.)
	/*for (PlayerIter<ALIVE,NOT_SAME_TEAM_AS> itPlayer(getActiveTeam());
		itPlayer.hasNext(); ++itPlayer)
	{
		FOR_EACH_CITY_VAR(pCity, *itPlayer)
			pCity->setLayoutDirty(true);
	}*/ // </advc.045>
}

void CvGame::updateDebugModeCache()
{
	//if ((gDLL->getChtLvl() > 0) || (gDLL->GetWorldBuilderMode()))
	if (isDebugToolsAllowed(false)) // advc.135c
		m_bDebugModeCache = m_bDebugMode;
	else m_bDebugModeCache = false;
}

// advc.135c:
bool CvGame::isDebugToolsAllowed(bool bWB) const
{
	if (gDLL->getInterfaceIFace()->isInAdvancedStart())
		return false;
	if (gDLL->GetWorldBuilderMode())
		return true;
	if (isGameMultiPlayer())
	{
		if (!GC.getDefineBOOL(CvGlobals::ENABLE_DEBUG_TOOLS_MULTIPLAYER))
			return false;
		if (isHotSeat())
			return true;
		return isGameNameEnableDebugTools(GC.getInitCore().getGameName());
	}
	if (bWB)
	{
		// Cut from canDoControl (CvGameInterface.cpp)
		return GC.getInitCore().getAdminPassword().empty();
	}
	return gDLL->getChtLvl() > 0;
}

// advc.135c:
bool CvGame::isGameNameEnableDebugTools(CvWString const& kGameName) const
{
	return (kGameName.compare(L"chipotle") == 0);
}


int CvGame::getPitbossTurnTime() const
{
	return GC.getInitCore().getPitbossTurnTime();
}


void CvGame::setPitbossTurnTime(int iHours)
{
	GC.getInitCore().setPitbossTurnTime(iHours);
}


bool CvGame::isSimultaneousTeamTurns() const
{
	if (!isNetworkMultiPlayer())
		return false;

	if (isMPOption(MPOPTION_SIMULTANEOUS_TURNS))
		return false;

	return true;
}

/*	advc (note): Not called when loading a savegame from the opening menu.
	Not set to false upon returning to the main menu. */
void CvGame::setFinalInitialized(bool bNewValue)
{
	PROFILE_FUNC();

	if (isFinalInitialized() == bNewValue)
		return;
	m_bFinalInitialized = bNewValue;
	if (!isFinalInitialized())
		return;
	updatePlotGroups();
	GC.getMap().updateIrrigated();
	// <advc.158> Replacing K-Mod code. If spawned later, CvPlayer::initInGame will handle it.
	for (TeamAIIter<ALIVE> itTeam; itTeam.hasNext(); ++itTeam)
	{
		itTeam->AI_strengthMemory().init(
				GC.getMap().numPlots(), itTeam->getID());
	} // </advc.158>
	for (TeamAIIter<ALIVE> itTeam; itTeam.hasNext(); ++itTeam)
		itTeam->AI_updateAreaStrategies();
}


bool CvGame::getPbemTurnSent() const
{
	return m_bPbemTurnSent;
}


void CvGame::setPbemTurnSent(bool bNewValue)
{
	m_bPbemTurnSent = bNewValue;
}


bool CvGame::getHotPbemBetweenTurns() const
{
	return m_bHotPbemBetweenTurns;
}


void CvGame::setHotPbemBetweenTurns(bool bNewValue)
{
	m_bHotPbemBetweenTurns = bNewValue;
}


bool CvGame::isPlayerOptionsSent() const
{
	return m_bPlayerOptionsSent;
}


void CvGame::sendPlayerOptions(bool bForce)
{
	if (getActivePlayer() == NO_PLAYER)
		return;
	if (!isPlayerOptionsSent() || bForce)
	{
		m_bPlayerOptionsSent = true;
		FOR_EACH_ENUM(PlayerOption)
		{
			gDLL->sendPlayerOption(eLoopPlayerOption,
					gDLL->getPlayerOption(eLoopPlayerOption));
		}
	}
}


void CvGame::setActivePlayer(PlayerTypes eNewValue, bool bForceHotSeat)
{
	PlayerTypes const eOldActivePlayer = getActivePlayer();
	if (eOldActivePlayer == eNewValue)
		return;
	int const iActiveNetId = (eOldActivePlayer != NO_PLAYER ?
			GET_PLAYER(eOldActivePlayer).getNetID() : -1);

    // rfc
    GC.getInitCore().setSlotStatus(eOldActivePlayer, SS_COMPUTER);
    GC.getInitCore().setSlotStatus(eNewValue, SS_TAKEN);

	GC.getInitCore().setActivePlayer(eNewValue);
	if (eNewValue != NO_PLAYER && // K-Mod
		GET_PLAYER(eNewValue).isHuman() &&
		(isHotSeat() || isPbem() || bForceHotSeat))
	{
		gDLL->getPassword(eNewValue);
		setHotPbemBetweenTurns(false);
		gDLL->getInterfaceIFace()->dirtyTurnLog(eNewValue);
		if (eOldActivePlayer != NO_PLAYER)
		{
			int iInactiveNetId = GET_PLAYER(eNewValue).getNetID();
			GET_PLAYER(eNewValue).setNetID(iActiveNetId);
			GET_PLAYER(eOldActivePlayer).setNetID(iInactiveNetId);
		}
		GET_PLAYER(eNewValue).showMissedMessages();
		if (countHumanPlayersAlive() == 1 && isPbem())
		{	// Nobody else left alive
			GC.getInitCore().setType(GAME_HOTSEAT_NEW);
		}
        // rfc
		//if (isHotSeat() || bForceHotSeat)
		//	sendPlayerOptions(true);
        sendPlayerOptions(true);

        // doc: enables victory again after switch
        if (getGameState() == GAMESTATE_EXTENDED)
            setGameState(GAMESTATE_ON)
	}
	updateActiveVisibility(); // advc.706: Moved into subroutine
}

// advc.706: Cut and pasted from CvGame::setActivePlayer
void CvGame::updateActiveVisibility()
{
	if (!GC.IsGraphicsInitialized())
		return;
	/*	<advc.001> Moved up - clear selection lists before
		updating the center unit in updateVisibility */
	gDLL->getInterfaceIFace()->clearSelectedCities();
	gDLL->getInterfaceIFace()->clearSelectionList(); // </advc.001>
	GC.getMap().updateFog();
	GC.getMap().updateVisibility();
	GC.getMap().updateSymbols();
	GC.getMap().updateMinimapColor();

	updateUnitEnemyGlow();

    gDLL->getInterfaceIFace()->setInAdvancedStart(false); // doc
    gDLL->getInterfaceIFace()->setWorldBuilder(false); // doc
	gDLL->getInterfaceIFace()->setEndTurnMessage(false);

	gDLL->getInterfaceIFace()->setDirty(PercentButtons_DIRTY_BIT, true);
	gDLL->getInterfaceIFace()->setDirty(ResearchButtons_DIRTY_BIT, true);
	gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
	gDLL->getInterfaceIFace()->setDirty(MinimapSection_DIRTY_BIT, true);
	gDLL->getInterfaceIFace()->setDirty(CityInfo_DIRTY_BIT, true);
	gDLL->getInterfaceIFace()->setDirty(UnitInfo_DIRTY_BIT, true);
	gDLL->getInterfaceIFace()->setDirty(Flag_DIRTY_BIT, true);
	gDLL->getInterfaceIFace()->setDirty(GlobeLayer_DIRTY_BIT, true);
	// <advc.003p>
	if (getActivePlayer() != NO_PLAYER)
		GET_PLAYER(getActivePlayer()).setBonusHelpDirty();
	FAssert(getActivePlayer() != NO_PLAYER);
	// </advc.003p>
	gDLL->getEngineIFace()->SetDirty(CultureBorders_DIRTY_BIT, true);
	gDLL->getInterfaceIFace()->setDirty(BlockadedPlots_DIRTY_BIT, true);
}


void CvGame::updateUnitEnemyGlow()
{
	for (PlayerIter<ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		FOR_EACH_UNIT_VAR(pLoopUnit, *itPlayer)
			gDLL->getEntityIFace()->updateEnemyGlow(pLoopUnit->getEntity());
	}
}


void CvGame::setHandicapType(HandicapTypes eHandicap)
{
	m_eHandicap = eHandicap;
}

// advc.250: This was originally a one-liner in CvUtils.py
int CvGame::getDifficultyForEndScore() const
{
	CvHandicapInfo const& kGameHandicap = GC.getInfo(getHandicapType());
	scaled r = kGameHandicap.getDifficulty();
	// <advc.084>
	if (getCivTeamsEverAlive() == 1)
		r /= 4; // </advc.084>
	if (isOption(GAMEOPTION_ONE_CITY_CHALLENGE))
		r += 30;
	if (!isOption(GAMEOPTION_SPAH))
		return r.round();
	std::vector<int> aiStartPointDistrib;
	m_pSpah->distribution(aiStartPointDistrib);
	std::vector<scaled> arDistr;
	for (size_t i = 0; i < aiStartPointDistrib.size(); i++)
		arDistr.push_back(aiStartPointDistrib[i]);
	return (r + (stats::max(arDistr) + stats::mean(arDistr)) /
			kGameHandicap.getAIAdvancedStartPercent()).round();
}


PlayerTypes CvGame::getPausePlayer() const
{
	return m_ePausePlayer;
}


bool CvGame::isPaused() const
{
	return (getPausePlayer() != NO_PLAYER);
}


void CvGame::setPausePlayer(PlayerTypes eNewValue)
{
	m_ePausePlayer = eNewValue;
}


UnitTypes CvGame::getBestLandUnit() const
{
	return m_eBestLandUnit;
}


int CvGame::getBestLandUnitCombat() const
{
	if (getBestLandUnit() == NO_UNIT)
		return 1;
	return std::max(1, GC.getInfo(getBestLandUnit()).getCombat());
}


void CvGame::setBestLandUnit(UnitTypes eNewValue)
{
	if (getBestLandUnit() != eNewValue)
	{
		m_eBestLandUnit = eNewValue;
		gDLL->getInterfaceIFace()->setDirty(UnitInfo_DIRTY_BIT, true);
	}
}


void CvGame::setWinner(TeamTypes eNewWinner, VictoryTypes eNewVictory)
{
	if (getWinner() == eNewWinner && getVictory() == eNewVictory)
		return;
	m_eWinner = eNewWinner;
	m_eVictory = eNewVictory;
	// advc.707: Handled by RiseFall::prepareForExtendedGame
	if (!isOption(GAMEOPTION_RISE_FALL))
	{	// AI_AUTO_PLAY_MOD, 07/09/08, jdog5000:
		CvEventReporter::getInstance().victory(eNewWinner, eNewVictory);
	}
	if (getVictory() != NO_VICTORY)
	{
		if (getWinner() != NO_TEAM)
		{
			CvWString szBuffer(gDLL->getText("TXT_KEY_GAME_WON",
					//GET_TEAM(getWinner()).getReplayName().GetCString(),
                    GET_PLAYER(GET_TEAM(getWinner()).getLeadrID()).getCivilzationShortDescription(), // rfc
					GC.getInfo(getVictory()).getTextKeyWide()));
			addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT,
					GET_TEAM(getWinner()).getLeaderID(), szBuffer,
					GC.getColorType("HIGHLIGHT_TEXT"));
		}
		if ((getAIAutoPlay() > 0 || gDLL->GetAutorun()) &&
			!isOption(GAMEOPTION_RISE_FALL)) // advc.707
		{
			setGameState(GAMESTATE_EXTENDED);
		}
		else setGameState(GAMESTATE_OVER);
	}
	gDLL->UI().setDirty(Center_DIRTY_BIT, true);
	CvEventReporter::getInstance().victory(eNewWinner, eNewVictory);
	// gDLL->UI().setDirty(Soundtrack_DIRTY_BIT, true); // victory soundtrack
}


void CvGame::setGameState(GameStateTypes eNewValue)
{
	if (getGameState() == eNewValue)
		return;
	m_eGameState = eNewValue;
	if (eNewValue == GAMESTATE_OVER)
	{
		CvEventReporter::getInstance().gameEnd();
		// BULL - AutoSave - start
		if (BUGOption::isEnabled("AutoSave__CreateEndSave", false))
			GC.getPythonCaller()->call("gameEndSave", PYCivModule);
		// BULL - AutoSave - end
		// <advc.707>
		if (isOption(GAMEOPTION_RISE_FALL))
			m_pRiseFall->prepareForExtendedGame(); // </advc.707>
		showEndGameSequence();
		// advc (note): For dead humans, the popup will only lead to the opening menu.
		for (PlayerIter<EVER_ALIVE> itHuman; itHuman.hasNext(); ++itHuman)
		{
			if (!itHuman->isHuman())
				continue;
			// One more turn?
			CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_EXTENDED_GAME);
			if (pInfo != NULL)
				itHuman->addPopup(pInfo);
		}
	}
	gDLL->UI().setDirty(Cursor_DIRTY_BIT, true);
}


void CvGame::setRankPlayer(PlayerTypes eRank, PlayerTypes ePlayer)
{
	if (getRankPlayer(eRank) != ePlayer)
	{
		m_aeRankPlayer.set(eRank, ePlayer);
		gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);
	}
}


void CvGame::setPlayerRank(PlayerTypes ePlayer, PlayerTypes eRank)
{
	m_aePlayerRank.set(ePlayer, eRank);
}


void CvGame::setPlayerScore(PlayerTypes ePlayer, int iScore)
{
	if (getPlayerScore(ePlayer) == iScore)
		return;
	m_aiPlayerScore.set(ePlayer, iScore);
	FAssert(getPlayerScore(ePlayer) >= 0);
	gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);
}


void CvGame::setRankTeam(TeamTypes eRank, TeamTypes eTeam)
{
	if (getRankTeam(eRank) != eTeam)
	{
		m_aeRankTeam.set(eRank, eTeam);
		gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);
	}
}


void CvGame::setTeamRank(TeamTypes eTeam, TeamTypes eRank)
{
	m_aeTeamRank.set(eTeam, eRank);
}


void CvGame::setTeamScore(TeamTypes eTeam, int iScore)
{
	m_aiTeamScore[eTeam] = iScore;
	FAssert(getTeamScore(eTeam) >= 0);
}


void CvGame::setOption(GameOptionTypes eIndex, bool bEnabled)
{
	GC.getInitCore().setOption(eIndex, bEnabled);
}


void CvGame::setMPOption(MultiplayerOptionTypes eIndex, bool bEnabled)
{
	GC.getInitCore().setMPOption(eIndex, bEnabled);
}


void CvGame::setForceControl(ForceControlTypes eIndex, bool bEnabled)
{
	GC.getInitCore().setForceControl(eIndex, bEnabled);
}

// advc: Mostly cut from CvPlayer::canConstruct
bool CvGame::canConstruct(BuildingTypes eBuilding,
	bool bIgnoreCost, bool bTestVisible) const
{
	CvBuildingInfo const& kBuilding = GC.getInfo(eBuilding);

	if (!bIgnoreCost && kBuilding.getProductionCost() == -1)
		return false;

	if (getCivTeamsEverAlive() < kBuilding.getNumTeamsPrereq())
		return false;
	{
		VictoryTypes ePrereqVict = kBuilding.getVictoryPrereq();
		if (ePrereqVict != NO_VICTORY && !isVictoryValid(ePrereqVict))
			return false;
	}
	{
		int iMaxStartEra = kBuilding.getMaxStartEra();
		if (iMaxStartEra != NO_ERA && getStartEra() > iMaxStartEra)
			return false;
	}
	if (isBuildingClassMaxedOut(kBuilding.getBuildingClassType()))
		return false;

	if (bTestVisible)
		return true;

	if (isNoNukes() && kBuilding.isAllowsNukes())
	{
		return false;
		// What the original code did:
		/*FOR_EACH_ENUM(Unit)
			if (GC.getInfo(eLoopUnit).isNuke())
				return false;*/
	}
	{
		SpecialBuildingTypes eSpecial = GC.getInfo(eBuilding).getSpecialBuildingType();
		if (eSpecial != NO_SPECIALBUILDING && !isSpecialBuildingValid(eSpecial))
			return false;
	}
	if (getNumCities() < GC.getInfo(eBuilding).getNumCitiesPrereq())
		return false;
	{
		CorporationTypes eFoundCorp = kBuilding.getFoundsCorporation();
		if (eFoundCorp != NO_CORPORATION && isCorporationFounded(eFoundCorp))
			return false;
	}
	return true;
}

// advc: Cut from CvPlayer::canTrain
bool CvGame::canTrain(UnitTypes eUnit, bool bIgnoreCost, bool bTestVisible) const
{
	CvUnitInfo const& kUnit = GC.getInfo(eUnit);

	if (!bIgnoreCost && kUnit.getProductionCost() == -1)
		return false;

	if (isOption(GAMEOPTION_NO_ESPIONAGE) &&
		(kUnit.isSpy() || kUnit.getEspionagePoints() > 0))
	{
		return false;
	}
	if (isUnitClassMaxedOut(kUnit.getUnitClassType()))
		return false;

	if (bTestVisible)
		return true;

	if ((isNoNukes() || !isNukesValid()) && kUnit.isNuke())
		return false;

	SpecialUnitTypes eSpecialUnit = kUnit.getSpecialUnitType();
	if (eSpecialUnit != NO_SPECIALUNIT && !isSpecialUnitValid(eSpecialUnit))
		return false;

	return true;
}


void CvGame::incrementUnitCreatedCount(UnitTypes eUnit)
{
	m_aiUnitCreatedCount.add(eUnit, 1);
}


bool CvGame::isUnitClassMaxedOut(UnitClassTypes eUnitClass, int iExtra) const
{
	CvUnitClassInfo const& kUnitClass = GC.getInfo(eUnitClass);
	if (!kUnitClass.isWorldUnit())
		return false;
	FAssertBounds(0, kUnitClass.getMaxGlobalInstances() + 1,
			getUnitClassCreatedCount(eUnitClass));
	return (getUnitClassCreatedCount(eUnitClass) + iExtra >=
			kUnitClass.getMaxGlobalInstances());
}


void CvGame::incrementUnitClassCreatedCount(UnitClassTypes eUnitClass)
{
	m_aiUnitClassCreatedCount.add(eUnitClass, 1);
}


bool CvGame::isBuildingClassMaxedOut(BuildingClassTypes eBuildingClass, int iExtra) const
{
	CvBuildingClassInfo const& kBuildingClass = GC.getInfo(eBuildingClass);
	if (!kBuildingClass.isWorldWonder())
		return false;
	FAssert(getBuildingClassCreatedCount(eBuildingClass) <=
			kBuildingClass.getMaxGlobalInstances());
	return (getBuildingClassCreatedCount(eBuildingClass) + iExtra >=
			kBuildingClass.getMaxGlobalInstances());
}


void CvGame::incrementBuildingClassCreatedCount(BuildingClassTypes eBuildingClass)
{
	m_aiBuildingClassCreatedCount.add(eBuildingClass, 1);
}


bool CvGame::isProjectMaxedOut(ProjectTypes eProject, int iExtra) const
{
	CvProjectInfo const& kProject = GC.getInfo(eProject);
	if (!kProject.isWorldProject())
		return false;
	FAssert(getProjectCreatedCount(eProject) <= kProject.getMaxGlobalInstances());
	return (getProjectCreatedCount(eProject) + iExtra >= kProject.getMaxGlobalInstances());
}


void CvGame::incrementProjectCreatedCount(ProjectTypes eProject, int iExtra)
{
	m_aiProjectCreatedCount.add(eProject, iExtra);
}


bool CvGame::isForceCivicOption(CivicOptionTypes eCivicOption) const
{
	FOR_EACH_ENUM(Civic)
	{
		if (GC.getInfo(eLoopCivic).getCivicOptionType() == eCivicOption)
		{
			if (isForceCivic(eLoopCivic))
				return true;
		}
	}
	return false;
}

/*	advc: Moved from CvGameCoreUtils; renamed from "getWorldSizeMaxConscript".
	(A few CvGame functions that call CvMap::getWorldSize should perhaps be
	moved to CvMap - or perhaps a new class CvWorld should be created so that
	CvMap can deal primarily with plot-related functions.) */
int CvGame::getMaxConscript(CivicTypes eCivic) const
{
	int iMaxConscript = GC.getInfo(eCivic).getMaxConscript();
	iMaxConscript *= std::max(0, GC.getInfo(GC.getMap().getWorldSize()).
			getMaxConscriptModifier() + 100);
	iMaxConscript /= 100;
	return iMaxConscript;
}


void CvGame::changeForceCivicCount(CivicTypes eCivic, int iChange)
{
	if (iChange == 0)
		return;
	bool const bOldForceCivic = isForceCivic(eCivic);
	m_aiForceCivicCount.add(eCivic, iChange);
	FAssert(getForceCivicCount(eCivic) >= 0);
	if (bOldForceCivic != isForceCivic(eCivic))
		verifyCivics();
}


bool CvGame::isVotePassed(VoteTypes eVote) const
{
	PlayerVoteTypes ePlayerVote = getVoteOutcome(eVote);
	if (isTeamVote(eVote))
		return (ePlayerVote >= 0 && ePlayerVote < MAX_CIV_TEAMS);
	return (ePlayerVote == PLAYER_VOTE_YES);
}


void CvGame::setVoteOutcome(VoteTriggeredData const& kData, PlayerVoteTypes eNewValue)
{
	VoteTypes eVote = kData.kVoteOption.eVote;
	FAssertEnumBounds(eVote);
	if (getVoteOutcome(eVote) != eNewValue)
	{
		bool bOldPassed = isVotePassed(eVote);
		m_aiVoteOutcome.set(eVote, eNewValue);
		if (bOldPassed != isVotePassed(eVote))
			processVote(kData, isVotePassed(eVote) ? 1 : -1);
	}
	for (PlayerIter<CIV_ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		itPlayer->setVote(kData.getID(), NO_PLAYER_VOTE);
	}
}


void CvGame::makeReligionFounded(ReligionTypes eReligion, PlayerTypes ePlayer)
{
	if (!isReligionFounded(eReligion))
	{
		m_aiReligionGameTurnFounded.set(eReligion, getGameTurn());
		FAssert(getReligionGameTurnFounded(eReligion) >= 0);
		CvEventReporter::getInstance().religionFounded(eReligion, ePlayer);
	}
}


void CvGame::setReligionSlotTaken(ReligionTypes eReligion, bool bTaken)
{
	// <advc.096> Update the tech-religion icons now shown on the tech tree
	if (bTaken && !isReligionSlotTaken(eReligion))
	{	/*	advc.001: This might be a minor bugfix -- tech-religion icons have
			always been used on the main interface. */
		gDLL->getInterfaceIFace()->setDirty(ResearchButtons_DIRTY_BIT, true);
		/*	Disabled this again - don't use tech-religion icons there.
			Not worth having to redraw the whole tech tree. */
		//gDLL->getInterfaceIFace()->setDirty(Tech_Screen_DIRTY_BIT, true);
	} // </advc.096>
	m_abReligionSlotTaken.set(eReligion, bTaken);
}


// doc
// TODO: update definition in header?
bool CvGame::isCorporationFounded(CorporationTypes eIndex)
{
    //return true; //Leoreth: corporations don't get founded anymore
    return (getCorporationGameTurnFounded(eIndex) != -1);
}


void CvGame::makeCorporationFounded(CorporationTypes eCorp, PlayerTypes ePlayer)
{
	if (!isCorporationFounded(eCorp))
	{
		FAssert(getGameTurn() >= 0);
		m_aiCorporationGameTurnFounded.set(eCorp, getGameTurn());
		CvEventReporter::getInstance().corporationFounded(eCorp, ePlayer);
	}
}


CvCity* CvGame::getHeadquarters(CorporationTypes eCorp) const
{
	CvPlot const* pPlot = GC.getMap().plotByIndex(m_aeHeadquarters.get(eCorp));
	return (pPlot == NULL ? NULL : pPlot->getPlotCity());
}


void CvGame::setVictoryValid(VictoryTypes eVictory, bool bValid)
{
	GC.getInitCore().setVictory(eVictory, bValid);
	AI().AI_updateVictoryWeights(); // advc.115f
}


void CvGame::makeSpecialUnitValid(SpecialUnitTypes eSpecialUnit)
{
	m_abSpecialUnitValid.set(eSpecialUnit, true);
}


void CvGame::makeSpecialBuildingValid(SpecialBuildingTypes eSpecialBuilding,
	bool bAnnounce)
{
	if (m_abSpecialBuildingValid.get(eSpecialBuilding))
		return;
	m_abSpecialBuildingValid.set(eSpecialBuilding, true);
	if (bAnnounce)
	{
		CvWString szBuffer = gDLL->getText("TXT_KEY_SPECIAL_BUILDING_VALID",
				GC.getInfo(eSpecialBuilding).getTextKeyWide());
		for (PlayerIter<MAJOR_CIV> itObs; itObs.hasNext(); ++itObs)
		{
			gDLL->UI().addMessage(itObs->getID(), false, -1, szBuffer,
					"AS2D_PROJECT_COMPLETED", MESSAGE_TYPE_MAJOR_EVENT, NULL,
					GC.getColorType("HIGHLIGHT_TEXT"));
		}
	}
}


void CvGame::makeNukesValid(bool bValid)
{
	m_bNukesValid = bValid;
}


bool CvGame::isInAdvancedStart() const
{
	FOR_EACH_ENUM(Player)
	{
		if ((GET_PLAYER(eLoopPlayer).getAdvancedStartPoints() >= 0) &&
			GET_PLAYER(eLoopPlayer).isHuman())
		{
			return true;
		}
	}
	return false;
}


void CvGame::setVoteChosen(int iSelection, int iVoteId)
{
	VoteSelectionData* pVoteSelectionData = getVoteSelection(iVoteId);
	if (pVoteSelectionData != NULL)
		addVoteTriggered(*pVoteSelectionData, iSelection);
	deleteVoteSelection(iVoteId);
}


CvCity* CvGame::getHolyCity(ReligionTypes eReligion) const
{
	CvPlot const* pPlot = GC.getMap().plotByIndex(m_aeHolyCity.get(eReligion));
	return (pPlot == NULL ? NULL : pPlot->getPlotCity());
}

// advc (note): Almost the same as setHeadquarters
void CvGame::setHolyCity(ReligionTypes eReligion, CvCity* pCity, bool bAnnounce)
{
	CvCity* pOldCity = getHolyCity(eReligion);
	if (pOldCity == pCity)
		return;
	// religion visibility now part of espionage
	//updateCitySight(false, true);
	m_aeHolyCity.set(eReligion, pCity == NULL ? NO_PLOT_NUM : pCity->plotNum());
	//updateCitySight(true, true);
	if (pOldCity != NULL)
	{
		pOldCity->changeReligionInfluence(eReligion,
				-GC.getDefineINT("HOLY_CITY_INFLUENCE"));
		pOldCity->updateReligionCommerce();
		pOldCity->setInfoDirty(true);
	}
	AI_makeAssignWorkDirty(); // advc: Moved up
	if (getHolyCity(eReligion) == NULL)
		return;

	CvCity* pHolyCity = getHolyCity(eReligion);
	//pHolyCity->setHasReligion(eReligion, true, bAnnounce, true);
	pHolyCity->spreadReligion(eReligion, false); // doc
    pHolyCity->changeReligionInfluence(eReligion, GC.getDefineINT("HOLY_CITY_INFLUENCE"));
	pHolyCity->updateReligionCommerce();
	pHolyCity->setInfoDirty(true);
	if (!bAnnounce || !isFinalInitialized() || gDLL->GetWorldBuilderMode())
		return;
	CvWString szMsgRevealed(gDLL->getText("TXT_KEY_MISC_REL_FOUNDED",
			GC.getInfo(eReligion).getTextKeyWide(), pHolyCity->getNameKey()));
	CvWString szMsgUnknown(gDLL->getText("TXT_KEY_MISC_REL_FOUNDED_UNKNOWN",
			GC.getInfo(eReligion).getTextKeyWide()));
	addReplayMessage(pHolyCity->getPlot(), REPLAY_MESSAGE_MAJOR_EVENT,
			pHolyCity->getOwner(), szMsgRevealed);
			// advc.106: Reserve this color for treaties
			//(ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"));
	for (PlayerIter<MAJOR_CIV> itObs; itObs.hasNext(); ++itObs)
	{
		bool bRevealed = (pHolyCity->isRevealed(itObs->getTeam()) ||
				itObs->isSpectator()); // advc.127
		gDLL->UI().addMessage(itObs->getID(), false,
				-1, // advc.106: was MESSAGE_TIME_LONG
				bRevealed ? szMsgRevealed : szMsgUnknown,
				GC.getInfo(eReligion).getSound(), MESSAGE_TYPE_MAJOR_EVENT,
				GC.getInfo(eReligion).getButton(),
				GC.getColorType("HIGHLIGHT_TEXT"),
				bRevealed ? pHolyCity->getX() : -1, bRevealed ? pHolyCity->getY() : -1,
				false, bRevealed);
	}
}

// advc (note): Almost the same as setHolyCity
void CvGame::setHeadquarters(CorporationTypes eCorp, CvCity* pCity, bool bAnnounce)
{
	CvCity* pOldCity = getHeadquarters(eCorp);
	if (pOldCity == pCity)
		return;
	m_aeHeadquarters.set(eCorp, pCity == NULL ? NO_PLOT_NUM : pCity->plotNum());
	if (pOldCity != NULL)
	{
		pOldCity->updateCorporation();
		pOldCity->setInfoDirty(true);
	}
	AI_makeAssignWorkDirty(); // advc: Moved up
	CvCity* pHeadquarters = getHeadquarters(eCorp);
	if (pHeadquarters == NULL)
		return;
	pHeadquarters->setHasCorporation(eCorp, true, bAnnounce);
	pHeadquarters->updateCorporation();
	pHeadquarters->setInfoDirty(true);
	if (!bAnnounce || !isFinalInitialized() || gDLL->GetWorldBuilderMode())
		return;
	CvWString szMsgRevealed(gDLL->getText("TXT_KEY_MISC_CORPORATION_FOUNDED",
			GC.getInfo(eCorp).getTextKeyWide(), pHeadquarters->getNameKey()));
	CvWString szMsgUnknown(gDLL->getText("TXT_KEY_MISC_CORPORATION_FOUNDED_UNKNOWN",
			GC.getInfo(eCorp).getTextKeyWide()));
	addReplayMessage(pHeadquarters->getPlot(), REPLAY_MESSAGE_MAJOR_EVENT,
			pHeadquarters->getOwner(), szMsgRevealed);
			// advc.106: Reserve this color for treaties
			//(ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"));
	for (PlayerIter<MAJOR_CIV> itObs; itObs.hasNext(); ++itObs)
	{
		bool bRevealed = (pHeadquarters->isRevealed(itObs->getTeam()) ||
				itObs->isSpectator()); // advc.127
		gDLL->UI().addMessage(itObs->getID(), false,
				-1, // advc.106: was MESASAGE_TIME_LONG
				bRevealed ? szMsgRevealed : szMsgUnknown,
				GC.getInfo(eCorp).getSound(), MESSAGE_TYPE_MAJOR_EVENT,
				GC.getInfo(eCorp).getButton(),
				GC.getColorType("HIGHLIGHT_TEXT"),
				bRevealed ? pHeadquarters->getX() : -1,
				bRevealed ? pHeadquarters->getY() : -1,
				false, bRevealed);
	}
}


PlayerVoteTypes CvGame::getPlayerVote(PlayerTypes eVoter, int iVote) const
{
	FAssertEnumBounds((CivPlayerTypes)eVoter);
	FAssert(getVoteTriggered(iVote) != NULL);
	return GET_PLAYER(eVoter).getVote(iVote);
}


void CvGame::setPlayerVote(PlayerTypes eVoter, int iVote, PlayerVoteTypes eNewValue)
{
	FAssertEnumBounds((CivPlayerTypes)eVoter);
	FAssert(getVoteTriggered(iVote) != NULL);
	GET_PLAYER(eVoter).setVote(iVote, eNewValue);
}


void CvGame::castVote(PlayerTypes eVoter, int iVote, PlayerVoteTypes ePlayerVote)
{
	VoteTriggeredData const* pTriggeredData = getVoteTriggered(iVote);
	if (pTriggeredData == NULL)
		return;
	TeamTypes const eVotingTeam = TEAMID(eVoter);
	CvVoteInfo const& kVote = GC.getInfo(pTriggeredData->kVoteOption.eVote);
	if (kVote.isAssignCity())
	{
		CvPlayerAI& kCityPlayer = GET_PLAYER(pTriggeredData->kVoteOption.ePlayer);
		if (eVotingTeam != kCityPlayer.getTeam())
		{
			switch (ePlayerVote)
			{
			/*	advc.130j (comment): Leave these alone for now. Should eventually
				be based on the number of votes cast. */
			case PLAYER_VOTE_YES:
				kCityPlayer.AI_changeMemoryCount(eVoter, MEMORY_VOTED_AGAINST_US, 1);
				break;
			case PLAYER_VOTE_NO:
				kCityPlayer.AI_changeMemoryCount(eVoter, MEMORY_VOTED_FOR_US, 1);
				break;
			}
		}
	}
	else if (isTeamVote(pTriggeredData->kVoteOption.eVote) &&
		ePlayerVote > NO_PLAYER_VOTE) // advc
	{
		TeamTypes const eTeamVotedFor = (TeamTypes)ePlayerVote;
		if (eVotingTeam != eTeamVotedFor)
		{
			for (MemberAIIter itMember(eTeamVotedFor); itMember.hasNext(); ++itMember)
			{
				/*	advc.130j (comment): Should not happen if there was
					only one name on the ballot. (Tbd.) */
				itMember->AI_changeMemoryCount(eVoter, MEMORY_VOTED_FOR_US, 1);
			}
		}
	}
	setPlayerVote(eVoter, iVote, ePlayerVote);
}


std::string CvGame::getScriptData() const
{
	return m_szScriptData;
}


void CvGame::setScriptData(std::string szNewValue)
{
	m_szScriptData = szNewValue;
}


CvWString const& CvGame::getName()
{
	return GC.getInitCore().getGameName();
}


void CvGame::setName(TCHAR const* szName)
{
	GC.getInitCore().setGameName(szName);
}


bool CvGame::isDestroyedCityName(CvWString& szName) const
{
	std::vector<CvWString>::const_iterator it;
	for (it = m_aszDestroyedCities.begin(); it != m_aszDestroyedCities.end(); ++it)
	{
		if (*it == szName)
			return true;
	}
	return false;
}


void CvGame::addDestroyedCityName(CvWString const& szName)
{
	m_aszDestroyedCities.push_back(szName);
}


bool CvGame::isGreatPersonBorn(CvWString& szName) const
{
	std::vector<CvWString>::const_iterator it;
	for (it = m_aszGreatPeopleBorn.begin(); it != m_aszGreatPeopleBorn.end(); ++it)
	{
		if (*it == szName)
			return true;
	}
	return false;
}


void CvGame::addGreatPersonBornName(CvWString const& szName)
{
	m_aszGreatPeopleBorn.push_back(szName);
}

// K-Mod note: I've made some unmarked style adjustments to this function.
void CvGame::doTurn()
{
	PROFILE_BEGIN("CvGame::doTurn()");

    // rfc
    for (PlayerIter it; it->hasNext(); ++it)
    {
        it->m_bTurnPlayed = false;
    }

	// END OF TURN
	if (!CvPlot::isAllFog()) // advc.706: Suppress popups
		CvEventReporter::getInstance().beginGameTurn(getGameTurn());

	doUpdateCacheOnTurn();
	updateScore();
	doDeals();

	/*for (iI = 0; iI < MAX_TEAMS; iI++) {
		if (GET_TEAM((TeamTypes)iI).isAlive())
			GET_TEAM((TeamTypes)iI).doTurn();
	}*/ // BtS
	/*	Disabled by K-Mod. CvTeam::doTurn is now called at the the same time
		as CvPlayer::doTurn, to fix certain turn-order imbalances. */

	GC.getMap().doTurn();

	getBarbarianWeightMap().getActivityMap().decay(); // advc.304
	// createBarbarianCities(); // rfc: disable
	createBarbarianUnits();

	doGlobalWarming();

    // rfc: disable
	// doHolyCity();
	// doHeadquarters();

	gDLL->getInterfaceIFace()->setEndTurnMessage(false);
	gDLL->getInterfaceIFace()->setHasMovedUnit(false);

	CvEventReporter::getInstance().endGameTurn(getGameTurn());

	if (getAIAutoPlay() > 0)
	{	/*	<advc.127> Flag added: don't change player status when decrementing
			the counter at the start of a round. Let onEndPlayerTurn in AIAutoPlay.py
			handle it. (Because human control should resume right before the human
			turn, which is not necessarily at the beginning of a round.) */
		changeAIAutoPlay(-1, false);
		if (getAIAutoPlay() > 0)
			checkInSync(); // May set AutoPlay counter to 0
		// </advc.127>
		if (getAIAutoPlay() == 0)
			reviveActivePlayer();
	}

	incrementGameTurn();
	incrementElapsedGameTurns();
	/*	advc.004: Already done in doDeals, but that's before incrementing the
		turn counter. Want to kill peace treaties asap. */
	verifyDeals();
	// <advc.700>
	if (isOption(GAMEOPTION_RISE_FALL))
		m_pRiseFall->atGameTurnStart(); // </advc.700>
	// advc.127: was right after doHeadquarters
	doDiploVote();

	if (isMPOption(MPOPTION_SIMULTANEOUS_TURNS))
	{
		int aiShuffle[MAX_PLAYERS];
		getSorenRand().shuffle(aiShuffle, MAX_PLAYERS);
		std::set<TeamTypes> activeTeams; // K-Mod
		for (int i = 0; i < MAX_PLAYERS; i++)
		{
			CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)aiShuffle[i]);
			if (kLoopPlayer.isAlive())
			{
				// K-Mod. call CvTeam::doTurn when the first player from each team is activated.
				if (activeTeams.insert(kLoopPlayer.getTeam()).second)
					GET_TEAM(kLoopPlayer.getTeam()).doTurn();
				// K-Mod end
				kLoopPlayer.setTurnActive(true);
			}
		}
	}
	else if (isSimultaneousTeamTurns())
	{
		for (int i = 0; i < MAX_TEAMS; i++)
		{
			CvTeam& kTeam = GET_TEAM((TeamTypes)i);
			if (kTeam.isAlive())
			{
				kTeam.setTurnActive(true);
				FAssert(getNumGameTurnActive() == kTeam.getAliveCount());
				/*	UNOFFICIAL_PATCH (bugfix), 06/10/10, snarko & jdog5000:
					Break only after first found alive player */
				break;
			}
		}
	}
	else
	{
		for (PlayerIter<ALIVE> it; it.hasNext(); ++it)
		{
			CvPlayer& kPlayer = *it;
			if (isPbem() && kPlayer.isHuman())
			{
				if (kPlayer.getID() == getActivePlayer())
				{
					// Nobody else left alive
					GC.getInitCore().setType(GAME_HOTSEAT_NEW);
					kPlayer.setTurnActive(true);
				}
				else if (!getPbemTurnSent())
					gDLL->sendPbemTurn(kPlayer.getID());
			}
			else
			{
				kPlayer.setTurnActive(true);
				FAssert(getNumGameTurnActive() == 1);
			}
			break;
		}
	}

	testVictory();

	gDLL->getEngineIFace()->SetDirty(GlobePartialTexture_DIRTY_BIT, true);
	gDLL->getEngineIFace()->DoTurn();

	PROFILE_END();

	stopProfilingDLL(true);

    // doc (edead): disable autosave during autoplay
    // TODO: refactor
    if (GC.getDefineINT("NO_AUTOSAVE_DURING_AUTOPLAY") == 0 || (getGameTurn() > 0 && getAIAutoPlay() == 0))
	{
	    // <advc.044>
	    if (isMPOption(MPOPTION_SIMULTANEOUS_TURNS) || isHotSeat())
		    autoSave();
	    else
	    {
		    CvPlayer const& kActivePlayer = GET_PLAYER(getActivePlayer());
		    if (!kActivePlayer.isAlive())
		    {
			    FAssert(kActivePlayer.isHumanDisabled());
			    autoSave();
		    }
	    } // (Otherwise, autosave in CvPlayer::setTurnActive.)
    }
	// </advc.044>

    // doc: initial autosave
    if (getGameTurn() > 0 && GET_PLAYER(getActivePlayer()).getInitialBirthTurn() == getGameTurn())
    {
        autoSave(true);
    }
}

// advc.106b:
void CvGame::setInBetweenTurns(bool b)
{
	m_bInBetweenTurns = b;
}


void CvGame::doDeals()
{
	verifyDeals();

	FOR_EACH_DEAL_VAR(pLoopDeal)
	{
		pLoopDeal->doTurn();
	}
	/*	advc.130p: K-Mod had only done this update for players involved in any deals
		(through an std::set), but third parties might disapprove of the deal.
		(I think this was a minor oversight in K-Mod - but matters more in AdvCiv
		b/c of changes to trade values of annual deals.) */
	CvPlayerAI::AI_updateAttitudes();
}

// advc.055: For doGlobalWarming (needs to have external linkage)
namespace
{
	struct PreGWPlot
	{
		PreGWPlot(CvPlot const* pPlot, // No reference b/c need copy-ctor
			TerrainTypes eTerrain, FeatureTypes eFeature, ImprovementTypes eImprovement)
		:	pPlot(pPlot),
			eTerrain(eTerrain), eFeature(eFeature), eImprovement(eImprovement)
		{}
		CvPlot const* pPlot;
		TerrainTypes eTerrain;
		FeatureTypes eFeature;
		ImprovementTypes eImprovement;
	};
}

/*	K-Mod, 5/dec/10, karadoc
	complete rewrite of global warming, using some features from 'GWMod' by M.A. */
void CvGame::doGlobalWarming()
{
	PROFILE_FUNC();

	// Calculate change in GW index
	int iGlobalWarmingValue = calculateGlobalPollution();
	int iGlobalWarmingDefense = calculateGwSustainabilityThreshold(); // Natural global defence
	iGlobalWarmingDefense += calculateGwLandDefence(); // defence from features (forests & jungles)
	changeGlobalWarmingIndex(iGlobalWarmingValue - iGlobalWarmingDefense);

	// check if GW has 'activated'.
	if (getGwEventTally() < 0 && getGlobalWarmingIndex() > 0)
	{
		setGwEventTally(0);

		// Send a message saying that the threshold has been passed
		CvWString szBuffer;

		szBuffer = gDLL->getText("TXT_KEY_MISC_GLOBAL_WARMING_ACTIVE");
		// add the message to the replay
		addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, NO_PLAYER, szBuffer,
				GC.getColorType("HIGHLIGHT_TEXT"));

		for (PlayerIter<MAJOR_CIV> itObs; itObs.hasNext(); ++itObs)
		{
			gDLL->UI().addMessage(itObs->getID(), false, -1, szBuffer,
					"AS2D_GLOBALWARMING", MESSAGE_TYPE_MAJOR_EVENT, NULL,
					GC.getColorType("HIGHLIGHT_TEXT"));
			// Tell human players that the threshold has been reached
			if (itObs->isHuman() && !isNetworkMultiPlayer())
			{
				CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_TEXT);
				if (pInfo != NULL)
				{
					pInfo->setText(gDLL->getText("TXT_KEY_POPUP_ENVIRONMENTAL_ADVISOR"));
					gDLL->getInterfaceIFace()->addPopup(pInfo, itObs->getID());
				}
			}
		}

	}

	int iGlobalWarmingRolls = getGlobalWarmingChances();

	// Apply the effects of GW

	// advc.opt: Can't hurt to make these static
	static TerrainTypes const eWarmingTerrain = (TerrainTypes)GC.getDefineINT("GLOBAL_WARMING_TERRAIN");
	static TerrainTypes const eFrozenTerrain = (TerrainTypes)GC.getDefineINT("FROZEN_TERRAIN");
	static TerrainTypes const eColdTerrain = (TerrainTypes)GC.getDefineINT("COLD_TERRAIN");
	static TerrainTypes const eTemperateTerrain = (TerrainTypes)GC.getDefineINT("TEMPERATE_TERRAIN");
	static TerrainTypes const eDryTerrain = (TerrainTypes)GC.getDefineINT("DRY_TERRAIN");
	static TerrainTypes const eBarrenTerrain = (TerrainTypes)GC.getDefineINT("BARREN_TERRAIN");

	static FeatureTypes const eColdFeature = (FeatureTypes)GC.getDefineINT("COLD_FEATURE");
	static FeatureTypes const eTemperateFeature = (FeatureTypes)GC.getDefineINT("TEMPERATE_FEATURE");
	static FeatureTypes const eWarmFeature = (FeatureTypes)GC.getDefineINT("WARM_FEATURE");
	static FeatureTypes const eFalloutFeature = (FeatureTypes)GC.getDefineINT("NUKE_FEATURE");
	// advc.055:
	static bool const bPROTECT_FEATURE_ON_NON_DRY_TERRAIN = GC.getDefineBOOL("PROTECT_FEATURE_ON_NON_DRY_TERRAIN");

	// advc.055:
	std::vector<PreGWPlot> aChangedPlots;
	bool bSoundPlayed = false; // advc.002l
	for (int i = 0; i < iGlobalWarmingRolls; i++)
	{
		// note, warming prob out of 1000, not percent.
		int iLeftOdds = 10 * getSpeedPercent();
		if (SyncRandNum(iLeftOdds) >= GC.getDefineINT("GLOBAL_WARMING_PROB"))
			continue;
		//CvPlot* pPlot = GC.getMap().syncRandPlot(RANDPLOT_LAND | RANDPLOT_NOT_CITY);
		/*	Global warming is no longer completely random.
			getRandGWPlot will get a weighted random plot for us to strike. */
		// advc.055: Arg was 3. The higher the value, the greater the preference for cold terrain.
		CvPlot* pPlot = getRandGWPlot(2);
		if (pPlot == NULL)
			continue;
		// <advc.055>
		TerrainTypes const eTerrain = pPlot->getTerrainType();
		FeatureTypes const eFeature = pPlot->getFeatureType();
		ImprovementTypes const eImprov = pPlot->getImprovementType();
		// Just for the announcements
		PreGWPlot preGWPlot(pPlot, eTerrain, eFeature, eImprov);
		bool bProtectFeature = false;
		CvFeatureInfo const* pProtectedFeature = NULL;
		if (eImprov != NO_IMPROVEMENT && eFeature != NO_FEATURE)
		{
			if (SyncRandSuccess100(GC.getInfo(eImprov).get(
				CvImprovementInfo::GWFeatureProtection)))
			{
				bProtectFeature = true;
				pProtectedFeature = &GC.getInfo(eFeature);
			}
		} // </advc.055>
		bool bChanged = false;
		// rewritten terrain changing code:
		// 1) Melt frozen terrain
		if (eFeature == eColdFeature /* advc.055: */ && !bProtectFeature)
		{
			pPlot->setFeatureType(NO_FEATURE);
			bChanged = true;
		}
		else if (eTerrain == eFrozenTerrain &&
			(!bProtectFeature || pProtectedFeature->isTerrain(eColdTerrain))) // advc.055
		{
			pPlot->setTerrainType(eColdTerrain);
			bChanged = true;
		}
		else if (eTerrain == eColdTerrain &&
			(!bProtectFeature || pProtectedFeature->isTerrain(eDryTerrain))) // advc.055
		{
			pPlot->setTerrainType(eDryTerrain); // advc.055: was eTemperateTerrain
			bChanged = true;
		}
		// 2) Forest -> Jungle
		// advc.055: Commented out
		/*else if (eFeature == eTemperateFeature) {
			pPlot->setFeatureType(eWarmFeature);
			bChanged = true;
		}*/
		// 3) Remove other features
		else if (eFeature != NO_FEATURE && eFeature != eFalloutFeature &&
			/* <advc.055> */ !bProtectFeature &&
			(!bPROTECT_FEATURE_ON_NON_DRY_TERRAIN ||
			(eFeature != eTemperateFeature && eFeature != eWarmFeature) ||
			eTerrain == eDryTerrain)) // </advc.055>
		{
			pPlot->setFeatureType(NO_FEATURE);
			bChanged = true;
		}
		// 4) Dry the terrain
		else if (eTerrain == eTemperateTerrain &&
			(!bProtectFeature || pProtectedFeature->isTerrain(eDryTerrain))) // advc.055
		{
			pPlot->setTerrainType(eDryTerrain);
			bChanged = true;
		}
		else if (eTerrain == eDryTerrain &&
			(!bProtectFeature || pProtectedFeature->isTerrain(eBarrenTerrain))) // advc.055
		{	// <advc.055> Don't desertify (very) cold dry terrain
			int iColdScore = 0;
			FOR_EACH_ADJ_PLOT(*pPlot)
			{
				int iLoopColdScore = 0;
				if (pAdj->getTerrainType() == eFrozenTerrain ||
					pAdj->getFeatureType() == eColdFeature)
				{
					iLoopColdScore += 2;
				}
				else if (pAdj->getTerrainType() == eColdTerrain)
					iLoopColdScore++;
				if (plotDistance(pPlot, pAdj) <= 1)
					iLoopColdScore *= 2;
				iColdScore += iLoopColdScore;
			}
			if (iColdScore < 3) // </advc.055>
			{
				pPlot->setTerrainType(eBarrenTerrain);
				bChanged = true;
			}
		}
		/* 5) Sink coastal desert (disabled)
		else if (eTerrain == eBarrenTerrain) {
			if (isOption(GAMEOPTION_RISING_SEAS)) {
				if (pPlot->isCoastalLand()) {
					if (!pPlot->isHills() && !pPlot->isPeak()) {
						pPlot->forceBumpUnits();
						pPlot->setPlotType(PLOT_OCEAN);
						bChanged = true;
		} } } }*/
		if (bChanged)
		{
			// only destroy the improvement if the new terrain cannot support it
			if (!pPlot->canHaveImprovement(eImprov, NO_TEAM, false,
				NO_BUILD, false)) // kekm.9
			{
				pPlot->setImprovementType(NO_IMPROVEMENT, /* advc.055: */ true);
			}  // <advc.055>
			if (!pPlot->canHaveFeature(eFeature, true))
			{
				pPlot->setFeatureType(NO_FEATURE);
				FAssert(!bProtectFeature);
			}
			aChangedPlots.push_back(preGWPlot);
			// Do the announcements in a separate loop
			// </advc.055>
			changeGwEventTally(1);
		}
	}
	updateGwPercentAnger();
	if (getGlobalWarmingIndex() > 0)
	{
		changeGlobalWarmingIndex(-getGlobalWarmingIndex() *
				GC.getDefineINT("GLOBAL_WARMING_RESTORATION_RATE", 0)/100);
	}
	// <advc.055>
	/*	advc.706 (note): These will be shortlived INFO-type messages,
		no need to store those at AI players. */
	for (PlayerIter<HUMAN> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		std::vector<std::pair<CvCity const*,PreGWPlot> >
				aAffectedTeamCities, aAffectedRivalCities;
		int iMelted = 0;
		for (size_t i = 0; i < aChangedPlots.size(); i++)
		{
			CvPlot const& kPlot = *aChangedPlots[i].pPlot;
			if (!kPlot.isRevealed(itPlayer->getTeam()))
				continue;
			CvCity const* pCity = GC.getMap().findCity(kPlot.getX(), kPlot.getY(),
					NO_PLAYER, NO_TEAM, false); // (as in K-Mod)
			{
				bool bNearCity = (pCity != NULL &&
						(kPlot.getRevealedOwner(itPlayer->getTeam()) != NO_PLAYER ||
						plotDistance(&kPlot, pCity->plot()) <= CITY_PLOTS_RADIUS + 1));
				if (!bNearCity && aChangedPlots[i].eFeature == eColdFeature &&
					//aChangedPlots[i].eTerrain == GC.getWATER_TERRAIN(false)
					// Better for maps that might have Antarctica as a landmass
					kPlot.isWater())
				{
					iMelted++;
					continue;
				}
			}
			if (pCity == NULL) // Can't describe the affected tile w/o a city
			{
				FAssert(itPlayer->getNumCities() == 0);
				continue;
			}
			(pCity->getTeam() == itPlayer->getTeam() ?
					aAffectedTeamCities : aAffectedRivalCities).push_back(
					std::make_pair(pCity, aChangedPlots[i]));
		}
		int const iMaxRivalCityAnnouncements = 1;
		for (int iPass = 0; iPass < 2; iPass++)
		{
			bool const bTeamCities = (iPass == 0);
			std::vector<std::pair<CvCity const*,PreGWPlot> >&
					kAffectedCities = (bTeamCities ?
					aAffectedTeamCities : aAffectedRivalCities);
			if (!bTeamCities && kAffectedCities.size() > iMaxRivalCityAnnouncements)
				continue;
			for (size_t i = 0; i < kAffectedCities.size(); i++)
			{
				CvPlot const& kPlot = *kAffectedCities[i].second.pPlot;
				CvCity const& kCity = *kAffectedCities[i].first;
				TerrainTypes const eOldTerrain = kAffectedCities[i].second.eTerrain;
				FeatureTypes const eOldFeature = kAffectedCities[i].second.eFeature;
				ImprovementTypes const eOldImprov = kAffectedCities[i].second.eImprovement;
				CvWString szBuffer = gDLL->getText(
						bTeamCities ?
						"TXT_KEY_MISC_GLOBAL_WARMING_NEAR_YOUR_CITY" :
						"TXT_KEY_MISC_GLOBAL_WARMING_NEAR_CITY",
						kCity.getNameKey());
				std::vector<CvWString> aszGWEffects;
				if (eOldTerrain != kPlot.getTerrainType())
				{
					aszGWEffects.push_back(gDLL->getText(
							"TXT_KEY_GW_TERRAIN_OR_FEATURE_CHANGED",
							GC.getInfo(eOldTerrain).getDescription(),
							GC.getInfo(kPlot.getTerrainType()).getDescription()));
				}
				FeatureTypes const eNewFeature = kPlot.getFeatureType();
				if (eOldFeature != eNewFeature)
				{
					if (eOldFeature != NO_FEATURE && eNewFeature != NO_FEATURE)
					{
						aszGWEffects.push_back(gDLL->getText(
								"TXT_KEY_GW_TERRAIN_OR_FEATURE_CHANGED",
								GC.getInfo(eOldFeature).getDescription(),
								GC.getInfo(eNewFeature).getDescription()));
					}
					else if (eNewFeature == NO_FEATURE)
					{
						aszGWEffects.push_back(gDLL->getText(
								"TXT_KEY_GW_DESTROYED",
								GC.getInfo(eOldFeature).getDescription()));
					}
					else // Can't currently happen
					{
						aszGWEffects.push_back(gDLL->getText(
								"TXT_KEY_GW_CREATED",
								GC.getInfo(eNewFeature).getDescription()));
					}
				}
				/*	Fog of war is currently not a concern because improvements
					only get destroyed when the new terrain type (not subject to
					fog of war) mandates it. */
				ImprovementTypes const eNewImprov = kPlot.getImprovementType();
				if (eOldImprov != eNewImprov && eNewImprov == NO_IMPROVEMENT)
				{
					aszGWEffects.push_back(gDLL->getText(
							"TXT_KEY_GW_DESTROYED",
							GC.getInfo(eOldImprov).getDescription()));
				}
				bool bFirst = true;
				for (size_t j = 0; j < aszGWEffects.size(); j++)
				{
					setListHelp(szBuffer, L" (", aszGWEffects[j].c_str(), L", ", bFirst);
				}
				if (!bFirst)
					szBuffer.append(L")");
				bool bPlaySound = (!bSoundPlayed && // advc.002l
						bTeamCities);
				gDLL->UI().addMessage(itPlayer->getID(),
						false, -1, szBuffer, kPlot, // (as in K-Mod)
						bPlaySound ? NULL : // advc.002l
						"AS2D_SQUISH");
				bSoundPlayed = bPlaySound; // advc.002l: Once is enough
			}
		}
		// Too many events near rival cities to announce them separately
		if (aAffectedRivalCities.size() > iMaxRivalCityAnnouncements)
		{
			CvWString szBuffer = gDLL->getText(
					"TXT_KEY_MISC_GLOBAL_WARMING_NEAR_CITIES");
			bool bFirst = true;
			for (size_t i = 0; i < aAffectedRivalCities.size(); i++)
			{
				setListHelp(szBuffer, L" ", aAffectedRivalCities[i].first->getName(),
						L", ", bFirst);
				bFirst = false;
			}
			if (!bFirst)
				szBuffer.append(L".");
			gDLL->UI().addMessage(itPlayer->getID(), false, -1, szBuffer);
		}
		if (iMelted > 0)
		{
			CvWString szBuffer = gDLL->getText(
					"TXT_KEY_GW_MELTED",
					GC.getInfo(eColdFeature).getDescription(),
					iMelted,
					/*	It might be shallow water - but probably isn't,
						and calling it deep gets across that it's far away. */
					GC.getInfo(GC.getWATER_TERRAIN(false)).getDescription());
			gDLL->UI().addMessage(itPlayer->getID(), false, -1, szBuffer);
		}
	} // </advc.055>
}

// Choose the best plot for global warming to strike from a set of iPool random plots
CvPlot* CvGame::getRandGWPlot(int iPool)
{	// advc.opt: Can't hurt to make these static
	static const TerrainTypes eFrozenTerrain = (TerrainTypes)GC.getDefineINT("FROZEN_TERRAIN");
	static const TerrainTypes eColdTerrain = (TerrainTypes)GC.getDefineINT("COLD_TERRAIN");
	static const TerrainTypes eTemperateTerrain = (TerrainTypes)GC.getDefineINT("TEMPERATE_TERRAIN");
	static const TerrainTypes eDryTerrain = (TerrainTypes)GC.getDefineINT("DRY_TERRAIN");
	static const FeatureTypes eColdFeature = (FeatureTypes)GC.getDefineINT("COLD_FEATURE");

	/*	Currently we just choose the coldest tile;
		but I may include other tests in future versions. */
	CvPlot* pBestPlot = NULL;
	TerrainTypes eTerrain = NO_TERRAIN;
	int iBestScore = -1; // higher score means better target plot
	for (int i = 0; i < iPool; i++)
	{
		/*	I want to be able to select a water tile with ice on it;
			so I can't just exclude water completely... */
		//CvPlot* pTestPlot = GC.getMap().syncRandPlot(RANDPLOT_LAND | RANDPLOT_NOT_CITY);
		/*	advc (comment): Should arguably just create a new flag RANDPLOT_GLOBAL_WARMING
			and let syncRandPlot handle the randomized selection. */
		CvPlot* pTestPlot = NULL;
		/*	advc: Was < 100. If we want to be certain not to miss, then we should
			check the whole map. But a 1% failure chance is fine with me. */
		for (int j = 0; j < 25; j++)
		{
			pTestPlot = GC.getMap().syncRandPlot(RANDPLOT_NOT_CITY,
					/*	advc: iTimeout was 100 - don't need to draw that many cities
						to conclude that sth. is wrong. */
					NULL, -1, 20);
			if (pTestPlot == NULL)
			{
				FAssert(pTestPlot != NULL); // advc
				break; // give up
			}
			// check for ice
			if (pTestPlot->getFeatureType() == eColdFeature)
			{
				// pretend it's frozen terrain
				eTerrain = eFrozenTerrain;
				break;
			}
			// check for ordinary land plots
			if (!pTestPlot->isWater() && !pTestPlot->isPeak())
			{
				eTerrain = pTestPlot->getTerrainType();
				break;
			}
			// not a suitable plot, try again.
		}
		// advc: 2nd test unnecessary as I'm resetting pTestPlot in the outer loop
		if (pTestPlot == NULL/* || j == 100*/)
			continue;

		/*	if only I could do this with a switch...
			[advc: one cannot b/c the case labels need to be constant expressions] */
		int iTestScore = 0;
		if (eTerrain == eFrozenTerrain)
			iTestScore = 4;
		else if (eTerrain == eColdTerrain)
			iTestScore = 3;
		else if (eTerrain == eTemperateTerrain)
			iTestScore = 2;
		else if (eTerrain == eDryTerrain)
			iTestScore = 1;
		if (iTestScore > iBestScore)
		{
			if (iBestScore > 0 || iTestScore >= 3)
				return pTestPlot; // lets not target the ice too much...

			pBestPlot = pTestPlot;
			iBestScore = iTestScore;
		}
	}
	return pBestPlot;
} // K-Mod end


void CvGame::doHolyCity()
{
	if (GC.getPythonCaller()->doHolyCity())
		return;
	if (getElapsedGameTurns() < 5 && !isOption(GAMEOPTION_ADVANCED_START))
		return;

	int iRandOffset = SyncRandNum(GC.getNumReligionInfos());
	for (int iLoop = 0; iLoop < GC.getNumReligionInfos(); ++iLoop)
	{
		ReligionTypes eReligion = (ReligionTypes)(
				(iLoop + iRandOffset) % GC.getNumReligionInfos());
		if (isReligionSlotTaken(eReligion))
			continue;
		TeamTypes eBestTeam = NO_TEAM;
		{
			int iBestValue = MAX_INT;
			/*	advc.001: Was MAX_TEAMS. Make sure Barbarians don't get a religion
				here somehow. Inspired by Mongoose SDK ReligionMod. Though they can
				still get one through CvPlayer::doResearch and CvTeam::setHasTech. */
			for (TeamIter<CIV_ALIVE> itTeam; itTeam.hasNext(); ++itTeam)
			{
				if (!itTeam->isHasTech(GC.getInfo(eReligion).getTechPrereq()) ||
					itTeam->getNumCities() <= 0)
				{
					continue;
				}

				int iValue = SyncRandNum(10);
				FOR_EACH_ENUM(Religion)
				{
					int iReligionCount = itTeam->getHasReligionCount(eLoopReligion);
					if (iReligionCount > 0)
						iValue += iReligionCount * 20;
				}
				iValue -= religionPriority(itTeam->getID(), eReligion); // advc.138
				if (iValue < iBestValue)
				{
					iBestValue = iValue;
					eBestTeam = itTeam->getID();
				}
			}
		}
		if (eBestTeam == NO_TEAM)
			continue;

		int iBestValue = MAX_INT;
		PlayerTypes eBestPlayer = NO_PLAYER;
		for (MemberIter itMember(eBestTeam); itMember.hasNext(); ++itMember)
		{
			if (itMember->getNumCities() <= 0)
				continue;

			int iValue = SyncRandNum(10);
			if (!itMember->isHuman())
				iValue += 18; // advc.138: Was 10. Need some x: 15 < x < 20.
			FOR_EACH_ENUM(Religion)
			{
				int iReligionCount = itMember->getHasReligionCount(eLoopReligion);
				if (iReligionCount > 0)
					iValue += iReligionCount * 20;
			}
			iValue -= religionPriority(itMember->getID(), eReligion); // advc.138
			if (iValue < iBestValue)
			{
				iBestValue = iValue;
				eBestPlayer = itMember->getID();
			}
		}
		if (eBestPlayer == NO_PLAYER)
			continue;

		ReligionTypes eFoundReligion = eReligion;
		if (isOption(GAMEOPTION_PICK_RELIGION))
			eFoundReligion = GET_PLAYER(eBestPlayer).AI_chooseReligion();
		if (eFoundReligion != NO_RELIGION)
			GET_PLAYER(eBestPlayer).foundReligion(eFoundReligion, eReligion, false);
	}
}

// <advc.138>
int CvGame::religionPriority(TeamTypes eTeam, ReligionTypes eReligion) const {

	int iR = 0;
	MemberIter itMember(eTeam);
	for (; itMember.hasNext(); ++itMember)
	{
		iR += religionPriority(itMember->getID(), eReligion);
	}
	int iMembers = itMember.nextIndex();
	if (iMembers <= 0)
		return 0;
	return iR / iMembers;
}


int CvGame::religionPriority(PlayerTypes ePlayer, ReligionTypes eReligion) const
{
	int iR = 0;
	CvPlayer const& kPlayer = GET_PLAYER(ePlayer);
	FOR_EACH_ENUM2(Trait, eNoAnarchyTrait)
	{
		if (!kPlayer.hasTrait(eNoAnarchyTrait) ||
			GC.getInfo(eNoAnarchyTrait).getMaxAnarchy() != 0)
		{
			continue;
		}
		iR += 5;
		/*	Spiritual human should be sure to get a religion (so long as
			difficulty isn't above Noble). Not quite sure if my choice of
			numbers in this function and in doHolyCity accomplishes that. */
		if (kPlayer.isHuman())
			iR += 6;
		break;
	}
	iR += ((100 - GC.getInfo(kPlayer.getHandicapType()).
			getStartingLocationPercent()) * 31) / 100;
	// With the pick-rel option, eReligion will change later on anyway.
	if (!isOption(GAMEOPTION_PICK_RELIGION))
	{
		/*	Not excluding human here means that choosing a leader with an early
			fav religion can make a difference in human getting a religion.
			Unexpected, as fav. religions are pretty obscure knowledge. On the
			other hand, it's a pity to assign human an arbitrary religion when
			e.g. Buddhism would fit so well for Ashoka.
			Don't use PersonalityType here; fav. religion is always a matter
			of LeaderType. */
		if (kPlayer.getFavoriteReligion() == eReligion)
			iR += 6;
	}
	return iR;
} // </advc.138>

/*	advc: Since none of the BtS corps have a prereq. tech, this function
	normally does nothing. It has clearly never been properly tested (I've found
	two errors while refactoring it). I'm tempted to remove it, but corporations
	that get founded through a tech could be interesting for XML modding. It remains
	mostly untested though, and shares some (duplicate) code with doHlyCity. */
void CvGame::doHeadquarters()
{
	// advc.003y: Call to nonexistent Python function "doHeadquarters" removed

	if (getElapsedGameTurns() < 5)
		return;

	FOR_EACH_ENUM2(Corporation, eCorp)
	{
		CvCorporationInfo& kCorp = GC.getInfo(eCorp);
		if (isCorporationFounded(eCorp))
			continue;

		TeamTypes eBestTeam = NO_TEAM;
		{
			int iBestValue = MAX_INT;
			for (TeamIter<CIV_ALIVE> itTeam; itTeam.hasNext(); ++itTeam)
			{
				// advc (note): This is as far as execution gets in AdvCiv/BtS
				if (kCorp.getTechPrereq() == NO_TECH ||
					!itTeam->isHasTech(kCorp.getTechPrereq()))
				{
					continue;
				}
				if (itTeam->getNumCities() <= 0)
					continue;
				bool bHasBonus = false;
				for (int i = 0; i < kCorp.getNumPrereqBonuses(); i++)
				{
					if (itTeam->hasBonus(kCorp.getPrereqBonus(i)))
					{
						bHasBonus = true;
						break;
					}
				}
				if (!bHasBonus)
					continue;
				int iValue = SyncRandNum(10);
				FOR_EACH_ENUM(Corporation)
				{
					int iCorporationCount = //GET_PLAYER((PlayerTypes)iJ).getHasCorporationCount((CorporationTypes)iK);
							// advc.001: iJ isn't a player
							itTeam->getHasCorporationCount(eLoopCorporation);
					iValue += iCorporationCount * 20;
				}
				if (iValue < iBestValue)
				{
					iBestValue = iValue;
					eBestTeam = itTeam->getID();
				}
			} // advc.001: Team loop needs to end here
		}
		if (eBestTeam == NO_TEAM)
			continue;
		int iBestValue = MAX_INT;
		PlayerTypes eBestPlayer = NO_PLAYER;
		for (MemberIter itMember(eBestTeam); itMember.hasNext(); ++itMember)
		{
			if (itMember->getNumCities() <= 0)
				continue;
			bool bHasBonus = false;
			for (int i = 0; i < kCorp.getNumPrereqBonuses(); i++)
			{
				if (itMember->hasBonus(kCorp.getPrereqBonus(i)))
				{
					bHasBonus = true;
					break;
				}
			}
			if (!bHasBonus)
				continue;
			int iValue = SyncRandNum(10);
			if (!itMember->isHuman())
				iValue += 10;
			FOR_EACH_ENUM(Corporation)
			{
				int iCorporationCount = itMember->getHasCorporationCount(eLoopCorporation);
				if (iCorporationCount > 0)
					iValue += iCorporationCount * 20;
			}
			if (iValue < iBestValue)
			{
				iBestValue = iValue;
				eBestPlayer = itMember->getID();
			}
		}
		if (eBestPlayer != NO_PLAYER)
			GET_PLAYER(eBestPlayer).foundCorporation(eCorp);
	}
}


void CvGame::doDiploVote()
{
	doVoteResults();
	doVoteSelection();
}


void CvGame::createBarbarianCities()
{
	if (getMaxCityElimination() > 0)
		return;

	if (isOption(GAMEOPTION_NO_BARBARIANS))
		return;

	if (GC.getPythonCaller()->createBarbarianCities())
		return;

	if (GC.getInfo(getCurrentEra()).isNoBarbCities())
		return;

	CvHandicapInfo const& kGameHandicap = GC.getInfo(getHandicapType());
	if (kGameHandicap.getUnownedTilesPerBarbarianCity() <= 0)
		return;

	if (getNumCivCities() < countCivPlayersAlive() * 2)
			return;

	if (getElapsedGameTurns() * (getStartEra() + 1) * 100 <=
		kGameHandicap.getBarbarianCityCreationTurnsElapsed() *
		GC.getInfo(getGameSpeedType()).getBarbPercent())
	{
		return;
	}
	/*	<advc.300> Create up to two cities per turn, though at most one in an
		area settled by a civ. Moved the rest of createBarbarianCities (plural)
		into new function createBarbarianCity (singular). */
	createBarbarianCity(false);
	// A second city at full probability is too much; try 50%.
	createBarbarianCity(true, 50);
}


void CvGame::createBarbarianCity(bool bSkipCivAreas, int iProbModifierPercent)
{
	int const iEra = getCurrentEra();
	scaled rCreationProb = per100(GC.getInfo(getHandicapType()).
			/*	No cities past Medieval, so it's either +0 points (Ancient),
				+1 (Classical) or +4 (Medieval). */
			getBarbarianCityCreationProb() + SQR(iEra));
	rCreationProb *= per100(iProbModifierPercent);
	// Adjust creation prob to game speed
	CvGameSpeedInfo const& kSpeed = GC.getInfo(getGameSpeedType());
	rCreationProb *= per100(kSpeed.getBarbPercent());
	if (!SyncRandSuccess(rCreationProb)) // </advc.300>
		return;

	/*	advc (comment): This multiplier expresses how close the total number of
		Barbarian cities is to the global target. In contrast, iTargetCities
		in the loop is per area, not global.
		It's apparently a kind of percentage. If above 100, i.e. 100+x, it seems
		to mean that x% more barb cities are needed.
		The global target is between 20% and 40% of the number of civ cities,
		which is pretty ambitious. */
	int iTargetCitiesMultiplier = 100;
	{
		int iTargetBarbCities = (getNumCivCities() * 5 *
				GC.getInfo(getHandicapType()).getBarbarianCityCreationProb()) / 100;
		int iBarbCities = GET_PLAYER(BARBARIAN_PLAYER).getNumCities();
		if (iBarbCities < iTargetBarbCities)
		{
			iTargetCitiesMultiplier += (300 * (iTargetBarbCities - iBarbCities)) /
					iTargetBarbCities;
		}
		if (isOption(GAMEOPTION_RAGING_BARBARIANS))
		{
			iTargetCitiesMultiplier *= 3;
			iTargetCitiesMultiplier /= 2;
		}
	}

	CitySiteEvaluator citySiteEval(GET_PLAYER(BARBARIAN_PLAYER),
			GC.getDefineINT("MIN_BARBARIAN_CITY_STARTING_DISTANCE"));
	/*	<advc.300> Randomize penalty on short inter-city distance for more variety
		in Barbarian settling patterns. Was 8 in K-Mod. */
	citySiteEval.discourageBarbarians(5 + SyncRandNum(7));
	CvMap const& kMap = GC.getMap();
	std::map<int,int> perAreaUnowned; // Precomputed for efficiency
	FOR_EACH_AREA(pArea)
	{
		/*	Plots owned by Barbarians are counted in BtS, and I count them when
			creating units because it makes some sense that Barbarians get fewer free
			units once they have cities, but for cities, I'm not sure.
			Keep counting them for now. */
		std::pair<int,int> iiOwnedUnowned = pArea->countOwnedUnownedHabitableTiles();
				//a.countOwnedUnownedHabitableTiles(true);
		int iUnowned = iiOwnedUnowned.second;
		std::vector<Shelf*> shelves;
		kMap.getShelves(*pArea, shelves);
		for (size_t i = 0; i < shelves.size(); i++)
		{
			iUnowned += shelves[i]->countUnownedPlots() / 2;
		}
		perAreaUnowned.insert(std::make_pair(pArea->getID(), iUnowned));
	}
	bool bRage = isOption(GAMEOPTION_RAGING_BARBARIANS);
	// </advc.300>

	CvPlot const* pBestPlot = NULL;
	int iBestValue = 0;
	for (int iI = 0; iI < kMap.numPlots(); iI++)
	{
		CvPlot& kPlot = kMap.getPlotByIndex(iI);
		if (kPlot.isWater() || kPlot.isVisibleToCivTeam())
			continue;
		// <advc.300>
		CvArea& a = kPlot.getArea();
		int const iAreaSz = a.getNumTiles();
		bool bCivArea = (a.getNumCities() > a.getCitiesPerPlayer(BARBARIAN_PLAYER));
		if (bSkipCivAreas && bCivArea)
			continue;
		int iTargetCities = perAreaUnowned.find(a.getID())->second;
		if (bRage) // Didn't previously affect city density
		{
			iTargetCities *= 7;
			iTargetCities /= 5;
		}
		if (!bCivArea)
		{
			/*	BtS triples iTargetCities here. Want to make it era-based.
				Important that the multiplier is rather small in the first four eras
				so that civs get a chance to settle small landmasses before
				Barbarians appear there. Once there is a Barbarian city on a
				small landmass, there may not be room for another city, and a
				naval attack on a Barbarian city is difficult to execute for the AI. */
			scaled rMult = per100(50) + per100(88) * iEra;
			iTargetCities = (rMult * iTargetCities).round(); // </advc.300>
		}
		int iUnownedTilesThreshold = GC.getInfo(getHandicapType()).
				getUnownedTilesPerBarbarianCity();
		if (iAreaSz < iUnownedTilesThreshold / 3)
		{
			iTargetCities *= iTargetCitiesMultiplier;
			iTargetCities /= 100;
		} // <advc.304>
		int iDestroyedCities = a.getBarbarianCitiesEverCreated() -
				a.getCitiesPerPlayer(BARBARIAN_PLAYER);
		FAssert(iDestroyedCities >= 0);
		iDestroyedCities = std::max(0, iDestroyedCities);
		iUnownedTilesThreshold += iDestroyedCities * 3; // </advc.304>
		iTargetCities /= std::max(1, iUnownedTilesThreshold);

		if (a.getCitiesPerPlayer(BARBARIAN_PLAYER) < iTargetCities)
		{
			//iValue = GET_PLAYER(BARBARIAN_PLAYER).AI_foundValue(pLoopPlot->getX(), pLoopPlot->getY(), GC.getDefineINT("MIN_BARBARIAN_CITY_STARTING_DISTANCE"));
			// K-Mod
			int iValue = citySiteEval.evaluate(kPlot);
			if (iTargetCitiesMultiplier > 100)
			{/* <advc.300> This gives the area with the most owned tiles priority
				over other areas unless the global city target is reached (rare),
				or the most crowded area hasn't enough unowned tiles left.
				The idea of bSkipCivAreas is to settle terrae incognitae earlier,
				so I'm considerably reducing the impact in that case.
				Also, the first city placed in a previously uninhabited area is
				placed randomly b/c each found value gets multipied with 0,
				which is apparently a bug. Let's instead use the projected number
				of owned tiles after placing the city. */
				int iOwned = a.getNumOwnedTiles();
				if (bSkipCivAreas)
					iValue += iOwned;
				else iValue *= iOwned + NUM_INNER_PLOTS; // advc.001 </advc.300>
			}
			//iValue += (100 + SyncRandNum(50));
			/*	advc.300, advc.001: Looks like another bug; probably times 1 to 1.5
				was intended. (Dividing by 100 doesn't affect pBestPlot, but let's
				keep iBestValue is on the scale of a regular found value - although
				it isn't used for anything.)
				NB: This kind of randomization works mostly locally b/c nearby tiles
				tend to have similar found values. */
			iValue *= 100 + SyncRandNum(50);
			iValue /= 100;
			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				pBestPlot = &kPlot;
			}
		}
	}
	if (pBestPlot != NULL)
	{
		FAssert(iBestValue > 0); // advc.300
		GET_PLAYER(BARBARIAN_PLAYER).found(pBestPlot->getX(), pBestPlot->getY());
		// advc.300 (from MNAI):
		if (gPlayerLogLevel > 0 || /* advc.031c: */ gFoundLogLevel > 0) logBBAI("Barbarian city created at plot %d, %d", pBestPlot->getX(), pBestPlot->getY());
	}
}


void CvGame::createBarbarianUnits()
{
	if (isOption(GAMEOPTION_NO_BARBARIANS))
		return;

	if (GC.getPythonCaller()->createBarbarianUnits())
		return;

	//if (GC.getInfo(getCurrentEra()).isNoBarbUnits()) ...
	bool bCreateBarbarians = isBarbarianCreationEra(); // advc.307 (checked later now)
	bool bAnimals = false;
	/*	advc.300: No need to delay Barbarians (bAnimals=true) if they start slowly.
		For slow game speed settings, there is now a similar check in
		CvUnitAI::AI_barbAttackMove. */
	if (barbarianPeakLandRatio() < per100(30) &&
		getNumCivCities() * 2 < countCivPlayersAlive() * 3 &&
		!isOption(GAMEOPTION_ONE_CITY_CHALLENGE))
	{
		bAnimals = true;
	}
	// advc.300: Moved into new function
	if (getGameTurn() < getBarbarianStartTurn())
		bAnimals = true;

	if (bAnimals)
		createAnimals();
	// <advc.300>

    // rfc: disable
	//if (bAnimals)
	//	return;
    return;

	CvHandicapInfo const& kGameHandicap = GC.getInfo(getHandicapType());
	int iBaseTilesPerLandUnit = kGameHandicap.getUnownedTilesPerBarbarianUnit();
	// Divided by 10 b/c now only shelf water tiles count
	int iBaseTilesPerSeaUnit = kGameHandicap.getUnownedWaterTilesPerBarbarianUnit() / 8;
	// </advc.300>
	FOR_EACH_AREA_VAR(pLoopArea)
	{
		// <advc.300>
		CvArea& a = *pLoopArea;
		/*	For each land area, first spawn sea Barbarians for each shelf attached
			to that land area. Skip water areas entirely. Then spawn units in the
			land area. Shelves go first b/c units can now spawn in cargo;
			spawn fewer land units then. No units in unsettled areas.
			(Need to at least spawn a Barbarian city before that). */
		if (a.isWater() || a.getNumCities() == 0)
			continue;
		int iUnowned = 0, iTiles = 0;
		std::vector<Shelf*> shelves;
		GC.getMap().getShelves(a, shelves);
		for (size_t i = 0; i < shelves.size(); i++)
		{
			// Shelves also count for land Barbarians, ...
			iUnowned += shelves[i]->countUnownedPlots();
			iTiles += shelves[i]->size();
		}
		// ... but only half.
		iUnowned /= 2; iTiles /= 2;

		/*	For performance -- countOwnedUnownedHabitableTiles isn't cached;
			goes through the entire map for each land area, and archipelago-type maps
			can have a lot of those. */
		int const iTotal = a.getNumTiles() + iTiles;
		int const iUnownedTotal = a.getNumUnownedTiles() + iUnowned;
		if (iUnownedTotal >= iTotal)
			continue;

		/*	In the following, only care about "habitable" tiles, i.e. with a
			positive food yield (implied for shelf tiles).
			Should tiles visible to a civ count? Yes; it's not unrealistic that
			Barbarians originate in one (visible) place, and emerge as a threat
			in another (invisible) place. */
		std::pair<int,int> iiOwnedUnowned = a.countOwnedUnownedHabitableTiles();
		iUnowned += iiOwnedUnowned.second;
		iTiles += iiOwnedUnowned.first + iiOwnedUnowned.second;
		// NB: Animals are included in this count
		int iLandUnits = a.getUnitsPerPlayer(BARBARIAN_PLAYER);
		// Kill a Barbarian unit if the area gets crowded
		if (killBarbarian(iLandUnits, iTiles,
			a.getPopulationPerPlayer(BARBARIAN_PLAYER), a, NULL))
		{
			iLandUnits--;
		}
		if (iUnownedTotal < iBaseTilesPerLandUnit / 2)
			continue;
		{
			/*	Don't count city defenders. Settled Barbarians being less aggressive
				makes sense, but cities also reduce the number of unowned tiles;
				that's enough. Old Firaxis to-do comment on this subject:
				'XXX eventually need to measure	how many barbs of eBarbUnitAI we
				have in this area...' */
			int iDefenders = 0;
			FOR_EACH_CITY(pCity, GET_PLAYER(BARBARIAN_PLAYER))
			{
				if (pCity->isArea(a))
					iDefenders += pCity->getPlot().plotCount(PUF_isCityAIType);
			}
			iLandUnits = std::max(0, iLandUnits - iDefenders);
		}
		int iNeededLand = numBarbariansToCreate(iBaseTilesPerLandUnit, iTiles,
				iUnowned, iLandUnits);
		int const iBarbarianCities = a.getCitiesPerPlayer(BARBARIAN_PLAYER);
		for (size_t i = 0; i < shelves.size(); i++)
		{
			int iShips = shelves[i]->countBarbarians();
			if (killBarbarian(iShips, shelves[i]->size(),
				a.getPopulationPerPlayer(BARBARIAN_PLAYER), a, shelves[i]))
			{
				iShips--;
			}
			if (!bCreateBarbarians)
				continue;
			int iNeededSea = numBarbariansToCreate(iBaseTilesPerSeaUnit,
					shelves[i]->size(), shelves[i]->countUnownedPlots(), iShips);
			/* 'BETTER_BTS_AI_MOD 9/25/08 jdog5000
				Limit construction of barb ships based on player navies' */
			// advc: BBAI code deleted -- sanity check based on Barbarian cities instead:
			if (iShips > iBarbarianCities + 2)
				iNeededSea = 0;
			// <advc.306> Keep spawning units on ships
			if (iNeededSea <= 0 && iNeededLand <= 0 && a.getNumCivCities() > 0)
				createBarbarianUnits(1, iShips, a, shelves[i], true, true); // </advc.306>
			else
			{
				iNeededLand -= createBarbarianUnits(iNeededSea, iShips, a, shelves[i],
						iNeededLand > 0); // advc.306
			}
		}
		/*	Don't spawn Barbarian units on (or on shelves around) continents where
			civs don't outnumber Barbarians */
		int const iCivCities = a.getNumCivCities();
		FAssert(iBarbarianCities >= 0);
		if (iCivCities > iBarbarianCities && bCreateBarbarians)
			createBarbarianUnits(iNeededLand, iLandUnits, a, NULL);
		/*	Rest of the creation code: moved into functions numBarbariansToCreate and
			createBarbarians */
		// </advc.300>
	}
	FOR_EACH_UNIT_VAR(pLoopUnit, GET_PLAYER(BARBARIAN_PLAYER))
	{
		if (pLoopUnit->isAnimal() &&
			// advc.309: Don't cull animals where there are no civ cities
			pLoopUnit->getArea().getNumCivCities() > 0)
		{
			pLoopUnit->kill(false);
			break;
		}
	}
	// <advc.300>
	FOR_EACH_CITY(pCity, GET_PLAYER(BARBARIAN_PLAYER))
	{
		/*	Large Barb congregations are only a problem if they have nothing
			to attack */
		if (pCity->getArea().getNumCivCities() > 0)
			continue;
		int iUnits = pCity->getPlot().getNumDefenders(BARBARIAN_PLAYER);
		scaled rKillProb = (iUnits - scaled::max(fixp(1.5) * pCity->getPopulation(), 4)) / 4;
		if (SyncRandSuccess(rKillProb))
			pCity->getPlot().killRandomUnit(BARBARIAN_PLAYER, DOMAIN_LAND);
	} // </advc.300>
}


void CvGame::createAnimals()
{
	if (GC.getInfo(getCurrentEra()).isNoAnimals() ||
		isOption(GAMEOPTION_NO_ANIMALS)) // advc.309
	{
		return;
	}
	CvHandicapInfo const& kGameHandicap = GC.getInfo(getHandicapType());
	if (kGameHandicap.getUnownedTilesPerGameAnimal() <= 0)
		return;

	if (getNumCivCities() < countCivPlayersAlive())
		return;

	if (getElapsedGameTurns() < 5)
		return;

	int const iMinAnimalStartingDist = GC.getDefineINT("MIN_ANIMAL_STARTING_DISTANCE"); // advc.300
	FOR_EACH_AREA(pLoopArea)
	{
		if (pLoopArea->isWater())
			continue;

		int iNeededAnimals = pLoopArea->getNumUnownedTiles() /
				kGameHandicap.getUnownedTilesPerGameAnimal();
		/*	<advc.300> Will allow animals to survive longer on landmasses w/o
			civ cities. But only want a couple of animals there. */
		if (pLoopArea->getNumCivCities() <= 0)
			iNeededAnimals /= 2; // </advc.300>
		iNeededAnimals -= pLoopArea->getUnitsPerPlayer(BARBARIAN_PLAYER);
		if (iNeededAnimals <= 0)
			continue;

		iNeededAnimals = (iNeededAnimals / 5) + 1;
		for (int i = 0; i < iNeededAnimals; i++)
		{
			CvPlot* pPlot = GC.getMap().syncRandPlot(
					(RANDPLOT_NOT_VISIBLE_TO_CIV | RANDPLOT_PASSABLE
					| RANDPLOT_WATERSOURCE), // advc.300: Also use no iTimeout (try all plots)
					pLoopArea, iMinAnimalStartingDist);
			if (pPlot == NULL)
				continue;

			UnitTypes eBestUnit = NO_UNIT;
			int iBestValue = 0;
			// advc (comment): This loop picks an animal that is suitable for pPlot
			CvCivilization const& kCiv = GET_PLAYER(BARBARIAN_PLAYER).getCivilization();
			for (int j = 0; j < kCiv.getNumUnits(); j++)
			{
				UnitTypes eLoopUnit = kCiv.unitAt(j);
				CvUnitInfo const& kUnit = GC.getInfo(eLoopUnit);
				if (!kUnit.getUnitAIType(UNITAI_ANIMAL))
					continue;
				if (pPlot->isFeature() ?
					kUnit.getFeatureNative(pPlot->getFeatureType()) :
					kUnit.getTerrainNative(pPlot->getTerrainType()))
				{
					int iValue = 1 + SyncRandNum(1000);
					if (iValue > iBestValue)
					{
						eBestUnit = eLoopUnit;
						iBestValue = iValue;
					}
				}
			}
			if (eBestUnit != NO_UNIT)
			{
				GET_PLAYER(BARBARIAN_PLAYER).initUnit(eBestUnit,
						pPlot->getX(), pPlot->getY(), UNITAI_ANIMAL);
			}
		}
	}
}

// advc.307:
bool CvGame::isBarbarianCreationEra() const
{
	if (isOption(GAMEOPTION_NO_BARBARIANS))
		return false;
	EraTypes eCurrentEra = getCurrentEra();
	return (!GC.getInfo(eCurrentEra).isNoBarbUnits() &&
			/*	Also stop spawning when Barbarian tech falls behind too much;
				may resume once they catch up. */
			eCurrentEra <= GET_PLAYER(BARBARIAN_PLAYER).getCurrentEra() + 1);
}

// <advc.300>
int CvGame::getBarbarianStartTurn() const
{
	int iTargetElapsed = GC.getInfo(getHandicapType()).
			getBarbarianCreationTurnsElapsed() *
			GC.getInfo(getGameSpeedType()).getBarbPercent();
	// Akin to the era adjustment in createBarbarianCities
	iTargetElapsed /= (100 * std::max(1, (int)getStartEra()));
	int iStartTurn = getStartTurn();
	// Have Barbarians appear earlier in Ancient Advanced Start
	if (isOption(GAMEOPTION_ADVANCED_START) && getStartEra() <= 0 &&
		// advc.250b: Earlier Barbarians only if humans start Advanced too
		!isOption(GAMEOPTION_SPAH))
	{
		iStartTurn /= 2;
	}
	// <advc.309>
	else if (isOption(GAMEOPTION_NO_ANIMALS))
		iTargetElapsed = intdiv::uround(iTargetElapsed * 3, 4); // </advc.309>
	iTargetElapsed = std::max(iTargetElapsed, 9);
	return iStartTurn + iTargetElapsed;
}

// Based on code originally in createBarbarianUnits, but modified beyond recognition.
int CvGame::numBarbariansToCreate(int iTilesPerUnit, int iTiles, int iUnowned,
	int iUnitsPresent)
{
	int const iOwned = iTiles - iUnowned;
	scaled const rPeakRatio = barbarianPeakLandRatio();
	if (iOwned <= 0 || rPeakRatio <= 0)
		return 0;
	scaled rDivisor = iTilesPerUnit;
	scaled rDividend;
	{
		scaled rOwnedRatio(iOwned, iTiles);
		bool bPeakReached = (rOwnedRatio >= rPeakRatio);
		if (bPeakReached)
		{
			rDivisor *= (1 - rPeakRatio);
			rDividend = iUnowned;
		}
		else
		{
			rDivisor *= rPeakRatio;
			rDividend = iOwned;
		}
	}
	/*	For Rage, reduce divisor to 65% (50% in BtS), but
		<advc.307> reduces it further based on the game era. */
	if (isOption(GAMEOPTION_RAGING_BARBARIANS))
	{
		int iCurrentEra = getCurrentEra();
		/*	Don't reduce divisor in start era (gets too tough on Classical
			and Medieval starts b/c the starting defenders are mere Archers). */
		if (iCurrentEra <= getStartEra())
			iCurrentEra = 0;
		scaled rRageMultiplier = fixp(0.65);
		rRageMultiplier.mulDiv(8 - iCurrentEra, 8);
		rDivisor *= rRageMultiplier;
		rDivisor.increaseTo(10);
	} // </advc.307>
	else rDivisor.increaseTo(14);
	scaled rTarget = rDividend / rDivisor;
	/*	Make sure that there's enough unowned land where the Barbarians
		could plausibly gather. */
	rTarget.decreaseTo(scaled(iUnowned, 6));
	static scaled const rAdjustment = 1 + per100(GC.getDefineINT(
			"BARB_ACTIVITY_ADJUSTMENT"));
	rTarget *= rAdjustment;

	scaled r = rTarget - iUnitsPresent;
	if (r < 1)
		return 0; // Avoid very small creation probabilities
	scaled rCreationRate = fixp(0.25); // the BtS rate
	// Novel: adjusted to game speed
	rCreationRate /= per100(GC.getInfo(getGameSpeedType()).getBarbPercent());
	r *= rCreationRate;
	/*	BtS always created at least one unit, but, on Marathon, this could be too fast.
		Probabilistic instead. */
	if (r < 1)
	{
		if (SyncRandSuccess(r))
			return 1;
		return 0;
	}
	return r.round();
}

/*	Returns the number of land units spawned (possibly in cargo).
	The first half is new code. */
int CvGame::createBarbarianUnits(int iUnitsToCreate, int iUnitsPresent,
	CvArea& kArea, Shelf* pShelf, bool bCargoAllowed, bool bOnlyCargo) // </advc.300>
{
	/*	<advc.306> Spawn cargo load before ships. Otherwise, the newly placed ship
		would always be an eligible target and too many ships would carry cargo. */
	FAssert(!bCargoAllowed || pShelf != NULL);
	FAssert(!bOnlyCargo || bCargoAllowed);
	int iCreated = 0;
	if (bCargoAllowed)
	{
		CvUnit* pTransport = pShelf->randomBarbarianTransport();
		if (pTransport != NULL)
		{
			UnitAITypes eLoadAI = UNITAI_ATTACK;
			for (int i = 0; i < 2; i++)
			{
				UnitTypes eLoadUnit = randomBarbarianUnit(eLoadAI,
						pTransport->getPlot());
				if (eLoadUnit == NO_UNIT)
					break;
				CvUnit* pLoadUnit = GET_PLAYER(BARBARIAN_PLAYER).initUnit(
						eLoadUnit, pTransport->getX(), pTransport->getY(), eLoadAI);
				/*	(Don't set pTransport to UNITAI_ASSAULT_SEA -- that's for
					medium-/large-scale invasions, and too laborious to adjust.
					Instead add an unload routine to CvUnitAI::barbAttackSeaMove.) */
				if (pLoadUnit == NULL)
					break;
				pLoadUnit->setTransportUnit(pTransport);
				// <advc.304>
				getBarbarianWeightMap().getActivityMap().change(pLoadUnit->getPlot(),
						BarbarianActivityMap::maxStrength() / 2, 2); // </advc.304>
				iCreated++;
				/*	Only occasionally spawn two units at once. Prefer the natural
					way, i.e. a ship receiving a second passenger while travelling
					to its target through fog of war. (I don't think that happens
					often though ...) */
				if (pTransport->getCargo() > 1 || SyncRandSuccess100(73))
					break;
			}
		}
		if (bOnlyCargo)
			return iCreated;
	} // </advc.306>

	for (int i = 0; i < iUnitsToCreate; i++)
	{	// <advc.300>
		int iValid=0;
		CvPlot* pPlot = randomBarbarianPlot(iValid, kArea, pShelf);
		{
			int const iUnitsTarget = iUnitsPresent + 1; // About to create one more
			if (pPlot != NULL)
			{
				FAssert(iValid > 0);
				// Don't create any units if far too few valid tiles remain
				if ((pShelf != NULL && iValid * 100 < pShelf->size()) ||
					iUnitsTarget > iValid)
				{
					pPlot = NULL;
				}
			}
			if (pPlot == NULL)
				return iCreated;
			/*	Skip only one unit, probabilistically. (This could probably
				be simplified a bit.) */
			scaled rSkipProb = std::max(scaled(iUnitsTarget, iValid),
					// In case that both valid count and target number are very small
					scaled(std::min(iUnitsTarget + 2, 3), iValid + 2));
			// Don't let unguarded plots go entirely unpunished forever
			rSkipProb.decreaseTo(fixp(0.9));
			// Especially don't want a constant stream of units from low-weight plots
			rSkipProb *= scaled::max(1, 2 - per100(getBarbarianWeightMap().get(*pPlot)));
			if (SyncRandSuccess(rSkipProb))
				continue;
		}
		UnitAITypes eUnitAI = UNITAI_ATTACK;
		if (pShelf != NULL)
			eUnitAI = UNITAI_ATTACK_SEA;
		// Original code moved into new function:
		UnitTypes eUnitType = randomBarbarianUnit(eUnitAI, *pPlot);
		if (eUnitType == NO_UNIT)
			return iCreated;
		/*CvUnit* pNewUnit =*/GET_PLAYER(BARBARIAN_PLAYER).initUnit(eUnitType,
				pPlot->getX(), pPlot->getY(), eUnitAI);
		if (!pPlot->isWater())
			iCreated++;
		// </advc.300>
	// advc.313: Replaced by a handicap-based modifier
	#if 0
		/*	K-Mod. Sorry, barbarians. Free ships are just too dangerous for
			real civilizations to defend against. */
		if (pPlot->isWater() &&
			!pNewUnit->getUnitInfo().isHiddenNationality()) // kekm.12
		{
			PromotionTypes eDisorganized = (PromotionTypes)
					GC.getInfoTypeForString("PROMOTION_DISORGANIZED", true);
			if (eDisorganized != NO_PROMOTION)
				pNewUnit->setHasPromotion(eDisorganized, true);
		} // K-Mod end
	#endif
		// <advc.304> Discourage nearby unit placement for some time
		getBarbarianWeightMap().getActivityMap().change(*pPlot,
				BarbarianActivityMap::maxStrength() / 2, 2); // </advc.304>
	}
	return iCreated; // advc.306
}

// <advc.300>
CvPlot* CvGame::randomBarbarianPlot(/* out-param */int& iValid,
	CvArea const& kArea, Shelf const* pShelf)
{
	RandPlotFlags const eFlags = (RANDPLOT_NOT_VISIBLE_TO_CIV |
			/*	Shelves already ensure this and one-tile islands
				can't spawn Barbarians anyway. */
			//RANDPLOT_ADJACENT_LAND |
			RANDPLOT_PASSABLE |
			RANDPLOT_HABITABLE | // new
			RANDPLOT_UNOWNED);
	/*	Added the "unowned" flag to prevent spawning in Barbarian land.
		Could otherwise happen now b/c the visible flag and dist. restriction
		no longer apply to Barbarians previously spawned; see
		CvPlot::isVisibleToCivTeam, CvMap::isCivUnitNearby. */
	static int const iDist = GC.getDefineINT("MIN_BARBARIAN_STARTING_DISTANCE");
	// <advc.304>
	CvPlot* pRandPlot = NULL;
	if (pShelf == NULL)
	{
		pRandPlot = GC.getMap().syncRandPlot(eFlags, &kArea, iDist, -1,
				&iValid, &getBarbarianWeightMap());
	}
	else
	{
		pRandPlot = pShelf->randomPlot(eFlags, iDist,
				&iValid, &getBarbarianWeightMap());
	}
	return pRandPlot; // </advc.304>
}


bool CvGame::killBarbarian(int iUnitsPresent, int iTiles, int iPop,
	CvArea& kArea, Shelf* pShelf)
{
	if (iUnitsPresent <= 5) // 5 is never a crowd
		return false;
	scaled rDivisor = std::max(1, 4 * iPop);
	if (pShelf != NULL)
		rDivisor += pShelf->size();
	else rDivisor += iTiles; /*	Includes 50% shelf (given the way this function
								is currently used). */
	// Don't want large Barbarian continents crawling with units
	rDivisor.exponentiate(fixp(0.7));
	rDivisor *= 5;
	if (!SyncRandSuccess(iUnitsPresent / rDivisor))
		return false;
	if (pShelf != NULL)
		return pShelf->killBarbarian();
	CvUnit* pVictim = NULL;
	int iBestValue = 0;
	/*	Same order as for animal culling. Should result in
		first-in-first-out behavior; fair enough for breaking ties. */
	FOR_EACH_UNIT_VAR(pUnit, GET_PLAYER(BARBARIAN_PLAYER))
	{
		CvUnit& u = *pUnit;
		if (u.isAnimal() || !u.isArea(kArea) ||
			u.getUnitCombatType() == NO_UNITCOMBAT)
		{
			continue;
		}
		int iKillValue = 1;
		if (!u.getPlot().isVisibleToWatchingHuman())
			iKillValue += 100;
		if (!u.getPlot().isVisibleToCivTeam())
			iKillValue += 10;
		if (u.getPlot().isCity() &&
			u.getPlot().getNumDefenders(BARBARIAN_PLAYER) >
			GC.getInfo(getHandicapType()).getBarbarianInitialDefenders())
		{
			iKillValue += 5;
		}
		if (iKillValue > iBestValue)
		{
			iBestValue = iKillValue;
			pVictim = &u;
		}
	}
	if (pVictim == NULL)
		return false;
	pVictim->kill(false);
	return true;
}

// Based on BtS code originally in createBarbarianUnits
UnitTypes CvGame::randomBarbarianUnit(UnitAITypes eUnitAI, CvPlot const& kPlot)
{
	bool bSea;
	switch (eUnitAI)
	{
	case UNITAI_ATTACK_SEA: bSea = true; break;
	case UNITAI_ATTACK: bSea = false; break;
	default: return NO_UNIT;
	}
	/*	<advc.301> Era numbers are just too coarse. Going by tech costs
		isn't great for mod-mods (which may completely overhaul tech costs),
		don't know how to do this more properly with reasonable effort. */
	bool bAnyExpensiveTech = false;
	FOR_EACH_ENUM(Tech)
	{
		if (GET_TEAM(BARBARIAN_TEAM).isHasTech(eLoopTech) &&
			GC.getInfo(eLoopTech).getResearchCost() > 100)
		{
			bAnyExpensiveTech = true;
			break;
		}
	} // </advc.301>
	UnitTypes eR = NO_UNIT;
	int iBestValue = 0;
	CvCivilization const& kCiv = GET_PLAYER(BARBARIAN_PLAYER).getCivilization();
	for (int i = 0; i < kCiv.getNumUnits(); i++)
	{
		UnitTypes const eUnit = kCiv.unitAt(i);
		CvUnitInfo const& kUnit = GC.getInfo(eUnit);
		DomainTypes const eDomain = kUnit.getDomainType();
		if (kUnit.getCombat() <= 0 || eDomain == DOMAIN_AIR ||
			kUnit.isMostlyDefensive() || // advc.315
			(eDomain == DOMAIN_SEA) != bSea ||
			!GET_PLAYER(BARBARIAN_PLAYER).canTrain(eUnit))
		{
			continue;
		}
		// <advc.301>
		BonusTypes const eAndBonus = kUnit.getPrereqAndBonus();
		std::vector<TechTypes> aeAndBonusTechs;
		if (eAndBonus != NO_BONUS)
		{
			CvBonusInfo const& kAndBonus = GC.getInfo(eAndBonus);
			TechTypes eTradeTech = kAndBonus.getTechCityTrade(); // (as in BtS)
			if (eTradeTech != NO_TECH)
				aeAndBonusTechs.push_back(eTradeTech);
			TechTypes eRevealTech = kAndBonus.getTechReveal();
			if (eRevealTech != NO_TECH)
				aeAndBonusTechs.push_back(eRevealTech);
			bool bValid = true;
			for (size_t j = 0; j < aeAndBonusTechs.size(); j++)
			{
				if (!GET_TEAM(BARBARIAN_TEAM).isHasTech(aeAndBonusTechs[j]))
				{
					bValid = false;
					break;
				}
			}
			if (!bValid || !kPlot.getArea().hasAnyAreaPlayerBonus(eAndBonus))
				continue;
		}
		//bool bFound = false;
		// Store these techs for the era check below
		std::vector<TechTypes> aeOrBonusTechsFound;
		// </advc.301>
		bool bRequires = false;
		for (int j = 0; j < kUnit.getNumPrereqOrBonuses(); j++)
		{
			bRequires = true;
			BonusTypes const eOrBonus = kUnit.getPrereqOrBonuses(j);
			CvBonusInfo const& kOrBonus = GC.getInfo(eOrBonus);
			if (GET_TEAM(BARBARIAN_TEAM).isHasTech(kOrBonus.getTechCityTrade()) &&
				// <advc.301>
				GET_TEAM(BARBARIAN_TEAM).isHasTech(kOrBonus.getTechReveal()) &&
				kPlot.getArea().hasAnyAreaPlayerBonus(eOrBonus))
			{
				//bFound = true;
				aeOrBonusTechsFound.push_back(kOrBonus.getTechCityTrade());
				aeOrBonusTechsFound.push_back(kOrBonus.getTechReveal());
				// </advc.301>
			}
		}
		if (bRequires && aeOrBonusTechsFound.empty())
			continue;
		int iDieSides = 1000;
		// <advc.301>
		TechTypes const eAndTech = kUnit.getPrereqAndTech();
		int iUnitEra = 0;
		if (eAndTech != NO_TECH)
			iUnitEra = GC.getInfo(eAndTech).getEra();
		// No units from more than 1 era behind the civs
		if (iUnitEra + 1 < getCurrentEra())
			continue;
		// Treat Warrior as pre-Ancient in the following
		if (eAndTech == NO_TECH)
			iUnitEra = -1;
		// Mounted units only in open terrain
		static UnitCombatTypes const eMounted = (UnitCombatTypes)
				GC.getInfoTypeForString("UNITCOMBAT_MOUNTED");
		bool const bMounted = (kUnit.getUnitCombatType() == eMounted);
		if (bMounted)
		{
			if (kPlot.isWater() || kPlot.defenseModifier(NO_TEAM, true) > 0)
				continue;
			// Don't place them in disease-ridden land either
			int iBadHealth = 0;
			for (SquareIter it(kPlot, 1); it.hasNext(); ++it)
			{
				if (it->isFeature())
				{
					iBadHealth += std::min(0,
							GC.getInfo(it->getFeatureType()).getHealthPercent());
				}
			}
			if (iBadHealth <= -100)
				continue;
		}
		// Higher chance for non-outdated units w/o resource reqs (i.e. Archer)
		scaled const rNoBonusReqDieSidesMult = fixp(1.3);
		if ((!bRequires && eAndBonus == NO_BONUS &&
			/*	Want Warrior to be as likely as Archer until Axes and Spears
				become available. The game era is usually already Classical
				when Archers become available. */
			(!bAnyExpensiveTech || iUnitEra + 1 >= getCurrentEra())) ||
			bMounted) // To make up for the terrain restriction
		{
			iDieSides = (iDieSides * rNoBonusReqDieSidesMult).uround();
		} // </advc.301>
		int iValue = 1 + SyncRandNum(iDieSides);
		if (kUnit.getUnitAIType(eUnitAI))
		{
			//iValue += 200;
			// <advc.301>
			iValue += (rNoBonusReqDieSidesMult + 1).getPercent();
		}
		for (size_t j = 0; j < aeAndBonusTechs.size(); j++)
		{
			iUnitEra = std::max<int>(iUnitEra,
					GC.getInfo(aeAndBonusTechs[j]).getEra());
		}
		{
			int iOrBonusEra = MAX_INT;
			for (size_t j = 0; j < aeOrBonusTechsFound.size(); j++)
			{
				iOrBonusEra = std::min<int>(iOrBonusEra,
						GC.getInfo(aeOrBonusTechsFound[j]).getEra());
			}
			if (iOrBonusEra < MAX_INT)
				iUnitEra = std::max(iUnitEra, iOrBonusEra);
		}
		/*	Absolute preference for units of the current or previous era
			of the Barbarians. Due to the game era check above and Barbarians
			normally being behind the game era, this will matter mainly just
			for Warrior, which we're treating as pre-Ancient here:
			No more Warriors once Swords are available. */
		iValue += 10000 * (1 + std::min(iUnitEra,
				GET_TEAM(BARBARIAN_TEAM).getCurrentEra() - 1));
		// </advc.301>
		if (iValue > iBestValue)
		{
			eR = eUnit;
			iBestValue = iValue;
		}
	}
	return eR;
}

// (See documentation in XML)
scaled CvGame::barbarianPeakLandRatio() const
{
	scaled r;
	if (isOption(GAMEOPTION_RAGING_BARBARIANS))
	{
		static scaled const rRagingRatio = per100(GC.getDefineINT(
				"BARB_RAGE_PEAK_PERCENT"));
		r = rRagingRatio;
	}
	else
	{
		static scaled const rNormalRatio = per100(GC.getDefineINT(
				"BARB_PEAK_PERCENT"));
		r = rNormalRatio;
	}
	r.clamp(0, 1);
	return r;
}
// </advc.300>

void CvGame::updateWar()
{
	if (isOption(GAMEOPTION_ALWAYS_WAR))
	{
		for (int iI = 0; iI < MAX_TEAMS; iI++)
		{
			CvTeam& kTeam1 = GET_TEAM((TeamTypes)iI);
			if (kTeam1.isAlive() && kTeam1.isHuman())
			{
				for (int iJ = 0; iJ < MAX_TEAMS; iJ++)
				{
					CvTeam& kTeam2 = GET_TEAM((TeamTypes)iJ);
					if (kTeam2.isAlive() && !kTeam2.isHuman())
					{
						FAssert(iI != iJ);
						if (kTeam1.isHasMet((TeamTypes)iJ))
						{
							if (!kTeam1.isAtWar((TeamTypes)iJ))
							{
								kTeam1.declareWar(((TeamTypes)iJ), false, NO_WARPLAN);
							}
						}
					}
				}
			}
		}
	}
}


void CvGame::updateMoves()
{
	int aiShuffle[MAX_PLAYERS];
	if (isMPOption(MPOPTION_SIMULTANEOUS_TURNS))
		getSorenRand().shuffle(aiShuffle, MAX_PLAYERS);
	else
	{
		for (int iI = 0; iI < MAX_PLAYERS; iI++)
		{
			aiShuffle[iI] = iI;
		}
	} // <advc.001y>
	int iMaxUnitUpdateAttempts = 18;
	FAssertMsg(m_iUnitUpdateAttempts != iMaxUnitUpdateAttempts, "Unit stuck in a loop");
#ifdef _DEBUG
	iMaxUnitUpdateAttempts += 4; // Extra iterations for debugging
#endif
	// </advc.001y>
	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		CvPlayerAI& kPlayer = GET_PLAYER((PlayerTypes)aiShuffle[iI]);
		if (!kPlayer.isAlive() || !kPlayer.isTurnActive())
			continue;

		if (!kPlayer.isAutoMoves())
		{
			kPlayer.AI_unitUpdate();
			if (!kPlayer.isHuman() && !kPlayer.hasBusyUnit())
			{
				/*	advc.001y: Safety measure against infinite loop
					(Complementing Vanilla Civ 4 code in CvSelectionGroupAI::AI_update.
					The attempt counter there won't work when CvUnitAI::AI_update
					joins a different selection group.) */
				if (m_iUnitUpdateAttempts > iMaxUnitUpdateAttempts ||
					!kPlayer.hasReadyUnit(true))
				{
					kPlayer.setAutoMoves(true);
				}
				else m_iUnitUpdateAttempts++; // advc.001y
			}
		}
		if (kPlayer.isAutoMoves())
		{
			FOR_EACH_GROUP_VAR(pGroup, kPlayer)
				pGroup->autoMission();
			/*	K-Mod. Here's where we do the AI for automated units.
				Note, we can't do AI_update and autoMission in the same loop, because
				either one might delete the group - and thus cause the other to crash. */
			if (kPlayer.isHuman())
			{
				FOR_EACH_GROUPAI_VAR(pGroup, kPlayer)
				{
					if (pGroup->AI_update())
					{
						FAssert(kPlayer.hasBusyUnit());
						break;
					}
				}
				/*	Refresh the group cycle for human players.
					Non-human players can wait for their units to wake up, or regain moves -
					group cycle isn't very important for them anyway. */
				kPlayer.refreshGroupCycleList();
			} // K-Mod end
			if (!kPlayer.hasBusyUnit())
				kPlayer.setAutoMoves(false);
		}
	}
}


void CvGame::verifyCivics()
{
	for (PlayerIter<ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		itPlayer->verifyCivics();
	}
}


void CvGame::updateTimers()
{
	for (PlayerIter<ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		itPlayer->updateTimers();
	}
}


void CvGame::updateTurnTimer()
{
	if (!isMPOption(MPOPTION_TURN_TIMER)) // Are we using a turn timer?
		return;

	if (getElapsedGameTurns() <= 0 && isOption(GAMEOPTION_ADVANCED_START))
		return;

	if (getTurnSlice() <= getCutoffSlice()) // Has the turn expired?
		return;

	for (int i = 0; i < MAX_PLAYERS; i++)
	{
		if (GET_PLAYER((PlayerTypes)i).isAlive() &&
			GET_PLAYER((PlayerTypes)i).isTurnActive())
		{
			GET_PLAYER((PlayerTypes)i).setEndTurn(true);
			if (!isMPOption(MPOPTION_SIMULTANEOUS_TURNS) && !isSimultaneousTeamTurns())
				break;
		}
	}
}


void CvGame::testAlive()
{
	FOR_EACH_ENUM(Player)
		GET_PLAYER(eLoopPlayer).verifyAlive();
}


bool CvGame::testVictory(VictoryTypes eVictory, TeamTypes eTeam, bool* pbEndScore) const
{
	FAssertEnumBounds(eVictory);
	FAssertBounds(0, MAX_CIV_TEAMS, eTeam);
	FAssert(GET_TEAM(eTeam).isAlive());

	if (pbEndScore != NULL)
		*pbEndScore = false;

	if (!isVictoryValid(eVictory))
		return false;

	CvVictoryInfo const& kVictory = GC.getInfo(eVictory);
	if (kVictory.isEndScore())
	{
		if (pbEndScore)
			*pbEndScore = true;

		if (getMaxTurns() == 0 || getElapsedGameTurns() < getMaxTurns())
			return false;
	}
	if (kVictory.isTargetScore())
	{
		if (getTargetScore() == 0 || getTeamScore(eTeam) < getTargetScore())
			return false;
	}
	if (kVictory.isEndScore() || kVictory.isTargetScore())
	{
		int const iTestScore = getTeamScore(eTeam);
		for (TeamIter<CIV_ALIVE,NOT_SAME_TEAM_AS> itOther(eTeam);
			itOther.hasNext(); ++itOther)
		{
			if (getTeamScore(itOther->getID()) >= iTestScore)
				return false;
		}
	}
	CvTeam const& kTeam = GET_TEAM(eTeam);
	if (kVictory.isConquest())
	{
		if (kTeam.getNumCities() <= 0)
			return false;
		for (TeamIter<CIV_ALIVE,NOT_SAME_TEAM_AS> itOther(eTeam);
			itOther.hasNext(); ++itOther)
		{
			if (!itOther->isVassal(eTeam) && itOther->getNumCities() > 0)
				return false;
		}
	}
	if (kVictory.isDiploVote())
	{
		bool bFound = false;
		FOR_EACH_ENUM(Vote)
		{
			if (GC.getInfo(eLoopVote).isVictory() &&
				getVoteOutcome(eLoopVote) == eTeam)
			{
				bFound = true;
				break;
			}
		}
		if (!bFound)
			return false;
	}
	if (getAdjustedPopulationPercent(eVictory) > 0)
	{
		if (100 * kTeam.getTotalPopulation() <
			getTotalPopulation() * getAdjustedPopulationPercent(eVictory))
		{
			return false;
		}
	}
	if (getAdjustedLandPercent(eVictory) > 0)
	{
		if (100 * kTeam.getTotalLand() <
			GC.getMap().getLandPlots() * getAdjustedLandPercent(eVictory))
		{
			return false;
		}
	}
	if (kVictory.getReligionPercent() > 0)
	{
		if (getNumCivCities() <= countCivPlayersAlive() * 2)
			return false;

		bool bFound = false;
		FOR_EACH_ENUM(Religion)
		{
			if (kTeam.hasHolyCity(eLoopReligion) &&
				calculateReligionPercent(eLoopReligion) >=
				kVictory.getReligionPercent())
			{
				bFound = true;
				break;
			}
		}
		if (!bFound)
			return false;
	}
	if (kVictory.getCityCulture() != NO_CULTURELEVEL &&
		kVictory.getNumCultureCities() > 0)
	{
		int iCount = 0;
		for (MemberIter itMember(eTeam); itMember.hasNext(); ++itMember)
		{
			FOR_EACH_CITY(pCity, *itMember)
			{
				if (pCity->getCultureLevel() >= culturalVictoryCultureLevel())
					iCount++;
			}
		}
		if (iCount < kVictory.getNumCultureCities())
			return false;
	}
	if (kVictory.getTotalCultureRatio() > 0)
	{
		int const iThreshold = (kTeam.countTotalCulture() * 100) /
				kVictory.getTotalCultureRatio();
		for (TeamIter<CIV_ALIVE,NOT_SAME_TEAM_AS> itOther(eTeam);
			itOther.hasNext(); ++itOther)
		{
			if (itOther->countTotalCulture() > iThreshold)
				return false;
		}
	}
	FOR_EACH_ENUM(BuildingClass)
	{
		if (GC.getInfo(eLoopBuildingClass).getVictoryThreshold(eVictory) >
			kTeam.getBuildingClassCount(eLoopBuildingClass))
		{
			return false;
		}
	}
	FOR_EACH_ENUM(Project)
	{
		if (GC.getInfo(eLoopProject).getVictoryMinThreshold(eVictory) >
			kTeam.getProjectCount(eLoopProject))
		{
			return false;
		}
	}
	if (!GC.getPythonCaller()->isVictory(eVictory))
		return false;

	return true;
}


void CvGame::testVictory()
{
	bool bEndScore = false;

	if (getVictory() != NO_VICTORY)
		return;

	if (getGameState() == GAMESTATE_EXTENDED)
		return;

	updateScore();
	// <advc.003y> Replace Python callback (which is now disabled by default)
	if (getElapsedGameTurns() <= 10 || !GC.getPythonCaller()->isVictoryPossible())
		return; // </advc.003y>

	std::vector<std::pair<TeamTypes,VictoryTypes> > aeeWinners; // advc: was vector<vector<int> >
	for (TeamIter<MAJOR_CIV> itTeam; itTeam.hasNext(); ++itTeam)
	{
		CvTeam& kTeam = *itTeam;
		FOR_EACH_ENUM2(Victory, eVictory)
		{
			if (testVictory(eVictory, kTeam.getID(), &bEndScore))
			{
                // rfc: historical and religious victory checked in Python
                if (eVictory == VICTORY_HISTORICAL || eVictory == VICTORY_RELIGIOUS)
                    continue;

				if (kTeam.getVictoryCountdown(eVictory) < 0)
				{
					if (kTeam.getVictoryDelay(eVictory) == 0)
						kTeam.setVictoryCountdown(eVictory, 0);
				}
				//update victory countdown
				if (kTeam.getVictoryCountdown(eVictory) > 0)
					kTeam.changeVictoryCountdown(eVictory, -1);
				if (kTeam.getVictoryCountdown(eVictory) == 0)
				{
					if (SyncRandSuccess100(kTeam.getLaunchSuccessRate(eVictory)))
						aeeWinners.push_back(std::make_pair(kTeam.getID(), eVictory));
					else kTeam.resetVictoryProgress();
				}
			}
		}
	}
	if (aeeWinners.size() > 0)
	{
		int iWinner = SyncRandNum(aeeWinners.size());
		setWinner(aeeWinners[iWinner].first, aeeWinners[iWinner].second);
	}
	if (getVictory() == NO_VICTORY && !bEndScore && getMaxTurns() > 0 &&
		getElapsedGameTurns() >= getMaxTurns())
	{
		if (getAIAutoPlay() > 0 || gDLL->GetAutorun())
			setGameState(GAMESTATE_EXTENDED);
		else setGameState(GAMESTATE_OVER);
	}
}


void CvGame::processVote(const VoteTriggeredData& kData, int iChange)
{
	FAssert(iChange != 0); // advc
	CvVoteInfo const& kVote = GC.getInfo(kData.kVoteOption.eVote);
	changeTradeRoutes(kVote.getTradeRoutes() * iChange);
	if (kVote.isFreeTrade())
		changeFreeTradeCount(iChange);
	if (kVote.isNoNukes())
		changeNoNukesCount(iChange);
	FOR_EACH_NON_DEFAULT_KEY(kVote.isForceCivic(), Civic)
	{
		changeForceCivicCount(eLoopCivic, iChange);
	}
	if (iChange <= 0)
		return;

	if (kVote.isOpenBorders() || kVote.isDefensivePact()) // advc: Merged these two handlers
	{
		for (TeamIter<MAJOR_CIV> itFirst; itFirst.hasNext(); ++itFirst)
		{
            // doc: unaffected by defied resolution
            if (getPlayerVote(itFirst->getLeaderID(), kData.getID()) == PLAYER_VOTE_NEVER)
                continue;
			if (!itFirst->isVotingMember(kData.eVoteSource))
				continue;
			for (TeamIter<MAJOR_CIV> itSecond; itSecond.hasNext(); ++itSecond)
			{
			    // doc: unaffected by defied resolution
			    if (getPlayerVote(itSecond->getLeaderID(), kData.getID()) == PLAYER_VOTE_NEVER)
			        continue;
				if (!itSecond->isVotingMember(kData.eVoteSource))
					continue;
				if (itSecond->getID() > itFirst->getID())
				{
					if (kVote.isOpenBorders())
						itFirst->signOpenBorders(itSecond->getID(), /* advc.032: */ true);
					if (kVote.isDefensivePact())
						itFirst->signDefensivePact(itSecond->getID(), /* advc.032: */ true);
				}
			}
		}
		setVoteOutcome(kData, NO_PLAYER_VOTE);
	}
	else if (kVote.isForcePeace())
	{
		FAssert(NO_PLAYER != kData.kVoteOption.ePlayer);
		CvPlayer& kPlayer = GET_PLAYER(kData.kVoteOption.ePlayer);
		if (gTeamLogLevel >= 1) logBBAI("  Vote for forcing peace against team %d (%S) passes", kPlayer.getTeam(), kPlayer.getCivilizationDescription(0)); // BETTER_BTS_AI_MOD, AI logging, 10/02/09, jdog5000
		// <kekm.25> 'Cancel defensive pacts with the attackers first'
		FOR_EACH_DEAL_VAR(pLoopDeal)
		{
			if ((TEAMID(pLoopDeal->getFirstPlayer()) == kPlayer.getTeam() &&
				GET_TEAM(pLoopDeal->getSecondPlayer()).
				isVotingMember(kData.eVoteSource)) ||
				(TEAMID(pLoopDeal->getSecondPlayer()) == kPlayer.getTeam() &&
				GET_TEAM(pLoopDeal->getFirstPlayer()).
				isVotingMember(kData.eVoteSource)))
			{
				FOR_EACH_TRADE_ITEM(pLoopDeal->getFirstList())
				{
					if (pItem->m_eItemType == TRADE_DEFENSIVE_PACT)
					{
						pLoopDeal->kill();
						break;
					}
				} // advc: Don't bother with SecondTrades; DPs are dual.
			}
		} // </kekm.25>
		for (PlayerIter<MAJOR_CIV,NOT_SAME_TEAM_AS> itLoopPlayer(kPlayer.getTeam());
			itLoopPlayer.hasNext(); ++itLoopPlayer)
		{
            // doc: unaffected by defied resolution
            if (getPlayerVote(itLoopPlayer->getID(), kData.getID()) == PLAYER_VOTE_NEVER)
                continue;
			if (!itLoopPlayer->isVotingMember(kData.eVoteSource))
				continue;
			/*	advc.130v (note): Not replaced with CvTeam::signPeaceTreaty
				because I want vassals to get their own peace treaties here. */
            // rfc: war check
			if (atWar(itLoopPlayer->getTeam(), GET_PLAYER(kData.kVoteOption.ePlayer).getTeam())
            {
                itLoopPlayer->forcePeace(kData.kVoteOption.ePlayer);
			    CvEventReporter::getInstance().peaceBrokered(GET_TEAM(getSecretaryGeneral(kData.eVoteSource)).getLeaderID(), itLoopPlayer->getID(), kData.kVoteOption.ePlayer);
            }
		}
		setVoteOutcome(kData, NO_PLAYER_VOTE);
	}
	else if (kVote.isForceNoTrade())
	{
		FAssert(NO_PLAYER != kData.kVoteOption.ePlayer);
		CvPlayer& kPlayer = GET_PLAYER(kData.kVoteOption.ePlayer);
		for (PlayerIter<MAJOR_CIV> itLoopPlayer; itLoopPlayer.hasNext(); ++itLoopPlayer)
		{
			if (!itLoopPlayer->isVotingMember(kData.eVoteSource))
				continue;
			if (itLoopPlayer->canStopTradingWithTeam(kPlayer.getTeam()))
				itLoopPlayer->stopTradingWithTeam(kPlayer.getTeam());
		}
		setVoteOutcome(kData, NO_PLAYER_VOTE);
	}
	else if (kVote.isForceWar())
	{
		CvPlayer& kPlayer = GET_PLAYER(kData.kVoteOption.ePlayer);
		if (gTeamLogLevel >= 1) logBBAI("  Vote for war against team %d (%S) passes", kPlayer.getTeam(), kPlayer.getCivilizationDescription(0)); // BETTER_BTS_AI_MOD, AI logging, 10/02/09, jdog5000
		CvTeamAI& kTeam = GET_TEAM(kPlayer.getTeam());
		// advc.001: Exclude dead civs
		for (PlayerIter<MAJOR_CIV,POTENTIAL_ENEMY_OF> it(kTeam.getID());
			it.hasNext(); ++it)
		{
            // doc: unaffected by defied resolution
            if (getPlayerVote(it->getID(), kData.getID()) == PLAYER_VOTE_NEVER)
                continue;

			CvTeam& kFullMember = GET_TEAM(it->getTeam());
			// kekm.25/advc: was isVotingMember
			if (!kFullMember.isFullMember(kData.eVoteSource))
				continue;
			if (kFullMember.canChangeWarPeace(kTeam.getID()))
			{
				// <kekm.26>
				CvTeam::queueWar(kFullMember.getID(), kTeam.getID(),
						false, WARPLAN_DOGPILE); // </kekm.26>
				kTeam.AI_makeUnwillingToTalk(kFullMember.getID()); // advc.104i
			}
		}
		CvTeam::triggerWars(); // kekm.26
		setVoteOutcome(kData, NO_PLAYER_VOTE);
	}
	else if (kVote.isAssignCity())
	{
		CvPlayer& kPlayer = GET_PLAYER(kData.kVoteOption.ePlayer);
		CvCity* pCity = kPlayer.getCity(kData.kVoteOption.iCityId);
		if (pCity != NULL &&
			kData.kVoteOption.eOtherPlayer != NO_PLAYER)
		{
            // doc: can be defied but leads to war
            if (getPlayerVote(pCity->getOwner(), kData.getID()) == PLAYER_VOTE_NEVER)
            [
                for (PlayerIter<MAJOR_CIV,POTENTIAL_ENEMY_OF> it(kPlayer.getTeam()); it.hasNext(); ++it)
                {
                    if (getPlayerVote(it->getID(), kData.getID()) == PLAYER_VOTE_YES)
                    {
                        GET_TEAM(it->getTeam()).declareWar(pCity->getTeam(), true, WARPLAN_LIMITED);
                    }
                }
            }
            else
            {
   			    CvPlayer& kNewOwner = GET_PLAYER(kData.kVoteOption.eOtherPlayer);
			    if (kNewOwner.getID() != pCity->getOwner())
			    {
				    if (gTeamLogLevel >= 1) logBBAI("  Vote for assigning %S to %d (%S) passes", pCity->getName().GetCString(), kNewOwner.getTeam(), kNewOwner.getCivilizationDescription(0)); // BETTER_BTS_AI_MOD, AI logging, 10/02/09, jdog5000
				    kNewOwner.acquireCity(pCity, false, true, true,
						    false, true); // advc.ctr
			    }
            }
		}
		// advc (note): Otherwise, the city has changed owner while the votes were cast.
		setVoteOutcome(kData, NO_PLAYER_VOTE);
	}
    // doc: revoke membership resolution
	else if (kVote.isRevokeMembership())
	{
		GET_PLAYER(kData.kVoteOption.ePlayer).setLoyalMember(kData.eVoteSource, false);
	}
    // doc: gold resolution
	else if (kVote.getGoldPercent() > 0)
	{
		int iGold;
		int iTotalGold = 0;

	    for (PlayerIter<MAJOR_CIV> it; it.hasNext(); ++it)
	    {
	        // dpc: unaffected by defied resolution
	        if (getPlayerVote(it->getID(), kData.getID()) == PLAYER_VOTE_NEVER)
                 continue;
	        if (kData.kVoteOption.ePlayer == it->getID())
                continue;

	        if (it->isFullMember(kData.eVoteSource))
	        {
	            iGold = it->getGold() * kVote.getGoldPercent();
	            iGold /= 100;
	            iTotalGold += iGold;
	            kLoopPlayer.changeGold(-iGold);
	        }
        }

		if (kData.kVoteOption.ePlayer != NO_PLAYER)
		{
			GET_PLAYER(kData.kVoteOption.ePlayer).changeGold(iTotalGold / 2);
			// TODO: refactor
            m_kUI.addMessage(kData.kVoteOption.ePlayer, true, GC.getEVENT_MESSAGE_TIME(), gDLL->getText("TXT_KEY_APOSTOLIC_PALACE_COLLECT_TITHE", iTotalGold / 2), "", MESSAGE_TYPE_MAJOR_EVENT, "", (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), -1, -1, true, true);
		}

		setVoteOutcome(kData, NO_PLAYER_VOTE);
	}

	if (kVote.getEspionage() > 0)
	{
		PlayerTypes ePlayer = kData.kVoteOption.ePlayer;
		PlayerTypes eOtherPlayer = kData.kVoteOption.eOtherPlayer;

		if (ePlayer != NO_PLAYER && eOtherPlayer != NO_PLAYER)
		{
			GET_TEAM(GET_PLAYER(ePlayer).getTeam()).changeEspionagePointsAgainstTeam(GET_PLAYER(eOtherPlayer).getTeam(), kVote.getEspionage() * GET_PLAYER(ePlayer).getReligionPopulation(GC.getGame().getVoteSourceReligion(kData.eVoteSource)));
		}

		setVoteOutcome(kData, NO_PLAYER_VOTE);
	}

	if (kVote.getHappiness() < 0)
	{
		int iLoop;
		for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
		{
			CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iI);

			if (kLoopPlayer.isMinorCiv())
			{
				continue;
			}

			// Leoreth: unaffected by defied, but passed resolution
			if (getPlayerVote((PlayerTypes)iI, kData.getID()) == PLAYER_VOTE_NEVER)
			{
				continue;
			}

			if (kLoopPlayer.isFullMember(kData.eVoteSource))
			{
				for (CvCity* pLoopCity = kLoopPlayer.firstCity(&iLoop); NULL != pLoopCity; pLoopCity = kLoopPlayer.nextCity(&iLoop))
				{
					ReligionTypes eReligion = GC.getGameINLINE().getVoteSourceReligion(kData.eVoteSource);

					if (NO_RELIGION == eReligion || pLoopCity->isHasReligion(eReligion))
					{
						int iAngerLength = pLoopCity->flatDefyResolutionAngerLength();
						if (NO_RELIGION != eReligion && pLoopCity->isHasReligion(eReligion))
						{
							iAngerLength /= std::max(1, pLoopCity->getReligionCount());
						}

						pLoopCity->changeDefyResolutionAngerTimer(iAngerLength);
					}
				}
			}
		}

		if (kVote.isDecolonize())
		{
			CvCity* pCity = GET_PLAYER(kData.kVoteOption.ePlayer).getCity(kData.kVoteOption.iCityId);

			pCity->liberate(false);
		}

		if (kVote.isReleaseCivilization())
		{
			GET_PLAYER(kData.kVoteOption.ePlayer).splitEmpire(kData.kVoteOption.eOtherPlayer);
		}

		setVoteOutcome(kData, NO_PLAYER_VOTE);
	}
}


int CvGame::getIndexAfterLastDeal()
{
	return m_deals.getIndexAfterLast();
}


CvDeal* CvGame::addDeal()
{
	return m_deals.add();
}


 void CvGame::deleteDeal(int iID)
{
	m_deals.removeAt(iID);
	gDLL->getInterfaceIFace()->setDirty(Foreign_Screen_DIRTY_BIT, true);
}

/*	advc.072: All the FAssert(false) in this function mean that we're somehow
	out of step with the iteration that happens in the EXE. */
CvDeal* CvGame::nextCurrentDeal(PlayerTypes eGivePlayer, PlayerTypes eReceivePlayer,
	TradeableItems eItemType, int iData, bool bWidget)
{
	if (!m_bShowingCurrentDeals)
	{
		m_currentDeals.clear(); // Probably not needed, but can't hurt to clear them.
		m_currentDealsWidget.clear();
		return NULL;
	}
	// Probably not needed:
	PlayerTypes eDiploPlayer = (PlayerTypes)gDLL->getDiplomacyPlayer();
	if (!((getActivePlayer() == eGivePlayer && eDiploPlayer == eReceivePlayer) ||
		(getActivePlayer() == eReceivePlayer && eDiploPlayer == eGivePlayer)))
	{
		return NULL;
	}
	CLinkList<DealItemData>& kCurrentDeals = (bWidget ? m_currentDealsWidget :
			m_currentDeals);
	if (kCurrentDeals.getLength() <= 0)
	{
		bool bFirstFound = false;
		FOR_EACH_DEAL(d)
		{
			if (!d->isBetween(eGivePlayer, eReceivePlayer))
				continue;
			CLinkList<TradeData> const& kGiveList = (d->getFirstPlayer() == eGivePlayer ?
					d->getFirstList() : d->getSecondList());
			FOR_EACH_TRADE_ITEM(kGiveList)
			{
				if (!CvDeal::isAnnual(pItem->m_eItemType) &&
					pItem->m_eItemType != TRADE_PEACE_TREATY)
				{
					break;
				}
				if (!bFirstFound)
				{
					if (pItem->m_eItemType != eItemType ||
						pItem->m_iData != iData)
					{
						FAssert(false);
						return NULL;
					}
					bFirstFound = true;
				}
				DealItemData data(eGivePlayer, eReceivePlayer, pItem->m_eItemType,
						pItem->m_iData, d->getID());
				kCurrentDeals.insertAtEnd(data);
			}
		}
	}
	if (kCurrentDeals.getLength() <= 0)
	{
		FAssert(false);
		return NULL;
	}
	CLLNode<DealItemData>* pNode = kCurrentDeals.head();
	DealItemData data = pNode->m_data;
	if (data.eGivePlayer != eGivePlayer || data.eReceivePlayer != eReceivePlayer ||
		data.iData != iData || data.eItemType != eItemType)
	{
		kCurrentDeals.clear();
		FAssert(false);
		return NULL;
	}
	CvDeal* pNext = getDeal(pNode->m_data.iDeal);
	kCurrentDeals.deleteNode(pNode);
	FAssert(pNext != NULL);
	return pNext;
}

// advc.027b:
std::pair<uint,uint> CvGame::getInitialRandSeed() const
{
	return std::make_pair(m_initialRandSeed.uiMap, m_initialRandSeed.uiSync);
}


int CvGame::calculateSyncChecksum()
{
	//PROFILE_FUNC(); // advc.003o
	// <advc.opt>
	if (!isNetworkMultiPlayer())
		return 0; // </advc.opt>

	int iValue = 0;
	iValue += getMapRand().getSeed();
	iValue += getSorenRand().getSeed();

	iValue += getNumCities();
	iValue += getTotalPopulation();
	iValue += getNumDeals();

	iValue += GC.getMap().getOwnedPlots();
	iValue += GC.getMap().getNumAreas();

	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		CvPlayerAI const& kPlayer = GET_PLAYER((PlayerTypes)iI);
		if (!kPlayer.isEverAlive())
			continue;

		int iJ=-1;
		int iMultiplier = getPlayerScore(kPlayer.getID());
		// <advc.001n>
		/*	Would like checkInSync to set this before calling CvDLLUtilityIFaceBase::
			GetSyncOOS, but that doesn't work b/c, apparently, GetSyncOOS returns
			the most recently computed checksum instead of calling calculateSyncChecksum. */
		bool const bFullOOSCheck = false;
		std::vector<int> aiMultipliers;
		int const iCases = 8; // Originally 4, K-Mod added another 4.
		for (int k = 0; k < (bFullOOSCheck ? iCases : 1); k++)
		{
			switch (bFullOOSCheck ? k : // </advc.001n>
				(getTurnSlice() % iCases))
			{
			case 0:
				iMultiplier += (kPlayer.getTotalPopulation() * 543271);
				iMultiplier += (kPlayer.getTotalLand() * 327382);
				iMultiplier += (kPlayer.getGold() * 107564);
				iMultiplier += (kPlayer.getAssets() * 327455);
				iMultiplier += (kPlayer.getPower() * 135647);
				iMultiplier += (kPlayer.getNumCities() * 436432);
				iMultiplier += (kPlayer.getNumUnits() * 324111);
				iMultiplier += (kPlayer.getNumSelectionGroups() * 215356);
				break;

			case 1:
				for (iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
					iMultiplier += (kPlayer.calculateTotalYield((YieldTypes)iJ) * 432754);
				for (iJ = 0; iJ < NUM_COMMERCE_TYPES; iJ++)
					iMultiplier += (kPlayer.getCommerceRate((CommerceTypes)iJ) * 432789);
				break;

			case 2:
				for (iJ = 0; iJ < GC.getNumBonusInfos(); iJ++)
				{
					iMultiplier += (kPlayer.getNumAvailableBonuses((BonusTypes)iJ) * 945732);
					iMultiplier += (kPlayer.getBonusImport((BonusTypes)iJ) * 326443);
					iMultiplier += (kPlayer.getBonusExport((BonusTypes)iJ) * 932211);
				}
				for (iJ = 0; iJ < GC.getNumImprovementInfos(); iJ++)
					iMultiplier += (kPlayer.getImprovementCount((ImprovementTypes)iJ) * 883422);
				for (iJ = 0; iJ < GC.getNumBuildingClassInfos(); iJ++)
					iMultiplier += (kPlayer.getBuildingClassCountPlusMaking((BuildingClassTypes)iJ) * 954531);
				for (iJ = 0; iJ < GC.getNumUnitClassInfos(); iJ++)
					iMultiplier += (kPlayer.getUnitClassCountPlusMaking((UnitClassTypes)iJ) * 754843);
				for (iJ = 0; iJ < NUM_UNITAI_TYPES; iJ++)
					iMultiplier += (kPlayer.AI_totalUnitAIs((UnitAITypes)iJ) * 643383);
				break;

			case 3:
				FOR_EACH_UNIT(pLoopUnit, kPlayer)
				{
					iMultiplier += (pLoopUnit->getX() * 876543);
					iMultiplier += (pLoopUnit->getY() * 985310);
					iMultiplier += (pLoopUnit->getDamage() * 736373);
					iMultiplier += (pLoopUnit->getExperience() * 820622);
					iMultiplier += (pLoopUnit->getLevel() * 367291);
				}
				break;
			// K-Mod - new checks.
			case 4: // attitude cache
				// <advc.003n>
				if (iI == BARBARIAN_PLAYER)
					break; // </advc.003n>
				for (iJ = 0; iJ < MAX_CIV_PLAYERS; iJ++)
				{
					if (iI != iJ) // advc: self-attitude should never matter
						iMultiplier += kPlayer.AI_getAttitudeVal((PlayerTypes)iJ, false) << iJ;
				}
				// strategy hash
				//iMultiplier += kPlayer.AI_getStrategyHash() * 367291;
				break;
			case 5: // city religions and corporations
				FOR_EACH_CITY(pLoopCity, kPlayer)
				{
					for (iJ = 0; iJ < GC.getNumReligionInfos(); iJ++)
					{
						if (pLoopCity->isHasReligion((ReligionTypes)iJ))
							iMultiplier += pLoopCity->getID() * (iJ+1);
					}
					for (iJ = 0; iJ < GC.getNumCorporationInfos(); iJ++)
					{
						if (pLoopCity->isHasCorporation((CorporationTypes)iJ))
							iMultiplier += (pLoopCity->getID()+1) * (iJ+1);
					}
				}
				break;
			case 6: // city production
				/*FOR_EACH_CITY(pLoopCity, kPlayer) {
					CLLNode<OrderData>* pOrderNode = pLoopCity->headOrderQueueNode();
					if (pOrderNode != NULL)
						iMultiplier += pLoopCity->getID()*(pOrderNode->m_data.eOrderType+2*pOrderNode->m_data.iData1+3*pOrderNode->m_data.iData2+6);
				} break;*/
				// city health and happiness
				FOR_EACH_CITYAI(pLoopCity, kPlayer)
				{
					iMultiplier += pLoopCity->goodHealth() * 876543;
					iMultiplier += pLoopCity->badHealth() * 985310;
					iMultiplier += pLoopCity->happyLevel() * 736373;
					iMultiplier += pLoopCity->unhappyLevel() * 820622;
					iMultiplier += pLoopCity->getFood() * 367291;
					/*for (iJ = 0; iJ < MAX_PLAYERS; iJ++) {
						if (GET_PLAYER((PlayerTypes)iJ).isAlive()) {
							iMultiplier += (pLoopCity->AI_playerCloseness(
									(PlayerTypes)iJ, DEFAULT_PLAYER_CLOSENESS, true) + 1) * (iJ + 1);
						}
					}*/
					/*	<advc.001n> FloatingDefenders should be good enough as closeness
						factors into that */
					if (!kPlayer.isBarbarian())
						iMultiplier += pLoopCity->AI_neededFloatingDefenders(false, true) * 324111;
					// </advc.001n>
				}
				break;
			case 7: // city event history
				FOR_EACH_CITY(pLoopCity, kPlayer)
				{
					for (iJ = 0; iJ < GC.getNumEventInfos(); iJ++)
						iMultiplier += (iJ+1)*pLoopCity->isEventOccured((EventTypes)iJ);
				}
				break;
			// K-Mod end
			} // end TurnSlice switch
			// <advc.001n>
			aiMultipliers.push_back(iMultiplier);
		}
		if (bFullOOSCheck)
			iMultiplier = (scaled::hash(aiMultipliers) * scaled::MAX).floor();
		// </advc.001n>
		if (iMultiplier != 0)
			iValue *= iMultiplier;
	}
	return iValue;
}


int CvGame::calculateOptionsChecksum()
{
	//PROFILE_FUNC(); // advc.003o
	int iValue = 0;
	FOR_EACH_ENUM(Player)
	{
		FOR_EACH_ENUM(PlayerOption)
		{
			if (GET_PLAYER(eLoopPlayer).isOption(eLoopPlayerOption))
			{
				iValue += (eLoopPlayer * 943097);
				iValue += (eLoopPlayerOption * 281541);
			}
		}
	}
	return iValue;
}

// rfc
// TODO: used?
// TODO: refactor
bool CvGame::changePlayer( int playerIdx, int newCivType, int newLeader, int teamIdx, bool bIsHuman, bool bChangeGraphics )
{
	bool changedCivOrLeader = false;
	LeaderHeadTypes prevLeader = NO_LEADER;
	CvFlagEntity* newFlagSymbol = NULL;
	CvUnit* pLoopUnit;
	CvUnit* pNewUnit;
	int iLoop;
	TeamTypes prevTeam = GET_PLAYER((PlayerTypes)playerIdx).getTeam();

	if( playerIdx >= GC.getMAX_CIV_PLAYERS() )
	{
		//logMsg("Creating new player ... failed, invalid player index");
		return false;
	}
	if( !GET_PLAYER((PlayerTypes)playerIdx).isEverAlive() )
	{
		//logMsg("Changing player ... failed, player id never alive");
		return false;
	}
	if( newCivType >= GC.getNumCivilizationInfos() )
	{
		//logMsg("Creating new player ... failed, invalid civ type");
		return false;
	}
	if( newLeader >= GC.getNumLeaderHeadInfos() )
	{
		//logMsg("Creating new player ... failed, invalid leader type");
		return false;
	}
	if( teamIdx >= GC.getMAX_TEAMS() ) //( teamIdx >= GC.getMAX_CIV_TEAMS() )
	{
		//logMsg("Creating new player ... failed, invalid team index");
		return false;
	}

	//logMsg("Changing player ...");

	// Change whether this player is human
	if( bIsHuman )
	{
		if( GC.getInitCore().getSlotStatus( (PlayerTypes)playerIdx ) != SS_TAKEN )
			GC.getInitCore().setSlotStatus( (PlayerTypes)playerIdx, SS_TAKEN );
	}
	else
	{
		if( GC.getInitCore().getSlotStatus( (PlayerTypes)playerIdx ) == SS_TAKEN )
			GC.getInitCore().setSlotStatus( (PlayerTypes)playerIdx, SS_COMPUTER ); // or SS_OPEN?
	}

	// Change civ type
	if( (CivilizationTypes)newCivType != GC.getInitCore().getCiv((PlayerTypes)playerIdx) )
	{
		//logMsg("Changing civType");

		GC.getInitCore().setCiv((PlayerTypes)playerIdx, (CivilizationTypes)newCivType);

		changedCivOrLeader = true;
	}

	// Change Leader Head
	if( (LeaderHeadTypes)newLeader != GC.getInitCore().getLeader((PlayerTypes)playerIdx ) )
	{
		//logMsg("Changeing Leader");
		prevLeader = GC.getInitCore().getLeader((PlayerTypes)playerIdx );

		if( !GC.getCivilizationInfo( (CivilizationTypes)newCivType ).isLeaders( (LeaderHeadTypes)newLeader) )
		{
			//logMsg("WARNING: New leader not for this civ");
		}

		GC.getInitCore().setLeader((PlayerTypes)playerIdx, (LeaderHeadTypes)newLeader );
		GC.getInitCore().setLeaderName((PlayerTypes)playerIdx, GC.getLeaderHeadInfo((LeaderHeadTypes)newLeader).getDescription(0)); //Rhye

		changedCivOrLeader = true;
	}

	// Place on a different team?
	if( teamIdx >= 0 && (TeamTypes)teamIdx != prevTeam )
	{
		if( GET_TEAM(prevTeam).getNumMembers() == 1 )
		{
			GET_TEAM( (TeamTypes)teamIdx ).addTeam(prevTeam);
			gDLL->getInterfaceIFace()->setDirty(Fog_DIRTY_BIT, true);
			gDLL->getEngineIFace()->SetDirty(MinimapTexture_DIRTY_BIT, true);
			gDLL->getEngineIFace()->SetDirty(GlobeTexture_DIRTY_BIT, true);
			gDLL->getEngineIFace()->SetDirty(GlobePartialTexture_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(GlobeLayer_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(Foreign_Screen_DIRTY_BIT, true);
		}
		else
		{
			// This handles both changes to prev team and new team
			GET_PLAYER((PlayerTypes)playerIdx).setTeam((TeamTypes)teamIdx);
			gDLL->getInterfaceIFace()->setDirty(Fog_DIRTY_BIT, true);
			gDLL->getEngineIFace()->SetDirty(MinimapTexture_DIRTY_BIT, true);
			gDLL->getEngineIFace()->SetDirty(GlobeTexture_DIRTY_BIT, true);
			gDLL->getEngineIFace()->SetDirty(GlobePartialTexture_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(GlobeLayer_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(Foreign_Screen_DIRTY_BIT, true);
		}
	}

	// Update civs colors, artstyle, border colors, leader name on the score board, etc.
	// Current challenge is getting existing units to change their flag ...
	if( bChangeGraphics )
	{
		//logMsg("Changing player graphics");
		CivilizationTypes civType = GET_PLAYER((PlayerTypes)playerIdx).getCivilizationType();
		GC.getInitCore().setFlagDecal( (PlayerTypes)playerIdx, (CvWString)GC.getCivilizationInfo(civType).getFlagTexture() );
		GC.getInitCore().setColor( (PlayerTypes)playerIdx, (PlayerColorTypes)GC.getCivilizationInfo(civType).getDefaultPlayerColor() );
		GC.getInitCore().setArtStyle( (PlayerTypes)playerIdx, (ArtStyleTypes)GC.getCivilizationInfo(civType).getArtStyleType() );

		// Need to force redraw
		gDLL->getEngineIFace()->SetDirty(CultureBorders_DIRTY_BIT, true);
		gDLL->getEngineIFace()->SetDirty(MinimapTexture_DIRTY_BIT, true);
		gDLL->getEngineIFace()->SetDirty(GlobeTexture_DIRTY_BIT, true);
		gDLL->getEngineIFace()->SetDirty(GlobePartialTexture_DIRTY_BIT, true);

		gDLL->getInterfaceIFace()->setDirty(ColoredPlots_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(HighlightPlot_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(CityInfo_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(UnitInfo_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(InfoPane_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(GlobeLayer_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(Flag_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(MinimapSection_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(Foreign_Screen_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(SelectionSound_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(GlobeInfo_DIRTY_BIT, true);
/*
		//Change existing unit flags
		newFlagSymbol = gDLL->getFlagEntityIFace()->create((PlayerTypes)playerIdx);
		if( newFlagSymbol != NULL )
		{
			for(pLoopUnit = GET_PLAYER((PlayerTypes)playerIdx).firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = GET_PLAYER((PlayerTypes)playerIdx).nextUnit(&iLoop))
			{
				pLoopPlot = GC.getMapINLINE().plotINLINE(pLoopUnit->getX(),pLoopUnit->getY());
				//pLoopPlot->updateFlagSymbol();
				//gDLL->getFlagEntityIFace()->updateUnitInfo(newFlagSymbol, pLoopPlot);
			}
		}
		else
		{
			logMsg("New flag creation failed.");
		}
*/

		int numUnits = GET_PLAYER((PlayerTypes)playerIdx).getNumUnits();
		int i = 0;

		// Loop through players units, converting them
		for (pLoopUnit = GET_PLAYER((PlayerTypes)playerIdx).firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = GET_PLAYER((PlayerTypes)playerIdx).nextUnit(&iLoop))
		{
			// Concept borrowed from CvUnit::gift
			pNewUnit = GET_PLAYER((PlayerTypes)playerIdx).initUnit(pLoopUnit->getUnitType(), pLoopUnit->getX_INLINE(), pLoopUnit->getY_INLINE(), pLoopUnit->AI_getUnitAIType());
			// Will kill pLoopUnit
			pNewUnit->convert(pLoopUnit);

			char cArray[99];
			sprintf(cArray, "Converting unit type: %d", pNewUnit->getUnitType());
			//logMsg(cArray);

			// Without this, is infinite loop ...
			i++;
			if( i >= numUnits )
				break;
		}

	}

	// If civ or leader changed, need to update traits/personality/civ data
	if( changedCivOrLeader )
	{
		GET_PLAYER((PlayerTypes)playerIdx).reinit((PlayerTypes)playerIdx, prevLeader, false);
	}

	//logMsg("Player change complete");

	return true;
}

// rfc
// TODO: used?
// TODO: refctor
void CvGame::convertUnits( int playerIdx )
{
	CvUnit* pLoopUnit;
	CvUnit* pNewUnit;
	int iLoop;
	int numUnits = GET_PLAYER((PlayerTypes)playerIdx).getNumUnits();
	int i = 0;

	// Loop through players units, converting them
	for (pLoopUnit = GET_PLAYER((PlayerTypes)playerIdx).firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = GET_PLAYER((PlayerTypes)playerIdx).nextUnit(&iLoop))
	{
		// Concept borrowed from CvUnit::gift
		pNewUnit = GET_PLAYER((PlayerTypes)playerIdx).initUnit(pLoopUnit->getUnitType(), pLoopUnit->getX_INLINE(), pLoopUnit->getY_INLINE(), pLoopUnit->AI_getUnitAIType());
		// Will kill pLoopUnit
		pNewUnit->convert(pLoopUnit);

		char cArray[99];
		sprintf(cArray, "Converting unit type: %d", pNewUnit->getUnitType());
		//logMsg(cArray);

		// Without this, is infinite loop ...
		i++;
		if( i >= numUnits )
			break;
	}
}
// Rhye - end (jdog)

// advc.001n:
bool CvGame::checkInSync()
{
	if (!isNetworkMultiPlayer())
		return true;

	int iSyncHash = gDLL->GetSyncOOS(GET_PLAYER(getActivePlayer()).getNetID());
	for (int i = 0; i < MAX_CIV_PLAYERS; i++)
	{
		CvPlayer const& kOther = GET_PLAYER((PlayerTypes)i);
		if (kOther.isAlive() && kOther.getID() != getActivePlayer() &&
			(kOther.isHuman() || kOther.isHumanDisabled()))
		{
			int iOtherSyncHash = gDLL->GetSyncOOS(kOther.getNetID());
			if (iOtherSyncHash != iSyncHash)
			{
				FAssert(iOtherSyncHash == iSyncHash);
				setAIAutoPlay(0);
				return false;
			}
		}
	}
	return true;
}

/*	<advc.003g> Test the platform's floating point behavior (intermediate precision
	and/or rounding). */
int CvGame::FPChecksum() const
{
	/*	I've used this together with the _controlfp call at the end to test the
		error message in doFPCheck (i.e. for testing the test) */
	/*if (getActivePlayer() == 0)
		_controlfp(_PC_64, _MCW_PC);*/

	// Test 1: based on stackoverflow.com/questions/14749929/c-float-operations-have-different-results-on-i386-and-arm-but-why
	float x = 4.80000019f;
	int result1 = (int)(38000 / x + 10000 / x);
	result1 -= 9995;
	FAssert(result1 == 4 || result1 == 5);
	// Test 2: based on stackoverflow.com/questions/11832428/windows-intel-and-ios-arm-differences-in-floating-point-calculations
	x = (-5.241729736328125f * 94.37158203125f) - (-7.25933837890625f * 68.14253997802734f);
	int result2 = fmath::round(-10000.0 * x);
	FAssert(result2 == 5 || result2 == 6);

	/*if (getActivePlayer()==0)
		_controlfp(_PC_24, _MCW_PC);*/

	return 10 * result1 + result2; // Fold them into a single return value
	// (I'm sure there are simpler and more reliable ways to test FP behavior ...)
}


void CvGame::doFPCheck(int iChecksum, PlayerTypes ePlayer)
{
	if (m_bFPTestDone)
		return;
	m_bFPTestDone = true;
	if (iChecksum == FPChecksum())
		return; // Active player is able to reproduce checksum received over the net

	gDLL->UI().addMessage(getActivePlayer(), true, -1,
			CvWString::format(L"Your machine's FP test computation has yielded a"
			L" different result than that of %s. The game may frequently go"
			L" out of sync due to floating point calculations in the AdvCiv mod.",
			GET_PLAYER(ePlayer).getName()), NULL, MESSAGE_TYPE_MAJOR_EVENT, NULL,
			GC.getColorType("WARNING_TEXT"));
} // </advc.003g

// advc.003r:
void CvGame::handleUpdateTimer(UpdateTimerTypes eTimerType)
{
	if (m_aiUpdateTimers[eTimerType] < 0)
		return;

	if (m_aiUpdateTimers[eTimerType] == 0)
	{
		switch (eTimerType)
		{
		// <advc.085>
		case UPDATE_COLLAPSE_SCORE_BOARD:
			GET_PLAYER(getActivePlayer()).setScoreboardExpanded(false);
			break;
		case UPDATE_DIRTY_SCORE_HELP:
			gDLL->getInterfaceIFace()->setDirty(ScoreHelp_DIRTY_BIT, true);
			break; // </advc.085>
		// <advc.001w>
		case UPDATE_MOUSE_FOCUS:
			gDLL->getInterfaceIFace()->makeSelectionListDirty();
			break; // </advc.001w>
		// <advc.004j>
		case UPDATE_LOOK_AT_STARTING_PLOT:
		{
			CvPlot* pStartingPlot = GET_PLAYER(getActivePlayer()).getStartingPlot();
			if (pStartingPlot != NULL)
				gDLL->getInterfaceIFace()->lookAt(pStartingPlot->getPoint(), CAMERALOOKAT_NORMAL);
			break;
		} // </advc.004j>
		// advc.106n:
		case UPDATE_STORE_REPLAY_TEXTURE: GC.getMap().updateReplayTexture(); break;
		// advc.001:
		case UPDATE_REBUILD_PLOTS: gDLL->getEngineIFace()->RebuildAllPlots(); break;
		default: FErrorMsg("Unknown update timer type");
		}
	}
	m_aiUpdateTimers[eTimerType]--;
}


void CvGame::addReplayMessage(ReplayMessageTypes eType, PlayerTypes ePlayer,
	CvWString szText, ColorTypes eColor, int iPlotX, int iPlotY)
{
	int iGameTurn = getGameTurn();
	CvReplayMessage* pMessage = new CvReplayMessage(iGameTurn, eType, ePlayer);
	pMessage->setPlot(iPlotX, iPlotY);
	pMessage->setText(szText);
	if (NO_COLOR == eColor)
		eColor = GC.getColorType("WHITE");
	pMessage->setColor(eColor);
	m_listReplayMessages.push_back(pMessage);
}

// advc: Wrapper with CvPlot param
void CvGame::addReplayMessage(CvPlot const& kPlot, ReplayMessageTypes eType,
	PlayerTypes ePlayer, CvWString szText, ColorTypes eColor)
{
	addReplayMessage(eType, ePlayer, szText, eColor, kPlot.getX(), kPlot.getY());
}


void CvGame::clearReplayMessageMap()
{
	for (ReplayMessageList::iterator itList = m_listReplayMessages.begin();
		itList != m_listReplayMessages.end(); ++itList)
	{
		SAFE_DELETE(*itList);
	}
	m_listReplayMessages.clear();
}


// advc: To get rid of some duplicate code
bool CvGame::isValidReplayIndex(uint i) const
{
	if (i >= m_listReplayMessages.size())
		return false;
	CvReplayMessage const* pMessage = m_listReplayMessages[i];
	if (pMessage == NULL)
		return false;
	return true;
}


int CvGame::getReplayMessageTurn(uint i) const
{
	return (isValidReplayIndex(i) ? m_listReplayMessages[i]->getTurn() : -1);
}


ReplayMessageTypes CvGame::getReplayMessageType(uint i) const
{
	return (isValidReplayIndex(i) ? m_listReplayMessages[i]->getType() : NO_REPLAY_MESSAGE);
}

int CvGame::getReplayMessagePlotX(uint i) const
{
	return (isValidReplayIndex(i) ? m_listReplayMessages[i]->getPlotX() : INVALID_PLOT_COORD);
}


int CvGame::getReplayMessagePlotY(uint i) const
{
	return (isValidReplayIndex(i) ? m_listReplayMessages[i]->getPlotY() : INVALID_PLOT_COORD);
}


PlayerTypes CvGame::getReplayMessagePlayer(uint i) const
{
	return (isValidReplayIndex(i) ? m_listReplayMessages[i]->getPlayer() : NO_PLAYER);
}


LPCWSTR CvGame::getReplayMessageText(uint i) const
{
	return (isValidReplayIndex(i) ? m_listReplayMessages[i]->getText().GetCString() : NULL);
}


ColorTypes CvGame::getReplayMessageColor(uint i) const
{
	return (isValidReplayIndex(i) ? m_listReplayMessages[i]->getColor() : NO_COLOR);
}


uint CvGame::getNumReplayMessages() const
{
	return m_listReplayMessages.size();
}


void CvGame::read(FDataStreamBase* pStream)
{
	reset(NO_HANDICAP);

	uint uiFlag=0;
	pStream->Read(&uiFlag);
	/*	advc: So that onAllGameDataRead can perform some final updates
		based on the save version */
	m_uiSaveFlag = uiFlag;
	if (uiFlag < 1)
	{
		int iEndTurnMessagesSent;
		pStream->Read(&iEndTurnMessagesSent);
	}
	pStream->Read(&m_iElapsedGameTurns);
	pStream->Read(&m_iStartTurn);
	pStream->Read(&m_iStartYear);
	pStream->Read(&m_iEstimateEndTurn);
	pStream->Read(&m_iTurnSlice);
	pStream->Read(&m_iCutoffSlice);
	pStream->Read(&m_iNumGameTurnActive);
	pStream->Read(&m_iNumCities);
	pStream->Read(&m_iTotalPopulation);
	pStream->Read(&m_iTradeRoutes);
	pStream->Read(&m_iFreeTradeCount);
	pStream->Read(&m_iNoNukesCount);
	pStream->Read(&m_iNukesExploded);
	pStream->Read(&m_iMaxPopulation);
	pStream->Read(&m_iMaxLand);
	pStream->Read(&m_iMaxTech);
	pStream->Read(&m_iMaxWonders);
	pStream->Read(&m_iInitPopulation);
	pStream->Read(&m_iInitLand);
	pStream->Read(&m_iInitTech);
	pStream->Read(&m_iInitWonders);
    pStream->Read(&m_iAIAutoPlay);
    pStream->Read(&m_iCircumnavigated); // rfc
    pStream->Read(&m_iMedianTechValue); // doc
	// <advc.127> allGameDataRead will handle it properly
	if (m_iAIAutoPlay != 0)
		m_iAIAutoPlay = -1; // </advc.127>
	pStream->Read(&m_iGlobalWarmingIndex); // K-Mod
	pStream->Read(&m_iGwEventTally); // K-Mod
	pStream->Read(&m_iCivPlayersEverAlive);
	pStream->Read(&m_iCivTeamsEverAlive);
	// m_uiInitialTime not saved

	pStream->Read(&m_bScoreDirty);
	pStream->Read(&m_bCircumnavigated);
	// m_bDebugMode not saved
	pStream->Read(&m_bFinalInitialized);
	// m_bPbemTurnSent not saved
	pStream->Read(&m_bHotPbemBetweenTurns);
	// m_bPlayerOptionsSent not saved
	pStream->Read(&m_bNukesValid);

	pStream->Read((int*)&m_eHandicap);
	pStream->Read((int*)&m_eAIHandicap); // advc.127
	pStream->Read((int*)&m_ePausePlayer);
	pStream->Read((int*)&m_eBestLandUnit);
	pStream->Read((int*)&m_eWinner);
	pStream->Read((int*)&m_eVictory);
    pStream->Read((int*)&m_eGameState);
    pStream->Read((int*)&m_eCityScreenOwner); // doc // TODO: needs to be saved?
    pStream->Read((int*)&m_eGreatPeopleNotifications); // doc
    pStream->Read((int*)&m_eReligionSpreadNotifications); // doc
    pStream->Read((int*)&m_eEventEffectNotifications); // doc
	// <advc.106h>
	pStream->Read((int*)&m_eInitialActivePlayer);
	else m_eInitialActivePlayer = getActivePlayer(); // </advc.106h>
	// <advc.004m>
	pStream->Read((int*)&m_eCurrentLayer);
	/*	Initial autosave doesn't contain valid info about the globe layers
			b/c it gets created before Python calls reportCurrentLayer */
	if (getTurnSlice() > 0)
		m_bLayerFromSavegame = true;
	} // </advc.004m>
	pStream->ReadString(m_szScriptData);


	m_aeRankPlayer.read(pStream);
	m_aePlayerRank.read(pStream);
	m_aiPlayerScore.read(pStream);
	m_aeRankTeam.read(pStream);
	m_aeTeamRank.read(pStream);
	m_aiTeamScore.read(pStream);
    // TODO: refactor
    pStream->Read(NUM_CIVS, m_aiCivPeriod); // doc
    pStream->Read(MAX_TEAMS, m_aiTechRankTeam); // doc
	m_aiUnitCreatedCount.read(pStream);
	m_aiUnitClassCreatedCount.read(pStream);
	m_aiBuildingClassCreatedCount.read(pStream);
	m_aiProjectCreatedCount.read(pStream);
	m_aiForceCivicCount.read(pStream);
	m_aiVoteOutcome.read(pStream);
	m_aiReligionGameTurnFounded.read(pStream);
	m_aiCorporationGameTurnFounded.read(pStream);
	m_aiSecretaryGeneralTimer.read(pStream);
	m_aiVoteTimer.read(pStream);
	m_aiDiploVote.read(pStream);
	m_abSpecialUnitValid.read(pStream);
	m_abSpecialBuildingValid.read(pStream);
	m_abReligionSlotTaken.read(pStream);
	m_aeHolyCity.read(pStream);
    m_aeHeadquarters.read(pStream);
    // TODO: refactor
    pStream->Read(GC.getNumTechInfos(), m_aiFirstDiscovered); // doc
    pStream->Read(GC.getNumTechInfos(), m_aiFirstDiscoveredTurn); // doc

	{
		CvWString szBuffer;
		uint iSize;

		m_aszDestroyedCities.clear();
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			pStream->ReadString(szBuffer);
			m_aszDestroyedCities.push_back(szBuffer);
		}

		m_aszGreatPeopleBorn.clear();
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			pStream->ReadString(szBuffer);
			m_aszGreatPeopleBorn.push_back(szBuffer);
		}
	}

	ReadStreamableFFreeListTrashArray(m_deals, pStream);
	ReadStreamableFFreeListTrashArray(m_voteSelections, pStream);
	ReadStreamableFFreeListTrashArray(m_votesTriggered, pStream);

	m_mapRand.read(pStream);
	m_sorenRand.read(pStream);
	// <advc.027b>
	pStream->Read(&m_initialRandSeed.uiMap);
	pStream->Read(&m_initialRandSeed.uiSync);
	// <advc.tsl>, advc.701: Options have been shuffled around a few times
	bool bNewSeed = isOption((GameOptionTypes)
			(uiFlag < 2 || uiFlag >= 17 ? 17 : 19));
	bool bLockMods = isOption((GameOptionTypes)
			(uiFlag >= 15 && uiFlag < 17 ? 27 : 18));
	bool bNoVassals = isOption((GameOptionTypes)
			(uiFlag >= 17 ? 23 : 20));
	bool bNoEspionage = isOption((GameOptionTypes)
			(uiFlag >= 17 ? 27 : 23));
	bool bRiseFall = isOption((GameOptionTypes)
			(uiFlag < 2 ? false : (uiFlag < 17 ? 17 : 19)));
	bool bTrueStarts = isOption((GameOptionTypes)
			(uiFlag < 15 ? false : (uiFlag < 17 ? 18 : 20)));
	setOption(GAMEOPTION_NEW_RANDOM_SEED, bNewSeed);
	setOption(GAMEOPTION_LOCK_MODS, bLockMods);
	setOption(GAMEOPTION_RISE_FALL, bRiseFall);
	setOption(GAMEOPTION_TRUE_STARTS, bTrueStarts);
	setOption(GAMEOPTION_NO_VASSAL_STATES, bNoVassals);
	setOption(GAMEOPTION_NO_ESPIONAGE, bNoEspionage);
	// </advc.tsl>
	// <advc.250b>
	if (isOption(GAMEOPTION_SPAH))
		m_pSpah->read(pStream); // </advc.250b>
	// <advc.701>
	if (isOption(GAMEOPTION_RISE_FALL))
		m_pRiseFall->read(pStream); // </advc.701>
	{
		clearReplayMessageMap();
		ReplayMessageList::_Alloc::size_type iSize;
		pStream->Read(&iSize);
		for (ReplayMessageList::_Alloc::size_type i = 0; i < iSize; i++)
		{
			CvReplayMessage* pMessage = new CvReplayMessage(0);
			if (pMessage != NULL)
				pMessage->read(*pStream);
			m_listReplayMessages.push_back(pMessage);
		}
	}
	// m_pReplayInfo not saved

	pStream->Read(&m_iNumSessions);
	// <advc.tsl>
	pStream->Read(&m_iMapRegens); // </advc.tsl>
	if (!isNetworkMultiPlayer())
		m_iNumSessions++;
	/*	<advc.enum> In part based on code from obsolete structs
		PlotExtraYield, PlotExtraCost. */
	CvMap& kMap = GC.getMap();
	/*	Map hasn't yet been reset and won't reset the plot extra data at all
		when loading a legacy save. It's all up to CvGame then. */
	kMap.resetPlotExtraData();
	int iSize;
	pStream->Read(&iSize);
	for (int i = 0; i < iSize; i++)
	{
		int iX, iY;
		pStream->Read(&iX);
		pStream->Read(&iY);
		FOR_EACH_ENUM(Yield)
		{
			int iChange;
			pStream->Read(&iChange);
			kMap.setPlotExtraYield(kMap.plotNum(iX, iY), eLoopYield, iChange);
		}
	}
	pStream->Read(&iSize);
	for (int i = 0; i < iSize; i++)
	{
		int iX, iY, iCost;
		pStream->Read(&iX);
		pStream->Read(&iY);
		pStream->Read(&iCost);
		kMap.changePlotExtraCost(kMap.plotNum(iX, iY), iCost);
	}
	// <advc>
	m_aeVoteSourceReligion.read(pStream);
	if (!isOption(GAMEOPTION_NO_EVENTS))
	{
		m_abInactiveTriggers.read(pStream);
	}

	// Get the active player information from the initialization structure
	if (!isGameMultiPlayer())
	{
		FOR_EACH_ENUM(Player)
		{
			if (GET_PLAYER(eLoopPlayer).isHuman())
			{
				setActivePlayer(eLoopPlayer);
				break;
			}
		}
		addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, getActivePlayer(),
				gDLL->getText("TXT_KEY_MISC_RELOAD", m_iNumSessions));
	}

	if (isOption(GAMEOPTION_NEW_RANDOM_SEED))
	{
		if (!isNetworkMultiPlayer() &&
			!GC.getDefineBOOL("IGNORE_NEW_RANDOM_SEED_OPTION")) // advc
		{
			m_sorenRand.reseed(timeGetTime());
		}
	}
	pStream->Read(&m_iNumCultureVictoryCities);
	pStream->Read((int*)&m_eCultureVictoryCultureLevel);

    // doc: read civ history entries
    // TODO: refactor
    for (iI = 0; iI < NUM_HISTORY_TYPES; iI++)
    {
        m_aiCivilizationHistory[iI].clear();

        int iNumHistoryEntries;
        pStream->Read(&iNumHistoryEntries);

        for (int iJ = 0; iJ < iNumHistoryEntries; iJ++)
        {
            int iCivilization;
            pStream->Read(&iCivilization);

            int iNumCivilizationEntries;
            pStream->Read(&iNumCivilizationEntries);

            for (int iK = 0; iK < iNumCivilizationEntries; iK++)
            {
                int iTurn;
                int iValue;
                pStream->Read(&iTurn);
                pStream->Read(&iValue);

                setCivilizationHistory((HistoryTypes)iI, (CivilizationTypes)iCivilization, iTurn, iValue);
            }
        }
    }

	// <advc.052>
	pStream->Read(&m_bScenario); // </advc.052>
	m_iTurnLoadedFromSave = m_iElapsedGameTurns; // advc.044
	GAMETEXT.setAlwaysShowPlotCulture(uiFlag >= 10); // advc.099f
	applyOptionEffects(); // advc.310
	m_bFPTestDone = !isNetworkMultiPlayer(); // advc.003g
}


void CvGame::write(FDataStreamBase* pStream)
{
	PROFILE_FUNC(); // advc
	uint uiFlag;
	//uiFlag = 1; // BtS
	//uiFlag = 2; // advc.701: R&F option
	//uiFlag = 3; // advc.052
	//uiFlag = 4; // advc.opt: Players and teams ever alive
	//uiFlag = 5; // advc.004m
	//uiFlag = 6; // advc.106h
	//uiFlag = 7; // advc.027b
	//uiFlag = 8; // advc.172
	//uiFlag = 9; // advc (m_aeVoteSourceReligion)
	//uiFlag = 10; // advc.099f
	//uiFlag = 11; // advc.enum: new enum map save behavior
	//uiFlag = 12; // advc.130n: DifferentReligionThreat added to CvPlayerAI
	//uiFlag = 13; // advc.148: RELATIONS_THRESH_WORST_ENEMY
	//uiFlag = 14; // advc.148, advc.130n, advc.130x (religion attitude)
	//uiFlag = 15; // advc.tsl: new game option
	//uiFlag = 16; // advc.tsl: map regen counter
	//uiFlag = 17; // advc.tsl: game options moved around
	//uiFlag = 18; // advc.130c: change in rank hate calc
	//uiFlag = 19; // advc.500c: Update citizen assignments
	//uiFlag = 20; // advc.130r: Update war attitude
	//uiFlag = 21; // advc.enum
	//uiFlag = 22; // advc.130n: Bugfix in fave-civic attitude calc
	//uiFlag = 23; // advc.124b: Need a plot group update for compatibility
	/*	advc.enum: Bugfix in bool-valued ArrayEnumMap; advc.130c: tweak;
		advc.130n: fave civic based on displayed leader type. */
	//uiFlag = 24;
	//uiFlag = 25; // advc.130n (bugfix)
	//uiFlag = 26; // advc.130w: Cache for expansionist hate
	uiFlag = 27; // advc.130w: RivalVassalAttitude tweak
	pStream->Write(uiFlag);
	REPRO_TEST_BEGIN_WRITE("Game pt1");
	pStream->Write(m_iElapsedGameTurns);
	pStream->Write(m_iStartTurn);
	pStream->Write(m_iStartYear);
	pStream->Write(m_iEstimateEndTurn);
	REPRO_TEST_END_WRITE(); // Skip TurnSlice
	pStream->Write(m_iTurnSlice);
	pStream->Write(m_iCutoffSlice);
	pStream->Write(m_iNumGameTurnActive);
	REPRO_TEST_BEGIN_WRITE("Game pt2");
	pStream->Write(m_iNumCities);
	pStream->Write(m_iTotalPopulation);
	pStream->Write(m_iTradeRoutes);
	pStream->Write(m_iFreeTradeCount);
	pStream->Write(m_iNoNukesCount);
	pStream->Write(m_iNukesExploded);
	pStream->Write(m_iMaxPopulation);
	pStream->Write(m_iMaxLand);
	pStream->Write(m_iMaxTech);
	pStream->Write(m_iMaxWonders);
	pStream->Write(m_iInitPopulation);
	pStream->Write(m_iInitLand);
	pStream->Write(m_iInitTech);
	pStream->Write(m_iInitWonders);
    pStream->Write(m_iAIAutoPlay);
    pStream->Write(m_iCircumnavigated); // rfc
    pStream->Write(m_iMedianTechValue); // doc
	pStream->Write(m_iGlobalWarmingIndex); // K-Mod
	pStream->Write(m_iGwEventTally); // K-Mod
	// <advc.opt>
	pStream->Write(m_iCivPlayersEverAlive);
	pStream->Write(m_iCivTeamsEverAlive);
	// </advc.opt>
	// m_uiInitialTime not saved

	pStream->Write(m_bScoreDirty);
	pStream->Write(m_bCircumnavigated);
	// m_bDebugMode not saved
	pStream->Write(m_bFinalInitialized);
	// m_bPbemTurnSent not saved
	pStream->Write(m_bHotPbemBetweenTurns);
	// m_bPlayerOptionsSent not saved
	pStream->Write(m_bNukesValid);

	pStream->Write(m_eHandicap);
	pStream->Write(m_eAIHandicap); // advc.127
	pStream->Write(m_ePausePlayer);
	pStream->Write(m_eBestLandUnit);
	pStream->Write(m_eWinner);
	pStream->Write(m_eVictory);
    pStream->Write(m_eGameState);
    pStream->Write(m_eCityScreenOwner); // doc // TODO: needs to be saved?
    pStream->Write(m_eGreatPeopleNotifications); // doc
    pStream->Write(m_eReligionSpreadNotifications); // doc
    pStream->Write(m_eEventEffectNotifications); // doc
	pStream->Write(m_eInitialActivePlayer); // advc.106h
	pStream->Write(m_eCurrentLayer); // advc.004m

	pStream->WriteString(m_szScriptData);

	m_aeRankPlayer.write(pStream);
	m_aePlayerRank.write(pStream);
	m_aiPlayerScore.write(pStream);
	m_aeRankTeam.write(pStream);
	m_aeTeamRank.write(pStream);
	m_aiTeamScore.write(pStream);
    // TODO: refactor
	pStream->Write(NUM_CIVS, m_aiCivPeriod); // doc
	pStream->Write(MAX_TEAMS, m_aiTechRankTeam); // doc
	m_aiUnitCreatedCount.write(pStream);
	m_aiUnitClassCreatedCount.write(pStream);
	m_aiBuildingClassCreatedCount.write(pStream);
	m_aiProjectCreatedCount.write(pStream);
	m_aiForceCivicCount.write(pStream);
	m_aiVoteOutcome.write(pStream);
	m_aiReligionGameTurnFounded.write(pStream);
	m_aiCorporationGameTurnFounded.write(pStream);
	m_aiSecretaryGeneralTimer.write(pStream);
	m_aiVoteTimer.write(pStream);
	m_aiDiploVote.write(pStream);
	m_abSpecialUnitValid.write(pStream);
	m_abSpecialBuildingValid.write(pStream);
	m_abReligionSlotTaken.write(pStream);
	m_aeHolyCity.write(pStream);
    m_aeHeadquarters.write(pStream);
    // TODO: refactor
    pStream->Write(GC.getNumTechInfos(), m_aiFirstDiscovered); // doc
    pStream->Write(GC.getNumTechInfos(), m_aiFirstDiscoveredTurn); // doc
	{
		std::vector<CvWString>::iterator it;
		pStream->Write(m_aszDestroyedCities.size());
		for (it = m_aszDestroyedCities.begin(); it != m_aszDestroyedCities.end(); ++it)
		{
			pStream->WriteString(*it);
		}

		pStream->Write(m_aszGreatPeopleBorn.size());
		for (it = m_aszGreatPeopleBorn.begin(); it != m_aszGreatPeopleBorn.end(); ++it)
		{
			pStream->WriteString(*it);
		}
	}
	REPRO_TEST_END_WRITE();
	WriteStreamableFFreeListTrashArray(m_deals, pStream);
	REPRO_TEST_BEGIN_WRITE("Game pt3");
	WriteStreamableFFreeListTrashArray(m_voteSelections, pStream);
	WriteStreamableFFreeListTrashArray(m_votesTriggered, pStream);
	REPRO_TEST_END_WRITE();
	REPRO_TEST_BEGIN_WRITE("SyncRNGs");
	m_mapRand.write(pStream);
	m_sorenRand.write(pStream);
	// <advc.027b>
	pStream->Write(m_initialRandSeed.uiMap);
	pStream->Write(m_initialRandSeed.uiSync); // </advc.027b>
	REPRO_TEST_END_WRITE();
	// <advc.250b>
	if (isOption(GAMEOPTION_SPAH))
		m_pSpah->write(pStream); // </advc.250b>
	// <advc.701>
	if (isOption(GAMEOPTION_RISE_FALL))
		m_pRiseFall->write(pStream); // </advc.701>
	ReplayMessageList::_Alloc::size_type iSize = m_listReplayMessages.size();
	pStream->Write(iSize);
	for (ReplayMessageList::const_iterator it = m_listReplayMessages.begin();
		it != m_listReplayMessages.end(); ++it)
	{
		const CvReplayMessage* pMessage = *it;
		if (pMessage != NULL)
			pMessage->write(*pStream);
	}
	// m_pReplayInfo not saved
	pStream->Write(m_iNumSessions);
	/*	advc.tsl: Doesn't really have to be saved so far, but might become
		useful in the future. */
	pStream->Write(m_iMapRegens);
	REPRO_TEST_BEGIN_WRITE("Game pt3"); // (skip replay messages, sessions)

	// (advc.enum: Plot extra data now handled by CvMap)

	m_aeVoteSourceReligion.write(pStream); // advc
	/*	advc.003v: Important not to write this enum map when events are disabled
		b/c the number of triggers may then be 0 (if event XML not loaded). */
	if (!isOption(GAMEOPTION_NO_EVENTS))
		m_abInactiveTriggers.write(pStream);

	pStream->Write(m_iNumCultureVictoryCities);
	pStream->Write(m_eCultureVictoryCultureLevel);

    // doc: civ history graph
    // TODO: refactor
    for (iI = 0; iI < NUM_HISTORY_TYPES; iI++)
    {
        hash_map<int, hash_map<int, int> > history = m_aiCivilizationHistory[iI];

        int iNumHistoryEntries = history.size();
        pStream->Write(iNumHistoryEntries);

        hash_map<int, hash_map<int, int> >::iterator historyIt;
        for (historyIt = history.begin(); historyIt != history.end(); historyIt++)
        {
            hash_map<int, int> entries = historyIt->second;

            int iNumCivilizationEntries = entries.size();
            pStream->Write(historyIt->first);
            pStream->Write(iNumCivilizationEntries);

            hash_map<int, int>::iterator entriesIt;
            for (entriesIt = entries.begin(); entriesIt != entries.end(); entriesIt++)
            {
                pStream->Write(entriesIt->first);
                pStream->Write(entriesIt->second);
            }
        }
    }

	pStream->Write(m_bScenario); // advc.052
	REPRO_TEST_END_WRITE();
}

void CvGame::writeReplay(FDataStreamBase& stream, PlayerTypes ePlayer)
{
	GET_PLAYER(ePlayer).setSavingReplay(false); // advc.106i
	SAFE_DELETE(m_pReplayInfo);
	m_pReplayInfo = new CvReplayInfo();
	if (m_pReplayInfo)
	{
		m_pReplayInfo->createInfo(ePlayer);
		// <advc.707>
		if (isOption(GAMEOPTION_RISE_FALL))
			m_pReplayInfo->setFinalScore(m_pRiseFall->getFinalRiseScore());
		// </advc.707>
		m_pReplayInfo->write(stream);
	}
}

/*	advc: When loading a savegame, this function is called once all
	read functions have been called. */
void CvGame::onAllGameDataRead()
{
	// <advc.opt> Savegame compatibility (uiFlag<4)
	if (m_iCivPlayersEverAlive == 0)
		m_iCivPlayersEverAlive = countCivPlayersEverAlive();
	if (m_iCivTeamsEverAlive == 0)
		m_iCivTeamsEverAlive = countCivTeamsEverAlive();
	// </advc.opt>
	GC.getAgents().gameStart(true); // advc.agent
	// <advc.250a> Cf. CvInitCore::read
	if (m_uiSaveFlag <= 1)
	{
		if (getHandicapType() >= GC.getNumHandicapInfos())
		{
			setHandicapType(GET_PLAYER(getActivePlayer()).getHandicapType());
			initGameHandicap();
		}
	} // </advc.250a>
	// <advc.124b> River connection rules have changed
	if (m_uiSaveFlag <= 23)
		updatePlotGroups(); // </advc.124b>
	// <advc.003m>
	for (TeamIter<> it; it.hasNext(); ++it)
	{
		if (it->getNumWars() < 0 || it->getNumWars(false, false) < 0 ||
			it->getNumWars(true, true) < 0)
		{
			it->finalizeInit();
		}
	} // </advc.003m>  <advc.opt>
	for (TeamAIIter<> it; it.hasNext(); ++it)
	{
		FOR_EACH_ENUM(WarPlan)
		{
			if (it->AI_getNumWarPlans(eLoopWarPlan) < 0)
			{
				it->AI_finalizeInit();
				break;
			}
		}
	} // </advc.opt>
	m_bAllGameDataRead = true;
	// <advc.enum>
	if (m_uiSaveFlag < 21)
	{
		for (int i = 0; i < 7; i++)
		{
			CvCity const* pCity = getCity(m_pLegacyOrgSeatData[i]);
			if (pCity != NULL)
				m_aeHolyCity.set((ReligionTypes)i, pCity->plotNum());
		}
		for (int i = 7; i < 14; i++)
		{
			CvCity const* pCity = getCity(m_pLegacyOrgSeatData[i]);
			if (pCity != NULL)
				m_aeHeadquarters.set((CorporationTypes)(i - 7), pCity->plotNum());
		}
		SAFE_DELETE_ARRAY(m_pLegacyOrgSeatData);
	} // </advc.enum>
	// <advc.251> Maintenance changed in XML
	if (m_uiSaveFlag < 25)
	{
		for (PlayerIter<ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
			itPlayer->updateMaintenance();
	} // </advc.251>
	// <advc.130w>
	bool bAttitudeUpdated = false;
	if (m_uiSaveFlag < 26)
	{
		for (PlayerAIIter<MAJOR_CIV> itPlayer; itPlayer.hasNext(); ++itPlayer)
			itPlayer->AI_updateExpansionistHate();
		bAttitudeUpdated = true;
	} // </advc.130w>
	// <advc.130n>, advc.148, advc.130r, advc.130x, advc.130c, advc.130w
	if (m_uiSaveFlag < 27 ||
		// <advc.127> Save created during AI Auto Play
		(m_iAIAutoPlay != 0 && !isNetworkMultiPlayer()))
	{
		m_iAIAutoPlay = 0; // </advc.127>
		if (!bAttitudeUpdated) // advc.130w
			CvPlayerAI::AI_updateAttitudes();
	} // </advc.130n>
	// <advc.500c>
	if (m_uiSaveFlag < 19)
	{
		TechTypes eNationalism = (TechTypes)GC.getInfoTypeForString("TECH_NATIONALISM");
		if (eNationalism != NO_TECH)
		{
			for (PlayerIter<ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
			{
				if (GET_TEAM(itPlayer->getTeam()).isHasTech(eNationalism))
				{
					FOR_EACH_CITY_VAR(pCity, *itPlayer)
					{
						if (pCity->getMilitaryHappinessUnits() <= 0)
							pCity->AI_setAssignWorkDirty(true);
					}
				}
			}
		}
	} // </advc.500c>
	// <advc.172>
	if (m_uiSaveFlag < 8)
	{
		for (PlayerIter<ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
		{
			FOR_EACH_CITY_VAR(pCity, *itPlayer)
				pCity->updateReligionCommerce();
		}
	} // </advc.172>
	// <advc.134a>
	for (PlayerIter<HUMAN> itActive; itActive.hasNext(); ++itActive)
	{
		if (itActive->isTurnActive())
			itActive->validateDiplomacy();
	} // </advc.134a>
}

/*	advc: Called once the EXE signals that graphics have been initialized
	(w/e that means exactly) */
void CvGame::onGraphicsInitialized()
{
	// advc.095:
	setCityBarWidth(BUGOption::isEnabled("MainInterface__WideCityBars", false));
	/*	<advc.001> After loading, the camera tries to center on some unit
		(apparently; I don't know where that's implemented). If there is
		none, it seems to center on some random(?) unrevealed tile. */
	if (GET_PLAYER(getActivePlayer()).getNumUnits() == 0)
		setUpdateTimer(UPDATE_LOOK_AT_STARTING_PLOT, 1);
	// </advc.001>
	GC.getPythonCaller()->callScreenFunction("updateCameraStartDistance"); // advc.004m
}


void CvGame::saveReplay(PlayerTypes ePlayer)
{	// advc.106i: Hack to prepend sth. to the replay file name
	GET_PLAYER(ePlayer).setSavingReplay(true);
	gDLL->getEngineIFace()->SaveReplay(ePlayer);
	// advc.106i: Probably redundant b/c CvGame::writeReplay already sets it to false
	GET_PLAYER(ePlayer).setSavingReplay(false);
}


void CvGame::showEndGameSequence()
{
	long iHours = getMinutesPlayed() / 60;
	long iMinutes = getMinutesPlayed() % 60;
	// (PlayerIter<HUMAN> would only affect humans alive)
	for (PlayerIter<EVER_ALIVE> itHuman; itHuman.hasNext(); ++itHuman)
	{
		CvPlayer& kHuman = *itHuman;
		if (!kHuman.isHuman())
			continue;
		addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, kHuman.getID(),
				gDLL->getText("TXT_KEY_MISC_TIME_SPENT", iHours, iMinutes));
		CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_TEXT);
		if (pInfo != NULL)
		{
			if (getWinner() != NO_TEAM && getVictory() != NO_VICTORY)
			{
				pInfo->setText(gDLL->getText("TXT_KEY_GAME_WON",
   						//GET_TEAM(getWinner()).getName().GetCString(),
                        GET_PLAYER(GET_TEAM(getWinner()).getLeaderID()).getCivilizationShortDescription(), // rfc
						GC.getInfo(getVictory()).getTextKeyWide()));
			}
			else pInfo->setText(gDLL->getText("TXT_KEY_MISC_DEFEAT2")); // rfc
			kHuman.addPopup(pInfo);
		}
		if (getWinner() == kHuman.getTeam())
		{
			if (!CvString(GC.getInfo(getVictory()).getMovie()).empty())
			{
				// show movie
				pInfo = new CvPopupInfo(BUTTONPOPUP_PYTHON_SCREEN);
				if (pInfo != NULL)
				{
						pInfo->setText(L"showVictoryMovie");
						pInfo->setData1((int)getVictory());
						kHuman.addPopup(pInfo);
				}
			}
			else if (GC.getInfo(getVictory()).isDiploVote())
			{
				pInfo = new CvPopupInfo(BUTTONPOPUP_PYTHON_SCREEN);
				if (pInfo != NULL)
				{
					pInfo->setText(L"showUnVictoryScreen");
					kHuman.addPopup(pInfo);
				}
			}
		}
		// show replay
		pInfo = new CvPopupInfo(BUTTONPOPUP_PYTHON_SCREEN);
		if (pInfo != NULL)
		{
			pInfo->setText(L"showReplay");
			pInfo->setData1(kHuman.getID());
			/*	advc.106i (comment): The BtS comment below means that the HoF
				is not shown right after the player exits from the Replay screen.
				That it still gets shown later on is intentional (see a few
				lines below). */
			pInfo->setOption1(false); // don't go to HOF on exit
			kHuman.addPopup(pInfo);
		}
		// show top cities / stats
		pInfo = new CvPopupInfo(BUTTONPOPUP_PYTHON_SCREEN);
		if (pInfo != NULL)
		{
			pInfo->setText(L"showInfoScreen");
			pInfo->setData1(0);
			pInfo->setData2(1);
			kHuman.addPopup(pInfo);
		}
		// show Dan
		pInfo = new CvPopupInfo(BUTTONPOPUP_PYTHON_SCREEN);
		if (pInfo != NULL)
		{
			pInfo->setText(L"showDanQuayleScreen");
			kHuman.addPopup(pInfo);
		}
		// show Hall of Fame
		pInfo = new CvPopupInfo(BUTTONPOPUP_PYTHON_SCREEN);
		if (pInfo != NULL)
		{
			pInfo->setText(L"showHallOfFame");
			pInfo->setData1(0); // advc.003y: Disable replay buttons
			kHuman.addPopup(pInfo);
		}
	}
}


CvReplayInfo* CvGame::getReplayInfo() const
{
	return m_pReplayInfo;
}


void CvGame::setReplayInfo(CvReplayInfo* pReplay)
{
	SAFE_DELETE(m_pReplayInfo);
	m_pReplayInfo = pReplay;
}


bool CvGame::hasSkippedSaveChecksum() const
{
	return gDLL->hasSkippedSaveChecksum();
}


void CvGame::addPlayer(PlayerTypes eNewPlayer, LeaderHeadTypes eLeader, CivilizationTypes eCiv, int iBirthTurn, bool bAlive, bool bMinor)
{
	/*	UNOFFICIAL_PATCH Start: Fixed bug with colonies who occupy recycled player slots
		showing the old leader or civ names */
	CvWString szEmptyString = L"";
	LeaderHeadTypes const eOldLeader = GET_PLAYER(eNewPlayer).getLeaderType();
	CvInitCore& kInitCore = GC.getInitCore();
	if (eOldLeader != NO_LEADER && eOldLeader != eLeader)
		kInitCore.setLeaderName(eNewPlayer, szEmptyString);
	CivilizationTypes const eOldCiv = GET_PLAYER(eNewPlayer).getCivilizationType();
	if (eOldCiv != NO_CIVILIZATION && eOldCiv != eCiv)
	{
		kInitCore.setCivAdjective(eNewPlayer, szEmptyString);
		kInitCore.setCivDescription(eNewPlayer, szEmptyString);
		kInitCore.setCivShortDesc(eNewPlayer, szEmptyString);
	}
	// UNOFFICIAL_PATCH End
	PlayerColorTypes eColor = (PlayerColorTypes)GC.getInfo(eCiv).getDefaultPlayerColor();
    // rfc: disable color reassignment
	// <advc> Restructured these byzantine loops. Hope I got it right.
	/*bool bFindNewColor = (eColor == NO_PLAYERCOLOR);
	if (!bFindNewColor)
	{
		for (PlayerIter<EVER_ALIVE> itOther; itOther.hasNext(); ++itOther)
		{
			if (itOther->getID() != eNewPlayer &&
				//	UNOFFICIAL_PATCH, Bugfix, 12/30/08, jdog5000:
				//	Don't invalidate color choice if it's taken by this player
				itOther->getPlayerColor() == eColor)
			{
				bFindNewColor = true;
				break;
			}
		}
	}
	if (bFindNewColor)
	{
		PlayerColorTypes const eBarbarianColor = (PlayerColorTypes)GC.getInfo((CivilizationTypes)
				GC.getDefineINT("BARBARIAN_CIVILIZATION")).getDefaultPlayerColor();
		FOR_EACH_ENUM(PlayerColor)
		{
			if (eLoopPlayerColor == eBarbarianColor)
				continue;
			// advc: Better make sure we have _some_ color
			if (eColor == NO_PLAYERCOLOR)
				eColor = eLoopPlayerColor;

			bool bValid = true;
			for (PlayerIter<EVER_ALIVE> itOther; itOther.hasNext(); ++itOther)
			{
				if (itOther->getID() != eNewPlayer && // advc: Same as in the bugfix above
					itOther->getPlayerColor() == eLoopPlayerColor)
				{
					bValid = false;
					break;
				}
			}
			if (bValid)
			{
				eColor = eLoopPlayerColor;
				break;
			}
		}
	} // </advc>*/

	kInitCore.setLeader(eNewPlayer, eLeader);
	kInitCore.setCiv(eNewPlayer, eCiv);
	kInitCore.setSlotStatus(eNewPlayer, SS_COMPUTER);
	kInitCore.setColor(eNewPlayer, eColor);
	// advc.001: For RANDOM_PERSONALITIES option
	GET_PLAYER(eNewPlayer).changePersonalityType();
	/*GET_TEAM(eNewPlayer).init(eTeam);
	GET_PLAYER(eNewPlayer).init(eNewPlayer);*/
	// BETTER_BTS_AI_MOD, Bugfix, 12/30/08, jdog5000: START
	/*	Team init now handled when appropriate in player initInGame.
		Standard player init is written for beginning of game,
		it resets global random events for this player only among other flaws. */
	GET_PLAYER(eNewPlayer).initInGame(eNewPlayer);
	// BETTER_BTS_AI_MOD: END

    // doc: record birth turn
    if (iBirthTurn >= 0)
    {
        GET_PLAYER(eNewPlayer).setInitialBirthTurn(iBirthTurn);
    }

    // doc: set alive and minor status
    GET_PLAYER(eNewPlayer).setAlive(bAlive, false);
    GET_PLAYER(eNewPlayer).setMinorCiv(bMinor);

    // doc: civ assigned event and replay message
    if (eCiv != NO_CIVILIZATION)
    {
        CvEventReporter::getInstance().playerCivAssigned(eNewPlayer, eCiv);
        addReplayMessage(REPLAY_MESSAGE_CIV_ASSIGNED, eNewPlayer, (char*)NULL, eCiv);
    }
}

/*	BETTER_BTS_AI_MOD, Debug, 8/1/08, jdog5000: START
	(advc: Merged with code from nextActivePlayer) */
void CvGame::changeHumanPlayer(PlayerTypes eNewHuman,
	bool bSetTurnActive) // advc
{
	PlayerTypes const eCurHuman = getActivePlayer();
	/*	<advc.001> For BUG dot map update and Civ4lerts (when switching to
		a colonial vassal). */
	CyArgsList pyArgs;
	pyArgs.add(eCurHuman);
	CvEventReporter::getInstance().genericEvent(
			"SwitchHotSeatPlayer", pyArgs.makeFunctionArgs()); // </advc.001>
	/*	<advc> Probably not necessary, but seems cleaner to swap the
		player options of the old and new human rather than just copying
		from old to new. */
	EagerEnumMap<PlayerOptionTypes,bool> aeNewHumanOldOptions;
	FOR_EACH_ENUM(PlayerOption)
	{
		aeNewHumanOldOptions.set(eLoopPlayerOption,
				GET_PLAYER(eNewHuman).isOption(eLoopPlayerOption));
	} // </advc>
	FOR_EACH_ENUM(PlayerOption)
	{
		GET_PLAYER(eNewHuman).setOption(eLoopPlayerOption,
				GET_PLAYER(eCurHuman).isOption(eLoopPlayerOption));
	}
	// <advc>
	FOR_EACH_ENUM(PlayerOption)
	{
		GET_PLAYER(eCurHuman).setOption(eLoopPlayerOption,
				aeNewHumanOldOptions.get(eLoopPlayerOption));
	} // </advc>
	GET_PLAYER(eCurHuman).setIsHuman(false, /* advc.127c: */ true);
	GET_PLAYER(eNewHuman).setIsHuman(true, /* advc.127c: */ true);
	// <advc> Moved from nextActivePlayer
	if (bSetTurnActive)
	{
		GET_PLAYER(eCurHuman).setTurnActive(false, false);
		GET_PLAYER(eNewHuman).setTurnActive(true, false);
	} // </advc>
	// <advc.127c> Otherwise, the selected unit will affect CvPlot::updateCenterUnit.
	gDLL->getInterfaceIFace()->clearSelectionList();
	gDLL->getInterfaceIFace()->clearSelectedCities();
	setActivePlayer(eNewHuman, //false
			/*	This makes sure that net ids are updated. Apparently, inconsistent
				net ids can cause the diplo screen to refuse putting certain items
				on the table. */
			true);
	// (advc: Send options loop deleted; bForceHotSeat above takes care of that)
	// </advc.127c>
}


bool CvGame::isCompetingCorporation(CorporationTypes eCorp1, CorporationTypes eCorp2) const
{
    // doc (edead): corporation competition implemented in Python
    return false;

	/*// K-Mod
	if (eCorp1 == eCorp2)
		return false;
	// K-Mod end

	bool bShareResources = false;

	for (int i = 0; i < GC.getInfo(eCorp1).getNumPrereqBonuses() &&
		!bShareResources; i++)
	{
		for (int j = 0; j < GC.getInfo(eCorp2).getNumPrereqBonuses(); j++)
		{
			if (GC.getInfo(eCorp1).getPrereqBonus(i) ==
				GC.getInfo(eCorp2).getPrereqBonus(j))
			{
				return true;
			}
		}
	}

	return false;*/
}


void CvGame::setVoteSourceReligion(VoteSourceTypes eVoteSource,
	ReligionTypes eReligion, bool bAnnounce)
{
	m_aeVoteSourceReligion.set(eVoteSource, eReligion);
	if (bAnnounce && eReligion != NO_RELIGION)
	{
		CvWString szBuffer = gDLL->getText("TXT_KEY_VOTE_SOURCE_RELIGION",
				GC.getInfo(eReligion).getTextKeyWide(),
				GC.getInfo(eReligion).getAdjectiveKey(),
				GC.getInfo(eVoteSource).getTextKeyWide());
		for (PlayerIter<MAJOR_CIV> itPlayer; itPlayer.hasNext(); ++itPlayer)
		{
			// <advc.127b>
			std::pair<int,int> iiXY = getVoteSourceXY(eVoteSource,
					itPlayer->getTeam(), true); // </advc.127>
			gDLL->UI().addMessage(itPlayer->getID(), false, -1, szBuffer,
					GC.getInfo(eReligion).getSound(), MESSAGE_TYPE_MAJOR_EVENT,
					NULL, GC.getColorType("HIGHLIGHT_TEXT"),
					iiXY.first, iiXY.second); // advc.127b
		}
	}
}

// advc.001: For culturalVictoryNumCultureCities. Infinity that doesn't easily overflow.
namespace
{
	enum CultVictCityThresh
	{
		CULT_VICT_CITY_TRESH_INFINITE = arithm_traits<short>::max,
	};
}


int CvGame::culturalVictoryNumCultureCities() const
{
	//return m_iNumCultureVictoryCities;
	/*	advc.001: Easier to return infinity here than to ensure that all
		call locations check for culturalVictoryValid */
	return (culturalVictoryValid() ? m_iNumCultureVictoryCities : CULT_VICT_CITY_TRESH_INFINITE);
}


CultureLevelTypes CvGame::culturalVictoryCultureLevel() const
{
	return (culturalVictoryValid() ? m_eCultureVictoryCultureLevel : NO_CULTURELEVEL);
}


int CvGame::getCultureThreshold(CultureLevelTypes eLevel) const
{
	int iThreshold = GC.getInfo(eLevel).getSpeedThreshold(getGameSpeedType());
	if (isOption(GAMEOPTION_NO_ESPIONAGE))
	{
		static int const iNO_ESPIONAGE_CULTURE_LEVEL_MODIFIER = GC.getDefineINT("NO_ESPIONAGE_CULTURE_LEVEL_MODIFIER"); // advc.opt
		iThreshold *= 100 + iNO_ESPIONAGE_CULTURE_LEVEL_MODIFIER;
		iThreshold /= 100;
	}  // <advc.126>
	int const iExempt = 50; // Don't adjust thresholds below "developing"
	if (iThreshold >= iExempt)
	{
		iThreshold *= GC.getInfo(getStartEra()).getCulturePercent();
		iThreshold /= 100; // </advc.126>
		// <advc.251>
		int iMultiple = 1;
		if (iThreshold > 100000)
			iMultiple = 10000;
		else if (iThreshold > 50000)
			iMultiple = 5000;
		else if (iThreshold > 10000)
			iMultiple = 1000;
		else if (iThreshold > 1000)
			iMultiple = 100;
		else if (iThreshold > 100)
			iMultiple = 10;
		else iMultiple = 5;
		iThreshold *= GC.getInfo(getHandicapType()).getCultureLevelPercent();
		iThreshold = per100(iThreshold).roundToMultiple(iMultiple);
		iThreshold = std::max(iThreshold, iExempt);
	} // </advc.251>
	return iThreshold;
}

// advc.908b:
int CvGame::freeCityCultureFromTrait(TraitTypes eTrait) const
{
	return (GC.getInfo(eTrait).get(CvTraitInfo::FREE_CITY_CULTURE) *
			// advc.251: No longer fully adjusted to game speed
			GC.getInfo(getGameSpeedType()).getTrainPercent()) / 100;
}


void CvGame::doUpdateCacheOnTurn()
{
	// (advc.enum: Shrine data now cached by CvCity)

	// reset cultural victories
	/*	K-Mod (tbd.): Move this somewhere else;
		doesn't need to be updated every turn! */
	m_iNumCultureVictoryCities = 0;
	FOR_EACH_ENUM(Victory)
	{
		if (!isVictoryValid(eLoopVictory))
			continue;
		CvVictoryInfo const& kVictoryInfo = GC.getInfo(eLoopVictory);
		if (kVictoryInfo.getCityCulture() > 0)
		{
			int iNumCultureCities = kVictoryInfo.getNumCultureCities();
			if (iNumCultureCities > m_iNumCultureVictoryCities)
			{
				m_iNumCultureVictoryCities = iNumCultureCities;
				m_eCultureVictoryCultureLevel = (CultureLevelTypes)
						kVictoryInfo.getCityCulture();
			}
		}
	}
	// K-Mod.
	if (isFinalInitialized()) // advc.pf: Else pathfinder may not have been created yet
		CvSelectionGroup::resetPath(); // (one of the few manual resets we need)
	m_aiActivePlayerCycledGroups.clear();
	// K-Mod end
}


VoteSelectionData* CvGame::addVoteSelection(VoteSourceTypes eVoteSource)
{
	VoteSelectionData* pData = m_voteSelections.add();
	FAssert(pData != NULL); // advc
	pData->eVoteSource = eVoteSource;
	FOR_EACH_ENUM(Vote)  // advc.003n: Minor civs excluded from all loops
	{
		if (!GC.getInfo(eLoopVote).isVoteSourceType(eVoteSource) ||
			!isChooseElection(eLoopVote))
		{
			continue;
		}
		VoteSelectionSubData kData;
		kData.eVote = eLoopVote;
		kData.iCityId = -1;
		kData.ePlayer = NO_PLAYER;
		kData.eOtherPlayer = NO_PLAYER;
		if (GC.getInfo(kData.eVote).isOpenBorders())
		{
			if (isValidVoteSelection(eVoteSource, kData))
			{
				kData.szText = gDLL->getText("TXT_KEY_POPUP_ELECTION_OPEN_BORDERS",
						getVoteRequired(kData.eVote, eVoteSource),
						countPossibleVote(kData.eVote, eVoteSource));
				pData->aVoteOptions.push_back(kData);
			}
		}
		else if (GC.getInfo(kData.eVote).isDefensivePact())
		{
			if (isValidVoteSelection(eVoteSource, kData))
			{
				kData.szText = gDLL->getText("TXT_KEY_POPUP_ELECTION_DEFENSIVE_PACT",
						getVoteRequired(kData.eVote, eVoteSource),
						countPossibleVote(kData.eVote, eVoteSource));
				pData->aVoteOptions.push_back(kData);
			}
		}
		else if (GC.getInfo(kData.eVote).isForcePeace())
		{
			for (TeamIter<MAJOR_CIV> it; it.hasNext(); ++it)
			{
				kData.ePlayer = it->getLeaderID();
				if (isValidVoteSelection(eVoteSource, kData))
				{
					kData.szText = gDLL->getText("TXT_KEY_POPUP_ELECTION_FORCE_PEACE",
							//it->getName().GetCString(),
							it->getCivilizationShortDescription().GetCString(), // rfc
							getVoteRequired(kData.eVote, eVoteSource),
							countPossibleVote(kData.eVote, eVoteSource));
					pData->aVoteOptions.push_back(kData);
				}
			}
		}
		else if (GC.getInfo(kData.eVote).isForceNoTrade())
		{
			for (TeamIter<MAJOR_CIV> it; it.hasNext(); ++it)
			{
				kData.ePlayer = it->getLeaderID();
				if (isValidVoteSelection(eVoteSource, kData))
				{
					kData.szText = gDLL->getText("TXT_KEY_POPUP_ELECTION_FORCE_NO_TRADE",
							//it->getName().GetCString(),
							it->getCivilizationShortDescription().GetCString(), // rfc
							getVoteRequired(kData.eVote, eVoteSource),
							countPossibleVote(kData.eVote, eVoteSource));
					pData->aVoteOptions.push_back(kData);
				}
			}
		}
		else if (GC.getInfo(kData.eVote).isForceWar())
		{
			for (TeamIter<MAJOR_CIV> it; it.hasNext(); ++it)
			{
				kData.ePlayer = it->getLeaderID();
				if (isValidVoteSelection(eVoteSource, kData))
				{
					kData.szText =
							// <kekm.25/advc>
							(it->isActive() ?
							gDLL->getText("TXT_KEY_POPUP_ELECTION_FORCE_WAR_VS_YOU",
							getVoteRequired(kData.eVote, eVoteSource),
							countPossibleVote(kData.eVote, eVoteSource)) :
							// </kekm.25/advc>
							gDLL->getText("TXT_KEY_POPUP_ELECTION_FORCE_WAR",
							//it->getName().GetCString(),
							it->getCivilizationShortDescription().GetCString(), // rfc
							getVoteRequired(kData.eVote, eVoteSource),
							countPossibleVote(kData.eVote, eVoteSource)));
					pData->aVoteOptions.push_back(kData);
				}
			}
		}
		else if (GC.getInfo(kData.eVote).isAssignCity())
		{
			for (PlayerIter<MAJOR_CIV> it; it.hasNext(); ++it)
			{
				FOR_EACH_CITY(pLoopCity, *it)
				{
					PlayerTypes eNewOwner = pLoopCity->getPlot().findHighestCulturePlayer();
					if (eNewOwner != NO_PLAYER &&
					/*	advc.099: No longer implied by findHighestCulturePlayer;
						mustn't return cities to dead civs. */
						GET_PLAYER(eNewOwner).isAlive())
					{
						kData.ePlayer = it->getID();
						kData.iCityId =	pLoopCity->getID();
						kData.eOtherPlayer = eNewOwner;
						if (isValidVoteSelection(eVoteSource, kData))
						{
							kData.szText = gDLL->getText("TXT_KEY_POPUP_ELECTION_ASSIGN_CITY",
									it->getCivilizationAdjectiveKey(), pLoopCity->getNameKey(),
									//GET_PLAYER(eNewOwner).getNameKey(),
									GET_PLAYER(eNewOwner).getCivilizationShortDescriptionKey(), // rfc
									getVoteRequired(kData.eVote, eVoteSource),
									countPossibleVote(kData.eVote, eVoteSource));
							pData->aVoteOptions.push_back(kData);
						}
					}
				}
			}
		}
        // doc: revoke membership resolution
        // TODO: refactor
		else if (GC.getVoteInfo(kData.eVote).isRevokeMembership())
		{
			for (int iTeam1 = 0; iTeam1 < MAX_CIV_TEAMS; ++iTeam1)
			{
				CvTeam& kTeam1 = GET_TEAM((TeamTypes)iTeam1);

				if (kTeam1.isAlive())
				{
					kData.ePlayer = kTeam1.getLeaderID();

					if (isValidVoteSelection(eVoteSource, kData))
					{
						//kData.szText = gDLL->getText("TXT_KEY_POPUP_ELECTION_FORCE_WAR", kTeam1.getName().GetCString(), getVoteRequired(kData.eVote, eVoteSource), countPossibleVote(kData.eVote, eVoteSource)); //Rhye
						kData.szText = gDLL->getText("TXT_KEY_POPUP_ELECTION_EXCOMMUNICATION", GET_PLAYER((PlayerTypes)iTeam1).getCivilizationDescriptionKey(), getVoteRequired(kData.eVote, eVoteSource), countPossibleVote(kData.eVote, eVoteSource)); //Rhye
						pData->aVoteOptions.push_back(kData);
					}
				}
			}
		}
        // doc: gold resolution
        // TODO: refactor
		else if (GC.getVoteInfo(kData.eVote).getGoldPercent() > 0)
		{
			kData.ePlayer = GET_TEAM(GC.getGame().getSecretaryGeneral(eVoteSource)).getLeaderID();

			if (isValidVoteSelection(eVoteSource, kData))
			{
				kData.szText = gDLL->getText("TXT_KEY_POPUP_ELECTION_COLLECT_TITHE", getVoteRequired(kData.eVote, eVoteSource), countPossibleVote(kData.eVote, eVoteSource));
				pData->aVoteOptions.push_back(kData);
			}
		}
        // doc: espionage resolution
        // TODO: refactor
		else if (GC.getVoteInfo(kData.eVote).getEspionage() > 0)
		{
			kData.ePlayer = GET_TEAM(GC.getGame().getSecretaryGeneral(eVoteSource)).getLeaderID();

			for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
			{
				CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iI);

				if (kLoopPlayer.isMinorCiv())
				{
					continue;
				}

				bool bValid = false;
				for (int iJ =  0; iJ < NUM_RELIGIONS; iJ++)
				{
					if (kLoopPlayer.getReligionPopulation((ReligionTypes)iJ) > 0)
					{
						bValid = true;
						break;
					}
				}

				if (bValid)
				{
					kData.eOtherPlayer = kLoopPlayer.getID();

					if (isValidVoteSelection(eVoteSource, kData))
					{
						kData.szText = gDLL->getText("TXT_KEY_POPUP_ELECTION_INQUISITION", kLoopPlayer.getCivilizationShortDescription(), getVoteRequired(kData.eVote, eVoteSource), countPossibleVote(kData.eVote, eVoteSource));
						pData->aVoteOptions.push_back(kData);
					}
				}
			}
		}
        // doc: decolonize resolution
        // TODO: refactor
		else if (GC.getVoteInfo(kData.eVote).isDecolonize())
		{
			for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
			{
				PlayerTypes ePlayer = (PlayerTypes)iI;
				CvPlayer& kPlayer = GET_PLAYER(ePlayer);

				if (kPlayer.isMinorCiv())
				{
					continue;
				}

				if (kPlayer.getTeam() == getSecretaryGeneral(eVoteSource))
				{
					continue;
				}

				if (!kPlayer.isAlive())
				{
					continue;
				}

				if (kPlayer.countColonies() == 0)
				{
					continue;
				}

				int iBestID = -1;
				int iBestValue = MAX_INT;
				int iCurrentValue;

				int iLoop;
				for (CvCity* pLoopCity = kPlayer.firstCity(&iLoop); NULL != pLoopCity; pLoopCity = kPlayer.nextCity(&iLoop))
				{
					if (pLoopCity->plot()->isCore(ePlayer)) continue;
					if (pLoopCity->plot()->isOverseas(kPlayer.getCapitalCity()->plot())) continue;

					if (NO_PLAYER == pLoopCity->getLiberationPlayer(false))
					{
						iCurrentValue = pLoopCity->plot()->getSettlerValue(ePlayer);
						if (iBestID == -1 || iCurrentValue < iBestValue)
						{
							iBestID = pLoopCity->getID();
							iBestValue = iCurrentValue;
						}
					}
				}

				if (iBestID != -1)
				{
					kData.ePlayer = ePlayer;
					kData.iCityId = iBestID;
					kData.szText = gDLL->getText("TXT_KEY_POPUP_ELECTION_DECOLONIZE", kPlayer.getCity(iBestID)->getNameKey(), kPlayer.getCivilizationShortDescription(), getVoteRequired(kData.eVote, eVoteSource), countPossibleVote(kData.eVote, eVoteSource)); //Rhye
					pData->aVoteOptions.push_back(kData);
				}
			}
		}
        // doc: release civilization resolution
        // TODO: refactor
		else if (GC.getVoteInfo(kData.eVote).isReleaseCivilization())
		{
			PlayerTypes ePlayer;
			CivilizationTypes eReleasableCivilization;

			for (iI = 0; iI < MAX_CIV_PLAYERS; iI++)
			{
				ePlayer = (PlayerTypes)iI;

				if (GET_PLAYER(ePlayer).isMinorCiv())
				{
					continue;
				}

				if (GET_PLAYER(ePlayer).getTeam() == getSecretaryGeneral(eVoteSource))
				{
					continue;
				}

				if (!GET_PLAYER(ePlayer).isAlive())
				{
					continue;
				}

				for (int iJ = 0; iJ < NUM_CIVS; iJ++)
				{
					eReleasableCivilization = (CivilizationTypes)iJ;

					if (isCivAlive(eReleasableCivilization)) continue;
					if (!canRespawn(eReleasableCivilization)) continue;

					int iCityLoop;
					int iNumCities = 0;

					for (CvCity* pLoopCity = GET_PLAYER(ePlayer).firstCity(&iCityLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER(ePlayer).nextCity(&iCityLoop))
					{
						if (pLoopCity->isCore(eReleasableCivilization) && !pLoopCity->isCore(ePlayer) && !pLoopCity->isCapital())
						{
							++iNumCities;
						}
					}

					if (iNumCities > 1)
					{
						kData.ePlayer = ePlayer;
						kData.eOtherPlayer = (PlayerTypes)eReleasableCivilization;
						kData.szText = gDLL->getText("TXT_KEY_POPUP_ELECTION_RELEASE", GC.getCivilizationInfo(eReleasableCivilization).getText(), GET_PLAYER(ePlayer).getCivilizationAdjective(), getVoteRequired(kData.eVote, eVoteSource), countPossibleVote(kData.eVote, eVoteSource)); //Rhye
						pData->aVoteOptions.push_back(kData);
					}
				}
			}
		}
		else
		{
			kData.szText = gDLL->getText("TXT_KEY_POPUP_ELECTION_OPTION",
					GC.getInfo(kData.eVote).getTextKeyWide(),
					getVoteRequired(kData.eVote, eVoteSource),
					countPossibleVote(kData.eVote, eVoteSource));
			if (isVotePassed(kData.eVote))
				kData.szText += gDLL->getText("TXT_KEY_POPUP_PASSED");
			//if (canDoResolution(eVoteSource, kData))
			if (isValidVoteSelection(eVoteSource, kData)) // K-Mod (zomg!)
				pData->aVoteOptions.push_back(kData);
		}
	}

	if (pData->aVoteOptions.size() == 0)
	{
		deleteVoteSelection(pData->getID());
		pData = NULL;
	}
	return pData;
}


void CvGame::deleteVoteSelection(int iID)
{
	m_voteSelections.removeAt(iID);
}


VoteTriggeredData* CvGame::getVoteTriggered(int iID) const
{
	return m_votesTriggered.getAt(iID);
}


VoteTriggeredData* CvGame::addVoteTriggered(VoteSelectionData const& kData, int iChoice)
{
	if (iChoice == -1 || iChoice >= (int)kData.aVoteOptions.size())
		return NULL;
	return addVoteTriggered(kData.eVoteSource, kData.aVoteOptions[iChoice]);
}


VoteTriggeredData* CvGame::addVoteTriggered(VoteSourceTypes eVoteSource,
	VoteSelectionSubData const& kOptionData)
{
	VoteTriggeredData* pData = m_votesTriggered.add();
	FAssert(pData != NULL); // advc
	pData->eVoteSource = eVoteSource;
	pData->kVoteOption = kOptionData;
	for (PlayerAIIter<MAJOR_CIV> it; it.hasNext(); ++it)
	{
		CvPlayerAI& kVoter = *it;
		if (!kVoter.isVotingMember(eVoteSource))
			continue;

		if (!kVoter.isHuman())
		{
			castVote(kVoter.getID(), pData->getID(),
					kVoter.AI_diploVote(kOptionData, eVoteSource, false));
			continue;
		}
		// <kekm.25> (advc: simplified)
		if (isTeamVote(kOptionData.eVote))
		{
			TeamTypes const eVoterMaster = kVoter.getMasterTeam();
			if (eVoterMaster != kVoter.getTeam() &&
				GET_TEAM(kVoter.getTeam()).isCapitulated() && // advc
				isTeamVoteEligible(eVoterMaster, eVoteSource) &&
				!isTeamVoteEligible(kVoter.getTeam(), eVoteSource))
			{
				castVote(kVoter.getID(), pData->getID(),
						kVoter.AI_diploVote(kOptionData, eVoteSource, false));
				continue;
			}
		} // </kekm.25>
		CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_DIPLOVOTE);
		if (pInfo != NULL)
		{
			pInfo->setData1(pData->getID());
			gDLL->getInterfaceIFace()->addPopup(pInfo, kVoter.getID());
		}
	}
	return pData;
}


void CvGame::deleteVoteTriggered(int iID)
{
	m_votesTriggered.removeAt(iID);
}


void CvGame::doVoteResults()
{
	// advc.150b: To make sure it doesn't go out of scope
	static CvWString szTargetCityName;
	int iLoop=-1;
	for (VoteTriggeredData* pVoteTriggered = m_votesTriggered.beginIter(&iLoop);
		pVoteTriggered != NULL; pVoteTriggered = m_votesTriggered.nextIter(&iLoop))
	{
		CvWString szBuffer;
		CvWString szMessage;
		VoteSelectionSubData subdata = pVoteTriggered->kVoteOption; // advc
		VoteTypes eVote = subdata.eVote;
		VoteSourceTypes eVoteSource = pVoteTriggered->eVoteSource;
		bool bPassed = false;

		if (!canDoResolution(eVoteSource, subdata))
		{
			for (PlayerIter<MAJOR_CIV> itObs; itObs.hasNext(); ++itObs)
			{
				if (!itObs->isVotingMember(eVoteSource))
					continue;
				szMessage.clear();
				szMessage.Format(L"%s: %s",
						gDLL->getText("TXT_KEY_ELECTION_CANCELLED").c_str(),
						GC.getInfo(eVote).getDescription());
				// advc.127b:
				std::pair<int,int> xy = getVoteSourceXY(eVoteSource, itObs->getTeam());
				gDLL->UI().addMessage(itObs->getID(), false, -1, szMessage,
						"AS2D_NEW_ERA", MESSAGE_TYPE_INFO, NULL,
						GC.getColorType("HIGHLIGHT_TEXT"),
						xy.first, xy.second); // advc.127b
			}
		}
		else
		{
			bool bAllVoted = true;
			for (PlayerIter<MAJOR_CIV> itPlayer; itPlayer.hasNext(); ++itPlayer)
			{
				if (!itPlayer->isVotingMember(eVoteSource))
					continue;

                // doc: cannot vote for own victory resolution
                if (GC.getInfo(eVote).isVictory())
                    if (subdata.ePlayer == itPlayer->getID() ||
                        (GET_TEAM(itPlayer->getTeam()).isVassal(GET_PLAYER(subdata.ePlayer).getTeam()) && GET_TEAM(itPlayer->getTeam()).isCapitulated()))
                        continue;

				PlayerTypes const ePlayer = itPlayer->getID();
				if (getPlayerVote(ePlayer, pVoteTriggered->getID()) == NO_PLAYER_VOTE)
				{	//give player one more turn to submit vote
					setPlayerVote(ePlayer, pVoteTriggered->getID(), NO_PLAYER_VOTE_CHECKED);
					bAllVoted = false;
					break;
				}
				else if (getPlayerVote(ePlayer, pVoteTriggered->getID())
					== NO_PLAYER_VOTE_CHECKED)
				{	//default player vote to abstain
					setPlayerVote(ePlayer, pVoteTriggered->getID(), PLAYER_VOTE_ABSTAIN);
				}
			}

			if (!bAllVoted)
				continue;
			// <advc.150b>
			szTargetCityName = "";
			int iVotes = -1; // </advc.150b>
			if (isTeamVote(eVote))
			{
				TeamTypes const eTeam = findHighestVoteTeam(*pVoteTriggered);
				if (eTeam != NO_TEAM)
				{	// <advc.150b> Store vote count for later
					iVotes = countVote(*pVoteTriggered, (PlayerVoteTypes)eTeam);
					bPassed = (iVotes >= getVoteRequired(eVote, eVoteSource));
				}	// </advc.150b>
				szBuffer = GC.getInfo(eVote).getDescription();
				if (eTeam != NO_TEAM)
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(
							gDLL->getText("TXT_KEY_POPUP_DIPLOMATIC_VOTING_VICTORY",
							GET_TEAM(eTeam).getName().GetCString(),
							countVote(*pVoteTriggered, (PlayerVoteTypes)eTeam),
							getVoteRequired(eVote, eVoteSource),
							countPossibleVote(eVote, eVoteSource)));
				}
				FOR_EACH_ENUM_REV(Team)
				{
					PlayerVoteTypes const eTeamVotedFor = (PlayerVoteTypes)eLoopTeam;
					for (PlayerIter<MAJOR_CIV> itPlayer; itPlayer.hasNext(); ++itPlayer)
					{
						if (!itPlayer->isVotingMember(eVoteSource))
							continue;
						if (getPlayerVote(itPlayer->getID(), pVoteTriggered->getID()) ==
							eTeamVotedFor)
						{
							szBuffer.append(NEWLINE);
							szBuffer.append(
									gDLL->getText("TXT_KEY_POPUP_VOTES_FOR",
									itPlayer->getNameKey(),
									GET_TEAM(eLoopTeam).getName().GetCString(),
									itPlayer->getVotes(eVote, eVoteSource)));
						}
					}
				}
				for (PlayerIter<MAJOR_CIV> itPlayer; itPlayer.hasNext(); ++itPlayer)
				{
					if (!itPlayer->isVotingMember(eVoteSource))
						continue;
					PlayerTypes const eVoter = itPlayer->getID();
					if (getPlayerVote(eVoter, pVoteTriggered->getID()) ==
						PLAYER_VOTE_ABSTAIN)
					{
						szBuffer.append(NEWLINE);
						szBuffer.append(gDLL->getText("TXT_KEY_POPUP_ABSTAINS",
								GET_PLAYER(eVoter).getNameKey(),
								GET_PLAYER(eVoter).getVotes(eVote, eVoteSource)));
					}
				}
				if (eTeam != NO_TEAM && bPassed)
					setVoteOutcome(*pVoteTriggered, (PlayerVoteTypes)eTeam);
				else setVoteOutcome(*pVoteTriggered, PLAYER_VOTE_ABSTAIN);
			}
			else
			{	// <advc.150b>
				if (subdata.ePlayer != NO_PLAYER && subdata.iCityId >= 0)
				{
					CvCity* pTargetCity = GET_PLAYER(subdata.ePlayer).
							getCity(subdata.iCityId);
					if (pTargetCity != NULL)
						szTargetCityName = pTargetCity->getNameKey();
				}
				iVotes = countVote(*pVoteTriggered, PLAYER_VOTE_YES);
				bPassed = (iVotes >= getVoteRequired(eVote, eVoteSource));
				// </advc.150b>
				// Defying resolution
				if (bPassed)
				{
					for (PlayerIter<MAJOR_CIV> itPlayer; itPlayer.hasNext(); ++itPlayer)
					{
						if (getPlayerVote(itPlayer->getID(), pVoteTriggered->getID()) ==
							PLAYER_VOTE_NEVER &&
							// kekm.25/advc: May e.g. have become a vassal
							itPlayer->canDefyResolution(eVoteSource, subdata))
						{
                            // doc: religious vote can be defied can still pass - reduced effects instead (exception: espionage)
						    if (getVoteSourceReligion(eVoteSource) == NO_RELIGION || GC.getVoteInfo(eVote).getEspionage() > 0)
    							bPassed = false;
							itPlayer->setDefiedResolution(eVoteSource, subdata);
						}
					}
				}
				if (bPassed)
				{
					for (PlayerIter<MAJOR_CIV> itPlayer; itPlayer.hasNext(); ++itPlayer)
					{
						if (!itPlayer->isVotingMember(eVoteSource))
							continue;
						if (getPlayerVote(itPlayer->getID(), pVoteTriggered->getID()) ==
							PLAYER_VOTE_YES)
						{
							itPlayer->setEndorsedResolution(eVoteSource, subdata);
						}
					}
				}
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText(bPassed ?
						"TXT_KEY_POPUP_DIPLOMATIC_VOTING_SUCCEEDS" :
						"TXT_KEY_POPUP_DIPLOMATIC_VOTING_FAILURE",
						GC.getInfo(eVote).getTextKeyWide(),
						countVote(*pVoteTriggered, PLAYER_VOTE_YES),
						getVoteRequired(eVote, eVoteSource),
						countPossibleVote(eVote, eVoteSource)));
				for (int i = PLAYER_VOTE_NEVER; i <= PLAYER_VOTE_YES; i++)
				{
					PlayerVoteTypes ePlayerVote = (PlayerVoteTypes)i;
					for (PlayerIter<MAJOR_CIV> itPlayer; itPlayer.hasNext(); ++itPlayer)
					{
						CvPlayer const& kVoter = *itPlayer;
						if (!kVoter.isVotingMember(eVoteSource) ||
							getPlayerVote(kVoter.getID(), pVoteTriggered->getID()) !=
							ePlayerVote)
						{
							continue;
						}
						szBuffer.append(NEWLINE);
						switch (ePlayerVote)
						{
						case PLAYER_VOTE_ABSTAIN:
							szBuffer.append(gDLL->getText("TXT_KEY_POPUP_ABSTAINS",
									kVoter.getNameKey(),
									kVoter.getVotes(eVote, eVoteSource)));
							break;
						case PLAYER_VOTE_NEVER:
							szBuffer.append(gDLL->getText("TXT_KEY_POPUP_VOTES_YES_NO",
									kVoter.getNameKey(), L"TXT_KEY_POPUP_VOTE_NEVER",
									kVoter.getVotes(eVote, eVoteSource)));
							break;
						case PLAYER_VOTE_NO:
							szBuffer.append(gDLL->getText("TXT_KEY_POPUP_VOTES_YES_NO",
									kVoter.getNameKey(), L"TXT_KEY_POPUP_NO",
									kVoter.getVotes(eVote, eVoteSource)));
							break;
						case PLAYER_VOTE_YES:
							szBuffer.append(gDLL->getText("TXT_KEY_POPUP_VOTES_YES_NO",
									kVoter.getNameKey(), L"TXT_KEY_POPUP_YES",
									kVoter.getVotes(eVote, eVoteSource)));
							break;
						default:
							FAssert(false);
						}
					}
				}
				setVoteOutcome(*pVoteTriggered, bPassed ? PLAYER_VOTE_YES : PLAYER_VOTE_NO);
			}
			// <advc.150b>
			CvVoteInfo& kVote = GC.getInfo(eVote);
			if (bPassed && !kVote.isSecretaryGeneral())
			{
				CvWString szResolution;
				// Special treatment for resolutions with targets
				if (subdata.ePlayer != NO_PLAYER)
				{
					CvWString szKey;
					if (kVote.isForcePeace())
						szKey = L"TXT_KEY_POPUP_ELECTION_FORCE_PEACE";
					else if (kVote.isForceNoTrade())
						szKey = L"TXT_KEY_POPUP_ELECTION_FORCE_NO_TRADE";
					else if (kVote.isForceWar())
						szKey = L"TXT_KEY_POPUP_ELECTION_FORCE_WAR";
					if (!szKey.empty())
					{
						szResolution = gDLL->getText(szKey, GET_PLAYER(subdata.ePlayer).
								getReplayName(), 0, 0);
					}
					else if (kVote.isAssignCity() && !szTargetCityName.empty() &&
						subdata.eOtherPlayer != NO_PLAYER)
					{
						szResolution = gDLL->getText("TXT_KEY_POPUP_ELECTION_ASSIGN_CITY",
								GET_PLAYER(subdata.ePlayer).getCivilizationAdjectiveKey(),
								szTargetCityName.GetCString(),
								GET_PLAYER(subdata.eOtherPlayer).getReplayName(), 0, 0);
					}
				}
				if (szResolution.empty())
				{
					szResolution = kVote.getDescription();
					/*	This is e.g.
						"U.N. Resolution #1284 (Nuclear Non-Proliferation Treaty - Cannot Build Nuclear Weapons)
						Only want "Nuclear Non-Proliferation Treaty". */
					size_t pos1 = szResolution.find(L"(");
					if (pos1 != CvWString::npos && pos1 + 1 < szResolution.length())
					{
						// Mustn't remove the stuff after the dash if bForceCivic
						size_t pos2 = std::min((kVote.isForceCivic().isAnyNonDefault() ?
								CvWString::npos : szResolution.find(L" -")),
								szResolution.find(L")"));
						if (pos2 > pos1)
							szResolution = szResolution.substr(pos1 + 1, pos2 - pos1 - 1);
					}
				}
				else
				{
					/*	Throw out stuff in parentheses, e.g.
						"Stop the war against Napoleon (Requires 0 of 0 Total Votes)" */
					szResolution = szResolution.substr(0, szResolution.find(L"(") - 1);
				}
				TeamTypes eSecrGen = getSecretaryGeneral(eVoteSource);
				szMessage = gDLL->getText("TXT_KEY_REPLAY_RESOLUTION_PASSED",
						GC.getInfo(eVoteSource).getTextKeyWide(),
						(eSecrGen == NO_TEAM ?
						gDLL->getText("TXT_KEY_TOPCIVS_UNKNOWN").GetCString() :
						GET_TEAM(eSecrGen).getReplayName().GetCString()),
						iVotes, // Don't show the required votes after all
						//getVoteRequired(eVote, eVoteSource),
						countPossibleVote(eVote, eVoteSource),
						szResolution.GetCString());
				addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, NO_PLAYER, szMessage,
						GC.getColorType("HIGHLIGHT_TEXT"));
			} // </advc.150b>
			for (PlayerIter<MAJOR_CIV> itObs; itObs.hasNext(); ++itObs)
			{
				bool bShow = itObs->isVotingMember(pVoteTriggered->eVoteSource);
				if (bShow /* advc.127: */ && itObs->isHuman())
				{
					CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_TEXT);
					if (pInfo != NULL)
					{
						pInfo->setText(szBuffer);
						gDLL->getInterfaceIFace()->addPopup(pInfo, itObs->getID());
					}
				} // <advc>
				if (!bShow && itObs->getID() == subdata.ePlayer &&
					GET_PLAYER(subdata.ePlayer).
					isVotingMember(pVoteTriggered->eVoteSource))
				{
					bShow = true;
				}
				if (!bShow && itObs->getID() == subdata.eOtherPlayer &&
					GET_PLAYER(subdata.eOtherPlayer).
					isVotingMember(pVoteTriggered->eVoteSource))
				{
					bShow = true;
				} // </advc>
				if (bPassed && (bShow || // <advc.127>
					itObs->isSpectator()))
				{
					if (bShow || szMessage.empty() || kVote.isSecretaryGeneral())
					{	// </advc.127>
						szMessage = gDLL->getText("TXT_KEY_VOTE_RESULTS",
								GC.getInfo(eVoteSource).getTextKeyWide(),
								subdata.szText.GetCString());
						// Else use the replay msg
					}
					// <advc.127b>
					BuildingTypes eVSBuilding = getVoteSourceBuilding(eVoteSource);
					std::pair<int,int> iiXY = getVoteSourceXY(eVoteSource,
							itObs->getTeam(), true);
					// </advc.127b>
					gDLL->UI().addMessage(itObs->getID(), false, -1,
							szMessage, "AS2D_NEW_ERA",
							// <advc.127> was always MINOR
							kVote.isSecretaryGeneral() ? MESSAGE_TYPE_MINOR_EVENT :
							MESSAGE_TYPE_MAJOR_EVENT, // </advc.127>
							// <advc.127b>
							eVSBuilding == NO_BUILDING ? NULL :
							GC.getInfo(eVSBuilding).getButton(), // </advc.127b>
							GC.getColorType("HIGHLIGHT_TEXT"),
							iiXY.first, iiXY.second); // advc.127b
				}
			}
		}
		if (!bPassed && GC.getInfo(eVote).isSecretaryGeneral())
			setSecretaryGeneralTimer(eVoteSource, 0);

		deleteVoteTriggered(pVoteTriggered->getID());
	}
}


void CvGame::doVoteSelection()
{
	FOR_EACH_ENUM2(VoteSource, eVS)
	{
		if (!isDiploVote(eVS))
			continue;
		if (getVoteTimer(eVS) > 0)
		{
			changeVoteTimer(eVS, -1);
			continue;
		}
		setVoteTimer(eVS, (GC.getInfo(eVS).getVoteInterval() *
				// advc.252: Had used VictoryDelayPercent
				GC.getInfo(getGameSpeedType()).get(
				CvGameSpeedInfo::VoteIntervalPercent)) / 100);

		for (TeamIter<MAJOR_CIV> itTeam1; itTeam1.hasNext(); ++itTeam1)
		{
			if (!itTeam1->isVotingMember(eVS))
				continue;
			for (TeamIter<MAJOR_CIV> itTeam2; itTeam2.hasNext(); ++itTeam2)
			{
				if (!itTeam2->isVotingMember(eVS))
					continue;
				//itTeam1->meet(itTeam2->getID(), true);
				// <advc.071> Check isHasMet b/c getVoteSourceCity is a bit slow
				if (!itTeam1->isHasMet(itTeam2->getID()))
				{
					CvCity const* pSrcCity = getVoteSourceCity(eVS, NO_TEAM);
					if (pSrcCity == NULL)
						itTeam1->meet(itTeam2->getID(), true, NULL);
					else
					{
						FirstContactData fcData(pSrcCity->plot());
						itTeam1->meet(itTeam2->getID(), true, &fcData);
					} // </advc.071>
				}
			}
		}
		TeamTypes eSecretaryGeneral = getSecretaryGeneral(eVS);
		PlayerTypes eSecretaryPlayer = NO_PLAYER;
		if (eSecretaryGeneral != NO_TEAM)
			eSecretaryPlayer = GET_TEAM(eSecretaryGeneral).getSecretaryID();

		bool bSecretaryGeneralVote = false;
		if (canHaveSecretaryGeneral(eVS))
		{
			if (getSecretaryGeneralTimer(eVS) > 0)
				changeSecretaryGeneralTimer(eVS, -1);
			else
			{
				setSecretaryGeneralTimer(eVS, GC.getDefineINT(
						"DIPLO_VOTE_SECRETARY_GENERAL_INTERVAL"));
				FOR_EACH_ENUM(Vote)
				{
					CvVoteInfo const& kLoopVote = GC.getInfo(eLoopVote);
					if (kLoopVote.isSecretaryGeneral() && kLoopVote.isVoteSourceType(eVS))
					{
						VoteSelectionSubData kOptionData;
						kOptionData.iCityId = -1;
						kOptionData.ePlayer = NO_PLAYER;
						kOptionData.eOtherPlayer = NO_PLAYER; // kmodx: Missing initialization
						kOptionData.eVote = eLoopVote;
						kOptionData.szText = gDLL->getText("TXT_KEY_POPUP_ELECTION_OPTION",
								kLoopVote.getTextKeyWide(), getVoteRequired(eLoopVote, eVS),
								countPossibleVote(eLoopVote, eVS));
						addVoteTriggered(eVS, kOptionData);
						bSecretaryGeneralVote = true;
						break;
					}
				}
			}
		}

		if (!bSecretaryGeneralVote &&
			eSecretaryGeneral != NO_TEAM && eSecretaryPlayer != NO_PLAYER)
		{
			VoteSelectionData* pData = addVoteSelection(eVS);
			if (pData != NULL)
			{
				if (GET_PLAYER(eSecretaryPlayer).isHuman())
				{
					CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_CHOOSEELECTION);
					if (pInfo != NULL)
					{
						pInfo->setData1(pData->getID());
						gDLL->getInterfaceIFace()->addPopup(pInfo, eSecretaryPlayer);
					}
				}
				else
				{
					setVoteChosen(GET_TEAM(eSecretaryGeneral).AI_chooseElection(*pData),
							pData->getID());
				}
			}
			else setVoteTimer(eVS, 0);
		}
	}
}


void CvGame::initEvents()
{
	/*	<advc.003v> Triggers may or may not have been loaded.
		Better leave them alone. And no point in marking them all as inactive. */
	if (isOption(GAMEOPTION_NO_EVENTS))
		return; // </advc.003v>
	FOR_EACH_ENUM(EventTrigger)
	{
		if (//isOption(GAMEOPTION_NO_EVENTS) || // advc.003v
			SyncRandNum(100) >= GC.getInfo(eLoopEventTrigger).getPercentGamesActive())
		{
			m_abInactiveTriggers.set(eLoopEventTrigger, true);
		}
	}
}


bool CvGame::isCivEverActive(CivilizationTypes eCivilization) const
{
	FOR_EACH_ENUM(Player)
	{
		CvPlayer& kLoopPlayer = GET_PLAYER(eLoopPlayer);
		if (kLoopPlayer.isEverAlive() &&
			kLoopPlayer.getCivilizationType() == eCivilization)
		{
			return true;
		}
	}
	return false;
}


bool CvGame::isLeaderEverActive(LeaderHeadTypes eLeader) const
{
	FOR_EACH_ENUM(Player)
	{
		CvPlayer& kLoopPlayer = GET_PLAYER(eLoopPlayer);
		if (kLoopPlayer.isEverAlive() &&
			kLoopPlayer.getLeaderType() == eLeader)
		{
			return true;
		}
	}
	return false;
}


bool CvGame::isUnitEverActive(UnitTypes eUnit) const
{
	FOR_EACH_ENUM(Civilization)
	{
		if (isCivEverActive(eLoopCivilization))
		{
			if (eUnit == GC.getInfo(eLoopCivilization).getCivilizationUnits(
				GC.getInfo(eUnit).getUnitClassType()))
			{
				return true;
			}
		}
	}
	return false;
}


bool CvGame::isBuildingEverActive(BuildingTypes eBuilding) const
{
	FOR_EACH_ENUM(Civilization)
	{
		if (isCivEverActive(eLoopCivilization))
		{
			if (eBuilding == GC.getInfo(eLoopCivilization).getCivilizationBuildings(
				GC.getInfo(eBuilding).getBuildingClassType()))
			{
				return true;
			}
		}
	}
	return false;
}


void CvGame::processBuilding(BuildingTypes eBuilding, int iChange)
{
	FOR_EACH_ENUM(VoteSource)
	{
		if (GC.getInfo(eBuilding).getVoteSourceType() == eLoopVoteSource)
			changeDiploVote(eLoopVoteSource, iChange);
	}
}

// advc.314: Between 0 and GOODY_BUFF_PEAK_MULTIPLIER, depending on game turn.
scaled CvGame::goodyHutEffectFactor(
	/*	Use true when a goody hut effect is supposed to increase with
		the game speed. When set to false, the turn numbers in this
		function are still game-speed adjusted. */
	bool bSpeedAdjust) const
{
	static int const iGOODY_BUFF_START_TURN = GC.getDefineINT("GOODY_BUFF_START_TURN");
	static int const iGOODY_BUFF_PEAK_TURN = GC.getDefineINT("GOODY_BUFF_PEAK_TURN");
	static int const iGOODY_BUFF_PEAK_MULTIPLIER = GC.getDefineINT("GOODY_BUFF_PEAK_MULTIPLIER");
	scaled rTurnsSpeedFactor = per100(GC.getGame().getSpeedPercent());
	scaled rWorldFactor = 1;
		// Not sure if map-size adjustment is a good idea
		//=per100(GC.getInfo(GC.getMap().getWorldSize()).getResearchPercent());
	scaled rFinalSpeedFactor = (!bSpeedAdjust ? 1 :
			per100(GC.getInfo(GC.getGame().getGameSpeedType()).getTrainPercent()) *
			rWorldFactor);
	scaled rStartTurn = scaled::max(0, iGOODY_BUFF_START_TURN * rTurnsSpeedFactor);
	scaled rPeakTurn = scaled::max(rStartTurn, iGOODY_BUFF_PEAK_TURN * rTurnsSpeedFactor);
	scaled rPeakMult = std::max(1, iGOODY_BUFF_PEAK_MULTIPLIER);
	/*	Exponent for power-law function; aiming for a function shape that
		resembles the graphs on the Info tab. */
	scaled rExp = fixp(1.25);
	// (or rather: the inverse of the gradient)
	scaled rGradient = (rPeakTurn - rStartTurn).pow(rExp) / (rPeakMult - 1);
	rGradient.clamp(1, 500);
	scaled t = getGameTurn();
	/*	Function through (rStartTurn, 1) and (rPeakTurn, rPeakMult)
		[^that's assuming bSpeedAdjust=false] */
	scaled r = rFinalSpeedFactor * std::min(rPeakMult,
			(rGradient + (scaled::max(0, t - rStartTurn).pow(rExp))) / rGradient);
	return r;
}

// <advc.004m>
GlobeLayerTypes CvGame::getCurrentLayer() const
{
	return m_eCurrentLayer;
}

// Used by CvMainInterface.py to tell the DLL which layer is active
void CvGame::reportCurrentLayer(GlobeLayerTypes eLayer)
{
	if (m_bLayerFromSavegame && eLayer != m_eCurrentLayer)
	{
		m_bLayerFromSavegame = false;
		/*	Can only enable the Resource and Unit layer from the DLL. That should
			suffice as the others are only available in Globe view and we're not
			in Globe view right after loading.
			(Could call CyGlobeLayerManager.setCurrentLayer via Python to set a
			Globe-only layer. Would have to write a Python function that first uses
			CyGlobeLayerManager to figure out the proper layer id based on m_eCurrentLayer.) */
		gDLL->getEngineIFace()->setResourceLayer(m_eCurrentLayer == GLOBE_LAYER_RESOURCE);
		if (m_eCurrentLayer == GLOBE_LAYER_UNIT || eLayer == GLOBE_LAYER_UNIT)
			gDLL->getEngineIFace()->toggleUnitLayer(); // No setter available
	}
	else m_eCurrentLayer = eLayer;
} // </advc.004m>

// <advc.127b>
std::pair<int,int> CvGame::getVoteSourceXY(VoteSourceTypes eVS, TeamTypes eObserver,
	bool bDebug) const
{
	CvCity const* pVSCity = getVoteSourceCity(eVS, eObserver, bDebug);
	std::pair<int,int> r = std::make_pair(-1,-1);
	if (pVSCity == NULL)
		return r;
	r.first = pVSCity->getX();
	r.second = pVSCity->getY();
	return r;
}


CvCity* CvGame::getVoteSourceCity(VoteSourceTypes eVS, TeamTypes eObserver, bool bDebug) const
{
	BuildingTypes eVSBuilding = getVoteSourceBuilding(eVS);
	if (eVSBuilding == NO_BUILDING)
		return NULL;
	for (PlayerIter<ALIVE> itOwner; itOwner.hasNext(); ++itOwner)
	{
		FOR_EACH_CITY_VAR(pCity, *itOwner)
		{
			if (eObserver != NO_TEAM && !pCity->isRevealed(eObserver, bDebug))
				continue;
			if (pCity->getNumBuilding(eVSBuilding) > 0)
				return pCity;
		}
	}
	return NULL;
}

// advc: Used in several places and I want to make a small change
bool CvGame::isFreeStartEraBuilding(BuildingTypes eBuilding) const
{
	CvBuildingInfo const& kBuilding = GC.getInfo(eBuilding);
	return (kBuilding.getFreeStartEra() != NO_ERA &&
			getStartEra() >= kBuilding.getFreeStartEra() &&
			// <advc.126>
			(kBuilding.getMaxStartEra() == NO_ERA ||
			kBuilding.getMaxStartEra() >= getStartEra())); // </advc.126>
}


BuildingTypes CvGame::getVoteSourceBuilding(VoteSourceTypes eVS) const
{
	FOR_EACH_ENUM(Building)
	{
		if (GC.getInfo(eLoopBuilding).getVoteSourceType() == eVS)
			return eLoopBuilding;
	}
	return NO_BUILDING;
} // </advc.127b>

// advc.052:
void CvGame::setScenario(bool b)
{
	m_bScenario = b;
	/*	These two apparently check the same thing via the EXE,
		probably by checking the ending of the map script name,
		which is going to be somewhat slow. */
	FAssert(m_bScenario == gDLL->isWBMapScript());
	FAssert(m_bScenario == GC.getInitCore().getWBMapScript());
}

// advc.250b:
StartPointsAsHandicap const& CvGame::startPointsAsHandicap() const
{
	return *m_pSpah;
}

// advc.106i:
void CvGame::setHallOfFame(CvHallOfFameInfo* pHallOfFame)
{
	m_pHallOfFame = pHallOfFame;
}

// advc:
std::set<int>& CvGame::getActivePlayerCycledGroups()
{
	return m_aiActivePlayerCycledGroups; // Was public; now protected.
}

// doc
// TODO: refactor
bool CvGame::isNeighbors(PlayerTypes ePlayer1, PlayerTypes ePlayer2) const
{
    return (GET_PLAYER(ePlayer1).AI_calculateStolenCityRadiusPlots(ePlayer2) > 0 || GET_PLAYER(ePlayer2).AI_calculateStolenCityRadiusPlots(ePlayer1) > 0);
}

// doc
// TODO: refactor
TeamTypes CvGame::determineWinner(TeamTypes eTeam1, TeamTypes eTeam2) const
{
    return (GET_TEAM(eTeam1).AI_endWarVal(eTeam2) < GET_TEAM(eTeam2).AI_endWarVal(eTeam1)) ? eTeam1 : eTeam2;
}

// doc
// TODO: refactor
void CvGame::autosave(bool bInitial)
{
	gDLL->getEngineIFace()->AutoSave(bInitial);
}

// doc
// TODO: refactor
bool CvGame::isPlayerAutoplay(PlayerTypes ePlayer)
{
	if (ePlayer == NO_PLAYER)
	{
		ePlayer = getActivePlayer();
	}

	return getGameTurnYear() < GC.getCivilizationInfo(GET_PLAYER(ePlayer).getCivilizationType()).getStartingYear();
}

// doc
void CvGame::setCityScreenOwner(PlayerTypes ePlayer)
{
	m_eCityScreenOwner = ePlayer;
}

// doc
void CvGame::resetCityScreenOwner()
{
	setCityScreenOwner(NO_PLAYER);
}

// doc
// TODO: header
PlayerTypes CvGame::getCityScreenOwner() const
{
	return m_eCityScreenOwner;
}

// doc
bool CvGame::isNotification(PlayerTypes eNotifiedPlayer, PlayerTypes eCausingPlayer, NotificationLevelTypes eNotificationLevel) const
{
	switch (eNotificationLevel)
	{
	case NOTIFICATIONS_ALL:
		return true;
	case NOTIFICATIONS_KNOWN:
		return eNotifiedPlayer == eCausingPlayer || GET_PLAYER(eNotifiedPlayer).canContact(eCausingPlayer);
	case NOTIFICATIONS_NEARBY:
		return isNeighbors(eNotifiedPlayer, eCausingPlayer);
	case NOTIFICATIONS_OURS:
		return eNotifiedPlayer == eCausingPlayer;
	}

	return true;
}

// doc
// TODO: header
NotificationLevelTypes CvGame::getGreatPeopleNotifications() const
{
	return m_eGreatPeopleNotifications;
}

// doc
void CvGame::setGreatPeopleNotifications(NotificationLevelTypes eNotificationLevel)
{
	m_eGreatPeopleNotifications = eNotificationLevel;
}

// doc
bool CvGame::isGreatPeopleNotification(PlayerTypes eNotifiedPlayer, PlayerTypes eCausingPlayer) const
{
	return isNotification(eNotifiedPlayer, eCausingPlayer, getGreatPeopleNotifications());
}

// doc
NotificationLevelTypes CvGame::getReligionSpreadNotifications() const
{
	return m_eReligionSpreadNotifications;
}

// doc
void CvGame::setReligionSpreadNotifications(NotificationLevelTypes eNotificationLevel)
{
	m_eReligionSpreadNotifications = eNotificationLevel;
}

// doc
bool CvGame::isReligionSpreadNotification(PlayerTypes eNotifiedPlayer, PlayerTypes eCausingPlayer) const
{
	return isNotification(eNotifiedPlayer, eCausingPlayer, getReligionSpreadNotifications());
}

// doc
NotificationLevelTypes CvGame::getEventEffectNotifications() const
{
	return m_eEventEffectNotifications;
}

// doc
void CvGame::setEventEffectNotifications(NotificationLevelTypes eNotificationLevel)
{
	m_eEventEffectNotifications = eNotificationLevel;
}

// doc
bool CvGame::isEventEffectNotification(PlayerTypes eNotifiedPlayer, PlayerTypes eCausingPlayer) const
{
	return isNotification(eNotifiedPlayer, eCausingPlayer, getEventEffectNotifications());
}

// doc
// TODO: refactor
PeriodTypes CvGame::getPeriod(CivilizationTypes eCivilization) const
{
	if (eCivilization < NUM_CIVS)
	{
		return (PeriodTypes)m_aiCivPeriod[eCivilization];
	}

	return NO_PERIOD;
}

// doc
// TODO: refactor
void CvGame::setPeriod(CivilizationTypes eCivilization, PeriodTypes ePeriod)
{
	if (getPeriod(eCivilization) != ePeriod)
	{
		m_aiCivPeriod[eCivilization] = ePeriod;

		// Leoreth: update for Inca UP
		if (isFinalInitialized() && eCivilization == INCA)
		{
			for (int iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
			{
				CvPlot* pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);

				pLoopPlot->updateYield();
				pLoopPlot->setLayoutDirty(true);
			}
		}
	}
}

// doc
// TODO: refactor
void CvGame::setCivilizationHistory(HistoryTypes eHistory, CivilizationTypes eCivilization, int iTurn, int iValue)
{
	if (eCivilization == NO_CIVILIZATION)
	{
		return;
	}

	hash_map<int, hash_map<int, int> >::iterator it = m_aiCivilizationHistory[eHistory].find(eCivilization);
	if (it == m_aiCivilizationHistory[eHistory].end())
	{
		hash_map<int, int> civilizationHistory;
		civilizationHistory.insert(pair<int, int>(iTurn, iValue));
		m_aiCivilizationHistory[eHistory].insert(std::pair<int, hash_map<int, int> >(eCivilization, civilizationHistory));
	}
	else
	{
		it->second.insert(pair<int, int>(iTurn, iValue));
	}
}

// doc
// TODO: refactor
int CvGame::getCivilizationHistory(HistoryTypes eHistory, CivilizationTypes eCivilization, int iTurn) const
{
	hash_map<int, hash_map<int, int> >::iterator it = m_aiCivilizationHistory[eHistory].find(eCivilization);
	if (it != m_aiCivilizationHistory[eHistory].end())
	{
		hash_map<int, int>::iterator entryIt = it->second.find(iTurn);

		if (entryIt != it->second.end())
		{
			return entryIt->second;
		}
	}

	return 0;
}

// doc
// TODO: header
CivilizationTypes CvGame::getFirstDiscovered(TechTypes eTech) const
{
	FAssert(eTech > NO_TECH);
	FAssert(eTech < GC.getNumTechInfos());

	return (CivilizationTypes)m_aiFirstDiscovered[eTech];
}

// doc
// TODO: refactor
void CvGame::setFirstDiscovered(TechTypes eTech, CivilizationTypes eCiv)
{
	FAssert(eTech > NO_TECH);
	FAssert(eTech < GC.getNumTechInfos());
	FAssert(eCiv > NO_CIVILIZATION);
	FAssert(eCiv < NUM_CIVS);

	m_aiFirstDiscovered[eTech] = eCiv;
}

// doc
// TODO: header
int CvGame::getFirstDiscoveredTurn(TechTypes eTech) const
{
	FAssert(eTech > NO_TECH);
	FAssert(eTech < GC.getNumTechInfos());

	return m_aiFirstDiscoveredTurn[eTech];
}

// doc
// TODO: refactor
void CvGame::setFirstDiscoveredTurn(TechTypes eTech, int iTurn)
{
	FAssert(eTech > NO_TECH);
	FAssert(eTech < GC.getNumTechInfos());

	m_aiFirstDiscoveredTurn[eTech] = iTurn;
}