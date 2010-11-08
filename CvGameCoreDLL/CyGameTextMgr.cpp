//
// Python wrapper class for CyGameTextMgr 
// 
#include "CvGameCoreDLL.h"
#include "CvGameTextMgr.h"
#include "CyGameTextMgr.h"
#include "CyCity.h"
#include "CyDeal.h"
#include "CyUnit.h"

CyGameTextMgr::CyGameTextMgr() : 
m_pGameTextMgr(NULL)
{
	m_pGameTextMgr = &CvGameTextMgr::GetInstance();
}

CyGameTextMgr::CyGameTextMgr(CvGameTextMgr* pGameTextMgr) : 
m_pGameTextMgr(m_pGameTextMgr)
{}

void CyGameTextMgr::Reset()
{
	GAMETEXT.Reset();
}

std::wstring CyGameTextMgr::getTimeStr(int iGameTurn, bool bSave)
{
	CvWString str;
	GAMETEXT.setTimeStr(str, iGameTurn, bSave);
	return str;
}

std::wstring CyGameTextMgr::getDateStr(int iGameTurn, bool bSave, int /*CalendarTypes*/ eCalendar, int iStartYear, int /*GameSpeedTypes*/ eSpeed)
{
	CvWString str;
	GAMETEXT.setDateStr(str, iGameTurn, bSave, (CalendarTypes)eCalendar, iStartYear, (GameSpeedTypes)eSpeed);
	return str;
}

std::wstring CyGameTextMgr::getInterfaceTimeStr(int /*PlayerTypes*/ iPlayer)
{
	CvWString szBuffer;
	GAMETEXT.setInterfaceTime(szBuffer, ((PlayerTypes)iPlayer));
	return szBuffer;
}

std::wstring CyGameTextMgr::getGoldStr(int /*PlayerTypes*/ iPlayer)
{
	CvWString szBuffer;
	GAMETEXT.setGoldStr(szBuffer, ((PlayerTypes)iPlayer));
	return szBuffer;
}

std::wstring CyGameTextMgr::getResearchStr(int /*PlayerTypes*/ iPlayer)
{
	CvWString szBuffer;
	GAMETEXT.setResearchStr(szBuffer, ((PlayerTypes)iPlayer));
	return szBuffer;
}

std::wstring CyGameTextMgr::getOOSSeeds(int /*PlayerTypes*/ iPlayer)
{
	CvWString szBuffer;
	GAMETEXT.setOOSSeeds(szBuffer, ((PlayerTypes)iPlayer));
	return szBuffer;
}

std::wstring CyGameTextMgr::getNetStats(int /*PlayerTypes*/ iPlayer)
{
	CvWString szBuffer;
	GAMETEXT.setNetStats(szBuffer, ((PlayerTypes)iPlayer));
	return szBuffer;
}

std::wstring CyGameTextMgr::getTechHelp(int iTech, bool bCivilopediaText, bool bPlayerContext, bool bStrategyText, bool bTreeInfo, int iFromTech)
{
	CvWStringBuffer szBuffer;
	GAMETEXT.setTechHelp(szBuffer, (TechTypes)iTech, bCivilopediaText, bPlayerContext, bStrategyText, bTreeInfo, (TechTypes)iFromTech);
	return szBuffer.getCString();
}

std::wstring CyGameTextMgr::getUnitHelp(int iUnit, bool bCivilopediaText, bool bStrategyText, bool bTechChooserText, CyCity* pCity)
{
	CvWStringBuffer szBuffer;
	GAMETEXT.setUnitHelp(szBuffer, (UnitTypes)iUnit, bCivilopediaText, bStrategyText, bTechChooserText, ((pCity != NULL) ? pCity->getCity() : NULL));
	return szBuffer.getCString();
}

std::wstring CyGameTextMgr::getSpecificUnitHelp(CyUnit* pUnit, bool bOneLine, bool bShort)
{
	CvWStringBuffer szBuffer;
	if (pUnit && pUnit->getUnit())
	{
		GAMETEXT.setUnitHelp(szBuffer, pUnit->getUnit(), bOneLine, bShort);
	}
	return szBuffer.getCString();
}

