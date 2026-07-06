#include "CvGameCoreDLL.h"
#include "CvPlotGroup.h"
#include "CvPlayer.h"
#include "CvCity.h"
#include "CvMap.h"
#include "DepthFirstPlotSearch.h" // advc.opt
#include "CvInfo_Terrain.h"

int CvPlotGroup::m_iRecalculating = 0; // advc.064d


CvPlotGroup::CvPlotGroup()
{
	reset(0, NO_PLAYER, true);
}


CvPlotGroup::~CvPlotGroup()
{
	uninit();
}


void CvPlotGroup::init(int iID, PlayerTypes eOwner, CvPlot* pPlot)
{
	reset(iID, eOwner);
	addPlot(pPlot);
}


void CvPlotGroup::uninit()
{
	m_plots.clear();
}

// FUNCTION: reset()
// Initializes data members that are serialized.
void CvPlotGroup::reset(int iID, PlayerTypes eOwner, bool bConstructorCall)
{
	uninit();
	m_iID = iID;
	m_eOwner = eOwner;
	if (!bConstructorCall)
		m_aiNumBonuses.reset();
}


void CvPlotGroup::addPlot(CvPlot* pPlot, /* advc.064d: */ bool bVerifyProduction)
{
	XYCoords xy;
	xy.iX = pPlot->getX();
	xy.iY = pPlot->getY();
	insertAtEndPlots(xy);
	pPlot->setPlotGroup(getOwner(), this, /* advc.064d: */ bVerifyProduction);
}


void CvPlotGroup::removePlot(CvPlot* pPlot, /* advc.064d: */ bool bVerifyProduction)
{
	CLLNode<XYCoords>* pPlotNode = headPlotsNode();
	while (pPlotNode != NULL)
	{
		if (GC.getMap().plotSoren(pPlotNode->m_data.iX, pPlotNode->m_data.iY) == pPlot)
		{
			pPlot->setPlotGroup(getOwner(), NULL, /* advc.064d: */ bVerifyProduction);
			pPlotNode = deletePlotsNode(pPlotNode); // can delete this CvPlotGroup
			break;
		}
		else pPlotNode = nextPlotsNode(pPlotNode);
	}
}

// advc.opt: Replacing CvGlobals::m_plotGroupFinder
class CvPlotGroupSizeCheck : public SingleVisitPlotVisitor<false>
{
protected:
	PlayerTypes m_eOwner;
	TeamTypes m_eTeam;
	int m_iCount;
	int m_iMaxCount;
public:
	CvPlotGroupSizeCheck(CvPlayer const& kOwner, int iMaxCount = MAX_INT)
	{
		reset(kOwner, iMaxCount);
	}
	/*	Will have to reset before use if this ctor is used (owning player is required).
		Intended for reusable instances (reuse saves a little bit of time in the
		base class). */
	CvPlotGroupSizeCheck(CvPlayer const* pOwner = NULL, int iMaxCount = MAX_INT)
	{
		reset(pOwner, iMaxCount);
	}
	void reset(CvPlayer const& kOwner, int iMaxCount = MAX_INT)
	{
		reset(&kOwner, iMaxCount);
	}
	int getCount() const { return m_iCount; }
	bool canVisit(CvPlot const& kFrom, CvPlot const& kPlot) const
	{
		return (kFrom.isSamePlotGroup(kPlot, m_eOwner) &&
				// These need to be consistent with CvPlot::updatePlotGroup
				kPlot.isTradeNetwork(m_eTeam) &&
				kPlot.isTradeNetworkConnected(kFrom, m_eTeam));
	}
	bool visit(CvPlot& kPlot)
	{
		m_iCount++;
		if (m_iCount >= m_iMaxCount)
			return false;
		setVisited(kPlot);
		return true;
	}
private:
	void reset(CvPlayer const* pOwner, int iMaxCount)
	{
		if (pOwner == NULL)
		{
			m_eOwner = NO_PLAYER;
			m_eTeam = NO_TEAM;
		}
		else
		{
			m_eOwner = pOwner->getID();
			m_eTeam = pOwner->getTeam();
		}
		m_iCount = 0;
		m_iMaxCount = iMaxCount;
		SingleVisitPlotVisitor<false>::reset();
	}
};


