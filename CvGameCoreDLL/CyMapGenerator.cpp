//
//	FILE:	 CyMapGenerator.h
//	AUTHOR:  Mustafa Thamer
//	PURPOSE: 
//			Python wrapper class for CvMapGenerator
//
//-----------------------------------------------------------------------------
//	Copyright (c) 2005 Firaxis Games, Inc. All rights reserved.
//-----------------------------------------------------------------------------
//

#include "CvGameCoreDLL.h"
#include "CyMapGenerator.h"
#include "CvGlobals.h"
#include "CvDLLPythonIFaceBase.h"
#include "CvMapGenerator.h"
#include "CyPlot.h"

CyMapGenerator::CyMapGenerator() : m_pMapGenerator(NULL)
{
	m_pMapGenerator = &CvMapGenerator::GetInstance();
}

CyMapGenerator::CyMapGenerator(CvMapGenerator* pMapGenerator) : m_pMapGenerator(pMapGenerator)
{
}

bool CyMapGenerator::canPlaceBonusAt(int /*BonusTypes*/ eBonus, int iX, int iY, bool bIgnoreLatitude)	 
{
	return m_pMapGenerator ? m_pMapGenerator->canPlaceBonusAt((BonusTypes)eBonus, iX, iY, bIgnoreLatitude) : false;
}

bool CyMapGenerator::canPlaceGoodyAt(int /*ImprovementTypes*/ eImprovement, int iX, int iY)	 
{
	return m_pMapGenerator ? m_pMapGenerator->canPlaceGoodyAt((ImprovementTypes)eImprovement, iX, iY) : false;
}

void CyMapGenerator::addGameElements()
{
	if (m_pMapGenerator)
		m_pMapGenerator->addGameElements();
}

void CyMapGenerator::addLakes()
{
	if (m_pMapGenerator)
		m_pMapGenerator->addLakes();
}

void CyMapGenerator::addRivers()
{
	if (m_pMapGenerator)
		m_pMapGenerator->addRivers();
}

void CyMapGenerator::doRiver(CyPlot* pStartPlot, CardinalDirectionTypes eCardinalDirection)
{
	if (m_pMapGenerator)
		m_pMapGenerator->doRiver(pStartPlot->getPlot(), eCardinalDirection);
}

void CyMapGenerator::addFeatures()
{
	if (m_pMapGenerator)
		m_pMapGenerator->addFeatures();
}

void CyMapGenerator::addBonuses()
{
	if (m_pMapGenerator)
		m_pMapGenerator->addBonuses();
}

void CyMapGenerator::addUniqueBonusType(int /*BonusTypes*/ eBonusType)
{
	if (m_pMapGenerator)
		m_pMapGenerator->addUniqueBonusType((BonusTypes)eBonusType);
}

void CyMapGenerator::addNonUniqueBonusType(int /*BonusTypes*/ eBonusType)
{
	if (m_pMapGenerator)
		m_pMapGenerator->addNonUniqueBonusType((BonusTypes)eBonusType);
}

void CyMapGenerator::addGoodies()
{
	if (m_pMapGenerator)
		m_pMapGenerator->addGoodies();
}

void CyMapGenerator::eraseRivers()
{
	if (m_pMapGenerator)
		m_pMapGenerator->eraseRivers();
}

void CyMapGenerator::eraseFeatures()
{
	if (m_pMapGenerator)
		m_pMapGenerator->eraseFeatures();
}

void CyMapGenerator::eraseBonuses()
{
	if (m_pMapGenerator)
		m_pMapGenerator->eraseBonuses();
}

void CyMapGenerator::eraseGoodies()
{
	if (m_pMapGenerator)
		m_pMapGenerator->eraseGoodies();
}

void CyMapGenerator::generateRandomMap()
{
	if (m_pMapGenerator)
		m_pMapGenerator->generateRandomMap();
}

void CyMapGenerator::generatePlotTypes()
{
	if (m_pMapGenerator)
		m_pMapGenerator->generatePlotTypes();
}

void CyMapGenerator::generateTerrain()
{
	if (m_pMapGenerator)
		m_pMapGenerator->generateTerrain();
}

void CyMapGenerator::afterGeneration()
{
	if (m_pMapGenerator)
		m_pMapGenerator->afterGeneration();
}

void CyMapGenerator::setPlotTypes(boost::python::list& listPlotTypes)
{
	if (!m_pMapGenerator)
	{
		return;
	}

	int* paiPlotTypes = NULL;
	gDLL->getPythonIFace()->putSeqInArray(listPlotTypes.ptr() /*src*/, &paiPlotTypes /*dst*/);
	m_pMapGenerator->setPlotTypes(paiPlotTypes);
	delete [] paiPlotTypes;
}
