// advc.003x: Cut from CvInfos.cpp

#include "CvGameCoreDLL.h"
#include "CvInfo_Terrain.h"
#include "CvXMLLoadUtility.h"


CvTerrainInfo::CvTerrainInfo() :
m_iMovementCost(0),
m_iSeeFromLevel(0),
m_iSeeThroughLevel(0),
m_iBuildModifier(0),
m_iDefenseModifier(0),
m_bWater(false),
m_bImpassable(false),
m_bFound(false),
m_bFoundCoast(false),
m_bFoundFreshWater(false),
m_iWorldSoundscapeScriptId(0),
m_piYields(NULL),
m_piRiverYieldChange(NULL),
m_piHillsYieldChange(NULL),
m_pi3DAudioScriptFootstepIndex(NULL)
{}

CvTerrainInfo::~CvTerrainInfo()
{
	SAFE_DELETE_ARRAY(m_piYields);
	SAFE_DELETE_ARRAY(m_piRiverYieldChange);
	SAFE_DELETE_ARRAY(m_piHillsYieldChange);
	SAFE_DELETE_ARRAY(m_pi3DAudioScriptFootstepIndex);
}

const TCHAR* CvTerrainInfo::getArtDefineTag() const
{
	return m_szArtDefineTag;
}

int CvTerrainInfo::getWorldSoundscapeScriptId() const
{
	return m_iWorldSoundscapeScriptId;
}

int CvTerrainInfo::getYield(int i) const
{
	FAssertBounds(0, NUM_YIELD_TYPES, i);
	return m_piYields ? m_piYields[i] : 0; // advc.003t
}

int CvTerrainInfo::getRiverYieldChange(int i) const
{
	FAssertBounds(0, NUM_YIELD_TYPES, i);
	return m_piRiverYieldChange ? m_piRiverYieldChange[i] : 0; // advc.003t
}

int CvTerrainInfo::getHillsYieldChange(int i) const
{
	FAssertBounds(0, NUM_YIELD_TYPES, i);
	return m_piHillsYieldChange ? m_piHillsYieldChange[i] : 0; // advc.003t
}

int CvTerrainInfo::get3DAudioScriptFootstepIndex(int i) const
{
	FAssertBounds(0, GC.getNumFootstepAudioTypes(), i); // advc: Check for upper bound added
	return m_pi3DAudioScriptFootstepIndex ? m_pi3DAudioScriptFootstepIndex[i]
			: 0; // advc.003t: see get3DAudioScriptFootstepIndex
}

bool CvTerrainInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML))
		return false;

	pXML->GetChildXmlValByName(m_szArtDefineTag, "ArtDefineTag");

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),
		"Yields"))
	{
		pXML->SetYieldArray(&m_piYields);
	}
	else pXML->InitList(&m_piYields, NUM_YIELD_TYPES);

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),
		"RiverYieldChange"))
	{
		pXML->SetYieldArray(&m_piRiverYieldChange);
	}
	else pXML->InitList(&m_piRiverYieldChange, NUM_YIELD_TYPES);

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),
		"HillsYieldChange"))
	{
		pXML->SetYieldArray(&m_piHillsYieldChange);
	}
	else pXML->InitList(&m_piHillsYieldChange, NUM_YIELD_TYPES);

	pXML->GetChildXmlValByName(&m_bWater, "bWater");
	pXML->GetChildXmlValByName(&m_bImpassable, "bImpassable");
	pXML->GetChildXmlValByName(&m_bFound, "bFound");
	pXML->GetChildXmlValByName(&m_bFoundCoast, "bFoundCoast");
	pXML->GetChildXmlValByName(&m_bFoundFreshWater, "bFoundFreshWater");

	pXML->GetChildXmlValByName(&m_iMovementCost, "iMovement");
	pXML->GetChildXmlValByName(&m_iSeeFromLevel, "iSeeFrom");
	pXML->GetChildXmlValByName(&m_iSeeThroughLevel, "iSeeThrough");
	pXML->GetChildXmlValByName(&m_iBuildModifier, "iBuildModifier");
	pXML->GetChildXmlValByName(&m_iDefenseModifier, "iDefense");

	pXML->SetVariableListTagPairForAudioScripts(&m_pi3DAudioScriptFootstepIndex, "FootstepSounds", GC.getNumFootstepAudioTypes());
	{
		CvString szTextVal;
		pXML->GetChildXmlValByName(szTextVal, "WorldSoundscapeAudioScript", /* advc.006b: */ "");
		if (szTextVal.GetLength() > 0)
			m_iWorldSoundscapeScriptId = gDLL->getAudioTagIndex(szTextVal.GetCString(), AUDIOTAG_SOUNDSCAPE);
		else m_iWorldSoundscapeScriptId = -1;
	}
	return true;
}

const TCHAR* CvTerrainInfo::getButton() const
{
	const CvArtInfoTerrain* pTerrainArtInfo = getArtInfo();
	if (pTerrainArtInfo != NULL)
		return pTerrainArtInfo->getButton();

	return NULL;
}

const CvArtInfoTerrain* CvTerrainInfo::getArtInfo() const
{
	return ARTFILEMGR.getTerrainArtInfo(getArtDefineTag());
}

CvFeatureInfo::CvFeatureInfo() :
m_iMovementCost(0),
m_iSeeThroughChange(0),
m_iHealthPercent(0),
m_iAppearanceProbability(0),
m_iDisappearanceProbability(0),
m_iGrowthProbability(0),
m_iDefenseModifier(0),
m_iRivalDefenseModifier(0), // advc.012
m_iAdvancedStartRemoveCost(0),
m_iTurnDamage(0),
m_iWarmingDefense(0), //GWMod
m_bNoCoast(false),
m_bNoRiver(false),
m_bNoRiverSide(false), // advc.129b
m_bNoAdjacent(false),
m_bRequiresFlatlands(false),
m_bRequiresRiver(false),
m_bRequiresRiverSide(false), // advc.129b
m_bAddsFreshWater(false),
m_bImpassable(false),
m_bNoCity(false),
m_bNoImprovement(false),
m_bVisibleAlways(false),
m_bNukeImmune(false),
m_iWorldSoundscapeScriptId(0),
m_iEffectProbability(0),
m_piYieldChange(NULL),
m_piRiverYieldChange(NULL),
m_piHillsYieldChange(NULL),
m_pi3DAudioScriptFootstepIndex(NULL),
m_pbTerrain(NULL)
{}

CvFeatureInfo::~CvFeatureInfo()
{
	SAFE_DELETE_ARRAY(m_piYieldChange);
	SAFE_DELETE_ARRAY(m_piRiverYieldChange);
	SAFE_DELETE_ARRAY(m_piHillsYieldChange);
	SAFE_DELETE_ARRAY(m_pi3DAudioScriptFootstepIndex);
	SAFE_DELETE_ARRAY(m_pbTerrain);
}

int CvFeatureInfo::getAppearanceProbability() const
{
	return m_iAppearanceProbability;
}

int CvFeatureInfo::getDisappearanceProbability() const
{
	return m_iDisappearanceProbability;
}

int CvFeatureInfo::getGrowthProbability() const
{
	return m_iGrowthProbability;
}

int CvFeatureInfo::getAdvancedStartRemoveCost() const
{
	return m_iAdvancedStartRemoveCost;
}

int CvFeatureInfo::getTurnDamage() const
{
	return m_iTurnDamage;
}

int CvFeatureInfo::getWarmingDefense() const //GWMod
{
	return m_iWarmingDefense;
}

bool CvFeatureInfo::isNoCoast() const
{
	return m_bNoCoast;
}

bool CvFeatureInfo::isNoRiver() const
{
	return m_bNoRiver;
}
// advc.129b:
bool CvFeatureInfo::isNoRiverSide() const
{
	return m_bNoRiverSide;
}

bool CvFeatureInfo::isNoAdjacent() const
{
	return m_bNoAdjacent;
}

