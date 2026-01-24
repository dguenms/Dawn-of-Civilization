#include "CvGameCoreDLL.h"
#include "CvGame.h"
#include "CoreAI.h"
#include "CvCityAI.h"
#include "CvUnitAI.h"
#include "CvSelectionGroup.h"
#include "GroupPathFinder.h"
#include "FAStarNode.h"
#include "PlotRange.h"
#include "CvInfo_City.h"
#include "CvInfo_Command.h"
#include "CvInfo_Terrain.h"
#include "CvInfo_GameOption.h"
#include "RiseFall.h" // advc.700
#include "CvPopupInfo.h"
#include "CvGameTextMgr.h"
#include "CvMessageControl.h"
#include "CvBugOptions.h"
#include "SelfMod.h" // advc.092b
#include <fstream> // advc.003d

/*  advc: This file was added by patch 3.17, moving some UI functionality
	out of the EXE and thus exposing it to mods.
	The near name clash with CyGameInterface.cpp is coincidental. */

/*	<advc.007c> The functions in this header arguably shouldn't use any of the
	synchronized RNGs that are part of CvGame. */
#undef CVGAME_INSTANCE_FOR_RNG
#define CVGAME_INSTANCE_FOR_RNG NULL // </advc.007c>

void CvGame::updateColoredPlots()
{
	PROFILE_FUNC();
	// <advc.004z> Too early; player options haven't been set yet.
	if (getTurnSlice() <= 0)
		return; // </advc.004z>
	CvDLLEngineIFaceBase& kEngine = *gDLL->getEngineIFace();
	CvDLLInterfaceIFaceBase& kUI = gDLL->UI();

	kEngine.clearColoredPlots(PLOT_LANDSCAPE_LAYER_BASE);
	kEngine.clearAreaBorderPlots(AREA_BORDER_LAYER_CITY_RADIUS);
	kEngine.clearAreaBorderPlots(AREA_BORDER_LAYER_RANGED);
	kEngine.clearAreaBorderPlots(AREA_BORDER_LAYER_BLOCKADING);

	if (!gDLL->GetWorldBuilderMode() || kUI.isInAdvancedStart())
		kEngine.clearColoredPlots(PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS);

	if (GC.getPythonCaller()->updateColoredPlots())
		return;
	// <advc.004h>
	// Moved up
	CvUnit* pHeadSelectedUnit = kUI.getHeadSelectedUnit();
	if (pHeadSelectedUnit != NULL && pHeadSelectedUnit->isHuman())
		pHeadSelectedUnit->updateFoundingBorder();
	// </advc.004h>

	CvMap const& kMap = GC.getMap();
	// BETTER_BTS_AI_MOD, Debug, 06/25/09, jdog5000: START
	if (isDebugMode())
	{
		if (kUI.isShowYields() && !gDLL->GetWorldBuilderMode()) // advc.007
		{
			// City circles for debugging
			for (PlayerAIIter<CIV_ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
			{
				for (int i = 0; i < itPlayer->AI_getNumCitySites(); i++)
				{
					CvPlot const& kSite = itPlayer->AI_getCitySite(i);
					kEngine.addColoredPlot(kSite.getX(), kSite.getY(),
							GC.getInfo(GC.getInfo(itPlayer->getPlayerColor()).
							getColorTypePrimary()).getColor(),
							PLOT_STYLE_CIRCLE, PLOT_LANDSCAPE_LAYER_BASE);
				}
			}
			// Plot improvement replacement circles for debugging
			FOR_EACH_ENUM(PlotNum)
			{
				CvPlot& kPlot = kMap.getPlotByIndex(eLoopPlotNum);
				CvCityAI const* pWorkingCity = kPlot.AI_getWorkingCity();
				ImprovementTypes eImprovement = kPlot.getImprovementType();
				if (pWorkingCity != NULL && eImprovement != NO_IMPROVEMENT)
				{
					CityPlotTypes ePlot = pWorkingCity->getCityPlotIndex(kPlot);
					//int iBuildValue = pWorkingCity->AI_getBestBuildValue(ePlot);
					BuildTypes eBestBuild = pWorkingCity->AI_getBestBuild(ePlot);
					if (eBestBuild != NO_BUILD)
					{
						if (GC.getInfo(eBestBuild).getImprovement() != NO_IMPROVEMENT &&
							eImprovement != GC.getInfo(eBestBuild).getImprovement())
						{
							kEngine.addColoredPlot(kPlot.getX(), kPlot.getY(),
									GC.getInfo(GC.getColorType("RED")).getColor(),
									PLOT_STYLE_CIRCLE, PLOT_LANDSCAPE_LAYER_BASE);
						}
					}
				}
			}
		}
	} // BETTER_BTS_AI_MOD: END

	// City circles when in Advanced Start
	if (kUI.isInAdvancedStart())
	{
		FOR_EACH_ENUM(PlotNum)
		{
			CvPlot& kPlot = kMap.getPlotByIndex(eLoopPlotNum);
			if (GET_PLAYER(getActivePlayer()).getAdvancedStartCityCost(true, &kPlot) > 0)
			{
				bool bStartingPlot = false;
				FOR_EACH_ENUM(Player)
				{
					CvPlayer const& kPlayer = GET_PLAYER(eLoopPlayer);
					if (kPlayer.isAlive() && getActiveTeam() == kPlayer.getTeam() &&
						&kPlot == kPlayer.getStartingPlot())
					{
						bStartingPlot = true;
						break;
					}
				}
				if (bStartingPlot)
				{
					kEngine.addColoredPlot(kPlot.getX(), kPlot.getY(),
							GC.getInfo(GC.getColorType("WARNING_TEXT")).getColor(),
							PLOT_STYLE_CIRCLE, PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS);
				}
				else if (GET_PLAYER(getActivePlayer()).AI_isPlotCitySite(kPlot))
				{
					kEngine.addColoredPlot(kPlot.getX(), kPlot.getY(),
							GC.getInfo(GC.getColorType("HIGHLIGHT_TEXT")).getColor(),
							PLOT_STYLE_CIRCLE, PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS);
				}
				if (kPlot.isRevealed(getActiveTeam()))
				{
					NiColorA color(GC.getInfo(GC.getColorType("WHITE")).getColor());
					color.a = 0.4f;
					kEngine.fillAreaBorderPlot(kPlot.getX(), kPlot.getY(),
							color, AREA_BORDER_LAYER_CITY_RADIUS);
				}
			}
		}
	}

	CvCity const* pHeadSelectedCity = kUI.getHeadSelectedCity();
	if (pHeadSelectedCity != NULL)
	{
		if (kUI.isCityScreenUp())
		{
			NiColorA color(GC.getInfo(GC.getColorType("WHITE")).getColor());
			color.a = 0.7f; // advc: Moved out of the loop below
			for (WorkingPlotIter it(*pHeadSelectedCity); it.hasNext(); ++it)
			{
				kEngine.addColoredPlot(it->getX(), it->getY(), color,
						PLOT_STYLE_CIRCLE, PLOT_LANDSCAPE_LAYER_BASE);
			}

			// doc: display next culture plot
			// TODO: refactor
			int iEffectiveNextCoveredPlot = pHeadSelectedCity->getEffectiveNextCoveredPlot();
			if (iEffectiveNextCoveredPlot < NUM_CITY_PLOTS)
			{
				pLoopPlot = pHeadSelectedCity->getCulturePlot(iEffectiveNextCoveredPlot);

				if (pLoopPlot != NULL)
				{
					NiColorA color(GC.getColorInfo((ColorTypes)GC.getInfoTypeForString("COLOR_CULTURE_STORED")).getColor());
					color.a = 0.7f;
					gDLL->getEngineIFace()->addColoredPlot(pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE(), color, PLOT_STYLE_CIRCLE, PLOT_LANDSCAPE_LAYER_BASE);
				}
			}
		}
		else
		{
			for (CLLNode<IDInfo> const* pNode = kUI.headSelectedCitiesNode();
				pNode != NULL; pNode = kUI.nextSelectedCitiesNode(pNode))
			{
				CvCity const* pSelectedCity = ::getCity(pNode->m_data);
				if (pSelectedCity == NULL)
				{
					FAssertMsg(pSelectedCity != NULL, "Can this happen?");
					continue;
				}
				CvPlot* pRallyPlot = pSelectedCity->getRallyPlot();
				if (pRallyPlot != NULL)
				{
					kEngine.addColoredPlot(pRallyPlot->getX(), pRallyPlot->getY(),
							GC.getInfo(GC.getColorType("YELLOW")).getColor(),
							PLOT_STYLE_CIRCLE, PLOT_LANDSCAPE_LAYER_BASE);
				}
			}
		} // <advc>
		return;
	}
	if (pHeadSelectedUnit == NULL)
		return; // </advc>

	if (gDLL->getGraphicOption(GRAPHICOPTION_CITY_RADIUS))
	{
		//if (kUI.canSelectionListFound())
		if (pHeadSelectedUnit->isFound()) // advc.004h
		{
			FOR_EACH_ENUM(PlotNum)
			{
				CvPlot& kPlot = kMap.getPlotByIndex(eLoopPlotNum);
				if (kPlot.getOwner() == pHeadSelectedUnit->getOwner())
				{
					if (kPlot.getWorkingCity() != NULL)
					{
						NiColorA color(GC.getInfo(GC.getColorType("HIGHLIGHT_TEXT")
								/*(GC.getInfo(GET_PLAYER(pHeadSelectedUnit->getOwner()).getPlayerColor()).getColorTypePrimary())*/
								).getColor());
						color.a = 1.0f;
						kEngine.fillAreaBorderPlot(kPlot.getX(), kPlot.getY(),
								color, AREA_BORDER_LAYER_CITY_RADIUS);
					}
				}
			}
		}
	}
	/*	advc.rstr: Merged air range with ranged strike code so that the maximal range
		is highlighted also for range-strikers */
	if (pHeadSelectedUnit->airRange() > 0)
	{
		int iMaxAirRange = 0;
		for (CLLNode<IDInfo> const* pNode = kUI.headSelectionListNode();
			pNode != NULL; pNode = kUI.nextSelectionListNode(pNode))
		{
			CvUnit const* pSelectedUnit = ::getUnit(pNode->m_data);
			if (pSelectedUnit != NULL)
				iMaxAirRange = std::max(iMaxAirRange, pSelectedUnit->airRange());
		}
		if (iMaxAirRange > 0)
		{
			bool const bAir = (pHeadSelectedUnit->getDomainType() == DOMAIN_AIR);
			for (PlotCircleIter it(*pHeadSelectedUnit, iMaxAirRange); it.hasNext(); ++it)
			{
				CvPlot const& kTargetPlot = *it;
				if (bAir ||
					(kTargetPlot.isVisible(pHeadSelectedUnit->getTeam()) /*&&
					// advc.rstr: See CvUnit::canRangeStrikeAt
					pHeadSelectedUnit->getPlot().canSeePlot(
					&kTargetPlot, pHeadSelectedUnit->getTeam(), iMaxAirRange,
					pHeadSelectedUnit->getFacingDirection(true))*/))
				{
					NiColorA color(GC.getInfo(GC.getColorType("YELLOW")).getColor());
					color.a = 0.5f;
					kEngine.fillAreaBorderPlot(kTargetPlot.getX(), kTargetPlot.getY(),
							color, AREA_BORDER_LAYER_RANGED);
				}
			}
		}
	}
	if (!GET_PLAYER(getActivePlayer()).isOption(PLAYEROPTION_NO_UNIT_RECOMMENDATIONS) ||
		!GET_PLAYER(getActivePlayer()).isHuman()) // advc.127
	{
		CvUnitAI const& kRecommendUnit = pHeadSelectedUnit->AI(); // advc.003u
		if (kRecommendUnit.AI_getUnitAIType() == UNITAI_WORKER ||
			kRecommendUnit.AI_getUnitAIType() == UNITAI_WORKER_SEA)
		{
			if (kRecommendUnit.getPlot().getOwner() == kRecommendUnit.getOwner())
			{
				CvCityAI* pCity = kRecommendUnit.getPlot().AI_getWorkingCity();
				if (pCity != NULL)
				{
					CvPlot* pBestPlot = NULL;
					if (kRecommendUnit.AI_bestCityBuild(*pCity, &pBestPlot) &&
						pCity->AI_getBestBuildValue(pCity->getCityPlotIndex(*pBestPlot)) > 1)
					{
						FAssert(pBestPlot != NULL);
						kEngine.addColoredPlot(pBestPlot->getX(), pBestPlot->getY(),
								GC.getInfo(GC.getColorType("HIGHLIGHT_TEXT")).getColor(),
								PLOT_STYLE_CIRCLE, PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS);
						CvPlot* pNextBestPlot = NULL;
						if (kRecommendUnit.AI_bestCityBuild(*pCity, &pNextBestPlot, NULL, pBestPlot) &&
							pCity->AI_getBestBuildValue(pCity->getCityPlotIndex(*pNextBestPlot)) > 1)
						{
							FAssert(pNextBestPlot != NULL);
							kEngine.addColoredPlot(pNextBestPlot->getX(), pNextBestPlot->getY(),
									GC.getInfo(GC.getColorType("HIGHLIGHT_TEXT")).getColor(),
									PLOT_STYLE_CIRCLE, PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS);
						}
					}
				}
			}
		}
		/*	K-Mod. I've rearranged the following code a bit, so that it is more efficient, and so that
			it shows city sites within 7 turns, rather than just the ones in 4 plot range.
			the original code has been deleted, because it was quite bulky. */
		int const iMaxPathTurns = 7;
		// city sites
		CvPlayerAI const& kActivePlayer = GET_PLAYER(getActivePlayer());
		GroupPathFinder sitePath;
		sitePath.setGroup(*pHeadSelectedUnit->getGroup(), NO_MOVEMENT_FLAGS,
				iMaxPathTurns, GC.getMOVE_DENOMINATOR());
		if (pHeadSelectedUnit->isFound())
		{
			for (int i = 0; i < kActivePlayer.AI_getNumCitySites(); i++)
			{
				CvPlot const& kSite = kActivePlayer.AI_getCitySite(i);
				/*	(advc: BUFFY adds this check. I've instead removed the
					vision cheats from the AI city site evaluation.) */
				if (//kSite.isVisible(kActivePlayer.getTeam()) &&
					sitePath.generatePath(kSite))
				{	// <advc.004> Don't show weak sites if they're far away
					if (sitePath.getPathTurns() + i > iMaxPathTurns + 1)
						continue; // </advc.004>
					kEngine.addColoredPlot(kSite.getX(), kSite.getY(),
							GC.getInfo(GC.getColorType("HIGHLIGHT_TEXT")).getColor(),
							PLOT_STYLE_CIRCLE, PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS);
				}
			}
		}
		// goody huts
		//if (kHeadUnit.isNoBadGoodies())
		if (pHeadSelectedUnit->canFight()) // advc.004z: Replacing the above
		{
			int iRange = 4;
			// <advc.004z>
			if (pHeadSelectedUnit->isNoBadGoodies())
				iRange++;
			else iRange--; // </advc.004z>
			// just a smaller range.
			sitePath.setGroup(*pHeadSelectedUnit->getGroup(), NO_MOVEMENT_FLAGS,
					iRange, GC.getMOVE_DENOMINATOR());
			for (SquareIter it(*pHeadSelectedUnit, iRange); it.hasNext(); ++it)
			{
				CvPlot const& kLoopPlot = *it;
				if (kLoopPlot.isVisible(pHeadSelectedUnit->getTeam()) &&
					kLoopPlot.isRevealedGoody(pHeadSelectedUnit->getTeam()))
				{
					if (sitePath.generatePath(kLoopPlot))
					{
						kEngine.addColoredPlot(kLoopPlot.getX(), kLoopPlot.getY(),
								GC.getInfo(GC.getColorType("HIGHLIGHT_TEXT")).getColor(),
								PLOT_STYLE_CIRCLE, PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS);
					}
				}
			}
		}
		// K-Mod end
	}
	if (pHeadSelectedUnit->isBlockading())
	{
		for (MemberIter it(getActiveTeam()); it.hasNext(); ++it)
		{
			CvPlayer& kMember = *it;
			FOR_EACH_UNIT(pLoopUnit, kMember)
			{
				if (!pLoopUnit->isBlockading())
					continue;
				/*  <advc.033> Replacing code that was (mostly) equivalent
					to CvUnit::updatePlunder */
				std::vector<CvPlot*> apRange;
				pLoopUnit->blockadeRange(apRange);
				for (size_t j = 0; j < apRange.size(); j++) // </advc.033>
				{
					NiColorA color(GC.getInfo(GC.getInfo(
							/*GET_PLAYER(getActivePlayer())*/kMember. // advc.004
							getPlayerColor()).getColorTypePrimary()).getColor());
					color.a = 0.5f;
					kEngine.fillAreaBorderPlot(apRange[j]->getX(), apRange[j]->getY(),
							color, AREA_BORDER_LAYER_BLOCKADING);
				}
			}
		}
	}
}


void CvGame::updateBlockadedPlots()
{
	PROFILE_FUNC();

	CvDLLEngineIFaceBase& kEngine = *gDLL->getEngineIFace(); // advc
	kEngine.clearAreaBorderPlots(AREA_BORDER_LAYER_BLOCKADED);
	CvMap const& kMap = GC.getMap();
	for (int i = 0; i < kMap.numPlots(); ++i)
	{
		CvPlot& kPlot = kMap.getPlotByIndex(i);
		if (kPlot.getBlockadedCount(getActiveTeam()) > 0 && kPlot.isRevealed(getActiveTeam()))
		{
			NiColorA color(GC.getInfo(GC.getColorType("BLACK")).getColor());
			color.a = 0.35f;
			kEngine.fillAreaBorderPlot(kPlot.getX(), kPlot.getY(), color, AREA_BORDER_LAYER_BLOCKADED);
		}
	}
	/*  <advc.700> An odd place for initialization. Need graphics to be fully
		initialized so that I can send an error msg to the player if necessary.
		Not the case in e.g. CvGame::init or setInitialItems. */
	if (isOption(GAMEOPTION_RISE_FALL) && getElapsedGameTurns() <= 0)
		m_pRiseFall->init(); // </advc.700>
}


void CvGame::updateSelectionList()
{
	CvDLLInterfaceIFaceBase& kUI = gDLL->UI();
	CvUnit* pHeadSelectedUnit = kUI.getHeadSelectedUnit();
	// <advc.004k> (Needed for dealing with all units becoming unselected)
	if (pHeadSelectedUnit == NULL)
		gDLL->getEngineIFace()->clearAreaBorderPlots(AREA_BORDER_LAYER_PATROLLED);
	// </advc.004k>
	else pHeadSelectedUnit->onActiveSelection(); // advc
	if (GC.suppressCycling() || // K-Mod
		GET_PLAYER(getActivePlayer()).isOption(PLAYEROPTION_NO_UNIT_CYCLING))
	{
		return;
	}
	if (pHeadSelectedUnit == NULL || !pHeadSelectedUnit->getGroup()->readyToSelect(true))
	{
		if (kUI.getOriginalPlot() == NULL ||
			!cyclePlotUnits(kUI.getOriginalPlot(), true, true, kUI.getOriginalPlotCount()))
		{
			if (kUI.getSelectionPlot() == NULL ||
				!cyclePlotUnits(kUI.getSelectionPlot(), true, true))
			{
				cycleSelectionGroups(true);
			}
		}
		pHeadSelectedUnit = kUI.getHeadSelectedUnit();
		if (pHeadSelectedUnit != NULL &&
			!pHeadSelectedUnit->getGroup()->readyToSelect(/* advc.153: */ true))
		{
			kUI.clearSelectionList();
		}
	}
}


void CvGame::updateTestEndTurn()
{
	if (!GET_PLAYER(getActivePlayer()).isTurnActive())
		return;
	// <advc.003g>
	if (!m_bFPTestDone)
		CvMessageControl::getInstance().sendFPTest(FPChecksum()); // </advc.003g>
	CvDLLInterfaceIFaceBase& kUI = gDLL->UI();
	bool const bAny = (kUI.getHeadSelectedUnit() != NULL &&
			!GET_PLAYER(getActivePlayer()).isOption(PLAYEROPTION_NO_UNIT_CYCLING));
	if (kUI.isEndTurnMessage())
	{
		if (GET_PLAYER(getActivePlayer()).hasReadyUnit(bAny))
			kUI.setEndTurnMessage(false);
		return;
	}
	if (GET_PLAYER(getActivePlayer()).hasBusyUnit() ||
		GET_PLAYER(getActivePlayer()).hasReadyUnit(bAny))
	{
		return;
	}
	bool const bShift = GC.shiftKey();
	if (!kUI.isForcePopup())
	{
		if (!bShift && !GC.suppressCycling()) // K-Mod
			kUI.setForcePopup(true);
		return;
	}
	if (GET_PLAYER(getActivePlayer()).hasAutoUnit())
	{
		//if (!(GC.shiftKey()))
		// K-Mod. Don't start automoves if we currently have a group selected which would move.
		CvUnit* pSelectedUnit = kUI.getHeadSelectedUnit();
		if (!bShift && !GC.suppressCycling() &&
			(pSelectedUnit == NULL || !pSelectedUnit->getGroup()->readyToAuto()))
		{ // K-Mod end
			CvMessageControl::getInstance().sendAutoMoves();
		}
		return;
	}
	if (GET_PLAYER(getActivePlayer()).isOption(PLAYEROPTION_WAIT_END_TURN) ||
		!kUI.isHasMovedUnit() || isHotSeat() || isPbem())
	{
		kUI.setEndTurnMessage(true);
		return;
	}
	if (kUI.getEndTurnCounter() > 0)
	{
		kUI.changeEndTurnCounter(-1);
		return;
	}
	CvMessageControl::getInstance().sendTurnComplete();
	kUI.setEndTurnCounter(3); // XXX
}

// advc: Merge of two BtS functions that had largely the same body
CvUnit* CvGame::getPlotUnits(CvPlot const* pPlot,
	std::vector<CvUnit*>* pPlotUnits, int iIndex) const
{
	PROFILE_FUNC();

	FAssert((iIndex == -1) != (pPlotUnits == NULL));

	if (pPlotUnits != NULL)
		pPlotUnits->clear();

	if (pPlot == NULL)
		return NULL;

	int iCount = 0;
	PlayerTypes eActivePlayer = getActivePlayer();
	TeamTypes eActiveTeam = getActiveTeam();
	for (int iPass = 0; iPass < 2; iPass++)
	{
		FOR_EACH_UNIT_VAR_IN(pUnit, *pPlot)
		{
			if ((pUnit->getOwner() == eActivePlayer) != (iPass == 0))
				continue;
			if (pUnit->isInvisible(eActiveTeam, true) || pUnit->isCargo())
				continue;

			if (iCount == iIndex)
				return pUnit;

			iCount++;
			if (pPlotUnits != NULL)
				pPlotUnits->push_back(pUnit);
			//if (pLoopUnit1->getTeam() == activeTeam || isDebugMode()) {
			if (!pUnit->hasCargo())
				continue;
			FOR_EACH_UNIT_VAR_IN(pCargoUnit, *pPlot)
			{
				if (pCargoUnit->isInvisible(eActiveTeam, true))
					continue;
				if (pCargoUnit->getTransportUnit() == pUnit)
				{
					if (iCount == iIndex)
						return pCargoUnit;

					iCount++;
					if (pPlotUnits != NULL)
						pPlotUnits->push_back(pCargoUnit);
				}
			}
		}
	}
	return NULL;
}


void CvGame::cycleCities(bool bForward, bool bAdd) const
{
	/*	advc: bForward is now handled a bit differently b/c I've added
		separate functions for backward traversal (no functional change) */

	CvCity* pHeadSelectedCity = gDLL->UI().getHeadSelectedCity();
	CvCity* pSelectCity = NULL;
	if (pHeadSelectedCity != NULL &&
		(pHeadSelectedCity->getTeam() == getActiveTeam() || isDebugMode()))
	{
		int iLoop = pHeadSelectedCity->getIndex();
		iLoop += (bForward ? 1 : -1);
		CvPlayer const& kOwner = GET_PLAYER(pHeadSelectedCity->getOwner());
		CvCity* pLoopCity = (bForward ? kOwner.nextCity(&iLoop) : kOwner.prevCity(&iLoop));

		if (pLoopCity == NULL)
			pLoopCity = (bForward ? kOwner.firstCity(&iLoop) : kOwner.lastCity(&iLoop));

		if (pLoopCity != NULL && pLoopCity != pHeadSelectedCity)
			pSelectCity = pLoopCity;
	}
	else
	{
		int iLoop;
		pSelectCity = (bForward ? GET_PLAYER(getActivePlayer()).firstCity(&iLoop) :
				GET_PLAYER(getActivePlayer()).lastCity(&iLoop));
	}

	if (pSelectCity != NULL)
	{
		if (bAdd)
		{
			gDLL->UI().clearSelectedCities();
			gDLL->UI().addSelectedCity(pSelectCity);
		}
		else gDLL->UI().selectCity(pSelectCity);
	}
}

// advc.154: Extracted the const part out of cycleSelectionGroups
CvSelectionGroup* CvGame::getNextGroupInCycle(bool bForward, bool bWorkers,
	bool& bWrap, CvUnit*& pCycleUnit, // out-params
	std::set<int>* pCycledGroups) const
{
	bWrap = false;
	pCycleUnit = gDLL->UI().getHeadSelectedUnit();
	CvSelectionGroup* pGroup=NULL;
	if (pCycleUnit != NULL)
	{
		if (pCycleUnit->getOwner() != getActivePlayer())
			pCycleUnit = NULL;
		pGroup = GET_PLAYER(getActivePlayer()).getNextGroupInCycle(
				pCycleUnit, bForward, bWorkers, &bWrap, pCycledGroups);
	}
	else
	{
		CvPlot* pPlot = gDLL->UI().getLookAtPlot();
		pGroup = GC.getMap().findSelectionGroup(
				pPlot != NULL ? pPlot->getX() : 0,
				pPlot != NULL ? pPlot->getY() : 0,
				getActivePlayer(), true, bWorkers);
	}
	return pGroup;
}

/*	advc.154: Python wrapper for the above - but who knows, the DLL too
	might want to be able to tell what the cycle button is showing. */
CvUnit* CvGame::getCycleButtonUnit(bool bForward, bool bWorkers) const
{
	if (getActivePlayer() == NO_PLAYER ||
		!GET_PLAYER(getActivePlayer()).isHuman()) // AI Auto Play
	{
		return NULL;
	}
	bool bDummy=false;
	CvUnit* pDummy=NULL;
	CvSelectionGroup* pNextGroup = GC.getGame().getNextGroupInCycle(
			bForward, bWorkers, bDummy, pDummy);
	if (pNextGroup == NULL || pNextGroup->getNumUnits() <= 0)
		return NULL;
	for (int iPass = 0; iPass < (/*bWorkers ? 1 :*/ 2); iPass++)
	{
		FOR_EACH_UNIT_VAR_IN(pUnit, *pNextGroup)
		{
			if (!pUnit->IsSelected() && pUnit->canMove() &&
				/*	!bWorkers doesn't exclude all-worker groups, so we can only
					_prefer_ selecting a non-worker. */
				/*	Actually, let's always prefer to select a worker. Don't want
					to show different icons on the two buttons if they refer
					to the same group. */
				(iPass == 1 || /*bWorkers == */pUnit->isWorker()))
			{
				return pUnit;
			}
		}
	}
	return NULL;
}


void CvGame::cycleSelectionGroups(bool bClear, bool bForward, bool bWorkers)
{
	bool bWrap=false;
	CvUnit* pCycleUnit=NULL;
	// <advc.154> Moved into a const function ...
	CvSelectionGroup* pNextSelectionGroup = getNextGroupInCycle(
			bForward, bWorkers, bWrap, pCycleUnit); // </advc.154>
	if (gDLL->UI().getHeadSelectedUnit() != NULL)
	{
		GET_PLAYER(getActivePlayer()).cycleSelectionGroups(
				pCycleUnit, bForward, bWorkers, &bWrap);
	}
	if (bWrap)
	{	/*	K-Mod: I've weakend this condition so that the group cycle order
			can be refreshed by automoves.
			(Maybe I should create & use "sendCycleRefresh" instead.) */
		if (pNextSelectionGroup != NULL ||
			GET_PLAYER(getActivePlayer()).hasAutoUnit())
		{
			CvMessageControl::getInstance().sendAutoMoves();
		}
	}

	if (pNextSelectionGroup != NULL)
	{
		FAssert(pNextSelectionGroup->getOwner() == getActivePlayer());
		FAssert(pNextSelectionGroup->getHeadUnit() != NULL); // K-Mod
		gDLL->UI().selectUnit(pNextSelectionGroup->getHeadUnit(), bClear);
		/*	<advc.153> Could deselect units without moves here, but then
			the player can't just press skip without splitting up the group.
			Perhaps skip could somehow receive special treatment in this case ...
			So long as that's not implemented, it's better to let the player use
			the Go To (All) button if he or she does want to split the group. */
		/*FOR_EACH_UNIT_VAR_IN(pUnit, *pNextSelectionGroup)
		{
			if (!pUnit->canMove())
				gDLL->UI().removeFromSelectionList(pUnit);
		}*/ // </advc.153>
	}
	// K-Mod
	else if (pCycleUnit != NULL)
	{
		gDLL->UI().clearSelectionList();
		updateTestEndTurn();
		// <advc.002e> Hide glow when all units moved
		if (!BUGOption::isEnabled("PLE__ShowPromotionGlow", false))
		{
			CvPlayer const& kOwner = GET_PLAYER(pCycleUnit->getOwner());
			FOR_EACH_UNIT_VAR(u, kOwner)
				gDLL->getEntityIFace()->showPromotionGlow(u->getEntity(), false);
		} // </advc.002e>
	} // K-Mod end

	if (pCycleUnit != gDLL->UI().getHeadSelectedUnit() ||
		(pCycleUnit != NULL && pCycleUnit->getGroup()->readyToSelect(
		true))) // advc.153: was false
	{
		gDLL->UI().lookAtSelectionPlot();
	}
}

// K-Mod:
void CvGame::cycleSelectionGroups_delayed(int iDelay, bool bIncremental, bool bDelayOnly)
{
	PROFILE_FUNC(); // just hoping that the python call doesn't hurt the respose times

	if (GC.suppressCycling()) // cf. GvGame::updateSelectionList
		return;
	/*	Only rapid-cycle when not doing auto-play. Also note,
		cycleSelectionGroups currently causes a crash if the game is not initialised.
		(and this function is indirectly called during the set of up a new game -
		so we currently need that init check.) */
	PlayerTypes const eActive = getActivePlayer();
	if (isFinalInitialized() &&
		eActive != NO_PLAYER && GET_PLAYER(eActive).isHuman() &&
		BUGOption::isEnabled("MainInterface__RapidUnitCycling", false))
	{
		if (!bDelayOnly)
		{
			// (for the non-rapid case, this option is handled elsewhere.)
			if (GET_PLAYER(eActive).isOption(PLAYEROPTION_NO_UNIT_CYCLING))
				return;

			if (gDLL->getEngineIFace()->isCameraLocked())
			{	// immediate cycling might violate the camera lock. :(
				gDLL->UI().setCycleSelectionCounter(1);
			}
			else cycleSelectionGroups(true);
		}
	}
	else
	{
		if (bIncremental)
			gDLL->UI().changeCycleSelectionCounter(iDelay);
		else gDLL->UI().setCycleSelectionCounter(iDelay);
	}
}

// Returns true if unit was cycled...
bool CvGame::cyclePlotUnits(CvPlot* pPlot, bool bForward, bool bAuto, int iCount) const
{
	FAssert(iCount >= -1);

	CvUnit const* pUnit = NULL;
	CLLNode<IDInfo> const* pUnitNode = NULL;
	if (iCount == -1)
	{
		for (pUnitNode = pPlot->headUnitNode(); pUnitNode != NULL;
			pUnitNode = pPlot->nextUnitNode(pUnitNode))
		{
			pUnit = ::getUnit(pUnitNode->m_data);
			if (pUnit->IsSelected())
				break;
		}
	}
	else
	{
		for (pUnitNode = pPlot->headUnitNode(); pUnitNode != NULL;
			pUnitNode = pPlot->nextUnitNode(pUnitNode))
		{
			pUnit = ::getUnit(pUnitNode->m_data);
			if (iCount - 1 == 0)
				break;
			if (iCount > 0)
				iCount--;
		}
		if (pUnitNode == NULL)
		{
			pUnitNode = pPlot->tailUnitNode();
			if (pUnitNode != NULL)
				pUnit = ::getUnit(pUnitNode->m_data);
		}
	}
	if (pUnitNode == NULL)
		return false;

	CvUnit const* pSelectedUnit = pUnit;
	while (true)
	{
		if (bForward)
		{
			pUnitNode = pPlot->nextUnitNode(pUnitNode);
			if (pUnitNode == NULL)
				pUnitNode = pPlot->headUnitNode();
		}
		else
		{
			pUnitNode = pPlot->prevUnitNode(pUnitNode);
			if (pUnitNode == NULL)
				pUnitNode = pPlot->tailUnitNode();
		}
		CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
		if (iCount == -1)
		{
			if (pLoopUnit == pSelectedUnit)
				break;
		}
		if (pLoopUnit->getOwner() == getActivePlayer())
		{
			if (bAuto)
			{
				if (pLoopUnit->getGroup()->readyToSelect(/* advc.153: */ true))
				{
					gDLL->UI().selectUnit(pLoopUnit, true);
					return true;
				}
			}
			else
			{
				gDLL->UI().insertIntoSelectionList(pLoopUnit, true, false);
				return true;
			}
		}
		if (pLoopUnit == pSelectedUnit)
			break;
	}

	return false;
}


bool CvGame::selectCity(CvCity* pSelectCity, bool bCtrl, bool bAlt, bool bShift) const
{
	if (pSelectCity == NULL || !pSelectCity->canBeSelected())
		return false;
	if (!bShift)
		gDLL->UI().clearSelectedCities();
	if (bAlt)
	{
		FOR_EACH_CITY_VAR(pLoopCity, GET_PLAYER(pSelectCity->getOwner()))
			gDLL->UI().addSelectedCity(pLoopCity);
	}
	else if (bCtrl)
	{
		FOR_EACH_CITY_VAR(pLoopCity, GET_PLAYER(pSelectCity->getOwner()))
		{
			if (pLoopCity->sameArea(*pSelectCity))
				gDLL->UI().addSelectedCity(pLoopCity);
		}
	}
	else gDLL->UI().addSelectedCity(pSelectCity, bShift);
	return true;
}


void CvGame::selectionListMove(CvPlot* pPlot, bool bAlt, bool bShift, bool bCtrl) const
{
	if (pPlot == NULL)
		return;
	if (GC.getPythonCaller()->cannotSelectionListMoveOverride(*pPlot, bAlt, bShift, bCtrl))
		return;
	CvUnit* pHeadSelectedUnit = gDLL->UI().getHeadSelectedUnit();
	if (pHeadSelectedUnit == NULL || pHeadSelectedUnit->getOwner() != getActivePlayer())
		return;
	if (bAlt)
	{
		//gDLL->UI().selectGroup(pHeadSelectedUnit, false, false, true);
		gDLL->UI().selectGroup(pHeadSelectedUnit, false, true, true); // K-Mod
	}
	else if (bCtrl)
		gDLL->UI().selectGroup(pHeadSelectedUnit, false, true, false);
	/* bts code
	pSelectedUnitNode = gDLL->UI().headSelectionListNode();
	while (pSelectedUnitNode != NULL)
	{
		// advc: Rest deleted
		pSelectedUnitNode = gDLL->UI().nextSelectionListNode(pSelectedUnitNode);
	} */ // K-Mod has moved this to selectionListGameNetMessage.
	selectionListGameNetMessage(GAMEMESSAGE_PUSH_MISSION, MISSION_MOVE_TO,
			pPlot->getX(), pPlot->getY(), 0, false, bShift);
}


void CvGame::selectionListGameNetMessage(int eMessage, int iData2, int iData3, int iData4,
	int iFlags, bool bAlt, bool bShift) const
{
	int aiPyData[] = { iData2, iData3, iData4 };
	if (GC.getPythonCaller()->cannotSelectionListNetOverride((GameMessageTypes)
		eMessage, aiPyData, iFlags, bAlt, bShift))
	{
		return;
	}
	CvUnit* pHeadSelectedUnit = gDLL->UI().getHeadSelectedUnit();
	if (pHeadSelectedUnit == NULL || pHeadSelectedUnit->getOwner() != getActivePlayer())
		return; // advc

	CLLNode<IDInfo>* pSelectedUnitNode;
	CvUnit const* pSelectedUnit;
	if (eMessage == GAMEMESSAGE_JOIN_GROUP)
	{
		pSelectedUnitNode = gDLL->UI().headSelectionListNode();
		while (pSelectedUnitNode != NULL)
		{
			pSelectedUnit = ::getUnit(pSelectedUnitNode->m_data);
			pSelectedUnitNode = gDLL->UI().nextSelectionListNode(pSelectedUnitNode);
			if (bShift)
			{
				CvMessageControl::getInstance().sendJoinGroup(pSelectedUnit->getID(),
						FFreeList::INVALID_INDEX);
			}
			else
			{
				if (pSelectedUnit == pHeadSelectedUnit)
				{
					CvMessageControl::getInstance().sendJoinGroup(pSelectedUnit->getID(),
							FFreeList::INVALID_INDEX);
				}
				else // K-Mod
				{
					CvMessageControl::getInstance().sendJoinGroup(pSelectedUnit->getID(),
							pHeadSelectedUnit->getID());
				}
			}
		}
		if (bShift)
			gDLL->UI().selectUnit(pHeadSelectedUnit, true);
	}
	else if (eMessage == GAMEMESSAGE_DO_COMMAND)
	{	// K-Mod. When setting a unit to automate, we must be careful not to keep it grouped
		if (iData2 == COMMAND_AUTOMATE && !gDLL->UI().mirrorsSelectionGroup())
			selectionListGameNetMessage(GAMEMESSAGE_JOIN_GROUP);
		// K-Mod end
		pSelectedUnitNode = gDLL->UI().headSelectionListNode();
		while (pSelectedUnitNode != NULL)
		{
			pSelectedUnit = ::getUnit(pSelectedUnitNode->m_data);
			pSelectedUnitNode = gDLL->UI().nextSelectionListNode(pSelectedUnitNode);
			CvMessageControl::getInstance().sendDoCommand(pSelectedUnit->getID(),
					(CommandTypes)iData2, iData3, iData4, bAlt);
		}
	}
	else if (eMessage == GAMEMESSAGE_PUSH_MISSION || eMessage == GAMEMESSAGE_AUTO_MISSION)
	{
		if (!gDLL->UI().mirrorsSelectionGroup())
			selectionListGameNetMessage(GAMEMESSAGE_JOIN_GROUP);

		MovementFlags eFlags = (MovementFlags)iFlags;
		if (eMessage == GAMEMESSAGE_PUSH_MISSION)
		{	/*	K-Mod. I've moved the BUTTONPOPUP_DECLAREWARMOVE stuff to here
				from selectionListMove so that it can catch left-click moves
				as well as right-click moves.
				Note: If MOVE_DECLARE_WAR is set, then we assume it was set
				by a BUTTONPOPUP_DECLAREWARMOVE which was triggered already
				by this move. In which case we shouldn't check for declare war
				this time. This is a kludge to prevent the popup from appearing twice.
				Also, when this happens we should clear the MOVE_DECLARE_WAR flag.
				Otherwise it may cause the pathfinder to fail in some cases.
				(I'd rather not have UI stuff like this in this function,
				but this is the only place where I can catch left-click moves.) */
			if (iData2 == MISSION_MOVE_TO && !(eFlags & MOVE_DECLARE_WAR))
			{
				CvPlot* pPlot = GC.getMap().plot(iData3, iData4);
				FAssert(pPlot != NULL);
				pSelectedUnitNode = gDLL->UI().headSelectionListNode();
				while (pSelectedUnitNode != NULL)
				{
					pSelectedUnit = ::getUnit(pSelectedUnitNode->m_data);
					TeamTypes eRivalTeam = pSelectedUnit->getDeclareWarMove(pPlot);
					if (eRivalTeam != NO_TEAM)
					{	/* <advc.001> If an enemy unit is stacked with a neutral one,
							then the player apparently wants to attack the enemy unit
							(rather than declare war on the neutral party). However,
							if the enemy unit is on a tile owned by a third party that
							the player doesn't have OB or a vassal treaty with, then
							only a DoW on the third party makes sense. */
						if ((pPlot->getTeam() != NO_TEAM &&
							!GET_TEAM(pSelectedUnit->getTeam()).
							isFriendlyTerritory(pPlot->getTeam())) ||
							!pPlot->isVisibleEnemyUnit(pSelectedUnit))
						{ // </advc.001>
							CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_DECLAREWARMOVE);
							if (pInfo != NULL)
							{
								pInfo->setData1(eRivalTeam);
								pInfo->setData2(pPlot->getX());
								pInfo->setData3(pPlot->getY());
								pInfo->setOption1(bShift);
								pInfo->setOption2(pPlot->getTeam() != eRivalTeam);
								gDLL->UI().addPopup(pInfo);
							}
							return;
						}
					}
					// <advc.653> Disallow nuke attack through right-click
					if (pSelectedUnit->isNuke() &&
						gDLL->UI().getInterfaceMode() != INTERFACEMODE_NUKE &&
						!pSelectedUnit->canMoveInto(*pPlot))
					{
						return;
					} // </advc.653>
					pSelectedUnitNode = gDLL->UI().nextSelectionListNode(pSelectedUnitNode);
				}
			} // <advc.011b>
			bool bModified = false;
			if (iData2 == MISSION_BUILD ||
				iData2 == MISSION_PILLAGE || iData2 == MISSION_AIRBOMB) // advc.111
			{
				bModified = GC.ctrlKey();
			} // </advc.011b>
			// <advc.048>
			if (iData2 == MISSION_MOVE_TO)
				bModified = GC.altKey(); // </advc.048>
			CvMessageControl::getInstance().sendPushMission(pHeadSelectedUnit->getID(),
					(MissionTypes)iData2, iData3, iData4,
					eFlags & ~ MOVE_DECLARE_WAR, bShift, // K-Mod end
					bModified); // advc.011b
		}
		else CvMessageControl::getInstance().sendAutoMission(pHeadSelectedUnit->getID());
	}
	else FAssert(false);
}


