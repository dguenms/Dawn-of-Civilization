#pragma once

#ifndef CIV4_PLOT_GROUP_H
#define CIV4_PLOT_GROUP_H

#include "LinkedList.h"

class CvPlot;


class CvPlotGroup
{
public:

	CvPlotGroup();
	virtual ~CvPlotGroup();

	void init(int iID, PlayerTypes eOwner, CvPlot* pPlot);
	void uninit();
	void reset(int iID = 0, PlayerTypes eOwner = NO_PLAYER, bool bConstructorCall=false);

	void addPlot(CvPlot* pPlot, /* advc.064d: */ bool bVerifyProduction = true);
	void removePlot(CvPlot* pPlot, bool bVerifyProduction = true);
	void recalculatePlots(/* advc.064d: */ bool bVerifyProduction = true);

	int getID() const { return m_iID; }
	void setID(int iID) { m_iID = iID; }
	PlayerTypes getOwner() const { return m_eOwner; }
	bool isOwned() const { return getOwner() != NO_PLAYER; }

	int getNumBonuses(BonusTypes eBonus) const { return m_aiNumBonuses.get(eBonus); }
	bool hasBonus(BonusTypes eBonus) { return(getNumBonuses(eBonus) > 0); }
	void changeNumBonuses(BonusTypes eBonus, int iChange);
	void verifyCityProduction(); // advc.064d

	void insertAtEndPlots(XYCoords xy) { m_plots.insertAtEnd(xy); }
	CLLNode<XYCoords>* deletePlotsNode(CLLNode<XYCoords>* pNode);
	CLLNode<XYCoords>* nextPlotsNode(CLLNode<XYCoords>* pNode)
	{
		return m_plots.next(pNode);
	} // <advc.003s> Safer in 'for' loops
	CLLNode<XYCoords> const* nextPlotsNode(CLLNode<XYCoords> const* pNode)
	{
		return m_plots.next(pNode);
	} // </advc.003s>
	int getLengthPlots() const { return m_plots.getLength(); }
	CLLNode<XYCoords>* headPlotsNode() { return m_plots.head(); }

	// for serialization
	void read(FDataStreamBase* pStream);
	void write(FDataStreamBase* pStream);

protected:
	static int m_iRecalculating; // advc.064d
	int m_iID;
	PlayerTypes m_eOwner;
	ArrayEnumMap<BonusTypes,int,short> m_aiNumBonuses; // advc.enum
	CLinkList<XYCoords> m_plots;
};

#endif
