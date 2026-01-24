#include "CvGameCoreDLL.h"
#include "WarUtilityAspect.h"
#include "UWAICache.h"
#include "UWAIReport.h"
#include "WarEvalParameters.h"
#include "UWAIAgent.h"
#include "MilitaryAnalyst.h"
#include "CoreAI.h"
#include "CvCityAI.h"
#include "CvUnitAI.h"
#include "CvSelectionGroupAI.h"
#include "CvDeal.h"
#include "PlotRadiusIterator.h"
#include "CvArea.h"
#include "CvInfo_GameOption.h"
#include "CvInfo_Building.h" // Just for vote-related info

using std::vector;
using std::pair;
using std::make_pair;
typedef UWAICache::City City;

/*	These player and team data are accessed a lot in this file. Refer to the agent
	as "we" and to the current rival (set by evaluate(MilitaryAnalyst const&))
	as "they" -- for brevity, also in comments. */
#define kWe				(getAgentPlayer())
#define kOurTeam		(getAgentTeam())
#define eWe				(kWe.getID())
#define eOurTeam		(kOurTeam.getID())
#define kThey			(getRivalPlayer())
#define eThey			(kThey.getID())
#define kTheirTeam		(GET_TEAM(eThey))
#define eTheirTeam		(TEAMID(eThey))
#define kWeAI			(kWe.uwai())
#define kOurPersonality	(GC.getInfo(kWe.getPersonalityType()))


WarUtilityAspect::WarUtilityAspect(WarEvalParameters const& kParams)
:	m_kParams(kParams), m_kAgentTeam(GET_TEAM(kParams.getAgent())),
	m_kReport(kParams.getReport()), m_kGame(GC.AI_getGame()),
	m_eGameEra(m_kGame.getCurrentEra()),
	m_rGameEraAIFactor(m_kGame.AI_getCurrEraFactor()),
	m_kSpeed(GC.getInfo(m_kGame.getGameSpeedType())),
	m_iU(0)
{
	reset();
}


void WarUtilityAspect::reset()
{
	//PROFILE_FUNC(); // About 100,000 calls per game turn. Not a concern.
	m_pMilitaryAnalyst = NULL;
	m_pAgentPlayer = NULL;
	m_pAgentCache = NULL;
	resetRival();
}


void WarUtilityAspect::resetRival()
{
	m_pRivalPlayer = NULL;
	m_aeAgentConquersFromRival.clear();
	m_eTowardRival = m_eTowardAgent = NO_ATTITUDE;
	m_iDiploTowardRival = m_iDiploTowardAgent = -1;
}


int WarUtilityAspect::evaluate(MilitaryAnalyst const& kMilitaryAnalyst)
{
	PROFILE_FUNC();
	this->m_pMilitaryAnalyst = &kMilitaryAnalyst;
	m_pAgentPlayer = &(GET_PLAYER(kMilitaryAnalyst.getAgentPlayer()));
	m_pAgentCache = &m_pAgentPlayer->uwai().getCache();

	int iOverallUtility = preEvaluate();
	bool const bOnlyWarParties = concernsOnlyWarParties();
	for (PlayerIter<MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> itRival(eOurTeam);
		itRival.hasNext(); ++itRival)
	{
		if (bOnlyWarParties && !kMilitaryAnalyst.isPartOfAnalysis(itRival->getID()))
			continue;
		int iPerRivalUtility = evaluate(itRival->getID());
		if (iPerRivalUtility != 0)
		{
			log("*%s from %s: %d*", aspectName(),
					m_kReport.leaderName(itRival->getID(), 16), iPerRivalUtility);
		}
	}
	if (iOverallUtility != 0)
	{
		log("*%s (from no one in particular): %d*", aspectName(), iOverallUtility);
		m_iU += iOverallUtility;
	}
	scaled rXMLAdjust = getUWAI().aspectWeight(xmlID());
	if (m_iU != 0 && rXMLAdjust != 1)
	{
		log("Adjustment from XML: %d percent", rXMLAdjust.getPercent());
		m_iU = (m_iU * rXMLAdjust).round();
	}
	reset();
	return utility();
}


int WarUtilityAspect::evaluate(PlayerTypes eRivalPlayer)
{
	m_pRivalPlayer = &(GET_PLAYER(eRivalPlayer));
	/*	Should never use human attitude, but an error value like MIN_INT
		wouldn't get caught. Better to use a sane value (0 -> Cautious). */
	m_iDiploTowardAgent = (kThey.isHuman() ? 0 : kThey.AI_getAttitudeVal(eWe));
	/*	If we're human, it can mean that another AI player is evaluating war
		from the point of view of a human rival. Should therefore also
		disregard our attitude. */
	m_iDiploTowardRival = (kWe.isHuman() ? 0 : kWe.AI_getAttitudeVal(eThey));
	/*	In the very early game, war preparations take a long time, and diplo
		will often improve during that time b/c of "years of peace". If this
		brings attitude to Pleased, the war is usually off, and the preparations
		(very costly this early) are for nothing (unless there's an alt. target;
		not considered here). Need to anticipate the change in attitude. */
	/*	No worries once preparations are well underway or when asked to
		declare war immediately (or when already at war) */
	if (!kWe.isHuman() && m_kParams.getPreparationTime() > 5 &&
		m_kGame.gameTurnProgress() < fixp(0.18) &&
		kWe.AI_getPeaceAttitude(eThey) == 0 &&
		kOurTeam.AI_getAtPeaceCounter(eTheirTeam) * 2 >
		kOurPersonality.getAtPeaceAttitudeDivisor())
	{
		m_iDiploTowardRival++;
	}
	m_eTowardRival = (kWe.isHuman() ? ATTITUDE_CAUTIOUS :
			kWe.AI_getAttitudeFromValue(m_iDiploTowardRival));
	/*	advc.130o: If recently received tribute, we're pleased as far
		as war plans go. */
	if (!kWe.isHuman() && !m_kParams.isConsideringPeace() &&
		kWe.AI_getMemoryCount(eThey, MEMORY_ACCEPT_DEMAND) > 0 &&
		kThey.AI_getMemoryCount(eWe, MEMORY_MADE_DEMAND_RECENT) > 0)
	{
		m_eTowardRival = std::max(m_eTowardRival, ATTITUDE_PLEASED);
	}
	m_eTowardAgent = (kThey.isHuman() ? ATTITUDE_CAUTIOUS :
			kThey.AI_getAttitudeFromValue(m_iDiploTowardAgent));
	CitySet const& kWeConquer = militAnalyst().conqueredCities(eWe);
	for (CitySetIter it = kWeConquer.begin(); it != kWeConquer.end(); ++it)
	{
		if (militAnalyst().lostCities(eThey).count(*it) > 0)
			m_aeAgentConquersFromRival.push_back(*it);
	}
	int iUtilityBefore = m_iU;
	evaluate();
	resetRival();
	return m_iU - iUtilityBefore;
}


int WarUtilityAspect::preEvaluate() { return 0; }


bool WarUtilityAspect::concernsOnlyWarParties() const { return true; }


char const* WarUtilityAspect::aspectName() const
{
	if (m_kReport.isMute()) // Don't waste time processing the string then
		return getUWAI().aspectName(xmlID());
	// Convert from upper case to mixed case and replace underscores with spaces
	static CvString szBuffer;
	szBuffer = getUWAI().aspectName(xmlID());
	for (uint i = 0; i < szBuffer.length(); i++)
	{
		if (szBuffer[i] == '_')
			szBuffer[i] = ' ';
		if (i > 0 && szBuffer[i - 1] != ' ')
			szBuffer[i] = static_cast<char>(::tolower(szBuffer[i]));
	}
	return szBuffer.GetCString();
}

#if !DISABLE_UWAI_REPORT
void WarUtilityAspect::log(char const* fmt, ...) const
{
	/*	The time spent in this function is negligible when the report is muted,
		but the call overhead (up to 100,000 calls per game turn) and branching
		could still be harmful. Might want to profile e.g. ScaledNum::getPercent.
		Can't really be helped though so long as the report is enabled and disabled
		through XML. */
	//PROFILE_FUNC();
	if (m_kReport.isMute())
		return;
	va_list args;
	va_start(args, fmt);
	std::string szMsg = CvString::formatv(fmt, args);
	va_end(args);
	m_kReport.log(szMsg.c_str());
}
#endif

scaled WarUtilityAspect::normalizeUtility(scaled rUtilityTeamOnTeam,
	TeamTypes eOther) const
{
	if (eOther == NO_TEAM)
		eOther = eTheirTeam;
	return rUtilityTeamOnTeam /
			(GET_TEAM(eOther).getNumMembers() * kOurTeam.getNumMembers());
}


scaled WarUtilityAspect::netLostRivalAssetScore(PlayerTypes eTo,
	scaled* prTotalScore, TeamTypes eIgnoreGains) const
{
	PROFILE_FUNC();
	scaled rNetLoss;
	scaled rTotal;
	// Cities that they lose
	/*for (int i = 0; i < kThey.uwai().getCache().size(); i++) {
		City* pCacheCity = kThey.uwai().getCache().getCity(i);*/
	/*	In large games, looking up their cities is faster than a pass through their
		whole cache. */
	CitySet const& kTheyLose = militAnalyst().lostCities(eThey);
	FOR_EACH_CITY(pCity, kThey)
	{
		City const* pCacheCity = kThey.uwai().getCache().lookupCity(pCity->plotNum());
		if (pCacheCity == NULL)
			continue;
		if (!kOurTeam.AI_deduceCitySite(*pCity))
			continue;
		/*	Their cached value accounts for GP, but we're not supposed to see those.
			(Their cache contains some other info we shouldn't see, but nothing
			crucial I think.) */
		scaled rAssetScore = pCacheCity->getAssetScore()
				- 4 * pCity->getNumGreatPeople();
		if (kTheyLose.count(pCacheCity->getID()) > 0 &&
			(eTo == NO_PLAYER ||
			militAnalyst().conqueredCities(eTo).count(pCacheCity->getID()) > 0))
		{
			rNetLoss += rAssetScore;
			// Losing the capital is bad (but not all that bad b/c the Palace relocates)
			if (pCity->isCapital())
				rNetLoss += 4;
		}
		else if (pCity->isCapital())
			rTotal += 8;
		// National wonders other than Palace are invisible to us
		rTotal += rAssetScore;
	}
	// Cities that they gain
	CitySet const& kTheyConqer = militAnalyst().conqueredCities(eThey);
	for (CitySetIter it = kTheyConqer.begin(); it != kTheyConqer.end(); ++it)
	{
		City const* pCacheCity = kThey.uwai().getCache().lookupCity(*it);
		if (pCacheCity == NULL)
			continue;
		if ((eTo == NO_PLAYER ||
			militAnalyst().lostCities(eTo).count(pCacheCity->getID()) > 0) &&
			pCacheCity->city().getTeam() != eIgnoreGains)
		{
			/*	Their cache doesn't account for GP settled in cities of a
				third party (unless espionage visibility), so we
				don't subtract NumGreatPeople.
				I would rather use a score based on our visibility, however,
				the AssetScore from our cache would compute distance maintenance,
				tile culture and trade routes as if we were conquering the city,
				which is far worse.
				The clean solution - computing asset scores for all pairs of
				(oldOwner, newOwner) seems excessive. */
			rNetLoss -= pCacheCity->getAssetScore();
		}
	}
	// Non-city losses (nothing to be gained here) ...
	rNetLoss += lossesFromNukes(eThey, eTo);
	rTotal.increaseTo(rNetLoss);
	scaled const rBlockadeMultiplier = lossesFromBlockade(eThey, eTo);
	scaled const rFromBlockade = fixp(0.1) * rBlockadeMultiplier * (rTotal - rNetLoss);
	rNetLoss += rFromBlockade;
	rNetLoss += lossesFromFlippedTiles(eThey, eTo); // advc.035
	if (prTotalScore != NULL)
		*prTotalScore = rTotal;
	return rNetLoss;
}


scaled WarUtilityAspect::lossesFromBlockade(PlayerTypes eVictim, PlayerTypes eTo) const
{
	PROFILE_FUNC();
	// Blockades can be painful for maritime empires ...
	CvPlayerAI const& kVictim = GET_PLAYER(eVictim);
	scaled rTotalEnemyFleetPow;
	for (PlayerIter<MAJOR_CIV> itEnemy; itEnemy.hasNext(); ++itEnemy)
	{
		PlayerTypes const eEnemy = itEnemy->getID();
		if (!militAnalyst().isWar(eVictim, eEnemy) ||
			(eTo != NO_PLAYER && eTo != eEnemy))
		{
			continue;
		}
		// Cheat; see UWAICache::updateRelativeNavyPower.
		MilitaryBranch const& kEnemyFleet = *GET_PLAYER(eEnemy).uwai().getCache().
				getPowerValues()[FLEET];
		// I don't think blockading at war happens much before Frigates
		//if (!kEnemyFleet.canBombard()) // Let's cheat a little less (use eObserver arg)
		UnitTypes const eTypicalEnemyWarShip = kEnemyFleet.getTypicalUnit(eOurTeam);
		if (eTypicalEnemyWarShip == NO_UNIT ||
			GC.getInfo(eTypicalEnemyWarShip).getBombardRate() <= 0)
		{
			continue;
		}
		scaled rEnemyFleetPow = kEnemyFleet.power() +
				militAnalyst().gainedPower(eEnemy, FLEET);
		if (rEnemyFleetPow > 100) // Unlikely to send any ships otherwise
			rTotalEnemyFleetPow += rEnemyFleetPow;
	}
	scaled rEnemyToVictimPowRatio = 2;
	MilitaryBranch const& kVictimFleet = *kVictim.uwai().getCache().
			getPowerValues()[FLEET];
	// Allies of the victim? I suppose they wouldn't necessarily defend its shores.
	scaled rVictimFleetPow = kVictimFleet.power() +
			militAnalyst().gainedPower(eVictim, FLEET);
	if (rVictimFleetPow > 0)
		rEnemyToVictimPowRatio = rTotalEnemyFleetPow / rVictimFleetPow;
	if (rEnemyToVictimPowRatio < fixp(1.25)) // Enemies won't bring all their units
		return 0;
	int iCoastalPop = 0;
	int iTotalPop = 0;
	int iCoastalCities = 0;
	CitySet const& kVictimLosses = militAnalyst().lostCities(eVictim);
	FOR_EACH_CITY(pCity, kVictim)
	{
		if (!pCity->isRevealed(eOurTeam) || kVictimLosses.count(pCity->plotNum()) > 0)
			continue;
		int const iPop = pCity->getPopulation();
		iTotalPop += iPop;
		if (pCity->isCoastal())
		{
			iCoastalPop += iPop;
			iCoastalCities++;
		}
	}
	if (iCoastalCities <= 0)
		return 0;
	scaled rAvgCoastalPop(iCoastalPop, iCoastalCities);
	scaled rAttackFactor = rEnemyToVictimPowRatio - 1;
	rAttackFactor.clamp(0, 1);
	scaled rPopFactor(iCoastalPop, iTotalPop);
	// Small cities tend to work few coastal tiles (b/c land tiles are better)
	scaled rVulnerabilityFactor = scaled::min(1, fixp(0.1) + rAvgCoastalPop / 25);
	return rAttackFactor * rPopFactor * rVulnerabilityFactor;
}


scaled WarUtilityAspect::lossesFromNukes(PlayerTypes eVictim, PlayerTypes eSource) const
{
	int const iVictimCitiesLost = (int)militAnalyst().lostCities(eVictim).size();
	CvPlayerAI const& kVictim = GET_PLAYER(eVictim);
	UWAICache const& kVictimCache = kVictim.uwai().getCache();
	// Mild cheat; the total asset score is a pretty abstract number.
	scaled rScorePerCity = kVictimCache.totalAssetScore() /
			std::max(1, kVictim.getNumCities() - iVictimCitiesLost);
	/*	Assume that cities lost to eSource are more likely to take a hit
		(in the process of being conquered by eSource), and such a hit
		doesn't hurt the victim beyond the loss of the city. The remaining nukes
		are more likely to hit large cities, but some will also hit minor cities
		for tactical reasons, or no cities at all; this ought to even out.
		Also assume that the non-lost core cities are always a bit (1/3) afflicted. */
	scaled rHits = (eSource == NO_PLAYER ? militAnalyst().getNukesSufferedBy(eVictim) :
			militAnalyst().getNukedCities(eSource, eVictim));
	rHits = std::max(fixp(1/3.) * rHits, rHits - iVictimCitiesLost * fixp(0.75));
	scaled rLossRate = fixp(0.35);
	// More pessimistic if we're the victim
	if (eVictim == eWe)
		rLossRate = fixp(0.45);
	scaled r = rHits * (kVictimCache.canScrubFallout() ?
			rLossRate - fixp(0.05) : rLossRate + fixp(0.05)) * rScorePerCity;
	if (r >= fixp(0.5))
	{
		log("Lost score of %s for cities hit: %d; assets per city: %d; "
				"cities hit: %.2f; ", m_kReport.leaderName(eVictim),
				r.round(), rScorePerCity.uround(), rHits.getFloat());
	}
	return r;
}

// advc.035:
scaled WarUtilityAspect::lossesFromFlippedTiles(PlayerTypes eVictim,
	PlayerTypes eTo) const
{
	if (!GC.getDefineBOOL(CvGlobals::OWN_EXCLUSIVE_RADIUS))
		return 0;
	scaled r;
	int iVictimLostTiles = 0;
	vector<TeamTypes> aeTo;
	if (eTo == NO_PLAYER)
	{	// (Milit. analyst will filter out invalid teams below)
		for (TeamIter<MAJOR_CIV> it; it.hasNext(); ++it)
			aeTo.push_back(it->getID());
	}
	else aeTo.push_back(TEAMID(eTo));
	UWAICache const& kVictimCache = GET_PLAYER(eVictim).uwai().getCache();
	for (size_t i = 0; i < aeTo.size(); i++)
	{
		if (militAnalyst().isWar(aeTo[i], TEAMID(eVictim)))
			iVictimLostTiles += kVictimCache.numPlotsLostAtWar(aeTo[i]);
	}
	int const iRivalMembers = kTheirTeam.getNumMembers();
	if (std::abs(iVictimLostTiles) <= 4 * iRivalMembers)
		return 0;
	int iVictimLandTiles = GET_PLAYER(eVictim).getTotalLand();
	int const iWeightFactor = 125;
	r = scaled(iWeightFactor * iVictimLostTiles, std::max(5, iVictimLandTiles));
	// Tiles are counted per team, but this function gets called once per rival player.
	r /= iRivalMembers;
	return r;
}


scaled WarUtilityAspect::conqAssetScore(bool bMute) const
{
	if (ourConquestsFromThem().empty())
		return 0;
	scaled r;
	for (size_t i = 0; i < ourConquestsFromThem().size(); i++)
	{
		City const& kCacheCity = *ourCache().lookupCity(ourConquestsFromThem()[i]);
		// Capture gold negligible b/c it gets reduced if a city is young
		if (kCacheCity.city().isAutoRaze(eWe))
			continue;
		r += kCacheCity.getAssetScore();
	}
	if (r <= 0)
		return 0;
	/*	A little extra for buildings that may survive and things that are there
		but invisible to us. */
	r *= fixp(1.1);
	if (!bMute)
	{
		log("%d cities conquered from %s", (int)ourConquestsFromThem().size(),
				m_kReport.leaderName(eThey));
		log("Total asset score: %d", r.round());
	}
	/*	Reduce score to account for culture pressure from the current owner unless
		we expect that civ to eliminated or to be our vassal.
		Tbd.: Would better to apply this per area, i.e. no culture pressure if we
		take all their cities in one area. Then again, we may not know about
		all their cities in the area. */
	int const iTheirRemainingCities = kThey.getNumCities()
			- (int)militAnalyst().lostCities(eThey).size();
	if (militAnalyst().getCapitulationsAccepted(eOurTeam).count(eTheirTeam) == 0 &&
		iTheirRemainingCities > 0)
	{
		/*	Mean of a quotient based just on how many cities we conquer and another
			based on how much of them remains. Then shift that toward 1 a little. */
		r *= (4 * (1 - (scaled(1, 1 + (int)ourConquestsFromThem().size()) +
				scaled(iTheirRemainingCities, kThey.getNumCities())) / 2) + 1) / 5;
		if (!bMute)
			log("Asset score reduced to %d due to culture pressure", r.round());
	}
	else
	{
		/*	The penalties for the owner's culture applied by asset score are a
			bit high in this case. */
		r *= fixp(1.2);
		if (!bMute)
			log("Asset score increased to %d b/c enemy culture neutralized", r.round());
	}
	return r;
}


scaled WarUtilityAspect::remainingCityRatio(PlayerTypes ePlayer) const
{
	int const iCurrCities = GET_PLAYER(ePlayer).getNumCities();
	if (iCurrCities <= 0)
		return 0;
	return 1 - scaled((int)militAnalyst().lostCities(ePlayer).size(), iCurrCities);
}


scaled WarUtilityAspect::partnerUtilFromTech() const
{
	// Some overlap with the "Tech Groundbreaker" code in CvPlayerAI::AI_techValue
	if (m_kGame.isOption(GAMEOPTION_NO_TECH_TRADING))
		return 0;
	// How good our and their attitude needs to be at least to allow tech trade
	AttitudeTypes eOurAttitudeThresh = techRefuseThresh(eWe);
	AttitudeTypes eTheirAttitudeThresh = techRefuseThresh(eThey);
	if (!kThey.isHuman() && !kWe.isHuman() &&
		(towardThem() < eOurAttitudeThresh || towardUs() < eTheirAttitudeThresh))
	{
		log("No tech trade b/c of attitude");
		return 0;
	}
	int iWeCanOffer = 0;
	int iTheyCanOffer = 0;
	// Don't rely on human research progress
	bool const bCanSeeResearch = (!kThey.isHuman() && kWe.canSeeResearch(eThey));
	FOR_EACH_ENUM2(Tech, eTech)
	{
		bool bWeHaveIt = (kOurTeam.isHasTech(eTech) ||
				kOurTeam.getResearchProgress(eTech) > 0);
		bool bTheyHaveIt = (kTheirTeam.isHasTech(eTech) ||
				(bCanSeeResearch && kTheirTeam.getResearchProgress(eTech) > 0));
		if (bWeHaveIt && !bTheyHaveIt)
			iWeCanOffer++;
		else if (bTheyHaveIt && !bWeHaveIt)
			iTheyCanOffer++;
	}
	if ((iWeCanOffer == 0 || iTheyCanOffer == 0) &&
		std::abs(iWeCanOffer - iTheyCanOffer) > 4)
	{
		log("No utility from tech trade b/c progress too far apart");
		return 0;
	}
	// Humans are good at making tech trades work
	int iHumanExtra = 0;
	if (kWe.isHuman())
		iHumanExtra += 3;
	if (kThey.isHuman())
		iHumanExtra += 3;
	if (iHumanExtra > 0)
		log("Tech trade bonus for human civs: %d", iHumanExtra);
	// Use their commerce to determine potential for future tech trade
	scaled rTheyToUsCommerceRatio = kOurTeam.AI_estimateYieldRate(eThey, YIELD_COMMERCE) /
			(kOurTeam.AI_estimateYieldRate(eWe, YIELD_COMMERCE) + scaled::epsilon());
	if (rTheyToUsCommerceRatio > 1)
		rTheyToUsCommerceRatio.flipFraction();
	scaled r = SQR(rTheyToUsCommerceRatio) * (17 + iHumanExtra);
	scaled rNearFutureTrades = std::min(iWeCanOffer, iTheyCanOffer);
	if (rNearFutureTrades > 1) // Just 1 isn't likely to result in a trade
	{
		log("Added utility for %d foreseeable trades", rNearFutureTrades.floor());
		// Humans tend to make trades immediately, and avoid certain techs entirely.
		if (kThey.isHuman())
			rNearFutureTrades /= 2;
		r += fixp(10/3.) * scaled::min(3, rNearFutureTrades);
	}
	if (r > 0)
		log("Tech trade utility: %d", r.round());
	/*	The above assumes that tech trade is only inhibited by overlapping research
		and diverging tech rates. If there's also AI distrust, it's worse. */
	if ((!kWe.isHuman() && towardThem() != ATTITUDE_FRIENDLY) ||
		(!kThey.isHuman() && towardUs() != ATTITUDE_FRIENDLY))
	{
		log("Tech trade utility halved for distrust");
		r /= 2;
	}
	if (m_kGame.isOption(GAMEOPTION_NO_TECH_BROKERING))
		r *= fixp(2/3.);
	return r * kWeAI.amortizationMultiplier();
}


AttitudeTypes WarUtilityAspect::techRefuseThresh(PlayerTypes ePlayer) const
{
	// Humans are callous
	if (GET_PLAYER(ePlayer).isHuman())
		return ATTITUDE_FURIOUS;
	// The XML value is mostly ANNOYED; they'll trade at one above that.
	return (AttitudeTypes)(kOurPersonality.getTechRefuseAttitudeThreshold() + 1);
}


scaled WarUtilityAspect::partnerUtilFromTrade() const
{
	scaled rGoldVal;
	scaled rTradeValFromGold;
	int iResourceTrades = 0;
	int const iDefaultTimeHorizon = 25;
	FOR_EACH_DEAL(pDeal)
	{
		if (!pDeal->isBetween(eWe, eThey) || !pDeal->isEverCancelable(eWe))
			continue;
		bool const bGift = (pDeal->getGivesList(eWe).getLength() <= 0);
		// Handle OB and DP separately (AI_dealVal just counts cities for those)
		bool bSkip = false;
		bool bWeReceiveResource = false;
		FOR_EACH_TRADE_ITEM(pDeal->getReceivesList(eWe))
		{
			if (CvDeal::isDual(pItem->m_eItemType))
			{
				bSkip = true;
				continue;
			}
			if (pItem->m_eItemType == TRADE_RESOURCES)
			{
				bWeReceiveResource = true;
				if (bSkip)
					break; // Know everything we need
			}
			else FAssert(bSkip || pItem->m_eItemType == TRADE_GOLD_PER_TURN);
		}
		if (bSkip)
			continue;
		// Count only the first four resource trades
		if (bWeReceiveResource)
		{
			iResourceTrades++;
			int const iMaxResourceTrades = 4;
			if (iResourceTrades >= iMaxResourceTrades)
			{
				log("Skipped resource trades in excess of %d", iMaxResourceTrades);
				continue;
			}
		}
		/*	AI_dealVal is supposed to be gold-per-turn, but seems
			a bit high for that; hence divide by 1.5. */
		scaled rDealVal = kWe.AI_dealVal(eThey, pDeal->getReceivesList(eWe)) /
				(fixp(1.5) * GC.getDefineINT(CvGlobals::PEACE_TREATY_LENGTH));
		if (!bWeReceiveResource)
		{
			int const iMaxTradeValFromGold = 40;
			if (rTradeValFromGold + rDealVal > iMaxTradeValFromGold)
			{
				log("Trade value from gold capped at %d", iMaxTradeValFromGold);
				rDealVal = iMaxTradeValFromGold - rTradeValFromGold;
			}
			rTradeValFromGold += rDealVal;
		}
		log("GPT value for a %s trade: %d", (bWeReceiveResource ? "resource" : "gold"),
				rDealVal.round());
		/*	Similar approach in CvPlayerAI::AI_stopTradingTradeVal, which
			doubles the trade values of gifts. */
		if (!bGift)
			rDealVal /= 2;
		// This actually restores the result of AI_dealVal
		scaled rTimeHorizon = iDefaultTimeHorizon;
		// Don't trust young deals (could be human manipulation)
		int const iTurnsToCancel = pDeal->turnsToCancel();
		if (iTurnsToCancel > 0)
		{
			rTimeHorizon = scaled(iTurnsToCancel + 10, 2);
			log("Reduced time horizon for recent deal: %d", rTimeHorizon.round());
		}
		rDealVal *= rTimeHorizon;
		rGoldVal += rDealVal;
	}
	log("Net gold value of resource and gold: %d", rGoldVal.round());
	// Based on TradeUtil::calculateTradeRoutes (Python)
	scaled rTradeRouteProfit;
	FOR_EACH_CITY(pCity, kWe)
	{
		for (int i = 0; i < pCity->getTradeRoutes(); i++)
		{
			CvCity const* pTradeCity = pCity->getTradeCity(i);
			if (pTradeCity == NULL)
				continue;
			if (pTradeCity->getOwner() != eThey)
				continue;
			/*	Division accounts for other potential trade partners,
				in the worst case, domestic. */
			rTradeRouteProfit += pCity->calculateTradeProfit(pTradeCity) / fixp(2.5);
		}
	}
	int const iTradeRouteProfitCap = 40;
	if (rTradeRouteProfit > iTradeRouteProfitCap)
	{
		log("Per-turn Trade route profit capped at %d", iTradeRouteProfitCap);
		rTradeRouteProfit = iTradeRouteProfitCap;
	}
	else if (rTradeRouteProfit > 0)
		log("Per-turn trade route profit: %d", rTradeRouteProfit.uround());
	return kWeAI.tradeValToUtility(rGoldVal + rTradeRouteProfit * iDefaultTimeHorizon) *
			kWeAI.amortizationMultiplier();
}


