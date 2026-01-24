#include "CvGameCoreDLL.h"
#include "CvInfo_Misc.h"
#include "CvXMLLoadUtility.h"
#include "CvGameTextMgr.h" // for CvGameText::read

// advc: Better leave these alone b/c they're DLLExports
CvUnitFormationInfo::CvUnitFormationInfo() {}
CvUnitFormationInfo::~CvUnitFormationInfo() {}

const TCHAR* CvUnitFormationInfo::getFormationType() const
{
	return m_szFormationType;
}

const std::vector<EntityEventTypes> & CvUnitFormationInfo::getEventTypes() const
{
	return m_vctEventTypes;
}

int CvUnitFormationInfo::getNumUnitEntries() const
{
	return m_vctUnitEntries.size();
}

const CvUnitEntry &CvUnitFormationInfo::getUnitEntry(int index) const
{
	return m_vctUnitEntries[index];
}

void CvUnitFormationInfo::addUnitEntry(const CvUnitEntry &unitEntry)
{
	m_vctUnitEntries.push_back(unitEntry);
}

int CvUnitFormationInfo::getNumGreatUnitEntries() const
{
	return m_vctGreatUnitEntries.size();
}

const CvUnitEntry &CvUnitFormationInfo::getGreatUnitEntry(int index) const
{
	return m_vctGreatUnitEntries[index];
}

int CvUnitFormationInfo::getNumSiegeUnitEntries() const
{
	return m_vctSiegeUnitEntries.size();
}

const CvUnitEntry &CvUnitFormationInfo::getSiegeUnitEntry(int index) const
{
	return m_vctSiegeUnitEntries[index];
}

bool CvUnitFormationInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
		return false;

	pXML->GetChildXmlValByName(m_szFormationType, "FormationType");

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "EventMaskList"))
	{
		if (gDLL->getXMLIFace()->SetToChild(pXML->GetXML()))
		{
			CvString szTextVal;
			pXML->GetXmlVal(szTextVal);
			bool bNextSibling;
			do
			{
				int iIndex = pXML->FindInInfoClass(szTextVal);
				if (iIndex != -1)
					m_vctEventTypes.push_back((EntityEventTypes)iIndex);
				bNextSibling = pXML->GetNextXmlVal(szTextVal);
			}
			while(bNextSibling);
			gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "UnitEntry"))
	{
		do
		{
			CvUnitEntry unitEntry;
			CvString szTextVal;
			pXML->GetChildXmlValByName(szTextVal, "UnitEntryType");
			if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "Position"))
			{
				pXML->GetChildXmlValByName(&unitEntry.m_position.x, "x");
				pXML->GetChildXmlValByName(&unitEntry.m_position.y, "y");
				gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
			}
			pXML->GetChildXmlValByName(&unitEntry.m_fRadius, "PositionRadius");
			pXML->GetChildXmlValByName(&unitEntry.m_fFacingDirection, "Direction");
			pXML->GetChildXmlValByName(&unitEntry.m_fFacingVariance, "DirVariation");

			if(szTextVal.CompareNoCase("Unit") == 0)
				m_vctUnitEntries.push_back(unitEntry);
			else if(szTextVal.CompareNoCase("General") == 0)
				m_vctGreatUnitEntries.push_back(unitEntry);
			else if(szTextVal.CompareNoCase("Siege") == 0)
				m_vctSiegeUnitEntries.push_back(unitEntry);
			else FErrorMsg("[Jason] Unknown unit formation entry type.");
		}
		while (gDLL->getXMLIFace()->LocateNextSiblingNodeByTagName(pXML->GetXML(), "UnitEntry"));
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	FAssertMsg(m_vctGreatUnitEntries.size() > 0, "[Jason] Formation missing great general entry.");
	FAssertMsg(m_vctSiegeUnitEntries.size() > 0, "[Jason] Formation missing siege tower entry.");

	return true;
}

CvRiverModelInfo::CvRiverModelInfo() :
m_iTextureIndex(0)
{
	m_szDeltaString[0] = '\0';
	m_szConnectString[0] = '\0';
	m_szRotateString[0] = '\0';
}

const TCHAR* CvRiverModelInfo::getModelFile() const
{
	return m_szModelFile;
}

const TCHAR* CvRiverModelInfo::getBorderFile() const
{
	return m_szBorderFile;
}

int CvRiverModelInfo::getTextureIndex() const
{
	return m_iTextureIndex;
}

const TCHAR* CvRiverModelInfo::getDeltaString() const
{
	return m_szDeltaString;
}

const TCHAR* CvRiverModelInfo::getConnectString() const
{
	return m_szConnectString;
}

const TCHAR* CvRiverModelInfo::getRotateString() const
{
	return m_szRotateString;
}

bool CvRiverModelInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
		return false;

	if(pXML->GetChildXmlValByName(m_szModelFile, "ModelFile"))
	if(pXML->GetChildXmlValByName(m_szBorderFile, "BorderFile"))

	pXML->GetChildXmlValByName(&m_iTextureIndex, "TextureIndex");
	pXML->GetChildXmlValByName(m_szDeltaString, "DeltaType");
	pXML->GetChildXmlValByName(m_szConnectString, "Connections");
	pXML->GetChildXmlValByName(m_szRotateString, "Rotations");

	return true;
}


CvRouteModelInfo::CvRouteModelInfo() :
m_eRouteType(NO_ROUTE),
m_bAnimated(false)
{
	m_szConnectString[0] = '\0';
	m_szModelConnectString[0] = '\0';
	m_szRotateString[0] = '\0';
}

RouteTypes CvRouteModelInfo::getRouteType() const
{
	return m_eRouteType;
}

const TCHAR* CvRouteModelInfo::getModelFile() const
{
	return m_szModelFile;
}

const TCHAR* CvRouteModelInfo::getLateModelFile() const
{
	return m_szLateModelFile;
}

const TCHAR* CvRouteModelInfo::getModelFileKey() const
{
	return m_szModelFileKey;
}

bool CvRouteModelInfo::isAnimated() const
{
	return m_bAnimated;
}

const TCHAR* CvRouteModelInfo::getConnectString() const
{
	return m_szConnectString;
}

const TCHAR* CvRouteModelInfo::getModelConnectString() const
{
	return m_szModelConnectString;
}

const TCHAR* CvRouteModelInfo::getRotateString() const
{
	return m_szRotateString;
}

bool CvRouteModelInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
		return false;

	pXML->GetChildXmlValByName(m_szModelFile, "ModelFile");
	pXML->GetChildXmlValByName(m_szLateModelFile, "LateModelFile");
	pXML->GetChildXmlValByName(m_szModelFileKey, "ModelFileKey");

	pXML->GetChildXmlValByName(&m_bAnimated, "Animated");

	pXML->SetInfoIDFromChildXmlVal(m_eRouteType, "RouteType");

	pXML->GetChildXmlValByName(m_szConnectString, "Connections");
	pXML->GetChildXmlValByName(m_szModelConnectString, "ModelConnections");
	pXML->GetChildXmlValByName(m_szRotateString, "Rotations");

	return true;
}

const TCHAR* CvAdvisorInfo::getTexture() const
{
	return m_szTexture;
}

