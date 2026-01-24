// advc.003x: Cut from CvInfos.cpp

#include "CvGameCoreDLL.h"
#include "CvXMLLoadUtility.h"


const TCHAR* CvAssetInfoBase::getTag() const
{
	return getType();
}

void CvAssetInfoBase::setTag(const TCHAR* szDesc)
{
	m_szType = szDesc;
}

const TCHAR* CvAssetInfoBase::getPath() const
{
	return m_szPath;
}

void CvAssetInfoBase::setPath(const TCHAR* szDesc)
{
	m_szPath = szDesc;
}

bool CvAssetInfoBase::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
		return false;

	CvString szTextVal;
	pXML->GetChildXmlValByName(szTextVal, "Path", /* advc.006b: */ "");
	setPath(szTextVal);

	return true;
}

const TCHAR* CvArtInfoAsset::getNIF() const
{
	/*	advc.007 (from WtP): To find the XML type tag that causes a
		"texture failed to load" error in resmgr.log. NB: Failures to load
		FlagDECAL.dds and PlayerColor01.tga, ...02.tga are issues introduced
		by the BUG mod, difficult to diagnose, probably (pretty) harmless. */
	/*CvString szMsg;
	szMsg.Format("Opening nif for tag: %s", getTag());
	gDLL->logMsg("resmgr.log", szMsg);*/
	return m_szNIF;
}

const TCHAR* CvArtInfoAsset::getKFM() const
{
	return m_szKFM;
}

void CvArtInfoAsset::setNIF(const TCHAR* szDesc)
{
	m_szNIF = szDesc;
}

void CvArtInfoAsset::setKFM(const TCHAR* szDesc)
{
	m_szKFM = szDesc;
}

bool CvArtInfoAsset::read(CvXMLLoadUtility* pXML)
{
	if (!CvAssetInfoBase::read(pXML))
		return false;

	CvString szTextVal;
	pXML->GetChildXmlValByName(szTextVal, "NIF", /* advc.006b: */ "");
	setNIF(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "KFM", /* advc.006b: */ "");
	setKFM(szTextVal);

	return true;
}
// advc.xmldefault:
CvArtInfoScalableAsset::CvArtInfoScalableAsset(CvArtInfoScalableAsset const& kOther)
{
	FErrorMsg("No copy-ctor implemented");
}

bool CvArtInfoScalableAsset::read(CvXMLLoadUtility* pXML)
{
	if (!CvArtInfoAsset::read(pXML))
		return false;

	return CvScalableInfo::read(pXML);
}

CvArtInfoUnit::CvArtInfoUnit() :
m_fShadowScale(0.0f),
m_iDamageStates(0),
m_bActAsRanged(false),
m_bActAsLand(false),
m_bActAsAir(false),
m_bCombatExempt(false),
m_fTrailWidth(0.0f),
m_fTrailLength(0.0f),
m_fTrailTaper(0.0f),
m_fTrailFadeStartTime(0.0f),
m_fTrailFadeFalloff(0.0f),
m_fBattleDistance(0.0f), // kmodx
m_fRangedDeathTime(0.0f),
m_fExchangeAngle(0.0f),
m_bSmoothMove(false),
m_fAngleInterRate(FLT_MAX),
m_fBankRate(0),
m_iRunLoopSoundTag(0),
m_iRunEndSoundTag(0),
m_iSelectionSoundScriptId(0),
m_iActionSoundScriptId(0),
m_iPatrolSoundTag(0)
{}

bool CvArtInfoUnit::getActAsRanged() const
{
	return m_bActAsRanged;
}

bool CvArtInfoUnit::getActAsLand() const
{
	return m_bActAsLand;
}

bool CvArtInfoUnit::getActAsAir() const
{
	return m_bActAsAir;
}

const TCHAR* CvArtInfoUnit::getShaderNIF() const
{
	return m_szShaderNIF;
}

void CvArtInfoUnit::setShaderNIF(const TCHAR* szDesc)
{
	m_szShaderNIF = szDesc;
}

const TCHAR* CvArtInfoUnit::getShadowNIF() const
{
	return m_szShadowNIF;
}

float CvArtInfoUnit::getShadowScale() const
{
	return m_fShadowScale;
}

const TCHAR* CvArtInfoUnit::getShadowAttachNode() const
{
	return m_szShadowAttach;
}

