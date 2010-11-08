#include "CvGameCoreDLL.h"
#include "CyReplayInfo.h"
#include "CyMap.h"

CyReplayInfo::CyReplayInfo()
{
	m_pHoF = &m_replay;
}

CyReplayInfo::CyReplayInfo(CvReplayInfo* pReplayInfo) : m_pHoF(pReplayInfo)
{
}

void CyReplayInfo::createInfo(int iPlayer)
{
	if (m_pHoF)
	{
		m_pHoF->createInfo((PlayerTypes)iPlayer);
	}
}

int CyReplayInfo::getActivePlayer() const
{
	if (m_pHoF)
	{
		return m_pHoF->getActivePlayer();
	}
	return -1;
}


int CyReplayInfo::getLeader(int iPlayer) const
{
	if (m_pHoF)
	{
		return (int)(m_pHoF->getLeader(iPlayer));
	}
	return -1;
}

int CyReplayInfo::getColor(int iPlayer) const
{
	if (m_pHoF)
	{
		return (int)(m_pHoF->getColor(iPlayer));
	}
	return -1;
}

int CyReplayInfo::getDifficulty() const
{
	if (m_pHoF)
	{
		return (int)(m_pHoF->getDifficulty());
	}
	return -1;
}

std::wstring CyReplayInfo::getLeaderName() const
{
	if (m_pHoF)
	{
		return m_pHoF->getLeaderName().GetCString();
	}
	return L"";
}

std::wstring CyReplayInfo::getCivDescription() const
{
	if (m_pHoF)
	{
		return m_pHoF->getCivDescription().GetCString();
	}
	return L"";
}

std::wstring CyReplayInfo::getShortCivDescription() const
{
	if (m_pHoF)
	{
		return m_pHoF->getShortCivDescription().GetCString();
	}
	return L"";
}

std::wstring CyReplayInfo::getCivAdjective() const
{
	if (m_pHoF)
	{
		return m_pHoF->getCivAdjective().GetCString();
	}
	return L"";
}

std::wstring CyReplayInfo::getMapScriptName() const
{
	if (m_pHoF)
	{
		return m_pHoF->getMapScriptName().GetCString();
	}
	return L"";
}

int CyReplayInfo::getWorldSize() const
{
	if (m_pHoF)
	{
		return (int)(m_pHoF->getWorldSize());
	}
	return -1;
}

int CyReplayInfo::getClimate() const
{
	if (m_pHoF)
	{
		return (int)(m_pHoF->getClimate());
	}
	return -1;
}

int CyReplayInfo::getSeaLevel() const
{
	if (m_pHoF)
	{
		return (int)(m_pHoF->getSeaLevel());
	}
	return -1;
}

int CyReplayInfo::getEra() const
{
	if (m_pHoF)
	{
		return (int)(m_pHoF->getEra());
	}
	return -1;
}

int CyReplayInfo::getGameSpeed() const
{
	if (m_pHoF)
	{
		return (int)(m_pHoF->getGameSpeed());
	}
	return -1;
}

bool CyReplayInfo::isGameOption(int iOption) const
{
	if (m_pHoF)
	{
		return m_pHoF->isGameOption((GameOptionTypes)iOption);
	}
	return false;
}

bool CyReplayInfo::isVictoryCondition(int iVictory) const
{
	if (m_pHoF)
	{
		return m_pHoF->isVictoryCondition((VictoryTypes)iVictory);
	}
	return false;
}

int CyReplayInfo::getVictoryType() const
{
	if (m_pHoF)
	{
		return (int)(m_pHoF->getVictoryType());
	}
	return -1;
}

bool CyReplayInfo::isMultiplayer() const
{
	if (m_pHoF)
	{
		return m_pHoF->isMultiplayer();
	}
	return false;
}

int CyReplayInfo::getInitialTurn() const
{
	if (m_pHoF)
	{
		return m_pHoF->getInitialTurn();
	}
	return -1;
}

int CyReplayInfo::getStartYear() const
{
	if (m_pHoF)
	{
		return m_pHoF->getStartYear();
	}
	return -1;
}

int CyReplayInfo::getFinalTurn() const
{
	if (m_pHoF)
	{
		return m_pHoF->getFinalTurn();
	}
	return -1;
}

