#include "CvGameCoreDLL.h"
#include "CvDllPythonEvents.h"
#include "CvDLLEngineIFaceBase.h"
#include "CvDLLInterfaceIFaceBase.h"
#include "CyArgsList.h"
#include "CyUnit.h"
#include "CyPlot.h"

bool CvDllPythonEvents::preEvent()
{
	return gDLL->getPythonIFace()->isInitialized();
}

bool CvDllPythonEvents::postEvent(CyArgsList& eventData)
{
	eventData.add(GC.getGameINLINE().isDebugMode());
	eventData.add(false);
	eventData.add(gDLL->altKey());
	eventData.add(gDLL->ctrlKey());
	eventData.add(gDLL->shiftKey());
	eventData.add(gDLL->getChtLvl() > 0);

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
		gDLL->getInterfaceIFace()->getInterfaceScreenIdsForInput(screens);
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
{
	if (preEvent())
	{
		if(GC.getUSE_ON_UPDATE_CALLBACK())
		{
			CyArgsList eventData;
			eventData.add("Update");				// add key to lookup python handler fxn
			eventData.add(fDeltaTime);
			postEvent(eventData);
		}
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
		eventData.add((int)ePlayer);
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
		eventData.add((int)ePlayer);
		postEvent(eventData);
	}
}

void CvDllPythonEvents::reportFirstContact(TeamTypes eTeamID1, TeamTypes eTeamID2)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("firstContact");				// add key to lookup python handler fxn
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

// BUG - Combat Events - start
void CvDllPythonEvents::reportCombatRetreat(CvUnit* pAttacker, CvUnit* pDefender)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("combatRetreat");				// add key to lookup python handler fxn

		CyUnit* pCyAttacker = new CyUnit(pAttacker);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyAttacker));

		CyUnit* pCyDefender = new CyUnit(pDefender);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyDefender));

		postEvent(eventData);
		delete pCyDefender;
		delete pCyAttacker;
	}
}

void CvDllPythonEvents::reportCombatWithdrawal(CvUnit* pAttacker, CvUnit* pDefender)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("combatWithdrawal");			// add key to lookup python handler fxn

		CyUnit* pCyAttacker = new CyUnit(pAttacker);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyAttacker));

		CyUnit* pCyDefender = new CyUnit(pDefender);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyDefender));

		postEvent(eventData);
		delete pCyDefender;
		delete pCyAttacker;
	}
}

void CvDllPythonEvents::reportCombatLogCollateral(CvUnit* pAttacker, CvUnit* pDefender, int iDamage)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("combatLogCollateral");		// add key to lookup python handler fxn

		CyUnit* pCyAttacker = new CyUnit(pAttacker);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyAttacker));

		CyUnit* pCyDefender = new CyUnit(pDefender);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyDefender));

		eventData.add(iDamage);

		postEvent(eventData);
		delete pCyDefender;
		delete pCyAttacker;
	}
}

void CvDllPythonEvents::reportCombatLogFlanking(CvUnit* pAttacker, CvUnit* pDefender, int iDamage)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("combatLogFlanking");			// add key to lookup python handler fxn

		CyUnit* pCyAttacker = new CyUnit(pAttacker);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyAttacker));

		CyUnit* pCyDefender = new CyUnit(pDefender);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyDefender));

		eventData.add(iDamage);

		postEvent(eventData);
		delete pCyDefender;
		delete pCyAttacker;
	}
}
// BUG - Combat Events - end

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
{
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
		eventData.add((int)eTeam);

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
		eventData.add((int)eFeature);

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
		eventData.add((int) ePlayer);

		postEvent(eventData);
		delete pCyPlot;
	}
}

void CvDllPythonEvents::reportCityBuilt( CvCity *pCity )
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

