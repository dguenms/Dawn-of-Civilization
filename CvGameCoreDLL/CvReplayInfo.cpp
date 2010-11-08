#include "CvGameCoreDLL.h"
#include "CvReplayInfo.h"
#include "CvInfos.h"
#include "CvGlobals.h"
#include "CvGameAI.h"
#include "CvPlayerAI.h"
#include "CvMap.h"
#include "CvReplayMessage.h"
#include "CvGameTextMgr.h"
#include "CvDLLInterfaceIFaceBase.h"
#include "CvInitCore.h"

int CvReplayInfo::REPLAY_VERSION = 4;

CvReplayInfo::CvReplayInfo() :
	m_iActivePlayer(0),
	m_eDifficulty(NO_HANDICAP),
	m_eWorldSize(NO_WORLDSIZE),
	m_eClimate(NO_CLIMATE),
	m_eSeaLevel(NO_SEALEVEL),
	m_eEra(NO_ERA),
	m_eGameSpeed(NO_GAMESPEED),
	m_iInitialTurn(0),
	m_iFinalTurn(0),
	m_eVictoryType(NO_VICTORY),
	m_iMapHeight(0),
	m_iMapWidth(0),
	m_pcMinimapPixels(NULL),
	m_iNormalizedScore(0),
	m_bMultiplayer(false),
	m_iStartYear(0)
{
	m_nMinimapSize = ((GC.getDefineINT("MINIMAP_RENDER_SIZE") * GC.getDefineINT("MINIMAP_RENDER_SIZE")) / 2); 
}

CvReplayInfo::~CvReplayInfo()
{
	ReplayMessageList::const_iterator it;
	for (uint i = 0; i < m_listReplayMessages.size(); i++)
	{
		SAFE_DELETE(m_listReplayMessages[i]);
	}
	SAFE_DELETE(m_pcMinimapPixels);
}

