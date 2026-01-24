#include "CvGameCoreDLL.h"
#include "CvReplayInfo.h"
#include "CvPlayer.h"
#include "CvGameAI.h" // advc.104
#include "CvInfo_GameOption.h"
#include "CvMap.h"
#include "CvReplayMessage.h"
#include "CvGameTextMgr.h"
#include "StartPointsAsHandicap.h" // advc.250b
#include "CvBugOptions.h" // advc.106i

int CvReplayInfo::REPLAY_VERSION = 6; // advc.707, advc.106i: 4 in BtS

CvReplayInfo::CvReplayInfo() :
	m_eActivePlayer(NO_PLAYER), // (advc: was 0)
	m_eDifficulty(NO_HANDICAP),
	m_eWorldSize(NO_WORLDSIZE),
	m_eClimate(NO_CLIMATE),
	m_eSeaLevel(NO_SEALEVEL),
	m_eEra(NO_ERA),
	m_eGameSpeed(NO_GAMESPEED),
	m_iInitialTurn(0),
	m_iFinalTurn(0),
	m_eVictoryType(NO_VICTORY),
	m_iMapHeight(0),
	m_iMapWidth(0),
	m_pcMinimapPixels(NULL),
	m_eCalendar(NO_CALENDAR), // advc: Safer to initialize it here
	m_bMultiplayer(false),
	m_iStartYear(0)
{
	m_iMinimapSize = -1; // advc.106m: To be read from replay file
	// <advc.003k>
	m = new Data();
	m->iNormalizedScore = 0, // </advc.003k>
	m->iFinalScore = -1; // advc.707
	// <advc.106i>
	m->iVersionRead = -1;
	m->bDisplayOtherMods = false; // </advc.106i>
}
/*	advc.003k: Needs to have a copy-constructor b/c of its Python counterpart,
	but I don't think it'll actually get called. Copying m_pcMinimapPixels
	would seem undesirable. */
CvReplayInfo::CvReplayInfo(CvReplayInfo const&)
{
	FErrorMsg("No copy-constructor implemented for CvReplayInfo");
}

CvReplayInfo::~CvReplayInfo()
{
	for (uint i = 0; i < m_listReplayMessages.size(); i++)
	{
		SAFE_DELETE(m_listReplayMessages[i]);
	}
	SAFE_DELETE_ARRAY(m_pcMinimapPixels); // advc.001 (was SAFE_DELETE)
	SAFE_DELETE(m); // advc.003k
}

