// CvDeal.cpp

#include "CvGameCoreDLL.h"
#include "CvDeal.h"
#include "CoreAI.h"
#include "UWAIAgent.h" // advc.104
#include "CvCity.h"
#include "CvMap.h"
#include "CvUnit.h"
#include "CvGameTextMgr.h"
#include "CvInfo_Civics.h"
#include "CvInfo_Terrain.h" // just for a logBBAI call :(
#include "BBAILog.h" // BETTER_BTS_AI_MOD, AI logging, 10/02/09, jdog5000


CvDeal::CvDeal()
{
	reset();
}


CvDeal::~CvDeal()
{
	uninit();
}


void CvDeal::init(int iID, PlayerTypes eFirstPlayer, PlayerTypes eSecondPlayer)
{
	reset(iID, eFirstPlayer, eSecondPlayer); // Reset serialized data
	setInitialGameTurn(GC.getGame().getGameTurn());
}


void CvDeal::uninit()
{
	m_firstList.clear();
	m_secondList.clear();
}


// Initializes data members that are serialized.
void CvDeal::reset(int iID, PlayerTypes eFirstPlayer, PlayerTypes eSecondPlayer)
{
	uninit();

	m_iID = iID;
	m_iInitialGameTurn = 0;

	m_eFirstPlayer = eFirstPlayer;
	m_eSecondPlayer = eSecondPlayer;
}


void CvDeal::kill(bool bKillTeam, /* advc.130p: */ PlayerTypes eCancelPlayer,
	bool bNoSound) // advc.002l
{
	if (getLengthFirst() > 0 || getLengthSecond() > 0)
	{	// <advc.106j>
		bool bForce = false;
		FOR_EACH_TRADE_ITEM(getFirstList())
		{
			if(isDual(pItem->m_eItemType))
			{
				bForce = true;
				break;
			}
		}
		if (!GET_PLAYER(getFirstPlayer()).canTradeNetworkWith(getSecondPlayer()))
		{
			FOR_EACH_TRADE_ITEM(getFirstList())
			{
				if(pItem->m_eItemType == TRADE_RESOURCES)
				{
					bForce = true;
					break;
				}
			}
			if (!bForce)
			{
				FOR_EACH_TRADE_ITEM(getSecondList())
				{
					if(pItem->m_eItemType == TRADE_RESOURCES)
					{
						bForce = true;
						break;
					}
				}
			}
		} // </advc.106j>
		if (GET_TEAM(getFirstPlayer()).isHasMet(TEAMID(getSecondPlayer())))
		{
			// advc: Auxiliary function to remove duplicate code
			announceCancel(getFirstPlayer(), getSecondPlayer(), /* advc.106j: */ bForce,
					bNoSound); // advc.002l
			announceCancel(getSecondPlayer(), getFirstPlayer(), /* advc.106j: */ bForce,
					bNoSound); // advc.002l
		}
	}
	// <advc.036>
	killSilent(bKillTeam, /* advc.130p: */ true, eCancelPlayer);
}
// advc: Cut from 'kill' above
void CvDeal::announceCancel(PlayerTypes eMsgTarget, PlayerTypes eOther,
	bool bForce, // advc.106j
	bool bNoSound) const // advc.002l
{
	CvWString szString;
	CvWStringBuffer szDealString;
	CvWString szCancelString = gDLL->getText("TXT_KEY_POPUP_DEAL_CANCEL");
	GAMETEXT.getDealString(szDealString, *this, eMsgTarget, /* advc.004w: */ true);
	szString.Format(L"%s: %s", szCancelString.GetCString(), szDealString.getCString());
	gDLL->UI().addMessage(eMsgTarget, /* advc.106j: */ bForce,
			-1, szString,
			!bNoSound && // advc.002l
			bForce ? "AS2D_DEAL_CANCELLED" : NULL, // advc.106j
			// <advc.127b>
			MESSAGE_TYPE_INFO, NULL, NO_COLOR,
			GET_PLAYER(eOther).getCapitalX(eMsgTarget),
			GET_PLAYER(eOther).getCapitalY(eMsgTarget)); // </advc.127b>
}

void CvDeal::killSilent(bool bKillTeam, bool bUpdateAttitude, // </advc.036>
	PlayerTypes eCancelPlayer) // advc.130p
{
	FOR_EACH_TRADE_ITEM(getFirstList())
	{
		endTrade(*pItem, getFirstPlayer(), getSecondPlayer(), bKillTeam,
				bUpdateAttitude, // advc.036
				eCancelPlayer); // advc.130p
	}
	FOR_EACH_TRADE_ITEM(getSecondList())
	{
		endTrade(*pItem, getSecondPlayer(), getFirstPlayer(), bKillTeam,
				bUpdateAttitude, // advc.036
				eCancelPlayer); // advc.130p
	}
	GC.getGame().deleteDeal(getID());
}

