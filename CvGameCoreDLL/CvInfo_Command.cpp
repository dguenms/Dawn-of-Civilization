// advc.003x: Cut from CvInfos.cpp

#include "CvGameCoreDLL.h"
#include "CvInfo_Command.h"
#include "CvXMLLoadUtility.h"
#include "CvInfo_City.h" // Needed by CvActionInfo


CvCommandInfo::CvCommandInfo() :
m_iAutomate(NO_AUTOMATE),
m_bConfirmCommand(false),
m_bVisible(false),
m_bAll(false)
{}

int CvCommandInfo::getAutomate() const
{
	return m_iAutomate;
}

bool CvCommandInfo::getConfirmCommand() const
{
	return m_bConfirmCommand;
}

bool CvCommandInfo::getVisible() const
{
	return m_bVisible;
}

bool CvCommandInfo::getAll() const
{
	return m_bAll;
}

bool CvCommandInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML))
		return false;

	CvString szTextVal;
	if (pXML->GetChildXmlValByName(szTextVal, "Automate", /* advc.006b: */ ""))
		m_iAutomate = GC.getTypesEnum(szTextVal);

	pXML->GetChildXmlValByName(&m_bConfirmCommand, "bConfirmCommand", /* advc.006b: */ false);
	pXML->GetChildXmlValByName(&m_bVisible, "bVisible", /* advc.006b: */ false);
	pXML->GetChildXmlValByName(&m_bAll, "bAll", /* advc.006b: */ false);

	return true;
}

CvAutomateInfo::CvAutomateInfo() :
m_iCommand(NO_COMMAND),
m_iAutomate(NO_AUTOMATE),
m_bConfirmCommand(false),
m_bVisible(false)
{}

int CvAutomateInfo::getCommand() const
{
	return m_iCommand;
}

int CvAutomateInfo::getAutomate() const
{
	return m_iAutomate;
}

bool CvAutomateInfo::getConfirmCommand() const
{
	return m_bConfirmCommand;
}

bool CvAutomateInfo::getVisible() const
{
	return m_bVisible;
}

bool CvAutomateInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML))
		return false;

	pXML->SetInfoIDFromChildXmlVal(m_iCommand, "Command");
	// (advc: Info class not yet loaded)
	pXML->SetGlobalTypeFromChildXmlVal(m_iAutomate, "Automate");

	pXML->GetChildXmlValByName(&m_bConfirmCommand, "bConfirmCommand", /* advc.006b: */ false);
	pXML->GetChildXmlValByName(&m_bVisible, "bVisible");

	return true;
}

CvActionInfo::CvActionInfo() :
m_iSubID(-1),
m_eSubType(NO_ACTIONSUBTYPE)
{}

int CvActionInfo::getMissionData() const
{
	if (ACTIONSUBTYPE_BUILD == m_eSubType ||
		ACTIONSUBTYPE_RELIGION == m_eSubType ||
		ACTIONSUBTYPE_CORPORATION == m_eSubType ||
		ACTIONSUBTYPE_SPECIALIST == m_eSubType	||
		ACTIONSUBTYPE_BUILDING == m_eSubType)
	{
		return m_iSubID;
	}
	return -1;
}

int CvActionInfo::getCommandData() const
{
	switch(getSubType())
	{
	case ACTIONSUBTYPE_PROMOTION:
	case ACTIONSUBTYPE_UNIT:
		return m_iSubID;
	case ACTIONSUBTYPE_COMMAND:
		return GC.getInfo((CommandTypes)m_iSubID).getAutomate();
	case ACTIONSUBTYPE_AUTOMATE:
		return GC.getInfo((AutomateTypes)m_iSubID).getAutomate();
	default:
		return -1;
	}
}

int CvActionInfo::getAutomateType() const
{
	switch(getSubType())
	{
	case ACTIONSUBTYPE_COMMAND:
		return GC.getInfo((CommandTypes)m_iSubID).getAutomate();
	case ACTIONSUBTYPE_AUTOMATE:
		return GC.getInfo((AutomateTypes)m_iSubID).getAutomate();
	default:
		return NO_AUTOMATE;
	}
}