scaled WarUtilityAspect::partnerUtilFromMilitary() const
{
	if ((kThey.isHuman() || towardUs() < ATTITUDE_FRIENDLY) &&
		!kOurTeam.isDefensivePact(eTheirTeam))
	{
		return 0;
	}
	scaled r = kThey.uwai().getCache().getPowerValues()[ARMY]->power() /
			(ourCache().getPowerValues()[ARMY]->power() + scaled::epsilon());
	log("Their military relative to ours: %d percent", r.getPercent());
	/*	Only count their future military support as 10% b/c there are a lot of ifs
		despite friendship/ DP */
	return scaled::min(r * 10, 10);
}


void GreedForAssets::evaluate()
{
	PROFILE_FUNC();
	scaled const rConqScore = conqAssetScore(false);
	if (rConqScore <= 0)
		return;
	scaled const rPresentScore = ourCache().totalAssetScore();
	log("Score for present assets: %d", rPresentScore.round());
	/*	(Count non-wonder buildings for rPresentScore? May construct those
		in the conquered cities too eventually ...) */
	scaled rUtility = scaled::min(650, 350 * rConqScore /
			scaled::max(rPresentScore, 1));
	log("Base utility from assets: %d", rUtility.round());
	scaled const rTeamSzMult = teamSizeMultiplier();
	if (rTeamSzMult != 1)
		log("Team size multiplier: %d percent", rTeamSzMult.getPercent());
	scaled const rCompetitionMult = competitionMultiplier();
	if (rCompetitionMult != 1)
		log("Competition multiplier: %d percent", rCompetitionMult.getPercent());
	scaled const rOverextensionMult = overextensionMult();
	scaled const rDefensibilityMult = defensibilityMult();
	log("Cost modifiers: %d percent for overextension, %d for defensibility",
			rOverextensionMult.getPercent(), rDefensibilityMult.getPercent());
	rUtility *= rCompetitionMult * rTeamSzMult *
			(1 - rOverextensionMult - rDefensibilityMult);
	// Greed shouldn't motivate peaceful leaders too much
	if (kWe.AI_getPeaceWeight() >= 7)
	{
		int iCap = 260 - 10 * kWe.AI_getPeaceWeight();
		if (rUtility > iCap)
		{
			rUtility = iCap;
			log("Greed capped at %d b/c of peace-weight", iCap);
		}
	}
	int const iLoveOfPeace = kOurPersonality.getLoveOfPeace();
	if (iLoveOfPeace > 0)
	{
		rUtility *= std::max(fixp(0.1), 1 - per100(iLoveOfPeace));
		log("Greed reduced by %d percent b/c of love of peace", iLoveOfPeace);
	}
	/*	Cap utility per conquered city. Relevant mostly for One-City
		Challenge, but may also matter on dense maps in the early game. */
	rUtility.decreaseTo(120 * ourConquestsFromThem().size());
	m_iU += std::max(0, rUtility.round());
}


scaled GreedForAssets::overextensionMult() const
{
	/*	Number-of-city maintenance and increased civic upkeep from conquered cities
		are difficult to predict; only partially covered by AssetScore.
		Look at our current expenses: are we already overextended? */
	// Don't mind paying 25% for city maintenance
	scaled r = fixp(-0.25);
	scaled const rOurIncome = kOurTeam.AI_estimateYieldRate(eWe, YIELD_COMMERCE);
	if (rOurIncome > 0)
	{
		// Expenses excluding unit cost and supply
		scaled rOurMaintenance = per100(kWe.calculateInflationRate() + 100) *
				(kWe.getTotalMaintenance() + kWe.getCivicUpkeep(NULL, true));
		r += rOurMaintenance / rOurIncome;
		log("Rel. maint. = %d / %d = %d percent",
				rOurMaintenance.uround(), rOurIncome.uround(),
				(rOurMaintenance / rOurIncome).getPercent());
	}
	// Can happen in later-era start if a civ immediately changes civics/ religion
	else log("Failed to estimate income");
	return scaled::max(0, r);
}


scaled GreedForAssets::defensibilityMult() const
{
	// Check for hostile third parties
	scaled const rRemoteness = medianDistFromOurConquests(eWe);
	scaled rThreatFactor;
	for (PlayerIter<MAJOR_CIV> it; it.hasNext(); ++it)
	{
		rThreatFactor += threatToCities(it->getID(), rRemoteness);
	}
	if (rRemoteness > 5 && !m_kGame.isOption(GAMEOPTION_NO_BARBARIANS) &&
		m_rGameEraAIFactor < fixp(1.5))
	{
		scaled rBarbarianThreat = 1;
		if (m_kGame.isOption(GAMEOPTION_RAGING_BARBARIANS))
			rBarbarianThreat *= fixp(1.5);
		rBarbarianThreat *= rRemoteness / 60;
		rBarbarianThreat.decreaseTo(fixp(0.25));
		if (rBarbarianThreat >= fixp(0.005))
		{
			log("Threat factor from barbarians: %d percent",
					rBarbarianThreat.getPercent());
		}
		rThreatFactor += rBarbarianThreat;
	}
	if (rThreatFactor <= 0)
		return 0;
	// A little arcane
	int const iMaxWarMinAdjLand = kOurPersonality.getMaxWarMinAdjacentLandPercent();
	int iPersonalityPercent = 12 + 3 * iMaxWarMinAdjLand;
	/*	In BtS, 0 has a special role b/c it ignores shared borders entirely.
		That's a bit too extreme, but I'm setting it extra low.
		4 is rare (Liz, SiBull, Toku); I'm reinforcing that a bit as well. */
	if (iMaxWarMinAdjLand == 0)
		iPersonalityPercent /= 2;
	if (iMaxWarMinAdjLand >= 3)
		iPersonalityPercent += 5;
	log("Personality factor %d (MaxWarMinAdjLand %d); threat factor %d",
			iPersonalityPercent, iMaxWarMinAdjLand, rThreatFactor.getPercent());
	return std::min(fixp(0.5), rThreatFactor.sqrt() * per100(iPersonalityPercent));
}


scaled GreedForAssets::threatToCities(PlayerTypes ePlayer, scaled rRemoteness) const
{
	CvPlayerAI& kPlayer = GET_PLAYER(ePlayer);
	if (kPlayer.isAVassal() || !kOurTeam.isHasMet(kPlayer.getTeam()) ||
		kPlayer.getTeam() == eOurTeam || kPlayer.getTeam() == eTheirTeam ||
		!kPlayer.hasCapital() || GET_TEAM(kPlayer.getTeam()).AI_isAvoidWar(eOurTeam))
	{
		return 0;
	}
	// Add a constant b/c power ratios can be volatile in the early game
	scaled rPlayerPower = 150 +
			kPlayer.uwai().getCache().getPowerValues()[ARMY]->power();
	scaled rOurPower = 150 +
			ourCache().getPowerValues()[ARMY]->power();
	// Use present power if kPlayer not part of the analysis
	if (militAnalyst().isPartOfAnalysis(ePlayer))
	{
		rPlayerPower += militAnalyst().gainedPower(kPlayer.getID(), ARMY);
		rOurPower += militAnalyst().gainedPower(eWe, ARMY);
	}
	/*	Skip civs that aren't currently a threat.
		Add some utility for weak civs? Could use the conquered cities as a
		bridgehead for a later war. Too uncertain I think. */
	if (2 * rOurPower > 3 * rPlayerPower)
		return 0;
	// Only worry about civs that are closer to our conquests than we are
	scaled rPlayerDist = medianDistFromOurConquests(ePlayer);
	if (5 * rPlayerDist >= 4 * rRemoteness || rPlayerDist > 10)
		return 0;
	log("Dangerous civ near our conquests: %s (dist. ratio %d/%d)",
			m_kReport.leaderName(kPlayer.getID()),
			rPlayerDist.uround(), rRemoteness.uround());
	scaled rPowerRatio = scaled::max(0,
			rPlayerPower / scaled::max(10, rOurPower) - fixp(0.1));
	return SQR(rPowerRatio);
}


scaled GreedForAssets::medianDistFromOurConquests(PlayerTypes ePlayer) const
{
	CvPlayerAI const& kPlayer = GET_PLAYER(ePlayer);
	vector<scaled> arDistances;
	for (size_t i = 0; i < ourConquestsFromThem().size(); i++)
	{
		/*	For a human, it's almost always easy to tell whether one civ is
			closer to a set of cities than another, so the AI figuring it out
			through (possibly) a vision cheat isn't an issue for me. */
		City* pCacheCity = kPlayer.uwai().getCache().lookupCity(
				ourConquestsFromThem()[i]);
		if (pCacheCity == NULL)
			continue;
		/*	OK to use enormous distances for cities that shouldn't affect defensibility;
			median value can handle outliers. */
		int iDist = (pCacheCity->canReachByLand() ? pCacheCity->getDistance() : 100);
		if (iDist < 0) // unreachable
			iDist = 1000;
		arDistances.push_back(iDist);
	}
	scaled r = 1000;
	if (!arDistances.empty())
		r = stats::median(arDistances);
	return r;
}


scaled GreedForAssets::competitionMultiplier() const
{
	// (Shouldn't have to compute this otherwise)
	FAssert(ourConquestsFromThem().size() > 0);
	int const iTheirCities = kThey.getNumCities();
	/*	Only need this in the early game (I hope), and only if there are
		few cities to go around. */
	if (m_kGame.gameTurnProgress() >= fixp(0.25) || iTheirCities >= 5 ||
		iTheirCities <= 0 || ourConquestsFromThem().size() <= 0)
	{
		return 1;
	}
	/*	Milit. analysis already takes our war allies into account, and tells us
		which cities the allies conquer, and which ones we get. However, this is
		based on just one simulation trajectory, and if they (the target) have
		few cities, we might actually get none at all. Compute a penalty for
		our GreedForAssets utility in order to account for that risk.
		This should reduce early-game dogpiling. */
	int iCompetitors = 0;
	for (PlayerIter<FREE_MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> itAlly(eOurTeam);
		itAlly.hasNext(); ++itAlly)
	{
		CvPlayer const& kAlly = *itAlly;
		if (!militAnalyst().isWar(kAlly.getID(), eThey))
			continue;
		/*	Only worry if MilitaryAnalyst says that kAlly conquers
			at least as much as we do */
		int iAllyConqFromThem = 0;
		CitySet const& kAllyConquers = militAnalyst().conqueredCities(kAlly.getID());
		for (CitySetIter it = kAllyConquers.begin(); it != kAllyConquers.end(); ++it)
		{
			if (militAnalyst().lostCities(eThey).count(*it) > 0)
				iAllyConqFromThem++;
		}
		if (iAllyConqFromThem >= (int)ourConquestsFromThem().size())
			iCompetitors++;
	}
	FAssert(iTheirCities > iCompetitors); // Because we conquer at least 1 as well
	return scaled::max(0, 1 - scaled(iCompetitors, iTheirCities));
}


scaled GreedForAssets::teamSizeMultiplier() const
{
	/*	To account for team-on-team warfare having a somewhat slower pace than
		player-on-player, meaning that further conquests tend to happen after the
		time horizon of the simulation. (A longer horizon could be too costly
		computationally.) And to account for military assistance within a team
		being a bit underestimated by InvasionGraph (which can't be helped). */
	int iTeamSz = std::min(kOurTeam.getAliveCount(), kTheirTeam.getAliveCount());
	return std::min(fixp(1.43), (1 + scaled(iTeamSz).sqrt()) / 2);
}


void GreedForVassals::evaluate()
{
	TeamSet const& kNewVassals = militAnalyst().getCapitulationsAccepted(eOurTeam);
	if (kNewVassals.count(eTheirTeam) <= 0 ||
		!kWe.hasCapital() || !kThey.hasCapital()) // Will need the capitals later
	{
		return;
	}
	scaled rOurIncome = kOurTeam.AI_estimateYieldRate(eWe, YIELD_COMMERCE);
	rOurIncome.increaseTo(8);
	/*	Their commerce may be lower than now at the end of the war.
		(Don't try to estimate our own post-war commerce though.) */
	scaled const rTheirCityRatio = remainingCityRatio(eThey);
	log("Ratio of cities kept by the vassal: cr=%d percent",
			rTheirCityRatio.getPercent());
	// Vassal commerce to account for tech they might research for us
	scaled const rVassalIncome = kOurTeam.AI_estimateYieldRate(eThey, YIELD_COMMERCE);
	scaled const rVassalToOurIncome = rVassalIncome * rTheirCityRatio / rOurIncome;
	log("Rel. income of vassal %s = %d percent = cr * %d / %d",
			m_kReport.leaderName(eThey), rVassalToOurIncome.getPercent(),
			rVassalIncome.uround(), rOurIncome.uround());
	scaled rUtilityFromTechTrade = 100 * rVassalToOurIncome;
	// Tech they already have
	scaled const rTechScore = ourCache().vassalTechScore(eThey);
	log("Vassal score from tech they have in advance of us: %d",
			rTechScore.uround());
	rUtilityFromTechTrade += kWeAI.tradeValToUtility(rTechScore);
	log("Utility from vassal tech and income (still to be reduced): %d",
			rUtilityFromTechTrade.uround());
	/*	If they're much more advanced than us, we won't be able to trade for
		all their tech. */
	rUtilityFromTechTrade.decreaseTo(100);
	/*	Reduced a lot b/c of uncertainty and delays in tech trades. Expect human
		master to fare a bit better. */
	scaled rUtility = (kOurTeam.isHuman() ? fixp(0.5) : fixp(0.35)) *
			rUtilityFromTechTrade;
	scaled rUtilityFromResources = ourCache().vassalResourceScore(eThey);
	log("Resource score: %d", rUtilityFromResources.uround());
	// Expect just +1.5 commerce per each of their cities from trade routes
	scaled rUtilityFromTR = fixp(1.5) * kThey.getNumCities() / rOurIncome;
	log("Trade route score: %d", rUtilityFromTR.uround());
	// These trades are pretty safe bets; treated as 75% probable
	rUtility += fixp(0.75) * rTheirCityRatio * (rUtilityFromResources + rUtilityFromTR);
	int iOurVassalPlayers = PlayerIter<ALIVE,VASSAL_OF>::count(eOurTeam);
	for (TeamSetIter it = kNewVassals.begin(); it != kNewVassals.end(); ++it)
		iOurVassalPlayers += GET_TEAM(*it).getNumMembers();
	// Diminishing returns from having additional trade partners
	rUtility /= scaled(iOurVassalPlayers).sqrt();
	CvArea const& kOurArea = kWe.getCapital()->getArea();
	CvArea const& kTheirArea = kThey.getCapital()->getArea();
	bool bUsefulArea = false; // Look for a future enemy to dogpile on
	if (&kOurArea == &kTheirArea)
	{
		for (PlayerAIIter<FREE_MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> itTarget(eOurTeam);
			itTarget.hasNext(); ++itTarget)
		{
			CvPlayerAI const& kTarget = *itTarget;
			CvTeamAI const& kTargetTeam = GET_TEAM(kTarget.getTeam());
			if (3 * kTarget.getNumCities() <= std::max(1, kWe.getNumCities()) ||
				militAnalyst().isEliminated(kTarget.getID()) ||
				militAnalyst().hasCapitulated(kTargetTeam.getID()))
			{
				continue;
			}
			FAssert(kNewVassals.count(kTargetTeam.getID()) <= 0);
			if (kTarget.getCapital()->isArea(kOurArea) &&
				(!kTargetTeam.AI_isAvoidWar(eOurTeam) ||
				!kOurTeam.AI_isAvoidWar(kTargetTeam.getID(), true)))
			{
				bUsefulArea = true;
				break;
			}
		}
	}
	scaled const rTheirPower = kThey.uwai().getCache().getPowerValues()[ARMY]->power();
	scaled const rOurPower = ourCache().getPowerValues()[ARMY]->power();
	log("Their army/ ours: %d/%d", rTheirPower.round(), rOurPower.round());
	// Multiplier reflects coordination problems and lack of commitment
	scaled rUtilityFromMilitary = 45 * rTheirCityRatio * rTheirPower /
			scaled::max(rOurPower, 10);
	log("Base utility from military: %d", rUtilityFromMilitary.uround());
	if (!bUsefulArea)
	{
		rUtilityFromMilitary /= 2;
		log("Utility halved b/c vassal not in a useful area");
	}
	rUtilityFromMilitary.decreaseTo(30);
	rUtility += rUtilityFromMilitary;
	if (!kWe.AI_atVictoryStage(AI_VICTORY_CONQUEST3))
		rUtility -= 5; // To account for the diplo penalty from capitulated vassals
	int iLoveOfPeace = kOurPersonality.getLoveOfPeace();
	if (iLoveOfPeace > 0)
	{
		rUtility *= std::max(fixp(0.1), 1 - per100(iLoveOfPeace));
		log("Greed reduced by %d percent b/c of love of peace", iLoveOfPeace);
	}
	m_iU += std::max(0, rUtility.round());
}


void GreedForSpace::evaluate()
{
	/*	If they lose cities, but aren't eliminated, they'll try to settle sites
		aggressively; doesn't help us. */
	if (!militAnalyst().isEliminated(eThey) ||
		ourCache().numAdjacentLandPlots(eThey) <= 0)
	{
		return;
	}
	int const iOurCities = std::max(1, kWe.getNumCities());
	int const iOurSites = std::min(iOurCities, kWe.AI_getNumCitySites());
	int iTheirSites = 0;
	/*	Would be too brazen a cheat to ignore visibility here.
		(And might encourage very early wars.) */
	for (int i = 0; i < kThey.AI_getNumCitySites(); i++)
	{
		CvPlot const& kSite = kThey.AI_getCitySite(i);
		if (kSite.isRevealed(eOurTeam))
			iTheirSites++;
		else
		{
			FOR_EACH_ADJ_PLOT(kSite)
			{
				if (pAdj->isRevealed(eOurTeam))
				{
					iTheirSites++;
					break;
				}
			}
		}
	}
	// Expect to raze only when we have to
	for (size_t i = 0; i < ourConquestsFromThem().size(); i++)
	{
		if (ourCache().lookupCity(ourConquestsFromThem()[i])->city().
			isAutoRaze(eWe))
		{
			iTheirSites++;
		}
	}
	/*	All sites could still be claimed by third parties or could be just barely
		worth settling. Their sites are extra uncertain because they could be far
		away from our capital. */
	scaled rExpectedSites = iOurSites + fixp(0.63) * iTheirSites;
	// Don't expect to more than double our territory in the foreseeable future
	rExpectedSites.decreaseTo(iOurCities);
	// Increase in sites relative to our current city count
	scaled rIncr = (rExpectedSites - iOurSites) / iOurCities;
	FAssert(rIncr >= 0 && rIncr <= 1);
	scaled rUtility = (40 * rIncr * kWeAI.amortizationMultiplier());
	if (rUtility.abs() >= fixp(0.5))
	{
		log("Their orphaned sites: %d, our current sites: %d, our current cities: %d",
				iTheirSites, iOurSites, iOurCities);
		m_iU += rUtility.round();
	}
}


void GreedForCash::evaluate()
{
	if (militAnalyst().isEliminated(eThey) ||
		ourCache().numReachableCities(eThey) <= 0)
	{
		return;
	}
	int const iTheyLoseToUs = ourConquestsFromThem().size();
	if (iTheyLoseToUs <= 0)
		return;
	int iWeLoseToThem = 0;
	CitySet const& kTheyConquer = militAnalyst().conqueredCities(eThey);
	for (CitySetIter it = kTheyConquer.begin(); it != kTheyConquer.end(); ++it)
	{
		if (militAnalyst().lostCities(eWe).count(*it) > 0)
		{
			iWeLoseToThem++;
			if (iWeLoseToThem >= iTheyLoseToUs)
				return;
		}
	}
	log("Adding utility for future reparations");
	m_iU += normalizeUtility(4).uround(); // Only one team member will pay
}


void Loathing::evaluate()
{
	PROFILE_FUNC();
	if (kWe.isHuman())
		return;
	/*	Only count this if at war with them? No, that could lead to us joining
		a war despite not contributing anything to their losses.
		Can't tell who causes their losses. */
	if ((towardThem() > ATTITUDE_FURIOUS &&
		(kOurTeam.isAtWar(eTheirTeam) ||
		/*	I.e. only loath them if a) furious or b) at peace and worst enemy.
			Rationale: When at war, they'll usually become our worst enemy
			(and I don't want loathing to count virtually always once at war),
			whereas Furious attitude is not a matter of course even when at war. */
		kOurTeam.AI_getWorstEnemy() != eTheirTeam)) ||
		kTheirTeam.isCapitulated() || // Capitulated is as good as dead
		// Don't commit suicide just to inconvenience an enemy
		militAnalyst().isEliminated(eWe))
	{
		return;
	}
	int const iVengefulness = kWeAI.vengefulness();
	if (iVengefulness == 0)
	{
		log("No loathing b/c of our leader's personality");
		return;
	}
	scaled rLossRating = lossRating();
	rLossRating.clamp(-1, 1);
	if (rLossRating.abs() <= 0)
		return;
	rLossRating *= 100;
	log("Loss rating for %s: %d", m_kReport.leaderName(eThey), rLossRating.round());
	log("Our vengefulness: %d", iVengefulness);
	// Utility proportional to iVengefulness and rLossRating would be too extreme
	scaled rFromLosses = fixp(10/3.) * (iVengefulness * rLossRating.abs()).sqrt();
	if (rLossRating.isNegative())
		rFromLosses.flipSign();
	// We like to bring in war allies against our nemesis
	int iJointDoW = 0;
	PlyrSet const& kWarsDeclaredOnThem = militAnalyst().getWarsDeclaredOn(eThey);
	for (PlayerIter<FREE_MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> itAlly(eOurTeam);
		itAlly.hasNext(); ++itAlly)
	{
		if (kWarsDeclaredOnThem.count(itAlly->getID()) > 0)
		{
			log("Joint DoW by %s", m_kReport.leaderName(itAlly->getID()));
			iJointDoW++;
		}
	}
	scaled rFromDiplo = 10 * scaled(iVengefulness).sqrt() * iJointDoW;
	int iFreeCivPlayers = countFreeRivals<false>();
	if (!kOurTeam.isAVassal())
		iFreeCivPlayers += kOurTeam.getNumMembers();
	/*	Obsessing over one enemy is unwise if there are many potential enemies.
		Rounded down b/c it would be a bit too high otherwise. */
	int const iFreeCivDivisor = scaled(std::max(1, iFreeCivPlayers)).sqrt().floor();
	log("Divisor from number of free rival players (%d): %d",
			iFreeCivPlayers, iFreeCivDivisor);
	m_iU += ((rFromLosses + rFromDiplo) /
			// Count Loathing only once per team member
			(iFreeCivDivisor * kOurTeam.getNumMembers())).round();
}

/*	How much they're losing compared with what we have. I.e. we don't much care
	for kicking them when they're down. */
scaled Loathing::lossRating() const
{
	if (militAnalyst().isEliminated(eThey) ||
		militAnalyst().hasCapitulated(eTheirTeam))
	{
		log("Loss rating based on score");
		return scaled(m_kGame.getPlayerScore(eThey),
				std::max(10, m_kGame.getPlayerScore(eWe)));
	}
	/*	We mainly care about how much they lose relative to what we have; only
		use their present status as a sanity check, so that we don't get excited
		if we're doing badly and they suffer some minor losses. */
	scaled rTheirAssets;
	scaled rTheirLostAssets = netLostRivalAssetScore(NO_PLAYER, &rTheirAssets);
	rTheirAssets.increaseTo(1);
	CitySet const& kTheyLose = militAnalyst().lostCities(eThey);
	for (CitySetIter it = kTheyLose.begin(); it != kTheyLose.end(); ++it)
	{
		City const* pCacheCity = kThey.uwai().getCache().lookupCity(*it);
		if (pCacheCity == NULL)
			continue;
		/*	Already included in theirLostScore, but count it once more for the
			symbolic value. */
		if (pCacheCity->city().isCapital())
			rTheirLostAssets += 4;
	}
	scaled const rOurAssets = scaled::max(1, ourCache().totalAssetScore());
	scaled rTheirAssetsToOurs = scaled::min(rTheirLostAssets / rOurAssets,
			3 * rTheirLostAssets / rTheirAssets);
	if (rTheirAssetsToOurs >= fixp(0.005))
	{
		log("Their lost assets: %d; their present assets: %d;"
				" our present assets: %d; asset ratio: %d percent",
				rTheirLostAssets.uround(), rTheirAssets.uround(),
				rOurAssets.uround(), rTheirAssetsToOurs.getPercent());
	}
	/*	This is mostly about their losses, and not ours, but we shouldn't be
		satisfied to have weakened their army if ours fares far worse.
		Slightly weird side-effect: Peace scenario can have higher
		utility for Loathing even if we only fight against other civs. */
	scaled rTheirMinusOurLostPower = scaled::max(0,
			// Never mind losses in HOME_GUARD; LOGISTICS is included in FLEET.
			militAnalyst().lostPower(eThey, ARMY) + militAnalyst().lostPower(eThey, FLEET)
			- fixp(0.5) *
			(militAnalyst().lostPower(eWe, ARMY) + militAnalyst().lostPower(eWe, FLEET)));
	vector<MilitaryBranch*> const& kOurMilitary = ourCache().
			getPowerValues();
	vector<MilitaryBranch*> const& kTheirMilitary = kThey.uwai().getCache().
			getPowerValues();
	/*	Future power is a better point of reference; AI build-up during war
		preparations and reinforcements throughout a war tend to dwarf
		present military power. */
	scaled const rOurPower = kOurMilitary[ARMY]->power() + kOurMilitary[FLEET]->power() +
			militAnalyst().gainedPower(eWe, ARMY) + militAnalyst().gainedPower(eWe, FLEET);
	scaled const rTheirPower = kTheirMilitary[ARMY]->power() + kTheirMilitary[FLEET]->power() +
			militAnalyst().gainedPower(eThey, ARMY) + militAnalyst().gainedPower(eThey, FLEET);
	scaled const rTheirLostPowRatio = std::min(
			rTheirMinusOurLostPower / (rOurPower + scaled::epsilon()),
			3 * rTheirMinusOurLostPower / (rTheirPower + scaled::epsilon()));
	if (rTheirLostPowRatio.abs() > fixp(0.005))
	{
		log("Difference in lost power (adjusted): %d; their projected power: %d;"
				" our projected power: %d; lost pow percentage: %d",
				rTheirMinusOurLostPower.round(), rTheirPower.round(),
				rOurPower.round(), rTheirLostPowRatio.getPercent());
	}
	/*	rTheirLostPowRatio is less important, and also tends to be high b/c peace-time
		armies (rOurPower, rTheirPower) are often small compared to war-time armies. */
	return (2 * rTheirAssetsToOurs +
			fixp(0.5) * std::min(fixp(1.8), rTheirLostPowRatio)) / 3;
	/*	rTheirLostPowRatio is important when we can't conquer any of their cities,
		i.e. in all cases when we loath a stronger opponent.
		Hence all the checks and balances. */
}


