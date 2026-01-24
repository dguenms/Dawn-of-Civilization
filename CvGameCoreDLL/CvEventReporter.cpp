#include "CvGameCoreDLL.h"
#include "CvEventReporter.h"
#include "CvGame.h"
#include "CvPlayer.h"
#include "CvDLLPythonIFaceBase.h" // advc

//
// static, singleton accessor
//
CvEventReporter& CvEventReporter::getInstance()
{
	static CvEventReporter gEventReporter;
	return gEventReporter;
}


void CvEventReporter::resetStatistics()
{
	m_kStatistics.reset();
}

// advc.106l: Explicit constructor added, so I can initialize my booleans.
CvEventReporter::CvEventReporter() : m_bPreAutoSave(false), m_bPreQuickSave(false) {}

// advc.003y: Just pass the call along
void CvEventReporter::initPythonCallbackGuards()
{
	m_kPythonEventMgr.initCallbackGuards();
}

// Returns true if the event is consumed by Python
bool CvEventReporter::mouseEvent(int evt, int iCursorX, int iCursorY, bool bInterfaceConsumed)
{
	return m_kPythonEventMgr.reportMouseEvent(evt, iCursorX, iCursorY, bInterfaceConsumed);
}

// Returns true if the event is consumed by Python
bool CvEventReporter::kbdEvent(int evt, int key, int iCursorX, int iCursorY)
{
	return m_kPythonEventMgr.reportKbdEvent(evt, key, iCursorX, iCursorY);
}

void CvEventReporter::genericEvent(const char* szEventName, void *pyArgs)
{
	m_kPythonEventMgr.reportGenericEvent(szEventName, pyArgs);
}


void CvEventReporter::newGame()
{
	/*	This will only be called if statistics are being reported!
		Called at the launch of a game (new or loaded) */

	// Report initial stats for the game
	m_kStatistics.setMapName(CvString(GC.getInitCore().getMapScriptName()).GetCString());
	m_kStatistics.setEra(GC.getInitCore().getEra());
}

void CvEventReporter::newPlayer(PlayerTypes ePlayer)
{
	/*	This will only be called if statistics are being reported!
		Called at the launch of a game (new or loaded) */

	// Report initial stats for this player
	m_kStatistics.setLeader(ePlayer, GET_PLAYER(ePlayer).getLeaderType());
}

void CvEventReporter::reportModNetMessage(int iData1, int iData2, int iData3, int iData4, int iData5)
{
	m_kPythonEventMgr.reportModNetMessage(iData1, iData2, iData3, iData4, iData5);
}

void CvEventReporter::init()
{
	m_kPythonEventMgr.reportInit();
}

void CvEventReporter::update(float fDeltaTime)
{
	m_kPythonEventMgr.reportUpdate(fDeltaTime);
}

void CvEventReporter::unInit()
{
	m_kPythonEventMgr.reportUnInit();
}

void CvEventReporter::gameStart()
{
	m_kPythonEventMgr.reportGameStart();
}

void CvEventReporter::gameEnd()
{
	m_kPythonEventMgr.reportGameEnd();
}

void CvEventReporter::beginGameTurn(int iGameTurn)
{
	m_kPythonEventMgr.reportBeginGameTurn(iGameTurn);
}

void CvEventReporter::endGameTurn(int iGameTurn)
{
	m_kPythonEventMgr.reportEndGameTurn(iGameTurn);
}

void CvEventReporter::beginPlayerTurn(int iGameTurn, PlayerTypes ePlayer)
{
	m_kPythonEventMgr.reportBeginPlayerTurn(iGameTurn, ePlayer);
}

void CvEventReporter::endPlayerTurn(int iGameTurn, PlayerTypes ePlayer)
{
	m_kPythonEventMgr.reportEndPlayerTurn(iGameTurn, ePlayer);
}

void CvEventReporter::firstContact(TeamTypes eTeamID1, TeamTypes eTeamID2)
{
	m_kPythonEventMgr.reportFirstContact(eTeamID1, eTeamID2);
}

