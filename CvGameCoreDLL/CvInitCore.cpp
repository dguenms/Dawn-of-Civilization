#include "CvGameCoreDLL.h"
#include "CvInitCore.h"
#include "CvPlayer.h"
#include "CvInfo_GameOption.h"


CvInitCore::CvInitCore()
{
	m_aszLeaderName = new CvWString[MAX_PLAYERS];
	m_aszCivDescription = new CvWString[MAX_PLAYERS];
	m_aszCivShortDesc = new CvWString[MAX_PLAYERS];
	m_aszCivAdjective = new CvWString[MAX_PLAYERS];
	m_aszCivPassword = new CvWString[MAX_PLAYERS];
	m_aszEmail = new CvString[MAX_PLAYERS];
	m_aszSmtpHost = new CvString[MAX_PLAYERS];
	m_aszFlagDecal = new CvWString[MAX_PLAYERS];
	m_aszPythonCheck = new CvString[MAX_PLAYERS];
	m_aszXMLCheck = new CvString[MAX_PLAYERS];

	m_aeSlotStatus = new SlotStatus[MAX_PLAYERS];
	m_aeSlotClaim = new SlotClaim[MAX_PLAYERS];

	m_aeCustomMapOptions = NULL;
	m_abVictories = NULL;

	reset(NO_GAMEMODE);
}

CvInitCore::~CvInitCore()
{
	uninit();

	SAFE_DELETE_ARRAY(m_aszLeaderName);
	SAFE_DELETE_ARRAY(m_aszCivDescription);
	SAFE_DELETE_ARRAY(m_aszCivShortDesc);
	SAFE_DELETE_ARRAY(m_aszCivAdjective);
	SAFE_DELETE_ARRAY(m_aszCivPassword);
	SAFE_DELETE_ARRAY(m_aszEmail);
	SAFE_DELETE_ARRAY(m_aszSmtpHost);
	SAFE_DELETE_ARRAY(m_aszFlagDecal);
	SAFE_DELETE_ARRAY(m_aszPythonCheck);
	SAFE_DELETE_ARRAY(m_aszXMLCheck);
	SAFE_DELETE_ARRAY(m_aeSlotStatus);
	SAFE_DELETE_ARRAY(m_aeSlotClaim);
}

void CvInitCore::init(GameMode eMode)
{
	//--------------------------------
	// Init saved data
	reset(eMode);
}

void CvInitCore::uninit()
{
	// <advc.003w> So that memory doesn't remain allocated after exit to opening menu
	if (GC.IsGraphicsInitialized())
	{
		for (int i = 0; i < MAX_CIV_PLAYERS; i++)
			setCiv((PlayerTypes)i, NO_CIVILIZATION);
	} // </advc.003w>
	clearCustomMapOptions();
	SAFE_DELETE_ARRAY(m_abVictories);
	m_iNumVictories = 0;
}

// Initializes data members that are serialized.
void CvInitCore::reset(GameMode eMode)
{
	uninit();
	resetGame();
	resetPlayers();
	setMode(eMode);
	if (getMode() != NO_GAMEMODE)
		setDefaults();
}

void CvInitCore::setDefaults()
{
	FOR_EACH_ENUM(GameOption)
	{
		m_abOptions.set(eLoopGameOption, GC.getInfo(eLoopGameOption).getDefault());
	}
	FOR_EACH_ENUM(MPOption)
	{
		m_abMPOptions.set(eLoopMPOption, GC.getInfo(eLoopMPOption).getDefault());
	}
}


bool CvInitCore::getHuman(PlayerTypes eID) const
{
	if (getSlotStatus(eID) == SS_TAKEN)
		return true;
	if (getSlotStatus(eID) == SS_OPEN)
		return (gDLL->isGameActive() || getHotseat() || getPitboss() || getPbem());
	return false;
}

int CvInitCore::getNumHumans() const
{
	int iNumHumans = 0;
	for (int i = 0; i < MAX_CIV_PLAYERS; i++)
	{
		if (getHuman((PlayerTypes)i))
			iNumHumans++;
	}
	return iNumHumans;
}

int CvInitCore::getNumDefinedPlayers() const
{
	int iCount = 0;
	for (int i = 0; i < MAX_CIV_PLAYERS; i++)
	{
		PlayerTypes eLoopPlayer = (PlayerTypes)i;
		if (getCiv(eLoopPlayer) != NO_CIVILIZATION &&
			getLeader(eLoopPlayer) != NO_LEADER)
		{
			iCount++;
		}
	}
	return iCount;
}

bool CvInitCore::getMultiplayer() const
{
	switch (getType())
	{
	case GAME_MP_NEW:
	case GAME_MP_LOAD:
	case GAME_MP_SCENARIO:
		return true;
	default:
		return false;
	}
}

bool CvInitCore::getNewGame() const
{
	switch (getType())
	{
	case GAME_SP_NEW:
	case GAME_SP_SCENARIO:
	case GAME_MP_NEW:
	case GAME_MP_SCENARIO:
	case GAME_HOTSEAT_NEW:
	case GAME_HOTSEAT_SCENARIO:
	case GAME_PBEM_NEW:
	case GAME_PBEM_SCENARIO:
		return true;
	default:
		return false;
	}
}

bool CvInitCore::getSavedGame() const
{
	switch (getType())
	{
	case GAME_SP_LOAD:
	case GAME_MP_LOAD:
	case GAME_HOTSEAT_LOAD:
	case GAME_PBEM_LOAD:
		return true;
	default:
		return false;
	}
}

bool CvInitCore::getPitboss() const
{
	return (getMode() == GAMEMODE_PITBOSS);
}

bool CvInitCore::getHotseat() const
{
	return (getType() == GAME_HOTSEAT_NEW ||
			getType() == GAME_HOTSEAT_SCENARIO ||
			getType() == GAME_HOTSEAT_LOAD);
}


bool CvInitCore::getPbem() const
{
	return (getType() == GAME_PBEM_NEW ||
			getType() == GAME_PBEM_SCENARIO ||
			getType() == GAME_PBEM_LOAD);
}


bool CvInitCore::getSlotVacant(PlayerTypes eID) const
{
	FAssertBounds(0, MAX_CIV_PLAYERS, eID);
	SlotStatus eStatus = getSlotStatus(eID);
	return ((eStatus == SS_OPEN ||
		(eStatus == SS_COMPUTER && getMPOption(MPOPTION_TAKEOVER_AI))) &&
		getSlotClaim(eID) != SLOTCLAIM_ASSIGNED);
}

// the next ID available
PlayerTypes CvInitCore::getAvailableSlot()
{
	// First check for open slots only
	for (int i = 0; i < MAX_CIV_PLAYERS; i++)
	{
		PlayerTypes eID = (PlayerTypes)i;
		if (getSlotClaim(eID) == SLOTCLAIM_UNASSIGNED && getSlotStatus(eID) == SS_OPEN)
		{
			setSlotClaim(eID, SLOTCLAIM_ASSIGNED);
			return eID;
		}
	}

	// That didn't work, check to see if we can assign computer slots
	if (getMPOption(MPOPTION_TAKEOVER_AI))
	{
		for (int i = 0; i < MAX_CIV_PLAYERS; i++)
		{
			PlayerTypes eID = (PlayerTypes)i;
			if (getSlotClaim(eID) == SLOTCLAIM_UNASSIGNED &&
				getSlotStatus(eID) == SS_COMPUTER)
			{
				setSlotClaim(eID, SLOTCLAIM_ASSIGNED);
				return eID;
			}
		}
	}

	return NO_PLAYER; // None available at all...
}