void CvDllPythonEvents::reportCityRazed( CvCity *pCity, PlayerTypes ePlayer )
{
	if (preEvent())
	{
		FAssert(ePlayer != NO_PLAYER);

		CyArgsList eventData;
		eventData.add("cityRazed");						// add key to lookup python handler fxn

		CyCity* pCyCity = new CyCity(pCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyCity));
		eventData.add((int)ePlayer);

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
		eventData.add((int)eOldOwner);
		eventData.add((int)ePlayer);

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
		eventData.add((int)ePlayer);

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

void CvDllPythonEvents::reportCultureExpansion( CvCity *pCity, PlayerTypes ePlayer )
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("cultureExpansion");						// add key to lookup python handler fxn

		CyCity* pCyCity = new CyCity(pCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyCity));

		eventData.add((int) ePlayer);

		postEvent(eventData);
		delete pCyCity;
	}
}

void CvDllPythonEvents::reportCityGrowth( CvCity *pCity, PlayerTypes ePlayer )
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("cityGrowth");						// add key to lookup python handler fxn

		CyCity* pCyCity = new CyCity(pCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyCity));

		eventData.add((int) ePlayer);

		postEvent(eventData);
		delete pCyCity;
	}
}

void CvDllPythonEvents::reportCityProduction( CvCity *pCity, PlayerTypes ePlayer )
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("cityDoTurn");						// add key to lookup python handler fxn

		CyCity* pCyCity = new CyCity(pCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyCity));

		eventData.add((int) ePlayer);

		postEvent(eventData);
		delete pCyCity;
	}
}

void CvDllPythonEvents::reportCityBuildingUnit( CvCity *pCity, UnitTypes eUnitType )
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("cityBuildingUnit");						// add key to lookup python handler fxn

		CyCity* pCyCity = new CyCity(pCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyCity));

		eventData.add((int) eUnitType);

		postEvent(eventData);
		delete pCyCity;
	}
}

void CvDllPythonEvents::reportCityBuildingBuilding( CvCity *pCity, BuildingTypes eBuildingType )
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("cityBuildingBuilding");						// add key to lookup python handler fxn

		CyCity* pCyCity = new CyCity(pCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyCity));

		eventData.add((int) eBuildingType);

		postEvent(eventData);
		delete pCyCity;
	}
}

// BUG - Project Started Event - start
void CvDllPythonEvents::reportCityBuildingProject( CvCity* pCity, ProjectTypes eProjectType )
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("cityBuildingProject");						// add key to lookup python handler fxn

		CyCity* pCyCity = new CyCity(pCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyCity));

		eventData.add((int) eProjectType);

		postEvent(eventData);
		delete pCyCity;
	}
}
// BUG - Project Started Event - end

// BUG - Process Started Event - start
void CvDllPythonEvents::reportCityBuildingProcess( CvCity* pCity, ProcessTypes eProcessType )
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("cityBuildingProcess");						// add key to lookup python handler fxn

		CyCity* pCyCity = new CyCity(pCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyCity));

		eventData.add((int) eProcessType);

		postEvent(eventData);
		delete pCyCity;
	}
}
// BUG - Process Started Event - end

void CvDllPythonEvents::reportCityRename( CvCity *pCity )
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

void CvDllPythonEvents::reportCityHurry( CvCity *pCity, HurryTypes eHurry )
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("cityHurry");						// add key to lookup python handler fxn

		CyCity* pCyCity = new CyCity(pCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyCity));

		eventData.add((int) eHurry);

		postEvent(eventData);
		delete pCyCity;
	}
}

void CvDllPythonEvents::reportCityCaptureGold(CvCity *pCity, PlayerTypes ePlayer, int iCaptureGold)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("cityCaptureGold");

		CyCity* pCyCity = new CyCity(pCity);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyCity));

		eventData.add((int)ePlayer);
		eventData.add(iCaptureGold);

		postEvent(eventData);
		delete pCyCity;
	}
}

