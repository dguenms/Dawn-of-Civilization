//
// init/cleanup XML functions
//
#include "CvGameCoreDLL.h"
#include "CvXMLLoadUtility.h"
#include "CvGameTextMgr.h"
#include "CvInfo_Building.h"
#include "CvInfo_Terrain.h"


/*  allocate and initialize a CvString pointer list of iListLen size to "", or
	to szString if it is supplied */
void CvXMLLoadUtility::InitStringList(CvString **ppszList, int iListLen, CvString szString)
{
	PROFILE_FUNC();

	FAssertMsg(*ppszList == NULL, "memory leak?");
	FAssertMsg(0 < iListLen, "list size to allocate is less than 1");
	// allocate memory for the boolean pointer based on the list length parameter
	*ppszList = new CvString[iListLen];
	// set the local pointer to the memory we just allocated
	CvString* pszList = *ppszList;

	for (int i = 0; i < iListLen; i++)
		pszList[i] = szString;
}

// allocate and initialize a 2d array of float data
void CvXMLLoadUtility::Init2DFloatList(float*** pppfList, int iSizeX, int iSizeY)
{
	PROFILE_FUNC();

	FAssertMsg(*pppfList == NULL, "memory leak?");
	FAssertMsg(0 < iSizeX && 0 < iSizeY, "list size to allocate is less than 1");
	// allocate the memory for the array of pointers to arrays of floats
	*pppfList = new float *[iSizeX];
	// set the local pointer to the newly allocated memory
	float** ppfList = *pppfList;

	for (int i = 0; i < iSizeX; i++)
	{
		ppfList[i] = new float[iSizeY];
		for (int j = 0; j < iSizeY; j++)
			ppfList[i][j] = 0.0f;
	}
}

// allocate and initialize a 2d array of int data
void CvXMLLoadUtility::Init2DIntList(int*** pppiList, int iSizeX, int iSizeY)
{
	PROFILE_FUNC();

	FAssertMsg(*pppiList == NULL, "memory leak?");
	FAssertMsg(0 < iSizeX && 0 < iSizeY, "list size to allocate is less than 1");
	// allocate the memory for the array of pointers to arrays of ints
	*pppiList = new int *[iSizeX];
	// set the local pointer to the newly allocated memory
	int** ppiList = *pppiList;

	for (int i = 0; i < iSizeX; i++)
	{
		ppiList[i] = new int[iSizeY];
		for (int j = 0; j < iSizeY; j++)
			ppiList[i][j] = 0;
	}
}

// allocate and initialize a 2d array of float data
void CvXMLLoadUtility::InitPointerFloatList(float*** pppfList, int iSizeX)
{
	PROFILE_FUNC();

	FAssertMsg(*pppfList == NULL, "memory leak?");
	FAssertMsg(0 < iSizeX, "list size to allocate is less than 1");
	// allocate the memory for the array of pointers to arrays of floats
	*pppfList = new float *[iSizeX];
	// set the local pointer to the newly allocated memory
	float** ppfList = *pppfList;

	for (int i = 0; i < iSizeX; i++)
		ppfList[i] = NULL;
}

// allocate and initialize a 2d array of int data
void CvXMLLoadUtility::InitPointerIntList(int*** pppiList, int iSizeX)
{
	PROFILE_FUNC();

	FAssertMsg(*pppiList == NULL, "memory leak?");
	FAssertMsg(0 < iSizeX, "list size to allocate is less than 1");
	// allocate the memory for the array of pointers to arrays of ints
	*pppiList = new int *[iSizeX];
	// set the local pointer to the newly allocated memory
	int** ppiList = *pppiList;

	for (int i = 0; i < iSizeX; i++)
		ppiList[i] = NULL;
}

// allocate and initialize a 2d array of DirectionTypes data
void CvXMLLoadUtility::Init2DDirectionTypesList(DirectionTypes*** pppiList, int iSizeX, int iSizeY)
{

	PROFILE_FUNC();

	FAssertMsg(*pppiList == NULL, "memory leak?");
	FAssertMsg(0 < iSizeX && 0 < iSizeY, "list size to allocate is less than 1");
	// allocate the memory for the array of pointers to arrays of DirectionTypes
	*pppiList = new DirectionTypes *[iSizeX];
	// set the local pointer to the newly allocated memory
	DirectionTypes** ppiList = *pppiList;

	for (int i = 0; i < iSizeX; i++) // loop through each of the pointers
	{
		// allocate a list of DirectionTypes for the current pointer
		ppiList[i] = new DirectionTypes[iSizeY];
		// loop through all of the current pointer's DirectionTypes
		for (int j = 0; j < iSizeY; j++)
			ppiList[i][j] = NO_DIRECTION;
	}
}

// allocate a improvement bonus struct list of iListLen size and initialize it's members
void CvXMLLoadUtility::InitImprovementBonusList(CvImprovementBonusInfo** ppImprovementBonus, int iListLen)
{
	PROFILE_FUNC();

	FAssertMsg(*ppImprovementBonus == NULL, "memory leak?");
	FAssertMsg(0 < iListLen, "list size to allocate is less than 1");
	// allocate memory for the bonus type pointer based on the list length parameter
	*ppImprovementBonus = new CvImprovementBonusInfo[iListLen];
	// set the local pointer to the memory we just allocated
	CvImprovementBonusInfo* paImprovementBonus = *ppImprovementBonus;

	for (int i = 0; i < iListLen; i++) // loop through all the bonus structs
	{
		paImprovementBonus[i].m_bBonusMakesValid = false;
		paImprovementBonus[i].m_bBonusTrade = false;
		FAssertMsg(paImprovementBonus[i].m_piYieldChange==NULL, "mem leak");
		paImprovementBonus[i].m_piYieldChange = new int[NUM_YIELD_TYPES];
		for (int j = 0; j < NUM_YIELD_TYPES; j++)
			paImprovementBonus[i].m_piYieldChange[j] = 0;
		paImprovementBonus[i].m_iDiscoverRand = 0;
	}
}

// allocate and initialize the civilization's default buildings
void CvXMLLoadUtility::InitBuildingDefaults(int **ppiDefaults)
{
	PROFILE_FUNC();

	FAssertMsg(*ppiDefaults == NULL,"memory leak?");
	*ppiDefaults = new int[GC.getNumBuildingClassInfos()];
	int* piDefaults = *ppiDefaults;

	FOR_EACH_ENUM(BuildingClass)
		piDefaults[eLoopBuildingClass] = GC.getInfo(eLoopBuildingClass).getDefaultBuilding();
}

// allocate and initialize the civilization's default Units
void CvXMLLoadUtility::InitUnitDefaults(int **ppiDefaults)
{
	PROFILE_FUNC();

	FAssertMsg(*ppiDefaults == NULL,"memory leak?");
	*ppiDefaults = new int[GC.getNumUnitClassInfos()];
	int* piDefaults = *ppiDefaults;

	FOR_EACH_ENUM(UnitClass)
		piDefaults[eLoopUnitClass] = GC.getInfo(eLoopUnitClass).getDefaultUnit();
}

// Free memory asociated with global variables
void CvXMLLoadUtility::CleanUpGlobalVariables()
{
	CvGlobals::getInstance().deleteInfoArrays();
}