std::wstring CyGameTextMgr::getBuildingHelp(int iBuilding, bool bCivilopediaText, bool bStrategyText, bool bTechChooserText, CyCity* pCity)
{
	CvWStringBuffer szBuffer;
	GAMETEXT.setBuildingHelp(szBuffer, (BuildingTypes)iBuilding, bCivilopediaText, bStrategyText, bTechChooserText, ((pCity != NULL) ? pCity->getCity() : NULL));
	return szBuffer.getCString();
}

std::wstring CyGameTextMgr::getProjectHelp(int iProject, bool bCivilopediaText, CyCity* pCity)
{
	CvWStringBuffer szBuffer;
	GAMETEXT.setProjectHelp(szBuffer, (ProjectTypes)iProject, bCivilopediaText, ((pCity != NULL) ? pCity->getCity() : NULL));
	return szBuffer.getCString();
}

std::wstring CyGameTextMgr::getPromotionHelp(int iPromotion, bool bCivilopediaText)
{
	CvWStringBuffer szBuffer;
	GAMETEXT.setPromotionHelp(szBuffer, (PromotionTypes)iPromotion, bCivilopediaText);
	return szBuffer.getCString();
}

std::wstring CyGameTextMgr::getBonusHelp(int iBonus, bool bCivilopediaText)
{
	CvWStringBuffer szBuffer;
	GAMETEXT.setBonusHelp(szBuffer, (BonusTypes)iBonus, bCivilopediaText);
	return szBuffer.getCString();
}

std::wstring CyGameTextMgr::getReligionHelpCity(int iReligion, CyCity* pCity, bool bCityScreen, bool bForceReligion, bool bForceState, bool bNoStateReligion)
{
	CvWStringBuffer szBuffer;
	GAMETEXT.setReligionHelpCity(szBuffer, (ReligionTypes)iReligion, ((pCity != NULL) ? pCity->getCity() : NULL), bCityScreen, bForceReligion, bForceState, bNoStateReligion);
	return szBuffer.getCString();
}

std::wstring CyGameTextMgr::getCorporationHelpCity(int iCorporation, CyCity* pCity, bool bCityScreen, bool bForceCorporation)
{
	CvWStringBuffer szBuffer;
	GAMETEXT.setCorporationHelpCity(szBuffer, (CorporationTypes)iCorporation, ((pCity != NULL) ? pCity->getCity() : NULL), bCityScreen, bForceCorporation);
	return szBuffer.getCString();
}

std::wstring CyGameTextMgr::getImprovementHelp(int iImprovement, bool bCivilopediaText)
{
	CvWStringBuffer szBuffer;
	GAMETEXT.setImprovementHelp(szBuffer, (ImprovementTypes)iImprovement, bCivilopediaText);
	return szBuffer.getCString();
}

std::wstring CyGameTextMgr::getFeatureHelp(int iFeature, bool bCivilopediaText)
{
	CvWStringBuffer szBuffer;
	GAMETEXT.setFeatureHelp(szBuffer, (FeatureTypes)iFeature, bCivilopediaText);
	return szBuffer.getCString();
}

std::wstring CyGameTextMgr::getTerrainHelp(int iTerrain, bool bCivilopediaText)
{
	CvWStringBuffer szBuffer;
	GAMETEXT.setTerrainHelp(szBuffer, (TerrainTypes)iTerrain, bCivilopediaText);
	return szBuffer.getCString();
}

std::wstring CyGameTextMgr::parseCivicInfo(int /*CivicTypes*/ iCivicType, bool bCivilopediaText, bool bPlayerContext, bool bSkipName)
{
	CvWStringBuffer szBuffer;
	GAMETEXT.parseCivicInfo(szBuffer, (CivicTypes) iCivicType, bCivilopediaText, bPlayerContext, bSkipName);
	return szBuffer.getCString();
}

std::wstring CyGameTextMgr::parseReligionInfo(int /*ReligionTypes*/ iReligionType, bool bCivilopediaText)
{
	CvWStringBuffer szBuffer;
	GAMETEXT.setReligionHelp(szBuffer, (ReligionTypes) iReligionType, bCivilopediaText);
	return szBuffer.getCString();
}

