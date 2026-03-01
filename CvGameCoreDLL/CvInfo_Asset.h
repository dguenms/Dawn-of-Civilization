#pragma once

#ifndef CV_INFO_ASSET_H
#define CV_INFO_ASSET_H

/*  advc.003x: CvAssetInfoBase and all its derived classes.
	Cut from CvInfos.h; to be precompiled, mainly b/c CvArtInfoUnit and
	CvArtInfoFeature are pretty big and none of these are going to change. */

class CvXMLLoadUtility;

/*	advc.003k (caveat): Changing the memory layout of CvArtInfoScalableAsset
	or any of its direct or indirect base classes is probably not safe b/c of
	multiple inheritance and type casts in the EXE. */

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvAssetInfoBase
//  Base for classes that store data from Art\Civ4ArtDefines.xml
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvAssetInfoBase : public CvInfoBase
{
	/*	advc.003k (caveat): Used to have an exported (blank) ctor. Not sure
		what this means for this class and its derived classes, i.e. to what extent
		their memory layout can be safely modified. */
public: // Exposed to Python (except 'read')
	const TCHAR* getTag() const;  // 'tag' is the same as 'type'
	void setTag(const TCHAR* szDesc);
	DllExport const TCHAR* getPath() const;
	void setPath(const TCHAR* szDesc);

	bool read(CvXMLLoadUtility* pXML);

protected:
	CvString m_szPath;
};

class CvArtInfoAsset : 	public CvAssetInfoBase
{
public: // Exposed to Python (except 'read')
	DllExport const TCHAR* getNIF() const;
	DllExport const TCHAR* getKFM() const;
	void setNIF(const TCHAR* szDesc);
	void setKFM(const TCHAR* szDesc);

	bool read(CvXMLLoadUtility* pXML);

protected:
	CvString m_szKFM;
	CvString m_szNIF;
};

// Another base class
class CvArtInfoScalableAsset : public CvArtInfoAsset, public CvScalableInfo
{
public:
	// <advc.xmldefault> (for LoadGlobalClassInfo template)
	CvArtInfoScalableAsset() {}
	CvArtInfoScalableAsset(CvArtInfoScalableAsset const& kOther);
	bool isDefaultsType() const { return false; }
	// </advc.xmldefault>
	bool read(CvXMLLoadUtility* pXML);
};

