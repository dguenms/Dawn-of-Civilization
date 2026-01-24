//  $Header:
//------------------------------------------------------------------------------------------------
//  FILE:    CvInfoWater.cpp
//  PURPOSE: The base class for all info classes to inherit from.
//------------------------------------------------------------------------------------------------
//  Copyright (c) 2003 Firaxis Games, Inc. All rights reserved.
//------------------------------------------------------------------------------------------------

// advc.003x: Some minor stlyle changes throughout this file

#include "CvGameCoreDLL.h"
#include "CvInfo_Water.h"
#include "CvXMLLoadUtility.h"

CvWaterPlaneInfo::CvWaterPlaneInfo()
// <kmodx>
: m_fMaterialAlpha(0.0f),
  m_BaseTextureScale(0.0f),
  m_fURate(0.0f),
  m_fVRate(0.0f) // </kmodx>
{}

float CvWaterPlaneInfo::getMaterialAlpha() const
{
	return m_fMaterialAlpha;
}

NiColor	CvWaterPlaneInfo::getMaterialDiffuse() const
{
	return m_kMaterialDiffuse;
}

NiColor	CvWaterPlaneInfo::getMaterialSpecular() const
{
	return m_kMaterialSpecular;
}

NiColor	CvWaterPlaneInfo::getMaterialEmmisive() const
{
	return m_kMaterialEmmisive;
}

const TCHAR * CvWaterPlaneInfo::getBaseTexture() const
{
	return m_szBaseTexture;
}

const TCHAR * CvWaterPlaneInfo::getTransitionTexture() const
{
	return m_szTransitionTexture;
}

float CvWaterPlaneInfo::getTextureScaling() const
{
	return m_BaseTextureScale;
}

float CvWaterPlaneInfo::getTextureScrollRateU() const
{
	return m_fURate;
}

float CvWaterPlaneInfo::getTextureScrollRateV() const
{
	return m_fVRate;
}

bool CvWaterPlaneInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
		return false;

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "WaterMaterial"))
	{
		if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "MaterialColors"))
		{
			if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "DiffuseMaterialColor"))
			{
				pXML->GetChildXmlValByName( &m_kMaterialDiffuse.r, "r");
				pXML->GetChildXmlValByName( &m_kMaterialDiffuse.g, "g");
				pXML->GetChildXmlValByName( &m_kMaterialDiffuse.b, "b");
				gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
			}
			if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "SpecularMaterialColor"))
			{
				pXML->GetChildXmlValByName( &m_kMaterialSpecular.r, "r");
				pXML->GetChildXmlValByName( &m_kMaterialSpecular.g, "g");
				pXML->GetChildXmlValByName( &m_kMaterialSpecular.b, "b");
				gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
			}
			if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "EmmisiveMaterialColor"))
			{
				pXML->GetChildXmlValByName( &m_kMaterialEmmisive.r, "r");
				pXML->GetChildXmlValByName( &m_kMaterialEmmisive.g, "g");
				pXML->GetChildXmlValByName( &m_kMaterialEmmisive.b, "b");
				gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
			}
			gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
		}

		pXML->GetChildXmlValByName( &m_fMaterialAlpha, "MaterialAlpha");

		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "WaterTextures"))
	{
		if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "WaterBaseTexture"))
		{
			pXML->GetChildXmlValByName(m_szBaseTexture, "TextureFile");

			pXML->GetChildXmlValByName( &m_BaseTextureScale, "TextureScaling");
			pXML->GetChildXmlValByName( &m_fURate, "URate");
			pXML->GetChildXmlValByName( &m_fVRate, "VRate");

			gDLL->getXMLIFace()->SetToParent(pXML->GetXML());

		}
		if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "WaterTransitionTexture"))
		{
			pXML->GetChildXmlValByName(m_szTransitionTexture, "TextureFile");
		}

		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	return true;
}

CvTerrainPlaneInfo::CvTerrainPlaneInfo()
// <kmodx>
: m_bVisible(false),
  m_bGroundPlane(false),
  m_fMaterialAlpha(0.0f),
  m_fCloseAlpha(0.0f),
  m_BaseTextureScaleU(0.0f),
  m_BaseTextureScaleV(0.0f),
  m_fURate(0.0f),
  m_fVRate(0.0f),
  m_fZHeight(0.0f),
  m_eFogType(FOG_TYPE_NONE)
