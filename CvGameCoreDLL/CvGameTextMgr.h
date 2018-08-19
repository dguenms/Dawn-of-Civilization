#pragma once

//  $Header:
//------------------------------------------------------------------------------------------------
//
//  FILE:    CvGameTextMgr.h
//
//  AUTHOR:  Jesse Smith  --  10/2004
//
//  PURPOSE: Group of functions to manage CIV Game Text
//
//------------------------------------------------------------------------------------------------
//  Copyright (c) 2004 Firaxis Games, Inc. All rights reserved.
//------------------------------------------------------------------------------------------------
#ifndef CIV4_GAME_TEXT_MGR_H
#define CIV4_GAME_TEXT_MGR_H

#include "CvInfos.h"
//#include "CvEnums.h"

#pragma warning( disable: 4251 )	// needs to have dll-interface to be used by clients of class

class CvCity;
class CvDeal;
class CvPopupInfo;
class CvPlayer;

//
// Class:		CvGameTextMgr
// Purpose:		Manages Game Text...
class CvGameTextMgr
{
	friend class CvGlobals;
public:
	// singleton accessor
	DllExport static CvGameTextMgr& GetInstance();

	DllExport CvGameTextMgr();
	DllExport virtual ~CvGameTextMgr();

	DllExport void Initialize();
	DllExport void DeInitialize();
	DllExport void Reset();

	DllExport int getCurrentLanguage();

	DllExport void setTimeStr(CvWString& szString, int iGameTurn, bool bSave);
	DllExport void setYearStr(CvWString& szString, int iGameTurn, bool bSave, CalendarTypes eCalendar, int iStartYear, GameSpeedTypes eSpeed);
	DllExport void setDateStr(CvWString& szString, int iGameTurn, bool bSave, CalendarTypes eCalendar, int iStartYear, GameSpeedTypes eSpeed);
	DllExport void setDateStrPlayer(CvWString& szString, int iGameTurn, bool bSave, CalendarTypes eCalendar, int iStartYear, GameSpeedTypes eSpeed, PlayerTypes ePlayer); //Rhye
	DllExport void setInterfaceTime(CvWString& szString, PlayerTypes ePlayer);
	DllExport void setGoldStr(CvWString& szString, PlayerTypes ePlayer);
	DllExport void setResearchStr(CvWString& szString, PlayerTypes ePlayer);
	DllExport void setOOSSeeds(CvWString& szString, PlayerTypes ePlayer);
	DllExport void setNetStats(CvWString& szString, PlayerTypes ePlayer);
	DllExport void setMinimizePopupHelp(CvWString& szString, const CvPopupInfo & info);

	DllExport void setUnitHelp(CvWStringBuffer &szString, const CvUnit* pUnit, bool bOneLine = false, bool bShort = false);
	DllExport void setPlotListHelp(CvWStringBuffer &szString, CvPlot* pPlot, bool bOneLine, bool bShort);
	DllExport bool setCombatPlotHelp(CvWStringBuffer &szString, CvPlot* pPlot);
	DllExport void setPlotHelp(CvWStringBuffer &szString, CvPlot* pPlot);
	DllExport void setCityBarHelp(CvWStringBuffer &szString, CvCity* pCity);
	DllExport void setScoreHelp(CvWStringBuffer &szString, PlayerTypes ePlayer);

