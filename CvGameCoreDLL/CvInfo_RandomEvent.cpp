// advc.003x: Cut from CvInfos.cpp

#include "CvGameCoreDLL.h"
#include "CvInfo_RandomEvent.h"
#include "CvXMLLoadUtility.h"


CvEventInfo::CvEventInfo() :
	m_bQuest(false),
	m_bGlobal(false),
	m_bTeam(false),
	m_bCityEffect(false),
	m_bOtherPlayerCityEffect(false),
	m_bGoldToPlayer(false),
	m_bGoldenAge(false),
	m_bDeclareWar(false),
	m_bDisbandUnit(false),
	m_iGold(0),
	m_iRandomGold(0),
	m_iCulture(0),
	m_iEspionagePoints(0),
	m_iTech(NO_TECH),
	m_iTechPercent(0),
	m_iTechCostPercent(0),
	m_iTechMinTurnsLeft(0),
	m_iPrereqTech(NO_TECH),
	m_iUnitClass(NO_UNITCLASS),
	m_iNumUnits(0),
	m_iUnitExperience(0),
	m_iUnitImmobileTurns(0),
	m_iBuildingClass(NO_BUILDINGCLASS),
	m_iBuildingChange(0),
	m_iHappy(0),
	m_iHealth(0),
	m_iHurryAnger(0),
	m_iHappyTurns(0),
	m_iFood(0),
	m_iFoodPercent(0),
	m_iFeature(NO_FEATURE),
	m_iFeatureChange(0),
	m_iImprovement(NO_IMPROVEMENT),
	m_iImprovementChange(0),
	m_iBonus(NO_BONUS),
	m_iBonusChange(0),
	m_iRoute(NO_ROUTE),
	m_iRouteChange(0),
	m_iBonusRevealed(NO_BONUS),
	m_iBonusGift(NO_BONUS),
	m_iConvertOwnCities(0),
	m_iConvertOtherCities(0),
	m_iMaxNumReligions(-1),
	m_iOurAttitudeModifier(0),
	m_iAttitudeModifier(0),
	m_iTheirEnemyAttitudeModifier(0),
	m_iPopulationChange(0),
	m_iRevoltTurns(0),
	m_iMinPillage(0),
	m_iMaxPillage(0),
	m_iUnitPromotion(NO_PROMOTION),
	m_iFreeUnitSupport(0),
	m_iInflationModifier(0),
	m_iSpaceProductionModifier(0),
	m_iAIValue(0),
	m_piTechFlavorValue(NULL),
	m_piPlotExtraYields(NULL),
	m_piFreeSpecialistCount(NULL),
	m_piAdditionalEventChance(NULL),
	m_piAdditionalEventTime(NULL),
	m_piClearEventChance(NULL),
	m_piUnitCombatPromotions(NULL),
	m_piUnitClassPromotions(NULL)
{}

CvEventInfo::~CvEventInfo()
{
	SAFE_DELETE_ARRAY(m_piTechFlavorValue);
	SAFE_DELETE_ARRAY(m_piPlotExtraYields);
	SAFE_DELETE_ARRAY(m_piFreeSpecialistCount);
	SAFE_DELETE_ARRAY(m_piAdditionalEventChance);
	SAFE_DELETE_ARRAY(m_piAdditionalEventTime);
	SAFE_DELETE_ARRAY(m_piClearEventChance);
	SAFE_DELETE_ARRAY(m_piUnitCombatPromotions);
	SAFE_DELETE_ARRAY(m_piUnitClassPromotions);
}

bool CvEventInfo::isGlobal() const
{
	return m_bGlobal;
}

bool CvEventInfo::isQuest() const
{
	return m_bQuest;
}

bool CvEventInfo::isTeam() const
{
	return m_bTeam;
}

bool CvEventInfo::isCityEffect() const
{
	return m_bCityEffect;
}

bool CvEventInfo::isOtherPlayerCityEffect() const
{
	return m_bOtherPlayerCityEffect;
}

bool CvEventInfo::isGoldToPlayer() const
{
	return m_bGoldToPlayer;
}

bool CvEventInfo::isGoldenAge() const
{
	return m_bGoldenAge;
}

bool CvEventInfo::isDeclareWar() const
{
	return m_bDeclareWar;
}

bool CvEventInfo::isDisbandUnit() const
{
	return m_bDisbandUnit;
}

int CvEventInfo::getGold() const
{
	return m_iGold;
}

int CvEventInfo::getRandomGold() const
{
	return m_iRandomGold;
}

int CvEventInfo::getCulture() const
{
	return m_iCulture;
}

int CvEventInfo::getEspionagePoints() const
{
	return m_iEspionagePoints;
}

int CvEventInfo::getTech() const
{
	return m_iTech;
}

int CvEventInfo::getTechPercent() const
{
	return m_iTechPercent;
}

int CvEventInfo::getTechCostPercent() const
{
	return m_iTechCostPercent;
}

int CvEventInfo::getTechMinTurnsLeft() const
{
	return m_iTechMinTurnsLeft;
}

int CvEventInfo::getPrereqTech() const
{
	return m_iPrereqTech;
}

int CvEventInfo::getUnitClass() const
{
	return m_iUnitClass;
}

int CvEventInfo::getNumUnits() const
{
	return m_iNumUnits;
}

int CvEventInfo::getUnitExperience() const
{
	return m_iUnitExperience;
}

int CvEventInfo::getUnitImmobileTurns() const
{
	return m_iUnitImmobileTurns;
}

int CvEventInfo::getBuildingClass() const
{
	return m_iBuildingClass;
}

int CvEventInfo::getBuildingChange() const
{
	return m_iBuildingChange;
}

int CvEventInfo::getHappy() const
{
	return m_iHappy;
}

int CvEventInfo::getHealth() const
{
	return m_iHealth;
}

int CvEventInfo::getHurryAnger() const
{
	return m_iHurryAnger;
}

int CvEventInfo::getHappyTurns() const
{
	return m_iHappyTurns;
}

int CvEventInfo::getFood() const
{
	return m_iFood;
}

int CvEventInfo::getFoodPercent() const
{
	return m_iFoodPercent;
}

int CvEventInfo::getFeature() const
{
	return m_iFeature;
}

int CvEventInfo::getFeatureChange() const
{
	return m_iFeatureChange;
}

int CvEventInfo::getImprovement() const
{
	return m_iImprovement;
}

int CvEventInfo::getImprovementChange() const
{
	return m_iImprovementChange;
}

int CvEventInfo::getBonus() const
{
	return m_iBonus;
}

int CvEventInfo::getBonusChange() const
{
	return m_iBonusChange;
}

int CvEventInfo::getRoute() const
{
	return m_iRoute;
}

int CvEventInfo::getRouteChange() const
{
	return m_iRouteChange;
}

int CvEventInfo::getBonusRevealed() const
{
	return m_iBonusRevealed;
}

int CvEventInfo::getBonusGift() const
{
	return m_iBonusGift;
}

int CvEventInfo::getConvertOwnCities() const
{
	return m_iConvertOwnCities;
}

int CvEventInfo::getConvertOtherCities() const
{
	return m_iConvertOtherCities;
}

int CvEventInfo::getMaxNumReligions() const
{
	return m_iMaxNumReligions;
}

int CvEventInfo::getOurAttitudeModifier() const
{
	return m_iOurAttitudeModifier;
}

int CvEventInfo::getAttitudeModifier() const
{
	return m_iAttitudeModifier;
}

int CvEventInfo::getTheirEnemyAttitudeModifier() const
{
	return m_iTheirEnemyAttitudeModifier;
}

int CvEventInfo::getPopulationChange() const
{
	return m_iPopulationChange;
}

int CvEventInfo::getRevoltTurns() const
{
	return m_iRevoltTurns;
}

int CvEventInfo::getMinPillage() const
{
	return m_iMinPillage;
}

int CvEventInfo::getMaxPillage() const
{
	return m_iMaxPillage;
}

int CvEventInfo::getUnitPromotion() const
{
	return m_iUnitPromotion;
}

int CvEventInfo::getFreeUnitSupport() const
{
	return m_iFreeUnitSupport;
}

int CvEventInfo::getInflationModifier() const
{
	return m_iInflationModifier;
}

int CvEventInfo::getSpaceProductionModifier() const
{
	return m_iSpaceProductionModifier;
}

int CvEventInfo::getAIValue() const
{
	return m_iAIValue;
}

int CvEventInfo::getAdditionalEventChance(int i) const
{
	FAssertBounds(0, GC.getNumEventInfos(), i);
	return m_piAdditionalEventChance ? m_piAdditionalEventChance[i] : 0;
}

