// advc.003x: Cut from CvInfos.cpp

#include "CvGameCoreDLL.h"
#include "CvInfo_Civics.h"
#include "CvXMLLoadUtility.h"


CvCivicInfo::CvCivicInfo() :
m_eCivicOptionType(NO_CIVICOPTION),
m_iAnarchyLength(0),
m_iUpkeep(0),
m_iAIWeight(0),
m_bCanAlwaysForce(false), // advc.132
m_iGreatPeopleRateModifier(0),
m_iGreatGeneralRateModifier(0),
m_iDomesticGreatGeneralRateModifier(0),
m_iStateReligionGreatPeopleRateModifier(0),
m_iDistanceMaintenanceModifier(0),
m_iColonyMaintenanceModifier(0), // advc.912g
m_iNumCitiesMaintenanceModifier(0),
m_iCorporationMaintenanceModifier(0),
m_iExtraHealth(0),
m_iExtraHappiness(0), // K-Mod
m_iFreeExperience(0),
m_iWorkerSpeedModifier(0),
m_iImprovementUpgradeRateModifier(0),
m_iMilitaryProductionModifier(0),
m_iBaseFreeUnits(0),
m_iBaseFreeMilitaryUnits(0),
m_iFreeUnitsPopulationPercent(0),
m_iFreeMilitaryUnitsPopulationPercent(0),
m_iGoldPerUnit(0),
m_iGoldPerMilitaryUnit(0),
m_iHappyPerMilitaryUnit(0),
m_iLuxuryModifier(0), // advc.912c
m_iLargestCityHappiness(0),
m_iWarWearinessModifier(0),
m_iFreeSpecialist(0),
m_iTradeRoutes(0),
m_eTechPrereq(NO_TECH),
m_iCivicPercentAnger(0),
m_iMaxConscript(0),
m_iStateReligionHappiness(0),
m_iNonStateReligionHappiness(0),
m_iStateReligionUnitProductionModifier(0),
m_iStateReligionBuildingProductionModifier(0),
m_iStateReligionFreeExperience(0),
m_iExpInBorderModifier(0),
m_iLevelExperienceModifier(0), // doc
m_iCorporationUnhappinessModifier(0), // doc
m_iProcessModifier(0), // doc
m_iFoodProductionModifier(0), // doc
m_iWonderProductionModifier(0), // doc
m_iCorporationCommerceModifier(0), // doc
m_iDefensivePactTradeModifier(0), // doc
m_iVassalTradeModifier(0), // doc
m_iShrineIncomeLimitChange(0), // doc
m_iCaptureGoldModifier(0), // doc
m_iCapitalBuildingProductionModifier(0), // doc
m_iOccupationTimeChange(0), // doc
m_bMilitaryFoodProduction(false),
//m_bNoUnhealthyPopulation(false),
m_iUnhealthyPopulationModifier(0), // K-Mod
m_bBuildingOnlyHealthy(false),
m_bNoForeignTrade(false),
m_bNoCorporations(false),
m_bNoForeignCorporations(false),
m_bStateReligion(false),
m_bNoNonStateReligionSpread(false),
m_bNoForeignTradeModifier(false), // doc
m_bSlavery(false), // doc
m_bNoSlavery(false), // doc
m_bColonialSlavery(false), // doc
m_bNoStateReligionAnarchy(false), // doc
m_bFreeImprovementUpgrade(false), // doc
m_piYieldModifier(NULL),
m_piCapitalYieldModifier(NULL),
m_piTradeYieldModifier(NULL),
m_piCommerceModifier(NULL),
m_piCapitalCommerceModifier(NULL),
m_piSpecialistExtraCommerce(NULL),
m_piStateReligionBuildingYield(NULL), // doc
m_piSpecialistExtraYield(NULL), // doc
m_piSpecialistCount(NULL), // doc
m_paiBuildingHappinessChanges(NULL),
m_paiBuildingHealthChanges(NULL),
m_paiFeatureHappinessChanges(NULL),
m_paiDomainExperienceModifiers(NULL), // doc
m_paiBuildingProductionModifiers(NULL), // doc
m_pabHurry(NULL),
m_pabSpecialBuildingNotRequired(NULL),
m_pabSpecialistValid(NULL),
m_ppiImprovementYieldChanges(NULL)
{}

