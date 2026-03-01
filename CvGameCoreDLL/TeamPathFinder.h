#pragma once

#ifndef TEAM_PATH_FINDER_H
#define TEAM_PATH_FINDER_H

#include "KmodPathFinder.h"
#include "CvMap.h" // for inlining heuristicCost

/*	advc.104b: Pathfinder for hypothetical units of a team.
	Primarily for AI war planning.
	Takes into account foreign borders, terrain and routes.
	(On terrain and routes, some corners are cut to reduce computing time;
	see comments in the cost function.)
	Visibility is not checked - if the user ensures that destinations are
	revealed or can at least be deduced, then it's not too much of a cheat to
	assume that the shortest path is revealed or can be deduced as well.
	The cost of a path is the sum of the movement costs along the path
	scaled by MOVE_DENOMINATOR.
	The length of a path is the number of plots entered (not counting the start),
	i.e. the speed (base moves) of the units doesn't matter and no travel time
	(number of turns) is computed. */

class CvTeam;

namespace TeamPath
{
	enum Mode
	{	// Assume that the moving unit is ...
		/*	... a land unit that can move through all land terrain that isn't
			categorically impassable, can't enter water, can use routes. */
		LAND,
		/*	... a sea unit that can move through all water terrain at a uniform cost
			unless it is categorically impassable, can't move through land unless
			a city or improvement acts as a canal, and may have a coastal land plot
			as its destination. No extra cost is counted for loading and unloading
			of cargo. */
		ANY_WATER,
		SHALLOW_WATER, // Like ANY_WATER but mustn't enter deep water
		// (and all moves have to respect borders unless war is assumed)
	};
};

template<TeamPath::Mode eMODE> // Want to know at compile time for performance reasons
class TeamStepMetric : public StepMetricBase<PathNode>
{
public:
	TeamStepMetric(CvTeam const* pTeam = NULL,
		CvTeam const* pWarTarget = NULL,
		int iMaxPath = -1, int iHeuristicWeight = -1)
	:	StepMetricBase<PathNode>(iMaxPath),
		m_pTeam(pTeam), m_pWarTarget(pWarTarget),
		m_iHeuristicWeight(iHeuristicWeight)
	{}
	int heuristicCost(CvPlot const& kFrom, CvPlot const& kTo) const
	{
		return stepDistance(kFrom.getX(), kFrom.getY(), kTo.getX(), kTo.getY()) *
				m_iHeuristicWeight;
	}
	int initialPathLength() const { return 0; }
	void initializePathData(PathNode& kNode) const
	{	// (Same as base class, but calling TeamStepMetric::initialPathLength)
		kNode.setPathLength(initialPathLength());
	}
	bool isValidStep(CvPlot const& kFrom, CvPlot const& kTo) const
	{
		if (eMODE != TeamPath::LAND)
		{
			if (GC.getMap().isSeparatedByIsthmus(kFrom, kTo))
				return false;
		}
		return true;
	}
	bool canStepThrough(CvPlot const& kPlot) const;
	bool canStepThrough(CvPlot const& kPlot, PathNode const& kNode) const
	{	// No path data to be taken into account
		return true;
	}
	bool isValidDest(CvPlot const& kStart, CvPlot const& kDest) const;
	int cost(CvPlot const& kFrom, CvPlot const& kTo,
		PathNode const& kParentNode) const
	{
		return cost(kFrom, kTo); // disregard kParentNode
	}
	int cost(CvPlot const& kFrom, CvPlot const& kTo) const;
protected:
	CvTeam const* m_pTeam;
	CvTeam const* m_pWarTarget;
	int m_iHeuristicWeight;
};

template<TeamPath::Mode eMODE>
class TeamPathFinder : public KmodPathFinder<TeamStepMetric<eMODE> >
{
public:
	TeamPathFinder(CvTeam const& kTeam, CvTeam const* pWarTarget = NULL,
		int iMaxPath = -1)
	{
		init(kTeam, pWarTarget, iMaxPath);
	}
	void reset(CvTeam const* pWarTarget = NULL, int iMaxPath = -1);
	/*	ctor allowing m_pTeam to be set later so that different teams
		can use the same node map w/o memory reallocation */
	TeamPathFinder() : m_pTeam(NULL), m_iHeuristicWeight(-1) {}
	void init(CvTeam const& kTeam, CvTeam const* pWarTarget = NULL,
		int iMaxPath = -1)
	{
		m_pTeam = &kTeam;
		if (eMODE == TeamPath::LAND)
			m_iHeuristicWeight = minimumStepCost(1);
		else
		{	// Assume that water movement has uniform cost
			m_iHeuristicWeight = GC.getMOVE_DENOMINATOR();
		}
		reset(pWarTarget, iMaxPath);
	}
	int getPathCost() const
	{
		return m_pEndNode->m_iTotalCost;
	}
protected:
	CvTeam const* m_pTeam;
	int m_iHeuristicWeight;
};

class TeamPathFinders // For code that needs all three (and for forward declarations)
{
public:
	TeamPathFinders(
		TeamPathFinder<TeamPath::LAND>& kLandFinder,
		TeamPathFinder<TeamPath::ANY_WATER>& kAnyWaterFinder,
		TeamPathFinder<TeamPath::SHALLOW_WATER>& kShallowWaterFinder)
	:	m_kLandFinder(kLandFinder),
		m_kAnyWaterFinder(kAnyWaterFinder),
		m_kShallowWaterFinder(kShallowWaterFinder)
	{}
	TeamPathFinder<TeamPath::LAND>& landFinder() const
	{
		return m_kLandFinder;
	}
	TeamPathFinder<TeamPath::ANY_WATER>& anyWaterFinder() const
	{
		return m_kAnyWaterFinder;
	}
	TeamPathFinder<TeamPath::SHALLOW_WATER>& shallowWaterFinder() const
	{
		return m_kShallowWaterFinder;
	}
private:
	TeamPathFinder<TeamPath::LAND>& m_kLandFinder;
	TeamPathFinder<TeamPath::ANY_WATER>& m_kAnyWaterFinder;
	TeamPathFinder<TeamPath::SHALLOW_WATER>& m_kShallowWaterFinder;
};

// Work around the lack of runtime polymorphism
class TeamWaterPathFinder
{
public:
	TeamWaterPathFinder(CvTeam const& kTeam, CvTeam const* pWarTarget = NULL,
		int iMaxPath = -1)
	{
		// (These aren't expensive)
		m_pAnyWaterFinder = new TeamPathFinder<TeamPath::ANY_WATER>(
				kTeam, pWarTarget, iMaxPath);
		m_pShallowWaterFinder = new TeamPathFinder<TeamPath::SHALLOW_WATER>(
				kTeam, pWarTarget, iMaxPath);
	}
	~TeamWaterPathFinder()
	{
		delete m_pAnyWaterFinder;
		delete m_pShallowWaterFinder;
	}
	TeamPathFinder<TeamPath::ANY_WATER>& anyWaterFinder()
	{
		return *m_pAnyWaterFinder;
	}
	TeamPathFinder<TeamPath::SHALLOW_WATER>& shallowWaterFinder()
	{
		return *m_pShallowWaterFinder;
	}
private:
	TeamPathFinder<TeamPath::ANY_WATER>* m_pAnyWaterFinder;
	TeamPathFinder<TeamPath::SHALLOW_WATER>* m_pShallowWaterFinder;
};

#endif
