// Python wrapper class for CvMap

#include "CvGameCoreDLL.h"
#include "CyMap.h"
#include "CvMap.h"
#include "CySelectionGroup.h"
#include "CyArea.h"
#include "CvMapGenerator.h"
#include "CvGame.h" // advc.savem
#include "CvReplayInfo.h" // advc.savem


void CyMap::erasePlots()
{
	m_kMap.erasePlots();
}

void CyMap::setRevealedPlots(int /*TeamTypes*/ eTeam, bool bNewValue, bool bTerrainOnly)
{
	m_kMap.setRevealedPlots((TeamTypes) eTeam, bNewValue, bTerrainOnly);
}

void CyMap::setAllPlotTypes(int /*PlotTypes*/ ePlotType)
{
	m_kMap.setAllPlotTypes((PlotTypes) ePlotType);
}

void CyMap::updateVisibility()
{
	m_kMap.updateVisibility();
}

CyPlot* CyMap::syncRandPlot(int iFlags, int iArea, int iMinUnitDistance, int iTimeout)
{
	// advc: No longer takes an area id
	CvArea* pArea = m_kMap.getArea(iArea);
	return new CyPlot(m_kMap.syncRandPlot(/* advc.enum: */(RandPlotFlags)iFlags,
			pArea, iMinUnitDistance, iTimeout));
}

CyCity* CyMap::findCity(int iX, int iY, int /*PlayerTypes*/ eOwner, int /*TeamTypes*/ eTeam, bool bSameArea, bool bCoastalOnly,
	int /*TeamTypes*/ eTeamAtWarWith, int /*DirectionTypes*/ eDirection, CyCity* pSkipCity)
{
	return new CyCity(m_kMap.findCity(iX, iY, (PlayerTypes)eOwner, (TeamTypes)eTeam, bSameArea, bCoastalOnly,
			((TeamTypes)eTeamAtWarWith), (DirectionTypes)eDirection, pSkipCity->getCity()));
}

CySelectionGroup* CyMap::findSelectionGroup(int iX, int iY, int /*PlayerTypes*/ eOwner, bool bReadyToSelect, bool bWorkers)
{
	return new CySelectionGroup(m_kMap.findSelectionGroup(iX, iY, (PlayerTypes)eOwner, bReadyToSelect, bWorkers));
}

CyArea* CyMap::findBiggestArea(bool bWater)
{
	return new CyArea(m_kMap.findBiggestArea(bWater));
}

int CyMap::getMapFractalFlags()
{
	return m_kMap.getMapFractalFlags();
}

bool CyMap::findWater(CyPlot* pPlot, int iRange, bool bFreshWater)
{
	return m_kMap.findWater(pPlot->getPlot(), iRange, bFreshWater);
}

bool CyMap::isPlot(int iX, int iY)
{
	return m_kMap.isPlot(iX, iY);
}

int CyMap::numPlots()
{
	return m_kMap.numPlots();
}

int CyMap::plotNum(int iX, int iY)
{
	return m_kMap.plotNum(iX, iY);
}

int CyMap::plotX(int iIndex)
{
	// advc: Cut from deleted CvMap::plotX
	return iIndex % m_kMap.getGridWidth();
}

int CyMap::plotY(int iIndex)
{
	// advc: Cut from deleted CvMap::plotY
	return iIndex / m_kMap.getGridWidth();
}

int CyMap::getGridWidth()
{
	return m_kMap.getGridWidth();
}

int CyMap::getGridHeight()
{
	return m_kMap.getGridHeight();
}

int CyMap::getLandPlots()
{
	return m_kMap.getLandPlots();
}

int CyMap::getOwnedPlots()
{
	return m_kMap.getOwnedPlots();
}

int CyMap::getTopLatitude()
{
	return m_kMap.getTopLatitude();
}

int CyMap::getBottomLatitude()
{
	return m_kMap.getBottomLatitude();
}

int CyMap::getNextRiverID()
{
	return m_kMap.getNextRiverID();
}

void CyMap::incrementNextRiverID()
{
	m_kMap.incrementNextRiverID();
}

bool CyMap::isWrapX()
{
	return m_kMap.isWrapX();
}

bool CyMap::isWrapY()
{
	return m_kMap.isWrapY();
}

std::wstring CyMap::getMapScriptName()
{
	return GC.getInitCore().getMapScriptName().GetCString();
}

WorldSizeTypes CyMap::getWorldSize()
{
	return m_kMap.getWorldSize();
}

ClimateTypes CyMap::getClimate()
{
	return m_kMap.getClimate();
}

SeaLevelTypes CyMap::getSeaLevel()
{
	return m_kMap.getSeaLevel();
}

int CyMap::getNumCustomMapOptions()
{
	return m_kMap.getNumCustomMapOptions();
}

CustomMapOptionTypes CyMap::getCustomMapOption(int iOption)
{
	return m_kMap.getCustomMapOption(iOption);
}
// advc.190b:
std::wstring CyMap::getNonDefaultCustomMapOptionDesc(int iOption)
{
	return m_kMap.getNonDefaultCustomMapOptionDesc(iOption);
}
// advc.savem:
std::wstring CyMap::getSettingsString()
{
	PlayerTypes const eActivePlayer = GC.getGame().getActivePlayer();
	if (eActivePlayer == NO_PLAYER)
		return L"";
	CvReplayInfo tmpReplay;
	tmpReplay.createInfo(eActivePlayer);
	CvWString szSettings;
	tmpReplay.appendSettingsMsg(szSettings, eActivePlayer);
	return szSettings; // by value
}
int CyMap::getNumBonuses(int /* BonusTypes */ eIndex)
{
	return m_kMap.getNumBonuses((BonusTypes)eIndex);
}

