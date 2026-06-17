#include "CvGameCoreDLL.h"
#include "CvDllPythonEvents.h"
#include "CvDLLPythonIFaceBase.h"
#include "CvGame.h"
#include "CvPlot.h"
#include "CvSelectionGroup.h"
#include "CvUnit.h"

/*  <advc.003y> Move the callback defines from CvGlobals to where they are used
	(i.e. move some here and the rest to CvPythonCaller). */
/*  See CvGlobals.h about this macro. Would like to add more, but most of the
	callbacks are actually in use - by Autolog, EventSigns or Civ4lerts. */
#define DO_FOR_EACH_CALLBACK_DEFINE(DO) \
	DO(ON_UPDATE) \
	DO(ON_UNIT_SET_XY) \
	DO(ON_UNIT_SELECTED) \
	DO(ON_UNIT_CREATED) \
	DO(ON_UNIT_LOST) \
	/* New additions (callbacks unused in BtS/AdvCiv) */ \
	DO(ROUTE_BUILT) \
	DO(UNIT_MOVE) \
	DO(UNIT_BUILD_IMPROVEMENT) \
	/* </advc> */
enum CallbackDefines
{
	DO_FOR_EACH_CALLBACK_DEFINE(MAKE_ENUMERATOR)
	NUM_CALLBACK_DEFINES
};
#define MAKE_STRING(VAR) "USE_"#VAR"_CALLBACK",

CvDllPythonEvents::CvDllPythonEvents() : m_abUseCallback(NULL) {}

CvDllPythonEvents::~CvDllPythonEvents()
{
	SAFE_DELETE_ARRAY(m_abUseCallback);
}

void CvDllPythonEvents::initCallbackGuards()
{
	// Duplicate code unfortunately (cf. CvPythonCaller)
	const char* const aszGlobalCallbackTagNames[] = {
		DO_FOR_EACH_CALLBACK_DEFINE(MAKE_STRING)
	};
	FAssert(sizeof(aszGlobalCallbackTagNames) / sizeof(char*) == NUM_CALLBACK_DEFINES);
	m_abUseCallback = new bool[NUM_CALLBACK_DEFINES];
	for (int i = 0; i < NUM_CALLBACK_DEFINES; i++)
		m_abUseCallback[i] = GC.getDefineBOOL(aszGlobalCallbackTagNames[i]);
} // </advc.003y>

bool CvDllPythonEvents::preEvent()
{
	return gDLL->getPythonIFace()->isInitialized();
}

bool CvDllPythonEvents::postEvent(CyArgsList& eventData)
{
	eventData.add(GC.getGame().isDebugMode());
	eventData.add(false);
	eventData.add(GC.altKey());
	eventData.add(GC.ctrlKey());
	eventData.add(GC.shiftKey());
	eventData.add(gDLL->getChtLvl() > 0 ||
			GC.getGame().isDebugMode()); // advc.135c

	long lResult = -1;
	bool bOK = gDLL->getPythonIFace()->callFunction(PYEventModule, "onEvent", eventData.makeFunctionArgs(), &lResult);

	return (bOK && lResult==1);
}

bool CvDllPythonEvents::reportKbdEvent(int evt, int key, int iCursorX, int iCursorY)
{
	if (preEvent())
	{
		NiPoint3 pt3Location;
		CvPlot* pPlot = gDLL->getEngineIFace()->pickPlot(iCursorX, iCursorY, pt3Location);
		CyArgsList eventData;
		eventData.add("kbdEvent");
		eventData.add(evt);
		eventData.add(key);
		eventData.add(iCursorX);
		eventData.add(iCursorY);
		eventData.add(pPlot ? pPlot->getX() : -1);
		eventData.add(pPlot ? pPlot->getY() : -1);

		return postEvent(eventData);
	}
	return false;
}

bool CvDllPythonEvents::reportMouseEvent(int evt, int iCursorX, int iCursorY, bool bInterfaceConsumed)
{
	if (preEvent())
	{
		NiPoint3 pt3Location;
		CvPlot* pPlot = gDLL->getEngineIFace()->pickPlot(iCursorX, iCursorY, pt3Location);
		CyArgsList eventData;
		eventData.add("mouseEvent");				// add key to lookup python handler fxn
		eventData.add(evt);
		eventData.add(iCursorX);
		eventData.add(iCursorY);
		eventData.add(pPlot ? pPlot->getX() : -1);
		eventData.add(pPlot ? pPlot->getY() : -1);
		eventData.add(bInterfaceConsumed);

		// add list of active screens
		std::vector<int> screens;
		gDLL->UI().getInterfaceScreenIdsForInput(screens);
		eventData.add(screens.size() ? &screens[0] : NULL, screens.size());

		return postEvent(eventData);
	}
	return false;
}