const std::wstring CyReplayInfo::getFinalDate() const
{
	if (m_pHoF)
	{
		return m_pHoF->getFinalDate();
	}
	return L"";
}

int CyReplayInfo::getCalendar() const
{
	if (m_pHoF)
	{
		return m_pHoF->getCalendar();
	}
	return -1;
}


int CyReplayInfo::getFinalScore() const
{
	if (m_pHoF)
	{
		return m_pHoF->getFinalScore();
	}
	return -1;
}

int CyReplayInfo::getFinalEconomy() const
{
	if (m_pHoF)
	{
		return m_pHoF->getFinalEconomy();
	}
	return -1;
}

int CyReplayInfo::getFinalIndustry() const
{
	if (m_pHoF)
	{
		return m_pHoF->getFinalIndustry();
	}
	return -1;
}

int CyReplayInfo::getFinalAgriculture() const
{
	if (m_pHoF)
	{
		return m_pHoF->getFinalAgriculture();
	}
	return -1;
}

int CyReplayInfo::getNormalizedScore() const
{
	if (m_pHoF)
	{
		return m_pHoF->getNormalizedScore();
	}
	return -1;
}

int CyReplayInfo::getMapWidth() const
{
	if (m_pHoF)
	{
		return m_pHoF->getMapWidth();
	}
	return -1;
}

int CyReplayInfo::getMapHeight() const
{
	if (m_pHoF)
	{
		return m_pHoF->getMapHeight();
	}
	return -1;
}

int CyReplayInfo::getNumPlayers() const
{
	if (m_pHoF)
	{
		return m_pHoF->getNumPlayers();
	}
	return -1;
}

int CyReplayInfo::getPlayerScore(int iPlayer, int iTurn) const
{
	if (m_pHoF)
	{
		return m_pHoF->getPlayerScore(iPlayer, iTurn);
	}
	return -1;
}

int CyReplayInfo::getPlayerEconomy(int iPlayer, int iTurn) const
{
	if (m_pHoF)
	{
		return m_pHoF->getPlayerEconomy(iPlayer, iTurn);
	}
	return -1;
}

int CyReplayInfo::getPlayerIndustry(int iPlayer, int iTurn) const
{
	if (m_pHoF)
	{
		return m_pHoF->getPlayerIndustry(iPlayer, iTurn);
	}
	return -1;
}

int CyReplayInfo::getPlayerAgriculture(int iPlayer, int iTurn) const
{
	if (m_pHoF)
	{
		return m_pHoF->getPlayerAgriculture(iPlayer, iTurn);
	}
	return -1;
}

int CyReplayInfo::getReplayMessageTurn(int i) const
{
	if (m_pHoF)
	{
		return m_pHoF->getReplayMessageTurn((uint)i);
	}
	return -1;
}

int CyReplayInfo::getReplayMessageType(int i) const
{
	if (m_pHoF)
	{
		return (int)m_pHoF->getReplayMessageType((uint)i);
	}
	return -1;
}

int CyReplayInfo::getReplayMessagePlotX(int i) const
{
	if (m_pHoF)
	{
		return m_pHoF->getReplayMessagePlotX((uint)i);
	}
	return -1;
}

int CyReplayInfo::getReplayMessagePlotY(int i) const
{
	if (m_pHoF)
	{
		return m_pHoF->getReplayMessagePlotY((uint)i);
	}
	return -1;
}

int CyReplayInfo::getReplayMessagePlayer(int i) const
{
	if (m_pHoF)
	{
		return (int)m_pHoF->getReplayMessagePlayer((uint)i);
	}
	return -1;
}

const std::wstring CyReplayInfo::getReplayMessageText(int i) const
{
	std::wstring szText;
	if (m_pHoF)
	{
		szText = m_pHoF->getReplayMessageText((uint)i);
	}
	return szText;
}

int CyReplayInfo::getNumReplayMessages() const
{
	if (m_pHoF)
	{
		return (int)m_pHoF->getNumReplayMessages();
	}
	return -1;
}

int CyReplayInfo::getReplayMessageColor(int i) const
{
	if (m_pHoF)
	{
		return (int)m_pHoF->getReplayMessageColor((uint)i);
	}
	return -1;
}

const char* CyReplayInfo::getModName() const
{
	if (m_pHoF)
	{
		return (m_pHoF->getModName());
	}
	return "";
}