// doc: restored contact event
void CvEventReporter::restoredContact(TeamTypes eTeamID1, TeamTypes eTeamID2)
{
	m_kPythonEventMgr.reportRestoredContact(eTeamID1, eTeamID2);
}

void CvEventReporter::combatResult(CvUnit* pWinner, CvUnit* pLoser)
{
	m_kPythonEventMgr.reportCombatResult(pWinner, pLoser);
}

// advc: Cut from CvUnit::resolveCombat
void CvEventReporter::combatLogHit(CombatDetails const& kAttackerDetails,
	CombatDetails const& kDefenderDetails, int iDamage, bool bAttackerTakesHit)
{
	CyArgsList pyArgs;
	pyArgs.add(gDLL->getPythonIFace()->makePythonObject(&kAttackerDetails));
	pyArgs.add(gDLL->getPythonIFace()->makePythonObject(&kDefenderDetails));
	pyArgs.add(bAttackerTakesHit ? 1 : 0);
	pyArgs.add(iDamage);
	genericEvent("combatLogHit", pyArgs.makeFunctionArgs());
}

void CvEventReporter::improvementBuilt(int iImprovementType, int iX, int iY)
{
	m_kPythonEventMgr.reportImprovementBuilt(iImprovementType, iX, iY);
}

void CvEventReporter::improvementDestroyed(int iImprovementType, int iPlayer, int iX, int iY)
{
	m_kPythonEventMgr.reportImprovementDestroyed(iImprovementType, iPlayer, iX, iY);
}

void CvEventReporter::routeBuilt(int iRouteType, int iX, int iY)
{
	m_kPythonEventMgr.reportRouteBuilt(iRouteType, iX, iY);
}

void CvEventReporter::plotRevealed(CvPlot *pPlot, TeamTypes eTeam)
{
	m_kPythonEventMgr.reportPlotRevealed(pPlot, eTeam);
}

void CvEventReporter::plotFeatureRemoved(CvPlot *pPlot, FeatureTypes eFeature, CvCity* pCity)
{
	m_kPythonEventMgr.reportPlotFeatureRemoved(pPlot, eFeature, pCity);
}

void CvEventReporter::plotPicked(CvPlot *pPlot)
{
	m_kPythonEventMgr.reportPlotPicked(pPlot);
}

void CvEventReporter::nukeExplosion(CvPlot *pPlot, CvUnit* pNukeUnit)
{
	m_kPythonEventMgr.reportNukeExplosion(pPlot, pNukeUnit);
}

void CvEventReporter::gotoPlotSet(CvPlot *pPlot, PlayerTypes ePlayer)
{
	m_kPythonEventMgr.reportGotoPlotSet(pPlot, ePlayer);
}

void CvEventReporter::cityBuilt(CvCity *pCity)
{
	m_kPythonEventMgr.reportCityBuilt(pCity);
	m_kStatistics.cityBuilt(pCity);
}

void CvEventReporter::cityRazed(CvCity *pCity, PlayerTypes ePlayer)
{
	m_kPythonEventMgr.reportCityRazed(pCity, ePlayer);
	m_kStatistics.cityRazed(pCity, ePlayer);
}

void CvEventReporter::cityAcquired(PlayerTypes eOldOwner, PlayerTypes iPlayer, CvCity* pCity, bool bConquest, bool bTrade)
{
	m_kPythonEventMgr.reportCityAcquired(eOldOwner, iPlayer, pCity, bConquest, bTrade);
}

void CvEventReporter::cityAcquiredAndKept(PlayerTypes iPlayer, CvCity* pCity)
{
	m_kPythonEventMgr.reportCityAcquiredAndKept(iPlayer, pCity);
}

void CvEventReporter::cityLost( CvCity *pCity)
{
	m_kPythonEventMgr.reportCityLost(pCity);
}

// doc: city gifted event
void CvEventReporter::cityGifted(CvCity* pCity)
{
    m_kPythonEventMgr.reportCityGifted(pCity);
}

// doc: city liberated event
void CvEventReporter::cityLiberated(CvCity* pCity)
{
    m_kPythonEventMgr.reportCityLiberated(pCity);
}

