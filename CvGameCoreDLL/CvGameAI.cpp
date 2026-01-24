#include "CvGameCoreDLL.h"
#include "CvGameAI.h"
#include "CoreAI.h"
#include "CvCityAI.h"
#include "UWAIAgent.h"
#include "CvInfo_GameOption.h"
#include "CvInfo_Building.h" // advc.erai
#include "CvInfo_City.h" // advc.251

// <advc.007c>
#undef CVGAME_INSTANCE_FOR_RNG
#define CVGAME_INSTANCE_FOR_RNG (*this) // </advc.007c>



CvGameAI::CvGameAI()
{
	m_arExclusiveRadiusWeight.resize(3);
	AI_reset(true);
}


CvGameAI::~CvGameAI()
{
	AI_uninit();
}


void CvGameAI::AI_init()
{
	AI_reset();
	AI_sortOutUWAIOptions(false); // advc.104
}

/*	advc.104u: Parts of the AI don't seem to get properly initialized in scenarios.
	Not sure if this has always been the case, if it has to do with K-Mod changes to
	the turn order (team turns vs. player turns) or is a problem I introduced.
	Amendment: */
void CvGameAI::AI_initScenario()
{
	// Citizens not properly assigned
	for (PlayerAIIter<ALIVE> it; it.hasNext(); ++it)
	{
		FOR_EACH_CITYAI_VAR(c, *it)
		{
			/*  Added after getting failed assertions in CvCity::doTurn in the
				Europe1000AD scenario (I'm guessing due to production from Apostolic Palace). */
			for(int j = 0; j < NUM_YIELD_TYPES; j++)
			{
				YieldTypes y = (YieldTypes)j;
				c->setBaseYieldRate(y, c->calculateBaseYieldRate(y));
			}
			c->AI_assignWorkingPlots();
		}
	}
	/*	BtS seems to tolerate major civs w/o capitals (e.g. Italy in Lokolus's
		Earth1862AD scenario), but UWAI can't work with that. */
	for (PlayerIter<MAJOR_CIV> it; it.hasNext(); ++it)
	{
		if (it->getNumCities() > 1 && !it->hasCapital())
		{
			FErrorMsg("Major civ player w/o a capital");
			it->findNewCapital();
		}
	}
	if (getUWAI().isEnabled() || getUWAI().isEnabled(true))
	{
		for (TeamAIIter<MAJOR_CIV> it; it.hasNext(); ++it)
			it->uwai().turnPre();
	}
}

/*  advc.104: I'm repurposing the Aggressive AI option so that it disables UWAI
	in addition to the option's normal effect. A bit of a hack, but less invasive
	than changing all the isOption(AGGRESSIVE_AI) checks. Don't want two separate
	options because UWAI implies Aggressive AI. */
void CvGameAI::AI_sortOutUWAIOptions(bool bFromSaveGame)
{
	if(GC.getDefineINT("USE_KMOD_AI_NONAGGRESSIVE"))
	{
		m_uwai.setUseLegacyAI(true);
		setOption(GAMEOPTION_AGGRESSIVE_AI, false);
		return;
	}
	if(GC.getDefineINT("DISABLE_UWAI"))
	{
		m_uwai.setUseLegacyAI(true);
		setOption(GAMEOPTION_AGGRESSIVE_AI, true);
		return;
	}
	m_uwai.setInBackground(GC.getDefineINT("UWAI_IN_BACKGROUND") > 0);
	if(bFromSaveGame)
	{
		if(m_uwai.isEnabled() || m_uwai.isEnabled(true))
			setOption(GAMEOPTION_AGGRESSIVE_AI, true);
		return;
	}
	// If still not returned: settings according to Custom Game screen
	bool bUseKModAI = isOption(GAMEOPTION_AGGRESSIVE_AI);
	m_uwai.setUseLegacyAI(bUseKModAI);
	if(!bUseKModAI)
		setOption(GAMEOPTION_AGGRESSIVE_AI, true);
}


void CvGameAI::AI_uninit() {}


void CvGameAI::AI_reset(/* advc (as in CvGame): */ bool bConstructor)
{
	AI_uninit();
	//m_iPad = 0; // advc: unused
	m_iMaxCultureLevelPercent = 0; // advc.251
	if (!bConstructor)
	{
		AI_updateExclusiveRadiusWeight(); // advc.099b
		AI_updateVoteSourceEras(); // advc.erai
		AI_updateMaxCultureLevelPercent(); // advc.251
	}
}


void CvGameAI::AI_makeAssignWorkDirty()
{
	for (PlayerIter<ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		itPlayer->AI_makeAssignWorkDirty();
	}
}


void CvGameAI::AI_updateAssignWork()
{
	for (PlayerAIIter<HUMAN> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		itPlayer->AI_updateAssignWork();
	}
}


int CvGameAI::AI_combatValue(UnitTypes eUnit) /* K-Mod: */ const
{
	int iValue = 100;
	if (GC.getInfo(eUnit).getDomainType() == DOMAIN_AIR)
		iValue *= GC.getInfo(eUnit).getAirCombat();
	else
	{
		iValue *= GC.getInfo(eUnit).getCombat();

		iValue *= 100 + ((GC.getInfo(eUnit).getFirstStrikes() * 2 +
				GC.getInfo(eUnit).getChanceFirstStrikes()) * (GC.getCOMBAT_DAMAGE() / 5));
		iValue /= 100;
	}
	iValue /= getBestLandUnitCombat();
	return iValue;
}


int CvGameAI::AI_turnsPercent(int iTurns, int iPercent) const
{
	FAssert(iPercent > 0);
	if (iTurns != MAX_INT)
	{
		iTurns *= (iPercent);
		iTurns /= 100;
	}
	return std::max(1, iTurns);
}

