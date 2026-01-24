#pragma once

#ifndef _CVDLLWIDGETDATA_H_
#define _CVDLLWIDGETDATA_H_


class CvDLLWidgetData
{

public:

	DllExport static CvDLLWidgetData& getInstance();
	DllExport static void freeInstance();

	//	This will parse the help for the widget
	DllExport void parseHelp(CvWStringBuffer &szBuffer, CvWidgetDataStruct &widgetDataStruct);

	//	This will execute the action for the widget
	DllExport bool executeAction(CvWidgetDataStruct &widgetDataStruct);

	//	This will execute an alternate action for the widget
	DllExport bool executeAltAction(CvWidgetDataStruct &widgetDataStruct);

	DllExport bool isLink(const CvWidgetDataStruct &widgetDataStruct) const;

	//	Actions to be executed
	void doPlotList(CvWidgetDataStruct &widgetDataStruct);
	void doPlotListShift(int iChange, bool bMaxStep = false); // advc
	void doLiberateCity();
	void doRenameCity();
	void doRenameUnit();
	void doCreateGroup();
	void doDeleteGroup();
	void doTrain(CvWidgetDataStruct &widgetDataStruct);
	void doConstruct(CvWidgetDataStruct &widgetDataStruct);
	void doCreate(CvWidgetDataStruct &widgetDataStruct);
	void doMaintain(CvWidgetDataStruct &widgetDataStruct);
	void doHurry(CvWidgetDataStruct &widgetDataStruct);
	void doConscript();
	void doAction(CvWidgetDataStruct &widgetDataStruct);
	void doChangeSpecialist(CvWidgetDataStruct &widgetDataStruct);
	void doResearch(CvWidgetDataStruct &widgetDataStruct);
	void doChangePercent(CvWidgetDataStruct &widgetDataStruct);
	void doChangePercentAlt(CvWidgetDataStruct &widgetDataStruct); // K-Mod (right-click)
	void doCityTab(CvWidgetDataStruct &widgetDataStruct);
	void doContactCiv(CvWidgetDataStruct &widgetDataStruct);
	void doConvert(CvWidgetDataStruct &widgetDataStruct);
	void doAutomateCitizens();
	void doAutomateProduction();
	void doEmphasize(CvWidgetDataStruct &widgetDataStruct);
	void doCancelCivics();
	void applyCityEdit();
	void doUnitModel();
	void doFlag();
	void doSelected(CvWidgetDataStruct &widgetDataStruct);
	void doPediaCultureLevelJump(CvWidgetDataStruct &widgetDataStruct); // doc // TODO: move
	void doFinanceAdvisor(CvWidgetDataStruct &widgetDataStruct); // doc // TODO: move?
	/*  advc.003y: Replaced the doPedia.... functions with jumpToPedia functions
		in CvPythonCaller */
	void doGotoTurnEvent(CvWidgetDataStruct &widgetDataStruct);
	void doDealKill(CvWidgetDataStruct &widgetDataStruct);
	void doMenu();
	void doLaunch(CvWidgetDataStruct &widgetDataStruct);

protected:

	static CvDLLWidgetData* m_pInst;