void CvGame::selectedCitiesGameNetMessage(int eMessage, int iData2, int iData3, int iData4,
	bool bOption, bool bAlt, bool bShift, bool bCtrl) const
{
	for (CLLNode<IDInfo> const* pSelectedCityNode = gDLL->UI().headSelectedCitiesNode();
		pSelectedCityNode != NULL;
		pSelectedCityNode = gDLL->UI().nextSelectedCitiesNode(pSelectedCityNode))
	{
		CvCity* pSelectedCity = ::getCity(pSelectedCityNode->m_data);
		if (pSelectedCity == NULL || pSelectedCity->getOwner() != getActivePlayer())
			continue;
		switch (eMessage)
		{
		case GAMEMESSAGE_PUSH_ORDER:
			cityPushOrder(pSelectedCity, (OrderTypes)iData2, iData3, bAlt, bShift, bCtrl);
			break;
		case GAMEMESSAGE_POP_ORDER:
			/*if (pSelectedCity->getOrderQueueLength() > 1)
				CvMessageControl::getInstance().sendPopOrder(pSelectedCity->getID(), iData2);
			*/ // BtS
			// K-Mod. Some additional controls
			if (bAlt || (bShift != bCtrl))
			{
				// bCtrl moves the order up, bShift moves the order down.
				// bAlt toggles bSave (ie. repeat)
				int iNewPos = iData2 + (bShift ? 1 : 0) + (bCtrl ? -1 : 0);
				if (pSelectedCity->getOrderQueueLength() > iNewPos && iNewPos >= 0)
				{
					OrderData order = pSelectedCity->getOrderData(iData2);
					if (order.eOrderType != NO_ORDER &&
						(bShift || bCtrl || order.eOrderType == ORDER_TRAIN))
					{
						order.bSave = order.bSave != (bAlt && order.eOrderType == ORDER_TRAIN);
						CvMessageControl::getInstance().sendPopOrder(
								pSelectedCity->getID(), iData2);
						CvMessageControl::getInstance().sendPushOrder(
								pSelectedCity->getID(), order.eOrderType,
								order.iData1, order.bSave, false, iNewPos);
					}
				}
			}
			/*	Allow us to cancel the final order for automated cities.
				(The governor can choose production at the end of the turn.) */
			else if (pSelectedCity->getOrderQueueLength() > 1 ||
				pSelectedCity->isProductionAutomated())
			{
				CvMessageControl::getInstance().sendPopOrder(pSelectedCity->getID(), iData2);
			} // K-Mod end
			break;
		case GAMEMESSAGE_DO_TASK:
			CvMessageControl::getInstance().sendDoTask(pSelectedCity->getID(),
					(TaskTypes)iData2, iData3, iData4, bOption, bAlt, bShift, bCtrl);
			break;
		default:
			FAssert(false);
		}
	}
}


