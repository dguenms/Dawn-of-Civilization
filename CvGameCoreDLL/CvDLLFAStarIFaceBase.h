#pragma once

#ifndef CvDLLFAStarIFaceBase_h
#define CvDLLFAStarIFaceBase_h

//
// abstract interface for FAStar functions used by DLL
//

class FAStar;
class FAStarNode;

// Function prototype for Cost and Validity functions
typedef int(*FAPointFunc)(int, int, const void*, FAStar*);
typedef int(*FAHeuristic)(int, int, int, int);
typedef int(*FAStarFunc)(FAStarNode*, FAStarNode*, int, const void*, FAStar*);

class CvDLLFAStarIFaceBase
{
public:
	virtual FAStar* create() = 0;
	virtual void destroy(FAStar*& ptr, bool bSafeDelete=true) = 0;
	virtual bool GeneratePath(FAStar*, int iXstart, int iYstart, int iXdest, int iYdest, bool bCardinalOnly = false, int iInfo = 0, bool bReuse = false) = 0;
	virtual void Initialize(FAStar*, int iColumns, int iRows, bool bWrapX, bool bWrapY, FAPointFunc DestValidFunc, FAHeuristic HeuristicFunc, FAStarFunc CostFunc, FAStarFunc ValidFunc, FAStarFunc NotifyChildFunc, FAStarFunc NotifyListFunc, void *pData) = 0;
	virtual void SetData(FAStar*, const void* pData) = 0;
	virtual FAStarNode *GetLastNode(FAStar*) = 0;
	virtual bool IsPathStart(FAStar*, int iX, int iY) = 0;
	virtual bool IsPathDest(FAStar*, int iX, int iY) = 0;
	virtual int GetStartX(FAStar*) = 0;
	virtual int GetStartY(FAStar*) = 0;
	virtual int GetDestX(FAStar*) = 0;
	virtual int GetDestY(FAStar*) = 0;
	virtual int GetInfo(FAStar*) = 0;
	virtual void ForceReset(FAStar*) = 0;
};

#endif	// CvDLLFAStarIFaceBase_h
