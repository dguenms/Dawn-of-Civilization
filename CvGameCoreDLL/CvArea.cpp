// area.cpp

#include "CvGameCoreDLL.h"
#include "CvArea.h"
#include "CvMap.h"
#include "CvGamePlay.h"
#include "CvCity.h"
#include "CvUnit.h"
#include "CvPlayerAI.h"
#include "CvInfo_Terrain.h"


CvArea::CvArea()
{
	m_aTargetCities = new IDInfo[MAX_PLAYERS];
	// advc: Default id was 0; invalid seems safer.
	reset(FFreeList::INVALID_INDEX, false, true);
}


CvArea::~CvArea()
{
	uninit();
	SAFE_DELETE_ARRAY(m_aTargetCities);
}


void CvArea::init(bool bWater) // advc: iID param removed; always gets set beforehand.
{
	reset(getID(), bWater);
}


void CvArea::uninit() { /* (advc.enum: No memory to free here currently) */ }

// Initializes data members that are serialized.
void CvArea::reset(int iID, bool bWater, bool bConstructorCall)
{
	uninit();

	m_iID = iID;
	m_iNumTiles = 0;
	m_iNumOwnedTiles = 0;
	m_iNumRiverEdges = 0;
	m_iNumUnits = 0;
	m_iNumCities = 0;
	m_iTotalPopulation = 0;
	m_iNumStartingPlots = 0;
	m_iBarbarianCitiesEver = 0; // advc.300
	// <advc.030>
	m_bLake = false;
	m_iRepresentativeArea = iID;
	// </advc.030>
	m_bWater = bWater;

	m_aiUnitsPerPlayer.reset();
	m_aiCitiesPerPlayer.reset();
	m_aiPopulationPerPlayer.reset();
	m_aiBuildingGoodHealth.reset();
	m_aiBuildingBadHealth.reset();
	m_aiBuildingHappiness.reset();
	m_aiTradeRoutes.reset(); // advc.310
	m_aiFreeSpecialist.reset();
	m_aiPower.reset();
	m_aiBestFoundValue.reset();
	m_aiNumRevealedTiles.reset();
	m_aiCleanPowerCount.reset();
	m_aiBorderObstacleCount.reset();
	m_aiBonuses.reset();
	//m_aiImprovements.reset(); // advc.opt
	m_aeAreaAIType.reset();

	FOR_EACH_ENUM(Player)
		m_aTargetCities[eLoopPlayer].reset();

	m_aaiYieldRateModifier.reset();
	m_aaiNumTrainAIUnits.reset();
	m_aaiNumAIUnits.reset();
}


void CvArea::setID(int iID)
{
	m_iID = iID;
	m_iRepresentativeArea = iID; // advc.030
}


int CvArea::calculateTotalBestNatureYield() const
{
	int iCount = 0;
	CvMap const& kMap = GC.getMap();
	for (int i = 0; i < kMap.numPlots(); i++)
	{
		CvPlot const& kPlot = kMap.getPlotByIndex(i);
		if (kPlot.isArea(*this))
			iCount += kPlot.calculateTotalBestNatureYield(NO_TEAM);
	}
	return iCount;
}


int CvArea::countCoastalLand() const
{
	if (isWater())
		return 0;

	int iCount = 0;
	CvMap const& kMap = GC.getMap();
	for (int iI = 0; iI < kMap.numPlots(); iI++)
	{
		CvPlot const& kPlot = kMap.getPlotByIndex(iI);
		if (kPlot.isArea(*this))
		{
			if (kPlot.isCoastalLand())
				iCount++;
		}
	}
	return iCount;
}


int CvArea::countNumUniqueBonusTypes() const
{
	int iCount = 0;
	for (int iI = 0; iI < GC.getNumBonusInfos(); iI++)
	{
		if (getNumBonuses((BonusTypes)iI) > 0)
		{
			if (GC.getInfo((BonusTypes)iI).isOneArea())
				iCount++;
		}
	}
	return iCount;
}


