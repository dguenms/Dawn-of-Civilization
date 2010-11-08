#include "CvGameCoreDLL.h"
#include "CvMapGenerator.h"
#include "CvMap.h"
#include "CvFractal.h"
#include "CvPlot.h"
#include "CvGlobals.h"
#include "CvRandom.h"
#include "CvGameCoreUtils.h"
#include "CvGameAI.h"
//#include "CvEnums.h"
#include "CvInfos.h"
#include "CvDLLPythonIFaceBase.h"
#include "FProfiler.h"
#include "CyPlot.h"
#include "CyArgsList.h"

//
// static
//
CvMapGenerator* CvMapGenerator::m_pInst = NULL;

//
// singleton accessor
//
CvMapGenerator& CvMapGenerator::GetInstance()
{
	if (m_pInst==NULL)
	{
		m_pInst = new CvMapGenerator;
	}
	return *m_pInst;
}


CvMapGenerator::CvMapGenerator()
{
}


CvMapGenerator::~CvMapGenerator()
{
}


bool CvMapGenerator::canPlaceBonusAt(BonusTypes eBonus, int iX, int iY, bool bIgnoreLatitude)
{
	PROFILE_FUNC();

	CvArea* pArea;
	CvPlot* pPlot;
	CvPlot* pLoopPlot;
	int iRange;
	int iDX, iDY;
	int iI;

	pPlot = GC.getMapINLINE().plotINLINE(iX, iY);
	pArea = pPlot->area();

	if (!(pPlot->canHaveBonus(eBonus, bIgnoreLatitude)))
	{
		return false;
	}

	long result = 0;
	CyPlot kPlot = CyPlot(pPlot);
	CyArgsList argsList;
	argsList.add(gDLL->getPythonIFace()->makePythonObject(&kPlot));
	if (gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "canPlaceBonusAt", argsList.makeFunctionArgs(), &result))
	{
		if (!gDLL->getPythonIFace()->pythonUsingDefaultImpl())
		{
			if (result >= 0)
			{
				return result;
			}
			else
			{
				FAssertMsg(false, "canPlaceBonusAt() must return >= 0");
			}
		}
	}

	for (iI = 0; iI < NUM_DIRECTION_TYPES; iI++)
	{
		pLoopPlot = plotDirection(iX, iY, ((DirectionTypes)iI));

		if (pLoopPlot != NULL)
		{
			if ((pLoopPlot->getBonusType() != NO_BONUS) && (pLoopPlot->getBonusType() != eBonus))
			{
				return false;
			}
		}
	}

	CvBonusInfo& pInfo = GC.getBonusInfo(eBonus);
	CvBonusClassInfo& pClassInfo = GC.getBonusClassInfo((BonusClassTypes) pInfo.getBonusClassType());

	if (pPlot->isWater())
	{
		if (((GC.getMapINLINE().getNumBonusesOnLand(eBonus) * 100) / (GC.getMapINLINE().getNumBonuses(eBonus) + 1)) < pInfo.getMinLandPercent())
		{
			return false;
		}
	}

	// Make sure there are no bonuses of the same class (but a different type) nearby:

	iRange = pClassInfo.getUniqueRange();

	for (iDX = -(iRange); iDX <= iRange; iDX++)
	{
		for (iDY = -(iRange); iDY <= iRange; iDY++)
		{
			pLoopPlot	= plotXY(iX, iY, iDX, iDY);

			if (pLoopPlot != NULL)
			{
				if (pLoopPlot->area() == pArea)
				{
					if (plotDistance(iX, iY, pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE()) <= iRange)
					{
						BonusTypes eOtherBonus = pLoopPlot->getBonusType();
						if (eOtherBonus != NO_BONUS)
						{
							if (GC.getBonusInfo(eOtherBonus).getBonusClassType() == pInfo.getBonusClassType())
							{
								return false;
							}
						}
					}
				}
			}
		}
	}

	// Make sure there are none of the same bonus nearby:

	iRange = pInfo.getUniqueRange();

	for (iDX = -(iRange); iDX <= iRange; iDX++)
	{
		for (iDY = -(iRange); iDY <= iRange; iDY++)
		{
			pLoopPlot	= plotXY(iX, iY, iDX, iDY);

			if (pLoopPlot != NULL)
			{
				if (pLoopPlot->area() == pArea)
				{
					if (plotDistance(iX, iY, pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE()) <= iRange)
					{
						if (pLoopPlot->getBonusType() == eBonus)
						{
							return false;
						}
					}
				}
			}
		}
	}

	return true;
}