void CvInitCore::reassignPlayer(PlayerTypes eOldID, PlayerTypes eNewID)
{
	FAssertBounds(0, MAX_CIV_PLAYERS, eOldID);
	FAssertBounds(0, MAX_CIV_PLAYERS, eNewID);

	// *** SAVE TARGET SLOT DETAILS TEMPORARILY
	// Temp civ details
	CvWString szLeaderName = m_aszLeaderName[eNewID];
	CvWString szCivDescription = m_aszCivDescription[eNewID];
	CvWString szCivShortDesc = m_aszCivShortDesc[eNewID];
	CvWString szCivAdjective = m_aszCivAdjective[eNewID];
	CvWString szCivPassword = m_aszCivPassword[eNewID];
	CvString szEmail = m_aszEmail[eNewID];
	CvString szSmtpHost = m_aszSmtpHost[eNewID];
	bool bWhiteFlag = m_abWhiteFlag.get(eNewID);
	CvWString szFlagDecal = m_aszFlagDecal[eNewID];
	CivilizationTypes eCiv = m_aeCiv.get(eNewID);
	LeaderHeadTypes eLeader = m_aeLeader.get(eNewID);
	// <advc.190c>
	bool bRandomCiv = m_abCivChosenRandomly.get(eNewID);
	bool bRandomLeader = m_abCivChosenRandomly.get(eNewID);
	// </advc.190c>
	TeamTypes eTeam = m_aeTeam.get(eNewID);
	HandicapTypes eHandicap = m_aeHandicap.get(eNewID);
	PlayerColorTypes eColor = m_aeColor.get(eNewID);
	ArtStyleTypes eArtStyle = m_aeArtStyle.get(eNewID);
	// Temp slot data
	SlotStatus eSlotStatus = m_aeSlotStatus[eNewID];
	SlotClaim eSlotClaim = m_aeSlotClaim[eNewID];
	// Temp civ flags
	bool bPlayableCiv = m_abPlayableCiv.get(eNewID);
	bool bMinorNationCiv = m_abMinorNationCiv.get(eNewID);
	// Temp unsaved player data
	PlayerTypes eNetID = m_aiNetID.get(eNewID);
	bool bReady = m_abReady.get(eNewID);
	CvString szPythonCheck = m_aszPythonCheck[eNewID];
	CvString szXMLCheck = m_aszXMLCheck[eNewID];

	// *** SAVE OLD SLOT DETAILS IN NEW SLOT
	// New civ details
	m_aszLeaderName[eNewID] = m_aszLeaderName[eOldID];
	m_aszCivDescription[eNewID] = m_aszCivDescription[eOldID];
	m_aszCivShortDesc[eNewID] = m_aszCivShortDesc[eOldID];
	m_aszCivAdjective[eNewID] = m_aszCivAdjective[eOldID];
	m_aszCivPassword[eNewID] = m_aszCivPassword[eOldID];
	m_aszEmail[eNewID] = m_aszEmail[eOldID];
	m_aszSmtpHost[eNewID] = m_aszSmtpHost[eOldID];
	m_abWhiteFlag.set(eNewID, m_abWhiteFlag.get(eOldID));
	m_aszFlagDecal[eNewID] = m_aszFlagDecal[eOldID];
	//m_aeCiv[eNewID] = m_aeCiv[eOldID];
	setCiv(eNewID, m_aeCiv.get(eOldID)); // advc.003w
	m_aeLeader.set(eNewID, m_aeLeader.get(eOldID));
	// <advc.190c>
	m_abCivChosenRandomly.set(eNewID, m_abCivChosenRandomly.get(eOldID));
	m_abLeaderChosenRandomly.set(eNewID, m_abLeaderChosenRandomly.get(eOldID));
	// </advc.190c>
	m_aeTeam.set(eNewID, m_aeTeam.get(eOldID));
	m_aeHandicap.set(eNewID, m_aeHandicap.get(eOldID));
	m_aeColor.set(eNewID, m_aeColor.get(eOldID));
	m_aeArtStyle.set(eNewID, m_aeArtStyle.get(eOldID));
	// New slot data
	m_aeSlotStatus[eNewID] = m_aeSlotStatus[eOldID];
	m_aeSlotClaim[eNewID] = m_aeSlotClaim[eOldID];
	// New civ flags
	m_abPlayableCiv.set(eNewID, m_abPlayableCiv.get(eOldID));
	m_abMinorNationCiv.set(eNewID, m_abMinorNationCiv.get(eOldID));
	// New unsaved player data
	m_aiNetID.set(eNewID, m_aiNetID.get(eOldID));
	m_abReady.set(eNewID, m_abReady.get(eOldID));
	m_aszPythonCheck[eNewID] = m_aszPythonCheck[eOldID];
	m_aszXMLCheck[eNewID] = m_aszXMLCheck[eOldID];

	// *** SAVE TEMP DETAILS IN OLD SLOT
	// New civ details
	m_aszLeaderName[eOldID] = szLeaderName;
	m_aszCivDescription[eOldID] = szCivDescription;
	m_aszCivShortDesc[eOldID] = szCivShortDesc;
	m_aszCivAdjective[eOldID] = szCivAdjective;
	m_aszCivPassword[eOldID] = szCivPassword;
	m_aszEmail[eOldID] = szEmail;
	m_aszSmtpHost[eOldID] = szSmtpHost;
	m_abWhiteFlag.set(eOldID, bWhiteFlag);
	m_aszFlagDecal[eOldID] = szFlagDecal;
	//m_aeCiv[eOldID] = eCiv;
	setCiv(eOldID, eCiv); // advc.003w
	m_aeLeader.set(eOldID, eLeader);
	// <advc.190c>
	m_abCivChosenRandomly.set(eOldID, bRandomCiv);
	m_abLeaderChosenRandomly.set(eOldID, bRandomLeader);
	// </advc.190c>
	m_aeTeam.set(eOldID, eTeam);
	m_aeHandicap.set(eOldID, eHandicap);
	m_aeColor.set(eOldID, eColor);
	m_aeArtStyle.set(eOldID, eArtStyle);
	// New slot data
	m_aeSlotStatus[eOldID] = eSlotStatus;
	m_aeSlotClaim[eOldID] = eSlotClaim;
	// New civ flags
	m_abPlayableCiv.set(eOldID, bPlayableCiv);
	m_abMinorNationCiv.set(eOldID, bMinorNationCiv);
	// New unsaved player data
	m_aiNetID.set(eOldID, eNetID);
	m_abReady.set(eOldID, bReady);
	m_aszPythonCheck[eOldID] = szPythonCheck;
	m_aszXMLCheck[eOldID] = szXMLCheck;

	// We may have a new active player id...
	if (getActivePlayer() == eOldID)
		setActivePlayer(eNewID);
	else if (getActivePlayer() == eNewID)
		setActivePlayer(eOldID);

	if (CvPlayer::areStaticsInitialized())
	{
		GET_PLAYER(eOldID).updateTeamType();
		GET_PLAYER(eNewID).updateTeamType();
		GET_PLAYER(eOldID).updateHuman();
		GET_PLAYER(eNewID).updateHuman();
	}
}

/*	advc (caveat from C2C): When launching a network game, the EXE calls this only
	on the host. Must not add code here that needs to be synchronized.
	(Could add it e.g. in CvGame::init instead.) */
void CvInitCore::closeInactiveSlots()
{
	// Open inactive slots mean different things to different game modes and types...
	// Let's figure out what they mean for us

	for (int i = 0; i < MAX_CIV_PLAYERS; i++)
	{
		PlayerTypes eID = (PlayerTypes)i;
		if (getSlotStatus(eID) == SS_OPEN)
		{
			if (getPitboss() || getHotseat() || getPbem())
			{
				// Pitboss & hotseat - all "open" slots are non-present human players
				setSlotStatus(eID, SS_TAKEN);
			}
			else if (getType() == GAME_MP_SCENARIO)
			{
				// Multiplayer scenario - all "open" slots should be filled with an AI player
				setSlotStatus(eID, SS_COMPUTER);
			}
			else
			{
				// If it's a normal game, all "open" slots should be closed.
				setSlotStatus(eID, SS_CLOSED);
			}
			setSlotClaim(eID, SLOTCLAIM_UNASSIGNED);

			gDLL->sendPlayerInfo(eID);
		}
	}
}

void CvInitCore::reopenInactiveSlots()
{
	// "Inactive" open slots will only be in Pitboss and Hotseat
	if (getPitboss() || getHotseat() || getPbem())
	{
		for (int i = 0; i < MAX_CIV_PLAYERS; ++i)
		{
			PlayerTypes eID = (PlayerTypes)i;
			// Reopen all slots that don't have active connections
			if (getSlotStatus(eID) == SS_TAKEN)
			{
				if ( getSlotClaim(eID) != SLOTCLAIM_ASSIGNED )
				{
					setSlotStatus(eID, SS_OPEN);
				}
			}
		}
	}
}

void CvInitCore::resetGame(/* advc.enum: */ bool bBeforeRead)
{
	// Descriptive strings about game and map
	m_eType = GAME_NONE;
	m_szGameName.clear();
	m_szGamePassword.clear();
	m_szAdminPassword.clear();
	m_szMapScriptName.clear();
	m_bPangaea = false; // advc
	m_bWBMapNoPlayers = false;

	// Standard game parameters
	m_eWorldSize = NO_WORLDSIZE;		// STANDARD_ option?

	if (!bBeforeRead) // advc.enum (doesn't really matter ...)
	/*  <advc.003c> This function is called multiple times before XML is loaded.
		GC.getDefineINT returns 0 then, which is fine, but now also triggers
		a failed assertion. Therefore check if GC is done with the loading
		(and caching) of XML values.
		The in-line comments "NO_ option?" below are from the Vanilla developers.
		If I'd just set everything to NO_..., I'd have to set proper values at
		some later point though. */
	{
		bool cd = GC.isCachingDone();
		m_eClimate = cd ? (ClimateTypes)GC.getDefineINT("STANDARD_CLIMATE") : NO_CLIMATE;			// NO_ option?
		m_eSeaLevel = cd ? (SeaLevelTypes)GC.getDefineINT("STANDARD_SEALEVEL") : NO_SEALEVEL;		// NO_ option?
		m_eEra = cd ? (EraTypes)GC.getDefineINT("STANDARD_ERA") : NO_ERA;							// NO_ option?
		m_eGameSpeed = cd ? (GameSpeedTypes)GC.getDefineINT("STANDARD_GAMESPEED") : NO_GAMESPEED;	// NO_ option?
		m_eTurnTimer = cd ? (TurnTimerTypes)GC.getDefineINT("STANDARD_TURNTIMER") : NO_TURNTIMER;	// NO_ option?
		m_eCalendar = cd ? (CalendarTypes)GC.getDefineINT("STANDARD_CALENDAR") : NO_CALENDAR;		// NO_ option?
	} // </advc.003c>
	// Map-specific custom parameters
	clearCustomMapOptions();
	m_iNumHiddenCustomMapOptions = 0; // advc: ensure initialization
	// Data-defined victory conditions
	//refreshVictories();
	/*	<advc> Unrolling that function should make it easier to use an EnumMap instead
		-- if I ever take another stab at that, which probably I should not. */
	SAFE_DELETE_ARRAY(m_abVictories);
	if (!bBeforeRead) // advc.enum
	{
		m_iNumVictories = GC.getNumVictoryInfos();
		if (m_iNumVictories > 0)
		{
			m_abVictories = new bool[m_iNumVictories];
			for (int i = 0; i < m_iNumVictories; i++)
				m_abVictories[i] = true;
		} // </advc>
	}
	// Standard game options
	m_abOptions.reset();
	m_abMPOptions.reset();
	// <advc.enum>
	if (bBeforeRead)
		return; // </advc.enum>
	m_abForceControls.reset();
	m_iMaxCityElimination = 0;
	m_iNumAdvancedStartPoints = 0;

	// Misc
	m_bStatReporting = false;
	m_bCivLeaderSetupKnown = false; // advc.190c

	// Game turn mgmt
	m_iGameTurn = 0;
	m_iMaxTurns = 0;
	m_iPitbossTurnTime = 0;
	m_iTargetScore = 0;

	// Unsaved game data
	m_uiSyncRandSeed = 0;
	m_uiMapRandSeed = 0;
	m_eActivePlayer = NO_PLAYER;
	m_eActiveTeam = NO_TEAM; // advc.opt

	// Temp vars
	m_szTemp.clear();
}

/*	advc (note): This seems to get used for resetting CvGlobals::m_initCore and
	m_loadedInitCore to pSource = &CvGlobals::m_iniInitCore, i.e. (presumably)
	to the data stored in CivilizationIV.ini.
	Also used for resetting m_initCore to pSource = &m_loadedInitCore when
	loading a savegame. */