int CvArea::countHasReligion(ReligionTypes eReligion, PlayerTypes eOwner) const
{
	int iCount = 0;
	// <advc.opt> Don't go through all players if eOwner is given
	if (eOwner == NO_PLAYER)
	{
		for (PlayerIter<ALIVE> itOwner; itOwner.hasNext(); ++itOwner)
		{	// Recursive call with eOwner!=NO_PLAYER
			iCount += countHasReligion(eReligion, itOwner->getID());
		}
		return iCount;
	} // </advc.opt>
	FOR_EACH_CITY(pLoopCity, GET_PLAYER(eOwner))
	{
		if (pLoopCity->isArea(*this))
		{
			if (pLoopCity->isHasReligion(eReligion))
				iCount++;
		}
	}
	return iCount;
}

// TODO: refactor
int CvArea::countCanSpread(ReligionTypes eReligion, PlayerTypes eOwner, bool bMissionary) const
{
	CvCity* pLoopCity;
	int iCount;
	int iLoop;
	int iI;

	iCount = 0;

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			if ((eOwner == NO_PLAYER) || (iI == eOwner))
			{
				for (pLoopCity = GET_PLAYER((PlayerTypes)iI).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER((PlayerTypes)iI).nextCity(&iLoop))
				{
					if (pLoopCity->area()->getID() == getID())
					{
						if (pLoopCity->canSpread(eReligion, bMissionary))
						{
							iCount++;
						}
					}
				}
			}
		}
	}

	return iCount;
}

int CvArea::countHasCorporation(CorporationTypes eCorporation, PlayerTypes eOwner) const
{
	int iCount = 0;
	// <advc.opt> Don't go through all players if eOwner is given
	if (eOwner == NO_PLAYER)
	{
		for (PlayerIter<ALIVE> itOwner; itOwner.hasNext(); ++itOwner)
		{	// Recursive call with eOwner!=NO_PLAYER
			iCount += countHasCorporation(eCorporation, itOwner->getID());
		}
		return iCount;
	} // </advc.opt>

	FOR_EACH_CITY(pLoopCity, GET_PLAYER(eOwner))
	{
		if (pLoopCity->isArea(*this))
		{
			if (pLoopCity->isHasCorporation(eCorporation))
				iCount++;
		}
	}
	return iCount;
}

// <advc.030>
void CvArea::updateLake(bool bCheckRepr)
{
	PROFILE_FUNC();
	m_bLake = false;
	if(!isWater())
		return;
	int iTotalTiles = getNumTiles();
	if(iTotalTiles > GC.getDefineINT(CvGlobals::LAKE_MAX_AREA_SIZE))
		return;
	if(!bCheckRepr)
	{
		m_bLake = true;
		return;
	}
	FOR_EACH_AREA(pOther)
	{
		if(pOther->m_iRepresentativeArea == m_iRepresentativeArea &&
			pOther->getID() != getID())
		{
			iTotalTiles += pOther->getNumTiles();
			if(iTotalTiles > GC.getDefineINT(CvGlobals::LAKE_MAX_AREA_SIZE))
				return;
		}
	}
	m_bLake = true;
}

void CvArea::setRepresentativeArea(int iArea)
{
	m_iRepresentativeArea = iArea;
}

/*  Replacement for the BtS area()==area() checks. Mostly used for
	performance reasons before costlier more specific checks. */
bool CvArea::canBeEntered(CvArea const& kFrom, CvUnit const* u) const
{
	// Called very often. Mostly from the various plot danger functions.
	//PROFILE_FUNC();
	if(getID() == kFrom.getID())
		return true;
	/*  If I wanted to support canMoveAllTerrain here, then I couldn't do
		anything more when u==NULL. So that's not supported. */
	if(isWater() == kFrom.isWater() &&
		(m_iRepresentativeArea != kFrom.m_iRepresentativeArea ||
		(u != NULL && !u->canMoveImpassable())))
	{
		return false;
	}
	/*  Can't rule out movement between water and land without knowing if the
		unit is a ship inside a city or a land unit aboard a transport */
	if(u == NULL)
		return true;
	if(isWater() && (u->getDomainType() != DOMAIN_SEA || !u->getPlot().isCity()))
		return false;
	if(!isWater() && (u->getDomainType() != DOMAIN_LAND || !u->isCargo()))
		return false;
	/*  In the cases above, movement may actually still be possible if it's
		a sea unit entering a city or a land unit boarding a transport.
		So this function really assumes that u enters a hostile plot. */
	return true;
} // </advc.030>

