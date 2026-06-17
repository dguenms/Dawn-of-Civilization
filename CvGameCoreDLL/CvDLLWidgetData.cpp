#include "CvGameCoreDLL.h"
#include "CvDLLWidgetData.h"
#include "CoreAI.h"
#include "CvCityAI.h"
#include "CvUnit.h"
#include "CvSelectionGroup.h"
#include "CvDeal.h"
#include "PlotRange.h"
#include "CvGameTextMgr.h"
#include "CvPopupInfo.h"
#include "CvMessageControl.h"
#include "CvInfo_All.h"
#include "CvBugOptions.h"
#include "WarEvaluator.h" // advc.104l
#include "RiseFall.h" // advc.706


CvDLLWidgetData* CvDLLWidgetData::m_pInst = NULL;

CvDLLWidgetData& CvDLLWidgetData::getInstance()
{
	if (m_pInst == NULL)
		m_pInst = new CvDLLWidgetData;
	return *m_pInst;
}

void CvDLLWidgetData::freeInstance()
{
	delete m_pInst;
	m_pInst = NULL;
}

// advc:
namespace
{
	__inline PlayerTypes getActivePlayer()
	{
		return GC.getGame().getActivePlayer();
	}
	__inline TeamTypes getActiveTeam()
	{
		return GC.getGame().getActiveTeam();
	}
}

