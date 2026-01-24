#include "CvGameCoreDLL.h"
#include "CvGame.h"
#include "CvInitCore.h"
#include "CyPlot.h"
#include "CyArgsList.h"
#include "CvPopupInfo.h"
#include "CvDLLInterfaceIFaceBase.h"
#include "CvDLLEngineIFaceBase.h"
#include "CvDLLFAStarIFaceBase.h"
#include "FAStarNode.h"
#include "CvGameTextMgr.h"
#include "CvMessageControl.h"

void CvGame::updateColoredPlots()
{
	PROFILE_FUNC();

	CLLNode<IDInfo>* pSelectedCityNode;
	CLLNode<IDInfo>* pSelectedUnitNode;
	CvCity* pHeadSelectedCity;
	CvCity* pSelectedCity;
	CvCity* pCity;
	CvUnit* pHeadSelectedUnit;
	CvUnit* pSelectedUnit;
	CvPlot* pRallyPlot;
	CvPlot* pLoopPlot;
	CvPlot* pBestPlot;
	CvPlot* pNextBestPlot;
	long lResult;
	int iMaxAirRange;
	int iRange;
	int iDX, iDY;
	int iI;

	gDLL->getEngineIFace()->clearColoredPlots(PLOT_LANDSCAPE_LAYER_BASE);
	gDLL->getEngineIFace()->clearAreaBorderPlots(AREA_BORDER_LAYER_CITY_RADIUS);
	gDLL->getEngineIFace()->clearAreaBorderPlots(AREA_BORDER_LAYER_RANGED);
	gDLL->getEngineIFace()->clearAreaBorderPlots(AREA_BORDER_LAYER_BLOCKADING);

	if (!gDLL->GetWorldBuilderMode() || gDLL->getInterfaceIFace()->isInAdvancedStart())
	{
		gDLL->getEngineIFace()->clearColoredPlots(PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS);
	}

	lResult = 0;
	gDLL->getPythonIFace()->callFunction(PYGameModule, "updateColoredPlots", NULL, &lResult);
	if (lResult == 1)
	{
		return;
	}

	// City circles when in Advanced Start
	if (gDLL->getInterfaceIFace()->isInAdvancedStart())
	{
		for (int iPlotLoop = 0; iPlotLoop < GC.getMap().numPlots(); iPlotLoop++)
		{
			CvPlot* pLoopPlot = GC.getMap().plotByIndex(iPlotLoop);

			if (pLoopPlot != NULL)
			{
				if (GET_PLAYER(getActivePlayer()).getAdvancedStartCityCost(true, pLoopPlot) > 0)
				{
					bool bStartingPlot = false;
					for (int iPlayer = 0; iPlayer < MAX_PLAYERS; ++iPlayer)
					{
						CvPlayer& kPlayer = GET_PLAYER((PlayerTypes) iPlayer);
						if (kPlayer.isAlive() && getActiveTeam() == kPlayer.getTeam())
						{
							if (pLoopPlot == kPlayer.getStartingPlot())
							{
								bStartingPlot = true;
								break;
							}
						}
					}
					if (bStartingPlot)
					{
						gDLL->getEngineIFace()->addColoredPlot(pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE(), GC.getColorInfo((ColorTypes)GC.getInfoTypeForString("COLOR_WARNING_TEXT")).getColor(), PLOT_STYLE_CIRCLE, PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS);
					}
					else if (GET_PLAYER(getActivePlayer()).AI_isPlotCitySite(pLoopPlot))
					{
						gDLL->getEngineIFace()->addColoredPlot(pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE(), GC.getColorInfo((ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT")).getColor(), PLOT_STYLE_CIRCLE, PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS);
					}

					if (pLoopPlot->isRevealed(getActiveTeam(), false))
					{
						NiColorA color(GC.getColorInfo((ColorTypes)GC.getInfoTypeForString("COLOR_WHITE")).getColor());
						color.a = 0.4f;
						gDLL->getEngineIFace()->fillAreaBorderPlot(pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE(), color, AREA_BORDER_LAYER_CITY_RADIUS);
					}
				}
			}
		}
	}

	pHeadSelectedCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();
	pHeadSelectedUnit = gDLL->getInterfaceIFace()->getHeadSelectedUnit();

	if (pHeadSelectedCity != NULL)
	{
		if (gDLL->getInterfaceIFace()->isCityScreenUp())
		{
			for (iI = 0; iI < NUM_CITY_PLOTS; iI++)
			{
				if (pHeadSelectedCity->isWorkingPlot(iI))
				{
					pLoopPlot = plotCity(pHeadSelectedCity->getX_INLINE(), pHeadSelectedCity->getY_INLINE(), iI);

					if (pLoopPlot != NULL)
					{
						NiColorA color(GC.getColorInfo((ColorTypes)GC.getInfoTypeForString("COLOR_WHITE")).getColor());
						color.a = 0.7f;
						gDLL->getEngineIFace()->addColoredPlot(pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE(), color, PLOT_STYLE_CIRCLE, PLOT_LANDSCAPE_LAYER_BASE);
					}
				}
			}
		}
		else
		{
			pSelectedCityNode = gDLL->getInterfaceIFace()->headSelectedCitiesNode();

			while (pSelectedCityNode != NULL)
			{
				pSelectedCity = ::getCity(pSelectedCityNode->m_data);
				pSelectedCityNode = gDLL->getInterfaceIFace()->nextSelectedCitiesNode(pSelectedCityNode);

				if (pSelectedCity != NULL)
				{
					pRallyPlot = pSelectedCity->getRallyPlot();

					if (pRallyPlot != NULL)
					{
						gDLL->getEngineIFace()->addColoredPlot(pRallyPlot->getX_INLINE(), pRallyPlot->getY_INLINE(), GC.getColorInfo((ColorTypes)GC.getInfoTypeForString("COLOR_YELLOW")).getColor(), PLOT_STYLE_CIRCLE, PLOT_LANDSCAPE_LAYER_BASE);
					}
				}
			}
		}
	}
	else if (pHeadSelectedUnit != NULL)
	{
		if (gDLL->getGraphicOption(GRAPHICOPTION_CITY_RADIUS))
		{
			if (gDLL->getInterfaceIFace()->canSelectionListFound())
			{
				for (iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
				{
					pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);

					if (pLoopPlot->getOwnerINLINE() == pHeadSelectedUnit->getOwnerINLINE())
					{
						if (pLoopPlot->getWorkingCity() != NULL)
						{
							NiColorA color(GC.getColorInfo((ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT")/*(GC.getPlayerColorInfo(GET_PLAYER(pHeadSelectedUnit->getOwnerINLINE()).getPlayerColor()).getColorTypePrimary())*/).getColor());
							color.a = 1.0f;
							gDLL->getEngineIFace()->fillAreaBorderPlot(pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE(), color, AREA_BORDER_LAYER_CITY_RADIUS);
						}
					}
				}
			}
		}

		if (pHeadSelectedUnit->getDomainType() == DOMAIN_AIR)
		{
			iMaxAirRange = 0;

			pSelectedUnitNode = gDLL->getInterfaceIFace()->headSelectionListNode();

			while (pSelectedUnitNode != NULL)
			{
				pSelectedUnit = ::getUnit(pSelectedUnitNode->m_data);
				pSelectedUnitNode = gDLL->getInterfaceIFace()->nextSelectionListNode(pSelectedUnitNode);

				if (pSelectedUnit != NULL)
				{
					iMaxAirRange = std::max(iMaxAirRange, pSelectedUnit->airRange());
				}
			}

			if (iMaxAirRange > 0)
			{
				for (iDX = -(iMaxAirRange); iDX <= iMaxAirRange; iDX++)
				{
					for (iDY = -(iMaxAirRange); iDY <= iMaxAirRange; iDY++)
					{
						pLoopPlot = plotXY(pHeadSelectedUnit->getX_INLINE(), pHeadSelectedUnit->getY_INLINE(), iDX, iDY);

						if (pLoopPlot != NULL)
						{
							if (plotDistance(pHeadSelectedUnit->getX_INLINE(), pHeadSelectedUnit->getY_INLINE(), pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE()) <= iMaxAirRange)
							{
								NiColorA color(GC.getColorInfo((ColorTypes)GC.getInfoTypeForString("COLOR_YELLOW")).getColor());
								color.a = 0.5f;
								gDLL->getEngineIFace()->fillAreaBorderPlot(pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE(), color, AREA_BORDER_LAYER_RANGED);
							}
						}
					}
				}
			}
		}
		else if(pHeadSelectedUnit->airRange() > 0) //other ranged units
		{
			int iRange = pHeadSelectedUnit->airRange();
			for (iDX = -(iRange); iDX <= iRange; iDX++)
			{
				for (iDY = -(iRange); iDY <= iRange; iDY++)
				{
					CvPlot* pTargetPlot = plotXY(pHeadSelectedUnit->getX_INLINE(), pHeadSelectedUnit->getY_INLINE(), iDX, iDY);

					if (pTargetPlot != NULL && pTargetPlot->isVisible(pHeadSelectedUnit->getTeam(), false))
					{
						if (plotDistance(pHeadSelectedUnit->getX_INLINE(), pHeadSelectedUnit->getY_INLINE(), pTargetPlot->getX_INLINE(), pTargetPlot->getY_INLINE()) <= iRange)
						{
							if (pHeadSelectedUnit->plot()->canSeePlot(pTargetPlot, pHeadSelectedUnit->getTeam(), iRange, pHeadSelectedUnit->getFacingDirection(true)))
							{
								NiColorA color(GC.getColorInfo((ColorTypes)GC.getInfoTypeForString("COLOR_YELLOW")).getColor());
								color.a = 0.5f;
								gDLL->getEngineIFace()->fillAreaBorderPlot(pTargetPlot->getX_INLINE(), pTargetPlot->getY_INLINE(), color, AREA_BORDER_LAYER_RANGED);
							}
						}
					}
				}
			}
		}

		FAssert(getActivePlayer() != NO_PLAYER);

		if (!(GET_PLAYER(getActivePlayer()).isOption(PLAYEROPTION_NO_UNIT_RECOMMENDATIONS)))
		{
			if ((pHeadSelectedUnit->AI_getUnitAIType() == UNITAI_WORKER) || (pHeadSelectedUnit->AI_getUnitAIType() == UNITAI_WORKER_SEA))
			{
				if (pHeadSelectedUnit->plot()->getOwnerINLINE() == pHeadSelectedUnit->getOwnerINLINE())
				{
					pCity = pHeadSelectedUnit->plot()->getWorkingCity();

					if (pCity != NULL)
					{
						if (pHeadSelectedUnit->AI_bestCityBuild(pCity, &pBestPlot))
						{
							FAssert(pBestPlot != NULL);
							gDLL->getEngineIFace()->addColoredPlot(pBestPlot->getX_INLINE(), pBestPlot->getY_INLINE(), GC.getColorInfo((ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT")).getColor(), PLOT_STYLE_CIRCLE, PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS);

							if (pHeadSelectedUnit->AI_bestCityBuild(pCity, &pNextBestPlot, NULL, pBestPlot))
							{
								FAssert(pNextBestPlot != NULL);
								gDLL->getEngineIFace()->addColoredPlot(pNextBestPlot->getX_INLINE(), pNextBestPlot->getY_INLINE(), GC.getColorInfo((ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT")).getColor(), PLOT_STYLE_CIRCLE, PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS);
							}
						}
					}
				}
			}

			iRange = 4;

			for (iDX = -(iRange); iDX <= iRange; iDX++)
			{
				for (iDY = -(iRange); iDY <= iRange; iDY++)
				{
					pLoopPlot = plotXY(pHeadSelectedUnit->getX_INLINE(), pHeadSelectedUnit->getY_INLINE(), iDX, iDY);

					if (pLoopPlot != NULL)
					{
						if ((pLoopPlot->area() == pHeadSelectedUnit->area()) || pLoopPlot->isAdjacentToArea(pHeadSelectedUnit->area()))
						{
							if (pHeadSelectedUnit->canFound(pLoopPlot))
							{
								if (GET_PLAYER(pHeadSelectedUnit->getOwnerINLINE()).AI_isPlotCitySite(pLoopPlot))
								{
									gDLL->getEngineIFace()->addColoredPlot(pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE(), GC.getColorInfo((ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT")).getColor(), PLOT_STYLE_CIRCLE, PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS);
								}
							}
							if (plotDistance(pHeadSelectedUnit->getX_INLINE(), pHeadSelectedUnit->getY_INLINE(), pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE()) <= iRange)
							{
								if (pLoopPlot->isVisible(pHeadSelectedUnit->getTeam(), false))
								{
									if (pHeadSelectedUnit->isNoBadGoodies())
									{
										if (pLoopPlot->isRevealedGoody(pHeadSelectedUnit->getTeam()))
										{
											gDLL->getEngineIFace()->addColoredPlot(pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE(), GC.getColorInfo((ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT")).getColor(), PLOT_STYLE_CIRCLE, PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS);
										}
									}
								}
							}
						}
					}
				}
			}
		}

		if (pHeadSelectedUnit->isBlockading())
		{
			int iBlockadeRange = GC.getDefineINT("SHIP_BLOCKADE_RANGE");

			for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; ++iPlayer)
			{
				CvPlayer& kPlayer = GET_PLAYER((PlayerTypes)iPlayer);

				if (kPlayer.getTeam() == getActiveTeam())
				{
					int iLoop;
					for (CvUnit* pLoopUnit = kPlayer.firstUnit(&iLoop); NULL != pLoopUnit; pLoopUnit = kPlayer.nextUnit(&iLoop))
					{
						if (pLoopUnit->isBlockading())
						{
							for (int i = -iBlockadeRange; i <= iBlockadeRange; ++i)
							{
								for (int j = -iBlockadeRange; j <= iBlockadeRange; ++j)
								{
									CvPlot* pLoopPlot = ::plotXY(pLoopUnit->getX_INLINE(), pLoopUnit->getY_INLINE(), i, j);
									if (NULL != pLoopPlot && pLoopPlot->isRevealed(getActiveTeam(), false))
									{
										if (pLoopPlot->isWater() && pLoopPlot->area() == pLoopUnit->area())
										{
											NiColorA color(GC.getColorInfo((ColorTypes)GC.getPlayerColorInfo(GET_PLAYER(getActivePlayer()).getPlayerColor()).getColorTypePrimary()).getColor());
											color.a = 0.5f;
											gDLL->getEngineIFace()->fillAreaBorderPlot(pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE(), color, AREA_BORDER_LAYER_BLOCKADING);
										}
									}
								}
							}
						}
					}
				}
			}
		}
	}
}

void CvGame::updateBlockadedPlots()
{
	PROFILE_FUNC();

	gDLL->getEngineIFace()->clearAreaBorderPlots(AREA_BORDER_LAYER_BLOCKADED);

	int iNumPlots = GC.getMapINLINE().numPlots();
	for (int i = 0; i < iNumPlots; ++i)
	{
		CvPlot* pLoopPlot = GC.getMapINLINE().plotByIndex(i);

		FAssert(NULL != pLoopPlot);

		if (pLoopPlot->getBlockadedCount(getActiveTeam()) > 0 && pLoopPlot->isRevealed(getActiveTeam(), false))
		{
			NiColorA color(GC.getColorInfo((ColorTypes)GC.getInfoTypeForString("COLOR_BLACK")).getColor());
			color.a = 0.35f;
			gDLL->getEngineIFace()->fillAreaBorderPlot(pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE(), color, AREA_BORDER_LAYER_BLOCKADED);
		}
	}
}


void CvGame::updateSelectionList()
{
	CvUnit* pHeadSelectedUnit;

	if (GET_PLAYER(getActivePlayer()).isOption(PLAYEROPTION_NO_UNIT_CYCLING))
	{
		return;
	}

	pHeadSelectedUnit = gDLL->getInterfaceIFace()->getHeadSelectedUnit();

	if ((pHeadSelectedUnit == NULL) || !(pHeadSelectedUnit->getGroup()->readyToSelect(true)))
	{
		if ((gDLL->getInterfaceIFace()->getOriginalPlot() == NULL) || !(cyclePlotUnits(gDLL->getInterfaceIFace()->getOriginalPlot(), true, true, gDLL->getInterfaceIFace()->getOriginalPlotCount())))
		{
			if ((gDLL->getInterfaceIFace()->getSelectionPlot() == NULL) || !(cyclePlotUnits(gDLL->getInterfaceIFace()->getSelectionPlot(), true, true)))
			{
				cycleSelectionGroups(true);
			}
		}

		pHeadSelectedUnit = gDLL->getInterfaceIFace()->getHeadSelectedUnit();

		if (pHeadSelectedUnit != NULL)
		{
			if (!(pHeadSelectedUnit->getGroup()->readyToSelect()))
			{
				gDLL->getInterfaceIFace()->clearSelectionList();
			}
		}
	}
}


void CvGame::updateTestEndTurn()
{
	bool bAny;

	bAny = ((gDLL->getInterfaceIFace()->getHeadSelectedUnit() != NULL) && !(GET_PLAYER(getActivePlayer()).isOption(PLAYEROPTION_NO_UNIT_CYCLING)));

	if (GET_PLAYER(getActivePlayer()).isTurnActive())
	{
		if (gDLL->getInterfaceIFace()->isEndTurnMessage())
		{
			if (GET_PLAYER(getActivePlayer()).hasReadyUnit(bAny))
			{
				gDLL->getInterfaceIFace()->setEndTurnMessage(false);
			}
		}
		else
		{
			if (!(GET_PLAYER(getActivePlayer()).hasBusyUnit()) && !(GET_PLAYER(getActivePlayer()).hasReadyUnit(bAny)))
			{
				if (!(gDLL->getInterfaceIFace()->isForcePopup()))
				{
					gDLL->getInterfaceIFace()->setForcePopup(true);
				}
				else
				{
					if (GET_PLAYER(getActivePlayer()).hasAutoUnit())
					{
						if (!(gDLL->shiftKey()))
						{
							CvMessageControl::getInstance().sendAutoMoves();
						}
					}
					else
					{
						if (GET_PLAYER(getActivePlayer()).isOption(PLAYEROPTION_WAIT_END_TURN) || !(gDLL->getInterfaceIFace()->isHasMovedUnit()) || isHotSeat() || isPbem())
						{
							gDLL->getInterfaceIFace()->setEndTurnMessage(true);
						}
						else
						{
							if (gDLL->getInterfaceIFace()->getEndTurnCounter() > 0)
							{
								gDLL->getInterfaceIFace()->changeEndTurnCounter(-1);
							}
							else
							{
								CvMessageControl::getInstance().sendTurnComplete();
								gDLL->getInterfaceIFace()->setEndTurnCounter(3); // XXX
							}
						}
					}
				}
			}
		}
	}
}

CvUnit* CvGame::getPlotUnit(const CvPlot* pPlot, int iIndex) const
{
	PROFILE_FUNC();

	CLLNode<IDInfo>* pUnitNode1;
	CLLNode<IDInfo>* pUnitNode2;
	CvUnit* pLoopUnit1;
	CvUnit* pLoopUnit2;
	int iCount;
	int iPass;
	PlayerTypes activePlayer = getActivePlayer();
	TeamTypes activeTeam = getActiveTeam();

	if (pPlot != NULL)
	{
		iCount = 0;

		for (iPass = 0; iPass < 2; iPass++)
		{
			pUnitNode1 = pPlot->headUnitNode();

			while (pUnitNode1 != NULL)
			{
				pLoopUnit1 = ::getUnit(pUnitNode1->m_data);
				pUnitNode1 = pPlot->nextUnitNode(pUnitNode1);

				if (!(pLoopUnit1->isInvisible(activeTeam, true)))
				{
					if (!(pLoopUnit1->isCargo()))
					{
						if ((pLoopUnit1->getOwnerINLINE() == activePlayer) == (iPass == 0))
						{
							if (iCount == iIndex)
							{
								return pLoopUnit1;
							}

							iCount++;

							//if ((pLoopUnit1->getTeam() == activeTeam) || isDebugMode())
							{
								if (pLoopUnit1->hasCargo())
								{
									pUnitNode2 = pPlot->headUnitNode();

									while (pUnitNode2 != NULL)
									{
										pLoopUnit2 = ::getUnit(pUnitNode2->m_data);
										pUnitNode2 = pPlot->nextUnitNode(pUnitNode2);

										if (!(pLoopUnit2->isInvisible(activeTeam, true)))
										{
											if (pLoopUnit2->getTransportUnit() == pLoopUnit1)
											{
												if (iCount == iIndex)
												{
													return pLoopUnit2;
												}

												iCount++;
											}
										}
									}
								}
							}
						}
					}
				}
			}
		}
	}

	return NULL;
}

void CvGame::getPlotUnits(const CvPlot *pPlot, std::vector<CvUnit *> &plotUnits) const
{
	PROFILE_FUNC();
	plotUnits.erase(plotUnits.begin(), plotUnits.end());

	CLLNode<IDInfo>* pUnitNode1;
	CLLNode<IDInfo>* pUnitNode2;
	CvUnit* pLoopUnit1;
	CvUnit* pLoopUnit2;
	int iPass;
	PlayerTypes activePlayer = getActivePlayer();
	TeamTypes activeTeam = getActiveTeam();

	if (pPlot != NULL)
	{
		for (iPass = 0; iPass < 2; iPass++)
		{
			pUnitNode1 = pPlot->headUnitNode();

			while (pUnitNode1 != NULL)
			{
				pLoopUnit1 = ::getUnit(pUnitNode1->m_data);
				pUnitNode1 = pPlot->nextUnitNode(pUnitNode1);

				if (!(pLoopUnit1->isInvisible(activeTeam, true)))
				{
					if (!(pLoopUnit1->isCargo()))
					{
						if ((pLoopUnit1->getOwnerINLINE() == activePlayer) == (iPass == 0))
						{
							plotUnits.push_back(pLoopUnit1);

							//if ((pLoopUnit1->getTeam() == activeTeam) || isDebugMode())
							{
								if (pLoopUnit1->hasCargo())
								{
									pUnitNode2 = pPlot->headUnitNode();

									while (pUnitNode2 != NULL)
									{
										pLoopUnit2 = ::getUnit(pUnitNode2->m_data);
										pUnitNode2 = pPlot->nextUnitNode(pUnitNode2);

										if (!(pLoopUnit2->isInvisible(activeTeam, true)))
										{
											if (pLoopUnit2->getTransportUnit() == pLoopUnit1)
											{
												plotUnits.push_back(pLoopUnit2);
											}
										}
									}
								}
							}
						}
					}
				}
			}
		}
	}
}

void CvGame::cycleCities(bool bForward, bool bAdd) const
{
	CvCity* pHeadSelectedCity;
	CvCity* pSelectCity;
	CvCity* pLoopCity;
	int iLoop;

	pSelectCity = NULL;

	pHeadSelectedCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();

	if ((pHeadSelectedCity != NULL) && ((pHeadSelectedCity->getTeam() == getActiveTeam()) || isDebugMode()))
	{
		iLoop = pHeadSelectedCity->getIndex();
		iLoop += (bForward ? 1 : -1);

		pLoopCity = GET_PLAYER(pHeadSelectedCity->getOwnerINLINE()).nextCity(&iLoop, !bForward);

		if (pLoopCity == NULL)
		{
			pLoopCity = GET_PLAYER(pHeadSelectedCity->getOwnerINLINE()).firstCity(&iLoop, !bForward);
		}

		if ((pLoopCity != NULL) && (pLoopCity != pHeadSelectedCity))
		{
			pSelectCity = pLoopCity;
		}
	}
	else
	{
		pSelectCity = GET_PLAYER(getActivePlayer()).firstCity(&iLoop, !bForward);
	}

	if (pSelectCity != NULL)
	{
		if (bAdd)
		{
			gDLL->getInterfaceIFace()->clearSelectedCities();
			gDLL->getInterfaceIFace()->addSelectedCity(pSelectCity);
		}
		else
		{
			gDLL->getInterfaceIFace()->selectCity(pSelectCity);
		}
	}
}


void CvGame::cycleSelectionGroups(bool bClear, bool bForward, bool bWorkers) const
{
	CvSelectionGroup* pNextSelectionGroup;
	CvPlot* pPlot;
	CvUnit* pCycleUnit;
	bool bWrap;

	pCycleUnit = gDLL->getInterfaceIFace()->getHeadSelectedUnit();

	if (pCycleUnit != NULL)
	{
		if (pCycleUnit->getOwnerINLINE() != getActivePlayer())
		{
			pCycleUnit = NULL;
		}

		pNextSelectionGroup = GET_PLAYER(getActivePlayer()).cycleSelectionGroups(pCycleUnit, bForward, bWorkers, &bWrap);

		if (bWrap)
		{
			if (GET_PLAYER(getActivePlayer()).hasAutoUnit())
			{
				CvMessageControl::getInstance().sendAutoMoves();
			}
		}
	}
	else
	{
		pPlot = gDLL->getInterfaceIFace()->getLookAtPlot();
		pNextSelectionGroup = GC.getMapINLINE().findSelectionGroup(((pPlot != NULL) ? pPlot->getX() : 0), ((pPlot != NULL) ? pPlot->getY() : 0), getActivePlayer(), true, bWorkers);
	}

	if (pNextSelectionGroup != NULL)
	{
		FAssert(pNextSelectionGroup->getOwnerINLINE() == getActivePlayer());
		gDLL->getInterfaceIFace()->selectUnit(pNextSelectionGroup->getHeadUnit(), bClear);
	}

	if ((pCycleUnit != gDLL->getInterfaceIFace()->getHeadSelectedUnit()) || ((pCycleUnit != NULL) && pCycleUnit->getGroup()->readyToSelect()))
	{
		gDLL->getInterfaceIFace()->lookAtSelectionPlot();
	}
}


// Returns true if unit was cycled...
bool CvGame::cyclePlotUnits(CvPlot* pPlot, bool bForward, bool bAuto, int iCount) const
{
	CLLNode<IDInfo>* pUnitNode;
	CvUnit* pSelectedUnit;
	CvUnit* pLoopUnit = NULL;

	FAssertMsg(iCount >= -1, "iCount expected to be >= -1");

	if (iCount == -1)
	{
		pUnitNode = pPlot->headUnitNode();

		while (pUnitNode != NULL)
		{
			pLoopUnit = ::getUnit(pUnitNode->m_data);

			if (pLoopUnit->IsSelected())
			{
				break;
			}

			pUnitNode = pPlot->nextUnitNode(pUnitNode);
		}
	}
	else
	{
		pUnitNode = pPlot->headUnitNode();

		while (pUnitNode != NULL)
		{
			pLoopUnit = ::getUnit(pUnitNode->m_data);

			if ((iCount - 1) == 0)
			{
				break;
			}

			if (iCount > 0)
			{
				iCount--;
			}

			pUnitNode = pPlot->nextUnitNode(pUnitNode);
		}

		if (pUnitNode == NULL)
		{
			pUnitNode = pPlot->tailUnitNode();

			if (pUnitNode != NULL)
			{
				pLoopUnit = ::getUnit(pUnitNode->m_data);
			}
		}
	}

	if (pUnitNode != NULL)
	{
		pSelectedUnit = pLoopUnit;

		while (true)
		{
			if (bForward)
			{
				pUnitNode = pPlot->nextUnitNode(pUnitNode);
				if (pUnitNode == NULL)
				{
					pUnitNode = pPlot->headUnitNode();
				}
			}
			else
			{
				pUnitNode = pPlot->prevUnitNode(pUnitNode);
				if (pUnitNode == NULL)
				{
					pUnitNode = pPlot->tailUnitNode();
				}
			}

			pLoopUnit = ::getUnit(pUnitNode->m_data);

			if (iCount == -1)
			{
				if (pLoopUnit == pSelectedUnit)
				{
					break;
				}
			}

			if (pLoopUnit->getOwnerINLINE() == getActivePlayer())
			{
				if (bAuto)
				{
					if (pLoopUnit->getGroup()->readyToSelect())
					{
						gDLL->getInterfaceIFace()->selectUnit(pLoopUnit, true);
						return true;
					}
				}
				else
				{
					gDLL->getInterfaceIFace()->insertIntoSelectionList(pLoopUnit, true, false);
					return true;
				}
			}

			if (pLoopUnit == pSelectedUnit)
			{
				break;
			}
		}
	}

	return false;
}

bool CvGame::selectCity(CvCity* pSelectCity, bool bCtrl, bool bAlt, bool bShift) const
{
	if (pSelectCity == NULL || !pSelectCity->canBeSelected())
	{
		return false;
	}

	if (!bShift)
	{
		gDLL->getInterfaceIFace()->clearSelectedCities();
	}

	if (bAlt)
	{
		int iLoop;
		for (CvCity* pLoopCity = GET_PLAYER(pSelectCity->getOwnerINLINE()).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER(pSelectCity->getOwnerINLINE()).nextCity(&iLoop))
		{
			gDLL->getInterfaceIFace()->addSelectedCity(pLoopCity);
		}
	}
	else if (bCtrl)
	{
		int iLoop;
		for (CvCity* pLoopCity = GET_PLAYER(pSelectCity->getOwnerINLINE()).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER(pSelectCity->getOwnerINLINE()).nextCity(&iLoop))
		{
			if (pLoopCity->getArea() == pSelectCity->getArea())
			{
				gDLL->getInterfaceIFace()->addSelectedCity(pLoopCity);
			}
		}
	}
	else
	{
		gDLL->getInterfaceIFace()->addSelectedCity(pSelectCity, bShift);
	}

	return true;
}

void CvGame::selectionListMove(CvPlot* pPlot, bool bAlt, bool bShift, bool bCtrl) const
{
	CLLNode<IDInfo>* pSelectedUnitNode;
	CvUnit* pHeadSelectedUnit;
	CvUnit* pSelectedUnit;
	TeamTypes eRivalTeam;

	if (pPlot == NULL)
	{
		return;
	}

	CyPlot* pyPlot = new CyPlot(pPlot);
	CyArgsList argsList;
	argsList.add(gDLL->getPythonIFace()->makePythonObject(pyPlot));	// pass in plot class
	argsList.add(bAlt);
	argsList.add(bShift);
	argsList.add(bCtrl);
	long lResult=0;
	gDLL->getPythonIFace()->callFunction(PYGameModule, "cannotSelectionListMove", argsList.makeFunctionArgs(), &lResult);
	delete pyPlot;	// python fxn must not hold on to this pointer 
	if (lResult == 1)
	{
		return;
	}

	pHeadSelectedUnit = gDLL->getInterfaceIFace()->getHeadSelectedUnit();

	if ((pHeadSelectedUnit == NULL) || (pHeadSelectedUnit->getOwnerINLINE() != getActivePlayer()))
	{
		return;
	}

	if (bAlt)
	{
		gDLL->getInterfaceIFace()->selectGroup(pHeadSelectedUnit, false, false, true);
	}
	else if (bCtrl)
	{
		gDLL->getInterfaceIFace()->selectGroup(pHeadSelectedUnit, false, true, false);
	}

	pSelectedUnitNode = gDLL->getInterfaceIFace()->headSelectionListNode();

	while (pSelectedUnitNode != NULL)
	{
		pSelectedUnit = ::getUnit(pSelectedUnitNode->m_data);

		eRivalTeam = pSelectedUnit->getDeclareWarMove(pPlot);

		if (eRivalTeam != NO_TEAM)
		{
			CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_DECLAREWARMOVE);
			if (NULL != pInfo)
			{
				pInfo->setData1(eRivalTeam);
				pInfo->setData2(pPlot->getX());
				pInfo->setData3(pPlot->getY());
				pInfo->setOption1(bShift);
				pInfo->setOption2(pPlot->getTeam() != eRivalTeam);
				gDLL->getInterfaceIFace()->addPopup(pInfo);
			}
			return;
		}

		pSelectedUnitNode = gDLL->getInterfaceIFace()->nextSelectionListNode(pSelectedUnitNode);
	}

	selectionListGameNetMessage(GAMEMESSAGE_PUSH_MISSION, MISSION_MOVE_TO, pPlot->getX(), pPlot->getY(), 0, false, bShift);
}


void CvGame::selectionListGameNetMessage(int eMessage, int iData2, int iData3, int iData4, int iFlags, bool bAlt, bool bShift) const
{
	CLLNode<IDInfo>* pSelectedUnitNode;
	CvUnit* pHeadSelectedUnit;
	CvUnit* pSelectedUnit;

	CyArgsList argsList;
	argsList.add(eMessage);	// pass in plot class
	argsList.add(iData2);
	argsList.add(iData3);
	argsList.add(iData4);
	argsList.add(iFlags);
	argsList.add(bAlt);
	argsList.add(bShift);
	long lResult=0;
	gDLL->getPythonIFace()->callFunction(PYGameModule, "cannotSelectionListGameNetMessage", argsList.makeFunctionArgs(), &lResult);
	if (lResult == 1)
	{
		return;
	}

	pHeadSelectedUnit = gDLL->getInterfaceIFace()->getHeadSelectedUnit();

	if (pHeadSelectedUnit != NULL)
	{
		if (pHeadSelectedUnit->getOwnerINLINE() == getActivePlayer())
		{
			if (eMessage == GAMEMESSAGE_JOIN_GROUP)
			{
				pSelectedUnitNode = gDLL->getInterfaceIFace()->headSelectionListNode();

				while (pSelectedUnitNode != NULL)
				{
					pSelectedUnit = ::getUnit(pSelectedUnitNode->m_data);
					pSelectedUnitNode = gDLL->getInterfaceIFace()->nextSelectionListNode(pSelectedUnitNode);

					if (bShift)
					{
						CvMessageControl::getInstance().sendJoinGroup(pSelectedUnit->getID(), FFreeList::INVALID_INDEX);
					}
					else
					{
						if (pSelectedUnit == pHeadSelectedUnit)
						{
							CvMessageControl::getInstance().sendJoinGroup(pSelectedUnit->getID(), FFreeList::INVALID_INDEX);
						}

						CvMessageControl::getInstance().sendJoinGroup(pSelectedUnit->getID(), pHeadSelectedUnit->getID());
					}
				}

				if (bShift)
				{
					gDLL->getInterfaceIFace()->selectUnit(pHeadSelectedUnit, true);
				}
			}
			else if (eMessage == GAMEMESSAGE_DO_COMMAND)
			{
				pSelectedUnitNode = gDLL->getInterfaceIFace()->headSelectionListNode();

				while (pSelectedUnitNode != NULL)
				{
					pSelectedUnit = ::getUnit(pSelectedUnitNode->m_data);
					pSelectedUnitNode = gDLL->getInterfaceIFace()->nextSelectionListNode(pSelectedUnitNode);

					CvMessageControl::getInstance().sendDoCommand(pSelectedUnit->getID(), ((CommandTypes)iData2), iData3, iData4, bAlt);
				}
			}
			else if ((eMessage == GAMEMESSAGE_PUSH_MISSION) || (eMessage == GAMEMESSAGE_AUTO_MISSION))
			{
				if (!(gDLL->getInterfaceIFace()->mirrorsSelectionGroup()))
				{
					selectionListGameNetMessage(GAMEMESSAGE_JOIN_GROUP);
				}

				if (eMessage == GAMEMESSAGE_PUSH_MISSION)
				{
					CvMessageControl::getInstance().sendPushMission(pHeadSelectedUnit->getID(), ((MissionTypes)iData2), iData3, iData4, iFlags, bShift);
				}
				else
				{
					CvMessageControl::getInstance().sendAutoMission(pHeadSelectedUnit->getID());
				}
			}
			else
			{
				FAssert(false);
			}
		}
	}
}


void CvGame::selectedCitiesGameNetMessage(int eMessage, int iData2, int iData3, int iData4, bool bOption, bool bAlt, bool bShift, bool bCtrl) const
{
	CLLNode<IDInfo>* pSelectedCityNode;
	CvCity* pSelectedCity;

	pSelectedCityNode = gDLL->getInterfaceIFace()->headSelectedCitiesNode();

	while (pSelectedCityNode != NULL)
	{
		pSelectedCity = ::getCity(pSelectedCityNode->m_data);
		pSelectedCityNode = gDLL->getInterfaceIFace()->nextSelectedCitiesNode(pSelectedCityNode);

		if (pSelectedCity != NULL)
		{
			if (pSelectedCity->getOwnerINLINE() == getActivePlayer())
			{
				switch (eMessage)
				{
				case GAMEMESSAGE_PUSH_ORDER:
					cityPushOrder(pSelectedCity, ((OrderTypes)iData2), iData3, bAlt, bShift, bCtrl);
					break;

				case GAMEMESSAGE_POP_ORDER:
					if (pSelectedCity->getOrderQueueLength() > 1)
					{
						CvMessageControl::getInstance().sendPopOrder(pSelectedCity->getID(), iData2);
					}
					break;

				case GAMEMESSAGE_DO_TASK:
					CvMessageControl::getInstance().sendDoTask(pSelectedCity->getID(), ((TaskTypes)iData2), iData3, iData4, bOption, bAlt, bShift, bCtrl);
					break;

				default:
					FAssert(false);
					break;
				}
			}
		}
	}
}


bool CvGame::canHandleAction(int iAction, CvPlot* pPlot, bool bTestVisible, bool bUseCache) const
{
	PROFILE_FUNC();

	CvSelectionGroup* pSelectedGroup;
	CvUnit* pHeadSelectedUnit;
	CvPlot* pMissionPlot;
	bool bShift = gDLL->shiftKey();

	if(GC.getUSE_CANNOT_HANDLE_ACTION_CALLBACK())
	{
		CyPlot* pyPlot = new CyPlot(pPlot);
		CyArgsList argsList;
		argsList.add(gDLL->getPythonIFace()->makePythonObject(pyPlot));	// pass in plot class
		argsList.add(iAction);
		argsList.add(bTestVisible);
		long lResult=0;
		gDLL->getPythonIFace()->callFunction(PYGameModule, "cannotHandleAction", argsList.makeFunctionArgs(), &lResult);
		delete pyPlot;	// python fxn must not hold on to this pointer 
		if (lResult == 1)
		{
			return false;
		}
	}

	if (GC.getActionInfo(iAction).getControlType() != NO_CONTROL)
	{
		if (canDoControl((ControlTypes)(GC.getActionInfo(iAction).getControlType())))
		{
			return true;
		}
	}

	if (gDLL->getInterfaceIFace()->isCitySelection())
	{
		return false; // XXX hack!
	}

	pHeadSelectedUnit = gDLL->getInterfaceIFace()->getHeadSelectedUnit();

	if (pHeadSelectedUnit != NULL)
	{
		if (pHeadSelectedUnit->getOwnerINLINE() == getActivePlayer())
		{
			if (isMPOption(MPOPTION_SIMULTANEOUS_TURNS) || GET_PLAYER(pHeadSelectedUnit->getOwnerINLINE()).isTurnActive())
			{
				CvSelectionGroup* pSelectedInterfaceList = gDLL->getInterfaceIFace()->getSelectionList();

				if (GC.getActionInfo(iAction).getMissionType() != NO_MISSION)
				{
					if (gDLL->getInterfaceIFace()->mirrorsSelectionGroup())
					{
						pSelectedGroup = pHeadSelectedUnit->getGroup();

						if (pPlot != NULL)
						{
							pMissionPlot = pPlot;
						}
						else if (bShift)
						{
							pMissionPlot = pSelectedGroup->lastMissionPlot();
						}
						else
						{
							pMissionPlot = NULL;
						}

						if ((pMissionPlot == NULL) || !(pMissionPlot->isVisible(pHeadSelectedUnit->getTeam(), false)))
						{
							pMissionPlot = pSelectedGroup->plot();
						}

					}
					else
					{
						pMissionPlot = pSelectedInterfaceList->plot();
					}

					if (pSelectedInterfaceList->canStartMission(GC.getActionInfo(iAction).getMissionType(), GC.getActionInfo(iAction).getMissionData(), -1, pMissionPlot, bTestVisible, bUseCache))
					{
						return true;
					}
				}

				if (GC.getActionInfo(iAction).getCommandType() != NO_COMMAND)
				{
					if (pSelectedInterfaceList->canDoCommand(((CommandTypes)(GC.getActionInfo(iAction).getCommandType())), GC.getActionInfo(iAction).getCommandData(), -1, bTestVisible, bUseCache))
					{
						return true;
					}
				}

				if (gDLL->getInterfaceIFace()->canDoInterfaceMode(((InterfaceModeTypes)GC.getActionInfo(iAction).getInterfaceModeType()), pSelectedInterfaceList))
				{
					return true;
				}
			}
		}
	}

	return false;
}

void CvGame::setupActionCache() const
{
	gDLL->getInterfaceIFace()->getSelectionList()->setupActionCache();
}

void CvGame::handleAction(int iAction)
{
	CvUnit* pHeadSelectedUnit;
	bool bAlt;
	bool bShift;
	bool bSkip;

	bAlt = gDLL->altKey();
	bShift = gDLL->shiftKey();

	if (!(gDLL->getInterfaceIFace()->canHandleAction(iAction)))
	{
		return;
	}

	if (GC.getActionInfo(iAction).getControlType() != NO_CONTROL)
	{
		doControl((ControlTypes)(GC.getActionInfo(iAction).getControlType()));
	}

	if (gDLL->getInterfaceIFace()->canDoInterfaceMode((InterfaceModeTypes)GC.getActionInfo(iAction).getInterfaceModeType(), gDLL->getInterfaceIFace()->getSelectionList()))
	{
		pHeadSelectedUnit = gDLL->getInterfaceIFace()->getHeadSelectedUnit();

		if (pHeadSelectedUnit != NULL)
		{
			if (GC.getInterfaceModeInfo((InterfaceModeTypes)GC.getActionInfo(iAction).getInterfaceModeType()).getSelectAll())
			{
				gDLL->getInterfaceIFace()->selectGroup(pHeadSelectedUnit, false, false, true);
			}
			else if (GC.getInterfaceModeInfo((InterfaceModeTypes)GC.getActionInfo(iAction).getInterfaceModeType()).getSelectType())
			{
				gDLL->getInterfaceIFace()->selectGroup(pHeadSelectedUnit, false, true, false);
			}
		}

		gDLL->getInterfaceIFace()->setInterfaceMode((InterfaceModeTypes)GC.getActionInfo(iAction).getInterfaceModeType());
	}

	if (GC.getActionInfo(iAction).getMissionType() != NO_MISSION)
	{
		selectionListGameNetMessage(GAMEMESSAGE_PUSH_MISSION, GC.getActionInfo(iAction).getMissionType(), GC.getActionInfo(iAction).getMissionData(), -1, 0, false, bShift);
	}

	if (GC.getActionInfo(iAction).getCommandType() != NO_COMMAND)
	{
		bSkip = false;

		if (GC.getActionInfo(iAction).getCommandType() == COMMAND_LOAD)
		{
			CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_LOADUNIT);
			if (NULL != pInfo)
			{
				gDLL->getInterfaceIFace()->addPopup(pInfo);
				bSkip = true;
			}
		}

		if (!bSkip)
		{
			if (GC.getActionInfo(iAction).isConfirmCommand())
			{
				CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_CONFIRMCOMMAND);
				if (NULL != pInfo)
				{
					pInfo->setData1(iAction);
					pInfo->setOption1(bAlt);
					gDLL->getInterfaceIFace()->addPopup(pInfo);
				}
			}
			else
			{
				selectionListGameNetMessage(GAMEMESSAGE_DO_COMMAND, GC.getActionInfo(iAction).getCommandType(), GC.getActionInfo(iAction).getCommandData(), -1, 0, bAlt);
			}
		}
	}
}


bool CvGame::canDoControl(ControlTypes eControl) const
{
	CyArgsList argsList;
	argsList.add(eControl);
	long lResult=0;
	gDLL->getPythonIFace()->callFunction(PYGameModule, "cannotDoControl", argsList.makeFunctionArgs(), &lResult);
	if (lResult == 1)
	{
		return false;
	}

	switch (eControl)
	{
	case CONTROL_SELECTYUNITTYPE:
	case CONTROL_SELECTYUNITALL:
	case CONTROL_SELECT_HEALTHY:
	case CONTROL_SELECTCITY:
	case CONTROL_SELECTCAPITAL:
	case CONTROL_NEXTUNIT:
	case CONTROL_PREVUNIT:
	case CONTROL_CYCLEUNIT:
	case CONTROL_CYCLEUNIT_ALT:
	case CONTROL_CYCLEWORKER:
	case CONTROL_LASTUNIT:
	case CONTROL_AUTOMOVES:
	case CONTROL_SAVE_GROUP:
	case CONTROL_QUICK_SAVE:
	case CONTROL_QUICK_LOAD:
	case CONTROL_ORTHO_CAMERA:
	case CONTROL_CYCLE_CAMERA_FLYING_MODES:
	case CONTROL_ISOMETRIC_CAMERA_LEFT:
	case CONTROL_ISOMETRIC_CAMERA_RIGHT:
	case CONTROL_FLYING_CAMERA:
	case CONTROL_MOUSE_FLYING_CAMERA:
	case CONTROL_TOP_DOWN_CAMERA:
	case CONTROL_TURN_LOG:
	case CONTROL_CHAT_ALL:
	case CONTROL_CHAT_TEAM:
	case CONTROL_GLOBE_VIEW:
		if (!gDLL->getInterfaceIFace()->isFocused())
		{
			return true;
		}
		break;

	case CONTROL_FORCEENDTURN:
		if (!gDLL->getInterfaceIFace()->isFocused() && !gDLL->getInterfaceIFace()->isInAdvancedStart())
		{
			return true;
		}
		break;


	case CONTROL_PING:
	case CONTROL_SIGN:
	case CONTROL_GRID:
	case CONTROL_BARE_MAP:
	case CONTROL_YIELDS:
	case CONTROL_RESOURCE_ALL:
	case CONTROL_UNIT_ICONS:
	case CONTROL_GLOBELAYER:
	case CONTROL_SCORES:
	case CONTROL_FREE_COLONY:
		if (!gDLL->getInterfaceIFace()->isFocusedWidget())
		{
			return true;
		}
		break;

	case CONTROL_OPTIONS_SCREEN:
	case CONTROL_DOMESTIC_SCREEN:
	case CONTROL_VICTORY_SCREEN:
	case CONTROL_CIVILOPEDIA:
	case CONTROL_RELIGION_SCREEN:
	case CONTROL_CORPORATION_SCREEN:
	case CONTROL_CIVICS_SCREEN:
	case CONTROL_FOREIGN_SCREEN:
	case CONTROL_FINANCIAL_SCREEN:
	case CONTROL_MILITARY_SCREEN:
	case CONTROL_TECH_CHOOSER:
	case CONTROL_DIPLOMACY:
	case CONTROL_HALL_OF_FAME:
	case CONTROL_INFO:
	case CONTROL_DETAILS:
	case CONTROL_SAVE_NORMAL:
		return true;
		break;
	case CONTROL_ESPIONAGE_SCREEN:
		if (!isOption(GAMEOPTION_NO_ESPIONAGE))
		{
			return true;
		}
		break;

	case CONTROL_NEXTCITY:
	case CONTROL_PREVCITY:
		if (!gDLL->getInterfaceIFace()->isSpaceshipScreenUp())
		{
			return true;
		}
		break;

	case CONTROL_ADMIN_DETAILS:
		return true;
		break;

	case CONTROL_CENTERONSELECTION:
		if (gDLL->getInterfaceIFace()->getLookAtPlot() != gDLL->getInterfaceIFace()->getSelectionPlot())
		{
			return true;
		}
		break;

	case CONTROL_LOAD_GAME:
		if (!(isNetworkMultiPlayer()))
		{
			return true;
		}
		break;

	case CONTROL_RETIRE:
		if ((getGameState() == GAMESTATE_ON) || isGameMultiPlayer())
		{
			if (GET_PLAYER(getActivePlayer()).isAlive())
			{
				if (isPbem() || isHotSeat())
				{
					if (!GET_PLAYER(getActivePlayer()).isEndTurn())
					{
						return true;
					}
				}
				else
				{
					return true;
				}
			}
		}
		break;

	case CONTROL_WORLD_BUILDER:
		if (!(isGameMultiPlayer()) && GC.getInitCore().getAdminPassword().empty() && !gDLL->getInterfaceIFace()->isInAdvancedStart())
		{
			return true;
		}
		break;

	case CONTROL_ENDTURN:
	case CONTROL_ENDTURN_ALT:
		if (gDLL->getInterfaceIFace()->isEndTurnMessage() && !gDLL->getInterfaceIFace()->isFocused() && !gDLL->getInterfaceIFace()->isInAdvancedStart())
		{
			return true;
		}
		break;

	default:
		FAssertMsg(false, "eControl did not match any valid options");
		break;
	}

	return false;
}


void CvGame::doControl(ControlTypes eControl)
{
	CvPopupInfo* pInfo;
	CvCity* pCapitalCity;
	CvUnit* pHeadSelectedUnit;
	CvUnit* pUnit;
	CvPlot* pPlot;

	if (!canDoControl(eControl))
	{
		return;
	}

	switch (eControl)
	{
	case CONTROL_CENTERONSELECTION:
		gDLL->getInterfaceIFace()->lookAtSelectionPlot();
		break;

	case CONTROL_SELECTYUNITTYPE:
		pHeadSelectedUnit = gDLL->getInterfaceIFace()->getHeadSelectedUnit();
		if (pHeadSelectedUnit != NULL)
		{
			gDLL->getInterfaceIFace()->selectGroup(pHeadSelectedUnit, false, true, false);
		}
		break;

	case CONTROL_SELECTYUNITALL:
		pHeadSelectedUnit = gDLL->getInterfaceIFace()->getHeadSelectedUnit();
		if (pHeadSelectedUnit != NULL)
		{
			gDLL->getInterfaceIFace()->selectGroup(pHeadSelectedUnit, false, false, true);
		}
		break;

	case CONTROL_SELECT_HEALTHY:
		{
			CvUnit* pGroupHead = NULL;
			pHeadSelectedUnit = gDLL->getInterfaceIFace()->getHeadSelectedUnit();
			gDLL->getInterfaceIFace()->clearSelectionList();
			if (pHeadSelectedUnit != NULL)
			{
				CvPlot* pPlot = pHeadSelectedUnit->plot();
				std::vector<CvUnit *> plotUnits;
				getPlotUnits(pPlot, plotUnits);
				gDLL->getInterfaceIFace()->selectionListPreChange();
				for (int iI = 0; iI < (int) plotUnits.size(); iI++)
				{
					pUnit = plotUnits[iI];

					if (pUnit->getOwnerINLINE() == getActivePlayer())
					{
						if (!isMPOption(MPOPTION_SIMULTANEOUS_TURNS) || getTurnSlice() - pUnit->getLastMoveTurn() > GC.getDefineINT("MIN_TIMER_UNIT_DOUBLE_MOVES"))
						{
							if (pUnit->isHurt())
							{
								if (pGroupHead != NULL)
								{
									CvMessageControl::getInstance().sendJoinGroup(pUnit->getID(), pGroupHead->getID());
								}
								else
								{
									pGroupHead = pUnit;
								}

								gDLL->getInterfaceIFace()->insertIntoSelectionList(pUnit, false, false, true, true, true);
							}
						}
					}
				}

				gDLL->getInterfaceIFace()->selectionListPostChange();
			}
		}
		break;

	case CONTROL_SELECTCITY:
		if (gDLL->getInterfaceIFace()->isCityScreenUp())
		{
			cycleCities();
		}
		else
		{
			gDLL->getInterfaceIFace()->selectLookAtCity();
		}
		break;

	case CONTROL_SELECTCAPITAL:
		pCapitalCity = GET_PLAYER(getActivePlayer()).getCapitalCity();
		if (pCapitalCity != NULL)
		{
			gDLL->getInterfaceIFace()->selectCity(pCapitalCity);
		}
		break;

	case CONTROL_NEXTCITY:
		if (gDLL->getInterfaceIFace()->isCitySelection())
		{
			cycleCities(true, !(gDLL->getInterfaceIFace()->isCityScreenUp()));
		}
		else
		{
			gDLL->getInterfaceIFace()->selectLookAtCity(true);
		}
		gDLL->getInterfaceIFace()->lookAtSelectionPlot();
		break;

	case CONTROL_PREVCITY:
		if (gDLL->getInterfaceIFace()->isCitySelection())
		{
			cycleCities(false, !(gDLL->getInterfaceIFace()->isCityScreenUp()));
		}
		else
		{
			gDLL->getInterfaceIFace()->selectLookAtCity(true);
		}
		gDLL->getInterfaceIFace()->lookAtSelectionPlot();
		break;

	case CONTROL_NEXTUNIT:
		pPlot = gDLL->getInterfaceIFace()->getSelectionPlot();
		if (pPlot != NULL)
		{
			cyclePlotUnits(pPlot);
		}
		break;

	case CONTROL_PREVUNIT:
		pPlot = gDLL->getInterfaceIFace()->getSelectionPlot();
		if (pPlot != NULL)
		{
			cyclePlotUnits(pPlot, false);
		}
		break;

	case CONTROL_CYCLEUNIT:
	case CONTROL_CYCLEUNIT_ALT:
		cycleSelectionGroups(true);
		break;

	case CONTROL_CYCLEWORKER:
		cycleSelectionGroups(true, true, true);
		break;

	case CONTROL_LASTUNIT:
		pUnit = gDLL->getInterfaceIFace()->getLastSelectedUnit();

		if (pUnit != NULL)
		{
			gDLL->getInterfaceIFace()->selectUnit(pUnit, true);
			gDLL->getInterfaceIFace()->lookAtSelectionPlot();
		}
		else
		{
			cycleSelectionGroups(true, false);
		}

		gDLL->getInterfaceIFace()->setLastSelectedUnit(NULL);
		break;

	case CONTROL_ENDTURN:
	case CONTROL_ENDTURN_ALT:
		if (gDLL->getInterfaceIFace()->isEndTurnMessage())
		{
			CvMessageControl::getInstance().sendTurnComplete();
		}
		break;

	case CONTROL_FORCEENDTURN:
		CvMessageControl::getInstance().sendTurnComplete();
		break;

	case CONTROL_AUTOMOVES:
		CvMessageControl::getInstance().sendAutoMoves();
		break;

	case CONTROL_PING:
		gDLL->getInterfaceIFace()->setInterfaceMode(INTERFACEMODE_PING);
		break;

	case CONTROL_SIGN:
		gDLL->getInterfaceIFace()->setInterfaceMode(INTERFACEMODE_SIGN);
		break;

	case CONTROL_GRID:
		gDLL->getEngineIFace()->SetGridMode(!(gDLL->getEngineIFace()->GetGridMode()));
		break;

	case CONTROL_BARE_MAP:
		gDLL->getInterfaceIFace()->toggleBareMapMode();
		break;

	case CONTROL_YIELDS:
		gDLL->getInterfaceIFace()->toggleYieldVisibleMode();
		break;

	case CONTROL_RESOURCE_ALL:
		gDLL->getEngineIFace()->toggleResourceLayer();
		break;

	case CONTROL_UNIT_ICONS:
		gDLL->getEngineIFace()->toggleUnitLayer();
		break;

	case CONTROL_GLOBELAYER:
		gDLL->getEngineIFace()->toggleGlobeview();
		break;

	case CONTROL_SCORES:
		gDLL->getInterfaceIFace()->toggleScoresVisible();
		break;

	case CONTROL_LOAD_GAME:
		gDLL->LoadGame();
		break;

	case CONTROL_OPTIONS_SCREEN:
		gDLL->getPythonIFace()->callFunction("CvScreensInterface", "showOptionsScreen");
		break;

	case CONTROL_RETIRE:
		if (!isGameMultiPlayer() || countHumanPlayersAlive() == 1)
		{
			if (gDLL->GetAutorun())
			{
				GC.getInitCore().setSlotStatus(getActivePlayer(), SS_COMPUTER);
			}
			else
			{
				setGameState(GAMESTATE_OVER);
				gDLL->getInterfaceIFace()->setDirty(Soundtrack_DIRTY_BIT, true);
			}
		}
		else
		{
			if (isNetworkMultiPlayer())
			{
				gDLL->sendMPRetire();
				gDLL->getInterfaceIFace()->exitingToMainMenu();
			}
			else
			{
				gDLL->handleRetirement(getActivePlayer());
			}
		}
		break;

	case CONTROL_SAVE_GROUP:
		gDLL->SaveGame(SAVEGAME_GROUP);
		break;

	case CONTROL_SAVE_NORMAL:
		gDLL->SaveGame(SAVEGAME_NORMAL);
		break;

	case CONTROL_QUICK_SAVE:
		if (!(isNetworkMultiPlayer()))	// SP only!
		{
			gDLL->QuickSave();
		}
		break;

	case CONTROL_QUICK_LOAD:
		if (!(isNetworkMultiPlayer()))	// SP only!
		{
			gDLL->QuickLoad();
		}
		break;

	case CONTROL_ORTHO_CAMERA:
		gDLL->getEngineIFace()->SetOrthoCamera(!(gDLL->getEngineIFace()->GetOrthoCamera()));
		break;

	case CONTROL_CYCLE_CAMERA_FLYING_MODES:
		gDLL->getEngineIFace()->CycleFlyingMode(1);
		break;

	case CONTROL_ISOMETRIC_CAMERA_LEFT:
		gDLL->getEngineIFace()->MoveBaseTurnLeft();
		break;

	case CONTROL_ISOMETRIC_CAMERA_RIGHT:
		gDLL->getEngineIFace()->MoveBaseTurnRight();
		break;

	case CONTROL_FLYING_CAMERA:
		gDLL->getEngineIFace()->SetFlying(!(gDLL->getEngineIFace()->GetFlying()));
		break;

	case CONTROL_MOUSE_FLYING_CAMERA:
		gDLL->getEngineIFace()->SetMouseFlying(!(gDLL->getEngineIFace()->GetMouseFlying()));
		break;

	case CONTROL_TOP_DOWN_CAMERA:
		gDLL->getEngineIFace()->SetSatelliteMode(!(gDLL->getEngineIFace()->GetSatelliteMode()));
		break;

	case CONTROL_CIVILOPEDIA:
		gDLL->getPythonIFace()->callFunction(PYScreensModule, "pediaShow");
		break;

	case CONTROL_RELIGION_SCREEN:
		gDLL->getPythonIFace()->callFunction(PYScreensModule, "showReligionScreen");
		break;

	case CONTROL_CORPORATION_SCREEN:
		gDLL->getPythonIFace()->callFunction(PYScreensModule, "showCorporationScreen");
		break;

	case CONTROL_CIVICS_SCREEN:
		gDLL->getPythonIFace()->callFunction(PYScreensModule, "showCivicsScreen");
		break;

	case CONTROL_FOREIGN_SCREEN:
		{
			CyArgsList argsList;
			argsList.add(-1);
			gDLL->getPythonIFace()->callFunction(PYScreensModule, "showForeignAdvisorScreen", argsList.makeFunctionArgs());
		}
		break;

	case CONTROL_FINANCIAL_SCREEN:
		gDLL->getPythonIFace()->callFunction(PYScreensModule, "showFinanceAdvisor");
		break;

	case CONTROL_MILITARY_SCREEN:
		gDLL->getPythonIFace()->callFunction(PYScreensModule, "showMilitaryAdvisor");
		break;

	case CONTROL_TECH_CHOOSER:
		gDLL->getPythonIFace()->callFunction(PYScreensModule, "showTechChooser");
		break;

	case CONTROL_TURN_LOG:
		if (!gDLL->GetWorldBuilderMode() || gDLL->getInterfaceIFace()->isInAdvancedStart())
		{
			gDLL->getInterfaceIFace()->toggleTurnLog();
		}
		break;

	case CONTROL_CHAT_ALL:
		if (!gDLL->GetWorldBuilderMode() || gDLL->getInterfaceIFace()->isInAdvancedStart())
		{
			gDLL->getInterfaceIFace()->showTurnLog(CHATTARGET_ALL);
		}
		break;

	case CONTROL_CHAT_TEAM:
		if (!gDLL->GetWorldBuilderMode() || gDLL->getInterfaceIFace()->isInAdvancedStart())
		{
			gDLL->getInterfaceIFace()->showTurnLog(CHATTARGET_TEAM);
		}
		break;

	case CONTROL_DOMESTIC_SCREEN:
		{
			CyArgsList argsList;
			argsList.add(-1);
			gDLL->getPythonIFace()->callFunction(PYScreensModule, "showDomesticAdvisor", argsList.makeFunctionArgs());
		}
		break;

	case CONTROL_VICTORY_SCREEN:
		gDLL->getPythonIFace()->callFunction(PYScreensModule, "showVictoryScreen");
		break;

	case CONTROL_INFO:
		{
			CyArgsList args;
			args.add(0);
			args.add(getGameState() == GAMESTATE_ON ? 0 : 1);
			gDLL->getPythonIFace()->callFunction(PYScreensModule, "showInfoScreen", args.makeFunctionArgs());
		}
		break;

	case CONTROL_GLOBE_VIEW:
		gDLL->getEngineIFace()->toggleGlobeview();
		break;

	case CONTROL_DETAILS:
		gDLL->getInterfaceIFace()->showDetails();
		break;

	case CONTROL_ADMIN_DETAILS:
		if (GC.getInitCore().getAdminPassword().empty())
		{
			gDLL->getInterfaceIFace()->showAdminDetails();
		}
		else
		{
			CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_ADMIN_PASSWORD);
			if (NULL != pInfo)
			{
				pInfo->setData1((int)CONTROL_ADMIN_DETAILS);
				gDLL->getInterfaceIFace()->addPopup(pInfo, NO_PLAYER, true);
			}
		}
		break;

	case CONTROL_HALL_OF_FAME:
		{
			CyArgsList args;
			args.add(true);
			gDLL->getPythonIFace()->callFunction(PYScreensModule, "showHallOfFame", args.makeFunctionArgs());
		}
		break;

	case CONTROL_WORLD_BUILDER:
		if (GC.getInitCore().getAdminPassword().empty())
		{
			gDLL->getInterfaceIFace()->setWorldBuilder(!(gDLL->GetWorldBuilderMode()));
		}
		else
		{
			CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_ADMIN_PASSWORD);
			if (NULL != pInfo)
			{
				pInfo->setData1((int)CONTROL_WORLD_BUILDER);
				gDLL->getInterfaceIFace()->addPopup(pInfo, NO_PLAYER, true);
			}
		}
		break;

	case CONTROL_ESPIONAGE_SCREEN:
		gDLL->getPythonIFace()->callFunction(PYScreensModule, "showEspionageAdvisor");
		break;

	case CONTROL_FREE_COLONY:
		{
			CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_FREE_COLONY);
			if (pInfo)
			{
				gDLL->getInterfaceIFace()->addPopup(pInfo);
			}
		}
		break;

	case CONTROL_DIPLOMACY:
		pInfo = new CvPopupInfo(BUTTONPOPUP_DIPLOMACY);
		if (NULL != pInfo)
		{
			gDLL->getInterfaceIFace()->addPopup(pInfo);
		}
		break;

	default:
		FAssertMsg(false, "eControl did not match any valid options");
		break;
	}
}

void CvGame::getGlobeLayers(std::vector<CvGlobeLayerData>& aLayers) const
{
	CvGlobeLayerData kUnit(GLOBE_LAYER_UNIT);
	kUnit.m_strName = "UNITS";
	kUnit.m_strButtonHelpTag = "TXT_KEY_GLOBELAYER_UNITS";
	kUnit.m_strButtonStyle = "Button_HUDGlobeUnit_Style";
	kUnit.m_iNumOptions = NUM_UNIT_OPTION_TYPES;
	kUnit.m_bGlobeViewRequired = false;
	aLayers.push_back(kUnit);

	CvGlobeLayerData kResource(GLOBE_LAYER_RESOURCE);
	kResource.m_strName = "RESOURCES";
	kResource.m_strButtonHelpTag = "TXT_KEY_GLOBELAYER_RESOURCES";
	kResource.m_strButtonStyle = "Button_HUDBtnResources_Style";
	kResource.m_iNumOptions = NUM_RESOURCE_OPTION_TYPES;
	kResource.m_bGlobeViewRequired = false;
	aLayers.push_back(kResource);

	CvGlobeLayerData kCulture(GLOBE_LAYER_CULTURE);
	kCulture.m_strName = "CULTURE";
	kCulture.m_strButtonHelpTag = "TXT_KEY_GLOBELAYER_CULTURE";
	kCulture.m_strButtonStyle = "Button_HUDGlobeCulture_Style";
	kCulture.m_bShouldCitiesZoom = true;
	aLayers.push_back(kCulture);

	CvGlobeLayerData kTrade(GLOBE_LAYER_TRADE);
	kTrade.m_strName = "TRADE";
	kTrade.m_strButtonHelpTag = "TXT_KEY_GLOBELAYER_TRADE";
	kTrade.m_strButtonStyle = "Button_HUDGlobeTrade_Style";
	kTrade.m_bShouldCitiesZoom = true;
	aLayers.push_back(kTrade);

	CvGlobeLayerData kReligion(GLOBE_LAYER_RELIGION);
	kReligion.m_strName = "RELIGION";
	kReligion.m_strButtonHelpTag = "TXT_KEY_GLOBELAYER_RELIGION";
	kReligion.m_strButtonStyle = "Button_HUDGlobeReligion_Style";
	kReligion.m_iNumOptions = GC.getNumReligionInfos();
	kReligion.m_bShouldCitiesZoom = true;
	aLayers.push_back(kReligion);
}

void CvGame::startFlyoutMenu(const CvPlot* pPlot, std::vector<CvFlyoutMenuData>& aFlyoutItems) const
{
	aFlyoutItems.clear();

	bool bUnits = false;
	bool bFortifyUnit = false;
	bool bSleepUnit = false;
	bool bWakeUnit = false;
	CLLNode<IDInfo>* pUnitNode = pPlot->headUnitNode();
	while (pUnitNode != NULL)
	{
		CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = pPlot->nextUnitNode(pUnitNode);

		if (pLoopUnit->getOwnerINLINE() == getActivePlayer())
		{
			bUnits = true;

			if (pLoopUnit->canFortify(pPlot))
			{
				bFortifyUnit = true;
			}
			else if (pLoopUnit->canSleep(pPlot))
			{
				bSleepUnit = true;
			}
			else if (pLoopUnit->isWaiting())
			{
				bWakeUnit = true;
			}
		}
	}

	CvWString szBuffer;
	CvCity* pCity = pPlot->getPlotCity();
	if (pCity != NULL)
	{
		if (pCity->getOwnerINLINE() == getActivePlayer())
		{
			szBuffer = gDLL->getText("TXT_KEY_CHANGE_PRODUCTION");
			aFlyoutItems.push_back(CvFlyoutMenuData(NO_FLYOUT, -1, -1, -1, szBuffer));
			for (int iI = 0; iI < GC.getNumUnitClassInfos(); iI++)
			{
				UnitTypes eLoopUnit = (UnitTypes) GC.getCivilizationInfo(pCity->getCivilizationType()).getCivilizationUnits(iI);
				if (eLoopUnit != NO_UNIT)
				{
					if (pCity->canTrain(eLoopUnit))
					{
						szBuffer.Format(L"%s (%d)", GC.getUnitInfo(eLoopUnit).getDescription(), pCity->getProductionTurnsLeft(eLoopUnit, 0));
						aFlyoutItems.push_back(CvFlyoutMenuData(FLYOUT_TRAIN, eLoopUnit, pPlot->getX_INLINE(), pPlot->getY_INLINE(), szBuffer));
					}
				}
			}

			for (int iI = 0; iI < GC.getNumBuildingClassInfos(); iI++)
			{
				BuildingTypes eLoopBuilding = (BuildingTypes)GC.getCivilizationInfo(pCity->getCivilizationType()).getCivilizationBuildings(iI);
				if (eLoopBuilding != NO_BUILDING)
				{
					if (pCity->canConstruct(eLoopBuilding))
					{
						szBuffer.Format(L"%s (%d)", GC.getBuildingInfo(eLoopBuilding).getDescription(), pCity->getProductionTurnsLeft(eLoopBuilding, 0));
						aFlyoutItems.push_back(CvFlyoutMenuData(FLYOUT_CONSTRUCT, eLoopBuilding, pPlot->getX_INLINE(), pPlot->getY_INLINE(), szBuffer));
					}
				}
			}

			for (int iI = 0; iI < GC.getNumProjectInfos(); iI++)
			{
				ProjectTypes eProject = (ProjectTypes) iI;
				if (pCity->canCreate(eProject))
				{
					szBuffer.Format(L"%s (%d)", GC.getProjectInfo(eProject).getDescription(), pCity->getProductionTurnsLeft(eProject, 0));
					aFlyoutItems.push_back(CvFlyoutMenuData(FLYOUT_CREATE, eProject, pPlot->getX_INLINE(), pPlot->getY_INLINE(), szBuffer));
				}
			}

			for (int iI = 0; iI < GC.getNumProcessInfos(); iI++)
			{
				if (pCity->canMaintain((ProcessTypes)iI))
				{
					szBuffer = GC.getProcessInfo((ProcessTypes)iI).getDescription();
					aFlyoutItems.push_back(CvFlyoutMenuData(FLYOUT_MAINTAIN, iI, pPlot->getX_INLINE(), pPlot->getY_INLINE(), szBuffer));
				}
			}


			aFlyoutItems.push_back(CvFlyoutMenuData(NO_FLYOUT, -1, -1, -1, L""));

			for (int iI = 0; iI < GC.getNumHurryInfos(); iI++)
			{
				if (pCity->canHurry((HurryTypes)iI))
				{
					szBuffer = gDLL->getText("TXT_KEY_HURRY_PRODUCTION");

					int iHurryGold = pCity->hurryGold((HurryTypes)iI);
					if (iHurryGold > 0)
					{
						szBuffer += gDLL->getText("TXT_KEY_HURRY_PRODUCTION_GOLD", iHurryGold);
					}

					int iHurryPopulation = pCity->hurryPopulation((HurryTypes)iI);
					if (iHurryPopulation > 0)
					{
						szBuffer += gDLL->getText("TXT_KEY_HURRY_PRODUCTION_POP", iHurryPopulation);
					}

					aFlyoutItems.push_back(CvFlyoutMenuData(FLYOUT_HURRY, iI, pPlot->getX_INLINE(), pPlot->getY_INLINE(), szBuffer));
				}
			}

			if (pCity->canConscript())
			{
				UnitTypes eConscriptUnit = pCity->getConscriptUnit();
				if (eConscriptUnit != NO_UNIT)
				{
					szBuffer = gDLL->getText("TXT_KEY_DRAFT_UNIT", GC.getUnitInfo(eConscriptUnit).getDescription(), pCity->getConscriptPopulation());
					aFlyoutItems.push_back(CvFlyoutMenuData(FLYOUT_CONSCRIPT, iI, pPlot->getX_INLINE(), pPlot->getY_INLINE(), szBuffer));
				}
			}
		}
	}

	CvUnit* pHeadSelectedUnit = gDLL->getInterfaceIFace()->getHeadSelectedUnit();
	if (pHeadSelectedUnit != NULL && !pHeadSelectedUnit->atPlot(pPlot))
	{
		gDLL->getFAStarIFace()->SetData(&GC.getInterfacePathFinder(), gDLL->getInterfaceIFace()->getSelectionList());
		if ((pHeadSelectedUnit->getDomainType() == DOMAIN_AIR) || gDLL->getFAStarIFace()->GeneratePath(&GC.getInterfacePathFinder(), pHeadSelectedUnit->getX(), pHeadSelectedUnit->getY(), pPlot->getX(), pPlot->getY(), false, MOVE_DECLARE_WAR, true))
		{
			if (pHeadSelectedUnit->getDomainType() == DOMAIN_AIR)
			{
				szBuffer = gDLL->getText("TXT_KEY_FLYOUT_MENU_FLY_TO");
			}
			else
			{
				szBuffer = gDLL->getText("TXT_KEY_FLYOUT_MENU_MOVE_TO", gDLL->getFAStarIFace()->GetLastNode(&GC.getInterfacePathFinder())->m_iData2);
			}
			aFlyoutItems.push_back(CvFlyoutMenuData(FLYOUT_MOVE_TO, 0, pPlot->getX_INLINE(), pPlot->getY_INLINE(), szBuffer));
		}
	}

	if (bUnits)
	{
		szBuffer = gDLL->getText("TXT_KEY_FLYOUT_MENU_SELECT_ALL");
		aFlyoutItems.push_back(CvFlyoutMenuData(FLYOUT_SELECT_ALL, 0, pPlot->getX_INLINE(), pPlot->getY_INLINE(), szBuffer));

		if (bWakeUnit)
		{
			szBuffer = gDLL->getText("TXT_KEY_FLYOUT_MENU_WAKE_ALL");
			aFlyoutItems.push_back(CvFlyoutMenuData(FLYOUT_WAKE_ALL, 0, pPlot->getX_INLINE(), pPlot->getY_INLINE(), szBuffer));
		}

		if (bFortifyUnit)
		{
			szBuffer = gDLL->getText("TXT_KEY_FLYOUT_MENU_FORTIFY_ALL");
			aFlyoutItems.push_back(CvFlyoutMenuData(FLYOUR_FORTIFY_ALL, 0, pPlot->getX_INLINE(), pPlot->getY_INLINE(), szBuffer));
		}
		else if (bSleepUnit)
		{
			szBuffer = gDLL->getText("TXT_KEY_FLYOUT_MENU_SLEEP_ALL");
			aFlyoutItems.push_back(CvFlyoutMenuData(FLYOUR_SLEEP_ALL, 0, pPlot->getX_INLINE(), pPlot->getY_INLINE(), szBuffer));
		}

		static std::vector<CvUnit*> plotUnits;
		getPlotUnits(pPlot, plotUnits);
		CvWStringBuffer szTempBuffer;
		for (int iI = 0; iI < (int) plotUnits.size(); iI++)
		{
			CvUnit* pLoopUnit = plotUnits[iI];
			if (pLoopUnit->getOwnerINLINE() == getActivePlayer())
			{
				CvWStringBuffer szTempBuffer;
				GAMETEXT.setUnitHelp(szTempBuffer, pLoopUnit, true);
				aFlyoutItems.push_back(CvFlyoutMenuData(FLYOUT_SELECT_UNIT, pLoopUnit->getID(), pPlot->getX_INLINE(), pPlot->getY_INLINE(), szTempBuffer.getCString()));
			}
		}
	}
}


void CvGame::applyFlyoutMenu(const CvFlyoutMenuData& kItem)
{
	CvPlot* pPlot = GC.getMapINLINE().plotINLINE(kItem.m_iX, kItem.m_iY);
	if (pPlot != NULL)
	{
		switch (kItem.m_eFlyout)
		{
		case NO_FLYOUT:
		default:
			FAssert(false);
			break;

		case FLYOUT_HURRY:
			{
				CvCity* pCity = pPlot->getPlotCity();
				if (pCity != NULL)
				{
					if (pCity->getOwnerINLINE() == getActivePlayer())
					{
						CvMessageControl::getInstance().sendDoTask(pCity->getID(), TASK_HURRY, kItem.m_iID, -1, false, false, false, false);
					}
				}
			}
			break;

		case FLYOUT_CONSCRIPT:
			{
				CvCity* pCity = pPlot->getPlotCity();
				if (pCity != NULL)
				{
					if (pCity->getOwnerINLINE() == getActivePlayer())
					{
						CvMessageControl::getInstance().sendDoTask(pCity->getID(), TASK_CONSCRIPT, -1, -1, false, false, false, false);
					}
				}
			}
			break;

		case FLYOUT_TRAIN:
			{
				CvCity* pCity = pPlot->getPlotCity();
				if (pCity != NULL)
				{
					if (pCity->getOwnerINLINE() == getActivePlayer())
					{
						cityPushOrder(pCity, ORDER_TRAIN, kItem.m_iID);
					}
				}
			}
			break;

		case FLYOUT_CONSTRUCT:
			{
				CvCity* pCity = pPlot->getPlotCity();
				if (pCity != NULL)
				{
					if (pCity->getOwnerINLINE() == getActivePlayer())
					{
						cityPushOrder(pCity, ORDER_CONSTRUCT, kItem.m_iID);
					}
				}
			}
			break;

		case FLYOUT_CREATE:
			{
				CvCity* pCity = pPlot->getPlotCity();
				if (pCity != NULL)
				{
					if (pCity->getOwnerINLINE() == getActivePlayer())
					{
						cityPushOrder(pCity, ORDER_CREATE, kItem.m_iID);
					}
				}
			}
			break;

		case FLYOUT_MAINTAIN:
			{
				CvCity* pCity = pPlot->getPlotCity();
				if (pCity != NULL)
				{
					if (pCity->getOwnerINLINE() == getActivePlayer())
					{
						cityPushOrder(pCity, ORDER_MAINTAIN, kItem.m_iID);
					}
				}
			}
			break;

		case FLYOUT_MOVE_TO:
			selectionListMove(pPlot, false, false, false);
			break;

		case FLYOUT_SELECT_UNIT:
			{
				CvUnit* pUnit = GET_PLAYER(getActivePlayer()).getUnit(kItem.m_iID);
				if (pUnit != NULL)
				{
					gDLL->getInterfaceIFace()->selectUnit(pUnit, true);
				}
			}
			break;

		case FLYOUT_SELECT_ALL:
			gDLL->getInterfaceIFace()->selectAll(pPlot);
			break;

		case FLYOUT_WAKE_ALL:
			{
				CLLNode<IDInfo>* pUnitNode = pPlot->headUnitNode();
				while (pUnitNode != NULL)
				{
					CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
					pUnitNode = pPlot->nextUnitNode(pUnitNode);
					if (pLoopUnit->isGroupHead())
					{
						CvMessageControl::getInstance().sendDoCommand(pLoopUnit->getID(), COMMAND_WAKE, -1, -1, false);
					}
				}
			}
			break;

		case FLYOUR_FORTIFY_ALL:
		case FLYOUR_SLEEP_ALL:
			{
				CLLNode<IDInfo>* pUnitNode = pPlot->headUnitNode();
				while (pUnitNode != NULL)
				{
					CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
					pUnitNode = pPlot->nextUnitNode(pUnitNode);
					if (pLoopUnit->isGroupHead())
					{
						CvMessageControl::getInstance().sendPushMission(pLoopUnit->getID(), ((pLoopUnit->isFortifyable()) ? MISSION_FORTIFY : MISSION_SLEEP), -1, -1, 0, false);
					}
				}
			}
			break;
		}
	}
}

CvPlot* CvGame::getNewHighlightPlot() const
{
	CvPlot* pNewPlot = NULL;
	if (gDLL->GetWorldBuilderMode())
	{
		std::vector<int> coords;
		bool bOK = false;
		CyArgsList argsList;
		argsList.add(0);
		bOK = gDLL->getPythonIFace()->callFunction(PYScreensModule, "WorldBuilderGetHighlightPlot", argsList.makeFunctionArgs(), &coords);
		if (bOK && coords.size())
		{
			pNewPlot = GC.getMap().plot(coords[0],coords[1]);
		}
	}
	else
	{
		if (GC.getInterfaceModeInfo(gDLL->getInterfaceIFace()->getInterfaceMode()).getHighlightPlot())
		{
			pNewPlot = gDLL->getInterfaceIFace()->getMouseOverPlot();
		}
	}
	return pNewPlot;
}


ColorTypes CvGame::getPlotHighlightColor(CvPlot* pPlot) const
{
	ColorTypes eColor = NO_COLOR;

	if (pPlot != NULL)
	{
		eColor = (ColorTypes) GC.getInfoTypeForString("COLOR_GREEN");
		if (!gDLL->GetWorldBuilderMode())
		{
			switch (gDLL->getInterfaceIFace()->getInterfaceMode())
			{
			case INTERFACEMODE_PING:
			case INTERFACEMODE_SIGN:
				if (!pPlot->isRevealed(getActiveTeam(), true))
				{
					eColor = NO_COLOR;
				}
				break;
			case INTERFACEMODE_PYTHON_PICK_PLOT:
				if (!pPlot->isRevealed(getActiveTeam(), true))
				{
					eColor = NO_COLOR;
				}
				else
				{
					CyPlot* pyPlot = new CyPlot(pPlot);
					CyArgsList argsList;
					argsList.add(gDLL->getPythonIFace()->makePythonObject(pyPlot));	// pass in plot class
					long lResult = 0;
					gDLL->getPythonIFace()->callFunction(PYGameModule, "canPickPlot", argsList.makeFunctionArgs(), &lResult);
					delete pyPlot;	// python fxn must not hold on to this pointer 
					if (lResult == 0)
					{
						eColor = NO_COLOR;
					}
				}
				break;
			case INTERFACEMODE_SAVE_PLOT_NIFS:
				eColor = (ColorTypes) GC.getInfoTypeForString("COLOR_DARK_GREY");
				break;
			default:
				if (!gDLL->getInterfaceIFace()->getSelectionList()->canDoInterfaceModeAt(gDLL->getInterfaceIFace()->getInterfaceMode(), pPlot))
				{
					eColor = (ColorTypes) GC.getInfoTypeForString("COLOR_DARK_GREY");
				}
				break;
			}
		}
	}
	return eColor;
}

void CvGame::loadBuildQueue(const CvString& strItem) const
{
	for (int iI = 0; iI < GC.getNumUnitInfos(); iI++)
	{
		UnitClassTypes eUnitClass = (UnitClassTypes)GC.getUnitInfo((UnitTypes)iI).getUnitClassType();
		UnitTypes eUnit = NO_UNIT;

		if (NO_UNITCLASS != eUnitClass)
		{
			eUnit = (UnitTypes)GC.getCivilizationInfo(getActiveCivilizationType()).getCivilizationUnits(eUnitClass);

			if (NO_UNIT != eUnit && strItem == GC.getUnitInfo(eUnit).getType())
			{
				selectedCitiesGameNetMessage(GAMEMESSAGE_PUSH_ORDER, ORDER_TRAIN, eUnit, -1, false, false, true);
				return;
			}
		}
	}

	for (int iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		BuildingClassTypes eBuildingClass = (BuildingClassTypes)GC.getBuildingInfo((BuildingTypes)iI).getBuildingClassType();
		BuildingTypes eBuilding = NO_BUILDING;

		if (NO_BUILDINGCLASS != eBuildingClass)
		{
			eBuilding = (BuildingTypes)GC.getCivilizationInfo(getActiveCivilizationType()).getCivilizationBuildings(eBuildingClass);

			if (NO_BUILDING != eBuilding && strItem == GC.getBuildingInfo(eBuilding).getType())
			{
				selectedCitiesGameNetMessage(GAMEMESSAGE_PUSH_ORDER, ORDER_CONSTRUCT, eBuilding, -1, false, false, true);
				return;
			}
		}
	}

	for (int iI = 0; iI < GC.getNumProjectInfos(); iI++)
	{
		if (strItem == GC.getProjectInfo((ProjectTypes)iI).getType())
		{
			selectedCitiesGameNetMessage(GAMEMESSAGE_PUSH_ORDER, ORDER_CREATE, ((ProjectTypes)iI), -1, false, false, true);
			return;
		}
	}

	for (int iI = 0; iI < GC.getNumProcessInfos(); iI++)
	{
		if (strItem == GC.getProcessInfo((ProcessTypes)iI).getType())
		{
			selectedCitiesGameNetMessage(GAMEMESSAGE_PUSH_ORDER, ORDER_MAINTAIN, ((ProcessTypes)iI), -1, false, false, true);
			return;
		}
	}
}

void CvGame::cheatSpaceship() const
{
	//add one space project that is still available
	CvTeam& kTeam = GET_TEAM(getActiveTeam());
	for (int i = 0; i < GC.getNumProjectInfos(); i++)
	{
		ProjectTypes eProject = (ProjectTypes) i;
		CvProjectInfo& kProject = GC.getProjectInfo(eProject);
		if (kProject.isSpaceship())
		{
			//cheat required projects
			for (int j = 0; j < GC.getNumProjectInfos(); j++)
			{
				ProjectTypes eRequiredProject = (ProjectTypes) j;
				int iNumReqProjects = kProject.getProjectsNeeded(eRequiredProject);
				while (kTeam.getProjectCount(eRequiredProject) < iNumReqProjects)
				{
					kTeam.changeProjectCount(eRequiredProject, 1);
				}
			}

			//cheat required techs
			TechTypes eRequiredTech = (TechTypes) kProject.getTechPrereq();
			if (!kTeam.isHasTech(eRequiredTech))
			{
				kTeam.setHasTech(eRequiredTech, true, getActivePlayer(), true, true);
			}

			//cheat one space component
			if (kTeam.getProjectCount(eProject) < kProject.getMaxTeamInstances())
			{
				kTeam.changeProjectCount(eProject, 1);

				CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_PYTHON_SCREEN, eProject);
				pInfo->setText(L"showSpaceShip");
				gDLL->getInterfaceIFace()->addPopup(pInfo, getActivePlayer());
			}
		}
	}
}

DomainTypes CvGame::getUnitDomain(UnitTypes eUnit) const
{
	return (DomainTypes) GC.getUnitInfo(eUnit).getDomainType();
}

const CvArtInfoBuilding* CvGame::getBuildingArtInfo(BuildingTypes eBuilding) const
{
	return GC.getBuildingInfo(eBuilding).getArtInfo();
}

bool CvGame::isWaterBuilding(BuildingTypes eBuilding) const
{
	return GC.getBuildingInfo(eBuilding).isWater();
}

CivilopediaWidgetShowTypes CvGame::getWidgetShow(BonusTypes eBonus) const
{
	// Don't show the widget if it's an abstract bonus that doesn't have any terrain (or art) associated with it.
	// Hit singles, movies, musicals, in our case
	bool bShowWidget = false;

	for (int i = 0; i < GC.getNumTerrainInfos(); i++)
	{
		if (GC.getBonusInfo(eBonus).isTerrain(i))
		{
			bShowWidget = true;
			break;
		}
	}

	if (!bShowWidget)
	{
		for (int i = 0; i < GC.getNumFeatureInfos(); i++)
		{
			if (GC.getBonusInfo(eBonus).isFeature(i))
			{
				bShowWidget = true;
				break;
			}
		}
	}

	if (!bShowWidget)
	{
		return CIVILOPEDIA_WIDGET_SHOW_NONE;
	}

	CivilopediaWidgetShowTypes eType = CIVILOPEDIA_WIDGET_SHOW_LAND;
	for (int i = 0; i < GC.getNumTerrainInfos(); i++)
	{
		if (GC.getTerrainInfo((TerrainTypes) i).isWater())
		{
			if (GC.getBonusInfo(eBonus).isTerrain(i))
			{
				eType = CIVILOPEDIA_WIDGET_SHOW_WATER;
			}
		}
	}

	return eType;
}

CivilopediaWidgetShowTypes CvGame::getWidgetShow(ImprovementTypes eImprovement) const
{
	CivilopediaWidgetShowTypes eType = CIVILOPEDIA_WIDGET_SHOW_LAND;
	if (GC.getImprovementInfo(eImprovement).isWater())
	{
		eType = CIVILOPEDIA_WIDGET_SHOW_WATER;
	}
	return eType;
}

VictoryTypes CvGame::getSpaceVictory() const
{
	VictoryTypes eVictory = NO_VICTORY;
	for (int i=0; i < GC.getNumProjectInfos(); i++)
	{
		ProjectTypes eProject = (ProjectTypes) i;
		if (GC.getProjectInfo(eProject).isSpaceship())
		{
			eVictory = (VictoryTypes) GC.getProjectInfo(eProject).getVictoryPrereq();
			break;
		}
	}

	FAssertMsg(eVictory != NO_VICTORY, "Invalid space victory type.");
	return eVictory;
}

void CvGame::nextActivePlayer(bool bForward)
{
	int iNewPlayer = getActivePlayer();
	for (int i = 1; i < MAX_PLAYERS; ++i)
	{
		if (bForward)
		{
			iNewPlayer += 1;
		}
		else
		{
			iNewPlayer += MAX_PLAYERS - 1;
		}
		iNewPlayer %= MAX_PLAYERS;

		PlayerTypes eNewPlayer = (PlayerTypes) iNewPlayer;
		if (GET_PLAYER(eNewPlayer).isAlive() && !(GET_PLAYER(eNewPlayer).isBarbarian()))
		{
			GC.getInitCore().setSlotStatus(getActivePlayer(), SS_COMPUTER);
			GC.getInitCore().setSlotStatus(eNewPlayer, SS_TAKEN);
			GET_PLAYER(getActivePlayer()).setTurnActive(false, false);
			GET_PLAYER(eNewPlayer).setTurnActive(true, false);
			setActivePlayer(eNewPlayer, true);
			break;
		}
	}
}


int CvGame::getNextSoundtrack(EraTypes eLastEra, int iLastSoundtrack) const
{
	EraTypes eCurEra = GET_PLAYER(getActivePlayer()).getCurrentEra();
	CvEraInfo& kCurrentEra = GC.getEraInfo(eCurEra);
	if (kCurrentEra.getNumSoundtracks() == 0)
	{
		return -1;
	}
	else if (kCurrentEra.getNumSoundtracks() == 1 || (eLastEra != eCurEra && kCurrentEra.isFirstSoundtrackFirst()))
	{
		return kCurrentEra.getSoundtracks(0);
	}
	else 
	{
		return kCurrentEra.getSoundtracks(GC.getASyncRand().get(kCurrentEra.getNumSoundtracks(), "Pick Song ASYNC"));
	}
}

int CvGame::getSoundtrackSpace() const
{
	return std::max(1, GC.getEraInfo(GET_PLAYER(getActivePlayer()).getCurrentEra()).getSoundtrackSpace());
}

bool CvGame::isSoundtrackOverride(CvString& strSoundtrack) const
{
	if (GC.getDefineINT("VICTORY_SOUNDTRACK_AVAILABLE") != 0)
	{
		if (getGameState() == GAMESTATE_EXTENDED || getGameState() == GAMESTATE_OVER)
		{
			if (getWinner() == getActiveTeam())
			{
				strSoundtrack = "AS2D_VICTORY";
			}
			else
			{
				strSoundtrack = "AS2D_DEFEAT";
			}
			return true;
		}
	}
	return false;
}

void CvGame::initSelection() const
{
	bool bSelected = false;
	int iLoop;
	for (CvUnit* pLoopUnit = GET_PLAYER(getActivePlayer()).firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = GET_PLAYER(getActivePlayer()).nextUnit(&iLoop))
	{
		if (pLoopUnit->getGroup()->readyToSelect())
		{
			if (pLoopUnit->canFight())
			{
				selectUnit(pLoopUnit, true);
				bSelected = true;
				break;
			}
		}
	}

	if (!bSelected)
	{
		for (CvUnit* pLoopUnit = GET_PLAYER(getActivePlayer()).firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = GET_PLAYER(getActivePlayer()).nextUnit(&iLoop))
		{
			if (pLoopUnit->getGroup()->readyToSelect())
			{
				selectUnit(pLoopUnit, true);
				bSelected = true;
				break;
			}
		}
	}

	if (!bSelected)
	{
		for (CvUnit* pLoopUnit = GET_PLAYER(getActivePlayer()).firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = GET_PLAYER(getActivePlayer()).nextUnit(&iLoop))
		{
			gDLL->getInterfaceIFace()->centerCamera(pLoopUnit);
			break;
		}
	}
}

bool CvGame::canDoPing(CvPlot* pPlot, PlayerTypes ePlayer) const
{
	if (pPlot == NULL || !pPlot->isRevealed(getActiveTeam(), false))
	{
		return false;
	}

	if (GET_PLAYER(ePlayer).getTeam() != getActiveTeam())
	{
		return false;
	}

	return true;
}

bool CvGame::shouldDisplayReturn() const
{
	return gDLL->getInterfaceIFace()->isCitySelection();
}

bool CvGame::shouldDisplayEndTurn() const
{
	return (!gDLL->getInterfaceIFace()->isCitySelection() && GET_PLAYER(getActivePlayer()).isTurnActive());
}

bool CvGame::shouldDisplayWaitingOthers() const
{
	if (!gDLL->getInterfaceIFace()->isCitySelection())
	{
		if (!GET_PLAYER(getActivePlayer()).isTurnActive())
		{
			return true;
		}

		if (gDLL->getInterfaceIFace()->isInAdvancedStart() && GET_PLAYER(getActivePlayer()).getAdvancedStartPoints() < 0)
		{
			return true;
		}
	}
	return false;
}

bool CvGame::shouldDisplayWaitingYou() const
{
	if (!gDLL->getInterfaceIFace()->isCitySelection())
	{
		if (GET_PLAYER(getActivePlayer()).isTurnActive())
		{
			if (isNetworkMultiPlayer())
			{
				if (isMPOption(MPOPTION_SIMULTANEOUS_TURNS) && 1 == countNumHumanGameTurnActive())
				{
					return true;
				}

				if (isSimultaneousTeamTurns() && 1 == GET_TEAM(getActiveTeam()).countNumHumanGameTurnActive() && GET_TEAM(getActiveTeam()).getAliveCount() > 1)
				{
					return true;
				}
			}
		}
	}

	return false;
}

bool CvGame::shouldDisplayEndTurnButton() const
{
	if (!gDLL->getInterfaceIFace()->isCitySelection())
	{
		if (!gDLL->GetWorldBuilderMode())
		{
			if (GET_PLAYER(getActivePlayer()).isTurnActive())
			{
				return true;
			}
		}
	}

	return false;
}

bool CvGame::shouldDisplayFlag() const
{
	if (gDLL->getInterfaceIFace()->isCitySelection() ||
		gDLL->getInterfaceIFace()->getHeadSelectedCity() != NULL ||
		gDLL->isDiplomacy() ||
		gDLL->isMPDiplomacyScreenUp() ||
		gDLL->GetWorldBuilderMode())
	{
		return false;
	}

	return true;
}

bool CvGame::shouldDisplayUnitModel() const
{
	if (gDLL->isDiplomacy() ||
		gDLL->isMPDiplomacyScreenUp() ||
		gDLL->GetWorldBuilderMode())
	{
		return false;
	}

	if (gDLL->getInterfaceIFace()->getHeadSelectedUnit() != NULL || gDLL->getInterfaceIFace()->isCityScreenUp())
	{
		return true;
	}

	return false;
}

bool CvGame::shouldShowResearchButtons() const
{
	if (!gDLL->GetWorldBuilderMode())
	{
		if (GET_PLAYER(getActivePlayer()).isAlive())
		{
			if (!gDLL->getInterfaceIFace()->isCityScreenUp())
			{
				if (GET_PLAYER(getActivePlayer()).getCurrentResearch() == NO_TECH)
				{
					return true;
				}
			}
		}
	}

	return false;
}

bool CvGame::shouldCenterMinimap() const
{
	return (isDebugMode() || GET_TEAM(getActiveTeam()).isMapCentering());
}

EndTurnButtonStates CvGame::getEndTurnState() const
{
	EndTurnButtonStates eNewState = END_TURN_GO;

	if ((isNetworkMultiPlayer() && 
		(isMPOption(MPOPTION_SIMULTANEOUS_TURNS) && 1 == countNumHumanGameTurnActive() || 
		(!isSimultaneousTeamTurns() && 1 == GET_TEAM(getActiveTeam()).countNumHumanGameTurnActive() && GET_TEAM(getActiveTeam()).getAliveCount() > 1))))
	{
		eNewState = END_TURN_OVER_HIGHLIGHT;
	}
	else
	{
		eNewState = END_TURN_GO;
	}

	return eNewState;
}

void CvGame::handleCityScreenPlotPicked(CvCity* pCity, CvPlot* pPlot, bool bAlt, bool bShift, bool bCtrl) const
{
	FAssert(pPlot != NULL);
	if (pCity != NULL && pPlot != NULL)
	{
		int iIndex = pCity->getCityPlotIndex(pPlot);
		if ((pPlot->getOwnerINLINE() == getActivePlayer()) && (pCity->getOwnerINLINE() == getActivePlayer()) && (iIndex != -1))
		{
			CvMessageControl::getInstance().sendDoTask(pCity->getID(), TASK_CHANGE_WORKING_PLOT, iIndex, -1, false, bAlt, bShift, bCtrl);
		}
		else if (GC.getDefineINT("CITY_SCREEN_CLICK_WILL_EXIT"))
		{
			gDLL->getInterfaceIFace()->clearSelectedCities();
		}
	}
}

void CvGame::handleCityScreenPlotDoublePicked(CvCity* pCity, CvPlot* pPlot, bool bAlt, bool bShift, bool bCtrl) const
{
	if (pCity != NULL)
	{
		if (pCity->plot() == pPlot)
		{
			gDLL->getInterfaceIFace()->clearSelectedCities();
		}
	}
}

void CvGame::handleCityScreenPlotRightPicked(CvCity* pCity, CvPlot* pPlot, bool bAlt, bool bShift, bool bCtrl) const
{
	if (pCity != NULL && pPlot != NULL)
	{
		if ((pCity->getOwnerINLINE() == getActivePlayer()) && (pPlot->getOwnerINLINE() == getActivePlayer()) && (pCity->getCityPlotIndex(pPlot) != -1))
		{
			CvMessageControl::getInstance().sendDoTask(pCity->getID(), TASK_CLEAR_WORKING_OVERRIDE, pCity->getCityPlotIndex(pPlot), -1, false, bAlt, bShift, bCtrl);
		}
	}
}

void CvGame::handleCityPlotRightPicked(CvCity* pCity, CvPlot* pPlot, bool bAlt, bool bShift, bool bCtrl) const
{
	if (pPlot != NULL)
	{
		if ((pCity != NULL) && gDLL->getInterfaceIFace()->isCitySelected(pCity))
		{
			selectedCitiesGameNetMessage(GAMEMESSAGE_DO_TASK, TASK_CLEAR_RALLY_PLOT);
		}
		else
		{
			if (bShift)
			{
				selectedCitiesGameNetMessage(GAMEMESSAGE_DO_TASK, TASK_RALLY_PLOT, pPlot->getX(), pPlot->getY());
			}
			else
			{
				gDLL->getInterfaceIFace()->clearSelectedCities();
			}
		}
	}
}

void CvGame::handleMiddleMouse(bool bCtrl, bool bAlt, bool bShift)
{
	if (gDLL->getInterfaceIFace()->isCitySelection())
	{
		gDLL->getInterfaceIFace()->clearSelectedCities();
	}
	else
	{
		if (bAlt)
		{
			doControl(CONTROL_SELECTYUNITALL);
		}
		else if (bCtrl)
		{
			doControl(CONTROL_SELECTYUNITTYPE);
		}
		else
		{
			doControl(CONTROL_CENTERONSELECTION); 
		}
	}
}

void CvGame::handleDiplomacySetAIComment(DiploCommentTypes eComment) const
{
	PlayerTypes eOtherPlayer = (PlayerTypes) gDLL->getDiplomacyPlayer();
	FAssert(eOtherPlayer != NO_PLAYER);
	if (GC.getInfoTypeForString("AI_DIPLOCOMMENT_ACCEPT_ASK") == eComment || 
		GC.getInfoTypeForString("AI_DIPLOCOMMENT_ACCEPT_DEMAND") == eComment)
	{
		if (!GET_TEAM(getActiveTeam()).isAVassal() && !GET_TEAM(GET_PLAYER(eOtherPlayer).getTeam()).isAVassal())
		{
			CLinkList<TradeData> playerList;
			CLinkList<TradeData> loopPlayerList;
			TradeData kTradeData;
			setTradeItem(&kTradeData, TRADE_PEACE_TREATY);
			playerList.insertAtEnd(kTradeData);
			loopPlayerList.insertAtEnd(kTradeData);

			gDLL->sendImplementDealMessage(eOtherPlayer, &playerList, &loopPlayerList);
		}
	}
}
