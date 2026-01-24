//
// Python wrapper class for CvPlot 
// 
//
#include "CvGameCoreDLL.h"
#include "CyPlot.h"
#include "CyCity.h"
#include "CyArea.h"
#include "CyUnit.h"
#include "CvPlot.h"

CyPlot::CyPlot(CvPlot* pPlot) : m_pPlot(pPlot)
{

}

CyPlot::CyPlot() : m_pPlot(NULL)
{

}

void CyPlot::erase()
{
	if (m_pPlot)
		m_pPlot->erase();
}

NiPoint3 CyPlot::getPoint()
{
	return m_pPlot ? m_pPlot->getPoint() : NiPoint3(0,0,0);
}

int CyPlot::getTeam()
{
	return m_pPlot ? m_pPlot->getTeam() : -1;
}

void CyPlot::nukeExplosion(int iRange, CyUnit* pNukeUnit)
{
	if (m_pPlot)
		m_pPlot->nukeExplosion(iRange, pNukeUnit->getUnit());
}

bool CyPlot::isConnectedTo(CyCity* pCity)
{
	return m_pPlot ? m_pPlot->isConnectedTo(pCity->getCity()) : false;
}

bool CyPlot::isConnectedToCapital(int /*PlayerTypes*/ ePlayer)
{
	return m_pPlot ? m_pPlot->isConnectedToCapital((PlayerTypes) ePlayer): false;
}

int CyPlot::getPlotGroupConnectedBonus(int /*PlayerTypes*/ ePlayer, int /*BonusTypes*/ eBonus)
{
	return m_pPlot ? m_pPlot->getPlotGroupConnectedBonus((PlayerTypes) ePlayer, (BonusTypes) eBonus) : -1;
}

bool CyPlot::isPlotGroupConnectedBonus(int /*PlayerTypes*/ ePlayer, int /*BonusTypes*/ eBonus)
{
	return m_pPlot ? m_pPlot->isPlotGroupConnectedBonus((PlayerTypes) ePlayer, (BonusTypes) eBonus) : false;
}

bool CyPlot::isAdjacentPlotGroupConnectedBonus(int /*PlayerTypes*/ ePlayer, int /*BonusTypes*/ eBonus)
{
	return m_pPlot ? m_pPlot->isAdjacentPlotGroupConnectedBonus((PlayerTypes) ePlayer, (BonusTypes) eBonus) : false;
}

void CyPlot::updateVisibility()
{
	if (m_pPlot)
	{
		m_pPlot->updateVisibility();
	}
}

bool CyPlot::isAdjacentToArea(CyArea* pArea)
{
	return m_pPlot ? m_pPlot->isAdjacentToArea(pArea->getArea()) : false;
}

bool CyPlot::shareAdjacentArea(CyPlot* pPlot)
{
	return m_pPlot ? m_pPlot->shareAdjacentArea(pPlot->getPlot()) : false;
}

bool CyPlot::isAdjacentToLand()
{
	return m_pPlot ? m_pPlot->isAdjacentToLand() : false;
}

bool CyPlot::isCoastalLand()
{
	return m_pPlot ? m_pPlot->isCoastalLand() : false;
}

bool CyPlot::isWithinTeamCityRadius(int /*TeamTypes*/ eTeam, int /*PlayerTypes*/ eIgnorePlayer)
{
	return m_pPlot ? m_pPlot->isWithinTeamCityRadius((TeamTypes) eTeam, (PlayerTypes) eIgnorePlayer) : false;
}
bool CyPlot::isLake()
{
	return m_pPlot ? m_pPlot->isLake() : false;
}

bool CyPlot::isFreshWater()
{
	return m_pPlot ? m_pPlot->isFreshWater() : false;
}

bool CyPlot::isPotentialIrrigation()
{
	return m_pPlot ? m_pPlot->isPotentialIrrigation() : false;
}

bool CyPlot::canHavePotentialIrrigation()
{
	return m_pPlot ? m_pPlot->canHavePotentialIrrigation() : false;
}

bool CyPlot::isIrrigationAvailable(bool bIgnoreSelf)
{
	return m_pPlot ? m_pPlot->isIrrigationAvailable(bIgnoreSelf) : false;
}

bool CyPlot::isRiverSide()
{
	return m_pPlot ? m_pPlot->isRiverSide() : false;
}

bool CyPlot::isRiver()
{
	return m_pPlot ? m_pPlot->isRiver() : false;
}

bool CyPlot::isRiverConnection(int /*DirectionTypes*/ eDirection)
{
	return m_pPlot ? m_pPlot->isRiverConnection((DirectionTypes) eDirection) : false;
}

