#pragma once

#ifndef _CYMESSAGECONTROL_H
#define _CYMESSAGECONTROL_H

namespace python = boost::python;

class CyMessageControl
{
public:
	void sendPushOrder(int iCityID, int eOrder, int iData, bool bAlt, bool bShift, bool bCtrl); // K-Mod note: the arguments here no longer match CvMessageControl::sendPushOrder.  Sorry about that.
	void sendDoTask(int iCity, int eTask, int iData1, int iData2, bool bOption, bool bAlt, bool bShift, bool bCtrl);
	void sendTurnComplete();
	void sendUpdateCivics(boost::python::list& iCivics);
	void sendResearch(int eTech, bool bShift);
	void sendPlayerOption (int /*PlayerOptionTypes*/ eOption, bool bValue);
	void sendEspionageSpendingWeightChange (int /*TeamTypes*/ eTargetTeam, int iChange);
	void sendAdvancedStartAction	(int /*AdvancedStartActionTypes*/ eAction, int /*PlayerTypes*/ ePlayer, int iX, int iY, int iData, bool bAdd);
	void sendModNetMessage(int iData1, int iData2, int iData3, int iData4, int iData5);
	void sendConvert(int /*ReligionTypes*/ iReligion);
	void sendEmpireSplit(int /*PlayerTypes*/ ePlayer, int iAreaId);

	//	Helper function to determine the first bad connection...
	int GetFirstBadConnection();
	int GetConnState(int iPlayer);
};

#endif // _CYMESSAGECONTROL_H
