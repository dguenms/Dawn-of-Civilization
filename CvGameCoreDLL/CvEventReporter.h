#pragma once

#ifndef CvEventReporter_h
#define CvEventReporter_h

#include "CvStatistics.h"
#include "CvDllPythonEvents.h"

//
// A singleton class which is used to track game events.
// It will report events to python and the stats collector.
//

struct CvStatBase;
struct TradeData;
class CyDiplomacyTrade;
class CvUnit;
class CvCity;
class CvPlot;
class CvSelectionGroup;
class CvEventReporter
{
	friend class CyStatistics;
public:
	DllExport static CvEventReporter& getInstance();		// singleton accessor
	DllExport void resetStatistics();

	DllExport bool mouseEvent(int evt, int iCursorX, int iCursorY, bool bInterfaceConsumed=false);												
	DllExport bool kbdEvent(int evt, int key, int iCursorX, int iCursorY);
	void genericEvent(const char* szEventName, void *pyArgs);

	DllExport void newGame();
	DllExport void newPlayer(PlayerTypes ePlayer);

	DllExport void reportModNetMessage(int iData1, int iData2, int iData3, int iData4, int iData5);
	
	DllExport void init();
	DllExport void update(float fDeltaTime);
	DllExport void unInit();
	DllExport void gameStart();
	void gameEnd();
	DllExport void windowActivation(bool bActive);

	void beginGameTurn(int iGameTurn);
	void endGameTurn(int iGameTurn);

	void beginPlayerTurn(int iGameTurn, PlayerTypes);
	void endPlayerTurn(int iGameTurn, PlayerTypes);

	void firstContact(TeamTypes eTeamID1, TeamTypes eTeamID2);						
	void combatResult(CvUnit* pWinner, CvUnit* pLoser);					
// BUG - Combat Events - start
	void combatRetreat(CvUnit* pAttacker, CvUnit* pDefender);
	void combatWithdrawal(CvUnit* pAttacker, CvUnit* pDefender);
	void combatLogCollateral(CvUnit* pAttacker, CvUnit* pDefender, int iDamage);
	void combatLogFlanking(CvUnit* pAttacker, CvUnit* pDefender, int iDamage);
// BUG - Combat Events - start
	void improvementBuilt(int iImprovementType, int iX, int iY);	
	void improvementDestroyed(int iImprovementType, int iPlayer, int iX, int iY);	
	void routeBuilt(int iRouteType, int iX, int iY);	
	
	void plotRevealed(CvPlot *pPlot, TeamTypes eTeam);
	void plotFeatureRemoved(CvPlot *pPlot, FeatureTypes eFeature, CvCity* pCity);
	DllExport void plotPicked(CvPlot *pPlot);
	void nukeExplosion(CvPlot *pPlot, CvUnit* pNukeUnit);
	DllExport void gotoPlotSet(CvPlot *pPlot, PlayerTypes ePlayer);

	void cityBuilt(CvCity *pCity);
	void cityRazed(CvCity *pCity, PlayerTypes ePlayer);
	void cityAcquired(PlayerTypes eOldOwner, PlayerTypes ePlayer, CvCity* pCity, bool bConquest, bool bTrade);
	void cityAcquiredAndKept(PlayerTypes ePlayer, CvCity* pCity);
	void cityLost(CvCity *pCity);
	void cultureExpansion( CvCity *pCity, PlayerTypes ePlayer);
	void cityGrowth(CvCity *pCity, PlayerTypes ePlayer);
	void cityDoTurn(CvCity *pCity, PlayerTypes ePlayer);
	void cityBuildingUnit(CvCity* pCity, UnitTypes eUnitType);
	void cityBuildingBuilding(CvCity* pCity, BuildingTypes eBuildingType);
// BUG - Project Started Event - start
	void cityBuildingProject(CvCity* pCity, ProjectTypes eProjectType);
// BUG - Project Started Event - end
// BUG - Process Started Event - start
	void cityBuildingProcess(CvCity* pCity, ProcessTypes eProcessType);
// BUG - Process Started Event - end
	void cityRename(CvCity* pCity);
	void cityHurry(CvCity* pCity, HurryTypes eHurry);
	void cityCaptureGold(CvCity* pCity, PlayerTypes ePlayer, int iCaptureGold);

	void selectionGroupPushMission(CvSelectionGroup* pSelectionGroup, MissionTypes eMission);

