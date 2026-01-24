// Python wrapper class for CvGame

#include "CvGameCoreDLL.h"
#include "CyGame.h"
#include "CvGameAI.h"
#include "StartPointsAsHandicap.h" // advc.250b
#include "RiseFall.h" // advc.703
#include "CyPlayer.h"
#include "CyDeal.h"
#include "CyReplayInfo.h"
#include "CvMap.h" // advc.enum

void CyGame::updateScore(bool bForce)
{
	m_kGame.updateScore(bForce);
}

void CyGame::cycleCities(bool bForward, bool bAdd)
{
	m_kGame.cycleCities(bForward, bAdd);
}

void CyGame::cycleSelectionGroups(bool bClear, bool bForward, bool bWorkers)
{
	m_kGame.cycleSelectionGroups(bClear, bForward, bWorkers);
}

bool CyGame::cyclePlotUnits(CyPlot* pPlot, bool bForward, bool bAuto, int iCount)
{
	return m_kGame.cyclePlotUnits(pPlot->getPlot(), bForward, bAuto, iCount);
}
// advc.154:
CyUnit* CyGame::getNextUnitInCycle(bool bForward, bool bWorkers)
{
	CvUnit* pUnit = GC.getGame().getCycleButtonUnit(bForward, bWorkers);
	if (pUnit == NULL)
		return NULL;
	return new CyUnit(pUnit);
}

void CyGame::selectionListMove(CyPlot* pPlot, bool bAlt, bool bShift, bool bCtrl)
{
	GC.getGame().selectionListMove(pPlot->getPlot(), bAlt, bShift, bCtrl);
}

void CyGame::selectionListGameNetMessage(int eMessage, int iData2, int iData3, int iData4, int iFlags, bool bAlt, bool bShift)
{
	GC.getGame().selectionListGameNetMessage(eMessage, iData2, iData3, iData4, iFlags, bAlt, bShift);
}

void CyGame::selectedCitiesGameNetMessage(int eMessage, int iData2, int iData3, int iData4, bool bOption, bool bAlt, bool bShift, bool bCtrl)
{
	GC.getGame().selectedCitiesGameNetMessage(eMessage, iData2, iData3, iData4, bOption, bAlt, bShift, bCtrl);
}

void CyGame::cityPushOrder(CyCity* pCity, OrderTypes eOrder, int iData, bool bAlt, bool bShift, bool bCtrl)
{
	GC.getGame().cityPushOrder(pCity->getCity(), eOrder, iData, bAlt, bShift, bCtrl);
}

int CyGame::getSymbolID(int iSymbol)
{
	return m_kGame.getSymbolID(iSymbol);
}

int CyGame::getProductionPerPopulation(int /*HurryTypes*/ eHurry)
{
	return m_kGame.getProductionPerPopulation((HurryTypes) eHurry);
}

int CyGame::getAdjustedPopulationPercent(int /*VictoryTypes*/ eVictory)
{
	return m_kGame.getAdjustedPopulationPercent((VictoryTypes) eVictory);
}

int CyGame::getAdjustedLandPercent(int /* VictoryTypes*/ eVictory)
{
	return m_kGame.getAdjustedLandPercent((VictoryTypes) eVictory);
}
// advc.178:
bool CyGame::isDiploVictoryValid()
{
	return m_kGame.isDiploVictoryValid();
}

bool CyGame::isTeamVote(int /*VoteTypes*/ eVote) const
{
	return m_kGame.isTeamVote((VoteTypes) eVote);
}

bool CyGame::isChooseElection(int /*VoteTypes*/ eVote) const
{
	return m_kGame.isChooseElection((VoteTypes) eVote);
}

bool CyGame::isTeamVoteEligible(int /*TeamTypes*/ eTeam, int /*VoteSourceTypes*/ eVoteSource) const
{
	return m_kGame.isTeamVoteEligible((TeamTypes) eTeam, (VoteSourceTypes)eVoteSource);
}

int CyGame::countPossibleVote(int /*VoteTypes*/ eVote, int /*VoteSourceTypes*/ eVoteSource) const
{
	return m_kGame.countPossibleVote((VoteTypes) eVote, (VoteSourceTypes)eVoteSource);
}

int CyGame::getVoteRequired(int /*VoteTypes*/ eVote, int /*VoteSourceTypes*/ eVoteSource) const
{
	return m_kGame.getVoteRequired((VoteTypes)eVote, (VoteSourceTypes) eVoteSource);
}

int CyGame::getSecretaryGeneral(int /*VoteSourceTypes*/ eVoteSource) const
{
	return m_kGame.getSecretaryGeneral((VoteSourceTypes) eVoteSource);
}

bool CyGame::canHaveSecretaryGeneral(int /*VoteSourceTypes*/ eVoteSource) const
{
	return m_kGame.canHaveSecretaryGeneral((VoteSourceTypes) eVoteSource);
}

int CyGame::getVoteSourceReligion(int /*VoteSourceTypes*/ eVoteSource) const
{
	return m_kGame.getVoteSourceReligion((VoteSourceTypes) eVoteSource);
}

