#include "CvGameCoreDLL.h"
#include "CyGameTextMgr.h"

//
// published python interface for CyGameTextMgr
//

void CyGameTextMgrInterface()
{
	OutputDebugString("Python Extension Module - CyTextMgr\n");

	python::class_<CyGameTextMgr>("CyGameTextMgr")
		.def("isNone", &CyGameTextMgr::isNone, "bool () - Checks to see if pointer points to a real object")

		.def("Reset", &CyGameTextMgr::Reset, "void ()")
		.def("getTimeStr", &CyGameTextMgr::getTimeStr, "wstring (int iGameTurn, bool bSave)")
		.def("getDateStr", &CyGameTextMgr::getDateStr, "wstring (int iGameTurn, bool bSave, int /*CalendarTypes*/ eCalendar, int iStartYear, int /*GameSpeedTypes*/ eSpeed)")
		.def("getInterfaceTimeStr", &CyGameTextMgr::getInterfaceTimeStr, "wstring (int /*PlayerTypes*/ iPlayer)")
		.def("getGoldStr", &CyGameTextMgr::getGoldStr, "wstring (int /*PlayerTypes*/ iPlayer)")
		.def("getResearchStr", &CyGameTextMgr::getResearchStr, "wstring (int /*PlayerTypes*/ iPlayer)")
		.def("getOOSSeeds", &CyGameTextMgr::getOOSSeeds, "wstring (int /*PlayerTypes*/ iPlayer)")
		.def("getNetStats", &CyGameTextMgr::getNetStats, "wstring (int /*PlayerTypes*/ iPlayer)")
		.def("getTechHelp", &CyGameTextMgr::getTechHelp, "wstring (int iTech, bool bCivilopediaText, bool bPlayerContext, bool bStrategyText, bool bTreeInfo, int iFromTech)")
		.def("getUnitHelp", &CyGameTextMgr::getUnitHelp, "wstring (int iUnit, bool bCivilopediaText, bool bStrategyText, bool bTechChooserText, CyCity* pCity)")
		.def("getSpecificUnitHelp", &CyGameTextMgr::getSpecificUnitHelp, "wstring (CyUnit* pUnit, bool bOneLine, bool bShort)")
		.def("getBuildingHelp", &CyGameTextMgr::getBuildingHelp, "wstring (int iBuilding, bool bCivilopediaText, bool bStrategyText, bool bTechChooserText, CyCity* pCity)")
		.def("getProjectHelp", &CyGameTextMgr::getProjectHelp, "wstring (int iProject, bool bCivilopediaText, CyCity* pCity)")
		.def("getPromotionHelp", &CyGameTextMgr::getPromotionHelp, "wstring (int iPromotion, bool bCivilopediaText)")
		.def("getBonusHelp", &CyGameTextMgr::getBonusHelp, "wstring (int iBonus, bool bCivilopediaText)")
		.def("getReligionHelpCity", &CyGameTextMgr::getReligionHelpCity, "wstring (int iReligion, CyCity* pCity, bool bCityScreen, bool bForceReligion, bool bForceState)")
		.def("getCorporationHelpCity", &CyGameTextMgr::getCorporationHelpCity, "wstring (int iCorporation, CyCity* pCity, bool bCityScreen, bool bForceCorporation)")
		.def("getImprovementHelp", &CyGameTextMgr::getImprovementHelp, "wstring (int iImprovement, bool bCivilopediaText)")
		.def("getTerrainHelp", &CyGameTextMgr::getTerrainHelp, "wstring (int iTerrain, bool bCivilopediaText)")
		.def("getFeatureHelp", &CyGameTextMgr::getFeatureHelp, "wstring (int iFeature, bool bCivilopediaText)")
		.def("parseCivicInfo", &CyGameTextMgr::parseCivicInfo, "wstring (int /*CivicTypes*/ iCivicType, bool bCivilopediaText, bool bPlayerContext, bool bSkipName)")
		.def("parseReligionInfo", &CyGameTextMgr::parseReligionInfo, "wstring (int /*ReligionTypes*/ iReligionType, bool bCivilopediaText)")
		.def("parseCorporationInfo", &CyGameTextMgr::parseCorporationInfo, "wstring (int /*CorporationTypes*/ iCorporationType, bool bCivilopediaText)")
		.def("parseCivInfos", &CyGameTextMgr::parseCivInfos, "wstring (int /*CivilizationTypes*/ iCivilization, bool bDawnOfMan)")
		.def("parseLeaderTraits", &CyGameTextMgr::parseLeaderTraits, "wstring (int /*LeaderHeadTypes*/ iLeader, int /*CivilizationTypes*/ iCivilization, bool bDawnOfMan, bool bCivilopediaText)")
		.def("getSpecialistHelp", &CyGameTextMgr::getSpecialistHelp, "wstring (TradeData* pTradeData, int iPlayer1, int iPlayer2)")
		.def("getTradeString", &CyGameTextMgr::getTradeString, "wstring (int iSpecialist, bool bCivilopediaText)")
		.def("buildHintsList", &CyGameTextMgr::buildHintsList, "wstring ()")
		.def("getAttitudeString", &CyGameTextMgr::getAttitudeString, "wstring (int iPlayer, int iTargetPlayer)")
		.def("setConvertHelp", &CyGameTextMgr::setConvertHelp, "wstring (int iPlayer, int iReligion)")
		.def("setRevolutionHelp", &CyGameTextMgr::setRevolutionHelp, "wstring (int iPlayer)")
		.def("setVassalRevoltHelp", &CyGameTextMgr::setVassalRevoltHelp, "wstring (int iMaster, int iVassal)")
		.def("getActiveDealsString", &CyGameTextMgr::getActiveDealsString, "wstring (int iThisPlayer, int iOtherPlayer)")
		.def("getDealString", &CyGameTextMgr::getDealString, "wstring (CyDeal* pDeal, int iPlayerPerspective)")
	;
}
