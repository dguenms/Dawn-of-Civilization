#pragma once

// game.h

#ifndef CIV4_GAME_H
#define CIV4_GAME_H

//#include "CvStructs.h"
#include "CvDeal.h"
#include "CvRandom.h"

class CvPlot;
class CvCity;
class CvReplayMessage;
class CvReplayInfo;

typedef std::vector<const CvReplayMessage*> ReplayMessageList;

class CvGame
{

public:

	DllExport CvGame();
	DllExport virtual ~CvGame();

	DllExport void init(HandicapTypes eHandicap);
	DllExport void reset(HandicapTypes eHandicap, bool bConstructorCall = false);

protected:

	void uninit();

public:

	DllExport void setInitialItems();
	DllExport void regenerateMap();

	DllExport void initDiplomacy();
	DllExport void initFreeState();
	DllExport void initFreeUnits();

	DllExport void assignStartingPlots();
	DllExport void normalizeStartingPlots();

	DllExport void update();
	DllExport void updateScore(bool bForce = false);

	DllExport void updateColoredPlots();
	DllExport void updateBlockadedPlots();

	DllExport void updatePlotGroups();
	DllExport void updateBuildingCommerce();
	DllExport void updateCitySight(bool bIncrement);
	DllExport void updateTradeRoutes();

	DllExport void updateSelectionList();
	DllExport void updateTestEndTurn();

	DllExport void testExtendedGame();

	DllExport CvUnit* getPlotUnit(const CvPlot* pPlot, int iIndex) const;
	DllExport void getPlotUnits(const CvPlot *pPlot, std::vector<CvUnit*>& plotUnits) const;

	DllExport void cycleCities(bool bForward = true, bool bAdd = false) const;																				// Exposed to Python
	DllExport void cycleSelectionGroups(bool bClear, bool bForward = true, bool bWorkers = false) const;							// Exposed to Python
	DllExport bool cyclePlotUnits(CvPlot* pPlot, bool bForward = true, bool bAuto = false, int iCount = -1) const;		// Exposed to Python
	DllExport bool selectCity(CvCity* pSelectCity, bool bCtrl, bool bAlt, bool bShift) const;

	DllExport void selectionListMove(CvPlot* pPlot, bool bAlt, bool bShift, bool bCtrl) const;												// Exposed to Python
	DllExport void selectionListGameNetMessage(int eMessage, int iData2 = -1, int iData3 = -1, int iData4 = -1, int iFlags = 0, bool bAlt = false, bool bShift = false) const;	// Exposed to Python
	DllExport void selectedCitiesGameNetMessage(int eMessage, int iData2 = -1, int iData3 = -1, int iData4 = -1, bool bOption = false, bool bAlt = false, bool bShift = false, bool bCtrl = false) const;	// Exposed to Python
	DllExport void cityPushOrder(CvCity* pCity, OrderTypes eOrder, int iData, bool bAlt = false, bool bShift = false, bool bCtrl = false) const;	// Exposed to Python

	DllExport void selectUnit(CvUnit* pUnit, bool bClear, bool bToggle = false, bool bSound = false) const;
	DllExport void selectGroup(CvUnit* pUnit, bool bShift, bool bCtrl, bool bAlt) const;
	DllExport void selectAll(CvPlot* pPlot) const;

	DllExport bool selectionListIgnoreBuildingDefense() const;

	DllExport bool canHandleAction(int iAction, CvPlot* pPlot = NULL, bool bTestVisible = false, bool bUseCache = false) const;
	DllExport void setupActionCache() const;
	DllExport void handleAction(int iAction);

	bool canDoControl(ControlTypes eControl) const;
	void doControl(ControlTypes eControl);

	DllExport void implementDeal(PlayerTypes eWho, PlayerTypes eOtherWho, CLinkList<TradeData>* pOurList, CLinkList<TradeData>* pTheirList, bool bForce = false);
	void verifyDeals();

	DllExport void getGlobeviewConfigurationParameters(TeamTypes eTeam, bool& bStarsVisible, bool& bWorldIsRound);

	DllExport int getSymbolID(int iSymbol);																	// Exposed to Python

	int getProductionPerPopulation(HurryTypes eHurry);											// Exposed to Python

	int getAdjustedPopulationPercent(VictoryTypes eVictory) const;								// Exposed to Python
	int getAdjustedLandPercent(VictoryTypes eVictory) const;											// Exposed to Python

