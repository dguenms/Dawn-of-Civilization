#pragma once

#ifndef CIV4_GAME_H
#define CIV4_GAME_H

class CvPlot;
class CvCity;
class CvReplayMessage;
class CvReplayInfo;
class CvArtInfoBuilding;
class CvArea;
class CvHallOfFameInfo; // advc.106i
class CvGameAI;
class CvDeal;
class CvCivilization; // advc.003w
class NormalizationTarget; // advc.027
class Shelf; // advc.300
class BarbarianWeightMap; // advc.304
class StartPointsAsHandicap; // advc.250b
class RiseFall; // advc.700

#include "History.h"

typedef std::vector<const CvReplayMessage*> ReplayMessageList;


class CvGame /* advc.003e: */ : private boost::noncopyable
{
public:

	CvGame();
	virtual ~CvGame();
protected: // advc.003u: Can't easily move these past AI_makeAssignWorkDirty (the EXE relies on the order)
	virtual void read(FDataStreamBase* pStream);
	virtual void write(FDataStreamBase* pStream);
	virtual void writeReplay(FDataStreamBase& stream, PlayerTypes ePlayer);
public:
	// advc.003u: Keep one pure virtual function so that this class is abstract
	virtual void AI_makeAssignWorkDirty() = 0;

	DllExport void init(HandicapTypes eHandicap);
	DllExport void reset(HandicapTypes eHandicap, bool bConstructorCall = false);

	DllExport void setInitialItems();
	DllExport void regenerateMap()
	{	// <advc.tsl>
		regenerateMap(false);
	}
	void regenerateMap(bool bAutomated); // </advc.tsl>
	void showDawnOfMan(); // advc.004j
	DllExport void initDiplomacy();
	DllExport void initFreeUnits();

	/* <advc.108>: Three levels of start plot normalization:
	 1: low (weak starting plots on average, high variance); for single-player
	 2: medium (strong starting plots, low variance); for multi-player
	 3: high (very strong starting plots, low variance);  BtS/ K-Mod behavior
	 (the differences between all three aren't very great) */
	enum StartingPlotNormalizationLevel {
		NORMALIZE_DEFAULT, NORMALIZE_LOW, NORMALIZE_MEDIUM, NORMALIZE_HIGH };
	StartingPlotNormalizationLevel getStartingPlotNormalizationLevel() const;
	void setStartingPlotNormalizationLevel(
			StartingPlotNormalizationLevel eLevel = NORMALIZE_DEFAULT);
	// </advc.108>
	int getStartingPlotRange() const; // advc.opt (exposed to Python via CyPlayer)

	DllExport void update();
	void updateScore(bool bForce = false);
	// <advc.003y>
	int getScoreComponent(int iRawScore, int iInitial, int iMax, int iMultiplier,
			bool bExponential, bool bFinal, bool bVictory) const; // </advc.003y>
	int getDifficultyForEndScore() const; // advc.250 (exposed to Python; hence public)
	void updateAIHandicap(); // advc.127

	DllExport void updateColoredPlots();
	DllExport void updateBlockadedPlots();
	bool updateNukeAreaOfEffect(CvPlot const* pPlot = NULL) const; // advc.653
	void updateSeaPatrolColors(CvUnit const& kSelectedUnit); // advc.004k

	void updatePlotGroups();
	void updateBuildingCommerce();
	void updateCitySight(bool bIncrement);
	void updateTradeRoutes();
	void updateGwPercentAnger(); // K-Mod

	DllExport void updateSelectionList();
	DllExport void updateTestEndTurn();
	void autoSave(bool bInitial = false); // advc.106l
	DllExport void testExtendedGame();

	DllExport CvUnit* getPlotUnit(const CvPlot* pPlot, int iIndex) const
	{
		return getPlotUnits(pPlot, NULL, iIndex); // advc
	}
	DllExport void getPlotUnits(const CvPlot *pPlot, std::vector<CvUnit*>& kPlotUnits) const
	{
		getPlotUnits(pPlot, &kPlotUnits, -1); // advc
	}

	DllExport void cycleCities(bool bForward = true, bool bAdd = false) const;							// Exposed to Python
	// <advc.154>
	CvSelectionGroup* getNextGroupInCycle(bool bForward, bool bWorkers,
			bool& bWrap, CvUnit*& pCycleUnit, std::set<int>* pCycledGroups = NULL) const;
	CvUnit* getCycleButtonUnit(bool bForward, bool bWorkers) const; // </advc.154>						// Exposed to Python
	void cycleSelectionGroups(bool bClear,																// Exposed to Python
			bool bForward = true, bool bWorkers = false);
	// K-Mod:
	void cycleSelectionGroups_delayed(int iDelay, bool bIncremental, bool bDelayOnly = false);
	DllExport bool cyclePlotUnits(CvPlot* pPlot,														// Exposed to Python
			bool bForward = true, bool bAuto = false, int iCount = -1) const;
	DllExport bool selectCity(CvCity* pSelectCity, bool bCtrl, bool bAlt, bool bShift) const;

	DllExport void selectionListMove(CvPlot* pPlot, bool bAlt, bool bShift, bool bCtrl) const;												// Exposed to Python
	DllExport void selectionListGameNetMessage(int eMessage,											// Exposed to Python
			int iData2 = -1, int iData3 = -1, int iData4 = -1, int iFlags = 0,
			bool bAlt = false, bool bShift = false) const;
	DllExport void selectedCitiesGameNetMessage(int eMessage,											// Exposed to Python
			int iData2 = -1, int iData3 = -1, int iData4 = -1, bool bOption = false,
			bool bAlt = false, bool bShift = false, bool bCtrl = false) const;
	void cityPushOrder(CvCity* pCity, OrderTypes eOrder, int iData,										// Exposed to Python
			bool bAlt = false, bool bShift = false, bool bCtrl = false) const;

	DllExport void selectUnit(CvUnit* pUnit, bool bClear, bool bToggle = false,
			bool bSound = false) const;
	DllExport void selectGroup(CvUnit* pUnit, bool bShift, bool bCtrl, bool bAlt) const;
	DllExport void selectAll(CvPlot* pPlot) const;

	DllExport bool selectionListIgnoreBuildingDefense() const;

	DllExport bool canHandleAction(int iAction, CvPlot* pPlot = NULL,
			bool bTestVisible = false, bool bUseCache = false) const;
	DllExport void setupActionCache() const;
	DllExport void handleAction(int iAction);

	bool canDoControl(ControlTypes eControl) const;
	void doControl(ControlTypes eControl);
	// <K-Mod>
	void retire();
	void enterWorldBuilder(); // </K-Mod>
	void exitToMenu(); // advc
	void setGlobeView(bool b); // advc

	DllExport void implementDeal(PlayerTypes eWho, PlayerTypes eOtherWho,
			CLinkList<TradeData>* pOurList, CLinkList<TradeData>* pTheirList,
			bool bForce = false);
	void implementDeal(PlayerTypes eWho, PlayerTypes eOtherWho,
			// advc (note): Not const; callee may perform in-place preprocessing.
			CLinkList<TradeData>& kOurList, CLinkList<TradeData>& kTheirList,
			bool bForce = false);
	// <advc.036>
	CvDeal* implementAndReturnDeal(PlayerTypes eWho, PlayerTypes eOtherWho,
			CLinkList<TradeData>& kOurList, CLinkList<TradeData>& kTheirList,
			bool bForce = false); // </advc.036>
	void verifyDeals();

	DllExport void getGlobeviewConfigurationParameters(TeamTypes eTeam,
			bool& bStarsVisible, bool& bWorldIsRound);

	int getSymbolID(int iSymbol)																		// Exposed to Python
	{
		return gDLL->getInterfaceIFace()->getSymbolID(iSymbol);
	}

	int getProductionPerPopulation(HurryTypes eHurry) const;											// Exposed to Python
	int getHurryAngerLength() const; // advc

