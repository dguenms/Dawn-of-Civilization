#include "CvGameCoreDLL.h"
#include "UWAICache.h"
#include "UWAIAgent.h"
#include "UWAIReport.h"
#include "MilitaryBranch.h"
#include "WarEvalParameters.h"
#include "WarEvaluator.h"
#include "CoreAI.h"
#include "TeamPathFinder.h"
#include "CvSelectionGroupAI.h"
#include "CityPlotIterator.h"
#include "CvArea.h"
#include "CvInfo_City.h"
#include "CvInfo_Terrain.h"


UWAICache::UWAICache()
:	m_eOwner(NO_PLAYER), m_iNonNavalUnits(-1),
	m_rGoldPerProduction(-1), m_rTotalAssets(-1),
	m_bOffensiveTrait(false), m_bDefensiveTrait(false), m_bCanScrub(false),
	m_bHaveDeepSeaTransports(false), m_bHaveAnyTransports(false),
	m_bFocusOnPeacefulVictory(false)
{}


UWAICache::~UWAICache()
{
	// Don't call clear; most destructors get called automatically.
	deleteUWAICities();
	deleteMilitaryBranches();
}


void UWAICache::init(PlayerTypes eOwner)
{
	m_eOwner = eOwner;
	clear();
	updateTraits();
	createMilitaryBranches();
}


void UWAICache::uninit() 
{
	// Clearing the EnumMaps will free memory (could benefit performance)
	clear();
}


void UWAICache::createMilitaryBranches()
{
	for (int i = 0; i < NUM_BRANCHES; i++)
	{
		m_militaryPower.push_back(MilitaryBranch::create(
				(MilitaryBranchTypes)i, m_eOwner));
	}
}


void UWAICache::deleteMilitaryBranches()
{
	for (size_t i = 0; i < m_militaryPower.size(); i++)
		SAFE_DELETE(m_militaryPower[i]);
	m_militaryPower.clear();
}


void UWAICache::deleteUWAICities()
{
	for (size_t i = 0; i < m_cityList.size(); i++)
		delete m_cityList[i];
	m_cityList.clear();
}


void UWAICache::clear(bool bBeforeUpdate)
{
	deleteUWAICities();
	m_cityMap.clear();
	/*	Tbd.: Can some of these reset calls be avoided before an update?
		They're going to deallocate memory, which might be slow. */
	m_aiReachableCities.reset();
	m_aiReachableCities.set(m_eOwner, GET_PLAYER(m_eOwner).getNumCities());
	m_aiTargetMissions.reset();
	m_arThreatRating.reset();
	m_aiVassalTechScore.reset();
	m_aiVassalResourceScore.reset();
	m_aiAdjLandPlots.reset();
	m_arRelativeNavyPow.reset();
	m_arWarAnger.reset();

	m_rTotalAssets = 0;
	m_rGoldPerProduction = 0;
	m_bCanScrub = false;
	m_bHaveDeepSeaTransports = false;
	m_bHaveAnyTransports = false;
	m_bFocusOnPeacefulVictory = false;

	m_aiPlotsLostAtWar.reset(); // advc.035
	m_aiWarUtilityIgnoringDistraction.reset();

	if (!bBeforeUpdate)
	{	// These are updated at various times, not by the regular update function.
		m_iNonNavalUnits = 0;
		deleteMilitaryBranches();
		m_aiPastWarScore.reset();
		m_aiBounty.reset();
		m_aeSponsorPerTarget.reset();
		m_abCanBeHiredAgainst.reset();
	}
}


void UWAICache::write(FDataStreamBase* pStream) const
{
	PROFILE_FUNC();
	int iSaveVersion;
	//iSaveVersion = 1;
	//iSaveVersion = 2; // advc.035
	//iSaveVersion = 3; // hireAgainst added
	//iSaveVersion = 4; // granularity of pastWarScore increased
	//iSaveVersion = 5; // focusOnPeacefulVictory added
	//iSaveVersion = 6; // advc.enum: Store as float
	//iSaveVersion = 7; // remove latestTurnReachableBySea
	//iSaveVersion = 8; // advc.fract: Store as scaled (not float)
	iSaveVersion = 9; // advc.enum: new enum map save behavior
	/*	I hadn't thought of a version number in the initial release. Need
		to fold it into ownerId now to avoid breaking compatibility. */
	pStream->Write(m_eOwner + 100 * iSaveVersion);
	pStream->Write(numCities());
	for (int i = 0; i < numCities(); i++)
		m_cityList[i]->write(pStream);
	m_aiReachableCities.write(pStream);
	m_aiTargetMissions.write(pStream);
	m_arThreatRating.write(pStream);
	m_aiVassalTechScore.write(pStream);
	m_aiVassalResourceScore.write(pStream);
	m_aiAdjLandPlots.write(pStream);
	m_arRelativeNavyPow.write(pStream);
	m_arWarAnger.write(pStream);
	m_aiPlotsLostAtWar.write(pStream); // advc.035
	m_aiPastWarScore.write(pStream);
	m_aiBounty.write(pStream);
	m_aeSponsorPerTarget.write(pStream);
	m_aiWarUtilityIgnoringDistraction.write(pStream);
	m_abCanBeHiredAgainst.write(pStream);

	pStream->Write(m_bOffensiveTrait);
	pStream->Write(m_bDefensiveTrait);
	pStream->Write(m_bCanScrub);
	pStream->Write(m_bHaveDeepSeaTransports);
	pStream->Write(m_bHaveAnyTransports);
	pStream->Write(m_bFocusOnPeacefulVictory);
	pStream->Write(m_readyToCapitulateTo.size());
	for(std::set<TeamTypes>::const_iterator it = m_readyToCapitulateTo.begin();
		it != m_readyToCapitulateTo.end(); ++it)
	{
		pStream->Write(*it);
	}
	for(size_t i = 0; i < m_militaryPower.size(); i++)
		m_militaryPower[i]->write(pStream);
	pStream->Write(m_iNonNavalUnits);
	m_rTotalAssets.write(pStream);
	m_rGoldPerProduction.write(pStream);
}