void CvArea::changeNumTiles(int iChange)
{
	if(iChange == 0)
		return;

	bool bOldLake = isLake();

	m_iNumTiles = (m_iNumTiles + iChange);
	FAssert(getNumTiles() >= 0);

	if (bOldLake != isLake())
	{
		GC.getMap().updateIrrigated();
		GC.getMap().updateYield();
	}
}


void CvArea::changeNumOwnedTiles(int iChange)
{
	m_iNumOwnedTiles = (m_iNumOwnedTiles + iChange);
	FAssert(getNumOwnedTiles() >= 0);
	FAssert(getNumUnownedTiles() >= 0);
}

// <advc.300>
std::pair<int,int> CvArea::countOwnedUnownedHabitableTiles(bool bIgnoreBarb) const
{
	std::pair<int,int> r(0, 0);
	CvMap const& kMap = GC.getMap();
	for(int i = 0; i < kMap.numPlots(); i++)
	{
		CvPlot const& kPlot = kMap.getPlotByIndex(i);
		if(!kPlot.isArea(*this) || !kPlot.isHabitable())
			continue;
		if(kPlot.isOwned() && (!bIgnoreBarb || kPlot.getOwner() != BARBARIAN_PLAYER))
			r.first++;
		else r.second++;
	}
	return r;
}


bool CvArea::hasAnyAreaPlayerBonus(BonusTypes eBonus) const
{
	for (PlayerIter<ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		// Barbarian, minor civ, anything goes so long as there's a city.
		if (getCitiesPerPlayer(itPlayer->getID()) > 0 && itPlayer->hasBonus(eBonus))
			return true;
	}
	return false;
}


int CvArea::getBarbarianCitiesEverCreated() const
{
	return m_iBarbarianCitiesEver;
}


void CvArea::reportBarbarianCityCreated()
{
	m_iBarbarianCitiesEver++;
} // </advc.300>


void CvArea::changeNumRiverEdges(int iChange)
{
	m_iNumRiverEdges = (m_iNumRiverEdges + iChange);
	FAssert(getNumRiverEdges() >= 0);
}


void CvArea::changeNumStartingPlots(int iChange)
{
	m_iNumStartingPlots = m_iNumStartingPlots + iChange;
	FAssert(getNumStartingPlots() >= 0);
}


void CvArea::changeUnitsPerPlayer(PlayerTypes eIndex, int iChange)
{
	m_aiUnitsPerPlayer.add(eIndex, iChange);
	// advc (can be temporarily negative while recalculating areas)
	FAssert(getUnitsPerPlayer(eIndex) >= 0 || gDLL->GetWorldBuilderMode());
	m_iNumUnits += iChange;
	FAssert(getNumUnits() >= 0);
}


int CvArea::getCitiesPerPlayer(PlayerTypes eIndex, /* <advc.030b> */ bool bCheckAdjacentCoast) const
{
	/*  Perhaps this parameter isn't really needed, but this function gets called
		from so many places that I can't check if one of them might have a problem
		with water areas having a positive city count. */
	if(!bCheckAdjacentCoast && isWater())
		return 0; // </advc.030b>
	return m_aiCitiesPerPlayer.get(eIndex);
}


void CvArea::changeCitiesPerPlayer(PlayerTypes eIndex, int iChange)
{
	m_aiCitiesPerPlayer.add(eIndex, iChange);
	FAssert(getCitiesPerPlayer(eIndex, true) >= 0 || gDLL->GetWorldBuilderMode()); // advc
	m_iNumCities += iChange;
	FAssert(getNumCities() >= 0);
	// <advc.300>
	for (int i = 0; i < iChange; i++)
		reportBarbarianCityCreated(); // </advc.300>
}


void CvArea::changePopulationPerPlayer(PlayerTypes eIndex, int iChange)
{
	m_aiPopulationPerPlayer.add(eIndex, iChange);
	FAssert(getPopulationPerPlayer(eIndex) >= 0 || gDLL->GetWorldBuilderMode()); // advc
	m_iTotalPopulation += iChange;
	FAssert(getTotalPopulation() >= 0);
}


