#pragma once

#ifndef CyTeam_h
#define CyTeam_h
//
// Python wrapper class for CvTeam
// 

// //#include "CvEnums.h"

class CvTeam;
class CyArea;
class CyTeam
{
public:
	CyTeam();
	CyTeam(CvTeam* pTeam);		// Call from C++
	CvTeam* getTeam() { return m_pTeam;	}	// Call from C++

	bool isNone() { return (m_pTeam==NULL); }

	void addTeam(int /*TeamTypes*/ eTeam);

	bool canChangeWarPeace(int /*TeamTypes*/ eTeam);
	bool canDeclareWar(int /*TeamTypes*/ eTeam);
	void declareWar(int /*TeamTypes*/ eTeam, bool bNewDiplo, int /*WarPlanTypes*/ eWarPlan);
	void makePeace(int /*TeamTypes*/ eTeam);
	bool canContact(int /*TeamTypes*/ eTeam);
	void meet(int /*TeamTypes*/ eTeam, bool bNewDiplo);
	void signOpenBorders(int /*TeamTypes*/ eTeam);
	void signDefensivePact(int /*TeamTypes*/ eTeam);

	int getAssets();
	int getPower(bool bIncludeVassals);
	int getDefensivePower();
	int getNumNukeUnits();

	int getAtWarCount(bool bIgnoreMinors);
	int getWarPlanCount(int /*WarPlanTypes*/ eWarPlan, bool bIgnoreMinors);
	int getAnyWarPlanCount(bool bIgnoreMinors);
	int getChosenWarCount(bool bIgnoreMinors);
	int getHasMetCivCount(bool bIgnoreMinors);
	bool hasMetHuman();
	int getDefensivePactCount();
	bool isAVassal() const;

	int getUnitClassMaking(int /*UnitClassTypes*/ eUnitClass);
	int getUnitClassCountPlusMaking(int /*UnitClassTypes*/ eUnitClass);
	int getBuildingClassMaking(int /*BuildingClassTypes*/ eBuildingClass);
	int getBuildingClassCountPlusMaking(int /*BuildingClassTypes*/ eUnitClass);
	int getHasReligionCount(int /*ReligionTypes*/ eReligion);
	int getHasCorporationCount(int /*CorporationTypes*/ eCorporation);

	int countTotalCulture();

	int countNumUnitsByArea(CyArea* pArea);
	int countNumCitiesByArea(CyArea* pArea);
	int countTotalPopulationByArea(CyArea* pArea);
	int countPowerByArea(CyArea* pArea);
	int countEnemyPowerByArea(CyArea* pArea);
	int countNumAIUnitsByArea(CyArea* pArea, int /*UnitAITypes*/ eUnitAI);
	int countEnemyDangerByArea(CyArea* pArea);

	int getResearchCost(int /*TechTypes*/ eTech);
	int getResearchLeft(int /*TechTypes*/ eTech);

	bool hasHolyCity(int /*ReligionTypes*/ eReligion);
	bool hasHeadquarters(int /*CorporationTypes*/ eCorporation);

	bool isHuman();
	bool isBarbarian();
	bool isMinorCiv();
	int /*PlayerTypes*/ getLeaderID();
	int /*PlayerTypes*/ getSecretaryID();
	int /*HandicapTypes*/ getHandicapType();
	std::wstring getName();

	int getNumMembers();
	bool isAlive();
	bool isEverAlive();
	int getNumCities();
	int getTotalPopulation();
	int getTotalLand();
	int getNukeInterception();
	void changeNukeInterception(int iChange);	 