void CvReplayInfo::createInfo(PlayerTypes ePlayer)
{
	if (!isStoringReplaysAsBtS()) // advc.106i (and moved up)
		m_szModName = GC.getModName().getFullPath();
	CvGame const& kGame = GC.getGame();
	CvMap const& kMap = GC.getMap();
	/*  <advc>: createInfo gets called when Python scripts are (re-)loaded.
		Somehow, skipping the code above gets the Python loading code stuck
		in an infinite loop. Therefore I only skip the somewhat costly
		copying of the terrain texture after loading scripts for the first time.
		(Don't know how to identify a Python reload here. Mustn't break Shift+F1.) */
	static bool bFirstCall = true;
	if (bFirstCall && kGame.isFinalInitialized() && kGame.getGameState() != GAMESTATE_OVER)
	{
		bFirstCall = false;
		return;
	} // </advc>

	if (ePlayer == NO_PLAYER)
		ePlayer = kGame.getActivePlayer();

	if (ePlayer != NO_PLAYER)
	{
		CvPlayer const& kPlayer = GET_PLAYER(ePlayer);
		// advc.708: Game handicap is the one to display in R&F games
		m_eDifficulty = (kGame.isOption(GAMEOPTION_RISE_FALL) ? kGame.getHandicapType() :
				kPlayer.getHandicapType());
		m_szLeaderName = kPlayer.getName();
		m_szCivDescription = kPlayer.getCivilizationDescription();
		m_szShortCivDescription = kPlayer.getCivilizationShortDescription();
		m_szCivAdjective = kPlayer.getCivilizationAdjective();
		m_szMapScriptName = GC.getInitCore().getMapScriptName();
		m_eWorldSize = kMap.getWorldSize();
		m_eClimate = kMap.getClimate();
		m_eSeaLevel = kMap.getSeaLevel();
		m_eEra = kGame.getStartEra();
		m_eGameSpeed = kGame.getGameSpeedType();

		m_listGameOptions.clear();
		FOR_EACH_ENUM(GameOption)
		{
			if (kGame.isOption(eLoopGameOption))
				m_listGameOptions.push_back(eLoopGameOption);
		}

		m_listVictoryTypes.clear();
		FOR_EACH_ENUM(Victory)
		{
			if (kGame.isVictoryValid(eLoopVictory))
				m_listVictoryTypes.push_back(eLoopVictory);
		}
		if (kGame.getWinner() == kPlayer.getTeam())
			m_eVictoryType = kGame.getVictory();
		else m_eVictoryType = NO_VICTORY;

		m->iNormalizedScore = kPlayer.calculateScore(
				true, kPlayer.getTeam() == kGame.getWinner());
		// <advc.707> Treat R&F games as "Score" victory (previously unused)
		if(kGame.isOption(GAMEOPTION_RISE_FALL))
		{
			FOR_EACH_ENUM(Victory)
			{
				if(GC.getInfo(eLoopVictory).isTargetScore())
				{
					m_eVictoryType = eLoopVictory;
					break;
				}
			}
		} // </advc.707>
	}

	m_bMultiplayer = kGame.isGameMultiPlayer();


	m_iInitialTurn = kGame.getStartTurn();
	m_iStartYear = kGame.getStartYear();
	m_iFinalTurn = kGame.getGameTurn();
	GAMETEXT.setYearStr(m_szFinalDate, m_iFinalTurn, false, kGame.getCalendar(),
			kGame.getStartYear(), kGame.getGameSpeedType());

	m_eCalendar = kGame.getCalendar();

	m_listPlayerScoreHistory.clear();
	EagerEnumMap<PlayerTypes,PlayerTypes> aePlayerIndices; // advc.enum
	/*	advc (note): This loop remaps player IDs so that players never alive are skipped.
		Not sure if this is really needed. */
	PlayerTypes eNewIndex = (PlayerTypes)0;
	for (int i = 0; i < MAX_PLAYERS; i++)
	{
		CvPlayer const& kLoopPlayer = GET_PLAYER((PlayerTypes)i);
		if (!kLoopPlayer.isEverAlive())
			continue; // advc
		aePlayerIndices.set(kLoopPlayer.getID(), eNewIndex);
		if (kLoopPlayer.getID() == kGame.getActivePlayer())
			m_eActivePlayer = eNewIndex;
		++eNewIndex;
		PlayerInfo playerInfo;
		playerInfo.m_eLeader = kLoopPlayer.getLeaderType();
		playerInfo.m_eColor = GC.getInfo(kLoopPlayer.getPlayerColor()).getColorTypePrimary();
		// K-Mod. (bypass the conceal colour check.) // advc.007: Not needed anymore
		//GC.getInitCore().getColor((PlayerTypes)iPlayer)).getColorTypePrimary();
		for (int iTurn = m_iInitialTurn; iTurn <= m_iFinalTurn; iTurn++)
		{
			TurnData score;
			// advc.004s: max(0,) b/c unavailable data is represented as -1
			score.m_iScore = std::max(0, kLoopPlayer.getHistorySafe(
					PLAYER_HISTORY_SCORE, iTurn));
			score.m_iAgriculture = std::max(0, kLoopPlayer.getHistorySafe(
					PLAYER_HISTORY_AGRICULTURE, iTurn));
			score.m_iIndustry = std::max(0, kLoopPlayer.getHistorySafe(
					PLAYER_HISTORY_INDUSTRY, iTurn));
			score.m_iEconomy = std::max(0, kLoopPlayer.getHistorySafe(
					PLAYER_HISTORY_ECONOMY, iTurn));

			playerInfo.m_listScore.push_back(score);
		}
		m_listPlayerScoreHistory.push_back(playerInfo);
	}

	//m_listReplayMessages.clear();
	FAssert(m_listReplayMessages.empty()); // advc: The above would leak memory
	// <advc.106h>
	if(kGame.getGameState() == GAMESTATE_OVER &&
		GC.getDefineINT("SETTINGS_IN_REPLAYS") > 0)
	{
		addSettingsMsg();
	} // </advc.106h>
	for (uint i = 0; i < kGame.getNumReplayMessages(); i++)
	{	// <advc.enum>
		PlayerTypes eMsgPlayer = kGame.getReplayMessagePlayer(i);
		PlayerTypes ePlayerIndex = (eMsgPlayer == NO_PLAYER ? NO_PLAYER :
				aePlayerIndices.get(kGame.getReplayMessagePlayer(i))); // </advc.enum>
		if (ePlayerIndex != NO_PLAYER)
		{
			CvReplayMessage* pMsg = new CvReplayMessage(kGame.getReplayMessageTurn(i),
					kGame.getReplayMessageType(i), ePlayerIndex);
			if (pMsg != NULL)
			{
				pMsg->setColor(kGame.getReplayMessageColor(i));
				pMsg->setText(kGame.getReplayMessageText(i));
				pMsg->setPlot(kGame.getReplayMessagePlotX(i),
						kGame.getReplayMessagePlotY(i));
				m_listReplayMessages.push_back(pMsg);
			}
		}
		else
		{
			CvReplayMessage* pMsg = new CvReplayMessage(kGame.getReplayMessageTurn(i),
					kGame.getReplayMessageType(i), NO_PLAYER);
			if (pMsg != NULL)
			{
				pMsg->setColor(kGame.getReplayMessageColor(i));
				pMsg->setText(kGame.getReplayMessageText(i));
				pMsg->setPlot(kGame.getReplayMessagePlotX(i),
						kGame.getReplayMessagePlotY(i));
				m_listReplayMessages.push_back(pMsg);
			}
		}
	}
	// <advc.707>
	if(m->iFinalScore < 0)
		m->iFinalScore = getFinalPlayerScore(); // </advc.707>

	m_iMapWidth = kMap.getGridWidth();
	m_iMapHeight = kMap.getGridHeight();
	// <advc.106m>
	if (m_iMinimapSize == -1)
		setMinimapSizeFromXML();
	// </advc.106m>  <advc.106n>
	byte const* pTexture = kMap.getReplayTexture();
	if (pTexture == NULL)
		pTexture = gDLL->UI().getMinimapBaseTexture();
	// </advc.106n>
	SAFE_DELETE_ARRAY(m_pcMinimapPixels); // advc.001 (was SAFE_DELETE)
	m_pcMinimapPixels = new byte[/* advc.106m: */ minimapPixels()];
	if (pTexture != NULL)
		memcpy((void*)m_pcMinimapPixels, pTexture, /* advc.106m: */ minimapPixels());
}

