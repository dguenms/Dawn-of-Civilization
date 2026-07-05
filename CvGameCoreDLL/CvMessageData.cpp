#include "CvGameCoreDLL.h"
#include "CvMessageData.h"
#include "CvInfo_Command.h"
#include "CvGamePlay.h"
#include "CvCity.h"
#include "CvUnit.h"
#include "CvSelectionGroup.h"


CvMessageData* CvMessageData::createMessage(GameMessageTypes eType)
{
	switch (eType)
	{
	case GAMEMESSAGE_EXTENDED_GAME:
		return new CvNetExtendedGame();
	case GAMEMESSAGE_AUTO_MOVES:
		return new CvNetAutoMoves();
	case GAMEMESSAGE_TURN_COMPLETE:
		return new CvNetTurnComplete();
	case GAMEMESSAGE_PUSH_ORDER:
		return new CvNetPushOrder();
	case GAMEMESSAGE_POP_ORDER:
		return new CvNetPopOrder();
	case GAMEMESSAGE_DO_TASK:
		return new CvNetDoTask();
	case GAMEMESSAGE_UPDATE_CIVICS:
		return new CvNetUpdateCivics();
	case GAMEMESSAGE_RESEARCH:
		return new CvNetResearch();
	case GAMEMESSAGE_ESPIONAGE_CHANGE:
		return new CvNetEspionageChange();
	case GAMEMESSAGE_ADVANCED_START_ACTION:
		return new CvNetAdvancedStartAction();
	case GAMEMESSAGE_MOD_NET_MESSAGE:
		return new CvNetModNetMessage();
	case GAMEMESSAGE_CONVERT:
		return new CvNetConvert();
	case GAMEMESSAGE_EMPIRE_SPLIT:
		return new CvNetEmpireSplit();
	case GAMEMESSAGE_FOUND_RELIGION:
		return new CvNetFoundReligion();
	case GAMEMESSAGE_LAUNCH_SPACESHIP:
		return new CvNetLaunchSpaceship();
	case GAMEMESSAGE_EVENT_TRIGGERED:
		return new CvNetEventTriggered();
	case GAMEMESSAGE_JOIN_GROUP:
		return new CvNetJoinGroup();
	case GAMEMESSAGE_PUSH_MISSION:
		return new CvNetPushMission();
	case GAMEMESSAGE_AUTO_MISSION:
		return new CvNetAutoMission();
	case GAMEMESSAGE_DO_COMMAND:
		return new CvNetDoCommand();
	case GAMEMESSAGE_PERCENT_CHANGE:
		return new CvNetPercentChange();
	case GAMEMESSAGE_CHANGE_VASSAL:
		return new CvNetChangeVassal();
	case GAMEMESSAGE_CHOOSE_ELECTION:
		return new CvNetChooseElection();
	case GAMEMESSAGE_DIPLO_VOTE:
		return new CvNetDiploVote();
	case GAMEMESSAGE_CHANGE_WAR:
		return new CvNetChangeWar();
	case GAMEMESSAGE_PING:
		return new CvNetPing();
	// <advc.003g>
	case GAMEMESSAGE_FP_TEST:
		return new CvNetFPTest(); // </advc.003g>
	// <advc.190c>
	case GAMEMESSAGE_CIV_LEADER_SETUP:
		return new CvNetCivLeaderSetup(); // </advc.190c>
	default:
		FErrorMsg("Unknown message type");
	}
	return NULL;
}

CvMessageData::CvMessageData(GameMessageTypes eType) :
	m_eType(eType)
{
}

CvMessageData::~CvMessageData()
{
}

GameMessageTypes CvMessageData::getType() const
{
	return m_eType;
}

CvNetExtendedGame::CvNetExtendedGame(PlayerTypes ePlayer) :
	CvMessageData(GAMEMESSAGE_EXTENDED_GAME), m_ePlayer(ePlayer)
{
}

void CvNetExtendedGame::Debug(char* szAddendum)
{
	sprintf(szAddendum, "Extended Game, %d", m_ePlayer);
}

void CvNetExtendedGame::Execute()
{
	if (m_ePlayer != NO_PLAYER)
	{
		GET_PLAYER(m_ePlayer).makeExtendedGame();
	}
}

void CvNetExtendedGame::PutInBuffer(FDataStreamBase* pStream)
{
	pStream->Write(m_ePlayer);
}

void CvNetExtendedGame::SetFromBuffer(FDataStreamBase* pStream)
{
	pStream->Read((int*)&m_ePlayer);
}

CvNetAutoMoves::CvNetAutoMoves(PlayerTypes ePlayer) :
	CvMessageData(GAMEMESSAGE_AUTO_MOVES), m_ePlayer(ePlayer)
{
}

void CvNetAutoMoves::Debug(char* szAddendum)
{
	sprintf(szAddendum, "Auto Moves, %d", m_ePlayer);
}

void CvNetAutoMoves::Execute()
{
	if (m_ePlayer != NO_PLAYER)
	{
		GET_PLAYER(m_ePlayer).setAutoMoves(true);
	}
}

void CvNetAutoMoves::PutInBuffer(FDataStreamBase* pStream)
{
	pStream->Write(m_ePlayer);
}

void CvNetAutoMoves::SetFromBuffer(FDataStreamBase* pStream)
{
	pStream->Read((int*)&m_ePlayer);
}

CvNetTurnComplete::CvNetTurnComplete(PlayerTypes ePlayer) :
	CvMessageData(GAMEMESSAGE_TURN_COMPLETE), m_ePlayer(ePlayer)
{
}

void CvNetTurnComplete::Debug(char* szAddendum)
{
	sprintf(szAddendum, "Turn Complete, %d", m_ePlayer);
}

void CvNetTurnComplete::Execute()
{
	if (m_ePlayer != NO_PLAYER)
	{
		GET_PLAYER(m_ePlayer).setEndTurn(true);
	}
}

void CvNetTurnComplete::PutInBuffer(FDataStreamBase* pStream)
{
	pStream->Write(m_ePlayer);
}