void CvDllPythonEvents::reportModNetMessage(int iData1, int iData2, int iData3, int iData4, int iData5)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("ModNetMessage");				// add key to lookup python handler fxn
		eventData.add(iData1);
		eventData.add(iData2);
		eventData.add(iData3);
		eventData.add(iData4);
		eventData.add(iData5);
		postEvent(eventData);
	}
}

void CvDllPythonEvents::reportInit()
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("Init");				// add key to lookup python handler fxn
		postEvent(eventData);
	}
}

void CvDllPythonEvents::reportUpdate(float fDeltaTime)
{	// <advc.003y>
	if (!isUse(ON_UPDATE))
		return; // </advc.003y>
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("Update");				// add key to lookup python handler fxn
		eventData.add(fDeltaTime);
		postEvent(eventData);
	}
}

void CvDllPythonEvents::reportUnInit()
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("UnInit");				// add key to lookup python handler fxn
		postEvent(eventData);
	}
}

void CvDllPythonEvents::reportGameStart()
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("GameStart");				// add key to lookup python handler fxn
		postEvent(eventData);
	}
}

void CvDllPythonEvents::reportGameEnd()
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("GameEnd");				// add key to lookup python handler fxn
		postEvent(eventData);
	}
}


void CvDllPythonEvents::reportWindowActivation(bool bActive)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("windowActivation");
		eventData.add(bActive);
		postEvent(eventData);
	}
}

void CvDllPythonEvents::reportBeginGameTurn(int iGameTurn)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("BeginGameTurn");				// add key to lookup python handler fxn
		eventData.add(iGameTurn);
		postEvent(eventData);
	}
}

void CvDllPythonEvents::reportEndGameTurn(int iGameTurn)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("EndGameTurn");				// add key to lookup python handler fxn
		eventData.add(iGameTurn);
		postEvent(eventData);
	}
}

void CvDllPythonEvents::reportBeginPlayerTurn(int iGameTurn, PlayerTypes ePlayer)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("BeginPlayerTurn");				// add key to lookup python handler fxn
		eventData.add(iGameTurn);
		eventData.add(ePlayer);
		postEvent(eventData);
	}
}

void CvDllPythonEvents::reportEndPlayerTurn(int iGameTurn, PlayerTypes ePlayer)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("EndPlayerTurn");				// add key to lookup python handler fxn
		eventData.add(iGameTurn);
		eventData.add(ePlayer);
		postEvent(eventData);
	}
}

void CvDllPythonEvents::reportFirstContact(TeamTypes eTeamID1, TeamTypes eTeamID2)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("firstContact");				// add key to lookup python handler fxn
		eventData.add(eTeamID1);
		eventData.add(eTeamID2);
		postEvent(eventData);
	}
}

// doc: restored contact event
void CvDllPythonEvents::reportRestoredContact(TeamTypes eTeamID1, TeamTypes eTeamID2)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("restoredContact");
		eventData.add((int)eTeamID1);
		eventData.add((int)eTeamID2);
		postEvent(eventData);
	}
}

void CvDllPythonEvents::reportCombatResult(CvUnit* pWinner, CvUnit* pLoser)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("combatResult");				// add key to lookup python handler fxn

		CyUnit* pCyWinner = new CyUnit(pWinner);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyWinner));

		CyUnit* pCyLoser = new CyUnit(pLoser);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyLoser));

		postEvent(eventData);
		delete pCyLoser;
		delete pCyWinner;
	}
}

void CvDllPythonEvents::reportImprovementBuilt(int iImprovementType, int iX, int iY)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("improvementBuilt");				// add key to lookup python handler fxn
		eventData.add(iImprovementType);
		eventData.add(iX);
		eventData.add(iY);
		postEvent(eventData);
	}
}

void CvDllPythonEvents::reportImprovementDestroyed(int iImprovementType, int iPlayer, int iX, int iY)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("improvementDestroyed");				// add key to lookup python handler fxn
		eventData.add(iImprovementType);
		eventData.add(iPlayer);
		eventData.add(iX);
		eventData.add(iY);
		postEvent(eventData);
	}
}

void CvDllPythonEvents::reportRouteBuilt(int iRouteType, int iX, int iY)
{	// <advc.003y>
	if (!isUse(ROUTE_BUILT))
		return; // </advc.003y>
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("routeBuilt");				// add key to lookup python handler fxn
		eventData.add(iRouteType);
		eventData.add(iX);
		eventData.add(iY);
		postEvent(eventData);
	}
}