// advc: renamed from "addTrades"
void CvDeal::addTradeItems(
	// advc (note): Not const b/c bHidden status of items can be changed
	CLinkList<TradeData>& kFirstList, CLinkList<TradeData>& kSecondList,
	bool bCheckAllowed)
{
	if (isVassalTrade(kFirstList) && isVassalTrade(kSecondList))
		return;
	if (bCheckAllowed) // advc.opt (moved up)
	{
		FOR_EACH_TRADE_ITEM_VAR(kFirstList)
		{
			if (!GET_PLAYER(getFirstPlayer()).canTradeItem(getSecondPlayer(), *pItem))
				return;
		}
		FOR_EACH_TRADE_ITEM_VAR(kSecondList)
		{
			if (!GET_PLAYER(getSecondPlayer()).canTradeItem(getFirstPlayer(), *pItem))
				return;
		}
	}
	// <advc.130p>
	TeamTypes eWarTradeTarget = NO_TEAM;
	TeamTypes ePeaceTradeTarget = NO_TEAM; // </advc.130p>
	bool bPeaceTreaty = false; // advc.ctr
	bool bPeaceTreatyFromTrade = false; // advc.ctr
	// <advc>
	CLinkList<TradeData>* apLists[] = { &kFirstList, &kSecondList };
	for (int i = 0; i < 2; i++)
	{
		FOR_EACH_TRADE_ITEM_VAR(*apLists[i])
		{	// <advc.130p>
			if(pItem->m_eItemType == TRADE_WAR)
				eWarTradeTarget = (TeamTypes)pItem->m_iData;
			else if(pItem->m_eItemType == TRADE_PEACE)
				ePeaceTradeTarget = (TeamTypes)pItem->m_iData;
			// </advc.130p>  <advc.104m> (cf. CvPlayer::buildTradeTable)
			if (pItem->m_eItemType == TRADE_PEACE_TREATY)
			{
				pItem->m_bHidden = pItem->m_bOffering = false;
				bPeaceTreaty = true;
				if (pItem->m_iData > 0) // Set in CvPlayer::updateTradeList
					bPeaceTreatyFromTrade = true;
			} // </advc.104m>
		}
	} // </advc>
	TeamTypes eFirstTeam = GET_PLAYER(getFirstPlayer()).getTeam();
	TeamTypes eSecondTeam = GET_PLAYER(getSecondPlayer()).getTeam();
	bool bBumpUnits = false; // K-Mod
	/*  <advc.130p> MakePeace calls moved down. Want to count trade value (partially)
		for peace deals, and I don't think AI_dealValue will work correctly when
		no longer at war. */
	bool const bMakingPeace = ::atWar(eFirstTeam, eSecondTeam);
	bool bUpdateAttitude = false;
	// advc.ctr:
	bool const bAIRequest = (bPeaceTreaty && !bPeaceTreatyFromTrade && !bMakingPeace);
	/*  Calls to changePeacetimeTradeValue moved into a new function
		(also for advc.ctr) */
	if (GET_PLAYER(getSecondPlayer()).AI_processTradeValue(kFirstList, getFirstPlayer(),
		kSecondList.getLength() <= 0, bMakingPeace, ePeaceTradeTarget, eWarTradeTarget,
		bAIRequest)) // advc.ctr
	{
		bUpdateAttitude = true;
	}
	if (GET_PLAYER(getFirstPlayer()).AI_processTradeValue(kSecondList, getSecondPlayer(),
		kFirstList.getLength() <= 0, bMakingPeace, ePeaceTradeTarget, eWarTradeTarget,
		bAIRequest)) // advc.ctr
	{
		bUpdateAttitude = true;
	}
	if (bMakingPeace)
	{
		bUpdateAttitude = true; // </advc.130p>
		// free vassals of capitulating team before peace is signed
		/*  advc.130y: Deleted; let CvTeam::setVassal free the vassals
			after signing peace */
		/*if (isVassalTrade(pSecondList))
		{ ... }
		else if (isVassalTrade(pFirstList)) // K-Mod added 'else'
		{ ... }*/

		//GET_TEAM(eFirstTeam).makePeace(eSecondTeam, !isVassalTrade(pFirstList) && !isVassalTrade(pSecondList));
		/*  K-Mod. Bump units only after all trades are completed, because some deals
			(such as city gifts) may affect which units get bumped. (originally,
			units were bumped automatically while executing the peace deal trades)
			Note: the original code didn't bump units for vassal trades. This can
			erroneously allow the vassal's units to stay in the master's land. */
		// <advc.039>
		bool bSurrender = isVassalTrade(kFirstList) || isVassalTrade(kSecondList);
		bool bDone = false;
		if(!bSurrender && GC.getDefineBOOL(CvGlobals::ANNOUNCE_REPARATIONS))
		{
			int iFirstLength = kFirstList.getLength();
			int iSecondLength = kSecondList.getLength();
			// Call makePeace on the recipient of reparations
			if(iFirstLength == 1 && iSecondLength > 1)
			{
				GET_TEAM(eFirstTeam).makePeace(eSecondTeam, false, NO_TEAM,
						false, &kSecondList);
				bDone = true;
			}
			else if(iSecondLength == 1 && iFirstLength > 1)
			{
				GET_TEAM(eSecondTeam).makePeace(eFirstTeam, false, NO_TEAM,
						false, &kFirstList);
				bDone = true;
			}
		}
		if(!bDone) // </advc.039>
		{
		// <advc.034>
			GET_TEAM(eFirstTeam).makePeace(eSecondTeam, false, NO_TEAM,
					bSurrender); // advc.039
		} // </advc.034>
		bBumpUnits = true;
		// K-Mod end
	}
	if(bUpdateAttitude) // advc.opt: Don't update unnecessarily
	{
		// K-Mod
		GET_PLAYER(getFirstPlayer()).AI_updateAttitude(getSecondPlayer());
		GET_PLAYER(getSecondPlayer()).AI_updateAttitude(getFirstPlayer());
		// K-Mod end
	}


	bool bAlliance = false;
    // doc: track deal outcomes for events
    bool bFirstSlaves = false;
    bool bSecondSlaves = false;
    int iFirstGold = 0;
    int iSecondGold = 0;
    bool bFirstPeace = false;
    bool bSecondPeace = false;
    bool bFirstTrade = false;
    bool bSecondTrade = false;
    bool bFirstSurrender = false;
    bool bSecondSurrender = false;

	// K-Mod. Vassal deals need to be implemented last, so that master/vassal power is set correctly.
	/*for (CLLNode<TradeData>* pNode = kFirstList.head(); pNode != NULL; pNode = kFirstList.next(pNode)) {
		if (isVassal(pNode->m_data.m_eItemType)) {
			pFirstList->moveToEnd(pNode);
			break;
		}
	}*/ // K-Mod end
	bool const bReportUWAI = getUWAI().isEnabled();
	bool bPeaceTreatyImplied = false; // advc.ctr
	// advc (fixme): This whole loop is mostly duplicated below
    if (!atWar(eFirstTeam, eSecondTeam)) // doc: prevent crash caused by war triggered by tech trade and subsequent peace treaty
    {
	    for (int iPass = 0; iPass < 2; iPass++) // advc: Replacing the K-Mod loop above
	    {
		    FOR_EACH_TRADE_ITEM(kFirstList)
		    {
			    if (isVassal(pItem->m_eItemType) == (iPass == 0))
				    continue;
			    // <advc.104> Allow UWAI to record the value of the sponsorship
			    if (bReportUWAI && pItem->m_eItemType == TRADE_WAR)
			    {
				    GET_PLAYER(getFirstPlayer()).uwai().getCache().
						    reportSponsoredWar(kSecondList, getSecondPlayer(),
						    (TeamTypes)pItem->m_iData);
			    } // </advc.104>
			    bool bSave = startTrade(*pItem, getFirstPlayer(), getSecondPlayer(),
					    bMakingPeace, bPeaceTreatyImplied); // advc.ctr
			    bBumpUnits = (bBumpUnits || pItem->m_eItemType == TRADE_PEACE); // K-Mod
			    if (bSave)
			        insertAtEndFirst(*pItem);

                // doc: track deal outcomes for events
                switch (pItem->m_eItemType)
                {
                case TRADE_PERMANENT_ALLIANCE:
                    bAlliance = true;
                    break;
                case TRADE_PEACE_TREATY:
                    bFirstPeace = true;
                    break;
                case TRADE_SLAVE:
                    bFirstTrade = true;
                    bFirstSlaves = true;
                    break;
                case TRADE_GOLD:
                    bFirstTrade = true;
                    iFirstGold += pItem->m_iData;
                    break;
                case TRADE_GOLD_PER_TURN:
                case TRADE_VASSAL:
                case TRADE_TECHNOLOGIES:
                case TRADE_RESOURCES:
                case TRADE_CITIES:
                    bFirstTrade = true;
                    break;
                case TRADE_SURRENDER:
                    bFirstSurrender = true;
                    break;
                }
		    }
	    }
    }
	/*	advc: Replacing deleted K-Mod code; tagging
		advc.001 b/c I think that code contained a copy-paste error. */
	if (!atWar(eFirstTeam, eSecondTeam)) // doc: prevent crash caused by war triggered by tech trade and subsequent peace treaty
    {
        for (int iPass = 0; iPass < 2; iPass++)
	    {
		    FOR_EACH_TRADE_ITEM(kSecondList)
		    {
			    if (isVassal(pItem->m_eItemType) == (iPass == 0))
				    continue;
			    // <advc.104> As above
			    if (bReportUWAI && pItem->m_eItemType == TRADE_WAR)
			    {
				    GET_PLAYER(getSecondPlayer()).uwai().getCache().
						    reportSponsoredWar(kFirstList, getFirstPlayer(),
						    (TeamTypes)pItem->m_iData);
			    } // </advc.104>
			    bool bSave = startTrade(*pItem, getSecondPlayer(), getFirstPlayer(),
					    bMakingPeace, bPeaceTreatyImplied); // advc.ctr
			    bBumpUnits = (bBumpUnits || pItem->m_eItemType == TRADE_PEACE); // K-Mod

			    if (bSave)
				    insertAtEndSecond(*pItem);

		        // doc: track deal outcomes for events
                switch (pItem->m_eItemType)
                {
                case TRADE_PERMANENT_ALLIANCE:
                    bAlliance = true;
                    break;
                case TRADE_PEACE_TREATY:
                    bSecondPeace = true;
                    break;
                case TRADE_SLAVE:
                    bSecondTrade = true;
                    bSecondSlaves = true;
                    break;
                case TRADE_GOLD:
                    bSecondTrade = true;
                    iSecondGold += pItem->m_iData;
                    break;
                case TRADE_GOLD_PER_TURN:
                case TRADE_VASSAL:
                case TRADE_TECHNOLOGIES:
                case TRADE_RESOURCES:
                case TRADE_CITIES:
                    bSecondTrade = true;
                    break;
                case TRADE_SURRENDER:
                    bSecondSurrender = true;
                    break;
                }
		    }
	    }
    }

    // doc: slave trade event
    if (bFirstSlaves)
        CvEventReporter::getInstance().playerSlaveTrade(getFirstPlayer(), iSecondGold);
    if (bSecondSlaves)
        CvEventReporter::getInstance().playerSlaveTrade(getSecondPlayer(), iFirstGold);

    // doc: tribute event
    if (bFirstPeace && bSecondPeace)
    {
        if (bSecondTrade && !bFirstTrade)
            CvEventReporter::getInstance().tribute(getSecondPlayer(), getFirstPlayer());
        if (bFirstTrade && !bSecondTrade)
            CvEventReporter::getInstance().tribute(getFirstPlayer(), getSecondPlayer());
    }
    else
    {
        if (bSecondSurrender && !bFirstTrade)
            CvEventReporter::getInstance().tribute(getSecondPlayer(), getFirstPlayer());
        if (bFirstSurrender && !bSecondTrade)
            CvEventReporter::getInstance().tribute(getFirstPlayer(), getSecondPlayer());
    }

	if (bAlliance)
	{
		if (eFirstTeam < eSecondTeam)
			GET_TEAM(eFirstTeam).addTeam(eSecondTeam);
		else if (eSecondTeam < eFirstTeam)
			GET_TEAM(eSecondTeam).addTeam(eFirstTeam);
	}
	/*	<advc.ctr> Can't do this directly in startTrade b/c the trade may
		(explicitly) include a peace treaty and then we may end up implementing
		only one half of that treaty before signing a 2nd treaty and end up with
		two unilateral treaties. */
	else if (bPeaceTreatyImplied)
		GET_TEAM(getFirstPlayer()).signPeaceTreaty(TEAMID(getSecondPlayer()));
	// </advc.ctr>
	// K-Mod
	if (bBumpUnits)
		GC.getMap().verifyUnitValidPlot();
	// K-Mod end
}


