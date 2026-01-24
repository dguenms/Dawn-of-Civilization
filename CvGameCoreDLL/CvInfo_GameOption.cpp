// advc.003x: Cut from CvInfos.cpp

#include "CvGameCoreDLL.h"
#include "CvInfo_GameOption.h"
#include "CvXMLLoadUtility.h"
#include "CvInitCore.h" // advc.137


CvGameOptionInfo::CvGameOptionInfo() :
m_bDefault(false),
m_bVisible(true),
m_bVisibleXML(true) // advc.054
{}

bool CvGameOptionInfo::getDefault() const
{
	return m_bDefault;
}

bool CvGameOptionInfo::getVisible() const
{
	return m_bVisible;
}
// <advc.054>
bool CvGameOptionInfo::getVisibleXML() const
{
	return m_bVisibleXML;
}

void CvGameOptionInfo::setVisible(bool b) {

	m_bVisible = b;
} // </advc.054>

bool CvGameOptionInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML))
		return false;

	pXML->GetChildXmlValByName(&m_bDefault, "bDefault");
	pXML->GetChildXmlValByName(&m_bVisible, "bVisible");
	m_bVisibleXML = m_bVisible; // advc.054

	return true;
}

CvMPOptionInfo::CvMPOptionInfo() : m_bDefault(false) {}

bool CvMPOptionInfo::getDefault() const
{
	return m_bDefault;
}

bool CvMPOptionInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML))
		return false;

	pXML->GetChildXmlValByName(&m_bDefault, "bDefault");
	return true;
}

// <advc.erai>
EraTypes CvEraInfo::m_eAIAgeOfExploration = ERA_NEVER;
EraTypes CvEraInfo::m_eAIAgeOfPestilence = ERA_NEVER;
EraTypes CvEraInfo::m_eAIAgeOfPollution = ERA_NEVER;
EraTypes CvEraInfo::m_eAIAgeOfFertility = ERA_NEVER;
EraTypes CvEraInfo::m_eAIAgeOfGuns = ERA_NEVER;
EraTypes CvEraInfo::m_eAIAtomicAge = ERA_NEVER;
// </advc.erai>

CvEraInfo::CvEraInfo() :
m_iStartingUnitMultiplier(0),
m_iStartingDefenseUnits(0),
m_iStartingWorkerUnits(0),
m_iStartingExploreUnits(0),
m_iAdvancedStartPoints(0),
m_iStartingGold(0),
m_iFreePopulation(0),
m_iStartPercent(0),
m_iGrowthPercent(0),
m_iTrainPercent(0),
m_iConstructPercent(0),
m_iCreatePercent(0),
m_iResearchPercent(/* advc: */ -1),
m_iTechCostModifier(0), // BETTER_BTS_AI_MOD, Tech Diffusion, 08/21/09, jdog5000
m_iBuildPercent(0),
m_iImprovementPercent(0),
m_iGreatPeoplePercent(0),
m_iCulturePercent(0), // advc.126
m_iAnarchyPercent(0),
m_iEventChancePerTurn(0),
m_iSoundtrackSpace(0),
m_iNumSoundtracks(0),
m_bNoGoodies(false),
m_bNoAnimals(false),
m_bNoBarbUnits(false),
m_bNoBarbCities(false),
m_bFirstSoundtrackFirst(false),
m_paiCitySoundscapeScriptIds(NULL),
m_paiSoundtracks(NULL)
{}

CvEraInfo::~CvEraInfo()
{
	SAFE_DELETE_ARRAY(m_paiCitySoundscapeScriptIds);
	SAFE_DELETE_ARRAY(m_paiSoundtracks);
}

int CvEraInfo::getStartingUnitMultiplier() const
{
	return m_iStartingUnitMultiplier;
}

int CvEraInfo::getStartingDefenseUnits() const
{
	return m_iStartingDefenseUnits;
}

int CvEraInfo::getStartingWorkerUnits() const
{
	return m_iStartingWorkerUnits;
}

int CvEraInfo::getStartingExploreUnits() const
{
	return m_iStartingExploreUnits;
}

int CvEraInfo::getAdvancedStartPoints() const
{
	return m_iAdvancedStartPoints;
}

int CvEraInfo::getStartingGold() const
{
	return m_iStartingGold;
}

int CvEraInfo::getFreePopulation() const
{
	return m_iFreePopulation;
}

int CvEraInfo::getStartPercent() const
{
	return m_iStartPercent;
}

int CvEraInfo::getEventChancePerTurn() const
{
	return m_iEventChancePerTurn;
}

int CvEraInfo::getSoundtrackSpace() const
{
	return m_iSoundtrackSpace;
}

bool CvEraInfo::isFirstSoundtrackFirst() const
{
	return m_bFirstSoundtrackFirst;
}

int CvEraInfo::getNumSoundtracks() const
{
	return m_iNumSoundtracks;
}

const TCHAR* CvEraInfo::getAudioUnitVictoryScript() const
{
	return m_szAudioUnitVictoryScript;
}

const TCHAR* CvEraInfo::getAudioUnitDefeatScript() const
{
	return m_szAudioUnitDefeatScript;
}

bool CvEraInfo::isNoGoodies() const
{
	return m_bNoGoodies;
}

bool CvEraInfo::isNoAnimals() const
{
	return m_bNoAnimals;
}

bool CvEraInfo::isNoBarbUnits() const
{
	return m_bNoBarbUnits;
}

bool CvEraInfo::isNoBarbCities() const
{
	return m_bNoBarbCities;
}

int CvEraInfo::getSoundtracks(int i) const
{
	FAssertBounds(0, getNumSoundtracks(), i);
	/*	advc (note): For all other audio ids, the default is 0, but the -1 here
		is consistent with CvEraInfo::read and CvGame::getNextSoundtrack. */
	return m_paiSoundtracks ? m_paiSoundtracks[i] : -1;
}

int CvEraInfo::getCitySoundscapeScriptId(int i) const
{
	FAssertBounds(0, NUM_CITYSIZE_TYPES, i); // advc: Check for upper bound added
	return m_paiCitySoundscapeScriptIds ? m_paiCitySoundscapeScriptIds[i] : 0; // advc.003t
}