void CvDLLWidgetData::parseHelp(CvWStringBuffer &szBuffer, CvWidgetDataStruct &widgetDataStruct)
{
	// <advc.085> Replacing a few sporadic tests in the parse... functions
	static WidgetTypes aePlayerAsData1[] =
	{
		WIDGET_HELP_FINANCE_AWAY_SUPPLY, WIDGET_HELP_FINANCE_CITY_MAINT,
		WIDGET_HELP_FINANCE_CIVIC_UPKEEP, WIDGET_HELP_FINANCE_DOMESTIC_TRADE,
		WIDGET_HELP_FINANCE_FOREIGN_INCOME, WIDGET_HELP_FINANCE_INFLATED_COSTS,
		WIDGET_HELP_FINANCE_NUM_UNITS, WIDGET_HELP_FINANCE_SPECIALISTS,
		WIDGET_HELP_FINANCE_UNIT_COST,
		WIDGET_LEADERHEAD, WIDGET_LEADERHEAD_RELATIONS, WIDGET_LEADER_LINE,
		WIDGET_CONTACT_CIV, WIDGET_SCORE_BREAKDOWN, WIDGET_POWER_RATIO,
		WIDGET_GOLDEN_AGE, WIDGET_ANARCHY
	};
	for (int i = 0; i < ARRAYSIZE(aePlayerAsData1); i++)
	{
		if (widgetDataStruct.m_eWidgetType == aePlayerAsData1[i] &&
			(widgetDataStruct.m_iData1 <= NO_PLAYER ||
			widgetDataStruct.m_iData1 >= MAX_PLAYERS))
		{
			FErrorMsg("Player id missing in widget data");
			return;
		}
	} // </advc.085>
	/*	advc: (Note - Better not to assume that this is valid, widgets might perhaps
		get triggered while returning to opening menu or sth. like that.) */
	PlayerTypes const eActivePlayer = getActivePlayer();
	switch (widgetDataStruct.m_eWidgetType)
	{
	case WIDGET_PLOT_LIST:
		parsePlotListHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PLOT_LIST_SHIFT:
		szBuffer.assign(gDLL->getText("TXT_KEY_MISC_CTRL_SHIFT",
				GC.getDefineINT("MAX_PLOT_LIST_SIZE") - 1));
		break;

	case WIDGET_CITY_SCROLL:
		break;

	case WIDGET_LIBERATE_CITY:
		parseLiberateCityHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_CITY_NAME:
		parseCityNameHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_UNIT_NAME:
		szBuffer.append(gDLL->getText("TXT_KEY_CHANGE_NAME"));
		break;

	case WIDGET_CREATE_GROUP:
		szBuffer.append(gDLL->getText("TXT_KEY_WIDGET_CREATE_GROUP"));
		break;

	case WIDGET_DELETE_GROUP:
		szBuffer.append(gDLL->getText("TXT_KEY_WIDGET_DELETE_GROUP"));
		break;

	case WIDGET_TRAIN:
		parseTrainHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_CONSTRUCT:
		parseConstructHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_CREATE:
		parseCreateHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_MAINTAIN:
		parseMaintainHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HURRY:
		parseHurryHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_MENU_ICON:
		szBuffer.append(gDLL->getText("TXT_KEY_MAIN_MENU"));

	case WIDGET_CONSCRIPT:
		parseConscriptHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_ACTION:
		parseActionHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_CITIZEN:
		parseCitizenHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_FREE_CITIZEN:
		parseFreeCitizenHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_DISABLED_CITIZEN:
		parseDisabledCitizenHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_ANGRY_CITIZEN:
		parseAngryCitizenHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_CHANGE_SPECIALIST:
		parseChangeSpecialistHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_RESEARCH:
		parseResearchHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_TECH_TREE:
		parseTechTreeHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_CHANGE_PERCENT:
		parseChangePercentHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_CITY_TAB:
	{
		CvWString szTemp;
		szTemp.Format(L"%s", GC.getInfo((CityTabTypes)widgetDataStruct.m_iData1).getDescription());
		szBuffer.assign(szTemp);
		break;
	}

	case WIDGET_CONTACT_CIV:
		parseContactCivHelp(widgetDataStruct, szBuffer);
		break;
	// advc.085 (comment): Was unused in BtS; now used on the scoreboard.
	case WIDGET_SCORE_BREAKDOWN:
		parseScoreHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_ZOOM_CITY:
	case WIDGET_EXAMINE_CITY: // advc.186b
		szBuffer.append(gDLL->getText("TXT_KEY_ZOOM_CITY_HELP"));
		// BUG - Zoom City Details - start (advc.186b)
		if (widgetDataStruct.m_eWidgetType == WIDGET_EXAMINE_CITY &&
			// Only if the active player owns the city
			eActivePlayer == widgetDataStruct.m_iData1)
		{
			szBuffer.append(NEWLINE);
			GAMETEXT.setCityBarHelp(szBuffer,
					*GET_PLAYER((PlayerTypes)widgetDataStruct.m_iData1).
					getCity(widgetDataStruct.m_iData2));
		} // BUG - Zoom City Details - end
		break;

	case WIDGET_END_TURN:
		szBuffer.append(gDLL->getText("TXT_KEY_WIDGET_END_TURN"));
		break;

	case WIDGET_LAUNCH_VICTORY:
		szBuffer.append(gDLL->getText("TXT_KEY_WIDGET_LAUNCH_VICTORY"));
		break;

	case WIDGET_AUTOMATE_CITIZENS:
		parseAutomateCitizensHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_AUTOMATE_PRODUCTION:
		parseAutomateProductionHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_EMPHASIZE:
		parseEmphasizeHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_TRADE_ITEM:
		parseTradeItem(widgetDataStruct, szBuffer);
		break;

	case WIDGET_UNIT_MODEL:
		parseUnitModelHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_FLAG:
		parseFlagHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_MAINTENANCE:
		parseMaintenanceHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_RELIGION:
		parseReligionHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_RELIGION_CITY:
		parseReligionHelpCity(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_CORPORATION_CITY:
		parseCorporationHelpCity(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_NATIONALITY:
		parseNationalityHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_DEFENSE:
		break;

	case WIDGET_HELP_HEALTH:
		parseHealthHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_HAPPINESS:
		parseHappinessHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_POPULATION:
		parsePopulationHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_PRODUCTION:
		parseProductionHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_CULTURE:
		parseCultureHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_GREAT_PEOPLE:
		parseGreatPeopleHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_GREAT_GENERAL:
		parseGreatGeneralHelp(widgetDataStruct, szBuffer);
		break;

	// doc: great spy
	case WIDGET_HELP_GREAT_SPY:
		parseGreatSpyHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_SELECTED:
		parseSelectedHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_BUILDING:
		parseBuildingHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_TRADE_ROUTE_CITY:
		parseTradeRouteCityHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_ESPIONAGE_COST:
		parseEspionageCostHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_TECH_ENTRY:
		parseTechEntryHelp(widgetDataStruct, szBuffer);
		break;
	// BULL - Trade Denial - start
	case WIDGET_PEDIA_JUMP_TO_TECH_TRADE:
		parseTechTradeEntryHelp(widgetDataStruct, szBuffer);
		break;
	// BULL - Trade Denial - end
	case WIDGET_HELP_TECH_PREPREQ:
		parseTechPrereqHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_OBSOLETE:
		parseObsoleteHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_OBSOLETE_BONUS:
		parseObsoleteBonusString(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_OBSOLETE_SPECIAL:
		parseObsoleteSpecialHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_MOVE_BONUS:
		parseMoveHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_FREE_UNIT:
		parseFreeUnitHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_FEATURE_PRODUCTION:
		parseFeatureProductionHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_WORKER_RATE:
		parseWorkerRateHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_TRADE_ROUTES:
		parseTradeRouteHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_HEALTH_RATE:
		parseHealthRateHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_HAPPINESS_RATE:
		parseHappinessRateHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_FREE_TECH:
		parseFreeTechHelp(widgetDataStruct, szBuffer);
		break;
	// <advc.500c>
	case WIDGET_HELP_NO_FEAR_FOR_SAFETY:
		GAMETEXT.buildNoFearForSafetyString(szBuffer, (TechTypes)widgetDataStruct.m_iData1);
		break; // </advc.500c>

	case WIDGET_HELP_LOS_BONUS:
		parseLOSHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_MAP_CENTER:
		parseMapCenterHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_MAP_REVEAL:
		parseMapRevealHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_MAP_TRADE:
		parseMapTradeHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_TECH_TRADE:
		parseTechTradeHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_GOLD_TRADE:
		parseGoldTradeHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_OPEN_BORDERS:
		parseOpenBordersHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_DEFENSIVE_PACT:
		parseDefensivePactHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_PERMANENT_ALLIANCE:
		parsePermanentAllianceHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_VASSAL_STATE:
		parseVassalStateHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_BUILD_BRIDGE:
		parseBuildBridgeHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_IRRIGATION:
		parseIrrigationHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_IGNORE_IRRIGATION:
		parseIgnoreIrrigationHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_WATER_WORK:
		parseWaterWorkHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_IMPROVEMENT:
		parseBuildHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_DOMAIN_EXTRA_MOVES:
		parseDomainExtraMovesHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_ADJUST:
		parseAdjustHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_TERRAIN_TRADE:
		parseTerrainTradeHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_SPECIAL_BUILDING:
		parseSpecialBuildingHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_YIELD_CHANGE:
		parseYieldChangeHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_BONUS_REVEAL:
		parseBonusRevealHelp(widgetDataStruct, szBuffer);
		break;

	// doc: bonus player trade
	case WIDGET_HELP_BONUS_PLAYER_TRADE:
		parseBonusPlayerTradeHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_CIVIC_REVEAL:
		parseCivicRevealHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_PROCESS_INFO:
		parseProcessInfoHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_FOUND_RELIGION:
		parseFoundReligionHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_FOUND_CORPORATION:
		parseFoundCorporationHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_FINANCE_NUM_UNITS:
		parseFinanceNumUnits(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_FINANCE_UNIT_COST:
		parseFinanceUnitCost(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_FINANCE_AWAY_SUPPLY:
		parseFinanceAwaySupply(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_FINANCE_CITY_MAINT:
		parseFinanceCityMaint(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_FINANCE_CIVIC_UPKEEP:
		parseFinanceCivicUpkeep(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_FINANCE_FOREIGN_INCOME:
		parseFinanceForeignIncome(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_FINANCE_INFLATED_COSTS:
		parseFinanceInflatedCosts(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_FINANCE_GROSS_INCOME:
		parseFinanceGrossIncome(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_FINANCE_NET_GOLD:
		parseFinanceNetGold(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_FINANCE_GOLD_RESERVE:
		parseFinanceGoldReserve(widgetDataStruct, szBuffer);
		break;
	// BULL - Finance Advisor - start
	case WIDGET_HELP_FINANCE_DOMESTIC_TRADE:
		parseFinanceDomesticTrade(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_FINANCE_FOREIGN_TRADE:
		parseFinanceForeignTrade(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_FINANCE_SPECIALISTS:
		parseFinanceSpecialistGold(widgetDataStruct, szBuffer);
		break; // BULL - Finance Advisor - end

	case WIDGET_PEDIA_JUMP_TO_TECH:
		parseTechEntryHelp(widgetDataStruct, szBuffer);
	    break;

    // doc: stability help
	case WIDGET_HELP_STABILITY_EXPANSION:
	    parseStabilityExpansionHelp(widgetDataStruct, szBuffer);
	    break;

    // doc: stability help
	case WIDGET_HELP_STABILITY_ECONOMY:
	    parseStabilityEconomyHelp(widgetDataStruct, szBuffer);
	    break;

    // doc: stability help
	case WIDGET_HELP_STABILITY_DOMESTIC:
	    parseStabilityDomesticHelp(widgetDataStruct, szBuffer);
	    break;

	// doc: stability help
	case WIDGET_HELP_STABILITY_FOREIGN:
	    parseStabilityForeignHelp(widgetDataStruct, szBuffer);
	    break;

	// doc: stability help
	case WIDGET_HELP_STABILITY_MILITARY:
	    parseStabilityMilitaryHelp(widgetDataStruct, szBuffer);
	    break;

	// doc: stability help
	case WIDGET_HELP_STABILITY:
	    parseStabilityHelp(widgetDataStruct, szBuffer);
	    break;

	case WIDGET_PEDIA_JUMP_TO_REQUIRED_TECH:
		parseTechTreePrereq(widgetDataStruct, szBuffer, false);
		break;

	case WIDGET_PEDIA_JUMP_TO_DERIVED_TECH:
		parseTechTreePrereq(widgetDataStruct, szBuffer, true);
		break;

    // doc: culture level pedia
	case WIDGET_PEDIA_JUMP_TO_CULTURE_LEVEL:
		parseCultureLevelHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PEDIA_JUMP_TO_UNIT:
		parseUnitHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PEDIA_JUMP_TO_BUILDING:
		parseBuildingHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PEDIA_BACK:
		// parsePediaBack(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PEDIA_FORWARD:
		// parsePediaForward(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PEDIA_JUMP_TO_BONUS:
		parseBonusHelp(widgetDataStruct, szBuffer);
		break;

    // doc: city bonus help
	case WIDGET_HELP_BONUS_CITY:
		parseBonusHelpCity(widgetDataStruct, szBuffer);
		break;

// BUG - Trade Denial - start
	case WIDGET_PEDIA_JUMP_TO_BONUS_TRADE:
		parseBonusTradeHelp(widgetDataStruct, szBuffer);
		break;
// BUG - Trade Denial - end

	case WIDGET_PEDIA_MAIN:
		break;

	case WIDGET_PEDIA_JUMP_TO_PROMOTION:
	case WIDGET_HELP_PROMOTION:
		parsePromotionHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_CHOOSE_EVENT:
		parseEventHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT:
		parseUnitCombatHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PEDIA_JUMP_TO_IMPROVEMENT:
		parseImprovementHelp(widgetDataStruct, szBuffer);
		break;

	// doc: route pedia
	case WIDGET_PEDIA_JUMP_TO_ROUTE:
		parseRouteHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PEDIA_JUMP_TO_CIVIC:
		parseCivicHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PEDIA_JUMP_TO_CIV:
		parseCivilizationHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PEDIA_JUMP_TO_LEADER:
		parseLeaderHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PEDIA_JUMP_TO_SPECIALIST:
		if (widgetDataStruct.m_iData1 != NO_SPECIALIST && widgetDataStruct.m_iData2 != 0)
		{
			CvWString szTemp;
			szTemp.Format(L"%s", GC.getInfo((SpecialistTypes)widgetDataStruct.m_iData1).getDescription());
			szBuffer.assign(szTemp);
		}
		break;

	case WIDGET_PEDIA_JUMP_TO_PROJECT:
		parseProjectHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PEDIA_JUMP_TO_RELIGION:
		parseReligionHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PEDIA_JUMP_TO_CORPORATION:
		parseCorporationHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PEDIA_JUMP_TO_TERRAIN:
		parseTerrainHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PEDIA_JUMP_TO_FEATURE:
		parseFeatureHelp(widgetDataStruct, szBuffer);
		break;

	// doc: pagan religion pedia
	case WIDGET_PEDIA_JUMP_TO_PAGAN_RELIGION:
		parsePaganReligionHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PEDIA_DESCRIPTION:
		parseDescriptionHelp(widgetDataStruct, szBuffer, false);
		break;

	case WIDGET_CLOSE_SCREEN:
		//parseCloseScreenHelp(szBuffer);
		break;

	case WIDGET_DEAL_KILL:
		parseKillDealHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PEDIA_DESCRIPTION_NO_HELP:
		//parseDescriptionHelp(widgetDataStruct, szBuffer, true);
		break;

	case WIDGET_MINIMAP_HIGHLIGHT:
		// <advc.004> Leader help for Military Advisor
		if (widgetDataStruct.m_iData1 == 2) // mode id
		{
			PlayerTypes ePlayer = (PlayerTypes)widgetDataStruct.m_iData2;
			if (ePlayer > NO_PLAYER && ePlayer < MAX_CIV_PLAYERS)
				GAMETEXT.parseLeaderHeadHelp(szBuffer, ePlayer, NO_PLAYER);
		} // </advc.004>
		break;

	case WIDGET_PRODUCTION_MOD_HELP:
		parseProductionModHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_LEADERHEAD:
		parseLeaderheadHelp(widgetDataStruct, szBuffer);
		break;
	// <advc.152>
	case WIDGET_LH_GLANCE:
		//parseLeaderheadHelp(widgetDataStruct, szBuffer);
		parseLeaderheadRelationsHelp(widgetDataStruct, szBuffer); // BULL - Leaderhead Relations
		// Might as well call GAMETEXT right here
		GAMETEXT.parseWarTradesHelp(szBuffer, (PlayerTypes)widgetDataStruct.m_iData1,
				(PlayerTypes)widgetDataStruct.m_iData2);
		break; // </advc.152>
	// BULL - Leaderhead Relations - start
	case WIDGET_LEADERHEAD_RELATIONS:
		parseLeaderheadRelationsHelp(widgetDataStruct, szBuffer);
		break; // BULL - Leaderhead Relations - end

	case WIDGET_LEADER_LINE:
		parseLeaderLineHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_COMMERCE_MOD_HELP:
		parseCommerceModHelp(widgetDataStruct, szBuffer);
	    break;

    // doc (Merijn): wonder limit
	case WIDGET_HELP_WONDER_LIMIT:
	    parseWonderLimitHelp(widgetDataStruct, szBuffer);
	    break;

    // doc: satellite limit
	case WIDGET_HELP_SATELLITE_LIMIT:
	    parseSatelliteLimitHelp(widgetDataStruct, szBuffer);
	    break;

    // doc: first discovered in tech tree
	case WIDGET_FIRST_DISCOVERED:
	    parseFirstDiscoveredHelp(widgetDataStruct, szBuffer);
	    break;

	// K-Mod. Environmental advisor widgets.
	case WIDGET_HELP_POLLUTION_OFFSETS:
		parsePollutionOffsetsHelp(widgetDataStruct, szBuffer);
		break;
	case WIDGET_HELP_POLLUTION_SOURCE:
		parsePollutionHelp(widgetDataStruct, szBuffer);
		break;
	case WIDGET_HELP_SUSTAINABILITY_THRESHOLD:
		szBuffer.assign(gDLL->getText("TXT_KEY_SUSTAINABILITY_THRESHOLD_HELP"));
		break;
	case WIDGET_HELP_GW_RELATIVE_CONTRIBUTION:
		szBuffer.assign(gDLL->getText("TXT_KEY_GW_RELATIVE_CONTRIBUTION_HELP"));
		break;
	case WIDGET_HELP_GW_INDEX:
		szBuffer.assign(gDLL->getText("TXT_KEY_GW_INDEX_HELP"));
		break;
	case WIDGET_HELP_GW_UNHAPPY:
		szBuffer.assign(gDLL->getText("TXT_KEY_GW_UNHAPPY_HELP"));
		break;
	// K-Mod. Global commerce modifiers, extra specialist commerce
	case WIDGET_HELP_GLOBAL_COMMERCE_MODIFIER:
		GAMETEXT.setCommerceChangeHelp(szBuffer, L"", L"", gDLL->getText("TXT_KEY_CIVIC_IN_ALL_CITIES").GetCString(), GC.getInfo((TechTypes)(widgetDataStruct.m_iData1)).getCommerceModifierArray(), true, false);
		break;
	case WIDGET_HELP_EXTRA_SPECIALIST_COMMERCE:
		GAMETEXT.setCommerceChangeHelp(szBuffer, L"", L"", gDLL->getText("TXT_KEY_CIVIC_PER_SPECIALIST").GetCString(), GC.getInfo((TechTypes)(widgetDataStruct.m_iData1)).getSpecialistExtraCommerceArray(), false, false);
		break;
	// K-Mod end
	// <advc.706>
	case WIDGET_RF_CIV_CHOICE:
		GC.getGame().getRiseFall().assignCivSelectionHelp(szBuffer,
				(PlayerTypes)widgetDataStruct.m_iData1);
		break; // </advc.706>  <advc.ctr>
	case WIDGET_CITY_TRADE:
	{
		CvCity* pCity = NULL;
		PlayerTypes eWhoTo = NO_PLAYER;
		bool bListMore = parseCityTradeHelp(widgetDataStruct, pCity, eWhoTo);
		if (pCity != NULL)
			GAMETEXT.setCityTradeHelp(szBuffer, *pCity, eWhoTo, bListMore);
		break;
	} // </advc.ctr>  <advc.106i>
	case WIDGET_SHOW_REPLAY:
		szBuffer.append(gDLL->getText(widgetDataStruct.m_iData1 == 0 ?
				"TXT_KEY_HOF_SHOW_REPLAY" : "TXT_KEY_HOF_WARN"));
		break; // </advc.106i>
	// BULL - Trade Hover - start
	case WIDGET_TRADE_ROUTES:
	case WIDGET_TRADE_ROUTES_SCOREBOARD: // advc.085
		parseTradeRoutes(widgetDataStruct, szBuffer);
		break; // BULL - Trade Hover - end
	// BULL - Food Rate Hover - start
	case WIDGET_FOOD_MOD_HELP:
		parseFoodModHelp(widgetDataStruct, szBuffer);
		break; // BULL - Food Rate Hover - end
	// <advc.154>
	case WIDGET_CYCLE_UNIT:
		if (eActivePlayer != NO_PLAYER)
		{
			CvUnit const* pUnit = GET_PLAYER(eActivePlayer).
					getUnit(widgetDataStruct.m_iData2);
			if (pUnit == NULL)
				GAMETEXT.setUnselectUnitHelp(szBuffer);
			else GAMETEXT.setCycleUnitHelp(szBuffer, widgetDataStruct.m_iData1, *pUnit);
		}
		break; // </advc.154>
	// <advc.085>
	case WIDGET_EXPAND_SCORES:
		break; // Handled below (not the only widget that expands the scoreboard)
	case WIDGET_POWER_RATIO:
		parsePowerRatioHelp(widgetDataStruct, szBuffer);
		break;
	case WIDGET_GOLDEN_AGE:
		parseGoldenAgeAnarchyHelp((PlayerTypes)widgetDataStruct.m_iData1,
				widgetDataStruct.m_iData2, false, szBuffer);
		break;
	case WIDGET_ANARCHY:
		parseGoldenAgeAnarchyHelp((PlayerTypes)widgetDataStruct.m_iData1,
				widgetDataStruct.m_iData2, true, szBuffer);
		break;
	}
	if (getActivePlayer() == NO_PLAYER)
		return;
	static WidgetTypes aeExpandTypes[] =
	{
		WIDGET_CONTACT_CIV, WIDGET_DEAL_KILL, WIDGET_PEDIA_JUMP_TO_TECH,
		WIDGET_EXPAND_SCORES, WIDGET_SCORE_BREAKDOWN, WIDGET_POWER_RATIO,
		WIDGET_GOLDEN_AGE, WIDGET_ANARCHY
	};
	for(int i = 0; i < ARRAYSIZE(aeExpandTypes); i++)
	{
		if((widgetDataStruct.m_eWidgetType == aeExpandTypes[i] &&
			widgetDataStruct.m_iData2 == 0) ||
			// Need iData2 for sth. else; must only use these WidgetTypes on the scoreboard.
			widgetDataStruct.m_eWidgetType == WIDGET_TRADE_ROUTES_SCOREBOARD ||
			widgetDataStruct.m_eWidgetType == WIDGET_POWER_RATIO)
		{
			GET_PLAYER(getActivePlayer()).setScoreboardExpanded(true);
		}
	} // </advc.085>
}


bool CvDLLWidgetData::executeAction(CvWidgetDataStruct &widgetDataStruct)
{
	/*	Right now general bHandled = false;  We can specific-case this to true later.
		Game will run with this = false; */
	bool bHandled = false;
	// <advc.003y>
	CvPythonCaller const& py = *GC.getPythonCaller();
	int const iData1 = widgetDataStruct.m_iData1;
	int const iData2 = widgetDataStruct.m_iData2; // </advc.003y>
	switch (widgetDataStruct.m_eWidgetType)
	{
	case WIDGET_PLOT_LIST:
		doPlotList(widgetDataStruct);
		break;

	case WIDGET_PLOT_LIST_SHIFT:
		doPlotListShift(iData1); // advc: Moved into new function
		break;

	case WIDGET_CITY_SCROLL:
		if (iData1 > 0)
			GC.getGame().doControl(CONTROL_NEXTCITY);
		else GC.getGame().doControl(CONTROL_PREVCITY);
		break;

	case WIDGET_LIBERATE_CITY:
		doLiberateCity();
		break;

	case WIDGET_CITY_NAME:
		doRenameCity();
		break;

	case WIDGET_UNIT_NAME:
		doRenameUnit();
		break;

	case WIDGET_CREATE_GROUP:
		doCreateGroup();
		break;

	case WIDGET_DELETE_GROUP:
		doDeleteGroup();
		break;

	case WIDGET_TRAIN:
		doTrain(widgetDataStruct);
		break;

	case WIDGET_CONSTRUCT:
		doConstruct(widgetDataStruct);
		break;

	case WIDGET_CREATE:
		doCreate(widgetDataStruct);
		break;

	case WIDGET_MAINTAIN:
		doMaintain(widgetDataStruct);
		break;

	case WIDGET_HURRY:
		doHurry(widgetDataStruct);
		break;

	case WIDGET_MENU_ICON:
		doMenu();

	case WIDGET_CONSCRIPT:
		doConscript();
		break;

	case WIDGET_ACTION:
		doAction(widgetDataStruct);
		break;

	case WIDGET_CITIZEN:
		break;

	case WIDGET_FREE_CITIZEN:
		break;

	case WIDGET_DISABLED_CITIZEN:
		break;

	case WIDGET_ANGRY_CITIZEN:
		break;

	case WIDGET_CHANGE_SPECIALIST:
		doChangeSpecialist(widgetDataStruct);
		break;

	case WIDGET_RESEARCH:
	case WIDGET_TECH_TREE:
		doResearch(widgetDataStruct);
		break;

	case WIDGET_CHANGE_PERCENT:
		doChangePercent(widgetDataStruct);
		break;

	case WIDGET_CITY_TAB:
		doCityTab(widgetDataStruct);
		break;

	case WIDGET_CONTACT_CIV:
		doContactCiv(widgetDataStruct);
		break;

	case WIDGET_END_TURN:
		GC.getGame().doControl(CONTROL_FORCEENDTURN);
		break;

	case WIDGET_LAUNCH_VICTORY:
		doLaunch(widgetDataStruct);
		break;

	case WIDGET_CONVERT:
		doConvert(widgetDataStruct);
		break;

	case WIDGET_REVOLUTION:
		// handled in Python
		break;

	case WIDGET_AUTOMATE_CITIZENS:
		doAutomateCitizens();
		break;

	case WIDGET_AUTOMATE_PRODUCTION:
		doAutomateProduction();
		break;

	case WIDGET_EMPHASIZE:
		doEmphasize(widgetDataStruct);
		break;

	case WIDGET_DIPLOMACY_RESPONSE:
		// CLEANUP -- PD
		// GC.getDiplomacyScreen().handleClick(m_pWidget);
		break;

	case WIDGET_TRADE_ITEM:
		break;

	case WIDGET_UNIT_MODEL:
		doUnitModel();
		break;

	case WIDGET_FLAG:
		doFlag();
		break;

	case WIDGET_HELP_SELECTED:
		doSelected(widgetDataStruct);
		break;

	case WIDGET_PEDIA_JUMP_TO_UNIT:
		py.jumpToPedia(iData1, "Unit");
		break;

	case WIDGET_PEDIA_JUMP_TO_BUILDING:
		py.jumpToPedia(iData1, "Building");
		break;

	case WIDGET_PEDIA_JUMP_TO_TECH:
	case WIDGET_PEDIA_JUMP_TO_REQUIRED_TECH:
	case WIDGET_PEDIA_JUMP_TO_DERIVED_TECH:
		py.jumpToPedia(iData1, "Tech");
		break;

    // doc: culture level pedia
	case WIDGET_PEDIA_JUMP_TO_CULTURE_LEVEL:
		py.jumpToPedia(iData1, "CultureLevel");
		break;

	case WIDGET_PEDIA_BACK:
		py.callScreenFunction("pediaBack");
		break;
	case WIDGET_PEDIA_FORWARD:
		py.callScreenFunction("pediaForward");
		break;

	case WIDGET_PEDIA_JUMP_TO_BONUS:
		py.jumpToPedia(iData1, "Bonus");
		break;

	case WIDGET_PEDIA_MAIN:
		py.jumpToPediaMain(iData1);
		break;

	case WIDGET_PEDIA_JUMP_TO_PROMOTION:
		py.jumpToPedia(iData1, "Promotion");
		break;

	case WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT:
		py.jumpToPedia(iData1, "UnitChart");
		break;

	case WIDGET_PEDIA_JUMP_TO_IMPROVEMENT:
		py.jumpToPedia(iData1, "Improvement");
		break;

	// doc: route pedia
	case WIDGET_PEDIA_JUMP_TO_ROUTE:
		py.jumpToPedia(iData1, "Route");
		break;

	case WIDGET_PEDIA_JUMP_TO_CIVIC:
		py.jumpToPedia(iData1, "Civic");
		break;

	case WIDGET_PEDIA_JUMP_TO_CIV:
		py.jumpToPedia(iData1, "Civ");
		break;

	case WIDGET_PEDIA_JUMP_TO_LEADER:
		py.jumpToPedia(iData1, "Leader");
		break;

	case WIDGET_PEDIA_JUMP_TO_SPECIALIST:
		py.jumpToPedia(iData1, "Specialist");
		break;

	case WIDGET_PEDIA_JUMP_TO_PROJECT:
		py.jumpToPedia(iData1, "Project");
		break;

	case WIDGET_PEDIA_JUMP_TO_RELIGION:
		py.jumpToPedia(iData1, "Religion");
		break;

	case WIDGET_PEDIA_JUMP_TO_CORPORATION:
		py.jumpToPedia(iData1, "Corporation");
		break;

	case WIDGET_PEDIA_JUMP_TO_TERRAIN:
		py.jumpToPedia(iData1, "Terrain");
		break;

	case WIDGET_PEDIA_JUMP_TO_FEATURE:
		py.jumpToPedia(iData1, "Feature");
		break;

	// doc: pagan religion pedia
	case WIDGET_PEDIA_JUMP_TO_PAGAN_RELIGION:
		py.jumpToPedia(iData1, "PaganReligion");
		break;

	case WIDGET_PEDIA_DESCRIPTION:
	case WIDGET_PEDIA_DESCRIPTION_NO_HELP:
		py.jumpToPediaDescription(iData1, iData2);
		break;

	case WIDGET_TURN_EVENT:
		doGotoTurnEvent(widgetDataStruct);
		break;

	case WIDGET_FOREIGN_ADVISOR:
		py.showForeignAdvisorScreen(iData1);
		break;

    // doc: finance advisor
	case WIDGET_FINANCE_ADVISOR:
		py.showFinanceAdvisorScreen();
		break;

	case WIDGET_DEAL_KILL:
		/*	advc (note, known issue in multiplayer): The EXE seems to call this
			on all players involved in the deal, weirdly. (Perhaps to ensure that
			cancellation happens on all machines.) So the popups appear for both.
			Don't think this can be worked around - we don't know who clicked. */
		doDealKill(widgetDataStruct);
		break;

	case WIDGET_MINIMAP_HIGHLIGHT:
		py.refreshMilitaryAdvisor(iData1, iData2);
		break;

	// <advc.706>
	case WIDGET_RF_CIV_CHOICE:
		GC.getGame().getRiseFall().handleCivSelection((PlayerTypes)iData1);
		break;
	// </advc.706>  <advc.ctr>
	case WIDGET_CITY_TRADE:
	{
		CvCity* pCity = NULL;
		PlayerTypes eDummy;
		parseCityTradeHelp(widgetDataStruct, pCity, eDummy);
		// Can't move the camera while Foreign Advisor is up
		//gDLL->UI().lookAt(pCity->getPlot().getPoint(), CAMERALOOKAT_NORMAL);
		// Better than nothing: open city screen (while Foreign Advisor remains open too)
		if (pCity != NULL)
		{	// Close city screen with another click on WIDGET_CITY_TRADE
			if (gDLL->UI().isCitySelected(pCity))
				gDLL->UI().clearSelectedCities();
			else if (pCity->canBeSelected()) // (Tbd.: Could we otherwise at least highlight it on the minimap?)
				gDLL->UI().selectCity(pCity);
		}
		break;
	} // </advc.ctr>
	// <advc.154>
	case WIDGET_CYCLE_UNIT:
	{
		GC.getGame().doControl(iData2 == -1 ? CONTROL_UNSELECT_ALL :
				(iData1 == 1 ? CONTROL_CYCLEWORKER : CONTROL_CYCLEUNIT_ALT));
		break;
	} // </advc.154>
	}

	return bHandled;
}

//	right clicking action
bool CvDLLWidgetData::executeAltAction(CvWidgetDataStruct &widgetDataStruct)
{
	// <advc.003y>
	CvPythonCaller const& py = *GC.getPythonCaller();
	int iData1 = widgetDataStruct.m_iData1;
	int iData2 = widgetDataStruct.m_iData2; // </advc.003y>
	CvCivilization const& kActiveCiv = *GC.getGame().getActiveCivilization();
	bool bHandled = true;
	switch (widgetDataStruct.m_eWidgetType)
	{
	// <advc.004n>
	case WIDGET_PLOT_LIST_SHIFT:
		doPlotListShift(iData1, true);
		break; // </advc.004n>
	case WIDGET_HELP_TECH_ENTRY:
	case WIDGET_HELP_TECH_PREPREQ:
	case WIDGET_RESEARCH:
	case WIDGET_TECH_TREE:
		py.jumpToPedia(iData1, "Tech");
		break;
	// K-Mod
	case WIDGET_CHANGE_PERCENT:
		doChangePercentAlt(widgetDataStruct);
		break;
	// K-Mod end
	case WIDGET_TRAIN:
		py.jumpToPedia(kActiveCiv.getUnit((UnitClassTypes)iData1), "Unit");
		break;
	case WIDGET_CONSTRUCT:
		py.jumpToPedia(kActiveCiv.getBuilding((BuildingClassTypes)iData1), "Building");
		break;
	case WIDGET_CREATE:
		py.jumpToPedia(iData1, "Project");
		break;
	case WIDGET_PEDIA_JUMP_TO_UNIT:
	case WIDGET_HELP_FREE_UNIT:
		py.jumpToPedia(iData1, "Unit");
		break;
	case WIDGET_HELP_FOUND_RELIGION:
		py.jumpToPedia(iData2, "Religion");
		break;
	case WIDGET_PEDIA_JUMP_TO_RELIGION:
		py.jumpToPedia(iData1, "Religion");
		break;
	case WIDGET_HELP_FOUND_CORPORATION:
		py.jumpToPedia(iData2, "Corporation");
		break;
	case WIDGET_PEDIA_JUMP_TO_CORPORATION:
		py.jumpToPedia(iData1, "Corporation");
		break;
	case WIDGET_PEDIA_JUMP_TO_BUILDING:
		py.jumpToPedia(iData1, "Building");
		break;
	case WIDGET_PEDIA_JUMP_TO_PROMOTION:
		py.jumpToPedia(iData1, "Promotion");
		break;
	case WIDGET_HELP_OBSOLETE:
		py.jumpToPedia(iData1, "Building");
		break;
	case WIDGET_HELP_IMPROVEMENT:
	{	// advc.003y: Moved out of the deleted doPediaBuildJump
		ImprovementTypes eImprovement = NO_IMPROVEMENT;
		BuildTypes eBuild = (BuildTypes)widgetDataStruct.m_iData2;
		if (eBuild != NO_BUILD)
			eImprovement = GC.getInfo(eBuild).getImprovement();
		if (eImprovement != NO_IMPROVEMENT)
			py.jumpToPedia(eImprovement, "Improvement");
		break;
	}
	case WIDGET_HELP_YIELD_CHANGE:
		py.jumpToPedia(widgetDataStruct.m_iData2, "Improvement");
		break;
	case WIDGET_HELP_BONUS_REVEAL:
	case WIDGET_HELP_OBSOLETE_BONUS:
		py.jumpToPedia(widgetDataStruct.m_iData2, "Bonus");
		break;
	case WIDGET_CITIZEN:
	case WIDGET_FREE_CITIZEN:
	case WIDGET_DISABLED_CITIZEN:
		py.jumpToPedia(iData1, "Specialist");
		break;
	case WIDGET_PEDIA_JUMP_TO_PROJECT:
		py.jumpToPedia(iData1, "Project");
		break;
	case WIDGET_HELP_CIVIC_REVEAL:
		py.jumpToPedia(iData2, "Civic");
		break;
	case WIDGET_LH_GLANCE: // advc.152
	case WIDGET_LEADERHEAD:
		#ifdef ENABLE_REPRO_TEST
			ReproTest::startTest(widgetDataStruct.m_iData1);
		#else
			doContactCiv(widgetDataStruct);
		#endif
		break;  // <advc.ctr>
	case WIDGET_CITY_TRADE:
		// Both left and right click close the city screen
		if (gDLL->UI().isCityScreenUp())
			return executeAction(widgetDataStruct);
		break; // </advc.ctr>
	// <advc.154>
	case WIDGET_CYCLE_UNIT:
	{
		if (iData2 == -1)
		{
			GC.getGame().doControl(CONTROL_UNSELECT_ALL);
			break;
		}
		// Focus on the unit?
		/*CvPlayer const& kActivePlayer = GET_PLAYER(getActivePlayer());
		CvUnit const* pUnit = kActivePlayer.getUnit(iData2);
		if (pUnit != NULL)
			gDLL->getEngineIFace()->cameraLookAt(pUnit->getPlot().getPoint());*/
		// Maybe better: cycle backwards
		if (iData1 == 0) // (but not on the worker button)
			GC.getGame().doControl(CONTROL_LASTUNIT);
		break;
	} // </advc.154>
	default:
		bHandled = false;
		break;
	}

	return (bHandled);
}

bool CvDLLWidgetData::isLink(const CvWidgetDataStruct &widgetDataStruct) const
{
	bool bLink = false;
	switch (widgetDataStruct.m_eWidgetType)
	{
	case WIDGET_PEDIA_JUMP_TO_TECH:
	case WIDGET_PEDIA_JUMP_TO_REQUIRED_TECH:
	case WIDGET_PEDIA_JUMP_TO_DERIVED_TECH:
	case WIDGET_PEDIA_JUMP_TO_CULTURE_LEVEL: // doc
	case WIDGET_PEDIA_JUMP_TO_BUILDING:
	case WIDGET_PEDIA_JUMP_TO_UNIT:
	case WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT:
	case WIDGET_PEDIA_JUMP_TO_PROMOTION:
	case WIDGET_PEDIA_JUMP_TO_BONUS:
	case WIDGET_PEDIA_JUMP_TO_IMPROVEMENT:
	case WIDGET_PEDIA_JUMP_TO_ROUTE: // doc
	case WIDGET_PEDIA_JUMP_TO_CIVIC:
	case WIDGET_PEDIA_JUMP_TO_CIV:
	case WIDGET_PEDIA_JUMP_TO_LEADER:
	case WIDGET_PEDIA_JUMP_TO_SPECIALIST:
	case WIDGET_PEDIA_JUMP_TO_PROJECT:
	case WIDGET_PEDIA_JUMP_TO_RELIGION:
	case WIDGET_PEDIA_JUMP_TO_CORPORATION:
	case WIDGET_PEDIA_JUMP_TO_TERRAIN:
	case WIDGET_PEDIA_JUMP_TO_FEATURE:
	case WIDGET_PEDIA_JUMP_TO_PAGAN_RELIGION: // doc
	case WIDGET_PEDIA_FORWARD:
	case WIDGET_PEDIA_BACK:
	case WIDGET_PEDIA_MAIN:
	case WIDGET_TURN_EVENT:
	case WIDGET_FOREIGN_ADVISOR:
	case WIDGET_FINANCE_ADVISOR: // doc
	case WIDGET_PEDIA_DESCRIPTION:
	case WIDGET_PEDIA_DESCRIPTION_NO_HELP:
	case WIDGET_MINIMAP_HIGHLIGHT:
		bLink = (widgetDataStruct.m_iData1 >= 0);
		break;
	case WIDGET_DEAL_KILL:
		{
			CvDeal* pDeal = GC.getGame().getDeal(widgetDataStruct.m_iData1);
			bLink = (NULL != pDeal && pDeal->isCancelable(getActivePlayer()));
		}
		break;
	case WIDGET_CONVERT:
		bLink = (0 != widgetDataStruct.m_iData2);
		break;
	case WIDGET_GENERAL:
	case WIDGET_REVOLUTION:
		bLink = (1 == widgetDataStruct.m_iData1);
		break;
	}
	return (bLink);
}


void CvDLLWidgetData::doPlotList(CvWidgetDataStruct &widgetDataStruct)
{
	PROFILE_FUNC();

	int iUnitIndex = widgetDataStruct.m_iData1 + gDLL->UI().getPlotListColumn()
			- gDLL->UI().getPlotListOffset();
	CvUnit* pUnit = gDLL->UI().getInterfacePlotUnit(
			gDLL->UI().getSelectionPlot(), iUnitIndex);
	if (pUnit != NULL && pUnit->isActiveOwned())
	{
		bool bWasCityScreenUp = gDLL->UI().isCityScreenUp();
		gDLL->UI().selectGroup(pUnit,
				//gDLL->shiftKey(), gDLL->ctrlKey(), gDLL->altKey());
				GC.shiftKey(), GC.ctrlKey() || GC.altKey(), GC.altKey()); // K-Mod
		if (bWasCityScreenUp)
			gDLL->UI().lookAtSelectionPlot();
	}
}

// advc: This has gotten verbose, moving it out of executeAction.
void CvDLLWidgetData::doPlotListShift(int iChange, bool bMaxStep)
{
	//int iIncr = (GC.ctrlKey() ? GC.getDefineINT("MAX_PLOT_LIST_SIZE") - 1 : 1); // BtS
	// <advc.004n>
	if (GC.getMAX_PLOT_LIST_ROWS() <= 1)
		return;
	CvPlot const* pPlot = gDLL->UI().getSelectionPlot();
	if (pPlot == NULL)
		return;
	int const iPlotUnits = pPlot->getNumUnits();
	int iStep = 10;
	if (gDLL->UI().isCityScreenUp())
	{
		// (Not sure that this is really a maximal limit of anything)
		int const iBigStep = GC.getDefineINT("MAX_PLOT_LIST_SIZE"); // 100
		/*	BUG drawing method will only ever show a single row on the city screen.
			Don't want to expand rapidly upon the first right-shift then.
			Instead, let the bMaxStep param jump to the final column. */
		bool bBUGMethod = BUGOption::isEnabled("PLE__BUG_Style", false);
		static int iUnitsPerRow = 0;
		if (GC.getGame().getPlotListShift() == 0 && iChange == 1)
		{
			/*	Unhelpfully, the offset counts backward from the maximal
				number of units that CvMainInterface can display at once.
				Since we know that the city screen shows 1 row initially,
				we can figure out how many units are actually shown.*/
			iUnitsPerRow = gDLL->UI().getPlotListOffset() /
					(GC.getMAX_PLOT_LIST_ROWS() - 1);
			/*	Show a total of MAX_PLOT_LIST_SIZE. (Then move in steps of 10,
				same as on the main screen, which shows multiple rows already
				at shift 0.) */
			if (!bBUGMethod)
			{
				iStep = std::max(iStep, std::min(
						iPlotUnits, iBigStep - iUnitsPerRow));
			}
			else if (bMaxStep)
				iStep = iPlotUnits - iUnitsPerRow;
		}
		else if (GC.getGame().getPlotListShift() == 1 && iChange == -1 &&
			!bBUGMethod)
		{
			FAssert(iUnitsPerRow > 0);
			iStep = std::min(iBigStep, iPlotUnits) - iUnitsPerRow;
		}
		else if (bBUGMethod && bMaxStep)
			iStep = iPlotUnits - iUnitsPerRow;
	}
	GC.getGame().changePlotListShift(iChange);
	gDLL->UI().changePlotListColumn(iChange * iStep); // </advc.004n>
}


void CvDLLWidgetData::doLiberateCity()
{
	GC.getGame().selectedCitiesGameNetMessage(GAMEMESSAGE_DO_TASK, TASK_LIBERATE, 0);
	gDLL->UI().clearSelectedCities();
}


void CvDLLWidgetData::doRenameCity()
{
	CvCity* pHeadSelectedCity = gDLL->UI().getHeadSelectedCity();
	if (pHeadSelectedCity != NULL && pHeadSelectedCity->isActiveOwned())
		CvEventReporter::getInstance().cityRename(pHeadSelectedCity);
}


void CvDLLWidgetData::doRenameUnit()
{
	CvUnit* pHeadSelectedUnit = gDLL->UI().getHeadSelectedUnit();
	if (pHeadSelectedUnit != NULL && pHeadSelectedUnit->isActiveOwned())
		CvEventReporter::getInstance().unitRename(pHeadSelectedUnit);
}


void CvDLLWidgetData::doCreateGroup()
{
	GC.getGame().selectionListGameNetMessage(GAMEMESSAGE_JOIN_GROUP);
}


void CvDLLWidgetData::doDeleteGroup()
{
	GC.getGame().selectionListGameNetMessage(GAMEMESSAGE_JOIN_GROUP, -1, -1, -1, 0, false, true);
}


void CvDLLWidgetData::doTrain(CvWidgetDataStruct &widgetDataStruct)
{	// <advc.003w>
	UnitClassTypes eUnitClass = (UnitClassTypes)widgetDataStruct.m_iData1;
	UnitTypes eUnit = GC.getGame().getActiveCivilization()->getUnit(eUnitClass);
	// </advc.003w>
	if (widgetDataStruct.m_iData2 != FFreeList::INVALID_INDEX)
	{
		CvMessageControl::getInstance().sendPushOrder(widgetDataStruct.m_iData2, ORDER_TRAIN,
				eUnit, false, //false, false);
				true, 0); // K-Mod
	}
	else
	{
		GC.getGame().selectedCitiesGameNetMessage(GAMEMESSAGE_PUSH_ORDER, ORDER_TRAIN,
				eUnit, -1, false, GC.altKey(), GC.shiftKey(), GC.ctrlKey());
	}

	gDLL->UI().setCityTabSelectionRow(CITYTAB_UNITS);
}


void CvDLLWidgetData::doConstruct(CvWidgetDataStruct &widgetDataStruct)
{	// <advc.003w>
	BuildingClassTypes eBuildingClass = (BuildingClassTypes)widgetDataStruct.m_iData1;
	BuildingTypes eBuilding = GC.getGame().getActiveCivilization()->getBuilding(eBuildingClass);
	// </advc.003w>
	if (widgetDataStruct.m_iData2 != FFreeList::INVALID_INDEX)
	{
		CvMessageControl::getInstance().sendPushOrder(widgetDataStruct.m_iData2, ORDER_CONSTRUCT,
				eBuilding, false, //false, false);
				true, 0); // K-Mod
	}
	else
	{
		GC.getGame().selectedCitiesGameNetMessage(GAMEMESSAGE_PUSH_ORDER, ORDER_CONSTRUCT,
				eBuilding, -1, false, GC.altKey(), GC.shiftKey(), GC.ctrlKey());
	}
	if (GC.getInfo(eBuildingClass).isLimited())
		gDLL->UI().setCityTabSelectionRow(CITYTAB_WONDERS);
	else gDLL->UI().setCityTabSelectionRow(CITYTAB_BUILDINGS);
}


void CvDLLWidgetData::doCreate(CvWidgetDataStruct &widgetDataStruct)
{
	if (widgetDataStruct.m_iData2 != FFreeList::INVALID_INDEX)
	{
		CvMessageControl::getInstance().sendPushOrder(widgetDataStruct.m_iData2, ORDER_CREATE,
				widgetDataStruct.m_iData1, false, //false, false);
				true, 0); // K-Mod
	}
	else
	{
		GC.getGame().selectedCitiesGameNetMessage(GAMEMESSAGE_PUSH_ORDER, ORDER_CREATE,
				widgetDataStruct.m_iData1, -1, false, GC.altKey(), GC.shiftKey(), GC.ctrlKey());
	}
	gDLL->UI().setCityTabSelectionRow(CITYTAB_WONDERS);
}


void CvDLLWidgetData::doMaintain(CvWidgetDataStruct &widgetDataStruct)
{
	if (widgetDataStruct.m_iData2 != FFreeList::INVALID_INDEX)
	{
		//CvMessageControl::getInstance().sendPushOrder(widgetDataStruct.m_iData2, ORDER_MAINTAIN, widgetDataStruct.m_iData1, false, false, false);
		CvMessageControl::getInstance().sendPushOrder(widgetDataStruct.m_iData2, ORDER_MAINTAIN,
				widgetDataStruct.m_iData1, false, //false, false);
				true, 0); // K-Mod
	}
	else
	{
		GC.getGame().selectedCitiesGameNetMessage(GAMEMESSAGE_PUSH_ORDER, ORDER_MAINTAIN,
				widgetDataStruct.m_iData1, -1, false, GC.altKey(), GC.shiftKey(), GC.ctrlKey());
	}
	gDLL->UI().setCityTabSelectionRow(CITYTAB_WONDERS);
}


void CvDLLWidgetData::doHurry(CvWidgetDataStruct &widgetDataStruct)
{
	GC.getGame().selectedCitiesGameNetMessage(GAMEMESSAGE_DO_TASK, TASK_HURRY, widgetDataStruct.m_iData1);
}


void CvDLLWidgetData::doConscript()
{
	GC.getGame().selectedCitiesGameNetMessage(GAMEMESSAGE_DO_TASK, TASK_CONSCRIPT);
}


void CvDLLWidgetData::doAction(CvWidgetDataStruct &widgetDataStruct)
{
	GC.getGame().handleAction(widgetDataStruct.m_iData1);
}


void CvDLLWidgetData::doChangeSpecialist(CvWidgetDataStruct &widgetDataStruct)
{
	GC.getGame().selectedCitiesGameNetMessage(GAMEMESSAGE_DO_TASK, TASK_CHANGE_SPECIALIST, widgetDataStruct.m_iData1, widgetDataStruct.m_iData2);
}

void CvDLLWidgetData::doResearch(CvWidgetDataStruct &widgetDataStruct)
{
	/*bool bShift = GC.shiftKey();
	if(!bShift) {
		if ((GetKeyState(VK_LSHIFT) & 0x8000) || (GetKeyState(VK_RSHIFT) & 0x8000))
			bShift = true;
	}*/ // BtS
	bool bShift = GC.shiftKey();

	// UNOFFICIAL_PATCH, Bugfix (Free Tech Popup Fix), 12/07/09, EmperorFool: START
	CvPlayer& kActivePlayer = GET_PLAYER(getActivePlayer());
	if (widgetDataStruct.m_iData2 > 0)
	{
		if (!kActivePlayer.isChoosingFreeTech())
		{
			gDLL->UI().addMessage(getActivePlayer(), true, -1,
					gDLL->getText("TXT_KEY_CHEATERS_NEVER_PROSPER"), NULL, MESSAGE_TYPE_MAJOR_EVENT);
			FErrorMsg("doResearch called for free tech when !isChoosingFreeTech()");
			return;
		}
		else kActivePlayer.changeChoosingFreeTechCount(-1);
	} // UNOFFICIAL_PATCH: END
	TechTypes eNewActiveResearch = (TechTypes)widgetDataStruct.m_iData1;
	/*	<advc.001> The main interface now passes the tech ID when the name of
		the current research is clicked (for the right-click Pedia jump). But
		we still want to clear the current research on left-click, so we mustn't
		pass the tech ID along here. */
	if (widgetDataStruct.m_eWidgetType == WIDGET_RESEARCH &&
		eNewActiveResearch == kActivePlayer.getCurrentResearch())
	{
		eNewActiveResearch = NO_TECH;
	} // </advc.001>
	CvMessageControl::getInstance().sendResearch(eNewActiveResearch,
			widgetDataStruct.m_iData2, bShift);
}


void CvDLLWidgetData::doChangePercent(CvWidgetDataStruct &widgetDataStruct)
{
	CvMessageControl::getInstance().sendPercentChange(((CommerceTypes)widgetDataStruct.m_iData1), widgetDataStruct.m_iData2);
}

// K-Mod. Right click on "change percent" buttons will set them to min / max.
void CvDLLWidgetData::doChangePercentAlt(CvWidgetDataStruct &widgetDataStruct)
{
	CvMessageControl::getInstance().sendPercentChange((CommerceTypes)widgetDataStruct.m_iData1, widgetDataStruct.m_iData2 * 100);
	// <advc.120c>
	gDLL->UI().setDirty(Espionage_Advisor_DIRTY_BIT, true);
	gDLL->UI().setDirty(PercentButtons_DIRTY_BIT, true);
	// </advc.120c>
}
// K-Mod end

void CvDLLWidgetData::doCityTab(CvWidgetDataStruct &widgetDataStruct)
{
	gDLL->UI().setCityTabSelectionRow((CityTabTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::doContactCiv(CvWidgetDataStruct &widgetDataStruct)
{
	if (gDLL->isDiplomacy() || gDLL->isMPDiplomacyScreenUp())
		return;

	//	Do not execute this if we are trying to contact ourselves...
	if (getActivePlayer() == widgetDataStruct.m_iData1)
	{
		if (!gDLL->UI().isFocusedWidget() &&
			// advc.085: Never minimize the scoreboard
			gDLL->UI().isScoresMinimized())
		{
			gDLL->UI().toggleScoresMinimized();
		}
		return;
	}  /* <advc.085> Give the player time to move the cursor off the scoreboard
		  (cf. comments in CvPlayer::setScoreboardExpanded) */
	if (BUGOption::isEnabled("Scores__ExpandOnHover", false, false))
		GC.getGame().setUpdateTimer(CvGame::UPDATE_DIRTY_SCORE_HELP, 4); // </advc.085>
	// BETTER_BTS_AI_MOD, Player Interface, 01/11/09, jdog5000: START
	if (GC.shiftKey() && !GC.altKey())
	{
		if (GET_PLAYER((PlayerTypes)widgetDataStruct.m_iData1).isHuman() &&
			widgetDataStruct.m_iData1 != getActivePlayer())
		{
			gDLL->UI().showTurnLog((ChatTargetTypes)widgetDataStruct.m_iData1);
		}
		return;
	}

	if (GC.altKey())
	{
		TeamTypes eWidgetTeam = GET_PLAYER((PlayerTypes)widgetDataStruct.m_iData1).getTeam(); // K-Mod
		if (GC.shiftKey())
		{
			// Warning: use of this is not multiplayer compatible
			// K-Mod, since this it isn't MP compatible, I'm going to disable it for the time being.
			/*{
				if (GET_TEAM(getActiveTeam()).canDeclareWar(eWidgetTeam))
				{
					if (GET_TEAM(getActiveTeam()).AI_getWarPlan(eWidgetTeam) == WARPLAN_PREPARING_TOTAL)
					{
						GET_TEAM(getActiveTeam()).AI_setWarPlan(eWidgetTeam, NO_WARPLAN);
					}
					else
					{
						GET_TEAM(getActiveTeam()).AI_setWarPlan(eWidgetTeam, WARPLAN_PREPARING_TOTAL);
					}
					gDLL->UI().setDirty(Score_DIRTY_BIT, true);
				}
			}*/ // K-Mod end
		}
		else
		{
			if (GET_TEAM(getActiveTeam()).canDeclareWar(eWidgetTeam))
			{
				//CvMessageControl::getInstance().sendChangeWar(GET_PLAYER((PlayerTypes)widgetDataStruct.m_iData1).getTeam(), true);
				// K-Mod. Give us a confirmation popup...
				CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_DECLAREWARMOVE);
				if (NULL != pInfo)
				{
					pInfo->setData1(eWidgetTeam);
					pInfo->setOption1(false); // shift key
					pInfo->setFlags(1); // don't do the "move" part of the declare-war-move.
					gDLL->UI().addPopup(pInfo);
				}
				// K-Mod end
			}
			else if (GET_TEAM(eWidgetTeam).isVassal(getActiveTeam()))
			{
				CvPopupInfo* pInfo = new CvPopupInfo(
						BUTTONPOPUP_VASSAL_DEMAND_TRIBUTE, widgetDataStruct.m_iData1);
				if (pInfo)
				{
					gDLL->UI().addPopup(pInfo, getActivePlayer(), true);
				}
			}
		}
		return;
	}
	// BETTER_BTS_AI_MOD: END
	GET_PLAYER(getActivePlayer()).contact((PlayerTypes)
			widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::doConvert(CvWidgetDataStruct &widgetDataStruct)
{
	if (widgetDataStruct.m_iData2 != 0)
	{
		CvMessageControl::getInstance().sendConvert((ReligionTypes)(widgetDataStruct.m_iData1));
	}
}

void CvDLLWidgetData::doAutomateCitizens()
{
	CvCity* pHeadSelectedCity;

	pHeadSelectedCity = gDLL->UI().getHeadSelectedCity();

	if (pHeadSelectedCity != NULL)
	{
		GC.getGame().selectedCitiesGameNetMessage(GAMEMESSAGE_DO_TASK, TASK_SET_AUTOMATED_CITIZENS, -1, -1, !(pHeadSelectedCity->isCitizensAutomated()));
	}
}

void CvDLLWidgetData::doAutomateProduction()
{
	CvCity* pHeadSelectedCity;

	pHeadSelectedCity = gDLL->UI().getHeadSelectedCity();

	if (pHeadSelectedCity != NULL)
	{
		GC.getGame().selectedCitiesGameNetMessage(GAMEMESSAGE_DO_TASK, TASK_SET_AUTOMATED_PRODUCTION, -1, -1, !pHeadSelectedCity->isProductionAutomated(), GC.altKey(), GC.shiftKey(), GC.ctrlKey());
	}
}

void CvDLLWidgetData::doEmphasize(CvWidgetDataStruct &widgetDataStruct)
{
	CvCity* pHeadSelectedCity = gDLL->UI().getHeadSelectedCity();
	if (pHeadSelectedCity != NULL)
	{
		GC.getGame().selectedCitiesGameNetMessage(GAMEMESSAGE_DO_TASK,
				TASK_SET_EMPHASIZE, widgetDataStruct.m_iData1, -1,
				!pHeadSelectedCity->AI().AI_isEmphasize((EmphasizeTypes)
				widgetDataStruct.m_iData1));
	}
}

void CvDLLWidgetData::doUnitModel()
{
	if (gDLL->UI().isFocused())
	{
		//	Do NOT execute if a screen is up...
		return;
	}

	gDLL->UI().lookAtSelectionPlot();
}


void CvDLLWidgetData::doFlag()
{
	GC.getGame().doControl(CONTROL_SELECTCAPITAL);
}

void CvDLLWidgetData::doSelected(CvWidgetDataStruct &widgetDataStruct)
{
	CvCity* pHeadSelectedCity;

	pHeadSelectedCity = gDLL->UI().getHeadSelectedCity();

	if (pHeadSelectedCity != NULL)
	{
		//GC.getGame().selectedCitiesGameNetMessage(GAMEMESSAGE_POP_ORDER, widgetDataStruct.m_iData1);
		GC.getGame().selectedCitiesGameNetMessage(GAMEMESSAGE_POP_ORDER, widgetDataStruct.m_iData1, -1, -1, false, GC.altKey(), GC.shiftKey(), GC.ctrlKey());
	}
}

void CvDLLWidgetData::doGotoTurnEvent(CvWidgetDataStruct &widgetDataStruct)
{
	CvPlot* pPlot = GC.getMap().plot(widgetDataStruct.m_iData1, widgetDataStruct.m_iData2);
	if (pPlot != NULL && !gDLL->getEngineIFace()->isCameraLocked())
	{
		if (pPlot->isRevealed(getActiveTeam()))
			gDLL->getEngineIFace()->cameraLookAt(pPlot->getPoint());
	}
}

void CvDLLWidgetData::doMenu()
{
	if (!gDLL->isGameInitializing())
	{
		CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_MAIN_MENU);
		if (pInfo != NULL)
			gDLL->UI().addPopup(pInfo, NO_PLAYER, true);
	}
}

void CvDLLWidgetData::doLaunch(CvWidgetDataStruct &widgetDataStruct)
{
	if (GET_TEAM(getActiveTeam()).canLaunch(
		(VictoryTypes)widgetDataStruct.m_iData1) &&
		GC.getGame().testVictory(
		(VictoryTypes)widgetDataStruct.m_iData1, getActiveTeam()))
	{
		CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_LAUNCH, widgetDataStruct.m_iData1);
		if (pInfo != NULL)
			gDLL->UI().addPopup(pInfo);
	}
}

//
//	HELP PARSING FUNCTIONS
//

void CvDLLWidgetData::parsePlotListHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	PROFILE_FUNC();

	int iUnitIndex = widgetDataStruct.m_iData1 + gDLL->UI().getPlotListColumn() -
			gDLL->UI().getPlotListOffset();

	CvPlot *selectionPlot = gDLL->UI().getSelectionPlot();
	CvUnit* pUnit = gDLL->UI().getInterfacePlotUnit(selectionPlot, iUnitIndex);
	if (pUnit == NULL)
		return;

	GAMETEXT.setUnitHelp(szBuffer, pUnit,
			// <advc.069>
			false, false, false, // defaults
			pUnit->isActiveOwned());
			// </advc.069>
	if (pUnit->getPlot().plotCount(PUF_isUnitType, pUnit->getUnitType(), -1, pUnit->getOwner()) > 1)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_CTRL_SELECT", GC.getInfo(pUnit->getUnitType()).getTextKeyWide()));
	}
	if (pUnit->getPlot().plotCount(NULL, -1, -1, pUnit->getOwner()) > 1)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_ALT_SELECT"));
	}
}


void CvDLLWidgetData::parseLiberateCityHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity = gDLL->UI().getHeadSelectedCity();
	if (pHeadSelectedCity != NULL)
	{
		PlayerTypes ePlayer = pHeadSelectedCity->getLiberationPlayer();
		if (NO_PLAYER != ePlayer)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_LIBERATE_CITY_HELP",
					pHeadSelectedCity->getNameKey(), GET_PLAYER(ePlayer).getNameKey()));
		}
	}
}


void CvDLLWidgetData::parseCityNameHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity = gDLL->UI().getHeadSelectedCity();
	if (pHeadSelectedCity != NULL)
	{
		szBuffer.append(pHeadSelectedCity->getName());

		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_CITY_POPULATION", pHeadSelectedCity->getRealPopulation()));
		CvWString szTempBuffer;
		GAMETEXT.setTimeStr(szTempBuffer, pHeadSelectedCity->getGameTurnFounded(), false);
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_CITY_FOUNDED", szTempBuffer.GetCString()));

		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_CHANGE_NAME"));
	}
}


void CvDLLWidgetData::parseTrainHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity;
	if (widgetDataStruct.m_iData2 != FFreeList::INVALID_INDEX)
		pHeadSelectedCity = GET_PLAYER(getActivePlayer()).getCity(widgetDataStruct.m_iData2);
	else pHeadSelectedCity = gDLL->UI().getHeadSelectedCity();

	if (pHeadSelectedCity != NULL)
	{
		CvCivilization const& kCiv = pHeadSelectedCity->getCivilization();
		GAMETEXT.setUnitHelp(szBuffer,
				kCiv.getUnit((UnitClassTypes)widgetDataStruct.m_iData1),
				false, widgetDataStruct.m_bOption, false, pHeadSelectedCity);
	}
}


void CvDLLWidgetData::parseConstructHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity;
	if (widgetDataStruct.m_iData2 != FFreeList::INVALID_INDEX)
		pHeadSelectedCity = GET_PLAYER(getActivePlayer()).getCity(widgetDataStruct.m_iData2);
	else pHeadSelectedCity = gDLL->UI().getHeadSelectedCity();

	if (pHeadSelectedCity != NULL)
	{
		CvCivilization const& kCiv = pHeadSelectedCity->getCivilization();
		//GAMETEXT.setBuildingHelp(...
		// BUG - Building Actual Effects:
		GAMETEXT.setBuildingHelpActual(szBuffer,
				kCiv.getBuilding((BuildingClassTypes)widgetDataStruct.m_iData1),
				false, widgetDataStruct.m_bOption, false, pHeadSelectedCity);
	}
}


void CvDLLWidgetData::parseCreateHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity;
	if (widgetDataStruct.m_iData2 != FFreeList::INVALID_INDEX)
		pHeadSelectedCity = GET_PLAYER(getActivePlayer()).getCity(widgetDataStruct.m_iData2);
	else pHeadSelectedCity = gDLL->UI().getHeadSelectedCity();

	GAMETEXT.setProjectHelp(szBuffer, ((ProjectTypes)widgetDataStruct.m_iData1), false, pHeadSelectedCity);
}


void CvDLLWidgetData::parseMaintainHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.setProcessHelp(szBuffer, (ProcessTypes)widgetDataStruct.m_iData1);
}


void CvDLLWidgetData::parseHurryHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)  // advc: style changes
{
	CvCity* pHeadSelectedCity = gDLL->UI().getHeadSelectedCity();
	if (pHeadSelectedCity == NULL)
		return;
	CvCity const& kCity = *pHeadSelectedCity;
	szBuffer.assign(gDLL->getText("TXT_KEY_MISC_HURRY_PROD", kCity.getProductionNameKey()));
	// <advc.064b>
	if (kCity.isDisorder())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_DISORDER_BLOCKS_HURRY"));
		return;
	} // </advc.064b>
	HurryTypes eHurry = (HurryTypes)widgetDataStruct.m_iData1;
	// advc.001: canHurry check in order to avoid (inconsequential) overflow
	int const iHurryGold = (kCity.canHurry(eHurry, true) ? kCity.hurryGold(eHurry) : 0);
	int const iHurryPopulation = kCity.hurryPopulation(eHurry);
	if (iHurryGold > 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_HURRY_GOLD", iHurryGold));
	}
	bool bReasonGiven = false; // advc.064b: Why we can't hurry
	{
		if (iHurryPopulation > 0 &&
			kCity.hurryCost(false) > 0) // advc.004: Don't show hurry pop if no production chosen
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HURRY_POP", iHurryPopulation));
			if (iHurryPopulation > kCity.maxHurryPopulation())
			{
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_MAX_POP_HURRY",
						kCity.maxHurryPopulation()));
				bReasonGiven = true; // advc.064b
			}
		}
	}
	// BUG - Hurry Overflow - start (advc.064)
	if (BUGOption::isEnabled("MiscHover__HurryOverflow", true))
	{
		int iOverflowProduction = 0;
		int iOverflowGold = 0;
		bool bIncludeCurrent = BUGOption::isEnabled("MiscHover__HurryOverflowIncludeCurrent", false);
		if (kCity.hurryOverflow(eHurry, &iOverflowProduction, &iOverflowGold, bIncludeCurrent))
		{
			if (iOverflowProduction != 0 || iOverflowGold > 0)
			{	// <advc.064b>
				FAssert(iOverflowProduction > 0 ||
						(iOverflowProduction == -GC.getInfo(YIELD_PRODUCTION).getMinCity() && !bIncludeCurrent));
				// </advc.064b>
				bool bFirst = true;
				CvWStringBuffer szOverflowBuffer;
				CvWString szTempBuffer;
				// advc: Plus signs added if !bIncludeCurrent
				if (iOverflowProduction != 0)
				{
					szTempBuffer.Format(L"%s%d%c",
							(bIncludeCurrent || iOverflowProduction <= 0 ? L"" : L"+"),
							iOverflowProduction, GC.getInfo(YIELD_PRODUCTION).getChar());
					setListHelp(szOverflowBuffer, NULL, szTempBuffer, L", ", bFirst);
				}
				if (iOverflowGold > 0)
				{
					szTempBuffer.Format(L"%s%d%c",
							(bIncludeCurrent ? L"" : L"+"),
							iOverflowGold, GC.getInfo(COMMERCE_GOLD).getChar());
					setListHelp(szOverflowBuffer, NULL, szTempBuffer, L", ", bFirst);
				}
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_HURRY_OVERFLOW",
						szOverflowBuffer.getCString()));
			}
		}
	} // BUG - Hurry Overflow - end
	{
		int iHurryAngerLength = kCity.hurryAngerLength(eHurry);

        // doc: anger scales with sacrificed population
        int iHurryAngerModifier = (1 + iHurryPopulation) / 2;
        int iHurryAnger = GC.getDefineINT(CvGlobals::HURRY_POP_ANGER) * iHurryAngerModifier;

        // doc: Blue Mosque effect
        if (kCity.isHasBuildingEffect(BLUE_MOSQUE))
            iHurryAnger = 1;

        if (iHurryAngerLength > 0)
		{
			szBuffer.append(NEWLINE);
            // doc
			int iTotalHurryAngerLength = iHurryAngerLength * iHurryAngerModifier + pHeadSelectedCity->getHurryAngerTimer();
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_ANGER_TURNS", iHurryAnger, iTotalHurryAngerLength));
		}
	}
	if (!pHeadSelectedCity->isProductionUnit() && !kCity.isProductionBuilding())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_UNIT_BUILDING_HURRY"));
		bReasonGiven = true; // advc.064b
	}
	if(!kCity.canHurry(eHurry, false)) // advc.064b
	{
		bool bFirst = true;
		if (!GET_PLAYER(kCity.getOwner()).canHurry(eHurry))
		{
			FOR_EACH_ENUM(Civic)
			{
				if (!GC.getInfo(eLoopCivic).isHurry(eHurry))
					continue;
				CvWString szTempBuffer(NEWLINE + gDLL->getText("TXT_KEY_REQUIRES"));
				setListHelp(szBuffer, szTempBuffer, GC.getInfo(eLoopCivic).getDescription(),
						gDLL->getText("TXT_KEY_OR").c_str(), bFirst);
			}
			if (!bFirst)
				szBuffer.append(ENDCOLR);
		} // <advc.064b> Explain changes in CvCity::canHurry
		if(!bFirst)
			bReasonGiven = true;
		if(!bReasonGiven && kCity.getProduction() < kCity.getProductionNeeded() &&
			kCity.getCurrentProductionDifference(true, true, false, true, true)
			+ kCity.getProduction() >= kCity.getProductionNeeded())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_OVERFLOW_BLOCKS_HURRY"
					/*,kCity.getProductionNameKey()*/)); // (gets too long)
			bReasonGiven = true;
		}
		if(!bReasonGiven && GC.getInfo(eHurry).getGoldPerProduction() > 0 &&
			iHurryGold <= 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_PRODUCTION_BLOCKS_HURRY"));
		} // </advc.064b>
	}
}