void CvArea::changeBuildingGoodHealth(PlayerTypes eIndex, int iChange)
{
	if (iChange != 0)
	{
		m_aiBuildingGoodHealth.add(eIndex, iChange);
		FAssert(getBuildingGoodHealth(eIndex) >= 0);
		GET_PLAYER(eIndex).AI_makeAssignWorkDirty();
	}
}


void CvArea::changeBuildingBadHealth(PlayerTypes eIndex, int iChange)
{
	if (iChange != 0)
	{
		m_aiBuildingBadHealth.add(eIndex, iChange);
		FAssert(getBuildingBadHealth(eIndex) >= 0);
		GET_PLAYER(eIndex).AI_makeAssignWorkDirty();
	}
}


void CvArea::changeBuildingHappiness(PlayerTypes eIndex, int iChange)
{
	if (iChange != 0)
	{
		m_aiBuildingHappiness.add(eIndex, iChange);
		GET_PLAYER(eIndex).AI_makeAssignWorkDirty();
	}
}

// advc.310:
void CvArea::changeTradeRoutes(PlayerTypes eIndex, int iChange)
{
	if(iChange != 0)
	{
		m_aiTradeRoutes.add(eIndex, iChange);
		FAssert(getTradeRoutes(eIndex) >= 0);
		GET_PLAYER(eIndex).updateTradeRoutes();
	}
}


void CvArea::changeFreeSpecialist(PlayerTypes eIndex, int iChange)
{
	if (iChange != 0)
	{
		m_aiFreeSpecialist.add(eIndex, iChange);
		FAssert(getFreeSpecialist(eIndex) >= 0);
		GET_PLAYER(eIndex).AI_makeAssignWorkDirty();
	}
}


int CvArea::getPower(PlayerTypes eIndex) const
{
    FAssertMsg(eIndex >= 0, "eIndex is expected to be >= 0");
    FAssertMsg(eIndex < MAX_PLAYERS, "eIndex is expected to be < MAX_PLAYERS");

    int iPower = m_aiPower.get(eIndex);

    if (GET_PLAYER(eIndex).isBarbarian())
        iPower /= 2;
    else if (GET_PLAYER(eIndex).isIndependent())
        iPower /= 8;
    else if (GET_PLAYER(eIndex).isMinorCiv())
        iPower /= 4;

    return iPower;
}


void CvArea::changePower(PlayerTypes eIndex, int iChange)
{
	m_aiPower.add(eIndex, iChange);
	/*  <advc.006> Can happen when continuing a game after changing a
		unit power value in XML */
	if(getPower(eIndex) < 0)
	{
		m_aiPower.set(eIndex, 0); // </advc.006>
		FAssertMsg(getPower(eIndex) >= 0, "OK when playing from an old savegame "
				"with an updated version of the mod");
	}
}


void CvArea::setBestFoundValue(PlayerTypes eIndex, int iNewValue)
{
	m_aiBestFoundValue.set(eIndex, iNewValue);
	FAssert(getBestFoundValue(eIndex) >= 0);
}


void CvArea::changeNumRevealedTiles(TeamTypes eIndex, int iChange)
{
	m_aiNumRevealedTiles.add(eIndex, iChange);
	FAssert(getNumRevealedTiles(eIndex) >= 0);
}


void CvArea::changeCleanPowerCount(TeamTypes eIndex, int iChange)
{
	if(iChange == 0)
		return;
	bool bOldCleanPower = isCleanPower(eIndex);
	m_aiCleanPowerCount.add(eIndex, iChange);
	if (bOldCleanPower != isCleanPower(eIndex))
	{
		GET_TEAM(eIndex).updateCommerce();
		GET_TEAM(eIndex).updatePowerHealth();
		if (eIndex == GC.getGame().getActiveTeam())
			gDLL->UI().setDirty(CityInfo_DIRTY_BIT, true);
	}
}


void CvArea::changeBorderObstacleCount(TeamTypes eIndex, int iChange)
{
	m_aiBorderObstacleCount.add(eIndex, iChange);
	if (iChange > 0 && m_aiBorderObstacleCount.get(eIndex) == iChange)
		GC.getMap().verifyUnitValidPlot();
}


void CvArea::setAreaAIType(TeamTypes eIndex, AreaAITypes eNewValue)
{
	m_aeAreaAIType.set(eIndex, eNewValue);
}