bool CvEraInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML)) // advc.tag
		return false;

	pXML->GetChildXmlValByName(&m_bNoGoodies, "bNoGoodies");
	pXML->GetChildXmlValByName(&m_bNoAnimals, "bNoAnimals");
	pXML->GetChildXmlValByName(&m_bNoBarbUnits, "bNoBarbUnits");
	pXML->GetChildXmlValByName(&m_bNoBarbCities, "bNoBarbCities");
	pXML->GetChildXmlValByName(&m_iStartingUnitMultiplier, "iStartingUnitMultiplier");
	pXML->GetChildXmlValByName(&m_iStartingDefenseUnits, "iStartingDefenseUnits");
	pXML->GetChildXmlValByName(&m_iStartingWorkerUnits, "iStartingWorkerUnits");
	pXML->GetChildXmlValByName(&m_iStartingExploreUnits, "iStartingExploreUnits");
	pXML->GetChildXmlValByName(&m_iAdvancedStartPoints, "iAdvancedStartPoints");
	pXML->GetChildXmlValByName(&m_iStartingGold, "iStartingGold");
	pXML->GetChildXmlValByName(&m_iFreePopulation, "iFreePopulation");
	pXML->GetChildXmlValByName(&m_iStartPercent, "iStartPercent");
	pXML->GetChildXmlValByName(&m_iGrowthPercent, "iGrowthPercent");
	pXML->GetChildXmlValByName(&m_iTrainPercent, "iTrainPercent");
	pXML->GetChildXmlValByName(&m_iConstructPercent, "iConstructPercent");
	pXML->GetChildXmlValByName(&m_iCreatePercent, "iCreatePercent");
	pXML->GetChildXmlValByName(&m_iResearchPercent, "iResearchPercent");
	FAssert(m_iResearchPercent > 0); // advc
	// BETTER_BTS_AI_MOD, Tech Diffusion, 08/21/09, jdog5000:
	pXML->GetChildXmlValByName(&m_iTechCostModifier, "iTechCostModifier", 0);
	pXML->GetChildXmlValByName(&m_iBuildPercent, "iBuildPercent");
	pXML->GetChildXmlValByName(&m_iImprovementPercent, "iImprovementPercent");
	pXML->GetChildXmlValByName(&m_iGreatPeoplePercent, "iGreatPeoplePercent");
	pXML->GetChildXmlValByName(&m_iCulturePercent, "iCulturePercent"); // advc.126
	pXML->GetChildXmlValByName(&m_iAnarchyPercent, "iAnarchyPercent");
	pXML->GetChildXmlValByName(&m_iEventChancePerTurn, "iEventChancePerTurn");
	pXML->GetChildXmlValByName(&m_iSoundtrackSpace, "iSoundtrackSpace");
	pXML->GetChildXmlValByName(&m_bFirstSoundtrackFirst, "bFirstSoundtrackFirst");
	pXML->GetChildXmlValByName(m_szAudioUnitVictoryScript, "AudioUnitVictoryScript");
	pXML->GetChildXmlValByName(m_szAudioUnitDefeatScript, "AudioUnitDefeatScript");

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "EraInfoSoundtracks"))
	{
		CvString* pszSoundTrackNames = NULL;
		pXML->SetStringList(&pszSoundTrackNames, &m_iNumSoundtracks);
		if (m_iNumSoundtracks > 0)
		{
			m_paiSoundtracks = new int[m_iNumSoundtracks];
			for (int j = 0; j < m_iNumSoundtracks; j++)
			{
				m_paiSoundtracks[j] = (gDLL->getAudioDisabled() ? -1 :
						gDLL->getAudioTagIndex(pszSoundTrackNames[j], AUDIOTAG_2DSCRIPT));
			}
		}
		else m_paiSoundtracks = NULL;
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
		SAFE_DELETE_ARRAY(pszSoundTrackNames);
	}

	pXML->SetVariableListTagPairForAudioScripts(&m_paiCitySoundscapeScriptIds,
			"CitySoundscapes",
			//CvGlobals::getInstance().getCitySizeTypes(), // advc: callee didn't use it
			//sizeof(GC.getCitySizeTypes((CitySizeTypes)0))
			/*	advc.001 (The above was greater than the correct value,
				so it didn't do any real harm.) */
			NUM_CITYSIZE_TYPES);

	return true;
}

// advc.erai:
void CvEraInfo::allInfosRead()
{
	FOR_EACH_ENUM(Era)
	{
		CvEraInfo& kLoopEra = GC.getInfo(eLoopEra);
		// Set default values for AI era factors
		if (kLoopEra.get(CvEraInfo::AIEraFactor) == -1)
		{
			kLoopEra.set((base_t::IntElementTypes)
					CvEraInfo::AIEraFactor, 100 * eLoopEra);
			/*	The idea is to map the eras of a mod to the BtS eras that the
				AI code has been written for. Therefore shouldn't exceed 100 times
				the highest BtS era index. */
			FAssertBounds(0, 601, kLoopEra.get(CvEraInfo::AIEraFactor));
			FAssert(eLoopEra <= 0 ||
					// Era factors should increase strictly
					GC.getInfo((EraTypes)(eLoopEra - 1)).get(CvEraInfo::AIEraFactor) <
					kLoopEra.get(CvEraInfo::AIEraFactor));
		}
		// Set AI ages
		if (m_eAIAgeOfExploration == ERA_NEVER &&
			kLoopEra.get(CvEraInfo::AIAgeOfExploration))
		{
			m_eAIAgeOfExploration = eLoopEra;
		}
		if (m_eAIAgeOfPestilence == ERA_NEVER &&
			kLoopEra.get(CvEraInfo::AIAgeOfPestilence))
		{
			m_eAIAgeOfPestilence = eLoopEra;
		}
		if (m_eAIAgeOfPollution == ERA_NEVER &&
			kLoopEra.get(CvEraInfo::AIAgeOfPollution))
		{
			m_eAIAgeOfPollution = eLoopEra;
		}
		if (m_eAIAgeOfFertility == ERA_NEVER &&
			kLoopEra.get(CvEraInfo::AIAgeOfFertility))
		{
			m_eAIAgeOfFertility = eLoopEra;
		}
		if (m_eAIAgeOfGuns == ERA_NEVER &&
			kLoopEra.get(CvEraInfo::AIAgeOfGuns))
		{
			m_eAIAgeOfGuns = eLoopEra;
		}
		if (m_eAIAtomicAge == ERA_NEVER &&
			kLoopEra.get(CvEraInfo::AIAtomicAge))
		{
			m_eAIAtomicAge = eLoopEra;
		}
	}
}

CvGameSpeedInfo::CvGameSpeedInfo() :
m_iGrowthPercent(0),
m_iTrainPercent(0),
m_iConstructPercent(0),
m_iCreatePercent(0),
m_iResearchPercent(/* advc: */ -1),
m_iBuildPercent(0),
m_iImprovementPercent(0),
m_iGreatPeoplePercent(0),
m_iAnarchyPercent(0),
m_iBarbPercent(0),
m_iFeatureProductionPercent(0),
m_iUnitDiscoverPercent(0),
m_iUnitHurryPercent(0),
m_iUnitTradePercent(0),
m_iUnitGreatWorkPercent(0),
m_iGoldenAgePercent(0),
m_iHurryPercent(0),
m_iHurryConscriptAngerPercent(0),
m_iInflationOffset(0),
m_iInflationPercent(0),
m_iVictoryDelayPercent(0),
m_iNumTurnIncrements(0),
m_pGameTurnInfo(NULL)
{}

CvGameSpeedInfo::~CvGameSpeedInfo()
{
	SAFE_DELETE_ARRAY(m_pGameTurnInfo);
}

int CvGameSpeedInfo::getBarbPercent() const
{
	return m_iBarbPercent;
}

int CvGameSpeedInfo::getFeatureProductionPercent() const
{
	return m_iFeatureProductionPercent;
}

int CvGameSpeedInfo::getUnitDiscoverPercent() const
{
	return m_iUnitDiscoverPercent;
}

int CvGameSpeedInfo::getUnitHurryPercent() const
{
	return m_iUnitHurryPercent;
}

int CvGameSpeedInfo::getUnitTradePercent() const
{
	return m_iUnitTradePercent;
}

int CvGameSpeedInfo::getUnitGreatWorkPercent() const
{
	return m_iUnitGreatWorkPercent;
}

int CvGameSpeedInfo::getHurryPercent() const
{
	return m_iHurryPercent;
}

int CvGameSpeedInfo::getHurryConscriptAngerPercent() const
{
	return m_iHurryConscriptAngerPercent;
}

int CvGameSpeedInfo::getInflationOffset() const
{
	return m_iInflationOffset;
}

int CvGameSpeedInfo::getInflationPercent() const
{
	return m_iInflationPercent;
}

int CvGameSpeedInfo::getNumTurnIncrements() const
{
	return m_iNumTurnIncrements;
}

GameTurnInfo& CvGameSpeedInfo::getGameTurnInfo(int iIndex) const
{
	FAssertBounds(0, getNumTurnIncrements(), iIndex); // advc: added
	return m_pGameTurnInfo[iIndex];
}

void CvGameSpeedInfo::allocateGameTurnInfos(const int iSize)
{
	m_pGameTurnInfo = new GameTurnInfo[iSize];
}