void MilitaryVictory::evaluate()
{
	PROFILE_FUNC();
	// Vassals shouldn't strive for victory; not until breaking free.
	if (kOurTeam.isAVassal())
		return;
	scaled rTotalProgressRating;
	scaled rMaxProgress = -1;
	std::vector<scaled> arProgressRatings;
	/*	The distinction between stage 3 and 4 is too coarse to be useful;
		treat them the same way. At stage 2, the AI should focus on
		building up military power; too early for conquering land for the
		sake of the victory thresholds. */
	if (kWe.AI_atVictoryStage(AI_VICTORY_CONQUEST3))
		arProgressRatings.push_back(progressRatingConquest());
	if (kWe.AI_atVictoryStage(AI_VICTORY_DOMINATION3))
		arProgressRatings.push_back(progressRatingDomination());
	// Diplomatic victories can come through military means
	if (kWe.AI_atVictoryStage(AI_VICTORY_DIPLOMACY3))
		arProgressRatings.push_back(progressRatingDiplomacy());
	if (arProgressRatings.empty())
		return;
	for (size_t i = 0; i < arProgressRatings.size(); i++)
	{
		scaled rProgress = arProgressRatings[i];
		rProgress.clamp(0, 1);
		if (rProgress > rMaxProgress)
			rMaxProgress = rProgress;
		rTotalProgressRating += rProgress;
	}
	FAssert(rMaxProgress >= 0);
	int const iFreeRivals = countFreeRivals<false>();
	if (rTotalProgressRating > 0)
	{
		log("Rivals remaining: %d", iFreeRivals);
		log("Pursued mil. victory conditions: %d", (int)arProgressRatings.size());
	}
	if (iFreeRivals <= 0)
		return;
	/*	Division by (sqrt of) iVictories because it's not so useful to pursue
		several victory conditions at once. But don't go below the max of the
		progress values. */
	scaled rProgressRating = std::max(rMaxProgress, rTotalProgressRating /
			scaled(arProgressRatings.size()).sqrt());
	// The fewer rivals remain, the more we're willing to go all-in for victory
	scaled rDivisor = 2 + scaled(iFreeRivals).sqrt();
	scaled rUtility = 540 * rProgressRating / rDivisor;
	/*	May lose votes if nuked. This could be better integrated with the progress
		ratings above. First had it as a separate class, now kind of tacked on. */
	scaled rVoteCost;
	scaled rHitUs = militAnalyst().getNukedCities(eThey, eWe);
	if (rHitUs > 0 &&
		(kWe.AI_atVictoryStage(AI_VICTORY_DIPLOMACY3 |
		/*	The other peaceful victories are similar enough to Diplo;
			don't want our population to be nuked. */
		AI_VICTORY_CULTURE3 | AI_VICTORY_SPACE3) &&
		// Don't fret if we can also win differently
		(!kWe.AI_atVictoryStage(AI_VICTORY_DOMINATION3) &&
		!kWe.AI_atVictoryStage(AI_VICTORY_DOMINATION4) &&
		!kWe.AI_atVictoryStage(AI_VICTORY_CONQUEST3) &&
		!kWe.AI_atVictoryStage(AI_VICTORY_CONQUEST4) &&
		// Probably too late for nukes to stop us then
		!kWe.AI_atVictoryStage(AI_VICTORY_SPACE4) &&
		!kWe.AI_atVictoryStage(AI_VICTORY_CULTURE4))))
	{
		// Slow to grow back if we can't clean up
		scaled rPopLossRate = rHitUs *
				(ourCache().canScrubFallout() ? fixp(0.35) : fixp(0.45)) /
				std::max(1,
				kWe.getNumCities() - (int)militAnalyst().lostCities(eWe).size());
		rPopLossRate.decreaseTo(fixp(0.5));
		rVoteCost += rPopLossRate * 60;
		if (kWe.AI_atVictoryStage(AI_VICTORY_DIPLOMACY4))
			rVoteCost += rPopLossRate * 40;
		if (rVoteCost >= fixp(0.5))
		{
			FErrorMsg("Just sth. to take a look at b/c it seems to come up"
					" very rarely if ever - peaceful victory discouraging nuclear war");
			log("Nuclear war jeopardizes peaceful victory: %d "
					"(%d percent population loss expected)",
					rVoteCost.round(), rPopLossRate.getPercent());
		}
	}
	rUtility -= rVoteCost;
	m_iU += rUtility.round();
}


int MilitaryVictory::preEvaluate()
{
	m_iVotesToGo = kOurTeam.AI_votesToGoForVictory();
	// Rather try to get the last few votes through growth
	m_bEnoughVotes = (m_iVotesToGo < 8);
	return 0;
}


scaled MilitaryVictory::progressRatingConquest() const
{
	if (militAnalyst().isEliminated(eThey) ||
		militAnalyst().getCapitulationsAccepted(eOurTeam).count(eTheirTeam))
	{
		log("They're conquered entirely");
		return 1;
	}
	// If we don't take them out entirely - how much do they lose
	scaled rTheirScore;
	scaled rTheirLostAssets = netLostRivalAssetScore(eWe, &rTheirScore);
	if (rTheirScore < 25)
		return 0;
	/*	Utility of vassals is normally computed separately (linked wars),
		but in this case, our vassals may do something that helps the master
		specifically (namely bring down our last remaining rivals). */
	for (PlayerIter<ALIVE,VASSAL_OF> it(eOurTeam); it.hasNext(); ++it)
		rTheirLostAssets += netLostRivalAssetScore(it->getID());
	if (rTheirLostAssets < 5)
		return 0;
	scaled r = rTheirLostAssets / rTheirScore;
	r.decreaseTo(1);
	log("Their loss ratio: %d percent", r.getPercent());
	/*	Reduced because we can't be sure that we'll eventually finish them off.
		In particular, they could become someone else's vassal. */
	return fixp(2/3.) * r;
}

namespace
{
	VictoryTypes getDominationVictory()
	{
		static VictoryTypes eDomination = NO_VICTORY; // cache it
		if (eDomination == NO_VICTORY)
		{
			// (Same thing is done in CvPlayerAI::AI_calculateDominationVictoryStage.)
			FOR_EACH_ENUM(Victory)
			{
				if (GC.getInfo(eLoopVictory).getLandPercent() > 0)
				{
					eDomination = eLoopVictory;
					break;
				}
			}
		}
		return eDomination;
	}

	// Caller needs to guarantee that Domination victory exists (and is enabled etc.)
	scaled getDominationTargetPopPortion()
	{	// Not something we can cache in a static variable
		return per100(GC.getGame().getAdjustedPopulationPercent(getDominationVictory()));
	}
}

scaled MilitaryVictory::progressRatingDomination() const
{
	VictoryTypes const eDomination = getDominationVictory();
	if (eDomination == NO_VICTORY || militAnalyst().conqueredCities(eWe).empty())
		return 0;
	int const iPopTarget = (getDominationTargetPopPortion() *
			m_kGame.getTotalPopulation()).ceil();
	int const iPopToGo = iPopTarget - kOurTeam.getTotalPopulation();
	scaled const rOurLandPortion(kOurTeam.getTotalLand(), GC.getMap().getLandPlots());
	scaled const rAdjustedLandForDomination = per100(
			m_kGame.getAdjustedLandPercent(eDomination));
	// How close we are to the victory threshold
	scaled rLandVictoryStatus = rOurLandPortion / rAdjustedLandForDomination;
	// Dealing with land tiles is too complicated. Need a target number of cities.
	/*	If rLandVictoryStatus is what our current cities give us, we'll need this
		many for victory: */
	scaled rTargetCities = kOurTeam.getNumCities() /
			(rLandVictoryStatus + scaled::epsilon());
	/*	But the additional cities may well give us less land than our current cities.
		How many cities would we need if the goal was to have a certain fraction
		of cities rather than land tiles? Use the average of these two predictions. */
	rTargetCities += rAdjustedLandForDomination * m_kGame.getNumCities();
	rTargetCities /= 2;
	scaled rCitiesToGo = rTargetCities - kOurTeam.getNumCities();
	scaled rPopGained;
	scaled rCitiesGained;
	CitySet const& kWeConquer = militAnalyst().conqueredCities(eWe);
	CitySet const& kTheyLose = militAnalyst().lostCities(eThey);
	for (CitySetIter it = kWeConquer.begin(); it != kWeConquer.end(); ++it)
	{
		if (kTheyLose.count(*it) == 0)
			continue;
		City const& kCacheCity = *ourCache().lookupCity(*it);
		/*	Minus 0.5 for pop lost upon conquest (not -1 b/c target decreases
			as well) */
		rPopGained += kCacheCity.city().getPopulation() - fixp(0.5);
		rCitiesGained++;
	}
	if (militAnalyst().getCapitulationsAccepted(eOurTeam).count(eTheirTeam) > 0)
	{
		int iTheirPopRemaining = kThey.getTotalPopulation();
		FAssertMsg(!kTheyLose.empty(), "They capitulated w/o losing a city?");
		int const iTheirCitiesRemaining = kThey.getNumCities() - (int)kTheyLose.size();
		for (CitySetIter it = kTheyLose.begin(); it != kTheyLose.end(); ++it)
		{
			iTheirPopRemaining -= ourCache().lookupCity(*it)->city().getPopulation();
		}
		if (iTheirCitiesRemaining > 0)
		{
			log("%d vassal pop gained, and %d cities",
					iTheirPopRemaining, iTheirCitiesRemaining);
		}
		rCitiesGained += fixp(0.5) * iTheirCitiesRemaining;
		rPopGained += fixp(0.5) * iTheirPopRemaining;
	}
	if (rCitiesGained == 0)
		return 0;
	log("%d population-to-go for domination, %d cities",
			rPopGained.uround(), rCitiesToGo.round());
	FAssert(rPopGained > 0);
	log("%d pop gained, and %d cities", rPopGained.uround(), rCitiesGained.uround());
	// No use in population beyond the victory threshold
	rPopGained.decreaseTo(iPopToGo);
	/*	The to-go values can be negative (already past the threshold). In the case
		of rCitiesToGo it's not clear if we've really reached the land threshold -
		perhaps our cities own relatively few land tiles. If iPopToGo is negative,
		it's certain we've reached the pop threshold. */
	if (iPopToGo < 0)
	{
		/*	If rCitiesToGo is non-positive, then boths victory thresholds
			should be met -- but somehow we haven't won.
			Assume that we need a few more cities. */
		int const iMinCitiesToGo = 4;
		if (rCitiesToGo < iMinCitiesToGo)
		{
			log("Cities-to-go set to lower bound: %d", iMinCitiesToGo);
			rCitiesToGo = iMinCitiesToGo;
		}
		rCitiesGained.decreaseTo(rCitiesToGo);
		return rCitiesGained / rCitiesToGo;
	}
	else
	{
		if (rCitiesToGo < 0)
		{
			// Assume that we have enough land.
			return rPopGained / iPopToGo;
		}
		log("Progress towards domination based on both gained cities and population");
		return fixp(0.5) * (rCitiesGained / rCitiesToGo + rPopGained / iPopToGo);
	}
}


scaled MilitaryVictory::progressRatingDiplomacy() const
{
	if (m_bEnoughVotes)
	{
		log("Votes for diplo victory already secured");
		return 0;
	}
	VoteSourceTypes const eVS = kOurTeam.AI_getLatestVictoryVoteSource();
	if (eVS == NO_VOTESOURCE)
	{	// DIPLO3 should normally rule that out (at the call site)
		log("No vote source yet");
		return 0;
	}
	ReligionTypes const eVSReligion = m_kGame.getVoteSourceReligion(eVS);
	bool const bSecular = (eVSReligion == NO_RELIGION);
	scaled rPopGained;
	std::map<PlotNumTypes,scaled> weightedConq;
	CitySet conqFriendly;
	CitySet conqPleased;
	CitySet const& kTheyLose = militAnalyst().lostCities(eThey);
	int const iReligionObstacles = kOurTeam.AI_countVSNonMembers(eVS);
	int iReligionObstaclesRemoved = 0;
	/*	Vassal conquests just as good as our own for getting votes.
		Conquests by friends and partners can only help a little (reduced weight). */
	for (CitySetIter it = kTheyLose.begin(); it != kTheyLose.end(); ++it)
	{
		if (militAnalyst().conqueredCities(eWe).count(*it))
			weightedConq.insert(make_pair(*it, 1));
	}
	for (PlayerIter<ALIVE,VASSAL_OF> itVassal(eOurTeam);
		itVassal.hasNext(); ++itVassal)
	{
		PlayerTypes const eVassalMember = itVassal->getID();
		if (!GET_PLAYER(eVassalMember).isVotingMember(eVS))
			continue;
		// Halve weight for vassals that are mere voting members
		scaled rWeight = fixp(0.5);
		if (bSecular || GET_PLAYER(eVassalMember).isFullMember(eVS))
			rWeight = 1;
		for (CitySetIter it = kTheyLose.begin(); it != kTheyLose.end(); ++it)
		{
			if (militAnalyst().conqueredCities(eVassalMember).count(*it) > 0)
				weightedConq.insert(make_pair(*it, rWeight));
		}
	}
	// Need to deal with them somehow for AP victory
	if (!bSecular && !kThey.isVotingMember(eVS))
	{
		if (militAnalyst().isEliminated(eThey))
			iReligionObstaclesRemoved++;
	}
	scaled rObstacleProgress;
	if (iReligionObstacles > 0)
	{
		rObstacleProgress = scaled(iReligionObstaclesRemoved, iReligionObstacles);
		if (rObstacleProgress > 0)
		{
			log("Progress on AP obstacles: %d percent",
					rObstacleProgress.getPercent());
		}
	}
	if (bSecular || kThey.isVotingMember(eVS))
	{
		scaled rMembershipMult = 1;
		if (!kThey.isFullMember(eVS))
			rMembershipMult = fixp(0.5);
		// Conquests by friends from non-friends: 2/3 weight
		addConquestsByPartner(weightedConq, ATTITUDE_FRIENDLY,
				fixp(2/3.) * rMembershipMult);
		// Pleased: 1/3
		addConquestsByPartner(weightedConq, ATTITUDE_PLEASED,
				fixp(1/3.) * rMembershipMult);
	}
	for (std::map<PlotNumTypes,scaled>::const_iterator it = weightedConq.begin();
		it != weightedConq.end(); ++it)
	{
		City const& kCacheCity = *ourCache().lookupCity(it->first);
		/*	Apply weight for new owner. -0.5 for population loss upon conquest
			(not -1 b/c total decreases as well). */
		scaled rPop = it->second * (kCacheCity.city().getPopulation() - fixp(0.5));
		PlayerTypes const eCityOwner = kCacheCity.city().getOwner();
		// Weight for old owner
		if (!GET_TEAM(eCityOwner).isHuman())
		{
			/*	AP: Conquests from non-full members are always worthwhile
				b/c, as full members, we can make their votes count twice. */
			if (bSecular || kThey.isFullMember(eVS))
			{
				AttitudeTypes const eOwnerTowardUs = GET_PLAYER(eCityOwner).
						AI_getAttitude(eWe);
				if (eOwnerTowardUs >= ATTITUDE_FRIENDLY)
					rPop /= 3;
				if (eOwnerTowardUs == ATTITUDE_PLEASED)
					rPop *= fixp(2/3.);
			}
		}
		if (!bSecular && !kCacheCity.city().isHasReligion(eVSReligion))
			rPop *= fixp(0.5); // Not 0 b/c religion can still be spread
		log("Votes expected from %s: %d", m_kReport.cityName(kCacheCity.city()),
				rPop.uround());
		rPopGained += rPop;
	}
	if (militAnalyst().getCapitulationsAccepted(eOurTeam).count(eTheirTeam) > 0)
	{
		scaled rNewVassalVotes;
		// Faster than a full pass through ourCache()
		FOR_EACH_CITY(pCity, kThey)
		{
			City const* pCacheCity = ourCache().lookupCity(pCity->plotNum());
			if (pCacheCity == NULL ||
				militAnalyst().lostCities(eThey).count(pCacheCity->getID()) > 0)
			{
				continue;
			}
			scaled rPop = pCity->getPopulation();
			if (!bSecular && !pCity->isHasReligion(eVSReligion))
				rPop *= fixp(0.5);
			rNewVassalVotes += rPop;
		}
		if (bSecular || kThey.isFullMember(eVS))
		{
			// Not much point if they already love us
			if (towardUs() >= ATTITUDE_FRIENDLY)
				rNewVassalVotes /= 3;
			else if (towardUs() == ATTITUDE_PLEASED)
				rNewVassalVotes *= fixp(2/3.);
		}
		log("Votes expected from capitulated cities of %s: %d",
				m_kReport.leaderName(eThey), rNewVassalVotes.uround());
		rPopGained += rNewVassalVotes;
	}
	if (rPopGained >= fixp(0.5))
	{
		log("Total expected votes: %d, current votes-to-go: %d",
				rPopGained.uround(), m_iVotesToGo);
	}
	FAssert(m_iVotesToGo > 0);
	rPopGained.decreaseTo(m_iVotesToGo);
	scaled rProgress = rPopGained / m_iVotesToGo;
	if (iReligionObstacles <= 0)
		return rProgress;
	// If there are AP obstacles, give the progress rate on those 25% weight.
	return fixp(0.25) * rObstacleProgress + fixp(0.75) * rProgress;
}


void MilitaryVictory::addConquestsByPartner(
	std::map<PlotNumTypes,scaled>& kWeightedConquests,
	AttitudeTypes eAttitudeThresh, scaled rWeight) const
{
	if (kTheirTeam.isHuman()) // Human won't vote for us unless a vassal
	{
		if (!kTheirTeam.isVassal(eOurTeam))
			return;
	}
	else if (towardUs() < eAttitudeThresh)
		return;
	CitySet const& kTheyConquer = militAnalyst().conqueredCities(eThey);
	for (CitySetIter it = kTheyConquer.begin(); it != kTheyConquer.end(); ++it)
	{
		City const& kCacheCity = *ourCache().lookupCity(*it);
		PlayerTypes const eCityOwner = kCacheCity.city().getOwner();
		// Never good news when we lose cities
		if (GET_PLAYER(eCityOwner).getMasterTeam() == kOurTeam.getMasterTeam())
			continue;
		/*	Don't bother checking AP membership here (although it would be smart
			to count conquests by friends that are full members at the expense of
			friends that aren't) */
		if (GET_PLAYER(eCityOwner).AI_getAttitude(eWe) < eAttitudeThresh ||
			GET_TEAM(eCityOwner).isHuman())
		{
			kWeightedConquests.insert(make_pair(*it, rWeight));
		}
	}
}

namespace
{
	int const iPartnerUtilFromOB = 8;
}

void Assistance::evaluate()
{
	PROFILE_FUNC();
	/*	Could use CvPlayerAI::AI_stopTradingTradeVal, but that also accounts for
		angering the civ we stop trading with, and it's a bit too crude.
		I use a bit of code from there in partnerUtilFromTrade. */
	if (// Don't want to end up helping a potentially dangerous master
		kTheirTeam.isAVassal() ||
		/*	These checks can make us inclined to attack a friend if it's already
			under attack; b/c the peace scenario will have reduced utility from
			Assistance and the war scenario won't. I guess that's OK.
			"At least, if we attack them too, we don't have to worry about
			their losses (because they won't trade with us anymore anyway)."
			Costs from Affection and Ill Will should still lead to a sensible
			decision overall. */
		kOurTeam.AI_getWarPlan(eTheirTeam) != NO_WARPLAN ||
		militAnalyst().getWarsDeclaredBy(eWe).count(eThey) > 0 ||
		militAnalyst().getWarsDeclaredOn(eWe).count(eThey) > 0)
	{
		return;
	}
	/*	Utility of teammates is added up in the end; don't count extra utility
		here for assisting teammates. Since Assistance isn't a BroaderAspect,
		it should only get called for rivals in the first place. */
	FAssert(eTheirTeam != eOurTeam);
	// Shared-war bonus handled under SuckingUp
	if ((kWe.isHuman() && (kThey.isHuman() || towardUs() < ATTITUDE_CAUTIOUS)) ||
		(!kWe.isHuman() && towardThem() < ATTITUDE_PLEASED))
	{
		return;
	}
	scaled rAssistRatio = assistanceRatio();
	if (rAssistRatio > 0)
	{
		log("Expecting them to lose %d percent of their assets",
				rAssistRatio.getPercent());
	}
	else return;
	scaled rTradeUtility = rAssistRatio * partnerUtilFromTrade();
	// Tech trade and military support are more sensitive to losses than trade
	scaled rOtherUtility = rAssistRatio.sqrt() *
			(partnerUtilFromTech() + partnerUtilFromMilitary());
	if (rTradeUtility > 0 || rOtherUtility > 0)
	{
		log("Utility for trade: %d, tech/military: %d, both weighted by saved assets",
				rTradeUtility.uround(), rOtherUtility.uround());
	}
	scaled rUtility = rTradeUtility + rOtherUtility;
	if (!kWe.isHuman() && towardThem() >= ATTITUDE_FRIENDLY)
	{
		scaled rPureAffectionUtility = rAssistRatio * 20;
		log("Utility raised to %d for pure affection", rPureAffectionUtility.round());
		rUtility.increaseTo(rPureAffectionUtility);
	}
	scaled rOBUtil;
	if (kOurTeam.isOpenBorders(eTheirTeam))
		rOBUtil = iPartnerUtilFromOB * rAssistRatio;
	if (rUtility < rOBUtil && rOBUtil > 0)
	{
		rUtility = rOBUtil;
		log("Utility raised to %d for strategic value of OB", rUtility.round());
	}
	scaled rPersonalityMult = kWeAI.protectiveInstinct();
	log("Personality multiplier: %d percent", rPersonalityMult.getPercent());
	/*	Assistance really counts the negative utility from losses
		that our partner suffers */
	m_iU -= (rUtility * rPersonalityMult).round();
}


scaled Assistance::assistanceRatio() const
{
	/*	Asset scores aren't entirely reliable, therefore, treat elimination
		separately. */
	if (militAnalyst().isEliminated(eThey))
		return 1;
	scaled rTheirAssets;
	scaled rTheirLostAssets = netLostRivalAssetScore(NO_PLAYER, &rTheirAssets);
	if (rTheirAssets <= 0)
		return 0;
	scaled r(rTheirLostAssets / rTheirAssets);
	// Don't want to help them conquer cities - only look at what they lose.
	r.increaseTo(0);
	FAssert(r <= 1);
	if (militAnalyst().hasCapitulated(eTheirTeam))
	{
		// Count capitulation as a 50% devaluation of their remaining assets
		r += fixp(0.5) * (1 - r);
		log("%s capitulates", m_kReport.leaderName(eThey));
	}
	return r;
}


void Reconquista::evaluate()
{
	CitySet const& kWeConquer = militAnalyst().conqueredCities(eWe);
	if (kWeConquer.empty())
		return;
	int const iProjectedCities = kWe.getNumCities() +
			(int)(kWeConquer.size() - militAnalyst().lostCities(eWe).size());
	scaled const rBaseReconqVal = scaled::max(5, scaled(90, iProjectedCities + 2));
	scaled rUtility;
	for (CitySetIter it = kWeConquer.begin(); it != kWeConquer.end(); ++it)
	{
		if (militAnalyst().lostCities(eThey).count(*it) <= 0)
			continue;
		CvCity const& kCity = ourCache().lookupCity(*it)->city();
		if (!kCity.isEverOwned(eWe))
			continue;
		/*	Lower the utility if our culture is small; suggests that we only
			held the city briefly or long ago. */
		scaled rReconqMult = (scaled::min(1,
				scaled(kCity.getPlot().calculateCulturePercent(eWe), 50)
				)).sqrt();
		rUtility += rBaseReconqVal * rReconqMult;
		log("Reconquering %s; base val %d, modifier %d percent",
				m_kReport.cityName(kCity),
				rBaseReconqVal.uround(), rReconqMult.getPercent());
	}
	m_iU += rUtility.round();
}


void Rebuke::evaluate()
{
	/*	<advc.134a> More reluctant to make peace when they (human)
		have recently turned down a peace offer */
	if (kWe.AI_getContactTimer(eThey, CONTACT_PEACE_TREATY) > 0)
	{
		/*	Don't want to use the remaining time here b/c that gets doubled when
			capitulation is offered */
		int iRejectedPeaceCost = intdiv::uround(
				kOurPersonality.getContactDelay(CONTACT_PEACE_TREATY), 5);
		log("+%d for rejected peace offer", iRejectedPeaceCost);
		m_iU += iRejectedPeaceCost;
	} // </advc.134a>
	// Don't expect humans to follow through on rejected demands
	int const iRebukeDiplo = (kWe.isHuman() ? 0 :
			-1 * kWe.AI_getMemoryAttitude(eThey, MEMORY_REJECTED_DEMAND));
	if (iRebukeDiplo <= 0)
		return;
	if (militAnalyst().getCapitulationsAccepted(eOurTeam).count(eTheirTeam) > 0)
	{
		log("%s capitulates to us after rebuke", m_kReport.leaderName(eThey));
		/*	OK to count this multiple times for members of the same team; typically,
			only some member pairs are going to have a rebuke memory. */
		m_iU += 30;
		return;
	}
	scaled rTheirAssets;
	scaled rTheirLostAssets = netLostRivalAssetScore(eWe, &rTheirAssets);
	if (rTheirAssets <= 0)
		return;
	/*	Give their loss and our gain equal weight. We want to demonstrate that we
		can take by force what is denied to us (and more), and that those who
		deny us end up paying more than was asked. */
	scaled rPunishmentRatio = fixp(0.5) *
			(rTheirLostAssets / rTheirAssets +
			conqAssetScore() / scaled::max(10, ourCache().totalAssetScore()));
	if (rPunishmentRatio <= 0)
		return;
	log("Punishment ratio: %d percent, rebuke diplo: %d",
			rPunishmentRatio.getPercent(), iRebukeDiplo);
	m_iU += std::min(30,
			(scaled(iRebukeDiplo).sqrt() * 100 * rPunishmentRatio).round());
}


void Fidelity::evaluate()
{
	PROFILE_FUNC();
	/*	Don't care about our success here at all. If we declared war, we've proved
		that we don't tolerate attacks on our (declared) friends. */
	if (militAnalyst().getWarsDeclaredBy(eWe).count(eThey) <= 0)
		return;
	// Human doesn't really have friends, needs special treatment.
	if (!kWe.isHuman() && kWe.AI_getMemoryCount(eThey, MEMORY_DECLARED_WAR_ON_FRIEND) <= 0)
		return;
	/*	Check if we still like the "friend" and if they're still at war.
		Unless attacked recently, we can't tell who started it, but that's
		just as well; let's not fuss over water under the bridge. */
	bool bWarOngoing = false;
	for (PlayerIter<FREE_MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> itPartner(eOurTeam);
		itPartner.hasNext(); ++itPartner)
	{
		PlayerTypes const ePartner = itPartner->getID();
		if (GET_TEAM(ePartner).isAtWar(eOurTeam) ||
			GET_TEAM(ePartner).AI_getWarPlan(eTheirTeam) != WARPLAN_ATTACKED_RECENT ||
			!kWe.canContact(ePartner, true))
		{
			continue;
		}
		AttitudeTypes eOurAttitude = (kWe.isHuman() ?
				// Assume that humans likes civs that like them back
				GET_PLAYER(ePartner).AI_getAttitude(eWe) :
				kWe.AI_getAttitude(ePartner));
		/*	Pleased vs. Friendly are distinguished under "Assistance".
			I want to be consistent with the relations penalty here,
			which is the same for Pleased and Friendly. */
		if (eOurAttitude >= ATTITUDE_PLEASED)
		{
			bWarOngoing = true;
			log("%s recently attacked our friend %s", m_kReport.leaderName(eThey),
					m_kReport.leaderName(ePartner));
			break;
		}
	}
	if (!bWarOngoing)
		return;
	scaled rLeaderFactor = 1;
	if (!kWe.isHuman())
	{
		/*	Only Gandhi applies a penalty of 200% for war on friend.
			Not sure if I want him to act as a peacekeeper ... Let's try it. */
		rLeaderFactor = per100(kOurPersonality.
				getMemoryAttitudePercent(MEMORY_DECLARED_WAR_ON_FRIEND));
		if (!rLeaderFactor.isNegative())
			return;
		rLeaderFactor = (-rLeaderFactor).sqrt();
	}
	m_iU += (rLeaderFactor * 10).round();
}


