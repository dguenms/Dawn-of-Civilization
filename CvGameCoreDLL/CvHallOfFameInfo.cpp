#include "CvGameCoreDLL.h"
#include "CvHallOfFameInfo.h"
#include "CvReplayInfo.h"
#include "CvGame.h"

CvHallOfFameInfo::CvHallOfFameInfo()
{
	GC.getGame().setHallOfFame(this); // advc.106i
}

CvHallOfFameInfo::~CvHallOfFameInfo()
{	// <advc.106i>
	uninit();
}

void CvHallOfFameInfo::uninit()
{
	GC.getGame().setHallOfFame(NULL);
	CvGlobals::getInstance().setHoFScreenUp(false);
	for(size_t i = 0; i < m_aReplays.size(); i++)
		SAFE_DELETE(m_aReplays[i]);
	m_aReplays.clear();
} // </advc.106i>

void CvHallOfFameInfo::loadReplays()
{
	CvGlobals::getInstance().setHoFScreenUp(true); // advc.106i
	gDLL->loadReplays(m_aReplays);
}

int CvHallOfFameInfo::getNumGames() const
{
	return (int)m_aReplays.size();
}

CvReplayInfo* CvHallOfFameInfo::getReplayInfo(int i)
{
	return m_aReplays[i];
}