#ifndef CIV4_DLL_PYTHON_EVENTS_H
#define CIV4_DLL_PYTHON_EVENTS_H

class CyArgsList;
enum CallbackDefines; // advc.003y

class CvDllPythonEvents
{
public:
	// <advc.003y>
	CvDllPythonEvents();
	~CvDllPythonEvents();
	void initCallbackGuards(); // </advc.003y>
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
	void reportRestoredContact(TeamTypes iTeamID1, TeamTypes iTeamID2); // doc
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
	void reportCityGifted(CvCity* pCity); // doc
	void reportCityLiberated(CvCity* pCity); // doc
	void reportCultureExpansion(CvCity *pCity, PlayerTypes ePlayer);
	void reportCityGrowth(CvCity *pCity, PlayerTypes ePlayer);
	void reportCityProduction(CvCity *pCity, PlayerTypes ePlayer);
	void reportCityBuildingUnit(CvCity *pCity, UnitTypes eUnitType);
	void reportCityBuildingBuilding(CvCity *pCity, BuildingTypes eBuildingType);
	void reportCityRename(CvCity *pCity);
	void reportCityHurry(CvCity *pCity, HurryTypes eHurry);
	void reportCityCaptureGold(CvCity *pCity, PlayerTypes ePlayer, int iCaptureGold); // doc
	void reportCitySacked(CvCity* pCity); // doc

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
	void reportUnitPillage(CvUnit* pUnit, ImprovementTypes eImprovement, RouteTypes eRoute, PlayerTypes ePlayer, int iPillagedGold);
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
	void reportChangeWar(bool bWar, TeamTypes eTeam, TeamTypes eOtherTeam, bool bFromDefensivePact);
	void reportChat(CvWString szString);
	void reportVictory(TeamTypes eNewWinner, VictoryTypes eNewVictory);

	void reportVassalState(TeamTypes eMaster, TeamTypes eVassal, bool bVassal, bool bCapitulated);
	void reportRevolution(PlayerTypes ePlayerID); // doc (edead)

	void reportTradeMission(UnitTypes unitID, PlayerTypes ePlayer, int iX, int iY, int iGold); // doc
	void reportPlayerSlaveTrade(PlayerTypes ePlayer, int iGold); // doc
	void reportReleasedCivilization(PlayerTypes ePlayer, CivilizationTypes eReleasedCivilization); // doc
	void reportBlockade(PlayerTypes ePlayer, CvCity* pCity, int iGold); // doc
	void reportPeaceBrokered(PlayerTypes eBroker, PlayerTypes ePlayer1, PlayerTypes ePlayer2); // doc
	void reportXMLLoaded(); // doc
	void reportFontsLoaded(); // doc
	void reportCivicChanged(PlayerTypes ePlayer, CivicTypes eOldCivic, CivicTypes eNewCivic); // doc
	void reportAutoplayEnded(); // doc
	void reportPlayerCivAssigned(PlayerTypes ePlayer, CivilizationTypes eNewCivilization); // doc
	void reportPlayerDestroyed(PlayerTypes ePlayer); // doc
	void reportPlayerSwitch(PlayerTypes eOldPlayer, PlayerTypes eNewPlayer); // doc
	void reportTechTraded(PlayerTypes eFrom, PlayerTypes eTo, TechTypes eTech); // doc
	void reportTribute(PlayerTypes eFrom, PlayerTypes eTo); // doc
	void reportGlobalWarming(int iGlobalWarmingValue, int iGlobalWarmingDefense); // doc
	void reportGlobalWarmingEffect(CvPlot* pPlot, bool bChanged, TerrainTypes ePreviousTerrain, TerrainTypes eNewTerrain, FeatureTypes ePreviousFeature); // doc
	void reportBuildingProcessed(CvCity* pCity, BuildingTypes eBuilding, int iChange); // doc

	void reportSetPlayerAlive(PlayerTypes ePlayerID, bool bNewValue);
	void reportPlayerChangeStateReligion(PlayerTypes ePlayerID, ReligionTypes eNewReligion, ReligionTypes eOldReligion);
	void reportPlayerGoldTrade(PlayerTypes eFromPlayer, PlayerTypes eToPlayer, int iAmount);

	void preSave();

private:
	// <advc.003y>
	bool* m_abUseCallback;

	bool isUse(CallbackDefines eCallback) const
	{
		return (m_abUseCallback == NULL ? false : m_abUseCallback[eCallback]);
	} // </advc.003y>
	bool preEvent();
	bool postEvent(CyArgsList& eventData);
};

#endif