	int getAdjustedPopulationPercent(VictoryTypes eVictory) const;										// Exposed to Python
	int getAdjustedLandPercent(VictoryTypes eVictory) const;											// Exposed to Python
	bool isDiploVictoryValid() const; // advc.178 (exposed to Python)
	bool isTeamVote(VoteTypes eVote) const;																// Exposed to Python
	bool isChooseElection(VoteTypes eVote) const;														// Exposed to Python
	bool isTeamVoteEligible(TeamTypes eTeam, VoteSourceTypes eVoteSource) const;						// Exposed to Python
	int countVote(const VoteTriggeredData& kData, PlayerVoteTypes eChoice) const;
	int countPossibleVote(VoteTypes eVote, VoteSourceTypes eVoteSource) const;							// Exposed to Python
	TeamTypes findHighestVoteTeam(const VoteTriggeredData& kData) const;
	int getVoteRequired(VoteTypes eVote, VoteSourceTypes eVoteSource) const;							// Exposed to Python
	TeamTypes getSecretaryGeneral(VoteSourceTypes eVoteSource) const;									// Exposed to Python
	bool canHaveSecretaryGeneral(VoteSourceTypes eVoteSource) const;									// Exposed to Python
	void clearSecretaryGeneral(VoteSourceTypes eVoteSource);
	void updateSecretaryGeneral();

	int countCivPlayersAlive() const;																	// Exposed to Python
	int countMajorPlayersAlive() const; // doc															// Exposed to Python
	int countCivPlayersEverAlive() const;																// Exposed to Python
	int countCivTeamsAlive() const;																		// Exposed to Python
	int countCivTeamsEverAlive() const;																	// Exposed to Python
	int countHumanPlayersAlive() const;																	// Exposed to Python
	int countFreeTeamsAlive() const; // K-Mod
	// advc.137: Replaces getDefaultPlayers for most purposes
	int getRecommendedPlayers() const;
	int getSeaLevelChange() const; // advc.137, advc.140

	int countTotalCivPower() const;																		// Exposed to Python
	int countTotalNukeUnits() const;																	// Exposed to Python
	int countKnownTechNumTeams(TechTypes eTech) const;													// Exposed to Python
	int getNumFreeBonuses(BuildingTypes eBuilding) const;												// Exposed to Python

	int countReligionLevels(ReligionTypes eReligion) const;												// Exposed to Python
	int calculateReligionPercent(ReligionTypes eReligion,												// Exposed to Python
			bool bIgnoreOtherReligions = false) const; // advc.115b
	int countCorporationLevels(CorporationTypes eCorporation) const;									// Exposed to Python
	void replaceCorporation(CorporationTypes eOldCorp, CorporationTypes eNewCorp);

	int goldenAgeLength() const;																		// Exposed to Python
	int victoryDelay(VictoryTypes eVictory) const;														// Exposed to Python
	int getImprovementUpgradeTime(ImprovementTypes eImprovement) const;									// Exposed to Python
	int getSpeedPercent() const; // advc.252

	bool canTrainNukes() const;																			// Exposed to Python
	EraTypes getCurrentEra() const;																		// Exposed to Python
	EraTypes getHighestEra() const; // advc
	scaled groundbreakingNormalizationModifier(TechTypes eTech) const; // advc.groundbr

	DllExport TeamTypes getActiveTeam() const															// Exposed to Python
	{
		return GC.getInitCore().getActiveTeam(); // advc.opt (cached)
	}
	CivilizationTypes getActiveCivilizationType() const;												// Exposed to Python
	CvCivilization const* getActiveCivilization() const; // advc.003w

	DllExport bool isNetworkMultiPlayer() const															// Exposed to Python
	{
		return GC.getInitCore().getMultiplayer();
	}
	DllExport bool isGameMultiPlayer() const;															// Exposed to Python
	DllExport bool isTeamGame() const;																	// Exposed to Python

	bool isModem() const;
	void setModem(bool bModem);

	DllExport void reviveActivePlayer();																// Exposed to Python
	DllExport int getNumHumanPlayers()																	// Exposed to Python
	{
		return GC.getInitCore().getNumHumans();
	}
	DllExport int getGameTurn() // <advc> Need a const version											// Exposed to Python
	{	CvGame const& kThis = *this;
		return kThis.getGameTurn();
	}
	int getGameTurn() const
	{
		return GC.getInitCore().getGameTurn();
	} // </advc>
	void setGameTurn(int iNewValue);																	// Exposed to Python
	void incrementGameTurn();

	int getTurnYear(int iGameTurn) const;																// Exposed to Python
	int getGameTurnYear() const																			// Exposed to Python
	{
		return getTurnYear(getGameTurn());
	}
	int getElapsedGameTurns() const																		// Exposed to Python
	{
		return m_iElapsedGameTurns;
	}
	void incrementElapsedGameTurns();
	int AIHandicapAdjustment() const; // advc.251

	int getMaxTurns() const																				// Exposed to Python
	{
		return GC.getInitCore().getMaxTurns();
	}
	void setMaxTurns(int iNewValue);																	// Exposed to Python
	void changeMaxTurns(int iChange);																	// Exposed to Python

	int getMaxCityElimination() const																	// Exposed to Python
	{
		return GC.getInitCore().getMaxCityElimination();
	}
	void setMaxCityElimination(int iNewValue);															// Exposed to Python

	int getNumAdvancedStartPoints() const																// Exposed to Python
	{
		return GC.getInitCore().getNumAdvancedStartPoints();
	}
	void setNumAdvancedStartPoints(int iNewValue);														// Exposed to Python

	int getStartTurn() const																			// Exposed to Python
	{
		return m_iStartTurn;
	}
	void setStartTurn(int iNewValue);

	int getStartYear() const																			// Exposed to Python
	{
		return m_iStartYear;
	}
	void setStartYear(int iNewValue);																	// Exposed to Python

	int getEstimateEndTurn() const																		// Exposed to Python
	{
		return m_iEstimateEndTurn;
	}
	void setEstimateEndTurn(int iNewValue);																// Exposed to Python
	scaled gameTurnProgress(int iDelay = 0) const; // advc

	DllExport int getTurnSlice() const { return m_iTurnSlice; }											// Exposed to Python
	int getMinutesPlayed() const;																		// Exposed to Python
	int getSecondsPlayed() const; // doc
	void setTurnSlice(int iNewValue);
	void changeTurnSlice(int iChange);

	int getCutoffSlice() const;
	void setCutoffSlice(int iNewValue);
	void changeCutoffSlice(int iChange);
	DllExport int getTurnSlicesRemaining()
	// <advc> Need a const version
	{	CvGame const& kThis = *this;
		return kThis.getTurnSlicesRemaining();
	}
	int getTurnSlicesRemaining() const { return getCutoffSlice() - getTurnSlice(); };
	// </advc>
	void resetTurnTimer();
	void incrementTurnTimer(int iNumTurnSlices);
	int getMaxTurnLen();

	int getTargetScore() const																			// Exposed to Python
	{
		return GC.getInitCore().getTargetScore();
	}
	void setTargetScore(int iNewValue);																	// Exposed to Python

	int getNumGameTurnActive() { return m_iNumGameTurnActive; }											// Exposed to Python
	DllExport int countNumHumanGameTurnActive() const;													// Exposed to Python
	void changeNumGameTurnActive(int iChange);

	int getNumCities() const																			// Exposed to Python
	{
		return m_iNumCities;
	}
	int getNumCivCities() const;																		// Exposed to Python
	void changeNumCities(int iChange);

	int getTotalPopulation() const																		// Exposed to Python
	{
		return m_iTotalPopulation;
	}
	void changeTotalPopulation(int iChange);

	int getTradeRoutes() const																			// Exposed to Python
	{
		return m_iTradeRoutes;
	}
	void changeTradeRoutes(int iChange);																// Exposed to Python

	int getFreeTradeCount() const																		// Exposed to Python
	{
		return m_iFreeTradeCount;
	}
	bool isFreeTrade() const																			// Exposed to Python
	{
		return (getFreeTradeCount() > 0);
	}
	void changeFreeTradeCount(int iChange);																// Exposed to Python

	int getNoNukesCount() const																			// Exposed to Python
	{
		return m_iNoNukesCount;
	}
	bool isNoNukes() const																				// Exposed to Python
	{
		return (getNoNukesCount() > 0);
	}
	void changeNoNukesCount(int iChange);																// Exposed to Python

	int getSecretaryGeneralTimer(VoteSourceTypes eVoteSource) const										// Exposed to Python
	{
		return m_aiSecretaryGeneralTimer.get(eVoteSource);
	}
	void setSecretaryGeneralTimer(VoteSourceTypes eVoteSource, int iNewValue);
	void changeSecretaryGeneralTimer(VoteSourceTypes eVoteSource, int iChange);