CvCivicInfo::~CvCivicInfo()
{
	SAFE_DELETE_ARRAY(m_piYieldModifier);
	SAFE_DELETE_ARRAY(m_piCapitalYieldModifier);
	SAFE_DELETE_ARRAY(m_piTradeYieldModifier);
	SAFE_DELETE_ARRAY(m_piCommerceModifier);
	SAFE_DELETE_ARRAY(m_piCapitalCommerceModifier);
	SAFE_DELETE_ARRAY(m_piSpecialistExtraCommerce);
	SAFE_DELETE_ARRAY(m_piStateReligionBuildingYield); // doc
	SAFE_DELETE_ARRAY(m_piSpecialistExtraYield); // doc
	SAFE_DELETE_ARRAY(m_piSpecialistCount); // doc
	SAFE_DELETE_ARRAY(m_paiBuildingHappinessChanges);
	SAFE_DELETE_ARRAY(m_paiBuildingHealthChanges);
	SAFE_DELETE_ARRAY(m_paiFeatureHappinessChanges);
	SAFE_DELETE_ARRAY(m_paiDomainExperienceModifiers); // doc
	SAFE_DELETE_ARRAY(m_paiBuildingProductionModifiers); // doc
	SAFE_DELETE_ARRAY(m_pabHurry);
	SAFE_DELETE_ARRAY(m_pabSpecialBuildingNotRequired);
	SAFE_DELETE_ARRAY(m_pabSpecialistValid);
	if (m_ppiImprovementYieldChanges != NULL)
	{
		for (int iI = 0; iI < GC.getNumImprovementInfos(); iI++)
			SAFE_DELETE_ARRAY(m_ppiImprovementYieldChanges[iI]);
		SAFE_DELETE_ARRAY(m_ppiImprovementYieldChanges);
	}
	// doc
	if (m_ppiSpecialistTypeExtraYields != NULL)
	{
		FOR_EACH_ENUM(Specialist)
		{
			SAFE_DELETE_ARRAY(m_ppiSpecialistTypeExtraYields[eLoopSpecialist]);
		}
		SAFE_DELETE_ARRAY(m_ppiSpecialistTypeExtraYields);
	}
}

const wchar* CvCivicInfo::getWeLoveTheKing()
{
	return m_szWeLoveTheKingKey;
}

int CvCivicInfo::getYieldModifier(int i) const
{
	FAssertBounds(0, NUM_YIELD_TYPES, i);
	return m_piYieldModifier ? m_piYieldModifier[i] : 0; // advc.003t
}

int* CvCivicInfo::getYieldModifierArray() const
{
	return m_piYieldModifier;
}

int CvCivicInfo::getCapitalYieldModifier(int i) const
{
	FAssertBounds(0, NUM_YIELD_TYPES, i);
	return m_piCapitalYieldModifier ? m_piCapitalYieldModifier[i] : 0; // advc.003t
}

int* CvCivicInfo::getCapitalYieldModifierArray() const
{
	return m_piCapitalYieldModifier;
}

int CvCivicInfo::getTradeYieldModifier(int i) const
{
	FAssertBounds(0, NUM_YIELD_TYPES, i);
	return m_piTradeYieldModifier ? m_piTradeYieldModifier[i] : 0; // advc.003t
}

int* CvCivicInfo::getTradeYieldModifierArray() const
{
	return m_piTradeYieldModifier;
}

int CvCivicInfo::getCommerceModifier(int i) const
{
	FAssertBounds(0, NUM_COMMERCE_TYPES, i);
	return m_piCommerceModifier ? m_piCommerceModifier[i] : 0; // advc.003t
}

int* CvCivicInfo::getCommerceModifierArray() const
{
	return m_piCommerceModifier;
}

int CvCivicInfo::getCapitalCommerceModifier(int i) const
{
	FAssertBounds(0, NUM_COMMERCE_TYPES, i);
	return m_piCapitalCommerceModifier ? m_piCapitalCommerceModifier[i] : 0; // advc.003t
}

int* CvCivicInfo::getCapitalCommerceModifierArray() const
{
	return m_piCapitalCommerceModifier;
}

int CvCivicInfo::getSpecialistExtraCommerce(int i) const
{
	FAssertBounds(0, NUM_COMMERCE_TYPES, i);
	return m_piSpecialistExtraCommerce ? m_piSpecialistExtraCommerce[i] : 0; // advc.003t
}

int* CvCivicInfo::getSpecialistExtraCommerceArray() const
{
	return m_piSpecialistExtraCommerce;
}

int CvCivicInfo::getBuildingHappinessChanges(int i) const
{
	FAssertBounds(0, GC.getNumBuildingClassInfos(), i);
	return m_paiBuildingHappinessChanges ? m_paiBuildingHappinessChanges[i] : 0; // advc.003t
}

int CvCivicInfo::getBuildingHealthChanges(int i) const
{
	FAssertBounds(0, GC.getNumBuildingClassInfos(), i);
	return m_paiBuildingHealthChanges ? m_paiBuildingHealthChanges[i] : 0; // advc.003t
}

int CvCivicInfo::getFeatureHappinessChanges(int i) const
{
	FAssertBounds(0, GC.getNumFeatureInfos(), i);
	return m_paiFeatureHappinessChanges ? m_paiFeatureHappinessChanges[i] : 0; // advc.003t
}

bool CvCivicInfo::isHurry(int i) const
{
	FAssertBounds(0, GC.getNumHurryInfos(), i);
	return m_pabHurry ? m_pabHurry[i] : false;
}

bool CvCivicInfo::isSpecialBuildingNotRequired(int i) const
{
	FAssertBounds(0, GC.getNumSpecialBuildingInfos(), i);
	return m_pabSpecialBuildingNotRequired ? m_pabSpecialBuildingNotRequired[i] : false;
}

bool CvCivicInfo::isSpecialistValid(int i) const
{
	FAssertBounds(0, GC.getNumSpecialistInfos(), i);
	return m_pabSpecialistValid ? m_pabSpecialistValid[i] : false;
}

int CvCivicInfo::getImprovementYieldChanges(int i, int j) const
{
	FAssertBounds(0, GC.getNumImprovementInfos(), i);
	FAssertBounds(0, NUM_YIELD_TYPES, j);
	return m_ppiImprovementYieldChanges[i][j];
}

