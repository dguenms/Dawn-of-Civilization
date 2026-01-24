#pragma once

#ifndef CyGame_h
#define CyGame_h
//
// Python wrapper class for CvGame 
// SINGLETON
// updated 6-5

//#include "CvEnums.h"

class CvGame;
class CvGameAI;
class CyCity;
class CvRandom;
class CyDeal;
class CyReplayInfo;
class CyPlot;

class CyGame
{
public:
	CyGame();
	CyGame(CvGame* pGame);			// Call from C++
	CyGame(CvGameAI* pGame);			// Call from C++;
	CvGame* getGame() { return m_pGame;	}	// Call from C++
	bool isNone() { return (m_pGame==NULL); }

	void updateScore(bool bForce);
	void cycleCities(bool bForward, bool bAdd);
	void cycleSelectionGroups(bool bClear, bool bForward, bool bWorkers);
	bool cyclePlotUnits(CyPlot* pPlot, bool bForward, bool bAuto, int iCount);

	void selectionListMove(CyPlot* pPlot, bool bAlt, bool bShift, bool bCtrl);
	void selectionListGameNetMessage(int eMessage, int iData2, int iData3, int iData4, int iFlags, bool bAlt, bool bShift);
	void selectedCitiesGameNetMessage(int eMessage, int iData2, int iData3, int iData4, bool bOption, bool bAlt, bool bShift, bool bCtrl);
	void cityPushOrder(CyCity* pCity, OrderTypes eOrder, int iData, bool bAlt, bool bShift, bool bCtrl);

	int getSymbolID(int iSymbol);

	int getProductionPerPopulation(int /*HurryTypes*/ eHurry);

	int getAdjustedPopulationPercent(int /*VictoryTypes*/ eVictory);
	int getAdjustedLandPercent(int /* VictoryTypes*/ eVictory);

	bool isTeamVote(int /*VoteTypes*/ eVote) const;
	bool isChooseElection(int /*VoteTypes*/ eVote) const;
	bool isTeamVoteEligible(int /*TeamTypes*/ eTeam, int /*VoteSourceTypes*/ eVoteSource) const;
	int countPossibleVote(int /*VoteTypes*/ eVote, int /*VoteSourceTypes*/ eVoteSource) const;
	int getVoteRequired(int /*VoteTypes*/ eVote, int /*VoteSourceTypes*/ eVoteSource) const;
	int getSecretaryGeneral(int /*VoteSourceTypes*/ eVoteSource) const;
	bool canHaveSecretaryGeneral(int /*VoteSourceTypes*/ eVoteSource) const;
	int getVoteSourceReligion(int /*VoteSourceTypes*/ eVoteSource) const;
	void setVoteSourceReligion(int /*VoteSourceTypes*/ eVoteSource, int /*ReligionTypes*/ eReligion, bool bAnnounce);

	int countCivPlayersAlive();
	int countCivPlayersEverAlive();
	int countCivTeamsAlive();
	int countCivTeamsEverAlive();
	int countHumanPlayersAlive();

	int countTotalCivPower();
	int countTotalNukeUnits();
	int countKnownTechNumTeams(int /*TechTypes*/ eTech);
	int getNumFreeBonuses(int /*BuildingTypes*/ eBuilding);

	int countReligionLevels(int /*ReligionTypes*/ eReligion);	
	int calculateReligionPercent(int /* ReligionTypes*/ eReligion);
	int countCorporationLevels(int /*CorporationTypes*/ eCorporation);	

	int goldenAgeLength();
	int victoryDelay(int /*VictoryTypes*/ eVictory);
	int getImprovementUpgradeTime(int /* ImprovementTypes*/ eImprovement);
	bool canTrainNukes();

	int /* EraTypes */ getCurrentEra();

	int getActiveTeam();
	int /* CivilizationTypes */ getActiveCivilizationType();
	bool isNetworkMultiPlayer();
	bool isGameMultiPlayer();
	bool isTeamGame();

	bool isModem();
	void setModem(bool bModem);

	void reviveActivePlayer();

	int getNumHumanPlayers();
	int getGameTurn();
	void setGameTurn(int iNewValue);
	int getTurnYear(int iGameTurn);
	int getGameTurnYear();
	
