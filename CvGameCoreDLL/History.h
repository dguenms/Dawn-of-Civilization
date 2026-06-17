#pragma once

#ifndef HISTORY_H
#define HISTORY_H

/*	advc.004s: Replacing CvTurnScoreMap, which was a stdext::hash_map typedef
	in CvPlayer.h. Since AdvCiv uses player histories for AI decisions, lookup
	needs to be faster. A custom class also allows for a cleaner implementation
	of a moving average. */
class History
{
public:
	History() : m_iMovingAvgSamples(0) {}
	void reset(int iMovingAvgSamples = 0)
	{
		m_iMovingAvgSamples = iMovingAvgSamples;
		m_aiValues.clear();
	}
	void grow(int iSize);
	int size() const { return (int)m_aiValues.size(); }
	int get(int iTurn) const
	{
		FAssertBounds(0, size(), iTurn); // iTurn is in the future or m_eOwner not alive
		return m_aiValues[iTurn];
	}
	int getSafe(int iTurn) const
	{
		if (iTurn >= size())
			return -1;
		return get(iTurn);
	}
	void set(int iTurn, int iValue);
	void read(FDataStreamBase* pStream);
	void write(FDataStreamBase* pStream);

private:
	std::vector<int> m_aiValues; // serialized
	int m_iMovingAvgSamples;
};

#endif
