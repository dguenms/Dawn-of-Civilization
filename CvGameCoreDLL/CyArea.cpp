//
// Python wrapper class for CvArea 
// 
#include "CvGameCoreDLL.h"
#include "CyCity.h"
#include "CyArea.h"
#include "CvArea.h"

CyArea::CyArea() : m_pArea(NULL)
{
}

CyArea::CyArea(CvArea* pArea) : m_pArea(pArea)
{
}

int CyArea::calculateTotalBestNatureYield()
{
	return m_pArea ? m_pArea->calculateTotalBestNatureYield() : -1;
}

int CyArea::countCoastalLand()
{
	return m_pArea ? m_pArea->countCoastalLand() : -1;
}

int CyArea::countNumUniqueBonusTypes()
{
	return m_pArea ? m_pArea->countNumUniqueBonusTypes() : -1;
}

int CyArea::countHasReligion(int /*ReligionTypes*/ eReligion, int /*PlayerTypes*/ eOwner)
{
	return m_pArea ? m_pArea->countHasReligion((ReligionTypes)eReligion, (PlayerTypes)eOwner) : -1;
}

int CyArea::countHasCorporation(int /*CorporationTypes*/ eCorporation, int /*PlayerTypes*/ eOwner)
{
	return m_pArea ? m_pArea->countHasCorporation((CorporationTypes)eCorporation, (PlayerTypes)eOwner) : -1;
}

int CyArea::getID()
{
	return m_pArea ? m_pArea->getID() : -1;
}

int CyArea::getNumTiles()
{
	return m_pArea ? m_pArea->getNumTiles() : -1;
}

bool CyArea::isLake()
{
	return m_pArea ? m_pArea->isLake() : -1;
}

int CyArea::getNumOwnedTiles()
{
	return m_pArea ? m_pArea->getNumOwnedTiles() : -1;
}

int CyArea::getNumUnownedTiles()
{
	return m_pArea ? m_pArea->getNumUnownedTiles() : -1;
}

int CyArea::getNumRiverEdges()
{
	return m_pArea ? m_pArea->getNumRiverEdges() : -1;
}

int CyArea::getNumCities()
{
	return m_pArea ? m_pArea->getNumCities() : -1;
}

int CyArea::getNumUnits()
{
	return m_pArea ? m_pArea->getNumUnits() : -1;
}

int CyArea::getTotalPopulation()
{
	return m_pArea ? m_pArea->getTotalPopulation() : -1;
}

int CyArea::getNumStartingPlots()
{
	return m_pArea ? m_pArea->getNumStartingPlots() : -1;
}

bool CyArea::isWater()
{
	return m_pArea ? m_pArea->isWater() : false;
}

int CyArea::getUnitsPerPlayer(int /*PlayerTypes*/ eIndex)
{
	return m_pArea ? m_pArea->getUnitsPerPlayer((PlayerTypes) eIndex) : -1;
}

int CyArea::getAnimalsPerPlayer(int /*PlayerTypes*/ eIndex)
{
	return m_pArea ? m_pArea->getAnimalsPerPlayer((PlayerTypes) eIndex) : -1;
}

int CyArea::getCitiesPerPlayer(int /*PlayerTypes*/ eIndex)
{
	return m_pArea ? m_pArea->getCitiesPerPlayer((PlayerTypes) eIndex) : -1;
}

int CyArea::getPopulationPerPlayer(int /*PlayerTypes*/ eIndex)
{
	return m_pArea ? m_pArea->getPopulationPerPlayer((PlayerTypes) eIndex) : -1;
}

int CyArea::getBuildingGoodHealth(int /*PlayerTypes*/ eIndex)
{
	return m_pArea ? m_pArea->getBuildingGoodHealth((PlayerTypes) eIndex) : -1;
}

int CyArea::getBuildingBadHealth(int /*PlayerTypes*/ eIndex)
{
	return m_pArea ? m_pArea->getBuildingBadHealth((PlayerTypes) eIndex) : -1;
}

int CyArea::getBuildingHappiness(int /*PlayerTypes*/ eIndex)
{
	return m_pArea ? m_pArea->getBuildingHappiness((PlayerTypes) eIndex) : -1;
}

int CyArea::getFreeSpecialist(int /*PlayerTypes*/ eIndex)
{
	return m_pArea ? m_pArea->getFreeSpecialist((PlayerTypes) eIndex) : -1;
}

int CyArea::getPower(int /*PlayerTypes*/ eIndex)
{
	return m_pArea ? m_pArea->getPower((PlayerTypes) eIndex) : -1;
}

int CyArea::getBestFoundValue(int /*PlayerTypes*/ eIndex)
{
	return m_pArea ? m_pArea->getBestFoundValue((PlayerTypes) eIndex) : -1;
}

int CyArea::getNumRevealedTiles(int /*TeamTypes*/ eIndex)
{
	return m_pArea ? m_pArea->getNumRevealedTiles((TeamTypes)eIndex) : -1;
}

int CyArea::getNumUnrevealedTiles(int /*TeamTypes*/ eIndex)
{
	return m_pArea ? m_pArea->getNumUnrevealedTiles((TeamTypes)eIndex) : -1;
}

bool CyArea::isCleanPower(int /*TeamTypes*/ eIndex)
{
	return m_pArea ? m_pArea->isCleanPower((TeamTypes)eIndex) : false;
}

bool CyArea::isBorderObstacle(int /*TeamTypes*/ eIndex)
{
	return m_pArea ? m_pArea->isBorderObstacle((TeamTypes)eIndex) : false;
}

int /*AreaAITypes*/ CyArea::getAreaAIType(int /*TeamTypes*/ eIndex)
{
	return m_pArea ? (AreaAITypes) m_pArea->getAreaAIType((TeamTypes)eIndex) : -1;
}

CyCity* CyArea::getTargetCity(int /*PlayerTypes*/ eIndex)
{
	return m_pArea ? new CyCity(m_pArea->getTargetCity((PlayerTypes) eIndex)) : NULL;
}

int CyArea::getYieldRateModifier(int /*PlayerTypes*/ eIndex1, int /*YieldTypes*/ eIndex2)
{
	return m_pArea ? m_pArea->getYieldRateModifier((PlayerTypes)eIndex1, (YieldTypes) eIndex2) : -1;
}

int CyArea::getNumTrainAIUnits(int /*PlayerTypes*/ eIndex1, int /*UnitAITypes*/ eIndex2)
{
	return m_pArea ? m_pArea->getNumTrainAIUnits((PlayerTypes)eIndex1, (UnitAITypes) eIndex2) : -1;
}

int CyArea::getNumAIUnits(int /*PlayerTypes*/ eIndex1, int /*UnitAITypes*/ eIndex2)
{
	return m_pArea ? m_pArea->getNumAIUnits((PlayerTypes)eIndex1, (UnitAITypes) eIndex2) : -1;
}

int CyArea::getNumBonuses(int /*BonusTypes*/ eBonus)
{
	return m_pArea ? m_pArea->getNumBonuses((BonusTypes)eBonus) : -1;
}

int CyArea::getNumTotalBonuses()
{
	return m_pArea ? m_pArea->getNumTotalBonuses() : -1;
}


int CyArea::getNumImprovements(int /*ImprovementTypes*/ eImprovement)
{
	return m_pArea ? m_pArea->getNumImprovements( (ImprovementTypes)eImprovement) : -1;
}