int CyPlot::getNearestLandArea()
{
	return m_pPlot ? m_pPlot->getNearestLandArea() : -1;
}

CyPlot* CyPlot::getNearestLandPlot()
{
	return m_pPlot ? new CyPlot(m_pPlot->getNearestLandPlot()) : NULL;
}

int CyPlot::seeFromLevel(int /*TeamTypes*/ eTeam)
{
	return m_pPlot ? m_pPlot->seeFromLevel((TeamTypes)eTeam) : -1;
}

int CyPlot::seeThroughLevel()
{
	return m_pPlot ? m_pPlot->seeThroughLevel() : -1;
}

bool CyPlot::canHaveBonus(int /*BonusTypes*/ eBonus, bool bIgnoreLatitude)
{
	return m_pPlot ? m_pPlot->canHaveBonus((BonusTypes)eBonus, bIgnoreLatitude) : false;
}

bool CyPlot::canHaveImprovement(int /* ImprovementTypes */ eImprovement, int /*TeamTypes*/ eTeam, bool bPotential)
{
	return m_pPlot ? m_pPlot->canHaveImprovement(((ImprovementTypes)eImprovement), ((TeamTypes)eTeam), bPotential) : false;
}

bool CyPlot::canBuild(int /*BuildTypes*/ eBuild, int /*PlayerTypes*/ ePlayer, bool bTestVisible)
{
	return m_pPlot ? m_pPlot->canBuild((BuildTypes) eBuild, (PlayerTypes) ePlayer, bTestVisible) : false;
}

int CyPlot::getBuildTime(int /* BuildTypes */ eBuild)
{
	return m_pPlot ? m_pPlot->getBuildTime((BuildTypes)eBuild) : -1;
}

int CyPlot::getBuildTurnsLeft(int /*BuildTypes*/ eBuild, int iNowExtra, int iThenExtra)
{
	return m_pPlot ? m_pPlot->getBuildTurnsLeft((BuildTypes) eBuild, iNowExtra, iThenExtra) : -1;
}

int CyPlot::getFeatureProduction(int /*BuildTypes*/ eBuild, int /*TeamTypes*/ eTeam, CyCity* ppCity)
{
	CvCity* tempCity = ppCity->getCity();
	return m_pPlot ? m_pPlot->getFeatureProduction((BuildTypes) eBuild, (TeamTypes) eTeam, &tempCity) : -1;
}

CyUnit* CyPlot::getBestDefender(int /*PlayerTypes*/ eOwner, int /*PlayerTypes*/ eAttackingPlayer, CyUnit* pAttacker, bool bTestAtWar, bool bTestPotentialEnemy, bool bTestCanMove)
{
	return m_pPlot ? new CyUnit(m_pPlot->getBestDefender((PlayerTypes) eOwner, (PlayerTypes) eAttackingPlayer, pAttacker->getUnit(), bTestAtWar, bTestPotentialEnemy, bTestCanMove)) : NULL;
}	

CyUnit* CyPlot::getSelectedUnit()
{
	return m_pPlot ? new CyUnit(m_pPlot->getSelectedUnit()) : NULL;
}

int CyPlot::getUnitPower(int /* PlayerTypes */ eOwner)
{
	return m_pPlot ? m_pPlot->getUnitPower((PlayerTypes)eOwner) : -1;
}

int CyPlot::movementCost(CyUnit* pUnit, CyPlot* pFromPlot)
{
	return m_pPlot ? m_pPlot->movementCost(pUnit->getUnit(), pFromPlot->getPlot()) : -1;
}

int CyPlot::defenseModifier(int iDefendTeam, bool bIgnoreBuilding, bool bHelp)
{
	return m_pPlot ? m_pPlot->defenseModifier((TeamTypes)iDefendTeam, bIgnoreBuilding, bHelp) : -1;
}

int CyPlot::getExtraMovePathCost()
{
	return m_pPlot ? m_pPlot->getExtraMovePathCost() : -1;
}

void CyPlot::changeExtraMovePathCost(int iChange)
{
	if (m_pPlot)
		m_pPlot->changeExtraMovePathCost(iChange);
}

bool CyPlot::isAdjacentOwned()
{
	return m_pPlot ? m_pPlot->isAdjacentOwned() : false;
}

bool CyPlot::isAdjacentPlayer(int /*PlayerTypes*/ ePlayer, bool bLandOnly)
{
	return m_pPlot ? m_pPlot->isAdjacentPlayer((PlayerTypes)ePlayer, bLandOnly) : false;
}

bool CyPlot::isAdjacentTeam(int /*TeamTypes*/ ePlayer, bool bLandOnly)
{
	return m_pPlot ? m_pPlot->isAdjacentTeam((TeamTypes)ePlayer, bLandOnly) : false;
}