bool CvMapGenerator::canPlaceGoodyAt(ImprovementTypes eImprovement, int iX, int iY)
{
	PROFILE_FUNC();

	CvPlot* pPlot;

	FAssertMsg(eImprovement != NO_IMPROVEMENT, "Improvement is not assigned a valid value");
	FAssertMsg(GC.getImprovementInfo(eImprovement).isGoody(), "ImprovementType eImprovement is expected to be a goody");

	if (GC.getGameINLINE().isOption(GAMEOPTION_NO_GOODY_HUTS))
	{
		return false;
	}

	pPlot = GC.getMapINLINE().plotINLINE(iX, iY);

	if (!(pPlot->canHaveImprovement(eImprovement, NO_TEAM))) 
	{
		return false;
	}

	long result = 0;
	CyPlot kPlot = CyPlot(pPlot);
	CyArgsList argsList;
	argsList.add(gDLL->getPythonIFace()->makePythonObject(&kPlot));
	if (gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "canPlaceGoodyAt", argsList.makeFunctionArgs(), &result))
	{
		if (!gDLL->getPythonIFace()->pythonUsingDefaultImpl()) // Python override
		{
			if (result >= 0)
			{
				return result;
			}
			else
			{
				FAssertMsg(false, "python canPlaceGoodyAt() must return >= 0");
			}
		}
	}

	if (pPlot->getImprovementType() != NO_IMPROVEMENT) 
	{
		return false;
	}

	if (pPlot->getBonusType() != NO_BONUS)
	{
		return false;
	}

	if (pPlot->isImpassable()) 
	{
		return false;
	}

	int iUniqueRange = GC.getImprovementInfo(eImprovement).getGoodyUniqueRange();
	for (int iDX = -iUniqueRange; iDX <= iUniqueRange; iDX++) 
	{
		for (int iDY = -iUniqueRange; iDY <= iUniqueRange; iDY++)
		{
			CvPlot *pLoopPlot	= plotXY(iX, iY, iDX, iDY);
			if (pLoopPlot != NULL && pLoopPlot->getImprovementType() == eImprovement) 
			{
				return false;
			}
		}
	}

	return true;
}


void CvMapGenerator::addGameElements()
{
	addRivers();
	gDLL->logMemState("CvMapGen after add rivers");

	addLakes();
	gDLL->logMemState("CvMapGen after add lakes");

	addFeatures();
	gDLL->logMemState("CvMapGen after add features");

	addBonuses();
	gDLL->logMemState("CvMapGen after add bonuses");

	addGoodies();
	gDLL->logMemState("CvMapGen after add goodies");

	// Call for Python to make map modifications after it's been generated
	afterGeneration();
}


void CvMapGenerator::addLakes()
{
	PROFILE("CvMapGenerator::addLakes");

	if (gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "addLakes"))
	{
		if (!gDLL->getPythonIFace()->pythonUsingDefaultImpl())
		{
			return;
		}
	}

	gDLL->NiTextOut("Adding Lakes...");
	CvPlot* pLoopPlot;
	int iI;

	for (iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
	{
		gDLL->callUpdater();
		pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);
		FAssertMsg(pLoopPlot != NULL, "LoopPlot is not assigned a valid value");

		if (!(pLoopPlot->isWater()))
		{
			if (!(pLoopPlot->isCoastalLand()))
			{
				if (!(pLoopPlot->isRiver()))
				{
					if (GC.getGameINLINE().getMapRandNum(GC.getDefineINT("LAKE_PLOT_RAND"), "addLakes") == 0)
					{
						pLoopPlot->setPlotType(PLOT_OCEAN);
					}
				}
			}
		}
	}
}

void CvMapGenerator::addRivers()
{
	PROFILE("CvMapGenerator::addRivers");

	if (gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "addRivers"))
	{
		if (!gDLL->getPythonIFace()->pythonUsingDefaultImpl())
		{
			return;
		}
	}

	gDLL->NiTextOut("Adding Rivers...");
	CvPlot* pLoopPlot;
	CvPlot* pStartPlot;
	int iPass;
	int iRiverSourceRange;
	int iSeaWaterRange;
	int iI;

	for (iPass = 0; iPass < 4; iPass++)
	{
		if (iPass <= 1)
		{
			iRiverSourceRange = GC.getDefineINT("RIVER_SOURCE_MIN_RIVER_RANGE");
		}
		else
		{
			iRiverSourceRange = (GC.getDefineINT("RIVER_SOURCE_MIN_RIVER_RANGE") / 2);
		}

		if (iPass <= 1)
		{
			iSeaWaterRange = GC.getDefineINT("RIVER_SOURCE_MIN_SEAWATER_RANGE");
		}
		else
		{
			iSeaWaterRange = (GC.getDefineINT("RIVER_SOURCE_MIN_SEAWATER_RANGE") / 2);
		}

		for (iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
		{
			gDLL->callUpdater();
			pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);
			FAssertMsg(pLoopPlot != NULL, "LoopPlot is not assigned a valid value");

			if (!(pLoopPlot->isWater()))
			{
				if (((iPass == 0) && (pLoopPlot->isHills() || pLoopPlot->isPeak())) ||
					  ((iPass == 1) && !(pLoopPlot->isCoastalLand()) && (GC.getGameINLINE().getMapRandNum(8, "addRivers") == 0)) ||
					  ((iPass == 2) && (pLoopPlot->isHills() || pLoopPlot->isPeak()) && (pLoopPlot->area()->getNumRiverEdges() < ((pLoopPlot->area()->getNumTiles() / GC.getDefineINT("PLOTS_PER_RIVER_EDGE")) + 1))) ||
					  ((iPass == 3) && (pLoopPlot->area()->getNumRiverEdges() < ((pLoopPlot->area()->getNumTiles() / GC.getDefineINT("PLOTS_PER_RIVER_EDGE")) + 1))))
				{
					if (!(GC.getMapINLINE().findWater(pLoopPlot, iRiverSourceRange, true)))
					{
						if (!(GC.getMapINLINE().findWater(pLoopPlot, iSeaWaterRange, false)))
						{
							pStartPlot = pLoopPlot->getInlandCorner();

							if (pStartPlot != NULL)
							{
								doRiver(pStartPlot);
							}
						}
					}
				}
			}
		}
	}
}