void CvReplayInfo::createInfo(PlayerTypes ePlayer)
{
	CvGame& game = GC.getGameINLINE();
	CvMap& map = GC.getMapINLINE();

	if (ePlayer == NO_PLAYER)
	{
		ePlayer = game.getActivePlayer();
	}
	if (NO_PLAYER != ePlayer)
	{
		CvPlayer& player = GET_PLAYER(ePlayer);

		m_eDifficulty = player.getHandicapType();
		m_szLeaderName = player.getName();
		m_szCivDescription = player.getCivilizationDescription();
		m_szShortCivDescription = player.getCivilizationShortDescription();
		m_szCivAdjective = player.getCivilizationAdjective();
		m_szMapScriptName = GC.getInitCore().getMapScriptName();
		m_eWorldSize = map.getWorldSize();
		m_eClimate = map.getClimate();
		m_eSeaLevel = map.getSeaLevel();
		m_eEra = game.getStartEra();
		m_eGameSpeed = game.getGameSpeedType();

		m_listGameOptions.clear();
		for (int i = 0; i < NUM_GAMEOPTION_TYPES; i++)
		{
			GameOptionTypes eOption = (GameOptionTypes)i;
			if (game.isOption(eOption))
			{
				m_listGameOptions.push_back(eOption);
			}
		}

		m_listVictoryTypes.clear();
		for (int i = 0; i < GC.getNumVictoryInfos(); i++)
		{
			VictoryTypes eVictory = (VictoryTypes)i;
			if (game.isVictoryValid(eVictory))
			{
				m_listVictoryTypes.push_back(eVictory);
			}
		}
		if (game.getWinner() == player.getTeam())
		{
			m_eVictoryType = game.getVictory();
		}
		else
		{
			m_eVictoryType = NO_VICTORY;
		}

		m_iNormalizedScore = player.calculateScore(true, player.getTeam() == GC.getGameINLINE().getWinner());
	}

	m_bMultiplayer = game.isGameMultiPlayer();


	m_iInitialTurn = GC.getGameINLINE().getStartTurn();
	m_iStartYear = GC.getGameINLINE().getStartYear();
	m_iFinalTurn = game.getGameTurn();
	GAMETEXT.setYearStr(m_szFinalDate, m_iFinalTurn, false, GC.getGameINLINE().getCalendar(), GC.getGameINLINE().getStartYear(), GC.getGameINLINE().getGameSpeedType());

	m_eCalendar = GC.getGameINLINE().getCalendar();


	std::map<PlayerTypes, int> mapPlayers;
	m_listPlayerScoreHistory.clear();
	int iPlayerIndex = 0;
	for (int iPlayer = 0; iPlayer < MAX_PLAYERS; iPlayer++)
	{
		CvPlayer& player = GET_PLAYER((PlayerTypes)iPlayer);
		if (player.isEverAlive())
		{
			mapPlayers[(PlayerTypes)iPlayer] = iPlayerIndex;
			if ((PlayerTypes)iPlayer == game.getActivePlayer())
			{
				m_iActivePlayer = iPlayerIndex;
			}
			++iPlayerIndex;

			PlayerInfo playerInfo;
			playerInfo.m_eLeader = player.getLeaderType();
			playerInfo.m_eColor = (ColorTypes)GC.getPlayerColorInfo(player.getPlayerColor()).getColorTypePrimary();
			for (int iTurn = m_iInitialTurn; iTurn <= m_iFinalTurn; iTurn++)
			{
				TurnData score;
				score.m_iScore = player.getScoreHistory(iTurn);
				score.m_iAgriculture = player.getAgricultureHistory(iTurn);
				score.m_iIndustry = player.getIndustryHistory(iTurn);
				score.m_iEconomy = player.getEconomyHistory(iTurn);

				playerInfo.m_listScore.push_back(score);
			}
			m_listPlayerScoreHistory.push_back(playerInfo);
		}
	}

	m_listReplayMessages.clear();
	for (uint i = 0; i < game.getNumReplayMessages(); i++)
	{
		std::map<PlayerTypes, int>::iterator it = mapPlayers.find(game.getReplayMessagePlayer(i));
		if (it != mapPlayers.end())
		{
			CvReplayMessage* pMsg = new CvReplayMessage(game.getReplayMessageTurn(i), game.getReplayMessageType(i), (PlayerTypes)it->second);
			if (NULL != pMsg)
			{
				pMsg->setColor(game.getReplayMessageColor(i));
				pMsg->setText(game.getReplayMessageText(i));
				pMsg->setPlot(game.getReplayMessagePlotX(i), game.getReplayMessagePlotY(i));
				m_listReplayMessages.push_back(pMsg);
			}	
		}
		else
		{
			CvReplayMessage* pMsg = new CvReplayMessage(game.getReplayMessageTurn(i), game.getReplayMessageType(i), NO_PLAYER);
			if (NULL != pMsg)
			{
				pMsg->setColor(game.getReplayMessageColor(i));
				pMsg->setText(game.getReplayMessageText(i));
				pMsg->setPlot(game.getReplayMessagePlotX(i), game.getReplayMessagePlotY(i));
				m_listReplayMessages.push_back(pMsg);
			}	
		}
	}

	m_iMapWidth = GC.getMapINLINE().getGridWidthINLINE();
	m_iMapHeight = GC.getMapINLINE().getGridHeightINLINE();
	
	SAFE_DELETE(m_pcMinimapPixels);	
	m_pcMinimapPixels = new unsigned char[m_nMinimapSize];
	
	void *ptexture = (void*)gDLL->getInterfaceIFace()->getMinimapBaseTexture();
	if (ptexture)
		memcpy((void*)m_pcMinimapPixels, ptexture, m_nMinimapSize);

	m_szModName = gDLL->getModName();
}

int CvReplayInfo::getNumPlayers() const
{
	return (int)m_listPlayerScoreHistory.size();
}


bool CvReplayInfo::isValidPlayer(int i) const
{
	return (i >= 0 && i < (int)m_listPlayerScoreHistory.size());
}

bool CvReplayInfo::isValidTurn(int i) const
{
	return (i >= m_iInitialTurn && i <= m_iFinalTurn);
}

int CvReplayInfo::getActivePlayer() const
{
	return m_iActivePlayer;
}

LeaderHeadTypes CvReplayInfo::getLeader(int iPlayer) const
{
	if (iPlayer < 0)
	{
		iPlayer = m_iActivePlayer;
	}
	if (isValidPlayer(iPlayer))
	{
		return m_listPlayerScoreHistory[iPlayer].m_eLeader;
	}
	return NO_LEADER;
}

ColorTypes CvReplayInfo::getColor(int iPlayer) const
{
	if (iPlayer < 0)
	{
		iPlayer = m_iActivePlayer;
	}
	if (isValidPlayer(iPlayer))
	{
		return m_listPlayerScoreHistory[iPlayer].m_eColor;
	}
	return NO_COLOR;
}

HandicapTypes CvReplayInfo::getDifficulty() const
{
	return m_eDifficulty;
}

const CvWString& CvReplayInfo::getLeaderName() const
{
	return m_szLeaderName;
}

const CvWString& CvReplayInfo::getCivDescription() const
{
	return m_szCivDescription;
}

const CvWString& CvReplayInfo::getShortCivDescription() const
{
	return m_szShortCivDescription;
}

