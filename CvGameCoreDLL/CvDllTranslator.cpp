#include "CvGameCoreDLL.h"
#include "CvDllTranslator.h"
#include "CvGame.h"
#include "CvPlayer.h"

void CvDllTranslator::initializeTags(CvWString& szTagStartIcon, CvWString& szTagStartOur, CvWString& szTagStartCT, CvWString& szTagStartColor, CvWString& szTagStartLink, CvWString& szTagEndLink, CvWString& szEndLinkReplacement, std::map<std::wstring, CvWString>& aIconMap, std::map<std::wstring, CvWString>& aColorMap)
{
	szTagStartIcon = L"[ICON_";
	szTagStartOur = L"[OUR_";
	szTagStartCT = L"[CT_";
	szTagStartColor = L"[COLOR_";
	szTagStartLink = L"[LINK";
	szTagEndLink = L"[\\LINK";
	szEndLinkReplacement = L"</link>";

	//create icons map
	aIconMap[L"[ICON_BULLET]"] = std::wstring(1, (wchar)gDLL->getSymbolID(BULLET_CHAR));
	aIconMap[L"[ICON_HAPPY]"] = std::wstring(1, (wchar)gDLL->getSymbolID(HAPPY_CHAR));
	aIconMap[L"[ICON_UNHAPPY]"] = std::wstring(1, (wchar)gDLL->getSymbolID(UNHAPPY_CHAR));
	aIconMap[L"[ICON_HEALTHY]"] = std::wstring(1, (wchar)gDLL->getSymbolID(HEALTHY_CHAR));
	aIconMap[L"[ICON_UNHEALTHY]"] = std::wstring(1, (wchar)gDLL->getSymbolID(UNHEALTHY_CHAR));
	aIconMap[L"[ICON_STRENGTH]"] = std::wstring(1, (wchar)gDLL->getSymbolID(STRENGTH_CHAR));
	aIconMap[L"[ICON_MOVES]"] = std::wstring(1, (wchar)gDLL->getSymbolID(MOVES_CHAR));
	aIconMap[L"[ICON_RELIGION]"] = std::wstring(1, (wchar)gDLL->getSymbolID(RELIGION_CHAR));
	aIconMap[L"[ICON_STAR]"] = std::wstring(1, (wchar)gDLL->getSymbolID(STAR_CHAR));
	aIconMap[L"[ICON_SILVER_STAR]"] = std::wstring(1, (wchar)gDLL->getSymbolID(SILVER_STAR_CHAR));
	aIconMap[L"[ICON_TRADE]"] = std::wstring(1, (wchar)gDLL->getSymbolID(TRADE_CHAR));
	aIconMap[L"[ICON_DEFENSE]"] = std::wstring(1, (wchar)gDLL->getSymbolID(DEFENSE_CHAR));
	aIconMap[L"[ICON_GREATPEOPLE]"] = std::wstring(1, (wchar)gDLL->getSymbolID(GREAT_PEOPLE_CHAR));
	aIconMap[L"[ICON_BAD_GOLD]"] = std::wstring(1, (wchar)gDLL->getSymbolID(BAD_GOLD_CHAR));
	aIconMap[L"[ICON_BAD_FOOD]"] = std::wstring(1, (wchar)gDLL->getSymbolID(BAD_FOOD_CHAR));
	aIconMap[L"[ICON_EATENFOOD]"] = std::wstring(1, (wchar)gDLL->getSymbolID(EATEN_FOOD_CHAR));
	aIconMap[L"[ICON_GOLDENAGE]"] = std::wstring(1, (wchar)gDLL->getSymbolID(GOLDEN_AGE_CHAR));
	aIconMap[L"[ICON_ANGRYPOP]"] = std::wstring(1, (wchar)gDLL->getSymbolID(ANGRY_POP_CHAR));
	aIconMap[L"[ICON_OPENBORDERS]"] = std::wstring(1, (wchar)gDLL->getSymbolID(OPEN_BORDERS_CHAR));
	aIconMap[L"[ICON_DEFENSIVEPACT]"] = std::wstring(1, (wchar)gDLL->getSymbolID(DEFENSIVE_PACT_CHAR));
	aIconMap[L"[ICON_MAP]"] = std::wstring(1, (wchar)gDLL->getSymbolID(MAP_CHAR));
	aIconMap[L"[ICON_OCCUPATION]"] = std::wstring(1, (wchar)gDLL->getSymbolID(OCCUPATION_CHAR));
	aIconMap[L"[ICON_POWER]"] = std::wstring(1, (wchar)gDLL->getSymbolID(POWER_CHAR));
	aIconMap[L"[ICON_CLEAN_POWER]"] = std::wstring(1, (wchar)gDLL->getSymbolID(CLEAN_POWER_CHAR));
	aIconMap[L"[ICON_SCALES]"] = std::wstring(1, (wchar)gDLL->getSymbolID(SCALES_CHAR));
	aIconMap[L"[ICON_MILITARY]"] = std::wstring(1, (wchar)gDLL->getSymbolID(MILITARY_CHAR));

	aIconMap[L"[ICON_GOLD]"] = std::wstring(1, (wchar)GC.getInfo(COMMERCE_GOLD).getChar());
	aIconMap[L"[ICON_RESEARCH]"] = std::wstring(1, (wchar)GC.getInfo(COMMERCE_RESEARCH).getChar());
	aIconMap[L"[ICON_CULTURE]"] = std::wstring(1, (wchar)GC.getInfo(COMMERCE_CULTURE).getChar());
	aIconMap[L"[ICON_ESPIONAGE]"] = std::wstring(1, (wchar)GC.getInfo(COMMERCE_ESPIONAGE).getChar());

	aIconMap[L"[ICON_FOOD]"] = std::wstring(1, (wchar)GC.getInfo(YIELD_FOOD).getChar());
	aIconMap[L"[ICON_PRODUCTION]"] = std::wstring(1, (wchar)GC.getInfo(YIELD_PRODUCTION).getChar());
	aIconMap[L"[ICON_COMMERCE]"] = std::wstring(1, (wchar)GC.getInfo(YIELD_COMMERCE).getChar());
	// advc.064:
	aIconMap[L"[ICON_CITIZEN]"] = std::wstring(1, (wchar)gDLL->getSymbolID(CITIZEN_CHAR));
	// <advc.002f>
	aIconMap[L"[ICON_GREATGENERAL]"] = std::wstring(1, (wchar)gDLL->getSymbolID(GENERAL_CHAR));
	aIconMap[L"[ICON_AIRPORT]"] = std::wstring(1, (wchar)gDLL->getSymbolID(AIRPORT_CHAR));
	// </advc.002f>
	//create color map
	aColorMap[L"[COLOR_REVERT]"] = CvWString(L"</color>");
	for(int i=0; i < GC.getNumColorInfos(); i++)
	{
		const NiColorA& color = GC.getInfo((ColorTypes) i).getColor();
		CvWString colorType(GC.getInfo((ColorTypes) i).getType());
		CvWString wideColorType;
		wideColorType.Format(L"[%s]", colorType.GetCString());
		CvWString colorOut;
		colorOut.Format(L"<color=%i,%i,%i,%i>", (int) (color.r * 255), (int) (color.g * 255), (int) (color.b * 255), (int) (color.a * 255));
		aColorMap[wideColorType.GetCString()] = colorOut;
	}
}