void UWAICache::read(FDataStreamBase* pStream)
{
	int iSaveVersion=-1;
	{
		int iTmp;
		pStream->Read(&iTmp);
		iSaveVersion = iTmp / 100;
		m_eOwner = (PlayerTypes)(iTmp % 100);
	}
	// Important to set owner first b/c clear uses it
	clear();
	{
		int iCities = 0;
		pStream->Read(&iCities);
		for (int i = 0; i < iCities; i++)
		{
			m_cityList.push_back(new City);
			m_cityList[i]->read(pStream);
			m_cityMap.insert(std::make_pair(m_cityList[i]->getID(), m_cityList[i]));
		}
	}
	if (iSaveVersion >= 9)
	{
		m_aiReachableCities.read(pStream);
		m_aiTargetMissions.read(pStream);
	}
	else
	{
		m_aiReachableCities.readArray<int>(pStream);
		m_aiTargetMissions.readArray<int>(pStream);
	}
	if (iSaveVersion >= 8)
	{
		if (iSaveVersion >= 9)
			m_arThreatRating.read(pStream);
		else m_arThreatRating.readArray<scaled>(pStream);
	}
	else
	{
		CivPlayerMap<float> afThreatRating;
		if (iSaveVersion >= 6)
			afThreatRating.readArray<float>(pStream);
		else afThreatRating.readArray<double>(pStream);
		FOR_EACH_ENUM(CivPlayer)
		{
			m_arThreatRating.set(eLoopCivPlayer, scaled::fromDouble(
					afThreatRating.get(eLoopCivPlayer)));
		}
	}
	if (iSaveVersion >= 9)
	{
		m_aiVassalTechScore.read(pStream);
		m_aiVassalResourceScore.read(pStream);
		m_aiAdjLandPlots.read(pStream);
	}
	else
	{
		m_aiVassalTechScore.readArray<int>(pStream);
		m_aiVassalResourceScore.readArray<int>(pStream);
		m_aiAdjLandPlots.readArray<int>(pStream);
	}
	if (iSaveVersion >= 1)
	{
		if (iSaveVersion >= 8)
		{
			if (iSaveVersion >= 9)
				m_arRelativeNavyPow.read(pStream);
			else m_arRelativeNavyPow.readArray<scaled>(pStream);
		}
		else
		{
			CivPlayerMap<float> afRelativeNavyPow;
			if (iSaveVersion >= 6)
				afRelativeNavyPow.readArray<float>(pStream);
			else afRelativeNavyPow.readArray<double>(pStream);
			FOR_EACH_ENUM(CivPlayer)
			{
				m_arRelativeNavyPow.set(eLoopCivPlayer, scaled::fromDouble(
						afRelativeNavyPow.get(eLoopCivPlayer)));
			}
		}
	}
	if (iSaveVersion >= 8)
	{
		if (iSaveVersion >= 9)
			m_arWarAnger.read(pStream);
		else m_arWarAnger.readArray<scaled>(pStream);
	}
	else
	{
		CivPlayerMap<float> afWarAnger;
		if (iSaveVersion >= 6)
			afWarAnger.readArray<float>(pStream);
		else afWarAnger.readArray<double>(pStream);
		FOR_EACH_ENUM(CivPlayer)
		{
			m_arWarAnger.set(eLoopCivPlayer, scaled::fromDouble(
					afWarAnger.get(eLoopCivPlayer)));
		}
	}
	// <advc.035>
	if (iSaveVersion >= 2)
	{
		if (iSaveVersion >= 9)
			m_aiPlotsLostAtWar.read(pStream);
		else m_aiPlotsLostAtWar.readArray<int>(pStream);
	} // </advc.035>
	if (iSaveVersion >= 9)
		m_aiPastWarScore.read(pStream);
	else m_aiPastWarScore.readArray<int>(pStream);
	if (iSaveVersion < 4)
	{
		for (TeamIter<CIV_ALIVE> it; it.hasNext(); ++it)
			m_aiPastWarScore.multiply(it->getID(), 100);
	}
	if (iSaveVersion >= 9)
	{
		m_aiBounty.read(pStream);
		m_aeSponsorPerTarget.read(pStream);
		m_aiWarUtilityIgnoringDistraction.read(pStream);
	}
	else
	{
		m_aiBounty.readArray<int>(pStream);
		m_aeSponsorPerTarget.readArray<int>(pStream);
		m_aiWarUtilityIgnoringDistraction.readArray<int>(pStream);
	}
	if (iSaveVersion >= 3)
	{
		if (iSaveVersion >= 9)
			m_abCanBeHiredAgainst.read(pStream);
		else m_abCanBeHiredAgainst.readArray<bool>(pStream);
	}
	pStream->Read(&m_bOffensiveTrait);
	pStream->Read(&m_bDefensiveTrait);
	pStream->Read(&m_bCanScrub);
	pStream->Read(&m_bHaveDeepSeaTransports);
	pStream->Read(&m_bHaveAnyTransports);
	if (iSaveVersion >= 5)
		pStream->Read(&m_bFocusOnPeacefulVictory);
	{
		int iSize;
		pStream->Read(&iSize);
		for (int i = 0; i < iSize; i++)
		{
			TeamTypes eMaster;
			pStream->Read((int*)&eMaster);
			FAssertEnumBounds(eMaster);
			m_readyToCapitulateTo.insert(eMaster);
		}
	}
	if (iSaveVersion < 7)
	{
		int iSize;
		pStream->Read(&iSize);
		for (int i = 0; i < iSize; i++)
		{
			int iKey, iFirstVal, iSecondVal;
			pStream->Read(&iKey);
			pStream->Read(&iFirstVal);
			pStream->Read(&iSecondVal);
			// No longer used; just discard the data.
			//latestTurnReachableBySea[iKey] = std::make_pair(iFirstVal, iSecondVal);
		}
	}
	createMilitaryBranches();
	for (size_t i = 0; i < m_militaryPower.size(); i++)
		m_militaryPower[i]->read(pStream);
	pStream->Read(&m_iNonNavalUnits);
	if (iSaveVersion < 8)
	{
		double dTotalAssets;
		pStream->Read(&dTotalAssets);
		double dGoldPerProduction;
		pStream->Read(&dGoldPerProduction);
		m_rTotalAssets = scaled::fromDouble(dTotalAssets);
		m_rGoldPerProduction = scaled::fromDouble(dGoldPerProduction);
	}
	else
	{
		m_rTotalAssets.read(pStream);
		m_rGoldPerProduction.read(pStream);
	}
	if (iSaveVersion < 1)
		updateRelativeNavyPower();
}

/*	Called each turn. Some data are also updated throughout the turn, e.g. through
	reportUnitCreated. */
void UWAICache::update(bool bNewPlayer)
{
	PROFILE_FUNC();
	clear(true);
	m_bFocusOnPeacefulVictory = calculateFocusOnPeacefulVictory();
	// Needs to be done before updating cities
	updateTransports();
	TeamPathFinders* pPathFinders = NULL;
	if (TeamIter<MAJOR_CIV,OTHER_KNOWN_TO>::count(TEAMID(m_eOwner)) > 0)
	{	// Will have to reset these after each team; but allocate memory only once.
		pPathFinders = createTeamPathFinders();
	}
	for (TeamIter<MAJOR_CIV,KNOWN_TO> it(TEAMID(m_eOwner)); it.hasNext(); ++it)
		updateCities(it->getID(), pPathFinders);
	if (pPathFinders != NULL)
		deleteTeamPathFinders(*pPathFinders);
	sortCitiesByAttackPriority();
	updateTotalAssetScore();
	updateTargetMissionCounts();
	updateTypicalUnits();
	bool const bPlayerHistAvailable = (GC.getGame().getElapsedGameTurns() > 0 &&
			!bNewPlayer);
	if (bPlayerHistAvailable) // Can't do yield estimates on the first turn
		updateThreatRatings();
	if (!GET_PLAYER(m_eOwner).isAVassal())
		updateVassalScores();
	updateAdjacentLand();
	updateLostTilesAtWar(); // advc.035
	updateRelativeNavyPower();
	updateGoldPerProduction();
	updateWarAnger();
	updateCanScrub();

	/*	(Apart from the yield estimation problem, the other players' caches
		wouldn't be up to date, which can cause problems in scenarios.) */
	if (bPlayerHistAvailable)
	{	// Any cache data used by war evaluation needs to be updated before this!
		updateWarUtility();
	}
}


TeamPathFinders* UWAICache::createTeamPathFinders() const
{
	/*	Would be nice to make one instance of each TeamPathFinder class a member of
		CvTeam rather than creating temporary instances. However - see the comment in
		KmodPathFinder::resetNodes. */
	CvTeam const& kCacheTeam = GET_TEAM(m_eOwner);
	using namespace TeamPath;
	return new TeamPathFinders(
			*new TeamPathFinder<LAND>(kCacheTeam),
			*new TeamPathFinder<ANY_WATER>(kCacheTeam),
			*new TeamPathFinder<SHALLOW_WATER>(kCacheTeam));
}


void UWAICache::deleteTeamPathFinders(TeamPathFinders& kPathFinders)
{
	delete &kPathFinders.landFinder();
	delete &kPathFinders.anyWaterFinder();
	delete &kPathFinders.shallowWaterFinder();
	delete &kPathFinders;
}


void UWAICache::resetTeamPathFinders(TeamPathFinders& kPathFinders,
	TeamTypes eWarTarget) const
{
	int const iSeaLimit = getUWAI().maxSeaDist() * shipSpeed();
	int const iLandLimit = getUWAI().maxLandDist();
	CvTeam const* pWarTarget = &GET_TEAM(eWarTarget);
	kPathFinders.landFinder().reset(pWarTarget, iLandLimit);
	kPathFinders.anyWaterFinder().reset(pWarTarget, iSeaLimit);
	kPathFinders.shallowWaterFinder().reset(pWarTarget, iSeaLimit);
}


void UWAICache::updateCities(TeamTypes eTeam, TeamPathFinders* pPathFinders)
{
	PROFILE_FUNC();
	CvTeamAI const& kCacheTeam = GET_TEAM(m_eOwner);
	bool const bHuman = GET_PLAYER(m_eOwner).isHuman();
	if (eTeam == kCacheTeam.getID())
		pPathFinders = NULL;
	else resetTeamPathFinders(*pPathFinders, eTeam);
	for (MemberAIIter itMember(eTeam); itMember.hasNext(); ++itMember)
	{
		FOR_EACH_CITY_VAR(pCity, *itMember)
		{
			// pCity.isRevealed() impedes the AI too much
			if (eTeam == kCacheTeam.getID() ||
				// Assume that human can locate all cities of known civs
				bHuman || kCacheTeam.AI_deduceCitySite(*pCity))
			{
				add(*new City(m_eOwner, *pCity, pPathFinders));
			}
		}
	}
}


void UWAICache::add(City& kCacheCity)
{
	m_cityList.push_back(&kCacheCity);
	m_cityMap.insert(std::make_pair(kCacheCity.getID(), &kCacheCity));
	PlayerTypes eCityOwner = kCacheCity.city().getOwner();
	if (TEAMID(eCityOwner) != TEAMID(m_eOwner) && kCacheCity.canReach())
		m_aiReachableCities.add(eCityOwner, 1);
}

/*	Only for updates triggered by unit movement of other players.
	Caller is assumed to check visibility and civ status
	(the cache only covers major civs). */
void UWAICache::add(CvCity& kCity)
{
	TeamPathFinders* pPathFinders = NULL;
	if (kCity.getTeam() != TEAMID(m_eOwner))
	{
		pPathFinders = createTeamPathFinders();
		resetTeamPathFinders(*pPathFinders, kCity.getTeam());
	}
	add(*new City(m_eOwner, kCity, pPathFinders));
	if (pPathFinders != NULL)
		deleteTeamPathFinders(*pPathFinders);
}


void UWAICache::remove(CvCity const& kCity)
{
	City* pCacheCity = NULL;
	std::map<PlotNumTypes,City*>::iterator posMap = m_cityMap.find(kCity.plotNum());
	if (posMap != m_cityMap.end())
		pCacheCity = posMap->second;
	if (pCacheCity == NULL) // OK, caller doesn't need to rule this out.
		return;
	PlayerTypes eOldCityOwner = pCacheCity->city().getOwner();
	if (TEAMID(eOldCityOwner) != TEAMID(m_eOwner) && pCacheCity->canReach())
		m_aiReachableCities.add(eOldCityOwner, -1);
	m_cityMap.erase(posMap);
	std::vector<City*>::iterator posVector = std::find(
			m_cityList.begin(), m_cityList.end(), pCacheCity);
	if (posVector == m_cityList.end())
	{
		FAssert(posVector != m_cityList.end());
		return;
	}
	delete *posVector;
	m_cityList.erase(posVector);
}


