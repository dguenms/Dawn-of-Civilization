#pragma once

#ifndef SHELF_H
#define SHELF_H

class CvPlot;
class CvUnit;
class RandPlotWeightMap; // (see CvMap::syncRandPlot)
enum RandPlotFlags;

/*	advc.300: New class representing a continental shelf, akin to a CvArea
	(but inheriting from that class isn't practical).
	For spawning Barbarian sea units. */
class Shelf
{
public:
	typedef std::pair<int,int> Id;

	void add(CvPlot* pPlot);
	CvPlot* randomPlot(RandPlotFlags eRestrictions, int iUnitDistance,
			int* piValidCount = NULL, RandPlotWeightMap const* pWeights = NULL) const;
	int size() const { return (int)m_apPlots.size(); }
	int countUnownedPlots() const;
	int countBarbarians() const;
	CvUnit* randomBarbarianTransport() const; // advc.306
	bool killBarbarian(); // Just any one Barbarian ship; false if none.

private:
	std::vector<CvPlot*> m_apPlots;
};

#endif