bool CvDllTranslator::replaceOur(const CvWString& szKey, int iForm, CvWString& szReplacement)
{
	CvPlayer const& kPlayer = GET_PLAYER((PlayerTypes) gDLL->getDiplomacyPlayer());
	if (szKey == L"[OUR_NAME")
	{
		szReplacement = kPlayer.getName(iForm);
	}
	else if (szKey == L"[OUR_EMPIRE")
	{
		szReplacement = kPlayer.getCivilizationDescription(iForm);
	}
	else if(szKey == L"[OUR_CIV_SHORT")
	{
		szReplacement = kPlayer.getCivilizationShortDescription(iForm);
	}
	else if(szKey == L"[OUR_CIV_ADJ")
	{
		szReplacement = kPlayer.getCivilizationAdjective(iForm);
	}
	else if(szKey == L"[OUR_STATE_RELIGION")
	{
		szReplacement = kPlayer.getStateReligionName(iForm);
	}
	else if(szKey == L"[OUR_BEST_UNIT")
	{
		szReplacement = kPlayer.getBestAttackUnitName(iForm);
	}
	else if(szKey == L"[OUR_WORST_ENEMY")
	{
		szReplacement = kPlayer.getWorstEnemyName();
	}
	else
	{
		FErrorMsg("Unknown Diplomacy String");
		return false;
	}
	return true;
}

bool CvDllTranslator::replaceCt(const CvWString& szKey, int iForm, CvWString& szReplacement)
{
	CvPlayer const& kPlayer = GET_PLAYER(GC.getGame().getActivePlayer());
	if (szKey == L"[CT_NAME")
	{
		szReplacement = kPlayer.getName(iForm);
	}
	else if (szKey == L"[CT_EMPIRE")
	{
		szReplacement = kPlayer.getCivilizationDescription(iForm);
	}
	else if(szKey == L"[CT_CIV_SHORT")
	{
		szReplacement = kPlayer.getCivilizationShortDescription(iForm);
	}
	else if(szKey == L"[CT_CIV_ADJ")
	{
		szReplacement = kPlayer.getCivilizationAdjective(iForm);
	}
	else if(szKey == L"[CT_STATE_RELIGION")
	{
		szReplacement = kPlayer.getStateReligionName(iForm);
	}
	else if(szKey == L"[CT_BEST_UNIT")
	{
		szReplacement = kPlayer.getBestAttackUnitName(iForm);
	}
	else if(szKey == L"[CT_WORST_ENEMY")
	{
		szReplacement = kPlayer.getWorstEnemyName();
	}
	else
	{
		FErrorMsg("Unknown Diplomacy String");
		return false;
	}
	return true;
}