void CvNetTurnComplete::SetFromBuffer(FDataStreamBase* pStream)
{
	pStream->Read((int*)&m_ePlayer);
}

/*CvNetPushOrder::CvNetPushOrder() : CvMessageData(GAMEMESSAGE_PUSH_ORDER), m_ePlayer(NO_PLAYER), m_iCityID(-1), m_eOrder(NO_ORDER), m_iData(-1), m_bAlt(false), m_bShift(false), m_bCtrl(false) {}

CvNetPushOrder::CvNetPushOrder(PlayerTypes ePlayer, int iCityID, OrderTypes eOrder, int iData, bool bAlt, bool bShift, bool bCtrl) : CvMessageData(GAMEMESSAGE_PUSH_ORDER), m_ePlayer(ePlayer), m_iCityID(iCityID), m_eOrder(eOrder), m_iData(iData), m_bAlt(bAlt), m_bShift(bShift), m_bCtrl(bCtrl) {}*/ // BtS - disabled by K-mod

void CvNetPushOrder::Debug(char* szAddendum)
{
	sprintf(szAddendum, "Pushing an order at the city, order is %d, data is %d", m_eOrder, m_iData);
}

void CvNetPushOrder::Execute()
{
	if (m_ePlayer != NO_PLAYER)
	{
		CvCity* pCity = GET_PLAYER(m_ePlayer).getCity(m_iCityID);
		if (pCity != NULL)
		{
			//pCity->pushOrder(m_eOrder, m_iData, -1, m_bAlt, !(m_bShift || m_bCtrl), m_bShift);
			pCity->pushOrder(m_eOrder, m_iData, -1, m_bSave, m_bPop, m_iPosition); // K-Mod
			// K-Mod. We don't want automated cities to overrule our production choice.
			if (pCity->isHuman())
				pCity->setChooseProductionDirty(false);
			// K-Mod end
		}

		if (GC.getGame().getActivePlayer() == m_ePlayer)
			gDLL->UI().updatePythonScreens();
	}
}

void CvNetPushOrder::PutInBuffer(FDataStreamBase* pStream)
{
	pStream->Write(m_ePlayer);
	pStream->Write(m_iCityID);
	pStream->Write(m_eOrder);
	pStream->Write(m_iData);
	/* pStream->Write(m_bAlt);
	pStream->Write(m_bShift);
	pStream->Write(m_bCtrl); */
	// K-Mod
	pStream->Write(m_bSave);
	pStream->Write(m_bPop);
	pStream->Write(m_iPosition);
	// K-Mod end
}

void CvNetPushOrder::SetFromBuffer(FDataStreamBase* pStream)
{
	pStream->Read((int*)&m_ePlayer);
	pStream->Read(&m_iCityID);
	pStream->Read((int*)&m_eOrder);
	pStream->Read(&m_iData);
	/* pStream->Read(&m_bAlt);
	pStream->Read(&m_bShift);
	pStream->Read(&m_bCtrl); */
	// K-Mod
	pStream->Read(&m_bSave);
	pStream->Read(&m_bPop);
	pStream->Read(&m_iPosition);
	// K-Mod end
}

CvNetPopOrder::CvNetPopOrder() :
	CvMessageData(GAMEMESSAGE_POP_ORDER),
	m_ePlayer(NO_PLAYER),
	m_iCityID(-1),
	m_iNum(0)
{
}

CvNetPopOrder::CvNetPopOrder(PlayerTypes ePlayer, int iCityID, int iNum) :
	CvMessageData(GAMEMESSAGE_POP_ORDER),
	m_ePlayer(ePlayer),
	m_iCityID(iCityID),
	m_iNum(iNum)
{
}

void CvNetPopOrder::Debug(char* szAddendum)
{
	sprintf(szAddendum, "Pop Order at City, city ID is %d", m_iCityID);
}

void CvNetPopOrder::Execute()
{
	if (m_ePlayer != NO_PLAYER)
	{
		CvCity* pCity = GET_PLAYER(m_ePlayer).getCity(m_iCityID);
		if (pCity != NULL)
			pCity->popOrder(m_iNum);
		if (GC.getGame().getActivePlayer() == m_ePlayer)
			gDLL->UI().updatePythonScreens();
	}
}

void CvNetPopOrder::PutInBuffer(FDataStreamBase* pStream)
{
	pStream->Write(m_ePlayer);
	pStream->Write(m_iCityID);
	pStream->Write(m_iNum);
}

void CvNetPopOrder::SetFromBuffer(FDataStreamBase* pStream)
{
	pStream->Read((int*)&m_ePlayer);
	pStream->Read(&m_iCityID);
	pStream->Read(&m_iNum);
}

CvNetDoTask::CvNetDoTask() :
	CvMessageData(GAMEMESSAGE_DO_TASK),
	m_ePlayer(NO_PLAYER),
	m_iCityID(-1),
	m_eTask(NO_TASK),
	m_iData1(-1), m_iData2(-1), m_bOption(false),
	m_bAlt(false), m_bShift(false), m_bCtrl(false)
{
}

CvNetDoTask::CvNetDoTask(PlayerTypes ePlayer, int iCityID, TaskTypes eTask,
	int iData1, int iData2, bool bOption, bool bAlt, bool bShift, bool bCtrl) :
	CvMessageData(GAMEMESSAGE_DO_TASK),
	m_ePlayer(ePlayer),
	m_iCityID(iCityID),
	m_eTask(eTask),
	m_iData1(iData1), m_iData2(iData2), m_bOption(bOption),
	m_bAlt(bAlt), m_bShift(bShift), m_bCtrl(bCtrl)
{
}

void CvNetDoTask::Debug(char* szAddendum)
{
	sprintf(szAddendum, "Do Task at City, city ID is %d", m_iCityID);
}