int CvAdvisorInfo::getNumCodes() const
{
	return m_vctEnableDisableCodes.size();
}

int CvAdvisorInfo::getEnableCode(uint uiCode) const
{
	FAssert(uiCode < m_vctEnableDisableCodes.size());
	return m_vctEnableDisableCodes[uiCode].first;
}

int CvAdvisorInfo::getDisableCode(uint uiCode) const
{
	FAssert(uiCode < m_vctEnableDisableCodes.size());
	return m_vctEnableDisableCodes[uiCode].second;
}

bool CvAdvisorInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
		return false;

	pXML->GetChildXmlValByName(m_szTexture, "Texture",
			""); // advc.006b: Actually, none of them has a texture.

	gDLL->getXMLIFace()->SetToChild(pXML->GetXML());
	while(gDLL->getXMLIFace()->LocateNextSiblingNodeByTagName(pXML->GetXML(), "EventCodes"))
	{
		int iEnableCode, iDisableCode;
		pXML->GetChildXmlValByName(&iEnableCode, "iEnableCode");
		pXML->GetChildXmlValByName(&iDisableCode, "iDisableCode");
		m_vctEnableDisableCodes.push_back(std::make_pair(iEnableCode, iDisableCode));
	}
	gDLL->getXMLIFace()->SetToParent(pXML->GetXML());

	return true;
}

const TCHAR* CvCursorInfo::getPath()
{
	return m_szPath;
}

void CvCursorInfo::setPath(const TCHAR* szVal)
{
	m_szPath = szVal;
}

bool CvCursorInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
		return false;

	CvString szTextVal;
	pXML->GetChildXmlValByName(szTextVal, "CursorPath");
	setPath(szTextVal);

	return true;
}

const TCHAR* CvThroneRoomCamera::getFileName()
{
	return m_szFileName;
}

void CvThroneRoomCamera::setFileName(const TCHAR* szVal)
{
	m_szFileName = szVal;
}

bool CvThroneRoomCamera::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
		return false;

	CvString szTextVal;
	pXML->GetChildXmlValByName(szTextVal, "FileName");
	setFileName(szTextVal);

	return true;
}

CvThroneRoomInfo::CvThroneRoomInfo() :
m_iFromState(0),
m_iToState(0),
m_iAnimation(0)
{}

const TCHAR* CvThroneRoomInfo::getEvent()
{
	return m_szEvent;
}

const TCHAR* CvThroneRoomInfo::getNodeName()
{
	return m_szNodeName;
}

int CvThroneRoomInfo::getFromState()
{
	return m_iFromState;
}

int CvThroneRoomInfo::getToState()
{
	return m_iToState;
}

int CvThroneRoomInfo::getAnimation()
{
	return m_iAnimation;
}

bool CvThroneRoomInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
		return false;

	pXML->GetChildXmlValByName(m_szEvent, "Event");
	pXML->GetChildXmlValByName(&m_iFromState, "iFromState");
	pXML->GetChildXmlValByName(&m_iToState, "iToState");
	pXML->GetChildXmlValByName(m_szNodeName, "NodeName");
	pXML->GetChildXmlValByName(&m_iAnimation, "iAnimation");

	return true;
}

const TCHAR* CvThroneRoomStyleInfo::getArtStyleType()
{
	return m_szArtStyleType;
}

const TCHAR* CvThroneRoomStyleInfo::getEraType()
{
	return m_szEraType;
}

const TCHAR* CvThroneRoomStyleInfo::getFileName()
{
	return m_szFileName;
}

bool CvThroneRoomStyleInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
		return false;

	pXML->GetChildXmlValByName(m_szArtStyleType, "ArtStyleType");
	pXML->GetChildXmlValByName(m_szEraType, "EraType");
	pXML->GetChildXmlValByName(m_szFileName, "FileName");

	if(gDLL->getXMLIFace()->SetToChild(pXML->GetXML()))
	{
		CvString szTextVal;
		while(gDLL->getXMLIFace()->LocateNextSiblingNodeByTagName(pXML->GetXML(), "NodeName"))
		{
			pXML->GetXmlVal(szTextVal);
			m_aNodeNames.push_back(szTextVal);
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	if(gDLL->getXMLIFace()->SetToChild(pXML->GetXML()))
	{
		CvString szTextVal;
		while(gDLL->getXMLIFace()->LocateNextSiblingNodeByTagName(pXML->GetXML(), "TextureName"))
		{
			pXML->GetXmlVal(szTextVal);
			m_aTextureNames.push_back(szTextVal);
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	return true;
}

CvSlideShowInfo::CvSlideShowInfo() : m_fStartTime(0.0f) {}

const TCHAR* CvSlideShowInfo::getPath()
{
	return m_szPath;
}

void CvSlideShowInfo::setPath(const TCHAR* szVal)
{
	m_szPath = szVal;
}

const TCHAR* CvSlideShowInfo::getTransitionType()
{
	return m_szTransitionType;
}

void CvSlideShowInfo::setTransitionType(const TCHAR* szVal)
{
	m_szTransitionType = szVal;
}

float CvSlideShowInfo::getStartTime()
{
	return m_fStartTime;
}

void CvSlideShowInfo::setStartTime(float fVal)
{
	m_fStartTime = fVal;
}

bool CvSlideShowInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
		return false;

	float fVal;
	CvString szTextVal;
	pXML->GetChildXmlValByName(szTextVal, "Path");
	setPath(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "TransitionType");
	setTransitionType(szTextVal);
	pXML->GetChildXmlValByName(&fVal, "fStartTime");
	setStartTime(fVal);

	return true;
}

const TCHAR* CvSlideShowRandomInfo::getPath()
{
	return m_szPath;
}

void CvSlideShowRandomInfo::setPath(const TCHAR* szVal)
{
	m_szPath = szVal;
}

bool CvSlideShowRandomInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvInfoBase::read(pXML))
		return false;

	pXML->GetChildXmlValByName(szTextVal, "Path");
	setPath(szTextVal);

	return true;
}

const TCHAR* CvWorldPickerInfo::getMapName()
{
	return m_szMapName;
}

const TCHAR* CvWorldPickerInfo::getModelFile()
{
	return m_szModelFile;
}

int CvWorldPickerInfo::getNumSizes()
{
	return m_aSizes.size();
}

float CvWorldPickerInfo::getSize(int index)
{
	return m_aSizes[index];
}

int CvWorldPickerInfo::getNumClimates()
{
	return m_aClimates.size();
}

const TCHAR* CvWorldPickerInfo::getClimatePath(int index)
{
	return m_aClimates[index];
}

int CvWorldPickerInfo::getNumWaterLevelDecals()
{
	return m_aWaterLevelDecals.size();
}

const TCHAR* CvWorldPickerInfo::getWaterLevelDecalPath(int index)
{
	return m_aWaterLevelDecals[index];
}

int CvWorldPickerInfo::getNumWaterLevelGloss()
{
	return m_aWaterLevelGloss.size();
}

const TCHAR* CvWorldPickerInfo::getWaterLevelGlossPath(int index)
{
	return m_aWaterLevelGloss[index];
}