void CvPlotGroup::recalculatePlots(/* advc.064d: */ bool bVerifyProduction)
{
	PlayerTypes const eOwner = getOwner();
	{
		CLLNode<XYCoords>* pPlotNode = headPlotsNode();
		if (pPlotNode != NULL)
		{
			PROFILE("CvPlotGroup::recalculatePlots PlotGroupFinder");
			int const iOldCount = getLengthPlots();
			CvPlot& kPlot = GC.getMap().getPlot(
					pPlotNode->m_data.iX, pPlotNode->m_data.iY);
			/*int iCount= 0;
			gDLL->getFAStarIFace()->SetData(&GC.getPlotGroupFinder(), &iCount);
			gDLL->getFAStarIFace()->GeneratePath(&GC.getPlotGroupFinder(),
					kPlot.getX(), kPlot.getY(), -1, -1, false, eOwner);*/
			/*	<advc.pf> This upfront check had taken up the bulk of the time.
				Running a simple DFS seems about 4 times faster than using the
				FAStar finder for this purpose. Semantically, it's the same check
				as in BtS: whether all plots in the (old) group are still connected.
				I guess expanding plot groups are handled by CvPlot::updatePlotGroup. */
			// Static to avoid reallocating memory for visited flags
			static CvPlotGroupSizeCheck check;
			check.reset(GET_PLAYER(eOwner), iOldCount + 1);
			DepthFirstPlotSearch<CvPlotGroupSizeCheck> dfs(kPlot, check);
			int iCount = check.getCount();
			FAssert(iCount <= iOldCount); // </advc.pf>
			if (iCount == iOldCount)
				return;
		}
	}
	/*  <advc.064d> To deal with nested recalculatePlots calls. Mustn't
		verifyCityProduction so long as any recalculation is ongoing. */
	m_iRecalculating++;
	/*  Hopefully, it's enough to verify the production of all cities that are
		in the plot group before recalc. Any cities added during recalc get
		removed from some other plot group. However, I'm doing this only for the
		root recalc call, so ... might be inadequate. */
	std::vector<CvCity*> apOldCities; // </advc.064d>
	{
		CLinkList<XYCoords> oldPlotGroup;
		{
			PROFILE("CvPlotGroup::recalculatePlots - update 1");
			XYCoords xy;
			CLLNode<XYCoords>* pPlotNode = headPlotsNode();
			while (pPlotNode != NULL)
			{
				CvPlot& kPlot = GC.getMap().getPlot(
						pPlotNode->m_data.iX, pPlotNode->m_data.iY);
				// <advc.064d>
				CvCity* pPlotCity = kPlot.getPlotCity();
				if (pPlotCity != NULL)
					apOldCities.push_back(pPlotCity);
				// </advc.064d>
				xy.iX = kPlot.getX();
				xy.iY = kPlot.getY();
				oldPlotGroup.insertAtEnd(xy);
				kPlot.setPlotGroup(eOwner, NULL);
				pPlotNode = deletePlotsNode(pPlotNode); // will delete this PlotGroup...
			}
		}
		{
			PROFILE("CvPlotGroup::recalculatePlots - update 2");
			CLLNode<XYCoords>* pPlotNode = oldPlotGroup.head();
			while (pPlotNode != NULL)
			{
				CvPlot& kPlot = GC.getMap().getPlot(
						pPlotNode->m_data.iX, pPlotNode->m_data.iY);
				kPlot.updatePlotGroup(eOwner, true);
				pPlotNode = oldPlotGroup.deleteNode(pPlotNode);
			}
		}
	}
	// <advc.064d>
	m_iRecalculating--;
	FAssert(m_iRecalculating >= 0);
	if (m_iRecalculating == 0 && bVerifyProduction)
	{
		PROFILE("CvPlotGroup::recalculatePlots - verifyProduction");
		for (size_t i = 0; i < apOldCities.size(); i++)
			apOldCities[i]->verifyProduction();
	} // </advc.064d>
}