int CvArtInfoUnit::getDamageStates() const
{
	return m_iDamageStates;
}


const TCHAR* CvArtInfoUnit::getTrailTexture() const
{
	return m_szTrailTexture;
}

float CvArtInfoUnit::getTrailWidth() const
{
	return m_fTrailWidth;
}

float CvArtInfoUnit::getTrailLength() const
{
	return m_fTrailLength;
}

float CvArtInfoUnit::getTrailTaper() const
{
	return m_fTrailTaper;
}

float CvArtInfoUnit::getTrailFadeStarTime() const
{
	return m_fTrailFadeStartTime;
}

float CvArtInfoUnit::getTrailFadeFalloff() const
{
	return m_fTrailFadeFalloff;
}

float CvArtInfoUnit::getBattleDistance() const
{
	return m_fBattleDistance;
}

float CvArtInfoUnit::getRangedDeathTime() const
{
	return m_fRangedDeathTime;
}

float CvArtInfoUnit::getExchangeAngle() const
{
	return m_fExchangeAngle;
}

bool CvArtInfoUnit::getCombatExempt() const
{
	return m_bCombatExempt;
}

bool CvArtInfoUnit::getSmoothMove() const
{
	return m_bSmoothMove;
}

float CvArtInfoUnit::getAngleInterpRate() const
{
	return m_fAngleInterRate;
}

float CvArtInfoUnit::getBankRate() const
{
	return m_fBankRate;
}

bool CvArtInfoUnit::read(CvXMLLoadUtility* pXML)
{
	if (!CvArtInfoScalableAsset::read(pXML))
		return false;

	CvString szTextVal;

	pXML->GetChildXmlValByName(szTextVal, "ActionSound", /* advc.006b: */ "");
	m_iActionSoundScriptId = (szTextVal.GetLength() > 0) ? gDLL->getAudioTagIndex(szTextVal.GetCString(), AUDIOTAG_3DSCRIPT) : -1;
	pXML->GetChildXmlValByName(szTextVal, "SelectionSound", /* advc.006b: */ "");
	m_iSelectionSoundScriptId = (szTextVal.GetLength() > 0) ? gDLL->getAudioTagIndex(szTextVal.GetCString(), AUDIOTAG_3DSCRIPT) : -1;
	pXML->GetChildXmlValByName(szTextVal, "PatrolSound", /* advc.006b: */ "");
	m_iPatrolSoundTag = (szTextVal.GetLength() > 0) ? gDLL->getAudioTagIndex( szTextVal.GetCString(), AUDIOTAG_3DSCRIPT) : -1;

	pXML->GetChildXmlValByName(szTextVal, "TrainSound", /* advc.006b: */ "");
	setTrainSound(szTextVal);

	pXML->GetChildXmlValByName(&m_bActAsRanged, "bActAsRanged");
	pXML->GetChildXmlValByName(&m_bActAsLand, "bActAsLand");
	pXML->GetChildXmlValByName(&m_bActAsAir, "bActAsAir");
	pXML->GetChildXmlValByName(&m_bCombatExempt, "bCombatExempt", false);
	pXML->GetChildXmlValByName(&m_fExchangeAngle, "fExchangeAngle", 0.0f);
	pXML->GetChildXmlValByName(&m_bSmoothMove, "bSmoothMove", false);
	pXML->GetChildXmlValByName(&m_fAngleInterRate, "fAngleInterpRate", FLT_MAX);
	pXML->GetChildXmlValByName(&m_fBankRate, "fBankRate", 0);

	pXML->GetChildXmlValByName(szTextVal, "SHADERNIF", /* advc.006b: */ "");
	setShaderNIF(szTextVal);

	if ( gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "ShadowDef"))
	{
		pXML->GetChildXmlValByName(m_szShadowAttach, "ShadowAttachNode");
		pXML->GetChildXmlValByName(m_szShadowNIF, "ShadowNIF");
		pXML->GetChildXmlValByName(&m_fShadowScale, "fShadowScale");
		gDLL->getXMLIFace()->SetToParent( pXML->GetXML());
	}

	pXML->GetChildXmlValByName(&m_iDamageStates, "iDamageStates", 0);
	pXML->GetChildXmlValByName(&m_fBattleDistance, "fBattleDistance", 0.0f);
	pXML->GetChildXmlValByName(&m_fRangedDeathTime, "fRangedDeathTime", 0.0f);

	m_fTrailWidth = -1.0f; // invalid.
	if ( gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "TrailDefinition"))
	{
		pXML->GetChildXmlValByName(m_szTrailTexture, "Texture");
		pXML->GetChildXmlValByName(&m_fTrailWidth, "fWidth");
		pXML->GetChildXmlValByName(&m_fTrailLength, "fLength");
		pXML->GetChildXmlValByName(&m_fTrailTaper, "fTaper");
		pXML->GetChildXmlValByName(&m_fTrailFadeStartTime, "fFadeStartTime");
		pXML->GetChildXmlValByName(&m_fTrailFadeFalloff, "fFadeFalloff");
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "AudioRunSounds"))
	{
		pXML->GetChildXmlValByName(szTextVal, "AudioRunTypeLoop");
		m_iRunLoopSoundTag = CvGlobals::getInstance().getFootstepAudioTypeByTag(szTextVal);
		pXML->GetChildXmlValByName(szTextVal, "AudioRunTypeEnd");
		m_iRunEndSoundTag = CvGlobals::getInstance().getFootstepAudioTypeByTag(szTextVal);
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	return true;
}