void CvEventReporter::cultureExpansion(CvCity *pCity, PlayerTypes ePlayer)
{
	m_kPythonEventMgr.reportCultureExpansion(pCity, ePlayer);
}

void CvEventReporter::cityGrowth(CvCity *pCity, PlayerTypes ePlayer)
{
	m_kPythonEventMgr.reportCityGrowth(pCity, ePlayer);
}

void CvEventReporter::cityDoTurn(CvCity *pCity, PlayerTypes ePlayer)
{
	m_kPythonEventMgr.reportCityProduction(pCity, ePlayer);
}

void CvEventReporter::cityBuildingUnit(CvCity* pCity, UnitTypes eUnitType)
{
	m_kPythonEventMgr.reportCityBuildingUnit(pCity, eUnitType);
}

void CvEventReporter::cityBuildingBuilding(CvCity* pCity, BuildingTypes eBuildingType)
{
	m_kPythonEventMgr.reportCityBuildingBuilding(pCity, eBuildingType);
}

void CvEventReporter::cityRename(CvCity* pCity)
{
	m_kPythonEventMgr.reportCityRename(pCity);
}

void CvEventReporter::cityHurry(CvCity* pCity, HurryTypes eHurry)
{
	m_kPythonEventMgr.reportCityHurry(pCity, eHurry);
}

// doc: city capture gold event
void CvEventReporter::cityCaptureGold(CvCity* pCity, PlayerTypes ePlayer, int iCaptureGold)
{
	m_kPythonEventMgr.reportCityCaptureGold(pCity, ePlayer, iCaptureGold);
}

void CvEventReporter::selectionGroupPushMission(CvSelectionGroup* pSelectionGroup, MissionTypes eMission)
{
	m_kPythonEventMgr.reportSelectionGroupPushMission(pSelectionGroup, eMission);
}

void CvEventReporter::unitMove(CvPlot* pPlot, CvUnit* pUnit, CvPlot* pOldPlot)
{
	m_kPythonEventMgr.reportUnitMove(pPlot, pUnit, pOldPlot);
}

void CvEventReporter::unitSetXY(CvPlot* pPlot, CvUnit* pUnit)
{
	m_kPythonEventMgr.reportUnitSetXY(pPlot, pUnit);
}

void CvEventReporter::unitCreated(CvUnit *pUnit)
{
	m_kPythonEventMgr.reportUnitCreated(pUnit);
}

void CvEventReporter::unitBuilt(CvCity *pCity, CvUnit *pUnit)
{
	m_kPythonEventMgr.reportUnitBuilt(pCity, pUnit);
	m_kStatistics.unitBuilt(pUnit);
}

void CvEventReporter::unitKilled(CvUnit *pUnit, PlayerTypes eAttacker)
{
	m_kPythonEventMgr.reportUnitKilled(pUnit, eAttacker);
	m_kStatistics.unitKilled(pUnit, eAttacker);
}

void CvEventReporter::unitLost(CvUnit *pUnit)
{
	m_kPythonEventMgr.reportUnitLost(pUnit);
}

void CvEventReporter::unitPromoted(CvUnit *pUnit, PromotionTypes ePromotion)
{
	m_kPythonEventMgr.reportUnitPromoted(pUnit, ePromotion);
}

void CvEventReporter::unitSelected( CvUnit *pUnit)
{
	m_kPythonEventMgr.reportUnitSelected(pUnit);
}

void CvEventReporter::unitRename(CvUnit* pUnit)
{
	m_kPythonEventMgr.reportUnitRename(pUnit);
}

void CvEventReporter::unitPillage(CvUnit* pUnit, ImprovementTypes eImprovement, RouteTypes eRoute, PlayerTypes ePlayer, int iPillagedGold)
{
	m_kPythonEventMgr.reportUnitPillage(pUnit, eImprovement, eRoute, ePlayer, iPillagedGold);
}

void CvEventReporter::unitSpreadReligionAttempt(CvUnit* pUnit, ReligionTypes eReligion, bool bSuccess)
{
	m_kPythonEventMgr.reportUnitSpreadReligionAttempt(pUnit, eReligion, bSuccess);
}