void CvDLLWidgetData::parseConscriptHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)  // advc: style changes
{
	CvCity* pHeadSelectedCity = gDLL->UI().getHeadSelectedCity();
	if (pHeadSelectedCity == NULL || pHeadSelectedCity->getConscriptUnit() == NO_UNIT)
		return;
	{
		CvWString szTemp;
		szTemp.Format(SETCOLR L"%s" ENDCOLR, TEXT_COLOR("COLOR_UNIT_TEXT"),
				GC.getInfo(pHeadSelectedCity->getConscriptUnit()).getDescription());
		szBuffer.assign(szTemp);
	}
	{
		int iConscriptPopulation = pHeadSelectedCity->getConscriptPopulation();
		if (iConscriptPopulation > 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HURRY_POP", iConscriptPopulation));
		}
	}
	{
		int iConscriptAngerLength = pHeadSelectedCity->flatConscriptAngerLength();
	    int iConscriptAnger = GC.getDefineINT("CONSCRIPT_POP_ANGER");

        // doc: Blue Mosque effect
        if (pHeadSelectedCity->isHasBuildingEffect(BLUE_MOSQUE))
            iConscriptAnger = 1;

        if (iConscriptAngerLength > 0)
        {
            // doc
            int iTotalAngerLength = iConscriptAngerLength + pHeadSelectedCity->getConscriptAngerTimer();
            szBuffer.append(NEWLINE);
            szBuffer.append(gDLL->getText("TXT_KEY_MISC_ANGER_TURNS", iConscriptAnger, iTotalAngerLength));
		}
	}
	{
		int iMinCityPopulation = pHeadSelectedCity->conscriptMinCityPopulation();
		if (pHeadSelectedCity->getPopulation() < iMinCityPopulation)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_MIN_CITY_POP", iMinCityPopulation));
		}
	}
	{
		int iMinCulturePercent = GC.getDefineINT("CONSCRIPT_MIN_CULTURE_PERCENT");
		if (pHeadSelectedCity->getPlot().calculateTeamCulturePercent(
			pHeadSelectedCity->getTeam()) < iMinCulturePercent)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_MIN_CULTURE_PERCENT",
					iMinCulturePercent));
		}
	}
	if (GET_PLAYER(pHeadSelectedCity->getOwner()).getMaxConscript() == 0)
	{
		bool bFirst = true;
		FOR_EACH_ENUM(Civic)
		{
			if (GC.getGame().getMaxConscript(eLoopCivic) > 0)
			{
				CvWString szTempBuffer(NEWLINE + gDLL->getText("TXT_KEY_REQUIRES"));
				setListHelp(szBuffer, szTempBuffer, GC.getInfo(eLoopCivic).getDescription(),
						gDLL->getText("TXT_KEY_OR").c_str(), bFirst);
			}
		}
		if (!bFirst)
			szBuffer.append(ENDCOLR);
	}
}


void CvDLLWidgetData::parseActionHelp(CvWidgetDataStruct &widgetDataStruct,
	CvWStringBuffer &szBuffer)
{
	CvWString szTemp;
	CvActionInfo const& kAction = GC.getActionInfo(widgetDataStruct.m_iData1);
	szTemp.Format(SETCOLR L"%s" ENDCOLR , TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
			kAction.getHotKeyDescription().c_str());
	szBuffer.assign(szTemp);
	CvDLLInterfaceIFaceBase& kUI = *gDLL->getInterfaceIFace();

	CvUnit const* pHeadSelectedUnit = kUI.getHeadSelectedUnit();
	if (pHeadSelectedUnit != NULL)
	{
		MissionTypes eMission = (MissionTypes)kAction.getMissionType();
		if (eMission != NO_MISSION)
		{	// advc: Moved into subroutine
			parseActionHelp_Mission(kAction, *pHeadSelectedUnit, eMission, szBuffer);
		}
		if (kAction.getCommandType() != NO_COMMAND)
		{
			bool bAlt = GC.altKey();
			CvWString szTempBuffer;
			if (kAction.getCommandType() == COMMAND_PROMOTION)
			{
				GAMETEXT.parsePromotionHelp(szBuffer,
						(PromotionTypes)kAction.getCommandData());
			}
			else if (kAction.getCommandType() == COMMAND_UPGRADE)
			{
				UnitTypes const eTo = (UnitTypes)kAction.getCommandData();
				GAMETEXT.setBasicUnitHelp(szBuffer, eTo);

				// <advc.080>
				int iLostXP = 0;
				bool bSingleUnit = true; // </advc.080>
				int iPrice = 0;
				if (bAlt && GC.getInfo((CommandTypes)kAction.getCommandType()).getAll())
				{
					CvPlayer const& kHeadOwner = GET_PLAYER(pHeadSelectedUnit->getOwner());
					UnitTypes eFrom = pHeadSelectedUnit->getUnitType();
					iPrice = kHeadOwner.upgradeAllPrice(eTo, eFrom);
					// <advc.080>
					iLostXP = -kHeadOwner.upgradeAllXPChange(eTo, eFrom);
					bSingleUnit = false; // </advc.080>
				}
				else
				{
					for (CLLNode<IDInfo> const* pNode = kUI.headSelectionListNode();
						pNode != NULL; pNode = kUI.nextSelectionListNode(pNode))
					{
						CvUnit const* pSelectedUnit = ::getUnit(pNode->m_data);
						if (pSelectedUnit->canUpgrade(eTo, true))
						{
							iPrice += pSelectedUnit->upgradePrice(eTo);
							// <advc.080>
							if (iLostXP != 0)
								bSingleUnit = false;
							iLostXP -= pSelectedUnit->upgradeXPChange(eTo);
						}
					}
				}
				if (iLostXP > 0)
				{
					szBuffer.append(NEWLINE);
					if (bSingleUnit)
						szBuffer.append(gDLL->getText("TXT_KEY_MISC_LOST_XP", iLostXP));
					else szBuffer.append(gDLL->getText("TXT_KEY_MISC_LOST_XP_TOTAL", iLostXP));
				} // </advc.080>
				szTempBuffer.Format(L"%s%d %c", NEWLINE, iPrice, GC.getInfo(COMMERCE_GOLD).getChar());
				szBuffer.append(szTempBuffer);
			}
			else if (kAction.getCommandType() == COMMAND_GIFT &&
				pHeadSelectedUnit->getPlot().isOwned())
			{
				CvPlot const& kGiftPlot = pHeadSelectedUnit->getPlot();
				PlayerTypes const eRecipient = kGiftPlot.getOwner();
				CvPlayerAI const& kRecipient = GET_PLAYER(eRecipient);
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_ACTION_GOES_TO_CIV"));
				szTempBuffer.Format(SETCOLR L"%s" ENDCOLR, PLAYER_TEXT_COLOR(kRecipient),
						kRecipient.getCivilizationShortDescription());
				szBuffer.append(szTempBuffer);
				for (CLLNode<IDInfo> const* pNode = kUI.headSelectionListNode();
					pNode != NULL; pNode = kUI.nextSelectionListNode(pNode))
				{
					CvUnit const& kSelectedUnit = *::getUnit(pNode->m_data);
					// <advc.093> Check this upfront, then look into the specific reason.
					if (kSelectedUnit.canGift())
						continue;
					szBuffer.append(NEWLINE); // </advc.093>
					// <advc.705>
					if (GC.getGame().isOption(GAMEOPTION_RISE_FALL) &&
						GC.getGame().getRiseFall().isCooperationRestricted(eRecipient))
					{
						szBuffer.append(gDLL->getText("TXT_KEY_REFUSE_GIFT_RF",
								kRecipient.getNameKey()));
						break;
					} // </advc.705>
					// <advc.093>
					if (kGiftPlot.isVisibleEnemyUnit(eRecipient) ||
						kGiftPlot.isVisibleEnemyUnit(pHeadSelectedUnit->getOwner()))
					{
						szBuffer.append(gDLL->getText("TXT_KEY_GIFT_NO_ENEMY"));
						break;
					} // </advc.093>
					// <advc.123a>
					if (kSelectedUnit.AI_getUnitAIType() == UNITAI_MISSIONARY &&
						kRecipient.isNoNonStateReligionSpread())
					{
						ReligionTypes eRecipientReligion = kRecipient.
								getStateReligion();
						FOR_EACH_ENUM(Religion)
						{
							if (kSelectedUnit.getUnitInfo().
								getReligionSpreads(eLoopReligion) <= 0)
							{
								continue;
							}
							if (eRecipientReligion != NO_RELIGION &&
								eLoopReligion != NO_RELIGION &&
								eRecipientReligion != eLoopReligion)
							{
								szBuffer.append(gDLL->getText("TXT_KEY_GIFT_NO_MISSIONARY",
										GC.getInfo(eRecipientReligion).getChar(),
										kRecipient.getNameKey()));
								break;
							}
						}
					} // </advc.123a>
					// <advc.093>
					{
						bool bAnyCorpSpread = false;
						FOR_EACH_ENUM(Corporation)
						{
							if (kSelectedUnit.getUnitInfo().getCorporationSpreads(
								eLoopCorporation) > 0)
							{
								bAnyCorpSpread = true;
								break;
							}
						}
						if (bAnyCorpSpread)
						{
							szBuffer.append(gDLL->getText("TXT_KEY_GIFT_NO_EXECUTIVE"));
							break;
						}
					} // </advc.093>
					// (The only case that BtS had explained to the player)
					if (!kRecipient.AI_acceptUnit(kSelectedUnit))
					{
						szBuffer.append(gDLL->getText("TXT_KEY_REFUSE_GIFT",
								kRecipient.getNameKey()));
						break;
					}
					// <advc.093> Catch-all answer (future-proofing)
					szBuffer.append(gDLL->getText("TXT_KEY_MUST_REFUSE_GIFT",
							kRecipient.getNameKey()));
					break; // </advc.093>
				}
			}
			CommandTypes const eCommand = (CommandTypes)kAction.getCommandType();
			CvCommandInfo const& kCommand = GC.getInfo(eCommand);
			if (kCommand.getAll())
				szBuffer.append(gDLL->getText("TXT_KEY_ACTION_ALL_UNITS"));

			if (!CvWString(kCommand.getHelp()).empty() &&
				// <advc.004> Don't explain these details if we can't do it anyway
				(kUI.getSelectionList() == NULL ||
				kUI.getSelectionList()->canDoCommand(eCommand,
				// If we do know any command data, it'll have to be this.
				widgetDataStruct.m_iData2, -1)))
			{	// </advc.004>
				szBuffer.append(NEWLINE);
				// <advc.004g>
				if(kAction.getCommandType() == COMMAND_LOAD && pHeadSelectedUnit != NULL &&
						pHeadSelectedUnit->isCargo())
					szBuffer.append(gDLL->getText("TXT_KEY_COMMAND_TRANSFER_HELP"));
				else // </advc.004g>
					szBuffer.append(kCommand.getHelp());
			}
			// <advc.004b>
			if(kAction.getCommandType() == COMMAND_DELETE)
			{
				CvPlayer const& kActivePlayer = GET_PLAYER(getActivePlayer());
				szBuffer.append(L" (");
				int iCurrentUnitExpenses = kActivePlayer.calculateUnitSupply() +
						kActivePlayer.calculateUnitCost();
				// Needed in order to account for inflation
				int iOtherExpenses = kActivePlayer.getTotalMaintenance() +
						kActivePlayer.getCivicUpkeep();
				int iInflationPercent = kActivePlayer.calculateInflationRate();
				int iCurrentExpenses = ((iOtherExpenses + iCurrentUnitExpenses) *
						(iInflationPercent + 100)) / 100;
				FAssert(iCurrentExpenses == kActivePlayer.calculateInflatedCosts());
				int iExtraCost = 0;
				int iUnits = 0;
				for (CLLNode<IDInfo> const* pNode = kUI.headSelectionListNode();
					pNode != NULL; pNode = kUI.nextSelectionListNode(pNode))
				{
					CvUnit const& kUnit = *::getUnit(pNode->m_data);
					iExtraCost += kUnit.getUnitInfo().getExtraCost();
					iUnits--;
					/*  No danger of double counting b/c it's not possible to select
						a transport and its cargo at the same time */
					std::vector<CvUnit*> apCargo;
					kUnit.getCargoUnits(apCargo);
					for (size_t i = 0; i < apCargo.size(); i++)
					{
						iExtraCost += apCargo[i]->getUnitInfo().getExtraCost();
						iUnits--;
					}
				}
				int iProjectedSupply = 0;
				bool bSupply = (!pHeadSelectedUnit->getPlot().isActiveTeam());
				iProjectedSupply = kActivePlayer.calculateUnitSupply(bSupply ? iUnits : 0);
				int iProjectedUnitCost = kActivePlayer.calculateUnitCost(0, iUnits);
				int iProjectedExpenses = iProjectedSupply + iProjectedUnitCost +
						iOtherExpenses - iExtraCost;
				iProjectedExpenses = (iProjectedExpenses *
						(iInflationPercent + 100)) / 100;
				FAssert(iExtraCost >= 0 && iProjectedExpenses >= 0);
				int iGold = iCurrentExpenses - iProjectedExpenses;
				if(iGold > 0)
				{
					szBuffer.append(gDLL->getText("TXT_KEY_COMMAND_DELETE_DECREASE",
							iGold));
				}
				else
				{
					FAssert(iGold == 0);
					int iMaxTries = 5;
					int iDeltaUnits = 0;
					int iOldProj = iProjectedExpenses;
					for(int i = 1; i <= iMaxTries; i++)
					{
						/*  Assume that the additional units are inside borders:
							only recompute UnitCost. */
						iProjectedExpenses = iProjectedSupply - iExtraCost +
								iOtherExpenses;
						iProjectedExpenses += kActivePlayer.calculateUnitCost(0, iUnits - i);
						iProjectedExpenses = (iProjectedExpenses *
								(iInflationPercent + 100)) / 100;
						if(iProjectedExpenses < iOldProj)
						{
							iDeltaUnits = i;
							break;
						}
					}
					if(iDeltaUnits > 0)
					{
						if(iDeltaUnits == 1)
							szBuffer.append(gDLL->getText("TXT_KEY_COMMAND_DELETE_ONE_MORE"));
						else szBuffer.append(gDLL->getText("TXT_KEY_COMMAND_DELETE_MORE",
								iDeltaUnits));
					}
					else if(bSupply)
						szBuffer.append(gDLL->getText("TXT_KEY_COMMAND_DELETE_NO_DECREASE"));
					else szBuffer.append(gDLL->getText("TXT_KEY_COMMAND_DELETE_NO_DECREASE_UNIT_COST"));
				}
				szBuffer.append(L")");
			} // </advc.004b>
		}

		if (kAction.getAutomateType() != NO_AUTOMATE)
		{
			CvAutomateInfo const& kAutomate = GC.getInfo((AutomateTypes)
					kAction.getAutomateType());
			if (!CvWString(kAutomate.getHelp()).empty())
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(kAutomate.getHelp());
			}
		}
	}

	if (kAction.getControlType() != NO_CONTROL)
	{
		CvControlInfo const& kControl = GC.getInfo((ControlTypes)
				kAction.getControlType());
		if (!CvWString(kControl.getHelp()).empty())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(kControl.getHelp());
		}
	}

	if (kAction.getInterfaceModeType() != NO_INTERFACEMODE)
	{
		CvInterfaceModeInfo const& kIMode = GC.getInfo((InterfaceModeTypes)
				kAction.getInterfaceModeType());
		if (!CvWString(kIMode.getHelp()).empty())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(kIMode.getHelp());
		}
	}
}