	int getVoteTimer(VoteSourceTypes eVoteSource) const													// Exposed to Python
	{
		return m_aiVoteTimer.get(eVoteSource);
	}
	void setVoteTimer(VoteSourceTypes eVoteSource, int iNewValue);
	void changeVoteTimer(VoteSourceTypes eVoteSource, int iChange);

	int getNukesExploded() const																		// Exposed to Python
	{
		return m_iNukesExploded;
	}
	void changeNukesExploded(int iChange);																// Exposed to Python

	int getMaxPopulation() const { return m_iMaxPopulation; }											// Exposed to Python
	int getMaxLand() const { return m_iMaxLand; }														// Exposed to Python
	int getMaxTech() const { return m_iMaxTech; }														// Exposed to Python
	int getMaxWonders() const { return m_iMaxWonders; }													// Exposed to Python
	int getInitPopulation() const { return m_iInitPopulation; }											// Exposed to Python
	int getInitLand() const { return m_iInitLand; }														// Exposed to Python
	int getInitTech() const { return m_iInitTech; }														// Exposed to Python
	int getInitWonders() const { return m_iInitWonders; }												// Exposed to Python
	/*	<advc> Asset score functions moved from CvGameCoreUtils. Could be static -
		but let's not commit to that. */
	int getPopulationAsset(int iPopulation) const
	{
		return iPopulation * 2;
	}
	int getLandPlotsAsset(int iLandPlots) const
	{
		return iLandPlots;
	}
	int getPopulationPower(int iPopulation) const
	{
		return iPopulation / 2;
	}
	int getPopulationScore(int iPopulation) const
	{
		return iPopulation;
	}
	int getLandPlotsScore(int iLandPlots) const
	{
		return iLandPlots;
	}
	int getTechScore(TechTypes eTech) const
	{
		return GC.getInfo(eTech).getEra() + 1;
	}
	int getWonderScore(BuildingClassTypes eWonderClass) const; // </advc>
	DllExport void initScoreCalculation();

	int getAIAutoPlay() const																			// Exposed to Python
	{
		return m_iAIAutoPlay;
	}
	DllExport void setAIAutoPlay(int iNewValue)															// Exposed to Python
	{	// <advc.127>
		setAIAutoPlay(iNewValue, true);
	}
	void setAIAutoPlay(int iNewValue, bool bChangePlayerStatus); // </advc.127>
	void changeAIAutoPlay(int iChange, /* advc.127: */ bool bChangePlayerStatus = true);
	// <advc.opt>
	int getCivPlayersEverAlive() const;
	void changeCivPlayersEverAlive(int iChange);
	int getCivTeamsEverAlive() const;
	void changeCivTeamsEverAlive(int iChange);
	// </advc.opt>
	// <K-Mod>
	int getGlobalWarmingIndex() const { return m_iGlobalWarmingIndex; }									// Exposed to Python
	void setGlobalWarmingIndex(int iNewValue);
	void changeGlobalWarmingIndex(int iChange);
	int getGlobalWarmingChances() const;																// Exposed to Python
	int getGwEventTally() const { return m_iGwEventTally; }												// Exposed to Python
	void setGwEventTally(int iNewValue);
	void changeGwEventTally(int iChange);
	int calculateGlobalPollution() const;																// Exposed to Python
	int calculateGwLandDefence(PlayerTypes ePlayer = NO_PLAYER) const;									// Exposed to Python
	int calculateGwSustainabilityThreshold(PlayerTypes ePlayer = NO_PLAYER) const;						// Exposed to Python
	int calculateGwSeverityRating() const;																// Exposed to Python
	// </K-Mod>
	unsigned int getInitialTime();
	DllExport void setInitialTime(unsigned int uiNewValue);

	bool isScoreDirty() const;																			// Exposed to Python
	void setScoreDirty(bool bNewValue);																	// Exposed to Python
	// <advc.003r> Akin to deferCall in BugUtil.py
	enum UpdateTimerTypes {
		UPDATE_COLLAPSE_SCORE_BOARD, // advc.085
		UPDATE_DIRTY_SCORE_HELP, // advc.085
		UPDATE_MOUSE_FOCUS, // advc.001w
		UPDATE_LOOK_AT_STARTING_PLOT, // advc.004j
		UPDATE_STORE_REPLAY_TEXTURE, // advc.106n
		UPDATE_REBUILD_PLOTS, // advc.001
		NUM_UPDATE_TIMER_TYPES
	};
	void setUpdateTimer(UpdateTimerTypes eTimerType, int iDelay);
	// Unused so far (x3)
	void cancelUpdateTimer(UpdateTimerTypes eTimerType) { setUpdateTimer(eTimerType, -1); }
	int getUpdateTimer(UpdateTimerTypes eTimerType) const;
	bool isUpdatePending(UpdateTimerTypes eTimerType) const
	{
		return (getUpdateTimer(eTimerType) >= 0);
	} // </advc.003r>

	bool isCircumnavigated() const { return m_bCircumnavigated; }										// Exposed to Python
	void makeCircumnavigated();																			// Exposed to Python
	int getCircumnavigated(); // rfc // TODO: needed?													// Exposed to Python
	void setCircumnavigated(int i);	// rfc // TODO: needed?
	bool circumnavigationAvailable() const;

	bool isDiploVote(VoteSourceTypes eVoteSource) const													// Exposed to Python
	{
		return (getDiploVoteCount(eVoteSource) > 0);
	}
	int getDiploVoteCount(VoteSourceTypes eVoteSource) const
	{
		return m_aiDiploVote.get(eVoteSource);
	}
	void changeDiploVote(VoteSourceTypes eVoteSource, int iChange);																					// Exposed to Python
	bool canDoResolution(VoteSourceTypes eVoteSource,
			VoteSelectionSubData const& kData) const;
	bool isValidVoteSelection(VoteSourceTypes eVoteSource,
			VoteSelectionSubData const& kData) const;

	DllExport bool isDebugMode() const																	// Exposed to Python
	{
		return m_bDebugModeCache;
	}
	DllExport void toggleDebugMode();																	// Exposed to Python
	DllExport void updateDebugModeCache();
	bool isDebugToolsAllowed(bool bWB) const; // advc.135c
	bool isGameNameEnableDebugTools(CvWString const& kGameName) const; // advc.135c
	DllExport int getPitbossTurnTime() const;															// Exposed to Python
	DllExport void setPitbossTurnTime(int iHours);														// Exposed to Python

	DllExport bool isHotSeat() const																	// Exposed to Python
	{
		return GC.getInitCore().getHotseat();
	}
	DllExport bool isPbem() const																		// Exposed to Python
	{
		return GC.getInitCore().getPbem();
	}
	DllExport bool isPitboss() const																	// Exposed to Python
	{
		return GC.getInitCore().getPitboss();
	}
	bool isSimultaneousTeamTurns() const;																// Exposed to Python

	DllExport bool isFinalInitialized() const															// Exposed to Python
	{
		return m_bFinalInitialized;
	}
	DllExport void setFinalInitialized(bool bNewValue);
	// <advc.004x>
	void setDawnOfManShown(bool b);
	bool isAboutToShowDawnOfMan() const; // </advc.004x>
	// <advc.061>
	void setScreenDimensions(int iWidth, int iHeight); // (exposed to Python)
	int getScreenWidth() const;
	int getScreenHeight() const;
	// </advc.061>  <advc.004n>
	void changePlotListShift(int iChange) { m_iPlotListShift += iChange; }
	int getPlotListShift() const { return m_iPlotListShift; }
	void onCityScreenChange(); // </advc.004n>
	bool getPbemTurnSent() const;
	DllExport void setPbemTurnSent(bool bNewValue);

	DllExport bool getHotPbemBetweenTurns() const;
	void setHotPbemBetweenTurns(bool bNewValue);

	bool isPlayerOptionsSent() const;
	void sendPlayerOptions(bool bForce = false);

	DllExport PlayerTypes getActivePlayer() const														// Exposed to Python
	{
		return GC.getInitCore().getActivePlayer();
	}
	DllExport void setActivePlayer(PlayerTypes eNewValue, bool bForceHotSeat = false);					// Exposed to Python
	void updateActiveVisibility(); // advc.706
	DllExport void updateUnitEnemyGlow();
	/* <advc.106b> When a DLL function is called from the EXE, there is no (other)
	   way to determine whether it's during a human turn.
	   (Or would CvPlayer::isTurnActive work? But that's not as convenient ...) */
	// Also used for various other AdvCiv changes
	bool isInBetweenTurns() const { return m_bInBetweenTurns; }
	void setInBetweenTurns(bool b); // </advc.106b>