void HiredHand::evaluate()
{
	if (!m_kParams.isConsideringPeace() || !kOurTeam.isAtWar(eTheirTeam) ||
		// Perhaps redundant(?)
		militAnalyst().getWarsContinued(eWe).count(eThey) <= 0 ||
		kTheirTeam.isAVassal() || // AI can only be hired vs. master
		/*	Humans can't be hired for war and if they hire someone,
			it doesn't mean the human keeps fighting. */
		kWe.isHuman() ||
		/*	If we start another war, we'll probably focus on the new
			war enemy, and withdraw our attention from the sponsored war.
			This isn't what a faithful ally does. */
		militAnalyst().getWarsDeclaredBy(eWe).size() > 0)
	{
		return;
	}
	PlayerTypes const eSponsor = ourCache().sponsorAgainst(eTheirTeam);
	int const iOriginalUtility = ourCache().bountyAgainst(eTheirTeam);
	FAssert((eSponsor == NO_PLAYER) == (iOriginalUtility <= 0));
	scaled rUtility;
	if (eSponsor != NO_PLAYER && iOriginalUtility > 0 &&
		GET_PLAYER(eSponsor).isAlive() &&
		kOurTeam.AI_getAttitude(TEAMID(eSponsor)) >= kOurPersonality.
		/*	Between Annoyed and Pleased; has to be strictly better to allow
			sponsorship. If it becomes strictly worse, we bail. */
		getDeclareWarRefuseAttitudeThreshold())
	{
		log("We've been hired by %s; original utility of payment: %d",
				m_kReport.leaderName(eSponsor), iOriginalUtility);
		// Inclined to fight for 20 turns
		rUtility += eval(eSponsor, iOriginalUtility, 20);
		int iDeniedHelpDiplo = 0;
		for (MemberIter itSponsorMember(TEAMID(eSponsor));
			itSponsorMember.hasNext(); ++itSponsorMember)
		{
			iDeniedHelpDiplo -= kWe.AI_getMemoryAttitude(
					itSponsorMember->getID(), MEMORY_DENIED_JOIN_WAR);
		}
		if (iDeniedHelpDiplo > 0) // (The above normally subtracts a negative value)
		{
			log("Utility reduced b/c of denied help");
			rUtility /= scaled(iDeniedHelpDiplo).sqrt();
		}
	}
	// Have we hired someone to help us against eThey?
	for (PlayerAIIter<FREE_MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> itAlly(eOurTeam);
		itAlly.hasNext(); ++itAlly)
	{
		CvPlayerAI const& kAlly = *itAlly;
		/*	No point in checking if the ally is coming through. Need to allow
			some time for that, and we don't feel obliged for that long anyway.
			Or might say: We keep up the war just long enough to find out if
			our ally can make a difference. That's actually almost rational. */
		if (kAlly.uwai().getCache().sponsorAgainst(eTheirTeam) == eWe ||
			(kWe.AI_getMemoryCount(kAlly.getID(), MEMORY_ACCEPTED_JOIN_WAR) > 0 &&
			/*	Still can't be sure that the current war between the (human) ally
				and eThey is the war we've asked the ally to declare, but that's OK. */
			kThey.AI_getMemoryCount(eWe, MEMORY_HIRED_WAR_ALLY) > 0))
		{
			log("We've hired %s for war against %s",
					m_kReport.leaderName(kAlly.getID()),
					m_kReport.leaderName(eThey));
			if (kWe.AI_getAttitude(kAlly.getID()) <= ATTITUDE_ANNOYED)
			{
				log("... but we don't like our hireling enough to care");
				continue;
			}
			/*	Behave as if someone had paid us the equivalent of 25 utility;
				feel obliged to fight along the ally for 10 turns.
				(Or should it matter how much we've paid the ally?) */
			rUtility += eval(kAlly.getID(), 25, 10);
		}
	}
	/*	Have we been at war since the start of the game? Then it's a scenario
		and we should try to play along for a while. Tbd.: Should be a
		separate aspect "Historical Role". */
	if (kOurTeam.AI_getAtWarCounter(eTheirTeam) >= m_kGame.getElapsedGameTurns())
		rUtility += eval(NO_PLAYER, 50, 12);
	m_iU += rUtility.round();
}


scaled HiredHand::eval(PlayerTypes eAlly, int iOriginalUtility,
	int iObligationThresh) const
{
	// (These conditions overlap with those under Fidelity)
	if (eAlly != NO_PLAYER && (kOurTeam.isAtWar(TEAMID(eAlly)) ||
		// Important to check isAtWar first; infinite recursion possible otherwise.
		!kWe.canContact(eAlly, true) ||
		kOurTeam.AI_getWorstEnemy() == TEAMID(eAlly) ||
		GET_TEAM(eAlly).isAVassal()))
	{ // Don't feel obliged to vassals
		log("We don't feel obliged to fight for %s", m_kReport.leaderName(eAlly));
		return 0;
	}
	int const iOurAtWarCounter = (kOurTeam.isAtWar(eTheirTeam) ?
			kOurTeam.AI_getAtWarCounter(eTheirTeam) : MAX_INT);
	int const iAllyAtWarCounter =
			(eAlly == NO_PLAYER || !GET_TEAM(eAlly).isAtWar(eTheirTeam) ?
			MAX_INT : GET_TEAM(eAlly).AI_getAtWarCounter(eTheirTeam));
	// Whoever has been hired must have the smaller AtWarCounter
	int iTurnsFought = std::min(iOurAtWarCounter, iAllyAtWarCounter);
	log("Hired team has fought %d turns against %s", iTurnsFought,
			m_kReport.leaderName(eThey));
	if (iTurnsFought >= iObligationThresh)
	{
		log("Fought long enough");
		return 0;
	}
	scaled rObligationRatio(iObligationThresh - iTurnsFought, iObligationThresh);
	/*	Count the value of the sponsorship double initially to make relatively sure
		that we don't make peace right away due to some change in circumstance. */
	scaled rUtility = 2 * SQR(rObligationRatio) * iOriginalUtility;
	if (rUtility >= fixp(0.5))
	{
		log("Utility for sticking with %s: %d", eAlly == NO_PLAYER ?
				"our historical role" : m_kReport.leaderName(eAlly),
				rUtility.round());
	}
	return rUtility;
}


void BorderDisputes::evaluate()
{
	PROFILE_FUNC();
	int iDiploPenalty = -1 * kWe.AI_getCloseBordersAttitude(eThey);
	if (iDiploPenalty <= 0)
		return;
	{
		/*	Assume iCloseBordersAttitudeChange of -4 for human instead of the
			value from XML (which is between -2 and -4). Humans don't like
			having their cities culture-pressured. */
		int iCloseBordersAttitudeChange = kOurPersonality.
				getCloseBordersAttitudeChange();
		if (kWe.isHuman() && iCloseBordersAttitudeChange != 0)
		{
			FAssert(iCloseBordersAttitudeChange < 0);
			iDiploPenalty = intdiv::round(-4 * iDiploPenalty,
					iCloseBordersAttitudeChange);
			if (iDiploPenalty <= 0) // ==0 could happen through XML changes
			{
				FAssert(iDiploPenalty == 0);
				return;
			}
		}
	}
	if (militAnalyst().getCapitulationsAccepted(eOurTeam).count(eTheirTeam) > 0)
	{
		log("They capitulate; shared-borders diplo%s: %d",
				kWe.isHuman() ? " (human)" : "", iDiploPenalty);
		m_iU += iDiploPenalty * 8;
		return;
	}
	scaled rUtility;
	CitySet const& kTheyLose = militAnalyst().lostCities(eThey);
	for (CitySetIter itCity = kTheyLose.begin(); itCity != kTheyLose.end(); ++itCity)
	{
		CvCity const& kCity = ourCache().lookupCity(*itCity)->city();
		int const iOurPlotCulturePercent = kCity.getPlot().calculateCulturePercent(eWe);
		scaled rNewOwnerMultiplier = 0;
		for (PlayerIter<MAJOR_CIV> itConqueror; itConqueror.hasNext(); ++itConqueror)
		{
			PlayerTypes const eConquerer = itConqueror->getID();
			if (militAnalyst().conqueredCities(eConquerer).count(*itCity) <= 0)
				continue;
			// Conquests by our vassals (or by us) help us fully
			if (GET_PLAYER(eConquerer).getMasterTeam() == eOurTeam)
				rNewOwnerMultiplier = 1;
			// Third party: depends on how much culture they have
			else
			{
				// (Might be better to check city culture here?)
				rNewOwnerMultiplier = per100(
						75 - kCity.getPlot().calculateCulturePercent(eConquerer));
				rNewOwnerMultiplier.increaseTo(0);
			}
			log("%s possible border city; our culture: %d percent",
					m_kReport.cityName(kCity), iOurPlotCulturePercent);
			/*	If we have very little culture there and we don't conquer it,
				assume that the city is far away from our border. */
			if (eConquerer != eWe && iOurPlotCulturePercent < 1)
			{
				rNewOwnerMultiplier = 0;
				log("Skipped b/c conquered by third party and "
						"our culture very small");
			}
			else if (kCity.getPlot().getCulture(eWe) <= 0)
			{
				rNewOwnerMultiplier = 0;
				log("Skipped b/c we have 0 culture there");
			}
			break;
		}
		if (rNewOwnerMultiplier <= 0)
			continue;
		// advc.003g: Tbd.: Write a fixed-point logarithm function
		double dOurCultureMultiplier = iOurPlotCulturePercent / 100.0;
		/*	E.g. dOurCultureModifier=1 if 0% culture;
			5% -> 0.92; 10% -> 0.67; 20% -> 0.42; 50% -> 0.08.
			If we already have a lot of culture in the city, then it's probably
			not the city causing us to lose border tiles. */
		if (dOurCultureMultiplier > 0.04)
		{
			dOurCultureMultiplier = std::max(0.0,
					1 - 0.25 * std::log(25 * dOurCultureMultiplier) /
					0.301/*std::log(2.0)*/); // binary log
		}
		else dOurCultureMultiplier = 1;
		scaled rOurCultureModifier = scaled::fromDouble(dOurCultureMultiplier);
		log("Multiplier for our rel. tile culture: %d percent",
				rOurCultureModifier.getPercent());
		log("Diplo penalty from border dispute: %d", iDiploPenalty);
		rUtility += 5 * rNewOwnerMultiplier * rOurCultureModifier * iDiploPenalty;
	}
	m_iU += rUtility.round();
}


void SuckingUp::evaluate()
{
	/*	Similar to Assistance and Fidelity, but this one is only about improving
		relations through the shared-war diplo modifier, whereas Assistance is about
		preventing a civ that is already a partner from being marginalized, and
		Fidelity is about discouraging future attacks on our friends. */

	/*	Sucking up to humans doesn't work, and it's unclear if relations with our
		enemies are going to matter. */
	if (kThey.isHuman() || militAnalyst().isWar(eWe, eThey) ||
		kOurTeam.AI_getWorstEnemy() == eTheirTeam ||
		// Don't bet on a loser
		militAnalyst().isEliminated(eThey) ||
		militAnalyst().hasCapitulated(eTheirTeam) ||
		militAnalyst().lostCities(eThey).size() >
		militAnalyst().conqueredCities(eThey).size() ||
		/*	(Be more generous about score when aiming at a diplo victory?
			No; better not to declare non-essential wars then.) */
		m_kGame.getPlayerScore(eWe) * 6 > m_kGame.getPlayerScore(eThey) * 10 ||
		// Hopeless case:
		diploTowardUs() <= GC.getDefineINT(CvGlobals::RELATIONS_THRESH_FURIOUS) + 1 ||
		// No need to improve relations further:
		100 * diploTowardUs() >=
		140 * GC.getDefineINT(CvGlobals::RELATIONS_THRESH_FRIENDLY))
	{
		return;
	}
	/*	If they don't need the assist or if we don't actually fight, there'll
		be no diplo bonus. The 10*NumCities threshold is very arbitrary. */
	if (militAnalyst().lostPower(eWe, ARMY) < 10 * kWe.getNumCities() ||
		militAnalyst().lostPower(eThey, ARMY) < 10 * kThey.getNumCities())
	{
		return;
	}
	int iSharedWars = 0;
	int iOurWars = 0;
	for (TeamIter<FREE_MAJOR_CIV> itEnemy; itEnemy.hasNext(); ++itEnemy)
	{
		TeamTypes const eEnemy = itEnemy->getID();
		if (eEnemy == eOurTeam || eEnemy == eTheirTeam)
			continue;
		if (militAnalyst().isWar(eOurTeam, eEnemy))
		{
			iOurWars++;
			if (militAnalyst().isWar(eTheirTeam, eEnemy))
				iSharedWars++;
		}
	}
	// If we'll fight multiple wars, we may not be able to actually assist them.
	if (iSharedWars <= 0 || iOurWars > iSharedWars)
		return;
	// Between 2 (Ashoka) and 6 (DeGaulle)
	int const iMaxDiplo = (m_kGame.isOption(GAMEOPTION_RANDOM_PERSONALITIES) ? 4 :
			GC.getInfo(kThey.getPersonalityType()).getShareWarAttitudeChangeLimit());
	scaled rUtility = fixp(1.6) * iMaxDiplo; // Should iSharedWars have an impact?
	log("Sharing a war with %s; up to +%d diplo",
			m_kReport.leaderName(eThey), iMaxDiplo);
	int const iCivPlayersAlive = m_kGame.countCivPlayersAlive();
	if (towardUs() == ATTITUDE_PLEASED &&
		kWe.AI_atVictoryStage(AI_VICTORY_DIPLOMACY3) && iCivPlayersAlive > 2)
	{
		log("Bonus utility for them being pleased and us close to diplo victory");
		rUtility += 5;
	}
	/*	Diplo bonus with just one civ less important in large games, but also in
		very small games or when there are few civs left. */
	m_iU += (rUtility / scaled(std::max(4, iCivPlayersAlive)).sqrt()).round();
}


void PreEmptiveWar::evaluate()
{
	/*	If an unfavorable war with them seems likely in the long run,
		we rather take our chances now. */
	// Don't worry about long-term threat when getting close to victory
	if (kOurTeam.AI_anyMemberAtVictoryStage3() || militAnalyst().isEliminated(eWe) ||
		militAnalyst().hasCapitulated(kOurTeam.getID()))
	{
		return;
	}
	scaled const rCurrThreat = ourCache().threatRating(eThey);
	/*	War evaluation should always assume minor threats;
		not worth addressing here explicitly. */
	if (rCurrThreat < fixp(0.15))
		return;
	// rCurrThreat includes their vassals, so include vassals here as well.
	scaled rTheirCurrentCities;
	scaled rTheirPredictedCities;
	for (PlayerIter<MAJOR_CIV> itTheirAlly; itTheirAlly.hasNext(); ++itTheirAlly)
	{	// Them, a teammate or a vassal.
		CvPlayer const& kTheirAlly = *itTheirAlly;
		bool const bNewVassal = (militAnalyst().getCapitulationsAccepted(eTheirTeam).
				count(kTheirAlly.getTeam()) > 0);
		if (!bNewVassal &&
			kTheirAlly.getMasterTeam() != GET_PLAYER(eThey).getMasterTeam())
		{
			continue;
		}
		scaled rVassalMult = 1;
		if (bNewVassal || kTheirAlly.isAVassal())
			rVassalMult = fixp(0.5);
		if (!bNewVassal)
			rTheirCurrentCities += kTheirAlly.getNumCities() * rVassalMult;
		rTheirPredictedCities += rVassalMult *
				(kTheirAlly.getNumCities() +
				((int)militAnalyst().conqueredCities(kTheirAlly.getID()).size()) -
				((int)militAnalyst().lostCities(kTheirAlly.getID()).size()));
		/*	Ignore cities that their side gains from our human target
			(to avoid dogpiling on human) */
		TeamTypes const eOurTarget = m_kParams.getTarget();
		if (eOurTarget != NO_TEAM && eOurTarget != eTheirTeam &&
			GET_TEAM(eOurTarget).isHuman())
		{
			CitySet const& kConq = militAnalyst().conqueredCities(kTheirAlly.getID());
			for (CitySetIter itCity = kConq.begin(); itCity != kConq.end(); ++itCity)
			{
				CvCity const& kCity = *GC.getMap().getPlotByIndex(*itCity).
						getPlotCity();
				if (kCity.getTeam() == eOurTarget)
					rTheirPredictedCities -= rVassalMult;
			}
			FAssert(rTheirPredictedCities >= 0);
		}
	}
	scaled const rTheirPredictedToCurrCities = (rTheirCurrentCities > 0 ?
			rTheirPredictedCities / rTheirCurrentCities : 1);
	/*	We assume that they are going to attack us some 50 turns from now,
		and they're going to choose the time that suits them best. Therefore,
		cities that they conquer are assumed to contribute to their power,
		whereas conquests by us or our vassals are assumed to be too recent to
		contribute. However, cities of new vassals don't need time to become
		productive. */
	scaled rOurPredictedCities = kOurTeam.getNumCities()
			- (int)militAnalyst().lostCities(eWe).size();
	scaled rOurCurrentCities = kOurTeam.getNumCities();
	TeamSet const& kCapAccepted = militAnalyst().getCapitulationsAccepted(eOurTeam);
	for (PlayerIter<MAJOR_CIV> itOurVassal; itOurVassal.hasNext(); ++itOurVassal)
	{
		CvPlayer const& kOurVassal = *itOurVassal;
		if (GET_TEAM(kOurVassal.getTeam()).isVassal(eOurTeam))
		{
			rOurCurrentCities += fixp(0.5) *
					(kOurVassal.getNumCities()
					- (int)militAnalyst().lostCities(kOurVassal.getID()).size());
		}
		else if (kCapAccepted.count(kOurVassal.getTeam()) > 0)
		{
			rOurPredictedCities += fixp(0.5) *
					(kOurVassal.getNumCities()
					- (int)militAnalyst().lostCities(kOurVassal.getID()).size());
		}
	}
	scaled const rOurPredictedToCurrCities = (rOurCurrentCities > 0 ?
			rOurPredictedCities / rOurCurrentCities : 1);
	// Assume that our gain is equally their loss
	scaled rTheirEdge = rTheirPredictedToCurrCities - rOurPredictedToCurrCities;
	rTheirEdge.clamp(fixp(-0.5), fixp(0.5));
	if (rTheirEdge == 0)
		return;
	log("Long-term threat rating for %s: %d percent", m_kReport.leaderName(eThey),
			rCurrThreat.getPercent());
	log("Our cities (now/predicted) and theirs: %d/%d, %d/%d",
			rOurCurrentCities.uround(), rOurPredictedCities.uround(),
			rTheirCurrentCities.uround(), rTheirPredictedCities.uround());
	log("Their gain in power: %d percent", rTheirEdge.getPercent());
	// Shifts in power tend to affect the threat disproportionately
	scaled rThreatChange = rTheirEdge.abs().sqrt();
	if (rTheirEdge < 0)
		rThreatChange.flipSign();
	log("Change in threat: %d percent", rThreatChange.getPercent());
	scaled rUtility = -90 * rCurrThreat * rThreatChange;
	// Kingmaking should handle the endgame (but not quite there yet)
	if (rUtility.abs().uround() >= 1 && kTheirTeam.AI_anyMemberAtVictoryStage3())
	{
		log("Util from pre-emptive war reduced b/c they're close to victory");
		rUtility *= fixp(0.6);
	}
	scaled rDistrustFactor = kWeAI.distrustRating();
	log("Our distrust: %d percent", rDistrustFactor.getPercent());
	m_iU += (rUtility * rDistrustFactor).round();
}

scaled const KingMaking::m_rScoreMargin = fixp(0.25);

int KingMaking::preEvaluate()
{
	PROFILE_FUNC();
	m_winningFuture.clear();
	m_winningPresent.clear();
	/*	(Scoreboard ranks just aren't meaningful off the bat, even if the game
		starts in the Modern era. Leaving m_winningPresent empty causes 0 utility
		to be counted by evaluate.) */
	if (m_eGameEra <= m_kGame.getStartEra())
		return 0;
	// Don't start or continue suicidal wars out of spite
	if (militAnalyst().isEliminated(eWe))
		return 0;
	addWinning(m_winningFuture, true);
	addWinning(m_winningPresent, false);
	scaled const rEraFactor = kOurTeam.AI_getCurrEraFactor();
	// Sealing the deal through war is a pretty aggressive move
	int const iPeaceWeight = kWe.AI_getPeaceWeight();
	int const iVeryHighPeaceWeight = 11;
	if (iPeaceWeight < iVeryHighPeaceWeight &&
		rEraFactor > 0 &&
		m_winningFuture.count(kOurTeam.getLeaderID()) > 0 &&
		m_winningFuture.size() <= 1 &&
		// We don't want to be the only winner if it means betraying our partners
		(m_kParams.getTarget() == NO_TEAM ||
		kOurTeam.isAtWar(m_kParams.getTarget()) ||
		kOurTeam.AI_isChosenWar(m_kParams.getTarget()) ||
		!kOurTeam.AI_isAvoidWar(m_kParams.getTarget(), true)))
	{
		log("We'll be the only winners; peace weight: %d", iPeaceWeight);
		return (rEraFactor * (iVeryHighPeaceWeight - iPeaceWeight)).round();
	}
	return 0;
}


void KingMaking::addWinning(std::set<PlayerTypes>& kWinning, bool bPredict) const
{
	/*	Three categories of civs; all in the best non-empty category are likely
		winners in our book. Important to base this on the game state predicted
		by the military analysis so that the AI can tell when its actions thwart
		a rival victory or prevent a rival from getting way ahead in score.
		anyVictory and addLeadingPlayers take care of this. */
	// Category III: Civs at victory stage 4
	for (PlayerAIIter<FREE_MAJOR_CIV> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		AIVictoryStage eFlags = itPlayer->AI_getVictoryStageHash();
		if ((eFlags & AI_VICTORY_CULTURE4) &&
			itPlayer->AI_calculateCultureVictoryStage(167) < 4)
		{
			eFlags &= ~AI_VICTORY_CULTURE4;
		}
		if (anyVictory(itPlayer->getID(), eFlags, 4, bPredict))
			kWinning.insert(itPlayer->getID());
	}
	int const iMaxTurns = m_kGame.getMaxTurns();
	int const iTurnsRemaining = ((iMaxTurns - m_kGame.getElapsedGameTurns()) * 100) /
			m_kGame.getSpeedPercent(); // normalized turns
	/*	If we're already past the turn limit, then apparently time victory is disabled.
		(Would be safer but slower to check m_kGame.isVictoryValid in addition.) */
	bool const bTimeVictoryImminent = (iMaxTurns > 0 && iTurnsRemaining > 0 &&
			iTurnsRemaining <= 17);
	if (!bTimeVictoryImminent)
	{
		if (!kWinning.empty()) // Only stage 4 matters unless time victory is imminent
			return;
		// (If none at stage 4 and time victory not imminent)
		// Category II: Civs at victory stage 3 or game score near the top
		for (PlayerAIIter<FREE_MAJOR_CIV> itPlayer; itPlayer.hasNext(); ++itPlayer)
		{
			if (anyVictory(itPlayer->getID(),
				itPlayer->AI_getVictoryStageHash(), 3, bPredict))
			{
				kWinning.insert(itPlayer->getID());
			}
		}
	}
	// Category I: Civs with a competitive game score
	addLeadingPlayers(kWinning, m_rScoreMargin, bPredict);
}


bool KingMaking::anyVictory(PlayerTypes ePlayer, AIVictoryStage eFlags, int iStage,
	bool bPredict) const
{
	FAssert(iStage == 3 || iStage == 4);
	CvPlayerAI const& kPlayer = GET_PLAYER(ePlayer);
	if (!bPredict)
	{
		if (iStage == 3)
			return kPlayer.AI_atVictoryStage3();
		return (eFlags & (AI_VICTORY_SPACE4 | AI_VICTORY_MILITARY4 |
				AI_VICTORY_DIPLOMACY4 | AI_VICTORY_CULTURE4));
	}
	if (militAnalyst().isEliminated(ePlayer) ||
		militAnalyst().hasCapitulated(kPlayer.getTeam()))
	{
		return false;
	}
	if ((eFlags & AI_VICTORY_SPACE4) && iStage == 4)
	{
		if (kPlayer.hasCapital() &&
			militAnalyst().lostCities(ePlayer).
			count(kPlayer.getCapital()->plotNum()) <= 0)
		{
			return true;
		}
	}
	if (eFlags & AI_VICTORY_CONQUEST3)
	{
		/*	Very coarse -- consider a player whose power stagnates to be
			no longer on course to a conquest victory */
		if (militAnalyst().gainedPower(ePlayer, ARMY) > 0)
		{
			if (((eFlags & AI_VICTORY_CONQUEST3) && iStage == 3) ||
				((eFlags & AI_VICTORY_CONQUEST4) && iStage == 4))
			{
				return true;
			}
		}
	}
	// Space4 and Conq already handled above
	bool bCultValid = (iStage == 4 && (eFlags & AI_VICTORY_CULTURE4)) ||
			(iStage == 3 && (eFlags & AI_VICTORY_CULTURE3));
	bool bSpaceValid = (iStage == 3 && (eFlags & AI_VICTORY_SPACE3));
	bool bDomValid = (iStage == 4 && (eFlags & AI_VICTORY_DOMINATION4)) ||
			(iStage == 3 && (eFlags & AI_VICTORY_DOMINATION3));
	bool bDiploValid = (iStage == 4 && (eFlags & AI_VICTORY_DIPLOMACY4)) ||
			(iStage == 3 && (eFlags & AI_VICTORY_DIPLOMACY3));
	/*	Conquests could bring kPlayer closer to a military victory, but that seems
		difficult to predict. Only looking at setbacks here -- which are also
		a bit difficult to predict; the main point of this function is really
		thwarted Culture/Space victory. */
	if (!bCultValid && !bSpaceValid && !bDomValid && !bDiploValid)
		return false;
	CvMap const& kMap = GC.getMap();
	int iLostPop = 0;
	int iLostNationalWonders = 0;
	CitySet const& kLostCities = militAnalyst().lostCities(ePlayer);
	for (CitySetIter it = kLostCities.begin(); it != kLostCities.end(); ++it)
	{
		CvCity const& kCity = *kMap.getPlotByIndex(*it).getPlotCity();
		/*	kPlayer could have enough other high-culture cities, but I don't mind
			if the AI is a bit too optimistic about thwarting a rival's victory
			(or extra worried about jeopardizing its own victory). */
		if ((iStage == 3 &&
			kCity.getCultureLevel() >= m_kGame.culturalVictoryCultureLevel() - 1) ||
			(iStage == 4 &&
			2 * kCity.getCulture(ePlayer) >= kCity.getCultureThreshold(
			m_kGame.culturalVictoryCultureLevel())))
		{
			bCultValid = false;
		}
		iLostNationalWonders += kCity.getNumNationalWonders();
		if (kCity.isCapital())
			iLostNationalWonders += 2;
		iLostPop += kCity.getPopulation();
	}
	if (iLostNationalWonders > 1)
		bSpaceValid = false;
	CitySet const& kGainedCities = militAnalyst().conqueredCities(ePlayer);
	for (CitySetIter it = kGainedCities.begin(); it != kGainedCities.end(); ++it)
	{
		CvCity const& kCity = *kMap.getPlotByIndex(*it).getPlotCity();
		iLostPop -= kCity.getPopulation();
	}
	if (iLostPop > 0)
	{
		scaled const rRemainingWorldPopPortion(
				std::max(0, kPlayer.getTotalPopulation() - iLostPop),
				m_kGame.getTotalPopulation());
		if (rRemainingWorldPopPortion < (iStage == 3 ? fixp(0.32) : fixp(0.375)))
			bDiploValid = false;
		VictoryTypes const eDomination = getDominationVictory();
		if (eDomination != NO_VICTORY)
		{
			if (rRemainingWorldPopPortion <
				getDominationTargetPopPortion() * (iStage == 3 ? fixp(0.8) : 1))
			{
				bDomValid = false;
			}
		}
	}
	return (bCultValid || bSpaceValid || bDomValid || bDiploValid);
}


void KingMaking::addLeadingPlayers(std::set<PlayerTypes>& kLeading, scaled rMargin,
	bool bPredict) const
{
	CvCity const* pOurCapital = kWe.getCapital();
	scaled rBestScore = 1;
	for (PlayerIter<FREE_MAJOR_CIV> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		PlayerTypes const ePlayer = itPlayer->getID();
		scaled rScore = (bPredict ? militAnalyst().predictedGameScore(ePlayer) :
				m_kGame.getPlayerScore(ePlayer));
		CvPlayerAI const& kPlayer = GET_PLAYER(ePlayer);
		/*	Count extra score for commerce so that players that are getting far
			ahead in tech are identified as a threat */
		scaled const rPlayerEraAIFactor = kPlayer.AI_getCurrEraFactor();
		if (rPlayerEraAIFactor > fixp(2.5) &&
			// The late game is covered by victory stages
			rPlayerEraAIFactor < fixp(4.5) && m_rGameEraAIFactor < fixp(4.5))
		{
			scaled rCommerceRate = kOurTeam.AI_estimateYieldRate(ePlayer, YIELD_COMMERCE);
			rScore += rCommerceRate / 2;
			// Beware of peaceful civs on other landmasses
			CvCity const* pPlayerCapital = kPlayer.getCapital();
			if (pOurCapital != NULL && pPlayerCapital != NULL &&
				!pOurCapital->sameArea(*pPlayerCapital) &&
				kPlayer.AI_atVictoryStage(AI_VICTORY_CULTURE2 | AI_VICTORY_SPACE2) &&
				pOurCapital->getArea().getNumStartingPlots() >
				pPlayerCapital->getArea().getNumStartingPlots())
			{
				rScore *= fixp(4/3.);
			}
		}
		rBestScore.increaseTo(rScore);
	}
	for (PlayerIter<FREE_MAJOR_CIV> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		if ((bPredict ? militAnalyst().predictedGameScore(itPlayer->getID()) :
			m_kGame.getPlayerScore(itPlayer->getID())) / rBestScore >=
			(itPlayer->isHuman() ? fixp(0.7) : fixp(0.75)))
		{
			kLeading.insert(itPlayer->getID());
		}
	}
}


