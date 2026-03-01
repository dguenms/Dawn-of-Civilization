#ifndef CV_MESSAGE_DATA
#define CV_MESSAGE_DATA

class FDataStreamBase;

class CvMessageData
{
public:
	virtual ~CvMessageData();
	virtual void Debug(char* szAddendum) = 0;
	virtual void Execute() = 0;
	virtual void PutInBuffer(FDataStreamBase* pStream) = 0;
	virtual void SetFromBuffer(FDataStreamBase* pStream) = 0;

	DllExport GameMessageTypes getType() const;

	DllExport static CvMessageData* createMessage(GameMessageTypes eType);

protected: // advc
	CvMessageData(GameMessageTypes eType);

private:
	GameMessageTypes m_eType;
};

class CvNetExtendedGame : public CvMessageData
{
public:
	CvNetExtendedGame(PlayerTypes ePlayer = NO_PLAYER);
	virtual void Debug(char* szAddendum);
	virtual void Execute();
	virtual void PutInBuffer(FDataStreamBase* pStream);
	virtual void SetFromBuffer(FDataStreamBase* pStream);
private:
	PlayerTypes m_ePlayer;
};

class CvNetAutoMoves : public CvMessageData
{
public:
	CvNetAutoMoves(PlayerTypes ePlayer = NO_PLAYER);
	virtual void Debug(char* szAddendum);
	virtual void Execute();
	virtual void PutInBuffer(FDataStreamBase* pStream);
	virtual void SetFromBuffer(FDataStreamBase* pStream);
private:
	PlayerTypes m_ePlayer;
};

class CvNetTurnComplete : public CvMessageData
{
public:
	CvNetTurnComplete(PlayerTypes ePlayer = NO_PLAYER);
	virtual void Debug(char* szAddendum);
	virtual void Execute();
	virtual void PutInBuffer(FDataStreamBase* pStream);
	virtual void SetFromBuffer(FDataStreamBase* pStream);
private:
	PlayerTypes m_ePlayer;
};

class CvNetPushOrder : public CvMessageData
{
public:
	//CvNetPushOrder();
	//CvNetPushOrder(PlayerTypes ePlayer, int iCityID, OrderTypes eOrder, int iData, bool bAlt, bool bShift, bool bCtrl);
	// K-Mod
	CvNetPushOrder(PlayerTypes ePlayer = NO_PLAYER, int iCityID = -1, OrderTypes eOrder = NO_ORDER, int iData = -1, bool bSave = false, bool bPop = true, int iPosition = 0)
		: CvMessageData(GAMEMESSAGE_PUSH_ORDER), m_ePlayer(ePlayer), m_iCityID(iCityID), m_eOrder(eOrder), m_iData(iData), m_bSave(bSave), m_bPop(bPop), m_iPosition(iPosition) { }
	// K-Mod end
	virtual void Debug(char* szAddendum);
	virtual void Execute();
	virtual void PutInBuffer(FDataStreamBase* pStream);
	virtual void SetFromBuffer(FDataStreamBase* pStream);
private:
	PlayerTypes m_ePlayer;
	int m_iCityID;
	OrderTypes m_eOrder;
	int m_iData;
	/*bool m_bAlt;
	bool m_bShift;
	bool m_bCtrl;*/
	// K-Mod
	bool m_bSave;
	bool m_bPop;
	int m_iPosition;
	// K-Mod end
};

class CvNetPopOrder : public CvMessageData
{
public:
	CvNetPopOrder();
	CvNetPopOrder(PlayerTypes ePlayer, int iCityID, int iNum);
	virtual void Debug(char* szAddendum);
	virtual void Execute();
	virtual void PutInBuffer(FDataStreamBase* pStream);
	virtual void SetFromBuffer(FDataStreamBase* pStream);
private:
	PlayerTypes m_ePlayer;
	int m_iCityID;
	int m_iNum;
};

class CvNetDoTask : public CvMessageData
{
public:
	CvNetDoTask();
	CvNetDoTask(PlayerTypes ePlayer, int iCityID, TaskTypes eTask, int iData1, int iData2, bool bOption, bool bAlt, bool bShift, bool bCtrl);
	virtual void Debug(char* szAddendum);
	virtual void Execute();
	virtual void PutInBuffer(FDataStreamBase* pStream);
	virtual void SetFromBuffer(FDataStreamBase* pStream);
private:
	PlayerTypes m_ePlayer;
	int m_iCityID;
	TaskTypes m_eTask;
	int m_iData1;
	int m_iData2;
	bool m_bOption;
	bool m_bAlt;
	bool m_bShift;
	bool m_bCtrl;
};

