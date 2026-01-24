//
// Python wrapper class for CvTeam 
// updated 6-5
//
#include "CvGameCoreDLL.h"
#include "CyTeam.h"
#include "CyArea.h"
#include "CvTeam.h"

CyTeam::CyTeam() : m_pTeam(NULL)
{
}

CyTeam::CyTeam(CvTeam* pTeam) : m_pTeam(pTeam)
{
}

void CyTeam::addTeam(int /*TeamTypes*/ eTeam)
{
	if (m_pTeam)
		m_pTeam->addTeam((TeamTypes)eTeam);
}

bool CyTeam::canChangeWarPeace(int /*TeamTypes*/ eTeam)
{
	return m_pTeam ? m_pTeam->canChangeWarPeace((TeamTypes)eTeam) : false;
}

bool CyTeam::canDeclareWar(int /*TeamTypes*/ eTeam)
{
	return m_pTeam ? m_pTeam->canDeclareWar((TeamTypes)eTeam) : false;
}

void CyTeam::declareWar(int /*TeamTypes*/ eTeam, bool bNewDiplo, int /*WarPlanTypes*/ eWarPlan)
{
	if (m_pTeam)
		m_pTeam->declareWar((TeamTypes)eTeam, bNewDiplo, (WarPlanTypes)eWarPlan);
}

void CyTeam::makePeace(int /*TeamTypes*/ eTeam)
{
	if (m_pTeam)
		m_pTeam->makePeace((TeamTypes)eTeam);
}

bool CyTeam::canContact(int /*TeamTypes*/ eTeam)
{
	return m_pTeam ? m_pTeam->canContact((TeamTypes)eTeam) : false;
}

void CyTeam::meet(int /*TeamTypes*/ eTeam, bool bNewDiplo)
{
	if (m_pTeam)
		m_pTeam->meet((TeamTypes)eTeam, bNewDiplo);
}

void CyTeam::signOpenBorders(int /*TeamTypes*/ eTeam)
{
	if (m_pTeam)
		m_pTeam->signOpenBorders((TeamTypes)eTeam);
}

void CyTeam::signDefensivePact(int /*TeamTypes*/ eTeam)
{
	if (m_pTeam)
		m_pTeam->signDefensivePact((TeamTypes)eTeam);
}

int CyTeam::getAssets()
{
	return m_pTeam ? m_pTeam->getAssets() : -1;
}

int CyTeam::getPower(bool bIncludeVassals)
{
	return m_pTeam ? m_pTeam->getPower(bIncludeVassals) : -1;
}

int CyTeam::getDefensivePower()
{
	return m_pTeam ? m_pTeam->getDefensivePower() : -1;
}

int CyTeam::getNumNukeUnits()
{
	return m_pTeam ? m_pTeam->getNumNukeUnits() : -1;
}

int CyTeam::getAtWarCount(bool bIgnoreMinors)
{
	return m_pTeam ? m_pTeam->getAtWarCount(bIgnoreMinors) : -1;
}

int CyTeam::getWarPlanCount(int /*WarPlanTypes*/ eWarPlan, bool bIgnoreMinors)
{
	return m_pTeam ? m_pTeam->getWarPlanCount((WarPlanTypes) eWarPlan, bIgnoreMinors) : -1;
}

int CyTeam::getAnyWarPlanCount(bool bIgnoreMinors)
{
	return m_pTeam ? m_pTeam->getAnyWarPlanCount(bIgnoreMinors) : -1;
}

int CyTeam::getChosenWarCount(bool bIgnoreMinors)
{
	return m_pTeam ? m_pTeam->getChosenWarCount(bIgnoreMinors) : -1;
}

int CyTeam::getHasMetCivCount(bool bIgnoreMinors)
{
	return m_pTeam ? m_pTeam->getHasMetCivCount(bIgnoreMinors) : -1;
}

bool CyTeam::hasMetHuman()
{
	return m_pTeam ? m_pTeam->hasMetHuman() : false;
}

int CyTeam::getDefensivePactCount()
{
	return m_pTeam ? m_pTeam->getDefensivePactCount() : -1;
}

bool CyTeam::isAVassal() const
{
	return m_pTeam ? m_pTeam->isAVassal() : false;
}