	int getForceTeamVoteEligibilityCount(int /*VoteSourceTypes*/ eVoteSource);
	bool isForceTeamVoteEligible(int /*VoteSourceTypes*/ eVoteSource);
	void changeForceTeamVoteEligibilityCount(int /*VoteSourceTypes*/ eVoteSource, int iChange);
	int getExtraWaterSeeFromCount();
	bool isExtraWaterSeeFrom();		 
	void changeExtraWaterSeeFromCount(int iChange);
	int getMapTradingCount();
	bool isMapTrading();
	void changeMapTradingCount(int iChange);
	int getTechTradingCount();
	bool isTechTrading();
	void changeTechTradingCount(int iChange);
	int getGoldTradingCount();
	bool isGoldTrading();
	void changeGoldTradingCount(int iChange);
	int getOpenBordersTradingCount();
	bool isOpenBordersTrading();
	void changeOpenBordersTradingCount(int iChange);
	int getDefensivePactTradingCount();
	bool isDefensivePactTrading();
	void changeDefensivePactTradingCount(int iChange);															
	int getPermanentAllianceTradingCount();
	bool isPermanentAllianceTrading();
	void changePermanentAllianceTradingCount(int iChange);													
	int getVassalTradingCount();
	bool isVassalStateTrading();
	void changeVassalTradingCount(int iChange);													
	int getBridgeBuildingCount();
	bool isBridgeBuilding();
	void changeBridgeBuildingCount(int iChange);																		
	int getIrrigationCount();
	bool isIrrigation();
	void changeIrrigationCount(int iChange);																				
	int getIgnoreIrrigationCount();
	bool isIgnoreIrrigation();
	void changeIgnoreIrrigationCount(int iChange);																	
	int getWaterWorkCount();
	bool isWaterWork();
	void changeWaterWorkCount(int iChange);																	

	int getVassalPower() const;
	void setVassalPower(int iPower);
	int getMasterPower() const;
	void setMasterPower(int iPower);

	int getEnemyWarWearinessModifier() const;																																			// Exposed to Python
	void changeEnemyWarWearinessModifier(int iChange);

	bool isMapCentering();
	void setMapCentering(bool bNewValue);

	int getID();

	bool isStolenVisibility(int /*TeamTypes*/ eIndex);
	int getWarWeariness(int /*TeamTypes*/ eIndex);								 
	void setWarWeariness(int /*TeamTypes*/ eIndex, int iNewValue);	 
	void changeWarWeariness(int /*TeamTypes*/ eIndex, int iChange);	 
	int getTechShareCount(int iIndex);
	bool isTechShare(int iIndex);
	void changeTechShareCount(int iIndex, int iChange);
	int getCommerceFlexibleCount(int /*CommerceTypes*/ eIndex);
	bool isCommerceFlexible(int /*CommerceTypes*/ eIndex);
	void changeCommerceFlexibleCount(int /*CommerceTypes*/ eIndex, int iChange);

	int getExtraMoves(int /*DomainTypes*/ eIndex);
	void changeExtraMoves(int /*DomainTypes*/ eIndex, int iChange);

	bool isHasMet(int /*TeamTypes*/ eIndex);
	bool isAtWar(int /*TeamTypes*/ eIndex);
	bool isPermanentWarPeace(int /*TeamTypes*/ eIndex);
	void setPermanentWarPeace(int /*TeamTypes*/ eIndex, bool bNewValue);

	bool isFreeTrade(int /*TeamTypes*/ eIndex);
	bool isOpenBorders(int /*TeamTypes*/ eIndex);
	bool isForcePeace(int /*TeamTypes*/ eIndex);
	bool isVassal(int /*TeamTypes*/ eIndex);
	void setVassal(int /*TeamTypes*/ eIndex, bool bVassal, bool bCapitulated);
	void assignVassal(int /*TeamTypes*/ eIndex, bool bSurrender);
	void freeVassal(int /*TeamTypes*/ eIndex);
	bool isDefensivePact(int /*TeamTypes*/ eIndex);
	int getRouteChange(int /*RouteTypes*/ eIndex);
	void changeRouteChange(int /*RouteTypes*/ eIndex, int iChange);
	int getProjectCount(int /*ProjectTypes*/ eIndex);
	int getProjectDefaultArtType(int /*ProjectTypes*/ eIndex);
	void setProjectDefaultArtType(int /*ProjectTypes*/ eIndex, int value);
	int getProjectArtType(int /*ProjectTypes*/ eIndex, int number);
	void setProjectArtType(int /*ProjectTypes*/ eIndex, int number, int value);
	bool isProjectMaxedOut(int /*ProjectTypes*/ eIndex, int iExtra);
	bool isProjectAndArtMaxedOut(int /*ProjectTypes*/ eIndex);
	void changeProjectCount(int /*ProjectTypes*/ eIndex, int iChange);
	int getProjectMaking(int /*ProjectTypes*/ eIndex);
	int getUnitClassCount(int /*UnitClassTypes*/ eIndex);
	bool isUnitClassMaxedOut(int /*UnitClassTypes*/ eIndex, int iExtra);
	int getBuildingClassCount(int /*BuildingClassTypes*/ eIndex);
	bool isBuildingClassMaxedOut(int /*BuildingClassTypes*/ eIndex, int iExtra);
	int getObsoleteBuildingCount(int /*BuildingTypes*/ eIndex);
	bool isObsoleteBuilding(int /*BuildingTypes*/ eIndex);