void CvInitCore::resetGame(CvInitCore* pSource, bool bClear, bool bSaveGameType)
{
	FAssert(pSource != NULL);
	FAssertMsg(!bClear || !bSaveGameType, "Should not clear while trying to preserve gametype info");
	if (bClear || pSource == NULL)
		resetGame();
	if (pSource == NULL)
		return;

	// Only copy over saved data

	// Descriptive strings about game and map
	if (!bSaveGameType || getGameMultiplayer() != pSource->getGameMultiplayer())
		setType(pSource->getType());
	setGameName(pSource->getGameName());
	setGamePassword(pSource->getGamePassword());
	setAdminPassword(pSource->getAdminPassword(), false);
	setMapScriptName(pSource->getMapScriptName());

	setWBMapNoPlayers(pSource->getWBMapNoPlayers());

	// Standard game parameters
	setWorldSize(pSource->getWorldSize());
	setClimate(pSource->getClimate());
	setSeaLevel(pSource->getSeaLevel());
	setEra(pSource->getEra());
	setGameSpeed(pSource->getGameSpeed());
	setTurnTimer(pSource->getTurnTimer());
	setCalendar(pSource->getCalendar());

	// Map-specific custom parameters
	setCustomMapOptions(pSource->getNumCustomMapOptions(), pSource->getCustomMapOptions());
	m_iNumHiddenCustomMapOptions = pSource->getNumHiddenCustomMapOptions();
	// <advc.enum>
	FOR_EACH_ENUM(Victory)
	{
		// Instead of calling that nasty (exported) setVictories function
		setVictory(eLoopVictory, pSource->getVictory(eLoopVictory));
	} // </advc.enum>

	// Standard game options
	FOR_EACH_ENUM(GameOption)
	{
		bool b = pSource->getOption(eLoopGameOption);
		// <kekm.18>
		CvGameOptionInfo const& kLoopGameOption = GC.getInfo(eLoopGameOption);
		if (!kLoopGameOption.getVisible())
			b = kLoopGameOption.getDefault(); // </kekm.18>
		setOption(eLoopGameOption, b);
	}
	FOR_EACH_ENUM(MPOption)
	{
		setMPOption(eLoopMPOption, pSource->getMPOption(eLoopMPOption));
	}
	setMaxCityElimination(pSource->getMaxCityElimination());
	setNumAdvancedStartPoints(pSource->getNumAdvancedStartPoints());

	// Misc
	setStatReporting(pSource->getStatReporting());
	m_bCivLeaderSetupKnown = pSource->m_bCivLeaderSetupKnown; // advc.190c

	// Game turn mgmt
	setGameTurn(pSource->getGameTurn());
	setMaxTurns(pSource->getMaxTurns());
	setPitbossTurnTime(pSource->getPitbossTurnTime());
	setTargetScore(pSource->getTargetScore());

	setSyncRandSeed(pSource->getSyncRandSeed());
	setMapRandSeed(pSource->getMapRandSeed());
}

void CvInitCore::resetPlayers(/* advc.enum: */ bool bBeforeRead)
{
	for (int i = 0; i < MAX_PLAYERS; ++i)
	{
		resetPlayer((PlayerTypes)i, /* advc.enum: */ bBeforeRead);
	}
}

void CvInitCore::resetPlayers(CvInitCore * pSource, bool bClear, bool bSaveSlotInfo)
{
	for (int i = 0; i < MAX_PLAYERS; ++i)
	{
		resetPlayer((PlayerTypes)i, pSource, bClear, bSaveSlotInfo);
	}
}

void CvInitCore::resetPlayer(PlayerTypes eID,
	bool bBeforeRead) // advc.enum
{
	FAssertBounds(0, MAX_PLAYERS, eID);

	// Civ details
	m_aszLeaderName[eID].clear();
	m_aszCivDescription[eID].clear();
	m_aszCivShortDesc[eID].clear();
	m_aszCivAdjective[eID].clear();
	m_aszCivPassword[eID].clear();
	m_aszEmail[eID].clear();
	m_aszSmtpHost[eID].clear();
	m_uiTotalNameLength = 0; // advc.003k

	m_abWhiteFlag.resetVal(eID);
	m_aszFlagDecal[eID].clear();

	m_aeCiv.resetVal(eID);
	m_aeLeader.resetVal(eID);
	// <advc.190c>
	m_abCivChosenRandomly.resetVal(eID);
	m_abLeaderChosenRandomly.resetVal(eID);
	// </advc.190c>
	m_aeTeam.set(eID, static_cast<TeamTypes>(eID));
	// <advc.003c> See comment in resetGame
	m_aeHandicap.set(eID, GC.isCachingDone() ?
			(HandicapTypes)GC.getDefineINT("STANDARD_HANDICAP") : NO_HANDICAP);
	// </advc.003c>
	m_aeColor.resetVal(eID);
	m_aeArtStyle.resetVal(eID);


	// Slot data
	m_aeSlotStatus[eID] = SS_CLOSED;
	m_aeSlotClaim[eID] = SLOTCLAIM_UNASSIGNED;

	// Civ flags
	m_abPlayableCiv.resetVal(eID);
	m_abMinorNationCiv.resetVal(eID);
	// <advc.001p>
	if (bBeforeRead)
	{	// Avoid crash when loading from within a game
		if (GET_PLAYER(eID).isEverAlive())
			GET_PLAYER(eID).reset(eID); // </advc.001p>
		return; // advc.enum
	}

	// Unsaved player data
	m_aiNetID.resetVal(eID);
	m_abReady.resetVal(eID);
	m_aszPythonCheck[eID].clear();
	m_aszXMLCheck[eID].clear();

	if (CvPlayer::areStaticsInitialized())
	{
		GET_PLAYER(eID).updateTeamType();
		GET_PLAYER(eID).updateHuman();
	}
}

void CvInitCore::resetPlayer(PlayerTypes eID, CvInitCore * pSource, bool bClear, bool bSaveSlotInfo)
{
	FAssert(pSource != NULL);
	FAssertBounds(0, MAX_PLAYERS, eID);
	FAssertMsg(!bClear || !bSaveSlotInfo, "Should not be clearing data while trying to preserve slot info in CvInitCore::resetPlayer");
	if (bClear || pSource == NULL)
		resetPlayer(eID);
	if (pSource == NULL)
		return; // advc

	// Only copy over saved data

	// Civ details
	setCivDescription(eID, pSource->getCivDescription(eID));
	setCivShortDesc(eID, pSource->getCivShortDesc(eID));
	setCivAdjective(eID, pSource->getCivAdjective(eID));

	setCivPassword(eID, pSource->getCivPassword(eID), false);
	setEmail(eID, pSource->getEmail(eID));
	setSmtpHost(eID, pSource->getSmtpHost(eID));
	setFlagDecal(eID, pSource->getFlagDecal(eID));
	setWhiteFlag(eID, pSource->getWhiteFlag(eID));

	setHandicap(eID, pSource->getHandicap(eID));
	setCiv(eID, pSource->getCiv(eID));
	setTeam(eID, pSource->getTeam(eID));
	setLeader(eID, pSource->getLeader(eID));
	// <advc.190c>
	m_abCivChosenRandomly.set(eID, pSource->m_abCivChosenRandomly.get(eID));
	m_abLeaderChosenRandomly.set(eID, pSource->m_abLeaderChosenRandomly.get(eID));
	// </advc.190c>
	setColor(eID, pSource->getColor(eID));
	setArtStyle(eID, pSource->getArtStyle(eID));

	setPlayableCiv(eID, pSource->getPlayableCiv(eID));
	setMinorNationCiv(eID, pSource->getMinorNationCiv(eID));

	if (!bSaveSlotInfo) // Slot data
	{
		// We don't wanna reset the slot data if we are loading a game
		// from init - we want to keep the changes we made during init
		setLeaderName(eID, pSource->getLeaderName(eID));
		setSlotStatus(eID, pSource->getSlotStatus(eID));
		setSlotClaim(eID, pSource->getSlotClaim(eID));
		// <advc.001p> Reset players while loading from within a game to avoid crash
		if (pSource->getSavedGame() && GET_PLAYER(eID).isEverAlive())
			GET_PLAYER(eID).reset(eID); // </advc.001p>
	}
}


CvWString CvInitCore::getMapScriptName() const
{
	if (!getWBMapScript() && // advc: Order switched; not sure what getTransferredMap does.
		gDLL->getTransferredMap())
	{
		// If it's a transferred Python file, we have to hack in the transferred extension
		return (m_szMapScriptName + CvWString(MAP_TRANSFER_EXT));
	}
	return m_szMapScriptName;
}

void CvInitCore::setMapScriptName(CvWString const& szMapScriptName)
{
	m_szMapScriptName = szMapScriptName;
	refreshCustomMapOptions();
	updatePangaea();
}

bool CvInitCore::getWBMapScript() const
{
	return (gDLL->isDescFileName(CvString(m_szMapScriptName).GetCString()));
}

/*  advc.030 (from Civ4Col): This only works at the start of a game b/c all savegames
	have type GAME_..._LOAD. Use CvGame::isScenario if it's not the start of a game. */
bool CvInitCore::getScenario() const
{
	switch(m_eType)
	{
	case GAME_SP_SCENARIO:
	case GAME_MP_SCENARIO:
	case GAME_HOTSEAT_SCENARIO:
	case GAME_PBEM_SCENARIO:
		return true;
	}
	return false;
}


void CvInitCore::setWorldSize(CvWString const& szWorldSize)
{
	FOR_EACH_ENUM(WorldSize)
	{
		if (wcsicmp(szWorldSize.GetCString(),
			CvWString(GC.getInfo(eLoopWorldSize).getType()).GetCString()) == 0 )
		{
			setWorldSize(eLoopWorldSize);
		}
	}
}

const CvWString& CvInitCore::getWorldSizeKey(CvWString& szBuffer) const
{
	if (checkBounds(getWorldSize(), 0, GC.getNumWorldInfos()))
	{
		szBuffer = GC.getInfo(getWorldSize()).getType();
		return szBuffer;
	}
	szBuffer = L"NO_WORLDSIZE";
	return szBuffer;
}