bool CvGameSpeedInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML))
		return false;

	pXML->GetChildXmlValByName(&m_iGrowthPercent, "iGrowthPercent");
	pXML->GetChildXmlValByName(&m_iTrainPercent, "iTrainPercent");
	pXML->GetChildXmlValByName(&m_iConstructPercent, "iConstructPercent");
	pXML->GetChildXmlValByName(&m_iCreatePercent, "iCreatePercent");
	pXML->GetChildXmlValByName(&m_iResearchPercent, "iResearchPercent");
	FAssert(m_iResearchPercent > 0); // advc
	pXML->GetChildXmlValByName(&m_iBuildPercent, "iBuildPercent");
	pXML->GetChildXmlValByName(&m_iImprovementPercent, "iImprovementPercent");
	pXML->GetChildXmlValByName(&m_iGreatPeoplePercent, "iGreatPeoplePercent");
	pXML->GetChildXmlValByName(&m_iAnarchyPercent, "iAnarchyPercent");
	pXML->GetChildXmlValByName(&m_iBarbPercent, "iBarbPercent");
	pXML->GetChildXmlValByName(&m_iFeatureProductionPercent, "iFeatureProductionPercent");
	pXML->GetChildXmlValByName(&m_iUnitDiscoverPercent, "iUnitDiscoverPercent");
	pXML->GetChildXmlValByName(&m_iUnitHurryPercent, "iUnitHurryPercent");
	pXML->GetChildXmlValByName(&m_iUnitTradePercent, "iUnitTradePercent");
	pXML->GetChildXmlValByName(&m_iUnitGreatWorkPercent, "iUnitGreatWorkPercent");
	pXML->GetChildXmlValByName(&m_iGoldenAgePercent, "iGoldenAgePercent");
	// <advc>
	FAssertMsg(m_iResearchPercent >= 100 ?
			(m_iGoldenAgePercent * 3 > m_iResearchPercent && m_iGoldenAgePercent <= m_iResearchPercent) :
			(3 * m_iGoldenAgePercent < 4 * m_iResearchPercent && m_iGoldenAgePercent >= m_iResearchPercent),
			"The Golden Age modifier gets used for various adjustments; unusual values should be avoided."); // </advc>
	pXML->GetChildXmlValByName(&m_iHurryPercent, "iHurryPercent");
	pXML->GetChildXmlValByName(&m_iHurryConscriptAngerPercent, "iHurryConscriptAngerPercent");
	pXML->GetChildXmlValByName(&m_iInflationOffset, "iInflationOffset");
	pXML->GetChildXmlValByName(&m_iInflationPercent, "iInflationPercent");
	pXML->GetChildXmlValByName(&m_iVictoryDelayPercent, "iVictoryDelayPercent");

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"GameTurnInfos"))
	{
		m_iNumTurnIncrements = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
		if (gDLL->getXMLIFace()->SetToChild(pXML->GetXML()))
		{
			allocateGameTurnInfos(getNumTurnIncrements());
			for (int j = 0; j < getNumTurnIncrements(); j++)
			{
				int iTempVal;
				pXML->GetChildXmlValByName(&iTempVal, "iMonthIncrement");
				getGameTurnInfo(j).iMonthIncrement = iTempVal;
				pXML->GetChildXmlValByName(&iTempVal, "iTurnsPerIncrement");
				getGameTurnInfo(j).iNumGameTurnsPerIncrement = iTempVal;
				if (!gDLL->getXMLIFace()->NextSibling(pXML->GetXML()))
					break;
			}
			gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	return true;
}

CvTurnTimerInfo::CvTurnTimerInfo() :
m_iBaseTime(0),
m_iCityBonus(0),
m_iUnitBonus(0),
m_iFirstTurnMultiplier(0)
{}

int CvTurnTimerInfo::getBaseTime() const
{
	return m_iBaseTime;
}

int CvTurnTimerInfo::getCityBonus() const
{
	return m_iCityBonus;
}

int CvTurnTimerInfo::getUnitBonus() const
{
	return m_iUnitBonus;
}

int CvTurnTimerInfo::getFirstTurnMultiplier() const
{
	return m_iFirstTurnMultiplier;
}

bool CvTurnTimerInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML))
		return false;

	pXML->GetChildXmlValByName(&m_iBaseTime, "iBaseTime");
	pXML->GetChildXmlValByName(&m_iCityBonus, "iCityBonus");
	pXML->GetChildXmlValByName(&m_iUnitBonus, "iUnitBonus");
	pXML->GetChildXmlValByName(&m_iFirstTurnMultiplier, "iFirstTurnMultiplier");

	return true;
}

CvVictoryInfo::CvVictoryInfo() :
m_iPopulationPercentLead(0),
m_iLandPercent(0),
m_iMinLandPercent(0),
m_iReligionPercent(0),
m_iCityCulture(0),
m_iNumCultureCities(0),
m_iTotalCultureRatio(0),
m_iVictoryDelayTurns(0),
m_bTargetScore(false),
m_bEndScore(false),
m_bConquest(false),
m_bDiploVote(false),
m_bPermanent(false)
{}

int CvVictoryInfo::getPopulationPercentLead() const
{
	return m_iPopulationPercentLead;
}

int CvVictoryInfo::getLandPercent() const
{
	return m_iLandPercent;
}

int CvVictoryInfo::getMinLandPercent() const
{
	return m_iMinLandPercent;
}

int CvVictoryInfo::getReligionPercent() const
{
	return m_iReligionPercent;
}

int CvVictoryInfo::getCityCulture() const
{
	return m_iCityCulture;
}

int CvVictoryInfo::getNumCultureCities() const
{
	return m_iNumCultureCities;
}

int CvVictoryInfo::getTotalCultureRatio() const
{
	return m_iTotalCultureRatio;
}

int CvVictoryInfo::getVictoryDelayTurns() const
{
	return m_iVictoryDelayTurns;
}

bool CvVictoryInfo::isTargetScore() const
{
	return m_bTargetScore;
}

bool CvVictoryInfo::isEndScore() const
{
	return m_bEndScore;
}

bool CvVictoryInfo::isConquest() const
{
	return m_bConquest;
}

bool CvVictoryInfo::isDiploVote() const
{
	return m_bDiploVote;
}

bool CvVictoryInfo::isPermanent() const
{
	return m_bPermanent;
}

const char* CvVictoryInfo::getMovie() const
{
	return m_szMovie;
}

bool CvVictoryInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML))
		return false;

	pXML->GetChildXmlValByName(&m_bTargetScore, "bTargetScore");
	pXML->GetChildXmlValByName(&m_bEndScore, "bEndScore");
	pXML->GetChildXmlValByName(&m_bConquest, "bConquest");
	pXML->GetChildXmlValByName(&m_bDiploVote, "bDiploVote");
	pXML->GetChildXmlValByName(&m_bPermanent, "bPermanent");
	pXML->GetChildXmlValByName(&m_iPopulationPercentLead, "iPopulationPercentLead");
	pXML->GetChildXmlValByName(&m_iLandPercent, "iLandPercent");
	pXML->GetChildXmlValByName(&m_iMinLandPercent, "iMinLandPercent");
	pXML->GetChildXmlValByName(&m_iReligionPercent, "iReligionPercent");

	pXML->SetInfoIDFromChildXmlVal(m_iCityCulture, "CityCulture");

	pXML->GetChildXmlValByName(&m_iNumCultureCities, "iNumCultureCities");
	pXML->GetChildXmlValByName(&m_iTotalCultureRatio, "iTotalCultureRatio");
	pXML->GetChildXmlValByName(&m_iVictoryDelayTurns, "iVictoryDelayTurns");
	pXML->GetChildXmlValByName(m_szMovie, "VictoryMovie");

	return true;
}

