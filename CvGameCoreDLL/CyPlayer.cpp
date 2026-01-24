//
// Python wrapper class for CvPlayer 
//

#include "CvGameCoreDLL.h"
#include "CyPlayer.h"
#include "CyUnit.h"
#include "CyCity.h"
#include "CyArea.h"
#include "CyPlot.h"
#include "CvPlayerAI.h"
//#include "CvEnums.h"
#include "CvCity.h"
#include "CvMap.h"
#include "CvPlot.h"
#include "CySelectionGroup.h"
#include "CvDLLPythonIFaceBase.h"
#include "CvGlobals.h"

CyPlayer::CyPlayer() : m_pPlayer(NULL)
{
}

CyPlayer::CyPlayer(CvPlayer* pPlayer) : m_pPlayer(pPlayer)
{
}

int CyPlayer::startingPlotRange()
{
	return m_pPlayer ? m_pPlayer->startingPlotRange() : -1;
}

bool CyPlayer::startingPlotWithinRange(CyPlot *pPlot, int /*PlayerTypes*/ ePlayer, int iRange, int iPass)
{
	if (m_pPlayer && pPlot != NULL && !pPlot->isNone())
	{
		CvPlot *pcvPlot = pPlot->getPlot();
		if (pPlot)
		{
			return m_pPlayer->startingPlotWithinRange(pcvPlot, (PlayerTypes)ePlayer, iRange, iPass);
		}
	}
	return NULL;
}

CyPlot* CyPlayer::findStartingPlot(bool bRandomize) 
{
	return m_pPlayer ? new CyPlot(m_pPlayer->findStartingPlot(bRandomize)) : NULL;
}

CyCity* CyPlayer::initCity(int x, int y) 
{
	return m_pPlayer ? new CyCity(m_pPlayer->initCity(x, y, true, true)) : NULL;
}

void CyPlayer::acquireCity(CyCity* pCity, bool bConquest, bool bTrade)
{
	if (m_pPlayer)
		m_pPlayer->acquireCity(pCity->getCity(), bConquest, bTrade, true);
}

void CyPlayer::killCities()
{
	if (m_pPlayer)
		m_pPlayer->killCities();
}

std::wstring CyPlayer::getNewCityName()
{
	return m_pPlayer ? m_pPlayer->getNewCityName() : std::wstring();
}

CyUnit* CyPlayer::initUnit(int /*UnitTypes*/ iIndex, int iX, int iY, UnitAITypes eUnitAI, DirectionTypes eFacingDirection)
{
	return m_pPlayer ? new CyUnit(m_pPlayer->initUnit((UnitTypes) iIndex, iX, iY, eUnitAI, eFacingDirection)) : NULL;
}

void CyPlayer::disbandUnit(bool bAnnounce)
{
	return m_pPlayer ? m_pPlayer->disbandUnit(bAnnounce) : NULL;
}

void CyPlayer::killUnits()
{
	if (m_pPlayer)
		m_pPlayer->killUnits();
}

bool CyPlayer::hasTrait(int /*TraitTypes*/ iIndex)
{
	return m_pPlayer ? m_pPlayer->hasTrait((TraitTypes) iIndex) : false;
}

bool CyPlayer::isHuman()
{
	return m_pPlayer ? m_pPlayer->isHuman() : false;
}

bool CyPlayer::isBarbarian()
{
	return m_pPlayer ? m_pPlayer->isBarbarian() : false;
}

std::wstring CyPlayer::getName()
{
	return m_pPlayer ? m_pPlayer->getName() : std::wstring();
}

std::wstring CyPlayer::getNameForm(int iForm)
{
	return m_pPlayer ? m_pPlayer->getName((uint)iForm) : std::wstring();
}

std::wstring CyPlayer::getNameKey()
{
	return m_pPlayer ? m_pPlayer->getNameKey() : std::wstring();
}

std::wstring CyPlayer::getCivilizationDescription(int iForm)
{
	return m_pPlayer ? m_pPlayer->getCivilizationDescription((uint)iForm) : std::wstring();
}

std::wstring CyPlayer::getCivilizationDescriptionKey()
{
	return m_pPlayer ? m_pPlayer->getCivilizationDescriptionKey() : std::wstring();
}

std::wstring CyPlayer::getCivilizationShortDescription(int iForm)
{
	return m_pPlayer ? m_pPlayer->getCivilizationShortDescription((uint)iForm) : std::wstring();
}

std::wstring CyPlayer::getCivilizationShortDescriptionKey()
{
	return m_pPlayer ? m_pPlayer->getCivilizationShortDescriptionKey() : std::wstring();
}

std::wstring CyPlayer::getCivilizationAdjective(int iForm)
{
	return m_pPlayer ? m_pPlayer->getCivilizationAdjective((uint)iForm) : std::wstring();
}

std::wstring CyPlayer::getCivilizationAdjectiveKey( )
{
	return m_pPlayer ? m_pPlayer->getCivilizationAdjectiveKey() : std::wstring();
}

std::wstring CyPlayer::getFlagDecal( )
{
	return m_pPlayer ? m_pPlayer->getFlagDecal() : std::wstring();
}

bool CyPlayer::isWhiteFlag()
{
	return m_pPlayer ? m_pPlayer->isWhiteFlag() : false;
}

std::wstring CyPlayer::getStateReligionName(int iForm)
{
	return m_pPlayer ? m_pPlayer->getStateReligionName((int)iForm) : std::wstring();
}

std::wstring CyPlayer::getStateReligionKey( )
{
	return m_pPlayer ? m_pPlayer->getStateReligionKey() : std::wstring();
}

std::wstring CyPlayer::getBestAttackUnitName(int iForm)
{
	return m_pPlayer ? m_pPlayer->getBestAttackUnitName((uint)iForm) : std::wstring();
}

std::wstring CyPlayer::getWorstEnemyName()
{
	return m_pPlayer ? m_pPlayer->getWorstEnemyName() : std::wstring();
}

std::wstring CyPlayer::getBestAttackUnitKey()
{
	return m_pPlayer ? m_pPlayer->getBestAttackUnitKey() : std::wstring();
}

int /*ArtStyleTypes*/ CyPlayer::getArtStyleType()
{
	return m_pPlayer ? (int) m_pPlayer->getArtStyleType() : -1;
}

std::string CyPlayer::getUnitButton(int eUnit)
{
	return m_pPlayer ? m_pPlayer->getUnitButton((UnitTypes)eUnit) : "";
}

int CyPlayer::findBestFoundValue( )
{
	return m_pPlayer ? m_pPlayer->findBestFoundValue() : -1;
}

int CyPlayer::countReligionSpreadUnits(CyArea* pArea, int /*ReligionTypes*/ eReligion)
{
	return m_pPlayer ? m_pPlayer->countReligionSpreadUnits(pArea->getArea(), (ReligionTypes) eReligion) : -1;
}

int CyPlayer::countNumCoastalCities()
{
	return m_pPlayer ? m_pPlayer->countNumCoastalCities() : -1;
}

int CyPlayer::countNumCoastalCitiesByArea(CyArea* pArea)
{
	return m_pPlayer ? m_pPlayer->countNumCoastalCitiesByArea(pArea->getArea()) : -1;
}

int CyPlayer::countTotalCulture()
{
	return m_pPlayer ? m_pPlayer->countTotalCulture() : -1;
}

int CyPlayer::countOwnedBonuses(int /*BonusTypes*/ eBonus)
{
	return m_pPlayer ? m_pPlayer->countOwnedBonuses((BonusTypes)eBonus) : NO_BONUS;
}

int CyPlayer::countUnimprovedBonuses(CyArea* pArea, CyPlot* pFromPlot)
{
	return m_pPlayer ? m_pPlayer->countUnimprovedBonuses(pArea->getArea(), pFromPlot->getPlot()) : -1;
}

int CyPlayer::countCityFeatures(int /*FeatureTypes*/ eFeature)
{
	return m_pPlayer ? m_pPlayer->countCityFeatures((FeatureTypes) eFeature) : -1;
}

int CyPlayer::countNumBuildings(int /*BuildingTypes*/ eBuilding)
{
	return m_pPlayer ? m_pPlayer->countNumBuildings((BuildingTypes) eBuilding) : -1;
}

int CyPlayer::countPotentialForeignTradeCities(CyArea* pIgnoreArea)
{
	return m_pPlayer ? m_pPlayer->countPotentialForeignTradeCities(pIgnoreArea->getArea()) : -1;
}

int CyPlayer::countPotentialForeignTradeCitiesConnected()
{
	return m_pPlayer ? m_pPlayer->countPotentialForeignTradeCitiesConnected() : -1;
}

int CyPlayer::countNumCitiesConnectedToCapital()
{
	return m_pPlayer ? m_pPlayer->countNumCitiesConnectedToCapital() : -1;
}

bool CyPlayer::canContact(int /*PlayerTypes*/ ePlayer)
{
	return m_pPlayer ? m_pPlayer->canContact((PlayerTypes)ePlayer) : false;
}

void CyPlayer::contact(int /*PlayerTypes*/ ePlayer)
{
	if (m_pPlayer)
		m_pPlayer->contact((PlayerTypes)ePlayer);
}

bool CyPlayer::canTradeWith(int /*PlayerTypes*/ eWhoTo)
{
	return m_pPlayer ? m_pPlayer->canTradeWith((PlayerTypes)eWhoTo) : false;
}

bool CyPlayer::canTradeItem(int /*PlayerTypes*/ eWhoTo, TradeData item, bool bTestDenial)
{
	return m_pPlayer ? m_pPlayer->canTradeItem((PlayerTypes)eWhoTo, item, bTestDenial) : false;
}

DenialTypes CyPlayer::getTradeDenial(int /*PlayerTypes*/ eWhoTo, TradeData item)
{
	return m_pPlayer ? m_pPlayer->getTradeDenial((PlayerTypes)eWhoTo, item) : NO_DENIAL;
}

bool CyPlayer::canTradeNetworkWith(int /*PlayerTypes*/ iPlayer)
{
	return m_pPlayer ? m_pPlayer->canTradeNetworkWith((PlayerTypes)iPlayer) : false;
}