// doc
int CvCivicInfo::getSpecialistTypeExtraYield(SpecialistTypes eSpecialist, YieldTypes eYield) const
{
	FAssertBounds(0, GC.getNumSpecialistInfos(), eSpecialist);
	FAssertBounds(0, NUM_YIELD_TYPES, eYield);
	return m_ppiSpecialistTypeExtraYields[eSpecialist][eYield];
}

#if ENABLE_XML_FILE_CACHE
void CvCivicInfo::read(FDataStreamBase* stream)
{
	base_t::read(stream);
	uint uiFlag=0;
	stream->Read(&uiFlag);

	stream->Read((int*)&m_eCivicOptionType);
	stream->Read(&m_iAnarchyLength);
	stream->Read(&m_iUpkeep);
	stream->Read(&m_iAIWeight);
	stream->Read(&m_bCanAlwaysForce); // advc.132
	stream->Read(&m_iGreatPeopleRateModifier);
	stream->Read(&m_iGreatGeneralRateModifier);
	stream->Read(&m_iDomesticGreatGeneralRateModifier);
	stream->Read(&m_iStateReligionGreatPeopleRateModifier);
	stream->Read(&m_iDistanceMaintenanceModifier);
	stream->Read(&m_iColonyMaintenanceModifier); // advc.912g
	stream->Read(&m_iNumCitiesMaintenanceModifier);
	stream->Read(&m_iCorporationMaintenanceModifier);
	stream->Read(&m_iExtraHealth);
	stream->Read(&m_iExtraHappiness);
	stream->Read(&m_iFreeExperience);
	stream->Read(&m_iWorkerSpeedModifier);
	stream->Read(&m_iImprovementUpgradeRateModifier);
	stream->Read(&m_iMilitaryProductionModifier);
	stream->Read(&m_iBaseFreeUnits);
	stream->Read(&m_iBaseFreeMilitaryUnits);
	stream->Read(&m_iFreeUnitsPopulationPercent);
	stream->Read(&m_iFreeMilitaryUnitsPopulationPercent);
	stream->Read(&m_iGoldPerUnit);
	stream->Read(&m_iGoldPerMilitaryUnit);
	stream->Read(&m_iHappyPerMilitaryUnit);
	stream->Read(&m_iLuxuryModifier); // advc.912c
	stream->Read(&m_iLargestCityHappiness);
	stream->Read(&m_iWarWearinessModifier);
	stream->Read(&m_iFreeSpecialist);
	stream->Read(&m_iTradeRoutes);
	stream->Read((int*)&m_eTechPrereq);
	stream->Read(&m_iCivicPercentAnger);
	stream->Read(&m_iMaxConscript);
	stream->Read(&m_iStateReligionHappiness);
	stream->Read(&m_iNonStateReligionHappiness);
	stream->Read(&m_iStateReligionUnitProductionModifier);
	stream->Read(&m_iStateReligionBuildingProductionModifier);
	stream->Read(&m_iStateReligionFreeExperience);
	stream->Read(&m_iExpInBorderModifier);
	stream->Read(&m_iLevelExperienceModifier); // doc
	stream->Read(&m_iCorporationUnhappinessModifier); // doc
	stream->Read(&m_iProcessModifier); // doc
	stream->Read(&m_iFoodProductionModifier); // doc
	stream->Read(&m_iWonderProductionModifier); // doc
	stream->Read(&m_iCorporationCommerceModifier); // doc
	stream->Read(&m_iDefensivePactTradeModifier); // doc
	stream->Read(&m_iVassalTradeModifier); // doc
	stream->Read(&m_iShrineIncomeLimitChange); // doc
	stream->Read(&m_iCaptureGoldModifier); // doc
	stream->Read(&m_iCapitalBuildingProductionModifier); // doc
	stream->Read(&m_iOccupationTimeChange); // doc
	stream->Read(&m_bMilitaryFoodProduction);
	//stream->Read(&m_bNoUnhealthyPopulation);
	stream->Read(&m_iUnhealthyPopulationModifier); // K-Mod
	stream->Read(&m_bBuildingOnlyHealthy);
	stream->Read(&m_bNoForeignTrade);
	stream->Read(&m_bNoCorporations);
	stream->Read(&m_bNoForeignCorporations);
	stream->Read(&m_bStateReligion);
	stream->Read(&m_bNoNonStateReligionSpread);
	stream->Read(&m_bNoForeignTradeModifier); // doc
	stream->Read(&m_bSlavery); // doc
	stream->Read(&m_bNoSlavery); // doc
	stream->Read(&m_bColonialSlavery); // doc
	stream->Read(&m_bNoStateReligionAnarchy); // doc
	stream->Read(&m_bFreeImprovementUpgrade); // doc
	SAFE_DELETE_ARRAY(m_piYieldModifier);
	m_piYieldModifier = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_piYieldModifier);
	SAFE_DELETE_ARRAY(m_piCapitalYieldModifier);
	m_piCapitalYieldModifier = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_piCapitalYieldModifier);
	SAFE_DELETE_ARRAY(m_piTradeYieldModifier);
	m_piTradeYieldModifier = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_piTradeYieldModifier);
	SAFE_DELETE_ARRAY(m_piCommerceModifier);
	m_piCommerceModifier = new int[NUM_COMMERCE_TYPES];
	stream->Read(NUM_COMMERCE_TYPES, m_piCommerceModifier);
	SAFE_DELETE_ARRAY(m_piCapitalCommerceModifier);
	m_piCapitalCommerceModifier = new int[NUM_COMMERCE_TYPES];
	stream->Read(NUM_COMMERCE_TYPES, m_piCapitalCommerceModifier);
	SAFE_DELETE_ARRAY(m_piSpecialistExtraCommerce);
	m_piSpecialistExtraCommerce = new int[NUM_COMMERCE_TYPES];
	stream->Read(NUM_COMMERCE_TYPES, m_piSpecialistExtraCommerce);

	// doc
	SAFE_DELETE_ARRAY(m_piStateReligionBuildingYield);
	m_piSpecialistExtraCommerce = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_piStateReligionBuildingYield);
	SAFE_DELETE_ARRAY(m_piSpecialistExtraYield);
	m_piSpecialistExtraYield = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_piSpecialistExtraYield);
	SAFE_DELETE_ARRAY(m_piSpecialistCount);
	m_piSpecialistCount = new int[GC.getNumSpecialistInfos()];
	stream->Read(GC.getNumSpecialistInfos(), m_piSpecialistCount);

	SAFE_DELETE_ARRAY(m_paiBuildingHappinessChanges);
	m_paiBuildingHappinessChanges = new int[GC.getNumBuildingClassInfos()];
	stream->Read(GC.getNumBuildingClassInfos(), m_paiBuildingHappinessChanges);
	SAFE_DELETE_ARRAY(m_paiBuildingHealthChanges);
	m_paiBuildingHealthChanges = new int[GC.getNumBuildingClassInfos()];
	stream->Read(GC.getNumBuildingClassInfos(), m_paiBuildingHealthChanges);
	SAFE_DELETE_ARRAY(m_paiFeatureHappinessChanges);
	m_paiFeatureHappinessChanges = new int[GC.getNumFeatureInfos()];
	stream->Read(GC.getNumFeatureInfos(), m_paiFeatureHappinessChanges);

	// doc
	SAFE_DELETE_ARRAY(m_paiDomainExperienceModifiers);
	m_paiDomainExperienceModifiers = new int[NUM_DOMAIN_TYPES];
	stream.Read(NUM_DOMAIN_TYPES, m_paiDomainExperienceModifiers);
	SAFE_DELETE_ARRAY(m_paiBuildingProductionModifiers);
	m_paiBuildingProductionModifiers = new int[GC.getNumBuildingClassInfos()];
	stream.Read(GC.getNumBuildingClassInfos(), m_paiBuildingProductionModifiers);

	SAFE_DELETE_ARRAY(m_pabHurry);
	m_pabHurry = new bool[GC.getNumHurryInfos()];
	stream->Read(GC.getNumHurryInfos(), m_pabHurry);
	SAFE_DELETE_ARRAY(m_pabSpecialBuildingNotRequired);
	m_pabSpecialBuildingNotRequired = new bool[GC.getNumSpecialBuildingInfos()];
	stream->Read(GC.getNumSpecialBuildingInfos(), m_pabSpecialBuildingNotRequired);
	SAFE_DELETE_ARRAY(m_pabSpecialistValid);
	m_pabSpecialistValid = new bool[GC.getNumSpecialistInfos()];
	stream->Read(GC.getNumSpecialistInfos(), m_pabSpecialistValid);

	if (m_ppiImprovementYieldChanges != NULL)
	{
		for(int i = 0; i < GC.getNumImprovementInfos(); i++)
			SAFE_DELETE_ARRAY(m_ppiImprovementYieldChanges[i]);
		SAFE_DELETE_ARRAY(m_ppiImprovementYieldChanges);
	}
	m_ppiImprovementYieldChanges = new int*[GC.getNumImprovementInfos()];
	for(int i = 0;i < GC.getNumImprovementInfos(); i++)
	{
		m_ppiImprovementYieldChanges[i]  = new int[NUM_YIELD_TYPES];
		stream->Read(NUM_YIELD_TYPES, m_ppiImprovementYieldChanges[i]);
	}

	// doc
	if (m_ppiSpecialistTypeExtraYields != NULL)
	{
		FOR_EACH_ENUM(Specialist)
		{
			SAFE_DELETE_ARRAY(m_ppiSpecialistTypeExtraYields[eLoopSpecialist]);
		}
		SAFE_DELETE_ARRAY(m_ppiSpecialistTypeExtraYields);
	}
	m_ppiSpecialistTypeExtraYields = new int* [GC.getNumSpecialistInfos()];
	FOR_EACH_ENUM(Specialist)
	{
		m_ppiSpecialistTypeExtraYields[eLoopSpecialist] = new int[NUM_YIELD_TYPES];
		stream->Read(NUM_YIELD_TYPES, m_ppiSpecialistTypeExtraYields[eLoopSpecialist]);
	}

	stream->ReadString(m_szWeLoveTheKingKey);
}