std::wstring CyGameTextMgr::parseCorporationInfo(int /*CorporationTypes*/ iCorporationType, bool bCivilopediaText)
{
	CvWStringBuffer szBuffer;
	GAMETEXT.setCorporationHelp(szBuffer, (CorporationTypes) iCorporationType, bCivilopediaText);
	return szBuffer.getCString();
}

std::wstring CyGameTextMgr::parseCivInfos(int /*CivilizationTypes*/ iCivilization, bool bDawnOfMan)
{
	CvWStringBuffer szBuffer;
	GAMETEXT.parseCivInfos(szBuffer, (CivilizationTypes) iCivilization, bDawnOfMan);
	return szBuffer.getCString();
}

std::wstring CyGameTextMgr::parseLeaderTraits(int /*LeaderHeadTypes*/ iLeader, int /*CivilizationTypes*/ iCivilization, bool bDawnOfMan, bool bCivilopediaText)
{
	CvWStringBuffer szBuffer;
	GAMETEXT.parseLeaderTraits(szBuffer, (LeaderHeadTypes)iLeader, (CivilizationTypes) iCivilization, bDawnOfMan, bCivilopediaText);
	return szBuffer.getCString();
}

std::wstring CyGameTextMgr::getTradeString(TradeData* pTradeData, int iPlayer1, int iPlayer2)
{
	CvWStringBuffer szBuffer;
	if (NULL != pTradeData)
	{
		GAMETEXT.getTradeString(szBuffer, *pTradeData, (PlayerTypes)iPlayer1, (PlayerTypes) iPlayer2);
	}
	return szBuffer.getCString();
}

std::wstring CyGameTextMgr::getSpecialistHelp(int iSpecialist, bool bCivilopediaText)
{
	CvWStringBuffer szBuffer;
	GAMETEXT.parseSpecialistHelp(szBuffer, (SpecialistTypes) iSpecialist, NULL, bCivilopediaText);
	return szBuffer.getCString();
}

std::wstring CyGameTextMgr::buildHintsList()
{
	CvWStringBuffer szBuffer;
	GAMETEXT.buildHintsList(szBuffer);
	return szBuffer.getCString();
}

std::wstring CyGameTextMgr::getAttitudeString(int iPlayer, int iTargetPlayer)
{
	CvWStringBuffer szBuffer;
	GAMETEXT.getAttitudeString(szBuffer, (PlayerTypes)iPlayer, (PlayerTypes) iTargetPlayer);
	return szBuffer.getCString();
}

std::wstring CyGameTextMgr::setConvertHelp(int iPlayer, int iReligion)
{
	CvWStringBuffer szBuffer;
	GAMETEXT.setConvertHelp(szBuffer, (PlayerTypes)iPlayer, (ReligionTypes) iReligion);
	return szBuffer.getCString();
}

std::wstring CyGameTextMgr::setRevolutionHelp(int iPlayer)
{
	CvWStringBuffer szBuffer;
	GAMETEXT.setRevolutionHelp(szBuffer, (PlayerTypes)iPlayer);
	return szBuffer.getCString();
}

std::wstring CyGameTextMgr::setVassalRevoltHelp(int iMaster, int iVassal)
{
	CvWStringBuffer szBuffer;
	GAMETEXT.setVassalRevoltHelp(szBuffer, (TeamTypes)iMaster, (TeamTypes)iVassal);
	return szBuffer.getCString();
}

std::wstring CyGameTextMgr::getActiveDealsString(int iThisPlayer, int iOtherPlayer)
{
	CvWStringBuffer szBuffer;
	GAMETEXT.getActiveDealsString(szBuffer, (PlayerTypes)iThisPlayer, (PlayerTypes)iOtherPlayer);
	return szBuffer.getCString();
}

std::wstring CyGameTextMgr::getDealString(CyDeal* pDeal, int iPlayerPerspective)
{
	CvWStringBuffer szBuffer;
	if (pDeal && pDeal->getDeal())
	{
		GAMETEXT.getDealString(szBuffer, *(pDeal->getDeal()), (PlayerTypes)iPlayerPerspective);
	}
	return szBuffer.getCString();
}