void CvDeal::doTurn()
{
	if (!isPeaceDeal() &&
	/*  <advc.130p> Open Borders and Defensive Pact have very small AI_dealVals.
		In (most?) other places, this doesn't matter b/c the AI never pays for
		these deals, but here it means that OB and DP have practically no impact
		on Grant and Trade values. I'm going to handle all isDual deals entirely
		in the CvPlayerAI::AI_get...Attitude functions and skip them here.
		In multiplayer, dual deals can be mixed with e.g. gold per turn, which is
		why I'm only skipping single-item deals. For mixed multiplayer deals,
		OB and DP will be counted as some value between 0 and 5, which is a bit
		messy, but not really a problem. */
		(getLengthSecond() != getLengthFirst() ||
		getLengthSecond() > 1 ||
		!isDual(getFirstList().head()->m_data.m_eItemType)) &&
		/*  The first ten turns of an annual deal are already counted when
			the deal is implemented */
		isCancelable()) // </advc.130p>
	{
		if (getLengthSecond() > 0)
		{
			int iValue = (GET_PLAYER(getFirstPlayer()).AI_dealVal(
					getSecondPlayer(), getSecondList()) /
					GC.getDefineINT(CvGlobals::PEACE_TREATY_LENGTH));
			if (getLengthFirst() > 0)
			{
				GET_PLAYER(getFirstPlayer()).AI_processPeacetimeTradeValue(
						getSecondPlayer(), iValue);
			}
			else
			{
				GET_PLAYER(getFirstPlayer()).AI_processPeacetimeGrantValue(
						getSecondPlayer(), iValue);
			}
		}

		if (getLengthFirst() > 0)
		{
			int iValue = (GET_PLAYER(getSecondPlayer()).AI_dealVal(
					getFirstPlayer(), getFirstList()) /
					GC.getDefineINT(CvGlobals::PEACE_TREATY_LENGTH));
			if (getLengthSecond() > 0)
			{
				GET_PLAYER(getSecondPlayer()).AI_processPeacetimeTradeValue(
						getFirstPlayer(), iValue, /* advc.130p: */ false);
			}
			else
			{
				GET_PLAYER(getSecondPlayer()).AI_processPeacetimeGrantValue(
						getFirstPlayer(), iValue, /* advc.130p: */ false);
			}
		}
		/*	K-Mod note: for balance reasons this function should probably
			be called at the boundary of some particular player's turn,
			rather than at the turn boundary of the game itself.
			-- Unfortunately, the game currently doesn't work like this.
			Also, note that we do not update attitudes of particular players here,
			but instead update all of them at the game turn boundary
			[advc: i.e. in CvGame::doDeals]. */
	}
}

// XXX probably should have some sort of message for the user or something...
void CvDeal::verify()
{
	// advc: Moved into auxiliary function to get rid of duplicate code
	if (!verify(getFirstPlayer(), getSecondPlayer()) ||
		!verify(getSecondPlayer(), getFirstPlayer()) ||
		(isCancelable(NO_PLAYER) && isPeaceDeal())) // advc.104m
	{
		kill();
	}
}

// advc: Cut from 'verify' above
bool CvDeal::verify(PlayerTypes eRecipient, PlayerTypes eGiver)
{
	CvPlayer& kGiver = GET_PLAYER(eGiver);
	FOR_EACH_TRADE_ITEM(getReceivesList(eRecipient))
	{
		if (pItem->m_eItemType == TRADE_RESOURCES)
		{
			BonusTypes eBonus = (BonusTypes)pItem->m_iData;
			// XXX embargoes? // advc.130f (note): Handled by CvPlayer::stopTradingWithTeam
			if ((kGiver.getNumTradeableBonuses(eBonus) < 0) ||
				!kGiver.canTradeNetworkWith(eRecipient) ||
				GET_TEAM(kGiver.getTeam()).isBonusObsolete(eBonus) ||
				GET_TEAM(eRecipient).isBonusObsolete(eBonus))
			{
				return false;
			}
		}
		// <advc.133> Force-cancel GPT deals when broke
		if (pItem->m_eItemType == TRADE_GOLD_PER_TURN)
		{
			if (kGiver.getCommercePercent(COMMERCE_GOLD) >= 100 &&
				kGiver.getGold() < pItem->m_iData && !kGiver.isAnarchy() &&
				kGiver.calculateGoldRate() < 0)
			{
				return false;
			}
		} // </advc.133>
	}
	return true;
}


bool CvDeal::isPeaceDeal() const  // advc: simplified
{
	FOR_EACH_TRADE_ITEM(getFirstList())
	{
		if (pItem->m_eItemType == getPeaceItem())
			return true;
	}
	return false;
}


bool CvDeal::isVassalDeal() const
{
	return (isVassalTrade(m_firstList) || isVassalTrade(m_secondList));
}


bool CvDeal::isVassalTrade(CLinkList<TradeData> const& kList)
{
	FOR_EACH_TRADE_ITEM(kList)
	{
		if (isVassal(pItem->m_eItemType))
			return true;
	}
	return false;
}

/*	advc.001: Rewrote this function. The BtS code was (even more) convoluted,
	inefficient and contained at least one bug.
	(The first player was passed to setVassalRevoltHelp as eVassal even if the
	first player was on the eMaster team; copy-paste error probably.) */
