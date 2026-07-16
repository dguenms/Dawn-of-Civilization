#pragma once

#ifndef CIV4_GAMECORE_UTILS_H
#define CIV4_GAMECORE_UTILS_H

class CvPlot;
class CvCity;
class CvCityAI; // advc.003u
class CvUnit;
class CvUnitAI; // advc.003u
class CvSelectionGroup;
class CvString;
class CvRandom;
class FAStarNode;
class FAStar;

/*	advc:
 +	All functions dealing with arithmetics moved to ArithmeticUtils.h
	except getSign (now in CvPlot.cpp) and any functions involving randomness.
 +	Distance functions moved into CvMap.h.
 +	Shuffle functions moved to CvRandom.
 +	advc.opt: getCity, getUnit moved to CvPlayer.h. CvCity::fromIDInfo and
	CvUnit::fromIDInfo as alternatives in files that don't include CvPlayer.h.
 +	Unit cycling functions moved to CvSelectionGroup, CvUnit.
 +	Asset score functions moved to CvGame; no longer exposed to Python.
 +	isPromotionValid moved to CvUnitInfo, finalImprovementUpgrade to CvImprovementInfo,
	getEspionageModifier to CvTeam, getWorldSizeMaxConscript to CvGame (as getMaxConscript;
	no longer exposed to Python).
 +	advc.003w: Moved some two dozen functions to CvInfo classes;
	mostly functions dealing with building and unit class limitations.
	Removed isTechRequiredForProject.
 +	getCombatOdds, LFBgetCombatOdds moved to CombatOdds.
 +	advc.pf: FAStar functions moved into new header FAStarFunc.h
 What's left here are (non-arithmetic) things that people (such as myself)
 have been too lazy to find a proper place for. */

// advc:
namespace std11
{
// Erik: "Back-ported" from C++11
template<class ForwardIt, class T>
void iota(ForwardIt first, ForwardIt last, T value)
{
	while (first != last)
	{
		*first++ = value;
		value++;
	}
}
};

/*	advc: Based K-Mod code in CvPlayer::getNextGroupInCycle; I find myself using
	this pattern from time to time:
	When a function optionally returns an additional value through a
	pointer argument that can be NULL, then define a local reference that
	refers to the same memory as the pointer arg - unless the pointer arg
	is NULL, in which case a local dummy variable is referenced instead. */