int CyTeam::getUnitClassMaking(int /*UnitClassTypes*/ eUnitClass)
{
	return m_pTeam ? m_pTeam->getUnitClassMaking((UnitClassTypes)eUnitClass) : -1;
}

int CyTeam::getUnitClassCountPlusMaking(int /*UnitClassTypes*/ eUnitClass)
{
	return m_pTeam ? m_pTeam->getUnitClassCountPlusMaking((UnitClassTypes)eUnitClass) : -1;
}

int CyTeam::getBuildingClassMaking(int /*BuildingClassTypes*/ eBuildingClass)
{
	return m_pTeam ? m_pTeam->getBuildingClassMaking((BuildingClassTypes)eBuildingClass) : -1;
}

int CyTeam::getBuildingClassCountPlusMaking(int /*BuildingClassTypes*/ eBuildingClass)
{
	return m_pTeam ? m_pTeam->getBuildingClassCountPlusMaking((BuildingClassTypes)eBuildingClass) : -1;
}

int CyTeam::getHasReligionCount(int /*ReligionTypes*/ eReligion)
{
	return m_pTeam ? m_pTeam->getHasReligionCount((ReligionTypes)eReligion) : -1;
}
int CyTeam::getHasCorporationCount(int /*CorporationTypes*/ eReligion)
{
	return m_pTeam ? m_pTeam->getHasCorporationCount((CorporationTypes)eReligion) : -1;
}
int CyTeam::countTotalCulture()
{
	return m_pTeam ? m_pTeam->countTotalCulture() : -1;
}

int CyTeam::countNumUnitsByArea(CyArea* pArea)
{
	return m_pTeam ? m_pTeam->countNumUnitsByArea(pArea->getArea()) : -1;
}

int CyTeam::countNumCitiesByArea(CyArea* pArea)
{
	return m_pTeam ? m_pTeam->countNumCitiesByArea(pArea->getArea()) : -1;
}

int CyTeam::countTotalPopulationByArea(CyArea* pArea)
{
	return m_pTeam ? m_pTeam->countTotalPopulationByArea(pArea->getArea()) : -1;
}

int CyTeam::countPowerByArea(CyArea* pArea)
{
	return m_pTeam ? m_pTeam->countPowerByArea(pArea->getArea()) : -1;
}

int CyTeam::countEnemyPowerByArea(CyArea* pArea)
{
	return m_pTeam ? m_pTeam->countEnemyPowerByArea(pArea->getArea()) : -1;
}

int CyTeam::countNumAIUnitsByArea(CyArea* pArea, int /*UnitAITypes*/ eUnitAI)
{
	return m_pTeam ? m_pTeam->countNumAIUnitsByArea(pArea->getArea(), (UnitAITypes) eUnitAI) : -1;
}

int CyTeam::countEnemyDangerByArea(CyArea* pArea)
{
	return m_pTeam ? m_pTeam->countEnemyDangerByArea(pArea->getArea()) : -1;
}

int CyTeam::getResearchCost(int /*TechTypes*/ eTech)
{
	return m_pTeam ? m_pTeam->getResearchCost((TechTypes)eTech) : -1;
}

int CyTeam::getResearchLeft(int /*TechTypes*/ eTech)
{
	return m_pTeam ? m_pTeam->getResearchLeft((TechTypes)eTech) : -1;
}
bool CyTeam::hasHolyCity(int /*ReligionTypes*/ eReligion)
{
	return m_pTeam ? m_pTeam->hasHolyCity((ReligionTypes)eReligion) : false;
}

bool CyTeam::hasHeadquarters(int /*CorporationTypes*/ eCorporation)
{
	return m_pTeam ? m_pTeam->hasHeadquarters((CorporationTypes)eCorporation) : false;
}

bool CyTeam::isHuman()
{
	return m_pTeam ? m_pTeam->isHuman() : false;
}

bool CyTeam::isBarbarian()
{
	return m_pTeam ? m_pTeam->isBarbarian() : false;
}

bool CyTeam::isMinorCiv()
{
	return m_pTeam ? m_pTeam->isMinorCiv() : false;
}

int /*PlayerTypes*/ CyTeam::getLeaderID()
{
	return m_pTeam ? m_pTeam->getLeaderID() : -1;
}