	bool isTeamVote(VoteTypes eVote) const;												// Exposed to Python
	bool isChooseElection(VoteTypes eVote) const;									// Exposed to Python
	bool isTeamVoteEligible(TeamTypes eTeam, VoteSourceTypes eVoteSource) const;								// Exposed to Python
	int countVote(const VoteTriggeredData& kData, PlayerVoteTypes eChoice) const;
	int countPossibleVote(VoteTypes eVote, VoteSourceTypes eVoteSource) const;																// Exposed to Python
	TeamTypes findHighestVoteTeam(const VoteTriggeredData& kData) const;
	int getVoteRequired(VoteTypes eVote, VoteSourceTypes eVoteSource) const;										// Exposed to Python
	TeamTypes getSecretaryGeneral(VoteSourceTypes eVoteSource) const;												// Exposed to Python
	bool canHaveSecretaryGeneral(VoteSourceTypes eVoteSource) const;												// Exposed to Python
	void clearSecretaryGeneral(VoteSourceTypes eVoteSource);
	void updateSecretaryGeneral();

	DllExport int countCivPlayersAlive() const;																		// Exposed to Python
	DllExport int countCivPlayersEverAlive() const;																// Exposed to Python
	DllExport int countCivTeamsAlive() const;																			// Exposed to Python
	DllExport int countCivTeamsEverAlive() const;																	// Exposed to Python
	DllExport int countHumanPlayersAlive() const;																	// Exposed to Python

	int countTotalCivPower();																								// Exposed to Python
	int countTotalNukeUnits();																							// Exposed to Python
	int countKnownTechNumTeams(TechTypes eTech);														// Exposed to Python
	int getNumFreeBonuses(BuildingTypes eBuilding);													// Exposed to Python

	int countReligionLevels(ReligionTypes eReligion);							// Exposed to Python 
	int calculateReligionPercent(ReligionTypes eReligion) const;				// Exposed to Python
	int countCorporationLevels(CorporationTypes eCorporation);							// Exposed to Python 
	void replaceCorporation(CorporationTypes eCorporation1, CorporationTypes eCorporation2);

	int goldenAgeLength() const;																					// Exposed to Python
	int victoryDelay(VictoryTypes eVictory) const;							// Exposed to Python
	int getImprovementUpgradeTime(ImprovementTypes eImprovement) const;		// Exposed to Python

	bool canTrainNukes() const;																		// Exposed to Python
	DllExport EraTypes getCurrentEra() const;											// Exposed to Python

	DllExport TeamTypes getActiveTeam() const;																		// Exposed to Python
	DllExport CivilizationTypes getActiveCivilizationType() const;								// Exposed to Python

	DllExport bool isNetworkMultiPlayer() const;																	// Exposed to Python
	DllExport bool isGameMultiPlayer() const;																			// Exposed to Python
	DllExport bool isTeamGame() const;																						// Exposed to Python

	bool isModem();
	void setModem(bool bModem);

	DllExport void reviveActivePlayer();																		// Exposed to Python

	DllExport int getNumHumanPlayers();																			// Exposed to Python

	DllExport int getGameTurn();																						// Exposed to Python
	DllExport void setGameTurn(int iNewValue);															// Exposed to Python
	void incrementGameTurn();
	int getTurnYear(int iGameTurn);																// Exposed to Python
	int getGameTurnYear();																				// Exposed to Python

	int getElapsedGameTurns() const;																		// Exposed to Python
	void incrementElapsedGameTurns();

	int getMaxTurns() const;																			// Exposed to Python
	DllExport void setMaxTurns(int iNewValue);															// Exposed to Python
	void changeMaxTurns(int iChange);															// Exposed to Python

	DllExport int getMaxCityElimination() const;														// Exposed to Python
	DllExport void setMaxCityElimination(int iNewValue);										// Exposed to Python

	DllExport int getNumAdvancedStartPoints() const;														// Exposed to Python
	DllExport void setNumAdvancedStartPoints(int iNewValue);										// Exposed to Python

	DllExport int getStartTurn() const;																			// Exposed to Python
	DllExport void setStartTurn(int iNewValue);

	int getStartYear() const;																			// Exposed to Python
	void setStartYear(int iNewValue);															// Exposed to Python

