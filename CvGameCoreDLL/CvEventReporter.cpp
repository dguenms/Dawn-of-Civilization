#include "CvGameCoreDLL.h"
#include "CvEventReporter.h"
#include "CvDllPythonEvents.h"
#include "CvInitCore.h"

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

//
// Returns true if the event is consumed by Python
//
bool CvEventReporter::mouseEvent(int evt, int iCursorX, int iCursorY, bool bInterfaceConsumed)
{
	return m_kPythonEventMgr.reportMouseEvent(evt, iCursorX, iCursorY, bInterfaceConsumed);
}

//
// Returns true if the event is consumed by Python
//
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
	// This will only be called if statistics are being reported!
	// Called at the launch of a game (new or loaded)

	// Report initial stats for the game
	m_kStatistics.setMapName( CvString(GC.getInitCore().getMapScriptName()).GetCString() );
	m_kStatistics.setEra(GC.getInitCore().getEra());
}

void CvEventReporter::newPlayer(PlayerTypes ePlayer)
{
	// This will only be called if statistics are being reported!
	// Called at the launch of a game (new or loaded)

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

void CvEventReporter::combatResult(CvUnit* pWinner, CvUnit* pLoser)
{
	m_kPythonEventMgr.reportCombatResult(pWinner, pLoser);
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

void CvEventReporter::cityBuilt( CvCity *pCity )
{
	m_kPythonEventMgr.reportCityBuilt(pCity);
	m_kStatistics.cityBuilt(pCity);
}

void CvEventReporter::cityRazed( CvCity *pCity, PlayerTypes ePlayer )
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

void CvEventReporter::cultureExpansion( CvCity *pCity, PlayerTypes ePlayer )
{
	m_kPythonEventMgr.reportCultureExpansion(pCity, ePlayer);
}

void CvEventReporter::cityGrowth(CvCity *pCity, PlayerTypes ePlayer)
{
	m_kPythonEventMgr.reportCityGrowth(pCity, ePlayer);
}

void CvEventReporter::cityDoTurn( CvCity *pCity, PlayerTypes ePlayer )
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

void CvEventReporter::unitKilled(CvUnit *pUnit, PlayerTypes eAttacker )
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

void CvEventReporter::unitPillage(CvUnit* pUnit, ImprovementTypes eImprovement, RouteTypes eRoute, PlayerTypes ePlayer)
{
	m_kPythonEventMgr.reportUnitPillage(pUnit, eImprovement, eRoute, ePlayer);
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

void CvEventReporter::changeWar(bool bWar, TeamTypes eTeam, TeamTypes eOtherTeam)
{
	m_kPythonEventMgr.reportChangeWar(bWar, eTeam, eOtherTeam);
}

void CvEventReporter::setPlayerAlive( PlayerTypes ePlayerID, bool bNewValue )
{
	m_kPythonEventMgr.reportSetPlayerAlive( ePlayerID, bNewValue );
}

void CvEventReporter::playerChangeStateReligion(PlayerTypes ePlayerID, ReligionTypes eNewReligion, ReligionTypes eOldReligion)
{
	m_kPythonEventMgr.reportPlayerChangeStateReligion(ePlayerID, eNewReligion, eOldReligion);
}

void CvEventReporter::playerGoldTrade(PlayerTypes eFromPlayer, PlayerTypes eToPlayer, int iAmount)
{
	m_kPythonEventMgr.reportPlayerGoldTrade(eFromPlayer, eToPlayer, iAmount);
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

	// automatically report MP stats on victory
	gDLL->reportStatistics();
}

void CvEventReporter::vassalState(TeamTypes eMaster, TeamTypes eVassal, bool bVassal)
{
	m_kPythonEventMgr.reportVassalState(eMaster, eVassal, bVassal);
}

void CvEventReporter::preSave()
{
	m_kPythonEventMgr.preSave();
}

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


		// Units by type
		CvString strKey;
		for (int j = 0; j < GC.getNumUnitInfos(); ++j)
		{
			strKey.format("unit_%d_built", j);
			aStats.push_back(new CvStatInt(strKey, pRecord->getNumUnitsBuilt(j)));

			strKey.format("unit_%d_killed", j);
			aStats.push_back(new CvStatInt(strKey, pRecord->getNumUnitsKilled(j)));

			strKey.format("unit_%d_lost", j);
			aStats.push_back(new CvStatInt(strKey, pRecord->getNumUnitsWasKilled(j)));
		}

		// Buildings by type
		for (int j = 0; j < GC.getNumBuildingInfos(); ++j)
		{
			strKey.format("building_%d_built", j);
			aStats.push_back(new CvStatInt(strKey, pRecord->getNumBuildingsBuilt((BuildingTypes)j)));
		}

		// Religions by type
		for (int j = 0; j < GC.getNumReligionInfos(); ++j)
		{
			strKey.format("religion_%d_founded", j);
			aStats.push_back(new CvStatInt(strKey, pRecord->getReligionFounded((ReligionTypes)j)));
		}
	}
}

void CvEventReporter::readStatistics(FDataStreamBase* pStream)
{
	m_kStatistics.reset();
	m_kStatistics.read(pStream);
}
void CvEventReporter::writeStatistics(FDataStreamBase* pStream)
{
	m_kStatistics.write(pStream);
}