void CvEventReporter::unitGifted(CvUnit* pUnit, PlayerTypes eGiftingPlayer, CvPlot* pPlotLocation)
{
	m_kPythonEventMgr.reportUnitGifted(pUnit, eGiftingPlayer, pPlotLocation);
}

void CvEventReporter::unitBuildImprovement(CvUnit* pUnit, BuildTypes eBuild, bool bFinished)
{
	m_kPythonEventMgr.reportUnitBuildImprovement(pUnit, eBuild, bFinished);
}

void CvEventReporter::goodyReceived(PlayerTypes ePlayer, CvPlot *pGoodyPlot, CvUnit *pGoodyUnit, GoodyTypes eGoodyType)
{
	m_kPythonEventMgr.reportGoodyReceived(ePlayer, pGoodyPlot, pGoodyUnit, eGoodyType);
}

void CvEventReporter::greatPersonBorn(CvUnit *pUnit, PlayerTypes ePlayer, CvCity *pCity)
{
	m_kPythonEventMgr.reportGreatPersonBorn( pUnit, ePlayer, pCity);
	m_kStatistics.unitBuilt(pUnit);
}

void CvEventReporter::buildingBuilt(CvCity *pCity, BuildingTypes eBuilding)
{
	m_kPythonEventMgr.reportBuildingBuilt(pCity, eBuilding);
	m_kStatistics.buildingBuilt(pCity, eBuilding);
}

void CvEventReporter::projectBuilt(CvCity *pCity, ProjectTypes eProject)
{
	m_kPythonEventMgr.reportProjectBuilt(pCity, eProject);
}

void CvEventReporter::techAcquired(TechTypes eType, TeamTypes eTeam, PlayerTypes ePlayer, bool bAnnounce)
{
	m_kPythonEventMgr.reportTechAcquired(eType, eTeam, ePlayer, bAnnounce);
}

void CvEventReporter::techSelected(TechTypes eTech, PlayerTypes ePlayer)
{
	m_kPythonEventMgr.reportTechSelected(eTech, ePlayer);
}

void CvEventReporter::religionFounded(ReligionTypes eType, PlayerTypes ePlayer)
{
	m_kPythonEventMgr.reportReligionFounded(eType, ePlayer);
	m_kStatistics.religionFounded(eType, ePlayer);
}

void CvEventReporter::religionSpread(ReligionTypes eType, PlayerTypes ePlayer, CvCity* pSpreadCity)
{
	m_kPythonEventMgr.reportReligionSpread(eType, ePlayer, pSpreadCity);
}

void CvEventReporter::religionRemove(ReligionTypes eType, PlayerTypes ePlayer, CvCity* pSpreadCity)
{
	m_kPythonEventMgr.reportReligionRemove(eType, ePlayer, pSpreadCity);
}

void CvEventReporter::corporationFounded(CorporationTypes eType, PlayerTypes ePlayer)
{
	m_kPythonEventMgr.reportCorporationFounded(eType, ePlayer);
}

void CvEventReporter::corporationSpread(CorporationTypes eType, PlayerTypes ePlayer, CvCity* pSpreadCity)
{
	m_kPythonEventMgr.reportCorporationSpread(eType, ePlayer, pSpreadCity);
}

void CvEventReporter::corporationRemove(CorporationTypes eType, PlayerTypes ePlayer, CvCity* pSpreadCity)
{
	m_kPythonEventMgr.reportCorporationRemove(eType, ePlayer, pSpreadCity);
}

void CvEventReporter::goldenAge(PlayerTypes ePlayer)
{
	m_kPythonEventMgr.reportGoldenAge(ePlayer);
	m_kStatistics.goldenAge(ePlayer);
}

void CvEventReporter::endGoldenAge(PlayerTypes ePlayer)
{
	m_kPythonEventMgr.reportEndGoldenAge(ePlayer);
}

void CvEventReporter::changeWar(bool bWar, TeamTypes eTeam, TeamTypes eOtherTeam, bool bFromDefensivePact)
{
	m_kPythonEventMgr.reportChangeWar(bWar, eTeam, eOtherTeam, bFromDefensivePact);
}