CvHandicapInfo::CvHandicapInfo() :
m_iFreeWinsVsBarbs(0),
m_iAnimalAttackProb(0),
m_iStartingLocationPercent(0),
m_iAdvancedStartPointsMod(0),
m_iStartingGold(0),
m_iFreeUnits(0),
m_iUnitCostPercent(0),
// <advc.251>
m_iBuildTimePercent(0),
m_iBaseGrowthThresholdPercent(0),
m_iGPThresholdPercent(0),
m_iCultureLevelPercent(0),
// </advc.251>
m_iResearchPercent(/* advc: */ -1),
// <advc.251>
m_iTrainPercent(0),
m_iConstructPercent(0),
m_iCreatePercent(0),
// </advc.251>
m_iDistanceMaintenancePercent(0),
m_iNumCitiesMaintenancePercent(0),
m_iMaxNumCitiesMaintenance(0),
m_iColonyMaintenancePercent(0),
m_iMaxColonyMaintenance(0),
m_iCorporationMaintenancePercent(0),
m_iCivicUpkeepPercent(0),
m_iInflationPercent(0),
m_iHealthBonus(0),
m_iHappyBonus(0),
m_iAttitudeChange(0),
m_iNoTechTradeModifier(0),
m_iTechTradeKnownModifier(0),
m_iUnownedTilesPerGameAnimal(0),
m_iUnownedTilesPerBarbarianUnit(0),
m_iUnownedWaterTilesPerBarbarianUnit(0),
m_iUnownedTilesPerBarbarianCity(0),
m_iBarbarianCreationTurnsElapsed(0),
m_iBarbarianCityCreationTurnsElapsed(0),
m_iBarbarianCityCreationProb(0),
m_iAnimalCombatModifier(0),
m_iBarbarianCombatModifier(0),
m_iAIAnimalCombatModifier(0),
m_iAIBarbarianCombatModifier(0),
m_iStartingDefenseUnits(0),
m_iStartingWorkerUnits(0),
m_iStartingExploreUnits(0),
m_iAIStartingUnitMultiplier(0),
m_iAIStartingDefenseUnits(0),
m_iAIStartingWorkerUnits(0),
m_iAIStartingExploreUnits(0),
m_iBarbarianInitialDefenders(0),
m_iAIDeclareWarProb(0),
m_iAIWorkRateModifier(0),
m_iAIGrowthPercent(/* advc: */ -1),
// <advc.251>
m_iAIGPThresholdPercent(0),
m_iAIResearchPercent(-1),
// </advc.251>
m_iAITrainPercent(/* advc: */ -1),
m_iAIWorldTrainPercent(0),
m_iAIConstructPercent(/* advc: */ -1),
m_iAIWorldConstructPercent(0),
m_iAICreatePercent(0),
m_iAIWorldCreatePercent(0),
m_iAICivicUpkeepPercent(0),
m_iAIUnitCostPercent(0),
m_iAIUnitSupplyPercent(0),
m_iAIUnitUpgradePercent(0),
m_iAIInflationPercent(0),
m_iAIWarWearinessPercent(0),
//m_iAIPerEraModifier(0),
m_iAIHandicapIncrementTurns(0), // advc.251
m_iAIAttitudeChangePercent(1), // advc.148
m_iAIAdvancedStartPercent(0),
m_iNumGoodies(0),
m_iDifficulty(-1), // advc.250a
m_piGoodies(NULL),
m_pbFreeTechs(NULL),
m_pbAIFreeTechs(NULL)
{}

CvHandicapInfo::~CvHandicapInfo()
{
	SAFE_DELETE_ARRAY(m_piGoodies);
	SAFE_DELETE_ARRAY(m_pbFreeTechs);
	SAFE_DELETE_ARRAY(m_pbAIFreeTechs);
}

int CvHandicapInfo::getFreeWinsVsBarbs() const
{
	return m_iFreeWinsVsBarbs;
}

int CvHandicapInfo::getAnimalAttackProb() const
{
	return m_iAnimalAttackProb;
}

int CvHandicapInfo::getStartingLocationPercent() const
{
	return m_iStartingLocationPercent;
}

int CvHandicapInfo::getAdvancedStartPointsMod() const
{
	return m_iAdvancedStartPointsMod;
}

int CvHandicapInfo::getStartingGold() const
{
	return m_iStartingGold;
}

int CvHandicapInfo::getFreeUnits() const
{
	return m_iFreeUnits;
}

int CvHandicapInfo::getUnitCostPercent() const
{
	return m_iUnitCostPercent;
}

int CvHandicapInfo::getDistanceMaintenancePercent() const
{
	return m_iDistanceMaintenancePercent;
}

int CvHandicapInfo::getNumCitiesMaintenancePercent() const
{
	return m_iNumCitiesMaintenancePercent;
}

int CvHandicapInfo::getMaxNumCitiesMaintenance() const
{
	return m_iMaxNumCitiesMaintenance;
}

int CvHandicapInfo::getColonyMaintenancePercent() const
{
	return m_iColonyMaintenancePercent;
}

int CvHandicapInfo::getMaxColonyMaintenance() const
{
	return m_iMaxColonyMaintenance;
}

int CvHandicapInfo::getCorporationMaintenancePercent() const
{
	return m_iCorporationMaintenancePercent;
}

int CvHandicapInfo::getCivicUpkeepPercent() const
{
	return m_iCivicUpkeepPercent;
}

int CvHandicapInfo::getInflationPercent() const
{
	return m_iInflationPercent;
}

int CvHandicapInfo::getHealthBonus() const
{
	return m_iHealthBonus;
}

int CvHandicapInfo::getHappyBonus() const
{
	return m_iHappyBonus;
}

int CvHandicapInfo::getAttitudeChange() const
{
	return m_iAttitudeChange;
}

int CvHandicapInfo::getNoTechTradeModifier() const
{
	return m_iNoTechTradeModifier;
}

int CvHandicapInfo::getTechTradeKnownModifier() const
{
	return m_iTechTradeKnownModifier;
}

int CvHandicapInfo::getUnownedTilesPerGameAnimal() const
{
	return m_iUnownedTilesPerGameAnimal;
}

int CvHandicapInfo::getUnownedTilesPerBarbarianUnit() const
{
	return m_iUnownedTilesPerBarbarianUnit;
}

int CvHandicapInfo::getUnownedWaterTilesPerBarbarianUnit() const
{
	return m_iUnownedWaterTilesPerBarbarianUnit;
}

int CvHandicapInfo::getUnownedTilesPerBarbarianCity() const
{
	return m_iUnownedTilesPerBarbarianCity;
}

int CvHandicapInfo::getBarbarianCreationTurnsElapsed() const
{
	return m_iBarbarianCreationTurnsElapsed;
}

int CvHandicapInfo::getBarbarianCityCreationTurnsElapsed() const
{
	return m_iBarbarianCityCreationTurnsElapsed;
}

int CvHandicapInfo::getBarbarianCityCreationProb() const
{
	return m_iBarbarianCityCreationProb;
}

int CvHandicapInfo::getAnimalCombatModifier() const
{
	return m_iAnimalCombatModifier;
}

int CvHandicapInfo::getBarbarianCombatModifier() const
{
	return m_iBarbarianCombatModifier;
}

int CvHandicapInfo::getAIAnimalCombatModifier() const
{
	return m_iAIAnimalCombatModifier;
}

int CvHandicapInfo::getAIBarbarianCombatModifier() const
{
	return m_iAIBarbarianCombatModifier;
}

int CvHandicapInfo::getStartingDefenseUnits() const
{
	return m_iStartingDefenseUnits;
}

int CvHandicapInfo::getStartingWorkerUnits() const
{
	return m_iStartingWorkerUnits;
}

int CvHandicapInfo::getStartingExploreUnits() const
{
	return m_iStartingExploreUnits;
}

int CvHandicapInfo::getAIStartingUnitMultiplier() const
{
	return m_iAIStartingUnitMultiplier;
}

int CvHandicapInfo::getAIStartingDefenseUnits() const
{
	return m_iAIStartingDefenseUnits;
}

int CvHandicapInfo::getAIStartingWorkerUnits() const
{
	return m_iAIStartingWorkerUnits;
}

