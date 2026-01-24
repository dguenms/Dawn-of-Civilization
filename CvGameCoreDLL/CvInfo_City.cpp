// advc.003x: Cut from CvInfos.cpp

#include "CvGameCoreDLL.h"
#include "CvInfo_City.h"
#include "CvXMLLoadUtility.h"


CvProcessInfo::CvProcessInfo() :
m_eTechPrereq(NO_TECH),
m_aiProductionToCommerceModifier(NULL)
{}

CvProcessInfo::~CvProcessInfo()
{
	SAFE_DELETE_ARRAY(m_aiProductionToCommerceModifier);
}

int CvProcessInfo::getProductionToCommerceModifier(CommerceTypes eCommerce) const
{
	FAssertEnumBounds(eCommerce);
	return (m_aiProductionToCommerceModifier == NULL ? 0 : // advc.003t
			m_aiProductionToCommerceModifier[eCommerce]);
}

bool CvProcessInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML))
		return false;

	pXML->SetInfoIDFromChildXmlVal(m_eTechPrereq, "TechPrereq");

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),
		"ProductionToCommerceModifiers"))
	{
		pXML->SetCommerceArray(&m_aiProductionToCommerceModifier);
	}
	else pXML->InitList(&m_aiProductionToCommerceModifier, NUM_COMMERCE_TYPES);

	return true;
}

CvSpecialistInfo::CvSpecialistInfo() :
m_iGreatPeopleUnitClass(NO_UNITCLASS),
m_iGreatPeopleRateChange(0),
m_iMissionType(NO_MISSION),
m_bVisible(false),
m_piYieldChange(NULL),
m_piCommerceChange(NULL),
m_piFlavorValue(NULL),
m_iExperience(0)
{}

CvSpecialistInfo::~CvSpecialistInfo()
{
	SAFE_DELETE_ARRAY(m_piYieldChange);
	SAFE_DELETE_ARRAY(m_piCommerceChange);
	SAFE_DELETE_ARRAY(m_piFlavorValue);
}

int CvSpecialistInfo::getGreatPeopleUnitClass() const
{
	return m_iGreatPeopleUnitClass;
}

int CvSpecialistInfo::getGreatPeopleRateChange() const
{
	return m_iGreatPeopleRateChange;
}

int CvSpecialistInfo::getMissionType() const
{
	return m_iMissionType;
}

void CvSpecialistInfo::setMissionType(int iNewType)
{
	m_iMissionType = iNewType;
}

bool CvSpecialistInfo::isVisible() const
{
	return m_bVisible;
}

int CvSpecialistInfo::getExperience() const
{
	return m_iExperience;
}

int CvSpecialistInfo::getYieldChange(int i) const
{
	FAssertBounds(0, NUM_YIELD_TYPES, i);
	return m_piYieldChange ? m_piYieldChange[i] : 0; // advc.003t
}

const int* CvSpecialistInfo::getYieldChangeArray() const
{
	return m_piYieldChange;
}

int CvSpecialistInfo::getCommerceChange(int i) const
{
	FAssertBounds(0, NUM_COMMERCE_TYPES, i);
	return m_piCommerceChange ? m_piCommerceChange[i] : 0; // advc.003t
}

int CvSpecialistInfo::getFlavorValue(int i) const
{
	FAssertBounds(0, GC.getNumFlavorTypes(), i);
	return m_piFlavorValue ? m_piFlavorValue[i] : 0; // advc.003t
}

const TCHAR* CvSpecialistInfo::getTexture() const
{
	return m_szTexture;
}

bool CvSpecialistInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML))
		return false;

	pXML->GetChildXmlValByName(m_szTexture, "Texture");
	pXML->GetChildXmlValByName(&m_bVisible, "bVisible");
	{
		CvString szTextVal;
		pXML->GetChildXmlValByName(szTextVal, "GreatPeopleUnitClass");
		m_iGreatPeopleUnitClass = pXML->FindInInfoClass(szTextVal);
	}
	pXML->GetChildXmlValByName(&m_iGreatPeopleRateChange, "iGreatPeopleRateChange");
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "Yields"))
		pXML->SetYieldArray(&m_piYieldChange);
	else pXML->InitList(&m_piYieldChange, NUM_YIELD_TYPES);
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "Commerces"))
		pXML->SetCommerceArray(&m_piCommerceChange);
	else pXML->InitList(&m_piCommerceChange, NUM_COMMERCE_TYPES);
	pXML->GetChildXmlValByName(&m_iExperience, "iExperience");
	pXML->SetVariableListTagPair(&m_piFlavorValue, "Flavors", GC.getNumFlavorTypes());
	return true;
}