const TCHAR* CvArtInfoUnit::getTrainSound() const
{
	return m_szTrainSound;
}

void CvArtInfoUnit::setTrainSound(const TCHAR* szVal)
{
	m_szTrainSound = szVal;
}

int CvArtInfoUnit::getRunLoopSoundTag() const
{
	return m_iRunLoopSoundTag;
}

int CvArtInfoUnit::getRunEndSoundTag() const
{
	return m_iRunEndSoundTag;
}

int CvArtInfoUnit::getPatrolSoundTag() const
{
	return m_iPatrolSoundTag;
}

int CvArtInfoUnit::getSelectionSoundScriptId() const
{
	return m_iSelectionSoundScriptId;
}

int CvArtInfoUnit::getActionSoundScriptId() const
{
	return m_iActionSoundScriptId;
}

CvArtInfoBuilding::CvArtInfoBuilding() : m_bAnimated(false) {}

bool CvArtInfoBuilding::isAnimated() const
{
	return m_bAnimated;
}

const TCHAR* CvArtInfoBuilding::getLSystemName() const
{
	return m_szLSystemName;
}

bool CvArtInfoBuilding::read(CvXMLLoadUtility* pXML)
{
	if (!CvArtInfoScalableAsset::read(pXML))
		return false;

	pXML->GetChildXmlValByName(m_szLSystemName, "LSystem");

	pXML->GetChildXmlValByName(&m_bAnimated, "bAnimated");
	return true;
}

CvArtInfoCivilization::CvArtInfoCivilization() : m_bWhiteFlag(false) {}

bool CvArtInfoCivilization::isWhiteFlag() const
{
	return m_bWhiteFlag;
}

bool CvArtInfoCivilization::read(CvXMLLoadUtility* pXML)
{
	if (!CvArtInfoAsset::read(pXML))
		return false;

	pXML->GetChildXmlValByName(&m_bWhiteFlag, "bWhiteFlag");
	return true;
}

const TCHAR* CvArtInfoLeaderhead::getNoShaderNIF() const
{
	return m_szNoShaderNIF;
}

void CvArtInfoLeaderhead::setNoShaderNIF(const TCHAR* szNIF)
{
	m_szNoShaderNIF = szNIF;
}

const TCHAR* CvArtInfoLeaderhead::getBackgroundKFM() const
{
	return m_szBackgroundKFM;
}

void CvArtInfoLeaderhead::setBackgroundKFM( const TCHAR* szKFM)
{
	m_szBackgroundKFM = szKFM;
}

bool CvArtInfoLeaderhead::read(CvXMLLoadUtility* pXML)
{
	if (!CvArtInfoAsset::read(pXML))
		return false;

	CvString szTextVal;
	pXML->GetChildXmlValByName(szTextVal, "NoShaderNIF");
	setNoShaderNIF(szTextVal);
	if (pXML->GetChildXmlValByName(szTextVal, "BackgroundKFM"))
		setBackgroundKFM(szTextVal);
	else setBackgroundKFM("");

	return true;
}