int CyPlayer::getNumAvailableBonuses(int /*BonusTypes*/ eBonus)
{
	return m_pPlayer ? m_pPlayer->getNumAvailableBonuses((BonusTypes)eBonus) : NO_BONUS;
}

int CyPlayer::getNumTradeableBonuses(int /*BonusTypes*/ eBonus)
{
	return m_pPlayer ? m_pPlayer->getNumTradeableBonuses((BonusTypes)eBonus) : NO_BONUS;
}

int CyPlayer::getNumTradeBonusImports(int /*PlayerTypes*/ ePlayer)
{
	return m_pPlayer ? m_pPlayer->getNumTradeBonusImports((PlayerTypes) ePlayer) : -1;
}

bool CyPlayer::hasBonus(int /*BonusTypes*/ eBonus)
{
	return m_pPlayer ? m_pPlayer->hasBonus((BonusTypes)eBonus) : NO_BONUS;
}

bool CyPlayer::canStopTradingWithTeam(int /*TeamTypes*/ eTeam)
{
	return m_pPlayer ? m_pPlayer->canStopTradingWithTeam((TeamTypes) eTeam) : false;
}

void CyPlayer::stopTradingWithTeam(int /*TeamTypes*/ eTeam)
{
	if (m_pPlayer)
		m_pPlayer->stopTradingWithTeam((TeamTypes) eTeam);
}

void CyPlayer::killAllDeals()
{
	if (m_pPlayer)
		m_pPlayer->killAllDeals();
}

bool CyPlayer::isTurnActive()
{
	return m_pPlayer ? m_pPlayer->isTurnActive() : false;
}

void CyPlayer::findNewCapital()
{
	if (m_pPlayer)
		m_pPlayer->findNewCapital();
}

int CyPlayer::getNumGovernmentCenters()
{
	return m_pPlayer ? m_pPlayer->getNumGovernmentCenters() : -1;
}

bool CyPlayer::canRaze(CyCity* pCity)
{
	return m_pPlayer ? m_pPlayer->canRaze(pCity->getCity()) : false;
}

void CyPlayer::raze(CyCity* pCity)
{
	if (m_pPlayer)
		m_pPlayer->raze(pCity->getCity());
}

void CyPlayer::disband(CyCity* pCity)
{
	if (m_pPlayer)
		m_pPlayer->disband(pCity->getCity());
}

bool CyPlayer::canReceiveGoody(CyPlot* pPlot, int /*GoodyTypes*/ iIndex, CyUnit* pUnit)
{
	return m_pPlayer ? m_pPlayer->canReceiveGoody(pPlot->getPlot(), (GoodyTypes) iIndex, pUnit->getUnit()) : false;
}

void CyPlayer::receiveGoody(CyPlot* pPlot, int /*GoodyTypes*/ iIndex, CyUnit* pUnit)
{
	if (m_pPlayer)
		m_pPlayer->receiveGoody(pPlot->getPlot(), (GoodyTypes) iIndex, pUnit->getUnit());
}

void CyPlayer::doGoody(CyPlot* pPlot, CyUnit* pUnit)
{
	if (m_pPlayer)
		m_pPlayer->doGoody(pPlot->getPlot(), pUnit->getUnit());
}

bool CyPlayer::canFound(int iX, int iY)
{
	return m_pPlayer ? m_pPlayer->canFound(iX, iY) : false;
}

void CyPlayer::found(int x, int y) 
{
	if (m_pPlayer)
		m_pPlayer->found(x,y);
}

bool CyPlayer::canTrain(int /*UnitTypes*/ eUnit, bool bContinue, bool bTestVisible)
{
	return m_pPlayer ? m_pPlayer->canTrain((UnitTypes)eUnit, bContinue, bTestVisible) : false;
}

bool CyPlayer::canConstruct(int /*BuildingTypes*/eBuilding, bool bContinue, bool bTestVisible, bool bIgnoreCost)
{
	return m_pPlayer ? m_pPlayer->canConstruct((BuildingTypes)eBuilding, bContinue, bTestVisible, bIgnoreCost) : false;
}

bool CyPlayer::canCreate(int /*ProjectTypes*/ eProject, bool bContinue, bool bTestVisible)
{
	return m_pPlayer ? m_pPlayer->canCreate((ProjectTypes)eProject, bContinue, bTestVisible) : false;
}

bool CyPlayer::canMaintain(int /*ProcessTypes*/ eProcess, bool bContinue)
{
	return m_pPlayer ? m_pPlayer->canMaintain((ProcessTypes)eProcess, bContinue) : false;
}

bool CyPlayer::isProductionMaxedUnitClass(int /*UnitClassTypes*/ eUnitClass)
{
	return m_pPlayer ? m_pPlayer->isProductionMaxedUnitClass((UnitClassTypes) eUnitClass) : false;
}

bool CyPlayer::isProductionMaxedBuildingClass(int /*BuildingClassTypes*/ eBuildingClass, bool bAcquireCity)
{
	return m_pPlayer ? m_pPlayer->isProductionMaxedBuildingClass((BuildingClassTypes) eBuildingClass, bAcquireCity) : false;
}

bool CyPlayer::isProductionMaxedProject(int /*ProjectTypes*/ eProject)
{
	return m_pPlayer ? m_pPlayer->isProductionMaxedProject((ProjectTypes) eProject) : false;
}

int CyPlayer::getUnitProductionNeeded(int /*UnitTypes*/ iIndex)
{
	return m_pPlayer ? m_pPlayer->getProductionNeeded((UnitTypes) iIndex) : -1;
}

int CyPlayer::getBuildingProductionNeeded(int /*BuildingTypes*/ iIndex)
{
	return m_pPlayer ? m_pPlayer->getProductionNeeded((BuildingTypes) iIndex) : -1;
}

int CyPlayer::getProjectProductionNeeded(int /*ProjectTypes*/ iIndex)
{
	return m_pPlayer ? m_pPlayer->getProductionNeeded((ProjectTypes)iIndex) : -1;
}

int CyPlayer::getBuildingClassPrereqBuilding(int /*BuildingTypes*/ eBuilding, int /*BuildingClassTypes*/ ePrereqBuildingClass, int iExtra)
{
	return m_pPlayer ? m_pPlayer->getBuildingClassPrereqBuilding((BuildingTypes) eBuilding, (BuildingClassTypes) ePrereqBuildingClass, iExtra) : -1;
}

void CyPlayer::removeBuildingClass(int /*BuildingClassTypes*/ eBuildingClass)
{
	if (m_pPlayer)
		m_pPlayer->removeBuildingClass((BuildingClassTypes)eBuildingClass);
}

bool CyPlayer::canBuild(CyPlot* pPlot, int /*BuildTypes*/ eBuild, bool bTestEra, bool bTestVisible)
{
	return m_pPlayer ? m_pPlayer->canBuild(pPlot->getPlot(), (BuildTypes)eBuild, bTestEra, bTestVisible) : false;
}

int /*RouteTypes*/ CyPlayer::getBestRoute(CyPlot* pPlot) const
{
	return m_pPlayer ? (int) m_pPlayer->getBestRoute(NULL != pPlot ? pPlot->getPlot() : NULL) : -1;
}

int CyPlayer::getImprovementUpgradeRate() const
{
	return m_pPlayer ? m_pPlayer->getImprovementUpgradeRate() : -1;
}

int CyPlayer::calculateTotalYield(int /*YieldTypes*/ eYield)
{
	return m_pPlayer ? m_pPlayer->calculateTotalYield((YieldTypes)eYield) : -1;
}

int CyPlayer::calculateTotalExports(int /*YieldTypes*/ eYield)
{
	return m_pPlayer ? m_pPlayer->calculateTotalExports((YieldTypes)eYield) : -1;
}

int CyPlayer::calculateTotalImports(int /*YieldTypes*/ eYield)
{
	return m_pPlayer ? m_pPlayer->calculateTotalImports((YieldTypes)eYield) : -1;
}

int CyPlayer::calculateTotalCityHappiness()
{
	return m_pPlayer ? m_pPlayer->calculateTotalCityHappiness() : -1;
}

int CyPlayer::calculateTotalCityUnhappiness()
{
	return m_pPlayer ? m_pPlayer->calculateTotalCityUnhappiness() : -1;
}

int CyPlayer::calculateTotalCityHealthiness()
{
	return m_pPlayer ? m_pPlayer->calculateTotalCityHealthiness() : -1;
}

int CyPlayer::calculateTotalCityUnhealthiness()
{
	return m_pPlayer ? m_pPlayer->calculateTotalCityUnhealthiness() : -1;
}

int CyPlayer::calculateUnitCost()
{
	return m_pPlayer ? m_pPlayer->calculateUnitCost() : -1;
}

int CyPlayer::calculateUnitSupply()
{
	return m_pPlayer ? m_pPlayer->calculateUnitSupply() : -1;
}

int CyPlayer::calculatePreInflatedCosts()
{
	return m_pPlayer ? m_pPlayer->calculatePreInflatedCosts() : -1;
}

int CyPlayer::calculateInflationRate()
{
	return m_pPlayer ? m_pPlayer->calculateInflationRate() : -1;
}

int CyPlayer::calculateInflatedCosts()
{
	return m_pPlayer ? m_pPlayer->calculateInflatedCosts() : -1;
}

int CyPlayer::calculateGoldRate()
{
	return m_pPlayer ? m_pPlayer->calculateGoldRate() : -1;
}

int CyPlayer::calculateTotalCommerce()
{
	return m_pPlayer ? m_pPlayer->calculateTotalCommerce() : -1;
}

int CyPlayer::calculateResearchRate(int /*TechTypes*/ eTech)
{
	return m_pPlayer ? m_pPlayer->calculateResearchRate((TechTypes)eTech) : -1;
}

int CyPlayer::calculateResearchModifier(int /*TechTypes*/ eTech)
{
	return m_pPlayer ? m_pPlayer->calculateResearchModifier((TechTypes)eTech) : -1;
}

int CyPlayer::calculateBaseNetResearch()
{
	return m_pPlayer ? m_pPlayer->calculateBaseNetResearch() : -1;
}

bool CyPlayer::isResearch()
{
	return m_pPlayer ? m_pPlayer->isResearch() : false;
}

