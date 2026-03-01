#pragma once

#ifndef CIV4_INITCORE_H
#define CIV4_INITCORE_H


class CvInitCore /* advc.003e */ : boost::noncopyable
{
public:

	CvInitCore();
	virtual ~CvInitCore();
	/*	advc: Moved up so that all virtual functions are in one place.
		The EXE calls read and write but not the destructor. */
	virtual void read(FDataStreamBase* pStream);
	virtual void write(FDataStreamBase* pStream);

	DllExport void init(GameMode eMode);

protected:

	void uninit();
	void reset(GameMode eMode);

	void setDefaults();

	bool checkBounds(int iValue, int iLower, int iUpper) const
	{
		return (iLower <= iValue && iValue < iUpper);
	}

public:

	// Applications of data ...

	DllExport bool getHuman(PlayerTypes eID) const;
	int getNumHumans() const;

	DllExport int getNumDefinedPlayers() const;

	DllExport bool getMultiplayer() const;
	DllExport bool getNewGame() const;
	DllExport bool getSavedGame() const;
	DllExport bool getGameMultiplayer() const
	{
		return (getMultiplayer() || getPitboss() || getPbem() || getHotseat());
	}
	DllExport bool getPitboss() const;
	DllExport bool getHotseat() const;
	DllExport bool getPbem() const;

	DllExport bool getSlotVacant(PlayerTypes eID) const;
	DllExport PlayerTypes getAvailableSlot();
	DllExport void reassignPlayer(PlayerTypes eOldID, PlayerTypes eNewID);

	DllExport void closeInactiveSlots();
	DllExport void reopenInactiveSlots();

	void resetGame(/* advc.enum: */ bool bBeforeRead = false);
	DllExport void resetGame(CvInitCore* pSource, bool bClear = true, bool bSaveGameType = false);
	DllExport void resetPlayers() /* <advc.enum> */ { resetPlayers(false); }
	void resetPlayers(bool bBeforeRead); // </advc.enum>
	DllExport void resetPlayers(CvInitCore* pSource, bool bClear = true, bool bSaveSlotInfo = false);
	void resetPlayer(PlayerTypes eID, /* advc.enum: */ bool bBeforeRead = false);
	DllExport void resetPlayer(PlayerTypes eID, CvInitCore* pSource, bool bClear = true, bool bSaveSlotInfo = false);


	/*	Member access ... (advc.003k, note: The non-exported getters aren't called
		by the EXE but were originally exported and have, apparently, been
		inline-expanded. I.e. the EXE will access the respective members directly
		through a memory offset.) */

	const CvWString& getGameName() const { return m_szGameName; } // TODO: remove cpp override
	DllExport void setGameName(const CvWString& szGameName);

	const CvWString& getGamePassword() const { return m_szGamePassword; }
	DllExport void setGamePassword(const CvWString& szGamePassword);

	const CvWString& getAdminPassword() const { return m_szAdminPassword; }
	DllExport void setAdminPassword(const CvWString& szAdminPassword, bool bEncrypt = true);

	DllExport CvWString getMapScriptName() const;
	DllExport void setMapScriptName(const CvWString& szMapScriptName);
	DllExport bool getWBMapScript() const;
	bool isPangaea() const { return m_bPangaea; } // advc
	// advc (note): This appears to say whether a scenario uses random players
	bool getWBMapNoPlayers() const { return m_bWBMapNoPlayers; }
	void setWBMapNoPlayers(bool bValue) { m_bWBMapNoPlayers = bValue; }

	WorldSizeTypes getWorldSize() const { return m_eWorldSize; }
	void setWorldSize(WorldSizeTypes eWorldSize) { m_eWorldSize = eWorldSize; }
	DllExport void setWorldSize(const CvWString& szWorldSize);
	DllExport const CvWString& getWorldSizeKey(CvWString& szBuffer) const;

	ClimateTypes getClimate() const { return m_eClimate; }
	void setClimate(ClimateTypes eClimate) { m_eClimate = eClimate; }
	DllExport void setClimate(const CvWString& szClimate);
	DllExport const CvWString& getClimateKey(CvWString& szBuffer) const;