void CvEventReporter::setPlayerAlive(PlayerTypes ePlayerID, bool bNewValue)
{
	m_kPythonEventMgr.reportSetPlayerAlive(ePlayerID, bNewValue);
}

void CvEventReporter::playerChangeStateReligion(PlayerTypes ePlayerID, ReligionTypes eNewReligion, ReligionTypes eOldReligion)
{
	m_kPythonEventMgr.reportPlayerChangeStateReligion(ePlayerID, eNewReligion, eOldReligion);
}

void CvEventReporter::playerGoldTrade(PlayerTypes eFromPlayer, PlayerTypes eToPlayer, int iAmount)
{
	m_kPythonEventMgr.reportPlayerGoldTrade(eFromPlayer, eToPlayer, iAmount);
}

// doc (edead): revolution event
void CvEventReporter::revolution(PlayerTypes ePlayerID)
{
    m_kPythonEventMgr.reportRevolution(ePlayerID);
}

/*	advc.make: To get rid of the K-Mod friend declaration in the header.
	Not const because CvStatistics performs lazy initialization of player records. */
CvPlayerRecord const* CvEventReporter::getPlayerRecord(PlayerTypes ePlayer)
{
	return m_kStatistics.getPlayerRecord(ePlayer);
}

void CvEventReporter::chat(CvWString szString)
{
	m_kPythonEventMgr.reportChat(szString);
}

void CvEventReporter::victory(TeamTypes eWinner, VictoryTypes eVictory)
{
	m_kPythonEventMgr.reportVictory(eWinner, eVictory);
	m_kStatistics.setVictory(eWinner, eVictory);

	// Set all human player's final total time played
	for (int i = 0; i < MAX_PLAYERS; ++i)
	{
		if (GET_PLAYER((PlayerTypes)i).isEverAlive())
		{
			m_kStatistics.setTimePlayed((PlayerTypes)i, GET_PLAYER((PlayerTypes)i).getTotalTimePlayed());
		}
	}
	gDLL->reportStatistics(); // automatically report MP stats on victory
}

void CvEventReporter::vassalState(TeamTypes eMaster, TeamTypes eVassal, bool bVassal, bool bCapitulated)
{
	m_kPythonEventMgr.reportVassalState(eMaster, eVassal, bVassal, bCapitulated);
}

// doc: trade mission event
void CvEventReporter::tradeMission(UnitTypes unitID, PlayerTypes ePlayer, int iX, int iY, int iGold)
{
	m_kPythonEventMgr.reportTradeMission(unitID, ePlayer, iX, iY, iGold);
}

// doc: slave trade event
void CvEventReporter::playerSlaveTrade(PlayerTypes ePlayer, int iGold)
{
	m_kPythonEventMgr.reportPlayerSlaveTrade(ePlayer, iGold);
}

// doc: civilization released event
void CvEventReporter::releasedCivilization(PlayerTypes ePlayer, CivilizationTypes eReleasedCivilization)
{
	m_kPythonEventMgr.reportReleasedCivilization(ePlayer, eReleasedCivilization);
}

// doc: blockade event
void CvEventReporter::blockade(PlayerTypes ePlayer, CvCity* pCity, int iGold)
{
	m_kPythonEventMgr.reportBlockade(ePlayer, pCity, iGold);
}

// doc: peace brokered event
void CvEventReporter::peaceBrokered(PlayerTypes eBroker, PlayerTypes ePlayer1, PlayerTypes ePlayer2)
{
	m_kPythonEventMgr.reportPeaceBrokered(eBroker, ePlayer1, ePlayer2);
}

// doc: XML loaded before menu
void CvEventReporter::xmlLoaded()
{
	m_kPythonEventMgr.reportXMLLoaded();
}

// doc: fonts loaded and font IDs assigned
void CvEventReporter::fontsLoaded()
{
	m_kPythonEventMgr.reportFontsLoaded();
}

// doc: civic changed event
void CvEventReporter::civicChanged(PlayerTypes ePlayer, CivicTypes eOldCivic, CivicTypes eNewCivic)
{
	m_kPythonEventMgr.reportCivicChanged(ePlayer, eOldCivic, eNewCivic);
}