void UWAICache::updateTotalAssetScore()
{
	// For Palace; it's counted as a national wonder below, but it's worth another 5.
	m_rTotalAssets = 5;
	for (int i = numCities() - 1; i >= 0; i--)
	{
		City const& kCacheCity = cityAt(i);
		if (!kCacheCity.isOwnTeamCity())
			break; // Sorted so that cities of owner's team are at the end
		CvCity& kCity = kCacheCity.city();
		if (kCity.getOwner() == m_eOwner)
		{
			m_rTotalAssets += kCacheCity.getAssetScore() +
					/*	National wonders aren't included in the per-city asset score
						b/c they shouldn't count for rival cities. */
					kCity.getNumNationalWonders() * 4;
		}
	}
}


void UWAICache::updateGoldPerProduction()
{
	/*	Akin in purpose to CvPlayerAI::AI_yieldWeight - which, however,
		isn't much more than a stub. */
	m_rGoldPerProduction = std::max(goldPerProdBuildings(), goldPerProdSites());
	m_rGoldPerProduction *= GET_PLAYER(m_eOwner).uwai().amortizationMultiplier();
	m_rGoldPerProduction.increaseTo(goldPerProdProcess());
	m_rGoldPerProduction.increaseTo(1); // (even if w/o a good coversion process)
	m_rGoldPerProduction.increaseTo(goldPerProdVictory());
	/*	Currently, this ratio is pretty much 1. Just so that any changes
		to AI_yieldWeight or Civ4YieldInfos.xml are taken into account here. */
	m_rGoldPerProduction.mulDiv(
			GET_PLAYER(m_eOwner).AI_yieldWeight(YIELD_PRODUCTION), 225);
}

namespace
{
	scaled const rGoldPerProductionCap = fixp(4.5);
}

scaled UWAICache::goldPerProdBuildings()
{
	PROFILE_FUNC();
	std::vector<scaled> arWonderCounts;
	std::vector<scaled> arNonWonderCounts;
	CvPlayerAI const& kOwner = GET_PLAYER(m_eOwner);
	int const iOwnerEra = kOwner.getCurrentEra();
	ReligionTypes const eOwnerReligion = kOwner.getStateReligion();
	FOR_EACH_CITY(pCity, kOwner)
	{
		/*	Tbd.? CvCiytAI::AI_buildingValue has a cache, so it might be possible
			to do a calculation here based on that, CvCity::getProductionNeeded
			and CvPlayerAI::AI_targetAmortizationTurns. */
		int iWonders = 0;
		int iNonWonders = 0;
		FOR_EACH_ENUM2(Building, eBuilding)
		{
			CvBuildingInfo const& kBuilding = GC.getInfo(eBuilding);
			if (pCity->canConstruct(eBuilding) &&
				!kBuilding.isCapital() && // exclude Palace
				// War preparations probably won't cause the city to switch
				pCity->getProductionBuilding() != eBuilding)
			{
				{	// Soon obsolete
					TechTypes eObsTech = kBuilding.getObsoleteTech();
					if (eObsTech != NO_TECH &&
						GC.getInfo(eObsTech).getEra() <= iOwnerEra)
					{
						continue;
					}
				}
				if (kBuilding.getReligionType() != NO_RELIGION &&
					// If in a state religion, count only buildings of that religion.
					eOwnerReligion != NO_RELIGION &&
					kBuilding.getReligionType() != eOwnerReligion)
				{
					continue;
				}
				if (kBuilding.isLimited())
					iWonders++;
				else iNonWonders++;
			}
		}
		arNonWonderCounts.push_back(iNonWonders);
		arWonderCounts.push_back(iWonders);
	}
	if (arNonWonderCounts.empty()) // No city founded yet
		return 2;
	// Cities about to be founded; will soon need buildings.
	int iFutureCities = (fixp(0.6) * std::min(
			kOwner.AI_getNumAIUnits(UNITAI_SETTLE),
			kOwner.AI_getNumCitySites())).uround();
	scaled const rMaxNonWonderCount = stats::max(arNonWonderCounts);
	for (int i = 0; i < iFutureCities; i++)
		arNonWonderCounts.push_back(rMaxNonWonderCount);
	CvLeaderHeadInfo const& kOwnerPersonality = GC.getInfo(
			kOwner.getPersonalityType());
	scaled rMedianDesiredBuildings = stats::median(arNonWonderCounts) +
			scaled::max(0, stats::median(arWonderCounts) -
			/*	Assume one useless (small or great) wonder per era, but two for
				Classical. (Should work well enough with custom eras as well;
				not adding a bAgeOfWonders flag to CvEraInfo via advc.erai.) */
			(std::min(5, iOwnerEra) + (iOwnerEra > 0 ? 1 : 0))) *
			// WCR=30 is typical
			scaled(kOwnerPersonality.getWonderConstructRand() + 20, 50);
	// Assume 6 desirable buildings (incl. wonders) made available per era
	int const iMaxDesiredBuildings = (iOwnerEra + 1) * 6;
	scaled r = rMedianDesiredBuildings / iMaxDesiredBuildings;
	// The more units, the fewer buildings. (BUP=25 is typical.)
	r *= scaled(100 - kOwnerPersonality.getBuildUnitProb(), 75);
	r.decreaseTo(1);
	r *= rGoldPerProductionCap;
	return r;
}


scaled UWAICache::goldPerProdSites()
{
	PROFILE_FUNC();
	CvPlayerAI const& kOwner = GET_PLAYER(m_eOwner);
	std::vector<int> aiFoundVals;
	for (int i = 0; i < kOwner.AI_getNumCitySites(); i++)
	{
		aiFoundVals.push_back(kOwner.AI_getCitySite(i).getFoundValue(kOwner.getID()));
	}
	std::sort(aiFoundVals.begin(), aiFoundVals.end(), std::greater<int>());
	scaled arSiteWeights[] = { 1, fixp(0.8), fixp(0.6), fixp(0.4), fixp(0.2) };
	int const iSitesMax = ARRAYSIZE(arSiteWeights);
	scaled rSiteScore;
	int const iSettlers = kOwner.AI_getNumAIUnits(UNITAI_SETTLE);
	for (int i = iSettlers; i < std::min(iSitesMax, (int)aiFoundVals.size()); i++)
	{
		/*	Once the settlers have been used, the found value of more remote sites
			may increase a bit
			(see rShapeWeight in AIFoundValue::adjustToCivSurroundings) */
		rSiteScore += (aiFoundVals[i] * (arSiteWeights[i] + iSettlers) / 10) / 2500;
	}
	/*	Don't want to count faraway Barbarian cities. Reference value set after
		looking at some sample targetCityValues; let's hope these generalize. */
	int const iRefVal = 50;
	FOR_EACH_CITY(pBarbCity, GET_PLAYER(BARBARIAN_PLAYER))
	{
		if (GET_TEAM(kOwner.getTeam()).AI_deduceCitySite(*pBarbCity))
		{
			int const iTargetVal = kOwner.AI_targetCityValue(*pBarbCity, false, true);
			if (iTargetVal > 0)
				rSiteScore += scaled(std::min(iTargetVal, iRefVal), iRefVal).pow(3);
		}
	}
	CvGameAI const& kGame = GC.AI_getGame();
	int const iGameEra = kGame.getCurrentEra();
	/*	Rage option makes it more worthwhile to focus on early expansion (at least
		for the AI), regardless of whether the additional cities are new or
		conquered from the Barbarians. */
	if (kGame.isOption(GAMEOPTION_RAGING_BARBARIANS) &&
		(kGame.AI_getCurrEraFactor() < fixp(1.5) || iGameEra == kGame.getStartEra()))
	{
		rSiteScore *= fixp(1.25);
	}
	int const iCities = std::max(1, kOwner.getNumCities());
	// Shouldn't expect to claim all sites with few cities
	rSiteScore.decreaseTo(iCities);
	scaled r = std::min(rGoldPerProductionCap,
			rGoldPerProductionCap * rSiteScore / iCities);
	return r;
}


scaled UWAICache::goldPerProdProcess()
{
	scaled r;
	FOR_EACH_ENUM(Process)
	{
		if (GET_PLAYER(m_eOwner).canMaintain(eLoopProcess))
		{
			r.increaseTo(per100(GC.getInfo(eLoopProcess).
					getProductionToCommerceModifier(COMMERCE_RESEARCH)));
			r.increaseTo(per100(GC.getInfo(eLoopProcess).
					getProductionToCommerceModifier(COMMERCE_GOLD)));
		}
	}
	/*	If our buildings are so bad that a process is our best option - but we do
		at least have a process - then we shouldn't necessarily wage war; focusing
		on tech might help us more. This function is supposed to say how much we
		value production in terms of gold, not how much we value gold or research.
		So it would more consistent to make this adjustment, say, in WarUtilityAspect
		::Effort. However, it's convenient to do it here b/c we've already determined
		whether we've run out of buildings to construct. */
	return r * fixp(1.28);
}