class CvNetUpdateCivics : public CvMessageData
{
public:
	CvNetUpdateCivics();
	CvNetUpdateCivics(PlayerTypes ePlayer, CivicMap const& kCivics);
	virtual void Debug(char* szAddendum);
	virtual void Execute();
	virtual void PutInBuffer(FDataStreamBase* pStream);
	virtual void SetFromBuffer(FDataStreamBase* pStream);
private:
	PlayerTypes m_ePlayer;
	CivicMap m_aeCivics; // advc.enum
};

class CvNetResearch : public CvMessageData
{
public:
	CvNetResearch();
	CvNetResearch(PlayerTypes ePlayer, TechTypes eTech, int iDiscover, bool bShift);
	virtual void Debug(char* szAddendum);
	virtual void Execute();
	virtual void PutInBuffer(FDataStreamBase* pStream);
	virtual void SetFromBuffer(FDataStreamBase* pStream);
private:
	PlayerTypes m_ePlayer;
	int m_iDiscover;
	bool m_bShift;
	TechTypes m_eTech;
};

class CvNetEspionageChange : public CvMessageData
{
public:
	CvNetEspionageChange();
	CvNetEspionageChange(PlayerTypes ePlayer, TeamTypes eTargetTeam, int iChange);
	virtual void Debug(char* szAddendum);
	virtual void Execute();
	virtual void PutInBuffer(FDataStreamBase* pStream);
	virtual void SetFromBuffer(FDataStreamBase* pStream);
private:
	PlayerTypes m_ePlayer;
	TeamTypes m_eTargetTeam;
	int m_iChange;
};

class CvNetAdvancedStartAction : public CvMessageData
{
public:
	CvNetAdvancedStartAction(AdvancedStartActionTypes eAction = NO_ADVANCEDSTARTACTION, PlayerTypes ePlayer = NO_PLAYER, int iX = -1, int iY = -1, int iData = -1, bool bAdd = true);
	void Debug(char* szAddendum);
	virtual void Execute();
	virtual void PutInBuffer(FDataStreamBase* pStream);
	virtual void SetFromBuffer(FDataStreamBase* pStream);
private:
	AdvancedStartActionTypes m_eAction;
	PlayerTypes m_ePlayer;
	int m_iX;
	int m_iY;
	int m_iData;
	bool m_bAdd;
};

class CvNetModNetMessage : public CvMessageData
{
public:
	CvNetModNetMessage(int iData1 = -1, int iData2 = -1, int iData3 = -1, int iData4 = -1, int iData5 = -1);
	virtual void Debug(char* szAddendum);
	virtual void Execute();
	virtual void PutInBuffer(FDataStreamBase* pStream);
	virtual void SetFromBuffer(FDataStreamBase* pStream);
private:
	int m_iData1;
	int m_iData2;
	int m_iData3;
	int m_iData4;
	int m_iData5;
};

//  Convert religions
class CvNetConvert : public CvMessageData
{
public:
	CvNetConvert(PlayerTypes ePlayer = NO_PLAYER, ReligionTypes eReligion = NO_RELIGION);
	virtual void Debug(char* szAddendum);
	virtual void Execute();
	virtual void PutInBuffer(FDataStreamBase* pStream);
	virtual void SetFromBuffer(FDataStreamBase* pStream);
private:
	PlayerTypes m_ePlayer;
	ReligionTypes m_eReligion;
};

class CvNetEmpireSplit : public CvMessageData
{
public:
	CvNetEmpireSplit(PlayerTypes ePlayer = NO_PLAYER, int iPlayerID = -1);
	virtual void Debug(char* szAddendum);
	virtual void Execute();
	virtual void PutInBuffer(FDataStreamBase* pStream);
	virtual void SetFromBuffer(FDataStreamBase* pStream);
private:
	PlayerTypes m_ePlayer;
	int m_iPlayerID;
};

