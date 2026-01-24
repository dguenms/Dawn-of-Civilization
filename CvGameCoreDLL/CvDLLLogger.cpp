// advc: New class; see CvDLLLogger.h.

#include "CvGameCoreDLL.h"
#include "CvGame.h"
#include "CvPlayer.h"
#include "CvCity.h"
#include "CvUnit.h"
// <advc.mapstat>
#include "CvMap.h"
#include "CvArea.h"
#include "CvInfo_Terrain.h"
// </advc.mapstat>
#include "AgentIterator.h" // advc.tsl

CvDLLLogger::CvDLLLogger(bool bEnabled, bool bRandEnabled)
:	m_bEnabled(bEnabled), m_bRandEnabled(bRandEnabled) {}

// Cut from CvRandom::getInt
void CvDLLLogger::logRandomNumber(const TCHAR* szMsg, unsigned short usNum,
	unsigned int uiSeed, int iData1, int iData2,
	CvString const* pszFileName) // advc.007b
{
	FAssert(isEnabledRand()); // Caller should handle this, for performance reasons.
	if (szMsg == NULL)
		return;
	int const iTurnSlice = GC.getGame().getTurnSlice();
	if (iTurnSlice <= 0)
		return;
	TCHAR szOut[1024];
	// <advc.007>
	CvString szData;
	if (iData1 > MIN_INT)
	{
		if(iData2 == MIN_INT)
			szData.Format(" (%d)", iData1);
		else szData.Format(" (%d, %d)", iData1, iData2);
	}
	bool bNetworkMP = GC.getGame().isNetworkMultiPlayer();
	/*  Don't show iTurnSlice in singleplayer b/c that makes it harder to
		compare log files. */
	int iOn = iTurnSlice;
	if (!bNetworkMP)
		iOn = GC.getGame().getGameTurn(); // (any more useful info to put here?)
	// The second and last %s are new
	std::sprintf(szOut, "Rand = %u / %hu (%s%s) on %s%d\n", uiSeed, usNum,
			szMsg, szData.c_str(), bNetworkMP ? "" : "t", iOn);
	// <advc.007b>
	if (pszFileName != NULL)
		gDLL->logMsg(pszFileName->c_str(), szOut, false, false);
	else // </advc.007b>
	if (GC.getDefineBOOL(CvGlobals::PER_PLAYER_MESSAGE_CONTROL_LOG) && bNetworkMP)
	{
		CvString logName = CvString::format("MPLog%d.log",
				(int)GC.getGame().getActivePlayer());
		gDLL->logMsg(logName.c_str(), szOut, false, false);
	}
	else // </advc.007>
		gDLL->messageControlLog(szOut);
}

// Cut from CvPlayer::setTurnActive
void CvDLLLogger::logTurnActive(PlayerTypes ePlayer)
{
	if (!isEnabled()) // || gDLL->getChtLvl() <= 0) // advc.007
		return;
	TCHAR szOut[1024];
	std::sprintf(szOut, "Player %d Turn ON\n", ePlayer);
	gDLL->messageControlLog(szOut);
}

// Cut from CvCity::init
void CvDLLLogger::logCityBuilt(CvCity const& kCity)
{
	if (!isEnabled()) //|| gDLL->getChtLvl() <= 0) // advc.007
		return;
	TCHAR szOut[1024];
	std::sprintf(szOut, "Player %d City %d built at %d:%d\n", kCity.getOwner(),
			kCity.getID(), kCity.getX(), kCity.getY());
	gDLL->messageControlLog(szOut);
}

// Cut from CvUnit::setCombatUnit
void CvDLLLogger::logCombat(CvUnit const& kAttacker, CvUnit const& kDefender)
{
	if (!isEnabled()) //|| gDLL->getChtLvl() <= 0) // advc.007
		return;
	char szOut[1024];
	std::sprintf( szOut, "*** KOMBAT!\n     ATTACKER: Player %d Unit %d (%S's %S), CombatStrength=%d\n"
		"     DEFENDER: Player %d Unit %d (%S's %S), CombatStrength=%d\n",
			kAttacker.getOwner(), kAttacker.getID(), GET_PLAYER(kAttacker.getOwner()).getName(), kAttacker.getName().GetCString(), kAttacker.currCombatStr(NULL, NULL),
			kDefender.getOwner(), kDefender.getID(), GET_PLAYER(kDefender.getOwner()).getName(), kDefender.getName().GetCString(), kDefender.currCombatStr(kDefender.plot(), &kAttacker));
	gDLL->messageControlLog(szOut);
}