int CvEventInfo::getAdditionalEventTime(int i) const
{
	FAssertBounds(0, GC.getNumEventInfos(), i);
	FAssert (i >= 0 && i < GC.getNumEventInfos());
	return m_piAdditionalEventTime ? m_piAdditionalEventTime[i] : 0;
}

int CvEventInfo::getClearEventChance(int i) const
{
	FAssertBounds(0, GC.getNumEventInfos(), i);
	FAssert (i >= 0 && i < GC.getNumEventInfos());
	return m_piClearEventChance ? m_piClearEventChance[i] : 0;
}

int CvEventInfo::getTechFlavorValue(int i) const
{
	FAssertBounds(0, GC.getNumFlavorTypes(), i);
	return m_piTechFlavorValue ? m_piTechFlavorValue[i] : 0; // advc.003t
}

int CvEventInfo::getPlotExtraYield(int i) const
{
	FAssertBounds(0, NUM_YIELD_TYPES, i);
	return m_piPlotExtraYields ? m_piPlotExtraYields[i] : 0; // advc.003t
}

int CvEventInfo::getFreeSpecialistCount(int i) const
{
	FAssertBounds(0, GC.getNumSpecialistInfos(), i);
	return m_piFreeSpecialistCount ? m_piFreeSpecialistCount[i] : 0; // advc.003t
}

int CvEventInfo::getUnitCombatPromotion(int i) const
{
	FAssertBounds(0, GC.getNumUnitCombatInfos(), i);
	return m_piUnitCombatPromotions ? m_piUnitCombatPromotions[i] : NO_PROMOTION; // advc.003t
}

int CvEventInfo::getUnitClassPromotion(int i) const
{
	FAssertBounds(0, GC.getNumUnitClassInfos(), i);
	return m_piUnitClassPromotions ? m_piUnitClassPromotions[i] : NO_PROMOTION; // advc.003t
}

const CvWString& CvEventInfo::getWorldNews(int i) const
{
	FAssert(i >= 0 && i < (int)m_aszWorldNews.size());
	return m_aszWorldNews[i];
}

int CvEventInfo::getNumWorldNews() const
{
	return m_aszWorldNews.size();
}

const char* CvEventInfo::getPythonCallback() const
{
	return m_szPythonCallback;
}

const char* CvEventInfo::getPythonExpireCheck() const
{
	return m_szPythonExpireCheck;
}

const char* CvEventInfo::getPythonCanDo() const
{
	return m_szPythonCanDo;
}

const char* CvEventInfo::getPythonHelp() const
{
	return m_szPythonHelp;
}

const wchar* CvEventInfo::getUnitNameKey() const
{
	return m_szUnitName;
}

const wchar* CvEventInfo::getQuestFailTextKey() const
{
	return m_szQuestFailText;
}

const wchar* CvEventInfo::getLocalInfoTextKey() const
{
	return m_szLocalInfoText;
}

const wchar* CvEventInfo::getOtherPlayerPopup() const
{
	return m_szOtherPlayerPopup;
}
#if ENABLE_XML_FILE_CACHE
void CvEventInfo::read(FDataStreamBase* stream)
{
	base_t::read(stream);
	uint uiFlag=0;
	stream->Read(&uiFlag);

	stream->Read(&m_bQuest);
	stream->Read(&m_bGlobal);
	stream->Read(&m_bTeam);
	stream->Read(&m_bCityEffect);
	stream->Read(&m_bOtherPlayerCityEffect);
	stream->Read(&m_bGoldToPlayer);
	stream->Read(&m_bGoldenAge);
	stream->Read(&m_bDeclareWar);
	stream->Read(&m_bDisbandUnit);
	stream->Read(&m_iGold);
	stream->Read(&m_iRandomGold);
	stream->Read(&m_iCulture);
	stream->Read(&m_iEspionagePoints);
	stream->Read(&m_iTech);
	stream->Read(&m_iTechPercent);
	stream->Read(&m_iTechCostPercent);
	stream->Read(&m_iTechMinTurnsLeft);
	stream->Read(&m_iPrereqTech);
	stream->Read(&m_iUnitClass);
	stream->Read(&m_iNumUnits);
	stream->Read(&m_iUnitExperience);
	stream->Read(&m_iUnitImmobileTurns);
	stream->Read(&m_iBuildingClass);
	stream->Read(&m_iBuildingChange);
	stream->Read(&m_iHappy);
	stream->Read(&m_iHealth);
	stream->Read(&m_iHurryAnger);
	stream->Read(&m_iHappyTurns);
	stream->Read(&m_iFood);
	stream->Read(&m_iFoodPercent);
	stream->Read(&m_iFeature);
	stream->Read(&m_iFeatureChange);
	stream->Read(&m_iImprovement);
	stream->Read(&m_iImprovementChange);
	stream->Read(&m_iBonus);
	stream->Read(&m_iBonusChange);
	stream->Read(&m_iRoute);
	stream->Read(&m_iRouteChange);
	stream->Read(&m_iBonusRevealed);
	stream->Read(&m_iBonusGift);
	stream->Read(&m_iConvertOwnCities);
	stream->Read(&m_iConvertOtherCities);
	stream->Read(&m_iMaxNumReligions);
	stream->Read(&m_iOurAttitudeModifier);
	stream->Read(&m_iAttitudeModifier);
	stream->Read(&m_iTheirEnemyAttitudeModifier);
	stream->Read(&m_iPopulationChange);
	stream->Read(&m_iRevoltTurns);
	stream->Read(&m_iMinPillage);
	stream->Read(&m_iMaxPillage);
	stream->Read(&m_iUnitPromotion);
	stream->Read(&m_iFreeUnitSupport);
	stream->Read(&m_iInflationModifier);
	stream->Read(&m_iSpaceProductionModifier);
	stream->Read(&m_iAIValue);
	SAFE_DELETE_ARRAY(m_piTechFlavorValue);
	m_piTechFlavorValue = new int[GC.getNumFlavorTypes()];
	stream->Read(GC.getNumFlavorTypes(), m_piTechFlavorValue);
	SAFE_DELETE_ARRAY(m_piPlotExtraYields);
	m_piPlotExtraYields = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_piPlotExtraYields);
	SAFE_DELETE_ARRAY(m_piFreeSpecialistCount);
	m_piFreeSpecialistCount = new int[GC.getNumSpecialistInfos()];
	stream->Read(GC.getNumSpecialistInfos(), m_piFreeSpecialistCount);
	SAFE_DELETE_ARRAY(m_piAdditionalEventChance);
	m_piAdditionalEventChance = new int[GC.getNumEventInfos()];
	stream->Read(GC.getNumEventInfos(), m_piAdditionalEventChance);
	SAFE_DELETE_ARRAY(m_piAdditionalEventTime);
	m_piAdditionalEventTime = new int[GC.getNumEventInfos()];
	stream->Read(GC.getNumEventInfos(), m_piAdditionalEventTime);
	SAFE_DELETE_ARRAY(m_piClearEventChance);
	m_piClearEventChance = new int[GC.getNumEventInfos()];
	stream->Read(GC.getNumEventInfos(), m_piClearEventChance);
	SAFE_DELETE_ARRAY(m_piUnitCombatPromotions);
	m_piUnitCombatPromotions = new int[GC.getNumUnitCombatInfos()];
	stream->Read(GC.getNumUnitCombatInfos(), m_piUnitCombatPromotions);
	SAFE_DELETE_ARRAY(m_piUnitClassPromotions);
	m_piUnitClassPromotions = new int[GC.getNumUnitClassInfos()];
	stream->Read(GC.getNumUnitClassInfos(), m_piUnitClassPromotions);
	int iNumElements;
	CvWString szText;
	stream->Read(&iNumElements);
	m_aszWorldNews.clear();
	for (int i = 0; i < iNumElements; ++i)
	{
		stream->ReadString(szText);
		m_aszWorldNews.push_back(szText);
	}
	// <advc.003t>
	BuildingYieldChange().read(stream);
	BuildingCommerceChange().read(stream);
	BuildingHappyChange().read(stream);
	BuildingHealthChange().read(stream); // </advc.003t>
	stream->ReadString(m_szUnitName);
	stream->ReadString(m_szOtherPlayerPopup);
	stream->ReadString(m_szQuestFailText);
	stream->ReadString(m_szLocalInfoText);
	stream->ReadString(m_szPythonCallback);
	stream->ReadString(m_szPythonExpireCheck);
	stream->ReadString(m_szPythonCanDo);
	stream->ReadString(m_szPythonHelp);
}