int CvHandicapInfo::getAIStartingExploreUnits() const
{
	return m_iAIStartingExploreUnits;
}

int CvHandicapInfo::getBarbarianInitialDefenders() const
{
	return m_iBarbarianInitialDefenders;
}

int CvHandicapInfo::getAIDeclareWarProb() const
{
	return m_iAIDeclareWarProb;
}

int CvHandicapInfo::getAIWorkRateModifier() const
{
	return m_iAIWorkRateModifier;
}

int CvHandicapInfo::getAIGrowthPercent() const
{
	return m_iAIGrowthPercent;
}

int CvHandicapInfo::getAITrainPercent() const
{
	return m_iAITrainPercent;
}

int CvHandicapInfo::getAIWorldTrainPercent() const
{
	return m_iAIWorldTrainPercent;
}

int CvHandicapInfo::getAIConstructPercent() const
{
	return m_iAIConstructPercent;
}

int CvHandicapInfo::getAIWorldConstructPercent() const
{
	return m_iAIWorldConstructPercent;
}

int CvHandicapInfo::getAICreatePercent() const
{
	return m_iAICreatePercent;
}

int CvHandicapInfo::getAIWorldCreatePercent() const
{
	return m_iAIWorldCreatePercent;
}

int CvHandicapInfo::getAICivicUpkeepPercent() const
{
	return m_iAICivicUpkeepPercent;
}

int CvHandicapInfo::getAIUnitCostPercent() const
{
	return m_iAIUnitCostPercent;
}

int CvHandicapInfo::getAIUnitSupplyPercent() const
{
	return m_iAIUnitSupplyPercent;
}

int CvHandicapInfo::getAIUnitUpgradePercent() const
{
	return m_iAIUnitUpgradePercent;
}

int CvHandicapInfo::getAIInflationPercent() const
{
	return m_iAIInflationPercent;
}

int CvHandicapInfo::getAIWarWearinessPercent() const
{
	return m_iAIWarWearinessPercent;
}
// advc.251: Replaced by AIHandicapIncrementTurns
/*int CvHandicapInfo::getAIPerEraModifier() const {
	return m_iAIPerEraModifier;
}*/

int CvHandicapInfo::getAIAdvancedStartPercent() const
{
	return m_iAIAdvancedStartPercent;
}
// <advc.148>
int CvHandicapInfo::getAIAttitudeChangePercent() const
{
	return m_iAIAttitudeChangePercent;
} // </advc.148>

int CvHandicapInfo::getNumGoodies() const
{
	return m_iNumGoodies;
}

// advc.250a:
int CvHandicapInfo::getDifficulty() const { return m_iDifficulty; }

int CvHandicapInfo::getGoodies(int i) const
{
	FAssertBounds(0, getNumGoodies(), i);
	return m_piGoodies[i];
}

bool CvHandicapInfo::isFreeTechs(int i) const // advc.003t: Return type was int
{
	FAssertBounds(0, GC.getNumTechInfos(), i);
	return (m_pbFreeTechs != NULL ? m_pbFreeTechs[i] : false);
}

bool CvHandicapInfo::isAIFreeTechs(int i) const // advc.003t: Return type was int
{
	FAssertBounds(0, GC.getNumTechInfos(), i);
	return (m_pbAIFreeTechs != NULL ? m_pbAIFreeTechs[i] : false);
}
#if ENABLE_XML_FILE_CACHE
void CvHandicapInfo::read(FDataStreamBase* stream)
{
	base_t::read(stream); // advc.tag
	uint uiFlag=0;
	stream->Read(&uiFlag);

	stream->Read(&m_iFreeWinsVsBarbs);
	stream->Read(&m_iAnimalAttackProb);
	stream->Read(&m_iStartingLocationPercent);
	stream->Read(&m_iAdvancedStartPointsMod);
	stream->Read(&m_iStartingGold);
	stream->Read(&m_iFreeUnits);
	stream->Read(&m_iUnitCostPercent);
	stream->Read(&m_iBuildTimePercent);
	stream->Read(&m_iBaseGrowthThresholdPercent);
	stream->Read(&m_iGPThresholdPercent);
	stream->Read(&m_iCultureLevelPercent);
	// </advc.251>
	stream->Read(&m_iResearchPercent);
	// <advc.251>
	stream->Read(&m_iTrainPercent);
	stream->Read(&m_iConstructPercent);
	stream->Read(&m_iCreatePercent);
	// </advc.251>
	stream->Read(&m_iDistanceMaintenancePercent);
	stream->Read(&m_iNumCitiesMaintenancePercent);
	stream->Read(&m_iMaxNumCitiesMaintenance);
	stream->Read(&m_iColonyMaintenancePercent);
	stream->Read(&m_iMaxColonyMaintenance);
	stream->Read(&m_iCorporationMaintenancePercent);
	stream->Read(&m_iCivicUpkeepPercent);
	stream->Read(&m_iInflationPercent);
	stream->Read(&m_iHealthBonus);
	stream->Read(&m_iHappyBonus);
	stream->Read(&m_iAttitudeChange);
	stream->Read(&m_iNoTechTradeModifier);
	stream->Read(&m_iTechTradeKnownModifier);
	stream->Read(&m_iUnownedTilesPerGameAnimal);
	stream->Read(&m_iUnownedTilesPerBarbarianUnit);
	stream->Read(&m_iUnownedWaterTilesPerBarbarianUnit);
	stream->Read(&m_iUnownedTilesPerBarbarianCity);
	stream->Read(&m_iBarbarianCreationTurnsElapsed);
	stream->Read(&m_iBarbarianCityCreationTurnsElapsed);
	stream->Read(&m_iBarbarianCityCreationProb);
	stream->Read(&m_iAnimalCombatModifier);
	stream->Read(&m_iBarbarianCombatModifier);
	stream->Read(&m_iAIAnimalCombatModifier);
	stream->Read(&m_iAIBarbarianCombatModifier);
	stream->Read(&m_iStartingDefenseUnits);
	stream->Read(&m_iStartingWorkerUnits);
	stream->Read(&m_iStartingExploreUnits);
	stream->Read(&m_iAIStartingUnitMultiplier);
	stream->Read(&m_iAIStartingDefenseUnits);
	stream->Read(&m_iAIStartingWorkerUnits);
	stream->Read(&m_iAIStartingExploreUnits);
	stream->Read(&m_iBarbarianInitialDefenders);
	stream->Read(&m_iAIDeclareWarProb);
	stream->Read(&m_iAIWorkRateModifier);
	stream->Read(&m_iAIGrowthPercent);
	// <advc.251>
	stream->Read(&m_iAIGPThresholdPercent);
	stream->Read(&m_iAIResearchPercent);
	// </advc.251>
	stream->Read(&m_iAITrainPercent);
	stream->Read(&m_iAIWorldTrainPercent);
	stream->Read(&m_iAIConstructPercent);
	stream->Read(&m_iAIWorldConstructPercent);
	stream->Read(&m_iAICreatePercent);
	stream->Read(&m_iAIWorldCreatePercent);
	stream->Read(&m_iAICivicUpkeepPercent);
	stream->Read(&m_iAIUnitCostPercent);
	stream->Read(&m_iAIUnitSupplyPercent);
	stream->Read(&m_iAIUnitUpgradePercent);
	stream->Read(&m_iAIInflationPercent);
	stream->Read(&m_iAIWarWearinessPercent);
	//stream->Read(&m_iAIPerEraModifier);
	stream->Read(&m_iAIHandicapIncrementTurns); // advc.251
	stream->Read(&m_iAIAdvancedStartPercent);
	// <advc.148>
	stream->Read(&m_iAIAttitudeChangePercent); // </advc.148>
	stream->Read(&m_iNumGoodies);
	stream->Read(&m_iDifficulty); // advc.250a
	stream->ReadString(m_szHandicapName);
	SAFE_DELETE_ARRAY(m_piGoodies);
	m_piGoodies = new int[getNumGoodies()];
	stream->Read(getNumGoodies(), m_piGoodies);
	SAFE_DELETE_ARRAY(m_pbFreeTechs);
	m_pbFreeTechs = new bool[GC.getNumTechInfos()];
	stream->Read(GC.getNumTechInfos(), m_pbFreeTechs);
	SAFE_DELETE_ARRAY(m_pbAIFreeTechs);
	m_pbAIFreeTechs = new bool[GC.getNumTechInfos()];
	stream->Read(GC.getNumTechInfos(), m_pbAIFreeTechs);
}