const CvWString& CvReplayInfo::getCivAdjective() const
{
	return m_szCivAdjective;
}

const CvWString& CvReplayInfo::getMapScriptName() const
{
	return m_szMapScriptName;
}

WorldSizeTypes CvReplayInfo::getWorldSize() const
{
	return m_eWorldSize;
}

ClimateTypes CvReplayInfo::getClimate() const
{
	return m_eClimate;
}

SeaLevelTypes CvReplayInfo::getSeaLevel() const
{
	return m_eSeaLevel;
}

EraTypes CvReplayInfo::getEra() const
{
	return m_eEra;
}

GameSpeedTypes CvReplayInfo::getGameSpeed() const
{
	return m_eGameSpeed;
}

bool CvReplayInfo::isGameOption(GameOptionTypes eOption) const
{
	for (uint i = 0; i < m_listGameOptions.size(); i++)
	{
		if (m_listGameOptions[i] == eOption)
		{
			return true;
		}
	}
	return false;
}

bool CvReplayInfo::isVictoryCondition(VictoryTypes eVictory) const
{
	for (uint i = 0; i < m_listVictoryTypes.size(); i++)
	{
		if (m_listVictoryTypes[i] == eVictory)
		{
			return true;
		}
	}
	return false;
}

VictoryTypes CvReplayInfo::getVictoryType() const
{
	return m_eVictoryType;
}

bool CvReplayInfo::isMultiplayer() const
{
	return m_bMultiplayer;
}


void CvReplayInfo::addReplayMessage(CvReplayMessage* pMessage)
{
	m_listReplayMessages.push_back(pMessage);
}

void CvReplayInfo::clearReplayMessageMap()
{
	for (ReplayMessageList::const_iterator itList = m_listReplayMessages.begin(); itList != m_listReplayMessages.end(); itList++)
	{
		const CvReplayMessage* pMessage = *itList;
		if (NULL != pMessage)
		{
			delete pMessage;
		}
	}
	m_listReplayMessages.clear();
}

int CvReplayInfo::getReplayMessageTurn(uint i) const
{
	if (i >= m_listReplayMessages.size())
	{
		return (-1);
	}
	const CvReplayMessage* pMessage =  m_listReplayMessages[i];
	if (NULL == pMessage)
	{
		return (-1);
	}
	return pMessage->getTurn();
}

ReplayMessageTypes CvReplayInfo::getReplayMessageType(uint i) const
{
	if (i >= m_listReplayMessages.size())
	{
		return (NO_REPLAY_MESSAGE);
	}
	const CvReplayMessage* pMessage =  m_listReplayMessages[i];
	if (NULL == pMessage)
	{
		return (NO_REPLAY_MESSAGE);
	}
	return pMessage->getType();
}

int CvReplayInfo::getReplayMessagePlotX(uint i) const
{
	if (i >= m_listReplayMessages.size())
	{
		return (-1);
	}
	const CvReplayMessage* pMessage =  m_listReplayMessages[i];
	if (NULL == pMessage)
	{
		return (-1);
	}
	return pMessage->getPlotX();
}

int CvReplayInfo::getReplayMessagePlotY(uint i) const
{
	if (i >= m_listReplayMessages.size())
	{
		return (-1);
	}
	const CvReplayMessage* pMessage =  m_listReplayMessages[i];
	if (NULL == pMessage)
	{
		return (-1);
	}
	return pMessage->getPlotY();
}

PlayerTypes CvReplayInfo::getReplayMessagePlayer(uint i) const
{
	if (i >= m_listReplayMessages.size())
	{
		return (NO_PLAYER);
	}
	const CvReplayMessage* pMessage =  m_listReplayMessages[i];
	if (NULL == pMessage)
	{
		return (NO_PLAYER);
	}
	return pMessage->getPlayer();
}

LPCWSTR CvReplayInfo::getReplayMessageText(uint i) const
{
	if (i >= m_listReplayMessages.size())
	{
		return (NULL);
	}
	const CvReplayMessage* pMessage =  m_listReplayMessages[i];
	if (NULL == pMessage)
	{
		return (NULL);
	}
	return pMessage->getText().GetCString();
}

ColorTypes CvReplayInfo::getReplayMessageColor(uint i) const
{
	if (i >= m_listReplayMessages.size())
	{
		return (NO_COLOR);
	}
	const CvReplayMessage* pMessage =  m_listReplayMessages[i];
	if (NULL == pMessage)
	{
		return (NO_COLOR);
	}
	return pMessage->getColor();
}


uint CvReplayInfo::getNumReplayMessages() const
{
	return m_listReplayMessages.size();
}


