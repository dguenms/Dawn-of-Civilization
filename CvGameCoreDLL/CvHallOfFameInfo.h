#ifndef CVHALLOFFAMEINFO_H
#define CVHALLOFFAMEINFO_H

#pragma once

#include "CvReplayInfo.h"

class CvHallOfFameInfo
{
public:
	CvHallOfFameInfo();
	virtual ~CvHallOfFameInfo();

	void loadReplays();
	int getNumGames() const;
	CvReplayInfo* getReplayInfo(int i);

protected:
	std::vector<CvReplayInfo*> m_aReplays;
};

#endif