// Cut from CvSelectionGroupAI::AI_update
void CvDLLLogger::logUnitStuck(CvUnit const& kUnit)
{
	if (!isEnabled())
		return;
	TCHAR szOut[1024];
	CvWString szTempString;
	::getUnitAIString(szTempString, kUnit.AI_getUnitAIType());
	std::sprintf(szOut, "Unit stuck in loop: %S(%S)[%d, %d] (%S)\n",
			kUnit.getName().GetCString(), GET_PLAYER(kUnit.getOwner()).getName(),
			kUnit.getX(), kUnit.getY(), szTempString.GetCString());
	gDLL->messageControlLog(szOut);
}

// <advc.mapstat>
// Don't really want to include sstream in the header. Hence free functions.
namespace
{
void appendPercentage(std::ostringstream& os, char const* szLabel, int iAbsolute, int iTotal)
{
	FAssert(iAbsolute <= iTotal);
	if (iAbsolute <= 0)
		return;
	os.precision(1);
	os << szLabel << ": " << std::fixed << (100 * iAbsolute / (float)iTotal) <<
			"%% (" << iAbsolute << ")\n";
}

void appendPercentage(std::ostringstream& os, wchar const* szLabel, int iAbsolute, int iTotal)
{
	CvWString szWide(szLabel);
	CvString szNarrow(szWide);
	appendPercentage(os, szNarrow.c_str(), iAbsolute, iTotal);
}
}