bool CyPlot::isWithinCultureRange(int /*PlayerTypes*/ ePlayer)
{
	return m_pPlot ? m_pPlot->isWithinCultureRange((PlayerTypes)ePlayer) : false;
}

int CyPlot::getNumCultureRangeCities(int /*PlayerTypes*/ ePlayer)
{
	return m_pPlot ? m_pPlot->getNumCultureRangeCities((PlayerTypes)ePlayer) : -1;
}

int /*PlayerTypes*/ CyPlot::calculateCulturalOwner()
{
	return m_pPlot ? m_pPlot->calculateCulturalOwner() : -1;
}

bool CyPlot::isOwned()
{
	return m_pPlot ? m_pPlot->isOwned() : false;
}

bool CyPlot::isBarbarian()
{
	return m_pPlot ? m_pPlot->isBarbarian() : false;
}

bool CyPlot::isRevealedBarbarian()
{
	return m_pPlot ? m_pPlot->isRevealedBarbarian() : false;
}

bool CyPlot::isVisible(int /*TeamTypes*/ eTeam, bool bDebug)
{
	return m_pPlot ? m_pPlot->isVisible((TeamTypes)eTeam, bDebug) : false;
}

bool CyPlot::isActiveVisible(bool bDebug)
{
	return m_pPlot ? m_pPlot->isActiveVisible(bDebug) : false;
}

bool CyPlot::isVisibleToWatchingHuman()
{
	return m_pPlot ? m_pPlot->isVisibleToWatchingHuman() : false;
}

bool CyPlot::isAdjacentVisible(int /*TeamTypes*/ eTeam, bool bDebug)
{
	return m_pPlot ? m_pPlot->isAdjacentVisible((TeamTypes) eTeam, bDebug) : false;
}

bool CyPlot::isAdjacentNonvisible(int /*TeamTypes*/ eTeam)
{
	return m_pPlot ? m_pPlot->isAdjacentNonvisible((TeamTypes) eTeam) : false;
}

bool CyPlot::isAdjacentRevealed(int /*TeamTypes*/ eTeam)
{
	return m_pPlot ? m_pPlot->isAdjacentRevealed((TeamTypes) eTeam) : false;
}

bool CyPlot::isAdjacentNonrevealed(int /*TeamTypes*/ eTeam)
{
	return m_pPlot ? m_pPlot->isAdjacentNonrevealed((TeamTypes) eTeam) : false;
}

void CyPlot::removeGoody()
{
	if (m_pPlot)
	{
		m_pPlot->removeGoody();
	}
}

bool CyPlot::isGoody()
{
	return m_pPlot ? m_pPlot->isGoody() : false;
}

bool CyPlot::isRevealedGoody(int /*TeamTypes*/ eTeam)
{
	return m_pPlot ? m_pPlot->isRevealedGoody((TeamTypes) eTeam) : false;
}

bool CyPlot::isCity()
{
	return m_pPlot ? m_pPlot->isCity() : false;
}

bool CyPlot::isFriendlyCity(CyUnit* pUnit, bool bCheckImprovement)													
{
	return m_pPlot ? m_pPlot->isFriendlyCity(*(pUnit->getUnit()), bCheckImprovement) : false;
}

bool CyPlot::isEnemyCity(CyUnit* pUnit)														
{
	return m_pPlot ? m_pPlot->isEnemyCity(*(pUnit->getUnit())) : false;
}

bool CyPlot::isOccupation()
{
	return m_pPlot ? m_pPlot->isOccupation() : false;
}

bool CyPlot::isBeingWorked()
{
	return m_pPlot ? m_pPlot->isBeingWorked() : false;
}

bool CyPlot::isUnit()
{
	return m_pPlot ? m_pPlot->isUnit() : false;
}

bool CyPlot::isInvestigate(int /*TeamTypes*/ eTeam)
{
	return m_pPlot ? m_pPlot->isInvestigate((TeamTypes) eTeam) : false;
}

bool CyPlot::isVisibleEnemyDefender(CyUnit* pUnit)
{
	return m_pPlot ? m_pPlot->isVisibleEnemyDefender(pUnit->getUnit()) : false;
}

int CyPlot::getNumDefenders(int /*PlayerTypes*/ ePlayer)
{
	return m_pPlot ? m_pPlot->getNumDefenders((PlayerTypes) ePlayer) : -1;
}

int CyPlot::getNumVisibleEnemyDefenders(CyUnit* pUnit)
{
	return m_pPlot ? m_pPlot->getNumVisibleEnemyDefenders(pUnit->getUnit()) : -1;
}