void CvDllPythonEvents::reportChat(CvWString szString)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("chat");							// add key to lookup python handler fxn
		eventData.add(szString);
		postEvent(eventData);
	}
}

void CvDllPythonEvents::reportPlotRevealed(CvPlot *pPlot, TeamTypes eTeam)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("plotRevealed");						// add key to lookup python handler fxn

		CyPlot* pCyPlot = new CyPlot(pPlot);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyPlot));
		eventData.add(eTeam);

		postEvent(eventData);
		delete pCyPlot;
	}
}

void CvDllPythonEvents::reportPlotFeatureRemoved(CvPlot *pPlot, FeatureTypes eFeature, CvCity* pCity)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("plotFeatureRemoved");						// add key to lookup python handler fxn

		CyPlot* pCyPlot = new CyPlot(pPlot);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyPlot));
		CyCity* pCyCity= new CyCity(pCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyCity));
		eventData.add(eFeature);

		postEvent(eventData);
		delete pCyPlot;
		delete pCyCity;
	}
}

void CvDllPythonEvents::reportPlotPicked(CvPlot *pPlot)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("plotPicked");						// add key to lookup python handler fxn

		CyPlot* pCyPlot = new CyPlot(pPlot);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyPlot));

		postEvent(eventData);
		delete pCyPlot;
	}
}

void CvDllPythonEvents::reportNukeExplosion(CvPlot *pPlot, CvUnit* pNukeUnit)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("nukeExplosion");						// add key to lookup python handler fxn

		CyPlot* pCyPlot = new CyPlot(pPlot);
		CyUnit* pCyUnit = new CyUnit(pNukeUnit);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyPlot));
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyUnit));

		postEvent(eventData);
		delete pCyPlot;
		delete pCyUnit;
	}
}

void CvDllPythonEvents::reportGotoPlotSet(CvPlot *pPlot, PlayerTypes ePlayer)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("gotoPlotSet");						// add key to lookup python handler fxn

		CyPlot* pCyPlot = new CyPlot(pPlot);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyPlot));
		eventData.add(ePlayer);

		postEvent(eventData);
		delete pCyPlot;
	}
}

void CvDllPythonEvents::reportCityBuilt(CvCity *pCity)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("cityBuilt");						// add key to lookup python handler fxn

		CyCity* pCyCity = new CyCity(pCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyCity));

		postEvent(eventData);
		delete pCyCity;
	}
}

void CvDllPythonEvents::reportCityRazed(CvCity *pCity, PlayerTypes ePlayer)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("cityRazed");						// add key to lookup python handler fxn

		CyCity* pCyCity = new CyCity(pCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyCity));
		eventData.add(ePlayer);

		postEvent(eventData);
		delete pCyCity;
	}
}

void CvDllPythonEvents::reportCityAcquired(PlayerTypes eOldOwner, PlayerTypes ePlayer, CvCity* pOldCity, bool bConquest, bool bTrade)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("cityAcquired");					// add key to lookup python handler fxn
		eventData.add(eOldOwner);
		eventData.add(ePlayer);

		CyCity* pCyCity = new CyCity(pOldCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyCity));

		eventData.add(bConquest);
		eventData.add(bTrade);
		postEvent(eventData);
		delete pCyCity;
	}
}

void CvDllPythonEvents::reportCityAcquiredAndKept(PlayerTypes ePlayer, CvCity* pOldCity)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("cityAcquiredAndKept");					// add key to lookup python handler fxn
		eventData.add(ePlayer);

		CyCity* pCyCity = new CyCity(pOldCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyCity));

		postEvent(eventData);
		delete pCyCity;
	}
}

void CvDllPythonEvents::reportCityLost(CvCity* pCity)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("cityLost");						// add key to lookup python handler fxn

		CyCity* pyu = new CyCity(pCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pyu));
		postEvent(eventData);
		delete pyu;
	}
}

// doc: city gifted event
void CvDllPythonEvents::reportCityGifted(CvCity* pCity)
{
    if (preEvent())
    {
        CyArgsList eventData;
        eventData.add("cityGifted");

        CyCity* pyu = new CyCity(pCity);
        eventData.add(gDLL->getPythonIFace()->makePythonObject(pyu));
        postEvent(eventData);
        delete pyu;
    }
}

// doc: city liberated event
void CvDllPythonEvents::reportCityLiberated(CvCity* pCity)
{
    if (preEvent())
    {
        CyArgsList eventData;
        eventData.add("cityLiberated");

        CyCity* pyu = new CyCity(pCity);
        eventData.add(gDLL->getPythonIFace()->makePythonObject(pyu));
        postEvent(eventData);
        delete pyu;
    }
}