bool CvArtInfoBonus::read(CvXMLLoadUtility* pXML)
{
	if (!CvArtInfoScalableAsset::read(pXML))
		return false;

	CvString szTextVal;
	pXML->GetChildXmlValByName(szTextVal, "SHADERNIF", /* advc.006b: */ "");
	setShaderNIF(szTextVal);
	pXML->GetChildXmlValByName(&m_iFontButtonIndex, "FontButtonIndex");
	return true;
}

CvArtInfoBonus::CvArtInfoBonus()
{
	m_iFontButtonIndex = 0;
}

int CvArtInfoBonus::getFontButtonIndex() const
{
	return m_iFontButtonIndex;
}

const TCHAR* CvArtInfoBonus::getShaderNIF() const
{
	return m_szShaderNIF;
}

void CvArtInfoBonus::setShaderNIF(const TCHAR* szDesc)
{
	m_szShaderNIF = szDesc;
}

CvArtInfoImprovement::CvArtInfoImprovement() : m_bExtraAnimations(false) {}

bool CvArtInfoImprovement::isExtraAnimations() const
{
	return m_bExtraAnimations;
}

bool CvArtInfoImprovement::read(CvXMLLoadUtility* pXML)
{
	if (!CvArtInfoScalableAsset::read(pXML))
		return false;

	pXML->GetChildXmlValByName(&m_bExtraAnimations, "bExtraAnimations");

	CvString szTextVal;
	pXML->GetChildXmlValByName(szTextVal, "SHADERNIF", /* advc.006b: */ "");
	setShaderNIF(szTextVal);

	return true;
}

CvArtInfoTerrain::CvArtInfoTerrain() :
m_iLayerOrder(0),
m_bAlphaShader(false),
m_numTextureBlends(16),
m_pTextureSlots(NULL)
{
	m_pTextureSlots = new CvTextureBlendSlotList * [m_numTextureBlends];
	for (int i = 0; i < m_numTextureBlends; i++)
		m_pTextureSlots[i] = new CvTextureBlendSlotList;
}

CvArtInfoTerrain::~CvArtInfoTerrain()
{
	for (int i = 0; i < m_numTextureBlends; i++)
		SAFE_DELETE(m_pTextureSlots[i]);
	SAFE_DELETE_ARRAY( m_pTextureSlots);
}

const TCHAR* CvArtInfoTerrain::getBaseTexture()
{
	return getPath();
}

void CvArtInfoTerrain::setBaseTexture(const TCHAR* szTmp)
{
	setPath(szTmp);
}

const TCHAR* CvArtInfoTerrain::getGridTexture()
{
	return m_szGridTexture;
}

void CvArtInfoTerrain::setGridTexture(const TCHAR* szTmp)
{
	m_szGridTexture = szTmp;
}

const TCHAR* CvArtInfoTerrain::getDetailTexture()
{
	return m_szDetailTexture;
}

void CvArtInfoTerrain::setDetailTexture(const TCHAR* szTmp)
{
	m_szDetailTexture = szTmp;
}

int CvArtInfoTerrain::getLayerOrder()
{
	return m_iLayerOrder;
}

bool CvArtInfoTerrain::useAlphaShader()
{
	return m_bAlphaShader;
}

CvTextureBlendSlotList &CvArtInfoTerrain::getBlendList(int blendMask)
{
	FAssert(blendMask>0 && blendMask<16);
	return *m_pTextureSlots[blendMask];
}
namespace // advc
{
	void BuildSlotList(CvTextureBlendSlotList &list, CvString &numlist)
	{
		//convert string to
		char seps[]   = " ,\t\n";
		char *token;
		const char *numstring = numlist;
		token = strtok( const_cast<char *>(numstring), seps);
		while(token != NULL)
		{
			int slot = atoi(token);
			token = strtok( NULL, seps);
			int rotation = atoi(token);
			list.push_back(std::make_pair( slot, rotation));
			token = strtok( NULL, seps);
		}
	}
}
bool CvArtInfoTerrain::read(CvXMLLoadUtility* pXML)
{
	if (!CvArtInfoAsset::read(pXML))
		return false;

	CvString szTextVal;

	pXML->GetChildXmlValByName(szTextVal, "Grid");
	setGridTexture(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "Detail");
	setDetailTexture(szTextVal);
	pXML->GetChildXmlValByName(&m_iLayerOrder, "LayerOrder");
	pXML->GetChildXmlValByName(&m_bAlphaShader, "AlphaShader");

	// Parse texture slots for blend tile lists
	char xmlName[] = "TextureBlend00";
	for(int i =1; i < m_numTextureBlends; i++)
	{
		sprintf(xmlName+(strlen(xmlName)-2),"%02d",i);
		pXML->GetChildXmlValByName(szTextVal, xmlName);
		BuildSlotList(*m_pTextureSlots[i], szTextVal);
	}

	return CvArtInfoAsset::read(pXML);
}


