// advc.003x: Cut from CvInfos.cpp

#include "CvGameCoreDLL.h"
#include "CvInfo_Build.h"
#include "CvXMLLoadUtility.h"


CvBuildInfo::CvBuildInfo() :
m_iTime(0),
m_iCost(0),
m_iTechPrereq(NO_TECH),
m_iImprovement(NO_IMPROVEMENT),
m_iRoute(NO_ROUTE),
m_iEntityEvent(NO_ENTITYEVENT),
m_iMissionType(NO_MISSION),
m_bKill(false),
m_paiFeatureTech(NULL),
m_paiFeatureTime(NULL),
m_paiFeatureProduction(NULL),
m_pabFeatureRemove(NULL)
{}

CvBuildInfo::~CvBuildInfo()
{
	SAFE_DELETE_ARRAY(m_paiFeatureTech);
	SAFE_DELETE_ARRAY(m_paiFeatureTime);
	SAFE_DELETE_ARRAY(m_paiFeatureProduction);
	SAFE_DELETE_ARRAY(m_pabFeatureRemove);
}

int CvBuildInfo::getEntityEvent() const
{
	return m_iEntityEvent;
}

int CvBuildInfo::getMissionType() const
{
	return m_iMissionType;
}

void CvBuildInfo::setMissionType(int iNewType)
{
	m_iMissionType = iNewType;
}

TechTypes CvBuildInfo::getFeatureTech(FeatureTypes eFeature) const
{
	FAssertEnumBounds(eFeature);
	return m_paiFeatureTech ? (TechTypes)m_paiFeatureTech[eFeature] : NO_TECH; // advc.003t
}

int CvBuildInfo::getFeatureTime(FeatureTypes eFeature) const
{
	FAssertEnumBounds(eFeature);
	return m_paiFeatureTime ? m_paiFeatureTime[eFeature] : 0; // advc.003t
}

int CvBuildInfo::getFeatureProduction(FeatureTypes eFeature) const
{
	FAssertEnumBounds(eFeature);
	return m_paiFeatureProduction ? m_paiFeatureProduction[eFeature] : 0; // advc.003t
}

bool CvBuildInfo::isFeatureRemove(FeatureTypes eFeature) const
{
	FAssertEnumBounds(eFeature);
	return m_pabFeatureRemove ? m_pabFeatureRemove[eFeature] : false;
}

bool CvBuildInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML))
		return false;

	pXML->SetInfoIDFromChildXmlVal(m_iTechPrereq, "PrereqTech");

	pXML->GetChildXmlValByName(&m_iTime, "iTime");
	pXML->GetChildXmlValByName(&m_iCost, "iCost");
	pXML->GetChildXmlValByName(&m_bKill, "bKill");

	pXML->SetInfoIDFromChildXmlVal(m_iImprovement, "ImprovementType");
	pXML->SetInfoIDFromChildXmlVal(m_iRoute, "RouteType");
	pXML->SetInfoIDFromChildXmlVal(m_iEntityEvent, "EntityEvent");

	pXML->SetFeatureStruct(&m_paiFeatureTech, &m_paiFeatureTime, &m_paiFeatureProduction, &m_pabFeatureRemove);

	return true;
}