	DllExport void parseTraits(CvWStringBuffer &szHelpString, TraitTypes eTrait, CivilizationTypes eCivilization = NO_CIVILIZATION, bool bDawnOfMan = false);
	DllExport void parseLeaderTraits(CvWStringBuffer &szInfoText, LeaderHeadTypes eLeader = NO_LEADER, CivilizationTypes eCivilization = NO_CIVILIZATION, bool bDawnOfMan = false, bool bCivilopediaText = false);
	DllExport void parseLeaderShortTraits(CvWStringBuffer &szInfoText, LeaderHeadTypes eLeader);
	DllExport void parseCivInfos(CvWStringBuffer &szHelpString, CivilizationTypes eCivilization, bool bDawnOfMan = false, bool bLinks = true);
	DllExport void parseSpecialistHelp(CvWStringBuffer &szHelpString, SpecialistTypes eSpecialist, CvCity* pCity, bool bCivilopediaText = false);
// BUG - Specialist Actual Effects - start
	void parseSpecialistHelpActual(CvWStringBuffer &szHelpString, SpecialistTypes eSpecialist, CvCity* pCity, bool bCivilopediaText = false, int iChange = 0);
// BUG - Specialist Actual Effects - end
	DllExport void parseFreeSpecialistHelp(CvWStringBuffer &szHelpString, const CvCity& kCity);
	DllExport void parsePromotionHelp(CvWStringBuffer &szBuffer, PromotionTypes ePromotion, const wchar* pcNewline = NEWLINE);
	DllExport void parseCivicInfo(CvWStringBuffer &szBuffer, CivicTypes eCivic, bool bCivilopediaText = false, bool bPlayerContext = false, bool bSkipName = false);
	DllExport void parsePlayerTraits(CvWStringBuffer &szBuffer, PlayerTypes ePlayer);
	DllExport void parseLeaderHeadHelp(CvWStringBuffer &szBuffer, PlayerTypes eThisPlayer, PlayerTypes eOtherPlayer);
	DllExport void parseLeaderLineHelp(CvWStringBuffer &szBuffer, PlayerTypes eThisPlayer, PlayerTypes eOtherPlayer);
	DllExport void parseGreatPeopleHelp(CvWStringBuffer &szBuffer, CvCity& city);
// BUG - Building Additional Great People - start
	bool setBuildingAdditionalGreatPeopleHelp(CvWStringBuffer &szBuffer, const CvCity& city, const CvWString& szStart, bool bStarted = false);
// BUG - Building Additional Great People - end
	DllExport void parseGreatGeneralHelp(CvWStringBuffer &szBuffer, CvPlayer& kPlayer);
	DllExport void parseGreatSpyHelp(CvWStringBuffer &szBuffer, CvPlayer& kPlayer); // Leoreth
	DllExport void parseMinorReligionHelp(CvWStringBuffer &szBuffer, CivilizationTypes eCivilization); // Leoreth