	int getEstimateEndTurn() const;																// Exposed to Python
	void setEstimateEndTurn(int iNewValue);												// Exposed to Python

	DllExport int getTurnSlice() const;																			// Exposed to Python
	int getMinutesPlayed() const;																	// Exposed to Python
	void setTurnSlice(int iNewValue);
	void changeTurnSlice(int iChange);

	int getCutoffSlice() const;
	void setCutoffSlice(int iNewValue);
	void changeCutoffSlice(int iChange);

	DllExport int getTurnSlicesRemaining();
	void resetTurnTimer();
	void incrementTurnTimer(int iNumTurnSlices);
	DllExport int getMaxTurnLen();

	int getTargetScore() const;																		// Exposed to Python
	DllExport void setTargetScore(int iNewValue);														// Exposed to Python

	int getNumGameTurnActive();																		// Exposed to Python
	DllExport int countNumHumanGameTurnActive() const;														// Exposed to Python
	void changeNumGameTurnActive(int iChange);

	DllExport int getNumCities() const;																						// Exposed to Python
	int getNumCivCities() const;																				// Exposed to Python
	void changeNumCities(int iChange);

	DllExport int getTotalPopulation() const;																// Exposed to Python
	void changeTotalPopulation(int iChange);

	int getTradeRoutes() const;																		// Exposed to Python
	void changeTradeRoutes(int iChange);													// Exposed to Python

	int getFreeTradeCount() const;																// Exposed to Python
	bool isFreeTrade() const;																			// Exposed to Python
	void changeFreeTradeCount(int iChange);												// Exposed to Python

	int getNoNukesCount() const;																	// Exposed to Python
	bool isNoNukes() const;																				// Exposed to Python
	void changeNoNukesCount(int iChange);													// Exposed to Python

	int getSecretaryGeneralTimer(VoteSourceTypes eVoteSource) const;													// Exposed to Python
	void setSecretaryGeneralTimer(VoteSourceTypes eVoteSource, int iNewValue);
	void changeSecretaryGeneralTimer(VoteSourceTypes eVoteSource, int iChange);

	int getVoteTimer(VoteSourceTypes eVoteSource) const;													// Exposed to Python
	void setVoteTimer(VoteSourceTypes eVoteSource, int iNewValue);
	void changeVoteTimer(VoteSourceTypes eVoteSource, int iChange);

	int getNukesExploded() const;																	// Exposed to Python
	void changeNukesExploded(int iChange);												// Exposed to Python

	int getMaxPopulation() const;																	// Exposed to Python
	int getMaxLand() const;																				// Exposed to Python
	int getMaxTech() const;																				// Exposed to Python
	int getMaxWonders() const;																		// Exposed to Python
	int getInitPopulation() const;																// Exposed to Python
	int getInitLand() const;																			// Exposed to Python
	int getInitTech() const;																			// Exposed to Python
	int getInitWonders() const;																		// Exposed to Python
	DllExport void initScoreCalculation();

	int getAIAutoPlay();																				// Exposed to Python
	DllExport void setAIAutoPlay(int iNewValue);																// Exposed to Python
	void changeAIAutoPlay(int iChange);

	DllExport unsigned int getInitialTime();
	DllExport void setInitialTime(unsigned int uiNewValue);

	bool isScoreDirty() const;																							// Exposed to Python
	void setScoreDirty(bool bNewValue);																			// Exposed to Python

	bool isCircumnavigated() const;																// Exposed to Python
	void makeCircumnavigated();																		// Exposed to Python
	bool circumnavigationAvailable() const;

	bool isDiploVote(VoteSourceTypes eVoteSource) const;																			// Exposed to Python
	int getDiploVoteCount(VoteSourceTypes eVoteSource) const;
	void changeDiploVote(VoteSourceTypes eVoteSource, int iChange);																					// Exposed to Python
	bool canDoResolution(VoteSourceTypes eVoteSource, const VoteSelectionSubData& kData) const;
	bool isValidVoteSelection(VoteSourceTypes eVoteSource, const VoteSelectionSubData& kData) const;

	DllExport bool isDebugMode() const;																			// Exposed to Python
	DllExport void toggleDebugMode();																				// Exposed to Python
	DllExport void updateDebugModeCache();

	DllExport int getPitbossTurnTime() const;																			// Exposed to Python
	DllExport void setPitbossTurnTime(int iHours);																			// Exposed to Python

