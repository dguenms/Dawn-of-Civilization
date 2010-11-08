#pragma once

#ifndef __CY_Replay_H__
#define __CY_Replay_H__

#include "CvReplayInfo.h"

class CyReplayInfo
{
public:
	CyReplayInfo();
	CyReplayInfo(CvReplayInfo* pInfo);
	const CvReplayInfo* getReplayInfo() const { return m_pHoF; }
	bool isNone() { return (NULL == m_pHoF); }

	void createInfo(int iPlayer);
	int getActivePlayer() const;
	int getLeader(int iPlayer) const;
	int getColor(int iPlayer) const;
	int getDifficulty() const;
	std::wstring getLeaderName() const;
	std::wstring getCivDescription() const;
	std::wstring getShortCivDescription() const;
	std::wstring getCivAdjective() const;
	std::wstring getMapScriptName() const;
	int getWorldSize() const;
	int getClimate() const;
	int getSeaLevel() const;
	int getEra() const;
	int getGameSpeed() const;
	bool isGameOption(int iOption) const;
	bool isVictoryCondition(int iVictory) const;
	int getVictoryType() const;
	bool isMultiplayer() const;

	int getNumPlayers() const;
	int getPlayerScore(int iPlayer, int iTurn) const;
	int getPlayerEconomy(int iPlayer, int iTurn) const;
	int getPlayerIndustry(int iPlayer, int iTurn) const;
	int getPlayerAgriculture(int iPlayer, int iTurn) const;

	int getNormalizedScore() const;

	int getReplayMessageTurn(int i) const;
	int getReplayMessageType(int i) const;
	int getReplayMessagePlotX(int i) const;
	int getReplayMessagePlotY(int i) const;
	int getReplayMessagePlayer(int i) const;
	const std::wstring getReplayMessageText(int i) const;
	int getNumReplayMessages() const;
	int getReplayMessageColor(int i) const;

	int getInitialTurn() const;
	int getStartYear() const;
	int getFinalTurn() const;
	const std::wstring getFinalDate() const;
	int getCalendar() const;

	int getFinalScore() const;
	int getFinalEconomy() const;
	int getFinalIndustry() const;
	int getFinalAgriculture() const;

	int getMapWidth() const;
	int getMapHeight() const;

	const char* getModName() const;

private:
	CvReplayInfo* m_pHoF;

	CvReplayInfo m_replay;
};

#endif __CY_Replay_H__
