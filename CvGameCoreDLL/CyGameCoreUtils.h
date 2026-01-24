#pragma once

#ifndef CyGameCoreUtils_h
#define CyGameCoreUtils_h

//
// Python wrapper functions for DLL 
//

class CyCity;
class CyPlot;
class CyUnit;

int cyIntRange(int iNum, int iLow, int iHigh);
float cyFloatRange(float fNum, float fLow, float fHigh);
int cyDxWrap(int iDX);
int cyDyWrap(int iDY);
int cyPlotDistance(int iX1, int iY1, int iX2, int iY2);
int cyStepDistance(int iX1, int iY1, int iX2, int iY2);
CyPlot* cyPlotDirection(int iX, int iY, DirectionTypes eDirection);
CyPlot* cyPlotCardinalDirection(int iX, int iY, CardinalDirectionTypes eCardDirection);
CyPlot* cysPlotCardinalDirection(int iX, int iY, CardinalDirectionTypes eCardDirection);
CyPlot* cyPlotXY(int iX, int iY, int iDX, int iDY);
CyPlot* cysPlotXY(int iX, int iY, int iDX, int iDY);
DirectionTypes cyDirectionXYFromInt(int iDX, int iDY);
DirectionTypes cyDirectionXYFromPlot(CyPlot* pFromPlot, CyPlot* pToPlot);
CyPlot* cyPlotCity(int iX, int iY, int iIndex);
int cyPlotCityXYFromInt(int iDX, int iDY);
int cyPlotCityXYFromCity(CyCity* pCity, CyPlot* pPlot);
CardinalDirectionTypes cyGetOppositeCardinalDirection(CardinalDirectionTypes eDir);
DirectionTypes cyCardinalDirectionToDirection(CardinalDirectionTypes eCard);

bool cyIsCardinalDirection(DirectionTypes eDirection);
DirectionTypes cyEstimateDirection(int iDX, int iDY);

bool cyAtWar(int /*TeamTypes*/ eTeamA, int /*TeamTypes*/ eTeamB);
bool cyIsPotentialEnemy(int /*TeamTypes*/ eOurPlayer, int /*TeamTypes*/ eTheirPlayer);

CyCity* cyGetCity(IDInfo city);
CyUnit* cyGetUnit(IDInfo unit);

bool cyIsPromotionValid(int /*PromotionTypes*/ ePromotion, int /*UnitTypes*/ eUnit, bool bLeader);
int cyGetPopulationAsset(int iPopulation);
int cyGetLandPlotsAsset(int iLandPlots);
int cyGetPopulationPower(int iPopulation);
int cyGetPopulationScore(int iPopulation);
int cyGetLandPlotsScore(int iPopulation);
int cyGetTechScore(int /*TechTypes*/ eTech);
int cyGetWonderScore(int /*BuildingClassTypes*/ eWonderClass);
int /*ImprovementTypes*/ cyFinalImprovementUpgrade(int /*ImprovementTypes*/ eImprovement, int iCount);

int cyGetWorldSizeMaxConscript(int /*CivicTypes*/ eCivic);

bool cyIsReligionTech(int /*TechTypes*/ eTech);

bool cyIsTechRequiredForUnit(int /*TechTypes*/ eTech, int /*UnitTypes*/ eUnit);
bool cyIsTechRequiredForBuilding(int /*TechTypes*/ eTech, int /*BuildingTypes*/ eBuilding);
bool cyIsTechRequiredForProject(int /*TechTypes*/ eTech, int /*ProjectTypes*/ eProject);
bool cyIsWorldUnitClass(int /*UnitClassTypes*/ eUnitClass);
bool cyIsTeamUnitClass(int /*UnitClassTypes*/ eUnitClass);
bool cyIsNationalUnitClass(int /*UnitClassTypes*/ eUnitClass);
bool cyIsLimitedUnitClass(int /*UnitClassTypes*/ eUnitClass);
bool cyIsWorldWonderClass(int /*BuildingClassTypes*/ eBuildingClass);
bool cyIsTeamWonderClass(int /*BuildingClassTypes*/ eBuildingClass);
bool cyIsNationalWonderClass(int /*BuildingClassTypes*/ eBuildingClass);
bool cyIsLimitedWonderClass(int /*BuildingClassTypes*/ eBuildingClass);
bool cyIsWorldProject(int /*ProjectTypes*/ eProject);
bool cyIsTeamProject(int /*ProjectTypes*/ eProject);
bool cyIsLimitedProject(int /*ProjectTypes*/ eProject);
int cyGetCombatOdds(CyUnit* pAttacker, CyUnit* pDefender);
int cyGetEspionageModifier(int /*TeamTypes*/ iOurTeam, int /*TeamTypes*/ iTargetTeam);

#endif	// CyGameCoreUtils_h
