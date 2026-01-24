#pragma once
#ifndef BARBARIAN_WEIGHT_MAP_H
#define BARBARIAN_WEIGHT_MAP_H

/*	advc.304: Memory of Barbarian activity and (based on that past activity)
	weight distribution for future Barbarian activity. */

#include "CvMap.h"

class FDataStreamBase;

class BarbarianActivityMap
{
public:
	void reset()
	{
		m_map.reset();
	}
	void read(FDataStreamBase* pStream) { m_map.read(pStream); }
	void write(FDataStreamBase* pStream) const { m_map.write(pStream); }
	int get(CvPlot const& kPlot) const
	{
		return m_map.get(kPlot.plotNum());
	}
	void decay();
	void change(CvPlot const& kPlot, int iChange = iMAX_STR, int iPlotRange = 5);
	static int maxStrength() { return iMAX_STR; }

private:
	ArrayEnumMap<PlotNumTypes,int,short> m_map;
	/*	120 is more easily divisible than 100. CvGame will trigger decay
		before placing Barbarian units, so the max strength will be ca. 100 then. */
	static int const iMAX_STR = 120;
};

class BarbarianWeightMap : public RandPlotWeightMap
{
public:
	int getProbWeight(CvPlot const& kPlot) const // override
	{
		return get(kPlot);
	}
	int get(CvPlot const& kPlot) const;
	BarbarianActivityMap& getActivityMap() { return m_activityMap; }
	BarbarianActivityMap const& getActivityMap() const { return m_activityMap; }

private:
	BarbarianActivityMap m_activityMap;
};

#endif