bool CyPlayer::canEverResearch(int /*TechTypes*/ eTech)
{
	return m_pPlayer ? m_pPlayer->canEverResearch((TechTypes)eTech) : false;
}

bool CyPlayer::canResearch(int /*TechTypes*/ eTech, bool bTrade)
{
	return m_pPlayer ? m_pPlayer->canResearch((TechTypes)eTech, bTrade) : false;
}

int /* TechTypes */ CyPlayer::getCurrentResearch()
{
	return m_pPlayer ? (int) m_pPlayer->getCurrentResearch() : (int) NO_TECH;
}

bool CyPlayer::isCurrentResearchRepeat()
{
	return m_pPlayer ? m_pPlayer->isCurrentResearchRepeat() : false;
}

bool CyPlayer::isNoResearchAvailable()
{
	return m_pPlayer ? m_pPlayer->isNoResearchAvailable() : false;
}

int CyPlayer::getResearchTurnsLeft(int /*TechTypes*/ eTech, bool bOverflow)
{
	return m_pPlayer ? m_pPlayer->getResearchTurnsLeft((TechTypes)eTech, bOverflow) : -1;
}

bool CyPlayer::isCivic(int /*CivicTypes*/ eCivic)
{
	return m_pPlayer ? m_pPlayer->isCivic((CivicTypes)eCivic) : false;
}

bool CyPlayer::canDoCivics(int /*CivicTypes*/ eCivic)
{
	return m_pPlayer ? m_pPlayer->canDoCivics((CivicTypes)eCivic) : false;
}

bool CyPlayer::canRevolution(int /*CivicTypes**/ paeNewCivics)
{
	return m_pPlayer ? m_pPlayer->canRevolution((CivicTypes*)paeNewCivics) : false;
}

void CyPlayer::revolution(int /*CivicTypes**/ paeNewCivics, bool bForce)
{
	if (m_pPlayer)
		m_pPlayer->revolution((CivicTypes*)paeNewCivics, bForce);
}

int CyPlayer::getCivicPercentAnger(int /*CivicTypes*/ eCivic)
{
	return m_pPlayer ? m_pPlayer->getCivicPercentAnger((CivicTypes) eCivic) : -1;
}

bool CyPlayer::canDoReligion(int /*ReligionTypes*/ eReligion)
{
	return m_pPlayer ? m_pPlayer->canDoReligion((ReligionTypes) eReligion) : false;
}

bool CyPlayer::canChangeReligion()
{
	return m_pPlayer ? m_pPlayer->canChangeReligion() : false;
}

bool CyPlayer::canConvert(int /*ReligionTypes*/ iIndex)
{
	return m_pPlayer ? m_pPlayer->canConvert((ReligionTypes)iIndex) : false;
}

void CyPlayer::convert(int /*ReligionTypes*/ iIndex)
{
	if (m_pPlayer)
		m_pPlayer->convert((ReligionTypes)iIndex);
}

bool CyPlayer::hasHolyCity(int /*ReligionTypes*/ eReligion)
{
	return m_pPlayer ? m_pPlayer->hasHolyCity((ReligionTypes)eReligion) : false;
}

int CyPlayer::countHolyCities()
{
	return m_pPlayer ? m_pPlayer->countHolyCities() : -1;
}

void CyPlayer::foundReligion(int /*ReligionTypes*/ iIndex, int /*ReligionTypes*/ iSlotReligion, bool bAward)
{
	if (m_pPlayer)
		m_pPlayer->foundReligion((ReligionTypes)iIndex, (ReligionTypes)iSlotReligion, bAward);
}

bool CyPlayer::hasHeadquarters(int /*CorporationTypes*/ eCorporation)
{
	return m_pPlayer ? m_pPlayer->hasHeadquarters((CorporationTypes)eCorporation) : false;
}

int CyPlayer::countHeadquarters()
{
	return m_pPlayer ? m_pPlayer->countHeadquarters() : -1;
}

int CyPlayer::countCorporations(int /*CorporationTypes*/ eCorporation)
{
	return m_pPlayer ? m_pPlayer->countCorporations((CorporationTypes)eCorporation) : -1;
}

void CyPlayer::foundCorporation(int /*CorporationTypes*/ iIndex)
{
	if (m_pPlayer)
		m_pPlayer->foundCorporation((CorporationTypes)iIndex);
}

int CyPlayer::getCivicAnarchyLength(boost::python::list& /*CivicTypes**/ paeNewCivics)
{
	int* pCivics = NULL;
	gDLL->getPythonIFace()->putSeqInArray(paeNewCivics.ptr() /*src*/, &pCivics /*dst*/);

	int iRet = m_pPlayer ? m_pPlayer->getCivicAnarchyLength((CivicTypes*)pCivics) : -1;
	delete [] pCivics;
	return iRet;
}

int CyPlayer::getReligionAnarchyLength()
{
	return m_pPlayer ? m_pPlayer->getReligionAnarchyLength() : -1;
}

int CyPlayer::unitsRequiredForGoldenAge()
{
	return m_pPlayer ? m_pPlayer->unitsRequiredForGoldenAge() : -1;
}

int CyPlayer::unitsGoldenAgeCapable()
{
	return m_pPlayer ? m_pPlayer->unitsGoldenAgeCapable() : -1;
}

int CyPlayer::unitsGoldenAgeReady()
{
	return m_pPlayer ? m_pPlayer->unitsGoldenAgeReady() : -1;
}

int CyPlayer::greatPeopleThreshold(bool bMilitary)
{
	return m_pPlayer ? m_pPlayer->greatPeopleThreshold(bMilitary) : -1;
}

int CyPlayer::specialistYield(int /*SpecialistTypes*/ eSpecialist, int /*YieldTypes*/ eCommerce)

{
	return m_pPlayer ? m_pPlayer->specialistYield((SpecialistTypes)eSpecialist, (YieldTypes)eCommerce) : -1;
}

int CyPlayer::specialistCommerce(int /*SpecialistTypes*/ eSpecialist, int /*CommerceTypes*/ eCommerce)

{
	return m_pPlayer ? m_pPlayer->specialistCommerce((SpecialistTypes)eSpecialist, (CommerceTypes)eCommerce) : -1;
}

CyPlot* CyPlayer::getStartingPlot()
{
	if (!m_pPlayer)
	{
		return NULL;
	}

	return new CyPlot(m_pPlayer->getStartingPlot());
}

void CyPlayer::setStartingPlot(CyPlot* pPlot, bool bUpdateStartDist)
{
	if (!m_pPlayer)
	{
		return;
	}

	m_pPlayer->setStartingPlot(NULL != pPlot ? pPlot->getPlot() : NULL, bUpdateStartDist);
}

int CyPlayer::getTotalPopulation()
{
	return m_pPlayer ? m_pPlayer->getTotalPopulation() : -1;
}

int CyPlayer::getAveragePopulation()
{
	return m_pPlayer ? m_pPlayer->getAveragePopulation() : -1;
}

long CyPlayer::getRealPopulation()
{
	return m_pPlayer ? m_pPlayer->getRealPopulation() : -1;
}

int CyPlayer::getTotalLand()
{
	return m_pPlayer ? m_pPlayer->getTotalLand() : -1;
}

int CyPlayer::getTotalLandScored()
{
	return m_pPlayer ? m_pPlayer->getTotalLandScored() : -1;
}

int CyPlayer::getGold() 
{
	return m_pPlayer ? m_pPlayer->getGold() : -1;
}

void CyPlayer::setGold(int iNewValue)
{
	if (m_pPlayer)
		m_pPlayer->setGold(iNewValue);
}

void CyPlayer::changeGold(int iChange)
{
	if (m_pPlayer)
		m_pPlayer->changeGold(iChange);
}

int CyPlayer::getGoldPerTurn()
{
	return m_pPlayer ? m_pPlayer->getGoldPerTurn() : -1;
}

int CyPlayer::getAdvancedStartPoints() 
{
	return m_pPlayer ? m_pPlayer->getAdvancedStartPoints() : -1;
}

void CyPlayer::setAdvancedStartPoints(int iNewValue)
{
	if (m_pPlayer)
		m_pPlayer->setAdvancedStartPoints(iNewValue);
}

void CyPlayer::changeAdvancedStartPoints(int iChange)
{
	if (m_pPlayer)
		m_pPlayer->changeAdvancedStartPoints(iChange);
}

int CyPlayer::getAdvancedStartUnitCost(int /*UnitTypes*/ eUnit, bool bAdd, CyPlot* pPlot)
{
	return m_pPlayer ? m_pPlayer->getAdvancedStartUnitCost((UnitTypes) eUnit, bAdd, NULL != pPlot ? pPlot->getPlot() : NULL) : -1;
}

int CyPlayer::getAdvancedStartCityCost(bool bAdd, CyPlot* pPlot)
{
	return m_pPlayer ? m_pPlayer->getAdvancedStartCityCost(bAdd, NULL != pPlot ? pPlot->getPlot() : NULL) : -1;
}

int CyPlayer::getAdvancedStartPopCost(bool bAdd, CyCity* pCity)
{
	return m_pPlayer ? m_pPlayer->getAdvancedStartPopCost(bAdd, pCity->getCity()) : -1;
}

int CyPlayer::getAdvancedStartCultureCost(bool bAdd, CyCity* pCity)
{
	return m_pPlayer ? m_pPlayer->getAdvancedStartCultureCost(bAdd, pCity->getCity()) : -1;
}

int CyPlayer::getAdvancedStartBuildingCost(int /*BuildingTypes*/ eBuilding, bool bAdd, CyCity* pCity)
{
	return m_pPlayer ? m_pPlayer->getAdvancedStartBuildingCost((BuildingTypes) eBuilding, bAdd, pCity->getCity()) : -1;
}

int CyPlayer::getAdvancedStartImprovementCost(int /*ImprovementTypes*/ eImprovement, bool bAdd, CyPlot* pPlot)
{
	return m_pPlayer ? m_pPlayer->getAdvancedStartImprovementCost((ImprovementTypes) eImprovement, bAdd, NULL != pPlot ? pPlot->getPlot() : NULL) : -1;
}