	HandicapTypes getHandicapType() const { return m_eHandicap; }										// Exposed to Python
	void setHandicapType(HandicapTypes eHandicap);
	HandicapTypes getAIHandicap() const { return m_eAIHandicap; } // advc.127 (advc.708: exposed to Python)

	DllExport PlayerTypes getPausePlayer() const;														// Exposed to Python
	DllExport bool isPaused() const;																									// Exposed to Python
	DllExport void setPausePlayer(PlayerTypes eNewValue);

	UnitTypes getBestLandUnit() const;																	// Exposed to Python
	int getBestLandUnitCombat() const;																	// Exposed to Python
	void setBestLandUnit(UnitTypes eNewValue);

	TeamTypes getWinner() const																			// Exposed to Python
	{
		return m_eWinner;
	}
	VictoryTypes getVictory() const																		// Exposed to Python
	{
		return m_eVictory;
	}
	void setWinner(TeamTypes eNewWinner, VictoryTypes eNewVictory);										// Exposed to Python

	DllExport GameStateTypes getGameState() const														// Exposed to Python
	{
		return m_eGameState;
	}
	DllExport void setGameState(GameStateTypes eNewValue);

	// advc.106h:
	PlayerTypes getInitialActivePlayer() const
	{
		return m_eInitialActivePlayer;
	}
	EraTypes getStartEra() const																		// Exposed to Python
	{
		return GC.getInitCore().getEra();
	}
	CalendarTypes getCalendar() const																	// Exposed to Python
	{
		return GC.getInitCore().getCalendar();
	}
	GameSpeedTypes getGameSpeedType() const																// Exposed to Python
	{
		return GC.getInitCore().getGameSpeed();
	}

	PlayerTypes getRankPlayer(PlayerTypes eRank) const													// Exposed to Python
	{
		return m_aeRankPlayer.get(eRank);
	}
	void setRankPlayer(PlayerTypes eRank, PlayerTypes ePlayer);
	// advc (note): The topmost rank is 0
	PlayerTypes getPlayerRank(PlayerTypes ePlayer) const												// Exposed to Python
	{
		return m_aePlayerRank.get(ePlayer);
	}
	void setPlayerRank(PlayerTypes ePlayer, PlayerTypes eRank);
	DllExport int getPlayerScore(PlayerTypes ePlayer) const												// Exposed to Python
	{
		return m_aiPlayerScore.get(ePlayer);
	}
	void setPlayerScore(PlayerTypes ePlayer, int iScore);
	TeamTypes getRankTeam(TeamTypes eRank) const														// Exposed to Python
	{
		return m_aeRankTeam.get(eRank);
	}
	void setRankTeam(TeamTypes eRank, TeamTypes eTeam);
	int getTeamRank(TeamTypes eTeam) const																// Exposed to Python
	{
		return m_aeTeamRank.get(eTeam);
	}
	void setTeamRank(TeamTypes eTeam, TeamTypes eRank);
	DllExport int getTeamScore(TeamTypes eTeam) const													// Exposed to Python
	{
		return m_aiTeamScore.get(eTeam);
	}
	void setTeamScore(TeamTypes eTeam, int iScore);

	DllExport bool isOption(GameOptionTypes eIndex) const												// Exposed to Python
	{
		return GC.getInitCore().getOption(eIndex);
	}
	void setOption(GameOptionTypes eIndex, bool bEnabled);												// Exposed to Python

	DllExport bool isMPOption(MultiplayerOptionTypes eIndex) const										// Exposed to Python
	{
		return GC.getInitCore().getMPOption(eIndex);
	}
	void setMPOption(MultiplayerOptionTypes eIndex, bool bEnabled);

	bool isForcedControl(ForceControlTypes eIndex) const												// Exposed to Python
	{
		return GC.getInitCore().getForceControl(eIndex);
	}
	void setForceControl(ForceControlTypes eIndex, bool bEnabled);
	// <advc>
	bool canConstruct(BuildingTypes eBuilding, bool bIgnoreCost, bool bTestVisible) const;
	bool canTrain(UnitTypes eUnit, bool bIgnoreCost, bool bTestVisible) const;
	// </advc>
	int getUnitCreatedCount(UnitTypes eUnit) const														// Exposed to Python
	{
		return m_aiUnitCreatedCount.get(eUnit);
	}
	void incrementUnitCreatedCount(UnitTypes eUnit);
	int getUnitClassCreatedCount(UnitClassTypes eUnitClass) const										// Exposed to Python
	{
		return m_aiUnitClassCreatedCount.get(eUnitClass);
	}
	bool isUnitClassMaxedOut(UnitClassTypes eUnitClass, int iExtra = 0) const;							// Exposed to Python
	void incrementUnitClassCreatedCount(UnitClassTypes eUnitClass);
	int getBuildingClassCreatedCount(BuildingClassTypes eBuildingClass) const							// Exposed to Python
	{
		return m_aiBuildingClassCreatedCount.get(eBuildingClass);
	}
	bool isBuildingClassMaxedOut(BuildingClassTypes eBuildingClass, int iExtra = 0) const;				// Exposed to Python
	void incrementBuildingClassCreatedCount(BuildingClassTypes eBuildingClass);
	int getProjectCreatedCount(ProjectTypes eProject) const												// Exposed to Python
	{
		return m_aiProjectCreatedCount.get(eProject);
	}
	bool isProjectMaxedOut(ProjectTypes eProject, int iExtra = 0) const;								// Exposed to Python
	void incrementProjectCreatedCount(ProjectTypes eProject, int iExtra = 1);

	int getForceCivicCount(CivicTypes eCivic) const														// Exposed to Python
	{
		return m_aiForceCivicCount.get(eCivic);
	}
	bool isForceCivic(CivicTypes eCivic) const															// Exposed to Python
	{
		return (getForceCivicCount(eCivic) > 0);
	}
	bool isForceCivicOption(CivicOptionTypes eCivicOption) const;										// Exposed to Python
	void changeForceCivicCount(CivicTypes eCivic, int iChange);
	int getMaxConscript(CivicTypes eCivic) const;

	PlayerVoteTypes getVoteOutcome(VoteTypes eVote) const												// Exposed to Python
	{
		return m_aiVoteOutcome.get(eVote);
	}
	bool isVotePassed(VoteTypes eVote) const;															// Exposed to Python
	void setVoteOutcome(VoteTriggeredData const& kData, PlayerVoteTypes eNewValue);

	bool isVictoryValid(VictoryTypes eVictory) const													// Exposed to Python
	{
		return GC.getInitCore().getVictory(eVictory);
	}
	void setVictoryValid(VictoryTypes eVictory, bool bValid); // (advc: Exposed to Python)

	bool isSpecialUnitValid(SpecialUnitTypes eSpecialUnit) const										// Exposed to Python
	{
		return m_abSpecialUnitValid.get(eSpecialUnit);
	}
	void makeSpecialUnitValid(SpecialUnitTypes eSpecialUnit);											// Exposed to Python
	bool isSpecialBuildingValid(SpecialBuildingTypes eSpecialBuilding) const							// Exposed to Python
	{
		return m_abSpecialBuildingValid.get(eSpecialBuilding);
	}
	void makeSpecialBuildingValid(SpecialBuildingTypes eSpecialBuilding,								// Exposed to Python
			bool bAnnounce = false);

	bool isNukesValid() const																			// Exposed to Python
	{
		return m_bNukesValid;
	}
	void makeNukesValid(bool bValid = true);															// Exposed to Python

	bool isInAdvancedStart() const;																		// Exposed to Python

	void setVoteChosen(int iSelection, int iVoteId);

	int getReligionGameTurnFounded(ReligionTypes eReligion) const										// Exposed to Python
	{
		return m_aiReligionGameTurnFounded.get(eReligion);
	}
	bool isReligionFounded(ReligionTypes eReligion) const												// Exposed to Python
	{
		return (getReligionGameTurnFounded(eReligion) >= 0);
	}
	void setReligionGameTurnFounded(ReligionTypes eReligion, int iGameTurn); // doc
	void makeReligionFounded(ReligionTypes eReligion, PlayerTypes ePlayer);
	bool isReligionSlotTaken(ReligionTypes eReligion) const												// Exposed to Python
	{
		return m_abReligionSlotTaken.get(eReligion);
	}
	void setReligionSlotTaken(ReligionTypes eReligion, bool bTaken);
	CvCity* getHolyCity(ReligionTypes eReligion) const;													// Exposed to Python
	void setHolyCity(ReligionTypes eReligion, CvCity* pCity, bool bAnnounce);							// Exposed to Python

