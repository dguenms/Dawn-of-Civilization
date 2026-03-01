#pragma once

#ifndef CV_INFO_RANDOM_EVENT_H
#define CV_INFO_RANDOM_EVENT_H

/*  advc.003x: Cut from CvInfos.h. Just CvEventInfo and CvEventTriggerInfo.
	Will precompile these although they're used by few classes b/c they're large
	and unlikely to change (random events are the realm of XML/Python modders). */

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvEventInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvEventInfo : public CvInfoBase
{
	typedef CvInfoBase base_t;
	friend class CvXMLLoadUtility;
public: // All the const functions returning primitive types are exposed to Python
	CvEventInfo();
	~CvEventInfo();

	bool isQuest() const;
	bool isGlobal() const;
	bool isTeam() const;
	bool isCityEffect() const;
	bool isOtherPlayerCityEffect() const;
	bool isGoldToPlayer() const;
	bool isGoldenAge() const;
	bool isDeclareWar() const;
	bool isDisbandUnit() const;

	int getGold() const;
	int getRandomGold() const;
	int getEspionagePoints() const;
	int getCulture() const;
	int getTech() const;
	int getTechPercent() const;
	int getTechCostPercent() const;
	int getTechMinTurnsLeft() const;
	int getPrereqTech() const;
	int getUnitClass() const;
	int getNumUnits() const;
	int getBuildingClass() const;
	int getBuildingChange() const;
	int getHappy() const;
	int getHealth() const;
	int getHurryAnger() const;
	int getHappyTurns() const;
	int getFood() const;
	int getFoodPercent() const;
	int getFeature() const;
	int getFeatureChange() const;
	int getImprovement() const;
	int getImprovementChange() const;
	int getBonus() const;
	int getBonusChange() const;
	int getRoute() const;
	int getRouteChange() const;
	int getBonusRevealed() const;
	int getBonusGift() const;
	int getUnitExperience() const;
	int getUnitImmobileTurns() const;
	int getConvertOwnCities() const;
	int getConvertOtherCities() const;
	int getMaxNumReligions() const;
	int getOurAttitudeModifier() const;
	int getAttitudeModifier() const;
	int getTheirEnemyAttitudeModifier() const;
	int getPopulationChange() const;
	int getRevoltTurns() const;
	int getMinPillage() const;
	int getMaxPillage() const;
	int getUnitPromotion() const;
	int getFreeUnitSupport() const;
	int getInflationModifier() const;
	int getSpaceProductionModifier() const;
	int getAIValue() const;

	int getAdditionalEventChance(int i) const;
	int getAdditionalEventTime(int i) const;
	int getClearEventChance(int i) const;
	int getTechFlavorValue(int i) const;
	int getPlotExtraYield(int i) const;
	int getFreeSpecialistCount(int i) const;
	int getUnitCombatPromotion(int i) const;
	int getUnitClassPromotion(int i) const;
	const CvWString& getWorldNews(int i) const;
	int getNumWorldNews() const;

	// <advc.003t> Replacing vectors of tuples
	DEF_INFO_ENUM2SHORT_MAP(BuildingYieldChange, BuildingClass, Yield, YieldChangeMap, NonDefaultEnumMap);
	DEF_INFO_ENUM2SHORT_MAP(BuildingCommerceChange, BuildingClass, Commerce, CommerceChangeMap, NonDefaultEnumMap);
	DEF_INFO_ENUM_MAP(BuildingHappyChange, BuildingClass, int, char, NonDefaultEnumMap);
	DEF_INFO_ENUM_MAP(BuildingHealthChange, BuildingClass, int, char, NonDefaultEnumMap);
	// </advc.003t>

	const char* getPythonCallback() const;
	const char* getPythonExpireCheck() const;
	const char* getPythonCanDo() const;
	const char* getPythonHelp() const;
	const wchar* getUnitNameKey() const;
	const wchar* getQuestFailTextKey() const;
	const wchar* getOtherPlayerPopup() const;
	const wchar* getLocalInfoTextKey() const;
	#if ENABLE_XML_FILE_CACHE
	void read(FDataStreamBase* );
	void write(FDataStreamBase* );
	#endif
	bool read(CvXMLLoadUtility* pXML);
	bool readPass2(CvXMLLoadUtility* pXML);

private:
	bool m_bQuest;
	bool m_bGlobal;
	bool m_bTeam;
	bool m_bCityEffect;
	bool m_bOtherPlayerCityEffect;
	bool m_bGoldToPlayer;
	bool m_bGoldenAge;
	bool m_bDeclareWar;
	bool m_bDisbandUnit;

	int m_iGold;
	int m_iRandomGold;
	int m_iCulture;
	int m_iEspionagePoints;
	int m_iTech;
	int m_iTechPercent;
	int m_iTechCostPercent;
	int m_iTechMinTurnsLeft;
	int m_iPrereqTech;
	int m_iUnitClass;
	int m_iNumUnits;
	int m_iBuildingClass;
	int m_iBuildingChange;
	int m_iHappy;
	int m_iHealth;
	int m_iHurryAnger;
	int m_iHappyTurns;
	int m_iFood;
	int m_iFoodPercent;
	int m_iFeature;
	int m_iFeatureChange;
	int m_iImprovement;
	int m_iImprovementChange;
	int m_iBonus;
	int m_iBonusChange;
	int m_iRoute;
	int m_iRouteChange;
	int m_iBonusRevealed;
	int m_iBonusGift;
	int m_iUnitExperience;
	int m_iUnitImmobileTurns;
	int m_iConvertOwnCities;
	int m_iConvertOtherCities;
	int m_iMaxNumReligions;
	int m_iOurAttitudeModifier;
	int m_iAttitudeModifier;
	int m_iTheirEnemyAttitudeModifier;
	int m_iPopulationChange;
	int m_iRevoltTurns;
	int m_iMinPillage;
	int m_iMaxPillage;
	int m_iUnitPromotion;
	int m_iFreeUnitSupport;
	int m_iInflationModifier;
	int m_iSpaceProductionModifier;
	int m_iAIValue;

	int* m_piTechFlavorValue;
	int* m_piPlotExtraYields;
	int* m_piFreeSpecialistCount;
	int* m_piAdditionalEventChance;
	int* m_piAdditionalEventTime;
	int* m_piClearEventChance;
	int* m_piUnitCombatPromotions;
	int* m_piUnitClassPromotions;

	CvString m_szPythonCallback;
	CvString m_szPythonExpireCheck;
	CvString m_szPythonCanDo;
	CvString m_szPythonHelp;
	CvWString m_szUnitName;
	CvWString m_szOtherPlayerPopup;
	CvWString m_szQuestFailText;
	CvWString m_szLocalInfoText;
	std::vector<CvWString> m_aszWorldNews;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvEventTriggerInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvEventTriggerInfo : public CvInfoBase
{
	typedef CvInfoBase base_t;
	friend class CvXMLLoadUtility;
public: // All the const functions returning primitive types are exposed to Python
	CvEventTriggerInfo();

	int getPercentGamesActive() const;
	int getProbability() const;
	int getNumUnits() const;
	int getNumBuildings() const;
	int getNumUnitsGlobal() const;
	int getNumBuildingsGlobal() const;
	int getNumPlotsRequired() const;
	int getPlotType() const;
	int getNumReligions() const;
	int getNumCorporations() const;
	int getOtherPlayerShareBorders() const;
	int getOtherPlayerHasTech() const;
	int getCityFoodWeight() const;
	int getCivic() const;
	int getMinPopulation() const;
	int getMaxPopulation() const;
	int getMinMapLandmass() const;
	int getMinOurLandmass() const;
	int getMaxOurLandmass() const;
	int getMinDifficulty() const;
	int getAngry() const;
	int getUnhealthy() const;
	int getUnitDamagedWeight() const;
	int getUnitDistanceWeight() const;
	int getUnitExperienceWeight() const;
	int getMinTreasury() const;

	int getBuildingRequired(int i) const;
	int getNumBuildingsRequired() const;
	int getUnitRequired(int i) const;
	int getNumUnitsRequired() const;
	int getPrereqOrTechs(int i) const;
	int getNumPrereqOrTechs() const;
	int getPrereqAndTechs(int i) const;
	int getNumPrereqAndTechs() const;
	int getObsoleteTech(int i) const;
	int getNumObsoleteTechs() const;
	int getEvent(int i) const;
	int getNumEvents() const;
	int getPrereqEvent(int i) const;
	int getNumPrereqEvents() const;
	int getFeatureRequired(int i) const;
	int getNumFeaturesRequired() const;
	int getTerrainRequired(int i) const;
	int getNumTerrainsRequired() const;
	int getImprovementRequired(int i) const;
	int getNumImprovementsRequired() const;
	int getBonusRequired(int i) const;
	int getNumBonusesRequired() const;
	int getRouteRequired(int i) const;
	int getNumRoutesRequired() const;
	int getReligionRequired(int i) const;
	int getNumReligionsRequired() const;
	int getCorporationRequired(int i) const;
	int getNumCorporationsRequired() const;

	const CvWString& getText(int i) const;
	int getTextEra(int i) const;
	int getNumTexts() const;
	const CvWString& getWorldNews(int i) const;
	int getNumWorldNews() const;

	bool isSinglePlayer() const;
	bool isTeam() const;
	bool isRecurring() const;
	bool isGlobal() const;
	bool isPickPlayer() const;
	bool isOtherPlayerWar() const;
	bool isOtherPlayerHasReligion() const;
	bool isOtherPlayerHasOtherReligion() const;
	bool isOtherPlayerAI() const;
	bool isPickCity() const;
	bool isPickOtherPlayerCity() const;
	bool isShowPlot() const;
	bool isUnitsOnPlot() const;
	bool isOwnPlot() const;
	bool isPickReligion() const;
	bool isStateReligion() const;
	bool isHolyCity() const;
	bool isPickCorporation() const;
	bool isHeadquarters() const;
	bool isProbabilityUnitMultiply() const;
	bool isProbabilityBuildingMultiply() const;
	bool isPrereqEventCity() const;

	bool isPlotEventTrigger() const; // advc.003w: Moved from CvGameCoreUtils

	const char* getPythonCallback() const;
	const char* getPythonCanDo() const;
	const char* getPythonCanDoCity() const;
	const char* getPythonCanDoUnit() const;
	#if ENABLE_XML_FILE_CACHE
	void read(FDataStreamBase* );
	void write(FDataStreamBase* );
	#endif
	bool read(CvXMLLoadUtility* pXML);

private:
	int m_iPercentGamesActive;
	int m_iProbability;
	int m_iNumUnits;
	int m_iNumBuildings;
	int m_iNumUnitsGlobal;
	int m_iNumBuildingsGlobal;
	int m_iNumPlotsRequired;
	int m_iPlotType;
	int m_iNumReligions;
	int m_iNumCorporations;
	int m_iOtherPlayerShareBorders;
	int m_iOtherPlayerHasTech;
	int m_iCityFoodWeight;
	int m_iCivic;
	int m_iMinPopulation;
	int m_iMaxPopulation;
	int m_iMinMapLandmass;
	int m_iMinOurLandmass;
	int m_iMaxOurLandmass;
	int m_iMinDifficulty;
	int m_iAngry;
	int m_iUnhealthy;
	int m_iUnitDamagedWeight;
	int m_iUnitDistanceWeight;
	int m_iUnitExperienceWeight;
	int m_iMinTreasury;

	std::vector<int> m_aiUnitsRequired;
	std::vector<int> m_aiBuildingsRequired;
	std::vector<int> m_aiPrereqOrTechs;
	std::vector<int> m_aiPrereqAndTechs;
	std::vector<int> m_aiObsoleteTechs;
	std::vector<int> m_aiEvents;
	std::vector<int> m_aiPrereqEvents;
	std::vector<int> m_aiFeaturesRequired;
	std::vector<int> m_aiTerrainsRequired;
	std::vector<int> m_aiImprovementsRequired;
	std::vector<int> m_aiBonusesRequired;
	std::vector<int> m_aiRoutesRequired;
	std::vector<int> m_aiReligionsRequired;
	std::vector<int> m_aiCorporationsRequired;

	std::vector<int> m_aiTextEra;
	std::vector<CvWString> m_aszText;
	std::vector<CvWString> m_aszWorldNews;

	bool m_bSinglePlayer;
	bool m_bTeam;
	bool m_bRecurring;
	bool m_bGlobal;
	bool m_bPickPlayer;
	bool m_bOtherPlayerWar;
	bool m_bOtherPlayerHasReligion;
	bool m_bOtherPlayerHasOtherReligion;
	bool m_bOtherPlayerAI;
	bool m_bPickCity;
	bool m_bPickOtherPlayerCity;
	bool m_bShowPlot;
	bool m_bUnitsOnPlot;
	bool m_bOwnPlot;
	bool m_bPickReligion;
	bool m_bStateReligion;
	bool m_bHolyCity;
	bool m_bPickCorporation;
	bool m_bHeadquarters;
	bool m_bProbabilityUnitMultiply;
	bool m_bProbabilityBuildingMultiply;
	bool m_bPrereqEventCity;

	CvString m_szPythonCallback;
	CvString m_szPythonCanDo;
	CvString m_szPythonCanDoCity;
	CvString m_szPythonCanDoUnit;
};

#endif