void KingMaking::evaluate()
{
	/*	Someone is always ahead; an empty set indicates a special situation
		(usually: too early in the game) in which no utility should be counted. */
	if (m_winningPresent.empty())
		return;
	/*	If they're only in m_winningPresent, i.e. if we expect them to fall back,
		then that'll be covered by comparing utility with a scenario in which they
		don't fall back. (If they fall back in every scenario, then it's apparently
		out of our hands, and no utility needs to be counted.) */
	if (m_winningFuture.count(eThey) <= 0)
		return;
	if (kTheirTeam.isAVassal()) // Assumed to be out of contention
		return;
	/*	As humans we are very much not OK with rivals winning the game,
		so ATTITUDE_FURIOUS would be the smarter assumption, however, I don't want
		a leading AI to be extremely alert about a human runner-up. */
	int iAttitude = (kWe.isHuman() ? ATTITUDE_ANNOYED : towardThem());
	if (kOurTeam.isAtWar(eTheirTeam)) // When at war, bad attitude is normal.
		iAttitude++;
	if (iAttitude >= ATTITUDE_FRIENDLY)
	{	/*	We don't go as far as helping a friend win
			(only indirectly by trying to thwart the victory of a disliked civ) */
		return;
	}
	scaled rAttitudeMult = fixp(0.03) + fixp(0.25) * (ATTITUDE_PLEASED - iAttitude);
	scaled rCaughtUpPremium;
	scaled rCatchUpVal = (16 * m_rGameEraAIFactor) / m_winningPresent.size();
	rCatchUpVal.exponentiate(fixp(0.75));
	rCatchUpVal *= SQR((1 + kWeAI.amortizationMultiplier()) / 2);
	bool bCaughtUp = false;
	// We're less inclined to interfere if several rivals are in competition
	int iWinningRivals = m_winningFuture.size();
	if (m_winningFuture.count(eWe) > 0)
	{
		iWinningRivals--;
		if (m_winningPresent.count(eWe) <= 0)
		{
			/*	We're not presently winning, but our predicted conquests bring us
				back in competition. */
			rCaughtUpPremium += rCatchUpVal;
			bCaughtUp = true;
			log("%d for catching up with %s", rCaughtUpPremium.round(),
					m_kReport.leaderName(eThey));
		}
		else
		{
			/*	If we're among the likely winners, then it's a showdown between us
				and them, and we try to prevent their victory despite being Pleased.
				If we're out of contention (for the time being), we don't mind if
				they win at Pleased. */
			rAttitudeMult += fixp(0.25);
		}
	}
	else if (m_winningPresent.count(eWe) > 0)
	{
		rCaughtUpPremium -= rCatchUpVal;
		// Be more reckless when falling behind
		rAttitudeMult += fixp(0.25);
		log("%d for falling behind %s", rCaughtUpPremium.round(),
				m_kReport.leaderName(eThey));
	}
	if (rAttitudeMult <= 0)
	{
		m_iU += rCaughtUpPremium.round();
		return;
	}
	/*	If they (or their vassals) make a net asset gain, we incur a cost;
		if they make a net asset loss, that's our gain. */
	scaled rTheirLoss = theirRelativeLoss();
	if (rTheirLoss.abs() < fixp(0.01)) // Don't pollute the log then
	{
		m_iU += rCaughtUpPremium.round();
		return;
	}
	scaled rWeight(10,3); // So that 30% loss correspond to 100 utility
	// We're a bit less worried about helping them indirectly
	if (rTheirLoss < 0)
	{
		// If we'll catch up despite their progress, we're even less worried.
		rWeight = (bCaughtUp ? 2 : 3);
	}
	scaled rUtility = rTheirLoss * 100 * rWeight;
	log("%d base utility for change in asset ratio", rUtility.round());
	scaled rCompetitionMult;
	{
		/*	Over the course of the game, we become more willing to take out rivals
			even if several rivals are still in competition. */
		scaled rProgressFactor = fixp(3/4.) - fixp(1/3.) * m_kGame.gameTurnProgress();
		FAssert(rProgressFactor > 0);
		scaled rDiv = 1 + SQR(rProgressFactor * iWinningRivals);
		rCompetitionMult = 1 / rDiv;
	}
	log("Winning civs: %d (%d rivals)", (int)m_winningFuture.size(), iWinningRivals);
	rUtility.clamp(-100, 100);
	log("Attitude multiplier: %d percent, competition multiplier: %d percent",
			rAttitudeMult.getPercent(), rCompetitionMult.getPercent());
	rUtility *= rAttitudeMult * rCompetitionMult;
	if (rUtility.abs() < fixp(0.5)) // Report confusing to read w/o this
		log("(Kingmaking gain from %s negligibly small)", m_kReport.leaderName(eThey));
	m_iU += (rUtility + rCaughtUpPremium).round();
}


scaled KingMaking::theirRelativeLoss() const
{
	PROFILE_FUNC();
	if (!militAnalyst().isPartOfAnalysis(eThey)) // To save time
		return 0;
	// Ignore assets that they gain from human target (to avoid dogpiling on human)
	TeamTypes eIgnoreGains = m_kParams.getTarget();
	if (eIgnoreGains != NO_TEAM && !GET_TEAM(eIgnoreGains).isHuman())
		eIgnoreGains = NO_TEAM;
	TeamSet const& kCapitulationsAccepted = militAnalyst().
			getCapitulationsAccepted(eTheirTeam);
	scaled rTheirLostAssets;
	scaled rTheirAssets;
	for (PlayerIter<MAJOR_CIV> itTheirAlly; itTheirAlly.hasNext(); ++itTheirAlly)
	{	// Them or a teammate or vassal of them
		PlayerTypes const eTheirAlly = itTheirAlly->getID();
		CvTeam const& kTheirAllyTeam = GET_TEAM(eTheirAlly);
		scaled rVassalFactor = 1;
		if (kTheirAllyTeam.isAVassal())
			rVassalFactor /= 2;
		if (kTheirAllyTeam.getMasterTeam() != eTheirTeam)
		{
			if (kCapitulationsAccepted.count(kTheirAllyTeam.getID()) > 0)
			{
				scaled rAssets;
				netLostRivalAssetScore(NO_PLAYER, &rAssets);
				scaled rTheirGain = rVassalFactor *
						remainingCityRatio(eTheirAlly) * rAssets;
				log("Gained from new vassal: %d", rTheirGain.round());
				rTheirLostAssets -= rTheirGain;
			}
			continue;
		}
		scaled rAssets;
		// can be negative
		scaled rLostAssets = netLostRivalAssetScore(NO_PLAYER, &rAssets, eIgnoreGains);
		rTheirAssets += rVassalFactor * rAssets;
		rTheirLostAssets += rVassalFactor * rLostAssets;
	}
	if (rTheirAssets <= 0)
	{
		// They haven't founded a city yet; can happen in late-era start
		return 0;
	}
	return rTheirLostAssets / rTheirAssets;
}

namespace
{
	/*	Kludge. ArmamentForecast will often predict dramatic increases in
		military power. Not sure how wrong those are, but I don't want to
		base the evaluation of future uses for military units on such
		grandiose projections. */
	void adjustPowerChangeProjection(scaled& rChange)
	{
		if (rChange > fixp(1.5))
		{
			rChange.exponentiate(fixp(0.5));
			rChange *= fixp(1.225);
		}
	}
}

int Effort::preEvaluate()
{
	/*	Not nice to put all code into this supposedly preparatory function.
		For most aspects, it makes sense to assign utility to each war opponent
		separately (WarUtilityAspect::evaluate(0)), but, for this aspect, the
		simulation doesn't track against whom we lose units, and our military
		build-up isn't directed against any opponent in particular. */
	scaled rUtility; // (Positive value, will be subtracted in the end.)
	// For civic and research changes at wartime:
	if (!militAnalyst().getWarsContinued(eWe).empty() ||
		!militAnalyst().getWarsDeclaredBy(eWe).empty())
	{
		bool bAllWarsLongDist = true;
		bool bAllPushOver = true;
		PlyrSet const& kWeContinue = militAnalyst().getWarsContinued(eWe);
		for (PlyrSetIter it = kWeContinue.begin(); it != kWeContinue.end(); ++it)
		{
			if (kWe.AI_hasSharedPrimaryArea(*it))
				bAllWarsLongDist = false;
			if (!kOurTeam.AI_isPushover(TEAMID(*it)))
				bAllPushOver = false;
		}
		PlyrSet const& kWeDeclare = militAnalyst().getWarsDeclaredBy(eWe);
		for (PlyrSetIter it = kWeDeclare.begin(); it != kWeDeclare.end(); ++it)
		{
			if (kWe.AI_hasSharedPrimaryArea(*it))
				bAllWarsLongDist = false;
			if (!kOurTeam.AI_isPushover(TEAMID(*it)))
				bAllPushOver = false;
		}
		if (bAllPushOver)
		{
			/*	Can't be sure that this won't lead to a change in civics
				(though it shouldn't); therefore not 0 cost. */
			rUtility += 2;
			log("All targets are short work; only %d for wartime economy",
					rUtility.uround());
		}
		else
		{
			/*	Reduced cost for long-distance war; less disturbance of Workers
				and Settlers, and less danger of pillaging. */
			rUtility += militAnalyst().turnsSimulated() /
					((bAllWarsLongDist ? 10 : 7) +
					// Workers not much of a concern later on
					kWe.AI_getCurrEraFactor() / 2);
			log("Cost for wartime economy and ravages: %d%s", rUtility.uround(),
					(bAllWarsLongDist ? " (reduced b/c of distance)" : ""));
		}
	}
	scaled rGoldPerProduction = ourCache().goldValueOfProduction();
	log("1 production valued as %.2f gold", rGoldPerProduction.getFloat());
	// Rather use the max over all wars?
	int const iDuration = kOurTeam.AI_getAtWarCounter(m_kParams.getTarget());
	/*	How powerful are we relative to our rivals at the end of the simulation?
		Simpler to use the BtS power ratio here than to go through all military
		branches. Our rival's per-branch power isn't public info either.
		The simulation yields per-branch losses though. Use relative losses
		in armies to predict the BtS power ratios. */
	scaled rOurPowerChange = militAnalyst().gainedPower(eWe, ARMY) /
			(ourCache().getPowerValues()[ARMY]->power() + scaled::epsilon());
	adjustPowerChangeProjection(rOurPowerChange); // Don't drink the koolaid
	scaled const rOurPower = kWe.getPower() * (1 + rOurPowerChange);
	scaled rHighestRivalPower;
	for (PlayerAIIter<MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> itRival(eOurTeam);
		itRival.hasNext(); ++itRival)
	{
		CvPlayerAI const& kRival = *itRival;
		scaled rRivalPowerChange = militAnalyst().gainedPower(kRival.getID(), ARMY);
		/*	If they're not part of the military analysis, estimate their power based
			on BtS statistics. */
		if (rRivalPowerChange == 0)
		{
			rRivalPowerChange = kWeAI.estimateBuildUpRate(kRival.getID(),
					militAnalyst().turnsSimulated());
		}
		else
		{
			rRivalPowerChange /= (GET_PLAYER(kRival.getID()).uwai().getCache().
					getPowerValues()[ARMY]->power() + scaled::epsilon());
		}
		adjustPowerChangeProjection(rRivalPowerChange);
		scaled rRivalPower = kRival.getPower() * (1 + rRivalPowerChange);
		if (kWe.isHuman())
			rRivalPower *= kRival.uwai().confidenceAgainstHuman();
		else if (kRival.isHuman())
			rRivalPower *= 1 / (kWeAI.confidenceAgainstHuman() + scaled::epsilon());
		rHighestRivalPower.increaseTo(rRivalPower);
	}
	// Express our losses in terms of production
	scaled rOurLostProductionInUnits;
	scaled rOurLostUnits;
	for (int i = 0; i < NUM_BRANCHES; i++)
	{
		MilitaryBranchTypes const eBranch = (MilitaryBranchTypes)i;
		if (eBranch == CAVALRY || eBranch == LOGISTICS) // Included in other branches
			continue;
		MilitaryBranch const& kBranch = *ourCache().getPowerValues()[eBranch];
		UnitTypes const eTypicalUnit = kBranch.getTypicalUnit();
		if (eTypicalUnit == NO_UNIT)
			continue;
		scaled rLostBranchPow = militAnalyst().lostPower(eWe, eBranch);
		/*	Really shouldn't be negative, but sometimes it was
			minus 0.0-something; probably not a bug worth chasing. */
		FAssert(rLostBranchPow >= -1);
		if (rLostBranchPow < 0)
			continue;
		scaled const rTypicalPow = kBranch.getTypicalPower(eOurTeam);
		scaled rLostBranchUnits = rLostBranchPow / rTypicalPow;
		rOurLostUnits += rLostBranchUnits;
		scaled const rTypicalCost = kBranch.getTypicalCost(eOurTeam);
		FAssert(rTypicalCost > 0);
		rOurLostProductionInUnits += rTypicalCost * rLostBranchUnits;
	}
	/*	How useful are units that survive the war going forward?
		If we'll be far more powerful than our most dangerous rival, we probably
		have more units than we need.
		Some of the lost units may also be outdated chaff that we would have to
		upgrade soon if we didn't lose them. */
	scaled rFutureUse = rHighestRivalPower / (rOurPower + scaled::epsilon());
	rFutureUse.clamp(fixp(0.35), fixp(1.65));
	/*	Division by e.g. 2.2 means survivors can be valued up to 75%; 2.75: 60%
		(not taking into account the exponentiation below) */
	rFutureUse /= fixp(2.55);
	rFutureUse.exponentiate(fixp(0.75));
	if (!kWe.isHuman())
	{
		rFutureUse += scaled::max(0,
				// I.e. add between 3 (Gandhi) and 8 (Ragnar) percentage points
				scaled(kOurPersonality.getBuildUnitProb(), 500));
	}
	scaled const rInvested = militAnalyst().militaryProduction(eWe);
	scaled const rOurLostProduction = rOurLostProductionInUnits * rFutureUse +
			rInvested *
			/*	Total vs. limited war is already reflected by ArmamentForecast,
				but a strong focus on military build-up is extra harmful b/c
				even essential buildings may not get constructed then. */
			(1 - rFutureUse) * (m_kParams.isTotal() ? fixp(1.1) : 1) *
			// Future use of transports is a long shot
			(m_kParams.isNaval() ? fixp(1.2) : 1);
	log("Production value of lost units: %d, invested production: %d,"
			" multiplier for future use of trained units: %d percent, "
			"adjusted production value of build-up and losses: %d",
			rOurLostProductionInUnits.uround(), rInvested.uround(),
			rFutureUse.getPercent(), rOurLostProduction.uround());
	scaled rSupplyCost; // Assume none if we're losing (i.e. on the defensive)
	if (militAnalyst().lostCities(eWe).empty() && rOurLostUnits > 0)
	{
		/*	Use rOurLostUnits as a measure of the number of active fighters.
			No need to apply the handicap modifier; humans can avoid supply much
			better than the AI; that ought to cancel out.
			Halved because some of the simulated turns may be preparation,
			and even fighting units aren't constantly in foreign borders. */
		rSupplyCost = militAnalyst().turnsSimulated() * fixp(0.5) * rOurLostUnits;
		if (militAnalyst().conqueredCities(eWe).empty())
		{	// Not clear that we're on the offensive
			rSupplyCost /= 2;
		}
		log("Estimated gold for supply: %d (%d turns simulated, %d units lost)",
				rSupplyCost.uround(), militAnalyst().turnsSimulated(),
				rOurLostUnits.uround());
		rSupplyCost *= kWeAI.amortizationMultiplier();
	}
	/*	If the war has been going on for a long time, increase rGoldPerProduction
		because opportunities for peaceful development might get overlooked
		(by UWAICache::updateGoldPerProduction) in a wartime economy. (Maybe this
		is handwaving and I just want to discourage long, indecisive wars.) */
	int const iGiveWarAChanceDuration = 15;
	int iExtraDuration = iDuration - iGiveWarAChanceDuration;
	if (iExtraDuration > 0)
	{
		scaled rGameSpeedDiv = per100(m_kGame.getSpeedPercent());
		scaled const rVagueOpportunityWeight = fixp(2.3); // pretty arbitrary
		rGoldPerProduction = scaled::min(5, rGoldPerProduction *
				(1 + rVagueOpportunityWeight * fixp(0.025) *
				std::min(iExtraDuration, 40) / rGameSpeedDiv));
		log("Gold per production adjusted to %.2f based on war duration (%d turns)",
				rGoldPerProduction.getFloat(), iDuration);
	}
	scaled rTradeVal = rSupplyCost + rGoldPerProduction * rOurLostProduction;
	log("Trade value of build-up and war effort: %d", rTradeVal.uround());
	rUtility += kWeAI.tradeValToUtility(rTradeVal);
	/*	Nukes are included in army, and therefore already covered by the costs above.
		But these don't take into account that nukes are always lost when used.
		Therefore add some extra cost. */
	scaled const rFired = militAnalyst().getNukesFiredBy(eWe);
	MilitaryBranch const& kNukeBranch = *ourCache().getPowerValues()[NUCLEAR];
	UnitTypes const eNuke = kNukeBranch.getTypicalUnit();
	if (eNuke != NO_UNIT && rFired > 0)
	{
		/*	Not clear that we have to replace the fired nukes.
			Reduce the lost production to about a third for that reason,
			and b/c already partially covered by army losses. */
		scaled rNukeProduction = fixp(0.3) * rFired * kNukeBranch.getTypicalCost();
		scaled rNukeCost = kWeAI.tradeValToUtility(rGoldPerProduction * rNukeProduction);
		log("Extra cost for fired nukes: %d; lost prod: %d",
				rNukeCost.uround(), rNukeProduction.uround());
		rUtility += rNukeCost;
	}
	return -std::min(200, rUtility.round());
}


void Effort::evaluate() {}


int Risk::preEvaluate()
{
	// Handle potential losses of our vassals here
	scaled rUtility; // (Positive value, gets subtracted in the end.)
	for (PlayerIter<ALIVE,VASSAL_OF> itVassal(eOurTeam); itVassal.hasNext(); ++itVassal)
	{
		PlayerTypes const eVassal = itVassal->getID();
		CvPlayerAI const& kVassal = GET_PLAYER(eVassal);
		// OK to peek into our vassal's cache
		UWAICache const& kVassalCache = kVassal.uwai().getCache();
		scaled rRelativeVassalLoss = 1;
		if (!militAnalyst().isEliminated(eVassal))
		{
			scaled rLostVassalAssets;
			CitySet const& kLostCities = militAnalyst().lostCities(eVassal);
			for (CitySetIter it = kLostCities.begin(); it != kLostCities.end(); ++it)
			{
				City const* pCacheCity = kVassalCache.lookupCity(*it);
				if (pCacheCity == NULL)
					continue;
				rLostVassalAssets += pCacheCity->getAssetScore();
			}
			rRelativeVassalLoss = rLostVassalAssets /
					scaled::max(1, kVassalCache.totalAssetScore());
		}
		scaled rVassalCost; // (i.e. negative utility)
		if (rRelativeVassalLoss > 0)
		{	/*	advc.test: Total asset score less than the sum of the city scores.
				Had not worked correctly when called from UWAI::processNewPlayerInGame.
				Should be fixed now; let's see ... */
			FAssert(rRelativeVassalLoss <= 1);
			rRelativeVassalLoss.decreaseTo(1);
			rVassalCost = rRelativeVassalLoss * 33;
			log("Cost for losses of vassal %s: %d", m_kReport.leaderName(eVassal),
					rVassalCost.uround());
		}
		if (!GET_TEAM(eVassal).isCapitulated())
		{
			scaled rRelativePow =
					(militAnalyst().gainedPower(eVassal, ARMY) +
					kVassalCache.getPowerValues()[ARMY]->power()) /
					(militAnalyst().gainedPower(eWe, ARMY) +
					ourCache().getPowerValues()[ARMY]->power() + scaled::epsilon());
			rRelativePow -= fixp(0.9);
			if (rRelativePow > 0)
			{
				scaled rBreakAwayCost = scaled::min(20, rRelativePow.sqrt() * 40);
				if (rBreakAwayCost >= fixp(0.5))
				{
					log("Cost for %s breaking free: %d", m_kReport.leaderName(eVassal),
							rBreakAwayCost.uround());
				}
				rVassalCost += rBreakAwayCost;
			}
		}
		rUtility += rVassalCost;
	}
	return -rUtility.round();
}


void Risk::evaluate()
{
	PROFILE_FUNC();
	/*	Thwarted victory is mainly handled by Kingmaking::anyVictory, but, so long
		as one victory condition remains feasible/imminent, that function won't
		yield negative utility. Therefore count some extra lost assets for lost cities
		that are important for a victory condition. */
	bool const bSpace4 = kWe.AI_atVictoryStage(AI_VICTORY_SPACE4);
	bool const bCulture3 = kWe.AI_atVictoryStage(AI_VICTORY_CULTURE3);
	bool const bCulture4 = bCulture3 && kWe.AI_atVictoryStage(AI_VICTORY_CULTURE4);
	scaled rLostAssets;
	CitySet const& kWeLose = militAnalyst().lostCities(eWe);
	for (CitySetIter it = kWeLose.begin(); it != kWeLose.end(); ++it)
	{
		/*	It doesn't matter here whom the city is lost to, but looking at
			one enemy at a time produces better debug output. */
		if (militAnalyst().conqueredCities(eThey).count(*it) <= 0)
			continue;
		City const& kCacheCity = *ourCache().lookupCity(*it);
		scaled rAssetScore = kCacheCity.getAssetScore();
		CvCity const& kCity = kCacheCity.city();
		if (bSpace4)
		{
			if (kCity.isCapital() && kWe.AI_atVictoryStage(AI_VICTORY_SPACE4))
				rAssetScore += 15;
		}
		if (bCulture3)
		{
			// Same condition as in CvPlayerAI::AI_conquerCity
			if (2 * kCity.getCulture(kCity.getOwner()) >=
				kCity.getCultureThreshold(m_kGame.culturalVictoryCultureLevel()))
			{
				rAssetScore += (bCulture4 ? 15 : 8);
			}
		}
		log("%s: %d lost assets%s", m_kReport.cityName(kCity), rAssetScore.round(),
				(bCulture3 || bSpace4 ? " (important for victory)" : ""));
		rLostAssets += rAssetScore;
	}
	rLostAssets.increaseTo(0); // Per-city score can be negative (maintenance)
	scaled rUtility = 400 * rLostAssets; // (Will be subtracted in the end)
	scaled const rTotalAssets = ourCache().totalAssetScore() + scaled::epsilon();
	scaled rFromBlockade = lossesFromBlockade(eWe, eThey) * fixp(0.1) *
			(rTotalAssets - rLostAssets);
	rFromBlockade.increaseTo(0);
	rUtility += rFromBlockade;
	scaled rFromNukes = 400 * lossesFromNukes(eWe, eThey);
	int const iScareCost = 26;
	if (kThey.getNumNukeUnits() > 0 &&
		militAnalyst().getWarsDeclaredBy(eWe).count(eThey) > 0 &&
		kTheirTeam.getNumWars() <= 0 && rFromNukes <= iScareCost)
	{
		log("Nuke cost raised to %d for fear", iScareCost);
		rFromNukes = iScareCost;
	}
	rUtility += rFromNukes;
	/*	advc.035 (comment): Don't consider lossFromFlippedTiles here. We might
		capture the very cities that steal our tiles by continuing the war. */
	rUtility /= rTotalAssets;
	if (rUtility >= fixp(0.5))
	{
		if (rFromBlockade / rTotalAssets >= fixp(0.5))
			log("From naval blockade: %d", (rFromBlockade / rTotalAssets).uround());
		if (rFromNukes / rTotalAssets >= fixp(0.5))
			log("From nukes: %d", (rFromNukes / rTotalAssets).uround());
		log("Cost for lost assets: %d (loss: %d, present: %d)",
				rUtility.round(), rLostAssets.uround(), rTotalAssets.uround());
	}
	if (militAnalyst().getCapitulationsAccepted(eTheirTeam).count(eOurTeam) > 0)
	{	/*	Counting lost cities in addition to capitulation might make us too
			afraid of decisively lost wars. Then again, perhaps one can never be too
			afraid of those? */
		rUtility /= 2;
		int const iCostForCapitulation = 100;
		rUtility += iCostForCapitulation;
		log("Cost halved because of capitulation; %d added", iCostForCapitulation);
	}
	/*	Count something extra for elimination just to make sure that peace is
		sought even when fighting multiple hopeless wars. */
	if (militAnalyst().isEliminated(eWe) && militAnalyst().isWar(eWe, eThey) &&
		/*	Don't require them to conquer any cities in the military analysis.
			Another war enemy may get to us much faster, but it's still good
			to end wars with any dangerous enemy. */
		kThey.uwai().getCache().numReachableCities(eWe) >= kWe.getNumCities() &&
		/*	Require _some_ action though; don't want players to declare war
			just to extract some reparations. */
		kTheirTeam.AI_getWarSuccess(eOurTeam) >= GC.getWAR_SUCCESS_CITY_CAPTURING())
	{
		rUtility += kThey.getNumCities(); // a little arbitrary ...
	}
	m_iU -= rUtility.round();
}


int IllWill::preEvaluate()
{
	int iHostiles = 0;
	for (PlayerAIIter<FREE_MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> itHostile(eOurTeam);
		itHostile.hasNext(); ++itHostile)
	{
		if (militAnalyst().isWar(eWe, itHostile->getID()) ||
			(!itHostile->isHuman() &&
			itHostile->AI_getAttitude(eWe) <= ATTITUDE_ANNOYED))
		{
			iHostiles++;
		}
	}
	int iPartners = countFreeRivals<true>() - iHostiles;
	m_rAltPartnerFactor = scaled(1, std::max(1, iPartners - 3)).sqrt();
	return 0;
}


void IllWill::evaluate() 
{
	PROFILE_FUNC();
	m_rCost = 0;
	// We can't trade with our war enemies
	evalLostPartner();
	bool const bEndNigh = (kOurTeam.AI_anyMemberAtVictoryStage4() ||
			kTheirTeam.AI_anyMemberAtVictoryStage4());
	if ((!bEndNigh && !kOurTeam.isAVassal() && !kTheirTeam.isAVassal()) ||
		kWe.AI_atVictoryStage(AI_VICTORY_DIPLOMACY4) ||
		kThey.AI_atVictoryStage(AI_VICTORY_DIPLOMACY4))
	{
		// Civs (our potential partners) don't like when we attack their (other) partners
		evalAngeredPartners();
	}
	if (!bEndNigh && !kOurTeam.isAVassal() && !kTheirTeam.isAVassal() &&
		!militAnalyst().hasCapitulated(eOurTeam) && !militAnalyst().isEliminated(eWe) &&
		!militAnalyst().hasCapitulated(eTheirTeam) && !militAnalyst().isEliminated(eThey))
	{
		// Ill will from war makes them more likely to attack us in the future
		evalRevenge();
	}
	scaled rNukeCost;
	// Fired but intercepted nukes don't cause bad diplo
	scaled rCitiesWeNuked = militAnalyst().getNukedCities(eWe, eThey);
	if (rCitiesWeNuked > 0)
		rNukeCost = nukeCost(rCitiesWeNuked);
	if (rNukeCost >= fixp(0.5))
		log("Diplo cost for nukes: %d", rNukeCost.round());
	// NB: Subroutines have added to m_rCost
	m_rCost += rNukeCost;
	m_iU -= m_rCost.round();
}


scaled IllWill::nukeCost(scaled rCitiesWeNuked) const
{
	if (kThey.isHuman() ||
		100 * diploTowardUs() >
		120 * GC.getDefineINT(CvGlobals::RELATIONS_THRESH_FRIENDLY) ||
		towardUs() <= ATTITUDE_FURIOUS || towardThem() <= ATTITUDE_FURIOUS)
	{
		return 0;
	}
	scaled rNukeCost;
	for (PlayerAIIter<FREE_MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> itThird(eOurTeam);
		itThird.hasNext(); ++itThird)
	{
		CvPlayerAI const& kThirdPlayer = *itThird;
		if (kThirdPlayer.getTeam() == eTheirTeam || kThirdPlayer.isHuman() ||
			militAnalyst().isWar(eWe, kThirdPlayer.getID()) ||
			kThirdPlayer.AI_getAttitudeVal(eWe) > 12 ||
			kThirdPlayer.AI_getAttitude(eThey) < ATTITUDE_PLEASED)
		{
			continue;
		}
		scaled rAttitudeFactor = 3;
		/*	If they like us too, we don't necessarily get a penalty due to change
			130q. Small factor anyway since, this late in the game, we mostly care
			about other civs as war allies or enemies. */
		if (kThirdPlayer.AI_getAttitude(eWe) >= ATTITUDE_PLEASED)
			rAttitudeFactor /= 2;
		log("Diplo penalty from %s: %d times %.2f", m_kReport.leaderName(kThirdPlayer.getID()),
				rAttitudeFactor.round(), rCitiesWeNuked.getFloat());
		rNukeCost += rAttitudeFactor * rCitiesWeNuked;
	}
	rNukeCost.decreaseTo(40);
	return rNukeCost;
}