// <advc.106h>
void CvReplayInfo::addSettingsMsg()
{
	PlayerTypes ePlayer = GC.getGame().getInitialActivePlayer();
	if(ePlayer == NO_PLAYER)
		return;
	CvReplayMessage* pSettingsMsg = new CvReplayMessage(0,
			REPLAY_MESSAGE_MAJOR_EVENT, ePlayer);
	CvWString szSettings(gDLL->getText("TXT_KEY_MISC_RELOAD", 1) + L". " +
			gDLL->getText("TXT_KEY_MAIN_MENU_SETTINGS") + L":\n");
	appendSettingsMsg(szSettings, ePlayer);
	pSettingsMsg->setText(szSettings);
	pSettingsMsg->setColor(GC.getColorType("WHITE"));
	FAssert(m_listReplayMessages.empty());
	m_listReplayMessages.push_back(pSettingsMsg);
}


void CvReplayInfo::appendSettingsMsg(CvWString& szSettings, PlayerTypes ePlayer) const
{
	CvGame const& kGame = GC.getGame();
	bool bScenario = false;
	// Strip away file ending of WB scenario
	CvWString const szWBEnding = L".CivBeyondSwordWBSave";
	CvWString szMapName = getMapScriptName();
	if(szMapName.length() > szWBEnding.length() && szMapName.substr(szMapName.length() -
		szWBEnding.length(), szWBEnding.length()).compare(szWBEnding) == 0)
	{
		szMapName = szMapName.substr(0, szMapName.length() - szWBEnding.length());
		bScenario = true;
	}
	CvPlayer const& kPlayer = GET_PLAYER(ePlayer);
	szSettings += 
			gDLL->getText("TXT_KEY_NAME_LEADER_CIV",
			GC.getInfo(kPlayer.getLeaderType()).getTextKeyWide(),
			kPlayer.getCivilizationShortDescriptionKey(), kPlayer.getReplayName()) + L"\n" +
			gDLL->getText("TXT_KEY_SETTINGS_DIFFICULTY",
			GC.getInfo(getDifficulty()).getTextKeyWide()) + L"\n" +
			(bScenario ? szMapName : gDLL->getText("TXT_KEY_SIZE_MAP_WITH",
			GC.getInfo(getWorldSize()).getTextKeyWide(),
			getMapScriptName().GetCString()) + L" " +
			gDLL->getText("TXT_KEY_SETTINGS_SEA_LEVEL",
			GC.getInfo(getSeaLevel()).getTextKeyWide())) +
			(getClimate() == 0 ? L"" : (L", " +
			gDLL->getText("TXT_KEY_SETTINGS_CLIMATE",
			GC.getInfo(getClimate()).getTextKeyWide())));
	// <advc.190b>
	CvMap const& kMap = GC.getMap();
	for(int i = 0; i < kMap.getNumCustomMapOptions(); i++)
	{
		CvWString szDesc(kMap.getNonDefaultCustomMapOptionDesc(i));
		if (szDesc.empty()) // Meaning that the option is set to its default value
			continue;
		szSettings.append(L", ");
		szSettings.append(szDesc);
	} // </advc.190b>
	szSettings.append(NEWLINE);
	szSettings.append(gDLL->getText("TXT_KEY_SETTINGS_GAME_SPEED",
			GC.getInfo(getGameSpeed()).getTextKeyWide()));
	if (getEra() != 0)
	{
		szSettings.append(L", ");
		szSettings.append(gDLL->getText("TXT_KEY_SETTINGS_STARTING_ERA",
			GC.getInfo(getEra()).getTextKeyWide()));
	}
	szSettings.append(NEWLINE);
	// <advc.250b>
	if(kGame.isOption(GAMEOPTION_ADVANCED_START) && !kGame.isOption(GAMEOPTION_SPAH))
	{
		szSettings += gDLL->getText("TXT_KEY_ADVANCED_START_POINTS") + L" "
				+ CvWString::format(L"%d", kGame.getNumAdvancedStartPoints()) + L"\n";
	} // </advc.250b>
	int iDisabled = 0;
	for(int i = 0; i < GC.getNumVictoryInfos(); i++)
	{
		VictoryTypes eVictory = (VictoryTypes)i;
		if(kGame.isVictoryValid(eVictory))
			continue;
		iDisabled++;
		szSettings += GC.getInfo(eVictory).getDescription();
		szSettings += L", ";
	}
	if(iDisabled > 0)
	{
		szSettings = szSettings.substr(0, szSettings.length() - 2) + L" "; // Drop the final comma
		szSettings += gDLL->getText("TXT_KEY_VICTORY_DISABLED") + L"\n";
	} // <advc.250b>
	if(kGame.isOption(GAMEOPTION_SPAH))
	{
		// bTab=false b/c that's a bit too much indentation
		std::wstring* pszPointDistrib = kGame.startPointsAsHandicap().forSettingsScreen(false);
		if(pszPointDistrib != NULL)
			szSettings += *pszPointDistrib;
	} // </advc.250b>
	int iOptions = 0;
	for(int i = 0; i < NUM_GAMEOPTION_TYPES; i++)
	{
		GameOptionTypes eOption = (GameOptionTypes)i;
		// advc.250b:
		if(eOption == GAMEOPTION_ADVANCED_START || eOption == GAMEOPTION_SPAH ||
			!kGame.isOption(eOption) ||
			// advc.104:
			(eOption == GAMEOPTION_AGGRESSIVE_AI && getUWAI().isEnabled()))
		{
			continue;
		}
		iOptions++;
		szSettings += GC.getInfo(eOption).getDescription();
		szSettings += L", ";
	}
	if(iOptions > 0)
		szSettings = szSettings.substr(0, szSettings.length() - 2) + L"\n";
	//CvWString szModName(GC.getModName().getName) // I'd like the prefix to be configurable
	CvWString const szKey = "TXT_KEY_REPLAY_PREFIX";
	CvWString szModName = gDLL->getText(szKey);
	// Don't list mod name if the tag isn't present
	if(szKey.compare(szModName) == 0)
		szSettings = szSettings.substr(0, szSettings.length() - 1); // drop \n
	else
	{
		// Remove brackets
		if(szModName.at(0) == '[' && szModName.at(szModName.length() - 1) == ']')
			szModName = szModName.substr(1, szModName.length() - 2);
		szSettings += szModName + L" Mod";
	}
} // </advc.106h>