	int getCorporationGameTurnFounded(CorporationTypes eCorp) const										// Exposed to Python
	{
		return m_aiCorporationGameTurnFounded.get(eCorp);
	}
	bool isCorporationFounded(CorporationTypes eCorp) const												// Exposed to Python
	{
		return getCorporationGameTurnFounded(eCorp) >= 0;
	}
	void makeCorporationFounded(CorporationTypes eCorp, PlayerTypes ePlayer);
	CvCity* getHeadquarters(CorporationTypes eCorp) const;												// Exposed to Python
	void setHeadquarters(CorporationTypes eCorp, CvCity* pCity, bool bAnnounce);						// Exposed to Python

	PlayerVoteTypes getPlayerVote(PlayerTypes eVoter, int iVote) const;									// Exposed to Python
	void setPlayerVote(PlayerTypes eVoter, int iVote, PlayerVoteTypes eNewValue);
	void castVote(PlayerTypes eVoter, int iVote, PlayerVoteTypes ePlayerVote);

	DllExport CvWString const& getName();
	void setName(TCHAR const* szName);

	// Script data needs to be a narrow string for pickling in Python
	std::string getScriptData() const;																	// Exposed to Python
	void setScriptData(std::string szNewValue);															// Exposed to Python

	bool isDestroyedCityName(CvWString& szName) const;
	void addDestroyedCityName(CvWString const& szName);

	bool isGreatPersonBorn(CvWString& szName) const;
	void addGreatPersonBornName(CvWString const& szName);

	DllExport int getIndexAfterLastDeal();																// Exposed to Python
	int getNumDeals() { return m_deals.getCount(); }													// Exposed to Python

	DllExport CvDeal* getDeal(int iID)																	// Exposed to Python
	{
		return m_deals.getAt(iID);
	}
	CvDeal const* getDeal(int iID) const // advc: const version
	{
		return m_deals.getAt(iID);
	}

	CvDeal* addDeal();
	void deleteDeal(int iID);
	// iteration (advc: const)
	CvDeal* firstDeal(int *pIterIdx, bool bRev=false) const												// Exposed to Python
	{	//return (!bRev ? m_deals.beginIter(pIterIdx) : m_deals.endIter(pIterIdx));
		FAssert(!bRev);
		return m_deals.beginIter(pIterIdx); // advc.opt
	}
	CvDeal* nextDeal(int *pIterIdx, bool bRev=false) const												// Exposed to Python
	{	//return (!bRev ? m_deals.nextIter(pIterIdx) : m_deals.prevIter(pIterIdx));
		return m_deals.nextIter(pIterIdx); // advc.opt
	}
	// <advc.072>
	CvDeal* nextCurrentDeal(PlayerTypes eGivePlayer, PlayerTypes eReceivePlayer,
			TradeableItems eItemType, int iData = -1, bool bWidget = false);
	// </advc.072>
	VoteSelectionData* getVoteSelection(int iID) const
	{
		return m_voteSelections.getAt(iID);
	}
	VoteSelectionData* addVoteSelection(VoteSourceTypes eVoteSource);
	void deleteVoteSelection(int iID);

	VoteTriggeredData* getVoteTriggered(int iID) const;
	VoteTriggeredData* addVoteTriggered(VoteSelectionData const& kData, int iChoice);
	VoteTriggeredData* addVoteTriggered(VoteSourceTypes eVoteSource,
			VoteSelectionSubData const& kOptionData);
	void deleteVoteTriggered(int iID);

	CvRandom& getMapRand()																				// Exposed to Python
	{
		return m_mapRand;
	}
	int getMapRandNum(int iNum, const char* pszLog)
	{
		return m_mapRand.get(iNum, pszLog);
	}
	CvRandom& getSorenRand()																			// Exposed to Python
	{
		return m_sorenRand;
	}
	//  Returns a value from the half-closed interval [0,iNum)
	int getSorenRandNum(int iNum, const char* pszLog,
		int iData1 = MIN_INT, int iData2 = MIN_INT) // advc.007
	{
		return m_sorenRand.getInt(iNum, pszLog, /* advc.007: */ iData1, iData2);
	}
	// (map rand, sync rand)
	std::pair<uint,uint> getInitialRandSeed() const; // advc.027b

	DllExport int calculateSyncChecksum();																// Exposed to Python
	DllExport int calculateOptionsChecksum();															// Exposed to Python
	bool checkInSync(); // advc.001n
	void doFPCheck(int iChecksum, PlayerTypes ePlayer); // advc.003g

	bool changePlayer( int playerIdx, int newCivType, int newLeader, int teamIdx, bool bIsHuman, bool bChangeGraphics ); // rfc // TODO: needed?
	void convertUnits( int playerIdx ); // rfc // TODO: needed?

	void addReplayMessage(ReplayMessageTypes eType = NO_REPLAY_MESSAGE,
			PlayerTypes ePlayer = NO_PLAYER, CvWString szText = L"",
			// <advc> Move coords to the end - or to the start.
			ColorTypes eColor = NO_COLOR,
			int iPlotX = INVALID_PLOT_COORD, int iPlotY = INVALID_PLOT_COORD);
	void addReplayMessage(CvPlot const& kPlot,
			ReplayMessageTypes eType = NO_REPLAY_MESSAGE,
			PlayerTypes ePlayer = NO_PLAYER, CvWString szText = L"",
			ColorTypes eColor = NO_COLOR); // </advc>
	void clearReplayMessageMap();
	int getReplayMessageTurn(uint i) const;
	ReplayMessageTypes getReplayMessageType(uint i) const;
	int getReplayMessagePlotX(uint i) const;
	int getReplayMessagePlotY(uint i) const;
	PlayerTypes getReplayMessagePlayer(uint i) const;
	LPCWSTR getReplayMessageText(uint i) const;
	uint getNumReplayMessages() const;
	ColorTypes getReplayMessageColor(uint i) const;
	// <advc>
	void onAllGameDataRead();
	bool isAllGameDataRead() const { return m_bAllGameDataRead; }
	void onGraphicsInitialized(); // </advc>

	void updateTechRanks(); // doc
	int getTechRank(TeamTypes eTeam) const; // doc
	void setTechRank(int iRank, TeamTypes eTeam); // doc

	int getMedianTechValue() const;
	void setMedianTechValue(int iValue);

	CvReplayInfo* getReplayInfo() const;
	DllExport void setReplayInfo(CvReplayInfo* pReplay);
	void saveReplay(PlayerTypes ePlayer);

	bool hasSkippedSaveChecksum() const;																// Exposed to Python

	void addPlayer(PlayerTypes eNewPlayer, LeaderHeadTypes eLeader, CivilizationTypes eCiv, int iBirthTurn, bool bAlive, bool bMinor); // doc   // Exposed to Python
	// BETTER_BTS_AI_MOD, Debug, 8/1/08, jdog5000:
	void changeHumanPlayer(PlayerTypes eNewHuman, /* advc: */ bool bSetTurnActive = false);

	bool testVictory(VictoryTypes eVictory, TeamTypes eTeam, bool* pbEndScore = NULL) const;

	bool isCompetingCorporation(CorporationTypes eCorp1, CorporationTypes eCorp2) const;
	// advc.enum: Cache this at CvCity instead (implementations deleted)
	/*int getShrineBuildingCount(ReligionTypes eReligion = NO_RELIGION);
	BuildingTypes getShrineBuilding(int eIndex, ReligionTypes eReligion = NO_RELIGION);
	void changeShrineBuilding(BuildingTypes eBuilding, ReligionTypes eReligion, bool bRemove = false);*/

	bool culturalVictoryValid() const
	{	// (advc, note: Important not to call culturalVictoryNumCultureCities here.)
		return (m_iNumCultureVictoryCities > 0);
	}
	int culturalVictoryNumCultureCities() const;
	CultureLevelTypes culturalVictoryCultureLevel() const;
	int getCultureThreshold(CultureLevelTypes eLevel) const;
	int freeCityCultureFromTrait(TraitTypes eTrait) const; // advc.908b
	// advc.enum: Moved to CvMap
	/*int getPlotExtraYield(int iX, int iY, YieldTypes eYield) const;
	void setPlotExtraYield(int iX, int iY, YieldTypes eYield, int iCost);
	void removePlotExtraYield(int iX, int iY);
	int getPlotExtraCost(int iX, int iY) const;
	void changePlotExtraCost(int iX, int iY, int iCost);
	void removePlotExtraCost(int iX, int iY);*/