	//	Help parsing (advc: These were all public)
	void parsePlotListHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseLiberateCityHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseCityNameHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseTrainHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseConstructHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseCreateHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseMaintainHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseHurryHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseConscriptHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseActionHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	// <advc>
	void parseActionHelp_Mission(CvActionInfo const& kAction, CvUnit const& kUnit,
			MissionTypes eMission, CvWStringBuffer& szBuffer); // </advc>
	void parseDiscoverHelp(CvPlot* pMissionPlot, CvWStringBuffer& szBuffer); // doc
	void parseCitizenHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseFreeCitizenHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseDisabledCitizenHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseAngryCitizenHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseChangeSpecialistHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseResearchHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseTechTreeHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseChangePercentHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseContactCivHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseScoreboardCheatText(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer); // K-Mod, the cheat mode text associated with ContactCivHelp
	void parseCompleteStabilityInfo(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer); // rfc
	void parseHistoricalVictoryInfo(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer); // rfc
	void parseScoreHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	// BULL - Trade Hover:
	void parseTradeRoutes(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	// BULL - Food Rate Hover:
	void parseFoodModHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	// <advc.085>
	void parsePowerRatioHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseGoldenAgeAnarchyHelp(PlayerTypes ePlayer, int iData2, bool bAnarchy, CvWStringBuffer &szBuffer);
	// </advc.085>
	void parseConvertHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseRevolutionHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	// void parsePopupQueue(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseAutomateCitizensHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseAutomateProductionHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseEmphasizeHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseTradeItem(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseUnitModelHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseFlagHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseMaintenanceHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseNationalityHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseHealthHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseHappinessHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parsePopulationHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseProductionHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseCultureHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseGreatPeopleHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseGreatGeneralHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseGreatSpyHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer); // doc
	void parseSelectedHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseTradeRouteCityHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseEspionageCostHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseBuildingHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseProjectHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseTerrainHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseFeatureHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseTechEntryHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	// BULL - Trade Denial - start
	void parseTechTradeEntryHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	// BULL - Trade Denial - end
	void parseTechPrereqHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseTechTreePrereq(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer, bool bTechTreeInfo);
	void parseCultureLevelHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseObsoleteHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseObsoleteBonusString(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseObsoleteSpecialHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseMoveHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseFreeUnitHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseFeatureProductionHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseWorkerRateHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseTradeRouteHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseHealthRateHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseHappinessRateHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseFreeTechHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseLOSHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseMapCenterHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseMapRevealHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseMapTradeHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseTechTradeHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseGoldTradeHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseOpenBordersHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseDefensivePactHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parsePermanentAllianceHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseVassalStateHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseBuildBridgeHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseIrrigationHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseIgnoreIrrigationHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseWaterWorkHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseBuildHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseDomainExtraMovesHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseAdjustHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseTerrainTradeHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseSpecialBuildingHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseYieldChangeHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseBonusRevealHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseBonusPlayerTradeHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer); // doc
	void parseCivicRevealHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseProcessInfoHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseFoundReligionHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseFoundCorporationHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseFinanceNumUnits(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseFinanceUnitCost(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseFinanceAwaySupply(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseFinanceCityMaint(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseFinanceCivicUpkeep(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseFinanceForeignIncome(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseFinanceInflatedCosts(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseFinanceGrossIncome(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseFinanceNetGold(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseFinanceGoldReserve(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	// BULL - Finance Advisor - start
	void parseFinanceDomesticTrade(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseFinanceForeignTrade(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseFinanceSpecialistGold(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	// BULL - Finance Advisor - end
	void parseUnitHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parsePediaBack(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parsePediaForward(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseBonusHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseBonusHelpCity(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer); // doc
	// BULL - Trade Denial - start
	void parseBonusTradeHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	// BULL - Trade Denial - end
	void parseReligionHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseReligionHelpCity(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseCorporationHelpCity(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseCorporationHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parsePromotionHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseEventHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseUnitCombatHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseImprovementHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseCivicHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseCivilizationHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseLeaderHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	// BULL - Leaderhead Relations:
	void parseLeaderheadRelationsHelp(CvWidgetDataStruct& widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseDescriptionHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer, bool bMinimal);
	void parseCloseScreenHelp(CvWStringBuffer &szBuffer);
	void parseKillDealHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseProductionModHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseLeaderheadHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseLeaderLineHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parseCommerceModHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	/*  K-Mod, 5/jan/11, karadoc
		Environmental advisor mouse-over text */
	void parsePollutionOffsetsHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	void parsePollutionHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer);
	// K-Mod end  <advc.ctr>
	bool parseCityTradeHelp(CvWidgetDataStruct const& kWidget, CvCity*& pCity,
	PlayerTypes& eWhoTo) const; // </advc.ctr>

    void parseStabilityExpansionHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer); // doc
    void parseStabilityEconomyHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer); // doc
    void parseStabilityDomesticHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer); // doc
    void parseStabilityForeignHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer); // doc
    void parseStabilityMilitaryHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer); // doc
    void parseStabilityHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer); // doc

    void parsePaganReligionHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer); // doc // TODO: move?
    void doPediaPaganReligionHelp(CvWidgetDataStruct &widgetDataStruct); // doc // TODO: move?

    void parseRouteHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer); // doc // TODO: move?
    void doPediaRouteJump(CvWidgetDataStruct &widgetDataStruct); // doc // TODO: move?

    void parseWonderLimitHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer); // doc
    void parseSatelliteLimitHelp(CvWidgetDataStruct& widgetDataStruct, CvWStringBuffer& szBuffer); // doc
    void parseFirstDiscoveredHelp(CvWidgetDataStruct& widgetDataStruct, CvWStringBuffer& szBuffer); // doc
};

#endif
