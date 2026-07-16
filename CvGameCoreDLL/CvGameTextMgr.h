#pragma once
//  AUTHOR:  Jesse Smith  --  10/2004
//  PURPOSE: Group of functions to manage CIV Game Text
//  Copyright (c) 2004 Firaxis Games, Inc. All rights reserved.
#ifndef CIV4_GAME_TEXT_MGR_H
#define CIV4_GAME_TEXT_MGR_H

class CvCity;
class CvDeal;
class CvPopupInfo;
class CvPlayer;


class CvGameTextMgr
{
	friend class CvGlobals;
public:
	DllExport static CvGameTextMgr& GetInstance() // singleton accessor
	{
		static CvGameTextMgr gs_GameTextMgr;
		return gs_GameTextMgr;
	}

	CvGameTextMgr() : /* advc.099f: */ m_bAlwaysShowPlotCulture(true) {}
	virtual ~CvGameTextMgr() {}

	DllExport void Initialize() {} // allocate memory
	DllExport void DeInitialize(); // deallocate memory
	DllExport void Reset();

	int getCurrentLanguage();

	DllExport void setTimeStr(CvWString& szString, int iGameTurn, bool bSave);
	void setYearStr(CvWString& szString, int iGameTurn, bool bSave, CalendarTypes eCalendar, int iStartYear, GameSpeedTypes eSpeed);
	void setDateStr(CvWString& szString, int iGameTurn, bool bSave, CalendarTypes eCalendar, int iStartYear, GameSpeedTypes eSpeed);
	void setDateStrPlayer(CvWString& szString, int iGameTurn, bool bSave, CalendarTypes eCalendar, int iStartYear, GameSpeedTypes eSpeed, PlayerTypes ePlayer); // rfc
	void setInterfaceTime(CvWString& szString, PlayerTypes ePlayer);
	void setGoldStr(CvWString& szString, PlayerTypes ePlayer);
	void setResearchStr(CvWString& szString, PlayerTypes ePlayer);
	void setOOSSeeds(CvWString& szString, PlayerTypes ePlayer);
	void setNetStats(CvWString& szString, PlayerTypes ePlayer);
	DllExport void setMinimizePopupHelp(CvWString& szString, const CvPopupInfo & info);

	void setUnitHelp(CvWStringBuffer &szString, const CvUnit* pUnit,
			bool bOneLine = false, bool bShort = false,
			bool bColorAllegiance = false, // advc.048
			bool bOmitOwner = false, // advc.061
			bool bIndicator = false); // advc.007
	// advc.004 (Exposed to Python, replacing redundant code in CyMainInterface.py)
	void setHurtUnitStrength(CvWString& szBuffer, CvUnit const& kUnit,
			int iHP = -1); // advc.048c
	void setPlotListHelp(CvWStringBuffer &szString, CvPlot const& kPlot, bool bOneLine, bool bShort,
			bool bIndicator = false); // advc.061
	// <advc.004c>
	void setInterceptPlotHelp(CvPlot const& kPlot, CvUnit const& kUnit,
			CvWString& szHelp, bool bNewline = true); // </advc.004c>
	bool setCombatPlotHelp(CvWStringBuffer &szString, CvPlot* pPlot);
	// <advc> Note: These are now implemented in ACOText.cpp
	void setACOPlotHelp(CvWStringBuffer &szString, CvPlot const& kPlot,
			CvUnit const& kAttacker, CvUnit const& kDefender, int iView,
			bool bBestOddsHelp);
	void setACOModifiersPlotHelp(CvWStringBuffer &szString, CvPlot const& kPlot,
			CvUnit const& kAttacker, CvUnit const& kDefender, int iView);
	// </advc>
	// <advc.089>
	void setCannotAttackHelp(CvWStringBuffer& szHelp, CvUnit const& kAttacker,
			CvUnit const& kDefender); // </advc.089>
	void setPlotHelp(CvWStringBuffer &szString, CvPlot const& kPlot);
	// <advc.099f> (only for legacy saves)
	void setAlwaysShowPlotCulture(bool bAlwaysShowPlotCulture)
	{
		m_bAlwaysShowPlotCulture = bAlwaysShowPlotCulture;
	} // </advc.099f>
	void setCityBarHelp(CvWStringBuffer &szString, CvCity const& kCity);
	void setRevoltHelp(CvWStringBuffer &szString, CvCity const& kCity); // advc.101
	void setScoreHelp(CvWStringBuffer &szString, PlayerTypes ePlayer);

