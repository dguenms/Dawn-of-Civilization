#pragma once

// CvDeal.h

#ifndef CIV4_DEAL_H
#define CIV4_DEAL_H


class CvDeal
{
public:

	CvDeal();
	~CvDeal();

	void init(int iID, PlayerTypes eFirstPlayer, PlayerTypes eSecondPlayer);
	void uninit();
	void reset(int iID = 0, PlayerTypes eFirstPlayer = NO_PLAYER, PlayerTypes eSecondPlayer = NO_PLAYER);

	DllExport void kill(bool bKillTeam = true)  // <advc.130p>
	{
		kill(bKillTeam, NO_PLAYER);
	}
	void kill(bool bKillTeam, PlayerTypes eCancelPlayer, // </advc.130p>
			bool bNoSound = false); // advc.002l
	// advc.036:
	void killSilent(bool bKillTeam = true, bool bUpdateAttitude = true,
			PlayerTypes eCancelPlayer = NO_PLAYER); // advc.130p
	void addTradeItems(CLinkList<TradeData>& kFirstList, CLinkList<TradeData>& kSecondList,
			bool bCheckAllowed);

	void doTurn();
	void verify();

	bool isPeaceDeal() const;
	// advc.130p: BtS function; now unused.
	//bool isPeaceDealBetweenOthers(CLinkList<TradeData>* pFirstList, CLinkList<TradeData>* pSecondList) const;
	// advc: Made public; could be useful elsewhere.
	static bool isVassalTrade(CLinkList<TradeData> const& kList);
	bool isVassalDeal() const;
	DllExport static bool isVassalTributeDeal(const CLinkList<TradeData>* pList);
	/*  advc: The above checks if pList contains only TRADE_RESSOURCE items;
		need a function that checks if this deal is a tribute deal between a vassal and a master. */
	bool isVassalTributeDeal() const;
	bool isDisengage() const; // advc.034

	DllExport int getID() const { return m_iID; }
	void setID(int iID);

	int getInitialGameTurn() const;
	void setInitialGameTurn(int iNewValue);
	int getAge() const; // advc.133
	// <advc.003s>
	/*	These two are exported via the .def file. Internally, one should use
		FOR_EACH_TRADE_ITEM(getFirstList()) instead, or just getFirstList. */
	CLLNode<TradeData>* headFirstTradesNodeExternal() const;
	CLLNode<TradeData>* nextFirstTradesNodeExternal(CLLNode<TradeData>* pNode) const;
	/*	These two are exported via the .def file. Internally, one should use
		use FOR_EACH_TRADE_ITEM(getSecondList()) instead, or just getSecondList. */
	CLLNode<TradeData>* headSecondTradesNodeExternal() const;
	CLLNode<TradeData>* nextSecondTradesNodeExternal(CLLNode<TradeData>* pNode) const;
	// </advc.003s> 
	DllExport PlayerTypes getFirstPlayer() const
	{
		return m_eFirstPlayer;
	}
	// advc: Renamed from "getFirstTrades"
	CLinkList<TradeData> const& getFirstList() const
	{
		return m_firstList;
	}
	DllExport PlayerTypes CvDeal::getSecondPlayer() const
	{
		return m_eSecondPlayer;
	}
	// advc: Renamed from "getSecondTrades"
	CLinkList<TradeData> const& getSecondList() const
	{
		return m_secondList;
	}