int CyPlayer::getAdvancedStartRouteCost(int /*RouteTypes*/ eRoute, bool bAdd, CyPlot* pPlot)
{
	return m_pPlayer ? m_pPlayer->getAdvancedStartRouteCost((RouteTypes) eRoute, bAdd, NULL != pPlot ? pPlot->getPlot() : NULL) : -1;
}

int CyPlayer::getAdvancedStartTechCost(int /*TechTypes*/ eTech, bool bAdd)
{
	return m_pPlayer ? m_pPlayer->getAdvancedStartTechCost((TechTypes) eTech, bAdd) : -1;
}

int CyPlayer::getAdvancedStartVisibilityCost(bool bAdd, CyPlot* pPlot)
{
	return m_pPlayer ? m_pPlayer->getAdvancedStartVisibilityCost(bAdd, NULL != pPlot ? pPlot->getPlot() : NULL) : -1;
}

int CyPlayer::getEspionageSpending(int /*TeamTypes*/ eIndex)
{
	return m_pPlayer ? m_pPlayer->getEspionageSpending((TeamTypes) eIndex) : -1;
}

bool CyPlayer::canDoEspionageMission(int /*EspionageMissionTypes*/ eMission, int /*PlayerTypes*/ eTargetPlayer, CyPlot* pPlot, int iExtraData)
{
	return m_pPlayer ? m_pPlayer->canDoEspionageMission((EspionageMissionTypes) eMission, (PlayerTypes) eTargetPlayer, NULL != pPlot ? pPlot->getPlot() : NULL, iExtraData, NULL) : false;
}

int CyPlayer::getEspionageMissionCost(int /*EspionageMissionTypes*/ eMission, int /*PlayerTypes*/ eTargetPlayer, CyPlot* pPlot, int iExtraData)
{
	return m_pPlayer ? m_pPlayer->getEspionageMissionCost((EspionageMissionTypes) eMission, (PlayerTypes) eTargetPlayer, NULL != pPlot ? pPlot->getPlot() : NULL, iExtraData) : -1;
}

void CyPlayer::doEspionageMission(int /*EspionageMissionTypes*/ eMission, int /*PlayerTypes*/ eTargetPlayer, CyPlot* pPlot, int iExtraData, CyUnit* pUnit)
{
	if (m_pPlayer)
		m_pPlayer->doEspionageMission((EspionageMissionTypes) eMission, (PlayerTypes) eTargetPlayer, NULL != pPlot ? pPlot->getPlot() : NULL, iExtraData, pUnit->getUnit());
}

int CyPlayer::getEspionageSpendingWeightAgainstTeam(int /*TeamTypes*/ eIndex)
{
	return m_pPlayer ? m_pPlayer->getEspionageSpendingWeightAgainstTeam((TeamTypes) eIndex) : -1;
}

void CyPlayer::setEspionageSpendingWeightAgainstTeam(int /*TeamTypes*/ eIndex, int iValue)
{
	if (m_pPlayer)
		m_pPlayer->setEspionageSpendingWeightAgainstTeam((TeamTypes) eIndex, iValue);
}

void CyPlayer::changeEspionageSpendingWeightAgainstTeam(int /*TeamTypes*/ eIndex, int iChange)
{
	if (m_pPlayer)
		m_pPlayer->changeEspionageSpendingWeightAgainstTeam((TeamTypes) eIndex, iChange);
}

int CyPlayer::getGoldenAgeTurns()
{
	return m_pPlayer ? m_pPlayer->getGoldenAgeTurns() : -1;
}

int CyPlayer::getGoldenAgeLength()
{
	return m_pPlayer ? m_pPlayer->getGoldenAgeLength() : -1;
}

bool CyPlayer::isGoldenAge()
{
	return m_pPlayer ? m_pPlayer->isGoldenAge() : false;
}

void CyPlayer::changeGoldenAgeTurns(int iChange)
{
	if (m_pPlayer)
		m_pPlayer->changeGoldenAgeTurns(iChange);
}

int CyPlayer::getNumUnitGoldenAges()
{
	return m_pPlayer ? m_pPlayer->getNumUnitGoldenAges() : -1;
}

void CyPlayer::changeNumUnitGoldenAges(int iChange)
{
	if (m_pPlayer)
		m_pPlayer->changeNumUnitGoldenAges(iChange);
}

int CyPlayer::getAnarchyTurns()
{
	return m_pPlayer ? m_pPlayer->getAnarchyTurns() : -1;
}

bool CyPlayer::isAnarchy()
{
	return m_pPlayer ? m_pPlayer->isAnarchy() : false;
}

void CyPlayer::changeAnarchyTurns(int iChange)
{
	if (m_pPlayer)
		m_pPlayer->changeAnarchyTurns(iChange);
}

int CyPlayer::getStrikeTurns()
{
	return m_pPlayer ? m_pPlayer->getStrikeTurns() : -1;
}

int CyPlayer::getMaxAnarchyTurns()
{
	return m_pPlayer ? m_pPlayer->getMaxAnarchyTurns() : -1;
}

int CyPlayer::getAnarchyModifier()
{
	return m_pPlayer ? m_pPlayer->getAnarchyModifier() : -1;
}

int CyPlayer::getGoldenAgeModifier()
{
	return m_pPlayer ? m_pPlayer->getGoldenAgeModifier() : -1;
}

int CyPlayer::getHurryModifier()
{
	return m_pPlayer ? m_pPlayer->getHurryModifier() : -1;
}

void CyPlayer::createGreatPeople(int eGreatPersonUnit, bool bIncrementThreshold, bool bIncrementExperience, int iX, int iY)
{
	if (m_pPlayer)
	{
		m_pPlayer->createGreatPeople((UnitTypes)eGreatPersonUnit, bIncrementThreshold, bIncrementExperience, iX, iY);
	}

}

int CyPlayer::getGreatPeopleCreated()
{
	return m_pPlayer ? m_pPlayer->getGreatPeopleCreated() : -1;
}

int CyPlayer::getGreatGeneralsCreated()
{
	return m_pPlayer ? m_pPlayer->getGreatGeneralsCreated() : -1;
}

int CyPlayer::getGreatPeopleThresholdModifier()
{
	return m_pPlayer ? m_pPlayer->getGreatPeopleThresholdModifier() : -1;
}

int CyPlayer::getGreatGeneralsThresholdModifier()
{
	return m_pPlayer ? m_pPlayer->getGreatGeneralsThresholdModifier() : -1;
}

int CyPlayer::getGreatPeopleRateModifier()
{
	return m_pPlayer ? m_pPlayer->getGreatPeopleRateModifier() : -1;
}

int CyPlayer::getGreatGeneralRateModifier()
{
	return m_pPlayer ? m_pPlayer->getGreatGeneralRateModifier() : -1;
}

int CyPlayer::getDomesticGreatGeneralRateModifier()
{
	return m_pPlayer ? m_pPlayer->getDomesticGreatGeneralRateModifier() : -1;
}

int CyPlayer::getStateReligionGreatPeopleRateModifier()
{
	return m_pPlayer ? m_pPlayer->getStateReligionGreatPeopleRateModifier() : -1;
}

int CyPlayer::getMaxGlobalBuildingProductionModifier()
{
	return m_pPlayer ? m_pPlayer->getMaxGlobalBuildingProductionModifier() : -1;
}

int CyPlayer::getMaxTeamBuildingProductionModifier()
{
	return m_pPlayer ? m_pPlayer->getMaxTeamBuildingProductionModifier() : -1;
}

int CyPlayer::getMaxPlayerBuildingProductionModifier()
{
	return m_pPlayer ? m_pPlayer->getMaxPlayerBuildingProductionModifier() : -1;
}

int CyPlayer::getFreeExperience()
{
	return m_pPlayer ? m_pPlayer->getFreeExperience() : -1;
}

int CyPlayer::getFeatureProductionModifier()
{
	return m_pPlayer ? m_pPlayer->getFeatureProductionModifier() : -1;
}

int CyPlayer::getWorkerSpeedModifier()
{
	return m_pPlayer ? m_pPlayer->getWorkerSpeedModifier() : -1;
}

int CyPlayer::getImprovementUpgradeRateModifier()
{
	return m_pPlayer ? m_pPlayer->getImprovementUpgradeRateModifier() : -1;
}

int CyPlayer::getMilitaryProductionModifier()
{
	return m_pPlayer ? m_pPlayer->getMilitaryProductionModifier() : -1;
}

int CyPlayer::getSpaceProductionModifier()
{
	return m_pPlayer ? m_pPlayer->getSpaceProductionModifier() : -1;
}

int CyPlayer::getCityDefenseModifier()
{
	return m_pPlayer ? m_pPlayer->getCityDefenseModifier() : -1;
}

int CyPlayer::getNumNukeUnits()
{
	return m_pPlayer ? m_pPlayer->getNumNukeUnits() : -1;
}

int CyPlayer::getNumOutsideUnits()
{
	return m_pPlayer ? m_pPlayer->getNumOutsideUnits() : -1;
}

int CyPlayer::getBaseFreeUnits()
{
	return m_pPlayer ? m_pPlayer->getBaseFreeUnits() : -1;
}

int CyPlayer::getBaseFreeMilitaryUnits()
{
	return m_pPlayer ? m_pPlayer->getBaseFreeMilitaryUnits() : -1;
}

int CyPlayer::getFreeUnitsPopulationPercent()
{
	return m_pPlayer ? m_pPlayer->getFreeUnitsPopulationPercent() : -1;
}

int CyPlayer::getFreeMilitaryUnitsPopulationPercent()
{
	return m_pPlayer ? m_pPlayer->getFreeMilitaryUnitsPopulationPercent() : -1;
}

int CyPlayer::getGoldPerUnit()
{
	return m_pPlayer ? m_pPlayer->getGoldPerUnit() : -1;
}

int CyPlayer::getGoldPerMilitaryUnit()
{
	return m_pPlayer ? m_pPlayer->getGoldPerMilitaryUnit() : -1;
}

int CyPlayer::getExtraUnitCost()
{
	return m_pPlayer ? m_pPlayer->getExtraUnitCost() : -1;
}

int CyPlayer::getNumMilitaryUnits()
{
	return m_pPlayer ? m_pPlayer->getNumMilitaryUnits() : -1;
}

