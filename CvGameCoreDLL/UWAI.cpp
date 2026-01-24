#include "CvGameCoreDLL.h"
#include "UWAI.h"
#include "UWAIAgent.h"
#include "WarEvaluator.h"
#include "CoreAI.h"
#include "CvMap.h"

UWAI::UWAI() : m_bEnabled(false), m_bInBackground(false)
{
	FAssertMsg(CvGlobals::getInstance().getGamePointer() == NULL,
			"Accidental creation of another instance?");
}


void UWAI::invalidateUICache()
{
	WarEvaluator::clearCache();
}


void UWAI::setUseLegacyAI(bool b)
{
	m_bEnabled = !b;
}


void UWAI::setInBackground(bool b)
{
	m_bInBackground = b;
}


void UWAI::initNewPlayerInGame(PlayerTypes eNewPlayer)
{
	WarEvaluator::clearCache();
	GET_TEAM(eNewPlayer).uwai().init(TEAMID(eNewPlayer));
	GET_PLAYER(eNewPlayer).uwai().init(eNewPlayer);
}


void UWAI::processNewPlayerInGame(PlayerTypes eNewPlayer)
{
	GET_PLAYER(eNewPlayer).uwai().getCache().update(true);
	for (TeamAIIter<MAJOR_CIV> it; it.hasNext(); ++it)
		it->uwai().turnPre();
}


bool UWAI::isEnabled(bool bInBackground) const
{
	if (!m_bEnabled)
		return false;
	return (bInBackground == m_bInBackground);
}


void UWAI::read(FDataStreamBase* pStream)
{
	pStream->Read(&m_bEnabled);
}


void UWAI::write(FDataStreamBase* pStream) const
{
	pStream->Write(m_bEnabled);
}


int UWAI::maxSeaDist() const
{
	CvMap const& kMap = GC.getMap();
	int iR = 15;
	// That's true for Large and Huge maps
	if (kMap.getGridWidth() > 100 || kMap.getGridHeight() > 100)
		iR += 3;
	if (!kMap.isWrapX() && !kMap.isWrapY())
		iR = (iR * 6) / 5;
	return iR;
}


bool UWAI::isReady() const
{
	/*  In scenarios, CvTeamAI functions aren't properly called during the first
		turn. Should skip war planning in the first two turns to make sure that
		all AI data is properly initialized and updated. */
	return ((!GC.getGame().isScenario() && !GC.getInitCore().getScenario()) ||
			GC.getGame().getElapsedGameTurns() > 1);
}


#define MAKE_TAG_NAME(VAR) "UWAI_WEIGHT_"#VAR,
#define MAKE_REPORT_NAME(VAR) #VAR,

void UWAI::doXML()
{
	char const* const aszAspectTagNames[] = {
		DO_FOR_EACH_WAR_UTILITY_ASPECT(MAKE_TAG_NAME)
	};
	FAssert(ARRAYSIZE(aszAspectTagNames) == NUM_ASPECTS);
	for (int i = 0; i < NUM_ASPECTS; i++)
		m_aiXmlWeights.push_back(GC.getDefineINT(aszAspectTagNames[i]));

	char const* const aszAspectReportNames[] = {
		DO_FOR_EACH_WAR_UTILITY_ASPECT(MAKE_REPORT_NAME)
	};
	FAssert(ARRAYSIZE(aszAspectReportNames) == NUM_ASPECTS);
	for (int i = 0; i < NUM_ASPECTS; i++)
		m_aszAspectNames.push_back(aszAspectReportNames[i]);

	applyPersonalityWeight();
}