int /*PlayerTypes*/ CyTeam::getSecretaryID()
{
	return m_pTeam ? m_pTeam->getSecretaryID() : -1;
}

int /*HandicapTypes*/ CyTeam::getHandicapType()
{
	return m_pTeam ? m_pTeam->getHandicapType() : -1;
}

std::wstring CyTeam::getName()
{
	return m_pTeam ? m_pTeam->getName() : L"";
}

int CyTeam::getNumMembers()
{
	return m_pTeam ? m_pTeam->getNumMembers() : -1;
}

bool CyTeam::isAlive()
{
	return m_pTeam ? m_pTeam->isAlive() : false;
}

bool CyTeam::isEverAlive()
{
	return m_pTeam ? m_pTeam->isEverAlive() : false;
}

int CyTeam::getNumCities()
{
	return m_pTeam ? m_pTeam->getNumCities() : -1;
}

int CyTeam::getTotalPopulation()
{
	return m_pTeam ? m_pTeam->getTotalPopulation() : -1;
}

int CyTeam::getTotalLand()
{
	return m_pTeam ? m_pTeam->getTotalLand() : -1;
}

int CyTeam::getNukeInterception()
{
	return m_pTeam ? m_pTeam->getNukeInterception() : -1;
}

void CyTeam::changeNukeInterception(int iChange)
{
	if (m_pTeam)
		m_pTeam->changeNukeInterception(iChange);
}

int CyTeam::getForceTeamVoteEligibilityCount(int /*VoteSourceTypes*/ eVoteSource)
{
	return m_pTeam ? m_pTeam->getForceTeamVoteEligibilityCount((VoteSourceTypes)eVoteSource) : -1;
}

bool CyTeam::isForceTeamVoteEligible(int /*VoteSourceTypes*/ eVoteSource)
{
	return m_pTeam ? m_pTeam->isForceTeamVoteEligible((VoteSourceTypes)eVoteSource) : false;
}

void CyTeam::changeForceTeamVoteEligibilityCount(int /*VoteSourceTypes*/ eVoteSource, int iChange)
{
	if (m_pTeam)
		m_pTeam->changeForceTeamVoteEligibilityCount((VoteSourceTypes)eVoteSource, iChange);
}

int CyTeam::getExtraWaterSeeFromCount()
{
	return m_pTeam ? m_pTeam->getExtraWaterSeeFromCount() : -1;
}

bool CyTeam::isExtraWaterSeeFrom()	 
{
	return m_pTeam ? m_pTeam->isExtraWaterSeeFrom() : false;
}

void CyTeam::changeExtraWaterSeeFromCount(int iChange)
{
	if (m_pTeam)
		m_pTeam->changeExtraWaterSeeFromCount(iChange);
}

int CyTeam::getMapTradingCount()
{
	return m_pTeam ? m_pTeam->getMapTradingCount() : -1;
}

bool CyTeam::isMapTrading()
{
	return m_pTeam ? m_pTeam->isMapTrading() : false;
}

void CyTeam::changeMapTradingCount(int iChange)
{
	if (m_pTeam)
		m_pTeam->changeMapTradingCount(iChange);
}

int CyTeam::getTechTradingCount()
{
	return m_pTeam ? m_pTeam->getTechTradingCount() : -1;
}

bool CyTeam::isTechTrading()
{
	return m_pTeam ? m_pTeam->isTechTrading() : false;
}

void CyTeam::changeTechTradingCount(int iChange)
{
	if (m_pTeam)
		m_pTeam->changeTechTradingCount(iChange);
}

int CyTeam::getGoldTradingCount()
{
	return m_pTeam ? m_pTeam->getGoldTradingCount() : -1;
}

bool CyTeam::isGoldTrading()
{
	return m_pTeam ? m_pTeam->isGoldTrading() : false;
}

void CyTeam::changeGoldTradingCount(int iChange)
{
	if (m_pTeam)
		m_pTeam->changeGoldTradingCount(iChange);
}

int CyTeam::getOpenBordersTradingCount()
{
	return m_pTeam ? m_pTeam->getOpenBordersTradingCount() : -1;
}

bool CyTeam::isOpenBordersTrading()
{
	return m_pTeam ? m_pTeam->isOpenBordersTrading() : false;
}

