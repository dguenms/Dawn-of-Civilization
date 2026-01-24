#pragma once

#ifndef TALKINGHEADMESSAGE_H
#define TALKINGHEADMESSAGE_H

class CvTalkingHeadMessage
{
public:
	DllExport CvTalkingHeadMessage(int iMessageTurn = 0, int iLen = 0,
			LPCWSTR pszDesc = NULL, LPCTSTR pszSound = NULL, 
			InterfaceMessageTypes eType = MESSAGE_TYPE_INFO, LPCTSTR icon = NULL,
			ColorTypes eColor = NO_COLOR, int iX = -1, int iY = -1,
			bool bShowOffScreenArrows = false, bool bShowOnScreenArrows = false);
	DllExport virtual ~CvTalkingHeadMessage();

	void read(FDataStreamBase& stream);
	void write(FDataStreamBase& stream) const;

	// Accessors
	DllExport const wchar* getDescription() const;
	void setDescription(CvWString pszDescription);
	DllExport const CvString& getSound() const;
	void setSound(LPCTSTR pszSound);
	DllExport const CvString& getIcon() const;
	void setIcon(LPCTSTR pszIcon);
	DllExport int getLength() const;
	DllExport void setLength(int iLength);
	DllExport ColorTypes getFlashColor() const;
	void setFlashColor(ColorTypes eColor);
	DllExport int getX() const;
	void setX(int i);
	DllExport int getY() const;
	void setY(int i);
	DllExport bool getOffScreenArrows() const;
	void setOffScreenArrows(bool bArrows);
	DllExport bool getOnScreenArrows() const;
	void setOnScreenArrows(bool bArrows);
	DllExport int getTurn() const;
	void setTurn(int iTurn);
	DllExport InterfaceMessageTypes getMessageType() const;
	void setMessageType(InterfaceMessageTypes eType);
	DllExport ChatTargetTypes getTarget() const;
	DllExport void setTarget(ChatTargetTypes eType);
	DllExport PlayerTypes getFromPlayer() const;
	DllExport void setFromPlayer(PlayerTypes eFromPlayer);
	bool getShown() const;
	DllExport void setShown(bool bShown);
	bool getSoundPlayed() const; // advc.106b
	int getExpireTurn(/* advc.700: */ bool bHuman = true);

protected: // advc.003k (warning): It's not safe to add data members to this class!
	CvWString m_szDescription;
	CvString m_szSound;
	CvString m_szIcon;
	int m_iLength;
	ColorTypes m_eFlashColor;
	int m_iFlashX;
	int m_iFlashY;
	bool m_bOffScreenArrows;
	bool m_bOnScreenArrows;
	int m_iTurn;
	InterfaceMessageTypes m_eMessageType;
	PlayerTypes m_eFromPlayer;
	ChatTargetTypes m_eTarget;
	bool m_bShown;
	/*	advc.106b: (This one bool doesn't actually increase the class size.
		Could even add two more.) */
	mutable bool m_bSoundPlayed;
};

BOOST_STATIC_ASSERT(sizeof(CvTalkingHeadMessage) == 128); // advc.003k

#endif
