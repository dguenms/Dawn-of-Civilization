#ifndef CvReplayInfo_H
#define CvReplayInfo_H

#pragma once

class CvReplayMessage;

class CvReplayInfo
{
	CvReplayInfo& operator=(CvReplayInfo const&); // advc.003k (private)
public:
	CvReplayInfo(CvReplayInfo const&); // advc.003k
	DllExport CvReplayInfo();
	virtual ~CvReplayInfo();

	void createInfo(PlayerTypes ePlayer);

	PlayerTypes getActivePlayer() const;
	LeaderHeadTypes getLeader(PlayerTypes ePlayer = NO_PLAYER) const;
	ColorTypes getColor(PlayerTypes ePlayer = NO_PLAYER) const;
	HandicapTypes getDifficulty() const;
	const CvWString& getLeaderName() const;
	const CvWString& getCivDescription() const;
	const CvWString& getShortCivDescription() const;
	const CvWString& getCivAdjective() const;
	const CvWString& getMapScriptName() const;
	WorldSizeTypes getWorldSize() const;
	ClimateTypes getClimate() const;
	SeaLevelTypes getSeaLevel() const;
	EraTypes getEra() const;
	GameSpeedTypes getGameSpeed() const;
	bool isGameOption(GameOptionTypes eOption) const;
	bool isVictoryCondition(VictoryTypes eVictory) const;
	VictoryTypes getVictoryType() const;
	bool isMultiplayer() const;

	void addReplayMessage(CvReplayMessage* pMessage);
	void clearReplayMessageMap();
	int getReplayMessageTurn(uint i) const;
	ReplayMessageTypes getReplayMessageType(uint i) const;
	int getReplayMessagePlotX(uint i) const;
	int getReplayMessagePlotY(uint i) const;
	PlayerTypes getReplayMessagePlayer(uint i) const;
	const wchar* getReplayMessageText(uint i) const;
	uint getNumReplayMessages() const;
	ColorTypes getReplayMessageColor(uint i) const;

	int getInitialTurn() const;
	int getFinalTurn() const;
	int getStartYear() const;
	const wchar* getFinalDate() const;
	CalendarTypes getCalendar() const;
	int getNumPlayers() const;
	int getPlayerScore(int iPlayer, int iTurn) const;
	int getPlayerEconomy(int iPlayer, int iTurn) const;
	int getPlayerIndustry(int iPlayer, int iTurn) const;
	int getPlayerAgriculture(int iPlayer, int iTurn) const;
	int getFinalScore() const;
	// <advc.707>
	void setFinalScore(int iScore);
	int getFinalPlayerScore() const; // </advc.707>
	int getFinalEconomy() const;
	int getFinalIndustry() const;
	int getFinalAgriculture() const;
	int getNormalizedScore() const;

	DllExport int getMapHeight() const;
	DllExport int getMapWidth() const;
	DllExport const unsigned char* getMinimapPixels() const;
	int getMinimapSize() const; // advc.106m: for expo to Python
	static int minimapPixels(int iMinimapSize); // advc.106m
	// advc.106h: (exposed to Python for advc.savem through CyMap::getSettingsString)
	void appendSettingsMsg(CvWString& szSettings, PlayerTypes ePlayer) const;

	DllExport const char* getModName() const;

	DllExport bool read(FDataStreamBase& stream);
	void write(FDataStreamBase& stream);

protected:
	bool isValidPlayer(int i) const;
	bool isValidTurn(int i) const;
	bool isReplayMsgValid(uint i) const; // advc
	// <advc.106m>
	int minimapPixels() const;
	void setDefaultMinimapSize();
	void setMinimapSizeFromXML(); // </advc.106m>
	void addSettingsMsg(); // advc.106h
	// <advc.106i>
	bool checkBounds(int iValue, int iLower, int iUpper) const;
	bool isStoringReplaysAsBtS() const;
	// </advc.106i>
	static int REPLAY_VERSION;

	PlayerTypes m_eActivePlayer;
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
	//int m_iNormalizedScore;
	// <advc.003k> Additional data members
	class Data
	{
		int iNormalizedScore; // (moved into Data to make room for Data* m)
		int iFinalScore; // advc.707
		// <advc.106i>
		int iVersionRead;
		bool bDisplayOtherMods;
		// </advc.106i>
		friend CvReplayInfo;
	};
	Data* m;
	// </advc.003k>
	struct TurnData
	{
		int m_iScore;
		int m_iEconomy;
		int m_iIndustry;
		int m_iAgriculture;
	};
	typedef std::vector<TurnData> ScoreHistory;
	TurnData const& getTurnData(int iPlayer, int iTurn) const; // advc

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
	int m_iMinimapSize;
	byte const* m_pcMinimapPixels; // advc.106n: const

	CvString m_szModName;
};
BOOST_STATIC_ASSERT(sizeof(CvReplayInfo) == 336); // advc.003k

#endif