int CyPlot::getNumVisiblePotentialEnemyDefenders(CyUnit* pUnit)
{
	return m_pPlot ? m_pPlot->getNumVisiblePotentialEnemyDefenders(pUnit->getUnit()) : -1;
}

bool CyPlot::isVisibleEnemyUnit(int /*PlayerTypes*/ ePlayer)
{
	return m_pPlot ? m_pPlot->isVisibleEnemyUnit((PlayerTypes) ePlayer) : false;
}

bool CyPlot::isVisibleOtherUnit(int /*PlayerTypes*/ ePlayer)
{
	return m_pPlot ? m_pPlot->isVisibleOtherUnit((PlayerTypes) ePlayer) : false;
}

bool CyPlot::isFighting()
{
	return m_pPlot ? m_pPlot->isFighting() : false;
}

bool CyPlot::canHaveFeature(int /*FeatureTypes*/ eFeature)
{
	return m_pPlot ? m_pPlot->canHaveFeature((FeatureTypes)eFeature) : false;
}

bool CyPlot::isRoute()
{
	return m_pPlot ? m_pPlot->isRoute() : false;
}

bool CyPlot::isNetworkTerrain(int /*TeamTypes*/ eTeam)
{
	return m_pPlot ? m_pPlot->isNetworkTerrain((TeamTypes) eTeam) : false;
}

bool CyPlot::isBonusNetwork(int /*TeamTypes*/ eTeam)
{
	return m_pPlot ? m_pPlot->isBonusNetwork((TeamTypes) eTeam) : false;
}
bool CyPlot::isTradeNetworkImpassable(int /*TeamTypes*/ eTeam)
{
	return m_pPlot ? m_pPlot->isTradeNetworkImpassable((TeamTypes) eTeam) : false;
}

bool CyPlot::isTradeNetwork(int /*TeamTypes*/ eTeam)
{
	return m_pPlot ? m_pPlot->isTradeNetwork((TeamTypes)eTeam) : false;
}

bool CyPlot::isTradeNetworkConnected(CyPlot* pPlot, int /*TeamTypes*/ eTeam)
{
	return m_pPlot ? m_pPlot->isTradeNetworkConnected(pPlot->getPlot(), (TeamTypes)eTeam) : false;
}

bool CyPlot::isValidDomainForLocation(CyUnit* pUnit) const
{
	return (m_pPlot && pUnit && pUnit->getUnit()) ? m_pPlot->isValidDomainForLocation(*(pUnit->getUnit())) : false;
}

bool CyPlot::isValidDomainForAction(CyUnit* pUnit) const
{
	return (m_pPlot && pUnit && pUnit->getUnit()) ? m_pPlot->isValidDomainForAction(*(pUnit->getUnit())) : false;
}

bool CyPlot::isImpassable()
{
	return m_pPlot ? m_pPlot->isImpassable() : false;
}

int CyPlot::getX() 
{
	return m_pPlot ? m_pPlot->getX_INLINE() : -1;
}

int CyPlot::getY() 
{
	return m_pPlot ? m_pPlot->getY_INLINE() : -1;
}

bool CyPlot::at(int iX, int iY)
{
	return m_pPlot ? m_pPlot->at(iX, iY) : false;
}

int CyPlot::getLatitude()																						
{
	return m_pPlot ? m_pPlot->getLatitude() : -1;
}

CyArea* CyPlot::area()
{
	return m_pPlot ? new CyArea(m_pPlot->area()) : NULL;
}

CyArea* CyPlot::waterArea()
{
	return m_pPlot ? new CyArea(m_pPlot->waterArea()) : NULL;
}

int CyPlot::getArea()
{
	return m_pPlot ? m_pPlot->getArea() : -1;
}

int CyPlot::getUpgradeProgress()
{
	return m_pPlot ? m_pPlot->getUpgradeProgress() : -1;
}

int CyPlot::getUpgradeTimeLeft(int /*ImprovementTypes*/ eImprovement, int /*PlayerTypes*/ ePlayer)
{
	return m_pPlot ? m_pPlot->getUpgradeTimeLeft((ImprovementTypes) eImprovement, (PlayerTypes) ePlayer) : -1;
}

void CyPlot::setUpgradeProgress(int iNewValue)
{
	if (m_pPlot)
		m_pPlot->setUpgradeProgress(iNewValue);
}

void CyPlot::changeUpgradeProgress(int iChange)
{
	if (m_pPlot)
		m_pPlot->changeUpgradeProgress(iChange);
}

int CyPlot::getForceUnownedTimer()
{
	return m_pPlot ? m_pPlot->getForceUnownedTimer() : -1;
}

bool CyPlot::isForceUnowned()
{
	return m_pPlot ? m_pPlot->isForceUnowned() : false;
}