scaled UWAICache::goldPerProdVictory()
{
	CvTeamAI const& kOwnerTeam = GET_TEAM(m_eOwner);
	int iOwnerVictoryStage = 0;
	if (kOwnerTeam.AI_anyMemberAtVictoryStage(AI_VICTORY_CULTURE3 | AI_VICTORY_SPACE3))
		iOwnerVictoryStage = 3;
	else if(kOwnerTeam.AI_anyMemberAtVictoryStage(AI_VICTORY_CULTURE4 | AI_VICTORY_SPACE4))
		iOwnerVictoryStage = 4;
	if (iOwnerVictoryStage < 3)
	{
		if (kOwnerTeam.AI_anyMemberAtVictoryStage(AI_VICTORY_CULTURE2 | AI_VICTORY_SPACE2))
			return 1;
		return fixp(0.5);
	}
	scaled r = iOwnerVictoryStage + 1;
	for (TeamAIIter<MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> itRival(kOwnerTeam.getID());
		itRival.hasNext(); ++itRival)
	{
		int iRivalVictoryStage = 0;
		if (itRival->AI_anyMemberAtVictoryStage3())
			iRivalVictoryStage = 3;
		else if (itRival->AI_anyMemberAtVictoryStage4())
			iRivalVictoryStage = 4;
		if (iRivalVictoryStage >= iOwnerVictoryStage)
			r--;
		if (iRivalVictoryStage > iOwnerVictoryStage)
			r--;
	}
	return r;
}


void UWAICache::updateWarUtility()
{
	PROFILE_FUNC();
	if(!getUWAI().isReady())
		return;
	CvTeamAI const& kOwnerTeam = GET_TEAM(m_eOwner);
	if (m_eOwner != kOwnerTeam.getLeaderID())
		return;
	for (TeamIter<FREE_MAJOR_CIV> itTarget; itTarget.hasNext(); ++itTarget)
	{
		if (kOwnerTeam.uwai().isWarEvalNeeded(itTarget->getID()))
			updateWarUtilityIgnDistraction(itTarget->getID());
	}
}


void UWAICache::updateWarUtilityIgnDistraction(TeamTypes eTarget)
{
	CvTeamAI const& kOwnerTeam = GET_TEAM(m_eOwner);
	FAssert(m_eOwner == kOwnerTeam.getLeaderID());
	if (kOwnerTeam.isAVassal()) // Not needed for vassals
	{
		m_aiWarUtilityIgnoringDistraction.set(eTarget, 0);
		return;
	}
	UWAIReport report(true); // silent
	WarEvalParameters params(kOwnerTeam.getID(), eTarget, report,
			true); // Ignore distraction cost
	WarEvaluator eval(params);
	WarPlanTypes eWP = kOwnerTeam.AI_getWarPlan(eTarget);
	int iPrepTime = 0;
	// Just limited war and naval based on AI_isLandTarget is good enough here
	if (eWP == NO_WARPLAN)
	{
		eWP = WARPLAN_PREPARING_LIMITED;
		if (!kOwnerTeam.AI_isPushover(eTarget))
			iPrepTime = 5;
	}
	m_aiWarUtilityIgnoringDistraction.set(eTarget, eval.evaluate(
			eWP, !kOwnerTeam.AI_isLandTarget(eTarget), iPrepTime));
}


void UWAICache::updateWarAnger()
{
	CvPlayerAI const& kOwner = GET_PLAYER(m_eOwner);
	if (kOwner.isAnarchy())
		return;
	/*	Would be interesting to know the hypothetical anger from war weariness,
		i.e. assuming that war breaks out. Currently, we only consider anger
		from ongoing wars. */
	scaled rAngerScore;
	FOR_EACH_CITY(pCity, kOwner)
	{
		if (pCity->isDisorder())
			continue;
		/*	Disregard happiness from culture rate unless we need culture
			regardless of happiness */
		int iAngry = pCity->angryPopulation(0,
				!kOwner.AI_atVictoryStage(AI_VICTORY_CULTURE3) &&
				!kOwner.AI_atVictoryStage(AI_VICTORY_CULTURE4));
		rAngerScore += scaled::min(iAngry, scaled(
				pCity->getWarWearinessPercentAnger() * pCity->getPopulation(),
				GC.getPERCENT_ANGER_DIVISOR()));
	}
	if (rAngerScore <= 0)
		return;
	// Who causes the anger?
	CivTeamMap<int> aiAngerContrib;
	int iTotalAngerContribs = 0;
	for (TeamIter<MAJOR_CIV,ENEMY_OF> itEnemy(kOwner.getTeam());
		itEnemy.hasNext(); ++itEnemy)
	{
		/*	Never mind all the modifiers in CvPlayer::updateWarWearinessPercentAnger;
			they apply equally to each contribution. */
		int iContrib = GET_TEAM(kOwner.getTeam()).
				getWarWeariness(itEnemy->getID(), true);
		aiAngerContrib.set(itEnemy->getID(), iContrib);
		iTotalAngerContribs += iContrib;
	}
	if (iTotalAngerContribs <= 0)
		return;
	for (PlayerIter<CIV_ALIVE,ENEMY_OF> itEnemy(kOwner.getTeam());
		itEnemy.hasNext(); ++itEnemy)
	{
		m_arWarAnger.set(itEnemy->getID(), rAngerScore *
				// Turn per-team into per-civ
				scaled(aiAngerContrib.get(itEnemy->getTeam()), iTotalAngerContribs) /
				GET_TEAM(kOwner.getTeam()).getNumMembers());
	}
}


void UWAICache::updateCanScrub()
{
	static FeatureTypes eFallout = NO_FEATURE; // why not cache it
	if (eFallout == NO_FEATURE)
	{
		FOR_EACH_ENUM(Feature)
		{
			if (GC.getInfo(eLoopFeature).getHealthPercent() <= -50)
			{
				eFallout = eLoopFeature;
				break;
			}
		}
	}
	FOR_EACH_ENUM(Build)
	{
		TechTypes eFeatureTech = GC.getInfo(eLoopBuild).getFeatureTech(eFallout);
		if (eFeatureTech != NO_TECH && GET_TEAM(m_eOwner).isHasTech(eFeatureTech))
		{
			m_bCanScrub = true;
			break;
		}
	}
}


void UWAICache::updateTransports()
{
	PROFILE_FUNC();
	CvPlayerAI const& kOwner = GET_PLAYER(m_eOwner);
	CvCivilization const& kOwnerCiv = kOwner.getCivilization();
	for (int i = 0; i < kOwnerCiv.getNumUnits(); i++)
	{
		UnitTypes const eUnit = kOwnerCiv.unitAt(i);
		CvUnitInfo const& kUnit = GC.getInfo(eUnit);
		if (kUnit.getUnitAIType(UNITAI_ASSAULT_SEA) && kOwner.canTrain(eUnit))
		{
			m_bHaveAnyTransports = true;
			if (!kOwner.AI_isAnyImpassable(eUnit))
				m_bHaveDeepSeaTransports = true;
		}
	}
}


bool UWAICache::calculateFocusOnPeacefulVictory()
{
	CvPlayerAI const& kOwner = GET_PLAYER(m_eOwner);
	if (kOwner.AI_atVictoryStage(AI_VICTORY_CULTURE4 | AI_VICTORY_SPACE4))
		return true;
	if (kOwner.AI_atVictoryStage4() || // (Diplo doesn't count as peaceful)
		(!kOwner.AI_atVictoryStage(AI_VICTORY_CULTURE3) &&
		!kOwner.AI_atVictoryStage(AI_VICTORY_SPACE3)))
	{
		return false;
	}
	bool const bHuman = kOwner.isHuman();
	// Space3 or Culture3 -- but is there a rival at stage 4?
	for (PlayerAIIter<MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> itRival(kOwner.getTeam());
		itRival.hasNext(); ++itRival)
	{
		if (!itRival->AI_atVictoryStage(AI_VICTORY_CULTURE4) &&
			!itRival->AI_atVictoryStage(AI_VICTORY_SPACE4))
		{
			continue;
		}
		// Could we possibly(!) stop them? Would we want to?
		if (!bHuman && kOwner.AI_getAttitude(itRival->getID()) >= ATTITUDE_FRIENDLY)
			continue;
		CvTeamAI const& kRivalTeam = GET_TEAM(itRival->getTeam());
		if (kRivalTeam.AI_getWarSuccessRating() < 0)
			return false;
		if (GET_TEAM(kOwner.getTeam()).getPower(true) * (bHuman ? 5 : 4) >
			kRivalTeam.getPower(false) * 3)
		{
			return false;
		}
	}
	return true;
}


int UWAICache::shipSpeed() const
{
	MilitaryBranch const* pLogistics = getPowerValues()[LOGISTICS];
	if (pLogistics != NULL)
	{
		UnitTypes eTypicalTransport = pLogistics->getTypicalUnit();
		if (eTypicalTransport != NO_UNIT)
			return GC.getInfo(eTypicalTransport).getMoves();
	}
	// Fallback (needed?)
	return ::range(GET_PLAYER(m_eOwner).getCurrentEra() + 1, 3, 5);
}