void CvInitCore::setClimate(CvWString const& szClimate)
{
	FOR_EACH_ENUM(Climate)
	{
		if (wcsicmp(szClimate.GetCString(),
			CvWString(GC.getInfo(eLoopClimate).getType()).GetCString()) == 0 )
		{
			setClimate(eLoopClimate);
		}
	}
}

const CvWString& CvInitCore::getClimateKey(CvWString& szBuffer) const
{
	if (checkBounds(getClimate(), 0, GC.getNumClimateInfos()))
	{
		szBuffer = GC.getInfo(getClimate()).getType();
		return szBuffer;
	}
	szBuffer = L"NO_CLIMATE";
	return szBuffer;
}

void CvInitCore::setSeaLevel(CvWString const& szSeaLevel)
{
	FOR_EACH_ENUM(SeaLevel)
	{
		if (wcsicmp(szSeaLevel.GetCString(),
			CvWString(GC.getInfo(eLoopSeaLevel).getType()).GetCString()) == 0)
		{
			setSeaLevel(eLoopSeaLevel);
		}
	}
}

const CvWString& CvInitCore::getSeaLevelKey(CvWString& szBuffer) const
{
	if (checkBounds(getSeaLevel(), 0, GC.getNumSeaLevelInfos()))
	{
		szBuffer = GC.getInfo(getSeaLevel()).getType();
		return szBuffer;
	}
	szBuffer = L"NO_SEALEVEL";
	return szBuffer;
}

void CvInitCore::setEra(CvWString const& szEra)
{
	FOR_EACH_ENUM(Era)
	{
		if (wcsicmp(szEra.GetCString(),
			CvWString(GC.getInfo(eLoopEra).getType()).GetCString()) == 0 )
		{
			setEra(eLoopEra);
		}
	}
}

const CvWString& CvInitCore::getEraKey(CvWString& szBuffer) const
{
	if (checkBounds(getEra(), 0, GC.getNumEraInfos()))
	{
		szBuffer = GC.getInfo(getEra()).getType();
		return szBuffer;
	}
	szBuffer = L"NO_ERA";
	return szBuffer;
}

void CvInitCore::setGameSpeed(CvWString const& szGameSpeed)
{
	FOR_EACH_ENUM(GameSpeed)
	{
		if (wcsicmp(szGameSpeed.GetCString(),
			CvWString(GC.getInfo(eLoopGameSpeed).getType()).GetCString()) == 0)
		{
			setGameSpeed(eLoopGameSpeed);
		}
	}
}

CvWString const& CvInitCore::getGameSpeedKey(CvWString& szBuffer) const
{
	if (checkBounds(getGameSpeed(), 0, GC.getNumGameSpeedInfos()))
	{
		szBuffer = GC.getInfo(getGameSpeed()).getType();
		return szBuffer;
	}
	szBuffer = L"NO_GAMESPEED";
	return szBuffer;
}

void CvInitCore::setTurnTimer(CvWString const& szTurnTimer)
{
	FOR_EACH_ENUM(TurnTimer)
	{
		if (wcsicmp(szTurnTimer.GetCString(),
			CvWString(GC.getInfo(eLoopTurnTimer).getType()).GetCString()) == 0 )
		{
			setTurnTimer(eLoopTurnTimer);
		}
	}
}

CvWString const& CvInitCore::getTurnTimerKey(CvWString& szBuffer) const
{
	if (checkBounds(getTurnTimer(), 0, GC.getNumTurnTimerInfos()))
	{
		szBuffer = GC.getInfo(getTurnTimer()).getType();
		return szBuffer;
	}
	szBuffer = L"NO_TURNTIMER";
	return szBuffer;
}

void CvInitCore::setCalendar(CvWString const& szCalendar)
{
	FOR_EACH_ENUM(Calendar)
	{
		if (wcsicmp(szCalendar.GetCString(),
			CvWString(GC.getInfo(eLoopCalendar).getType()).GetCString()) == 0 )
		{
			setCalendar(eLoopCalendar);
		}
	}
}

CvWString const& CvInitCore::getCalendarKey(CvWString& szBuffer) const
{
	if (checkBounds(getCalendar(), 0, NUM_CALENDAR_TYPES))
	{
		szBuffer = GC.getInfo(getCalendar()).getType();
		return szBuffer;
	}
	szBuffer = L"NO_CALENDAR";
	return szBuffer;
}


void CvInitCore::clearCustomMapOptions()
{
	SAFE_DELETE_ARRAY(m_aeCustomMapOptions);
	m_iNumCustomMapOptions = 0;
}

void CvInitCore::refreshCustomMapOptions()
{
	clearCustomMapOptions();
	if (getWBMapScript())
		return;
	CvString szMapScriptNameNarrow(getMapScriptName());
	char const* szMapScriptName = szMapScriptNameNarrow.GetCString();
	if (!gDLL->pythonMapExists(szMapScriptName))
	{	/*	advc: GAME_NONE means we're on the opening menu. The map script actually
			needs to be present at that point b/c that's (apparently) when the EXE
			caches the number of custom map options. However, this won't matter
			if the player then selects to load a savegame or start a scenario.
			We'll get another call upon entering a non-WB game setup screen;
			lets wait for that with the assertion - if the script can't be found
			earlier, it still won't be found then. */
		FAssertMsg(getType() == GAME_NONE || getType() == GAME_SP_LOAD, "Map script not found");
		return;
	}
	CvPythonCaller const& py = *GC.getPythonCaller();
	m_iNumHiddenCustomMapOptions = py.numCustomMapOptions(szMapScriptName, true);
	int iOptions = py.numCustomMapOptions(szMapScriptName, false);
	if (iOptions <= 0)
		return;

	CustomMapOptionTypes* aeMapOptions = new CustomMapOptionTypes[iOptions];
	for (int i = 0; i < iOptions; i++)
		aeMapOptions[i] = py.customMapOptionDefault(szMapScriptName, i);
	setCustomMapOptions(iOptions, aeMapOptions);
	SAFE_DELETE_ARRAY(aeMapOptions);
}

// advc:
void CvInitCore::updatePangaea()
{
	// That's the name of the .py file; not language-dependent.
	m_bPangaea = (getMapScriptName().compare(L"Pangaea") == 0);
}

void CvInitCore::setCustomMapOptions(int iNumCustomMapOptions,
	CustomMapOptionTypes const* aeCustomMapOptions)
{
	clearCustomMapOptions();
	if (iNumCustomMapOptions > 0)
	{
		FAssertMsg(aeCustomMapOptions != NULL, "CustomMap Num/Pointer mismatch in CvInitCore::setCustomMapOptions");
		m_iNumCustomMapOptions = iNumCustomMapOptions;
		m_aeCustomMapOptions = new CustomMapOptionTypes[m_iNumCustomMapOptions];
		for (int i = 0; i < m_iNumCustomMapOptions; ++i)
		{
			m_aeCustomMapOptions[i] = aeCustomMapOptions[i];
		}
	}
}

CustomMapOptionTypes CvInitCore::getCustomMapOption(int iOptionID) const
{
	FAssertBounds(0, m_iNumCustomMapOptions, iOptionID);
	if (checkBounds(iOptionID, 0, m_iNumCustomMapOptions))
		return m_aeCustomMapOptions[iOptionID];
	return NO_CUSTOM_MAPOPTION;
}

void CvInitCore::setCustomMapOption(int iOptionID, CustomMapOptionTypes eCustomMapOption)
{
	FAssertBounds(0, m_iNumCustomMapOptions, iOptionID);
	if (checkBounds(iOptionID, 0, m_iNumCustomMapOptions))
    {
		m_aeCustomMapOptions[iOptionID] = eCustomMapOption;

        // doc: setup scenario in Python
		GC.getPythonCaller()->updateCustomMapOption(iOptionID, eCustomMapOption);
	}
}

void CvInitCore::setVictories(int iVictories, bool const* abVictories)
{
	SAFE_DELETE_ARRAY(m_abVictories);
	m_iNumVictories = 0;
	if (iVictories > 0)
	{
		m_iNumVictories = iVictories;
		m_abVictories = new bool[m_iNumVictories];
		for (int i = 0; i < m_iNumVictories; i++)
			m_abVictories[i] = abVictories[i];
	}
}

void CvInitCore::setVictory(VictoryTypes eVictory, bool bVictory)
{
	if (checkBounds(eVictory, 0, m_iNumVictories))
		m_abVictories[eVictory] = bVictory;
	else FAssertBounds(0, m_iNumVictories, eVictory);
}

bool CvInitCore::getVictory(VictoryTypes eVictory) const
{
	FAssertBounds(0, m_iNumVictories, eVictory);
	if (checkBounds(eVictory, 0, m_iNumVictories))
		return m_abVictories[eVictory];
	return false;
}

void CvInitCore::setOption(GameOptionTypes eIndex, bool bOption)
{
	m_abOptions.set(eIndex, bOption);
}

void CvInitCore::setMPOption(MultiplayerOptionTypes eIndex, bool bOption)
{
	m_abMPOptions.set(eIndex, bOption);
}

void CvInitCore::setForceControl(ForceControlTypes eIndex, bool bOption)
{
	m_abForceControls.set(eIndex, bOption);
}

void CvInitCore::setActivePlayer(PlayerTypes eActivePlayer)
{
	m_uiTotalNameLength = 0; // advc.003k (tidier to reset this asap)
	// <advc>
	if (m_eActivePlayer == eActivePlayer)
		return; // </advc>
	/*	<advc.004s>, advc.001: Player switching skips the player history updates.
		In BtS, this merely results in a discontinuity in the graphs, but the new
		PlayerHistory class doesn't tolerate this at all. (Tbd.: Move this to
		CvGame::setActivePlayer? Not sure if all calls go through there ...) */
	if (m_eActivePlayer != NO_PLAYER)
	{
		CvPlayer& kPrevActivePlayer = GET_PLAYER(m_eActivePlayer);
		if (kPrevActivePlayer.isAlive())
		{
			FOR_EACH_ENUM(PlayerHistory)
			{
				kPrevActivePlayer.updateHistory(eLoopPlayerHistory, getGameTurn());
			}
		}
	} // </advc.004s>
	m_eActivePlayer = eActivePlayer;
	updateActiveTeam(); // advc.opt
	if (m_eActivePlayer != NO_PLAYER)
	{	// Automatically claim this slot
		setSlotClaim(m_eActivePlayer, SLOTCLAIM_ASSIGNED);
	}
	else m_eActiveTeam = NO_TEAM; // advc.opt
}