void CvNetDoTask::Execute()
{
	if (m_ePlayer != NO_PLAYER)
	{
		CvCity* pCity = GET_PLAYER(m_ePlayer).getCity(m_iCityID);
		if (pCity != NULL)
		{
			pCity->doTask(m_eTask, m_iData1, m_iData2,
					m_bOption, m_bAlt, m_bShift, m_bCtrl);
		}
	}
}

void CvNetDoTask::PutInBuffer(FDataStreamBase* pStream)
{
	pStream->Write(m_ePlayer);
	pStream->Write(m_iCityID);
	pStream->Write(m_eTask);
	pStream->Write(m_iData1);
	pStream->Write(m_iData2);
	pStream->Write(m_bOption);
	pStream->Write(m_bAlt);
	pStream->Write(m_bShift);
	pStream->Write(m_bCtrl);
}

void CvNetDoTask::SetFromBuffer(FDataStreamBase* pStream)
{
	pStream->Read((int*)&m_ePlayer);
	pStream->Read(&m_iCityID);
	pStream->Read((int*)&m_eTask);
	pStream->Read(&m_iData1);
	pStream->Read(&m_iData2);
	pStream->Read(&m_bOption);
	pStream->Read(&m_bAlt);
	pStream->Read(&m_bShift);
	pStream->Read(&m_bCtrl);
}

CvNetUpdateCivics::CvNetUpdateCivics() :
	CvMessageData(GAMEMESSAGE_UPDATE_CIVICS),
	m_ePlayer(NO_PLAYER)
{
}

CvNetUpdateCivics::CvNetUpdateCivics(PlayerTypes ePlayer, CivicMap const& kCivics) :
	CvMessageData(GAMEMESSAGE_UPDATE_CIVICS), m_ePlayer(ePlayer)
{
	// <advc.enum>
	FOR_EACH_ENUM(CivicOption)
		m_aeCivics.set(eLoopCivicOption, kCivics.get(eLoopCivicOption));
	// </advc.enum>
}


void CvNetUpdateCivics::Debug(char* szAddendum)
{
	sprintf(szAddendum, "Update Civics, ePlayer is %d", (int)m_ePlayer);
}

void CvNetUpdateCivics::Execute()
{
	if (m_ePlayer != NO_PLAYER /*&& !m_aeCivics.empty()*/) // advc.enum
	{
		GET_PLAYER(m_ePlayer).revolution(m_aeCivics);
	}
}

void CvNetUpdateCivics::PutInBuffer(FDataStreamBase* pStream)
{
	pStream->Write(m_ePlayer);
	m_aeCivics.write(pStream);
}

void CvNetUpdateCivics::SetFromBuffer(FDataStreamBase* pStream)
{
	pStream->Read((int*)&m_ePlayer);
	m_aeCivics.read(pStream);
}

CvNetResearch::CvNetResearch() :
	CvMessageData(GAMEMESSAGE_RESEARCH),
	m_ePlayer(NO_PLAYER),
	m_iDiscover(-1),
	m_bShift(false),
	m_eTech(NO_TECH)
{
}

CvNetResearch::CvNetResearch(PlayerTypes ePlayer, TechTypes eTech,
	int iDiscover, bool bShift) :
	CvMessageData(GAMEMESSAGE_RESEARCH),
	m_ePlayer(ePlayer),
	m_iDiscover(iDiscover),
	m_bShift(bShift),
	m_eTech(eTech)
{
}

void CvNetResearch::Debug(char* szAddendum)
{
	sprintf(szAddendum, "Research, %d",	m_eTech);
}

void CvNetResearch::Execute()
{
	if (m_ePlayer != NO_PLAYER)
	{
		CvPlayer& kPlayer = GET_PLAYER(m_ePlayer);
		if (m_iDiscover > 0)
		{
			kPlayer.setFreeTechChosen(m_eTech); // doc

			GET_TEAM(kPlayer.getTeam()).setHasTech(m_eTech, true, m_ePlayer, true, true);
			if (m_iDiscover > 1)
			{
				if (m_ePlayer == GC.getGame().getActivePlayer())
					kPlayer.chooseTech(m_iDiscover - 1);
			}
		}
		else
		{
			if (m_eTech == NO_TECH)
				kPlayer.clearResearchQueue();
			else if (kPlayer.canEverResearch(m_eTech))
			{
				if ((GET_TEAM(kPlayer.getTeam()).isHasTech(m_eTech) ||
					kPlayer.isResearchingTech(m_eTech)) && !m_bShift)
				{
					kPlayer.clearResearchQueue();
				}
				kPlayer.pushResearch(m_eTech, !m_bShift);
			}
		}
		if (GC.getGame().getActivePlayer() == m_ePlayer)
			gDLL->UI().updatePythonScreens();
	}
}

void CvNetResearch::PutInBuffer(FDataStreamBase* pStream)
{
	pStream->Write(m_ePlayer);
	pStream->Write(m_iDiscover);
	pStream->Write(m_bShift);
	pStream->Write(m_eTech);
}

void CvNetResearch::SetFromBuffer(FDataStreamBase* pStream)
{
	pStream->Read((int*)&m_ePlayer);
	pStream->Read(&m_iDiscover);
	pStream->Read(&m_bShift);
	pStream->Read((int*)&m_eTech);
}

CvNetEspionageChange::CvNetEspionageChange() :
	CvMessageData(GAMEMESSAGE_ESPIONAGE_CHANGE),
	m_ePlayer(NO_PLAYER),
	m_eTargetTeam(NO_TEAM),
	m_iChange(0)
{
}

CvNetEspionageChange::CvNetEspionageChange(PlayerTypes ePlayer,
	TeamTypes eTargetTeam, int iChange) :
	CvMessageData(GAMEMESSAGE_ESPIONAGE_CHANGE),
	m_ePlayer(ePlayer),
	m_eTargetTeam(eTargetTeam),
	m_iChange(iChange)
{
}

void CvNetEspionageChange::Debug(char* szAddendum)
{
	sprintf(szAddendum, "TargetTeam: %d, Espionage Change: %d", m_eTargetTeam, m_iChange);
}

