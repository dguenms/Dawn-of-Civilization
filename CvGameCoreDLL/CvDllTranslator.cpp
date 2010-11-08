#include "CvGameCoreDLL.h"
#include "CvDllTranslator.h"

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

	aIconMap[L"[ICON_GOLD]"] = std::wstring(1, (wchar)GC.getCommerceInfo(COMMERCE_GOLD).getChar());
	aIconMap[L"[ICON_RESEARCH]"] = std::wstring(1, (wchar)GC.getCommerceInfo(COMMERCE_RESEARCH).getChar());
	aIconMap[L"[ICON_CULTURE]"] = std::wstring(1, (wchar)GC.getCommerceInfo(COMMERCE_CULTURE).getChar());
	aIconMap[L"[ICON_ESPIONAGE]"] = std::wstring(1, (wchar)GC.getCommerceInfo(COMMERCE_ESPIONAGE).getChar());

	aIconMap[L"[ICON_FOOD]"] = std::wstring(1, (wchar)GC.getYieldInfo(YIELD_FOOD).getChar());
	aIconMap[L"[ICON_PRODUCTION]"] = std::wstring(1, (wchar)GC.getYieldInfo(YIELD_PRODUCTION).getChar());
	aIconMap[L"[ICON_COMMERCE]"] = std::wstring(1, (wchar)GC.getYieldInfo(YIELD_COMMERCE).getChar());

	//create color map
	aColorMap[L"[COLOR_REVERT]"] = CvWString(L"</color>");
	for(int i=0; i < GC.getNumColorInfos(); i++)
	{
		const NiColorA& color = GC.getColorInfo((ColorTypes) i).getColor();
		CvWString colorType(GC.getColorInfo((ColorTypes) i).getType());
		CvWString wideColorType;
		wideColorType.Format(L"[%s]", colorType.GetCString());
		CvWString colorOut;
		colorOut.Format(L"<color=%i,%i,%i,%i>", (int) (color.r * 255), (int) (color.g * 255), (int) (color.b * 255), (int) (color.a * 255));
		aColorMap[wideColorType.GetCString()] = colorOut;
	}
}

bool CvDllTranslator::replaceOur(const CvWString& szKey, int iForm, CvWString& szReplacement)
{
	CvPlayerAI& player = GET_PLAYER((PlayerTypes) gDLL->getDiplomacyPlayer());
	if (szKey == L"[OUR_NAME")
	{
		szReplacement = player.getName(iForm);
	}
	else if (szKey == L"[OUR_EMPIRE")
	{
		szReplacement = player.getCivilizationDescription(iForm);
	}
	else if(szKey == L"[OUR_CIV_SHORT")
	{
		szReplacement = player.getCivilizationShortDescription(iForm);
	}
	else if(szKey == L"[OUR_CIV_ADJ")
	{
		szReplacement = player.getCivilizationAdjective(iForm);
	}
	else if(szKey == L"[OUR_STATE_RELIGION")
	{
		szReplacement = player.getStateReligionName(iForm);
	}
	else if(szKey == L"[OUR_BEST_UNIT")
	{
		szReplacement = player.getBestAttackUnitName(iForm);
	}
	else if(szKey == L"[OUR_WORST_ENEMY")
	{
		szReplacement = player.getWorstEnemyName();
	}
	else
	{
		FAssertMsg(false, "Unknown Diplomacy String");
		return false;
	}
	return true;
}

bool CvDllTranslator::replaceCt(const CvWString& szKey, int iForm, CvWString& szReplacement)
{
	CvPlayerAI& player = GET_PLAYER(GC.getGameINLINE().getActivePlayer());
	if (szKey == L"[CT_NAME")
	{
		szReplacement = player.getName(iForm);
	}
	else if (szKey == L"[CT_EMPIRE")
	{
		szReplacement = player.getCivilizationDescription(iForm);
	}
	else if(szKey == L"[CT_CIV_SHORT")
	{
		szReplacement = player.getCivilizationShortDescription(iForm);
	}
	else if(szKey == L"[CT_CIV_ADJ")
	{
		szReplacement = player.getCivilizationAdjective(iForm);
	}
	else if(szKey == L"[CT_STATE_RELIGION")
	{
		szReplacement = player.getStateReligionName(iForm);
	}
	else if(szKey == L"[CT_BEST_UNIT")
	{
		szReplacement = player.getBestAttackUnitName(iForm);
	}
	else if(szKey == L"[CT_WORST_ENEMY")
	{
		szReplacement = player.getWorstEnemyName();
	}
	else
	{
		FAssertMsg(false, "Unknown Diplomacy String");
		return false;
	}
	return true;
}