bool CvFeatureInfo::isRequiresFlatlands() const
{
	return m_bRequiresFlatlands;
}

bool CvFeatureInfo::isRequiresRiver() const
{
	return m_bRequiresRiver;
}
// advc.129b:
bool CvFeatureInfo::isRequiresRiverSide() const
{
	return m_bRequiresRiverSide;
}

bool CvFeatureInfo::isAddsFreshWater() const
{
	return m_bAddsFreshWater;
}

bool CvFeatureInfo::isNoCity() const
{
	return m_bNoCity;
}

bool CvFeatureInfo::isVisibleAlways() const
{
	return m_bVisibleAlways;
}

bool CvFeatureInfo::isNukeImmune() const
{
	return m_bNukeImmune;
}

const TCHAR* CvFeatureInfo::getOnUnitChangeTo() const
{
	return m_szOnUnitChangeTo;
}

const TCHAR* CvFeatureInfo::getArtDefineTag() const
{
	return m_szArtDefineTag;
}

int CvFeatureInfo::getWorldSoundscapeScriptId() const
{
	return m_iWorldSoundscapeScriptId;
}

const TCHAR* CvFeatureInfo::getEffectType() const
{
	return m_szEffectType;
}

int CvFeatureInfo::getEffectProbability() const
{
	return m_iEffectProbability;
}

int CvFeatureInfo::get3DAudioScriptFootstepIndex(int i) const
{
	FAssertBounds(0, GC.getNumFootstepAudioTypes(), i); // advc: Check for upper bound added
	return m_pi3DAudioScriptFootstepIndex ? m_pi3DAudioScriptFootstepIndex[i]
			// advc.003t: Was -1. CvTerrainInfo::read sets 0 as the default, so 0 works apparently.
			: 0;
}

bool CvFeatureInfo::isTerrain(int i) const
{
	FAssertBounds(0, GC.getNumTerrainInfos(), i);
	return m_pbTerrain ? m_pbTerrain[i] : false;
}

int CvFeatureInfo::getNumVarieties() const
{
	return getArtInfo()->getNumVarieties();
}

const TCHAR* CvFeatureInfo::getButton() const
{
	const CvArtInfoFeature* pFeatureArtInfo = getArtInfo();
	if (pFeatureArtInfo != NULL)
		return pFeatureArtInfo->getButton();

	else return NULL;
}

const CvArtInfoFeature* CvFeatureInfo::getArtInfo() const
{
	return ARTFILEMGR.getFeatureArtInfo( getArtDefineTag());
}

bool CvFeatureInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML))
		return false;

	pXML->GetChildXmlValByName(m_szArtDefineTag, "ArtDefineTag");

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),
		"YieldChanges"))
	{
		pXML->SetYieldArray(&m_piYieldChange);
	}
	else
	{
		pXML->InitList(&m_piYieldChange, NUM_YIELD_TYPES);
	}

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),
		"RiverYieldChange"))
	{
		pXML->SetYieldArray(&m_piRiverYieldChange);
	}
	else
	{
		pXML->InitList(&m_piRiverYieldChange, NUM_YIELD_TYPES);
	}

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),
		"HillsYieldChange"))
	{
		pXML->SetYieldArray(&m_piHillsYieldChange);
	}
	else pXML->InitList(&m_piHillsYieldChange, NUM_YIELD_TYPES);

	pXML->GetChildXmlValByName(&m_iMovementCost, "iMovement");
	pXML->GetChildXmlValByName(&m_iSeeThroughChange, "iSeeThrough");
	pXML->GetChildXmlValByName(&m_iHealthPercent, "iHealthPercent");
	pXML->GetChildXmlValByName(&m_iDefenseModifier, "iDefense");
	// advc.012:
	pXML->GetChildXmlValByName(&m_iRivalDefenseModifier, "iRivalDefense", 0);
	pXML->GetChildXmlValByName(&m_iAdvancedStartRemoveCost, "iAdvancedStartRemoveCost");
	pXML->GetChildXmlValByName(&m_iTurnDamage, "iTurnDamage");
	pXML->GetChildXmlValByName(&m_iWarmingDefense, "iWarmingDefense", // GWMod new xml field M.A.
			0); // advc: Default value; now optional.
	pXML->GetChildXmlValByName(&m_iAppearanceProbability, "iAppearance");
	pXML->GetChildXmlValByName(&m_iDisappearanceProbability, "iDisappearance");
	pXML->GetChildXmlValByName(&m_iGrowthProbability, "iGrowth");
	pXML->GetChildXmlValByName(&m_bNoCoast, "bNoCoast");
	// advc.129b:
	pXML->GetChildXmlValByName(&m_bNoRiverSide, "bNoRiverSide", false);
	pXML->GetChildXmlValByName(&m_bNoRiver, "bNoRiver");
	// <advc.129b> Make sure these are consistent
	if (m_bNoRiver)
		m_bNoRiverSide = true; // </advc.129b>
	pXML->GetChildXmlValByName(&m_bNoAdjacent, "bNoAdjacent");
	pXML->GetChildXmlValByName(&m_bRequiresFlatlands, "bRequiresFlatlands");
	pXML->GetChildXmlValByName(&m_bRequiresRiver, "bRequiresRiver");
	// <advc.129b>
	pXML->GetChildXmlValByName(&m_bRequiresRiverSide, "bRequiresRiverSide", false);
	if (m_bRequiresRiverSide)
		m_bRequiresRiver = true; // </advc.129b>
	pXML->GetChildXmlValByName(&m_bAddsFreshWater, "bAddsFreshWater");
	pXML->GetChildXmlValByName(&m_bImpassable, "bImpassable");
	pXML->GetChildXmlValByName(&m_bNoCity, "bNoCity");
	pXML->GetChildXmlValByName(&m_bNoImprovement, "bNoImprovement");
	pXML->GetChildXmlValByName(&m_bVisibleAlways, "bVisibleAlways");
	pXML->GetChildXmlValByName(&m_bNukeImmune, "bNukeImmune");
	pXML->GetChildXmlValByName(m_szOnUnitChangeTo, "OnUnitChangeTo");

	pXML->SetVariableListTagPairForAudioScripts(&m_pi3DAudioScriptFootstepIndex, "FootstepSounds", GC.getNumFootstepAudioTypes());
	{
		CvString szTextVal;
		pXML->GetChildXmlValByName(szTextVal, "WorldSoundscapeAudioScript", /* advc.006b: */ "");
		if (szTextVal.GetLength() > 0)
			m_iWorldSoundscapeScriptId = gDLL->getAudioTagIndex(szTextVal.GetCString(), AUDIOTAG_SOUNDSCAPE);
		else m_iWorldSoundscapeScriptId = -1;
	}
	pXML->GetChildXmlValByName(m_szEffectType, "EffectType");
	pXML->GetChildXmlValByName(&m_iEffectProbability, "iEffectProbability");

	pXML->SetVariableListTagPair(&m_pbTerrain, "TerrainBooleans", GC.getNumTerrainInfos());

	return true;
}

CvBonusInfo::CvBonusInfo() :
m_eBonusClassType(NO_BONUSCLASS),
m_wcSymbol(0),
m_eTechReveal(NO_TECH),
m_eTechCityTrade(NO_TECH),
m_eTechObsolete(NO_TECH),
m_eeTechImprove(std::make_pair(NO_TECH, NO_TECH)), // advc.003w
m_iAITradeModifier(0),
m_iAIObjective(0),
m_iHealth(0),
m_iHappiness(0),
m_iMinAreaSize(0),
m_iMinLatitude(0),
m_iMaxLatitude(90),
m_iPlacementOrder(0),
m_iConstAppearance(0),
m_iRandAppearance1(0),
m_iRandAppearance2(0),
m_iRandAppearance3(0),
m_iRandAppearance4(0),
m_iPercentPerPlayer(0),
m_iTilesPer(0),
m_iMinLandPercent(0),
m_iUniqueRange(0),
m_iGroupRange(0),
m_iGroupRand(0),
m_bOneArea(false),
m_bHills(false),
m_bFlatlands(false),
m_bNoRiverSide(false),
m_bNormalize(false),
m_piYieldChange(NULL),
m_pbTerrain(NULL),
m_pbFeature(NULL),
m_pbFeatureTerrain(NULL)
{}