int CvReplayInfo::getInitialTurn() const
{
	return m_iInitialTurn;
}

int CvReplayInfo::getStartYear() const
{
	return m_iStartYear;
}

int CvReplayInfo::getFinalTurn() const
{
	return m_iFinalTurn;
}

const wchar* CvReplayInfo::getFinalDate() const
{
	return m_szFinalDate;
}

CalendarTypes CvReplayInfo::getCalendar() const
{
	return m_eCalendar;
}


int CvReplayInfo::getPlayerScore(int iPlayer, int iTurn) const
{
	if (isValidPlayer(iPlayer) && isValidTurn(iTurn))
	{
		return m_listPlayerScoreHistory[iPlayer].m_listScore[iTurn-m_iInitialTurn].m_iScore;
	}
	return 0;
}

int CvReplayInfo::getPlayerEconomy(int iPlayer, int iTurn) const
{
	if (isValidPlayer(iPlayer) && isValidTurn(iTurn))
	{
		return m_listPlayerScoreHistory[iPlayer].m_listScore[iTurn-m_iInitialTurn].m_iEconomy;
	}
	return 0;
}

int CvReplayInfo::getPlayerIndustry(int iPlayer, int iTurn) const
{
	if (isValidPlayer(iPlayer) && isValidTurn(iTurn))
	{
		return m_listPlayerScoreHistory[iPlayer].m_listScore[iTurn-m_iInitialTurn].m_iIndustry;
	}
	return 0;
}

int CvReplayInfo::getPlayerAgriculture(int iPlayer, int iTurn) const
{
	if (isValidPlayer(iPlayer) && isValidTurn(iTurn))
	{
		return m_listPlayerScoreHistory[iPlayer].m_listScore[iTurn-m_iInitialTurn].m_iAgriculture;
	}
	return 0;
}

int CvReplayInfo::getFinalScore() const
{
	return getPlayerScore(m_iActivePlayer, m_iFinalTurn);
}

int CvReplayInfo::getFinalEconomy() const
{
	return getPlayerEconomy(m_iActivePlayer, m_iFinalTurn);
}

int CvReplayInfo::getFinalIndustry() const
{
	return getPlayerIndustry(m_iActivePlayer, m_iFinalTurn);
}

int CvReplayInfo::getFinalAgriculture() const
{
	return getPlayerAgriculture(m_iActivePlayer, m_iFinalTurn);
}

int CvReplayInfo::getNormalizedScore() const
{
	return m_iNormalizedScore;
}

int CvReplayInfo::getMapHeight() const
{
	return m_iMapHeight;
}

int CvReplayInfo::getMapWidth() const
{
	return m_iMapWidth;
}

const unsigned char* CvReplayInfo::getMinimapPixels() const
{
	return m_pcMinimapPixels;
}

const char* CvReplayInfo::getModName() const
{
	return m_szModName;
}