void CvDLLLogger::logMapStats(bool bAfterNormalization)
{
	if (!isEnabled() || !GC.getDefineBOOL("LOG_MAP_STATS"))
		return;
	std::ostringstream out;
	out << "\nMap stats";
	if (bAfterNormalization)
		out << " after normalization";
	out << ":\n\n";
	/*  As for map settings - will have to go to the Victory screen
		and maybe take a screenshot. */
	std::vector<int> plotTypeCounts;
	plotTypeCounts.resize(NUM_PLOT_TYPES);
	std::vector<int> landTerrainCounts;
	landTerrainCounts.resize(GC.getNumTerrainInfos());
	std::vector<int> waterTerrainCounts;
	waterTerrainCounts.resize(GC.getNumTerrainInfos());
	std::vector<int> landFeatureCounts;
	landFeatureCounts.resize(GC.getNumFeatureInfos());
	std::vector<int> waterFeatureCounts;
	waterFeatureCounts.resize(GC.getNumFeatureInfos());
	std::vector<int> landResourceCounts;
	landResourceCounts.resize(GC.getNumBonusInfos());
	std::vector<int> waterResourceCounts;
	waterResourceCounts.resize(GC.getNumBonusInfos());
	int iRiverPlots = 0;
	int iResourceTotal = 0;
	CvMap const& kMap = GC.getMap();
	for (int i = 0; i < kMap.numPlots(); i++)
	{
		CvPlot const& kPlot = kMap.getPlotByIndex(i);
		plotTypeCounts[kPlot.getPlotType()]++;
		BonusTypes eBonus = kPlot.getBonusType();
		if (eBonus != NO_BONUS)
			iResourceTotal++;
		if (kPlot.isWater())
		{
			waterTerrainCounts[kPlot.getTerrainType()]++;
			waterFeatureCounts[kPlot.getFeatureType()]++;
			if (eBonus != NO_BONUS)
				waterResourceCounts[eBonus]++;
		}
		else
		{
			landTerrainCounts[kPlot.getTerrainType()]++;
			landFeatureCounts[kPlot.getFeatureType()]++;
			if (eBonus != NO_BONUS)
				landResourceCounts[eBonus]++;
			if (kPlot.isRiver())
				iRiverPlots++;
		}
	}
	int iTotal = kMap.numPlots();
	out << "Total tile count: " << iTotal << " (" << kMap.getGridWidth()
			<< "x" << kMap.getGridHeight() << ")\n";
	int iWater = plotTypeCounts[PLOT_OCEAN];
	int iLand = iTotal - iWater;
	FAssert(iLand > 0);
	appendPercentage(out, "Land", iLand, iTotal);
	float fResourcesPerPlayer = iResourceTotal / (float)GC.getGame().getCivPlayersEverAlive();
	out.precision(2);
	out << "Resource total: " << iResourceTotal << " (" << std::fixed << fResourcesPerPlayer <<
			" per player)\n";
	for (int iPass = 0; iPass < 2; iPass++)
	{
		bool const bWater = (iPass == 1);
		out << (bWater ? "Water" : "Land") << " breakdown:\n";
		if (!bWater)
		{
			appendPercentage(out, "Hills", plotTypeCounts[PLOT_HILLS], iLand);
			appendPercentage(out, "Peak", plotTypeCounts[PLOT_PEAK], iLand);
		}
		int iTiles = (bWater ? iWater : iLand);
		std::vector<int>& terrainCounts = (bWater ? waterTerrainCounts : landTerrainCounts);
		std::vector<int>& featureCounts = (bWater ? waterFeatureCounts : landFeatureCounts);
		std::vector<int>& resourceCounts = (bWater ? waterResourceCounts : landResourceCounts);
		for (size_t i = 0; i < terrainCounts.size(); i++)
		{
			CvTerrainInfo const& kTerrain = GC.getInfo((TerrainTypes)i);
			appendPercentage(out, kTerrain.getDescription(), terrainCounts[i], iTiles);
		}
		for (size_t i = 0; i < featureCounts.size(); i++)
		{
			CvFeatureInfo const& kFeature = GC.getInfo((FeatureTypes)i);
			appendPercentage(out, kFeature.getDescription(), featureCounts[i], iTiles);
		}
		int iResources = 0;
		for (size_t i = 0; i < resourceCounts.size(); i++)
			iResources += resourceCounts[i];
		out << "Resources: " << iResources << "\n";
		for (size_t i = 0; i < resourceCounts.size(); i++)
		{
			if (resourceCounts[i] <= 0)
				continue;
			CvBonusInfo const& kBonus = GC.getInfo((BonusTypes)i);
			CvWString szWide(kBonus.getDescription());
			CvString szNarrow(szWide);
			out << szNarrow.c_str() << ": " << resourceCounts[i] << "\n";
		}
	}
	appendPercentage(out, "River plots", iRiverPlots, iLand);
	std::vector<int> majorLandmassSizes;
	int iIslands = 0;
	int iLargeIslands = 0;
	int iContinents = 0;
	FOR_EACH_AREA(pArea)
	{
		if (pArea->isWater())
			continue;
		int iSize = pArea->getNumTiles();
		if (iSize >= NUM_CITY_PLOTS)
		{
			majorLandmassSizes.push_back(iSize);
			if (iSize >= 3 * NUM_CITY_PLOTS)
				iContinents++;
			else iLargeIslands++;
		}
		else iIslands++;
	}
	out << "Continents: " << iContinents << ", large islands: " << iLargeIslands <<
			", islands: " << iIslands << "\n";
	std::sort(majorLandmassSizes.rbegin(), majorLandmassSizes.rend());
	if (!majorLandmassSizes.empty())
		out << "Major landmass sizes:\n";
	for (size_t i = 0; i < majorLandmassSizes.size(); i++)
	{
		out << majorLandmassSizes[i];
		if (i + 1 < majorLandmassSizes.size())
			out << ", ";
	}
	out << std::endl;
	gDLL->messageControlLog(const_cast<char*>(out.str().c_str()));
} // </advc.mapstat>

// advc.tsl:
void CvDLLLogger::logCivLeaders()
{
	if (!isEnabled())
		return;
	CvWString szCivNames;
	bool bFirst = true;
	for (PlayerIter<CIV_ALIVE> it; it.hasNext(); ++it)
	{
		setListHelp(szCivNames, L"\nCiv leaders on map: ",
				GC.getInfo(it->getLeaderType()).getDescription(),
				L", ", bFirst);
	}
	szCivNames.append(NEWLINE);
	gDLL->messageControlLog(const_cast<char*>(CvString(szCivNames).c_str()));
}