// doc: autoplay ended event
void CvEventReporter::autoplayEnded()
{
	m_kPythonEventMgr.reportAutoplayEnded();
}

// doc: player civilization assigned event
void CvEventReporter::playerCivAssigned(PlayerTypes ePlayer, CivilizationTypes eNewCivilization)
{
	m_kPythonEventMgr.reportPlayerCivAssigned(ePlayer, eNewCivilization);
}

// doc: player destroyed event
void CvEventReporter::playerDestroyed(PlayerTypes ePlayer)
{
	m_kPythonEventMgr.reportPlayerDestroyed(ePlayer);
}

// doc: player switched event
void CvEventReporter::playerSwitch(PlayerTypes eOldPlayer, PlayerTypes eNewPlayer)
{
	m_kPythonEventMgr.reportPlayerSwitch(eOldPlayer, eNewPlayer);
}

// doc: tech traded event
void CvEventReporter::techTraded(PlayerTypes eFrom, PlayerTypes eTo, TechTypes eTech)
{
	m_kPythonEventMgr.reportTechTraded(eFrom, eTo, eTech);
}

// doc: tribute given event
void CvEventReporter::tribute(PlayerTypes eFrom, PlayerTypes eTo)
{
	m_kPythonEventMgr.reportTribute(eFrom, eTo);
}

// doc: global warming event
void CvEventReporter::globalWarming(int iGlobalWarmingValue, int iGlobalWarmingDefense)
{
	m_kPythonEventMgr.reportGlobalWarming(iGlobalWarmingValue, iGlobalWarmingDefense);
}

// doc: global warming effect event
void CvEventReporter::globalWarmingEffect(CvPlot* pPlot, bool bChanged, TerrainTypes ePreviousTerrain, TerrainTypes eNewTerrain, FeatureTypes ePreviousFeature)
{
	m_kPythonEventMgr.reportGlobalWarmingEffect(pPlot, bChanged, ePreviousTerrain, eNewTerrain, ePreviousFeature);
}

// doc: building processed event
void CvEventReporter::buildingProcessed(CvCity* pCity, BuildingTypes eBuilding, int iChange)
{
	m_kPythonEventMgr.reportBuildingProcessed(pCity, eBuilding, iChange);
}

// doc: city sacked event
void CvEventReporter::citySacked(CvCity* pCity)
{
	m_kPythonEventMgr.reportCitySacked(pCity);
}

void CvEventReporter::preSave()
{
	m_kPythonEventMgr.preSave();
	/*  <advc.106l> The original "saving" messages are disabled through game text XML
		b/c the EXE displays them for too long. Will show replacement messages here. */
	bool bAutoSave = m_bPreAutoSave;
	bool bQuickSave = m_bPreQuickSave;
	m_bPreAutoSave = m_bPreQuickSave = false;
	FAssertMsg(bAutoSave || !GC.getGame().isInBetweenTurns() ||
			GC.getInitCore().getPbem() || GC.getGame().isNetworkMultiPlayer(),
			"Quicksave in between turns?");
	char const* szDefineName = "";
	CvWString szMsgTag;
	if(bAutoSave)
	{
		szDefineName = "AUTO_SAVING_MESSAGE_TIME";
		szMsgTag = L"TXT_KEY_AUTOSAVING2";
	}
	else if(bQuickSave)
	{
		szDefineName = "QUICK_SAVING_MESSAGE_TIME";
		szMsgTag = L"TXT_KEY_QUICK_SAVING2";
	}
	else
	{
		szDefineName = "SAVING_MESSAGE_TIME";
		szMsgTag = L"TXT_KEY_SAVING_GAME2";
	}
	int iLength = GC.getDefineINT(szDefineName);
	if(iLength <= 0)
		return;
	PlayerTypes eActivePlayer = GC.getGame().getActivePlayer();
	if(eActivePlayer == NO_PLAYER)
	{
		FAssert(eActivePlayer != NO_PLAYER);
		return;
	}
	gDLL->UI().addMessage(eActivePlayer, true,
			iLength, gDLL->getText(szMsgTag), NULL, MESSAGE_TYPE_DISPLAY_ONLY);
}