	SeaLevelTypes getSeaLevel() const { return m_eSeaLevel; }
	void setSeaLevel(SeaLevelTypes eSeaLevel) { m_eSeaLevel = eSeaLevel; }
	DllExport void setSeaLevel(const CvWString& szSeaLevel);
	DllExport const CvWString& getSeaLevelKey(CvWString& szBuffer) const;

	EraTypes getEra() const { return m_eEra; }
	void setEra(EraTypes eEra) { m_eEra = eEra; }
	DllExport void setEra(const CvWString& szEra);
	DllExport const CvWString& getEraKey(CvWString& szBuffer) const;

	GameSpeedTypes getGameSpeed() const { return m_eGameSpeed; }
	void setGameSpeed(GameSpeedTypes eGameSpeed) { m_eGameSpeed = eGameSpeed; }
	DllExport void setGameSpeed(const CvWString& szGameSpeed);
	DllExport const CvWString& getGameSpeedKey(CvWString& szBuffer) const;

	TurnTimerTypes getTurnTimer() const { return m_eTurnTimer; }
	void setTurnTimer(TurnTimerTypes eTurnTimer) { m_eTurnTimer = eTurnTimer; }
	void setTurnTimer(const CvWString& szTurnTimer);
	const CvWString& getTurnTimerKey(CvWString& szBuffer) const;

	CalendarTypes getCalendar() const { return m_eCalendar; }
	void setCalendar(CalendarTypes eCalendar) { m_eCalendar = eCalendar; }
	void setCalendar(const CvWString& szCalendar);
	const CvWString& getCalendarKey(CvWString& szBuffer) const;


	int getNumCustomMapOptions() const { return m_iNumCustomMapOptions; }
	int getNumHiddenCustomMapOptions() const { return m_iNumHiddenCustomMapOptions; }

	CustomMapOptionTypes const* getCustomMapOptions() const { return m_aeCustomMapOptions; }
	DllExport void setCustomMapOptions(int iNumCustomMapOptions,
			CustomMapOptionTypes const* aeCustomMapOptions);

	DllExport CustomMapOptionTypes getCustomMapOption(int iOptionID) const;
	DllExport void setCustomMapOption(int iOptionID, CustomMapOptionTypes eCustomMapOption);

	DllExport void setVictories(int iVictories, bool const* abVictories);
	DllExport bool getVictory(VictoryTypes eVictory) const;
	DllExport void setVictory(VictoryTypes eVictory, bool bVictory);

	DllExport bool getOption(GameOptionTypes eIndex) const { return m_abOptions.get(eIndex); }
	DllExport void setOption(GameOptionTypes eIndex, bool bOption);

	DllExport bool getMPOption(MultiplayerOptionTypes eIndex) const { return m_abMPOptions.get(eIndex); }
	DllExport void setMPOption(MultiplayerOptionTypes eIndex, bool bMPOption);

	bool getStatReporting() const { return m_bStatReporting; }
	void setStatReporting(bool bStatReporting) { m_bStatReporting = bStatReporting; }

	DllExport bool getForceControl(ForceControlTypes eIndex) const { return m_abForceControls.get(eIndex); }
	DllExport void setForceControl(ForceControlTypes eIndex, bool bForceControl);

	int getGameTurn() const { return m_iGameTurn; }
	void setGameTurn(int iGameTurn) { m_iGameTurn = iGameTurn; }

	int getMaxTurns() const { return m_iMaxTurns; }
	void setMaxTurns(int iMaxTurns) { m_iMaxTurns = iMaxTurns; }

	DllExport int getPitbossTurnTime() const { return m_iPitbossTurnTime; }
	DllExport void setPitbossTurnTime(int iPitbossTurnTime);

	int getTargetScore() const { return m_iTargetScore; }
	void setTargetScore(int iTargetScore) { m_iTargetScore = iTargetScore; }

	// Number of city eliminations permitted
	int getMaxCityElimination() const { return m_iMaxCityElimination; }
	void setMaxCityElimination(int iMaxCityElimination) { m_iMaxCityElimination = iMaxCityElimination; }

	int getNumAdvancedStartPoints() const { return m_iNumAdvancedStartPoints; }
	void setNumAdvancedStartPoints(int iNumPoints) { m_iNumAdvancedStartPoints = iNumPoints; }
	int getAdvancedStartMinPoints() const; // advc.250c