void UWAICache::setCanBeHiredAgainst(TeamTypes eTeam, bool b)
{
	leaderCache().m_abCanBeHiredAgainst.set(eTeam, b);
}


void UWAICache::updateCanBeHiredAgainst(TeamTypes eTeam,
	int iWarUtility, int iUtilityThresh)
{
	// (Part of the update happens in UWAI::Team::doWar)
	scaled rProb = -1;
	if (!m_abCanBeHiredAgainst.get(eTeam))
		rProb = std::min(fixp(0.58), (iWarUtility - fixp(1.5) * iUtilityThresh) / 100);
	else rProb = scaled(1 - (iUtilityThresh - iWarUtility), 100);
	m_abCanBeHiredAgainst.set(eTeam, SyncRandSuccess(rProb));
}


UWAICache const& UWAICache::leaderCache() const
{
	if (m_eOwner == GET_TEAM(m_eOwner).getLeaderID())
		return *this;
	return GET_PLAYER(GET_TEAM(m_eOwner).getLeaderID()).uwai().getCache();
}

UWAICache& UWAICache::leaderCache()
{
	if (m_eOwner == GET_TEAM(m_eOwner).getLeaderID())
		return *this;
	return GET_PLAYER(GET_TEAM(m_eOwner).getLeaderID()).uwai().getCache();
}


void UWAICache::sortCitiesByAttackPriority()
{
	PROFILE_FUNC();
	/*	Selection sort b/c I want to factor in city areas. An invading army tends
		to stay in one area until all cities there are conquered. */
	for (int i = 0; i < numCities() - 1; i++)
	{
		CvCity* pPrevCity = NULL;
		if (i > 0)
			pPrevCity = &m_cityList[i - 1]->city();
		CvArea const* pPrevArea = (pPrevCity == NULL ? NULL : &pPrevCity->getArea());
		scaled rMaxPriority = -100;
		int iArgMax = -1;
		for (int j = i; j < numCities(); j++)
		{
			scaled rPriority = m_cityList[j]->attackPriority();
			if (i > 0 && pPrevArea != NULL && !m_cityList[j]->city().isArea(*pPrevArea) &&
				rPriority.isPositive())
			{
				rPriority /= 2;
			}
			if (rPriority > rMaxPriority)
			{
				iArgMax = j;
				rMaxPriority = rPriority;
			}
		}
		if (iArgMax >= 0)
			std::swap(m_cityList[i], m_cityList[iArgMax]);
	}
}


CvCity& UWAICache::cvCityById(PlotNumTypes ePlot)
{
	return *GC.getMap().getPlotByIndex(ePlot).getPlotCity();
}


void UWAICache::updateTraits()
{
	m_bOffensiveTrait = false;
	m_bDefensiveTrait = false;
	FOR_EACH_ENUM(Trait)
	{
		if (!GET_PLAYER(m_eOwner).hasTrait(eLoopTrait) ||
			!GC.getInfo(eLoopTrait).isAnyFreePromotion())
		{
			continue;
		}
		FOR_EACH_ENUM(Promotion)
		{
			if (!GC.getInfo(eLoopTrait).isFreePromotion(eLoopPromotion))
				continue;
			if (GC.getInfo(eLoopPromotion).getCombatPercent() > 0)
				m_bOffensiveTrait = true;
			else if (GC.getInfo(eLoopPromotion).getCityDefensePercent() > 0)
				m_bDefensiveTrait = true;
		}
	}
}


void UWAICache::updateTargetMissionCounts()
{
	/*	Doesn't hurt to count missions to non-rival territory
		(though it's a waste of time I guess ...) */
	for (PlayerIter<MAJOR_CIV,KNOWN_TO> it(TEAMID(m_eOwner)); it.hasNext(); ++it)
		updateTargetMissionCount(it->getID());
}


void UWAICache::updateThreatRatings()
{
	for (PlayerIter<MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> it(TEAMID(m_eOwner));
		it.hasNext(); ++it)
	{
		m_arThreatRating.set(it->getID(), calculateThreatRating(it->getID()));
	}
}


void UWAICache::updateVassalScores()
{
	for(PlayerIter<FREE_MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> it(TEAMID(m_eOwner));
		it.hasNext(); ++it)
	{
		updateVassalScore(it->getID());
	}
}


void UWAICache::updateAdjacentLand()
{
	PROFILE_FUNC();
	CvMap const& kMap = GC.getMap();
	for (int i = 0; i < kMap.numPlots(); i++)
	{
		CvPlot const& kPlot = kMap.getPlotByIndex(i);
		if (kPlot.isWater())
			continue;
		PlayerTypes const ePlotOwner = kPlot.getOwner();
		if (ePlotOwner == NO_PLAYER || !GET_PLAYER(ePlotOwner).isAlive() ||
			!GET_PLAYER(ePlotOwner).isMajorCiv() ||
			TEAMID(ePlotOwner) == TEAMID(m_eOwner))
		{
			continue;
		}
		if (kPlot.isAdjacentPlayer(m_eOwner, true))
			m_aiAdjLandPlots.add(ePlotOwner, 1);
	}
}

// advc.035:
void UWAICache::updateLostTilesAtWar()
{
	//PROFILE_FUNC();
	if (!GC.getDefineBOOL(CvGlobals::OWN_EXCLUSIVE_RADIUS))
		return;
	CvTeam const& kOwnerTeam = GET_TEAM(m_eOwner);
	for (TeamIter<MAJOR_CIV,NOT_SAME_TEAM_AS> itOther(kOwnerTeam.getID());
		itOther.hasNext(); ++itOther)
	{
		std::vector<CvPlot*> apFlipped;
		::contestedPlots(apFlipped, kOwnerTeam.getID(), itOther->getID());
		int iLost = 0;
		for (size_t j = 0; j < apFlipped.size(); j++)
		{
			TeamTypes ePlotTeam = apFlipped[j]->getTeam(); // current tile owner
			// Count the tiles that kOwnerTeam loses when at war with itOther
			if (ePlotTeam == (kOwnerTeam.isAtWar(itOther->getID()) ?
				itOther->getID() : kOwnerTeam.getID()))
			{
				iLost++;
			}
		}
		m_aiPlotsLostAtWar.set(itOther->getID(), iLost);
	}
}


void UWAICache::updateRelativeNavyPower()
{
	/*PROFILE_FUNC();
	for(PlayerIter<MAJOR_CIV> it; it.hasNext(); ++it) {
		PlayerTypes const ePlayer = it->getID();*/
		/*	Tbd.:
			Exact result: (their navy power) /
						  (their total power from navy, army, home guard)

			Intelligence ratio (100%: assume we know all their positions;
			0: we know nothing, in particular if
			!GET_TEAM(ePlayer).isHasMet(TEAMID(m_eOwner))).

			-100%
			+100% * #(their cities visible to us) / #(their cities)
			+100% * #(their cities revealed to us) / #(their cities)
				+25% if OB, otherwise
				+max{0, -25% + 50% * #(our spies)/ #(cities revealed to us)}
			+10% * (our era) + 5% * (war plan age)
				+range(closeness%, 0, 100%) if same capital area, otherwise
				+#(their coastal cities revealed to us) / #(their cities) *
						(50 + 10 * #(our sea patrols) + #(our explorers))

			Result guessed based on revealed info on map:
			(0.7 * #(their revealed coastal cities) / #(their revealed cities))
			/ (2 + #(rivals on their continent)
			Watch out for div by 0.
			Return average weighted by int. ratio of exact and guessed result.
			Apply result after copying of the exact values in InvasionGraph, and
			in WarUtilityAspect::LossesFromBlockade.
			Int. ratio might have further uses in the future (would have to
			store it separately then though). */
	//}
	// CvTeamAI::AI_getRivalAirPower also cheats with per-branch power values
}

/*	Based on CvPlayerAI::AI_enemyTargetMissions.
	(Need target missions per player, not per team.) */
void UWAICache::updateTargetMissionCount(PlayerTypes ePlayer)
{
	int iMissions = 0;
	CvPlayerAI const& kOwner = GET_PLAYER(m_eOwner);
	FOR_EACH_GROUPAI(pGroup, kOwner)
	{
		if (pGroup->getNumUnits() <= 0) // Can be empty
			continue;
		CvPlot const* pMissionPlot = pGroup->AI_getMissionAIPlot();
		/*	Humans don't (typically?) have missions, but at least we can
			count the boots on the ground. */
		if (pMissionPlot == NULL)
			pMissionPlot = pGroup->plot();
		if (pMissionPlot->getOwner() == ePlayer)
		{
			iMissions += pGroup->getNumUnits();
			iMissions += pGroup->getCargo();
		}
	}
	m_aiTargetMissions.set(ePlayer, iMissions);
}


scaled UWAICache::calculateThreatRating(PlayerTypes eRival) const
{
	// Can't reliably estimate yield rates in the early game
	if (GC.getGame().getCurrentEra() <= GC.getGame().getStartEra())
		return 0;
	/*	Check rival's cache to see if cache owner's capital is reachable
		for rival (mild cheat) */
	CvCity const* pCapital = GET_PLAYER(m_eOwner).getCapital();
	City const* pCacheCapital = NULL;
	if (pCapital != NULL)
	{
		pCacheCapital = GET_PLAYER(eRival).uwai().getCache().lookupCity(
				pCapital->plotNum());
	}
	if (pCacheCapital != NULL && !pCacheCapital->canReach())
		return 0;
	return teamThreat(TEAMID(eRival));
}