int CvReplayInfo::getNumPlayers() const
{
	return (int)m_listPlayerScoreHistory.size();
}


bool CvReplayInfo::isValidPlayer(int i) const
{
	return (i >= 0 && i < (int)m_listPlayerScoreHistory.size());
}

bool CvReplayInfo::isValidTurn(int i) const
{
	return (i >= m_iInitialTurn && i <= m_iFinalTurn);
}

/*	advc: Return type was int. This ID may differ from the ID in the original game,
	but, within the context of a replay, I think it gets used as a proper PlayerTypes ID. */
PlayerTypes CvReplayInfo::getActivePlayer() const
{
	return m_eActivePlayer;
}

LeaderHeadTypes CvReplayInfo::getLeader(PlayerTypes ePlayer) const
{
	if (ePlayer == NO_PLAYER)
		ePlayer = m_eActivePlayer;
	if (isValidPlayer(ePlayer))
		return m_listPlayerScoreHistory[ePlayer].m_eLeader;
	return NO_LEADER;
}

ColorTypes CvReplayInfo::getColor(PlayerTypes ePlayer) const
{
	if (ePlayer == NO_PLAYER)
		ePlayer = m_eActivePlayer;
	if (isValidPlayer(ePlayer))
		return m_listPlayerScoreHistory[ePlayer].m_eColor;
	return NO_COLOR;
}

HandicapTypes CvReplayInfo::getDifficulty() const
{
	return m_eDifficulty;
}

const CvWString& CvReplayInfo::getLeaderName() const
{
	return m_szLeaderName;
}

const CvWString& CvReplayInfo::getCivDescription() const
{
	return m_szCivDescription;
}

const CvWString& CvReplayInfo::getShortCivDescription() const
{
	return m_szShortCivDescription;
}

const CvWString& CvReplayInfo::getCivAdjective() const
{
	return m_szCivAdjective;
}

const CvWString& CvReplayInfo::getMapScriptName() const
{
	return m_szMapScriptName;
}

WorldSizeTypes CvReplayInfo::getWorldSize() const
{
	return m_eWorldSize;
}

ClimateTypes CvReplayInfo::getClimate() const
{
	return m_eClimate;
}

SeaLevelTypes CvReplayInfo::getSeaLevel() const
{
	return m_eSeaLevel;
}

EraTypes CvReplayInfo::getEra() const
{
	return m_eEra;
}

GameSpeedTypes CvReplayInfo::getGameSpeed() const
{
	return m_eGameSpeed;
}

bool CvReplayInfo::isGameOption(GameOptionTypes eOption) const
{
	for (uint i = 0; i < m_listGameOptions.size(); i++)
	{
		if (m_listGameOptions[i] == eOption)
			return true;
	}
	return false;
}

bool CvReplayInfo::isVictoryCondition(VictoryTypes eVictory) const
{
	for (uint i = 0; i < m_listVictoryTypes.size(); i++)
	{
		if (m_listVictoryTypes[i] == eVictory)
			return true;
	}
	return false;
}

VictoryTypes CvReplayInfo::getVictoryType() const
{
	return m_eVictoryType;
}

bool CvReplayInfo::isMultiplayer() const
{
	return m_bMultiplayer;
}


void CvReplayInfo::addReplayMessage(CvReplayMessage* pMessage)
{
	m_listReplayMessages.push_back(pMessage);
}

void CvReplayInfo::clearReplayMessageMap()
{
	for (ReplayMessageList::const_iterator itList = m_listReplayMessages.begin();
		itList != m_listReplayMessages.end(); ++itList)
	{
		CvReplayMessage const* pMessage = *itList;
		if (pMessage != NULL)
			delete pMessage;
	}
	m_listReplayMessages.clear();
}
// advc: To reduce code duplication
bool CvReplayInfo::isReplayMsgValid(uint i) const
{
	return (i < m_listReplayMessages.size() && m_listReplayMessages[i] != NULL);
}

int CvReplayInfo::getReplayMessageTurn(uint i) const
{
	return (isReplayMsgValid(i) ? m_listReplayMessages[i]->getTurn() : -1);
}

ReplayMessageTypes CvReplayInfo::getReplayMessageType(uint i) const
{
	return (isReplayMsgValid(i) ? m_listReplayMessages[i]->getType() : NO_REPLAY_MESSAGE);
}