bool CvGame::canHandleAction(int iAction, CvPlot* pPlot, bool bTestVisible, bool bUseCache) const
{
	PROFILE_FUNC();

	bool const bShift = GC.shiftKey();

	if (GC.getPythonCaller()->cannotHandleActionOverride(pPlot, iAction, bTestVisible))
		return false;

	CvActionInfo const& kAction = GC.getActionInfo(iAction);
	if (kAction.getControlType() != NO_CONTROL &&
		canDoControl((ControlTypes)kAction.getControlType()))
	{
		return true;
	}
	if (gDLL->UI().isCitySelection())
		return false; // XXX hack!
	CvUnit* pHeadSelectedUnit = gDLL->UI().getHeadSelectedUnit();
	if (pHeadSelectedUnit == NULL || pHeadSelectedUnit->getOwner() != getActivePlayer())
		return false;
	if (!isMPOption(MPOPTION_SIMULTANEOUS_TURNS) &&
		!GET_PLAYER(pHeadSelectedUnit->getOwner()).isTurnActive())
	{
		return false;
	}
	CvSelectionGroup* pSelectedInterfaceList = gDLL->UI().getSelectionList();
	if (kAction.getMissionType() != NO_MISSION)
	{
		CvPlot* pMissionPlot = NULL;
		if (gDLL->UI().mirrorsSelectionGroup())
		{
			CvSelectionGroup* pSelectedGroup = pHeadSelectedUnit->getGroup();
			if (pPlot != NULL)
				pMissionPlot = pPlot;
			else if (bShift)
				pMissionPlot = pSelectedGroup->lastMissionPlot();
			else pMissionPlot = NULL;
			if (pMissionPlot == NULL ||
				!pMissionPlot->isVisible(pHeadSelectedUnit->getTeam()))
			{
				pMissionPlot = pSelectedGroup->plot();
			}
		}
		else pMissionPlot = pSelectedInterfaceList->plot();
		if (pSelectedInterfaceList->canStartMission((MissionTypes)kAction.getMissionType(),
			kAction.getMissionData(), -1, pMissionPlot, bTestVisible, bUseCache))
		{
			return true;
		}
	}
	if (kAction.getCommandType() != NO_COMMAND)
	{
		if (pSelectedInterfaceList->canDoCommand((CommandTypes)
			kAction.getCommandType(),
			kAction.getCommandData(), -1, bTestVisible, bUseCache))
		{
			return true;
		}
	}
	if (gDLL->UI().canDoInterfaceMode((InterfaceModeTypes)
		kAction.getInterfaceModeType(), pSelectedInterfaceList))
	{
		return true;
	}
	return false;
}