// pStartPlot = the plot at whose SE corner the river is starting
// 
void CvMapGenerator::doRiver(CvPlot *pStartPlot, CardinalDirectionTypes eLastCardinalDirection, CardinalDirectionTypes eOriginalCardinalDirection, int iThisRiverID)
{
	if (iThisRiverID == -1)
	{
		iThisRiverID = GC.getMapINLINE().getNextRiverID();
		GC.getMapINLINE().incrementNextRiverID();
	}

	int iOtherRiverID = pStartPlot->getRiverID();
	if (iOtherRiverID != -1 && iOtherRiverID != iThisRiverID)
	{
		return; // Another river already exists here; can't branch off of an existing river!
	}

	CvPlot *pRiverPlot = NULL;
	CvPlot *pAdjacentPlot = NULL;

	CardinalDirectionTypes eBestCardinalDirection = NO_CARDINALDIRECTION;

	if (eLastCardinalDirection==CARDINALDIRECTION_NORTH) 
	{
		pRiverPlot = pStartPlot;
		if (pRiverPlot == NULL)
		{
			return;
		}
		pAdjacentPlot = plotCardinalDirection(pRiverPlot->getX_INLINE(), pRiverPlot->getY_INLINE(), CARDINALDIRECTION_EAST);
		if ((pAdjacentPlot == NULL) || pRiverPlot->isWOfRiver() || pRiverPlot->isWater() || pAdjacentPlot->isWater())
		{
			return;
		}

		pStartPlot->setRiverID(iThisRiverID);
		pRiverPlot->setWOfRiver(true, eLastCardinalDirection);
		pRiverPlot = plotCardinalDirection(pRiverPlot->getX_INLINE(), pRiverPlot->getY_INLINE(), CARDINALDIRECTION_NORTH);
	}
	else if (eLastCardinalDirection==CARDINALDIRECTION_EAST)
	{
		pRiverPlot = plotCardinalDirection(pStartPlot->getX_INLINE(), pStartPlot->getY_INLINE(), CARDINALDIRECTION_EAST);
		if (pRiverPlot == NULL)
		{
			return;
		}
		pAdjacentPlot = plotCardinalDirection(pRiverPlot->getX_INLINE(), pRiverPlot->getY_INLINE(), CARDINALDIRECTION_SOUTH);
		if ((pAdjacentPlot == NULL) || pRiverPlot->isNOfRiver() || pRiverPlot->isWater() || pAdjacentPlot->isWater())
		{
			return;
		}

		pStartPlot->setRiverID(iThisRiverID);
		pRiverPlot->setNOfRiver(true, eLastCardinalDirection);
	}
	else if (eLastCardinalDirection==CARDINALDIRECTION_SOUTH)
	{
		pRiverPlot = plotCardinalDirection(pStartPlot->getX_INLINE(), pStartPlot->getY_INLINE(), CARDINALDIRECTION_SOUTH);
		if (pRiverPlot == NULL)
		{
			return;
		}
		pAdjacentPlot = plotCardinalDirection(pRiverPlot->getX_INLINE(), pRiverPlot->getY_INLINE(), CARDINALDIRECTION_EAST);
		if ((pAdjacentPlot == NULL) || pRiverPlot->isWOfRiver() || pRiverPlot->isWater() || pAdjacentPlot->isWater())
		{
			return;
		}

		pStartPlot->setRiverID(iThisRiverID);
		pRiverPlot->setWOfRiver(true, eLastCardinalDirection);
	}

	else if (eLastCardinalDirection==CARDINALDIRECTION_WEST)
	{
		pRiverPlot = pStartPlot;
		if (pRiverPlot == NULL)
		{
			return;
		}
		pAdjacentPlot = plotCardinalDirection(pRiverPlot->getX_INLINE(), pRiverPlot->getY_INLINE(), CARDINALDIRECTION_SOUTH);
		if ((pAdjacentPlot == NULL) || pRiverPlot->isNOfRiver() || pRiverPlot->isWater() || pAdjacentPlot->isWater())
		{
			return;
		}

		pStartPlot->setRiverID(iThisRiverID);
		pRiverPlot->setNOfRiver(true, eLastCardinalDirection);
		pRiverPlot = plotCardinalDirection(pRiverPlot->getX_INLINE(), pRiverPlot->getY_INLINE(), CARDINALDIRECTION_WEST);
	}
	else
	{
		//FAssertMsg(false, "Illegal direction type"); 
		// River is starting here, set the direction in the next step
		pRiverPlot = pStartPlot;

		long result = 0;
		CyPlot kPlot = CyPlot(pRiverPlot);
		CyArgsList argsList;
		argsList.add(gDLL->getPythonIFace()->makePythonObject(&kPlot));
		if (gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "getRiverStartCardinalDirection", argsList.makeFunctionArgs(), &result))
		{
			if (!gDLL->getPythonIFace()->pythonUsingDefaultImpl()) // Python override
			{
				if (result >= 0)
				{
					eBestCardinalDirection = ((CardinalDirectionTypes)result);
				}
				else
				{
					FAssertMsg(false, "python getRiverStartCardinalDirection() must return >= 0");
				}
			}
		}
	}

	if (pRiverPlot == NULL)
	{
		return; // The river has flowed off the edge of the map. All is well.
	}
	else if (pRiverPlot->hasCoastAtSECorner())
	{
		return; // The river has flowed into the ocean. All is well.
	}

	if (eBestCardinalDirection == NO_CARDINALDIRECTION)
	{
		int iBestValue = MAX_INT;

		for (int iI = 0; iI < NUM_CARDINALDIRECTION_TYPES; iI++)
		{
			if (getOppositeCardinalDirection((CardinalDirectionTypes)iI) != eOriginalCardinalDirection)
			{
				if (getOppositeCardinalDirection((CardinalDirectionTypes)iI) != eLastCardinalDirection)
				{
					CvPlot* pAdjacentPlot;
					pAdjacentPlot = plotCardinalDirection(pRiverPlot->getX_INLINE(), pRiverPlot->getY_INLINE(), ((CardinalDirectionTypes)iI));
					if (pAdjacentPlot != NULL)
					{
						int iValue = getRiverValueAtPlot(pAdjacentPlot);
						if (iValue < iBestValue)
						{
							iBestValue = iValue;
							eBestCardinalDirection = (CardinalDirectionTypes)iI;
						}
					}
				}
			}
		}
	}

	if (eBestCardinalDirection != NO_CARDINALDIRECTION)
	{
		if  (eOriginalCardinalDirection	== NO_CARDINALDIRECTION)
		{
			eOriginalCardinalDirection = eBestCardinalDirection;
		}
		doRiver(pRiverPlot, eBestCardinalDirection, eOriginalCardinalDirection, iThisRiverID);
	}
}
//Note from Blake:
//Iustus wrote this function, it ensures that a new river actually
//creates fresh water on the passed plot. Quite useful really
//Altouh I veto'd it's use since I like that you don't always 
//get fresh water starts.
// pFreshWaterPlot = the plot we want to give a fresh water river
// 
bool CvMapGenerator::addRiver(CvPlot* pFreshWaterPlot)
{
	FAssertMsg(pFreshWaterPlot != NULL, "NULL plot parameter");
	
	// cannot have a river flow next to water
	if (pFreshWaterPlot->isWater())
	{
		return false;
	}
	
	// if it already has a fresh water river, then success! we done
	if (pFreshWaterPlot->isRiver())
	{
		return true;
	}
	
	bool bSuccess = false;

	// randomize the order of directions
	int aiShuffle[NUM_CARDINALDIRECTION_TYPES];
	shuffleArray(aiShuffle, NUM_CARDINALDIRECTION_TYPES, GC.getGameINLINE().getMapRand());

	// make two passes, once for each flow direction of the river
	int iNWFlowPass = GC.getGameINLINE().getMapRandNum(2, "addRiver");
	for (int iPass = 0; !bSuccess && iPass <= 1; iPass++)
	{
		// try placing a river edge in each direction, in random order
		for (int iI = 0; !bSuccess && iI < NUM_CARDINALDIRECTION_TYPES; iI++)
		{
			CardinalDirectionTypes eRiverDirection = NO_CARDINALDIRECTION;
			CvPlot *pRiverPlot = NULL;
			
			switch (aiShuffle[iI])
			{
			case CARDINALDIRECTION_NORTH:
				if (iPass == iNWFlowPass)
				{
					pRiverPlot = plotDirection(pFreshWaterPlot->getX_INLINE(), pFreshWaterPlot->getY_INLINE(), DIRECTION_NORTH);
					eRiverDirection = CARDINALDIRECTION_WEST;
				}
				else 
				{
					pRiverPlot = plotDirection(pFreshWaterPlot->getX_INLINE(), pFreshWaterPlot->getY_INLINE(), DIRECTION_NORTHWEST);
					eRiverDirection = CARDINALDIRECTION_EAST;
				}
				break;

			case CARDINALDIRECTION_EAST:
				if (iPass == iNWFlowPass)
				{
					pRiverPlot = pFreshWaterPlot;
					eRiverDirection = CARDINALDIRECTION_NORTH;
				}
				else 
				{
					pRiverPlot = plotDirection(pFreshWaterPlot->getX_INLINE(), pFreshWaterPlot->getY_INLINE(), DIRECTION_NORTH);
					eRiverDirection = CARDINALDIRECTION_SOUTH;
				}
				break;

			case CARDINALDIRECTION_SOUTH:
				if (iPass == iNWFlowPass)
				{
					pRiverPlot = pFreshWaterPlot;
					eRiverDirection = CARDINALDIRECTION_WEST;
				}
				else 
				{
					pRiverPlot = plotDirection(pFreshWaterPlot->getX_INLINE(), pFreshWaterPlot->getY_INLINE(), DIRECTION_WEST);
					eRiverDirection = CARDINALDIRECTION_EAST;
				}
				break;

			case CARDINALDIRECTION_WEST:
				if (iPass == iNWFlowPass)
				{
					pRiverPlot = plotDirection(pFreshWaterPlot->getX_INLINE(), pFreshWaterPlot->getY_INLINE(), DIRECTION_WEST);
					eRiverDirection = CARDINALDIRECTION_NORTH;
				}
				else 
				{
					pRiverPlot = plotDirection(pFreshWaterPlot->getX_INLINE(), pFreshWaterPlot->getY_INLINE(), DIRECTION_NORTHWEST);
					eRiverDirection = CARDINALDIRECTION_SOUTH;
				}
				break;

			default:
				FAssertMsg(false, "invalid cardinal direction");
			}
			
			if (pRiverPlot != NULL && !pRiverPlot->hasCoastAtSECorner())
			{
				// try to make the river
				doRiver(pRiverPlot, eRiverDirection, eRiverDirection, -1);

				// if it succeeded, then we will be a river now!
				if (pFreshWaterPlot->isRiver())
				{
					bSuccess = true;
				}
			}
		}
	}

	return bSuccess;
}