int CvReplayInfo::getReplayMessagePlotX(uint i) const
{
	return (isReplayMsgValid(i) ? m_listReplayMessages[i]->getPlotX() : -1);
}

int CvReplayInfo::getReplayMessagePlotY(uint i) const
{
	return (isReplayMsgValid(i) ? m_listReplayMessages[i]->getPlotY() : -1);
}

PlayerTypes CvReplayInfo::getReplayMessagePlayer(uint i) const
{
	return (isReplayMsgValid(i) ? m_listReplayMessages[i]->getPlayer() : NO_PLAYER);
}

LPCWSTR CvReplayInfo::getReplayMessageText(uint i) const
{
	return (isReplayMsgValid(i) ? m_listReplayMessages[i]->getText().GetCString() : NULL);
}

ColorTypes CvReplayInfo::getReplayMessageColor(uint i) const
{
	return (isReplayMsgValid(i) ? m_listReplayMessages[i]->getColor() : NO_COLOR);
}


uint CvReplayInfo::getNumReplayMessages() const
{
	return m_listReplayMessages.size();
}


int CvReplayInfo::getInitialTurn() const
{
	return m_iInitialTurn;
}

int CvReplayInfo::getStartYear() const
{
	return m_iStartYear;
}

int CvReplayInfo::getFinalTurn() const
{
	return m_iFinalTurn;
}

const wchar* CvReplayInfo::getFinalDate() const
{
	return m_szFinalDate;
}

CalendarTypes CvReplayInfo::getCalendar() const
{
	return m_eCalendar;
}
// advc:
CvReplayInfo::TurnData const& CvReplayInfo::getTurnData(int iPlayer, int iTurn) const
{
	return m_listPlayerScoreHistory[iPlayer].m_listScore[iTurn-m_iInitialTurn];
}

int CvReplayInfo::getPlayerScore(int iPlayer, int iTurn) const
{
	return (isValidPlayer(iPlayer) && isValidTurn(iTurn) ?
			getTurnData(iPlayer, iTurn).m_iScore : 0);
}

int CvReplayInfo::getPlayerEconomy(int iPlayer, int iTurn) const
{
	return (isValidPlayer(iPlayer) && isValidTurn(iTurn) ?
			getTurnData(iPlayer, iTurn).m_iEconomy : 0);
}

int CvReplayInfo::getPlayerIndustry(int iPlayer, int iTurn) const
{
	return (isValidPlayer(iPlayer) && isValidTurn(iTurn) ?
			getTurnData(iPlayer, iTurn).m_iIndustry : 0);
}

int CvReplayInfo::getPlayerAgriculture(int iPlayer, int iTurn) const
{
	return (isValidPlayer(iPlayer) && isValidTurn(iTurn) ?
			getTurnData(iPlayer, iTurn).m_iAgriculture : 0);
}

int CvReplayInfo::getFinalScore() const
{
	return m->iFinalScore; // advc.707
}
// <advc.707> This new function does what getFinalScore used to do
int CvReplayInfo::getFinalPlayerScore() const
{
	return getPlayerScore(m_eActivePlayer, m_iFinalTurn);
}
// Can now also set the final score to sth. other than the player score
void CvReplayInfo::setFinalScore(int iScore)
{
	m->iFinalScore = iScore;
} // </advc.707>

int CvReplayInfo::getFinalEconomy() const
{
	return getPlayerEconomy(m_eActivePlayer, m_iFinalTurn);
}

int CvReplayInfo::getFinalIndustry() const
{
	return getPlayerIndustry(m_eActivePlayer, m_iFinalTurn);
}

int CvReplayInfo::getFinalAgriculture() const
{
	return getPlayerAgriculture(m_eActivePlayer, m_iFinalTurn);
}

int CvReplayInfo::getNormalizedScore() const
{
	return m->iNormalizedScore;
}

int CvReplayInfo::getMapHeight() const
{
	return m_iMapHeight;
}

int CvReplayInfo::getMapWidth() const
{
	return m_iMapWidth;
}

const unsigned char* CvReplayInfo::getMinimapPixels() const
{
	return m_pcMinimapPixels;
}
// advc.106m:
int CvReplayInfo::getMinimapSize() const
{
	return m_iMinimapSize;
}

const char* CvReplayInfo::getModName() const
{
	//return m_szModName;s
	/*	advc.106i: Pretend to the EXE that every replay is an AdvCiv replay.
		Let CvReplayInfo::read decide which ones to show in HoF. */
	return GC.getModName().getFullPath();
}