void CvGame::setupActionCache() const
{
	gDLL->UI().getSelectionList()->setupActionCache();
}


void CvGame::handleAction(int iAction)
{
	bool const bAlt = GC.altKey();
	bool const bShift = GC.shiftKey();

	if (!gDLL->UI().canHandleAction(iAction))
		return;
	CvActionInfo const& kAction = GC.getActionInfo(iAction);
	if (kAction.getControlType() != NO_CONTROL)
		doControl((ControlTypes)kAction.getControlType());
	if (gDLL->UI().canDoInterfaceMode((InterfaceModeTypes)kAction.getInterfaceModeType(),
		gDLL->UI().getSelectionList()))
	{
		CvUnit* pHeadSelectedUnit = gDLL->UI().getHeadSelectedUnit();
		if (pHeadSelectedUnit != NULL)
		{
			if (GC.getInfo((InterfaceModeTypes)
				kAction.getInterfaceModeType()).getSelectAll())
			{
				//gDLL->UI().selectGroup(pHeadSelectedUnit, false, false, true);
				gDLL->UI().selectGroup(pHeadSelectedUnit, false, true, true); // K-Mod
			}
			else if (GC.getInfo((InterfaceModeTypes)
				kAction.getInterfaceModeType()).getSelectType())
			{
				gDLL->UI().selectGroup(pHeadSelectedUnit, false, true, false);
			}
		}

		gDLL->UI().setInterfaceMode((InterfaceModeTypes)
				kAction.getInterfaceModeType());
	}
	if (kAction.getMissionType() != NO_MISSION)
	{
		selectionListGameNetMessage(GAMEMESSAGE_PUSH_MISSION, kAction.getMissionType(),
				kAction.getMissionData(), -1, 0, false, bShift);
	}
	if (kAction.getCommandType() != NO_COMMAND)
	{
		bool bSkip = false;

		if (kAction.getCommandType() == COMMAND_LOAD)
		{
			CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_LOADUNIT);
			if (NULL != pInfo)
			{
				gDLL->UI().addPopup(pInfo);
				bSkip = true;
			}
		}
		if (!bSkip)
		{
			if (kAction.isConfirmCommand())
			{
				CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_CONFIRMCOMMAND);
				if (NULL != pInfo)
				{
					pInfo->setData1(iAction);
					pInfo->setOption1(bAlt);
					gDLL->UI().addPopup(pInfo);
				}
			}
			else
			{
				selectionListGameNetMessage(GAMEMESSAGE_DO_COMMAND,
						kAction.getCommandType(),
						kAction.getCommandData(), -1, 0, bAlt);
			}
		}
	}
}


bool CvGame::canDoControl(ControlTypes eControl) const
{
	if (GC.getPythonCaller()->cannotDoControlOverride(eControl))
		return false;

	/*  <advc.706> I don't think loading is possible in between turns, but there
		would be no harm in it. */
	if (CvPlot::isAllFog() && eControl != CONTROL_LOAD_GAME &&
		eControl != CONTROL_QUICK_LOAD && eControl != CONTROL_OPTIONS_SCREEN)
	{
		return false;
	} // </advc.706>
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
		if (!gDLL->UI().isFocused())
			return true;
		break;

	case CONTROL_FORCEENDTURN:
		if (!gDLL->UI().isFocused() && !gDLL->UI().isInAdvancedStart())
			return true;
		break;

	case CONTROL_PING:
	case CONTROL_SIGN:
	case CONTROL_GRID:
	case CONTROL_BARE_MAP:
	case CONTROL_YIELDS:
	case CONTROL_RESOURCE_ALL:
	case CONTROL_UNIT_ICONS:
	case CONTROL_STABILITY_OVERLAY: // doc (edead)
	case CONTROL_GLOBELAYER:
	case CONTROL_SCORES:
	case CONTROL_FREE_COLONY:
		if (!gDLL->UI().isFocusedWidget())
			return true;
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

	case CONTROL_ESPIONAGE_SCREEN:
		if (!isOption(GAMEOPTION_NO_ESPIONAGE))
			return true;
		break;

	case CONTROL_NEXTCITY:
	case CONTROL_PREVCITY:
		if (!gDLL->UI().isSpaceshipScreenUp())
			return true;
		break;

	case CONTROL_ADMIN_DETAILS:
		return true;

	case CONTROL_CENTERONSELECTION:
		if (gDLL->UI().getLookAtPlot() != gDLL->UI().getSelectionPlot())
			return true;
		break;

	case CONTROL_LOAD_GAME:
		if (!isNetworkMultiPlayer())
			return true;
		break;

	case CONTROL_RETIRE:
		if (getGameState() == GAMESTATE_ON || isGameMultiPlayer())
		{
			if (GET_PLAYER(getActivePlayer()).isAlive())
			{
				if (isPbem() || isHotSeat())
				{
					if (!GET_PLAYER(getActivePlayer()).isEndTurn())
						return true;
				}
				else return true;
			}
		}
		break;

	case CONTROL_WORLD_BUILDER:
		return isDebugToolsAllowed(true); // advc.135c
		/*if (!(isGameMultiPlayer()) && GC.getInitCore().getAdminPassword().empty() && !gDLL->UI().isInAdvancedStart())
			return true;*/
		break;

	case CONTROL_ENDTURN:
	case CONTROL_ENDTURN_ALT:
		if (gDLL->UI().isEndTurnMessage() &&
			!gDLL->UI().isFocused() &&
			!gDLL->UI().isInAdvancedStart())
		{
			return true;
		}
		break;
	// <advc.088>
	case CONTROL_UNSELECT_ALL:
		if (gDLL->UI().getInterfaceMode() == INTERFACEMODE_SELECTION &&
			!gDLL->UI().isCityScreenUp() && gDLL->UI().getHeadSelectedUnit() != NULL)
		{
			return true;
		}
		break; // </advc.088>

	default:
		FErrorMsg("eControl did not match any valid options");
	}

	return false;
}