// </kmodx>
{}

bool CvTerrainPlaneInfo::isVisible() const
{
	return m_bVisible;
}

bool CvTerrainPlaneInfo::isGroundPlane() const
{
	return m_bGroundPlane;
}

float CvTerrainPlaneInfo::getMaterialAlpha() const
{
	return m_fMaterialAlpha;
}

float CvTerrainPlaneInfo::getCloseAlpha() const
{
	return m_fCloseAlpha;
}

const TCHAR * CvTerrainPlaneInfo::getBaseTexture() const
{
	return m_szBaseTexture;
}

float CvTerrainPlaneInfo::getTextureScalingU() const
{
	return m_BaseTextureScaleU;
}

float CvTerrainPlaneInfo::getTextureScalingV() const
{
	return m_BaseTextureScaleV;
}

float CvTerrainPlaneInfo::getTextureScrollRateU() const
{
	return m_fURate;
}

float CvTerrainPlaneInfo::getTextureScrollRateV() const
{
	return m_fVRate;
}

float CvTerrainPlaneInfo::getZHeight() const
{
	return m_fZHeight;
}

FogTypes CvTerrainPlaneInfo::getFogType() const
{
	return m_eFogType;
}

bool CvTerrainPlaneInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
		return false;

	pXML->GetChildXmlValByName( &m_bVisible, "bVisible");
	pXML->GetChildXmlValByName( &m_bGroundPlane, "bGroundPlane");
	pXML->GetChildXmlValByName( &m_fMaterialAlpha, "MaterialAlpha");
	pXML->GetChildXmlValByName( &m_fCloseAlpha, "CloseAlpha");

	pXML->GetChildXmlValByName(m_szBaseTexture, "TextureFile");

	pXML->GetChildXmlValByName( &m_BaseTextureScaleU, "TextureScalingU");
	pXML->GetChildXmlValByName( &m_BaseTextureScaleV, "TextureScalingV");
	pXML->GetChildXmlValByName( &m_fURate, "URate");
	pXML->GetChildXmlValByName( &m_fVRate, "VRate");
	pXML->GetChildXmlValByName( &m_fZHeight, "ZHeight");

	CvString szTextVal;
	pXML->GetChildXmlValByName( szTextVal, "FogType");
	if(szTextVal.CompareNoCase("FOG_TYPE_NONE") == 0)
		m_eFogType = FOG_TYPE_NONE;
	else if(szTextVal.CompareNoCase("FOG_TYPE_PARALLEL") == 0)
		m_eFogType = FOG_TYPE_PARALLEL;
	else if(szTextVal.CompareNoCase("FOG_TYPE_PROJECTED") == 0)
		m_eFogType = FOG_TYPE_PROJECTED;
	else
	{
		FErrorMsg("[Jason] Unknown fog type.");
		m_eFogType = FOG_TYPE_NONE;
	}

	return true;
}


CvCameraOverlayInfo::CvCameraOverlayInfo()
: m_bVisible(false), m_eCameraOverlayType(CAMERA_OVERLAY_DECAL) // kmodx
{}

bool CvCameraOverlayInfo::isVisible() const
{
	return m_bVisible;
}

const TCHAR * CvCameraOverlayInfo::getBaseTexture() const
{
	return m_szBaseTexture;
}

CameraOverlayTypes CvCameraOverlayInfo::getCameraOverlayType() const
{
	return m_eCameraOverlayType;
}

bool CvCameraOverlayInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
		return false;

	pXML->GetChildXmlValByName(&m_bVisible, "bVisible");
	pXML->GetChildXmlValByName(m_szBaseTexture, "TextureFile");

	CvString szTextVal;
	pXML->GetChildXmlValByName(szTextVal, "CameraOverlayType");
	if(szTextVal.CompareNoCase("CAMERA_OVERLAY_DECAL") == 0)
		m_eCameraOverlayType = CAMERA_OVERLAY_DECAL;
	else if(szTextVal.CompareNoCase("CAMERA_OVERLAY_ADDITIVE") == 0)
		m_eCameraOverlayType = CAMERA_OVERLAY_ADDITIVE;
	else
	{
		FErrorMsg("[Jason] Unknown camera overlay type.");
		m_eCameraOverlayType = CAMERA_OVERLAY_DECAL;
	}

	return true;
}