void CvMapGenerator::addFeatures()
{
	PROFILE("CvMapGenerator::addFeatures");

	if (gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "addFeatures", NULL))
	{
		if (!gDLL->getPythonIFace()->pythonUsingDefaultImpl())
		{
			return;
		}
	}

	for (int iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
	{
		CvPlot* pPlot = GC.getMapINLINE().plotByIndexINLINE(iI);
		FAssert(pPlot != NULL);

		for (int iJ = 0; iJ < GC.getNumFeatureInfos(); iJ++)
		{
			if (pPlot->canHaveFeature((FeatureTypes)iJ))
			{
				if (GC.getGameINLINE().getMapRandNum(10000, "addFeaturesAtPlot") < GC.getFeatureInfo((FeatureTypes)iJ).getAppearanceProbability())
				{
					pPlot->setFeatureType((FeatureTypes)iJ);
				}
			}
		}
	}
}

void CvMapGenerator::addBonuses()
{
	PROFILE("CvMapGenerator::addBonuses");
	gDLL->NiTextOut("Adding Bonuses...");

	if (gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "addBonuses", NULL))
	{
		if (!gDLL->getPythonIFace()->pythonUsingDefaultImpl())
		{
			return; // Python override
		}
	}

	for (int iOrder = 0; iOrder < GC.getNumBonusInfos(); iOrder++)
	{
		for (int iI = 0; iI < GC.getNumBonusInfos(); iI++)
		{
			gDLL->callUpdater();
			if (GC.getBonusInfo((BonusTypes)iI).getPlacementOrder() == iOrder)
			{
				CyArgsList argsList;
				argsList.add(iI);
				if (!gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "addBonusType", argsList.makeFunctionArgs()) || gDLL->getPythonIFace()->pythonUsingDefaultImpl())
				{
					if (GC.getBonusInfo((BonusTypes)iI).isOneArea())
					{
						addUniqueBonusType((BonusTypes)iI);
					}
					else
					{
						addNonUniqueBonusType((BonusTypes)iI);
					}
				}
			}
		}
	}
}