void CvEventReporter::preAutoSave()
{
	/*  Can detect failed auto-saves here, but only if AutoSaveInterval=1 in the INI.
		Can't test in the DLL if that's the case. (Can't parse the INI file either;
		it could be any file passed to the EXE at startup through ini="...") */
	//FAssertMsg(!m_bPreAutoSave || GC.getGame().isNetworkMultiPlayer(), "Should've been reset by preSave");
	m_bPreAutoSave = true;
}

void CvEventReporter::preQuickSave()
{
	//FAssertMsg(!m_bPreAutoSave || GC.getGame().isNetworkMultiPlayer(), "Should've been reset by preSave");
	m_bPreQuickSave = true;
} // </advc.106l>

void CvEventReporter::windowActivation(bool bActive)
{
	m_kPythonEventMgr.reportWindowActivation(bActive);
}

void CvEventReporter::getGameStatistics(std::vector<CvStatBase*>& aStats)
{
	aStats.clear();
	aStats.push_back(new CvStatString("mapname", m_kStatistics.getMapName()));
	aStats.push_back(new CvStatInt("era", m_kStatistics.getEra()));

	// Report game params governing some server-side loops
	aStats.push_back(new CvStatInt("numplayers", MAX_CIV_PLAYERS));
	aStats.push_back(new CvStatInt("numunittypes", GC.getNumUnitInfos()));
	aStats.push_back(new CvStatInt("numbuildingtypes", GC.getNumBuildingInfos()));
	aStats.push_back(new CvStatInt("numreligiontypes", GC.getNumReligionInfos()));
}

void CvEventReporter::getPlayerStatistics(PlayerTypes ePlayer, std::vector<CvStatBase*>& aStats)
{
	aStats.clear();
	CvPlayerRecord* pRecord = m_kStatistics.getPlayerRecord(ePlayer);
	if (pRecord != NULL)
	{
		aStats.push_back(new CvStatInt("victorytype", pRecord->getVictory()));
		aStats.push_back(new CvStatInt("timeplayed", pRecord->getMinutesPlayed()));
		aStats.push_back(new CvStatInt("leader", pRecord->getLeader()-1));  // -1 because index 0 is barb
		aStats.push_back(new CvStatInt("citiesbuilt", pRecord->getNumCitiesBuilt()));
		aStats.push_back(new CvStatInt("citiesrazed", pRecord->getNumCitiesRazed()));
		aStats.push_back(new CvStatInt("goldenages", pRecord->getNumGoldenAges()));

		CvString strKey;
		FOR_EACH_ENUM(Unit)
		{
			strKey.format("unit_%d_built", eLoopUnit);
			aStats.push_back(new CvStatInt(strKey,
					pRecord->getNumUnitsBuilt(eLoopUnit)));
			strKey.format("unit_%d_killed", eLoopUnit);
			aStats.push_back(new CvStatInt(strKey,
					pRecord->getNumUnitsKilled(eLoopUnit)));
			strKey.format("unit_%d_lost", eLoopUnit);
			aStats.push_back(new CvStatInt(strKey,
					pRecord->getNumUnitsWasKilled(eLoopUnit)));
		}

		FOR_EACH_ENUM(Building)
		{
			strKey.format("building_%d_built", eLoopBuilding);
			aStats.push_back(new CvStatInt(strKey,
					pRecord->getNumBuildingsBuilt(eLoopBuilding)));
		}

		FOR_EACH_ENUM(Religion)
		{
			strKey.format("religion_%d_founded", eLoopReligion);
			aStats.push_back(new CvStatInt(strKey,
					pRecord->getReligionFounded(eLoopReligion)));
		}
	}
}

void CvEventReporter::readStatistics(FDataStreamBase* pStream)
{
	m_kStatistics.reset();
	m_kStatistics.read(pStream);
	GC.getGame().onAllGameDataRead(); // advc
}

void CvEventReporter::writeStatistics(FDataStreamBase* pStream)
{
	PROFILE_FUNC(); // advc
	REPRO_TEST_BEGIN_WRITE("Statistics");
	m_kStatistics.write(pStream);
	REPRO_TEST_FINAL_WRITE();
}
