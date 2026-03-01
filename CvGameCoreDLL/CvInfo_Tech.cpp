// advc.003x: Cut from CvInfos.cpp

#include "CvGameCoreDLL.h"
#include "CvInfo_Tech.h"
#include "CvXMLLoadUtility.h"


CvTechInfo::CvTechInfo() :
m_iAdvisorType(NO_ADVISOR),
m_iAIWeight(0),
m_iAITradeModifier(0),
m_iResearchCost(0),
m_iAdvancedStartCost(0),
m_iAdvancedStartCostIncrease(0),
m_iEra(NO_ERA),
m_iTradeRoutes(0),
m_iFeatureProductionModifier(0),
m_iWorkerSpeedModifier(0),
m_iFirstFreeUnitClass(NO_UNITCLASS),
m_iHealth(0),
m_iHappiness(0),
m_iFirstFreeTechs(0),
m_iAssetValue(0),
m_iPowerValue(0),
m_iGridX(0),
m_iGridY(0),
m_bRepeat(false),
m_bTrade(false),
m_bDisable(false),
m_bGoodyTech(false),
m_bExtraWaterSeeFrom(false),
m_bMapCentering(false),
m_bMapVisible(false),
m_bMapTrading(false),
m_bTechTrading(false),
m_bGoldTrading(false),
m_bOpenBordersTrading(false),
m_bDefensivePactTrading(false),
m_bPermanentAllianceTrading(false),
m_bVassalStateTrading(false),
m_bBridgeBuilding(false),
m_bIrrigation(false),
m_bIgnoreIrrigation(false),
m_bWaterWork(false),
m_bRiverTrade(false),
m_piDomainExtraMoves(NULL),
m_piFlavorValue(NULL),
m_piCommerceModifier(NULL), // K-Mod
m_piSpecialistExtraCommerce(NULL), // K-Mod
m_pbCommerceFlexible(NULL),
m_pbTerrainTrade(NULL)
{}

CvTechInfo::~CvTechInfo()
{
	SAFE_DELETE_ARRAY(m_piDomainExtraMoves);
	SAFE_DELETE_ARRAY(m_piFlavorValue);
	SAFE_DELETE_ARRAY(m_piCommerceModifier); // K-Mod
	SAFE_DELETE_ARRAY(m_piSpecialistExtraCommerce); // K-Mod
	SAFE_DELETE_ARRAY(m_pbCommerceFlexible);
	SAFE_DELETE_ARRAY(m_pbTerrainTrade);
}

std::wstring CvTechInfo::getQuote()	const
{
	return gDLL->getText(m_szQuoteKey);
}

const TCHAR* CvTechInfo::getSound() const
{
	return m_szSound;
}

const TCHAR* CvTechInfo::getSoundMP() const
{
	return m_szSoundMP;
}

int CvTechInfo::getDomainExtraMoves(int i) const
{
	FAssertBounds(0, NUM_DOMAIN_TYPES, i); // advc: check bounds
	return m_piDomainExtraMoves ? m_piDomainExtraMoves[i] : 0; // advc.003t
}

int CvTechInfo::getFlavorValue(int i) const
{
	FAssertBounds(0, GC.getNumFlavorTypes(), i);
	return m_piFlavorValue ? m_piFlavorValue[i] : 0; // advc.003t
}
// <advc.003t> Calls from Python aren't going to respect the bounds
int CvTechInfo::py_getPrereqOrTechs(int i) const
{
	if (i < 0 || i >= getNumOrTechPrereqs())
		return NO_TECH;
	return m_aePrereqOrTechs[i];
}

int CvTechInfo::py_getPrereqAndTechs(int i) const
{
	if (i < 0 || i >= getNumAndTechPrereqs())
		return NO_TECH;
	return m_aePrereqAndTechs[i];
} // </advc.003t>

// K-Mod
int CvTechInfo::getCommerceModifier(int i) const
{
	FAssertBounds(0, NUM_COMMERCE_TYPES, i);
	return m_piCommerceModifier ? m_piCommerceModifier[i] : 0;
}

int* CvTechInfo::getCommerceModifierArray() const
{
	return m_piCommerceModifier;
}

int CvTechInfo::getSpecialistExtraCommerce(int i) const
{
	FAssertBounds(0, GC.getNumFlavorTypes(), i);
	return m_piSpecialistExtraCommerce ? m_piSpecialistExtraCommerce[i] : 0;
}

int* CvTechInfo::getSpecialistExtraCommerceArray() const
{
	return m_piSpecialistExtraCommerce;
} // K-Mod end

bool CvTechInfo::isCommerceFlexible(int i) const
{
	FAssertBounds(0, NUM_COMMERCE_TYPES, i);
	return m_pbCommerceFlexible ? m_pbCommerceFlexible[i] : false;
}

