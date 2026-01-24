#pragma once

#ifndef CvEventReporter_h
#define CvEventReporter_h

#include "CvStatistics.h"
#include "CvDllPythonEvents.h"

//
// A singleton class which is used to track game events.
// It will report events to python and the stats collector.
//

/*class CyDiplomacyTrade;
struct TradeData;*/ // advc: not used
struct CvStatBase;
class CvUnit;
class CvCity;
class CvPlot;
class CvSelectionGroup;
struct CombatDetails; // advc

class CvEventReporter
{
	friend class CyStatistics;
	/*  advc.make: Want to precompile this header, so CvPlayer.h can't be included.
		I've instead added a public CvEventReporter::getPlayerRecord function. */
	//friend const CvPlayerRecord* CvPlayer::getPlayerRecord() const; // K-Mod. Allow direct read-only access to player stats
	CvEventReporter(); // advc.106l
public:
	DllExport static CvEventReporter& getInstance();		// singleton accessor
	DllExport void resetStatistics();
	void initPythonCallbackGuards(); //n advc.003y

	DllExport bool mouseEvent(int evt, int iCursorX, int iCursorY, bool bInterfaceConsumed=false);
	DllExport bool kbdEvent(int evt, int key, int iCursorX, int iCursorY);
	void genericEvent(const char* szEventName, void *pyArgs);

	DllExport void newGame();
	DllExport void newPlayer(PlayerTypes ePlayer);

	void reportModNetMessage(int iData1, int iData2, int iData3, int iData4, int iData5);

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
	void restoredContact(TeamTypes eTeamID1, TeamTypes eTeamID2); // doc
	void combatResult(CvUnit* pWinner, CvUnit* pLoser);
	// advc:
	void combatLogHit(CombatDetails const& kAttackerDetails,
			CombatDetails const& kDefenderDetails,
			int iDamage, bool bAttackerTakesHit);
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
	void cityGifted(CvCity* pCity); // doc
	void cityLiberated(CvCity* pCity); // doc
	void cultureExpansion( CvCity *pCity, PlayerTypes ePlayer);
	void cityGrowth(CvCity *pCity, PlayerTypes ePlayer);
	void cityDoTurn(CvCity *pCity, PlayerTypes ePlayer);
	void cityBuildingUnit(CvCity* pCity, UnitTypes eUnitType);
	void cityBuildingBuilding(CvCity* pCity, BuildingTypes eBuildingType);
	void cityRename(CvCity* pCity);
	void cityHurry(CvCity* pCity, HurryTypes eHurry);
	void cityCaptureGold(CvCity* pCity, PlayerTypes ePlayer, int iCaptureGold); // doc
	void citySacked(CvCity* pCity); // doc

	void selectionGroupPushMission(CvSelectionGroup* pSelectionGroup, MissionTypes eMission);

	void unitMove(CvPlot* pPlot, CvUnit* pUnit, CvPlot* pOldPlot);
	void unitSetXY(CvPlot* pPlot, CvUnit* pUnit);
	void unitCreated(CvUnit *pUnit);
	void unitBuilt(CvCity *pCity, CvUnit *pUnit);
	void unitKilled(CvUnit *pUnit, PlayerTypes eAttacker);
	void unitLost(CvUnit *pUnit);
	void unitPromoted(CvUnit *pUnit, PromotionTypes ePromotion);
	DllExport void unitSelected(CvUnit *pUnit);
	void unitRename(CvUnit* pUnit);
	void unitPillage(CvUnit* pUnit, ImprovementTypes eImprovement, RouteTypes eRoute, PlayerTypes ePlayer, int iPillagedGold);
	void unitSpreadReligionAttempt(CvUnit* pUnit, ReligionTypes eReligion, bool bSuccess);
	void unitGifted(CvUnit* pUnit, PlayerTypes eGiftingPlayer, CvPlot* pPlotLocation);
	void unitBuildImprovement(CvUnit* pUnit, BuildTypes eBuild, bool bFinished);

	void goodyReceived(PlayerTypes ePlayer, CvPlot *pGoodyPlot, CvUnit *pGoodyUnit, GoodyTypes eGoodyType);

	void greatPersonBorn(CvUnit *pUnit, PlayerTypes ePlayer, CvCity *pCity);

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
	void changeWar(bool bWar, TeamTypes eTeam, TeamTypes eOtherTeam, bool bFromDefensivePact);

	void setPlayerAlive(PlayerTypes ePlayerID, bool bNewValue);
	void playerChangeStateReligion(PlayerTypes ePlayerID, ReligionTypes eNewReligion, ReligionTypes eOldReligion);
	void playerGoldTrade(PlayerTypes eFromPlayer, PlayerTypes eToPlayer, int iAmount);
	CvPlayerRecord const* getPlayerRecord(PlayerTypes ePlayer); // advc.make

	void revolution(PlayerTypes ePlayerID); // doc (edead)

	DllExport void chat(CvWString szString);

	void victory(TeamTypes eWinner, VictoryTypes eVictory);

	void vassalState(TeamTypes eMaster, TeamTypes eVassal, bool bVassal, bool bCapitulated);

	void tradeMission(UnitTypes unitID, PlayerTypes ePlayer, int iX, int iY, int iGold); // doc
	void playerSlaveTrade(PlayerTypes ePlayer, int iGold); // doc
	void releasedCivilization(PlayerTypes ePlayer, CivilizationTypes eReleasedCivilization); // doc
	void blockade(PlayerTypes ePlayer, CvCity* pCity, int iGold); // doc
	void peaceBrokered(PlayerTypes eBroker, PlayerTypes ePlayer1, PlayerTypes ePlayer2); // doc
	void xmlLoaded(); // doc
	void fontsLoaded(); // doc
	void civicChanged(PlayerTypes ePlayer, CivicTypes eOldCivic, CivicTypes eNewCivic); // doc
	void autoplayEnded(); // doc
	void playerCivAssigned(PlayerTypes ePlayer, CivilizationTypes eNewCivilization); // doc
	void playerDestroyed(PlayerTypes ePlayer); // doc
	void playerSwitch(PlayerTypes eOldPlayer, PlayerTypes eNewPlayer); // doc
	void techTraded(PlayerTypes eFrom, PlayerTypes eTo, TechTypes eTech); // doc
	void tribute(PlayerTypes eFrom, PlayerTypes eTo); // doc
	void globalWarming(int iGlobalWarmingValue, int iGlobalWarmingDefense); // doc
	void globalWarmingEffect(CvPlot* pPlot, bool bChanged, TerrainTypes ePreviousTerrain, TerrainTypes eNewTerrain, FeatureTypes ePreviousFeature); // doc
	void buildingProcessed(CvCity* pCity, BuildingTypes eBuilding, int iChange); // doc

	DllExport void preSave();
	// <advc.106l> Will call these before (and in addition to) preSave
	void preAutoSave();
	void preQuickSave();
	// </advc.106l>
	DllExport void getGameStatistics(std::vector<CvStatBase*>& aStats);
	DllExport void getPlayerStatistics(PlayerTypes ePlayer, std::vector<CvStatBase*>& aStats);
	DllExport void readStatistics(FDataStreamBase* pStream);
	DllExport void writeStatistics(FDataStreamBase* pStream);

private:
	CvDllPythonEvents m_kPythonEventMgr;
	CvStatistics m_kStatistics;
	// <advc.106l>
	bool m_bPreAutoSave;
	bool m_bPreQuickSave;
	// </advc.106l>
};

// helper
#define EVENT_REPORTER CvEventReporter::getInstance()

#endif	// CvEventReporter_h