bool CvDeal::isUncancelableVassalDeal(PlayerTypes eByPlayer, CvWString* pszReason) const
{
	FAssertMsg(involves(eByPlayer), "Caller should have ensured this");
	// Vassal and master (technically) have the same master
	TeamTypes const eMaster = GET_PLAYER(getFirstPlayer()).getMasterTeam();
	if (eMaster != GET_PLAYER(getSecondPlayer()).getMasterTeam())
		return false; // There is no vassal deal, so this can't be one.
	TeamTypes eVassal;
	if (GET_TEAM(getFirstPlayer()).isVassal(eMaster))
		eVassal = TEAMID(getFirstPlayer());
	else if(GET_TEAM(getSecondPlayer()).isVassal(eMaster))
		eVassal = TEAMID(getSecondPlayer());
	else return false; // sibling vassals
	if (TEAMID(getFirstPlayer()) == TEAMID(getSecondPlayer()))
		return false; // headGivesNode(TeamTypes) can't handle deals within a team
	FOR_EACH_TRADE_ITEM(getGivesList(eVassal))
	{
		if (!isVassal(pItem->m_eItemType))
			continue;

        // doc: master can cancel
		/*if (TEAMID(eByPlayer) == eMaster) // Master can never cancel
		{
			if (pszReason)
				*pszReason += gDLL->getText("TXT_KEY_MISC_DEAL_NO_CANCEL_EVER");
			return true;
		}
		FAssert(TEAMID(eByPlayer) == eVassal);*/
		// Voluntary vassal can always cancel
		if (pItem->m_eItemType != TRADE_SURRENDER)
			return false;

		if (!GET_TEAM(eVassal).canVassalRevolt(eMaster))
		{
			if (pszReason)
			{
				CvWStringBuffer szBuffer;
				GAMETEXT.setVassalRevoltHelp(szBuffer, eMaster, eVassal);
				*pszReason = szBuffer.getCString();
			}
			return true;
		}
		return false; // Assume at most one vassal item per deal
	}
	return false;
}


bool CvDeal::isVassalTributeDeal(CLinkList<TradeData> const* pList)
{
	FOR_EACH_TRADE_ITEM(*pList)
	{
		if (pItem->m_eItemType != TRADE_RESOURCES)
			return false;
	}
	return true;
}

/*  advc: True if one side is the other side's vassal, and the vassal gives
	only resources, and the master gives nothing in return. */
bool CvDeal::isVassalTributeDeal() const
{
	PlayerTypes eVassalPlayer = NO_PLAYER;
	PlayerTypes eMasterPlayer = NO_PLAYER;
	if(GET_TEAM(getFirstPlayer()).isVassal(TEAMID(getSecondPlayer())))
	{
		eVassalPlayer = getFirstPlayer();
		eMasterPlayer = getSecondPlayer();
	}
	else if(GET_TEAM(getSecondPlayer()).isVassal(TEAMID(getFirstPlayer())))
	{
		eVassalPlayer = getSecondPlayer();
		eMasterPlayer = getFirstPlayer();
	}
	return eVassalPlayer != NO_PLAYER && getGivesList(eMasterPlayer).getLength() <= 0 &&
			CvDeal::isVassalTributeDeal(&getGivesList(eVassalPlayer));
}

// advc.034:
bool CvDeal::isDisengage() const
{
	return (getLengthFirst() == 1 && getLengthSecond() == 1 &&
			getFirstList().head()->m_data.m_eItemType == TRADE_DISENGAGE);
}

// advc.130p: Replaced by code in CvPlayerAI::AI_processTradeValue
/*bool CvDeal::isPeaceDealBetweenOthers(CLinkList<TradeData>* pFirstList, CLinkList<TradeData>* pSecondList) const {
//... }*/

void CvDeal::setID(int iID)
{
	m_iID = iID;
}


int CvDeal::getInitialGameTurn() const
{
	return m_iInitialGameTurn;
}


void CvDeal::setInitialGameTurn(int iNewValue)
{
	m_iInitialGameTurn = iNewValue;
}

// advc.133:
int CvDeal::getAge() const
{
	return GC.getGame().getGameTurn() - getInitialGameTurn();
}


CLLNode<TradeData>* CvDeal::headFirstTradesNodeExternal() const
{
	return m_firstList.head();
}


CLLNode<TradeData>* CvDeal::nextFirstTradesNodeExternal(CLLNode<TradeData>* pNode) const
{
	return m_firstList.next(pNode);
}


CLLNode<TradeData>* CvDeal::headSecondTradesNodeExternal() const
{
	return m_secondList.head();
}


CLLNode<TradeData>* CvDeal::nextSecondTradesNodeExternal(CLLNode<TradeData>* pNode) const
{
	return m_secondList.next(pNode);
}

// <advc> Might be important here that getFirstPlayer and getSecondPlayer are inlined
bool CvDeal::isBetween(PlayerTypes ePlayer, PlayerTypes eOtherPlayer) const
{
	return (ePlayer == getFirstPlayer() && eOtherPlayer == getSecondPlayer()) ||
		   (eOtherPlayer == getFirstPlayer() && ePlayer == getSecondPlayer());
}


bool CvDeal::isBetween(TeamTypes eTeam, TeamTypes eOtherTeam) const
{
	return (eTeam == TEAMID(getFirstPlayer()) && eOtherTeam == TEAMID(getSecondPlayer())) ||
		   (eOtherTeam == TEAMID(getFirstPlayer()) && eTeam == TEAMID(getSecondPlayer()));
}


bool CvDeal::isBetween(PlayerTypes ePlayer, TeamTypes eTeam) const
{
	return (ePlayer == getFirstPlayer() && eTeam == TEAMID(getSecondPlayer())) ||
		   (eTeam == TEAMID(getFirstPlayer()) && ePlayer == getSecondPlayer());
}


bool CvDeal::involves(PlayerTypes ePlayer) const
{
	return (getFirstPlayer() == ePlayer || getSecondPlayer() == ePlayer);
}


bool CvDeal::involves(TeamTypes eTeam) const
{
	return (TEAMID(getFirstPlayer()) == eTeam || TEAMID(getSecondPlayer()) == eTeam);
}


PlayerTypes CvDeal::getOtherPlayer(PlayerTypes ePlayer) const
{
	FAssert(ePlayer == getFirstPlayer() || ePlayer == getSecondPlayer());
	return (ePlayer == getFirstPlayer() ? getSecondPlayer() : getFirstPlayer());
}


CLinkList<TradeData> const& CvDeal::getGivesList(PlayerTypes eGivingPlayer) const {

	FAssert(eGivingPlayer == getFirstPlayer() || eGivingPlayer == getSecondPlayer());
	return (eGivingPlayer == getFirstPlayer() ? getFirstList() : getSecondList());
}


CLinkList<TradeData> const& CvDeal::getGivesList(TeamTypes eGivingTeam) const
{
	FAssert((TEAMID(getFirstPlayer()) == eGivingTeam) != (TEAMID(getSecondPlayer()) == eGivingTeam));
	return (TEAMID(getFirstPlayer()) == eGivingTeam ? getFirstList() : getSecondList());
}


CLinkList<TradeData> const& CvDeal::getReceivesList(PlayerTypes eReceivingPlayer) const
{
	FAssert(eReceivingPlayer == getFirstPlayer() || eReceivingPlayer == getSecondPlayer());
	return (eReceivingPlayer == getFirstPlayer() ? getSecondList() : getFirstList());
}


CLinkList<TradeData> const& CvDeal::getReceivesList(TeamTypes eReceivingTeam) const
{
	FAssert((TEAMID(getFirstPlayer()) == eReceivingTeam) != (TEAMID(getSecondPlayer()) == eReceivingTeam));
	return (TEAMID(getFirstPlayer()) == eReceivingTeam ? getSecondList() : getFirstList());
} // </advc>