void CyGame::setVoteSourceReligion(int /*VoteSourceTypes*/ eVoteSource, int /*ReligionTypes*/ eReligion, bool bAnnounce)
{
	m_kGame.setVoteSourceReligion((VoteSourceTypes)eVoteSource, (ReligionTypes)eReligion, bAnnounce);
}

int CyGame::countCivPlayersAlive()
{
	return m_kGame.countCivPlayersAlive();
}

int CyGame::countCivPlayersEverAlive()
{	// advc.opt: was m_kGame.countCivPlayersEverAlive()
	return m_kGame.getCivPlayersEverAlive();
}

int CyGame::countCivTeamsAlive()
{
	return m_kGame.countCivTeamsAlive();
}

int CyGame::countCivTeamsEverAlive()
{	// advc.opt: was m_kGame.countCivTeamsEverAlive()
	return m_kGame.getCivTeamsEverAlive();
}

int CyGame::countHumanPlayersAlive()
{
	return m_kGame.countHumanPlayersAlive();
}

int CyGame::countTotalCivPower()
{
	return m_kGame.countTotalCivPower();
}

int CyGame::countTotalNukeUnits()
{
	return m_kGame.countTotalNukeUnits();
}

int CyGame::countKnownTechNumTeams(int /*TechTypes*/ eTech)
{
	return m_kGame.countKnownTechNumTeams((TechTypes) eTech);
}

int CyGame::getNumFreeBonuses(int /*BuildingTypes*/ eBuilding)
{
	return m_kGame.getNumFreeBonuses((BuildingTypes) eBuilding);
}

int CyGame::countReligionLevels(int /*ReligionTypes*/ eReligion)
{
	return m_kGame.countReligionLevels((ReligionTypes) eReligion);
}

int CyGame::countCorporationLevels(int /*CorporationTypes*/ eCorporation)
{
	return m_kGame.countCorporationLevels((CorporationTypes) eCorporation);
}

int CyGame::calculateReligionPercent(int /*ReligionTypes*/ eReligion)
{
	return m_kGame.calculateReligionPercent((ReligionTypes) eReligion);
}

int CyGame::goldenAgeLength()
{
	return m_kGame.goldenAgeLength();
}

int CyGame::victoryDelay(int iVictory)
{
	return m_kGame.victoryDelay((VictoryTypes)iVictory);
}

int CyGame::getImprovementUpgradeTime(int /*ImprovementTypes*/ eImprovement)
{
	return m_kGame.getImprovementUpgradeTime((ImprovementTypes) eImprovement);
}

bool CyGame::canTrainNukes()
{
	return m_kGame.canTrainNukes();
}

int CyGame::getCurrentEra()
{
	return m_kGame.getCurrentEra();
}

int CyGame::getActiveTeam()
{
	return m_kGame.getActiveTeam();
}

int /* CivilizationTypes */ CyGame::getActiveCivilizationType()
{
	return m_kGame.getActiveCivilizationType();
}

bool CyGame::isNetworkMultiPlayer()
{
	return m_kGame.isNetworkMultiPlayer();
}

bool CyGame::isGameMultiPlayer()
{
	return m_kGame.isGameMultiPlayer();
}

bool CyGame::isTeamGame()
{
	return m_kGame.isTeamGame();
}

bool CyGame::isModem()
{
	return m_kGame.isModem(); // err on the side of caution
}

void CyGame::setModem(bool bModem)
{
	m_kGame.setModem(bModem);
}

void CyGame::reviveActivePlayer()
{
	m_kGame.reviveActivePlayer();
}

int CyGame::getNumHumanPlayers()
{
	return m_kGame.getNumHumanPlayers();
}

int CyGame::getGameTurn()
{
	return m_kGame.getGameTurn();
}

void CyGame::setGameTurn(int iNewValue)
{
	m_kGame.setGameTurn(iNewValue);
}

int CyGame::getTurnYear(int iGameTurn)
{
	return  m_kGame.getTurnYear(iGameTurn);
}

int CyGame::getGameTurnYear()
{
	return  m_kGame.getGameTurnYear();
}

int CyGame::getElapsedGameTurns()
{
	return m_kGame.getElapsedGameTurns();
}

int CyGame::getMaxTurns() const
{
	return m_kGame.getMaxTurns();
}

void CyGame::setMaxTurns(int iNewValue)
{
	m_kGame.setMaxTurns(iNewValue);
}

void CyGame::changeMaxTurns(int iChange)
{
	m_kGame.changeMaxTurns(iChange);
}

int CyGame::getMaxCityElimination() const
{
	return m_kGame.getMaxCityElimination();
}

void CyGame::setMaxCityElimination(int iNewValue)
{
	m_kGame.setMaxCityElimination(iNewValue);
}

int CyGame::getNumAdvancedStartPoints() const
{
	return m_kGame.getNumAdvancedStartPoints();
}

void CyGame::setNumAdvancedStartPoints(int iNewValue)
{
	m_kGame.setNumAdvancedStartPoints(iNewValue);
}

int CyGame::getStartTurn() const
{
	return m_kGame.getStartTurn();
}

// doc
void CyGame::setStartTurn(int iNewValue)
{
	if (m_pGame) m_pGame->setStartTurn(iNewValue);
}

int CyGame::getStartYear() const
{
	return m_kGame.getStartYear();
}