void CvCivicInfo::write(FDataStreamBase* stream)
{
	base_t::write(stream);
	uint uiFlag = 0;
	stream->Write(uiFlag);

	stream->Write(m_eCivicOptionType);
	stream->Write(m_iAnarchyLength);
	stream->Write(m_iUpkeep);
	stream->Write(m_iAIWeight);
	stream->Write(m_bCanAlwaysForce); // advc.132
	stream->Write(m_iGreatPeopleRateModifier);
	stream->Write(m_iGreatGeneralRateModifier);
	stream->Write(m_iDomesticGreatGeneralRateModifier);
	stream->Write(m_iStateReligionGreatPeopleRateModifier);
	stream->Write(m_iDistanceMaintenanceModifier);
	stream->Write(m_iColonyMaintenanceModifier); // advc.912g
	stream->Write(m_iNumCitiesMaintenanceModifier);
	stream->Write(m_iCorporationMaintenanceModifier);
	stream->Write(m_iExtraHealth);
	stream->Write(m_iExtraHappiness); // K-Mod
	stream->Write(m_iFreeExperience);
	stream->Write(m_iWorkerSpeedModifier);
	stream->Write(m_iImprovementUpgradeRateModifier);
	stream->Write(m_iMilitaryProductionModifier);
	stream->Write(m_iBaseFreeUnits);
	stream->Write(m_iBaseFreeMilitaryUnits);
	stream->Write(m_iFreeUnitsPopulationPercent);
	stream->Write(m_iFreeMilitaryUnitsPopulationPercent);
	stream->Write(m_iGoldPerUnit);
	stream->Write(m_iGoldPerMilitaryUnit);
	stream->Write(m_iHappyPerMilitaryUnit);
	stream->Write(m_iLuxuryModifier); // advc.912c
	stream->Write(m_iLargestCityHappiness);
	stream->Write(m_iWarWearinessModifier);
	stream->Write(m_iFreeSpecialist);
	stream->Write(m_iTradeRoutes);
	stream->Write(m_eTechPrereq);
	stream->Write(m_iCivicPercentAnger);
	stream->Write(m_iMaxConscript);
	stream->Write(m_iStateReligionHappiness);
	stream->Write(m_iNonStateReligionHappiness);
	stream->Write(m_iStateReligionUnitProductionModifier);
	stream->Write(m_iStateReligionBuildingProductionModifier);
	stream->Write(m_iStateReligionFreeExperience);
	stream->Write(m_iExpInBorderModifier);
	stream->Write(m_iLevelExperienceModifier); // doc
	stream->Write(m_iCorporationUnhappinessModifier); // doc
	stream->Write(m_iProcessModifier); // doc
	stream->Write(m_iFoodProductionModifier); // doc
	stream->Write(m_iWonderProductionModifier); // doc
	stream->Write(m_iCorporationCommerceModifier); // doc
	stream->Write(m_iDefensivePactTradeModifier); // doc
	stream->Write(m_iVassalTradeModifier); // doc
	stream->Write(m_iShrineIncomeLimitChange); // doc
	stream->Write(m_iCaptureGoldModifier); // doc
	stream->Write(m_iCapitalBuildingProductionModifier); // doc
	stream->Write(m_iOccupationTimeChange); // doc
	//stream->Write(m_bNoUnhealthyPopulation);
	stream->Write(m_iUnhealthyPopulationModifier); // K-Mod
	stream->Write(m_bBuildingOnlyHealthy);
	stream->Write(m_bNoForeignTrade);
	stream->Write(m_bNoCorporations);
	stream->Write(m_bNoForeignCorporations);
	stream->Write(m_bStateReligion);
	stream->Write(m_bNoNonStateReligionSpread);
	stream->Write(m_bNoForeignTradeModifier); // doc
	stream->Write(m_bSlavery); // doc
	stream->Write(m_bNoSlavery); // doc
	stream->Write(m_bColonialSlavery); // doc
	stream->Write(m_bNoStateReligionAnarchy); // doc
	stream->Write(m_bFreeImprovementUpgrade); // doc
	stream->Write(NUM_YIELD_TYPES, m_piYieldModifier);
	stream->Write(NUM_YIELD_TYPES, m_piCapitalYieldModifier);
	stream->Write(NUM_YIELD_TYPES, m_piTradeYieldModifier);
	stream->Write(NUM_COMMERCE_TYPES, m_piCommerceModifier);
	stream->Write(NUM_COMMERCE_TYPES, m_piCapitalCommerceModifier);
	stream->Write(NUM_COMMERCE_TYPES, m_piSpecialistExtraCommerce);
	stream->Write(NUM_YIELD_TYPES, m_piStateReligionBuildingYield); // doc
	stream->Write(NUM_YIELD_TYPES, m_piSpecialistExtraYield); // doc
	stream->Write(GC.getNumSpecialistInfos(), m_piSpecialistExtraYield); // doc
	stream->Write(GC.getNumBuildingClassInfos(), m_paiBuildingHappinessChanges);
	stream->Write(GC.getNumBuildingClassInfos(), m_paiBuildingHealthChanges);
	stream->Write(GC.getNumFeatureInfos(), m_paiFeatureHappinessChanges);
	stream->Write(NUM_DOMAIN_TYPES, m_paiDomainExperienceModifiers); // doc
	stream->Write(GC.getNumBuildingClassInfos(), m_paiBuildingProductionModifiers); // doc
	stream->Write(GC.getNumHurryInfos(), m_pabHurry);
	stream->Write(GC.getNumSpecialBuildingInfos(), m_pabSpecialBuildingNotRequired);
	stream->Write(GC.getNumSpecialistInfos(), m_pabSpecialistValid);

	for(int i = 0;i < GC.getNumImprovementInfos(); i++)
		stream->Write(NUM_YIELD_TYPES, m_ppiImprovementYieldChanges[i]);

	// doc
	FOR_EACH_ENUM(Specialist)
	{
		stream.Write(NUM_YIELD_TYPES, m_ppiSpecialistTypeExtraYields[eLoopSpecialist]);
	}

	stream->WriteString(m_szWeLoveTheKingKey);
}
#endif
bool CvCivicInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML))
		return false;

	pXML->SetInfoIDFromChildXmlVal(m_eCivicOptionType, "CivicOptionType");
	FAssert(m_eCivicOptionType != NO_CIVICOPTION); // advc
	pXML->SetInfoIDFromChildXmlVal(m_eTechPrereq, "TechPrereq");

	pXML->GetChildXmlValByName(&m_iAnarchyLength, "iAnarchyLength");

	pXML->SetInfoIDFromChildXmlVal(m_iUpkeep, "Upkeep");

	pXML->GetChildXmlValByName(&m_iAIWeight, "iAIWeight");
	pXML->GetChildXmlValByName(&m_bCanAlwaysForce, "bCanAlwaysForce", false); // advc.132
	pXML->GetChildXmlValByName(&m_iGreatPeopleRateModifier, "iGreatPeopleRateModifier");
	pXML->GetChildXmlValByName(&m_iGreatGeneralRateModifier, "iGreatGeneralRateModifier");
	pXML->GetChildXmlValByName(&m_iDomesticGreatGeneralRateModifier, "iDomesticGreatGeneralRateModifier");
	pXML->GetChildXmlValByName(&m_iStateReligionGreatPeopleRateModifier, "iStateReligionGreatPeopleRateModifier");
	pXML->GetChildXmlValByName(&m_iDistanceMaintenanceModifier, "iDistanceMaintenanceModifier");
	// advc.912g:
	pXML->GetChildXmlValByName(&m_iColonyMaintenanceModifier, "iColonyMaintenanceModifier", 0);
	pXML->GetChildXmlValByName(&m_iNumCitiesMaintenanceModifier, "iNumCitiesMaintenanceModifier");
	pXML->GetChildXmlValByName(&m_iCorporationMaintenanceModifier, "iCorporationMaintenanceModifier");
	pXML->GetChildXmlValByName(&m_iExtraHealth, "iExtraHealth");
	pXML->GetChildXmlValByName(&m_iExtraHappiness, "iExtraHappiness", 0); // K-Mod (advc: made optional)
	pXML->GetChildXmlValByName(&m_iFreeExperience, "iFreeExperience");
	pXML->GetChildXmlValByName(&m_iWorkerSpeedModifier, "iWorkerSpeedModifier");
	pXML->GetChildXmlValByName(&m_iImprovementUpgradeRateModifier, "iImprovementUpgradeRateModifier");
	pXML->GetChildXmlValByName(&m_iMilitaryProductionModifier, "iMilitaryProductionModifier");
	pXML->GetChildXmlValByName(&m_iBaseFreeUnits, "iBaseFreeUnits");
	pXML->GetChildXmlValByName(&m_iBaseFreeMilitaryUnits, "iBaseFreeMilitaryUnits");
	pXML->GetChildXmlValByName(&m_iFreeUnitsPopulationPercent, "iFreeUnitsPopulationPercent");
	pXML->GetChildXmlValByName(&m_iFreeMilitaryUnitsPopulationPercent, "iFreeMilitaryUnitsPopulationPercent");
	pXML->GetChildXmlValByName(&m_iGoldPerUnit, "iGoldPerUnit");
	pXML->GetChildXmlValByName(&m_iGoldPerMilitaryUnit, "iGoldPerMilitaryUnit");
	pXML->GetChildXmlValByName(&m_iHappyPerMilitaryUnit, "iHappyPerMilitaryUnit");
	pXML->GetChildXmlValByName(&m_iLuxuryModifier, "iLuxuryModifier", 0); // advc.912c
	pXML->GetChildXmlValByName(&m_bMilitaryFoodProduction, "bMilitaryFoodProduction");
	pXML->GetChildXmlValByName(&m_iMaxConscript, "iMaxConscript");
	//pXML->GetChildXmlValByName(&m_bNoUnhealthyPopulation, "bNoUnhealthyPopulation");
	// K-Mod (advc - optional):
	pXML->GetChildXmlValByName(&m_iUnhealthyPopulationModifier, "iUnhealthyPopulationModifier", 0);
	pXML->GetChildXmlValByName(&m_bBuildingOnlyHealthy, "bBuildingOnlyHealthy");
	pXML->GetChildXmlValByName(&m_iLargestCityHappiness, "iLargestCityHappiness");
	pXML->GetChildXmlValByName(&m_iWarWearinessModifier, "iWarWearinessModifier");
	pXML->GetChildXmlValByName(&m_iFreeSpecialist, "iFreeSpecialist");
	pXML->GetChildXmlValByName(&m_iTradeRoutes, "iTradeRoutes");
	pXML->GetChildXmlValByName(&m_bNoForeignTrade, "bNoForeignTrade");
	pXML->GetChildXmlValByName(&m_bNoCorporations, "bNoCorporations");
	pXML->GetChildXmlValByName(&m_bNoForeignCorporations, "bNoForeignCorporations");
	pXML->GetChildXmlValByName(&m_iCivicPercentAnger, "iCivicPercentAnger");
	pXML->GetChildXmlValByName(&m_bStateReligion, "bStateReligion");
	pXML->GetChildXmlValByName(&m_bNoNonStateReligionSpread, "bNoNonStateReligionSpread");

	// doc
	pXML->GetChildXmlValByName(&m_bNoForeignTradeModifier, "bNoForeignTradeModifier");
	pXML->GetChildXmlValByName(&m_bSlavery, "bSlavery");
	pXML->GetChildXmlValByName(&m_bNoSlavery, "bNoSlavery");
	pXML->GetChildXmlValByName(&m_bColonialSlavery, "bColonialSlavery");
	pXML->GetChildXmlValByName(&m_bNoStateReligionAnarchy, "bNoStateReligionAnarchy");
	pXML->GetChildXmlValByName(&m_bFreeImprovementUpgrade, "bFreeImprovementUpgrade");

	pXML->GetChildXmlValByName(&m_iStateReligionHappiness, "iStateReligionHappiness");
	pXML->GetChildXmlValByName(&m_iNonStateReligionHappiness, "iNonStateReligionHappiness");
	pXML->GetChildXmlValByName(&m_iStateReligionUnitProductionModifier, "iStateReligionUnitProductionModifier");
	pXML->GetChildXmlValByName(&m_iStateReligionBuildingProductionModifier, "iStateReligionBuildingProductionModifier");
	pXML->GetChildXmlValByName(&m_iStateReligionFreeExperience, "iStateReligionFreeExperience");
	pXML->GetChildXmlValByName(&m_iExpInBorderModifier, "iExpInBorderModifier");

	// doc
	pXML->GetChildXmlValByName(&m_iLevelExperienceModifier, "iLevelExperienceModifier");
	pXML->GetChildXmlValByName(&m_iCorporationUnhappinessModifier, "iCorporationUnhappinessModifier");
	pXML->GetChildXmlValByName(&m_iProcessModifier, "iProcessModifier");
	pXML->GetChildXmlValByName(&m_iFoodProductionModifier, "iFoodProductionModifier");
	pXML->GetChildXmlValByName(&m_iWonderProductionModifier, "iWonderProductionModifier");
	pXML->GetChildXmlValByName(&m_iCorporationCommerceModifier, "iCorporationCommerceModifier");
	pXML->GetChildXmlValByName(&m_iDefensivePactTradeModifier, "iDefensivePactTradeModifier");
	pXML->GetChildXmlValByName(&m_iVassalTradeModifier, "iVassalTradeModifier");
	pXML->GetChildXmlValByName(&m_iShrineIncomeLimitChange, "iShrineIncomeLimitChange");
	pXML->GetChildXmlValByName(&m_iCaptureGoldModifier, "iCaptureGoldModifier");
	pXML->GetChildXmlValByName(&m_iCapitalBuildingProductionModifier, "iCapitalBuildingProductionModifier");
	pXML->GetChildXmlValByName(&m_iOccupationTimeChange, "iOccupationTimeChange");

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),
		"YieldModifiers"))
	{
		pXML->SetYieldArray(&m_piYieldModifier);
	}
	else pXML->InitList(&m_piYieldModifier, NUM_YIELD_TYPES);

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),
		"CapitalYieldModifiers"))
	{
		pXML->SetYieldArray(&m_piCapitalYieldModifier);
	}
	else pXML->InitList(&m_piCapitalYieldModifier, NUM_YIELD_TYPES);

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),
		"TradeYieldModifiers"))
	{
		pXML->SetYieldArray(&m_piTradeYieldModifier);
	}
	else pXML->InitList(&m_piTradeYieldModifier, NUM_YIELD_TYPES);

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),
		"CommerceModifiers"))
	{
		pXML->SetCommerceArray(&m_piCommerceModifier);
	}
	else pXML->InitList(&m_piCommerceModifier, NUM_COMMERCE_TYPES);

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),
		"CapitalCommerceModifiers"))
	{
		pXML->SetCommerceArray(&m_piCapitalCommerceModifier);
	}
	else pXML->InitList(&m_piCapitalCommerceModifier, NUM_COMMERCE_TYPES);

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),
		"SpecialistExtraCommerces"))
	{
		pXML->SetCommerceArray(&m_piSpecialistExtraCommerce);
	}
	else pXML->InitList(&m_piSpecialistExtraCommerce, NUM_COMMERCE_TYPES);

	// doc
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),
		"StateReligionBuildingYields"))
	{
		pXML->SetCommerceArray(&m_piStateReligionBuildingYield);
	}
	else pXML->InitList(&m_piStateReligionBuildingYield, NUM_YIELD_TYPES);

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),
		"SpecialistExtraYields"))
	{
		pXML->SetCommerceArray(&m_piSpecialistExtraYield);
	}
	else pXML->InitList(&m_piSpecialistExtraYield, NUM_YIELD_TYPES);

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),
		"SpecialistCounts"))
	{
		pXML->SetCommerceArray(&m_piSpecialistCount);
	}
	else pXML->InitList(&m_piSpecialistCount, NUM_YIELD_TYPES);

	pXML->SetVariableListTagPair(&m_pabHurry, "Hurrys", GC.getNumHurryInfos());
	pXML->SetVariableListTagPair(&m_pabSpecialBuildingNotRequired, "SpecialBuildingNotRequireds", GC.getNumSpecialBuildingInfos());
	pXML->SetVariableListTagPair(&m_pabSpecialistValid, "SpecialistValids", GC.getNumSpecialistInfos());

	pXML->SetVariableListTagPair(&m_paiBuildingHappinessChanges, "BuildingHappinessChanges", GC.getNumBuildingClassInfos());
	pXML->SetVariableListTagPair(&m_paiBuildingHealthChanges, "BuildingHealthChanges", GC.getNumBuildingClassInfos());
	pXML->SetVariableListTagPair(&m_paiFeatureHappinessChanges, "FeatureHappinessChanges", GC.getNumFeatureInfos());

	// doc
	pXML->SetVariableListTagPair(&m_paiDomainExperienceModifiers, "DomainExperienceModifiers", NUM_DOMAIN_TYPES);
	pXML->SetVariableListTagPair(&m_paiBuildingProductionModifiers, "BuildingProductionModifiers", GC.getNumBuildingClassInfos());

	FAssert(GC.getNumImprovementInfos() > 0);
	pXML->Init2DIntList(&m_ppiImprovementYieldChanges, GC.getNumImprovementInfos(), NUM_YIELD_TYPES);
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "ImprovementYieldChanges"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			if (gDLL->getXMLIFace()->SetToChild(pXML->GetXML()))
			{
				if (iNumSibs > 0)
				{
					for (int j = 0; j < iNumSibs; j++)
					{
						CvString szTextVal;
						pXML->GetChildXmlValByName(szTextVal, "ImprovementType");
						int iIndex = pXML->FindInInfoClass(szTextVal);
						if (iIndex > -1)
						{
							SAFE_DELETE_ARRAY(m_ppiImprovementYieldChanges[iIndex]);
							if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),
								"ImprovementYields"))
							{
								pXML->SetYieldArray(&m_ppiImprovementYieldChanges[iIndex]);
							}
							else pXML->InitList(&m_ppiImprovementYieldChanges[iIndex], NUM_YIELD_TYPES);
						}
						if (!gDLL->getXMLIFace()->NextSibling(pXML->GetXML()))
							break;
					}
				}
				gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	// doc
	FAssert(GC.getNumSpecialistInfos() > 0);
	pXML->Init2DIntList(&m_ppiSpecialistTypeExtraYields, GC.getNumSpecialistInfos(), NUM_YIELD_TYPES);
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "SpecialistTypeExtraYields"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			if (gDLL->getXMLIFace()->SetToChild(pXML->GetXML()))
			{
				if (iNumSibs > 0)
				{
					for (int j = 0; j < iNumSibs; j++)
					{
						CvString szTextVal;
						pXML->GetChildXmlValByName(szTextVal, "SpecialistType");
						int iIndex = pXML->FindInInfoClass(szTextVal);
						if (iIndex > -1)
						{
							SAFE_DELETE_ARRAY(m_ppiSpecialistTypeExtraYields[iIndex]);
							if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),
								"SpecialistYields"))
							{
								pXML->SetYieldArray(&m_ppiSpecialistTypeExtraYields[iIndex]);
							}
							else pXML->InitList(&m_ppiSpecialistTypeExtraYields[iIndex], NUM_YIELD_TYPES);
						}
						if (!gDLL->getXMLIFace()->NextSibling(pXML->GetXML()))
							break;
					}
				}
				gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	pXML->GetChildXmlValByName(m_szWeLoveTheKingKey, "WeLoveTheKing");

	return true;
}

CvCivicOptionInfo::CvCivicOptionInfo() : m_pabTraitNoUpkeep(NULL) {}

CvCivicOptionInfo::~CvCivicOptionInfo()
{
	SAFE_DELETE_ARRAY(m_pabTraitNoUpkeep);
}

bool CvCivicOptionInfo::getTraitNoUpkeep(int i) const
{
	FAssertBounds(0, GC.getNumTraitInfos(), i);
	return m_pabTraitNoUpkeep ? m_pabTraitNoUpkeep[i] : false;
}

bool CvCivicOptionInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML))
		return false;

	pXML->SetVariableListTagPair(&m_pabTraitNoUpkeep, "TraitNoUpkeeps", GC.getNumTraitInfos());

	return true;
}

CvUpkeepInfo::CvUpkeepInfo() :
m_iPopulationPercent(0),
m_iCityPercent(0)
{}

bool CvUpkeepInfo::read(CvXMLLoadUtility* pXml)
{
	if (!base_t::read(pXml))
		return false;

	pXml->GetChildXmlValByName(&m_iPopulationPercent, "iPopulationPercent");
	pXml->GetChildXmlValByName(&m_iCityPercent, "iCityPercent");

	return true;
}
