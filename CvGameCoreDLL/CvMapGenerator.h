#pragma once

#ifndef CIV4_MAPGENERATOR_H
#define CIV4_MAPGENERATOR_H

//#include "CvEnums.h"

#pragma warning( disable: 4251 )		// needs to have dll-interface to be used by clients of class

class CvFractal;
class CvPlot;
class CvArea;

class CvMapGenerator
{
public:
	DllExport static CvMapGenerator& GetInstance();
	DllExport static void FreeInstance() { SAFE_DELETE(m_pInst); }
	DllExport CvMapGenerator();
	DllExport virtual ~CvMapGenerator();

	bool canPlaceBonusAt(BonusTypes eBonus, int iX, int iY, bool bIgnoreLatitude);		// Exposed to Python
	bool canPlaceGoodyAt(ImprovementTypes eImprovement, int iX, int iY);							// Exposed to Python

	// does all of the below "add..." functions:
	DllExport void addGameElements();											// Exposed to Python

	void addLakes();																			// Exposed to Python
	DllExport void addRivers();														// Exposed to Python
	void doRiver(CvPlot* pStartPlot, CardinalDirectionTypes eLastCardinalDirection=NO_CARDINALDIRECTION, CardinalDirectionTypes eOriginalCardinalDirection=NO_CARDINALDIRECTION, int iThisRiverID=-1);	// Exposed to Python
	bool addRiver(CvPlot *pFreshWaterPlot);
	DllExport void addFeatures();													// Exposed to Python
	DllExport void addBonuses();													// Exposed to Python
	void addUniqueBonusType(BonusTypes eBonusType);				// Exposed to Python
	void addNonUniqueBonusType(BonusTypes eBonusType);		// Exposed to Python
	DllExport void addGoodies();													// Exposed to Python

	DllExport void eraseRivers();													// Exposed to Python
	DllExport void eraseFeatures();												// Exposed to Python
	DllExport void eraseBonuses();												// Exposed to Python
	DllExport void eraseGoodies();												// Exposed to Python

	DllExport void generateRandomMap();										// Exposed to Python

	void generatePlotTypes();															// Exposed to Python
	void generateTerrain();																// Exposed to Python

	void afterGeneration();																// Exposed to Python

	void setPlotTypes(const int* paiPlotTypes);						// Exposed to Python

protected:

	// Utility functions for roughenHeights()
	int getRiverValueAtPlot(CvPlot* pPlot);
	int calculateNumBonusesToAdd(BonusTypes eBonusType);

private:
	static CvMapGenerator* m_pInst;

};
#endif
