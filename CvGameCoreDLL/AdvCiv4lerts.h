#pragma once

#ifndef ADVCIV4LERTS_H
#define ADVCIV4LERTS_H

/*	advc.210: I don't want to implement alerts in Python, so I'm having
	Civ4lerts.py call this class. Will need to make changes in Civ4lerts.py,
	Civ4lerts.xml, BugAlertsOptionsTab.py, CvPlayer.cpp and some file for
	game text (like CIV4GameText_advc.xml) to add more alerts. */
class AdvCiv4lert
{
public:
	AdvCiv4lert(PlayerTypes eOwner);
	virtual ~AdvCiv4lert() {}
	// (Silent calls are for initializing data after loading a savegame)
	void check(bool bSilent);

protected:
	virtual void check()=0;
	void showMessage(CvWString szMsg, char const* szIcon = NULL, int iX = -1, int iY = -1,
			ColorTypes eColor = NO_COLOR) const;
	PlayerTypes m_eOwner;
	bool m_bSilent;
	bool m_bDebug;
};

// advc.210a:
class WarTradeAlert : public AdvCiv4lert
{
public:
	WarTradeAlert(PlayerTypes eOwner) : AdvCiv4lert(eOwner) {}
protected:
	void check();
private:
	void showMessage(TeamTypes eHireling, std::vector<TeamTypes> aeTargets,
			bool bTrade) const;
	void showMessage(TeamTypes eHireling, bool bNowTooManyWars) const;
	void showMessage(CvWString szMsg, TeamTypes eHireling) const;
	ArrayEnumMap2D<TeamTypes,TeamTypes,bool> m_willWar;
	ArrayEnumMap<TeamTypes,bool> m_tooManyWars;
};

// advc.210b:
class RevoltAlert : public AdvCiv4lert
{
public:
	RevoltAlert(PlayerTypes eOwner);
protected:
	void check();
private:
	std::set<PlotNumTypes> m_revoltPossible;
	std::set<PlotNumTypes> m_occupation;
};

// advc.210d:
class BonusThirdPartiesAlert : public AdvCiv4lert
{
public:
	BonusThirdPartiesAlert(PlayerTypes eOwner);
protected:
	void check();
private:
	void getExportData(CLinkList<TradeData> const& kList, PlayerTypes eTo,
			std::vector<int>& kResult) const;
	void showMessage(PlayerTypes eFrom, int iData, int iNewQuantity,
			int iOldQuantity);
	std::multiset<int> m_exportDeals[MAX_CIV_PLAYERS];
};

// <advc.ctr>
class CvCity;

class CityTradeAlert : public AdvCiv4lert
{
public:
	CityTradeAlert(PlayerTypes eOwner);
protected:
	void check();
private:
	void msgWilling(std::vector<CvCity const*> const& kCities,
			PlayerTypes ePlayer, bool bCede) const;
	void msgLiberate(std::vector<CvCity const*> const& kCities,
			PlayerTypes ePlayer) const;
	std::vector<int> m_willCede[MAX_CIV_PLAYERS];
	std::vector<int> m_willBuy[MAX_CIV_PLAYERS];
	std::vector<int> m_canLiberate[MAX_CIV_PLAYERS];
}; // </advc.ctr>

#endif
