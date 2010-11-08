#include "CvGameCoreDLL.h"
#include "CvTalkingHeadMessage.h"
#include "CvGameAI.h"
#include "CvGlobals.h"

CvTalkingHeadMessage::CvTalkingHeadMessage(int iMessageTurn, int iLen, LPCWSTR pszDesc, LPCTSTR pszSound, InterfaceMessageTypes eType, LPCTSTR pszIcon, ColorTypes eColor, int iX, int iY, bool bShowOffScreenArrows, bool bShowOnScreenArrows) :
	m_iTurn(iMessageTurn),
	m_szDescription(pszDesc),
	m_szSound(pszSound),
	m_szIcon(pszIcon),
	m_iLength(iLen),
	m_eFlashColor(eColor),
	m_iFlashX(iX),
	m_iFlashY(iY),
	m_bOffScreenArrows(bShowOffScreenArrows),
	m_bOnScreenArrows(bShowOnScreenArrows),
	m_eMessageType(eType),
	m_eFromPlayer(NO_PLAYER),
	m_eTarget(NO_CHATTARGET),
	m_bShown(false)
{
}

CvTalkingHeadMessage::~CvTalkingHeadMessage(void)
{
}


void CvTalkingHeadMessage::read(FDataStreamBase& stream)
{
	stream.ReadString(m_szDescription);
	stream.ReadString(m_szSound);
	stream.ReadString(m_szIcon);
	stream.Read(&m_iLength);
	int iColor;
	stream.Read(&iColor);
	m_eFlashColor = (ColorTypes)iColor;
	stream.Read(&m_iFlashX);
	stream.Read(&m_iFlashY);
	stream.Read(&m_bOffScreenArrows);
	stream.Read(&m_bOnScreenArrows);
	stream.Read(&m_iTurn);
	int iType;
	stream.Read(&iType);
	m_eMessageType = (InterfaceMessageTypes)iType;
	stream.Read(&iType);
	m_eFromPlayer = (PlayerTypes)iType;
	stream.Read(&iType);
	m_eTarget = (ChatTargetTypes)iType;
	stream.Read(&m_bShown);
}

void CvTalkingHeadMessage::write(FDataStreamBase& stream) const
{
	stream.WriteString(m_szDescription);
	stream.WriteString(m_szSound);
	stream.WriteString(m_szIcon);
	stream.Write(m_iLength);
	stream.Write(m_eFlashColor);
	stream.Write(m_iFlashX);
	stream.Write(m_iFlashY);
	stream.Write(m_bOffScreenArrows);
	stream.Write(m_bOnScreenArrows);
	stream.Write(m_iTurn);
	stream.Write(m_eMessageType);
	stream.Write(m_eFromPlayer);
	stream.Write(m_eTarget);
	stream.Write(m_bShown);
}

const wchar* CvTalkingHeadMessage::getDescription() const
{
	return (m_szDescription);
}

void CvTalkingHeadMessage::setDescription(CvWString pszDescription)
{
	m_szDescription = pszDescription;
}

const CvString& CvTalkingHeadMessage::getSound() const
{
	return (m_szSound);
}

void CvTalkingHeadMessage::setSound(LPCTSTR pszSound)
{
	m_szSound = pszSound;
}

const CvString& CvTalkingHeadMessage::getIcon() const
{
	return (m_szIcon);
}

void CvTalkingHeadMessage::setIcon(LPCTSTR pszIcon)
{
	m_szIcon = pszIcon;
}


int CvTalkingHeadMessage::getLength() const
{
	return (m_iLength);
}

void CvTalkingHeadMessage::setLength(int iLength)
{
	m_iLength = iLength;
}

ColorTypes CvTalkingHeadMessage::getFlashColor() const
{
	return (m_eFlashColor);
}

void CvTalkingHeadMessage::setFlashColor(ColorTypes eColor)
{
	m_eFlashColor = eColor;
}

int CvTalkingHeadMessage::getX() const
{
	return (m_iFlashX);
}

void CvTalkingHeadMessage::setX(int i)
{
	m_iFlashX = i;
}

int CvTalkingHeadMessage::getY() const
{
	return (m_iFlashY);
}

void CvTalkingHeadMessage::setY(int i)
{
	m_iFlashY = i;
}

bool CvTalkingHeadMessage::getOffScreenArrows() const
{
	return (m_bOffScreenArrows);
}

void CvTalkingHeadMessage::setOffScreenArrows(bool bArrows)
{
	m_bOffScreenArrows = bArrows;
}

bool CvTalkingHeadMessage::getOnScreenArrows() const
{
	return (m_bOnScreenArrows);
}

void CvTalkingHeadMessage::setOnScreenArrows(bool bArrows)
{
	m_bOnScreenArrows = bArrows;
}

int CvTalkingHeadMessage::getTurn() const
{
	return (m_iTurn);
}

void CvTalkingHeadMessage::setTurn(int iTurn)
{
	m_iTurn = iTurn;
}

InterfaceMessageTypes CvTalkingHeadMessage::getMessageType() const
{
	return (m_eMessageType);
}

void CvTalkingHeadMessage::setMessageType(InterfaceMessageTypes eType)
{
	m_eMessageType = eType;
}

PlayerTypes CvTalkingHeadMessage::getFromPlayer() const
{
	return (m_eFromPlayer);
}

void CvTalkingHeadMessage::setFromPlayer(PlayerTypes eFromPlayer)
{
	m_eFromPlayer = eFromPlayer;
}

ChatTargetTypes CvTalkingHeadMessage::getTarget() const
{
	return (m_eTarget);
}

void CvTalkingHeadMessage::setTarget(ChatTargetTypes eType)
{
	m_eTarget = eType;
}

int CvTalkingHeadMessage::getExpireTurn()
{
	int iExpireTurn = getTurn();
	switch (m_eMessageType)
	{
	case MESSAGE_TYPE_INFO:
		iExpireTurn += 2;
		break;
	case MESSAGE_TYPE_CHAT:
		iExpireTurn += 20;
		break;
    case MESSAGE_TYPE_COMBAT_MESSAGE:
		iExpireTurn += 20;
		break;
	case MESSAGE_TYPE_MINOR_EVENT:
		iExpireTurn += 20;
		break;
	case MESSAGE_TYPE_QUEST:
	case MESSAGE_TYPE_MAJOR_EVENT:
		// never expires
		iExpireTurn = GC.getGameINLINE().getGameTurn() + 1;
		break;
	case MESSAGE_TYPE_DISPLAY_ONLY:
		// never saved
		iExpireTurn = GC.getGameINLINE().getGameTurn() - 1;
		break;
	default:
		FAssert(false);
		break;
	}
	return (iExpireTurn);
}

bool CvTalkingHeadMessage::getShown() const
{
	return m_bShown;
}

void CvTalkingHeadMessage::setShown(bool bShown)
{
	m_bShown = bShown;
}