scaled UWAICache::teamThreat(TeamTypes eRival) const
{
	// A bit of overlap with the paranoia calculation in CvPlayerAI
	CvTeamAI const& kRival = GET_TEAM(eRival);
	TeamTypes eOwnerTeam = TEAMID(m_eOwner);
	AttitudeTypes const eTowardOwner = (kRival.isHuman() ? ATTITUDE_CAUTIOUS :
			kRival.AI_getAttitude(eOwnerTeam));
	if (kRival.isAVassal() || eTowardOwner >= ATTITUDE_FRIENDLY ||
		// Don't worry about long-term threat if they're already close to victory
		kRival.AI_anyMemberAtVictoryStage4())
	{
		return 0;
	}
	scaled rRivalPow = longTermPower(eRival);
	scaled rOwnerPow = longTermPower(GET_TEAM(eOwnerTeam).getMasterTeam(), true);
	if (kRival.isHuman())
		rOwnerPow *= GET_PLAYER(m_eOwner).uwai().confidenceAgainstHuman();
	rOwnerPow.increaseTo(scaled::epsilon());
	scaled rPowFactor = rRivalPow / rOwnerPow - fixp(0.75);
	rPowFactor.clamp(0, 1);
	/*	(If presently at war, attitude is likely to improve in the medium term.
		That said, the present war suggests a clash of interests that may persist
		in the long run. Assume that these factors cancel out, and
		don't adjust attitude.) */
	scaled rDiploFactor(ATTITUDE_FRIENDLY - eTowardOwner, 4);
	FAssert(rDiploFactor.isPositive());
	if (kRival.AI_anyMemberAtVictoryStage(AI_VICTORY_CONQUEST2))
		rDiploFactor += fixp(0.15);
	else if (kRival.AI_anyMemberAtVictoryStage(AI_VICTORY_DIPLOMACY2))
		rDiploFactor += fixp(0.1);
	// Nuclear deterrent
	if (GET_PLAYER(m_eOwner).getNumNukeUnits() > 0)
		rDiploFactor -= fixp(0.2);
	rDiploFactor.clamp(0, 1);
	// Less likely to attack us if there are many targets to choose from
	scaled rAltTargetsDivisor(TeamIter<FREE_MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF>::
			count(eRival) + 1, 5);
	rAltTargetsDivisor.exponentiate(fixp(0.7));
	rAltTargetsDivisor.increaseTo(fixp(0.35));
	return rDiploFactor * rPowFactor / rAltTargetsDivisor;
}


scaled UWAICache::longTermPower(TeamTypes eTeam, bool bDefensive) const
{
	CvTeamAI const& kOwnerTeam = GET_TEAM(m_eOwner);
	scaled r;
	for (PlayerAIIter<MAJOR_CIV> itAlly; itAlly.hasNext(); ++itAlly)
	{
		CvPlayerAI const& kAlly = *itAlly;
		PlayerTypes const eAlly = kAlly.getID();
		TeamTypes const eAllyMaster = kAlly.getMasterTeam();
		if (eAllyMaster != eTeam &&
			(!bDefensive || !GET_TEAM(eAllyMaster).isDefensivePact(eTeam)))
		{
			continue;
		}
		UWAI::Player const& kAllyUWAI = kAlly.uwai();
		MilitaryBranch const& kArmy = *kAllyUWAI.getCache().getPowerValues()[ARMY];
		scaled const rTypicalUnitCost = kArmy.getTypicalCost();
		if (rTypicalUnitCost <= 0)
			continue;
		/*	Long-term power mostly depends on production capacity and willingness
			to produce units. That said, 50~100 turns are also enough to
			translate food yield into additional production and commerce
			into better units. */
		r += (kOwnerTeam.AI_estimateYieldRate(eAlly, YIELD_PRODUCTION) +
				fixp(0.35) * kOwnerTeam.AI_estimateYieldRate(eAlly, YIELD_FOOD) +
				fixp(0.25) * kOwnerTeam.AI_estimateYieldRate(eAlly, YIELD_COMMERCE)) *
				(kAllyUWAI.buildUnitProb() + fixp(0.15)) *
				kArmy.getTypicalPower() / rTypicalUnitCost;
	}
	return r;
}


void UWAICache::updateVassalScore(PlayerTypes eRival)
{
	int iTechScore = 0;
	FOR_EACH_ENUM(Tech)
	{
		if (GET_PLAYER(eRival).canTradeItem(m_eOwner, TradeData(
			TRADE_TECHNOLOGIES, eLoopTech), false))
		{
			iTechScore += GET_TEAM(m_eOwner).AI_techTradeVal(
					eLoopTech, TEAMID(eRival), true);
		}
	}
	m_aiVassalTechScore.set(eRival, iTechScore);
	int iMasterBonuses = 0;
	int iTributes = 0;
	FOR_EACH_ENUM(Bonus)
	{
		if (GET_TEAM(m_eOwner).isBonusObsolete(eLoopBonus))
			continue;
		TechTypes const eRevealTech = GC.getInfo(eLoopBonus).getTechReveal();
		if (GET_TEAM(m_eOwner).isHasTech(eRevealTech))
		{
			if (GET_PLAYER(m_eOwner).getNumAvailableBonuses(eLoopBonus) > 0)
			{
				iMasterBonuses++;
				continue;
			}
		}
		/*	Don't mind if we can't use it yet (TechCityTrade), but we can't know
			that they have it if we can't see it. */
		else continue;
		if (GET_TEAM(eRival).isHasTech(eRevealTech) &&
			// Can't trade obsolete resource
			!GET_TEAM(eRival).isBonusObsolete(eLoopBonus) &&
			GET_PLAYER(eRival).getNumAvailableBonuses(eLoopBonus) > 0)
		{
			iTributes++;
		}
	}
	m_aiVassalResourceScore.set(eRival,
			scaled(25 * iTributes, std::max(4, iMasterBonuses)).round());
}

// Called once all CvCity objects have been loaded 
void UWAICache::cacheCitiesAfterRead()
{
	for (int i = 0; i < numCities(); i++)
		cityAt(i).cacheCvCity();
}


void UWAICache::reportUnitCreated(UnitTypes eUnit)
{
	reportUnit(eUnit, 1);
}


void UWAICache::reportUnitDestroyed(UnitTypes eUnit)
{
	reportUnit(eUnit, -1);
}


void UWAICache::reportUnit(UnitTypes eUnit, int iChange)
{
	/*	i=1: skip HOME_GUARD. Potential guard units are counted as Army and
		split later through the HomeGuard constructor. */
	for (size_t i = 1; i < m_militaryPower.size(); i++)
		m_militaryPower[i]->reportUnit(eUnit, iChange);
	CvUnitInfo const& kUnit = GC.getInfo(eUnit);
	if (kUnit.getDomainType() != DOMAIN_SEA && kUnit.isMilitaryProduction() &&
		kUnit.getDefaultUnitAIType() != UNITAI_EXPLORE) // exclude Recon
	{
		m_iNonNavalUnits += iChange;
	}
}


void UWAICache::reportWarEnding(TeamTypes eEnemy,
	CLinkList<TradeData> const* pWeReceive,
	CLinkList<TradeData> const* pWeGive)
{
	// Forget sponsorship once a war ends
	m_aiBounty.set(eEnemy, 0);
	m_aeSponsorPerTarget.set(eEnemy, NO_PLAYER);
	// Evaluate reparations
	bool bForceSuccess = false;
	bool bForceFailure = false;
	bool bForceNoFailure = false;
	bool bForceNoSuccess = false;
	if (pWeReceive != NULL)
	{
		int iTechs = 0;
		int iCities = 0;
		// Ignore gold for simplicity (although a large sum could of course be relevant)
		FOR_EACH_TRADE_ITEM(*pWeReceive)
		{
			if (pItem->m_eItemType == TRADE_TECHNOLOGIES)
				iTechs++;
			else if (pItem->m_eItemType == TRADE_CITIES)
				iCities++;
		}
		if(iTechs + iCities > 0)
			bForceNoFailure = true;
		if(iTechs >= 2 || iCities > 0)
			bForceSuccess = true;
	}
	else if (pWeGive != NULL)
	{
		int iTechs = 0;
		int iCities = 0;
		FOR_EACH_TRADE_ITEM(*pWeGive)
		{
			if (pItem->m_eItemType == TRADE_TECHNOLOGIES)
				iTechs++;
			else if (pItem->m_eItemType == TRADE_CITIES)
				iCities++;
		}
		if (iTechs + iCities > 0)
			bForceNoSuccess = true;
		if (iTechs >= 2 || iCities > 0)
			bForceFailure = true;
	}
	// Evaluate war success
	scaled rOurSuccess = GET_TEAM(m_eOwner).AI_getWarSuccess(eEnemy);
	scaled rTheirSuccess = GET_TEAM(eEnemy).AI_getWarSuccess(TEAMID(m_eOwner));
	if (rOurSuccess + rTheirSuccess < GC.getWAR_SUCCESS_CITY_CAPTURING() &&
		!bForceFailure && !bForceSuccess)
	{
		return;
	}
	// Use our era as the baseline for what is significant war success
	scaled const rOurTechEra = GET_PLAYER(m_eOwner).AI_getCurrEraFactor();
	scaled const rSuccessThresh = GC.getWAR_SUCCESS_CITY_CAPTURING() *
			rOurTechEra * fixp(0.7);
	scaled rSuccessRatio = rOurSuccess / std::max(scaled::epsilon(), rTheirSuccess);
	if ((rSuccessRatio > 1 && rOurSuccess < rSuccessThresh) ||
		(rSuccessRatio < 1 && rTheirSuccess < rSuccessThresh))
	{
		rSuccessRatio = 1;
	}
	// Be less critical about our performance if we fought a human
	if (GET_TEAM(eEnemy).isHuman())
		rSuccessRatio *= fixp(4/3.);
	if (GET_PLAYER(m_eOwner).isHuman())
		rSuccessRatio /= fixp(4/3.);
	bool const bChosenWar = GET_TEAM(m_eOwner).AI_isChosenWar(eEnemy);
	int const iDuration = GET_TEAM(m_eOwner).AI_getAtWarCounter(eEnemy);
	scaled const rDurationFactor = fixp(0.365) * scaled(std::max(1, iDuration)).sqrt();
	/*	Don't be easily emboldened by winning a defensive war. Past war score
		is intended to discourage war more than to encourage it. */
	if ((((rSuccessRatio > fixp(1.3) && bChosenWar) || rSuccessRatio > fixp(1.5)) &&
		!bForceNoSuccess) || bForceSuccess)
	{
		m_aiPastWarScore.add(eEnemy, (100 / rDurationFactor).uround());
	}
	// Equal war success not good enough if we started it
	else if (((bChosenWar || rSuccessRatio < fixp(0.7)) &&
		!bForceNoFailure) || bForceFailure)
	{
		m_aiPastWarScore.add(eEnemy, -(100 * rDurationFactor).uround());
	}
}