CvBonusInfo::~CvBonusInfo()
{
	SAFE_DELETE_ARRAY(m_piYieldChange);
	SAFE_DELETE_ARRAY(m_pbTerrain);
	SAFE_DELETE_ARRAY(m_pbFeature);
	SAFE_DELETE_ARRAY(m_pbFeatureTerrain); // free memory - MT
}

wchar CvBonusInfo::getChar() const
{
	return m_wcSymbol;
}

void CvBonusInfo::setChar(wchar wc)
{
	m_wcSymbol = wc;
}

int CvBonusInfo::getAITradeModifier() const
{
	return m_iAITradeModifier;
}

int CvBonusInfo::getAIObjective() const
{
	return m_iAIObjective;
}

int CvBonusInfo::getMinAreaSize() const
{
	return m_iMinAreaSize;
}

int CvBonusInfo::getMinLatitude() const
{
	return m_iMinLatitude;
}

int CvBonusInfo::getMaxLatitude() const
{
	return m_iMaxLatitude;
}

int CvBonusInfo::getPlacementOrder() const
{
	return m_iPlacementOrder;
}

int CvBonusInfo::getConstAppearance() const
{
	return m_iConstAppearance;
}

int CvBonusInfo::getRandAppearance1() const
{
	return m_iRandAppearance1;
}

int CvBonusInfo::getRandAppearance2() const
{
	return m_iRandAppearance2;
}

int CvBonusInfo::getRandAppearance3() const
{
	return m_iRandAppearance3;
}

int CvBonusInfo::getRandAppearance4() const
{
	return m_iRandAppearance4;
}

int CvBonusInfo::getPercentPerPlayer() const
{
	return m_iPercentPerPlayer;
}

int CvBonusInfo::getTilesPer() const
{
	return m_iTilesPer;
}

int CvBonusInfo::getMinLandPercent() const
{
	return m_iMinLandPercent;
}

int CvBonusInfo::getUniqueRange() const
{
	return m_iUniqueRange;
}

int CvBonusInfo::getGroupRange() const
{
	return m_iGroupRange;
}

int CvBonusInfo::getGroupRand() const
{
	return m_iGroupRand;
}

bool CvBonusInfo::isOneArea() const
{
	return m_bOneArea;
}

bool CvBonusInfo::isHills() const
{
	return m_bHills;
}

bool CvBonusInfo::isFlatlands() const
{
	return m_bFlatlands;
}

bool CvBonusInfo::isNoRiverSide() const
{
	return m_bNoRiverSide;
}

bool CvBonusInfo::isNormalize() const
{
	return m_bNormalize;
}

const TCHAR* CvBonusInfo::getArtDefineTag() const
{
	return m_szArtDefineTag;
}

const CvArtInfoBonus* CvBonusInfo::getArtInfo() const
{
	return ARTFILEMGR.getBonusArtInfo( getArtDefineTag());
}

int CvBonusInfo::getYieldChange(int i) const
{
	FAssertBounds(0, NUM_YIELD_TYPES, i);
	return m_piYieldChange ? m_piYieldChange[i] : 0; // advc.003t
}

int* CvBonusInfo::getYieldChangeArray()
{
	return m_piYieldChange;
}

bool CvBonusInfo::isTerrain(int i) const
{
	FAssertBounds(0, GC.getNumTerrainInfos(), i);
	return m_pbTerrain ? m_pbTerrain[i] : false;
}

bool CvBonusInfo::isFeature(int i) const
{
	FAssertBounds(0, GC.getNumFeatureInfos(), i);
	return m_pbFeature ? m_pbFeature[i] : false;
}

bool CvBonusInfo::isFeatureTerrain(int i) const
{
	FAssertBounds(0, GC.getNumTerrainInfos(), i);
	return m_pbFeatureTerrain ?	m_pbFeatureTerrain[i] : false;
}

const TCHAR* CvBonusInfo::getButton() const
{
	const CvArtInfoBonus* pBonusArtInfo = getArtInfo();
	if (pBonusArtInfo != NULL)
		return pBonusArtInfo->getButton();

	return NULL;
}
#if ENABLE_XML_FILE_CACHE
void CvBonusInfo::read(FDataStreamBase* stream)
{
	base_t::read(stream);
	uint uiFlag=0;
	stream->Read(&uiFlag);

	stream->Read((int*)&m_eBonusClassType);
	{
		int iSymbol;
		stream->Read(&iSymbol);
		m_wcSymbol = safeIntCast<wchar>(iSymbol);
	}
	stream->Read((int*)&m_eTechReveal);
	stream->Read((int*)&m_eTechCityTrade);
	stream->Read((int*)&m_eTechObsolete);
	stream->Read(&m_iAITradeModifier);
	stream->Read(&m_iAIObjective);
	stream->Read(&m_iHealth);
	stream->Read(&m_iHappiness);
	stream->Read(&m_iMinAreaSize);
	stream->Read(&m_iMinLatitude);
	stream->Read(&m_iMaxLatitude);
	stream->Read(&m_iPlacementOrder);
	stream->Read(&m_iConstAppearance);
	stream->Read(&m_iRandAppearance1);
	stream->Read(&m_iRandAppearance2);
	stream->Read(&m_iRandAppearance3);
	stream->Read(&m_iRandAppearance4);
	stream->Read(&m_iPercentPerPlayer);
	stream->Read(&m_iTilesPer);
	stream->Read(&m_iMinLandPercent);
	stream->Read(&m_iUniqueRange);
	stream->Read(&m_iGroupRange);
	stream->Read(&m_iGroupRand);
	stream->Read(&m_bOneArea);
	stream->Read(&m_bHills);
	stream->Read(&m_bFlatlands);
	stream->Read(&m_bNoRiverSide);
	stream->Read(&m_bNormalize);
	stream->ReadString(m_szArtDefineTag);
	SAFE_DELETE_ARRAY(m_piYieldChange);
	m_piYieldChange = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_piYieldChange);
	SAFE_DELETE_ARRAY(m_pbTerrain);
	m_pbTerrain = new bool[GC.getNumTerrainInfos()];
	stream->Read(GC.getNumTerrainInfos(), m_pbTerrain);
	SAFE_DELETE_ARRAY(m_pbFeature);
	m_pbFeature = new bool[GC.getNumFeatureInfos()];
	stream->Read(GC.getNumFeatureInfos(), m_pbFeature);
	SAFE_DELETE_ARRAY(m_pbFeatureTerrain);
	m_pbFeatureTerrain = new bool[GC.getNumTerrainInfos()];
	stream->Read(GC.getNumTerrainInfos(), m_pbFeatureTerrain);
}