void CyTeam::changeOpenBordersTradingCount(int iChange)
{
	if (m_pTeam)
		m_pTeam->changeOpenBordersTradingCount(iChange);
}

int CyTeam::getDefensivePactTradingCount()
{
	return m_pTeam ? m_pTeam->getDefensivePactTradingCount() : -1;
}

bool CyTeam::isDefensivePactTrading()
{
	return m_pTeam ? m_pTeam->isDefensivePactTrading() : false;
}

void CyTeam::changeDefensivePactTradingCount(int iChange)
{
	if (m_pTeam)
		m_pTeam->changeDefensivePactTradingCount(iChange);
}

int CyTeam::getPermanentAllianceTradingCount()
{
	return m_pTeam ? m_pTeam->getPermanentAllianceTradingCount() : -1;
}

bool CyTeam::isPermanentAllianceTrading()
{
	return m_pTeam ? m_pTeam->isPermanentAllianceTrading() : false;
}

void CyTeam::changePermanentAllianceTradingCount(int iChange)
{
	if (m_pTeam)
		m_pTeam->changePermanentAllianceTradingCount(iChange);
}

int CyTeam::getVassalTradingCount()
{
	return m_pTeam ? m_pTeam->getVassalTradingCount() : -1;
}

bool CyTeam::isVassalStateTrading()
{
	return m_pTeam ? m_pTeam->isVassalStateTrading() : false;
}

void CyTeam::changeVassalTradingCount(int iChange)
{
	if (m_pTeam)
		m_pTeam->changeVassalTradingCount(iChange);
}

int CyTeam::getBridgeBuildingCount()
{
	return m_pTeam ? m_pTeam->getBridgeBuildingCount() : -1;
}

bool CyTeam::isBridgeBuilding()
{
	return m_pTeam ? m_pTeam->isBridgeBuilding() : false;
}

void CyTeam::changeBridgeBuildingCount(int iChange)
{
	if (m_pTeam)
		m_pTeam->changeBridgeBuildingCount(iChange);
}

int CyTeam::getIrrigationCount()
{
	return m_pTeam ? m_pTeam->getIrrigationCount() : -1;
}

bool CyTeam::isIrrigation()
{
	return m_pTeam ? m_pTeam->isIrrigation() : false;
}

void CyTeam::changeIrrigationCount(int iChange)
{
	if (m_pTeam)
		m_pTeam->changeIrrigationCount(iChange);
}

int CyTeam::getIgnoreIrrigationCount()
{
	return m_pTeam ? m_pTeam->getIgnoreIrrigationCount() : -1;
}

bool CyTeam::isIgnoreIrrigation()
{
	return m_pTeam ? m_pTeam->isIgnoreIrrigation() : false;
}

void CyTeam::changeIgnoreIrrigationCount(int iChange)
{
	if (m_pTeam)
		m_pTeam->changeIgnoreIrrigationCount(iChange);
}

int CyTeam::getWaterWorkCount()
{
	return m_pTeam ? m_pTeam->getWaterWorkCount() : -1;
}

bool CyTeam::isWaterWork()
{
	return m_pTeam ? m_pTeam->isWaterWork() : false;
}

void CyTeam::changeWaterWorkCount(int iChange)
{
	if (m_pTeam)
		m_pTeam->changeWaterWorkCount(iChange);
}

int CyTeam::getVassalPower() const
{
	return (m_pTeam ? m_pTeam->getVassalPower() : -1);
}

void CyTeam::setVassalPower(int iPower)
{
	if (m_pTeam)
	{
		m_pTeam->setVassalPower(iPower);
	}
}

int CyTeam::getMasterPower() const
{
	return (m_pTeam ? m_pTeam->getMasterPower() : -1);
}

void CyTeam::setMasterPower(int iPower)
{
	if (m_pTeam)
	{
		m_pTeam->setMasterPower(iPower);
	}
}

int CyTeam::getEnemyWarWearinessModifier() const
{
	return m_pTeam ? m_pTeam->getEnemyWarWearinessModifier() : -1;
}

void CyTeam::changeEnemyWarWearinessModifier(int iChange)
{
	if (m_pTeam)
	{
		m_pTeam->changeEnemyWarWearinessModifier(iChange);
	}
}

bool CyTeam::isMapCentering()
{
	return m_pTeam ? m_pTeam->isMapCentering() : false;
}