bool CvReplayInfo::read(FDataStreamBase& stream)
{
	bool bSuccess = true;
	try
	{
		int iType;
		int iNumTypes;
		int iVersion;
		stream.Read(&iVersion);
		// <advc.106i> Unpack mod id and version
		int iAdvCivID = GC.getDefineINT("SAVE_VERSION");
		int iModID = -1;
		m->bDisplayOtherMods = (GC.getDefineINT("HOF_DISPLAY_OTHER_MOD_REPLAYS") > 0);
		if(iVersion >= 100 * iAdvCivID)
		{
			iModID = iVersion / 100;
			iVersion = iVersion % 100;
			/*  This would have to be an AdvCiv modmod with a different id, or
				any mod that uses a very high replay version number. */
			if(iModID != iAdvCivID && !m->bDisplayOtherMods)
				return false;
		} /* Replay from another mod that has increased the replay version;
			 won't be able to parse that. (Actually, it might be OK - if the mod
			 only appends additional data at the end of the stream.) */
		if(iVersion > REPLAY_VERSION &&
			// Taurus replays set a single bit in the version number
			(iVersion & ~(1 << 7)) > REPLAY_VERSION)
		{
			return false;
		}
		m->iVersionRead = iVersion; // For the checkBounds function
		// </advc.106i>
		if (iVersion < 2)
			return false;
		// <advc.106m> Unpack active player id and minimap resolution
		int iActivePlayer;
		stream.Read(&iActivePlayer);
		if (iActivePlayer >= MAX_CHAR)
		{
			m_iMinimapSize = iActivePlayer / MAX_CHAR;
			iActivePlayer %= MAX_CHAR;
		}
		else setDefaultMinimapSize();
		m_eActivePlayer = (PlayerTypes)iActivePlayer;
		// </advc.106m>
		if(!checkBounds(m_eActivePlayer, 0, 64)) return false; // advc.106i
		stream.Read(&iType);
		m_eDifficulty = (HandicapTypes)iType;
		if(!checkBounds(m_eDifficulty, 0, GC.getNumHandicapInfos())) return false; // advc.106i  (not -1 b/c of advc.250a)
		stream.ReadString(m_szLeaderName);
		if(!checkBounds(m_szLeaderName.length(), 0, 128)) return false; // advc.106i
		stream.ReadString(m_szCivDescription);
		if(!checkBounds(m_szCivDescription.length(), 0, 128)) return false; // advc.106i
		stream.ReadString(m_szShortCivDescription);
		if(!checkBounds(m_szShortCivDescription.length(), 0, 128)) return false; // advc.106i
		stream.ReadString(m_szCivAdjective);
		if(!checkBounds(m_szCivAdjective.length(), 0, 128)) return false; // advc.106i
		if(iVersion > 3)
		{
			stream.ReadString(m_szMapScriptName);
			if(!checkBounds(m_szMapScriptName.length(), 0, 128)) return false; // advc.106i
		}
		else m_szMapScriptName = gDLL->getText("TXT_KEY_TRAIT_PLAYER_UNKNOWN");
		stream.Read(&iType);
		m_eWorldSize = (WorldSizeTypes)iType;
		if(!checkBounds(m_eWorldSize, 0, GC.getNumWorldInfos() - 1)) return false; // advc.106i
		stream.Read(&iType);
		m_eClimate = (ClimateTypes)iType;
		if(!checkBounds(m_eClimate, 0, GC.getNumClimateInfos() - 1)) return false; // advc.106i
		stream.Read(&iType);
		 // <advc.106i> For compatibility with advc.707
		if(iVersion >= 6)
		{
			m->iFinalScore = iType;
			m_eSeaLevel = NO_SEALEVEL; // unused
		}
		else
		{
			m->iFinalScore = MIN_INT; // Compute it later
			m_eSeaLevel = (SeaLevelTypes)iType;
			if(!checkBounds(m_eSeaLevel, 0, GC.getNumSeaLevelInfos() - 1)) return false; // advc.106i
		} // </advc.106i>
		stream.Read(&iType);
		m_eEra = (EraTypes)iType;
		if(!checkBounds(m_eEra, 0, GC.getNumEraInfos() - 1)) return false; // advc.106i
		stream.Read(&iType);
		m_eGameSpeed = (GameSpeedTypes)iType;
		if(!checkBounds(m_eGameSpeed, 0, GC.getNumGameSpeedInfos() - 1)) return false; // advc.106i
		stream.Read(&iNumTypes);
		if(!checkBounds(iNumTypes, 0, NUM_GAMEOPTION_TYPES - 1)) return false; // advc.106i
		for (int i = 0; i < iNumTypes; i++)
		{
			stream.Read(&iType);
			if(!checkBounds(iType, 0, NUM_GAMEOPTION_TYPES - 1)) return false; // advc.106i
			m_listGameOptions.push_back((GameOptionTypes)iType);
		}
		stream.Read(&iNumTypes);
		for (int i = 0; i < iNumTypes; i++)
		{
			stream.Read(&iType);
			if(!checkBounds(iType, 0, GC.getNumVictoryInfos() - 1)) return false; // advc.106i
			m_listVictoryTypes.push_back((VictoryTypes)iType);
		}
		stream.Read(&iType);
		m_eVictoryType = (VictoryTypes)iType;
		if(!checkBounds(m_eVictoryType, -1, GC.getNumVictoryInfos() - 1)) return false; // advc.106i
		stream.Read(&iNumTypes);
		if(!checkBounds(iNumTypes, 0, 50000)) return false; // advc.106i
		for (int i = 0; i < iNumTypes; i++)
		{
			CvReplayMessage* pMessage = new CvReplayMessage(0);
			if (pMessage != NULL)
				pMessage->read(stream);
			m_listReplayMessages.push_back(pMessage);
		}
		stream.Read(&m_iInitialTurn);
		if(!checkBounds(m_iInitialTurn, 0, 1500)) return false; // advc.106i
		stream.Read(&m_iStartYear);
		if(!checkBounds(m_iStartYear, -10000, 100000)) return false; // advc.106i
		stream.Read(&m_iFinalTurn);
		checkBounds(m_iFinalTurn, 0, 10000); // advc.106i
		stream.ReadString(m_szFinalDate);
		if(!checkBounds(m_szFinalDate.length(), 4, 50)) return false; // advc.106i
		stream.Read(&iType);
		m_eCalendar = (CalendarTypes)iType;
		if(!checkBounds(m_eCalendar, 0, NUM_CALENDAR_TYPES - 1)) return false; // advc.106i
		stream.Read(&m->iNormalizedScore);
		if(!checkBounds(m->iNormalizedScore, -10000, 1000000)) return false; // advc.106i
		stream.Read(&iNumTypes);
		if(!checkBounds(iNumTypes, 1, 64)) return false; // advc.106i
		for (int i = 0; i < iNumTypes; i++)
		{
			PlayerInfo info;
			stream.Read(&iType);
			info.m_eLeader = (LeaderHeadTypes)iType;
			if(!checkBounds(info.m_eLeader, 0, GC.getNumLeaderHeadInfos() - 1)) return false; // advc.106i
			stream.Read(&iType);
			info.m_eColor = (ColorTypes)iType;
			if(!checkBounds(info.m_eColor, 0, GC.getNumColorInfos() - 1)) return false; // advc.106i
			int jNumTypes;
			stream.Read(&jNumTypes);
			if(!checkBounds(jNumTypes, 0, 10000)) return false; // advc.106i
			for (int j = 0; j < jNumTypes; j++)
			{
				TurnData data;
				stream.Read(&(data.m_iScore));
				stream.Read(&(data.m_iEconomy));
				stream.Read(&(data.m_iIndustry));
				stream.Read(&(data.m_iAgriculture));
				info.m_listScore.push_back(data);
			}
			m_listPlayerScoreHistory.push_back(info);
		}
		stream.Read(&m_iMapWidth);
		if(!checkBounds(m_iMapWidth, 1, 1000)) return false; // advc.106i
		stream.Read(&m_iMapHeight);
		if(!checkBounds(m_iMapHeight, 1, 1000)) return false; // advc.106i
		SAFE_DELETE_ARRAY(m_pcMinimapPixels); // advc.001 (was SAFE_DELETE)
		m_pcMinimapPixels = new byte[/* advc.106m: */ minimapPixels()];
		stream.Read(/* advc.106m: */ minimapPixels(),
				const_cast<byte*>(m_pcMinimapPixels)); // advc.106n: cast
		stream.Read(&m_bMultiplayer);
		if (iVersion > 2)
		{	// <advc.106i>
			try /*  I've had some issues with m_szModName sometimes remaining
					uninitialized, so I've added a separate try block. */
			{
				stream.ReadString(m_szModName);
				m_szModName.GetLength(); // To check if bad ptr
			}
			catch(...)
			{
				FErrorMsg("Failed to read replay file");
				return false;
			}
			if(m_szModName.empty())
			{
				if(iModID < 0 && GC.getDefineINT("HOF_DISPLAY_BTS_REPLAYS") <= 0)
					return false;
			}
			else if(!m->bDisplayOtherMods &&
				std::strcmp(m_szModName.c_str(), GC.getModName().getFullPath()) != 0)
			{
				return false; // Replay from a different mod
			} // </advc.106i>
		} // <advc.707>
		if(iVersion == 5)
			stream.Read(&m->iFinalScore);
		// </advc.707>
	}
	catch(...)
	{
		FErrorMsg("Failed to read replay file");
		return false;
	} // <advc.707>
	if(m->iFinalScore == MIN_INT)
		m->iFinalScore = getFinalPlayerScore();
	// </advc.707>
	return bSuccess;
}