void CyGame::setStartYear(int iNewValue)
{
	m_kGame.setStartYear(iNewValue);
}

int CyGame::getEstimateEndTurn() const
{
	return m_kGame.getEstimateEndTurn();
}

void CyGame::setEstimateEndTurn(int iNewValue)
{
	m_kGame.setEstimateEndTurn(iNewValue);
}

int CyGame::getTurnSlice() const
{
	return m_kGame.getTurnSlice();
}

int CyGame::getMinutesPlayed() const
{
	return m_kGame.getMinutesPlayed();
}

// doc
int CyGame::getSecondsPlayed() const
{
	return m_pGame ? m_pGame->getSecondsPlayed() : 0;
}

int CyGame::getTargetScore() const
{
	return m_kGame.getTargetScore();
}

void CyGame::setTargetScore(int iNewValue)
{
	m_kGame.setTargetScore(iNewValue);
}

int CyGame::getNumGameTurnActive()
{
	return m_kGame.getNumGameTurnActive();
}

int CyGame::countNumHumanGameTurnActive()
{
	return m_kGame.countNumHumanGameTurnActive();
}

int CyGame::getNumCities()
{
	return m_kGame.getNumCities();
}

int CyGame::getNumCivCities()
{
	return m_kGame.getNumCivCities();
}

int CyGame::getTotalPopulation()
{
	return m_kGame.getTotalPopulation();
}

int CyGame::getTradeRoutes() const
{
	return m_kGame.getTradeRoutes();
}

void CyGame::changeTradeRoutes(int iChange)
{
	m_kGame.changeTradeRoutes(iChange);
}

int CyGame::getFreeTradeCount() const
{
	return m_kGame.getFreeTradeCount();
}

bool CyGame::isFreeTrade() const
{
	return m_kGame.isFreeTrade();
}

void CyGame::changeFreeTradeCount(int iChange)
{
	m_kGame.changeFreeTradeCount(iChange);
}

int CyGame::getNoNukesCount() const
{
	return m_kGame.getNoNukesCount();
}

bool CyGame::isNoNukes() const
{
	return m_kGame.isNoNukes();
}

void CyGame::changeNoNukesCount(int iChange)
{
	m_kGame.changeNoNukesCount(iChange);
}

int CyGame::getSecretaryGeneralTimer(int iVoteSource) const
{
	return m_kGame.getSecretaryGeneralTimer((VoteSourceTypes)iVoteSource);
}

int CyGame::getVoteTimer(int iVoteSource) const
{
	return m_kGame.getVoteTimer((VoteSourceTypes)iVoteSource);
}

int CyGame::getNukesExploded() const
{
	return m_kGame.getNukesExploded();
}

void CyGame::changeNukesExploded(int iChange)
{
	m_kGame.changeNukesExploded(iChange);
}

int CyGame::getMaxPopulation() const
{
	return m_kGame.getMaxPopulation();
}

int CyGame::getMaxLand() const
{
	return m_kGame.getMaxLand();
}

int CyGame::getMaxTech() const
{
	return m_kGame.getMaxTech();
}

int CyGame::getMaxWonders() const
{
	return m_kGame.getMaxWonders();
}

int CyGame::getInitPopulation() const
{
	return m_kGame.getInitPopulation();
}

int CyGame::getInitLand() const
{
	return m_kGame.getInitLand();
}

int CyGame::getInitTech() const
{
	return m_kGame.getInitTech();
}

int CyGame::getInitWonders() const
{
	return m_kGame.getInitWonders();
}

int CyGame::getAIAutoPlay() const
{
	return m_kGame.getAIAutoPlay();
}

void CyGame::setAIAutoPlay(int iNewValue)
{
	m_kGame.setAIAutoPlay(iNewValue);
}

// K-Mod, 11/dec/10, start
int CyGame::getGlobalWarmingIndex() const
{
	return m_kGame.getGlobalWarmingIndex();
}

int CyGame::getGlobalWarmingChances() const
{
	return m_kGame.getGlobalWarmingChances();
}

int CyGame::getGwEventTally() const
{
	return m_kGame.getGwEventTally();
}

int CyGame::calculateGlobalPollution() const
{
	return m_kGame.calculateGlobalPollution();
}

int CyGame::calculateGwLandDefence(int /* PlayerTypes */ ePlayer) const
{
	return m_kGame.calculateGwLandDefence((PlayerTypes)ePlayer);
}

int CyGame::calculateGwSustainabilityThreshold(int /* PlayerTypes */ ePlayer) const
{
	return m_kGame.calculateGwSustainabilityThreshold((PlayerTypes)ePlayer);
}

int CyGame::calculateGwSeverityRating() const
{
	return m_kGame.calculateGwSeverityRating();
}
// K-Mod end

bool CyGame::isScoreDirty() const
{
	return m_kGame.isScoreDirty();
}

void CyGame::setScoreDirty(bool bNewValue)
{
	m_kGame.setScoreDirty(bNewValue);
}

bool CyGame::isCircumnavigated() const
{
	return m_kGame.isCircumnavigated();
}

void CyGame::makeCircumnavigated()
{
	m_kGame.makeCircumnavigated();
}

// rfc
int CyGame::getCircumnavigated()
{
	return m_pGame ? m_pGame->getCircumnavigated() : false;
}