int CyPlayer::getHappyPerMilitaryUnit()
{
	return m_pPlayer ? m_pPlayer->getHappyPerMilitaryUnit() : -1;
}

bool CyPlayer::isMilitaryFoodProduction()
{
	return m_pPlayer ? m_pPlayer->isMilitaryFoodProduction() : false;
}

int CyPlayer::getHighestUnitLevel()
{
	return m_pPlayer ? m_pPlayer->getHighestUnitLevel() : -1;
}

int CyPlayer::getConscriptCount()
{
	return m_pPlayer ? m_pPlayer->getConscriptCount() : -1;
}

void CyPlayer::setConscriptCount(int iNewValue)
{
	if (m_pPlayer)
		m_pPlayer->setConscriptCount(iNewValue);
}

void CyPlayer::changeConscriptCount(int iChange)
{
	if (m_pPlayer)
		m_pPlayer->changeConscriptCount(iChange);
}

int CyPlayer::getMaxConscript()
{
	return m_pPlayer ? m_pPlayer->getMaxConscript() : -1;
}

int CyPlayer::getOverflowResearch()
{
	return m_pPlayer ? m_pPlayer->getOverflowResearch() : 0;
}

bool CyPlayer::isNoUnhealthyPopulation()
{
	return m_pPlayer ? m_pPlayer->isNoUnhealthyPopulation() : false;
}

bool CyPlayer::getExpInBorderModifier()
{
	return m_pPlayer ? m_pPlayer->getExpInBorderModifier() : false;
}

bool CyPlayer::isBuildingOnlyHealthy()
{
	return m_pPlayer ? m_pPlayer->isBuildingOnlyHealthy() : false;
}

int CyPlayer::getDistanceMaintenanceModifier()
{
	return m_pPlayer ? m_pPlayer->getDistanceMaintenanceModifier() : -1;
}

int CyPlayer::getNumCitiesMaintenanceModifier()
{
	return m_pPlayer ? m_pPlayer->getNumCitiesMaintenanceModifier() : -1;
}

int CyPlayer::getCorporationMaintenanceModifier()
{
	return m_pPlayer ? m_pPlayer->getCorporationMaintenanceModifier() : -1;
}

int CyPlayer::getTotalMaintenance()
{
	return m_pPlayer ? m_pPlayer->getTotalMaintenance() : -1;
}

int CyPlayer::getUpkeepModifier()
{
	return m_pPlayer ? m_pPlayer->getUpkeepModifier() : -1;
}

int CyPlayer::getLevelExperienceModifier() const
{
	return m_pPlayer ? m_pPlayer->getLevelExperienceModifier() : -1;
}

int CyPlayer::getExtraHealth()
{
	return m_pPlayer ? m_pPlayer->getExtraHealth() : -1;
}

int CyPlayer::getBuildingGoodHealth()
{
	return m_pPlayer ? m_pPlayer->getBuildingGoodHealth() : -1;
}

int CyPlayer::getBuildingBadHealth()
{
	return m_pPlayer ? m_pPlayer->getBuildingBadHealth() : -1;
}

int CyPlayer::getExtraHappiness()
{
	return m_pPlayer ? m_pPlayer->getExtraHappiness() : -1;
}

void CyPlayer::changeExtraHappiness(int iChange)
{
	if (m_pPlayer)
		m_pPlayer->changeExtraHappiness(iChange);
}

int CyPlayer::getBuildingHappiness()
{
	return m_pPlayer ? m_pPlayer->getBuildingHappiness() : -1;
}

int CyPlayer::getLargestCityHappiness()
{
	return m_pPlayer ? m_pPlayer->getLargestCityHappiness() : -1;
}

int CyPlayer::getWarWearinessPercentAnger()
{
	return m_pPlayer ? m_pPlayer->getWarWearinessPercentAnger() : -1;
}

int CyPlayer::getWarWearinessModifier()
{
	return m_pPlayer ? m_pPlayer->getWarWearinessModifier() : -1;
}

int CyPlayer::getFreeSpecialist()
{
	return m_pPlayer ? m_pPlayer->getFreeSpecialist() : -1;
}

bool CyPlayer::isNoForeignTrade()
{
	return m_pPlayer ? m_pPlayer->isNoForeignTrade() : false;
}
bool CyPlayer::isNoCorporations()
{
	return m_pPlayer ? m_pPlayer->isNoCorporations() : false;
}
bool CyPlayer::isNoForeignCorporations()
{
	return m_pPlayer ? m_pPlayer->isNoForeignCorporations() : false;
}

int CyPlayer::getCoastalTradeRoutes()
{
	return m_pPlayer ? m_pPlayer->getCoastalTradeRoutes() : -1;
}

void CyPlayer::changeCoastalTradeRoutes(int iChange)
{
	if (m_pPlayer)
		m_pPlayer->changeCoastalTradeRoutes(iChange);
}

int CyPlayer::getTradeRoutes()
{
	return m_pPlayer ? m_pPlayer->getTradeRoutes() : -1;
}

int CyPlayer::getConversionTimer()
{
	return m_pPlayer ? m_pPlayer->getConversionTimer() : -1;
}

int CyPlayer::getRevolutionTimer()
{
	return m_pPlayer ? m_pPlayer->getRevolutionTimer() : -1;
}

bool CyPlayer::isStateReligion()
{
	return m_pPlayer ? m_pPlayer->isStateReligion() : false;
}

bool CyPlayer::isNoNonStateReligionSpread()
{
	return m_pPlayer ? m_pPlayer->isNoNonStateReligionSpread() : false;
}

int CyPlayer::getStateReligionHappiness()
{
	return m_pPlayer ? m_pPlayer->getStateReligionHappiness() : -1;
}

int CyPlayer::getNonStateReligionHappiness()
{
	return m_pPlayer ? m_pPlayer->getNonStateReligionHappiness() : -1;
}

int CyPlayer::getStateReligionUnitProductionModifier()
{
	return m_pPlayer ? m_pPlayer->getStateReligionUnitProductionModifier() : -1;
}

void CyPlayer::changeStateReligionUnitProductionModifier(int iChange)
{
	if (m_pPlayer)
		m_pPlayer->changeStateReligionUnitProductionModifier(iChange);
}

int CyPlayer::getStateReligionBuildingProductionModifier()
{
	return m_pPlayer ? m_pPlayer->getStateReligionBuildingProductionModifier() : -1;
}

void CyPlayer::changeStateReligionBuildingProductionModifier(int iChange)
{
	if (m_pPlayer)
		m_pPlayer->changeStateReligionBuildingProductionModifier(iChange);
}

int CyPlayer::getStateReligionFreeExperience()
{
	return m_pPlayer ? m_pPlayer->getStateReligionFreeExperience() : -1;
}

CyCity* CyPlayer::getCapitalCity()
{
	return m_pPlayer ? new CyCity(m_pPlayer->getCapitalCity()) : NULL;
}

int CyPlayer::getCitiesLost()
{
	return m_pPlayer ? m_pPlayer->getCitiesLost() : -1;
}

int CyPlayer::getWinsVsBarbs()
{
	return m_pPlayer ? m_pPlayer->getWinsVsBarbs() : -1;
}

int CyPlayer::getAssets()
{
	return m_pPlayer ? m_pPlayer->getAssets() : -1;
}

void CyPlayer::changeAssets(int iChange)
{
	if (m_pPlayer)
		m_pPlayer->changeAssets(iChange);
}

int CyPlayer::getPower()
{
	return m_pPlayer ? m_pPlayer->getPower() : -1;
}

int CyPlayer::getPopScore()
{
	return m_pPlayer ? m_pPlayer->getPopScore() : -1;
}

int CyPlayer::getLandScore()
{
	return m_pPlayer ? m_pPlayer->getLandScore() : -1;
}

int CyPlayer::getWondersScore()
{
	return m_pPlayer ? m_pPlayer->getWondersScore() : -1;
}

int CyPlayer::getTechScore()
{
	return m_pPlayer ? m_pPlayer->getTechScore() : -1;
}

int CyPlayer::getTotalTimePlayed()
{
	return m_pPlayer ? m_pPlayer->getTotalTimePlayed() : -1;
}

bool CyPlayer::isMinorCiv()
{
	return m_pPlayer ? m_pPlayer->isMinorCiv() : false;
}

bool CyPlayer::isAlive() 
{
	return m_pPlayer ? m_pPlayer->isAlive() : false;
}

bool CyPlayer::isEverAlive() 
{
	return m_pPlayer ? m_pPlayer->isEverAlive() : false;
}

bool CyPlayer::isExtendedGame() 
{
	return m_pPlayer ? m_pPlayer->isExtendedGame() : false;
}

bool CyPlayer::isFoundedFirstCity()
{
	return m_pPlayer ? m_pPlayer->isFoundedFirstCity() : false;
}

bool CyPlayer::isStrike()
{
	return m_pPlayer ? m_pPlayer->isStrike() : false;
}

int CyPlayer::getID()
{
	return m_pPlayer ? m_pPlayer->getID() : -1;
}

int /* HandicapTypes */ CyPlayer::getHandicapType()
{
	return m_pPlayer ? (int) m_pPlayer->getHandicapType() : -1;
}

int /* CivilizationTypes */  CyPlayer::getCivilizationType() 
{
	return m_pPlayer ? (int) m_pPlayer->getCivilizationType() : NO_CIVILIZATION;
}

int /*LeaderHeadTypes*/ CyPlayer::getLeaderType()
{
	return m_pPlayer ? (int) m_pPlayer->getLeaderType() : -1;
}

int /*LeaderHeadTypes*/ CyPlayer::getPersonalityType()
{
	return m_pPlayer ? (int) m_pPlayer->getPersonalityType() : -1;
}

void CyPlayer::setPersonalityType(int /*LeaderHeadTypes*/ eNewValue)
{
	if (m_pPlayer)
		m_pPlayer->setPersonalityType((LeaderHeadTypes) eNewValue);
}

int /*ErasTypes*/ CyPlayer::getCurrentEra()
{
	return m_pPlayer ? (int) m_pPlayer->getCurrentEra() : NO_ERA;
}

void CyPlayer::setCurrentEra(int /*EraTypes*/ iNewValue)
{
	if (m_pPlayer)
		m_pPlayer->setCurrentEra((EraTypes) iNewValue);
}