void CvDeal::write(FDataStreamBase* pStream)
{
	PROFILE_FUNC(); // advc
	uint uiFlag=0;
	pStream->Write(uiFlag);
	REPRO_TEST_BEGIN_WRITE(CvString::format("Deal(%d,%d,%d)", getID(), getFirstPlayer(), getSecondPlayer()));
	pStream->Write(m_iID);
	pStream->Write(m_iInitialGameTurn);

	pStream->Write(m_eFirstPlayer);
	pStream->Write(m_eSecondPlayer);

	m_firstList.Write(pStream);
	m_secondList.Write(pStream);
	REPRO_TEST_END_WRITE();
}

void CvDeal::read(FDataStreamBase* pStream)
{
	uint uiFlag=0;
	pStream->Read(&uiFlag);

	pStream->Read(&m_iID);
	pStream->Read(&m_iInitialGameTurn);

	pStream->Read((int*)&m_eFirstPlayer);
	pStream->Read((int*)&m_eSecondPlayer);

	m_firstList.Read(pStream);
	m_secondList.Read(pStream);
}

// Returns true if the trade should be saved...
bool CvDeal::startTrade(TradeData trade, PlayerTypes eFromPlayer, PlayerTypes eToPlayer,
	bool bPeace, bool& bPeaceTreatyImplied) // advc.ctr
{
	PROFILE_FUNC();
	CvPlayerAI& kFromPlayer = GET_PLAYER(eFromPlayer);
	CvPlayerAI& kToPlayer = GET_PLAYER(eToPlayer);
	bool bSave = false;

	switch (trade.m_eItemType)
	{
	case TRADE_TECHNOLOGIES:
	{
		// <advc.550e> Code moved into subroutine and modified there
		bool const bSignificantTech = kToPlayer.isSignificantDiscovery(
				(TechTypes)trade.m_iData); // </advc.550e>
		GET_TEAM(eToPlayer).setHasTech((TechTypes)trade.m_iData, true, eToPlayer, true, true);
		if (bSignificantTech) // advc.550e
			GET_TEAM(eToPlayer).setNoTradeTech((TechTypes)trade.m_iData, true);
		if (gTeamLogLevel >= 2) logBBAI("    Player %d (%S) trades tech %S to player %d (%S)", eFromPlayer, kFromPlayer.getCivilizationDescription(0), GC.getInfo((TechTypes)trade.m_iData).getDescription(), eToPlayer, kToPlayer.getCivilizationDescription(0));
		// advc.550e: (K-Mod had checked this only for MEMORY_RECEIVED_TECH_FROM_ANY)
		if (bSignificantTech)
		{
			for (MemberAIIter itToMember(kToPlayer.getTeam());
				itToMember.hasNext(); ++itToMember)
			{
				itToMember->AI_changeMemoryCount(eFromPlayer, MEMORY_TRADED_TECH_TO_US, 1);
			}
			for (PlayerAIIter<MAJOR_CIV,OTHER_KNOWN_TO> itThird(kToPlayer.getTeam());
				itThird.hasNext(); ++itThird)
			{
				itThird->AI_changeMemoryCount(eToPlayer, MEMORY_RECEIVED_TECH_FROM_ANY, 1);
			}
		}
		break;
	}

	case TRADE_RESOURCES:
	{
		kFromPlayer.changeBonusExport((BonusTypes)trade.m_iData, 1);
		kToPlayer.changeBonusImport((BonusTypes)trade.m_iData, 1);
		if (gTeamLogLevel >= 2) logBBAI("    Player %d (%S) trades bonus type %S due to TRADE_RESOURCES with %d (%S)", eFromPlayer, kFromPlayer.getCivilizationDescription(0), GC.getInfo((BonusTypes)trade.m_iData).getDescription(), eToPlayer, kToPlayer.getCivilizationDescription(0));
		bSave = true;
		break;
	}
	case TRADE_CITIES:
	{
		CvCity* pCity = kFromPlayer.getCity(trade.m_iData);
		if (pCity != NULL)
		{
			bool bLib = (pCity->getLiberationPlayer() == eToPlayer); // advc.ctr
			if (gTeamLogLevel >= 2) logBBAI("    Player %d (%S) gives a city due to TRADE_CITIES with %d (%S)", eFromPlayer, kFromPlayer.getCivilizationDescription(0), eToPlayer, kToPlayer.getCivilizationDescription(0));
			pCity->doTask(/* advc.ctr: */ bPeace ? TASK_CEDE :
					TASK_GIFT, eToPlayer);
			// <advc.ctr>
			if (!bPeace && !bLib)
			{
				FAssert(!GET_TEAM(eFromPlayer).isAtWar(kToPlayer.getTeam()));
				bPeaceTreatyImplied = true;
			} // </advc.ctr>
		}
		break;
	}

	// doc (edead): slave trade based on Afforess' Advanced Diplomacy
	case TRADE_SLAVE:
	{
		CvUnit* pUnit = GET_PLAYER(eFromPlayer).getUnit(trade.m_iData);
		if (pUnit != NULL)
		{
			if (pUnit->isCargo())
				pUnit->unload();
			pUnit->tradeUnit(eToPlayer);
		}
		break;
	}

	case TRADE_GOLD:
		kFromPlayer.changeGold(-trade.m_iData);
		kToPlayer.changeGold(trade.m_iData);
		kFromPlayer.AI_changeGoldTradedTo(eToPlayer, trade.m_iData);
		if (gTeamLogLevel >= 2) logBBAI("    Player %d (%S) trades gold %d due to TRADE_GOLD with player %d (%S)", eFromPlayer, kFromPlayer.getCivilizationDescription(0), trade.m_iData, eToPlayer, kToPlayer.getCivilizationDescription(0));
		CvEventReporter::getInstance().playerGoldTrade(eFromPlayer, eToPlayer, trade.m_iData);
		break;

	case TRADE_GOLD_PER_TURN:
		kFromPlayer.changeGoldPerTurnByPlayer(eToPlayer, -(trade.m_iData));
		kToPlayer.changeGoldPerTurnByPlayer(eFromPlayer, trade.m_iData);
		if (gTeamLogLevel >= 2) logBBAI("    Player %d (%S) trades gold per turn %d due to TRADE_GOLD_PER_TURN with player %d (%S)", eFromPlayer, kFromPlayer.getCivilizationDescription(0), trade.m_iData, eToPlayer, kToPlayer.getCivilizationDescription(0));
		bSave = true;
		break;

	case TRADE_MAPS:
	{	// <advc.003o>
		#ifdef PROFILE_AI_AUTO_PLAY
		/*	Implementing map trades for the active player is very slow due to
			graphics updates, which, it seems could only be optimized in the EXE.
			Don't want that to skew DLL profiling on AI Auto Play. */
		if (GC.getGame().getAIAutoPlay() > 0 &&
			GC.getGame().getActiveTeam() == kToPlayer.getTeam())
		{
			break;
		}
		#endif
		// </advc.003o>
		PROFILE("CvDeal::startTrade.MAPS"); // advc
		CvMap const& kMap = GC.getMap();
		for (int i = 0; i < kMap.numPlots(); i++)
		{
			CvPlot& kPlot = kMap.getPlotByIndex(i);
			if (kPlot.isRevealed(kFromPlayer.getTeam()))
				kPlot.setRevealed(kToPlayer.getTeam(), true, false, kFromPlayer.getTeam(), false);
		}
		for (MemberIter it(kToPlayer.getTeam()); it.hasNext(); ++it)
		{
			it->updatePlotGroups();
		}
		if (gTeamLogLevel >= 2) logBBAI("    Player %d (%S) trades maps due to TRADE_MAPS with player %d (%S)", eFromPlayer, kFromPlayer.getCivilizationDescription(0), eToPlayer, kToPlayer.getCivilizationDescription(0));
		break;
	}
	case TRADE_SURRENDER:
	case TRADE_VASSAL:
		if (trade.m_iData <= 0) // advc: Was ==. Important b/c I've changed the default value from 0 to -1.
		{
			startTeamTrade(trade.m_eItemType, kFromPlayer.getTeam(), kToPlayer.getTeam(), false);
			GET_TEAM(eFromPlayer).setVassal(kToPlayer.getTeam(), true, TRADE_SURRENDER == trade.m_eItemType);
			if (gTeamLogLevel >= 2)
			{
				if (TRADE_SURRENDER == trade.m_eItemType) logBBAI("    Player %d (%S) trades themselves as vassal due to TRADE_SURRENDER with player %d (%S)", eFromPlayer, kFromPlayer.getCivilizationDescription(0), eToPlayer, kToPlayer.getCivilizationDescription(0));
				else logBBAI("    Player %d (%S) trades themselves as vassal due to TRADE_VASSAL with player %d (%S)", eFromPlayer, kFromPlayer.getCivilizationDescription(0), eToPlayer, kToPlayer.getCivilizationDescription(0));
			}
		}
		else bSave = true;

		break;

	case TRADE_PEACE:
		if (gTeamLogLevel >= 2) logBBAI("    Team %d (%S) makes peace with team %d due to TRADE_PEACE with %d (%S)", kFromPlayer.getTeam(), kFromPlayer.getCivilizationDescription(0), trade.m_iData, eToPlayer, kToPlayer.getCivilizationDescription(0));
		//GET_TEAM(eFromPlayer).makePeace((TeamTypes)trade.m_iData);
		// K-Mod. (units will be bumped after the rest of the trade deals are completed.)
		// <advc.100b>
		GET_TEAM(eFromPlayer).makePeace((TeamTypes)trade.m_iData, false, kToPlayer.getTeam());
		// K-Mod. Use a standard peace treaty rather than a simple cease-fire.
		GET_TEAM(eFromPlayer).signPeaceTreaty((TeamTypes)trade.m_iData);
		// </advc.100b>
		/*	K-Mod todo: this team should offer something fair to the peace-team
			if this teams endWarVal is higher. */
        // doc: peace brokered event
	    CvEventReporter::getInstance().peaceBrokered(eToPlayer, eFromPlayer, GET_TEAM((TeamTypes)trade.m_iData).getLeaderID());
		break;

	case TRADE_WAR:
	{
		if (gTeamLogLevel >= 2) logBBAI("    Team %d (%S) declares war on team %d due to TRADE_WAR with %d (%S)", kFromPlayer.getTeam(), kFromPlayer.getCivilizationDescription(0), trade.m_iData, eToPlayer, kToPlayer.getCivilizationDescription(0));
		TeamTypes const eAttackedTeam = (TeamTypes)trade.m_iData;
		GET_TEAM(eFromPlayer).declareWar(eAttackedTeam, true, NO_WARPLAN,
				true, eToPlayer); // advc.100
		bPeaceTreatyImplied = true; // advc.146
		for (MemberAIIter itAttackedMember(eAttackedTeam);
			itAttackedMember.hasNext(); ++itAttackedMember)
		{
			// advc.130j:
			itAttackedMember->AI_rememberEvent(eToPlayer, MEMORY_HIRED_WAR_ALLY);
			// <advc.104i> Similar to code in CvTeam::makeUnwillingToTalk
			if (itAttackedMember->AI_getMemoryCount(eFromPlayer, MEMORY_DECLARED_WAR_RECENT) < 2)
				itAttackedMember->AI_rememberEvent(eFromPlayer, MEMORY_DECLARED_WAR_RECENT);
			if (GET_TEAM(eToPlayer).isAtWar(eAttackedTeam) &&
				itAttackedMember->AI_getMemoryCount(eToPlayer, MEMORY_DECLARED_WAR_RECENT) < 2)
			{
				itAttackedMember->AI_rememberEvent(eToPlayer, MEMORY_DECLARED_WAR_RECENT);
			} // </advc.104i>
		}
		break;
	}
	case TRADE_EMBARGO:
	{
		TeamTypes const eTargetTeam = (TeamTypes)trade.m_iData;
		kFromPlayer.stopTradingWithTeam(eTargetTeam);
		/*	<advc.130f> The instigator needs to stop too. (If an AI suggested
			the embargo to a human, that's not handled here but by CvPlayer::handleDiploEvent.) */
		if (!GET_TEAM(eFromPlayer).isCapitulated() || !GET_TEAM(eFromPlayer).isVassal(kToPlayer.getTeam()))
			kToPlayer.stopTradingWithTeam(eTargetTeam, false);
		// </advc.130f>
		for (MemberAIIter itTargetMember(eTargetTeam);
			itTargetMember.hasNext(); ++itTargetMember)
		{	// advc.130j:
			itTargetMember->AI_rememberEvent(eToPlayer, MEMORY_HIRED_TRADE_EMBARGO);
		}
		if (gTeamLogLevel >= 2) logBBAI("    Player %d (%S) signs embargo against team %d due to TRADE_EMBARGO with player %d (%S)", eFromPlayer, kFromPlayer.getCivilizationDescription(0), (TeamTypes)trade.m_iData, eToPlayer, kToPlayer.getCivilizationDescription(0));
		break;
	}
	case TRADE_CIVIC:
	{
		CivicMap aeNewCivics;
		kFromPlayer.getCivics(aeNewCivics);
		CivicTypes const eCivic = (CivicTypes)trade.m_iData;
		aeNewCivics.set(GC.getInfo(eCivic).getCivicOptionType(), eCivic);
		kFromPlayer.revolution(aeNewCivics, true);
		if (kFromPlayer.AI_getCivicTimer() < GC.getDefineINT(CvGlobals::PEACE_TREATY_LENGTH))
			kFromPlayer.AI_setCivicTimer(GC.getDefineINT(CvGlobals::PEACE_TREATY_LENGTH));
		if (gTeamLogLevel >= 2) logBBAI("    Player %d (%S) switched civics due to TRADE_CIVICS with player %d (%S)", eFromPlayer, kFromPlayer.getCivilizationDescription(0), eToPlayer, kToPlayer.getCivilizationDescription(0));
		break;
	}
	case TRADE_RELIGION:
		kFromPlayer.convert((ReligionTypes)trade.m_iData, /* advc.001v: */ true);
		if (kFromPlayer.AI_getReligionTimer() < GC.getDefineINT(CvGlobals::PEACE_TREATY_LENGTH))
			kFromPlayer.AI_setReligionTimer(GC.getDefineINT(CvGlobals::PEACE_TREATY_LENGTH));
		if (gTeamLogLevel >= 2) logBBAI("    Player %d (%S) switched religions due to TRADE_RELIGION with player %d (%S)", eFromPlayer, kFromPlayer.getCivilizationDescription(0), eToPlayer, kToPlayer.getCivilizationDescription(0));
		break;

	case TRADE_OPEN_BORDERS:
		if (trade.m_iData <= 0) // advc: was ==
		{
			// <advc.032>
			if (GET_TEAM(eFromPlayer).isOpenBorders(kToPlayer.getTeam()))
			{
				if (kFromPlayer.resetDualDeal(eToPlayer, TRADE_OPEN_BORDERS))
				{
					if (gTeamLogLevel >= 2) logBBAI("    Player %d (%S_1) prolongs open borders with player %d (%S_2)", eFromPlayer, kFromPlayer.getCivilizationDescription(0), eToPlayer, kToPlayer.getCivilizationDescription(0));
					break;
				}
			} // </advc.032>
			startTeamTrade(TRADE_OPEN_BORDERS, kFromPlayer.getTeam(), kToPlayer.getTeam(), true);
			GET_TEAM(eFromPlayer).setOpenBorders(kToPlayer.getTeam(), true);
			if (gTeamLogLevel >= 2) logBBAI("    Player %d (%S_1) signs open borders due to TRADE_OPEN_BORDERS with player %d (%S_2)", eFromPlayer, kFromPlayer.getCivilizationDescription(0), eToPlayer, kToPlayer.getCivilizationDescription(0));
		}
		else bSave = true;
		break;

	case TRADE_DEFENSIVE_PACT:
		if (trade.m_iData <= 0) // advc: was ==
		{
			// <advc.032>
			if (GET_TEAM(eFromPlayer).isDefensivePact(kToPlayer.getTeam()))
			{
				if (kFromPlayer.resetDualDeal(eToPlayer, TRADE_DEFENSIVE_PACT))
				{
					if (gTeamLogLevel >= 2) logBBAI("    Player %d (%S) prolongs defensive pact with player %d (%S)", eFromPlayer, kFromPlayer.getCivilizationDescription(0), eToPlayer, kToPlayer.getCivilizationDescription(0));
					break;
				}
			} // </advc.032>
			startTeamTrade(TRADE_DEFENSIVE_PACT, kFromPlayer.getTeam(), kToPlayer.getTeam(), true);
			GET_TEAM(eFromPlayer).setDefensivePact(kToPlayer.getTeam(), true);
			if (gTeamLogLevel >= 2) logBBAI("    Player %d (%S) signs defensive pact due to TRADE_DEFENSIVE_PACT with player %d (%S)", eFromPlayer, kFromPlayer.getCivilizationDescription(0), eToPlayer, kToPlayer.getCivilizationDescription(0));
		}
		else bSave = true;
		break;

	case TRADE_PERMANENT_ALLIANCE:
		break;

	case TRADE_PEACE_TREATY:
		// <advc.032>
		if (GET_TEAM(eFromPlayer).isForcePeace(kToPlayer.getTeam()))
		{
			if (kFromPlayer.resetDualDeal(eToPlayer, TRADE_PEACE_TREATY))
			{
				if (gTeamLogLevel >= 2) logBBAI("    Player %d (%S) prolongs peace treaty with player %d (%S)", eFromPlayer, kFromPlayer.getCivilizationDescription(0), eToPlayer, kToPlayer.getCivilizationDescription(0));
				break;
			}
		} // </advc.032>
		GET_TEAM(eFromPlayer).setForcePeace(kToPlayer.getTeam(), true);
		if (gTeamLogLevel >= 2) logBBAI("    Player %d (%S) signs peace treaty due to TRADE_PEACE_TREATY with player %d (%S)", eFromPlayer, kFromPlayer.getCivilizationDescription(0), eToPlayer, kToPlayer.getCivilizationDescription(0));
		bSave = true;
		break;
	// <advc.034>
	case TRADE_DISENGAGE:
		if(trade.m_iData <= 0)
		{
			startTeamTrade(TRADE_DISENGAGE, kFromPlayer.getTeam(),
					kToPlayer.getTeam(), true);
			GET_TEAM(eFromPlayer).setDisengage(kToPlayer.getTeam(), true);
		}
		else bSave = true;
		break;
	// </advc.034>
	default:
		FAssert(false);
	}

	return bSave;
}