	int getElapsedGameTurns();
	int getMaxTurns() const;
	void setMaxTurns(int iNewValue);
	void changeMaxTurns(int iChange);
	int getMaxCityElimination() const;
	void setMaxCityElimination(int iNewValue);
	int getNumAdvancedStartPoints() const;
	void setNumAdvancedStartPoints(int iNewValue);
	int getStartTurn() const;
	int getStartYear() const;
	void setStartYear(int iNewValue);
	int getEstimateEndTurn() const;
	void setEstimateEndTurn(int iNewValue);
	int getTurnSlice() const;
	int getMinutesPlayed() const;
	int getTargetScore() const;
	void setTargetScore(int iNewValue);

	int getNumGameTurnActive();
	int countNumHumanGameTurnActive();
	int getNumCities();
	int getNumCivCities();
	int getTotalPopulation();

	int getTradeRoutes() const;
	void changeTradeRoutes(int iChange);
	int getFreeTradeCount() const;
	bool isFreeTrade() const;
	void changeFreeTradeCount(int iChange);
	int getNoNukesCount() const;
	bool isNoNukes() const;
	void changeNoNukesCount(int iChange);
	int getSecretaryGeneralTimer(int iVoteSource) const;
	int getVoteTimer(int iVoteSource) const;
	int getNukesExploded() const;
	void changeNukesExploded(int iChange);

	int getMaxPopulation() const;
	int getMaxLand() const;
	int getMaxTech() const;
	int getMaxWonders() const;
	int getInitPopulation() const;
	int getInitLand() const;
	int getInitTech() const;
	int getInitWonders() const;

	int getAIAutoPlay() const;
	void setAIAutoPlay(int iNewValue);

	bool isScoreDirty() const;
	void setScoreDirty(bool bNewValue);
	bool isCircumnavigated() const;
	void makeCircumnavigated();
	bool isDiploVote(int /*VoteSourceTypes*/ eVoteSource) const;
	void changeDiploVote(int /*VoteSourceTypes*/ eVoteSource, int iChange);
	bool isDebugMode() const;
	void toggleDebugMode();

	int getPitbossTurnTime();
	void setPitbossTurnTime(int iHours);
	bool isHotSeat();
	bool isPbem();
	bool isPitboss();
	bool isSimultaneousTeamTurns();

	bool isFinalInitialized();

	int /*PlayerTypes*/ getActivePlayer();
	void setActivePlayer(int /*PlayerTypes*/ eNewValue, bool bForceHotSeat);
	int getPausePlayer();
	bool isPaused();
	int /*UnitTypes*/ getBestLandUnit();
	int getBestLandUnitCombat();
	
	int /*TeamTypes*/ getWinner();
	int /*VictoryTypes*/ getVictory();
	void setWinner(int /*TeamTypes*/ eNewWinner, int /*VictoryTypes*/ eNewVictory);
	int /*GameStateTypes*/ getGameState();
	int /*HandicapTypes*/ getHandicapType();
	CalendarTypes getCalendar() const;
	int /*EraTypes*/ getStartEra();
	int /*GameSpeedTypes*/ getGameSpeedType();	
	/*PlayerTypes*/ int getRankPlayer(int iRank);
	int getPlayerRank(int /*PlayerTypes*/ iIndex);
	int getPlayerScore(int /*PlayerTypes*/ iIndex);
	int /*TeamTypes*/ getRankTeam(int iRank);
	int getTeamRank(int /*TeamTypes*/ iIndex);
	int getTeamScore(int /*TeamTypes*/ iIndex);
	bool isOption(int /*GameOptionTypes*/ eIndex);
	void setOption(int /*GameOptionTypes*/ eIndex, bool bEnabled);
	bool isMPOption(int /*MultiplayerOptionTypes*/ eIndex);
	bool isForcedControl(int /*ForceControlTypes*/ eIndex);
	int getUnitCreatedCount(int /*UnitTypes*/ eIndex);
	int getUnitClassCreatedCount(int /*UnitClassTypes*/ eIndex);
	bool isUnitClassMaxedOut(int /*UnitClassTypes*/ eIndex, int iExtra);
	int getBuildingClassCreatedCount(int /*BuildingClassTypes*/ eIndex);
	bool isBuildingClassMaxedOut(int /*BuildingClassTypes*/ eIndex, int iExtra);

	int getProjectCreatedCount(int /*ProjectTypes*/ eIndex);
	bool isProjectMaxedOut(int /*ProjectTypes*/ eIndex, int iExtra);

