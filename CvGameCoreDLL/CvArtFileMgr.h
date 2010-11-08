#pragma once

//---------------------------------------------------------------------------------------
//
//  *****************   Civilization IV   ********************
//
//  FILE:    CvArtFileMgr.h
//
//  AUTHOR:  Jesse Smith / Mustafa Thamer	9/2004
//
//  PURPOSE: Interfaces with Civ4ArtDefines.xml to manage the paths of art files
//
//---------------------------------------------------------------------------------------
//  Copyright (c) 2004 Firaxis Games, Inc. All rights reserved.
//---------------------------------------------------------------------------------------
#ifndef CIV4_ARTFILEMGR_H
#define CIV4_ARTFILEMGR_H

// Class:			CvArtFileMgr
// Purpose:		To Manage the Locations of Art Assets
//
// Adding a New Entry:
//		*	Create a new ArtInfo<new> in 'CvInfos.h' & add to CyInfosInterface
//		*	Add a new ART_INFO_DECL to 'CvArtFileMgr.h'
//		*	Add a new ART_INFO_DEFN to 'CvArtFileMgr.cpp'
//		*	Update Python 'CyGlobalContext & CyArtFileMgr' files
//		*	Add INIT_GLOBAL_XML_LOAD item to SetGlobalArtDefines in 'CvXMLLoadUtilitySet'
//		*	Add <new> to 'XML\Art\CIV4ArtDefines.xml' and update the 'CIV4ArtDefinesSchema'

class CvArtInfoAsset;
class CvArtInfoMisc;
class CvArtInfoUnit;
class CvArtInfoBuilding;
class CvArtInfoCivilization;
class CvArtInfoLeaderhead;
class CvArtInfoBonus;
class CvArtInfoImprovement;
class CvArtInfoTerrain;
class CvArtInfoFeature;
class CvArtInfoMovie;
class CvArtInfoInterface;

// Example usage: ART_INFO_DECL(Unit)
#define ART_INFO_DECL(name) \
public: \
	friend class Cv##name##ArtInfoItem; \
	DllExport CvArtInfo##name##* get##name##ArtInfo(const char *szArtDefineTag) const; \
	DllExport int getNum##name##ArtInfos() { return (int)m_pa##name##ArtInfo.size(); } \
	DllExport std::vector<CvArtInfo##name##*>& get##name##ArtInfo() { return m_pa##name##ArtInfo; } \
	DllExport CvArtInfo##name##& get##name##ArtInfo(int i); \
private: \
	typedef std::map<const char* /* index */,CvArtInfo##name##* /*value */, ltstr> ArtInfo##name##MapType; \
	ArtInfo##name##MapType* m_map##name##ArtInfos; \
	std::vector<CvArtInfo##name##*> m_pa##name##ArtInfo; \

class CvArtFileMgr
{
private:
	class ArtInfoItem
	{
	public:
		ArtInfoItem() { CvArtFileMgr::GetInstance().addArtInfoItem(this); }
		virtual void init() = 0;
		virtual void deInit() = 0;
		virtual void buildMap() = 0;
	};
public:
	// singleton accessor
	DllExport static CvArtFileMgr& GetInstance();

	DllExport CvArtFileMgr() {};
	DllExport virtual ~CvArtFileMgr() {};

	DllExport void Init();
	DllExport void DeInit();

	// Deletes Maps, Reloads Infos from XML, Rebuilds Maps
	DllExport void Reset();																														// Exposed to Python
	
	// Builds Maps
	DllExport void buildArtFileInfoMaps();																							// Exposed to Python

	// Adds an Art File List
	void addArtInfoItem(CvArtFileMgr::ArtInfoItem* item) { m_artInfoItems.push_back(item);	}
private:
	struct ltstr
	{
		bool operator()(const char* s1, const char* s2) const
		{
			return strcmp(s1, s2) < 0;
		}
	};

	ART_INFO_DECL(Asset);
	ART_INFO_DECL(Misc);
	ART_INFO_DECL(Unit);
	ART_INFO_DECL(Building);
	ART_INFO_DECL(Civilization);
	ART_INFO_DECL(Leaderhead);
	ART_INFO_DECL(Bonus);
	ART_INFO_DECL(Improvement);
	ART_INFO_DECL(Terrain);
	ART_INFO_DECL(Feature);
	ART_INFO_DECL(Movie);
	ART_INFO_DECL(Interface);

	std::vector<ArtInfoItem*> m_artInfoItems;
};

// Singleton Accessor
#define ARTFILEMGR CvArtFileMgr::GetInstance()

#endif