// advc.130p: Cut from CvDeal::endTrade
namespace
{
	void addEndTradeMemory(PlayerTypes eEndingPlayer, PlayerTypes eRememberingPlayer,
		TradeableItems eItemType, /* advc.130j: */ bool bHalve = false)
	{
		for (MemberAIIter itRememberingMember(TEAMID(eRememberingPlayer));
			itRememberingMember.hasNext(); ++itRememberingMember)
		{
			for (MemberIter itEndingMember(TEAMID(eEndingPlayer));
				itEndingMember.hasNext(); ++itEndingMember)
			{
				MemoryTypes eMemory = MEMORY_CANCELLED_OPEN_BORDERS;
				if (eItemType == TRADE_DEFENSIVE_PACT)
					eMemory = MEMORY_CANCELLED_DEFENSIVE_PACT;
				else if(eItemType == TRADE_VASSAL)
					eMemory = MEMORY_CANCELLED_VASSAL_AGREEMENT;
				/*	<advc.130j> Twice remembered (unless remembering it only half)
					b/c now twice as fast forgotten. */
				itRememberingMember->AI_setMemoryCount(itEndingMember->getID(),
						eMemory, bHalve ? 1 : 2); // </advc.130j>
			}
		}
	}
}


void CvDeal::endTrade(TradeData trade, PlayerTypes eFromPlayer,
	PlayerTypes eToPlayer, bool bTeam, /* advc.036: */ bool bUpdateAttitude,
	PlayerTypes eCancelPlayer) // advc.130p
{
	bool bTeamTradeEnded = false; // advc.133
	/*	<advc> Skip some steps when a trade ends through the defeat of one party -
		to avoid failed assertions */
	bool const bAlive = (GET_PLAYER(eFromPlayer).isAlive() &&
			GET_PLAYER(eToPlayer).isAlive());
	if (!bAlive)
		bUpdateAttitude = false; // </advc>
	switch(trade.m_eItemType)
	{
	case TRADE_RESOURCES:
		GET_PLAYER(eToPlayer).changeBonusImport((BonusTypes)trade.m_iData, -1);
		GET_PLAYER(eFromPlayer).changeBonusExport((BonusTypes)trade.m_iData, -1);
		break;

	case TRADE_GOLD_PER_TURN:
		GET_PLAYER(eFromPlayer).changeGoldPerTurnByPlayer(eToPlayer, trade.m_iData);
		GET_PLAYER(eToPlayer).changeGoldPerTurnByPlayer(eFromPlayer, -trade.m_iData);
		break;

	// <advc.143>
	case TRADE_VASSAL:
	case TRADE_SURRENDER:
	{
		if (!bAlive)
			break;
		bool bSurrender = (trade.m_eItemType == TRADE_SURRENDER);
		// Canceled b/c of failure to protect vassal?
		bool bDeniedHelp = false;
		if(bSurrender)
		{
			bDeniedHelp = (GET_TEAM(eFromPlayer).isLossesAllowRevolt(TEAMID(eToPlayer)) &&
					// Doesn't count if losses obviously only from cultural borders
					GET_TEAM(eFromPlayer).AI_isAnyWarPlan());
		}
		else
		{
			DenialTypes eReason = GET_TEAM(eFromPlayer).
					AI_surrenderTrade(TEAMID(eToPlayer));
			bDeniedHelp = (eReason == DENIAL_POWER_YOUR_ENEMIES);
		}
		GET_TEAM(eFromPlayer).setVassal(TEAMID(eToPlayer), false, bSurrender);
		if(bTeam)
		{
			if(bSurrender)
				endTeamTrade(TRADE_SURRENDER, TEAMID(eFromPlayer), TEAMID(eToPlayer));
			else endTeamTrade(TRADE_VASSAL, TEAMID(eFromPlayer), TEAMID(eToPlayer));
			bTeamTradeEnded = true; // advc.133
		}
		addEndTradeMemory(eFromPlayer, eToPlayer, TRADE_VASSAL);
		if(!bDeniedHelp) // Master remembers for 2x10 turns
			addEndTradeMemory(eFromPlayer, eToPlayer, TRADE_VASSAL);
		else /* Vassal remembers for 3x10 turns (and master for 1x10 turns,
				which could matter when a human becomes a vassal) */
		{
			for(int i = 0; i < 3; i++)
				addEndTradeMemory(eToPlayer, eFromPlayer, TRADE_VASSAL);
		}
		break;
	} // </advc.143>
	case TRADE_OPEN_BORDERS:
		GET_TEAM(eFromPlayer).setOpenBorders(TEAMID(eToPlayer), false);
		if(bTeam)
		{
			endTeamTrade(TRADE_OPEN_BORDERS, TEAMID(eFromPlayer), TEAMID(eToPlayer));
			bTeamTradeEnded = true; // advc.133
			// <advc.130p>
			/*  Don't check this after all -- if the other side loses all visible
				territory and then regains some, they may still not really be worth
				trading with. */
			/*if(eCancelPlayer == NO_PLAYER ||
				GET_TEAM(eCancelPlayer).AI_openBordersTrade(
					TEAMID(eCancelPlayer == eToPlayer ? eFromPlayer : eToPlayer)) !=
					DENIAL_NO_GAIN)*/
			if (bAlive)
			{
				addEndTradeMemory(eFromPlayer, eToPlayer, TRADE_OPEN_BORDERS,
						eCancelPlayer != eFromPlayer);
			}
			/* (This class really shouldn't be adding cancellation
				memory as this is an AI thing; but BtS does it that way too.) */
			// </advc.130p>
		}
		break;

	case TRADE_DEFENSIVE_PACT:
		GET_TEAM(eFromPlayer).setDefensivePact(TEAMID(eToPlayer), false);
		if(bTeam)
		{
			endTeamTrade(TRADE_DEFENSIVE_PACT, TEAMID(eFromPlayer), TEAMID(eToPlayer));
			bTeamTradeEnded = true; // advc.133
			if (bAlive)
			{
				addEndTradeMemory(eFromPlayer, eToPlayer, TRADE_DEFENSIVE_PACT,
						eCancelPlayer != eFromPlayer); // advc.130p
			}
		}
		break;

	case TRADE_PEACE_TREATY:
		GET_TEAM(eFromPlayer).setForcePeace(TEAMID(eToPlayer), false);
		break;
	// <advc.034>
	case TRADE_DISENGAGE:
		GET_TEAM(eFromPlayer).setDisengage(TEAMID(eToPlayer), false);
		if(bTeam)
			endTeamTrade(TRADE_DISENGAGE, TEAMID(eFromPlayer), TEAMID(eToPlayer));
		return; // No need to update attitude
	// </advc.034>
	default: FAssert(false);
	} // <advc.036>
	if (!bUpdateAttitude)
		return; // </advc.036>
	// <advc.133> (I think this is needed even w/o change 133 canceling more deals)
	if(!bTeamTradeEnded)
		GET_PLAYER(eFromPlayer).AI_updateAttitude(eToPlayer);
	else GET_TEAM(eFromPlayer).AI_updateAttitude(TEAMID(eToPlayer));
	// </advc.133>
}


