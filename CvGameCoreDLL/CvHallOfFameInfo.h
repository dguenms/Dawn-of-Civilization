#ifndef CVHALLOFFAMEINFO_H
#define CVHALLOFFAMEINFO_H

#pragma once

class ReplayInfo;

class CvHallOfFameInfo
{
public:
	CvHallOfFameInfo();
	virtual ~CvHallOfFameInfo();
	void uninit(); // advc.106i

	void loadReplays();
	int getNumGames() const;
	CvReplayInfo* getReplayInfo(int i);

protected:
	std::vector<CvReplayInfo*> m_aReplays;
};

#endif