CvArtInfoFeature::CvArtInfoFeature() :
m_bAnimated(false),
m_bRiverArt(false),
m_eTileArtType(TILE_ART_TYPE_NONE),
m_eLightType(LIGHT_TYPE_NONE)
{}

bool CvArtInfoFeature::isAnimated() const
{
	return m_bAnimated;
}

bool CvArtInfoFeature::isRiverArt() const
{
	return m_bRiverArt;
}

TileArtTypes CvArtInfoFeature::getTileArtType() const
{
	return m_eTileArtType;
}

LightTypes CvArtInfoFeature::getLightType() const
{
	return m_eLightType;
}

bool CvArtInfoFeature::read(CvXMLLoadUtility* pXML)
{
	if (!CvArtInfoScalableAsset::read(pXML))
		return false;

	pXML->GetChildXmlValByName(&m_bAnimated, "bAnimated");
	pXML->GetChildXmlValByName(&m_bRiverArt, "bRiverArt");

	CvString szTemp;
	pXML->GetChildXmlValByName(szTemp, "TileArtType");
	if(szTemp.CompareNoCase("TILE_ART_TYPE_NONE") == 0)
		m_eTileArtType = TILE_ART_TYPE_NONE;
	else if(szTemp.CompareNoCase("TILE_ART_TYPE_TREES") == 0)
		m_eTileArtType = TILE_ART_TYPE_TREES;
	else if(szTemp.CompareNoCase("TILE_ART_TYPE_HALF_TILING") == 0)
		m_eTileArtType = TILE_ART_TYPE_HALF_TILING;
	else if(szTemp.CompareNoCase("TILE_ART_TYPE_PLOT_TILING") == 0)
		m_eTileArtType = TILE_ART_TYPE_PLOT_TILING;
	else FErrorMsg("[Jason] Unknown TileArtType.");

	pXML->GetChildXmlValByName(szTemp, "LightType");
	if(szTemp.CompareNoCase("LIGHT_TYPE_NONE") == 0)
		m_eLightType = LIGHT_TYPE_NONE;
	else if(szTemp.CompareNoCase("LIGHT_TYPE_SUN") == 0)
		m_eLightType = LIGHT_TYPE_SUN;
	else if(szTemp.CompareNoCase("LIGHT_TYPE_TERRAIN") == 0)
		m_eLightType = LIGHT_TYPE_TERRAIN;
	else if(szTemp.CompareNoCase("LIGHT_TYPE_UNIT") == 0)
		m_eLightType = LIGHT_TYPE_UNIT;
	else FErrorMsg("[Jason] Unknown LightType.");

	//feature varieties
	if(gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"FeatureVariety"))
	{
		do
		{
			m_aFeatureVarieties.push_back(FeatureVariety());
			FeatureVariety &featureVariety = m_aFeatureVarieties.back();

			//generate rotations
			bool generateRotations = false;
			pXML->GetChildXmlValByName(&generateRotations, "bGenerateRotations");

			//feature art pieces
			if(gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"FeatureArtPieces"))
			{
				if(gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"FeatureArtPiece"))
				{
					do
					{
						//connection mask
						pXML->GetChildXmlValByName(szTemp, "Connections");
						int connectionMask = getConnectionMaskFromString(szTemp);

						//model files
						if(gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"ModelFile"))
						{
							do
							{
								pXML->GetXmlVal(szTemp);
								if(!generateRotations)
								{
									FeatureArtPiece &featureArtPiece = featureVariety.createFeatureArtPieceFromConnectionMask(connectionMask);
									featureArtPiece.m_aArtModels.push_back(FeatureArtModel(szTemp, ROTATE_NONE));
								}
								else
								{
									for(int i = 0; i < NUM_ROTATION_TYPES; i++)
									{
										int newConnectionMask = getRotatedConnectionMask(connectionMask, (RotationTypes) i);
										FeatureArtPiece &featureArtPiece = featureVariety.createFeatureArtPieceFromConnectionMask(newConnectionMask);
										featureArtPiece.m_aArtModels.push_back(FeatureArtModel(szTemp, (RotationTypes) i));
									}
								}
							} while(gDLL->getXMLIFace()->LocateNextSiblingNodeByTagName(pXML->GetXML(), "ModelFile"));
							gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
						}
					} while(gDLL->getXMLIFace()->LocateNextSiblingNodeByTagName(pXML->GetXML(), "FeatureArtPiece"));
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
				gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
			}
			//feature art pieces
			if(gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"FeatureDummyNodes"))
			{
				if(gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"FeatureDummyNode"))
				{
					do
					{
						CvString tagName;
						pXML->GetChildXmlValByName(tagName, "Tag");
						CvString nodeName;
						pXML->GetChildXmlValByName(nodeName, "Name");
						featureVariety.createFeatureDummyNode(tagName, nodeName);
					} while(gDLL->getXMLIFace()->LocateNextSiblingNodeByTagName(pXML->GetXML(), "FeatureDummyNode"));
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
				gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
			}
			//variety button
			pXML->GetChildXmlValByName(featureVariety.m_szVarietyButton, "VarietyButton");
		} while(gDLL->getXMLIFace()->LocateNextSiblingNodeByTagName(pXML->GetXML(), "FeatureVariety"));
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	return true;
}