	DllExport bool isHotSeat() const;																							// Exposed to Python
	DllExport bool isPbem() const;																								// Exposed to Python
	DllExport bool isPitboss() const;																							// Exposed to Python
	DllExport bool isSimultaneousTeamTurns() const;																							// Exposed to Python

	DllExport bool isFinalInitialized() const;																		// Exposed to Python
	DllExport void setFinalInitialized(bool bNewValue);

	bool getPbemTurnSent() const;
	DllExport void setPbemTurnSent(bool bNewValue);

	DllExport bool getHotPbemBetweenTurns() const;
	DllExport void setHotPbemBetweenTurns(bool bNewValue);

	DllExport bool isPlayerOptionsSent() const;
	DllExport void sendPlayerOptions(bool bForce = false);

	DllExport PlayerTypes getActivePlayer() const;																				// Exposed to Python
	DllExport void setActivePlayer(PlayerTypes eNewValue, bool bForceHotSeat = false);		// Exposed to Python
	DllExport void updateUnitEnemyGlow();

	DllExport HandicapTypes getHandicapType() const;
	DllExport void setHandicapType(HandicapTypes eHandicap);

	DllExport PlayerTypes getPausePlayer() const;																			// Exposed to Python
	DllExport bool isPaused() const;																									// Exposed to Python
	DllExport void setPausePlayer(PlayerTypes eNewValue);

	UnitTypes getBestLandUnit() const;																			// Exposed to Python
	int getBestLandUnitCombat() const;																			// Exposed to Python
	void setBestLandUnit(UnitTypes eNewValue);

	DllExport TeamTypes getWinner() const;																			// Exposed to Python
	DllExport VictoryTypes getVictory() const;																	// Exposed to Python
	void setWinner(TeamTypes eNewWinner, VictoryTypes eNewVictory);		// Exposed to Python

	DllExport GameStateTypes getGameState() const;																		// Exposed to Python
	DllExport void setGameState(GameStateTypes eNewValue);

	DllExport EraTypes getStartEra() const;																			// Exposed to Python

	DllExport CalendarTypes getCalendar() const;																// Exposed to Python

	DllExport GameSpeedTypes getGameSpeedType() const;													// Exposed to Python 

	PlayerTypes getRankPlayer(int iRank) const;															// Exposed to Python
	void setRankPlayer(int iRank, PlayerTypes ePlayer);

	int getPlayerRank(PlayerTypes ePlayer) const;														// Exposed to Python 
	void setPlayerRank(PlayerTypes ePlayer, int iRank);

	DllExport int getPlayerScore(PlayerTypes ePlayer) const;													// Exposed to Python
	void setPlayerScore(PlayerTypes ePlayer, int iScore);

	TeamTypes getRankTeam(int iRank) const;																	// Exposed to Python
	void setRankTeam(int iRank, TeamTypes eTeam);

	int getTeamRank(TeamTypes eTeam)const;																	// Exposed to Python
	void setTeamRank(TeamTypes eTeam, int iRank);

	DllExport int getTeamScore(TeamTypes eTeam) const;																// Exposed to Python
	void setTeamScore(TeamTypes eTeam, int iScore);

	DllExport bool isOption(GameOptionTypes eIndex) const;																// Exposed to Python
	DllExport void setOption(GameOptionTypes eIndex, bool bEnabled);

	DllExport bool isMPOption(MultiplayerOptionTypes eIndex) const;												// Exposed to Python
	DllExport void setMPOption(MultiplayerOptionTypes eIndex, bool bEnabled);

	DllExport bool isForcedControl(ForceControlTypes eIndex) const;												// Exposed to Python
	DllExport void setForceControl(ForceControlTypes eIndex, bool bEnabled);

	int getUnitCreatedCount(UnitTypes eIndex);																	// Exposed to Python
	void incrementUnitCreatedCount(UnitTypes eIndex);

	int getUnitClassCreatedCount(UnitClassTypes eIndex);												// Exposed to Python
	bool isUnitClassMaxedOut(UnitClassTypes eIndex, int iExtra = 0);						// Exposed to Python
	void incrementUnitClassCreatedCount(UnitClassTypes eIndex);

	int getBuildingClassCreatedCount(BuildingClassTypes eIndex);								// Exposed to Python
	bool isBuildingClassMaxedOut(BuildingClassTypes eIndex, int iExtra = 0);		// Exposed to Python
	void incrementBuildingClassCreatedCount(BuildingClassTypes eIndex);

