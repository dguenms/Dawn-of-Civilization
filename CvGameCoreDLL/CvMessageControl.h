#ifndef CV_MESSAGE_CONTROL
#define CV_MESSAGE_CONTROL

class CvMessageControl
{
public:
	DllExport static CvMessageControl& getInstance();
	void sendExtendedGame();
	void sendAutoMoves();
	void sendTurnComplete();
	void sendPushOrder(int iCityID, OrderTypes eOrder, int iData, bool bAlt, bool bShift, bool bCtrl);
	void sendPopOrder(int iCity, int iNum);
	DllExport void sendDoTask(int iCityID, TaskTypes eTask, int iData1, int iData2, bool bOption, bool bAlt, bool bShift, bool bCtrl);
	void sendUpdateCivics(const std::vector<CivicTypes>& aeCivics);
	void sendResearch(TechTypes eTech, int iDiscover, bool bShift);
	void sendEspionageSpendingWeightChange(TeamTypes eTargetTeam, int iChange);
	DllExport void sendAdvancedStartAction(AdvancedStartActionTypes eAction, PlayerTypes ePlayer, int iX, int iY, int iData, bool bAdd);
	void sendModNetMessage(int iData1, int iData2, int iData3, int iData4, int iData5);
	void sendConvert(ReligionTypes eReligion);
	void sendEmpireSplit(PlayerTypes ePlayer, int iAreaId);
	void sendFoundReligion(PlayerTypes ePlayer, ReligionTypes eReligion, ReligionTypes eSlotReligion);
	DllExport void sendLaunch(PlayerTypes ePlayer, VictoryTypes eVictory);
	void sendEventTriggered(PlayerTypes ePlayer, EventTypes eEvent, int iEventTriggeredId);
	DllExport void sendJoinGroup(int iUnitID, int iHeadID);
	void sendPushMission(int iUnitID, MissionTypes eMission, int iData1, int iData2, int iFlags, bool bShift);
	void sendAutoMission(int iUnitID);
	void sendDoCommand(int iUnitID, CommandTypes eCommand, int iData1, int iData2, bool bAlt);
	void sendPercentChange(CommerceTypes eCommerce, int iChange);
	void sendChangeVassal(TeamTypes eMasterTeam, bool bVassal, bool bCapitulated);
	void sendChooseElection(int iSelection, int iVoteId);
	void sendDiploVote(int iVoteId, PlayerVoteTypes eChoice);
	DllExport void sendChangeWar(TeamTypes eRivalTeam, bool bWar);
	DllExport void sendPing(int iX, int iY);
};


#endif