bool CvWorldPickerInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
		return false;

	pXML->GetChildXmlValByName(m_szMapName, "MapName");
	pXML->GetChildXmlValByName(m_szModelFile, "ModelFile");

	if(gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "Sizes"))
	{
		if(gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "Size"))
		{
			do
			{
				float fVal;
				pXML->GetXmlVal(fVal);
				m_aSizes.push_back(fVal);
			} while (gDLL->getXMLIFace()->LocateNextSiblingNodeByTagName(pXML->GetXML(), "Size"));

			gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	if(gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "Climates"))
	{
		if(gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "ClimatePath"))
		{
			CvString szTextVal;
			do
			{
				pXML->GetXmlVal(szTextVal);
				m_aClimates.push_back(szTextVal);
			} while (gDLL->getXMLIFace()->LocateNextSiblingNodeByTagName(pXML->GetXML(), "ClimatePath"));

			gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	if(gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "WaterLevelDecals"))
	{
		if(gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "WaterLevelDecalPath"))
		{
			CvString szTextVal;
			do
			{
				pXML->GetXmlVal(szTextVal);
				m_aWaterLevelDecals.push_back(szTextVal);
			} while (gDLL->getXMLIFace()->LocateNextSiblingNodeByTagName(pXML->GetXML(), "WaterLevelDecalPath"));

			gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	if(gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "WaterLevelGloss"))
	{
		if(gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "WaterLevelGlossPath"))
		{
			CvString szTextVal;
			do
			{
				pXML->GetXmlVal(szTextVal);
				m_aWaterLevelGloss.push_back(szTextVal);
			} while (gDLL->getXMLIFace()->LocateNextSiblingNodeByTagName(pXML->GetXML(), "WaterLevelGlossPath"));

			gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	return true;
}

CvSpaceShipInfo::CvSpaceShipInfo() :
m_eSpaceShipInfoType(SPACE_SHIP_INFO_TYPE_NONE),
m_iPartNumber(-1),
m_iArtType(-1),
m_iEventCode(-1),
m_eProjectType(NO_PROJECT),
m_eCameraUpAxis(AXIS_X)
{}

const TCHAR* CvSpaceShipInfo::getNodeName()
{
	return m_szNodeName;
}

const TCHAR* CvSpaceShipInfo::getProjectName()
{
	return m_szProjectName;
}

void CvSpaceShipInfo::setProjectName(const TCHAR* szVal)
{
	m_szProjectName = szVal;
	m_eProjectType = (ProjectTypes)GC.getInfoTypeForString(m_szProjectName, true);
}

ProjectTypes CvSpaceShipInfo::getProjectType()
{
	return m_eProjectType;
}

AxisTypes CvSpaceShipInfo::getCameraUpAxis()
{
	return m_eCameraUpAxis;
}

SpaceShipInfoTypes CvSpaceShipInfo::getSpaceShipInfoType()
{
	return m_eSpaceShipInfoType;
}

int CvSpaceShipInfo::getPartNumber()
{
	return m_iPartNumber;
}

int CvSpaceShipInfo::getArtType()
{
	return m_iArtType;
}

int CvSpaceShipInfo::getEventCode()
{
	return m_iEventCode;
}

bool CvSpaceShipInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
		return false;

	pXML->GetChildXmlValByName(m_szNodeName, "NodeName");

	CvString szTextVal;

	pXML->GetChildXmlValByName(szTextVal, "ProjectName");
	setProjectName(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "CameraUpAxis");
	if(szTextVal.CompareNoCase("AXIS_X") == 0)
		m_eCameraUpAxis = AXIS_X;
	else if(szTextVal.CompareNoCase("AXIS_Y") == 0)
		m_eCameraUpAxis = AXIS_Y;
	else if(szTextVal.CompareNoCase("AXIS_Z") == 0)
		m_eCameraUpAxis = AXIS_Z;
	else FErrorMsg("[Jason] Unknown Axis Type.");

	pXML->GetChildXmlValByName(&m_iPartNumber, "PartNumber");
	pXML->GetChildXmlValByName(&m_iArtType, "ArtType");
	pXML->GetChildXmlValByName(&m_iEventCode, "EventCode");

	pXML->GetChildXmlValByName(szTextVal, "InfoType");
	if(szTextVal.CompareNoCase("SPACE_SHIP_INFO_TYPE_FILENAME") == 0)
		m_eSpaceShipInfoType = SPACE_SHIP_INFO_TYPE_FILENAME;
	else if(szTextVal.CompareNoCase("SPACE_SHIP_INFO_TYPE_ALPHA_CENTAURI") == 0)
		m_eSpaceShipInfoType = SPACE_SHIP_INFO_TYPE_ALPHA_CENTAURI;
	else if(szTextVal.CompareNoCase("SPACE_SHIP_INFO_TYPE_LAUNCH") == 0)
		m_eSpaceShipInfoType = SPACE_SHIP_INFO_TYPE_LAUNCH;
	else if(szTextVal.CompareNoCase("SPACE_SHIP_INFO_TYPE_LAUNCHED") == 0)
		m_eSpaceShipInfoType = SPACE_SHIP_INFO_TYPE_LAUNCHED;
	else if(szTextVal.CompareNoCase("SPACE_SHIP_INFO_TYPE_ZOOM_IN") == 0)
		m_eSpaceShipInfoType = SPACE_SHIP_INFO_TYPE_ZOOM_IN;
	else if(szTextVal.CompareNoCase("SPACE_SHIP_INFO_TYPE_ZOOM_MOVE") == 0)
		m_eSpaceShipInfoType = SPACE_SHIP_INFO_TYPE_ZOOM_MOVE;
	else if(szTextVal.CompareNoCase("SPACE_SHIP_INFO_TYPE_COMPONENT_OFF") == 0)
		m_eSpaceShipInfoType = SPACE_SHIP_INFO_TYPE_COMPONENT_OFF;
	else if(szTextVal.CompareNoCase("SPACE_SHIP_INFO_TYPE_COMPONENT_APPEAR") == 0)
		m_eSpaceShipInfoType = SPACE_SHIP_INFO_TYPE_COMPONENT_APPEAR;
	else if(szTextVal.CompareNoCase("SPACE_SHIP_INFO_TYPE_COMPONENT_PREVIEW") == 0)
		m_eSpaceShipInfoType = SPACE_SHIP_INFO_TYPE_COMPONENT_PREVIEW;
	else if(szTextVal.CompareNoCase("SPACE_SHIP_INFO_TYPE_COMPONENT_ON") == 0)
		m_eSpaceShipInfoType = SPACE_SHIP_INFO_TYPE_COMPONENT_ON;
	else if(szTextVal.CompareNoCase("SPACE_SHIP_INFO_TYPE_LIGHT_OFF") == 0)
		m_eSpaceShipInfoType = SPACE_SHIP_INFO_TYPE_LIGHT_OFF;
	else if(szTextVal.CompareNoCase("SPACE_SHIP_INFO_TYPE_GANTRY_SMOKE_ON") == 0)
		m_eSpaceShipInfoType = SPACE_SHIP_INFO_TYPE_GANTRY_SMOKE_ON;
	else if(szTextVal.CompareNoCase("SPACE_SHIP_INFO_TYPE_IN_SPACE_SMOKE_ON") == 0)
		m_eSpaceShipInfoType = SPACE_SHIP_INFO_TYPE_IN_SPACE_SMOKE_ON;
	else if(szTextVal.CompareNoCase("SPACE_SHIP_INFO_TYPE_IN_GAME_SMOKE_ON") == 0)
		m_eSpaceShipInfoType = SPACE_SHIP_INFO_TYPE_IN_GAME_SMOKE_ON;
	else FErrorMsg("[Jason] Unknown SpaceShipInfoType.");

	return true;
}