void UWAI::applyPersonalityWeight()
{
	int const iWeight = GC.getDefineINT("UWAI_PERSONALITY_PERCENT");
	if (iWeight == 100)
		return;
	std::vector<std::vector<int*>*> personalityMatrix;
	int iMembers = -1;
	/*	Hack to make this function compatible with unallocated
		CvLeaderHeadInfo member arrays */
	static int aiDevNull[100] = {};
	FOR_EACH_ENUM(LeaderHead)
	{
		CvLeaderHeadInfo& kLeader = GC.getInfo(eLoopLeaderHead);
		if (std::strcmp(kLeader.getType(), "LEADER_BARBARIAN") == 0)
			continue;
		/*  Basically serialize CvLeaderHeadInfo to avoid writing any more code
			per member variable than necessary. Tempting to use CvLeaderHeadInfo::
			write(FDataStreamBase*) for this, but some members have to be excluded. */
		int* aiPrimitiveMembers[]  = {
			&kLeader.m_iWonderConstructRand,
			&kLeader.m_iBaseAttitude, &kLeader.m_iBasePeaceWeight,
			&kLeader.m_iPeaceWeightRand, &kLeader.m_iWarmongerRespect,
			&kLeader.m_iEspionageWeight, &kLeader.m_iRefuseToTalkWarThreshold,
			&kLeader.m_iNoTechTradeThreshold, &kLeader.m_iTechTradeKnownPercent,
			&kLeader.m_iMaxGoldTradePercent, &kLeader.m_iMaxGoldPerTurnTradePercent,
			&kLeader.m_iCultureVictoryWeight, &kLeader.m_iSpaceVictoryWeight,
			&kLeader.m_iConquestVictoryWeight, &kLeader.m_iDominationVictoryWeight,
			&kLeader.m_iDiplomacyVictoryWeight, &kLeader.m_iMaxWarRand,
			&kLeader.m_iMaxWarNearbyPowerRatio, &kLeader.m_iMaxWarDistantPowerRatio,
			&kLeader.m_iMaxWarMinAdjacentLandPercent, &kLeader.m_iLimitedWarRand,
			&kLeader.m_iLimitedWarPowerRatio, &kLeader.m_iDogpileWarRand,
			&kLeader.m_iMakePeaceRand, &kLeader.m_iDeclareWarTradeRand,
			&kLeader.m_iDemandRebukedSneakProb, &kLeader.m_iDemandRebukedWarProb,
			&kLeader.m_iRazeCityProb, &kLeader.m_iBuildUnitProb,
			&kLeader.m_iBaseAttackOddsChange, &kLeader.m_iAttackOddsChangeRand,
			&kLeader.m_iWorseRankDifferenceAttitudeChange,
			&kLeader.m_iBetterRankDifferenceAttitudeChange,
			&kLeader.m_iCloseBordersAttitudeChange,
			&kLeader.m_iLostWarAttitudeChange, &kLeader.m_iAtWarAttitudeDivisor,
			&kLeader.m_iAtWarAttitudeChangeLimit, &kLeader.m_iAtPeaceAttitudeDivisor,
			&kLeader.m_iAtPeaceAttitudeChangeLimit, &kLeader.m_iSameReligionAttitudeChange,
			&kLeader.m_iSameReligionAttitudeDivisor, &kLeader.m_iSameReligionAttitudeChangeLimit,
			&kLeader.m_iDifferentReligionAttitudeChange, &kLeader.m_iDifferentReligionAttitudeDivisor,
			&kLeader.m_iDifferentReligionAttitudeChangeLimit,
			&kLeader.m_iBonusTradeAttitudeDivisor, &kLeader.m_iBonusTradeAttitudeChangeLimit,
			&kLeader.m_iOpenBordersAttitudeDivisor, &kLeader.m_iOpenBordersAttitudeChangeLimit,
			&kLeader.m_iDefensivePactAttitudeDivisor, &kLeader.m_iDefensivePactAttitudeChangeLimit,
			&kLeader.m_iShareWarAttitudeChange, &kLeader.m_iShareWarAttitudeDivisor,
			&kLeader.m_iShareWarAttitudeChangeLimit, &kLeader.m_iFavoriteCivicAttitudeChange,
			&kLeader.m_iFavoriteCivicAttitudeDivisor, &kLeader.m_iFavoriteCivicAttitudeChangeLimit,
			&kLeader.m_iDemandTributeAttitudeThreshold, &kLeader.m_iNoGiveHelpAttitudeThreshold,
			&kLeader.m_iTechRefuseAttitudeThreshold, &kLeader.m_iStrategicBonusRefuseAttitudeThreshold,
			&kLeader.m_iCityRefuseAttitudeThreshold, &kLeader.m_iNativeCityRefuseAttitudeThreshold, // advc.ctr
			&kLeader.m_iHappinessBonusRefuseAttitudeThreshold, &kLeader.m_iHealthBonusRefuseAttitudeThreshold,
			&kLeader.m_iMapRefuseAttitudeThreshold,
			&kLeader.m_iDeclareWarRefuseAttitudeThreshold, &kLeader.m_iDeclareWarThemRefuseAttitudeThreshold,
			&kLeader.m_iStopTradingRefuseAttitudeThreshold, &kLeader.m_iStopTradingThemRefuseAttitudeThreshold,
			&kLeader.m_iAdoptCivicRefuseAttitudeThreshold, &kLeader.m_iConvertReligionRefuseAttitudeThreshold,
			&kLeader.m_iOpenBordersRefuseAttitudeThreshold, &kLeader.m_iDefensivePactRefuseAttitudeThreshold,
			&kLeader.m_iPermanentAllianceRefuseAttitudeThreshold, &kLeader.m_iVassalRefuseAttitudeThreshold,
			&kLeader.m_iVassalPowerModifier, &kLeader.m_iFreedomAppreciation,
			&kLeader.m_iLoveOfPeace,
		};
		int const iPrimitiveMembers = ARRAYSIZE(aiPrimitiveMembers);
		std::vector<int*>* paiPersonalityVector = new std::vector<int*>(
				aiPrimitiveMembers, aiPrimitiveMembers + iPrimitiveMembers);
		int* aiFlavorValue = (kLeader.m_piFlavorValue == NULL ? aiDevNull :
				kLeader.m_piFlavorValue);
		FOR_EACH_ENUM(Flavor)
			paiPersonalityVector->push_back(&aiFlavorValue[eLoopFlavor]);
		int* aiContactRand = (kLeader.m_piContactRand == NULL ? aiDevNull :
				kLeader.m_piContactRand);
		FOR_EACH_ENUM(Contact)
			paiPersonalityVector->push_back(&aiContactRand[eLoopContact]);
		int* aiContactDelay = (kLeader.m_piContactDelay == NULL ? aiDevNull :
				kLeader.m_piContactDelay);
		FOR_EACH_ENUM(Contact)
			paiPersonalityVector->push_back(&aiContactDelay[eLoopContact]);
		int* aiMemoryDecayRand = (kLeader.m_piMemoryDecayRand == NULL ? aiDevNull :
				kLeader.m_piMemoryDecayRand);
		FOR_EACH_ENUM(Memory)
			paiPersonalityVector->push_back(&aiMemoryDecayRand[eLoopMemory]);
		int* aiMemoryAttitudePercent = (kLeader.m_piMemoryAttitudePercent == NULL ? aiDevNull :
				kLeader.m_piMemoryAttitudePercent);
		FOR_EACH_ENUM(Memory)
			paiPersonalityVector->push_back(&aiMemoryAttitudePercent[eLoopMemory]);
		int* aiNoWarAttitudeProb = (kLeader.m_piNoWarAttitudeProb == NULL ? aiDevNull :
				kLeader.m_piNoWarAttitudeProb);
		FOR_EACH_ENUM(Attitude)
			paiPersonalityVector->push_back(&aiNoWarAttitudeProb[eLoopAttitude]);
		int* aiUnitAIWeightModifier = (kLeader.m_piUnitAIWeightModifier == NULL ? aiDevNull :
				kLeader.m_piUnitAIWeightModifier);
		FOR_EACH_ENUM(UnitAI)
			paiPersonalityVector->push_back(&aiUnitAIWeightModifier[eLoopUnitAI]);
		int* aiImprovementWeightModifier = (kLeader.m_piImprovementWeightModifier == NULL ? aiDevNull :
				kLeader.m_piImprovementWeightModifier);
		FOR_EACH_ENUM(Improvement)
			paiPersonalityVector->push_back(&aiImprovementWeightModifier[eLoopImprovement]);
		personalityMatrix.push_back(paiPersonalityVector);
		FAssert(iMembers == -1 || iMembers == paiPersonalityVector->size());
		iMembers = (int)paiPersonalityVector->size();
		if (iWeight == 0) // Clear fav. civic and religion
		{
			kLeader.m_eFavoriteCivic = NO_CIVIC;
			kLeader.m_eFavoriteReligion = NO_RELIGION;
		}
	}
	for (int j = 0; j < iMembers; j++)
	{
		std::vector<scaled> arDistrib;
		for(size_t i = 0; i < personalityMatrix.size(); i++)
			arDistrib.push_back(*personalityMatrix[i]->at(j));
		scaled rMedianValue = stats::median(arDistrib);
		for (size_t i = 0; i < personalityMatrix.size(); i++)
		{
			*personalityMatrix[i]->at(j) = ((rMedianValue * (100 - iWeight) +
					(*personalityMatrix[i]->at(j)) * iWeight) / 100).round();
		}
	}
	for (size_t i = 0; i < personalityMatrix.size(); i++)
		delete personalityMatrix[i];
}