void CvNetEspionageChange::Execute()
{
	if (m_ePlayer != NO_PLAYER)
	{
		GET_PLAYER(m_ePlayer).changeEspionageSpendingWeightAgainstTeam(
				m_eTargetTeam, m_iChange);
	}
}

void CvNetEspionageChange::PutInBuffer(FDataStreamBase* pStream)
{
	pStream->Write(m_ePlayer);
	pStream->Write(m_eTargetTeam);
	pStream->Write(m_iChange);
}

void CvNetEspionageChange::SetFromBuffer(FDataStreamBase* pStream)
{
	pStream->Read((int*)&m_ePlayer);
	pStream->Read((int*)&m_eTargetTeam);
	pStream->Read(&m_iChange);
}

CvNetAdvancedStartAction::CvNetAdvancedStartAction(AdvancedStartActionTypes eAction,
	PlayerTypes ePlayer, int iX, int iY, int iData, bool bAdd) :
	CvMessageData(GAMEMESSAGE_ADVANCED_START_ACTION),
	m_eAction(eAction),
	m_ePlayer(ePlayer),
	m_iX(iX),
	m_iY(iY),
	m_iData(iData),
	m_bAdd(bAdd)
{
}

void CvNetAdvancedStartAction::Debug(char* szAddendum)
{
	sprintf(szAddendum, "Non-simultaneous Advanced Start Action notification");
}

void CvNetAdvancedStartAction::Execute()
{
	if (m_ePlayer != NO_PLAYER && !gDLL->UI().isExitingToMainMenu())
		GET_PLAYER(m_ePlayer).doAdvancedStartAction(m_eAction, m_iX, m_iY, m_iData, m_bAdd);
}

void CvNetAdvancedStartAction::PutInBuffer(FDataStreamBase* pStream)
{
	pStream->Write(m_eAction);
	pStream->Write(m_ePlayer);
	pStream->Write(m_iX);
	pStream->Write(m_iY);
	pStream->Write(m_iData);
	pStream->Write(m_bAdd);
}

void CvNetAdvancedStartAction::SetFromBuffer(FDataStreamBase* pStream)
{
	pStream->Read((int*)&m_eAction);
	pStream->Read((int*)&m_ePlayer);
	pStream->Read(&m_iX);
	pStream->Read(&m_iY);
	pStream->Read(&m_iData);
	pStream->Read(&m_bAdd);
}

CvNetModNetMessage::CvNetModNetMessage(int iData1, int iData2, int iData3,
	int iData4, int iData5) :
	CvMessageData(GAMEMESSAGE_MOD_NET_MESSAGE),
	m_iData1(iData1), m_iData2(iData2), m_iData3(iData3), m_iData4(iData4), m_iData5(iData5)
{
}

void CvNetModNetMessage::Debug(char* szAddendum)
{
	sprintf(szAddendum, "Non-simultaneous ModNetMessage notification");
}

void CvNetModNetMessage::Execute()
{
	CvEventReporter::getInstance().reportModNetMessage(
			m_iData1, m_iData2, m_iData3, m_iData4, m_iData5);
}

void CvNetModNetMessage::PutInBuffer(FDataStreamBase* pStream)
{
	pStream->Write(m_iData1);
	pStream->Write(m_iData2);
	pStream->Write(m_iData3);
	pStream->Write(m_iData4);
	pStream->Write(m_iData5);
}

void CvNetModNetMessage::SetFromBuffer(FDataStreamBase* pStream)
{
	pStream->Read(&m_iData1);
	pStream->Read(&m_iData2);
	pStream->Read(&m_iData3);
	pStream->Read(&m_iData4);
	pStream->Read(&m_iData5);
}

CvNetConvert::CvNetConvert(PlayerTypes ePlayer, ReligionTypes eReligion) :
	CvMessageData(GAMEMESSAGE_CONVERT), m_ePlayer(ePlayer), m_eReligion(eReligion)
{
}

void CvNetConvert::Debug(char* szAddendum)
{
	sprintf(szAddendum, "Religion: %d", m_eReligion);
}

void CvNetConvert::Execute()
{
	if (m_ePlayer != NO_PLAYER)
	{
		GET_PLAYER(m_ePlayer).convert(m_eReligion);
	}
}

void CvNetConvert::PutInBuffer(FDataStreamBase* pStream)
{
	pStream->Write(m_ePlayer);
	pStream->Write(m_eReligion);
}

void CvNetConvert::SetFromBuffer(FDataStreamBase* pStream)
{
	pStream->Read((int*)&m_ePlayer);
	pStream->Read((int*)&m_eReligion);
}

CvNetEmpireSplit::CvNetEmpireSplit(PlayerTypes ePlayer, int iPlayerID) :
    CvMessageData(GAMEMESSAGE_EMPIRE_SPLIT),
	m_ePlayer(ePlayer),
	m_iPlayerID(iPlayerID)
{
}

void CvNetEmpireSplit::Debug(char* szAddendum)
{
	sprintf(szAddendum, "Non-simultaneous empire split notification");
}

void CvNetEmpireSplit::Execute()
{
	if (m_ePlayer != NO_PLAYER)
	{
		GET_PLAYER(m_ePlayer).splitEmpire((CivilizationTypes)m_iPlayerID);
	}
}

void CvNetEmpireSplit::PutInBuffer(FDataStreamBase* pStream)
{
	pStream->Write(m_ePlayer);
	pStream->Write(m_iPlayerID);
}

void CvNetEmpireSplit::SetFromBuffer(FDataStreamBase* pStream)
{
	pStream->Read((int*)&m_ePlayer);
	pStream->Read(&m_iPlayerID);
}

CvNetFoundReligion::CvNetFoundReligion(PlayerTypes ePlayer, ReligionTypes eReligion,
	ReligionTypes eSlotReligion) :
	CvMessageData(GAMEMESSAGE_FOUND_RELIGION),
	m_ePlayer(ePlayer),
	m_eReligion(eReligion),
	m_eSlotReligion(eSlotReligion)
{
}

