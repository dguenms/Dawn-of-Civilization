#pragma once

#ifndef CV_INFO_COMMAND_H
#define CV_INFO_COMMAND_H

/*  advc.003x: Cut from CvInfos.h. Info classes for dealing with unit commands:
	CvCommandInfo, CvAutomateInfo, CvActionInfo, CvMissionInfo,
	CvInterfaceModeInfo and CvControlInfo.
	Spy missions don't get attached to a unit or group; hence, CvEspionageMission
	is in CvInfo_Units.h. */

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvCommandInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvCommandInfo : public CvHotkeyInfo
{
	typedef CvHotkeyInfo base_t;
public:
	CvCommandInfo();

	int getAutomate() const;

	bool getConfirmCommand() const;
	bool getVisible() const;
	bool getAll() const;

	bool read(CvXMLLoadUtility* pXML);

protected:
	int m_iAutomate;
	bool m_bConfirmCommand;
	bool m_bVisible;
	bool m_bAll;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvAutomateInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvAutomateInfo : public CvHotkeyInfo
{
	typedef CvHotkeyInfo base_t;
public:
	CvAutomateInfo();

	int getCommand() const;
	int getAutomate() const;

	bool getConfirmCommand() const;
	bool getVisible() const;

	bool read(CvXMLLoadUtility* pXML);

protected:
	int m_iCommand;
	int m_iAutomate;
	bool m_bConfirmCommand;
	bool m_bVisible;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvActionInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// advc: Replaced if/else sequences with switch statements in the implementation of this class
class CvActionInfo :
	// advc.003e (Note that CvActionInfo is wrapped around CvHotkeyInfo rather than being derived from it)
	private boost::noncopyable
{
public:
	CvActionInfo();
	// advc.opt: virtual destructor deleted

	// functions to replace the CvInfoBase calls
	const TCHAR* getType() const;
	DllExport const wchar* getDescription() const;
	const wchar* getCivilopedia() const;
	DllExport const wchar* getHelp() const;
	const wchar* getStrategy() const;
	virtual const TCHAR* getButton() const;
	const wchar* getTextKeyWide() const;
	void reset() {} // advc.enum: for CvGlobals::infosReset

	// functions to replace the CvHotkey calls
	int getActionInfoIndex() const;
	DllExport int getHotKeyVal() const;
	DllExport int getHotKeyPriority() const;
	DllExport int getHotKeyValAlt() const;
	DllExport int getHotKeyPriorityAlt() const;
	int getOrderPriority() const;

	const TCHAR* getHotKey() const; // Exposed to Python
	std::wstring getHotKeyDescription() const; // Exposed to Python

	int getMissionData() const; // Exposed to Python
	int getCommandData() const; // Exposed to Python

	int getAutomateType() const; // (advc.004k: Exposed to Python)
	int getInterfaceModeType() const; // Exposed to Python
	DllExport int getMissionType() const; // Exposed to Python
	int getCommandType() const; // Exposed to Python
	int getControlType() const; // Exposed to Python
	/*	<advc> Renamed from "OriginalIndex". It's what the user is supposed to
		cast to the enum type indicated by getSubType. E.g. MISSION_SLEEP
		if this action represents the Sleep mission. */
	int getSubID() const;
	void setSubID(int i); // </advc>

	bool isConfirmCommand() const; // Exposed to Python
	DllExport bool isVisible() const; // Exposed to Python
	DllExport ActionSubTypes getSubType() const;
	void setSubType(ActionSubTypes eSubType);

	DllExport bool isAltDown() const;
	DllExport bool isShiftDown() const;
	DllExport bool isCtrlDown() const;
	DllExport bool isAltDownAlt() const;
	DllExport bool isShiftDownAlt() const;
	DllExport bool isCtrlDownAlt() const;

protected:
	int m_iSubID;
	ActionSubTypes m_eSubType;

private:
	CvHotkeyInfo* getHotkeyInfo() const;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvMissionInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvMissionInfo : public CvHotkeyInfo
{
	typedef CvHotkeyInfo base_t;
public: // The const functions are exposed to Python
	CvMissionInfo();

	DllExport int getTime() const;

	bool isSound() const;
	DllExport bool isTarget() const;
	bool isBuild() const;
	bool getVisible() const;
	DllExport EntityEventTypes getEntityEvent() const;

	const TCHAR* getWaypoint() const; // effect type, Exposed to Python

	bool read(CvXMLLoadUtility* pXML);

protected:
	int m_iTime;
	bool m_bSound;
	bool m_bTarget;
	bool m_bBuild;
	bool m_bVisible;
	EntityEventTypes m_eEntityEvent;
	CvString m_szWaypoint;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvInterfaceModeInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvInterfaceModeInfo : public CvHotkeyInfo
{
	typedef CvHotkeyInfo base_t;
public: // "(ADD to Python)" // <-- advc: Looks like all the const functions are exposed as usual
	CvInterfaceModeInfo();

	DllExport int getCursorIndex() const;
	DllExport int getMissionType() const;

	bool getVisible() const;
	DllExport bool getGotoPlot() const;
	bool getHighlightPlot() const;
	bool getSelectType() const;
	bool getSelectAll() const;

	bool read(CvXMLLoadUtility* pXML);

protected:
	int m_iCursorIndex;
	int m_iMissionType;

	bool m_bVisible;
	bool m_bGotoPlot;
	bool m_bHighlightPlot;
	bool m_bSelectType;
	bool m_bSelectAll;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvControlInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
/*  advc: This class doesn't quite fit here, but it's tiny and required for the
	implementation of CvActionInfo. */
class CvControlInfo : public CvHotkeyInfo {};

#endif