	ReligionTypes getVoteSourceReligion(VoteSourceTypes eVoteSource) const	 							// Exposed to Python
	{
		return m_aeVoteSourceReligion.get(eVoteSource);
	}
	void setVoteSourceReligion(VoteSourceTypes eVoteSource,												// Exposed to Python
			ReligionTypes eReligion, bool bAnnounce = false);

	bool isEventActive(EventTriggerTypes eTrigger) const												// Exposed to Python
	{
		FAssert(!isOption(GAMEOPTION_NO_EVENTS)); // advc.003v
		return !m_abInactiveTriggers.get(eTrigger);
	}
	DllExport void initEvents();
		// advc (note): The ..EverActive functions are currently only called from Python (Pedia)
	bool isCivEverActive(CivilizationTypes eCivilization) const;										// Exposed to Python
	bool isLeaderEverActive(LeaderHeadTypes eLeader) const;												// Exposed to Python
	bool isUnitEverActive(UnitTypes eUnit) const;														// Exposed to Python
	bool isBuildingEverActive(BuildingTypes eBuilding) const;											// Exposed to Python
	void processBuilding(BuildingTypes eBuilding, int iChange);
	//bool pythonIsBonusIgnoreLatitudes() const; // advc.003y: Moved to CvPythonCaller

	DllExport void getGlobeLayers(std::vector<CvGlobeLayerData>& aLayers) const;
	DllExport void startFlyoutMenu(CvPlot const* pPlot,
			std::vector<CvFlyoutMenuData>& aFlyoutItems) const;
	DllExport void applyFlyoutMenu(CvFlyoutMenuData const& kItem);
	DllExport CvPlot* getNewHighlightPlot() const;
	DllExport ColorTypes getPlotHighlightColor(CvPlot* pPlot) const;
	DllExport void cheatSpaceship() const;
	DllExport VictoryTypes getSpaceVictory() const;
	VictoryTypes getDominationVictory() const; // advc.115f
	DllExport void nextActivePlayer(bool bForward);

	// advc.003j (note): Isn't (and imo shouldn't be) used DLL-internally
	DllExport DomainTypes getUnitDomain(UnitTypes eUnit) const;
	DllExport CvArtInfoBuilding const* getBuildingArtInfo(BuildingTypes eBuilding) const;
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

	void setCityBarWidth(bool bWide); // advc.095 (exposed to Python)
	DllExport void handleCityScreenPlotPicked(CvCity* pCity, CvPlot* pPlot,
			bool bAlt, bool bShift, bool bCtrl) const;
	DllExport void handleCityScreenPlotDoublePicked(CvCity* pCity, CvPlot* pPlot,
			bool bAlt, bool bShift, bool bCtrl) const;
	DllExport void handleCityScreenPlotRightPicked(CvCity* pCity, CvPlot* pPlot,
			bool bAlt, bool bShift, bool bCtrl) const;
	DllExport void handleCityPlotRightPicked(CvCity* pCity, CvPlot* pPlot,
			bool bAlt, bool bShift, bool bCtrl) const;
	DllExport void handleMiddleMouse(bool bCtrl, bool bAlt, bool bShift);
	DllExport void handleDiplomacySetAIComment(DiploCommentTypes eComment) const;

	scaled goodyHutEffectFactor(bool bSpeedAdjust = true) const; // advc.314
	// <advc.004m>
	GlobeLayerTypes getCurrentLayer() const;
	void reportCurrentLayer(GlobeLayerTypes eLayer);		// (exposed to Python)
	// </advc.004m>  <advc.052>
	bool isScenario() const { return m_bScenario; }			// (exposed to Python)
	void setScenario(bool b);
	// </advc.052>  <advc.127b>
	/*  Returns (-1,-1) if 'vs' doesn't exist in any city or (eObserver!=NO_TEAM)
		isn't revealed to eObserver */
	std::pair<int,int> getVoteSourceXY(VoteSourceTypes eVS, TeamTypes eObserver,
			bool bDebug = false) const;
	BuildingTypes getVoteSourceBuilding(VoteSourceTypes eVS) const;
	CvCity* getVoteSourceCity(VoteSourceTypes eVS, TeamTypes eObserver,
			bool bDebug = false) const;
	// </advc.127b>
	bool isFreeStartEraBuilding(BuildingTypes eBuilding) const; // advc
	/*  advc.250b: Used for exposing a StartPointsAsHandicap member function
		to Python. (Don't want to create a Python wrapper just for that one function.) */
	StartPointsAsHandicap const& startPointsAsHandicap() const;
	int getBarbarianStartTurn() const; // advc.300		(exposed to Python)
	bool isBarbarianCreationEra() const; // advc.307
	// <advc.304>
	BarbarianWeightMap& getBarbarianWeightMap() { return *m_pBarbarianWeightMap; }
	BarbarianWeightMap const& getBarbarianWeightMap() const { return *m_pBarbarianWeightMap; }
	// </advc.304>  <advc.703>
	RiseFall const& getRiseFall() const { return *m_pRiseFall; }
	RiseFall& getRiseFall() { return *m_pRiseFall; }
	// </advc.703>
	void setHallOfFame(CvHallOfFameInfo* pHallOfFame); // advc.106i
	std::set<int>& getActivePlayerCycledGroups(); // advc
	// <advc.003u>
	CvGameAI& AI()
	{	//return *static_cast<CvGameAI*>(const_cast<CvGame*>(this));
		/*  The above won't work in an inline function b/c the compiler doesn't know
			that CvGameAI is derived from CvGame */
		return *reinterpret_cast<CvGameAI*>(this);
	}
	CvGameAI const& AI() const
	{	//return *static_cast<CvGameAI const*>(this);
		return *reinterpret_cast<CvGameAI const*>(this);
	} // </advc.003u>

	bool isNeighbors(PlayerTypes ePlayer1, PlayerTypes ePlayer2) const; // doc
	TeamTypes determineWinner(TeamTypes eTeam1, TeamTypes eTeam2) const; // doc
	void autosave(bool bInitial = false); // doc
	bool isPlayerAutoplay(PlayerTypes ePlayer = NO_PLAYER); // doc
	void setCityScreenOwner(PlayerTypes ePlayer); // doc
	void resetCityScreenOwner(); // doc
	PlayerTypes getCityScreenOwner() const; // doc

	bool isNotification(PlayerTypes eNotifiedPlayer, PlayerTypes eCausingPlayer, NotificationLevelTypes eNotificationLevel) const; // doc

	NotificationLevelTypes getGreatPeopleNotifications() const; // doc
	void setGreatPeopleNotifications(NotificationLevelTypes eNotificationLevel); // doc
	bool isGreatPeopleNotification(PlayerTypes eNotifiedPlayer, PlayerTypes eCausingPlayer) const; // doc
	NotificationLevelTypes getReligionSpreadNotifications() const; // doc
	void setReligionSpreadNotifications(NotificationLevelTypes eNotificationLevel); // doc
	bool isReligionSpreadNotification(PlayerTypes eNotifiedPlayer, PlayerTypes eCausingPlayer) const; // doc
	NotificationLevelTypes getEventEffectNotifications() const; // doc
	void setEventEffectNotifications(NotificationLevelTypes eNotificationLevel); // doc
	bool isEventEffectNotification(PlayerTypes eNotifiedPlayer, PlayerTypes eCausingPlayer) const; // doc

	PeriodTypes getPeriod(CivilizationTypes eCivilization) const { return m_aeCivPeriod.get(eCivilization); } // doc
	void setPeriod(CivilizationTypes eCivilization, PeriodTypes ePeriod); // doc

	int getCivilizationHistory(HistoryTypes eHistory, CivilizationTypes eCivilization, int iTurn) const { return m_apCivilizationHistory[eCivilization][eHistory].get(iTurn); } // doc
	void setCivilizationHistory(HistoryTypes eHistory, CivilizationTypes eCivilization, int iTurn, int iValue); // doc