void IllWill::evalLostPartner()
{
	if (countFreeRivals<false>() < 2)
	{
		// Zero-sum game then, and our loss is equally their loss.
		return;
	}
	bool const bTheyCapitulated = (kTheirTeam.isCapitulated() ||
			militAnalyst().hasCapitulated(eTheirTeam));
	if (kOurTeam.isAtWar(eTheirTeam))
	{
		if (militAnalyst().isWar(eWe, eThey) ||
			militAnalyst().isEliminated(eThey))
		{
			return;
		}
		// Ending the war - can we reconcile with them?
		scaled rDiploDiv = fixp(0.7);
		if (!kThey.isHuman())
		{
			// Only master attitude matters for capitulated vassals (b/c of change 130v)
			if (!bTheyCapitulated &&
				(towardUs() <= ATTITUDE_FURIOUS ||
				// Takes two to tango
				(!kWe.isHuman() && towardThem() <= ATTITUDE_FURIOUS)))
			{
				rDiploDiv += fixp(0.3);
			}
			// Rare as this may be ...
			if (towardThem() >= ATTITUDE_CAUTIOUS)
				rDiploDiv -= fixp(0.15);
			if (towardUs() >= ATTITUDE_CAUTIOUS)
				rDiploDiv -= fixp(0.15);
		}
		/*	Humans are forgiving and tend to end wars quickly. This
			special treatment should lead to slightly greater willingness to
			declare war against human (handled at the end of this function),
			but also slightly greater willingness to make peace again. */
		else rDiploDiv -= fixp(0.15);
		// Don't expect much from reconciling with minor players
		if (militAnalyst().isEliminated(eThey) || bTheyCapitulated)
			rDiploDiv = 2;
		// Reconciliation is a long shot for the AI
		scaled rReconciliationUtility =
				4 * (m_rAltPartnerFactor / rDiploDiv) *
				kWeAI.amortizationMultiplier();
		log("%d for the possibility of reconciliation",
				rReconciliationUtility.round());
		m_rCost -= rReconciliationUtility;
		return;
	}
	if (!militAnalyst().isWar(eWe, eThey))
		return;
	scaled rPartnerUtil = partnerUtilFromTrade() +
			/*	Don't expect to trade anything with a capitulated vassal that the
				master wouldn't trade */
			(bTheyCapitulated ? 0 : partnerUtilFromTech()) +
			partnerUtilFromMilitary();
	// Halved because can still enter their borders by force.
	if (kOurTeam.isOpenBorders(eTheirTeam))
		rPartnerUtil += iPartnerUtilFromOB / (bTheyCapitulated ? 4 : 2);
	log("Base partner utility from %s: %d", m_kReport.leaderName(eThey),
			rPartnerUtil.round());
	log("Modifier for alt. partners: %d percent", m_rAltPartnerFactor.getPercent());
	scaled rUtility = rPartnerUtil * m_rAltPartnerFactor;
	// They may help us again in the future (if we don't go to war with them)
	if (kWe.AI_getMemoryCount(eThey, MEMORY_GIVE_HELP) > 0)
	{
		scaled rGiftUtility = 5 * kWeAI.amortizationMultiplier();
		log("%d for given help", rGiftUtility.round());
		rUtility += rGiftUtility;
	}
	scaled const rHumanMult = fixp(0.81);
	if (kThey.isHuman())
	{
		log("Lost-partner cost reduced b/c humans are forgiving");
		rUtility *= rHumanMult;
	}
	if (kWe.isHuman())
		rUtility *= rHumanMult;
	m_rCost += rUtility;
}


void IllWill::evalRevenge()
{
	if (!militAnalyst().isWar(eWe, eThey) ||
		// Looks like they won't be a threat for long
		militAnalyst().lostCities(eThey).size() > 1)
	{
		return;
	}
	scaled const rTheirToOurPow = theirToOurPowerRatio();
	/*	Mainly care about the case where relations are worsened by our DoW;
		otherwise, PreEmptiveWar handles it. Special case however:
		They're far more powerful than we are, have already taken all our cities
		that were easy to reach and now we expect them to go after some easily
		reachable war ally of ours (who also won't stand a chance).
		So we're (presumably) safe for the moment, but staying at war is a
		long-term risk. Offering a token of goodwill might help and can't really hurt.
		This isn't a matter of PreEmptiveWar b/c the trend of the power ratio
		isn't relevant here - they'll always be stronger than us. */
	if (kOurTeam.isAtWar(eTheirTeam))
	{
		if (rTheirToOurPow > fixp(1.45) &&
			kTheirTeam.AI_getWarSuccess(eOurTeam) -
			kOurTeam.AI_getWarSuccess(eTheirTeam) >
			fixp(2.4) * GC.getWAR_SUCCESS_CITY_CAPTURING())
		{
			/*	If we expect to lose further cities to them,
				then they're not distracted; the Risk aspect will handle it. */
			CitySet const& kWeLose = militAnalyst().lostCities(eWe);
			for (CitySetIter it = kWeLose.begin(); it != kWeLose.end(); ++it)
			{
				if (militAnalyst().conqueredCities(eThey).count(*it) > 0)
					return;
			}
			// If they're not succeeding overall, then our coalition may yet beat them.
			if (kTheirTeam.AI_getWarSuccessRating() < 30)
				return;
			/*scaled rMult(kOurTeam.AI_getWarSuccessRating(), -10);
			rMult.clamp(3, fixp(6.5));*/ // Instead of the 5.5?
			scaled rHopelessStalemateCost = (1 - kWe.uwai().prideRating()) * fixp(5.5);
			log("Cost for hopeless stalemate: %d", rHopelessStalemateCost.uround());
			m_rCost += rHopelessStalemateCost;
		}
		return;
	}
	scaled rRevengeCost;
	/*	Even if they're not a major threat, they may well cause us some inconvenience,
		in particular, as part of a coalition. */
	if (rTheirToOurPow > fixp(0.7))
		rRevengeCost += 4;
	// If relations are already bad, a war won't make matters far worse.
	scaled rAttitudeMult = 1;
	if (kThey.isHuman())
		rAttitudeMult = fixp(0.67);
	else if (towardUs() <= ATTITUDE_FURIOUS)
		rAttitudeMult = fixp(0.2);
	else if (towardUs() == ATTITUDE_ANNOYED)
		rAttitudeMult = fixp(0.5);
	else if (towardUs() == ATTITUDE_CAUTIOUS)
		rAttitudeMult = fixp(0.85);
	scaled rPowRatioMult = rTheirToOurPow - 1;
	rPowRatioMult.clamp(0, 1);
	rRevengeCost += rPowRatioMult * 28 * rAttitudeMult;
	if (rRevengeCost >= fixp(0.5))
	{
		log("Cost for possible revenge: %d (attitude mult.: %d percent)",
				rRevengeCost.round(), rAttitudeMult.getPercent());
	}
	m_rCost += rRevengeCost;
}


scaled IllWill::theirToOurPowerRatio() const
{
	/*	Don't count vassals; they're not a reliable defense (and it's easier
		to exclude them). */
	scaled rOurPow = ourCache().getPowerValues()[ARMY]->power() +
			militAnalyst().gainedPower(eWe, ARMY);
	if (kThey.isHuman())
		rOurPow *= kWeAI.confidenceAgainstHuman();
	scaled rTheirPow = kThey.uwai().getCache().getPowerValues()[ARMY]->power() +
			militAnalyst().gainedPower(eThey, ARMY);
	if (kWe.isHuman())
		rTheirPow *= kThey.uwai().confidenceAgainstHuman();
	scaled r = rTheirPow / scaled::max(10, rOurPow);
	log("Power ratio %s:%s after military analysis: %d percent",
			m_kReport.leaderName(eThey), m_kReport.leaderName(eWe), r.getPercent());
	return r;
}


void IllWill::evalAngeredPartners()
{
	if (kThey.isHuman() || militAnalyst().isWar(eWe, eThey) ||
		// When nothing can alienate them ...
		100 * diploTowardUs() > 120 * GC.getDefineINT(CvGlobals::RELATIONS_THRESH_FRIENDLY) ||
		eTheirTeam == eOurTeam)
	{
		return;
	}
	// 2 only for Gandhi; else 1.
	scaled const rPenaltyPerDoW = (m_kGame.isOption(GAMEOPTION_RANDOM_PERSONALITIES) ? 1 :
			-per100(GC.getInfo(kThey.getPersonalityType()).
			getMemoryAttitudePercent(MEMORY_DECLARED_WAR_ON_FRIEND)));
	scaled rPenalties;
	PlyrSet const& kWeDecl = militAnalyst().getWarsDeclaredBy(eWe);
	for (PlyrSetIter it = kWeDecl.begin(); it != kWeDecl.end(); ++it)
	{
		if (GET_TEAM(*it).isAVassal() || eTheirTeam == TEAMID(*it))
			continue;
		//if (kThey.AI_getAttitude(*it) >= ATTITUDE_PLEASED)
		if (kThey.AI_disapprovesOfDoW(eOurTeam, TEAMID(*it))) // advc.130h
		{
			log("-%d relations with %s for DoW on %s", rPenaltyPerDoW.floor(),
					m_kReport.leaderName(eThey), m_kReport.leaderName(*it));
			rPenalties += rPenaltyPerDoW;
		}
	}
	if (rPenalties <= 0)
		return;
	bool const bWillDisplease = (kThey.AI_getAttitudeFromValue(
			// -1 b/c barely Pleased could quickly tip to Cautious
			diploTowardUs() - rPenalties.floor() - 1) <= ATTITUDE_CAUTIOUS);
	scaled rTheirToOurPow = theirToOurPowerRatio();
	rTheirToOurPow.decreaseTo(1000); // avoid overflow
	scaled rCostPerPenalty =
			partnerUtilFromTrade() + partnerUtilFromTech() +
			partnerUtilFromMilitary() +
			(kOurTeam.isOpenBorders(eTheirTeam) ? iPartnerUtilFromOB : 0) +
			(bWillDisplease ? std::min(fixp(14.5), 9 * SQR(rTheirToOurPow)) : 0);
	rCostPerPenalty /=
			((bWillDisplease && towardUs() >= ATTITUDE_CAUTIOUS) ?
			fixp(3.75) : fixp(5.25)) *
			/*	Don't worry quite as much about diplo in team games. AI DoW
				aren't as dynamic, and it's sufficient for tech trading if some
				team members get along. */
			scaled(kOurTeam.getNumMembers()).sqrt();
	log("Cost per -1 relations: %d", rCostPerPenalty.uround());
	/*	costPerPenalty already adjusted to game progress, but want to dilute
		the impact of leader personality in addition to that. diploWeight is
		mostly about trading, and trading becomes less relevant in the latem_kGame. */
	scaled rDiploWeight = 1 + (kWeAI.diploWeight() - 1) * kWeAI.amortizationMultiplier();
	// The bad diplo hurts us, but our anger at eThey is difficult to contain.
	if (!kWe.isHuman() && towardThem() <= ATTITUDE_FURIOUS)
		rDiploWeight /= 2;
	/*	We've actually one partner less b/c we're considering alternatives to a
		partner that (probably) isn't counted by preEvaluate as hostile. */
	m_rCost += rCostPerPenalty * rPenalties * rDiploWeight * m_rAltPartnerFactor;
	log("Diplo weight: %d percent, alt.-partner factor: %d percent",
			rDiploWeight.getPercent(), m_rAltPartnerFactor.getPercent());
	if (towardUs() >= ATTITUDE_PLEASED &&
		kWe.AI_atVictoryStage(AI_VICTORY_DIPLOMACY4 | AI_VICTORY_DIPLOMACY3))
	{
		scaled rVictoryFactor(kThey.getTotalPopulation(),
				std::max(1, m_kGame.getTotalPopulation()));
		scaled rVictoryCost = 25 * rVictoryFactor * rPenalties;
		log("-%d for jeopardizing diplo victory", rVictoryCost.round());
		m_rCost += rVictoryCost;
	}
}


Affection::Affection(WarEvalParameters const& kParams) : WarUtilityAspect(kParams)
{
	m_rGameProgressFactor = 1 - fixp(0.2) * m_kGame.gameTurnProgress();
}


void Affection::evaluate()
{
	// Humans are unaffectionate
	if (kWe.isHuman() ||
		// No qualms about attacking capitulated vassals
		kOurTeam.isCapitulated() || kTheirTeam.isCapitulated() ||
		!militAnalyst().isWar(eWe, eThey) || kOurTeam.AI_getWorstEnemy() == eTheirTeam)
	{
		return;
	}
	scaled rWarImminentMult = 1;
	WarPlanTypes const eWP = kOurTeam.AI_getWarPlan(eTheirTeam);
	/*	Once we've adopted a direct warplan, affection is greatly reduced -- a civ
		that'll only please us when it sees our soldiers approach isn't a true friend. */
	if (eWP != WARPLAN_PREPARING_LIMITED && eWP != WARPLAN_PREPARING_TOTAL &&
		eWP != NO_WARPLAN)
	{
		rWarImminentMult = scaled::min(1,
				fixp(0.085) * scaled::max(1,
				/*	If war stays imminent for a long time, and relations remain good,
					affection should matter again. Adjust a bit for game progress b/c
					turns feel longer in the late game. (This runs counter to the
					progress adjustment in the end.) If a human player _feels_ that
					relations have been good for quite some time when war is declared,
					then that's a problem.
					Take into account the time spent on preparations? That would reflect the
					sunk cost of the AI and would also tend to be shorter in the late game.
					But that duration isn't currently kept track of by CvTeamAI ... */
				kOurTeam.AI_getWarPlanStateCounter(eTheirTeam)
				- 4 * (fixp(2.5) * m_rGameProgressFactor - fixp(1.5))));
	}
	// We're not fully responsible for wars triggered by our DoW
	scaled rLinkedWarMult;
	if (militAnalyst().getWarsDeclaredBy(eWe).count(eThey) > 0)
	{
		if (kTheirTeam.isAVassal()) // non-capitulated
			rLinkedWarMult = fixp(0.25);
		else rLinkedWarMult = 1;
	}
	/*	We're also somewhat responsible for wars declared on us through
		defensive pacts (DP). No need to check for current DP b/c a DP is
		the only way that a DoW on us can happen in the military analysis
		(all other DoW on us are unforeseen). */
	if (militAnalyst().getWarsDeclaredBy(eThey).count(eWe) > 0)
		rLinkedWarMult = fixp(0.4);
	if (rLinkedWarMult <= 0)
		return;
	int iNoWarPercent = kOurTeam.AI_noWarProbAdjusted(eTheirTeam);
	scaled rUtility; // (Positive value; gets subtracted in the end.)
	if (iNoWarPercent > 0) // for efficiency
	{
		/*	Capitulated vassals don't interest us, but a voluntary vassal can
			reduce our affection for its master. The Affection aspect also gets
			evaluated with eThey set to the vassal, but that only accounts for
			our scruples about attacking the vassal.
			There's already a diplo penalty for having an unpopular vassal,
			so I'm only applying a minor penalty here. */
		scaled rVassalPenalty;
		for (PlayerIter<MAJOR_CIV,VASSAL_OF> itTheirVassal(eTheirTeam);
			itTheirVassal.hasNext(); ++itTheirVassal)
		{
			PlayerTypes const eTheirVassal = itTheirVassal->getID();
			if (GET_TEAM(eTheirVassal).isCapitulated())
				continue;
			int iVassalNoWarPercent = kOurPersonality.getNoWarAttitudeProb(
					kWe.AI_getAttitude(eTheirVassal));
			int iDelta = iNoWarPercent - iVassalNoWarPercent;
			if (iDelta > 0)
				rVassalPenalty += scaled(iDelta, 10);
		}
		int const iVassalPenalty = rVassalPenalty.uround();
		if (iVassalPenalty > 0)
		{
			iNoWarPercent = std::max(iNoWarPercent / 2, iNoWarPercent - iVassalPenalty);
			log("No-war-chance for %s reduced by %d b/c of peace vassals",
					m_kReport.leaderName(eThey), iVassalPenalty);
		}
		//rUtility = per100(iNoWarPercent).pow(fixp(5.5)) * 75;
		// ^That progression is a bit too steep
		// The new formula would go toward infinity for high iNoWarPercent
		int const iNoWarPercentCapped = std::min(iNoWarPercent, 94);
		/*	Subtract 1 so that iNoWarPercent=0 yields 0. The exponent and
			dividend (1) are magic constants. */
		rUtility += 1 / (1 - per100(iNoWarPercentCapped).pow(fixp(0.223)));
		rUtility -= 1; // So that iNoWarPercent=0 yields 0
		rUtility += iNoWarPercent - iNoWarPercentCapped;

	}
	if (towardThem() >= ATTITUDE_FRIENDLY)
		rUtility += 34; // 40 prior to AdvCiv 0.97
	bool const bIgnDistr = m_kParams.isIgnoreDistraction();
	/*	The Catherine clause - doesn't make sense for her to consider sponsored
		war on a friend if the cost is always prohibitive. */
	bool const bHiredAgainstFriend = (towardThem() >= ATTITUDE_FRIENDLY &&
			(m_kParams.getSponsor() != NO_PLAYER ||
			/*	The computations ignoring distraction are also used for decisions
				on joint wars (see UWAI::Team::declareWarTrade) */
			bIgnDistr));
	if (bHiredAgainstFriend)
		rUtility = 50;
	rUtility *= rLinkedWarMult * rWarImminentMult * m_rGameProgressFactor;
	// When there's supposed to be uncertainty
	if (!bIgnDistr && ((iNoWarPercent > 0 && iNoWarPercent < 100) || bHiredAgainstFriend))
	{
		vector<int> aiInputs;
		aiInputs.push_back(eThey);
		aiInputs.push_back(towardThem());
		aiInputs.push_back(kWe.AI_getMemoryCount(eThey, MEMORY_DECLARED_WAR));
		aiInputs.push_back(kThey.AI_getMemoryCount(eWe, MEMORY_DECLARED_WAR));
		scaled rHashVal = scaled::hash(aiInputs, eWe);
		scaled const rUncertaintyBound = 12;
		scaled rUncertainVal = rHashVal * std::min(2 * rUncertaintyBound, rUtility) -
				std::min(rUncertaintyBound, fixp(0.5) * rUtility);
		if (rUncertainVal.abs() >= fixp(0.5))
		{
			log("%d %s for uncertainty", rUncertainVal.abs().round(),
					(rUncertainVal > 0 ? "added" : "subtracted"));
		}
		rUtility += rUncertainVal;
		FAssert(rUtility >= 0);
	}
	/*	In team games, the pairwise affection adds up more than the
		pairwise conquests; need to correct that a bit. */
	if (kOurTeam.getNumMembers() > 1)
		rUtility = normalizeUtility(rUtility) * kOurTeam.getNumMembers() * fixp(2/3.);
	if (rUtility >= fixp(0.5))
	{
		log("NoWarAttProb: %d percent, our attitude: %d, for linked war: %d percent,"
				" for direct war plan: %d percent, for game turn: %d percent",
				iNoWarPercent, towardThem(), rLinkedWarMult.getPercent(),
				rWarImminentMult.getPercent(), m_rGameProgressFactor.getPercent());
		m_iU -= rUtility.round();
	}
}


void Distraction::evaluate()
{
	if (kOurTeam.isAVassal() || kTheirTeam.isAVassal() ||
		!militAnalyst().isWar(eWe, eThey))
	{
		return;
	}
	if (!kWeAI.canReach(eThey) && !kThey.uwai().canReach(eWe))
	{
		log("No distraction from %s b/c neither side can reach the other",
				m_kReport.leaderName(eThey));
		return;
	}
	FAssert(!m_kParams.isIgnoreDistraction());
	int const iWarDuration = kOurTeam.AI_getAtWarCounter(eTheirTeam);
	// Utility ignoring Distraction cost
	scaled const rWarUtilityVsThem = normalizeUtility(
			ourCache().warUtilityIgnoringDistraction(eTheirTeam));
	scaled rDistractionCost;
	int iAltWars = 0;
	scaled rTotalOpportunityCost;
	scaled rHighestOpportunityCost;
	for (TeamIter<FREE_MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> itAltTarget(eOurTeam);
		itAltTarget.hasNext(); ++itAltTarget)
	{
		TeamTypes const eAltTarget = itAltTarget->getID();
		if (eAltTarget == eTheirTeam ||
			kOurTeam.AI_isPushover(eAltTarget) ||
			(!kOurTeam.uwai().canReach(eAltTarget) &&
			!GET_TEAM(eAltTarget).uwai().canReach(eOurTeam)))
		{
			continue;
		}
		scaled rWarUtilityVsAlt = normalizeUtility(
				ourCache().warUtilityIgnoringDistraction(eAltTarget), eAltTarget);
		if (rWarUtilityVsAlt >= 50 && kOurTeam.isAtWar(eTheirTeam))
		{
			log("Distraction unproblematic b/c war utility against %s is high (%d)",
					m_kReport.teamName(eAltTarget), rWarUtilityVsAlt.round());
			continue;
		}
		/*	The war against eThey distracts us from our war against eAltTarget.
			The comparison between war and peace scenario should cover this kind of
			distraction - but doesn't always b/c military analysis can have
			counterintuitive outcomes with greater losses in the peace scenario.
			Needs a little extra nudge. */
		if (kOurTeam.AI_getWarPlan(eAltTarget) != NO_WARPLAN)
		{
			rDistractionCost += fixp(5.5);
			log("War plan against %s distracts us from (actual)"
					" war plan against %s", m_kReport.leaderName(eThey),
					m_kReport.teamName(eAltTarget));
			/*	The cached value is for limited war in 5 turns, which isn't
				necessarily the best war plan against eAltTarget. */
			rWarUtilityVsAlt += fixp(7.5);
			if (rWarUtilityVsAlt >= fixp(0.5) &&
				!militAnalyst().isOnTheirSide(eAltTarget, true) &&
				!kOurTeam.isAtWar(eAltTarget))
			{
			/*	This means, war against eAltTarget is still in preparation or imminent,
				and we're considering peace with eThey; or there's a special offer
				(sponsored or diplo vote) to declare war on eThey. (Not possible:
				preparations against eAltTarget and eThey at the same time.) */
				rDistractionCost += rWarUtilityVsAlt;
				log("%d extra cost for distraction from war in preparation",
						rWarUtilityVsAlt.uround());
			}
			// NB: Imminent war against eAltTarget is covered by UWAI::Team::considerPeace
		}
		/*	eAltTarget as a potential alternative war target. rOurWarUtility is the
			utility of fighting both eThey and eAltTarget. Won't be able to tell
			how worthwhile war against eAltTarget really is until we make peace
			with eThey. Assume that we wouldn't have started a war against eThey
			if eAltTarget was the better target. But the longer the war against
			eThey lasts, the likelier a change in circumstances becomes. */
		else if (kOurTeam.isAtWar(eTheirTeam) &&
			// If eAltTarget==getTarget, then eAltTarget isn't an "alternative".
			m_kParams.getTarget() != eAltTarget &&
			/*	If there's a peace treaty, then we probably
				don't want to attack them urgently. */
			kOurTeam.canDeclareWar(eAltTarget) &&
			rWarUtilityVsAlt > -iWarDuration)
		{
			scaled rOpportunityCost = iWarDuration +
					rWarUtilityVsAlt - scaled::max(0, rWarUtilityVsThem);
			rOpportunityCost /= fixp(1.55);
			if (rOpportunityCost >= fixp(0.5))
			{
				rOpportunityCost.decreaseTo(15);
				log("War against %s (%d turns) distracts us from potential war plan "
						"against %s. Current utilities: %d/%d; Distraction cost: %d",
						m_kReport.leaderName(eThey), iWarDuration,
						m_kReport.teamName(eAltTarget), rWarUtilityVsThem.round(),
						rWarUtilityVsAlt.round(), rOpportunityCost.uround());
				rHighestOpportunityCost.increaseTo(rOpportunityCost);
				rTotalOpportunityCost += rOpportunityCost;
				iAltWars++;
			}
		}
	}
	if (iAltWars > 0)
	{
		/*	We're going start at most one of the potential wars, but having
			several candidates should be an extra incentive for freeing our hands. */
		scaled rOverallOpportunityCost = rHighestOpportunityCost +
				(rTotalOpportunityCost - rHighestOpportunityCost) /
				scaled(iAltWars).sqrt();
		if (rOverallOpportunityCost >= fixp(0.5))
		{
			log("Adjusted cost for all (%d) potential wars: %d", iAltWars,
					rOverallOpportunityCost.uround());
			rDistractionCost += rOverallOpportunityCost;
		}
	}
	/*	If we expect to knock them out, the current war may be over before the
		time horizon of the simulation; then it's a smaller distraction.
		(InvasionGraph could store elimination timestamps, but that seems too much
		work to implement. Can guess the time well enough here by counting their
		remaining cities.) */
	if (rDistractionCost > 0 &&
		(militAnalyst().isEliminated(eThey) ||
		militAnalyst().getCapitulationsAccepted(eOurTeam).count(eTheirTeam) > 0))
	{
		scaled rAlmostDoneMult(kThey.getNumCities(), 3);
		if (rAlmostDoneMult < 1)
		{
			log("Distraction cost reduced to %d percent b/c we're almost done with %s",
					rAlmostDoneMult.getPercent(), m_kReport.leaderName(eThey));
			rDistractionCost *= rAlmostDoneMult;
		}
	}
	m_iU -= rDistractionCost.round();
}


void PublicOpposition::evaluate()
{
	if (kWe.isAnarchy() || !militAnalyst().isWar(eWe, eThey) ||
		militAnalyst().isEliminated(eWe))
	{
		return;
	}
	int iTotalPop = kWe.getTotalPopulation();
	if (iTotalPop <= 0)
		return;
	scaled rFaithAnger;
	FOR_EACH_CITY(pCity, kWe)
	{
		if (pCity->isDisorder())
			continue;
		scaled rAngry = pCity->angryPopulation(0,
				!kWe.AI_atVictoryStage(AI_VICTORY_CULTURE3));
		rFaithAnger += std::min(rAngry,
				pCity->getReligionPercentAnger(eThey) * pCity->getPopulation() /
				GC.getPERCENT_ANGER_DIVISOR());
	}
	// Known issue: This is 0 if not currently at war with them
	scaled rWWAnger = ourCache().angerFromWarWeariness(eThey);
	if (rWWAnger + rFaithAnger <= 0)
		return;
	log("Angry citizens from religion: %d, from ww: %d; total citizens: %d",
			rFaithAnger.uround(), rWWAnger.uround(), iTotalPop);
	// Assume that more WW is coming, and especially if we take the fight to them.
	WarPlanTypes const eWarPlan = kOurTeam.AI_getWarPlan(eTheirTeam);
	bool bTotal = (eWarPlan == WARPLAN_PREPARING_TOTAL || eWarPlan == WARPLAN_TOTAL);
	if (m_kParams.getTarget() == eTheirTeam && m_kParams.isTotal())
		bTotal = true;
	scaled rExtraAngerPortion = (bTotal ? fixp(0.5) : fixp(0.35));
	rExtraAngerPortion += (fixp(1.5) * ourConquestsFromThem().size()) /
			std::max(kWe.getNumCities(), 1);
	if (rWWAnger > 0)
	{
		log("Expected increase in WW: %d percent (%d conquered cities, %s war)",
				rExtraAngerPortion.getPercent(), (int)ourConquestsFromThem().size(),
				(bTotal ? "total" : "limited"));
	}
	scaled const rAngerRate = (rWWAnger * (1 + rExtraAngerPortion) + rFaithAnger) /
			iTotalPop;
	if (rAngerRate <= 0)
		return;
	scaled rAngerCost = 125 * rAngerRate;
	// Don't go too high
	rAngerCost.exponentiate(fixp(0.75));
	rAngerCost *= 2; // (normalization factor)
	/*	Shouldn't be much of a deterrent when playing for military victory.
		(Letting the utility counted for the MilitaryVictory aspect cancel out
		the PublicOpposition isn't quite working out, I think, b/c the
		latter aspect is being overvalued so that it can serve as a safeguard
		against interminable wars.) */
	if (kWe.AI_atVictoryStage(AI_VICTORY_MILITARY3))
	{
		int const iDiv = (kWe.isHuman() ? 3 : 2); // Humans are especially goal-driven
		rAngerCost /= iDiv;
		if (kWe.AI_atVictoryStage(AI_VICTORY_MILITARY4))
			rAngerCost /= iDiv;
	}
	log("War anger rate: %d percent%s", rAngerRate.getPercent(),
			(rAngerCost <= fixp(0.5) ? " (negligible)" : ""));
	m_iU -= rAngerCost.round();
}