void CyTeam::setMapCentering(bool bNewValue)
{
	if (m_pTeam)
		m_pTeam->setMapCentering(bNewValue);
}

int CyTeam::getID()
{
	return m_pTeam ? m_pTeam->getID() : -1;
}

bool CyTeam::isStolenVisibility(int /*TeamTypes*/ eIndex)
{
	return m_pTeam ? m_pTeam->isStolenVisibility((TeamTypes)eIndex) : false;
}

int CyTeam::getWarWeariness(int /*TeamTypes*/ eIndex)
{
	return m_pTeam ? m_pTeam->getWarWeariness((TeamTypes)eIndex) : -1;
}

void CyTeam::setWarWeariness(int /*TeamTypes*/ eIndex, int iNewValue)
{
	if (m_pTeam)
		m_pTeam->setWarWeariness((TeamTypes)eIndex, iNewValue);
}

void CyTeam::changeWarWeariness(int /*TeamTypes*/ eIndex, int iChange)	 
{
	if (m_pTeam)
		m_pTeam->changeWarWeariness((TeamTypes)eIndex, iChange);
}

int CyTeam::getTechShareCount(int iIndex)
{
	return m_pTeam ? m_pTeam->getTechShareCount(iIndex) : -1;
}

bool CyTeam::isTechShare(int iIndex)
{
	return m_pTeam ? m_pTeam->isTechShare(iIndex) : false;
}

void CyTeam::changeTechShareCount(int iIndex, int iChange)
{
	if (m_pTeam)
		m_pTeam->changeTechShareCount(iIndex, iChange);
}

int CyTeam::getCommerceFlexibleCount(int /*CommerceTypes*/ eIndex)
{
	return m_pTeam ? m_pTeam->getCommerceFlexibleCount((CommerceTypes)eIndex) : -1;
}

bool CyTeam::isCommerceFlexible(int /*CommerceTypes*/ eIndex)
{
	return m_pTeam ? m_pTeam->isCommerceFlexible((CommerceTypes)eIndex) : false;
}

void CyTeam::changeCommerceFlexibleCount(int /*CommerceTypes*/ eIndex, int iChange)
{
	if (m_pTeam)
		m_pTeam->changeCommerceFlexibleCount((CommerceTypes)eIndex, iChange);
}

int CyTeam::getExtraMoves(int /*DomainTypes*/ eIndex)
{
	return m_pTeam ? m_pTeam->getExtraMoves((DomainTypes)eIndex) : -1;
}

void CyTeam::changeExtraMoves(int /*DomainTypes*/ eIndex, int iChange)
{
	if (m_pTeam)
		m_pTeam->changeExtraMoves((DomainTypes)eIndex, iChange);
}

bool CyTeam::isHasMet(int /*TeamTypes*/ eIndex)
{
	return m_pTeam ? m_pTeam->isHasMet((TeamTypes)eIndex) : false;
}

bool CyTeam::isAtWar(int /*TeamTypes*/ iIndex)
{
	if (iIndex == NO_TEAM) return false;
	return m_pTeam ? m_pTeam->isAtWar((TeamTypes)iIndex) : false;
}

bool CyTeam::isPermanentWarPeace(int /*TeamTypes*/ eIndex)
{
	return m_pTeam ? m_pTeam->isPermanentWarPeace((TeamTypes)eIndex) : false;
}

void CyTeam::setPermanentWarPeace(int /*TeamTypes*/ eIndex, bool bNewValue)
{
	if (m_pTeam)
		m_pTeam->setPermanentWarPeace((TeamTypes)eIndex, bNewValue);
}

bool CyTeam::isFreeTrade(int /*TeamTypes*/ eIndex)
{
	return m_pTeam ? m_pTeam->isFreeTrade((TeamTypes)eIndex) : false;
}

bool CyTeam::isOpenBorders(int /*TeamTypes*/ eIndex)
{
	return m_pTeam ? m_pTeam->isOpenBorders((TeamTypes)eIndex) : false;
}

bool CyTeam::isForcePeace(int /*TeamTypes*/ eIndex)				 
{
	return m_pTeam ? m_pTeam->isForcePeace((TeamTypes)eIndex) : false;
}

