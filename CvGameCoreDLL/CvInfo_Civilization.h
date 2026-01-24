#pragma once

#ifndef CV_INFO_CIVILIZATION_H
#define CV_INFO_CIVILIZATION_H

/*  advc.003x: Cut from CvInfos.h.
	CvCivilizationInfo, CvLeaderHeadInfo, CvTraitInfo,
	CvDiplomacyInfo, CvDiplomacyResponse
	Want to precompile these. CvLeaderHeadInfo is frequently needed (by most of
	the AI code - but not only), is large and tags are added rarely. CvCivilization
	still (despite change advc.003w) plays a role in mapping building/ unit classes
	to types. */

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvCivilizationInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvCivilizationInfo : public CvInfoBase
{
	typedef CvInfoBase base_t;
public: // advc: All the const functions are exposed to Python
	CvCivilizationInfo();
	~CvCivilizationInfo();
	void reset(); // override

	int getDerivativeCiv() const;
	DllExport int getDefaultPlayerColor() const;
	ArtStyleTypes getArtStyleType() const { return m_eArtStyleType; }
	int getUnitArtStyleType() const;
	int getNumCityNames() const;
	int getNumLeaders() const;
	int getSelectionSoundScriptId() const;
	int getActionSoundScriptId() const;

	DllExport bool isAIPlayable() const;
	DllExport bool isPlayable() const;

	std::wstring pyGetShortDescription(uint uiForm) { return getShortDescription(uiForm); }
	DllExport const wchar* getShortDescription(uint uiForm = 0);
	const wchar* getShortDescriptionKey() const;
	std::wstring pyGetShortDescriptionKey() { return getShortDescriptionKey(); }

	std::wstring pyGetAdjective(uint uiForm) { return getAdjective(uiForm); }
	DllExport const wchar* getAdjective(uint uiForm = 0);
	const wchar* getAdjectiveKey() const;
	std::wstring pyGetAdjectiveKey() { return getAdjectiveKey(); }

	DllExport const TCHAR* getFlagTexture() const;
	const TCHAR* getArtDefineTag() const;

	// Array access:

	BuildingTypes getCivilizationBuildings(int i) const;
	UnitTypes getCivilizationUnits(int i) const;
	int getCivilizationFreeUnitsClass(int i) const;
	int getCivilizationInitialCivics(int i) const;

	DllExport bool isLeaders(int i) const;
	bool isCivilizationFreeBuildingClass(int i) const;
	bool isCivilizationFreeTechs(int i) const;
	bool isCivilizationDisableTechs(int i) const;

	std::string getCityNames(int i) const;

	const CvArtInfoCivilization* getArtInfo() const; // (not exposed to Python)
	const TCHAR* getButton() const;

	bool read(CvXMLLoadUtility* pXML);
	bool readPass2(CvXMLLoadUtility* pXML);
	#if ENABLE_XML_FILE_CACHE
	void read(FDataStreamBase* stream);
	void write(FDataStreamBase* stream);
	#endif

protected:
	int m_iDefaultPlayerColor;
	ArtStyleTypes m_eArtStyleType;
	int m_iUnitArtStyleType; // FlavorUnits by Impaler[WrG]
	int m_iNumCityNames;
	int m_iNumLeaders; // the number of leaders the Civ has, this is needed so that random leaders can be generated easily
	int m_iSelectionSoundScriptId;
	int m_iActionSoundScriptId;
	int m_iDerivativeCiv;

	bool m_bAIPlayable;
	bool m_bPlayable;

	CvString m_szArtDefineTag;
	CvWString m_szShortDescriptionKey;
	CvWString m_szAdjectiveKey;

	int* m_piCivilizationBuildings;
	int* m_piCivilizationUnits;
	int* m_piCivilizationFreeUnitsClass;
	int* m_piCivilizationInitialCivics;

	bool* m_pbLeaders;
	bool* m_pbCivilizationFreeBuildingClass;
	bool* m_pbCivilizationFreeTechs;
	bool* m_pbCivilizationDisableTechs;

	CvString* m_paszCityNames;

	mutable std::vector<CvWString> m_aszShortDescription;
	mutable std::vector<CvWString> m_aszAdjective;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvLeaderHeadInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvLeaderHeadInfo : public CvInfoBase
{
	typedef CvInfoBase base_t;
	friend class UWAI; // advc.104x (for applyPersonalityWeight)
public: // advc: All the const functions are exposed to Python except those added by mods
	CvLeaderHeadInfo();
	CvLeaderHeadInfo(CvLeaderHeadInfo const& kOther); // advc.xmldefault
	~CvLeaderHeadInfo();

	int getWonderConstructRand() const { return m_iWonderConstructRand; }
	int getBaseAttitude() const { return m_iBaseAttitude; }
	int getBasePeaceWeight() const { return m_iBasePeaceWeight; }
	int getPeaceWeightRand() const { return m_iPeaceWeightRand; }
	int getWarmongerRespect() const { return m_iWarmongerRespect; }
	int getEspionageWeight() const { return m_iEspionageWeight; }
	int getRefuseToTalkWarThreshold() const { return m_iRefuseToTalkWarThreshold; }
	int getNoTechTradeThreshold() const { return m_iNoTechTradeThreshold; }
	int getTechTradeKnownPercent() const { return m_iTechTradeKnownPercent; }
	int getMaxGoldTradePercent() const { return m_iMaxGoldTradePercent; }
	int getMaxGoldPerTurnTradePercent() const { return m_iMaxGoldPerTurnTradePercent; }
	// BETTER_BTS_AI_MOD, Victory Strategy AI, 03/21/10, jdog5000: START
	int getCultureVictoryWeight() const { return m_iCultureVictoryWeight; }
	int getSpaceVictoryWeight() const { return m_iSpaceVictoryWeight; }
	int getConquestVictoryWeight() const { return m_iConquestVictoryWeight; }
	int getDominationVictoryWeight() const { return m_iDominationVictoryWeight; }
	int getDiplomacyVictoryWeight() const { return m_iDiplomacyVictoryWeight; }
	// BETTER_BTS_AI_MOD: END
	int getMaxWarRand() const { return m_iMaxWarRand; }
	int getMaxWarNearbyPowerRatio() const { return m_iMaxWarNearbyPowerRatio; }
	int getMaxWarDistantPowerRatio() const { return m_iMaxWarDistantPowerRatio; }
	int getMaxWarMinAdjacentLandPercent() const { return m_iMaxWarMinAdjacentLandPercent; }
	int getLimitedWarRand() const { return m_iLimitedWarRand; }
	int getLimitedWarPowerRatio() const { return m_iLimitedWarPowerRatio; }
	int getDogpileWarRand() const { return m_iDogpileWarRand; }
	int getMakePeaceRand() const { return m_iMakePeaceRand; }
	int getDeclareWarTradeRand() const { return m_iDeclareWarTradeRand; }
	int getDemandRebukedSneakProb() const { return m_iDemandRebukedSneakProb; }
	int getDemandRebukedWarProb() const { return m_iDemandRebukedWarProb; }
	int getRazeCityProb() const { return m_iRazeCityProb; }
	int getBuildUnitProb() const { return m_iBuildUnitProb; }
	int getBaseAttackOddsChange() const { return m_iBaseAttackOddsChange; }
	int getAttackOddsChangeRand() const { return m_iAttackOddsChangeRand; }
	int getWorseRankDifferenceAttitudeChange() const { return m_iWorseRankDifferenceAttitudeChange; }
	int getBetterRankDifferenceAttitudeChange() const { return m_iBetterRankDifferenceAttitudeChange; }
	int getCloseBordersAttitudeChange() const { return m_iCloseBordersAttitudeChange; }
	int getLostWarAttitudeChange() const { return m_iLostWarAttitudeChange; }
	int getAtWarAttitudeDivisor() const { return m_iAtWarAttitudeDivisor; }
	int getAtWarAttitudeChangeLimit() const { return m_iAtWarAttitudeChangeLimit; }
	int getAtPeaceAttitudeDivisor() const { return m_iAtPeaceAttitudeDivisor; }
	int getAtPeaceAttitudeChangeLimit() const { return m_iAtPeaceAttitudeChangeLimit; }
	int getSameReligionAttitudeChange() const { return m_iSameReligionAttitudeChange; }
	int getSameReligionAttitudeDivisor() const { return m_iSameReligionAttitudeDivisor; }
	int getSameReligionAttitudeChangeLimit() const { return m_iSameReligionAttitudeChangeLimit; }
	int getDifferentReligionAttitudeChange() const { return m_iDifferentReligionAttitudeChange; }
	int getDifferentReligionAttitudeDivisor() const { return m_iDifferentReligionAttitudeDivisor; }
	int getDifferentReligionAttitudeChangeLimit() const { return m_iDifferentReligionAttitudeChangeLimit; }
	int getBonusTradeAttitudeDivisor() const { return m_iBonusTradeAttitudeDivisor; }
	int getBonusTradeAttitudeChangeLimit() const { return m_iBonusTradeAttitudeChangeLimit; }
	int getOpenBordersAttitudeDivisor() const { return m_iOpenBordersAttitudeDivisor; }
	int getOpenBordersAttitudeChangeLimit() const { return m_iOpenBordersAttitudeChangeLimit; }
	int getDefensivePactAttitudeDivisor() const { return m_iDefensivePactAttitudeDivisor; }
	int getDefensivePactAttitudeChangeLimit() const { return m_iDefensivePactAttitudeChangeLimit; }
	int getShareWarAttitudeChange() const { return m_iShareWarAttitudeChange; }
	int getShareWarAttitudeDivisor() const { return m_iShareWarAttitudeDivisor; }
	int getShareWarAttitudeChangeLimit() const { return m_iShareWarAttitudeChangeLimit; }
	int getFavoriteCivicAttitudeChange() const { return m_iFavoriteCivicAttitudeChange; }
	int getFavoriteCivicAttitudeDivisor() const { return m_iFavoriteCivicAttitudeDivisor; }
	int getFavoriteCivicAttitudeChangeLimit() const { return m_iFavoriteCivicAttitudeChangeLimit; }
	int getDemandTributeAttitudeThreshold() const { return m_iDemandTributeAttitudeThreshold; }
	int getNoGiveHelpAttitudeThreshold() const { return m_iNoGiveHelpAttitudeThreshold; }
	int getTechRefuseAttitudeThreshold() const { return m_iTechRefuseAttitudeThreshold; }
	// <advc.ctr>
	int getCityRefuseAttitudeThreshold() const { return m_iCityRefuseAttitudeThreshold; }
	int getNativeCityRefuseAttitudeThreshold() const { return m_iNativeCityRefuseAttitudeThreshold; }
	// </advc.ctr>
	int getStrategicBonusRefuseAttitudeThreshold() const { return m_iStrategicBonusRefuseAttitudeThreshold; }
	int getHappinessBonusRefuseAttitudeThreshold() const { return m_iHappinessBonusRefuseAttitudeThreshold; }
	int getHealthBonusRefuseAttitudeThreshold() const { return m_iHealthBonusRefuseAttitudeThreshold; }
	int getMapRefuseAttitudeThreshold() const { return m_iMapRefuseAttitudeThreshold; }
	int getDeclareWarRefuseAttitudeThreshold() const { return m_iDeclareWarRefuseAttitudeThreshold; }
	int getDeclareWarThemRefuseAttitudeThreshold() const { return m_iDeclareWarThemRefuseAttitudeThreshold; }
	int getStopTradingRefuseAttitudeThreshold() const { return m_iStopTradingRefuseAttitudeThreshold; }
	int getStopTradingThemRefuseAttitudeThreshold() const { return m_iStopTradingThemRefuseAttitudeThreshold; }
	int getAdoptCivicRefuseAttitudeThreshold() const { return m_iAdoptCivicRefuseAttitudeThreshold; }
	int getConvertReligionRefuseAttitudeThreshold() const { return m_iConvertReligionRefuseAttitudeThreshold; }
	int getOpenBordersRefuseAttitudeThreshold() const { return m_iOpenBordersRefuseAttitudeThreshold; }
	int getDefensivePactRefuseAttitudeThreshold() const { return m_iDefensivePactRefuseAttitudeThreshold; }
	int getPermanentAllianceRefuseAttitudeThreshold() const { return m_iPermanentAllianceRefuseAttitudeThreshold; }
	int getVassalRefuseAttitudeThreshold() const { return m_iVassalRefuseAttitudeThreshold; }
	int getVassalPowerModifier() const { return m_iVassalPowerModifier; }
	CivicTypes getFavoriteCivic() const { return m_eFavoriteCivic; }
	ReligionTypes getFavoriteReligion() const { return m_eFavoriteReligion; }
	int getFreedomAppreciation() const { return m_iFreedomAppreciation; }
	int getLoveOfPeace() const { return m_iLoveOfPeace; } // advc.104

	const TCHAR* getArtDefineTag() const;

	// Array access:

	bool hasTrait(int i) const;

	int getFlavorValue(int i) const;
	int getContactRand(int i) const;
	int getContactDelay(int i) const;
	int getMemoryDecayRand(int i) const;
	int getMemoryAttitudePercent(int i) const;
	int getNoWarAttitudeProb(int i) const;
	int getUnitAIWeightModifier(int i) const;
	int getImprovementWeightModifier(int i) const;
	int getDiploPeaceIntroMusicScriptIds(int i) const;
	int getDiploPeaceMusicScriptIds(int i) const;
	int getDiploWarIntroMusicScriptIds(int i) const;
	int getDiploWarMusicScriptIds(int i) const;

	// (not exposed to Python)
	DllExport const CvArtInfoLeaderhead* getArtInfo() const;
	const TCHAR* getLeaderHead() const;
	const TCHAR* getButton() const;
	#if ENABLE_XML_FILE_CACHE
	void read(FDataStreamBase* stream);
	void write(FDataStreamBase* stream);
	#endif
	bool read(CvXMLLoadUtility* pXML);

protected:
	/*	advc.xmldefault (note): The copy-ctor relies on m_iWonderConstructRand
		being the first data member */
	/*	Also note: Data members added here should also be added to the list
		in UWAI::applyPersonalityWeight */
	int m_iWonderConstructRand;
	int m_iBaseAttitude;
	int m_iBasePeaceWeight;
	int m_iPeaceWeightRand;
	int m_iWarmongerRespect;
	int m_iEspionageWeight;
	int m_iRefuseToTalkWarThreshold;
	int m_iNoTechTradeThreshold;
	int m_iTechTradeKnownPercent;
	int m_iMaxGoldTradePercent;
	int m_iMaxGoldPerTurnTradePercent;
	// BETTER_BTS_AI_MOD; Victory Strategy AI, 03/21/10, jdog5000: START
	int m_iCultureVictoryWeight;
	int m_iSpaceVictoryWeight;
	int m_iConquestVictoryWeight;
	int m_iDominationVictoryWeight;
	int m_iDiplomacyVictoryWeight;
	// BETTER_BTS_AI_MOD: END
	int m_iMaxWarRand;
	int m_iMaxWarNearbyPowerRatio;
	int m_iMaxWarDistantPowerRatio;
	int m_iMaxWarMinAdjacentLandPercent;
	int m_iLimitedWarRand;
	int m_iLimitedWarPowerRatio;
	int m_iDogpileWarRand;
	int m_iMakePeaceRand;
	int m_iDeclareWarTradeRand;
	int m_iDemandRebukedSneakProb;
	int m_iDemandRebukedWarProb;
	int m_iRazeCityProb;
	int m_iBuildUnitProb;
	int m_iBaseAttackOddsChange;
	int m_iAttackOddsChangeRand;
	int m_iWorseRankDifferenceAttitudeChange;
	int m_iBetterRankDifferenceAttitudeChange;
	int m_iCloseBordersAttitudeChange;
	int m_iLostWarAttitudeChange;
	int m_iAtWarAttitudeDivisor;
	int m_iAtWarAttitudeChangeLimit;
	int m_iAtPeaceAttitudeDivisor;
	int m_iAtPeaceAttitudeChangeLimit;
	int m_iSameReligionAttitudeChange;
	int m_iSameReligionAttitudeDivisor;
	int m_iSameReligionAttitudeChangeLimit;
	int m_iDifferentReligionAttitudeChange;
	int m_iDifferentReligionAttitudeDivisor;
	int m_iDifferentReligionAttitudeChangeLimit;
	int m_iBonusTradeAttitudeDivisor;
	int m_iBonusTradeAttitudeChangeLimit;
	int m_iOpenBordersAttitudeDivisor;
	int m_iOpenBordersAttitudeChangeLimit;
	int m_iDefensivePactAttitudeDivisor;
	int m_iDefensivePactAttitudeChangeLimit;
	int m_iShareWarAttitudeChange;
	int m_iShareWarAttitudeDivisor;
	int m_iShareWarAttitudeChangeLimit;
	int m_iFavoriteCivicAttitudeChange;
	int m_iFavoriteCivicAttitudeDivisor;
	int m_iFavoriteCivicAttitudeChangeLimit;
	int m_iDemandTributeAttitudeThreshold;
	int m_iNoGiveHelpAttitudeThreshold;
	int m_iTechRefuseAttitudeThreshold;
	// <advc.ctr>
	int m_iCityRefuseAttitudeThreshold;
	int m_iNativeCityRefuseAttitudeThreshold; // </advc.ctr>
	int m_iStrategicBonusRefuseAttitudeThreshold;
	int m_iHappinessBonusRefuseAttitudeThreshold;
	int m_iHealthBonusRefuseAttitudeThreshold;
	int m_iMapRefuseAttitudeThreshold;
	int m_iDeclareWarRefuseAttitudeThreshold;
	int m_iDeclareWarThemRefuseAttitudeThreshold;
	int m_iStopTradingRefuseAttitudeThreshold;
	int m_iStopTradingThemRefuseAttitudeThreshold;
	int m_iAdoptCivicRefuseAttitudeThreshold;
	int m_iConvertReligionRefuseAttitudeThreshold;
	int m_iOpenBordersRefuseAttitudeThreshold;
	int m_iDefensivePactRefuseAttitudeThreshold;
	int m_iPermanentAllianceRefuseAttitudeThreshold;
	int m_iVassalRefuseAttitudeThreshold;
	int m_iVassalPowerModifier;
	int m_iFreedomAppreciation;
	int m_iLoveOfPeace; // advc.104
	CivicTypes m_eFavoriteCivic;
	ReligionTypes m_eFavoriteReligion;

	CvString m_szArtDefineTag;

	bool* m_pbTraits;

	/*	Caveat: UWAI::applyPersonalityWeight depends on these being implemented
		as int arrays */
	int* m_piFlavorValue;
	int* m_piContactRand;
	int* m_piContactDelay;
	int* m_piMemoryDecayRand;
	int* m_piMemoryAttitudePercent;
	int* m_piNoWarAttitudeProb;
	int* m_piUnitAIWeightModifier;
	int* m_piImprovementWeightModifier;
	int* m_piDiploPeaceIntroMusicScriptIds;
	int* m_piDiploPeaceMusicScriptIds;
	int* m_piDiploWarIntroMusicScriptIds;
	int* m_piDiploWarMusicScriptIds;
	// <advc.xmldefault>
	static CvXMLLoadUtility* m_pXML;
	static void GetChildXmlValByName(int& r, TCHAR const* szName, int iDefault = MIN_INT);
	// </advc.xmldefault>
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvTraitInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvTraitInfo : /* <advc.tag> */ public CvXMLInfo
{
	typedef CvXMLInfo base_t;
protected:
	void addElements(ElementList& kElements) const
	{
		base_t::addElements(kElements);
		kElements.addInt(FREE_CITY_CULTURE, "FreeCityCulture");
	}
public:
	enum IntElementTypes
	{
		FREE_CITY_CULTURE = CvXMLInfo::NUM_INT_ELEMENT_TYPES, // advc.908b
		NUM_INT_ELEMENT_TYPES
	};
	int get(IntElementTypes e) const
	{
		return base_t::get(static_cast<base_t::IntElementTypes>(e));
	} // </advc.tag>

	// advc: All the const functions are exposed to Python except those added by mods
	CvTraitInfo();
	~CvTraitInfo();

	int getHealth() const;
	int getHappiness() const;
	int getMaxAnarchy() const;
	int getUpkeepModifier() const;
	int getLevelExperienceModifier() const;
	int getGreatPeopleRateModifier() const;
	int getGreatGeneralRateModifier() const;
	int getDomesticGreatGeneralRateModifier() const;
	int getMaxGlobalBuildingProductionModifier() const;
	int getMaxTeamBuildingProductionModifier() const;
	int getMaxPlayerBuildingProductionModifier() const;

	const TCHAR* getShortDescription() const;
	void setShortDescription(const TCHAR* szVal);

	// Array access:

	int getExtraYieldThreshold(int i) const;
	// advc.908a:
	DEF_SHORT_INFO_ENUM_MAP(ExtraYieldNaturalThreshold, Yield, YieldChangeMap);
	int getTradeYieldModifier(int i) const;
	int getCommerceChange(int i) const;
	int getCommerceModifier(int i) const;

	bool isFreePromotion(int i) const; // advc.003t: Return type was int
	bool isAnyFreePromotion() const { return (m_pabFreePromotion != NULL); } // advc.003t
	bool isFreePromotionUnitCombat(int i) const; // advc.003t: Return type was int

	bool read(CvXMLLoadUtility* pXML);

protected:
	int m_iHealth;
	int m_iHappiness;
	int m_iMaxAnarchy;
	int m_iUpkeepModifier;
	int m_iLevelExperienceModifier;
	int m_iGreatPeopleRateModifier;
	int m_iGreatGeneralRateModifier;
	int m_iDomesticGreatGeneralRateModifier;
	int m_iMaxGlobalBuildingProductionModifier;
	int m_iMaxTeamBuildingProductionModifier;
	int m_iMaxPlayerBuildingProductionModifier;

	CvString m_szShortDescription;

	int* m_paiExtraYieldThreshold;
	int* m_paiTradeYieldModifier;
	int* m_paiCommerceChange;
	int* m_paiCommerceModifier;

	bool* m_pabFreePromotion;
	bool* m_pabFreePromotionUnitCombat;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvDiplomacyResponse (helper for DiplomacyInfo)
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvDiplomacyResponse
{
public: // advc: All the const functions are exposed to Python (some const qualifiers added by me)
	CvDiplomacyResponse();
	~CvDiplomacyResponse(); // advc: was virtual

	int getNumDiplomacyText() const;
	// advc.003j: Disabled the unused setters and bool* getters
	//void setNumDiplomacyText(int i);

	bool getCivilizationTypes(int i) const;
	//bool* getCivilizationTypes() const;
	//void setCivilizationTypes(int i, bool bVal);

	bool getLeaderHeadTypes(int i) const;
	//bool* getLeaderHeadTypes() const;
	//void setLeaderHeadTypes(int i, bool bVal);

	bool getAttitudeTypes(int i) const;
	//bool* getAttitudeTypes() const;
	//void setAttitudeTypes(int i, bool bVal);

	bool getDiplomacyPowerTypes(int i) const;
	//bool* getDiplomacyPowerTypes() const;
	//void setDiplomacyPowerTypes(int i, bool bVal);

	const TCHAR* getDiplomacyText(int i) const;
	const CvString* getDiplomacyText() const;
	void setDiplomacyText(int i, CvString szText);
	#if ENABLE_XML_FILE_CACHE
	void read(FDataStreamBase* stream);
	void write(FDataStreamBase* stream);
	#endif
	bool read(CvXMLLoadUtility* pXML);

protected:
	int m_iNumDiplomacyText;
	bool* m_pbCivilizationTypes;
	bool* m_pbLeaderHeadTypes;
	bool* m_pbAttitudeTypes;
	bool* m_pbDiplomacyPowerTypes;
	CvString* m_paszDiplomacyText;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvDiplomacyInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvDiplomacyInfo : public CvInfoBase
{
friend class CvXMLLoadUtility;
public: // advc: All the const functions are exposed to Python
	~CvDiplomacyInfo();
	//void uninit(); // advc: Merged into destructor

	CvDiplomacyResponse const& getResponse(int iNum) const;
	// advc.705: (underscore avoids ambiguity in Python export)
	CvDiplomacyResponse& getResponse_(int iNum);
	int getNumResponses() const;

	bool getCivilizationTypes(int i, int j) const;
	bool getLeaderHeadTypes(int i, int j) const;
	bool getAttitudeTypes(int i, int j) const;
	bool getDiplomacyPowerTypes(int i, int j) const;

	int getNumDiplomacyText(int i) const;

	const TCHAR* getDiplomacyText(int i, int j) const;
	#if ENABLE_XML_FILE_CACHE
	void read(FDataStreamBase* stream);
	void write(FDataStreamBase* stream);
	#endif
	bool read(CvXMLLoadUtility* pXML);

protected:
	std::vector<CvDiplomacyResponse*> m_pResponses;
};

#endif