CvCityAI* CvArea::AI_getTargetCity(PlayerTypes eIndex) const
{
	FAssertBounds(0, MAX_PLAYERS, eIndex);
	return ::AI_getCity(m_aTargetCities[eIndex]);
}


void CvArea::AI_setTargetCity(PlayerTypes eIndex, CvCity* pNewValue)
{
	FAssertBounds(0, MAX_PLAYERS, eIndex);
	if (pNewValue != NULL)
		m_aTargetCities[eIndex] = pNewValue->getIDInfo();
	else m_aTargetCities[eIndex].reset();
}


void CvArea::changeYieldRateModifier(PlayerTypes eIndex1, YieldTypes eIndex2, int iChange)
{
	if (iChange == 0)
		return;

	m_aaiYieldRateModifier.add(eIndex1, eIndex2, iChange);

	GET_PLAYER(eIndex1).invalidateYieldRankCache(eIndex2);
	if (eIndex2 == YIELD_COMMERCE)
		GET_PLAYER(eIndex1).updateCommerce();
	GET_PLAYER(eIndex1).AI_makeAssignWorkDirty();
	if (GET_PLAYER(eIndex1).getTeam() == GC.getGame().getActiveTeam())
		gDLL->UI().setDirty(CityInfo_DIRTY_BIT, true);
}


void CvArea::changeNumTrainAIUnits(PlayerTypes eIndex1, UnitAITypes eIndex2, int iChange)
{
	m_aaiNumTrainAIUnits.add(eIndex1, eIndex2, iChange);
	FAssert(getNumTrainAIUnits(eIndex1, eIndex2) >= 0);
}


int CvArea::getNumAIUnits(PlayerTypes eIndex1, UnitAITypes eIndex2) const
{
	// <advc.124> NO_UNITAI counts all units of eIndex1
	//FAssertMsg(eIndex2 >= 0, "eIndex2 is expected to be >= 0");
	if (eIndex2 < 0)
	{
		int iR = 0;
		FOR_EACH_ENUM(UnitAI)
			iR += m_aaiNumAIUnits.get(eIndex1, eLoopUnitAI);
		return iR;
	} // </advc.124>
	return m_aaiNumAIUnits.get(eIndex1, eIndex2);
}


void CvArea::changeNumAIUnits(PlayerTypes eIndex1, UnitAITypes eIndex2, int iChange)
{
	m_aaiNumAIUnits.add(eIndex1, eIndex2, iChange);
	FAssert(getNumAIUnits(eIndex1, eIndex2) >= 0);
}


int CvArea::getNumTotalBonuses() const
{
	int iCount = 0;
	FOR_EACH_ENUM(Bonus)
		iCount += m_aiBonuses.get(eLoopBonus);
	return iCount;
}


void CvArea::changeNumBonuses(BonusTypes eBonus, int iChange)
{
	m_aiBonuses.add(eBonus, iChange);
	FAssert(getNumBonuses(eBonus) >= 0);
}

// advc.opt: No longer used
/*int CvArea::getNumImprovements(ImprovementTypes eImprovement) const
{
	return m_aiImprovements.get(eImprovement);
}

void CvArea::changeNumImprovements(ImprovementTypes eImprovement, int iChange)
{
	m_aiImprovements.add(eImprovement, iChange);
	FAssert(getNumImprovements(eImprovement) >= 0);
}*/


CvArea* CvArea::findClosestArea(int iMinSize) const
{
	if (getNumTiles() >= iMinSize)
		return NULL;

	CvPlot* pCurrentPlot;
	CvPlot* pLoopPlot;
	int iCurrentDistance;

	CvArea* pClosestArea = NULL;
	int iClosestDistance = MAX_INT;

	for (int iI = 0; iI < GC.getMap().numPlots(); iI++)
	{
		pCurrentPlot = GC.getMap().plotByIndex(iI);
		if (!pCurrentPlot->isArea(*this))
			continue;

		for (int iJ = 0; iJ < GC.getMap().numPlots(); iJ++)
		{
			pLoopPlot = GC.getMap().plotByIndex(iJ);
			if (!pLoopPlot->isArea(*this))
				continue;
			if (pLoopPlot->isWater())
				continue;
			if (pLoopPlot->getArea().getNumTiles() < iMinSize)
				continue;
			// doc: only use Australia as closest continent for Oceania
			if (pLoopPlot->getRegionID() == REGION_AUSTRALIA && pCurrentPlot->getRegionID() != REGION_OCEANIA)
				continue;

			iCurrentDistance = stepDistance(pCurrentPlot->getX(), pCurrentPlot->getY(), pLoopPlot->getX(), pLoopPlot->getY());
			if (iCurrentDistance < iClosestDistance)
			{
				iClosestDistance = iCurrentDistance;
				pClosestArea = pLoopPlot->area();
			}
		}
	}

	return pClosestArea;
}