void CvDllPythonEvents::reportSelectionGroupPushMission(CvSelectionGroup* pSelectionGroup, MissionTypes eMission)
{
	if (NULL == pSelectionGroup)
	{
		return;
	}

	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("selectionGroupPushMission");						// add key to lookup python handler fxn
		eventData.add(pSelectionGroup->getOwner());
		eventData.add(eMission);
		int iNumUnits = pSelectionGroup->getNumUnits();
		eventData.add(iNumUnits);

		int* aiUnitIds = new int[iNumUnits];
		CLLNode<IDInfo>* pUnitNode = pSelectionGroup->headUnitNode();
		for (int i = 0; pUnitNode; i++)
		{
			CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
			pUnitNode = pSelectionGroup->nextUnitNode(pUnitNode);
			aiUnitIds[i] = pLoopUnit->getID();
			FAssert(i < iNumUnits);
		}

		if (aiUnitIds)
		{
			eventData.add(aiUnitIds, iNumUnits);
		}

		postEvent(eventData);

		delete aiUnitIds;
	}
}

void CvDllPythonEvents::reportUnitMove(CvPlot* pPlot, CvUnit* pUnit, CvPlot* pOldPlot)
{
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
{
	if (preEvent())
	{
		if(GC.getUSE_ON_UNIT_SET_XY_CALLBACK())
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
}

void CvDllPythonEvents::reportUnitCreated(CvUnit* pUnit)
{
	if (preEvent())
	{
		if(GC.getUSE_ON_UNIT_CREATED_CALLBACK())
		{
			CyArgsList eventData;
			eventData.add("unitCreated");						// add key to lookup python handler fxn

			CyUnit* pyu = new CyUnit(pUnit);
			eventData.add(gDLL->getPythonIFace()->makePythonObject(pyu));
			postEvent(eventData);
			delete pyu;
		}
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
		eventData.add((int)eAttacker);
		postEvent(eventData);
		delete pyu;
	}
}

// BUG - Unit Captured Event - start
void CvDllPythonEvents::reportUnitCaptured(PlayerTypes eFromPlayer, UnitTypes eUnitType, CvUnit* pNewUnit)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("unitCaptured");						// add key to lookup python handler fxn

		eventData.add(eFromPlayer);
		eventData.add(eUnitType);
		CyUnit* pyNewUnit = new CyUnit(pNewUnit);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pyNewUnit));
		postEvent(eventData);
		delete pyNewUnit;
	}
}
// BUG - Unit Captured Event - end

void CvDllPythonEvents::reportUnitLost(CvUnit* pUnit)
{
	if (preEvent())
	{
		if(GC.getUSE_ON_UNIT_LOST_CALLBACK())
		{
			CyArgsList eventData;
			eventData.add("unitLost");						// add key to lookup python handler fxn

			CyUnit* pyu = new CyUnit(pUnit);
			eventData.add(gDLL->getPythonIFace()->makePythonObject(pyu));
			postEvent(eventData);
			delete pyu;
		}
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
		eventData.add((int)ePromotion);
		postEvent(eventData);
		delete pyu;
	}
}

// BUG - Upgrade Unit Event - start
void CvDllPythonEvents::reportUnitUpgraded(CvUnit* pOldUnit, CvUnit* pNewUnit, int iPrice)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("unitUpgraded");						// add key to lookup python handler fxn

		CyUnit* pyOldUnit = new CyUnit(pOldUnit);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pyOldUnit));
		CyUnit* pyNewUnit = new CyUnit(pNewUnit);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pyNewUnit));
		eventData.add(iPrice);
		postEvent(eventData);
		delete pyNewUnit;
		delete pyOldUnit;
	}
}
// BUG - Upgrade Unit Event - end