void CvMapGenerator::addUniqueBonusType(BonusTypes eBonusType)
{
	int* piAreaTried = new int[GC.getMapINLINE().getNumAreas()];

	for (int iI = 0; iI < GC.getMapINLINE().getNumAreas(); iI++)
	{
		piAreaTried[iI] = FFreeList::INVALID_INDEX;
	}

	CvBonusInfo& pBonusInfo = GC.getBonusInfo(eBonusType);

	int iBonusCount = calculateNumBonusesToAdd(eBonusType);

	bool bIgnoreLatitude = GC.getGameINLINE().pythonIsBonusIgnoreLatitudes();

	FAssertMsg(pBonusInfo.isOneArea(), "addUniqueBonusType called with non-unique bonus type");

	while (true)
	{
		int iBestValue = 0;
		int iLoop = 0;
		CvArea *pBestArea = NULL;
		CvArea *pLoopArea = NULL;

		for(pLoopArea = GC.getMapINLINE().firstArea(&iLoop); pLoopArea != NULL; pLoopArea = GC.getMapINLINE().nextArea(&iLoop))
		{
			bool bTried = false;

			for (int iI = 0; iI < GC.getMapINLINE().getNumAreas(); iI++)
			{
				if (pLoopArea->getID() == piAreaTried[iI])
				{
					bTried = true;
					break;
				}
			}

			if (!bTried)
			{
				int iNumUniqueBonusesOnArea = pLoopArea->countNumUniqueBonusTypes() + 1; // number of unique bonuses starting on the area, plus this one
				int iNumTiles = pLoopArea->getNumTiles();
				int iValue = iNumTiles / iNumUniqueBonusesOnArea;

				if (iValue > iBestValue)
				{
					iBestValue = iValue;
					pBestArea = pLoopArea;
				}
			}
		}

		if (pBestArea == NULL)
		{
			break; // can't place bonus on any area
		}

		for (int iI = 0; iI < GC.getMapINLINE().getNumAreas(); iI++)
		{
			if (piAreaTried[iI] == FFreeList::INVALID_INDEX)
			{
				piAreaTried[iI] = pBestArea->getID();
				break;
			}
		}

		// Place the bonuses:

		int* piShuffle = shuffle(GC.getMapINLINE().numPlotsINLINE(), GC.getGameINLINE().getMapRand());

		for (int iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
		{
			CvPlot* pPlot = GC.getMapINLINE().plotByIndexINLINE(piShuffle[iI]);
			FAssertMsg(pPlot != NULL, "addUniqueBonusType(): pPlot is null");

			if (GC.getMapINLINE().getNumBonuses(eBonusType) >= iBonusCount)
			{
				break; // We already have enough
			}

			if (pBestArea == pPlot->area())
			{
				if (canPlaceBonusAt(eBonusType, pPlot->getX_INLINE(), pPlot->getY_INLINE(), bIgnoreLatitude))
				{
					pPlot->setBonusType(eBonusType);

					for (int iDX = -(pBonusInfo.getGroupRange()); iDX <= pBonusInfo.getGroupRange(); iDX++)
					{
						for (int iDY = -(pBonusInfo.getGroupRange()); iDY <= pBonusInfo.getGroupRange(); iDY++)
						{
							if (GC.getMapINLINE().getNumBonuses(eBonusType) < iBonusCount)
							{
								CvPlot* pLoopPlot	= plotXY(pPlot->getX_INLINE(), pPlot->getY_INLINE(), iDX, iDY);

								if (pLoopPlot != NULL && (pLoopPlot->area() == pBestArea))
								{
									if (canPlaceBonusAt(eBonusType, pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE(), bIgnoreLatitude))
									{
										if (GC.getGameINLINE().getMapRandNum(100, "addUniqueBonusType") < pBonusInfo.getGroupRand())
										{
											pLoopPlot->setBonusType(eBonusType);
										}
									}
								}
							}
						}
					}
				}
			}
		}

		SAFE_DELETE_ARRAY(piShuffle);
	}

	SAFE_DELETE_ARRAY(piAreaTried);
}

void CvMapGenerator::addNonUniqueBonusType(BonusTypes eBonusType)
{
	int iBonusCount = calculateNumBonusesToAdd(eBonusType);

	if (iBonusCount == 0)
	{
		return;
	}

	int* piShuffle = shuffle(GC.getMapINLINE().numPlotsINLINE(), GC.getGameINLINE().getMapRand());

	CvBonusInfo& pBonusInfo = GC.getBonusInfo(eBonusType);

	bool bIgnoreLatitude = GC.getGameINLINE().pythonIsBonusIgnoreLatitudes();

	CvPlot* pPlot = NULL;
	for (int iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
	{
		pPlot = GC.getMapINLINE().plotByIndexINLINE(piShuffle[iI]);
		if (canPlaceBonusAt(eBonusType, pPlot->getX_INLINE(), pPlot->getY_INLINE(), bIgnoreLatitude))
		{
			pPlot->setBonusType(eBonusType);
			iBonusCount--;

			for (int iDX = -(pBonusInfo.getGroupRange()); iDX <= pBonusInfo.getGroupRange(); iDX++)
			{
				for (int iDY = -(pBonusInfo.getGroupRange()); iDY <= pBonusInfo.getGroupRange(); iDY++)
				{
					if (iBonusCount > 0)
					{
						CvPlot* pLoopPlot	= plotXY(pPlot->getX_INLINE(), pPlot->getY_INLINE(), iDX, iDY);

						if (pLoopPlot != NULL)
						{
							if (canPlaceBonusAt(eBonusType, pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE(), bIgnoreLatitude))
							{
								if (GC.getGameINLINE().getMapRandNum(100, "addNonUniqueBonusType") < pBonusInfo.getGroupRand())
								{
									pLoopPlot->setBonusType(eBonusType);
									iBonusCount--;
								}
							}
						}
					}
				}
			}

			FAssertMsg(iBonusCount >= 0, "iBonusCount must be >= 0");

			if (iBonusCount == 0)
			{
				break;
			}
		}
	}

	SAFE_DELETE_ARRAY(piShuffle);
}


void CvMapGenerator::addGoodies()
{
	PROFILE("CvMapGenerator::addGoodies");

	if (gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "addGoodies"))
	{
		if (!gDLL->getPythonIFace()->pythonUsingDefaultImpl())
		{
			return; // Python override
		}
	}

	gDLL->NiTextOut("Adding Goodies...");

	if (GC.getEraInfo(GC.getGameINLINE().getStartEra()).isNoGoodies())
	{
		return;
	}

	int iNumPlots = GC.getMapINLINE().numPlotsINLINE();
	int* piShuffle = shuffle(iNumPlots, GC.getGameINLINE().getMapRand());

	for (int iI = 0; iI < GC.getNumImprovementInfos(); iI++)
	{
		if (GC.getImprovementInfo((ImprovementTypes)iI).isGoody() && GC.getImprovementInfo((ImprovementTypes)iI).getTilesPerGoody() > 0)
		{
			for (int iJ = 0; iJ < iNumPlots; iJ++)
			{
				gDLL->callUpdater();
				CvPlot *pPlot = GC.getMapINLINE().plotByIndexINLINE(piShuffle[iJ]);
				FAssertMsg(pPlot, "pPlot is expected not to be NULL");
				if (!(pPlot->isWater()))
				{
					CvArea *pArea = GC.getMapINLINE().getArea(pPlot->getArea());
					FAssertMsg(pArea, "pArea is expected not to be NULL");
					if (pArea->getNumImprovements((ImprovementTypes)iI) < ((pArea->getNumTiles() + (GC.getImprovementInfo((ImprovementTypes)iI).getTilesPerGoody() / 2)) / GC.getImprovementInfo((ImprovementTypes) iI).getTilesPerGoody()))
					{
						if (canPlaceGoodyAt(((ImprovementTypes)iI), pPlot->getX_INLINE(), pPlot->getY_INLINE()))
						{
							pPlot->setImprovementType((ImprovementTypes)iI);
						}
					}
				}
			}
		}
	}

	SAFE_DELETE_ARRAY(piShuffle);
}


void CvMapGenerator::eraseRivers()
{
	int i;

	for (i = 0; i < GC.getMapINLINE().numPlotsINLINE(); i++)
	{
		CvPlot* pPlot = GC.getMapINLINE().plotByIndexINLINE(i);
		if (pPlot->isNOfRiver())
		{
			pPlot->setNOfRiver(false, NO_CARDINALDIRECTION);
		}
		if (pPlot->isWOfRiver())
		{
			pPlot->setWOfRiver(false, NO_CARDINALDIRECTION);
		}
	}
}

void CvMapGenerator::eraseFeatures()
{
	int i;

	for (i = 0; i < GC.getMapINLINE().numPlotsINLINE(); i++)
	{
		CvPlot* pPlot = GC.getMapINLINE().plotByIndexINLINE(i);
		pPlot->setFeatureType(NO_FEATURE);
	}
}

void CvMapGenerator::eraseBonuses()
{
	int i;

	for (i = 0; i < GC.getMapINLINE().numPlotsINLINE(); i++)
	{
		CvPlot* pPlot = GC.getMapINLINE().plotByIndexINLINE(i);
		pPlot->setBonusType(NO_BONUS);
	}
}

void CvMapGenerator::eraseGoodies()
{
	int i;

	for (i = 0; i < GC.getMapINLINE().numPlotsINLINE(); i++)
	{
		CvPlot* pPlot = GC.getMapINLINE().plotByIndexINLINE(i);
		if (pPlot->isGoody())
		{
			pPlot->removeGoody();
		}
	}
}

//------------------------------------------------------------------------------------------------
//
// Call python function to generate random map
// It will call applyMapData when it's done
//

void CvMapGenerator::generateRandomMap()
{
	PROFILE("generateRandomMap()");

	gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "beforeGeneration");

	if (gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "generateRandomMap"))
	{
		if (!gDLL->getPythonIFace()->pythonUsingDefaultImpl())
		{
			return; // Python override
		}
	}

	char buf[256];

	sprintf(buf, "Generating Random Map %S, %S...", gDLL->getMapScriptName().GetCString(), GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getDescription());
	gDLL->NiTextOut(buf);

	generatePlotTypes();
	generateTerrain();
}

