#pragma once

#ifndef CyMap_h
#define CyMap_h

//#include "CvEnums.h"
//
// Python wrapper class for CvMap 
// SINGLETON
//

class CyPlot;
class CvMap;
class CyCity;
class CySelectionGroup;
class CyUnit;
class CyArea;
class CyMap
{
public:
	DllExport CyMap();
	CyMap(CvMap* pMap);		// Call from C++
	CvMap* getMap() { return m_pMap;	}	// Call from C++
	bool isNone() { return (m_pMap==NULL); }
	
	void erasePlots();
	void setRevealedPlots(int /*TeamTypes*/ eTeam, bool bNewValue, bool bTerrainOnly);
	void setAllPlotTypes(int /*PlotTypes*/ ePlotType);

	void updateVisibility();
	CyPlot* syncRandPlot(int iFlags, int iArea, int iMinUnitDistance, int iTimeout);

	CyCity* findCity(int iX, int iY, int /*PlayerTypes*/ eOwner, int /*TeamTypes*/ eTeam, bool bSameArea, bool bCoastalOnly, int /*TeamTypes*/ eTeamAtWarWith, int /*DirectionTypes*/ eDirection, CyCity* pSkipCity);
	CySelectionGroup* findSelectionGroup(int iX, int iY, int /*PlayerTypes*/ eOwner, bool bReadyToSelect, bool bWorkers);

	CyArea* findBiggestArea(bool bWater);

	int getMapFractalFlags();
	bool findWater(CyPlot* pPlot, int iRange, bool bFreshWater);
	bool isPlot(int iX, int iY);
	int numPlots();
	int plotNum(int iX, int iY);
	int plotX(int iIndex);
	int plotY(int iIndex);
	int getGridWidth();
	int getGridHeight();

	int getLandPlots();
	int getOwnedPlots();

	int getTopLatitude();
	int getBottomLatitude();

	int getNextRiverID();
	void incrementNextRiverID();

	bool isWrapX();
	bool isWrapY();
	std::wstring getMapScriptName();
	WorldSizeTypes getWorldSize();
	ClimateTypes getClimate();
	SeaLevelTypes getSeaLevel();
	int getNumCustomMapOptions();
	CustomMapOptionTypes getCustomMapOption(int iOption);
	int getNumBonuses(int /* BonusTypes */ eIndex);
	int getNumBonusesOnLand(int /* BonusTypes */ eIndex);

	CyPlot* plotByIndex(int iIndex);
	CyPlot* sPlotByIndex(int iIndex);
	CyPlot* plot(int iX, int iY);
	CyPlot* sPlot(int iX, int iY) ;
	CyPlot* pointToPlot(float fX, float fY);
	int getIndexAfterLastArea();
	int getNumAreas();
	int getNumLandAreas();
	CyArea* getArea(int iID);
	void recalculateAreas();
	void resetPathDistance();

	int calculatePathDistance(CyPlot* pSource, CyPlot* pDest);
	void rebuild(int iGridW, int iGridH, int iTopLatitude, int iBottomLatitude, bool bWrapX, bool bWrapY, WorldSizeTypes eWorldSize, ClimateTypes eClimate, SeaLevelTypes eSeaLevel, int iNumCustomMapOptions, CustomMapOptionTypes * aeCustomMapOptions);
	void regenerateGameElements();
	void updateFog();
	void updateMinimapColor();
	void updateMinOriginalStartDist(CyArea* pArea);

	// PYTHON HELPER FUNCTIONS
	//int getNumPlayerOwnedPlots(int /*PlayerTypes*/ iPlayer);

protected:
	CvMap* m_pMap;
};

#endif	// CyMap_h