void CvGame::doControl(ControlTypes eControl)
{
	if (!canDoControl(eControl))
		return;
	// <advc>
	CvDLLInterfaceIFaceBase& kUI = gDLL->UI();
	CvDLLEngineIFaceBase& kEngine = *gDLL->getEngineIFace();
	CvUnit* pHeadSelectedUnit = kUI.getHeadSelectedUnit();
	CvPlot* pSelectionPlot = kUI.getSelectionPlot();
	// </advc>
	switch (eControl)
	{
	case CONTROL_CENTERONSELECTION:
		kUI.lookAtSelectionPlot();
		break;

	case CONTROL_SELECTYUNITTYPE:
		if (pHeadSelectedUnit != NULL)
			kUI.selectGroup(pHeadSelectedUnit, false, true, false);
		break;

	case CONTROL_SELECTYUNITALL:
		if (pHeadSelectedUnit != NULL)
		{
			kUI.selectGroup(pHeadSelectedUnit, false,
					/*false, true*/ true, true); // K-Mod
		}
		break;

	case CONTROL_SELECT_HEALTHY:  // advc: Refactored this case
		if (pHeadSelectedUnit != NULL)
		{
			/*  <advc.001z> Compute the units to be selected upfront b/c, if there
				are none, then the current selection shouldn't be cleared. */
			std::vector<CvUnit*> toBeSelected;
			std::vector<CvUnit*> plotUnits;
			getPlotUnits(pHeadSelectedUnit->plot(), plotUnits);
			for (size_t i = 0; i < plotUnits.size(); i++)
			{
				CvUnit& kUnit = *plotUnits[i];
				// disabled by K-Mod
				//if (!isMPOption(MPOPTION_SIMULTANEOUS_TURNS) || getTurnSlice() - kUnit.getLastMoveTurn() > GC.getDefineINT("MIN_TIMER_UNIT_DOUBLE_MOVES")) {
				if (kUnit.getOwner() == getActivePlayer() && kUnit.isHurt() &&
					// advc.001z: Can't select units of different domains
					kUnit.getDomainType() == pHeadSelectedUnit->getDomainType())
				{
					toBeSelected.push_back(&kUnit);
				}
			}
			if (!toBeSelected.empty()) // advc.001z
			{
				kUI.clearSelectionList();
				kUI.selectionListPreChange();
				CvUnit const* pGroupHead = NULL;
				for (size_t i = 0; i < toBeSelected.size(); i++) // advc.001z
				{
					CvUnit* pUnit = toBeSelected[i]; // advc.001z
					if (pGroupHead != NULL)
					{
						CvMessageControl::getInstance().sendJoinGroup(
								pUnit->getID(), pGroupHead->getID());
					}
					else pGroupHead = pUnit;
					kUI.insertIntoSelectionList(pUnit, false, false, true, true, true);
				}
				kUI.selectionListPostChange();
			}
		}
		break;

	case CONTROL_SELECTCITY:
		if (kUI.isCityScreenUp())
			cycleCities();
		else kUI.selectLookAtCity();
		break;

	case CONTROL_SELECTCAPITAL:
	{
		CvCity* pCapital = GET_PLAYER(getActivePlayer()).getCapital();
		if (pCapital != NULL)
			kUI.selectCity(pCapital);
		break;
	}
	case CONTROL_NEXTCITY:
		if (kUI.isCitySelection())
			cycleCities(true, !kUI.isCityScreenUp());
		else kUI.selectLookAtCity(true);
		kUI.lookAtSelectionPlot();
		break;

	case CONTROL_PREVCITY:
		if (kUI.isCitySelection())
			cycleCities(false, !kUI.isCityScreenUp());
		else kUI.selectLookAtCity(true);
		kUI.lookAtSelectionPlot();
		break;

	case CONTROL_NEXTUNIT:
		if (pSelectionPlot != NULL)
			cyclePlotUnits(pSelectionPlot);
		break;

	case CONTROL_PREVUNIT:
		if (pSelectionPlot != NULL)
			cyclePlotUnits(pSelectionPlot, false);
		break;

	case CONTROL_CYCLEUNIT:
	case CONTROL_CYCLEUNIT_ALT:
		cycleSelectionGroups(true);
		break;

	case CONTROL_CYCLEWORKER:
		cycleSelectionGroups(true, true, true);
		break;

	case CONTROL_LASTUNIT:
	{
		CvUnit* pUnit = kUI.getLastSelectedUnit();
		if (pUnit != NULL)
		{
			kUI.selectUnit(pUnit, true);
			kUI.lookAtSelectionPlot();
		}
		else cycleSelectionGroups(true, false);

		kUI.setLastSelectedUnit(NULL);
		break;
	}
	case CONTROL_ENDTURN:
	case CONTROL_ENDTURN_ALT:
		if (kUI.isEndTurnMessage())
			CvMessageControl::getInstance().sendTurnComplete();
		break;

	case CONTROL_FORCEENDTURN:
		CvMessageControl::getInstance().sendTurnComplete();
		break;

	case CONTROL_AUTOMOVES:
		CvMessageControl::getInstance().sendAutoMoves();
		break;

	case CONTROL_PING:
		kUI.setInterfaceMode(INTERFACEMODE_PING);
		break;

	case CONTROL_SIGN:
		kUI.setInterfaceMode(INTERFACEMODE_SIGN);
		break;

	case CONTROL_GRID:
		kEngine.SetGridMode(!kEngine.GetGridMode());
		break;

	case CONTROL_BARE_MAP:
		kUI.toggleBareMapMode();
		break;

	case CONTROL_YIELDS:
		kUI.toggleYieldVisibleMode();
		break;

	case CONTROL_RESOURCE_ALL:
		kEngine.toggleResourceLayer();
		break;

	case CONTROL_UNIT_ICONS:
		kEngine.toggleUnitLayer();
		break;

	case CONTROL_GLOBELAYER:
		kEngine.toggleGlobeview();
		break;

	case CONTROL_SCORES:
		kUI.toggleScoresVisible();
		break;

	case CONTROL_LOAD_GAME:
		gDLL->LoadGame();
		break;

	case CONTROL_OPTIONS_SCREEN:
		GC.getPythonCaller()->showPythonScreen("OptionsScreen");
		break;

	case CONTROL_RETIRE: // <advc.706> Need three buttons, so no BUTTONPOPUP_CONFIRM_MENU.
		if (isOption(GAMEOPTION_RISE_FALL))
		{
			CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_RF_RETIRE);
			if (pInfo != NULL)
				kUI.addPopup(pInfo, getActivePlayer(), true);
		}
		else // </advc.706>
		// K-Mod. (original code moved into CvGame::retire)
		{
			CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_CONFIRM_MENU);
			if (pInfo != NULL)
			{
				pInfo->setData1(2);
				kUI.addPopup(pInfo, getActivePlayer(), true);
			}
		} // K-Mod end
		break;

	case CONTROL_SAVE_GROUP:
		gDLL->SaveGame(SAVEGAME_GROUP);
		break;

	case CONTROL_SAVE_NORMAL:
		gDLL->SaveGame(SAVEGAME_NORMAL);
		break;

	case CONTROL_QUICK_SAVE:
		if (!isNetworkMultiPlayer()) // SP only!
		{
			CvEventReporter::getInstance().preQuickSave(); // advc.106l
			gDLL->QuickSave();
		}
		break;

	case CONTROL_QUICK_LOAD:
		if (isNetworkMultiPlayer()) // SP only!
			break;
		// <advc.003d>
		/*  Loading works fine in windowed mode, and when a debugger is
			attached, exitingToMainMenu can actually be quite slow.
			(Fullscreen pretty much rules out that a debugger is attached.) */
		if (gDLL->getGraphicOption(GRAPHICOPTION_FULLSCREEN))
		{
			/*  On my system, it's "C:\\Users\\Administrator\\Documents\\My Games\\Beyond the Sword\\Saves\\single\\quick\\QuickSave.CivBeyondSwordSave";
				the user directory can vary. */
			CvString szQuickSavePath(BUGOption::userDirPath());
			if (!szQuickSavePath.empty())
			{
				szQuickSavePath += "\\Beyond the Sword\\Saves\\single\\quick\\QuickSave.CivBeyondSwordSave";
				// CTD if loading fails, so let's make sure that the file is good.
				std::ifstream quickSaveFile(szQuickSavePath);
				if (quickSaveFile.good())
				{
					kUI.exitingToMainMenu(szQuickSavePath.c_str());
					break;
				}
			}
			FErrorMsg("Failed to find quicksave");
		} // </advc.003d>
		gDLL->QuickLoad();
		break;

	case CONTROL_ORTHO_CAMERA:
		kEngine.SetOrthoCamera(!kEngine.GetOrthoCamera());
		break;

	case CONTROL_CYCLE_CAMERA_FLYING_MODES:
		kEngine.CycleFlyingMode(1);
		break;

	case CONTROL_ISOMETRIC_CAMERA_LEFT:
		kEngine.MoveBaseTurnLeft();
		break;

	case CONTROL_ISOMETRIC_CAMERA_RIGHT:
		kEngine.MoveBaseTurnRight();
		break;

	case CONTROL_FLYING_CAMERA:
		kEngine.SetFlying(!kEngine.GetFlying());
		break;

	case CONTROL_MOUSE_FLYING_CAMERA:
		kEngine.SetMouseFlying(!kEngine.GetMouseFlying());
		break;

	case CONTROL_TOP_DOWN_CAMERA:
		kEngine.SetSatelliteMode(!kEngine.GetSatelliteMode());
		break;

	case CONTROL_CIVILOPEDIA:
		GC.getPythonCaller()->callScreenFunction("pediaShow");
		break;

	case CONTROL_RELIGION_SCREEN:
		GET_PLAYER(getActivePlayer()).killAll(BUTTONPOPUP_CHANGERELIGION); // advc.004x
		GC.getPythonCaller()->showPythonScreen("ReligionScreen");
		break;

	case CONTROL_CORPORATION_SCREEN:
		GC.getPythonCaller()->showPythonScreen("CorporationScreen");
		break;

	case CONTROL_CIVICS_SCREEN:
		GET_PLAYER(getActivePlayer()).killAll(BUTTONPOPUP_CHANGECIVIC); // advc.004x
		GC.getPythonCaller()->showPythonScreen("CivicsScreen");
		break;

	case CONTROL_FOREIGN_SCREEN:
		GC.getPythonCaller()->showForeignAdvisorScreen();
		break;

	case CONTROL_FINANCIAL_SCREEN:
		GC.getPythonCaller()->showPythonScreen("FinanceAdvisor");
		break;

	case CONTROL_MILITARY_SCREEN:
		GC.getPythonCaller()->showPythonScreen("MilitaryAdvisor");
		break;

	case CONTROL_TECH_CHOOSER:
		GC.getPythonCaller()->showPythonScreen("TechChooser");
		break;

	case CONTROL_TURN_LOG:
		if (!gDLL->GetWorldBuilderMode() || kUI.isInAdvancedStart())
			kUI.toggleTurnLog();
		break;

	case CONTROL_CHAT_ALL:
		if (!gDLL->GetWorldBuilderMode() || kUI.isInAdvancedStart())
			kUI.showTurnLog(CHATTARGET_ALL);
		break;

	case CONTROL_CHAT_TEAM:
		if (!gDLL->GetWorldBuilderMode() || kUI.isInAdvancedStart())
			kUI.showTurnLog(CHATTARGET_TEAM);
		break;

	case CONTROL_DOMESTIC_SCREEN:
		//argsList.add(-1); // advc.003y: Unused param removed from CyScreensInterface.py
		GC.getPythonCaller()->showPythonScreen("DomesticAdvisor");
		break;

	case CONTROL_VICTORY_SCREEN:
		GC.getPythonCaller()->showPythonScreen("VictoryScreen");
		break;

	case CONTROL_INFO:
		GC.getPythonCaller()->showInfoScreen(0, getGameState() != GAMESTATE_ON);
		break;

	case CONTROL_GLOBE_VIEW:
		kEngine.toggleGlobeview();
		break;

	case CONTROL_DETAILS:
		kUI.showDetails();
		break;

	case CONTROL_ADMIN_DETAILS:
		if (GC.getInitCore().getAdminPassword().empty())
			kUI.showAdminDetails();
		else
		{
			CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_ADMIN_PASSWORD);
			if (pInfo != NULL)
			{
				pInfo->setData1((int)CONTROL_ADMIN_DETAILS);
				kUI.addPopup(pInfo, NO_PLAYER, true);
			}
		}
		break;

	case CONTROL_HALL_OF_FAME:
		GC.getPythonCaller()->showHallOfFameScreen(true);
		break;

	case CONTROL_WORLD_BUILDER:
		// K-Mod. (original code moved into CvGame::retire)
		// <advc.007>
		if (isDebugMode())
			enterWorldBuilder();
		else // </advc.007>
		{
			CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_CONFIRM_MENU);
			if (pInfo != NULL)
			{
				pInfo->setData1(4);
				kUI.addPopup(pInfo, getActivePlayer(), true);
			}
		} // K-Mod end
		break;

	case CONTROL_ESPIONAGE_SCREEN:
		GC.getPythonCaller()->showPythonScreen("EspionageAdvisor");
		break;

	case CONTROL_FREE_COLONY:
	{
		CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_FREE_COLONY);
		if (pInfo != NULL)
			kUI.addPopup(pInfo);
		break;
	}
	case CONTROL_DIPLOMACY:
	{
		CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_DIPLOMACY);
		if (pInfo != NULL)
			kUI.addPopup(pInfo);
		break;
	}  // <advc.088>
	case CONTROL_UNSELECT_ALL:
	{
		kUI.clearSelectionList();
		break;
	} // </advc.088>
	// doc (edead)
	case CONTROL_STABILITY_OVERLAY:
	{
		gDLL->getPythonIFace()->callFunction(PYScreensModule, "toggleStabilityOverlay");
		break;
	}
	default: FErrorMsg("Unknown control type");
	}
}

/*	K-Mod. This code use to be inside CvGame::doControl. I've moved it here and
	told doControl to simply create a confirmation popup. */
void CvGame::retire()
{
	FAssert(canDoControl(CONTROL_RETIRE));

	if (!isGameMultiPlayer() || countHumanPlayersAlive() == 1)
	{
		if (gDLL->GetAutorun())
		{
			GC.getInitCore().setSlotStatus(getActivePlayer(), SS_COMPUTER);
		}
		else
		{
			setGameState(GAMESTATE_OVER);
			gDLL->UI().setDirty(Soundtrack_DIRTY_BIT, true);
		}
	}
	else
	{
		if (isNetworkMultiPlayer())
		{
			gDLL->sendMPRetire();
			GC.getGame().exitToMenu();
		}
		else gDLL->handleRetirement(getActivePlayer());
	}
}