void CyPlot::setForceUnownedTimer(int iNewValue)
{
	if (m_pPlot)
		m_pPlot->setForceUnownedTimer(iNewValue);
}

void CyPlot::changeForceUnownedTimer(int iChange)
{
	if (m_pPlot)
		m_pPlot->changeForceUnownedTimer(iChange);
}

int CyPlot::getCityRadiusCount()
{
	return m_pPlot ? m_pPlot->getCityRadiusCount() : -1;
}

int CyPlot::isCityRadius()
{
	return m_pPlot ? m_pPlot->isCityRadius() : -1;
}

bool CyPlot::isStartingPlot()
{
	return m_pPlot ? m_pPlot->isStartingPlot() : false;
}

void CyPlot::setStartingPlot(bool bNewValue)
{
	if (m_pPlot)
		m_pPlot->setStartingPlot(bNewValue);
}

bool CyPlot::isNOfRiver()
{
	return m_pPlot ? m_pPlot->isNOfRiver() : false;
}

void CyPlot::setNOfRiver(bool bNewValue, CardinalDirectionTypes eRiverDir)
{
	if (m_pPlot)
	{
		m_pPlot->setNOfRiver(bNewValue, eRiverDir);
	}
}

bool CyPlot::isWOfRiver()
{
	return m_pPlot ? m_pPlot->isWOfRiver() : false;
}

void CyPlot::setWOfRiver(bool bNewValue, CardinalDirectionTypes eRiverDir)
{
	if (m_pPlot)
	{
		m_pPlot->setWOfRiver(bNewValue, eRiverDir);
	}
}

CardinalDirectionTypes CyPlot::getRiverWEDirection()
{
	return m_pPlot->getRiverWEDirection();
}

CardinalDirectionTypes CyPlot::getRiverNSDirection()
{
	return m_pPlot->getRiverNSDirection();
}

bool CyPlot::isIrrigated()
{
	return m_pPlot ? m_pPlot->isIrrigated() : false;
}

bool CyPlot::isPotentialCityWork()
{
	return m_pPlot ? m_pPlot->isPotentialCityWork() : false;
}

bool CyPlot::isPotentialCityWorkForArea(CyArea* pArea)
{
	return m_pPlot ? m_pPlot->isPotentialCityWorkForArea(pArea->getArea()) : false;
}

bool CyPlot::isFlagDirty()
{
	return m_pPlot ? m_pPlot->isFlagDirty() : false;
}

void CyPlot::setFlagDirty(bool bNewValue)
{
	if (m_pPlot)
	{
		m_pPlot->setFlagDirty(bNewValue);
	}
}

int CyPlot::getOwner()
{
	return m_pPlot ? m_pPlot->getOwnerINLINE() : -1;
}

void CyPlot::setOwner(int /*PlayerTypes*/ eNewValue)
{
	if (m_pPlot)
		m_pPlot->setOwner((PlayerTypes) eNewValue, true, true);
}

void CyPlot::setOwnerNoUnitCheck(int /*PlayerTypes*/ eNewValue)
{
	if (m_pPlot)
		m_pPlot->setOwner((PlayerTypes) eNewValue, false, true);
}
PlotTypes CyPlot::getPlotType()
{
	return m_pPlot ? m_pPlot->getPlotType() : NO_PLOT;
}

bool CyPlot::isWater()
{
	return m_pPlot ? m_pPlot->isWater() : false;
}

bool CyPlot::isFlatlands()
{
	return m_pPlot ? m_pPlot->isFlatlands() : false;
}

bool CyPlot::isHills()
{
	return m_pPlot ? m_pPlot->isHills() : false;
}

bool CyPlot::isPeak()
{
	return m_pPlot ? m_pPlot->isPeak() : false;
}

void CyPlot::setPlotType(PlotTypes eNewValue, bool bRecalculate, bool bRebuildGraphics)
{
	if (m_pPlot)
		m_pPlot->setPlotType(eNewValue, bRecalculate, bRebuildGraphics);
}

int /*TerrainTypes*/ CyPlot::getTerrainType()
{
	return m_pPlot ? m_pPlot->getTerrainType() : -1;
}

void CyPlot::setTerrainType(int /*TerrainTypes*/ eNewValue, bool bRecalculate, bool bRebuildGraphics)
{
	if (m_pPlot)
		m_pPlot->setTerrainType((TerrainTypes)eNewValue, bRecalculate, bRebuildGraphics);
}

int /*FeatureTypes*/ CyPlot::getFeatureType()
{
	return m_pPlot ? m_pPlot->getFeatureType() : -1;
}