bool CyTeam::isVassal(int /*TeamTypes*/ eIndex)				 
{
	return m_pTeam ? m_pTeam->isVassal((TeamTypes)eIndex) : false;
}

void CyTeam::setVassal(int /*TeamTypes*/ eIndex, bool bVassal, bool bCapitulated)				 
{
	if (m_pTeam)
	{
		m_pTeam->setVassal((TeamTypes)eIndex, bVassal, bCapitulated);
	}
}

void CyTeam::assignVassal(int /*TeamTypes*/ eIndex, bool bSurrender)				 
{
	if (m_pTeam)
	{
		m_pTeam->assignVassal((TeamTypes)eIndex, bSurrender);
	}
}

void CyTeam::freeVassal(int /*TeamTypes*/ eIndex)				 
{
	if (m_pTeam)
	{
		m_pTeam->freeVassal((TeamTypes)eIndex);
	}
}

bool CyTeam::isDefensivePact(int /*TeamTypes*/ eIndex)				 
{
	return m_pTeam ? m_pTeam->isDefensivePact((TeamTypes)eIndex) : false;
}

int CyTeam::getRouteChange(int /*RouteTypes*/ eIndex)
{
	return m_pTeam ? m_pTeam->getRouteChange((RouteTypes)eIndex) : -1;
}

void CyTeam::changeRouteChange(int /*RouteTypes*/ eIndex, int iChange)
{
	if (m_pTeam)
		m_pTeam->changeRouteChange((RouteTypes)eIndex, iChange);
}

int CyTeam::getProjectCount(int /*ProjectTypes*/ eIndex)
{
	return m_pTeam ? m_pTeam->getProjectCount((ProjectTypes)eIndex) : -1;
}

int CyTeam::getProjectDefaultArtType(int /*ProjectTypes*/ eIndex)
{
	return m_pTeam ? m_pTeam->getProjectDefaultArtType((ProjectTypes)eIndex) : -1;
}

void CyTeam::setProjectDefaultArtType(int /*ProjectTypes*/ eIndex, int value)
{
	if(m_pTeam != NULL)
		m_pTeam->setProjectDefaultArtType((ProjectTypes)eIndex, value);
}

int CyTeam::getProjectArtType(int /*ProjectTypes*/ eIndex, int number)
{
	if(m_pTeam != NULL)
		return m_pTeam->getProjectArtType((ProjectTypes)eIndex, number);
	else
		return -1;
}

void CyTeam::setProjectArtType(int /*ProjectTypes*/ eIndex, int number, int value)
{
	if(m_pTeam != NULL)
		m_pTeam->setProjectArtType((ProjectTypes)eIndex, number, value);
}


bool CyTeam::isProjectMaxedOut(int /*ProjectTypes*/ eIndex, int iExtra)
{
	return m_pTeam ? m_pTeam->isProjectMaxedOut((ProjectTypes)eIndex, iExtra) : false;
}

bool CyTeam::isProjectAndArtMaxedOut(int /*ProjectTypes*/ eIndex)
{
	return m_pTeam ? m_pTeam->isProjectAndArtMaxedOut((ProjectTypes)eIndex) : false;
}

void CyTeam::changeProjectCount(int /*ProjectTypes*/ eIndex, int iChange)
{
	if (m_pTeam)
		m_pTeam->changeProjectCount((ProjectTypes)eIndex, iChange);
}

int CyTeam::getProjectMaking(int /*ProjectTypes*/ eIndex)
{
	return m_pTeam ? m_pTeam->getProjectMaking((ProjectTypes)eIndex) : -1;
}

int CyTeam::getUnitClassCount(int /*UnitClassTypes*/ eIndex)
{
	return m_pTeam ? m_pTeam->getUnitClassCount((UnitClassTypes)eIndex) : -1;
}

bool CyTeam::isUnitClassMaxedOut(int /*UnitClassTypes*/ eIndex, int iExtra)
{
	return m_pTeam ? m_pTeam->isUnitClassMaxedOut((UnitClassTypes)eIndex, iExtra) : false;
}

int CyTeam::getBuildingClassCount(int /*BuildingClassTypes*/ eIndex)
{
	return m_pTeam ? m_pTeam->getBuildingClassCount((BuildingClassTypes)eIndex) : -1;
}