	int getProjectCreatedCount(ProjectTypes eIndex);														// Exposed to Python
	bool isProjectMaxedOut(ProjectTypes eIndex, int iExtra = 0);								// Exposed to Python
	void incrementProjectCreatedCount(ProjectTypes eIndex, int iExtra = 1);

	int getForceCivicCount(CivicTypes eIndex) const;														// Exposed to Python
	bool isForceCivic(CivicTypes eIndex) const;																	// Exposed to Python
	bool isForceCivicOption(CivicOptionTypes eCivicOption) const;								// Exposed to Python
	void changeForceCivicCount(CivicTypes eIndex, int iChange);

	PlayerVoteTypes getVoteOutcome(VoteTypes eIndex) const;																	// Exposed to Python
	bool isVotePassed(VoteTypes eIndex) const;																	// Exposed to Python
	void setVoteOutcome(const VoteTriggeredData& kData, PlayerVoteTypes eNewValue);

	bool isVictoryValid(VictoryTypes eIndex) const;															// Exposed to Python
	void setVictoryValid(VictoryTypes eIndex, bool bValid);

	bool isSpecialUnitValid(SpecialUnitTypes eIndex);														// Exposed to Python  
	void makeSpecialUnitValid(SpecialUnitTypes eIndex);													// Exposed to Python

	bool isSpecialBuildingValid(SpecialBuildingTypes eIndex);										// Exposed to Python
	void makeSpecialBuildingValid(SpecialBuildingTypes eIndex, bool bAnnounce = false);									// Exposed to Python

	bool isNukesValid() const;														// Exposed to Python  
	void makeNukesValid(bool bValid = true);													// Exposed to Python

	bool isInAdvancedStart() const;														// Exposed to Python  

	DllExport void setVoteChosen(int iSelection, int iVoteId);

	int getReligionGameTurnFounded(ReligionTypes eIndex);												// Exposed to Python
	bool isReligionFounded(ReligionTypes eIndex);																// Exposed to Python
	void makeReligionFounded(ReligionTypes eIndex, PlayerTypes ePlayer);

	bool isReligionSlotTaken(ReligionTypes eReligion) const;											// Exposed to Python
	void setReligionSlotTaken(ReligionTypes eReligion, bool bTaken);

	CvCity* getHolyCity(ReligionTypes eIndex);																	// Exposed to Python
	void setHolyCity(ReligionTypes eIndex, CvCity* pNewValue, bool bAnnounce);	// Exposed to Python

	int getCorporationGameTurnFounded(CorporationTypes eIndex);												// Exposed to Python
	bool isCorporationFounded(CorporationTypes eIndex);																// Exposed to Python
	void makeCorporationFounded(CorporationTypes eIndex, PlayerTypes ePlayer);

	CvCity* getHeadquarters(CorporationTypes eIndex);																	// Exposed to Python
	void setHeadquarters(CorporationTypes eIndex, CvCity* pNewValue, bool bAnnounce);	// Exposed to Python

	PlayerVoteTypes getPlayerVote(PlayerTypes eOwnerIndex, int iVoteId) const;			// Exposed to Python
	void setPlayerVote(PlayerTypes eOwnerIndex, int iVoteId, PlayerVoteTypes eNewValue);
	DllExport void castVote(PlayerTypes eOwnerIndex, int iVoteId, PlayerVoteTypes ePlayerVote);

	DllExport const CvWString & getName();
	DllExport void setName(const TCHAR* szName);

	// Script data needs to be a narrow string for pickling in Python
	std::string getScriptData() const;																										// Exposed to Python	
	void setScriptData(std::string szNewValue);																						// Exposed to Python	
																																												
	bool isDestroyedCityName(CvWString& szName) const;													
	void addDestroyedCityName(const CvWString& szName);													
																																												
	bool isGreatPersonBorn(CvWString& szName) const;													
	void addGreatPersonBornName(const CvWString& szName);													

