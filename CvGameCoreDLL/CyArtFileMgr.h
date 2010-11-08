#pragma once

#ifndef CyArtFileMgr_h
#define CyArtFileMgr_h

//
// Python wrapper class for CvArtFileMgr
//

class CvArtFileMgr;
class CvArtInfoInterface;
class CvArtInfoMovie;
class CvArtInfoMisc;
class CvArtInfoUnit;
class CvArtInfoGenericBuilding;
class CvArtInfoGenericCity;
class CvArtInfoBuilding;
class CvArtInfoLeaderhead;
class CvArtInfoBonus;
class CvArtInfoImprovement;
class CvArtInfoTerrain;
class CvArtInfoFeature;
class CvArtInfoCivilization;
class CyArtFileMgr 
{
public:
	CyArtFileMgr();
	CyArtFileMgr(CvArtFileMgr* pArtFileMgr);			// Call from C++
	bool isNone() { return (m_pArtFileMgr==NULL); }

	void Reset();
	void buildArtFileInfoMaps();

	CvArtInfoInterface* getInterfaceArtInfo( const char * szArtDefineTag ) const;
	CvArtInfoMovie* getMovieArtInfo( const char * szArtDefineTag ) const;
	CvArtInfoMisc* getMiscArtInfo( const char * szArtDefineTag ) const;
	CvArtInfoUnit* getUnitArtInfo( const char * szArtDefineTag ) const;
	CvArtInfoGenericBuilding* getGenericBuildingArtInfo( const char * szArtDefineTag ) const;
	CvArtInfoGenericCity* getGenericCityArtInfo( const char * szArtDefineTag ) const;
	CvArtInfoBuilding* getBuildingArtInfo( const char * szArtDefineTag ) const;
	CvArtInfoCivilization* getCivilizationArtInfo( const char * szArtDefineTag ) const;
	CvArtInfoLeaderhead* getLeaderheadArtInfo( const char * szArtDefineTag ) const;
	CvArtInfoBonus* getBonusArtInfo( const char * szArtDefineTag ) const;
	CvArtInfoImprovement* getImprovementArtInfo( const char * szArtDefineTag ) const;
	CvArtInfoTerrain* getTerrainArtInfo( const char * szArtDefineTag ) const;
	CvArtInfoFeature* getFeatureArtInfo( const char * szArtDefineTag ) const;
	
protected:
	CvArtFileMgr* m_pArtFileMgr;
};

#endif	// #ifndef CyArtFileMgr