void CvHandicapInfo::write(FDataStreamBase* stream)
{
	base_t::write(stream); // advc.tag
	uint uiFlag = 0;
	stream->Write(uiFlag);
	stream->Write(m_iFreeWinsVsBarbs);
	stream->Write(m_iAnimalAttackProb);
	stream->Write(m_iStartingLocationPercent);
	stream->Write(m_iAdvancedStartPointsMod);
	stream->Write(m_iStartingGold);
	stream->Write(m_iFreeUnits);
	stream->Write(m_iUnitCostPercent);
	// <advc.251>
	stream->Write(m_iBuildTimePercent);
	stream->Write(m_iBaseGrowthThresholdPercent);
	stream->Write(m_iGPThresholdPercent);
	stream->Write(m_iCultureLevelPercent);
	// </advc.251>
	stream->Write(m_iResearchPercent);
	// <advc.251>
	stream->Write(m_iTrainPercent);
	stream->Write(m_iConstructPercent);
	stream->Write(m_iCreatePercent);
	// </advc.251>
	stream->Write(m_iDistanceMaintenancePercent);
	stream->Write(m_iNumCitiesMaintenancePercent);
	stream->Write(m_iMaxNumCitiesMaintenance);
	stream->Write(m_iColonyMaintenancePercent);
	stream->Write(m_iMaxColonyMaintenance);
	stream->Write(m_iCorporationMaintenancePercent);
	stream->Write(m_iCivicUpkeepPercent);
	stream->Write(m_iInflationPercent);
	stream->Write(m_iHealthBonus);
	stream->Write(m_iHappyBonus);
	stream->Write(m_iAttitudeChange);
	stream->Write(m_iNoTechTradeModifier);
	stream->Write(m_iTechTradeKnownModifier);
	stream->Write(m_iUnownedTilesPerGameAnimal);
	stream->Write(m_iUnownedTilesPerBarbarianUnit);
	stream->Write(m_iUnownedWaterTilesPerBarbarianUnit);
	stream->Write(m_iUnownedTilesPerBarbarianCity);
	stream->Write(m_iBarbarianCreationTurnsElapsed);
	stream->Write(m_iBarbarianCityCreationTurnsElapsed);
	stream->Write(m_iBarbarianCityCreationProb);
	stream->Write(m_iAnimalCombatModifier);
	stream->Write(m_iBarbarianCombatModifier);
	stream->Write(m_iAIAnimalCombatModifier);
	stream->Write(m_iAIBarbarianCombatModifier);
	stream->Write(m_iStartingDefenseUnits);
	stream->Write(m_iStartingWorkerUnits);
	stream->Write(m_iStartingExploreUnits);
	stream->Write(m_iAIStartingUnitMultiplier);
	stream->Write(m_iAIStartingDefenseUnits);
	stream->Write(m_iAIStartingWorkerUnits);
	stream->Write(m_iAIStartingExploreUnits);
	stream->Write(m_iBarbarianInitialDefenders);
	stream->Write(m_iAIDeclareWarProb);
	stream->Write(m_iAIWorkRateModifier);
	stream->Write(m_iAIGrowthPercent);
	// <advc.251>
	stream->Write(m_iAIGPThresholdPercent);
	stream->Write(m_iAIResearchPercent);
	// </advc.251>
	stream->Write(m_iAITrainPercent);
	stream->Write(m_iAIWorldTrainPercent);
	stream->Write(m_iAIConstructPercent);
	stream->Write(m_iAIWorldConstructPercent);
	stream->Write(m_iAICreatePercent);
	stream->Write(m_iAIWorldCreatePercent);
	stream->Write(m_iAICivicUpkeepPercent);
	stream->Write(m_iAIUnitCostPercent);
	stream->Write(m_iAIUnitSupplyPercent);
	stream->Write(m_iAIUnitUpgradePercent);
	stream->Write(m_iAIInflationPercent);
	stream->Write(m_iAIWarWearinessPercent);
	//stream->Write(m_iAIPerEraModifier);
	stream->Write(m_iAIHandicapIncrementTurns); // advc.261
	stream->Write(m_iAIAdvancedStartPercent);
	stream->Write(m_iAIAttitudeChangePercent); // advc.148
	stream->Write(m_iNumGoodies);
	stream->Write(m_iDifficulty); // advc.250a
	stream->WriteString(m_szHandicapName);
	stream->Write(getNumGoodies(), m_piGoodies);
	stream->Write(GC.getNumTechInfos(), m_pbFreeTechs);
	stream->Write(GC.getNumTechInfos(), m_pbAIFreeTechs);
}
#endif
bool CvHandicapInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML)) // advc.tag
		return false;

	pXML->GetChildXmlValByName(&m_iFreeWinsVsBarbs, "iFreeWinsVsBarbs");
	pXML->GetChildXmlValByName(&m_iAnimalAttackProb, "iAnimalAttackProb");
	pXML->GetChildXmlValByName(&m_iStartingLocationPercent, "iStartingLocPercent");
	pXML->GetChildXmlValByName(&m_iAdvancedStartPointsMod, "iAdvancedStartPointsMod");
	pXML->GetChildXmlValByName(&m_iStartingGold, "iGold");
	pXML->GetChildXmlValByName(&m_iFreeUnits, "iFreeUnits");
	pXML->GetChildXmlValByName(&m_iUnitCostPercent, "iUnitCostPercent");
	// <advc.251>
	pXML->GetChildXmlValByName(&m_iBuildTimePercent, "iBuildTimePercent");
	pXML->GetChildXmlValByName(&m_iBaseGrowthThresholdPercent, "iBaseGrowthThresholdPercent");
	pXML->GetChildXmlValByName(&m_iGPThresholdPercent, "iGPThresholdPercent");
	pXML->GetChildXmlValByName(&m_iCultureLevelPercent, "iCultureLevelPercent");
	// </advc.251>
	pXML->GetChildXmlValByName(&m_iResearchPercent, "iResearchPercent");
	FAssert(m_iResearchPercent > 0); // advc
	// <advc.251>
	pXML->GetChildXmlValByName(&m_iTrainPercent, "iTrainPercent");
	pXML->GetChildXmlValByName(&m_iConstructPercent, "iConstructPercent");
	pXML->GetChildXmlValByName(&m_iCreatePercent, "iCreatePercent");
	// </advc.251>
	pXML->GetChildXmlValByName(&m_iDistanceMaintenancePercent, "iDistanceMaintenancePercent");
	pXML->GetChildXmlValByName(&m_iNumCitiesMaintenancePercent, "iNumCitiesMaintenancePercent");
	pXML->GetChildXmlValByName(&m_iMaxNumCitiesMaintenance, "iMaxNumCitiesMaintenance");
	pXML->GetChildXmlValByName(&m_iColonyMaintenancePercent, "iColonyMaintenancePercent");
	pXML->GetChildXmlValByName(&m_iMaxColonyMaintenance, "iMaxColonyMaintenance");
	pXML->GetChildXmlValByName(&m_iCorporationMaintenancePercent, "iCorporationMaintenancePercent");
	pXML->GetChildXmlValByName(&m_iCivicUpkeepPercent, "iCivicUpkeepPercent");
	pXML->GetChildXmlValByName(&m_iInflationPercent, "iInflationPercent");
	pXML->GetChildXmlValByName(&m_iHealthBonus, "iHealthBonus");
	pXML->GetChildXmlValByName(&m_iHappyBonus, "iHappyBonus");
	pXML->GetChildXmlValByName(&m_iAttitudeChange, "iAttitudeChange");
	pXML->GetChildXmlValByName(&m_iNoTechTradeModifier, "iNoTechTradeModifier");
	pXML->GetChildXmlValByName(&m_iTechTradeKnownModifier, "iTechTradeKnownModifier");
	pXML->GetChildXmlValByName(&m_iUnownedTilesPerGameAnimal, "iUnownedTilesPerGameAnimal");
	pXML->GetChildXmlValByName(&m_iUnownedTilesPerBarbarianUnit, "iUnownedTilesPerBarbarianUnit");
	pXML->GetChildXmlValByName(&m_iUnownedWaterTilesPerBarbarianUnit, "iUnownedWaterTilesPerBarbarianUnit");
	pXML->GetChildXmlValByName(&m_iUnownedTilesPerBarbarianCity, "iUnownedTilesPerBarbarianCity");
	pXML->GetChildXmlValByName(&m_iBarbarianCreationTurnsElapsed, "iBarbarianCreationTurnsElapsed");
	pXML->GetChildXmlValByName(&m_iBarbarianCityCreationTurnsElapsed, "iBarbarianCityCreationTurnsElapsed");
	pXML->GetChildXmlValByName(&m_iBarbarianCityCreationProb, "iBarbarianCityCreationProb");
	pXML->GetChildXmlValByName(&m_iAnimalCombatModifier, "iAnimalBonus");
	pXML->GetChildXmlValByName(&m_iBarbarianCombatModifier, "iBarbarianBonus");
	pXML->GetChildXmlValByName(&m_iAIAnimalCombatModifier, "iAIAnimalBonus");
	pXML->GetChildXmlValByName(&m_iAIBarbarianCombatModifier, "iAIBarbarianBonus");
	pXML->GetChildXmlValByName(&m_iStartingDefenseUnits, "iStartingDefenseUnits");
	pXML->GetChildXmlValByName(&m_iStartingWorkerUnits, "iStartingWorkerUnits");
	pXML->GetChildXmlValByName(&m_iStartingExploreUnits, "iStartingExploreUnits");
	pXML->GetChildXmlValByName(&m_iAIStartingUnitMultiplier, "iAIStartingUnitMultiplier");
	pXML->GetChildXmlValByName(&m_iAIStartingDefenseUnits, "iAIStartingDefenseUnits");
	pXML->GetChildXmlValByName(&m_iAIStartingWorkerUnits, "iAIStartingWorkerUnits");
	pXML->GetChildXmlValByName(&m_iAIStartingExploreUnits, "iAIStartingExploreUnits");
	pXML->GetChildXmlValByName(&m_iBarbarianInitialDefenders, "iBarbarianDefenders");
	pXML->GetChildXmlValByName(&m_iAIDeclareWarProb, "iAIDeclareWarProb");
	pXML->GetChildXmlValByName(&m_iAIWorkRateModifier, "iAIWorkRateModifier");
	pXML->GetChildXmlValByName(&m_iAIGrowthPercent, "iAIGrowthPercent");
	FAssert(m_iAIGrowthPercent > 0); // advc
	// <advc.251>
	pXML->GetChildXmlValByName(&m_iAIGPThresholdPercent, "iAIGPThresholdPercent");
	pXML->GetChildXmlValByName(&m_iAIResearchPercent, "iAIResearchPercent");
	FAssert(m_iAIResearchPercent > 0);
	// </advc.251>
	pXML->GetChildXmlValByName(&m_iAITrainPercent, "iAITrainPercent");
	FAssert(m_iAITrainPercent > 0); // advc
	pXML->GetChildXmlValByName(&m_iAIWorldTrainPercent, "iAIWorldTrainPercent");
	pXML->GetChildXmlValByName(&m_iAIConstructPercent, "iAIConstructPercent");
	FAssert(m_iAIConstructPercent > 0); // advc
	pXML->GetChildXmlValByName(&m_iAIWorldConstructPercent, "iAIWorldConstructPercent");
	pXML->GetChildXmlValByName(&m_iAICreatePercent, "iAICreatePercent");
	pXML->GetChildXmlValByName(&m_iAIWorldCreatePercent, "iAIWorldCreatePercent");
	pXML->GetChildXmlValByName(&m_iAICivicUpkeepPercent, "iAICivicUpkeepPercent");
	pXML->GetChildXmlValByName(&m_iAIUnitCostPercent, "iAIUnitCostPercent");
	pXML->GetChildXmlValByName(&m_iAIUnitSupplyPercent, "iAIUnitSupplyPercent");
	pXML->GetChildXmlValByName(&m_iAIUnitUpgradePercent, "iAIUnitUpgradePercent");
	pXML->GetChildXmlValByName(&m_iAIInflationPercent, "iAIInflationPercent");
	pXML->GetChildXmlValByName(&m_iAIWarWearinessPercent, "iAIWarWearinessPercent");
	//pXML->GetChildXmlValByName(&m_iAIPerEraModifier, "iAIPerEraModifier");
	// advc.251:
	pXML->GetChildXmlValByName(&m_iAIHandicapIncrementTurns, "iAIHandicapIncrementTurns");
	pXML->GetChildXmlValByName(&m_iAIAdvancedStartPercent, "iAIAdvancedStartPercent");
	// advc.148:
	pXML->GetChildXmlValByName(&m_iAIAttitudeChangePercent, "iAIAttitudeChangePercent");
	pXML->GetChildXmlValByName(&m_iDifficulty, "iDifficulty"); // advc.250a

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "Goodies"))
	{
		CvString* pszGoodyNames = NULL;
		pXML->SetStringList(&pszGoodyNames, &m_iNumGoodies);
		if (m_iNumGoodies > 0)
		{
			m_piGoodies = new int[m_iNumGoodies];
			for (int j = 0; j < m_iNumGoodies; j++)
				m_piGoodies[j] = pXML->FindInInfoClass(pszGoodyNames[j]);
		}
		else m_piGoodies = NULL;
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
		SAFE_DELETE_ARRAY(pszGoodyNames);
	}

	pXML->SetVariableListTagPair(&m_pbFreeTechs, "FreeTechs", GC.getNumTechInfos());
	pXML->SetVariableListTagPair(&m_pbAIFreeTechs, "AIFreeTechs", GC.getNumTechInfos());

	return true;
}

