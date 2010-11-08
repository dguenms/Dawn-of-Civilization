//---------------------------------------------------------------------------------------
//
//  *****************   Civilization IV   ********************
//
//  FILE:    CvArtFileMgr.cpp
//
//  AUTHOR:  Jesse Smith / Mustafa Thamer	9/2004
//
//  PURPOSE: Interfaces with Civ4ArtDefines.xml to manage the paths of art files
//
//---------------------------------------------------------------------------------------
//  Copyright (c) 2004 Firaxis Games, Inc. All rights reserved.
//---------------------------------------------------------------------------------------
#include "CvGameCoreDLL.h"
#include "CvArtFileMgr.h"
#include "CvXMLLoadUtility.h"
#include "CvGlobals.h"
#include "CvInfos.h"
#include "CvDLLUtilityIFaceBase.h"

// Macro for Building Art Info Maps
#if 0	// DEBUGGING
#define BUILD_INFO_MAP(map, infoArray, numInfos) \
{ \
	int iI; \
	for (iI = 0; iI < numInfos; iI++) \
	{ \
		char temp[256];	\
		sprintf(temp, "type = %s\n", infoArray(iI).getType()); \
		OutputDebugString(temp); \
		sprintf(temp, "description = %S\n", infoArray(iI).getDescription()); \
		OutputDebugString(temp); \
		(map)[infoArray(iI).getTag()] = &infoArray(iI); \
	} \
}
#else
#define BUILD_INFO_MAP(map, infoArray, numInfos) \
{ \
	int iI; \
	for (iI = 0; iI < numInfos; iI++) \
	{ \
	(map)[infoArray(iI).getTag()] = &infoArray(iI); \
	} \
}
#endif

//
// creates a derived artItem class which automatically registers itself with the ARTFILEMGR upon contruction.
// creates a static var of that artItem type which constructs (and registers) at startup.
// creates a getFooArtInfo() function that searches the map based on the id provided and returns the artInfo struct or null.
//
#define ART_INFO_DEFN(name) \
\
class Cv##name##ArtInfoItem : public CvArtFileMgr::ArtInfoItem \
{ \
	void init() { ARTFILEMGR.m_map##name##ArtInfos = new CvArtFileMgr::ArtInfo##name##MapType; } \
	void deInit(); \
	void buildMap() { BUILD_INFO_MAP(*ARTFILEMGR.m_map##name##ArtInfos, ARTFILEMGR.get##name##ArtInfo, ARTFILEMGR.getNum##name##ArtInfos()); } \
}; \
\
static Cv##name##ArtInfoItem g##name##ArtInfoItem; \
\
CvArtInfo##name##* CvArtFileMgr::get##name##ArtInfo( const char *szArtDefineTag ) const \
{ \
	FAssertMsg(szArtDefineTag, "NULL string on art info lookup?"); \
	ArtInfo##name##MapType::const_iterator it = m_map##name##ArtInfos->find( szArtDefineTag );\
	if ( it == m_map##name##ArtInfos->end() ) \
	{\
		char szErrorMsg[256]; \
		sprintf(szErrorMsg, "get##name##ArtInfo: %s was not found", szArtDefineTag); \
		FAssertMsg(false, szErrorMsg ); \
		if ( 0 == strcmp(szArtDefineTag, "ERROR") ) \
		{ \
			return NULL; \
		} \
		else \
		{ \
			return get##name##ArtInfo( "ERROR" ); \
		} \
	} \
	return it->second; \
} \
void Cv##name##ArtInfoItem::deInit() \
{ \
	SAFE_DELETE(ARTFILEMGR.m_map##name##ArtInfos); \
	for (uint i = 0; i < ARTFILEMGR.m_pa##name##ArtInfo.size(); ++i) \
	{ \
		SAFE_DELETE(ARTFILEMGR.m_pa##name##ArtInfo[i]); \
	} \
	ARTFILEMGR.m_pa##name##ArtInfo.clear(); \
} \
CvArtInfo##name##& CvArtFileMgr::get##name##ArtInfo(int i) { return *(m_pa##name##ArtInfo[i]); }

//----------------------------------------------------------------------------
//
//	FUNCTION:	GetInstance()
//
//	PURPOSE:	Get the instance of this class.
//
//----------------------------------------------------------------------------
CvArtFileMgr& CvArtFileMgr::GetInstance()
{
	static CvArtFileMgr gs_ArtFileMgr;
	return gs_ArtFileMgr;
}

//----------------------------------------------------------------------------
//
//	FUNCTION:	Init()
//
//	PURPOSE:	Initializes the Maps
//
//----------------------------------------------------------------------------
void CvArtFileMgr::Init()
{
	int i;
	for(i=0;i<(int)m_artInfoItems.size();i++)
	{
		m_artInfoItems[i]->init();
	}
}

//----------------------------------------------------------------------------
//
//	FUNCTION:	DeInit()
//
//	PURPOSE:	Deletes the Maps
//
//----------------------------------------------------------------------------
void CvArtFileMgr::DeInit()
{
	int i;
	for(i=0;i<(int)m_artInfoItems.size();i++)
	{
		m_artInfoItems[i]->deInit();
	}
}

//----------------------------------------------------------------------------
//
//	FUNCTION:	Reset()
//
//	PURPOSE:	Reloads the XML & Rebuilds the Maps
//
//----------------------------------------------------------------------------
void CvArtFileMgr::Reset()
{
	DeInit();		// Cleans Art Defines
	CvXMLLoadUtility XMLLoadUtility;
	XMLLoadUtility.SetGlobalArtDefines();		// Reloads/allocs Art Defines
	Init();			// reallocs maps
	buildArtFileInfoMaps();
}

//----------------------------------------------------------------------------
//
//	FUNCTION:	buildArtFileInfoMaps()
//
//	PURPOSE:	Builds the Art File Maps
//
//----------------------------------------------------------------------------
void CvArtFileMgr::buildArtFileInfoMaps()
{
	int i;
	for(i=0;i<(int)m_artInfoItems.size();i++)
	{
		m_artInfoItems[i]->buildMap();
	}
}

// Macros the creation of the art file info maps
ART_INFO_DEFN(Asset);
ART_INFO_DEFN(Misc);
ART_INFO_DEFN(Unit);
ART_INFO_DEFN(Building);
ART_INFO_DEFN(Civilization);
ART_INFO_DEFN(Leaderhead);
ART_INFO_DEFN(Bonus);
ART_INFO_DEFN(Improvement);
ART_INFO_DEFN(Terrain);
ART_INFO_DEFN(Feature);
ART_INFO_DEFN(Movie);
ART_INFO_DEFN(Interface);