	DllExport int getIndexAfterLastDeal();																								// Exposed to Python	
	DllExport int getNumDeals();																													// Exposed to Python	
	DllExport CvDeal* getDeal(int iID);																										// Exposed to Python	
	DllExport CvDeal* addDeal();																													
	DllExport void deleteDeal(int iID);																										
	// iteration																																					
	DllExport CvDeal* firstDeal(int *pIterIdx, bool bRev=false);													// Exposed to Python									
	DllExport CvDeal* nextDeal(int *pIterIdx, bool bRev=false);														// Exposed to Python									

	VoteSelectionData* getVoteSelection(int iID) const;
	VoteSelectionData* addVoteSelection(VoteSourceTypes eVoteSource);
	void deleteVoteSelection(int iID);

	VoteTriggeredData* getVoteTriggered(int iID) const;
	VoteTriggeredData* addVoteTriggered(const VoteSelectionData& kData, int iChoice);
	VoteTriggeredData* addVoteTriggered(VoteSourceTypes eVoteSource, const VoteSelectionSubData& kOptionData);
	void deleteVoteTriggered(int iID);

	CvRandom& getMapRand();																											// Exposed to Python	
	int getMapRandNum(int iNum, const char* pszLog);														
																																												
	CvRandom& getSorenRand();																										// Exposed to Python	
	int getSorenRandNum(int iNum, const char* pszLog);													
																																												
	DllExport int calculateSyncChecksum();																								// Exposed to Python	
	DllExport int calculateOptionsChecksum();																							// Exposed to Python	

	void addReplayMessage(ReplayMessageTypes eType = NO_REPLAY_MESSAGE, PlayerTypes ePlayer = NO_PLAYER, CvWString pszText = L"", 
		int iPlotX = -1, int iPlotY = -1, ColorTypes eColor = NO_COLOR);
	void clearReplayMessageMap();
	int getReplayMessageTurn(uint i) const;
	ReplayMessageTypes getReplayMessageType(uint i) const;
	int getReplayMessagePlotX(uint i) const;
	int getReplayMessagePlotY(uint i) const;
	PlayerTypes getReplayMessagePlayer(uint i) const;
	LPCWSTR getReplayMessageText(uint i) const;
	uint getNumReplayMessages() const;
	ColorTypes getReplayMessageColor(uint i) const;

	DllExport virtual void read(FDataStreamBase* pStream);
	DllExport virtual void write(FDataStreamBase* pStream);
	DllExport virtual void writeReplay(FDataStreamBase& stream, PlayerTypes ePlayer);

	DllExport virtual void AI_init() = 0;
	DllExport virtual void AI_reset() = 0;
	DllExport virtual void AI_makeAssignWorkDirty() = 0;
	DllExport virtual void AI_updateAssignWork() = 0;
	DllExport virtual int AI_combatValue(UnitTypes eUnit) = 0;

	CvReplayInfo* getReplayInfo() const;
	DllExport void setReplayInfo(CvReplayInfo* pReplay);
	void saveReplay(PlayerTypes ePlayer);

	bool hasSkippedSaveChecksum() const;

	void addPlayer(PlayerTypes eNewPlayer, LeaderHeadTypes eLeader, CivilizationTypes eCiv);   // Exposed to Python

	bool testVictory(VictoryTypes eVictory, TeamTypes eTeam, bool* pbEndScore = NULL) const;

	bool isCompetingCorporation(CorporationTypes eCorporation1, CorporationTypes eCorporation2) const;

	int getShrineBuildingCount(ReligionTypes eReligion = NO_RELIGION);
	BuildingTypes getShrineBuilding(int eIndex, ReligionTypes eReligion = NO_RELIGION);
	void changeShrineBuilding(BuildingTypes eBuilding, ReligionTypes eReligion, bool bRemove = false);

	bool culturalVictoryValid();
	int culturalVictoryNumCultureCities();
	CultureLevelTypes culturalVictoryCultureLevel();
	int getCultureThreshold(CultureLevelTypes eLevel) const;

	int getPlotExtraYield(int iX, int iY, YieldTypes eYield) const;
	void setPlotExtraYield(int iX, int iY, YieldTypes eYield, int iCost);   // exposed to Python
	void removePlotExtraYield(int iX, int iY);

	int getPlotExtraCost(int iX, int iY) const;
	void changePlotExtraCost(int iX, int iY, int iCost);   // exposed to Python
	void removePlotExtraCost(int iX, int iY);

	ReligionTypes getVoteSourceReligion(VoteSourceTypes eVoteSource) const;      // Exposed to Python
	void setVoteSourceReligion(VoteSourceTypes eVoteSource, ReligionTypes eReligion, bool bAnnounce = false);      // Exposed to Python

