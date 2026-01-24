#include "CvGameCoreDLL.h"
#include "FAStarFunc.h"
#include "FAStarNode.h"
#include "GroupPathFinder.h"
#include "CoreAI.h" // for AI war plans

// advc.pf: New implementation file; see comment in header.


BOOL pathDestValid(int iToX, int iToY, void const* pointer, FAStar* finder)
{	// <advc.pf>
	return GroupStepMetric::isValidDest(GC.getMap().getPlot(iToX, iToY),
			*reinterpret_cast<CvSelectionGroup const*>(pointer),
			(MovementFlags)gDLL->getFAStarIFace()->GetInfo(finder)); // </advc.pf>
}


int pathHeuristic(int iFromX, int iFromY, int iToX, int iToY)
{
	return GroupStepMetric::heuristicStepCost(iFromX, iFromY, iToX, iToY);
}


int pathCost(FAStarNode* parent, FAStarNode* node,
	int data, // advc (note): unused
	void const* pointer, FAStar* finder)
{	// <advc.pf>
	return GroupStepMetric::cost(
			GC.getMap().getPlot(parent->m_iX, parent->m_iY),
			GC.getMap().getPlot(node->m_iX, node->m_iY),
			*reinterpret_cast<CvSelectionGroup const*>(pointer),
			(MovementFlags)gDLL->getFAStarIFace()->GetInfo(finder),
			parent->m_iData1, parent->m_iKnownCost == 0); // </advc.pf>
}


BOOL pathValid(FAStarNode* parent, FAStarNode* node, int data, void const* pointer, FAStar* finder)
{
	PROFILE_FUNC();

	if(parent == NULL)
		return TRUE;
	// advc: Was unused (apart from an assertion)
	/*CvPlot* pFromPlot = ...;
	CvPlot* pToPlot = ...;*/
	//pSelectionGroup = ((CvSelectionGroup const*)pointer);
	// K-Mod
	/*CvSelectionGroup const* pSelectionGroup = finder ? (CvSelectionGroup const*)pointer :
			((CvPathSettings const*)pointer)->pGroup;
	int iFlags = finder ? gDLL->getFAStarIFace()->GetInfo(finder) :
			((CvPathSettings const*)pointer)->iFlags;*/
	// K-Mod end
	// <advc.pf>
	CvPlot const& kFrom = GC.getMap().getPlot(parent->m_iX, parent->m_iY);
	CvPlot const& kTo = GC.getMap().getPlot(node->m_iX, node->m_iY);
	CvSelectionGroup const& kGroup = *reinterpret_cast<CvSelectionGroup const*>(pointer);
	MovementFlags eFlags = (MovementFlags)gDLL->getFAStarIFace()->GetInfo(finder);
	if (!GroupStepMetric::isValidStep(kFrom, kTo, kGroup, eFlags))
		return FALSE;
	if (!GroupStepMetric::canStepThrough(kFrom, kGroup, eFlags))
		return FALSE;
	if (!GroupStepMetric::canStepThrough(kFrom, kGroup, eFlags,
		parent->m_iData1, parent->m_iData2))
	{
		return FALSE;
	}
	return TRUE; // </advc.pf>
}


BOOL pathAdd(FAStarNode* parent, FAStarNode* node, int data, void const* pointer, FAStar* finder)
{	// <advc.pf>
	CvSelectionGroup const& kGroup = *reinterpret_cast<CvSelectionGroup const*>(pointer);
	MovementFlags eFlags = (MovementFlags)gDLL->getFAStarIFace()->GetInfo(finder);
	if (data == ASNC_INITIALADD)
	{
		node->setPathTurns(1);
		node->setMoves(GroupStepMetric::initialMoves(kGroup, eFlags));
	}
	else GroupStepMetric::updatePathData(*node, *parent, kGroup, eFlags);
	return TRUE; // </advc.pf>
}


BOOL stepDestValid(int iToX, int iToY, void const* pointer, FAStar* finder)
{
	PROFILE_FUNC();

	CvPlot const& kFrom = GC.getMap().getPlot(
			gDLL->getFAStarIFace()->GetStartX(finder),
			gDLL->getFAStarIFace()->GetStartY(finder));
	CvPlot const& kTo = GC.getMap().getPlot(iToX, iToY);
	if (!kFrom.sameArea(kTo))
		return FALSE;

	return TRUE;
}


BOOL stepValid(FAStarNode* parent, FAStarNode* node,
	int data, // advc (note): unused
	void const* pointer, FAStar* finder)
{
	if (parent == NULL)
		return TRUE;

	CvPlot const& kTo = GC.getMap().getPlot(node->m_iX, node->m_iY);
	if (kTo.isImpassable())
		return FALSE;

	CvPlot const& kFrom = GC.getMap().getPlot(parent->m_iX, parent->m_iY);
	if (!kFrom.sameArea(kTo))
		return FALSE;

	// BETTER_BTS_AI_MOD, Bugfix, 12/12/08, jdog5000: START
	if (GC.getMap().isSeparatedByIsthmus(kFrom, kTo)) // (advc: Moved into new function)
		return FALSE; // BETTER_BTS_AI_MOD: END

	return TRUE;
}


BOOL stepAdd(FAStarNode* parent, FAStarNode* node,
	int data, // advc (note): unused
	void const* pointer, FAStar* finder)
{
	if (data == ASNC_INITIALADD)
		node->m_iData1 = 0;
	else node->m_iData1 = (parent->m_iData1 + 1);
	FAssertMsg(node->m_iData1 >= 0, "invalid Index");
	return TRUE;
}