void CvDeal::startTeamTrade(TradeableItems eItem, TeamTypes eFromTeam, TeamTypes eToTeam, bool bDual)
{
	for (MemberIter itFromMember(eFromTeam); itFromMember.hasNext(); ++itFromMember)
	{
		for (MemberIter itToMember(eToTeam); itToMember.hasNext(); ++itToMember)
		{
			TradeData item(eItem, 1);
			CLinkList<TradeData> ourList;
			ourList.insertAtEnd(item);
			CLinkList<TradeData> theirList;
			if (bDual)
				theirList.insertAtEnd(item);
			GC.getGame().implementDeal(itFromMember->getID(), itToMember->getID(),
					ourList, theirList);
		}
	}
}

void CvDeal::endTeamTrade(TradeableItems eItem, TeamTypes eFromTeam, TeamTypes eToTeam)
{
	FOR_EACH_DEAL_VAR(pLoopDeal)
	{
		if (pLoopDeal == this)
			continue;

		bool bValid = true;
		if (TEAMID(pLoopDeal->getFirstPlayer()) == eFromTeam &&
			TEAMID(pLoopDeal->getSecondPlayer()) == eToTeam)
		{
			FOR_EACH_TRADE_ITEM(pLoopDeal->getFirstList())
			{
				if (pItem->m_eItemType == eItem)
				{
					bValid = false;
					break;
				}
			}
		}
		if (bValid && TEAMID(pLoopDeal->getFirstPlayer()) == eToTeam &&
				TEAMID(pLoopDeal->getSecondPlayer()) == eFromTeam)
		{
			FOR_EACH_TRADE_ITEM(pLoopDeal->getSecondList())
			{
				if (pItem->m_eItemType == eItem)
				{
					bValid = false;
					break;
				}
			}
		}

		if (!bValid)
			pLoopDeal->kill(false);
	}
}

