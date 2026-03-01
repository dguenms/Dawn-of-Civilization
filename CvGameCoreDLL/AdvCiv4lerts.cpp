#include "CvGameCoreDLL.h"
#include "AdvCiv4lerts.h"
#include "CvInfo_Terrain.h"
#include "CoreAI.h"
#include "CvDeal.h"
#include "CvCity.h"
#include "RiseFall.h" // advc.706
#include "UWAIAgent.h" // advc.ctr

using std::set;
using std::vector;
using std::inserter;
using std::set_difference;


AdvCiv4lert::AdvCiv4lert(PlayerTypes eOwner) : m_eOwner(eOwner)
{
	m_bSilent = false;
	/*	Set this to true in a derived constructor in order to test or debug a
		particular alert through AI Auto Play */
	m_bDebug = false;
}


void AdvCiv4lert::showMessage(CvWString szMsg, char const* szIcon, int iX, int iY,
	ColorTypes eColor) const
{
	if (m_bSilent)
		return;
	// <advc.127>
	bool bAutoPlayJustEnded = GET_PLAYER(m_eOwner).isAutoPlayJustEnded();
	CvGame& kGame = GC.getGame();
	bool bForce = (m_bDebug && (GET_PLAYER(m_eOwner).isSpectator() ||
			/*	When Auto Play has just ended, we're no longer in spectator mode,
				but the message should still be force-delivered. */
			(bAutoPlayJustEnded && kGame.isDebugMode())));
	if (!bForce && (GET_PLAYER(m_eOwner).isHumanDisabled() || bAutoPlayJustEnded))
		return; // </advc.127>
	// <advc.706>
	if (kGame.isOption(GAMEOPTION_RISE_FALL) && kGame.getRiseFall().isBlockPopups())
		return; // </advc.706>
	bool bArrows = (szIcon != NULL);
	gDLL->UI().addMessage(m_eOwner, false, -1, szMsg, NULL,
			bForce && m_bDebug ? MESSAGE_TYPE_MAJOR_EVENT : MESSAGE_TYPE_INFO, // advc.127
			szIcon, (ColorTypes)eColor, iX, iY, bArrows, bArrows);
}


void AdvCiv4lert::check(bool bSilent)
{
	if (m_eOwner == NO_PLAYER || (!m_bDebug && !GET_PLAYER(m_eOwner).isHuman()))
	{
		/*	Normally no need to check during Auto Play. Wouldn't hurt
			except that the checks aren't super fast. */
		return;
	}
	bool const bWasSilent = m_bSilent;
	if (bSilent)
		m_bSilent = true;
	check();
	m_bSilent = bWasSilent;
}

// <advc.210a>
void WarTradeAlert::check()
{
	CvPlayer const& kOwner = GET_PLAYER(m_eOwner);
	for (TeamAIIter<FREE_MAJOR_CIV,OTHER_KNOWN_TO> itHireling(kOwner.getTeam());
		itHireling.hasNext(); ++itHireling)
	{
		CvTeamAI const& kHireling = *itHireling;
		bool const bHirelingValid = (
				!kHireling.isHuman() &&
				!kHireling.isAtWar(kOwner.getTeam()) &&
				kOwner.canContact(kHireling.getLeaderID(), true));
		vector<TeamTypes> aeWillTradeMsgTeams;
		vector<TeamTypes> aeNoLongerTradeMsgTeams;
		bool bNowTooManyWars = false; // Only relevant when UWAI is disabled
		for (TeamIter<FREE_MAJOR_CIV,OTHER_KNOWN_TO> itTarget(kOwner.getTeam());
			itTarget.hasNext(); ++itTarget)
		{
			CvTeam const& kTarget = *itTarget;
			bool const bValid = (bHirelingValid &&
					kTarget.getID() != kHireling.getID() &&
					!kHireling.isAtWar(kTarget.getID()) &&
					// Can't suggest war trades otherwise
					kHireling.isOpenBordersTrading());
			DenialTypes eTradeDenial = (bValid ? kHireling.AI_declareWarTrade(
					kTarget.getID(), kOwner.getTeam()) : NO_DENIAL);
			bool bWillNowWar = (bValid && eTradeDenial == NO_DENIAL);
			if (!getUWAI().isEnabled() && bValid && !bNowTooManyWars &&
				eTradeDenial == DENIAL_TOO_MANY_WARS && kHireling.getNumWars() <= 0)
			{
				bNowTooManyWars = true;
			}
			if (bWillNowWar == m_willWar.get(kHireling.getID(), kTarget.getID()))
				continue;
			m_willWar.set(kHireling.getID(), kTarget.getID(), bWillNowWar);
			if (bWillNowWar)
				aeWillTradeMsgTeams.push_back(kTarget.getID());
			// Obviously can't hire anymore after war is declared
			else if (!kHireling.isAtWar(kTarget.getID()))
				aeNoLongerTradeMsgTeams.push_back(kTarget.getID());
		}
		showMessage(kHireling.getID(), aeWillTradeMsgTeams, true);
		if (GC.getDefineBOOL("ALERT_ON_NO_LONGER_WAR_TRADE"))
			showMessage(kHireling.getID(), aeNoLongerTradeMsgTeams, false);
		if (!getUWAI().isEnabled() &&
			bNowTooManyWars != m_tooManyWars.get(kHireling.getID()) &&
			// Willingness to start a war implies not having "too much on their hands"
			(aeWillTradeMsgTeams.empty() || bNowTooManyWars))
		{
			showMessage(kHireling.getID(), bNowTooManyWars);
		}
		m_tooManyWars.set(kHireling.getID(), bNowTooManyWars);
	}
}