	DllExport unsigned int getSyncRandSeed() const { return m_uiSyncRandSeed; }
	DllExport void setSyncRandSeed(unsigned int uiSyncRandSeed);

	DllExport unsigned int getMapRandSeed() const { return m_uiMapRandSeed; }
	DllExport void setMapRandSeed(unsigned int uiMapRandSeed);

	PlayerTypes getActivePlayer() const { return m_eActivePlayer; }
	DllExport void setActivePlayer(PlayerTypes eActivePlayer);
	TeamTypes getActiveTeam() const { return m_eActiveTeam; } // advc.opt
	void updateActiveTeam(); // advc.opt

	DllExport GameType getType() const { return m_eType; }
	DllExport void setType(GameType eType);
	DllExport void setType(const CvWString& szType);
	bool getScenario() const; // advc.030

	GameMode getMode() const { return m_eMode; }
	DllExport void setMode(GameMode eMode);


	DllExport const CvWString& getLeaderName(PlayerTypes eID, uint uiForm = 0) const;
	DllExport void setLeaderName(PlayerTypes eID, const CvWString& szLeaderName);
	DllExport const CvWString& getLeaderNameKey(PlayerTypes eID) const;

	DllExport const CvWString& getCivDescription(PlayerTypes eID, uint uiForm = 0) const;
	DllExport void setCivDescription(PlayerTypes eID, const CvWString& szCivDescription);
	DllExport const CvWString& getCivDescriptionKey(PlayerTypes eID) const;

	DllExport const CvWString& getCivShortDesc(PlayerTypes eID, uint uiForm = 0) const;
	DllExport void setCivShortDesc(PlayerTypes eID, const CvWString& szCivShortDesc);
	DllExport const CvWString& getCivShortDescKey(PlayerTypes eID) const;

	DllExport const CvWString& getCivAdjective(PlayerTypes eID, uint uiForm = 0) const;
	DllExport void setCivAdjective(PlayerTypes eID, const CvWString& szCivAdjective);
	DllExport const CvWString& getCivAdjectiveKey(PlayerTypes eID) const;

	DllExport const CvWString& getCivPassword(PlayerTypes eID) const;
	DllExport void setCivPassword(PlayerTypes eID, const CvWString& szCivPassword, bool bEncrypt = true);

	DllExport const CvString& getEmail(PlayerTypes eID) const;
	DllExport void setEmail(PlayerTypes eID, const CvString& szEmail);

	DllExport const CvString& getSmtpHost(PlayerTypes eID) const;
	DllExport void setSmtpHost(PlayerTypes eID, const CvString& szHost);

	DllExport bool getWhiteFlag(PlayerTypes eID) const { return m_abWhiteFlag.get(eID); }
	DllExport void setWhiteFlag(PlayerTypes eID, bool bWhiteFlag);

	DllExport const CvWString& getFlagDecal(PlayerTypes eID) const;
	DllExport void setFlagDecal(PlayerTypes eID, const CvWString& szFlagDecal);


	DllExport CivilizationTypes getCiv(PlayerTypes eID) const { return m_aeCiv.get(eID); }
	DllExport void setCiv(PlayerTypes eID, CivilizationTypes eCiv);

	DllExport LeaderHeadTypes getLeader(PlayerTypes eID) const { return m_aeLeader.get(eID); }
	void setLeader(PlayerTypes eID, LeaderHeadTypes eLeader);
	// advc.191: (exported through .def file)
	void setLeaderExternal(PlayerTypes eID, LeaderHeadTypes eLeader);
	// // <advc.190c> (all exposed to Python via CvPlayer, CvGame)
	bool wasCivRandomlyChosen(PlayerTypes eID) const;
	bool wasLeaderRandomlyChosen(PlayerTypes eID) const;
	bool isCivLeaderSetupKnown() const { return m_bCivLeaderSetupKnown; }
	// Just for network sync
	void setCivLeaderRandomlyChosen(PlayerTypes eID, bool bRandomCiv, bool bRandomLeader);
	// </advc.190c>
	DllExport TeamTypes getTeam(PlayerTypes eID) const { return m_aeTeam.get(eID); }
	DllExport void setTeam(PlayerTypes eID, TeamTypes eTeam);