CvAnimationPathInfo::CvAnimationPathInfo() : m_bMissionPath(false) {}

int CvAnimationPathInfo::getPathCategory(int i)
{
	return (int)m_vctPathDefinition.size() > i ? m_vctPathDefinition[i].first : -1;
}

float CvAnimationPathInfo::getPathParameter(int i)
{
	return (int)m_vctPathDefinition.size() > i ? m_vctPathDefinition[i].second : -1;
}

int CvAnimationPathInfo::getNumPathDefinitions()
{
	return m_vctPathDefinition.size();
}

CvAnimationPathDefinition * CvAnimationPathInfo::getPath()
{
	return &m_vctPathDefinition;
}

bool CvAnimationPathInfo::isMissionPath() const
{
	return m_bMissionPath;
}

bool CvAnimationPathInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
		return false;

	TCHAR szTempString[1024];	// Extracting text
	int iCurrentCategory; // The current category information we are building
	float fParameter; // Temporary

	pXML->GetChildXmlValByName(&m_bMissionPath, "bMissionPath");
	gDLL->getXMLIFace()->SetToChild(pXML->GetXML());
	gDLL->getXMLIFace()->GetLastNodeText(pXML->GetXML(), szTempString);
	gDLL->getXMLIFace()->NextSibling(pXML->GetXML());
	gDLL->getXMLIFace()->NextSibling(pXML->GetXML());
	do
	{
		if (pXML->GetChildXmlValByName(szTempString, _T("Category"), /* advc.006b: */ ""))
		{
			iCurrentCategory = pXML->FindInInfoClass(szTempString);
			fParameter = 0.0f;
		}
		else
		{
			pXML->GetChildXmlValByName( szTempString, _T("Operator"));
			iCurrentCategory = GC.getTypesEnum(szTempString);
			iCurrentCategory = ((int)ANIMOP_FIRST) + iCurrentCategory;
			if (!pXML->GetChildXmlValByName(&fParameter, "Parameter"))
				fParameter = 0.0f;
		}
		m_vctPathDefinition.push_back(std::make_pair(iCurrentCategory, fParameter));
	}
	while (gDLL->getXMLIFace()->NextSibling(pXML->GetXML()));
	gDLL->getXMLIFace()->SetToParent(pXML->GetXML());

	return true;
}

CvAnimationCategoryInfo::CvAnimationCategoryInfo()
{
	m_kCategory.second = -7540; // invalid.
}

int CvAnimationCategoryInfo::getCategoryBaseID()
{
	return m_kCategory.first;
}

int CvAnimationCategoryInfo::getCategoryDefaultTo()
{
	if (m_kCategory.second < -1)
	{
		// CvXMLLoadUtility *pXML = new CvXMLLoadUtility();
		m_kCategory.second = CvXMLLoadUtility::FindInInfoClass( m_szDefaultTo);
	}
	return (int)m_kCategory.second;
}

bool CvAnimationCategoryInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
		return false;

	pXML->GetChildXmlValByName(m_szDefaultTo, "DefaultTo");
	int	iBaseID; // Temporary
	pXML->GetChildXmlValByName(&iBaseID, "BaseID");
	m_kCategory.first = iBaseID;
	return true;
}

CvEntityEventInfo::CvEntityEventInfo() : m_bUpdateFormation(true) {}