void CvDllPythonEvents::reportCultureExpansion(CvCity *pCity, PlayerTypes ePlayer)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("cultureExpansion");						// add key to lookup python handler fxn

		CyCity* pCyCity = new CyCity(pCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyCity));

		eventData.add(ePlayer);

		postEvent(eventData);
		delete pCyCity;
	}
}

void CvDllPythonEvents::reportCityGrowth(CvCity *pCity, PlayerTypes ePlayer)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("cityGrowth");						// add key to lookup python handler fxn

		CyCity* pCyCity = new CyCity(pCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyCity));

		eventData.add(ePlayer);

		postEvent(eventData);
		delete pCyCity;
	}
}

void CvDllPythonEvents::reportCityProduction(CvCity *pCity, PlayerTypes ePlayer)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("cityDoTurn");						// add key to lookup python handler fxn

		CyCity* pCyCity = new CyCity(pCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyCity));

		eventData.add(ePlayer);

		postEvent(eventData);
		delete pCyCity;
	}
}

void CvDllPythonEvents::reportCityBuildingUnit(CvCity *pCity, UnitTypes eUnitType)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("cityBuildingUnit");						// add key to lookup python handler fxn

		CyCity* pCyCity = new CyCity(pCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyCity));

		eventData.add(eUnitType);

		postEvent(eventData);
		delete pCyCity;
	}
}

void CvDllPythonEvents::reportCityBuildingBuilding(CvCity *pCity, BuildingTypes eBuildingType)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("cityBuildingBuilding");						// add key to lookup python handler fxn

		CyCity* pCyCity = new CyCity(pCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyCity));

		eventData.add(eBuildingType);

		postEvent(eventData);
		delete pCyCity;
	}
}

void CvDllPythonEvents::reportCityRename(CvCity *pCity)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("cityRename");						// add key to lookup python handler fxn

		CyCity* pCyCity = new CyCity(pCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyCity));

		postEvent(eventData);
		delete pCyCity;
	}
}

void CvDllPythonEvents::reportCityHurry(CvCity *pCity, HurryTypes eHurry)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("cityHurry");						// add key to lookup python handler fxn

		CyCity* pCyCity = new CyCity(pCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyCity));

		eventData.add(eHurry);

		postEvent(eventData);
		delete pCyCity;
	}
}

// doc: city capture gold event
void CvDllPythonEvents::reportCityCaptureGold(CvCity *pCity, PlayerTypes ePlayer, int iCaptureGold)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("cityCaptureGold");

		CyCity* pCyCity = new CyCity(pCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyCity));

		eventData.add(ePlayer);
		eventData.add(iCaptureGold);

		postEvent(eventData);
		delete pCyCity;
	}
}

void CvDllPythonEvents::reportSelectionGroupPushMission(CvSelectionGroup* pSelectionGroup, MissionTypes eMission)
{
	if (pSelectionGroup == NULL)
		return;

	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("selectionGroupPushMission");						// add key to lookup python handler fxn
		eventData.add(pSelectionGroup->getOwner());
		eventData.add(eMission);
		int iNumUnits = pSelectionGroup->getNumUnits();
		eventData.add(iNumUnits);

		int* aiUnitIds = new int[iNumUnits];
		CLLNode<IDInfo> const* pUnitNode = pSelectionGroup->headUnitNode();
		for (int i = 0; pUnitNode != NULL; i++)
		{
			CvUnit* pLoopUnit = CvUnit::fromIDInfo(pUnitNode->m_data);
			pUnitNode = pSelectionGroup->nextUnitNode(pUnitNode);
			aiUnitIds[i] = pLoopUnit->getID();
			FAssert(i < iNumUnits);
		}

		if (aiUnitIds != NULL)
			eventData.add(aiUnitIds, iNumUnits);

		postEvent(eventData);

		delete[] aiUnitIds; // kmodx: Memory leak
	}
}

void CvDllPythonEvents::reportUnitMove(CvPlot* pPlot, CvUnit* pUnit, CvPlot* pOldPlot)
{	// <advc.003y>
	if (!isUse(UNIT_MOVE))
		return; // </advc.003y>
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("unitMove");						// add key to lookup python handler fxn

		CyPlot* py = new CyPlot(pPlot);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(py));

		CyUnit* pyu = new CyUnit(pUnit);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pyu));

		CyPlot* pyOld = new CyPlot(pOldPlot);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pyOld));

		postEvent(eventData);

		delete py;
		delete pyu;
		delete pyOld;
	}
}