bool CvDeal::isCancelable(PlayerTypes eByPlayer, CvWString* pszReason) const
{
	if (eByPlayer != NO_PLAYER)
	{
		// <advc.001> Not really a bug, but you'd really expect this function to check this.
		if (!involves(eByPlayer))
			return false; // </advc.001>
		if (isUncancelableVassalDeal(eByPlayer, pszReason))
			return false;
	}
	int iTurns = turnsToCancel(eByPlayer);
	if (pszReason != NULL && iTurns > 0)
		*pszReason = gDLL->getText("TXT_KEY_MISC_DEAL_NO_CANCEL", iTurns);
	return (iTurns <= 0);
}

/*  advc.130f: Based on isCancelable; doesn't check turnsToCancel.
	See declaration in CvDeal.h. */
bool CvDeal::isEverCancelable(PlayerTypes eByPlayer) const
{
	if (!involves(eByPlayer))
		return false;

	return !isUncancelableVassalDeal(eByPlayer);
}

int CvDeal::turnsToCancel(PlayerTypes eByPlayer) const
{	// <advc.034>
	int iLen = GC.getDefineINT(CvGlobals::PEACE_TREATY_LENGTH);
	if(isDisengage())
		iLen = std::min(GC.getDefineINT(CvGlobals::DISENGAGE_LENGTH), iLen);
	return (getInitialGameTurn() + iLen - // </advc.034>
			GC.getGame().getGameTurn());
}

// advc:
bool CvDeal::isAllDual() const
{
	FOR_EACH_TRADE_ITEM(getFirstList())
	{
		if(!CvDeal::isDual(pItem->m_eItemType))
			return false;
	}
	FOR_EACH_TRADE_ITEM(getSecondList())
	{
		if(!CvDeal::isDual(pItem->m_eItemType))
			return false;
	}
	return true;
}


bool CvDeal::isAnnual(TradeableItems eItem)
{
	switch (eItem)
	{
	case TRADE_RESOURCES:
	case TRADE_GOLD_PER_TURN:
	case TRADE_VASSAL:
	case TRADE_SURRENDER:
	case TRADE_OPEN_BORDERS:
	case TRADE_DISENGAGE: // advc.034
	case TRADE_DEFENSIVE_PACT:
	case TRADE_PERMANENT_ALLIANCE:
		return true;
		break;
	}
	return false;
}


bool CvDeal::isDual(TradeableItems eItem, bool bExcludePeace)
{
	switch (eItem)
	{
	case TRADE_OPEN_BORDERS:
	case TRADE_DISENGAGE: // advc.034
	case TRADE_DEFENSIVE_PACT:
	case TRADE_PERMANENT_ALLIANCE:
		return true;
	case TRADE_PEACE_TREATY:
		return (!bExcludePeace);
	}
	return false;
}


bool CvDeal::hasData(TradeableItems eItem)
{
	return (eItem != TRADE_MAPS &&
			eItem != TRADE_VASSAL &&
			eItem != TRADE_SURRENDER &&
			eItem != TRADE_OPEN_BORDERS &&
			eItem != TRADE_DISENGAGE && // advc.034
			eItem != TRADE_DEFENSIVE_PACT &&
			eItem != TRADE_PERMANENT_ALLIANCE &&
			eItem != TRADE_PEACE_TREATY);
}


bool CvDeal::isEndWar(TradeableItems eItem)
{
	if (eItem == getPeaceItem())
		return true;

	if (isVassal(eItem))
		return true;

	return false;
}
