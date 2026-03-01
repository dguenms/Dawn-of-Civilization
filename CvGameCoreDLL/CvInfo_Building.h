#pragma once

#ifndef CV_INFO_BUILDING_H
#define CV_INFO_BUILDING_H

/*  advc.003x: Cut from CvInfos.h. Building-related classes:
	CvBuildingInfo
	CvBuildingClassInfo (for the mapping to CvBuildingInfo, CvCivilizationInfo gets precompiled)
	CvSpecialBuildingInfo
	CvVoteSourceInfo (tied to a building)
	CvVoteInfo (should stay with CvVoteSourceInfo)
	CvProjectInfo (very similar to a building)
	advc.003t: All array members in this class replaced with CvInfoMaps or vectors. */
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvBuildingClassInfo  // advc: Moved up for inline function calls from CvBuilding
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvBuildingClassInfo : public CvInfoBase
{
	typedef CvInfoBase base_t;
public: // All the const functions are exposed to Python
	CvBuildingClassInfo();

	int getMaxGlobalInstances() const
	{
		return m_iMaxGlobalInstances;
	}
	bool isWorldWonder() const // advc.003w: Replacing global isWorldWonderClass
	{
		return (getMaxGlobalInstances() != -1);
	}
	int getMaxTeamInstances() const
	{
		return m_iMaxTeamInstances;
	}
	bool isTeamWonder() const // advc.003w: Replacing global isTeamWonderClass
	{
		return (getMaxTeamInstances() != -1);
	}
	int getMaxPlayerInstances() const
	{
		return m_iMaxPlayerInstances;
	}
	bool isNationalWonder() const // advc.003w: Replacing global isNationalWonderClass
	{
		return (getMaxPlayerInstances() != -1);
	}
	bool isLimited() const // advc.003w: Replacing global isLimitedWonderClass
	{
		return (isWorldWonder() || isTeamWonder() || isNationalWonder());
	}
	int getExtraPlayerInstances() const
	{
		return m_iExtraPlayerInstances;
	}
	BuildingTypes getDefaultBuilding() const // advc.003x: Renamed from getDefaultBuildingIndex
	{
		return (BuildingTypes)m_iDefaultBuildingIndex;
	}
	bool isNoLimit() const
	{
		return m_bNoLimit;
	}
	int getLimit() const; // advc.003w: Replacing global limitedWonderClassLimit

	bool isMonument() const { return m_bMonument; }
	/*  advc (note): Unused in XML. Number of buildings of this class required for
		team victory as a necessary (not sufficient) condition. No AI code for this. */
	DEF_INFO_ENUM_MAP(VictoryThreshold, Victory, int, short, NonDefaultEnumMap);

	bool read(CvXMLLoadUtility* pXML);
	bool readPass3();

protected:
	int m_iMaxGlobalInstances;
	int m_iMaxTeamInstances;
	int m_iMaxPlayerInstances;
	int m_iExtraPlayerInstances;
	int m_iDefaultBuildingIndex;

	bool m_bNoLimit;
	bool m_bMonument;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvBuildingInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvBuildingInfo : public CvHotkeyInfo
{
	// <advc.tag>
	typedef CvHotkeyInfo base_t;
protected:
	void addElements(ElementList& kElements) const
	{
		base_t::addElements(kElements);
		kElements.addInt(RaiseDefense, "RaiseDefense"); // advc.004c
	}
public:
	enum IntElementTypes
	{
		RaiseDefense = base_t::NUM_INT_ELEMENT_TYPES, // advc.004c
		NUM_INT_ELEMENT_TYPES
	};
	int get(IntElementTypes e) const
	{
		return base_t::get(static_cast<base_t::IntElementTypes>(e));
	} // </advc.tag>

	/*	All the const functions are exposed to Python.
		Integers in signatures replaced with enum types. */
	CvBuildingInfo();

	BuildingClassTypes getBuildingClassType() const
	{
		return m_eBuildingClassType;
	}
	VictoryTypes getVictoryPrereq() const { return m_eVictoryPrereq; }
	EraTypes getFreeStartEra() const { return m_eFreeStartEra; }
	EraTypes getMaxStartEra() const { return m_eMaxStartEra; }
	TechTypes getObsoleteTech() const { return m_eObsoleteTech; }
	TechTypes getPrereqAndTech() const { return m_ePrereqAndTech; }
	bool isTechRequired(TechTypes eTech) const; // advc.003w: Replacing global isTechRequiredForBuilding
	BonusTypes getNoBonus() const { return m_eNoBonus; }
	BonusTypes getPowerBonus() const { return m_ePowerBonus; }
	BonusTypes getFreeBonus() const { return m_eFreeBonus; }
	int getNumFreeBonuses() const { return m_iNumFreeBonuses; }
	BuildingClassTypes getFreeBuildingClass() const { return m_eFreeBuildingClass; }
	PromotionTypes getFreePromotion() const { return m_eFreePromotion; }
	CivicOptionTypes getCivicOption() const { return m_eCivicOption; }
	int getAIWeight() const { return m_iAIWeight; }
	int getProductionCost() const { return m_iProductionCost; }
	int getHurryCostModifier() const { return m_iHurryCostModifier; }
	int getHurryAngerModifier() const { return m_iHurryAngerModifier; }
	int getAdvancedStartCost() const { return m_iAdvancedStartCost; }
	int getAdvancedStartCostIncrease() const { return m_iAdvancedStartCostIncrease; }
	int getMinAreaSize() const { return m_iMinAreaSize; }
	int getNumCitiesPrereq() const { return m_iNumCitiesPrereq; }
	int getNumTeamsPrereq() const { return m_iNumTeamsPrereq; }
	int getUnitLevelPrereq() const { return m_iUnitLevelPrereq; }
	int getMinLatitude() const { return m_iMinLatitude; }
	int getMaxLatitude() const { return m_iMaxLatitude; }
	int getGreatPeopleRateModifier() const { return m_iGreatPeopleRateModifier; }
	int getGreatGeneralRateModifier() const { return m_iGreatGeneralRateModifier; }
	int getDomesticGreatGeneralRateModifier() const;
	int getGlobalGreatPeopleRateModifier() const { return m_iGlobalGreatPeopleRateModifier; }
	int getAnarchyModifier() const { return m_iAnarchyModifier; }
	int getGoldenAgeModifier() const { return m_iGoldenAgeModifier; }
	int getGlobalHurryModifier() const { return m_iGlobalHurryModifier; }
	int getFreeExperience() const { return m_iFreeExperience; }
	int getGlobalFreeExperience() const { return m_iGlobalFreeExperience; }
	int getFoodKept() const { return m_iFoodKept; }
	int getAirlift() const { return m_iAirlift; }
	int getAirModifier() const { return m_iAirModifier; }
	int getAirUnitCapacity() const { return m_iAirUnitCapacity; }
	int getNukeModifier() const { return m_iNukeModifier; }
	int getNukeExplosionRand() const { return m_iNukeExplosionRand; }
	int getFreeSpecialist() const { return m_iFreeSpecialist; }
	int getAreaFreeSpecialist() const { return m_iAreaFreeSpecialist; }
	int getGlobalFreeSpecialist() const { return m_iGlobalFreeSpecialist; }
	int getHappiness() const { return m_iHappiness; }
	int getAreaHappiness() const { return m_iAreaHappiness; }
	int getGlobalHappiness() const { return m_iGlobalHappiness; }
	int getStateReligionHappiness() const { return m_iStateReligionHappiness; }
	int getWorkerSpeedModifier() const { return m_iWorkerSpeedModifier; }
	int getMilitaryProductionModifier() const { return m_iMilitaryProductionModifier; }
	int getSpaceProductionModifier() const { return m_iSpaceProductionModifier; }
	int getGlobalSpaceProductionModifier() const { return m_iGlobalSpaceProductionModifier; }
	int getTradeRoutes() const { return m_iTradeRoutes; }
	int getCoastalTradeRoutes() const { return m_iCoastalTradeRoutes; }
	int getAreaTradeRoutes() const; // advc.310: Renamed; was getGlobalTradeRoutes.
	int getTradeRouteModifier() const { return m_iTradeRouteModifier; }
	int getForeignTradeRouteModifier() const { return m_iForeignTradeRouteModifier; }
	int getAssetValue() const { return m_iAssetValue; }
	int getPowerValue() const { return m_iPowerValue; }
	SpecialBuildingTypes getSpecialBuildingType() const
	{
		return m_eSpecialBuildingType;
	}
	AdvisorTypes getAdvisorType() const { return m_eAdvisorType; }
	ReligionTypes getHolyCity() const { return m_eHolyCity; }
	ReligionTypes getReligionType() const { return m_eReligionType; }
	ReligionTypes getStateReligion() const { return m_eStateReligion; }
	ReligionTypes getPrereqReligion() const { return m_ePrereqReligion; }
	CorporationTypes getPrereqCorporation() const
	{
		return m_ePrereqCorporation;
	}
	CorporationTypes getFoundsCorporation() const
	{
		return m_eFoundsCorporation;
	}
	ReligionTypes getGlobalReligionCommerce() const
	{
		return m_eGlobalReligionCommerce;
	}
	CorporationTypes getGlobalCorporationCommerce() const
	{
		return m_eGlobalCorporationCommerce;
	}
	BonusTypes getPrereqAndBonus() const { return m_ePrereqAndBonus; }
	UnitClassTypes getGreatPeopleUnitClass() const { return m_eGreatPeopleUnitClass; }
	int getGreatPeopleRateChange() const { return m_iGreatPeopleRateChange; }
	int getConquestProbability() const { return m_iConquestProbability; }
	int getMaintenanceModifier() const { return m_iMaintenanceModifier; }
	int getWarWearinessModifier() const { return m_iWarWearinessModifier; }
	int getGlobalWarWearinessModifier() const { return m_iGlobalWarWearinessModifier; }
	int getEnemyWarWearinessModifier() const { return m_iEnemyWarWearinessModifier; }
	int getHealRateChange() const { return m_iHealRateChange; }
	int getHealth() const { return m_iHealth; }
	int getAreaHealth() const { return m_iAreaHealth; }
	int getGlobalHealth() const { return m_iGlobalHealth; }
	int getGlobalPopulationChange() const { return m_iGlobalPopulationChange; }
	int getFreeTechs() const { return m_iFreeTechs; }
	int getDefenseModifier() const { return m_iDefenseModifier; }
	int getBombardDefenseModifier() const { return m_iBombardDefenseModifier; }
	int getAllCityDefenseModifier() const { return m_iAllCityDefenseModifier; }
	int getEspionageDefenseModifier() const { return m_iEspionageDefenseModifier; }
	MissionTypes getMissionType() const { return m_eMissionType; }
	void setMissionType(MissionTypes eNewType);
	VoteSourceTypes getVoteSourceType() const { return m_eVoteSourceType; }

	float getVisibilityPriority() const;

	bool isTeamShare() const { return m_bTeamShare; }
	bool isWater() const { return m_bWater; }
	bool isRiver() const { return m_bRiver; }
	bool isPower() const { return m_bPower; }
	bool isDirtyPower() const { return m_bDirtyPower; }
	bool isAreaCleanPower() const { return m_bAreaCleanPower; }
	bool isAreaBorderObstacle() const;
	bool isForceTeamVoteEligible() const { return m_bForceTeamVoteEligible; }
	bool isCapital() const { return m_bCapital; }
	bool isGovernmentCenter() const { return m_bGovernmentCenter; }
	bool isGoldenAge() const { return m_bGoldenAge; }
	bool isMapCentering() const { return m_bMapCentering; }
	bool isNoUnhappiness() const { return m_bNoUnhappiness; }
	//bool isNoUnhealthyPopulation() const;
	int getUnhealthyPopulationModifier() const // K-Mod, Exposed to Python
	{
		return m_iUnhealthyPopulationModifier;
	}
	bool isBuildingOnlyHealthy() const { return m_bBuildingOnlyHealthy; }
	bool isNeverCapture() const { return m_bNeverCapture; }
	bool isNukeImmune() const { return m_bNukeImmune; }
	bool isPrereqReligion() const { return m_bPrereqReligion; }
	bool isCenterInCity() const { return m_bCenterInCity; }
	bool isStateReligion() const { return m_bStateReligion; }
	bool isAllowsNukes() const { return m_bAllowsNukes; }

	const TCHAR* getConstructSound() const;
	const TCHAR* getArtDefineTag() const;
	const TCHAR* getMovieDefineTag() const;

	// Array access ...

	DEF_SHORT_INFO_ENUM_MAP(YieldChange, Yield, YieldChangeMap);
	DEF_SHORT_INFO_ENUM_MAP(YieldModifier, Yield, YieldPercentMap);
	DEF_SHORT_INFO_ENUM_MAP(PowerYieldModifier, Yield, YieldPercentMap);
	DEF_SHORT_INFO_ENUM_MAP(AreaYieldModifier, Yield, YieldPercentMap);
	DEF_SHORT_INFO_ENUM_MAP(GlobalYieldModifier, Yield, YieldPercentMap);
	DEF_SHORT_INFO_ENUM_MAP(SeaPlotYieldChange, Yield, YieldChangeMap);
	DEF_SHORT_INFO_ENUM_MAP(RiverPlotYieldChange, Yield, YieldChangeMap);
	DEF_SHORT_INFO_ENUM_MAP(GlobalSeaPlotYieldChange, Yield, YieldChangeMap);
	DEF_SHORT_INFO_ENUM_MAP(CommerceChange, Commerce, CommerceChangeMap);
	DEF_SHORT_INFO_ENUM_MAP(ObsoleteSafeCommerceChange, Commerce, CommerceChangeMap);
	DEF_SHORT_INFO_ENUM_MAP(CommerceChangeDoubleTime, Commerce, CommercePercentMap);
	DEF_SHORT_INFO_ENUM_MAP(CommerceModifier, Commerce, CommercePercentMap);
	DEF_SHORT_INFO_ENUM_MAP(GlobalCommerceModifier, Commerce, CommercePercentMap);
	DEF_SHORT_INFO_ENUM_MAP(SpecialistExtraCommerce, Commerce, CommercePercentMap); // (not exposed to Python)
	DEF_SHORT_INFO_ENUM_MAP(StateReligionCommerce, Commerce, CommerceChangeMap);
	DEF_SHORT_INFO_ENUM_MAP(CommerceHappiness, Commerce, CommercePercentMap);

	DEF_INFO_ENUM_MAP(ReligionChange, Religion, int, char, NonDefaultEnumMap);
	DEF_INFO_ENUM_MAP(SpecialistCount, Specialist, int, char, ArrayEnumMap);
	DEF_INFO_ENUM_MAP(FreeSpecialistCount, Specialist, int, char, NonDefaultEnumMap);
	DEF_INFO_ENUM_MAP(BonusHealthChanges, Bonus, int, char, NonDefaultEnumMap);
	DEF_INFO_ENUM_MAP(BonusHappinessChanges, Bonus, int, char, NonDefaultEnumMap);
	DEF_INFO_ENUM_MAP(BonusProductionModifier, Bonus, int, short, NonDefaultEnumMap);
	DEF_INFO_ENUM_MAP(UnitCombatFreeExperience, UnitCombat, int, char, NonDefaultEnumMap);
	DEF_INFO_ENUM_MAP(DomainFreeExperience, Domain, int, char, ArrayEnumMap);
	DEF_INFO_ENUM_MAP(DomainProductionModifier, Domain, int, short, ArrayEnumMap);

	int getNumPrereqAndTechs() const { return m_aePrereqAndTechs.size(); }
	int getNumPrereqOrBonuses() const { return m_aePrereqOrBonuses.size(); }
	TechTypes getPrereqAndTechs(int i) const
	{
		FAssertBounds(0, getNumPrereqAndTechs(), i);
		return m_aePrereqAndTechs[i];
	}
	BonusTypes getPrereqOrBonuses(int i) const
	{
		FAssertBounds(0, getNumPrereqOrBonuses(), i);
		return m_aePrereqOrBonuses[i];
	}
	int py_getPrereqAndTechs(int i) const;
	int py_getPrereqOrBonuses(int i) const;

	DEF_INFO_ENUM_MAP(ProductionTraits, Trait, int, short, NonDefaultEnumMap);
	DEF_INFO_ENUM_MAP(HappinessTraits, Trait, int, char, NonDefaultEnumMap);
	DEF_INFO_ENUM_MAP(BuildingHappinessChanges, BuildingClass, int, char, NonDefaultEnumMap);
	DEF_INFO_ENUM_MAP(PrereqNumOfBuildingClass, BuildingClass, int, char, NonDefaultEnumMap);
	DEF_INFO_ENUM_MAP(FlavorValue, Flavor, int, short, NonDefaultEnumMap);
	DEF_INFO_ENUM_MAP(ImprovementFreeSpecialist, Improvement, int, char, NonDefaultEnumMap);
	DEF_INFO_ENUM_MAP_BOOL(CommerceFlexible, Commerce, ArrayEnumMap);
	DEF_INFO_ENUM_MAP_BOOL(CommerceChangeOriginalOwner, Commerce, ArrayEnumMap);
	DEF_INFO_ENUM_SET(BuildingClassNeededInCity, BuildingClass);
	// (Replacing optimizations by UNOFFICIAL_PATCH, 06/27/10, Afforess & jdog5000)
	DEF_INFO_ENUM2SHORT_MAP(SpecialistYieldChange, Specialist, Yield, YieldChangeMap, NonDefaultEnumMap);
	DEF_INFO_ENUM2SHORT_MAP(BonusYieldModifier, Bonus, Yield, YieldPercentMap, NonDefaultEnumMap);
	// <advc.003w> for convenience
	bool isWorldWonder() const
	{
		return GC.getInfo(getBuildingClassType()).isWorldWonder();
	}
	bool isTeamWonder() const
	{
		return GC.getInfo(getBuildingClassType()).isTeamWonder();
	}
	bool isNationalWonder() const
	{
		return GC.getInfo(getBuildingClassType()).isNationalWonder();
	}
	bool isLimited() const
	{
		return GC.getInfo(getBuildingClassType()).isLimited();
	} // </advc.003w>

	// Other

	const CvArtInfoBuilding* getArtInfo() const;
	const CvArtInfoMovie* getMovieInfo() const;
	const TCHAR* getButton() const;
	const TCHAR* getMovie() const;

	bool nameNeedsArticle() const; // advc.008e

	#if ENABLE_XML_FILE_CACHE
	void read(FDataStreamBase*);
	void write(FDataStreamBase*);
	#endif
	bool read(CvXMLLoadUtility* pXML);
	// <advc.310>
	static void setDomesticGreatGeneralRateModifierEnabled(bool b);
	static void setAreaTradeRoutesEnabled(bool b);
	static void setAreaBorderObstacleEnabled(bool b);
	// </advc.310>

protected:
	BuildingClassTypes m_eBuildingClassType;
	VictoryTypes m_eVictoryPrereq;
	EraTypes m_eFreeStartEra;
	EraTypes m_eMaxStartEra;
	TechTypes m_eObsoleteTech;
	TechTypes m_ePrereqAndTech;
	BonusTypes m_eNoBonus;
	BonusTypes m_ePowerBonus;
	BonusTypes m_eFreeBonus;
	int m_iNumFreeBonuses;
	BuildingClassTypes m_eFreeBuildingClass;
	PromotionTypes m_eFreePromotion;
	CivicOptionTypes m_eCivicOption;
	int m_iAIWeight;
	int m_iProductionCost;
	int m_iHurryCostModifier;
	int m_iHurryAngerModifier;
	int m_iAdvancedStartCost;
	int m_iAdvancedStartCostIncrease;
	int m_iMinAreaSize;
	int m_iNumCitiesPrereq;
	int m_iNumTeamsPrereq;
	int m_iUnitLevelPrereq;
	int m_iMinLatitude;
	int m_iMaxLatitude;
	int m_iGreatPeopleRateModifier;
	int m_iGreatGeneralRateModifier;
	int m_iDomesticGreatGeneralRateModifier;
	int m_iGlobalGreatPeopleRateModifier;
	int m_iAnarchyModifier;
	int m_iGoldenAgeModifier;
	int m_iGlobalHurryModifier;
	int m_iFreeExperience;
	int m_iGlobalFreeExperience;
	int m_iFoodKept;
	int m_iAirlift;
	int m_iAirModifier;
	int m_iAirUnitCapacity;
	int m_iNukeModifier;
	int m_iNukeExplosionRand;
	int m_iFreeSpecialist;
	int m_iAreaFreeSpecialist;
	int m_iGlobalFreeSpecialist;
	int m_iHappiness;
	int m_iAreaHappiness;
	int m_iGlobalHappiness;
	int m_iStateReligionHappiness;
	int m_iWorkerSpeedModifier;
	int m_iMilitaryProductionModifier;
	int m_iSpaceProductionModifier;
	int m_iGlobalSpaceProductionModifier;
	int m_iTradeRoutes;
	int m_iCoastalTradeRoutes;
	int m_iAreaTradeRoutes; // advc.310: was m_iGlobalTradeRoutes
	int m_iTradeRouteModifier;
	int m_iForeignTradeRouteModifier;
	int m_iAssetValue;
	int m_iPowerValue;
	SpecialBuildingTypes m_eSpecialBuildingType;
	AdvisorTypes m_eAdvisorType;
	ReligionTypes m_eHolyCity;
	ReligionTypes m_eReligionType;
	ReligionTypes m_eStateReligion;
	ReligionTypes m_ePrereqReligion;
	CorporationTypes m_ePrereqCorporation;
	CorporationTypes m_eFoundsCorporation;
	ReligionTypes m_eGlobalReligionCommerce;
	CorporationTypes m_eGlobalCorporationCommerce;
	BonusTypes m_ePrereqAndBonus;
	UnitClassTypes m_eGreatPeopleUnitClass;
	int m_iGreatPeopleRateChange;
	int m_iConquestProbability;
	int m_iMaintenanceModifier;
	int m_iWarWearinessModifier;
	int m_iGlobalWarWearinessModifier;
	int m_iEnemyWarWearinessModifier;
	int m_iHealRateChange;
	int m_iHealth;
	int m_iAreaHealth;
	int m_iGlobalHealth;
	int m_iGlobalPopulationChange;
	int m_iFreeTechs;
	int m_iDefenseModifier;
	int m_iBombardDefenseModifier;
	int m_iAllCityDefenseModifier;
	int m_iEspionageDefenseModifier;
	int m_iUnhealthyPopulationModifier; // K-Mod: was m_bNoUnhealthyPopulation
	MissionTypes m_eMissionType;
	VoteSourceTypes m_eVoteSourceType;

	float m_fVisibilityPriority;

	bool m_bTeamShare;
	bool m_bWater;
	bool m_bRiver;
	bool m_bPower;
	bool m_bDirtyPower;
	bool m_bAreaCleanPower;
	bool m_bAreaBorderObstacle;
	bool m_bConditional; // advc.310
	bool m_bForceTeamVoteEligible;
	bool m_bCapital;
	bool m_bGovernmentCenter;
	bool m_bGoldenAge;
	bool m_bMapCentering;
	bool m_bNoUnhappiness;
	bool m_bBuildingOnlyHealthy;
	bool m_bNeverCapture;
	bool m_bNukeImmune;
	bool m_bPrereqReligion;
	bool m_bCenterInCity;
	bool m_bStateReligion;
	bool m_bAllowsNukes;

	CvString m_szConstructSound;
	CvString m_szArtDefineTag;
	CvString m_szMovieDefineTag;

	std::vector<TechTypes> m_aePrereqAndTechs;
	std::vector<BonusTypes> m_aePrereqOrBonuses;
	// <advc.310>
	static bool m_bEnabledAreaBorderObstacle;
	static bool m_bEnabledAreaTradeRoutes;
	static bool m_bEnabledDomesticGreatGeneralRateModifier;
	// </advc.310>
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvSpecialBuildingInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvSpecialBuildingInfo : public CvInfoBase
{
	typedef CvInfoBase base_t;
public: // All the const functions are exposed to Python
	CvSpecialBuildingInfo();

	TechTypes getObsoleteTech() const { return m_eObsoleteTech; }
	TechTypes getTechPrereq() const { return m_eTechPrereq; }
	TechTypes getTechPrereqAnyone() const { return m_eTechPrereqAnyone; }

	bool isValid() const { return m_bValid; }

	DEF_INFO_ENUM_MAP(ProductionTraits, Trait, int, short, NonDefaultEnumMap);

	bool read(CvXMLLoadUtility* pXML);

protected:
	TechTypes m_eObsoleteTech;
	TechTypes m_eTechPrereq;
	TechTypes m_eTechPrereqAnyone;

	bool m_bValid;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvVoteSourceInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvVoteSourceInfo : public CvInfoBase
{
	typedef CvInfoBase base_t;
public: // The const functions are exposed to Python
	CvVoteSourceInfo();

	int getVoteInterval() const { return m_iVoteInterval; }
	SpecialistTypes getFreeSpecialist() const { return m_eFreeSpecialist; }
	CivicTypes getCivic() const { return m_eCivic; }
	const CvWString getPopupText() const; // (not exposed to python)
	const CvWString getSecretaryGeneralText() const;

	std::wstring pyGetSecretaryGeneralText() { return getSecretaryGeneralText(); }

	DEF_SHORT_INFO_ENUM_MAP(ReligionYield, Yield, YieldChangeMap);
	DEF_SHORT_INFO_ENUM_MAP(ReligionCommerce, Commerce, CommerceChangeMap);

	bool read(CvXMLLoadUtility* pXML);
	bool readPass3();

protected:
	int m_iVoteInterval;
	SpecialistTypes m_eFreeSpecialist;
	CivicTypes m_eCivic;

	CvString m_szPopupText;
	CvString m_szSecretaryGeneralText;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvVoteInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvVoteInfo :	public CvInfoBase
{
	typedef CvInfoBase base_t;
public: // All the const functions are exposed to Python
	CvVoteInfo();

	int getPopulationThreshold() const { return m_iPopulationThreshold; }
	int getStateReligionVotePercent() const { return m_iStateReligionVotePercent; }
	int getTradeRoutes() const { return m_iTradeRoutes; }
	int getMinVoters() const { return m_iMinVoters; }

	bool isSecretaryGeneral() const { return m_bSecretaryGeneral; }
	bool isVictory() const { return m_bVictory; }
	bool isFreeTrade() const { return m_bFreeTrade; }
	bool isNoNukes() const { return m_bNoNukes; }
	bool isCityVoting() const { return m_bCityVoting; }
	bool isCivVoting() const { return m_bCivVoting; }
	bool isDefensivePact() const { return m_bDefensivePact; }
	bool isOpenBorders() const { return m_bOpenBorders; }
	bool isForcePeace() const { return m_bForcePeace; }
	bool isForceNoTrade() const { return m_bForceNoTrade; }
	bool isForceWar() const { return m_bForceWar; }
	bool isAssignCity() const { return m_bAssignCity; }

	DEF_INFO_ENUM_SET(ForceCivic, Civic);
	DEF_INFO_ENUM_MAP_BOOL(VoteSourceType, VoteSource, ArrayEnumMap);

	bool read(CvXMLLoadUtility* pXML);

protected:
	int m_iPopulationThreshold;
	int m_iStateReligionVotePercent;
	int m_iTradeRoutes;
	int m_iMinVoters;

	bool m_bSecretaryGeneral;
	bool m_bVictory;
	bool m_bFreeTrade;
	bool m_bNoNukes;
	bool m_bCityVoting;
	bool m_bCivVoting;
	bool m_bDefensivePact;
	bool m_bOpenBorders;
	bool m_bForcePeace;
	bool m_bForceNoTrade;
	bool m_bForceWar;
	bool m_bAssignCity;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvProjectInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvProjectInfo : public CvInfoBase
{
	typedef CvInfoBase base_t;
public: // All const functions are exposed to Python
	CvProjectInfo();

	VictoryTypes getVictoryPrereq() const
	{
		return m_eVictoryPrereq;
	}
	TechTypes getTechPrereq() const
	{
		return m_eTechPrereq;
	}
	ProjectTypes getAnyoneProjectPrereq() const
	{
		return m_eAnyoneProjectPrereq;
	}
	int getMaxGlobalInstances() const
	{
		return m_iMaxGlobalInstances;
	}
	bool isWorldProject() const // advc.003w: Replacing global isWorldProject(ProjectTypes)
	{
		return (getMaxGlobalInstances() != -1);
	}
	int getMaxTeamInstances() const
	{
		return m_iMaxTeamInstances;
	}
	bool isTeamProject() const // advc.003w: Replacing global isTeamProject(ProjectTypes)
	{
		return (getMaxTeamInstances() != -1);
	}
	bool isLimited() const // advc.003w: Replacing global isLimitedProject(ProjectTypes)
	{
		return (isWorldProject() || isTeamProject());
	} 
	int getProductionCost() const
	{
		return m_iProductionCost;
	}
	int getNukeInterception() const
	{
		return m_iNukeInterception;
	}
	// advc/ kekm38 (note): This returns a player count (not a player id)
	int getTechShare() const
	{
		return m_iTechShare;
	}
	SpecialUnitTypes getEveryoneSpecialUnit() const
	{
		return m_eEveryoneSpecialUnit;
	}
	SpecialBuildingTypes getEveryoneSpecialBuilding() const
	{
		return m_eEveryoneSpecialBuilding;
	}
	int getVictoryDelayPercent() const
	{
		return m_iVictoryDelayPercent;
	}
	int getSuccessRate() const
	{
		return m_iSuccessRate;
	}
	bool isSpaceship() const
	{
		return m_bSpaceship;
	}
	bool isAllowsNukes() const
	{
		return m_bAllowsNukes;
	}

	const char* getMovieArtDef() const;
	const TCHAR* getCreateSound() const;
	void setCreateSound(const TCHAR* szVal);

	bool nameNeedsArticle() const;

	// Arrays access ...
	DEF_INFO_ENUM_MAP(BonusProductionModifier, Bonus, int, short, NonDefaultEnumMap);
	DEF_INFO_ENUM_MAP(VictoryThreshold, Victory, int, short, NonDefaultEnumMap);
	DEF_INFO_ENUM_MAP(VictoryMinThreshold, Victory, int, short, NonDefaultEnumMap);
	DEF_INFO_ENUM_MAP(ProjectsNeeded, Project, int, short, NonDefaultEnumMap);

	bool read(CvXMLLoadUtility* pXML);
	bool readPass2(CvXMLLoadUtility* pXML);

protected:
	VictoryTypes m_eVictoryPrereq;
	TechTypes m_eTechPrereq;
	ProjectTypes m_eAnyoneProjectPrereq;
	int m_iMaxGlobalInstances;
	int m_iMaxTeamInstances;
	int m_iProductionCost;
	int m_iNukeInterception;
	int m_iTechShare;
	SpecialUnitTypes m_eEveryoneSpecialUnit;
	SpecialBuildingTypes m_eEveryoneSpecialBuilding;
	int m_iVictoryDelayPercent;
	int m_iSuccessRate;

	bool m_bSpaceship;
	bool m_bAllowsNukes;

	CvString m_szCreateSound;
	CvString m_szMovieArtDef;
};

#endif