CvWorldInfo::CvWorldInfo() :
m_iDefaultPlayers(0),
m_iUnitNameModifier(0),
m_iTargetNumCities(0),
m_iNumFreeBuildingBonuses(0),
m_iBuildingClassPrereqModifier(0),
m_iMaxConscriptModifier(0),
m_iWarWearinessModifier(0),
m_iGridWidth(0),
m_iGridHeight(0),
m_iTerrainGrainChange(0),
m_iFeatureGrainChange(0),
m_iResearchPercent(/* advc: */ -1),
m_iTradeProfitPercent(0),
m_iDistanceMaintenancePercent(0),
m_iNumCitiesMaintenancePercent(0),
m_iColonyMaintenancePercent(0),
m_iCorporationMaintenancePercent(0),
m_iNumCitiesAnarchyPercent(0),
m_iAdvancedStartPointsMod(0)
{}

int CvWorldInfo::getUnitNameModifier() const
{
	return m_iUnitNameModifier;
}

int CvWorldInfo::getNumFreeBuildingBonuses() const
{
	return m_iNumFreeBuildingBonuses;
}

int CvWorldInfo::getMaxConscriptModifier() const
{
	return m_iMaxConscriptModifier;
}

int CvWorldInfo::getWarWearinessModifier() const
{
	return m_iWarWearinessModifier;
}

