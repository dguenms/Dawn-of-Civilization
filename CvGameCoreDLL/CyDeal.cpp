//
// Python wrapper class for CvGame 
// 

#include "CvGameCoreDLL.h"
#include "CyDeal.h"
#include "CvDeal.h"

CyDeal::CyDeal(CvDeal* pDeal) :
	m_pDeal(pDeal)
{

}

CyDeal::~CyDeal()
{
}

bool CyDeal::isNone()
{ 
	return (NULL == m_pDeal); 
}

int CyDeal::getID() const
{
	return (m_pDeal ? m_pDeal->getID() : -1);
}

int CyDeal::getInitialGameTurn() const
{
	return (m_pDeal ? m_pDeal->getInitialGameTurn() : -1);
}

int CyDeal::getFirstPlayer() const
{
	return (m_pDeal ? m_pDeal->getFirstPlayer() : -1);
}

int CyDeal::getSecondPlayer() const
{
	return (m_pDeal ? m_pDeal->getSecondPlayer() : -1);
}

int CyDeal::getLengthFirstTrades() const
{
	return (m_pDeal ? m_pDeal->getLengthFirstTrades() : 0);
}

int CyDeal::getLengthSecondTrades() const
{
	return (m_pDeal ? m_pDeal->getLengthSecondTrades() : 0);
}

TradeData* CyDeal::getFirstTrade(int i) const
{
	if (i < getLengthFirstTrades() && NULL != m_pDeal && NULL != m_pDeal->getFirstTrades())
	{
		const CLinkList<TradeData>& listTradeData = *(m_pDeal->getFirstTrades());
		int iCount = 0;
		for (CLLNode<TradeData>* pNode = listTradeData.head(); NULL != pNode; pNode = listTradeData.next(pNode))
		{
			if (iCount == i)
			{
				return &(pNode->m_data);
			}
			iCount++;
		}
	}
	return (NULL);
}

TradeData* CyDeal::getSecondTrade(int i) const
{
	if (i < getLengthSecondTrades() && NULL != m_pDeal && NULL != m_pDeal->getSecondTrades())
	{
		const CLinkList<TradeData>& listTradeData = *(m_pDeal->getSecondTrades());
		int iCount = 0;
		for (CLLNode<TradeData>* pNode = listTradeData.head(); NULL != pNode; pNode = listTradeData.next(pNode))
		{
			if (iCount == i)
			{
				return &(pNode->m_data);
			}
			iCount++;
		}
	}
	return (NULL);
}

void CyDeal::kill()
{
	if (NULL != m_pDeal)
	{
		m_pDeal->kill();
	}
}

// BUG - Expose Deal Cancelability - start
bool CyDeal::isCancelable(int /*PlayerTypes*/ eByPlayer, bool bIgnoreWaitingPeriod) const
{
	if (NULL != m_pDeal)
	{
		if (bIgnoreWaitingPeriod)
		{
			return !m_pDeal->isUncancelableVassalDeal((PlayerTypes)eByPlayer, NULL);
		}

		return m_pDeal->isCancelable((PlayerTypes)eByPlayer, NULL);
	}
	
	return false;
}

std::wstring CyDeal::getCannotCancelReason(int /*PlayerTypes*/ eByPlayer) const
{
	CvWString szReason;
	if (NULL != m_pDeal)
	{
		m_pDeal->isCancelable((PlayerTypes)eByPlayer, &szReason);
	}
	return szReason;
}

int CyDeal::turnsToCancel(int /*PlayerTypes*/ eByPlayer) const
{
	return (m_pDeal ? m_pDeal->turnsToCancel((PlayerTypes)eByPlayer) : -1);
}
// BUG - Expose Deal Cancelability - end
