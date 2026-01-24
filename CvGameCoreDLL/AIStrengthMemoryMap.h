#pragma once

#ifndef AI_STRENGTH_MEMORY_MAP_H
#define AI_STRENGTH_MEMORY_MAP_H

/*	advc.158: New class based on K-Mod code cut from CvTeamAI.
	"K-Mod. Strength Memory - a very basic and rough reminder-map
	of how strong the enemy presence is on each plot. [...]
	Should not be used by human players because it may cause OOS errors."
	The only problem I'm seeing is that the human pathfinder mustn't update
	strength memory; but that doesn't mean human civs can't have strength memory
	at all. It's nice to have for situations when the AI takes over for a human. */
class AIStrengthMemoryMap
{
	//std::vector<int> m_aiMap;
	/*	It's a pretty sparse map, often entirely empty.
		K-Mod had used a std::vector, which was faster than std::map in my tests,
		but not quite as fast as hash_map. I'm keeping the vector code in comments.
		(Haven't tried ListEnumMap b/c that class didn't exist yet.) */
	typedef stdext::hash_map<PlotNumTypes,int> PlotStrengthMap;
	PlotStrengthMap m_map;
	TeamTypes m_eTeam;
public:
	AIStrengthMemoryMap() : m_eTeam(NO_TEAM) {}
	void init(PlotNumTypes eMapSize, TeamTypes eTeam);
	void reset();
	void decay();
	void read(FDataStreamBase* pStream, uint uiFlag, TeamTypes eTeam);
	void write(FDataStreamBase* pStream) const;
	int get(PlotNumTypes ePlot) const
	{
		/*FAssertBounds(0, m_aiMap.size(), ePlot);
		return m_aiMap[ePlot];*/
		PlotStrengthMap::const_iterator pos = m_map.find(ePlot);
		return (pos != m_map.end() ? pos->second : 0);
	}
	int get(CvPlot const& kPlot) const;
	void set(CvPlot const& kPlot, int iNewValue);
};

#endif