int CyMap::getNumBonusesOnLand(int /* BonusTypes */ eIndex)
{
	return m_kMap.getNumBonusesOnLand((BonusTypes)eIndex);
}

CyPlot* CyMap::plotByIndex(int iIndex)
{
	return new CyPlot(m_kMap.plotByIndex(iIndex));
}

CyPlot* CyMap::sPlotByIndex(int iIndex) // static version
{
	static CyPlot plot;
	plot.setPlot(m_kMap.plotByIndex(iIndex));
	return &plot;
}

// doc
int CyMap::plotIndex(int iX, int iY)
{
    return m_kMap.plotIndex(iX, iY);
}

CyPlot* CyMap::plot(int iX, int iY)
{
	return new CyPlot(m_kMap.plot(iX, iY));
}

CyPlot* CyMap::sPlot(int iX, int iY) // static version
{
	static CyPlot p;
	p.setPlot(m_kMap.plot(iX, iY));
	return &p;
}

CyPlot* CyMap::pointToPlot(float fX, float fY)
{
	return new CyPlot(m_kMap.pointToPlot(fX, fY));
}

int CyMap::getIndexAfterLastArea()
{
	return m_kMap.getIndexAfterLastArea();
}

int CyMap::getNumAreas()
{
	return m_kMap.getNumAreas();
}

int CyMap::getNumLandAreas()
{
	return m_kMap.getNumLandAreas();
}

CyArea* CyMap::getArea(int iID)
{
	return new CyArea(m_kMap.getArea(iID));
}

void CyMap::recalculateAreas()
{
	m_kMap.recalculateAreas();
}

void CyMap::resetPathDistance()
{
	m_kMap.resetPathDistance();
}

int CyMap::calculatePathDistance(CyPlot* pSource, CyPlot* pDest)
{
	return m_kMap.calculatePathDistance(pSource->getPlot(), pDest->getPlot());
}

void CyMap::rebuild(int iGridW, int iGridH, int iPrimeMeridian, int iEquator, int iTopLatitude, int iBottomLatitude, bool bWrapX, bool bWrapY, WorldSizeTypes eWorldSize, ClimateTypes eClimate, SeaLevelTypes eSeaLevel, int iNumCustomMapOptions, CustomMapOptionTypes * aeCustomMapOptions)
{
	m_kMap.rebuild(iGridW, iGridH, iPrimeMeridian, iEquator, iTopLatitude, iBottomLatitude, bWrapX, bWrapY, eWorldSize, eClimate, eSeaLevel, iNumCustomMapOptions, aeCustomMapOptions);
}

void CyMap::regenerateGameElements()
{
	CvMapGenerator* pMapGen = &CvMapGenerator::GetInstance();
	pMapGen->eraseRivers();
	pMapGen->eraseFeatures();
	pMapGen->eraseBonuses();
	pMapGen->eraseGoodies();
	pMapGen->addGameElements();
}

void CyMap::updateFog()
{
	m_kMap.updateFog();
}

void CyMap::updateMinimapColor()
{
	m_kMap.updateMinimapColor();
}

void CyMap::updateMinOriginalStartDist(CyArea* pArea)
{
	m_kMap.updateMinOriginalStartDist(pArea->getArea());
}

// <advc.enum> Moved from CyGame
int CyMap::getPlotExtraYield(int iX, int iY, int /*YieldTypes*/ eYield) // K-Mod
{
	CvPlot const* pPlot = m_kMap.plot(iX, iY);
	if (pPlot == NULL)
		return 0;
	return m_kMap.getPlotExtraYield(*pPlot, (YieldTypes)eYield);
}

void CyMap::setPlotExtraYield(int iX, int iY, int /*YieldTypes*/ eYield, int iExtraYield)
{
	CvPlot* pPlot = m_kMap.plot(iX, iY);
	if (pPlot == NULL)
		return;
	m_kMap.setPlotExtraYield(*pPlot, (YieldTypes)eYield, iExtraYield);
}

void CyMap::changePlotExtraCost(int iX, int iY, int iCost)
{
	CvPlot* pPlot = m_kMap.plot(iX, iY);
	if (pPlot == NULL)
		return;
	m_kMap.changePlotExtraCost(*pPlot, iCost);
} // </advc.enum>

// <advc.002a>
void CyMap::setMinimapShowUnits(bool b)
{
	m_kMap.getMinimapSettings().setShowUnits(b);
}

void CyMap::setMinimapWaterAlpha(float f)
{
	m_kMap.getMinimapSettings().setWaterAlpha(f);
}

void CyMap::setMinimapLandAlpha(float f)
{
	m_kMap.getMinimapSettings().setLandAlpha(f);
}

bool CyMap::isMinimapShowUnits()
{
	return m_kMap.getMinimapSettings().isShowUnits();
}

float CyMap::getMinimapWaterAlpha()
{
	return m_kMap.getMinimapSettings().getWaterAlpha();
}

float CyMap::getMinimapLandAlpha()
{
	return m_kMap.getMinimapSettings().getLandAlpha();
} // </advc.002a>

// doc
int CyMap::getPrimeMeridian()
{
    return m_kMap.getPrimeMeridian();
}

// doc
int CyMap::getEquator()
{
    return m_kMap.getEquator();
}

// doc
void CyMap::updateCulture()
{
    m_kMap.updateCulture();
}

// doc
int CyMap::maxStepDistance()
{
    return m_kMap.maxStepDistance();
}

// doc
int CyMap::maxPlotDistance()
{
    return m_kMap.maxPlotDistance();
}

// doc
int CyMap::getScenario()
{
    return m_kMap.getScenario();
}