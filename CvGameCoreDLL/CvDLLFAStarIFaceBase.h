#pragma once

#ifndef CvDLLFAStarIFaceBase_h
#define CvDLLFAStarIFaceBase_h

// abstract interface for FAStar functions used by DLL

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
	virtual bool GeneratePath(FAStar*, int iStartX, int iStartY, int iDestX, int iDestY,
			bool bCardinalOnly = false, int iInfo = 0, bool bReuse = false) = 0;
	virtual void Initialize(FAStar*, int iColumns, int iRows, bool bWrapX, bool bWrapY,
			FAPointFunc DestValidFunc, FAHeuristic HeuristicFunc, FAStarFunc CostFunc,
			FAStarFunc ValidFunc, FAStarFunc NotifyChildFunc, FAStarFunc NotifyListFunc,
			void* pData) = 0;
	virtual void SetData(FAStar*, void const* pData) = 0;
	virtual FAStarNode* GetLastNode(FAStar*) = 0;
	virtual bool IsPathStart(FAStar*, int iX, int iY) = 0;
	virtual bool IsPathDest(FAStar*, int iX, int iY) = 0;
	virtual int GetStartX(FAStar*) = 0;
	virtual int GetStartY(FAStar*) = 0;
	virtual int GetDestX(FAStar*) = 0;
	virtual int GetDestY(FAStar*) = 0;
	virtual int GetInfo(FAStar*) = 0;
	virtual void ForceReset(FAStar*) = 0;
};

/*	advc.pf: FAStar is defined in the EXE, but we can take a guess at its
	memory layout. This could be used (perhaps, not tested) to let GroupPathFinder
	overwrite the result of the FAStar instance used for the waypoints on the main map
	(through reinterpret_cast<FAStarData*>(pFinder)->overwritePath(pEndNode)).
	Should then also try to cut the FAStar calculation short by temporarily
	setting DestX/Y to StartX/Y.
	I've added the getters just to illustrate the conjectured relation with
	CvDLLFAStarIFaceBase. */
#if 0
class FAStarData
{
public:
	void overwritePath(FAStarNode* pNewLastNode) { m_pLastNode = pNewLastNode; }
	FAStarNode* getLastNode() const { return m_pLastNode; }
	void setData(void const* pData) { m_pData = pData; }
	int getInfo() const { return m_iInfo; }
	int getStartX() const { return m_iStartX; }
	int getStartY() const { return m_iStartY; }
	int getDestX() const { return m_iDestX; }
	int getDestY() const { return m_iDestY; }
	bool isPathStart(int iX, int iY) const { return (m_iStartX == iX && m_iStartY == iY); }
	bool isPathDest(int iX, int iY) const { return (m_iDestX == iX && m_iDestY == iY); }
private:
	// The function pointers that were passed to CvDLLFAStarIFaceBase::Initialize
	void* m_pPathFuncs[5];
	/*	I've only seen 0 here. Easy enough to verify that these bytes get set
		by setData, but I haven't done so. */
	void const* m_pData;
	/*	I've seen e.g. 214452064 and similarly high numbers. Could've been
		group movement flags I guess, but I haven't verified that. */
	int m_iInfo;
	int m_iMapWidth;
	int m_iMapHeight;
	// Start, Dest: likely ...
	int m_iStartX;
	int m_iStartY;
	int m_iDestX;
	int m_iDestY;
	int m_iUnknown1; // I've seen 8
	int m_iUnknown2; // I've seen 1 (bool?)
	/*	I really don't know how the nodes are arranged. Probably there is an
		array of all nodes, and probably the end node is stored separately.
		In my (very few) tests, pLastNode and pNodes were pointing to the
		node returned by CvDLLFAStarIFaceBase::GetLastNode. */
	FAStarNode* m_pSomeNode; // ?
	FAStarNode* m_pLastNode;
	FAStarNode* m_pNodes;
};
#endif

#endif
