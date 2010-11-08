#pragma once
#ifndef CVREPLAYMESSAGE_H
#define CVREPLAYMESSAGE_H

class CvReplayMessage
{
public:
	CvReplayMessage(int iTurn, ReplayMessageTypes eType = NO_REPLAY_MESSAGE, PlayerTypes ePlayer = NO_PLAYER);
	virtual ~CvReplayMessage();

	const CvReplayMessage& operator=(const CvReplayMessage& other);

	// Accessors
	void setTurn(int iTurn);
	int getTurn() const;
	void setType(ReplayMessageTypes eType);
	ReplayMessageTypes getType() const;
	void setPlot(int iX, int iY);
	int getPlotX() const;
	int getPlotY() const;
	void setPlayer(PlayerTypes ePlayer);
	PlayerTypes getPlayer() const;
	void setText(CvWString pszText);
	const CvWString& getText() const;
	void setColor(ColorTypes eColor);
	ColorTypes getColor() const;

	void read(FDataStreamBase& stream);
	void write(FDataStreamBase& stream) const;

private:
	int m_iTurn;
	ReplayMessageTypes m_eType;
	int m_iPlotX;
	int m_iPlotY;
	PlayerTypes m_ePlayer;
	CvWString m_szText;
	ColorTypes m_eColor;
};

#endif