// advc: Cut from parseActionHelp, refactored.
void CvDLLWidgetData::parseActionHelp_Mission(CvActionInfo const& kAction,
	CvUnit const& kUnit, MissionTypes eMission, CvWStringBuffer& szBuffer)
{
	CvGame const& kGame = GC.getGame();
	CvPlayer const& kUnitOwner = GET_PLAYER(kUnit.getOwner());
	CvTeam const& kUnitTeam = GET_TEAM(kUnit.getTeam());
	bool const bShift = GC.shiftKey();
	CvWString szTempBuffer;
	CvWString szFirstBuffer;

	CvPlot const& kMissionPlot = (
			(bShift && gDLL->UI().mirrorsSelectionGroup()) ?
			*kUnit.getGroup()->lastMissionPlot() :
			*kUnit.plot());
	CvCity* pMissionCity = kMissionPlot.getPlotCity();

	switch(eMission) { // advc: was if/else
	case MISSION_SENTRY_HEAL: // advc.004l
	case MISSION_HEAL:
	{
		int iTurns = 0;
		for (CLLNode<IDInfo> const* pNode = gDLL->UI().headSelectionListNode();
			pNode != NULL; pNode = gDLL->UI().nextSelectionListNode(pNode))
		{
			CvUnit const& kSelectedUnit = *::getUnit(pNode->m_data);
			iTurns = std::max(iTurns, kSelectedUnit.healTurns(&kMissionPlot));
		}
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_TURN_OR_TURNS", iTurns));
		break;
	}
	case MISSION_PILLAGE:
	{	// <advc.111>
		if (kUnit.getDestructibleStructureAt(kMissionPlot, true, GC.ctrlKey()) ==
			CvUnit::STRUCTURE_IMPROVEMENT)
		{
			GAMETEXT.setPillageHelp(szBuffer, kMissionPlot.getImprovementType());
		}
		else
		{
			GAMETEXT.setPillageHelp(szBuffer, kMissionPlot.getRouteType());
			if (!GC.ctrlKey() && kUnit.getDestructibleStructureAt(kMissionPlot, true, true) ==
				CvUnit::STRUCTURE_IMPROVEMENT)
			{
				szBuffer.append(L". (");
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_DESTROY_OWN_STRUCTURE",
						GC.getInfo(kMissionPlot.getRevealedImprovementType(
						getActiveTeam())).getTextKeyWide()));
				szBuffer.append(L".)");
			}
		} // </advc.111>
		break;
	}
	case MISSION_PLUNDER:
	{
		//if (kMissionPlot.getTeam() == kUnitTeam.getID())
		if(!kUnit.canPlunder(kMissionPlot)) // advc.033
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_ACTION_PLUNDER_IN_BORDERS"));
		}
		break;
	}
	case MISSION_SABOTAGE:
	{
		for (CLLNode<IDInfo> const* pNode = gDLL->UI().headSelectionListNode();
			pNode != NULL; pNode = gDLL->UI().nextSelectionListNode(pNode))
		{
			CvUnit const& kSelectedUnit = *::getUnit(pNode->m_data);
			// XXX if queuing up this action, use the current plot along the goto...
			if (!kSelectedUnit.canSabotage(&kMissionPlot, true))
				continue;
			int iPrice = kSelectedUnit.sabotageCost(&kMissionPlot);
			if (iPrice > 0)
			{
				szTempBuffer.Format(L"%d %c", iPrice,
						GC.getInfo(COMMERCE_GOLD).getChar());
				szBuffer.append(NEWLINE);
				szBuffer.append(szTempBuffer);
			}
			int iLow = kSelectedUnit.sabotageProb(&kMissionPlot, PROBABILITY_LOW);
			int iHigh = kSelectedUnit.sabotageProb(&kMissionPlot, PROBABILITY_HIGH);
			if (iLow == iHigh)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_ACTION_PROBABILITY", iHigh));
			}
			else
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_ACTION_PROBABILITY_RANGE",
						iLow, iHigh));
			}
			break;
		}
		break;
	}
	case MISSION_DESTROY:
	{
		for (CLLNode<IDInfo> const* pNode = gDLL->UI().headSelectionListNode();
			pNode != NULL; pNode = gDLL->UI().nextSelectionListNode(pNode))
		{
			CvUnit const& kSelectedUnit = *::getUnit(pNode->m_data);
			// XXX if queuing up this action, use the current plot along the goto...
			if (!kSelectedUnit.canDestroy(&kMissionPlot, true))
				continue;
			int iPrice = kSelectedUnit.destroyCost(&kMissionPlot);
			if (iPrice > 0)
			{
				szTempBuffer.Format(L"%d %c", iPrice,
						GC.getInfo(COMMERCE_GOLD).getChar());
				szBuffer.append(NEWLINE);
				szBuffer.append(szTempBuffer);
			}
			int iLow = kSelectedUnit.destroyProb(&kMissionPlot, PROBABILITY_LOW);
			int iHigh = kSelectedUnit.destroyProb(&kMissionPlot, PROBABILITY_HIGH);
			if (iLow == iHigh)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_ACTION_PROBABILITY", iHigh));
			}
			else
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_ACTION_PROBABILITY_RANGE",
						iLow, iHigh));
			}
			break;
		}
		break;
	}
	case MISSION_STEAL_PLANS:
	{
		for (CLLNode<IDInfo> const* pNode = gDLL->UI().headSelectionListNode();
			pNode != NULL; pNode = gDLL->UI().nextSelectionListNode(pNode))
		{
			CvUnit const& kSelectedUnit = *::getUnit(pNode->m_data);
			// XXX if queuing up this action, use the current plot along the goto...
			if (kSelectedUnit.canStealPlans(&kMissionPlot, true))
			{
				int iPrice = kSelectedUnit.stealPlansCost(&kMissionPlot);
				if (iPrice > 0)
				{
					szTempBuffer.Format(L"%d %c", iPrice,
							GC.getInfo(COMMERCE_GOLD).getChar());
					szBuffer.append(NEWLINE);
					szBuffer.append(szTempBuffer);
				}
				int iLow = kSelectedUnit.stealPlansProb(&kMissionPlot, PROBABILITY_LOW);
				int iHigh = kSelectedUnit.stealPlansProb(&kMissionPlot, PROBABILITY_HIGH);
				if (iLow == iHigh)
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_ACTION_PROBABILITY", iHigh));
				}
				else
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_ACTION_PROBABILITY_RANGE",
							iLow, iHigh));
				}
				break;
			}
		}
		break;
	}
	case MISSION_FOUND:
	{
		if (!kUnitOwner.canFound(kMissionPlot, /* advc.181: */ false, false))
		{
			for (SquareIter it(kMissionPlot, GC.getDefineINT(CvGlobals::MIN_CITY_RANGE));
				it.hasNext(); ++it)
			{
				if (it->isCity() &&
					/*	<advc.181> Don't give away rival cities in the fog of war.
						And same-area check added. */
					!kUnitOwner.canFound(kMissionPlot, false, false) &&
					it->sameArea(kMissionPlot)) // </advc.181>
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_ACTION_CANNOT_FOUND",
							GC.getDefineINT(CvGlobals::MIN_CITY_RANGE)));
					break;
				}
			}
		}
		// <advc.004b> Show the projected increase in city maintenance
		else
		{
			// No projection for the initial city
			if (kUnitOwner.getNumCities() > 0)
				GAMETEXT.setFoundCostHelp(szBuffer, kMissionPlot);
			GAMETEXT.setHomePlotYieldHelp(szBuffer, kMissionPlot);
			GAMETEXT.setFoundHealthHelp(szBuffer, kMissionPlot);
			// To set the info apart from TXT_KEY_MISSION_BUILD_CITY_HELP
			szBuffer.append(NEWLINE);
		} // </advc.004b>
		break;
	}
	case MISSION_SPREAD:
	{
		ReligionTypes eReligion = (ReligionTypes)kAction.getMissionData();
		if(pMissionCity == NULL)
			break;
		if (pMissionCity->getTeam() != kUnitTeam.getID()) // XXX still true???
		{
			if (GET_PLAYER(pMissionCity->getOwner()).isNoNonStateReligionSpread())
			{
				if (eReligion != GET_PLAYER(pMissionCity->getOwner()).getStateReligion())
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_ACTION_CANNOT_SPREAD_NON_STATE_RELIGION"));
				}
			}
		}
		CvWStringBuffer szReligionHelp; // advc.001
		GAMETEXT.setReligionHelpCity(szReligionHelp, eReligion, pMissionCity, false, true);
		// <advc.001> Don't display empty line
		if (!szReligionHelp.isEmpty())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(szReligionHelp);
		} // </advc.001>
		break;
	}
	case MISSION_SPREAD_CORPORATION:
	{
		CorporationTypes eCorporation = (CorporationTypes)kAction.getMissionData();
		if(pMissionCity == NULL)
			break;
		szBuffer.append(NEWLINE);
		GAMETEXT.setCorporationHelpCity(szBuffer, eCorporation, pMissionCity, false, true);
		FOR_EACH_ENUM2(Corporation, eLoopCorp)
		{
			if (eCorporation != eLoopCorp &&
				pMissionCity->isHasCorporation(eLoopCorp) &&
				kGame.isCompetingCorporation(eCorporation, eLoopCorp))
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_ACTION_WILL_ELIMINATE_CORPORATION",
						GC.getInfo(eLoopCorp).getTextKeyWide()));
			}
		}
		CvPlayer const& kMissionCityOwner = GET_PLAYER(pMissionCity->getOwner());
		szTempBuffer.Format(L"%s%d %c", NEWLINE, kUnit.spreadCorporationCost(
				eCorporation, pMissionCity),
				GC.getInfo(COMMERCE_GOLD).getChar());
		szBuffer.append(szTempBuffer);
		if (!kUnit.canSpreadCorporation(&kMissionPlot, eCorporation))
		{
			if (!kMissionCityOwner.isActiveCorporation(eCorporation))
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_ACTION_CORPORATION_NOT_ACTIVE",
						GC.getInfo(eCorporation).getTextKeyWide(),
						kMissionCityOwner.getCivilizationAdjective()));
			}
			CorporationTypes eCompetition = NO_CORPORATION;
			FOR_EACH_ENUM2(Corporation, eLoopCorp)
			{
				if (pMissionCity->isHeadquarters(eLoopCorp) &&
					kGame.isCompetingCorporation(eLoopCorp, eCorporation))
				{
					eCompetition = eLoopCorp;
					break;
				}
			}
			if (eCompetition != NO_CORPORATION)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_ACTION_CORPORATION_COMPETING_HEADQUARTERS",
						GC.getInfo(eCorporation).getTextKeyWide(),
						GC.getInfo(eCompetition).getTextKeyWide()));
			}
			CvWStringBuffer szBonusList;
			bool bValid = false;
			bool bFirst = true;
			for (int i = 0; i < GC.getInfo(eCorporation).getNumPrereqBonuses(); i++)
			{
				BonusTypes const eBonus = GC.getInfo(eCorporation).getPrereqBonus(i);
				if (!bFirst)
					szBonusList.append(L", ");
				else bFirst = false;
				szBonusList.append(GC.getInfo(eBonus).getDescription());
				if (pMissionCity->hasBonus(eBonus))
				{
					bValid = true;
					break;
				}
			}
			if (!bValid)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_ACTION_CORPORATION_NO_RESOURCES",
						pMissionCity->getNameKey(), szBonusList.getCString()));
			}
		}
		break;
	}
	case MISSION_JOIN:
	{
		CvUnit* pSelectedUnit = gDLL->UI().getHeadSelectedUnit();
		GAMETEXT.parseSpecialistHelp(szBuffer, (SpecialistTypes)
				kAction.getMissionData(), pMissionCity, true);

	    // doc: House of Wisdom effect
	    if (GET_PLAYER(pSelectedUnit->getOwner()).isHasBuildingEffect(HOUSE_OF_WISDOM))
	    {
	        szBuffer.append(NEWLINE);
	        szBuffer.append(NEWLINE);
	        szBuffer.append(CvWString::format(SETCOLR L"%s (%s)" ENDCOLR, TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"), GC.getMissionInfo(MISSION_DISCOVER).getDescription(), GC.getBuildingInfo(HOUSE_OF_WISDOM).getText()).c_str());
			// TODO: add discover help from MISSION_DISCOVER
			szBuffer.append(CvWString::format(L"%s%s", NEWLINE, GC.getMissionInfo(MISSION_DISCOVER).getHelp()).c_str());
	    }

		break;
	}
	case MISSION_CONSTRUCT:
	{
		BuildingTypes eBuilding = (BuildingTypes)kAction.getMissionData();
		if(pMissionCity == NULL)
			break;
		if (/*!kUnit.getUnitInfo().getForceBuildings(eBuilding) &&*/ // advc.003t
			!pMissionCity->canConstruct(eBuilding, false, false, true) &&
			!kGame.isBuildingClassMaxedOut(GC.getInfo(eBuilding).getBuildingClassType()))
		{
			GAMETEXT.buildBuildingRequiresString(szBuffer,(BuildingTypes)kAction.
					getMissionData(), false, false, pMissionCity);
		}
		else
		{
			szBuffer.append(NEWLINE);
			//GAMETEXT.setBuildingHelp(szBuffer, (BuildingTypes)kAction.getMissionData(), false, false, false, pMissionCity);
			// BUG - Building Actual Effects - start
			GAMETEXT.setBuildingHelpActual(szBuffer, (BuildingTypes)
					kAction.getMissionData(), false, false, false, pMissionCity);
			// BUG - Building Actual Effects - end
		}
		break;
	}
	case MISSION_DISCOVER:
	{
		for (CLLNode<IDInfo> const* pNode = gDLL->UI().headSelectionListNode();
			pNode != NULL; pNode = gDLL->UI().nextSelectionListNode(pNode))
		{
			CvUnit const& kSelectedUnit = *::getUnit(pNode->m_data);
			if (!kSelectedUnit.canDiscover(&kMissionPlot))
				continue;
			TechTypes const eTech = kSelectedUnit.getDiscoveryTech();
			int const iResearchLeft = GET_TEAM(kSelectedUnit.getTeam()).
					getResearchLeft(eTech);
			if (kSelectedUnit.getDiscoverResearch(eTech) >= iResearchLeft)
			{
				szBuffer.append(NEWLINE);
				szTempBuffer.Format(SETCOLR L"%s" ENDCOLR, TEXT_COLOR("COLOR_TECH_TEXT"),
						GC.getInfo(eTech).getDescription());
				szBuffer.append(szTempBuffer);
				// <advc.004a>
				/*  Probably not a good idea after all. Players might
					not get that this is the amount of research left;
					they could assume that they're only getting
					(partial) progress toward eTech. */
				/*if(iResearchLeft > 0) {
					szTempBuffer.Format(L" (%d%c)", iResearchLeft, GC.getInfo(COMMERCE_RESEARCH).getChar());
					szBuffer.append(szTempBuffer);
				}*/ // </advc.004a>
			}
			else
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_ACTION_EXTRA_RESEARCH",
						kSelectedUnit.getDiscoverResearch(eTech),
						GC.getInfo(eTech).getTextKeyWide()));
			}
			break;
		}
		break;
	}
	case MISSION_HURRY:
	{
		if(pMissionCity == NULL)
			break;
		if (!pMissionCity->isProductionBuilding())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_ACTION_BUILDING_HURRY"));
			break;
		}
		for (CLLNode<IDInfo> const* pNode = gDLL->UI().headSelectionListNode();
			pNode != NULL; pNode = gDLL->UI().nextSelectionListNode(pNode))
		{
			CvUnit const& kSelectedUnit = *::getUnit(pNode->m_data);
			if (!kSelectedUnit.canHurry(&kMissionPlot, true))
				continue;
			wchar const* pcKey = NULL;
			if (pMissionCity->getProductionProject() != NO_PROJECT)
				pcKey = GC.getInfo(pMissionCity->getProductionProject()).getTextKeyWide();
			else if (pMissionCity->getProductionBuilding() != NO_BUILDING)
				pcKey = GC.getInfo(pMissionCity->getProductionBuilding()).getTextKeyWide();
			else if (pMissionCity->getProductionUnit() != NO_UNIT)
				pcKey = GC.getInfo(pMissionCity->getProductionUnit()).getTextKeyWide();
			if (pcKey != NULL && kSelectedUnit.getHurryProduction(&kMissionPlot) >=
				pMissionCity->productionLeft())
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_ACTION_FINISH_CONSTRUCTION", pcKey));
			}
				else
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_ACTION_EXTRA_CONSTRUCTION",
							kSelectedUnit.getHurryProduction(&kMissionPlot), pcKey));
				}
				break;
		}
		break;
	}
	case MISSION_TRADE:
	{
		if(pMissionCity == NULL)
			break;
		if (pMissionCity->getOwner() == kUnitOwner.getID())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_ACTION_TRADE_MISSION_FOREIGN"));
			break;
		}
		for (CLLNode<IDInfo> const* pNode = gDLL->UI().headSelectionListNode();
			pNode != NULL; pNode = gDLL->UI().nextSelectionListNode(pNode))
		{
			CvUnit const& kSelectedUnit = *::getUnit(pNode->m_data);
			if (!kSelectedUnit.canTrade(&kMissionPlot, true))
				continue;
			szTempBuffer.Format(L"%s+%d%c", NEWLINE,
					kSelectedUnit.getTradeGold(&kMissionPlot),
					GC.getInfo(COMMERCE_GOLD).getChar());
			szBuffer.append(szTempBuffer);
			break;
		}
		break;
	}
	case MISSION_GREAT_WORK:
	{
		for (CLLNode<IDInfo> const* pNode = gDLL->UI().headSelectionListNode();
			pNode != NULL; pNode = gDLL->UI().nextSelectionListNode(pNode))
		{
			CvUnit const& kSelectedUnit = *::getUnit(pNode->m_data);
			if (!kSelectedUnit.canGreatWork(&kMissionPlot))
				continue;
			szBuffer.append(NEWLINE);
			/*szTempBuffer.Format(L"+%d%c", kSelectedUnit.getGreatWorkCulture(&kMissionPlot),
					GC.getInfo(COMMERCE_CULTURE).getChar());
			szBuffer.append(szTempBuffer);*/
			// <advc.251>
			int iPerEra=0;
			int iCulture = kSelectedUnit.getGreatWorkCulture(&kMissionPlot, &iPerEra);
			szBuffer.append(gDLL->getText("TXT_KEY_MISSION_GREAT_WORK_WIDGET_HELP",
					iCulture, iPerEra)); // </advc.251>
			break;
		}
		break;
	}
	case MISSION_INFILTRATE:
	{
		if(pMissionCity == NULL)
			break;
		if (pMissionCity->getOwner() == kUnitOwner.getID())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_ACTION_INFILTRATE_MISSION_FOREIGN"));
			break;
		}
		for (CLLNode<IDInfo> const* pNode = gDLL->UI().headSelectionListNode();
			pNode != NULL; pNode = gDLL->UI().nextSelectionListNode(pNode))
		{
			CvUnit const& kSelectedUnit = *::getUnit(pNode->m_data);
			if (!kSelectedUnit.canEspionage(&kMissionPlot))
				continue;
			szTempBuffer.Format(L"%s+%d%c", NEWLINE,
					kSelectedUnit.getEspionagePoints(&kMissionPlot),
					GC.getInfo(COMMERCE_ESPIONAGE).getChar());
			szBuffer.append(szTempBuffer);
			break;
		}
		break;
	}
	case MISSION_GOLDEN_AGE:
	{
		int iUnitConsume = kUnitOwner.unitsRequiredForGoldenAge();
		int iUnitDiff = (iUnitConsume - kUnitOwner.unitsGoldenAgeReady());
		if (iUnitDiff > 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_ACTION_MORE_GREAT_PEOPLE", iUnitDiff));
		}
		if (iUnitConsume > 1)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_ACTION_CONSUME_GREAT_PEOPLE", iUnitConsume));
		}
		break;
	}
	case MISSION_LEAD:
	{
		if (kUnit.getUnitInfo().getLeaderExperience() > 0)
		{
			int iNumUnits = kUnit.canGiveExperience(kUnit.plot());
			if (iNumUnits > 0)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_ACTION_LEAD_TROOPS",
						kUnit.getStackExperienceToGive(iNumUnits)));
			}
		}
		if (kUnit.getUnitInfo().getLeaderPromotion() != NO_PROMOTION)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_WHEN_LEADING"));
			GAMETEXT.parsePromotionHelp(szBuffer, (PromotionTypes)
				kUnit.getUnitInfo().getLeaderPromotion(), L"\n   ");
		}
		break;
	}
	case MISSION_ESPIONAGE:
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_ACTION_ESPIONAGE_MISSION"));
		GAMETEXT.setEspionageMissionHelp(szBuffer, &kUnit);
		break;
	}
	/*	<advc.004c> (Note: similar code in CvGameTextMgr::getAirBombPlotHelp
		for air bomb mission) */
	case MISSION_BOMBARD:
	{
		CvCity const* pBombardCity = kUnit.bombardTarget(kMissionPlot);
		if (pBombardCity == NULL)
			break;
		int const iMaxDamage = pBombardCity->getDefenseModifier(
				kUnit.ignoreBuildingDefense());
		int iDamage = 0;
		for (CLLNode<IDInfo> const* pNode = gDLL->UI().headSelectionListNode();
			pNode != NULL; pNode = gDLL->UI().nextSelectionListNode(pNode))
		{
			CvUnit const& kSelectedUnit = *::getUnit(pNode->m_data);
			iDamage += kSelectedUnit.damageToBombardTarget(kMissionPlot);
			if (iDamage >= iMaxDamage)
			{
				iDamage = iMaxDamage;
				break;
			}
		}
		szBuffer.append(NEWLINE);
		if (iDamage > 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ACTION_BOMBARD_MISSION",
					pBombardCity->getNameKey(), iDamage));
		}
		else szBuffer.append(gDLL->getText("TXT_KEY_ACTION_BOMBARD_MISSION_NO_DAMAGE",
					pBombardCity->getNameKey()));
		break;
	} // </advc.004c>
	case MISSION_BUILD:
	{
		BuildTypes eBuild = (BuildTypes)kAction.getMissionData();
		ImprovementTypes eImprovement = GC.getInfo(eBuild).getImprovement();
		RouteTypes eRoute = GC.getInfo(eBuild).getRoute();
		BonusTypes eBonus = kMissionPlot.getBonusType(kUnitTeam.getID());
		FOR_EACH_ENUM2(Yield, eYield)
		{
			int iYield = 0;
			if (eImprovement != NO_IMPROVEMENT)
			{
				iYield += kMissionPlot.calculateImprovementYieldChange(
						eImprovement, eYield, kUnitOwner.getID());
				if (kMissionPlot.isImproved())
				{
					iYield -= kMissionPlot.calculateImprovementYieldChange(
							kMissionPlot.getImprovementType(), eYield, kUnitOwner.getID());
				}
			}
			if (kMissionPlot.isFeature())
			{
				if (GC.getInfo(eBuild).isFeatureRemove(kMissionPlot.getFeatureType()))
				{
					iYield -= GC.getInfo(kMissionPlot.getFeatureType()).
							getYieldChange(eYield);
				}
			}
			if (iYield != 0)
			{
				szTempBuffer.Format(L", %s%d%c", iYield > 0 ? "+" : "", iYield,
						GC.getInfo(eYield).getChar());
				szBuffer.append(szTempBuffer);
			}
		}
		// advc.059: Moved into new function (and rewritten)
		GAMETEXT.setHealthHappyBuildActionHelp(szBuffer, kMissionPlot, eBuild);
		// advc.059: Feature production (moved up)
		if (kMissionPlot.isFeature() &&
			GC.getInfo(eBuild).isFeatureRemove(kMissionPlot.getFeatureType()))
		{
			CvCity* pProductionCity=NULL;
			int iProduction = kMissionPlot.getFeatureProduction(eBuild,
					kUnitTeam.getID(), &pProductionCity);
			if (iProduction > 0)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_ACTION_CHANGE_PRODUCTION",
						iProduction, pProductionCity->getNameKey()));
			}
		}
		bool bValid = false;
		for (CLLNode<IDInfo> const* pNode = gDLL->UI().headSelectionListNode();
			pNode != NULL; pNode = gDLL->UI().nextSelectionListNode(pNode))
		{
			CvUnit const& kSelectedUnit = *::getUnit(pNode->m_data);
			if (kSelectedUnit.canBuild(kMissionPlot, eBuild))
			{
				bValid = true;
				break;
			}
		}
		if (!bValid)
		{
			if (eImprovement != NO_IMPROVEMENT)
			{
				CvImprovementInfo const& kImprov = GC.getInfo(eImprovement);
				if (kMissionPlot.getTeam() != kUnitTeam.getID())
				{
					if (kImprov.isOutsideBorders())
					{
						if (kMissionPlot.getTeam() != NO_TEAM)
						{
							szBuffer.append(NEWLINE);
							szBuffer.append(gDLL->getText(
									"TXT_KEY_ACTION_NEEDS_OUT_RIVAL_CULTURE_BORDER"));
						}
					}
					else
					{
						szBuffer.append(NEWLINE);
						szBuffer.append(gDLL->getText(
								"TXT_KEY_ACTION_NEEDS_CULTURE_BORDER"));
					}
				}
				if (eBonus == NO_BONUS || !kImprov.isImprovementBonusTrade(eBonus))
				{
					if (!kUnitTeam.isIrrigation() && !kUnitTeam.isIgnoreIrrigation())
					{
						if (kImprov.isRequiresIrrigation() &&
								!kMissionPlot.isIrrigationAvailable())
						{
							FOR_EACH_ENUM(Tech)
							{
								CvTechInfo const& kIrrigTech = GC.getInfo(eLoopTech);
								if (kIrrigTech.isIrrigation())
								{
									szBuffer.append(NEWLINE);
									szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_REQUIRES_STRING",
											kIrrigTech.getTextKeyWide()));
									break;
								}
							}
						}
					}
				}
			}
			TechTypes eBuildPrereq = GC.getInfo(eBuild).getTechPrereq();
			if (!kUnitTeam.isHasTech(eBuildPrereq))
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_REQUIRES_STRING",
						GC.getInfo(eBuildPrereq).getTextKeyWide()));
			}
			if (eRoute != NO_ROUTE)
			{
				BonusTypes const eRoutePrereq = GC.getInfo(eRoute).getPrereqBonus();
				if (eRoutePrereq != NO_BONUS)
				{
					if (!kMissionPlot.isAdjacentPlotGroupConnectedBonus(
							kUnitOwner.getID(), eRoutePrereq))
					{
						szBuffer.append(NEWLINE);
						szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_REQUIRES_STRING",
							GC.getInfo(eRoutePrereq).getTextKeyWide()));
					}
				}
				bool bFoundValid = true;
				std::vector<BonusTypes> aeOrBonuses;
				for (int i = 0; i < GC.getInfo(eRoute).getNumPrereqOrBonuses(); ++i)
				{
					BonusTypes const eRoutePrereqOr = GC.getInfo(eRoute).
							getPrereqOrBonus(i);
					aeOrBonuses.push_back(eRoutePrereqOr);
					bFoundValid = false;
					if (kMissionPlot.isAdjacentPlotGroupConnectedBonus(
						kUnitOwner.getID(), eRoutePrereqOr))
					{
						bFoundValid = true;
						break;
					}
				}
				if (!bFoundValid)
				{
					bool bFirst = true;
					for (std::vector<BonusTypes>::iterator it = aeOrBonuses.begin();
						it != aeOrBonuses.end(); ++it)
					{
						szFirstBuffer = NEWLINE +
								gDLL->getText("TXT_KEY_BUILDING_REQUIRES_LIST");
						szTempBuffer.Format(SETCOLR L"<link=literal>%s</link>" ENDCOLR,
								TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
								GC.getInfo(*it).getDescription());
						setListHelp(szBuffer, szFirstBuffer.GetCString(),
								szTempBuffer, gDLL->getText("TXT_KEY_OR").c_str(), bFirst);
					}
				}
			}
			if (kMissionPlot.isFeature())
			{
				TechTypes eFeatureTech = GC.getInfo(eBuild).
						getFeatureTech(kMissionPlot.getFeatureType());
				if (!kUnitTeam.isHasTech(eFeatureTech))
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_REQUIRES_STRING",
							GC.getInfo(eFeatureTech).getTextKeyWide()));
				}
			}
		}
		if (eImprovement != NO_IMPROVEMENT)
		{
			if (kMissionPlot.isImproved())
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_ACTION_WILL_DESTROY_IMP",
						GC.getInfo(kMissionPlot.getImprovementType()).
						getTextKeyWide()));
			}
		}
		if (GC.getInfo(eBuild).isKill())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_ACTION_CONSUME_UNIT"));
		}
		if (kMissionPlot.isFeature())
		{
			if (GC.getInfo(eBuild).isFeatureRemove(kMissionPlot.getFeatureType()))
			{
				// (advc.059: Feature production moved up)
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_ACTION_REMOVE_FEATURE",
						GC.getInfo(kMissionPlot.getFeatureType()).getTextKeyWide()));
				// UNOFFICIAL_PATCH, Bugfix, 06/10/10, EmperorFool
				if (eImprovement == NO_IMPROVEMENT &&
					kMissionPlot.isImproved() &&
					GC.getInfo(kMissionPlot.getImprovementType()).
					getFeatureMakesValid(kMissionPlot.getFeatureType()))
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_ACTION_WILL_DESTROY_IMP",
							GC.getInfo(kMissionPlot.getImprovementType()).
							getTextKeyWide()));
				} // UNOFFICIAL_PATCH: END
			}
		}
		if (eImprovement != NO_IMPROVEMENT)
		{
			CvImprovementInfo const& kImprov = GC.getInfo(eImprovement);
			if (eBonus != NO_BONUS)
			{
				//if (!kUnitTeam.isBonusObsolete(eBonus))
				if (kUnitOwner.doesImprovementConnectBonus(eImprovement, eBonus)) // K-Mod
				{ //if (kImprov.isImprovementBonusTrade(eBonus))
					CvBonusInfo const& kBonus = GC.getInfo(eBonus);
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_ACTION_PROVIDES_BONUS",
							kBonus.getTextKeyWide()));
					if (kBonus.getHealth() != 0)
					{
						szTempBuffer.Format(L" (+%d%c)", abs(kBonus.getHealth()),
								(kBonus.getHealth() > 0 ?
								gDLL->getSymbolID(HEALTHY_CHAR) :
								gDLL->getSymbolID(UNHEALTHY_CHAR)));
						szBuffer.append(szTempBuffer);
					}
					if (kBonus.getHappiness() != 0)
					{
						szTempBuffer.Format(L" (+%d%c)", abs(kBonus.getHappiness()),
								(kBonus.getHappiness() > 0 ?
								gDLL->getSymbolID(HAPPY_CHAR) :
								gDLL->getSymbolID(UNHAPPY_CHAR)));
						szBuffer.append(szTempBuffer);
					}
				}
			}
			else
			{
				bool bFirst = true;
				FOR_EACH_ENUM2(Bonus, eRandBonus)
				{
					if (kUnitTeam.canDiscoverBonus(eRandBonus) &&
						kImprov.getImprovementBonusDiscoverRand(eRandBonus) > 0 &&
						kMissionPlot.canHaveBonus(eRandBonus, false, // advc.rom3
						true)) // advc.129
					{
						szFirstBuffer.Format(L"%s%s", NEWLINE,
								gDLL->getText("TXT_KEY_ACTION_CHANCE_DISCOVER").c_str());
						szTempBuffer.Format(L"%c", GC.getInfo(eRandBonus).getChar());
						setListHelp(szBuffer, szFirstBuffer, szTempBuffer, L", ", bFirst);
					}
				}
			}
			if (!kMissionPlot.isIrrigationAvailable())
			{
				GAMETEXT.setYieldChangeHelp(szBuffer,
						gDLL->getText("TXT_KEY_ACTION_IRRIGATED").c_str(), L": ", L"",
						GC.getInfo(eImprovement).getIrrigatedYieldChangeArray());
			}
			if (eRoute == NO_ROUTE)
			{
				FOR_EACH_ENUM(Route)
				{
					if (kMissionPlot.getRouteType() != eLoopRoute)
					{
						GAMETEXT.setYieldChangeHelp(szBuffer,
								GC.getInfo(eLoopRoute).getDescription(), L": ", L"",
								kImprov.getRouteYieldChangesArray(eLoopRoute));
					}
				}
			}
			if (kImprov.getDefenseModifier() != 0)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_ACTION_DEFENSE_MODIFIER",
						kImprov.getDefenseModifier()));
			}
			ImprovementTypes eUpgr = kImprov.getImprovementUpgrade();
			if (eUpgr != NO_IMPROVEMENT)
			{
				szBuffer.append(NEWLINE);
				int iTurns = kMissionPlot.getUpgradeTimeLeft(eImprovement,
						kUnitOwner.getID());
				// <advc.912f>
				bool bStagnant = (iTurns < 0);
				if (bStagnant)
				{
					iTurns *= -1;
					szBuffer.append(CvWString::format(SETCOLR,
							TEXT_COLOR("COLOR_LIGHT_GREY")));
				} // </advc.912f>
				szBuffer.append(gDLL->getText("TXT_KEY_ACTION_BECOMES_IMP",
						GC.getInfo(eUpgr).getTextKeyWide(), iTurns));
				// <advc.912f>
				if (bStagnant)
					szBuffer.append(ENDCOLR); // </advc.912f>
			}
		}
		if (eRoute != NO_ROUTE)
		{
			ImprovementTypes eFinalImprovement = eImprovement;
			if (eFinalImprovement == NO_IMPROVEMENT)
				eFinalImprovement = kMissionPlot.getImprovementType();
			if (eFinalImprovement != NO_IMPROVEMENT)
			{
				GAMETEXT.setYieldChangeHelp(szBuffer, GC.getInfo(
						eFinalImprovement).getDescription(), L": ", L"",
						GC.getInfo(eFinalImprovement).
						getRouteYieldChangesArray(eRoute));
			}
			int iMovementCost = GC.getInfo(eRoute).getMovementCost() +
					kUnitTeam.getRouteChange(eRoute);
			int iFlatMovementCost = GC.getInfo(eRoute).getFlatMovementCost();
			int iMoves = GC.getMOVE_DENOMINATOR();
			if (iMovementCost > 0)
			{
				iMoves /= iMovementCost;
				if (iMoves * iMovementCost < GC.getMOVE_DENOMINATOR())
					iMoves++;
			}
			int iFlatMoves = GC.getMOVE_DENOMINATOR();
			if (iFlatMovementCost > 0)
			{
				iFlatMoves /= iFlatMovementCost;
				if (iFlatMoves * iFlatMovementCost < GC.getMOVE_DENOMINATOR())
					iFlatMoves++;
			}
			if (iMoves > 1 || iFlatMoves > 1)
			{
				if (iMoves >= iFlatMoves)
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_ACTION_MOVEMENT_COST", iMoves));
				}
				else
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_ACTION_FLAT_MOVEMENT_COST",
							iFlatMoves));
				}
			}
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_ACTION_CONNECTS_RESOURCES"));
		}
		int iBuildCost = kUnitOwner.getBuildCost(kMissionPlot, eBuild);
		if (iBuildCost > 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_BUILD_COST", iBuildCost));
		}
		int iNowWorkRate = 0;
		int iThenWorkRate = 0;
		for (CLLNode<IDInfo> const* pNode = gDLL->UI().headSelectionListNode();
			pNode != NULL; pNode = gDLL->UI().nextSelectionListNode(pNode))
		{
			CvUnit const& kSelectedUnit = *::getUnit(pNode->m_data);
			if (kSelectedUnit.getBuildType() != eBuild)
			{
				iNowWorkRate += kSelectedUnit.workRate(false);
				iThenWorkRate += kSelectedUnit.workRate(true);
			}

            // doc (merijn): Chateau Frontenac effect
            if (GET_PLAYER(kSelectedUnit.getOwner()).isHasBuildingEffect(FRONTENAC))
            {
                if (GC.getInfo(eBuild).getTechPrereq() == RAILROAD)
                {
                    iNowWorkRate *= 150;
                    iNowWorkRate /= 100;

                    iThenWorkRate *= 150;
                    iThenWorkRate /= 100;
                }
            }
		}
		int iTurns = kMissionPlot.getBuildTurnsLeft(eBuild,
				kUnitOwner.getID(), // advc.251
				iNowWorkRate, iThenWorkRate);
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_ACTION_NUM_TURNS", iTurns));
		CvBuildInfo const& kBuild = GC.getInfo(eBuild);
		if (!CvWString(kBuild.getHelp()).empty())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(kBuild.getHelp());
		} // <advc.011b>
		if(bValid && iTurns > 1 && GC.ctrlKey())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_SUSPEND_WORK"));
		} // </advc.011b>
		break; // advc: Last case of switch(eMission)
	}
	} // end of switch

	if (!CvWString(GC.getInfo(eMission).getHelp()).empty())
	{	// <advc.004a>
		if (eMission == MISSION_DISCOVER)
			GAMETEXT.setDiscoverPathHelp(szBuffer, kUnit.getUnitType());
		else // </advc.004a>  <advc.004c>
		if (eMission == MISSION_BOMBARD && kUnit.bombardTarget(kMissionPlot) != NULL)
		{} // Fully handled in switch block above
		else // </advc.004c>
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(GC.getInfo(eMission).getHelp());
		}
	}
}

// doc
// TODO: not in advciv - alternative? - this handles first and second discover
void CvDLLWidgetData::parseDiscoverHelp(CvPlot* pMissionPlot, CvWStringBuffer& szBuffer)
{
	CvUnit* pSelectedUnit;
	TechTypes eFirstDiscovery, eSecondDiscovery;
	CvWString szTempBuffer;
	int iFirstResearch, iSecondResearch;
	int iFirstResearchLeft, iSecondResearchLeft;

	CLLNode<IDInfo>* pSelectedUnitNode = gDLL->getInterfaceIFace()->headSelectionListNode();

	while (pSelectedUnitNode != NULL)
	{
		pSelectedUnit = ::getUnit(pSelectedUnitNode->m_data);

		if (pSelectedUnit->canDiscover(pMissionPlot))
		{
			eFirstDiscovery = pSelectedUnit->getDiscoveryTech();
			iFirstResearchLeft = GET_TEAM(pSelectedUnit->getTeam()).getResearchLeft(eFirstDiscovery);
			iFirstResearch = pSelectedUnit->getDiscoverResearch(eFirstDiscovery);

			eSecondDiscovery = pSelectedUnit->getDiscoveryTech(eFirstDiscovery);
			iSecondResearch = 0;
			iSecondResearchLeft = -1;

			if (eSecondDiscovery != NO_TECH && iFirstResearch >= iFirstResearchLeft)
			{
				iSecondResearch = std::max(0, pSelectedUnit->getDiscoverResearch(eSecondDiscovery) - iFirstResearchLeft);
				iSecondResearchLeft = pSelectedUnit->getDiscoveryTech(eSecondDiscovery);
			}

			szBuffer.append(NEWLINE);

			if (iFirstResearch >= iFirstResearchLeft)
			{
				szTempBuffer.Format(SETCOLR L"%s" ENDCOLR, TEXT_COLOR("COLOR_TECH_TEXT"), GC.getTechInfo(eFirstDiscovery).getDescription());
				szBuffer.append(szTempBuffer);
			}
			else
			{
				szBuffer.append(gDLL->getText("TXT_KEY_ACTION_EXTRA_RESEARCH", iFirstResearch, GC.getTechInfo(eFirstDiscovery).getTextKeyWide()));
			}

			if (iSecondResearch > 0)
			{
				szBuffer.append(gDLL->getText("TXT_KEY_AND"));

				if (iSecondResearch >= iSecondResearchLeft)
				{
					szTempBuffer.Format(SETCOLR L"%s" ENDCOLR, TEXT_COLOR("COLOR_TECH_TEXT"), GC.getTechInfo(eSecondDiscovery).getDescription());
					szBuffer.append(szTempBuffer);
				}
				else
				{
					szBuffer.append(gDLL->getText("TXT_KEY_ACTION_EXTRA_RESEARCH", iSecondResearch, GC.getTechInfo(eSecondDiscovery).getTextKeyWide()));
				}
			}

			break;
		}

		pSelectedUnitNode = gDLL->getInterfaceIFace()->nextSelectionListNode(pSelectedUnitNode);
	}
}


void CvDLLWidgetData::parseCitizenHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)  // advc: style changes
{
	CvCity* pHeadSelectedCity = gDLL->UI().getHeadSelectedCity();
	if (pHeadSelectedCity == NULL || widgetDataStruct.m_iData1 == NO_SPECIALIST)
		return;

	GAMETEXT.parseSpecialistHelp(szBuffer, (SpecialistTypes)
			widgetDataStruct.m_iData1, pHeadSelectedCity);

	if (widgetDataStruct.m_iData2 == -1)
		return;

	int iCount = 0;
	FOR_EACH_ENUM(Specialist)
	{
		if (eLoopSpecialist < widgetDataStruct.m_iData1)
			iCount += pHeadSelectedCity->getSpecialistCount(eLoopSpecialist);
		else if (eLoopSpecialist == widgetDataStruct.m_iData1)
			iCount += widgetDataStruct.m_iData2;
	}
	if (iCount < pHeadSelectedCity->totalFreeSpecialists())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_FREE_SPECIALIST"));
	}
}


void CvDLLWidgetData::parseFreeCitizenHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity = gDLL->UI().getHeadSelectedCity();
	if (pHeadSelectedCity == NULL)
		return; // advc

	SpecialistTypes eSpecialist = (SpecialistTypes)widgetDataStruct.m_iData1;
	if (NO_SPECIALIST != eSpecialist)
		GAMETEXT.parseSpecialistHelp(szBuffer, eSpecialist, pHeadSelectedCity);
	if (widgetDataStruct.m_iData2 != -1)
	{
		szBuffer.append(SEPARATOR);
		GAMETEXT.parseFreeSpecialistHelp(szBuffer, *pHeadSelectedCity);
	}
}


void CvDLLWidgetData::parseDisabledCitizenHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)  // advc: style changes
{
	CvCity* pHeadSelectedCity = gDLL->UI().getHeadSelectedCity();
	if (pHeadSelectedCity == NULL || widgetDataStruct.m_iData1 == NO_SPECIALIST)
		return;

	GAMETEXT.parseSpecialistHelp(szBuffer, (SpecialistTypes)
			widgetDataStruct.m_iData1, pHeadSelectedCity);

	if (pHeadSelectedCity->isSpecialistValid((SpecialistTypes)
			widgetDataStruct.m_iData1, 1))
		return;

	CvWString szTempBuffer;
	bool bFirst = true;
	CvCivilization const& kCiv = *GC.getGame().getActiveCivilization();
	for (int i = 0; i < kCiv.getNumBuildings(); i++)
	{
		BuildingTypes eLoopBuilding = kCiv.buildingAt(i);
		if (GC.getInfo(eLoopBuilding).getSpecialistCount((SpecialistTypes)
			widgetDataStruct.m_iData1) <= 0)
		{
			continue;
		}
		if (pHeadSelectedCity->getNumBuilding(eLoopBuilding) <= 0 &&
			!GC.getInfo(eLoopBuilding).isLimited())
		{
			if (GC.getInfo(eLoopBuilding).getSpecialBuildingType() == NO_SPECIALBUILDING ||
				pHeadSelectedCity->canConstruct(eLoopBuilding))
			{
				szTempBuffer = NEWLINE + gDLL->getText("TXT_KEY_REQUIRES");
				setListHelp(szBuffer, szTempBuffer, GC.getInfo(
						eLoopBuilding).getDescription(),
						gDLL->getText("TXT_KEY_OR").c_str(), bFirst);
			}
		}
	}

	if (!bFirst)
		szBuffer.append(ENDCOLR);
}