	void parseTraits(CvWStringBuffer &szHelpString, TraitTypes eTrait, CivilizationTypes eCivilization = NO_CIVILIZATION, bool bDawnOfMan = false);
	DllExport void parseLeaderTraits(CvWStringBuffer &szInfoText, LeaderHeadTypes eLeader = NO_LEADER, CivilizationTypes eCivilization = NO_CIVILIZATION, bool bDawnOfMan = false, bool bCivilopediaText = false);
	DllExport void parseLeaderShortTraits(CvWStringBuffer &szInfoText, LeaderHeadTypes eLeader);
	DllExport void parseCivInfos(CvWStringBuffer &szHelpString, CivilizationTypes eCivilization, bool bDawnOfMan = false, bool bLinks = true);
	// <advc>
	void appendUniqueDesc(CvWStringBuffer& szBuffer, bool bSeparator, bool bDawnOfMan, bool bLinks,
			wchar const* szUniqueDesc, wchar const* szDefaultDesc = NULL); // </advc>
	void parseSpecialistHelp(CvWStringBuffer &szHelpString, SpecialistTypes eSpecialist, CvCity* pCity, bool bCivilopediaText = false);
	void parseFreeSpecialistHelp(CvWStringBuffer &szHelpString, const CvCity& kCity);
	void parsePromotionHelp(CvWStringBuffer &szBuffer, PromotionTypes ePromo, const wchar* pcNewline = NEWLINE);
	void parseSingleCivicRevealHelp(CvWStringBuffer& szBuffer, CivicTypes eCivic); // advc.mnai
	void parseCivicInfo(CvWStringBuffer &szBuffer, CivicTypes eCivic, bool bCivilopediaText = false, bool bPlayerContext = false, bool bSkipName = false);
	void parsePlayerTraits(CvWStringBuffer &szBuffer, PlayerTypes ePlayer);
	void parseLeaderHeadHelp(CvWStringBuffer &szBuffer, PlayerTypes eThisPlayer, PlayerTypes eOtherPlayer);
	// advc.152:
	void parseWarTradesHelp(CvWStringBuffer& szBuffer, PlayerTypes eThisPlayer, PlayerTypes eOtherPlayer);
	void parseLeaderLineHelp(CvWStringBuffer &szBuffer, PlayerTypes eThisPlayer, PlayerTypes eOtherPlayer);
	void parseGreatPeopleHelp(CvWStringBuffer &szBuffer, CvCity const& kCity);
// BUG - Building Additional Great People - start
	bool setBuildingAdditionalGreatPeopleHelp(CvWStringBuffer &szBuffer, const CvCity& city, const CvWString& szStart, bool bStarted = false);
// BUG - Building Additional Great People - end
	void parseGreatGeneralHelp(CvWStringBuffer &szBuffer, CvPlayer& kPlayer);
    void parseGreatSpyHelp(CvWStringBuffer &szBuffer, CvPlayer& kPlayer); // doc
    void parsePaganReligionHelp(CvWStringBuffer &szBuffer, PaganReligionTypes ePaganReligion); // doc