void CvNetFoundReligion::Debug(char* szAddendum)
{
	sprintf(szAddendum, "Non-simultaneous found religion notification");
}

void CvNetFoundReligion::Execute()
{
	if (m_ePlayer != NO_PLAYER)
	{
		GET_PLAYER(m_ePlayer).foundReligion(m_eReligion, m_eSlotReligion, true);
	}
}

void CvNetFoundReligion::PutInBuffer(FDataStreamBase* pStream)
{
	pStream->Write(m_ePlayer);
	pStream->Write(m_eReligion);
	pStream->Write(m_eSlotReligion);
}

void CvNetFoundReligion::SetFromBuffer(FDataStreamBase* pStream)
{
	pStream->Read((int*)&m_ePlayer);
	pStream->Read((int*)&m_eReligion);
	pStream->Read((int*)&m_eSlotReligion);
}

CvNetLaunchSpaceship::CvNetLaunchSpaceship(PlayerTypes ePlayer, VictoryTypes eVictory) :
	CvMessageData(GAMEMESSAGE_LAUNCH_SPACESHIP),
	m_ePlayer(ePlayer),
	m_eVictory(eVictory)
{
}

void CvNetLaunchSpaceship::Debug(char* szAddendum)
{
	sprintf(szAddendum, "Non-simultaneous spaceship launch notification");
}

void CvNetLaunchSpaceship::Execute()
{
	if (m_ePlayer != NO_PLAYER)
	{
		GET_PLAYER(m_ePlayer).launch(m_eVictory);
	}
}

void CvNetLaunchSpaceship::PutInBuffer(FDataStreamBase* pStream)
{
	pStream->Write(m_ePlayer);
	pStream->Write(m_eVictory);
}

void CvNetLaunchSpaceship::SetFromBuffer(FDataStreamBase* pStream)
{
	pStream->Read((int*)&m_ePlayer);
	pStream->Read((int*)&m_eVictory);
}

CvNetEventTriggered::CvNetEventTriggered(PlayerTypes ePlayer, EventTypes eEvent,
	int iEventTriggeredId) :
	CvMessageData(GAMEMESSAGE_EVENT_TRIGGERED),
	m_ePlayer(ePlayer), m_eEvent(eEvent),
	m_iEventTriggeredId(iEventTriggeredId)
{
}

void CvNetEventTriggered::Debug(char* szAddendum)
{
	sprintf(szAddendum, "Non-simultaneous event trigger notification");
}

void CvNetEventTriggered::Execute()
{
	if (m_ePlayer != NO_PLAYER)
	{
		GET_PLAYER(m_ePlayer).applyEvent(m_eEvent, m_iEventTriggeredId);
	}
}

void CvNetEventTriggered::PutInBuffer(FDataStreamBase* pStream)
{
	pStream->Write(m_ePlayer);
	pStream->Write(m_eEvent);
	pStream->Write(m_iEventTriggeredId);
}

void CvNetEventTriggered::SetFromBuffer(FDataStreamBase* pStream)
{
	pStream->Read((int*)&m_ePlayer);
	pStream->Read((int*)&m_eEvent);
	pStream->Read((int*)&m_iEventTriggeredId);
}

CvNetJoinGroup::CvNetJoinGroup() :
	CvMessageData(GAMEMESSAGE_JOIN_GROUP), m_ePlayer(NO_PLAYER), m_iUnitID(-1), m_iHeadID(-1)
{
}

CvNetJoinGroup::CvNetJoinGroup(PlayerTypes ePlayer, int iUnitID, int iHeadID) :
	CvMessageData(GAMEMESSAGE_JOIN_GROUP), m_ePlayer(ePlayer), m_iUnitID(iUnitID), m_iHeadID(iHeadID)
{
}

void CvNetJoinGroup::Debug(char* szAddendum)
{
	sprintf(szAddendum, "Join Group unit %d -> head unit %d", m_iUnitID, m_iHeadID);
}

void CvNetJoinGroup::Execute()
{
	if (m_ePlayer != NO_PLAYER)
	{
		CvUnit* pUnit = GET_PLAYER(m_ePlayer).getUnit(m_iUnitID);
		if (pUnit != NULL)
		{
			CvUnit* pHeadUnit = GET_PLAYER(m_ePlayer).getUnit(m_iHeadID);
			if (pHeadUnit != NULL)
			{
				pUnit->joinGroup(pHeadUnit->getGroup());
			}
			else
			{
				pUnit->joinGroup(NULL);
			}
		}
	}
}

void CvNetJoinGroup::PutInBuffer(FDataStreamBase* pStream)
{
	pStream->Write(m_ePlayer);
	pStream->Write(m_iUnitID);
	pStream->Write(m_iHeadID);
}

void CvNetJoinGroup::SetFromBuffer(FDataStreamBase* pStream)
{
	pStream->Read((int*)&m_ePlayer);
	pStream->Read(&m_iUnitID);
	pStream->Read(&m_iHeadID);
}

CvNetPushMission::CvNetPushMission() :
	CvMessageData(GAMEMESSAGE_PUSH_MISSION), m_ePlayer(NO_PLAYER), m_iUnitID(-1),
	m_eMission(NO_MISSION), m_iData1(-1), m_iData2(-1), m_eFlags(NO_MOVEMENT_FLAGS),
	m_bShift(false),
	m_bModified(false) // advc.011b
{}

CvNetPushMission::CvNetPushMission(PlayerTypes ePlayer, int iUnitID,
	MissionTypes eMission, int iData1, int iData2, MovementFlags eFlags,
	bool bShift,
	bool bModified) // advc.011b
:	CvMessageData(GAMEMESSAGE_PUSH_MISSION), m_ePlayer(ePlayer), m_iUnitID(iUnitID),
	m_eMission(eMission), m_iData1(iData1), m_iData2(iData2), m_eFlags(eFlags),
	m_bShift(bShift),
	m_bModified(bModified) // advc.011b
{}