bool CvEntityEventInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
		return false;

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"AnimationPathTypes"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			if (iNumSibs > 0)
			{
				CvString szTmp;
				if (pXML->GetChildXmlVal(szTmp))
				{
					AnimationPathTypes eAnimationPath = (AnimationPathTypes)CvXMLLoadUtility::FindInInfoClass(szTmp);
					if (eAnimationPath > ANIMATIONPATH_NONE)
						m_vctAnimationPathType.push_back(eAnimationPath);
					for (int i = 1; i < iNumSibs; i++)
					{
						if (!pXML->GetNextXmlVal(szTmp))
							break;
						// advc: renamed to avoid shadowing of eAnimationPath
						AnimationPathTypes eLoopAnimationPath = (AnimationPathTypes)CvXMLLoadUtility::FindInInfoClass(szTmp);
						if (eLoopAnimationPath > ANIMATIONPATH_NONE)
							m_vctAnimationPathType.push_back(eLoopAnimationPath);
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"EffectTypes"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			if (iNumSibs > 0)
			{
				CvString szTmp;
				if (pXML->GetChildXmlVal(szTmp))
				{
					EffectTypes eEffectType = (EffectTypes)CvXMLLoadUtility::FindInInfoClass(szTmp);
					if (eEffectType > NO_EFFECT)
						m_vctEffectTypes.push_back(eEffectType);
					for (int i = 1; i < iNumSibs; i++)
					{
						if (!pXML->GetNextXmlVal(szTmp))
							break;
						// advc: renamed to avoid shadowing of eEffectType
						EffectTypes eLoopEffectType = (EffectTypes)CvXMLLoadUtility::FindInInfoClass(szTmp);
						if (eLoopEffectType > NO_EFFECT)
							m_vctEffectTypes.push_back(eLoopEffectType);
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	pXML->GetChildXmlValByName(&m_bUpdateFormation, "bUpdateFormation");

	return true;
}

AnimationPathTypes CvEntityEventInfo::getAnimationPathType(int iIndex) const
{
	return iIndex >= (int)m_vctAnimationPathType.size() ? ANIMATIONPATH_NONE : m_vctAnimationPathType[iIndex];
}

EffectTypes CvEntityEventInfo::getEffectType(int iIndex) const
{
	return iIndex >= (int)m_vctEffectTypes.size() ? NO_EFFECT : m_vctEffectTypes[iIndex];
}

int CvEntityEventInfo::getAnimationPathCount() const
{
	return m_vctAnimationPathType.size();
}

int CvEntityEventInfo::getEffectTypeCount() const
{
	return m_vctEffectTypes.size();
}

bool CvEntityEventInfo::getUpdateFormation() const
{
	return m_bUpdateFormation;
}

CvLandscapeInfo::CvLandscapeInfo() :
m_iFogR(0),
m_iFogG(0),
m_iFogB(0),
m_iHorizontalGameCell(0),
m_iVerticalGameCell(0),
m_iPlotsPerCellX(0),
m_iPlotsPerCellY(0),
m_iHorizontalVertCnt(0),
m_iVerticalVertCnt(0),
m_iWaterHeight(0),
m_fTextureScaleX(0.0f),
m_fTextureScaleY(0.0f),
m_fZScale(0.0f),
// <kmodx>
m_fPeakScale(0.0f),
m_fHillScale(0.0f),
// </kmodx>
m_bUseTerrainShader(false),
m_bUseLightmap(false),
m_bRandomMap(false)
{}

int CvLandscapeInfo::getFogR() const
{
	return m_iFogR;
}

int CvLandscapeInfo::getFogG() const
{
	return m_iFogG;
}

int CvLandscapeInfo::getFogB() const
{
	return m_iFogB;
}

int CvLandscapeInfo::getHorizontalGameCell() const
{
	return m_iHorizontalGameCell;
}

int CvLandscapeInfo::getVerticalGameCell() const
{
	return m_iVerticalGameCell;
}

int CvLandscapeInfo::getPlotsPerCellX() const
{
	return m_iPlotsPerCellX;
}

int CvLandscapeInfo::getPlotsPerCellY() const
{
	return m_iPlotsPerCellY;
}

int CvLandscapeInfo::getHorizontalVertCnt() const
{
	return m_iHorizontalVertCnt;
}

int CvLandscapeInfo::getVerticalVertCnt() const
{
	return m_iVerticalVertCnt;
}

int CvLandscapeInfo::getWaterHeight() const
{
	return m_iWaterHeight;
}

float CvLandscapeInfo::getTextureScaleX() const
{
	return m_fTextureScaleX;
}

float CvLandscapeInfo::getTextureScaleY() const
{
	return m_fTextureScaleY;
}

float CvLandscapeInfo::getZScale() const
{
	return m_fZScale;
}

bool CvLandscapeInfo::isUseTerrainShader() const
{
	return m_bUseTerrainShader;
}

bool CvLandscapeInfo::isUseLightmap() const
{
	return m_bUseLightmap;
}
float CvLandscapeInfo::getPeakScale() const
{
	return 	m_fPeakScale;
}

float CvLandscapeInfo::getHillScale() const
{
	return 	m_fHillScale;
}

bool CvLandscapeInfo::isRandomMap() const
{
	return m_bRandomMap;
}

const TCHAR* CvLandscapeInfo::getSkyArt()
{
	return m_szSkyArt;
}

void CvLandscapeInfo::setSkyArt(const TCHAR* szPath)
{
	m_szSkyArt = szPath;
}

const TCHAR* CvLandscapeInfo::getHeightMap()
{
	return m_szHeightMap;
}

void CvLandscapeInfo::setHeightMap(const TCHAR* szPath)
{
	m_szHeightMap = szPath;
}

const TCHAR* CvLandscapeInfo::getTerrainMap()
{
	return m_szTerrainMap;
}

void CvLandscapeInfo::setTerrainMap(const TCHAR* szPath)
{
	m_szTerrainMap = szPath;
}

const TCHAR* CvLandscapeInfo::getNormalMap()
{
	return m_szNormalMap;
}

void CvLandscapeInfo::setNormalMap(const TCHAR* szPath)
{
	m_szNormalMap = szPath;
}

const TCHAR* CvLandscapeInfo::getBlendMap()
{
	return m_szBlendMap;
}

void CvLandscapeInfo::setBlendMap(const TCHAR* szPath)
{
	m_szBlendMap = szPath;
}

bool CvLandscapeInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
		return false;

	pXML->GetChildXmlValByName(&m_iWaterHeight, "iWaterHeight");
	pXML->GetChildXmlValByName(&m_bRandomMap, "bRandomMap");

	CvString szTextVal;

	pXML->GetChildXmlValByName(szTextVal, "HeightMap");
	setHeightMap(szTextVal);

	pXML->GetChildXmlValByName(szTextVal, "TerrainMap");
	setTerrainMap(szTextVal);

	pXML->GetChildXmlValByName(szTextVal, "NormalMap");
	setNormalMap(szTextVal);

	pXML->GetChildXmlValByName(szTextVal, "BlendMap");
	setBlendMap(szTextVal);

	pXML->GetChildXmlValByName(szTextVal, "SkyArt");
	setSkyArt(szTextVal);

	pXML->GetChildXmlValByName(&m_iFogR, "iFogR");
	pXML->GetChildXmlValByName(&m_iFogG, "iFogG");
	pXML->GetChildXmlValByName(&m_iFogB, "iFogB");

	pXML->GetChildXmlValByName(&m_fTextureScaleX, "fTextureScaleX");
	pXML->GetChildXmlValByName(&m_fTextureScaleY, "fTextureScaleY");

	pXML->GetChildXmlValByName(&m_iHorizontalGameCell, "iGameCellSizeX");
	pXML->GetChildXmlValByName(&m_iVerticalGameCell, "iGameCellSizeY");

	pXML->GetChildXmlValByName(&m_iPlotsPerCellX, "iPlotsPerCellX");
	pXML->GetChildXmlValByName(&m_iPlotsPerCellY, "iPlotsPerCellY");

	m_iHorizontalVertCnt = m_iPlotsPerCellX * m_iHorizontalGameCell - (m_iPlotsPerCellX - 1);
	m_iVerticalVertCnt   = m_iPlotsPerCellY * m_iVerticalGameCell - (m_iPlotsPerCellY - 1);

	pXML->GetChildXmlValByName(&m_fZScale, "fZScale");
	pXML->GetChildXmlValByName(&m_bUseTerrainShader, "bTerrainShader");
	pXML->GetChildXmlValByName(&m_bUseLightmap, "bUseLightmap");
	pXML->GetChildXmlValByName(&m_fPeakScale, "fPeakScale");
	pXML->GetChildXmlValByName(&m_fHillScale, "fHillScale");

	return true;
}

int CvGameText::NUM_LANGUAGES = 0; // static

int CvGameText::getNumLanguages() const
{
	return NUM_LANGUAGES;
}
void CvGameText::setNumLanguages(int iNum)
{
	NUM_LANGUAGES = iNum;
}

CvGameText::CvGameText() :
	m_szGender("N"),
	m_szPlural("false")
{}

const wchar* CvGameText::getText() const
{
	return m_szText;
}

void CvGameText::setText(const wchar* szText)
{
	m_szText = szText;
}

// K-Mod. I've rewritten most of this function to change the way we find the appropriate language.
bool CvGameText::read(CvXMLLoadUtility* pXML, const std::string& language_name)
{
	if (!CvInfoBase::read(pXML))
		return false;

	gDLL->getXMLIFace()->SetToChild(pXML->GetXML());
	pXML->GetXmlVal(m_szType); // TAG

	//static const int iMaxNumLanguages = GC.getDefineINT("MAX_NUM_LANGUAGES");
	//int iNumLanguages = NUM_LANGUAGES ? NUM_LANGUAGES : iMaxNumLanguages + 1;

	// K-Mod
	bool bValid = false;
	if (!language_name.empty())
	{
		FAssert(getNumLanguages() > 0);
		// again, a big wtf to the original devs for not making the argument const.
		if (gDLL->getXMLIFace()->LocateFirstSiblingNodeByTagName(pXML->GetXML(), const_cast<TCHAR*>(language_name.c_str())))
			bValid = true;
		else
		{
			// if the language string is set, but we can't find it, use language #0.
			if (pXML->SkipToNextVal() && gDLL->getXMLIFace()->NextSibling(pXML->GetXML()))
				bValid = true;
		}
	}
	else
	{
		// otherwise, if the language string has not been set, just count until we get to our language number.
		// Note: if the langauge_name isn't set, the maybe the number of language isn't set either. (in the original code, it was determined here.)
		// So lets set it now.
		int iNumLanguages = getNumLanguages();
		if (iNumLanguages <= 0)
		{
			iNumLanguages = std::min(gDLL->getXMLIFace()->GetNumSiblings(pXML->GetXML()), GC.getDefineINT("MAX_NUM_LANGUAGES"));
			setNumLanguages(iNumLanguages);
		}

		for (int j = 0; j < iNumLanguages; j++)
		{
			if (!pXML->SkipToNextVal() || !gDLL->getXMLIFace()->NextSibling(pXML->GetXML()))
				break;

			if (j == GAMETEXT.getCurrentLanguage()) // Only add appropriate language Text
			{
				bValid = true;
				break;
			}
		}
	}
	// K-Mod. the setting of the text, moved from above.
	if (bValid)
	{
		CvWString wszTextVal;
		// TEXT
		if (pXML->GetChildXmlValByName(wszTextVal, "Text", /* advc.006b: */ L""))
		{
			setText(wszTextVal);
		}
		else
		{
			pXML->GetXmlVal(wszTextVal);
			setText(wszTextVal);
		}

		// GENDER
		if (pXML->GetChildXmlValByName(wszTextVal, "Gender", /* advc.006b: */ L""))
		{
			setGender(wszTextVal);
		}

		// PLURAL
		if (pXML->GetChildXmlValByName(wszTextVal, "Plural", /* advc.006b: */ L""))
		{
			setPlural(wszTextVal);
		}
	}

	gDLL->getXMLIFace()->SetToParent(pXML->GetXML()); // Move back up to Parent

	return bValid;
}


CvDiplomacyTextInfo::CvDiplomacyTextInfo() :
m_iNumResponses(0),
m_pResponses(NULL)
{}

// note - Response member vars allocated by CvXmlLoadUtility
void CvDiplomacyTextInfo::init(int iNum)
{
	uninit();
	m_pResponses = new Response[iNum];
	m_iNumResponses=iNum;
}

void CvDiplomacyTextInfo::uninit()
{
	SAFE_DELETE_ARRAY(m_pResponses);
}

int CvDiplomacyTextInfo::getNumResponses() const
{
	return m_iNumResponses;
}

bool CvDiplomacyTextInfo::getCivilizationTypes(int i, int j) const
{
	FAssertBounds(0, getNumResponses(), i);
	FAssertBounds(0, GC.getNumCivilizationInfos(), j);
	return (m_pResponses[i].m_pbCivilizationTypes[j] == NULL ? false : // advc.003t
			m_pResponses[i].m_pbCivilizationTypes[j]);
}

bool CvDiplomacyTextInfo::getLeaderHeadTypes(int i, int j) const
{
	FAssertBounds(0, getNumResponses(), i);
	FAssertBounds(0, GC.getNumLeaderHeadInfos(), j);
	return (m_pResponses[i].m_pbLeaderHeadTypes[j] == NULL ? false : // advc.003t
			m_pResponses[i].m_pbLeaderHeadTypes[j]);
}

bool CvDiplomacyTextInfo::getAttitudeTypes(int i, int j) const
{
	FAssertBounds(0, getNumResponses(), i);
	FAssertBounds(0, NUM_ATTITUDE_TYPES, j);
	return (m_pResponses[i].m_pbAttitudeTypes[j] == NULL ? false : // advc.003t
			m_pResponses[i].m_pbAttitudeTypes[j]);
}

bool CvDiplomacyTextInfo::getDiplomacyPowerTypes(int i, int j) const
{
	FAssertBounds(0, getNumResponses(), i);
	FAssertBounds(0, NUM_DIPLOMACYPOWER_TYPES, j);
	return (m_pResponses[i].m_pbDiplomacyPowerTypes[j] == NULL ? false : // advc.003t
			m_pResponses[i].m_pbDiplomacyPowerTypes[j]);
}

int CvDiplomacyTextInfo::getNumDiplomacyText(int i) const
{
	FAssertBounds(0, getNumResponses(), i);
	return m_pResponses[i].m_iNumDiplomacyText;
}

const TCHAR* CvDiplomacyTextInfo::getDiplomacyText(int i, int j) const
{
	FAssertBounds(0, getNumResponses(), i);
	FAssertBounds(0, getNumDiplomacyText(i), j);
	return m_pResponses[i].m_paszDiplomacyText[j];
}
#if ENABLE_XML_FILE_CACHE
void CvDiplomacyTextInfo::Response::read(FDataStreamBase* stream)
{
	stream->Read(&m_iNumDiplomacyText);
	SAFE_DELETE_ARRAY(m_pbCivilizationTypes);
	m_pbCivilizationTypes = new bool[GC.getNumCivilizationInfos()];
	stream->Read(GC.getNumCivilizationInfos(), m_pbCivilizationTypes);
	SAFE_DELETE_ARRAY(m_pbLeaderHeadTypes);
	m_pbLeaderHeadTypes = new bool[GC.getNumLeaderHeadInfos()];
	stream->Read(GC.getNumLeaderHeadInfos(), m_pbLeaderHeadTypes);
	SAFE_DELETE_ARRAY(m_pbAttitudeTypes);
	m_pbAttitudeTypes = new bool[NUM_ATTITUDE_TYPES];
	stream->Read(NUM_ATTITUDE_TYPES, m_pbAttitudeTypes);
	SAFE_DELETE_ARRAY(m_pbDiplomacyPowerTypes);
	m_pbDiplomacyPowerTypes = new bool[NUM_DIPLOMACYPOWER_TYPES];
	stream->Read(NUM_DIPLOMACYPOWER_TYPES, m_pbDiplomacyPowerTypes);
	SAFE_DELETE_ARRAY(m_paszDiplomacyText);
	m_paszDiplomacyText = new CvString[m_iNumDiplomacyText];
	stream->ReadString(m_iNumDiplomacyText, m_paszDiplomacyText);
}

void CvDiplomacyTextInfo::Response::write(FDataStreamBase* stream)
{
	stream->Write(m_iNumDiplomacyText);
	stream->Write(GC.getNumCivilizationInfos(), m_pbCivilizationTypes);
	stream->Write(GC.getNumLeaderHeadInfos(), m_pbLeaderHeadTypes);
	stream->Write(NUM_ATTITUDE_TYPES, m_pbAttitudeTypes);
	stream->Write(NUM_DIPLOMACYPOWER_TYPES, m_pbDiplomacyPowerTypes);
	stream->WriteString(m_iNumDiplomacyText, m_paszDiplomacyText);
}

void CvDiplomacyTextInfo::read(FDataStreamBase* stream)
{
	CvInfoBase::read(stream);
	uint uiFlag=0;
	stream->Read(&uiFlag);
	stream->Read(&m_iNumResponses);
	init(m_iNumResponses);
	for (uint uiIndex = 0; (int) uiIndex < m_iNumResponses; uiIndex++)
		m_pResponses[uiIndex].read(stream);
}

void CvDiplomacyTextInfo::write(FDataStreamBase* stream)
{
	CvInfoBase::write(stream);
	uint uiFlag=0;
	stream->Write(uiFlag);
	stream->Write(m_iNumResponses);
	for (uint uiIndex = 0; (int) uiIndex < m_iNumResponses; uiIndex++)
		m_pResponses[uiIndex].write(stream);
}
#endif
bool CvDiplomacyTextInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
		return false;

	CvString szTextVal;
	pXML->GetChildXmlValByName(szTextVal, "Type");

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"Responses"))
	{
		int iIndexVal = gDLL->getXMLIFace()->NumOfChildrenByTagName(pXML->GetXML(), "Response");
		// advc.006b: GetChildXmlValByName can't handle comments
		FAssertMsg(iIndexVal > 0, "XML comment inside Responses?");
		init(iIndexVal);

		for (int j = 0; j < iIndexVal; j++)
		{
			if (j == 0)
				gDLL->getXMLIFace()->SetToChild(pXML->GetXML());
			// Civilizations
			pXML->SetVariableListTagPair(&m_pResponses[j].m_pbCivilizationTypes, "Civilizations", GC.getNumCivilizationInfos());
			// Leaders
			pXML->SetVariableListTagPair(&m_pResponses[j].m_pbLeaderHeadTypes, "Leaders", GC.getNumLeaderHeadInfos());
			// AttitudeTypes
			pXML->SetVariableListTagPair(&m_pResponses[j].m_pbAttitudeTypes, "Attitudes", NUM_ATTITUDE_TYPES);
			// PowerTypes
			pXML->SetVariableListTagPair(&m_pResponses[j].m_pbDiplomacyPowerTypes, "DiplomacyPowers", NUM_DIPLOMACYPOWER_TYPES);
			// DiplomacyText
			if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"DiplomacyText"))
			{
				pXML->SetStringList(&m_pResponses[j].m_paszDiplomacyText, &m_pResponses[j].m_iNumDiplomacyText);
				gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
			}

			if (!gDLL->getXMLIFace()->NextSibling(pXML->GetXML()))
				break;
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	gDLL->getXMLIFace()->SetToParent(pXML->GetXML());

	return true;
}

CvEffectInfo::CvEffectInfo() :
m_fUpdateRate(0.0f),
m_bProjectile(false),
m_bSticky(false),
m_fProjectileSpeed(0.0f),
m_fProjectileArc(0.0f)
{}

// advc.xmldefault:
CvEffectInfo::CvEffectInfo(CvEffectInfo const& kOther)
{
	FErrorMsg("Copy-ctor not implemented");
}

bool CvEffectInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
		return false;

	CvScalableInfo::read(pXML);

	CvString szTextVal;
	pXML->GetChildXmlValByName(szTextVal, "Path");
	setPath(szTextVal);

	pXML->GetChildXmlValByName(&m_fUpdateRate, "fUpdateRate");

	int iTemporary;
	pXML->GetChildXmlValByName(&iTemporary, "bIsProjectile");
	m_bProjectile = iTemporary != 0;

	pXML->GetChildXmlValByName(&m_fProjectileSpeed, "fSpeed", /* advc.006b: */ 0);
	pXML->GetChildXmlValByName(&m_fProjectileArc, "fArcValue", /* advc.006b: */ 0);
	pXML->GetChildXmlValByName(&m_bSticky, "bSticky", false);
	return true;
}