void CvGame::enterWorldBuilder()
{
	FAssert(canDoControl(CONTROL_WORLD_BUILDER));
	if (GC.getInitCore().getAdminPassword().empty())
	{	// <advc.135c>
		/*  In multiplayer, setWorldBuilder apparently checks ChtLvl>0 and setChtLvl
			doesn't work. Need to make the EXE believe that we're in singleplayer. */
		m_bFeignSP = true;
		gDLL->setChtLvl(1); // </advc.135c>
		gDLL->UI().setWorldBuilder(!gDLL->GetWorldBuilderMode());
		m_bFeignSP = false; // advc.135c
	}
	else
	{
		CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_ADMIN_PASSWORD);
		if (NULL != pInfo)
		{
			pInfo->setData1((int)CONTROL_WORLD_BUILDER);
			gDLL->UI().addPopup(pInfo, NO_PLAYER, true);
		}
	}
} // K-Mod end

/*	advc: Wrapper for CvDLLInterfaceIFaceBase::exitingToMainMenu.
	In case that there's something we want to do beforehand. */
void CvGame::exitToMenu()
{
	gDLL->UI().exitingToMainMenu();
}

// advc:
void CvGame::setGlobeView(bool b)
{
	if (gDLL->getEngineIFace()->isGlobeviewUp() != b)
		gDLL->getEngineIFace()->toggleGlobeview();
}


void CvGame::getGlobeLayers(std::vector<CvGlobeLayerData>& aLayers) const
{
	CvGlobeLayerData kUnit(GLOBE_LAYER_UNIT);
	kUnit.m_strName = "UNITS";
	kUnit.m_strButtonHelpTag = "TXT_KEY_GLOBELAYER_UNITS";
	kUnit.m_strButtonStyle = "Button_HUDGlobeUnit_Style";
	kUnit.m_iNumOptions =
			(GC.getDefineINT("SHOW_UNIT_LAYER_OPTIONS") <= 0 ? 0 : // advc.004z
			NUM_UNIT_OPTION_TYPES);
	kUnit.m_bGlobeViewRequired = false;
	aLayers.push_back(kUnit);

	CvGlobeLayerData kResource(GLOBE_LAYER_RESOURCE);
	kResource.m_strName = "RESOURCES";
	kResource.m_strButtonHelpTag = "TXT_KEY_GLOBELAYER_RESOURCES";
	kResource.m_strButtonStyle = "Button_HUDBtnResources_Style";
	/*  advc.004z (comment): Could check and enforce
		getBugOptionBOOL("MainInterface__ResourceIconOptions", false)
		here, but then the BUG option would require a restart. Therefore,
		this is done in CvMainInterface.py (updateGlobeviewButtons) instead. */
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


void CvGame::startFlyoutMenu(CvPlot const* pPlot,
	std::vector<CvFlyoutMenuData>& aFlyoutItems) const
{
	aFlyoutItems.clear();

	bool bUnits = false;
	bool bFortifyUnit = false;
	bool bSleepUnit = false;
	bool bWakeUnit = false;

	FOR_EACH_UNIT_IN(pUnit, *pPlot)
	{
		if (pUnit->getOwner() != getActivePlayer())
			continue;
		bUnits = true;
		if (pUnit->canFortify(pPlot))
			bFortifyUnit = true;
		else if (pUnit->canSleep(pPlot))
			bSleepUnit = true;
		else if (pUnit->isWaiting())
			bWakeUnit = true;
	}

	CvWString szBuffer;
	CvCity* pCity = pPlot->getPlotCity();
	if (pCity != NULL && pCity->getOwner() == getActivePlayer())
	{
		szBuffer = gDLL->getText("TXT_KEY_CHANGE_PRODUCTION");
		aFlyoutItems.push_back(CvFlyoutMenuData(NO_FLYOUT, -1, -1, -1, szBuffer));
		CvCivilization const& kCiv = pCity->getCivilization(); // advc.003w
		for (int i = 0; i < kCiv.getNumUnits(); i++)
		{
			UnitTypes eLoopUnit = kCiv.unitAt(i);
			if (!pCity->canTrain(eLoopUnit))
				continue;
			szBuffer = GC.getInfo(eLoopUnit).getDescription();
			int iTurns = pCity->getProductionTurnsLeft(eLoopUnit, 0);
			if (iTurns < MAX_INT) // advc.004x
				szBuffer.append(CvWString::format(L" (%d)", iTurns));
			aFlyoutItems.push_back(CvFlyoutMenuData(FLYOUT_TRAIN, eLoopUnit,
					pPlot->getX(), pPlot->getY(), szBuffer));
		}
		for (int i = 0; i < kCiv.getNumBuildings(); i++)
		{
			BuildingTypes eLoopBuilding = kCiv.buildingAt(i);
			if (!pCity->canConstruct(eLoopBuilding))
				continue;
			szBuffer = GC.getInfo(eLoopBuilding).getDescription();
			int iTurns = pCity->getProductionTurnsLeft(eLoopBuilding, 0);
			if (iTurns < MAX_INT) // advc.004x
				szBuffer.append(CvWString::format(L" (%d)", iTurns));
			aFlyoutItems.push_back(CvFlyoutMenuData(FLYOUT_CONSTRUCT, eLoopBuilding,
					pPlot->getX(), pPlot->getY(), szBuffer));
		}
		FOR_EACH_ENUM(Project)
		{
			if (!pCity->canCreate(eLoopProject))
				continue;
			szBuffer = GC.getInfo(eLoopProject).getDescription();
			int iTurns = pCity->getProductionTurnsLeft(eLoopProject, 0);
			if (iTurns < MAX_INT) // advc.004x
				szBuffer.append(CvWString::format(L" (%d)", iTurns));
			aFlyoutItems.push_back(CvFlyoutMenuData(FLYOUT_CREATE, eLoopProject,
					pPlot->getX(), pPlot->getY(), szBuffer));
		}
		FOR_EACH_ENUM(Process)
		{
			if (!pCity->canMaintain(eLoopProcess))
				continue;
			szBuffer = GC.getInfo(eLoopProcess).getDescription();
			aFlyoutItems.push_back(CvFlyoutMenuData(FLYOUT_MAINTAIN, eLoopProcess,
					pPlot->getX(), pPlot->getY(), szBuffer));
		}

		aFlyoutItems.push_back(CvFlyoutMenuData(NO_FLYOUT, -1, -1, -1, L""));
		FOR_EACH_ENUM(Hurry)
		{
			if (!pCity->canHurry(eLoopHurry))
				continue;
			szBuffer = gDLL->getText("TXT_KEY_HURRY_PRODUCTION");
			int iHurryGold = pCity->hurryGold(eLoopHurry);
			if (iHurryGold > 0)
				szBuffer += gDLL->getText("TXT_KEY_HURRY_PRODUCTION_GOLD", iHurryGold);
			int iHurryPopulation = pCity->hurryPopulation(eLoopHurry);
			if (iHurryPopulation > 0)
				szBuffer += gDLL->getText("TXT_KEY_HURRY_PRODUCTION_POP", iHurryPopulation);
				aFlyoutItems.push_back(CvFlyoutMenuData(FLYOUT_HURRY, eLoopHurry,
						pPlot->getX(), pPlot->getY(), szBuffer));
		}

		if (pCity->canConscript())
		{
			UnitTypes eConscriptUnit = pCity->getConscriptUnit();
			if (eConscriptUnit != NO_UNIT)
			{
				szBuffer = gDLL->getText("TXT_KEY_DRAFT_UNIT",
						GC.getInfo(eConscriptUnit).getDescription(),
						pCity->getConscriptPopulation());
				aFlyoutItems.push_back(CvFlyoutMenuData(FLYOUT_CONSCRIPT,
						GC.getNumHurryInfos(), pPlot->getX(), pPlot->getY(), szBuffer));
			}
		}
	}

	CvUnit* pHeadSelectedUnit = gDLL->UI().getHeadSelectedUnit();
	if (pHeadSelectedUnit != NULL && !pHeadSelectedUnit->atPlot(pPlot))
	{
		gDLL->getFAStarIFace()->SetData(&GC.getInterfacePathFinder(),
				gDLL->UI().getSelectionList());
		if (pHeadSelectedUnit->getDomainType() == DOMAIN_AIR ||
			gDLL->getFAStarIFace()->GeneratePath(&GC.getInterfacePathFinder(),
			pHeadSelectedUnit->getX(), pHeadSelectedUnit->getY(),
			pPlot->getX(), pPlot->getY(), false, MOVE_DECLARE_WAR, true))
		{
			if (pHeadSelectedUnit->getDomainType() == DOMAIN_AIR)
				szBuffer = gDLL->getText("TXT_KEY_FLYOUT_MENU_FLY_TO");
			else
			{
				szBuffer = gDLL->getText("TXT_KEY_FLYOUT_MENU_MOVE_TO",
						gDLL->getFAStarIFace()->GetLastNode(
						&GC.getInterfacePathFinder())->m_iData2);
			}
			aFlyoutItems.push_back(CvFlyoutMenuData(FLYOUT_MOVE_TO, 0,
					pPlot->getX(), pPlot->getY(), szBuffer));
		}
	}

	if (bUnits)
	{
		szBuffer = gDLL->getText("TXT_KEY_FLYOUT_MENU_SELECT_ALL");
		aFlyoutItems.push_back(CvFlyoutMenuData(FLYOUT_SELECT_ALL,
				0, pPlot->getX(), pPlot->getY(), szBuffer));

		if (bWakeUnit)
		{
			szBuffer = gDLL->getText("TXT_KEY_FLYOUT_MENU_WAKE_ALL");
			aFlyoutItems.push_back(CvFlyoutMenuData(FLYOUT_WAKE_ALL,
					0, pPlot->getX(), pPlot->getY(), szBuffer));
		}

		if (bFortifyUnit)
		{
			szBuffer = gDLL->getText("TXT_KEY_FLYOUT_MENU_FORTIFY_ALL");
			aFlyoutItems.push_back(CvFlyoutMenuData(FLYOUR_FORTIFY_ALL,
					0, pPlot->getX(), pPlot->getY(), szBuffer));
		}
		else if (bSleepUnit)
		{
			szBuffer = gDLL->getText("TXT_KEY_FLYOUT_MENU_SLEEP_ALL");
			aFlyoutItems.push_back(CvFlyoutMenuData(FLYOUR_SLEEP_ALL,
					0, pPlot->getX(), pPlot->getY(), szBuffer));
		}

		static std::vector<CvUnit*> plotUnits;
		getPlotUnits(pPlot, plotUnits);
		for (int iI = 0; iI < (int)plotUnits.size(); iI++)
		{
			CvUnit* pLoopUnit = plotUnits[iI];
			if (pLoopUnit->getOwner() == getActivePlayer())
			{
				CvWStringBuffer szTempBuffer;
				GAMETEXT.setUnitHelp(szTempBuffer, pLoopUnit, true);
				aFlyoutItems.push_back(CvFlyoutMenuData(FLYOUT_SELECT_UNIT,
						pLoopUnit->getID(), pPlot->getX(), pPlot->getY(),
						szTempBuffer.getCString()));
			}
		}
	}
}


void CvGame::applyFlyoutMenu(CvFlyoutMenuData const& kItem)
{
	CvPlot* pPlot = GC.getMap().plot(kItem.m_iX, kItem.m_iY);
	if (pPlot == NULL)
		return;

	switch (kItem.m_eFlyout)
	{
	case NO_FLYOUT:
	default:
		FAssert(false);
		break;

	case FLYOUT_HURRY:
	{
		CvCity* pCity = pPlot->getPlotCity();
		if (pCity != NULL && pCity->getOwner() == getActivePlayer())
		{
			CvMessageControl::getInstance().sendDoTask(pCity->getID(),
					TASK_HURRY, kItem.m_iID, -1, false, false, false, false);
		}
		break;
	}

	case FLYOUT_CONSCRIPT:
	{
		CvCity* pCity = pPlot->getPlotCity();
		if (pCity != NULL && pCity->getOwner() == getActivePlayer())
		{
			CvMessageControl::getInstance().sendDoTask(pCity->getID(),
					TASK_CONSCRIPT, -1, -1, false, false, false, false);
		}
		break;
	}

	case FLYOUT_TRAIN:
	{
		CvCity* pCity = pPlot->getPlotCity();
		if (pCity != NULL && pCity->getOwner() == getActivePlayer())
			cityPushOrder(pCity, ORDER_TRAIN, kItem.m_iID);
		break;
	}

	case FLYOUT_CONSTRUCT:
	{
		CvCity* pCity = pPlot->getPlotCity();
		if (pCity != NULL && pCity->getOwner() == getActivePlayer())
			cityPushOrder(pCity, ORDER_CONSTRUCT, kItem.m_iID);
		break;
	}

	case FLYOUT_CREATE:
	{
		CvCity* pCity = pPlot->getPlotCity();
		if (pCity != NULL && pCity->getOwner() == getActivePlayer())
			cityPushOrder(pCity, ORDER_CREATE, kItem.m_iID);
		break;
	}

	case FLYOUT_MAINTAIN:
	{
		CvCity* pCity = pPlot->getPlotCity();
		if (pCity != NULL && pCity->getOwner() == getActivePlayer())
			cityPushOrder(pCity, ORDER_MAINTAIN, kItem.m_iID);
		break;
	}

	case FLYOUT_MOVE_TO:
		selectionListMove(pPlot, false, false, false);
		break;

	case FLYOUT_SELECT_UNIT:
	{
		CvUnit* pUnit = GET_PLAYER(getActivePlayer()).getUnit(kItem.m_iID);
		if (pUnit != NULL)
			gDLL->UI().selectUnit(pUnit, true);
		break;
	}

	case FLYOUT_SELECT_ALL:
		gDLL->UI().selectAll(pPlot);
		break;

	case FLYOUT_WAKE_ALL:
	{
		FOR_EACH_UNIT_IN(pUnit, *pPlot)
		{
			if (pUnit->isGroupHead() &&
				pUnit->getOwner() == getActivePlayer()) // K-Mod
			{
				CvMessageControl::getInstance().sendDoCommand(pUnit->getID(),
						COMMAND_WAKE, -1, -1, false);
			}
		}
		break;
	}
	case FLYOUR_FORTIFY_ALL:
	case FLYOUR_SLEEP_ALL:
	{
		FOR_EACH_UNIT_IN(pUnit, *pPlot)
		{
			if (pUnit->isGroupHead() &&
				pUnit->getOwner() == getActivePlayer()) // K-Mod
			{
				CvMessageControl::getInstance().sendPushMission(pUnit->getID(),
						pUnit->isFortifyable() ? MISSION_FORTIFY : MISSION_SLEEP,
						-1, -1, NO_MOVEMENT_FLAGS, false, /* advc.011b: */ GC.ctrlKey());
			}
		}
		break;
	}
	}
}


CvPlot* CvGame::getNewHighlightPlot() const
{
	if (gDLL->GetWorldBuilderMode())
		return GC.getPythonCaller()->WBGetHighlightPlot();
	if (GC.getInfo(gDLL->UI().getInterfaceMode()).getHighlightPlot())
		return gDLL->UI().getMouseOverPlot();
	updateNukeAreaOfEffect(); // advc.653
	return NULL;
}


ColorTypes CvGame::getPlotHighlightColor(CvPlot* pPlot) const
{
	if (pPlot == NULL)
		return NO_COLOR;
	ColorTypes const eDefaultColor = GC.getColorType("GREEN");
	if (gDLL->GetWorldBuilderMode())
		return eDefaultColor;
	ColorTypes const eNegativeColor = GC.getColorType("DARK_GREY");

	switch (gDLL->UI().getInterfaceMode())
	{
	case INTERFACEMODE_PING:
	case INTERFACEMODE_SIGN:
		if (!pPlot->isRevealed(getActiveTeam(), true))
			return NO_COLOR;
		return eDefaultColor;
	case INTERFACEMODE_PYTHON_PICK_PLOT:
		if (!pPlot->isRevealed(getActiveTeam(), true) ||
			!GC.getPythonCaller()->canPickRevealedPlot(*pPlot))
		{
			return NO_COLOR;
		}
		return eDefaultColor;
	case INTERFACEMODE_SAVE_PLOT_NIFS:
		return eNegativeColor;
	}
	bool bCanDoMode = gDLL->UI().getSelectionList()->
			canDoInterfaceModeAt(gDLL->UI().getInterfaceMode(), pPlot);
	// <advc.653>
	if (updateNukeAreaOfEffect(bCanDoMode ? pPlot : NULL))
		return NO_COLOR; // </advc.653>
	if (bCanDoMode)
		return eDefaultColor;
	return eNegativeColor;
}

// advc.653: (Returns true if plots have been colored)
bool CvGame::updateNukeAreaOfEffect(CvPlot const* pCenter) const
{
	CvUnit const* pNuke = gDLL->UI().getHeadSelectedUnit();
	if (pNuke == NULL || !pNuke->isNuke())
		return false;
	gDLL->getEngineIFace()->clearAreaBorderPlots(AREA_BORDER_LAYER_NUKE);
	if (pCenter == NULL || gDLL->UI().getInterfaceMode() != INTERFACEMODE_NUKE)
		return false;
	if (!pNuke->canNukeAt(pNuke->getPlot(), pCenter->getX(), pCenter->getY(),
		pNuke->getTeam()))
	{
		return false;
	}
	NiColorA const& kColor = GC.getInfo(GC.getColorType("YELLOW")).getColor();
	for (SquareIter itPlot(*pCenter, pNuke->nukeRange()); itPlot.hasNext(); ++itPlot)
	{
		gDLL->getEngineIFace()->fillAreaBorderPlot(itPlot->getX(), itPlot->getY(),
				kColor, AREA_BORDER_LAYER_NUKE);
	}
	return true;
}

// advc.004k:
void CvGame::updateSeaPatrolColors(CvUnit const& kSelectedUnit)
{
	gDLL->getEngineIFace()->clearAreaBorderPlots(AREA_BORDER_LAYER_PATROLLED);
	if (!kSelectedUnit.isSeaPatrolling())
		return;
	for (SquareIter itPlot(kSelectedUnit, GC.getMAX_SEA_PATROL_RANGE(), false);
		itPlot.hasNext(); ++itPlot)
	{
		if (kSelectedUnit.canReachBySeaPatrol(*itPlot))
		{
			gDLL->getEngineIFace()->fillAreaBorderPlot(itPlot->getX(), itPlot->getY(),
					GC.getInfo((ColorTypes)GC.getInfoTypeForString("COLOR_CITY_BLUE")).
					getColor(), AREA_BORDER_LAYER_PATROLLED);
		}
	}
}

void CvGame::loadBuildQueue(const CvString& strItem) const
{
	// advc.003w: The first two loops were needlessly complicated
	CvCivilization const& kCiv = *getActiveCivilization();
	for (int i = 0; i < kCiv.getNumUnits(); i++)
	{
		UnitTypes eUnit = kCiv.unitAt(i);
		if (GC.getInfo(eUnit).getType() == strItem)
		{
			selectedCitiesGameNetMessage(GAMEMESSAGE_PUSH_ORDER, ORDER_TRAIN,
					eUnit, -1, false, false, true);
			return;
		}
	}
	for (int i = 0; i < kCiv.getNumBuildings(); i++)
	{
		BuildingTypes eBuilding = kCiv.buildingAt(i);
		if (GC.getInfo(eBuilding).getType() == strItem)
		{
			selectedCitiesGameNetMessage(GAMEMESSAGE_PUSH_ORDER, ORDER_CONSTRUCT,
					eBuilding, -1, false, false, true);
			return;
		}
	}
	FOR_EACH_ENUM(Project)
	{
		if (strItem == GC.getInfo(eLoopProject).getType())
		{
			selectedCitiesGameNetMessage(GAMEMESSAGE_PUSH_ORDER, ORDER_CREATE,
					eLoopProject, -1, false, false, true);
			return;
		}
	}

	FOR_EACH_ENUM(Process)
	{
		if (strItem == GC.getInfo(eLoopProcess).getType())
		{
			selectedCitiesGameNetMessage(GAMEMESSAGE_PUSH_ORDER, ORDER_MAINTAIN,
					eLoopProcess, -1, false, false, true);
			return;
		}
	}
}


void CvGame::cheatSpaceship() const
{	// <advc.007b> I don't know how this is triggered; it's safer to block it.
	if (!isDebugMode())
		return; // </advc.007b>
	//add one space project that is still available
	CvTeam& kTeam = GET_TEAM(getActiveTeam());
	FOR_EACH_ENUM2(Project, eProject)
	{
		CvProjectInfo const& kProject = GC.getInfo(eProject);
		if (kProject.isSpaceship())
		{
			//cheat required projects
			FOR_EACH_ENUM2(Project, eReqProject)
			{
				int iNumReqProjects = kProject.getProjectsNeeded(eReqProject);
				while (kTeam.getProjectCount(eReqProject) < iNumReqProjects)
				{
					kTeam.changeProjectCount(eReqProject, 1);
				}
			}

			//cheat required techs
			TechTypes eRequiredTech = kProject.getTechPrereq();
			if (!kTeam.isHasTech(eRequiredTech))
				kTeam.setHasTech(eRequiredTech, true, getActivePlayer(), true, true);

			//cheat one space component
			if (kTeam.getProjectCount(eProject) < kProject.getMaxTeamInstances())
			{
				kTeam.changeProjectCount(eProject, 1);
				CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_PYTHON_SCREEN, eProject);
				pInfo->setText(L"showSpaceShip");
				gDLL->UI().addPopup(pInfo, getActivePlayer());
			}
		}
	}
}