void CvReplayInfo::write(FDataStreamBase& stream)
{
	//stream.Write(REPLAY_VERSION);
	// <advc.106i> Fold AdvCiv's (hopefully) globally unique id into the replay version
	stream.Write(GC.getDefineINT("SAVE_VERSION") * 100 + REPLAY_VERSION);
	// <advc.106m> Fold minimap resolution into active player ID
	if (!isStoringReplaysAsBtS())
	{
		setMinimapSizeFromXML();
		FAssert(m_iMinimapSize > 0);
		stream.Write(m_iMinimapSize * MAX_CHAR + m_eActivePlayer);
	}
	else // </advc.106m>
		stream.Write(m_eActivePlayer);
	stream.Write(m_eDifficulty);
	stream.WriteString(m_szLeaderName);
	stream.WriteString(m_szCivDescription);
	stream.WriteString(m_szShortCivDescription);
	stream.WriteString(m_szCivAdjective);
	stream.WriteString(m_szMapScriptName);
	stream.Write(m_eWorldSize);
	stream.Write(m_eClimate);
	//stream.Write(m_eSeaLevel);
	/*  advc.106i: m_eSeaLevel is unused in AdvCiv and BtS. Need to stick to the
		BtS replay format. Well, it's probably OK to append additional data at
		the end, but I'm not quite sure. */
	stream.Write(m->iFinalScore); // advc.707
	stream.Write(m_eEra);
	stream.Write(m_eGameSpeed);
	stream.Write((int)m_listGameOptions.size());
	for (uint i = 0; i < m_listGameOptions.size(); i++)
	{
		stream.Write(m_listGameOptions[i]);
	}
	stream.Write((int)m_listVictoryTypes.size());
	for (uint i = 0; i < m_listVictoryTypes.size(); i++)
	{
		stream.Write(m_listVictoryTypes[i]);
	}
	stream.Write(m_eVictoryType);
	stream.Write((int)m_listReplayMessages.size());
	for (uint i = 0; i < m_listReplayMessages.size(); i++)
	{
		if (m_listReplayMessages[i] != NULL)
		{
			m_listReplayMessages[i]->write(stream);
		}
	}
	stream.Write(m_iInitialTurn);
	stream.Write(m_iStartYear);
	stream.Write(m_iFinalTurn);
	stream.WriteString(m_szFinalDate);
	stream.Write(m_eCalendar);
	stream.Write(m->iNormalizedScore);
	stream.Write((int)m_listPlayerScoreHistory.size());
	for (uint i = 0; i < m_listPlayerScoreHistory.size(); i++)
	{
		PlayerInfo& info = m_listPlayerScoreHistory[i];
		stream.Write(info.m_eLeader);
		stream.Write(info.m_eColor);
		stream.Write((int)info.m_listScore.size());
		for (uint j = 0; j < info.m_listScore.size(); j++)
		{
			stream.Write(info.m_listScore[j].m_iScore);
			stream.Write(info.m_listScore[j].m_iEconomy);
			stream.Write(info.m_listScore[j].m_iIndustry);
			stream.Write(info.m_listScore[j].m_iAgriculture);
		}
	}
	stream.Write(m_iMapWidth);
	stream.Write(m_iMapHeight);
	stream.Write(/* <advc.106m> */ minimapPixels() /* </advc.106m> */, m_pcMinimapPixels);
	stream.Write(m_bMultiplayer);
	stream.WriteString(m_szModName);
}
// <advc.106m>
// (Same formula as in BtS; moved from constructor.)
int CvReplayInfo::minimapPixels(int iMinimapSize)
{
	// i.e. 2:1 aspect ratio
	return (iMinimapSize * iMinimapSize) / 2;
}