void CvDllPythonEvents::reportUnitSetXY(CvPlot* pPlot, CvUnit* pUnit)
{	// <advc.003y>
	if (!isUse(ON_UNIT_SET_XY))
		return; // </advc.003y>
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("unitSetXY");						// add key to lookup python handler fxn

		CyPlot* py = new CyPlot(pPlot);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(py));

		CyUnit* pyu = new CyUnit(pUnit);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pyu));

		postEvent(eventData);

		delete py;
		delete pyu;
	}
}

void CvDllPythonEvents::reportUnitCreated(CvUnit* pUnit)
{	// <advc.003y>
	if (!isUse(ON_UNIT_CREATED))
		return; // </advc.003y>
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("unitCreated");						// add key to lookup python handler fxn

		CyUnit* pyu = new CyUnit(pUnit);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pyu));
		postEvent(eventData);
		delete pyu;
	}
}

void CvDllPythonEvents::reportUnitBuilt(CvCity *pCity, CvUnit* pUnit)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("unitBuilt");						// add key to lookup python handler fxn

		CyCity* pyc = new CyCity(pCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pyc));

		CyUnit* pyu = new CyUnit(pUnit);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pyu));

		postEvent(eventData);

		delete pyc;
		delete pyu;
	}
}

void CvDllPythonEvents::reportUnitKilled(CvUnit* pUnit, PlayerTypes eAttacker)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("unitKilled");						// add key to lookup python handler fxn

		CyUnit* pyu = new CyUnit(pUnit);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pyu));
		eventData.add(eAttacker);
		postEvent(eventData);
		delete pyu;
	}
}

void CvDllPythonEvents::reportUnitLost(CvUnit* pUnit)
{	// <advc.003y>
	if (!isUse(ON_UNIT_LOST))
		return; // </advc.003y>
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("unitLost");						// add key to lookup python handler fxn

		CyUnit* pyu = new CyUnit(pUnit);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pyu));
		postEvent(eventData);
		delete pyu;
	}
}

void CvDllPythonEvents::reportUnitPromoted(CvUnit* pUnit, PromotionTypes ePromotion)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("unitPromoted");						// add key to lookup python handler fxn

		CyUnit* pyu = new CyUnit(pUnit);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pyu));
		eventData.add(ePromotion);
		postEvent(eventData);
		delete pyu;
	}
}

void CvDllPythonEvents::reportUnitSelected(CvUnit* pUnit)
{	// <advc.003y>
	if (!isUse(ON_UNIT_SELECTED))
		return; // </advc.003y>
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("unitSelected");						// add key to lookup python handler fxn

		CyUnit* pyu = new CyUnit(pUnit);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pyu));
		postEvent(eventData);
		delete pyu;
	}
}

void CvDllPythonEvents::reportUnitRename(CvUnit *pUnit)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("UnitRename");						// add key to lookup python handler fxn

		CyUnit* pCyUnit = new CyUnit(pUnit);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyUnit));

		postEvent(eventData);
		delete pCyUnit;
	}
}

void CvDllPythonEvents::reportUnitPillage(CvUnit* pUnit, ImprovementTypes eImprovement, RouteTypes eRoute, PlayerTypes ePlayer, int iPillagedGold)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("unitPillage");						// add key to lookup python handler fxn

		CyUnit* pCyUnit = new CyUnit(pUnit);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyUnit));
		eventData.add(eImprovement);
		eventData.add(eRoute);
		eventData.add(ePlayer);
		eventData.add(iPillagedGold); // doc: include pillaged gold

		postEvent(eventData);
		delete pCyUnit;
	}
}

void CvDllPythonEvents::reportUnitSpreadReligionAttempt(CvUnit* pUnit, ReligionTypes eReligion, bool bSuccess)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("unitSpreadReligionAttempt");						// add key to lookup python handler fxn

		CyUnit* pCyUnit = new CyUnit(pUnit);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyUnit));
		eventData.add(eReligion);
		eventData.add(bSuccess);

		postEvent(eventData);
		delete pCyUnit;
	}
}

void CvDllPythonEvents::reportUnitGifted(CvUnit* pUnit, PlayerTypes eGiftingPlayer, CvPlot* pPlotLocation)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("unitGifted");						// add key to lookup python handler fxn

		CyUnit* pCyUnit = new CyUnit(pUnit);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyUnit));
		eventData.add(eGiftingPlayer);
		CyPlot* pCyPlot = new CyPlot(pPlotLocation);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyPlot));

		postEvent(eventData);
		delete pCyUnit;
		delete pCyPlot;
	}
}