	CivilizationTypes getFirstDiscovered(TechTypes eTech) const { return m_aeFirstDiscovered.get(eTech); } // doc
	void setFirstDiscovered(TechTypes eTech, CivilizationTypes eCivilization); // doc

	int getFirstDiscoveredTurn(TechTypes eTech) const { return m_aeFirstDiscoveredTurn.get(eTech); } // doc
	void setFirstDiscoveredTurn(TechTypes eTech, int iTurn); // doc

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
	int m_iCircumnavigated; // rfc // TODO: needed?
	int m_iGlobalWarmingIndex;	// K-Mod
	int m_iGwEventTally;		// K-Mod
	int m_iTurnLoadedFromSave; // advc.044
	// <advc.opt>
	mutable int m_iStartingPlotRange;
	int m_iCivPlayersEverAlive;
	int m_iCivTeamsEverAlive;
	// </advc.opt>
	int m_iUnitUpdateAttempts; // advc.001y
	int m_iScreenWidth, m_iScreenHeight; // advc.061
	// <advc.004n>
	int m_iPlotListShift;
	bool m_bCityScreenUp; // </advc.004n>
	unsigned int m_uiInitialTime;
	unsigned int m_uiSaveFlag; // advc

	// doc
	int m_iMedianTechValue;

	bool m_bScoreDirty;
	bool m_bCircumnavigated;
	bool m_bDebugMode;
	bool m_bDebugModeCache;
	bool m_bFinalInitialized;
	bool m_bPbemTurnSent;
	bool m_bHotPbemBetweenTurns;
	bool m_bPlayerOptionsSent;
	bool m_bNukesValid;
	bool m_bInBetweenTurns; // advc.106b
	bool m_bFeignSP; // advc.135c
	bool m_bScenario; // advc.052
	bool m_bAllGameDataRead; // advc
	bool m_bDoMShown; // advc.004x
	bool m_bLayerFromSavegame; // advc.004m
	bool m_bFPTestDone; // advc.003g

	HandicapTypes m_eHandicap;
	HandicapTypes m_eAIHandicap; // advc.127
	PlayerTypes m_ePausePlayer;
	UnitTypes m_eBestLandUnit;
	TeamTypes m_eWinner;
	VictoryTypes m_eVictory;
	GameStateTypes m_eGameState;
	PlayerTypes m_eEventPlayer; // doc
	PlayerTypes m_eCityScreenOwner; // doc
	PlayerTypes m_eInitialActivePlayer; // advc.106h
	GlobeLayerTypes m_eCurrentLayer; // advc.004m
	//PlayerTypes m_eEventPlayer; // (advc: unused)
	StartingPlotNormalizationLevel m_eNormalizationLevel; // advc.108

	NotificationLevelTypes m_eGreatPeopleNotifications; // doc
	NotificationLevelTypes m_eReligionSpreadNotifications; // doc
	NotificationLevelTypes m_eEventEffectNotifications; // doc

	CvRandom m_mapRand;
	CvRandom m_sorenRand;

	CvString m_szScriptData;

	int m_aiUpdateTimers[NUM_UPDATE_TIMER_TYPES]; // advc.003r
	/*	<advc.enum> (NB: Mustn't use eager allocation for dynamic enum types
		b/c XML isn't loaded yet.) */
	EagerEnumMap<PlayerTypes,PlayerTypes> m_aeRankPlayer; // Ordered by rank
	EagerEnumMap<PlayerTypes,PlayerTypes> m_aePlayerRank;
	EagerEnumMap<PlayerTypes,int> m_aiPlayerScore;
	EagerEnumMap<TeamTypes,TeamTypes> m_aeRankTeam; // Ordered by rank
	EagerEnumMap<TeamTypes,TeamTypes> m_aeTeamRank;
	EagerEnumMap<TeamTypes,int> m_aiTeamScore;

	ArrayEnumMap<UnitTypes,int> m_aiUnitCreatedCount;
	ArrayEnumMap<UnitClassTypes,int> m_aiUnitClassCreatedCount;
	ArrayEnumMap<BuildingClassTypes,int> m_aiBuildingClassCreatedCount;
	ArrayEnumMap<ProjectTypes,int> m_aiProjectCreatedCount;
	ArrayEnumMap<CivicTypes,int,char> m_aiForceCivicCount;

	ArrayEnumMap<VoteTypes,PlayerVoteTypes> m_aiVoteOutcome;
	ArrayEnumMap<ReligionTypes,int,void*,-1> m_aiReligionGameTurnFounded;
	ArrayEnumMap<CorporationTypes,int,void*,-1> m_aiCorporationGameTurnFounded;
	ArrayEnumMap<VoteSourceTypes,int> m_aiSecretaryGeneralTimer;
	ArrayEnumMap<VoteSourceTypes,int> m_aiVoteTimer;
	ArrayEnumMap<VoteSourceTypes,int> m_aiDiploVote;
	/*	advc (note): Used to be used for ICBM, unused since BtS.
		SpecialBuildingValid is still used for Bomb Shelters. */
	ArrayEnumMap<SpecialUnitTypes,bool> m_abSpecialUnitValid;
	ArrayEnumMap<SpecialBuildingTypes,bool> m_abSpecialBuildingValid;
	ArrayEnumMap<ReligionTypes,bool> m_abReligionSlotTaken;

	ArrayEnumMap<ReligionTypes,PlotNumTypes> m_aeHolyCity;
	ArrayEnumMap<CorporationTypes,PlotNumTypes> m_aeHeadquarters;
	IDInfo* m_pLegacyOrgSeatData;
	//int** m_apaiPlayerVote; // obsoleted by BtS
	// </advc.enum>
	std::vector<CvWString> m_aszDestroyedCities;
	std::vector<CvWString> m_aszGreatPeopleBorn;

	std::hash_map<int, std::hash_map<int, int> >* m_aiCivilizationHistory; // doc // TODO: refactor

	FFreeListTrashArray<VoteSelectionData> m_voteSelections;
	FFreeListTrashArray<VoteTriggeredData> m_votesTriggered;
	FFreeListTrashArray<CvDeal> m_deals;
	/*  <advc.072> Not serialized. One for use by CvPlayer::getItemTradeString,
		the other for CvDLLWidgetData::parseTradeItem. */
	CLinkList<DealItemData> m_currentDeals;
	CLinkList<DealItemData> m_currentDealsWidget;
	mutable bool m_bShowingCurrentDeals;
	// </advc.072>

	// <advc.027b>
	struct InitialRandSeed
	{
		uint uiMap;
		uint uiSync;
	} m_initialRandSeed;
	// </advc.027b>
	ReplayMessageList m_listReplayMessages;
	CvReplayInfo* m_pReplayInfo;
	int m_iNumSessions;
	int m_iMapRegens; // advc.tsl
	CvHallOfFameInfo* m_pHallOfFame; // advc.106i

	BarbarianWeightMap* m_pBarbarianWeightMap; // advc.304 (serialized by CvMap)
	// <advc.enum> Replacing hash_map, vector
	ArrayEnumMap<VoteSourceTypes,ReligionTypes> m_aeVoteSourceReligion;
	ArrayEnumMap<EventTriggerTypes,bool> m_abInactiveTriggers; // </advc.enum>

	/*  K-Mod. This is used to track which groups have been cycled through in the current turn.
		Note: it does not need to be kept in sync for multiplayer games. */
	std::set<int> m_aiActivePlayerCycledGroups; // advc: Was public; public getter added.

	// cache some frequently used values
	/*int m_iShrineBuildingCount;
	int* m_aiShrineBuilding;
	int* m_aiShrineReligion;*/ // advc.enum: Handled directly by CvCity now
	int m_iNumCultureVictoryCities;
	CultureLevelTypes m_eCultureVictoryCultureLevel;

	StartPointsAsHandicap* m_pSpah; // advc.250b
	RiseFall* m_pRiseFall; // advc.700

	// doc
	EagerEnumMap<TeamTypes, int, char> m_aiTechRankTeam;
	ListEnumMap<CivilizationTypes, PeriodTypes, char> m_aeCivPeriod;
	ListEnumMap<TechTypes, CivilizationTypes, char> m_aeFirstDiscovered;
	ListEnumMap<TechTypes, int, short> m_aeFirstDiscoveredTurn;
	History* m_apCivilizationHistory[NUM_CIVILIZATION_TYPES]; // TODO: grow for every civ in CvGame::doTurn, set for every player in CvPlayer::doTurn

	void uninit();
	void setStartTurnYear(int iTurn = 0); // advc.250c
	void initScenario(); // advc.051