bool CyTeam::isBuildingClassMaxedOut(int /*BuildingClassTypes*/ eIndex, int iExtra)
{
	return m_pTeam ? m_pTeam->isBuildingClassMaxedOut((BuildingClassTypes)eIndex, iExtra) : false;
}

int CyTeam::getObsoleteBuildingCount(int /*BuildingTypes*/ eIndex)
{
	return m_pTeam ? m_pTeam->getObsoleteBuildingCount((BuildingTypes)eIndex) : -1;
}

bool CyTeam::isObsoleteBuilding(int /*BuildingTypes*/ eIndex)
{
	return m_pTeam ? m_pTeam->isObsoleteBuilding((BuildingTypes)eIndex) : false;
}

int CyTeam::getResearchProgress(int /*TechTypes*/ eIndex)
{
	return m_pTeam ? m_pTeam->getResearchProgress((TechTypes)eIndex) : -1;
}

void CyTeam::setResearchProgress(int /*TechTypes*/ eIndex, int iNewValue, int /*PlayerTypes*/ ePlayer)
{
	if (m_pTeam)
		m_pTeam->setResearchProgress((TechTypes)eIndex, iNewValue, (PlayerTypes)ePlayer);
}

void CyTeam::changeResearchProgress(int /*TechTypes*/ eIndex, int iChange, int /*PlayerTypes*/ ePlayer)
{
	if (m_pTeam)
		m_pTeam->changeResearchProgress((TechTypes)eIndex, iChange, (PlayerTypes)ePlayer);
}

int CyTeam::getTechCount(int /*TechTypes*/ eIndex)
{
	return m_pTeam ? m_pTeam->getTechCount((TechTypes)eIndex) : -1;
}

bool CyTeam::isTerrainTrade(int /*TerrainTypes*/ eIndex)
{
	if (m_pTeam)
	{
		return m_pTeam->isTerrainTrade((TerrainTypes)eIndex);
	}
	return false;
}

bool CyTeam::isRiverTrade()
{
	if (m_pTeam)
	{
		return m_pTeam->isRiverTrade();
	}
	return false;
}

bool CyTeam::isHasTech(int /* TechTypes */ iIndex)
{
	return m_pTeam ? m_pTeam->isHasTech((TechTypes)iIndex) : false;
}

void CyTeam::setHasTech(int /*TechTypes*/ eIndex, bool bNewValue, int /*PlayerTypes*/ ePlayer, bool bFirst, bool bAnnounce)
{
	if (m_pTeam)
		m_pTeam->setHasTech((TechTypes)eIndex, bNewValue, (PlayerTypes)ePlayer, bFirst, bAnnounce);
}

bool CyTeam::isNoTradeTech(int /* TechTypes */ iIndex)
{
	return m_pTeam ? m_pTeam->isNoTradeTech((TechTypes)iIndex) : false;
}

void CyTeam::setNoTradeTech(int /*TechTypes*/ eIndex, bool bNewValue)
{
	if (m_pTeam)
		m_pTeam->setNoTradeTech((TechTypes)eIndex, bNewValue);
}

int CyTeam::getImprovementYieldChange(int /*ImprovementTypes*/ eIndex1, int /*YieldTypes*/ eIndex2)
{
	return m_pTeam ? m_pTeam->getImprovementYieldChange((ImprovementTypes)eIndex1, (YieldTypes)eIndex2) : -1;
}

void CyTeam::changeImprovementYieldChange(int /*ImprovementTypes*/ eIndex1, int /*YieldTypes*/ eIndex2, int iChange)
{
	if (m_pTeam)
		m_pTeam->changeImprovementYieldChange((ImprovementTypes)eIndex1, (YieldTypes)eIndex2, iChange);
}

int CyTeam::getVictoryCountdown(int /*VictoryTypes*/ eVictory)
{
	return (m_pTeam ? m_pTeam->getVictoryCountdown((VictoryTypes)eVictory) : -1);
}

int CyTeam::getVictoryDelay(int /*VictoryTypes*/ eVictory)
{
	return (m_pTeam ? m_pTeam->getVictoryDelay((VictoryTypes)eVictory) : -1);
}

bool CyTeam::canLaunch(int /*VictoryTypes*/ eVictory)
{
	return (m_pTeam ? m_pTeam->canLaunch((VictoryTypes)eVictory) : false);
}