	// <advc> More convenient interface for iteration
	/*  Want to make all the CLLNodes const - should generally not modify deal lists
		while traversing them. (Though this means that CLLNode::m_data also can't be
		changed; make that mutable?) */
	bool isBetween(PlayerTypes ePlayer, PlayerTypes eOtherPlayer) const;
	bool isBetween(TeamTypes eTeam, TeamTypes eOtherTeam) const;
	bool isBetween(PlayerTypes ePlayer, TeamTypes eTeam) const;
	bool involves(PlayerTypes ePlayer) const;
	bool involves(TeamTypes eTeam) const;
	PlayerTypes getOtherPlayer(PlayerTypes ePlayer) const;
	// Caller has to ensure that ePlayer/ eTeam is involved in the trade!
	CLinkList<TradeData> const& getGivesList(PlayerTypes eGivingPlayer) const;
	CLinkList<TradeData> const& getGivesList(TeamTypes eGivingTeam) const;
	CLinkList<TradeData> const& getReceivesList(PlayerTypes eReceivingPlayer) const;
	CLinkList<TradeData> const& getReceivesList(TeamTypes eReceivingTeam) const;
	// </advc>
	// <advc.003j> Unused, let's keep it that way.
	//void clearFirstTrades();
	//void clearSecondTrades(); // </advc.003j>
	int getLengthFirst() const { return m_firstList.getLength(); }
	int getLengthSecond() const { return m_secondList.getLength(); }
	void insertAtEndFirst(TradeData item) // (currently only used internally)
	{
		m_firstList.insertAtEnd(item);
	}
	void insertAtEndSecond(TradeData item) // (currently only used internally)
	{
		m_secondList.insertAtEnd(item);
	}

	DllExport bool isCancelable(PlayerTypes eByPlayer = NO_PLAYER, CvWString* pszReason = NULL)
	// <advc> Need a const version
	{
		CvDeal const& kThis = *this;
		return kThis.isCancelable(eByPlayer, pszReason);
	} bool isCancelable(PlayerTypes eByPlayer = NO_PLAYER, CvWString* pszReason = NULL) const;
	// </advc>
	bool isEverCancelable(PlayerTypes eByPlayer) const; // advc.130f
	int turnsToCancel(PlayerTypes eByPlayer = NO_PLAYER) /* advc: */ const;
	bool isAllDual() const; // advc

	static bool isAnnual(TradeableItems eItem);
	DllExport static bool isDual(TradeableItems eItem, bool bExcludePeace = false);
	DllExport static bool hasData(TradeableItems eItem);
	DllExport static bool isEndWar(TradeableItems eItem);
	DllExport static bool isGold(TradeableItems eItem)
	{
		return (eItem == getGoldItem() || eItem == getGoldPerTurnItem());
	}
	static bool isVassal(TradeableItems eItem)
	{
		return (eItem == TRADE_VASSAL || eItem == TRADE_SURRENDER);
	}
	DllExport static TradeableItems getPeaceItem() { return TRADE_PEACE_TREATY; }
	DllExport static TradeableItems getGoldItem() { return TRADE_GOLD; }
	DllExport static TradeableItems getGoldPerTurnItem() { return TRADE_GOLD_PER_TURN; }

	void read(FDataStreamBase* pStream);
	void write(FDataStreamBase* pStream);

protected:
	// <advc> Python may modify - not the lists themselves - but the items
	friend class CyDeal;
	CLinkList<TradeData>& getFirstListVar()
	{
		return m_firstList;
	}
	CLinkList<TradeData>& getSecondListVar()
	{
		return m_secondList;
	} // </advc>

	bool startTrade(TradeData trade, PlayerTypes eFromPlayer, PlayerTypes eToPlayer,
			bool bPeace, bool& bPeaceTreatyImplied); // advc.ctr
	void endTrade(TradeData trade, PlayerTypes eFromPlayer, PlayerTypes eToPlayer, bool bTeam,
			bool bUpdateAttitude = true, // advc.036
			PlayerTypes eCancelPlayer = NO_PLAYER); // advc.130p
	void startTeamTrade(TradeableItems eItem, TeamTypes eFromTeam, TeamTypes eToTeam, bool bDual);
	void endTeamTrade(TradeableItems eItem, TeamTypes eFromTeam, TeamTypes eToTeam);
	void announceCancel(PlayerTypes eMsgTarget, PlayerTypes eOther, // advc
			bool bForce, // advc.106j
			bool bNoSound) const; // advc.002l
	bool verify(PlayerTypes eRecipient, PlayerTypes eGiver);
	// advc: was public
	bool isUncancelableVassalDeal(PlayerTypes eByPlayer, CvWString* pszReason = NULL) const;

	int m_iID;
	int m_iInitialGameTurn;

	PlayerTypes m_eFirstPlayer;
	PlayerTypes m_eSecondPlayer;

	CLinkList<TradeData> m_firstList;
	CLinkList<TradeData> m_secondList;
};

#endif