// advc.opt:
void CvInitCore::updateActiveTeam()
{
	m_eActiveTeam = (m_eActivePlayer == NO_PLAYER ? NO_TEAM :
			GET_PLAYER(m_eActivePlayer).getTeam());
}

void CvInitCore::setType(GameType eType)
{
	if (getType() == eType)
		return;

	m_eType = eType;
	// <advc.054>
	// Permanent war/peace always visible in scenarios
	CvGameOptionInfo& kPermWarPeace = GC.getInfo(GAMEOPTION_NO_CHANGING_WAR_PEACE);
	if(getScenario())
		kPermWarPeace.setVisible(true);
	// Otherwise as set in XML
	else kPermWarPeace.setVisible(kPermWarPeace.getVisibleXML());
	// Never visible in MP
	GameOptionTypes aeHideMP[] = {
		GAMEOPTION_LOCK_MODS,
		GAMEOPTION_NEW_RANDOM_SEED,
		GAMEOPTION_RISE_FALL, // advc.701
	};
	for (int i = 0; i < ARRAYSIZE(aeHideMP); i++)
	{
		CvGameOptionInfo& kOption = GC.getInfo(aeHideMP[i]);
		if (getGameMultiplayer())
			kOption.setVisible(false);
		else kOption.setVisible(kOption.getVisibleXML());
	} // </advc.054>
	/*	<advc.tsl> Disable in network games b/c it can't apply just to civs
		set to "random"? (Cf. comment in TrueStarts::updateFitnessValues.)
		No, I think it's still worth having. */
	/*CvGameOptionInfo& kTrueStarts = GC.getInfo(GAMEOPTION_TRUE_STARTS);
	if (eType == GAME_MP_SCENARIO || eType == GAME_MP_NEW || eType == GAME_MP_LOAD)
		kTrueStarts.setVisible(false);
	else kTrueStarts.setVisible(kTrueStarts.getVisibleXML());*/
	// </advc.tsl>
	if (CvPlayer::areStaticsInitialized())
	{
		for (int i = 0; i < MAX_PLAYERS; ++i)
		{
			GET_PLAYER((PlayerTypes)i).updateHuman();
		}
	}
}

void CvInitCore::setType(CvWString const& szType)
{
	if (wcsicmp(szType.GetCString(), L"singleplayer") == 0)
		setType(GAME_SP_NEW);
	else if (wcsicmp(szType.GetCString(), L"spload") == 0)
		setType(GAME_SP_LOAD);
	//FErrorMsg(false, "Invalid game type in ini file!");
	setType(GAME_NONE);
}

void CvInitCore::setMode(GameMode eMode)
{
	if (getMode() != eMode)
	{
		m_eMode = eMode;
		if(CvPlayer::areStaticsInitialized())
		{
			for (int i = 0; i < MAX_PLAYERS; ++i)
			{
				GET_PLAYER((PlayerTypes)i).updateHuman();
			}
		}
	}
}

CvWString const& CvInitCore::getLeaderName(PlayerTypes eID, uint uiForm) const
{
	if (checkBounds(eID, 0, MAX_PLAYERS))
	{
		m_szTemp = gDLL->getObjectText(
				CvString(m_aszLeaderName[eID]).GetCString(), uiForm, true);
	}
	else
	{
		FAssertBounds(0, MAX_PLAYERS, eID);
		m_szTemp.clear();
	}
	return m_szTemp;
}

void CvInitCore::setLeaderName(PlayerTypes eID, CvWString const& szLeaderName)
{
	if (checkBounds(eID, 0, MAX_PLAYERS))
	{
        // doc: prevent early initialization issues
        if (getCiv(eID) == NO_CIVILIZATION)
            return;

		CvWString szName = szLeaderName;
		gDLL->stripSpecialCharacters(szName);
		m_aszLeaderName[eID] = szName;
		countNameLength(szName); // advc.003k
	}
	else FAssertBounds(0, MAX_PLAYERS, eID);
	gDLL->UI().setDirty(Score_DIRTY_BIT, true); // advc.001m
}

CvWString const& CvInitCore::getLeaderNameKey(PlayerTypes eID) const
{
	if (checkBounds(eID, 0, MAX_PLAYERS))
		return m_aszLeaderName[eID];

	FAssertBounds(0, MAX_PLAYERS, eID);
	m_szTemp.clear();
	return m_szTemp;
}

CvWString const& CvInitCore::getCivDescription(PlayerTypes eID, uint uiForm) const
{
	if (checkBounds(eID, 0, MAX_PLAYERS))
	{
		m_szTemp = gDLL->getObjectText(
				CvString(m_aszCivDescription[eID]).GetCString(), uiForm, true);
	}
	else
	{
		FAssertBounds(0, MAX_PLAYERS, eID);
		m_szTemp.clear();
	}
	return m_szTemp;
}

void CvInitCore::setCivDescription(PlayerTypes eID, CvWString const& szCivDescription)
{
	FAssertBounds(0, MAX_PLAYERS, eID);
	CvWString szName = szCivDescription;
	gDLL->stripSpecialCharacters(szName);
	m_aszCivDescription[eID] = szName;
	countNameLength(szName); // advc.003k
}

CvWString const& CvInitCore::getCivDescriptionKey(PlayerTypes eID) const
{
	if (checkBounds(eID, 0, MAX_PLAYERS))
		return m_aszCivDescription[eID];

	FAssertBounds(0, MAX_PLAYERS, eID);
	m_szTemp.clear();
	return m_szTemp;
}

CvWString const& CvInitCore::getCivShortDesc(PlayerTypes eID, uint uiForm) const
{
	if (checkBounds(eID, 0, MAX_PLAYERS))
	{
		// Assume we have stored the key
		m_szTemp = gDLL->getObjectText(
				CvString(m_aszCivShortDesc[eID]).GetCString(), uiForm, true);
	}
	else
	{
		FAssertBounds(0, MAX_PLAYERS, eID);
		m_szTemp.clear();
	}
	return m_szTemp;
}

void CvInitCore::setCivShortDesc(PlayerTypes eID, CvWString const& szCivShortDesc)
{
	FAssertBounds(0, MAX_PLAYERS, eID);
	CvWString szName = szCivShortDesc;
	gDLL->stripSpecialCharacters(szName);
	m_aszCivShortDesc[eID] = szName;
}

CvWString const& CvInitCore::getCivShortDescKey(PlayerTypes eID) const
{
	if (checkBounds(eID, 0, MAX_PLAYERS))
		return m_aszCivShortDesc[eID];

	FAssertBounds(0, MAX_PLAYERS, eID);
	m_szTemp.clear();
	return m_szTemp;
}

CvWString const& CvInitCore::getCivAdjective(PlayerTypes eID, uint uiForm) const
{
	if (checkBounds(eID, 0, MAX_PLAYERS))
	{
		// Assume we have stored the key
		m_szTemp = gDLL->getObjectText(
				CvString(m_aszCivAdjective[eID]).GetCString(), uiForm, true);
	}
	else
	{
		FAssertBounds(0, MAX_PLAYERS, eID);
		m_szTemp.clear();
	}
	return m_szTemp;
}

void CvInitCore::setCivAdjective(PlayerTypes eID, CvWString const& szCivAdjective)
{
	FAssertBounds(0, MAX_PLAYERS, eID);
	CvWString szName = szCivAdjective;
	gDLL->stripSpecialCharacters(szName);
	m_aszCivAdjective[eID] = szName;
}

CvWString const& CvInitCore::getCivAdjectiveKey(PlayerTypes eID) const
{
	if (checkBounds(eID, 0, MAX_PLAYERS))
		return m_aszCivAdjective[eID];

	FAssertBounds(0, MAX_PLAYERS, eID);
	m_szTemp.clear();
	return m_szTemp;
}

CvWString const& CvInitCore::getCivPassword(PlayerTypes eID) const
{
	if (checkBounds(eID, 0, MAX_PLAYERS))
		return m_aszCivPassword[eID];

	FAssertBounds(0, MAX_PLAYERS, eID);
	m_szTemp.clear();
	return m_szTemp;
}

void CvInitCore::setCivPassword(PlayerTypes eID, CvWString const& szCivPassword, bool bEncrypt)
{
	FAssertBounds(0, MAX_PLAYERS, eID);
	if (szCivPassword.empty() || !bEncrypt)
		m_aszCivPassword[eID] = szCivPassword;
	else
	{
		m_aszCivPassword[eID] = CvWString(gDLL->md5String((char*)
				CvString(szCivPassword).GetCString()));
	}
}

CvString const& CvInitCore::getEmail(PlayerTypes eID) const
{
	if (checkBounds(eID, 0, MAX_PLAYERS))
		return m_aszEmail[eID];

	FAssertBounds(0, MAX_PLAYERS, eID);
	m_szTempA.clear();
	return m_szTempA;
}

void CvInitCore::setEmail(PlayerTypes eID, CvString const& szEmail)
{
	FAssertBounds(0, MAX_PLAYERS, eID);
	m_aszEmail[eID] = szEmail;
}

CvString const& CvInitCore::getSmtpHost(PlayerTypes eID) const
{
	if (checkBounds(eID, 0, MAX_PLAYERS))
		return m_aszSmtpHost[eID];

	FAssertBounds(0, MAX_PLAYERS, eID);
	m_szTempA.clear();
	return m_szTempA;
}

void CvInitCore::setSmtpHost(PlayerTypes eID, CvString const& szHost)
{
	FAssertBounds(0, MAX_PLAYERS, eID);
	m_aszSmtpHost[eID] = szHost;
}

// advc.003k:
void CvInitCore::countNameLength(CvWString const& kName)
{
	#ifdef FASSERT_ENABLE
	if (getActivePlayer() == NO_PLAYER && getScenario())
	{
		m_uiTotalNameLength += kName.length();
		FAssertMsg(m_uiTotalNameLength < 1240, "Total length of LeaderName"
				" and CivDesc strings might crash civ selection screen.");
	}
	#endif
}

