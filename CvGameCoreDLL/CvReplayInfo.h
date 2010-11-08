#ifndef CvReplayInfo_H
#define CvReplayInfo_H

#pragma once

#include "CvEnums.h"

class CvReplayMessage;


class CvReplayInfo
{
public:
	DllExport CvReplayInfo();
	DllExport virtual ~CvReplayInfo();

	DllExport void createInfo(PlayerTypes ePlayer);

	DllExport int getActivePlayer() const;
	DllExport LeaderHeadTypes getLeader(int iPlayer = -1) const;
	DllExport ColorTypes getColor(int iPlayer = -1) const;
	DllExport HandicapTypes getDifficulty() const;
	DllExport const CvWString& getLeaderName() const;
	DllExport const CvWString& getCivDescription() const;
	DllExport const CvWString& getShortCivDescription() const;
	DllExport const CvWString& getCivAdjective() const;
	DllExport const CvWString& getMapScriptName() const;
	DllExport WorldSizeTypes getWorldSize() const;
	DllExport ClimateTypes getClimate() const;
	DllExport SeaLevelTypes getSeaLevel() const;
	DllExport EraTypes getEra() const;
	DllExport GameSpeedTypes getGameSpeed() const;
	DllExport bool isGameOption(GameOptionTypes eOption) const;
	DllExport bool isVictoryCondition(VictoryTypes eVictory) const;
	DllExport VictoryTypes getVictoryType() const;
	DllExport bool isMultiplayer() const;

	DllExport void addReplayMessage(CvReplayMessage* pMessage);
	DllExport void clearReplayMessageMap();
	DllExport int getReplayMessageTurn(uint i) const;
	DllExport ReplayMessageTypes getReplayMessageType(uint i) const;
	DllExport int getReplayMessagePlotX(uint i) const;
	DllExport int getReplayMessagePlotY(uint i) const;
	DllExport PlayerTypes getReplayMessagePlayer(uint i) const;
	DllExport const wchar* getReplayMessageText(uint i) const;
	DllExport uint getNumReplayMessages() const;
	DllExport ColorTypes getReplayMessageColor(uint i) const;

	DllExport int getInitialTurn() const;
	DllExport int getFinalTurn() const;
	DllExport int getStartYear() const;
	DllExport const wchar* getFinalDate() const;
	DllExport CalendarTypes getCalendar() const;
	DllExport int getNumPlayers() const;
	DllExport int getPlayerScore(int iPlayer, int iTurn) const;
	DllExport int getPlayerEconomy(int iPlayer, int iTurn) const;
	DllExport int getPlayerIndustry(int iPlayer, int iTurn) const;
	DllExport int getPlayerAgriculture(int iPlayer, int iTurn) const;
	DllExport int getFinalScore() const;
	DllExport int getFinalEconomy() const;
	DllExport int getFinalIndustry() const;
	DllExport int getFinalAgriculture() const;
	DllExport int getNormalizedScore() const;

	DllExport int getMapHeight() const;
	DllExport int getMapWidth() const;
	DllExport const unsigned char* getMinimapPixels() const;

	DllExport const char* getModName() const;

	DllExport bool read(FDataStreamBase& stream);
	DllExport void write(FDataStreamBase& stream);

protected:
	bool isValidPlayer(int i) const;
	bool isValidTurn(int i) const;

	static int REPLAY_VERSION;

	int m_iActivePlayer;
	HandicapTypes m_eDifficulty;
	CvWString m_szLeaderName;
	CvWString m_szCivDescription;
	CvWString m_szShortCivDescription;
	CvWString m_szCivAdjective;

	CvWString m_szMapScriptName;
	WorldSizeTypes m_eWorldSize;
	ClimateTypes m_eClimate;
	SeaLevelTypes m_eSeaLevel;
	EraTypes m_eEra;
	GameSpeedTypes m_eGameSpeed;
	std::vector<GameOptionTypes> m_listGameOptions;
	std::vector<VictoryTypes> m_listVictoryTypes;
	VictoryTypes m_eVictoryType;
	bool m_bMultiplayer;

	typedef std::vector<const CvReplayMessage*> ReplayMessageList;
	ReplayMessageList m_listReplayMessages; 

	int m_iInitialTurn;
	int m_iFinalTurn;
	int m_iStartYear;
	CvWString m_szFinalDate;
	CalendarTypes m_eCalendar;
	int m_iNormalizedScore;

	struct TurnData
	{
		int m_iScore;
		int m_iEconomy;
		int m_iIndustry;
		int m_iAgriculture;
	};
	typedef std::vector<TurnData> ScoreHistory;

	struct PlayerInfo
	{
		LeaderHeadTypes m_eLeader;
		ColorTypes m_eColor;
		ScoreHistory m_listScore;
	};
	typedef std::vector<PlayerInfo> PlayerScoreHistory;
	PlayerScoreHistory m_listPlayerScoreHistory;

	int m_iMapHeight;
	int m_iMapWidth;
	unsigned char* m_pcMinimapPixels;

	int m_nMinimapSize;

	CvString m_szModName;
};

#endif