CvAttachableInfo::CvAttachableInfo() : m_fUpdateRate(0.0f) {}
// advc.xmldefault:
CvAttachableInfo::CvAttachableInfo(CvAttachableInfo const& kOther)
{
	FErrorMsg("Copy-ctor not implemented");
}

bool CvAttachableInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
		return false;

	CvScalableInfo::read(pXML);

	CvString szTextVal;
	pXML->GetChildXmlValByName(szTextVal, "Path");
	setPath(szTextVal);

	return true;
}

/*bool CvCameraInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
		return false;

	CvString szTextVal;
	pXML->GetChildXmlValByName(szTextVal, "Path");
	setPath(szTextVal);

	return true;
}*/ // advc.003j: unused

// advc.003j: unused
/*CvQuestInfo::CvQuestInfo() :
m_iNumQuestMessages(0),
m_iNumQuestLinks(0),
m_iNumQuestSounds(0),
m_paszQuestMessages(NULL),
m_pQuestLinks(NULL),
m_paszQuestSounds(NULL)
{
	m_szQuestScript = "NONE";
}

CvQuestInfo::~CvQuestInfo()
{
	reset();
}

void CvQuestInfo::reset()
{
	CvInfoBase::reset();
	SAFE_DELETE_ARRAY(m_paszQuestMessages);
	SAFE_DELETE_ARRAY(m_pQuestLinks);
	SAFE_DELETE_ARRAY(m_paszQuestSounds);
}

bool CvQuestInfo::initQuestLinks(int iNum)
{
	reset();
	if (iNum > 0)
	{
		m_pQuestLinks = new QuestLink[iNum];
		m_iNumQuestLinks = iNum;
		return true;
	}
	return false;
}

const TCHAR* CvQuestInfo::getQuestObjective() const
{
	return m_szQuestObjective;
}

const TCHAR* CvQuestInfo::getQuestBodyText() const
{
	return m_szQuestBodyText;
}

int CvQuestInfo::getNumQuestMessages() const
{
	return m_iNumQuestMessages;
}

const TCHAR* CvQuestInfo::getQuestMessages(int iIndex) const
{
	return m_paszQuestMessages ? m_paszQuestMessages[iIndex] : "";
}

int CvQuestInfo::getNumQuestLinks() const
{
	return m_iNumQuestLinks;
}

const TCHAR* CvQuestInfo::getQuestLinkType(int iIndex)  const
{
	return m_pQuestLinks[iIndex].m_szQuestLinkType;
}

const TCHAR* CvQuestInfo::getQuestLinkName(int iIndex)  const
{
	return m_pQuestLinks[iIndex].m_szQuestLinkName;
}

int CvQuestInfo::getNumQuestSounds() const
{
	return m_iNumQuestSounds;
}

const TCHAR* CvQuestInfo::getQuestSounds(int iIndex) const
{
	return m_paszQuestSounds ? m_paszQuestSounds[iIndex] : "";
}

const TCHAR* CvQuestInfo::getQuestScript() const
{
	return m_szQuestScript;
}

void CvQuestInfo::setQuestObjective(const TCHAR* szText)
{
	m_szQuestObjective = szText;
}

void CvQuestInfo::setQuestBodyText(const TCHAR* szText)
{
	m_szQuestBodyText = szText;
}

void CvQuestInfo::setNumQuestMessages(int iNum)
{
	m_iNumQuestMessages = iNum;
}

void CvQuestInfo::setQuestMessages(int iIndex, const TCHAR* szText)
{
	m_paszQuestMessages[iIndex] = szText;
}

void CvQuestInfo::setNumQuestSounds(int iNum)
{
	m_iNumQuestSounds = iNum;
}

void CvQuestInfo::setQuestSounds(int iIndex, const TCHAR* szText)
{
	m_paszQuestSounds[iIndex] = szText;
}

void CvQuestInfo::setQuestScript(const TCHAR* szText)
{
	m_szQuestScript = szText;
}

bool CvQuestInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
		return false;

	CvString szTextVal;

	pXML->GetChildXmlValByName(szTextVal, "QuestObjective");
	setQuestObjective(szTextVal);

	pXML->GetChildXmlValByName(szTextVal, "QuestBodyText");
	setQuestBodyText(szTextVal);

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "QuestMessages"))
	{
		pXML->SetStringList(&m_paszQuestMessages, &m_iNumQuestMessages);
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"QuestLinks"))
	{
		int iNum;
		iNum = gDLL->getXMLIFace()->NumOfChildrenByTagName(pXML->GetXML(), "QuestLink");

		if (initQuestLinks(iNum))
		{
			for (int i = 0; i<m_iNumQuestLinks; i++)
			{
				pXML->GetChildXmlValByName(szTextVal, "QuestLinkType");
				m_pQuestLinks[i].m_szQuestLinkType = szTextVal;

				pXML->GetChildXmlValByName(szTextVal, "QuestLinkName");
				m_pQuestLinks[i].m_szQuestLinkName = szTextVal;

				if (!gDLL->getXMLIFace()->NextSibling(pXML->GetXML()))
					break;
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "QuestSounds"))
	{
		pXML->SetStringList(&m_paszQuestSounds, &m_iNumQuestSounds);
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	pXML->GetChildXmlValByName(szTextVal, "QuestScript");
	setQuestScript(szTextVal);

	return true;
}*/