	DllExport void setTechHelp(CvWStringBuffer &szBuffer, TechTypes eTech, bool bCivilopediaText = false, bool bPlayerContext = false, bool bStrategyText = false, bool bTreeInfo = true, TechTypes eFromTech = NO_TECH);
// BUG - Trade Denial - start
	DllExport void setTechTradeHelp(CvWStringBuffer &szBuffer, TechTypes eTech, PlayerTypes eTradePlayer, bool bCivilopediaText = false, bool bPlayerContext = false, bool bStrategyText = false, bool bTreeInfo = true, TechTypes eFromTech = NO_TECH);
// BUG - Trade Denial - end
	DllExport void setBasicUnitHelp(CvWStringBuffer &szBuffer, UnitTypes eUnit, bool bCivilopediaText = false);
// BUG - Starting Experience - start
	void setBasicUnitHelpWithCity(CvWStringBuffer &szBuffer, UnitTypes eUnit, bool bCivilopediaText = false, CvCity* pCity = NULL, bool bConscript = false);
	void setUnitExperienceHelp(CvWStringBuffer &szBuffer, CvWString szStart, UnitTypes eUnit, CvCity* pCity, bool bConscript = false);
// BUG - Starting Experience - end
	DllExport void setUnitHelp(CvWStringBuffer &szBuffer, UnitTypes eUnit, bool bCivilopediaText = false, bool bStrategyText = false, bool bTechChooserText = false, CvCity* pCity = NULL);
	DllExport void setBuildingHelp(CvWStringBuffer &szBuffer, BuildingTypes eBuilding, bool bCivilopediaText = false, bool bStrategyText = false, bool bTechChooserText = false, CvCity* pCity = NULL);
// BUG - Building Actual Effects - start
	void setBuildingActualEffects(CvWStringBuffer &szBuffer, CvWString &szStart, BuildingTypes eBuilding, CvCity* pCity, bool bNewLine = true);
	void setBuildingHelpActual(CvWStringBuffer &szBuffer, BuildingTypes eBuilding, bool bCivilopediaText = false, bool bStrategyText = false, bool bTechChooserText = false, CvCity* pCity = NULL, bool bActual = true);
// BUG - Building Actual Effects - end
// BUG - Production Decay - start
	void setProductionDecayHelp(CvWStringBuffer &szBuffer, int iTurnsLeft, int iThreshold, int iDecay, bool bProducing);
// BUG - Production Decay - end
	DllExport void setProjectHelp(CvWStringBuffer &szBuffer, ProjectTypes eProject, bool bCivilopediaText = false, CvCity* pCity = NULL);
	DllExport void setProcessHelp(CvWStringBuffer &szBuffer, ProcessTypes eProcess);
	DllExport void setGoodHealthHelp(CvWStringBuffer &szBuffer, CvCity& city);
	DllExport void setBadHealthHelp(CvWStringBuffer &szBuffer, CvCity& city);
// BUG - Building Additional Health - start
	bool setBuildingAdditionalHealthHelp(CvWStringBuffer &szBuffer, const CvCity& city, const CvWString& szStart, bool bStarted = false);
// BUG - Building Additional Health - end
	DllExport void setAngerHelp(CvWStringBuffer &szBuffer, CvCity& city);
	DllExport void setHappyHelp(CvWStringBuffer &szBuffer, CvCity& city);
// BUG - Building Additional Happiness - start
	bool setBuildingAdditionalHappinessHelp(CvWStringBuffer &szBuffer, const CvCity& city, const CvWString& szStart, bool bStarted = false);
// BUG - Building Additional Happiness - end
	DllExport void setYieldChangeHelp(CvWStringBuffer &szBuffer, const CvWString& szStart, const CvWString& szSpace, const CvWString& szEnd, const int* piYieldChange, bool bPercent = false, bool bNewLine = true);
	DllExport void setCommerceChangeHelp(CvWStringBuffer &szBuffer, const CvWString& szStart, const CvWString& szSpace, const CvWString& szEnd, const int* piCommerceChange, bool bPercent = false, bool bNewLine = true);
// BUG - Resumable Value Change Help - start
	void setCommerceTimes100ChangeHelp(CvWStringBuffer &szBuffer, const CvWString& szStart, const CvWString& szSpace, const CvWString& szEnd, const int* piCommerceChange, bool bNewLine = false, bool bStarted = false);
	bool setResumableYieldChangeHelp(CvWStringBuffer &szBuffer, const CvWString& szStart, const CvWString& szSpace, const CvWString& szEnd, const int* piYieldChange, bool bPercent = false, bool bNewLine = true, bool bStarted = false);
	bool setResumableCommerceChangeHelp(CvWStringBuffer &szBuffer, const CvWString& szStart, const CvWString& szSpace, const CvWString& szEnd, const int* piCommerceChange, bool bPercent = false, bool bNewLine = true, bool bStarted = false);
	bool setResumableCommerceTimes100ChangeHelp(CvWStringBuffer &szBuffer, const CvWString& szStart, const CvWString& szSpace, const CvWString& szEnd, const int* piCommerceChange, bool bNewLine, bool bStarted = false);
	bool setResumableGoodBadChangeHelp(CvWStringBuffer &szBuffer, const CvWString& szStart, const CvWString& szSpace, const CvWString& szEnd, int iGood, int iGoodSymbol, int iBad, int iBadSymbol, bool bPercent = false, bool bNewLine = false, bool bStarted = false);
	bool setResumableValueChangeHelp(CvWStringBuffer &szBuffer, const CvWString& szStart, const CvWString& szSpace, const CvWString& szEnd, int iValue, int iSymbol, bool bPercent = false, bool bNewLine = false, bool bStarted = false);
	bool setResumableValueTimes100ChangeHelp(CvWStringBuffer &szBuffer, const CvWString& szStart, const CvWString& szSpace, const CvWString& szEnd, int iValue, int iSymbol, bool bNewLine = false, bool bStarted = false);
// BUG - Resumable Value Change Help - end
	DllExport void setBonusHelp(CvWStringBuffer &szBuffer, BonusTypes eBonus, bool bCivilopediaText = false, CvCity* pCity = NULL);
// BUG - Trade Denial - start
	DllExport void setBonusTradeHelp(CvWStringBuffer &szBuffer, BonusTypes eBonus, bool bCivilopediaText, PlayerTypes eTradePlayer, CvCity* pCity = NULL);
// BUG - Trade Denial - end
	DllExport void setReligionHelp(CvWStringBuffer &szBuffer, ReligionTypes eReligion, bool bCivilopedia = false, bool bStateReligion = false);
	DllExport void setReligionHelpCity(CvWStringBuffer &szBuffer, ReligionTypes eReligion, CvCity *pCity, bool bCityScreen = false, bool bForceReligion = false, bool bForceState = false, bool bNoStateReligion = false);
	DllExport void setCorporationHelp(CvWStringBuffer &szBuffer, CorporationTypes eCorporation, bool bCivilopedia = false);
	DllExport void setCorporationHelpCity(CvWStringBuffer &szBuffer, CorporationTypes eCorporation, CvCity *pCity, bool bCityScreen = false, bool bForceCorporation = false);
	DllExport void setPromotionHelp(CvWStringBuffer &szBuffer, PromotionTypes ePromotion, bool bCivilopediaText = false);
	DllExport void setUnitCombatHelp(CvWStringBuffer &szBuffer, UnitCombatTypes eUnitCombat);
	DllExport void setImprovementHelp(CvWStringBuffer &szBuffer, ImprovementTypes eImprovement, bool bCivilopediaText = false);
	DllExport void setRemoveHelp(CvWStringBuffer &szBuffer, TechTypes eTech);
	DllExport void setTerrainHelp(CvWStringBuffer &szBuffer, TerrainTypes eTerrain, bool bCivilopediaText = false);
	DllExport void setFeatureHelp(CvWStringBuffer &szBuffer, FeatureTypes eFeature, bool bCivilopediaText = false);
// BUG - Food Rate Hover - start
	void setFoodHelp(CvWStringBuffer &szBuffer, CvCity& city);
// BUG - Food Rate Hover - end
// BUG - Building Additional Yield - start
	bool setBuildingAdditionalYieldHelp(CvWStringBuffer &szBuffer, const CvCity& city, YieldTypes eIndex, const CvWString& szStart, bool bStarted = false);
// BUG - Building Additional Yield - end
	DllExport void setProductionHelp(CvWStringBuffer &szBuffer, CvCity& city);
	DllExport void setCommerceHelp(CvWStringBuffer &szBuffer, CvCity& city, CommerceTypes eCommerceType);
// BUG - Building Additional Commerce - start
	bool setBuildingAdditionalCommerceHelp(CvWStringBuffer &szBuffer, const CvCity& city, CommerceTypes eIndex, const CvWString& szStart, bool bStarted = false);
// BUG - Building Additional Commerce - end
// BUG - Building Saved Maintenance - start
	bool setBuildingSavedMaintenanceHelp(CvWStringBuffer &szBuffer, const CvCity& city, const CvWString& szStart, bool bStarted = false);
// BUG - Building Saved Maintenance - start
	DllExport void setYieldHelp(CvWStringBuffer &szBuffer, CvCity& city, YieldTypes eYieldType);
	DllExport void setConvertHelp(CvWStringBuffer& szBuffer, PlayerTypes ePlayer, ReligionTypes eReligion);
	DllExport void setRevolutionHelp(CvWStringBuffer& szBuffer, PlayerTypes ePlayer);
	DllExport void setVassalRevoltHelp(CvWStringBuffer& szBuffer, TeamTypes eMaster, TeamTypes eVassal);
	DllExport void setEventHelp(CvWStringBuffer& szBuffer, EventTypes eEvent, int iEventTriggeredId, PlayerTypes ePlayer);
	DllExport void setTradeRouteHelp(CvWStringBuffer &szBuffer, int iRoute, CvCity* pCity);
	DllExport void setEspionageCostHelp(CvWStringBuffer &szBuffer, EspionageMissionTypes eMission, PlayerTypes eTargetPlayer, const CvPlot* pPlot, int iExtraData, const CvUnit* pSpyUnit);
	DllExport void setEspionageMissionHelp(CvWStringBuffer &szBuffer, const CvUnit* pUnit);

