// AUTHOR:  Jesse Smith / Mustafa Thamer	9/2004
// Interfaces with Civ4ArtDefines.xml to manage the paths of art files
//  Copyright (c) 2004 Firaxis Games, Inc. All rights reserved.
#include "CvGameCoreDLL.h"
#include "CvArtFileMgr.h"
#include "CvXMLLoadUtility.h"

// Macro for Building Art Info Maps
// (DEBUGGING)
#if 0
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
/*	creates a derived artItem class which automatically registers itself with
	the ARTFILEMGR upon construction. creates a static var of that artItem type,
	which constructs (and registers) at startup. creates a getFooArtInfo() function
	that searches the map based on the id provided and returns the artInfo struct
	or null. */
#define ART_INFO_DEFN(name) \
\
class Cv##name##ArtInfoItem : public CvArtFileMgr::ArtInfoItem \
{ \
	void init() { ARTFILEMGR.m_map##name##ArtInfos = new CvArtFileMgr::ArtInfo##name##MapType; } \
	void deInit(); \
	void buildMap() \
	{ \
		BUILD_INFO_MAP(*ARTFILEMGR.m_map##name##ArtInfos, ARTFILEMGR.get##name##ArtInfo, ARTFILEMGR.getNum##name##ArtInfos()); \
	} \
}; \
\
CvArtInfo##name* CvArtFileMgr::get##name##ArtInfo(char const* szArtDefineTag) const \
{ \
	FAssertMsg(szArtDefineTag, "NULL string on art info lookup?"); \
	ArtInfo##name##MapType::const_iterator it = m_map##name##ArtInfos->find(szArtDefineTag);\
	if (it == m_map##name##ArtInfos->end()) \
	{\
		char szErrorMsg[256]; \
		/* advc.001: Need to stringize for the error msg */ \
		sprintf(szErrorMsg, "get" #name "ArtInfo: %s was not found", szArtDefineTag); \
		FErrorMsg(szErrorMsg); \
		if (strcmp(szArtDefineTag, "ERROR") == 0) \
			return NULL; \
		return get##name##ArtInfo("ERROR"); \
	} \
	return it->second; \
} \
/* <advc> */\
TCHAR const* CvArtFileMgr::get##name##ArtPath(char const* szArtDefineTag) const \
{ \
	return get##name##ArtInfo(szArtDefineTag)->getPath(); \
} \
/* </advc> */ \
void Cv##name##ArtInfoItem::deInit() \
{ \
	SAFE_DELETE(ARTFILEMGR.m_map##name##ArtInfos); \
	for (uint i = 0; i < ARTFILEMGR.m_pa##name##ArtInfo.size(); i++) \
	{ \
		SAFE_DELETE(ARTFILEMGR.m_pa##name##ArtInfo[i]); \
	} \
	ARTFILEMGR.m_pa##name##ArtInfo.clear(); \
} \
CvArtInfo##name& CvArtFileMgr::get##name##ArtInfo(int i) { return *(m_pa##name##ArtInfo[i]); }


// Macros for the declaration of the art file info maps
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


/*	advc: Not nice to allocate the singleton with new and then never delete it.
	Use local static instances instead. Tbd.: Looks like the ArtInfo instances
	should really be members of the ArtFileMgr. */
#define ART_INFO_INST(name) static Cv##name##ArtInfoItem g##name##ArtInfoItem;
CvArtFileMgr& CvArtFileMgr::GetInstance()
{
	static CvArtFileMgr g_ArtFileMgr;
	ART_INFO_INST(Asset);
	ART_INFO_INST(Misc);
	ART_INFO_INST(Unit);
	ART_INFO_INST(Building);
	ART_INFO_INST(Civilization);
	ART_INFO_INST(Leaderhead);
	ART_INFO_INST(Bonus);
	ART_INFO_INST(Improvement);
	ART_INFO_INST(Terrain);
	ART_INFO_INST(Feature);
	ART_INFO_INST(Movie);
	ART_INFO_INST(Interface);
	return g_ArtFileMgr;
}

// Initializes the maps
void CvArtFileMgr::Init()
{
	for(size_t i = 0; i < m_artInfoItems.size(); i++)
		m_artInfoItems[i]->init();
}

// Deletes the maps
void CvArtFileMgr::DeInit()
{
	for(size_t i = 0; i < m_artInfoItems.size(); i++)
		m_artInfoItems[i]->deInit();
}

// Reloads the XML and rebuilds the maps
void CvArtFileMgr::Reset()
{	// <advc.007b> Reloading Art Defines (Ctrl+Alt+R) is broken; would crash.
	if(GC.IsGraphicsInitialized())
		return; // </advc.007b>
	DeInit(); // Cleans Art Defines
	CvXMLLoadUtility XMLLoadUtility;
	XMLLoadUtility.SetGlobalArtDefines(); // Reloads/allocs Art Defines
	Init(); // reallocs maps
	buildArtFileInfoMaps();
}

// advc.enum: (for CvGlobals::infosReset)
void CvArtFileMgr::resetInfo()
{
	#define RESET_ART_INFO(Name) \
		for (int i = 0; i < getNum##Name##ArtInfos(); i++) \
			get##Name##ArtInfo(i).reset();
	// These are the ones that used to be added to CvGlobals::m_aInfoVectors
	RESET_ART_INFO(Misc);
	RESET_ART_INFO(Unit);
	RESET_ART_INFO(Building);
	RESET_ART_INFO(Civilization);
	RESET_ART_INFO(Leaderhead);
	RESET_ART_INFO(Bonus);
	RESET_ART_INFO(Improvement);
	RESET_ART_INFO(Terrain);
	RESET_ART_INFO(Feature);
	RESET_ART_INFO(Movie);
	RESET_ART_INFO(Interface);
	#undef RESET_ART_INFO
}

// Builds the art file maps
void CvArtFileMgr::buildArtFileInfoMaps()
{
	for(size_t i = 0; i < m_artInfoItems.size(); i++)
		m_artInfoItems[i]->buildMap();
	testThemePath(); // advc.002b
}

// advc.002b: (The install location gets checked by CvGlobals::testInstallLocation)
void CvArtFileMgr::testThemePath()
{
	std::string sThmPath = getMiscArtPath("DEFAULT_THEME_NAME");
	size_t posMods = sThmPath.find("Mods/");
	size_t posRes = sThmPath.find("/Resource");
	std::string sModName = GC.getModName().getName();
	if (posMods == std::string::npos || posRes == std::string::npos)
	{
		/*	Has apparently been edited by the user - possibly reverted to the
			BtS theme, which is fine. */
		return;
	}
	std::string sThmPathModName = sThmPath.substr(posMods + 5, posRes - 5);
	// Temp. copy for lower case - the mod name isn't case-sensitive.
	std::string sModNameLC = sModName;
	if (cstring::tolower(sThmPathModName) == cstring::tolower(sModNameLC))
		return;
	CvString sMsg = "The DEFAULT_THEME_NAME path set in\n"
			"Mods\\";
	sMsg += sModName;
	sMsg += "\\Assets\\XML\\CIV4ArtDefines_Misc.xml\n"
			"does not appear to match the name of the mod folder.\n"
			"If you've renamed the mod folder, the name also needs\n"
			"to be changed in CIV4ArtDefines_Misc.xml and (twice) in\n"
			"Mods\\";
	sMsg += sModName;
	sMsg += "\\Resource\\Civ4.thm - otherwise,\n"
			"the UI theme will probably fail to load.\n";
	char szMessage[1024];
	sprintf(szMessage, sMsg);
	CvString sHeading = "Invalid path to UI theme";
	gDLL->MessageBox(szMessage, sHeading);
}

// advc.095: Hack for getting the EXE to switch between wide and narrow city bars
void CvArtFileMgr::swapCityBarPaths()
{
	m_bCityBarPathsSwapped = !m_bCityBarPathsSwapped;
	char const* aaszCityBarTags[][2] =
	{
		{ "INTERFACE_CITY_BAR_MODEL", "INTERFACE_WIDE_CITY_BAR_MODEL" },
		{ "INTERFACE_CITY_BAR_REGULAR_GLOW", "INTERFACE_WIDE_CITY_BAR_REGULAR_GLOW" },
		{ "INTERFACE_CITY_BAR_CAPITAL_GLOW", "INTERFACE_WIDE_CITY_BAR_CAPITAL_GLOW" }
	};
	int const iCityBarTags = ARRAYSIZE(aaszCityBarTags);
	CvArtInfoInterface* aapCityBarArtInfos[iCityBarTags][2];
	for (int i = 0; i < iCityBarTags; i++)
	{
		for (int j = 0; j < 2; j++)
		{
			aapCityBarArtInfos[i][j] = getInterfaceArtInfo(aaszCityBarTags[i][j]);
			if (aapCityBarArtInfos[i][j] == NULL)
				return; // Art file manager not ready (or tags missing in XML)
		}
	}
	for (int i = 0; i < iCityBarTags; i++)
	{
		CvString sTmp(aapCityBarArtInfos[i][0]->getPath());
		aapCityBarArtInfos[i][0]->setPath(aapCityBarArtInfos[i][1]->getPath());
		aapCityBarArtInfos[i][1]->setPath(sTmp);
	}
}