int /*ReligonTypes*/ CyPlayer::getStateReligion()
{
	return m_pPlayer ? (int) m_pPlayer->getStateReligion() : NO_RELIGION;
}

void CyPlayer::setLastStateReligion(int /*ReligionTypes*/ iNewReligion)
{
	if (m_pPlayer)
		m_pPlayer->setLastStateReligion((ReligionTypes) iNewReligion);
}

int CyPlayer::getTeam()
{
	return m_pPlayer ? m_pPlayer->getTeam() : -1;
}

int /*PlayerColorTypes*/ CyPlayer::getPlayerColor()
{
	return m_pPlayer ? (int) m_pPlayer->getPlayerColor() : NO_COLOR;
}

int CyPlayer::getPlayerTextColorR()
{
	return m_pPlayer ? m_pPlayer->getPlayerTextColorR() : -1;
}

int CyPlayer::getPlayerTextColorG()
{
	return m_pPlayer ? m_pPlayer->getPlayerTextColorG() : -1;
}

int CyPlayer::getPlayerTextColorB()
{
	return m_pPlayer ? m_pPlayer->getPlayerTextColorB() : -1;
}

int CyPlayer::getPlayerTextColorA()
{
	return m_pPlayer ? m_pPlayer->getPlayerTextColorA() : -1;
}

int CyPlayer::getSeaPlotYield(YieldTypes eIndex)
{
	return m_pPlayer ? (int) m_pPlayer->getSeaPlotYield(eIndex) : NO_YIELD;
}

int CyPlayer::getYieldRateModifier(YieldTypes eIndex)
{
	return m_pPlayer ? m_pPlayer->getYieldRateModifier(eIndex) : NO_YIELD;
}

int CyPlayer::getCapitalYieldRateModifier(YieldTypes eIndex)
{
	return m_pPlayer ? m_pPlayer->getCapitalYieldRateModifier(eIndex) : NO_YIELD;
}

int CyPlayer::getExtraYieldThreshold(YieldTypes eIndex)
{
	return m_pPlayer ? m_pPlayer->getExtraYieldThreshold(eIndex) : NO_YIELD;
}

int CyPlayer::getTradeYieldModifier(YieldTypes eIndex)
{
	return m_pPlayer ? m_pPlayer->getTradeYieldModifier(eIndex) : NO_YIELD;
}

int CyPlayer::getFreeCityCommerce(CommerceTypes eIndex)
{
	return m_pPlayer ? m_pPlayer->getFreeCityCommerce(eIndex) : NO_COMMERCE;
}

int CyPlayer::getCommercePercent(int /*CommerceTypes*/ eIndex)
{
	return m_pPlayer ? m_pPlayer->getCommercePercent((CommerceTypes)eIndex) : NO_COMMERCE;
}

void CyPlayer::setCommercePercent(CommerceTypes eIndex, int iNewValue)
{
	if (m_pPlayer)
		m_pPlayer->setCommercePercent(eIndex, iNewValue);
}

void CyPlayer::changeCommercePercent(CommerceTypes eIndex, int iChange)
{
	if (m_pPlayer)
		m_pPlayer->changeCommercePercent(eIndex, iChange);
}

int CyPlayer::getCommerceRate(CommerceTypes eIndex)
{
	return m_pPlayer ? m_pPlayer->getCommerceRate(eIndex) : -1;
}

int CyPlayer::getCommerceRateModifier(CommerceTypes eIndex)
{
	return m_pPlayer ? m_pPlayer->getCommerceRateModifier(eIndex) : NO_COMMERCE;
}

int CyPlayer::getCapitalCommerceRateModifier(CommerceTypes eIndex)
{
	return m_pPlayer ? m_pPlayer->getCapitalCommerceRateModifier(eIndex) : NO_COMMERCE;
}

int CyPlayer::getStateReligionBuildingCommerce(CommerceTypes eIndex)
{
	return m_pPlayer ? m_pPlayer->getStateReligionBuildingCommerce(eIndex) : NO_COMMERCE;
}

int CyPlayer::getSpecialistExtraCommerce(CommerceTypes eIndex)
{
	return m_pPlayer ? m_pPlayer->getSpecialistExtraCommerce(eIndex) : NO_COMMERCE;
}

bool CyPlayer::isCommerceFlexible(int /*CommerceTypes*/ eIndex)
{
	return m_pPlayer ? m_pPlayer->isCommerceFlexible((CommerceTypes)eIndex) : false;
}

int CyPlayer::getGoldPerTurnByPlayer(int /*PlayerTypes*/ eIndex)
{
	return m_pPlayer ? m_pPlayer->getGoldPerTurnByPlayer((PlayerTypes) eIndex) : -1;
}

bool CyPlayer::isFeatAccomplished(int /*FeatTypes*/ eIndex)	
{
	return m_pPlayer ? m_pPlayer->isFeatAccomplished((FeatTypes)eIndex) : false;
}

void CyPlayer::setFeatAccomplished(int /*FeatTypes*/ eIndex, bool bNewValue)
{
	if (m_pPlayer)
		m_pPlayer->setFeatAccomplished((FeatTypes)eIndex, bNewValue);
}

bool CyPlayer::isOption(int /*PlayerOptionTypes*/ eIndex)	
{
	return m_pPlayer ? m_pPlayer->isOption((PlayerOptionTypes)eIndex) : false;
}

void CyPlayer::setOption(int /*PlayerOptionTypes*/ eIndex, bool bNewValue)
{
	if (m_pPlayer)
		m_pPlayer->setOption((PlayerOptionTypes)eIndex, bNewValue);
}

bool CyPlayer::isLoyalMember(int /*VoteSourceTypes*/ eIndex)	
{
	return m_pPlayer ? m_pPlayer->isLoyalMember((VoteSourceTypes)eIndex) : false;
}

void CyPlayer::setLoyalMember(int /*VoteSourceTypes*/ eIndex, bool bNewValue)
{
	if (m_pPlayer)
		m_pPlayer->setLoyalMember((VoteSourceTypes)eIndex, bNewValue);
}

int CyPlayer::getVotes(int /*VoteTypes*/ eVote, int /*VoteSourceTypes*/ eVoteSource)
{
	return m_pPlayer ? m_pPlayer->getVotes((VoteTypes)eVote, (VoteSourceTypes)eVoteSource) : -1;
}

bool CyPlayer::isFullMember(int /*VoteSourceTypes*/ eVoteSource) const
{
	return m_pPlayer ? m_pPlayer->isFullMember((VoteSourceTypes)eVoteSource) : false;
}

bool CyPlayer::isVotingMember(int /*VoteSourceTypes*/ eVoteSource) const
{
	return m_pPlayer ? m_pPlayer->isVotingMember((VoteSourceTypes)eVoteSource) : false;
}

bool CyPlayer::isPlayable()
{
	return m_pPlayer ? m_pPlayer->isPlayable() : false;
}

void CyPlayer::setPlayable(bool bNewValue)
{
	if (m_pPlayer)
		m_pPlayer->setPlayable(bNewValue);
}

int CyPlayer::getBonusExport(int /*BonusTypes*/ iIndex)
{
	return m_pPlayer ? m_pPlayer->getBonusExport((BonusTypes)iIndex) : -1;
}

int CyPlayer::getBonusImport(int /*BonusTypes*/ iIndex)
{
	return m_pPlayer ? m_pPlayer->getBonusImport((BonusTypes)iIndex) : -1;
}

int CyPlayer::getImprovementCount(int /*ImprovementTypes*/ iIndex)
{
	return m_pPlayer ? m_pPlayer->getImprovementCount((ImprovementTypes)iIndex) : -1;
}

bool CyPlayer::isBuildingFree(int /*BuildingTypes*/ iIndex)
{
	return m_pPlayer ? m_pPlayer->isBuildingFree((BuildingTypes)iIndex) : false;
}

int CyPlayer::getExtraBuildingHappiness(int /*BuildingTypes*/ iIndex)
{
	return m_pPlayer ? m_pPlayer->getExtraBuildingHappiness((BuildingTypes)iIndex) : -1;
}

int CyPlayer::getExtraBuildingHealth(int /*BuildingTypes*/ iIndex)
{
	return m_pPlayer ? m_pPlayer->getExtraBuildingHealth((BuildingTypes)iIndex) : -1;
}

int CyPlayer::getFeatureHappiness(int /*FeatureTypes*/ iIndex)
{
	return m_pPlayer ? m_pPlayer->getFeatureHappiness((FeatureTypes)iIndex) : -1;
}

int CyPlayer::getUnitClassCount(int /*UnitClassTypes*/ eIndex)
{
	return m_pPlayer ? m_pPlayer->getUnitClassCount((UnitClassTypes) eIndex) : NO_UNITCLASS;
}

bool CyPlayer::isUnitClassMaxedOut(int /*UnitClassTypes*/ eIndex, int iExtra)
{
	return m_pPlayer ? m_pPlayer->isUnitClassMaxedOut((UnitClassTypes) eIndex, iExtra) : false;
}

int CyPlayer::getUnitClassMaking(int /*UnitClassTypes*/ eIndex)
{
	return m_pPlayer ? m_pPlayer->getUnitClassMaking((UnitClassTypes) eIndex) : -1;
}

int CyPlayer::getUnitClassCountPlusMaking(int /*UnitClassTypes*/ eIndex)
{
	return m_pPlayer ? m_pPlayer->getUnitClassCountPlusMaking((UnitClassTypes) eIndex) : -1;
}

int CyPlayer::getBuildingClassCount(int /*BuildingClassTypes*/ iIndex)
{
	return m_pPlayer ? m_pPlayer->getBuildingClassCount((BuildingClassTypes)iIndex) : -1;
}

bool CyPlayer::isBuildingClassMaxedOut(int /*BuildingClassTypes*/ iIndex, int iExtra)
{
	return m_pPlayer ? m_pPlayer->isBuildingClassMaxedOut((BuildingClassTypes)iIndex, iExtra) : false;
}

int CyPlayer::getBuildingClassMaking(int /*BuildingClassTypes*/ iIndex)
{
	return m_pPlayer ? m_pPlayer->getBuildingClassMaking((BuildingClassTypes)iIndex) : -1;
}