// TODO: refactor
int CvArea::getEnemyPower(PlayerTypes ePlayer, bool bIncludeMinors) const
{
	int iPower = 0;

	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		CvPlayer& kPlayer = GET_PLAYER((PlayerTypes)iI);
		if (bIncludeMinors || !kPlayer.isMinorCiv())
		{
			if (GET_TEAM(kPlayer.getTeam()).isAtWar(GET_PLAYER(ePlayer).getTeam()))
			{
				if (getCitiesPerPlayer((PlayerTypes)iI) > 0)
				{
					iPower += kPlayer.getPower();
				}
			}
		}
	}

	return iPower;
}


void CvArea::read(FDataStreamBase* pStream)
{
	reset();

	uint uiFlag=0;
	pStream->Read(&uiFlag);

	pStream->Read(&m_iID);
	pStream->Read(&m_iNumTiles);
	pStream->Read(&m_iNumOwnedTiles);
	pStream->Read(&m_iNumRiverEdges);
	pStream->Read(&m_iNumUnits);
	pStream->Read(&m_iNumCities);
	pStream->Read(&m_iTotalPopulation);
	pStream->Read(&m_iNumStartingPlots);
	pStream->Read(&m_iBarbarianCitiesEver); // advc.300

	pStream->Read(&m_bWater);
	// <advc.030>
	if(uiFlag >= 1)
	{
		pStream->Read(&m_bLake);
		pStream->Read(&m_iRepresentativeArea);
	}
	else
	{
		updateLake(false);
		m_iRepresentativeArea = m_iID;
	} // </advc.030>
	if (uiFlag < 4)
		m_aiUnitsPerPlayer.readArray<int>(pStream);
	else m_aiUnitsPerPlayer.read(pStream);
	// <advc>
	if (uiFlag < 2)
	{
		// Discard AnimalsPerPlayer
		FOR_EACH_ENUM(Player)
		{
			int iTmp;
			pStream->Read(&iTmp);
		}
	} // </advc>
	if (uiFlag < 4)
	{
		m_aiCitiesPerPlayer.readArray<int>(pStream);
		m_aiPopulationPerPlayer.readArray<int>(pStream);
		m_aiBuildingGoodHealth.readArray<int>(pStream);
		m_aiBuildingBadHealth.readArray<int>(pStream);
		m_aiBuildingHappiness.readArray<int>(pStream);
		m_aiTradeRoutes.readArray<int>(pStream); // advc.310
		m_aiFreeSpecialist.readArray<int>(pStream);
		m_aiPower.readArray<int>(pStream);
		m_aiBestFoundValue.readArray<int>(pStream);
		m_aiNumRevealedTiles.readArray<int>(pStream);
		m_aiCleanPowerCount.readArray<int>(pStream);
		m_aiBorderObstacleCount.readArray<int>(pStream);
		m_aeAreaAIType.readArray<int>(pStream);
	}
	else
	{
		m_aiCitiesPerPlayer.read(pStream);
		m_aiPopulationPerPlayer.read(pStream);
		m_aiBuildingGoodHealth.read(pStream);
		m_aiBuildingBadHealth.read(pStream);
		m_aiBuildingHappiness.read(pStream);
		m_aiTradeRoutes.read(pStream); // advc.310
		m_aiFreeSpecialist.read(pStream);
		m_aiPower.read(pStream);
		m_aiBestFoundValue.read(pStream);
		m_aiNumRevealedTiles.read(pStream);
		m_aiCleanPowerCount.read(pStream);
		m_aiBorderObstacleCount.read(pStream);
		m_aeAreaAIType.read(pStream);
	}

	FOR_EACH_ENUM(Player)
	{
		pStream->Read((int*)&m_aTargetCities[eLoopPlayer].eOwner);
		pStream->Read(&m_aTargetCities[eLoopPlayer].iID);
		m_aTargetCities[eLoopPlayer].validateOwner(); // advc.opt
	}

	if (uiFlag < 4)
	{
		ArrayEnumMap2D<PlayerTypes,YieldTypes,short> aaiYieldRateModifier;
		if (uiFlag < 2)
			aaiYieldRateModifier.readArray<int>(pStream);
		else aaiYieldRateModifier.readArray<short>(pStream);
		FOR_EACH_ENUM(Player)
		{
			FOR_EACH_ENUM(Yield)
			{
				m_aaiYieldRateModifier.set(eLoopPlayer, eLoopYield,
						 aaiYieldRateModifier.get(eLoopPlayer, eLoopYield));
			}
		}
		m_aaiNumTrainAIUnits.readArray<int>(pStream);
		m_aaiNumAIUnits.readArray<int>(pStream);
	}
	else
	{
		m_aaiYieldRateModifier.read(pStream);
		m_aaiNumTrainAIUnits.read(pStream);
		m_aaiNumAIUnits.read(pStream);
	}
	if (uiFlag < 4)
		m_aiBonuses.readArray<int>(pStream);
	else m_aiBonuses.read(pStream);
	//m_aiImprovements.Read(pStream);
	// <advc.opt>
	if (uiFlag < 3)
	{
		EagerEnumMap<ImprovementTypes,int> dummy;
		dummy.readArray<int>(pStream);
	} // </advc.opt>
}