void WarTradeAlert::showMessage(TeamTypes eHireling, std::vector<TeamTypes> aeTargets,
	bool bTrade) const
{
	if (aeTargets.empty())
		return;
	CvTeam const& kHireling = GET_TEAM(eHireling);
	CvWString szMsg = gDLL->getText(bTrade ?
			"TXT_KEY_CIV4LERTS_TRADE_WAR" :
			"TXT_KEY_CIV4LERTS_NO_LONGER_TRADE_WAR",
			GET_PLAYER(kHireling.getLeaderID()).getName());
	if (aeTargets.size() > 1)
		szMsg += L":";
	szMsg += L" ";
	for (size_t i = 0; i < aeTargets.size(); i++)
	{
		szMsg += GET_TEAM(aeTargets[i]).getName();
		if (i != aeTargets.size() - 1)
			szMsg += L", ";
		else szMsg += L".";
	}
	showMessage(szMsg, eHireling);
}


void WarTradeAlert::showMessage(TeamTypes eHireling, bool bNowTooManyWars) const
{
	CvWString szMsg = gDLL->getText(bNowTooManyWars ?
			"TXT_KEY_CIV4LERTS_TOO_MANY_WARS" :
			"TXT_KEY_CIV4LERTS_NO_LONGER_TOO_MANY_WARS",
			GET_TEAM(eHireling).getName().GetCString());
	showMessage(szMsg, eHireling);
}


void WarTradeAlert::showMessage(CvWString szMsg, TeamTypes eHireling) const
{
	AdvCiv4lert::showMessage(szMsg, NULL,
			// <advc.127b>
			GET_TEAM(eHireling).getCapitalX(TEAMID(m_eOwner)),
			GET_TEAM(eHireling).getCapitalY(TEAMID(m_eOwner)), // </advc.127b>
			GC.getColorType("WAR_TRADE_ALERT"));
} // </advc.210a>

// <advc.210b>
RevoltAlert::RevoltAlert(PlayerTypes eOwner) : AdvCiv4lert(eOwner) {}