void CvBonusInfo::write(FDataStreamBase* stream)
{
	base_t::write(stream);
	uint uiFlag=0;
	stream->Write(uiFlag);

	stream->Write(m_eBonusClassType);
	{
		int iSymbol = m_wcSymbol;
		stream->Write(iSymbol);
	}
	stream->Write(m_eTechReveal);
	stream->Write(m_eTechCityTrade);
	stream->Write(m_eTechObsolete);
	stream->Write(m_iAITradeModifier);
	stream->Write(m_iAIObjective);
	stream->Write(m_iHealth);
	stream->Write(m_iHappiness);
	stream->Write(m_iMinAreaSize);
	stream->Write(m_iMinLatitude);
	stream->Write(m_iMaxLatitude);
	stream->Write(m_iPlacementOrder);
	stream->Write(m_iConstAppearance);
	stream->Write(m_iRandAppearance1);
	stream->Write(m_iRandAppearance2);
	stream->Write(m_iRandAppearance3);
	stream->Write(m_iRandAppearance4);
	stream->Write(m_iPercentPerPlayer);
	stream->Write(m_iTilesPer);
	stream->Write(m_iMinLandPercent);
	stream->Write(m_iUniqueRange);
	stream->Write(m_iGroupRange);
	stream->Write(m_iGroupRand);
	stream->Write(m_bOneArea);
	stream->Write(m_bHills);
	stream->Write(m_bFlatlands);
	stream->Write(m_bNoRiverSide);
	stream->Write(m_bNormalize);
	stream->WriteString(m_szArtDefineTag);
	stream->Write(NUM_YIELD_TYPES, m_piYieldChange);
	stream->Write(GC.getNumTerrainInfos(), m_pbTerrain);
	stream->Write(GC.getNumFeatureInfos(), m_pbFeature);
	stream->Write(GC.getNumTerrainInfos(), m_pbFeatureTerrain);
}
#endif
bool CvBonusInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML))
		return false;

	pXML->SetInfoIDFromChildXmlVal(m_eBonusClassType, "BonusClassType");

	pXML->GetChildXmlValByName(m_szArtDefineTag, "ArtDefineTag");

	pXML->SetInfoIDFromChildXmlVal(m_eTechReveal, "TechReveal");
	pXML->SetInfoIDFromChildXmlVal(m_eTechCityTrade, "TechCityTrade");
	pXML->SetInfoIDFromChildXmlVal(m_eTechObsolete, "TechObsolete");

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),
		"YieldChanges"))
	{
		pXML->SetYieldArray(&m_piYieldChange);
	}
	else pXML->InitList(&m_piYieldChange, NUM_YIELD_TYPES);

	pXML->GetChildXmlValByName(&m_iAITradeModifier, "iAITradeModifier");
	pXML->GetChildXmlValByName(&m_iAIObjective, "iAIObjective");
	pXML->GetChildXmlValByName(&m_iHealth, "iHealth");
	pXML->GetChildXmlValByName(&m_iHappiness, "iHappiness");
	pXML->GetChildXmlValByName(&m_iMinAreaSize, "iMinAreaSize");
	pXML->GetChildXmlValByName(&m_iMinLatitude, "iMinLatitude");
	pXML->GetChildXmlValByName(&m_iMaxLatitude, "iMaxLatitude", 90);
	pXML->GetChildXmlValByName(&m_iPlacementOrder, "iPlacementOrder");
	pXML->GetChildXmlValByName(&m_iConstAppearance, "iConstAppearance");

	// if we can set the current xml node to it's next sibling
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"Rands"))
	{
		pXML->GetChildXmlValByName(&m_iRandAppearance1, "iRandApp1");
		pXML->GetChildXmlValByName(&m_iRandAppearance2, "iRandApp2");
		pXML->GetChildXmlValByName(&m_iRandAppearance3, "iRandApp3");
		pXML->GetChildXmlValByName(&m_iRandAppearance4, "iRandApp4");

		// set the current xml node to it's parent node
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	pXML->GetChildXmlValByName(&m_iPercentPerPlayer, "iPlayer");
	pXML->GetChildXmlValByName(&m_iTilesPer, "iTilesPer");
	pXML->GetChildXmlValByName(&m_iMinLandPercent, "iMinLandPercent");
	pXML->GetChildXmlValByName(&m_iUniqueRange, "iUnique");
	pXML->GetChildXmlValByName(&m_iGroupRange, "iGroupRange");
	pXML->GetChildXmlValByName(&m_iGroupRand, "iGroupRand");
	pXML->GetChildXmlValByName(&m_bOneArea, "bArea");
	pXML->GetChildXmlValByName(&m_bHills, "bHills");
	pXML->GetChildXmlValByName(&m_bFlatlands, "bFlatlands");
	pXML->GetChildXmlValByName(&m_bNoRiverSide, "bNoRiverSide");
	pXML->GetChildXmlValByName(&m_bNormalize, "bNormalize");

	pXML->SetVariableListTagPair(&m_pbTerrain, "TerrainBooleans", GC.getNumTerrainInfos());
	pXML->SetVariableListTagPair(&m_pbFeature, "FeatureBooleans", GC.getNumFeatureInfos());
	pXML->SetVariableListTagPair(&m_pbFeatureTerrain, "FeatureTerrainBooleans", GC.getNumTerrainInfos());

	return true;
}

// <advc.003w>
TechTypes CvBonusInfo::getTechImprove(bool bWater) const
{
	return (bWater ? m_eeTechImprove.second : m_eeTechImprove.first);
}

void CvBonusInfo::updateCache(BonusTypes eBonus)
{
	std::pair<int,int> iiLowestTechCost = std::make_pair(MAX_INT, MAX_INT);
	FOR_EACH_ENUM2(Build, eBuild)
	{
		CvBuildInfo const& kBuild = GC.getInfo(eBuild);
		TechTypes eBuildTech = kBuild.getTechPrereq();
		if (eBuildTech == NO_TECH)
			continue;
		ImprovementTypes eImprov = kBuild.getImprovement();
		if (eImprov == NO_IMPROVEMENT)
			continue;
		CvImprovementInfo const& kImprov = GC.getInfo(eImprov);
		bool bAnyImprovYield = false;
		FOR_EACH_ENUM(Yield)
		{
			if (kImprov.getImprovementBonusYield(eBonus,eLoopYield) > 0)
			{
				bAnyImprovYield = true;
				break;
			}
		}
		if (!bAnyImprovYield)
			continue;
		int iTechCost = GC.getInfo(eBuildTech).getResearchCost();
		if (kImprov.isWater())
		{
			if (iTechCost < iiLowestTechCost.second)
			{
				iiLowestTechCost.second = iTechCost;
				m_eeTechImprove.second = eBuildTech;
			}
		}
		else
		{
			if (iTechCost < iiLowestTechCost.first)
			{
				iiLowestTechCost.first = iTechCost;
				m_eeTechImprove.first = eBuildTech;
			}
		}
	}
	if (m_eTechReveal == NO_TECH)
		return;
	// Will have to reveal (but not trade) the resource in order to improve it
	int iRevealTechCost = GC.getInfo(m_eTechReveal).getResearchCost();
	if (m_eeTechImprove.first == NO_TECH || iRevealTechCost > iiLowestTechCost.first)
		m_eeTechImprove.first = m_eTechReveal;
	if (m_eeTechImprove.second == NO_TECH || iRevealTechCost > iiLowestTechCost.second)
		m_eeTechImprove.second = m_eTechReveal;
} // </advc.003w>

CvBonusClassInfo::CvBonusClassInfo() : m_iUniqueRange(0) {}


int CvBonusClassInfo::getUniqueRange() const
{
	return m_iUniqueRange;
}

bool CvBonusClassInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML))
		return false;
	pXML->GetChildXmlValByName(&m_iUniqueRange, "iUnique");
	return true;
}

CvRouteInfo::CvRouteInfo() :
m_iAdvancedStartCost(0),
m_iAdvancedStartCostIncrease(0),
m_iValue(0),
m_iMovementCost(0),
m_iFlatMovementCost(0),
m_eRoutePillage(NO_ROUTE), // advc.255
m_ePrereqBonus(NO_BONUS),
m_piYieldChange(NULL),
m_piTechMovementChange(NULL)
{}

CvRouteInfo::~CvRouteInfo()
{
	SAFE_DELETE_ARRAY(m_piYieldChange);
	SAFE_DELETE_ARRAY(m_piTechMovementChange);
}

int CvRouteInfo::getAdvancedStartCost() const
{
	return m_iAdvancedStartCost;
}

int CvRouteInfo::getAdvancedStartCostIncrease() const
{
	return m_iAdvancedStartCostIncrease;
}