void CvPlotGroup::changeNumBonuses(BonusTypes eBonus, int iChange)
{
	if (iChange == 0)
		return; // advc

	//iOldNumBonuses = getNumBonuses(eBonus);
	m_aiNumBonuses.add(eBonus, iChange);

	//FAssert(m_aiNumBonuses.get(eBonus) >= 0); // XXX
	/*	K-Mod note, m_aiNumBonuses[eBonus] is often temporarily negative
		while plot groups are being updated.
		It's an unfortunate side effect of the way the update is implemented. ...
		and so this assert is invalid.
		(This isn't my fault. I haven't changed it. It has always been like this.) */
	{
		/*	advc: Worth maintaining a list of the group owner's cities
			(CLinkList<CvCity*> m_ownerCities)? */
		PROFILE("CvPlotGroup::changeNumBonuses - cities");
		CLLNode<XYCoords>* pPlotNode = headPlotsNode();
		while (pPlotNode != NULL)
		{
			CvCity* pCity = GC.getMap().getPlot(
					pPlotNode->m_data.iX, pPlotNode->m_data.iY).getPlotCity();
			if (pCity != NULL)
			{
				if (pCity->getOwner() == getOwner())
					pCity->changeNumBonuses(eBonus, iChange);
			}
			pPlotNode = nextPlotsNode(pPlotNode);
		}

		// doc: Escorial effect
		if (isOwned() && GET_PLAYER(getOwner()).isHasBuildingEffect(ESCORIAL))
		{
			if (eBonus == BONUS_SILVER || eBonus == BONUS_GOLD)
			{
				FOR_EACH_CITY_VAR(pLoopCity, GET_PLAYER(getOwner()))
				{
					if (pLoopCity->isHasRealBuilding(ESCORIAL))
					{
						pLoopCity->changeBuildingCommerceChange(ESCORIAL, COMMERCE_GOLD, 2 * iChange);
						break;
					}
				}
			}
		}

		// doc: Atomium effect
		if (isOwned() && GET_PLAYER(getOwner()).isHasBuildingEffect(ATOMIUM))
		{
			if (eBonus == BONUS_URANIUM || eBonus == BONUS_IRON || eBonus == BONUS_COPPER || eBonus == BONUS_ALUMINUM)
			{
				FOR_EACH_CITY_VAR(pLoopCity, GET_PLAYER(getOwner()))
				{
					pLoopCity->changeBuildingCommerceChange(ATOMIUM, COMMERCE_RESEARCH, (eBonus == BONUS_URANIUM ? 10 : 1) * iChange);
				}
			}
		}

		// doc: Global Seed Vault effect
		if (isOwned() && GET_PLAYER(getOwner()).isHasBuildingEffect(GLOBAL_SEED_VAULT))
		{
			FOR_EACH_CITY_VAR(pLoopCity, GET_PLAYER(getOwner()))
			{
				if (pLoopCity->isHasRealBuilding(GLOBAL_SEED_VAULT))
				{
					FOR_EACH_ENUM(Build)
					{
						CvBuildInfo const& kBuild = GC.getInfo(eLoopBuild);
						if (kBuild.isGraphicalOnly())
							continue;
						if (kBuild.getImprovement() == NO_IMPROVEMENT)
							continue;

						if (kBuild.getTechPrereq() == AGRICULTURE || kBuild.getTechPrereq() == POTTERY || kBuild.getTechPrereq() == CALENDAR)
						{
							CvImprovementInfo const& kImprovement = GC.getInfo(kBuild.getImprovement());
							if (kImprovement.isImprovementBonusMakesValid(eBonus) && !kImprovement.isGraphicalOnly() && !kImprovement.isActsAsCity())
							{
								pLoopCity->changeBuildingCommerceChange(GC.getInfo(GLOBAL_SEED_VAULT).getBuildingClassType(), COMMERCE_RESEARCH, iChange);
								break;
							}
						}
					}
					break;
				}
			}
		}
	}
}

// advc.064d:
void CvPlotGroup::verifyCityProduction()
{
	PROFILE_FUNC();
	if (m_iRecalculating > 0)
		return;
	CvMap const& kMap = GC.getMap();
	for (CLLNode<XYCoords> const* pPlotNode = headPlotsNode(); pPlotNode != NULL;
		pPlotNode = nextPlotsNode(pPlotNode))
	{
		CvCity* pCity = kMap.getPlot(pPlotNode->m_data.iX, pPlotNode->m_data.iY).getPlotCity();
		if (pCity != NULL && pCity->getOwner() == getOwner())
			pCity->verifyProduction();
	}
}


CLLNode<XYCoords>* CvPlotGroup::deletePlotsNode(CLLNode<XYCoords>* pNode)
{
	CLLNode<XYCoords>* pPlotNode;
	pPlotNode = m_plots.deleteNode(pNode);
	if (getLengthPlots() == 0)
		GET_PLAYER(getOwner()).deletePlotGroup(getID());
	return pPlotNode;
}


void CvPlotGroup::read(FDataStreamBase* pStream)
{
	reset();

	uint uiFlag=0;
	pStream->Read(&uiFlag);
	pStream->Read(&m_iID);
	pStream->Read((int*)&m_eOwner);
	if (uiFlag >= 1)
		m_aiNumBonuses.read(pStream);
	else m_aiNumBonuses.readArray<int>(pStream);
	m_plots.Read(pStream);
}


void CvPlotGroup::write(FDataStreamBase* pStream)
{
	uint uiFlag;
	//uiFlag = 0;
	uiFlag = 1; // advc.enum: new enum map save behavior
	pStream->Write(uiFlag);
	pStream->Write(m_iID);
	pStream->Write(m_eOwner);
	m_aiNumBonuses.write(pStream);
	m_plots.Write(pStream);
}