void CvDllPythonEvents::reportUnitBuildImprovement(CvUnit* pUnit, BuildTypes eBuild, bool bFinished)
{	// <advc.003y>
	if (!isUse(UNIT_BUILD_IMPROVEMENT))
		return; // </advc.003y>
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("unitBuildImprovement");						// add key to lookup python handler fxn

		CyUnit* pCyUnit = new CyUnit(pUnit);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyUnit));
		eventData.add(eBuild);
		eventData.add(bFinished);

		postEvent(eventData);
		delete pCyUnit;
	}
}

void CvDllPythonEvents::reportGoodyReceived(PlayerTypes ePlayer, CvPlot *pGoodyPlot, CvUnit *pGoodyUnit, GoodyTypes eGoodyType)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("goodyReceived");						// add key to lookup python handler fxn

		eventData.add(ePlayer);

		CyPlot* py = new CyPlot(pGoodyPlot);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(py));

		CyUnit* pyu = new CyUnit(pGoodyUnit);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pyu));

		eventData.add(eGoodyType);

		postEvent(eventData);

		delete py;
		delete pyu;
	}
}

void CvDllPythonEvents::reportGreatPersonBorn(CvUnit *pUnit, PlayerTypes ePlayer, CvCity *pCity)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("greatPersonBorn");						// add key to lookup python handler fxn

		CyUnit* py = new CyUnit(pUnit);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(py));

		eventData.add(ePlayer);

		CyCity* pyu = new CyCity(pCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pyu));

		postEvent(eventData);

		delete py;
		delete pyu;
	}
}

void CvDllPythonEvents::reportBuildingBuilt(CvCity *pCity, BuildingTypes eBuilding)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("buildingBuilt");					// add key to lookup python handler fxn

		CyCity* pCyCity = new CyCity(pCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyCity));

		eventData.add(eBuilding);

		postEvent(eventData);

		delete pCyCity;
	}
}

void CvDllPythonEvents::reportProjectBuilt(CvCity *pCity, ProjectTypes eProject)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("projectBuilt");					// add key to lookup python handler fxn

		CyCity* pCyCity = new CyCity(pCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyCity));

		eventData.add(eProject);

		postEvent(eventData);

		delete pCyCity;
	}
}

void CvDllPythonEvents::reportTechAcquired(TechTypes eType, TeamTypes eTeam, PlayerTypes ePlayer, bool bAnnounce)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("techAcquired");					// add key to lookup python handler fxn
		eventData.add(eType);
		eventData.add(eTeam);
		eventData.add(ePlayer);
		eventData.add(bAnnounce);
		postEvent(eventData);
	}
}

void CvDllPythonEvents::reportTechSelected(TechTypes eTech, PlayerTypes ePlayer)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("techSelected");					// add key to lookup python handler fxn
		eventData.add(eTech);
		eventData.add(ePlayer);
		postEvent(eventData);
	}
}

void CvDllPythonEvents::reportReligionFounded(ReligionTypes eType, PlayerTypes ePlayer)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("religionFounded");			// add key to lookup python handler fxn
		eventData.add(eType);
		eventData.add(ePlayer);
		postEvent(eventData);
	}
}

void CvDllPythonEvents::reportReligionSpread(ReligionTypes eType, PlayerTypes ePlayer, CvCity* pSpreadCity)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("religionSpread");			// add key to lookup python handler fxn
		eventData.add(eType);
		eventData.add(ePlayer);

		CyCity* pyu = new CyCity(pSpreadCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pyu));

		postEvent(eventData);
		delete pyu;
	}
}

void CvDllPythonEvents::reportReligionRemove(ReligionTypes eType, PlayerTypes ePlayer, CvCity* pSpreadCity)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("religionRemove");			// add key to lookup python handler fxn
		eventData.add(eType);
		eventData.add(ePlayer);

		CyCity* pyu = new CyCity(pSpreadCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pyu));

		postEvent(eventData);
		delete pyu;
	}
}

void CvDllPythonEvents::reportCorporationFounded(CorporationTypes eType, PlayerTypes ePlayer)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("corporationFounded");			// add key to lookup python handler fxn
		eventData.add(eType);
		eventData.add(ePlayer);
		postEvent(eventData);
	}
}

void CvDllPythonEvents::reportCorporationSpread(CorporationTypes eType, PlayerTypes ePlayer, CvCity* pSpreadCity)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("corporationSpread");			// add key to lookup python handler fxn
		eventData.add(eType);
		eventData.add(ePlayer);

		CyCity* pyu = new CyCity(pSpreadCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pyu));

		postEvent(eventData);
		delete pyu;
	}
}