int CvRouteInfo::getValue() const
{
	return m_iValue;
}

int CvRouteInfo::getYieldChange(int i) const
{
	FAssertBounds(0, NUM_YIELD_TYPES, i);
	return m_piYieldChange ? m_piYieldChange[i] : 0; // advc.003t
}

int CvRouteInfo::getTechMovementChange(int i) const
{
	FAssertBounds(0, GC.getNumTechInfos(), i);
	return m_piTechMovementChange ? m_piTechMovementChange[i] : 0; // advc.003t
}

// advc.003t: Calls from Python aren't going to respect the bounds
int CvRouteInfo::py_getPrereqOrBonus(int i) const
{
	if (i < 0 || i >= getNumPrereqOrBonuses())
		return NO_BONUS;
	return m_aePrereqOrBonuses[i];
}

bool CvRouteInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML))
		return false;

	pXML->GetChildXmlValByName(&m_iAdvancedStartCost, "iAdvancedStartCost");
	pXML->GetChildXmlValByName(&m_iAdvancedStartCostIncrease, "iAdvancedStartCostIncrease");

	pXML->GetChildXmlValByName(&m_iValue, "iValue");
	pXML->GetChildXmlValByName(&m_iMovementCost, "iMovement");
	pXML->GetChildXmlValByName(&m_iFlatMovementCost, "iFlatMovement");

	pXML->SetInfoIDFromChildXmlVal(m_ePrereqBonus, "BonusType");

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),
		"Yields"))
	{
		pXML->SetYieldArray(&m_piYieldChange);
	}
	else pXML->InitList(&m_piYieldChange, NUM_YIELD_TYPES);

	pXML->SetVariableListTagPair(&m_piTechMovementChange, "TechMovementChanges", GC.getNumTechInfos());

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"PrereqOrBonuses"))
	{
		if (pXML->SkipToNextVal())
		{
			int const iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			if (iNumSibs > 0)
			{
				CvString szTextVal;
				if (pXML->GetChildXmlVal(szTextVal))
				{	// advc.003t: The DLL can handle any number, but Python maybe not.
					FAssert(iNumSibs <= GC.getDefineINT(CvGlobals::NUM_ROUTE_PREREQ_OR_BONUSES));
					for (int j = 0; j < iNumSibs; j++)
					{	// <advc.003t>
						BonusTypes eBonus = (BonusTypes)pXML->FindInInfoClass(szTextVal);
						if (eBonus != NO_BONUS)
							m_aePrereqOrBonuses.push_back(eBonus); // </advc.003t>
						if (!pXML->GetNextXmlVal(szTextVal))
							break;
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	return true;
}

// advc.255:
bool CvRouteInfo::readPass2(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	pXML->GetChildXmlValByName(szTextVal, "RoutePillage", "");
	m_eRoutePillage = (RouteTypes)GC.getInfoTypeForString(szTextVal);
	return true;
}


CvImprovementInfo::CvImprovementInfo() :
m_iAdvancedStartCost(0),
m_iAdvancedStartCostIncrease(0),
m_iTilesPerGoody(0),
m_iGoodyUniqueRange(0),
m_iFeatureGrowthProbability(0),
m_iUpgradeTime(0),
m_iAirBombDefense(0),
m_iDefenseModifier(0),
m_iHappiness(0),
m_iPillageGold(0),
m_eImprovementPillage(NO_IMPROVEMENT),
m_eImprovementUpgrade(NO_IMPROVEMENT),
m_bActsAsCity(false), // advc: was true
m_bHillsMakesValid(false),
m_bFreshWaterMakesValid(false),
m_bRiverSideMakesValid(false),
m_bNoFreshWater(false),
m_bRequiresFlatlands(false),
m_bRequiresRiverSide(false),
m_bRequiresIrrigation(false),
m_bCarriesIrrigation(false),
m_bRequiresFeature(false),
m_bWater(false),
m_bGoody(false),
m_bPermanent(false),
m_bOutsideBorders(false),
m_iWorldSoundscapeScriptId(0),
m_piPrereqNatureYield(NULL),
m_piYieldChange(NULL),
m_piRiverSideYieldChange(NULL),
m_piHillsYieldChange(NULL),
m_piIrrigatedChange(NULL),
m_pbTerrainMakesValid(NULL),
m_pbFeatureMakesValid(NULL),
m_ppiTechYieldChanges(NULL),
m_ppiRouteYieldChanges(NULL),
m_paImprovementBonus(NULL)
{}

CvImprovementInfo::~CvImprovementInfo()
{
	SAFE_DELETE_ARRAY(m_piPrereqNatureYield);
	SAFE_DELETE_ARRAY(m_piYieldChange);
	SAFE_DELETE_ARRAY(m_piRiverSideYieldChange);
	SAFE_DELETE_ARRAY(m_piHillsYieldChange);
	SAFE_DELETE_ARRAY(m_piIrrigatedChange);
	SAFE_DELETE_ARRAY(m_pbTerrainMakesValid);
	SAFE_DELETE_ARRAY(m_pbFeatureMakesValid);

	if (m_paImprovementBonus != NULL)
	{
		SAFE_DELETE_ARRAY(m_paImprovementBonus); // XXX make sure this isn't leaking memory...
		// ^advc: Should be fine; ~CvImprovementBonusInfo gets called.
	}
	if (m_ppiTechYieldChanges != NULL)
	{
		for (int iI = 0; iI < GC.getNumTechInfos(); iI++)
			SAFE_DELETE_ARRAY(m_ppiTechYieldChanges[iI]);
		SAFE_DELETE_ARRAY(m_ppiTechYieldChanges);
	}

	if (m_ppiRouteYieldChanges != NULL)
	{
		for (int iI = 0; iI < GC.getNumRouteInfos(); iI++)
			SAFE_DELETE_ARRAY(m_ppiRouteYieldChanges[iI]);
		SAFE_DELETE_ARRAY(m_ppiRouteYieldChanges);
	}
}

int CvImprovementInfo::getAdvancedStartCost() const
{
	return m_iAdvancedStartCost;
}

int CvImprovementInfo::getAdvancedStartCostIncrease() const
{
	return m_iAdvancedStartCostIncrease;
}

int CvImprovementInfo::getTilesPerGoody() const
{
	return m_iTilesPerGoody;
}

int CvImprovementInfo::getGoodyUniqueRange() const
{
	return m_iGoodyUniqueRange;
}

int CvImprovementInfo::getFeatureGrowthProbability() const
{
	return m_iFeatureGrowthProbability;
}

int CvImprovementInfo::getPillageGold() const
{
	return m_iPillageGold;
}

const TCHAR* CvImprovementInfo::getArtDefineTag() const
{
	return m_szArtDefineTag;
}

int CvImprovementInfo::getWorldSoundscapeScriptId() const
{
	return m_iWorldSoundscapeScriptId;
}

int CvImprovementInfo::getPrereqNatureYield(int i) const
{
	FAssertBounds(0, NUM_YIELD_TYPES, i);
	return m_piPrereqNatureYield ? m_piPrereqNatureYield[i] : 0; // advc.003t
}

int CvImprovementInfo::getYieldChange(int i) const
{
	FAssertBounds(0, NUM_YIELD_TYPES, i);
	return m_piYieldChange ? m_piYieldChange[i] : 0; // advc.003t
}

int CvImprovementInfo::getRiverSideYieldChange(int i) const
{
	FAssertBounds(0, NUM_YIELD_TYPES, i);
	return m_piRiverSideYieldChange ? m_piRiverSideYieldChange[i] : 0; // advc.003t
}

int CvImprovementInfo::getHillsYieldChange(int i) const
{
	FAssertBounds(0, NUM_YIELD_TYPES, i);
	return m_piHillsYieldChange ? m_piHillsYieldChange[i] : 0; // advc.003t
}

int CvImprovementInfo::getIrrigatedYieldChange(int i) const
{
	FAssertBounds(0, NUM_YIELD_TYPES, i);
	return m_piIrrigatedChange ? m_piIrrigatedChange[i] : 0; // advc.003t
}

bool CvImprovementInfo::getTerrainMakesValid(int i) const
{
	FAssertBounds(0, GC.getNumTerrainInfos(), i);
	return m_pbTerrainMakesValid ? m_pbTerrainMakesValid[i] : false;
}

bool CvImprovementInfo::getFeatureMakesValid(int i) const
{
	FAssertBounds(0, GC.getNumFeatureInfos(), i);
	return m_pbFeatureMakesValid ? m_pbFeatureMakesValid[i] : false;
}

int CvImprovementInfo::getTechYieldChanges(int i, int j) const
{
	FAssertBounds(0, GC.getNumTechInfos(), i);
	FAssertBounds(0, NUM_YIELD_TYPES, j);
	return m_ppiTechYieldChanges[i][j];
}

int const* CvImprovementInfo::getTechYieldChangesArray(int i) const
{
	FAssertBounds(0, GC.getNumTechInfos(), i); // advc
	return m_ppiTechYieldChanges[i];
}

int CvImprovementInfo::getRouteYieldChanges(int i, int j) const
{
	FAssertBounds(0, GC.getNumRouteInfos(), i);
	FAssertBounds(0, NUM_YIELD_TYPES, j);
	return m_ppiRouteYieldChanges[i][j];
}

int const* CvImprovementInfo::getRouteYieldChangesArray(int i) const
{
	FAssertBounds(0, GC.getNumRouteInfos(), i); // advc
	return m_ppiRouteYieldChanges[i];
}

int CvImprovementInfo::getImprovementBonusYield(int iBonus, int iYield) const
{
	FAssertBounds(0, GC.getNumBonusInfos(), iBonus);
	FAssertBounds(0, NUM_YIELD_TYPES, iYield);
	return m_paImprovementBonus[iBonus].m_piYieldChange ? m_paImprovementBonus[iBonus].getYieldChange(iYield) : 0; // advc.003t
}

bool CvImprovementInfo::isImprovementBonusMakesValid(int i) const
{
	FAssertBounds(0, GC.getNumBonusInfos(), i);
	return m_paImprovementBonus[i].m_bBonusMakesValid;
}

bool CvImprovementInfo::isImprovementBonusTrade(int i) const
{
	FAssertBounds(0, GC.getNumBonusInfos(), i);
	return m_paImprovementBonus[i].m_bBonusTrade;
}

int CvImprovementInfo::getImprovementBonusDiscoverRand(int i) const
{
	FAssertBounds(0, GC.getNumBonusInfos(), i);
	return m_paImprovementBonus[i].m_iDiscoverRand;
}

/*ImprovementTypes finalImprovementUpgrade(ImprovementTypes eImprovement, int iCount) {
	if (iCount > GC.getNumImprovementInfos())
		return NO_IMPROVEMENT;
	if (getImprovementUpgrade() != NO_IMPROVEMENT)
		return finalImprovementUpgrade(((ImprovementTypes)getImprovementUpgrade()), iCount + 1);
	else return eImprovement;
}*/ // BtS
// K-Mod (I've removed iCount here, and in the python defs. It's a meaningless parameter.)
ImprovementTypes CvImprovementInfo::finalUpgrade(ImprovementTypes eImprov)
{
	if (eImprov == NO_IMPROVEMENT)
		return NO_IMPROVEMENT;
	int iLoopDetector = GC.getNumImprovementInfos();
	while (GC.getInfo(eImprov).getImprovementUpgrade() != NO_IMPROVEMENT && --iLoopDetector > 0)
		eImprov = GC.getInfo(eImprov).getImprovementUpgrade();
	return (iLoopDetector == 0 ? NO_IMPROVEMENT : eImprov);
} // K-Mod end

const TCHAR* CvImprovementInfo::getButton() const
{
	const CvArtInfoImprovement* pImprovementArtInfo = getArtInfo();
	if (pImprovementArtInfo != NULL)
		return pImprovementArtInfo->getButton();

	return NULL;
}

const CvArtInfoImprovement* CvImprovementInfo::getArtInfo() const
{
	return ARTFILEMGR.getImprovementArtInfo(getArtDefineTag());
}

const TCHAR* CvArtInfoImprovement::getShaderNIF() const
{
	return m_szShaderNIF;
}
void CvArtInfoImprovement::setShaderNIF(const TCHAR* szDesc)
{
	m_szShaderNIF = szDesc;
}
#if ENABLE_XML_FILE_CACHE
void CvImprovementInfo::read(FDataStreamBase* stream)
{
	base_t::read(stream); // advc.tag
	uint uiFlag=0;
	stream->Read(&uiFlag);

	stream->Read(&m_iAdvancedStartCost);
	stream->Read(&m_iAdvancedStartCostIncrease);
	stream->Read(&m_iTilesPerGoody);
	stream->Read(&m_iGoodyUniqueRange);
	stream->Read(&m_iFeatureGrowthProbability);
	stream->Read(&m_iUpgradeTime);
	stream->Read(&m_iAirBombDefense);
	stream->Read(&m_iDefenseModifier);
	stream->Read(&m_iHappiness);
	stream->Read(&m_iPillageGold);
	stream->Read((int*)&m_eImprovementPillage);
	stream->Read((int*)&m_eImprovementUpgrade);
	stream->Read(&m_bActsAsCity);
	stream->Read(&m_bHillsMakesValid);
	stream->Read(&m_bFreshWaterMakesValid);
	stream->Read(&m_bRiverSideMakesValid);
	stream->Read(&m_bNoFreshWater);
	stream->Read(&m_bRequiresFlatlands);
	stream->Read(&m_bRequiresRiverSide);
	stream->Read(&m_bRequiresIrrigation);
	stream->Read(&m_bCarriesIrrigation);
	stream->Read(&m_bRequiresFeature);
	stream->Read(&m_bWater);
	stream->Read(&m_bGoody);
	stream->Read(&m_bPermanent);
	stream->Read(&m_bOutsideBorders);
	stream->ReadString(m_szArtDefineTag);
	stream->Read(&m_iWorldSoundscapeScriptId);
	SAFE_DELETE_ARRAY(m_piPrereqNatureYield);
	m_piPrereqNatureYield = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_piPrereqNatureYield);
	SAFE_DELETE_ARRAY(m_piYieldChange);
	m_piYieldChange = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_piYieldChange);
	SAFE_DELETE_ARRAY(m_piRiverSideYieldChange);
	m_piRiverSideYieldChange = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_piRiverSideYieldChange);
	SAFE_DELETE_ARRAY(m_piHillsYieldChange);
	m_piHillsYieldChange = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_piHillsYieldChange);
	SAFE_DELETE_ARRAY(m_piIrrigatedChange);
	m_piIrrigatedChange = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_piIrrigatedChange);
	SAFE_DELETE_ARRAY(m_pbTerrainMakesValid);
	m_pbTerrainMakesValid = new bool[GC.getNumTerrainInfos()];
	stream->Read(GC.getNumTerrainInfos(), m_pbTerrainMakesValid);
	SAFE_DELETE_ARRAY(m_pbFeatureMakesValid);
	m_pbFeatureMakesValid = new bool[GC.getNumFeatureInfos()];
	stream->Read(GC.getNumFeatureInfos(), m_pbFeatureMakesValid);
	SAFE_DELETE_ARRAY(m_paImprovementBonus);
	m_paImprovementBonus = new CvImprovementBonusInfo[GC.getNumBonusInfos()];
	for (int i = 0; i < GC.getNumBonusInfos(); i++)
		m_paImprovementBonus[i].read(stream);
	if (m_ppiTechYieldChanges != NULL)
	{
		for(int i = 0; i < GC.getNumTechInfos(); i++)
			SAFE_DELETE_ARRAY(m_ppiTechYieldChanges[i]);
		SAFE_DELETE_ARRAY(m_ppiTechYieldChanges);
	}
	m_ppiTechYieldChanges = new int*[GC.getNumTechInfos()];
	for(int i = 0; i < GC.getNumTechInfos(); i++)
	{
		m_ppiTechYieldChanges[i]  = new int[NUM_YIELD_TYPES];
		stream->Read(NUM_YIELD_TYPES, m_ppiTechYieldChanges[i]);
	}
	if (m_ppiRouteYieldChanges != NULL)
	{
		for(int i = 0; i < GC.getNumRouteInfos(); i++)
		{
			SAFE_DELETE_ARRAY(m_ppiRouteYieldChanges[i]);
		}
		SAFE_DELETE_ARRAY(m_ppiRouteYieldChanges);
	}
	m_ppiRouteYieldChanges = new int*[GC.getNumRouteInfos()];
	for(int i = 0; i < GC.getNumRouteInfos(); i++)
	{
		m_ppiRouteYieldChanges[i]  = new int[NUM_YIELD_TYPES];
		stream->Read(NUM_YIELD_TYPES, m_ppiRouteYieldChanges[i]);
	}
}