void CvInitCore::setWhiteFlag(PlayerTypes eID, bool bWhiteFlag)
{
	m_abWhiteFlag.set(eID, bWhiteFlag);
}

CvWString const& CvInitCore::getFlagDecal(PlayerTypes eID) const
{
	if (checkBounds(eID, 0, MAX_PLAYERS))
		return m_aszFlagDecal[eID];

	FAssertBounds(0, MAX_PLAYERS, eID);
	m_szTemp.clear();
	return m_szTemp;
}

void CvInitCore::setFlagDecal(PlayerTypes eID, CvWString const& szFlagDecal)
{
	FAssertBounds(0, MAX_PLAYERS, eID);
	m_aszFlagDecal[eID] = szFlagDecal;
}

void CvInitCore::setCiv(PlayerTypes eID, CivilizationTypes eCiv)
{
	FAssertBounds(0, MAX_PLAYERS, eID);
	/*  advc.003w: Guard added (This way, the CvCivilization data is
		not even recomputed when reloading from within a game.) */
	if (m_aeCiv.get(eID) != eCiv)
	{
		m_aeCiv.set(eID, eCiv);
		GET_PLAYER(eID).setCivilization(eCiv); // advc.003w
	}
}

void CvInitCore::setLeader(PlayerTypes eID, LeaderHeadTypes eLeader)
{
	m_aeLeader.set(eID, eLeader);
}

void CvInitCore::setTeam(PlayerTypes eID, TeamTypes eTeam)
{
	FAssertBounds(0, MAX_PLAYERS, eID);
	if (getTeam(eID) == eTeam)
		return;
	m_aeTeam.set(eID, eTeam);
	if (CvPlayer::areStaticsInitialized())
	{
		GET_PLAYER(eID).updateTeamType();
		updateActiveTeam(); // advc.opt
	}
}

void CvInitCore::setHandicap(PlayerTypes eID, HandicapTypes eHandicap)
{	/*	advc: This can happen when an unknown handicap type string was read
		from CivilizationIV.ini. Maybe that can only happen when AdvCiv itself
		has used and then disused a custom handicap type -- which won't happen.
		However, if another mod can cause this problem too, then it'll be
		important to handle it gracefully ... */
	FAssert(eHandicap != NO_HANDICAP);
	m_aeHandicap.set(eID, eHandicap);
}

void CvInitCore::setColor(PlayerTypes eID, PlayerColorTypes eColor)
{
	m_aeColor.set(eID, eColor);
}

void CvInitCore::setArtStyle(PlayerTypes eID, ArtStyleTypes eArtStyle)
{
	m_aeArtStyle.set(eID, eArtStyle);
}


SlotStatus CvInitCore::getSlotStatus(PlayerTypes eID) const
{
	if (checkBounds(eID, 0, MAX_PLAYERS))
		return m_aeSlotStatus[eID];
	FAssertBounds(0, MAX_PLAYERS, eID);
	return SS_CLOSED;
}

void CvInitCore::setSlotStatus(PlayerTypes eID, SlotStatus eSlotStatus)
{
	FAssertBounds(0, MAX_PLAYERS, eID);
	if (getSlotStatus(eID) != eSlotStatus)
	{
		m_aeSlotStatus[eID] = eSlotStatus;
		if(CvPlayer::areStaticsInitialized())
			GET_PLAYER(eID).updateHuman();
	}
}

SlotClaim CvInitCore::getSlotClaim(PlayerTypes eID) const
{
	if (checkBounds(eID, 0, MAX_PLAYERS))
		return m_aeSlotClaim[eID];
	FAssertBounds(0, MAX_PLAYERS, eID);
	return SLOTCLAIM_UNASSIGNED;
}

void CvInitCore::setSlotClaim(PlayerTypes eID, SlotClaim eSlotClaim)
{
	FAssertBounds(0, MAX_PLAYERS, eID);
	m_aeSlotClaim[eID] = eSlotClaim;
}

void CvInitCore::setReady(PlayerTypes eID, bool bReady)
{
	m_abReady.set(eID, bReady);
}


bool CvInitCore::getPlayableCiv(PlayerTypes eID) const
{
	FAssertBounds(0, MAX_PLAYERS, eID);
	if (getWBMapScript() && !getWBMapNoPlayers())
		return m_abPlayableCiv.get(eID);
	if (getCiv(eID) != NO_CIVILIZATION)
		return GC.getInfo(getCiv(eID)).isPlayable();
	// Don't allow people to play the barb civ
	return (eID < BARBARIAN_PLAYER);
}

void CvInitCore::setPlayableCiv(PlayerTypes eID, bool bPlayableCiv)
{
	m_abPlayableCiv.set(eID, bPlayableCiv);
}

void CvInitCore::setMinorNationCiv(PlayerTypes eID, bool bMinorNationCiv)
{
	/*  advc.003m: Not just a matter of calling CvTeam::updateMinorCiv -
		wars would have to be declared etc. */
	FAssertMsg(bMinorNationCiv == m_abMinorNationCiv.get(eID) || !GET_PLAYER(eID).isAlive(), "Minor civ status has changed after game start; this isn't supported.");
	m_abMinorNationCiv.set(eID, bMinorNationCiv);
}

void CvInitCore::setNetID(PlayerTypes eID, int iNetID)
{
	m_aiNetID.set(eID, static_cast<PlayerTypes>(iNetID));
}

CvString const& CvInitCore::getPythonCheck(PlayerTypes eID) const
{
	if (checkBounds(eID, 0, MAX_PLAYERS))
		return m_aszPythonCheck[eID];
	FAssertBounds(0, MAX_PLAYERS, eID);
	m_szTempCheck.clear();
	return m_szTempCheck;
}

void CvInitCore::setPythonCheck(PlayerTypes eID, CvString const& szPythonCheck)
{
	FAssertBounds(0, MAX_PLAYERS, eID);
	m_aszPythonCheck[eID] = szPythonCheck;
}

CvString const& CvInitCore::getXMLCheck(PlayerTypes eID) const
{
	if (checkBounds(eID, 0, MAX_PLAYERS))
		return m_aszXMLCheck[eID];
	FAssertBounds(0, MAX_PLAYERS, eID);
	m_szTempCheck.clear();
	return m_szTempCheck;
}

void CvInitCore::setXMLCheck(PlayerTypes eID, CvString const& szXMLCheck)
{
	FAssertBounds(0, MAX_PLAYERS, eID);
	m_aszXMLCheck[eID] = szXMLCheck;
}

void CvInitCore::setGamePassword(CvWString const& szGamePassword)
{
	m_szGamePassword = szGamePassword;
}

void CvInitCore::setPitbossTurnTime(int iPitbossTurnTime)
{
	m_iPitbossTurnTime = iPitbossTurnTime;
}

void CvInitCore::setSyncRandSeed(unsigned int uiSyncRandSeed)
{
	m_uiSyncRandSeed = uiSyncRandSeed;
}

void CvInitCore::setMapRandSeed(unsigned int uiMapRandSeed)
{
	m_uiMapRandSeed = uiMapRandSeed;
} // </advc>

void CvInitCore::setAdminPassword(CvWString const& szAdminPassword, bool bEncrypt)
{
	if (szAdminPassword.empty() || !bEncrypt)
		m_szAdminPassword = szAdminPassword;
	else
	{
		m_szAdminPassword = CvWString(
				gDLL->md5String((char*)CvString(szAdminPassword).GetCString()));
	}
}

void CvInitCore::resetAdvancedStartPoints()
{
	int iPoints = 0;

	if (getEra() != NO_ERA)
		iPoints += GC.getInfo(getEra()).getAdvancedStartPoints();

	if (getWorldSize() != NO_WORLDSIZE)
	{
		iPoints *= GC.getInfo(getWorldSize()).getAdvancedStartPointsMod();
		iPoints /= 100;
	}
	// <advc.250c> Reduce start-point costs based on game speed instead.
	/*if (NO_GAMESPEED != getGameSpeed()) {
		iPoints *= GC.getInfo(getGameSpeed()).getGrowthPercent();
		iPoints /= 100;
	}*/
	// (Effect of world size removed through WorldInfo XML)
	// </advc.250c>
	setNumAdvancedStartPoints(iPoints);
}

// <advc.190c>
/*	Report external calls to CvRandom so that the DLL can figure out
	which leaders and civs have been assigned at random by the EXE. */
void CvInitCore::externalRNGCall(int iUpper, CvRandom const* pRandom)
{
	if (getSavedGame())
		return;
	/*	RNG call for loading screen hint makes sure that this gets set
		when a new game is started */
	m_bCivLeaderSetupKnown = true;
	/*	With 34 playable civs and 5 players, all set to random civs and leaders,
		I'm getting 167 calls plus/minus a few. That could be 34+33+32+31+30=160 plus 3 for
		3 civs with just 1 available leader plus 2x2 for 2 civs 2 available leaders
		or 4 civs with 1 available leader plus 1 civ with 3 available leaders).
		I.e. the EXE seems to roll a die for each valid civ and leader. */

	if (iUpper != 10000)
		return;
	for (int i = 0; i < MAX_CIV_PLAYERS; i++)
	{
		if (GET_PLAYER((PlayerTypes)i).isEverAlive())
			return; // We're already past the civ and leader assignment at game start
	}
	std::vector<PlayerTypes> aeSlotPlayer;
	for (int i = 0; i < MAX_CIV_PLAYERS; i++)
	{
		PlayerTypes ePlayer = (PlayerTypes)i;
		if ((getSlotStatus(ePlayer) == SS_TAKEN ||
			getSlotStatus(ePlayer) == SS_COMPUTER) &&
			!getMinorNationCiv(ePlayer))
		{
			aeSlotPlayer.push_back(ePlayer);
		}
	}
	/*	When a player i is set to "Random", m_aeCiv[i], m_aeLeader[i]
		remain at -1 (NO_...) until the dice have been rolled.
		So, there's no need to count the RNG calls; we just need to
		find the first player who doesn't already have a civ, and,
		if all have a civ, then the first player without a leader. */
	for (size_t i = 0; i < aeSlotPlayer.size(); i++)
	{
		if (getCiv(aeSlotPlayer[i]) == NO_CIVILIZATION)
		{
			m_abCivChosenRandomly.set(aeSlotPlayer[i], true);
			return;
		}
	}
	bool const bLeadAnyCiv = getOption(GAMEOPTION_LEAD_ANY_CIV);
	for (size_t i = 0; i < aeSlotPlayer.size(); i++)
	{
		if (getLeader(aeSlotPlayer[i]) == NO_LEADER)
		{
			// Not truly random if there is only one leader available
			int iLeaders = 0;
			FOR_EACH_ENUM(LeaderHead)
			{
				if (bLeadAnyCiv ||
					GC.getInfo(getCiv(aeSlotPlayer[i])).isLeaders(eLoopLeaderHead))
				{
					iLeaders++;
					if (iLeaders > 1)
					{
						m_abLeaderChosenRandomly.set(aeSlotPlayer[i], true);
						break;
					}
				}
			}
			FAssertMsg(iLeaders > 0, "Civ type w/o any valid leader type");
			return;
		}
	}
}