	DllExport HandicapTypes getHandicap(PlayerTypes eID) const { return m_aeHandicap.get(eID); }
	DllExport void setHandicap(PlayerTypes eID, HandicapTypes eHandicap);

	DllExport PlayerColorTypes getColor(PlayerTypes eID) const { return m_aeColor.get(eID); }
	DllExport void setColor(PlayerTypes eID, PlayerColorTypes eColor);

	DllExport ArtStyleTypes getArtStyle(PlayerTypes eID) const { return m_aeArtStyle.get(eID); }
	DllExport void setArtStyle(PlayerTypes eID, ArtStyleTypes eArtStyle);


	DllExport SlotStatus getSlotStatus(PlayerTypes eID) const;
	DllExport void setSlotStatus(PlayerTypes eID, SlotStatus eSlotStatus);

	DllExport SlotClaim getSlotClaim(PlayerTypes eID) const;
	DllExport void setSlotClaim(PlayerTypes eID, SlotClaim eSlotClaim);


	DllExport bool getPlayableCiv(PlayerTypes eID) const;
	DllExport void setPlayableCiv(PlayerTypes eID, bool bPlayableCiv);

	DllExport bool getMinorNationCiv(PlayerTypes eID) const { return m_abMinorNationCiv.get(eID); }
	DllExport void setMinorNationCiv(PlayerTypes eID, bool bMinorNationCiv);


	DllExport int getNetID(PlayerTypes eID) const { return m_aiNetID.get(eID); }
	DllExport void setNetID(PlayerTypes eID, int iNetID);

	DllExport bool getReady(PlayerTypes eID) const { return m_abReady.get(eID); }
	DllExport void setReady(PlayerTypes eID, bool bReady);

	DllExport const CvString& getPythonCheck(PlayerTypes eID) const;
	DllExport void setPythonCheck(PlayerTypes eID, const CvString& iPythonCheck);

	DllExport const CvString& getXMLCheck(PlayerTypes eID) const;
	DllExport void setXMLCheck(PlayerTypes eID, const CvString& iXMLCheck);

	DllExport void resetAdvancedStartPoints();

	void externalRNGCall(int iUpper, CvRandom const* pRandom); // advc.190c

protected:
	/* advc.003k (caveat): It's not safe to add data members to this class
		nor to reorder the existing data members, probably due to inlined
		getter functions. After the declaration of m_eMode, it seems to be OK
		to add and rearrange stuff. */
	// CORE GAME INIT DATA ...

	// Game type
	GameType m_eType;

	// Descriptive strings about game and map
	CvWString m_szGameName;
	CvWString m_szGamePassword;
	CvWString m_szAdminPassword;
	CvWString m_szMapScriptName;

	bool m_bWBMapNoPlayers;

	// Standard game parameters
	WorldSizeTypes m_eWorldSize;
	ClimateTypes m_eClimate;
	SeaLevelTypes m_eSeaLevel;
	EraTypes m_eEra;
	GameSpeedTypes m_eGameSpeed;
	TurnTimerTypes m_eTurnTimer;
	CalendarTypes m_eCalendar;

	// Map-specific custom parameters
	int m_iNumCustomMapOptions;
	int m_iNumHiddenCustomMapOptions;
	CustomMapOptionTypes* m_aeCustomMapOptions;
	//bool m_bPangaea; // (advc: Can't add this here b/c it would change the memory layout)

	// Standard game options
	/*	advc.enum: Important to limit the size of these maps to 4 byte, so that the
		memory layout doesn't change when there are more than 32 options. */
	ArrayEnumMap<GameOptionTypes,bool,void*,false,false,4> m_abOptions;
	ArrayEnumMap<MPOptionTypes,bool,void*,false,false,4> m_abMPOptions;
	bool m_bStatReporting;
	/*	advc: Not related to "standard game options". But here's a good place
		to add a bool b/c of padding; the memory layout stays the same. */
	bool m_bPangaea;
	ArrayEnumMap<ForceControlTypes,bool,void*,false,false,4> m_abForceControls; // (unsaved)