void Revolts::evaluate()
{
	/*	The war against eThey occupies our units while revolts break out
		in the primary areas of eThey */
	if (!militAnalyst().isWar(eWe, eThey) || kOurTeam.AI_isPushover(eTheirTeam))
		return;
	scaled rLossesFromRevolts;
	int iTotalAssets = 0;
	FOR_EACH_AREA(pArea)
	{
		if (!kThey.AI_isPrimaryArea(*pArea))
			continue;
		if (kOurTeam.isAtWar(eTheirTeam)) // Can't rely on AreaAIType otherwise
		{
			AreaAITypes const eAreaAI = pArea->getAreaAIType(eOurTeam);
			// Training defenders is the CityAI's best remedy for revolts
			if (eAreaAI == AREAAI_DEFENSIVE || eAreaAI == AREAAI_NEUTRAL ||
				eAreaAI == NO_AREAAI)
			{
				continue;
			}
		}
		FOR_EACH_CITY(pCity, kWe)
		{
			if (!pCity->isArea(*pArea))
				continue;
			City const* pCacheCity = ourCache().lookupCity(pCity->plotNum());
			// Count each city only once
			if (pCacheCity == NULL || m_countedCities.count(pCity->plotNum()) > 0)
				continue;
			m_countedCities.insert(pCity->plotNum());
			int const iCityAssets = pCacheCity->getAssetScore();
			iTotalAssets += iCityAssets;
			scaled rRevoltProb = pCity->revoltProbability(false, false, true);
			if (rRevoltProb <= 0)
				continue;
			/*	If we've been failing to suppress a city for a long time,
				then it's probably not mainly a matter of distracted units. */
			if (pCity->getNumRevolts() > GC.getDefineINT(CvGlobals::NUM_WARNING_REVOLTS))
			{
				log("%s skipped as hopeless", m_kReport.cityName(*pCity));
				continue;
			}
			scaled rLossMult = 5 * std::min(fixp(0.1), rRevoltProb);
			if (rLossMult > 0)
			{
				log("%s in danger of revolt (%d percent; assets: %d)",
						m_kReport.cityName(*pCity),
						rRevoltProb.getPercent(), iCityAssets);
				rLossesFromRevolts += iCityAssets * rLossMult;
			}
		}
	}
	if (iTotalAssets <= 0)
		return;
	/*	Dilute amortizationMultiplier because revolts make cities less useful
		economically, but can also disrupt victory conditions. */
	scaled rRevoltCost = (1 + kWeAI.amortizationMultiplier()) *
			50 * rLossesFromRevolts / iTotalAssets;
	m_iU -= rRevoltCost.round();
}


void UlteriorMotives::evaluate()
{
	if (kWe.isHuman())
		return;
	/*	Difference between ourCache().sponsorAgainst(t) and
		m_kParams.getSponsor() returning t:
		The former tells us that our war against t has been sponsored; so, we've
		already agreed to the war trade. The latter says that we're currently
		considering war against t. This aspect needs to apply when considering the
		offer. Once we've declared war, we should forget about our issues with the
		sponsor's motives, and instead live up to our promise (as enforced by
		HiredHand). */
	if (militAnalyst().isPeaceScenario() || eThey != m_kParams.getSponsor() ||
		!kWe.hasCapital() || !kThey.hasCapital())
	{
		return;
	}
	if (kOurTeam.AI_getWarPlan(eTheirTeam) != NO_WARPLAN)
	{
		/*	They're probably trying to deflect our attack. That doesn't have to
			be bad for us; Distraction cost accounts for the difference in
			war utility vs. sponsor and target. But if they're willing to pay us off,
			we should ask for sth. extra. And don't want to make it too easy
			for humans to avoid wars. */
		FAssert(!m_kParams.isIgnoreDistraction()); // Sponsor should be NO_PLAYER then
		int iUtilityVsThem = ourCache().warUtilityIgnoringDistraction(eTheirTeam);
		m_iU -= std::max(5, iUtilityVsThem / 2);
		return;
	}
	TeamTypes const eTarget = m_kParams.getTarget();
	CvTeamAI const& kTarget = GET_TEAM(eTarget);
	bool const bJointWar = militAnalyst().isWar(eTheirTeam, eTarget);
	// If they're in a hot war, their motives seem clear (and honest) enough.
	bool const bHot = (bJointWar && kTarget.AI_getWarSuccess(eTheirTeam) +
			2 * kTheirTeam.AI_getWarSuccess(eTarget) >
			3 * GC.getWAR_SUCCESS_CITY_CAPTURING() &&
			kTarget.uwai().canReach(eTheirTeam)); // Perhaps no longer hot
	if (bHot &&
		// If the target is in our area but not theirs, that's fishy.
		(!kTarget.AI_isPrimaryArea(kWe.getCapital()->getArea()) ||
		kTarget.AI_isPrimaryArea(kThey.getCapital()->getArea())))
	{
		return;
	}
	/*	Otherwise, they might want to hurt us as much as the target, and we should
		demand extra payment to allay our suspicions. Use DWRAT (greater than
		Annoyed, Cautious or Pleased respectively) as an indicator of how
		suspicious we are. */
	int iSuspicionFactor = kOurPersonality.getDeclareWarRefuseAttitudeThreshold()
			- towardThem() + 1;
	if (towardThem() == ATTITUDE_FRIENDLY)
		iSuspicionFactor--;
	int iMotivesCost = 8 + 4 * iSuspicionFactor;
	if (!bJointWar)
		iMotivesCost += 4;
	/*	An AI sponsor can, in principle, have ulterior motives. For example,
		if they expect the war to hurt us, this could result in positive utility
		from Kingmaking for them. This is a bit farfetched though, so ... */
	if (!bHot && !kThey.isHuman())
		iMotivesCost /= 2;
	if (iMotivesCost > 0)
	{
		log("Attitude level towards %s: %d, refusal thresh: %d",
				m_kReport.leaderName(eThey), towardThem());
		m_iU -= iMotivesCost;
	}
}


void FairPlay::evaluate()
{
	if (kWe.isHuman() || // Don't expect humans to pull punches
		kTheirTeam.isAVassal() ||
		militAnalyst().getWarsDeclaredBy(eWe).count(eThey) <= 0 ||
		// No kid gloves if they've attacked us recently (or repeatedly)
		kWe.AI_getMemoryAttitude(eThey, MEMORY_DECLARED_WAR) < -2 ||
		kThey.AI_atVictoryStage3() ||
		// Then our attack dooms them regardless of other war parties
		(kOurTeam.AI_isPushover(eTheirTeam) &&
		(!kThey.isHuman() || kThey.getCurrentEra() > 0)) ||
		/*	If they can't win anymore, we shouldn't hold back. Don't want to
			leave all the loot to others. A human with such poor war success
			isn't going to win either, but if the human is a good sport and
			keeps playing, the AI shouldn't punish that. */
		(!kThey.isHuman() && kTheirTeam.AI_getWarSuccessRating() <= -60))
	{
		return;
	}
	// Avoid big dogpiles (or taking turns attacking a single target)
	scaled rOtherEnemies; // Apart from us
	int iPotentialOtherEnemies = 0;
	int const iTheirRank = m_kGame.getPlayerRank(eThey);
	for (PlayerAIIter<FREE_MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> itOther(eOurTeam);
		itOther.hasNext(); ++itOther)
	{
		CvPlayerAI const& kOther = *itOther;
		if (kOther.getID() == eThey || !kTheirTeam.isHasMet(kOther.getTeam()))
			continue;
		iPotentialOtherEnemies++;
		bool const bWar = (kTheirTeam.isAtWar(kOther.getTeam()) ||
				militAnalyst().getWarsDeclaredBy(kOther.getID()).count(eThey) > 0);
		int const iTheirWarMemoryAttitude = kThey.AI_getMemoryAttitude(kOther.getID(),
				MEMORY_DECLARED_WAR);
		if (bWar || iTheirWarMemoryAttitude <= -2)
		{
			scaled rEnemyWeight = fixp(1.15);
			if (!bWar)
			{
				rEnemyWeight *= fixp(0.73);
				if (iTheirWarMemoryAttitude == -2)
					rEnemyWeight *= fixp(0.85);
			}
			int iOtherRank = m_kGame.getPlayerRank(kOther.getID());
			// Ganging up on the leader is less problematic
			if (iTheirRank < iOtherRank)
				rEnemyWeight *= scaled(iTheirRank + 1, iOtherRank + 1);
			rOtherEnemies += rEnemyWeight;
			log("Another enemy of %s: %s; increment: %d percent",
					m_kReport.leaderName(eThey),
					m_kReport.leaderName(kOther.getID()),
					rEnemyWeight.getPercent());
		}
		else if (kTheirTeam.AI_shareWar(kOther.getTeam()))
		{
			log("An ally of %s: %s", m_kReport.leaderName(eThey),
					m_kReport.leaderName(kOther.getID()));
			rOtherEnemies -= scaled(1,
					std::max(1, GET_TEAM(kOther.getTeam()).getNumWars(true, true)));
		}
		if (kOther.AI_getMemoryAttitude(eThey, MEMORY_DECLARED_WAR) <= -2)
		{
			log("They've attacked %s before", m_kReport.leaderName(kOther.getID()));
			rOtherEnemies -= fixp(0.5);
		}
	}
	if (rOtherEnemies > fixp(0.1))
	{
		scaled rFromOtherEnemies = 30 * ((rOtherEnemies + scaled(std::max(0,
				/*	The number of cities we expect them to lose to others.
					The subtracted conquests of ours could include cities of
					other civs, but, in that case, we're apparently busy with
					another enemy and our DoW won't really hurt. */
				((int)militAnalyst().lostCities(eThey).size()) -
				((int)militAnalyst().conqueredCities(eWe).size()))).sqrt()) /
				(scaled(std::max(1, iPotentialOtherEnemies)).sqrt() - fixp(1/3.)));
		rFromOtherEnemies *= (1 - fixp(2/3.) * m_kGame.gameTurnProgress());
		/*	Once we've gone through the trouble of preparing war, we'd like to go
			through with it, but if there are many civs in the game, there's a good
			chance that several of them start plotting at the same time, so
			enforcing fairness only before and during preparations isn't enough. */
		if (kOurTeam.AI_isSneakAttackReady(eTheirTeam))
		{
			scaled rPotentialEnemyMult(iPotentialOtherEnemies, 10);
			rPotentialEnemyMult.clamp(fixp(0.25), fixp(0.75));
			rFromOtherEnemies *= rPotentialEnemyMult;
		}
		if (rFromOtherEnemies >= fixp(0.5))
		{
			log("From other enemies: %d", rFromOtherEnemies.uround());
			m_iU -= rFromOtherEnemies.uround();
		}
	}
	// The rest of this function deals with the early game
	/*	Assume that early AI-on-AI wars are always fair b/c they have the same
		handicap. Not actually true in e.g. the EarthAD1000 scenario. Still,
		early attacks on AI civs aren't a serious problem. */
	if (!kThey.isHuman() ||
		kWe.AI_getMemoryAttitude(eThey, MEMORY_DECLARED_WAR_ON_FRIEND) < 0)
	{
		return;
	}
	/*	Mostly care about Archery, which has power 6. The Wheel isn't unfair
		(power 4). BW and IW have power 8 and 10. */
	/*CvHandicapInfo const& kGameHandicap = GC.getInfo(m_kGame.getHandicapType());
	bool bPowerTechFound = false;
	FOR_EACH_ENUM(Tech)
	{
		if (kGameHandicap.isAIFreeTechs(i) &&
			GC.getInfo(eLoopTech).getPowerValue() >= 5)
		{
			bPowerTechFound = true;
			break;
		}
	}
	if (!bPowerTechFound)
		return;*/
	/*	Actually, never mind checking for starting tech. Don't want early rushes
		on low difficulty either. */
	EraTypes const eStartEra = m_kGame.getStartEra();
	scaled const rTrainMod = per100(m_kSpeed.getTrainPercent()) *
			per100(GC.getInfo(eStartEra).getTrainPercent());
	FAssert(rTrainMod > 0);

	scaled rFairnessCost;
	/*	All bets off by turn 100, but, already by turn 50, the cost may
		no longer be prohibitive. */
	int iTargetTurn = 100 + m_kGame.getStartTurn();
	// Allow earlier aggression on crowded maps
	iTargetTurn = (iTargetTurn * ((1 + fixp(1.5) *
			scaled(m_kGame.getRecommendedPlayers(), m_kGame.getCivPlayersEverAlive())) /
			fixp(2.5))).uround();
	int const iElapsed = (m_kGame.getElapsedGameTurns() / rTrainMod).uround();
	int iTurnsRemaining = iTargetTurn - iElapsed
			- GC.getInfo(eStartEra).getStartPercent();
	if (iTurnsRemaining > 0)
	{
		log("Fair-play turns remaining: %d", iTurnsRemaining);
		rFairnessCost += scaled(iTurnsRemaining, 2).pow(fixp(1.28));
		if (m_eGameEra > eStartEra)
		{
			log("The game era has surpassed the start era");
			rFairnessCost *= fixp(3/4.);
		}
		if (kThey.getCurrentEra() > eStartEra)
		{
			log("Their era has surpassed the start era");
			rFairnessCost *= fixp(3/4.);
		}
		scaled scoreRatio(m_kGame.getPlayerScore(eWe), m_kGame.getPlayerScore(eThey));
		log("Score ratio: %s", scoreRatio.str(100).c_str());
		scoreRatio -= fixp(0.1);
		scoreRatio.clamp(fixp(0.4), fixp(5/3.));
		rFairnessCost *= scoreRatio;
	}
	if (m_rGameEraAIFactor > fixp(1.5)) // Dogpiling remains an issue in the Classical era
		return;
	// Don't dogpile when human has lost cities in the early game
	int const iCitiesTheyFounded = kThey.getPlayerRecord()->getNumCitiesBuilt();
	int const iCitiesTheyHave = kThey.getNumCities();
	scaled rFromCityLoss;
	if (iCitiesTheyFounded > 0 && iCitiesTheyHave < iCitiesTheyFounded)
		rFromCityLoss = 100 * (1 - scaled(iCitiesTheyHave, iCitiesTheyFounded)).pow(fixp(0.85));
	if (rFromCityLoss >= fixp(0.5))
	{
		log("From lost human cities: %d", rFromCityLoss.uround());
		rFairnessCost += rFromCityLoss;
	}
	// If no cities gained nor lost, at least don't DoW in quick succession.
	else if (kThey.getNumCities() == iCitiesTheyFounded)
	{
		int iFromRecentDoW = 35 * kTheirTeam.AI_getNumWarPlans(WARPLAN_ATTACKED_RECENT);
		log("From recent DoW: %d", iFromRecentDoW);
		rFairnessCost += iFromRecentDoW;
	}
	int iAttitudeDiv = 3 - towardThem() +
			kWe.AI_getMemoryAttitude(eThey, MEMORY_REJECTED_DEMAND); // negative
	if (iAttitudeDiv > 1)
	{
		log("Divided by %d because of attitude", iAttitudeDiv);
		rFairnessCost /= iAttitudeDiv;
	}
	m_iU -= std::max(0, rFairnessCost.round());
}

// (no longer used)
/*int FairPlay::initialMilitaryUnits(PlayerTypes ePlayer)
{
	CvPlayer const& kPlayer = GET_PLAYER(ePlayer);
	CvHandicapInfo const& kPlayerHandicap = GC.getInfo(kPlayer.getHandicapType());
	// DefenseUnits aren't all that defensive
	return kPlayerHandicap.getStartingDefenseUnits() +
			(kPlayer.isHuman() ? 0 : kPlayerHandicap.getAIStartingDefenseUnits());
}*/

void Bellicosity::evaluate()
{
	if (kWe.isHuman() || !militAnalyst().isWar(eOurTeam, eTheirTeam) ||
		!kWeAI.canReach(eThey))
	{
		return;
	}
	// One war is enough
	if (kOurTeam.getNumWars() > 0 && !kOurTeam.isAtWar(eTheirTeam))
		return;
	/*	This is what makes units attack against the odds. 6 for Napoleon and Ragnar,
		4 for Alexander, Boudica, Brennus, Genghis, Gilgamesh, Hannibal, Montezuma,
		Peter, Shaka and Sitting Bull. Just the suicidal types I need except
		for Sitting Bull. Subtract peace-weight to exclude him - all the others
		have a peace-weight near 0. */
	int const iBellicosity = kOurPersonality.getBaseAttackOddsChange()
			- kOurPersonality.getBasePeaceWeight();
	if (iBellicosity <= 0)
		return;
	scaled rOurMinusTheirLostPow;
	scaled rCurrentAggrPow;
	for (int i = 0; i < NUM_BRANCHES; i++)
	{
		MilitaryBranchTypes const eBranch = (MilitaryBranchTypes)i;
		// Included in other branches; and we never itch for nuclear war.
		if (eBranch == CAVALRY || eBranch == LOGISTICS || eBranch == NUCLEAR)
			continue;
		scaled const rOurLostPow = militAnalyst().lostPower(eWe, eBranch);
		/*	If they lose much more than we do, chances are that a third party is
			causing this. And don't want a warlike AI to attack a weak civ just
			for sport. */
		rOurMinusTheirLostPow += std::min(fixp(2.35) * rOurLostPow,
				militAnalyst().lostPower(eThey, eBranch)) - fixp(0.75) * rOurLostPow;
		if (eBranch != HOME_GUARD) // Not tracked by cache, and not really relevant here.
			rCurrentAggrPow += ourCache().getPowerValues()[eBranch]->power();
	}
	if (rOurMinusTheirLostPow <= 0 || rCurrentAggrPow < 1)
		return;
	// A good war is one that we win, and that occupies many of our eager warriors.
	scaled rGloryRate = rOurMinusTheirLostPow / rCurrentAggrPow;
	rGloryRate.decreaseTo(1);
	log("Difference in lost power: %d; present aggressive power: %d; bellicosity: %d",
			rOurMinusTheirLostPow.uround(), rCurrentAggrPow.uround(), iBellicosity);
	m_iU += (2 * iBellicosity * rGloryRate).round();
}


void TacticalSituation::evaluate()
{
	if (!militAnalyst().isWar(eWe, eThey))
		return;
	if (kOurTeam.isAtWar(eTheirTeam))
		evalEngagement();
	else evalOperational();
}


void TacticalSituation::evalEngagement()
{
	PROFILE_FUNC();
	/*	Can't move this to UWAICache (to compute it only once at the start of a turn)
		b/c it needs to be up-to-date during the turns of other civs, in particular
		the humans that could propose peace at any point of their turns. */
	int iOurExposed = 0;
	int iTheirExposed = 0;
	int iEntangled = 0;
	int iOurTotal = 0;
	int iOurMissions = 0;
	int const iDamagedHPThresh = 60;
	// How many of our units threaten each plot
	std::map<PlotNumTypes,int> weThreaten;
	CvMap const& kMap = GC.getMap();
	FOR_EACH_GROUPAI(pGroup, kWe)
	{
		CvUnit const* pHeadUnit = pGroup->getHeadUnit();
		if (pHeadUnit == NULL || !pHeadUnit->canDefend())
			continue;
		int iGroupSize = pGroup->getNumUnits();
		iOurTotal += iGroupSize;
		// Assume units in cities to be less engaged
		if (pGroup->getPlot().isCity())
			iGroupSize = intdiv::uround(iGroupSize, 2);
		int iRange = 1;
		CvPlot const& kGroupPlot = pGroup->getPlot();
		PlayerTypes const ePlotOwner = kGroupPlot.getOwner();
		/*	Limit range, not least for performance reasons, to cover combat imminent
			on our current turn or the opponent's next turn. If our group is on a
			friendly route, we can probably attack units two tiles away,
			though we probably won't if our units are damaged. */
		if (pHeadUnit->maxHitPoints() - pHeadUnit->getDamage() >= 80)
		{
			if (kGroupPlot.getArea().isWater())
				iRange++;
			else if (ePlotOwner != NO_PLAYER && kGroupPlot.isRoute() &&
				(ePlotOwner == eWe || kOurTeam.canPeacefullyEnter(TEAMID(ePlotOwner))))
			{
				iRange++;
			}
		}
		/*	(Using CvPlayerAI::AI_getPlotDanger for entanglement
			could result in double counting) */
		for (SquareIter itPlot(kGroupPlot, iRange, false); itPlot.hasNext(); ++itPlot)
		{
			CvPlot const& kPlot = *itPlot;
			if (!kPlot.isVisible(eOurTeam) || !kPlot.sameArea(kGroupPlot) ||
				!kPlot.isUnit() || // shortcut
				// Could do without this if it's too slow
				!pHeadUnit->canMoveInto(kPlot, true, false, false, true,
				/*	We're about to move our units, but their movement points haven't
					been restored yet, so it's important not to check for moves. */
				/*bDangerCheck=*/true))
			{
				continue;
			}
			PlotNumTypes ePlot = kPlot.plotNum();
			std::map<PlotNumTypes,int>::iterator pos = weThreaten.find(ePlot);
			if (pos == weThreaten.end())
				weThreaten.insert(std::make_pair(ePlot, iGroupSize));
			else pos->second += iGroupSize;
		}
		if (!kGroupPlot.isCity()) // ourEvac covers exposed cities
		{
			// For identifying exposed units of ours, AI_getPlotDanger is adequate.
			int iOurDamaged = 0;
			int iDanger = kWe.AI_getPlotDanger(
					kGroupPlot, 1, false, iGroupSize, false, eThey);
			if (iDanger > 0)
			{
				FOR_EACH_UNIT_IN(pGroupUnit, *pGroup)
				{ 
					if (pGroupUnit->maxHitPoints() - pGroupUnit->getDamage() <=
						iDamagedHPThresh)
					{
						iOurDamaged++;
						if (iOurDamaged >= iDanger)
							break;
					}
				}
			}
			// Damaged units protected by healthy units aren't exposed
			iOurDamaged = ::range(iDanger + iOurDamaged - iGroupSize, 0, iOurDamaged);
			iOurExposed += iOurDamaged;
		}
		if (!kWe.isHuman())
		{
			// Akin to CvPlayerAI::AI_enemyTargetMissions
			MissionAITypes const eMission = pGroup->AI_getMissionAIType();
			CvPlot const* pMissionPlot = pGroup->AI_getMissionAIPlot();
			bool const bPillage = (eMission == MISSIONAI_PILLAGE && ePlotOwner == eThey);
			if (bPillage ||
				// (K-Mod uses MISSIONAI_ASSAULT also for land-based assaults on cities)
				((eMission == MISSIONAI_ASSAULT || eMission == MISSIONAI_GROUP ||
				eMission == MISSIONAI_REINFORCE) &&
				pMissionPlot != NULL && pMissionPlot->getOwner() == eThey &&
				// Don't count besiegers
				(!pMissionPlot->isCity() || stepDistance(&kGroupPlot, pMissionPlot) > 1)))
			{
				int iMissionScore = pGroup->getNumUnits() + pGroup->getCargo();
				if (bPillage)
					iMissionScore = intdiv::uround(iMissionScore, 2);
				iOurMissions += iMissionScore;
			}
		}
	}
	if (iOurMissions > 0 && kOurTeam.AI_isPushover(eTheirTeam))
	{
		/*	If the target is weak, even a small fraction of our military en route
			could have a big impact once it arrives. */
		iOurMissions *= 3;
		iOurMissions /= 2;
		log("Mission count increased b/c target is short work");
	}
	/*	So long as we check canMoveInto with bAttack=true above, this here
		probably won't save time. */
	/*FOR_EACH_GROUPAI(pGroup, kWe)
	{
		CvUnit const* pHeadUnit = pGroup->getHeadUnit();
		if (pHeadUnit == NULL || !pHeadUnit->canDefend())
			continue;
		weThreaten.erase(kMap.plotNum(pGroup->getPlot()));
	}*/
	scaled rEraMult = 1 - fixp(0.2) *
			(kThey.AI_getCurrEraFactor() - kWe.AI_getCurrEraFactor());
	rEraMult.clamp(fixp(0.4), fixp(1.6));
	{	PROFILE("TacticalSituation::evalEngagement - weThreaten");
	for (std::map<PlotNumTypes,int>::const_iterator it = weThreaten.begin();
		it != weThreaten.end(); ++it)
	{
		CvPlot const& kPlot = kMap.getPlotByIndex(it->first);
		int iOurUnits = it->second;
		int iTheirUnits = 0;
		int iTheirDamaged = 0;
		// Some overlap with CvPlayerAI::AI_countDangerousUnits
		FOR_EACH_UNIT_IN(pPlotUnit, kPlot)
		{
			if (pPlotUnit->getCombatOwner(eOurTeam) != eThey)
				continue;
			iTheirUnits++;
			if (pPlotUnit->currHitPoints() <= iDamagedHPThresh)
				iTheirDamaged++;
			/*if (iTheirUnits - iTheirDamaged >= iOurUnits)
				break;*/ // Need the full count of iTheirUnits after all
		}
		// Damaged units protected by healthy units aren't exposed
		iTheirDamaged = ::range(iOurUnits + iTheirDamaged - iTheirUnits,
				0, iTheirDamaged);
		/*	If their healthy units outnumber or outclass ours,
			then we probably won't want to engage. */
		if (iTheirUnits > iTheirDamaged)
		{
			iOurUnits = (iOurUnits * scaled::min(1,
					(fixp(1.3) * iOurUnits * rEraMult) /
					(iTheirUnits - iTheirDamaged))).round();
		}
		/*	Count at most one enemy unit per unit of ours as "entangled",
			i.e. count pairs of units. */
		iTheirUnits = std::min(iTheirUnits, iOurUnits);
		if (kPlot.isCity())
		{
			iTheirUnits = intdiv::uround(iTheirUnits, 2);
			iTheirDamaged = 0; // Covered by theirEvac
		}
		iEntangled += iTheirUnits;
		iTheirExposed += iTheirDamaged;
	}
	} // (end of profile scope)
	int const iOurEvac = evacPop(eWe, eThey);
	int const iTheirEvac = evacPop(eThey, eWe);
	/*	If a human is involved or if it's our turn, then we shouldn't worry too
		much about our units being exposed - humans may well have already made
		all attacks against vulnerable units before contacting us. If it's our turn,
		it's still the beginning of the turn, so we can probably save our units. */
	scaled rInitiativeMult = fixp(0.25); // Low if they have the initiative
	if (kWe.isHuman() || kThey.isHuman())
		rInitiativeMult *= 2;
	scaled rUtility = (4 * (rInitiativeMult * iTheirExposed -
			(1 - rInitiativeMult) * iOurExposed) + iOurMissions) /
			std::max(iOurTotal, 1);
	// getNumUnits is an information cheat, but it's all quite fuzzy anyway.
	rUtility += (2 * iEntangled) / std::max(1, iOurTotal + kThey.getNumUnits());
	if (kWe.getTotalPopulation() > 0)
		rUtility += 3 * (iTheirEvac - fixp(1.35) * iOurEvac) / kWe.getTotalPopulation();
	rUtility *= 100;
	int iRecentlyLostPop = 0;
	/*	A mod could add requirements for building roads, but it seems fair to assume
		that roads will be available by the time that roads become faster. */
	bool const bFastRoads = (GET_TEAM(eOurTeam).getRouteChange((RouteTypes)0) <= -10);
	FOR_EACH_CITY(pCity, kThey)
	{
		int iRange = 2;
		if (bFastRoads)
			iRange++;
		if (pCity->isOccupation() && pCity->isEverOwned(eWe) &&
			/*	Just want to know if we have some presence beyond a single
				stray unit near the city */
			kThey.AI_getPlotDanger(pCity->getPlot(), iRange, false, 2, false) > 1)
		{
			iRecentlyLostPop += pCity->getPopulation();
		}
	}
	scaled rRecentlyLostPopPortion;
	if (kWe.getTotalPopulation() > 0)
	{
		rRecentlyLostPopPortion = scaled(
				2 * iRecentlyLostPop,
				kWe.getTotalPopulation() + kThey.getTotalPopulation());
	}
	rUtility += rRecentlyLostPopPortion * 100;
	if (rUtility.abs() >= fixp(0.5))
	{
		log("Their exposed units: %d, ours: %d; entanglement: %d; "
				"their evacuating population: %d, ours: %d; our missions: %d; "
				"our total milit. units: %d; our population: %d; "
				"recently lost population: %d (%d percent)",
				iTheirExposed, iOurExposed, iEntangled, iTheirEvac,
				iOurEvac, iOurMissions, iOurTotal, kWe.getTotalPopulation(),
				iRecentlyLostPop, rRecentlyLostPopPortion.getPercent());
		m_iU += rUtility.round();
	}
}


