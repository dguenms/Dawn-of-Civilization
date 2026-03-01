#pragma once

//  FILE:    CvInfos.h
//  PURPOSE: All Civ4 info classes and the base class for them
//  Copyright (c) 2003 Firaxis Games, Inc. All rights reserved.
/*  advc.003x: Renamed to CvInfo_Misc.h. I've moved the info classes that are
	essential for the game core DLL into various new CvInfo_... header files;
	only classes that no DLL implementation file needs to include separately
	remain here. Unused CvRiverInfo removed. And I've made some style changes. */

#ifndef CV_INFO_MISC_H
#define CV_INFO_MISC_H

// advc.003x: Include this with the other info classes that aren't needed in the DLL
#include "CvInfo_Water.h"

/*#pragma warning(disable: 251)
#pragma warning(disable: 127)*/ // advc.make: Handled by PragmaWarnings.h

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// class	: CvUnitFormationInfo
// \brief	: Holds information relating to the formation of sub-units within a unit
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvUnitEntry
{
public:
	CvUnitEntry() {}

	CvUnitEntry(const NiPoint2 &position, float radius, float facingDirection, float facingVariance) :
		m_position(position),
		m_fRadius(radius),
		m_fFacingDirection(facingDirection),
		m_fFacingVariance(facingVariance) {}

	NiPoint2 m_position;
	float m_fRadius;
	float m_fFacingDirection;
	float m_fFacingVariance;
};

class CvUnitFormationInfo : public CvInfoBase
{
public:
	DllExport CvUnitFormationInfo();
	DllExport ~CvUnitFormationInfo();

	DllExport const TCHAR* getFormationType() const;
	// The list of EntityEventTypes that this formation is intended for
	DllExport const std::vector<EntityEventTypes> & getEventTypes() const;

	DllExport int getNumUnitEntries() const;
	DllExport const CvUnitEntry &getUnitEntry(int index) const;
	DllExport void addUnitEntry(const CvUnitEntry &unitEntry);
	int getNumGreatUnitEntries() const;
	DllExport const CvUnitEntry &getGreatUnitEntry(int index) const;
	int getNumSiegeUnitEntries() const;
	DllExport const CvUnitEntry &getSiegeUnitEntry(int index) const;

	bool read(CvXMLLoadUtility* pXML);

protected:
	CvString m_szFormationType;
	std::vector<EntityEventTypes> m_vctEventTypes;

	std::vector<CvUnitEntry> m_vctUnitEntries;
	std::vector<CvUnitEntry> m_vctGreatUnitEntries;
	std::vector<CvUnitEntry> m_vctSiegeUnitEntries;
};