void CvDLLWidgetData::parseAngryCitizenHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity = gDLL->UI().getHeadSelectedCity();
	if (pHeadSelectedCity != NULL)
	{
		szBuffer.assign(gDLL->getText("TXT_KEY_MISC_ANGRY_CITIZEN"));
		szBuffer.append(NEWLINE);

		GAMETEXT.setAngerHelp(szBuffer, *pHeadSelectedCity);
	}
}


void CvDLLWidgetData::parseChangeSpecialistHelp(
	CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity = gDLL->UI().getHeadSelectedCity();
	if (pHeadSelectedCity == NULL)
		return;
	SpecialistTypes const eSpecialist = (SpecialistTypes)widgetDataStruct.m_iData1;
	int const iChange = widgetDataStruct.m_iData2;
	if (iChange > 0)
	{
		GAMETEXT.parseSpecialistHelp(szBuffer, eSpecialist, pHeadSelectedCity);
		if (widgetDataStruct.m_iData1 != GC.getDEFAULT_SPECIALIST())
		{
            // doc: disabled unlimited specialists
			// if (!GET_PLAYER(pHeadSelectedCity->getOwner()).
			//		isSpecialistValid((SpecialistTypes)widgetDataStruct.m_iData1))
			{
				if (pHeadSelectedCity->getMaxSpecialistCount((SpecialistTypes)
						widgetDataStruct.m_iData1) > 0)
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_MISC_MAX_SPECIALISTS",
							pHeadSelectedCity->getMaxSpecialistCount(
							(SpecialistTypes)widgetDataStruct.m_iData1)));
				}
			}
		}
	}
	else
	{
		/*	<advc.004> Stacker display has no separate remove button;
			should therefore show yields regardless of iChange. */
		bool const bStacker = (BUGOption::getValue("CityScreen__Specialists", 2) == 1);
		if (bStacker)
		{
			GAMETEXT.parseSpecialistHelp(szBuffer, eSpecialist, pHeadSelectedCity);
			szBuffer.append(NEWLINE);
		} // </advc.004>
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_REMOVE_SPECIALIST", GC.getInfo(
				(SpecialistTypes)widgetDataStruct.m_iData1).getTextKeyWide()));
		if (pHeadSelectedCity->getForceSpecialistCount((SpecialistTypes)widgetDataStruct.m_iData1) > 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_FORCED_SPECIALIST",
					pHeadSelectedCity->getForceSpecialistCount((SpecialistTypes)
					widgetDataStruct.m_iData1)));
		}
	}
}


void CvDLLWidgetData::parseResearchHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	TechTypes eTech = (TechTypes)widgetDataStruct.m_iData1;
	if (eTech == NO_TECH)
	{
		TechTypes eCurrentResearch = GET_PLAYER(getActivePlayer()).getCurrentResearch();
		if (eCurrentResearch != NO_TECH)
		{
			szBuffer.assign(gDLL->getText("TXT_KEY_MISC_CHANGE_RESEARCH"));
			szBuffer.append(NEWLINE);
			GAMETEXT.setTechHelp(szBuffer, eCurrentResearch, false, true);
		}
	}
	else GAMETEXT.setTechHelp(szBuffer, eTech, false, true, widgetDataStruct.m_bOption);
}


void CvDLLWidgetData::parseTechTreeHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	TechTypes eTech = (TechTypes)widgetDataStruct.m_iData1;
	GAMETEXT.setTechHelp(szBuffer, eTech, false,
			// advc.096: bPlayerContext
			!GET_TEAM(getActiveTeam()).isHasTech(eTech),
			false, false);
}


void CvDLLWidgetData::parseChangePercentHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	int const iChange = widgetDataStruct.m_iData2;
	szBuffer.assign(gDLL->getText(iChange > 0 ?
			"TXT_KEY_MISC_INCREASE_RATE" : "TXT_KEY_MISC_DECREASE_RATE",
			GC.getInfo((CommerceTypes)widgetDataStruct.m_iData1).getTextKeyWide(),
			abs(iChange)));
	// <advc.004> Hint about right-click behavior
	if (!BUGOption::isEnabled("MainInterface__MinMax_Commerce", false))
	{
		szBuffer.append(gDLL->getText(iChange > 0 ?
				"TXT_KEY_MISC_INCREASE_RATE_HINT" :
				"TXT_KEY_MISC_DECREASE_RATE_HINT"));
	} // </advc.004>
}

// advc (comment): Could this function be merged into CvGameTextMgr::parseLeaderHeadHelp?
void CvDLLWidgetData::parseContactCivHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)  // advc: Some style changes
{
	PlayerTypes ePlayer = (PlayerTypes)widgetDataStruct.m_iData1;
	// do not execute if player is not a real civ
	CvPlayerAI const& kPlayer = GET_PLAYER(ePlayer);
	if (kPlayer.getCivilizationType() == NO_CIVILIZATION)
		return;
	// make sure its empty to start
	szBuffer.clear();

	TeamTypes eTeam = kPlayer.getTeam();
	PlayerTypes eActivePlayer = getActivePlayer();
	TeamTypes eActiveTeam = GET_PLAYER(eActivePlayer).getTeam();
	CvTeamAI const& kActiveTeam = GET_TEAM(eActiveTeam);

	// if alt down and cheat on, show extra info
	if (GC.altKey() && //gDLL->getChtLvl() > 0)
		GC.getGame().isDebugMode()) // advc.135c
	{
		// K-Mod. I've moved the code from here into its own function, just to get it out of the way.
		parseScoreboardCheatText(widgetDataStruct, szBuffer);
		// K-Mod end
	}
	// Show score info instead if we are trying to contact ourselves...
	/*  advc.085: No, show active player's contact hover, mainly, for the worst-enemy info.
		(And I've moved these checks into Scoreboard.py.) */
	/*if(eActivePlayer == ePlayer || (GC.ctrlKey() && GC.getGame().isDebugMode())) {
		parseScoreHelp(widgetDataStruct, szBuffer);
		return;
	}*/

    // rfc: show stability and victory info
    // TODO: refactor
    if (eActivePlayer == ePlayer)
    {
        parseCompleteStabilityInfo(widgetDataStruct, szBuffer);
        szBuffer.append(gDLL->getText("TXT_KEY_STABILITY_CHECKF2"));
        szBuffer.append(NEWLINE);

        parseHistoricalVictoryInfo(widgetDataStruct, szBuffer);
        szBuffer.append(gDLL->getText("TXT_KEY_VICTORY_CHECKF8"));
        szBuffer.append(NEWLINE);
        szBuffer.append(gDLL->getText("------------------------"));
        szBuffer.append(NEWLINE);

        parseScoreHelp(widgetDataStruct, szBuffer);
        return;
    }

    // rfc
    szBuffer.assign(gDLL->getText("TXT_KEY_MISC_CONTACT_LEADER", GET_PLAYER(ePlayer).getNameKey(), GET_PLAYER(ePlayer).getCivilizationDescription()));


	/*szBuffer.append(gDLL->getText("TXT_KEY_MISC_CONTACT_LEADER", kPlayer.getNameKey(), kPlayer.getCivilizationShortDescription()));
	szBuffer.append(NEWLINE);
	GAMETEXT.parsePlayerTraits(szBuffer, ePlayer);*/ // BtS
	if (eActivePlayer != ePlayer && // advc.085
			!kActiveTeam.isHasMet(eTeam))
	{	/*	K-Mod. If we haven't met the player yet - don't say "contact".
			Because we can't actually contact them! */
		szBuffer.append(CvWString::format(SETCOLR L"%s" ENDCOLR,
				TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"), kPlayer.getName())); // K-Mod end
		// <advc.007>
		szBuffer.append(L" ");
		GAMETEXT.parsePlayerTraits(szBuffer, ePlayer); // </advc.007>
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_HAVENT_MET_CIV"));
	}
	// K-Mod
	else
	{
		CvWString szTmp; // advc.085
		szTmp.append(gDLL->getText(
				eActivePlayer == ePlayer ? "TXT_KEY_LEADER_CIV_DESCRIPTION" : // advc.085
				"TXT_KEY_MISC_CONTACT_LEADER",
				kPlayer.getNameKey(), kPlayer.getCivilizationShortDescription()));
		// <advc.085>
		if(eActivePlayer == ePlayer)
		{
			szBuffer.append(CvWString::format(SETCOLR L"%s" ENDCOLR,
					TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"), szTmp.GetCString()));
		}
		else szBuffer.append(szTmp); // </advc.085>
		szBuffer.append(NEWLINE);
		GAMETEXT.parsePlayerTraits(szBuffer, ePlayer);
	} // K-Mod end

	bool bWillTalk = false; // advc.007: Needed in outer scope
	if (kActiveTeam.isHasMet(eTeam)
		/*|| GC.getGame().isDebugMode()*/) // advc.007: Not helpful in Debug mode
	{	/*if (!kPlayer.isHuman()) {
			if (!kPlayer.AI_isWillingToTalk(eActivePlayer)) {
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_REFUSES_TO_TALK"));
			}
			if (!((GC.altKey() || GC.ctrlKey()) && gDLL->getChtLvl() > 0)) {
				szBuffer.append(NEWLINE);
				GAMETEXT.getAttitudeString(szBuffer, ePlayer, eActivePlayer);
				szBuffer.append(NEWLINE);
				GAMETEXT.getEspionageString(szBuffer, ((PlayerTypes)widgetDataStruct.m_iData1), eActivePlayer);
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_CTRL_TRADE"));
			}
		}
		else {
			szBuffer.append(NEWLINE);
			GAMETEXT.getEspionageString(szBuffer, ((PlayerTypes)widgetDataStruct.m_iData1), eActivePlayer);
		}*/ // BtS
		bWillTalk = (eActivePlayer == ePlayer || // advc.085
				kPlayer.AI_isWillingToTalk(eActivePlayer, /* advc.104l: */ true));
		// K-Mod
		if (!bWillTalk)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_REFUSES_TO_TALK"));
		}
		if (!((GC.altKey() || GC.ctrlKey()) && //gDLL->getChtLvl() > 0))
			GC.getGame().isDebugMode())) // advc.135c
		{
			if(eActivePlayer != ePlayer && kActiveTeam.isHasMet(eTeam)) // advc.085
				GAMETEXT.getAttitudeString(szBuffer, ePlayer, eActivePlayer);
			GAMETEXT.getWarWearinessString(szBuffer, ePlayer, // K-Mod
					eActivePlayer == ePlayer ? NO_PLAYER : // advc.085
					eActivePlayer);
			// <advc.104v> Handled later
			/*if (!kPlayer.isHuman() && willTalk) {
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_CTRL_TRADE"));
			}*/
		} // K-Mod end
		// <advc.034>
		if(GET_TEAM(eActiveTeam).isDisengage(eTeam))
		{
			CvWString szString;
			GAMETEXT.buildDisengageString(szString, eActivePlayer, ePlayer);
			szBuffer.append(NEWLINE);
			szBuffer.append(szString);
		} // </advc.034>
	}
	if (kActiveTeam.isHasMet(eTeam) || GC.getGame().isDebugMode()) // advc
	{
		//if (eTeam != eActiveTeam) // advc.085
		// Show which civs this player is at war with
		CvWStringBuffer szWarWithString;
		CvWStringBuffer szWorstEnemyString;
		bool bFirstWar = true;
		bool bFirstWorstEnemy = true;
		for (TeamAIIter<MAJOR_CIV,NOT_SAME_TEAM_AS> itOther(eTeam);
			itOther.hasNext(); ++itOther)
		{
			// K-Mod. show "at war" for the active player if appropriate
			//if (itOther->getID() == eActiveTeam) continue;

			if (!kActiveTeam.isHasMet(itOther->getID()) &&
				!GC.getGame().isDebugMode()) // advc.007
			{
				continue;
			}
			if (itOther->isAtWar(eTeam))
			{
				setListHelp(szWarWithString, L"",
						itOther->getName().GetCString(), L", ", bFirstWar);
			}
			if (!itOther->isHuman() && // K-Mod
				itOther->AI_getWorstEnemy() == eTeam)
			{
				setListHelp(szWorstEnemyString, L"",
						itOther->getName().GetCString(), L", ", bFirstWorstEnemy);
			}
		}
		if (!szWarWithString.isEmpty()) // advc.004: List wars before worst enemies
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText(L"TXT_KEY_AT_WAR_WITH",
					szWarWithString.getCString()));
		}
		if (!szWorstEnemyString.isEmpty())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText(L"TXT_KEY_WORST_ENEMY_OF",
					szWorstEnemyString.getCString()));
		}
		// <advc.004v> Moved here from above
		bool bShowCtrlTrade = (
				(!GC.altKey() && !GC.ctrlKey()) &&
				//gDLL->getChtLvl() > 0 && // advc.135c
				!kPlayer.isHuman() && bWillTalk &&
				ePlayer != eActivePlayer); // advc.085
		if (bShowCtrlTrade)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_CTRL_TRADE"));
		} // </advc.004>
		if (!kActiveTeam.isAtWar(eTeam) /* advc.085: */ && ePlayer != eActivePlayer &&
			kActiveTeam.isHasMet(eTeam)) // advc.007
		{
			if (kActiveTeam.canDeclareWar(eTeam))
			{	// <advc.104v>
				if(bShowCtrlTrade)
					szBuffer.append(L", "); // Put them on one line
				else // </advc.104v>
					szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_ALT_DECLARE_WAR"));
			}
			else
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_CANNOT_DECLARE_WAR"));
			}
			/*	K-Mod. The BBAI war plan control currently is
				not implemented for multiplayer, and it is only relevant for team games. */
			if (!GC.getGame().isGameMultiPlayer() && kActiveTeam.getAliveCount() > 1)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_SHIFT_ALT_PREPARE_WAR"));
			}
		}
	}
	if (kPlayer.isHuman() /* advc.085: */ && eActivePlayer != ePlayer)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_SHIFT_SEND_CHAT"));
	}
}

// rfc: display stability info
void CvDLLWidgetData::parseCompleteStabilityInfo(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer) {
	int iStabilityLevel = GC.getPythonCaller()->getStabilityLevel((PlayerTypes)widgetDataStruct.m_iData1);

    szBuffer.append(gDLL->getText("TXT_KEY_STABILITY_ADVISOR_TITLE"));
    szBuffer.append(" ");

	switch (iStabilityLevel)
	{
	case 0:
		szBuffer.append(gDLL->getText("TXT_KEY_STABILITY_COLLAPSING"));
		break;
	case 1:
		szBuffer.append(gDLL->getText("TXT_KEY_STABILITY_UNSTABLE"));
		break;
	case 2:
		szBuffer.append(gDLL->getText("TXT_KEY_STABILITY_SHAKY"));
		break;
	case 3:
		szBuffer.append(gDLL->getText("TXT_KEY_STABILITY_STABLE"));
		break;
	default:
		szBuffer.append(gDLL->getText("TXT_KEY_STABILITY_SOLID"));
	}

    szBuffer.append(NEWLINE);
}

// rfc: display victory info
void CvDLLWidgetData::parseHistoricalVictoryInfo(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer) {
	int iNumAchievedGoals = GC.getPythonCaller()->countAchievedGoals((PlayerTypes)widgetDataStruct.m_iData1);
    szBuffer.append(gDLL->getText("TXT_KEY_VICTORY_ACCOMPLISHED", iNumAchievedGoals));
    szBuffer.append(NEWLINE);
}

