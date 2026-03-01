#include "CvGameCoreDLL.h"
#include "TeamPathFinder.h"
#include "CvGamePlay.h"
#include "CvInfo_Terrain.h"

// advc.104b: New implementation file; see comment in header.

using namespace TeamPath;

template<Mode eMODE>
void TeamPathFinder<eMODE>::reset(CvTeam const* pWarTarget = NULL, int iMaxPath = -1)
{
	FAssert(pWarTarget != m_pTeam);
	resetNodes();
	m_stepMetric = TeamStepMetric<eMODE>(m_pTeam,
			// Avoid NULL checks down the line
			pWarTarget == NULL ? &GET_TEAM(BARBARIAN_TEAM) : pWarTarget,
			iMaxPath, m_iHeuristicWeight);
}

template<Mode eMODE>
bool TeamStepMetric<eMODE>::canStepThrough(CvPlot const& kPlot) const
{
	if (kPlot.isImpassable())
		return false;
	if (eMODE == LAND)
	{
		if (kPlot.isWater())
			return false;
	}
	TeamTypes const ePlotTeam = kPlot.getTeam();
	if (eMODE == SHALLOW_WATER)
	{
		if (kPlot.getTerrainType() == GC.getWATER_TERRAIN(false) &&
			ePlotTeam != m_pTeam->getID())
		{
			return false;
		}
	}
	/*	The canal check is somewhat expensive; push that down into the
		owned-by-non-enemy branch. */
	bool bCanal = false;
	if (ePlotTeam != NO_TEAM)
	{
		bool const bWar = (m_pTeam->isAtWar(ePlotTeam) ||
				GET_TEAM(ePlotTeam).getMasterTeam() == m_pWarTarget->getMasterTeam());
		/*	(War plans against a team other than the target aren't good enough;
			may well get abandoned. Likewise, defensive pacts of the target could
			get canceled.) */
		if (!bWar)
		{
			if (eMODE != LAND)
			{
				//bCanal = (kPlot.isImproved() && m_pTeam->isBase(kPlot));
				/*	^Just too needlessly slow. We check most of the conditions here
					anyway. As much as I don't like having redundant code ... */
				bCanal = (kPlot.isCity() || (kPlot.isImproved() &&
						GC.getInfo(kPlot.getImprovementType()).isActsAsCity()));
			}
			// I expect that this is the slowest check
			if (!m_pTeam->canPeacefullyEnter(ePlotTeam))
				return false;
		}
	}
	if (eMODE != LAND)
	{
		if (!kPlot.isWater() && !bCanal)
			return false;
	}
	return true;
}

template<Mode eMODE>
bool TeamStepMetric<eMODE>::isValidDest(CvPlot const& kStart, CvPlot const& kDest) const
{
	if (kDest.isImpassable())
		return false;
	if (eMODE == LAND) // Has to be land-only, no impassables.
		return (kStart.sameArea(kDest) && !kDest.isWater());
	if (eMODE == SHALLOW_WATER) // Can't enter non-team deep water
	{
		if (kDest.getTerrainType() == GC.getWATER_TERRAIN(false) &&
			kDest.getTeam() != m_pTeam->getID())
		{
			return false;
		}
	}
	/*	The same-area checks below would miss out on canals connecting water areas.
		Most maps have only one large water area anyway, and lakes can be easily
		handled in client code by checking CvPlot::isCoastalLand(-1). Also, it's
		not going to take the pathfinder long to realize that a lake is a dead-end. */
	if (kStart.isWater())
	{
		if (kDest.isWater())
			return /*kStart.sameArea(kDest)*/ true;
		// May unload onto a coastal land plot (but not pass through)
		FOR_EACH_ADJ_PLOT(kDest)
		{
			if (pAdj->isWater()) //pAdj->sameArea(kStart)
				return true;
		}
		return false;
	}
	// Water movement starting on land: need to be adjacent to water.
	FOR_EACH_ADJ_PLOT2(pAdjStart, kStart)
	{
		if (!pAdjStart->isWater())
			continue;
		//if (pAdjStart->sameArea(kDest))
		if (kDest.isWater())
			return true;
		//if (!kDest.isWater())
		else
		{
			FOR_EACH_ADJ_PLOT2(pAdjDest, kDest)
			{
				if (pAdjDest->isWater()) //pAdjStart->sameArea(*pAdjDest)
					return true;
			}
		}
	}
	return false;
}

template<Mode eMODE>
int TeamStepMetric<eMODE>::cost(CvPlot const& kFrom, CvPlot const& kTo) const
{
	int iCost = GC.getMOVE_DENOMINATOR();
	if (eMODE != LAND)
		return iCost;
	// Enemy routes have no effect
	{
		TeamTypes const eToTeam = kTo.getTeam();
		if (eToTeam != NO_TEAM &&
			(m_pTeam->isAtWar(eToTeam) ||
			GET_TEAM(eToTeam).getMasterTeam() == m_pWarTarget->getMasterTeam()))
		{
			return iCost; 
		}
	}
	{
		TeamTypes const eFromTeam = kFrom.getTeam();
		if (eFromTeam != NO_TEAM &&
			(m_pTeam->isAtWar(eFromTeam) ||
			GET_TEAM(eFromTeam).getMasterTeam() == m_pWarTarget->getMasterTeam()))
		{
			return iCost;
		}
	}
	/*	Don't bother with hills and features. They're only relevant
		when units have multiple moves, i.e. not until the Modern era,
		and, by then, routes will be everywhere.
		Also don't check for river crossings; not worth the effort. */
	RouteTypes const eFromRoute = kFrom.getRouteType();
	/*	To cut another corner, assume that both plots have
		route type eFromRoute. */
	if (eFromRoute != NO_ROUTE && kTo.getRouteType() != NO_ROUTE)
	{
		iCost = GC.getInfo(eFromRoute).getMovementCost() +
				m_pTeam->getRouteChange(eFromRoute);
	}
	return iCost;
}

// Eplicit instantiations ...
#define DO_FOR_EACH_MODE(DO) \
		DO(LAND) \
		DO(ANY_WATER) \
		DO(SHALLOW_WATER)
#define INSTANTIATE_TEAM_PATH_FINDER(eMODE) \
	template class TeamPathFinder<eMODE>;
#define INSTANTIATE_TEAM_STEP_METRIC(eMODE) \
	template class TeamStepMetric<eMODE>;
DO_FOR_EACH_MODE(INSTANTIATE_TEAM_PATH_FINDER)
DO_FOR_EACH_MODE(INSTANTIATE_TEAM_STEP_METRIC)