bool CvInitCore::wasCivRandomlyChosen(PlayerTypes eID) const
{
	return m_abCivChosenRandomly.get(eID);
}


bool CvInitCore::wasLeaderRandomlyChosen(PlayerTypes eID) const
{
	if (wasCivRandomlyChosen(eID) && !getOption(GAMEOPTION_LEAD_ANY_CIV))
		return true;
	return m_abLeaderChosenRandomly.get(eID);
}

void CvInitCore::setCivLeaderRandomlyChosen(PlayerTypes eID, bool bRandomCiv, bool bRandomLeader)
{
	m_bCivLeaderSetupKnown = true;
	m_abCivChosenRandomly.set(eID, bRandomCiv);
	m_abLeaderChosenRandomly.set(eID, bRandomLeader);
} // </advc.190c>

// <advc.191>
void CvInitCore::setLeaderExternal(PlayerTypes eID, LeaderHeadTypes eLeader)
{
	LeaderHeadTypes eOldLeader = getLeader(eID);
	if (eOldLeader == eLeader)
		return;
	setLeader(eID, eLeader); // This is all that BtS did here
	if (eOldLeader == NO_LEADER &&
		// BtS behavior is sufficient when only one of them is randomized
		wasLeaderRandomlyChosen(eID) &&
		wasCivRandomlyChosen(eID) &&
		!getSavedGame() && getActivePlayer() != NO_PLAYER)
	{
		for (int i = MAX_CIV_PLAYERS - 1; i > eID; i--)
		{
			PlayerTypes eLoopPlayer = (PlayerTypes)i;
			if (getLeader(eLoopPlayer) == NO_LEADER &&
				!getMinorNationCiv(eLoopPlayer) &&
				(getSlotStatus(eLoopPlayer) == SS_TAKEN ||
				getSlotStatus(eLoopPlayer) == SS_COMPUTER))
			{
				return;
			}
		}
		// All random leaders have been assigned
		reRandomizeCivsAndLeaders();
	}
}


void CvInitCore::reRandomizeCivsAndLeaders()
{
	/*	NB: Only executed by the host. The EXE syncs most of the data, but not the
		was-randomly-chosen info. That gets handled by CvGame::setInitialItems.
		Not letting CvInitCore send net messages makes clear that they're not
		delivered until CvGame takes over the setup procedure. */
	if (getOption(GAMEOPTION_LEAD_ANY_CIV))
		return;
	int const iPER_EXTRA_LEADER_CIV_SELECTION_WEIGHT = GC.getDefineINT(
			"PER_EXTRA_LEADER_CIV_SELECTION_WEIGHT");
	if (iPER_EXTRA_LEADER_CIV_SELECTION_WEIGHT == 0) // BtS behavior
		return;
	FOR_EACH_ENUM2(Civilization, eCiv)
	{
		if (GC.getInfo(eCiv).isAIPlayable() != GC.getInfo(eCiv).isPlayable())
		{
			/*FErrorMsg("Not sure how to handle (non)-AI playable leaders; "
					"falling back on BtS algorithm.");*/ // Well, not exactly an error ...
			return;
		}
	}
	EagerEnumMap<PlayerTypes,bool> abRandomize;
	for (int i = 0; i < MAX_CIV_PLAYERS; i++)
	{
		PlayerTypes const ePlayer = (PlayerTypes)i;
		// If only the leader was randomized, then the BtS behavior is fine.
		if (wasCivRandomlyChosen(ePlayer) &&
			wasLeaderRandomlyChosen(ePlayer))
		{
			abRandomize.set(ePlayer, true);
		}
	}
	if (!abRandomize.isAnyNonDefault())
		return;
	std::vector<PlayerTypes> aeSlotPlayers;
	for (int i = 0; i < MAX_CIV_PLAYERS; i++)
	{
		PlayerTypes const ePlayer = (PlayerTypes)i;
		if (!getMinorNationCiv(ePlayer) &&
			(getSlotStatus(ePlayer) == SS_TAKEN ||
			getSlotStatus(ePlayer) == SS_COMPUTER))
		{
			aeSlotPlayers.push_back(ePlayer);
			FAssert(getLeader(ePlayer) != NO_LEADER);
			FAssert(getCiv(ePlayer) != NO_CIVILIZATION);
		}
	}
	EagerEnumMap<CivilizationTypes,int> aiTakersPerCiv;
	EagerEnumMap<LeaderHeadTypes,bool> abLeaderTaken;
	int iRandomLeadersNeeded = 0;
	for (size_t i = 0; i < aeSlotPlayers.size(); i++)
	{
		PlayerTypes const ePlayer = aeSlotPlayers[i];
		if (!abRandomize.get(ePlayer))
		{
			abLeaderTaken.set(getLeader(ePlayer), true);
			aiTakersPerCiv.add(getCiv(ePlayer), 1);
		}
		else iRandomLeadersNeeded++;
	}
	std::map<CivilizationTypes,std::vector<LeaderHeadTypes> > leadersPerCiv;
	int iLeadersAvailable = 0;
	FOR_EACH_ENUM2(LeaderHead, eLeader)
	{
		bool bPlayable = false;
		FOR_EACH_ENUM2(Civilization, eCiv)
		{
			if (GC.getInfo(eCiv).isLeaders(eLeader) &&
				GC.getInfo(eCiv).isPlayable())
			{
				leadersPerCiv[eCiv].push_back(eLeader);
				bPlayable = true;
			}
		}
		if (bPlayable && !abLeaderTaken.get(eLeader))
			iLeadersAvailable++;
	}
	if (iRandomLeadersNeeded > iLeadersAvailable)
	{
		FAssertMsg(iRandomLeadersNeeded <= iLeadersAvailable,
				"Can't assign unique leaders; falling back on BtS algorithm.");
		return;
	}

	CvRandom rand;
	/*	Need to use a synchronized RNG. Don't want to include CvGame here;
		using a synchronized seed should do. */
	rand.init(getSyncRandSeed());
	for (size_t i = 0; i < aeSlotPlayers.size(); i++)
	{
		PlayerTypes const ePlayer = aeSlotPlayers[i];
		if (!abRandomize.get(ePlayer))
			continue;
		CivilizationTypes eNewCiv = NO_CIVILIZATION;
		for (int iMaxTaken = 0; iMaxTaken < ((int)aeSlotPlayers.size()) &&
			eNewCiv == NO_CIVILIZATION; iMaxTaken++)
		{
			EagerEnumMap<CivilizationTypes,int> aiWeights;
			int iTotalWeight = 0;
			FOR_EACH_ENUM2(Civilization, eCiv)
			{
				if (aiTakersPerCiv.get(eCiv) > iMaxTaken)
					continue;
				CvCivilizationInfo const& kCiv = GC.getInfo(eCiv);
				if (!kCiv.isPlayable())
					continue;
				int iWeight = 0;
				for (size_t j = 0; j < leadersPerCiv[eCiv].size(); j++)
				{
					if (!abLeaderTaken.get(leadersPerCiv[eCiv][j]))
						iWeight += iPER_EXTRA_LEADER_CIV_SELECTION_WEIGHT;
				}
				if (iWeight == 0) // All leaders already taken
					continue;
				iWeight += 100;
				iWeight = std::max(iWeight, 0);
				aiWeights.set(eCiv, iWeight);
				iTotalWeight += iWeight;
			}
			if (iTotalWeight <= 0)
				continue;
			int const iRoll = rand.get(iTotalWeight);
			int iPartialSum = 0;
			FOR_EACH_ENUM2(Civilization, eCiv)
			{
				iPartialSum += aiWeights.get(eCiv);
				if (iRoll < iPartialSum)
				{
					eNewCiv = eCiv;
					aiTakersPerCiv.add(eNewCiv, 1);
					break;
				}
			}
		}
		if (eNewCiv == NO_CIVILIZATION)
		{
			FAssert(eNewCiv != NO_CIVILIZATION);
			return;
		}
		std::vector<LeaderHeadTypes> aeAvailableLeaders;
		for (size_t j = 0; j < leadersPerCiv[eNewCiv].size(); j++)
		{
			if (!abLeaderTaken.get(leadersPerCiv[eNewCiv][j]))
				aeAvailableLeaders.push_back(leadersPerCiv[eNewCiv][j]);
		}
		if (aeAvailableLeaders.empty())
		{
			FAssert(!aeAvailableLeaders.empty()); // Shouldn't have chosen eNewCiv then
			return;
		}
		LeaderHeadTypes eNewLeader = aeAvailableLeaders[
				rand.get(aeAvailableLeaders.size())];
		setCiv(ePlayer, eNewCiv);
		setLeader(ePlayer, eNewLeader);
	}
} // </advc.191>

// advc.250c:
int CvInitCore::getAdvancedStartMinPoints() const
{
	FOR_EACH_ENUM(UnitClass)
	{
		CvUnitInfo const& u = GC.getInfo(GC.getInfo(eLoopUnitClass).getDefaultUnit());
		if (u.isFound())
			return u.getAdvancedStartCost();
	}
	FAssert(false);
	return -1;
}


/*	<advc> Definitions of exported setters moved from the header.
	Easier to track external calls in the debugger this way. */
