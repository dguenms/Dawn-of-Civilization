#ifndef CIV4_DLL_PYTHON_EVENTS_H
#define CIV4_DLL_PYTHON_EVENTS_H

class CyArgsList;

class CvDllPythonEvents
{
public:
	void reportGenericEvent(const char* szEventName, void *pyArgs);
	bool reportKbdEvent(int evt, int key, int iCursorX, int iCursorY);
	bool reportMouseEvent(int evt, int iCursorX, int iCursorY, bool bInterfaceConsumed=false);												
	void reportModNetMessage(int iData1, int iData2, int iData3, int iData4, int iData5);

	void reportInit();
	void reportUpdate(float fDeltaTime);
	void reportUnInit();
	void reportGameStart();
	void reportGameEnd();
	void reportWindowActivation(bool bActive);

	void reportBeginGameTurn(int iGameTurn);
	void reportEndGameTurn(int iGameTurn);

	void reportBeginPlayerTurn(int iGameTurn, PlayerTypes);
	void reportEndPlayerTurn(int iGameTurn, PlayerTypes);

	void reportFirstContact(TeamTypes iTeamID1, TeamTypes iTeamID2);						
	void reportCombatResult(CvUnit* pWinner, CvUnit* pLoser);					
	void reportImprovementBuilt(int iImprovementType, int iX, int iY);	
	void reportImprovementDestroyed(int iImprovementType, int iPlayer, int iX, int iY);	
	void reportRouteBuilt(int iRouteType, int iX, int iY);	

	void reportPlotRevealed(CvPlot *pPlot, TeamTypes eTeam);
	void reportPlotFeatureRemoved(CvPlot *pPlot, FeatureTypes eFeature, CvCity* pCity);
	void reportPlotPicked(CvPlot *pPlot);
	void reportNukeExplosion(CvPlot *pPlot, CvUnit* pNukeUnit);
	void reportGotoPlotSet(CvPlot *pPlot, PlayerTypes ePlayer);

	void reportCityBuilt(CvCity *pCity);
	void reportCityRazed(CvCity *pCity, PlayerTypes ePlayer);
	void reportCityAcquired(PlayerTypes eOldOwner, PlayerTypes ePlayer, CvCity* pOldCity, bool bConquest, bool bTrade);
	void reportCityAcquiredAndKept(PlayerTypes ePlayer, CvCity* pCity);
	void reportCityLost(CvCity *pCity);
	void reportCultureExpansion(CvCity *pCity, PlayerTypes ePlayer);
	void reportCityGrowth(CvCity *pCity, PlayerTypes ePlayer);
	void reportCityProduction(CvCity *pCity, PlayerTypes ePlayer);
	void reportCityBuildingUnit(CvCity *pCity, UnitTypes eUnitType);
	void reportCityBuildingBuilding(CvCity *pCity, BuildingTypes eBuildingType);
	void reportCityRename(CvCity *pCity);
	void reportCityHurry(CvCity *pCity, HurryTypes eHurry);

	void reportSelectionGroupPushMission(CvSelectionGroup* pSelectionGroup, MissionTypes eMission);

	void reportUnitMove(CvPlot* pPlot, CvUnit* pUnit, CvPlot* pOldPlot);					
	void reportUnitSetXY(CvPlot* pPlot, CvUnit* pUnit);					
	void reportUnitCreated(CvUnit *pUnit);
	void reportUnitBuilt(CvCity *pCity, CvUnit *pUnit);
	void reportUnitKilled(CvUnit *pUnit, PlayerTypes eAttacker);			
	void reportUnitLost(CvUnit *pUnit);
	void reportUnitPromoted(CvUnit* pUnit, PromotionTypes ePromotion);
	void reportUnitSelected(CvUnit *pUnit);
	void reportUnitRename(CvUnit *pUnit);
	void reportUnitPillage(CvUnit* pUnit, ImprovementTypes eImprovement, RouteTypes eRoute, PlayerTypes ePlayer);
	void reportUnitSpreadReligionAttempt(CvUnit* pUnit, ReligionTypes eReligion, bool bSuccess);
	void reportUnitGifted(CvUnit* pUnit, PlayerTypes eGiftingPlayer, CvPlot* pPlotLocation);
	void reportUnitBuildImprovement(CvUnit* pUnit, BuildTypes eBuild, bool bFinished);

	void reportGoodyReceived(PlayerTypes ePlayer, CvPlot *pGoodyPlot, CvUnit *pGoodyUnit, GoodyTypes eGoodyType);

	void reportGreatPersonBorn(CvUnit *pUnit, PlayerTypes ePlayer, CvCity *pCity);

	void reportBuildingBuilt(CvCity *pCity, BuildingTypes eBuilding);
	void reportProjectBuilt(CvCity *pCity, ProjectTypes eProject);

	void reportTechAcquired(TechTypes eType, TeamTypes eTeam, PlayerTypes ePlayer, bool bAnnounce);
	void reportTechSelected(TechTypes eTech, PlayerTypes ePlayer);

	void reportReligionFounded(ReligionTypes eType, PlayerTypes ePlayer);
	void reportReligionSpread(ReligionTypes eType, PlayerTypes ePlayer, CvCity* pSpreadCity);
	void reportReligionRemove(ReligionTypes eType, PlayerTypes ePlayer, CvCity* pSpreadCity);

	void reportCorporationFounded(CorporationTypes eType, PlayerTypes ePlayer);
	void reportCorporationSpread(CorporationTypes eType, PlayerTypes ePlayer, CvCity* pSpreadCity);
	void reportCorporationRemove(CorporationTypes eType, PlayerTypes ePlayer, CvCity* pSpreadCity);

	void reportGoldenAge(PlayerTypes ePlayer);
	void reportEndGoldenAge(PlayerTypes ePlayer);
	void reportChangeWar(bool bWar, TeamTypes eTeam, TeamTypes eOtherTeam);
	void reportChat(CvWString szString);				
	void reportVictory(TeamTypes eNewWinner, VictoryTypes eNewVictory);

	void reportVassalState(TeamTypes eMaster, TeamTypes eVassal, bool bVassal);

	void reportSetPlayerAlive(PlayerTypes ePlayerID, bool bNewValue);
	void reportPlayerChangeStateReligion(PlayerTypes ePlayerID, ReligionTypes eNewReligion, ReligionTypes eOldReligion);
	void reportPlayerGoldTrade(PlayerTypes eFromPlayer, PlayerTypes eToPlayer, int iAmount);

	void preSave();

private:
	bool preEvent();
	bool postEvent(CyArgsList& eventData);
};

#endif
