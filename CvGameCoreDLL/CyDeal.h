#pragma once

// CyDeal.h
// Python wrapper class for CvDeal 

#ifndef CY_DEAL_H
#define CY_DEAL_H

//#include "CvEnums.h"
//#include "CvStructs.h"

class CvDeal;

class CyDeal
{

public:
	CyDeal(CvDeal* pDeal = NULL);
	virtual ~CyDeal();
	CvDeal* getDeal() const { return m_pDeal; }

	bool isNone();

	int getID() const;
	int getInitialGameTurn() const;
	int getFirstPlayer() const;
	int getSecondPlayer() const;
	int getLengthFirstTrades() const;
	int getLengthSecondTrades() const;
	TradeData* getFirstTrade(int i) const;
	TradeData* getSecondTrade(int i) const;

	void kill();

protected:
	CvDeal* m_pDeal;
};

#endif