void CyPlot::setFeatureType(int /*FeatureTypes*/ eNewValue, int iVariety)
{
	if (m_pPlot)
		m_pPlot->setFeatureType((FeatureTypes)eNewValue, iVariety);
}

void CyPlot::setFeatureDummyVisibility(std::string dummyTag, bool show)
{
	if(m_pPlot)
		m_pPlot->setFeatureDummyVisibility(dummyTag.c_str(), show);
}

void CyPlot::addFeatureDummyModel(std::string dummyTag, std::string modelTag)
{
	if(m_pPlot)
		m_pPlot->addFeatureDummyModel(dummyTag.c_str(), modelTag.c_str());
}

void CyPlot::setFeatureDummyTexture(std::string dummyTag, std::string textureTag)
{
	if(m_pPlot)
		m_pPlot->setFeatureDummyTexture(dummyTag.c_str(), textureTag.c_str());
}

std::string CyPlot::pickFeatureDummyTag(int mouseX, int mouseY)
{
	if(m_pPlot)
		return m_pPlot->pickFeatureDummyTag(mouseX, mouseY);
	else
		return "";
}

void CyPlot::resetFeatureModel()
{
	if(m_pPlot)
		m_pPlot->resetFeatureModel();
}

int CyPlot::getFeatureVariety()
{
	return m_pPlot ? m_pPlot->getFeatureVariety() : -1;
}

int CyPlot::getOwnershipDuration()
{
	return m_pPlot ? m_pPlot->getOwnershipDuration() : -1;
}

bool CyPlot::isOwnershipScore()
{
	return m_pPlot ? m_pPlot->isOwnershipScore() : false;
}

void CyPlot::setOwnershipDuration(int iNewValue)
{
	if (m_pPlot)
		m_pPlot->setOwnershipDuration(iNewValue);
}

void CyPlot::changeOwnershipDuration(int iChange)
{
	if (m_pPlot)
		m_pPlot->changeOwnershipDuration(iChange);
}

int CyPlot::getImprovementDuration()
{
	return m_pPlot ? m_pPlot->getImprovementDuration() : -1;
}

void CyPlot::setImprovementDuration(int iNewValue)
{
	if (m_pPlot)
		m_pPlot->setImprovementDuration(iNewValue);
}

void CyPlot::changeImprovementDuration(int iChange)
{
	if (m_pPlot)
		m_pPlot->changeImprovementDuration(iChange);
}

int /* BonusTypes */ CyPlot::getBonusType(int /*TeamTypes*/ eTeam)
{
	return m_pPlot ? m_pPlot->getBonusType((TeamTypes)eTeam) : -1;
}

int /* BonusTypes */ CyPlot::getNonObsoleteBonusType(int /*TeamTypes*/ eTeam)
{
	return m_pPlot ? m_pPlot->getNonObsoleteBonusType((TeamTypes)eTeam) : -1;
}

void CyPlot::setBonusType(int /* BonusTypes */ eNewValue)
{
	if (m_pPlot)
		m_pPlot->setBonusType((BonusTypes)eNewValue);
}

int /* ImprovementTypes */ CyPlot::getImprovementType()
{
	return m_pPlot ? m_pPlot->getImprovementType() : -1;
}

void CyPlot::setImprovementType(int /* ImprovementTypes */ eNewValue)
{
	if (m_pPlot)
		m_pPlot->setImprovementType((ImprovementTypes)eNewValue);
}

int /* RouteTypes */ CyPlot::getRouteType()
{
	return m_pPlot ? m_pPlot->getRouteType() : -1;
}

void CyPlot::setRouteType(int /*RouteTypes*/ eNewValue)
{
	if (m_pPlot)
		m_pPlot->setRouteType((RouteTypes) eNewValue, true);
}

CyCity* CyPlot::getPlotCity()
{
	return m_pPlot ? new CyCity(m_pPlot->getPlotCity()) : NULL;
}

CyCity* CyPlot::getWorkingCity()
{
	return m_pPlot ? new CyCity(m_pPlot->getWorkingCity()) : NULL;
}

CyCity* CyPlot::getWorkingCityOverride()
{
	return m_pPlot ? new CyCity(m_pPlot->getWorkingCityOverride()) : NULL;
}

int CyPlot::getRiverID() const
{
	return m_pPlot ? m_pPlot->getRiverID() : -1;
}

void CyPlot::setRiverID(int iNewValue)
{
	if (m_pPlot)
		m_pPlot->setRiverID(iNewValue);
}

int CyPlot::getMinOriginalStartDist()
{
	return m_pPlot ? m_pPlot->getMinOriginalStartDist() : -1;
}

int CyPlot::getReconCount()
{
	return m_pPlot ? m_pPlot->getReconCount() : -1;
}

