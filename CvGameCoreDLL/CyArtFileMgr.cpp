//
// Python wrapper class for CvArtFileMgr 
// 
#include "CvGameCoreDLL.h"
#include "CyArtFileMgr.h"
#include "CvArtFileMgr.h"
#include "CyGlobalContext.h"

CyArtFileMgr::CyArtFileMgr() : m_pArtFileMgr(NULL)
{
	m_pArtFileMgr = &ARTFILEMGR;
}

CyArtFileMgr::CyArtFileMgr(CvArtFileMgr* pArtFileMgr) : m_pArtFileMgr(pArtFileMgr)
{}

void CyArtFileMgr::Reset()
{
	if (m_pArtFileMgr)
	{
		m_pArtFileMgr->Reset();
	}
}

void CyArtFileMgr::buildArtFileInfoMaps()
{
	if (m_pArtFileMgr)
	{
		m_pArtFileMgr->buildArtFileInfoMaps();
	}
}

CvArtInfoInterface* CyArtFileMgr::getInterfaceArtInfo( const char * szArtDefineTag ) const
{
	return m_pArtFileMgr ? m_pArtFileMgr->getInterfaceArtInfo( szArtDefineTag ) : NULL;
}

CvArtInfoMovie* CyArtFileMgr::getMovieArtInfo( const char * szArtDefineTag ) const
{
	return m_pArtFileMgr ? m_pArtFileMgr->getMovieArtInfo( szArtDefineTag ) : NULL;
}

CvArtInfoMisc* CyArtFileMgr::getMiscArtInfo( const char * szArtDefineTag ) const
{
	return m_pArtFileMgr ? m_pArtFileMgr->getMiscArtInfo( szArtDefineTag ) : NULL;
}

CvArtInfoUnit* CyArtFileMgr::getUnitArtInfo( const char * szArtDefineTag ) const
{
	return m_pArtFileMgr ? m_pArtFileMgr->getUnitArtInfo( szArtDefineTag ) : NULL;
}

CvArtInfoBuilding* CyArtFileMgr::getBuildingArtInfo( const char * szArtDefineTag ) const
{
	return m_pArtFileMgr ? m_pArtFileMgr->getBuildingArtInfo( szArtDefineTag ) : NULL;
}

CvArtInfoCivilization* CyArtFileMgr::getCivilizationArtInfo( const char * szArtDefineTag ) const
{
	return m_pArtFileMgr ? m_pArtFileMgr->getCivilizationArtInfo( szArtDefineTag ) : NULL;
}

CvArtInfoLeaderhead* CyArtFileMgr::getLeaderheadArtInfo( const char * szArtDefineTag ) const
{
	return m_pArtFileMgr ? m_pArtFileMgr->getLeaderheadArtInfo( szArtDefineTag ) : NULL;
}

CvArtInfoBonus* CyArtFileMgr::getBonusArtInfo( const char * szArtDefineTag ) const
{
	return m_pArtFileMgr ? m_pArtFileMgr->getBonusArtInfo( szArtDefineTag ) : NULL;
}

CvArtInfoImprovement* CyArtFileMgr::getImprovementArtInfo( const char * szArtDefineTag ) const
{
	return m_pArtFileMgr ? m_pArtFileMgr->getImprovementArtInfo( szArtDefineTag ) : NULL;
}

CvArtInfoTerrain* CyArtFileMgr::getTerrainArtInfo( const char * szArtDefineTag ) const
{
	return m_pArtFileMgr ? m_pArtFileMgr->getTerrainArtInfo( szArtDefineTag ) : NULL;
}

CvArtInfoFeature* CyArtFileMgr::getFeatureArtInfo( const char * szArtDefineTag ) const
{
	return m_pArtFileMgr ? m_pArtFileMgr->getFeatureArtInfo( szArtDefineTag ) : NULL;
}