void CvDllPythonEvents::reportCorporationRemove(CorporationTypes eType, PlayerTypes ePlayer, CvCity* pSpreadCity)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("corporationRemove");			// add key to lookup python handler fxn
		eventData.add(eType);
		eventData.add(ePlayer);

		CyCity* pyu = new CyCity(pSpreadCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pyu));

		postEvent(eventData);
		delete pyu;
	}
}

void CvDllPythonEvents::reportGoldenAge(PlayerTypes ePlayer)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("goldenAge");			// add key to lookup python handler fxn
		eventData.add(ePlayer);
		postEvent(eventData);
	}
}

void CvDllPythonEvents::reportEndGoldenAge(PlayerTypes ePlayer)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("endGoldenAge");			// add key to lookup python handler fxn
		eventData.add(ePlayer);
		postEvent(eventData);
	}
}

void CvDllPythonEvents::reportChangeWar(bool bWar, TeamTypes eTeam, TeamTypes eOtherTeam, bool bFromDefensivePact)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("changeWar");			// add key to lookup python handler fxn
		eventData.add(bWar);
		eventData.add(eTeam);
		eventData.add(eOtherTeam);
		eventData.add(bFromDefensivePact); // doc
		postEvent(eventData);
	}
}

void CvDllPythonEvents::reportVictory(TeamTypes eNewWinner, VictoryTypes eNewVictory)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("victory");					// add key to lookup python handler fxn
		eventData.add(eNewWinner);
		eventData.add(eNewVictory);
		postEvent(eventData);
	}
}

void CvDllPythonEvents::reportVassalState(TeamTypes eMaster, TeamTypes eVassal, bool bVassal, bool bCapitulated)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("vassalState");					// add key to lookup python handler fxn
		eventData.add(eMaster);
		eventData.add(eVassal);
		eventData.add(bVassal);
		eventData.add(bCapitulated); // doc: add capitulated

		postEvent(eventData);
	}
}

void CvDllPythonEvents::reportSetPlayerAlive(PlayerTypes ePlayerID, bool bNewValue)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("setPlayerAlive");
		eventData.add(ePlayerID);
		eventData.add(bNewValue);
		postEvent(eventData);
	}
}

void CvDllPythonEvents::reportPlayerChangeStateReligion(PlayerTypes ePlayerID, ReligionTypes eNewReligion, ReligionTypes eOldReligion)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("playerChangeStateReligion");			// add key to lookup python handler fxn

		eventData.add(ePlayerID);
		eventData.add(eNewReligion);
		eventData.add(eOldReligion);

		postEvent(eventData);
	}
}


void CvDllPythonEvents::reportPlayerGoldTrade(PlayerTypes eFromPlayer, PlayerTypes eToPlayer, int iAmount)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("playerGoldTrade");			// add key to lookup python handler fxn

		eventData.add(eFromPlayer);
		eventData.add(eToPlayer);
		eventData.add(iAmount);

		postEvent(eventData);
	}
}

// doc (edead): revolution event
void CvDllPythonEvents::reportRevolution(PlayerTypes ePlayer)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("revolution");			// add key to lookup python handler fxn

		eventData.add(ePlayer);

		postEvent(eventData);
	}
}

// doc: trade mission event
void CvDllPythonEvents::reportTradeMission(UnitTypes eUnit, PlayerTypes ePlayer, int iX, int iY, int iGold)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("tradeMission");

		eventData.add(eUnit);
		eventData.add(ePlayer);
		eventData.add(iX);
		eventData.add(iY);
		eventData.add(iGold);

		postEvent(eventData);
	}
}

// doc: slave trade event
void CvDllPythonEvents::reportPlayerSlaveTrade(PlayerTypes ePlayer, int iGold)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("playerSlaveTrade");

		eventData.add(ePlayer);
		eventData.add(iGold);

		postEvent(eventData);
	}
}

// doc: released civilization event
void CvDllPythonEvents::reportReleasedCivilization(PlayerTypes ePlayer, CivilizationTypes eReleasedCivilization)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("releasedCivilization");

		eventData.add(ePlayer);
		eventData.add(eReleasedCivilization);

		postEvent(eventData);
	}
}

// doc: blockade event
void CvDllPythonEvents::reportBlockade(PlayerTypes ePlayer, CvCity* pCity, int iGold)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("blockade");

		eventData.add(ePlayer);
		CyCity* pCyCity = new CyCity(pCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyCity));
		eventData.add(iGold);

		postEvent(eventData);
		delete pCyCity;
	}
}

