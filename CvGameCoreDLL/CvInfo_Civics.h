#pragma once

#ifndef CV_INFO_CIVICS_H
#define CV_INFO_CIVICS_H

/*  advc.003x: Cut from CvInfos.h. Just the civics classes:
	CvCivicInfo, CvCivicOptionInfo, CvUpkeepInfo.
	Would fit well together with CvTechInfo, but civics aren't included as often
	and are fairly likely to change; don't want to precompile them.
	Including civics in CvInfo_GameOption.h would be practical but counterintuitive. */

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvCivicInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvCivicInfo : public CvInfoBase
{
	typedef CvInfoBase base_t;
public: // The const functions are exposed to Python except those added by AdvCiv
	CvCivicInfo();
	~CvCivicInfo();

	CivicOptionTypes getCivicOptionType() const { return m_eCivicOptionType; }
	int getAnarchyLength() const { return m_iAnarchyLength; }
	int getUpkeep() const { return m_iUpkeep; }
	int getAIWeight() const { return m_iAIWeight; }
	bool canAlwaysForce() const { return m_bCanAlwaysForce; } // advc.132
	int getGreatPeopleRateModifier() const { return m_iGreatPeopleRateModifier; }
	int getGreatGeneralRateModifier() const { return m_iGreatGeneralRateModifier; }
	int getDomesticGreatGeneralRateModifier() const { return m_iDomesticGreatGeneralRateModifier; }
	int getStateReligionGreatPeopleRateModifier() const { return m_iStateReligionGreatPeopleRateModifier; }
	int getDistanceMaintenanceModifier() const { return m_iDistanceMaintenanceModifier; }
	// advc.912g:
	int getColonyMaintenanceModifier() const { return m_iColonyMaintenanceModifier; }
	int getNumCitiesMaintenanceModifier() const { return m_iNumCitiesMaintenanceModifier; }
	int getCorporationMaintenanceModifier() const { return m_iCorporationMaintenanceModifier; }
	int getExtraHealth() const { return m_iExtraHealth; }
	int getExtraHappiness() const { return m_iExtraHappiness; } // K-Mod, Exposed to Python
	int getFreeExperience() const { return m_iFreeExperience; }
	int getWorkerSpeedModifier() const { return m_iWorkerSpeedModifier; }
	int getImprovementUpgradeRateModifier() const { return m_iImprovementUpgradeRateModifier; }
	int getMilitaryProductionModifier() const { return m_iMilitaryProductionModifier; }
	int getBaseFreeUnits() const { return m_iBaseFreeUnits; }
	int getBaseFreeMilitaryUnits() const { return m_iBaseFreeMilitaryUnits; }
	int getFreeUnitsPopulationPercent() const { return m_iFreeUnitsPopulationPercent; }
	int getFreeMilitaryUnitsPopulationPercent() const { return m_iFreeMilitaryUnitsPopulationPercent; }
	int getGoldPerUnit() const { return m_iGoldPerUnit; }
	int getGoldPerMilitaryUnit() const { return m_iGoldPerMilitaryUnit; }
	int getHappyPerMilitaryUnit() const { return m_iHappyPerMilitaryUnit; }
	int getLuxuryModifier() const { return m_iLuxuryModifier; } // advc.912c
	int getLargestCityHappiness() const { return m_iLargestCityHappiness; }
	int getWarWearinessModifier() const { return m_iWarWearinessModifier; }
	int getFreeSpecialist() const { return m_iFreeSpecialist; }
	int getTradeRoutes() const { return m_iTradeRoutes; }
	TechTypes getTechPrereq() const { return m_eTechPrereq; }
	int getCivicPercentAnger() const { return m_iCivicPercentAnger; }
	int getMaxConscript() const { return m_iMaxConscript; }
	int getStateReligionHappiness() const { return m_iStateReligionHappiness; }
	int getNonStateReligionHappiness() const { return m_iNonStateReligionHappiness; }
	int getStateReligionUnitProductionModifier() const { return m_iStateReligionUnitProductionModifier; }
	int getStateReligionBuildingProductionModifier() const { return m_iStateReligionBuildingProductionModifier; }
	int getStateReligionFreeExperience() const { return m_iStateReligionFreeExperience; }
	int getExpInBorderModifier() const { return m_iExpInBorderModifier; }

	// doc
	int getLevelExperienceModifier() const { return m_iLevelExperienceModifier; }
	int getCorporationUnhappinessModifier() const { return m_iCorporationUnhappinessModifier; }
	int getProcessModifier() const { return m_iProcessModifier; }
	int getFoodProductionModifier() const { return m_iFoodProductionModifier; }
	int getWonderProductionModifier() const { return m_iWonderProductionModifier; }
	int getCorporationCommerceModifier() const { return m_iCorporationCommerceModifier; }
	int getDefensivePactTradeModifier() const { return m_iDefensivePactTradeModifier; }
	int getVassalTradeModifier() const { return m_iVassalTradeModifier; }
	int getShrineIncomeLimitChange() const { return m_iShrineIncomeLimitChange; }
	int getCaptureGoldModifier() const { return m_iCaptureGoldModifier; }
	int getCapitalBuildingProductionModifier() const { return m_iCapitalBuildingProductionModifier; }
	int getOccupationTimeChange() const { return m_iOccupationTimeChange; }

	bool isMilitaryFoodProduction() const { return m_bMilitaryFoodProduction; }
	//bool isNoUnhealthyPopulation() const; // K-Mod, 27/dec/10:
	int getUnhealthyPopulationModifier() const { return m_iUnhealthyPopulationModifier; }	// Exposed to Python
	bool isBuildingOnlyHealthy() const { return m_bBuildingOnlyHealthy; }
	bool isNoForeignTrade() const { return m_bNoForeignTrade; }
	bool isNoCorporations() const { return m_bNoCorporations; }
	bool isNoForeignCorporations() const { return m_bNoForeignCorporations; }
	bool isStateReligion() const { return m_bStateReligion; }
	bool isNoNonStateReligionSpread() const { return m_bNoNonStateReligionSpread; }

	// doc
	bool isNoForeignTradeModifier() const { return m_bNoForeignTradeModifier; }
	bool isSlavery() const { return m_bSlavery; }
	bool isNoSlavery() const { return m_bNoSlavery; }
	bool isColonialSlavery() const { return m_bColonialSlavery; }
	bool isNoStateReligionAnarchy() const { return m_bNoStateReligionAnarchy; }
	bool isFreeImprovementUpgrade() const { return m_bFreeImprovementUpgrade; }

	std::wstring pyGetWeLoveTheKing() { return getWeLoveTheKing(); }
	const wchar* getWeLoveTheKing();

	// Array access:

	int getYieldModifier(int i) const;
	int* getYieldModifierArray() const;
	int getCapitalYieldModifier(int i) const;
	int* getCapitalYieldModifierArray() const;
	int getTradeYieldModifier(int i) const;
	int* getTradeYieldModifierArray() const;
	int getCommerceModifier(int i) const;
	int* getCommerceModifierArray() const;
	int getCapitalCommerceModifier(int i) const;
	int* getCapitalCommerceModifierArray() const;
	int getSpecialistExtraCommerce(int i) const;
	int* getSpecialistExtraCommerceArray() const;

	// doc
	int getStateReligionBuildingYield(YieldTypes eYield) const { m_piStateReligionBuildingYield[eYield]; }
	int* getStateReligionBuildingYieldArray() { return m_piStateReligionBuildingYield; }
	int getSpecialistExtraYield(YieldTypes eYield) const { return m_piSpecialistExtraYield[eYield]; }
	int* getSpecialistExtraYieldArray() const { return m_piSpecialistExtraYield; }
	int getSpecialistCount(SpecialistTypes eSpecialist) const { return m_piSpecialistCount[eSpecialist]; }
	int* getSpecialistCountArray() const { return m_piSpecialistCount;  }

	int getBuildingHappinessChanges(int i) const;
	bool isAnyBuildingHappinessChanges() const { return (m_paiBuildingHappinessChanges != NULL); } // advc.003t
	int getBuildingHealthChanges(int i) const;
	bool isAnyBuildingHealthChanges() const { return (m_paiBuildingHealthChanges != NULL); } // advc.003t
	int getFeatureHappinessChanges(int i) const;

	// doc
	int getDomainExperienceModifier(DomainTypes eDomain) const { return m_paiDomainExperienceModifiers[eDomain]; }
	int getBuildingProductionModifier(BuildingClassTypes eBuildingClass) const { return m_paiBuildingProductionModifiers[eBuildingClass]; }

	bool isHurry(int i) const;
	bool isSpecialBuildingNotRequired(int i) const;
	bool isSpecialistValid(int i) const;

	int getImprovementYieldChanges(int i, int j) const;

	// doc
	int getSpecialistTypeExtraYield(SpecialistTypes eSpecialist, YieldTypes eYield) const;

	#if ENABLE_XML_FILE_CACHE
	void read(FDataStreamBase* stream);
	void write(FDataStreamBase* stream);
	#endif
	bool read(CvXMLLoadUtility* pXML);

protected:
	CivicOptionTypes m_eCivicOptionType;
	int m_iAnarchyLength;
	int m_iUpkeep;
	int m_iAIWeight;
	int m_iGreatPeopleRateModifier;
	int m_iGreatGeneralRateModifier;
	int m_iDomesticGreatGeneralRateModifier;
	int m_iStateReligionGreatPeopleRateModifier;
	int m_iDistanceMaintenanceModifier;
	int m_iColonyMaintenanceModifier; // advc.912g
	int m_iNumCitiesMaintenanceModifier;
	int m_iCorporationMaintenanceModifier;
	int m_iExtraHealth;
	int m_iExtraHappiness; // K-Mod
	int m_iFreeExperience;
	int m_iWorkerSpeedModifier;
	int m_iImprovementUpgradeRateModifier;
	int m_iMilitaryProductionModifier;
	int m_iBaseFreeUnits;
	int m_iBaseFreeMilitaryUnits;
	int m_iFreeUnitsPopulationPercent;
	int m_iFreeMilitaryUnitsPopulationPercent;
	int m_iGoldPerUnit;
	int m_iGoldPerMilitaryUnit;
	int m_iHappyPerMilitaryUnit;
	int m_iLuxuryModifier; // advc.912c
	int m_iLargestCityHappiness;
	int m_iWarWearinessModifier;
	int m_iFreeSpecialist;
	int m_iTradeRoutes;
	TechTypes m_eTechPrereq;
	int m_iCivicPercentAnger;
	int m_iMaxConscript;
	int m_iStateReligionHappiness;
	int m_iNonStateReligionHappiness;
	int m_iStateReligionUnitProductionModifier;
	int m_iStateReligionBuildingProductionModifier;
	int m_iStateReligionFreeExperience;
	int m_iExpInBorderModifier;

	// doc
	int m_iLevelExperienceModifier;
	int m_iCorporationUnhappinessModifier;
	int m_iProcessModifier;
	int m_iFoodProductionModifier;
	int m_iWonderProductionModifier;
	int m_iCorporationCommerceModifier;
	int m_iDefensivePactTradeModifier;
	int m_iVassalTradeModifier;
	int m_iShrineIncomeLimitChange;
	int m_iCaptureGoldModifier;
	int m_iCapitalBuildingProductionModifier;
	int m_iOccupationTimeChange;

	//bool m_bNoUnhealthyPopulation;
	int m_iUnhealthyPopulationModifier; // K-Mod
	bool m_bMilitaryFoodProduction;
	bool m_bBuildingOnlyHealthy;
	bool m_bNoForeignTrade;
	bool m_bNoCorporations;
	bool m_bNoForeignCorporations;
	bool m_bStateReligion;
	bool m_bNoNonStateReligionSpread;
	bool m_bCanAlwaysForce; // advc.132

	// doc
	bool m_bNoForeignTradeModifier;
	bool m_bSlavery;
	bool m_bNoSlavery;
	bool m_bColonialSlavery;
	bool m_bNoStateReligionAnarchy;
	bool m_bFreeImprovementUpgrade;

	CvWString m_szWeLoveTheKingKey;

	int* m_piYieldModifier;
	int* m_piCapitalYieldModifier;
	int* m_piTradeYieldModifier;
	int* m_piCommerceModifier;
	int* m_piCapitalCommerceModifier;
	int* m_piSpecialistExtraCommerce;

	// doc
	int* m_piStateReligionBuildingYield;
	int* m_piSpecialistExtraYield;
	int* m_piSpecialistCount;

	int* m_paiBuildingHappinessChanges;
	int* m_paiBuildingHealthChanges;
	int* m_paiFeatureHappinessChanges;

	// doc
	int* m_paiDomainExperienceModifiers;
	int* m_paiBuildingProductionModifiers;

	bool* m_pabHurry;
	bool* m_pabSpecialBuildingNotRequired;
	bool* m_pabSpecialistValid;

	int** m_ppiImprovementYieldChanges;
	int** m_ppiSpecialistTypeExtraYields; // doc
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvCivicOptionInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvCivicOptionInfo : public CvInfoBase
{
	typedef CvInfoBase base_t;
public:
	CvCivicOptionInfo();
	~CvCivicOptionInfo();

	bool getTraitNoUpkeep(int i) const; // Exposed to Python
	bool read(CvXMLLoadUtility* pXML);

protected:
	bool* m_pabTraitNoUpkeep;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvUpkeepInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvUpkeepInfo : public CvInfoBase
{
	typedef CvInfoBase base_t;
public:
	CvUpkeepInfo();

	int getPopulationPercent() const //	Exposed to Python
	{
		return m_iPopulationPercent;
	}
	int getCityPercent() const	//	Exposed to Python
	{
		return m_iCityPercent;
	}
	bool read(CvXMLLoadUtility* pXML);

protected:
	int m_iPopulationPercent;
	int m_iCityPercent;

};

#endif