void RevoltAlert::check()
{
	set<PlotNumTypes> updatedRevolt;
	set<PlotNumTypes> updatedOccupation;
	CvPlayer const& kOwner = GET_PLAYER(m_eOwner);
	FOR_EACH_CITY(pCity, kOwner)
	{
		bool const bCouldPreviouslyRevolt = (m_revoltPossible.
				count(pCity->plotNum()) > 0);
		bool const bWasOccupation = (m_occupation.
				count(pCity->plotNum()) > 0);
		scaled rRevoltProb = pCity->revoltProbability();
		if (rRevoltProb > 0)
		{
			updatedRevolt.insert(pCity->plotNum());
			/*	Report only change in revolt chance OR change in occupation status;
				the latter takes precedence. */
			if (!bCouldPreviouslyRevolt && bWasOccupation == pCity->isOccupation())
			{
				wchar szTempBuffer[1024];
				swprintf(szTempBuffer, L"%.1f", 100 * rRevoltProb.getFloat());
				showMessage(gDLL->getText("TXT_KEY_CIV4LERTS_REVOLT",
						pCity->getName().c_str(), szTempBuffer),
						//ARTFILEMGR.getInterfaceArtInfo("INTERFACE_RESISTANCE")->getPath(),
						NULL, // Icon works - but is too distracting
						pCity->getX(), pCity->getY());
						// (red text also too distracting)
						//GC.getColorType("WARNING_TEXT")
			}
		}
		#if 0 // Disabled: Message when revolt chance becomes 0
		else if (bCouldPreviouslyRevolt && bWasOccupation == pCity->isOccupation() &&
			/*	Don't report 0 revolt chance when in occupation b/c
				revolt chance will increase a bit when occupation ends. */
			!pCity->isOccupation())
		{
			showMessage(gDLL->getText("TXT_KEY_CIV4LERTS_NO_LONGER_REVOLT",
					pCity->getName().c_str(),
					//ARTFILEMGR.getInterfaceArtInfo("INTERFACE_RESISTANCE")->getPath(),
					NULL, pCity->getX(), pCity->getY());
		}
		#endif
		if (pCity->isOccupation())
			updatedOccupation.insert(pCity->plotNum());
		/*	If there's no order queued, the city will come to the player's attention
			anyway when it asks for orders. */
		else if (bWasOccupation && pCity->getNumOrdersQueued() > 0)
		{
			showMessage(gDLL->getText("TXT_KEY_CIV4LERTS_CITY_PACIFIED_ADVC",
					pCity->getName().c_str(),
					//ARTFILEMGR.getInterfaceArtInfo("INTERFACE_RESISTANCE")->getPath(),
					NULL, pCity->getX(), pCity->getY()));
			/*	Pretend that revolt chance is 0 after occupation ends, so that
				a spearate alert is fired on the next turn if it's actually not 0. */
			updatedRevolt.erase(pCity->plotNum());
		}
	}
	m_revoltPossible.clear();
	m_revoltPossible.insert(updatedRevolt.begin(), updatedRevolt.end());
	m_occupation.clear();
	m_occupation.insert(updatedOccupation.begin(), updatedOccupation.end());
} // </advc.210b>

// <advc.210d>
BonusThirdPartiesAlert::BonusThirdPartiesAlert(PlayerTypes eOwner) : AdvCiv4lert(eOwner)
{
	m_bDebug = false;
}


void BonusThirdPartiesAlert::check()
{
	std::multiset<int> updatedDeals[MAX_CIV_PLAYERS];
	FOR_EACH_DEAL(pDeal)
	{
		// This alert ignores trades of the alert owner
		if (pDeal->getFirstPlayer() == m_eOwner || pDeal->getSecondPlayer() == m_eOwner)
			continue;
		vector<int> aiDealData;
		getExportData(pDeal->getFirstList(), pDeal->getSecondPlayer(), aiDealData);
		for(size_t i = 0; i < aiDealData.size(); i++)
			updatedDeals[pDeal->getFirstPlayer()].insert(aiDealData[i]);
		aiDealData.clear();
		getExportData(pDeal->getSecondList(), pDeal->getFirstPlayer(), aiDealData);
		for(size_t i = 0; i < aiDealData.size(); i++)
			updatedDeals[pDeal->getSecondPlayer()].insert(aiDealData[i]);
	}
	for (PlayerIter<MAJOR_CIV> itFrom; itFrom.hasNext(); ++itFrom)
	{
		PlayerTypes const eFrom = itFrom->getID();
		if (eFrom == m_eOwner)
			continue;
		vector<int> aiNewDeals;
		set_difference(updatedDeals[eFrom].begin(), updatedDeals[eFrom].end(),
				m_exportDeals[eFrom].begin(), m_exportDeals[eFrom].end(),
				inserter(aiNewDeals, aiNewDeals.begin()));
		vector<int> aiMissingDeals;
		set_difference(m_exportDeals[eFrom].begin(), m_exportDeals[eFrom].end(),
				updatedDeals[eFrom].begin(), updatedDeals[eFrom].end(),
				inserter(aiMissingDeals, aiMissingDeals.begin()));
		for (size_t i = 0; i < aiNewDeals.size(); i++)
		{
			int iNewCount = updatedDeals[eFrom].count(aiNewDeals[i]);
			int iOldCount = m_exportDeals[eFrom].count(aiNewDeals[i]);
			FAssert(iNewCount > iOldCount);
			showMessage(eFrom, aiNewDeals[i], iNewCount, iOldCount);
		}
		for (size_t i = 0; i < aiMissingDeals.size(); i++)
		{
			int iNewCount = updatedDeals[eFrom].count(aiMissingDeals[i]);
			int iOldCount = m_exportDeals[eFrom].count(aiMissingDeals[i]);
			FAssert(iNewCount < iOldCount);
			showMessage(eFrom, aiMissingDeals[i], iNewCount, iOldCount);
		}
		m_exportDeals[eFrom] = updatedDeals[eFrom];
	}
}


void BonusThirdPartiesAlert::getExportData(CLinkList<TradeData> const& kList,
	PlayerTypes eTo, std::vector<int>& kResult) const
{
	FOR_EACH_TRADE_ITEM(kList)
	{
		if (pItem->m_eItemType == TRADE_RESOURCES)
			kResult.push_back(GC.getNumBonusInfos() * eTo + pItem->m_iData);
	}
}


void BonusThirdPartiesAlert::showMessage(PlayerTypes eFrom, int iData,
	int iNewQuantity, int iOldQuantity)
{
	BonusTypes const eBonus = (BonusTypes)(iData % GC.getNumBonusInfos());
	PlayerTypes const eTo = (PlayerTypes)((iData - eBonus) / GC.getNumBonusInfos());
	CvPlayerAI const& kFrom = GET_PLAYER(eFrom);
	CvPlayerAI const& kTo = GET_PLAYER(eTo);
	// Don't report ended trade when the reason is obvious
	if (!kFrom.isAlive() || !kTo.isAlive() ||
		GET_TEAM(kFrom.getTeam()).isAtWar(kTo.getTeam()) ||
		kFrom.AI_getMemoryCount(eTo, MEMORY_STOPPED_TRADING_RECENT) > 0 ||
		kTo.AI_getMemoryCount(eFrom, MEMORY_STOPPED_TRADING_RECENT) > 0)
	{
		return;
	}
	// Don't report unseen trades
	if (!GET_PLAYER(m_eOwner).isSpectator() && // advc.127
		(!GET_TEAM(m_eOwner).isHasMet(kFrom.getTeam()) ||
		!GET_TEAM(m_eOwner).isHasMet(kTo.getTeam())))
	{
		return;
	}
	int const iBonusChar = GC.getInfo(eBonus).getChar();
	CvWString szMsg;
	CvWString szQuantity;
	if (!m_bDebug || iNewQuantity == 0 || iOldQuantity == 0)
		szQuantity = gDLL->getText("TXT_KEY_CIV4LERTS_BONUS_ICON", iBonusChar);
	else
	{
		szQuantity = (iNewQuantity > iOldQuantity ?
				/*	The difference should practically always be 1; if it's more,
					it's still not incorrect to claim that one more resource is
					being traded. */
				gDLL->getText("TXT_KEY_CIV4LERTS_ONE_MORE", iBonusChar) :
				gDLL->getText("TXT_KEY_CIV4LERTS_ONE_FEWER", iBonusChar));
	}
	if (m_bDebug)
	{
		szMsg = (iNewQuantity > 0 ?
				gDLL->getText("TXT_KEY_CIV4LERTS_NOW_EXPORTING",
				kFrom.getNameKey(), szQuantity.c_str(), kTo.getNameKey()) :
				gDLL->getText("TXT_KEY_CIV4LERTS_NO_LONGER_EXPORTING",
				kFrom.getNameKey(), szQuantity.c_str(), kTo.getNameKey()));
	}
	else
	{
		if ((iNewQuantity > 0) == (iOldQuantity > 0))
			return;
		CvBonusInfo const& kBonus = GC.getInfo(eBonus);
		bool bStrategic = (kBonus.getHappiness() + kBonus.getHealth() <= 0);
		if (!bStrategic)
		{
			CvCivilization const& kCiv = kTo.getCivilization();
			// Don't bother with buildings (only need to cover Ivory)
			for (int i = 0; i < kCiv.getNumUnits(); i++)
			{
				UnitTypes const eUnit = kCiv.unitAt(i);
				CvUnitInfo const& kUnit = GC.getInfo(eUnit);
				if (kUnit.getPrereqAndBonus() == eBonus)
				{
					// Only report Ivory while it's relevant
					TechTypes eTech = kUnit.getPrereqAndTech();
					if (eTech != NO_TECH &&
						kTo.getCurrentEra() - GC.getInfo(eTech).getEra() < 2)
					{
						bStrategic = true;
						break;
					}
				}
			}
		}
		if (bStrategic)
		{
			szMsg = gDLL->getText(iNewQuantity > 0 ?
					"TXT_KEY_CIV4LERTS_EXPORTING_STRATEGIC" :
					"TXT_KEY_CIV4LERTS_NOT_EXPORTING_STRATEGIC",
					kFrom.getNameKey(), kTo.getNameKey(), szQuantity.c_str());
		}
		else
		{
			int iImports = kTo.getNumTradeBonusImports(eFrom);
			FAssert(iImports >= iNewQuantity);
			if (iNewQuantity < iImports)
				return;
			szMsg = gDLL->getText((iNewQuantity > 0 ?
					"TXT_KEY_CIV4LERTS_EXPORTING_ANY" :
					"TXT_KEY_CIV4LERTS_EXPORTING_NONE"),
					kFrom.getNameKey(), kTo.getNameKey(), szQuantity.c_str());
		}
	}
	AdvCiv4lert::showMessage(szMsg);
} // </advc.210d>

// <advc.ctr>
CityTradeAlert::CityTradeAlert(PlayerTypes eOwner) : AdvCiv4lert(eOwner) {}


void CityTradeAlert::check()
{
	PROFILE_FUNC();
	CvPlayer const& kAlertPlayer = GET_PLAYER(m_eOwner);
	for (PlayerAIIter<MAJOR_CIV,OTHER_KNOWN_TO> itPlayer(kAlertPlayer.getTeam());
		itPlayer.hasNext(); ++itPlayer)
	{
		CvPlayerAI const& kPlayer = *itPlayer;
		vector<int> willCedeNow;
		vector<int> willBuyNow;
		vector<int> canLiberateNow;
		vector<CvCity const*> diffCede;
		vector<CvCity const*> diffBuy;
		vector<CvCity const*> diffLiberate;
		if (kAlertPlayer.canContact(kPlayer.getID(), true))
		{
			bool const bWar = ::atWar(kAlertPlayer.getTeam(), kPlayer.getTeam());
			/*	Don't report "will cede" when war enemy unwilling to pay for peace
				(especially not cities that kPlayer has just conquered from kAlertPlayer) */
			if (!bWar || !getUWAI().isEnabled() || GET_TEAM(kPlayer.getTeam()).
				uwai().endWarVal(kAlertPlayer.getTeam()) > 0)
			{
				vector<int>& kWasWilling = m_willCede[kPlayer.getID()];
				FOR_EACH_CITY(pCity, kPlayer)
				{
					int const iCity = pCity->getID();
					TradeData item(TRADE_CITIES, iCity);
					if (kPlayer.canTradeItem(kAlertPlayer.getID(), item, true))
					{
						// When at war, check if they'd actually cede the city for peace.
						if (bWar)
						{
							CLinkList<TradeData> alertPlayerGives;
							CLinkList<TradeData> alertPlayerReceives;
							TradeData peaceTreaty(TRADE_PEACE_TREATY);
							alertPlayerGives.insertAtEnd(peaceTreaty);
							alertPlayerReceives.insertAtEnd(peaceTreaty);
							alertPlayerReceives.insertAtEnd(item);
							if (!kPlayer.AI_considerHypotheticalOffer(
								kAlertPlayer.getID(),
								alertPlayerGives, alertPlayerReceives, 1))
							{
								continue;
							}
						}
						willCedeNow.push_back(iCity);
						if (std::find(kWasWilling.begin(), kWasWilling.end(), iCity) ==
							kWasWilling.end())
						{
							diffCede.push_back(pCity);
						}
					}
				}
			}
			if (!bWar)
			{
				FOR_EACH_CITY(pCity, kAlertPlayer)
				{
					int const iCity = pCity->getID();
					if (kAlertPlayer.canTradeItem(kPlayer.getID(), TradeData(
						TRADE_CITIES, iCity), true))
					{
						bool const bLiberate = (pCity->getLiberationPlayer() ==
								kPlayer.getID());
						if (bLiberate)
							canLiberateNow.push_back(iCity);
						else willBuyNow.push_back(iCity);
						if( // Don't report cities right after acquisition
							//GC.getGame().getGameTurn() - pCity->getGameTurnAcquired() > 1 &&
							// Don't report possible liberation right after making peace
							/*(!bLiberate || GET_TEAM(kPlayer.getTeam()).
							getTurnsAtPeace(kAlertPlayer.getTeam()) > 1)*/
							//^Try a different tack.
							(!bLiberate || pCity->getPreviousOwner() != kPlayer.getID()))
						{
							vector<int>& kWas = (bLiberate ? m_canLiberate[kPlayer.getID()] :
									m_willBuy[kPlayer.getID()]);
							if (std::find(kWas.begin(), kWas.end(), iCity) == kWas.end())
								(bLiberate ? diffLiberate : diffBuy).push_back(pCity);
						}
					}
				}
			}
			m_willCede[kPlayer.getID()].clear();
			m_willBuy[kPlayer.getID()].clear();
			m_canLiberate[kPlayer.getID()].clear();
			m_willCede[kPlayer.getID()].insert(m_willCede[kPlayer.getID()].begin(),
					willCedeNow.begin(), willCedeNow.end());
			m_willBuy[kPlayer.getID()].insert(m_willBuy[kPlayer.getID()].begin(),
					willBuyNow.begin(), willBuyNow.end());
			m_canLiberate[kPlayer.getID()].insert(m_canLiberate[kPlayer.getID()].begin(),
					canLiberateNow.begin(), canLiberateNow.end());
		}
		msgWilling(diffCede, kPlayer.getID(), true);
		msgWilling(diffBuy, kPlayer.getID(), false);
		msgLiberate(diffLiberate, kPlayer.getID());
	}
}


void CityTradeAlert::msgWilling(std::vector<CvCity const*> const& kCities,
	PlayerTypes ePlayer, bool bCede) const
{
	if (kCities.empty())
		return;

	CvWString szMsg(GET_PLAYER(ePlayer).getName());
	szMsg.append(L" ");
	szMsg.append(gDLL->getText(bCede ? "TXT_KEY_WILLING_TO_CEDE" : "TXT_KEY_WILLING_TO_TRADE_FOR"));
	for (size_t i = 0; i < kCities.size(); i++)
	{
		if (i > 0)
			szMsg.append(L",");
		szMsg.append(L" ");
		szMsg.append(kCities[i]->getName());
	}
	showMessage(szMsg, NULL,
			kCities.size() == 1 ? kCities[0]->getX() : - 1,
			kCities.size() == 1 ? kCities[0]->getY() : - 1,
			GC.getColorType("CITY_BLUE"));
}


void CityTradeAlert::msgLiberate(std::vector<CvCity const*> const& kCities,
	PlayerTypes ePlayer) const
{
	if (kCities.empty())
		return;

	CvWString szMsg;
	for (size_t i = 0; i < kCities.size(); i++)
	{
		szMsg.append(kCities[i]->getName());
		if(i < kCities.size() - 1)
			szMsg.append(L",");
		szMsg.append(L" ");
	}
	CvWString szName(GET_PLAYER(ePlayer).getName());
	szMsg.append(gDLL->getText("TXT_KEY_CAN_LIBERATE", szName.c_str()));
	showMessage(szMsg, NULL,
			kCities.size() == 1 ? kCities[0]->getX() : - 1,
			kCities.size() == 1 ? kCities[0]->getY() : - 1,
			GC.getColorType("CITY_BLUE"));
}
// </advc.ctr>