#define LOCAL_REF(T, localRefVarName, pointerArgName, tInitialVal) \
	T localRefVarName##_local = tInitialVal; /* dummy */ \
	T& localRefVarName = (pointerArgName == NULL ? localRefVarName##_local : *pointerArgName); \
	localRefVarName = tInitialVal; /* ensure initialization */

void contestedPlots(std::vector<CvPlot*>& r, TeamTypes t1, TeamTypes t2); // advc.035
// advc.130h:
template<typename T> void removeDuplicates(std::vector<T>& v)
{
	std::set<T> aeTmp(v.begin(), v.end());
	v.assign(aeTmp.begin(), aeTmp.end());
}

// advc.004w:
void applyColorToString(CvWString& s, char const* szColor, bool bLink = false);

float colorDifference(NiColorA const& c1, NiColorA const& c2); // advc.002i

// <advc> Replacing (unused) tables in CvGlobals for single-step rotation
inline DirectionTypes rotateDirClockw(DirectionTypes eDir,
	int i45DegRotations = 1) // Mustn't be less than -NUM_DIRECTION_TYPES
{
	/*	Could also try
		return static_cast<DirectionTypes>((eDir + i45DegRotations) & (NUM_DIRECTION_TYPES - 1));
		... but I guess the optimizer will handle it. */
	return static_cast<DirectionTypes>((eDir + i45DegRotations
			+ NUM_DIRECTION_TYPES) // To avoid negative remainder
			% NUM_DIRECTION_TYPES);
}

inline DirectionTypes rotateDirCounterClockw(DirectionTypes eDir,
	int i45DegRotations = 1)
{
	return rotateDirClockw(eDir, -i45DegRotations);
} // </advc>
inline CardinalDirectionTypes getOppositeCardinalDirection(CardinalDirectionTypes eDir)		// Exposed to Python
{
	return (CardinalDirectionTypes)((eDir + 2) % NUM_CARDINALDIRECTION_TYPES);
}
DirectionTypes cardinalDirectionToDirection(CardinalDirectionTypes eCard);					// Exposed to Python
DllExport inline bool isCardinalDirection(DirectionTypes eDirection)						// Exposed to Python
{
	switch (eDirection)
	{
	case DIRECTION_EAST:
	case DIRECTION_NORTH:
	case DIRECTION_SOUTH:
	case DIRECTION_WEST:
		return true;
	}
	return false;
}
DirectionTypes estimateDirection(int iDX, int iDY);											// Exposed to Python
DllExport DirectionTypes estimateDirection(const CvPlot* pFromPlot, const CvPlot* pToPlot);

// advc: Moved from CvXMLLoadUtility. (CvHotKeyInfo might be an even better place?)
namespace hotkeyDescr
{
	CvWString keyStringFromKBCode(TCHAR const* szDescr);
	CvWString hotKeyFromDescription(TCHAR const* szDescr,
			bool bShift = false, bool bAlt = false, bool bCtrl = false);
}

bool atWar(TeamTypes eTeamA, TeamTypes eTeamB);												// Exposed to Python
//isPotentialEnemy(TeamTypes eOurTeam, TeamTypes eTheirTeam); // advc: Use CvTeamAI::AI_mayAttack instead

int estimateCollateralWeight(const CvPlot* pPlot, TeamTypes eAttackTeam, TeamTypes eDefenseTeam = NO_TEAM); // K-Mod

/*	advc (note): Still used in the DLL by CvPlayer::buildTradeTable, but mostly deprecated.
	Use the TradeData constructor instead. */
DllExport void setTradeItem(TradeData* pItem, TradeableItems eItemType = TRADE_ITEM_NONE, int iData = 0);

/*	advc: Unused. Thought about moving these to CvGameTextMgr,
	but that'll lead to more header inclusions. */
//void setListHelp(wchar* szBuffer, const wchar* szStart, const wchar* szItem, const wchar* szSeparator, bool bFirst);
void setListHelp(CvWString& szBuffer, wchar const* szStart, wchar const* szItem,
		wchar const* szSeparator, bool& bFirst); // advc: bool&
void setListHelp(CvWStringBuffer& szBuffer, wchar const* szStart, wchar const* szItem,
		wchar const* szSeparator, bool& bFirst); // advc: bool&
/*	<advc> Add variants for items that can go into one list only when a value
	matches the most recently added item. (This stuff should really be wrapped
	into a class.) */
void setListHelp(CvWString& szBuffer, wchar const* szStart, wchar const* szItem,
		wchar const* szSeparator, int& iLastListID, int iListID);
void setListHelp(CvWStringBuffer& szBuffer, wchar const* szStart, wchar const* szItem,
		wchar const* szSeparator, int& iLastListID, int iListID); // </advc>

// PlotUnitFunc's...  (advc: Parameters iData1, iData2 renamed)
bool PUF_isGroupHead(CvUnit const* pUnit, int iDummy1 = -1, int iDummy2 = -1);
bool PUF_isPlayer(CvUnit const* pUnit, int iOwner, int iForTeam = NO_TEAM);
bool PUF_isTeam(CvUnit const* pUnit, int iTeam, int iDummy = -1);
bool PUF_isCombatTeam(CvUnit const* pUnit, int iTeam, int iForTeam);
bool PUF_isOtherPlayer(CvUnit const* pUnit, int iPlayer, int iDummy = -1);
bool PUF_isOtherTeam(CvUnit const* pUnit, int iPlayer, int iDummy = -1);
bool PUF_canDefend(CvUnit const* pUnit, int iDummy1 = -1, int iDummy2 = -1);
bool PUF_canDefendAgainst( const CvUnit* pUnit, int iData1 = -1, int iData2 = -1); // doc
bool PUF_cannotDefend(CvUnit const* pUnit, int iDummy1 = -1, int iDummy2 = -1);
bool PUF_canDefendGroupHead(CvUnit const* pUnit, int iDummy1 = -1, int iDummy2 = -1);
bool PUF_canDefendPotentialEnemy(CvUnit const* pUnit, int iPlayer, BOOL iAlwaysHostile = false);
bool PUF_canDefendEnemy(CvUnit const* pUnit, int iPlayer, BOOL iAlwaysHostile = false);
bool PUF_canDefendAgainstEnemy( const CvUnit* pUnit, int iData1, int iData2 = 1); // doc // TODO: needed?
bool PUF_isPotentialEnemy(CvUnit const* pUnit, int iPlayer, BOOL iAlwaysHostile = false);
bool PUF_isEnemy(CvUnit const* pUnit, int iPlayer, BOOL iAlwaysHostile = false);
bool PUF_canDeclareWar(CvUnit const* pUnit, int iPlayer, BOOL iAlwaysHostile = false);
// advc.ctr:
bool PUF_isEnemyCityAttacker(CvUnit const* pUnit, int iPlayer, int iAssumePeaceTeam = NO_TEAM);
bool PUF_isVisible(CvUnit const* pUnit, int iPlayer, int iDummy = -1);
bool PUF_isVisibleDebug(CvUnit const* pUnit, int iTargetPlayer, int iDummy = -1);
bool PUF_isLethal(CvUnit const* pUnit, int iDummy1 = -1, int iDummy2 = -1); // advc.298
bool PUF_canSiege(CvUnit const* pUnit, int iTargetPlayer, int iDummy = -1);
bool PUF_canAirAttack(CvUnit const* pUnit, int iDummy1 = -1, int iDummy2 = -1);
bool PUF_canAirDefend(CvUnit const* pUnit, int iDummy1 = -1, int iDummy2 = -1);
bool PUF_isAirIntercept(CvUnit const* pUnit, int iDummy1, int iDummy2); // K-Mod
bool PUF_isFighting(CvUnit const* pUnit, int iDummy1 = -1, int iDummy2 = -1);
bool PUF_isAnimal(CvUnit const* pUnit, int iDummy1 = -1, int iDummy2 = -1);
bool PUF_isMilitaryHappiness(CvUnit const* pUnit, int iDummy1 = -1, int iDummy2 = -1);
bool PUF_isInvestigate(CvUnit const* pUnit, int iDummy1 = -1, int iDummy2 = -1);
bool PUF_isCounterSpy(CvUnit const* pUnit, int iDummy1 = -1, int iDummy2 = -1);
bool PUF_isSpy(CvUnit const* pUnit, int iDummy1 = -1, int iDummy2 = -1);
bool PUF_isDomainType(CvUnit const* pUnit, int iDomain, int iDummy = -1);
bool PUF_isUnitType(CvUnit const* pUnit, int iUnit, int iDummy = -1);
bool PUF_isUnitAIType(CvUnit const* pUnit, int iUnitAI, int iDummy = -1);
bool PUF_isMissionAIType(CvUnit const* pUnit, int iMissionAI, int iDummy = -1); // K-Mod
bool PUF_isCityAIType(CvUnit const* pUnit, int iDummy1 = -1, int iDummy2 = -1);
bool PUF_isNotCityAIType(CvUnit const* pUnit, int iDummy1 = -1, int iDummy2 = -1);
bool PUF_isSelected(CvUnit const* pUnit, int iDummy1 = -1, int iDummy2 = -1);
//bool PUF_isNoMission(const CvUnit* pUnit, int iDummy1 = -1, int iDummy2 = -1);
// advc.113b:
bool PUF_isMissionPlotWorkingCity(CvUnit const* pUnit, int iCity, int iOwner);
bool PUF_isFiniteRange(CvUnit const* pUnit, int iDummy1 = -1, int iDummy2 = -1);
// bbai start
bool PUF_isAvailableUnitAITypeGroupie(CvUnit const* pUnit, int iUnitAI, int iDummy);
bool PUF_isFiniteRangeAndNotJustProduced(CvUnit const* pUnit, int iDummy1 = -1, int iDummy2 = -1);
// bbai end

bool PUF_makeInfoBarDirty(CvUnit* pUnit, int iDummy1 = -1, int iDummy2 = -1);

int baseYieldToSymbol(int iNumYieldTypes, int iYieldStack);
//bool isPickableName(const TCHAR* szName); // advc.003j

/*  advc: Hash based on kInputs. Plot index of capital factored in for
	increased range if ePlayer given. (ePlayer is ignored if it has no capital.) */
int intHash(std::vector<int> const& kInputs, PlayerTypes ePlayer = NO_PLAYER);

// <advc.003g>
namespace fmath
{
	/*	See intHash about the parameters.
		Result between 0 and 1. Returns float b/c CvRandom uses float (not double).
		(Similar but more narrow: CvUnitAI::AI_unitBirthmarkHash, AI_unitPlotHash) */
	inline float hash(std::vector<int> const& kInputs, PlayerTypes ePlayer = NO_PLAYER)
	{
		/*  Use ASyncRand to avoid the overhead of creating a new object?
			Or use stdlib's rand/srand? I don't think it matters. */
		/*CvRandom& rng = GC.getASyncRand();
		rng.reset(hashVal);*/
		CvRandom rng;
		rng.init(intHash(kInputs, ePlayer));
		return rng.getFloat();
	}
	// For hashing just a single input
	inline float hash(int iInputs, PlayerTypes ePlayer = NO_PLAYER)
	{
		std::vector<int> inputs;
		inputs.push_back(iInputs);
		return hash(inputs, ePlayer);
	}
} // </advc.003g>

int getTurnMonthForGame(int iGameTurn, int iStartYear, CalendarTypes eCalendar, GameSpeedTypes eSpeed);
int getTurnYearForGame(int iGameTurn, int iStartYear, CalendarTypes eCalendar, GameSpeedTypes eSpeed);

int getTurnForYear(int iTurnYear); // doc (edead)
int getGameTurnForYear(int iTurnYear, int iStartYear, CalendarTypes eCalendar, GameSpeedTypes eSpeed); // doc (edead)
int getGameTurnForMonth(int iTurnMonth, int iStartYear, CalendarTypes eCalendar, GameSpeedTypes eSpeed); // doc (edead)
int getTurns(int iTurns); // doc (edead)

ScenarioTypes getScenario(); // doc
int getScenarioStartYear(ScenarioTypes eScenario = NO_SCENARIO); // doc
int getScenarioStartTurn(); // doc

BuildingTypes getUniqueBuilding(CivilizationTypes eCivilization, BuildingTypes eBuilding); // doc
UnitTypes getUniqueUnit(CivilizationTypes eCivilization, UnitTypes eUnit); // doc

bool isPrecursor(ReligionTypes ePrecursor, ReligionTypes eReligion); // doc

void setDirty(InterfaceDirtyBits eDirtyBit, bool bNewValue);

void log(char* format, ...);
void log(CvWString message);
void log(CvString logfile, CvString message);

bool isCivAlive(CivilizationTypes eCivilization); // doc
bool validatePeriodConstant(PeriodTypes ePeriod); // doc

bool isHumanVictoryWonder(BuildingTypes eBuilding, BuildingTypes eWonder, CivilizationTypes eCivilization);

void getDirectionTypeString(CvWString& szString, DirectionTypes eDirectionType);
void getCardinalDirectionTypeString(CvWString& szString, CardinalDirectionTypes eDirectionType);
void getActivityTypeString(CvWString& szString, ActivityTypes eActivityType);
void getMissionTypeString(CvWString& szString, MissionTypes eMissionType);
void getMissionAIString(CvWString& szString, MissionAITypes eMissionAI);
void getUnitAIString(CvWString& szString, UnitAITypes eUnitAI);

#endif