void CvDllPythonEvents::reportUnitSelected(CvUnit* pUnit)
{
	if (preEvent())
	{
		if(GC.getUSE_ON_UNIT_SELECTED_CALLBACK())
		{
			CyArgsList eventData;
			eventData.add("unitSelected");						// add key to lookup python handler fxn

			CyUnit* pyu = new CyUnit(pUnit);
			eventData.add(gDLL->getPythonIFace()->makePythonObject(pyu));
			postEvent(eventData);
			delete pyu;
		}
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
		eventData.add((int) eImprovement);
		eventData.add((int) eRoute);
		eventData.add((int) ePlayer);
		eventData.add((int) iPillagedGold);

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
		eventData.add((int) eReligion);
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
		eventData.add((int) eGiftingPlayer);
		CyPlot* pCyPlot = new CyPlot(pPlotLocation);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyPlot));

		postEvent(eventData);
		delete pCyUnit;
		delete pCyPlot;
	}
}

void CvDllPythonEvents::reportUnitBuildImprovement(CvUnit* pUnit, BuildTypes eBuild, bool bFinished)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("unitBuildImprovement");						// add key to lookup python handler fxn

		CyUnit* pCyUnit = new CyUnit(pUnit);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pCyUnit));
		eventData.add((int) eBuild);
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

		eventData.add((int)ePlayer);

		CyPlot* py = new CyPlot(pGoodyPlot);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(py));

		CyUnit* pyu = new CyUnit(pGoodyUnit);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(pyu));

		eventData.add((int) eGoodyType);

		postEvent(eventData);

		delete py;
		delete pyu;
	}
}

void CvDllPythonEvents::reportGreatPersonBorn( CvUnit *pUnit, PlayerTypes ePlayer, CvCity *pCity )
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("greatPersonBorn");						// add key to lookup python handler fxn

		CyUnit* py = new CyUnit(pUnit);
		eventData.add(gDLL->getPythonIFace()->makePythonObject(py));

		eventData.add((int)ePlayer);

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
		eventData.add((int)eType);
		eventData.add((int)eTeam);
		eventData.add((int)ePlayer);
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
		eventData.add((int)eTech);
		eventData.add((int)ePlayer);
		postEvent(eventData);
	}
}

void CvDllPythonEvents::reportReligionFounded(ReligionTypes eType, PlayerTypes ePlayer)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("religionFounded");			// add key to lookup python handler fxn
		eventData.add((int)eType);
		eventData.add((int)ePlayer);
		postEvent(eventData);
	}
}

void CvDllPythonEvents::reportReligionSpread(ReligionTypes eType, PlayerTypes ePlayer, CvCity* pSpreadCity)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("religionSpread");			// add key to lookup python handler fxn
		eventData.add((int)eType);
		eventData.add((int)ePlayer);

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
		eventData.add((int)eType);
		eventData.add((int)ePlayer);

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
		eventData.add((int)eType);
		eventData.add((int)ePlayer);
		postEvent(eventData);
	}
}

void CvDllPythonEvents::reportCorporationSpread(CorporationTypes eType, PlayerTypes ePlayer, CvCity* pSpreadCity)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("corporationSpread");			// add key to lookup python handler fxn
		eventData.add((int)eType);
		eventData.add((int)ePlayer);

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
		eventData.add((int)eType);
		eventData.add((int)ePlayer);

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
		eventData.add((int)ePlayer);
		postEvent(eventData);
	}
}

void CvDllPythonEvents::reportEndGoldenAge(PlayerTypes ePlayer)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("endGoldenAge");			// add key to lookup python handler fxn
		eventData.add((int)ePlayer);
		postEvent(eventData);
	}
}

void CvDllPythonEvents::reportChangeWar(bool bWar, TeamTypes eTeam, TeamTypes eOtherTeam)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("changeWar");			// add key to lookup python handler fxn
		eventData.add(bWar);
		eventData.add((int)eTeam);
		eventData.add((int)eOtherTeam);
		postEvent(eventData);
	}
}

void CvDllPythonEvents::reportVictory(TeamTypes eNewWinner, VictoryTypes eNewVictory)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("victory");					// add key to lookup python handler fxn
		eventData.add((int)eNewWinner);
		eventData.add((int)eNewVictory);
		postEvent(eventData);
	}
}