int CvReplayInfo::minimapPixels() const
{
	return minimapPixels(m_iMinimapSize);
}

void CvReplayInfo::setMinimapSizeFromXML()
{
	if (GC.getDefineINT(CvGlobals::MINIMAP_RENDER_SIZE) >= 10000)
	{
		// Not a reasonable resolution, and can't piggyback that safely into the replay file.
		FErrorMsg("MINIMAP_RENDER_SIZE too large");
		return;
	}
	m_iMinimapSize = GC.getDefineINT(CvGlobals::MINIMAP_RENDER_SIZE);
}

void CvReplayInfo::setDefaultMinimapSize()
{
	m_iMinimapSize = 512; // As in BtS GlobalDefines
} // </advc.106m>

// <advc.106i>
bool CvReplayInfo::checkBounds(int iValue, int iLower, int iUpper) const
{
	/*  If CvReplayInfo::read encounters a replay from another mod, it won't be able
		to tell until it reaches the mod name at the end of the stream. I'm not aware
		of any mods that change the replay format, but, if they do, the read function
		is going to get out of step, which may cause an exception. There's a catch(...),
		but that's not going to catch hardware exceptions unless the /EHa compiler option
		is used. (AdvCiv, like just about every mod, uses /EHsc.) So I think there could
		be a crash, and, as all mods place their replays in the same folder, encountering
		a very strange replay doesn't seem so unlikely. */
	if(m->bDisplayOtherMods) // Still want sanity checks then, but be more generous.
		iUpper *= 2;
	if(iValue < iLower || iValue > iUpper)
	{
		/*  The assertion is only there to warn me when an AdvCiv replay gets
			rejected. If another mod has changed the replay format, then probably
			just once, from version 4 to 5, but not to REPLAY_VERSION. */
		FAssert(m->bDisplayOtherMods || m->iVersionRead < REPLAY_VERSION);
		return false;
	}
	return true;
}

bool CvReplayInfo::isStoringReplaysAsBtS() const
{
	if (BUGOption::isEnabled("MainInterface__ModNameInReplays", false,
		false)) // BUG not being available is OK, we'll get another call later.
	{
		return false;
	}
	// <advc.106m>
	if (GC.getDefineINT(CvGlobals::MINIMAP_RENDER_SIZE) != 512)
	{
		FErrorMsg("MINIMAP_RENDER_SIZE incompatible with BtS replay format;"
				" Mod-Name-in-Replays option ignored");
		return false;
	} // </advc.106m>
	/*	The option says to store as BtS, but we'll ignore that if running the replay
		might crash BtS. AdvCiv won't have that problem, but a mod-mod might. */
	if (getWorldSize() > 5)
	{
		FErrorMsg("World size incompatible with BtS replay format");
		return false;
	}
	if (getGameSpeed() > 3)
	{
		FErrorMsg("Game speed incompatible with BtS replay format");
		return false;
	}
	for (int iVictory = 7; iVictory < GC.getNumVictoryInfos(); iVictory++)
	{
		if (isVictoryCondition((VictoryTypes)iVictory))
		{
			FErrorMsg("Enabled victory incompatible with BtS replay format");
			return false;
		}
	}
	if (getDifficulty() > 8)
	{
		FErrorMsg("Difficulty level (handicap) incompatible with BtS replay format");
		return false;
	}
	FOR_EACH_ENUM(Player)
	{
		if (GET_PLAYER(eLoopPlayer).isEverAlive() && getColor(eLoopPlayer) > 126)
		{
			FErrorMsg("Player (text) color incompatible with BtS replay format");
			return false;
		}
	}
	/*	(Not going to check getReplayMessageColor for every replay message;
		there can be a lot of messages, seems a little excessive.) */
	return true;		
} // </advc.106i>