bool CvTechInfo::isTerrainTrade(int i) const
{
	FAssertBounds(0, GC.getNumTerrainInfos(), i); // advc: check bounds
	return m_pbTerrainTrade ? m_pbTerrainTrade[i] : false;
}
#if ENABLE_XML_FILE_CACHE
void CvTechInfo::read(FDataStreamBase* stream)
{
	base_t::read(stream);
	uint uiFlag=0;
	stream->Read(&uiFlag);

	stream->Read(&m_iAdvisorType);
	stream->Read(&m_iAIWeight);
	stream->Read(&m_iAITradeModifier);
	stream->Read(&m_iResearchCost);
	stream->Read(&m_iAdvancedStartCost);
	stream->Read(&m_iAdvancedStartCostIncrease);
	stream->Read(&m_iEra);
	stream->Read(&m_iFirstFreeUnitClass);
	stream->Read(&m_iFeatureProductionModifier);
	stream->Read(&m_iWorkerSpeedModifier);
	stream->Read(&m_iTradeRoutes);
	stream->Read(&m_iHealth);
	stream->Read(&m_iHappiness);
	stream->Read(&m_iFirstFreeTechs);
	stream->Read(&m_iAssetValue);
	stream->Read(&m_iPowerValue);
	stream->Read(&m_bRepeat);
	stream->Read(&m_bTrade);
	stream->Read(&m_bDisable);
	stream->Read(&m_bGoodyTech);
	stream->Read(&m_bExtraWaterSeeFrom);
	stream->Read(&m_bMapCentering);
	stream->Read(&m_bMapVisible);
	stream->Read(&m_bMapTrading);
	stream->Read(&m_bTechTrading);
	stream->Read(&m_bGoldTrading);
	stream->Read(&m_bOpenBordersTrading);
	stream->Read(&m_bDefensivePactTrading);
	stream->Read(&m_bPermanentAllianceTrading);
	stream->Read(&m_bVassalStateTrading);
	stream->Read(&m_bBridgeBuilding);
	stream->Read(&m_bIrrigation);
	stream->Read(&m_bIgnoreIrrigation);
	stream->Read(&m_bWaterWork);
	stream->Read(&m_bRiverTrade);
	stream->Read(&m_iGridX);
	stream->Read(&m_iGridY);
	SAFE_DELETE_ARRAY(m_piDomainExtraMoves);
	m_piDomainExtraMoves = new int[NUM_DOMAIN_TYPES];
	stream->Read(NUM_DOMAIN_TYPES, m_piDomainExtraMoves);
	SAFE_DELETE_ARRAY(m_piFlavorValue);
	m_piFlavorValue = new int[GC.getNumFlavorTypes()];
	stream->Read(GC.getNumFlavorTypes(), m_piFlavorValue);
	// <advc.003t>
	int iOrTechPrereqs;
	stream->Read(&iOrTechPrereqs);
	if (iOrTechPrereqs > 0)
	{
		m_aePrereqOrTechs.resize(iOrTechPrereqs);
		stream->Read(iOrTechPrereqs, (int*)&m_aePrereqOrTechs[0]);
	}
	int iAndTechPrereqs;
	stream->Read(&iAndTechPrereqs);
	if (iAndTechPrereqs > 0)
	{
		m_aePrereqAndTechs.resize(iAndTechPrereqs);
		stream->Read(iAndTechPrereqs, (int*)&m_aePrereqAndTechs[0]);
	} // </advc.003t>
	// K-Mod
	SAFE_DELETE_ARRAY(m_piCommerceModifier)
	m_piCommerceModifier = new int[NUM_COMMERCE_TYPES];
	stream->Read(NUM_COMMERCE_TYPES, m_piCommerceModifier);
	SAFE_DELETE_ARRAY(m_piSpecialistExtraCommerce)
	m_piSpecialistExtraCommerce = new int[NUM_COMMERCE_TYPES];
	stream->Read(NUM_COMMERCE_TYPES, m_piSpecialistExtraCommerce);
	// K-Mod end
	SAFE_DELETE_ARRAY(m_pbCommerceFlexible);
	m_pbCommerceFlexible = new bool[NUM_COMMERCE_TYPES];
	stream->Read(NUM_COMMERCE_TYPES, m_pbCommerceFlexible);
	SAFE_DELETE_ARRAY(m_pbTerrainTrade);
	m_pbTerrainTrade = new bool[GC.getNumTerrainInfos()];
	stream->Read(GC.getNumTerrainInfos(), m_pbTerrainTrade);
	stream->ReadString(m_szQuoteKey);
	stream->ReadString(m_szSound);
	stream->ReadString(m_szSoundMP);
}