int CyPlayer::getBuildingClassCountPlusMaking(int /*BuildingClassTypes*/ iIndex)
{
	return m_pPlayer ? m_pPlayer->getBuildingClassCountPlusMaking((BuildingClassTypes)iIndex) : -1;
}

int CyPlayer::getHurryCount(int /*HurryTypes*/ eIndex)
{
	return m_pPlayer ? m_pPlayer->getHurryCount((HurryTypes)eIndex) : (int) NO_HURRY;
}

bool CyPlayer::canHurry(int /*HurryTypes*/ eIndex)
{
	return m_pPlayer ? m_pPlayer->canHurry((HurryTypes)eIndex) : (int) NO_HURRY;
}

int CyPlayer::getSpecialBuildingNotRequiredCount(int /*SpecialBuildingTypes*/ eIndex)
{
	return m_pPlayer ? m_pPlayer->getSpecialBuildingNotRequiredCount((SpecialBuildingTypes)eIndex) : -1;
}

bool CyPlayer::isSpecialBuildingNotRequired(int /*SpecialBuildingTypes*/ eIndex)
{
	return m_pPlayer ? m_pPlayer->isSpecialBuildingNotRequired((SpecialBuildingTypes)eIndex) : -1;
}

bool CyPlayer::isHasCivicOption(int /*CivicOptionTypes*/ eIndex)
{
	return m_pPlayer ? m_pPlayer->isHasCivicOption((CivicOptionTypes) eIndex) : false;
}

bool CyPlayer::isNoCivicUpkeep(int /*CivicOptionTypes*/ iIndex)
{
	return m_pPlayer ? m_pPlayer->isNoCivicUpkeep((CivicOptionTypes)iIndex) : false;
}

int CyPlayer::getHasReligionCount(int /*ReligionTypes*/ iIndex)
{
	return m_pPlayer ? m_pPlayer->getHasReligionCount((ReligionTypes)iIndex) : -1;
}

int CyPlayer::countTotalHasReligion()
{
	return m_pPlayer ? m_pPlayer->countTotalHasReligion() : -1;
}

int CyPlayer::getHasCorporationCount(int /*CorporationTypes*/ iIndex)
{
	return m_pPlayer ? m_pPlayer->getHasCorporationCount((CorporationTypes)iIndex) : -1;
}

int CyPlayer::countTotalHasCorporation()
{
	return m_pPlayer ? m_pPlayer->countTotalHasCorporation() : -1;
}

int CyPlayer::findHighestHasReligionCount()
{
	return m_pPlayer ? m_pPlayer->findHighestHasReligionCount() : -1;
}

int CyPlayer::getUpkeepCount(int /*UpkeepTypes*/ eIndex)
{
	return m_pPlayer ? m_pPlayer->getUpkeepCount((UpkeepTypes) eIndex) : -1;
}

bool CyPlayer::isSpecialistValid(int /*SpecialistTypes*/ iIndex)
{
	return m_pPlayer ? m_pPlayer->isSpecialistValid((SpecialistTypes)iIndex) : false;
}

bool CyPlayer::isResearchingTech(int /*TechTypes*/ iIndex)
{
	return m_pPlayer ? m_pPlayer->isResearchingTech((TechTypes)iIndex) : false;
}

int /* CivicTypes */ CyPlayer::getCivics(int /*CivicOptionTypes*/ iIndex)
{
	return m_pPlayer ? m_pPlayer->getCivics((CivicOptionTypes)iIndex) : -1;
}

int CyPlayer::getSingleCivicUpkeep(int /*CivicTypes*/ eCivic, bool bIgnoreAnarchy)
{
	return m_pPlayer ? m_pPlayer->getSingleCivicUpkeep((CivicTypes) eCivic, bIgnoreAnarchy) : -1;
}

int CyPlayer::getCivicUpkeep(boost::python::list& /*CivicTypes*/ paiCivics, bool bIgnoreAnarchy)
{
	int* pCivics = NULL;
	gDLL->getPythonIFace()->putSeqInArray(paiCivics.ptr() /*src*/, &pCivics /*dst*/);
	int iRet = m_pPlayer ? m_pPlayer->getCivicUpkeep((CivicTypes*)pCivics, bIgnoreAnarchy) : -1;
	delete [] pCivics;
	return iRet;
}

void CyPlayer::setCivics(int /*CivicOptionTypes*/ eIndex, int /*CivicTypes*/ eNewValue)
{
	if (m_pPlayer)
		m_pPlayer->setCivics((CivicOptionTypes) eIndex, (CivicTypes) eNewValue);
}

int CyPlayer::getCombatExperience() const
{
	if (m_pPlayer)
	{
		return m_pPlayer->getCombatExperience();
	}
	return -1;
}

void CyPlayer::changeCombatExperience(int iChange)
{
	if (m_pPlayer)
	{
		m_pPlayer->changeCombatExperience(iChange);
	}
	
}

void CyPlayer::setCombatExperience(int iExperience)
{
	if (m_pPlayer)
	{
		m_pPlayer->setCombatExperience(iExperience);
	}

}

int CyPlayer::getSpecialistExtraYield(int /*SpecialistTypes*/ eIndex1, int /*YieldTypes*/ eIndex2)
{
	return m_pPlayer ? m_pPlayer->getSpecialistExtraYield((SpecialistTypes) eIndex1, (YieldTypes) eIndex2) : -1;
}

int CyPlayer::findPathLength(int /*TechTypes*/ eTech, bool bCost)
{
	return m_pPlayer ? m_pPlayer->findPathLength((TechTypes)eTech, bCost) : -1;
}

int CyPlayer::getQueuePosition( int /* TechTypes */ eTech )
{
	if (m_pPlayer)
	{
		return m_pPlayer->getQueuePosition((TechTypes)eTech);
	}
	return -1;
}

void CyPlayer::clearResearchQueue()
{
	if (m_pPlayer)
		m_pPlayer->clearResearchQueue();
}

bool CyPlayer::pushResearch(int /*TechTypes*/ iIndex, bool bClear)
{
	return m_pPlayer ? m_pPlayer->pushResearch((TechTypes)iIndex, bClear) : false;
}

void CyPlayer::popResearch(int /*TechTypes*/ eTech)
{
	if (m_pPlayer)
		m_pPlayer->popResearch((TechTypes) eTech);
}

int CyPlayer::getLengthResearchQueue()
{
	return m_pPlayer ? m_pPlayer->getLengthResearchQueue() : -1;
}

void CyPlayer::addCityName(std::wstring szName)
{
	if (m_pPlayer)
		m_pPlayer->addCityName(szName);
}

int CyPlayer::getNumCityNames()
{
	return m_pPlayer ? m_pPlayer->getNumCityNames() : -1;
}

std::wstring CyPlayer::getCityName(int iIndex)
{
	return m_pPlayer ? m_pPlayer->getCityName(iIndex) : std::wstring();
}

// returns tuple of (CyCity, iterOut)
python::tuple CyPlayer::firstCity(bool bRev)
{
	int iterIn = 0;
	CvCity* pvObj = m_pPlayer ? m_pPlayer->firstCity(&iterIn, bRev) : NULL;
	CyCity* pyObj = pvObj ? new CyCity(pvObj) : NULL;
	python::tuple tup=python::make_tuple(pyObj, iterIn);
	delete pyObj;
	return tup;
}

// returns tuple of (CyCity, iterOut)
python::tuple CyPlayer::nextCity(int iterIn, bool bRev)
{
	CvCity* pvObj = m_pPlayer ? m_pPlayer->nextCity(&iterIn, bRev) : NULL;
	CyCity* pyObj = pvObj ? new CyCity(pvObj) : NULL;
	python::tuple tup=python::make_tuple(pyObj, iterIn);
	delete pyObj;
	return tup;
}

int CyPlayer::getNumCities()
{
	return m_pPlayer ? m_pPlayer->getNumCities() : -1;
}

CyCity* CyPlayer::getCity(int iID)
{
	return m_pPlayer ? new CyCity(m_pPlayer->getCity(iID)) : NULL;
}

// returns tuple of (CyUnit, iterOut)
python::tuple CyPlayer::firstUnit(bool bRev)
{
	int iterIn = 0;
	CvUnit* pvUnit = m_pPlayer ? m_pPlayer->firstUnit(&iterIn, bRev) : NULL;
	CyUnit* pyUnit = pvUnit ? new CyUnit(pvUnit) : NULL;
	python::tuple tup=python::make_tuple(pyUnit, iterIn);
	delete pyUnit;
	return tup;
}

// returns tuple of (CyUnit, iterOut)
python::tuple CyPlayer::nextUnit(int iterIn, bool bRev)
{
	CvUnit* pvObj = m_pPlayer ? m_pPlayer->nextUnit(&iterIn, bRev) : NULL;
	CyUnit* pyObj = pvObj ? new CyUnit(pvObj) : NULL;
	python::tuple tup=python::make_tuple(pyObj, iterIn);
	delete pyObj;
	return tup;

}

int CyPlayer::getNumUnits()
{
	return m_pPlayer ? m_pPlayer->getNumUnits() : -1;
}

CyUnit* CyPlayer::getUnit(int iID)
{
	return m_pPlayer ? new CyUnit(m_pPlayer->getUnit(iID)) : NULL;
}

// returns tuple of (CySelectionGroup, iterOut)
python::tuple CyPlayer::firstSelectionGroup(bool bRev)
{
	int iterIn = 0;
	CvSelectionGroup* pvObj = m_pPlayer ? m_pPlayer->firstSelectionGroup(&iterIn, bRev) : NULL;
	CySelectionGroup* pyObj = pvObj ? new CySelectionGroup(pvObj) : NULL;
	python::tuple tup=python::make_tuple(pyObj, iterIn);
	delete pyObj;
	return tup;
}

// returns tuple of (CySelectionGroup, iterOut)
python::tuple CyPlayer::nextSelectionGroup(int iterIn, bool bRev)
{
	CvSelectionGroup* pvObj = m_pPlayer ? m_pPlayer->nextSelectionGroup(&iterIn, bRev) : NULL;
	CySelectionGroup* pyObj = pvObj ? new CySelectionGroup(pvObj) : NULL;
	python::tuple tup=python::make_tuple(pyObj, iterIn);
	delete pyObj;
	return tup;
}