// rfc
void CyGame::setCircumnavigated(int iNewValue)
{
	if (m_pGame)
		m_pGame->setCircumnavigated(iNewValue);
}

bool CyGame::isDiploVote(int /*VoteSourceTypes*/ eVoteSource) const
{
	return m_kGame.isDiploVote((VoteSourceTypes)eVoteSource);
}

void CyGame::changeDiploVote(int /*VoteSourceTypes*/ eVoteSource, int iChange)
{
	m_kGame.changeDiploVote((VoteSourceTypes)eVoteSource, iChange);
}

// rfc
bool CyGame::isCheatingEnabled() const
{
	return (gDLL->getChtLvl() > 0);
}

bool CyGame::isDebugMode() const
{
	return m_kGame.isDebugMode();
}

void CyGame::toggleDebugMode()
{
	m_kGame.toggleDebugMode();
}

int CyGame::getPitbossTurnTime()
{
	return m_kGame.getPitbossTurnTime();
}

void CyGame::setPitbossTurnTime(int iHours)
{
	m_kGame.setPitbossTurnTime(iHours);
}

bool CyGame::isHotSeat()
{
	return m_kGame.isHotSeat();
}

bool CyGame::isPbem()
{
	return m_kGame.isPbem();
}

bool CyGame::isPitboss()
{
	return m_kGame.isPitboss();
}

bool CyGame::isSimultaneousTeamTurns()
{
	return m_kGame.isSimultaneousTeamTurns();
}

bool CyGame::isFinalInitialized()
{
	return m_kGame.isFinalInitialized();
}
// advc.061:
void CyGame::setScreenDimensions(int iWidth, int iHeight)
{
	m_kGame.setScreenDimensions(iWidth, iHeight);
}

int /*PlayerTypes*/ CyGame::getActivePlayer()
{
	return m_kGame.getActivePlayer();
}

void CyGame::setActivePlayer(int /*PlayerTypes*/ eNewValue, bool bForceHotSeat)
{
	m_kGame.setActivePlayer((PlayerTypes)eNewValue, bForceHotSeat);
}

int CyGame::getPausePlayer()
{
	return m_kGame.getPausePlayer();
}

bool CyGame::isPaused()
{
	return m_kGame.isPaused();
}

int /*PlayerTypes*/ CyGame::getBestLandUnit()
{
	return m_kGame.getBestLandUnit();
}

int CyGame::getBestLandUnitCombat()
{
	return m_kGame.getBestLandUnitCombat();
}

int /*TeamTypes*/ CyGame::getWinner()
{
	return m_kGame.getWinner();
}

int /*VictoryTypes*/ CyGame::getVictory()
{
	return m_kGame.getVictory();
}

void CyGame::setWinner(int /*TeamTypes*/ eNewWinner, int /*VictoryTypes*/ eNewVictory)
{
	m_kGame.setWinner((TeamTypes) eNewWinner, (VictoryTypes) eNewVictory);
}

int /*GameStateTypes*/ CyGame::getGameState()
{
	return m_kGame.getGameState();
}

int /* HandicapTypes */ CyGame::getHandicapType()
{
	return m_kGame.getHandicapType();
}

// advc.708:
int CyGame::getAIHandicap()
{
	return m_kGame.getAIHandicap();
}

CalendarTypes CyGame::getCalendar() const
{
	return m_kGame.getCalendar();
}

int /*EraTypes*/ CyGame::getStartEra()
{
	return m_kGame.getStartEra();
}

int /*GameSpeedTypes*/ CyGame::getGameSpeedType()
{
	return m_kGame.getGameSpeedType();
}

int /*PlayerTypes*/ CyGame::getRankPlayer(int iRank)
{
	return m_kGame.getRankPlayer((PlayerTypes)iRank);
}

int CyGame::getPlayerRank(int /*PlayerTypes*/ ePlayer)
{
	return m_kGame.getPlayerRank((PlayerTypes)ePlayer);
}

int CyGame::getPlayerScore(int /*PlayerTypes*/ ePlayer)
{
	return m_kGame.getPlayerScore((PlayerTypes)ePlayer);
}

int /*TeamTypes*/ CyGame::getRankTeam(int iRank)
{
	return m_kGame.getRankTeam((TeamTypes)iRank);
}

int CyGame::getTeamRank(int /*TeamTypes*/ eTeam)
{
	return m_kGame.getTeamRank((TeamTypes)eTeam);
}

int CyGame::getTeamScore(int /*TeamTypes*/ eTeam)
{
	return m_kGame.getTeamScore((TeamTypes)eTeam);
}

/*	advc: Exposed so that players can fix accidental settings
	through the Python console */
void CyGame::setVictoryValid(int iVictory, bool b)
{
	m_kGame.setVictoryValid((VictoryTypes)iVictory, b);
}

bool CyGame::isOption(int /*GameOptionTypes*/ eIndex)
{
	return m_kGame.isOption((GameOptionTypes)eIndex);
}

void CyGame::setOption(int /*GameOptionTypes*/ eIndex, bool bEnabled)
{
	m_kGame.setOption((GameOptionTypes)eIndex, bEnabled);
}