// TODO: refactor
void CvInitCore::setGameName(CvWString const& szGameName)
{
	/*	<advc.135c> Changing the game name can be a step to enable debug tools.
		Make sure that the other players are aware. */
	if (getMultiplayer() && !m_szGameName.empty() && m_szGameName != szGameName &&
		getActivePlayer() != NO_PLAYER)
	{
		GET_PLAYER(getActivePlayer()).announceGameNameChange(m_szGameName, szGameName);
	} // </advc.135c>

	// doc: encode mod version in game name for better save game inspection
	static CvWString szAppliedGameName = szGameName;
	static CvWString szModVersion = GC.getDefineSTRING("DAWN_OF_CIV_MOD_VERSION");
	static CvWString szLeft = " (v";
	static CvWString szRight = ")";

	if (szModVersion != NULL && !szModVersion.empty())
	{
		int iSuffixIndex = szAppliedGameName.find(szLeft);
		if (iSuffixIndex != std::string::npos)
		{
			szAppliedGameName = szAppliedGameName.substr(0, iSuffixIndex);
		}

		m_szGameName = szAppliedGameName + szLeft + szModVersion + szRight;
		return;
	}

	m_szGameName = szGameName;
}


void CvInitCore::read(FDataStreamBase* pStream)
{
	/*	<advc.enum> The EXE doesn't reset this class before calling read.
		Need to free all dynamic memory and clear everything that doesn't get
		fully replaced with data from pStream. */
	resetGame(true);
	resetPlayers(true); // </advc.enum>

	uint uiFlag=0;
	pStream->Read(&uiFlag);

	// GAME DATA
	pStream->Read((int*)&m_eType);
	pStream->ReadString(m_szGameName);
	pStream->ReadString(m_szGamePassword);
	pStream->ReadString(m_szAdminPassword);
	pStream->ReadString(m_szMapScriptName);
	pStream->Read(&m_bPangaea);
	pStream->Read(&m_bWBMapNoPlayers);

	pStream->Read((int*)&m_eWorldSize);
	pStream->Read((int*)&m_eClimate);
	pStream->Read((int*)&m_eSeaLevel);
	pStream->Read((int*)&m_eEra);
	pStream->Read((int*)&m_eGameSpeed);
	pStream->Read((int*)&m_eTurnTimer);
	pStream->Read((int*)&m_eCalendar);

	//SAFE_DELETE_ARRAY(m_aeCustomMapOptions); // advc.enum: Now handled by resetGame
	pStream->Read(&m_iNumCustomMapOptions);
	pStream->Read(&m_iNumHiddenCustomMapOptions);
	if (m_iNumCustomMapOptions > 0)
	{
		m_aeCustomMapOptions = new CustomMapOptionTypes[m_iNumCustomMapOptions];
		pStream->Read(m_iNumCustomMapOptions, (int*)m_aeCustomMapOptions);
	}
	//SAFE_DELETE_ARRAY(m_abVictories); // advc.enum: Now handled by resetGame
	pStream->Read(&m_iNumVictories);
	if (m_iNumVictories > 0)
	{
		m_abVictories = new bool[m_iNumVictories];
		pStream->Read(m_iNumVictories, m_abVictories);
	}
	// <advc.enum>
	m_abOptions.read(pStream);
	m_abMPOptions.read(pStream);

    pStream->Read(&m_bStatReporting);

	pStream->Read(&m_iGameTurn);
	pStream->Read(&m_iMaxTurns);
	pStream->Read(&m_iPitbossTurnTime);
	pStream->Read(&m_iTargetScore);

	pStream->Read(&m_iMaxCityElimination);
	pStream->Read(&m_iNumAdvancedStartPoints);

	// PLAYER DATA
	pStream->ReadString(MAX_PLAYERS, m_aszLeaderName);
	pStream->ReadString(MAX_PLAYERS, m_aszCivDescription);
	pStream->ReadString(MAX_PLAYERS, m_aszCivShortDesc);
	pStream->ReadString(MAX_PLAYERS, m_aszCivAdjective);
	pStream->ReadString(MAX_PLAYERS, m_aszCivPassword);
	pStream->ReadString(MAX_PLAYERS, m_aszEmail);
	pStream->ReadString(MAX_PLAYERS, m_aszSmtpHost);

	m_abWhiteFlag.read(pStream);
	pStream->ReadString(MAX_PLAYERS, m_aszFlagDecal);

	m_aeCiv.read(pStream);
	m_aeLeader.read(pStream);
	m_aeTeam.read(pStream);
	m_aeHandicap.read(pStream);
	m_aeColor.read(pStream);
	m_aeArtStyle.read(pStream);
	// <advc.190c>
	m_abCivChosenRandomly.read(pStream);
	m_abLeaderChosenRandomly.read(pStream);

	pStream->Read(MAX_PLAYERS, (int*)m_aeSlotStatus);
	pStream->Read(MAX_PLAYERS, (int*)m_aeSlotClaim);

	for (int i = 0; i < MAX_PLAYERS; i++)
	{
		if (m_aeSlotClaim[i] == SLOTCLAIM_ASSIGNED)
			m_aeSlotClaim[i] = SLOTCLAIM_RESERVED;
	}

	m_abPlayableCiv.read(pStream);
	m_abMinorNationCiv.read(pStream);

	if (CvPlayer::areStaticsInitialized())
	{
		for (int i = 0; i < MAX_PLAYERS; i++)
		{
			CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)i); // advc
			/*  <advc.706> Had a reproducible crash when loading a non-R&F game
				from within an R&F game right after inspecting a city.
				Resetting the human players before reading any other player data
				seems to have fixed it. */
			if(kLoopPlayer.isHuman())
			{
				kLoopPlayer.reset((PlayerTypes)i);
				kLoopPlayer.setIsHuman(true);
			} // </advc.706>
			kLoopPlayer.updateHuman();
			kLoopPlayer.updateTeamType();
		}
	}
}


void CvInitCore::write(FDataStreamBase* pStream)
{
	REPRO_TEST_BEGIN_WRITE("InitCore");
	uint uiFlag = 0;

	pStream->Write(uiFlag);

	// GAME DATA ...

	//pStream->Write(m_eType);
	/*	<advc.001p> Make sure that resetPlayer will be able to tell
		that a game is being loaded when reloading this savegame.
		After loading, the EXE calls setType(..._LOAD). When ..._LOAD is
		already the game type, some code in setType won't be executed -
		but I don't think that code needs to run at that point. */
	GameType eWriteGameType = m_eType;
	switch (eWriteGameType)
	{
	case GAME_SP_NEW:
	case GAME_SP_SCENARIO:
		eWriteGameType = GAME_SP_LOAD;
		break;
	case GAME_MP_NEW:
	case GAME_MP_SCENARIO:
		eWriteGameType = GAME_MP_LOAD;
		break;
	case GAME_HOTSEAT_NEW:
	case GAME_HOTSEAT_SCENARIO:
		eWriteGameType = GAME_HOTSEAT_LOAD;
		break;
	case GAME_PBEM_NEW:
	case GAME_PBEM_SCENARIO:
		eWriteGameType = GAME_PBEM_LOAD;
	}
	pStream->Write(eWriteGameType); // </advc.001p>
	pStream->WriteString(m_szGameName);
	pStream->WriteString(m_szGamePassword);
	pStream->WriteString(m_szAdminPassword);
	pStream->WriteString(m_szMapScriptName);
	pStream->Write(m_bPangaea); // advc
	pStream->Write(m_bWBMapNoPlayers);

	pStream->Write(m_eWorldSize);
	pStream->Write(m_eClimate);
	pStream->Write(m_eSeaLevel);
	pStream->Write(m_eEra);
	pStream->Write(m_eGameSpeed);
	pStream->Write(m_eTurnTimer);
	pStream->Write(m_eCalendar);

	pStream->Write(m_iNumCustomMapOptions);
	pStream->Write(m_iNumHiddenCustomMapOptions);
	pStream->Write(m_iNumCustomMapOptions, (int*)m_aeCustomMapOptions);

	pStream->Write(m_iNumVictories);
	pStream->Write(m_iNumVictories, m_abVictories);

	m_abOptions.write(pStream);
	// <advc.test>
	#ifdef FASSERT_ENABLE
	if (!getGameMultiplayer())
	{
		FOR_EACH_ENUM(MPOption)
			FAssert(!m_abMPOptions.get(eLoopMPOption));
	}
	#endif // </advc.test>
	m_abMPOptions.write(pStream);

	pStream->Write(m_bStatReporting);

	pStream->Write(m_iGameTurn);
	pStream->Write(m_iMaxTurns);
	pStream->Write(m_iPitbossTurnTime);
	pStream->Write(m_iTargetScore);

	pStream->Write(m_iMaxCityElimination);
	pStream->Write(m_iNumAdvancedStartPoints);

	// PLAYER DATA ...

	pStream->WriteString(MAX_PLAYERS, m_aszLeaderName);
	pStream->WriteString(MAX_PLAYERS, m_aszCivDescription);
	pStream->WriteString(MAX_PLAYERS, m_aszCivShortDesc);
	pStream->WriteString(MAX_PLAYERS, m_aszCivAdjective);
	pStream->WriteString(MAX_PLAYERS, m_aszCivPassword);
	pStream->WriteString(MAX_PLAYERS, m_aszEmail);
	pStream->WriteString(MAX_PLAYERS, m_aszSmtpHost);

	m_abWhiteFlag.write(pStream);
	pStream->WriteString(MAX_PLAYERS, m_aszFlagDecal);

	m_aeCiv.write(pStream);
	m_aeLeader.write(pStream);
	m_aeTeam.write(pStream);
	m_aeHandicap.write(pStream);
	m_aeColor.write(pStream);
	m_aeArtStyle.write(pStream);
	// <advc.190c>
	m_abCivChosenRandomly.write(pStream);
	m_abLeaderChosenRandomly.write(pStream);
	pStream->Write(m_bCivLeaderSetupKnown); // </advc.190c>
	REPRO_TEST_END_WRITE(); // (skip slot data)
	pStream->Write(MAX_PLAYERS, (int*)m_aeSlotStatus);
	pStream->Write(MAX_PLAYERS, (int*)m_aeSlotClaim);

	m_abPlayableCiv.write(pStream);
	m_abMinorNationCiv.write(pStream);
}