//class CvRiverInfo : public CvInfoBase {}; // unused

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvRiverModelInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvRiverModelInfo : public CvInfoBase
{
public: // All const functions are exposed to Python
	CvRiverModelInfo();

	DllExport const TCHAR* getModelFile() const; // The model filename
	DllExport const TCHAR* getBorderFile() const; // The border filename

	DllExport int getTextureIndex() const; // (not exposed to Python)
	DllExport const TCHAR* getDeltaString() const; // The delta type
	// The connections this cell makes ( N S E W NE NW SE SW )
	DllExport const TCHAR* getConnectString() const;
	// The possible rotations for this cell ( 0 90 180 270 )
	DllExport const TCHAR* getRotateString() const;

	bool read(CvXMLLoadUtility* pXML);

protected:
	CvString m_szModelFile;
	CvString m_szBorderFile;

	TCHAR m_szDeltaString[32];		
	TCHAR m_szConnectString[32];
	TCHAR m_szRotateString[32];
	int m_iTextureIndex;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvRouteModelInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvRouteModelInfo : public CvInfoBase
{
public: // All the const functions are exposed to Python
	CvRouteModelInfo();

	DllExport RouteTypes getRouteType() const; // The route type

	DllExport const TCHAR* getModelFile() const; // The model filename
	DllExport const TCHAR* getLateModelFile() const; // The model filename
	const TCHAR* getModelFileKey() const; // The model file key reference

	DllExport bool isAnimated() const;
	// The connections this cell makes ( N S E W NE NW SE SW )
	DllExport const TCHAR* getConnectString() const;
	// The connections this model makes ( N S E W NE NW SE SW )
	DllExport const TCHAR* getModelConnectString() const;
	// The possible rotations for this cell ( 0 90 180 270 )
	DllExport const TCHAR* getRotateString() const;

	bool read(CvXMLLoadUtility* pXML);

protected:
	RouteTypes	m_eRouteType;

	CvString m_szModelFile;
	CvString m_szLateModelFile;
	CvString m_szModelFileKey;
	bool m_bAnimated;

	TCHAR m_szConnectString[32];
	TCHAR m_szModelConnectString[32];
	TCHAR m_szRotateString[32];
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvAdvisorInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvAdvisorInfo : public CvInfoBase
{
public:
	const TCHAR* getTexture() const; // Exposed to Python
	int getNumCodes() const;
	int getEnableCode(uint uiCode) const;
	int getDisableCode(uint uiCode) const;

	bool read(CvXMLLoadUtility* pXML);

protected:
	CvString m_szTexture;
	std::vector<std::pair<int, int> > m_vctEnableDisableCodes;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvCursorInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvCursorInfo : public CvInfoBase
{
public:
	DllExport const TCHAR* getPath(); // Exposed to Python
	void setPath(const TCHAR* szVal);
	bool read(CvXMLLoadUtility* pXML);

protected:
	CvString m_szPath;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvThroneRoomCamera
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvThroneRoomCamera : public CvInfoBase
{
public:
	DllExport const TCHAR* getFileName();
	void setFileName(const TCHAR* szVal);
	bool read(CvXMLLoadUtility* pXML);

protected:
	CvString m_szFileName;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvThroneRoomInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvThroneRoomInfo : public CvInfoBase
{
public:
	CvThroneRoomInfo();

	DllExport const TCHAR* getEvent();
	DllExport const TCHAR* getNodeName();
	DllExport int getFromState();
	DllExport int getToState();
	DllExport int getAnimation();

	bool read(CvXMLLoadUtility* pXML);

protected:
	int m_iFromState;
	int m_iToState;
	int m_iAnimation;
	CvString m_szEvent;
	CvString m_szNodeName;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvThroneRoomStyleInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvThroneRoomStyleInfo : public CvInfoBase
{
public:
	DllExport const TCHAR* getArtStyleType();
	DllExport const TCHAR* getEraType();
	DllExport const TCHAR* getFileName();

	bool read(CvXMLLoadUtility* pXML);

protected:
	CvString m_szArtStyleType;
	CvString m_szEraType;
	CvString m_szFileName;
	std::vector<CvString> m_aNodeNames;
	std::vector<CvString> m_aTextureNames;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvSlideShowInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvSlideShowInfo : public CvInfoBase
{
public:
	CvSlideShowInfo();

	DllExport const TCHAR* getPath();
	void setPath(const TCHAR* szVal);
	DllExport const TCHAR* getTransitionType();
	void setTransitionType(const TCHAR* szVal);
	DllExport float getStartTime();
	void setStartTime(float fVal);

	bool read(CvXMLLoadUtility* pXML);

protected:
	float m_fStartTime;
	CvString m_szPath;
	CvString m_szTransitionType;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvSlideShowRandomInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvSlideShowRandomInfo : public CvInfoBase
{
public:
	DllExport const TCHAR* getPath();
	void setPath(const TCHAR* szVal);
	bool read(CvXMLLoadUtility* pXML);

protected:
	CvString m_szPath;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvWorldPickerInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvWorldPickerInfo : public CvInfoBase
{
public:
	DllExport const TCHAR* getMapName();
	DllExport const TCHAR* getModelFile();
	DllExport int getNumSizes();
	DllExport float getSize(int index);
	DllExport int getNumClimates();
	DllExport const TCHAR* getClimatePath(int index);
	DllExport int getNumWaterLevelDecals();
	DllExport const TCHAR* getWaterLevelDecalPath(int index);
	DllExport int getNumWaterLevelGloss();
	DllExport const TCHAR* getWaterLevelGlossPath(int index);

	bool read(CvXMLLoadUtility* pXML);

protected:
	CvString m_szMapName;
	CvString m_szModelFile;
	std::vector<float> m_aSizes;
	std::vector<CvString> m_aClimates;
	std::vector<CvString> m_aWaterLevelDecals;
	std::vector<CvString> m_aWaterLevelGloss;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvSpaceShipInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvSpaceShipInfo : public CvInfoBase
{
public:
	CvSpaceShipInfo();

	DllExport const TCHAR* getNodeName();
	DllExport const TCHAR* getProjectName();
	void setProjectName(const TCHAR* szVal);
	DllExport ProjectTypes getProjectType();
	DllExport AxisTypes getCameraUpAxis();
	DllExport SpaceShipInfoTypes getSpaceShipInfoType();
	DllExport int getPartNumber();
	DllExport int getArtType();
	DllExport int getEventCode();

	bool read(CvXMLLoadUtility* pXML);

protected:
	CvString m_szNodeName;
	CvString m_szProjectName;
	ProjectTypes m_eProjectType;
	AxisTypes m_eCameraUpAxis;
	int m_iPartNumber;
	int m_iArtType;
	int m_iEventCode;
	SpaceShipInfoTypes m_eSpaceShipInfoType;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvAnimationInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
typedef std::vector<std::pair<int,float> > CvAnimationPathDefinition;
typedef std::pair<int,int> CvAnimationCategoryDefinition;

class CvAnimationPathInfo : public CvInfoBase
{
public:
	CvAnimationPathInfo();

	DllExport int getPathCategory(int i);
	float getPathParameter(int i);
	DllExport int getNumPathDefinitions();
	DllExport CvAnimationPathDefinition* getPath();
	// True if this animation is used in missions
	DllExport bool isMissionPath() const;

	bool read(CvXMLLoadUtility* pXML);

private:
	CvAnimationPathDefinition m_vctPathDefinition; // Animation path definitions, pair(category,param).
	bool m_bMissionPath;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvAnimationCategoryInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvAnimationCategoryInfo : public CvInfoBase
{
public:
	CvAnimationCategoryInfo();

	DllExport int getCategoryBaseID();
	// Holds the default to parameter, until all categories are read
	DllExport int getCategoryDefaultTo();
	bool read(CvXMLLoadUtility* pXML);

private:
	CvAnimationCategoryDefinition m_kCategory; // The pair(base IDs, default categories) defining the animation categories
	CvString m_szDefaultTo;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvEntityEventInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvEntityEventInfo : public CvInfoBase
{
public:
	CvEntityEventInfo();

	bool read(CvXMLLoadUtility* pXML);

	DllExport AnimationPathTypes getAnimationPathType(int iIndex = 0) const;
	DllExport EffectTypes getEffectType(int iIndex = 0) const;
	int getAnimationPathCount() const;
	int getEffectTypeCount() const;
	bool getUpdateFormation() const;

private:
	std::vector<AnimationPathTypes> m_vctAnimationPathType;
	std::vector<EffectTypes> m_vctEffectTypes;
	bool m_bUpdateFormation;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvLandscapeInfo
//  Purpose:	This info acts as the Civ4Terrain.ini and is initialize in
//  CvXmlLoadUtility with the infos in XML/Terrain/TerrainSettings.xml
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvLandscapeInfo : public CvInfoBase
{
public:
	CvLandscapeInfo();

	int getFogR() const;
	int getFogG() const;
	int getFogB() const;
	DllExport int getHorizontalGameCell() const;
	DllExport int getVerticalGameCell() const;
	DllExport int getPlotsPerCellX() const;
	DllExport int getPlotsPerCellY() const;
	DllExport int getHorizontalVertCnt() const;
	DllExport int getVerticalVertCnt() const;
	DllExport int getWaterHeight() const;

	float getTextureScaleX() const;
	float getTextureScaleY() const;
	DllExport float getZScale() const;

	bool isUseTerrainShader() const;
	bool isUseLightmap() const;
	bool isRandomMap() const;
	DllExport float getPeakScale() const;
	DllExport float getHillScale() const;

	const TCHAR* getSkyArt();
	void setSkyArt(const TCHAR* szPath);
	const TCHAR* getHeightMap();
	void setHeightMap(const TCHAR* szPath);
	const TCHAR* getTerrainMap();
	void setTerrainMap(const TCHAR* szPath);
	const TCHAR* getNormalMap();
	void setNormalMap(const TCHAR* szPath);
	const TCHAR* getBlendMap();
	void setBlendMap(const TCHAR* szPath);

	bool read(CvXMLLoadUtility* pXML);

protected:
	int m_iFogR;
	int m_iFogG;
	int m_iFogB;
	int m_iHorizontalGameCell;
	int m_iVerticalGameCell;
	int m_iPlotsPerCellX;
	int m_iPlotsPerCellY;
	int m_iHorizontalVertCnt;
	int m_iVerticalVertCnt;
	int m_iWaterHeight;

	float m_fTextureScaleX;
	float m_fTextureScaleY;
	float m_fZScale;
	float m_fPeakScale;
	float m_fHillScale;

	bool m_bUseTerrainShader;
	bool m_bUseLightmap;
	bool m_bRandomMap;

	CvString m_szSkyArt;
	CvString m_szHeightMap;
	CvString m_szTerrainMap;
	CvString m_szNormalMap;
	CvString m_szBlendMap;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvGameText
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvGameText : public CvInfoBase
{
public:
	DllExport CvGameText();

	const wchar* getText() const;
	void setText(const wchar* szText);

	std::wstring pyGetText() const { return getText(); } // for Python

	void setGender(const wchar* szGender) { m_szGender = szGender; }
	const wchar* getGender() const { return m_szGender; }

	void setPlural(const wchar* szPlural) { m_szPlural = szPlural; }
	const wchar* getPlural() const { return m_szPlural; }

	DllExport int getNumLanguages() const; // not static for Python access
	DllExport void setNumLanguages(int iNum); // not static for Python access

	//bool read(CvXMLLoadUtility* pXML);
	// K-Mod
	// choose which language to load. nullptr means default
	bool read(CvXMLLoadUtility* pXML, const std::string& szLanguageName);
	bool read(CvXMLLoadUtility* pXML) { return read(pXML, ""); }
	// K-Mod end

protected:
	CvWString m_szText;
	CvWString m_szGender;
	CvWString m_szPlural;

	static int NUM_LANGUAGES;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvDiplomacyTextInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvDiplomacyTextInfo :	public CvInfoBase
{
	friend class CvXMLLoadUtility; // so it can initialize the class
public:
	struct Response
	{
		Response() :
			m_iNumDiplomacyText(0),
			m_pbCivilizationTypes(NULL),
			m_pbLeaderHeadTypes(NULL),
			m_pbAttitudeTypes(NULL),
			m_pbDiplomacyPowerTypes(NULL),
			m_paszDiplomacyText(NULL)
		{}

		~Response ()
		{
			SAFE_DELETE_ARRAY(m_pbCivilizationTypes);
			SAFE_DELETE_ARRAY(m_pbLeaderHeadTypes);
			SAFE_DELETE_ARRAY(m_pbAttitudeTypes);
			SAFE_DELETE_ARRAY(m_pbDiplomacyPowerTypes);
			SAFE_DELETE_ARRAY(m_paszDiplomacyText);
		}
		#if ENABLE_XML_FILE_CACHE
		void read(FDataStreamBase* stream);
		void write(FDataStreamBase* stream);
		#endif
		int m_iNumDiplomacyText;
		bool* m_pbCivilizationTypes;
		bool* m_pbLeaderHeadTypes;
		bool* m_pbAttitudeTypes;
		bool* m_pbDiplomacyPowerTypes;
		CvString* m_paszDiplomacyText; // needs to be public for xml load assignment
	};

	CvDiplomacyTextInfo();
	~CvDiplomacyTextInfo() { uninit(); } // free memory - MT

	// note - Response member vars allocated by CvXmlLoadUtility
	void init(int iNum);
	void uninit();

	const Response& getResponse(int iNum) const { return m_pResponses[iNum]; } // Exposed to Python
	int getNumResponses() const;															// Exposed to Python

	// These six are exposed to Python
	bool getCivilizationTypes(int i, int j) const;
	bool getLeaderHeadTypes(int i, int j) const;
	bool getAttitudeTypes(int i, int j) const;
	bool getDiplomacyPowerTypes(int i, int j) const;
	int getNumDiplomacyText(int i) const;
	const TCHAR* getDiplomacyText(int i, int j) const;

	#if ENABLE_XML_FILE_CACHE
	void read(FDataStreamBase* stream);
	void write(FDataStreamBase* stream);
	#endif
	bool read(CvXMLLoadUtility* pXML);

private:
	int m_iNumResponses; // set by init
	Response* m_pResponses;
};


//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvEffectInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvEffectInfo : public CvInfoBase, public CvScalableInfo
{
public:
	CvEffectInfo();
	// <advc.xmldefault> (for LoadGlobalClassInfo template)
	CvEffectInfo(CvEffectInfo const& kOther);
	bool isDefaultsType() const { return false; }
	// </advc.xmldefault>

	DllExport const TCHAR* getPath() const { return m_szPath; }
	/*	advc.003k (note): These used to be exported and have probably been
		inline-expanded in the EXE */
	void setPath(const TCHAR* szVal) { m_szPath = szVal; }
	float getUpdateRate() const { return m_fUpdateRate; };
	void setUpdateRate(float fUpdateRate) { m_fUpdateRate = fUpdateRate; }
	bool isProjectile() const { return m_bProjectile; };
	float getProjectileSpeed() const { return m_fProjectileSpeed; };
	float getProjectileArc() const { return m_fProjectileArc; };
	bool isSticky() const { return m_bSticky; };

	bool read(CvXMLLoadUtility* pXML);

private: // advc.003k (caveat): Probably not safe to rearrange data members
	CvString m_szPath;
	float m_fUpdateRate;
	bool m_bProjectile;
	bool m_bSticky;
	float m_fProjectileSpeed;
	float m_fProjectileArc;
};
/*	advc.003k: Probably OK to increase the size, but new data members should be
	added only after m_fProjectileArc. */
BOOST_STATIC_ASSERT(sizeof(CvEffectInfo) == 44 + sizeof(CvInfoBase) + sizeof(CvScalableInfo));

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvAttachableInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvAttachableInfo : public CvInfoBase, public CvScalableInfo
{
public:
	CvAttachableInfo();
	// <advc.xmldefault> (for LoadGlobalClassInfo template)
	CvAttachableInfo(CvAttachableInfo const& kOther);
	bool isDefaultsType() const { return false; }
	// </advc.xmldefault>

	DllExport const TCHAR* getPath() const { return m_szPath; }
	void setPath(const TCHAR* szVal) { m_szPath = szVal; }

	bool read(CvXMLLoadUtility* pXML);

private: /*	advc.003k (caveat): Might not be safe to add data before m_szPath b/c
			setPath used to be exported and may have been inlined in the EXE */
	CvString m_szPath;
	float m_fUpdateRate;
};

// advc.003j: unused
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvCameraInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
/*class CvCameraInfo : public CvInfoBase
{
public:
	CvCameraInfo() {}
	~CvCameraInfo() {}

	const TCHAR* getPath() const { return m_szPath; }
	void setPath(const TCHAR* szVal) { m_szPath = szVal; }
	bool read(CvXMLLoadUtility* pXML);

private:
	CvString m_szPath;
};*/

// advc.003j: unused
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvQuestInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
/*class CvQuestInfo : public CvInfoBase {
public:
	struct QuestLink {
		// Stores the QuestLinks Type and Name
		QuestLink() :
		m_szQuestLinkType("No Type"),
		m_szQuestLinkName("No Name")
		{}
	CvString m_szQuestLinkType;
	CvString m_szQuestLinkName;
	};

	CvQuestInfo();
	~CvQuestInfo();

	void reset();
	bool initQuestLinks(int iNum);

	int getNumQuestMessages() const;
	int getNumQuestLinks() const;
	int getNumQuestSounds() const;
	const TCHAR* getQuestObjective() const;
	const TCHAR* getQuestBodyText() const;
	const TCHAR* getQuestMessages(int iIndex) const;
	const TCHAR* getQuestLinkType(int iIndex) const;
	const TCHAR* getQuestLinkName(int iIndex) const;
	const TCHAR* getQuestSounds(int iIndex) const;
	const TCHAR* getQuestScript() const;

	void setNumQuestMessages(int iNum);
	void setNumQuestSounds(int iNum);
	void setQuestObjective(const TCHAR* szText);
	void setQuestBodyText(const TCHAR* szText);
	void setQuestMessages(int iIndex, const TCHAR* szText);
	void setQuestSounds(int iIndex, const TCHAR* szText);
	void setQuestScript(const TCHAR* szText);

	bool read(CvXMLLoadUtility* pXML);

private:
	int m_iNumQuestMessages;
	int m_iNumQuestLinks;
	int m_iNumQuestSounds;

	CvString m_szQuestObjective;
	CvString m_szQuestBodyText;
	CvString m_szQuestScript;

	CvString* m_paszQuestMessages;
	QuestLink* m_pQuestLinks;
	CvString* m_paszQuestSounds;
};*/

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvTutorialInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvTutorialMessage
{
public:
	CvTutorialMessage();
	~CvTutorialMessage();

	const TCHAR* getText() const;
	const TCHAR* getImage() const;
	const TCHAR* getSound() const;

	int getNumTutorialScripts() const;
	const TCHAR* getTutorialScriptByIndex(int i) const;
	bool read(CvXMLLoadUtility* pXML);

private:
	int m_iNumTutorialScripts;
	CvString m_szTutorialMessageText;
	CvString m_szTutorialMessageImage;
	CvString m_szTutorialMessageSound;
	CvString* m_paszTutorialScripts;
};

class CvTutorialMessage;
class CvTutorialInfo :
	public CvInfoBase
{
public:
	CvTutorialInfo();
	virtual ~CvTutorialInfo();

	const TCHAR* getNextTutorialInfoType();

	bool initTutorialMessages(int iNum);
	void resetMessages();

	int getNumTutorialMessages() const;
	const CvTutorialMessage* getTutorialMessage(int iIndex) const;

	bool read(CvXMLLoadUtility* pXML);

private:
	CvString m_szNextTutorialInfoType;
	int m_iNumTutorialMessages;
	CvTutorialMessage* m_paTutorialMessages;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvForceControlInfo - Forced Controls and their default values
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvForceControlInfo : public CvInfoBase
{
public:
	CvForceControlInfo();

	bool getDefault() const;
	bool read(CvXMLLoadUtility* pXML);

private:
	bool m_bDefault;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvPlayerOptionInfo - Player options and their default values
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvPlayerOptionInfo : public CvInfoBase
{
public:
	CvPlayerOptionInfo();

	DllExport bool getDefault() const;
	bool read(CvXMLLoadUtility* pXML);

private:
	bool m_bDefault;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvGraphicOptionInfo - Graphic options and their default values
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvGraphicOptionInfo : public CvInfoBase
{
public:
	CvGraphicOptionInfo();

	DllExport bool getDefault() const;
	bool read(CvXMLLoadUtility* pXML);

private:
	bool m_bDefault;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvMainMenuInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvMainMenuInfo : public CvInfoBase
{
public:
	DllExport std::string getScene() const;
	DllExport std::string getSceneNoShader() const;
	DllExport std::string getSoundtrack() const;
	DllExport std::string getLoading() const;
	DllExport std::string getLoadingSlideshow() const;

	bool read(CvXMLLoadUtility* pXML);

protected:
	std::string m_szScene;
	std::string m_szSceneNoShader;
	std::string m_szSoundtrack;
	std::string m_szLoading;
	std::string m_szLoadingSlideshow;
};
#endif