	bool isEventActive(EventTriggerTypes eTrigger) const;    // exposed to Python
	DllExport void initEvents();

	bool isCivEverActive(CivilizationTypes eCivilization) const;      // Exposed to Python
	bool isLeaderEverActive(LeaderHeadTypes eLeader) const;		// Exposed to Python
	bool isUnitEverActive(UnitTypes eUnit) const;		// Exposed to Python
	bool isBuildingEverActive(BuildingTypes eBuilding) const;		// Exposed to Python

	void processBuilding(BuildingTypes eBuilding, int iChange);

	bool pythonIsBonusIgnoreLatitudes() const;

	DllExport void getGlobeLayers(std::vector<CvGlobeLayerData>& aLayers) const;
	DllExport void startFlyoutMenu(const CvPlot* pPlot, std::vector<CvFlyoutMenuData>& aFlyoutItems) const;
	DllExport void applyFlyoutMenu(const CvFlyoutMenuData& kItem);
	DllExport CvPlot* getNewHighlightPlot() const;
	DllExport ColorTypes getPlotHighlightColor(CvPlot* pPlot) const;
	DllExport void cheatSpaceship() const;
	DllExport VictoryTypes getSpaceVictory() const;
	DllExport void nextActivePlayer(bool bForward);

	DllExport DomainTypes getUnitDomain(UnitTypes eUnit) const;
	DllExport const CvArtInfoBuilding* getBuildingArtInfo(BuildingTypes eBuilding) const;
	DllExport bool isWaterBuilding(BuildingTypes eBuilding) const;
	DllExport CivilopediaWidgetShowTypes getWidgetShow(BonusTypes eBonus) const;
	DllExport CivilopediaWidgetShowTypes getWidgetShow(ImprovementTypes eImprovement) const;

	DllExport void loadBuildQueue(const CvString& strItem) const;

	DllExport int getNextSoundtrack(EraTypes eLastEra, int iLastSoundtrack) const;
	DllExport int getSoundtrackSpace() const;
	DllExport bool isSoundtrackOverride(CvString& strSoundtrack) const;

	DllExport void initSelection() const;
	DllExport bool canDoPing(CvPlot* pPlot, PlayerTypes ePlayer) const;
	DllExport bool shouldDisplayReturn() const;
	DllExport bool shouldDisplayEndTurn() const;
	DllExport bool shouldDisplayWaitingOthers() const;
	DllExport bool shouldDisplayWaitingYou() const;
	DllExport bool shouldDisplayEndTurnButton() const;
	DllExport bool shouldDisplayFlag() const;
	DllExport bool shouldDisplayUnitModel() const;
	DllExport bool shouldShowResearchButtons() const;
	DllExport bool shouldCenterMinimap() const;
	DllExport EndTurnButtonStates getEndTurnState() const;

	DllExport void handleCityScreenPlotPicked(CvCity* pCity, CvPlot* pPlot, bool bAlt, bool bShift, bool bCtrl) const;
	DllExport void handleCityScreenPlotDoublePicked(CvCity* pCity, CvPlot* pPlot, bool bAlt, bool bShift, bool bCtrl) const;
	DllExport void handleCityScreenPlotRightPicked(CvCity* pCity, CvPlot* pPlot, bool bAlt, bool bShift, bool bCtrl) const;
	DllExport void handleCityPlotRightPicked(CvCity* pCity, CvPlot* pPlot, bool bAlt, bool bShift, bool bCtrl) const;
	DllExport void handleMiddleMouse(bool bCtrl, bool bAlt, bool bShift);

	DllExport void handleDiplomacySetAIComment(DiploCommentTypes eComment) const;

protected:
	int m_iElapsedGameTurns;
	int m_iStartTurn;
	int m_iStartYear;
	int m_iEstimateEndTurn;
	int m_iTurnSlice;
	int m_iCutoffSlice;
	int m_iNumGameTurnActive;
	int m_iNumCities;
	int m_iTotalPopulation;
	int m_iTradeRoutes;
	int m_iFreeTradeCount;
	int m_iNoNukesCount;
	int m_iNukesExploded;
	int m_iMaxPopulation;
	int m_iMaxLand;
	int m_iMaxTech;
	int m_iMaxWonders;
	int m_iInitPopulation;
	int m_iInitLand;
	int m_iInitTech;
	int m_iInitWonders;
	int m_iAIAutoPlay;