// K-Mod. The cheat mode text associated with parseContactCivHelp.
void CvDLLWidgetData::parseScoreboardCheatText(CvWidgetDataStruct &widgetDataStruct,
	CvWStringBuffer &szBuffer)
{
	PlayerTypes const ePlayer = (PlayerTypes)widgetDataStruct.m_iData1;
	CvPlayerAI const& kPlayer = GET_PLAYER(ePlayer);
	TeamTypes const eTeam = kPlayer.getTeam();
	CvTeamAI const& kTeam = GET_TEAM(eTeam);
	PlayerTypes const eActivePlayer = getActivePlayer();

	// Show tech percent adjust
	szBuffer.append(CvWString::format(SETCOLR L"TechPercent: %d%%, CurResMod: %d%%" ENDCOLR,
			TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"), kTeam.getBestKnownTechScorePercent(),
			kPlayer.calculateResearchModifier(kPlayer.getCurrentResearch())));
	szBuffer.append(NEWLINE);
	szBuffer.append(NEWLINE);

	szBuffer.append("Power");
	szBuffer.append(NEWLINE);
	// show everyones power for the active player
	if (eActivePlayer == ePlayer)
	{
		for (PlayerAIIter<CIV_ALIVE> itLoopPlayer; // advc.003n: exclude Barbarians
			itLoopPlayer.hasNext(); ++itLoopPlayer)
		{
			CvPlayerAI const& kLoopPlayer = *itLoopPlayer;
			CvTeam const& kLoopTeam = GET_TEAM(kLoopPlayer.getTeam());
			szBuffer.append(CvWString::format(SETCOLR L"%s (team%d): %d (%d def)" ENDCOLR,
					TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
					kLoopPlayer.getName(), kLoopPlayer.getTeam(), kLoopPlayer.getPower(),
					kLoopTeam.getDefensivePower()));
			// if in financial trouble, show that
			if (kLoopPlayer.AI_isFinancialTrouble())
			{
				szBuffer.append(CvWString::format(SETCOLR L" ($$$)" ENDCOLR,
						TEXT_COLOR("COLOR_NEGATIVE_TEXT")));
			}
			szBuffer.append(NEWLINE);
		}
	}
	// only should this one power if not active player
	else
	{
		szBuffer.append(CvWString::format(SETCOLR L"%d (%d) power" ENDCOLR,
				TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
				kPlayer.getPower(), kTeam.getPower(true)));

		// if in financial trouble, show that
		if (kPlayer.AI_isFinancialTrouble())
		{
			szBuffer.append(CvWString::format(SETCOLR L" ($$$)" ENDCOLR,
					TEXT_COLOR("COLOR_NEGATIVE_TEXT")));
		}

		szBuffer.append(NEWLINE);
	}

	// Strategies
	CvWString szTempBuffer;
	szTempBuffer.Format(L"");

	// advc.007: bDebug=true param added so that human strategies get shown as well
	if (kPlayer.AI_isDoStrategy(AI_STRATEGY_DAGGER, true))
	{
		szTempBuffer.Format(L"Dagger, ");
		szBuffer.append(szTempBuffer);
	}
	if (kPlayer.AI_isDoStrategy(AI_STRATEGY_CRUSH, true))
	{
		szTempBuffer.Format(L"Crush, ");
		szBuffer.append(szTempBuffer);
	}
	if (kPlayer.AI_isDoStrategy(AI_STRATEGY_ALERT1, true))
	{
		szTempBuffer.Format(L"Alert1, ");
		szBuffer.append(szTempBuffer);
	}
	if (kPlayer.AI_isDoStrategy(AI_STRATEGY_ALERT2, true))
	{
		szTempBuffer.Format(L"Alert2, ");
		szBuffer.append(szTempBuffer);
	}
	if (kPlayer.AI_isDoStrategy(AI_STRATEGY_TURTLE, true))
	{
		szTempBuffer.Format(L"Turtle, ");
		szBuffer.append(szTempBuffer);
	}
	if (kPlayer.AI_isDoStrategy(AI_STRATEGY_LAST_STAND, true))
	{
		szTempBuffer.Format(L"LastStand, ");
		szBuffer.append(szTempBuffer);
	}
	if (kPlayer.AI_isDoStrategy(AI_STRATEGY_FINAL_WAR, true))
	{
		szTempBuffer.Format(L"FinalWar, ");
		szBuffer.append(szTempBuffer);
	}
	if (kPlayer.AI_isDoStrategy(AI_STRATEGY_GET_BETTER_UNITS, true))
	{
		szTempBuffer.Format(L"GetBetterUnits, ");
		szBuffer.append(szTempBuffer);
	}
	if (kPlayer.AI_isDoStrategy(AI_STRATEGY_PRODUCTION, true))
	{
		szTempBuffer.Format(L"Production, ");
		szBuffer.append(szTempBuffer);
	}
	if (kPlayer.AI_isDoStrategy(AI_STRATEGY_MISSIONARY, true))
	{
		szTempBuffer.Format(L"Missionary, ");
		szBuffer.append(szTempBuffer);
	}
	if (kPlayer.AI_isDoStrategy(AI_STRATEGY_BIG_ESPIONAGE, true))
	{
		szTempBuffer.Format(L"BigEspionage, ");
		szBuffer.append(szTempBuffer);
	}
	if (kPlayer.AI_isDoStrategy(AI_STRATEGY_ECONOMY_FOCUS, true)) // K-Mod
	{
		szTempBuffer.Format(L"EconomyFocus, ");
		szBuffer.append(szTempBuffer);
	}
	if (kPlayer.AI_isDoStrategy(AI_STRATEGY_ESPIONAGE_ECONOMY, true)) // K-Mod
	{
		szTempBuffer.Format(L"EspionageEconomy, ");
		szBuffer.append(szTempBuffer);
	}

	szBuffer.append(NEWLINE);
	szTempBuffer.Format(L"Vic Strats: ");
	szBuffer.append(szTempBuffer);

	szTempBuffer.Format(L"");
	// Victory strategies

	/*  <advc.007> Reordered and "else" added so that only the highest stage is
		displayed. */
	if (kPlayer.AI_atVictoryStage(AI_VICTORY_CULTURE4))
	{
		szTempBuffer.Format(L"Culture4, ");
		szBuffer.append(szTempBuffer);
	}
	else if (kPlayer.AI_atVictoryStage(AI_VICTORY_CULTURE3))
	{
		szTempBuffer.Format(L"Culture3, ");
		szBuffer.append(szTempBuffer);
	}
	else if (kPlayer.AI_atVictoryStage(AI_VICTORY_CULTURE2))
	{
		szTempBuffer.Format(L"Culture2, ");
		szBuffer.append(szTempBuffer);
	}
	else if (kPlayer.AI_atVictoryStage(AI_VICTORY_CULTURE1))
	{
		szTempBuffer.Format(L"Culture1, ");
		szBuffer.append(szTempBuffer);
	}

	if (kPlayer.AI_atVictoryStage(AI_VICTORY_SPACE4))
	{
		szTempBuffer.Format(L"Space4, ");
		szBuffer.append(szTempBuffer);
	}
	else if (kPlayer.AI_atVictoryStage(AI_VICTORY_SPACE3))
	{
		szTempBuffer.Format(L"Space3, ");
		szBuffer.append(szTempBuffer);
	}
	else if (kPlayer.AI_atVictoryStage(AI_VICTORY_SPACE2))
	{
		szTempBuffer.Format(L"Space2, ");
		szBuffer.append(szTempBuffer);
	}
	else if (kPlayer.AI_atVictoryStage(AI_VICTORY_SPACE1))
	{
		szTempBuffer.Format(L"Space1, ");
		szBuffer.append(szTempBuffer);
	}

	if (kPlayer.AI_atVictoryStage(AI_VICTORY_CONQUEST4))
	{
		szTempBuffer.Format(L"Conq4, ");
		szBuffer.append(szTempBuffer);
	}
	else if (kPlayer.AI_atVictoryStage(AI_VICTORY_CONQUEST3))
	{
		szTempBuffer.Format(L"Conq3, ");
		szBuffer.append(szTempBuffer);
	}
	else if (kPlayer.AI_atVictoryStage(AI_VICTORY_CONQUEST2))
	{
		szTempBuffer.Format(L"Conq2, ");
		szBuffer.append(szTempBuffer);
	}
	else if (kPlayer.AI_atVictoryStage(AI_VICTORY_CONQUEST1))
	{
		szTempBuffer.Format(L"Conq1, ");
		szBuffer.append(szTempBuffer);
	}

	if (kPlayer.AI_atVictoryStage(AI_VICTORY_DOMINATION4))
	{
		szTempBuffer.Format(L"Dom4, ");
		szBuffer.append(szTempBuffer);
	}
	else if (kPlayer.AI_atVictoryStage(AI_VICTORY_DOMINATION3))
	{
		szTempBuffer.Format(L"Dom3, ");
		szBuffer.append(szTempBuffer);
	}
	else if (kPlayer.AI_atVictoryStage(AI_VICTORY_DOMINATION2))
	{
		szTempBuffer.Format(L"Dom2, ");
		szBuffer.append(szTempBuffer);
	}
	else if (kPlayer.AI_atVictoryStage(AI_VICTORY_DOMINATION1))
	{
		szTempBuffer.Format(L"Dom1, ");
		szBuffer.append(szTempBuffer);
	}

	if (kPlayer.AI_atVictoryStage(AI_VICTORY_DIPLOMACY4))
	{
		szTempBuffer.Format(L"Diplo4, ");
		szBuffer.append(szTempBuffer);
	}
	else if (kPlayer.AI_atVictoryStage(AI_VICTORY_DIPLOMACY3))
	{
		szTempBuffer.Format(L"Diplo3, ");
		szBuffer.append(szTempBuffer);
	}
	else if (kPlayer.AI_atVictoryStage(AI_VICTORY_DIPLOMACY2))
	{
		szTempBuffer.Format(L"Diplo2, ");
		szBuffer.append(szTempBuffer);
	}
	else if (kPlayer.AI_atVictoryStage(AI_VICTORY_DIPLOMACY1))
	{
		szTempBuffer.Format(L"Diplo1, ");
		szBuffer.append(szTempBuffer);
	} // </advc.007>

	// List the top 3 culture cities (by culture value weight).
	//if (kPlayer.AI_atVictoryStage(AI_VICTORY_CULTURE1))
	/*  advc.007: The line above was already commented out; i.e. culture info was
		always shown. */
	if (kPlayer.AI_atVictoryStage(AI_VICTORY_CULTURE3) || GC.ctrlKey())
	{
		szBuffer.append(CvWString::format(L"\n\nTop %c cities by weight:",
				GC.getInfo(COMMERCE_CULTURE).getChar()));
		int iLegendaryCulture = GC.getGame().getCultureThreshold(
				CvCultureLevelInfo::finalCultureLevel());
		std::vector<std::pair<int,int> > city_list; // (weight, city id)

		FOR_EACH_CITYAI(pLoopCity, kPlayer)
		{
			city_list.push_back(std::make_pair(
					kPlayer.AI_commerceWeight(COMMERCE_CULTURE, pLoopCity),
					pLoopCity->getID()));
		}
		int iListCities = std::min((int)city_list.size(), 3);
		std::partial_sort(city_list.begin(), city_list.begin()+iListCities,
				city_list.end(), std::greater<std::pair<int,int> >());

		int iGoldCommercePercent = kPlayer.AI_estimateBreakEvenGoldPercent();

		for (int i = 0; i < iListCities; i++)
		{
			CvCity const* pLoopCity = kPlayer.getCity(city_list[i].second);
			int iEstimatedRate = pLoopCity->getCommerceRate(COMMERCE_CULTURE);
			iEstimatedRate +=
					(100 - iGoldCommercePercent - kPlayer.getCommercePercent(COMMERCE_CULTURE)) *
					pLoopCity->getYieldRate(YIELD_COMMERCE) *
					pLoopCity->getTotalCommerceRateModifier(COMMERCE_CULTURE) / 10000;
			int iCountdown = (iLegendaryCulture - pLoopCity->getCulture(kPlayer.getID())) /
					std::max(1, iEstimatedRate);

			szBuffer.append(CvWString::format(L"\n %s:\t%d%%, %d turns",
					pLoopCity->getName().GetCString(), city_list[i].first, iCountdown));
		}
		szBuffer.append(CvWString::format(L"\n(assuming %d%% gold)", iGoldCommercePercent));
	}

	// skip a line
	szBuffer.append(NEWLINE);
	szBuffer.append(NEWLINE);
	{
		// show peace values
		bool bHadAny = false;
		bool bFirst = true;
		for (TeamAIIter<MAJOR_CIV,ENEMY_OF> itEnemy(eTeam); itEnemy.hasNext(); ++itEnemy)
		{
			if (bFirst)
			{
				szBuffer.append(CvWString::format(SETCOLR L"Current War:\n" ENDCOLR,
						TEXT_COLOR("COLOR_UNIT_TEXT")));
				bFirst = false;
			}
			bHadAny = true;
			WarPlanTypes const eWarPlan = kTeam.AI_getWarPlan(itEnemy->getID());
			CvWStringBuffer szWarplan;
			GAMETEXT.getWarplanString(szWarplan, eWarPlan);
			// <advc.104>
			if(getUWAI().isEnabled())
			{
				szBuffer.append(CvWString::format(
						SETCOLR L" %s (%d) with %s\n" ENDCOLR,
						TEXT_COLOR("COLOR_NEGATIVE_TEXT"),
						szWarplan.getCString(),
						kTeam.AI_getWarPlanStateCounter(itEnemy->getID()),
						itEnemy->getName().GetCString()));
			}
			else // </advc.104>
			{
				int iOtherValue = kTeam.AI_endWarVal(itEnemy->getID());
				int iTheirValue = itEnemy->AI_endWarVal(eTeam);
				szBuffer.append(CvWString::format(SETCOLR L" %s "
						ENDCOLR SETCOLR L"(%d, %d)" ENDCOLR SETCOLR L" with %s "
						ENDCOLR  SETCOLR L"(%d, %d)\n" ENDCOLR,
						TEXT_COLOR((iOtherValue < iTheirValue) ?
						"COLOR_POSITIVE_TEXT" : "COLOR_NEGATIVE_TEXT"),
						szWarplan.getCString(),
						TEXT_COLOR((iOtherValue < iTheirValue) ?
						"COLOR_POSITIVE_TEXT" : "COLOR_NEGATIVE_TEXT"),
						iOtherValue, kTeam.AI_getWarSuccess(itEnemy->getID()).uround(),
						TEXT_COLOR((iOtherValue < iTheirValue) ?
						"COLOR_POSITIVE_TEXT" : "COLOR_NEGATIVE_TEXT"),
						itEnemy->getName().GetCString(),
						TEXT_COLOR((iTheirValue < iOtherValue) ?
						"COLOR_POSITIVE_TEXT" : "COLOR_NEGATIVE_TEXT"),
						iTheirValue, itEnemy->AI_getWarSuccess(eTeam).uround()));
			}
		}
		if (kTeam.AI_isAnyWarPlan()) // double space if had any war
		{
			int iEnemyPowerPercent = kTeam.AI_getEnemyPowerPercent();
			szBuffer.append(CvWString::format(SETCOLR L"\nEnemy Power Percent: %d" ENDCOLR,
					TEXT_COLOR(iEnemyPowerPercent < 100 ?
					"COLOR_POSITIVE_TEXT" : "COLOR_NEGATIVE_TEXT"),
					iEnemyPowerPercent));

		}
		if (bHadAny)
		{
			int iWarSuccessRating = kTeam.AI_getWarSuccessRating();
			szBuffer.append(CvWString::format(SETCOLR L"\nWar Success Ratio: %d" ENDCOLR,
					TEXT_COLOR((iWarSuccessRating > 0) ?
					"COLOR_POSITIVE_TEXT" : "COLOR_NEGATIVE_TEXT"),
					iWarSuccessRating));
		}
		if (bHadAny || kTeam.AI_isAnyWarPlan())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(NEWLINE);
		}
	}
	{
		// show warplan values
		bool bHadAny = false;
		bool bFirst = true;
		for (TeamIter<CIV_ALIVE,NOT_SAME_TEAM_AS> itRival(eTeam);
			itRival.hasNext(); ++itRival)
		{
			WarPlanTypes const eWarPlan = kTeam.AI_getWarPlan(itRival->getID());
			if (itRival->isAtWar(eTeam) || eWarPlan == NO_WARPLAN)
				continue;
			if (bFirst)
			{
				szBuffer.append(CvWString::format(SETCOLR L"Imminent War:\n" ENDCOLR,
						TEXT_COLOR("COLOR_UNIT_TEXT")));
						bFirst = false;
			}
			bHadAny = true;
			CvWStringBuffer szWarplan;
			GAMETEXT.getWarplanString(szWarplan, eWarPlan);
			szBuffer.append(CvWString::format(SETCOLR L" %s (%d) with %s\n" ENDCOLR,
					TEXT_COLOR("COLOR_NEGATIVE_TEXT"),
					szWarplan.getCString(),
					// advc.104: Show war plan age instead of K-Mod's startWarVal
					getUWAI().isEnabled() ? kTeam.AI_getWarPlanStateCounter(itRival->getID()) :
					kTeam.AI_startWarVal(itRival->getID(), eWarPlan,
					true), // advc.001n
					itRival->getName().GetCString()));
		}
		// double space if had any war plan
		if (bHadAny)
			szBuffer.append(NEWLINE);
	}
	// <advc.104> K-Mod/BBAI war percentages aren't helpful for testing UWAI
	if (getUWAI().isEnabled())
		return; // </advc.104>

	// calculate war percentages
	float fOverallWarPercentage = 0;
	bool const bAnyCapitalAreaAlone = kTeam.AI_isAnyCapitalAreaAlone();
	bool bAggressive = GC.getGame().isOption(GAMEOPTION_AGGRESSIVE_AI);
	int iFinancialTroubleCount = 0;
	int iDaggerCount = 0;
	int iGetBetterUnitsCount = 0;
	for (MemberAIIter itMember(eTeam); itMember.hasNext(); ++itMember)
	{
		if (itMember->AI_isDoStrategy(AI_STRATEGY_DAGGER, /* advc.007: */ true) ||
			itMember->AI_atVictoryStage(AI_VICTORY_CONQUEST3) ||
			itMember->AI_atVictoryStage(AI_VICTORY_DOMINATION4))
		{
			iDaggerCount++;
			bAggressive = true;
		}
		if (itMember->AI_isDoStrategy(AI_STRATEGY_GET_BETTER_UNITS, /* advc.007: */ true))
			iGetBetterUnitsCount++;
		if (itMember->AI_isFinancialTrouble())
			iFinancialTroubleCount++;
	}

	// calculate unit spending for use in iTotalWarRandThreshold ...

	/*	if random in this range is 0, we go to war of this type
		(so lower numbers are higher probablity) average of everyone on our team */
	int iTotalWarRand;
	int iLimitedWarRand;
	int iDogpileWarRand;
	kTeam.AI_getWarRands(iTotalWarRand, iLimitedWarRand, iDogpileWarRand);

	int iTotalWarThreshold;
	int iLimitedWarThreshold;
	int iDogpileWarThreshold;
	kTeam.AI_getWarThresholds(iTotalWarThreshold, iLimitedWarThreshold, iDogpileWarThreshold);

	// we oppose war if half the non-dagger teammates in financial trouble
	bool bFinancesOpposeWar = false;
	if ((iFinancialTroubleCount - iDaggerCount) >= std::max(1, kTeam.getNumMembers() / 2))
	{	// this can be overridden by by the pro-war booleans
		bFinancesOpposeWar = true;
	}

	// if agressive, we may start a war to get money
	bool bFinancesProTotalWar = false;
	bool bFinancesProLimitedWar = false;
	bool bFinancesProDogpileWar = false;
	if (iFinancialTroubleCount > 0)
	{
		// do we like all out wars?
		if (iDaggerCount > 0 || iTotalWarRand < 100)
			bFinancesProTotalWar = true;
		// do we like limited wars?
		if (iLimitedWarRand < 100)
			bFinancesProLimitedWar = true;
		// do we like dogpile wars?
		if (iDogpileWarRand < 100)
			bFinancesProDogpileWar = true;
	}
	bool const bFinancialProWar = (bFinancesProTotalWar ||
			bFinancesProLimitedWar || bFinancesProDogpileWar);

	// overall war check (quite frequently true)
	int const iMembers = kTeam.getNumMembers();
	if ((iGetBetterUnitsCount - iDaggerCount) * 3 < iMembers * 2)
	{
		if (bFinancialProWar || !bFinancesOpposeWar)
		{
			fOverallWarPercentage = std::min(100.f, (float)GC.getInfo(
					GC.getGame().getHandicapType()).getAIDeclareWarProb());
		}
	}

	// team power (if agressive, we use higher value)
	int iTeamPower = kTeam.getPower(true);
	if (bAggressive && !kTeam.AI_isAnyWarPlan())
	{
		iTeamPower *= 4;
		iTeamPower /= 3;
	}

	iTeamPower *= 100 - kTeam.AI_getEnemyPowerPercent();
	iTeamPower /= 100;

	// we will put the values into an array, then sort it for display
	int iBestPossibleMaxWarPass = MAX_INT;
	struct CvStartWarInfo
	{
		int		iStartWarValue;
		int		iNoWarAttitudeProb;
		int		iPossibleMaxWarPass;
		bool	bPossibleLimitedWar;
		bool	bPossibleDogpileWar;
		bool	bEnoughDogpilePower;

		bool	bValid;
		bool	bLandTarget;
		bool	bVictory4;
		//bool	bAnyCapitalAreaAlone; // advc: unused
		bool	bAdjacentCheckPassed;
		bool	bMaxWarNearbyPowerRatio;
		bool	bMaxWarDistantPowerRatio;
	} aStartWarInfo[MAX_TEAMS];

	// first calculate all the values and put into array
	FOR_EACH_ENUM(Team)
	{
		aStartWarInfo[eLoopTeam].bValid = false;
		CvTeamAI& kLoopTeam = GET_TEAM(eLoopTeam);
		if (eLoopTeam != eTeam && kLoopTeam.isAlive() && !kLoopTeam.isBarbarian())
		{
			WarPlanTypes eWarPlan = kTeam.AI_getWarPlan(eLoopTeam);
			if (!kTeam.isAtWar(eLoopTeam) && eWarPlan == NO_WARPLAN &&
				kTeam.canEventuallyDeclareWar(eLoopTeam) && kTeam.isHasMet(eLoopTeam))
			{
				if (GET_TEAM(eLoopTeam).isAVassal() &&
					!kTeam.AI_isOkayVassalTarget(eLoopTeam))
				{
					continue;
				}
				aStartWarInfo[eLoopTeam].bValid = true;

				int iLoopTeamPower = kLoopTeam.getDefensivePower();
				bool bLandTarget = kTeam.AI_isLandTarget(eLoopTeam);
				aStartWarInfo[eLoopTeam].bLandTarget = bLandTarget;

				bool bVictory4 = GET_TEAM(eLoopTeam).AI_anyMemberAtVictoryStage4();
				aStartWarInfo[eLoopTeam].bVictory4 = bVictory4;

				//int iNoWarAttitudeProb = kTeam.AI_noWarAttitudeProb(kTeam.AI_getAttitude(eLoopTeam));
				int iNoWarAttitudeProb = std::max(
						kTeam.AI_noWarAttitudeProb(
						kTeam.AI_getAttitude(eLoopTeam)),
						kTeam.AI_noWarAttitudeProb(
						kTeam.AI_getAttitude(GET_TEAM(eLoopTeam).getMasterTeam())));
				aStartWarInfo[eLoopTeam].iNoWarAttitudeProb = iNoWarAttitudeProb;

				// total war
				aStartWarInfo[eLoopTeam].iPossibleMaxWarPass = MAX_INT;
				if (iNoWarAttitudeProb < 100 && (bFinancesProTotalWar || !bFinancesOpposeWar))
				{
					int iNoWarChance = range(iNoWarAttitudeProb
							- (bAggressive ? 10 : 0)
							- (bFinancesProTotalWar ? 10 : 0) +
							(20 * iGetBetterUnitsCount) / iMembers, 0, 100);
					if (iNoWarChance < 100)
					{
						bool bMaxWarNearbyPowerRatio = (iLoopTeamPower <
								((iTeamPower * kTeam.AI_maxWarNearbyPowerRatio()) / 100));
						bool bMaxWarDistantPowerRatio = (iLoopTeamPower <
								((iTeamPower * kTeam.AI_maxWarDistantPowerRatio()) / 100));
						aStartWarInfo[eLoopTeam].bMaxWarNearbyPowerRatio = bMaxWarNearbyPowerRatio;
						aStartWarInfo[eLoopTeam].bMaxWarDistantPowerRatio = bMaxWarDistantPowerRatio;

						bool bAdjacentCheckPassed = true;
						int iMaxWarMinAdjacentPercent = kTeam.AI_maxWarMinAdjacentLandPercent();
						if (iMaxWarMinAdjacentPercent > 0)
						{
							int iMinAdjacentPlots =
									(kTeam.getTotalLand() * iMaxWarMinAdjacentPercent) / 100;
							if (iMinAdjacentPlots > 0)
							{
								bAdjacentCheckPassed =
										(kTeam.AI_calculateAdjacentLandPlots(eLoopTeam) >=
										iMinAdjacentPlots);
							}
						}
						aStartWarInfo[eLoopTeam].bAdjacentCheckPassed = bAdjacentCheckPassed;

						// check to see which max war pass, if any is valid for this loop team
						int iPossibleMaxWarPass = MAX_INT;
						if (bMaxWarNearbyPowerRatio && (bAdjacentCheckPassed || bVictory4))
							iPossibleMaxWarPass = 0;
						else if (bMaxWarNearbyPowerRatio &&
							(bLandTarget || bAnyCapitalAreaAlone || bVictory4))
						{
							iPossibleMaxWarPass = 1;
						}
						else if (bMaxWarDistantPowerRatio)
							iPossibleMaxWarPass = 2;
						aStartWarInfo[eLoopTeam].iPossibleMaxWarPass = iPossibleMaxWarPass;
						// if this team is valid on a lower pass, then it is the best pass
						if (iPossibleMaxWarPass < iBestPossibleMaxWarPass)
							iBestPossibleMaxWarPass = iPossibleMaxWarPass;
					}
				}
				// limited war
				aStartWarInfo[eLoopTeam].bPossibleLimitedWar = false;
				if (iNoWarAttitudeProb < 100 &&
					(bFinancesProLimitedWar || !bFinancesOpposeWar))
				{
					int iNoWarChance = std::max(0, iNoWarAttitudeProb + 10 -
							(bAggressive ? 10 : 0) -
							(bFinancesProLimitedWar ? 10 : 0));
					if (iNoWarChance < 100)
					{
						bool bLimitedPowerRatio = (iLoopTeamPower <
								((iTeamPower * kTeam.AI_limitedWarPowerRatio()) / 100));
						bool bAnyLoopTeamCapitalAreaAlone = kLoopTeam.AI_isAnyCapitalAreaAlone();
						if (bLimitedPowerRatio && (bLandTarget ||
							(bAnyCapitalAreaAlone && bAnyLoopTeamCapitalAreaAlone)))
						{
							aStartWarInfo[eLoopTeam].bPossibleLimitedWar = true;
						}
					}
				}

				// dogpile war
				aStartWarInfo[eLoopTeam].bPossibleDogpileWar = false;
				aStartWarInfo[eLoopTeam].bEnoughDogpilePower = false;
				if (iNoWarAttitudeProb < 100 &&
					(bFinancesProDogpileWar || !bFinancesOpposeWar) &&
					kTeam.canDeclareWar(eLoopTeam))
				{
					int iNoWarChance = std::max(0,
							iNoWarAttitudeProb + 20 -
							(bAggressive ? 10 : 0) -
							(bFinancesProDogpileWar ? 10 : 0));
					if (iNoWarChance < 100)
					{
						int iDogpilePower = iTeamPower;
						for (TeamIter<CIV_ALIVE,ENEMY_OF> itDogpileLoopTeam(eLoopTeam);
							itDogpileLoopTeam.hasNext(); ++itDogpileLoopTeam)
						{
							iDogpilePower += itDogpileLoopTeam->getPower(false);
						}
						bool bDogpilePowerRatio = ((iLoopTeamPower * 3) / 2 < iDogpilePower);
						aStartWarInfo[eLoopTeam].bPossibleDogpileWar = true;
						if (bDogpilePowerRatio)
							aStartWarInfo[eLoopTeam].bEnoughDogpilePower = true;
					}
				}
				// if this team can have any war, calculate the start war value
				aStartWarInfo[eLoopTeam].iStartWarValue = 0;
				if (aStartWarInfo[eLoopTeam].iPossibleMaxWarPass < MAX_INT ||
					aStartWarInfo[eLoopTeam].bPossibleLimitedWar ||
					aStartWarInfo[eLoopTeam].bPossibleDogpileWar)
				{
					aStartWarInfo[eLoopTeam].iStartWarValue = kTeam.AI_startWarVal(
							eLoopTeam, WARPLAN_TOTAL, /* advc.001n: */ true);
				}
			}
		}
	}

	if (bFinancesOpposeWar)
	{
		szBuffer.append(CvWString::format(SETCOLR L"## Finances oppose war%s%s%s\n" ENDCOLR,
				TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
				bFinancesProTotalWar ? L", pro Total" : L"",
				bFinancesProLimitedWar ? L", pro Limited" : L"",
				bFinancesProDogpileWar ? L", pro Dogpile" : L""));
		szBuffer.append(NEWLINE);
	}

	{
		// display total war items, sorting the list
		bool bHadAny = false;
		bool bFirst = true;
		int iBestValue;
		int iLastValue = MAX_INT;
		do
		{
			// find the highest value item left to do
			iBestValue = 0;
			FOR_EACH_ENUM(Team)
			{
				if (aStartWarInfo[eLoopTeam].bValid &&
					aStartWarInfo[eLoopTeam].iPossibleMaxWarPass < MAX_INT)
				{
					if (aStartWarInfo[eLoopTeam].iStartWarValue > iBestValue &&
						aStartWarInfo[eLoopTeam].iStartWarValue < iLastValue)
					{
						iBestValue = aStartWarInfo[eLoopTeam].iStartWarValue;
					}
				}
			}
			if (iBestValue > 0) // did we find one?
			{
				// setup for next loop
				iLastValue = iBestValue;
				// now display every team that has that value
				FOR_EACH_ENUM(Team)
				{
					if (aStartWarInfo[eLoopTeam].bValid &&
						aStartWarInfo[eLoopTeam].iStartWarValue == iBestValue)
					{
						CvTeam const& kLoopTeam = GET_TEAM(eLoopTeam);
						if (bFirst)
						{
							float fMaxWarPercentage = ((fOverallWarPercentage *
									(iTotalWarThreshold + 1)) / iTotalWarRand);
							szBuffer.append(CvWString::format(
									SETCOLR L"%.2f%% [%d/%d] Total War:\n" ENDCOLR,
									TEXT_COLOR("COLOR_UNIT_TEXT"), fMaxWarPercentage,
									iTotalWarThreshold + 1, iTotalWarRand));
							bFirst = false;
						}
						bHadAny = true;
						int iNoWarChance = std::max(0,
								aStartWarInfo[eLoopTeam].iNoWarAttitudeProb -
								(bAggressive ? 10 : 0) - (bFinancesProTotalWar ? 10 : 0));
						int iTeamWarPercentage = (100 - iNoWarChance);

						if (aStartWarInfo[eLoopTeam].iPossibleMaxWarPass <=
							iBestPossibleMaxWarPass)
						{
							szBuffer.append(CvWString::format(
									SETCOLR L" %d%% %s%s war (%d) with %s\n" ENDCOLR,
									TEXT_COLOR("COLOR_ALT_HIGHLIGHT_TEXT"),
									iTeamWarPercentage,
									(aStartWarInfo[eLoopTeam].bVictory4) ? L"**" : L"",
									(aStartWarInfo[eLoopTeam].bLandTarget) ? L"land" : L"sea",
									aStartWarInfo[eLoopTeam].iStartWarValue,
									kLoopTeam.getName().GetCString()));
						}
						else
						{
							szBuffer.append(CvWString::format(
									SETCOLR L" (%d%% %s%s war (%d) with %s [%s%s])\n" ENDCOLR,
									TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
									iTeamWarPercentage,
									(aStartWarInfo[eLoopTeam].bVictory4) ? L"**" : L"",
									(aStartWarInfo[eLoopTeam].bLandTarget) ? L"land" : L"sea",
									aStartWarInfo[eLoopTeam].iStartWarValue,
									kLoopTeam.getName().GetCString(),
									(iBestPossibleMaxWarPass == 0) ?
									((aStartWarInfo[eLoopTeam].bMaxWarNearbyPowerRatio) ?
									L"not adjacent" : L"low power") : L"",
									(iBestPossibleMaxWarPass == 1) ?
									((aStartWarInfo[eLoopTeam].bMaxWarNearbyPowerRatio) ?
									L"not land" : L"low power") : L""));
						}
					}
				}
			}
		}
		while (iBestValue > 0);

		// double space if had any war
		if (bHadAny)
			szBuffer.append(NEWLINE);
	}
	{
		// display limited war items, sorting the list
		bool bHadAny = false;
		bool bFirst = true;
		int iLastValue = MAX_INT;
		int iBestValue;
		do
		{
			iBestValue = 0;
			FOR_EACH_ENUM(Team)
			{
				if (aStartWarInfo[eLoopTeam].bValid &&
					aStartWarInfo[eLoopTeam].bPossibleLimitedWar)
				{
					if (aStartWarInfo[eLoopTeam].iStartWarValue > iBestValue &&
						aStartWarInfo[eLoopTeam].iStartWarValue < iLastValue)
					{
						iBestValue = aStartWarInfo[eLoopTeam].iStartWarValue;
					}
				}
			}
			if (iBestValue > 0)
			{
				iLastValue = iBestValue;
				FOR_EACH_ENUM(Team)
				{
					if (aStartWarInfo[eLoopTeam].bValid &&
						aStartWarInfo[eLoopTeam].iStartWarValue == iBestValue)
					{
						if (bFirst)
						{
							float fLimitedWarPercentage = (fOverallWarPercentage *
									(iLimitedWarThreshold + 1)) / iLimitedWarRand;
							szBuffer.append(CvWString::format(
									SETCOLR L"%.2f%% Limited War:\n" ENDCOLR,
									TEXT_COLOR("COLOR_UNIT_TEXT"), fLimitedWarPercentage));
							bFirst = false;
						}

						bHadAny = true;

						int iNoWarChance = std::max(0,
								aStartWarInfo[eLoopTeam].iNoWarAttitudeProb +
								10 - (bAggressive ? 10 : 0) -
								(bFinancesProLimitedWar ? 10 : 0));
						int iTeamWarPercentage = (100 - iNoWarChance);

						szBuffer.append(CvWString::format(
							SETCOLR L" %d%% %s%s war (%d) with %s\n" ENDCOLR,
							TEXT_COLOR("COLOR_ALT_HIGHLIGHT_TEXT"),
							iTeamWarPercentage,
							(aStartWarInfo[eLoopTeam].bVictory4) ? L"**" : L"",
							(aStartWarInfo[eLoopTeam].bLandTarget) ? L"land" : L"sea",
							aStartWarInfo[eLoopTeam].iStartWarValue,
							GET_TEAM(eLoopTeam).getName().GetCString()));
					}
				}
			}
		}
		while (iBestValue > 0);
		if (bHadAny)
			szBuffer.append(NEWLINE);
	}
	{
		// display dogpile war items, sorting the list
		bool bHadAny = false;
		bool bFirst = true;
		int iLastValue = MAX_INT;
		int iBestValue;
		do
		{
			iBestValue = 0;
			FOR_EACH_ENUM(Team)
			{
				if (aStartWarInfo[eLoopTeam].bValid &&
					aStartWarInfo[eLoopTeam].bPossibleDogpileWar)
				{
					if (aStartWarInfo[eLoopTeam].iStartWarValue > iBestValue &&
						aStartWarInfo[eLoopTeam].iStartWarValue < iLastValue)
					{
						iBestValue = aStartWarInfo[eLoopTeam].iStartWarValue;
					}
				}
			}
			if (iBestValue > 0)
			{
				iLastValue = iBestValue;
				FOR_EACH_ENUM(Team)
				{
					if (aStartWarInfo[eLoopTeam].bValid &&
						aStartWarInfo[eLoopTeam].iStartWarValue == iBestValue)
					{
						if (bFirst)
						{
							float fDogpileWarPercentage = (fOverallWarPercentage *
									(iDogpileWarThreshold + 1)) / iDogpileWarRand;
							szBuffer.append(CvWString::format(
									SETCOLR L"%.2f%% Dogpile War:\n" ENDCOLR,
									TEXT_COLOR("COLOR_UNIT_TEXT"), fDogpileWarPercentage));
							bFirst = false;
						}

						bHadAny = true;

						int iNoWarChance = std::max(0,
								aStartWarInfo[eLoopTeam].iNoWarAttitudeProb +
								20 - (bAggressive ? 10 : 0) -
								(bFinancesProDogpileWar ? 10 : 0));
						int iTeamWarPercentage = (100 - iNoWarChance);

						if (aStartWarInfo[eLoopTeam].bEnoughDogpilePower)
						{
							if (aStartWarInfo[eLoopTeam].bLandTarget ||
								aStartWarInfo[eLoopTeam].bVictory4)
							{
								szBuffer.append(CvWString::format(
									SETCOLR L" %d%% %s%s war (%d) with %s\n" ENDCOLR,
									TEXT_COLOR("COLOR_ALT_HIGHLIGHT_TEXT"),
									iTeamWarPercentage,
									(aStartWarInfo[eLoopTeam].bVictory4) ? L"**" : L"",
									L"land",
									aStartWarInfo[eLoopTeam].iStartWarValue,
									GET_TEAM(eLoopTeam).getName().GetCString()));
							}
							else
							{
								szBuffer.append(CvWString::format(
										SETCOLR L" %d%% %s%s war (%d) with %s\n" ENDCOLR,
										TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
										iTeamWarPercentage,
										(aStartWarInfo[eLoopTeam].bVictory4) ? L"**" : L"",
										L"sea",
										aStartWarInfo[eLoopTeam].iStartWarValue,
										GET_TEAM(eLoopTeam).getName().GetCString()));
							}
						}
						else
						{
							szBuffer.append(CvWString::format(
									SETCOLR L" Lack power for %s%s war (%d) with %s\n" ENDCOLR,
									TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
									(aStartWarInfo[eLoopTeam].bVictory4) ? L"**" : L"",
									(aStartWarInfo[eLoopTeam].bLandTarget) ? L"land" : L"sea",
									aStartWarInfo[eLoopTeam].iStartWarValue,
									GET_TEAM(eLoopTeam).getName().GetCString()));
						}
					}
				}
			}
		}
		while (iBestValue > 0);
		if (bHadAny)
			szBuffer.append(NEWLINE);
	}
	if (GC.shiftKey())
		return;
}

// advc.003j (comment): unused
void CvDLLWidgetData::parseConvertHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
	{
		if (widgetDataStruct.m_iData1 == NO_RELIGION)
			szBuffer.assign(gDLL->getText("TXT_KEY_MISC_NO_STATE_REL"));
		else
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_CONVERT_TO_REL",
					GC.getInfo((ReligionTypes) widgetDataStruct.m_iData1).getTextKeyWide()));
		}
	}
	else
	{
		GAMETEXT.setConvertHelp(szBuffer, getActivePlayer(),
				(ReligionTypes)widgetDataStruct.m_iData1);
	}
}

// advc.003j (comment): unused
void CvDLLWidgetData::parseRevolutionHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData1 != 0)
		szBuffer.assign(gDLL->getText("TXT_KEY_MISC_CHANGE_CIVICS"));
	else GAMETEXT.setRevolutionHelp(szBuffer, getActivePlayer());
}

/*void CvDLLWidgetData::parsePopupQueue(CvWidgetDataStruct &widgetDataStruct, CvWString &szBuffer) {
	PopupEventTypes eEvent;
	if (m_pPopup || m_pScreen) {
		if (m_pPopup)
			eEvent = m_pPopup->getPopupType();
		else if (m_pScreen)
			eEvent = m_pScreen->getPopupType();
		switch (eEvent) {
			case POPUPEVENT_NONE:
				szBuffer = gDLL->getText("TXT_KEY_MISC_NO_MOUSEOVER_TEXT");
				break;

			case POPUPEVENT_PRODUCTION:
				szBuffer = gDLL->getText("TXT_KEY_MISC_PRODUCTION_COMPLETE");
				break;

			case POPUPEVENT_TECHNOLOGY:
				szBuffer = gDLL->getText("TXT_KEY_MISC_TECH_RESEARCH_COMPLETE");
				break;

			case POPUPEVENT_RELIGION:
				szBuffer = gDLL->getText("TXT_KEY_MISC_NEW_REL_DISCOVERED");
				break;

			case POPUPEVENT_WARNING:
				szBuffer = gDLL->getText("TXT_KEY_MISC_WARNING");
				break;

			case POPUPEVENT_CIVIC:
				szBuffer = gDLL->getText("TXT_KEY_MISC_NEW_CIVIC_ACCESSIBLE");
				break;
		}
	}
}*/

void CvDLLWidgetData::parseAutomateCitizensHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity = gDLL->UI().getHeadSelectedCity();
	if (pHeadSelectedCity != NULL)
	{
		if (pHeadSelectedCity->isCitizensAutomated())
			szBuffer.assign(gDLL->getText("TXT_KEY_MISC_OFF_CITIZEN_AUTO"));
		else szBuffer.assign(gDLL->getText("TXT_KEY_MISC_ON_CITIZEN_AUTO"));
	}
}

void CvDLLWidgetData::parseAutomateProductionHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity = gDLL->UI().getHeadSelectedCity();
	if (pHeadSelectedCity != NULL)
	{
		if (pHeadSelectedCity->isProductionAutomated())
			szBuffer.assign(gDLL->getText("TXT_KEY_MISC_OFF_PROD_AUTO"));
		else szBuffer.assign(gDLL->getText("TXT_KEY_MISC_ON_PROD_AUTO"));
	}
}

void CvDLLWidgetData::parseEmphasizeHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	szBuffer.clear();

	CvCity* pHeadSelectedCity = gDLL->UI().getHeadSelectedCity();
	if (pHeadSelectedCity != NULL)
	{
		if (pHeadSelectedCity->AI().AI_isEmphasize((EmphasizeTypes)
			widgetDataStruct.m_iData1))
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_TURN_OFF"));
		}
		else szBuffer.append(gDLL->getText("TXT_KEY_MISC_TURN_ON"));
	}

	szBuffer.append(GC.getInfo((EmphasizeTypes)widgetDataStruct.m_iData1).getDescription());
}


void CvDLLWidgetData::parseTradeItem(CvWidgetDataStruct &widgetDataStruct,
	CvWStringBuffer &szBuffer)
{
	szBuffer.clear();
	CvGame& kGame = GC.getGame();
	PlayerTypes eWhoFrom = getActivePlayer();
	PlayerTypes eWhoTo = NO_PLAYER;
	if (gDLL->isDiplomacy())
		eWhoTo = (PlayerTypes)gDLL->getDiplomacyPlayer();
	else if (gDLL->isMPDiplomacyScreenUp())
		eWhoTo = (PlayerTypes)gDLL->getMPDiplomacyPlayer();
	// <advc> Simplified
	if (eWhoFrom == NO_PLAYER || eWhoTo == NO_PLAYER)
		return;
	bool const bToActivePlayer = widgetDataStruct.m_bOption;
	if (bToActivePlayer)
		std::swap(eWhoTo, eWhoFrom); // </advc>
	TradeableItems const eItemType = (TradeableItems)widgetDataStruct.m_iData1;
	switch (eItemType)
	{
	case TRADE_TECHNOLOGIES:
		GAMETEXT.setTechHelp(szBuffer, (TechTypes)widgetDataStruct.m_iData2);
		break;
	case TRADE_RESOURCES:
		GAMETEXT.setBonusHelp(szBuffer, (BonusTypes)widgetDataStruct.m_iData2);
		break;
	case TRADE_CITIES:
	{	// <advc.ctr>
		CvCity const* pCity = GET_PLAYER(eWhoFrom).getCity(widgetDataStruct.m_iData2);
		if (pCity != NULL)
			GAMETEXT.setCityTradeHelp(szBuffer, *pCity, eWhoTo, false, false);
		else // </advc.ctr>
			szBuffer.assign(gDLL->getText("TXT_KEY_TRADE_CITIES"));
		break;
	}
	case TRADE_PEACE:
		szBuffer.append(gDLL->getText("TXT_KEY_TRADE_MAKE_PEACE",
				GET_TEAM(eWhoFrom).getName().GetCString(),
				GET_TEAM((TeamTypes)widgetDataStruct.m_iData2).getName().GetCString()));
		break;
	case TRADE_WAR:
		szBuffer.append(gDLL->getText("TXT_KEY_TRADE_MAKE_WAR",
				GET_TEAM(eWhoFrom).getName().GetCString(),
				GET_TEAM((TeamTypes)widgetDataStruct.m_iData2).getName().GetCString()));
		break;
	case TRADE_EMBARGO:
		szBuffer.append(gDLL->getText("TXT_KEY_TRADE_STOP_TRADING",
				GET_TEAM(eWhoFrom).getName().GetCString(),
				GET_TEAM((TeamTypes)widgetDataStruct.m_iData2).getName().GetCString()));
		break;
	case TRADE_CIVIC:
		szBuffer.append(gDLL->getText("TXT_KEY_TRADE_ADOPT_CIVIC",
				GC.getInfo((CivicTypes)widgetDataStruct.m_iData2).
				getDescription()));
		break;
	case TRADE_RELIGION:
		szBuffer.append(gDLL->getText("TXT_KEY_TRADE_CONVERT_RELIGION",
				GC.getInfo((ReligionTypes)widgetDataStruct.m_iData2).
				getDescription()));
		break;
	case TRADE_GOLD:
		szBuffer.append(gDLL->getText("TXT_KEY_TRADE_GOLD"));
		break;
	case TRADE_GOLD_PER_TURN:
		szBuffer.append(gDLL->getText("TXT_KEY_TRADE_GOLD_PER_TURN"));
		break;
	case TRADE_MAPS:
		szBuffer.append(gDLL->getText("TXT_KEY_TRADE_MAPS"));
		break;
	// BETTER_BTS_AI_MOD, Diplomacy, 12/07/09, jdog5000: START
	case TRADE_SURRENDER:
		szBuffer.append(gDLL->getText("TXT_KEY_TRADE_CAPITULATE"));
		break;
	case TRADE_VASSAL:
		szBuffer.append(gDLL->getText("TXT_KEY_TRADE_VASSAL"));
		break;
	// BETTER_BTS_AI_MOD: END
	case TRADE_OPEN_BORDERS:
		szBuffer.append(gDLL->getText("TXT_KEY_TRADE_OPEN_BORDERS"));
		break;
	case TRADE_DEFENSIVE_PACT:
		szBuffer.append(gDLL->getText("TXT_KEY_TRADE_DEFENSIVE_PACT"));
		break;
	case TRADE_PERMANENT_ALLIANCE:
		szBuffer.append(gDLL->getText("TXT_KEY_TRADE_PERMANENT_ALLIANCE"));
		break;
	case TRADE_PEACE_TREATY:
		szBuffer.append(gDLL->getText("TXT_KEY_TRADE_PEACE_TREATY",
				GC.getDefineINT(CvGlobals::PEACE_TREATY_LENGTH)));
	    break;
    // doc (edead): slave trade
	case TRADE_SLAVE:
	{
		CvUnit* pUnit = GET_PLAYER(eWhoFrom).getUnit(widgetDataStruct.m_iData2);
		GAMETEXT.setUnitHelp(szBuffer, pUnit, true);
		break;
	}
	// <advc.034>
	case TRADE_DISENGAGE:
		szBuffer.append(gDLL->getText("TXT_KEY_TRADE_DISENGAGE"));
		break; // </advc.034>
	}
	CvWString szTempBuffer;
	// <advc.072>
	if (CvDeal::isAnnual(eItemType) || eItemType == TRADE_PEACE_TREATY)
	{
		CvDeal* pDeal = kGame.nextCurrentDeal(eWhoFrom, eWhoTo, eItemType,
				widgetDataStruct.m_iData2, true);
		if (pDeal != NULL)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(NEWLINE);
			CvWString szReason;
			if (pDeal->isCancelable(getActivePlayer(), &szReason))
			{
				szTempBuffer.Format(SETCOLR L"%s" ENDCOLR,
						TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
						gDLL->getText("TXT_KEY_MISC_CLICK_TO_CANCEL").GetCString());
				szBuffer.append(szTempBuffer);
			}
			else szBuffer.append(szReason);
			szBuffer.append(L":");
			szBuffer.append(NEWLINE);
			if (eItemType == TRADE_PEACE_TREATY) // Don't want the duration in parentheses here
				szBuffer.append(gDLL->getText("TXT_KEY_TRADE_PEACE_TREATY_STR"));
			else GAMETEXT.getDealString(szBuffer, *pDeal, getActivePlayer());
			return; // No denial info
		}
	} // </advc.072>
	/*  advc.104l: Can't easily move this code elsewhere b/c the cache should
		only be used when TradeDenial is checked by this class. */
	WarEvaluator::enableCache();
	DenialTypes eDenial = GET_PLAYER(eWhoFrom).getTradeDenial(eWhoTo, TradeData(
			(TradeableItems)widgetDataStruct.m_iData1, widgetDataStruct.m_iData2));
	WarEvaluator::disableCache(); // advc.104l
	if (eDenial == NO_DENIAL)
		return;
	// <advc> Moved out of the switch block above
	PlayerTypes eWhoDenies = eWhoFrom;
	if (!bToActivePlayer)
	{
		switch (eItemType)
		{
		case TRADE_TECHNOLOGIES:
		case TRADE_RESOURCES:
		case TRADE_CITIES:
			eWhoDenies = eWhoTo;
			break;
		// BETTER_BTS_AI_MOD, Diplomacy, 12/07/09, jdog5000: START
		case TRADE_SURRENDER:
		case TRADE_VASSAL:
			eWhoDenies = NO_PLAYER;
			break;
		case TRADE_SLAVE:
			eWhoDenies = widgetDataStruct.m_bOption ? eWhoFrom : eWhoTo;
			break;
		// BETTER_BTS_AI_MOD: END
		}
	} // </advc>
	// BETTER_BTS_AI_MOD, Diplomacy, 12/07/09, jdog5000: START
	if (eWhoDenies == NO_PLAYER)
	{
		switch(eDenial)
		{
		case DENIAL_POWER_US:
			eDenial = DENIAL_POWER_YOU;
			break;
		case DENIAL_POWER_YOU:
			eDenial = DENIAL_POWER_US;
			break;
		case DENIAL_WAR_NOT_POSSIBLE_US:
			eDenial = DENIAL_WAR_NOT_POSSIBLE_YOU;
			break;
		case DENIAL_WAR_NOT_POSSIBLE_YOU:
			eDenial = DENIAL_WAR_NOT_POSSIBLE_US;
			break;
		case DENIAL_PEACE_NOT_POSSIBLE_US:
			eDenial = DENIAL_PEACE_NOT_POSSIBLE_YOU;
			break;
		case DENIAL_PEACE_NOT_POSSIBLE_YOU:
			eDenial = DENIAL_PEACE_NOT_POSSIBLE_US;
			break;
		default :
			break;
		}
		szTempBuffer.Format(L"%s: " SETCOLR L"%s" ENDCOLR,
				GET_PLAYER(eWhoTo).getName(),
				TEXT_COLOR("COLOR_WARNING_TEXT"),
				GC.getInfo(eDenial).getDescription());
	}
	else
	{
		szTempBuffer.Format(L"%s: " SETCOLR L"%s" ENDCOLR,
				GET_PLAYER(eWhoDenies).getName(),
				TEXT_COLOR("COLOR_WARNING_TEXT"),
				GC.getInfo(eDenial).getDescription());
	}
	// BETTER_BTS_AI_MOD: END
	szBuffer.append(NEWLINE);
	szBuffer.append(szTempBuffer);
}