/*	advc.inl (note): These two functions are only called from the EXE,
	so there's no point in trying to get them inlined. */
int stepHeuristic(int iFromX, int iFromY, int iToX, int iToY)
{
	return stepDistance(iFromX, iFromY, iToX, iToY);
}

int stepCost(FAStarNode* parent, FAStarNode* node, int data, void const* pointer, FAStar* finder)
{
	return 1;
}


BOOL routeValid(FAStarNode* parent, FAStarNode* node,
	int data, // advc (note): unused
	void const* pointer, FAStar* finder)
{
	if (parent == NULL)
		return TRUE;

	CvPlot const& kNewPlot = GC.getMap().getPlot(node->m_iX, node->m_iY);
	PlayerTypes ePlayer = (PlayerTypes)gDLL->getFAStarIFace()->GetInfo(finder);
	if (!kNewPlot.isOwned() || kNewPlot.getTeam() == TEAMID(ePlayer))
	{
		if (kNewPlot.getRouteType() == GET_PLAYER(ePlayer).getBestRoute(&kNewPlot))
			return TRUE;
	}
	return FALSE;
}


BOOL borderValid(FAStarNode* parent, FAStarNode* node, int data, void const* pointer, FAStar* finder)
{
	if (parent == NULL)
		return TRUE;

	PlayerTypes ePlayer = (PlayerTypes)gDLL->getFAStarIFace()->GetInfo(finder);
	if (GC.getMap().getPlot(node->m_iX, node->m_iY).getTeam() == TEAMID(ePlayer))
		return TRUE;

	return FALSE;
}


BOOL areaValid(FAStarNode* parent, FAStarNode* node, int data, void const* pointer, FAStar* finder)
{
	if (parent == NULL)
		return TRUE;

	return ((GC.getMap().getPlot(parent->m_iX, parent->m_iY).isWater() ==
			GC.getMap().getPlot(node->m_iX, node->m_iY).isWater()) ? TRUE : FALSE);
	// (advc.030 takes care of this)
	// BETTER_BTS_AI_MOD, General AI, 10/02/09, jdog5000
	// BBAI TODO: Why doesn't this work to break water and ice into separate area?
	/*if (GC.getMap().plotSoren(parent->m_iX, parent->m_iY)->isWater() != GC.getMap().plotSoren(node->m_iX, node->m_iY)->isWater())
	return FALSE;
	// Ice blocks become their own area
	if (GC.getMap().plotSoren(parent->m_iX, parent->m_iY)->isWater() && GC.getMap().plotSoren(node->m_iX, node->m_iY)->isWater()) {
		if (GC.getMap().plotSoren(parent->m_iX, parent->m_iY)->isImpassable() != GC.getMap().plotSoren(node->m_iX, node->m_iY)->isImpassable())
			return FALSE;
	}
	return TRUE;*/
}


BOOL joinArea(FAStarNode* parent, FAStarNode* node, int data, void const* pointer, FAStar* finder)
{
	if (data == ASNL_ADDCLOSED)
	{
		CvMap const& kMap = GC.getMap();
		kMap.getPlot(node->m_iX, node->m_iY).setArea(
				kMap.getArea(gDLL->getFAStarIFace()->GetInfo(finder)));
	}
	return TRUE;
}


BOOL plotGroupValid(FAStarNode* parent, FAStarNode* node,
	int data, // advc (note): unused
	void const* pointer, FAStar* finder)
{
	//PROFILE_FUNC(); // advc.003o
	if (parent == NULL)
		return TRUE;

	CvPlot const& kOldPlot = GC.getMap().getPlot(parent->m_iX, parent->m_iY);
	CvPlot const& kNewPlot = GC.getMap().getPlot(node->m_iX, node->m_iY);

	PlayerTypes const ePlayer = (PlayerTypes)gDLL->getFAStarIFace()->GetInfo(finder);
	TeamTypes const eTeam = TEAMID(ePlayer);
	if (kOldPlot.isSamePlotGroup(kNewPlot, ePlayer) &&
		kNewPlot.isTradeNetwork(eTeam) &&
		kNewPlot.isTradeNetworkConnected(kOldPlot, eTeam))
	{
		return TRUE;
	}
	return FALSE;
}


BOOL countPlotGroup(FAStarNode* parent, FAStarNode* node, int data, void const* pointer, FAStar* finder)
{
	if (data == ASNL_ADDCLOSED)
		(*((int*)pointer))++;
	return TRUE;
}


BOOL potentialIrrigation(FAStarNode* parent, FAStarNode* node, int data, void const* pointer, FAStar* finder)
{
	if (parent == NULL)
		return TRUE;
	return (GC.getMap().getPlot(node->m_iX, node->m_iY).isPotentialIrrigation() ? TRUE : FALSE);
}


BOOL checkFreshWater(FAStarNode* parent, FAStarNode* node, int data, void const* pointer, FAStar* finder)
{
	if (data == ASNL_ADDCLOSED)
	{
		if (GC.getMap().getPlot(node->m_iX, node->m_iY).isFreshWater())
			*((bool *)pointer) = true;
	}
	return TRUE;
}


BOOL changeIrrigated(FAStarNode* parent, FAStarNode* node, int data, void const* pointer, FAStar* finder)
{
	if (data == ASNL_ADDCLOSED)
		GC.getMap().getPlot(node->m_iX, node->m_iY).setIrrigated(*((bool*)pointer));
	return TRUE;
}