	void setTechHelp(CvWStringBuffer &szBuffer, TechTypes eTech, bool bCivilopediaText = false, bool bPlayerContext = false, bool bStrategyText = false, bool bTreeInfo = true, TechTypes eFromTech = NO_TECH);
// BULL - Trade Denial - start
	void setTechTradeHelp(CvWStringBuffer &szBuffer, TechTypes eTech,
			PlayerTypes eTradePlayer, bool bCivilopediaText = false,
			bool bPlayerContext = false, bool bStrategyText = false,
			bool bTreeInfo = true, TechTypes eFromTech = NO_TECH);
// BULL - Trade Denial - end
	// advc.004a:
	void setDiscoverPathHelp(CvWStringBuffer& szBuffer, UnitTypes eUnit);
	// <advc.ctr>
	void setCityTradeHelp(CvWStringBuffer& szBuffer, CvCity const& kCity,
			PlayerTypes eWhoTo, bool bListMore, bool bReason = true); // </advc.ctr>
	void setBasicUnitHelp(CvWStringBuffer &szBuffer, UnitTypes eUnit, bool bCivilopediaText = false);
	void setUnitHelp(CvWStringBuffer &szBuffer, UnitTypes eUnit, bool bCivilopediaText = false, bool bStrategyText = false, bool bTechChooserText = false, CvCity* pCity = NULL);
	void setBuildingHelp(CvWStringBuffer &szBuffer, BuildingTypes eBuilding, bool bCivilopediaText = false, bool bStrategyText = false, bool bTechChooserText = false, CvCity* pCity = NULL);
// BUG - Building Additional Happiness - start
	void setBuildingNetEffectsHelp(CvWStringBuffer &szBuffer, BuildingTypes eBuilding, CvCity const* pCity);
	void setBuildingHelpActual(CvWStringBuffer &szBuffer, BuildingTypes eBuilding, bool bCivilopediaText = false, bool bStrategyText = false, bool bTechChooserText = false, CvCity* pCity = NULL, bool bActual = true);
// BUG - Building Additional Happiness - end
	void setProjectHelp(CvWStringBuffer &szBuffer, ProjectTypes eProject, bool bCivilopediaText = false, CvCity* pCity = NULL);
	void setProcessHelp(CvWStringBuffer &szBuffer, ProcessTypes eProcess);
	// BULL - Production Decay: (advc.094)
	void setProductionDecayHelp(CvWStringBuffer &szBuffer, int iTurnsLeft, int iThreshold, int iDecay, bool bProducing);
	void setGoodHealthHelp(CvWStringBuffer &szBuffer, CvCity const& kCity);
	void setBadHealthHelp(CvWStringBuffer &szBuffer, CvCity const& kCity);
	// <advc.004b>
	void setFoundHealthHelp(CvWStringBuffer& szBuffer, CvPlot const& kCityPlot);
	void setFoundCostHelp(CvWStringBuffer& szBuffer, CvPlot const& kCityPlot);
	void setHomePlotYieldHelp(CvWStringBuffer& szBuffer, CvPlot const& kCityPlot);
	// </advc.004b>
// BUG - Building Additional Health - start
	bool setBuildingAdditionalHealthHelp(CvWStringBuffer &szBuffer, const CvCity& city, const CvWString& szStart, bool bStarted = false);
// BUG - Building Additional Health - end
	void setAngerHelp(CvWStringBuffer &szBuffer, CvCity const& kCity);
	void setHappyHelp(CvWStringBuffer &szBuffer, CvCity const& kCity);
// BUG - Building Additional Happiness - start
	bool setBuildingAdditionalHappinessHelp(CvWStringBuffer &szBuffer, const CvCity& kCity, const CvWString& szStart, bool bStarted = false);
// BUG - Building Additional Happiness - end
// BUG - Resumable Value Change Help - start  (advc: unnecessary wrappers removed)
	template<class YieldChanges> // advc.003t
	bool setYieldChangeHelp(CvWStringBuffer &szBuffer,
			const CvWString& szStart, const CvWString& szSpace, const CvWString& szEnd,
			YieldChanges piYieldChange,
			bool bPercent = false, bool bNewLine = true, bool bStarted = false);
	template<class CommerceChanges> // advc.003t
	bool setCommerceChangeHelp(CvWStringBuffer &szBuffer,
			const CvWString& szStart, const CvWString& szSpace, const CvWString& szEnd,
			CommerceChanges piCommerceChange,
			bool bPercent = false, bool bNewLine = true, bool bStarted = false);
	template<class CommercePercentChanges> // advc.003t
	bool setCommerceTimes100ChangeHelp(CvWStringBuffer &szBuffer,
			const CvWString& szStart, const CvWString& szSpace, const CvWString& szEnd,
			CommercePercentChanges piCommerceChange,
			bool bNewLine, bool bStarted = false);
	bool setGoodBadChangeHelp(CvWStringBuffer &szBuffer,
			const CvWString& szStart, const CvWString& szSpace, const CvWString& szEnd,
			int iGood, int iGoodSymbol, int iBad, int iBadSymbol,
			bool bPercent = false, bool bNewLine = false, bool bStarted = false);
	bool setValueChangeHelp(CvWStringBuffer &szBuffer,
			const CvWString& szStart, const CvWString& szSpace, const CvWString& szEnd,
			int iValue, int iSymbol,
			bool bPercent = false, bool bNewLine = false, bool bStarted = false);
	bool setValueTimes100ChangeHelp(CvWStringBuffer &szBuffer,
			const CvWString& szStart, const CvWString& szSpace, const CvWString& szEnd,
			int iValue, int iSymbol,
			bool bNewLine = false, bool bStarted = false);
// BUG - Resumable Value Change Help - end
	void setBonusHelp(CvWStringBuffer &szBuffer, BonusTypes eBonus, bool bCivilopediaText = false, CvCity const* pCity = NULL);
// BULL - Trade Denial - start
	void setBonusTradeHelp(CvWStringBuffer &szBuffer, BonusTypes eBonus,
			bool bCivilopediaText, PlayerTypes eTradePlayer,  bool bImport, 
			bool bForeignAdvisor, CvCity const* pCity = NULL);
// BULL - Trade Denial - end
	// <advc.004w>
	void setBonusExtraHelp(CvWStringBuffer &szBuffer, BonusTypes eBonus,
			bool bCivilopediaText, PlayerTypes eTradePlayer, bool bDiplo, CvCity const* pCity);
	// </advc.004w>  <advc.111>
	bool setPillageHelp(CvWStringBuffer &szBuffer, ImprovementTypes eImprovement);
	bool setPillageHelp(CvWStringBuffer &szBuffer, RouteTypes eRoute); // </advc.111>
	void setReligionHelp(CvWStringBuffer &szBuffer, ReligionTypes eReligion, bool bCivilopedia = false);
	void setReligionHelpCity(CvWStringBuffer &szBuffer, ReligionTypes eReligion, CvCity *pCity, bool bCityScreen = false, bool bForceReligion = false, bool bForceState = false, bool bNoStateReligion = false);
	void setCorporationHelp(CvWStringBuffer &szBuffer, CorporationTypes eCorporation, bool bCivilopedia = false);
	void setCorporationHelpCity(CvWStringBuffer &szBuffer, CorporationTypes eCorporation, CvCity *pCity, bool bCityScreen = false, bool bForceCorporation = false);
	void setPromotionHelp(CvWStringBuffer &szBuffer, PromotionTypes ePromotion, bool bCivilopediaText = false);
	void setUnitCombatHelp(CvWStringBuffer &szBuffer, UnitCombatTypes eUnitCombat);
	void setImprovementHelp(CvWStringBuffer &szBuffer, ImprovementTypes eImprovement, bool bCivilopediaText = false);
	void setTerrainHelp(CvWStringBuffer &szBuffer, TerrainTypes eTerrain, bool bCivilopediaText = false);
	void setFeatureHelp(CvWStringBuffer &szBuffer, FeatureTypes eFeature, bool bCivilopediaText = false);
	// BUG - Building Additional info - start
	bool setBuildingAdditionalYieldHelp(CvWStringBuffer &szBuffer, const CvCity& kCity, YieldTypes eIndex, const CvWString& szStart, bool bStarted = false);
	bool setBuildingAdditionalCommerceHelp(CvWStringBuffer &szBuffer, const CvCity& kCity, CommerceTypes eIndex, const CvWString& szStart, bool bStarted = false);
	bool setBuildingSavedMaintenanceHelp(CvWStringBuffer &szBuffer, const CvCity& kCity, const CvWString& szStart, bool bStarted = false);
	// BUG - Building Additional info - end
	void setProductionHelp(CvWStringBuffer &szBuffer, CvCity const& kCity);  // advc: const city in this function and the next 2
	void setCommerceHelp(CvWStringBuffer &szBuffer, CvCity const& kCity, CommerceTypes eCommerce);
	void setYieldHelp(CvWStringBuffer &szBuffer, CvCity const& kCity, YieldTypes eYield);
	void setConvertHelp(CvWStringBuffer& szBuffer, PlayerTypes ePlayer, ReligionTypes eReligion);
	void setRevolutionHelp(CvWStringBuffer& szBuffer, PlayerTypes ePlayer);
	void setVassalRevoltHelp(CvWStringBuffer& szBuffer, TeamTypes eMaster, TeamTypes eVassal);
	void setEventHelp(CvWStringBuffer& szBuffer, EventTypes eEvent, int iEventTriggeredId, PlayerTypes ePlayer);
	void setTradeRouteHelp(CvWStringBuffer &szBuffer, int iRoute, CvCity* pCity);
	void setEspionageCostHelp(CvWStringBuffer &szBuffer,
			EspionageMissionTypes eMission, PlayerTypes eTargetPlayer,
			CvPlot const* pPlot, int iExtraData, CvUnit const* pSpyUnit);
	void setEspionageMissionHelp(CvWStringBuffer &szBuffer, const CvUnit* pUnit);
	// advc.059:
	void setHealthHappyBuildActionHelp(CvWStringBuffer& szBuffer, CvPlot const& kPlot, BuildTypes eBuild) const;

