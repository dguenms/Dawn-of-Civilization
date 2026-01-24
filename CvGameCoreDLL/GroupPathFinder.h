#pragma once

#ifndef GROUP_PATH_FINDER_H
#define GROUP_PATH_FINDER_H

#include "KmodPathFinder.h"
#include "CvMap.h" // for inlining heuristicStepCost
#include "KmodPathFinderLegacy.h" // advc.test

/*	advc.pf: New header for classes implementing an A* pathfinder for
	selection groups of units. Mostly pre-AdvCiv code, just organized differently. */

class GroupPathNode : public PathNodeBase<GroupPathNode>
{
private:
	/*	Number of moves remaining to the unit with the fewest moves in the group.
		Corresponds to FAStarNode::m_iData1 in K-Mod. */
	int m_iMoves; // (short would suffice - but wouldn't help currently b/c of padding)
public:
	int getMoves() const
	{
		return m_iMoves;
	}
	void setMoves(int iMoves)
	{
		m_iMoves = iMoves;
	}
	// Aliases; to give path length a more specific name.
	int getPathTurns() const
	{
		return getPathLength();
	}
	void setPathTurns(int iPathTurns)
	{
		setPathLength(iPathTurns);
	}
};

class CvSelectionGroup;
#define PATH_MOVEMENT_WEIGHT (1024) // advc.opt: was 1000

class GroupStepMetric : public StepMetricBase<GroupPathNode>
{
public:
/*	static interface so that GroupStepMetric can share code with the
	FAStar pathfinder in the EXE */
	static bool isValidStep(CvPlot const& kFrom, CvPlot const& kTo,
			CvSelectionGroup const& kGroup, MovementFlags eFlags);
	static bool canStepThrough(CvPlot const& kFrom, CvSelectionGroup const& kGroup,
			MovementFlags eFlags);
	static bool canStepThrough(CvPlot const& kFrom, CvSelectionGroup const& kGroup,
			MovementFlags eFlags, int iMoves, int iPathTurns);
	static bool isValidDest(CvPlot const& kPlot, CvSelectionGroup const& kGroup,
			MovementFlags eFlags);
	static int cost(CvPlot const& kFrom, CvPlot const& kTo,
			CvSelectionGroup const& kGroup, MovementFlags eFlags,
			int iCurrMoves, bool bAtStart);
	static int heuristicStepCost(int iFromX, int iFromY, int iToX, int iToY)
	{
		return stepDistance(iFromX, iFromY, iToX, iToY) * PATH_MOVEMENT_WEIGHT;
	}
	/*	The K-Mod code for updating path data is pretty intrusive; needs to
		have access to the node objects. */
	template<class Node> // GroupPathNode or FAStarNode
	static bool updatePathData(Node& kNode, Node const& kParent,
			CvSelectionGroup const& kGroup, MovementFlags eFlags);
	static int initialMoves(CvSelectionGroup const& kGroup, MovementFlags eFlags);

// Non-static interface ...
	GroupStepMetric(CvSelectionGroup const* pGroup = NULL,
		MovementFlags eFlags = NO_MOVEMENT_FLAGS, int iMaxPath = -1,
		int iHeuristicWeight = -1)
	:	StepMetricBase<GroupPathNode>(iMaxPath), m_pGroup(pGroup),
		m_eFlags(eFlags), m_iHeuristicWeight(iHeuristicWeight)
	{}
	CvSelectionGroup const* getGroup() const
	{
		return m_pGroup;
	}
	MovementFlags getFlags() const
	{
		return m_eFlags;
	}
	int getHeuristicWeight() const
	{
		return m_iHeuristicWeight;
	}
	bool isValidStep(CvPlot const& kFrom, CvPlot const& kTo) const
	{
		return isValidStep(kFrom, kTo, *m_pGroup, m_eFlags);
	}
	bool canStepThrough(CvPlot const& kPlot) const
	{
		return canStepThrough(kPlot, *m_pGroup, m_eFlags);
	}
	bool canStepThrough(CvPlot const& kPlot, GroupPathNode const& kNode) const
	{
		return canStepThrough(kPlot, *m_pGroup, m_eFlags,
				kNode.getMoves(), kNode.getPathTurns());
	}
	bool isValidDest(CvPlot const& kStart, CvPlot const& kDest) const
	{
		return isValidDest(kDest, *m_pGroup, m_eFlags);
	}
	int cost(CvPlot const& kFrom, CvPlot const& kTo,
		GroupPathNode const& kParentNode) const
	{
		return cost(kFrom, kTo, *m_pGroup, m_eFlags,
				kParentNode.getMoves(), kParentNode.m_iKnownCost == 0);
	}
	int heuristicCost(CvPlot const& kFrom, CvPlot const& kTo) const
	{
		return heuristicStepCost(kFrom.getX(), kFrom.getY(), kTo.getX(), kTo.getY()) *
				m_iHeuristicWeight;
	}
	bool updatePathData(GroupPathNode& kNode, GroupPathNode const& kParent) const
	{
		return updatePathData(kNode, kParent, *m_pGroup, m_eFlags);
	}
	void initializePathData(GroupPathNode& kNode) const
	{
		StepMetricBase<GroupPathNode>::initializePathData(kNode);
		kNode.setMoves(initialMoves(*m_pGroup, m_eFlags));
	}
	bool canReuseInitialPathData(GroupPathNode const& kStart) const;

protected:
	CvSelectionGroup const* m_pGroup;
	MovementFlags m_eFlags;
	int m_iHeuristicWeight;
};


