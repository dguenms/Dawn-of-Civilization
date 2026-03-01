#include "CvGameCoreDLL.h"
#include "BarbarianWeightMap.h"
#include "PlotRadiusIterator.h"
#include "CvGame.h"
#include "CvInfo_GameOption.h"

// advc.304: New implementation file; see comment in header.

int BarbarianWeightMap::get(CvPlot const& kPlot) const
{
	/*	Note: We assume that invalid plots have already been filtered out
		through RandPlotFlags */
	int iWeight = RandPlotWeightMap::getProbWeight(kPlot);
	// <advc.300> Reduced weight for land plots with poor yield
	if (!kPlot.isWater())
	{
		int const iTargetYieldScore = 4;
		int iYieldScore = 0;
		FOR_EACH_ENUM(Yield)
		{
			iYieldScore += (eLoopYield == YIELD_COMMERCE ? 1 : 2) * std::min(
					/*	Kind of costly, but this is still early in the game
						when turns are fast. And using getYield could leak info
						about unrevealed resources. */
					kPlot.calculateNatureYield(eLoopYield, BARBARIAN_TEAM, true),
					kPlot.calculateNatureYield(eLoopYield, BARBARIAN_TEAM, false));
			if (iYieldScore >= iTargetYieldScore)
				break;
		}
		if (iYieldScore < iTargetYieldScore)
		{	/*	A fairly big decrease. Note that activity memory will have
				a bit of a leveling effect. */
			iWeight /= 5;
		}
	} // </advc.300>
	iWeight *= std::max(0, 100
			// Past activity discourages future activity
			- m_activityMap.get(kPlot));
	iWeight /= 100;
	return iWeight;
}


void BarbarianActivityMap::decay()
{
	if (!GC.getGame().isBarbarianCreationEra())
	{
		m_map.reset(); // free memory
		return;
	}
	int const iDecayPercent = (15 * 200) /
			(GC.getInfo(GC.getGame().getGameSpeedType()).getBarbPercent() + 100);
	FOR_EACH_NON_DEFAULT_PAIR(m_map, PlotNum, int)
	{
		perPlotNumVal.second *= 100 - iDecayPercent;
		perPlotNumVal.second /= 100;
		m_map.set(perPlotNumVal.first, perPlotNumVal.second);
	}
}


void BarbarianActivityMap::change(CvPlot const& kPlot, int iChange,
	int iPlotRange)
{
	for (PlotCircleIter itPlot(kPlot, iPlotRange); itPlot.hasNext(); ++itPlot)
	{
		if (itPlot->isWater() == kPlot.isWater())
		{
			m_map.set(itPlot->plotNum(), std::min(iMAX_STR, get(*itPlot) +
					// Geometric progression. Stopping at iPlotRange mainly saves time.
					iChange / std::max(1, itPlot.currPlotDist())));
		}
	}
}