void CvImprovementInfo::write(FDataStreamBase* stream)
{
	base_t::write(stream); // advc.tag
	uint uiFlag = 0;
	stream->Write(uiFlag);

	stream->Write(m_iAdvancedStartCost);
	stream->Write(m_iAdvancedStartCostIncrease);
	stream->Write(m_iTilesPerGoody);
	stream->Write(m_iGoodyUniqueRange);
	stream->Write(m_iFeatureGrowthProbability);
	stream->Write(m_iUpgradeTime);
	stream->Write(m_iAirBombDefense);
	stream->Write(m_iDefenseModifier);
	stream->Write(m_iHappiness);
	stream->Write(m_iPillageGold);
	stream->Write(m_eImprovementPillage);
	stream->Write(m_eImprovementUpgrade);
	stream->Write(m_bActsAsCity);
	stream->Write(m_bHillsMakesValid);
	stream->Write(m_bFreshWaterMakesValid);
	stream->Write(m_bRiverSideMakesValid);
	stream->Write(m_bNoFreshWater);
	stream->Write(m_bRequiresFlatlands);
	stream->Write(m_bRequiresRiverSide);
	stream->Write(m_bRequiresIrrigation);
	stream->Write(m_bCarriesIrrigation);
	stream->Write(m_bRequiresFeature);
	stream->Write(m_bWater);
	stream->Write(m_bGoody);
	stream->Write(m_bPermanent);
	stream->Write(m_bOutsideBorders);
	stream->WriteString(m_szArtDefineTag);
	stream->Write(m_iWorldSoundscapeScriptId);
	stream->Write(NUM_YIELD_TYPES, m_piPrereqNatureYield);
	stream->Write(NUM_YIELD_TYPES, m_piYieldChange);
	stream->Write(NUM_YIELD_TYPES, m_piRiverSideYieldChange);
	stream->Write(NUM_YIELD_TYPES, m_piHillsYieldChange);
	stream->Write(NUM_YIELD_TYPES, m_piIrrigatedChange);
	stream->Write(GC.getNumTerrainInfos(), m_pbTerrainMakesValid);
	stream->Write(GC.getNumFeatureInfos(), m_pbFeatureMakesValid);
	for (int i = 0; i < GC.getNumBonusInfos(); i++)
		m_paImprovementBonus[i].write(stream);
	for(int i = 0; i < GC.getNumTechInfos(); i++)
		stream->Write(NUM_YIELD_TYPES, m_ppiTechYieldChanges[i]);
	for(int i = 0; i < GC.getNumRouteInfos(); i++)
		stream->Write(NUM_YIELD_TYPES, m_ppiRouteYieldChanges[i]);
}
#endif