CvCultureLevelInfo::CvCultureLevelInfo() :
m_iCityDefenseModifier(0),
m_paiSpeedThreshold(NULL)
{}

CvCultureLevelInfo::~CvCultureLevelInfo()
{
	SAFE_DELETE_ARRAY(m_paiSpeedThreshold);
}

int CvCultureLevelInfo::getCityDefenseModifier() const
{
	return m_iCityDefenseModifier;
}

int CvCultureLevelInfo::getSpeedThreshold(int i) const
{
	FAssertBounds(0, GC.getNumGameSpeedInfos(), i);
	return (m_paiSpeedThreshold != NULL ? m_paiSpeedThreshold[i] : 0); // advc.003t
}

bool CvCultureLevelInfo::read(CvXMLLoadUtility* pXml)
{
	if (!base_t::read(pXml))
		return false;

	pXml->GetChildXmlValByName(&m_iCityDefenseModifier, "iCityDefenseModifier");
	pXml->SetVariableListTagPair(&m_paiSpeedThreshold, "SpeedThresholds", GC.getNumGameSpeedInfos());

	return true;
}

CvEmphasizeInfo::CvEmphasizeInfo() :
m_bAvoidGrowth(false),
m_bGreatPeople(false),
m_piYieldModifiers(NULL),
m_piCommerceModifiers(NULL)
{}

CvEmphasizeInfo::~CvEmphasizeInfo()
{
	SAFE_DELETE_ARRAY(m_piYieldModifiers);
	SAFE_DELETE_ARRAY(m_piCommerceModifiers);
}

bool CvEmphasizeInfo::isAvoidGrowth() const
{
	return m_bAvoidGrowth;
}

bool CvEmphasizeInfo::isGreatPeople() const
{
	return m_bGreatPeople;
}

int CvEmphasizeInfo::getYieldChange(int i) const
{
	FAssertBounds(0, NUM_YIELD_TYPES, i);
	return m_piYieldModifiers ? m_piYieldModifiers[i] : 0; // advc.003t
}

int CvEmphasizeInfo::getCommerceChange(int i) const
{
	FAssertBounds(0, NUM_COMMERCE_TYPES, i);
	return m_piCommerceModifiers ? m_piCommerceModifiers[i] : 0; // advc.003t
}

bool CvEmphasizeInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML))
		return false;

	pXML->GetChildXmlValByName(&m_bAvoidGrowth, "bAvoidGrowth");
	pXML->GetChildXmlValByName(&m_bGreatPeople, "bGreatPeople");

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),
		"YieldModifiers"))
	{
		pXML->SetYieldArray(&m_piYieldModifiers);
	}
	else pXML->InitList(&m_piYieldModifiers, NUM_YIELD_TYPES);

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),
		"CommerceModifiers"))
	{
		pXML->SetCommerceArray(&m_piCommerceModifiers);
	}
	else pXML->InitList(&m_piCommerceModifiers, NUM_COMMERCE_TYPES);

	return true;
}

CvHurryInfo::CvHurryInfo() :
m_iGoldPerProduction(0),
m_iProductionPerPopulation(0),
m_bAnger(false)
{}

int CvHurryInfo::getGoldPerProduction() const
{
	return m_iGoldPerProduction;
}

int CvHurryInfo::getProductionPerPopulation() const
{
	return m_iProductionPerPopulation;
}

bool CvHurryInfo::isAnger() const
{
	return m_bAnger;
}

bool CvHurryInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
		return false;

	pXML->GetChildXmlValByName(&m_iGoldPerProduction, "iGoldPerProduction");
	pXML->GetChildXmlValByName(&m_iProductionPerPopulation, "iProductionPerPopulation");
	pXML->GetChildXmlValByName(&m_bAnger, "bAnger");

	return true;
}
