#pragma once

//  $Header:
//------------------------------------------------------------------------------------------------
//  FILE:    CvInfosWater.h
//  AUTHOR:	tomw
//  PURPOSE: All Civ4 info classes and the base class for them
//------------------------------------------------------------------------------------------------
//  Copyright (c) 2003 Firaxis Games, Inc. All rights reserved.
//------------------------------------------------------------------------------------------------
/*  advc.003x: I've left this file alone apart from some style changes
	and an underscore added to the file name for consistency with the names of
	the header files that I've added.
	I'm including this header in CvInfo_Misc.h b/c there's no need to include
	CvInfo_Water.h in any implementation file separately. */

#ifndef CV_WATERINFO_H
#define CV_WATERINFO_H

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvWaterPlaneInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvWaterPlaneInfo :public CvInfoBase
{
public:
	CvWaterPlaneInfo();

	NiColor	getMaterialDiffuse() const;	// The water plane's material diffuse color
	NiColor	getMaterialSpecular() const; // The water plane's material specular color
	NiColor	getMaterialEmmisive() const; // The water plane's material emmisive color
	DllExport float getMaterialAlpha() const; // The water plane's material alpha

	DllExport float getTextureScaling() const; // The water plane's texture scale
	DllExport float getTextureScrollRateU() const; // The water plane's texture scroll rate in U
	DllExport float getTextureScrollRateV() const; // The water plane's texture scroll rate in V

	DllExport const TCHAR* getBaseTexture() const; // The filename of the base texture
	DllExport const TCHAR* getTransitionTexture() const; // The transition texture for fading ocean into land

	bool read(CvXMLLoadUtility*);

protected:

	NiColor	m_kMaterialDiffuse;
	NiColor	m_kMaterialSpecular;
	NiColor	m_kMaterialEmmisive;
	float m_fMaterialAlpha;

	CvString m_szBaseTexture;
	CvString m_szTransitionTexture;

	float m_BaseTextureScale; // Texture scaling
	float m_fURate; // Texture scroll rate
	float m_fVRate;
};


//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvTerrainPlaneInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvTerrainPlaneInfo :public CvInfoBase
{
public:
	CvTerrainPlaneInfo();

	DllExport bool isVisible() const; // The terrain plane's material alpha
	DllExport bool isGroundPlane() const; // The terrain plane's material alpha
	DllExport float getMaterialAlpha() const; // The terrain plane's material alpha
	DllExport float getCloseAlpha() const; // The terrain plane's material alpha

	DllExport float getTextureScalingU() const;	// The terrain plane's texture scale
	DllExport float getTextureScalingV() const;	 // The terrain plane's texture scale
	DllExport float getTextureScrollRateU() const; // The terrain plane's texture scroll rate in U
	DllExport float getTextureScrollRateV() const; // The terrain plane's texture scroll rate in V
	DllExport float getZHeight() const; // The terrain plane's z height in world units
	DllExport FogTypes getFogType() const;

	DllExport const TCHAR * getBaseTexture() const; // The filename of the base texture

	bool read(CvXMLLoadUtility*);

protected:

	bool m_bVisible;
	bool m_bGroundPlane;
	float m_fMaterialAlpha;
	float m_fCloseAlpha;

	CvString m_szBaseTexture;

	float m_BaseTextureScaleU;
	float m_BaseTextureScaleV;
	float m_fURate;
	float m_fVRate;
	float m_fZHeight;
	FogTypes m_eFogType;
};


//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvTerrainPlaneInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvCameraOverlayInfo :public CvInfoBase
{
public:
	CvCameraOverlayInfo();

	DllExport bool isVisible() const; // The terrain plane's material alpha
	DllExport CameraOverlayTypes getCameraOverlayType() const;

	DllExport const TCHAR * getBaseTexture() const; // The filename of the base texture

	bool read(CvXMLLoadUtility*);

protected:
	bool m_bVisible;
	CvString m_szBaseTexture;
	CameraOverlayTypes m_eCameraOverlayType;
};

#endif