// doc: peace brokered event
void CvDllPythonEvents::reportPeaceBrokered(PlayerTypes eBroker, PlayerTypes ePlayer1, PlayerTypes ePlayer2)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("peaceBrokered");

		eventData.add(eBroker);
		eventData.add(ePlayer1);
		eventData.add(ePlayer2);

		postEvent(eventData);
	}
}

// doc: XML loaded before menu
void CvDllPythonEvents::reportXMLLoaded()
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("xmlLoaded");
		postEvent(eventData);
	}
}

// doc: Font files loaded and font IDs assigned
void CvDllPythonEvents::reportFontsLoaded()
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("fontsLoaded");
		postEvent(eventData);
	}
}

// doc: civic changed event
void CvDllPythonEvents::reportCivicChanged(PlayerTypes ePlayer, CivicTypes eOldCivic, CivicTypes eNewCivic)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("civicChanged");
		eventData.add(ePlayer);
		eventData.add(eOldCivic);
		eventData.add(eNewCivic);
		postEvent(eventData);
	}
}

// doc: autoplay ended event
void CvDllPythonEvents::reportAutoplayEnded()
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("autoplayEnded");
		postEvent(eventData);
	}
}

// doc: player civilization assigned event
void CvDllPythonEvents::reportPlayerCivAssigned(PlayerTypes ePlayer, CivilizationTypes eNewCivilization)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("playerCivAssigned");
		eventData.add(ePlayer);
		eventData.add(eNewCivilization);
		postEvent(eventData);
	}
}

// doc: player destroyed event
void CvDllPythonEvents::reportPlayerDestroyed(PlayerTypes ePlayer)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("playerDestroyed");
		eventData.add(ePlayer);
		postEvent(eventData);
	}
}

// doc: switch event
void CvDllPythonEvents::reportPlayerSwitch(PlayerTypes eOldPlayer, PlayerTypes eNewPlayer)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("switch");
		eventData.add(eOldPlayer);
		eventData.add(eNewPlayer);
		postEvent(eventData);
	}
}

// doc: tech traded event
void CvDllPythonEvents::reportTechTraded(PlayerTypes eFrom, PlayerTypes eTo, TechTypes eTech)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("techTraded");
		eventData.add(eFrom);
		eventData.add(eTo);
		eventData.add(eTech);
		postEvent(eventData);
	}
}

// doc: tribute event
void CvDllPythonEvents::reportTribute(PlayerTypes eFrom, PlayerTypes eTo)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("tribute");
		eventData.add(eFrom);
		eventData.add(eTo);
		postEvent(eventData);
	}
}

// doc: global warming event
void CvDllPythonEvents::reportGlobalWarming(int iGlobalWarmingValue, int iGlobalWarmingDefense)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("globalWarming");
		eventData.add(iGlobalWarmingValue);
		eventData.add(iGlobalWarmingDefense);
		postEvent(eventData);
	}
}

// doc: global warming effect event
void CvDllPythonEvents::reportGlobalWarmingEffect(CvPlot* pPlot, bool bChanged, TerrainTypes ePreviousTerrain, TerrainTypes eNewTerrain, FeatureTypes ePreviousFeature)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("globalWarmingEffect");

		CyPlot* pCyPlot = new CyPlot(pPlot);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyPlot));

		eventData.add(bChanged);
		eventData.add(ePreviousTerrain);
		eventData.add(eNewTerrain);
		eventData.add(ePreviousFeature);
		postEvent(eventData);
	}
}

// doc: building processed event
// TODO: used?
void CvDllPythonEvents::reportBuildingProcessed(CvCity* pCity, BuildingTypes eBuilding, int iChange)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("buildingProcessed");					// add key to lookup python handler fxn

		CyCity* pCyCity = new CyCity(pCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyCity));

		eventData.add(eBuilding);
		eventData.add(iChange);

		postEvent(eventData);

		delete pCyCity;
	}
}

// doc: city sacked event
void CvDllPythonEvents::reportCitySacked(CvCity* pCity)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("citySacked");

		CyCity* pCyCity = new CyCity(pCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyCity));

		postEvent(eventData);

		delete pCyCity;
	}
}

void CvDllPythonEvents::reportGenericEvent(const char* szEventName, void *pyArgs)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add(szEventName);
		eventData.add(pyArgs);		// generic args tuple
		postEvent(eventData);
	}
}

void CvDllPythonEvents::preSave()
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("OnPreSave");
		postEvent(eventData);
	}
}