	void buildObsoleteString(CvWStringBuffer& szBuffer, int iItem, bool bList = false, bool bPlayerContext = false);
	void buildObsoleteBonusString(CvWStringBuffer& szBuffer, int iItem, bool bList = false, bool bPlayerContext = false);
	void buildObsoleteSpecialString(CvWStringBuffer& szBuffer, int iItem, bool bList = false, bool bPlayerContext = false);
	void buildMoveString(CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false);
	void buildFreeUnitString(CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false);
	void buildFeatureProductionString(CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false);
	void buildWorkerRateString(CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false);
	void buildTradeRouteString(CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false);
	void buildHealthRateString(CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false);
	void buildHappinessRateString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false);
	void buildFreeTechString(CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false);
	// advc.500c:
	void buildNoFearForSafetyString(CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false);
	void buildLOSString(CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false);
	void buildMapCenterString(CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false);
	void buildMapRevealString(CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false);
	void buildMapTradeString(CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false);
	void buildTechTradeString(CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false);
	void buildGoldTradeString(CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false);
	void buildOpenBordersString(CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false);
	void buildDefensivePactString(CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false);
	void buildPermanentAllianceString(CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false);
	void buildVassalStateString(CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false);
	void buildBridgeString(CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false);
	void buildIrrigationString(CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false);
	void buildIgnoreIrrigationString(CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false);
	void buildWaterWorkString(CvWStringBuffer &szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false);
	void buildImprovementString(CvWStringBuffer& szBuffer, TechTypes eTech, BuildTypes eBuild, bool bList = false, bool bPlayerContext = false);
	void buildDomainExtraMovesString(CvWStringBuffer& szBuffer, TechTypes eTech, DomainTypes eDomain, bool bList = false, bool bPlayerContext = false);
	void buildAdjustString(CvWStringBuffer& szBuffer, TechTypes eTech, CommerceTypes eCommerce, bool bList = false, bool bPlayerContext = false);
	void buildTerrainTradeString(CvWStringBuffer& szBuffer, TechTypes eTech, TerrainTypes eTerrain, bool bList = false, bool bPlayerContext = false);
	void buildRiverTradeString(CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false);
	void buildSpecialBuildingString(CvWStringBuffer& szBuffer, TechTypes eTech, SpecialBuildingTypes eSpecial, bool bList = false, bool bPlayerContext = false);
	void buildYieldChangeString(CvWStringBuffer& szBuffer, TechTypes eTech, ImprovementTypes eImprov, bool bList = false, bool bPlayerContext = false);
	bool buildBonusRevealString(CvWStringBuffer& szBuffer, TechTypes eTech, BonusTypes eBonus, bool bFirst, bool bList = false, bool bPlayerContext = false);
	bool buildCivicRevealString(CvWStringBuffer& szBuffer, TechTypes eTech, CivicTypes eCivic, bool bFirst, bool bList = false, bool bPlayerContext = false);
	bool buildBonusTradeString(CvWStringBuffer& szBuffer, TechTypes eTech, BonusTypes eBonusType, bool bFirst, bool bList = false, bool bPlayerContext = false ); // doc
	bool buildProcessInfoString(CvWStringBuffer& szBuffer, TechTypes eTech, ProcessTypes eProcess, bool bFirst, bool bList = false, bool bPlayerContext = false);
	bool buildFoundReligionString(CvWStringBuffer& szBuffer, TechTypes eTech, ReligionTypes eReligion, bool bFirst, bool bList = false, bool bPlayerContext = false);
	bool buildFoundCorporationString(CvWStringBuffer& szBuffer, TechTypes eTech, CorporationTypes eCorp, bool bFirst, bool bList = false, bool bPlayerContext = false);
	bool buildPromotionString(CvWStringBuffer& szBuffer, TechTypes eTech, PromotionTypes ePromotion, bool bFirst, bool bList = false, bool bPlayerContext = false);
	void buildHintsList(CvWStringBuffer& szBuffer);
	void buildBuildingRequiresString(CvWStringBuffer& szBuffer, BuildingTypes eBuilding, bool bCivilopediaText, bool bTechChooserText, const CvCity* pCity);
	// <advc.179>
	void buildBuildingReligionYieldString(CvWStringBuffer& szBuffer,
			CvBuildingInfo const& kBuilding); // </advc.179>

	DllExport void buildStabilityParameterString(CvWStringBuffer& szBuffer, int iStabilityCategory); // doc
	DllExport void buildStabilityString(CvWStringBuffer& szBuffer, int iStabilityChange); // doc

	DllExport void buildCityBillboardIconString( CvWStringBuffer& szBuffer, CvCity* pCity);
	DllExport void buildCityBillboardCityNameString( CvWStringBuffer& szBuffer, CvCity* pCity);
	DllExport void buildCityBillboardProductionString( CvWStringBuffer& szBuffer, CvCity* pCity);
	DllExport void buildCityBillboardCitySizeString( CvWStringBuffer& szBuffer, CvCity* pCity, const NiColorA& kColor);
	DllExport void getCityBillboardFoodbarColors(CvCity* pCity, std::vector<NiColorA>& aColors);
	DllExport void getCityBillboardProductionbarColors(CvCity* pCity, std::vector<NiColorA>& aColors);

	void buildSingleLineTechTreeString(CvWStringBuffer &szBuffer, TechTypes eTech, bool bPlayerContext);
	void buildTechTreeString(CvWStringBuffer &szBuffer, TechTypes eTech, bool bPlayerContext, TechTypes eFromTech);
	// advc.034:
	void buildDisengageString(CvWString& szString, PlayerTypes ePlayer, PlayerTypes eOther);

	void getWarplanString(CvWStringBuffer& szString, WarPlanTypes eWarPlan);
	void getAttitudeString(CvWStringBuffer& szBuffer, PlayerTypes ePlayer, PlayerTypes eTargetPlayer,
			bool bConstCache = false); // advc.sha
	// <advc>
	void appendToAttitudeBreakdown(CvWStringBuffer& szBreakdown, int iPass,
			int iAttitudeChange, int& iTotal,
			char const* szTextKey, char const* szTextKeyAlt = NULL); // </advc>
	void getVassalInfoString(CvWStringBuffer& szBuffer, PlayerTypes ePlayer); // K-Mod
	void getWarWearinessString(CvWStringBuffer& szBuffer, PlayerTypes ePlayer, PlayerTypes eTargetPlayer) const; // K-Mod
	//void getEspionageString(CvWStringBuffer& szBuffer, PlayerTypes ePlayer, PlayerTypes eTargetPlayer);
	void getTradeString(CvWStringBuffer& szBuffer, const TradeData& tradeData,
			PlayerTypes ePlayer1, PlayerTypes ePlayer2,
			int iTurnsToCancel = -1); // advc.004w
	void getDealString(CvWStringBuffer& szString, /* advc: const */ CvDeal const& kDeal,
			PlayerTypes ePlayerPerspective = NO_PLAYER,
			bool bCancel = false); // advc.004w
	//void getDealString(...); // advc: Merged into the above
	void getActiveDealsString(CvWStringBuffer& szString, PlayerTypes eThisPlayer, PlayerTypes eOtherPlayer,
			bool bExcludeDual = false); // advc.087
	void getOtherRelationsString(CvWStringBuffer& szString, PlayerTypes eThisPlayer, PlayerTypes eOtherPlayer);

	void buildFinanceInflationString(CvWStringBuffer& szDetails, PlayerTypes ePlayer);
	void buildFinanceUnitCostString(CvWStringBuffer& szDetails, PlayerTypes ePlayer);
	void buildFinanceAwaySupplyString(CvWStringBuffer& szDetails, PlayerTypes ePlayer);
	void buildFinanceCityMaintString(CvWStringBuffer& szDetails, PlayerTypes ePlayer);
	void buildFinanceCivicUpkeepString(CvWStringBuffer& szDetails, PlayerTypes ePlayer);
	void buildFinanceForeignIncomeString(CvWStringBuffer& szDetails, PlayerTypes ePlayer);

	DllExport void getTradeScreenTitleIcon(CvString& szButton, CvWidgetDataStruct& widgetData, PlayerTypes ePlayer);
	DllExport void getTradeScreenIcons(std::vector< std::pair<CvString, CvWidgetDataStruct> >& aIconInfos, PlayerTypes ePlayer);
	DllExport void getTradeScreenHeader(CvWString& szHeader, PlayerTypes ePlayer, PlayerTypes eOtherPlayer, bool bAttitude);
	// BULL - Finance Advisor - start
	void buildDomesticTradeString(CvWStringBuffer& szDetails, PlayerTypes ePlayer);
	void buildForeignTradeString(CvWStringBuffer& szDetails, PlayerTypes ePlayer);
	void buildFinanceSpecialistGoldString(CvWStringBuffer& szBuffer, PlayerTypes ePlayer);
	// BULL - Finance Advisor - end  // BULL - Trade Hover - start
	void buildTradeString(CvWStringBuffer& szBuffer, PlayerTypes ePlayer,
			PlayerTypes eWithPlayer = NO_PLAYER, bool bDomestic = true,
			bool bForeign = true, bool bHeading = true);
	// BULL - Trade Hover - end
	// BULL - Leaderhead Relations - start
	void parseLeaderHeadRelationsHelp(CvWStringBuffer &szBuffer,
			PlayerTypes eThisPlayer, PlayerTypes eOtherPlayer);
	// BULL - Leaderhead Relations - end
	// BULL - Food Rate Hover:
	void setFoodHelp(CvWStringBuffer &szBuffer, CvCity const& kCity);
	// <advc.154>
	void setCycleUnitHelp(CvWStringBuffer &szBuffer, bool bWorkers, CvUnit const& kUnit);
    void setUnselectUnitHelp(CvWStringBuffer &szBuffer); // </advc.154>
    void setWonderLimitHelp(CvWStringBuffer &szBuffer, CvCity& city, int iWonderType); // doc
    void setSatelliteLimitHelp(CvWStringBuffer& szBuffer, CvCity& city); // doc
	DllExport void getGlobeLayerName(GlobeLayerTypes eType, int iOption, CvWString& strName);

	DllExport void getPlotHelp(CvPlot* pMouseOverPlot, CvCity* pCity, CvPlot* pFlagPlot, bool bAlt, CvWStringBuffer& strHelp);
	void getRebasePlotHelp(CvPlot const& kPlot, CvUnit& kHeadSelectedUnit, CvWString& szHelp);
	void getNukePlotHelp(CvPlot const& kPlot, CvUnit& kNuke, CvWString& szHelp);
	// <advc.004c>
	void getAirBombPlotHelp(CvPlot const& kPlot, CvUnit& kHeadSelectedUnit, CvWString& szHelp);
	void getAirStrikePlotHelp(CvPlot const& kPlot, CvUnit& kHeadSelectedUnit, CvWString& szHelp);
	void getParadropPlotHelp(CvPlot const& kPlot, CvUnit& kHeadSelectedUnit, CvWString& szHelp); // </advc.004c>
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
	// BULL - Leaderhead Relations - start  // advc: private
	void getAllRelationsString(CvWStringBuffer& szString, TeamTypes eThisTeam);
	void getActiveTeamRelationsString(CvWStringBuffer& szString, TeamTypes eThisTeam);
	void getOtherRelationsString(CvWStringBuffer& szString, TeamTypes eThisTeam,
			TeamTypes eOtherTeam, TeamTypes eSkipTeam);
	// BULL - Leaderhead Relations - end
	void setCityPlotYieldValueString(CvWStringBuffer &szString, CvCityAI* pCity,
			//bool bAvoidGrowth, bool bIgnoreGrowth, bool bIgnoreFood = false);
			int iPlotIndex, bool bIgnoreFood, int iGrowthValue);
	void setYieldValueString(CvWStringBuffer &szString, int iValue, bool bActive = false, bool bMakeWhitespace = false);
	// <advc.059>
	void setPlotHealthHappyHelp(CvWStringBuffer& szBuffer, CvPlot const& kPlot) const;
	void setHealthChangeBuildActionHelp(CvWStringBuffer& szBuffer, int iChange,
			int iChangePercent, int iIcon) const; // </advc.059>
	// <advc>
	void appendCombatModifiers(CvWStringBuffer& szBuffer, CvPlot const& kPlot,
			CvUnit const& kAttacker, CvUnit const& kDefender,
			bool bAttackModifier, bool bACOEnabled,
			bool bOnlyGeneric = false, bool bOnlyNonGeneric = false);
	struct CombatModifierOutputParams
	{
		bool m_bAttackModifier;
		bool m_bGenericModifier;
		bool m_bACOEnabled;
	};
	void appendCombatModifier(CvWStringBuffer& szBuffer, int iModifier,
			CombatModifierOutputParams const& kParams, char const* szTextKey,
			wchar const* szTextArg = NULL);
	void appendFirstStrikes(CvWStringBuffer& szBuffer,
			CvUnit const& kFirstStriker, CvUnit const& kOther, bool bNegativeColor);
	void setPlotListHelpDebug(CvWStringBuffer& szString, CvPlot const& kPlot);
	// </advc>
	// <advc.004w>
	template<OrderTypes eORDER, typename ORDER_DATA1, typename ORDER_DATA2>
	void setProductionSpeedHelp(CvWStringBuffer& szBuffer,
			ORDER_DATA1 eData1, ORDER_DATA2 eData2,
			CvCity const* pCity, bool bCivilopediaText); // </advc.004w>
	// <advc.001>
	void setSpecialistLink(CvWString& szBuffer, SpecialistTypes eSpecialist,
			bool bPlural = false);
	void setCorporationLink(CvWString& szBuffer, CorporationTypes eCorp); // </advc.001>
	// <advc.135c>
	void setPlotHelpDebug(CvWStringBuffer& szString, CvPlot const& kPlot);
	void setPlotHelpDebug_Ctrl(CvWStringBuffer& szString, CvPlot const& kPlot);
	void setPlotHelpDebug_ShiftOnly(CvWStringBuffer& szString, CvPlot const& kPlot);
	void setPlotHelpDebug_AltOnly(CvWStringBuffer& szString, CvPlot const& kPlot);
	void setPlotHelpDebug_ShiftAltOnly(CvWStringBuffer& szString, CvPlot const& kPlot);
	// </advc.135c>
	// advc.910:
	void setResearchModifierHelp(CvWStringBuffer& szBuffer, TechTypes eTech);
	// <advc.061>
	void setPlotListHelpPerOwner(CvWStringBuffer& szString, CvPlot const& kPlot,
			bool bIndicator, bool bShort);
	void appendUnitOwnerHeading(CvWStringBuffer& szString, PlayerTypes eOwner,
			int iArmy, int iNavy, int iAir, int iTotal, bool bCollapsed = false);
	void appendUnitTypeAggregated(CvWStringBuffer& szString,
			std::vector<CvUnit const*> const& ownerUnits,
			UnitTypes eUnit, CvPlot const& kPlot, bool bIndicator);
	void appendAverageStrength(CvWStringBuffer& szString, int iSumMaxStrengthTimes100,
			int iSumStrengthTimes100, int iUnits);
	// For std::sort
	  static CvPlot const* m_pHelpPlot;
	  static bool listFirstUnitBeforeSecond(CvUnit const* pFirst, CvUnit const* pSecond);
	  static bool listFirstUnitTypeBeforeSecond(UnitTypes eFirst, UnitTypes eSecond);
	// </advc.061>
	std::vector<int*> m_apbPromotion;
	bool m_bAlwaysShowPlotCulture; // advc.099f
};

// Singleton Accessor
#define GAMETEXT CvGameTextMgr::GetInstance()

#endif