void CvTechInfo::write(FDataStreamBase* stream)
{
	base_t::write(stream);
	uint uiFlag = 0;
	stream->Write(uiFlag);

	stream->Write(m_iAdvisorType);
	stream->Write(m_iAIWeight);
	stream->Write(m_iAITradeModifier);
	stream->Write(m_iResearchCost);
	stream->Write(m_iAdvancedStartCost);
	stream->Write(m_iAdvancedStartCostIncrease);
	stream->Write(m_iEra);
	stream->Write(m_iFirstFreeUnitClass);
	stream->Write(m_iFeatureProductionModifier);
	stream->Write(m_iWorkerSpeedModifier);
	stream->Write(m_iTradeRoutes);
	stream->Write(m_iHealth);
	stream->Write(m_iHappiness);
	stream->Write(m_iFirstFreeTechs);
	stream->Write(m_iAssetValue);
	stream->Write(m_iPowerValue);
	stream->Write(m_bRepeat);
	stream->Write(m_bTrade);
	stream->Write(m_bDisable);
	stream->Write(m_bGoodyTech);
	stream->Write(m_bExtraWaterSeeFrom);
	stream->Write(m_bMapCentering);
	stream->Write(m_bMapVisible);
	stream->Write(m_bMapTrading);
	stream->Write(m_bTechTrading);
	stream->Write(m_bGoldTrading);
	stream->Write(m_bOpenBordersTrading);
	stream->Write(m_bDefensivePactTrading);
	stream->Write(m_bPermanentAllianceTrading);
	stream->Write(m_bVassalStateTrading);
	stream->Write(m_bBridgeBuilding);
	stream->Write(m_bIrrigation);
	stream->Write(m_bIgnoreIrrigation);
	stream->Write(m_bWaterWork);
	stream->Write(m_bRiverTrade);
	stream->Write(m_iGridX);
	stream->Write(m_iGridY);
	stream->Write(NUM_DOMAIN_TYPES, m_piDomainExtraMoves);
	stream->Write(GC.getNumFlavorTypes(), m_piFlavorValue);
	// <advc.003t>
	{
		int iOrTechPrereqs = getNumOrTechPrereqs();
		stream->Write(iOrTechPrereqs);
		if (iOrTechPrereqs > 0)
			stream->Write(iOrTechPrereqs, (int*)&m_aePrereqOrTechs[0]);
	}
	{
		int iAndTechPrereqs = getNumAndTechPrereqs();
		stream->Write(iAndTechPrereqs);
		if (iAndTechPrereqs > 0)
			stream->Write(iAndTechPrereqs, (int*)&m_aePrereqAndTechs[0]);
	} // </advc.003t>
	stream->Write(NUM_COMMERCE_TYPES, m_piCommerceModifier); // K-Mod
	stream->Write(NUM_COMMERCE_TYPES, m_piSpecialistExtraCommerce); // K-Mod
	stream->Write(NUM_COMMERCE_TYPES, m_pbCommerceFlexible);
	stream->Write(GC.getNumTerrainInfos(), m_pbTerrainTrade);
	stream->WriteString(m_szQuoteKey);
	stream->WriteString(m_szSound);
	stream->WriteString(m_szSoundMP);
}
#endif
bool CvTechInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML))
		return false;

	pXML->SetInfoIDFromChildXmlVal(m_iAdvisorType, "Advisor");

	pXML->GetChildXmlValByName(&m_iAIWeight, "iAIWeight");
	pXML->GetChildXmlValByName(&m_iAITradeModifier, "iAITradeModifier");
	pXML->GetChildXmlValByName(&m_iResearchCost, "iCost");
	pXML->GetChildXmlValByName(&m_iAdvancedStartCost, "iAdvancedStartCost");
	pXML->GetChildXmlValByName(&m_iAdvancedStartCostIncrease, "iAdvancedStartCostIncrease");

	pXML->SetInfoIDFromChildXmlVal(m_iEra, "Era");
	pXML->SetInfoIDFromChildXmlVal(m_iFirstFreeUnitClass, "FirstFreeUnitClass");

	pXML->GetChildXmlValByName(&m_iFeatureProductionModifier, "iFeatureProductionModifier");
	pXML->GetChildXmlValByName(&m_iWorkerSpeedModifier, "iWorkerSpeedModifier");
	pXML->GetChildXmlValByName(&m_iTradeRoutes, "iTradeRoutes");
	pXML->GetChildXmlValByName(&m_iHealth, "iHealth");
	pXML->GetChildXmlValByName(&m_iHappiness, "iHappiness");
	pXML->GetChildXmlValByName(&m_iFirstFreeTechs, "iFirstFreeTechs");
	pXML->GetChildXmlValByName(&m_iAssetValue, "iAsset");
	pXML->GetChildXmlValByName(&m_iPowerValue, "iPower");
	pXML->GetChildXmlValByName(&m_bRepeat, "bRepeat");
	pXML->GetChildXmlValByName(&m_bTrade, "bTrade");
	pXML->GetChildXmlValByName(&m_bDisable, "bDisable");
	pXML->GetChildXmlValByName(&m_bGoodyTech, "bGoodyTech");
	pXML->GetChildXmlValByName(&m_bExtraWaterSeeFrom, "bExtraWaterSeeFrom");
	pXML->GetChildXmlValByName(&m_bMapCentering, "bMapCentering");
	pXML->GetChildXmlValByName(&m_bMapVisible, "bMapVisible");
	pXML->GetChildXmlValByName(&m_bMapTrading, "bMapTrading");
	pXML->GetChildXmlValByName(&m_bTechTrading, "bTechTrading");
	pXML->GetChildXmlValByName(&m_bGoldTrading, "bGoldTrading");
	pXML->GetChildXmlValByName(&m_bOpenBordersTrading, "bOpenBordersTrading");
	pXML->GetChildXmlValByName(&m_bDefensivePactTrading, "bDefensivePactTrading");
	pXML->GetChildXmlValByName(&m_bPermanentAllianceTrading, "bPermanentAllianceTrading");
	pXML->GetChildXmlValByName(&m_bVassalStateTrading, "bVassalTrading");
	pXML->GetChildXmlValByName(&m_bBridgeBuilding, "bBridgeBuilding");
	pXML->GetChildXmlValByName(&m_bIrrigation, "bIrrigation");
	pXML->GetChildXmlValByName(&m_bIgnoreIrrigation, "bIgnoreIrrigation");
	pXML->GetChildXmlValByName(&m_bWaterWork, "bWaterWork");
	pXML->GetChildXmlValByName(&m_bRiverTrade, "bRiverTrade");
	pXML->GetChildXmlValByName(&m_iGridX, "iGridX");
	pXML->GetChildXmlValByName(&m_iGridY, "iGridY");

	// K-Mod
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),
		"CommerceModifiers"))
	{
		pXML->SetCommerce(&m_piCommerceModifier);
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	else pXML->InitList(&m_piCommerceModifier, NUM_COMMERCE_TYPES);
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),
		"SpecialistExtraCommerces"))
	{
		pXML->SetCommerceArray(&m_piSpecialistExtraCommerce);
	}
	else pXML->InitList(&m_piSpecialistExtraCommerce, NUM_COMMERCE_TYPES);
	// K-Mod end

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),
		"CommerceFlexible"))
	{
		pXML->SetCommerceArray(&m_pbCommerceFlexible);
	}
	else pXML->InitList(&m_pbCommerceFlexible, NUM_COMMERCE_TYPES);

	pXML->SetVariableListTagPair(&m_piDomainExtraMoves, "DomainExtraMoves", NUM_DOMAIN_TYPES);
	pXML->SetVariableListTagPair(&m_pbTerrainTrade, "TerrainTrades", GC.getNumTerrainInfos(), false);
	pXML->SetVariableListTagPair(&m_piFlavorValue, "Flavors", GC.getNumFlavorTypes());

	pXML->GetChildXmlValByName(m_szQuoteKey, "Quote");
	pXML->GetChildXmlValByName(m_szSound, "Sound");
	pXML->GetChildXmlValByName(m_szSoundMP, "SoundMP");

	return true;
}