	int getForceCivicCount(int /*CivicTypes*/ eIndex);
	bool isForceCivic(int /*CivicTypes*/ eIndex);
	bool isForceCivicOption(int /*CivicOptionTypes*/ eCivicOption);

	int getVoteOutcome(int /*VoteTypes*/ eIndex);

	int getReligionGameTurnFounded(int /*ReligionTypes*/ eIndex);
	bool isReligionFounded(int /*ReligionTypes*/ eIndex);
	bool isReligionSlotTaken(int /*ReligionTypes*/ eIndex);
	int getCorporationGameTurnFounded(int /*CorporationTypes*/ eIndex);
	bool isCorporationFounded(int /*CorporationTypes*/ eIndex);
	bool isVotePassed(int /*VoteTypes*/ eIndex) const;
	bool isVictoryValid(int /*VictoryTypes*/ eIndex);
	bool isSpecialUnitValid(int /*SpecialUnitTypes*/ eSpecialUnitType);
	void makeSpecialUnitValid(int /*SpecialUnitTypes*/ eSpecialUnitType);
	bool isSpecialBuildingValid(int /*SpecialBuildingTypes*/ eIndex);
	void makeSpecialBuildingValid(int /*SpecialBuildingTypes*/ eIndex);
	bool isNukesValid();
	void makeNukesValid(bool bValid);
	bool isInAdvancedStart();

	CyCity* getHolyCity(int /*ReligionTypes*/ eIndex);
	void setHolyCity(int /*ReligionTypes*/ eIndex, CyCity* pNewValue, bool bAnnounce);
	void clearHolyCity(int /*ReligionTypes*/ eIndex);

	CyCity* getHeadquarters(int /*CorporationTypes*/ eIndex);
	void setHeadquarters(int /*CorporationTypes*/ eIndex, CyCity* pNewValue, bool bAnnounce);
	void clearHeadquarters(int /*CorporationTypes*/ eIndex);

	int getPlayerVote(int /*PlayerTypes*/ eOwnerIndex, int iVoteId);

	std::string getScriptData() const;
	void setScriptData(std::string szNewValue);

	void setName(TCHAR* szName);
	std::wstring getName();
	int getIndexAfterLastDeal();
	int getNumDeals();
	CyDeal* getDeal(int iID);
	CyDeal* addDeal();
	void deleteDeal(int iID);
	CvRandom& getMapRand();
	int getMapRandNum(int iNum, TCHAR* pszLog);
	CvRandom& getSorenRand();
	int getSorenRandNum(int iNum, TCHAR* pszLog);
	int calculateSyncChecksum();
	int calculateOptionsChecksum();
	bool GetWorldBuilderMode() const;				// remove once CvApp is exposed
	bool isPitbossHost() const;				// remove once CvApp is exposed
	int getCurrentLanguage() const;				// remove once CvApp is exposed
	void setCurrentLanguage(int iNewLanguage);				// remove once CvApp is exposed

	int getReplayMessageTurn(int i) const;
	ReplayMessageTypes getReplayMessageType(int i) const;
	int getReplayMessagePlotX(int i) const;
	int getReplayMessagePlotY(int i) const;
	int getReplayMessagePlayer(int i) const;
	ColorTypes getReplayMessageColor(int i) const;
	std::wstring getReplayMessageText(int i) const;
	uint getNumReplayMessages() const;
	CyReplayInfo* getReplayInfo() const;
	bool hasSkippedSaveChecksum() const;

	void saveReplay(int iPlayer);

	void addPlayer(int /*PlayerTypes*/ eNewPlayer, int /*LeaderHeadTypes*/ eLeader, int /*CivilizationTypes*/ eCiv);
	int getCultureThreshold(int /*CultureLevelTypes*/ eLevel);
	void setPlotExtraYield(int iX, int iY, int /*YieldTypes*/ eYield, int iExtraYield);
	void changePlotExtraCost(int iX, int iY, int iExtraCost);
	
	bool isCivEverActive(int /*CivilizationTypes*/ eCivilization);
	bool isLeaderEverActive(int /*LeaderHeadTypes*/ eLeader);
	bool isUnitEverActive(int /*UnitTypes*/ eUnit);
	bool isBuildingEverActive(int /*BuildingTypes*/ eBuilding);

	bool isEventActive(int /*EventTriggerTypes*/ eTrigger);
	void doControl(int iControl);

protected:
	CvGame* m_pGame;
};

#endif	// #ifndef CyGame