void CvNetPushMission::Debug(char* szAddendum)
{
	sprintf(szAddendum, "Do Mission, who is %d, unit ID is %d, mission is %S", m_ePlayer, m_iUnitID, GC.getInfo(m_eMission).getDescription());
}

void CvNetPushMission::Execute()
{
	if (m_ePlayer != NO_PLAYER)
	{
		CvUnit* pUnit = GET_PLAYER(m_ePlayer).getUnit(m_iUnitID);
		if (pUnit != NULL)
		{
			CvSelectionGroup* pSelectionGroup = pUnit->getGroup();
			if (pSelectionGroup != NULL)
			{
				pSelectionGroup->pushMission(m_eMission, m_iData1, m_iData2,
						m_eFlags, m_bShift, true,
						NO_MISSIONAI, NULL, NULL, m_bModified); // advc.011b
			}
		}
	}
}

void CvNetPushMission::PutInBuffer(FDataStreamBase* pStream)
{
	pStream->Write(m_ePlayer);
	pStream->Write(m_iUnitID);
	pStream->Write(m_eMission);
	pStream->Write(m_iData1);
	pStream->Write(m_iData2);
	pStream->Write(m_eFlags);
	pStream->Write(m_bShift);
	pStream->Write(m_bModified); // advc.011b
}

void CvNetPushMission::SetFromBuffer(FDataStreamBase* pStream)
{
	pStream->Read((int*)&m_ePlayer);
	pStream->Read(&m_iUnitID);
	pStream->Read((int*)&m_eMission);
	pStream->Read(&m_iData1);
	pStream->Read(&m_iData2);
	pStream->Read((int*)&m_eFlags);
	pStream->Read(&m_bShift);
	pStream->Read(&m_bModified); // advc.011b
}

CvNetAutoMission::CvNetAutoMission() :
	CvMessageData(GAMEMESSAGE_AUTO_MISSION), m_ePlayer(NO_PLAYER), m_iUnitID(-1)
{
}

CvNetAutoMission::CvNetAutoMission(PlayerTypes ePlayer, int iUnitID) :
	CvMessageData(GAMEMESSAGE_AUTO_MISSION), m_ePlayer(ePlayer), m_iUnitID(iUnitID)
{
}

void CvNetAutoMission::Debug(char* szAddendum)
{
	sprintf(szAddendum, "Auto Mission, unit ID is %d",	m_iUnitID);
}

void CvNetAutoMission::Execute()
{
	if (m_ePlayer != NO_PLAYER)
	{
		CvUnit* pUnit = GET_PLAYER(m_ePlayer).getUnit(m_iUnitID);
		if (pUnit != NULL)
		{
			CvSelectionGroup* pSelectionGroup = pUnit->getGroup();
			if (pSelectionGroup != NULL)
			{
				pSelectionGroup->autoMission();
			}
		}
	}
}

void CvNetAutoMission::PutInBuffer(FDataStreamBase* pStream)
{
	pStream->Write(m_ePlayer);
	pStream->Write(m_iUnitID);
}

void CvNetAutoMission::SetFromBuffer(FDataStreamBase* pStream)
{
	pStream->Read((int*)&m_ePlayer);
	pStream->Read(&m_iUnitID);
}

CvNetDoCommand::CvNetDoCommand() :
	CvMessageData(GAMEMESSAGE_DO_COMMAND),
	m_ePlayer(NO_PLAYER),
	m_iUnitID(-1),
	m_eCommand(NO_COMMAND),
	m_iData1(-1), m_iData2(-1),
	m_bAlt(false)
{
}

CvNetDoCommand::CvNetDoCommand(PlayerTypes ePlayer, int iUnitID,
	CommandTypes eCommand, int iData1, int iData2, bool bAlt) :
	CvMessageData(GAMEMESSAGE_DO_COMMAND),
	m_ePlayer(ePlayer),
	m_iUnitID(iUnitID),
	m_eCommand(eCommand),
	m_iData1(iData1), m_iData2(iData2),
	m_bAlt(bAlt)
{
}

void CvNetDoCommand::Debug(char* szAddendum)
{
	sprintf(szAddendum, "Do Command, who is %d, unit ID is %d, command is %d", m_ePlayer, m_iUnitID, m_eCommand);
}

void CvNetDoCommand::Execute()
{
	if (m_ePlayer != NO_PLAYER)
	{
		CvUnit* pUnit = GET_PLAYER(m_ePlayer).getUnit(m_iUnitID);
		if (pUnit != NULL)
		{
			if (m_bAlt && GC.getInfo(m_eCommand).getAll())
			{
				/*FOR_EACH_UNIT_VAR(pLoopUnit, GET_PLAYER(m_ePlayer)) // BtS
					if (pLoopUnit->getUnitType() == pUnit->getUnitType())*/
				/*  UNOFFICIAL_PATCH, Bugfix, 07/08/09, jdog5000: START
					Have to save type ahead of time, pointer can change */
				UnitTypes eUpgradeType = pUnit->getUnitType();
				FOR_EACH_UNIT_VAR(pLoopUnit, GET_PLAYER(m_ePlayer))
				{
					if (pLoopUnit->getUnitType() == eUpgradeType)
					// UNOFFICIAL_PATCH: END
					{
						pLoopUnit->doCommand(m_eCommand, m_iData1, m_iData2);
					}
				}
			}
			else
			{
				pUnit->doCommand(m_eCommand, m_iData1, m_iData2);
			}
		}
	}
}

void CvNetDoCommand::PutInBuffer(FDataStreamBase* pStream)
{
	pStream->Write(m_ePlayer);
	pStream->Write(m_iUnitID);
	pStream->Write(m_eCommand);
	pStream->Write(m_iData1);
	pStream->Write(m_iData2);
	pStream->Write(m_bAlt);
}