bool CyGame::isMPOption(int /*MultiplayerOptionTypes*/ eIndex)
{
	return m_kGame.isMPOption((MultiplayerOptionTypes)eIndex);
}

bool CyGame::isForcedControl(int /*ForceControlTypes*/ eIndex)
{
	return m_kGame.isForcedControl((ForceControlTypes)eIndex);
}

int CyGame::getUnitCreatedCount(int /*UnitTypes*/ eIndex)
{
	return m_kGame.getUnitCreatedCount((UnitTypes)eIndex);
}

int CyGame::getUnitClassCreatedCount(int /*UnitClassTypes*/ eIndex)
{
	return m_kGame.getUnitClassCreatedCount((UnitClassTypes)eIndex);
}

bool CyGame::isUnitClassMaxedOut(int /*UnitClassTypes*/ eIndex, int iExtra)
{
	return m_kGame.isUnitClassMaxedOut((UnitClassTypes)eIndex, iExtra);
}

int CyGame::getBuildingClassCreatedCount(int /*BuildingClassTypes*/ eIndex)
{
	return m_kGame.getBuildingClassCreatedCount((BuildingClassTypes) eIndex);
}

bool CyGame::isBuildingClassMaxedOut(int /*BuildingClassTypes*/ eIndex, int iExtra)
{
	return m_kGame.isBuildingClassMaxedOut((BuildingClassTypes)eIndex, iExtra);
}

int CyGame::getProjectCreatedCount(int /*ProjectTypes*/ eIndex)
{
	return m_kGame.getProjectCreatedCount((ProjectTypes) eIndex);
}

bool CyGame::isProjectMaxedOut(int /*ProjectTypes*/ eIndex, int iExtra)
{
	return m_kGame.isProjectMaxedOut((ProjectTypes)eIndex, iExtra);
}

int CyGame::getForceCivicCount(int /*CivicTypes*/ eIndex)
{
	return m_kGame.getForceCivicCount((CivicTypes) eIndex);
}

bool CyGame::isForceCivic(int /*CivicTypes*/ eIndex)
{
	return m_kGame.isForceCivic((CivicTypes)eIndex);
}

bool CyGame::isForceCivicOption(int /*CivicOptionTypes*/ eCivicOption)
{
	return m_kGame.isForceCivicOption((CivicOptionTypes)eCivicOption);
}

int CyGame::getVoteOutcome(int /*VoteTypes*/ eIndex)
{
	return m_kGame.getVoteOutcome((VoteTypes) eIndex);
}

int CyGame::getReligionGameTurnFounded(int /*ReligionTypes*/ eIndex)
{
	return m_kGame.getReligionGameTurnFounded((ReligionTypes) eIndex);
}

// doc
void CyGame::setReligionGameTurnFounded(int eReligion, int iGameTurn)
{
	if (m_pGame) m_pGame->setReligionGameTurnFounded((ReligionTypes)eReligion, iGameTurn);
}

bool CyGame::isReligionFounded(int /*ReligionTypes*/ eIndex)
{
	return m_kGame.isReligionFounded((ReligionTypes) eIndex);
}

bool CyGame::isReligionSlotTaken(int /*ReligionTypes*/ eIndex)
{
	return m_kGame.isReligionSlotTaken((ReligionTypes) eIndex);
}

int CyGame::getCorporationGameTurnFounded(int /*CorporationTypes*/ eIndex)
{
	return m_kGame.getCorporationGameTurnFounded((CorporationTypes) eIndex);
}

bool CyGame::isCorporationFounded(int /*CorporationTypes*/ eIndex)
{
	return m_kGame.isCorporationFounded((CorporationTypes) eIndex);
}

bool CyGame::isVotePassed(int /*VoteTypes*/ eIndex) const
{
	return m_kGame.isVotePassed((VoteTypes)eIndex);
}

bool CyGame::isVictoryValid(int /*VictoryTypes*/ eIndex)
{
	return m_kGame.isVictoryValid((VictoryTypes)eIndex);
}

bool CyGame::isSpecialUnitValid(int /*SpecialUnitTypes*/ eSpecialUnitType)
{
	return m_kGame.isSpecialUnitValid((SpecialUnitTypes)eSpecialUnitType);
}

void CyGame::makeSpecialUnitValid(int /*SpecialUnitTypes*/ eSpecialUnitType)
{
	m_kGame.makeSpecialUnitValid((SpecialUnitTypes) eSpecialUnitType);
}

bool CyGame::isSpecialBuildingValid(int /*SpecialBuildingTypes*/ eIndex)
{
	return m_kGame.isSpecialBuildingValid((SpecialBuildingTypes)eIndex);
}

void CyGame::makeSpecialBuildingValid(int /*SpecialBuildingTypes*/ eIndex)
{
	m_kGame.makeSpecialBuildingValid((SpecialBuildingTypes) eIndex);
}

bool CyGame::isNukesValid()
{
	return m_kGame.isNukesValid();
}

void CyGame::makeNukesValid(bool bValid)
{
	m_kGame.makeNukesValid(bValid);
}

bool CyGame::isInAdvancedStart()
{
	return m_kGame.isInAdvancedStart();
}

CyCity* CyGame::getHolyCity(int /*ReligionTypes*/ eIndex)
{
	return new CyCity(m_kGame.getHolyCity((ReligionTypes) eIndex));
}