class CvNetFoundReligion : public CvMessageData
{
public:
	CvNetFoundReligion(PlayerTypes ePlayer = NO_PLAYER, ReligionTypes eReligion = NO_RELIGION, ReligionTypes eSlotReligion = NO_RELIGION);
	virtual void Debug(char* szAddendum);
	virtual void Execute();
	virtual void PutInBuffer(FDataStreamBase* pStream);
	virtual void SetFromBuffer(FDataStreamBase* pStream);
private:
	PlayerTypes m_ePlayer;
	ReligionTypes m_eReligion;
	ReligionTypes m_eSlotReligion;
};

class CvNetLaunchSpaceship : public CvMessageData
{
public:
	CvNetLaunchSpaceship(PlayerTypes ePlayer = NO_PLAYER, VictoryTypes eVictory = NO_VICTORY);
	virtual void Debug(char* szAddendum);
	virtual void Execute();
	virtual void PutInBuffer(FDataStreamBase* pStream);
	virtual void SetFromBuffer(FDataStreamBase* pStream);
private:
	PlayerTypes m_ePlayer;
	VictoryTypes m_eVictory;
};

class CvNetEventTriggered : public CvMessageData
{
public:
	CvNetEventTriggered(PlayerTypes ePlayer = NO_PLAYER, EventTypes eEvent = NO_EVENT, int iEventTriggeredId = -1);
	virtual void Debug(char* szAddendum);
	virtual void Execute();
	virtual void PutInBuffer(FDataStreamBase* pStream);
	virtual void SetFromBuffer(FDataStreamBase* pStream);
private:
	PlayerTypes m_ePlayer;
	EventTypes m_eEvent;
	int m_iEventTriggeredId;
};

class CvNetJoinGroup : public CvMessageData
{
public:
	CvNetJoinGroup();
	CvNetJoinGroup(PlayerTypes ePlayer, int iUnitID, int iHeadID);
	virtual void Debug(char* szAddendum);
	virtual void Execute();
	virtual void PutInBuffer(FDataStreamBase* pStream);
	virtual void SetFromBuffer(FDataStreamBase* pStream);
private:
	PlayerTypes m_ePlayer;
	int m_iUnitID;
	int m_iHeadID;
};

class CvNetPushMission : public CvMessageData
{
public:
	CvNetPushMission();
	CvNetPushMission(PlayerTypes ePlayer, int iUnitID, MissionTypes eMission,
			int iData1, int iData2, MovementFlags eFlags, bool bShift,
			bool bModified); // advc.011b
	virtual void Debug(char* szAddendum);
	virtual void Execute();
	virtual void PutInBuffer(FDataStreamBase* pStream);
	virtual void SetFromBuffer(FDataStreamBase* pStream);
private:
	PlayerTypes m_ePlayer;
	int m_iUnitID;
	MissionTypes m_eMission;
	int m_iData1;
	int m_iData2;
	MovementFlags m_eFlags;
	bool m_bShift;
	// advc.011b: Modifier key down (could be anything except Shift)
	bool m_bModified;
};

class CvNetAutoMission : public CvMessageData
{
public:
	CvNetAutoMission();
	CvNetAutoMission(PlayerTypes ePlayer, int iUnitID);
	virtual void Debug(char* szAddendum);
	virtual void Execute();
	virtual void PutInBuffer(FDataStreamBase* pStream);
	virtual void SetFromBuffer(FDataStreamBase* pStream);
private:
	PlayerTypes m_ePlayer;
	int m_iUnitID;
};

class CvNetDoCommand : public CvMessageData
{
public:
	CvNetDoCommand();
	CvNetDoCommand(PlayerTypes ePlayer, int iUnitID, CommandTypes eCommand, int iData1, int iData2, bool bAlt);
	virtual void Debug(char* szAddendum);
	virtual void Execute();
	virtual void PutInBuffer(FDataStreamBase* pStream);
	virtual void SetFromBuffer(FDataStreamBase* pStream);
private:
	PlayerTypes m_ePlayer;
	int m_iUnitID;
	CommandTypes m_eCommand;
	int m_iData1;
	int m_iData2;
	bool m_bAlt;
};

