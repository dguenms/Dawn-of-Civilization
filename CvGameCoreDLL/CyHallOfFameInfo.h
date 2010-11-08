#pragma once

#ifndef __CY_HallOfFame_H__
#define __CY_HallOfFame_H__

#include "CvHallOfFameInfo.h"

class CyReplayInfo;

class CyHallOfFameInfo
{
public:
	CyHallOfFameInfo();

	void loadReplays();
	int getNumGames() const;
	CyReplayInfo* getReplayInfo(int i);

private:
	CvHallOfFameInfo m_hallOfFame;
};

#endif __CY_HallOfFame_H__