void CvEventInfo::write(FDataStreamBase* stream)
{
	base_t::write(stream);
	uint uiFlag=0;
	stream->Write(uiFlag);

	stream->Write(m_bQuest);
	stream->Write(m_bGlobal);
	stream->Write(m_bTeam);
	stream->Write(m_bCityEffect);
	stream->Write(m_bOtherPlayerCityEffect);
	stream->Write(m_bGoldToPlayer);
	stream->Write(m_bGoldenAge);
	stream->Write(m_bDeclareWar);
	stream->Write(m_bDisbandUnit);
	stream->Write(m_iGold);
	stream->Write(m_iRandomGold);
	stream->Write(m_iCulture);
	stream->Write(m_iEspionagePoints);
	stream->Write(m_iTech);
	stream->Write(m_iTechPercent);
	stream->Write(m_iTechCostPercent);
	stream->Write(m_iTechMinTurnsLeft);
	stream->Write(m_iPrereqTech);
	stream->Write(m_iUnitClass);
	stream->Write(m_iNumUnits);
	stream->Write(m_iUnitExperience);
	stream->Write(m_iUnitImmobileTurns);
	stream->Write(m_iBuildingClass);
	stream->Write(m_iBuildingChange);
	stream->Write(m_iHappy);
	stream->Write(m_iHealth);
	stream->Write(m_iHurryAnger);
	stream->Write(m_iHappyTurns);
	stream->Write(m_iFood);
	stream->Write(m_iFoodPercent);
	stream->Write(m_iFeature);
	stream->Write(m_iFeatureChange);
	stream->Write(m_iImprovement);
	stream->Write(m_iImprovementChange);
	stream->Write(m_iBonus);
	stream->Write(m_iBonusChange);
	stream->Write(m_iRoute);
	stream->Write(m_iRouteChange);
	stream->Write(m_iBonusRevealed);
	stream->Write(m_iBonusGift);
	stream->Write(m_iConvertOwnCities);
	stream->Write(m_iConvertOtherCities);
	stream->Write(m_iMaxNumReligions);
	stream->Write(m_iOurAttitudeModifier);
	stream->Write(m_iAttitudeModifier);
	stream->Write(m_iTheirEnemyAttitudeModifier);
	stream->Write(m_iPopulationChange);
	stream->Write(m_iRevoltTurns);
	stream->Write(m_iMinPillage);
	stream->Write(m_iMaxPillage);
	stream->Write(m_iUnitPromotion);
	stream->Write(m_iFreeUnitSupport);
	stream->Write(m_iInflationModifier);
	stream->Write(m_iSpaceProductionModifier);
	stream->Write(m_iAIValue);
	stream->Write(GC.getNumFlavorTypes(), m_piTechFlavorValue);
	stream->Write(NUM_YIELD_TYPES, m_piPlotExtraYields);
	stream->Write(GC.getNumSpecialistInfos(), m_piFreeSpecialistCount);
	stream->Write(GC.getNumEventInfos(), m_piAdditionalEventChance);
	stream->Write(GC.getNumEventInfos(), m_piAdditionalEventTime);
	stream->Write(GC.getNumEventInfos(), m_piClearEventChance);
	stream->Write(GC.getNumUnitCombatInfos(), m_piUnitCombatPromotions);
	stream->Write(GC.getNumUnitClassInfos(), m_piUnitClassPromotions);
	stream->Write(m_aszWorldNews.size());
	for (std::vector<CvWString>::iterator it = m_aszWorldNews.begin(); it != m_aszWorldNews.end(); ++it)
		stream->WriteString(*it);
	// <advc.003t>
	BuildingYieldChange().write(stream);
	BuildingCommerceChange().write(stream);
	BuildingHappyChange().write(stream);
	BuildingHealthChange().write(stream); // </advc.003t>
	stream->WriteString(m_szUnitName);
	stream->WriteString(m_szOtherPlayerPopup);
	stream->WriteString(m_szQuestFailText);
	stream->WriteString(m_szLocalInfoText);
	stream->WriteString(m_szPythonCallback);
	stream->WriteString(m_szPythonExpireCheck);
	stream->WriteString(m_szPythonCanDo);
	stream->WriteString(m_szPythonHelp);
}
#endif
bool CvEventInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML))
		return false;

	pXML->GetChildXmlValByName(&m_bQuest, "bQuest");
	pXML->GetChildXmlValByName(&m_bGlobal, "bGlobal");
	pXML->GetChildXmlValByName(&m_bTeam, "bTeam");
	pXML->GetChildXmlValByName(&m_bCityEffect, "bPickCity");
	pXML->GetChildXmlValByName(&m_bOtherPlayerCityEffect, "bPickOtherPlayerCity");
	pXML->GetChildXmlValByName(&m_bGoldToPlayer, "bGoldToPlayer");
	pXML->GetChildXmlValByName(&m_bGoldenAge, "bGoldenAge");
	pXML->GetChildXmlValByName(&m_bDeclareWar, "bDeclareWar");
	pXML->GetChildXmlValByName(&m_iGold, "iGold");
	pXML->GetChildXmlValByName(&m_iRandomGold, "iRandomGold");
	pXML->GetChildXmlValByName(&m_iCulture, "iCulture");
	pXML->GetChildXmlValByName(&m_iEspionagePoints, "iEspionagePoints");
	pXML->SetInfoIDFromChildXmlVal(m_iTech, "Tech");
	pXML->GetChildXmlValByName(&m_iTechPercent, "iTechPercent");
	pXML->GetChildXmlValByName(&m_iTechCostPercent, "iTechCostPercent");
	pXML->GetChildXmlValByName(&m_iTechMinTurnsLeft, "iTechMinTurnsLeft");
	pXML->SetInfoIDFromChildXmlVal(m_iPrereqTech, "PrereqTech");
	pXML->SetInfoIDFromChildXmlVal(m_iUnitClass, "UnitClass");
	pXML->GetChildXmlValByName(&m_iNumUnits, "iNumFreeUnits");
	pXML->GetChildXmlValByName(&m_bDisbandUnit, "bDisbandUnit");
	pXML->GetChildXmlValByName(&m_iUnitExperience, "iUnitExperience");
	pXML->GetChildXmlValByName(&m_iUnitImmobileTurns, "iUnitImmobileTurns");
	pXML->SetInfoIDFromChildXmlVal(m_iBuildingClass, "BuildingClass");
	pXML->GetChildXmlValByName(&m_iBuildingChange, "iBuildingChange");

	pXML->GetChildXmlValByName(&m_iHappy, "iHappy");
	pXML->GetChildXmlValByName(&m_iHealth, "iHealth");
	pXML->GetChildXmlValByName(&m_iHurryAnger, "iHurryAnger");
	pXML->GetChildXmlValByName(&m_iHappyTurns, "iHappyTurns");
	pXML->GetChildXmlValByName(&m_iFood, "iFood");
	pXML->GetChildXmlValByName(&m_iFoodPercent, "iFoodPercent");

	pXML->SetInfoIDFromChildXmlVal(m_iFeature, "FeatureType");
	pXML->GetChildXmlValByName(&m_iFeatureChange, "iFeatureChange");

	pXML->SetInfoIDFromChildXmlVal(m_iImprovement, "ImprovementType");
	pXML->GetChildXmlValByName(&m_iImprovementChange, "iImprovementChange");

	pXML->SetInfoIDFromChildXmlVal(m_iBonus, "BonusType");
	pXML->GetChildXmlValByName(&m_iBonusChange, "iBonusChange");

	pXML->SetInfoIDFromChildXmlVal(m_iRoute, "RouteType");
	pXML->GetChildXmlValByName(&m_iRouteChange, "iRouteChange");

	pXML->SetInfoIDFromChildXmlVal(m_iBonusRevealed, "BonusRevealed");

	pXML->SetInfoIDFromChildXmlVal(m_iBonusGift, "BonusGift");

	pXML->SetVariableListTagPair(&m_piTechFlavorValue, "TechFlavors", GC.getNumFlavorTypes());
	pXML->SetVariableListTagPair(&m_piPlotExtraYields, "PlotExtraYields", NUM_YIELD_TYPES, 0);
	pXML->SetVariableListTagPair(&m_piFreeSpecialistCount, "FreeSpecialistCounts", GC.getNumSpecialistInfos());

	pXML->GetChildXmlValByName(&m_iConvertOwnCities, "iConvertOwnCities");
	pXML->GetChildXmlValByName(&m_iConvertOtherCities, "iConvertOtherCities");
	pXML->GetChildXmlValByName(&m_iMaxNumReligions, "iMaxNumReligions");
	pXML->GetChildXmlValByName(&m_iOurAttitudeModifier, "iOurAttitudeModifier");
	pXML->GetChildXmlValByName(&m_iAttitudeModifier, "iAttitudeModifier");
	pXML->GetChildXmlValByName(&m_iTheirEnemyAttitudeModifier, "iTheirEnemyAttitudeModifier");
	pXML->GetChildXmlValByName(&m_iPopulationChange, "iPopulationChange");
	pXML->GetChildXmlValByName(&m_iRevoltTurns, "iRevoltTurns");
	pXML->GetChildXmlValByName(&m_iMinPillage, "iMinPillage");
	pXML->GetChildXmlValByName(&m_iMaxPillage, "iMaxPillage");
	pXML->SetInfoIDFromChildXmlVal(m_iUnitPromotion, "UnitPromotion");
	pXML->GetChildXmlValByName(&m_iFreeUnitSupport, "iFreeUnitSupport");
	pXML->GetChildXmlValByName(&m_iInflationModifier, "iInflationMod");
	pXML->GetChildXmlValByName(&m_iSpaceProductionModifier, "iSpaceProductionMod");
	pXML->GetChildXmlValByName(&m_iAIValue, "iAIValue");

	CvString* pszPromotions = NULL;
	FAssertMsg(NULL == m_piUnitCombatPromotions, "Memory leak");
	m_piUnitCombatPromotions = new int[GC.getNumUnitCombatInfos()];
	pXML->SetVariableListTagPair(&pszPromotions, "UnitCombatPromotions", GC.getNumUnitCombatInfos(), "NONE");
	if (pszPromotions != NULL) // advc.003t
	{
		for (int i = 0; i < GC.getNumUnitCombatInfos(); ++i)
			m_piUnitCombatPromotions[i] = pXML->FindInInfoClass(pszPromotions[i]);
		SAFE_DELETE_ARRAY(pszPromotions);
	}
	FAssertMsg(NULL == m_piUnitClassPromotions, "Memory leak");
	m_piUnitClassPromotions = new int[GC.getNumUnitClassInfos()];
	pXML->SetVariableListTagPair(&pszPromotions, "UnitClassPromotions", GC.getNumUnitClassInfos(), "NONE");
	if (pszPromotions!= NULL) // advc.003t
	{
		for (int i = 0; i < GC.getNumUnitClassInfos(); ++i)
			m_piUnitClassPromotions[i] = pXML->FindInInfoClass(pszPromotions[i]);
		SAFE_DELETE_ARRAY(pszPromotions);
	}
	pXML->GetChildXmlValByName(m_szUnitName, "UnitName");
	pXML->GetChildXmlValByName(m_szOtherPlayerPopup, "OtherPlayerPopup");
	pXML->GetChildXmlValByName(m_szQuestFailText, "QuestFailText");
	pXML->GetChildXmlValByName(m_szLocalInfoText, "LocalInfoText");
	pXML->GetChildXmlValByName(m_szPythonCallback, "PythonCallback");
	pXML->GetChildXmlValByName(m_szPythonExpireCheck, "PythonExpireCheck");
	pXML->GetChildXmlValByName(m_szPythonCanDo, "PythonCanDo");
	pXML->GetChildXmlValByName(m_szPythonHelp, "PythonHelp");

	m_aszWorldNews.clear();
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "WorldNewsTexts"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			if (iNumSibs > 0)
			{
				CvString szTextVal;
				if (pXML->GetChildXmlVal(szTextVal))
				{
					for (int j = 0; j<iNumSibs; ++j)
					{
						m_aszWorldNews.push_back(szTextVal);
						if (!pXML->GetNextXmlVal(szTextVal))
							break;
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	// <advc.003t>
	pXML->SetVariableListTagRate(BuildingYieldChange(), "BuildingExtraYield");
	pXML->SetVariableListTagRate(BuildingCommerceChange(), "BuildingExtraCommerce");
	pXML->SetVariableListTagPair(BuildingHappyChange(), "BuildingExtraHappies");
	pXML->SetVariableListTagPair(BuildingHealthChange(), "BuildingExtraHealths");
	// </advc.003t>
	return true;
}

bool CvEventInfo::readPass2(CvXMLLoadUtility* pXML)
{
	pXML->SetVariableListTagPair(&m_piAdditionalEventChance, "AdditionalEvents", GC.getNumEventInfos(), 0);
	pXML->SetVariableListTagPair(&m_piAdditionalEventTime, "EventTimes", GC.getNumEventInfos(), 0);
	pXML->SetVariableListTagPair(&m_piClearEventChance, "ClearEvents", GC.getNumEventInfos(), 0);

	return true;
}

CvEventTriggerInfo::CvEventTriggerInfo() :
	m_iPercentGamesActive(0),
	m_iProbability(0),
	m_iNumUnits(0),
	m_iNumBuildings(0),
	m_iNumUnitsGlobal(0),
	m_iNumBuildingsGlobal(0),
	m_iNumPlotsRequired(0),
	m_iPlotType(0),
	m_iNumReligions(0),
	m_iNumCorporations(0),
	m_iOtherPlayerShareBorders(0),
	m_iOtherPlayerHasTech(NO_TECH),
	m_iCivic(NO_CIVIC),
	m_iMinPopulation(0),
	m_iMaxPopulation(0),
	m_iMinMapLandmass(0),
	m_iMinOurLandmass(0),
	m_iMaxOurLandmass(0),
	m_iMinDifficulty(NO_HANDICAP),
	m_iAngry(0),
	m_iUnhealthy(0),
	m_iUnitDamagedWeight(0),
	m_iUnitDistanceWeight(0),
	m_iUnitExperienceWeight(0),
	m_iMinTreasury(0),
	m_bSinglePlayer(false),
	m_bTeam(false),
	m_bRecurring(false),
	m_bGlobal(false),
	m_bPickPlayer(false),
	m_bOtherPlayerWar(false),
	m_bOtherPlayerHasReligion(false),
	m_bOtherPlayerHasOtherReligion(false),
	m_bOtherPlayerAI(false),
	m_bPickCity(false),
	m_bPickOtherPlayerCity(false),
	m_bShowPlot(true),
	m_iCityFoodWeight(0),
	m_bUnitsOnPlot(false),
	m_bOwnPlot(false),
	m_bPickReligion(false),
	m_bStateReligion(false),
	m_bHolyCity(false),
	m_bPickCorporation(false),
	m_bHeadquarters(false),
	m_bProbabilityUnitMultiply(false),
	m_bProbabilityBuildingMultiply(false),
	m_bPrereqEventCity(false)
{}

int CvEventTriggerInfo::getPercentGamesActive() const
{
	return m_iPercentGamesActive;
}

int CvEventTriggerInfo::getProbability() const
{
	return m_iProbability;
}

int CvEventTriggerInfo::getUnitRequired(int i) const
{
	return m_aiUnitsRequired[i];
}

int CvEventTriggerInfo::getNumUnitsRequired() const
{
	return (int)m_aiUnitsRequired.size();
}

int CvEventTriggerInfo::getBuildingRequired(int i) const
{
	return m_aiBuildingsRequired[i];
}

int CvEventTriggerInfo::getNumBuildingsRequired() const
{
	return (int)m_aiBuildingsRequired.size();
}

int CvEventTriggerInfo::getNumUnits() const
{
	return m_iNumUnits;
}

int CvEventTriggerInfo::getNumBuildings() const
{
	return m_iNumBuildings;
}

int CvEventTriggerInfo::getNumUnitsGlobal() const
{
	return m_iNumUnitsGlobal;
}

int CvEventTriggerInfo::getNumBuildingsGlobal() const
{
	return m_iNumBuildingsGlobal;
}

int CvEventTriggerInfo::getNumPlotsRequired() const
{
	return m_iNumPlotsRequired;
}

int CvEventTriggerInfo::getPlotType() const
{
	return m_iPlotType;
}

int CvEventTriggerInfo::getNumReligions() const
{
	return m_iNumReligions;
}

int CvEventTriggerInfo::getNumCorporations() const
{
	return m_iNumCorporations;
}

int CvEventTriggerInfo::getOtherPlayerShareBorders() const
{
	return m_iOtherPlayerShareBorders;
}

int CvEventTriggerInfo::getOtherPlayerHasTech() const
{
	return m_iOtherPlayerHasTech;
}

int CvEventTriggerInfo::getCivic() const
{
	return m_iCivic;
}

int CvEventTriggerInfo::getMinPopulation() const
{
	return m_iMinPopulation;
}

int CvEventTriggerInfo::getMaxPopulation() const
{
	return m_iMaxPopulation;
}

int CvEventTriggerInfo::getMinMapLandmass() const
{
	return m_iMinMapLandmass;
}

int CvEventTriggerInfo::getMinOurLandmass() const
{
	return m_iMinOurLandmass;
}

int CvEventTriggerInfo::getMaxOurLandmass() const
{
	return m_iMaxOurLandmass;
}

int CvEventTriggerInfo::getMinDifficulty() const
{
	return m_iMinDifficulty;
}

int CvEventTriggerInfo::getAngry() const
{
	return m_iAngry;
}

int CvEventTriggerInfo::getUnhealthy() const
{
	return m_iUnhealthy;
}

int CvEventTriggerInfo::getUnitDamagedWeight() const
{
	return m_iUnitDamagedWeight;
}

int CvEventTriggerInfo::getUnitDistanceWeight() const
{
	return m_iUnitDistanceWeight;
}

int CvEventTriggerInfo::getUnitExperienceWeight() const
{
	return m_iUnitExperienceWeight;
}

int CvEventTriggerInfo::getMinTreasury() const
{
	return m_iMinTreasury;
}

int CvEventTriggerInfo::getEvent(int i) const
{
	return m_aiEvents[i];
}

int CvEventTriggerInfo::getNumEvents() const
{
	return (int)m_aiEvents.size();
}

int CvEventTriggerInfo::getPrereqEvent(int i) const
{
	return m_aiPrereqEvents[i];
}

int CvEventTriggerInfo::getNumPrereqEvents() const
{
	return (int)m_aiPrereqEvents.size();
}

int CvEventTriggerInfo::getPrereqOrTechs(int i) const
{
	return m_aiPrereqOrTechs[i];
}

int CvEventTriggerInfo::getNumPrereqOrTechs() const
{
	return (int)m_aiPrereqOrTechs.size();
}

int CvEventTriggerInfo::getPrereqAndTechs(int i) const
{
	return m_aiPrereqAndTechs[i];
}

int CvEventTriggerInfo::getNumPrereqAndTechs() const
{
	return (int)m_aiPrereqAndTechs.size();
}

int CvEventTriggerInfo::getObsoleteTech(int i) const
{
	return m_aiObsoleteTechs[i];
}

int CvEventTriggerInfo::getNumObsoleteTechs() const
{
	return (int)m_aiObsoleteTechs.size();
}

int CvEventTriggerInfo::getFeatureRequired(int i) const
{
	return m_aiFeaturesRequired[i];
}

int CvEventTriggerInfo::getNumFeaturesRequired() const
{
	return (int)m_aiFeaturesRequired.size();
}

int CvEventTriggerInfo::getTerrainRequired(int i) const
{
	return m_aiTerrainsRequired[i];
}

int CvEventTriggerInfo::getNumTerrainsRequired() const
{
	return (int)m_aiTerrainsRequired.size();
}

int CvEventTriggerInfo::getImprovementRequired(int i) const
{
	return m_aiImprovementsRequired[i];
}

int CvEventTriggerInfo::getNumImprovementsRequired() const
{
	return (int)m_aiImprovementsRequired.size();
}

int CvEventTriggerInfo::getBonusRequired(int i) const
{
	return m_aiBonusesRequired[i];
}

int CvEventTriggerInfo::getNumBonusesRequired() const
{
	return (int)m_aiBonusesRequired.size();
}

int CvEventTriggerInfo::getRouteRequired(int i) const
{
	return m_aiRoutesRequired[i];
}

int CvEventTriggerInfo::getNumRoutesRequired() const
{
	return (int)m_aiRoutesRequired.size();
}

int CvEventTriggerInfo::getReligionRequired(int i) const
{
	return m_aiReligionsRequired[i];
}

int CvEventTriggerInfo::getNumReligionsRequired() const
{
	return (int)m_aiReligionsRequired.size();
}

int CvEventTriggerInfo::getCorporationRequired(int i) const
{
	return m_aiCorporationsRequired[i];
}

int CvEventTriggerInfo::getNumCorporationsRequired() const
{
	return (int)m_aiCorporationsRequired.size();
}

bool CvEventTriggerInfo::isSinglePlayer() const
{
	return m_bSinglePlayer;
}

bool CvEventTriggerInfo::isTeam() const
{
	return m_bTeam;
}

const CvWString& CvEventTriggerInfo::getText(int i) const
{
	FAssertBounds(0, (int)m_aszText.size(), i);
	return m_aszText[i];
}

int CvEventTriggerInfo::getTextEra(int i) const
{
	FAssertBounds(0, (int)m_aszText.size(), i);
	return m_aiTextEra[i];
}

int CvEventTriggerInfo::getNumTexts() const
{
	FAssert(m_aiTextEra.size() == m_aszText.size());
	return m_aszText.size();
}

const CvWString& CvEventTriggerInfo::getWorldNews(int i) const
{
	FAssertBounds(0, (int)m_aszWorldNews.size(), i);
	return m_aszWorldNews[i];
}

int CvEventTriggerInfo::getNumWorldNews() const
{
	return m_aszWorldNews.size();
}

bool CvEventTriggerInfo::isRecurring() const
{
	return m_bRecurring;
}

bool CvEventTriggerInfo::isGlobal() const
{
	return m_bGlobal;
}

bool CvEventTriggerInfo::isPickPlayer() const
{
	return m_bPickPlayer;
}

bool CvEventTriggerInfo::isOtherPlayerWar() const
{
	return m_bOtherPlayerWar;
}

bool CvEventTriggerInfo::isOtherPlayerHasReligion() const
{
	return m_bOtherPlayerHasReligion;
}

bool CvEventTriggerInfo::isOtherPlayerHasOtherReligion() const
{
	return m_bOtherPlayerHasOtherReligion;
}

bool CvEventTriggerInfo::isOtherPlayerAI() const
{
	return m_bOtherPlayerAI;
}

bool CvEventTriggerInfo::isPickCity() const
{
	return m_bPickCity;
}

bool CvEventTriggerInfo::isPickOtherPlayerCity() const
{
	return m_bPickOtherPlayerCity;
}

bool CvEventTriggerInfo::isShowPlot() const
{
	return m_bShowPlot;
}

int CvEventTriggerInfo::getCityFoodWeight() const
{
	return m_iCityFoodWeight;
}

bool CvEventTriggerInfo::isUnitsOnPlot() const
{
	return m_bUnitsOnPlot;
}

bool CvEventTriggerInfo::isOwnPlot() const
{
	return m_bOwnPlot;
}

bool CvEventTriggerInfo::isPickReligion() const
{
	return m_bPickReligion;
}

bool CvEventTriggerInfo::isStateReligion() const
{
	return m_bStateReligion;
}

bool CvEventTriggerInfo::isHolyCity() const
{
	return m_bHolyCity;
}

bool CvEventTriggerInfo::isPickCorporation() const
{
	return m_bPickCorporation;
}

bool CvEventTriggerInfo::isHeadquarters() const
{
	return m_bHeadquarters;
}

bool CvEventTriggerInfo::isProbabilityUnitMultiply() const
{
	return m_bProbabilityUnitMultiply;
}

bool CvEventTriggerInfo::isProbabilityBuildingMultiply() const
{
	return m_bProbabilityBuildingMultiply;
}

bool CvEventTriggerInfo::isPrereqEventCity() const
{
	return m_bPrereqEventCity;
}

bool CvEventTriggerInfo::isPlotEventTrigger() const  // advc: refactored
{
	if (getNumPlotsRequired() <= 0)
		return false;

	if (getPlotType() != NO_PLOT || getNumFeaturesRequired() > 0 ||
		getNumTerrainsRequired() > 0 || getNumImprovementsRequired() > 0 ||
		getNumBonusesRequired() > 0 || getNumRoutesRequired() > 0)
	{
		return true;
	}
	if (isUnitsOnPlot() && getNumUnitsRequired() > 0)
		return true;

	if (isPrereqEventCity() && !isPickCity())
		return true;

	return false;
}

const char* CvEventTriggerInfo::getPythonCallback() const
{
	return m_szPythonCallback;
}

const char* CvEventTriggerInfo::getPythonCanDo() const
{
	return m_szPythonCanDo;
}

const char* CvEventTriggerInfo::getPythonCanDoCity() const
{
	return m_szPythonCanDoCity;
}

const char* CvEventTriggerInfo::getPythonCanDoUnit() const
{
	return m_szPythonCanDoUnit;
}
#if ENABLE_XML_FILE_CACHE
void CvEventTriggerInfo::read(FDataStreamBase* stream)
{
	CvWString szElement;
	base_t::read(stream);
	uint uiFlag=0;
	stream->Read(&uiFlag);

	stream->Read(&m_iPercentGamesActive);
	stream->Read(&m_iProbability);
	stream->Read(&m_iNumUnits);
	stream->Read(&m_iNumBuildings);
	stream->Read(&m_iNumUnitsGlobal);
	stream->Read(&m_iNumBuildingsGlobal);
	stream->Read(&m_iNumPlotsRequired);
	stream->Read(&m_iPlotType);
	stream->Read(&m_iNumReligions);
	stream->Read(&m_iNumCorporations);
	stream->Read(&m_iOtherPlayerShareBorders);
	stream->Read(&m_iOtherPlayerHasTech);
	stream->Read(&m_iCivic);
	stream->Read(&m_iMinPopulation);
	stream->Read(&m_iMaxPopulation);
	stream->Read(&m_iMinMapLandmass);
	stream->Read(&m_iMinOurLandmass);
	stream->Read(&m_iMaxOurLandmass);
	stream->Read(&m_iMinDifficulty);
	stream->Read(&m_iAngry);
	stream->Read(&m_iUnhealthy);
	stream->Read(&m_iUnitDamagedWeight);
	stream->Read(&m_iUnitDistanceWeight);
	stream->Read(&m_iUnitExperienceWeight);
	stream->Read(&m_iMinTreasury);

	int iNumElements;
	int iElement;

	stream->Read(&iNumElements);
	m_aiUnitsRequired.clear();
	for (int i = 0; i < iNumElements; ++i)
	{
		stream->Read(&iElement);
		m_aiUnitsRequired.push_back(iElement);
	}
	stream->Read(&iNumElements);
	m_aiBuildingsRequired.clear();
	for (int i = 0; i < iNumElements; ++i)
	{
		stream->Read(&iElement);
		m_aiBuildingsRequired.push_back(iElement);
	}
	stream->Read(&iNumElements);
	m_aiPrereqOrTechs.clear();
	for (int i = 0; i < iNumElements; ++i)
	{
		stream->Read(&iElement);
		m_aiPrereqOrTechs.push_back(iElement);
	}
	stream->Read(&iNumElements);
	m_aiPrereqAndTechs.clear();
	for (int i = 0; i < iNumElements; ++i)
	{
		stream->Read(&iElement);
		m_aiPrereqAndTechs.push_back(iElement);
	}
	stream->Read(&iNumElements);
	m_aiObsoleteTechs.clear();
	for (int i = 0; i < iNumElements; ++i)
	{
		stream->Read(&iElement);
		m_aiObsoleteTechs.push_back(iElement);
	}
	stream->Read(&iNumElements);
	m_aiEvents.clear();
	for (int i = 0; i < iNumElements; ++i)
	{
		stream->Read(&iElement);
		m_aiEvents.push_back(iElement);
	}
	stream->Read(&iNumElements);
	m_aiPrereqEvents.clear();
	for (int i = 0; i < iNumElements; ++i)
	{
		stream->Read(&iElement);
		m_aiPrereqEvents.push_back(iElement);
	}
	stream->Read(&iNumElements);
	m_aiFeaturesRequired.clear();
	for (int i = 0; i < iNumElements; ++i)
	{
		stream->Read(&iElement);
		m_aiFeaturesRequired.push_back(iElement);
	}
	stream->Read(&iNumElements);
	m_aiTerrainsRequired.clear();
	for (int i = 0; i < iNumElements; ++i)
	{
		stream->Read(&iElement);
		m_aiTerrainsRequired.push_back(iElement);
	}
	stream->Read(&iNumElements);
	m_aiImprovementsRequired.clear();
	for (int i = 0; i < iNumElements; ++i)
	{
		stream->Read(&iElement);
		m_aiImprovementsRequired.push_back(iElement);
	}
	stream->Read(&iNumElements);
	m_aiBonusesRequired.clear();
	for (int i = 0; i < iNumElements; ++i)
	{
		stream->Read(&iElement);
		m_aiBonusesRequired.push_back(iElement);
	}
	stream->Read(&iNumElements);
	m_aiRoutesRequired.clear();
	for (int i = 0; i < iNumElements; ++i)
	{
		stream->Read(&iElement);
		m_aiRoutesRequired.push_back(iElement);
	}
	stream->Read(&iNumElements);
	m_aiReligionsRequired.clear();
	for (int i = 0; i < iNumElements; ++i)
	{
		stream->Read(&iElement);
		m_aiReligionsRequired.push_back(iElement);
	}
	stream->Read(&iNumElements);
	m_aiCorporationsRequired.clear();
	for (int i = 0; i < iNumElements; ++i)
	{
		stream->Read(&iElement);
		m_aiCorporationsRequired.push_back(iElement);
	}
	stream->Read(&m_bSinglePlayer);
	stream->Read(&m_bTeam);
	stream->Read(&m_bRecurring);
	stream->Read(&m_bGlobal);
	stream->Read(&m_bPickPlayer);
	stream->Read(&m_bOtherPlayerWar);
	stream->Read(&m_bOtherPlayerHasReligion);
	stream->Read(&m_bOtherPlayerHasOtherReligion);
	stream->Read(&m_bOtherPlayerAI);
	stream->Read(&m_bPickCity);
	stream->Read(&m_bPickOtherPlayerCity);
	stream->Read(&m_bShowPlot);
	stream->Read(&m_iCityFoodWeight);
	stream->Read(&m_bUnitsOnPlot);
	stream->Read(&m_bOwnPlot);
	stream->Read(&m_bPickReligion);
	stream->Read(&m_bStateReligion);
	stream->Read(&m_bHolyCity);
	stream->Read(&m_bPickCorporation);
	stream->Read(&m_bHeadquarters);
	stream->Read(&m_bProbabilityUnitMultiply);
	stream->Read(&m_bProbabilityBuildingMultiply);
	stream->Read(&m_bPrereqEventCity);
	stream->Read(&iNumElements);
	m_aszText.clear();
	for (int i = 0; i < iNumElements; ++i)
	{
		stream->ReadString(szElement);
		m_aszText.push_back(szElement);
	}
	m_aiTextEra.clear();
	for (int i = 0; i < iNumElements; ++i)
	{
		stream->Read(&iElement);
		m_aiTextEra.push_back(iElement);
	}
	stream->Read(&iNumElements);
	m_aszWorldNews.clear();
	for (int i = 0; i < iNumElements; ++i)
	{
		stream->ReadString(szElement);
		m_aszWorldNews.push_back(szElement);
	}
	stream->ReadString(m_szPythonCallback);
	stream->ReadString(m_szPythonCanDo);
	stream->ReadString(m_szPythonCanDoCity);
	stream->ReadString(m_szPythonCanDoUnit);
}

void CvEventTriggerInfo::write(FDataStreamBase* stream)
{
	base_t::write(stream);
	uint uiFlag=0;
	stream->Write(uiFlag);

	stream->Write(m_iPercentGamesActive);
	stream->Write(m_iProbability);
	stream->Write(m_iNumUnits);
	stream->Write(m_iNumBuildings);
	stream->Write(m_iNumUnitsGlobal);
	stream->Write(m_iNumBuildingsGlobal);
	stream->Write(m_iNumPlotsRequired);
	stream->Write(m_iPlotType);
	stream->Write(m_iNumReligions);
	stream->Write(m_iNumCorporations);
	stream->Write(m_iOtherPlayerShareBorders);
	stream->Write(m_iOtherPlayerHasTech);
	stream->Write(m_iCivic);
	stream->Write(m_iMinPopulation);
	stream->Write(m_iMaxPopulation);
	stream->Write(m_iMinMapLandmass);
	stream->Write(m_iMinOurLandmass);
	stream->Write(m_iMaxOurLandmass);
	stream->Write(m_iMinDifficulty);
	stream->Write(m_iAngry);
	stream->Write(m_iUnhealthy);
	stream->Write(m_iUnitDamagedWeight);
	stream->Write(m_iUnitDistanceWeight);
	stream->Write(m_iUnitExperienceWeight);
	stream->Write(m_iMinTreasury);
	stream->Write(m_aiUnitsRequired.size());
	for (std::vector<int>::iterator it = m_aiUnitsRequired.begin(); it != m_aiUnitsRequired.end(); ++it)
	{
		stream->Write(*it);
	}
	stream->Write(m_aiBuildingsRequired.size());
	for (std::vector<int>::iterator it = m_aiBuildingsRequired.begin(); it != m_aiBuildingsRequired.end(); ++it)
	{
		stream->Write(*it);
	}
	stream->Write(m_aiPrereqOrTechs.size());
	for (std::vector<int>::iterator it = m_aiPrereqOrTechs.begin(); it != m_aiPrereqOrTechs.end(); ++it)
	{
		stream->Write(*it);
	}
	stream->Write(m_aiPrereqAndTechs.size());
	for (std::vector<int>::iterator it = m_aiPrereqAndTechs.begin(); it != m_aiPrereqAndTechs.end(); ++it)
	{
		stream->Write(*it);
	}
	stream->Write(m_aiObsoleteTechs.size());
	for (std::vector<int>::iterator it = m_aiObsoleteTechs.begin(); it != m_aiObsoleteTechs.end(); ++it)
	{
		stream->Write(*it);
	}
	stream->Write(m_aiEvents.size());
	for (std::vector<int>::iterator it = m_aiEvents.begin(); it != m_aiEvents.end(); ++it)
	{
		stream->Write(*it);
	}
	stream->Write(m_aiPrereqEvents.size());
	for (std::vector<int>::iterator it = m_aiPrereqEvents.begin(); it != m_aiPrereqEvents.end(); ++it)
	{
		stream->Write(*it);
	}
	stream->Write(m_aiFeaturesRequired.size());
	for (std::vector<int>::iterator it = m_aiFeaturesRequired.begin(); it != m_aiFeaturesRequired.end(); ++it)
	{
		stream->Write(*it);
	}
	stream->Write(m_aiTerrainsRequired.size());
	for (std::vector<int>::iterator it = m_aiTerrainsRequired.begin(); it != m_aiTerrainsRequired.end(); ++it)
	{
		stream->Write(*it);
	}
	stream->Write(m_aiImprovementsRequired.size());
	for (std::vector<int>::iterator it = m_aiImprovementsRequired.begin(); it != m_aiImprovementsRequired.end(); ++it)
	{
		stream->Write(*it);
	}
	stream->Write(m_aiBonusesRequired.size());
	for (std::vector<int>::iterator it = m_aiBonusesRequired.begin(); it != m_aiBonusesRequired.end(); ++it)
	{
		stream->Write(*it);
	}
	stream->Write(m_aiRoutesRequired.size());
	for (std::vector<int>::iterator it = m_aiRoutesRequired.begin(); it != m_aiRoutesRequired.end(); ++it)
	{
		stream->Write(*it);
	}
	stream->Write(m_aiReligionsRequired.size());
	for (std::vector<int>::iterator it = m_aiReligionsRequired.begin(); it != m_aiReligionsRequired.end(); ++it)
	{
		stream->Write(*it);
	}
	stream->Write(m_aiCorporationsRequired.size());
	for (std::vector<int>::iterator it = m_aiCorporationsRequired.begin(); it != m_aiCorporationsRequired.end(); ++it)
	{
		stream->Write(*it);
	}
	stream->Write(m_bSinglePlayer);
	stream->Write(m_bTeam);
	stream->Write(m_bRecurring);
	stream->Write(m_bGlobal);
	stream->Write(m_bPickPlayer);
	stream->Write(m_bOtherPlayerWar);
	stream->Write(m_bOtherPlayerHasReligion);
	stream->Write(m_bOtherPlayerHasOtherReligion);
	stream->Write(m_bOtherPlayerAI);
	stream->Write(m_bPickCity);
	stream->Write(m_bPickOtherPlayerCity);
	stream->Write(m_bShowPlot);
	stream->Write(m_iCityFoodWeight);
	stream->Write(m_bUnitsOnPlot);
	stream->Write(m_bOwnPlot);
	stream->Write(m_bPickReligion);
	stream->Write(m_bStateReligion);
	stream->Write(m_bHolyCity);
	stream->Write(m_bPickCorporation);
	stream->Write(m_bHeadquarters);
	stream->Write(m_bProbabilityUnitMultiply);
	stream->Write(m_bProbabilityBuildingMultiply);
	stream->Write(m_bPrereqEventCity);
	stream->Write(m_aszText.size());
	for (std::vector<CvWString>::iterator it = m_aszText.begin(); it != m_aszText.end(); ++it)
	{
		stream->WriteString(*it);
	}
	for (std::vector<int>::iterator it = m_aiTextEra.begin(); it != m_aiTextEra.end(); ++it)
	{
		stream->Write(*it);
	}
	stream->Write(m_aszWorldNews.size());
	for (std::vector<CvWString>::iterator it = m_aszWorldNews.begin(); it != m_aszWorldNews.end(); ++it)
	{
		stream->WriteString(*it);
	}
	stream->WriteString(m_szPythonCallback);
	stream->WriteString(m_szPythonCanDo);
	stream->WriteString(m_szPythonCanDoCity);
	stream->WriteString(m_szPythonCanDoUnit);
}
#endif
bool CvEventTriggerInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML))
		return false;

	pXML->GetChildXmlValByName(&m_iPercentGamesActive, "iPercentGamesActive");
	pXML->GetChildXmlValByName(&m_iProbability, "iWeight");

	pXML->GetChildXmlValByName(&m_iNumUnits, "iNumUnits");
	pXML->GetChildXmlValByName(&m_iNumBuildings, "iNumBuildings");
	pXML->GetChildXmlValByName(&m_iNumUnitsGlobal, "iNumUnitsGlobal");
	pXML->GetChildXmlValByName(&m_iNumBuildingsGlobal, "iNumBuildingsGlobal");

	pXML->GetChildXmlValByName(&m_iNumPlotsRequired, "iNumPlotsRequired");
	pXML->GetChildXmlValByName(&m_iPlotType, "iPlotType");

	pXML->GetChildXmlValByName(&m_iNumReligions, "iNumReligions");
	pXML->GetChildXmlValByName(&m_iNumCorporations, "iNumCorporations");

	pXML->GetChildXmlValByName(&m_iOtherPlayerShareBorders, "iOtherPlayerShareBorders");

	pXML->GetChildXmlValByName(&m_iMinPopulation, "iMinPopulation");
	pXML->GetChildXmlValByName(&m_iMaxPopulation, "iMaxPopulation");

	pXML->GetChildXmlValByName(&m_iMinMapLandmass, "iMinMapLandmass");
	pXML->GetChildXmlValByName(&m_iMinOurLandmass, "iMinOurLandmass");
	pXML->GetChildXmlValByName(&m_iMaxOurLandmass, "iMaxOurLandmass");

	pXML->SetInfoIDFromChildXmlVal(m_iMinDifficulty, "MinDifficulty");

	pXML->GetChildXmlValByName(&m_iAngry, "iAngry");
	pXML->GetChildXmlValByName(&m_iUnhealthy, "iUnhealthy");
	pXML->GetChildXmlValByName(&m_iUnitDamagedWeight, "iUnitDamagedWeight");
	pXML->GetChildXmlValByName(&m_iUnitDistanceWeight, "iUnitDistanceWeight");
	pXML->GetChildXmlValByName(&m_iUnitExperienceWeight, "iUnitExperienceWeight");
	pXML->GetChildXmlValByName(&m_iMinTreasury, "iMinTreasury");

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"UnitsRequired"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			m_aiUnitsRequired.clear();
			if (iNumSibs > 0)
			{
				CvString szTextVal;
				if (pXML->GetChildXmlVal(szTextVal))
				{
					for (int j = 0; j < iNumSibs; j++)
					{
						m_aiUnitsRequired.push_back(pXML->FindInInfoClass(szTextVal));
						if (!pXML->GetNextXmlVal(szTextVal))
							break;
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"BuildingsRequired"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			m_aiBuildingsRequired.clear();
			if (iNumSibs > 0)
			{
				CvString szTextVal;
				if (pXML->GetChildXmlVal(szTextVal))
				{
					for (int j = 0; j < iNumSibs; j++)
					{
						m_aiBuildingsRequired.push_back(pXML->FindInInfoClass(szTextVal));
						if (!pXML->GetNextXmlVal(szTextVal))
							break;
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"OrPreReqs"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			m_aiPrereqOrTechs.clear();
			if (iNumSibs > 0)
			{
				CvString szTextVal;
				if (pXML->GetChildXmlVal(szTextVal))
				{
					for (int j = 0; j < iNumSibs; j++)
					{
						m_aiPrereqOrTechs.push_back(pXML->FindInInfoClass(szTextVal));
						if (!pXML->GetNextXmlVal(szTextVal))
							break;
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"AndPreReqs"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			m_aiPrereqAndTechs.clear();
			if (iNumSibs > 0)
			{
				CvString szTextVal;
				if (pXML->GetChildXmlVal(szTextVal))
				{
					for (int j = 0; j < iNumSibs; j++)
					{
						m_aiPrereqAndTechs.push_back(pXML->FindInInfoClass(szTextVal));
						if (!pXML->GetNextXmlVal(szTextVal))
							break;
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	pXML->SetInfoIDFromChildXmlVal(m_iOtherPlayerHasTech, "OtherPlayerHasTech");

	pXML->SetInfoIDFromChildXmlVal(m_iCivic, "Civic");

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "ObsoleteTechs"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			m_aiObsoleteTechs.clear();
			if (iNumSibs > 0)
			{
				CvString szTextVal;
				if (pXML->GetChildXmlVal(szTextVal))
				{
					for (int j = 0; j < iNumSibs; j++)
					{
						m_aiObsoleteTechs.push_back(pXML->FindInInfoClass(szTextVal));
						if (!pXML->GetNextXmlVal(szTextVal))
							break;
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"Events"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			m_aiEvents.clear();
			if (iNumSibs > 0)
			{
				CvString szTextVal;
				if (pXML->GetChildXmlVal(szTextVal))
				{
					for (int j = 0; j < iNumSibs; j++)
					{
						m_aiEvents.push_back(pXML->FindInInfoClass(szTextVal));
						if (!pXML->GetNextXmlVal(szTextVal))
							break;
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"PrereqEvents"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			m_aiPrereqEvents.clear();
			if (iNumSibs > 0)
			{
				CvString szTextVal;
				if (pXML->GetChildXmlVal(szTextVal))
				{
					for (int j = 0; j < iNumSibs; j++)
					{
						m_aiPrereqEvents.push_back(pXML->FindInInfoClass(szTextVal));
						if (!pXML->GetNextXmlVal(szTextVal))
							break;
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"FeaturesRequired"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			m_aiFeaturesRequired.clear();
			if (iNumSibs > 0)
			{
				CvString szTextVal;
				if (pXML->GetChildXmlVal(szTextVal))
				{
					for (int j = 0; j < iNumSibs; j++)
					{
						m_aiFeaturesRequired.push_back(pXML->FindInInfoClass(szTextVal));
						if (!pXML->GetNextXmlVal(szTextVal))
							break;
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"TerrainsRequired"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			m_aiTerrainsRequired.clear();
			if (iNumSibs > 0)
			{
				CvString szTextVal;
				if (pXML->GetChildXmlVal(szTextVal))
				{
					for (int j = 0; j < iNumSibs; j++)
					{
						m_aiTerrainsRequired.push_back(pXML->FindInInfoClass(szTextVal));
						if (!pXML->GetNextXmlVal(szTextVal))
						{
							break;
						}
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"ImprovementsRequired"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			m_aiImprovementsRequired.clear();
			if (iNumSibs > 0)
			{
				CvString szTextVal;
				if (pXML->GetChildXmlVal(szTextVal))
				{
					for (int j = 0; j < iNumSibs; j++)
					{
						m_aiImprovementsRequired.push_back(pXML->FindInInfoClass(szTextVal));
						if (!pXML->GetNextXmlVal(szTextVal))
						{
							break;
						}
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"BonusesRequired"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			m_aiBonusesRequired.clear();
			if (iNumSibs > 0)
			{
				CvString szTextVal;
				if (pXML->GetChildXmlVal(szTextVal))
				{
					for (int j = 0; j < iNumSibs; j++)
					{
						m_aiBonusesRequired.push_back(pXML->FindInInfoClass(szTextVal));
						if (!pXML->GetNextXmlVal(szTextVal))
							break;
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"RoutesRequired"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			m_aiRoutesRequired.clear();
			if (iNumSibs > 0)
			{
				CvString szTextVal;
				if (pXML->GetChildXmlVal(szTextVal))
				{
					for (int j = 0; j < iNumSibs; j++)
					{
						m_aiRoutesRequired.push_back(pXML->FindInInfoClass(szTextVal));
						if (!pXML->GetNextXmlVal(szTextVal))
							break;
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"ReligionsRequired"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			m_aiReligionsRequired.clear();
			if (iNumSibs > 0)
			{
				CvString szTextVal;
				if (pXML->GetChildXmlVal(szTextVal))
				{
					for (int j = 0; j < iNumSibs; j++)
					{
						m_aiReligionsRequired.push_back(pXML->FindInInfoClass(szTextVal));
						if (!pXML->GetNextXmlVal(szTextVal))
						{
							break;
						}
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"CorporationsRequired"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			m_aiCorporationsRequired.clear();
			if (iNumSibs > 0)
			{
				CvString szTextVal;
				if (pXML->GetChildXmlVal(szTextVal))
				{
					for (int j = 0; j < iNumSibs; j++)
					{
						m_aiCorporationsRequired.push_back(pXML->FindInInfoClass(szTextVal));
						if (!pXML->GetNextXmlVal(szTextVal))
						{
							break;
						}
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	m_aszText.clear();
	m_aiTextEra.clear();
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"TriggerTexts"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			if (iNumSibs > 0)
			{
				if (gDLL->getXMLIFace()->SetToChild(pXML->GetXML()))
				{
					CvString szTextVal;
					for (int j = 0; j < iNumSibs; ++j)
					{
						if (pXML->GetChildXmlVal(szTextVal))
						{
							m_aszText.push_back(szTextVal);
							pXML->GetNextXmlVal(szTextVal);
							m_aiTextEra.push_back(pXML->FindInInfoClass(szTextVal));

							gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
						}

						if (!gDLL->getXMLIFace()->NextSibling(pXML->GetXML()))
							break;
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	m_aszWorldNews.clear();
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"WorldNewsTexts"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			if (iNumSibs > 0)
			{
				CvString szTextVal;
				if (pXML->GetChildXmlVal(szTextVal))
				{
					for (int j = 0; j<iNumSibs; ++j)
					{
						m_aszWorldNews.push_back(szTextVal);
						if (!pXML->GetNextXmlVal(szTextVal))
							break;
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	pXML->GetChildXmlValByName(&m_bSinglePlayer, "bSinglePlayer");
	pXML->GetChildXmlValByName(&m_bTeam, "bTeam");
	pXML->GetChildXmlValByName(&m_bRecurring, "bRecurring");
	pXML->GetChildXmlValByName(&m_bGlobal, "bGlobal");
	pXML->GetChildXmlValByName(&m_bPickPlayer, "bPickPlayer");
	pXML->GetChildXmlValByName(&m_bOtherPlayerWar, "bOtherPlayerWar");
	pXML->GetChildXmlValByName(&m_bOtherPlayerHasReligion, "bOtherPlayerHasReligion");
	pXML->GetChildXmlValByName(&m_bOtherPlayerHasOtherReligion, "bOtherPlayerHasOtherReligion");
	pXML->GetChildXmlValByName(&m_bOtherPlayerAI, "bOtherPlayerAI");
	pXML->GetChildXmlValByName(&m_bPickCity, "bPickCity");
	pXML->GetChildXmlValByName(&m_bPickOtherPlayerCity, "bPickOtherPlayerCity");
	pXML->GetChildXmlValByName(&m_bShowPlot, "bShowPlot");
	pXML->GetChildXmlValByName(&m_iCityFoodWeight, "iCityFoodWeight");
	pXML->GetChildXmlValByName(&m_bUnitsOnPlot, "bUnitsOnPlot");
	pXML->GetChildXmlValByName(&m_bOwnPlot, "bOwnPlot");
	pXML->GetChildXmlValByName(&m_bPickReligion, "bPickReligion");
	pXML->GetChildXmlValByName(&m_bStateReligion, "bStateReligion");
	pXML->GetChildXmlValByName(&m_bHolyCity, "bHolyCity");
	pXML->GetChildXmlValByName(&m_bPickCorporation, "bPickCorporation");
	pXML->GetChildXmlValByName(&m_bHeadquarters, "bHeadquarters");
	pXML->GetChildXmlValByName(&m_bProbabilityUnitMultiply, "bProbabilityUnitMultiply");
	pXML->GetChildXmlValByName(&m_bProbabilityBuildingMultiply, "bProbabilityBuildingMultiply");
	pXML->GetChildXmlValByName(&m_bPrereqEventCity, "bPrereqEventPlot");

	pXML->GetChildXmlValByName(m_szPythonCallback, "PythonCallback");
	pXML->GetChildXmlValByName(m_szPythonCanDo, "PythonCanDo");
	pXML->GetChildXmlValByName(m_szPythonCanDoCity, "PythonCanDoCity");
	pXML->GetChildXmlValByName(m_szPythonCanDoUnit, "PythonCanDoUnit");

	return true;
}
