#include "CvGameCoreDLL.h"
#include "CyHallOfFameInfo.h"
#include "CyReplayInfo.h"

CyHallOfFameInfo::CyHallOfFameInfo()
{
}


void CyHallOfFameInfo::loadReplays()
{
	m_hallOfFame.loadReplays();
}

int CyHallOfFameInfo::getNumGames() const
{
	return m_hallOfFame.getNumGames();
}

CyReplayInfo* CyHallOfFameInfo::getReplayInfo(int i)
{
	return (new CyReplayInfo(m_hallOfFame.getReplayInfo(i)));
}