bool CvImprovementInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML)) // advc.tag
		return false;

	pXML->GetChildXmlValByName(m_szArtDefineTag, "ArtDefineTag");

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),
		"PrereqNatureYields"))
	{
		pXML->SetYieldArray(&m_piPrereqNatureYield);
	}
	else pXML->InitList(&m_piPrereqNatureYield, NUM_YIELD_TYPES);

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),
		"YieldChanges"))
	{
		pXML->SetYieldArray(&m_piYieldChange);
	}
	else pXML->InitList(&m_piYieldChange, NUM_YIELD_TYPES);

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),
		"RiverSideYieldChange"))
	{
		pXML->SetYieldArray(&m_piRiverSideYieldChange);
	}
	else pXML->InitList(&m_piRiverSideYieldChange, NUM_YIELD_TYPES);

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),
		"HillsYieldChange"))
	{
		pXML->SetYieldArray(&m_piHillsYieldChange);
	}
	else pXML->InitList(&m_piHillsYieldChange, NUM_YIELD_TYPES);

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),
		"IrrigatedYieldChange"))
	{
		pXML->SetYieldArray(&m_piIrrigatedChange);
	}
	else pXML->InitList(&m_piIrrigatedChange, NUM_YIELD_TYPES);

	pXML->GetChildXmlValByName(&m_iAdvancedStartCost, "iAdvancedStartCost");
	pXML->GetChildXmlValByName(&m_iAdvancedStartCostIncrease, "iAdvancedStartCostIncrease");
	pXML->GetChildXmlValByName(&m_bActsAsCity, "bActsAsCity");
	pXML->GetChildXmlValByName(&m_bHillsMakesValid, "bHillsMakesValid");
	pXML->GetChildXmlValByName(&m_bFreshWaterMakesValid, "bFreshWaterMakesValid");
	pXML->GetChildXmlValByName(&m_bRiverSideMakesValid, "bRiverSideMakesValid");
	pXML->GetChildXmlValByName(&m_bNoFreshWater, "bNoFreshWater");
	pXML->GetChildXmlValByName(&m_bRequiresFlatlands, "bRequiresFlatlands");
	pXML->GetChildXmlValByName(&m_bRequiresRiverSide, "bRequiresRiverSide");
	pXML->GetChildXmlValByName(&m_bRequiresIrrigation, "bRequiresIrrigation");
	pXML->GetChildXmlValByName(&m_bCarriesIrrigation, "bCarriesIrrigation");
	pXML->GetChildXmlValByName(&m_bRequiresFeature, "bRequiresFeature");
	pXML->GetChildXmlValByName(&m_bWater, "bWater");
	pXML->GetChildXmlValByName(&m_bGoody, "bGoody");
	pXML->GetChildXmlValByName(&m_bPermanent, "bPermanent");
	pXML->GetChildXmlValByName(&m_iTilesPerGoody, "iTilesPerGoody");
	pXML->GetChildXmlValByName(&m_iGoodyUniqueRange, "iGoodyRange");
	pXML->GetChildXmlValByName(&m_iFeatureGrowthProbability, "iFeatureGrowth");
	pXML->GetChildXmlValByName(&m_iUpgradeTime, "iUpgradeTime");
	pXML->GetChildXmlValByName(&m_iAirBombDefense, "iAirBombDefense");
	pXML->GetChildXmlValByName(&m_iDefenseModifier, "iDefenseModifier");
	pXML->GetChildXmlValByName(&m_iHappiness, "iHappiness");
	pXML->GetChildXmlValByName(&m_iPillageGold, "iPillageGold");
	pXML->GetChildXmlValByName(&m_bOutsideBorders, "bOutsideBorders");

	pXML->SetVariableListTagPair(&m_pbTerrainMakesValid, "TerrainMakesValids", GC.getNumTerrainInfos());
	pXML->SetVariableListTagPair(&m_pbFeatureMakesValid, "FeatureMakesValids", GC.getNumFeatureInfos());

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"BonusTypeStructs"))
	{
		pXML->SetImprovementBonuses(&m_paImprovementBonus);
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	else pXML->InitImprovementBonusList(&m_paImprovementBonus, GC.getNumBonusInfos());

	for (int i = 0; i < 2; i++) // advc: Reduce code duplication
	{
		bool bTech = (i == 0);
		int iNumInfos = (bTech ? GC.getNumTechInfos() : GC.getNumRouteInfos());
		FAssert(iNumInfos > 0);
		int*** pppiYieldChanges = &(bTech ? m_ppiTechYieldChanges : m_ppiRouteYieldChanges);
		pXML->Init2DIntList(pppiYieldChanges, iNumInfos, NUM_YIELD_TYPES);
		if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), bTech ?
			"TechYieldChanges" : "RouteYieldChanges"))
		{
			if (pXML->SkipToNextVal())
			{
				int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
				if (gDLL->getXMLIFace()->SetToChild(pXML->GetXML()))
				{
					if (iNumSibs > 0)
					{
						CvString szTextVal;
						for (int j = 0; j < iNumSibs; j++)
						{
							pXML->GetChildXmlValByName(szTextVal, bTech ?
									"PrereqTech" : "RouteType");
							int iIndex = pXML->FindInInfoClass(szTextVal);
							if (iIndex > -1)
							{
								SAFE_DELETE_ARRAY((*pppiYieldChanges)[iIndex]);
								if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), bTech ?
									"TechYields": "RouteYields"))
								{
									pXML->SetYieldArray(&(*pppiYieldChanges)[iIndex]);
								}
								else pXML->InitList(&(*pppiYieldChanges)[iIndex], NUM_YIELD_TYPES);
							}
							if (!gDLL->getXMLIFace()->NextSibling(pXML->GetXML()))
								break;
						}
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
			gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
		}
	}
	CvString szTextVal;
	pXML->GetChildXmlValByName(szTextVal, "WorldSoundscapeAudioScript", /* advc.006b: */ "");
	if (szTextVal.GetLength() > 0)
		m_iWorldSoundscapeScriptId = gDLL->getAudioTagIndex(szTextVal.GetCString(), AUDIOTAG_SOUNDSCAPE);
	else m_iWorldSoundscapeScriptId = -1;

	return true;
}