// <advc.erai> (based on CvGame::getCurrentEra)
scaled CvGameAI::AI_getCurrEraFactor() const
{
	scaled r;
	PlayerAIIter<CIV_ALIVE> it;
	for (; it.hasNext(); ++it)
		r += it->AI_getCurrEraFactor();
	int const iCount = it.nextIndex();
	if (iCount > 0)
		return r / iCount;
	FAssert(iCount > 0);
	return -1;
}


EraTypes CvGameAI::AI_getVoteSourceEra(VoteSourceTypes eVS) const
{
	if (eVS == NO_VOTESOURCE) // By default, return the latest vote source.
	{
		EraTypes eLatestVSEra = NO_ERA;
		FOR_EACH_ENUM(VoteSource)
		{
			eLatestVSEra = std::max(eLatestVSEra,
					AI_getVoteSourceEra(eLoopVoteSource)); // recursion
		}
		return eLatestVSEra;
	}
	return m_aeVoteSourceEras.get(eVS);
}

// (Purely based on XML data; not serialized.)
void CvGameAI::AI_updateVoteSourceEras()
{
	m_aeVoteSourceEras.reset();
	FOR_EACH_ENUM(Building)
	{
		CvBuildingInfo const& kLoopBuilding = GC.getInfo(eLoopBuilding);
		VoteSourceTypes eVS = kLoopBuilding.getVoteSourceType();
		if (eVS == NO_VOTESOURCE)
			continue;
		EraTypes eMaxEra = NO_ERA;
		FOR_EACH_ENUM(Tech)
		{
			EraTypes const eLoopEra = GC.getInfo(eLoopTech).getEra();
			if (eLoopEra > eMaxEra)
			{
				if (kLoopBuilding.isTechRequired(eLoopTech))
					eMaxEra = eLoopEra;
			}
		}
		m_aeVoteSourceEras.set(eVS, eMaxEra);
	}
} // </advc.erai>

// advc.251:
void CvGameAI::AI_updateMaxCultureLevelPercent()
{
	int iThresh = GC.getInfo(CvCultureLevelInfo::finalCultureLevel()).
			getSpeedThreshold(getGameSpeedType());
	int iNormalThresh = 50000; // fallback
	GameSpeedTypes eNormal = NO_GAMESPEED;
	FOR_EACH_ENUM(GameSpeed)
	{
		if (GC.getInfo(eLoopGameSpeed).getResearchPercent() == 100)
		{
			if (eNormal != NO_GAMESPEED) // More than one is unexpected
			{
				eNormal = NO_GAMESPEED;
				break;
			}
			eNormal = eLoopGameSpeed;
		}
	}
	if (eNormal != NO_GAMESPEED)
	{
		int iTmp = GC.getInfo(CvCultureLevelInfo::finalCultureLevel()).
				getSpeedThreshold(eNormal);
		if (iTmp > 0)
			iNormalThresh = iTmp;
	}
	m_iMaxCultureLevelPercent = (iThresh * 100) / iNormalThresh;
}


/*	advc.099b: Between 0 and 1. Expresses AI confidence about winning culturally
	contested tiles that are within the working radius of its cities exclusively.
	Since the decay of tile culture isn't based on game speed, that confidence
	is greater on the slower speed settings. */
scaled CvGameAI::AI_exclusiveRadiusWeight(int iDist) const
{
	if(iDist >= (int)m_arExclusiveRadiusWeight.size())
		return 0;
	// Position 0 of the array is for iDist==-1 (unknown distance)
	if (iDist <= 0)
		iDist++;
	FAssert(iDist >= 0);
	return m_arExclusiveRadiusWeight[iDist];
}

// advc.115f:
void CvGameAI::AI_updateVictoryWeights()
{
	for (PlayerAIIter<CIV_ALIVE> it; it.hasNext(); ++it)
		it->AI_updateVictoryWeights();
}

// advc.009b:
 void CvGameAI::AI_updateExclusiveRadiusWeight()
 {
	FAssert(m_arExclusiveRadiusWeight.size() == 3);
	for (int i = 0; i < (int)m_arExclusiveRadiusWeight.size(); i++)
	{
		scaled rDistMultiplier;
		switch(i)
		{
		case 1: rDistMultiplier = 2; break;
		case 2: rDistMultiplier = 1; break;
		default: rDistMultiplier = fixp(1.5);
		}
		// High exponent; better use higher precision than usual.
		ScaledNum<32*1024> rBase = 1 - rDistMultiplier *
				per1000(GC.getDefineINT(CvGlobals::CITY_RADIUS_DECAY));
		FAssertMsg(rBase > 0, "CITY_RADIUS_DECAY too great; negative base for scaled::pow.");
		m_arExclusiveRadiusWeight[i] = 1 - rBase.pow(
				25 * per100(GC.getInfo(getGameSpeedType()).getGoldenAgePercent()));
	}
 }


void CvGameAI::read(FDataStreamBase* pStream)
{
	CvGame::read(pStream);

	uint uiFlag;
	pStream->Read(&uiFlag);
	// <advc>
	if (uiFlag < 1)
	{
		int iPad;
		pStream->Read(&iPad);
	} // </advc>
	// <advc.104>
	m_uwai.read(pStream);
	AI_sortOutUWAIOptions(true); // </advc.104>
}


void CvGameAI::write(FDataStreamBase* pStream)
{
	CvGame::write(pStream);

	uint uiFlag = 0;
	uiFlag = 1; // advc: Remove m_iPad
	pStream->Write(uiFlag);

	//pStream->Write(m_iPad); // advc: unused
	m_uwai.write(pStream); // advc.104
}
