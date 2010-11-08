#pragma once

#ifndef CvDLLEngineIFaceBase_h
#define CvDLLEngineIFaceBase_h

//#include "CvEnums.h"
//#include "CvStructs.h"

//
// abstract interface for CvEngine functions used by DLL
//
class CvEngine;
class CvDLLEngineIFaceBase
{
public:
	virtual void cameraLookAt(NiPoint3 lookingPoint) = 0;
	virtual bool isCameraLocked() = 0;

	virtual void SetObeyEntityVisibleFlags(bool bObeyHide) = 0;
	virtual void AutoSave(bool bInitial = false) = 0;
	virtual void SaveReplay(PlayerTypes ePlayer = NO_PLAYER) = 0;
	virtual void SaveGame(CvString& szFilename, SaveGameTypes eType = SAVEGAME_NORMAL) = 0;
	virtual void DoTurn() = 0;
	virtual void ClearMinimap()	 = 0;
	virtual byte GetLandscapePlotTerrainData(uint uiX, uint uiY, uint uiPointX, uint uiPointY) = 0;
	virtual byte GetLandscapePlotHeightData(uint uiX, uint uiY, uint uiPointX, uint uiPointY) = 0;
	virtual LoadType getLoadType() = 0;
	virtual void ClampToWorldCoords(NiPoint3* pPt3, float fOffset = 0.0f) = 0;
	virtual void SetCameraZoom(float zoom) = 0;
	virtual float GetUpdateRate() = 0;
	virtual bool SetUpdateRate( float fUpdateRate ) = 0;
	virtual void toggleGlobeview() = 0;
	virtual bool isGlobeviewUp() = 0;
	virtual void toggleResourceLayer() = 0;
	virtual void toggleUnitLayer() = 0;
	virtual void setResourceLayer(bool bOn) = 0;

	virtual void MoveBaseTurnRight(float increment = 45) = 0;
	virtual void MoveBaseTurnLeft(float increment = 45) = 0;
	virtual void SetFlying(bool value) = 0;
	virtual void CycleFlyingMode(int displacement) = 0;
	virtual void SetMouseFlying(bool value) = 0;
	virtual void SetSatelliteMode(bool value) = 0;
	virtual void SetOrthoCamera(bool value) = 0;
	virtual bool GetFlying() = 0;
	virtual bool GetMouseFlying() = 0;
	virtual bool GetSatelliteMode() = 0;
	virtual bool GetOrthoCamera() = 0;

	// landscape
	virtual int InitGraphics() = 0;
	virtual void GetLandscapeDimensions(float &fWidth, float &fHeight) = 0;
	virtual void GetLandscapeGameDimensions(float &fWidth, float &fHeight) = 0;
	virtual uint GetGameCellSizeX() = 0;
	virtual uint GetGameCellSizeY() = 0;
	virtual float GetPointZSpacing() = 0;
	virtual float GetPointXYSpacing() = 0;
	virtual float GetPointXSpacing() = 0;
	virtual float GetPointYSpacing() = 0;
	virtual float GetHeightmapZ(const NiPoint3 &pt3, bool bClampAboveWater = true) = 0;						
	virtual void LightenVisibility(uint) = 0;
	virtual void DarkenVisibility(uint) = 0;
	virtual void BlackenVisibility(uint) = 0;
	virtual void RebuildAllPlots() = 0;
	virtual void RebuildPlot(int plotX, int plotY, bool bRebuildHeights, bool bRebuildTextures) = 0;
	virtual void RebuildRiverPlotTile(int plotX, int plotY, bool bRebuildHeights, bool bRebuildTextures) = 0;
	virtual void RebuildTileArt(int plotX, int plotY) = 0;
	virtual void ForceTreeOffsets(int plotX, int plotY) = 0;
	
	virtual bool GetGridMode() = 0;
	virtual void SetGridMode(bool bVal) = 0;

	virtual void addColoredPlot(int plotX, int plotY, const NiColorA &color, PlotStyles plotStyle, PlotLandscapeLayers layer) = 0;
	virtual void clearColoredPlots(PlotLandscapeLayers layer) = 0;
	virtual void fillAreaBorderPlot(int plotX, int plotY, const NiColorA &color, AreaBorderLayers layer) = 0;
	virtual void clearAreaBorderPlots(AreaBorderLayers layer) = 0;
	virtual void updateFoundingBorder() = 0;
	virtual void addLandmark(CvPlot *plot, const wchar *caption) = 0; 

	virtual void TriggerEffect(int iEffect, NiPoint3 pt3Point, float rotation = 0.0f) = 0;
	virtual void printProfileText() = 0;

	virtual void clearSigns() = 0;
	virtual CvPlot* pickPlot(int x, int y, NiPoint3& worldPoint) = 0;

	// dirty bits
	virtual void SetDirty(EngineDirtyBits eBit, bool bNewValue) = 0;
	virtual bool IsDirty(EngineDirtyBits eBit) = 0;
	virtual void PushFogOfWar(FogOfWarModeTypes eNewMode) = 0;
	virtual FogOfWarModeTypes PopFogOfWar() = 0;
	virtual void setFogOfWarFromStack() = 0;
	virtual void MarkBridgesDirty() = 0;
	virtual void AddLaunch(PlayerTypes playerType) = 0;
	virtual void AddGreatWall(CvCity *city) = 0;
	virtual void RemoveGreatWall(CvCity *city) = 0;
	virtual void MarkPlotTextureAsDirty(int plotX, int plotY) = 0;
};

#endif	// CvDLLEngineIFaceBase_h