int CvWorldInfo::getGridWidth() const
{
	return m_iGridWidth;
}

int CvWorldInfo::getGridHeight() const
{
	return m_iGridHeight;
}

int CvWorldInfo::getTerrainGrainChange() const
{
	return m_iTerrainGrainChange;
}

int CvWorldInfo::getFeatureGrainChange() const
{
	return m_iFeatureGrainChange;
}

int CvWorldInfo::getTradeProfitPercent() const
{
	return m_iTradeProfitPercent;
}

int CvWorldInfo::getDistanceMaintenancePercent() const
{
	return m_iDistanceMaintenancePercent;
}

int CvWorldInfo::getNumCitiesMaintenancePercent() const
{
	return m_iNumCitiesMaintenancePercent;
}

int CvWorldInfo::getColonyMaintenancePercent() const
{
	return m_iColonyMaintenancePercent;
}

int CvWorldInfo::getCorporationMaintenancePercent() const
{
	return m_iCorporationMaintenancePercent;
}

int CvWorldInfo::getNumCitiesAnarchyPercent() const
{
	return m_iNumCitiesAnarchyPercent;
}

int CvWorldInfo::getAdvancedStartPointsMod() const
{
	return m_iAdvancedStartPointsMod;
}

bool CvWorldInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML))
		return false;

	pXML->GetChildXmlValByName(&m_iDefaultPlayers, "iDefaultPlayers");
	pXML->GetChildXmlValByName(&m_iUnitNameModifier, "iUnitNameModifier");
	pXML->GetChildXmlValByName(&m_iTargetNumCities, "iTargetNumCities");
	pXML->GetChildXmlValByName(&m_iNumFreeBuildingBonuses, "iNumFreeBuildingBonuses");
	pXML->GetChildXmlValByName(&m_iBuildingClassPrereqModifier, "iBuildingClassPrereqModifier");
	pXML->GetChildXmlValByName(&m_iMaxConscriptModifier, "iMaxConscriptModifier");
	pXML->GetChildXmlValByName(&m_iWarWearinessModifier, "iWarWearinessModifier");
	pXML->GetChildXmlValByName(&m_iGridWidth, "iGridWidth");
	pXML->GetChildXmlValByName(&m_iGridHeight, "iGridHeight");
	pXML->GetChildXmlValByName(&m_iTerrainGrainChange, "iTerrainGrainChange");
	pXML->GetChildXmlValByName(&m_iFeatureGrainChange, "iFeatureGrainChange");
	pXML->GetChildXmlValByName(&m_iResearchPercent, "iResearchPercent");
	FAssert(m_iResearchPercent > 0); // advc
	pXML->GetChildXmlValByName(&m_iTradeProfitPercent, "iTradeProfitPercent");
	pXML->GetChildXmlValByName(&m_iDistanceMaintenancePercent, "iDistanceMaintenancePercent");
	pXML->GetChildXmlValByName(&m_iNumCitiesMaintenancePercent, "iNumCitiesMaintenancePercent");
	pXML->GetChildXmlValByName(&m_iColonyMaintenancePercent, "iColonyMaintenancePercent");
	pXML->GetChildXmlValByName(&m_iCorporationMaintenancePercent, "iCorporationMaintenancePercent");
	pXML->GetChildXmlValByName(&m_iNumCitiesAnarchyPercent, "iNumCitiesAnarchyPercent");
	pXML->GetChildXmlValByName(&m_iAdvancedStartPointsMod, "iAdvancedStartPointsMod");

	return true;
}

CvClimateInfo::CvClimateInfo() :
m_iDesertPercentChange(0),
m_iJungleLatitude(0),
m_iHillRange(0),
m_iPeakPercent(0),
m_fSnowLatitudeChange(0.0f),
m_fTundraLatitudeChange(0.0f),
m_fGrassLatitudeChange(0.0f),
m_fDesertBottomLatitudeChange(0.0f),
m_fDesertTopLatitudeChange(0.0f),
m_fIceLatitude(0.0f),
m_fRandIceLatitude(0.0f)
{}

int CvClimateInfo::getDesertPercentChange() const
{
	return m_iDesertPercentChange;
}

int CvClimateInfo::getJungleLatitude() const
{
	return m_iJungleLatitude;
}

int CvClimateInfo::getHillRange() const
{
	return m_iHillRange;
}

int CvClimateInfo::getPeakPercent() const
{
	return m_iPeakPercent;
}

float CvClimateInfo::getSnowLatitudeChange() const
{
	return m_fSnowLatitudeChange;
}

float CvClimateInfo::getTundraLatitudeChange() const
{
	return m_fTundraLatitudeChange;
}

float CvClimateInfo::getGrassLatitudeChange() const
{
	return m_fGrassLatitudeChange;
}

float CvClimateInfo::getDesertBottomLatitudeChange() const
{
	return m_fDesertBottomLatitudeChange;
}

float CvClimateInfo::getDesertTopLatitudeChange() const
{
	return m_fDesertTopLatitudeChange;
}

float CvClimateInfo::getIceLatitude() const
{
	return m_fIceLatitude;
}

float CvClimateInfo::getRandIceLatitude() const
{
	return m_fRandIceLatitude;
}

bool CvClimateInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML))
		return false;

	pXML->GetChildXmlValByName(&m_iDesertPercentChange, "iDesertPercentChange");
	pXML->GetChildXmlValByName(&m_iJungleLatitude, "iJungleLatitude");
	pXML->GetChildXmlValByName(&m_iHillRange, "iHillRange");
	pXML->GetChildXmlValByName(&m_iPeakPercent, "iPeakPercent");

	pXML->GetChildXmlValByName(&m_fSnowLatitudeChange, "fSnowLatitudeChange");
	pXML->GetChildXmlValByName(&m_fTundraLatitudeChange, "fTundraLatitudeChange");
	pXML->GetChildXmlValByName(&m_fGrassLatitudeChange, "fGrassLatitudeChange");
	pXML->GetChildXmlValByName(&m_fDesertBottomLatitudeChange, "fDesertBottomLatitudeChange");
	pXML->GetChildXmlValByName(&m_fDesertTopLatitudeChange, "fDesertTopLatitudeChange");
	pXML->GetChildXmlValByName(&m_fIceLatitude, "fIceLatitude");
	pXML->GetChildXmlValByName(&m_fRandIceLatitude, "fRandIceLatitude");

	return true;
}

CvSeaLevelInfo::CvSeaLevelInfo() :
m_iSeaLevelChange(0),
m_iResearchPercent(-1) // advc.910
{}

int CvSeaLevelInfo::getSeaLevelChange() const
{
	return m_iSeaLevelChange;
}

bool CvSeaLevelInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML))
		return false;

	pXML->GetChildXmlValByName(&m_iSeaLevelChange, "iSeaLevelChange");
	// <advc.910>
	pXML->GetChildXmlValByName(&m_iResearchPercent, "iResearchPercent");
	FAssert(m_iResearchPercent > 0); // </advc.910>

	return true;
}
// advc.137: Include recommendation in description on Custom Game screen
CvWString CvSeaLevelInfo::getDescriptionInternal() const
{
	CvInitCore const& kInitCore = GC.getInitCore();
	if (kInitCore.getActivePlayer() == NO_PLAYER &&
		/*	This distinguishes Custom Game from Play Now.
			(Play Now doesn't have enough room for a recommendation,
			and doesn't allow player counts to be adjusted.) */
		kInitCore.getSlotStatus((PlayerTypes)0) == SS_OPEN)
	{
		CvWString szTag = m_szTextKey + L"_RECOMMEND";
		CvWString szText = gDLL->getText(szTag);
		// If a text key with recommendation was found, show it.
		if (szText != szTag)
			return szText;
	}
	return base_t::getDescriptionInternal();
}