void CvNetDoCommand::SetFromBuffer(FDataStreamBase* pStream)
{
	pStream->Read((int*)&m_ePlayer);
	pStream->Read(&m_iUnitID);
	pStream->Read((int*)&m_eCommand);
	pStream->Read(&m_iData1);
	pStream->Read(&m_iData2);
	pStream->Read(&m_bAlt);
}

CvNetPercentChange::CvNetPercentChange() :
	CvMessageData(GAMEMESSAGE_PERCENT_CHANGE),
	m_ePlayer(NO_PLAYER),
	m_iChange(0),
	m_eCommerce(NO_COMMERCE)
{
}

CvNetPercentChange::CvNetPercentChange(PlayerTypes ePlayer,
	CommerceTypes eCommerce, int iChange) :
	CvMessageData(GAMEMESSAGE_PERCENT_CHANGE),
	m_ePlayer(ePlayer),
	m_iChange(iChange),
	m_eCommerce(eCommerce)
{
}

void CvNetPercentChange::Debug(char* szAddendum)
{
	sprintf(szAddendum, "Commerce: %d, Percent Change: %d", m_eCommerce, m_iChange);
}

void CvNetPercentChange::Execute()
{
	if (m_ePlayer != NO_PLAYER)
	{
		GET_PLAYER(m_ePlayer).changeCommercePercent(m_eCommerce, m_iChange);
	}
}

void CvNetPercentChange::PutInBuffer(FDataStreamBase* pStream)
{
	pStream->Write(m_ePlayer);
	pStream->Write(m_iChange);
	pStream->Write(m_eCommerce);
}

void CvNetPercentChange::SetFromBuffer(FDataStreamBase* pStream)
{
	pStream->Read((int*)&m_ePlayer);
	pStream->Read(&m_iChange);
	pStream->Read((int*)&m_eCommerce);
}

CvNetChangeVassal::CvNetChangeVassal() :
	CvMessageData(GAMEMESSAGE_CHANGE_VASSAL),
	m_ePlayer(NO_PLAYER),
	m_eMasterTeam(NO_TEAM),
	m_bVassal(false),
	m_bCapitulated(false)
{
}

CvNetChangeVassal::CvNetChangeVassal(PlayerTypes ePlayer, TeamTypes eMasterTeam,
	bool bVassal, bool bCapitulated) :
	CvMessageData(GAMEMESSAGE_CHANGE_VASSAL),
	m_ePlayer(ePlayer),
	m_eMasterTeam(eMasterTeam),
	m_bVassal(bVassal),
	m_bCapitulated(bCapitulated)
{
}

void CvNetChangeVassal::Debug(char* szAddendum)
{
	sprintf(szAddendum, "Change Vassal, master team is %d", m_eMasterTeam);
}

void CvNetChangeVassal::Execute()
{
	if (m_ePlayer != NO_PLAYER)
	{
		FAssert(TEAMID(m_ePlayer) != m_eMasterTeam);
		GET_TEAM(m_ePlayer).setVassal(m_eMasterTeam, m_bVassal, m_bCapitulated);
	}
}

void CvNetChangeVassal::PutInBuffer(FDataStreamBase* pStream)
{
	pStream->Write(m_ePlayer);
	pStream->Write(m_eMasterTeam);
	pStream->Write(m_bVassal);
	pStream->Write(m_bCapitulated);
}

void CvNetChangeVassal::SetFromBuffer(FDataStreamBase* pStream)
{
	pStream->Read((int*)&m_ePlayer);
	pStream->Read((int*)&m_eMasterTeam);
	pStream->Read(&m_bVassal);
	pStream->Read(&m_bCapitulated);
}

CvNetChooseElection::CvNetChooseElection() :
	CvMessageData(GAMEMESSAGE_CHOOSE_ELECTION),
	m_ePlayer(NO_PLAYER),
	m_iSelection(-1),
	m_iVoteId(-1)
{
}

CvNetChooseElection::CvNetChooseElection(PlayerTypes ePlayer, int iSelection, int iVoteId) :
	CvMessageData(GAMEMESSAGE_CHOOSE_ELECTION),
	m_ePlayer(ePlayer),
	m_iSelection(iSelection),
	m_iVoteId(iVoteId)
{
}

void CvNetChooseElection::Debug(char* szAddendum)
{
	sprintf(szAddendum, "Choose Election: %d", m_iSelection);
}

void CvNetChooseElection::Execute()
{
	GC.getGame().setVoteChosen(m_iSelection, m_iVoteId);
}

void CvNetChooseElection::PutInBuffer(FDataStreamBase* pStream)
{
	pStream->Write(m_ePlayer);
	pStream->Write(m_iSelection);
	pStream->Write(m_iVoteId);
}

void CvNetChooseElection::SetFromBuffer(FDataStreamBase* pStream)
{
	pStream->Read((int*)&m_ePlayer);
	pStream->Read(&m_iSelection);
	pStream->Read(&m_iVoteId);
}

CvNetDiploVote::CvNetDiploVote() :
	CvMessageData(GAMEMESSAGE_DIPLO_VOTE),
	m_ePlayer(NO_PLAYER),
	m_iVoteId(-1),
	m_eChoice(NO_PLAYER_VOTE)
{
}

CvNetDiploVote::CvNetDiploVote(PlayerTypes ePlayer, int iVoteId, PlayerVoteTypes eChoice) :
	CvMessageData(GAMEMESSAGE_DIPLO_VOTE),
	m_ePlayer(ePlayer),
	m_iVoteId(iVoteId),
	m_eChoice(eChoice)
{
}

void CvNetDiploVote::Debug(char* szAddendum)
{
	sprintf(szAddendum, "Diplo Vote for %d; Choice is %d", m_iVoteId, m_eChoice);
}

void CvNetDiploVote::Execute()
{
	GC.getGame().castVote(m_ePlayer, m_iVoteId, m_eChoice);
}

void CvNetDiploVote::PutInBuffer(FDataStreamBase* pStream)
{
	pStream->Write(m_ePlayer);
	pStream->Write(m_iVoteId);
	pStream->Write(m_eChoice);
}