DomainTypes CvGame::getUnitDomain(UnitTypes eUnit) const
{
	return GC.getInfo(eUnit).getDomainType();
}


CvArtInfoBuilding const* CvGame::getBuildingArtInfo(BuildingTypes eBuilding) const
{
	return GC.getInfo(eBuilding).getArtInfo();
}


bool CvGame::isWaterBuilding(BuildingTypes eBuilding) const
{
	return GC.getInfo(eBuilding).isWater();
}


CivilopediaWidgetShowTypes CvGame::getWidgetShow(BonusTypes eBonus) const
{
	/*	Don't show the widget if it's an abstract bonus that
		doesn't have any terrain (or art) associated with it.
		Hit singles, movies, musicals, in our case */
	bool bShowWidget = false;
	FOR_EACH_ENUM(Terrain)
	{
		if (GC.getInfo(eBonus).isTerrain(eLoopTerrain))
		{
			bShowWidget = true;
			break;
		}
	}
	if (!bShowWidget)
	{
		FOR_EACH_ENUM(Feature)
		{
			if (GC.getInfo(eBonus).isFeature(eLoopFeature))
			{
				bShowWidget = true;
				break;
			}
		}
	}
	if (!bShowWidget)
		return CIVILOPEDIA_WIDGET_SHOW_NONE;
	CivilopediaWidgetShowTypes eType = CIVILOPEDIA_WIDGET_SHOW_LAND;
	FOR_EACH_ENUM(Terrain)
	{
		if (GC.getInfo(eLoopTerrain).isWater())
		{
			if (GC.getInfo(eBonus).isTerrain(eLoopTerrain))
				eType = CIVILOPEDIA_WIDGET_SHOW_WATER;
		}
	}

	return eType;
}


CivilopediaWidgetShowTypes CvGame::getWidgetShow(ImprovementTypes eImprovement) const
{
	CivilopediaWidgetShowTypes eType = CIVILOPEDIA_WIDGET_SHOW_LAND;
	if (GC.getInfo(eImprovement).isWater())
		eType = CIVILOPEDIA_WIDGET_SHOW_WATER;
	return eType;
}

// (advc: getSpaceVictory implementation moved to CvGame.cpp)

// advc (note): Alt+Z causes the EXE to call this function
void CvGame::nextActivePlayer(bool bForward)
{
	int iNewPlayer = getActivePlayer();
	for (int i = 1; i < MAX_PLAYERS; i++)
	{
		if (bForward)
			iNewPlayer += 1;
		else iNewPlayer += MAX_PLAYERS - 1;
		iNewPlayer %= MAX_PLAYERS;

		PlayerTypes eNewPlayer = (PlayerTypes)iNewPlayer;
		if (GET_PLAYER(eNewPlayer).isAlive() && !GET_PLAYER(eNewPlayer).isBarbarian())
		{
			// advc.210: Merged into BBAI function, which also takes care of alerts.
			changeHumanPlayer(eNewPlayer);
			break;
		}
	}
}


int CvGame::getNextSoundtrack(EraTypes eLastEra, int iLastSoundtrack) const
{
	EraTypes eCurEra = GET_PLAYER(getActivePlayer()).getSoundtrackEra(); // doc: dynamic soundtracks
	CvEraInfo const& kCurrentEra = GC.getInfo(eCurEra);
	if (kCurrentEra.getNumSoundtracks() == 0)
		return -1;
	if (kCurrentEra.getNumSoundtracks() == 1 ||
		(eLastEra != eCurEra && kCurrentEra.isFirstSoundtrackFirst()))
	{
		return kCurrentEra.getSoundtracks(0);
	}
	//return kCurrentEra.getSoundtracks(GC.getASyncRand().get(kCurrentEra.getNumSoundtracks(), "Pick Song ASYNC"));
	/*	<advc.002o> Perhaps was meant to be implemented this way? Why else handle
		kCurrentEra.getNumSoundtracks()==1 upfront? (Not to mention the unused param.) */
	std::vector<int> aiTracks;
	for (int i = 0; i < kCurrentEra.getNumSoundtracks(); i++)
	{
		int iTrack = kCurrentEra.getSoundtracks(i);
		if (iTrack != iLastSoundtrack)
			aiTracks.push_back(iTrack);
	}
	if (aiTracks.empty())
		aiTracks.push_back(iLastSoundtrack);
	return aiTracks[GC.getASyncRand().get(
			aiTracks.size(), "Pick Song ASYNC")]; // </advc.002o>
}


int CvGame::getSoundtrackSpace() const
{
	return std::max(1, GC.getEraInfo(GET_PLAYER(getActivePlayer()).getSoundtrackEra()).getSoundtrackSpace()); // doc: dynamic soundtrack
}


bool CvGame::isSoundtrackOverride(CvString& strSoundtrack) const
{
	if (GC.getDefineINT("VICTORY_SOUNDTRACK_AVAILABLE") != 0)
	{
		if (getGameState() == GAMESTATE_EXTENDED || getGameState() == GAMESTATE_OVER)
		{
			if (getWinner() == getActiveTeam())
				strSoundtrack = "AS2D_VICTORY";
			else strSoundtrack = "AS2D_DEFEAT";
			return true;
		}
	}
	return false;
}