int CyTeam::getLaunchSuccessRate(int /*VictoryTypes*/ eVictory)
{
	return (m_pTeam ? m_pTeam->getLaunchSuccessRate((VictoryTypes)eVictory) : -1);
}


int CyTeam::getEspionagePointsAgainstTeam(int /*TeamTypes*/ eIndex)
{
	return m_pTeam ? m_pTeam->getEspionagePointsAgainstTeam((TeamTypes) eIndex) : -1;
}

void CyTeam::setEspionagePointsAgainstTeam(int /*TeamTypes*/ eIndex, int iValue)
{
	if (m_pTeam)
		m_pTeam->setEspionagePointsAgainstTeam((TeamTypes) eIndex, iValue);
}

void CyTeam::changeEspionagePointsAgainstTeam(int /*TeamTypes*/ eIndex, int iChange)
{
	if (m_pTeam)
		m_pTeam->changeEspionagePointsAgainstTeam((TeamTypes) eIndex, iChange);
}

int CyTeam::getEspionagePointsEver()
{
	return m_pTeam ? m_pTeam->getEspionagePointsEver() : -1;
}

void CyTeam::setEspionagePointsEver(int iValue)
{
	if (m_pTeam)
		m_pTeam->setEspionagePointsEver(iValue);
}

void CyTeam::changeEspionagePointsEver(int iChange)
{
	if (m_pTeam)
		m_pTeam->changeEspionagePointsEver(iChange);
}

int CyTeam::getCounterespionageTurnsLeftAgainstTeam(int /*TeamTypes*/ eIndex)
{
	return m_pTeam ? m_pTeam->getCounterespionageTurnsLeftAgainstTeam((TeamTypes) eIndex) : -1;
}

void CyTeam::setCounterespionageTurnsLeftAgainstTeam(int /*TeamTypes*/ eIndex, int iValue)
{
	if (m_pTeam)
		m_pTeam->setCounterespionageTurnsLeftAgainstTeam((TeamTypes) eIndex, iValue);
}

void CyTeam::changeCounterespionageTurnsLeftAgainstTeam(int /*TeamTypes*/ eIndex, int iChange)
{
	if (m_pTeam)
		m_pTeam->changeCounterespionageTurnsLeftAgainstTeam((TeamTypes) eIndex, iChange);
}

int CyTeam::getCounterespionageModAgainstTeam(int /*TeamTypes*/ eIndex)
{
	return m_pTeam ? m_pTeam->getCounterespionageModAgainstTeam((TeamTypes) eIndex) : -1;
}

void CyTeam::setCounterespionageModAgainstTeam(int /*TeamTypes*/ eIndex, int iValue)
{
	if (m_pTeam)
		m_pTeam->setCounterespionageModAgainstTeam((TeamTypes) eIndex, iValue);
}

void CyTeam::changeCounterespionageModAgainstTeam(int /*TeamTypes*/ eIndex, int iChange)
{
	if (m_pTeam)
		m_pTeam->changeCounterespionageModAgainstTeam((TeamTypes) eIndex, iChange);
}


bool CyTeam::AI_shareWar(int /*TeamTypes*/ eTeam)
{
	return m_pTeam ? m_pTeam->AI_shareWar((TeamTypes)eTeam) : false;
}

void CyTeam::AI_setWarPlan(int /*TeamTypes*/ eIndex, int /*WarPlanTypes*/ eNewValue)
{
	if (m_pTeam)
	{
		m_pTeam->AI_setWarPlan((TeamTypes)eIndex, (WarPlanTypes)eNewValue);
	}
}


int CyTeam::AI_getAtWarCounter(int /*TeamTypes*/ eTeam) const
{
	return m_pTeam ? m_pTeam->AI_getAtWarCounter((TeamTypes)eTeam) : -1;
}

int CyTeam::AI_getAtPeaceCounter(int /*TeamTypes*/ eTeam) const
{
	return m_pTeam ? m_pTeam->AI_getAtPeaceCounter((TeamTypes)eTeam) : -1;
}

int CyTeam::AI_getWarSuccess(int /*TeamTypes*/ eIndex) const
{
	return m_pTeam ? m_pTeam->AI_getWarSuccess((TeamTypes)eIndex) : -1;
}