int CvActionInfo::getInterfaceModeType() const
{
	if (ACTIONSUBTYPE_INTERFACEMODE == m_eSubType)
		return m_iSubID;

	return NO_INTERFACEMODE;
}

int CvActionInfo::getMissionType() const
{
	switch(getSubType())
	{
	case ACTIONSUBTYPE_BUILD:
		return (MissionTypes)GC.getInfo((BuildTypes)m_iSubID).getMissionType();
	case ACTIONSUBTYPE_RELIGION:
		return GC.getInfo((ReligionTypes)m_iSubID).getMissionType();
	case ACTIONSUBTYPE_CORPORATION:
		return GC.getInfo((CorporationTypes)m_iSubID).getMissionType();
	case ACTIONSUBTYPE_SPECIALIST:
		return (MissionTypes)GC.getInfo((SpecialistTypes)m_iSubID).getMissionType();
	case ACTIONSUBTYPE_BUILDING:
		return GC.getInfo((BuildingTypes)m_iSubID).getMissionType();
	case ACTIONSUBTYPE_MISSION:
		return (MissionTypes)m_iSubID;
	default:
		return NO_MISSION;
	}
}

int CvActionInfo::getCommandType() const
{
	switch(getSubType())
	{
	case ACTIONSUBTYPE_PROMOTION:
		return (CommandTypes)GC.getInfo((PromotionTypes)m_iSubID).getCommandType();
	case ACTIONSUBTYPE_UNIT:
		return (CommandTypes)GC.getInfo((UnitTypes)m_iSubID).getCommandType();
	case ACTIONSUBTYPE_AUTOMATE:
		return (CommandTypes)GC.getInfo((AutomateTypes)m_iSubID).getCommand();
	case ACTIONSUBTYPE_COMMAND:
		return (CommandTypes)m_iSubID;
	default:
		return NO_COMMAND;
	}
}

int CvActionInfo::getControlType() const
{
	if (ACTIONSUBTYPE_CONTROL == m_eSubType)
		return m_iSubID;

	return -1;
}

int CvActionInfo::getSubID() const
{
	return m_iSubID;
}

void CvActionInfo::setSubID(int i)
{
	m_iSubID = i;
}

bool CvActionInfo::isConfirmCommand() const
{
	switch(getSubType()) // advc (replacing if/else)
	{
	case ACTIONSUBTYPE_COMMAND:
		return GC.getInfo((CommandTypes)m_iSubID).getConfirmCommand();
	case ACTIONSUBTYPE_AUTOMATE:
		return GC.getInfo((AutomateTypes)m_iSubID).getConfirmCommand();
	default:
		return false;
	}
}

bool CvActionInfo::isVisible() const
{
	switch(getSubType())
	{
	case ACTIONSUBTYPE_CONTROL:
		return false;
	case ACTIONSUBTYPE_COMMAND:
		return GC.getInfo((CommandTypes)m_iSubID).getVisible();
	case ACTIONSUBTYPE_AUTOMATE:
		return GC.getInfo((AutomateTypes)m_iSubID).getVisible();
	case ACTIONSUBTYPE_MISSION:
		return GC.getInfo((MissionTypes)m_iSubID).getVisible();
	case ACTIONSUBTYPE_INTERFACEMODE:
		return GC.getInfo((InterfaceModeTypes)m_iSubID).getVisible();
	default:
		return true;
	}
}

ActionSubTypes CvActionInfo::getSubType() const
{
	return m_eSubType;
}

void CvActionInfo::setSubType(ActionSubTypes eSubType)
{
	m_eSubType = eSubType;
}

