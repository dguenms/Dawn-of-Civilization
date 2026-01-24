// advc.300: New class; see Shelf.h for description

#include "CvGameCoreDLL.h"
#include "Shelf.h"
#include "CvGame.h"
#include "BarbarianWeightMap.h"
#include "CvMap.h"
#include "CvUnit.h"
#include "CvPlayer.h"


void Shelf::add(CvPlot* pPlot)
{
	m_apPlots.push_back(pPlot);
}


CvPlot* Shelf::randomPlot(RandPlotFlags eRestrictions, int iUnitDistance,
	int* piValidCount, RandPlotWeightMap const* pWeights) const
{
	LOCAL_REF(int, iValid, piValidCount, 0);
	/*	Based on CvMap::syncRandPlot, but shelves are (normally) so small
		that random sampling isn't efficient. Instead, compute the valid
		plots first, then return one of those at random (NULL if none). */
	std::vector<CvPlot*> apValid;
	std::vector<int> aiWeights;
	for (size_t i = 0; i < m_apPlots.size(); i++)
	{
		CvPlot& p = *m_apPlots[i];
		bool const bValid = (
				!(RANDPLOT_LAND & eRestrictions) &&
				(!(RANDPLOT_UNOWNED & eRestrictions) || !p.isOwned()) &&
				(!(RANDPLOT_ADJACENT_UNOWNED & eRestrictions) || !p.isAdjacentOwned()) &&
				(!(RANDPLOT_NOT_VISIBLE_TO_CIV & eRestrictions) || !p.isVisibleToCivTeam()) &&
				// In case that a mod enables sea cities:
				(!(RANDPLOT_NOT_CITY & eRestrictions) || !p.isCity()) &&
				(!p.isCivUnitNearby(iUnitDistance)) &&
				!p.isUnit());
		/*	RANDPLOT_PASSIBLE, RANDPLOT_ADJACENT_LAND, RANDPLOT_HABITABLE:
			Ensured by CvMap::computeShelves. */
		if (bValid)
		{
			apValid.push_back(&p);
			if (pWeights != NULL)
				aiWeights.push_back(pWeights->getProbWeight(p));
		}
	}
	iValid = apValid.size();
	return syncRand().weightedChoice(apValid,
			pWeights == NULL ? NULL : &aiWeights);
}


int Shelf::countUnownedPlots() const
{
	int iR = 0;
	for (size_t i = 0; i < m_apPlots.size(); i++)
	{
		if (!m_apPlots[i]->isOwned())
			iR++;
	}
	return iR;
}


int Shelf::countBarbarians() const
{
	int iR = 0;
	for (size_t i = 0; i < m_apPlots.size(); i++)
	{
		CvPlot const& p = *m_apPlots[i];
		// Take advantage of Barbarians being unable to coexist with visible units
		CLLNode<IDInfo> const* pUnitNode = p.headUnitNode();
		if (pUnitNode == NULL)
			continue;
		CvUnit const* pAnyUnit = CvUnit::fromIDInfo(pUnitNode->m_data);
		if (pAnyUnit != NULL && pAnyUnit->isBarbarian())
			iR += p.plotCount(PUF_isVisible, BARBARIAN_PLAYER);
	}
	return iR;
}


bool Shelf::killBarbarian()
{
	for (size_t i = 0; i < m_apPlots.size(); i++)
	{
		CLLNode<IDInfo>* pUnitNode = m_apPlots[i]->headUnitNode();
		if (pUnitNode == NULL)
			continue;
		CvUnit* pAnyUnit = CvUnit::fromIDInfo(pUnitNode->m_data);
		if (pAnyUnit != NULL && pAnyUnit->isBarbarian() &&
			pAnyUnit->getUnitCombatType() != NO_UNITCOMBAT)
		{
			pAnyUnit->kill(false);
			return true;
		}
	}
	return false;
}

// advc.306:
CvUnit* Shelf::randomBarbarianTransport() const
{
	std::vector<CvUnit*> apValid;
	std::vector<int> aiWeights;
	for (size_t i = 0; i < m_apPlots.size(); i++)
	{
		CvPlot const& p = *m_apPlots[i];
		FOR_EACH_UNIT_VAR_IN(pTransport, p)
		{
			if (!pTransport->isBarbarian())
				break;
			// Load at most 2
			int iCargo = std::min(2, GC.getInfo(pTransport->getUnitType()).getCargoSpace());
			iCargo -= std::max(0, pTransport->getCargo());
			if (iCargo > 0 && !p.isVisibleToCivTeam())
			{
				apValid.push_back(pTransport);
				aiWeights.push_back(GC.getGame().getBarbarianWeightMap().get(p));
			}
		}
	}
	int iTotalWeight = 0;
	for (size_t i = 0; i < aiWeights.size(); i++)
		iTotalWeight += aiWeights[i];
	if (iTotalWeight <= 0)
		return NULL;
	scaled const rBaseProb = fixp(0.22);
	scaled rNoneProb = 1 - (std::min(per100(iTotalWeight) * rBaseProb, rBaseProb) +
			per100(iTotalWeight).pow(fixp(0.6)) / 10);
	if (SyncRandSuccess(rNoneProb))
		return NULL;
	return GC.getGame().getSorenRand().weightedChoice(apValid, &aiWeights);
}