class GroupPathFinder : public KmodPathFinder<GroupStepMetric, GroupPathNode>,
	private boost::noncopyable
{
public:
	void invalidateGroup(CvSelectionGroup const& kGroup);
	void setGroup( // was "SetSettings"
			CvSelectionGroup const& kGroup,
			MovementFlags eFlags = NO_MOVEMENT_FLAGS,
			int iMaxPath = -1, int iHeuristicWeight = -1);
	bool generatePath(CvPlot const& kTo);
	#if VERIFY_PATHF == 0 // advc.test
	// Unhide 2-argument version
	using KmodPathFinder<GroupStepMetric,GroupPathNode>::generatePath;
	int getPathTurns() const { return getPathLength(); }
	#endif // advc.test
	CvPlot& getPathEndTurnPlot() const;
	int getFinalMoves() const
	{
		if (m_pEndNode == NULL)
		{
			FAssert(m_pEndNode != NULL);
			return 0;
		}
		return m_pEndNode->getMoves();
	}
	/*	advc (tbd.): Remove this function so that GroupPathNode is fully encapasulated.
		Cf. comment in CvUnitAI::AI_considerPathDOW (the only call location). */
	GroupPathNode* getEndNode() const
	{	// Note: the returned pointer becomes invalid if the pathfinder is destroyed.
		FAssert(m_pEndNode != NULL);
		return m_pEndNode;
	}
	// <advc.test>
	#if VERIFY_PATHF
	bool generatePath(CvPlot const& kFrom, CvPlot const& kTo);
	int getPathTurns() const
	{
		int iTurns = getPathLength();
		FAssert(iTurns == kLegacyPathf.GetPathTurns());
		return iTurns;
	}
	void reset()
	{
		KmodPathFinder<GroupStepMetric, GroupPathNode>::reset();
		kLegacyPathf.Reset();
	}
	CvPlot& getPathFirstPlot() const
	{
		CvPlot& kPlot = KmodPathFinder<GroupStepMetric, GroupPathNode>::getPathFirstPlot();
		FAssert(&kPlot == kLegacyPathf.GetPathFirstPlot());
		return kPlot;
	}
	static void initHeuristicWeights(int iMinMovementCost, int iMinFlatMovementCost)
	{
		KmodPathFinderLegacy::InitHeuristicWeights();
		KmodPathFinder<GroupStepMetric,GroupPathNode>::initHeuristicWeights(
				iMinMovementCost, iMinFlatMovementCost);
	}
private:
	KmodPathFinderLegacy kLegacyPathf;
	#endif // <advc.test>
};

#endif