void CvMapGenerator::generatePlotTypes()
{
	int* paiPlotTypes = new int[GC.getMapINLINE().numPlotsINLINE()];

	int iNumPlots = GC.getMapINLINE().numPlotsINLINE();

	std::vector<int> plotTypesOut;
	if (gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "generatePlotTypes", NULL, &plotTypesOut) && !gDLL->getPythonIFace()->pythonUsingDefaultImpl())
	{
		// Python override
		FAssertMsg((int)plotTypesOut.size() == iNumPlots, "python generatePlotTypes() should return list with length numPlotsINLINE");
		for (int iI = 0; iI < iNumPlots; iI++)
		{
			paiPlotTypes[iI] = plotTypesOut[iI];
		}
	}
	else
	{
		for (int iI = 0; iI < iNumPlots; iI++)
		{
			paiPlotTypes[iI] = PLOT_LAND;
		}
	}

	setPlotTypes(paiPlotTypes);

	SAFE_DELETE_ARRAY(paiPlotTypes);
}

void CvMapGenerator::generateTerrain()
{
	PROFILE("generateTerrain()");

	std::vector<int> terrainMapOut;
	if (gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "generateTerrainTypes", NULL, &terrainMapOut) && !gDLL->getPythonIFace()->pythonUsingDefaultImpl())
	{
		 // Python override
		int iNumPlots = GC.getMapINLINE().numPlotsINLINE();
		FAssertMsg((int)terrainMapOut.size() == iNumPlots, "python generateTerrain() should return a list with length CyMap().getNumPoints()");
		// Generate terrain for each plot
		for (int iI = 0; iI < iNumPlots; iI++)
		{
			gDLL->callUpdater();
			GC.getMapINLINE().plotByIndexINLINE(iI)->setTerrainType(((TerrainTypes)(terrainMapOut[iI])), false, false);
		}
	}
}