void CyGame::setHolyCity(int /*ReligionTypes*/ eIndex, CyCity* pNewValue, bool bAnnounce)
{
	m_kGame.setHolyCity((ReligionTypes) eIndex, pNewValue->getCity(), bAnnounce);
}

void CyGame::clearHolyCity(int /*ReligionTypes*/ eIndex)
{
	m_kGame.setHolyCity((ReligionTypes) eIndex, NULL, false);
}

CyCity* CyGame::getHeadquarters(int /*CorporationTypes*/ eIndex)
{
	return new CyCity(m_kGame.getHeadquarters((CorporationTypes) eIndex));
}

void CyGame::setHeadquarters(int /*CorporationTypes*/ eIndex, CyCity* pNewValue, bool bAnnounce)
{
	m_kGame.setHeadquarters((CorporationTypes) eIndex, pNewValue->getCity(), bAnnounce);
}

void CyGame::clearHeadquarters(int /*CorporationTypes*/ eIndex)
{
	m_kGame.setHeadquarters((CorporationTypes) eIndex, NULL, false);
}

int CyGame::getPlayerVote(int /*PlayerTypes*/ eOwnerIndex, int iVoteId)
{
	return m_kGame.getPlayerVote((PlayerTypes) eOwnerIndex, iVoteId);
}

std::string CyGame::getScriptData() const
{
	return m_kGame.getScriptData();
}

void CyGame::setScriptData(std::string szNewValue)
{
	m_kGame.setScriptData(szNewValue);
}

void CyGame::setName(TCHAR* szNewValue)
{
	m_kGame.setName(szNewValue);
}

std::wstring CyGame::getName()
{
	return m_kGame.getName();
}

int CyGame::getIndexAfterLastDeal()
{
	return m_kGame.getIndexAfterLastDeal();
}

int CyGame::getNumDeals()
{
	return m_kGame.getNumDeals();
}

CyDeal* CyGame::getDeal(int iID)
{
	return new CyDeal(m_kGame.getDeal(iID));
}

CyDeal* CyGame::addDeal()
{
	return new CyDeal(m_kGame.addDeal());
}

void CyGame::deleteDeal(int iID)
{
	m_kGame.deleteDeal(iID);
}

CvRandom& CyGame::getMapRand()
{
	return m_kGame.getMapRand();
}

int CyGame::getMapRandNum(int iNum, TCHAR* pszLog)
{
	return m_kGame.getMapRandNum(iNum, pszLog);
}

CvRandom& CyGame::getSorenRand()
{
	return m_kGame.getSorenRand();
}

int CyGame::getSorenRandNum(int iNum, TCHAR* pszLog)
{
	return m_kGame.getSorenRandNum(iNum, pszLog);
}

int CyGame::calculateSyncChecksum()
{
	return m_kGame.calculateSyncChecksum();
}

int CyGame::calculateOptionsChecksum()
{
	return m_kGame.calculateOptionsChecksum();
}

// JS - can't access protected member declared in class CvGame

bool CyGame::GetWorldBuilderMode() const				// remove once CvApp is exposed
{
	return gDLL->GetWorldBuilderMode();
}

bool CyGame::isPitbossHost() const				// remove once CvApp is exposed
{
	return gDLL->IsPitbossHost();
}

int CyGame::getCurrentLanguage() const				// remove once CvApp is exposed
{
	return gDLL->getCurrentLanguage();
}

void CyGame::setCurrentLanguage(int iNewLanguage)			// remove once CvApp is exposed
{
	gDLL->setCurrentLanguage(iNewLanguage);
}

int CyGame::getReplayMessageTurn(int i) const
{
	return m_kGame.getReplayMessageTurn(i);
}

ReplayMessageTypes CyGame::getReplayMessageType(int i) const
{
	return m_kGame.getReplayMessageType(i);
}

int CyGame::getReplayMessagePlotX(int i) const
{
	return m_kGame.getReplayMessagePlotX(i);
}

int CyGame::getReplayMessagePlotY(int i) const
{
	return m_kGame.getReplayMessagePlotY(i);
}

int CyGame::getReplayMessagePlayer(int i) const
{
	return m_kGame.getReplayMessagePlayer(i);
}

ColorTypes CyGame::getReplayMessageColor(int i) const
{
	return m_kGame.getReplayMessageColor(i);
}

std::wstring CyGame::getReplayMessageText(int i) const
{
	return m_kGame.getReplayMessageText(i);
}

uint CyGame::getNumReplayMessages() const
{
	return m_kGame.getNumReplayMessages();
}

CyReplayInfo* CyGame::getReplayInfo() const
{
	return new CyReplayInfo(m_kGame.getReplayInfo());
}

bool CyGame::hasSkippedSaveChecksum() const
{
	return m_kGame.hasSkippedSaveChecksum();
}

void CyGame::saveReplay(int iPlayer)
{
	m_kGame.saveReplay((PlayerTypes)iPlayer);
}