void CvDLLWidgetData::parseUnitModelHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvUnit* pHeadSelectedUnit = gDLL->UI().getHeadSelectedUnit();
	if (pHeadSelectedUnit != NULL)
		GAMETEXT.setUnitHelp(szBuffer, pHeadSelectedUnit);
}


void CvDLLWidgetData::parseFlagHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvWString szTempBuffer;
	// <advc.135c>
	CvGame const& kGame = GC.getGame();
	if (kGame.isNetworkMultiPlayer() && kGame.isDebugToolsAllowed(false))
	{
		szTempBuffer.Format(SETCOLR L"%s" ENDCOLR, TEXT_COLOR("COLOR_WARNING_TEXT"),
				L"Cheats enabled");
		szBuffer.append(szTempBuffer);
		szBuffer.append(NEWLINE);
	} // </advc.135c>
	CvPlayer const& kActivePlayer = GET_PLAYER(getActivePlayer());
	szTempBuffer.Format(SETCOLR L"%s" ENDCOLR, TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
			GC.getInfo(kActivePlayer.getCivilizationType()).getDescription());
	szBuffer.append(szTempBuffer);
	// <advc.700>
	if (kGame.isOption(GAMEOPTION_RISE_FALL))
	{
		std::pair<int,int> iiCountdown = kGame.getRiseFall().getChapterCountdown();
		if(iiCountdown.second >= 0)
			szBuffer.append(L" (" + gDLL->getText("TXT_KEY_RF_CHAPTER_COUNTDOWN",
					iiCountdown.first, iiCountdown.second) + L")");
	} // </advc.700>
	szBuffer.append(NEWLINE);


	GAMETEXT.parseLeaderTraits(szBuffer, kActivePlayer.getLeaderType(),
			kActivePlayer.getCivilizationType());

	// <advc.027b> (Might be nicer to show this on the Settings tab, but - too much hassle.)
	if (kGame.isDebugMode() && GC.ctrlKey())
	{
		uint uiMapRandSeed = kGame.getInitialRandSeed().first;
		uint uiSyncRandSeed = kGame.getInitialRandSeed().second;
		if (uiMapRandSeed != 0 || uiSyncRandSeed != 0)
		{
			szBuffer.append(NEWLINE);
			if (uiMapRandSeed != 0)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(CvWString::format(L"Map rand seed: %u", uiMapRandSeed));
			}
			if (uiSyncRandSeed != 0)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(CvWString::format(L"Sync rand seed: %u", uiSyncRandSeed));
			}
		}
	} // </advc.027b>
}


void CvDLLWidgetData::parseMaintenanceHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity = gDLL->UI().getHeadSelectedCity();
	if (pHeadSelectedCity == NULL)
		return;

	if (pHeadSelectedCity->isWeLoveTheKingDay())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_WE_LOVE_KING_MAINT"));
		return;
	}

	int iInflationFactor = 100 + GET_PLAYER(pHeadSelectedCity->getOwner()).calculateInflationRate(); // K-Mod

	szBuffer.assign(gDLL->getText("TXT_KEY_MISC_MAINT_INFO"));
	szBuffer.append(NEWLINE);

	int iMaintenanceValue = (pHeadSelectedCity->calculateDistanceMaintenanceTimes100() *
			iInflationFactor) / 100; // K-Mod
	if (iMaintenanceValue != 0)
	{
		CvWString szMaint = CvWString::format(L"%d.%02d",
				iMaintenanceValue/100, iMaintenanceValue%100);
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_NUM_MAINT_FLOAT", szMaint.GetCString()) +
				(GET_PLAYER(pHeadSelectedCity->getOwner()).getNumGovernmentCenters() > 0 ?
				gDLL->getText("TXT_KEY_MISC_DISTANCE_FROM_PALACE") :
				gDLL->getText("TXT_KEY_MISC_NO_PALACE_PENALTY")));
	}

	iMaintenanceValue = (pHeadSelectedCity->calculateNumCitiesMaintenanceTimes100() *
			iInflationFactor) / 100; // K-Mod
	if (iMaintenanceValue != 0)
	{
		CvWString szMaint = CvWString::format(L"%d.%02d",
				iMaintenanceValue/100, iMaintenanceValue%100);
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_NUM_CITIES_FLOAT",
				szMaint.GetCString()));
	}

	iMaintenanceValue = (pHeadSelectedCity->calculateColonyMaintenanceTimes100() *
			iInflationFactor) / 100; // K-Mod
	if (iMaintenanceValue != 0)
	{
		CvWString szMaint = CvWString::format(L"%d.%02d",
				iMaintenanceValue/100, iMaintenanceValue%100);
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_COLONY_MAINT_FLOAT",
				szMaint.GetCString()));
	}

	iMaintenanceValue = (pHeadSelectedCity->calculateCorporationMaintenanceTimes100() *
			iInflationFactor) / 100; // K-Mod
	if (iMaintenanceValue != 0)
	{
		CvWString szMaint = CvWString::format(L"%d.%02d",
				iMaintenanceValue/100, iMaintenanceValue%100);
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_CORPORATION_MAINT_FLOAT",
				szMaint.GetCString()));
	}

	szBuffer.append(SEPARATOR);

	iMaintenanceValue = (pHeadSelectedCity->getMaintenanceTimes100() *
			iInflationFactor) / 100; // K-Mod
	CvWString szMaint = CvWString::format(L"%d.%02d",
			iMaintenanceValue/100, iMaintenanceValue%100);
	szBuffer.append(NEWLINE);
	szBuffer.append(gDLL->getText("TXT_KEY_MISC_TOTAL_MAINT_FLOAT", szMaint.GetCString()));

	iMaintenanceValue = pHeadSelectedCity->getMaintenanceModifier();

	if (iMaintenanceValue != 0)
	{
		wchar szTempBuffer[1024];
		swprintf(szTempBuffer, L" (%s%d%%)", iMaintenanceValue > 0 ? L"+" : L"",
				iMaintenanceValue);
		szBuffer.append(szTempBuffer);
	}

	// BUG - Building Saved Maintenance - start
	if (pHeadSelectedCity->isActiveOwned() &&
		(BUGOption::isEnabled("MiscHover__BuildingSavedMaintenance", false) ||
		GC.altKey())) // advc.063
	{
		GAMETEXT.setBuildingSavedMaintenanceHelp(szBuffer,
				*pHeadSelectedCity, DOUBLE_SEPARATOR);
	} // BUG - Building Saved Maintenance - end
}


void CvDLLWidgetData::parseHealthHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity = gDLL->UI().getHeadSelectedCity();
	if (pHeadSelectedCity == NULL)
		return; // advc

	GAMETEXT.setBadHealthHelp(szBuffer, *pHeadSelectedCity);
	szBuffer.append(L"\n=======================\n");
	GAMETEXT.setGoodHealthHelp(szBuffer, *pHeadSelectedCity);

	// BUG - Building Additional Health - start
	if (pHeadSelectedCity->isActiveOwned() &&
		(BUGOption::isEnabled("MiscHover__BuildingAdditionalHealth", false) ||
		GC.altKey())) // advc.063
	{
		GAMETEXT.setBuildingAdditionalHealthHelp(szBuffer, *pHeadSelectedCity, DOUBLE_SEPARATOR);
	} // BUG - Building Additional Health - end
}


void CvDLLWidgetData::parseNationalityHelp(CvWidgetDataStruct &widgetDataStruct,
	CvWStringBuffer &szBuffer)
{
	wchar szTempBuffer[1024];

	szBuffer.assign(gDLL->getText("TXT_KEY_MISC_CITY_NATIONALITY"));
	CvCity* pHeadSelectedCity = gDLL->UI().getHeadSelectedCity();
	if (pHeadSelectedCity == NULL)
		return;
	CvCity const& c = *pHeadSelectedCity;
    // doc: capture all civilizations: from alive players and dead civilizations
	// TODO: not just alive
	/*  <advc.099> Replaced "Alive" with "EverAlive", and sorted to match the
		order in updateCityScreen (CvMainInterface.py) */
	std::vector<std::pair<int,PlayerTypes> > aieSorted;
    std::vector<std::pair<int,CivilizationTypes> > aieCivsSorted;
    // doc: only alive - we capture other one on the civilization level
	for (PlayerIter<ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		PlayerTypes const ePlayer = itPlayer->getID();
		int iCulturePercent = c.calculateCulturePercent(itPlayer->getCivilizationType()); // doc: city culture
		if(iCulturePercent > 0)
			aieSorted.push_back(std::pair<int,PlayerTypes>(iCulturePercent, ePlayer));
	}
	std::sort(aieSorted.begin(), aieSorted.end());
	std::reverse(aieSorted.begin(), aieSorted.end());
	for (size_t i = 0; i < aieSorted.size(); i++)
	{
		CvPlayer const& kPlayer = GET_PLAYER(aieSorted[i].second);
		int iCulturePercent = aieSorted[i].first; // </advc.099>
		swprintf(szTempBuffer, L"\n%d%% " SETCOLR L"%s" ENDCOLR,
				iCulturePercent, PLAYER_TEXT_COLOR(kPlayer),
				kPlayer.getCivilizationAdjective());
		szBuffer.append(szTempBuffer);
	}

    // doc: civilizations
    FOR_EACH_ENUM(Civilization)
    {
        if (!isCivAlive(eLoopCivilization))
        {
            int iCulturePercent = c.calculateCulturePercent(eLoopCivilization); // doc: city culture
            if (iCulturePercent > 0)
                aieCivsSorted.push_back(std::pair<int,CivilizationTypes>(iCulturePercent, eLoopCivilization));
        }
    }
    std::sort(aieCivsSorted.begin(), aieCivsSorted.end());
    std::reverse(aieCivsSorted.begin(), aieCivsSorted.end());
    for (size_t i = 0; i < aieCivsSorted.size(); i++)
    {
        CvCivilizationInfo& kCivilization = GC.getInfo(aieCivsSorted[i].second);
        int iCulturePercent = aieCivsSorted[i].first;
        PlayerColorTypes ePlayerColor = (PlayerColorTypes)kCivilization.getDefaultPlayerColor();
        swprintf(szTempBuffer, L"\n%d%% " SETCOLR L"%s" ENDCOLR, iCulturePercent, COLORS(GC.getPlayerColorInfo(ePlayerColor).getTextColorType()), kCivilization.getAdjective());
        szBuffer.append(szTempBuffer);
    }

    // doc: stability effects of cultural control
    int iOwnCulturePercent = c.calculateCulturePercent(c.getOwner());
    if (c.getCivilizationType() != PERSIA) // doc: not with Persian UP // TODO: still true?
    {
        if (iOwnCulturePercent < 20)
        {
            szBuffer.append(NEWLINE);
            szBuffer.append(gDLL->getText("TXT_KEY_INTERFACE_HIGH_INSTABILITY_CULTURE"));
        }
        else if (iOwnCulturePercent < 50)
        {
            szBuffer.append(NEWLINE);
            szBuffer.append(gDLL->getText("TXT_KEY_INTERFACE_INSTABILITY_CULTURE"));
        }
    }

	PlayerTypes const eCulturalOwner = c.calculateCulturalOwner(); // advc.099c
	// <advc.101> (Akin to code in CvGameTextMgr::setCityBarHelp)
	std::vector<CvCity::GrievanceTypes> aeGrievances;
	// <advc.023>
	scaled const rDecrementProb = c.probabilityOccupationDecrement();
	scaled const rHypotheticalProb = c.revoltProbability(true, false, true);
	int const iCultureStr = c.cultureStrength(eCulturalOwner, false, false,
			&aeGrievances);
	int const iGarrisonStr = c.cultureGarrison(eCulturalOwner);
	scaled const rTrueProb = c.revoltProbability() * (1 - rDecrementProb);
	if (rHypotheticalProb > 0)
	{
		swprintf(szTempBuffer, (rTrueProb == 0 ? L"%.0f" : L"%.1f"),
				100 * rTrueProb.getFloat()); // </advc.023>
		// </advc.101>
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_CHANCE_OF_REVOLT", szTempBuffer));
		/*	<advc.023> Probability after occupation and war. (If only either ends,
			a third probability may apply, but I don't to bother showing that.) */
		if (rTrueProb != rHypotheticalProb)
		{
			szBuffer.append(NEWLINE);
			swprintf(szTempBuffer, L"%.1f", 100 * rHypotheticalProb.getFloat());
			CvWString szKey;
			if (c.isMartialLaw(eCulturalOwner) && c.isOccupation())
				szKey = "TXT_KEY_REVOLT_CHANCE_AFTER_WAR_OCCUPATION";
			else if (c.isMartialLaw(eCulturalOwner))
				szKey = "TXT_KEY_REVOLT_CHANCE_AFTER_WAR";
			else szKey = "TXT_KEY_REVOLT_CHANCE_AFTER_OCCUPATION";
			szBuffer.append(gDLL->getText(szKey, szTempBuffer));
		} // </advc.023>
		// <advc.101>
		szBuffer.append(NEWLINE);
		// Partial breakdown of the probability - not so helpful after all
		/*int const iCultureStrength = c.cultureStrength(eCulturalOwner);
		szBuffer.append(gDLL->getText("TXT_KEY_REVOLT_PR_BREAKDOWN",
				c.cultureGarrison(eCulturalOwner),
				// Can't break this down further - too complicated
				iCultureStrength, iCultureStrength,
				::round(100 * c.getRevoltTestProbability())));
		// Also show c.getRevoltProtection()? */
		if (iCultureStr > iGarrisonStr)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_GARRISON_STRENGTH_NEEDED",
					iCultureStr - iGarrisonStr));
		}
	}
	if (!c.isOccupation() && rHypotheticalProb <= 0 &&
		eCulturalOwner != c.getOwner() && iGarrisonStr >= iCultureStr)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_GARRISON_STRENGTH_EXCESS",
				std::min(999, iGarrisonStr - iCultureStr)));
	}
	if (eCulturalOwner != c.getOwner())
	{
		for (size_t i = 0; i < aeGrievances.size(); i++)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_INCREASED_BY_GRIEVANCE"));
			szBuffer.append(L" ");
			CvWString szGrievanceKey(L"TXT_KEY_GRIEVANCE_");
			switch (aeGrievances[i])
			{
			case CvCity::GRIEVANCE_HURRY: szGrievanceKey += L"HURRY"; break;
			case CvCity::GRIEVANCE_CONSCRIPT: szGrievanceKey += L"CONSCRIPT"; break;
			case CvCity::GRIEVANCE_RELIGION: szGrievanceKey += L"RELIGION"; break;
			default: FErrorMsg("Unknown grievance type");
			}
			szBuffer.append(gDLL->getText(szGrievanceKey.GetCString()));
		}
		// Warn about flipping
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_PRIOR_REVOLTS",
				c.getNumRevolts(eCulturalOwner)));
		if (rTrueProb > 0 && c.canCultureFlip(eCulturalOwner))
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_FLIP_WARNING"));
		}
	}
	if (c.isOccupation()) // </advc.101>
	{	// <advc.023>
		// Show probability of decrementing occupation - unless it's always 1
		if (GC.getDefineINT(CvGlobals::OCCUPATION_COUNTDOWN_EXPONENT) > 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_OCCUPATION_TIMER",
					c.getOccupationTimer()));
			szBuffer.append(NEWLINE);
			// Tends to be a high-ish probability, no need for decimal places
			int iDecrementPercent = rDecrementProb.getPercent();
			// But don't claim it's 0% or 100% if it isn't quite
			if (rDecrementProb > 0)
				iDecrementPercent = std::max(1, iDecrementPercent);
			if (rDecrementProb < 1)
				iDecrementPercent = std::min(99, iDecrementPercent);
			szBuffer.append(gDLL->getText("TXT_KEY_TIMER_DECREASE_CHANCE",
					iDecrementPercent));
		}
	} // </advc.023>
}


void CvDLLWidgetData::parseHappinessHelp(CvWidgetDataStruct &widgetDataStruct,
	CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity = gDLL->UI().getHeadSelectedCity();
	if (pHeadSelectedCity == NULL)
		return; // advc

	GAMETEXT.setAngerHelp(szBuffer, *pHeadSelectedCity);
	szBuffer.append(L"\n=======================\n");
	GAMETEXT.setHappyHelp(szBuffer, *pHeadSelectedCity);

	// BUG - Building Additional Happiness - start
	if (pHeadSelectedCity->isActiveOwned() &&
		(BUGOption::isEnabled("MiscHover__BuildingAdditionalHappiness", false) ||
		GC.altKey())) // advc.063
	{
		GAMETEXT.setBuildingAdditionalHappinessHelp(szBuffer,
				*pHeadSelectedCity, DOUBLE_SEPARATOR);
	} // BUG - Building Additional Happiness - end
}


void CvDLLWidgetData::parsePopulationHelp(CvWidgetDataStruct &widgetDataStruct,
	CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity = gDLL->UI().getHeadSelectedCity();
	if (pHeadSelectedCity != NULL)
	{
		szBuffer.assign(gDLL->getText("TXT_KEY_MISC_FOOD_THRESHOLD",
				pHeadSelectedCity->getFood(), pHeadSelectedCity->growthThreshold()));
	}
}


void CvDLLWidgetData::parseProductionHelp(CvWidgetDataStruct &widgetDataStruct,
	CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity = gDLL->UI().getHeadSelectedCity();
	if (pHeadSelectedCity != NULL &&
		pHeadSelectedCity->getProductionNeeded() != MAX_INT)
	{
		CvWString szTemp;
		szTemp.Format(L"%s: %d/%d %c", pHeadSelectedCity->getProductionName(),
				pHeadSelectedCity->getProduction(),
				pHeadSelectedCity->getProductionNeeded(),
				GC.getInfo(YIELD_PRODUCTION).getChar());
		szBuffer.assign(szTemp);
		/*  advc.064 (comment): Would be nice to show some hurry info here,
			if only to explain what the hurry-related icons on the production bar
			mean. However, untangling parseHurryHelp to avoid code duplication
			is too much work, so ... */
	}
}


void CvDLLWidgetData::parseCultureHelp(CvWidgetDataStruct &widgetDataStruct,
	CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity = gDLL->UI().getHeadSelectedCity();
	if (pHeadSelectedCity == NULL)
		return; // advc

    // doc: gradual border expansion
    CulturePlotTypes eNextCoveredPlot = pHeadSelectedCity->getNextCoveredPlot();
    CulturePlotTypes eEffectiveNextCoveredPlot = pHeadSelectedCity->getEffectiveNextCoveredPlot();

	int iThreshold = pHeadSelectedCity->getCultureThreshold();

	int iCultureTimes100 = pHeadSelectedCity->getCultureTimes100(pHeadSelectedCity->getOwner());
	if (iCultureTimes100%100 == 0)
	{
		szBuffer.assign(gDLL->getText("TXT_KEY_MISC_CULTURE", iCultureTimes100/100,
				pHeadSelectedCity->getCultureThreshold()));
	}
	else
	{
		CvWString szCulture = CvWString::format(L"%d.%02d",
				iCultureTimes100/100, iCultureTimes100%100);
		szBuffer.assign(gDLL->getText("TXT_KEY_MISC_CULTURE_FLOAT",
				szCulture.GetCString(), pHeadSelectedCity->getCultureThreshold()));
	}
	// <advc.042> Code moved into subroutine
	int iTurnsLeft = pHeadSelectedCity->getCultureTurnsLeft();
	if (iTurnsLeft > 0)
	{
		szBuffer.append(L' ');
		szBuffer.append(gDLL->getText("INTERFACE_CITY_TURNS", std::max(1, iTurnsLeft)));
	} // </advc.042>

    // doc: culture rank
    int iCultureRank = pHeadSelectedCity->getCultureRank();
    szBuffer.append(NEWLINE);
    szBuffer.append(gDLL->getText("TXT_KEY_CITY_CULTURE_RANK", iCultureRank+1));

    // doc: gradual border expansion
	int iCultureRateTimes100 = pHeadSelectedCity->getModifiedCultureRateTimes100();
    if (eEffectiveNextCoveredPlot < NUM_CULTURE_PLOTS && iCultureRateTimes100 > 0)
    {
        if (eEffectiveNextCoveredPlot >= eNextCoveredPlot) 
			iThreshold = pHeadSelectedCity->getCultureCost(eEffectiveNextCoveredPlot);
        else 
			iThreshold = pHeadSelectedCity->getCultureThreshold();

        int iCultureLeftTimes100 = 100 * iThreshold - iCultureTimes100;
        if (iCultureLeftTimes100 > 0)
        {
            int iTurnsLeft = (iCultureLeftTimes100 + iCultureRateTimes100 - 1) / iCultureRateTimes100;

            szBuffer.append(NEWLINE);
            szBuffer.append(gDLL->getText("TXT_KEY_INTERFACE_CITY_EXPANSION_TURNS", std::max(1, iTurnsLeft)));
        }
    }

	szBuffer.append(L"\n=======================\n");
	GAMETEXT.setCommerceHelp(szBuffer, *pHeadSelectedCity, COMMERCE_CULTURE);
}


// doc: great spy help
void CvDLLWidgetData::parseGreatSpyHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
    if (NO_PLAYER != GC.getGame().getActivePlayer())
    {
        GAMETEXT.parseGreatSpyHelp(szBuffer, GET_PLAYER(GC.getGame().getActivePlayer()));
    }
}


void CvDLLWidgetData::parseGreatPeopleHelp(CvWidgetDataStruct &widgetDataStruct,
	CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity = gDLL->UI().getHeadSelectedCity();
	if (pHeadSelectedCity != NULL)
		GAMETEXT.parseGreatPeopleHelp(szBuffer, *pHeadSelectedCity);
}


void CvDLLWidgetData::parseGreatGeneralHelp(CvWidgetDataStruct &widgetDataStruct,
	CvWStringBuffer &szBuffer)
{
	if (getActivePlayer() != NO_PLAYER)
		GAMETEXT.parseGreatGeneralHelp(szBuffer, GET_PLAYER(getActivePlayer()));
}


void CvDLLWidgetData::parseSelectedHelp(CvWidgetDataStruct &widgetDataStruct,
	CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity = gDLL->UI().getHeadSelectedCity();
	if (pHeadSelectedCity == NULL)
		return;

	OrderData* pOrder = pHeadSelectedCity->getOrderFromQueue(widgetDataStruct.m_iData1);
	if (pOrder == NULL)
		return;

	switch (pOrder->eOrderType)
	{
	case ORDER_TRAIN:
		GAMETEXT.setUnitHelp(szBuffer, (UnitTypes)pOrder->iData1,
				false, false, false, pHeadSelectedCity);
		break;

	case ORDER_CONSTRUCT:
		GAMETEXT.setBuildingHelpActual( // BUG - Building Actual Effects (was setBuildingHelp)
				szBuffer, (BuildingTypes)pOrder->iData1, false, false, false, pHeadSelectedCity);
		break;

	case ORDER_CREATE:
		GAMETEXT.setProjectHelp(szBuffer, (ProjectTypes)pOrder->iData1, false, pHeadSelectedCity);
		break;

	case ORDER_MAINTAIN:
		GAMETEXT.setProcessHelp(szBuffer, (ProcessTypes)pOrder->iData1);
		break;

	default:
		FErrorMsg("eOrderType did not match valid options");
		break;
	}
}


void CvDLLWidgetData::parseTradeRouteCityHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
	{
		GAMETEXT.setTradeRouteHelp(szBuffer, widgetDataStruct.m_iData1,
				gDLL->UI().getHeadSelectedCity());
	}
}

void CvDLLWidgetData::parseEspionageCostHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvUnit* pUnit = gDLL->UI().getHeadSelectedUnit();
	if (pUnit != NULL)
	{
		CvPlot* pPlot = pUnit->plot();
		if (NULL != pPlot)
		{
			GAMETEXT.setEspionageCostHelp(szBuffer, (EspionageMissionTypes)
					widgetDataStruct.m_iData1, pPlot->getOwner(), pPlot,
					widgetDataStruct.m_iData2, pUnit);
		}
	}
}

void CvDLLWidgetData::parseBuildingHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
	{
		GAMETEXT.setBuildingHelp(szBuffer, (BuildingTypes)widgetDataStruct.m_iData1,
				false, false, widgetDataStruct.m_bOption, gDLL->UI().getHeadSelectedCity());
	}
}

void CvDLLWidgetData::parseProjectHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
	{
		GAMETEXT.setProjectHelp(szBuffer, (ProjectTypes)widgetDataStruct.m_iData1,
				false, gDLL->UI().getHeadSelectedCity());
	}
}


void CvDLLWidgetData::parseTerrainHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
		GAMETEXT.setTerrainHelp(szBuffer, (TerrainTypes)widgetDataStruct.m_iData1);
}


void CvDLLWidgetData::parseFeatureHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
		GAMETEXT.setFeatureHelp(szBuffer, (FeatureTypes)widgetDataStruct.m_iData1);
}


void CvDLLWidgetData::parseTechEntryHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{	/*  advc.085: 0 was unused, so this check wasn't needed for anything. Now 0
		causes the scoreboard to expand (handled by caller). */
	//if (widgetDataStruct.m_iData2 != 0)
	GAMETEXT.setTechHelp(szBuffer, (TechTypes)widgetDataStruct.m_iData1);
}

// BULL - Trade Denial - start
void CvDLLWidgetData::parseTechTradeEntryHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 == -1)
		parseTechEntryHelp(widgetDataStruct, szBuffer);
	else
	{
		GAMETEXT.setTechTradeHelp(szBuffer, (TechTypes)widgetDataStruct.m_iData1,
				(PlayerTypes)widgetDataStruct.m_iData2);
	}
} // BULL - Trade Denial - end


void CvDLLWidgetData::parseTechPrereqHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	szBuffer.assign(gDLL->getText("TXT_KEY_MISC_TECH_REQUIRES_KNOWLEDGE_OF",
			GC.getInfo((TechTypes)widgetDataStruct.m_iData1).getTextKeyWide()));
}

void CvDLLWidgetData::parseTechTreePrereq(CvWidgetDataStruct &widgetDataStruct,
	CvWStringBuffer &szBuffer, bool bTreeInfo)
{
	GAMETEXT.setTechHelp(szBuffer, (TechTypes)widgetDataStruct.m_iData1, false,
			false, false, bTreeInfo, (TechTypes)widgetDataStruct.m_iData2);
}

// doc: culture level pedia
void CvDLLWidgetData::parseCultureLevelHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	szBuffer.assign(GC.getCultureLevelInfo((CultureLevelTypes)widgetDataStruct.m_iData1).getText());
}

// doc: culture level pedia
void CvDLLWidgetData::parseRouteHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	szBuffer.assign(GC.getRouteInfo((RouteTypes)widgetDataStruct.m_iData1).getText());
}