void CvDllPythonEvents::reportVassalState(TeamTypes eMaster, TeamTypes eVassal, bool bVassal, bool bCapitulated)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("vassalState");					// add key to lookup python handler fxn
		eventData.add((int)eMaster);
		eventData.add((int)eVassal);
		eventData.add(bVassal);
		eventData.add(bCapitulated);

		postEvent(eventData);
	}
}

void CvDllPythonEvents::reportSetPlayerAlive( PlayerTypes ePlayerID, bool bNewValue )
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("setPlayerAlive");
		eventData.add((int)ePlayerID);
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

		eventData.add((int)ePlayerID);
		eventData.add((int)eNewReligion);
		eventData.add((int)eOldReligion);

		postEvent(eventData);
	}
}


void CvDllPythonEvents::reportPlayerGoldTrade(PlayerTypes eFromPlayer, PlayerTypes eToPlayer, int iAmount)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("playerGoldTrade");			// add key to lookup python handler fxn

		eventData.add((int)eFromPlayer);
		eventData.add((int)eToPlayer);
		eventData.add(iAmount);

		postEvent(eventData);
	}
}

// edead: start
void CvDllPythonEvents::reportRevolution(PlayerTypes ePlayerID)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("revolution");			// add key to lookup python handler fxn

		eventData.add((int)ePlayerID);

		postEvent(eventData);
	}
}
// edead: end

// Leoreth: trade mission (great merchant)
void CvDllPythonEvents::reportTradeMission(UnitTypes unitID, PlayerTypes ePlayer, int iX, int iY, int iGold)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("tradeMission");

		eventData.add((int)unitID);
		eventData.add((int)ePlayer);
		eventData.add((int)iX);
		eventData.add((int)iY);
		eventData.add(iGold);

		postEvent(eventData);
	}
}

// Leoreth: slave trade (amount of gold received)
void CvDllPythonEvents::reportPlayerSlaveTrade(PlayerTypes ePlayer, int iGold)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("playerSlaveTrade");

		eventData.add((int)ePlayer);
		eventData.add(iGold);

		postEvent(eventData);
	}
}

// Leoreth: release dead civilizations
void CvDllPythonEvents::reportReleasedPlayer(PlayerTypes ePlayer, PlayerTypes eReleasedPlayer)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("releasedPlayer");

		eventData.add((int)ePlayer);
		eventData.add((int)eReleasedPlayer);

		postEvent(eventData);
	}
}

// Leoreth: blockade a city
void CvDllPythonEvents::reportBlockade(PlayerTypes ePlayer, int iGold)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("blockade");

		eventData.add((int)ePlayer);
		eventData.add(iGold);

		postEvent(eventData);
	}
}

// Leoreth: peace deal arranged between players
void CvDllPythonEvents::reportPeaceBrokered(PlayerTypes eBroker, PlayerTypes ePlayer1, PlayerTypes ePlayer2)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("peaceBrokered");

		eventData.add((int)eBroker);
		eventData.add((int)ePlayer1);
		eventData.add((int)ePlayer2);

		postEvent(eventData);
	}
}

// Leoreth: XML loaded before menu
void CvDllPythonEvents::reportXMLLoaded()
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("xmlLoaded");
		postEvent(eventData);
	}
}

// Leoreth: Font files loaded and font IDs assigned
void CvDllPythonEvents::reportFontsLoaded()
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("fontsLoaded");
		postEvent(eventData);
	}
}

// Leoreth: civic changed
void CvDllPythonEvents::reportCivicChanged(PlayerTypes ePlayer, CivicTypes eOldCivic, CivicTypes eNewCivic)
{
	if (preEvent())
	{
		CyArgsList eventData;
		eventData.add("civicChanged");
		eventData.add((int)ePlayer);
		eventData.add((int)eOldCivic);
		eventData.add((int)eNewCivic);
		postEvent(eventData);
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