	DllExport void buildObsoleteString( CvWStringBuffer& szBuffer, int iItem, bool bList = false, bool bPlayerContext = false );
	DllExport void buildObsoleteBonusString( CvWStringBuffer& szBuffer, int iItem, bool bList = false, bool bPlayerContext = false);
	DllExport void buildObsoleteSpecialString( CvWStringBuffer& szBuffer, int iItem, bool bList = false, bool bPlayerContext = false );
	DllExport void buildMoveString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildFreeUnitString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildFeatureProductionString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildWorkerRateString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildTradeRouteString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildHealthRateString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildHappinessRateString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildFreeTechString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildLOSString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildMapCenterString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildMapRevealString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false );
	DllExport void buildMapTradeString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildTechTradeString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildGoldTradeString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildOpenBordersString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildDefensivePactString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildPermanentAllianceString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildVassalStateString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildBridgeString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildIrrigationString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildIgnoreIrrigationString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildWaterWorkString( CvWStringBuffer &szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildImprovementString( CvWStringBuffer& szBuffer, TechTypes eTech, int iImprovement, bool bList = false, bool bPlayerContext = false );
	DllExport void buildDomainExtraMovesString( CvWStringBuffer& szBuffer, TechTypes eTech, int iCommerceType, bool bList = false, bool bPlayerContext = false );
	DllExport void buildAdjustString( CvWStringBuffer& szBuffer, TechTypes eTech, int iCommerceType, bool bList = false, bool bPlayerContext = false );
	DllExport void buildTerrainTradeString( CvWStringBuffer& szBuffer, TechTypes eTech, int iTerrainType, bool bList = false, bool bPlayerContext = false );
	DllExport void buildRiverTradeString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildSpecialBuildingString( CvWStringBuffer& szBuffer, TechTypes eTech, int iBuildingType, bool bList = false, bool bPlayerContext = false );
	DllExport void buildYieldChangeString( CvWStringBuffer& szBuffer, TechTypes eTech, int iTieldType, bool bList = false, bool bPlayerContext = false );
	DllExport bool buildBonusRevealString( CvWStringBuffer& szBuffer, TechTypes eTech, int iBonusType, bool bFirst, bool bList = false, bool bPlayerContext = false );
	DllExport bool buildCivicRevealString( CvWStringBuffer& szBuffer, TechTypes eTech, int iCivicType, bool bFirst, bool bList = false, bool bPlayerContext = false );
	DllExport bool buildBonusTradeString(CvWStringBuffer& szBuffer, TechTypes eTech, int iBonusType, bool bFirst, bool bList = false, bool bPlayerContext = false );
	DllExport bool buildProcessInfoString( CvWStringBuffer& szBuffer, TechTypes eTech, int iProcessType, bool bFirst, bool bList = false, bool bPlayerContext = false );
	DllExport bool buildFoundReligionString( CvWStringBuffer& szBuffer, TechTypes eTech, int iReligionType, bool bFirst, bool bList = false, bool bPlayerContext = false );
	DllExport bool buildFoundCorporationString( CvWStringBuffer& szBuffer, TechTypes eTech, int iCorporationType, bool bFirst, bool bList = false, bool bPlayerContext = false );
	DllExport bool buildPromotionString( CvWStringBuffer& szBuffer, TechTypes eTech, int iPromotionType, bool bFirst, bool bList = false, bool bPlayerContext = false );
	DllExport void buildHintsList(CvWStringBuffer& szBuffer);
	DllExport void buildBuildingRequiresString(CvWStringBuffer& szBuffer, BuildingTypes eBuilding, bool bCivilopediaText, bool bTechChooserText, const CvCity* pCity);

	// Leoreth
	DllExport void buildStabilityParameterString(CvWStringBuffer& szBuffer, int iStabilityCategory);
	DllExport void buildStabilityString(CvWStringBuffer& szBuffer, int iStabilityChange);

	DllExport void buildCityBillboardIconString( CvWStringBuffer& szBuffer, CvCity* pCity);
	DllExport void buildCityBillboardCityNameString( CvWStringBuffer& szBuffer, CvCity* pCity);
	DllExport void buildCityBillboardProductionString( CvWStringBuffer& szBuffer, CvCity* pCity);
	DllExport void buildCityBillboardCitySizeString( CvWStringBuffer& szBuffer, CvCity* pCity, const NiColorA& kColor);
	DllExport void getCityBillboardFoodbarColors(CvCity* pCity, std::vector<NiColorA>& aColors);
	DllExport void getCityBillboardProductionbarColors(CvCity* pCity, std::vector<NiColorA>& aColors);

	DllExport void buildSingleLineTechTreeString(CvWStringBuffer &szBuffer, TechTypes eTech, bool bPlayerContext);
	DllExport void buildTechTreeString(CvWStringBuffer &szBuffer, TechTypes eTech, bool bPlayerContext, TechTypes eFromTech);

	void getWarplanString(CvWStringBuffer& szString, WarPlanTypes eWarPlan);
	DllExport void getAttitudeString(CvWStringBuffer& szBuffer, PlayerTypes ePlayer, PlayerTypes eTargetPlayer);
	DllExport void getEspionageString(CvWStringBuffer& szBuffer, PlayerTypes ePlayer, PlayerTypes eTargetPlayer);
	DllExport void getTradeString(CvWStringBuffer& szBuffer, const TradeData& tradeData, PlayerTypes ePlayer1, PlayerTypes ePlayer2);
	DllExport void getDealString(CvWStringBuffer& szString, CvDeal& deal, PlayerTypes ePlayerPerspective = NO_PLAYER);
	void getDealString(CvWStringBuffer& szBuffer, PlayerTypes ePlayer1, PlayerTypes ePlayer2, const CLinkList<TradeData>* pListPlayer1, const CLinkList<TradeData>* pListPlayer2, PlayerTypes ePlayerPerspective = NO_PLAYER);
	DllExport void getActiveDealsString(CvWStringBuffer& szString, PlayerTypes eThisPlayer, PlayerTypes eOtherPlayer);
	void getOtherRelationsString(CvWStringBuffer& szString, PlayerTypes eThisPlayer, PlayerTypes eOtherPlayer);
// BUG - Leaderhead Relations - start
	void parseLeaderHeadRelationsHelp(CvWStringBuffer &szBuffer, PlayerTypes eThisPlayer, PlayerTypes eOtherPlayer);
	void getAllRelationsString(CvWStringBuffer& szString, TeamTypes eThisTeam);
	void getActiveTeamRelationsString(CvWStringBuffer& szString, TeamTypes eThisTeam);
	void getOtherRelationsString(CvWStringBuffer& szString, TeamTypes eThisTeam, TeamTypes eOtherTeam, TeamTypes eSkipTeam);
// BUG - Leaderhead Relations - end

// BUG - Finance Advisor - start
	void buildFinanceSpecialistGoldString(CvWStringBuffer& szBuffer, PlayerTypes ePlayer);
// BUG - Finance Advisor - end

	DllExport void buildFinanceInflationString(CvWStringBuffer& szDetails, PlayerTypes ePlayer);
	DllExport void buildFinanceUnitCostString(CvWStringBuffer& szDetails, PlayerTypes ePlayer);
	DllExport void buildFinanceAwaySupplyString(CvWStringBuffer& szDetails, PlayerTypes ePlayer);
	DllExport void buildFinanceCityMaintString(CvWStringBuffer& szDetails, PlayerTypes ePlayer);
	DllExport void buildFinanceCivicUpkeepString(CvWStringBuffer& szDetails, PlayerTypes ePlayer);
	DllExport void buildFinanceForeignIncomeString(CvWStringBuffer& szDetails, PlayerTypes ePlayer);

	DllExport void getTradeScreenTitleIcon(CvString& szButton, CvWidgetDataStruct& widgetData, PlayerTypes ePlayer);
	DllExport void getTradeScreenIcons(std::vector< std::pair<CvString, CvWidgetDataStruct> >& aIconInfos, PlayerTypes ePlayer);
	DllExport void getTradeScreenHeader(CvWString& szHeader, PlayerTypes ePlayer, PlayerTypes eOtherPlayer, bool bAttitude);

// BUG - Trade Hover - start
	void buildDomesticTradeString(CvWStringBuffer& szDetails, PlayerTypes ePlayer);
	void buildForeignTradeString(CvWStringBuffer& szDetails, PlayerTypes ePlayer);
	void buildTradeString(CvWStringBuffer& szBuffer, PlayerTypes ePlayer, PlayerTypes eWithPlayer=NO_PLAYER, bool bDomestic=true, bool bForeign=true, bool bHeading=true);
// BUG - Trade Hover - end

// BUG - Defense Hover - start
	void setDefenseHelp(CvWStringBuffer &szBuffer, CvCity& city);
// BUG - Defense Hover - end
// BUG - Building Additional Defense - start
	bool setBuildingAdditionalDefenseHelp(CvWStringBuffer &szBuffer, const CvCity& city, const CvWString& szStart, bool bStarted = false);
// BUG - Building Additional Defense - end
// BUG - Building Additional Bombard Defense - start
	bool setBuildingAdditionalBombardDefenseHelp(CvWStringBuffer &szBuffer, const CvCity& city, const CvWString& szStart, bool bStarted = false);
// BUG - Building Additional Bombard Defense - end

	DllExport void getGlobeLayerName(GlobeLayerTypes eType, int iOption, CvWString& strName);

	DllExport void getPlotHelp(CvPlot* pMouseOverPlot, CvCity* pCity, CvPlot* pFlagPlot, bool bAlt, CvWStringBuffer& strHelp);
	void getRebasePlotHelp(CvPlot* pPlot, CvWString& strHelp);
	void getNukePlotHelp(CvPlot* pPlot, CvWString& strHelp);
	DllExport void getInterfaceCenterText(CvWString& strText);
	DllExport void getTurnTimerText(CvWString& strText);
	DllExport void getFontSymbols(std::vector< std::vector<wchar> >& aacSymbols, std::vector<int>& aiMaxNumRows);
	DllExport void assignFontIds(int iFirstSymbolCode, int iPadAmount);

	DllExport void getCityDataForAS(std::vector<CvWBData>& mapCityList, std::vector<CvWBData>& mapBuildingList, std::vector<CvWBData>& mapAutomateList);
	DllExport void getUnitDataForAS(std::vector<CvWBData>& mapUnitList);
	DllExport void getImprovementDataForAS(std::vector<CvWBData>& mapImprovementList, std::vector<CvWBData>& mapRouteList);
	DllExport void getVisibilityDataForAS(std::vector<CvWBData>& mapVisibilityList);
	DllExport void getTechDataForAS(std::vector<CvWBData>& mapTechList);

	DllExport void getUnitDataForWB(std::vector<CvWBData>& mapUnitData);
	DllExport void getBuildingDataForWB(bool bStickyButton, std::vector<CvWBData>& mapBuildingData);
	DllExport void getTerrainDataForWB(std::vector<CvWBData>& mapTerrainData, std::vector<CvWBData>& mapFeatureData, std::vector<CvWBData>& mapPlotData, std::vector<CvWBData>& mapRouteData);
	DllExport void getTerritoryDataForWB(std::vector<CvWBData>& mapTerritoryData);

	DllExport void getTechDataForWB(std::vector<CvWBData>& mapTechData);
	DllExport void getPromotionDataForWB(std::vector<CvWBData>& mapPromotionData);
	DllExport void getBonusDataForWB(std::vector<CvWBData>& mapBonusData);
	DllExport void getImprovementDataForWB(std::vector<CvWBData>& mapImprovementData);
	DllExport void getReligionDataForWB(bool bHolyCity, std::vector<CvWBData>& mapReligionData);
	DllExport void getCorporationDataForWB(bool bHeadquarters, std::vector<CvWBData>& mapCorporationData);

private:
	void eventTechHelp(CvWStringBuffer& szBuffer, EventTypes eEvent, TechTypes eTech, PlayerTypes ePlayer, PlayerTypes eOtherPlayer);
	void eventGoldHelp(CvWStringBuffer& szBuffer, EventTypes eEvent, PlayerTypes ePlayer, PlayerTypes eOtherPlayer);

	std::vector<int*> m_apbPromotion;

	void setCityPlotYieldValueString(CvWStringBuffer &szString, CvCity* pCity, int iIndex, bool bAvoidGrowth, bool bIgnoreGrowth, bool bIgnoreFood = false);
	void setYieldValueString(CvWStringBuffer &szString, int iValue, bool bActive = false, bool bMakeWhitespace = false);

	// Leoreth
	CvWString createStars(int iNumStars);
};

// Singleton Accessor
#define GAMETEXT CvGameTextMgr::GetInstance()

#endif