CvTutorialMessage::CvTutorialMessage() :
m_iNumTutorialScripts(0),
m_paszTutorialScripts(NULL)
{
	m_szTutorialMessageText = "No Text";
	m_szTutorialMessageImage = "No Text";
	m_szTutorialMessageSound = "No Text";
}

CvTutorialMessage::~CvTutorialMessage()
{
	SAFE_DELETE_ARRAY(m_paszTutorialScripts);
}

const TCHAR* CvTutorialMessage::getText() const
{
	return m_szTutorialMessageText;
}

const TCHAR* CvTutorialMessage::getImage() const
{
	return m_szTutorialMessageImage;
}

const TCHAR* CvTutorialMessage::getSound() const
{
	return m_szTutorialMessageSound;
}

int CvTutorialMessage::getNumTutorialScripts() const
{
	return m_iNumTutorialScripts;
}

const TCHAR* CvTutorialMessage::getTutorialScriptByIndex(int i) const
{
	return m_paszTutorialScripts[i];
}

bool CvTutorialMessage::read(CvXMLLoadUtility* pXML)
{
	if (!pXML->SkipToNextVal())
		return false;

	pXML->MapChildren(); // try to hash children for fast lookup by name
	pXML->GetChildXmlValByName(m_szTutorialMessageText, "TutorialMessageText");
	pXML->GetChildXmlValByName(m_szTutorialMessageImage, "TutorialMessageImage");
	pXML->GetChildXmlValByName(m_szTutorialMessageSound, "TutorialMessageSound");

	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "TutorialScripts"))
	{
		pXML->SetStringList(&m_paszTutorialScripts, &m_iNumTutorialScripts);
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	return true;
}