/*	Note: City ownership changes result in the creation of a new city.
	It's important that the cache keep up with ownership changes
	so that the AI is aware of conquests made throughout a human turn. */
void UWAICache::reportCityCreated(CvCity& kCity)
{
	if (!GET_PLAYER(kCity.getOwner()).isMajorCiv())
		return;
	/*	If c was conquered from the cache owner and the cache owner is about to die,
		then trying to add the city to the cache will lead to problems. */
	if (GET_PLAYER(m_eOwner).getNumCities() <= 0)
		return;
	if (kCity.getTeam() == TEAMID(m_eOwner) ||
		GET_TEAM(m_eOwner).AI_deduceCitySite(kCity))
	{
		add(kCity);
		sortCitiesByAttackPriority();
	}
}


void UWAICache::reportSponsoredWar(CLinkList<TradeData> const& kWeReceive,
	PlayerTypes eSponsor, TeamTypes eTarget)
{
	if (eTarget == NO_TEAM || eSponsor == NO_PLAYER)
	{
		FAssert(false);
		return;
	}
	CvPlayerAI const& kOwner = GET_PLAYER(m_eOwner);
	m_aiBounty.set(eTarget, (kOwner.uwai().
			/*	Need to remember the utility. The deal value may not seem much
				10 turns from now if our economy grows.
				Should perhaps cap the deal val at AI_declareWarTradeVal.
				As it is now, paying more than the AI demands makes it a bit
				more reluctant to end the war. */
			tradeValToUtility(kOwner.AI_dealVal(eSponsor, kWeReceive))).round());
	if (m_aiBounty.get(eTarget) > 0)
		m_aeSponsorPerTarget.set(eTarget, eSponsor);
	else
	{
		m_aiBounty.set(eTarget, 0);
		m_aeSponsorPerTarget.set(eTarget, NO_PLAYER);
	}
}


bool UWAICache::isReadyToCapitulate(TeamTypes eMaster) const
{
	FAssert(GET_TEAM(eMaster).isHuman());
	if (GET_TEAM(m_eOwner).getLeaderID() == m_eOwner)
		return (m_readyToCapitulateTo.count(eMaster) > 0);
	return leaderCache().isReadyToCapitulate(eMaster);
}


void UWAICache::setReadyToCapitulate(TeamTypes eMaster, bool b)
{
	FAssert(GET_TEAM(eMaster).isHuman());
	if (b == isReadyToCapitulate(eMaster))
		return;
	if (GET_TEAM(m_eOwner).getLeaderID() == m_eOwner)
	{
		if (b)
			m_readyToCapitulateTo.insert(eMaster);
		else m_readyToCapitulateTo.erase(eMaster);
	}
	else
	{
		GET_PLAYER(GET_TEAM(m_eOwner).getLeaderID()).uwai().getCache().
				setReadyToCapitulate(eMaster, b);
	}
}


void UWAICache::addTeam(PlayerTypes eOtherLeader)
{
	// Get the team-related data from the other team's leader
	UWAICache& kOther = GET_PLAYER(eOtherLeader).uwai().getCache();
	// Fairly unimportant data ...
	for (TeamIter<MAJOR_CIV> itTeam; itTeam.hasNext(); ++itTeam)
	{
		TeamTypes const eTeam = itTeam->getID();
		m_aiPastWarScore.add(eTeam, kOther.m_aiPastWarScore.get(eTeam));
		if (kOther.m_aeSponsorPerTarget.get(eTeam) != NO_PLAYER)
		{
			if (m_aeSponsorPerTarget.get(eTeam) == NO_PLAYER ||
				m_aiBounty.get(eTeam) < kOther.m_aiBounty.get(eTeam))
			{
				m_aeSponsorPerTarget.set(eTeam, kOther.m_aeSponsorPerTarget.get(eTeam));
				m_aiBounty.set(eTeam, kOther.m_aiBounty.get(eTeam));
			}
		}
	}
}


void UWAICache::onTeamLeaderChanged(PlayerTypes eFormerLeader)
{
	if (eFormerLeader == NO_PLAYER)
		return;
	PlayerTypes const eLeader = GET_TEAM(m_eOwner).getLeaderID();
	if (eLeader == NO_PLAYER || eFormerLeader == eLeader)
		return;
	for (TeamIter<MAJOR_CIV> itTeam; itTeam.hasNext(); ++itTeam)
	{
		TeamTypes const eTeam = itTeam->getID();
		if (GET_TEAM(eTeam).isHuman())
		{
			GET_PLAYER(GET_TEAM(m_eOwner).getLeaderID()).uwai().getCache().
					setReadyToCapitulate(eTeam, GET_PLAYER(eFormerLeader).
					uwai().getCache().m_readyToCapitulateTo.count(eTeam) > 0);
		}
		GET_PLAYER(GET_TEAM(m_eOwner).getLeaderID()).uwai().getCache().
				m_aiWarUtilityIgnoringDistraction.set(eTeam, GET_PLAYER(eFormerLeader).
				uwai().getCache().m_aiWarUtilityIgnoringDistraction.get(eTeam));
	}
	/*	(CanBeHired and ReadyToCapitulate will get updated soon enough.
		Start out as false for the new leader.) */
}


void UWAICache::updateTypicalUnits()
{
	for (size_t i = 0; i < m_militaryPower.size(); i++)
		m_militaryPower[i]->updateTypicalUnit();
}


UWAICache::City::City(PlayerTypes eCacheOwner, CvCity& kCity,
	TeamPathFinders* pPathFinders)
{
	m_pCity = &kCity;
	m_ePlot = kCity.plotNum();
	updateDistance(pPathFinders, eCacheOwner);
	updateAssetScore(eCacheOwner);
	if (!canReach() || TEAMID(eCacheOwner) == kCity.getTeam())
		m_iTargetValue = -1;
	else
	{
		m_iTargetValue = GET_PLAYER(eCacheOwner).AI_targetCityValue(kCity,
				/*	Important that this UWAICity is fully initialized b/c
					we're passing it to AI_targetCityValue */
				false, true, this);
	}
}


void UWAICache::City::cacheCvCity()
{
	m_pCity = NULL;
	CvPlot* pCityPlot = GC.getMap().plotByIndex(m_ePlot);
	if (pCityPlot != NULL)
		m_pCity = pCityPlot->getPlotCity();
	FAssert(m_pCity != NULL); // Must never be NULL past this point
}


void UWAICache::City::write(FDataStreamBase* pStream) const
{
	int iSaveVersion;
	//iSaveVersion = 1; // canDeduce
	//iSaveVersion = 2; // take out can canDeduce again
	//iSaveVersion = 3; // reachBySea removed
	iSaveVersion = 4; // capitalArea added
	pStream->Write(m_ePlot);
	pStream->Write(m_iAssetScore);
	/*	I hadn't thought of a version number in the initial release.
		Fold it into m_iDistance to avoid breaking compatibility. */
	FAssertMsg(m_iDistance >= -1 && m_iDistance < 10000,
			"-2 is OK if loaded from an old savegame version");
	int iDistance = ::range(m_iDistance, -1, 9999);
	// Add 1 b/c distance can be -1
	pStream->Write(iDistance + 1 + 10000 * iSaveVersion);
	pStream->Write(m_iTargetValue);
	pStream->Write(m_bReachByLand);
	pStream->Write(m_bCapitalArea);
}