void CvArea::write(FDataStreamBase* pStream)
{
	PROFILE_FUNC(); // advc
	REPRO_TEST_BEGIN_WRITE(CvString::format("Area(%d)", getID()));
	uint uiFlag;
	//uiFlag = 1; // advc.030
	//uiFlag = 2; // advc: Remove m_aiAnimalsPerPlayer, advc.enum: write m_aaiYieldRateModifier as short
	//uiFlag = 3; // advc.opt: Remove m_aiImprovements
	uiFlag = 4; // advc.enum: new enum map save behavior
	pStream->Write(uiFlag);

	pStream->Write(m_iID);
	pStream->Write(m_iNumTiles);
	pStream->Write(m_iNumOwnedTiles);
	pStream->Write(m_iNumRiverEdges);
	pStream->Write(m_iNumUnits);
	pStream->Write(m_iNumCities);
	pStream->Write(m_iTotalPopulation);
	pStream->Write(m_iNumStartingPlots);
	pStream->Write(m_iBarbarianCitiesEver); // advc.300

	pStream->Write(m_bWater);
	// <advc.030>
	pStream->Write(m_bLake);
	pStream->Write(m_iRepresentativeArea);
	// </advc.030>
	m_aiUnitsPerPlayer.write(pStream);
	//m_aiAnimalsPerPlayer.write(pStream); // advc: removed
	m_aiCitiesPerPlayer.write(pStream);
	m_aiPopulationPerPlayer.write(pStream);
	m_aiBuildingGoodHealth.write(pStream);
	m_aiBuildingBadHealth.write(pStream);
	m_aiBuildingHappiness.write(pStream);
	m_aiTradeRoutes.write(pStream); // advc.310
	m_aiFreeSpecialist.write(pStream);
	m_aiPower.write(pStream);
	m_aiBestFoundValue.write(pStream);
	m_aiNumRevealedTiles.write(pStream);
	m_aiCleanPowerCount.write(pStream);
	m_aiBorderObstacleCount.write(pStream);
	m_aeAreaAIType.write(pStream);

	FOR_EACH_ENUM(Player)
	{
		pStream->Write(m_aTargetCities[eLoopPlayer].eOwner);
		pStream->Write(m_aTargetCities[eLoopPlayer].iID);
	}

	m_aaiYieldRateModifier.write(pStream);
	m_aaiNumTrainAIUnits.write(pStream);
	m_aaiNumAIUnits.write(pStream);
	m_aiBonuses.write(pStream);
	//m_aiImprovements.Write(pStream); // advc.opt
	REPRO_TEST_END_WRITE();
}