int CyPlot::getRiverCrossingCount()
{
	return m_pPlot ? m_pPlot->getRiverCrossingCount() : -1;
}

int CyPlot::getYield(YieldTypes eIndex)
{
	return m_pPlot ? m_pPlot->getYield(eIndex) : -1;
}

int CyPlot::calculateNatureYield(YieldTypes eIndex, TeamTypes eTeam, bool bIgnoreFeature)
{
	return m_pPlot ? m_pPlot->calculateNatureYield(eIndex, eTeam, bIgnoreFeature) : -1;
}

int CyPlot::calculateBestNatureYield(YieldTypes eIndex, TeamTypes eTeam)
{
	return m_pPlot ? m_pPlot->calculateBestNatureYield(eIndex, eTeam) : -1;
}

int CyPlot::calculateTotalBestNatureYield(TeamTypes eTeam)
{
	return m_pPlot ? m_pPlot->calculateTotalBestNatureYield(eTeam) : -1;
}

int CyPlot::calculateImprovementYieldChange(int /*ImprovementTypes*/ eImprovement, YieldTypes eYield, int /*PlayerTypes*/ ePlayer, bool bOptimal)
{
	return m_pPlot ? m_pPlot->calculateImprovementYieldChange((ImprovementTypes) eImprovement, eYield, (PlayerTypes) ePlayer, bOptimal) : -1;
}

int CyPlot::calculateYield(YieldTypes eIndex, bool bDisplay)
{
	return m_pPlot ? m_pPlot->calculateYield(eIndex, bDisplay) : -1;
}

bool CyPlot::hasYield()
{
	return m_pPlot ? m_pPlot->hasYield() : false;
}

int CyPlot::getCulture(int /*PlayerTypes*/ eIndex)
{
	return m_pPlot ? m_pPlot->getCulture((PlayerTypes)eIndex) : -1;
}

int CyPlot::countTotalCulture()
{
	return m_pPlot ? m_pPlot->countTotalCulture() : -1;
}

int /*TeamTypes*/ CyPlot::findHighestCultureTeam()
{
	return m_pPlot ? m_pPlot->findHighestCultureTeam() : -1;
}

int CyPlot::calculateCulturePercent(int /*PlayerTypes*/ eIndex)	
{
	return m_pPlot ? m_pPlot->calculateCulturePercent((PlayerTypes)eIndex) : -1;
}

int CyPlot::calculateTeamCulturePercent(int /*TeamTypes*/ eIndex)	
{
	return m_pPlot ? m_pPlot->calculateTeamCulturePercent((TeamTypes)eIndex) : -1;
}

void CyPlot::setCulture(int /*PlayerTypes*/ eIndex, int iChange, bool bUpdate)
{
	if (m_pPlot)
		m_pPlot->setCulture((PlayerTypes)eIndex, iChange, bUpdate, true);
}

void CyPlot::changeCulture(int /*PlayerTypes*/ eIndex, int iChange, bool bUpdate)
{
	if (m_pPlot)
		m_pPlot->changeCulture((PlayerTypes)eIndex, iChange, bUpdate);
}

int CyPlot::countNumAirUnits(int /*TeamTypes*/ eTeam)
{
	return m_pPlot ? m_pPlot->countNumAirUnits((TeamTypes)eTeam) : -1;
}

int CyPlot::getFoundValue(int /*PlayerTypes*/ eIndex)	
{
	return m_pPlot ? m_pPlot->getFoundValue((PlayerTypes)eIndex) : -1;
}

bool CyPlot::isBestAdjacentFound(int /*PlayerTypes*/ eIndex)	
{
	return m_pPlot ? m_pPlot->isBestAdjacentFound((PlayerTypes)eIndex) : false;
}

int CyPlot::getPlayerCityRadiusCount(int /*PlayerTypes*/ eIndex)	
{
	return m_pPlot ? m_pPlot->getPlayerCityRadiusCount((PlayerTypes)eIndex) : -1;
}

bool CyPlot::isPlayerCityRadius(int /*PlayerTypes*/ eIndex)	
{
	return m_pPlot ? m_pPlot->isPlayerCityRadius((PlayerTypes)eIndex) : false;
}

int CyPlot::getVisibilityCount(int /*TeamTypes*/ eTeam)
{
	return m_pPlot ? m_pPlot->getVisibilityCount((TeamTypes)eTeam) : -1;
}

void CyPlot::changeVisibilityCount(int /*TeamTypes*/ eTeam, int iChange, int /*InvisibleTypes*/ eSeeInvisible)
{
	if (m_pPlot)
		m_pPlot->changeVisibilityCount((TeamTypes) eTeam, iChange, (InvisibleTypes) eSeeInvisible, true);
}