CvHotkeyInfo* CvActionInfo::getHotkeyInfo() const
{
	int const iData = m_iSubID;
	switch(getSubType())
	{
		case ACTIONSUBTYPE_INTERFACEMODE:
			return &GC.getInfo((InterfaceModeTypes)iData);
		case ACTIONSUBTYPE_COMMAND:
			return &GC.getInfo((CommandTypes)iData);
		case ACTIONSUBTYPE_BUILD:
			return &GC.getInfo((BuildTypes)iData);
		case ACTIONSUBTYPE_PROMOTION:
			return &GC.getInfo((PromotionTypes)iData);
		case ACTIONSUBTYPE_UNIT:
			return &GC.getInfo((UnitTypes)iData);
		case ACTIONSUBTYPE_RELIGION:
			return &GC.getInfo((ReligionTypes)iData);
		case ACTIONSUBTYPE_CORPORATION:
			return &GC.getInfo((CorporationTypes)iData);
		case ACTIONSUBTYPE_SPECIALIST:
			return &GC.getInfo((SpecialistTypes)iData);
		case ACTIONSUBTYPE_BUILDING:
			return &GC.getInfo((BuildingTypes)iData);
		case ACTIONSUBTYPE_CONTROL:
			return &GC.getInfo((ControlTypes)iData);
		case ACTIONSUBTYPE_AUTOMATE:
			return &GC.getInfo((AutomateTypes)iData);
		case ACTIONSUBTYPE_MISSION:
			return &GC.getInfo((MissionTypes)iData);
		default:
		FAssertMsg((0) ,"Unknown Action Subtype in CvActionInfo::getHotkeyInfo");
		return NULL;
	}
}

const TCHAR* CvActionInfo::getType() const
{
	if (getHotkeyInfo())
		return getHotkeyInfo()->getType();

	return NULL;
}

const wchar* CvActionInfo::getDescription() const
{
	if (getHotkeyInfo())
		return getHotkeyInfo()->getDescription();

	return L"";
}

const wchar* CvActionInfo::getCivilopedia() const
{
	if (getHotkeyInfo())
		return getHotkeyInfo()->getCivilopedia();

	return L"";
}

const wchar* CvActionInfo::getHelp() const
{
	if (getHotkeyInfo())
		return getHotkeyInfo()->getHelp();

	return L"";
}

const wchar* CvActionInfo::getStrategy() const
{
	if (getHotkeyInfo())
		return getHotkeyInfo()->getStrategy();

	return L"";
}

const TCHAR* CvActionInfo::getButton() const
{
	if (getHotkeyInfo())
		return getHotkeyInfo()->getButton();

	return NULL;
}

const wchar* CvActionInfo::getTextKeyWide() const
{
	if (getHotkeyInfo())
		return getHotkeyInfo()->getTextKeyWide();

	return NULL;
}

int CvActionInfo::getActionInfoIndex() const
{
	if (getHotkeyInfo())
		return getHotkeyInfo()->getActionInfoIndex();

	return -1;
}

int CvActionInfo::getHotKeyVal() const
{
	if (getHotkeyInfo())
		return getHotkeyInfo()->getHotKeyVal();

	return -1;
}

int CvActionInfo::getHotKeyPriority() const
{
	if (getHotkeyInfo())
		return getHotkeyInfo()->getHotKeyPriority();

	return -1;
}

int CvActionInfo::getHotKeyValAlt() const
{
	if (getHotkeyInfo())
		return getHotkeyInfo()->getHotKeyValAlt();

	return -1;
}

int CvActionInfo::getHotKeyPriorityAlt() const
{
	if (getHotkeyInfo())
		return getHotkeyInfo()->getHotKeyPriorityAlt();

	return -1;
}

int CvActionInfo::getOrderPriority() const
{
	if (getHotkeyInfo())
		return getHotkeyInfo()->getOrderPriority();

	return -1;
}

bool CvActionInfo::isAltDown() const
{
	if (getHotkeyInfo())
		return getHotkeyInfo()->isAltDown();

	return false;
}

bool CvActionInfo::isShiftDown() const
{
	if (getHotkeyInfo())
		return getHotkeyInfo()->isShiftDown();

	return false;
}

bool CvActionInfo::isCtrlDown() const
{
	if (getHotkeyInfo())
		return getHotkeyInfo()->isCtrlDown();

	return false;
}

bool CvActionInfo::isAltDownAlt() const
{
	if (getHotkeyInfo())
		return getHotkeyInfo()->isAltDownAlt();

	return false;
}

bool CvActionInfo::isShiftDownAlt() const
{
	if (getHotkeyInfo())
		return getHotkeyInfo()->isShiftDownAlt();

	return false;
}