	void setPlayerColors(); // advc.002i
	void initGameHandicap(); // advc.127
	void initFreeState();
	void initFreeCivState(); // advc.tsl
	/* <advc.027> */ NormalizationTarget* /* </advc.027> */ assignStartingPlots();
	void normalizeStartingPlots(/* advc.027: */ NormalizationTarget const* pTarget = NULL);
	void updateStartingPlotRange() const; // advc.opt
	void applyOptionEffects(bool bEnableAll = false); // advc.310
	void doTurn();
	void doDeals();
	void doGlobalWarming();
	CvPlot* getRandGWPlot(int iPool); // K-Mod
	void doHolyCity();
	// <advc.138>
	int religionPriority(TeamTypes eTeam, ReligionTypes eReligion) const;
	int religionPriority(PlayerTypes ePlayer, ReligionTypes eReligion) const;
	// </advc.138>
	void doHeadquarters();
	void doDiploVote();
	void doVoteResults();
	void doVoteSelection();

	void createBarbarianCities();
	void createBarbarianUnits();
	void createAnimals();
	// <advc.300>
	void createBarbarianCity(bool bNoCivCities, int iProbModifierPercent = 100);
	int numBarbariansToCreate(int iTilesPerUnit, int iTiles, int iUnowned,
			int iUnitsPresent);
	int createBarbarianUnits(int iUnitsToCreate, int iUnitsPresent, CvArea& kArea,
			Shelf* pShelf = NULL, bool bCargoAllowed = false, bool bOnlyCargo = false);
	CvPlot* randomBarbarianPlot(int& iValid, CvArea const& kArea,
			Shelf const* pShelf = NULL);
	bool killBarbarian(int iUnitsPresent, int iTiles, int iPop,
			CvArea& kArea, Shelf* pShelf = NULL);
	UnitTypes randomBarbarianUnit(UnitAITypes eUnitAI, CvPlot const& kPlot);
	scaled barbarianPeakLandRatio() const;
	// </advc.300>

	void verifyCivics();

	void updateUnprofiled(); // advc.256
	void updateWar();
	void updateMoves();
	void updateTimers();
	void updateTurnTimer();

	void testAlive();
	void testVictory();
	void showEndGameSequence();
	int FPChecksum() const; // advc.003g
	void handleUpdateTimer(UpdateTimerTypes eTimerType); // advc.003r
	bool isValidReplayIndex(uint i) const; // advc

	void processVote(const VoteTriggeredData& kData, int iChange);

	//void normalizeStartingPlotLocations();
	// <advc.108b>
	void rearrangeTeamStarts(
			bool bOnlyWithinArea = false, scaled rInertia = 0); // advc.027
	void applyStartingLocHandicaps(/* advc.027: */ NormalizationTarget const* pStartValues);
	template<class Agent>
	void sortByStartingLocHandicap(
			std::vector<std::pair<Agent*,int> > const& kStartingLocPercentPerAgent,
			std::vector<Agent*>& kResult); // </advc.108b>
	int getTeamClosenessScore( // <advc>
			ArrayEnumMap2D<PlayerTypes,PlayerTypes,int> const& kDistances,
			std::vector<PlayerTypes> const& kStartingLocs); // </advc>
	void normalizeAddRiver();
	void normalizeRemovePeaks();
	void normalizeAddLakes();
	void normalizeRemoveBadFeatures();
	void normalizeRemoveBadTerrain();
	void normalizeAddFoodBonuses(/* advc.027: */ NormalizationTarget const* pTarget = NULL);
	void normalizeAddGoodTerrain();
	void normalizeAddExtras(/* advc.027: */ NormalizationTarget const* pTarget = NULL);
	// <advc>
	bool placeExtraBonus(PlayerTypes eStartPlayer, CvPlot& kPlot,
			bool bCheckCanPlace, bool bIgnoreLatitude, bool bRemoveFeature,
			bool bNoFood); // advc.108
	bool isNormalizationBonus(BonusTypes eBonus, PlayerTypes eStartPlayer, CvPlot const& kPlot,
			bool bCheckCanPlace, bool bIgnoreLatitude) const; // </advc>
	CvPlot* normalizeFindLakePlot(PlayerTypes ePlayer);
	// <advc.108>
	bool normalizeCanAddLakeTo(CvPlot const& kPlot) const;
	bool skipDuplicateNormalizationBonus(CvPlot const& kStartPlot, CvPlot const& kPlot,
			BonusTypes eBonus, bool bSecondPass = false);
	bool isPowerfulStartingBonus(CvPlot const& kPlot, PlayerTypes eStartPlayer) const;
	bool isWeakStartingFoodBonus(CvPlot const& kPlot, PlayerTypes eStartPlayer) const;
	// </advc.108>  <advc>
	void doUpdateCacheOnTurn();
	CvUnit* getPlotUnits(CvPlot const* pPlot, std::vector<CvUnit*>* pPlotUnits,
			int iIndex = -1) const; // </advc>

private: // advc.003u: (See comments in the private section of CvPlayer.h)
	//virtual void AI_initExternal();
	virtual void AI_resetExternal();
	virtual void AI_makeAssignWorkDirtyExternal();
	virtual void AI_updateAssignWorkExternal();
	virtual int AI_combatValueExternal(UnitTypes eUnit);
};

/*	<advc.007c> Some macros to make the RNG functions of the singleton
	CvGame instance less tedious to use */

// Implementation files can re-define this to use a different CvGame instance
#define CVGAME_INSTANCE_FOR_RNG GC.getGame()

inline CvRandom& syncRand()
{
	return CVGAME_INSTANCE_FOR_RNG.getSorenRand();
}
inline CvRandom& mapRand()
{
	return CVGAME_INSTANCE_FOR_RNG.getMapRand();
}
// These have to be macros to let CALL_LOC_STR expand to the proper code location
#define SyncRandNum(iNumOutcomes) \
	CVGAME_INSTANCE_FOR_RNG.getSorenRandNum((iNumOutcomes), CALL_LOC_STR)
#define SyncRandFract(ScaledNumType) \
	ScaledNumType::rand(syncRand(), CALL_LOC_STR)
#define SyncRandSuccess(rSuccessProb) \
	(rSuccessProb).randSuccess(syncRand(), CALL_LOC_STR)
/*	(Implementing this through conversion to ScaledNum would lead to
	precision problems or unnecessary arithmetic operations.) */
#define SyncRandSuccessRatio(iNumerator, iDenominator) \
	((iNumerator) > 0 && ((iNumerator) >= (iDenominator) || (iNumerator) > SyncRandNum(iDenominator)))
#define SyncRandSuccess100(iSuccessPercent) \
	SyncRandSuccessRatio(iSuccessPercent, 100)
#define SyncRandSuccess1000(iSuccessPermille) \
	SyncRandSuccessRatio(iSuccessPermille, 1000)
#define SyncRandSuccess10000(iSuccessPermyriad) \
	SyncRandSuccessRatio(iSuccessPermyriad, 10000)
// Not sure what to name this one. Success has 1 chance in iNumLots.
#define SyncRandOneChanceIn(iNumLots) \
	(SyncRandNum(iNumLots) == 0)

// Same as above, replacing "Sync" with "Map".
#define MapRandNum(iNumOutcomes) \
	CVGAME_INSTANCE_FOR_RNG.getMapRandNum((iNumOutcomes), CALL_LOC_STR)
#define MapRandFract(ScaledNumType) \
	ScaledNumType::rand(mapRand(), CALL_LOC_STR)
#define MapRandSuccess(rSuccessProb) \
	(rSuccessProb).randSuccess(mapRand(), CALL_LOC_STR)
#define MapRandSuccessRatio(iNumerator, iDenominator) \
	((iNumerator) > 0 && ((iNumerator) >= (iDenominator) || (iNumerator) > MapRandNum(iDenominator)))
#define MapRandSuccess100(iSuccessPercent) \
	MapRandSuccessRatio(iSuccessPercent, 100)
#define MapRandSuccess1000(iSuccessPermille) \
	MapRandSuccessRatio(iSuccessPermille, 1000)
#define MapRandSuccess10000(iSuccessPermyriad) \
	MapRandSuccessRatio(iSuccessPermyriad, 10000)
#define MapRandOneChanceIn(iNumLots) \
	(MapRandNum(iNumLots) == 0)
// </advc.007c>

#endif