	// Dynamic victory condition setting
	/*	(advc.enum: ^Whatever that means? Using a dummy variable and an EnumMap instead
		has been crashing the EXE. Could give it another try now that data is properly
		reset before reading savegames ...) */
	int m_iNumVictories;
	bool* m_abVictories;

	// Game turn mgmt
	int m_iGameTurn;
	int m_iMaxTurns;
	int m_iPitbossTurnTime;
	int m_iTargetScore;

	int m_iMaxCityElimination;
	int m_iNumAdvancedStartPoints;

	// Unsaved data
	unsigned int m_uiSyncRandSeed;
	unsigned int m_uiMapRandSeed;
	PlayerTypes m_eActivePlayer;
	GameMode m_eMode;

	// advc (note): From here on, it seems to be OK to change the memory layout.

	// advc.opt: Convenient to cache this here b/c this header gets precompiled
	TeamTypes m_eActiveTeam;

	// Temp var so we don't return locally scoped var
	mutable CvWString m_szTemp;
	mutable CvString m_szTempA;


	// CORE PLAYER INIT DATA ...

	// Civ details
	CvWString* m_aszLeaderName;
	CvWString* m_aszCivDescription;
	CvWString* m_aszCivShortDesc;
	CvWString* m_aszCivAdjective;
	CvWString* m_aszCivPassword;
	CvString* m_aszEmail;
	CvString* m_aszSmtpHost;
	size_t m_uiTotalNameLength; // advc.003k

	CvWString* m_aszFlagDecal;
	ArrayEnumMap<PlayerTypes,bool> m_abWhiteFlag;

	EagerEnumMap<PlayerTypes,CivilizationTypes> m_aeCiv;
	EagerEnumMap<PlayerTypes,LeaderHeadTypes> m_aeLeader;
	EagerEnumMap<PlayerTypes,TeamTypes> m_aeTeam;
	EagerEnumMap<PlayerTypes,HandicapTypes> m_aeHandicap;
	EagerEnumMap<PlayerTypes,PlayerColorTypes> m_aeColor;
	EagerEnumMap<PlayerTypes,ArtStyleTypes> m_aeArtStyle;
	// <advc.190c>
	ArrayEnumMap<PlayerTypes,bool> m_abCivChosenRandomly;
	ArrayEnumMap<PlayerTypes,bool> m_abLeaderChosenRandomly;
	bool m_bCivLeaderSetupKnown; // </advc.190c>

	// Slot data
	SlotStatus* m_aeSlotStatus;
	SlotClaim* m_aeSlotClaim;

	// Civ flags
	ArrayEnumMap<PlayerTypes,bool> m_abPlayableCiv;
	EagerEnumMap<PlayerTypes,bool> m_abMinorNationCiv;

	// Unsaved player data
	// (advc.enum: Store player net ids as PlayerTypes values)
	ArrayEnumMap<PlayerTypes,PlayerTypes> m_aiNetID;
	ArrayEnumMap<PlayerTypes,bool> m_abReady;

	CvString* m_aszPythonCheck;
	CvString* m_aszXMLCheck;
	mutable CvString m_szTempCheck;

	void reRandomizeCivsAndLeaders(); // advc.191

	void clearCustomMapOptions();
	void refreshCustomMapOptions();
	void updatePangaea(); // advc
	void countNameLength(CvWString const& kName);

	/*void clearVictories();
	void refreshVictories();*/ // advc: Easier to understand w/o these
};

/*  advc.003k: OK to increase the size of CvInitCore (and to update or remove this
	assertion). Just make sure that new data members are added in the right place.
	And think about whether they need to by synchronized in network games. */
BOOST_STATIC_ASSERT(sizeof(CvInitCore) ==
		(sizeof(ArrayEnumMap<PlayerTypes,bool>) > 4 ? 448 : 424));
// <advc>
BOOST_STATIC_ASSERT(
		// Custom Game screen probably relies on these
		GAMEOPTION_LEAD_ANY_CIV == 7 && GAMEOPTION_ADVANCED_START == 0 &&
		// EXE relies on this for assigning the random personalities
		GAMEOPTION_RANDOM_PERSONALITIES == 8 &&
		// EXE explicitly sets this one to false (under unknown circumstances)
		GAMEOPTION_LOCK_MODS == 18); // </advc>

#endif