void CyGame::addPlayer(int eNewPlayer, int eLeader, int eCiv, int iBirthTurn, bool bAlive, bool bMinor)
{
	m_kGame.addPlayer((PlayerTypes)eNewPlayer, (LeaderHeadTypes)eLeader, (CivilizationTypes)eCiv, iBirthTurn, bAlive, bMinor);
	/*  <advc.104r> Only relevant for mod-mods (e.g. Barbarian Civ, PlatyBuilder).
		Colonial vassals are handled by CvPlayer::splitEmpire instead. */
	if(getUWAI().isEnabled())
		getUWAI().processNewPlayerInGame((PlayerTypes)eNewPlayer); // </advc.104r>
}

// BETTER_BTS_AI_MOD, Debug, 8/1/08, jdog5000: START
void CyGame::changeHumanPlayer(int /*PlayerTypes*/ eNewHuman)
{
	m_kGame.changeHumanPlayer((PlayerTypes)eNewHuman);
} // BETTER_BTS_AI_MOD: END


int CyGame::getCultureThreshold(int eLevel)
{
	return m_kGame.getCultureThreshold((CultureLevelTypes) eLevel);
}

/*	<advc.enum> These three are preserved for compatibility in mods;
	they're deprecated in favor of homonymous CyMap functions. */
int CyGame::getPlotExtraYield(int iX, int iY, int eYield) // K-Mod
{
	CvPlot const* pPlot = GC.getMap().plot(iX, iY);
	if (pPlot == NULL)
		return 0;
	return GC.getMap().getPlotExtraYield(*pPlot, (YieldTypes)eYield);
}

void CyGame::setPlotExtraYield(int iX, int iY, int eYield, int iExtraYield)
{
	CvPlot* pPlot = GC.getMap().plot(iX, iY);
	if (pPlot == NULL)
		return;
	GC.getMap().setPlotExtraYield(*pPlot, (YieldTypes)eYield, iExtraYield);
}

void CyGame::changePlotExtraCost(int iX, int iY, int iCost)
{
	CvPlot* pPlot = GC.getMap().plot(iX, iY);
	if (pPlot == NULL)
		return;
	GC.getMap().changePlotExtraCost(*pPlot, iCost);
} // </advc.enum>

bool CyGame::isCivEverActive(int /*CivilizationTypes*/ eCivilization)
{
	return m_kGame.isCivEverActive((CivilizationTypes)eCivilization);
}

bool CyGame::isLeaderEverActive(int /*LeaderHeadTypes*/ eLeader)
{
	return m_kGame.isLeaderEverActive((LeaderHeadTypes)eLeader);
}

bool CyGame::isUnitEverActive(int /*UnitTypes*/ eUnit)
{
	return m_kGame.isUnitEverActive((UnitTypes)eUnit);
}

bool CyGame::isBuildingEverActive(int /*BuildingTypes*/ eBuilding)
{
	return m_kGame.isBuildingEverActive((BuildingTypes)eBuilding);
}

bool CyGame::isEventActive(int /*EventTriggerTypes*/ eTrigger)
{
	return m_kGame.isEventActive((EventTriggerTypes)eTrigger);
}

void CyGame::doControl(int iControl)
{
	m_kGame.doControl((ControlTypes) iControl);
}
// advc.095:
void CyGame::setCityBarWidth(bool bWide)
{
	m_kGame.setCityBarWidth(bWide);
}
// BULL - AutoSave:
void CyGame::saveGame(std::string szFileName)
{
	// <advc> The BULL code had instead cast szFileName to a CvString&
	static CvString szTmp;
	szTmp = szFileName; // </advc>
	gDLL->getEngineIFace()->SaveGame(szTmp, SAVEGAME_NORMAL);
}
// advc.104:
bool CyGame::useKModAI()
{
	return !getUWAI().isEnabled();
}
// advc.300:
int CyGame::getBarbarianStartTurn()
{
	return m_kGame.getBarbarianStartTurn();
}
// advc.250b:
std::wstring CyGame::SPaHPointsForSettingsScreen()
{
	std::wstring* r = m_kGame.startPointsAsHandicap().forSettingsScreen();
	if(r == NULL)
		return L"";
	return *r;
}
// advc.250:
int CyGame::getDifficultyForEndScore()
{
	return m_kGame.getDifficultyForEndScore();
}
// <advc.703>
int CyGame::getMaxChapters()
{
	return m_kGame.getRiseFall().getMaxChapters();
}
int CyGame::getCurrentChapter()
{
	return m_kGame.getRiseFall().getCurrentChapter();
}
int CyGame::getChapterStart(int chapter)
{
	return m_kGame.getRiseFall().getChapter(chapter).getStartTurn();
}
int CyGame::getChapterEnd(int chapter)
{
	return m_kGame.getRiseFall().getChapter(chapter).getEndTurn();
}
int CyGame::getChapterScore(int chapter)
{
	return m_kGame.getRiseFall().getChapter(chapter).computeScore();
}
int CyGame::getChapterScoreTurn(int chapter)
{
	return m_kGame.getRiseFall().getChapter(chapter).getScoreTurn();
}
int CyGame::getChapterCiv(int chapter)
{
	return m_kGame.getRiseFall().getChapter(chapter).getCiv();
}
std::wstring CyGame::chapterScoreBreakdown()
{
	std::wstring* r = m_kGame.getRiseFall().chapterScoreBreakdown();
	if(r == NULL)
		return L"";
	return *r;
}
std::wstring CyGame::riseScoreBreakdown()
{
	std::wstring* r = m_kGame.getRiseFall().riseScoreBreakdown();
	if(r == NULL)
		return L"";
	return *r;
} // </advc.703>
// <advc.706>
bool CyGame::isRFInterlude()
{
	return (m_kGame.isOption(GAMEOPTION_RISE_FALL) &&
			m_kGame.getRiseFall().getInterludeCountdown() >= 0);
}
bool CyGame::isRFBlockPopups()
{
	return (m_kGame.isOption(GAMEOPTION_RISE_FALL) &&
			m_kGame.getRiseFall().isBlockPopups());
} // </advc.706>
// advc.004m:
void CyGame::reportCurrentLayer(int iLayer)
{
	m_kGame.reportCurrentLayer((GlobeLayerTypes)iLayer);
}
// advc.190c:
bool CyGame::isCivLeaderSetupKnown()
{
	return GC.getInitCore().isCivLeaderSetupKnown();
}
// advc.052:
bool CyGame::isScenario()
{
	return m_kGame.isScenario();
}