bool CvActionInfo::isCtrlDownAlt() const
{
	if (getHotkeyInfo())
		return getHotkeyInfo()->isCtrlDownAlt();

	return false;
}

const TCHAR* CvActionInfo::getHotKey() const
{
	if (getHotkeyInfo())
		return getHotkeyInfo()->getHotKey();

	return NULL;
}

std::wstring CvActionInfo::getHotKeyDescription() const
{
	if (getHotkeyInfo())
		return getHotkeyInfo()->getHotKeyDescription();

	return L"";
}

CvMissionInfo::CvMissionInfo() :
m_iTime(0),
m_bSound(false),
m_bTarget(false),
m_bBuild(false),
m_bVisible(false),
m_eEntityEvent(NO_ENTITYEVENT)
{}

int CvMissionInfo::getTime() const
{
	return m_iTime;
}

bool CvMissionInfo::isSound() const
{
	return m_bSound;
}

bool CvMissionInfo::isTarget() const
{
	return m_bTarget;
}

bool CvMissionInfo::isBuild() const
{
	return m_bBuild;
}

bool CvMissionInfo::getVisible() const
{
	return m_bVisible;
}

const TCHAR* CvMissionInfo::getWaypoint() const
{
	return m_szWaypoint;
}

EntityEventTypes CvMissionInfo::getEntityEvent() const
{
	return m_eEntityEvent;
}

bool CvMissionInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML))
		return false;

	pXML->GetChildXmlValByName(m_szWaypoint, "Waypoint");
	pXML->GetChildXmlValByName(&m_iTime, "iTime");
	pXML->GetChildXmlValByName(&m_bSound, "bSound");
	pXML->GetChildXmlValByName(&m_bTarget, "bTarget");
	pXML->GetChildXmlValByName(&m_bBuild, "bBuild");
	pXML->GetChildXmlValByName(&m_bVisible, "bVisible", /* advc.006b: */ false);

	CvString szTmp;
	if (pXML->GetChildXmlValByName(szTmp, "EntityEventType", /* advc.006b: */ ""))
		m_eEntityEvent = (EntityEventTypes)pXML->FindInInfoClass(szTmp);
	else m_eEntityEvent = NO_ENTITYEVENT;

	return true;
}

CvInterfaceModeInfo::CvInterfaceModeInfo() :
m_iCursorIndex(NO_CURSOR),
m_iMissionType(NO_MISSION),
m_bVisible(false),
m_bGotoPlot(false),
m_bHighlightPlot(false),
m_bSelectType(false),
m_bSelectAll(false)
{}

int CvInterfaceModeInfo::getCursorIndex() const
{
	return m_iCursorIndex;
}

int CvInterfaceModeInfo::getMissionType() const
{
	return m_iMissionType;
}

bool CvInterfaceModeInfo::getVisible() const
{
	return m_bVisible;
}

bool CvInterfaceModeInfo::getGotoPlot() const
{
	return m_bGotoPlot;
}

bool CvInterfaceModeInfo::getHighlightPlot() const
{
	return m_bHighlightPlot;
}

bool CvInterfaceModeInfo::getSelectType() const
{
	return m_bSelectType;
}

bool CvInterfaceModeInfo::getSelectAll() const
{
	return m_bSelectAll;
}

bool CvInterfaceModeInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML))
		return false;

	pXML->SetInfoIDFromChildXmlVal(m_iCursorIndex, "CursorType");
	pXML->SetInfoIDFromChildXmlVal(m_iMissionType, "Mission");

	pXML->GetChildXmlValByName(&m_bVisible, "bVisible");
	pXML->GetChildXmlValByName(&m_bGotoPlot, "bGotoPlot");
	pXML->GetChildXmlValByName(&m_bHighlightPlot, "bHighlightPlot");
	pXML->GetChildXmlValByName(&m_bSelectType, "bSelectType");
	pXML->GetChildXmlValByName(&m_bSelectAll, "bSelectAll");

	return true;
}

// advc: Removed this pointless function
/*bool CvControlInfo::read(CvXMLLoadUtility* pXML)
{
	return CvHotkeyInfo::read(pXML);
}*/