int CyPlot::getStolenVisibilityCount(int /*TeamTypes*/ eTeam)
{
	return m_pPlot ? m_pPlot->getStolenVisibilityCount((TeamTypes)eTeam) : -1;
}

int /*PlayerTypes*/ CyPlot::getRevealedOwner(int /*TeamTypes*/ eTeam, bool bDebug)
{
	return m_pPlot ? m_pPlot->getRevealedOwner((TeamTypes)eTeam, bDebug) : -1;
}

int /*TeamTypes*/ CyPlot::getRevealedTeam(int /*TeamTypes*/ eTeam, bool bDebug)
{
	return m_pPlot ? m_pPlot->getRevealedTeam((TeamTypes)eTeam, bDebug) : -1;
}

bool CyPlot::isRiverCrossing(DirectionTypes eIndex)
{
	return m_pPlot ? m_pPlot->isRiverCrossing(eIndex) : false;
}

bool CyPlot::isRevealed(int /*TeamTypes*/ eTeam, bool bDebug)
{
	return m_pPlot ? m_pPlot->isRevealed((TeamTypes)eTeam, bDebug) : false;
}

void CyPlot::setRevealed(int /*TeamTypes*/ eTeam, bool bNewValue, bool bTerrainOnly, int /*TeamTypes*/ eFromTeam)
{
	if (m_pPlot)
		m_pPlot->setRevealed((TeamTypes)eTeam, bNewValue, bTerrainOnly, (TeamTypes)eFromTeam, true);
}

int /* ImprovementTypes */ CyPlot::getRevealedImprovementType(int /*TeamTypes*/ eTeam, bool bDebug)
{
	return m_pPlot ? m_pPlot->getRevealedImprovementType((TeamTypes)eTeam, bDebug) : -1;
}

int /* RouteTypes */ CyPlot::getRevealedRouteType(int /*TeamTypes*/ eTeam, bool bDebug)
{
	return m_pPlot ? m_pPlot->getRevealedRouteType((TeamTypes)eTeam, bDebug) : -1;
}

int CyPlot::getBuildProgress(int /*BuildTypes*/ eBuild)												
{
	return m_pPlot ? m_pPlot->getBuildProgress((BuildTypes)eBuild) : -1;
}

bool CyPlot::changeBuildProgress(int /*BuildTypes*/ eBuild, int iChange, int /*TeamTypes*/ eTeam)
{
	return m_pPlot ? m_pPlot->changeBuildProgress((BuildTypes)eBuild, iChange, (TeamTypes)eTeam) : false;
}

int CyPlot::getCultureRangeCities(int /*PlayerTypes*/ eOwnerIndex, int iRangeIndex)
{
	return m_pPlot ? m_pPlot->getCultureRangeCities((PlayerTypes) eOwnerIndex, iRangeIndex) : -1;
}

bool CyPlot::isCultureRangeCity(int /*PlayerTypes*/ eOwnerIndex, int iRangeIndex)
{
	return m_pPlot ? m_pPlot->isCultureRangeCity((PlayerTypes) eOwnerIndex, iRangeIndex) : false;
}

int CyPlot::getInvisibleVisibilityCount(int /*TeamTypes*/ eTeam, int /*InvisibleTypes*/ eInvisible)
{
	return m_pPlot ? m_pPlot->getInvisibleVisibilityCount((TeamTypes) eTeam, (InvisibleTypes) eInvisible) : -1;
}

bool CyPlot::isInvisibleVisible(int /*TeamTypes*/ eTeam, int /*InvisibleTypes*/ eInvisible)
{
	return m_pPlot ? m_pPlot->isInvisibleVisible((TeamTypes) eTeam, (InvisibleTypes) eInvisible) : -1;
}

void CyPlot::changeInvisibleVisibilityCount(int /*TeamTypes*/ eTeam, int /*InvisibleTypes*/ eInvisible, int iChange)
{
	if (m_pPlot)
		m_pPlot->changeInvisibleVisibilityCount((TeamTypes) eTeam, (InvisibleTypes) eInvisible, iChange);
}

int CyPlot::getNumUnits()
{
	return m_pPlot ? m_pPlot->getNumUnits() : -1;
}

CyUnit* CyPlot::getUnit(int iIndex)
{
	return m_pPlot ? new CyUnit(m_pPlot->getUnitByIndex(iIndex)) : NULL;
}

std::string CyPlot::getScriptData() const
{
	return m_pPlot ? m_pPlot->getScriptData() : "";
}

void CyPlot::setScriptData(std::string szNewValue)
{
	if (m_pPlot)
		m_pPlot->setScriptData(szNewValue.c_str());
}