void CvNetDiploVote::SetFromBuffer(FDataStreamBase* pStream)
{
	pStream->Read((int*)&m_ePlayer);
	pStream->Read(&m_iVoteId);
	pStream->Read((int*)&m_eChoice);
}

CvNetChangeWar::CvNetChangeWar() :
	CvMessageData(GAMEMESSAGE_CHANGE_WAR),
	m_ePlayer(NO_PLAYER),
	m_eRivalTeam(NO_TEAM),
	m_bWar(false)
{
}

CvNetChangeWar::CvNetChangeWar(PlayerTypes ePlayer, TeamTypes eRivalTeam, bool bWar) :
	CvMessageData(GAMEMESSAGE_CHANGE_WAR),
	m_ePlayer(ePlayer),
	m_eRivalTeam(eRivalTeam),
	m_bWar(bWar)
{
}

void CvNetChangeWar::Debug(char* szAddendum)
{
	sprintf(szAddendum, "Change War, rival team is %d", m_eRivalTeam);
}

void CvNetChangeWar::Execute()
{
	if (m_ePlayer != NO_PLAYER)
	{
		FAssert(GET_PLAYER(m_ePlayer).getTeam() != m_eRivalTeam);
		if (m_bWar)
		{
			GET_TEAM(m_ePlayer).declareWar(m_eRivalTeam, false, NO_WARPLAN);
			if (gDLL->isDiplomacy() &&
				TEAMID((PlayerTypes)gDLL->getDiplomacyPlayer()) == m_eRivalTeam)
			{
				gDLL->endDiplomacy();
			}
		}
		else GET_TEAM(m_ePlayer).makePeace(m_eRivalTeam);
	}
}

void CvNetChangeWar::PutInBuffer(FDataStreamBase* pStream)
{
	pStream->Write(m_ePlayer);
	pStream->Write(m_eRivalTeam);
	pStream->Write(m_bWar);
}

void CvNetChangeWar::SetFromBuffer(FDataStreamBase* pStream)
{
	pStream->Read((int*)&m_ePlayer);
	pStream->Read((int*)&m_eRivalTeam);
	pStream->Read(&m_bWar);
}

CvNetPing::CvNetPing(PlayerTypes ePlayer, int iX, int iY) :
	CvMessageData(GAMEMESSAGE_PING),
	m_ePlayer(ePlayer),
	m_iX(iX), m_iY(iY)
{
}

void CvNetPing::Debug(char* szAddendum)
{
	sprintf(szAddendum, "Ping message received");
}

void CvNetPing::PutInBuffer(FDataStreamBase* pStream)
{
	pStream->Write(m_ePlayer);
	pStream->Write(m_iX);
	pStream->Write(m_iY);
}

void CvNetPing::SetFromBuffer(FDataStreamBase* pStream)
{
	pStream->Read((int*)&m_ePlayer);
	pStream->Read(&m_iX);
	pStream->Read(&m_iY);
}

void CvNetPing::Execute()
{
	TeamTypes const eActiveTeam = GC.getGame().getActiveTeam();
	if (eActiveTeam != NO_TEAM)
	{
		if (TEAMID(m_ePlayer) == eActiveTeam ||
			GET_TEAM(eActiveTeam).isVassal(TEAMID(m_ePlayer)) ||
			GET_TEAM(m_ePlayer).isVassal(eActiveTeam))
		{
			gDLL->UI().doPing(m_iX, m_iY, m_ePlayer);
		}
	}
}
// <advc.003g>
CvNetFPTest::CvNetFPTest(PlayerTypes ePlayer, int iResult) :
	CvMessageData(GAMEMESSAGE_FP_TEST),
	m_ePlayer(ePlayer),
	m_iResult(iResult)
{}

void CvNetFPTest::Debug(char* szAddendum)
{
	sprintf(szAddendum, "FPTest message received");
}

void CvNetFPTest::PutInBuffer(FDataStreamBase* pStream)
{
	pStream->Write(m_iResult);
	pStream->Write(m_ePlayer);
}

void CvNetFPTest::SetFromBuffer(FDataStreamBase* pStream)
{
	pStream->Read(&m_iResult);
	pStream->Read((int*)&m_ePlayer);
}

void CvNetFPTest::Execute()
{
	GC.getGame().doFPCheck(m_iResult, m_ePlayer);
} // </advc.003g>
// <advc.190c>
CvNetCivLeaderSetup::CvNetCivLeaderSetup(PlayerTypes ePlayer,
	CvInitCore const* pInitCore)
:	CvMessageData(GAMEMESSAGE_CIV_LEADER_SETUP),
	m_ePlayer(ePlayer)
{
	if (pInitCore == NULL)
		return;
	FOR_EACH_ENUM(Player)
	{
		m_abCivChosenRandomly.set(eLoopPlayer,
				pInitCore->wasCivRandomlyChosen(eLoopPlayer));
		m_abLeaderChosenRandomly.set(eLoopPlayer,
				pInitCore->wasLeaderRandomlyChosen(eLoopPlayer));
	}
}

void CvNetCivLeaderSetup::Debug(char* szAddendum)
{
	sprintf(szAddendum, "CivLeaderSetup message received");
}

void CvNetCivLeaderSetup::PutInBuffer(FDataStreamBase* pStream)
{
	m_abCivChosenRandomly.write(pStream);
	m_abLeaderChosenRandomly.write(pStream);
}

void CvNetCivLeaderSetup::SetFromBuffer(FDataStreamBase* pStream)
{
	m_abCivChosenRandomly.read(pStream);
	m_abLeaderChosenRandomly.read(pStream);
}

void CvNetCivLeaderSetup::Execute()
{
	FOR_EACH_ENUM(Player)
	{
		GC.getInitCore().setCivLeaderRandomlyChosen(eLoopPlayer,
				m_abCivChosenRandomly.get(eLoopPlayer),
				m_abLeaderChosenRandomly.get(eLoopPlayer));
	}
} // </advc.190c>