// Allows for user-defined Python Actions for map generation after it's already been created
void CvMapGenerator::afterGeneration()
{
	PROFILE("CvMapGenerator::afterGeneration");

	gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "afterGeneration");
}

void CvMapGenerator::setPlotTypes(const int* paiPlotTypes)
{
	CvPlot* pLoopPlot;
	int iNumPlots;

	iNumPlots = GC.getMapINLINE().numPlotsINLINE();

	for (int iI = 0; iI < iNumPlots; iI++)
	{
		gDLL->callUpdater();
		GC.getMapINLINE().plotByIndexINLINE(iI)->setPlotType(((PlotTypes)(paiPlotTypes[iI])), false, false);
	}

	GC.getMapINLINE().recalculateAreas();

	for (int iI = 0; iI < iNumPlots; iI++)
	{
		gDLL->callUpdater();
		pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);

		if (pLoopPlot->isWater())
		{
			if (pLoopPlot->isAdjacentToLand())
			{
				pLoopPlot->setTerrainType(((TerrainTypes)(GC.getDefineINT("SHALLOW_WATER_TERRAIN"))), false, false);
			}
			else
			{
				pLoopPlot->setTerrainType(((TerrainTypes)(GC.getDefineINT("DEEP_WATER_TERRAIN"))), false, false);
			}
		}
	}
}