int CyPlayer::getNumSelectionGroups()
{
	return m_pPlayer ? m_pPlayer->getNumSelectionGroups() : -1;
}

CySelectionGroup* CyPlayer::getSelectionGroup(int iID)
{
	return m_pPlayer ? new CySelectionGroup(m_pPlayer->getSelectionGroup(iID)) : NULL;
}

void CyPlayer::trigger(/*EventTriggerTypes*/int eEventTrigger)
{
	if (m_pPlayer)
	{
		m_pPlayer->trigger((EventTriggerTypes)eEventTrigger);
	}

}

const EventTriggeredData* CyPlayer::getEventOccured(int /*EventTypes*/ eEvent) const
{
	return m_pPlayer ? m_pPlayer->getEventOccured((EventTypes)eEvent) : NULL;
}

void CyPlayer::resetEventOccured(int /*EventTypes*/ eEvent)
{
	if (m_pPlayer)
	{
		m_pPlayer->resetEventOccured((EventTypes)eEvent);
	}
}

EventTriggeredData* CyPlayer::getEventTriggered(int iID) const
{
	return m_pPlayer ? m_pPlayer->getEventTriggered(iID) : NULL;
}

EventTriggeredData* CyPlayer::initTriggeredData(int /*EventTriggerTypes*/ eEventTrigger, bool bFire, int iCityId, int iPlotX, int iPlotY, int /*PlayerTypes*/ eOtherPlayer, int iOtherPlayerCityId, int /*ReligionTypes*/ eReligion, int /*CorporationTypes*/ eCorporation, int iUnitId, int /*BuildingTypes*/ eBuilding)
{
	return m_pPlayer ? m_pPlayer->initTriggeredData((EventTriggerTypes)eEventTrigger, bFire, iCityId, iPlotX, iPlotY, (PlayerTypes)eOtherPlayer, iOtherPlayerCityId, (ReligionTypes)eReligion, (CorporationTypes)eCorporation, iUnitId, (BuildingTypes)eBuilding) : NULL;
}

int CyPlayer::getEventTriggerWeight(int /*EventTriggerTypes*/ eTrigger)
{
	return m_pPlayer ? m_pPlayer->getEventTriggerWeight((EventTriggerTypes)eTrigger) : NULL;
}

void CyPlayer::AI_updateFoundValues(bool bStartingLoc)
{
	if (m_pPlayer)
		m_pPlayer->AI_updateFoundValues(bStartingLoc);
}

int CyPlayer::AI_foundValue(int iX, int iY, int iMinUnitRange/* = -1*/, bool bStartingLoc/* = false*/)
{
	return m_pPlayer ? m_pPlayer->AI_foundValue(iX, iY, iMinUnitRange, bStartingLoc) : -1;
}

bool CyPlayer::AI_isFinancialTrouble()
{
	return m_pPlayer ? m_pPlayer->AI_isFinancialTrouble() : false;
}

bool CyPlayer::AI_demandRebukedWar(int /*PlayerTypes*/ ePlayer)
{
	return m_pPlayer ? m_pPlayer->AI_demandRebukedWar((PlayerTypes)ePlayer) : false;
}

AttitudeTypes CyPlayer::AI_getAttitude(int /*PlayerTypes*/ ePlayer)
{
	return m_pPlayer ? m_pPlayer->AI_getAttitude((PlayerTypes)ePlayer) : NO_ATTITUDE;
}

int CyPlayer::AI_unitValue(int /*UnitTypes*/ eUnit, int /*UnitAITypes*/ eUnitAI, CyArea* pArea)
{
	return m_pPlayer ? m_pPlayer->AI_unitValue((UnitTypes)eUnit, (UnitAITypes)eUnitAI, pArea->getArea()) : -1;
}

int CyPlayer::AI_civicValue(int /*CivicTypes*/ eCivic)
{
	return m_pPlayer ? m_pPlayer->AI_civicValue((CivicTypes)eCivic) : -1;
}

int CyPlayer::AI_totalUnitAIs(int /*UnitAITypes*/ eUnitAI)
{
	return m_pPlayer ? m_pPlayer->AI_totalUnitAIs((UnitAITypes)eUnitAI) : -1;
}

int CyPlayer::AI_totalAreaUnitAIs(CyArea* pArea, int /*UnitAITypes*/ eUnitAI)
{
	return m_pPlayer ? m_pPlayer->AI_totalAreaUnitAIs(pArea->getArea(), (UnitAITypes)eUnitAI) : -1;
}

int CyPlayer::AI_totalWaterAreaUnitAIs(CyArea* pArea, int /*UnitAITypes*/ eUnitAI)
{
	return m_pPlayer ? m_pPlayer->AI_totalWaterAreaUnitAIs(pArea->getArea(), (UnitAITypes)eUnitAI) : -1;
}

int CyPlayer::AI_getNumAIUnits(int /*UnitAITypes*/ eIndex)
{
	return m_pPlayer ? m_pPlayer->AI_getNumAIUnits((UnitAITypes)eIndex) : NO_UNITAI;
}

int CyPlayer::AI_getAttitudeExtra(int /*PlayerTypes*/ eIndex)
{
	return m_pPlayer ? m_pPlayer->AI_getAttitudeExtra((PlayerTypes)eIndex) : -1;
}

void CyPlayer::AI_setAttitudeExtra(int /*PlayerTypes*/ eIndex, int iNewValue)
{
	if (m_pPlayer)
		m_pPlayer->AI_setAttitudeExtra((PlayerTypes)eIndex, iNewValue);
}

void CyPlayer::AI_changeAttitudeExtra(int /*PlayerTypes*/ eIndex, int iChange)
{
	if (m_pPlayer)
		m_pPlayer->AI_changeAttitudeExtra((PlayerTypes)eIndex, iChange);
}

int CyPlayer::AI_getMemoryCount(int /*PlayerTypes*/ eIndex1, int /*MemoryTypes*/ eIndex2)
{
	return m_pPlayer ? m_pPlayer->AI_getMemoryCount((PlayerTypes)eIndex1, (MemoryTypes)eIndex2) : -1;
}

void CyPlayer::AI_changeMemoryCount(int /*PlayerTypes*/ eIndex1, int /*MemoryTypes*/ eIndex2, int iChange)
{
	if (m_pPlayer)
		m_pPlayer->AI_changeMemoryCount((PlayerTypes)eIndex1, (MemoryTypes)eIndex2, iChange);
}

int CyPlayer::AI_getExtraGoldTarget() const
{
	return m_pPlayer ? m_pPlayer->AI_getExtraGoldTarget() : -1;
}

void CyPlayer::AI_setExtraGoldTarget(int iNewValue)
{
	if (m_pPlayer)
	{
		m_pPlayer->AI_setExtraGoldTarget(iNewValue);
	}
}


int CyPlayer::getScoreHistory(int iTurn) const
{
	return (NULL != m_pPlayer ? m_pPlayer->getScoreHistory(iTurn) : 0);
}

int CyPlayer::getEconomyHistory(int iTurn) const
{
	return (NULL != m_pPlayer ? m_pPlayer->getEconomyHistory(iTurn) : 0);
}

int CyPlayer::getIndustryHistory(int iTurn) const
{
	return (NULL != m_pPlayer ? m_pPlayer->getIndustryHistory(iTurn) : 0);
}

int CyPlayer::getAgricultureHistory(int iTurn) const
{
	return (NULL != m_pPlayer ? m_pPlayer->getAgricultureHistory(iTurn) : 0);
}

int CyPlayer::getPowerHistory(int iTurn) const
{
	return (NULL != m_pPlayer ? m_pPlayer->getPowerHistory(iTurn) : 0);
}

int CyPlayer::getCultureHistory(int iTurn) const
{
	return (NULL != m_pPlayer ? m_pPlayer->getCultureHistory(iTurn) : 0);
}

int CyPlayer::getEspionageHistory(int iTurn) const
{
	return (NULL != m_pPlayer ? m_pPlayer->getEspionageHistory(iTurn) : 0);
}

std::string CyPlayer::getScriptData() const
{
	return m_pPlayer ? m_pPlayer->getScriptData() : "";
}

void CyPlayer::setScriptData(std::string szNewValue)
{
	if (m_pPlayer)
		m_pPlayer->setScriptData(szNewValue);
}

void CyPlayer::chooseTech(int iDiscover, std::wstring szText, bool bFront)
{
	if ( m_pPlayer )
	{
		m_pPlayer->chooseTech(iDiscover, szText.c_str(), bFront);
	}
}

int CyPlayer::AI_maxGoldTrade(int iPlayer)
{
	CvPlayerAI* pPlayer = dynamic_cast<CvPlayerAI*>(m_pPlayer);
	if (pPlayer)
	{
		return (pPlayer->AI_maxGoldTrade((PlayerTypes)iPlayer));
	}
	return 0;
}

int CyPlayer::AI_maxGoldPerTurnTrade(int iPlayer)
{
	CvPlayerAI* pPlayer = dynamic_cast<CvPlayerAI*>(m_pPlayer);
	if (pPlayer)
	{
		return (pPlayer->AI_maxGoldPerTurnTrade((PlayerTypes)iPlayer));
	}
	return 0;
}

bool CyPlayer::splitEmpire(int iAreaId)
{
	if (m_pPlayer)
	{
		return m_pPlayer->splitEmpire(iAreaId);
	}

	return false;
}

bool CyPlayer::canSplitEmpire() const
{
	if (m_pPlayer)
	{
		return m_pPlayer->canSplitEmpire();
	}

	return false;
}

bool CyPlayer::canSplitArea(int iAreaId) const
{
	if (m_pPlayer)
	{
		return m_pPlayer->canSplitArea(iAreaId);
	}

	return false;
}

bool CyPlayer::canHaveTradeRoutesWith(int iPlayer)
{
	return m_pPlayer ? m_pPlayer->canHaveTradeRoutesWith((PlayerTypes)iPlayer) : false;
}

void  CyPlayer::forcePeace(int iPlayer)
{
	if (m_pPlayer)
		m_pPlayer->forcePeace((PlayerTypes)iPlayer);
}