void CvGame::initSelection() const
{
	bool bSelected = false;
	CvPlayer& kActivePlayer = GET_PLAYER(getActivePlayer());
	// <advc.153> Replacing two non-nested loops
	enum PassTypes
	{
		FIGHT_AND_ALL_READY,
		ALL_READY,
		// New passes:
		FIGHT_AND_ANY_READY,
		ANY_READY,
		NUM_PASSES
	};
	for (int iPass = 0; iPass < NUM_PASSES &&
		!bSelected; iPass++)
	{
		PassTypes const ePass = (PassTypes)iPass;
		FOR_EACH_UNIT_VAR(pLoopUnit, kActivePlayer)
		{
			if ((ePass == FIGHT_AND_ALL_READY || ePass == FIGHT_AND_ANY_READY) &&
				!pLoopUnit->canFight())
			{
				continue;
			}
			if ((ePass == FIGHT_AND_ALL_READY || ePass == ALL_READY) &&
				!pLoopUnit->getGroup()->readyToSelect())
			{
				continue;
			}
			if ((ePass == FIGHT_AND_ANY_READY || ePass == ANY_READY) &&
				!pLoopUnit->getGroup()->readyToSelect(true))
			{
				continue;
			}
			selectUnit(pLoopUnit, true);
			bSelected = true;
			break;
		}
	} // </advc.153>
	if (!bSelected)
	{
		FOR_EACH_UNIT_VAR(pLoopUnit, kActivePlayer)
		{
			gDLL->UI().centerCamera(pLoopUnit);
			break;
		}
	}
}


bool CvGame::canDoPing(CvPlot* pPlot, PlayerTypes ePlayer) const
{
	if (pPlot == NULL || !pPlot->isRevealed(getActiveTeam()))
		return false;
	if (TEAMID(ePlayer) != getActiveTeam())
		return false;
	return true;
}


bool CvGame::shouldDisplayReturn() const
{
	return gDLL->UI().isCitySelection();
}


bool CvGame::shouldDisplayEndTurn() const
{
	return (!gDLL->UI().isCitySelection() &&
			GET_PLAYER(getActivePlayer()).isTurnActive());
}


bool CvGame::shouldDisplayWaitingOthers() const
{	// <advc.706>
	if (!GET_PLAYER(getActivePlayer()).isHuman())
		return false; // </advc.706>
	if (!gDLL->UI().isCitySelection())
	{
		if (!GET_PLAYER(getActivePlayer()).isTurnActive())
			return true;

		if (gDLL->UI().isInAdvancedStart() &&
			GET_PLAYER(getActivePlayer()).getAdvancedStartPoints() < 0)
		{
			return true;
		}
	}
	return false;
}


bool CvGame::shouldDisplayWaitingYou() const
{
	if (!gDLL->UI().isCitySelection() &&
		GET_PLAYER(getActivePlayer()).isTurnActive() &&
		isNetworkMultiPlayer())
	{
		if (isMPOption(MPOPTION_SIMULTANEOUS_TURNS) &&
			countNumHumanGameTurnActive() == 1)
		{
			return true;
		}
		if (isSimultaneousTeamTurns() &&
			GET_TEAM(getActiveTeam()).countNumHumanGameTurnActive() == 1 &&
			GET_TEAM(getActiveTeam()).getAliveCount() > 1)
		{
			return true;
		}
	}
	return false;
}


bool CvGame::shouldDisplayEndTurnButton() const
{
	return
		(!gDLL->UI().isCitySelection() &&
		!gDLL->GetWorldBuilderMode() &&
		GET_PLAYER(getActivePlayer()).isTurnActive());
}


bool CvGame::shouldDisplayFlag() const
{
	return
		!(gDLL->UI().isCitySelection() ||
		gDLL->UI().getHeadSelectedCity() != NULL ||
		gDLL->isDiplomacy() ||
		gDLL->isMPDiplomacyScreenUp() ||
		gDLL->GetWorldBuilderMode());
}


bool CvGame::shouldDisplayUnitModel() const
{
	if (gDLL->isDiplomacy() ||
		gDLL->isMPDiplomacyScreenUp() ||
		gDLL->GetWorldBuilderMode())
	{
		return false;
	}

	if (gDLL->UI().getHeadSelectedUnit() != NULL ||
		//gDLL->UI().isCityScreenUp()
		gDLL->UI().getHeadSelectedCity() != NULL) // advc.001
	{
		return true;
	}

	return false;
}


bool CvGame::shouldShowResearchButtons() const
{
	if (!gDLL->GetWorldBuilderMode())
	{
		CvPlayer const& kActivePlayer = GET_PLAYER(getActivePlayer()); // advc
		if (kActivePlayer.isAlive() && !gDLL->UI().isCityScreenUp())
		{
			if (kActivePlayer.isResearch() && // advc.004x
				kActivePlayer.getCurrentResearch() == NO_TECH)
			{
				return true;
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
	/*if ((isNetworkMultiPlayer() &&
		(isMPOption(MPOPTION_SIMULTANEOUS_TURNS) && countNumHumanGameTurnActive() == 1 ||
		(!isSimultaneousTeamTurns() && GET_TEAM(getActiveTeam()).countNumHumanGameTurnActive() == 1 &&
		GET_TEAM(getActiveTeam()).getAliveCount() > 1))))*/ // BtS
	/*	K-Mod. Don't use GET_TEAM in pitboss mode.
		(and note, I've fixed a typo in the parentheses.) */
	if (isNetworkMultiPlayer() && getActiveTeam() != NO_TEAM &&
		((isMPOption(MPOPTION_SIMULTANEOUS_TURNS) &&
		  countNumHumanGameTurnActive() == 1) ||
		(!isSimultaneousTeamTurns() &&
		  GET_TEAM(getActiveTeam()).countNumHumanGameTurnActive() == 1 &&
		  GET_TEAM(getActiveTeam()).getAliveCount() > 1)))
	// K-Mod end
	{
		return END_TURN_OVER_HIGHLIGHT;
	}
	return END_TURN_GO;
}

// advc.095:
void CvGame::setCityBarWidth(bool bWide)
{
	if (ARTFILEMGR.isCityBarPathsSwapped() == bWide)
		return;
	ARTFILEMGR.swapCityBarPaths();
	for (PlayerIter<ALIVE> itPlayer; itPlayer.hasNext(); ++itPlayer)
	{
		FOR_EACH_CITY_VAR(pCity, *itPlayer)
			pCity->reloadEntity();
	}
}


void CvGame::handleCityScreenPlotPicked(CvCity* pCity, CvPlot* pPlot,
	bool bAlt, bool bShift, bool bCtrl) const
{
	if (pCity == NULL || pPlot == NULL)
	{
		FAssert(false); // advc (BtS had only asserted pPlot)
		return;
	}
	int iIndex = pCity->getCityPlotIndex(*pPlot);
	if (pPlot->getOwner() == getActivePlayer() &&
		pCity->getOwner() == getActivePlayer() && iIndex != NO_CITYPLOT)
	{
		CvMessageControl::getInstance().sendDoTask(pCity->getID(),
				TASK_CHANGE_WORKING_PLOT, iIndex, -1, false, bAlt, bShift, bCtrl);
	}
	else //if (GC.getDefineINT("CITY_SCREEN_CLICK_WILL_EXIT"))
	if (BUGOption::isEnabled("CityScreen__ClickMapToExit", true)) // advc.004t
		gDLL->UI().clearSelectedCities();
}


void CvGame::handleCityScreenPlotDoublePicked(CvCity* pCity, CvPlot* pPlot,
	bool bAlt, bool bShift, bool bCtrl) const
{
	if (pCity != NULL && pCity->plot() == pPlot)
	{
		/*	<advc.004t> Exit upon double click outside the radius, not upon
			double click on the city center. */
		/*gDLL->UI().clearSelectedCities()*/;
	}
	else if (pPlot != NULL && pCity->getCityPlotIndex(*pPlot) == NO_CITYPLOT)
		gDLL->UI().clearSelectedCities(); // </advc.004t>
}


void CvGame::handleCityScreenPlotRightPicked(CvCity* pCity, CvPlot* pPlot,
	bool bAlt, bool bShift, bool bCtrl) const
{
	if (pCity == NULL || pPlot == NULL)
	{
		FAssert(false); // advc: As in handleCityScreenPlotPicked
		return;
	}
	/*  <advc.004t> Can't assign a working city to the city plot, so use this
		for exiting the screen. */
	if (pCity->plot() == pPlot)
	{
		CvPlot const* pCityPlot = (gDLL->UI().isCityScreenUp() ?
				gDLL->UI().getHeadSelectedCity()->plot() : NULL);
		gDLL->UI().clearSelectedCities();
		if (pCityPlot != NULL)
			gDLL->UI().lookAt(pCityPlot->getPoint(), CAMERALOOKAT_NORMAL);
		return;
	} // </advc.004t>
	if (pCity->getOwner() == getActivePlayer() &&
		pPlot->getOwner() == getActivePlayer() &&
		pCity->getCityPlotIndex(*pPlot) != -1)
	{
		CvMessageControl::getInstance().sendDoTask(pCity->getID(),
				TASK_CLEAR_WORKING_OVERRIDE, pCity->getCityPlotIndex(*pPlot),
				-1, false, bAlt, bShift, bCtrl);
	}
}


void CvGame::handleCityPlotRightPicked(CvCity* pCity, CvPlot* pPlot,
	bool bAlt, bool bShift, bool bCtrl) const
{
	if (pPlot == NULL)
		return;
	if (pCity != NULL && gDLL->UI().isCitySelected(pCity))
		selectedCitiesGameNetMessage(GAMEMESSAGE_DO_TASK, TASK_CLEAR_RALLY_PLOT);
	else
	{
		if (bShift)
		{
			selectedCitiesGameNetMessage(GAMEMESSAGE_DO_TASK, TASK_RALLY_PLOT,
					pPlot->getX(), pPlot->getY());
		}
		else gDLL->UI().clearSelectedCities();
	}
}


void CvGame::handleMiddleMouse(bool bCtrl, bool bAlt, bool bShift)
{
	if (gDLL->UI().isCitySelection())
		gDLL->UI().clearSelectedCities();
	else
	{
		if (bAlt)
			doControl(CONTROL_SELECTYUNITALL);
		else if (bCtrl)
			doControl(CONTROL_SELECTYUNITTYPE);
		else doControl(CONTROL_CENTERONSELECTION);
	}
}


void CvGame::handleDiplomacySetAIComment(DiploCommentTypes eComment) const
{
	PlayerTypes eOtherPlayer = (PlayerTypes) gDLL->getDiplomacyPlayer();
	FAssert(eOtherPlayer != NO_PLAYER);
	if (GC.getAIDiploCommentType("ACCEPT_ASK") == eComment ||
		GC.getAIDiploCommentType("ACCEPT_DEMAND") == eComment)
	{
		if (!GET_TEAM(getActiveTeam()).isAVassal() && !GET_TEAM(eOtherPlayer).isAVassal())
		{
			CLinkList<TradeData> playerList;
			CLinkList<TradeData> loopPlayerList;
			TradeData peaceTreaty(TRADE_PEACE_TREATY);
			playerList.insertAtEnd(peaceTreaty);
			loopPlayerList.insertAtEnd(peaceTreaty);
			gDLL->sendImplementDealMessage(eOtherPlayer, &playerList, &loopPlayerList);
		}
	}
	// advc.072:
	m_bShowingCurrentDeals = (eComment == GC.getAIDiploCommentType("CURRENT_DEALS"));
}

// <advc.004x>
void CvGame::setDawnOfManShown(bool b)
{
	m_bDoMShown = b;
}


bool CvGame::isAboutToShowDawnOfMan() const
{
	return (!m_bDoMShown && getElapsedGameTurns() <= 0);
} // </advc.004x>

/*	<advc.061> Could get this through winuser.h, but that's not trivial.
	Let's just let Python provide the info to us. */
void CvGame::setScreenDimensions(int iWidth, int iHeight)
{
	if (m_iScreenWidth == iWidth && m_iScreenHeight == iHeight)
		return;
	m_iScreenWidth = iWidth;
	m_iScreenHeight = iHeight;
	// advc.001: Avoid warped plot indicators upon changing resolution
	gDLL->UI().setDirty(GlobeLayer_DIRTY_BIT, true);
	CvGlobals::getInstance().updateCityCamDist(); // advc.004m
	/*	<advc.092b> Do this as soon as we know the screen dimensions, before
		a plot indicator gets created for the initially selected units. */
	if (m_iScreenHeight > 0)
		smc::BtS_EXE.patchPlotIndicatorSize(); // </advc.092b>
}

int CvGame::getScreenWidth() const
{
	return m_iScreenWidth;
}

int CvGame::getScreenHeight() const
{
	return m_iScreenHeight;
} // </advc.061>

// advc.004n:
void CvGame::onCityScreenChange()
{
	changePlotListShift(-getPlotListShift());
	/*	To fix a BtS issue with the bottom rows of the plot list
		being empty after having shifted the plot list on the city screen.
		(Looks like the EXE ensures a nonnegative column value. Could probably
		get the current value via Python for a more proper reset.) */
	gDLL->UI().changePlotListColumn(-100000);
	/*	<advc.092> Move the camera north a bit b/c that'll center the
		map excerpt on the city screen better. */
	if (m_bCityScreenUp)
	{
		CvPlot const* pCityPlot = gDLL->UI().getSelectionPlot();
		if (pCityPlot != NULL)
		{
			CvPlot const* pOneNorth = GC.getMap().plotDirection(
					pCityPlot->getX(), pCityPlot->getY(), DIRECTION_NORTH);
			if (pOneNorth != NULL)
			{
				NiPoint3 nOneNorth = pOneNorth->getPoint();
				NiPoint3 nCity = pCityPlot->getPoint();
				float const fDisplWeight = 0.23f +
						(BUGOption::isEnabled("MainInterface__EnlargeHUD", true) ?
						0.03f : 0);
				NiPoint3 nLookAt(nCity.x,
						nCity.y + fDisplWeight * (nOneNorth.y - nCity.y), nCity.z);
				gDLL->UI().lookAt(nLookAt, CAMERALOOKAT_CITY_ZOOM_IN);
			}
		}
	} // </advc.092>
}