// todoJS: Remove empty classes if additional items are not added
// advc.003j (comment): Maybe they could be removed(?), but they're not simply unused.
class CvArtInfoInterface : public CvArtInfoAsset {};
class CvArtInfoMisc : public CvArtInfoScalableAsset {};
class CvArtInfoMovie : public CvArtInfoAsset {};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvArtInfoUnit
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvArtInfoUnit : public CvArtInfoScalableAsset
{
public:
	CvArtInfoUnit();

	// true if the unit acts as a ranged unit in combat (but may or may not be actually a ranged unit)
	DllExport bool getActAsRanged() const;
	DllExport bool getActAsLand() const;
	DllExport bool getActAsAir() const;

	// The NIF used if the graphics card supports shaders
	DllExport const TCHAR* getShaderNIF() const;
	void setShaderNIF(const TCHAR* szDesc);
	// The shadow blob NIF to use for the unit
	DllExport const TCHAR* getShadowNIF() const;
	// the scale of the unit's shadow.
	DllExport float getShadowScale() const;
	// The name of the node to which the shadow takes its x,y position
	DllExport const TCHAR* getShadowAttachNode() const;
	// The maximum number of damage states this unit type supports
	DllExport int getDamageStates() const;

	// The trail texture of the unit
	DllExport const TCHAR* getTrailTexture() const;
	// The width of the trail
	DllExport float getTrailWidth() const;
	// The length of the trail
	DllExport float getTrailLength() const;
	// Tapering of the trail
	DllExport float getTrailTaper() const;
	// Time after which the trail starts to fade
	DllExport float getTrailFadeStarTime() const; // advc: misspelled - should be ...StartTime
	// Speed at which the fade happens
	DllExport float getTrailFadeFalloff() const;

	// The preferred attack distance of this unit (1.0 == plot size)
	DllExport float getBattleDistance() const;
	// The offset from firing in which an opponent should die
	DllExport float getRangedDeathTime() const;
	// The angle at which the unit does combat.
	DllExport float getExchangeAngle() const;
	// true if the unit is 'exempt' from combat - ie. it just flees instead of dying
	DllExport bool getCombatExempt() const;
	// true if the unit should do non-linear interpolation for moves
	bool getSmoothMove() const;
	// The rate at which the units' angle interpolates
	float getAngleInterpRate() const;
	DllExport float getBankRate() const;

	bool read(CvXMLLoadUtility* pXML);

	const TCHAR* getTrainSound() const;
	void setTrainSound(const TCHAR* szVal);
	DllExport int getRunLoopSoundTag() const;
	DllExport int getRunEndSoundTag() const;
	DllExport int getPatrolSoundTag() const;
	int getSelectionSoundScriptId() const;
	int getActionSoundScriptId() const;

protected:
	CvString m_szShaderNIF;
	CvString m_szShadowNIF;
	CvString m_szShadowAttach;

	float m_fShadowScale;		

	int m_iDamageStates;
	bool m_bActAsRanged;
	bool m_bActAsLand;
	bool m_bActAsAir;
	bool m_bCombatExempt;
	bool m_bSmoothMove;

	CvString m_szTrailTexture;
	float m_fTrailWidth;
	float m_fTrailLength;
	float m_fTrailTaper;
	float m_fTrailFadeStartTime;
	float m_fTrailFadeFalloff;

	float m_fBattleDistance;
	float m_fRangedDeathTime;
	float m_fExchangeAngle;
	float m_fAngleInterRate;
	float m_fBankRate;

	CvString m_szTrainSound;
	int m_iRunLoopSoundTag;
	int m_iRunEndSoundTag;
	int m_iPatrolSoundTag;
	int m_iSelectionSoundScriptId;
	int m_iActionSoundScriptId;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvArtInfoBuilding
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvArtInfoBuilding : public CvArtInfoScalableAsset
{
public:
	CvArtInfoBuilding();

	bool isAnimated() const; // Exposed to Python
	DllExport const TCHAR* getLSystemName() const;

	bool read(CvXMLLoadUtility* pXML);

protected:
	bool m_bAnimated;
	CvString m_szLSystemName;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvArtInfoCivilization
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvArtInfoCivilization : public CvArtInfoAsset
{
public:
	CvArtInfoCivilization();

	bool isWhiteFlag() const; // Exposed to Python

	bool read(CvXMLLoadUtility* pXML);

protected:
	bool m_bWhiteFlag;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvArtInfoLeaderhead
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvArtInfoLeaderhead : public CvArtInfoAsset
{
public:
	DllExport const TCHAR* getNoShaderNIF() const;
	void setNoShaderNIF(const TCHAR* szNIF);
	DllExport const TCHAR* getBackgroundKFM() const;
	void setBackgroundKFM( const TCHAR* szKFM);

	bool read(CvXMLLoadUtility* pXML);

protected:
	CvString m_szNoShaderNIF;
	CvString m_szBackgroundKFM;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvArtInfoBonus
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvArtInfoBonus : public CvArtInfoScalableAsset
{
public:
	CvArtInfoBonus();

	int getFontButtonIndex() const;
	// The NIF used if the graphics card supports shaders
	DllExport const TCHAR* getShaderNIF() const;
	void setShaderNIF(const TCHAR* szDesc);

	bool read(CvXMLLoadUtility* pXML);

protected:
	CvString m_szShaderNIF;
	int m_iFontButtonIndex;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvArtInfoImprovement
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvArtInfoImprovement : public CvArtInfoScalableAsset
{
public:
	CvArtInfoImprovement();

	bool isExtraAnimations() const; // Exposed to Python
	// The NIF used if the graphics card supports shaders
	DllExport const TCHAR* getShaderNIF() const;
	void setShaderNIF(const TCHAR* szDesc);

	bool read(CvXMLLoadUtility* pXML);

protected:
	CvString m_szShaderNIF;
	bool m_bExtraAnimations;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvArtInfoTerrain
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
typedef std::vector<std::pair<int, int> > CvTextureBlendSlotList;

class CvArtInfoTerrain : public CvArtInfoAsset
{
public:
	CvArtInfoTerrain();
	~CvArtInfoTerrain();

	DllExport const TCHAR* getBaseTexture();
	void setBaseTexture(const TCHAR* szTmp);
	DllExport const TCHAR* getGridTexture();
	void setGridTexture(const TCHAR* szTmp);
	DllExport const TCHAR* getDetailTexture();
	// Detail texture associated with the Terrain base texture
	void setDetailTexture(const TCHAR* szTmp);
	// Layering order of texture
	DllExport int getLayerOrder();
	DllExport bool useAlphaShader();
	// Array of Textureslots per blend tile
	DllExport CvTextureBlendSlotList &getBlendList(int blendMask);

	bool read(CvXMLLoadUtility* pXML);

protected:
	CvString m_szDetailTexture;
	CvString m_szGridTexture;

	int m_iLayerOrder;
	bool m_bAlphaShader;
	int m_numTextureBlends;
	CvTextureBlendSlotList **m_pTextureSlots;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvArtInfoFeature
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvArtInfoFeature : public CvArtInfoScalableAsset
{
public:
	CvArtInfoFeature();

	DllExport bool isAnimated() const; // Exposed to Python
	DllExport bool isRiverArt() const; // Exposed to Python
	DllExport TileArtTypes getTileArtType() const;
	DllExport LightTypes getLightType() const;

	bool read(CvXMLLoadUtility* pXML);

	class FeatureArtModel
	{
	public:
		FeatureArtModel(const CvString &modelFile, RotationTypes rotation)
		{
			m_szModelFile = modelFile;
			m_eRotation = rotation;
		}
		const CvString &getModelFile() const
		{
			return m_szModelFile;
		}
		RotationTypes getRotation() const
		{
			return m_eRotation;
		}
	private:
		CvString m_szModelFile;
		RotationTypes m_eRotation;
	};

	class FeatureArtPiece
	{
	public:
		FeatureArtPiece(int connectionMask)
		{
			m_iConnectionMask = connectionMask;
		}
		int getConnectionMask() const
		{
			return m_iConnectionMask;
		}
		int getNumArtModels() const
		{
			return m_aArtModels.size();
		}
		const FeatureArtModel &getArtModel(int index) const
		{
			FAssertMsg((index >= 0) && (index < (int) m_aArtModels.size()), "[Jason] Invalid feature model file index.");
			return m_aArtModels[index];
		}
	private:
		std::vector<FeatureArtModel> m_aArtModels;
		int m_iConnectionMask;
		friend CvArtInfoFeature;
	};

	class FeatureDummyNode
	{
	public:
		FeatureDummyNode(const CvString &tagName, const CvString &nodeName)
		{
			m_szTag = tagName;
			m_szName = nodeName;
		}
		const CvString getTagName() const
		{
			return m_szTag;
		}
		const CvString getNodeName() const
		{
			return m_szName;
		}
	private:
		CvString m_szTag;
		CvString m_szName;
	};

	class FeatureVariety
	{
	public:
		const CvString &getVarietyButton() const
		{
			return m_szVarietyButton;
		}
		const FeatureArtPiece &getFeatureArtPiece(int index) const
		{
			FAssertMsg((index >= 0) && (index < (int) m_aFeatureArtPieces.size()), "[Jason] Invalid feature art index.");
			return m_aFeatureArtPieces[index];
		}
		const FeatureArtPiece &getFeatureArtPieceFromConnectionMask(int connectionMask) const
		{
			for(int i=0;i<(int)m_aFeatureArtPieces.size();i++)
				if(m_aFeatureArtPieces[i].getConnectionMask() == connectionMask)
					return m_aFeatureArtPieces[i];

			FErrorMsg("[Jason] Failed to find feature art piece with valid connection mask.");
			return m_aFeatureArtPieces[0];
		}
		const CvString getFeatureDummyNodeName(const CvString &tagName) const
		{
			for(int i=0;i<(int)m_aFeatureDummyNodes.size();i++)
			{
				if(m_aFeatureDummyNodes[i].getTagName().CompareNoCase(tagName) == 0)
					return m_aFeatureDummyNodes[i].getNodeName();
			}
			FErrorMsg("[Jason] Failed to find dummy tag name.");
			return "";
		}
		const CvString getFeatureDummyTag(const CvString &nodeName) const
		{
			for(int i=0;i<(int)m_aFeatureDummyNodes.size();i++)
			{
				if(m_aFeatureDummyNodes[i].getNodeName().CompareNoCase(nodeName) == 0)
					return m_aFeatureDummyNodes[i].getTagName();
			}

			return "";
		}
		FeatureArtPiece &createFeatureArtPieceFromConnectionMask(int connectionMask)
		{
			for(int i=0;i<(int)m_aFeatureArtPieces.size();i++)
				if(m_aFeatureArtPieces[i].getConnectionMask() == connectionMask)
					return m_aFeatureArtPieces[i];

			m_aFeatureArtPieces.push_back(FeatureArtPiece(connectionMask));
			return m_aFeatureArtPieces.back();
		}
		void createFeatureDummyNode(const CvString &tagName, const CvString &nodeName)
		{
			m_aFeatureDummyNodes.push_back(FeatureDummyNode(tagName, nodeName));
		}
	private:
		std::vector<FeatureArtPiece> m_aFeatureArtPieces;
		std::vector<FeatureDummyNode> m_aFeatureDummyNodes;
		CvString m_szVarietyButton;
		friend CvArtInfoFeature;
	};

	DllExport const FeatureVariety &getVariety(int index) const;
	DllExport int getNumVarieties() const;
	std::string getFeatureDummyNodeName(int variety, std::string tagName);

protected:
	int getConnectionMaskFromString(const CvString &connectionString);
	int getRotatedConnectionMask(int connectionMask, RotationTypes rotation);

	bool m_bAnimated;
	bool m_bRiverArt;
	TileArtTypes m_eTileArtType;
	LightTypes m_eLightType;
	std::vector<FeatureVariety> m_aFeatureVarieties;
};

#endif