const CvArtInfoFeature::FeatureVariety &CvArtInfoFeature::getVariety(int index) const
{
	FAssertBounds(0, m_aFeatureVarieties.size(), index);
	return m_aFeatureVarieties[index];
}

int CvArtInfoFeature::getNumVarieties() const
{
	return m_aFeatureVarieties.size();
}

std::string CvArtInfoFeature::getFeatureDummyNodeName(int variety, std::string tagName)
{
	return getVariety(variety).getFeatureDummyNodeName(tagName);
}

int CvArtInfoFeature::getConnectionMaskFromString(const CvString &connectionString)
{
	if(connectionString.IsEmpty())
		return 0;
	else
	{
		std::vector<CvString> tokens;
		connectionString.getTokens(" \t\n", tokens);

		int connectionMask = 0;
		for(int i = 0; i < (int)tokens.size(); i++)
		{
			// found a token, parse it.
			CvString &token = tokens[i];
			if(token.CompareNoCase("NW") == 0)
				connectionMask |= DIRECTION_NORTHWEST_MASK;
			else if(token.CompareNoCase("N") == 0)
				connectionMask |= DIRECTION_NORTH_MASK;
			else if(token.CompareNoCase("NE") == 0)
				connectionMask |= DIRECTION_NORTHEAST_MASK;
			else if(token.CompareNoCase("E") == 0)
				connectionMask |= DIRECTION_EAST_MASK;
			else if(token.CompareNoCase("SE") == 0)
				connectionMask |= DIRECTION_SOUTHEAST_MASK;
			else if(token.CompareNoCase("S") == 0)
				connectionMask |= DIRECTION_SOUTH_MASK;
			else if(token.CompareNoCase("SW") == 0)
				connectionMask |= DIRECTION_SOUTHWEST_MASK;
			else if(token.CompareNoCase("W") == 0)
				connectionMask |= DIRECTION_WEST_MASK;
			else FErrorMsg("[Jason] Invalid connection direction.");
		}

		FAssertMsg(connectionMask > 0, "[Jason] Did not find feature connection mask.");
		return connectionMask;
	}
}

int CvArtInfoFeature::getRotatedConnectionMask(int connectionMask, RotationTypes rotation)
{
	/*if(rotation == ROTATE_NONE)
		connectionMask = connectionMask;
	else*/ if(rotation == ROTATE_90CW)
		connectionMask = connectionMask << 2; //rotate two directions CW
	else if(rotation == ROTATE_180CW)
		connectionMask = connectionMask << 4; //rotate four directions CW
	else if(rotation == ROTATE_270CW)
		connectionMask = connectionMask << 6; //rotate six directions CW

	//renormalize directions that wrapped around
	connectionMask = connectionMask | (connectionMask >> 8);
	connectionMask = connectionMask & 255;
	return connectionMask;
}