	void unitMove(CvPlot* pPlot, CvUnit* pUnit, CvPlot* pOldPlot);					
	void unitSetXY(CvPlot* pPlot, CvUnit* pUnit);					
	void unitCreated(CvUnit *pUnit);
	void unitBuilt(CvCity *pCity, CvUnit *pUnit);
	void unitKilled(CvUnit *pUnit, PlayerTypes eAttacker);
// BUG - Unit Captured Event - start
	void unitCaptured(PlayerTypes eFromPlayer, UnitTypes eUnitType, CvUnit* pNewUnit);
// BUG - Unit Captured Event - end
	void unitLost(CvUnit *pUnit);
	void unitPromoted(CvUnit *pUnit, PromotionTypes ePromotion);
// BUG - Upgrade Unit Event - start
	void unitUpgraded(CvUnit *pOldUnit, CvUnit *pNewUnit, int iPrice);
// BUG - Upgrade Unit Event - end
	DllExport void unitSelected(CvUnit *pUnit);
	void unitRename(CvUnit* pUnit);
	void unitPillage(CvUnit* pUnit, ImprovementTypes eImprovement, RouteTypes eRoute, PlayerTypes ePlayer, int iPillagedGold);
	void unitSpreadReligionAttempt(CvUnit* pUnit, ReligionTypes eReligion, bool bSuccess);
	void unitGifted(CvUnit* pUnit, PlayerTypes eGiftingPlayer, CvPlot* pPlotLocation);
	void unitBuildImprovement(CvUnit* pUnit, BuildTypes eBuild, bool bFinished);
	
	void goodyReceived(PlayerTypes ePlayer, CvPlot *pGoodyPlot, CvUnit *pGoodyUnit, GoodyTypes eGoodyType);
	
	void greatPersonBorn(CvUnit *pUnit, PlayerTypes ePlayer, CvCity *pCity );

	void buildingBuilt(CvCity *pCity, BuildingTypes eBuilding);
	void projectBuilt(CvCity *pCity, ProjectTypes eProject);

	void techAcquired(TechTypes eType, TeamTypes eTeam, PlayerTypes ePlayer, bool bAnnounce);		
	void techSelected(TechTypes eTech, PlayerTypes ePlayer);

	void religionFounded(ReligionTypes eType, PlayerTypes ePlayer);
	void religionSpread(ReligionTypes eType, PlayerTypes ePlayer, CvCity* pSpreadCity);
	void religionRemove(ReligionTypes eType, PlayerTypes ePlayer, CvCity* pSpreadCity);

	void corporationFounded(CorporationTypes eType, PlayerTypes ePlayer);
	void corporationSpread(CorporationTypes eType, PlayerTypes ePlayer, CvCity* pSpreadCity);
	void corporationRemove(CorporationTypes eType, PlayerTypes ePlayer, CvCity* pSpreadCity);

	void goldenAge(PlayerTypes ePlayer);
	void endGoldenAge(PlayerTypes ePlayer);
	void changeWar(bool bWar, TeamTypes eTeam, TeamTypes eOtherTeam);

	void setPlayerAlive( PlayerTypes ePlayerID, bool bNewValue );
	void playerChangeStateReligion(PlayerTypes ePlayerID, ReligionTypes eNewReligion, ReligionTypes eOldReligion);
	void playerGoldTrade(PlayerTypes eFromPlayer, PlayerTypes eToPlayer, int iAmount);

	void revolution(PlayerTypes ePlayerID); // edead

	DllExport void chat(CvWString szString);		

	void victory(TeamTypes eWinner, VictoryTypes eVictory);

	void vassalState(TeamTypes eMaster, TeamTypes eVassal, bool bVassal, bool bCapitulated);

	void tradeMission(UnitTypes unitID, PlayerTypes ePlayer, int iX, int iY, int iGold); // Leoreth
	void diplomaticMission(UnitTypes unitID, PlayerTypes ePlayer, int iX, int iY, bool bMadePeace); // 1SDAN
	void playerSlaveTrade(PlayerTypes ePlayer, int iGold); // Leoreth
	void releasedPlayer(PlayerTypes ePlayer, PlayerTypes eReleasedPlayer); // Leoreth
	void blockade(PlayerTypes ePlayer, int iGold); // Leoreth
	void peaceBrokered(PlayerTypes eBroker, PlayerTypes ePlayer1, PlayerTypes ePlayer2); // Leoreth

	void bordersOpened(PlayerTypes ePlayer1, PlayerTypes ePlayer2); // Steb
	void bordersClosed(PlayerTypes ePlayer1, PlayerTypes ePlayer2); // Steb

	DllExport void preSave();

	DllExport void getGameStatistics(std::vector<CvStatBase*>& aStats);
	DllExport void getPlayerStatistics(PlayerTypes ePlayer, std::vector<CvStatBase*>& aStats);
	DllExport void readStatistics(FDataStreamBase* pStream);
	DllExport void writeStatistics(FDataStreamBase* pStream);

private:
	CvDllPythonEvents m_kPythonEventMgr;
	CvStatistics m_kStatistics;
};

// helper
#define EVENT_REPORTER CvEventReporter::getInstance()	

#endif	// CvEventReporter_h