class CvNetPercentChange : public CvMessageData
{
public:
	CvNetPercentChange();
	CvNetPercentChange(PlayerTypes ePlayer, CommerceTypes eCommerce, int iChange);
	virtual void Debug(char* szAddendum);
	virtual void Execute();
	virtual void PutInBuffer(FDataStreamBase* pStream);
	virtual void SetFromBuffer(FDataStreamBase* pStream);
private:
	PlayerTypes m_ePlayer;
	int m_iChange;
	CommerceTypes m_eCommerce;
};

class CvNetChangeVassal : public CvMessageData
{
public:
	CvNetChangeVassal();
	CvNetChangeVassal(PlayerTypes ePlayer, TeamTypes eMasterTeam, bool bVassal, bool bCapitulated);
	virtual void Debug(char* szAddendum);
	virtual void Execute();
	virtual void PutInBuffer(FDataStreamBase* pStream);
	virtual void SetFromBuffer(FDataStreamBase* pStream);
private:
	bool m_bVassal;
	bool m_bCapitulated;
	PlayerTypes m_ePlayer;
	TeamTypes m_eMasterTeam;
};

class CvNetChooseElection : public CvMessageData
{
public:
	CvNetChooseElection();
	CvNetChooseElection(PlayerTypes ePlayer, int iSelection, int iVoteId);
	virtual void Debug(char* szAddendum);
	virtual void Execute();
	virtual void PutInBuffer(FDataStreamBase* pStream);
	virtual void SetFromBuffer(FDataStreamBase* pStream);
private:
	PlayerTypes m_ePlayer;
	int m_iSelection;
	int m_iVoteId;
};

class CvNetDiploVote : public CvMessageData
{
public:
	CvNetDiploVote();
	CvNetDiploVote(PlayerTypes ePlayer, int iVoteId, PlayerVoteTypes eChoice);
	virtual void Debug(char* szAddendum);
	virtual void Execute();
	virtual void PutInBuffer(FDataStreamBase* pStream);
	virtual void SetFromBuffer(FDataStreamBase* pStream);
private:
	PlayerTypes m_ePlayer;
	int m_iVoteId;
	PlayerVoteTypes m_eChoice;
};

class CvNetChangeWar : public CvMessageData
{
public:
	CvNetChangeWar();
	CvNetChangeWar(PlayerTypes ePlayer, TeamTypes eRivalTeam, bool bWar);
	virtual void Debug(char* szAddendum);
	virtual void Execute();
	virtual void PutInBuffer(FDataStreamBase* pStream);
	virtual void SetFromBuffer(FDataStreamBase* pStream);
private:
	bool m_bWar;
	PlayerTypes m_ePlayer;
	TeamTypes m_eRivalTeam;
};

class CvNetPing : public CvMessageData
{
public:
	CvNetPing(PlayerTypes ePlayer = NO_PLAYER, int iX = 0, int iY = 0);
	virtual void Debug(char* szAddendum);
	virtual void Execute();
	virtual void PutInBuffer(FDataStreamBase* pStream);
	virtual void SetFromBuffer(FDataStreamBase* pStream);
private:
	PlayerTypes m_ePlayer;
	int m_iX;
	int m_iY;
};
// advc.003g:
class CvNetFPTest : public CvMessageData
{
public:
	CvNetFPTest(PlayerTypes ePlayer = NO_PLAYER, int iResult = MIN_INT);
	virtual void Debug(char* szAddendum);
	virtual void Execute();
	virtual void PutInBuffer(FDataStreamBase* pStream);
	virtual void SetFromBuffer(FDataStreamBase* pStream);
private:
	PlayerTypes m_ePlayer;
	int m_iResult;
};
// advc.190c:
class CvNetCivLeaderSetup : public CvMessageData
{
public:
	CvNetCivLeaderSetup(PlayerTypes ePlayer = NO_PLAYER, CvInitCore const* pInitCore = NULL);
	virtual void Debug(char* szAddendum);
	virtual void Execute();
	virtual void PutInBuffer(FDataStreamBase* pStream);
	virtual void SetFromBuffer(FDataStreamBase* pStream);
private:
	PlayerTypes m_ePlayer;
	ArrayEnumMap<PlayerTypes,bool> m_abCivChosenRandomly;
	ArrayEnumMap<PlayerTypes,bool> m_abLeaderChosenRandomly;
};

#endif