bool CvReplayInfo::read(FDataStreamBase& stream)
{
	int iType;
	int iNumTypes;
	bool bSuccess = true;

	try
	{
		int iVersion;
		stream.Read(&iVersion);
		if (iVersion < 2)
		{
			return false;
		}

		stream.Read(&m_iActivePlayer);

		stream.Read(&iType);
		m_eDifficulty = (HandicapTypes)iType;
		stream.ReadString(m_szLeaderName);
		stream.ReadString(m_szCivDescription);
		stream.ReadString(m_szShortCivDescription);
		stream.ReadString(m_szCivAdjective);
		if (iVersion > 3)
		{
			stream.ReadString(m_szMapScriptName);
		}
		else
		{
			m_szMapScriptName = gDLL->getText("TXT_KEY_TRAIT_PLAYER_UNKNOWN");
		}
		stream.Read(&iType);
		m_eWorldSize = (WorldSizeTypes)iType;
		stream.Read(&iType);
		m_eClimate = (ClimateTypes)iType;
		stream.Read(&iType);
		m_eSeaLevel = (SeaLevelTypes)iType;
		stream.Read(&iType);
		m_eEra = (EraTypes)iType;
		stream.Read(&iType);
		m_eGameSpeed = (GameSpeedTypes)iType;
		stream.Read(&iNumTypes);
		for (int i = 0; i < iNumTypes; i++)
		{
			stream.Read(&iType);
			m_listGameOptions.push_back((GameOptionTypes)iType);
		}
		stream.Read(&iNumTypes);
		for (int i = 0; i < iNumTypes; i++)
		{
			stream.Read(&iType);
			m_listVictoryTypes.push_back((VictoryTypes)iType);
		}
		stream.Read(&iType);
		m_eVictoryType = (VictoryTypes)iType;
		stream.Read(&iNumTypes);
		for (int i = 0; i < iNumTypes; i++)
		{
			CvReplayMessage* pMessage = new CvReplayMessage(0);
			if (NULL != pMessage)
			{
				pMessage->read(stream);
			}
			m_listReplayMessages.push_back(pMessage);
		}
		stream.Read(&m_iInitialTurn);
		stream.Read(&m_iStartYear);
		stream.Read(&m_iFinalTurn);
		stream.ReadString(m_szFinalDate);
		stream.Read(&iType);
		m_eCalendar = (CalendarTypes)iType;
		stream.Read(&m_iNormalizedScore);
		stream.Read(&iNumTypes);
		for (int i = 0; i < iNumTypes; i++)
		{
			PlayerInfo info;
			stream.Read(&iType);
			info.m_eLeader = (LeaderHeadTypes)iType;
			stream.Read(&iType);
			info.m_eColor = (ColorTypes)iType;
			int jNumTypes;
			stream.Read(&jNumTypes);
			for (int j = 0; j < jNumTypes; j++)
			{
				TurnData data;
				stream.Read(&(data.m_iScore));
				stream.Read(&(data.m_iEconomy));
				stream.Read(&(data.m_iIndustry));
				stream.Read(&(data.m_iAgriculture));
				info.m_listScore.push_back(data);
			}
			m_listPlayerScoreHistory.push_back(info);
		}
		stream.Read(&m_iMapWidth);
		stream.Read(&m_iMapHeight);
		SAFE_DELETE(m_pcMinimapPixels);
		m_pcMinimapPixels = new unsigned char[m_nMinimapSize];
		stream.Read(m_nMinimapSize, m_pcMinimapPixels);
		stream.Read(&m_bMultiplayer);
		if (iVersion > 2)
		{
			stream.ReadString(m_szModName);
		}
	}
	catch (...)
	{
		bSuccess = false;
	}
	return bSuccess;
}

void CvReplayInfo::write(FDataStreamBase& stream)
{
	stream.Write(REPLAY_VERSION);
	stream.Write(m_iActivePlayer);
	stream.Write((int)m_eDifficulty);
	stream.WriteString(m_szLeaderName);
	stream.WriteString(m_szCivDescription);
	stream.WriteString(m_szShortCivDescription);
	stream.WriteString(m_szCivAdjective);
	stream.WriteString(m_szMapScriptName);
	stream.Write((int)m_eWorldSize);
	stream.Write((int)m_eClimate);
	stream.Write((int)m_eSeaLevel);
	stream.Write((int)m_eEra);
	stream.Write((int)m_eGameSpeed);
	stream.Write((int)m_listGameOptions.size());
	for (uint i = 0; i < m_listGameOptions.size(); i++)
	{
		stream.Write((int)m_listGameOptions[i]);
	}
	stream.Write((int)m_listVictoryTypes.size());
	for (uint i = 0; i < m_listVictoryTypes.size(); i++)
	{
		stream.Write((int)m_listVictoryTypes[i]);
	}
	stream.Write((int)m_eVictoryType);
	stream.Write((int)m_listReplayMessages.size());
	ReplayMessageList::const_iterator it;
	for (uint i = 0; i < m_listReplayMessages.size(); i++)
	{
		if (NULL != m_listReplayMessages[i])
		{
			m_listReplayMessages[i]->write(stream);
		}
	}
	stream.Write(m_iInitialTurn);
	stream.Write(m_iStartYear);
	stream.Write(m_iFinalTurn);
	stream.WriteString(m_szFinalDate);
	stream.Write((int)m_eCalendar);
	stream.Write(m_iNormalizedScore);
	stream.Write((int)m_listPlayerScoreHistory.size());
	for (uint i = 0; i < m_listPlayerScoreHistory.size(); i++)
	{
		PlayerInfo& info = m_listPlayerScoreHistory[i];
		stream.Write((int)info.m_eLeader);
		stream.Write((int)info.m_eColor);
		stream.Write((int)info.m_listScore.size());
		for (uint j = 0; j < info.m_listScore.size(); j++)
		{
			stream.Write(info.m_listScore[j].m_iScore);
			stream.Write(info.m_listScore[j].m_iEconomy);
			stream.Write(info.m_listScore[j].m_iIndustry);
			stream.Write(info.m_listScore[j].m_iAgriculture);
		}
	}
	stream.Write(m_iMapWidth);
	stream.Write(m_iMapHeight);
	stream.Write(m_nMinimapSize, m_pcMinimapPixels);
	stream.Write(m_bMultiplayer);
	stream.WriteString(m_szModName);
}