CvTutorialInfo::CvTutorialInfo() :
m_iNumTutorialMessages(0),
m_paTutorialMessages(NULL)
{
	m_szNextTutorialInfoType = "NONE";
}

CvTutorialInfo::~CvTutorialInfo()
{
	resetMessages();
}

const TCHAR* CvTutorialInfo::getNextTutorialInfoType()
{
	return m_szNextTutorialInfoType;
}

bool CvTutorialInfo::initTutorialMessages(int iNum)
{
	resetMessages();
	m_paTutorialMessages = new CvTutorialMessage[iNum];
	m_iNumTutorialMessages = iNum;
	return true;
}

void CvTutorialInfo::resetMessages()
{
	SAFE_DELETE_ARRAY(m_paTutorialMessages);
	m_iNumTutorialMessages = 0;
}

int CvTutorialInfo::getNumTutorialMessages() const
{
	return m_iNumTutorialMessages;
}

const CvTutorialMessage* CvTutorialInfo::getTutorialMessage(int iIndex) const
{
	return &m_paTutorialMessages[iIndex];
}

bool CvTutorialInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
		return false;

	pXML->MapChildren(); // try to hash children for fast lookup by name
	pXML->GetChildXmlValByName(m_szNextTutorialInfoType, "NextTutorialInfoType", /* advc.006b: */ "");
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"TutorialMessages"))
	{
		int iNum = gDLL->getXMLIFace()->NumOfChildrenByTagName(pXML->GetXML(), "TutorialMessage");
		if (iNum > 0)
		{
			gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"TutorialMessage");
			initTutorialMessages(iNum);
			for (int i = 0; i<m_iNumTutorialMessages; i++)
			{
				if (!m_paTutorialMessages[i].read(pXML))
					return false;

				if (!gDLL->getXMLIFace()->NextSibling(pXML->GetXML()))
					break;
			}
			gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	return true;
}

CvForceControlInfo::CvForceControlInfo() : m_bDefault(false) {}

bool CvForceControlInfo::getDefault() const
{
	return m_bDefault;
}

bool CvForceControlInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
		return false;
	pXML->GetChildXmlValByName(&m_bDefault, "bDefault");
	return true;
}

CvPlayerOptionInfo::CvPlayerOptionInfo() : m_bDefault(false) {}


bool CvPlayerOptionInfo::getDefault() const
{
	return m_bDefault;
}

bool CvPlayerOptionInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
		return false;

	pXML->GetChildXmlValByName(&m_bDefault, "bDefault");
	return true;
}

CvGraphicOptionInfo::CvGraphicOptionInfo() : m_bDefault(false) {}

bool CvGraphicOptionInfo::getDefault() const
{
	return m_bDefault;
}

bool CvGraphicOptionInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
		return false;
	pXML->GetChildXmlValByName(&m_bDefault, "bDefault");
	return true;
}

std::string CvMainMenuInfo::getScene() const
{
	return m_szScene;
}

std::string CvMainMenuInfo::getSceneNoShader() const
{
	return m_szSceneNoShader;
}

std::string CvMainMenuInfo::getSoundtrack() const
{
	return m_szSoundtrack;
}

std::string CvMainMenuInfo::getLoading() const
{
	return m_szLoading;
}

std::string CvMainMenuInfo::getLoadingSlideshow() const
{
	return m_szLoadingSlideshow;
}

bool CvMainMenuInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
		return false;

	pXML->GetChildXmlValByName(m_szScene, "Scene");
	pXML->GetChildXmlValByName(m_szSceneNoShader, "SceneNoShader");
	pXML->GetChildXmlValByName(m_szSoundtrack, "Soundtrack");
	pXML->GetChildXmlValByName(m_szLoading, "Loading");
	pXML->GetChildXmlValByName(m_szLoadingSlideshow, "LoadingSlideshow");

	return true;
}