void CvDLLWidgetData::parseObsoleteHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildObsoleteString(szBuffer, (TechTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseObsoleteBonusString(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildObsoleteBonusString(szBuffer, (BonusTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseObsoleteSpecialHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildObsoleteSpecialString(szBuffer, (TechTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseMoveHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildMoveString(szBuffer, (TechTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseFreeUnitHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildFreeUnitString(szBuffer, (TechTypes)widgetDataStruct.m_iData2);
}

void CvDLLWidgetData::parseFeatureProductionHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildFeatureProductionString(szBuffer, (TechTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseWorkerRateHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildWorkerRateString(szBuffer, (TechTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseTradeRouteHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildTradeRouteString(szBuffer, (TechTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseHealthRateHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildHealthRateString(szBuffer, (TechTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseHappinessRateHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildHappinessRateString(szBuffer, (TechTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseFreeTechHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildFreeTechString(szBuffer, (TechTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseLOSHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildLOSString(szBuffer, (TechTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseMapCenterHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildMapCenterString(szBuffer, (TechTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseMapRevealHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildMapRevealString(szBuffer, (TechTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseMapTradeHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildMapTradeString(szBuffer, (TechTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseTechTradeHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildTechTradeString(szBuffer, (TechTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseGoldTradeHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildGoldTradeString(szBuffer, (TechTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseOpenBordersHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildOpenBordersString(szBuffer, (TechTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseDefensivePactHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildDefensivePactString(szBuffer, (TechTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parsePermanentAllianceHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildPermanentAllianceString(szBuffer, (TechTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseVassalStateHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildVassalStateString(szBuffer, (TechTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseBuildBridgeHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildBridgeString(szBuffer, (TechTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseIrrigationHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildIrrigationString(szBuffer, (TechTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseIgnoreIrrigationHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildIgnoreIrrigationString(szBuffer, (TechTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseWaterWorkHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildWaterWorkString(szBuffer, (TechTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseBuildHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildImprovementString(szBuffer, (TechTypes)widgetDataStruct.m_iData1,
			(BuildTypes)widgetDataStruct.m_iData2);
}

void CvDLLWidgetData::parseDomainExtraMovesHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildDomainExtraMovesString(szBuffer, (TechTypes)widgetDataStruct.m_iData1,
			(DomainTypes)widgetDataStruct.m_iData2);
}

void CvDLLWidgetData::parseAdjustHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildAdjustString(szBuffer, (TechTypes)widgetDataStruct.m_iData1,
			(CommerceTypes)widgetDataStruct.m_iData2);
}

void CvDLLWidgetData::parseTerrainTradeHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 < GC.getNumTerrainInfos())
	{
		GAMETEXT.buildTerrainTradeString(szBuffer, (TechTypes)widgetDataStruct.m_iData1,
				(TerrainTypes)widgetDataStruct.m_iData2);
	}
	else if (widgetDataStruct.m_iData2 == GC.getNumTerrainInfos())
	{
		GAMETEXT.buildRiverTradeString(szBuffer, (TechTypes)widgetDataStruct.m_iData1);
	}
}

void CvDLLWidgetData::parseSpecialBuildingHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildSpecialBuildingString(szBuffer, (TechTypes)widgetDataStruct.m_iData1,
			(SpecialBuildingTypes)widgetDataStruct.m_iData2);
}

void CvDLLWidgetData::parseYieldChangeHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildYieldChangeString(szBuffer, (TechTypes)widgetDataStruct.m_iData1,
			(ImprovementTypes)widgetDataStruct.m_iData2, false);
}

void CvDLLWidgetData::parseBonusRevealHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildBonusRevealString(szBuffer, (TechTypes)widgetDataStruct.m_iData1,
			(BonusTypes)widgetDataStruct.m_iData2, true);
}

// doc: bonus trade help
void CvDLLWidgetData::parseBonusPlayerTradeHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	bool bFirst = true;
	TechTypes eTech = (TechTypes)widgetDataStruct.m_iData1;

	FOR_EACH_ENUM(Bonus)
	{
		if (GC.getInfo(eLoopBonus).getTechPlayerTrade() == eTech)
		{
			bFirst = GAMETEXT.buildBonusTradeString(szBuffer, eTech, eLoopBonus, bFirst, false, true);
		}
	}
}

void CvDLLWidgetData::parseCivicRevealHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	//GAMETEXT.buildCivicRevealString(szBuffer, (TechTypes)widgetDataStruct.m_iData1, (CivicTypes)widgetDataStruct.m_iData2, true);
	// advc.mnai (lfgr UI 11/2020): Show civic help in tech tree
	GAMETEXT.parseSingleCivicRevealHelp(szBuffer, (CivicTypes)widgetDataStruct.m_iData2);
}

void CvDLLWidgetData::parseProcessInfoHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildProcessInfoString(szBuffer, (TechTypes)widgetDataStruct.m_iData1,
			(ProcessTypes)widgetDataStruct.m_iData2, true);
}

void CvDLLWidgetData::parseFoundReligionHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildFoundReligionString(szBuffer, (TechTypes)widgetDataStruct.m_iData1,
			(ReligionTypes)widgetDataStruct.m_iData2, true);
}

void CvDLLWidgetData::parseFoundCorporationHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildFoundCorporationString(szBuffer, (TechTypes)widgetDataStruct.m_iData1,
			(CorporationTypes)widgetDataStruct.m_iData2, true);
}

void CvDLLWidgetData::parseFinanceNumUnits(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{	// advc.086: Disabled (noninformative)
	//szBuffer.assign(gDLL->getText("TXT_KEY_ECON_NUM_UNITS_SUPPORTING"));
}

void CvDLLWidgetData::parseFinanceUnitCost(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{	// advc.086: Disabled
	//szBuffer.assign(gDLL->getText("TXT_KEY_ECON_MONEY_SPENT_UPKEEP"));
	if (widgetDataStruct.m_iData2 > 0)
		GAMETEXT.buildFinanceUnitCostString(szBuffer, (PlayerTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseFinanceAwaySupply(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	szBuffer.assign(gDLL->getText("TXT_KEY_ECON_AMOUNT_MONEY_UNITS_ENEMY_TERRITORY"));
	if (widgetDataStruct.m_iData2 > 0)
		GAMETEXT.buildFinanceAwaySupplyString(szBuffer, (PlayerTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseFinanceCityMaint(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{	// advc.086: Disabled
	//szBuffer.assign(gDLL->getText("TXT_KEY_ECON_AMOUNT_MONEY_CITY_MAINT"));
	if (widgetDataStruct.m_iData2 > 0)
		GAMETEXT.buildFinanceCityMaintString(szBuffer, (PlayerTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseFinanceCivicUpkeep(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{	// advc.086: Disabled
	//szBuffer.assign(gDLL->getText("TXT_KEY_ECON_AMOUNT_MONEY_CIVIC_UPKEEP"));
	if (widgetDataStruct.m_iData2 > 0)
		GAMETEXT.buildFinanceCivicUpkeepString(szBuffer, (PlayerTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseFinanceForeignIncome(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	szBuffer.assign(gDLL->getText("TXT_KEY_ECON_AMOUNT_MONEY_FOREIGN"));
	if (widgetDataStruct.m_iData2 > 0)
		GAMETEXT.buildFinanceForeignIncomeString(szBuffer, (PlayerTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseFinanceInflatedCosts(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{	// advc (comment): Unused b/c of K-Mod changes to EconomicsAdvisor.py
	szBuffer.assign(gDLL->getText("TXT_KEY_ECON_AMOUNT_MONEY_AFTER_INFLATION"));
	if (widgetDataStruct.m_iData2 > 0)
		GAMETEXT.buildFinanceInflationString(szBuffer, (PlayerTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseFinanceGrossIncome(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	szBuffer.assign(gDLL->getText("TXT_KEY_ECON_GROSS_INCOME"));
}

void CvDLLWidgetData::parseFinanceNetGold(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	szBuffer.assign(gDLL->getText("TXT_KEY_ECON_NET_GOLD"));
}

void CvDLLWidgetData::parseFinanceGoldReserve(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	szBuffer.assign(gDLL->getText("TXT_KEY_ECON_GOLD_RESERVE"));
}
// BULL - Finance Advisor - start
void CvDLLWidgetData::parseFinanceDomesticTrade(CvWidgetDataStruct& widgetDataStruct, CvWStringBuffer& szBuffer)
{
	if(widgetDataStruct.m_iData2 > 0) // advc.086: Heading moved into CvGameTextMgr
		GAMETEXT.buildDomesticTradeString(szBuffer, (PlayerTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseFinanceForeignTrade(CvWidgetDataStruct& widgetDataStruct, CvWStringBuffer& szBuffer)
{
	if(widgetDataStruct.m_iData2 > 0)  // advc.086: Heading moved into CvGameTextMgr
		GAMETEXT.buildForeignTradeString(szBuffer, (PlayerTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseFinanceSpecialistGold(CvWidgetDataStruct& widgetDataStruct, CvWStringBuffer& szBuffer)
{
	// advc.086: No heading
	//szBuffer.assign(gDLL->getText("TXT_KEY_BUG_FINANCIAL_ADVISOR_SPECIALISTS"));
	//szBuffer.append(NEWLINE);
	if(widgetDataStruct.m_iData2 > 0)
		GAMETEXT.buildFinanceSpecialistGoldString(szBuffer, (PlayerTypes)widgetDataStruct.m_iData1);
} // BULL - Finance Advisor - end

void CvDLLWidgetData::parseUnitHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
	{
		GAMETEXT.setUnitHelp(szBuffer, (UnitTypes)widgetDataStruct.m_iData1, false, false,
				widgetDataStruct.m_bOption, gDLL->UI().getHeadSelectedCity());
	}
}

void CvDLLWidgetData::parsePediaBack(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
//	szBuffer = "Back";
	szBuffer.assign(gDLL->getText("TXT_KEY_MISC_PEDIA_BACK"));
}
// advc.003j (comment): Both unused
void CvDLLWidgetData::parsePediaForward(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
//	szBuffer = "Forward";
	szBuffer.assign(gDLL->getText("TXT_KEY_MISC_PEDIA_FORWARD"));
}

void CvDLLWidgetData::parseBonusHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
		GAMETEXT.setBonusHelp(szBuffer, (BonusTypes)widgetDataStruct.m_iData1);
}
// BULL - Trade Denial:
void CvDLLWidgetData::parseBonusTradeHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	// <advc.073>
	int iBonus = widgetDataStruct.m_iData1; // </advc.073>
	if (widgetDataStruct.m_iData2 == -1)
		parseBonusHelp(widgetDataStruct, szBuffer);
	else /* <advc.073> Hack. Need to distinguish between the import and export columns.
			Too few iData parameters for that and widgetDataStruct.m_bOption
			can't be set from Python (via setImageButton in the EXE).
			I'm adding +1000 to the bonus id in Python (CvExoticForeignAdvisor.
			drawResourceDeals) to signal that the widget is in the import column,
			Proper solution: Two separate widget types - probably wouldn't be that
			much work to implement either. */
	{
		bool bImport = false;
		if(widgetDataStruct.m_iData1 >= 1000)
		{
			iBonus -= 1000;
			bImport = true;
		} // </advc.073>
		GAMETEXT.setBonusTradeHelp(szBuffer, (BonusTypes)iBonus,
				false, (PlayerTypes)widgetDataStruct.m_iData2,
				bImport, true); // advc.073
	}
}

// doc: city bonus help
void CvDLLWidgetData::parseBonusHelpCity(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
    CvPlot* pPlot = GC.getMap().plotByIndex(widgetDataStruct.m_iData2);
    CvCity* pCity = pPlot != NULL && pPlot->isCity() ? pPlot->getPlotCity() : NULL;

    GAMETEXT.setBonusHelp(szBuffer, (BonusTypes)widgetDataStruct.m_iData1, pCity, false);
}

void CvDLLWidgetData::parseReligionHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
		GAMETEXT.setReligionHelp(szBuffer, (ReligionTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseReligionHelpCity(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.setReligionHelpCity(szBuffer, (ReligionTypes)widgetDataStruct.m_iData1,
			gDLL->UI().getHeadSelectedCity(), true);
}

void CvDLLWidgetData::parseCorporationHelpCity(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.setCorporationHelpCity(szBuffer, (CorporationTypes)widgetDataStruct.m_iData1,
			gDLL->UI().getHeadSelectedCity(), true);
}

void CvDLLWidgetData::parseCorporationHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
		GAMETEXT.setCorporationHelp(szBuffer, (CorporationTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parsePromotionHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
		GAMETEXT.setPromotionHelp(szBuffer, (PromotionTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseEventHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.setEventHelp(szBuffer, (EventTypes)widgetDataStruct.m_iData1,
			widgetDataStruct.m_iData2, getActivePlayer());
}

void CvDLLWidgetData::parseUnitCombatHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
		GAMETEXT.setUnitCombatHelp(szBuffer, (UnitCombatTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseImprovementHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
		GAMETEXT.setImprovementHelp(szBuffer, (ImprovementTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseCivicHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
		GAMETEXT.parseCivicInfo(szBuffer, (CivicTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseCivilizationHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
		GAMETEXT.parseCivInfos(szBuffer, (CivilizationTypes)widgetDataStruct.m_iData1);
}

// doc: pagan religion pedia
void CvDLLWidgetData::parsePaganReligionHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData1 >= 0)
	{
		GAMETEXT.parsePaganReligionHelp(szBuffer, (PaganReligionTypes)widgetDataStruct.m_iData1);
	}
}

void CvDLLWidgetData::parseLeaderHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != -1)
	{
		GAMETEXT.parseLeaderTraits(szBuffer, (LeaderHeadTypes)widgetDataStruct.m_iData1,
				(CivilizationTypes)widgetDataStruct.m_iData2);
	}
}
// BULL - Leaderhead Relations - start
void CvDLLWidgetData::parseLeaderheadRelationsHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer) {

	GAMETEXT.parseLeaderHeadRelationsHelp(szBuffer, (PlayerTypes)widgetDataStruct.m_iData1,
			(PlayerTypes)widgetDataStruct.m_iData2);
} // BULL - Leaderhead Relations - end
// advc.003j (comment): unused
void CvDLLWidgetData::parseCloseScreenHelp(CvWStringBuffer& szBuffer)
{
	szBuffer.assign(gDLL->getText("TXT_KEY_MISC_CLOSE_SCREEN"));
}

void CvDLLWidgetData::parseDescriptionHelp(CvWidgetDataStruct& widgetDataStruct,
	CvWStringBuffer& szBuffer, bool bMinimal)
{
	CivilopediaPageTypes eType = (CivilopediaPageTypes)widgetDataStruct.m_iData1;
	switch (eType)
	{
	case CIVILOPEDIA_PAGE_TECH:
		{
			TechTypes eTech = (TechTypes)widgetDataStruct.m_iData2;
			if (eTech != NO_TECH)
			{
				szBuffer.assign(bMinimal ?
						GC.getInfo(eTech).getDescription() :
						gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO",
						GC.getInfo(eTech).getTextKeyWide()));
			}
		}
		break;
	case CIVILOPEDIA_PAGE_UNIT:
		{
			UnitTypes eUnit = (UnitTypes)widgetDataStruct.m_iData2;
			if (eUnit != NO_UNIT)
			{
				szBuffer.assign(bMinimal ?
						GC.getInfo(eUnit).getDescription() :
						gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO",
						GC.getInfo(eUnit).getTextKeyWide()));
			}
		}
		break;
	case CIVILOPEDIA_PAGE_BUILDING:
	case CIVILOPEDIA_PAGE_WONDER:
		{
			BuildingTypes eBuilding = (BuildingTypes)widgetDataStruct.m_iData2;
			if (eBuilding != NO_BUILDING)
			{
				szBuffer.assign(bMinimal ?
						GC.getInfo(eBuilding).getDescription() :
						gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO",
						GC.getInfo(eBuilding).getTextKeyWide()));
			}
		}
		break;
	case CIVILOPEDIA_PAGE_BONUS:
		{
			BonusTypes eBonus = (BonusTypes)widgetDataStruct.m_iData2;
			if (eBonus != NO_BONUS)
			{
				szBuffer.assign(bMinimal ?
						GC.getInfo(eBonus).getDescription() :
						gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO",
						GC.getInfo(eBonus).getTextKeyWide()));
			}
		}
		break;
	case CIVILOPEDIA_PAGE_IMPROVEMENT:
		{
			ImprovementTypes eImprovement = (ImprovementTypes)widgetDataStruct.m_iData2;
			if (eImprovement != NO_IMPROVEMENT)
			{
				szBuffer.assign(bMinimal ?
						GC.getInfo(eImprovement).getDescription() :
						gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO",
						GC.getInfo(eImprovement).getTextKeyWide()));
			}
		}
		break;
	case CIVILOPEDIA_PAGE_UNIT_GROUP:
		{
			UnitCombatTypes eGroup = (UnitCombatTypes)widgetDataStruct.m_iData2;
			if (eGroup != NO_UNITCOMBAT)
			{
				szBuffer.assign(bMinimal ?
						GC.getInfo(eGroup).getDescription() :
						gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO",
						GC.getInfo(eGroup).getTextKeyWide()));
			}
		}
		break;
	case CIVILOPEDIA_PAGE_PROMOTION:
		{
			PromotionTypes ePromo = (PromotionTypes)widgetDataStruct.m_iData2;
			if (ePromo != NO_PROMOTION)
			{
				szBuffer.assign(bMinimal ?
						GC.getInfo(ePromo).getDescription() :
						gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO",
						GC.getInfo(ePromo).getTextKeyWide()));
			}
		}
		break;
	case CIVILOPEDIA_PAGE_CIV:
		{
			CivilizationTypes eCiv = (CivilizationTypes)widgetDataStruct.m_iData2;
			if (eCiv != NO_CIVILIZATION)
			{
				szBuffer.assign(bMinimal ?
						GC.getInfo(eCiv).getDescription() :
						gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO",
						GC.getInfo(eCiv).getTextKeyWide()));
			}
		}
		break;
	case CIVILOPEDIA_PAGE_LEADER:
		{
			LeaderHeadTypes eLeader = (LeaderHeadTypes)widgetDataStruct.m_iData2;
			if (eLeader != NO_LEADER)
			{
				szBuffer.assign(bMinimal ?
						GC.getInfo(eLeader).getDescription() :
						gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO",
						GC.getInfo(eLeader).getTextKeyWide()));
			}
		}
		break;
	case CIVILOPEDIA_PAGE_RELIGION:
		{
			ReligionTypes eReligion = (ReligionTypes)widgetDataStruct.m_iData2;
			if (eReligion != NO_RELIGION)
			{
				szBuffer.assign(bMinimal ?
						GC.getInfo(eReligion).getDescription() :
						gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO",
						GC.getInfo(eReligion).getTextKeyWide()));
			}
		}
		break;
	case CIVILOPEDIA_PAGE_CORPORATION:
		{
			CorporationTypes eCorporation = (CorporationTypes)widgetDataStruct.m_iData2;
			if (eCorporation != NO_CORPORATION)
			{
				szBuffer.assign(bMinimal ?
						GC.getInfo(eCorporation).getDescription() :
						gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO",
						GC.getInfo(eCorporation).getTextKeyWide()));
			}
		}
		break;
	case CIVILOPEDIA_PAGE_CIVIC:
		{
			CivicTypes eCivic = (CivicTypes)widgetDataStruct.m_iData2;
			if (eCivic != NO_CIVIC)
			{
				szBuffer.assign(bMinimal ?
						GC.getInfo(eCivic).getDescription() :
						gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO",
						GC.getInfo(eCivic).getTextKeyWide()));
			}
		}
		break;
	case CIVILOPEDIA_PAGE_PROJECT:
		{
			ProjectTypes eProject = (ProjectTypes)widgetDataStruct.m_iData2;
			if (eProject != NO_PROJECT)
			{
				szBuffer.assign(bMinimal ?
						GC.getInfo(eProject).getDescription() :
						gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO",
						GC.getInfo(eProject).getTextKeyWide()));
			}
		}
		break;
	case CIVILOPEDIA_PAGE_CONCEPT:
		{
			ConceptTypes eConcept = (ConceptTypes)widgetDataStruct.m_iData2;
			if (eConcept != NO_CONCEPT)
				szBuffer.assign(GC.getInfo(eConcept).getDescription());
		}
		break;
	case CIVILOPEDIA_PAGE_CONCEPT_NEW:
		{
			NewConceptTypes eConcept = (NewConceptTypes)widgetDataStruct.m_iData2;
			if (eConcept != NO_NEW_CONCEPT) // kmodx: was NO_CONCEPT
				szBuffer.assign(GC.getInfo(eConcept).getDescription());
		}
		break;
	case CIVILOPEDIA_PAGE_SPECIALIST:
		{
			SpecialistTypes eSpecialist = (SpecialistTypes)widgetDataStruct.m_iData2;
			if (eSpecialist != NO_SPECIALIST)
			{
				szBuffer.assign(bMinimal ?
						GC.getInfo(eSpecialist).getDescription() :
						gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO",
						GC.getInfo(eSpecialist).getTextKeyWide()));
			}
		}
		break;
	default:
		break;
	}
}

void CvDLLWidgetData::parseKillDealHelp(CvWidgetDataStruct &widgetDataStruct,
		CvWStringBuffer &szBuffer)
{
	CvWString szTemp = szBuffer.getCString();
	CvDeal const* pDeal = GC.getGame().getDeal(widgetDataStruct.m_iData1);
	if (pDeal != NULL)
	{
		PlayerTypes eActivePlayer = getActivePlayer();
		// <advc.073>
		GAMETEXT.getDealString(szBuffer, *pDeal, eActivePlayer, false);
		szBuffer.append(NEWLINE); // </advc.073>
		if (pDeal->isCancelable(eActivePlayer, &szTemp))
		{
			szTemp = gDLL->getText("TXT_KEY_MISC_CLICK_TO_CANCEL");
		}
	}
	szBuffer.append(szTemp); // advc.073: was assign
}


void CvDLLWidgetData::doDealKill(CvWidgetDataStruct &widgetDataStruct)
{
	CvDeal* pDeal = GC.getGame().getDeal(widgetDataStruct.m_iData1);
	if (pDeal != NULL)
	{
		if (!pDeal->isCancelable(getActivePlayer()))
		{
			CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_TEXT);
			if (pInfo != NULL)
			{
				pInfo->setText(gDLL->getText("TXT_KEY_POPUP_CANNOT_CANCEL_DEAL"));
				gDLL->UI().addPopup(pInfo, getActivePlayer(), true);
			}
		}
		else
		{
			CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_DEAL_CANCELED);
			if (pInfo != NULL)
			{
				pInfo->setData1(pDeal->getID());
				pInfo->setOption1(false);
				gDLL->UI().addPopup(pInfo, getActivePlayer(), true);
			}
		}
	}
}

void CvDLLWidgetData::parseProductionModHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pCity = gDLL->UI().getHeadSelectedCity();
	if (pCity != NULL)
		GAMETEXT.setProductionHelp(szBuffer, *pCity);
}

void CvDLLWidgetData::parseLeaderheadHelp(CvWidgetDataStruct &widgetDataStruct,
	CvWStringBuffer &szBuffer)
{
	GAMETEXT.parseLeaderHeadHelp(szBuffer, (PlayerTypes)widgetDataStruct.m_iData1,
			(PlayerTypes)widgetDataStruct.m_iData2);
}

void CvDLLWidgetData::parseLeaderLineHelp(CvWidgetDataStruct &widgetDataStruct,
	CvWStringBuffer &szBuffer)
{
	GAMETEXT.parseLeaderLineHelp(szBuffer, (PlayerTypes)widgetDataStruct.m_iData1,
			(PlayerTypes)widgetDataStruct.m_iData2);
}

void CvDLLWidgetData::parseCommerceModHelp(CvWidgetDataStruct &widgetDataStruct,
	CvWStringBuffer &szBuffer)
{
	CvCity* pCity = gDLL->UI().getHeadSelectedCity();
	if (pCity != NULL)
		GAMETEXT.setCommerceHelp(szBuffer, *pCity, (CommerceTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::parseScoreHelp(CvWidgetDataStruct& widgetDataStruct,
	CvWStringBuffer& szBuffer)
{
	GAMETEXT.setScoreHelp(szBuffer, (PlayerTypes)widgetDataStruct.m_iData1);
}
// BULL - Trade Hover - start
void CvDLLWidgetData::parseTradeRoutes(CvWidgetDataStruct& widgetDataStruct,
	CvWStringBuffer& szBuffer)
{
	GAMETEXT.buildTradeString(szBuffer, (PlayerTypes)widgetDataStruct.m_iData1,
			(PlayerTypes)widgetDataStruct.m_iData2);
	GAMETEXT.getActiveDealsString(szBuffer, (PlayerTypes)widgetDataStruct.m_iData1,
			(PlayerTypes)widgetDataStruct.m_iData2,
			true); // advc.087
} // BULL - Trade Hover - end
// BULL - Food Rate Hover - start
void CvDLLWidgetData::parseFoodModHelp(CvWidgetDataStruct &widgetDataStruct,
	CvWStringBuffer &szBuffer)
{
	CvCity const* pCity = gDLL->UI().getHeadSelectedCity();
	if(pCity == NULL)
		return;
	GAMETEXT.setFoodHelp(szBuffer, *pCity);
} // BUG - Food Rate Hover - end
// <advc.085>
void CvDLLWidgetData::parsePowerRatioHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvPlayer const& kPlayer = GET_PLAYER((PlayerTypes)widgetDataStruct.m_iData1);
	CvPlayer const& kActivePlayer = GET_PLAYER(getActivePlayer());
	bool bThemVsYou = (BUGOption::getValue("Scores__PowerFormula", 0, false) == 0);
	int iPow = std::max(1, kPlayer.getPower());
	int iActivePow = std::max(1, kActivePlayer.getPower());
	int iPowerRatioPercent = fmath::round(bThemVsYou ?
			(100.0 * iPow) / iActivePow : (100.0 * iActivePow) / iPow);
	CvWString szCompareTag("TXT_KEY_POWER_RATIO_");
	if(iPowerRatioPercent < 100)
		szCompareTag += L"SMALLER";
	else if(iPowerRatioPercent > 100)
		szCompareTag += L"GREATER";
	else szCompareTag += L"EQUAL";
	CvWString szPowerRatioHelpTag("TXT_KEY_POWER_RATIO_HELP_");
	if(bThemVsYou)
		szPowerRatioHelpTag += L"THEM_VS_YOU";
	else szPowerRatioHelpTag += L"YOU_VS_THEM";
	szBuffer.append(gDLL->getText(szPowerRatioHelpTag, kPlayer.getName(),
			gDLL->getText(szCompareTag).GetCString()));
	ColorTypes eRatioColor = widgetDataStruct.m_iData2 <= 0 ? NO_COLOR :
			(ColorTypes)widgetDataStruct.m_iData2;
	if(eRatioColor != NO_COLOR)
	{
		NiColorA const& kRatioColor = GC.getInfo(eRatioColor).getColor();
		szBuffer.append(CvWString::format(L" " SETCOLR L"%d%%" ENDCOLR,
				// Based on the TEXT_COLOR macro
				(int)(kRatioColor.r * 255), (int)(kRatioColor.g * 255),
				(int)(kRatioColor.b * 255), (int)(kRatioColor.a * 255),
				iPowerRatioPercent));
	}
	else szBuffer.append(CvWString::format(L" %d%%", iPowerRatioPercent));
	if(kActivePlayer.getMasterTeam() == kPlayer.getMasterTeam())
		return; // Espionage vs. allies isn't so interesting
	int iNeededDemographics = kActivePlayer.espionageNeededToSee(kPlayer.getID(), true);
	// (Might make more sense to show this in the tech hover)
	int iNeededResearch = kActivePlayer.espionageNeededToSee(kPlayer.getID(), false);
	FAssert((iNeededDemographics <= 0 && iNeededDemographics != MAX_INT) ||
			GC.getGame().isDebugMode());
	if(iNeededDemographics == MAX_INT)
		return;
	szBuffer.append(NEWLINE);
	CvWString szSeeWhat;
	int iNeeded = iNeededDemographics;
	if(iNeededResearch <= 0)
	{
		iNeeded = iNeededResearch;
		szSeeWhat = gDLL->getText("TXT_KEY_COMMERCE_RESEARCH");
	}
	else szSeeWhat = gDLL->getText("TXT_KEY_DEMO_SCREEN_TITLE");
	szBuffer.append(gDLL->getText("TXT_KEY_SEE_INTEL_THRESHOLD",
			szSeeWhat.GetCString(), -iNeeded));
}


void CvDLLWidgetData::parseGoldenAgeAnarchyHelp(PlayerTypes ePlayer, int iData2,
	bool bAnarchy, CvWStringBuffer &szBuffer)
{
	CvPlayer const& kPlayer = GET_PLAYER(ePlayer);
	if(bAnarchy)
	{
		int iTurns = kPlayer.getAnarchyTurns();
		FAssert(iTurns > 0);
		szBuffer.append(gDLL->getText("INTERFACE_ANARCHY", iTurns));
	}
	else
	{
		szBuffer.append(gDLL->getText("TXT_KEY_CONCEPT_GOLDEN_AGE"));
		int iTurns = kPlayer.getGoldenAgeTurns();
		FAssert(iTurns > 0);
		szBuffer.append(CvWString::format(L" (%s)",
				gDLL->getText("TXT_KEY_MISC_TURNS_LEFT2", iTurns).GetCString()));
	}
} // </advc.085>

// <K-Mod> 5/jan/11: Environmental advisor mouse-over text
void CvDLLWidgetData::parsePollutionOffsetsHelp(CvWidgetDataStruct &widgetDataStruct,
	CvWStringBuffer &szBuffer)
{
	szBuffer.append(gDLL->getText("TXT_KEY_POLLUTION_OFFSETS_HELP"));
	FOR_EACH_ENUM(Feature)
	{
		int iWarmingDefence = GC.getInfo(eLoopFeature).getWarmingDefense();
		if (iWarmingDefence != 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_OFFSET_PER_FEATURE",
					-iWarmingDefence, GC.getInfo(eLoopFeature).getTextKeyWide()));
		}
	}
}

void CvDLLWidgetData::parsePollutionHelp(CvWidgetDataStruct &widgetDataStruct,
	CvWStringBuffer &szBuffer)
{
	CvPlayer::PollutionFlags eFlags = (CvPlayer::PollutionFlags)widgetDataStruct.m_iData1;

	szBuffer.append(gDLL->getText("TXT_KEY_POLLUTION")+":");

	if (eFlags & CvPlayer::POLLUTION_POPULATION)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_POLLUTION_FROM_POPULATION",
				GC.getDefineINT("GLOBAL_WARMING_POPULATION_WEIGHT")));
	}
	if (eFlags & CvPlayer::POLLUTION_BUILDINGS)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_POLLUTION_FROM_BUILDINGS",
				GC.getDefineINT("GLOBAL_WARMING_BUILDING_WEIGHT")));
	}
	if (eFlags & CvPlayer::POLLUTION_BONUSES)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_POLLUTION_FROM_BONUSES",
				GC.getDefineINT("GLOBAL_WARMING_BONUS_WEIGHT")));
	}
	if (eFlags & CvPlayer::POLLUTION_POWER)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_POLLUTION_FROM_POWER",
				GC.getDefineINT("GLOBAL_WARMING_POWER_WEIGHT")));
	}
} // </K-Mod>

// advc.ctr:
bool CvDLLWidgetData::parseCityTradeHelp(CvWidgetDataStruct const& kWidget,
	CvCity*& pCity, PlayerTypes& eWhoTo) const
{
	bool bListMore = false;
	// bListMore, eOwner and eWhoTo are all folded into data1
	int iPlayerCode = kWidget.m_iData1;
	FAssert(iPlayerCode >= 100);
	// Undo the computation in drawCityDeals (CvExoticForeignAdvisor.py)
	if (iPlayerCode >= 10000)
	{
		bListMore = true;
		iPlayerCode /= 100;
		iPlayerCode--;
	}
	PlayerTypes eOwner = (PlayerTypes)(iPlayerCode % 100);
	FAssertBounds(0, MAX_CIV_PLAYERS, eOwner);
	eWhoTo = (PlayerTypes)((iPlayerCode / 100) - 1);
	FAssertBounds(0, MAX_CIV_PLAYERS, eWhoTo);
	pCity = ::getCity(IDInfo(eOwner, kWidget.m_iData2));
	FAssert(pCity != NULL);
	return bListMore;
}

// rfc: stability help
void CvDLLWidgetData::parseStabilityExpansionHelp(CvWidgetDataStruct& widgetDataStruct, CvWStringBuffer& szBuffer)
{
	GAMETEXT.buildStabilityParameterString(szBuffer, 0);
}

// rfc: stability help
void CvDLLWidgetData::parseStabilityEconomyHelp(CvWidgetDataStruct& widgetDataStruct, CvWStringBuffer& szBuffer)
{
	GAMETEXT.buildStabilityParameterString(szBuffer, 1);
}

// rfc: stability help
void CvDLLWidgetData::parseStabilityDomesticHelp(CvWidgetDataStruct& widgetDataStruct, CvWStringBuffer& szBuffer)
{
	GAMETEXT.buildStabilityParameterString(szBuffer, 2);
}

// rfc: stability help
void CvDLLWidgetData::parseStabilityForeignHelp(CvWidgetDataStruct& widgetDataStruct, CvWStringBuffer& szBuffer)
{
	GAMETEXT.buildStabilityParameterString(szBuffer, 3);
}

// rfc: stability help
void CvDLLWidgetData::parseStabilityMilitaryHelp(CvWidgetDataStruct& widgetDataStruct, CvWStringBuffer& szBuffer)
{
	GAMETEXT.buildStabilityParameterString(szBuffer, 4);
}

// rfc: stability help
void CvDLLWidgetData::parseStabilityHelp(CvWidgetDataStruct& widgetDataStruct, CvWStringBuffer& szBuffer)
{
	GAMETEXT.buildStabilityString(szBuffer, widgetDataStruct.m_iData1);
}

// doc (merijn): wonder limit help
void CvDLLWidgetData::parseWonderLimitHelp(CvWidgetDataStruct& widgetDataStruct, CvWStringBuffer& szBuffer)
{
	CvCity* pHeadSelectedCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();
	if (NULL != pHeadSelectedCity)
	{
		GAMETEXT.setWonderLimitHelp(szBuffer, *pHeadSelectedCity, widgetDataStruct.m_iData1);
	}
}

// doc: satellite limit help
void CvDLLWidgetData::parseSatelliteLimitHelp(CvWidgetDataStruct& widgetDataStruct, CvWStringBuffer& szBuffer)
{
	CvCity* pHeadSelectedCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();
	if (NULL != pHeadSelectedCity)
	{
		GAMETEXT.setSatelliteLimitHelp(szBuffer, *pHeadSelectedCity);
	}
}

// doc: first discovered help
void CvDLLWidgetData::parseFirstDiscoveredHelp(CvWidgetDataStruct& widgetDataStruct, CvWStringBuffer& szBuffer)
{
	int iFirstDiscoveredTurn = GC.getGame().getFirstDiscoveredTurn((TechTypes)widgetDataStruct.m_iData1);
	int iFirstDiscoveredYear = GC.getGame().getTurnYear(iFirstDiscoveredTurn);
	szBuffer.append(gDLL->getText("TXT_KEY_WIDGET_FIRST_DISCOVERED", GC.getCivilizationInfo(GC.getGame().getFirstDiscovered((TechTypes)widgetDataStruct.m_iData1)).getShortDescription(), abs(iFirstDiscoveredYear), iFirstDiscoveredYear >= 0 ? gDLL->getText("TXT_KEY_AD").c_str() : gDLL->getText("TXT_KEY_BC").c_str()));
}