	int getResearchProgress(int /*TechTypes*/ eIndex);
	void setResearchProgress(int /*TechTypes*/ eIndex, int iNewValue, int /*PlayerTypes*/ ePlayer);
	void changeResearchProgress(int /*TechTypes*/ eIndex, int iChange, int /*PlayerTypes*/ ePlayer);
	int getTechCount(int /*TechTypes*/ eIndex);

	bool isTerrainTrade(int /*TerrainTypes*/ eIndex);
	bool isRiverTrade();
	bool isHasTech(int /*TechTypes*/ iIndex);
	void setHasTech(int /*TechTypes*/ eIndex, bool bNewValue, int /*PlayerTypes*/ ePlayer, bool bFirst, bool bAnnounce);
	bool isNoTradeTech(int /*TechType */ iIndex);
	void setNoTradeTech(int /*TechTypes*/ eIndex, bool bNewValue);

	int getImprovementYieldChange(int /*ImprovementTypes*/ eIndex, int /*YieldTypes*/ eIndex2);
	void changeImprovementYieldChange(int /*ImprovementTypes*/ eIndex1, int /*YieldTypes*/ eIndex2, int iChange);

	int getVictoryCountdown(int /*VictoryTypes*/ eVictory);
	int getVictoryDelay(int /*VictoryTypes*/ eVictory);
	bool canLaunch(int /*VictoryTypes*/ eVictory);
	int getLaunchSuccessRate(int /*VictoryTypes*/ eVictory);

	int getEspionagePointsAgainstTeam(int /*TeamTypes*/ eIndex);
	void setEspionagePointsAgainstTeam(int /*TeamTypes*/ eIndex, int iValue);
	void changeEspionagePointsAgainstTeam(int /*TeamTypes*/ eIndex, int iChange);
	int getEspionagePointsEver();
	void setEspionagePointsEver(int iValue);
	void changeEspionagePointsEver(int iChange);
	int getCounterespionageTurnsLeftAgainstTeam(int /*TeamTypes*/ eIndex);
	void setCounterespionageTurnsLeftAgainstTeam(int /*TeamTypes*/ eIndex, int iValue);
	void changeCounterespionageTurnsLeftAgainstTeam(int /*TeamTypes*/ eIndex, int iChange);
	int getCounterespionageModAgainstTeam(int /*TeamTypes*/ eIndex);
	void setCounterespionageModAgainstTeam(int /*TeamTypes*/ eIndex, int iValue);
	void changeCounterespionageModAgainstTeam(int /*TeamTypes*/ eIndex, int iChange);

	bool AI_shareWar(int /*TeamTypes*/ eTeam);
	void AI_setWarPlan(int /*TeamTypes*/ eIndex, int /*WarPlanTypes*/ eNewValue);
	int AI_getAtWarCounter(int /*TeamTypes*/ eTeam) const;
	int AI_getAtPeaceCounter(int /*TeamTypes*/ eTeam) const;
	int AI_getWarSuccess(int /*TeamTypes*/ eIndex) const;

protected:

	CvTeam* m_pTeam;

};

#endif	// #ifndef CyTeam