// Protected functions:

int CvMapGenerator::getRiverValueAtPlot(CvPlot* pPlot)
{
	CvPlot* pAdjacentPlot;
	CvRandom riverRand;
	int iSum;
	int iI;

	FAssert(pPlot != NULL);

	long result = 0;
	CyPlot kPlot = CyPlot(pPlot);
	CyArgsList argsList;
	argsList.add(gDLL->getPythonIFace()->makePythonObject(&kPlot));
	if (gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "getRiverAltitude", argsList.makeFunctionArgs(), &result))
	{
		if (!gDLL->getPythonIFace()->pythonUsingDefaultImpl()) // Python override
		{
			if (result >= 0)
			{
				return result;
			}
			else
			{
				FAssertMsg(false, "python getRiverAltitude() must return >= 0");
			}
		}
	}

	iSum = result;

	iSum += ((NUM_PLOT_TYPES - pPlot->getPlotType()) * 20);

	for (iI = 0; iI < NUM_DIRECTION_TYPES; iI++)
	{
		pAdjacentPlot = plotDirection(pPlot->getX_INLINE(), pPlot->getY_INLINE(), ((DirectionTypes)iI));

		if (pAdjacentPlot != NULL)
		{
			iSum += (NUM_PLOT_TYPES - pAdjacentPlot->getPlotType());
		}
		else
		{
			iSum += (NUM_PLOT_TYPES * 10);
		}
	}

	riverRand.init((pPlot->getX_INLINE() * 43251267) + (pPlot->getY_INLINE() * 8273903));

	iSum += (riverRand.get(10, "River Rand"));

	return iSum;
}

int CvMapGenerator::calculateNumBonusesToAdd(BonusTypes eBonusType)
{
	CvBonusInfo& pBonusInfo = GC.getBonusInfo(eBonusType);

	// Calculate iBonusCount, the amount of this bonus to be placed:

	int iRand1 = GC.getGameINLINE().getMapRandNum(pBonusInfo.getRandAppearance1(), "calculateNumBonusesToAdd-1");
	int iRand2 = GC.getGameINLINE().getMapRandNum(pBonusInfo.getRandAppearance2(), "calculateNumBonusesToAdd-2");
	int iRand3 = GC.getGameINLINE().getMapRandNum(pBonusInfo.getRandAppearance3(), "calculateNumBonusesToAdd-3");
	int iRand4 = GC.getGameINLINE().getMapRandNum(pBonusInfo.getRandAppearance4(), "calculateNumBonusesToAdd-4");
	int iBaseCount = pBonusInfo.getConstAppearance() + iRand1 + iRand2 + iRand3 + iRand4;

	bool bIgnoreLatitude = GC.getGameINLINE().pythonIsBonusIgnoreLatitudes();

	// Calculate iNumPossible, the number of plots that are eligible to have this bonus:

	int iLandTiles = 0;
	if (pBonusInfo.getTilesPer() > 0)
	{
		int iNumPossible = 0;
		for (int iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
		{
			CvPlot* pPlot = GC.getMapINLINE().plotByIndexINLINE(iI);
			if (pPlot->canHaveBonus(eBonusType, bIgnoreLatitude))
			{
				iNumPossible++;
			}
		}
		iLandTiles += (iNumPossible / pBonusInfo.getTilesPer());
	}

	int iPlayers = (GC.getGameINLINE().countCivPlayersAlive() * pBonusInfo.getPercentPerPlayer()) / 100;
	int iBonusCount = (iBaseCount * (iLandTiles + iPlayers)) / 100;
	iBonusCount = std::max(1, iBonusCount);
	return iBonusCount;
}
