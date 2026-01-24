#include "CvGameCoreDLL.h"
#include "CvMessageControl.h"
#include "CvMessageData.h"
#include "CvGame.h"

CvMessageControl& CvMessageControl::getInstance()
{
	static CvMessageControl m_sInstance;
	return m_sInstance;
}

// advc: Make the active-player stuff a little less repetitive
namespace
{
	__inline PlayerTypes getActivePlayer()
	{
		return GC.getGame().getActivePlayer();
	}
	__inline bool isActive()
	{
		return (getActivePlayer() != NO_PLAYER);
	}
}

void CvMessageControl::sendExtendedGame()
{
	if (isActive())
		gDLL->sendMessageData(new CvNetExtendedGame(getActivePlayer()));
}

void CvMessageControl::sendAutoMoves()
{
	if (isActive())
		gDLL->sendMessageData(new CvNetAutoMoves(getActivePlayer()));
}

void CvMessageControl::sendTurnComplete()
{
	if (isActive())
		gDLL->sendMessageData(new CvNetTurnComplete(getActivePlayer()));
}

void CvMessageControl::sendPushOrder(int iCityID, OrderTypes eOrder, int iData,
	//bool bAlt, bool bShift, bool bCtrl)
	bool bSave, bool bPop, int iPosition) // K-Mod
{
	if (isActive())
	{
		gDLL->sendMessageData(new CvNetPushOrder(getActivePlayer(),
				iCityID, eOrder, iData, bSave, bPop, iPosition));
	}
}

void CvMessageControl::sendPopOrder(int iCity, int iNum)
{
	if (isActive())
		gDLL->sendMessageData(new CvNetPopOrder(getActivePlayer(), iCity, iNum));
}

void CvMessageControl::sendDoTask(int iCity, TaskTypes eTask, int iData1, int iData2,
	bool bOption, bool bAlt, bool bShift, bool bCtrl)
{
	if (isActive())
	{
		gDLL->sendMessageData(new CvNetDoTask(getActivePlayer(),
				iCity, eTask, iData1, iData2, bOption, bAlt, bShift, bCtrl));
	}
}

void CvMessageControl::sendUpdateCivics(/* advc.enum: */ CivicMap const& kCivics)
{
	if (isActive())
		gDLL->sendMessageData(new CvNetUpdateCivics(getActivePlayer(), kCivics));
}

void CvMessageControl::sendResearch(TechTypes eTech, int iDiscover, bool bShift)
{
	if (isActive())
		gDLL->sendMessageData(new CvNetResearch(getActivePlayer(), eTech, iDiscover, bShift));
}

void CvMessageControl::sendEspionageSpendingWeightChange(TeamTypes eTargetTeam, int iChange)
{
	if (isActive())
		gDLL->sendMessageData(new CvNetEspionageChange(getActivePlayer(), eTargetTeam, iChange));
}

void CvMessageControl::sendAdvancedStartAction(AdvancedStartActionTypes eAction,
	PlayerTypes ePlayer, int iX, int iY, int iData, bool bAdd)
{
	gDLL->sendMessageData(new CvNetAdvancedStartAction(eAction,
			ePlayer, iX, iY, iData, bAdd));
}

void CvMessageControl::sendModNetMessage(
	int iData1, int iData2, int iData3, int iData4, int iData5)
{
	gDLL->sendMessageData(new CvNetModNetMessage(
			iData1, iData2, iData3, iData4, iData5));
}

void CvMessageControl::sendConvert(ReligionTypes eReligion)
{
	if (isActive())
		gDLL->sendMessageData(new CvNetConvert(getActivePlayer(), eReligion));
}

void CvMessageControl::sendEmpireSplit(PlayerTypes ePlayer, int iPlayerID)
{
	gDLL->sendMessageData(new CvNetEmpireSplit(ePlayer, iPlayerID));
}

void CvMessageControl::sendFoundReligion(PlayerTypes ePlayer,
	ReligionTypes eReligion, ReligionTypes eSlotReligion)
{
	gDLL->sendMessageData(new CvNetFoundReligion(ePlayer, eReligion, eSlotReligion));
}

void CvMessageControl::sendLaunch(PlayerTypes ePlayer, VictoryTypes eVictory)
{
	gDLL->sendMessageData(new CvNetLaunchSpaceship(ePlayer, eVictory));
}

void CvMessageControl::sendEventTriggered(PlayerTypes ePlayer,
	EventTypes eEvent, int iEventTriggeredId)
{
	gDLL->sendMessageData(new CvNetEventTriggered(ePlayer, eEvent, iEventTriggeredId));
}

void CvMessageControl::sendJoinGroup(int iUnitID, int iHeadID)
{
	if (isActive())
		gDLL->sendMessageData(new CvNetJoinGroup(getActivePlayer(), iUnitID, iHeadID));
}

void CvMessageControl::sendPushMission(int iUnitID, MissionTypes eMission,
	int iData1, int iData2, MovementFlags eFlags, bool bShift,
	bool bModified) // advc.011b
{
	if (isActive())
	{
		gDLL->sendMessageData(new CvNetPushMission(getActivePlayer(),
				iUnitID, eMission, iData1, iData2, eFlags, bShift,
				bModified)); // advc.011b
	}
}

void CvMessageControl::sendAutoMission(int iUnitID)
{
	if (isActive())
		gDLL->sendMessageData(new CvNetAutoMission(getActivePlayer(), iUnitID));
}

void CvMessageControl::sendDoCommand(int iUnitID, CommandTypes eCommand,
	int iData1, int iData2, bool bAlt)
{
	if (isActive())
	{
		gDLL->sendMessageData(new CvNetDoCommand(getActivePlayer(),
				iUnitID, eCommand, iData1, iData2, bAlt));
	}
}

void CvMessageControl::sendPercentChange(CommerceTypes eCommerce, int iChange)
{
	if (isActive())
	{
		gDLL->sendMessageData(new CvNetPercentChange(getActivePlayer(),
				eCommerce, iChange));
	}
}

void CvMessageControl::sendChangeVassal(TeamTypes eMasterTeam,
	bool bVassal, bool bCapitulated)
{
	if (isActive())
	{
		gDLL->sendMessageData(new CvNetChangeVassal(getActivePlayer(),
				eMasterTeam, bVassal, bCapitulated));
	}
}

void CvMessageControl::sendChooseElection(int iSelection, int iVoteId)
{
	if (isActive())
	{
		gDLL->sendMessageData(new CvNetChooseElection(getActivePlayer(),
				iSelection, iVoteId));
	}
}

void CvMessageControl::sendDiploVote(int iVoteId, PlayerVoteTypes eChoice)
{
	if (isActive())
		gDLL->sendMessageData(new CvNetDiploVote(getActivePlayer(), iVoteId, eChoice));
}

void CvMessageControl::sendChangeWar(TeamTypes eRivalTeam, bool bWar)
{
	if (isActive())
		gDLL->sendMessageData(new CvNetChangeWar(getActivePlayer(), eRivalTeam, bWar));
}

void CvMessageControl::sendPing(int iX, int iY)
{
	if (isActive())
		gDLL->sendMessageData(new CvNetPing(getActivePlayer(), iX, iY));
}
// advc.003g:
void CvMessageControl::sendFPTest(int iResult)
{
	gDLL->sendMessageData(new CvNetFPTest(getActivePlayer(), iResult));
}
// advc.190c:
void CvMessageControl::sendCivLeaderSetup(CvInitCore const& kInitCore)
{
	gDLL->sendMessageData(new CvNetCivLeaderSetup(getActivePlayer(), &kInitCore));
}