// doc
bool CyGame::isNeighbors(int ePlayer1, int ePlayer2)
{
	return m_pGame ? m_pGame->isNeighbors((PlayerTypes)ePlayer1, (PlayerTypes)ePlayer2) : false;
}

// doc
int CyGame::determineWinner(int eTeam1, int eTeam2)
{
	return m_pGame ? m_pGame->determineWinner((TeamTypes)eTeam1, (TeamTypes)eTeam2) : eTeam1;
}

// doc
int CyGame::getXResolution() const
{
	return m_pGame ? m_pGame->getXResolution() : -1;
}

// doc
void CyGame::setXResolution(int iNewValue)
{
	if (m_pGame) m_pGame->setXResolution(iNewValue);
}

// doc
void CyGame::changeXResolution(int iChange)
{
	if (m_pGame) m_pGame->changeXResolution(iChange);
}

// doc
int CyGame::getYResolution() const
{
	return m_pGame ? m_pGame->getYResolution() : -1;
}

// doc
void CyGame::setYResolution(int iNewValue)
{
	if (m_pGame) m_pGame->setYResolution(iNewValue);
}

// doc
void CyGame::changeYResolution(int iChange)
{
	if (m_pGame) m_pGame->changeYResolution(iChange);
}

// doc
void CyGame::addGreatPersonBornName(std::wstring sName)
{
	if (m_pGame) m_pGame->addGreatPersonBornName(sName);
}

// doc
bool CyGame::isGreatPersonBorn(std::wstring sName)
{
	return m_pGame ? m_pGame->isGreatPersonBorn(CvWString(sName)) : false;
}

// doc
void CyGame::autosave()
{
	if (m_pGame) m_pGame->autosave();
}

// doc
void CyGame::initialSave()
{
	if (m_pGame) m_pGame->autosave(true);
}

// doc
void CyGame::incrementBuildingClassCreatedCount(int iBuildingClass)
{
	if (m_pGame) m_pGame->incrementBuildingClassCreatedCount((BuildingClassTypes)iBuildingClass);
}

// doc
void CyGame::setCityScreenOwner(int iPlayer)
{
	if (m_pGame) m_pGame->setCityScreenOwner((PlayerTypes)iPlayer);
}

// doc
void CyGame::resetCityScreenOwner()
{
	if (m_pGame) m_pGame->resetCityScreenOwner();
}

// doc
void CyGame::setGreatPeopleNotifications(int iNotificationLevel)
{
	if (m_pGame) m_pGame->setGreatPeopleNotifications((NotificationLevels)iNotificationLevel);
}

// doc
void CyGame::setReligionSpreadNotifications(int iNotificationLevel)
{
	if (m_pGame) m_pGame->setReligionSpreadNotifications((NotificationLevels)iNotificationLevel);
}

// doc
void CyGame::setEventEffectNotifications(int iNotificationLevel)
{
	if (m_pGame) m_pGame->setEventEffectNotifications((NotificationLevels)iNotificationLevel);
}

// doc
int CyGame::getPeriod(int iCivilization)
{
	return m_pGame ? m_pGame->getPeriod((CivilizationTypes)iCivilization) : -1;
}

// doc
void CyGame::setPeriod(int iCivilization, int iPeriod)
{
	if (m_pGame) m_pGame->setPeriod((CivilizationTypes)iCivilization, (PeriodTypes)iPeriod);
}

// doc
int CyGame::getCivilizationHistory(int iHistoryType, int iCivilization, int iTurn)
{
	return m_pGame ? m_pGame->getCivilizationHistory((HistoryTypes)iHistoryType, (CivilizationTypes)iCivilization, iTurn) : -1;
}

// doc
int CyGame::getFirstDiscovered(int iTech)
{
	return m_pGame ? m_pGame->getFirstDiscovered((TechTypes)iTech) : -1;
}

// doc
int CyGame::getFirstDiscoveredTurn(int iTech)
{
	return m_pGame ? m_pGame->getFirstDiscoveredTurn((TechTypes)iTech) : -1;
}

// doc
int CyGame::getMedianTechValue()
{
	return m_pGame ? m_pGame->getMedianTechValue() : -1;
}