void UWAICache::City::read(FDataStreamBase* pStream)
{
	pStream->Read((int*)&m_ePlot);
	pStream->Read(&m_iAssetScore);
	int iSaveVersion=-1;
	{
		int iTmp;
		pStream->Read(&iTmp);
		iSaveVersion = iTmp / 10000;
		m_iDistance = (iTmp % 10000) - 1;
	}
	pStream->Read(&m_iTargetValue);
	pStream->Read(&m_bReachByLand);
	if (iSaveVersion >= 4)
		pStream->Read(&m_bCapitalArea);
	else m_bCapitalArea = m_bReachByLand;
	if (iSaveVersion < 3)
	{
		bool bReachBySea; // discard
		pStream->Read(&bReachBySea);
	}
	if (iSaveVersion == 1)
	{
		bool bCanDeduce; // discard
		pStream->Read(&bCanDeduce);
	}
}


scaled UWAICache::City::attackPriority() const
{
	if (m_iDistance < 0)
		return -1;
	else if (isOwnTeamCity())
		return -2; // updateTotalAssetScore relies on own cities having minimal priority
	/*	targetValue is something like 10 to 100, distance 1 to 20 perhaps.
		Add 1000 b/c negative values should be reserved for error conditions. */
	return scaled::max(0, 1000 + getTargetValue() -
			scaled::min(100, fixp(1.5) * scaled(m_iDistance).pow(fixp(1.7))));
}


void UWAICache::City::updateDistance(TeamPathFinders* pPathFinders,
	PlayerTypes eCacheOwner)
{
	PROFILE_FUNC();
	CvCity const& kTargetCity = city();
	/*	For each city of the cache owner, compute a path to the target city
		assuming that war is declared. Derive from that length an estimated travel
		duration based on the typical speed of units and time for loading and
		unloading (iSeaPenalty).
		Set m_iDistance to a weighted average of the pairwise travel durations.
		The average gives the cache owner's cities nearest to the target city
		the greatest weight. Some cities of the cache owner are skipped, both
		for performance reasons (the pathfinding is computationally expensive)
		and b/c I want m_iDistance to reflect typical deployment distances,
		and insignificant cities don't produce (many) units.

		Landlocked civs (0 coastal cities) are treated as unreachable by sea.
		It's not that hard to compute mixed paths to such civs, but CvUnitAI
		isn't capable of carrying out naval assaults on non-coastal cities.

		Unreachable targets are indicated by a distance of -1. */

	if (pPathFinders == NULL) // City of cache owner's team
	{
		m_iDistance = 0;
		CvPlayerAI const& kTargetPlayer = GET_PLAYER(kTargetCity.getOwner());
		CvArea const& kTargetArea = kTargetCity.getArea();
		m_bReachByLand = kTargetPlayer.AI_isPrimaryArea(kTargetArea);
		m_bCapitalArea = (kTargetPlayer.hasCapital() &&
				kTargetPlayer.getCapital()->isArea(kTargetArea));
		return;
	}
	CvPlayerAI const& kCacheOwner = GET_PLAYER(eCacheOwner);
	m_iDistance = -1;
	m_bReachByLand = false;
	m_bCapitalArea = false;
	bool bReachBySea = false;
	bool const bHuman = kCacheOwner.isHuman();
	int const iEra = kCacheOwner.getCurrentEra();
	bool const bDeepSeaTransports = kCacheOwner.uwai().getCache().canTrainDeepSeaCargo();
	bool const bAnyTransports = kCacheOwner.uwai().getCache().canTrainAnyCargo();
	int const iSeaPenalty = (bHuman ? 2 : 4);
	std::vector<int> aiPairwDurations;
	/*	If we find no land path and no sea path from a city c to the target,
		but at least one other city that does have a path to the target, then there
		is most likely also some mixed path from c to the target. */
	int iMixedPaths = 0;
	CvCity const* pCapital = kCacheOwner.getCapital();
	FOR_EACH_CITY(pCity, kCacheOwner)
	{
		// Skip small and isolated cities
		if (!pCity->isCapital())
		{
			if (pCity->getArea().getCitiesPerPlayer(eCacheOwner) <= 1 ||
				pCity->getPopulation() * 3 < pCapital->getPopulation() ||
				pCity->getYieldRate(YIELD_PRODUCTION) < 5 + iEra)
			{
				continue;
			}
		}
		CvPlot const& kStart = pCity->getPlot();
		int iPairwDuration = MAX_INT; // pairwise travel duration
		/*	Search from target to source. TeamStepMetric is symmetrical in that regard.
			Doing it backwards allows intermediate results to be reused. */
		if (pPathFinders->landFinder().generatePath(kTargetCity.getPlot(), kStart))
		{
			iPairwDuration = intdiv::uround(pPathFinders->landFinder().getPathCost(),
					GC.getMOVE_DENOMINATOR());
			if (iPairwDuration == 0) // Make sure 0 is reserved for own cities
				iPairwDuration = 1;
			if (kCacheOwner.AI_isPrimaryArea(pCity->getArea()))
				m_bReachByLand = true;
			if (pCity->isCapital())
				m_bCapitalArea = true;
		}
		if (bAnyTransports &&
			// This ignores cities that can access the ocean only through a canal
			kStart.isCoastalLand(-1) &&
			// Don't bother with a naval path if it's at best a couple turns faster
			iPairwDuration > iSeaPenalty + 2)
		{
			CvPlot const* pTransportDest = kTargetCity.plot();
			if (!kTargetCity.isCoastal(-1))
			{
				/*	(Might still be able to reach the target city directly through
					a canal and a lake -- have only checked whether it's at a
					non-lake water area. A friendly canal near the target is
					quite unlikely however, so I'm not going to check.) */
				pTransportDest = NULL;
				// Can reach cities that are one off the coast
				int iShortestStepDist = MAX_INT;
				FOR_EACH_ADJ_PLOT(kTargetCity.getPlot())
				{
					if (pAdj->isCoastalLand(-1))
					{
						int iStepDist = stepDistance(&kStart, pAdj);
						if (iStepDist < iShortestStepDist)
						{
							pTransportDest = pAdj;
							iShortestStepDist = iStepDist;
						}
					}
				}
			}
			if (pTransportDest != NULL)
			{
				int iPathLength = -1;
				if (bDeepSeaTransports)
				{
					if (pPathFinders->anyWaterFinder().generatePath(*pTransportDest, kStart))
						iPathLength = pPathFinders->anyWaterFinder().getPathCost();
				}
				else
				{
					if (pPathFinders->shallowWaterFinder().generatePath(*pTransportDest, kStart))
						iPathLength = pPathFinders->shallowWaterFinder().getPathCost();
				}
				if (iPathLength > 0)
				{
					int iPathTurns = iSeaPenalty +
							intdiv::uceil(iPathLength,
							GC.getMOVE_DENOMINATOR() *
							kCacheOwner.uwai().getCache().shipSpeed());
					if (iPathTurns < iPairwDuration)
					{
						iPairwDuration = iPathTurns;
						bReachBySea = true;
					}
				}
			}
		}
		if (iPairwDuration < MAX_INT)
		{
			aiPairwDurations.push_back(iPairwDuration);
			// Extra weight for our capital
			if (pCity == pCapital)
				aiPairwDurations.push_back(iPairwDuration);
		}
		/*	No path from pCity to the target, but we assume that there is a path
			from pCity to every other city of the cache owner; so, if we find a path
			from some other city of the cache owner to the target, then we'll assume
			that there is a mixed path (involving land and sea movement) from pCity
			to the target. */
		else iMixedPaths++;
	}
	if ((!m_bReachByLand && !bReachBySea) || aiPairwDurations.empty())
		return; // This may leave m_iDistance at -1
	FAssert(kCacheOwner.getNumCities() > iMixedPaths);
	std::sort(aiPairwDurations.begin(), aiPairwDurations.end());
	FAssert(aiPairwDurations[0] >= 0);
	scaled rWeightedSum;
	{
		scaled rSumOfWeights;
		int iCap = aiPairwDurations[0];
		for (size_t i = 0; i < aiPairwDurations.size(); i++)
		{
			scaled rWeight(2, 3 * ((int)i + 1) - 1);
			rSumOfWeights += rWeight;
			int iPairwDuration = std::min(aiPairwDurations[i], iCap);
			// Allow distances to increase by at most 10 turns per iteration
			iCap = iPairwDuration + 10;
			rWeightedSum += iPairwDuration * rWeight;
		}
		rWeightedSum /= rSumOfWeights; // Normalization
	}
	/*	Hard to estimate the mixed paths. Their lengths certainly depend on
		the lengths of the other paths ... */
	m_iDistance = std::min(
			scaled(getUWAI().maxLandDist() + getUWAI().maxSeaDist(), 2),
			(rWeightedSum +
			scaled(4 * iMixedPaths, iMixedPaths + (int)aiPairwDurations.size())
			)).uround();
}


void UWAICache::City::updateAssetScore(PlayerTypes eCacheOwner)
{
	/*	Scale: Same as CvPlayerAI::AI_cityWonderVal, i.e. approx. 50% GPT.
		Would rather use 100% GPT, but war evaluation can't easily be
		adjusted to that. */
	m_iAssetScore = (GET_PLAYER(eCacheOwner).AI_assetVal(city().AI(), true) / 2).round();
}