int TacticalSituation::evacPop(PlayerTypes eOwner, PlayerTypes eInvader) const
{
	int iPop = 0;
	CvPlayerAI const& kOwner = GET_PLAYER(eOwner);
	FOR_EACH_CITYAI(pCity, kOwner)
	{
		/*	Check PlotDanger b/c we don't want to count cities that are threatened
			by a third party */
		if (pCity->AI_isEvacuating() && kOwner.AI_getPlotDanger(
			pCity->getPlot(), 1, false, 2, false, eInvader) >= 2)
		{
			iPop += pCity->getPopulation();
		}
	}
	return iPop;
}


void TacticalSituation::evalOperational()
{

	/*	Evaluate our readiness only for the target that we want to invade
		(not its vassals or allies from def. pact) */
	if (m_kParams.getTarget() != eTheirTeam)
		return;
	/*	When taking the human pov, we mustn't assume to know their exact unit counts.
		Whether they're ready for an attack is secret info. */
	if (kWe.isHuman())
		return;
	if (ourCache().numReachableCities(eThey) <= 0 ||
		(m_kParams.isNaval() &&
		// Won't need invaders then
		ourCache().getPowerValues()[LOGISTICS]->getTypicalUnit() == NO_UNIT))
	{
		return;
	}
	// Similar to CvUnitAI::AI_stackOfDoomExtra
	scaled rTargetAttackers = 4;
	scaled rTheyEra = kThey.AI_getCurrEraFactor();
	if (rTheyEra > 0)
		rTargetAttackers += rTheyEra.pow(fixp(1.3));
	if (m_kParams.isNaval())
		rTargetAttackers *= fixp(1.3);
	// Smaller target on lower difficulty
	{
		scaled rTrainMod = per100(GC.getInfo(m_kGame.getHandicapType()).
				getAITrainPercent());
		rTrainMod.clamp(1, fixp(1.5));
		rTargetAttackers /= rTrainMod;
	}
	/*	Don't necessarily need a larger initial stack for total war.
		A little maybe ... */
	if (m_kParams.isTotal())
		rTargetAttackers++;
	// Need larger stacks when not all our army units can destroy defenders
	bool const bCanBombard = ourCache().getPowerValues()[ARMY]->canBombard();
	if (bCanBombard)
		rTargetAttackers *= fixp(1.25);
	/*	To account for the AI's inability to put all available attackers in one spot,
		and misc. distractions like barbarians */
	rTargetAttackers += scaled::max(0, fixp(0.75) * kWe.getNumCities() - 2);
	scaled rTargetCargo;
	scaled rCargo;
	scaled rTargetEscort;
	// Minor issue: counts Galleons (even when we could be up against Frigates)
	int iEscort = kWe.AI_totalUnitAIs(UNITAI_ATTACK_SEA) +
			kWe.AI_totalUnitAIs(UNITAI_ESCORT_SEA) +
			kWe.AI_totalUnitAIs(UNITAI_RESERVE_SEA);
	if (m_kParams.isNaval())
	{
		rTargetCargo = rTargetAttackers;
		rCargo = ourCache().getPowerValues()[LOGISTICS]->power();
		/*	If we have 0 escorters, we probably can't build them; probably have
			Galleys then but no Triremes. That's OK.
			Also no need for escort if they're way behind in tech. */
		if (iEscort > 0 && kThey.getCurrentEra() >= kWe.getCurrentEra())
		{
			/*	More escort units would be nice, but I'm checking only
				bare necessities. */
			rTargetEscort = rTargetCargo / 6;
		}
	}
	/*	NB: Sea and air units have their own UNITAI types;
		this counts only land units. */
	int const iAttackers = std::max(0,
			kWe.AI_totalUnitAIs(UNITAI_ATTACK) +
			kWe.AI_totalUnitAIs(UNITAI_ATTACK_CITY) +
			kWe.AI_totalUnitAIs(UNITAI_RESERVE) +
			kWe.AI_totalUnitAIs(UNITAI_PILLAGE) +
			kWe.AI_totalUnitAIs(UNITAI_PARADROP) +
			kWe.AI_totalUnitAIs(UNITAI_COLLATERAL)
			/*	Settlers will occupy potential attackers as escorts.
				NB: The AI scraps Settlers eventually if it can't use them;
				can't block war plans permanently. */
			- 2 * kWe.AI_totalUnitAIs(UNITAI_SETTLE));
	/*	(Can't check if we have enough Siege units b/c their UNITAI types overlap
		with non-Siege attackers.) */
	scaled rReadiness = iAttackers / rTargetAttackers;
	if (rTargetCargo > 0)
		rReadiness.decreaseTo(rCargo / rTargetCargo);
	if (rTargetEscort > 0)
	{	// Escort not totally crucial
		rReadiness.decreaseTo((rReadiness + iEscort / rTargetEscort) / 2);
	}
	if (rReadiness >= 1)
		return;
	int const iRemainingTime = m_kParams.getPreparationTime();
	FAssert(iRemainingTime >= 0);
	int iInitialPrepTime = 0;
	if (!m_kParams.isImmediateDoW())
	{	// Overlaps with WarEvaluator::defaultPreparationTime
		if (m_kParams.isTotal())
		{
			if (m_kParams.isNaval())
				iInitialPrepTime = getUWAI().preparationTimeTotalNaval();
			else iInitialPrepTime = getUWAI().preparationTimeTotal();
		}
		else
		{
			if (m_kParams.isNaval())
				iInitialPrepTime = getUWAI().preparationTimeLimitedNaval();
			else iInitialPrepTime = getUWAI().preparationTimeLimited();
		}
	}
	FAssert(iInitialPrepTime >= 0);
	/*	Cost for lack of preparation is based on the assumption
		that it won't hurt much to prolong preparations a bit.
		Not true for immediate DoW. Treat this case as if half the prep time still
		remained (although actually there isn't and never was time to prepare). */
	scaled rPassedPortion = fixp(0.5);
	if (iInitialPrepTime > 0)
		rPassedPortion = 1 - scaled::min(1, scaled(iRemainingTime, iInitialPrepTime));
	if (rPassedPortion <= 0)
		return;
	if (bCanBombard)
		log("Extra attackers needed for mixed siege/attack stacks");
	log("Readiness %d percent (%d of %d attackers, %d of %d cargo, "
			"%d of %d escort); %d of %d turns for preparation remain",
			rReadiness.getPercent(), iAttackers, rTargetAttackers.round(),
			rCargo.uround(), rTargetCargo.uround(), iEscort, rTargetEscort.uround(),
			iRemainingTime, iInitialPrepTime);
	int iUnreadinessCost = (100 * rPassedPortion.pow(fixp(1.5)) *
			(1 - rReadiness.pow(fixp(3.7)))).uround();
	if (iUnreadinessCost == 0)
	{
		log("Cost for lack of readiness vs. %s negligible",
				m_kReport.leaderName(eThey));
	}
	m_iU -= iUnreadinessCost;
}


void LoveOfPeace::evaluate()
{
	int iLoPCost = kOurPersonality.getLoveOfPeace();
	if (iLoPCost <= 0 || !militAnalyst().isWar(eWe, eThey) || kWe.isHuman())
		return;
	if (kOurTeam.isAtWar(eTheirTeam))
	{
		if (militAnalyst().lostPower(eWe, ARMY) < 5 ||
			// Lost power alone isn't reliable; could be to a third party.
			(ourCache().numReachableCities(eThey) <= 0 &&
			kThey.uwai().getCache().numReachableCities(eWe) <= 0))
		{
			return;
		}
		iLoPCost /= 2;
	}
	m_iU -= iLoPCost;
}


int ThirdPartyIntervention::preEvaluate()
{
	scaled rOurLostPow = militAnalyst().lostPower(eWe, ARMY) +
			militAnalyst().lostPower(eWe, HOME_GUARD) +
			/*	Squared b/c logistics power is only the cargo capacity.
				(Fixme: should track power of cargo ships separately.) */
			SQR(militAnalyst().lostPower(eWe, LOGISTICS));
	scaled const rGainedPow = militAnalyst().gainedPower(eWe, ARMY) +
			militAnalyst().gainedPower(eWe, HOME_GUARD);
	m_rDefPow = ourCache().getPowerValues()[ARMY]->power(); // includes HOME_GUARD
	for (PlayerAIIter<MAJOR_CIV,OTHER_KNOWN_TO> itAlly(eOurTeam);
		itAlly.hasNext(); ++itAlly)
	{
		if(militAnalyst().isEliminated(itAlly->getID()))
			continue;
		if (itAlly->getMasterTeam() == kOurTeam.getMasterTeam() ||
			(kOurTeam.isDefensivePact(itAlly->getTeam()) &&
			// This distinction should make us reluctant to kill our DPs
			militAnalyst().getWarsDeclaredBy(eWe).empty()))
		{
			m_rDefPow += itAlly->uwai().getCache().
					getPowerValues()[ARMY]->power() / 2;
			// Let's not bother with their guard units, but count army fully.
			rOurLostPow += militAnalyst().lostPower(itAlly->getID(), ARMY);
		}
	}
	m_rLostDefPowRatio = rOurLostPow / std::max(m_rDefPow,
			m_rDefPow + rGainedPow);
	m_rLostDefPowRatio.clamp(0, fixp(0.5));
	/*	The timing of the intervention is difficult to predict. They may or may not
		need to build up units, and we may be weakest early in the simulation or
		late, but, even in the latter case, they might attack early b/c we already
		appear weak enough ... Too complicated to estimate their build-up, but it'll
		probably be less than ours because we'll start right away and won't stop
		until the war ends. So let's count our estimated change in power half
		and theirs not at all - and later adjust our power to account for
		m_rLostDefPowRatio (losses, distraction). */
	m_rDefPow.increaseTo(m_rDefPow + rGainedPow / 2);
	return 0;
}


void ThirdPartyIntervention::evaluate()
{
	/*	For setting a debugger breakpoint, may want to use this condition:
		m_kAgentTeam.m_eID == x && m_kParams.m_eTarget == y && m_pRivalPlayer->m_eID == z
	*/
	// Mustn't modify those members here
	scaled rOurPow = m_rDefPow;
	scaled rOurLostPowRatio = m_rLostDefPowRatio;
	TeamTypes const eTarget = m_kParams.getTarget();
	/*	Count this cost only when we're actually incurring losses from fighting
		against a 2nd party. Otherwise, we'd veer into the lane of the
		PreEmptiveWar aspect. If we're not incurring losses, then we're doing
		all that we can to avoid exposing us to the 3rd party (eThey). Active
		preparations for an anticipated DoW are handled by the Alert AI strategy. */
	if (rOurLostPowRatio <= 0 ||
		// War against them is already covered by the military analysis
		militAnalyst().isOnTheirSide(eTheirTeam, true) ||
		/*	They're busy fighting someone else. Need to be careful not to use a
			narrow check here - like them conquering cities - b/c that could
			indirectly encourage us to support their war effort. */
		militAnalyst().lostPower(eThey, ARMY) >= 1 ||
		/*	When already at war and winning decisively, try to wrap it up
			before worrying about 3rd parties. */
		(m_kParams.isConsideringPeace() && eTarget != NO_TEAM &&
		(militAnalyst().isEliminated(GET_TEAM(eTarget).getLeaderID()) ||
		!militAnalyst().getCapitulationsAccepted(eOurTeam).empty())) ||
		// Vassals are covered when evaluating their master
		!kTheirTeam.uwai().canSchemeAgainst(eOurTeam, true) ||
		!kTheirTeam.uwai().isLandTarget(eOurTeam))
	{
		return;
	}
	{	/*	Our losses should be small if our enemies are weak, but perhaps
			better not to rely on that. Fear of 3rd parties should not stop
			us from waging minor wars. (Well, having our troops away from
			home could actually hurt us a lot, but I'm more worried about
			the AI just sitting there in tonic immobility.) */
		bool bAllPushOver = true;
		for (TeamIter<FREE_MAJOR_CIV,KNOWN_POTENTIAL_ENEMY_OF> itEnemy(eOurTeam);
			itEnemy.hasNext(); ++itEnemy)
		{
			if (militAnalyst().isWar(eOurTeam, itEnemy->getID()) &&
				!kOurTeam.AI_isPushover(itEnemy->getID()))
			{
				bAllPushOver = false;
				break;
			}
		}
		if (bAllPushOver)
		{
			log("Not considering 3rd-party interventions b/c all enemies are weak");
			return;
		}
	}
	// Sending troops abroad is dangerous; will take long to redeploy.
	if (!militAnalyst().isPeaceScenario() && eTarget != NO_TEAM &&
		!kOurTeam.uwai().isLandTarget(eTarget) &&
		!GET_TEAM(eTarget).AI_hasSharedPrimaryArea(eTheirTeam))
	{
		log("Losses treated as higher b/c of overseas deployment");
		rOurLostPowRatio *= 2;
		rOurLostPowRatio.decreaseTo(fixp(0.6));
	}
	scaled rInterventionProb;
	/*	(If we applied different measures in the war/peace scenario, we could
		get inconsistent results, making us feel safer in the war scenario.) */
	if (//militAnalyst().isPeaceScenario() ||
		m_kParams.isConsideringPeace())
	{
		/*	In this case, all relevant wars are already reflected by their
			war utility against us. No worries if that utility is 0.
			Not sure if war utility _including_ Distraction would be better here;
			well, that's not cached and it shouldn't matter much. */
		scaled rUtilityVsUs = kThey.uwai().getCache().
				warUtilityIgnoringDistraction(eOurTeam);
		/*	We're not supposed to know everything that enters their war utility
			calculation. Add some noise. Hashing rank should result in a somewhat
			stable error. */
		scaled rNoise = 30 *
				(scaled::hash(m_kGame.getPlayerRank(eWe), eWe) - fixp(0.5));
		rUtilityVsUs += rNoise;
		if (rUtilityVsUs > 0)
		{
			log("Their war utility: %d (%d from noise)",
					rUtilityVsUs.uround(), rNoise.round());
			rUtilityVsUs.decreaseTo(94);
			rInterventionProb = fixp(0.8) * rUtilityVsUs / 100;
		}
	}
	else
	{	/*	If there are undeclared wars, it's really difficult to say how much
			higher their war utility will be after those DoW. Not worth letting
			the AI cheat more. Better just rely on paranoia. */
		int iOurDefPow = kOurTeam.getDefensivePower();
		iOurDefPow = (iOurDefPow * (1 - rOurLostPowRatio)).uround();
		int iParanoia = kWe.AI_paranoiaRating(eThey, iOurDefPow, false, true);
		iParanoia = std::min(iParanoia, 210);
		rInterventionProb = scaled(iParanoia - 28, 233);
		if (rInterventionProb > 0)
		{
			log("Our paranoia rating: %d", iParanoia);
			if (!kTheirTeam.isHuman() &&
				!m_kGame.isOption(GAMEOPTION_RANDOM_PERSONALITIES))
			{
				scaled rWarRand = kTheirTeam.AI_dogpileWarRand();
				log("Adjusting paranoia based on DogpileWarRand=%d", rWarRand.floor());
				rWarRand.mulDiv(4, 3);
				rWarRand.clamp(25, 200);
				// War rands matter less when war utility is high
				rInterventionProb /= (rWarRand / 100 + 5 * rInterventionProb) /
						(5 * rInterventionProb + 1);
			}
		}
	}
	if (rInterventionProb < per100(1))
		return;
	/*	(Would be nice to do this also when there has been no war, but there
		is no counter for the number of turns that we've been considering
		war against the target or have been afraid of an intervention.) */
	if (kWe.AI_getMemoryCount(eThey, MEMORY_DECLARED_WAR) +
		kThey.AI_getMemoryCount(eWe, MEMORY_DECLARED_WAR) > 0)
	{	// Avoid stalemates: don't be afraid of interventions forever
		int iAtPeaceTurns = kOurTeam.AI_getAtPeaceCounter(eTheirTeam);
		int iThresh = (5 * GC.getDefineINT(CvGlobals::PEACE_TREATY_LENGTH)) / 3 - 1;
		if (iAtPeaceTurns > iThresh)
		{
			scaled rAtPeaceTurns = fixp(1.5) * iAtPeaceTurns /
					(per100(m_kSpeed.getGoldenAgePercent()) + fixp(0.5));
			scaled rMult = std::max(fixp(1/3.), 1 - scaled(iAtPeaceTurns - iThresh, 30));
			log("Taking intervention prob times %d percent b/c peace has lasted %d turns",
					rMult.getPercent(), iAtPeaceTurns);
			rInterventionProb *= rMult;
		}
	}
	if (!kTheirTeam.isHuman() &&
		!m_kGame.isOption(GAMEOPTION_RANDOM_PERSONALITIES))
	{	/*	(DogpileWarRand is already accounted for above;
			is part of the war utility calc.) */
		int iLimitedWarRand = kTheirTeam.AI_limitedWarRand();
		scaled rWarRand(iLimitedWarRand +
				std::min(iLimitedWarRand, kTheirTeam.AI_maxWarRand()), 2);
		log("Adjusting intervention prob based on WarRand=%d", rWarRand.round());
		rWarRand.clamp(25, 200);
		rInterventionProb /= (rWarRand / 100 + 5 * rInterventionProb) /
				(5 * rInterventionProb + 1);
	}
	if (rInterventionProb < per100(1))
		return;
	/*	(Would be nice to anticipate war trades, but the request frequency is the
		same for almost all leaders anyway, and checking attitude thresholds -
		not to mention trade items - gets pretty complicated, especially
		considering that all parties involved could be human.) */
	/*	(Better not to create an incentive for joining the wars of civs
		that we fear. Let the SuckingUp aspect deal with that.) */
	/*if (militAnalyst().isOnOurSide(eTheirTeam))
		rInterventionProb *= fixp(2/3.);*/
	rInterventionProb.decreaseTo(fixp(0.85));
	log("Probability of intervention by %s: %d percent", m_kReport.leaderName(eThey),
			rInterventionProb.getPercent());
	scaled rTheirPow = kThey.uwai().getCache().
			getPowerValues()[ARMY]->power();
	if (kWe.isHuman())
		rTheirPow *= kThey.uwai().confidenceAgainstHuman();
	for (PlayerAIIter<MAJOR_CIV,VASSAL_OF> itTheirVassal(eTheirTeam);
		itTheirVassal.hasNext(); ++itTheirVassal)
	{
		rTheirPow += itTheirVassal->uwai().getCache().
				getPowerValues()[ARMY]->power() / 2;
	}
	rTheirPow.increaseTo(scaled::epsilon());
	// Preserve for later
	scaled const rTheirCurPowToOurs = rTheirPow / rOurPow;
	{
		// (Ignore their losses in home guard; we know that they haven't lost cities.)
		scaled rTheirLostPowMult = rTheirPow - militAnalyst().lostPower(eThey, ARMY);
		for (PlayerAIIter<MAJOR_CIV,VASSAL_OF> itTheirVassal(eTheirTeam);
			itTheirVassal.hasNext(); ++itTheirVassal)
		{
			rTheirLostPowMult -= militAnalyst().lostPower(
					itTheirVassal->getID(), ARMY) / 2;
		}
		rTheirLostPowMult /= rTheirPow;
		rTheirLostPowMult.increaseTo(fixp(0.6));
		rTheirPow *= rTheirLostPowMult;
	}
	if (kThey.isHuman())
		rOurPow *= kWeAI.confidenceAgainstHuman();
	rOurPow *= 1 - rOurLostPowRatio;
	scaled rTheirPowToOurs = rTheirPow / rOurPow;
	scaled const rPowRatioFloor = fixp(0.5);
	if (rTheirPowToOurs <= rPowRatioFloor)
		return;
	log("Our loss ratio from fighting 2nd parties: %d percent",
			rOurLostPowRatio.getPercent());
	log("Power ratio (they:we) %d:%d=%d percent", rTheirPow.uround(),
			rOurPow.uround(), rTheirPowToOurs.getPercent());
	/*	Proportional to the square of our losses (which are in the unit interval,
		hence sqrt). We want to avoid any tough fights with 2nd parties, when a
		dangerous 3rd-party intervention looms. */
	scaled rCost = rInterventionProb * 85 * rOurLostPowRatio.sqrt();
	{	// These formulas are a bit of a mess
		scaled const rPowRatioThresh = 2;
		if (rTheirPowToOurs > rPowRatioThresh)
		{
			rTheirPowToOurs = rPowRatioThresh +
					(rTheirPowToOurs - rPowRatioThresh + 1).sqrt() - 1;
		}
		else if (rTheirPowToOurs < 1)
			rTheirPowToOurs.exponentiate(fixp(0.5));
		rCost *= rTheirPowToOurs - rPowRatioThresh + 1 + rPowRatioFloor;
		rCost /= 1 + rPowRatioFloor;
		/*	If we can't stand up to them in any case, then we might as well
			expose ourselves and hope for the best. That said, even if we can't
			win, us being able to put up a fight may dissuade them on the
			bottom line. Important only to look at current power values for
			this - to avoid an incentive for incurring greater losses. */
		scaled rThresh = fixp(5/3.);
		if (rTheirCurPowToOurs > rThresh)
		{
			scaled rMult = rThresh / rTheirCurPowToOurs;
			log("Cost reduced by a factor of %d percent b/c 3rd party very powerful",
					rMult.getPercent());
			rCost *= rMult;
		}
	}
	if (kOurTeam.isHuman())
	{	// Humans tend to not worry much about being backstabbed
		rCost *= fixp(2/3.);
	}
	else
	{
		log("Our distrust rating: %d percent", kWeAI.distrustRating().getPercent());
		rCost *= kWeAI.distrustRating().sqrt();
	}
	if (kWe.hasCapital() && kThey.hasCapital() &&
		!kWe.getCapital()->sameArea(*kThey.getCapital()))
	{
		log("Cost decreased for differing capital areas");
		rCost /= 2;
	}
	if (!militAnalyst().getWarsDeclaredBy(eWe).empty() &&
		!kOurTeam.AI_isSneakAttackPreparing())
	{	/*	Not starting war preparations should be less of an inconvenience
			than abandoning preparations or ending an ongoing war. */
		log("Cost increased for our DoW");
		rCost *= fixp(4/3.);
	}
	{
		int iThresh = 35;
		if (rCost > iThresh)
			rCost = iThresh + (rCost - iThresh).sqrt();
	}
	{
		rCost *= 2;
		rCost /= (kOurTeam.getNumMembers() + kTheirTeam.getNumMembers());
	}
	if (rCost < fixp(0.5))
		log("(Not a relevant threat: %s)", m_kReport.leaderName(eThey));
	else m_iU -= rCost.uround();
}


int DramaticArc::preEvaluate()
{
	m_rTensionIncrease = 0;
	if (kOurTeam.isAVassal())
		return 0;
	scaled const rSpeedMult = 2 / per100(m_kGame.getSpeedPercent() +
			m_kSpeed.getTrainPercent());
	int const iElapsedTurns = m_kGame.getElapsedGameTurns();
	if (iElapsedTurns * rSpeedMult < 25) // (Even when starting in a later era)
		return 0;
	int const iOtherKnown = TeamIter<FREE_MAJOR_CIV,OTHER_KNOWN_TO>::count(eOurTeam);
	if (iOtherKnown <= 0)
		return 0;
	int const iMaxPeaceCounter = 100;
	std::vector<int> aiPeaceCounters;
	for (TeamAIIter<FREE_MAJOR_CIV,KNOWN_TO> itFirst(eOurTeam);
		itFirst.hasNext(); ++itFirst)
	{
		int iLoopMinCounter = iElapsedTurns;
		for (TeamIter<MAJOR_CIV,KNOWN_TO> itSecond(eOurTeam);
			itSecond.hasNext(); ++itSecond)
		{
			TeamTypes const eSecond = itSecond->getID();
			if (itFirst->getID() != eSecond)
			{
				int iAtPeace = itFirst->getTurnsAtPeace(eSecond);
				// With tolerance b/c the has-met counter isn't exact
				if (abs(itFirst->AI_getHasMetCounter(eSecond) - iAtPeace) >= 8)
					iLoopMinCounter = std::min(iLoopMinCounter, iAtPeace);
				// (else assume that they've always been at peace)
			}
		}
		aiPeaceCounters.push_back(std::min(iMaxPeaceCounter, iLoopMinCounter));
	}
	int const iMinPeaceCounter = stats::min(aiPeaceCounters);
	scaled rTension;
	if (iMinPeaceCounter > 0) // No wars ongoing
	{
		if (kWe.AI_isDoStrategy(AI_STRATEGY_ALERT1))
			return 0; // We're foreseeing enough tension
		/*	A lack of late-game warfare is not usually a problem,
			and can be due to Cold War dynamics (defensive pacts, nukes). */
		for (int i = 0; i <= m_kGame.getCurrentEra(); i++)
		{
			if (GC.getInfo((EraTypes)i).get(CvEraInfo::AIAgeOfGuns) ||
				GC.getInfo((EraTypes)i).get(CvEraInfo::AIAtomicAge))
			{
				return 0;
			}
		}
		rTension = 1 - scaled(iMinPeaceCounter, iMaxPeaceCounter) * rSpeedMult;
		rTension.increaseTo(0);
		rTension /= 2; // Less than 0.5 when there are no wars
	}
	else
	{
		// Mean of the per-team minima
		int const iMeanPeaceCounter = stats::mean(aiPeaceCounters);
		rTension = 1 - scaled(iMeanPeaceCounter, iMaxPeaceCounter) * rSpeedMult;
		rTension.increaseTo(0);
		// There is at least one war, so let's not go below 0.5.
		rTension += 1;
		rTension /= 2;
	}
	scaled rTensionTarget = m_kGame.gameTurnProgress() * fixp(10/3.);
	rTensionTarget.decreaseTo(fixp(2/3.));
	if (rTension.approxEquals(rTensionTarget, fixp(0.1)))
		return 0;
	m_rTensionIncrease = (rTensionTarget - rTension) *
			scaled(iOtherKnown).sqrt() / 2;
	m_rTensionIncrease.clamp(-1, 1);
	log("Seeking to adjust tension (overall warfare) by %d percent",
			m_rTensionIncrease.getPercent());
	return 0;
}


void DramaticArc::evaluate()
{
	if (m_rTensionIncrease == 0) // Often the case, save time.
		return;
	bool const bWillBeAtWar = militAnalyst().isWar(eWe, eThey);
	if (bWillBeAtWar == kOurTeam.isAtWar(eTheirTeam))
		return;
	if (kTheirTeam.isAVassal()) // Only care about wars between free civs
		return;
	/*	We're already doing our part. And don't prolong wars either just b/c there's
		already too little going on. The end of a war is an interesting event
		in itself, and let's see what will develop in the aftermath. */
	if (m_rTensionIncrease > 0 && kOurTeam.getNumWars() > 0)
		return;
	scaled const rWeight = 16;
	scaled rUtil = m_rTensionIncrease * (bWillBeAtWar ? 1 : -1) * rWeight;
	if (rUtil > 0 && bWillBeAtWar) // Don't encourage phoney or unfair wars ...
	{
		int iTheirLostCities = (int)militAnalyst().lostCities(eThey).size();
		if (iTheirLostCities > 2 || // We should be motivated enough (if it's a fair war)
			// I worry that the AI will go after humans too hard and too often ...
			(kThey.isHuman() && iTheirLostCities == 1 && kThey.hasCapital() &&
			militAnalyst().lostCities(eThey).count(kThey.getCapital()->plotNum()) > 0 &&
			TeamIter<MAJOR_CIV,OTHER_KNOWN_TO>::count(eOurTeam) > 2))
		{
			return;
		}
		if ((iTheirLostCities == 0 && militAnalyst().conqueredCities(eWe).empty()) ||
			(militAnalyst().lostPower(eWe, ARMY) + militAnalyst().lostPower(eThey, ARMY)) <
			std::max(ourCache().getPowerValues()[ARMY]->power(), scaled::epsilon()) / 20)
		{
			//log("Too little action expected - not a good way to increase tension");
			return;
		}
	}
	// Tension in team games is jumpy, don't try too hard to steer it.
	rUtil /= scaled(kOurTeam.getNumMembers() + kTheirTeam.getNumMembers(), 2);
	m_iU += rUtil.round();
}