bool CvImprovementInfo::readPass2(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;

	pXML->GetChildXmlValByName(szTextVal, "ImprovementPillage");
	m_eImprovementPillage = (ImprovementTypes)GC.getInfoTypeForString(szTextVal);

	pXML->GetChildXmlValByName(szTextVal, "ImprovementUpgrade");
	m_eImprovementUpgrade = (ImprovementTypes)GC.getInfoTypeForString(szTextVal);

	return true;
}

CvImprovementBonusInfo::CvImprovementBonusInfo() :
m_iDiscoverRand(0),
m_bBonusMakesValid(false),
m_bBonusTrade(false),
m_piYieldChange(NULL)
{}

CvImprovementBonusInfo::~CvImprovementBonusInfo()
{
	SAFE_DELETE_ARRAY(m_piYieldChange);
}

int CvImprovementBonusInfo::getDiscoverRand() const
{
	return m_iDiscoverRand;
}

bool CvImprovementBonusInfo::isBonusMakesValid() const
{
	return m_bBonusMakesValid;
}

bool CvImprovementBonusInfo::isBonusTrade() const
{
	return m_bBonusTrade;
}

int CvImprovementBonusInfo::getYieldChange(int i) const
{
	FAssertBounds(0, NUM_YIELD_TYPES, i);
	return m_piYieldChange ? m_piYieldChange[i] : 0; // advc.003t
}
#if ENABLE_XML_FILE_CACHE
void CvImprovementBonusInfo::read(FDataStreamBase* stream)
{
	base_t::read(stream);
	uint uiFlag=0;
	stream->Read(&uiFlag);
	stream->Read(&m_iDiscoverRand);
	stream->Read(&m_bBonusMakesValid);
	stream->Read(&m_bBonusTrade);
	SAFE_DELETE_ARRAY(m_piYieldChange);
	m_piYieldChange = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_piYieldChange);
}

void CvImprovementBonusInfo::write(FDataStreamBase* stream)
{
	base_t::write(stream);
	uint uiFlag=0;
	stream->Write(uiFlag);
	stream->Write(m_iDiscoverRand);
	stream->Write(m_bBonusMakesValid);
	stream->Write(m_bBonusTrade);
	stream->Write(NUM_YIELD_TYPES, m_piYieldChange);
}
#endif

CvGoodyInfo::CvGoodyInfo() :
m_iGold(0),
m_iGoldRand1(0),
m_iGoldRand2(0),
m_iMapOffset(0),
m_iMapRange(0),
m_iMapProb(0),
m_iExperience(0),
m_iHealing(0),
m_iDamagePrereq(0),
m_iBarbarianUnitProb(0),
m_iMinBarbarians(0),
m_iUnitClassType(NO_UNITCLASS),
m_iBarbarianUnitClass(NO_UNITCLASS),
m_bTech(false),
m_bBad(false)
{}

int CvGoodyInfo::getGold() const
{
	return m_iGold;
}

int CvGoodyInfo::getGoldRand1() const
{
	return m_iGoldRand1;
}

int CvGoodyInfo::getGoldRand2() const
{
	return m_iGoldRand2;
}

int CvGoodyInfo::getMapOffset() const
{
	return m_iMapOffset;
}

int CvGoodyInfo::getMapRange() const
{
	return m_iMapRange;
}

int CvGoodyInfo::getMapProb() const
{
	return m_iMapProb;
}

int CvGoodyInfo::getExperience() const
{
	return m_iExperience;
}

int CvGoodyInfo::getHealing() const
{
	return m_iHealing;
}

int CvGoodyInfo::getDamagePrereq() const
{
	return m_iDamagePrereq;
}

int CvGoodyInfo::getBarbarianUnitProb() const
{
	return m_iBarbarianUnitProb;
}

int CvGoodyInfo::getMinBarbarians() const
{
	return m_iMinBarbarians;
}

int CvGoodyInfo::getUnitClassType() const
{
	return m_iUnitClassType;
}

int CvGoodyInfo::getBarbarianUnitClass() const
{
	return m_iBarbarianUnitClass;
}

bool CvGoodyInfo::isTech() const
{
	return m_bTech;
}

bool CvGoodyInfo::isBad() const
{
	return m_bBad;
}

const TCHAR* CvGoodyInfo::getSound() const
{
	return m_szSound;
}

bool CvGoodyInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML))
		return false;

	pXML->GetChildXmlValByName(m_szSound, "Sound");

	pXML->GetChildXmlValByName(&m_iGold, "iGold");
	pXML->GetChildXmlValByName(&m_iGoldRand1, "iGoldRand1");
	pXML->GetChildXmlValByName(&m_iGoldRand2, "iGoldRand2");
	pXML->GetChildXmlValByName(&m_iMapOffset, "iMapOffset");
	pXML->GetChildXmlValByName(&m_iMapRange, "iMapRange");
	pXML->GetChildXmlValByName(&m_iMapProb, "iMapProb");
	pXML->GetChildXmlValByName(&m_iExperience, "iExperience");
	pXML->GetChildXmlValByName(&m_iHealing, "iHealing");
	pXML->GetChildXmlValByName(&m_iDamagePrereq, "iDamagePrereq");
	pXML->GetChildXmlValByName(&m_bTech, "bTech");
	pXML->GetChildXmlValByName(&m_bBad, "bBad");

	pXML->SetInfoIDFromChildXmlVal(m_iUnitClassType, "UnitClass");
	pXML->SetInfoIDFromChildXmlVal(m_iBarbarianUnitClass, "BarbarianClass");

	pXML->GetChildXmlValByName(&m_iBarbarianUnitProb, "iBarbarianUnitProb");
	pXML->GetChildXmlValByName(&m_iMinBarbarians, "iMinBarbarians");

	return true;
}