bool CvTechInfo::readPass2(CvXMLLoadUtility* pXML)
{
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "OrPreReqs"))
	{
		if (pXML->SkipToNextVal())
		{
			int const iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			if (iNumSibs > 0)
			{
				CvString szTextVal;
				if (pXML->GetChildXmlVal(szTextVal))
				{	// advc.003t: The DLL can handle any number, but Python maybe not.
					FAssert(iNumSibs <= GC.getDefineINT(CvGlobals::NUM_OR_TECH_PREREQS));
					for (int j = 0; j < iNumSibs; j++)
					{	// <advc.003t>
						TechTypes eTech = (TechTypes)GC.getInfoTypeForString(szTextVal);
						if (eTech != NO_TECH)
							m_aePrereqOrTechs.push_back(eTech); // </advc.003t>
						if (!pXML->GetNextXmlVal(szTextVal))
							break;
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	// (same with OR/or -> AND/and)
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "AndPreReqs"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			if (iNumSibs > 0)
			{
				CvString szTextVal;
				if (pXML->GetChildXmlVal(szTextVal))
				{
					FAssert(iNumSibs <= GC.getDefineINT(CvGlobals::NUM_AND_TECH_PREREQS));
					for (int j = 0; j < iNumSibs; j++)
					{	// <advc.003t>
						TechTypes eTech = (TechTypes)GC.getInfoTypeForString(szTextVal);
						if (eTech != NO_TECH)
							m_aePrereqAndTechs.push_back(eTech); // </advc.003t>
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