	unsigned int m_uiInitialTime;

	bool m_bScoreDirty;
	bool m_bCircumnavigated;
	bool m_bDebugMode;
	bool m_bDebugModeCache;
	bool m_bFinalInitialized;
	bool m_bPbemTurnSent;
	bool m_bHotPbemBetweenTurns;
	bool m_bPlayerOptionsSent;
	bool m_bNukesValid;

	HandicapTypes m_eHandicap;
	PlayerTypes m_ePausePlayer;
	UnitTypes m_eBestLandUnit;
	TeamTypes m_eWinner;
	VictoryTypes m_eVictory;
	GameStateTypes m_eGameState;
	PlayerTypes m_eEventPlayer;

	CvString m_szScriptData;

	int* m_aiRankPlayer;        // Ordered by rank...
	int* m_aiPlayerRank;        // Ordered by player ID...
	int* m_aiPlayerScore;       // Ordered by player ID...
	int* m_aiRankTeam;						// Ordered by rank...
	int* m_aiTeamRank;						// Ordered by team ID...
	int* m_aiTeamScore;						// Ordered by team ID...

	int* m_paiUnitCreatedCount;
	int* m_paiUnitClassCreatedCount;
	int* m_paiBuildingClassCreatedCount;
	int* m_paiProjectCreatedCount;
	int* m_paiForceCivicCount;
	PlayerVoteTypes* m_paiVoteOutcome;
	int* m_paiReligionGameTurnFounded;
	int* m_paiCorporationGameTurnFounded;
	int* m_aiSecretaryGeneralTimer;
	int* m_aiVoteTimer;
	int* m_aiDiploVote;

	bool* m_pabSpecialUnitValid;
	bool* m_pabSpecialBuildingValid;
	bool* m_abReligionSlotTaken; 

	IDInfo* m_paHolyCity;
	IDInfo* m_paHeadquarters;

	int** m_apaiPlayerVote;

	std::vector<CvWString> m_aszDestroyedCities;
	std::vector<CvWString> m_aszGreatPeopleBorn;

	FFreeListTrashArray<CvDeal> m_deals;
	FFreeListTrashArray<VoteSelectionData> m_voteSelections;
	FFreeListTrashArray<VoteTriggeredData> m_votesTriggered;

	CvRandom m_mapRand;
	CvRandom m_sorenRand;

	ReplayMessageList m_listReplayMessages; 
	CvReplayInfo* m_pReplayInfo;

	int m_iNumSessions;

	std::vector<PlotExtraYield> m_aPlotExtraYields;
	std::vector<PlotExtraCost> m_aPlotExtraCosts;
	stdext::hash_map<VoteSourceTypes, ReligionTypes> m_mapVoteSourceReligions;
	std::vector<EventTriggerTypes> m_aeInactiveTriggers;

	// CACHE: cache frequently used values
	int		m_iShrineBuildingCount;
	int*	m_aiShrineBuilding;
	int*	m_aiShrineReligion;

	int		m_iNumCultureVictoryCities;
	int		m_eCultureVictoryCultureLevel;

	void doTurn();
	void doDeals();
	void doGlobalWarming();
	void doHolyCity();
	void doHeadquarters();
	void doDiploVote();
	void doVoteResults();
	void doVoteSelection();

	void createBarbarianCities();
	void createBarbarianUnits();
	void createAnimals();

	void verifyCivics();

	void updateWar();
	void updateMoves();
	void updateTimers();
	void updateTurnTimer();

	void testAlive();
	void testVictory();

	void processVote(const VoteTriggeredData& kData, int iChange);

	int getTeamClosenessScore(int** aaiDistances, int* aiStartingLocs);
	void normalizeStartingPlotLocations();
	void normalizeAddRiver();
	void normalizeRemovePeaks();
	void normalizeAddLakes();
	void normalizeRemoveBadFeatures();
	void normalizeRemoveBadTerrain();
	void normalizeAddFoodBonuses();
	void normalizeAddGoodTerrain();
	void normalizeAddExtras();

	void showEndGameSequence();

	CvPlot* normalizeFindLakePlot(PlayerTypes ePlayer);

	void doUpdateCacheOnTurn();
};

#endif
