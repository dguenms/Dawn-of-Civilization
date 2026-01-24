#include "CvGameCoreDLL.h"
#include "CvGameTextMgr.h"
#include "CoreAI.h"
#include "CvUnitAI.h"
#include "CvSelectionGroupAI.h"
#include "CombatOdds.h"
#include "TeamPathFinder.h" // advc.104b
#include "CvCityAI.h"
#include "CitySiteEvaluator.h"
#include "CvDeal.h"
#include "CvPlotGroup.h"
#include "CvInfo_All.h"
#include "CvXMLLoadUtility.h"
#include "PlotRange.h"
#include "CvArea.h"
#include "RiseFall.h" // advc.700
#include "CvBugOptions.h"
#include "CvPopupInfo.h"
#include "CvDLLSymbolIFaceBase.h"


static char* szErrorMsg; // for displaying assertion and error messages

// advc:
namespace
{
	__inline PlayerTypes getActivePlayer()
	{
		return GC.getGame().getActivePlayer();
	}
	__inline TeamTypes getActiveTeam()
	{
		return GC.getGame().getActiveTeam();
	}
}


void CvGameTextMgr::DeInitialize()
{
	for (size_t i = 0 ; i < m_apbPromotion.size(); i++)
		delete[] m_apbPromotion[i];
}


void CvGameTextMgr::Reset()
{
	/*  Access CvXMLLoadUtility to clean global text memory and reload
		the XML files */
	CvXMLLoadUtility pXML;
	pXML.LoadGlobalText();
}


int CvGameTextMgr::getCurrentLanguage()
{
	return gDLL->getCurrentLanguage();
}


void CvGameTextMgr::setYearStr(CvWString& szString, int iGameTurn, bool bSave,
	CalendarTypes eCalendar, int iStartYear, GameSpeedTypes eSpeed)
{
	int iTurnYear = getTurnYearForGame(iGameTurn, iStartYear, eCalendar, eSpeed);
	// <advc.002k>
	enum NotationTypes { AD_PREFIX, AD_POSTFIX, COMMON_ERA };
	NotationTypes eNotation = (NotationTypes)BUGOption::getValue(
			"NJAGC__YearNotation", 0, false);
	// </advc.002k>
	if (iTurnYear < 0)
	{
		if (bSave)
		{
			szString = gDLL->getText( // <advc.002k>
					eNotation == COMMON_ERA ?
					"TXT_KEY_TIME_BCE_SAVE" : // </advc.002k>
					"TXT_KEY_TIME_BC_SAVE",
					CvWString::format(L"%04d", -iTurnYear).GetCString());
		}
		else
		{
			szString = gDLL->getText( // <advc.002k>
					eNotation == COMMON_ERA ?
					"TXT_KEY_TIME_BCE" : // </advc.002k>
					"TXT_KEY_TIME_BC", -iTurnYear);
		}
	}
	else // advc.002k: Melded the if(iTurnYear > 0)...else branches
	{
		if (bSave)
		{
			szString = gDLL->getText(
					eNotation == COMMON_ERA ? "TXT_KEY_TIME_CE_SAVE" : // advc.002k
					"TXT_KEY_TIME_AD_SAVE",
					iTurnYear > 0 ?
					CvWString::format(L"%04d", iTurnYear).GetCString() :
					L"0001");
		}
		else
		{	// <advc.002k>
			CvWString szTag;
			switch(eNotation)
			{
			case AD_POSTFIX: szTag = "TXT_KEY_TIME_AD"; break;
			case COMMON_ERA: szTag = "TXT_KEY_TIME_CE"; break;
			default: szTag = "TXT_KEY_AD_TIME"; break;
			} // </advc.002k>
			szString = gDLL->getText(szTag, std::max(1, iTurnYear));
		}
	}
}


void CvGameTextMgr::setDateStr(CvWString& szString, int iGameTurn, bool bSave, CalendarTypes eCalendar, int iStartYear, GameSpeedTypes eSpeed)
{
	CvWString szYearBuffer;
	CvWString szWeekBuffer;

	setYearStr(szYearBuffer, iGameTurn, bSave, eCalendar, iStartYear, eSpeed);

	switch (eCalendar)
	{
	case CALENDAR_DEFAULT:
		if (0 == (getTurnMonthForGame(iGameTurn + 1, iStartYear, eCalendar, eSpeed) - getTurnMonthForGame(iGameTurn, iStartYear, eCalendar, eSpeed)) % GC.getNumMonthInfos())
		{
			szString = szYearBuffer;
		}
		else
		{
			int iMonth = getTurnMonthForGame(iGameTurn, iStartYear, eCalendar, eSpeed);
			if (bSave)
			{
				szString = (szYearBuffer + "-" + GC.getInfo((MonthTypes)(iMonth % GC.getNumMonthInfos())).getDescription());
			}
			else
			{
				szString = (GC.getInfo((MonthTypes)(iMonth % GC.getNumMonthInfos())).getDescription() + CvString(", ") + szYearBuffer);
			}
		}
		break;
	case CALENDAR_YEARS:
	case CALENDAR_BI_YEARLY:
		szString = szYearBuffer;
		break;

	case CALENDAR_TURNS:
		szString = gDLL->getText("TXT_KEY_TIME_TURN", (iGameTurn + 1));
		break;

	case CALENDAR_SEASONS:
		if (bSave)
		{
			szString = (szYearBuffer + "-" + GC.getInfo((SeasonTypes)(iGameTurn % GC.getNumSeasonInfos())).getDescription());
		}
		else
		{
			szString = (GC.getInfo((SeasonTypes)(iGameTurn % GC.getNumSeasonInfos())).getDescription() + CvString(", ") + szYearBuffer);
		}
		break;

	case CALENDAR_MONTHS:
		if (bSave)
		{
			szString = (szYearBuffer + "-" + GC.getInfo((MonthTypes)(iGameTurn % GC.getNumMonthInfos())).getDescription());
		}
		else
		{
			szString = (GC.getInfo((MonthTypes)(iGameTurn % GC.getNumMonthInfos())).getDescription() + CvString(", ") + szYearBuffer);
		}
		break;

	case CALENDAR_WEEKS:
		szWeekBuffer = gDLL->getText("TXT_KEY_TIME_WEEK", ((iGameTurn % GC.getDefineINT("WEEKS_PER_MONTHS")) + 1));

		if (bSave)
		{
			szString = (szYearBuffer + "-" + GC.getInfo((MonthTypes)((iGameTurn / GC.getDefineINT("WEEKS_PER_MONTHS")) % GC.getNumMonthInfos())).getDescription() + "-" + szWeekBuffer);
		}
		else
		{
			szString = (szWeekBuffer + ", " + GC.getInfo((MonthTypes)((iGameTurn / GC.getDefineINT("WEEKS_PER_MONTHS")) % GC.getNumMonthInfos())).getDescription() + ", " + szYearBuffer);
		}
		break;

	default:
		FAssert(false);
	}
}


// rfc
// TODO: refactor
void CvGameTextMgr::setDateStrPlayer(CvWString& szString, int iGameTurn, bool bSave, CalendarTypes eCalendar, int iStartYear, GameSpeedTypes eSpeed, PlayerTypes ePlayer)
{
	if (GET_TEAM(GET_PLAYER(ePlayer).getTeam()).isHasTech((TechTypes)CALENDAR) || GC.getGameINLINE().getAIAutoPlay() > 0 || GC.getGameINLINE().isDebugMode())
		setDateStr(szString, iGameTurn, bSave, eCalendar, iStartYear, eSpeed);
	else if (GET_PLAYER(ePlayer).getCurrentEra() >= ERA_RENAISSANCE)
		szString = gDLL->getText("TXT_KEY_AGE_RENAISSANCE");
	else if (GET_PLAYER(ePlayer).getCurrentEra() == ERA_MEDIEVAL)
		szString = gDLL->getText("TXT_KEY_AGE_MEDIEVAL");
	else if (GET_TEAM(GET_PLAYER(ePlayer).getTeam()).isHasTech((TechTypes)BLOOMERY))
		szString = gDLL->getText("TXT_KEY_AGE_IRON");
	else if (GET_TEAM(GET_PLAYER(ePlayer).getTeam()).isHasTech((TechTypes)ALLOYS))
		szString = gDLL->getText("TXT_KEY_AGE_BRONZE");
	else szString = gDLL->getText("TXT_KEY_AGE_STONE");
	if (bSave)
		szString = szString + " " + gDLL->getText("TXT_KEY_SAVEGAME_TURN", (iGameTurn));
		/*if (gDLL->getCurrentLanguage() == 0)
				szString = szString + " " + gDLL->getText("TXT_KEY_SAVEGAME_TURN", (iGameTurn));
		else
				szString = gDLL->getText("TXT_KEY_SAVEGAME_TURN", (iGameTurn));*/
}


void CvGameTextMgr::setTimeStr(CvWString& szString, int iGameTurn, bool bSave)
{
	setDateStrPlayer(szString, iGameTurn, bSave, GC.getGameINLINE().getCalendar(), GC.getGameINLINE().getStartYear(), GC.getGameINLINE().getGameSpeedType(), GC.getGameINLINE().getActivePlayer()); // rfc
}


void CvGameTextMgr::setInterfaceTime(CvWString& szString, PlayerTypes ePlayer)
{
	CvWString szTempBuffer;

	if (GET_PLAYER(ePlayer).isGoldenAge())
	{
		szString.Format(L"%c(%d) ", gDLL->getSymbolID(GOLDEN_AGE_CHAR), GET_PLAYER(ePlayer).getGoldenAgeTurns());
	}
	else
	{
		szString.clear();
	}

	setDateStrPlayer(szTempBuffer, GC.getGameINLINE().getGameTurn(), false, GC.getGameINLINE().getCalendar(), GC.getGameINLINE().getStartYear(), GC.getGameINLINE().getGameSpeedType(), ePlayer); // rfc
	szString += CvWString(szTempBuffer);
}


void CvGameTextMgr::setGoldStr(CvWString& szString, PlayerTypes ePlayer)
{
	if (GET_PLAYER(ePlayer).getGold() < 0)
	{
		szString.Format(L"%c: " SETCOLR L"%d" SETCOLR, GC.getInfo(COMMERCE_GOLD).getChar(), TEXT_COLOR("COLOR_NEGATIVE_TEXT"), GET_PLAYER(ePlayer).getGold());
	}
	else
	{
		szString.Format(L"%c: %d", GC.getInfo(COMMERCE_GOLD).getChar(), GET_PLAYER(ePlayer).getGold());
	}

	int iGoldRate = GET_PLAYER(ePlayer).calculateGoldRate();
	if (iGoldRate < 0)
	{
		szString += gDLL->getText("TXT_KEY_MISC_NEG_GOLD_PER_TURN", iGoldRate);
	}
	else if (iGoldRate > 0)
	{
		szString += gDLL->getText("TXT_KEY_MISC_POS_GOLD_PER_TURN", iGoldRate);
	}

	if (GET_PLAYER(ePlayer).isStrike())
	{
		szString += gDLL->getText("TXT_KEY_MISC_STRIKE");
	}
}


void CvGameTextMgr::setResearchStr(CvWString& szString, PlayerTypes ePlayer)
{
	CvPlayer const& kPlayer = GET_PLAYER(ePlayer); // advc
	szString = gDLL->getText("TXT_KEY_MISC_RESEARCH_STRING",
			GC.getInfo(kPlayer.getCurrentResearch()).getTextKeyWide());
	CvWString szTempBuffer;
	if (GET_TEAM(ePlayer).getTechCount(GET_PLAYER(ePlayer).getCurrentResearch()) > 0)
	{
		szTempBuffer.Format(L" %d", GET_TEAM(ePlayer).getTechCount(kPlayer.
				getCurrentResearch()) + 1);
		szString += szTempBuffer;
	} // <advc.004x>
	int iTurnsLeft = kPlayer.getResearchTurnsLeft(kPlayer.getCurrentResearch(), true);
	if(iTurnsLeft >= 0) // </advc.004x>
		szTempBuffer.Format(L" (%d)", iTurnsLeft);
	szString += szTempBuffer;
}


void CvGameTextMgr::setOOSSeeds(CvWString& szString, PlayerTypes ePlayer)
{
	if (GET_PLAYER(ePlayer).isHuman())
	{
		int iNetID = GET_PLAYER(ePlayer).getNetID();
		if (gDLL->isConnected(iNetID))
		{
			szString = gDLL->getText("TXT_KEY_PLAYER_OOS", gDLL->GetSyncOOS(iNetID), gDLL->GetOptionsOOS(iNetID));
		}
	}
}

void CvGameTextMgr::setNetStats(CvWString& szString, PlayerTypes ePlayer)
{
	if (ePlayer == getActivePlayer() ||
		// advc.004v: Moved up
		!gDLL->UI().isNetStatsVisible())
	{
		return;
	}
	if (GET_PLAYER(ePlayer).isHuman())
	{
		int iNetID = GET_PLAYER(ePlayer).getNetID();
		if (gDLL->isConnected(iNetID))
			szString = gDLL->getText("TXT_KEY_MISC_NUM_MS", gDLL->GetLastPing(iNetID));
		else szString = gDLL->getText("TXT_KEY_MISC_DISCONNECTED");
	}
	else szString = gDLL->getText("TXT_KEY_MISC_AI");
}


void CvGameTextMgr::setMinimizePopupHelp(CvWString& szString, const CvPopupInfo & info)
{
	CvCity const* pCity;
	UnitTypes eTrainUnit;
	BuildingTypes eConstructBuilding;
	ProjectTypes eCreateProject;
	ReligionTypes eReligion;
	CivicTypes eCivic;

	switch (info.getButtonPopupType())
	{
	case BUTTONPOPUP_CHOOSEPRODUCTION:
		pCity = GET_PLAYER(getActivePlayer()).getCity(info.getData1());
		if (pCity != NULL)
		{
			eTrainUnit = NO_UNIT;
			eConstructBuilding = NO_BUILDING;
			eCreateProject = NO_PROJECT;

			switch (info.getData2())
			{
			case (ORDER_TRAIN):
				eTrainUnit = (UnitTypes)info.getData3();
				break;
			case (ORDER_CONSTRUCT):
				eConstructBuilding = (BuildingTypes)info.getData3();
				break;
			case (ORDER_CREATE):
				eCreateProject = (ProjectTypes)info.getData3();
				break;
			default:
				break;
			}

			if (eTrainUnit != NO_UNIT)
			{
				szString += gDLL->getText("TXT_KEY_MINIMIZED_CHOOSE_PRODUCTION_UNIT", GC.getInfo(eTrainUnit).getTextKeyWide(), pCity->getNameKey());
			}
			else if (eConstructBuilding != NO_BUILDING)
			{
				szString += gDLL->getText("TXT_KEY_MINIMIZED_CHOOSE_PRODUCTION_BUILDING", GC.getInfo(eConstructBuilding).getTextKeyWide(), pCity->getNameKey());
			}
			else if (eCreateProject != NO_PROJECT)
			{
				szString += gDLL->getText("TXT_KEY_MINIMIZED_CHOOSE_PRODUCTION_PROJECT", GC.getInfo(eCreateProject).getTextKeyWide(), pCity->getNameKey());
			}
			else
			{
				szString += gDLL->getText("TXT_KEY_MINIMIZED_CHOOSE_PRODUCTION", pCity->getNameKey());
			}
		}
		break;

	case BUTTONPOPUP_CHANGERELIGION:
		eReligion = ((ReligionTypes)(info.getData1()));
		if (eReligion != NO_RELIGION)
		{
			szString += gDLL->getText("TXT_KEY_MINIMIZED_CHANGE_RELIGION", GC.getInfo(eReligion).getTextKeyWide());
		}
		break;

	case BUTTONPOPUP_CHOOSETECH:
		if (info.getData1() > 0)
		{
			szString += gDLL->getText("TXT_KEY_MINIMIZED_CHOOSE_TECH_FREE");
		}
		else
		{
			szString += gDLL->getText("TXT_KEY_MINIMIZED_CHOOSE_TECH");
		}
		break;

	case BUTTONPOPUP_CHANGECIVIC:
		eCivic = ((CivicTypes)(info.getData2()));
		if (eCivic != NO_CIVIC)
		{
			szString += gDLL->getText("TXT_KEY_MINIMIZED_CHANGE_CIVIC", GC.getInfo(eCivic).getTextKeyWide());
		}
		break;
	}
}

// advc (note): This has been redundantly implemented in PLE.py (PLE.showUnitInfoPane)
void CvGameTextMgr::setEspionageMissionHelp(CvWStringBuffer &szBuffer, const CvUnit* pUnit)
{
	if (!pUnit->isSpy())
		return;
	PlayerTypes const eOwner =  pUnit->getPlot().getOwner();
	if (eOwner == NO_PLAYER || TEAMID(eOwner) == pUnit->getTeam())
		return;
	if (!pUnit->canEspionage(pUnit->plot()))
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_HELP_NO_ESPIONAGE"));

		if (pUnit->hasMoved() || pUnit->isMadeAttack())
		{
			szBuffer.append(gDLL->getText(
					"TXT_KEY_UNIT_HELP_NO_ESPIONAGE_REASON_MOVED"));
		}
		else if (!pUnit->isInvisible(GET_PLAYER(eOwner).getTeam(), false))
		{
			szBuffer.append(gDLL->getText(
					"TXT_KEY_UNIT_HELP_NO_ESPIONAGE_REASON_VISIBLE",
					GET_PLAYER(eOwner).getNameKey()));
		}
	}
	else if (pUnit->getFortifyTurns() > 0)
	{
		int iModifier = -pUnit->getFortifyTurns() *
				GC.getDefineINT("ESPIONAGE_EACH_TURN_UNIT_COST_DECREASE");
		if (iModifier != 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_COST", iModifier));
		}
	}
}


void CvGameTextMgr::setUnitHelp(CvWStringBuffer &szString, const CvUnit* pUnit,
	bool bOneLine, bool bShort,
	bool bColorAllegiance, // advc.048
	bool bOmitOwner, // advc.061
	bool bIndicator) // advc.007
{
	PROFILE_FUNC();

	CvGame const& kGame = GC.getGame(); // advc
	bool const bDebugMode = (kGame.isDebugMode() && !bIndicator); // advc.007
	bool const bShift = GC.shiftKey();
	bool const bAlt = GC.altKey();
	// <advc.007> Make info more compact in debug mode
	if (bDebugMode && bOneLine)
		bShort = true; // </advc.007>
	CvUnitInfo const& kInfo = pUnit->getUnitInfo(); // advc
	// <advc.048>
	char const* szColTag = "COLOR_UNIT_TEXT";
	if (bColorAllegiance)
	{
		szColTag = (//pUnit->isEnemy(getActiveTeam()) ?
				// For combat odds at peace (Alt hover)
				!pUnit->isActiveTeam() ?
				"COLOR_NEGATIVE_TEXT" : "COLOR_POSITIVE_TEXT");
	} // </advc.048>
	{
		CvWString szTempBuffer;
		szTempBuffer.Format(SETCOLR L"%s" ENDCOLR, TEXT_COLOR(
				szColTag), // advc.048
				pUnit->getName().GetCString());
		szString.append(szTempBuffer);
	}
	szString.append(L", ");

	if (pUnit->getDomainType() == DOMAIN_AIR)
	{
		if (pUnit->airBaseCombatStr() > 0)
		{
			CvWString szTempBuffer;
			if (pUnit->isFighting())
			{
				szTempBuffer.Format(L"?/%d%c", pUnit->airBaseCombatStr(),
						gDLL->getSymbolID(STRENGTH_CHAR));
			}
			else if (pUnit->isHurt())
				setHurtUnitStrength(szTempBuffer, *pUnit); // advc.004
			else
			{
				szTempBuffer.Format(L"%d%c", pUnit->airBaseCombatStr(),
						gDLL->getSymbolID(STRENGTH_CHAR));
			}
			szString.append(szTempBuffer);
			szString.append(L", "); // advc.004
		}
	}
	else
	{
		if (pUnit->canFight())
		{
			CvWString szTempBuffer;
			if (pUnit->isFighting())
			{
				szTempBuffer.Format(L"?/%d%c", pUnit->baseCombatStr(),
						gDLL->getSymbolID(STRENGTH_CHAR));
			}
			else if (pUnit->isHurt())
				setHurtUnitStrength(szTempBuffer, *pUnit); // advc.004
			else
			{
				szTempBuffer.Format(L"%d%c", pUnit->baseCombatStr(),
						gDLL->getSymbolID(STRENGTH_CHAR));
			}
			szString.append(szTempBuffer);
			szString.append(L", "); // advc.004
		}
	}
	int const iDenom = GC.getMOVE_DENOMINATOR(); // advc
	int const iCurrMoves = (pUnit->movesLeft() / iDenom) +
			(((pUnit->movesLeft() % iDenom) > 0) ? 1 : 0);
	// <advc.069>
	{
		bool const bFract = BUGOption::isEnabled("MainInterface__UnitMovementPointsFraction", true);
		CvWString szTempBuffer;
		if(pUnit->baseMoves() == (bFract ? pUnit->movesLeft() : iCurrMoves) || // </advc.069>
			!pUnit->isActiveTeam())
		{
			szTempBuffer.Format(L"%d%c", pUnit->baseMoves(), gDLL->getSymbolID(MOVES_CHAR));
		}
		// advc.069: Display as in BtS (as integer) if non-fractional
		else if(!bFract || pUnit->movesLeft() == iCurrMoves * iDenom)
		{
			szTempBuffer.Format(L"%d/%d%c", iCurrMoves, pUnit->baseMoves(),
					gDLL->getSymbolID(MOVES_CHAR));
		}
		// <advc.069> Akin to BUG code in CvMainInterface.py (Unit Movement Fraction)
		else
		{
			float fCurrMoves = pUnit->movesLeft() / (float)iDenom;
			szTempBuffer.Format(L"%.1f/%d%c", fCurrMoves, pUnit->baseMoves(),
					gDLL->getSymbolID(MOVES_CHAR));
		} // </advc.069>
		szString.append(szTempBuffer);
	}
	if (pUnit->airRange() > 0)
	{
		szString.append(gDLL->getText("TXT_KEY_UNIT_HELP_AIR_RANGE",
				pUnit->airRange()));
	}

	BuildTypes eBuild = pUnit->getBuildType();

	if (eBuild != NO_BUILD)
	{
		szString.append(L", ");
		/*  <advc.011b> Show turns-to-build as "(x+1)" when the Worker has been
			told not to finish it -- it'll build for x turns, make a pause,
			eventually build for 1 more turn. */
		szString.append(GC.getInfo(eBuild).getDescription());
		int iTurns = pUnit->getPlot().getBuildTurnsLeft(eBuild,
				/* advc.251: */ pUnit->getOwner(), 0, 0);
		bool bSuspend = false;
		if(iTurns > 1)
		{
			CLLNode<MissionData>* pNode = pUnit->getGroup()->headMissionQueueNode();
			if(pNode != NULL)
			{
				if(pNode->m_data.bModified && (GC.ctrlKey() ||
					BUGOption::isEnabled("MiscHover__PartialBuildsAlways", false)))
				{
					bSuspend = true;
				}
			}
		}
		CvWString szTempBuffer;
		if(bSuspend)
		{
			szTempBuffer.Format(L"(%d+" SETCOLR L"%d" ENDCOLR L")", iTurns - 1,
					TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"), 1);
		}
		else // </advc.011b>
			szTempBuffer.Format(L"(%d)", iTurns);
		szString.append(szTempBuffer);
	}

	if (pUnit->getImmobileTimer() > 0)
	{
		szString.append(L", ");
		szString.append(gDLL->getText("TXT_KEY_UNIT_HELP_IMMOBILE", pUnit->getImmobileTimer()));
	}

	/*if (!bOneLine) {
		if (pUnit->getUnitCombatType() != NO_UNITCOMBAT) {
			szTempBuffer.Format(L" (%s)", GC.getInfo(pUnit->getUnitCombatType()).getDescription());
			szString += szTempBuffer;
		}
	}*/

	// advc.007: Commented out.Can alway press Ctrl+Alt for this info.
	/*if (bDebugMode && !bAlt && !bShift) {
		FAssertMsg(pUnit->AI_getUnitAIType() != NO_UNITAI, "pUnit's AI type expected to != NO_UNITAI");
		szTempBuffer.Format(L" (%s)", GC.getInfo(pUnit->AI_getUnitAIType()).getDescription());
		szString.append(szTempBuffer);
	}*/

	if (pUnit->isActiveTeam() || (bDebugMode && /* advc.007: */ !bOneLine))
	{
		if (pUnit->getExperience() > 0 && !pUnit->isFighting())
		{
			szString.append(gDLL->getText("TXT_KEY_UNIT_HELP_LEVEL",
					pUnit->getExperience(), pUnit->experienceNeeded()));
		}
	}

	//if (!pUnit->isActiveOwned() && !pUnit->isAnimal() && !kInfo.isHiddenNationality())
	if (!bOmitOwner && !pUnit->isUnowned()) // advc.061: Replacing the above
	{
		CvPlayer const& kOwner = GET_PLAYER(pUnit->getOwner());
		szString.append(L", ");
		CvWString szTempBuffer;
		szTempBuffer.Format(SETCOLR L"%s" ENDCOLR,
				PLAYER_TEXT_COLOR(kOwner),
				//kOwner.getName());
				kOwner.getCivilizationAdjective()); // rfc
		szString.append(szTempBuffer);
	}
	{
		bool bFirst = true; // advc.004
		FOR_EACH_ENUM(Promotion)
		{
			if (pUnit->isHasPromotion(eLoopPromotion))
			{
				CvWString szTempBuffer;
				szTempBuffer.Format(L"<img=%S size=16 />",
						GC.getInfo(eLoopPromotion).getButton());
				// <advc.004>
				if (bFirst)
				{
					szString.append(' ');
					bFirst = false;
				} // </advc.004>
				szString.append(szTempBuffer);
			}
		}
	}
	if (bAlt && /*(gDLL->getChtLvl() > 0))*/ /* advc.135c: */ bDebugMode)
	{
		CvSelectionGroup const* pGroup = pUnit->getGroup();
		if (pGroup != NULL)
		{
			if (pUnit->isGroupHead())
				szString.append(CvWString::format(L"\nLeading "));
			else szString.append(L"\n");
			CvWString szTempBuffer;
			szTempBuffer.Format(L"Group(%d), %d units",
					pGroup->getID(), pGroup->getNumUnits());
			szString.append(szTempBuffer);
		}
	}

	if (bOneLine)
		return;

	// advc.007: Don't show rival spy test in Debug mode
	if (pUnit->isActiveTeam())
		setEspionageMissionHelp(szString, pUnit);

	// <advc.313>
	int iBarbarianMovesHandicap = 0;
	int iBarbarianCombatHandicap = 0;
	int iBarbarianCityAttackHandicap = 0;
	if (!bShort && pUnit->isBarbarian() && pUnit->canFight())
	{
		CvHandicapInfo const& kHandicap = GC.getInfo(
				GET_PLAYER(getActivePlayer()).getHandicapType());
		iBarbarianCombatHandicap += kHandicap.getBarbarianCombatModifier();
		if (pUnit->isAnimal())
			iBarbarianCombatHandicap += kHandicap.getAnimalCombatModifier();
		else if (pUnit->isKnownSeaBarbarian())
		{
			iBarbarianCombatHandicap += kHandicap.get(
					CvHandicapInfo::SeaBarbarianBonus);
			iBarbarianMovesHandicap += kHandicap.get(
					CvHandicapInfo::SeaBarbarianExtraMoves);
		}
		else if (pUnit->getDomainType() == DOMAIN_LAND)
		{
			iBarbarianCityAttackHandicap += kHandicap.get(
					CvHandicapInfo::BarbarianCityAttackBonus);
		}
		// (Will display these below along with promotion effects)
	} // </advc.313>

	if (pUnit->cargoSpace() > 0)
	{
		CvWString szTempBuffer;
		if (pUnit->isActiveTeam())
		{
			szTempBuffer = NEWLINE + gDLL->getText("TXT_KEY_UNIT_HELP_CARGO_SPACE",
					pUnit->getCargo(), pUnit->cargoSpace());
		}
		else
		{
			szTempBuffer = NEWLINE + gDLL->getText("TXT_KEY_UNIT_CARGO_SPACE",
					pUnit->cargoSpace());
		}
		szString.append(szTempBuffer);

		if (pUnit->specialCargo() != NO_SPECIALUNIT)
		{
			szString.append(gDLL->getText("TXT_KEY_UNIT_CARRIES",
					GC.getInfo(pUnit->specialCargo()).getTextKeyWide()));
		}
	}

	if (pUnit->fortifyModifier() != 0)
	{
		szString.append(NEWLINE);
		szString.append(gDLL->getText("TXT_KEY_UNIT_HELP_FORTIFY_BONUS",
				pUnit->fortifyModifier()));
	}

	if (!bShort)
	{
		if (pUnit->isNuke())
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_UNIT_CAN_NUKE"));
		}

		if (pUnit->alwaysInvisible())
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_UNIT_INVISIBLE_ALL"));
		}
		else if (pUnit->getInvisibleType() != NO_INVISIBLE)
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_UNIT_INVISIBLE_MOST"));
		}

		for (int i = 0; i < pUnit->getNumSeeInvisibleTypes(); i++)
		{
			if (pUnit->getSeeInvisibleType(i) != pUnit->getInvisibleType())
			{
				szString.append(NEWLINE);
				szString.append(gDLL->getText("TXT_KEY_UNIT_SEE_INVISIBLE",
						GC.getInfo(pUnit->getSeeInvisibleType(i)).getTextKeyWide()));
			}
		}

		if (pUnit->canMoveImpassable())
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_UNIT_CAN_MOVE_IMPASSABLE"));
		}
	}

	if (pUnit->maxFirstStrikes() > 0)
	{
		if (pUnit->firstStrikes() == pUnit->maxFirstStrikes())
		{
			if (pUnit->firstStrikes() == 1)
			{
				szString.append(NEWLINE);
				szString.append(gDLL->getText("TXT_KEY_UNIT_ONE_FIRST_STRIKE"));
			}
			else
			{
				szString.append(NEWLINE);
				szString.append(gDLL->getText("TXT_KEY_UNIT_NUM_FIRST_STRIKES",
						pUnit->firstStrikes()));
			}
		}
		else
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_UNIT_FIRST_STRIKE_CHANCES",
					pUnit->firstStrikes(), pUnit->maxFirstStrikes()));
		}
	}

	if (pUnit->immuneToFirstStrikes())
	{
		szString.append(NEWLINE);
		szString.append(gDLL->getText("TXT_KEY_UNIT_IMMUNE_FIRST_STRIKES"));
	}

	if (!bShort)
	{	// <advc.315> Whether a unit can attack is too important to omit
		if (pUnit->isOnlyDefensive())
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_UNIT_ONLY_DEFENSIVE"));
		} // </advc.315>
		// <advc.315a> Same code as under setBasicUnitHelp
		if (kInfo.isOnlyAttackAnimals())
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_UNIT_ONLY_ATTACK_ANIMALS"));
		} // </advc.315a>
		// <advc.315b>
		if (kInfo.isOnlyAttackBarbarians())
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_UNIT_ONLY_ATTACK_BARBARIANS"));
		} // </advc.315b>
		if (pUnit->noDefensiveBonus())
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_UNIT_NO_DEFENSE_BONUSES"));
		}
		/*	advc.opt: was pUnit->flatMovementCost, which is now always true
			for air units. Don't want to show text for those. */
		if (pUnit->getUnitInfo().isFlatMovementCost())
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_UNIT_FLAT_MOVEMENT"));
		}

		if (pUnit->ignoreTerrainCost())
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_UNIT_IGNORE_TERRAIN"));
		}

		if (pUnit->isBlitz())
		{
			szString.append(NEWLINE);
			// <advc.164>
			int iBlitz = pUnit->getBlitzCount();
			if (iBlitz > 0)
			{
				if (iBlitz > 1)
				{
					szString.append(gDLL->getText("TXT_KEY_PROMOTION_BLITZ_LIMIT",
							iBlitz + 1));
				}
				else szString.append(gDLL->getText("TXT_KEY_PROMOTION_BLITZ_TWICE"));
			}
			else // </advc.164>
				szString.append(gDLL->getText("TXT_KEY_PROMOTION_BLITZ_TEXT"));
		}

		if (pUnit->isAmphib())
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_PROMOTION_AMPHIB_TEXT"));
		}

		if (pUnit->isRiver())
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_PROMOTION_RIVER_ATTACK_TEXT"));
		}

		if (pUnit->isEnemyRoute())
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_PROMOTION_ENEMY_ROADS_TEXT"));
		}

		if (pUnit->isAlwaysHeal())
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_PROMOTION_ALWAYS_HEAL_TEXT"));
		}

		if (pUnit->isHillsDoubleMove())
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_PROMOTION_HILLS_MOVE_TEXT"));
		}

		FOR_EACH_ENUM(Terrain)
		{
			if (pUnit->isTerrainDoubleMove(eLoopTerrain))
			{
				szString.append(NEWLINE);
				szString.append(gDLL->getText("TXT_KEY_PROMOTION_DOUBLE_MOVE_TEXT",
						GC.getInfo(eLoopTerrain).getTextKeyWide()));
			}
		}

		FOR_EACH_ENUM(Feature)
		{
			if (pUnit->isFeatureDoubleMove(eLoopFeature))
			{
				szString.append(NEWLINE);
				szString.append(gDLL->getText("TXT_KEY_PROMOTION_DOUBLE_MOVE_TEXT",
						GC.getInfo(eLoopFeature).getTextKeyWide()));
			}
		}

		if (pUnit->getExtraVisibilityRange() != 0)
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_PROMOTION_VISIBILITY_TEXT",
					pUnit->getExtraVisibilityRange()));
		}

		if (pUnit->getExtraMoveDiscount() != 0)
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_PROMOTION_MOVE_DISCOUNT_TEXT",
					-pUnit->getExtraMoveDiscount()));
		}

		if (pUnit->getExtraEnemyHeal() != 0)
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_PROMOTION_HEALS_EXTRA_TEXT",
					pUnit->getExtraEnemyHeal()) +
					gDLL->getText("TXT_KEY_PROMOTION_ENEMY_LANDS_TEXT"));
		}

		if (pUnit->getExtraNeutralHeal() != 0)
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_PROMOTION_HEALS_EXTRA_TEXT",
					pUnit->getExtraNeutralHeal()) +
					gDLL->getText("TXT_KEY_PROMOTION_NEUTRAL_LANDS_TEXT"));
		}

		if (pUnit->getExtraFriendlyHeal() != 0)
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_PROMOTION_HEALS_EXTRA_TEXT",
					pUnit->getExtraFriendlyHeal()) +
					gDLL->getText("TXT_KEY_PROMOTION_FRIENDLY_LANDS_TEXT"));
		}

		if (pUnit->getSameTileHeal() != 0)
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_PROMOTION_HEALS_SAME_TEXT",
					pUnit->getSameTileHeal()) +
					gDLL->getText("TXT_KEY_PROMOTION_DAMAGE_TURN_TEXT"));
		}

		if (pUnit->getAdjacentTileHeal() != 0)
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_PROMOTION_HEALS_ADJACENT_TEXT",
					pUnit->getAdjacentTileHeal()) +
					gDLL->getText("TXT_KEY_PROMOTION_DAMAGE_TURN_TEXT"));
		}
	}

	if (pUnit->currInterceptionProbability() > 0)
	{
		// SuperSpies
		if (pUnit->isSpy())
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_UNIT_INTERCEPT_AIRCRAFT_SPY",
				pUnit->currInterceptionProbability()));
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_UNIT_INTERCEPT_AIRCRAFT_SPY_COUNTER",
				pUnit->currInterceptionProbability() * 5));
		}
		else
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_UNIT_INTERCEPT_AIRCRAFT",
				pUnit->currInterceptionProbability()));
		}
	}

	if (pUnit->evasionProbability() > 0)
	{
		szString.append(NEWLINE);
		szString.append(gDLL->getText("TXT_KEY_UNIT_EVADE_INTERCEPTION",
				pUnit->evasionProbability()));
	}

	if (pUnit->withdrawalProbability() > 0)
	{
		if (bShort)
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_UNIT_WITHDRAWL_PROBABILITY_SHORT",
					pUnit->withdrawalProbability()));
		}
		else
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_UNIT_WITHDRAWL_PROBABILITY",
					pUnit->withdrawalProbability()));
		}
	}

	if (pUnit->combatLimit() < GC.getMAX_HIT_POINTS() && pUnit->canAttack())
	{
		szString.append(NEWLINE);
		szString.append(gDLL->getText("TXT_KEY_UNIT_COMBAT_LIMIT",
				(100 * pUnit->combatLimit()) / GC.getMAX_HIT_POINTS()));
	}

	if (pUnit->collateralDamage() > 0)
	{
		szString.append(NEWLINE);
		if (pUnit->getExtraCollateralDamage() == 0)
		{
			szString.append(gDLL->getText(
					"TXT_KEY_UNIT_COLLATERAL_DAMAGE_SHORT", // advc.004: short version
					100 * kInfo.getCollateralDamageLimit() / GC.getMAX_HIT_POINTS(),
					pUnit->collateralDamageMaxUnits())); // advc.004
		}
		else
		{
			szString.append(gDLL->getText("TXT_KEY_UNIT_COLLATERAL_DAMAGE_EXTRA",
					pUnit->getExtraCollateralDamage()));
		}
	}

	FOR_EACH_ENUM(UnitCombat)
	{
		if (kInfo.getUnitCombatCollateralImmune(eLoopUnitCombat))
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_UNIT_COLLATERAL_IMMUNE",
					GC.getInfo(eLoopUnitCombat).getTextKeyWide()));
		}
	}

	if (pUnit->getCollateralDamageProtection() > 0)
	{
		szString.append(NEWLINE);
		szString.append(gDLL->getText("TXT_KEY_PROMOTION_COLLATERAL_PROTECTION_TEXT",
				pUnit->getCollateralDamageProtection()));
	}
	// <advc.313>
	if (iBarbarianCombatHandicap != 0)
	{
		szString.append(NEWLINE);
		szString.append(CvWString::format(SETCOLR L"%s" ENDCOLR,
				PLAYER_TEXT_COLOR(GET_PLAYER(pUnit->getOwner())),
				gDLL->getText("TXT_KEY_PROMOTION_STRENGTH_TEXT",
				iBarbarianCombatHandicap).c_str()));
	} // </advc.313>
	if (pUnit->getExtraCombatPercent() != 0)
	{
		szString.append(NEWLINE);
		szString.append(gDLL->getText("TXT_KEY_PROMOTION_STRENGTH_TEXT",
				pUnit->getExtraCombatPercent()));
	}
	// <advc.313>
	if (iBarbarianCityAttackHandicap != 0)
	{
		szString.append(NEWLINE);
		szString.append(CvWString::format(SETCOLR L"%s" ENDCOLR,
				PLAYER_TEXT_COLOR(GET_PLAYER(pUnit->getOwner())),
				gDLL->getText("TXT_KEY_PROMOTION_CITY_ATTACK_TEXT",
				iBarbarianCityAttackHandicap).c_str()));
	} // </advc.313>
	if (pUnit->cityAttackModifier() == pUnit->cityDefenseModifier())
	{
		if (pUnit->cityAttackModifier() != 0)
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_UNIT_CITY_STRENGTH_MOD",
					pUnit->cityAttackModifier()));
		}
	}
	else
	{
		if (pUnit->cityAttackModifier() != 0)
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_PROMOTION_CITY_ATTACK_TEXT",
					pUnit->cityAttackModifier()));
		}

		if (pUnit->cityDefenseModifier() != 0)
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_PROMOTION_CITY_DEFENSE_TEXT",
					pUnit->cityDefenseModifier()));
		}
	}

	if (pUnit->animalCombatModifier() != 0)
	{
		szString.append(NEWLINE);
		szString.append(gDLL->getText("TXT_KEY_UNIT_ANIMAL_COMBAT_MOD",
				pUnit->animalCombatModifier()));
	}
	// <advc.315c>
	if (pUnit->barbarianCombatModifier() != 0)
	{
		szString.append(NEWLINE);
		szString.append(gDLL->getText("TXT_KEY_UNIT_BARBARIAN_COMBAT_MOD",
				pUnit->barbarianCombatModifier()));
	} // </advc.315c>

	if (pUnit->getDropRange() > 0)
	{
		szString.append(NEWLINE);
		szString.append(gDLL->getText("TXT_KEY_UNIT_PARADROP_RANGE",
				pUnit->getDropRange()));
	}

	if (pUnit->hillsAttackModifier() == pUnit->hillsDefenseModifier())
	{
		if (pUnit->hillsAttackModifier() != 0)
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_UNIT_HILLS_STRENGTH",
					pUnit->hillsAttackModifier()));
		}
	}
	else
	{
		if (pUnit->hillsAttackModifier() != 0)
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_UNIT_HILLS_ATTACK",
					pUnit->hillsAttackModifier()));
		}

		if (pUnit->hillsDefenseModifier() != 0)
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_UNIT_HILLS_DEFENSE",
					pUnit->hillsDefenseModifier()));
		}
	}

	// doc: plains combat modifiers
	if (pUnit->plainsAttackModifier() == pUnit->plainsDefenseModifier())
	{
		if (pUnit->plainsAttackModifier() != 0)
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_UNIT_PLAINS_STRENGTH",
				pUnit->plainsAttackModifier()));
		}
	}
	else
	{
		if (pUnit->plainsAttackModifier() != 0)
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_UNIT_PLAINS_ATTACK",
				pUnit->plainsAttackModifier()));
		}

		if (pUnit->plainsDefenseModifier() != 0)
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_UNIT_PLAINS_DEFENSE",
				pUnit->plainsDefenseModifier()));
		}
	}

	// doc: river attack modifier
	if (pUnit->riverAttackModifier() != 0)
	{
		szString.append(NEWLINE);
		szString.append(gDLL->getText("TXT_KEY_UNIT_RIVER_ATTACK",
			pUnit->riverAttackModifier()));
	}

	FOR_EACH_ENUM(Terrain) // advc: loop refactored
	{
		int const iAttackMod = pUnit->terrainAttackModifier(eLoopTerrain);
		int const iDefenseMod = pUnit->terrainDefenseModifier(eLoopTerrain);
		if (iAttackMod != 0)
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText(iAttackMod == iDefenseMod ?
					"TXT_KEY_UNIT_STRENGTH" : "TXT_KEY_UNIT_ATTACK",
					iAttackMod, GC.getInfo(eLoopTerrain).getTextKeyWide()));
		}
		if (iAttackMod != iDefenseMod && iDefenseMod != 0)
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_UNIT_DEFENSE", iDefenseMod,
					GC.getInfo(eLoopTerrain).getTextKeyWide()));
		}
	}
	FOR_EACH_ENUM(Feature)
	{
		int const iAttackMod = pUnit->featureAttackModifier(eLoopFeature);
		int const iDefenseMod = pUnit->featureDefenseModifier(eLoopFeature);
		if (iAttackMod != 0)
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText(iAttackMod == iDefenseMod ?
					"TXT_KEY_UNIT_STRENGTH" : "TXT_KEY_UNIT_ATTACK",
					iAttackMod, GC.getInfo(eLoopFeature).getTextKeyWide()));
		}
		if (iAttackMod != iDefenseMod && iDefenseMod != 0)
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_UNIT_DEFENSE", iDefenseMod,
					GC.getInfo(eLoopFeature).getTextKeyWide()));
		}
	}
	FOR_EACH_ENUM(UnitClass)
	{
		int const iAttackMod = kInfo.getUnitClassAttackModifier(eLoopUnitClass);
		int const iDefenseMod = kInfo.getUnitClassDefenseModifier(eLoopUnitClass);
		if (iAttackMod != 0)
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText(iAttackMod == iDefenseMod ?
					"TXT_KEY_UNIT_MOD_VS_TYPE" : "TXT_KEY_UNIT_ATTACK_MOD_VS_CLASS",
					iAttackMod, GC.getInfo(eLoopUnitClass).getTextKeyWide()));
		}
		if (iAttackMod != iDefenseMod && iDefenseMod != 0)
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_UNIT_DEFENSE_MOD_VS_CLASS", iDefenseMod,
					GC.getInfo(eLoopUnitClass).getTextKeyWide()));
		}
	}
	FOR_EACH_ENUM(UnitCombat)
	{
		if (pUnit->unitCombatModifier(eLoopUnitCombat) != 0)
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_UNIT_MOD_VS_TYPE",
					pUnit->unitCombatModifier(eLoopUnitCombat),
					GC.getInfo(eLoopUnitCombat).getTextKeyWide()));
		}
	}
	FOR_EACH_ENUM(Domain)
	{
		if (pUnit->domainModifier(eLoopDomain) != 0)
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_UNIT_MOD_VS_TYPE",
					pUnit->domainModifier(eLoopDomain),
					GC.getInfo(eLoopDomain).getTextKeyWide()));
		}
	}
	{
		CvWString szTempBuffer;
		bool bFirst = true;
		FOR_EACH_ENUM(UnitClass)
		{
			if (kInfo.getTargetUnitClass(eLoopUnitClass))
			{
				if (bFirst)
					bFirst = false;
				else szTempBuffer += L", ";
				szTempBuffer += CvWString::format(L"<link=literal>%s</link>",
						GC.getInfo(eLoopUnitClass).getDescription());
			}
		}
		if (!bFirst)
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_UNIT_TARGETS_UNIT_FIRST",
					szTempBuffer.GetCString()));
		}
	}
	{
		CvWString szTempBuffer;
		bool bFirst = true;
		FOR_EACH_ENUM(UnitClass)
		{
			if (kInfo.getDefenderUnitClass(eLoopUnitClass))
			{
				if (bFirst)
					bFirst = false;
				else szTempBuffer += L", ";
				szTempBuffer += CvWString::format(L"<link=literal>%s</link>",
						GC.getInfo(eLoopUnitClass).getDescription());
			}
		}
		if (!bFirst)
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_UNIT_DEFENDS_UNIT_FIRST",
					szTempBuffer.GetCString()));
		}
	}
	{
		CvWString szTempBuffer;
		bool bFirst = true;
		FOR_EACH_ENUM(UnitCombat)
		{
			if (kInfo.getTargetUnitCombat(eLoopUnitCombat))
			{
				if (bFirst)
					bFirst = false;
				else szTempBuffer += L", ";
				szTempBuffer += CvWString::format(L"<link=literal>%s</link>",
						GC.getInfo(eLoopUnitCombat).getDescription());
			}
		}
		if (!bFirst)
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_UNIT_TARGETS_UNIT_FIRST",
					szTempBuffer.GetCString()));
		}
	}
	{
		CvWString szTempBuffer;
		bool bFirst = true;
		FOR_EACH_ENUM(UnitCombat)
		{
			if (kInfo.getDefenderUnitCombat(eLoopUnitCombat))
			{
				if (bFirst)
					bFirst = false;
				else szTempBuffer += L", ";
				szTempBuffer += CvWString::format(L"<link=literal>%s</link>",
						GC.getInfo(eLoopUnitCombat).getDescription());
			}
		}
		if (!bFirst)
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_UNIT_DEFENDS_UNIT_FIRST",
					szTempBuffer.GetCString()));
		}
	}
	{
		CvWString szTempBuffer;
		bool bFirst = true;
		FOR_EACH_ENUM(UnitClass)
		{
			if (kInfo.getFlankingStrikeUnitClass(eLoopUnitClass) > 0)
			{
				if (bFirst)
					bFirst = false;
				else szTempBuffer += L", ";
				szTempBuffer += CvWString::format(L"<link=literal>%s</link>",
						GC.getInfo(eLoopUnitClass).getDescription());
			}
		}
		if (!bFirst)
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_UNIT_FLANKING_STRIKES",
					szTempBuffer.GetCString()));
		}
	}
	{
		int iBombRate = pUnit->bombardRate();
		// <advc.004c>
		bool bAirBomb = false;
		if (iBombRate <= 0)
		{
			iBombRate = pUnit->airBombCurrRate();
			bAirBomb = true;
		} // </advc.004c>
		if (iBombRate > 0)
		{
			if (bShort ||
				bAirBomb) // advc.004c: Always use the short version for that
			{
				szString.append(NEWLINE);
				szString.append(gDLL->getText(
						bAirBomb ? "TXT_KEY_UNIT_AIR_BOMB_RATE_SHORT" : // advc.004c
						"TXT_KEY_UNIT_BOMBARD_RATE_SHORT",
						(iBombRate * 100) / GC.getMAX_CITY_DEFENSE_DAMAGE()));
			}
			else
			{
				szString.append(NEWLINE);
				szString.append(gDLL->getText("TXT_KEY_UNIT_BOMBARD_RATE",
						(iBombRate * 100) / GC.getMAX_CITY_DEFENSE_DAMAGE()));
			}
		}
	}

	if (pUnit->isSpy())
	{
		szString.append(NEWLINE);
		szString.append(gDLL->getText("TXT_KEY_UNIT_IS_SPY"));
	}

	if (kInfo.isNoRevealMap())
	{
		szString.append(NEWLINE);
		szString.append(gDLL->getText("TXT_KEY_UNIT_VISIBILITY_MOVE_RANGE"));
	}
	// <advc.313>
	if (iBarbarianMovesHandicap != 0)
	{
		szString.append(NEWLINE);
		szString.append(CvWString::format(SETCOLR L"%s" ENDCOLR,
				PLAYER_TEXT_COLOR(GET_PLAYER(pUnit->getOwner())),
				gDLL->getText("TXT_KEY_PROMOTION_MOVE_TEXT",
				iBarbarianMovesHandicap).c_str()));
	} // </advc.313>

	if (!CvWString(kInfo.getHelp()).empty())
	{
		szString.append(NEWLINE);
		szString.append(kInfo.getHelp());
	}

	if (bShift && /*(gDLL->getChtLvl() > 0))*/ /* advc.135c: */ bDebugMode)
	{
		CvWString szTempBuffer;
		szTempBuffer.Format(L"\nUnitAI Type = %s.",
				GC.getInfo(pUnit->AI_getUnitAIType()).getDescription());
		szString.append(szTempBuffer);
		szTempBuffer.Format(L"\nSacrifice Value = %d.",
				pUnit->AI().AI_sacrificeValue(NULL));
		szString.append(szTempBuffer);
	}
}

/*	advc.004: Based on code cut from setUnitHelp.
	Avoids showing units that are very slightly damaged at full strength
	or units that are barely alive at 0 strength. */
void CvGameTextMgr::setHurtUnitStrength(CvWString& szBuffer, CvUnit const& kUnit,
	/* <advc.048c> */ int iHP)
{
	if (iHP < 0)
		iHP = kUnit.currHitPoints(); // </advc.048c>
	int const iBaseStr = (kUnit.getDomainType() == DOMAIN_AIR ?
			kUnit.airBaseCombatStr() : kUnit.baseCombatStr());
	// as in BtS:
	float fCurrStrength = iBaseStr * iHP / (float)kUnit.maxHitPoints();
	int iCurrStrengthTimes100 = (100 * iBaseStr * iHP) / kUnit.maxHitPoints();
	// %.1f would round up to e.g. 2.0/2 for a Warrior here
	if (iBaseStr * kUnit.maxHitPoints() - iCurrStrengthTimes100 <= 5)
		fCurrStrength = iBaseStr - 0.1f;
	if (iCurrStrengthTimes100 < 5) // %.1f would show 0.0 here
		fCurrStrength = 0.1f;
	// as in BtS:
	szBuffer.Format(L"%.1f/%d%c", fCurrStrength,
			iBaseStr, gDLL->getSymbolID(STRENGTH_CHAR));
}

// <advc.061>
bool CvGameTextMgr::listFirstUnitBeforeSecond(CvUnit const* pFirst, CvUnit const* pSecond)
{
	// Top priority: cargo - but only if owned by active team
	TeamTypes eTeam = pFirst->getTeam(); // Caller ensures that both have same owner
	// ... which also means that these ids are unique:
	int iFirstID = pFirst->getID();
	int iSecondID = pSecond->getID();
	FAssert(pFirst != pSecond && iFirstID != iSecondID);
	if (eTeam == getActiveTeam() || GC.getGame().isDebugMode())
	{
		bool bFirstCargo = (pFirst->getCargo() > 0);
		bool bSecondCargo = (pSecond->getCargo() > 0);
		CvUnit const* pFirstTransport = (bFirstCargo ? pFirst :
				pFirst->getTransportUnit());
		CvUnit const* pSecondTransport = (bSecondCargo ? pSecond :
				pSecond->getTransportUnit());
		bool bFirstTransport = (pFirstTransport != NULL);
		bool bSecondTransport = (pSecondTransport != NULL);
		if (bFirstTransport != bSecondTransport)
			return bFirstTransport;
		if (bFirstTransport) // I.e. they're both involved with cargo
		{
			UnitTypes eFirstTransportType = pFirstTransport->getUnitType();
			UnitTypes eSecondTransportType = pSecondTransport->getUnitType();
			if(eFirstTransportType != eSecondTransportType)
			{
				return listFirstUnitTypeBeforeSecond(eFirstTransportType,
						eSecondTransportType);
			}
			int iFirstCargo = pFirstTransport->getCargo();
			int iSecondCargo = pSecondTransport->getCargo();
			if (iFirstCargo != iSecondCargo)
				return (iFirstCargo > iSecondCargo);
			// Use transport id to keep transport and cargo together
			int iFirstTransportID = pFirstTransport->getID();
			int iSecondTransportID = pSecondTransport->getID();
			if (iFirstTransportID != iSecondTransportID)
				return (iFirstTransportID < iSecondTransportID);
			// Only transport and its cargo left. Transport goes first.
			if (bFirstCargo != bSecondCargo)
				return bFirstCargo;
			/*  Now we know that pFirst and pSecond are loaded in the same transport.
				Let the non-transport code below determine their order. */
		}
	}
	UnitTypes eFirst = pFirst->getUnitType();
	UnitTypes eSecond = pSecond->getUnitType();
	if (eFirst == eSecond)
	{	// Make the order stable
		return (iFirstID < iSecondID);
	}
	return listFirstUnitTypeBeforeSecond(eFirst, eSecond);
}

CvPlot const* CvGameTextMgr::m_pHelpPlot = NULL;

bool CvGameTextMgr::listFirstUnitTypeBeforeSecond(UnitTypes eFirst, UnitTypes eSecond)
{
	CvUnit* pCenter = (m_pHelpPlot == NULL ? NULL : m_pHelpPlot->getCenterUnit());
	UnitTypes eCenterType = (pCenter == NULL ? NO_UNIT :
			pCenter->getUnitType());
	FAssert(eCenterType != NO_UNIT);
	if(eFirst != eSecond)
	{
		if(eFirst == eCenterType)
			return true;
		if(eSecond == eCenterType)
			return false;
	}
	CvUnitInfo const& u1 = GC.getInfo(eFirst);
	CvUnitInfo const& u2 = GC.getInfo(eSecond);
	int iFirstCombat = u1.getCombat();
	int iSecondCombat = u2.getCombat();
	if((iFirstCombat > 0) != (iSecondCombat > 0))
		return (iFirstCombat > 0);
	DomainTypes eFirstDomain = u1.getDomainType();
	DomainTypes eSecondDomain = u2.getDomainType();
	if(eFirstDomain != eSecondDomain)
	{
		DomainTypes eCenterDomain = (pCenter == NULL ? NO_DOMAIN :
				pCenter->getDomainType());
		FAssert(eCenterDomain != NO_DOMAIN);
		if(eFirstDomain == eCenterDomain)
			return true;
		if(eSecondDomain == eCenterDomain)
			return false;
		return (eFirstDomain > eSecondDomain);
	}
	if(iFirstCombat != iSecondCombat)
		return (iFirstCombat > iSecondCombat);
	return eFirst > eSecond;
}

void CvGameTextMgr::appendUnitOwnerHeading(CvWStringBuffer& szString, PlayerTypes eOwner,
	int iArmy, int iNavy, int iAir, int iTotal, bool bCollapsed)
{
	int iOther = iTotal - iArmy - iNavy; // Don't display iAir separately for now
	// Don't distinguish categories when there are few units in each
	if(iArmy < 5 && iNavy < 5 && iOther < 5 && !bCollapsed)
	{
		iOther = iTotal;
		iArmy = 0;
		iNavy = 0;
	}
	FAssert(iOther >= 0);
	if(!szString.isEmpty()) // No newline when PlotListHelp starts with a heading
		szString.append(NEWLINE);
	CvPlayer const& kOwner = GET_PLAYER(eOwner);
	szString.append(CvWString::format(SETCOLR L"%s" ENDCOLR,
			PLAYER_TEXT_COLOR(kOwner), kOwner.getName()));
	CvWString szCounts;
	if(iArmy >= iTotal || iNavy >= iTotal || iOther >= iTotal)
	{
		szCounts = CvWString::format(L" (%d %s)", iTotal,
				gDLL->getText("TXT_KEY_WB_UNITS").c_str());
	}
	else
	{
		szCounts = L" (";
		bool bFirst = true;
		if(iArmy > 0)
		{
			if(!bFirst)
				szCounts += L", ";
			bFirst = false;
			szCounts += CvWString::format(L"%d %s", iArmy,
					gDLL->getText("TXT_KEY_MISC_ARMY").c_str());
		}
		if(iNavy > 0)
		{
			if(!bFirst)
				szCounts += L", ";
			bFirst = false;
			szCounts += CvWString::format(L"%d %s", iNavy,
					gDLL->getText("TXT_KEY_MISC_NAVY").c_str());
		}
		if(iOther > 0)
		{
			szCounts += L", ";
			szCounts += CvWString::format(L"%d %s", iOther,
					gDLL->getText("TXT_KEY_MISC_OTHER").c_str());
		}
		szCounts += L")";
	}
	szString.append(szCounts);
	szString.append(L":");
}

// Reuses bits and pieces from setPlotListHelp
void CvGameTextMgr::appendUnitTypeAggregated(CvWStringBuffer& szString,
	std::vector<CvUnit const*> const& ownerUnits, UnitTypes eUnit,
	CvPlot const& kPlot, bool bIndicator) // advc.007
{
	CvUnit* pCenterUnit = kPlot.getCenterUnit();
	int iCount = 0;
	// These sums are computed as in BtS
	int iSumStrengthTimes100 = 0;
	int iSumMaxStrengthTimes100 = 0;
	std::vector<CvUnit const*> warlords;
	int const iPromotions = GC.getNumPromotionInfos();
	std::vector<int> promotionCounts(iPromotions, 0);
	for(size_t i = 0; i < ownerUnits.size(); i++)
	{
		CvUnit const* pUnit = ownerUnits[i];
		if(pUnit == NULL)
		{
			FAssert(pUnit != NULL);
			continue;
		}
		if(pUnit == pCenterUnit) // Already handled by caller
			continue;
		if(pUnit->getUnitType() != eUnit)
			continue;
		if(pUnit->getLeaderUnitType() != NO_UNIT)
		{
			warlords.push_back(pUnit);
			// These go on a separate line each
			continue;
		}
		iCount++;
		for(int j = 0; j < iPromotions; j++)
		{
			if(pUnit->isHasPromotion((PromotionTypes)j))
				promotionCounts[j]++;
		}
		if(pUnit->maxHitPoints() <= 0)
			continue;
		int iBase = (pUnit->getDomainType() == DOMAIN_AIR ?
				pUnit->airBaseCombatStr() : pUnit->baseCombatStr());
		if(iBase > 0)
		{
			iSumStrengthTimes100 += (100 * iBase * pUnit->currHitPoints()) /
					pUnit->maxHitPoints();
			iSumMaxStrengthTimes100 += 100 * iBase;
		}
	}
	if(iCount > 0)
	{
		szString.append(NEWLINE);
		CvUnitInfo const& u = GC.getInfo(eUnit);
		szString.append(CvWString::format(SETCOLR L"%s" ENDCOLR,
				TEXT_COLOR("COLOR_UNIT_TEXT"), u.getDescription()));
		appendAverageStrength(szString, iSumMaxStrengthTimes100,
				iSumStrengthTimes100, iCount);
		// Just like in setPlotListHelp (but with a vector)
		for(int j = 0; j < iPromotions; j++)
		{
			if(promotionCounts[j] > 0)
			{
				szString.append(CvWString::format(L"%d<img=%S size=16 />",
						promotionCounts[j],
						GC.getInfo((PromotionTypes)j).getButton()));
			}
		}
	}
	for(size_t i = 0; i < warlords.size(); i++)
	{
		szString.append(NEWLINE);
		setUnitHelp(szString, warlords[i], true, true, false, true,
				bIndicator); // advc.007
	}
}

// Cut and pasted (and refactored) from setPlotListHelp
void CvGameTextMgr::appendAverageStrength(CvWStringBuffer& szString,
	int iSumMaxStrengthTimes100, int iSumStrengthTimes100, int iUnits)
{
	if(iUnits > 1) // advc: This condition is new
		szString.append(CvWString::format(L" (%d)", iUnits));
	if(iSumMaxStrengthTimes100 <= 0)
		return;
	int iBase = (iSumMaxStrengthTimes100 / iUnits) / 100;
	int iCurrent = (iSumStrengthTimes100 / iUnits) / 100;
	int iCurrentRemainder = (iSumStrengthTimes100 / iUnits) % 100;
	if(iCurrentRemainder <= 0)
	{
		if(iBase == iCurrent)
			szString.append(CvWString::format(L" %d", iBase));
		else szString.append(CvWString::format(L" %d/%d", iCurrent, iBase));
	}
	else
	{
		szString.append(CvWString::format(L" %d.%02d/%d",
				iCurrent, iCurrentRemainder, iBase));
	}
	szString.append(CvWString::format(L"%c", gDLL->getSymbolID(STRENGTH_CHAR)));
}


void CvGameTextMgr::setPlotListHelpPerOwner(CvWStringBuffer& szString,
	CvPlot const& kPlot, bool bIndicator, bool bShort)
{
	if(kPlot.getCenterUnit() == NULL)
		return;
	// <advc.002b>
	int iFontSize = 12; // default when there is no custom theme
	CvArtInfoMisc const* pTheme = ARTFILEMGR.getMiscArtInfo("DEFAULT_THEME_NAME");
	if(pTheme != NULL && pTheme->getPath() != NULL)
	{
		CvString szThemePath(pTheme->getPath());
		/*  Don't know how to look up the font size. Would perhaps have to
			(re-)parse the theme files (no, thanks). Instead, the DLL is told
			through XML what font size to assume.
			I do know how to check if the mod's theme has been removed, and I don't
			want to rely on players changing the XML setting after removing it. */
		if(szThemePath.find("Mods") != CvString::npos)
			iFontSize = ::range(GC.getDefineINT("FONT_SIZE_FACTOR", 13), 7, 19);
	}
	// (The code below was written for iFontSize=14, so that's fontFactor=1.)
	double dFontFactor = 14.0 / iFontSize;
	// </advc.002b>
	CvGame const& kGame = GC.getGame();
	int iScreenHeight = kGame.getScreenHeight();
	int iLineLimit = (iScreenHeight == 0 ? 25 :
			fmath::round(32 * dFontFactor * kGame.getScreenHeight() / 1000.0 - 5));
	/*  When hovering over a plot indicator (unit layer), only info about units
		in kPlot is shown. This means more space. Same when hovering over a flag
		(bShort). */
	if(bIndicator || bShort)
		iLineLimit += 4;
	{	// Reserve space for interface mode info
		InterfaceModeTypes eMode = gDLL->UI().getInterfaceMode();
		if (eMode != INTERFACEMODE_SELECTION && eMode != INTERFACEMODE_GRIP &&
			eMode != INTERFACEMODE_PYTHON_PICK_PLOT && eMode != INTERFACEMODE_GO_TO)
		{
			iLineLimit--;
			// <advc.004c>
			// Interception info
			if (eMode == INTERFACEMODE_AIRBOMB ||
				eMode == INTERFACEMODE_AIRSTRIKE ||
				eMode == INTERFACEMODE_PARADROP)
			{
				iLineLimit -= 3;
			}
			// Airbomb effect
			if (eMode == INTERFACEMODE_AIRBOMB)
				iLineLimit--;
			// </advc.004c>
		}
	}
	TeamTypes const eActiveTeam = getActiveTeam();
	PlayerTypes const eActivePlayer = getActivePlayer();
	// Adjust to other info to be displayed
	iLineLimit += 4;
	if(kPlot.isImproved())
		iLineLimit--;
	if(kPlot.isRoute())
		iLineLimit--;
	if(kPlot.isFeature())
		iLineLimit--;
	if(kPlot.defenseModifier(eActiveTeam, true) > 0)
		iLineLimit--;
	if(kPlot.isFreshWater())
		iLineLimit--;
	/*	<advc.101> (Can even take up 2 lines, but checking for that gets too complicated;
		not checking MainInterface__RevoltHelp BUG option either.) */
	if (kPlot.isCity() && kPlot.getTeam() == eActiveTeam &&
		kPlot.getPlotCity()->revoltProbability() > 0)
	{
		iLineLimit--;
	} // </advc.101>
	for(int i = 0; i < MAX_PLAYERS; i++)
	{
		if(kPlot.calculateCulturePercent((PlayerTypes)i) > 0)
			iLineLimit--;
	}
	iLineLimit = std::max(iLineLimit, 15);
	/*  BtS shows no owner for Privateers and Animals (but it does for Barbarians);
		I'm calling units without a visible owner "rogue" units and they get their
		own entries in the perOwner vector. I'm also treating Barbarians inside
		cities that way b/c only Barbarian units (and spies) can exist there.
		These distinctions are implemented in CvUnit::isUnowned b/c I also want
		rogues to be preferred as the center unit -- this makes sure that the
		center unit can be listed first w/o the need for a heading.
		(That said, I'm also revealing the owner of Privateers when they're stacked
		with non-Privateers, meaning that such Privateers aren't rogues and that
		rogues really can't be stacked with non-rogues, so that change to the
		center unit is arguably obsolete.) */
	int const iRogueIndex = MAX_PLAYERS;
	int const ARMY = 0;
	int const NAVY = 1;
	int const AIR = 2;
	int const OTHER = 3;
	int const ALL = 4;
	std::vector<CvUnit const*> perOwner[iRogueIndex + 1][ALL+1];
	FOR_EACH_UNIT_IN(pUnit, kPlot)
	{
		if(pUnit == NULL)
		{
			FAssert(pUnit != NULL);
			continue;
		}
		if(pUnit->isInvisible(eActiveTeam, true))
			continue;
		PlayerTypes eVisualOwner = pUnit->getVisualOwner(eActiveTeam);
		if(eVisualOwner == NO_PLAYER)
		{
			FAssert(eVisualOwner != NO_PLAYER);
			continue;
		}
		int iType = OTHER;
		if(pUnit->baseCombatStr() > 0)
		{
			DomainTypes eDomain = pUnit->getDomainType();
			if(eDomain == DOMAIN_LAND)
				iType = ARMY;
			else if(eDomain == DOMAIN_SEA)
				iType = NAVY;
			else if(eDomain == DOMAIN_AIR)
				iType = AIR;
		}
		int iOwnerIndex = (pUnit->isUnowned() ? iRogueIndex : eVisualOwner);
		perOwner[iOwnerIndex][iType].push_back(pUnit);
		perOwner[iOwnerIndex][ALL].push_back(pUnit);
	}
	int iHeadings = 0;
	int iOwners = 0;
	uint uTotal = perOwner[iRogueIndex][ALL].size();
	for(int i = 0; i < iRogueIndex; i++) // Rogue units don't get a heading
	{
		int const iSize = perOwner[i][ALL].size();
		if (iSize <= 0)
			continue;
		iOwners++;
		//uTotal += iSize; // Not good enough; need to anticipate linewrap.
		for(int j = 0; j < iSize; j++)
		{
			uTotal++;
			// Ad hoc heuristic for estimating the required (horizontal) space
			int iSpaceValue = perOwner[i][ALL][j]->getName().length()
					+ (8 * perOwner[i][ALL][j]->getExperience()) / 5;
			if(perOwner[i][ALL][j]->getDamage() > 0)
				iSpaceValue += 2;
			if(iSpaceValue >= 30)
				uTotal++;
		}
		if(iSize > 1)
			iHeadings++;
	}
	int iTotal = (int)uTotal;
	CvUnit const& kCenterUnit = *kPlot.getCenterUnit();
	PlayerTypes eCenterOwner = kCenterUnit.getVisualOwner();
	int iCenterOwner = eCenterOwner;
	if(kCenterUnit.isUnowned())
		iCenterOwner = iRogueIndex;
	/*  First heading, unless rogue or a small number of units of only the active player,
		or a single unit of any player as the center unit. */
	else if((iTotal >= 5 || iHeadings > 1 || eCenterOwner != eActivePlayer) &&
		perOwner[iCenterOwner][ALL].size() > 1)
	{
		appendUnitOwnerHeading(szString, eCenterOwner, (int)perOwner[eCenterOwner][ARMY].size(),
				(int)perOwner[eCenterOwner][NAVY].size(), (int)perOwner[eCenterOwner][AIR].size(),
				(int)perOwner[eCenterOwner][ALL].size());
	}
	// Lines required for the center unit
	int iLinesCenter = 2; // The first line may well wrap
	int iLinesCenterShort = 1;
	{
		CvWStringBuffer szTempBuffer;
		setUnitHelp(szTempBuffer, &kCenterUnit, false, false, false, true,
				bIndicator); // advc.007
		CvWString szTemp(szTempBuffer.getCString());
		iLinesCenter += (int)std::count(szTemp.begin(), szTemp.end(), L'\n');
		szTempBuffer.clear();
		setUnitHelp(szTempBuffer, &kCenterUnit, false, true, false, true,
				bIndicator); // advc.007
		szTemp = szTempBuffer.getCString();
		iLinesCenterShort += (int)std::count(szTemp.begin(), szTemp.end(), L'\n');
	}
	if(!szString.isEmpty()) // No newline at the start of PlotListHelp
		szString.append(NEWLINE);
	int iLinesUsed = 1;
	bool const bOmitOwner = (iHeadings >= iOwners);
	if(iTotal + iHeadings + iLinesCenter <= iLineLimit)
	{
		setUnitHelp(szString, &kCenterUnit, false, false, false, bOmitOwner,
				bIndicator); // advc.007
		iLinesUsed = iLinesCenter;
	}
	else if(iTotal + iHeadings + iLinesCenterShort <= iLineLimit)
	{
		setUnitHelp(szString, &kCenterUnit, false, true, false, bOmitOwner,
				bIndicator); // advc.007
		iLinesUsed = iLinesCenterShort;
	}
	else
	{
		setUnitHelp(szString, &kCenterUnit, true, true, false, bOmitOwner,
				bIndicator); // advc.007
	}
	// Show each unit on a separate line (don't aggregate) if there is enough space
	bool bAggregate = false;
	std::set<UnitTypes> perOwnerUnitTypes[iRogueIndex + 1];
	/*  There may not even be enough space for the aggregated info; may have to
		show only a heading with unit counts for some owners. */
	bool abCollapse[iRogueIndex + 1] = { false };
	if(iTotal + iHeadings + iLinesUsed > iLineLimit)
	{
		bAggregate = true;
		int iTotalAggregated = 0;
		for(int i = 0; i <= iRogueIndex; i++)
		{
			for(size_t j = 0; j < perOwner[i][ALL].size(); j++)
			{
				if(perOwner[i][ALL][j] != &kCenterUnit)
					perOwnerUnitTypes[i].insert(perOwner[i][ALL][j]->getUnitType());
			}
			iTotalAggregated += perOwnerUnitTypes[i].size();
		}
		FAssert(iTotalAggregated <= iTotal);
		/*  Select the owner with the smallest number of units (but not the active
			player or rogue) and mark it as collapsed until the (estimated)
			iTotalAggregated is small enough. (implicit selection sort) */
		while(iTotalAggregated + iHeadings + iLinesUsed > iLineLimit +
		/*  This may result in some overlap with the sliders, but at least
			the player can then tell that it's actually necessary to omit
			info. But if the resolution is low, the LineLimit may already
			be too generous. */
			(iScreenHeight > 900 ? 3 : 0))
		{
			int iCollapseIndex = -1;
			uint iMin = MAX_INT;
			for(int i = 0; i < iRogueIndex; i++)
			{
				if(abCollapse[i] || // Important for loop termination
						i == eActivePlayer || i == eCenterOwner)
					continue;
				uint iUnits = perOwner[i][ALL].size();
				// Else too little to be gained by collapsing
				if(iUnits >= 4 && perOwnerUnitTypes[i].size() >= 3)
				{
					if(iUnits < iMin)
					{
						iMin = iUnits;
						iCollapseIndex = i;
					}
				}
			}
			if(iCollapseIndex < 0)
			{
				// Space may still be insufficient, but this can't be helped.
				break;
			}
			abCollapse[iCollapseIndex] = true;
			iTotalAggregated += 1 - (int)perOwnerUnitTypes[iCollapseIndex].size();
		}
	}
	/*  Another selection sort by the number of units per owner. Add a heading
		for each owner and list its units. Special treatment for the owner of the
		center unit (heading already added). */
	bool abDone[iRogueIndex + 1] = { false };
	bool bFirstCollapse = true;
	do
	{
		int iNextIndex = -1;
		if(!abDone[iCenterOwner])
			iNextIndex = iCenterOwner;
		else
		{
			int iMaxPriority = MIN_INT;
			for(int i = 0; i <= iRogueIndex; i++)
			{
				if(abDone[i])
					continue;
				int iPriority = (int)perOwner[i][ALL].size();
				if(iPriority <= 0)
					continue;
				if(abCollapse[i]) // Show collapsed entries last
					iPriority -= 10000;
				if(iPriority > iMaxPriority)
				{
					iMaxPriority = iPriority;
					iNextIndex = i;
				}
			}
		}
		if(iNextIndex < 0)
			break;
		abDone[iNextIndex] = true;
		// If it's just one unit, show the owner on the same line.
		if(perOwner[iNextIndex][ALL].size() == 1)
		{
			if(iNextIndex != iCenterOwner) // Center unit already listed
			{
				if(!szString.isEmpty())
					szString.append(NEWLINE);
				setUnitHelp(szString, perOwner[iNextIndex][ALL][0], true, true,
						false, false, bIndicator); // advc.007
			}
			continue;
		}
		if(iNextIndex != iCenterOwner &&
			iNextIndex <= BARBARIAN_PLAYER) // Can be > when a Spy is in a tile with Barbarians
		{
			appendUnitOwnerHeading(szString, (PlayerTypes)iNextIndex,
					(int)perOwner[iNextIndex][ARMY].size(), (int)perOwner[iNextIndex][NAVY].size(),
					(int)perOwner[iNextIndex][AIR].size(), (int)perOwner[iNextIndex][ALL].size(),
					abCollapse[iNextIndex]);
		}
		if(abCollapse[iNextIndex])
		{
			// Still on the same line as the heading
			if(bFirstCollapse)
			{
				szString.append(NEWLINE);
				szString.append(gDLL->getText("TXT_KEY_MISC_NOT_ENOUGH_SPACE").c_str());
			}
			else szString.append(L"...");
			bFirstCollapse = false;
			continue;
		}
		m_pHelpPlot = &kPlot;
		if(bAggregate)
		{
			std::vector<UnitTypes> unitTypes(perOwnerUnitTypes[iNextIndex].begin(),
					perOwnerUnitTypes[iNextIndex].end());
			std::sort(unitTypes.begin(), unitTypes.end(), listFirstUnitTypeBeforeSecond);
			for(size_t i = 0; i < unitTypes.size(); i++)
			{
				appendUnitTypeAggregated(szString, perOwner[iNextIndex][ALL],
					unitTypes[i], kPlot, bIndicator);
			}
		}
		else
		{
			std::vector<CvUnit const*>& units = perOwner[iNextIndex][ALL];
			std::sort(units.begin(), units.end(), listFirstUnitBeforeSecond);
			for(size_t i = 0; i < units.size(); i++)
			{
				if(units[i] != &kCenterUnit)
				{
					szString.append(NEWLINE);
					setUnitHelp(szString, units[i], true, true, false, true,
							bIndicator); // advc.007
				}
			}
		}
	} while(true);
} // </advc.061>


void CvGameTextMgr::setPlotListHelp(CvWStringBuffer &szString, CvPlot const& kPlot, // advc: was CvPlot*
	bool bOneLine, bool bShort,
	bool bIndicator) // advc.061, advc.007
{
	PROFILE_FUNC();
	TeamTypes const eActiveTeam = getActiveTeam();
	// <advc.opt>
	if(!kPlot.isVisible(eActiveTeam, true))
		return; // </advc.opt>

	if (//(gDLL->getChtLvl() > 0)
		GC.getGame().isDebugMode() &&// advc.135c
		!bIndicator && // advc.007: Don't attach debug info to plot indicators
		GC.ctrlKey())
	{
		/*  advc: Moved into subroutine. (Note: bShort and bOneLine are unused
			in BtS; advc.061 gives bShort a minor use.) */
		setPlotListHelpDebug(szString, kPlot); // display grouping info
		return;
	}
	// <advc.061>
	if(BUGOption::isEnabled("MainInterface__ListUnitsPerOwner", false))
	{
		setPlotListHelpPerOwner(szString, kPlot, bIndicator, bShort);
		return;
	} // </advc.061>

	/*  advc.002b: Was 15; sometimes takes up a bit too much space with increased
		font size. */
	static const uint iMaxNumUnits = 12;
	static std::vector<CvUnit*> apUnits;
	static std::vector<int> aiUnitNumbers;
	static std::vector<int> aiUnitStrength;
	static std::vector<int> aiUnitMaxStrength;
	static std::vector<CvUnit*> plotUnits;

	GC.getGame().getPlotUnits(&kPlot, plotUnits);

	int iNumVisibleUnits = 0;
	if (kPlot.isVisible(eActiveTeam, true))
	{
		FOR_EACH_UNIT_IN(pUnit, kPlot)
		{
			if (pUnit && !pUnit->isInvisible(eActiveTeam, true))
				iNumVisibleUnits++;
		}
	}

	apUnits.erase(apUnits.begin(), apUnits.end());

	int const iPromotionInfos = GC.getNumPromotionInfos();
	if (iNumVisibleUnits > iMaxNumUnits)
	{
		aiUnitNumbers.erase(aiUnitNumbers.begin(), aiUnitNumbers.end());
		aiUnitStrength.erase(aiUnitStrength.begin(), aiUnitStrength.end());
		aiUnitMaxStrength.erase(aiUnitMaxStrength.begin(), aiUnitMaxStrength.end());

		if (m_apbPromotion.empty())
		{
			for (int i = 0; i < (GC.getNumUnitInfos() * MAX_PLAYERS); i++)
			{
				/*	advc (note): The EXE frees this through DeInitialize -
					or so we shall hope ... */
				m_apbPromotion.push_back(new int[iPromotionInfos]);
			}
		}

		for (int i = 0; i < (GC.getNumUnitInfos() * MAX_PLAYERS); i++)
		{
			aiUnitNumbers.push_back(0);
			aiUnitStrength.push_back(0);
			aiUnitMaxStrength.push_back(0);
			for (int j = 0; j < iPromotionInfos; j++)
				m_apbPromotion[i][j] = 0;
		}
	}

	int iCount = 0;
	for (int i = iMaxNumUnits;
		i < iNumVisibleUnits && i < (int)plotUnits.size(); i++)
	{
		CvUnit* pLoopUnit = plotUnits[i];
		if (pLoopUnit == NULL || pLoopUnit == kPlot.getCenterUnit())
			continue;
		apUnits.push_back(pLoopUnit);
		if (iNumVisibleUnits <= iMaxNumUnits)
			continue;
		int iIndex = pLoopUnit->getUnitType() * MAX_PLAYERS + pLoopUnit->getOwner();
		if (aiUnitNumbers[iIndex] == 0)
			iCount++;
		aiUnitNumbers[iIndex]++;
		int iBase = (DOMAIN_AIR == pLoopUnit->getDomainType() ?
				pLoopUnit->airBaseCombatStr() : pLoopUnit->baseCombatStr());
		if (iBase > 0 && pLoopUnit->maxHitPoints() > 0)
		{
			aiUnitMaxStrength[iIndex] += 100 * iBase;
			aiUnitStrength[iIndex] += (100 * iBase * pLoopUnit->currHitPoints()) /
					pLoopUnit->maxHitPoints();
		}
		for (int j = 0; j < iPromotionInfos; j++)
		{
			if (pLoopUnit->isHasPromotion((PromotionTypes)j))
				m_apbPromotion[iIndex][j]++;
		}
	}


	if (iNumVisibleUnits > 0)
	{
		CvUnit* pCenterUnit = kPlot.getCenterUnit(); // advc
		if (pCenterUnit != NULL)
		{
			setUnitHelp(szString, pCenterUnit, iNumVisibleUnits > iMaxNumUnits, true,
					false, false, bIndicator); // advc.007
		}
		uint iNumShown = std::min<uint>(iMaxNumUnits, iNumVisibleUnits);
		for (size_t i = 0; i < iNumShown && i < (int)plotUnits.size(); i++)
		{
			CvUnit* pLoopUnit = plotUnits[i];
			if (pLoopUnit != pCenterUnit)
			{
				szString.append(NEWLINE);
				setUnitHelp(szString, pLoopUnit, true, true,
						false, false, bIndicator); // advc.007
			}
		}
		if(iNumVisibleUnits > iMaxNumUnits)
		{
			//bool bFirst = true;
			FOR_EACH_ENUM(Unit)
			{
				for (int i = 0; i < MAX_PLAYERS; i++)
				{
					int iIndex = eLoopUnit * MAX_PLAYERS + i;
					if (aiUnitNumbers[iIndex] <= 0)
						continue; // advc
					//if (iCount < 5 || bFirst) // advc.002b
					{
						szString.append(NEWLINE);
						//bFirst = false;
					}
					//else szString.append(L", "); // advc.002b
					szString.append(CvWString::format(SETCOLR L"%s" ENDCOLR,
							TEXT_COLOR("COLOR_UNIT_TEXT"),
							GC.getInfo(eLoopUnit).getDescription()));
					// <advc.061> Code moved into a subroutine
					appendAverageStrength(szString, aiUnitMaxStrength[iIndex],
							aiUnitStrength[iIndex], aiUnitNumbers[iIndex]);
					// </advc.061>
					FOR_EACH_ENUM(Promotion)
					{
						if(m_apbPromotion[iIndex][eLoopPromotion] > 0)
						{
							szString.append(CvWString::format(L"%d<img=%S size=16 />",
									m_apbPromotion[iIndex][eLoopPromotion],
									GC.getInfo(eLoopPromotion).getButton()));
						}
					}
					if (i != getActivePlayer() &&
						!GC.getInfo(eLoopUnit).isAnimal() &&
						!GC.getInfo(eLoopUnit).isHiddenNationality())
					{
						szString.append(L", ");
						CvPlayer const& kLoopPlayer = GET_PLAYER((PlayerTypes)i);
						szString.append(CvWString::format(SETCOLR L"%s" ENDCOLR,
								PLAYER_TEXT_COLOR(kLoopPlayer), kLoopPlayer.getName()));
					}
				}
			}
		}
	}
}

namespace
{
	/*	advc: Moved from the top of the file. Only used in setPlotListHelpDebug.
		I guess it was supposed to map FreeListTrashArray ids to e.g. the last
		few digits. I'll just leave it alone. */
	__inline int shortenID(int iId)
	{
		return iId;
	}
}

// advc: Cut from setPlotListHelp; refactored.
void CvGameTextMgr::setPlotListHelpDebug(CvWStringBuffer& szString, CvPlot const& kPlot)
{
	FOR_EACH_UNITAI_IN(pHeadUnit, kPlot)
	{
		// Is this unit the head of a group, not cargo, and visible?
		if(pHeadUnit == NULL || !pHeadUnit->isGroupHead() || pHeadUnit->isCargo())
			continue;
		TeamTypes eActiveTeam = getActiveTeam();
		if(pHeadUnit->isInvisible(eActiveTeam, true))
			continue;
		CvMap const& kMap = GC.getMap();
		CvWString szTempString;
		// head unit name and unitai
		szString.append(CvWString::format(SETCOLR L"%s" ENDCOLR, 255,190,0,255,
				pHeadUnit->getName().GetCString()));
		szString.append(CvWString::format(L" (%d)", shortenID(pHeadUnit->getID())));
		getUnitAIString(szTempString, pHeadUnit->AI_getUnitAIType());
		CvPlayer const& kHeadOwner = GET_PLAYER(pHeadUnit->getOwner());
		szString.append(CvWString::format(SETCOLR L" %s " ENDCOLR,
				PLAYER_TEXT_COLOR(kHeadOwner), szTempString.GetCString()));

		// promotion icons
		FOR_EACH_ENUM(Promotion)
		{
			if (pHeadUnit->isHasPromotion(eLoopPromotion))
			{
				szString.append(CvWString::format(L"<img=%S size=16 />",
						GC.getInfo(eLoopPromotion).getButton()));
			}
		}

		// group
		CvSelectionGroupAI const* pHeadGroup = pHeadUnit->AI_getGroup();
		FAssertMsg(pHeadGroup != NULL, "unit has NULL group");
		if (pHeadGroup->getNumUnits() > 1)
		{
			// BETTER_BTS_AI_MOD, DEBUG, 07/17/09, jdog5000: START
			szString.append(CvWString::format(L"\nGroup:%d [%d units",
					shortenID(pHeadGroup->getID()), pHeadGroup->getNumUnits()));
			if (pHeadGroup->getCargo() > 0)
			{
				szString.append(CvWString::format(L" + %d cargo", pHeadGroup->getCargo()));
			}
			szString.append(CvWString::format(L"]"));

			// get average damage
			int iAverageDamage = 0;
			/*pUnitNode = pHeadGroup->headUnitNode();
			while (pUnitNode != NULL)*/
			// advc.001: ^Looks like an error. We don't want to disrupt the outer loop.
			FOR_EACH_UNIT_IN(pLoopUnit, *pHeadGroup)
			{
				iAverageDamage += (pLoopUnit->getDamage() * pLoopUnit->maxHitPoints()) / 100;
			}
			iAverageDamage /= pHeadGroup->getNumUnits();
			if (iAverageDamage > 0)
				szString.append(CvWString::format(L" %d%%", 100 - iAverageDamage));
		}

		if (!pHeadGroup->isHuman() && pHeadGroup->AI_isStranded())
		{
			szString.append(CvWString::format(SETCOLR L"\n***STRANDED***" ENDCOLR,
					TEXT_COLOR("COLOR_RED")));
		}

		if (!GC.altKey())
		{
			// mission ai
			MissionAITypes eMissionAI = pHeadGroup->AI_getMissionAIType();
			if (eMissionAI != NO_MISSIONAI)
			{
				getMissionAIString(szTempString, eMissionAI);
				szString.append(CvWString::format(SETCOLR L"\n%s" ENDCOLR,
						TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"), szTempString.GetCString()));
			}

			// mission
			MissionTypes eMissionType = (MissionTypes) pHeadGroup->getMissionType(0);
			if (eMissionType != NO_MISSION)
			{
				getMissionTypeString(szTempString, eMissionType);
				szString.append(CvWString::format(SETCOLR L"\n%s" ENDCOLR,
						TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"), szTempString.GetCString()));
			}

			// mission unit
			CvUnit* pMissionUnit = pHeadGroup->AI_getMissionAIUnit();
			if (pMissionUnit != NULL && (eMissionAI != NO_MISSIONAI || eMissionType != NO_MISSION))
			{
				// mission unit
				szString.append(L"\n to ");
				CvPlayer const& kMissionPlayer = GET_PLAYER(pMissionUnit->getOwner());
				szString.append(CvWString::format(SETCOLR L"%s" ENDCOLR,
						PLAYER_TEXT_COLOR(kMissionPlayer), pMissionUnit->getName().GetCString()));
				szString.append(CvWString::format(L"(%d) G:%d", shortenID(pMissionUnit->getID()),
						shortenID(pMissionUnit->getGroupID())));
				getUnitAIString(szTempString, pMissionUnit->AI_getUnitAIType());
				szString.append(CvWString::format(SETCOLR L" %s" ENDCOLR,
						PLAYER_TEXT_COLOR(kMissionPlayer), szTempString.GetCString()));
			}

			// mission plot
			if (eMissionAI != NO_MISSIONAI || eMissionType != NO_MISSION)
			{
				// first try the plot from the missionAI
				CvPlot* pMissionPlot = pHeadGroup->AI_getMissionAIPlot();

				// if MissionAI does not have a plot, get one from the mission itself
				if (pMissionPlot == NULL && eMissionType != NO_MISSION)
				{
					switch (eMissionType)
					{
					case MISSION_MOVE_TO:
					case MISSION_ROUTE_TO:
						pMissionPlot = kMap.plot(pHeadGroup->getMissionData1(0),
								pHeadGroup->getMissionData2(0));
						break;

					case MISSION_MOVE_TO_UNIT:
						if (pMissionUnit != NULL)
							pMissionPlot = pMissionUnit->plot();
						break;
					}
				}

				if (pMissionPlot != NULL)
				{
					szString.append(CvWString::format(L"\n [%d,%d]",
							pMissionPlot->getX(), pMissionPlot->getY()));

					CvCity* pCity = pMissionPlot->getWorkingCity();
					if (pCity != NULL)
					{
						szString.append(L" (");

						if (!pMissionPlot->isCity())
						{
							DirectionTypes eDirection = estimateDirection(
									kMap.dxWrap(pMissionPlot->getX() - pCity->getPlot().getX()),
									kMap.dyWrap(pMissionPlot->getY() - pCity->getPlot().getY()));
							getDirectionTypeString(szTempString, eDirection);
							szString.append(CvWString::format(L"%s of ",
									szTempString.GetCString()));
						}
						CvPlayer const& kCityOwner = GET_PLAYER(pCity->getOwner());
						szString.append(CvWString::format(SETCOLR L"%s" ENDCOLR L")",
								PLAYER_TEXT_COLOR(kCityOwner), pCity->getName().GetCString()));
					}
					else
					{
						if (pMissionPlot != &kPlot)
						{
							DirectionTypes eDirection = estimateDirection(
									kMap.dxWrap(pMissionPlot->getX() - kPlot.getX()),
									kMap.dyWrap(pMissionPlot->getY() - kPlot.getY()));
							getDirectionTypeString(szTempString, eDirection);
							szString.append(CvWString::format(L" (%s)", szTempString.GetCString()));
						}

						PlayerTypes eMissionPlotOwner = pMissionPlot->getOwner();
						if (eMissionPlotOwner != NO_PLAYER)
						{
							CvPlayer const& kMissionPlotOwner = GET_PLAYER(eMissionPlotOwner);
							szString.append(CvWString::format(L", " SETCOLR L"%s" ENDCOLR,
									PLAYER_TEXT_COLOR(kMissionPlotOwner), kMissionPlotOwner.getName()));
						}
					}
				}
			}

			// activity
			ActivityTypes eActivityType = (ActivityTypes)pHeadGroup->getActivityType();
			if (eActivityType != NO_ACTIVITY)
			{
				getActivityTypeString(szTempString, eActivityType);
				// <advc.007> Was always a newline
				if(eMissionAI != NO_MISSIONAI || eMissionType != NO_MISSION)
					szString.append(L", ");
				else szString.append(NEWLINE); // </advc.007>
				szString.append(CvWString::format(SETCOLR L"%s" ENDCOLR,
						TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"), szTempString.GetCString()));
			}
		} // BETTER_BTS_AI_MOD: END
		// BETTER_BTS_AI_MOD, DEBUG, 06/10/08, jdog5000: START
		if(!GC.altKey() && !GC.shiftKey())
		{
			// display cargo for head unit
			std::vector<CvUnit*> aCargoUnits;
			pHeadUnit->getCargoUnits(aCargoUnits);
			for (uint i = 0; i < aCargoUnits.size(); ++i)
			{
				CvUnit* pCargoUnit = aCargoUnits[i];
				if (!pCargoUnit->isInvisible(eActiveTeam, true))
				{
					// name and unitai
					szString.append(CvWString::format(SETCOLR L"\n %s" ENDCOLR,
							TEXT_COLOR("COLOR_ALT_HIGHLIGHT_TEXT"),
							pCargoUnit->getName().GetCString()));
					szString.append(CvWString::format(L"(%d)", shortenID(pCargoUnit->getID())));
					getUnitAIString(szTempString, pCargoUnit->AI_getUnitAIType());
					CvPlayer const& kCargoOwner = GET_PLAYER(pCargoUnit->getOwner());
					szString.append(CvWString::format(SETCOLR L" %s " ENDCOLR,
							PLAYER_TEXT_COLOR(kCargoOwner), szTempString.GetCString()));

					// promotion icons
					FOR_EACH_ENUM(Promotion)
					{
						if (pCargoUnit->isHasPromotion(eLoopPromotion))
						{
							szString.append(CvWString::format(L"<img=%S size=16 />",
									GC.getInfo(eLoopPromotion).getButton()));
						}
					}
				}
			}

			// display grouped units
			FOR_EACH_UNIT_IN(pUnit, kPlot)
			{
				// is this unit not head, in head's group and visible?
				if (pUnit && pUnit != pHeadUnit && pUnit->getGroupID() == pHeadUnit->getGroupID() &&
					!pUnit->isInvisible(eActiveTeam, true))
				{
					FAssertMsg(!pUnit->isCargo(), "unit is cargo but head unit is not cargo");
					// name and unitai
					szString.append(CvWString::format(SETCOLR L"\n-%s" ENDCOLR,
							TEXT_COLOR("COLOR_UNIT_TEXT"), pUnit->getName().GetCString()));
					szString.append(CvWString::format(L" (%d)", shortenID(pUnit->getID())));
					getUnitAIString(szTempString, pUnit->AI_getUnitAIType());
					CvPlayer const& kUnitOwner = GET_PLAYER(pUnit->getOwner());
					szString.append(CvWString::format(SETCOLR L" %s " ENDCOLR,
							PLAYER_TEXT_COLOR(kUnitOwner), szTempString.GetCString()));

					// promotion icons
					FOR_EACH_ENUM(Promotion)
					{

						if (pUnit->isHasPromotion(eLoopPromotion))
						{
							szString.append(CvWString::format(L"<img=%S size=16 />",
									GC.getInfo(eLoopPromotion).getButton()));
						}
					}

					// display cargo for loop unit
					std::vector<CvUnit*> aLoopCargoUnits;
					pUnit->getCargoUnits(aLoopCargoUnits);
					for (uint i = 0; i < aLoopCargoUnits.size(); i++)
					{
						CvUnit* pCargoUnit = aLoopCargoUnits[i];
						if (!pCargoUnit->isInvisible(eActiveTeam, true))
						{
							// name and unitai
							szString.append(CvWString::format(SETCOLR L"\n %s" ENDCOLR,
									TEXT_COLOR("COLOR_ALT_HIGHLIGHT_TEXT"),
									pCargoUnit->getName().GetCString()));
							szString.append(CvWString::format(L"(%d)",
									shortenID(pCargoUnit->getID())));
							getUnitAIString(szTempString, pCargoUnit->AI_getUnitAIType());
							CvPlayer const& kCargoOwner = GET_PLAYER(pCargoUnit->getOwner());
							szString.append(CvWString::format(SETCOLR L" %s " ENDCOLR,
									PLAYER_TEXT_COLOR(kCargoOwner), szTempString.GetCString()));

							// promotion icons
							FOR_EACH_ENUM(Promotion)
							{
								if (pCargoUnit->isHasPromotion(eLoopPromotion))
								{
									szString.append(CvWString::format(L"<img=%S size=16 />",
											GC.getInfo(eLoopPromotion).getButton()));
								}
							}
						}
					}
				}
			}
		}

		if(!GC.altKey() && (kPlot.getTeam() == NO_TEAM ||
				GET_TEAM(pHeadGroup->getTeam()).isAtWar(kPlot.getTeam())))
		{
			szString.append(NEWLINE);
			CvWString szTempBuffer;
			CvPlayerAI const& kOwner = GET_PLAYER(pHeadGroup->getOwner());

			//AI strategies  // advc.007: bDebug=true added so that human strategies are displayed
			if (kOwner.AI_isDoStrategy(AI_STRATEGY_DAGGER, true))
			{
				szTempBuffer.Format(L"Dagger, ");
				szString.append(szTempBuffer);
			}
			if (kOwner.AI_isDoStrategy(AI_STRATEGY_CRUSH, true))
			{
				szTempBuffer.Format(L"Crush, ");
				szString.append(szTempBuffer);
			}
			if (kOwner.AI_isDoStrategy(AI_STRATEGY_ALERT1, true))
			{
				szTempBuffer.Format(L"Alert1, ");
				szString.append(szTempBuffer);
			}
			if (kOwner.AI_isDoStrategy(AI_STRATEGY_ALERT2, true))
			{
				szTempBuffer.Format(L"Alert2, ");
				szString.append(szTempBuffer);
			}
			if (kOwner.AI_isDoStrategy(AI_STRATEGY_TURTLE, true))
			{
				szTempBuffer.Format(L"Turtle, ");
				szString.append(szTempBuffer);
			}
			if (kOwner.AI_isDoStrategy(AI_STRATEGY_LAST_STAND, true))
			{
				szTempBuffer.Format(L"Last Stand, ");
				szString.append(szTempBuffer);
			}
			if (kOwner.AI_isDoStrategy(AI_STRATEGY_FINAL_WAR, true))
			{
				szTempBuffer.Format(L"FinalWar, ");
				szString.append(szTempBuffer);
			}
			if (kOwner.AI_isDoStrategy(AI_STRATEGY_GET_BETTER_UNITS, true))
			{
				szTempBuffer.Format(L"GetBetterUnits, ");
				szString.append(szTempBuffer);
			}
			if (kOwner.AI_isDoStrategy(AI_STRATEGY_FASTMOVERS, true))
			{
				szTempBuffer.Format(L"FastMovers, ");
				szString.append(szTempBuffer);
			}
			if (kOwner.AI_isDoStrategy(AI_STRATEGY_LAND_BLITZ, true))
			{
				szTempBuffer.Format(L"LandBlitz, ");
				szString.append(szTempBuffer);
			}
			if (kOwner.AI_isDoStrategy(AI_STRATEGY_AIR_BLITZ, true))
			{
				szTempBuffer.Format(L"AirBlitz, ");
				szString.append(szTempBuffer);
			}
			if (kOwner.AI_isDoStrategy(AI_STRATEGY_OWABWNW, true))
			{
				szTempBuffer.Format(L"OWABWNW, ");
				szString.append(szTempBuffer);
			}
			if (kOwner.AI_isDoStrategy(AI_STRATEGY_PRODUCTION, true))
			{
				szTempBuffer.Format(L"Production, ");
				szString.append(szTempBuffer);
			}
			if (kOwner.AI_isDoStrategy(AI_STRATEGY_MISSIONARY, true))
			{
				szTempBuffer.Format(L"Missionary, ");
				szString.append(szTempBuffer);
			}
			if (kOwner.AI_isDoStrategy(AI_STRATEGY_BIG_ESPIONAGE, true))
			{
				szTempBuffer.Format(L"BigEspionage, ");
				szString.append(szTempBuffer);
			}
			if (kOwner.AI_isDoStrategy(AI_STRATEGY_ECONOMY_FOCUS, true)) // K-Mod
			{
				szTempBuffer.Format(L"EconomyFocus, ");
				szString.append(szTempBuffer);
			}
			if (kOwner.AI_isDoStrategy(AI_STRATEGY_ESPIONAGE_ECONOMY, true)) // K-Mod
			{
				szTempBuffer.Format(L"EspionageEconomy, ");
				szString.append(szTempBuffer);
			}
			CvArea const& kArea = kPlot.getArea();
			//Area battle plans.
			switch(kArea.getAreaAIType(pHeadGroup->getTeam())) {
			case AREAAI_OFFENSIVE:
				szTempBuffer.Format(L"\n Area AI = OFFENSIVE"); break;
			case AREAAI_DEFENSIVE:
				szTempBuffer.Format(L"\n Area AI = DEFENSIVE"); break;
			case AREAAI_MASSING:
				szTempBuffer.Format(L"\n Area AI = MASSING"); break;
			case AREAAI_ASSAULT:
				szTempBuffer.Format(L"\n Area AI = ASSAULT"); break;
			case AREAAI_ASSAULT_MASSING:
				szTempBuffer.Format(L"\n Area AI = ASSAULT_MASSING"); break;
			case AREAAI_NEUTRAL:
				szTempBuffer.Format(L"\n Area AI = NEUTRAL"); break;
			default: szTempBuffer.Format(L"\n Unknown Area AI type"); break;
			}
			CvCity const* pTargetCity = kArea.AI_getTargetCity(pHeadGroup->getOwner());
			if(pTargetCity != NULL)
			{
				szString.append(CvWString::format(L"\nTarget City: %s (%d)",
						pTargetCity->getName().c_str(), pTargetCity->getOwner()));
			}
			else szString.append(CvWString::format(L"\nTarget City: None"));

			if(GC.shiftKey())
			{	// advc: unused
				/*int iBestTargetValue = (pTargetCity != NULL ?
						GET_PLAYER(pHeadGroup->getOwner()).
						AI_targetCityValue(pTargetCity,false,true) : 0);*/
				szString.append(CvWString::format(L"\n\nTarget City values:\n"));
				for(int iPlayer = 0; iPlayer < MAX_PLAYERS; iPlayer++)
				{
					CvPlayer const& pl = GET_PLAYER((PlayerTypes)iPlayer);
					if(GET_TEAM(pHeadGroup->getTeam()).AI_getWarPlan(pl.getTeam()) == NO_WARPLAN)
						continue;
					if(kArea.getCitiesPerPlayer((PlayerTypes)iPlayer) <= 0)
						continue;
					FOR_EACH_CITY(pLoopCity, pl)
					{
						if(pLoopCity->isArea(kArea) &&
							// advc.001:
							GET_TEAM(pHeadGroup->getTeam()).AI_deduceCitySite(*pLoopCity))
						{
							int iTargetValue = GET_PLAYER(pHeadGroup->getOwner()).
									AI_targetCityValue(*pLoopCity,false,true);
							if((kMap.calculatePathDistance(&kPlot, pLoopCity->plot()) < 20))
							{
								szString.append(CvWString::format(L"\n%s : %d + rand %d",
										pLoopCity->getName().c_str(), iTargetValue,
										pLoopCity->getPopulation() / 2));
							}
						}
					}
				}
			}
		} // BETTER_BTS_AI_MOD: END
		// advc.007: No newlines in the final iteration
		if (pHeadUnit->getIDInfo() != kPlot.tailUnitNode()->m_data)
		{
			// double space non-empty groups
			if (pHeadGroup->getNumUnits() > 1 || pHeadUnit->hasCargo())
				szString.append(NEWLINE);
			szString.append(NEWLINE);
		}
	}
}

// advc.004c:
namespace
{
	CvUnit const* bestInterceptor(CvUnit const& kUnit, CvPlot const& kMissionPlot,
		scaled& rOdds)
	{
		rOdds = 0;
		int const iEvasionPercent = kUnit.evasionProbability();
		if (iEvasionPercent >= 100)
			return NULL;
		scaled const rEvasionProb = per100(iEvasionPercent);
		CvUnit const* pInterceptor = kUnit.bestInterceptor(kMissionPlot, true);
		if (pInterceptor != NULL)
		{
			rOdds = per100(pInterceptor->currInterceptionProbability()) *
					(1 - rEvasionProb);
		}
		return pInterceptor;
	}
}

// advc.004c
void CvGameTextMgr::setInterceptPlotHelp(CvPlot const& kPlot, CvUnit const& kUnit,
	CvWString& szHelp, bool bNewline)
{
	scaled rInterceptProb;
	CvUnit const* pBestInterceptor = bestInterceptor(kUnit, kPlot, rInterceptProb);
	if (rInterceptProb > 0 && pBestInterceptor != NULL)
	{
		CvWStringBuffer szBuffer;
		setUnitHelp(szBuffer, pBestInterceptor, true, true, true);
		int iPercent = std::max(1, rInterceptProb.getPercent());
		// Don't show uncertain outcome as certain
		if (iPercent == 100 && rInterceptProb < 1)
			iPercent--;
		FAssert(iPercent <= 100);
		szHelp.append(gDLL->getText("TXT_KEY_AIR_MODE_INTERCEPT", iPercent,
				szBuffer.getCString()));
		if (gDLL->UI().getLengthSelectionList() > 1)
		{	// Say who is getting intercepted if multiple selected
			szBuffer.clear();
			setUnitHelp(szBuffer, &kUnit, true, true, true, true);
			szHelp.append(gDLL->getText("TXT_KEY_AIR_MODE_INTERCEPT_VERSUS",
					szBuffer.getCString()));
		}
		if (bNewline)
			szHelp.append(NEWLINE);
	}
}

/*	K-Mod note: this function can change the center unit on the plot.
	(because of a change I made)
	Also, I've made some unmarked structural changes to this function
	to make it easier to read and to fix a few minor bugs.
	advc.010: Now returns true only if unit capture help was given.
	(All callers had previously ignored the return value, which had said
	whether any help was given.) */
bool CvGameTextMgr::setCombatPlotHelp(CvWStringBuffer& szString, CvPlot* pPlot)
{
	PROFILE_FUNC();
	bool const ACO_enabled = BUGOption::isEnabled("ACO__Enabled", false);
	bool const bShift = GC.shiftKey();
	bool const bForceHostile = GC.altKey();
	// advc.048:
	int iLengthSelectionList = gDLL->UI().getLengthSelectionList();
	if (iLengthSelectionList <= 0)
		return false;
	// advc.048:
	CvSelectionGroupAI const& kSelectionList = gDLL->UI().getSelectionList()->AI();
	bool bValid = false;
	switch (kSelectionList.getDomainType())
	{
	case DOMAIN_SEA:
		bValid = pPlot->isWater();
		break;
	case DOMAIN_AIR:
		bValid = true;
		break;
	case DOMAIN_LAND:
		bValid = !pPlot->isWater();
		break;
	case DOMAIN_IMMOBILE:
		break;
	default:
		FAssert(false);
	}
	if (!bValid)
		return false;

	bool const bMaxSurvival = bForceHostile; // advc.048
	int iOddsDummy=-1;
	CvUnit* pAttacker = kSelectionList.AI_getBestGroupAttacker(pPlot, false, iOddsDummy,
			false, false, !bMaxSurvival, bMaxSurvival); // advc.048
	if (pAttacker == NULL)
	{
		pAttacker = kSelectionList.AI_getBestGroupAttacker(pPlot, false, iOddsDummy,
				true, // bypass checks for moves and war etc.
				false, !bMaxSurvival, bMaxSurvival); // advc.048
	}
	if (pAttacker == NULL)
		return false;

	CvUnit* pDefender = pPlot->getBestDefender(NO_PLAYER,
			pAttacker->getOwner(), pAttacker, !bForceHostile);
	// <advc.089>
	if (pDefender == NULL)
	{
		CvPlot::DefenderFilters defFilters(pAttacker->getOwner(), pAttacker,
				!bForceHostile);
		defFilters.m_bTestCanAttack = false;
		pDefender = pPlot->getBestDefender(NO_PLAYER, defFilters);
		if (pDefender != NULL)
		{
			setCannotAttackHelp(szString, *pAttacker, *pDefender);
			return false;
		}
	} // </advc.089>
	// <advc.010> Show capture help if war not yet declared even w/o bForceHostiley
	bool bCaptureHelpOnly = false;
	if (pDefender == NULL)
	{
		pDefender = pPlot->getBestDefender(NO_PLAYER, pAttacker->getOwner(), pAttacker);
		if (pDefender != NULL)
			bCaptureHelpOnly = true;
		else return false;
	} // </advc.010>
	if (!pAttacker->canAttack(*pDefender))
		return false;
	// doc: can defend against attacker
	if (!pDefender->canDefendAgainst(pAttacker, pPlot))
	{
		//return false;
		// <advc.010>
		/*	(Would be nice to show capture help also when
			pPlot->getNumVisibleEnemyDefenders()==1
			i.e. when there is a proper defender and the attacker's victory will
			immediately result in a captive. However, this gets too complicated
			b/c there could be multiple captives. If the best defender itself
			can be captured, then it's clear enough that the capture help refers
			only to that one unit.) */
		if (pAttacker->isNoUnitCapture())
			return false;
		UnitTypes const eCaptive = pDefender->getCaptureUnitType(
				GET_PLAYER(pAttacker->getOwner()).getCivilizationType());
		if (eCaptive == NO_UNIT)
			return false;
		int const iCaptureOdds = pAttacker->getCaptureOdds(*pDefender);
		int const iBaseOdds = GC.getDefineINT(CvGlobals::BASE_UNIT_CAPTURE_CHANCE);
		if (iCaptureOdds == iBaseOdds && (iBaseOdds <= 0 || iBaseOdds >= 100))
			return false;
		CvWString szOdds;
		szOdds.Format(SETCOLR L"%d%%" ENDCOLR, TEXT_COLOR(iCaptureOdds > 0 ?
				(iCaptureOdds >= 50 ? "COLOR_POSITIVE_TEXT" : "COLOR_YELLOW") :
				"COLOR_NEGATIVE_TEXT"), iCaptureOdds);
		szString.append(gDLL->getText(pDefender->getUnitType() == eCaptive ?
				"TXT_KEY_MISC_UNIT_CAPTURE_ODDS" :
				"TXT_KEY_MISC_UNIT_CAPTURE_ODDS_REPL",
				GC.getInfo(eCaptive).getDescription(), szOdds.c_str()));
		if (iCaptureOdds != iBaseOdds &&
			iCaptureOdds == GC.getDefineINT(CvGlobals::DOW_UNIT_CAPTURE_CHANCE) &&
			(GET_TEAM(pAttacker->getTeam()).hasJustDeclaredWar(pDefender->getTeam()) ||
			!GET_TEAM(pAttacker->getTeam()).isAtWar(pDefender->getTeam())))
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_MISC_NO_DOW_UNIT_CAPTURE"));
		}
		return true; // </advc.010>
	}
	// <advc.010>
	if (bCaptureHelpOnly)
		return false; // </advc.010>
	// <advc.048>
	bool bBestOddsHelp = false;
	if (!bMaxSurvival && GC.getDefineINT("GROUP_ATTACK_BEST_ODDS_HELP") > 0)
	{
		CvUnit* pBestOddsAttacker = kSelectionList.AI_getBestGroupAttacker(pPlot, false, iOddsDummy,
				false, false, false, true);
		if (pBestOddsAttacker == NULL)
		{
			pBestOddsAttacker = kSelectionList.AI_getBestGroupAttacker(pPlot, false, iOddsDummy,
					true, false, false, true);
		}
		if (pBestOddsAttacker != pAttacker)
			bBestOddsHelp = true;
	}
	if (!ACO_enabled && bBestOddsHelp)
	{
		szString.append(gDLL->getText("TXT_KEY_GROUP_ATTACK_BEST_ODDS_HELP"));
		szString.append(NEWLINE);
	} // </advc.048>

	/*	K-Mod. If the plot's center unit isn't one of our own units,
		then use this defender as the plot's center unit.
		With this, the map will accurately show who we're up against. */
	if (gDLL->UI().getSelectionPlot() != pPlot)
	{
		if (pDefender->isActiveOwned() ||
			// I don't think this is possible... but it's pretty cheap to check.
			pPlot->getCenterUnit() == NULL ||
			!pPlot->getCenterUnit()->isActiveOwned())
		{
			pPlot->setCenterUnit(pDefender);
		}

	} // K-Mod end
	// <advc.004c>
	if (pAttacker->getDomainType() == DOMAIN_AIR)
	{
		if (!szString.isEmpty())
			szString.append(NEWLINE);
		CvWString szInterceptHelp;
		setInterceptPlotHelp(*pPlot, *pAttacker, szInterceptHelp, false);
		szString.append(szInterceptHelp);
	} // <advc.004c>
	int iACOView = 0;
	if (ACO_enabled)
	{
		iACOView = (GC.shiftKey() ? 2 : 1);
		if (BUGOption::isEnabled("ACO__SwapViews", false))
			iACOView = 3 - iACOView; //swaps 1 and 2.
	}
	if (pAttacker->getDomainType() != DOMAIN_AIR)
	{
		int const iCombatOdds = calculateCombatOdds(*pAttacker, *pDefender);
		bool bVictoryOddsAppended = false; // advc.048
		if (pAttacker->combatLimit() >= GC.getMAX_HIT_POINTS())
		{
			if (!ACO_enabled || BUGOption::isEnabled("ACO__ForceOriginalOdds", false))
			{
				CvWString szTempBuffer;
				if (iCombatOdds > 999)
					szTempBuffer = L"&gt; 99.9";
				else if (iCombatOdds < 1)
					szTempBuffer = L"&lt; 0.1";
				else szTempBuffer.Format(L"%.1f", iCombatOdds / 10.0f);
				szString.append(gDLL->getText("TXT_KEY_COMBAT_PLOT_ODDS",
						szTempBuffer.GetCString()));
				bVictoryOddsAppended = true; // advc.048
				if (ACO_enabled)
					szString.append(NEWLINE);
			}
		}

		int iWithdrawal = 0;
		// doc: combat limit against defender
		if (pAttacker->combatLimitAgainst(pDefender) < GC.getMAX_HIT_POINTS())
			iWithdrawal += 100 * iCombatOdds;
		iWithdrawal += std::min(100, pAttacker->withdrawalProbability()) *
				(1000 - iCombatOdds);
		// doc: combat limit against defender
		if (iWithdrawal > 0 || pAttacker->combatLimitAgainst(pDefender) < GC.getMAX_HIT_POINTS())
		{
			if (!ACO_enabled || BUGOption::isEnabled("ACO__ForceOriginalOdds", false))
			{
				CvWString szTempBuffer;
				if (iWithdrawal > 99900)
					szTempBuffer = L"&gt; 99.9";
				else if (iWithdrawal < 100)
					szTempBuffer = L"&lt; 0.1";
				else szTempBuffer.Format(L"%.1f", iWithdrawal / 1000.0f);
				if(bVictoryOddsAppended) // advc.048
					szString.append(NEWLINE);
				szString.append(gDLL->getText("TXT_KEY_COMBAT_PLOT_ODDS_RETREAT", szTempBuffer.GetCString()));
				if (ACO_enabled)
					szString.append(NEWLINE);
			}
		}

		//szTempBuffer.Format(L"AI odds: %d%%", iOdds);
		//szString += NEWLINE + szTempBuffer;

		// TODO: move modifiers to right method
		// Leoreth
		if (pPlot->isPlains())
		{
			iModifier = pDefender->plainsDefenseModifier();

			if (iModifier != 0)
			{
				szString.append(NEWLINE);
				szString.append(gDLL->getText("TXT_KEY_COMBAT_PLOT_PLAINS_MOD", iModifier));
			}
		}
		// Leoreth
		if (pPlot->isPlains())
		{
			iModifier = pDefender->plainsDefenseModifier();

			if (iModifier != 0)
			{
				szString.append(NEWLINE);
				szString.append(gDLL->getText("TXT_KEY_COMBAT_PLOT_PLAINS_MOD", iModifier));
			}
		}
		// Leoreth
		if (!pPlot->isCity() && pPlot->isRiver() && pAttacker->plot()->isRiver())
		{
			iModifier = pAttacker->riverAttackModifier();

			if (iModifier != 0)
			{
				szString.append(NEWLINE);
				szString.append(gDLL->getText("TXT_KEY_COMBAT_PLOT_EXTRA_RIVER_MOD", -iModifier));
			}
		}
		// Leoreth: Vietnamese UP
		if (pAttacker->getCivilizationType() == VIETNAM && pAttacker->getOwnerINLINE() == pPlot->getOwnerINLINE())
		{
			if (!pAttacker->noDefensiveBonus())
			{
				iModifier = pAttacker->plot()->defenseModifier(pAttacker->getTeam(), pDefender->ignoreBuildingDefense());

				if (iModifier != 0)
				{
					szString.append(NEWLINE);
					szString.append(gDLL->getText("TXT_KEY_COMBAT_PLOT_TILE_MOD", -iModifier));
				}
			}

			iModifier = pAttacker->fortifyModifier();

			if (iModifier != 0)
			{
				szString.append(NEWLINE);
				szString.append(gDLL->getText("TXT_KEY_COMBAT_PLOT_FORTIFY_MOD", -iModifier));
			}

			if (pAttacker->plot()->isCity(true, pAttacker->getTeam()))
			{
				iModifier = pAttacker->cityDefenseModifier();

				if (iModifier != 0)
				{
					szString.append(NEWLINE);
					szString.append(gDLL->getText("TXT_KEY_COMBAT_PLOT_CITY_MOD", -iModifier));
				}
			}

			if (pAttacker->plot()->isHills())
			{
				iModifier = pAttacker->hillsDefenseModifier();

				if (iModifier != 0)
				{
					szString.append(NEWLINE);
					szString.append(gDLL->getText("TXT_KEY_COMBAT_PLOT_HILLS_MOD", -iModifier));
				}
			}

			// Leoreth
			if (pAttacker->plot()->isPlains())
			{
				iModifier = pAttacker->plainsDefenseModifier();

				if (iModifier != 0)
				{
					szString.append(NEWLINE);
					szString.append(gDLL->getText("TXT_KEY_COMBAT_PLOT_PLAINS_MOD", -iModifier));
				}
			}

			if (pAttacker->plot()->getFeatureType() != NO_FEATURE)
			{
				iModifier = pAttacker->featureDefenseModifier(pAttacker->plot()->getFeatureType());

				if (iModifier != 0)
				{
					szString.append(NEWLINE);
					szString.append(gDLL->getText("TXT_KEY_COMBAT_PLOT_UNIT_MOD", -iModifier, GC.getFeatureInfo(pAttacker->plot()->getFeatureType()).getTextKeyWide()));
				}
			}

			if (pAttacker->plot()->getFeatureType() == NO_FEATURE || GC.getFeatureInfo(pAttacker->plot()->getFeatureType()).getDefenseModifier() == 0)
			{
				iModifier = pAttacker->terrainDefenseModifier(pAttacker->plot()->getTerrainType());

				if (iModifier != 0)
				{
					szString.append(NEWLINE);
					szString.append(gDLL->getText("TXT_KEY_COMBAT_PLOT_UNIT_MOD", -iModifier, GC.getTerrainInfo(pAttacker->plot()->getTerrainType()).getTextKeyWide()));
				}
			}
		}
		// Leoreth
		if (pPlot->isPlains())
		{
			iModifier = pAttacker->plainsAttackModifier();

			if (iModifier != 0)
			{
				szString.append(NEWLINE);
				szString.append(gDLL->getText("TXT_KEY_COMBAT_PLOT_PLAINS_MOD", iModifier));
			}
		}
		// Leoreth
		if (!pPlot->isCity() && pPlot->isRiver() && pAttacker->plot()->isRiver())
		{
			iModifier = pAttacker->riverAttackModifier();

			if (iModifier != 0)
			{
				szString.append(NEWLINE);
				szString.append(gDLL->getText("TXT_KEY_COMBAT_PLOT_EXTRA_RIVER_MOD", iModifier));
			}
		}
		// TODO: different preconditions
		if (pPlot->getFeatureType() != NO_FEATURE)
		{
			iModifier = pAttacker->featureAttackModifier(pPlot->getFeatureType());

			if (iModifier != 0)
			{
				szString.append(NEWLINE);
				szString.append(gDLL->getText("TXT_KEY_COMBAT_PLOT_UNIT_MOD", iModifier, GC.getFeatureInfo(pPlot->getFeatureType()).getTextKeyWide()));
			}
		}
		else
		{
			iModifier = pAttacker->terrainAttackModifier(pPlot->getTerrainType());

			if (iModifier != 0)
			{
				szString.append(NEWLINE);
				szString.append(gDLL->getText("TXT_KEY_COMBAT_PLOT_UNIT_MOD", iModifier, GC.getTerrainInfo(pPlot->getTerrainType()).getTextKeyWide()));
			}
		}
		// Leoreth
		if (pPlot->isPlains())
		{
			iModifier = pDefender->plainsDefenseModifier();

			if (iModifier != 0)
			{
				szString.append(NEWLINE);
				szString.append(gDLL->getText("TXT_KEY_COMBAT_PLOT_PLAINS_MOD", iModifier));
			}
		}
		// TODO: different conditions
		if (pPlot->getFeatureType() != NO_FEATURE)
		{
			iModifier = pDefender->featureDefenseModifier(pPlot->getFeatureType());

			if (iModifier != 0)
			{
				szString.append(NEWLINE);
				szString.append(gDLL->getText("TXT_KEY_COMBAT_PLOT_UNIT_MOD", iModifier, GC.getFeatureInfo(pPlot->getFeatureType()).getTextKeyWide()));
			}
		}
		// TODO: different conditions
		if (pPlot->getFeatureType() == NO_FEATURE || GC.getFeatureInfo(pPlot->getFeatureType()).getDefenseModifier() == 0)
		{
			iModifier = pDefender->terrainDefenseModifier(pPlot->getTerrainType());

			if (iModifier != 0)
			{
				szString.append(NEWLINE);
				szString.append(gDLL->getText("TXT_KEY_COMBAT_PLOT_UNIT_MOD", iModifier, GC.getTerrainInfo(pPlot->getTerrainType()).getTextKeyWide()));
			}
		}

		if (ACO_enabled)
		{	// advc: Moved into subroutine
			setACOPlotHelp(szString, *pPlot, *pAttacker, *pDefender, iACOView,
					bBestOddsHelp); // advc.048
		}
	}
	if (ACO_enabled)
	{	// advc: Moved into subroutine
		setACOModifiersPlotHelp(szString, *pPlot, *pAttacker, *pDefender, iACOView);
	}
	else
	{	// <advc.048>
		if(iLengthSelectionList > 1)
		{
			if (!szString.isEmpty())
				szString.append(NEWLINE);
			setUnitHelp(szString, pAttacker, true, true, true);
		} // </advc.048>
		CvWString szOffenseOdds;
		szOffenseOdds.Format(L"%.2f", pAttacker->getDomainType() == DOMAIN_AIR ?
				pAttacker->airCurrCombatStrFloat(pDefender) :
				pAttacker->currCombatStrFloat(NULL, NULL));
		CvWString szDefenseOdds;
		szDefenseOdds.Format(L"%.2f", pDefender->currCombatStrFloat(pPlot, pAttacker));
		if (!szString.isEmpty()) // advc.001: for right click hover with air unit
			szString.append(NEWLINE);
		szString.append(gDLL->getText("TXT_KEY_COMBAT_PLOT_ODDS_VS",
				szOffenseOdds.GetCString(), szDefenseOdds.GetCString()));
		/*	<advc.048> BtS code replaced with functions shared with ACO.
			Also: show the generic modifier of the attacker upfront,
			then the name of the defending unit, then the rest of the modifiers
			-- like ACO does it too. */
		appendCombatModifiers(szString, *pPlot, *pAttacker, *pDefender,
				true, false, true);
		appendFirstStrikes(szString, *pAttacker, *pDefender, false);
		szString.append(NEWLINE);
		szString.append(gDLL->getText("TXT_KEY_MISC_VS"));
		szString.append(L" ");
		setUnitHelp(szString, pDefender, true, true, true);
		appendCombatModifiers(szString, *pPlot, *pAttacker, *pDefender,
				true, false, false, true);
		// Commented out (not sure if it had been shown in COLOR_NEGATIVE ...)
		/*if (pAttacker->isHurt()) {
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_COMBAT_PLOT_HP", pAttacker->currHitPoints(), pAttacker->maxHitPoints()));
		}*/
		appendCombatModifiers(szString, *pPlot, *pAttacker, *pDefender,
				false, false);
		appendFirstStrikes(szString, *pDefender, *pAttacker, true);
		// Commented out: </advc.048>
		/*if (pDefender->isHurt()) {
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_COMBAT_PLOT_HP", pDefender->currHitPoints(), pDefender->maxHitPoints()));
		}*/
	}

	szString.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));

	//if ((gDLL->getChtLvl() > 0))
	// BBAI: Only display this info in debug mode so game can be played with cheat code entered
	if (GC.getGame().isDebugMode() &&
		bShift) // advc.007
	{
		CvWString szTempBuffer;
		szTempBuffer.Format(L"\nStack Compare Value = %d",
				kSelectionList.AI_compareStacks(pPlot,
				false, true)); // advc.001n
		szString.append(szTempBuffer);

		if (pPlot->getPlotCity() != NULL)
		{
			szTempBuffer.Format(L"\nBombard turns = %d",
					kSelectionList.AI_getBombardTurns(pPlot->getPlotCity()));
			szString.append(szTempBuffer);
		}

		const CvPlayerAI& kPlayer = GET_PLAYER(getActivePlayer());
		int iOurStrengthDefense = kPlayer.AI_localDefenceStrength(
				pPlot, kPlayer.getTeam(), DOMAIN_LAND, 1, true, true, true);
		int iOurStrengthOffense = kPlayer.AI_localAttackStrength(
				pPlot, kPlayer.getTeam(), DOMAIN_LAND, 1, false, true, false);
		szTempBuffer.Format(L"\nPlot Strength(Ours)= d%d, o%d",
				iOurStrengthDefense, iOurStrengthOffense);
		szString.append(szTempBuffer);
		int iEnemyStrengthDefense = kPlayer.AI_localDefenceStrength(
				pPlot, NO_TEAM, DOMAIN_LAND, 1, true, true, true);
		int iEnemyStrengthOffense = kPlayer.AI_localAttackStrength(
				pPlot, NO_TEAM, DOMAIN_LAND, 1, false, true, false);
		szTempBuffer.Format(L"\nPlot Strength(Enemy)= d%d, o%d",
				iEnemyStrengthDefense, iEnemyStrengthOffense);
		szString.append(szTempBuffer);
	}

	szString.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));

	//return true;
	return false; // advc.010: see comment on top
}

/*	advc.089: Help text for the conditions checked by CvUnit::canAttack.
	Only damage limit so far. */
void CvGameTextMgr::setCannotAttackHelp(CvWStringBuffer& szHelp,
	CvUnit const& kAttacker, CvUnit const& kDefender)
{
	// List the units upfront (can't attack any of these)
	setPlotListHelp(szHelp, *kDefender.plot(), true, true);
	int iLimit = std::max(kAttacker.combatLimit(), kAttacker.airCombatLimit());
	if (kDefender.getDamage() < iLimit)
	{
		if (!kDefender.canFight() && kAttacker.combatLimit() < 100 &&
			kDefender.getPlot().plotCheck(PUF_isEnemy, kAttacker.getOwner(), false,
			NO_PLAYER, NO_TEAM, PUF_canDefend) != NULL)
		{
			iLimit = kAttacker.combatLimit();
		}
		else return;
	}
	if (kDefender.getDamage() >= iLimit)
	{
		if (!szHelp.isEmpty())
			szHelp.append(NEWLINE);
		szHelp.append(gDLL->getText("TXT_KEY_DAMAGE_LIMIT_REACHED", iLimit));
	}
}


/*namespace {
// DO NOT REMOVE - needed for font testing - Moose
void createTestFontString(CvWStringBuffer& szString)
{
	//	advc: Will have to restore this from BtS if it is indeed ever needed.
	//	Contains non-ASCII string literals that seem to trip up my Git merge tool.
} }*/

void CvGameTextMgr::setPlotHelp(CvWStringBuffer& szString, CvPlot const& kPlot)
{
	bool const bShift = GC.shiftKey();
	CvGame const& kGame = GC.getGame();
	// <advc.135c>
	if (kGame.isDebugMode())
	{
		setPlotHelpDebug(szString, kPlot);
		if (bShift || GC.ctrlKey() || GC.altKey())
			return;
	} // </advc.135c>

	TeamTypes const eActiveTeam = getActiveTeam();
	PlayerTypes const eActivePlayer = getActivePlayer();
	CvWString szTempBuffer;

    // doc: stability
	if (!pPlot->isWater())
	{
		if (pPlot->isCore(eActivePlayer))
		{
			szTempBuffer.append(CvWString::format(SETCOLR, TEXT_COLOR("COLOR_STABILITY_CORE")));
			szTempBuffer.append(gDLL->getText("TXT_KEY_STABILITY_CORE_AREA"));
		}
		else if (pPlot->getSettlerValue(eActivePlayer) > 0)
		{
			szTempBuffer.append(CvWString::format(SETCOLR, TEXT_COLOR("COLOR_STABILITY_HISTORICAL")));
			szTempBuffer.append(gDLL->getText("TXT_KEY_STABILITY_HISTORICAL_AREA"));
		}
		else if (pPlot->getWarValue(eActivePlayer) > 1)
		{
			szTempBuffer.append(CvWString::format(SETCOLR, TEXT_COLOR("COLOR_STABILITY_CONQUEST")));
			szTempBuffer.append(gDLL->getText("TXT_KEY_STABILITY_CONQUEST_AREA"));
		}
		else
		{
			szTempBuffer.append(CvWString::format(SETCOLR, TEXT_COLOR("COLOR_STABILITY_FOREIGN")));
			szTempBuffer.append(gDLL->getText("TXT_KEY_STABILITY_FOREIGN_AREA"));
		}

        szTempBuffer.append(CvWString::format( ENDCOLR ));
        szTempBuffer.append(NEWLINE);
    }

	// doc: victory
	CvWString victoryTooltip;
	CyArgsList victoryTooltipArgs;

	victoryTooltipArgs.add(eActivePlayer);
	victoryTooltipArgs.add(pPlot->getX());
	victoryTooltipArgs.add(pPlot->getY());

	gDLL->getPythonIFace()->callFunction(PYScreensModule, "getVictoryTooltip", victoryTooltipArgs.makeFunctionArgs(), &victoryTooltip);

	if (!victoryTooltip.empty())
	{
		szTempBuffer.append(CvWString::format(SETCOLR, TEXT_COLOR("COLOR_PLAYER_CYAN_TEXT")));
		szTempBuffer.append(victoryTooltip);
		szTempBuffer.append(CvWString::format(ENDCOLR));
		szTempBuffer.append(NEWLINE);
	}

	// doc (Merijn): city name for settlers
	CvUnit* pHeadSelectedUnit = gDLL->getInterfaceIFace()->getHeadSelectedUnit();
	if (pHeadSelectedUnit != NULL)
	{
		if (pHeadSelectedUnit->isFound())
		{
			if (!pPlot->isWater() && !pPlot->isPeak())
			{
				CvWString szName;
				CyArgsList argsList4;
				argsList4.add(GC.getGameINLINE().getActivePlayer());
				argsList4.add(pPlot->getX());
				argsList4.add(pPlot->getY());
				gDLL->getPythonIFace()->callFunction(PYScreensModule, "getCityName", argsList4.makeFunctionArgs(), &szName);

				if (!szName.empty())
				{
					szTempBuffer.append(szName);
					szTempBuffer.append(NEWLINE);
				}
			}
		}
	}

	// doc: region
	if (pPlot->getRegionID() >= 0)
	{
		szString.append(pPlot->getRegionName());
		szString.append(NEWLINE);
	}

	// doc: civilization birth protection
	if (pPlot->isBirthProtected())
	{
		szString.append(GET_PLAYER(pPlot->getBirthProtected()).formatColor(gDLL->getText("TXT_KEY_INTERFACE_BIRTH_PROTECTED", GC.getCivilizationInfo(GET_PLAYER(pPlot->getBirthProtected()).getCivilizationType()).getDescription())));
		szString.append(NEWLINE);
	}

	// doc: expansion target
	if (pPlot->isExpansion())
	{
		szString.append(GET_PLAYER(pPlot->getExpansion()).formatColor(gDLL->getText("TXT_KEY_INTERFACE_BIRTH_EXPANSION", GET_PLAYER(pPlot->getExpansion()).getCivilizationAdjective())));
		szString.append(NEWLINE);
	}

	// <advc.187>
	if (kPlot.isActiveVisible(false))
	{
		int iAirUnits = kPlot.countNumAirUnits(eActiveTeam);
		if (gDLL->UI().getInterfaceMode() == INTERFACEMODE_REBASE ||
			(iAirUnits > 0 && BUGOption::isEnabled("MainInterface__AirCapacity", true)))
		{
			szString.append(gDLL->getText("TXT_KEY_CITY_BAR_AIR_UNIT_CAPACITY",
					iAirUnits, kPlot.airUnitSpaceAvailable(eActiveTeam) + iAirUnits));
			szString.append(NEWLINE);
		}
	} // </advc.187>
	PlayerTypes const eRevealedOwner = kPlot.getRevealedOwner(eActiveTeam, true);
	if (eRevealedOwner != NO_PLAYER ||
		/*	<advc.099f> As of AdvCiv 1.0, culture no longer spreads to unowned plots.
			However, for legacy saves, showing culture w/o an option is annoying.
			Solution: let CvGame set this bool member based on the save version. */
		m_bAlwaysShowPlotCulture ||
		bShift/* || BUGOption::isEnabled("MiscHover__CultureInUnownedTiles", false)*/)
	{	// </advc.099f>
		if (kPlot.isActiveVisible(true))
		{	// <advc.101>
			if (kPlot.isCity() &&
				BUGOption::isEnabled("MainInterface__RevoltHelp", true))
			{
				CvWStringBuffer szRevoltHelp;
				setRevoltHelp(szRevoltHelp, *kPlot.getPlotCity());
				if (!szRevoltHelp.isEmpty())
				{
					szString.append(szRevoltHelp.getCString());
					szString.append(NEWLINE);
				}
			} // </advc.101>
			// <advc.099g> Put the players w/ tile culture in a container first
			std::vector<std::pair<int,PlayerTypes> > aieCulturePerPlayer;
			/*  Go backwards b/c of the stable_sort call below. Removing that call
				will restore the BtS ordering (except for the special treatment
				of eActivePlayer). */
			for (int i = MAX_PLAYERS - 1; i >= 0; i--)
			{
				if (i == eRevealedOwner || i == eActivePlayer) // Prepended below
					continue; // </advc.099g>
				CvPlayer const& kPlayer = GET_PLAYER((PlayerTypes)i);
				// advc.099: Replaced "Alive" with "EverAlive"
				if (kPlayer.isEverAlive() && kPlot.getCulture(kPlayer.getID()) > 0)
				{
					int iCulture = kPlot.calculateCulturePercent(kPlayer.getID());
					/*  K-Mod, 29/sep/10, Karadoc
						Prevent display of 0% culture, to reduce the spam created by trade culture. */
					if (iCulture >= 1)
					{	// advc.099g:
						aieCulturePerPlayer.push_back(std::make_pair(iCulture, kPlayer.getID()));
					}
				}
			}  // <advc.099g>
			std::stable_sort(aieCulturePerPlayer.begin(), aieCulturePerPlayer.end());
			if (eActivePlayer != eRevealedOwner)
			{
				int iCulture = kPlot.calculateCulturePercent(eActivePlayer);
				if (iCulture >= 1)
					aieCulturePerPlayer.push_back(std::make_pair(iCulture, eActivePlayer));
			}
			if (eRevealedOwner != NO_PLAYER) // advc.099f
			{	/*	<advc.001> Relevant when a plot attains an owner only due to
					being surrounded by owned plots */
				int iOwnerCulture = (aieCulturePerPlayer.empty() ? 100 :
						kPlot.calculateCulturePercent(eRevealedOwner)); // </advc.001>
				aieCulturePerPlayer.push_back(std::make_pair(
						iOwnerCulture, eRevealedOwner));
			}
			std::reverse(aieCulturePerPlayer.begin(), aieCulturePerPlayer.end());
			for (size_t i = 0; i < aieCulturePerPlayer.size(); i++)
			{
				CvPlayer const& kPlayer = GET_PLAYER(aieCulturePerPlayer[i].second);
				int iCulture = aieCulturePerPlayer[i].first;
				// </advc.099g>
				szTempBuffer.Format(L"%d%% " SETCOLR L"%s" ENDCOLR, iCulture,
						PLAYER_TEXT_COLOR(kPlayer), kPlayer.getCivilizationAdjective());
				szString.append(szTempBuffer);
				szString.append(NEWLINE);
				// <advc.099g> Put it all on one line? I guess better not.
				//setListHelp(szString, L"", szTempBuffer.GetCString(), L", ", i == 0);
			}
			/*if(!aieCulturePerPlayer.empty())
				szString.append(NEWLINE);*/
			// </advc.099g>
		}
		else if(eRevealedOwner != NO_PLAYER) // advc.099f
		{
			CvPlayer const& kRevealOwner = GET_PLAYER(eRevealedOwner);
			szTempBuffer.Format(SETCOLR L"%s" ENDCOLR,
					PLAYER_TEXT_COLOR(kRevealOwner), kRevealOwner.getCivilizationDescription());
			szString.append(szTempBuffer);
			szString.append(NEWLINE);
		}
	}
	CvUnit const* pHeadSelectedUnit = gDLL->UI().getHeadSelectedUnit(); // advc
	// <advc.012>
	TeamTypes const eDefTeam = (eRevealedOwner != NO_PLAYER ?
			GET_PLAYER(eRevealedOwner).getTeam() :
			NO_TEAM);
	int iDefWithFeatures = kPlot.defenseModifier(
			eDefTeam, true, NO_TEAM, true);
	int iDefWithoutFeatures = kPlot.defenseModifier(
			eDefTeam, true, kPlot.getRevealedTeam(eActiveTeam, true), true);
	int iDelta = iDefWithFeatures - iDefWithoutFeatures;
	if(iDefWithoutFeatures != 0 || iDefWithFeatures != 0)
	{
		if(iDefWithoutFeatures != 0)
		{
			szString.append(gDLL->getText("TXT_KEY_PLOT_BONUS", iDefWithoutFeatures));
			if(iDelta != 0)
				szString.append(L", ");
		}
		if(iDelta != 0)
		{
			if(iDefWithoutFeatures == 0)
				szString.append(gDLL->getText("TXT_KEY_TILE_RIVALDEF"));
			szString.append(gDLL->getText("TXT_KEY_FEATURE_RIVALDEF", iDelta));
		}
		szString.append(NEWLINE);
	} // </advc.012>

	if (kPlot.getTerrainType() != NO_TERRAIN)
	{
		if (kPlot.isPeak())
			szString.append(gDLL->getText("TXT_KEY_PLOT_PEAK"));
		else
		{
			if (kPlot.isWater())
			{
				szTempBuffer.Format(SETCOLR, TEXT_COLOR("COLOR_WATER_TEXT"));
				szString.append(szTempBuffer);
			}

			if (kPlot.isHills())
				szString.append(gDLL->getText("TXT_KEY_PLOT_HILLS"));

			if (kPlot.isFeature())
			{
				szTempBuffer.Format(L"%s/", GC.getInfo(kPlot.getFeatureType()).getDescription());
				szString.append(szTempBuffer);
			}

			szString.append(GC.getInfo(kPlot.getTerrainType()).getDescription());

			if (kPlot.isWater())
				szString.append(ENDCOLR);
		}
	}
	/*  advc.001w: hasYield is based on getYield, which is not always consistent
		with calculateYield. */
	//if (kPlot.hasYield())
	{
		FOR_EACH_ENUM(Yield)
		{
			int iYield = kPlot.calculateYield(eLoopYield, true);
			if (iYield != 0)
			{
				szTempBuffer.Format(L", %d%c", iYield, GC.getInfo(eLoopYield).getChar());
				szString.append(szTempBuffer);
			}
		}
	}
	// <advc.030> Warn about ice-locked water area
	int const iOceanThresh = GC.getDefineINT(CvGlobals::MIN_WATER_SIZE_FOR_OCEAN);
	CvArea const& kArea = kPlot.getArea();
	if (kPlot.isWater() && !kPlot.isImpassable() && !kPlot.isLake() &&
		kArea.getNumTiles() < iOceanThresh /*&& // Only when settler selected?
		pHeadSelectedUnit != NULL && pHeadSelectedUnit->canFound()*/)
	{
		bool bIceFound = false;
		bool bFullyRevealed = true; // Don't give away unrevealed plots
		bool bActiveCityFound = false; // Adjacent city will give them away anyway
		bool bShowIceLocked = false;
		for (SquareIter it(kPlot, iOceanThresh);
			!bShowIceLocked && it.hasNext(); ++it)
		{
			if (it->isArea(kArea))
			{
				if (!it->isRevealed(eActiveTeam))
					bFullyRevealed = false;
			}
			else if (it->isAdjacentToArea(kArea))
			{
				if (it->isImpassable())
					bIceFound = true;
				else if (it->getOwner() == eActivePlayer && it->isCity())
					bActiveCityFound = true;
			}
			bShowIceLocked = bIceFound && (bFullyRevealed || bActiveCityFound);
		}
		if (bShowIceLocked)
		{
			szString.append(CvWString::format(SETCOLR, TEXT_COLOR("COLOR_WATER_TEXT")));
			szString.append(L" ");
			szString.append(gDLL->getText("TXT_KEY_PLOT_ICE_LOCKED"));
			szString.append(ENDCOLR);
		}
	} // </advc.030>
	// <advc.001> Moved up. BtS was using getImprovementType in the eBonus code
	ImprovementTypes const ePlotImprovement = kPlot.getRevealedImprovementType(
			eActiveTeam, true); // </advc.001>
	// <advc.059>
	bool bHealthHappyShown = false; // Show it later if improved
	if (ePlotImprovement == NO_IMPROVEMENT ||
		(GC.getInfo(ePlotImprovement).get(CvImprovementInfo::HealthPercent) == 0 && // advc.901
		GC.getInfo(ePlotImprovement).getHappiness() == 0))
	{
		setPlotHealthHappyHelp(szString, kPlot);
		bHealthHappyShown = true;
	} // </advc.059>

	if (kPlot.isFreshWater())
	{
		szString.append(NEWLINE);
		szString.append(gDLL->getText("TXT_KEY_PLOT_FRESH_WATER"));
		// <advc.059>
		if(pHeadSelectedUnit != NULL &&
			pHeadSelectedUnit->isFound() && pHeadSelectedUnit->at(kPlot))
		{
			szTempBuffer = CvWString::format(L" +%d%c",
					GC.getDefineINT(CvGlobals::FRESH_WATER_HEALTH_CHANGE),
					gDLL->getSymbolID(HEALTHY_CHAR));
			szString.append(szTempBuffer);
		} // </advc.059>
	}

	if (kPlot.isLake())
	{
		szString.append(NEWLINE);
		szString.append(gDLL->getText("TXT_KEY_PLOT_FRESH_WATER_LAKE"));
	}

	if (kPlot.isImpassable())
	{
		szString.append(NEWLINE);
		szString.append(gDLL->getText("TXT_KEY_PLOT_IMPASSABLE"));
	}

	BonusTypes eBonus = NO_BONUS;
	if (kGame.isDebugMode())
		eBonus = kPlot.getBonusType();
	else eBonus = kPlot.getBonusType(eActiveTeam);
	if (eBonus != NO_BONUS)
	{
		szTempBuffer.Format(L"%c " SETCOLR L"%s" ENDCOLR, GC.getInfo(eBonus).getChar(), TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"), GC.getInfo(eBonus).getDescription());

		szString.append(NEWLINE);
		szString.append(szTempBuffer);

		// K-Mod. I've rearranged and edited some of the code in this section to fix some bugs.
		// (for example, obsolete bonuses shouldn't say "requires x improvement"; and neither should bonuses that are already connected with a fort.)
		if (!GET_TEAM(eActiveTeam).isBonusObsolete(eBonus))
		{
			bool bFirst = true; // advc.047
			if (GC.getInfo(eBonus).getHealth() != 0)
			{	// <advc.047>
				if(bFirst)
				{
					szString.append(L" ");
					bFirst = false;
				}
				else // </advc.047>
					szString.append(L", ");
				szTempBuffer.Format(L"+%d%c", abs(GC.getInfo(eBonus).getHealth()), ((GC.getInfo(eBonus).getHealth() > 0) ? gDLL->getSymbolID(HEALTHY_CHAR): gDLL->getSymbolID(UNHEALTHY_CHAR)));
				szString.append(szTempBuffer);
			}

			if (GC.getInfo(eBonus).getHappiness() != 0)
			{	// <advc.047>
				if(bFirst)
				{
					szString.append(L" ");
					bFirst = false;
				}
				else // </advc.047>
					szString.append(L", ");
				szTempBuffer.Format(L"+%d%c", abs(GC.getInfo(eBonus).getHappiness()),
						GC.getInfo(eBonus).getHappiness() > 0 ? gDLL->getSymbolID(HAPPY_CHAR):
						gDLL->getSymbolID(UNHAPPY_CHAR));
				szString.append(szTempBuffer);
			}
			CvWStringBuffer szReqs; // advc.047
			if (!GET_TEAM(eActiveTeam).isHasTech(GC.getInfo(eBonus).getTechCityTrade()))
			{
				/*szString.append(gDLL->getText("TXT_KEY_PLOT_RESEARCH",
					GC.getInfo((TechTypes)GC.getInfo(eBonus).
					getTechCityTrade()).getTextKeyWide())); */
				// <advc.047>
				szTempBuffer.Format(SETCOLR L"%s" ENDCOLR, TEXT_COLOR("COLOR_WARNING_TEXT"),
						GC.getInfo(GC.getInfo(eBonus).getTechCityTrade()).getText());
				szReqs.append(szTempBuffer);
			}
			bool bCity = kPlot.isCity();
			bool bConnected = GET_PLAYER(eActivePlayer).
					doesImprovementConnectBonus(ePlotImprovement, eBonus);
			// Moved up (b/c the route isn't needed for the yields)
			if(!bCity && !kPlot.isBonusNetwork(eActiveTeam) && !kPlot.isWater() &&
				bConnected) // Mention route only if all other pieces in place
			{
				//szString.append(gDLL->getText("TXT_KEY_PLOT_REQUIRES_ROUTE"));
				if(!szReqs.isEmpty())
					szReqs.append(L", ");
				szTempBuffer.Format(SETCOLR L"%s" ENDCOLR, TEXT_COLOR("COLOR_WARNING_TEXT"),
						gDLL->getText("TXT_KEY_ROUTE_ROAD").GetCString());
				szReqs.append(szTempBuffer);
			}
			bool bReqsDone = false;
			// </advc.047>
			if(!bCity)
			{
				if (!bConnected ||
					// <advc.047> Show what replacing Fort would yield
					(ePlotImprovement != NULL && GC.getInfo(
					ePlotImprovement).isActsAsCity())) // </advc.047>
				{
					/*  K-Mod note: unfortunately, the following code assumes that
						there is only one improvement marked "isImprovementBonusTrade"
						for each bonus. */
					/*  advc (comment): ... and it assumes that the most important
						one has the lowest id */
					FOR_EACH_ENUM(Build)
					{
						ImprovementTypes eLoopImprov = GC.getInfo(eLoopBuild).getImprovement();
						if(eLoopImprov == NO_IMPROVEMENT ||
							/*  advc.047: Show only missing improvement;
								!bConnected doesn't ensure this when the
								city-trade tech is missing. */
							eLoopImprov == ePlotImprovement)
						{
							continue;
						}

						CvImprovementInfo& kImprovementInfo = GC.getInfo(eLoopImprov);
						if(!kImprovementInfo.isImprovementBonusTrade(eBonus) ||
							!kPlot.canHaveImprovement(eLoopImprov, eActiveTeam, true))
						{
							continue;
						}
						if(!bConnected && eRevealedOwner != NO_PLAYER && // advc.047
							GET_TEAM(eActiveTeam).isHasTech(
							GC.getInfo(eLoopBuild).getTechPrereq()))
						{
							/*szString.append(gDLL->getText("TXT_KEY_PLOT_REQUIRES",
									kImprovementInfo.getTextKeyWide()));*/
							// <advc.047> Add to req list instead
							if(!szReqs.isEmpty())
								szReqs.append(L", ");
							szTempBuffer.Format(SETCOLR L"%s" ENDCOLR, TEXT_COLOR(
									"COLOR_WARNING_TEXT"), kImprovementInfo.getText());
							szReqs.append(szTempBuffer);
							// </advc.047>
						}
						/*else if (GC.getInfo(eBonus).getTechCityTrade() !=
								GC.getInfo(eLoopBuild).getTechPrereq()) {
							szString.append(gDLL->getText("TXT_KEY_PLOT_RESEARCH",
									GC.getInfo(GC.getInfo(eLoopBuild).
									getTechPrereq()).getTextKeyWide()));
						}*/ // <advc.047>
						// ^Too complicated. Player will have to look the tech up.
						if(!szReqs.isEmpty())
						{
							szString.append(L" (");
							szString.append(gDLL->getText("TXT_KEY_WITH") + L" ");
							szString.append(szReqs);
							szString.append(L")");
							bReqsDone = true;
						} // </advc.047>
						bFirst = true;
						FOR_EACH_ENUM(Yield)
						{
							int iYieldChange = kImprovementInfo.
									getImprovementBonusYield(eBonus, eLoopYield) +
									kImprovementInfo.getYieldChange(eLoopYield)
									/*  <advc.047> If there's already an improvement,
										show the difference between the yields. */
									- (ePlotImprovement == NO_IMPROVEMENT ||
									ePlotImprovement == eLoopImprov ? 0 :
									kPlot.calculateImprovementYieldChange(
									ePlotImprovement, eLoopYield, eActivePlayer));
									// </advc.047>
							if (iYieldChange != 0)
							{
								if (iYieldChange > 0)
								{
									szTempBuffer.Format(L"+%d%c", iYieldChange,
											GC.getInfo(eLoopYield).getChar());
								}
								else
								{
									szTempBuffer.Format(L"%d%c", iYieldChange,
											GC.getInfo(eLoopYield).getChar());
								}
								setListHelp(szString, L"\n", szTempBuffer, L", ", bFirst);
							}
						}
						if (!bFirst)
						{ // <advc.047>
						  // In red unless already shown red text about unconnected bonus
							CvWString szTag = L"TXT_KEY_BONUS_WITH_IMPROVEMENT";
							if(szReqs.isEmpty())
								szTag += L"_WARNING"; // </advc.047>
							szString.append(gDLL->getText(szTag, kImprovementInfo.getTextKeyWide()));
						}
						break;
					}
				}
				// advc.047: PLOT_REQUIRES_ROUTE code moved up
			}
			// <advc.047> Duplicate code; sorry.
			if(!bReqsDone && !szReqs.isEmpty())
			{
				szString.append(L" (");
				szString.append(gDLL->getText("TXT_KEY_WITH") + L" ");
				szString.append(szReqs);
				szString.append(L")");
				bReqsDone = true;
			} // </advc.047>

			// K-Mod note: I'm not sure whether or not the help should be displayed when the bonus is obsolete.
			// The fact is, none of the bonuses have help text in K-Mod (or standard bts.)
			if (!CvWString(GC.getInfo(eBonus).getHelp()).empty())
			{
				szString.append(NEWLINE);
				szString.append(GC.getInfo(eBonus).getHelp());
			}
		} // end !isBonusObsolete
		// <advc.050>
		CvInitCore const& ic = GC.getInitCore();
		if(GC.altKey()) /* [Alt] is also for combat odds. That takes
				precedence. This function isn't even called when ALT is
				pressed on a hostile unit. (Check [Ctrl] instead?) */
		{
			CvWString szMapName = ic.getMapScriptName();
			int iPos = szMapName.find(L"."); // Drop the file extension
			if(iPos != CvWString::npos && iPos >= 2)
				szMapName = szMapName.substr(0, iPos);
			std::transform(szMapName.begin(), szMapName.end(),
					szMapName.begin(), ::toupper); // to upper case
			std::wostringstream ssKey;
			ssKey << L"TXT_KEY_" << szMapName << L"_" <<
					kPlot.getX() << L"_" << kPlot.getY() << L"_BONUS_";
			CvWString szBonusName = GC.getInfo(eBonus).getDescription();
			std::transform(szBonusName.begin(), szBonusName.end(),
					szBonusName.begin(), ::toupper);
			// Tolerate plural errors
			if(szBonusName.at(szBonusName.length() - 1) == L'S')
				szBonusName = szBonusName.substr(0, szBonusName.length() - 1);
			ssKey << szBonusName;
			CvWString szKey = ssKey.str();
			CvWString szHistoryText = gDLL->getText(szKey);
			// getText returns txtKey if it can't find the text key
			if(szHistoryText.compare(szKey) == 0)
			{
				szKey.append(L"s");
				szHistoryText = gDLL->getText(szKey);
			}
			if(szHistoryText.compare(szKey) != 0)
			{
				szString.append(NEWLINE);
				szString.append(NEWLINE);
				szString.append(CvWString::format(SETCOLR,
						TEXT_COLOR("COLOR_HIGHLIGHT_TEXT")));
				szString.append(szHistoryText);
				szString.append(CvWString::format( ENDCOLR));
			}
		} // </advc.050>
	}

	if (ePlotImprovement != NO_IMPROVEMENT)
	{
		szString.append(NEWLINE);
		// <advc.005c>
		bool bNamedRuin = false;
		if(ePlotImprovement == GC.getRUINS_IMPROVEMENT())
		{
			wchar const* szRuinsName = kPlot.getRuinsName();
			if(szRuinsName != NULL/*&& wcslen(szRuinsName) > 0*/)
			{
				szString.append(gDLL->getText("TXT_KEY_IMPROVEMENT_CITY_RUINS_NAMED",
						szRuinsName));
				bNamedRuin = true;
			}
		}
		if(!bNamedRuin) // from Volcano event // </advc.005c>
			szString.append(GC.getInfo(ePlotImprovement).getDescription());

		bool bFound = false;

		FOR_EACH_ENUM(Yield)
		{
			if (GC.getInfo(ePlotImprovement).getIrrigatedYieldChange(eLoopYield) != 0)
			{
				bFound = true;
				break;
			}
		}

		if (bFound)
		{
			if (kPlot.isIrrigationAvailable())
				szString.append(gDLL->getText("TXT_KEY_PLOT_IRRIGATED"));
			else szString.append(gDLL->getText("TXT_KEY_PLOT_NOT_IRRIGATED"));
		}

		if (GC.getInfo(ePlotImprovement).getImprovementUpgrade() != NO_IMPROVEMENT)
		{
			if (kPlot.getUpgradeProgress() > 0 || kPlot.isBeingWorked())
			{
				int iTurns = kPlot.getUpgradeTimeLeft(ePlotImprovement, eRevealedOwner);
				// <advc.912f>
				bool bStagnant = (iTurns < 0);
				if (bStagnant)
				{
					iTurns *= -1;
					szString.append(CvWString::format(SETCOLR,
							TEXT_COLOR("COLOR_LIGHT_GREY")));
				} // </advc.912f>
				szString.append(gDLL->getText("TXT_KEY_PLOT_IMP_UPGRADE", iTurns,
						GC.getInfo(GC.getInfo(ePlotImprovement).getImprovementUpgrade()).
						getTextKeyWide()));
				// <advc.912f>
				if (bStagnant)
					szString.append(ENDCOLR); // </advc.912f>
			}
			else
			{
				szString.append(gDLL->getText("TXT_KEY_PLOT_WORK_TO_UPGRADE",
						GC.getInfo(GC.getInfo(ePlotImprovement).getImprovementUpgrade()).
						getTextKeyWide()));
			}
		}
	}
	// <advc.059>
	if (!bHealthHappyShown)
		setPlotHealthHappyHelp(szString, kPlot); // </advc.059>
	if (kPlot.getRevealedRouteType(eActiveTeam, true) != NO_ROUTE)
	{
		szString.append(NEWLINE);
		szString.append(GC.getInfo(kPlot.getRevealedRouteType(eActiveTeam, true)).getDescription());
	}
	// <advc.011c>
	FOR_EACH_ENUM2(Build, eBuild)
	{
		if(kPlot.getBuildProgress(eBuild) <= 0 ||
			!kPlot.canBuild(eBuild, eActivePlayer, false, false))
		{
			continue;
		}
		int iTurnsLeft = kPlot.getBuildTurnsLeft(eBuild, eActivePlayer);
		if(iTurnsLeft <= 0 || iTurnsLeft == MAX_INT)
			continue; // </advc.011c>
		// <advc.011b>
		int iInitialTurnsNeeded = scaled(
				kPlot.getBuildTime(eBuild, eActivePlayer),
				GET_PLAYER(eActivePlayer).getWorkRate(eBuild)).
				ceil();
		int iTurnsSpent = iInitialTurnsNeeded - iTurnsLeft;
		if(iTurnsSpent <= 0)
			continue;
		CvBuildInfo const& kBuild = GC.getInfo(eBuild);
		CvWString szBuildDescr = kBuild.getDescription();
		/*  Nicer to use the structure (improvement or route) name if it isn't a
			build that only removes a feature. */
		ImprovementTypes eImprovement = kBuild.getImprovement();
		if(eImprovement != NO_IMPROVEMENT)
			szBuildDescr = GC.getInfo(eImprovement).getDescription();
		else
		{
			RouteTypes eRoute = kBuild.getRoute();
			if(eRoute != NO_ROUTE)
				szBuildDescr = GC.getInfo(eRoute).getDescription();
		}
		szTempBuffer.Format(SETCOLR L"%s" ENDCOLR,
				TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
				szBuildDescr.c_str());
		szBuildDescr = szTempBuffer;
		bool bDecay = (GC.getDefineINT(CvGlobals::DELAY_UNTIL_BUILD_DECAY) > 0 &&
				kPlot.isBuildProgressDecaying(true));
		if(bDecay) // Check if Workers are getting on the task this turn
		{
			FOR_EACH_UNIT_IN(pUnit, kPlot)
			{
				if(pUnit->getTeam() == eActiveTeam && pUnit->movesLeft() > 0 &&
					pUnit->getGroup()->getMissionType(0) == MISSION_BUILD)
				{
					bDecay = false;
					break;
				}
			}
		}
		if(GC.ctrlKey() || BUGOption::isEnabled("MiscHover__PartialBuildsAlways", false))
		{
			szString.append(NEWLINE);
			szString.append(szBuildDescr);
			szString.append(CvWString::format(L" (%d/%d %s%s)",
					iTurnsSpent, iInitialTurnsNeeded, gDLL->getText("TXT_KEY_REPLAY_SCREEN_TURNS").c_str(),
					bDecay ? CvWString::format(L"; " SETCOLR L"%s" ENDCOLR,
					TEXT_COLOR("COLOR_WARNING_TEXT"),
					gDLL->getText("TXT_KEY_MISC_DECAY_WARNING").c_str()).c_str() : L""));
		}
	} // </advc.011b>

	// advc.003h (BBAI code from 07/11/08 by jdog5000 moved into setPlotHelpDebug)
	if (kPlot.getBlockadedCount(eActiveTeam) > 0)
	{
		szString.append(CvWString::format(SETCOLR, TEXT_COLOR("COLOR_NEGATIVE_TEXT")));
		szString.append(NEWLINE);
		szString.append(gDLL->getText("TXT_KEY_PLOT_BLOCKADED"));
		szString.append(CvWString::format(ENDCOLR));
	}
	// <advc.004k>
	if (pHeadSelectedUnit != NULL && pHeadSelectedUnit->isSeaPatrolling() &&
		pHeadSelectedUnit->canReachBySeaPatrol(kPlot))
	{
		szString.append(CvWString::format(SETCOLR, TEXT_COLOR("COLOR_CITY_BLUE_TEXT")));
		szString.append(NEWLINE);
		szString.append(gDLL->getText("TXT_KEY_PLOT_SEA_PATROLLED"));
		szString.append(CvWString::format(ENDCOLR));
	} // </advc.004k>

	if (kPlot.isFeature())
	{
		int iDamage = GC.getInfo(kPlot.getFeatureType()).getTurnDamage();

		if (iDamage > 0)
		{
			szString.append(CvWString::format(SETCOLR, TEXT_COLOR("COLOR_NEGATIVE_TEXT")));
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_PLOT_DAMAGE", iDamage));
			szString.append(CvWString::format( ENDCOLR));
		}
		// UNOFFICIAL_PATCH, User interface (FeatureDamageFix), 06/02/10, LunarMongoose: START
		else if (iDamage < 0)
		{
			szString.append(CvWString::format(SETCOLR, TEXT_COLOR("COLOR_POSITIVE_TEXT")));
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_PLOT_DAMAGE", iDamage));
			szString.append(CvWString::format( ENDCOLR));
		} // UNOFFICIAL_PATCH: END
	}
}

// <advc.059>
void CvGameTextMgr::setPlotHealthHappyHelp(CvWStringBuffer& szBuffer, CvPlot const& kPlot) const
{
	CvTeam const& kActiveTeam = GET_TEAM(getActiveTeam());
	CvPlayer const& kActivePlayer = GET_PLAYER(getActivePlayer());
	CvUnit const* pHeadSelectedUnit = gDLL->UI().getHeadSelectedUnit();
	bool bCanRemove = false;
	// <advc.004b>
	bool bFound = false;
	if (pHeadSelectedUnit != NULL)
	{
		if (pHeadSelectedUnit->isFound())
			bFound = true; // </advc.004b>
		if (pHeadSelectedUnit->AI_getUnitAIType() == UNITAI_WORKER &&
			pHeadSelectedUnit->at(kPlot) &&
			kPlot.isFeature())
		{
			FOR_EACH_ENUM(Build)
			{
				if (GC.getInfo(eLoopBuild).isFeatureRemove(kPlot.getFeatureType()) &&
					pHeadSelectedUnit->canBuild(kPlot, eLoopBuild, false, false))
				{
					bCanRemove = true;
					break;
				}
			}
		}
	}
	if(!bFound && !bCanRemove && !kPlot.isCityRadius())
		return;
	bool bNearSelectedCity = false;
	if (!bFound && !bCanRemove)
	{
		bool bOurCity = false;
		for (NearbyCityIter itCity(kPlot); itCity.hasNext(); ++itCity)
		{
			if (itCity->getOwner() == kActivePlayer.getID() ||
				(kPlot.getOwner() == kActivePlayer.getID() &&
				itCity->isRevealed(kActiveTeam.getID(), true)))
			{
				bOurCity = true;
				if (gDLL->UI().isCitySelected(&*itCity))
				{
					bNearSelectedCity = true;
					break;
				}
			}
		}
		if (!bOurCity)
			return;
	}
	int iHealthPercent = 0;
	int iHappy = 0;
	FeatureTypes eFeature = kPlot.getFeatureType();
	if (eFeature != NO_FEATURE)
	{	// <advc.901>
		if (kActiveTeam.canAccessHappyHealth(kPlot,
			GC.getInfo(eFeature).getHealthPercent())) // </advc.901>
		{
			iHealthPercent = GC.getInfo(eFeature).getHealthPercent();
		}  // <advc.901>
		if (kActiveTeam.canAccessHappyHealth(kPlot,
			kActivePlayer.getFeatureHappiness(eFeature))) // </advc.901>
		{
			iHappy = kActivePlayer.getFeatureHappiness(eFeature);
		}
	}
	ImprovementTypes eImprov = kPlot.getRevealedImprovementType(kActiveTeam.getID(), true);
	if (eImprov != NO_IMPROVEMENT)
	{
		CvImprovementInfo const& kImprov = GC.getInfo(eImprov);
		if (kActiveTeam.canAccessHappyHealth(kPlot, kImprov.getHappiness())) // advc.901
			iHappy += kImprov.getHappiness();  // <advc.901>
		if (kActiveTeam.canAccessHappyHealth(kPlot,
			kImprov.get(CvImprovementInfo::HealthPercent)))
		{
			iHealthPercent += kImprov.get(CvImprovementInfo::HealthPercent);
		} // </advc.901>
	}
	bool bCitySelected = (gDLL->UI().getHeadSelectedCity() != NULL);
	bool bAlwaysShow = (bFound || bCanRemove || bNearSelectedCity);
	if (iHappy != 0)
	{
		if (bAlwaysShow || !bCitySelected)
		{
			szBuffer.append(", ");
			int iIcon = gDLL->getSymbolID(iHappy > 0 ? HAPPY_CHAR : UNHAPPY_CHAR);
			szBuffer.append(CvWString::format(L"%d%c", abs(iHappy), iIcon));
		}
	}
	if (iHealthPercent != 0)
	{
		int iAbsHealthPercent = abs(iHealthPercent);
		if (bAlwaysShow || (!bCitySelected &&
			// Basically anything that isn't an ordinary Forest, Jungle, Flood Plains
			(iAbsHealthPercent >= 100 || iHealthPercent <= -50)))
		{
			szBuffer.append(", ");
			float fAbsHealth = iAbsHealthPercent / 100.0f;
			int iIcon = gDLL->getSymbolID(iHealthPercent > 0 ? HEALTHY_CHAR : UNHEALTHY_CHAR);
			if(iHealthPercent % 100 == 0)
				szBuffer.append(CvWString::format(L"%d%c", iAbsHealthPercent / 100, iIcon));
			else if(iHealthPercent % 10 == 0)
				szBuffer.append(CvWString::format(L"%.1f%c", fAbsHealth, iIcon));
			else szBuffer.append(CvWString::format(L"%.2f%c", fAbsHealth, iIcon));
		}
	}
}

// Replacing code originally in CvWidgetData::parseActionHelp
void CvGameTextMgr::setHealthHappyBuildActionHelp(CvWStringBuffer& szBuffer,
	CvPlot const& kPlot, BuildTypes eBuild) const
{
	CvBuildInfo const& kBuild = GC.getInfo(eBuild);
	ImprovementTypes const eNewImprov = kBuild.getImprovement();
	bool const bRemoveFeature = (kPlot.isFeature() &&
			kBuild.isFeatureRemove(kPlot.getFeatureType()));
	TeamTypes const eActiveTeam = getActiveTeam();
	if (eNewImprov != NO_IMPROVEMENT || bRemoveFeature)
	{
		ImprovementTypes eOldImprov = kPlot.getRevealedImprovementType(eActiveTeam, true);
		CvWString szNewItem;
		szNewItem.Format(NEWLINE L"%c", gDLL->getSymbolID(BULLET_CHAR));
		for (NearbyCityIter itCity(kPlot); itCity.hasNext(); ++itCity)
		{
			if (!itCity->isRevealed(eActiveTeam, true))
				continue;
			int iHappyChange, iUnhappyChange, iGoodHealthChange, iBadHealthChange,
					iGoodHealthPercentChange, iBadHealthPercentChange;
			itCity->goodBadHealthHappyChange(kPlot, eNewImprov == NO_IMPROVEMENT ?
					eOldImprov : eNewImprov, eOldImprov, bRemoveFeature,
					iHappyChange, iUnhappyChange, iGoodHealthChange, iBadHealthChange,
					iGoodHealthPercentChange, iBadHealthPercentChange);
			// Anger and bad health are counted as negative values (not my idea)
			iUnhappyChange *= -1;
			iBadHealthChange *= -1;
			iBadHealthPercentChange *= -1;
			bool bFirst = true;
			if (iHappyChange != 0)
			{
				szBuffer.append(bFirst ? szNewItem : L", "); bFirst = false;
				szBuffer.append(CvWString::format(L"%s%d%c", iHappyChange > 0 ? "+" : "",
						iHappyChange, gDLL->getSymbolID(HAPPY_CHAR)));
			}
			if (iUnhappyChange != 0)
			{
				szBuffer.append(bFirst ? szNewItem : L", "); bFirst = false;
				szBuffer.append(CvWString::format(L"%s%d%c", iUnhappyChange > 0 ? "+" : "",
						iUnhappyChange, gDLL->getSymbolID(UNHAPPY_CHAR)));
			}
			if (iGoodHealthPercentChange != 0)
			{
				szBuffer.append(bFirst ? szNewItem : L", "); bFirst = false;
				setHealthChangeBuildActionHelp(szBuffer, iGoodHealthChange,
						iGoodHealthPercentChange, gDLL->getSymbolID(HEALTHY_CHAR));
			}
			if (iBadHealthPercentChange != 0)
			{
				szBuffer.append(bFirst ? szNewItem : L", "); bFirst = false;
				setHealthChangeBuildActionHelp(szBuffer, iBadHealthChange,
						iBadHealthPercentChange, gDLL->getSymbolID(UNHEALTHY_CHAR));
			}
			if (!bFirst)
			{
				szBuffer.append(L" ");
				szBuffer.append(gDLL->getText("TXT_KEY_IN_CITY", itCity->getNameKey()));
			}
		}
	}
}


void CvGameTextMgr::setHealthChangeBuildActionHelp(CvWStringBuffer& szBuffer,
	int iChange, int iChangePercent, int iIcon) const
{
	char const* szSign = (iChangePercent > 0 ? "+" : "");
	CvWString szFraction;
	if (iChangePercent != iChange * 100)
	{
		float fAbsHealth = iChangePercent / 100.0f;
		bool bChange = (iChange != 0);
		if (bChange)
			szFraction.append(L"(");
		szFraction += CvWString::format(SETCOLR, TEXT_COLOR("COLOR_LIGHT_GREY"));
		if (iChangePercent % 10 == 0)
			szFraction += CvWString::format(L"%s%.1f", szSign, fAbsHealth);
		else szFraction += CvWString::format(L"%s%.2f", szSign, fAbsHealth);
		szFraction.append(ENDCOLR);
		if (bChange)
			szFraction.append(L")");
		else szFraction.append(CvWString::format(L"%c", iIcon));
	}
	if (iChange != 0)
	{
		szBuffer.append(CvWString::format(L"%s%d%c", szSign, iChange, iIcon));
		if (!szFraction.empty())
		{
			szBuffer.append(L" ");
			szBuffer.append(szFraction);
		}
	}
	else szBuffer.append(szFraction);
} // </advc.059>

// advc.135c:
void CvGameTextMgr::setPlotHelpDebug(CvWStringBuffer& szString, CvPlot const& kPlot) {

	//if (bCtrl && (gDLL->getChtLvl() > 0))
	// <advc.135c>
	if(GC.ctrlKey())
	{
		setPlotHelpDebug_Ctrl(szString, kPlot);
		return;
	} // </advc.135c>

	bool bShift = GC.shiftKey();
	bool bAlt = GC.altKey();

	//if (bShift && !bAlt && (gDLL->getChtLvl() > 0))
	// <advc.135c>
	if(bShift && !bAlt)
	{
		setPlotHelpDebug_ShiftOnly(szString, kPlot);
		return;
	} // </advc.135c>

	//if (!bShift && bAlt && (gDLL->getChtLvl() > 0))
	// <advc.135c>
	if(!bShift && bAlt)
	{
		setPlotHelpDebug_AltOnly(szString, kPlot);
		return;
	} // </advc.135c>

	//if (bShift && bAlt && (gDLL->getChtLvl() > 0))
	// <advc.135c>
	if(bShift && bAlt)
	{
		setPlotHelpDebug_ShiftAltOnly(szString, kPlot);
		return;
	} // </advc.135c>
}

// advc.135c: Cut and pasted from setPlotHelp
void CvGameTextMgr::setPlotHelpDebug_Ctrl(CvWStringBuffer& szString, CvPlot const& kPlot)
{
	bool bShift = GC.shiftKey();
	if (bShift && kPlot.headUnitNode() != NULL)
		return;

	bool const bAlt = GC.altKey();
	CvWString szTempBuffer;
	CvGame const& kGame = GC.getGame();
	bool bConstCache = kGame.isNetworkMultiPlayer(); // advc.001n

	if (kPlot.getOwner() != NO_PLAYER &&
		/*  advc.001n: AI_getPlotDanger calls setActivePlayerSafeRangeCache,
			which may not be a safe thing to do in multiplayer. */
		!bConstCache)
	{
		int iPlotDanger = GET_PLAYER(kPlot.getOwner()).AI_getPlotDanger(kPlot,
				2); // advc.135c
		if (iPlotDanger > 0)
			szString.append(CvWString::format(L"\nPlot Danger = %d", iPlotDanger));
	}

	CvCityAI const* pPlotCity = kPlot.AI_getPlotCity();
	if (pPlotCity != NULL /* advc.003n: */ && !pPlotCity->isBarbarian())
	{
		PlayerTypes ePlayer = kPlot.getOwner();
		CvPlayerAI& kPlayer = GET_PLAYER(ePlayer);

		int iCityDefenders = kPlot.plotCount(PUF_canDefendGroupHead, -1, -1, ePlayer, NO_TEAM, PUF_isCityAIType);
		int iAttackGroups = kPlot.plotCount(PUF_isUnitAIType, UNITAI_ATTACK, -1, ePlayer);
		szString.append(CvWString::format(L"\nDefenders [D+A]/N ([%d + %d] / %d)",
				iCityDefenders, iAttackGroups, pPlotCity->AI_neededDefenders(
				false, true))); // advc.001n
		// <advc.007>
		szString.append(CvWString::format(L"\nFloating Defenders Target: %d",
				pPlotCity->AI_neededFloatingDefenders(true, true)));
		szString.append(CvWString::format(L"\nArea Floating Def. H/N (%d / %d)", // </advc.007>
				kPlayer.AI_getTotalFloatingDefenders(pPlotCity->getArea()),
				kPlayer.AI_getTotalFloatingDefendersNeeded(pPlotCity->getArea(),
				true))); // advc.007
		szString.append(CvWString::format(L"\nAir Defenders H/N (%d / %d)",
				pPlotCity->getPlot().plotCount(PUF_canAirDefend, -1, -1,
				pPlotCity->getOwner(), NO_TEAM, PUF_isDomainType, DOMAIN_AIR),
				pPlotCity->AI_neededAirDefenders(/* advc.001n: */ true)));
		/*int iHostileUnits = kPlayer.AI_countNumAreaHostileUnits(pPlotCity->getArea());
		if (iHostileUnits > 0)
			szString+=CvWString::format(L"\nHostiles = %d", iHostileUnits);*/

		szString.append(CvWString::format(L"\nThreat C/P (%d / %d)",
				pPlotCity->AI_cityThreat(), kPlayer.AI_getTotalAreaCityThreat(pPlotCity->getArea())));

		bool bFirst = true;
		for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++) // advc.003n: was MAX_PLAYERS
		{
			PlayerTypes eLoopPlayer = (PlayerTypes)iI;
			CvPlayerAI& kLoopPlayer = GET_PLAYER(eLoopPlayer);
			if(eLoopPlayer == ePlayer || !kLoopPlayer.isAlive())
				continue;
			// BETTER_BTS_AI_MOD, DEBUG, 06/16/08, jdog5000: START
			// original code (advc: deleted)
			if(pPlotCity->isCapital())
			{
				int iCloseness = pPlotCity->AI_playerCloseness(eLoopPlayer, DEFAULT_PLAYER_CLOSENESS,
						true); // advc.001n
				int iPlayerCloseness = kPlayer.AI_playerCloseness(eLoopPlayer, DEFAULT_PLAYER_CLOSENESS,
						true); // advc.001n
				if(GET_TEAM(kPlayer.getTeam()).isHasMet(kLoopPlayer.getTeam()) || iPlayerCloseness != 0)
				{
					if(bFirst)
					{
						bFirst = false;
						szString.append(CvWString::format(L"\n\nCloseness + War: (in %d wars)", GET_TEAM(kPlayer.getTeam()).getNumWars()));
					}
					szString.append(CvWString::format(L"\n%s(%d) : %d ", kLoopPlayer.getName(), DEFAULT_PLAYER_CLOSENESS, iCloseness));
					szString.append(CvWString::format(L" [%d, ", iPlayerCloseness));
					if(kPlayer.getTeam() != kLoopPlayer.getTeam())
					{
						szString.append(CvWString::format(L"%d]",
								GET_TEAM(kPlayer.getTeam()).AI_teamCloseness(
								kLoopPlayer.getTeam(), DEFAULT_PLAYER_CLOSENESS,
								false, true))); // advc.001n
					/*  advc.001n: Only relevant for the K-Mod war AI, and I'm not totally sure that
						CvTeamAI::AI_startWarVal is safe for networked games
						(despite the bConstCache param that I've added). */
						if(!getUWAI().isEnabled())
						{
							if(GET_TEAM(kPlayer.getTeam()).isHasMet(kLoopPlayer.getTeam()) &&
									GET_TEAM(kPlayer.getTeam()).AI_getAttitude(kLoopPlayer.getTeam()) != ATTITUDE_FRIENDLY)
							{
								int iStartWarVal = GET_TEAM(kPlayer.getTeam()).AI_startWarVal(kLoopPlayer.getTeam(), WARPLAN_TOTAL,
										true); // advc.001n
								if(GET_TEAM(kPlayer.getTeam()).isAtWar(kLoopPlayer.getTeam()))
									szString.append(CvWString::format(L"\n   At War:   "));
								else if (GET_TEAM(kPlayer.getTeam()).AI_getWarPlan(kLoopPlayer.getTeam()) != NO_WARPLAN)
									szString.append(CvWString::format(L"\n   Plan. War:"));
								else  if(!GET_TEAM(kPlayer.getTeam()).canDeclareWar(kLoopPlayer.getTeam()))
									szString.append(CvWString::format(L"\n   Can't War:"));
								else szString.append(CvWString::format(L"\n   No War:   "));
								if(iStartWarVal > 1200)
									szString.append(CvWString::format(SETCOLR L" %d" ENDCOLR, TEXT_COLOR("COLOR_RED"), iStartWarVal));
								else if(iStartWarVal > 600)
									szString.append(CvWString::format(SETCOLR L" %d" ENDCOLR, TEXT_COLOR("COLOR_YELLOW"), iStartWarVal));
								else szString.append(CvWString::format(L" %d", iStartWarVal));
								// advc.003j: Unused
								/*szString.append(CvWString::format(L" (%d", GET_TEAM(kPlayer.getTeam()).AI_calculatePlotWarValue(kLoopPlayer.getTeam())));
								szString.append(CvWString::format(L", %d", GET_TEAM(kPlayer.getTeam()).AI_calculateBonusWarValue(kLoopPlayer.getTeam())));
								szString.append(CvWString::format(L", %d", GET_TEAM(kPlayer.getTeam()).AI_calculateCapitalProximity(kLoopPlayer.getTeam())));*/
								szString.append(CvWString::format(L", %4s", GC.getInfo(GET_TEAM(kPlayer.getTeam()).AI_getAttitude(kLoopPlayer.getTeam())).getDescription(0)));
								szString.append(CvWString::format(L", %d%%)", 100-GET_TEAM(kPlayer.getTeam()).AI_noWarAttitudeProb(GET_TEAM(kPlayer.getTeam()).AI_getAttitude(kLoopPlayer.getTeam()))));
							}
						}
					}
					else szString.append(CvWString::format(L"-]"));
				}
			}
			else
			{
				int iCloseness = pPlotCity->AI_playerCloseness(eLoopPlayer, DEFAULT_PLAYER_CLOSENESS,
						true); // advc.001n
				if (iCloseness != 0)
				{
					if (bFirst)
					{
						bFirst = false;
						szString.append(CvWString::format(L"\n\nCloseness:"));
					}
					szString.append(CvWString::format(L"\n%s(%d) : %d ", kLoopPlayer.getName(),
							DEFAULT_PLAYER_CLOSENESS, iCloseness));
					szString.append(CvWString::format(L" [%d, ",
							kPlayer.AI_playerCloseness(eLoopPlayer, DEFAULT_PLAYER_CLOSENESS,
							true))); // advc.001n
					if (kPlayer.getTeam() != kLoopPlayer.getTeam())
					{
						szString.append(CvWString::format(L"%d]", GET_TEAM(kPlayer.getTeam()).
								AI_teamCloseness(kLoopPlayer.getTeam(), DEFAULT_PLAYER_CLOSENESS,
								false, true))); // advc.001n
					}
					else szString.append(CvWString::format(L"-]"));
				}
			}
			// BETTER_BTS_AI_MOD: END
		}

		int iWorkersHave = pPlotCity->AI_getWorkersHave();
		int iWorkersNeeded = pPlotCity->AI_getWorkersNeeded();
		szString.append(CvWString::format(L"\n\nWorkers H/N (%d , %d)", iWorkersHave, iWorkersNeeded));
		int iWorkBoatsNeeded = pPlotCity->AI_neededSeaWorkers();
		szString.append(CvWString::format(L"\n\nWorkboats Needed = %d", iWorkBoatsNeeded));
		CvPlayerAI const& kOwner = GET_PLAYER(kPlot.getOwner()); // advc
		/*for (int iI = 0; iI < GC.getNumCivicInfos(); iI++)
			szString.append(CvWString::format(L"\n %s = %d", GC.getInfo((CivicTypes)iI).getDescription(), kOwner.AI_civicValue((CivicTypes)iI)));*/ // BtS
		// BETTER_BTS_AI_MOD (K-Mod edited), Debug, 11/30/08, jdog5000
		// advc.007: Moved up; show this only on the capital.
		if(bAlt && kPlot.getPlotCity()->isCapital())
		{
			// advc: Redundant calculation of owned bonuses deleted
			EagerEnumMap<BonusClassTypes,int> aiBonusClassRevealed;
			EagerEnumMap<BonusClassTypes,int> aiBonusClassUnrevealed;
			EagerEnumMap<BonusClassTypes,int> aiBonusClassHave;
			kOwner.AI_calculateTechRevealBonuses(
					aiBonusClassRevealed, aiBonusClassUnrevealed, aiBonusClassHave);
			bool bDummy;
			FOR_EACH_ENUM(Tech)
			{
				int iPathLength = kOwner.findPathLength(eLoopTech, false);
				if (iPathLength <= 3 && !GET_TEAM(kPlot.getTeam()).isHasTech(eLoopTech))
				{
					szString.append(CvWString::format(L"\n%s(%d)=%8d",
							GC.getInfo(eLoopTech).getDescription(),
							iPathLength, kOwner.AI_techValue(eLoopTech,
							1, false, true, aiBonusClassRevealed,
							/*	advc (note): Could now disable randomization through
								bRandomize=false. Currently, the UI will show the values
								fluctuate randomly. Perhaps this is better than just
								hiding the randomness. */
							aiBonusClassUnrevealed, aiBonusClassHave)));
					szString.append(CvWString::format(L" (bld:%d, ",
							kOwner.AI_techBuildingValue(eLoopTech, true, bDummy)));
					int iObs = kOwner.AI_obsoleteBuildingPenalty(eLoopTech, true);
					if (iObs != 0)
						szString.append(CvWString::format(L"obs:%d, ", -iObs));
					// <k146>
					int iPrj = kOwner.AI_techProjectValue(eLoopTech, 1, bDummy);
					if (iPrj != 0)
						szString.append(CvWString::format(L"prj:%d, ", iPrj));
					// </k146>
					szString.append(CvWString::format(L"unt:%d)",
							kOwner.AI_techUnitValue(eLoopTech, 1, bDummy)));
				}
			}
		}
		/*  <advc.001n> AI_getNumAreaCitySites and AI_getNumAdjacentAreaCitySites
			call CvPlot::getFoundValue, which may cache its result. */
		if(!bConstCache)
		{
			int iAreaSiteBestValue = 0;
			int iNumAreaCitySites = kPlayer.AI_getNumAreaCitySites(kPlot.getArea(), iAreaSiteBestValue);
			int iOtherSiteBestValue = 0;
			int iNumOtherCitySites = (kPlot.waterArea() == NULL) ? 0 :
					kPlayer.AI_getNumAdjacentAreaCitySites(
					iOtherSiteBestValue, *kPlot.waterArea(), kPlot.area());
			szString.append(CvWString::format(L"\n\nArea Sites = %d (%d)",
					iNumAreaCitySites, iAreaSiteBestValue));
			szString.append(CvWString::format(L"\nOther Sites = %d (%d)",
					iNumOtherCitySites, iOtherSiteBestValue));
		}
	}
	else if (kPlot.isOwned() && pPlotCity == NULL &&
		!kPlot.isWater()) // advc.007
	{
		if (bAlt && !bShift)
		{
			CvTeamAI const& kPlotTeam = GET_TEAM(kPlot.getTeam());
			// <advc.opt> Don't compute this over and over as the user inspects the text
			static TeamTypes eCacheTeam = NO_TEAM;
			static bool bHasPath = false;
			static ArrayEnumMap<TeamTypes,bool> abHasPath;
			bool const bUpdCache = (kPlotTeam.getID() != eCacheTeam);
			eCacheTeam = kPlotTeam.getID();
			if (bUpdCache)
				bHasPath = kPlotTeam.AI_isHasPathToEnemyCity(kPlot); // </advc.opt>
			if (bHasPath)
				szString.append(CvWString::format(L"\nCan reach an enemy city\n\n"));
			else szString.append(CvWString::format(L"\nNo reachable enemy cities\n\n"));
			for (TeamIter<ALIVE> itTarget; itTarget.hasNext(); ++itTarget)
			{	// <advc.opt>
				if (bUpdCache)
				{
					abHasPath.set(itTarget->getID(),
							&kPlotTeam == &*itTarget || // advc.pf
							kPlotTeam.AI_isHasPathToEnemyCity(kPlot, *itTarget));
				} // </advc.opt>
				if (abHasPath.get(itTarget->getID()))
				{
					szString.append(CvWString::format(SETCOLR L"Can reach %s city" ENDCOLR,
							TEXT_COLOR("COLOR_GREEN"), itTarget->getName().c_str()));
				}
				else
				{
					szString.append(CvWString::format(SETCOLR L"Cannot reach any %s city" ENDCOLR,
							TEXT_COLOR("COLOR_NEGATIVE_TEXT"), itTarget->getName().c_str()));
				}
				if (kPlotTeam.isAtWar(itTarget->getID()))
					szString.append(CvWString::format(L" (enemy)"));
				szString.append(CvWString::format(L"\n"));
				// <advc.007>
				for (MemberIter itMember(itTarget->getID()); itMember.hasNext(); ++itMember)
				{
					szString.append(CvString::format("Bonus trade counter: %d\n",
							GET_PLAYER(kPlot.getOwner()).AI_getBonusTradeCounter(
							itMember->getID())));
				} // </advc.007>
			}
		}
		else if (bShift && bAlt)
		{
			FOR_EACH_ENUM(Civic)
			{
				szString.append(CvWString::format(L"\n %s = %d",
						GC.getInfo(eLoopCivic).getDescription(),
						GET_PLAYER(kPlot.getOwner()).AI_civicValue(eLoopCivic)));
			}
		}
		// advc.007: Commented out
		/*else if(kPlot.headUnitNode() == NULL) {
			std::vector<UnitAITypes> vecUnitAIs;
			if (kPlot.isFeature()) {
				szString.append(CvWString::format(L"\nDefense unit AIs:"));
				vecUnitAIs.push_back(UNITAI_CITY_DEFENSE);
				vecUnitAIs.push_back(UNITAI_COUNTER);
				vecUnitAIs.push_back(UNITAI_CITY_COUNTER);
			}
			else {
				szString.append(CvWString::format(L"\nAttack unit AIs:"));
				vecUnitAIs.push_back(UNITAI_ATTACK);
				vecUnitAIs.push_back(UNITAI_ATTACK_CITY);
				vecUnitAIs.push_back(UNITAI_COUNTER);
			}
			CvCity* pCloseCity = GC.getMap().findCity(x, y, kPlot.getOwner(), NO_TEAM, true);
			if (pCloseCity != NULL) {
				for (uint iI = 0; iI < vecUnitAIs.size(); iI++) {
					CvWString szTempString;
					getUnitAIString(szTempString, vecUnitAIs[iI]);
					szString.append(CvWString::format(L"\n  %s  ", szTempString.GetCString()));
					for (int iJ = 0; iJ < GC.getNumUnitClassInfos(); iJ++) {
						UnitTypes eUnit = (UnitTypes)GC.getInfo(kOwner.getCivilizationType()).getCivilizationUnits((UnitClassTypes)iJ);
						if (eUnit != NO_UNIT && pCloseCity->canTrain(eUnit)) {
							int iValue = kOwner.AI_unitValue(eUnit, vecUnitAIs[iI], kPlot.area());
							if (iValue > 0)
								szString.append(CvWString::format(L"\n %s = %d", GC.getInfo(eUnit).getDescription(), iValue));
						}
					}
				}
			}
		}*/
		// BETTER_BTS_AI_MOD: END
	}
	/*  <advc.027> Shift+Ctrl on a plot w/o a unit shows a breakdown of the
		area score computed in CvPlayer::findStartingArea. */
	{
		CvArea const& a = kPlot.getArea();
		PlayerTypes activePl = getActivePlayer();
		if(!a.isWater() && bShift && !bAlt && !kPlot.isUnit() && activePl != NO_PLAYER)
		{
			int total = 0; int tmp = 0;
			tmp=a.calculateTotalBestNatureYield();total+=tmp;szTempBuffer.Format(L"\nTotalBestNatureYield: %d", tmp); szString.append(szTempBuffer);
			tmp=a.countCoastalLand() * 2;szTempBuffer.Format(L"\n(CoastalLand*2: %d)", tmp); szString.append(szTempBuffer);
			tmp=a.getNumRiverEdges();szTempBuffer.Format(L"\n(RiverEdges: %d)", tmp); szString.append(szTempBuffer);
			tmp=GET_PLAYER(activePl).coastRiverStartingAreaScore(a);total+=tmp;szTempBuffer.Format(L"\nCoastRiverScore: %d", tmp); szString.append(szTempBuffer);
			tmp=a.getNumTiles()/2;total+=tmp;szTempBuffer.Format(L"\nTiles*0.5: %d", tmp); szString.append(szTempBuffer);
			tmp=fmath::round(a.getNumTotalBonuses() * 1.5);total+=tmp;szTempBuffer.Format(L"\nBonuses*1.5: %d", tmp); szString.append(szTempBuffer);
			tmp=100*fmath::round(std::min(NUM_CITY_PLOTS + 1, a.getNumTiles() + 1)/ (NUM_CITY_PLOTS + 1.0));total+=tmp;szTempBuffer.Format(L"\nTilePercent: %d", tmp); szString.append(szTempBuffer);
			szTempBuffer.Format(L"\nAreaScore: %d", total); szString.append(szTempBuffer);
		}
	} // </advc.027>
	if (bShift && !bAlt)
	{
		// BETTER_BTS_AI_MOD, DEBUG, 07/11/08, jdog5000
		// advc.007: BBAI showed this regardless of pressed buttons
		bool bFirst = true;
		for (int iK = 0; iK < MAX_TEAMS; ++iK)
		{
			TeamTypes eTeam = (TeamTypes)iK;
			if (!GET_TEAM(eTeam).isAlive())
				continue;
			if (kPlot.getBlockadedCount(eTeam) > 0)
			{
				if (bFirst)
				{
					szString.append(CvWString::format(SETCOLR, TEXT_COLOR("COLOR_NEGATIVE_TEXT")));
					szString.append(NEWLINE);
					szString.append(gDLL->getText("TXT_KEY_PLOT_BLOCKADED"));
					szString.append(CvWString::format( ENDCOLR));

					szString.append(CvWString::format(L"Teams:"));
					bFirst = false;
				}
				szString.append(CvWString::format(L" %s,", GET_TEAM(eTeam).getName().c_str()));
			}
		} // BETTER_BTS_AI_MOD: END
		// <advc.test>, advc.104b
		{
			CvUnit const* pUnit = gDLL->UI().getHeadSelectedUnit();
			CvPlot const* pPlot = gDLL->UI().getMouseOverPlot();
			if (pUnit != NULL && pPlot != NULL && pPlot->isRevealed(pUnit->getTeam()))
			{	// Avoid lag from computing the same path over and over
				static CvPlot const* pOldPlot = NULL;
				static CvUnit const* pOldUnit = NULL;
				static int iCost = MAX_INT;
				static int iLength = MAX_INT;
				if (pPlot != pOldPlot || pUnit != pOldUnit)
				{
					pOldPlot = pPlot;
					pOldUnit = pUnit;
					CvTeam const& kTeam = GET_TEAM(pUnit->getTeam());
					CvTeam const* pWarTeam = NULL;
					{
						TeamTypes ePlotTeam = pPlot->getTeam();
						if (ePlotTeam != NO_TEAM && ePlotTeam != pUnit->getTeam())
							pWarTeam = &GET_TEAM(ePlotTeam);
					}
					int const iMaxPath = 15 * pUnit->baseMoves();
					CvPlot const& kStart = pUnit->getPlot();
					CvPlot const& kDest = *pPlot;
					using namespace TeamPath;
					Mode eMode = LAND;
					if (pUnit->getDomainType() != DOMAIN_LAND)
					{
						TechTypes const eTech = pUnit->getUnitInfo().getPrereqAndTech();
						if (eTech != NO_TECH && GC.getInfo(eTech).getEra() >= 2)
							eMode = ANY_WATER;
						else eMode = SHALLOW_WATER;
					}
					// TeamPathFinder isn't intended for dynamic dispatch, so this is awkward.
					switch(eMode)
					{
					case LAND:
					{
						TeamPathFinder<LAND> pf(kTeam, pWarTeam, iMaxPath);
						if (pf.generatePath(kStart, kDest))
						{
							iCost = pf.getPathCost();
							iLength = pf.getPathLength();
							#ifdef FASSERT_ENABLE // symmetry test (UWAICache relies on that)
							bool bSuccess = pf.generatePath(kDest, kStart);
							FAssert(bSuccess);
							if (bSuccess)
							{
								FAssert(pf.getPathCost() == iCost);
								FAssert(pf.getPathLength() == iLength);
							}
							#endif
						}
						else iCost = iLength = MAX_INT;
						break;
					}
					case ANY_WATER:
					{
						TeamPathFinder<ANY_WATER> pf(kTeam, pWarTeam, iMaxPath);
						if (pf.generatePath(kStart, kDest))
						{
							iCost = pf.getPathCost();
							iLength = pf.getPathLength();
							#ifdef FASSERT_ENABLE
							bool bSuccess = pf.generatePath(kDest, kStart);
							FAssert(bSuccess);
							if (bSuccess)
							{
								FAssert(pf.getPathCost() == iCost);
								FAssert(pf.getPathLength() == iLength);
							}
							#endif
						}
						else iCost = iLength = MAX_INT;
						break;
					}
					case SHALLOW_WATER:
					{
						TeamPathFinder<SHALLOW_WATER> pf(kTeam, pWarTeam, iMaxPath);
						if (pf.generatePath(kStart, kDest))
						{
							iCost = pf.getPathCost();
							iLength = pf.getPathLength();
							#ifdef FASSERT_ENABLE
							bool bSuccess = pf.generatePath(kDest, kStart);
							FAssert(bSuccess);
							if (bSuccess)
							{
								FAssert(pf.getPathCost() == iCost);
								FAssert(pf.getPathLength() == iLength);
							}
							#endif
						}
						else iCost = iLength = MAX_INT;
						break;
					}
					}
				}
				szString.append(NEWLINE);
				if (iCost == MAX_INT)
				{
					FAssert(iLength == MAX_INT);
					szString.append(L"No team path");
				}
				else
				{
					szString.append(CvWString::format(
							L"Team path cost: %d, length: %d", iCost, iLength));
				}
			}
		} // </advc.test>
	}
	// <advc.017b> Sea explorers
	if(!bShift && !bAlt && kPlot.isWater() && kPlot.isOwned())
	{
		CvPlayerAI const& kOwner = GET_PLAYER(kPlot.getOwner());
		// This corresponds to code in CvCityAI::AI_chooseProduction
		int iHave =  kOwner.AI_totalWaterAreaUnitAIs(kPlot.getArea(), UNITAI_EXPLORE_SEA);
		int iNeeded = kOwner.AI_neededExplorers(kPlot.getArea());
		szString.append(CvWString::format(L"\nSea explorers H/N (%d , %d)", iHave, iNeeded));
	} // </advc.017b>
}

// advc.135c: Cut and pasted from setPlotHelp
void CvGameTextMgr::setPlotHelpDebug_ShiftOnly(CvWStringBuffer& szString, CvPlot const& kPlot) {

	szString.append(GC.getInfo(kPlot.getTerrainType()).getDescription());

	// advc.007: Commented out
	/*for (int iI = 0; iI < GC.getNumBonusInfos(); ++iI) {
		if (kPlot.isPlotGroupConnectedBonus(getActivePlayer(), ((BonusTypes)iI))) {
			szString.append(NEWLINE);
			szString.append(GC.getInfo((BonusTypes)iI).getDescription());
			szString.append(CvWString::format(L" (%d)", GET_PLAYER(getActivePlayer()).AI_bonusVal((BonusTypes)iI, 0, true)));
		}
	}*/

	CvWString szTempBuffer;
	int x = kPlot.getX();
	int y = kPlot.getY();

	if (kPlot.getPlotGroup(getActivePlayer()) != NULL)
	{
		szTempBuffer.Format(L"\n(%d, %d) group: %d", x, y,
				kPlot.getPlotGroup(getActivePlayer())->getID());
	}
	else szTempBuffer.Format(L"\n(%d, %d) group: (-1, -1)", x, y);
	szString.append(szTempBuffer);

	szTempBuffer.Format(L"\nArea: %d", kPlot.getArea().getID());
	szString.append(szTempBuffer);

	// BETTER_BTS_AI_MOD, Debug, 07/13/09, jdog5000: START
	szTempBuffer.Format(L"\nLatitude: %d", kPlot.getLatitude());
	szString.append(szTempBuffer);
	// BETTER_BTS_AI_MOD: END
	char tempChar = 'x';
	if(kPlot.getRiverNSDirection() == CARDINALDIRECTION_NORTH)
	{
		tempChar = 'N';
	}
	else if(kPlot.getRiverNSDirection() == CARDINALDIRECTION_SOUTH)
	{
		tempChar = 'S';
	}
	szTempBuffer.Format(L"\nNSRiverFlow: %c", tempChar);
	szString.append(szTempBuffer);

	tempChar = 'x';
	if(kPlot.getRiverWEDirection() == CARDINALDIRECTION_WEST)
	{
		tempChar = 'W';
	}
	else if(kPlot.getRiverWEDirection() == CARDINALDIRECTION_EAST)
	{
		tempChar = 'E';
	}
	szTempBuffer.Format(L"\nWERiverFlow: %c", tempChar);
	szString.append(szTempBuffer);

	if(kPlot.isRoute())
	{
		szTempBuffer.Format(L"\nRoute: %s", GC.getInfo(kPlot.getRouteType()).getDescription());
		szString.append(szTempBuffer);
	}

	if(kPlot.getRouteSymbol() != NULL)
	{
		szTempBuffer.Format(L"\nConnection: %i", gDLL->getRouteIFace()->getConnectionMask(kPlot.getRouteSymbol()));
		szString.append(szTempBuffer);
	}

	for (int iI = 0; iI < MAX_PLAYERS; ++iI)
	{
		if (GET_PLAYER((PlayerTypes)iI).isEverAlive()) // advc.099: was isAlive
		{
			if (kPlot.getCulture((PlayerTypes)iI) > 0)
			{
				szTempBuffer.Format(L"\n%s Culture: %d", GET_PLAYER((PlayerTypes)iI).getName(), kPlot.getCulture((PlayerTypes)iI));
				szString.append(szTempBuffer);
			}
		}
	} // advc.007: Use Alt for found values
	/*if(!GC.getGame().isNetworkMultiPlayer()) { // advc.001n: Might cache FoundValue
		PlayerTypes eActivePlayer = getActivePlayer();
		int iActualFoundValue = kPlot.getFoundValue(eActivePlayer);
		int iCalcFoundValue = GET_PLAYER(eActivePlayer).AI_foundValue(x, y, -1, false);
		int iStartingFoundValue = GET_PLAYER(eActivePlayer).AI_foundValue(x, y, -1, true);
		szTempBuffer.Format(L"\nFound Value: %d, (%d, %d)", iActualFoundValue, iCalcFoundValue, iStartingFoundValue);
		szString.append(szTempBuffer);
	}*/
	CvCityAI const* pWorkingCity = kPlot.AI_getWorkingCity();
	if (pWorkingCity != NULL)
	{
		CityPlotTypes ePlot = pWorkingCity->getCityPlotIndex(kPlot);
		int iBuildValue = pWorkingCity->AI_getBestBuildValue(ePlot);
		BuildTypes eBestBuild = pWorkingCity->AI_getBestBuild(ePlot);
		// BETTER_BTS_AI_MOD, Debug, 06/25/09, jdog5000: START
		szString.append(NEWLINE);

		int iFoodMultiplier, iProductionMultiplier, iCommerceMultiplier, iDesiredFoodChange;
		pWorkingCity->AI_getYieldMultipliers(iFoodMultiplier, iProductionMultiplier, iCommerceMultiplier, iDesiredFoodChange);

		szTempBuffer.Format(L"\n%s yield multipliers: ", pWorkingCity->getName().c_str());
		szString.append(szTempBuffer);
		szTempBuffer.Format(L"\n   Food %d, Prod %d, Com %d, DesFoodChange %d", iFoodMultiplier, iProductionMultiplier, iCommerceMultiplier, iDesiredFoodChange);
		szString.append(szTempBuffer);
		szTempBuffer.Format(L"\nTarget pop: %d, (%d good tiles)", pWorkingCity->AI_getTargetPopulation(), pWorkingCity->AI_countGoodPlots());
		szString.append(szTempBuffer);

		ImprovementTypes eImprovement = kPlot.getImprovementType();

		if (eBestBuild != NO_BUILD)
		{

			if (GC.getInfo(eBestBuild).getImprovement() != NO_IMPROVEMENT &&
				eImprovement != NO_IMPROVEMENT &&
				eImprovement != GC.getInfo(eBestBuild).getImprovement())
			{
				szTempBuffer.Format(SETCOLR L"\nBest Build: %s (%d) replacing %s" ENDCOLR,
						/*  advc.007: Was RED; now same color as in the else branch
							(but I'm not sure if the else branch is ever executed). */
						TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
						GC.getInfo(eBestBuild).getDescription(), iBuildValue,
						GC.getInfo(eImprovement).getDescription());
			}
			else
			{
				szTempBuffer.Format(SETCOLR L"\nBest Build: %s (%d)" ENDCOLR,
						TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
						GC.getInfo(eBestBuild).getDescription(), iBuildValue);
			}

			szString.append(szTempBuffer);
		}

		szTempBuffer.Format(L"\nActual Build Values: ");
		szString.append(szTempBuffer);

		FOR_EACH_ENUM(Improvement)
		{
			if (kPlot.canHaveImprovement(eLoopImprovement, pWorkingCity->getTeam()))
			{
				int iOtherBuildValue = pWorkingCity->AI_getImprovementValue(
						kPlot, eLoopImprovement, iFoodMultiplier,
						iProductionMultiplier, iCommerceMultiplier,
						iDesiredFoodChange);
				// <advc.007>
				/*  The same as above. Probably supposed to be the
					ImprovementValue of the current improvement, but that's always 0;
					I think the value already takes the current improvement into account. */
				/*int iOldValue =        pWorkingCity->AI_getImprovementValue(
						kPlot, (ImprovementTypes)iI, iFoodMultiplier,
						iProductionMultiplier, iCommerceMultiplier,
						iDesiredFoodChange);*/
				// Save space
				if(iOtherBuildValue == 0)
					continue;
				szTempBuffer.Format(L"\n   %s : %d",// (old %d)",
						GC.getInfo(eLoopImprovement).getDescription(),
						iOtherBuildValue/*, iOldValue*/); // </advc.007>
				szString.append(szTempBuffer);
			}
		}

		szTempBuffer.Format(L"\nStandard Build Values: ");
		szString.append(szTempBuffer);

		FOR_EACH_ENUM(Improvement)
		{
			int iOtherBuildValue = pWorkingCity->AI_getImprovementValue(
					kPlot, eLoopImprovement, 100, 100, 100, 0);
			if (iOtherBuildValue > 0)
			{
				szTempBuffer.Format(L"\n   %s : %d",
						GC.getInfo(eLoopImprovement).getDescription(),
						iOtherBuildValue);
				szString.append(szTempBuffer);
			}
		}

		szString.append(NEWLINE);
		// BETTER_BTS_AI_MOD: END
	}
	/*{
		szTempBuffer.Format(L"\nStack Str: land=%d(%d), sea=%d(%d), air=%d(%d)",
			kPlot.AI_sumStrength(NO_PLAYER, NO_PLAYER, DOMAIN_LAND, false, false, false),
			kPlot.AI_sumStrength(NO_PLAYER, NO_PLAYER, DOMAIN_LAND, true, false, false),
			kPlot.AI_sumStrength(NO_PLAYER, NO_PLAYER, DOMAIN_SEA, false, false, false),
			kPlot.AI_sumStrength(NO_PLAYER, NO_PLAYER, DOMAIN_SEA, true, false, false),
			kPlot.AI_sumStrength(NO_PLAYER, NO_PLAYER, DOMAIN_AIR, false, false, false),
			kPlot.AI_sumStrength(NO_PLAYER, NO_PLAYER, DOMAIN_AIR, true, false, false));
		szString.append(szTempBuffer);
	}*/

	// advc.007: Commented out. Takes up too much room.
	/*if (kPlot.getPlotCity() != NULL) {
		PlayerTypes ePlayer = kPlot.getOwner();
		CvPlayerAI& kPlayer = GET_PLAYER(ePlayer);
		szString.append(CvWString::format(L"\n\nAI unit class weights ..."));
		for (int iI = 0; iI < GC.getNumUnitClassInfos(); ++iI) {
			if (kPlayer.AI_getUnitClassWeight((UnitClassTypes)iI) != 0)
				szString.append(CvWString::format(L"\n%s = %d", GC.getInfo((UnitClassTypes)iI).getDescription(), kPlayer.AI_getUnitClassWeight((UnitClassTypes)iI)));
		}
		szString.append(CvWString::format(L"\n\nalso unit combat type weights..."));
		for (int iI = 0; iI < GC.getNumUnitCombatInfos(); ++iI) {
			if (kPlayer.AI_getUnitCombatWeight((UnitCombatTypes)iI) != 0)
				szString.append(CvWString::format(L"\n%s = % d", GC.getInfo((UnitCombatTypes)iI).getDescription(), kPlayer.AI_getUnitCombatWeight((UnitCombatTypes)iI)));
		}
	}*/
}

// advc.135c: Cut and pasted from setPlotHelp
void CvGameTextMgr::setPlotHelpDebug_AltOnly(CvWStringBuffer& szString, CvPlot const& kPlot)
{
	CvWString szTempBuffer;

	if (kPlot.isOwned())
	{
		CvPlayerAI const& kOwner = GET_PLAYER(kPlot.getOwner()); // advc
		szTempBuffer.Format(L"\nThis player has %d area cities",
				kPlot.getArea().getCitiesPerPlayer(kOwner.getID()));
		szString.append(szTempBuffer);
		FOR_EACH_ENUM(Religion)
		{
			int iNeededMissionaries = kOwner.AI_neededMissionaries(
					kPlot.getArea(), eLoopReligion);
			if (iNeededMissionaries > 0)
			{
				szTempBuffer.Format(L"\nNeeded %c missionaries = %d",
						GC.getInfo(eLoopReligion).getChar(), iNeededMissionaries);
				szString.append(szTempBuffer);
			}
		}

		int iOurDefense = kOwner.AI_localDefenceStrength(&kPlot, kPlot.getTeam(), DOMAIN_LAND, 0,
				true, false, true);
		int iEnemyOffense = kOwner.AI_localAttackStrength(&kPlot);
		if (iEnemyOffense > 0)
		{
			szString.append(CvWString::format(SETCOLR L"\nDanger: %.2f (%d/%d)" ENDCOLR,
				TEXT_COLOR("COLOR_NEGATIVE_TEXT"),
				(iEnemyOffense * 1.0f) / std::max(1, iOurDefense), iEnemyOffense, iOurDefense));
		}

		CvCityAI* pCity = kPlot.AI_getPlotCity();
		if (pCity != NULL)
		{
			/* szTempBuffer.Format(L"\n\nCulture Pressure Value = %d (%d)", pCity->AI_calculateCulturePressure(), pCity->culturePressureFactor());
			szString.append(szTempBuffer); */

			szTempBuffer.Format(L"\nWater World Percent = %d",
					pCity->AI_calculateWaterWorldPercent());
			szString.append(szTempBuffer);

			CvPlayerAI& kCityOwner = GET_PLAYER(pCity->getOwner());
			/*int iUnitCost = kPlayer.calculateUnitCost();
			int iTotalCosts = kPlayer.calculatePreInflatedCosts();
			int iUnitCostPercentage = (iUnitCost * 100) / std::max(1, iTotalCosts);
			szString.append(CvWString::format(L"\nUnit cost percentage: %d (%d / %d)", iUnitCostPercentage, iUnitCost, iTotalCosts));*/ // BtS
			// K-Mod
			int iBuildUnitProb = pCity->AI_buildUnitProb(); // advc (cast)
			szString.append(CvWString::format(L"\nUnit Cost: %d (max: %d)",
					kCityOwner.AI_unitCostPerMil(),
					kCityOwner.AI_maxUnitCostPerMil(pCity->area(), iBuildUnitProb)));
			// K-Mod end

			szString.append(CvWString::format(L"\nUpgrade all units: %d gold",
					kCityOwner.AI_getGoldToUpgradeAllUnits()));
			// K-Mod
			{
				int iValue = 0;
				FOR_EACH_ENUM(Commerce)
				{
					iValue += (kCityOwner.getCommerceRate(eLoopCommerce) *
							kCityOwner.AI_commerceWeight(eLoopCommerce)) / 100;
				}
				FOR_EACH_CITY(pLoopCity, kCityOwner)
					iValue += 2*pLoopCity->getYieldRate(YIELD_PRODUCTION);
				iValue /= kCityOwner.getTotalPopulation();
				szString.append(CvWString::format(L"\nAverage citizen value: %d", iValue));

				//
				szString.append(CvWString::format(L"\nBuild unit prob: %d%%",
						iBuildUnitProb));
				BuildingTypes eBestBuilding = pCity->AI_bestBuildingThreshold(0, 0, 0, true);
				int iBestBuildingValue = (eBestBuilding == NO_BUILDING) ? 0 :
						pCity->AI_buildingValue(eBestBuilding, 0, 0, true);

				// Note. cf. adjustments made in AI_chooseProduction
				if (GC.getNumEraInfos() > 1)
				{
					iBestBuildingValue *= 2*(GC.getNumEraInfos()-1) - kCityOwner.getCurrentEra();
					iBestBuildingValue /= GC.getNumEraInfos()-1;
				} // advc.001n: AI_getNumAreaCitySites could cache FoundValue
				if(!GC.getGame().isNetworkMultiPlayer())
				{
					int iTargetCities = GC.getInfo(GC.getMap().getWorldSize()).getTargetNumCities();
					int foo=-1;
					if (kCityOwner.AI_getNumAreaCitySites(kPlot.getArea(), foo) > 0 &&
						kCityOwner.getNumCities() < iTargetCities)
					{
						iBestBuildingValue *= kCityOwner.getNumCities() + iTargetCities;
						iBestBuildingValue /= 2*iTargetCities;
					}
				}
				//

				iBuildUnitProb *= (250 + iBestBuildingValue);
				iBuildUnitProb /= (100 + 3 * iBestBuildingValue);
				szString.append(CvWString::format(L" (%d%%)", iBuildUnitProb));
			}
			// K-Mod end

			szString.append(CvWString::format(L"\n\nRanks:"));
			szString.append(CvWString::format(L"\nPopulation:%d",
					pCity->findPopulationRank()));

			szString.append(CvWString::format(L"\nFood:%d(%d), ",
					pCity->findYieldRateRank(YIELD_FOOD),
					pCity->findBaseYieldRateRank(YIELD_FOOD)));
			szString.append(CvWString::format(L"Prod:%d(%d), ",
					pCity->findYieldRateRank(YIELD_PRODUCTION),
					pCity->findBaseYieldRateRank(YIELD_PRODUCTION)));
			szString.append(CvWString::format(L"Commerce:%d(%d)",
					pCity->findYieldRateRank(YIELD_COMMERCE),
					pCity->findBaseYieldRateRank(YIELD_COMMERCE)));

			szString.append(CvWString::format(L"\nGold:%d, ",
					pCity->findCommerceRateRank(COMMERCE_GOLD)));
			szString.append(CvWString::format(L"Research:%d, ",
					pCity->findCommerceRateRank(COMMERCE_RESEARCH)));
			szString.append(CvWString::format(L"Culture:%d",
					pCity->findCommerceRateRank(COMMERCE_CULTURE)));
		}
		szString.append(NEWLINE);

		// BETTER_BTS_AI_MOD, Debug, 06/11/08, jdog5000: START
		//AI strategies  // advc.007: bDebug=true argument added
		if (kOwner.AI_isDoStrategy(AI_STRATEGY_DAGGER, true))
		{
			szTempBuffer.Format(L"Dagger, ");
			szString.append(szTempBuffer);
		}
		if (kOwner.AI_isDoStrategy(AI_STRATEGY_CRUSH, true))
		{
			szTempBuffer.Format(L"Crush, ");
			szString.append(szTempBuffer);
		}
		if (kOwner.AI_isDoStrategy(AI_STRATEGY_ALERT1, true))
		{
			szTempBuffer.Format(L"Alert1, ");
			szString.append(szTempBuffer);
		}
		if (kOwner.AI_isDoStrategy(AI_STRATEGY_ALERT2, true))
		{
			szTempBuffer.Format(L"Alert2, ");
			szString.append(szTempBuffer);
		}
		if (kOwner.AI_isDoStrategy(AI_STRATEGY_TURTLE, true))
		{
			szTempBuffer.Format(L"Turtle, ");
			szString.append(szTempBuffer);
		}
		if (kOwner.AI_isDoStrategy(AI_STRATEGY_LAST_STAND, true))
		{
			szTempBuffer.Format(L"LastStand, ");
			szString.append(szTempBuffer);
		}
		if (kOwner.AI_isDoStrategy(AI_STRATEGY_FINAL_WAR, true))
		{
			szTempBuffer.Format(L"FinalWar, ");
			szString.append(szTempBuffer);
		}
		if (kOwner.AI_isDoStrategy(AI_STRATEGY_GET_BETTER_UNITS, true))
		{
			szTempBuffer.Format(L"GetBetterUnits, ");
			szString.append(szTempBuffer);
		}
		if (kOwner.AI_isDoStrategy(AI_STRATEGY_FASTMOVERS, true))
		{
			szTempBuffer.Format(L"FastMovers, ");
			szString.append(szTempBuffer);
		}
		if (kOwner.AI_isDoStrategy(AI_STRATEGY_LAND_BLITZ, true))
		{
			szTempBuffer.Format(L"LandBlitz, ");
			szString.append(szTempBuffer);
		}
		if (kOwner.AI_isDoStrategy(AI_STRATEGY_AIR_BLITZ, true))
		{
			szTempBuffer.Format(L"AirBlitz, ");
			szString.append(szTempBuffer);
		}
		if (kOwner.AI_isDoStrategy(AI_STRATEGY_OWABWNW, true))
		{
			szTempBuffer.Format(L"OWABWNW, ");
			szString.append(szTempBuffer);
		}
		if (kOwner.AI_isDoStrategy(AI_STRATEGY_PRODUCTION, true))
		{
			szTempBuffer.Format(L"Production, ");
			szString.append(szTempBuffer);
		}
		if (kOwner.AI_isDoStrategy(AI_STRATEGY_MISSIONARY, true))
		{
			szTempBuffer.Format(L"Missionary, ");
			szString.append(szTempBuffer);
		}
		if (kOwner.AI_isDoStrategy(AI_STRATEGY_BIG_ESPIONAGE, true))
		{
			szTempBuffer.Format(L"BigEspionage, ");
			szString.append(szTempBuffer);
		}
		if (kOwner.AI_isDoStrategy(AI_STRATEGY_ECONOMY_FOCUS, true)) // K-Mod
		{
			szTempBuffer.Format(L"EconomyFocus, ");
			szString.append(szTempBuffer);
		}
		if (kOwner.AI_isDoStrategy(AI_STRATEGY_ESPIONAGE_ECONOMY, true)) // K-Mod
		{
			szTempBuffer.Format(L"EspionageEconomy, ");
			szString.append(szTempBuffer);
		}

		//Area battle plans.
		AreaAITypes eAAI = kPlot.getArea().getAreaAIType(kPlot.getTeam());
		switch(eAAI) // advc: If-else replaced with switch
		{
		case AREAAI_OFFENSIVE: szTempBuffer.Format(L"\n Area AI = OFFENSIVE");
			break;
		case AREAAI_DEFENSIVE: szTempBuffer.Format(L"\n Area AI = DEFENSIVE");
			break;
		case AREAAI_MASSING: szTempBuffer.Format(L"\n Area AI = MASSING");
			break;
		case AREAAI_ASSAULT: szTempBuffer.Format(L"\n Area AI = ASSAULT");
			break;
		case AREAAI_ASSAULT_MASSING: szTempBuffer.Format(L"\n Area AI = ASSAULT_MASSING");
			break;
		case AREAAI_NEUTRAL: szTempBuffer.Format(L"\n Area AI = NEUTRAL");
			break;
		// <advc.007> These two were missing
		case AREAAI_ASSAULT_ASSIST: szTempBuffer.Format(L"\n Area AI = ASSAULT_ASSIST");
			break;
		default: szTempBuffer.Format(L"\n Area AI = None"); // </advc.007>
		}

		szString.append(szTempBuffer);
		CvTeamAI const& kPlotTeam = GET_TEAM(kPlot.getTeam()); // advc
		szString.append(CvWString::format(L"\n\nNum Wars: %d + %d minor",
				kPlotTeam.getNumWars(),
				kPlotTeam.getNumWars(false) - kPlotTeam.getNumWars()));
		szString.append(CvWString::format(L"\nWarplans:"));
		for (int iK = 0; iK < MAX_TEAMS; ++iK)
		{
			TeamTypes eTeam = (TeamTypes)iK;

			if (GET_TEAM(eTeam).isAlive() || GET_TEAM(eTeam).isBarbarian())
			{
				WarPlanTypes eWarPlan = kPlotTeam.AI_getWarPlan(eTeam);
				switch(eWarPlan) { // advc: if-else replaced with switch
				case WARPLAN_ATTACKED:
					szString.append(CvWString::format(L"\n%s: ATTACKED",
							GET_TEAM(eTeam).getName().c_str()));
					break;
				case WARPLAN_ATTACKED_RECENT:
					szString.append(CvWString::format(L"\n%s: ATTACKED_RECENT",
							GET_TEAM(eTeam).getName().c_str()));
					break;
				case WARPLAN_PREPARING_LIMITED:
					szString.append(CvWString::format(L"\n%s: PREP_LIM",
							GET_TEAM(eTeam).getName().c_str()));
					break;
				case WARPLAN_PREPARING_TOTAL:
					szString.append(CvWString::format(L"\n%s: PREP_TOTAL",
							GET_TEAM(eTeam).getName().c_str()));
					break;
				case WARPLAN_LIMITED:
					szString.append(CvWString::format(L"\n%s: LIMITED",
							GET_TEAM(eTeam).getName().c_str()));
					break;
				case WARPLAN_TOTAL:
					szString.append(CvWString::format(L"\n%s: TOTAL",
							GET_TEAM(eTeam).getName().c_str()));
					break;
				case WARPLAN_DOGPILE:
					szString.append(CvWString::format(L"\n%s: DOGPILE",
							GET_TEAM(eTeam).getName().c_str()));
					break;
				default:
					if (kPlotTeam.isAtWar(eTeam))
					{
						szString.append(CvWString::format(
								SETCOLR L"\n%s: NO_WARPLAN!" ENDCOLR,
								TEXT_COLOR("COLOR_WARNING_TEXT"),
								GET_TEAM(eTeam).getName().c_str()));
					}
				}
			}

			if (kPlotTeam.isMinorCiv() || kPlotTeam.isBarbarian())
			{
				if (kPlot.getTeam() != eTeam && !kPlotTeam.isAtWar(eTeam))
				{
					szString.append(CvWString::format(
							SETCOLR L"\n%s: minor/barb not at war!" ENDCOLR,
							TEXT_COLOR("COLOR_WARNING_TEXT"),
							GET_TEAM(eTeam).getName().c_str()));
				}
			}
		}

		CvCity const* pTargetCity = kPlot.getArea().AI_getTargetCity(kPlot.getOwner());
		if (pTargetCity != NULL)
		{
			szString.append(CvWString::format(L"\nTarget City: %s",
					pTargetCity->getName().c_str()));
		}
		else szString.append(CvWString::format(L"\nTarget City: None"));
		// BETTER_BTS_AI_MOD: END
	} // end if (kPlot.isOwned())

	bool bFirst = true;
	// <advc>
	int x = kPlot.getX();
	int y = kPlot.getY(); // </advc>
	for (int iI = 0; iI < MAX_PLAYERS; ++iI)
	{
		PlayerTypes ePlayer = (PlayerTypes)iI;
		CvPlayerAI& kLoopPlayer = GET_PLAYER(ePlayer);

		if (kLoopPlayer.isAlive() &&
			// advc.001n: Might cache FoundValue
			!GC.getGame().isNetworkMultiPlayer())
		{ // <advc.007> Moved up, and skip unrevealed.
			bool bRevealed = kPlot.isRevealed(kLoopPlayer.getTeam());
			if(!bRevealed)
				continue; // </advc.007>
			int iActualFoundValue = kPlot.getFoundValue(ePlayer, /* advc.052: */ true);
			//int iCalcFoundValue = kPlayer.AI_foundValue(x, y, -1, false);
			// <advc.007>
			CitySiteEvaluator citySiteEval(kLoopPlayer);
			citySiteEval.setDebug(true);
			int iCalcFoundValue = citySiteEval.evaluate(x, y);
			int const iStartingFoundValue = 0;
			// Gets in the way of debugging bStartingLoc=false </advc.007>
					//=kPlayer.AI_foundValue(x, y, -1, true);
			int iBestAreaFoundValue = kPlot.getArea().getBestFoundValue(ePlayer);
			int iCitySiteBestValue=-1;
			int iNumAreaCitySites = kLoopPlayer.AI_getNumAreaCitySites(
					kPlot.getArea(), iCitySiteBestValue);

			if (iActualFoundValue > 0 || iCalcFoundValue > 0 || iStartingFoundValue > 0 ||
				(kPlot.getOwner() == iI && iBestAreaFoundValue > 0))
			{
				if (bFirst)
				{
					szString.append(CvWString::format(
							SETCOLR L"\nFound Values:" ENDCOLR,
							TEXT_COLOR("COLOR_UNIT_TEXT")));
					bFirst = false;
				}

				szString.append(NEWLINE);

				szString.append(CvWString::format(
						SETCOLR, TEXT_COLOR(bRevealed ?
						((iActualFoundValue > 0 && iActualFoundValue == iBestAreaFoundValue) ?
						"COLOR_UNIT_TEXT" : "COLOR_ALT_HIGHLIGHT_TEXT") :
						"COLOR_HIGHLIGHT_TEXT")));

				//if (!bRevealed) // advc.007
				{
					szString.append(CvWString::format(L"("));
				}

				szString.append(CvWString::format(L"%s: %d", kLoopPlayer.getName(),
						iCalcFoundValue)); // advc.007: Swapped with iActual

				//if (!bRevealed) // advc.007
				{
					szString.append(CvWString::format(L")"));
				}

				szString.append(CvWString::format(ENDCOLR));

				if (iCalcFoundValue > 0 || iStartingFoundValue > 0)
				{
					szTempBuffer.Format(L" (%d,s:%d), thresh: %d",
							iActualFoundValue, // advc.007: Swapped with iCalc
							iStartingFoundValue,
							// advc.007: thresh added
							kLoopPlayer.AI_getMinFoundValue());
					szString.append(szTempBuffer);
				}
				// advc: Moved to AIFoundValue class; difficult to access that from here.
				/*int iDeadlockCount = kLoopPlayer.AI_countDeadlockedBonuses(&kPlot);
				if (iDeadlockCount > 0) {
					szTempBuffer.Format(L", " SETCOLR L"d=%d" ENDCOLR, TEXT_COLOR("COLOR_NEGATIVE_TEXT"), iDeadlockCount);
					szString.append(szTempBuffer);
				}*/

				if (kLoopPlayer.AI_isPlotCitySite(kPlot))
				{
					szTempBuffer.Format(L", " SETCOLR L"X" ENDCOLR,
							TEXT_COLOR("COLOR_UNIT_TEXT"));
					szString.append(szTempBuffer);
				}

				if (iBestAreaFoundValue > 0 || iNumAreaCitySites > 0)
				{
					int iBestFoundValue = kLoopPlayer.findBestFoundValue();

					szTempBuffer.Format(L"\n  Area Best = %d, Best = %d, Sites = %d",
							iBestAreaFoundValue, iBestFoundValue, iNumAreaCitySites);
					szString.append(szTempBuffer);
				}
			}
		}
	}
}

// advc.135c: Cut and pasted from setPlotHelp
void CvGameTextMgr::setPlotHelpDebug_ShiftAltOnly(CvWStringBuffer& szString, CvPlot const& kPlot)
{
	CvWString szTempBuffer;

	CvCityAI* pCity = kPlot.AI_getWorkingCity();
	if (pCity != NULL)
	{
		// some functions we want to call are not in CvCity, worse some are protected, so made us a friend

		CvPlayerAI const& kCityOwner = GET_PLAYER(pCity->getOwner()); // advc
		//bool bAvoidGrowth = pCity->.AI_avoidGrowth();
		//bool bIgnoreGrowth = pCity->.AI_ignoreGrowth();
		int iGrowthValue = pCity->AI_growthValuePerFood();

		// if we over the city, then do an array of all the plots
		if (kPlot.getPlotCity() != NULL)
		{
			// check avoid growth
			/* if (bAvoidGrowth || bIgnoreGrowth) {
				// red color
				szString.append(CvWString::format(SETCOLR, TEXT_COLOR("COLOR_NEGATIVE_TEXT")));
				if (bAvoidGrowth) {
					szString.append(CvWString::format(L"AvoidGrowth"));
					if (bIgnoreGrowth)
						szString.append(CvWString::format(L", "));
				}
				if (bIgnoreGrowth)
					szString.append(CvWString::format(L"IgnoreGrowth"));
				// end color
				szString.append(CvWString::format( ENDCOLR L"\n"));
			} */

			// if control key is down, ignore food
			bool bIgnoreFood = GC.ctrlKey();

			// line one is: blank, 20, 9, 10, blank
			setCityPlotYieldValueString(szString, pCity, -1, bIgnoreFood, iGrowthValue);
			setCityPlotYieldValueString(szString, pCity, 20, bIgnoreFood, iGrowthValue);
			setCityPlotYieldValueString(szString, pCity, 9, bIgnoreFood, iGrowthValue);
			setCityPlotYieldValueString(szString, pCity, 10, bIgnoreFood, iGrowthValue);
			szString.append(L"\n");

			// line two is: 19, 8, 1, 2, 11
			setCityPlotYieldValueString(szString, pCity, 19, bIgnoreFood, iGrowthValue);
			setCityPlotYieldValueString(szString, pCity, 8, bIgnoreFood, iGrowthValue);
			setCityPlotYieldValueString(szString, pCity, 1, bIgnoreFood, iGrowthValue);
			setCityPlotYieldValueString(szString, pCity, 2, bIgnoreFood, iGrowthValue);
			setCityPlotYieldValueString(szString, pCity, 11, bIgnoreFood, iGrowthValue);
			szString.append(L"\n");

			// line three is: 18, 7, 0, 3, 12
			setCityPlotYieldValueString(szString, pCity, 18, bIgnoreFood, iGrowthValue);
			setCityPlotYieldValueString(szString, pCity, 7, bIgnoreFood, iGrowthValue);
			setCityPlotYieldValueString(szString, pCity, 0, bIgnoreFood, iGrowthValue);
			setCityPlotYieldValueString(szString, pCity, 3, bIgnoreFood, iGrowthValue);
			setCityPlotYieldValueString(szString, pCity, 12, bIgnoreFood, iGrowthValue);
			szString.append(L"\n");

			// line four is: 17, 6, 5, 4, 13
			setCityPlotYieldValueString(szString, pCity, 17, bIgnoreFood, iGrowthValue);
			setCityPlotYieldValueString(szString, pCity, 6, bIgnoreFood, iGrowthValue);
			setCityPlotYieldValueString(szString, pCity, 5, bIgnoreFood, iGrowthValue);
			setCityPlotYieldValueString(szString, pCity, 4, bIgnoreFood, iGrowthValue);
			setCityPlotYieldValueString(szString, pCity, 13, bIgnoreFood, iGrowthValue);
			szString.append(L"\n");

			// line five is: blank, 16, 15, 14, blank
			setCityPlotYieldValueString(szString, pCity, -1, bIgnoreFood, iGrowthValue);
			setCityPlotYieldValueString(szString, pCity, 16, bIgnoreFood, iGrowthValue);
			setCityPlotYieldValueString(szString, pCity, 15, bIgnoreFood, iGrowthValue);
			setCityPlotYieldValueString(szString, pCity, 14, bIgnoreFood, iGrowthValue);

			// show specialist values too
			for (int iI = 0; iI < GC.getNumSpecialistInfos(); ++iI)
			{
				int iMaxThisSpecialist = pCity->getMaxSpecialistCount((SpecialistTypes) iI);
				int iSpecialistCount = pCity->getSpecialistCount((SpecialistTypes) iI);
				bool bUsingSpecialist = (iSpecialistCount > 0);
				bool bDefaultSpecialist = (iI == GC.getDEFAULT_SPECIALIST());

				// can this city have any of this specialist?
				if (iMaxThisSpecialist > 0 || bDefaultSpecialist)
				{
					// start color
					if (pCity->getForceSpecialistCount((SpecialistTypes) iI) > 0)
						szString.append(CvWString::format(L"\n" SETCOLR, TEXT_COLOR("COLOR_NEGATIVE_TEXT")));
					else if (bUsingSpecialist)
						szString.append(CvWString::format(L"\n" SETCOLR, TEXT_COLOR("COLOR_ALT_HIGHLIGHT_TEXT")));
					else
						szString.append(CvWString::format(L"\n" SETCOLR, TEXT_COLOR("COLOR_HIGHLIGHT_TEXT")));

					// add name
					szString.append(GC.getInfo((SpecialistTypes) iI).getDescription());

					// end color
					szString.append(CvWString::format(ENDCOLR));

					// add usage
					szString.append(CvWString::format(L": (%d/%d) ", iSpecialistCount, iMaxThisSpecialist));

					// add value
					int iValue = pCity->AI_specialistValue((SpecialistTypes)iI, bUsingSpecialist, false, iGrowthValue);
					setYieldValueString(szString, iValue, bUsingSpecialist);
				}
			}
			{
				/* int iFood = kCityOwner.AI_averageYieldMultiplier(YIELD_FOOD);
				int iHammer = kCityOwner.AI_averageYieldMultiplier(YIELD_PRODUCTION);
				int iCommerce = kCityOwner.AI_averageYieldMultiplier(YIELD_COMMERCE);

				szString.append(CvWString::format(L"\nPlayer avg:       (f%d, h%d, c%d)", iFood, iHammer, iCommerce));

				iFood = pCity->AI_yieldMultiplier(YIELD_FOOD);
				iHammer = pCity->AI_yieldMultiplier(YIELD_PRODUCTION);
				iCommerce = pCity->AI_yieldMultiplier(YIELD_COMMERCE);

				szString.append(CvWString::format(L"\nCity yield mults: (f%d, h%d, c%d)", iFood, iHammer, iCommerce));

				iFood = kCityAI.AI_specialYieldMultiplier(YIELD_FOOD);
				iHammer = kCityAI.AI_specialYieldMultiplier(YIELD_PRODUCTION);
				iCommerce = kCityAI.AI_specialYieldMultiplier(YIELD_COMMERCE);

				szString.append(CvWString::format(L"\nCity spec mults:  (f%d, h%d, c%d)", iFood, iHammer, iCommerce)); */

				// K-Mod
				szString.append(L"\n\nPlayer avg:       (");
				for (YieldTypes i = (YieldTypes)0; i < NUM_YIELD_TYPES; i = (YieldTypes)(i+1))
					szString.append(CvWString::format(L"%s%d%c", i == 0 ? L"" : L", ", kCityOwner.AI_averageYieldMultiplier(i), GC.getInfo(i).getChar()));
				szString.append(L")");

				szString.append(L"\nCity yield mults: (");
				for (YieldTypes i = (YieldTypes)0; i < NUM_YIELD_TYPES; i = (YieldTypes)(i+1))
					szString.append(CvWString::format(L"%s%d%c", i == 0 ? L"" : L", ", pCity->AI_yieldMultiplier(i), GC.getInfo(i).getChar()));
				szString.append(L")");

				szString.append(L"\nCity spec mults:  (");
				for (YieldTypes i = (YieldTypes)0; i < NUM_YIELD_TYPES; i = (YieldTypes)(i+1))
					szString.append(CvWString::format(L"%s%d%c", i == 0 ? L"" : L", ", pCity->AI_specialYieldMultiplier(i), GC.getInfo(i).getChar()));
				szString.append(L")");
				szString.append(CvWString::format(L"\nCity weights: ("));
				for (CommerceTypes i = (CommerceTypes)0; i < NUM_COMMERCE_TYPES; i=(CommerceTypes)(i+1))
					szString.append(CvWString::format(L"%s%d%c", i == 0 ? L"" : L", ", kCityOwner.AI_commerceWeight(i, pCity), GC.getInfo(i).getChar()));
				szString.append(L")");
				// K-Mod end

				szString.append(CvWString::format(L"\nExchange"));
				for (int iI = 0; iI < NUM_COMMERCE_TYPES; ++iI)
				{
					int iCommerce = kCityOwner.AI_averageCommerceExchange((CommerceTypes)iI);
					szTempBuffer.Format(L", %d%c", iCommerce, GC.getInfo((CommerceTypes) iI).getChar());
					szString.append(szTempBuffer);
				}

				// BBAI
				szString.append(CvWString::format(L"\nAvg mults"));
				for (int iI = 0; iI < NUM_COMMERCE_TYPES; ++iI)
				{
					int iCommerce = kCityOwner.AI_averageCommerceMultiplier((CommerceTypes)iI);
					szTempBuffer.Format(L", %d%c", iCommerce, GC.getInfo((CommerceTypes) iI).getChar());
					szString.append(szTempBuffer);
				}
				// BBAI end
				// K-Mod
				szString.append(CvWString::format(L"\nAvg %c pressure: %d",
					GC.getInfo(COMMERCE_CULTURE).getChar(),
					kCityOwner.AI_averageCulturePressure()));
				// K-Mod end

				if (kCityOwner.AI_isFinancialTrouble())
				{
					szTempBuffer.Format(L"$$$!!!");
					szString.append(szTempBuffer);
				}
			}
		}
		else
		{
			bool bWorkingPlot = pCity->isWorkingPlot(kPlot);

			if (bWorkingPlot)
				szTempBuffer.Format( SETCOLR L"%s is working" ENDCOLR, TEXT_COLOR("COLOR_ALT_HIGHLIGHT_TEXT"), pCity->getName().GetCString());
			else
				szTempBuffer.Format( SETCOLR L"%s not working" ENDCOLR, TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"), pCity->getName().GetCString());
			szString.append(szTempBuffer);

			int iValue = pCity->AI_plotValue(kPlot, bWorkingPlot, false, false, iGrowthValue);
			int iRawValue = pCity->AI_plotValue(kPlot, bWorkingPlot, true, false, iGrowthValue);
			int iMagicValue = pCity->AI_getPlotMagicValue(kPlot, pCity->healthRate() == 0);

			szTempBuffer.Format(L"\nvalue = %d\nraw value = %d\nmagic value = %d", iValue, iRawValue, iMagicValue);
			szString.append(szTempBuffer);
		}
	} // <advc.007> For advc.040
	if(kPlot.isOwned())
	{
		szString.append(CvString::format("\nWorkers needed in area: %d\n",
				GET_PLAYER(kPlot.getOwner()).AI_neededWorkers(kPlot.getArea())));
	} // </advc.007>

	// calc some bonus info
	/*if (GC.getGame().isDebugMode())
		eBonus = kPlot.getBonusType();
	else eBonus = kPlot.getBonusType(getActiveTeam());*/
	BonusTypes eBonus = kPlot.getBonusType(); // advc.135c: Debug mode is guaranteed
	if (eBonus != NO_BONUS)
	{
		szString.append(CvWString::format(L"\n%s values:", GC.getInfo(eBonus).getDescription()));
		for (int iPlayerIndex = 0; iPlayerIndex < MAX_PLAYERS; iPlayerIndex++)
		{
			CvPlayerAI& kLoopPlayer = GET_PLAYER((PlayerTypes) iPlayerIndex);
			if (kLoopPlayer.isAlive())
			{	//szString.append(CvWString::format(L"\n %s: %d", kLoopPlayer.getName(), kLoopPlayer.AI_bonusVal(eBonus)));
				// BETTER_BTS_AI_MOD, DEBUG, 07/11/08, jdog5000: START
				BonusTypes eNonObsBonus = kPlot.getNonObsoleteBonusType(kLoopPlayer.getTeam());
				if (eNonObsBonus != NO_BONUS)
				{
					szString.append(CvWString::format(L"\n %s: %d", kLoopPlayer.getName(), kLoopPlayer.AI_bonusVal(eNonObsBonus, 0, true)));
				}
☻				else
				{
					szString.append(CvWString::format(L"\n %s: unknown (%d)", kLoopPlayer.getName(), kLoopPlayer.AI_bonusVal(eBonus, 0, true)));
				}
				// BETTER_BTS_AI_MOD: END
			}
		}
	}
}
// BULL - Leaderhead Relations - start
/*  Shows the peace/war/enemy/pact status between eThisTeam and all rivals known to the active player.
	Relations for the active player are shown first. */
void CvGameTextMgr::getAllRelationsString(CvWStringBuffer& szString, TeamTypes eThisTeam)
{
	getActiveTeamRelationsString(szString, eThisTeam);
	getOtherRelationsString(szString, eThisTeam, NO_TEAM, getActiveTeam());
}

// Shows the peace/war/enemy/pact status between eThisTeam and the active player.
void CvGameTextMgr::getActiveTeamRelationsString(CvWStringBuffer& szString, TeamTypes eThisTeam)
{
	CvTeamAI const& kThisTeam = GET_TEAM(eThisTeam);
	TeamTypes const eActiveTeam = getActiveTeam();
	if(!kThisTeam.isHasMet(eActiveTeam))
		return;

	if(kThisTeam.isAtWar(eActiveTeam))
	{
		szString.append(NEWLINE);
		szString.append(gDLL->getText(L"TXT_KEY_AT_WAR_WITH_YOU"));
	}
	// advc: Covered by active deals
	/*else if (kThisTeam.isForcePeace(eActiveTeam)) {
		szString.append(NEWLINE);
		szString.append(gDLL->getText(L"TXT_KEY_PEACE_TREATY_WITH_YOU"));
	}*/
	if(!kThisTeam.isHuman() && kThisTeam.AI_getWorstEnemy() == eActiveTeam)
	{
		szString.append(NEWLINE);
		szString.append(gDLL->getText(L"TXT_KEY_WORST_ENEMY_IS_YOU"));
	}
	// advc: Covered by active deals
	/*if(kThisTeam.isDefensivePact(eActiveTeam)) {
		szString.append(NEWLINE);
		szString.append(gDLL->getText(L"TXT_KEY_DEFENSIVE_PACT_WITH_YOU"));
	}*/
}

void CvGameTextMgr::getOtherRelationsString(CvWStringBuffer& szString,
		PlayerTypes eThisPlayer, PlayerTypes eOtherPlayer)
{
	if(eThisPlayer == NO_PLAYER || eOtherPlayer == NO_PLAYER)
		return;
	getOtherRelationsString(szString, TEAMID(eThisPlayer), TEAMID(eOtherPlayer), NO_TEAM);
}

/*  Shows the peace/war/enemy/pact status between eThisPlayer and all rivals known to the active player.
	If eOtherTeam is not NO_TEAM, only relations between it and eThisTeam are shown.
	If eSkipTeam is not NO_TEAM, relations involving it are not shown. */
/*  advc: This BULL function replaces CvGameTextMgr::getOtherRelationsString(
	CvWStringBuffer&, PlayerTypes, PlayerTypes). I've merged just one K-Mod
	change from the latter. */
void CvGameTextMgr::getOtherRelationsString(CvWStringBuffer& szString,
	TeamTypes eThisTeam, /* (advc: unused) */ TeamTypes eOtherTeam,
	TeamTypes eSkipTeam)
{
	if(eThisTeam == NO_TEAM)
		return;
	CvWString szWar, szPeace, szEnemy, szPact;
	bool bFirstWar = true, bFirstPeace = true, bFirstEnemy = true, bFirstPact = true;
	for (TeamAIIter<MAJOR_CIV,OTHER_KNOWN_TO> itThird(eThisTeam);
		itThird.hasNext(); ++itThird)
	{
		/*	K-Mod. (show "at war" even for the civ selected.)
			(advc: And war-related info like DP also) */
		if (itThird->getID() == eSkipTeam) //|| (eOtherTeam != NO_TEAM && itThird->getID() != eOtherTeam)
			continue;
		if (!itThird->isHasMet(getActiveTeam()))
			continue;
		if (itThird->isAtWar(eThisTeam))
			setListHelp(szWar, L"", itThird->getName().GetCString(), L", ", bFirstWar);
		else if (itThird->isForcePeace(eThisTeam))
			setListHelp(szPeace, L"", itThird->getName().GetCString(), L", ", bFirstPeace);
		if (!itThird->isHuman() && itThird->AI_getWorstEnemy() == eThisTeam)
			setListHelp(szEnemy, L"", itThird->getName().GetCString(), L", ", bFirstEnemy);
		if (itThird->isDefensivePact(eThisTeam))
			setListHelp(szPact, L"", itThird->getName().GetCString(), L", ", bFirstPact);
	}
	if(!szWar.empty())
	{
		szString.append(NEWLINE);
		szString.append(gDLL->getText(L"TXT_KEY_AT_WAR_WITH", szWar.GetCString()));
	}
	/*  Show only the teams whose enemy ThisTeam is - and not ThisTeam's enemy;
		too confusing to show both. */
	/*if(!kThisTeam.isHuman()) {
		TeamTypes eWorstEnemy = kThisTeam.AI_getWorstEnemy();
		if(eWorstEnemy != NO_TEAM && eWorstEnemy != eSkipTeam &&
				(eOtherTeam == NO_TEAM || eWorstEnemy == eOtherTeam) &&
				GET_TEAM(eWorstEnemy).isHasMet(getActiveTeam())) {
			szString.append(NEWLINE);
			szString.append(gDLL->getText(L"TXT_KEY_WORST_ENEMY_IS",
					GET_TEAM(eWorstEnemy).getName().GetCString()));
		}
	}*/
	if(!szEnemy.empty())
	{
		szString.append(NEWLINE);
		szString.append(gDLL->getText(L"TXT_KEY_WORST_ENEMY_OF", szEnemy.GetCString()));
	}
} // BULL - Leaderhead Relations - end

void CvGameTextMgr::setCityPlotYieldValueString(CvWStringBuffer &szString,
	CvCityAI* pCity, // advc.003u: Was CvCity*; this function is for AI debugging.
	int iPlotIndex, bool bIgnoreFood, int iGrowthValue)
{
	PROFILE_FUNC();

	// advc.enum: Too many call locations; can't change the type of iPlotIndex.
	CityPlotTypes ePlot = (CityPlotTypes)iPlotIndex;
	CvPlot* pPlot = NULL;
	if (ePlot >= 0 && ePlot < NUM_CITY_PLOTS)
		pPlot = pCity->getCityIndexPlot(ePlot);

	if (pPlot != NULL && pPlot->getWorkingCity() == pCity)
	{
		bool bWorkingPlot = pCity->isWorkingPlot(ePlot);
		int iValue = pCity->AI_plotValue(*pPlot, bWorkingPlot, bIgnoreFood, false, iGrowthValue);
		setYieldValueString(szString, iValue, /*bActive*/ bWorkingPlot);
	}
	else setYieldValueString(szString, 0, /*bActive*/ false, /*bMakeWhitespace*/ true);
}

void CvGameTextMgr::setYieldValueString(CvWStringBuffer &szString,
	int iValue, bool bActive, bool bMakeWhitespace)
{
	PROFILE_FUNC();

	//static bool bUseFloats = false;

	if (bActive)
		szString.append(CvWString::format(SETCOLR, TEXT_COLOR("COLOR_ALT_HIGHLIGHT_TEXT")));
	else szString.append(CvWString::format(SETCOLR, TEXT_COLOR("COLOR_HIGHLIGHT_TEXT")));

	if (!bMakeWhitespace)
	{
		bool const bUseFloats = false; // advc
		if (bUseFloats)
		{
			float fValue = ((float) iValue) / 10000;
			szString.append(CvWString::format(L"%2.3f " ENDCOLR, fValue));
		}
		else szString.append(CvWString::format(L"%05d  " ENDCOLR, iValue/10));
	}
	else szString.append(CvWString::format(L"           " ENDCOLR));
}


void CvGameTextMgr::setCityBarHelp(CvWStringBuffer &szString, CvCity const& kCity)
{
	PROFILE_FUNC();
	bool const bPopup = gDLL->UI().isPopupUp(); // advc.186b
	CvWString szTempBuffer(kCity.getName());
	// <advc.186b>
	if (bPopup)
	{
		szTempBuffer.Format(SETCOLR L"%s" ENDCOLR,
				TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"), szTempBuffer.GetCString());
	} // </advc.186b>
	szString.append(szTempBuffer);
	PlayerTypes const eOwner = kCity.getOwner();
	// <advc.186>
	// BULL - Health - start
	//if (BUGOption::isEnabled("CityBar__Health", true))
	{
		int iHealth = kCity.goodHealth() - kCity.badHealth();
		szTempBuffer.Format(L", %s%d%c", iHealth >= 0 ? L"+" : L"", abs(iHealth),
				gDLL->getSymbolID(iHealth >= 0 ? HEALTHY_CHAR : UNHEALTHY_CHAR));
		szString.append(szTempBuffer);
	} // BULL - Health - end
	// BULL - Happiness - start
	//if (BUGOption::isEnabled("CityBar__Happiness", true))
	{
		if (kCity.isDisorder())
		{
			int iAngryPop = kCity.angryPopulation();
			if (iAngryPop > 0)
			{
				szTempBuffer.Format(L", %d%c", iAngryPop,
						gDLL->getSymbolID(ANGRY_POP_CHAR));
				szString.append(szTempBuffer);
			}
		}
		else
		{
			int iHappy = kCity.happyLevel() - kCity.unhappyLevel();
			szTempBuffer.Format(L", %s%d%c", iHappy >= 0 ? L"+" : L"", abs(iHappy),
					gDLL->getSymbolID(iHappy >= 0 ? HAPPY_CHAR : UNHAPPY_CHAR));
			szString.append(szTempBuffer);
		}
	} // BULL - Happiness - end
	// Based on BULL code ("Hurry Anger Turns")
	if (eOwner == getActivePlayer() &&
		//BUGOption::isEnabled("CityBar__HurryAnger", true))
		BUGOption::isEnabled("CityScreen__Anger_Counter", true))
	{
		int iAngerTimer = std::max(kCity.getHurryAngerTimer(), kCity.getConscriptAngerTimer());
		// As in CvMainInterface.updateCityScreen
		iAngerTimer = std::max(iAngerTimer, kCity.getDefyResolutionAngerTimer());
		if (iAngerTimer > 0)
		{
			// No happiness is displayed in disorder
			bool const bParentheses = !kCity.isDisorder();
			if (bParentheses)
				szString.append(L"(");
			else szString.append(L", ");
			// (BULL had largely duplicated the CvCity::get...PercentAnger functions)
			int iPercentAnger = std::max(kCity.getHurryPercentAnger(),
					kCity.getConscriptPercentAnger());
			iPercentAnger = std::max(iPercentAnger,
					kCity.getDefyResolutionPercentAnger());
			int iAngryPop = (iPercentAnger * kCity.getPopulation()) /
					GC.getPERCENT_ANGER_DIVISOR();
			szString.append(gDLL->getText("TXT_KEY_CITY_BAR_ANGER_TIMER",
					iAngryPop, iAngerTimer));
			if (bParentheses)
				szString.append(L")");
		}
	} // </advc.186>
	// <advc.101>
	if (!BUGOption::isEnabled("MainInterface__RevoltHelp", true))
	{
		CvWStringBuffer szRevoltHelp;
		setRevoltHelp(szRevoltHelp, kCity);
		if (!szRevoltHelp.isEmpty())
		{
			szString.append(NEWLINE);
			szString.append(szRevoltHelp.getCString());
		}
	} // </advc.101>
	{
		int const iFoodDifference = kCity.foodDifference();
		// advc.002f:
		bool const bAvoidGrowth = kCity.AI().AI_isEmphasizeAvoidGrowth();
		if (iFoodDifference == 0) // advc.004: was <=
		{
			szString.append(gDLL->getText("TXT_KEY_CITY_BAR_GROWTH",
					kCity.getFood(), kCity.growthThreshold()));
			szString.append(L" (");
			szString.append(gDLL->getText("INTERFACE_CITY_STAGNANT"));
			szString.append(L")");
		}
		else
		{
			szString.append(gDLL->getText(
					// advc.189: Not merging BULL Food Assist - this tweak should suffice
					iFoodDifference < 0 ? "TXT_KEY_CITY_BAR_STARVATION" :
					"TXT_KEY_CITY_BAR_FOOD_GROWTH",
					iFoodDifference < 0 ? -iFoodDifference : // advc.189
					iFoodDifference, kCity.getFood(), kCity.growthThreshold(),
					abs(kCity.getFoodTurnsLeft()))); // advc.189: abs
		}
		// <advc.002f>
		if (bAvoidGrowth)
		{
			szTempBuffer = gDLL->getText("TXT_KEY_CITY_BAR_AVOID_GROWTH");
			if (kCity.getFoodTurnsLeft() == 1)
			{
				szTempBuffer.Format(SETCOLR L"%s" ENDCOLR,
						TEXT_COLOR("COLOR_WARNING_TEXT"), szTempBuffer.c_str());
			}
			szString.append(L" - ");
			szString.append(szTempBuffer);
		} // </advc.002f>
	}
	{
		int iProductionDiffNoFood = kCity.getCurrentProductionDifference(true,
				false, true); // advc.186
		int iProductionDiffJustFood = (kCity.getCurrentProductionDifference(false,
				false, true) // advc.186
				- iProductionDiffNoFood);
		// <advc.186>
		int iStoredProduction = kCity.getCurrentProductionDifference(
				true, true, false, true, true); // </advc.186>
		if (iProductionDiffNoFood + iProductionDiffJustFood + iStoredProduction > 0)
			szString.append(NEWLINE);
		if (iProductionDiffJustFood > 0)
		{
			szString.append(gDLL->getText(
					"TXT_KEY_CITY_BAR_FOOD_PRODUCTION_PER_TURN",
					iProductionDiffJustFood, iProductionDiffNoFood));
		}
		else if (iProductionDiffNoFood > 0)
		{
			szString.append(gDLL->getText(
					"TXT_KEY_CITY_BAR_PRODUCTION_PER_TURN",
					iProductionDiffNoFood));
		}
		int const iProductionTurns = kCity.getProductionTurnsLeft();
		if (iStoredProduction > 0)
		{
			if (iProductionTurns != MAX_INT)
			{
				szString.append(gDLL->getText(
						"TXT_KEY_CITY_BAR_ONE_TIME_PRODUCTION",
						iStoredProduction));
			}
			else
			{
				if (iProductionDiffNoFood + iProductionDiffJustFood > 0)
					szString.append(L", ");
				szString.append(gDLL->getText(
						"TXT_KEY_CITY_BAR_STORED_PRODUCTION",
						iStoredProduction));
			}
		}
		if (kCity.getProductionNeeded() != MAX_INT)
		{
			// <advc.004x>
			szString.append(gDLL->getText(
					"TXT_KEY_CITY_BAR_PRODUCTION", // (NB: starts with a linebreak)
					kCity.getProductionName(), kCity.getProduction(),
					kCity.getProductionNeeded()));
			if (iProductionTurns != MAX_INT) // </advc.004x>
			{
				szString.append(gDLL->getText(
						"TXT_KEY_CITY_BAR_PRODUCTION_TURNS",
						iProductionTurns));
			}

		}
		// <advc.186>
		else if (!kCity.isDisorder())
		{
			CvWString szProcessCommerce;
			bool bFirst = true;
			FOR_EACH_ENUM(Commerce)
			{
				// Akin to code in SetCommerceHelp
				int iRate = kCity.getProductionToCommerceModifier(eLoopCommerce) *
						kCity.getYieldRate(YIELD_PRODUCTION);
				if (iRate == 0)
					continue;
				wchar cIcon = GC.getInfo(eLoopCommerce).getChar();
				setListHelp(szProcessCommerce, L"", iRate % 100 == 0 ?
						CvWString::format(L"%d%c", iRate / 100, cIcon) :
						CvWString::format(L"%.2f%c", iRate / 100.f, cIcon),
						L", ", bFirst);
			}
			if (!szProcessCommerce.empty())
			{
				szString.append(NEWLINE);
				szString.append(gDLL->getText(
						"TXT_KEY_CITY_BAR_PRODUCTION_PROCESS",
						szProcessCommerce.c_str()));
			}
		} // </advc.186>
	}
	// BULL - Hurry Assist - start (advc.186)
	if (eOwner == getActivePlayer() &&
		BUGOption::isEnabled("CityScreen__WhipAssist", true))
	{
		bool bFirstHurry = true;
		FOR_EACH_ENUM(Hurry)
		{
			if (!kCity.canHurry(eLoopHurry))
				continue;
			CvWString szHurryHelp;
			bool bFirstDetail = true;
			int iPopulation = kCity.hurryPopulation(eLoopHurry);
			if (iPopulation > 0)
			{
				szTempBuffer.Format(L"%d%c", -iPopulation,
						gDLL->getSymbolID(CITIZEN_CHAR));
				setListHelp(szHurryHelp, L"", szTempBuffer, L", ", bFirstDetail);
			}
			int iGold = kCity.hurryGold(eLoopHurry);
			if (iGold > 0)
			{
				szTempBuffer.Format(L"%d%c", -iGold,
						GC.getInfo(COMMERCE_GOLD).getChar());
				setListHelp(szHurryHelp, L"", szTempBuffer, L", ", bFirstDetail);
			}
			int iOverflowProduction = 0;
			int iOverflowGold = 0;
			if (kCity.hurryOverflow(eLoopHurry, &iOverflowProduction, &iOverflowGold,
				BUGOption::isEnabled("CityScreen__WhipAssistOverflowCountCurrentProduction", false)))
			{
				if (iOverflowProduction > 0)
				{
					szTempBuffer.Format(L"+%d%c", iOverflowProduction,
							GC.getInfo(YIELD_PRODUCTION).getChar());
					setListHelp(szHurryHelp, L"", szTempBuffer, L", ", bFirstDetail);
				}
				if (iOverflowGold > 0)
				{
					szTempBuffer.Format(L"+%d%c", iOverflowGold,
							GC.getInfo(COMMERCE_GOLD).getChar());
					setListHelp(szHurryHelp, L"", szTempBuffer, L", ", bFirstDetail);
				}
			}
			if (!bFirstDetail)
			{
				szString.append(NEWLINE);
				setListHelp(szString, gDLL->getText("TXT_KEY_CITY_BAR_HURRY_HEADING"),
						szHurryHelp, gDLL->getText("TXT_KEY_OR"), bFirstHurry);
			}
		}
	} // BULL - Hurry Assist - end
	// BULL - Commerce - start
	/*	advc.186: Show raw commerce in the trade-routes line; not enough room
		in the commerce line (due to advc.002b), and also a bit confusing there. */
	//if (BUGOption::isEnabled("CityBar__Commerce", true)) {
	// (It looks like raw commerce is not treated as being 0 during disorder.)
	int const iCommerceRate = (kCity.isDisorder() ? 0 :
			kCity.getYieldRate(YIELD_COMMERCE));
	if (iCommerceRate != 0)
	{
		szString.append(NEWLINE);
		szTempBuffer.Format(L"%d%c", iCommerceRate,
				GC.getInfo(YIELD_COMMERCE).getChar());
		szString.append(szTempBuffer);
		szString.append(gDLL->getText("TXT_KEY_PER_TURN"));
	} // BULL - Commerce - end
	// BULL - Trade Detail - start (advc.186; fractional TR code removed)
	//if (BUGOption::isEnabled("CityBar__TradeDetail", true))
	{
		int iDomesticTrade = 0;
		int iDomesticRoutes = 0;
		int iForeignTrade = 0;
		int iForeignRoutes = 0;
		kCity.calculateTradeTotals(YIELD_COMMERCE, iDomesticTrade, iDomesticRoutes,
				iForeignTrade, iForeignRoutes);
		int const iTotalTrade = iDomesticTrade + iForeignTrade;
		if (iTotalTrade > 0)
		{
			FAssert(iCommerceRate > 0);
			szString.append(L", ");
			szString.append(gDLL->getText("TXT_KEY_CITY_BAR_FROM_TR", iTotalTrade));
			szString.append(L" (");
			if (iTotalTrade == iDomesticTrade)
				szString.append(gDLL->getText("TXT_KEY_CITY_BAR_ALL_DOMESTIC"));
			else if (iTotalTrade == iForeignTrade)
				szString.append(gDLL->getText("TXT_KEY_CITY_BAR_ALL_FOREIGN"));
			else szString.append(gDLL->getText("TXT_KEY_CITY_BAR_FOREIGN_TR_COMMERCE", iForeignTrade));
			szString.append(L")");
		}
	} // BULL - Trade Detail - end
	{
		bool bFirst = true;
		FOR_EACH_ENUM(Commerce)
		{
			int iRate = kCity.getCommerceRateTimes100(eLoopCommerce);
			if (iRate != 0)
			{
				wchar const cIcon = GC.getInfo(eLoopCommerce).getChar();
				/*	<advc.002b> Can probably fit all rates in one line by omitting
					trailing zeros */
				if (iRate % 100 == 0)
					szTempBuffer.Format(L"%d%c", iRate / 100, cIcon);
				else if (iRate % 10 == 0)
					szTempBuffer.Format(L"%d.%d%c", iRate / 100, (iRate % 100) / 10, cIcon);
				// </advc.002b>
				else szTempBuffer.Format(L"%d.%02d%c", iRate / 100, iRate % 100, cIcon);
				setListHelp(szString, NEWLINE, szTempBuffer, L", ", bFirst);
			}
		}
		if (!bFirst)
			szString.append(gDLL->getText("TXT_KEY_PER_TURN"));
	}
	// advc.186: Culture moved up; and CULTURELEVEL_NONE has id NO_CULTURELEVEL+1
	if (kCity.getCultureLevel() > NO_CULTURELEVEL + 1)
	{
		szString.append(NEWLINE);
		// advc.186: Don't name the culture level
		/*szString.append(gDLL->getText("TXT_KEY_CITY_BAR_CULTURE",
				kCity.getCulture(eOwner), kCity.getCultureThreshold(),
				GC.getInfo(kCity.getCultureLevel()).getTextKeyWide()));*/
		// BULL - Culture Turns - start
		szString.append(gDLL->getText("TXT_KEY_CITY_BAR_CULTURE_NO_LEVEL",
				kCity.getCulture(eOwner), kCity.getCultureThreshold()));
		int iCultureRate = kCity.getCommerceRateTimes100(COMMERCE_CULTURE);
		if (iCultureRate > 0)
		{
			int iCulture = kCity.getCultureTimes100(eOwner);
			int iCultureLeft = 100 * kCity.getCultureThreshold() - iCulture;
			if (iCultureLeft > 0) // (Inspired by Dawn of Civilization mod)
			{
				szString.append(L" ");
				szString.append(gDLL->getText("INTERFACE_CITY_TURNS",
						intdiv::uceil(iCultureLeft, iCultureRate)));
			}
		} // BULL - Culture Turns - end
	}
	// <advc.186> Separate line for GP rate
	{
		bool bNewlineNeeded = true;
		int iRate = kCity.getGreatPeopleRate();
		if (iRate != 0)
		{
			szString.append(NEWLINE);
			bNewlineNeeded = false;
			szTempBuffer.Format(L"%d%c", iRate, gDLL->getSymbolID(GREAT_PEOPLE_CHAR));
			szString.append(szTempBuffer);
			szString.append(gDLL->getText("TXT_KEY_PER_TURN"));
		}
		// City specialist (based on BULL)
		//if (BUGOption::isEnabled("CityBar__Specialists", true))
		std::vector<SpecialistTypes> aeSpecialists;
		FOR_EACH_ENUM(Specialist)
		{
			for (int i = 0; i < kCity.getSpecialistCount(eLoopSpecialist); i++)
				aeSpecialists.push_back(eLoopSpecialist);
		}
		// Free specialists last
		FOR_EACH_ENUM(Specialist)
		{
			for (int i = 0; i < kCity.getFreeSpecialistCount(eLoopSpecialist); i++)
			{
				aeSpecialists.push_back(eLoopSpecialist);
			}
		}
		if (!aeSpecialists.empty())
		{
			if (bNewlineNeeded)
				szString.append(NEWLINE);
			//bNewlineNeeded = false;
			bool bFirst = true;
			for (size_t i = 0; i < aeSpecialists.size(); i++)
			{	// (was size 24 in BULL)
				szTempBuffer.Format(L"<img=%S size=20></img>",
						GC.getInfo(aeSpecialists[i]).getButton());
				setListHelp(szString, L" ", szTempBuffer, L"", bFirst);
			}
		}
	}
	// Hide when 0 rate and no substantial progress
	if (kCity.getGreatPeopleRate() > 0 ||
		kCity.getGreatPeopleProgress() * 25 >
		GET_PLAYER(eOwner).greatPeopleThreshold())
	{	// <BtS>
		szString.append(gDLL->getText("TXT_KEY_CITY_BAR_GREAT_PEOPLE",
				kCity.getGreatPeopleProgress(),
				GET_PLAYER(eOwner).greatPeopleThreshold(false))); // </BtS>
		// (based on BULL's "Great Person Turns")
		int iTurnsLeft = kCity.GPTurnsLeft();
		if (iTurnsLeft >= 0)
		{
			szString.append(L" ");
			szString.append(gDLL->getText("INTERFACE_CITY_TURNS", iTurnsLeft));
		}
	}
	if (!kCity.isDisorder())// </advc.186>
	{
		szString.append(NEWLINE);
		szString.append(gDLL->getText("INTERFACE_CITY_MAINTENANCE"));
		int iMaintenance = kCity.getMaintenanceTimes100() *
				// K-Mod:
				(100 + GET_PLAYER(kCity.getOwner()).calculateInflationRate()) / 100;
		szString.append(CvWString::format(L" -%d.%02d%c",
				iMaintenance / 100, iMaintenance % 100,
				GC.getInfo(COMMERCE_GOLD).getChar()));
	}
	// <advc.186>
	{
		enum BuildingDisplayMode { DISPLAY_NONE, DISPLAY_ICONS, DISPLAY_NAMES };
		BuildingDisplayMode const eMode = (BuildingDisplayMode)BUGOption::getValue(
				"CityBar__BuildingDisplay", DISPLAY_ICONS);
		std::vector<std::pair<CvWString,BuildingTypes> > aszeBuildingsByName;
		if (eMode != DISPLAY_NONE)
		{
			CvCivilization const& kCiv = GET_PLAYER(eOwner).getCivilization();
			for (int i = 0; i < kCiv.getNumBuildings(); i++)
			{
				BuildingTypes eBuilding = kCiv.buildingAt(i);
				/*	(NB: If this were changed to getNumBuilding, then
					TXT_KEY_BUG_OPT_CITYBAR__BUILDINGDISPLAY_HOVER also ought to
					changed; currently warns that free buildings are omitted.) */
				if (kCity.getNumRealBuilding(eBuilding) > 0)
				{
					aszeBuildingsByName.push_back(std::make_pair(
						GC.getInfo(eBuilding).getDescription(), eBuilding));
				}
			}
			std::sort(aszeBuildingsByName.begin(), aszeBuildingsByName.end());
		}
		bool bFirst = true;
		for (size_t i = 0; i < aszeBuildingsByName.size(); i++)
		{
			if (eMode == DISPLAY_NAMES)
			{	// <BtS>
				setListHelp(szString, NEWLINE, aszeBuildingsByName[i].first,
						L", ", bFirst); // </BtS>
			}
			else
			{
				FAssert(eMode == DISPLAY_ICONS);
				// BULL - Building Icons - start (advc: BULL had used size 24)
				szTempBuffer.Format(L"<img=%S size=32></img>",
						GC.getInfo(aszeBuildingsByName[i].second).getButton());
				setListHelp(szString, NEWLINE, szTempBuffer, L"", bFirst);
				// BULL - Building Icons - end
			}
		}
	} // </advc.186>
	{
		TeamTypes eActiveTeam = getActiveTeam();
		int iAirUnits = kCity.getPlot().countNumAirUnits(eActiveTeam);
		if (iAirUnits > 0 &&
			// advc.187: Now shown in plot help by default
			!BUGOption::isEnabled("MainInterface__AirCapacity", true))
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText("TXT_KEY_CITY_BAR_AIR_UNIT_CAPACITY",
					iAirUnits, kCity.getAirUnitCapacity(eActiveTeam)));
		}
	}
	/*	<advc.186> Even as a single line, the hint is distracting. An option
		only makes sense if it's enabled by default. */
	#if 0
	if (bPopup || !BUGOption::isEnabled("CityBar__SelectionHelp", false))
		return;
	//szString.append(NEWLINE);
	szString.append(gDLL->getText("TXT_KEY_CITY_BAR_SELECT", kCity.getNameKey()));
	// Takes up too much space
	/*szString.append(gDLL->getText("TXT_KEY_CITY_BAR_SELECT_CTRL"));
	szString.append(gDLL->getText("TXT_KEY_CITY_BAR_SELECT_ALT"));*/
	#endif
	// </advc.186>
}

/*  advc.101: Similar to code added in CvDLLWidgetData::parseNationalityHelp;
	replacing BULL's "Revolt Chance" code (which was never merged into K-Mod/AdvCiv). */
void CvGameTextMgr::setRevoltHelp(CvWStringBuffer &szString, CvCity const& kCity)
{
	if (!kCity.getPlot().isActiveVisible(true))
		return;
	bool const bActiveOwned = kCity.isActiveOwned();
	scaled rRevoltProb = kCity.revoltProbability();
	// <advc.023>
	scaled const rDecrementProb = kCity.probabilityOccupationDecrement();
	rRevoltProb *= 1 - rDecrementProb; // </advc.023>
	PlayerTypes const eCulturalOwner = (bActiveOwned ?
			kCity.calculateCulturalOwner() : NO_PLAYER);
	int const iGarrisonStr = (bActiveOwned ?
			kCity.cultureGarrison(eCulturalOwner) : -1);
	int const iCultureStr = (bActiveOwned ?
			kCity.cultureStrength(eCulturalOwner) : -1);
	int iExcessStrength = 0;
	CvUnit const* pSelectedUnit = gDLL->UI().getHeadSelectedUnit();
	if (rRevoltProb > 0)
	{
		/*  CvCity::revoltProbability rounds probabilities that are too small to
			display to 0, but that doesn't take into account prDecrement, so
			prRevolt here can still be less than 1 permille -- though not much
			less, so this isn't going to overstate the probability much: */
		float fRevoltProb = std::max(0.001f, rRevoltProb.getFloat());
		wchar floatBuffer[1024];
		swprintf(floatBuffer, L"%.1f", 100 * fRevoltProb);
		szString.append(gDLL->getText(
				"TXT_KEY_MISC_CHANCE_OF_REVOLT", floatBuffer));
		if (bActiveOwned)
		{
			FAssert(iCultureStr > iGarrisonStr);
			int iGarrisonStrNeeded = std::max(1, iCultureStr - iGarrisonStr);
			szString.append(L"  ");
			szString.append(gDLL->getText(
					"TXT_KEY_GARRISON_STRENGTH_NEEDED_SHORT",
					iGarrisonStrNeeded));
			iExcessStrength = -iGarrisonStrNeeded;
		}
		int const iPriorRevolts = kCity.getNumRevolts();
		if (kCity.canCultureFlip())
		{
			szString.append(bActiveOwned ? NEWLINE : L" ");
			szString.append(gDLL->getText(bActiveOwned ?
					"TXT_KEY_MISC_WILL_FLIP" : "TXT_KEY_MISC_WILL_FLIP_SHORT"));
		}
		else if (iPriorRevolts > 0)
		{
			szString.append(bActiveOwned ? NEWLINE : L" (");
			szString.append(gDLL->getText(
					"TXT_KEY_MISC_PRIOR", iPriorRevolts));
			if (!bActiveOwned)
				szString.append(L" )");
		}
	}  // <advc.023>
	if (rDecrementProb > 0)
	{
		if (!szString.isEmpty())
			szString.append(NEWLINE);
		wchar floatBuffer[1024];
		swprintf(floatBuffer, L"%.1f", 100 * rDecrementProb.getFloat());
		szString.append(gDLL->getText(
				"TXT_KEY_OCCUPATION_DECREASE_CHANCE", floatBuffer));
	} // </advc.023>
	else if (rRevoltProb <= 0 && bActiveOwned && iGarrisonStr > 0 &&
		eCulturalOwner != kCity.getOwner() && iGarrisonStr >= iCultureStr)
	{
		// Show it only when a local unit is selected? Eh ...
		//if (pSelectedUnit != NULL && pSelectedUnit->at(kPlot))
		{
			int iSafeToRemove = iGarrisonStr - iCultureStr;
			if (iSafeToRemove < iGarrisonStr)
			{
				if (!szString.isEmpty())
					szString.append(NEWLINE);
				szString.append(gDLL->getText(
						"TXT_KEY_GARRISON_STRENGTH_EXCESS_SHORT",
						std::min(999, iSafeToRemove)));
				iExcessStrength = iSafeToRemove;
			}
		}
	}
	if (iExcessStrength != 0 && pSelectedUnit != NULL)
	{
		int iSelected = 0;
		int iSelectedStrength = 0;
		FOR_EACH_UNIT_IN(pUnit, *gDLL->UI().getSelectionList())
		{
			int iStr = pUnit->garrisonStrength();
			if (iStr != 0)
			{
				iSelectedStrength += iStr;
				iSelected++;
			}
		}
		if (iSelectedStrength != 0 && (iExcessStrength < 0 ||
			pSelectedUnit->at(kCity.getPlot()))/* && iSelected > 1*/)
		{
			szString.append(NEWLINE);
			szString.append(gDLL->getText(
					"TXT_KEY_GARRISON_STRENGTH_SELECTED",
					intdiv::uround(iSelectedStrength, 100)));
		}
	}
}


void CvGameTextMgr::parseTraits(CvWStringBuffer &szHelpString, TraitTypes eTrait,
	CivilizationTypes eCivilization, bool bDawnOfMan)
{
	PROFILE_FUNC();

	CvTraitInfo const& kTrait = GC.getInfo(eTrait);

	CvWString szText = kTrait.getDescription();
	{
		CvWString szTempBuffer;
		if (bDawnOfMan)
			szTempBuffer.Format(L"%s", szText.GetCString());
		else
		{
			szTempBuffer.Format(NEWLINE SETCOLR L"%s" ENDCOLR,
					TEXT_COLOR("COLOR_ALT_HIGHLIGHT_TEXT"), szText.GetCString());
		}
		szHelpString.append(szTempBuffer);
	}
	if (bDawnOfMan)
		return;

	//if (!CvWString(kTrait.getHelp()).empty()) // advc: unnecessary
	szHelpString.append(kTrait.getHelp());

	if (kTrait.getHealth() != 0)
		szHelpString.append(gDLL->getText("TXT_KEY_TRAIT_HEALTH", kTrait.getHealth()));

	if (kTrait.getHappiness() != 0)
		szHelpString.append(gDLL->getText("TXT_KEY_TRAIT_HAPPINESS", kTrait.getHappiness()));

	if (kTrait.getMaxAnarchy() != -1)
	{
		if (kTrait.getMaxAnarchy() == 0)
			szHelpString.append(gDLL->getText("TXT_KEY_TRAIT_NO_ANARCHY"));
		else
		{
			szHelpString.append(gDLL->getText("TXT_KEY_TRAIT_MAX_ANARCHY",
					kTrait.getMaxAnarchy()));
		}
	}
	if (kTrait.getUpkeepModifier() != 0)
	{
		szHelpString.append(gDLL->getText("TXT_KEY_TRAIT_CIVIC_UPKEEP_MODIFIER",
				kTrait.getUpkeepModifier()));
	}
	if (kTrait.getLevelExperienceModifier() != 0)
	{
		szHelpString.append(gDLL->getText("TXT_KEY_TRAIT_CIVIC_LEVEL_MODIFIER",
				kTrait.getLevelExperienceModifier()));
	}
	if (kTrait.getGreatPeopleRateModifier() != 0)
	{
		szHelpString.append(gDLL->getText("TXT_KEY_TRAIT_GREAT_PEOPLE_MODIFIER",
				kTrait.getGreatPeopleRateModifier()));
	}
	if (kTrait.getGreatGeneralRateModifier() != 0)
	{
		szHelpString.append(gDLL->getText("TXT_KEY_TRAIT_GREAT_GENERAL_MODIFIER",
				kTrait.getGreatGeneralRateModifier()));
	}
	if (kTrait.getDomesticGreatGeneralRateModifier() != 0)
	{
		szHelpString.append(gDLL->getText("TXT_KEY_TRAIT_DOMESTIC_GREAT_GENERAL_MODIFIER",
				kTrait.getDomesticGreatGeneralRateModifier()));
	}
	// Wonder Production Effects
	if (kTrait.getMaxGlobalBuildingProductionModifier() != 0 ||
		kTrait.getMaxTeamBuildingProductionModifier() != 0 ||
		kTrait.getMaxPlayerBuildingProductionModifier() != 0)
	{
		if (kTrait.getMaxGlobalBuildingProductionModifier() ==
			kTrait.getMaxTeamBuildingProductionModifier() &&
			kTrait.getMaxGlobalBuildingProductionModifier() ==
			kTrait.getMaxPlayerBuildingProductionModifier())
		{
			szHelpString.append(gDLL->getText("TXT_KEY_TRAIT_WONDER_PRODUCTION_MODIFIER",
					kTrait.getMaxGlobalBuildingProductionModifier()));
		}
		else
		{
			if (kTrait.getMaxGlobalBuildingProductionModifier() != 0)
			{
				szHelpString.append(
						gDLL->getText("TXT_KEY_TRAIT_WORLD_WONDER_PRODUCTION_MODIFIER",
						kTrait.getMaxGlobalBuildingProductionModifier()));
			}
			if (kTrait.getMaxTeamBuildingProductionModifier() != 0)
			{
				szHelpString.append(
						gDLL->getText("TXT_KEY_TRAIT_TEAM_WONDER_PRODUCTION_MODIFIER",
						kTrait.getMaxTeamBuildingProductionModifier()));
			}
			if (kTrait.getMaxPlayerBuildingProductionModifier() != 0)
			{
				szHelpString.append(
						gDLL->getText("TXT_KEY_TRAIT_NATIONAL_WONDER_PRODUCTION_MODIFIER",
						kTrait.getMaxPlayerBuildingProductionModifier()));
			}
		}
	}
	FOR_EACH_ENUM2(Yield, eYield)
	{
		wchar const iYieldChar = GC.getInfo(eYield).getChar();
		{
			int const iThresh = kTrait.getExtraYieldThreshold(eYield);
			if (iThresh != 0)
			{
				szHelpString.append(gDLL->getText(
						"TXT_KEY_TRAIT_EXTRA_YIELD_THRESHOLDS",
						iYieldChar, iThresh, iYieldChar));
			}
		}
		// <advc.908a>
		{

			int const iThresh = kTrait.getExtraYieldNaturalThreshold(eYield);
			if (iThresh != 0)
			{
				szHelpString.append(gDLL->getText(
						"TXT_KEY_TRAIT_EXTRA_YIELD_NATURAL_THRESHOLDS",
						iYieldChar, iThresh - 1, iYieldChar, iThresh, iYieldChar));
			}
		} // </advc.908a>
		{
			int const iModifier = kTrait.getTradeYieldModifier(eYield);
			if (iModifier != 0)
			{
				szHelpString.append(gDLL->getText(
						"TXT_KEY_TRAIT_TRADE_YIELD_MODIFIERS",
						iModifier, iYieldChar/*, "YIELD"*/)); // advc: wth?
			}
		}
	}
	FOR_EACH_ENUM2(Commerce, eCommerce)
	{
		if (kTrait.getCommerceChange(eCommerce) != 0)
		{
			szHelpString.append(gDLL->getText("TXT_KEY_TRAIT_COMMERCE_CHANGES",
					kTrait.getCommerceChange(eCommerce),
					GC.getInfo(eCommerce).getChar()/*, "COMMERCE"*/)); // advc
		}
		if (kTrait.getCommerceModifier(eCommerce) != 0)
		{
			szHelpString.append(gDLL->getText("TXT_KEY_TRAIT_COMMERCE_MODIFIERS",
					kTrait.getCommerceModifier(eCommerce),
					GC.getInfo(eCommerce).getChar()/*, "COMMERCE"*/)); // advc
		}
	}
	// <advc.908b>
	{
		CvGame const& kGame = GC.getGame();
		bool const bInGame = (getActivePlayer() != NO_PLAYER &&
				// Important for Play Now screens
				kGame.getHandicapType() != NO_HANDICAP);
		int const iFreeCityCulture = (bInGame ?
				kGame.freeCityCultureFromTrait(eTrait) :
				kTrait.get(CvTraitInfo::FREE_CITY_CULTURE));
		if (iFreeCityCulture != 0)
		{
			CultureLevelTypes eFreeLevel = NO_CULTURELEVEL;
			FOR_EACH_ENUM_REV(CultureLevel)
			{
				if (eLoopCultureLevel <= 1)
					break;
				int iThresh = (bInGame ? kGame.getCultureThreshold(eLoopCultureLevel) :
						// (Game speed is treated as default before game launch)
						GC.getInfo(eLoopCultureLevel).getSpeedThreshold(kGame.getGameSpeedType()));
				if (iFreeCityCulture < iThresh)
					continue;
				/*	This only works because (and so long as) the thresholds set in
					CultureLevel XML correspond to CvGame::freeCityCultureFromTrait.
					(Clean solution would be a separate XML tag for free culture level.) */
				if (iFreeCityCulture == iThresh)
					eFreeLevel = eLoopCultureLevel;
				break;
			}
			if (eFreeLevel != NO_CULTURELEVEL)
			{
				szHelpString.append(
						gDLL->getText("TXT_KEY_TRAIT_FREE_CULTURE_LEVEL",
						GC.getInfo(eFreeLevel).getDescription()));
			}
			else
			{
				szHelpString.append(
						gDLL->getText("TXT_KEY_TRAIT_FREE_CITY_CULTURE",
						iFreeCityCulture));
			}
		}
	} // </advc.908b>
	{
		CvWString szTempBuffer;
		bool bFoundPromotion = false;
		FOR_EACH_ENUM(Promotion)
		{
			if (kTrait.isFreePromotion(eLoopPromotion))
			{
				if (bFoundPromotion)
					szTempBuffer += L", ";
				szTempBuffer += CvWString::format(L"<link=literal>%s</link>",
						GC.getInfo(eLoopPromotion).getDescription());
				bFoundPromotion = true;
			}
		}
		if (bFoundPromotion)
		{
			szHelpString.append(gDLL->getText("TXT_KEY_TRAIT_FREE_PROMOTIONS",
					szTempBuffer.GetCString()));

			FOR_EACH_ENUM(UnitCombat)
			{
				if (kTrait.isFreePromotionUnitCombat(eLoopUnitCombat))
				{
					szTempBuffer.Format(L"\n        %c<link=literal>%s</link>",
							gDLL->getSymbolID(BULLET_CHAR),
							GC.getInfo(eLoopUnitCombat).getDescription());
					szHelpString.append(szTempBuffer);
				}
			}
		}
	}
	FOR_EACH_ENUM(CivicOption)
	{
		if (GC.getInfo(eLoopCivicOption).getTraitNoUpkeep(eTrait))
		{
			szHelpString.append(gDLL->getText("TXT_KEY_TRAIT_NO_UPKEEP",
					GC.getInfo(eLoopCivicOption).getTextKeyWide()));
		}
	}
	// Increase Building/Unit Production Speeds
	{
		int iLast = 0;
		FOR_EACH_ENUM(SpecialUnit)
		{
			int const iProductionModifier = GC.getInfo(eLoopSpecialUnit).
					getProductionTraits(eTrait);
			if (iProductionModifier == 0)
				continue;
			if (iProductionModifier == 100)
				szText = gDLL->getText("TXT_KEY_TRAIT_DOUBLE_SPEED");
			else
			{
				szText = gDLL->getText("TXT_KEY_TRAIT_PRODUCTION_MODIFIER",
						iProductionModifier);
			}
			setListHelp(szHelpString, szText.GetCString(),
					GC.getInfo(eLoopSpecialUnit).getDescription(), L", ",
					iLast, iProductionModifier);
		}
	}
	{
		int iLast = 0;
		FOR_EACH_ENUM(UnitClass)
		{
			UnitTypes const eLoopUnit = (eCivilization == NO_CIVILIZATION ?
					GC.getInfo(eLoopUnitClass).getDefaultUnit() :
					GC.getInfo(eCivilization).getCivilizationUnits(eLoopUnitClass));
			if (eLoopUnit == NO_UNIT || GC.getInfo(eLoopUnitClass).isWorldUnit())
				continue;
			int const iProductionModifier = GC.getInfo(eLoopUnit).
					getProductionTraits(eTrait);
			if (iProductionModifier == 0)
				continue;
			CvUnitInfo const& kLoopUnit = GC.getInfo(eLoopUnit);
			if (iProductionModifier == 100)
					szText = gDLL->getText("TXT_KEY_TRAIT_DOUBLE_SPEED");
			else
			{
				szText = gDLL->getText("TXT_KEY_TRAIT_PRODUCTION_MODIFIER",
						iProductionModifier);
			}
			CvWString szUnit;
			szUnit.Format(L"<link=literal>%s</link>", kLoopUnit.getDescription());
			setListHelp(szHelpString, szText.GetCString(),
					szUnit, L", ",
					iLast, iProductionModifier);
		}
	}
	{
		int iLast = 0;
		FOR_EACH_ENUM(SpecialBuilding)
		{
			int const iProductionModifier = GC.getInfo(eLoopSpecialBuilding).
					getProductionTraits(eTrait);
			if (iProductionModifier == 0)
				continue;
			if (iProductionModifier == 100)
				szText = gDLL->getText("TXT_KEY_TRAIT_DOUBLE_SPEED");
			else
			{
				szText = gDLL->getText("TXT_KEY_TRAIT_PRODUCTION_MODIFIER",
						iProductionModifier);
			}
			setListHelp(szHelpString, szText.GetCString(),
					GC.getInfo(eLoopSpecialBuilding).getDescription(), L", ",
					iLast, iProductionModifier);
		}
	}
	std::vector<CvBuildingInfo const*> apBuildings; // advc
	FOR_EACH_ENUM(BuildingClass)
	{
		BuildingTypes const eLoopBuilding = (eCivilization == NO_CIVILIZATION ?
				GC.getInfo(eLoopBuildingClass).getDefaultBuilding() :
				GC.getInfo(eCivilization).getCivilizationBuildings(eLoopBuildingClass));
		if (eLoopBuilding != NO_BUILDING &&
			!GC.getInfo(eLoopBuildingClass).isWorldWonder())
		{	// <advc>
			apBuildings.push_back(&GC.getInfo(eLoopBuilding));
		}
	}
	{
		int iLast = 0;
		for (size_t i = 0; i < apBuildings.size(); i++)
		{
			CvBuildingInfo const& kBuilding = *apBuildings[i]; // </advc>
			int const iProductionModifier = kBuilding.getProductionTraits(eTrait);
			if (iProductionModifier == 0)
				continue;
			if (kBuilding.getProductionTraits(eTrait) == 100)
				szText = gDLL->getText("TXT_KEY_TRAIT_DOUBLE_SPEED");
			else
			{
				szText = gDLL->getText("TXT_KEY_TRAIT_PRODUCTION_MODIFIER",
						iProductionModifier);
			}
			CvWString szBuilding;
			szBuilding.Format(L"<link=literal>%s</link>",
						kBuilding.getDescription());
			setListHelp(szHelpString, szText.GetCString(),
					szBuilding, L", ",
					iLast, iProductionModifier);
		}
	}
	{
		int iLast = 0;
		for (size_t i = 0; i < apBuildings.size(); i++)
		{
			CvBuildingInfo const& kBuilding = *apBuildings[i]; // </advc>
			int iHappiness = kBuilding.getHappinessTraits(eTrait);
			if (iHappiness == 0)
				continue;
			if (iHappiness > 0)
			{
				szText = gDLL->getText("TXT_KEY_TRAIT_BUILDING_HAPPINESS",
						iHappiness, gDLL->getSymbolID(HAPPY_CHAR));
			}
			else
			{
				szText = gDLL->getText("TXT_KEY_TRAIT_BUILDING_HAPPINESS",
						-iHappiness, gDLL->getSymbolID(UNHAPPY_CHAR));
			}
			CvWString szBuilding;
			szBuilding.Format(L"<link=literal>%s</link>", kBuilding.getDescription());
			setListHelp(szHelpString, szText.GetCString(),
					szBuilding, L", ",
					iLast, iHappiness);
		}
	}
}

// parseLeaderTraits - SimpleCivPicker
void CvGameTextMgr::parseLeaderTraits(CvWStringBuffer &szHelpString, LeaderHeadTypes eLeader,
	CivilizationTypes eCivilization, bool bDawnOfMan, bool bCivilopediaText)
{
	PROFILE_FUNC();

	if (eLeader != NO_LEADER)
	{
		if (!bDawnOfMan && !bCivilopediaText)
		{
			CvWString szTempBuffer;
			szTempBuffer.Format( SETCOLR L"%s" ENDCOLR, TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
					GC.getInfo(eLeader).getDescription());
			szHelpString.append(szTempBuffer);
		}
		bool bFirst = true;
		FOR_EACH_ENUM(Trait)
		{
			if (!GC.getInfo(eLeader).hasTrait(eLoopTrait))
				continue;
			if (!bFirst)
			{
				if (bDawnOfMan)
					szHelpString.append(L", ");
			}
			else bFirst = false;
			parseTraits(szHelpString, eLoopTrait, eCivilization, bDawnOfMan);
		}
	}
	else
	{	//	Random leader
		CvWString szTempBuffer;
		szTempBuffer.Format( SETCOLR L"%s" ENDCOLR, TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
				gDLL->getText("TXT_KEY_TRAIT_PLAYER_UNKNOWN").c_str());
		szHelpString.append(szTempBuffer);
	}
}

// parseLeaderTraits - SimpleCivPicker
void CvGameTextMgr::parseLeaderShortTraits(CvWStringBuffer &szHelpString,
	LeaderHeadTypes eLeader)
{
	PROFILE_FUNC();

	if (eLeader != NO_LEADER)
	{
		bool bFirst = true;
		FOR_EACH_ENUM(Trait)
		{
			if (!GC.getInfo(eLeader).hasTrait(eLoopTrait))
				continue;
			if (!bFirst)
				szHelpString.append(L"/");
			szHelpString.append(gDLL->getText(GC.getInfo(eLoopTrait).
					getShortDescription()));
			bFirst = false;
		}
	}
	else
	{	//	Random leader
		szHelpString.append(CvWString("???/???"));
	}
}

// Build Civilization Info Help Text
void CvGameTextMgr::parseCivInfos(CvWStringBuffer &szInfoText, CivilizationTypes eCivilization,
	bool bDawnOfMan, bool bLinks)
{
	PROFILE_FUNC();

	if (eCivilization == NO_CIVILIZATION)
	{
		// This is a random civ, let us know here...
		szInfoText.append(gDLL->getText("TXT_KEY_CIV_UNKNOWN"));
		return; // advc
	}
	CvWString szBuffer;
	if (!bDawnOfMan)
	{
		// Civ Name
		CvWstring szCivName = GC.getInfo(eCivilization).getDescription();

		// doc: sorting hack: restore original names
		if (szCivName.size() == 2)
		{
			FOR_EACH_ENUM(Civilization)
			{
				GC.getInfo(eCivilization).setDescription(GC.getInfo(eCivilization).getDescriptionKeyPersistent());
			}

			szCivName = GC.getInfo(eCivilization).getDescription();
		}

		szBuffer.Format(SETCOLR L"%s" ENDCOLR, TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
				szCivName);
		szInfoText.append(szBuffer);

		// Free Techs
		// rfc: disabled
		/*szBuffer.Format(NEWLINE SETCOLR L"%s" ENDCOLR,
				TEXT_COLOR("COLOR_ALT_HIGHLIGHT_TEXT"),
				gDLL->getText("TXT_KEY_FREE_TECHS").GetCString());
		szInfoText.append(szBuffer);

		bool bFound = false;
		FOR_EACH_ENUM(Tech)
		{
			if (GC.getInfo(eCivilization).isCivilizationFreeTechs(eLoopTech))
			{
				bFound = true;
				CvWString szText;
				szText.Format(bLinks ? L"<link=literal>%s</link>" : L"%s",
						GC.getInfo(eLoopTech).getDescription());
				szBuffer.Format(L"%s  %c%s", NEWLINE, gDLL->getSymbolID(BULLET_CHAR),
						szText.GetCString());
				szInfoText.append(szBuffer);
			}
		}
		if (!bFound)
		{
			szBuffer.Format(L"%s  %s", NEWLINE,
					gDLL->getText("TXT_KEY_FREE_TECHS_NO").GetCString());
			szInfoText.append(szBuffer);
		}*/
	}

	// rfc: starting year
	szText = gDLL->getText("TXT_KEY_STARTING_YEAR");
	if (bDawnOfMan)
	{
		swprintf(szBuffer, SETCOLR L"%s: " ENDCOLR, TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"), szText.GetCString());
	}
	else
	{
		swprintf(szBuffer, NEWLINE SETCOLR L"%s" ENDCOLR , TEXT_COLOR("COLOR_ALT_HIGHLIGHT_TEXT"), szText.GetCString());
	}
	szInfoText.append(szBuffer);

	int iStartingYear = GC.getCivilizationInfo(eCivilization).getStartingYear();
	if (bDawnOfMan && !GC.getGameINLINE().isFinalInitialized())
	{
		iStartingYear = std::max(iStartingYear, getScenarioStartYear());
	}

	szText = gDLL->getText(iStartingYear >= 0 ? "TXT_KEY_YEAR_AD" : "TXT_KEY_YEAR_BC", std::abs(iStartingYear));

	szText += NEWLINE;
	if (bDawnOfMan)
	{
		swprintf(szBuffer, L"%s", szText.GetCString());
		szInfoText.append(szBuffer);
	}
	else
	{
		swprintf(szBuffer, L"%s  %c%s", NEWLINE, gDLL->getSymbolID(BULLET_CHAR), szText.GetCString());
		szInfoText.append(szBuffer);
	}

	if (bDawnOfMan)
	{
		swprintf(szBuffer, L"%s", gDLL->getText("TXT_KEY_LOADING_TIME_MINUTES", GC.getCivilizationInfo(eCivilization).getLoadingTime(getScenario())).GetCString());
		szInfoText.append(szBuffer);
	}

	// Free Units
	CvWString szText = gDLL->getText("TXT_KEY_FREE_UNITS");
	if (bDawnOfMan)
		szBuffer.Format(L"%s: ", szText.GetCString());
	else
	{
		szBuffer.Format(NEWLINE SETCOLR L"%s" ENDCOLR,
				TEXT_COLOR("COLOR_ALT_HIGHLIGHT_TEXT"), szText.GetCString());
	}
	szInfoText.append(szBuffer);

	// Unique Units
	bool bFound = false;
	FOR_EACH_ENUM(UnitClass)
	{	/*	advc: These were switched, but perhaps on purpose.
			So I switch them again when they're used. */
		UnitTypes eUniqueUnit = GC.getInfo(eCivilization).
				getCivilizationUnits(eLoopUnitClass);
		UnitTypes eDefaultUnit = GC.getInfo(eLoopUnitClass).getDefaultUnit();
		if (/*eeDefaultUnit != NO_UNIT &&*/ // advc.004: Include UU w/o a default unit
			eUniqueUnit != NO_UNIT && eDefaultUnit != eUniqueUnit &&
			!GC.getInfo(eUniqueUnit).isGraphicalOnly()) // doc (edead): skip graphical only units
		{	// advc: Moved into new function
			appendUniqueDesc(szInfoText, bFound, bDawnOfMan, bLinks,
					GC.getInfo(eUniqueUnit).getDescription(),
					// advc.004:
					eDefaultUnit == NO_UNIT ? NULL : GC.getInfo(eDefaultUnit).getDescription());
			bFound = true;
		}
	}
	if (!bFound)
	{
		szText = gDLL->getText("TXT_KEY_FREE_UNITS_NO");
		if (bDawnOfMan)
			szBuffer.Format(L"%s", szText.GetCString());
		else szBuffer.Format(L"%s  %s", NEWLINE, szText.GetCString());
		szInfoText.append(szBuffer);
		bFound = true;
	}

	// Free Buildings
	szText = gDLL->getText("TXT_KEY_UNIQUE_BUILDINGS");
	if (bDawnOfMan)
	{
		if (bFound)
			szInfoText.append(NEWLINE);
		szBuffer.Format(L"%s: ", szText.GetCString());
	}
	else
	{
		szBuffer.Format(NEWLINE SETCOLR L"%s" ENDCOLR ,
				TEXT_COLOR("COLOR_ALT_HIGHLIGHT_TEXT"), szText.GetCString());
	}
	szInfoText.append(szBuffer);

	// Unique Buildings
	bFound = false;
	FOR_EACH_ENUM(BuildingClass)
	{	// advc: These two variables were switched
		BuildingTypes eUniqueBuilding = GC.getInfo(eCivilization).
				getCivilizationBuildings(eLoopBuildingClass);
		BuildingTypes eDefaultBuilding = GC.getInfo(eLoopBuildingClass).
				getDefaultBuilding();
		if (/*eDefaultBuilding != NO_BUILDING &&*/ // advc.004: Include UB w/o a default building
			eUniqueBuilding != NO_BUILDING && eDefaultBuilding != eUniqueBuilding &&
			!GC.getInfo(eUniqueBuilding).isGraphicalOnly()) // doc
		{	// advc: Moved into new function
			appendUniqueDesc(szInfoText, bFound, bDawnOfMan, bLinks,
					GC.getInfo(eUniqueBuilding).getDescription(),
					// <advc.004>
					eDefaultBuilding == NO_BUILDING ? NULL :
					GC.getInfo(eDefaultBuilding).getDescription()); // </advc.004>
			bFound = true;
		}
	}
	if (!bFound)
	{
		szText = gDLL->getText("TXT_KEY_UNIQUE_BUILDINGS_NO");
		if (bDawnOfMan)
			szBuffer.Format(L"%s", szText.GetCString());
		else szBuffer.Format(L"%s  %s", NEWLINE, szText.GetCString());
		szInfoText.append(szBuffer);
	}

	// rfc: Unique powers
	if (bDawnOfMan)
	{
		szText = NEWLINE + gDLL->getText("TXT_KEY_UNIQUE_POWER");
		swprintf(szTempString, SETCOLR L"%s: " ENDCOLR, TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"), szText.GetCString());
	}
	else
	{
		szText = gDLL->getText("TXT_KEY_UNIQUE_POWER");
		swprintf(szTempString, NEWLINE SETCOLR L"%s" ENDCOLR NEWLINE, TEXT_COLOR("COLOR_ALT_HIGHLIGHT_TEXT"), szText.GetCString());
	}
	szInfoText.append(szTempString);

	swprintf(szTempString, L"%s" NEWLINE, gDLL->getText("TXT_KEY_UP_" + GC.getCivilizationInfo(eCivilization).getIdentifier() + "_TITLE").GetCString());
	szInfoText.append(szTempString);

	swprintf(szTempString, L"%s" NEWLINE, gDLL->getText("TXT_KEY_UP_" + GC.getCivilizationInfo(eCivilization).getIdentifier()).GetCString());
	szInfoText.append(szTempString);

	// rfc: Historical Victory goals
	if (bDawnOfMan)
	{
		szText = NEWLINE + gDLL->getText("TXT_KEY_UHV_GOALS");
		swprintf(szTempString, SETCOLR L"%s:" NEWLINE ENDCOLR, TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"), szText.GetCString());
	}
	else
	{
		szText = gDLL->getText("TXT_KEY_UHV_GOALS");
		swprintf(szTempString, NEWLINE SETCOLR L"%s" ENDCOLR , TEXT_COLOR("COLOR_ALT_HIGHLIGHT_TEXT"), szText.GetCString());
	}
	szInfoText.append(szTempString);

	CvWString historicalVictoryDescriptions;
	CyArgsList historicalVictoryDescriptionsArgs;

	historicalVictoryDescriptionsArgs.add(eCivilization);

	gDLL->getPythonIFace()->callFunction(PYScreensModule, "getHistoricalVictoryDescriptions", historicalVictoryDescriptionsArgs.makeFunctionArgs(), &historicalVictoryDescriptions);

	if (!bDawnOfMan)
	{
		szInfoText.append(NEWLINE);
	}

	szInfoText.append(historicalVictoryDescriptions.GetCString());

	if (bDawnOfMan)
	{
		szInfoText.append(NEWLINE);

		// doc: Significance
		szText = NEWLINE + gDLL->getText("TXT_KEY_INTERFACE_SIGNIFICANCE");
		swprintf(szTempString, SETCOLR L"%s: " ENDCOLR, TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"), szText.GetCString());
		szInfoText.append(szTempString);

		if (GC.getCivilizationInfo(eCivilization).getImpact() == 0)
		{
			swprintf(szTempString, L"%c" NEWLINE, gDLL->getSymbolID(SILVER_STAR_CHAR));
			szInfoText.append(szTempString);
		}
		else
		{
			for (int iI = 0; iI < GC.getCivilizationInfo(eCivilization).getImpact(); iI++)
			{
				swprintf(szTempString, L"%c", gDLL->getSymbolID(STAR_CHAR));
				szInfoText.append(szTempString);
			}
			szInfoText.append(NEWLINE);
		}

		// doc: Strengths
		szText = gDLL->getText("TXT_KEY_INTERFACE_STRENGTHS");
		swprintf(szTempString, SETCOLR L"%s: " ENDCOLR, TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"), szText.GetCString());
		szInfoText.append(szTempString);

		swprintf(szTempString, L"%s" NEWLINE, gDLL->getText("TXT_KEY_STRENGTHS_" + GC.getCivilizationInfo(eCivilization).getIdentifier()).GetCString());
		szInfoText.append(szTempString);

		szText = gDLL->getText("TXT_KEY_INTERFACE_CHALLENGES");
		swprintf(szTempString, SETCOLR L"%s: " ENDCOLR, TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"), szText.GetCString());
		szInfoText.append(szTempString);

		swprintf(szTempString, L"%s", gDLL->getText("TXT_KEY_CHALLENGES_" + GC.getCivilizationInfo(eCivilization).getIdentifier()).GetCString());
		szInfoText.append(szTempString);
	}
}

// advc: Cut from parseCivInfos
void CvGameTextMgr::appendUniqueDesc(CvWStringBuffer& szBuffer, bool bSeparator, bool bDawnOfMan,
	bool bLinks, wchar const* szUniqueDesc, wchar const* szDefaultDesc)
{
	CvWString szTmp;
	if (bDawnOfMan)
	{
		if (bSeparator)
			szBuffer.append(L", ");
		szTmp.Format(!bLinks ? L"%s": L"<link=literal>%s</link>", szUniqueDesc);
		szBuffer.append(szTmp);
		if (szDefaultDesc != NULL)
		{
			szTmp.Format(!bLinks ? L" - (%s)" : L" - (<link=literal>%s</link>)",
					szDefaultDesc);
			szBuffer.append(szTmp);
		}
	}
	else
	{
		szTmp.Format(L"\n  %c%s", gDLL->getSymbolID(BULLET_CHAR), szUniqueDesc);
		szBuffer.append(szTmp);
		if (szDefaultDesc != NULL)
		{
			szTmp.Format(L" - (%s)", szDefaultDesc);
			szBuffer.append(szTmp);
		}
	}
}


void CvGameTextMgr::parseSpecialistHelp(CvWStringBuffer &szHelpString,
	SpecialistTypes eSpecialist, CvCity* pCity, bool bCivilopediaText)
{
	PROFILE_FUNC();

	CvSpecialistInfo const& kSpecialist = GC.getInfo(eSpecialist); // K-Mod

	if (eSpecialist != NO_SPECIALIST)
	{
		if (!bCivilopediaText)
		{
			szHelpString.append(kSpecialist.getDescription());
		}
		{
			int aiYields[NUM_YIELD_TYPES];
			FOR_EACH_ENUM(Yield)
			{
				if (getActivePlayer() == NO_PLAYER)
					aiYields[eLoopYield] = kSpecialist.getYieldChange(eLoopYield);
				else
				{
					aiYields[eLoopYield] =
							GET_PLAYER(pCity != NULL ? pCity->getOwner() :
							getActivePlayer()).
							specialistYield(eSpecialist, eLoopYield);
				}
			}
			setYieldChangeHelp(szHelpString, L"", L"", L"", aiYields);
		}
		{
			int aiCommerces[NUM_COMMERCE_TYPES];
			FOR_EACH_ENUM(Commerce)
			{
				if (getActivePlayer() == NO_PLAYER)
				{
					aiCommerces[eLoopCommerce] = kSpecialist.getCommerceChange(
							eLoopCommerce);
				}
				else
				{
					aiCommerces[eLoopCommerce] = GET_PLAYER(
							pCity != NULL ? pCity->getOwner() :
							getActivePlayer()).
							specialistCommerce(eSpecialist, eLoopCommerce);
				}
			}
			setCommerceChangeHelp(szHelpString, L"", L"", L"", aiCommerces);
		}

		// doc: specialist happiness
		int iHappinessChange = GC.getSpecialistInfo(eSpecialist).getHappiness();
		if (iHappinessChange != 0)
		{
			if (iHappinessChange > 0)
			{
				szHelpString.append(gDLL->getText("TXT_KEY_SPECIALIST_GOOD_HAPPINESS", iHappinessChange));
			}
			else
			{
				szHelpString.append(gDLL->getText("TXT_KEY_SPECIALIST_BAD_HAPPINESS", -iHappinessChange));
			}
		}

		if (kSpecialist.getExperience() > 0)
		{
			szHelpString.append(NEWLINE);
			szHelpString.append(gDLL->getText("TXT_KEY_SPECIALIST_EXPERIENCE",
					kSpecialist.getExperience()));
		}

		if (kSpecialist.getGreatPeopleRateChange() != 0)
		{
			szHelpString.append(NEWLINE);
			szHelpString.append(gDLL->getText("TXT_KEY_SPECIALIST_BIRTH_RATE",
					kSpecialist.getGreatPeopleRateChange()));

			// K-Mod
			if (!bCivilopediaText && //gDLL->getChtLvl() > 0
				GC.getGame().isDebugMode() && // advc.135c
				GC.ctrlKey())
			{
				szHelpString.append(NEWLINE);
				szHelpString.append(CvWString::format(L"weight: %d", GET_PLAYER(
						pCity != NULL ? pCity->getOwner() :
						getActivePlayer()).
						AI_getGreatPersonWeight((UnitClassTypes)
						kSpecialist.getGreatPeopleUnitClass())));
			}
			// K-Mod end
		}

		// BUG - Specialist Actual Effects - start
		if (pCity != NULL &&
			(GC.altKey() ||
			BUGOption::isEnabled("MiscHover__SpecialistActualEffects", false)) &&
			(pCity->isActiveOwned() || //gDLL->getChtLvl() > 0))
			GC.getGame().isDebugMode())) // advc.135c
		{
			bool bStarted = false;
			CvWString szStart;
			szStart.Format(L"\n"SETCOLR L"(%s", TEXT_COLOR("COLOR_LIGHT_GREY"),
					gDLL->getText("TXT_KEY_ACTUAL_EFFECTS").GetCString());
			{
				int aiYields[NUM_YIELD_TYPES];
				FOR_EACH_ENUM(Yield)
				{
					aiYields[eLoopYield] = pCity->getAdditionalYieldBySpecialist(
							eLoopYield, eSpecialist);
				}
				bStarted = setYieldChangeHelp(szHelpString, szStart,
						L": ", L"", aiYields, false, false, bStarted);
			}
			{
				int aiCommerces[NUM_COMMERCE_TYPES];
				FOR_EACH_ENUM(Commerce)
				{
					aiCommerces[eLoopCommerce] = pCity->
							getAdditionalCommerceTimes100BySpecialist(
							eLoopCommerce, eSpecialist);
				}
				bStarted = setCommerceTimes100ChangeHelp(szHelpString, szStart,
						L": ", L"", aiCommerces, false, bStarted);
			}
			// doc: Happiness
			bStarted = setResumableValueChangeHelp(szHelpString, szStart, L": ", L"", std::abs(iHappinessChange), iHappinessChange > 0 ? gDLL->getSymbolID(HAPPY_CHAR) : gDLL->getSymbolID(UNHAPPY_CHAR), false, true, bStarted);

			// Great People
			int iGreatPeopleRate = pCity->
					getAdditionalGreatPeopleRateBySpecialist(eSpecialist);
			bStarted = setValueChangeHelp(szHelpString, szStart, L": ", L"",
					iGreatPeopleRate, gDLL->getSymbolID(
					GREAT_PEOPLE_CHAR), false, false, bStarted);

			if (bStarted)
				szHelpString.append(L")" ENDCOLR);
		} // BUG - Specialist Actual Effects - end

		if (!CvWString(kSpecialist.getHelp()).empty() && !bCivilopediaText)
		{
			szHelpString.append(NEWLINE);
			szHelpString.append(kSpecialist.getHelp());
		}
	}
}

void CvGameTextMgr::parseFreeSpecialistHelp(CvWStringBuffer &szHelpString,
	CvCity const& kCity)
{
	PROFILE_FUNC();

	FOR_EACH_ENUM2(Specialist, eSpecialist)
	{
		int iNumSpecialists = kCity.getFreeSpecialistCount(eSpecialist);

		if (iNumSpecialists > 0)
		{
			szHelpString.append(NEWLINE);
			szHelpString.append(CvWString::format(L"%s (%d): ",
					GC.getInfo(eSpecialist).getDescription(), iNumSpecialists));
			int aiYields[NUM_YIELD_TYPES];
			FOR_EACH_ENUM(Yield)
			{
				aiYields[eLoopYield] = iNumSpecialists * GET_PLAYER(kCity.getOwner()).
						specialistYield(eSpecialist, eLoopYield);
			}
			CvWStringBuffer szYield;
			setYieldChangeHelp(szYield, L"", L"", L"", aiYields, false, false);
			szHelpString.append(szYield);
			int aiCommerces[NUM_COMMERCE_TYPES];
			FOR_EACH_ENUM(Commerce)
			{
				aiCommerces[eLoopCommerce] = iNumSpecialists * GET_PLAYER(kCity.getOwner()).
						specialistCommerce(eSpecialist, eLoopCommerce);
			}
			CvWStringBuffer szCommerceString;
			setCommerceChangeHelp(szCommerceString, L"", L"", L"", aiCommerces, false, false);
			if (!szYield.isEmpty() && !szCommerceString.isEmpty())
				szHelpString.append(L", ");
			szHelpString.append(szCommerceString);
			if (GC.getInfo(eSpecialist).getExperience() > 0)
			{	// kmodx: was !szYield.isEmpty()
				if (!szYield.isEmpty() || !szCommerceString.isEmpty())
					szHelpString.append(L", ");
				szHelpString.append(gDLL->getText("TXT_KEY_SPECIALIST_EXPERIENCE_SHORT",
						iNumSpecialists * GC.getInfo(eSpecialist).getExperience()));
			}
		}
	}
}


void CvGameTextMgr::parsePromotionHelp(CvWStringBuffer &szBuffer,
	PromotionTypes ePromo, const wchar* pcNewline)
{
	PROFILE_FUNC();

	if (ePromo == NO_PROMOTION)
		return;

	CvPromotionInfo const& kPromo = GC.getInfo(ePromo);

	//if (kPromo.isBlitz())
	// <advc.164>
	int iBlitz = kPromo.getBlitz();
	if(iBlitz != 0) // </advc.164>
	{
		szBuffer.append(pcNewline);
		// <advc.164>
		if(iBlitz > 0)
		{
			if(iBlitz > 1)
				szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_BLITZ_LIMIT", iBlitz + 1));
			else szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_BLITZ_TWICE"));
		}
		else // </advc.164>
			szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_BLITZ_TEXT"));
	}

	if (kPromo.isAmphib())
	{
		szBuffer.append(pcNewline);
		// SuperSpies: TSHEEP Display Spy Messages Differently
		if (kPromo.getSound()[5] == 'P')
		{
			szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_RADIATION_TEXT_SPY"));
		}
		else
		{
			szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_AMPHIB_TEXT"));
		}
	}

	if (kPromo.isRiver())
	{
		szBuffer.append(pcNewline);
		szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_RIVER_ATTACK_TEXT"));
	}

	if (kPromo.isEnemyRoute())
	{
		szBuffer.append(pcNewline);
		szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_ENEMY_ROADS_TEXT"));
	}

	if (kPromo.isAlwaysHeal())
	{
		szBuffer.append(pcNewline);
		// SuperSpies: TSHEEP Display Spy Messages Differently
		if (kPromo.getSound()[5] == 'P')
		{
			szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_LOYALTY_TEXT_SPY"));
		}
		else
		{
			szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_ALWAYS_HEAL_TEXT"));
		}
		// SuperSpies: TSHEEP End
	}

	if (kPromo.isHillsDoubleMove())
	{
		szBuffer.append(pcNewline);
		szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_HILLS_MOVE_TEXT"));
	}

	if (kPromo.isImmuneToFirstStrikes())
	{
		szBuffer.append(pcNewline);
		szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_IMMUNE_FIRST_STRIKES_TEXT"));
	}

	// doc: no upgrade
	if (kPromo.isNoUpgrade())
	{
		szBuffer.append(pcNewline);
		szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_NO_UPGRADE"));
	}

	FOR_EACH_ENUM(Terrain)
	{
		if (kPromo.getTerrainDoubleMove(eLoopTerrain))
		{
			szBuffer.append(pcNewline);
			szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_DOUBLE_MOVE_TEXT",
					GC.getInfo(eLoopTerrain).getTextKeyWide()));
		}
	}

	FOR_EACH_ENUM(Feature)
	{
		if (kPromo.getFeatureDoubleMove(eLoopFeature))
		{
			szBuffer.append(pcNewline);
			szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_DOUBLE_MOVE_TEXT",
					GC.getInfo(eLoopFeature).getTextKeyWide()));
		}
	}

	if (kPromo.getVisibilityChange() != 0)
	{
		szBuffer.append(pcNewline);
		szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_VISIBILITY_TEXT",
				kPromo.getVisibilityChange()));
	}

	if (kPromo.getMovesChange() != 0)
	{
		szBuffer.append(pcNewline);
		szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_MOVE_TEXT",
				kPromo.getMovesChange()));
	}

	if (kPromo.getMoveDiscountChange() != 0)
	{
		szBuffer.append(pcNewline);
		szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_MOVE_DISCOUNT_TEXT",
				-kPromo.getMoveDiscountChange()));
	}

	if (kPromo.getAirRangeChange() != 0)
	{
		szBuffer.append(pcNewline);
		szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_AIR_RANGE_TEXT",
				kPromo.getAirRangeChange()));
	}

	if (kPromo.getInterceptChange() != 0)
	{
		//SuperSpies: TSHEEP Display Spy Promotions Differently
		if (kPromo.getSound()[5] == 'P')
		{
			szBuffer.append(pcNewline);
			szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_INTERCEPT_TEXT_SPY",
				kPromo.getInterceptChange()));
			szBuffer.append(pcNewline);
			szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_INTERCEPT_TEXT_SPY_COUNTER",
				kPromo.getInterceptChange() * 5));
		}
		else
		{
			szBuffer.append(pcNewline);
			szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_INTERCEPT_TEXT",
					kPromo.getInterceptChange()));
		}
	}

	if (kPromo.getEvasionChange() != 0)
	{
		szBuffer.append(pcNewline);
		// SuperSpies: TSHEEP Display Spy Promotions Differently
		if (kPromo.getSound()[5] == 'P')
		{
			szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_EVASION_TEXT_SPY",
					kPromo.getEvasionChange()));
		}
		else
		{
			szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_EVASION_TEXT",
					kPromo.getEvasionChange()));
		}
	}

	if (kPromo.getWithdrawalChange() != 0)
	{
		szBuffer.append(pcNewline);
		//SuperSpies: TSHEEP Display Spy Promotions Differently
		if (kPromo.getSound()[5] == 'P')
		{
			szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_ESCAPE_TEXT_SPY",
					kPromo.getWithdrawalChange()));
		}
		else
		{
			szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_WITHDRAWAL_TEXT",
					kPromo.getWithdrawalChange()));
		}
	}

	if (kPromo.getCargoChange() != 0)
	{
		szBuffer.append(pcNewline);
		szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_CARGO_TEXT",
				kPromo.getCargoChange()));
	}

	if (kPromo.getCollateralDamageChange() != 0)
	{
		szBuffer.append(pcNewline);
		szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_COLLATERAL_DAMAGE_TEXT",
				kPromo.getCollateralDamageChange()));
	}

	if (kPromo.getBombardRateChange() != 0)
	{
		szBuffer.append(pcNewline);
		szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_BOMBARD_TEXT",
				kPromo.getBombardRateChange()));
	}

	if (kPromo.getFirstStrikesChange() != 0)
	{
		if (kPromo.getFirstStrikesChange() == 1)
		{
			szBuffer.append(pcNewline);
			szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_FIRST_STRIKE_TEXT",
					kPromo.getFirstStrikesChange()));
		}
		else
		{
			szBuffer.append(pcNewline);
			szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_FIRST_STRIKES_TEXT",
					kPromo.getFirstStrikesChange()));
		}
	}

	if (kPromo.getChanceFirstStrikesChange() != 0)
	{
		if (kPromo.getChanceFirstStrikesChange() == 1)
		{
			szBuffer.append(pcNewline);
			szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_FIRST_STRIKE_CHANCE_TEXT",
					kPromo.getChanceFirstStrikesChange()));
		}
		else
		{
			szBuffer.append(pcNewline);
			szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_FIRST_STRIKES_CHANCE_TEXT",
					kPromo.getChanceFirstStrikesChange()));
		}
	}

	if (kPromo.getEnemyHealChange() != 0)
	{
		szBuffer.append(pcNewline);
		// SuperSpies: TSHEEP Display Spy Promotions Differently
		if (kPromo.getSound()[5] == 'P')
		{
			szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_INSTIGATE_TEXT_SPY",
					kPromo.getEnemyHealChange()));
		}
		else
		{
			szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_HEALS_EXTRA_TEXT",
					kPromo.getEnemyHealChange()) +
					gDLL->getText("TXT_KEY_PROMOTION_ENEMY_LANDS_TEXT"));
		}
	}

	if (kPromo.getNeutralHealChange() != 0)
	{
		szBuffer.append(pcNewline);
		//SuperSpies: TSHEEP Display Spy Promotions Differently
		if (kPromo.getSound()[5] == 'P')
		{
			szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_INSTIGATE2_TEXT_SPY",
					kPromo.getNeutralHealChange()));
		}
		else
		{
			szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_HEALS_EXTRA_TEXT",
					kPromo.getNeutralHealChange()) +
					gDLL->getText("TXT_KEY_PROMOTION_NEUTRAL_LANDS_TEXT"));
		}
	}

	if (kPromo.getFriendlyHealChange() != 0)
	{
		szBuffer.append(pcNewline);
		// SuperSpies: TSHEEP Display Spy Promotions Differently
		if (kPromo.getSound()[5] == 'P')
		{
			szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_POISON_TEXT_SPY",
					kPromo.getFriendlyHealChange()));
		}
		else
		{
			szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_HEALS_EXTRA_TEXT",
					kPromo.getFriendlyHealChange()) +
					gDLL->getText("TXT_KEY_PROMOTION_FRIENDLY_LANDS_TEXT"));
		}
	}

	if (kPromo.getSameTileHealChange() != 0)
	{
		szBuffer.append(pcNewline);
		szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_HEALS_SAME_TEXT",
				kPromo.getSameTileHealChange()) +
				gDLL->getText("TXT_KEY_PROMOTION_DAMAGE_TURN_TEXT"));
	}

	if (kPromo.getAdjacentTileHealChange() != 0)
	{
		szBuffer.append(pcNewline);
		szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_HEALS_ADJACENT_TEXT",
				kPromo.getAdjacentTileHealChange()) +
				gDLL->getText("TXT_KEY_PROMOTION_DAMAGE_TURN_TEXT"));
	}

	if (kPromo.getCombatPercent() != 0)
	{
		szBuffer.append(pcNewline);
		szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_STRENGTH_TEXT",
				kPromo.getCombatPercent()));
	}

	if (kPromo.getCityAttackPercent() != 0)
	{
		szBuffer.append(pcNewline);
		szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_CITY_ATTACK_TEXT",
				kPromo.getCityAttackPercent()));
	}

	if (kPromo.getCityDefensePercent() != 0)
	{
		szBuffer.append(pcNewline);
		szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_CITY_DEFENSE_TEXT",
				kPromo.getCityDefensePercent()));
	}

	if (kPromo.getHillsAttackPercent() != 0)
	{
		szBuffer.append(pcNewline);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_HILLS_ATTACK",
				kPromo.getHillsAttackPercent()));
	}

	if (kPromo.getHillsDefensePercent() != 0)
	{
		szBuffer.append(pcNewline);
		szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_HILLS_DEFENSE_TEXT",
				kPromo.getHillsDefensePercent()));
	}

	// doc: open terrain attack
	if (kPromo.getPlainsAttackPercent() != 0)
	{
		szBuffer.append(pcNewline);
		szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_PLAINS_ATTACK_TEXT",
				kPromo.getPlainsAttackPercent()));
	}

	// doc: open terrain defense
	if (kPromo.getPlainsDefensePercent() != 0)
	{
		szBuffer.append(pcNewline);
		szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_PLAINS_DEFENSE_TEXT",
				kPromo.getPlainsDefensePercent()));
	}

	// doc: river attack
	if (GC.getPromotionInfo(ePromotion).getRiverAttackPercent() != 0)
	{
		szBuffer.append(pcNewline);
		szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_EXTRA_RIVER_ATTACK_TEXT",
				kPromo.getRiverAttackPercent()));
	}

	if (kPromo.getRevoltProtection() != 0)
	{
		szBuffer.append(pcNewline);
		szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_REVOLT_PROTECTION_TEXT",
				kPromo.getRevoltProtection()));
	}

	if (kPromo.getCollateralDamageProtection() != 0)
	{
		szBuffer.append(pcNewline);
		szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_COLLATERAL_PROTECTION_TEXT",
				kPromo.getCollateralDamageProtection()));
	}

	if (kPromo.getPillageChange() != 0)
	{
		szBuffer.append(pcNewline);
		szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_PILLAGE_CHANGE_TEXT",
				kPromo.getPillageChange()));
	}

	if (kPromo.getUpgradeDiscount() != 0)
	{
		// SuperSpies: TSHEEP Display Spy Promotions Differently
		if (kPromo.getSound()[5] == 'P')
		{
			szBuffer.append(pcNewline);
			szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_UPGRADE_DISCOUNT_TEXT_SPY",
					kPromo.getUpgradeDiscount()));
		}
		else if (100 == kPromo.getUpgradeDiscount())
		{
			szBuffer.append(pcNewline);
			szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_UPGRADE_DISCOUNT_FREE_TEXT"));
		}
		else
		{
			szBuffer.append(pcNewline);
			szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_UPGRADE_DISCOUNT_TEXT",
					kPromo.getUpgradeDiscount()));
		}
	}

	if (kPromo.getExperiencePercent() != 0)
	{
		szBuffer.append(pcNewline);
		szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_FASTER_EXPERIENCE_TEXT",
				kPromo.getExperiencePercent()));
	}

	if (kPromo.getKamikazePercent() != 0)
	{
		szBuffer.append(pcNewline);
		szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_KAMIKAZE_TEXT",
				kPromo.getKamikazePercent()));
	}

	// doc: extra upkeep
	if (kPromo.getExtraUpkeep() != 0)
	{
		szBuffer.append(pcNewline);
		szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_EXTRA_UPKEEP_TEXT",
				kPromo.getExtraUpkeep()));
	}

	FOR_EACH_ENUM(Terrain)
	{
		if (kPromo.getTerrainAttackPercent(eLoopTerrain) != 0)
		{
			szBuffer.append(pcNewline);
			szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_ATTACK_TEXT",
					kPromo.getTerrainAttackPercent(eLoopTerrain),
					GC.getInfo(eLoopTerrain).getTextKeyWide()));
		}
		if (kPromo.getTerrainDefensePercent(eLoopTerrain) != 0)
		{
			szBuffer.append(pcNewline);
			szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_DEFENSE_TEXT",
					kPromo.getTerrainDefensePercent(eLoopTerrain),
					GC.getInfo(eLoopTerrain).getTextKeyWide()));
		}
	}

	FOR_EACH_ENUM(Feature)
	{
		if (kPromo.getFeatureAttackPercent(eLoopFeature) != 0)
		{
			szBuffer.append(pcNewline);
			szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_ATTACK_TEXT",
					kPromo.getFeatureAttackPercent(eLoopFeature),
					GC.getInfo(eLoopFeature).getTextKeyWide()));
		}
		if (kPromo.getFeatureDefensePercent(eLoopFeature) != 0)
		{
			szBuffer.append(pcNewline);
			szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_DEFENSE_TEXT",
					kPromo.getFeatureDefensePercent(eLoopFeature),
					GC.getInfo(eLoopFeature).getTextKeyWide()));
		}
	}

	FOR_EACH_ENUM(UnitCombat)
	{
		if (kPromo.getUnitCombatModifierPercent(eLoopUnitCombat) != 0)
		{
			szBuffer.append(pcNewline);
			szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_VERSUS_TEXT",
					kPromo.getUnitCombatModifierPercent(eLoopUnitCombat),
					GC.getInfo(eLoopUnitCombat).getTextKeyWide()));
		}
	}

	FOR_EACH_ENUM(Domain)
	{
		if (kPromo.getDomainModifierPercent(eLoopDomain) != 0)
		{
			szBuffer.append(pcNewline);
			szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_VERSUS_TEXT",
					kPromo.getDomainModifierPercent(eLoopDomain),
					GC.getInfo(eLoopDomain).getTextKeyWide()));
		}
	}

	if (wcslen(kPromo.getHelp()) > 0)
	{
		szBuffer.append(pcNewline);
		szBuffer.append(kPromo.getHelp());
	}

	/*	<advc.004e> Show the promotions that ePromotion leads to.
		Based on CvPediaPromotion.py and CvUnit::canAcquirePromotion. */
	CvUnit const* pHeadSelectedUnit = gDLL->UI().getHeadSelectedUnit();
	std::vector<PromotionTypes> aeReq;
	std::vector<PromotionTypes> aeAltReq;
	FOR_EACH_ENUM2(Promotion, eLoopPromo)
	{
		CvPromotionInfo const& kLoopPromo = GC.getInfo(eLoopPromo);
		if(pHeadSelectedUnit != NULL && pHeadSelectedUnit->getOwner() != NO_PLAYER)
		{
			// Don't show eLoopPromotion if any requirements other than ePromotion aren't met
			CvUnit const& kUnit = *pHeadSelectedUnit;
			if(!kUnit.isPromotionValid(eLoopPromo))
				continue;
			if(kUnit.isHasPromotion(eLoopPromo) || kUnit.canAcquirePromotion(eLoopPromo))
				continue;
			CvPlayer const& kOwner = GET_PLAYER(kUnit.getOwner());
			if(kLoopPromo.getTechPrereq() != NO_TECH &&
				!GET_TEAM(kOwner.getTeam()).isHasTech((TechTypes)
				kLoopPromo.getTechPrereq()))
			{
				continue;
			}
			if(kLoopPromo.getStateReligionPrereq() != NO_RELIGION &&
				kOwner.getStateReligion() != kLoopPromo.getStateReligionPrereq())
			{
				continue;
			}
		}
		if(kLoopPromo.getPrereqPromotion() == ePromo)
			aeReq.push_back(eLoopPromo);
		if(kLoopPromo.getPrereqOrPromotion1() == ePromo ||
			kLoopPromo.getPrereqOrPromotion2() == ePromo ||
			kLoopPromo.getPrereqOrPromotion3() == ePromo)
		{
			aeAltReq.push_back(eLoopPromo);
		}
	}
	if(!aeReq.empty())
	{
		szBuffer.append(pcNewline);
		szBuffer.append(gDLL->getText("TXT_KEY_REQUIRED_FOR"));
		bool bFirst = true;
		for(size_t i = 0; i < aeReq.size(); i++)
		{
			setListHelp(szBuffer, L" ", GC.getInfo(aeReq[i]).getDescription(),
					L", ", bFirst);
		}
	}
	if(!aeAltReq.empty())
	{
		szBuffer.append(pcNewline);
		szBuffer.append(gDLL->getText("TXT_KEY_LEADS_TO"));
		bool bFirst = true;
		for(size_t i = 0; i < aeAltReq.size(); i++)
		{
			setListHelp(szBuffer, L" ", GC.getInfo(aeAltReq[i]).getDescription(),
					L", ", bFirst);
		};
	}
	// </advc.004e>
}

// advc.mnai (lfgr UI 11/2020): For "Allows civic" buttons in Tech tree
void CvGameTextMgr::parseSingleCivicRevealHelp(CvWStringBuffer& szBuffer, CivicTypes eCivic)
{
	szBuffer.append(CvWString::format(SETCOLR L"%s" ENDCOLR,
			TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
			GC.getInfo(eCivic).getDescription()));
	CvWStringBuffer szCivicHelp;
	GAMETEXT.parseCivicInfo(szCivicHelp, eCivic,
			true, true, true); // bCiviliopedia=true to hide tech prereq
	szBuffer.append(szCivicHelp);
}


void CvGameTextMgr::parseCivicInfo(CvWStringBuffer &szHelpText, CivicTypes eCivic, bool bCivilopediaText,
	bool bPlayerContext, bool bSkipName)
{
	PROFILE_FUNC();

	if(NO_CIVIC == eCivic)
		return;

	szHelpText.clear();

	PlayerTypes const eActivePlayer = getActivePlayer();
	FAssert(eActivePlayer != NO_PLAYER || !bPlayerContext);
	CvCivicInfo const& kCivic = GC.getInfo(eCivic);

	if (!bSkipName)
		szHelpText.append(kCivic.getDescription());

	if (!bCivilopediaText)
	{
		if (!bPlayerContext || !GET_PLAYER(eActivePlayer).canDoCivics(eCivic))
		{	// <advc.912d>
			bool bValid = true;
			if(bPlayerContext && GC.getGame().isOption(GAMEOPTION_NO_SLAVERY) &&
				GET_PLAYER(eActivePlayer).isHuman())
			{
				FOR_EACH_ENUM(Hurry)
				{
					if(kCivic.isHurry(eLoopHurry) && GC.getInfo(eLoopHurry).
						getProductionPerPopulation() > 0)
					{
						bValid = false;
						szHelpText.append(NEWLINE);
						szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_BLOCKED_BY_OPTION",
								kCivic.getDescription(),
								GC.getInfo(GAMEOPTION_NO_SLAVERY).getDescription()));
					}
				}
			} // </advc.912d>
			if (!bPlayerContext ||
				(bValid && // advc.912d: Don't show tech req if disabled by option
				!GET_TEAM(getActiveTeam()).isHasTech(kCivic.getTechPrereq())))
			{
				if (kCivic.getTechPrereq() != NO_TECH)
				{
					szHelpText.append(NEWLINE);
					szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_REQUIRES",
							GC.getInfo(kCivic.getTechPrereq()).getTextKeyWide()));
				}
			}
		}
	}

	// Special Building Not Required...
	FOR_EACH_ENUM(SpecialBuilding)
	{
		if (kCivic.isSpecialBuildingNotRequired(eLoopSpecialBuilding))
		{
			// XXX "Missionaries"??? - Now in XML
			szHelpText.append(NEWLINE);
			szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_BUILD_MISSIONARIES",
					GC.getInfo(eLoopSpecialBuilding).getTextKeyWide()));
		}
	}

	// Valid Specialists...

	CvWString szFirstBuffer;
	{
		bool bFirst = true;
		FOR_EACH_ENUM(Specialist)
		{
			if (!kCivic.isSpecialistValid(eLoopSpecialist))
				continue;
			szFirstBuffer.Format(L"%s%s", NEWLINE,
					gDLL->getText("TXT_KEY_CIVIC_UNLIMTED").c_str());
			CvWString szSpecialist;
			/*szSpecialist.Format(L"<link=literal>%s</link>",
					GC.getSpecialistInfo(eLoopSpecialist).getDescription());*/
			setSpecialistLink(szSpecialist, eLoopSpecialist, true); // advc.001
			setListHelp(szHelpText, szFirstBuffer, szSpecialist, L", ", bFirst);
		}
	}

	// doc: Level experience modifier
	if (kCivic.getLevelExperienceModifier() != 0)
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_LEVEL_MODIFIER",
				kCivic.getLevelExperienceModifier()));
	}

	//	Great People Modifier...
	if (kCivic.getGreatPeopleRateModifier() != 0)
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_GREAT_PEOPLE_MOD",
				kCivic.getGreatPeopleRateModifier()));
	}

	//	Great General Modifier...
	if (kCivic.getGreatGeneralRateModifier() != 0)
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_GREAT_GENERAL_MOD",
				kCivic.getGreatGeneralRateModifier()));
	}

	if (kCivic.getDomesticGreatGeneralRateModifier() != 0)
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_DOMESTIC_GREAT_GENERAL_MODIFIER",
				kCivic.getDomesticGreatGeneralRateModifier()));
	}

	//	State Religion Great People Modifier...
	if (kCivic.getStateReligionGreatPeopleRateModifier() != 0)
	{
		if (bPlayerContext &&
			GET_PLAYER(eActivePlayer).getStateReligion() != NO_RELIGION)
		{
			szHelpText.append(NEWLINE);
			szHelpText.append(gDLL->getText(
					"TXT_KEY_CIVIC_GREAT_PEOPLE_MOD_RELIGION",
					kCivic.getStateReligionGreatPeopleRateModifier(),
					GC.getInfo(GET_PLAYER(eActivePlayer).getStateReligion()).getChar()));
		}
		else
		{
			szHelpText.append(NEWLINE);
			szHelpText.append(gDLL->getText(
					"TXT_KEY_CIVIC_GREAT_PEOPLE_MOD_STATE_RELIGION",
					kCivic.getStateReligionGreatPeopleRateModifier(),
					gDLL->getSymbolID(RELIGION_CHAR)));
		}
	}

	//	Distance Maintenance Modifer...
	if (kCivic.getDistanceMaintenanceModifier() != 0)
	{
		if (kCivic.getDistanceMaintenanceModifier() <= -100)
		{
			szHelpText.append(NEWLINE);
			szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_DISTANCE_MAINT"));
		}
		else
		{
			szHelpText.append(NEWLINE);
			szHelpText.append(gDLL->getText(
					"TXT_KEY_CIVIC_DISTANCE_MAINT_MOD",
					kCivic.getDistanceMaintenanceModifier()));
		}
	}

	//	Num Cities Maintenance Modifer...
	if (kCivic.getNumCitiesMaintenanceModifier() != 0)
	{
		if (kCivic.getNumCitiesMaintenanceModifier() <= -100)
		{
			szHelpText.append(NEWLINE);
			szHelpText.append(gDLL->getText(
					"TXT_KEY_CIVIC_NO_MAINT_NUM_CITIES"));
		}
		else
		{
			szHelpText.append(NEWLINE);
			szHelpText.append(gDLL->getText(
					"TXT_KEY_CIVIC_NO_MAINT_NUM_CITIES_MOD",
					kCivic.getNumCitiesMaintenanceModifier()));
		}
	}

	//	Corporations Maintenance Modifer...
	if (kCivic.getCorporationMaintenanceModifier() != 0)
	{
		if (kCivic.getCorporationMaintenanceModifier() <= -100)
		{
			szHelpText.append(NEWLINE);
			szHelpText.append(gDLL->getText(
					"TXT_KEY_CIVIC_NO_MAINT_CORPORATION"));
		}
		else
		{
			szHelpText.append(NEWLINE);
			szHelpText.append(gDLL->getText(
					"TXT_KEY_CIVIC_NO_MAINT_CORPORATION_MOD",
					kCivic.getCorporationMaintenanceModifier()));
		}
	}

	// doc: corporation unhappiness modifier
	if (kCivic.getCorporationUnhappinessModifier() != 0)
	{
		szHelpText.append(NEWLINE);
		if (kCivic.getCorporationUnhappinessModifier() <= -100)
		{
			szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_NO_UNHAPPINESS_CORPORATION"));
		}
		else
		{
			szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_NO_UNHAPPINESS_CORPORATION_MOD", +
					kCivic.getCorporationUnhappinessModifier()));
		}
	}

	// <advc.912g>
	if (kCivic.getColonyMaintenanceModifier() != 0)
	{
		if (kCivic.getColonyMaintenanceModifier() <= -100)
		{
			szHelpText.append(NEWLINE);
			szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_COLONY_MAINT"));
		}
		else
		{
			szHelpText.append(NEWLINE);
			szHelpText.append(gDLL->getText(
					"TXT_KEY_CIVIC_COLONY_MAINT_MOD",
					kCivic.getColonyMaintenanceModifier()));
		}
	} // </advc.912g>
	//	Extra Health
	if (kCivic.getExtraHealth() != 0)
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_EXTRA_HEALTH",
				abs(kCivic.getExtraHealth()),
				kCivic.getExtraHealth() > 0 ?
				gDLL->getSymbolID(HEALTHY_CHAR) :
				gDLL->getSymbolID(UNHEALTHY_CHAR)));
	}

	//	Extra Happiness (new in K-Mod)
	if (kCivic.getExtraHappiness() != 0)
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_EXTRA_HEALTH",
				abs(kCivic.getExtraHappiness()),
				kCivic.getExtraHappiness() > 0 ?
				gDLL->getSymbolID(HAPPY_CHAR) :
				gDLL->getSymbolID(UNHAPPY_CHAR)));
		/*	note: TXT_KEY_CIVIC_EXTRA_HEALTH just says "[blah] in all cities",
			so it's ok for happiness as well as for health. */
	}

	//	Free Experience
	if (kCivic.getFreeExperience() != 0)
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_FREE_XP",
				kCivic.getFreeExperience()));
	}

	// doc: domain free experience
	FOR_EACH_ENUM(Domain)
	{
		if (kCivic.getDomainExperienceModifier(eLoopDomain) != 0)
		{
			szHelpText.append(NEWLINE);
			szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_DOMAIN_XP",
				kCivic.getDomainExperienceModifier(eLoopDomain), GC.getInfo(eLoopDomain).getText()));
		}
	}

	//	Worker speed modifier
	if (kCivic.getWorkerSpeedModifier() != 0)
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_WORKER_SPEED",
				kCivic.getWorkerSpeedModifier()));
	}

	// doc: Process yield modifier
	if (kCivic.getProcessModifier() != 0)
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_PROCESS_MODIFIER",
				kCivic.getProcessModifier()));
	}

	// doc: food production modifier
	if (kCivic.getFoodProductionModifier() != 0)
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_FOOD_TO_PRODUCTION_MODIFIER",
				kCivic.getFoodProductionModifier()));
	}

	//	Improvement upgrade rate modifier
	if (kCivic.getImprovementUpgradeRateModifier() != 0)
	{
		int iLast = 0;
		FOR_EACH_ENUM(Improvement)
		{
			if (GC.getInfo(eLoopImprovement).getImprovementUpgrade() != NO_IMPROVEMENT)
			{
				szFirstBuffer.Format(L"%s%s", NEWLINE,
						gDLL->getText("TXT_KEY_CIVIC_IMPROVEMENT_UPGRADE",
						kCivic.getImprovementUpgradeRateModifier()).c_str());
				CvWString szImprovement;
				szImprovement.Format(L"<link=literal>%s</link>",
						GC.getInfo(eLoopImprovement).getDescription());
				setListHelp(szHelpText, szFirstBuffer, szImprovement, L", ",
						iLast, kCivic.getImprovementUpgradeRateModifier());
			}
		}
	}

	//	Military unit production modifier
	if (kCivic.getMilitaryProductionModifier() != 0)
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_MILITARY_PRODUCTION",
				kCivic.getMilitaryProductionModifier()));
	}

	//	Free units population percent
	if (kCivic.getBaseFreeUnits() != 0 ||
		kCivic.getFreeUnitsPopulationPercent() != 0)
	{
		if (bPlayerContext)
		{
			szHelpText.append(NEWLINE);
			szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_FREE_UNITS",
					(kCivic.getBaseFreeUnits() +
					((GET_PLAYER(eActivePlayer).getTotalPopulation() *
					kCivic.getFreeUnitsPopulationPercent()) / 100))));
		}
		else
		{
			szHelpText.append(NEWLINE);
			szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_UNIT_SUPPORT"));
		}
	}

	//	Free military units population percent
	if (kCivic.getBaseFreeMilitaryUnits() != 0 ||
		kCivic.getFreeMilitaryUnitsPopulationPercent() != 0)
	{
		if (bPlayerContext)
		{
			szHelpText.append(NEWLINE);
			szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_FREE_MILITARY_UNITS",
					kCivic.getBaseFreeMilitaryUnits() +
					((GET_PLAYER(eActivePlayer).getTotalPopulation() *
					kCivic.getFreeMilitaryUnitsPopulationPercent()) / 100)));
		}
		else
		{
			szHelpText.append(NEWLINE);
			szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_MILITARY_UNIT_SUPPORT"));
		}
	}

	int const iHappyPerMilitaryUnit = kCivic.getHappyPerMilitaryUnit(); // advc
	if (iHappyPerMilitaryUnit != 0)
	{
		szHelpText.append(NEWLINE);
		/*  <advc.912c> If a player reverts to the BtS ability through XML,
			show the old help text (instead of "+2 happiness per 2 units"). */
		int iAbsHappyPerMilitaryUnit = abs(iHappyPerMilitaryUnit);
		if(iAbsHappyPerMilitaryUnit == 2)
		{
			szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_UNIT_HAPPINESS",
					iAbsHappyPerMilitaryUnit / 2, iHappyPerMilitaryUnit > 0 ?
					gDLL->getSymbolID(HAPPY_CHAR) : gDLL->getSymbolID(UNHAPPY_CHAR)));
		}
		else
		{
			szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_UNIT_HAPPINESS2", // </advc.912c>
					/*kCivic.getHappyPerMilitaryUnit(), ((kCivic.getHappyPerMilitaryUnit() > 0) ?
							gDLL->getSymbolID(HAPPY_CHAR) : gDLL->getSymbolID(UNHAPPY_CHAR))));*/ // BtS
					/*	UNOFFICIAL_PATCH, Bugfix, 08/28/09, jdog5000 (start):
						Use absolute value with unhappy face */
					iAbsHappyPerMilitaryUnit, iHappyPerMilitaryUnit > 0 ?
					gDLL->getSymbolID(HAPPY_CHAR) : gDLL->getSymbolID(UNHAPPY_CHAR)));
					// UNOFFICIAL_PATCH (end)
			// <advc.912c>
		}
	}
	if(kCivic.getLuxuryModifier() != 0)
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_LUXURY_MODIFIER",
				kCivic.getLuxuryModifier(), gDLL->getSymbolID(HAPPY_CHAR)));
	} // </advc.912c>

	//	Military units produced with food
	if (kCivic.isMilitaryFoodProduction())
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_MILITARY_FOOD"));
	}

	//	Conscription
	if (GC.getGame().getMaxConscript(eCivic) != 0)
	{
		szHelpText.append(NEWLINE);
		// <advc.004y>
		/*  Caller doesn't seem to set bPlayerContext and bCivilopediaText
			properly; will have to figure it out on our own: */
		bool bRange = (eActivePlayer == NO_PLAYER);
		if(bRange)
		{
			int iBase = kCivic.getMaxConscript();
			int iLow = (iBase * std::max(0, (GC.getInfo((WorldSizeTypes)0).
					getMaxConscriptModifier() + 100))) / 100;
			int iHigh = (iBase * std::max(0, GC.getInfo((WorldSizeTypes)
					(GC.getNumWorldInfos() - 1)).getMaxConscriptModifier() + 100)) / 100;
			if(iHigh == iLow)
				bRange = false;
			else
			{
				szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_CONSCRIPTION_RANGE",
						iLow, iHigh));
			}
		}
		if(!bRange) // </advc.004y>
		{
			szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_CONSCRIPTION",
					GC.getGame().getMaxConscript(eCivic)));
		}
	}

	//	Population Unhealthiness
	// K-Mod, 27/dec/10: replace with UnhealthyPopulationModifier
	/*if (kCivic.isNoUnhealthyPopulation()) {
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_NO_POP_UNHEALTHY"));
	}*/ // BtS
	if (kCivic.getUnhealthyPopulationModifier() != 0)
	{
		/*	If the modifier is less than -100, display the old NoUnhealth text.
			Note: this could be technically inaccurate if we combine
			this modifier with a positive modifier */
		if (kCivic.getUnhealthyPopulationModifier() <= -100)
		{
			szHelpText.append(NEWLINE);
			szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_NO_POP_UNHEALTHY"));
		}
		else
		{
			szHelpText.append(NEWLINE);
			szHelpText.append(gDLL->getText("TXT_KEY_UNHEALTHY_POP_MODIFIER",
					kCivic.getUnhealthyPopulationModifier()));
		}
	}
	// K-Mod end

	//	Building Unhealthiness
	if (kCivic.isBuildingOnlyHealthy())
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_NO_BUILDING_UNHEALTHY"));
	}

	//	Experience in borders modifier
	if (kCivic.getExpInBorderModifier() != 0)
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_EXPERIENCE_IN_BORDERS",
				kCivic.getExpInBorderModifier()));
	}

	//	War Weariness
	if (kCivic.getWarWearinessModifier() != 0)
	{
		if (kCivic.getWarWearinessModifier() <= -100)
		{
			szHelpText.append(NEWLINE);
			szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_NO_WAR_WEARINESS"));
		}
		else
		{
			szHelpText.append(NEWLINE);
			szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_EXTRA_WAR_WEARINESS",
					kCivic.getWarWearinessModifier()));
		}
	}

	// doc: wonder production modifier
	if (kCivic.getWonderProductionModifier() != 0)
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_WONDER_PRODUCTION",
					kCivic.getWonderProductionModifier()));
	}

	//	Free specialists
	if (kCivic.getFreeSpecialist() != 0)
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_FREE_SPECIALISTS",
				kCivic.getFreeSpecialist()));
	}
	//	Trade routes
	if (kCivic.getTradeRoutes() != 0)
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_TRADE_ROUTES",
				kCivic.getTradeRoutes()));
	}

	// doc: Corporation commerce
	if (kCivic.getCorporationCommerceModifier() != 0)
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_CORPORATION_COMMERCE",
				kCivic.getCorporationCommerceModifier()));
	}

	//	No Foreign Trade
	if (kCivic.isNoForeignTrade())
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_NO_FOREIGN_TRADE"));
	}

	// doc: no benefit from foreign trade
	if (kCivic.isNoForeignTradeModifier())
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_NO_FOREIGN_TRADE_MODIFIER"));
	}

	// doc: defensive pact trade modifier
	if (kCivic.getDefensivePactTradeModifier() != 0)
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_DEFENSIVE_PACT_TRADE_MODIFIER",
				kCivic.getDefensivePactTradeModifier()));
	}

	// doc: vassal trade modifier
	if (kCivic.getVassalTradeModifier() != 0)
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_VASSAL_TRADE_MODIFIER",
				kCivic.getVassalTradeModifier()));
	}

	//	No Corporations
	if (kCivic.isNoCorporations())
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_NO_CORPORATIONS"));
	}
	//	No Foreign Corporations
	if (kCivic.isNoForeignCorporations())
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_NO_FOREIGN_CORPORATIONS"));
	}

	// doc: can capture workers
	if (kCivic.isSlavery())
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_CAN_CAPTURE_WORKERS"));
	}

	//	Freedom Anger
	if (kCivic.getCivicPercentAnger() != 0)
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_FREEDOM_ANGER",
				kCivic.getTextKeyWide()));
	}

	if (!kCivic.isStateReligion())
	{
		bool bFound = false;

		FOR_EACH_ENUM(Civic)
		{
			if (GC.getInfo(eLoopCivic).getCivicOptionType() ==
				kCivic.getCivicOptionType() &&
				GC.getInfo(eLoopCivic).isStateReligion())
			{
				bFound = true;
			}
		}

		if (bFound)
		{
            szHelpText.append(NEWLINE);
            szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_NO_STATE_RELIGION"));
		}
	}

	if (kCivic.getStateReligionHappiness() != 0)
	{
		if (bPlayerContext &&
			GET_PLAYER(eActivePlayer).getStateReligion() != NO_RELIGION)
		{
			szHelpText.append(NEWLINE);
			szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_STATE_RELIGION_HAPPINESS",
					abs(kCivic.getStateReligionHappiness()),
					kCivic.getStateReligionHappiness() > 0 ?
					gDLL->getSymbolID(HAPPY_CHAR) :
					gDLL->getSymbolID(UNHAPPY_CHAR),
					GC.getInfo(GET_PLAYER(eActivePlayer).getStateReligion()).getChar()));
		}
		else
		{
			szHelpText.append(NEWLINE);
			szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_RELIGION_HAPPINESS",
					abs(kCivic.getStateReligionHappiness()),
					kCivic.getStateReligionHappiness() > 0 ?
					gDLL->getSymbolID(HAPPY_CHAR) : gDLL->getSymbolID(UNHAPPY_CHAR)));
		}
	}

	if (kCivic.getNonStateReligionHappiness() != 0)
	{
		if (!kCivic.isStateReligion())
		{
			szHelpText.append(NEWLINE);
			szHelpText.append(
					gDLL->getText("TXT_KEY_CIVIC_NON_STATE_REL_HAPPINESS_NO_STATE",
					/*	UNOFFICIAL_PATCH, Bugfix, 08/28/09, EmperorFool & jdog5000:
						(params were missing) */
					abs(kCivic.getNonStateReligionHappiness()),
					kCivic.getNonStateReligionHappiness() > 0 ?
					gDLL->getSymbolID(HAPPY_CHAR) : gDLL->getSymbolID(UNHAPPY_CHAR)));
		}
		else
		{
			szHelpText.append(NEWLINE);
			szHelpText.append(
					gDLL->getText("TXT_KEY_CIVIC_NON_STATE_REL_HAPPINESS_WITH_STATE",
					abs(kCivic.getNonStateReligionHappiness()),
					kCivic.getNonStateReligionHappiness() > 0 ?
					gDLL->getSymbolID(HAPPY_CHAR) : gDLL->getSymbolID(UNHAPPY_CHAR)));
		}
	}

	//	State Religion Unit Production Modifier
	if (kCivic.getStateReligionUnitProductionModifier() != 0)
	{
		if (bPlayerContext &&
			(GET_PLAYER(eActivePlayer).getStateReligion() != NO_RELIGION))
		{
			szHelpText.append(NEWLINE);
			szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_REL_TRAIN_BONUS",
					GC.getInfo(GET_PLAYER(eActivePlayer).getStateReligion()).getChar(),
					kCivic.getStateReligionUnitProductionModifier()));
		}
		else
		{
			szHelpText.append(NEWLINE);
			szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_STATE_REL_TRAIN_BONUS",
					kCivic.getStateReligionUnitProductionModifier()));
		}
	}

	//	State Religion Building Production Modifier
	if (kCivic.getStateReligionBuildingProductionModifier() != 0)
	{
		if (bPlayerContext &&
			(GET_PLAYER(eActivePlayer).getStateReligion() != NO_RELIGION))
		{
			szHelpText.append(NEWLINE);
			szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_REL_BUILDING_BONUS",
					GC.getInfo(GET_PLAYER(eActivePlayer).getStateReligion()).getChar(),
					kCivic.getStateReligionBuildingProductionModifier()));
		}
		else
		{
			szHelpText.append(NEWLINE);
			szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_STATE_REL_BUILDING_BONUS",
					kCivic.getStateReligionBuildingProductionModifier()));
		}
	}

	//	State Religion Free Experience
	if (kCivic.getStateReligionFreeExperience() != 0)
	{
		if (bPlayerContext &&
			GET_PLAYER(eActivePlayer).getStateReligion() != NO_RELIGION)
		{
			szHelpText.append(NEWLINE);
			szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_REL_FREE_XP",
					kCivic.getStateReligionFreeExperience(),
					GC.getInfo(GET_PLAYER(eActivePlayer).getStateReligion()).getChar()));
		}
		else
		{
			szHelpText.append(NEWLINE);
			szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_STATE_REL_FREE_XP",
					kCivic.getStateReligionFreeExperience()));
		}
	}

	if (kCivic.isNoNonStateReligionSpread())
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_NO_NON_STATE_SPREAD"));
	}

	if (kCivic.getNonStateReligionHappiness() != 0)
	{
		if (kCivic.isStateReligion())
		{
			szHelpText.append(NEWLINE);
			// doc (edead): fix display
			szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_NON_STATE_REL_HAPPINESS_WITH_STATE",
					abs(kCivic.getNonStateReligionHappiness()),
					kCivic.getNonStateReligionHappiness() > 0 ? gDLL->getSymbolID(HAPPY_CHAR) : gDLL->getSymbolID(UNHAPPY_CHAR));
		}
		else
		{
			szHelpText.append(NEWLINE);
			szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_NON_STATE_REL_HAPPINESS_WITH_STATE", abs(GC.getCivicInfo(eCivic).getNonStateReligionHappiness()), ((GC.getCivicInfo(eCivic).getNonStateReligionHappiness() > 0) ? gDLL->getSymbolID(HAPPY_CHAR) : gDLL->getSymbolID(UNHAPPY_CHAR))));
		}
	}

	// doc: no anarchy from state religion changes
	if (kCivic.isNoStateReligionAnarchy())
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_NO_STATE_RELIGION_ANARCHY"));
	}

	// doc: shrine income modifier
	if (kCivic.getShrineIncomeLimitChange() != 0)
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_SHRINE_INCOME_LIMIT_CHANGE",
					kCivic.getShrineIncomeLimitChange()));
	}

	// State Religion yield change
	setYieldChangeHelp(szHelpText, L"", L"", gDLL->getText("TXT_KEY_CIVIC_FROM_STATE_RELIGION_BUILDINGS").GetCString(), GC.getCivicInfo(eCivic).getStateReligionBuildingYieldArray());

	//	Yield Modifiers
	setYieldChangeHelp(szHelpText, L"", L"",
			gDLL->getText("TXT_KEY_CIVIC_IN_ALL_CITIES").GetCString(),
			kCivic.getYieldModifierArray(), true);
	//	Capital Yield Modifiers
	setYieldChangeHelp(szHelpText, L"", L"",
			gDLL->getText("TXT_KEY_CIVIC_IN_CAPITAL").GetCString(),
			kCivic.getCapitalYieldModifierArray(), true);
	//	Trade Yield Modifiers
	setYieldChangeHelp(szHelpText, L"", L"",
			gDLL->getText("TXT_KEY_CIVIC_FROM_TRADE_ROUTES").GetCString(),
			kCivic.getTradeYieldModifierArray(), true);
	//	Commerce Modifier
	setCommerceChangeHelp(szHelpText, L"", L"",
			gDLL->getText("TXT_KEY_CIVIC_IN_ALL_CITIES").GetCString(),
			kCivic.getCommerceModifierArray(), true);
	//	Capital Commerce Modifiers
	setCommerceChangeHelp(szHelpText, L"", L"",
			gDLL->getText("TXT_KEY_CIVIC_IN_CAPITAL").GetCString(),
			kCivic.getCapitalCommerceModifierArray(), true);
	//	Specialist Commerce
	setCommerceChangeHelp(szHelpText, L"", L"",
			gDLL->getText("TXT_KEY_CIVIC_PER_SPECIALIST").GetCString(),
			kCivic.getSpecialistExtraCommerceArray());

	// doc: Specialist Yield
	setYieldChangeHelp(szHelpText, L"", L"",
			gDLL->getText("TXT_KEY_CIVIC_PER_SPECIALIST").GetCString(),
			kCivic.getSpecialistExtraYieldArray());

	// doc: specialist type extra yield
	CvWString szSpecialistTypeYieldsBySpecialist;
	YieldTypes eLastSpecialistYield = NO_YIELD;
	int iLastSpecialistYield = -1;
	int iSpecialistTypeExtraYield;

	bool bFormatByYield = true;

	FOR_EACH_ENUM(Specialist)
	{
		bFound = false;
		CvWString szYields;

		FOR_EACH_ENUM(Yield)
		{
			iSpecialistTypeExtraYield = kCivic.getSpecialistTypeExtraYield(eLoopSpecialist, eLoopYield);
			if (iSpecialistTypeExtraYield != 0)
			{
				if (bFound)
				{
					szYields.append(L", ");
					bFormatByYield = false;
				}

				szYields.append(CvWString::format(L"+%d%c",
						iSpecialistTypeExtraYield,
						GC.getInfo(eLoopYield).getChar()));
				bFound = true;

				if (bFormatByYield)
				{
					if (eLastSpecialistYield != NO_YIELD)
					{
						if (eLastSpecialistYield != eLoopYield || iLastSpecialistYield != iSpecialistTypeExtraYield)
						{
							bFormatByYield = false;
						}
					}

					eLastSpecialistYield = eLoopYield;
					iLastSpecialistYield = iSpecialistTypeExtraYield;
				}
			}
		}

		if (bFound)
		{
			CvWString szSpecialist;
			szSpecialist.Format(L"<link=literal>%s</link>",
					GC.getInfo(eLoopSpecialist).getDescription());

			szSpecialistTypeYieldsBySpecialist.append(NEWLINE);
			szSpecialistTypeYieldsBySpecialist.append(gDLL->getText("TXT_KEY_CIVIC_SPECIALIST_TYPE_EXTRA_YIELD",
					szYields.GetCString(),
					szSpecialist.GetCString()));
		}
	}

	if (bFormatByYield)
	{
		CvWString szYield;
		CvWString szSpecialists;

		FOR_EACH_ENUM(Yield)
		{
			bFound = false;

			FOR_EACH_ENUM(Specialist)
			{
				iSpecialistTypeExtraYield = kCivic.getSpecialistTypeExtraYield(eLoopSpecialist, eLoopYield);
				if (iSpecialistTypeExtraYield != 0)
				{
					if (bFound)
					{
						szSpecialists.append(L", ");
					}
					else
					{
						szYield.Format(L"+%d%c",
								iSpecialistTypeExtraYield,
								GC.getInfo(eLoopYield).getChar());
					}

					szSpecialists.append(CvWString::format(L"<link=literal>%s</link>",
							GC.getSpecialistInfo(eLoopSpecialist).getDescription()));
					bFound = true;
				}
			}

			if (bFound)
			{
				szHelpText.append(NEWLINE);
				szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_SPECIALIST_TYPE_EXTRA_YIELD",
						szYield.GetCString(),
						szSpecialists.GetCString()));
			}
		}
	}
	else
	{
		szHelpText.append(szSpecialistTypeYieldsBySpecialist);
	}

	// doc: Specialist Count
	iLast = 0;
	FOR_EACH_ENUM(Specialist)
	{
		if (kCivic.getSpecialistCount(eLoopSpecialist) != 0)
		{
			szFirstBuffer.Format(L"%s%s",
					NEWLINE,
					gDLL->getText("TXT_KEY_CIVIC_SPECIALIST_COUNT",
							kCivic.getSpecialistCount(iI)).c_str());
			CvWString szSpecialist;
			szSpecialist.Format(L"<link=literal>%s</link>",
					GC.getInfo(eLoopSpecialist).getDescription());
			setListHelp(szHelpText, szFirstBuffer, szSpecialist, L", ",
					(kCivic.getSpecialistCount(eLoopSpecialist) != iLast));
			iLast = kCivic.getSpecialistCount(eLoopSpecialist);
		}
	}

	// doc: Capture gold modifier
	if (kCivic.getCaptureGoldModifier() != 0)
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_CAPTURE_GOLD_MODIFIER",
				kCivic.getCaptureGoldModifier()));
	}

	// doc: Capital building production modifier
	if (kCivic.getCapitalBuildingProductionModifier() != 0)
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_CAPITAL_BUILDING_PRODUCTION_MODIFIER",
				kCivic.getCapitalBuildingProductionModifier()));
	}

	// doc: Occupation time change
	if (GC.getCivicInfo(eCivic).getOccupationTimeChange() != 0)
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_OCCUPATION_TIME_CHANGE",
				getTurns(kCivic.getOccupationTimeChange())));
	}

	//	Largest City Happiness
	if (kCivic.getLargestCityHappiness() != 0)
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_LARGEST_CITIES_HAPPINESS",
				/*	UNOFFICIAL_PATCH, Bugfix, 08/28/09, jdog5000:
					Use absolute value with unhappy face */
				abs(kCivic.getLargestCityHappiness()),
				kCivic.getLargestCityHappiness() > 0 ?
				gDLL->getSymbolID(HAPPY_CHAR) : gDLL->getSymbolID(UNHAPPY_CHAR),
				GC.getInfo(GC.getMap().getWorldSize()).getTargetNumCities()));
	}

	//	Improvement Yields
	// doc: list positive and negative effects separate
	FOR_EACH_ENUM(Yield)
	{
		int iLast = 0;
		FOR_EACH_ENUM(Improvement)
		{
			int const iYieldChange = kCivic.getImprovementYieldChanges(
					eLoopImprovement, eLoopYield);
			if (iYieldChange > 0)
			{
				szFirstBuffer.Format(L"%s%s", NEWLINE, gDLL->getText(
						"TXT_KEY_CIVIC_IMPROVEMENT_YIELD_CHANGE", iYieldChange,
						GC.getInfo(eLoopYield).getChar()).c_str());
				CvWString szImprovement;
				szImprovement.Format(L"<link=literal>%s</link>",
						GC.getInfo(eLoopImprovement).getDescription());
				setListHelp(szHelpText, szFirstBuffer, szImprovement, L", ",
						iLast, iYieldChange);
			}
		}

		iLast = 0;
		FOR_EACH_ENUM(Improvement)
		{
			int const iYieldChange = kCivic.getImprovementYieldChanges(
					eLoopImprovement, eLoopYield);
			if (iYieldChange < 0)
			{
				szFirstBuffer.Format(L"%s%s", NEWLINE, gDLL->getText(
						"TXT_KEY_CIVIC_IMPROVEMENT_YIELD_CHANGE", iYieldChange,
						GC.getInfo(eLoopYield).getChar()).c_str());
				CvWString szImprovement;
				szImprovement.Format(L"<link=literal>%s</link>",
						GC.getInfo(eLoopImprovement).getDescription());
				setListHelp(szHelpText, szFirstBuffer, szImprovement, L", ",
						iLast, iYieldChange);
			}
		}
	}

	// doc: free improvement upgrade
	if (kCivic.isFreeImprovementUpgrade())
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_FREE_IMPROVEMENT_UPGRADE"));
	}

	//	Building Happiness and Health
	FOR_EACH_ENUM2(BuildingClass, eBuildingClass)
	{
		int const iHappy = kCivic.getBuildingHappinessChanges(eBuildingClass);
		int const iHealth = kCivic.getBuildingHealthChanges(eBuildingClass);
		if (iHappy != 0)
		{
			if (bPlayerContext && NO_PLAYER != eActivePlayer)
			{
				BuildingTypes eBuilding = GC.getGame().
						getActiveCivilization()->getBuilding(eBuildingClass);
				if (NO_BUILDING != eBuilding)
				{
					szHelpText.append(NEWLINE);
					szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_BUILDING_HAPPINESS",
							/*	UNOFFICIAL_PATCH, Bugfix, 08/28/09, jdog5000:
								Use absolute value with unhappy face */
							abs(iHappy), iHappy > 0 ?
							gDLL->getSymbolID(HAPPY_CHAR) :
							gDLL->getSymbolID(UNHAPPY_CHAR),
							GC.getInfo(eBuilding).getTextKeyWide()));
				}
			}
			else
			{
				szHelpText.append(NEWLINE);
				szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_BUILDING_HAPPINESS",
						/*	UNOFFICIAL_PATCH (Bugfix, 08/28/09, jdog5000): START
							Use absolute value with unhappy face */
						abs(kCivic.getBuildingHappinessChanges(eBuildingClass)),
						(kCivic.getBuildingHappinessChanges(eBuildingClass) > 0) ?
						gDLL->getSymbolID(HAPPY_CHAR) : gDLL->getSymbolID(UNHAPPY_CHAR),
						 // UNOFFICIAL_PACTH: END
						GC.getInfo(eBuildingClass).getTextKeyWide()));
			}
		}
		if (iHealth != 0)
		{
			if (bPlayerContext && NO_PLAYER != eActivePlayer)
			{
				BuildingTypes eBuilding = GC.getGame().
						getActiveCivilization()->getBuilding(eBuildingClass);
				if (NO_BUILDING != eBuilding)
				{
					szHelpText.append(NEWLINE);
					szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_BUILDING_HAPPINESS",
							/*	UNOFFICIAL_PATCH (Bugfix, 08/28/09, jdog5000): START
								Use absolute value with unhealthy symbol */
							abs(iHealth), iHealth > 0 ?
							gDLL->getSymbolID(HEALTHY_CHAR) :
							gDLL->getSymbolID(UNHEALTHY_CHAR), // UNOFFICIAL_PACTH: END
							GC.getInfo(eBuilding).getTextKeyWide()));
				}
			}
			else
			{
				szHelpText.append(NEWLINE);
				szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_BUILDING_HAPPINESS",
						/*	UNOFFICIAL_PATCH (Bugfix, 08/28/09, jdog5000): START
							Use absolute value with unhealthy symbol */
						abs(iHealth), iHealth > 0 ?
						gDLL->getSymbolID(HEALTHY_CHAR) :
						gDLL->getSymbolID(UNHEALTHY_CHAR),
						GC.getInfo(eBuildingClass).getTextKeyWide()));
			}
		}
	}

	// doc: Building Productio
	int iDoubleModifierCount = 0;
	CvWStringBuffer szDoubleModifiers;
	szDoubleModifiers.append(gDLL->getText("TXT_KEY_CIVIC_BUILDING_DOUBLE_PRODUCTION_START"));

	FOR_EACH_ENUM(BuildingClass)
	{
		int iProductionModifier = kCivic.getBuildingProductionModifier(eLoopBuildingClass);

		if (iProductionModifier != 0)
		{
			if (bPlayerContext && NO_PLAYER != GC.getGameINLINE().getActivePlayer())
			{
				BuildingTypes eBuilding = GC.getCivilizationInfo(GC.getGameINLINE().getActiveCivilizationType()).getCivilizationBuildings(eLoopBuildingClass);
				if (NO_BUILDING != eBuilding)
				{
					if (iProductionModifier == 100)
					{
						if (iDoubleModifierCount > 0) szDoubleModifiers.append(",");
						szDoubleModifiers.append(" ");
						szDoubleModifiers.append(gDLL->getText("TXT_KEY_CIVIC_BUILDING_DOUBLE_PRODUCTION_BUILDING",
								GC.getInfo(eBuilding).getTextKeyWide()));
						iDoubleModifierCount++;
					}
					else
					{
						szHelpText.append(NEWLINE);
						szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_BUILDING_PRODUCTION_MODIFIER",
								iProductionModifier,
								GC.getInfo(eBuilding).getTextKeyWide()));
					}
				}
			}
			else
			{
				if (iProductionModifier == 100)
				{
					if (iDoubleModifierCount > 0) szDoubleModifiers.append(",");
					szDoubleModifiers.append(" ");
					szDoubleModifiers.append(gDLL->getText("TXT_KEY_CIVIC_BUILDING_DOUBLE_PRODUCTION_BUILDING",
								GC.getInfo(eLoopBuildingClass).getTextKeyWide()));
					iDoubleModifierCount++;
				}
				else
				{
					szHelpText.append(NEWLINE);
					szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_BUILDING_PRODUCTION_MODIFIER",
								iProductionModifier,
								GC.getInfo(eLoopBuildingClass).getTextKeyWide()));
				}
			}
		}
	}

	if (iDoubleModifierCount > 0)
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(szDoubleModifiers.getCString());
	}

	{
		//	Feature Happiness
		int iLast = 0;
		FOR_EACH_ENUM(Feature)
		{
			int const iHappyChange = kCivic.getFeatureHappinessChanges(eLoopFeature);
			if (iHappyChange != 0)
			{
				szFirstBuffer.Format(L"%s%s", NEWLINE, gDLL->getText(
						"TXT_KEY_CIVIC_FEATURE_HAPPINESS",
						/*	UNOFFICIAL_PATCH (Bugfix, 08/28/09, jdog5000): START
							Use absolute value with unhappy face */
						abs(iHappyChange), iHappyChange > 0 ?
						gDLL->getSymbolID(HAPPY_CHAR) :
						gDLL->getSymbolID(UNHAPPY_CHAR)).c_str());
						// UNOFFICIAL_PACTH: END
				CvWString szFeature;
				szFeature.Format(L"<link=literal>%s</link>",
						GC.getInfo(eLoopFeature).getDescription());
				setListHelp(szHelpText, szFirstBuffer, szFeature, L", ",
						iLast, iHappyChange);
			}
		}
	}
	FOR_EACH_ENUM(Hurry)
	{
		if (kCivic.isHurry(eLoopHurry))
		{
			szHelpText.append(CvWString::format(L"%s%c%s", NEWLINE,
					gDLL->getSymbolID(BULLET_CHAR), GC.getInfo(eLoopHurry).getDescription()));
		}
	}

	// doc: hurrying units with gold also allows to bribe barbarians
	if (kCivic.isHurry(HURRY_GOLD_UNITS))
	{
		szHelpText.append(gDLL->getText("TXT_KEY_BRIBE_UNITS_EFFECT"));
	}

	// <K-Mod>
	float fInflationFactor = (!bPlayerContext ? 1.0f :
			(100 + GET_PLAYER(eActivePlayer).calculateInflationRate()) / 100.0f); // </K-Mod>
 	//	Gold cost per unit
	//	Gold cost per unit
	if (kCivic.getGoldPerUnit() != 0)
	{
		/* szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_SUPPORT_COSTS", (kCivic.getGoldPerUnit() > 0), GC.getInfo(COMMERCE_GOLD).getChar())); */
		// K-Mod
		szHelpText.append(CvWString::format(L"\n%c%+.2f%c %s",
				gDLL->getSymbolID(BULLET_CHAR), (float)
				kCivic.getGoldPerUnit()*fInflationFactor/100,
				GC.getInfo(COMMERCE_GOLD).getChar(),
				gDLL->getText("TXT_KEY_CIVIC_SUPPORT_COSTS").GetCString()));
		// K-Mod end
	}
	int iGoldPerMilitaryUnit = kCivic.getGoldPerMilitaryUnit(); // advc
	//	Gold cost per military unit
	if (iGoldPerMilitaryUnit != 0)
	{	// advc.912b:
		bool bFractional = (iGoldPerMilitaryUnit % 100 != 0);
		/* szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_MILITARY_SUPPORT_COSTS", (kCivic.getGoldPerMilitaryUnit() > 0), GC.getInfo(COMMERCE_GOLD).getChar())); */
		// K-Mod
		szHelpText.append(
				/*CvWString::format(L"\n%c%+.2f%c %s",
				gDLL->getSymbolID(BULLET_CHAR), (float)kCivic.
				getGoldPerMilitaryUnit()*fInflationFactor/100,*/
				// <advc.912b> Don't show inflation now that the total is shown
				bFractional ?
				CvWString::format(L"\n%c%+.2f%c %s",
				gDLL->getSymbolID(BULLET_CHAR), 0.01f * iGoldPerMilitaryUnit,
				// </advc.912b>
				GC.getInfo(COMMERCE_GOLD).getChar(),
				gDLL->getText("TXT_KEY_CIVIC_MILITARY_SUPPORT_COSTS").GetCString())
		// K-Mod end
				// <advc.912b>
				: CvWString::format(L"\n%c%+d%c %s", gDLL->getSymbolID(BULLET_CHAR),
				fmath::round(0.01 * iGoldPerMilitaryUnit), // </advc.912b>
				GC.getInfo(COMMERCE_GOLD).getChar(),
				gDLL->getText("TXT_KEY_CIVIC_MILITARY_SUPPORT_COSTS").GetCString()));
		// <advc.912b>
		if (bPlayerContext)
		{
			int iFreeUnits, iFreeMilitaryUnits, iPaidUnits, iPaidMilitaryUnits,
					iMilitaryCost, iBaseUnitCost, iExtraCost;
			GET_PLAYER(eActivePlayer).calculateUnitCost(
					iFreeUnits, iFreeMilitaryUnits, iPaidUnits, iPaidMilitaryUnits,
					iBaseUnitCost, iMilitaryCost, iExtraCost);
			float fCurrentTotal = 0.01f * fInflationFactor * iPaidMilitaryUnits *
					iGoldPerMilitaryUnit;
			szHelpText.append(CvWString::format(L"\n(%+.1f%c %s)",
					fCurrentTotal, GC.getInfo(COMMERCE_GOLD).getChar(),
					gDLL->getText("TXT_KEY_MISC_CURRENTLY").GetCString()));
		} // </advc.912b>
	}

	// doc: cannot use slaves
	if (kCivic.isNoSlavery())
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_CANNOT_USE_SLAVES"));
	}

	// doc: can use slaves in colonies
	if (kCivic.isColonialSlavery())
	{
		szHelpText.append(NEWLINE);
		szHelpText.append(gDLL->getText("TXT_KEY_CIVIC_CAN_CAPTURE_SLAVES"));
	}

	if (!CvWString(kCivic.getHelp()).empty())
		szHelpText.append(CvWString::format(L"%s%s", NEWLINE, kCivic.getHelp()).c_str());
}


void CvGameTextMgr::setTechHelp(CvWStringBuffer &szBuffer, TechTypes eTech, bool bCivilopediaText,
	bool bPlayerContext, bool bStrategyText, bool bTreeInfo, TechTypes eFromTech)
{
	// BULL - Trade Denial - start
	setTechTradeHelp(szBuffer, eTech, NO_PLAYER, bCivilopediaText, bPlayerContext,
			bStrategyText, bTreeInfo, eFromTech);
}


void CvGameTextMgr::setTechTradeHelp(CvWStringBuffer &szBuffer, TechTypes eTech, PlayerTypes eTradePlayer,
	bool bCivilopediaText, bool bPlayerContext, bool bStrategyText, bool bTreeInfo, TechTypes eFromTech)
// BULL - Trade Denial - end
{
	PROFILE_FUNC();

	CvWString szTempBuffer;
	CvGame const& kGame = GC.getGame(); // advc

	// show debug info if cheat level > 0 and alt down
	bool const bAlt = GC.altKey();
	if (bAlt && //(gDLL->getChtLvl() > 0))
		kGame.isDebugMode()) // advc.135c
	{
		szBuffer.clear();
		for (PlayerIter<ALIVE> it; it.hasNext(); ++it)
		{
			CvPlayer const& kPlayer = *it;
			CvTeam const& kTeam = GET_TEAM(kPlayer.getTeam());
			szTempBuffer.Format(L"%s: ", kPlayer.getName());
			szBuffer.append(szTempBuffer);

			TechTypes ePlayerTech = kPlayer.getCurrentResearch();
			if(ePlayerTech == NO_TECH)
				szTempBuffer.Format(L"-\n");
			else
			{
				szTempBuffer.Format(L"%s (%d->%dt)(%d/%d)\n",
						GC.getInfo(ePlayerTech).getDescription(),
						kPlayer.calculateResearchRate(ePlayerTech),
						kPlayer.getResearchTurnsLeft(ePlayerTech, true),
						kTeam.getResearchProgress(ePlayerTech),
						kTeam.getResearchCost(ePlayerTech));
			}
			szBuffer.append(szTempBuffer);
			szBuffer.append(NEWLINE);
		}
		// <advc.007> (Unrelated to the info above)
		szTempBuffer.Format(L"tech id = %d", eTech);
		szBuffer.append(szTempBuffer); // </advc.007>
		return;
	}


	if (eTech == NO_TECH)
		return;

	//	Tech Name
	if (!bCivilopediaText && (!bTreeInfo || (NO_TECH == eFromTech)))
	{
		szTempBuffer.Format( SETCOLR L"%s" ENDCOLR, TEXT_COLOR("COLOR_TECH_TEXT"),
				GC.getInfo(eTech).getDescription());
		szBuffer.append(szTempBuffer);
	}

	PlayerTypes const eActivePlayer = getActivePlayer();
	TeamTypes const eActiveTeam = (eActivePlayer == NO_PLAYER ?
			NO_TEAM : TEAMID(eActivePlayer));

	FAssert(eActivePlayer != NO_PLAYER || !bPlayerContext);

	if (bTreeInfo && NO_TECH != eFromTech)
		buildTechTreeString(szBuffer, eTech, bPlayerContext, eFromTech);

	//	Obsolete Buildings
	FOR_EACH_ENUM(BuildingClass)
	{
		if (!bPlayerContext || (GET_PLAYER(eActivePlayer).
			getBuildingClassCount(eLoopBuildingClass) > 0))
		{
			BuildingTypes eLoopBuilding;
			if (eActivePlayer != NO_PLAYER)
				eLoopBuilding = kGame.getActiveCivilization()->getBuilding(eLoopBuildingClass);
			else eLoopBuilding = GC.getInfo(eLoopBuildingClass).getDefaultBuilding();
			if (eLoopBuilding != NO_BUILDING)
			{
				//	Obsolete Buildings Check...
				if (GC.getInfo(eLoopBuilding).getObsoleteTech() == eTech)
					buildObsoleteString(szBuffer, eLoopBuilding, true);
			}
		}
	}

	//	Obsolete Bonuses
	FOR_EACH_ENUM(Bonus)
	{
		if (GC.getInfo(eLoopBonus).getTechObsolete() == eTech)
			buildObsoleteBonusString(szBuffer, eLoopBonus, true);
	}

	FOR_EACH_ENUM(SpecialBuilding)
	{
		if (GC.getInfo(eLoopSpecialBuilding).getObsoleteTech() == eTech)
			buildObsoleteSpecialString(szBuffer, eLoopSpecialBuilding, true);
	}

	//	Route movement change...
	buildMoveString(szBuffer, eTech, true, bPlayerContext);

	//	Creates a free unit...
	buildFreeUnitString(szBuffer, eTech, true, bPlayerContext);

	//	Increases feature production...
	buildFeatureProductionString(szBuffer, eTech, true, bPlayerContext);

	//	Increases worker build rate...
	buildWorkerRateString(szBuffer, eTech, true, bPlayerContext);

	//	Trade Routed per city change...
	buildTradeRouteString(szBuffer, eTech, true, bPlayerContext);

	//	Health increase...
	buildHealthRateString(szBuffer, eTech, true, bPlayerContext);

	//	Happiness increase...
	buildHappinessRateString(szBuffer, eTech, true, bPlayerContext);

	//	Free Techs...
	buildFreeTechString(szBuffer, eTech, true, bPlayerContext);

	//	Line of Sight Bonus across water...
	buildLOSString(szBuffer, eTech, true, bPlayerContext);

	//	Centers world map...
	buildMapCenterString(szBuffer, eTech, true, bPlayerContext);

	//	Reveals World Map...
	buildMapRevealString(szBuffer, eTech, true);

	//	Enables map trading...
	buildMapTradeString(szBuffer, eTech, true, bPlayerContext);

	//	Enables tech trading...
	buildTechTradeString(szBuffer, eTech, true, bPlayerContext);

	//	Enables gold trading...
	buildGoldTradeString(szBuffer, eTech, true, bPlayerContext);

	//	Enables open borders...
	buildOpenBordersString(szBuffer, eTech, true, bPlayerContext);

	//	Enables defensive pacts...
	buildDefensivePactString(szBuffer, eTech, true, bPlayerContext);

	//	Enables permanent alliances...
	buildPermanentAllianceString(szBuffer, eTech, true, bPlayerContext);

	//	Enables bridge building...
	buildBridgeString(szBuffer, eTech, true, bPlayerContext);

	//	Can spread irrigation...
	buildIrrigationString(szBuffer, eTech, true, bPlayerContext);

	//	Ignore irrigation...
	buildIgnoreIrrigationString(szBuffer, eTech, true, bPlayerContext);

	//	Coastal work...
	buildWaterWorkString(szBuffer, eTech, true, bPlayerContext);

	//	Enables permanent alliances...
	buildVassalStateString(szBuffer, eTech, true, bPlayerContext);

	//	Build farm, irrigation, etc...
	FOR_EACH_ENUM(Build)
	{
		// doc: exclude graphical only builds
		if (!GC.getInfo(eLoopBuild).isGraphicalOnly())
			buildImprovementString(szBuffer, eTech, eLoopBuild, true, bPlayerContext);
	}

	//	Extra moves for certain domains...
	FOR_EACH_ENUM(Domain)
	{
		buildDomainExtraMovesString(szBuffer, eTech, eLoopDomain, true, bPlayerContext);
	}

	//	K-Mod. Global commerce modifiers
	setCommerceChangeHelp(szBuffer, L"", L"",
			gDLL->getText("TXT_KEY_CIVIC_IN_ALL_CITIES").GetCString(),
			GC.getInfo(eTech).getCommerceModifierArray(), true);

	//	K-Mod. Extra specialist commerce
	setCommerceChangeHelp(szBuffer, L"", L"",
			gDLL->getText("TXT_KEY_CIVIC_PER_SPECIALIST").GetCString(),
			GC.getInfo(eTech).getSpecialistExtraCommerceArray());

	//	Adjusting culture, science, etc
	FOR_EACH_ENUM(Commerce)
	{
		buildAdjustString(szBuffer, eTech, eLoopCommerce, true, bPlayerContext);
	}

	//	Enabling trade routes on water...?
	FOR_EACH_ENUM(Terrain)
	{
		buildTerrainTradeString(szBuffer, eTech, eLoopTerrain, true, bPlayerContext);
	}

	buildRiverTradeString(szBuffer, eTech, true, bPlayerContext);

	//	Special Buildings
	FOR_EACH_ENUM(SpecialBuilding)
	{
		buildSpecialBuildingString(szBuffer, eTech, eLoopSpecialBuilding, true, bPlayerContext);
	}

	//	Build farm, mine, etc...
	FOR_EACH_ENUM(Improvement)
	{
		buildYieldChangeString(szBuffer, eTech, eLoopImprovement, true, bPlayerContext);
	}
	{
		bool bFirst = true;
		FOR_EACH_ENUM(Bonus)
		{
			bFirst = buildBonusRevealString(szBuffer, eTech, eLoopBonus,
					bFirst, true, bPlayerContext);
		}
	}
	{
		// doc: bonus trade
		bool bFirst = true;
		FOR_EACH_ENUM(Bonus)
		{
			bFirst = buildBonusTradeString(szBuffer, eTech, eLoopBonus,
					bFirst, true, bPlayerContext);
		}
	}
	{
		bool bFirst = true;
		FOR_EACH_ENUM(Civic)
		{
			bFirst = buildCivicRevealString(szBuffer, eTech, eLoopCivic,
					bFirst, true, bPlayerContext);
		}
	}
	if (!bCivilopediaText)
	{
		CvWString szFirstBuffer;
		{
			bool bFirst = true;
			FOR_EACH_ENUM(UnitClass)
			{
				if (bPlayerContext &&
					GET_PLAYER(eActivePlayer).isProductionMaxedUnitClass(eLoopUnitClass))
				{
					continue;
				}
				UnitTypes eLoopUnit;
				if (eActivePlayer != NO_PLAYER)
					eLoopUnit = kGame.getActiveCivilization()->getUnit(eLoopUnitClass);
				else eLoopUnit = GC.getInfo(eLoopUnitClass).getDefaultUnit();
				if (eLoopUnit == NO_UNIT)
					continue;
				if (bPlayerContext && GET_PLAYER(eActivePlayer).canTrain(eLoopUnit))
					continue;
				if (GC.getInfo(eLoopUnit).getPrereqAndTech() == eTech)
				{
					szFirstBuffer.Format(L"%s%s", NEWLINE,
							gDLL->getText("TXT_KEY_TECH_CAN_TRAIN").c_str());
					szTempBuffer.Format( SETCOLR L"%s" ENDCOLR ,
							TEXT_COLOR("COLOR_UNIT_TEXT"),
							GC.getInfo(eLoopUnit).getDescription());
					setListHelp(szBuffer, szFirstBuffer, szTempBuffer, L", ", bFirst);
				}
				else
				{
					for (int i = 0; i < GC.getInfo(eLoopUnit).getNumPrereqAndTechs(); i++)
					{
						if (GC.getInfo(eLoopUnit).getPrereqAndTechs(i) == eTech)
						{
							szFirstBuffer.Format(L"%s%s", NEWLINE,
									gDLL->getText("TXT_KEY_TECH_CAN_TRAIN").c_str());
							szTempBuffer.Format( SETCOLR L"%s" ENDCOLR,
									TEXT_COLOR("COLOR_UNIT_TEXT"),
									GC.getInfo(eLoopUnit).getDescription());
							setListHelp(szBuffer, szFirstBuffer, szTempBuffer, L", ", bFirst);
							break;
						}
					}
				}
			}
		}
		{
			bool bFirst = true;
			FOR_EACH_ENUM(BuildingClass)
			{
				if (bPlayerContext && GET_PLAYER(eActivePlayer).
					isProductionMaxedBuildingClass(eLoopBuildingClass))
				{
					continue;
				}
				BuildingTypes eLoopBuilding = (eActivePlayer != NO_PLAYER ?
						kGame.getActiveCivilization()->getBuilding(eLoopBuildingClass) :
						GC.getInfo(eLoopBuildingClass).getDefaultBuilding());
				if (eLoopBuilding != NO_BUILDING)
				{
					if (!bPlayerContext ||
						!GET_PLAYER(eActivePlayer).canConstruct(eLoopBuilding, false, true))
					{
						if (GC.getInfo(eLoopBuilding).getPrereqAndTech() == eTech)
						{
							szFirstBuffer.Format(L"%s%s", NEWLINE,
									gDLL->getText("TXT_KEY_TECH_CAN_CONSTRUCT").c_str());
							szTempBuffer.Format( SETCOLR L"<link=literal>%s</link>" ENDCOLR,
									TEXT_COLOR("COLOR_BUILDING_TEXT"),
									GC.getInfo(eLoopBuilding).getDescription());
							setListHelp(szBuffer, szFirstBuffer, szTempBuffer, L", ", bFirst);
						}
						else
						{
							for (int i = 0; i < GC.getInfo(eLoopBuilding).
								getNumPrereqAndTechs(); i++)
							{
								if (GC.getInfo(eLoopBuilding).getPrereqAndTechs(i) != eTech)
									continue;
								szFirstBuffer.Format(L"%s%s", NEWLINE,
										gDLL->getText("TXT_KEY_TECH_CAN_CONSTRUCT").c_str());
								szTempBuffer.Format(
										SETCOLR L"<link=literal>%s</link>" ENDCOLR,
										TEXT_COLOR("COLOR_BUILDING_TEXT"),
										GC.getInfo(eLoopBuilding).getDescription());
								setListHelp(szBuffer, szFirstBuffer, szTempBuffer, L", ", bFirst);
								break;
							}
						}
					}
				}
			}
		}
		{
			bool bFirst = true;
			FOR_EACH_ENUM(Project)
			{
				if (!bPlayerContext ||
					!GET_PLAYER(eActivePlayer).isProductionMaxedProject(eLoopProject))
				{
					if (!bPlayerContext ||
						!GET_PLAYER(eActivePlayer).canCreate(eLoopProject, false, true))
					{
						if (GC.getInfo(eLoopProject).getTechPrereq() == eTech)
						{
							szFirstBuffer.Format(L"%s%s", NEWLINE,
									gDLL->getText("TXT_KEY_TECH_CAN_CREATE").c_str());
							szTempBuffer.Format( SETCOLR L"%s" ENDCOLR,
									TEXT_COLOR("COLOR_PROJECT_TEXT"),
									GC.getInfo(eLoopProject).getDescription());
							setListHelp(szBuffer, szFirstBuffer, szTempBuffer, L", ", bFirst);
						}
					}
				}
			}
		}
	}
	{
		bool bFirst = true;
		FOR_EACH_ENUM(Process)
		{
			bFirst = buildProcessInfoString(szBuffer, eTech, eLoopProcess,
					bFirst, true, bPlayerContext);
		}
	}
	{
		bool bFirst = true;
		FOR_EACH_ENUM(Religion)
		{
			if (!bPlayerContext || !kGame.isReligionSlotTaken(eLoopReligion))
			{
				bFirst = buildFoundReligionString(szBuffer, eTech, eLoopReligion, bFirst,
						true, bPlayerContext);
			}
		}
	}
	{
		bool bFirst = true;
		FOR_EACH_ENUM(Corporation)
		{
			if (!bPlayerContext || !kGame.isCorporationFounded(eLoopCorporation))
			{
				bFirst = buildFoundCorporationString(szBuffer, eTech, eLoopCorporation, bFirst,
						true, bPlayerContext);
			}
		}
	}
	{
		bool bFirst = true;
		FOR_EACH_ENUM(Promotion)
		{
			bFirst = buildPromotionString(szBuffer, eTech, eLoopPromotion,
					bFirst, true, bPlayerContext);
		}
	}
	// advc.500c: (Pretty minor effect, place it far down the list.)
	buildNoFearForSafetyString(szBuffer, eTech, true, bPlayerContext);
	/*	advc.910: Moved above SingleLineTechTreeString - so that the custom help text
		(unused in BtS/AdvCiv btw) can't end up in the middle of cost-related info. */
	if (!CvWString(GC.getInfo(eTech).getHelp()).empty())
	{
		szBuffer.append(CvWString::format(L"%s%s", NEWLINE,
				GC.getInfo(eTech).getHelp()).c_str());
	}

	if (bTreeInfo && eFromTech == NO_TECH)
		buildSingleLineTechTreeString(szBuffer, eTech, bPlayerContext);

	bool const bDiplo = gDLL->isDiplomacy(); // advc.004x

	if (!bCivilopediaText)
	{
		if (eActivePlayer == NO_PLAYER)
		{
			szTempBuffer.Format(L"\n%d%c",
					GC.getInfo(eTech).getResearchCost(),
					GC.getInfo(COMMERCE_RESEARCH).getChar());
			szBuffer.append(szTempBuffer);
		}
		else if (GET_TEAM(eActiveTeam).isHasTech(eTech))
		{
			szTempBuffer.Format(L"\n%d%c",
					GET_TEAM(eActiveTeam).getResearchCost(eTech),
					GC.getInfo(COMMERCE_RESEARCH).getChar());
			szBuffer.append(szTempBuffer);
		}
		else
		{
			szBuffer.append(NEWLINE);
			// <advc.004x> (based on BtS code)
			bool bShowTurns = GET_PLAYER(eActivePlayer).isResearch();
			int iTurnsLeft = (!bShowTurns ? -1 :
					/*	Note: bTreeInfo is _false_ when hovering on the tech tree.
						The Shift check is for queuing up techs; don't know
						what the Ctrl check is for. */
					GET_PLAYER(eActivePlayer).getResearchTurnsLeft(eTech,
					//(!bTreeInfo && (GC.ctrlKey() || !GC.shiftKey()))
					/*	I think overflow should be included for researchable tech
						unless trading or queuing */
					(!bDiplo && (bTreeInfo || !GC.shiftKey())) &&
					GET_PLAYER(eActivePlayer).canResearch(eTech)));
			if (iTurnsLeft < 0)
				bShowTurns = false;
			if (bDiplo) // To set the cost apart from trade denial text
				szBuffer.append(CvWString::format(L"%c", gDLL->getSymbolID(BULLET_CHAR)));
			if (bShowTurns)
			{
				szBuffer.append(gDLL->getText("TXT_KEY_TECH_NUM_TURNS", iTurnsLeft));
				szBuffer.append(L' '); // Append this separately
			}
			// </advc.004x>
			szTempBuffer.Format(L"%s%d/%d %c%s",
					bShowTurns ? L"(" : L"", // advc.004x
					GET_TEAM(eActiveTeam).getResearchProgress(eTech),
					GET_TEAM(eActiveTeam).getResearchCost(eTech),
					GC.getInfo(COMMERCE_RESEARCH).getChar(),
					bShowTurns ? L")" : L""); // advc.004x
			szBuffer.append(szTempBuffer);

			// doc: display tech modifiers
			// TODO: refactor
			if (GET_TEAM(eActiveTeam).getResearchCost(eTech) != GET_TEAM(eActiveTeam).getResearchCost(eTech, false))
			{
				int iCost = GET_TEAM(eActiveTeam).getResearchCost(eTech, false);
				int iCostChange;

				szBuffer.append(NEWLINE);
				szBuffer.append(" ");
				szBuffer.append(gDLL->getText("TXT_KEY_TECH_BASE_COST"));
				szTempBuffer.Format(L" %d %c", iCost, GC.getCommerceInfo(COMMERCE_RESEARCH).getChar());
				szBuffer.append(szTempBuffer);

				// doc: population modifier
				if (GET_TEAM(eActiveTeam).getPopulationResearchModifier() != 0)
				{
					iCostChange = iCost * GET_TEAM(eActiveTeam).getPopulationResearchModifier();
					iCostChange /= 100;

					szBuffer.append(NEWLINE);
					szBuffer.append(" ");
					szBuffer.append(gDLL->getText("TXT_KEY_TECH_EMPIRE_SIZE"));
					szTempBuffer.Format(L" %s%d %c", (iCostChange > 0) ? "+" : "", iCostChange, GC.getCommerceInfo(COMMERCE_RESEARCH).getChar());
					szBuffer.append(szTempBuffer);
				}

				// doc: tech difference modifier
				if (GET_TEAM(eActiveTeam).getTechDifferenceModifier() != 0)
				{
					iCostChange = iCost * GET_TEAM(eActiveTeam).getTechDifferenceModifier();
					iCostChange /= 100;

					szBuffer.append(NEWLINE);
					szBuffer.append(" ");
					szBuffer.append(gDLL->getText("TXT_KEY_TECH_DIFFERENCE"));
					szTempBuffer.Format(L" %s%d %c", (iCostChange > 0) ? "+" : "", iCostChange, GC.getCommerceInfo(COMMERCE_RESEARCH).getChar());
					szBuffer.append(szTempBuffer);
				}

				// doc: spread research modifier
				if (GET_TEAM(eActiveTeam).getSpreadResearchModifier(eTech) != 0)
				{
					iCostChange = iCost * GET_TEAM(eActiveTeam).getSpreadResearchModifier(eTech);
					iCostChange /= 100;

					szBuffer.append(NEWLINE);
					szBuffer.append(" ");
					szBuffer.append(gDLL->getText("TXT_KEY_TECH_SPREAD_MODIFIER"));
					szTempBuffer.Format(L" %s%d %c", (iCostChange > 0) ? "+" : "", iCostChange, GC.getCommerceInfo(COMMERCE_RESEARCH).getChar());
					szBuffer.append(szTempBuffer);
				}

				// doc: turn research modifier
				if (GET_TEAM(eActiveTeam).getTurnResearchModifier() != 0)
				{
					iCostChange = iCost * GET_TEAM(eActiveTeam).getTurnResearchModifier();
					iCostChange /= 100;

					szBuffer.append(NEWLINE);
					szBuffer.append(" ");
					szBuffer.append(gDLL->getText("TXT_KEY_TECH_SPAWN_MODIFIER"));
					szTempBuffer.Format(L" %s%d %c", (iCostChange > 0) ? "+" : "", iCostChange, GC.getCommerceInfo(COMMERCE_RESEARCH).getChar());
					szBuffer.append(szTempBuffer);
				}

				if (GET_TEAM(eActiveTeam).getModernizationResearchModifier(eTech) != 0)
				{
					iCostChange = iCost * GET_TEAM(eActiveTeam).getModernizationResearchModifier(eTech);
					iCostChange /= 100;

					szBuffer.append(NEWLINE);
					szBuffer.append(" ");
					szBuffer.append(gDLL->getText("TXT_KEY_TECH_MODERNIZATION_MODIFIER"));
					szTempBuffer.Format(L" %s%d %c", (iCostChange > 0) ? "+" : "", iCostChange, GC.getCommerceInfo(COMMERCE_RESEARCH).getChar());
					szBuffer.append(szTempBuffer);
				}
			}

			// <advc.910>
			if (!bDiplo && bShowTurns && bPlayerContext)
				setResearchModifierHelp(szBuffer, eTech); // </advc.910>
		}
	}

	if (eActivePlayer != NO_PLAYER &&
		/*  advc.004: Don't show this when inspecting foreign research on the
			scoreboard, nor in Civilopedia. */
		bPlayerContext)
	{
		if (GET_PLAYER(eActivePlayer).canResearch(eTech))
		{	// advc.004a: Commented out // doc: restored
			FOR_EACH_ENUM(Unit)
			{
				CvUnitInfo& kUnit = GC.getInfo(eLoopUnit);
				if (kUnit.getBaseDiscover() > 0 || kUnit.getDiscoverMultiplier() > 0)
				{
					// doc: exclude graphical only units
					if (::getDiscoveryTech(eLoopUnit, eActivePlayer) == eTech && !kUnit.isGraphicalOnly())
					{
						szBuffer.append(NEWLINE);
						szBuffer.append(gDLL->getText("TXT_KEY_TECH_GREAT_PERSON_DISCOVER", kUnit.getTextKeyWide()));
					}
				}
			}
			if (GET_PLAYER(eActivePlayer).getCurrentEra() < GC.getInfo(eTech).getEra())
			{
				szBuffer.append(NEWLINE);
				/*	<advc.004x> Moved out of the text key. The era advance comes more down to
					the overall game state than to the specific eTech. Shouldn't be a
					bulleted item. (But place a bullet all the same during diplo in order
					to set it apart from the denial text.) */
				if (bDiplo)
					szBuffer.append(CvWString::format(L"%c", gDLL->getSymbolID(BULLET_CHAR)));
				// </advc.004x>
				szBuffer.append(gDLL->getText("TXT_KEY_TECH_ERA_ADVANCE",
						GC.getInfo(GC.getInfo(eTech).getEra()).getTextKeyWide()));
			}
		}
	}
	// BULL - Trade Denial - start (advc.073: refactored; BUGOption check removed)
	if (eTradePlayer != NO_PLAYER && eActivePlayer != NO_PLAYER)
	{
		TradeData item(TRADE_TECHNOLOGIES, eTech);
		if (GET_PLAYER(eTradePlayer).canTradeItem(eActivePlayer, item, false))
		{
			DenialTypes eDenial = GET_PLAYER(eTradePlayer).getTradeDenial(
					eActivePlayer, item);
			// <advc.073>
			if (eDenial == NO_DENIAL)
			{
				if(!GET_PLAYER(eTradePlayer).isHuman() && !GET_PLAYER(eTradePlayer).
						AI_isWillingToTalk(eActivePlayer, true))
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_MISC_REFUSES_TO_TALK"));
				}
			} // </advc.073>
			else
			{
				szTempBuffer.Format(SETCOLR L"%s" ENDCOLR,
						TEXT_COLOR("COLOR_NEGATIVE_TEXT"),
						GC.getInfo(eDenial).getDescription());
				szBuffer.append(NEWLINE);
				szBuffer.append(szTempBuffer);
			}
		}
	} // BULL - Trade Denial - end

	// rfc: disable
	/*if (bStrategyText)
	{
		if (!CvWString(GC.getInfo(eTech).getStrategy()).empty())
		{
			if ((eActivePlayer == NO_PLAYER) || GET_PLAYER(eActivePlayer).isOption(PLAYEROPTION_ADVISOR_HELP))
			{
				szBuffer.append(SEPARATOR);
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_SIDS_TIPS"));
				szBuffer.append(L'\"');
				szBuffer.append(GC.getInfo(eTech).getStrategy());
				szBuffer.append(L'\"');
			}
		}
	}*/
}

// advc.004a:
void CvGameTextMgr::setDiscoverPathHelp(CvWStringBuffer& szBuffer, UnitTypes eUnit)
{
	szBuffer.append(NEWLINE);
	CvPlayer const& kPlayer = GET_PLAYER(getActivePlayer());
	/*	Could have ported the code in BUG TechPrefs.py, but it's unnecessarily
		complicated for what I'm trying to do. Use getDiscoveryTech and,
		in between calls, pretend that the previous tech has already been discovered. */
	TechTypes eCurrentDiscover = kPlayer.getDiscoveryTech(eUnit);
	if (eCurrentDiscover == NO_TECH || eUnit == NO_UNIT)
		return;
	FlavorTypes eGPFlavor = NO_FLAVOR;
	int iMaxFlavor = -1;
	CvUnitInfo const& kUnit = GC.getInfo(eUnit);
	FOR_EACH_ENUM(Flavor)
	{
		int iFlavor = kUnit.getFlavorValue(eLoopFlavor);
		if (iFlavor > iMaxFlavor)
		{
			eGPFlavor = eLoopFlavor;
			iMaxFlavor = iFlavor;
		}
	}
	CvString szFlavor;
	switch (eGPFlavor)
	{
		case FLAVOR_SCIENCE: szFlavor = "SCIENCE"; break;
		case FLAVOR_MILITARY: szFlavor = "MILITARY"; break;
		case FLAVOR_RELIGION: szFlavor = "RELIGION"; break;
		case FLAVOR_PRODUCTION: szFlavor = "PRODUCTION"; break;
		case FLAVOR_GOLD: szFlavor = "GOLD"; break;
		case FLAVOR_CULTURE: szFlavor = "CULTURE"; break;
		case FLAVOR_GROWTH: szFlavor = "GROWTH"; break;
		default: FAssert(false); return;
	}
	szBuffer.append(gDLL->getText("TXT_KEY_MISSION_DISCOVER_HELP1"));
	szBuffer.append(L" ");
	CvString szFlavorKey("TXT_KEY_FLAVOR_" + szFlavor + "_TECH");
	szBuffer.append(gDLL->getText(szFlavorKey));
	szBuffer.append(L". ");
	CvTeam& kTeam = GET_TEAM(kPlayer.getTeam());
	/*	The same discovery could be enabled by multiple currently researchable techs.
		The map lists the alt. reqs for each target tech. */
	ArrayEnumMap2D<TechTypes,TechTypes,bool> discoverMap;
	FOR_EACH_ENUM2(Tech, eResearchOption)
	{
		if (!kPlayer.canResearch(eResearchOption))
			continue;
		/*	(Would not be so difficult to do this cleanly - pass eResearchOption
			to CvPlayer::canResearch via CvPlayer::getDiscoveryTech; tbd.?) */
		kTeam.setHasTechTemporarily(eResearchOption, true);
		TechTypes eNextDiscover = kPlayer.getDiscoveryTech(eUnit);
		kTeam.setHasTechTemporarily(eResearchOption, false);
		if (eNextDiscover != eCurrentDiscover && eNextDiscover != NO_TECH)
			discoverMap.set(eNextDiscover, eResearchOption, true);
	}
	int iSize = discoverMap.numNonDefault();
	if (iSize <= 0)
		return;
	szBuffer.append(gDLL->getText("TXT_KEY_MISSION_DISCOVER_HELP2"));
	szBuffer.append(L" ");
	if (iSize == 1)
		szBuffer.append(gDLL->getText(szFlavorKey));
	else
	{
		CvString szPluralKey = "TXT_KEY_FLAVOR_" + szFlavor + "_PLURAL";
		szBuffer.append(gDLL->getText(szPluralKey));
	}
	szBuffer.append(L": ");
	bool bFirst = true;
	FOR_EACH_ENUM2(Tech, eNextDiscover)
	{
		if (discoverMap.get(eNextDiscover) == NULL)
			continue;
		if (bFirst)
			bFirst = false;
		else szBuffer.append(L", ");
		CvTechInfo const& kNextDiscover = GC.getInfo(eNextDiscover);
		CvWString szTemp;
		szTemp.Format(SETCOLR L"%s" ENDCOLR, TEXT_COLOR("COLOR_TECH_TEXT"),
				kNextDiscover.getDescription());
		szBuffer.append(szTemp);
		szBuffer.append(L" (");
		szBuffer.append(gDLL->getText("TXT_KEY_MISSION_DISCOVER_REQ"));
		szBuffer.append(L" ");
		bool bFirstInner = true;
		FOR_EACH_ENUM2(Tech, eReqTech)
		{
			if (!discoverMap.get(eNextDiscover, eReqTech))
				continue;
			if (bFirstInner)
				bFirstInner = false;
			else
			{
				szBuffer.append(L" ");
				szBuffer.append(gDLL->getText("TXT_KEY_MISSION_DISCOVER_OR"));
				szBuffer.append(L" ");
			}
			szTemp.Format(SETCOLR L"%s" ENDCOLR, TEXT_COLOR("COLOR_TECH_TEXT"),
					GC.getInfo(eReqTech).getDescription());
			szBuffer.append(szTemp);
		}
		szBuffer.append(L")");
	}
	szBuffer.append(L".");
}

// advc.ctr:
void CvGameTextMgr::setCityTradeHelp(CvWStringBuffer& szBuffer, CvCity const& kCity,
	PlayerTypes eWhoTo, bool bListMore, bool bReason)
{
	PlayerTypes eActivePlayer = getActivePlayer();
	/*	For the debug menu on the Cities tab. Don't really know which
		perspective to assume; eWhoTo will be correct more often than not. */
	if (eActivePlayer != eWhoTo && eActivePlayer != kCity.getOwner())
	{
		FAssert(GC.getGame().isDebugMode());
		eActivePlayer = eWhoTo;
	}
	PlayerTypes eOtherPlayer = (eWhoTo == eActivePlayer ? kCity.getOwner() : eWhoTo);
	bool bLiberate = (eWhoTo == eOtherPlayer && kCity.getLiberationPlayer() == eWhoTo);
	DenialTypes eDenial = NO_DENIAL;
	if (kCity.getOwner() == eActivePlayer)
		eDenial = GET_PLAYER(eActivePlayer).AI_cityTrade(kCity.AI(), eOtherPlayer);
	else eDenial = GET_PLAYER(eOtherPlayer).AI_cityTrade(kCity.AI(), eActivePlayer);
	bool bWilling = (eDenial == NO_DENIAL);
	CvWString szReason;
	if (!bWilling && bReason)
	{
		szReason = CvWString::format(SETCOLR L"%s" ENDCOLR, TEXT_COLOR("COLOR_NEGATIVE_TEXT"),
				GC.getInfo(eDenial).getText());
	}
	szBuffer.append(GET_PLAYER(eOtherPlayer).getName());
	szBuffer.append(L" ");
	CvWString szAction;
	if (eWhoTo == eActivePlayer && bWilling)
		szAction = gDLL->getText("TXT_KEY_WILLING_TO_CEDE");
	else if (eWhoTo != eActivePlayer && bWilling)
	{
		if (bLiberate && !bListMore)
			szAction = gDLL->getText("TXT_KEY_WANTS_LIBERATED");
		else szAction = gDLL->getText("TXT_KEY_WILLING_TO_TRADE_FOR");
	}
	else if (eWhoTo == eActivePlayer && !bWilling)
		szAction = gDLL->getText("TXT_KEY_REFUSES_TO_CEDE");
	else
	{
		FAssert(eWhoTo != eActivePlayer && !bWilling);
		szAction = gDLL->getText("TXT_KEY_REFUSES_TO_ACCEPT");
	}
	szBuffer.append(szAction + L" ");
	szBuffer.append(kCity.getName());
	if (bListMore)
	{
		CvWString szLiberate = L" (" + gDLL->getText("TXT_KEY_LIBERATE_CITY") + ")";
		if (bLiberate)
			szBuffer.append(szLiberate);
		bool bFound = false;
		FOR_EACH_CITYAI(pLoopCity, GET_PLAYER(kCity.getOwner()))
		{
			// Skip to kCity
			if (!bFound && pLoopCity != &kCity)
				continue;
			bFound = true;
			if (!GET_PLAYER(kCity.getOwner()).canTradeItem(eWhoTo, TradeData(
				TRADE_CITIES, pLoopCity->getID())))
			{
				continue;
			}
			// Needs to be in the same column of the "Cities" tab as kCity
			if ((GET_PLAYER(kCity.getOwner()).
				AI_cityTrade(*pLoopCity, eWhoTo) == NO_DENIAL) != bWilling)
			{
				continue;
			}
			szBuffer.append(L", ");
			szBuffer.append(pLoopCity->getName());
			if (kCity.getOwner() == eActivePlayer && pLoopCity->getLiberationPlayer() == eWhoTo)
				szBuffer.append(szLiberate);
		}
	}
	/*  If the texts on the Cities tab show population counts, then this should
		be shown as an explanation. */
	/*szBuffer.append(CvWString::format(L" (%d %s)", kCity.getPopulation(),
			gDLL->getText("TXT_KEY_DEMO_SCREEN_POPULATION_TEXT").GetCString()));*/
	if (!szReason.empty() && !bListMore)
	{
		szBuffer.append(L":\n");
		szBuffer.append(szReason);
	}
}

// advc.910:
void CvGameTextMgr::setResearchModifierHelp(CvWStringBuffer& szBuffer, TechTypes eTech)
{
	int iFromOtherKnown, iFromPaths, iFromTeam;
	// Not necessary here, but let's make double sure to initialize.
	iFromOtherKnown = iFromPaths = iFromTeam = 0;
	int iMod = GET_PLAYER(getActivePlayer()).calculateResearchModifier(eTech,
			&iFromOtherKnown, &iFromPaths, &iFromTeam) - 100;
	// <advc.groundbr>
	int iFromGroundbreaking = -GET_PLAYER(getActivePlayer()).
			groundbreakingPenalty(eTech); // </advc.groundbr>
	int iNonZero = 0;
	if (iFromOtherKnown != 0 || iFromGroundbreaking != 0)
		iNonZero++;
	if (iFromPaths != 0)
		iNonZero++;
	if (iFromTeam != 0)
		iNonZero++;
	if (iNonZero > 0)
	{
		szBuffer.append(NEWLINE);
		char const* szPos = "COLOR_POSITIVE_TEXT";
		char const* szNeg = "COLOR_NEGATIVE_TEXT";
		int iBullet = gDLL->getSymbolID(BULLET_CHAR);
		szBuffer.append(gDLL->getText("TXT_KEY_RESEARCH_MODIFIER"));
		szBuffer.append(CvWString::format(L": " SETCOLR L"%s%d%%" ENDCOLR,
				TEXT_COLOR(iMod > 0 ? szPos : szNeg), iMod > 0 ? L"+" : L"", iMod));
		// <advc.groundbr> Show only either tech diffusion or the ground-breaking penalty
		if (iFromOtherKnown + iFromGroundbreaking != 0)
		{
			bool const bShowOtherKnown = (iFromOtherKnown + iFromGroundbreaking > 0);
			if (iNonZero == 1)
				szBuffer.append(L" ");
			else
			{
				szBuffer.append(NEWLINE);
				if (bShowOtherKnown)
				{
					szBuffer.append(CvWString::format(L"%c" SETCOLR L"%d%% " ENDCOLR,
							iBullet, TEXT_COLOR(iFromOtherKnown > 0 ? szPos : szNeg),
							iFromOtherKnown));
				}
				else
				{
					szBuffer.append(CvWString::format(L"%c" SETCOLR L"%d%% " ENDCOLR,
							iBullet, TEXT_COLOR(iFromGroundbreaking > 0 ? szPos : szNeg),
							iFromGroundbreaking));
				}
			}
			if (bShowOtherKnown)
				szBuffer.append(gDLL->getText("TXT_KEY_RESEARCH_MODIFIER_OTHER_KNOWN"));
			else szBuffer.append(gDLL->getText("TXT_KEY_RESEARCH_MODIFIER_GROUNDBREAKING"));
		} // </advc.groundbr>
		if (iFromPaths != 0)
		{
			if (iNonZero == 1)
				szBuffer.append(L" ");
			else
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(CvWString::format(L"%c" SETCOLR L"%d%% " ENDCOLR,
						iBullet, TEXT_COLOR(iFromPaths > 0 ? szPos : szNeg),
						iFromPaths));
			}
			szBuffer.append(gDLL->getText("TXT_KEY_RESEARCH_MODIFIER_PATHS"));
		}
		if (iFromTeam != 0)
		{
			if (iNonZero == 1)
				szBuffer.append(L" ");
			else
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(CvWString::format(L"%c" SETCOLR L"%d%% " ENDCOLR,
					iBullet, TEXT_COLOR(iFromTeam > 0 ? szPos : szNeg),
					iFromTeam));
			}
			szBuffer.append(gDLL->getText("TXT_KEY_RESEARCH_MODIFIER_TEAM"));
		}
	}
}


void CvGameTextMgr::setBasicUnitHelp(CvWStringBuffer &szBuffer, UnitTypes eUnit, bool bCivilopediaText)
{
	PROFILE_FUNC();

	if (eUnit == NO_UNIT)
		return;

	CvUnitInfo const& u = GC.getInfo(eUnit); // advc
	if (!bCivilopediaText)
	{
		szBuffer.append(NEWLINE);
		CvWString szTempBuffer;

		if (u.getDomainType() == DOMAIN_AIR)
		{
			if (u.getAirCombat() > 0)
			{
				szTempBuffer.Format(L"%d%c, ", u.getAirCombat(), gDLL->getSymbolID(STRENGTH_CHAR));
				szBuffer.append(szTempBuffer);
			}
		}
		else
		{
			if (u.getCombat() > 0)
			{
				szTempBuffer.Format(L"%d%c, ", u.getCombat(), gDLL->getSymbolID(STRENGTH_CHAR));
				szBuffer.append(szTempBuffer);
			}
		}
		// <advc.905b>
		bool bAllSpeedBonusesAvailable = true;
		CvCity* pCity = gDLL->UI().getHeadSelectedCity();
		if (pCity == NULL)
			bAllSpeedBonusesAvailable = false;
		// "3 MOVES_CHAR (+1 with Coal)" when not all bonuses available
		CvWStringBuffer szSpeedBonuses;
		// "4 MOVES_CHAR (with Coal)" for city screen when all bonuses available
		CvWStringBuffer szSpeedBonusesCompact;
		int iTotalExtraMoves = 0;
		for (int i = 0; i < u.getNumSpeedBonuses(); i++)
		{
			if (i > 0)
			{
				szSpeedBonuses.append(L", ");
				szSpeedBonusesCompact.append(L",");
			}
			else
			{
				szSpeedBonusesCompact.append(gDLL->getText("TXT_KEY_WITH"));
				szSpeedBonusesCompact.append(L" ");
			}
			int iExtraMoves = u.getExtraMoves(i);
			if (iExtraMoves > 0)
				szSpeedBonuses.append(L"+");
			szTempBuffer.Format(L"%d", iExtraMoves);
			iTotalExtraMoves += iExtraMoves;
			szSpeedBonuses.append(szTempBuffer);
			szSpeedBonuses.append(gDLL->getText("TXT_KEY_WITH_SPACE"));
			BonusTypes eBonus = u.getSpeedBonuses(i);
			szTempBuffer.Format(L"%c", GC.getInfo(eBonus).getChar());
			szSpeedBonuses.append(szTempBuffer);
			szSpeedBonusesCompact.append(szTempBuffer);
			if(bAllSpeedBonusesAvailable && !pCity->hasBonus(eBonus))
				bAllSpeedBonusesAvailable = false;
		}
		int iMoves = u.getMoves();
		if(bAllSpeedBonusesAvailable)
			iMoves = std::max(0, iMoves + iTotalExtraMoves);
		// </advc.905b>
		szTempBuffer.Format(L"%d%c", iMoves, gDLL->getSymbolID(MOVES_CHAR));
		szBuffer.append(szTempBuffer);
		// <advc.905b>
		if(!szSpeedBonuses.isEmpty())
		{
			// No space b/c there's already a bit of a space after MOVES_CHAR
			szBuffer.append(L"(");
			if(bAllSpeedBonusesAvailable)
				szBuffer.append(szSpeedBonusesCompact);
			else szBuffer.append(szSpeedBonuses);
			szBuffer.append(L")");
		} // </advc.905b>
		if (u.getAirRange() > 0)
		{
			szBuffer.append(L", ");
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_AIR_RANGE", u.getAirRange()));
		}
	}

	if (u.isGoldenAge())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_GOLDEN_AGE"));
	}

	if (u.getLeaderExperience() > 0)
	{
		if (GC.getDefineINT("WARLORD_EXTRA_EXPERIENCE_PER_UNIT_PERCENT") == 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_LEADER", u.getLeaderExperience()));
		}
		else
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_LEADER_EXPERIENCE", u.getLeaderExperience()));
		}
	}

	if (NO_PROMOTION != u.getLeaderPromotion())
	{
		szBuffer.append(CvWString::format(L"%s%c%s", NEWLINE, gDLL->getSymbolID(BULLET_CHAR), gDLL->getText("TXT_KEY_PROMOTION_WHEN_LEADING").GetCString()));
		parsePromotionHelp(szBuffer, (PromotionTypes)u.getLeaderPromotion(), L"\n   ");
	}

	if (u.getBaseDiscover() > 0 || u.getDiscoverMultiplier() > 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_DISCOVER_TECH"));
	}

	if (u.getBaseHurry() > 0 || u.getHurryMultiplier() > 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_HURRY_PRODUCTION"));
	}

	if (u.getBaseTrade() > 0 || u.getTradeMultiplier() > 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_TRADE_MISSION"));
	}

	if (u.getGreatWorkCulture() > 0)
	{
		int iCulture = u.getGreatWorkCulture();
		if (GC.getGame().getGameSpeedType() != NO_GAMESPEED)
		{
			iCulture *= GC.getInfo(GC.getGame().getGameSpeedType()).getUnitGreatWorkPercent();
			iCulture /= 100;
		}

		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_GREAT_WORK", iCulture));
	}

	if (u.getEspionagePoints() > 0)
	{
		int iEspionage = u.getEspionagePoints();
		if (NO_GAMESPEED != GC.getGame().getGameSpeedType())
		{
			iEspionage *= GC.getInfo(GC.getGame().getGameSpeedType()).getUnitGreatWorkPercent();
			iEspionage /= 100;
		}

		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_ESPIONAGE_MISSION", iEspionage));
	}

	// doc: statesman reform government
	if (u.isReformGovernment())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_CAN_REFORM_GOVERNMENT"));
	}

	// doc: statesman resolve crisis
	if (u.isResolveCrisis())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_CAN_RESOLVE_CRISIS"));
	}

	// doc: statesman diplomatic mission
	if (u.isDiplomaticMission())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_CAN_DIPLOMATIC_MISSION"));
	}

	// doc: religious persecution
	if (u.isPersecute())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_CAN_PERSECUTE"));
	}

	CvWString szTempBuffer;
	{
		bool bFirst = true;
		FOR_EACH_ENUM(Religion)
		{
			if (u.getReligionSpreads(eLoopReligion) > 0)
			{
				szTempBuffer.Format(L"%s%s", NEWLINE,
						gDLL->getText("TXT_KEY_UNIT_CAN_SPREAD").c_str());
				CvWString szReligion;
				szReligion.Format(L"<link=literal>%s</link>",
						GC.getInfo(eLoopReligion).getDescription());
				setListHelp(szBuffer, szTempBuffer, szReligion, L", ", bFirst);
			}
		}
	}
	// doc: missionary spread limitations
	{
		bool bFirst = true;
		FOR_EACH_ENUM(Religion)
		{
			if (u.getReligionSpreads(iI) > 0)
			{
				szBuffer.append(NEWLINE);
				if (GC.getInfo(eLoopReligion).isProselytizing())
				{
					szBuffer.append(gDLL->getText("TXT_KEY_UNIT_SPREAD_REQUIRES_GEOGRAPHY",
						GC.getInfo(eLoopReligion).getDescription()));
				}
				else
				{
					szBuffer.append(gDLL->getText("TXT_KEY_UNIT_SPREAD_REQUIRES_STATE_RELIGION",
						GC.getInfo(eLoopReligion).getDescription()));
				}
			}
		}
	}
	{
		bool bFirst = true;
		FOR_EACH_ENUM(Corporation)
		{
			if (u.getCorporationSpreads(eLoopCorporation) > 0)
			{
				szTempBuffer.Format(L"%s%s", NEWLINE,
						gDLL->getText("TXT_KEY_UNIT_CAN_EXPAND").c_str());
				CvWString szCorporation;
				szCorporation.Format(L"<link=literal>%s</link>",
						GC.getInfo(eLoopCorporation).getDescription());
				setListHelp(szBuffer, szTempBuffer, szCorporation, L", ", bFirst);
			}
		}
	}
	{
		bool bFirst = true;
		bool bSatellite = false;
		FOR_EACH_ENUM(Specialist)
		{
			if (u.getGreatPeoples(eLoopSpecialist))
			{
				szTempBuffer.Format(L"%s%s", NEWLINE,
						gDLL->getText("TXT_KEY_UNIT_CAN_JOIN").c_str());
				CvWString szSpecialistLink = CvWString::format(
						L"<link=literal>%s</link>",
						GC.getInfo(eLoopSpecialist).getDescription());
				setListHelp(szBuffer, szTempBuffer,
						szSpecialistLink.GetCString(), L", ", bFirst);

				if (GC.getInfo(eSpecialist).isSatellite())
					bSatellite = true;
			}
		}

		// doc: satellite limit
		if (bSatellite)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_SATELLITE_LIMIT"));
		}
	}
	// doc: slave
	{
		if (u.isSlave())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_SLAVE_LIMIT"));
		}
	}
	{
		bool bFirst = true;
		FOR_EACH_ENUM(Building)
		{
			if (u.getBuildings(eLoopBuilding)/* || u.getForceBuildings(eLoopBuilding)*/) // advc.003t
			{
				szTempBuffer.Format(L"%s%s", NEWLINE,
						gDLL->getText("TXT_KEY_UNIT_CAN_CONSTRUCT").c_str());
				CvWString szBuildingLink = CvWString::format(
							L"<link=literal>%s</link>",
							GC.getInfo(eLoopBuilding).getDescription());
				setListHelp(szBuffer, szTempBuffer,
						szBuildingLink.GetCString(), L", ", bFirst);
			}
		}
	}
	if (u.getCargoSpace() > 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_CARGO_SPACE", u.getCargoSpace()));

		if (u.getSpecialCargo() != NO_SPECIALUNIT)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_CARRIES",
					GC.getInfo(u.getSpecialCargo()).getTextKeyWide()));
		}
	}
	{
		bool bFirst = true;
		szTempBuffer.Format(L"%s%s ", NEWLINE,
				gDLL->getText("TXT_KEY_UNIT_CANNOT_ENTER").GetCString());
		if (u.isAnyTerrainImpassable()) // advc.003t
		{
			FOR_EACH_ENUM(Terrain)
			{
				// doc: we expect these to be impassable
				if (eLoopTerrain == TERRAIN_DESERT || eLoopTerrain == TERRAIN_TUNDRA || eLoopTerrain == TERRAIN_SNOW)
					continue;

				if (u.getTerrainImpassable(eLoopTerrain))
				{
					CvWString szTerrain;
					TechTypes eTech = u.getTerrainPassableTech(eLoopTerrain);
					if (NO_TECH == eTech)
					{
						szTerrain.Format(L"<link=literal>%s</link>",
								GC.getInfo(eLoopTerrain).getDescription());
					}
					else
					{
						szTerrain = gDLL->getText("TXT_KEY_TERRAIN_UNTIL_TECH",
								GC.getInfo(eLoopTerrain).getTextKeyWide(),
								GC.getInfo(eTech).getTextKeyWide());
					}
					setListHelp(szBuffer, szTempBuffer, szTerrain, L", ", bFirst);
				}
			}
		}
		if (u.isAnyFeatureImpassable()) // advc.003t
		{
			FOR_EACH_ENUM(Feature)
			{
				// doc: we expect these to be impassable
				if (eLoopFeature == FEATURE_JUNGLE || eLoopFeature == FEATURE_RAINFOREST || eLoopFeature == FEATURE_MARSH)
					continue;

				if (u.getFeatureImpassable(eLoopFeature))
				{
					// advc.001 (from MNAI): was getTerrainPassableTech
					TechTypes eTech = u.getFeaturePassableTech(eLoopFeature);
					CvWString szFeature;
					if (eTech == NO_TECH)
					{
						szFeature.Format(L"<link=literal>%s</link>",
								GC.getInfo(eLoopFeature).getDescription());
					}
					else
					{
						szFeature = gDLL->getText("TXT_KEY_TERRAIN_UNTIL_TECH",
								GC.getInfo(eLoopFeature).getTextKeyWide(),
								GC.getInfo(eTech).getTextKeyWide());
					}
					setListHelp(szBuffer, szTempBuffer, szFeature, L", ", bFirst);
					bFirst = false;
				}
			}
		}
	}
	// doc: generally impassable terrain being passable
	{
		bool bFirst = true;
		szTempBuffer.Format(L"%s%s ", NEWLINE, gDLL->getText("TXT_KEY_UNIT_CAN_ENTER").GetCString());

		if (u.getDomainType() == DOMAIN_LAND)
		{
			FOR_EACH_ENUM(Terrain)
			{
				if (eLoopTerrain == TERRAIN_DESERT || eLoopTerrain == TERRAIN_TUNDRA || eLoopTerrain == TERRAIN_SNOW)
				{
					if (!u.getTerrainImpassable(eLoopTerrain))
					{
						CvWString szTerrain;
						szTerrain.Format(L"<link=literal>%s</link>", GC.getInfo(eLoopTerrain).getDescription());
						setListHelp(szBuffer, szTempBuffer, szTerrain, L", ", bFirst);
						bFirst = false;
					}
				}
			}

			FOR_EACH_ENUM(Feature)
			{
				if (eLoopFeature == FEATURE_JUNGLE || eLoopFeature == FEATURE_RAINFOREST || eLoopFeature == FEATURE_MARSH)
				{
					if (!u.getFeatureImpassable(eLoopFeature))
					{
						CvWString szFeature;
						szFeature.Format(L"<link=literal>%s</link>", GC.getFeatureInfo((FeatureTypes)iI).getDescription());
						setListHelp(szBuffer, szTempBuffer, szFeature, L", ", bFirst);
						bFirst = false;
					}
				}
			}
		}
	}
	if (u.isInvisible())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_INVISIBLE_ALL"));
	}
	else if (u.getInvisibleType() != NO_INVISIBLE)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_INVISIBLE_MOST"));
	}

	for (int i = 0; i < u.getNumSeeInvisibleTypes(); i++)
	{
		if (bCivilopediaText || u.getSeeInvisibleType(i) != u.getInvisibleType())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_SEE_INVISIBLE",
					GC.getInfo((InvisibleTypes)u.getSeeInvisibleType(i)).getTextKeyWide()));
		}
	}

	if (u.canMoveImpassable())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_CAN_MOVE_IMPASSABLE"));
	}


	if (u.isNoBadGoodies())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_NO_BAD_GOODIES"));
	}

	if (u.isHiddenNationality())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_HIDDEN_NATIONALITY"));
	}

	if (u.isAlwaysHostile())
	{	/*  advc.033: Hidden nationality sounds like it implies "attack without
			declaring war". Only show the latter when the former isn't true. */
		if(!u.isHiddenNationality())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_ALWAYS_HOSTILE"));
		}
		// <advc.033> Not technically a unit ability, but should be regarded as one.
		if(u.isPillage() && u.getDomainType() == DOMAIN_SEA)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_CAN_PLUNDER"));
		} // </advc.033>
	}

	if (u.isOnlyDefensive())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_ONLY_DEFENSIVE"));
	}
	// <advc.315a>
	if (u.isOnlyAttackAnimals())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_ONLY_ATTACK_ANIMALS"));
	} // </advc.315a>
	// <advc.315b>
	if (u.isOnlyAttackBarbarians())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_ONLY_ATTACK_BARBARIANS"));
	} // </advc.315b>

	if (u.isNoCapture())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText(
				// advc.315b: Barbarian-only attackers can capture units
				u.isOnlyAttackBarbarians() ? "TXT_KEY_UNIT_CANNOT_CAPTURE_CITIES" :
				"TXT_KEY_UNIT_CANNOT_CAPTURE"));
	}

	if (u.isRivalTerritory())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_EXPLORE_RIVAL"));
	}

	if (u.isFound())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_FOUND_CITY"));

		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_REBUILD"));
	}
	{
		int iCount = 0;
		FOR_EACH_ENUM(Build)
		{
			if (u.getBuilds(eLoopBuild))
				iCount++;
		}
		// doc: hardcode this so only workers apply
		//if (iCount > (GC.getNumBuildInfos() * 3) / 4)
		if (iCount > 5)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_IMPROVE_PLOTS"));
		}
		else
		{
			bool bFirst = true;
			FOR_EACH_ENUM(Build)
			{
				if (u.getBuilds(eLoopBuild))
				{	// <advc.004w>
					TechTypes eTech = (TechTypes)GC.getInfo(eLoopBuild).getTechPrereq();
					PlayerTypes ePlayer = getActivePlayer();
					if(eTech != NO_TECH && ePlayer != NO_PLAYER && GC.getInfo(eTech).
						getEra() - GET_PLAYER(ePlayer).getCurrentEra() > 1)
					{
						continue;
					} // </advc.004w>
					//szTempBuffer.Format(L"%s%s ", NEWLINE,
					// K-Mod 4/jan/11: removed space
					szTempBuffer.Format(L"%s%s", NEWLINE,
							gDLL->getText("TXT_KEY_UNIT_CAN").c_str());
					setListHelp(szBuffer, szTempBuffer,
							GC.getInfo(eLoopBuild).getDescription(), L", ", bFirst);
				}
			}
		}
	}

	// doc: work rate
	if (u.getWorkRate() > 100)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_WORK_RATE_MODIFIER",
				u.getWorkRate() - 100));
	}

	if (u.isNuke())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_CAN_NUKE"));
	}

	if (u.isCounterSpy())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_EXPOSE_SPIES"));
	}

	if (u.getFirstStrikes() + u.getChanceFirstStrikes() > 0)
	{
		if (u.getChanceFirstStrikes() == 0)
		{
			if (u.getFirstStrikes() == 1)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_UNIT_ONE_FIRST_STRIKE"));
			}
			else
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_UNIT_NUM_FIRST_STRIKES",
						u.getFirstStrikes()));
			}
		}
		else
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_FIRST_STRIKE_CHANCES",
					u.getFirstStrikes(),
					u.getFirstStrikes() + u.getChanceFirstStrikes()));
		}
	}

	if (u.isFirstStrikeImmune())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_IMMUNE_FIRST_STRIKES"));
	}

	if (u.isNoDefensiveBonus())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_NO_DEFENSE_BONUSES"));
	}

	if (u.isFlatMovementCost())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_FLAT_MOVEMENT"));
	}

	if (u.isIgnoreTerrainCost())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_IGNORE_TERRAIN"));
	}

	if (u.getInterceptionProbability() > 0)
	{
		// SuperSpies: TSHEEP Display Spy Messages Differently
		if (u.isSpy())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_INTERCEPT_AIRCRAFT_SPY",
					u.getInterceptionProbability()));
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_INTERCEPT_AIRCRAFT_SPY_COUNTER",
					u.getInterceptionProbability() * 5));
		}
		else
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_INTERCEPT_AIRCRAFT",
					u.getInterceptionProbability()));
		}
	}

	if (u.getEvasionProbability() > 0)
	{
		szBuffer.append(NEWLINE);
		// SuperSpies: TSHEEP Display Spy Messages Differently
		if (u.isSpy())
		{
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_EVADE_INTERCEPTION_SPY",
					u.getEvasionProbability()));
		}
		else
		{
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_EVADE_INTERCEPTION",
					u.getEvasionProbability()));
		}
	}

	if (u.getWithdrawalProbability() > 0)
	{
		szBuffer.append(NEWLINE);
		// SuperSpies: TSHEEP Display Spy Messages Differently
		if (u.isSpy())
		{
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_ESCAPE_SPY",
					u.getWithdrawalProbability()));
		}
		else
		{
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_WITHDRAWL_PROBABILITY",
					u.getWithdrawalProbability()));
		}
	}

	if (u.getCombatLimit() < GC.getMAX_HIT_POINTS() &&
		u.getCombat() > 0 && !u.isOnlyDefensive())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_COMBAT_LIMIT",
				(100 * u.getCombatLimit()) / GC.getMAX_HIT_POINTS()));
	}

	if (u.getCollateralDamage() > 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText(/* advc.004: */ bCivilopediaText ?
				"TXT_KEY_UNIT_COLLATERAL_DAMAGE" :
				"TXT_KEY_UNIT_COLLATERAL_DAMAGE_SHORT", // advc.004
				100 * u.getCollateralDamageLimit() / GC.getMAX_HIT_POINTS(),
				u.getCollateralDamageMaxUnits()));// advc.004
	}

	FOR_EACH_ENUM(UnitCombat)
	{
		if (u.getUnitCombatCollateralImmune(eLoopUnitCombat))
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_COLLATERAL_IMMUNE",
					GC.getInfo(eLoopUnitCombat).getTextKeyWide()));
		}
	}

	if (u.getCityAttackModifier() == u.getCityDefenseModifier())
	{
		if (u.getCityAttackModifier() != 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_CITY_STRENGTH_MOD",
					u.getCityAttackModifier()));
		}
	}
	else
	{
		if (u.getCityAttackModifier() != 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_CITY_ATTACK_MOD",
					u.getCityAttackModifier()));
		}

		if (u.getCityDefenseModifier() != 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_CITY_DEFENSE_MOD",
					u.getCityDefenseModifier()));
		}
	}

	if (u.getAnimalCombatModifier() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_ANIMAL_COMBAT_MOD",
				u.getAnimalCombatModifier()));
	}
	// <advc.315c>
	if (u.getBarbarianCombatModifier() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_BARBARIAN_COMBAT_MOD",
				u.getBarbarianCombatModifier()));
	} // </advc.315c>

	if (u.getDropRange() > 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_PARADROP_RANGE",
				u.getDropRange()));
	}

	if (u.getHillsDefenseModifier() == u.getHillsAttackModifier())
	{
		if (u.getHillsAttackModifier() != 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_HILLS_STRENGTH",
					u.getHillsAttackModifier()));
		}
	}
	else
	{
		if (u.getHillsAttackModifier() != 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_HILLS_ATTACK",
					u.getHillsAttackModifier()));
		}

		if (u.getHillsDefenseModifier() != 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_HILLS_DEFENSE",
					u.getHillsDefenseModifier()));
		}
	}

	// doc: open terrain modifiers
	if (u.getPlainsAttackModifier() == u.getPlainsDefenseModifier())
	{
		if (u.getPlainsAttackModifier() != 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_PLAINS_STRENGTH",
					u.getPlainsAttackModifier()));
		}
	}
	else
	{
		if (u.getPlainsAttackModifier() != 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_PLAINS_ATTACK",
					u.getPlainsAttackModifier()));
		}

		if (u.getPlainsDefenseModifier() != 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_PLAINS_DEFENSE",
					u.getPlainsDefenseModifier()));
		}
	}

	FOR_EACH_ENUM(Terrain)
	{
		// doc: terrain strength
		if (u.getTerrainDefenseModifier(eLoopTerrain) == u.getTerrainAttackModifier(eLoopTerrain))
		{
			if (u.getTerrainAttackModifier(eLoopTerrain) != 0)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_UNIT_ATTACK_AND_DEFENSE",
						u.getTerrainAttackModifier(eLoopTerrain),
						GC.getInfo(eLoopTerrain).getTextKeyWide()));
			}
		}
		else
		{
			if (u.getTerrainDefenseModifier(eLoopTerrain) != 0)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_UNIT_DEFENSE",
						u.getTerrainDefenseModifier(eLoopTerrain),
						GC.getInfo(eLoopTerrain).getTextKeyWide()));
			}
			if (u.getTerrainAttackModifier(eLoopTerrain) != 0)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_UNIT_ATTACK",
						u.getTerrainAttackModifier(eLoopTerrain),
						GC.getInfo(eLoopTerrain).getTextKeyWide()));
			}
		}
	}

	FOR_EACH_ENUM(Feature)
	{
		// doc: feature strength
		if (u.getFeatureDefenseModifier(eLoopFeature) == u.getFeatureAttackModifier(eLoopFeature))
		{
			if (u.getFeatureAttackModifier(eLoopFeature) != 0)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_UNIT_ATTACK_AND_DEFENSE",
						u.getFeatureAttackModifier(eLoopFeature),
						GC.getInfo(eLoopFeature).getTextKeyWide()));
			}
		}
		else
		{
			if (u.getFeatureDefenseModifier(eLoopFeature) != 0)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_UNIT_DEFENSE",
						u.getFeatureDefenseModifier(eLoopFeature),
						GC.getInfo(eLoopFeature).getTextKeyWide()));
			}

			if (u.getFeatureAttackModifier(eLoopFeature) != 0)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_UNIT_ATTACK",
						u.getFeatureAttackModifier(eLoopFeature),
						GC.getInfo(eLoopFeature).getTextKeyWide()));
			}
		}
	}

	FOR_EACH_ENUM(UnitClass)
	{
		if (u.getUnitClassAttackModifier(eLoopUnitClass) ==
			u.getUnitClassDefenseModifier(eLoopUnitClass))
		{
			if (u.getUnitClassAttackModifier(eLoopUnitClass) != 0)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_UNIT_MOD_VS_TYPE",
						u.getUnitClassAttackModifier(eLoopUnitClass),
						GC.getInfo(eLoopUnitClass).getTextKeyWide()));
			}
		}
		else
		{
			if (u.getUnitClassAttackModifier(eLoopUnitClass) != 0)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_UNIT_ATTACK_MOD_VS_CLASS",
						u.getUnitClassAttackModifier(eLoopUnitClass),
						GC.getInfo(eLoopUnitClass).getTextKeyWide()));
			}

			if (u.getUnitClassDefenseModifier(eLoopUnitClass) != 0)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_UNIT_DEFENSE_MOD_VS_CLASS",
						u.getUnitClassDefenseModifier(eLoopUnitClass),
						GC.getInfo(eLoopUnitClass).getTextKeyWide()));
			}
		}
	}

	FOR_EACH_ENUM(UnitCombat)
	{
		if (u.getUnitCombatModifier(eLoopUnitCombat) != 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_MOD_VS_TYPE",
					u.getUnitCombatModifier(eLoopUnitCombat),
					GC.getInfo(eLoopUnitCombat).getTextKeyWide()));
		}
	}

	FOR_EACH_ENUM(Domain)
	{
		if (u.getDomainModifier(eLoopDomain) != 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_MOD_VS_TYPE_NO_LINK",
					u.getDomainModifier(eLoopDomain),
					GC.getInfo(eLoopDomain).getTextKeyWide()));
		}
	}
	{
		bool bFirst = true;
		szTempBuffer.clear();
		FOR_EACH_ENUM(UnitClass)
		{
			if (u.getTargetUnitClass(eLoopUnitClass))
			{
				if (bFirst)
					bFirst = false;
				else szTempBuffer += L", ";
				szTempBuffer += CvWString::format(L"<link=literal>%s</link>",
						GC.getInfo(eLoopUnitClass).getDescription());
			}
		}

		if (!bFirst)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_TARGETS_UNIT_FIRST",
					szTempBuffer.GetCString()));
		}
	}
	{
		bool bFirst = true;
		szTempBuffer.clear();
		FOR_EACH_ENUM(UnitClass)
		{
			if (u.getDefenderUnitClass(eLoopUnitClass))
			{
				if (bFirst)
					bFirst = false;
				else szTempBuffer += L", ";
				szTempBuffer += CvWString::format(L"<link=literal>%s</link>",
						GC.getInfo(eLoopUnitClass).getDescription());
			}
		}

		if (!bFirst)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_DEFENDS_UNIT_FIRST",
					szTempBuffer.GetCString()));
		}
	}
	{
		bool bFirst = true;
		szTempBuffer.clear();
		FOR_EACH_ENUM(UnitCombat)
		{
			if (u.getTargetUnitCombat(eLoopUnitCombat))
			{
				if (bFirst)
					bFirst = false;
				else szTempBuffer += L", ";
				szTempBuffer += CvWString::format(L"<link=literal>%s</link>",
						GC.getInfo(eLoopUnitCombat).getDescription());
			}
		}
		if (!bFirst)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_TARGETS_UNIT_FIRST",
					szTempBuffer.GetCString()));
		}
	}
	{
		bool bFirst = true;
		szTempBuffer.clear();
		FOR_EACH_ENUM(UnitCombat)
		{
			if (u.getDefenderUnitCombat(eLoopUnitCombat))
			{
				if (bFirst)
					bFirst = false;
				else szTempBuffer += L", ";
				szTempBuffer += CvWString::format(L"<link=literal>%s</link>",
						GC.getInfo(eLoopUnitCombat).getDescription());
			}
		}
		if (!bFirst)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_DEFENDS_UNIT_FIRST",
					szTempBuffer.GetCString()));
		}
	}
	{
		bool bFirst = true;
		szTempBuffer.clear();
		FOR_EACH_ENUM(UnitClass)
		{
			if (u.getFlankingStrikeUnitClass(eLoopUnitClass) > 0)
			{
				if (bFirst)
					bFirst = false;
				else szTempBuffer += L", ";
				szTempBuffer += CvWString::format(L"<link=literal>%s</link>",
						GC.getInfo(eLoopUnitClass).getDescription());
			}
		}
		if (!bFirst)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_FLANKING_STRIKES",
					szTempBuffer.GetCString()));
		}
	}
	if (u.getBombRate() > 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_BOMB_RATE",
				(u.getBombRate() * 100) / GC.getMAX_CITY_DEFENSE_DAMAGE()));
	}

	if (u.getBombardRate() > 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_BOMBARD_RATE",
				(u.getBombardRate() * 100) / GC.getMAX_CITY_DEFENSE_DAMAGE()));
	}
	// <advc.905b>
	if (bCivilopediaText)
	{
		for (int i = 0; i < u.getNumSpeedBonuses(); i++)
		{
			szBuffer.append(NEWLINE);
			szTempBuffer.Format(L"%c", gDLL->getSymbolID(BULLET_CHAR));
			szBuffer.append(szTempBuffer);
			int iExtraMoves = u.getExtraMoves(i);
			if(iExtraMoves > 0)
				szBuffer.append(L"+");
			szTempBuffer.Format(L"%d%c", iExtraMoves, gDLL->getSymbolID(MOVES_CHAR));
			szBuffer.append(szTempBuffer);
			szBuffer.append(gDLL->getText("TXT_KEY_WITH") + L" ");
			szTempBuffer.Format(L"<link=literal>%s</link>",
					GC.getInfo(u.getSpeedBonuses(i)).getDescription());
			szBuffer.append(szTempBuffer);
		}
	} // </advc.905b>
	{
		bool bFirst = true;
		FOR_EACH_ENUM(Promotion)
		{
			if (u.getFreePromotions(eLoopPromotion))
			{
				szTempBuffer.Format(L"%s%s", NEWLINE,
						gDLL->getText("TXT_KEY_UNIT_STARTS_WITH").c_str());
				setListHelp(szBuffer, szTempBuffer,
						CvWString::format(L"<link=literal>%s</link>",
						GC.getInfo(eLoopPromotion).getDescription()), L", ", bFirst);
			}
		}
	}
	if (u.getExtraCost() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_EXTRA_COST", u.getExtraCost()));
	}
	// doc: unit food production
	if (u.isFoodProduction())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_FOOD_PRODUCED"));
	}
	// (advc.004w: ProductionTraits moved into setProductionSpeedHelp)
	if (!CvWString(u.getHelp()).empty())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(u.getHelp());
	}
}


void CvGameTextMgr::setUnitHelp(CvWStringBuffer &szBuffer, UnitTypes eUnit,
	bool bCivilopediaText, bool bStrategyText, bool bTechChooserText, CvCity* pCity)
{
	PROFILE_FUNC();
	if (eUnit == NO_UNIT)
		return;
	CvWString szTempBuffer;
	CvUnitInfo const& u = GC.getInfo(eUnit);
	PlayerTypes ePlayer = NO_PLAYER;
	if (pCity != NULL)
		ePlayer = pCity->getOwner();
	else ePlayer = getActivePlayer();

	eCivilization = (ePlayer != NO_PLAYER) ? GET_PLAYER(ePlayer).getCivilizationType() : NO_CIVILIZATION;

	if (!bCivilopediaText)
	{
		szTempBuffer.Format(SETCOLR L"%s" ENDCOLR,
				TEXT_COLOR("COLOR_UNIT_TEXT"), u.getDescription());
		szBuffer.append(szTempBuffer);

		if (u.getUnitCombatType() != NO_UNITCOMBAT)
		{
			szTempBuffer.Format(L" (%s)",
					GC.getInfo(u.getUnitCombatType()).getDescription());
			szBuffer.append(szTempBuffer);
		}
	}
	// test for unique unit
	UnitClassTypes const eUnitClass = u.getUnitClassType();
	CvUnitClassInfo const& kUnitClass = GC.getInfo(eUnitClass); // advc
	UnitTypes const eDefaultUnit = kUnitClass.getDefaultUnit();

	if (eDefaultUnit != NO_UNIT && eDefaultUnit != eUnit &&
		!u.isGraphicalOnly()) // doc: exclude graphical only
	{
		FOR_EACH_ENUM(Civilization)
		{
			UnitTypes eUniqueUnit = GC.getInfo(eLoopCivilization).
					getCivilizationUnits(eUnitClass);
			if (eUniqueUnit == eUnit)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_UNIQUE_UNIT",
						GC.getInfo(eLoopCivilization).getTextKeyWide()));
			}
		}

		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_REPLACES_UNIT",
				GC.getInfo(eDefaultUnit).getTextKeyWide()));
	}

	if (kUnitClass.isWorldUnit())
	{
		if (pCity == NULL)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_WORLD_UNIT_ALLOWED",
					kUnitClass.getMaxGlobalInstances()));
		}
		else
		{
			//szBuffer.append(gDLL->getText("TXT_KEY_UNIT_WORLD_UNIT_LEFT", (kUnitClass.getMaxGlobalInstances() - (ePlayer != NO_PLAYER ? GC.getGame().getUnitClassCreatedCount(eUnitClass) + GET_TEAM(GET_PLAYER(ePlayer).getTeam()).getUnitClassMaking(eUnitClass) : 0))));
			// K-Mod
			int iRemaining = std::max(0, kUnitClass.getMaxGlobalInstances() -
					(ePlayer == NO_PLAYER ? 0 :
					GC.getGame().getUnitClassCreatedCount(eUnitClass) +
					GET_TEAM(GET_PLAYER(ePlayer).getTeam()).getUnitClassMaking(eUnitClass)));
			szBuffer.append(NEWLINE);

			if (iRemaining <= 0)
				szBuffer.append(CvWString::format(SETCOLR, TEXT_COLOR("COLOR_WARNING_TEXT")));

			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_WORLD_UNIT_LEFT", iRemaining));

			if (iRemaining <= 0)
				szBuffer.append(ENDCOLR);
			// K-Mod end
		}
	}

	if (GC.getInfo(eUnitClass).isTeamUnit())
	{
		if (pCity == NULL)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_TEAM_UNIT_ALLOWED",
					kUnitClass.getMaxTeamInstances()));
		}
		else
		{
			//szBuffer.append(gDLL->getText("TXT_KEY_UNIT_TEAM_UNIT_LEFT", (kUnitClass.getMaxTeamInstances() - (ePlayer != NO_PLAYER ? GET_TEAM(GET_PLAYER(ePlayer).getTeam()).getUnitClassCountPlusMaking(eUnitClass) : 0))));
			// K-Mod
			int iRemaining = std::max(0, kUnitClass.getMaxTeamInstances() -
					(ePlayer == NO_PLAYER ? 0 :
					GET_TEAM(ePlayer).getUnitClassCountPlusMaking(eUnitClass)));
			szBuffer.append(NEWLINE);

			if (iRemaining <= 0)
				szBuffer.append(CvWString::format(SETCOLR, TEXT_COLOR("COLOR_WARNING_TEXT")));

			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_TEAM_UNIT_LEFT", iRemaining));

			if (iRemaining <= 0)
				szBuffer.append(ENDCOLR);
			// K-Mod end
		}
	}

	if (GC.getInfo(eUnitClass).isNationalUnit())
	{
		// doc: Tibetan UP: can train unlimited missionaries
		bool bTibetanMissionary = false;
		if (eCivilizationType == TIBET)
		{
			FOR_EACH_ENUM(Religion)
			{
				if (u.getReligionSpreads(eLoopReligion) > 0)
				{
					bTibetanMissionary = true;
					break;
				}
			}
		}

		if (!bTibetanMissionary)
		{
			if (pCity == NULL)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_UNIT_NATIONAL_UNIT_ALLOWED",
						kUnitClass.getMaxPlayerInstances()));
			}
			else
			{
				//szBuffer.append(gDLL->getText("TXT_KEY_UNIT_NATIONAL_UNIT_LEFT", (kUnitClass.getMaxPlayerInstances() - (ePlayer != NO_PLAYER ? GET_PLAYER(ePlayer).getUnitClassCountPlusMaking(eUnitClass) : 0))));
				// K-Mod
				int iRemaining = std::max(0, kUnitClass.getMaxPlayerInstances() -
						(ePlayer == NO_PLAYER ? 0 :
						GET_PLAYER(ePlayer).getUnitClassCountPlusMaking(eUnitClass)));
				szBuffer.append(NEWLINE);

				if (iRemaining <= 0)
					szBuffer.append(CvWString::format(SETCOLR, TEXT_COLOR("COLOR_WARNING_TEXT")));

				szBuffer.append(gDLL->getText("TXT_KEY_UNIT_NATIONAL_UNIT_LEFT", iRemaining));

				if (iRemaining <= 0)
					szBuffer.append(ENDCOLR);
				// K-Mod end
			}
		}
	}

	setBasicUnitHelp(szBuffer, eUnit, bCivilopediaText);
	// advc.004g: Swapped so that BasicUnitHelp is printed before InstanceCostModifier
	if (kUnitClass.getInstanceCostModifier() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_INSTANCE_COST_MOD",
				kUnitClass.getInstanceCostModifier(),
				// advc.004g: Now also requires the unit class name
				kUnitClass.getDescription()));
	}

	if (pCity == NULL || !pCity->canTrain(eUnit))
	{
		if (pCity != NULL && GC.getGame().isNoNukes() && u.isNuke())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_NO_NUKES"));
		}

		if (u.getHolyCity() != NO_RELIGION)
		{
			if (pCity == NULL || !pCity->isHolyCity(u.getHolyCity()))
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_UNIT_REQUIRES_HOLY_CITY",
						GC.getInfo(u.getHolyCity()).getChar()));
			}
		}
		{
			bool bFirst = true;
			if (u.getSpecialUnitType() != NO_SPECIALUNIT &&
				(pCity == NULL ||
				!GC.getGame().isSpecialUnitValid(u.getSpecialUnitType())))
			{
				FOR_EACH_ENUM(Project)
				{
					if (GC.getInfo(eLoopProject).getEveryoneSpecialUnit() ==
						u.getSpecialUnitType())
					{
						szTempBuffer.Format(L"%s%s", NEWLINE,
								gDLL->getText("TXT_KEY_REQUIRES").c_str());
						CvWString szProject;
						szProject.Format(L"<link=literal>%s</link>",
								GC.getInfo(eLoopProject).getDescription());
						setListHelp(szBuffer, szTempBuffer, szProject,
								gDLL->getText("TXT_KEY_OR").c_str(), bFirst);
					}
				}
			}
			if (!bFirst)
				szBuffer.append(ENDCOLR);
		}
		{
			bool bFirst = true;
			if (u.isNuke() && (pCity == NULL || !GC.getGame().isNukesValid()))
			{
				FOR_EACH_ENUM(Project)
				{
					if (GC.getInfo(eLoopProject).isAllowsNukes())
					{
						szTempBuffer.Format(L"%s%s", NEWLINE,
								gDLL->getText("TXT_KEY_REQUIRES").c_str());
						CvWString szProject;
						szProject.Format(L"<link=literal>%s</link>",
								GC.getInfo(eLoopProject).getDescription());
						setListHelp(szBuffer, szTempBuffer, szProject,
								gDLL->getText("TXT_KEY_OR").c_str(), bFirst);
					}
				}
				FOR_EACH_ENUM(Building)
				{
					if (GC.getInfo(eLoopBuilding).isAllowsNukes())
					{
						szTempBuffer.Format(L"%s%s", NEWLINE,
								gDLL->getText("TXT_KEY_REQUIRES").c_str());
						CvWString szBuilding;
						szBuilding.Format(L"<link=literal>%s</link>",
								GC.getInfo(eLoopBuilding).getDescription());
						setListHelp(szBuffer, szTempBuffer, szBuilding,
								gDLL->getText("TXT_KEY_OR").c_str(), bFirst);
					}
				}
			}
			if (!bFirst)
				szBuffer.append(ENDCOLR);
		}
		if (!bCivilopediaText)
		{
			if (u.getPrereqBuilding() != NO_BUILDING)
			{
				if (pCity == NULL || pCity->getNumBuilding(u.getPrereqBuilding()) <= 0)
				{
					// K-Mod. Check if the player has an exemption from the building requirement.
					SpecialBuildingTypes eSpecialBuilding = GC.getInfo(u.getPrereqBuilding()).
							getSpecialBuildingType();
					if (pCity == NULL || eSpecialBuilding == NO_SPECIALBUILDING ||
						!GET_PLAYER(pCity->getOwner()).isSpecialBuildingNotRequired(eSpecialBuilding))
					{
					// K-Mod end
						szBuffer.append(NEWLINE);
						szBuffer.append(gDLL->getText("TXT_KEY_UNIT_REQUIRES_STRING",
								GC.getInfo(u.getPrereqBuilding()).getTextKeyWide()));
					}
				}
			}

			if (!bTechChooserText)
			{
				if (u.getPrereqAndTech() != NO_TECH)
				{
					if (getActivePlayer() == NO_PLAYER ||
						!GET_TEAM(ePlayer).isHasTech(u.getPrereqAndTech()))
					{
						szBuffer.append(NEWLINE);
						szBuffer.append(gDLL->getText("TXT_KEY_UNIT_REQUIRES_STRING",
								GC.getInfo(u.getPrereqAndTech()).getTextKeyWide()));
					}
				}
			}
			{
				bool bFirst = true;
				for (int i = 0; i < u.getNumPrereqAndTechs(); i++)
				{
					if (bTechChooserText || getActivePlayer() == NO_PLAYER ||
						!GET_TEAM(ePlayer).isHasTech(u.getPrereqAndTechs(i)))
					{
						szTempBuffer.Format(L"%s%s", NEWLINE,
								gDLL->getText("TXT_KEY_REQUIRES").c_str());
						setListHelp(szBuffer, szTempBuffer, GC.getInfo((TechTypes)
								u.getPrereqAndTechs(i)).getDescription(),
								gDLL->getText("TXT_KEY_AND").c_str(), bFirst);
					}
				}
				if (!bFirst)
					szBuffer.append(ENDCOLR);
			}
			if (u.getPrereqAndBonus() != NO_BONUS)
			{
				if (pCity == NULL || !pCity->hasBonus(u.getPrereqAndBonus()))
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_UNIT_REQUIRES_STRING",
							GC.getInfo(u.getPrereqAndBonus()).getTextKeyWide()));
				}
			}
			/*	<advc.004> (rewritten based on MNAI - lfgr fix 04/2021:
				Don't show any OR-prereq bonus if one of them is available.)
				This concerns units with an OR req. (which is met) and some
				additional requirement (which isn't met). */
			{
				std::vector<BonusTypes> aePrereqOrBonuses;
				bool bAnyReqFound = false;
				for (int i = 0; i < u.getNumPrereqOrBonuses(); i++)
				{
					if (pCity != NULL && pCity->hasBonus(u.getPrereqOrBonuses(i)))
					{
						bAnyReqFound = true;
						break;
					}
					aePrereqOrBonuses.push_back(u.getPrereqOrBonuses(i));
				}
				if (!bAnyReqFound && !aePrereqOrBonuses.empty())
				{
					szTempBuffer.Format(L"%s%s", NEWLINE, gDLL->getText("TXT_KEY_REQUIRES").c_str());
					bool bFirst = true;
					for (size_t i = 0; i < aePrereqOrBonuses.size(); i++)
					{
						setListHelp(szBuffer, szTempBuffer,
								GC.getInfo(u.getPrereqOrBonuses(i)).getDescription(),
								gDLL->getText("TXT_KEY_OR").c_str(), bFirst);
					}
					szBuffer.append(ENDCOLR);
				}
			} // </advc.004>
		}
	} /* <advc.004w> Show this right before the cost in Civilopedia text and
		 otherwise (i.e. in hover text) after the cost */
	if(bCivilopediaText)
	{
		setProductionSpeedHelp<ORDER_TRAIN>(szBuffer, eUnit, u.getSpecialUnitType(),
				pCity, true);
	} // </advc.004w>
	// advc.004y: Commented out
	//if (!bCivilopediaText && getActivePlayer() != NO_PLAYER)
	if (pCity == NULL)
	{
		if(u.getProductionCost() > 0 && !bCivilopediaText) // advc.004y
		{
			szTempBuffer.Format(L"%s%d%c", NEWLINE,
					// advc.004y:
					(getActivePlayer() == NO_PLAYER ? u.getProductionCost() :
					GET_PLAYER(ePlayer).getProductionNeeded(eUnit)),
					GC.getInfo(YIELD_PRODUCTION).getChar());
			szBuffer.append(szTempBuffer);
		}
	}
	else
	{
		szBuffer.append(NEWLINE);
		int iTurns = pCity->getProductionTurnsLeft(eUnit,
				(GC.ctrlKey() || !GC.shiftKey()) ? 0 : pCity->getOrderQueueLength());
		if (iTurns < MAX_INT) // advc.004x
		{
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_TURNS", iTurns));
				// advc: TXT_KEY_UNIT_TURNS takes only one argument
				//pCity->getProductionNeeded(eUnit), GC.getInfo(YIELD_PRODUCTION).getChar()));
			szBuffer.append(L" - "); // advc.004x: Moved up
		}
		int iProduction = pCity->getUnitProduction(eUnit);
		if (iProduction > 0)
		{
			szTempBuffer.Format(L"%d/%d%c", iProduction,
					pCity->getProductionNeeded(eUnit),
					GC.getInfo(YIELD_PRODUCTION).getChar());
			szBuffer.append(szTempBuffer);
			// BULL - Production Decay - start
			// advc.094: No separate ProductionDecayHover option
			if (BUGOption::isEnabled("CityScreen__ProductionDecayQueue", false) &&
				pCity->isActiveOwned()) // advc.094: Don't show this in foreign cities
			{
				setProductionDecayHelp(szBuffer, pCity->getUnitProductionDecayTurns(eUnit),
						// advc.094: No separate ProductionDecayHoverUnitThreshold option
						BUGOption::getValue("CityScreen__ProductionDecayQueueUnitThreshold", 5),
						pCity->getUnitProductionDecay(eUnit), pCity->getProductionUnit() == eUnit);
			} // BULL - Production Decay - end
		}
		else
		{
			szTempBuffer.Format(L"%d%c", pCity->getProductionNeeded(eUnit),
					GC.getInfo(YIELD_PRODUCTION).getChar());
			szBuffer.append(szTempBuffer);
		}
	}
	// <advc.004w> BonusProductionModifier moved into subroutine
	if(!bCivilopediaText)
	{
		setProductionSpeedHelp<ORDER_TRAIN>(szBuffer, eUnit, u.getSpecialUnitType(),
				pCity, false);
	} // </advc.004w>
	// <advc.001b>
	if(pCity != NULL &&
		GC.getDefineBOOL(CvGlobals::CAN_TRAIN_CHECKS_AIR_UNIT_CAP) &&
		pCity->getPlot().airUnitSpaceAvailable(pCity->getTeam()) < u.getAirUnitCap())
	{
		szTempBuffer.Format(L"%s%s", NEWLINE, gDLL->getText(
				"TXT_KEY_NOT_ENOUGH_SPACE").c_str());
		szBuffer.append(gDLL->getText("TXT_KEY_COLOR_NEGATIVE"));
		szBuffer.append(szTempBuffer);
		szBuffer.append(ENDCOLR);
	} // </advc.001b>

	// rfc: disable
	/*if (bStrategyText)
	{
		if (!CvWString(u.getStrategy()).empty())
		{
			if ((ePlayer == NO_PLAYER) || GET_PLAYER(ePlayer).isOption(PLAYEROPTION_ADVISOR_HELP))
			{
				szBuffer.append(SEPARATOR);
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_SIDS_TIPS"));
				szBuffer.append(L'\"');
				szBuffer.append(u.getStrategy());
				szBuffer.append(L'\"');
			}
		}
	}*/

	// doc (edead): replaced with unit buttons
	/*if (bCivilopediaText)
	{
		if (eDefaultUnit == eUnit)
		{
			FOR_EACH_ENUM(Unit)
			{
				if (eLoopUnit != eUnit &&
					eUnitClass == GC.getInfo(eLoopUnit).getUnitClassType())
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_REPLACED_BY_UNIT",
							GC.getInfo(eLoopUnit).getTextKeyWide()));
				}
			}
		}
	}*/

	if (pCity != NULL)
	{
		if (/*(gDLL->getChtLvl() > 0)*/ GC.getGame().isDebugMode() && // advc.135c
			GC.ctrlKey())
		{
			szBuffer.append(NEWLINE);
			for (int iUnitAI = 0; iUnitAI < NUM_UNITAI_TYPES; iUnitAI++)
			{
				int iTempValue = GET_PLAYER(pCity->getOwner()).AI_unitValue(eUnit,
						(UnitAITypes)iUnitAI, pCity->area());
				if (iTempValue != 0)
				{
					CvWString szTempString;
					getUnitAIString(szTempString, (UnitAITypes)iUnitAI);
					szBuffer.append(CvWString::format(L"(%s : %d) ",
							szTempString.GetCString(), iTempValue));
				}
			}
		}
	}
}

/*	BUG - Building Actual Effects - start
	Appends the actual (i.e. absolute) effects of adding eBuilding to pCity */
void CvGameTextMgr::setBuildingNetEffectsHelp(CvWStringBuffer &szBuffer,
	BuildingTypes eBuilding, CvCity const* pCity)
{
	if (pCity == NULL)
		return; // advc

	bool bStarted = false;
	CvWString szStart;
	szStart.Format(L"\n"SETCOLR L"(%s", TEXT_COLOR("COLOR_LIGHT_GREY"),
			gDLL->getText("TXT_KEY_ACTUAL_EFFECTS").GetCString());

	// Defense
	int iDefense = pCity->getAdditionalDefenseByBuilding(eBuilding);
	bStarted = setValueChangeHelp(szBuffer, szStart, L": ", L"",
			iDefense, gDLL->getSymbolID(DEFENSE_CHAR), true, false, bStarted);

	// Happiness
	int iGood = 0;
	int iBad = 0;
	pCity->getAdditionalHappinessByBuilding(eBuilding, iGood, iBad);
	/*int iAngryPop = pCity->getAdditionalAngryPopuplation(iGood, iBad);
	bStarted = setValueChangeHelp(szBuffer, szStart, L": ", L"", iAngryPop, gDLL->getSymbolID(ANGRY_POP_CHAR), false, bNewLine, bStarted);*/
	bStarted = setGoodBadChangeHelp(szBuffer, szStart, L": ", L"",
			iGood, gDLL->getSymbolID(HAPPY_CHAR), iBad,
			gDLL->getSymbolID(UNHAPPY_CHAR), false, false, bStarted);

	// Health
	iGood = 0;
	iBad = 0;
	pCity->getAdditionalHealthByBuilding(eBuilding, iGood, iBad);
	/*int iSpoiledFood = pCity->getAdditionalSpoiledFood(iGood, iBad);
	int iStarvation = pCity->getAdditionalStarvation(iSpoiledFood);
	/*bStarted = setValueChangeHelp(szBuffer, szStart, L": ", L"", iSpoiledFood, gDLL->getSymbolID(EATEN_FOOD_CHAR), false, false, bStarted);
	bStarted = setValueChangeHelp(szBuffer, szStart, L": ", L"", iStarvation, gDLL->getSymbolID(BAD_FOOD_CHAR), false, false, bStarted);*/
	bStarted = setGoodBadChangeHelp(szBuffer, szStart, L": ", L"",
			iGood, gDLL->getSymbolID(HEALTHY_CHAR), iBad,
			gDLL->getSymbolID(UNHEALTHY_CHAR), false, false, bStarted);

	// Yield
	int aiYields[NUM_YIELD_TYPES];
	FOR_EACH_ENUM(Yield)
	{
		aiYields[eLoopYield] = pCity->getAdditionalYieldByBuilding(
				eLoopYield, eBuilding);
	}
	bStarted = setYieldChangeHelp(szBuffer, szStart, L": ", L"",
			aiYields, false, false, bStarted);

	// Commerce
	int aiCommerces[NUM_COMMERCE_TYPES];
	FOR_EACH_ENUM(Commerce)
	{
		aiCommerces[eLoopCommerce] = pCity->getAdditionalCommerceTimes100ByBuilding(
				eLoopCommerce, eBuilding);
	}
	// Maintenance - add to gold
	aiCommerces[COMMERCE_GOLD] += pCity->getSavedMaintenanceTimes100ByBuilding(eBuilding);
	bStarted = setCommerceTimes100ChangeHelp(szBuffer, szStart, L": ", L"",
			aiCommerces, false, bStarted);

	// Great People
	int iGreatPeopleRate = pCity->getAdditionalGreatPeopleRateByBuilding(eBuilding);
	bStarted = setValueChangeHelp(szBuffer, szStart, L": ", L"",
			iGreatPeopleRate, gDLL->getSymbolID(GREAT_PEOPLE_CHAR), false, false, bStarted);

	if (bStarted)
		szBuffer.append(L")" ENDCOLR);
}


void CvGameTextMgr::setBuildingHelp(CvWStringBuffer &szBuffer, BuildingTypes eBuilding,
	bool bCivilopediaText, bool bStrategyText, bool bTechChooserText, CvCity* pCity)
{	// Call new function below without displaying actual effects.
	setBuildingHelpActual(szBuffer, eBuilding, bCivilopediaText, bStrategyText, bTechChooserText, pCity, false);
}

// New function, with option to display actual effects.
void CvGameTextMgr::setBuildingHelpActual(CvWStringBuffer &szBuffer,
	BuildingTypes eBuilding, bool bCivilopediaText, bool bStrategyText,
	bool bTechChooserText, CvCity* pCity, bool bActual)
// BUG - Building Actual Effects - end
{
	PROFILE_FUNC();

	if(NO_BUILDING == eBuilding)
		return; // advc

	CvWString szFirstBuffer;
	CvWString szTempBuffer;

	// <advc>
	CvGame const& kGame = GC.getGame();
	CvBuildingInfo const& kBuilding = GC.getInfo(eBuilding);
	PlayerTypes ePlayer = NO_PLAYER;
	if(pCity != NULL)
		ePlayer = pCity->getOwner();
	else ePlayer = getActivePlayer();
	BuildingClassTypes const eBuildingClass = kBuilding.getBuildingClassType();
	if(eBuildingClass == NO_BUILDINGCLASS)
		return;
	CvBuildingClassInfo const& kBuildingClass = GC.getInfo(eBuildingClass);
	/*  ePlayer is NO_PLAYER if Civilopedia accessed from opening menu.
		(bCivilopediaText is true when help text for a Civilpedia article is being
		composed; false for Civilopedia hover text and all non-Civilopedia texts.) */
	CvPlayer const* pPlayer = (ePlayer == NO_PLAYER ? NULL : &GET_PLAYER(ePlayer));
	//if(!bCivilopediaText && ePlayer != NO_PLAYER)
	if (!bCivilopediaText) // </advc>
	{
		szTempBuffer.Format( SETCOLR L"<link=literal>%s</link>" ENDCOLR,
				TEXT_COLOR("COLOR_BUILDING_TEXT"), kBuilding.getDescription());
		szBuffer.append(szTempBuffer);
	}

	// <advc.004w>
	bool bInBuildingList = false;
	if(!bCivilopediaText && pCity != NULL &&
		pCity->getNumBuilding(eBuilding) >= GC.getDefineINT(CvGlobals::CITY_MAX_NUM_BUILDINGS))
	{
		bInBuildingList = true;
	}
	bool bObsolete = true;
	if (pPlayer != NULL)
		bObsolete = GET_TEAM(ePlayer).isObsoleteBuilding(eBuilding);
	CvWString szObsoleteWithTag = bObsolete ? L"TXT_KEY_BUILDING_OBSOLETE_WITH" :
			L"TXT_KEY_BUILDING_NOT_OBSOLETE";
	// </advc.004w>
	{
		/*if (NULL != pCity)
			iHappiness = pCity->getBuildingHappiness(eBuilding);
		else iHappiness = kBuilding.getHappiness();*/ // BtS
		/*  K-Mod, 30/dec/10, karadoc
			changed so that conditional happiness is not double-reported.
			(such as happiness from state-religion buildings, or culture slider) */
		int iHappiness = kBuilding.getHappiness();
		if (pCity != NULL)
		{
			/*	special modifiers (eg. events). These don't get their own line of text,
				so they need to be included here. */
			iHappiness += pCity->getBuildingHappyChange(eBuildingClass);
			iHappiness += pPlayer->getExtraBuildingHappiness(eBuilding);
			/*	'Extra building happiness' includes happiness from several sources, including
				events, civics, traits, and boosts from other buildings.
				My aim here is to only include in the total what isn't already in the
				list of bonuses below. As far as I know the only thing that would
				be double-reported is the civic happiness. So I'll subtract that. */
			FOR_EACH_ENUM(Civic)
			{
				if (pPlayer->isCivic(eLoopCivic))
				{
					iHappiness -= GC.getInfo(eLoopCivic).
							getBuildingHappinessChanges(eBuildingClass);
				}
			}
		} // K-Mod end
		if (iHappiness != 0)
		{
			szTempBuffer.Format(L", +%d%c", abs(iHappiness), iHappiness > 0 ?
					gDLL->getSymbolID(HAPPY_CHAR) :
					gDLL->getSymbolID(UNHAPPY_CHAR));
			szBuffer.append(szTempBuffer);
		}
	}
	{
		/*if (NULL != pCity)
			iHealth = pCity->getBuildingGoodHealth(eBuilding);
		else {
			iHealth = kBuilding.getHealth();
			if (ePlayer != NO_PLAYER) {
				if (eBuilding == GC.getInfo(GET_PLAYER(ePlayer).getCivilizationType()).getCivilizationBuildings(kBuilding.getBuildingClassType()))
					iHealth += GET_PLAYER(ePlayer).getExtraBuildingHealth(eBuilding);
			}
		}
		if (iHealth != 0) {
			szTempBuffer.Format(L", +%d%c", abs(iHealth), ((iHealth > 0) ? gDLL->getSymbolID(HEALTHY_CHAR): gDLL->getSymbolID(UNHEALTHY_CHAR)));
			szBuffer.append(szTempBuffer);
		}
		iHealth = 0;
		if (NULL != pCity)
			iHealth = pCity->getBuildingBadHealth(eBuilding);*/ // BtS
		/*  K-Mod, 30/dec/10, karadoc
			changed so that conditional healthiness is not counted.
			(such as healthiness from public transport with environmentalism) */
		int iHealth = kBuilding.getHealth();
		if (pCity != NULL)
		{
			// special modifiers (eg. events). These modifiers don't get their own line of text, so they need to be included here.
			iHealth += pCity->getBuildingHealthChange(eBuildingClass);
			iHealth += pPlayer->getExtraBuildingHealth(eBuilding);

			// doc: Indian UP: +1 health for buildings that provide happiness
			if (eCivilization == INDIA && kBuilding.getHappiness() > 0)
				iHealth += 1M

			// We need to subtract any civic bonuses from 'extra building health', so as not to double-report. (see comments for the happiness section.)
			FOR_EACH_ENUM(Civic)
			{
				if (pPlayer->isCivic(eLoopCivic))
				{
					iHealth -= GC.getInfo(eLoopCivic).
							getBuildingHealthChanges(eBuildingClass);
				}
			}
		} // K-Mod end
		if (iHealth != 0)
		{
			szTempBuffer.Format(L", +%d%c", abs(iHealth), iHealth > 0 ?
					gDLL->getSymbolID(HEALTHY_CHAR) :
					gDLL->getSymbolID(UNHEALTHY_CHAR));
			szBuffer.append(szTempBuffer);
		}
	}
	int aiYields[NUM_YIELD_TYPES];
	FOR_EACH_ENUM(Yield)
	{
		aiYields[eLoopYield] = kBuilding.getYieldChange(eLoopYield);
		if (pCity != NULL)
		{
			aiYields[eLoopYield] += pCity->getBuildingYieldChange(
					eBuildingClass, eLoopYield);

			// doc: improved bonus yield change
			FOR_EACH_ENUM(Bonus)
			{
				aiYields[eLoopYield] += kBuilding.getBonusYieldChange(eLoopBonus, eLoopYield) * pCity->countNumBonusPlots(eLoopBonus);
			}
		}
	}
	setYieldChangeHelp(szBuffer, L", ", L"", L"", aiYields, false, false);

	int aiCommerces[NUM_COMMERCE_TYPES];
	FOR_EACH_ENUM2(Commerce, e)
	{
		if (pCity != NULL && pCity->getNumBuilding(eBuilding) > 0)
			aiCommerces[e] = pCity->getBuildingCommerceByBuilding(e, eBuilding);
		else
		{
			aiCommerces[e] = kBuilding.getCommerceChange(e);
			aiCommerces[e] += kBuilding.getObsoleteSafeCommerceChange(e);
			// K-Mod, 30/dec/10: added religious building bonus info
			if (ePlayer != NO_PLAYER && /* advc: */ !bCivilopediaText &&
				kBuilding.getReligionType() != NO_RELIGION &&
				kBuilding.getReligionType() == pPlayer->getStateReligion())
			{
				aiCommerces[e] += pPlayer->getStateReligionBuildingCommerce(e);
			} // K-Mod end
		}
	}
	setCommerceChangeHelp(szBuffer, L", ", L"", L"", aiCommerces, false, false);
	setYieldChangeHelp(szBuffer,
			bCivilopediaText ? L"" : L", ", // advc (was treated separately below)
			L"", L"", kBuilding.getYieldModifier(), true, bCivilopediaText);
	setCommerceChangeHelp(szBuffer,
			bCivilopediaText ? L"" : L", ", // advc (was treated separately below)
			L"", L"", kBuilding.getCommerceModifier(), true, bCivilopediaText);

	// doc: include city specific building great people rate change
	int iTotalGreatPeopleRateChange = kBuilding.getGreatPeopleRateChange();
	if (pCity != NULL)
		iTotalGreatPeopleRateChange += pCity->getBuildingGreatPeopleRateChange(eBuildingClassType)
	if (iTotalGreatPeopleRateChange != 0)
	{
		szTempBuffer.Format(
				(bInBuildingList ? L"\n%s%d%c" : // advc.004w: Doesn't fit in one line
				L", %s%d%c"), (iTotalGreatPeopleRateChange > 0) ? "+" : "",
				iTotalGreatPeopleRateChange, gDLL->getSymbolID(GREAT_PEOPLE_CHAR));
		szBuffer.append(szTempBuffer);
		UnitClassTypes eGPClass = kBuilding.getGreatPeopleUnitClass(); // advc
		if (eGPClass != NO_UNITCLASS)
		{
			UnitTypes eGreatPeopleUnit = NO_UNIT; // advc
			if (ePlayer != NO_PLAYER)
				eGreatPeopleUnit = pPlayer->getCivilization().getUnit(eGPClass);
			else eGreatPeopleUnit = GC.getInfo(eGPClass).getDefaultUnit();

			if (eGreatPeopleUnit != NO_UNIT)
			{
				szTempBuffer.Format(L" (%s)", GC.getInfo(eGreatPeopleUnit).getDescription());
				szBuffer.append(szTempBuffer);
			}
		}
	}

	// test for unique building
	BuildingTypes eDefaultBuilding = GC.getInfo(eBuildingClass).getDefaultBuilding();

	if (eDefaultBuilding != eBuilding && /* advc.004w: */ !bInBuildingList)
	{
		FOR_EACH_ENUM(Civilization)
		{
			BuildingTypes eUniqueBuilding = GC.getInfo(eLoopCivilization).
					getCivilizationBuildings(eBuildingClass);
			if (eUniqueBuilding == eBuilding &&
				!GC.getInfo(eUniqueBuilding).isGraphicalOnly()) // doc: exclude graphical only
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_UNIQUE_BUILDING",
						GC.getInfo(eLoopCivilization).getTextKeyWide()));
			}
		}
		// advc.003l: Moved from the enclosing conditional
		if (eDefaultBuilding != NO_BUILDING)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_REPLACES_UNIT",
					GC.getInfo(eDefaultBuilding).getTextKeyWide()));
		}
	}

	if (bCivilopediaText ||
		ePlayer == NO_PLAYER) // advc: Civilopedia from opening menu
	{	// advc: Already done higher up
		/*setYieldChangeHelp(szBuffer, L"", L"", L"", kBuilding.getYieldModifierArray(), true, bCivilopediaText);
		setCommerceChangeHelp(szBuffer, L"", L"", L"", kBuilding.getCommerceModifierArray(), true, bCivilopediaText);*/
	}
	else
	{
		// <advc.004w> Either already constructed in pCity, or queued.
		bool bConstruct = false;
		if(pCity != NULL)
		{
			if(bInBuildingList)
				bConstruct = true;
			else
			{
				for(CLLNode<OrderData>* pNode = pCity->headOrderQueueNode();
					pNode != NULL; pNode = pCity->nextOrderQueueNode(pNode))
				{
					if(pNode->m_data.eOrderType != ORDER_CONSTRUCT)
						continue;
					if(pNode->m_data.iData1 == eBuilding)
					{
						bConstruct = true;
						break;
					}
				}
			}
		}
		if(kBuilding.isWorldWonder())
		{
			szBuffer.append(NEWLINE); // Newline in any case
			int iMaxGlobal = kBuildingClass.getMaxGlobalInstances();
			if(pCity == NULL)
			{
				if(iMaxGlobal == 1)
					szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_WORLD_WONDER1"));
				else szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_WORLD_WONDER_ALLOWED",
						iMaxGlobal)); // </advc.004w>
			}
			else  // <advc.004w>
			{
				iMaxGlobal -= (kGame.getBuildingClassCreatedCount(eBuildingClass) +
						GET_TEAM(ePlayer).getBuildingClassMaking(eBuildingClass));
				if(iMaxGlobal == 1 || (iMaxGlobal == 0 && bConstruct))
					szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_WORLD_WONDER1"));
				else
				{
					if(!bConstruct)
						szBuffer.append(gDLL->getText("TXT_KEY_COLOR_NEGATIVE"));
					szBuffer.append(gDLL->getText(
							"TXT_KEY_BUILDING_WORLD_WONDER_LEFT", iMaxGlobal));
					if(!bConstruct)
						szBuffer.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));
				} // </advc.004w>
			}
		}
		if (kBuilding.isTeamWonder())  // <advc.004w>
		{
			szBuffer.append(NEWLINE); // Newline in any case
			int iMaxTeam = kBuildingClass.getMaxTeamInstances();
			if(pCity == NULL)
			{
				if(iMaxTeam == 1)
					szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_TEAM_WONDER1"));
				else
				{
					if(!bConstruct)
						szBuffer.append(gDLL->getText("TXT_KEY_COLOR_NEGATIVE"));
					szBuffer.append(gDLL->getText(
							"TXT_KEY_BUILDING_TEAM_WONDER_ALLOWED", iMaxTeam));
					if(!bConstruct)
						szBuffer.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));
				} // </advc.004w>
			}
			else // <advc.004w>
			{
				iMaxTeam -= GET_TEAM(ePlayer).getBuildingClassCountPlusMaking(
						eBuildingClass);
				if(iMaxTeam == 1)
					szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_TEAM_WONDER1"));
				else
				{
					if(!bConstruct)
						szBuffer.append(gDLL->getText("TXT_KEY_COLOR_NEGATIVE"));
					szBuffer.append(gDLL->getText(
							"TXT_KEY_BUILDING_TEAM_WONDER_LEFT", iMaxTeam));
					if(!bConstruct)
						szBuffer.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));
				} // </advc.004w>
			}
		}
		if (kBuilding.isNationalWonder() &&
			// <advc.004w> Palace isn't really a National Wonder
			!kBuilding.isCapital() &&
			// That case is handled below; no need for "0 left" in addition.
			(pCity == NULL || !pCity->isNationalWondersMaxed() || bConstruct))
		{
			szBuffer.append(NEWLINE); // Newline in any case
			int iMaxPlayer = kBuildingClass.getMaxPlayerInstances();
			if(pCity == NULL)
			{
				if(iMaxPlayer == 1)
					szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_NATIONAL_WONDER1"));
				else szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_NATIONAL_WONDER_ALLOWED",
						iMaxPlayer)); // </advc.004w>
			}
			else // <advc.004w>
			{
				iMaxPlayer -= pPlayer->getBuildingClassCountPlusMaking(eBuildingClass);
				/*  This would be the same behavior as for great wonders, but I
					want to show "0 left" only if the wonder is being built
					elsewhere; otherwise, show how many more national wonders
					the city can build. */
				/*if(iMaxPlayer == 1)
					szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_NATIONAL_WONDER1"));
				else szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_NATIONAL_WONDER_LEFT",
						iMaxPlayer)); */
				if(iMaxPlayer <= 0 && !bConstruct)
				{
					szBuffer.append(gDLL->getText("TXT_KEY_COLOR_NEGATIVE"));
					szBuffer.append(gDLL->getText(
							"TXT_KEY_BUILDING_NATIONAL_WONDER_LEFT", iMaxPlayer));
					szBuffer.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));
				}
				else
				{
					iMaxPlayer = pCity->getNumNationalWondersLeft();
					if(iMaxPlayer < 0)
						szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_NATIONAL_WONDER1"));
					else
					{
						szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_NATIONAL_WONDER_LEFT",
								iMaxPlayer));
					}
				} // </advc.004w>
			}
		}
	}
	{
		ReligionTypes const eGlobalCommerceReligion = kBuilding.getGlobalReligionCommerce();
		if (eGlobalCommerceReligion != NO_RELIGION)
		{
			szFirstBuffer = gDLL->getText("TXT_KEY_BUILDING_PER_CITY_WITH",
					GC.getInfo(eGlobalCommerceReligion).getChar());
			setCommerceChangeHelp(szBuffer, L"", L"", szFirstBuffer,
					GC.getInfo(eGlobalCommerceReligion).getGlobalReligionCommerceArray());
		}
	}
	// <advc.179>
	if(!bCivilopediaText && ePlayer != NO_PLAYER)
		buildBuildingReligionYieldString(szBuffer, kBuilding); // </advc.179>
	{
		CorporationTypes eFoundsCorp = kBuilding.getFoundsCorporation();
		if (eFoundsCorp != NO_CORPORATION &&
			!bInBuildingList) // advc.004w
		{
			szBuffer.append(NEWLINE);
			// <advc.001>
			CvWString szCorpLink;
			setCorporationLink(szCorpLink, eFoundsCorp); // </advc.001>
			szBuffer.append(gDLL->getText("TXT_KEY_FOUNDS_CORPORATION",
					//GC.getInfo(eFoundsCorp).getTextKeyWide()
					szCorpLink.c_str())); // advc.001
		}
	}
	{
		CorporationTypes const eGlobalCommerceCorp = kBuilding.getGlobalCorporationCommerce();
		if (eGlobalCommerceCorp != NO_CORPORATION)
		{
			szFirstBuffer = gDLL->getText("TXT_KEY_BUILDING_PER_CITY_WITH",
					GC.getInfo(eGlobalCommerceCorp).getChar());
			setCommerceChangeHelp(szBuffer, L"", L"", szFirstBuffer,
					GC.getInfo(eGlobalCommerceCorp).getHeadquarterCommerceArray());
		}
	}
	if (kBuilding.getNoBonus() != NO_BONUS)
	{
		CvBonusInfo& kBonus = GC.getInfo(kBuilding.getNoBonus());
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_DISABLES",
				kBonus.getTextKeyWide(), kBonus.getChar()));
	}

	if (kBuilding.getFreeBonus() != NO_BONUS)
	{
		szBuffer.append(NEWLINE);
		CvBonusInfo const& kFreeBonus = GC.getInfo(kBuilding.getFreeBonus());
		// <advc.004y>
		bool bRange = (ePlayer == NO_PLAYER);
		if(bRange)
		{
			int iLow = GC.getInfo((WorldSizeTypes)
					0).getNumFreeBuildingBonuses();
			int iHigh = GC.getInfo((WorldSizeTypes)
					(GC.getNumWorldInfos() - 1)).getNumFreeBuildingBonuses();
			if(iHigh == iLow)
				bRange = false;
			else
			{
				szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_PROVIDES_RANGE",
						iLow, iHigh, kFreeBonus.getTextKeyWide(), kFreeBonus.getChar()));
			}
		}
		if(!bRange) // </advc.004y>
		{
			szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_PROVIDES",
					kGame.getNumFreeBonuses(eBuilding), kFreeBonus.getTextKeyWide(),
					kFreeBonus.getChar()));
		}
		if (kFreeBonus.getHealth() != 0)
		{
			szTempBuffer.Format(L", +%d%c", abs(kFreeBonus.getHealth()),
					(kFreeBonus.getHealth() > 0 ? gDLL->getSymbolID(HEALTHY_CHAR) :
					gDLL->getSymbolID(UNHEALTHY_CHAR)));
			szBuffer.append(szTempBuffer);
		}

		if (kFreeBonus.getHappiness() != 0)
		{
			szTempBuffer.Format(L", +%d%c", abs(kFreeBonus.getHappiness()),
					(kFreeBonus.getHappiness() > 0 ? gDLL->getSymbolID(HAPPY_CHAR) :
					gDLL->getSymbolID(UNHAPPY_CHAR)));
			szBuffer.append(szTempBuffer);
		}
	}
	BuildingClassTypes eFreeBuildingClass = kBuilding.getFreeBuildingClass();
	if (eFreeBuildingClass != NO_BUILDINGCLASS)
	{
		BuildingTypes eFreeBuilding;
		if (ePlayer != NO_PLAYER)
			eFreeBuilding = pPlayer->getCivilization().getBuilding(eFreeBuildingClass);
		else eFreeBuilding = GC.getInfo(eFreeBuildingClass).getDefaultBuilding();
		if (NO_BUILDING != eFreeBuilding)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_FREE_IN_CITY",
					GC.getInfo(eFreeBuilding).getTextKeyWide()));
		}
	}

	if (kBuilding.getFreePromotion() != NO_PROMOTION)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_FREE_PROMOTION",
				GC.getInfo(kBuilding.getFreePromotion()).getTextKeyWide()));
	}

	if (kBuilding.getCivicOption() != NO_CIVICOPTION)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_ENABLES_CIVICS",
				GC.getInfo(kBuilding.getCivicOption()).getTextKeyWide()));
	}

	if (kBuilding.isPower())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_PROVIDES_POWER"));

		/*if (kBuilding.isDirtyPower() && (GC.getDefineINT(CvGlobals::DIRTY_POWER_HEALTH_CHANGE) != 0)) {
			szTempBuffer.Format(L" (+%d%c)", abs(GC.getDefineINT(CvGlobals::DIRTY_POWER_HEALTH_CHANGE)), ((GC.getDefineINT(CvGlobals::DIRTY_POWER_HEALTH_CHANGE) > 0) ? gDLL->getSymbolID(HEALTHY_CHAR): gDLL->getSymbolID(UNHEALTHY_CHAR)));
			szBuffer.append(szTempBuffer);
		}*/ // BtS
		// K-Mod. Also include base health change from power.
		int iPowerHealth = GC.getDefineINT(CvGlobals::POWER_HEALTH_CHANGE) +
				(!kBuilding.isDirtyPower() ? 0 :
				GC.getDefineINT(CvGlobals::DIRTY_POWER_HEALTH_CHANGE));
		if (iPowerHealth)
		{
			szTempBuffer.Format(L" (+%d%c)", abs(iPowerHealth), iPowerHealth > 0 ?
					gDLL->getSymbolID(HEALTHY_CHAR) : gDLL->getSymbolID(UNHEALTHY_CHAR));
			szBuffer.append(szTempBuffer);
		} // K-Mod end
	}

	if (kBuilding.isAreaCleanPower())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_PROVIDES_AREA_CLEAN_POWER"));
	}

	// doc: change great wall effect (but keep attribute for graphics)
	/*if (kBuilding.isAreaBorderObstacle())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_BORDER_OBSTACLE"));
	}*/

	// (advc.179: Triggered Election, Eligibility text moved down)

	if (kBuilding.isCapital())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_CAPITAL"));
	}

	if (kBuilding.isGovernmentCenter())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_REDUCES_MAINTENANCE"));
	}

	if (kBuilding.isGoldenAge() /* advc.004w: */ && !bInBuildingList)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_GOLDEN_AGE"));
	}

	if (kBuilding.isAllowsNukes())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_ENABLES_NUKES"));
	}

	if (kBuilding.isMapCentering() /* advc.004w: */ && !bInBuildingList)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_CENTERS_MAP"));
	}

	if (kBuilding.isNoUnhappiness())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_NO_UNHAPPY"));
	}
	/*if (kBuilding.isNoUnhealthyPopulation()) {
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_NO_UNHEALTHY_POP"));
	}*/ // BtS
	// K-Mod, 27/dec/10: replaced with UnhealthyPopulationModifier
	if (kBuilding.getUnhealthyPopulationModifier() != 0)
	{
		// If the modifier is less than -100, display the old NoUnhealth. text
		// Note: this could be techinically inaccurate if we combine this modifier with a positive modifier
		if (kBuilding.getUnhealthyPopulationModifier() <= -100)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_CIVIC_NO_POP_UNHEALTHY"));
		}
		else
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNHEALTHY_POP_MODIFIER",
					kBuilding.getUnhealthyPopulationModifier()));
		}
	} // K-Mod end

	if (kBuilding.isBuildingOnlyHealthy())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_NO_UNHEALTHY_BUILDINGS"));
	}

	// doc: no resistance
	if (kBuilding.isNoResistance())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_NO_RESISTANCE"));
	}

	// doc: unhealth modifier
	if (kBuilding.getBuildingUnhealthModifier() != 0)
	{
		szBuffer.append(NEWLINE);
		szTempBuffer.Format(L"%s%d",
				kBuilding.getBuildingUnhealthModifier() > 0 ? L"+" : L"", kBuilding.getBuildingUnhealthModifier());
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_BUILDING_UNHEALTH_MODIFIER",
				szTempBuffer.c_str()));
	}

	// doc: corporation unhealth modifier
	if (kBuilding.getCorporationUnhealthModifier() != 0)
	{
		szBuffer.append(NEWLINE);
		szTempBuffer.Format(L"%s%d",
				kBuilding.getCorporationUnhealthModifier() > 0 ? L"+" : L"", kBuilding.getCorporationUnhealthModifier());
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_CORPORATION_UNHEALTH_MODIFIER",
				szTempBuffer.c_str()));
	}

	if (kBuilding.getGreatPeopleRateModifier() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_BIRTH_RATE_MOD",
				kBuilding.getGreatPeopleRateModifier()));
	}

	// doc: culture level great people rate modifer
	if (kBuilding.getCultureGreatPeopleRateModifier() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_CULTURE_BIRTH_RATE_MOD",
				kBuilding.getCultureGreatPeopleRateModifier()));
	}

	if (kBuilding.getGreatGeneralRateModifier() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_GENERAL_RATE_MOD",
				kBuilding.getGreatGeneralRateModifier()));
	}

	if (kBuilding.getDomesticGreatGeneralRateModifier() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_DOMESTIC_GREAT_GENERAL_MODIFIER",
				kBuilding.getDomesticGreatGeneralRateModifier()));
	}

	if (kBuilding.getGlobalGreatPeopleRateModifier() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_BIRTH_RATE_MOD_ALL_CITIES",
				kBuilding.getGlobalGreatPeopleRateModifier()));
	}

	if (kBuilding.getAnarchyModifier() != 0)
	{
		if (-100 == kBuilding.getAnarchyModifier())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_NO_ANARCHY"));
		}
		else
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_ANARCHY_MOD",
					kBuilding.getAnarchyModifier()));

			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_ANARCHY_TIMER_MOD",
					kBuilding.getAnarchyModifier()));
		}
	}

	if (kBuilding.getGoldenAgeModifier() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_GOLDENAGE_MOD",
				kBuilding.getGoldenAgeModifier()));
	}

	if (kBuilding.getGlobalHurryModifier() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_HURRY_MOD",
				kBuilding.getGlobalHurryModifier()));
	}

	if (kBuilding.getFreeExperience() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_FREE_XP_UNITS",
				kBuilding.getFreeExperience()));
	}

	if (kBuilding.getGlobalFreeExperience() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_FREE_XP_ALL_CITIES",
				kBuilding.getGlobalFreeExperience()));
	}
	{
		int iFoodKept = (pPlayer == NULL ?
				kBuilding.getFoodKept() :
				pPlayer->getFoodKept(eBuilding)); // advc.912d
		if (iFoodKept != 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_STORES_FOOD", iFoodKept));
		}
	}
	if (kBuilding.getAirlift() > 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_AIRLIFT",
				kBuilding.getAirlift()));
	}

	if (kBuilding.getAirModifier() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_AIR_DAMAGE_MOD",
				kBuilding.getAirModifier()));
	}

	if (kBuilding.getAirUnitCapacity() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_AIR_UNIT_CAPACITY",
				kBuilding.getAirUnitCapacity()));
	}

	if (kBuilding.getNukeModifier() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_NUKE_DAMAGE_MOD",
				kBuilding.getNukeModifier()));
	}
	{
		int const iMeltdownRand = kBuilding.getNukeExplosionRand();
		if (iMeltdownRand > 0 &&
			// <advc.652> Don't show chance when building not operated
			(pCity == NULL || pCity->getNumBuilding(eBuilding) <= 0 ||
			(pCity->isMeltdownBuilding(eBuilding) &&
			!pCity->isMeltdownBuildingSuperseded(eBuilding))))
		{
			szBuffer.append(NEWLINE);
			float fPermilleChance = 1000.f / kBuilding.getNukeExplosionRand();
			szTempBuffer.Format(L"%.2g", fPermilleChance); // </advc.652>
			szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_NUKE_EXPLOSION_CHANCE",
					szTempBuffer.c_str())); // advc.652
		}
	}
	if (kBuilding.getFreeSpecialist() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_FREE_SPECIALISTS",
				kBuilding.getFreeSpecialist()));
	}

	if (kBuilding.getAreaFreeSpecialist() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_FREE_SPECIALISTS_CONT",
				kBuilding.getAreaFreeSpecialist()));
	}

	if (kBuilding.getGlobalFreeSpecialist() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_FREE_SPECIALISTS_ALL_CITIES",
				kBuilding.getGlobalFreeSpecialist()));
	}

	if (kBuilding.getMaintenanceModifier() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_MAINT_MOD",
				kBuilding.getMaintenanceModifier()));
	}

	if (kBuilding.getHurryAngerModifier() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_HURRY_ANGER_MOD",
				kBuilding.getHurryAngerModifier()));
		// <advc.912d>
		if(ePlayer != NO_PLAYER && kGame.isOption(GAMEOPTION_NO_SLAVERY) &&
			kBuilding.getHurryAngerModifier() < 0 && GET_PLAYER(ePlayer).isHuman())
		{
			szBuffer.append(NEWLINE);
			szTempBuffer.Format(L"%c", gDLL->getSymbolID(BULLET_CHAR));
			szBuffer.append(szTempBuffer);
			szBuffer.append(gDLL->getText("TXT_KEY_HURRY_POPULATION"));
		} // </advc.912d>
	}

	if (kBuilding.getWarWearinessModifier() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_WAR_WEAR_MOD",
				kBuilding.getWarWearinessModifier()));
	}

	if (kBuilding.getGlobalWarWearinessModifier() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_WAR_WEAR_MOD_ALL_CITIES",
				kBuilding.getGlobalWarWearinessModifier()));
	}

	if (kBuilding.getEnemyWarWearinessModifier() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_ENEMY_WAR_WEAR",
				kBuilding.getEnemyWarWearinessModifier()));
	}

	if (kBuilding.getHealRateChange() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_HEAL_MOD",
				kBuilding.getHealRateChange()));
	}

	if (kBuilding.getAreaHealth() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_HEALTH_CHANGE_CONT",
				abs(kBuilding.getAreaHealth()), kBuilding.getAreaHealth() > 0 ?
					gDLL->getSymbolID(HEALTHY_CHAR) :
					gDLL->getSymbolID(UNHEALTHY_CHAR)));
	}

	if (kBuilding.getGlobalHealth() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_HEALTH_CHANGE_ALL_CITIES",
				abs(kBuilding.getGlobalHealth()), kBuilding.getGlobalHealth() > 0 ?
				gDLL->getSymbolID(HEALTHY_CHAR) :
				gDLL->getSymbolID(UNHEALTHY_CHAR)));
	}

	if (kBuilding.getAreaHappiness() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_HAPPY_CHANGE_CONT",
				// UNOFFICIAL_PATCH, Bugfix, 08/28/09, jdog5000 (start): Use absolute value with unhappy face
				abs(kBuilding.getAreaHappiness()), kBuilding.getAreaHappiness() > 0 ?
				gDLL->getSymbolID(HAPPY_CHAR) : gDLL->getSymbolID(UNHAPPY_CHAR))); // UNOFFICIAL_PATCH (end)
	}

	if (kBuilding.getGlobalHappiness() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_HAPPY_CHANGE_ALL_CITIES",
				// UNOFFICIAL_PATCH, Bugfix, 08/28/09, jdog5000 (start): Use absolute value with unhappy face
				abs(kBuilding.getGlobalHappiness()), kBuilding.getGlobalHappiness() > 0 ?
				gDLL->getSymbolID(HAPPY_CHAR) : gDLL->getSymbolID(UNHAPPY_CHAR))); // UNOFFICIAL_PATCH (end)
	}

	if (kBuilding.getStateReligionHappiness() != 0)
	{
		if (kBuilding.getReligionType() != NO_RELIGION)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_RELIGION_HAPPINESS",
					// UNOFFICIAL_PATCH, Bugfix, 08/28/09, jdog5000 (start): Use absolute value with unhappy face
					abs(kBuilding.getStateReligionHappiness()), kBuilding.getStateReligionHappiness() > 0 ?
					gDLL->getSymbolID(HAPPY_CHAR) : gDLL->getSymbolID(UNHAPPY_CHAR), // UNOFFICIAL_PATCH (end)
					GC.getInfo((ReligionTypes)kBuilding.getReligionType()).getChar()));
		}
	}

	if (kBuilding.getWorkerSpeedModifier() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_WORKER_MOD",
				kBuilding.getWorkerSpeedModifier()));
	}

	if (kBuilding.getMilitaryProductionModifier() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_MILITARY_MOD",
				kBuilding.getMilitaryProductionModifier()));
	}

	if (kBuilding.getSpaceProductionModifier() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_SPACESHIP_MOD",
				kBuilding.getSpaceProductionModifier()));
	}

	if (kBuilding.getGlobalSpaceProductionModifier() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_SPACESHIP_MOD_ALL_CITIES",
				kBuilding.getGlobalSpaceProductionModifier()));
	}

	if (kBuilding.getTradeRoutes() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_TRADE_ROUTES",
				kBuilding.getTradeRoutes()));
	}

	if (kBuilding.getCoastalTradeRoutes() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_COASTAL_TRADE_ROUTES",
				kBuilding.getCoastalTradeRoutes()));
	}

	if (kBuilding.getAreaTradeRoutes() != 0) // advc.310: Renamed; was iGlobalTradeRoutes.
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_TRADE_ROUTES_ALL_CITIES",
				kBuilding.getAreaTradeRoutes())); // advc.310
	}

	if (kBuilding.getTradeRouteModifier() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_TRADE_ROUTE_MOD",
				kBuilding.getTradeRouteModifier()));
	}

	// doc: culture level trade route modifier
	if (kBuilding.getCultureTradeRouteModifier() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_CULTURE_TRADE_ROUTE_MOD",
				kBuilding.getCultureTradeRouteModifier()));
	}

	if (kBuilding.getForeignTradeRouteModifier() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_FOREIGN_TRADE_ROUTE_MOD",
				kBuilding.getForeignTradeRouteModifier()));
	}

	if (kBuilding.getGlobalPopulationChange() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_GLOBAL_POP",
				kBuilding.getGlobalPopulationChange()));
	}

	if (kBuilding.getFreeTechs() != 0)
	{
		if (kBuilding.getFreeTechs() == 1)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_FREE_TECH"));
		}
		else
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_FREE_TECHS",
					kBuilding.getFreeTechs()));
		}
	}

	if (kBuilding.getDefenseModifier() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_DEFENSE_MOD",
				kBuilding.getDefenseModifier()));
	}
	// <advc.004c>
	if (kBuilding.get(CvBuildingInfo::RaiseDefense) > 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_DEFENSE_RAISE",
				kBuilding.get(CvBuildingInfo::RaiseDefense)));
	} // </advc.004c>

	if (kBuilding.getBombardDefenseModifier() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_BOMBARD_DEFENSE_MOD",
				-kBuilding.getBombardDefenseModifier()));
	}

	// doc: unignorable bombard defense modifier
	if (kBuilding.getUnignorableBombardDefenseModifier() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_UNIGNORABLE_BOMBARD_DEFENSE_MOD",
				-kBuilding.getUnignorableBombardDefenseModifier()));
	}

	if (kBuilding.getAllCityDefenseModifier() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_DEFENSE_MOD_ALL_CITIES",
				kBuilding.getAllCityDefenseModifier()));
	}

	if (kBuilding.getEspionageDefenseModifier() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_ESPIONAGE_DEFENSE_MOD",
				kBuilding.getEspionageDefenseModifier()));
		// UNOFFICIAL_PATCH, Bugfix, 12/07/09, Afforess & jdog5000: guard added
		if (kBuilding.getEspionageDefenseModifier() > 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_EXPOSE_SPIES"));
		}
	}

	setYieldChangeHelp(szBuffer, gDLL->getText("TXT_KEY_BUILDING_WATER_PLOTS").c_str(),
			L": ", L"", kBuilding.getSeaPlotYieldChange());

	setYieldChangeHelp(szBuffer, gDLL->getText("TXT_KEY_BUILDING_RIVER_PLOTS").c_str(),
			L": ", L"", kBuilding.getRiverPlotYieldChange());

	// doc: flat river yield change
	setYieldChangeHelp(szBuffer, gDLL->getText("TXT_KEY_BUILDING_FLAT_RIVER_PLOTS").c_str(),
			L": ", L"", kBuilding.getFlatRiverPlotYieldChangeArray());

	// doc: improved bonus yield change
	FOR_EACH_ENUM(Bonus)
	{
		szTempBuffer.Format(L"");
		bool bFound = false;
		FOR_EACH_ENUM(Yield)
		{
			if (kBuilding.getBonusYieldChange(eLoopBonus, eLoopYield) != 0)
			{
				if (bFound)
					szTempBuffer += L", ";
				szTempBuffer += CvWString::format(L"%s%d%c",
						kBuilding.getBonusYieldChange(eLoopBonus, eLoopYield) > 0 ? L"+" : L"",
								kBuilding.getBonusYieldChange(eLoopBonus, eLoopYield),
								GC.getYieldInfo(eLoopYield).getChar());
				bFound = true;
			}
		}

		if (bFound)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_IMPROVED_RESOURCE_YIELDS",
						szTempBuffer.c_str(),
						GC.getInfo(eLoopBonus).getText()));
		}
	}

	// doc: religion building yield change
	setYieldChangeHelp(szBuffer, gDLL->getText("TXT_KEY_BUILDING_RELIGION_BUILDINGS",
			(ePlayer == NO_PLAYER || GET_PLAYER(ePlayer).getStateReligion() == NO_RELIGION) ? gDLL->getSymbolID(RELIGION_CHAR) : GC.getReligionInfo(GET_PLAYER(ePlayer).getStateReligion()).getChar()).c_str(),
			L": ", L"", kBuilding.getReligionYieldChangeArray());

	setYieldChangeHelp(szBuffer, gDLL->getText("TXT_KEY_BUILDING_WATER_PLOTS_ALL_CITIES").c_str(),
			L": ", L"", kBuilding.getGlobalSeaPlotYieldChange());

	// doc: display clean or dirty power
	bool bCleanPower = pCity != NULL && pCity->isPower() && !pCity->isDirtyPower();
	setYieldChangeHelp(szBuffer, L"", L"",
			gDLL->getText(bCleanPower ? "TXT_KEY_BUILDING_WITH_CLEAN_POWER" : "TXT_KEY_BUILDING_WITH_POWER").c_str(),
			kBuilding.getPowerYieldModifierArray(), true);

	// doc: power commerce modifier
	setCommerceChangeHelp(szBuffer, L"", L"",
			gDLL->getText(bCleanPower ? "TXT_KEY_BUILDING_WITH_CLEAN_POWER" : "TXT_KEY_BUILDING_WITH_POWER").c_str(),
			kBuilding.getPowerCommerceModifierArray(), true);

	// doc: culture level commerce modifier
	setCommerceChangeHelp(szBuffer, L"", L"",
			gDLL->getText("TXT_KEY_BUILDING_PER_CULTURE_LEVEL").c_str(),
			kBuilding.getCultureCommerceModifierArray(), true);

	setYieldChangeHelp(szBuffer, L"", L"",
			gDLL->getText("TXT_KEY_BUILDING_ALL_CITIES_THIS_CONTINENT").c_str(),
			kBuilding.getAreaYieldModifier(), true);

	setYieldChangeHelp(szBuffer, L"", L"",
			gDLL->getText("TXT_KEY_BUILDING_ALL_CITIES").c_str(),
			kBuilding.getGlobalYieldModifier(), true);

	setCommerceChangeHelp(szBuffer, L"", L"",
			gDLL->getText("TXT_KEY_BUILDING_ALL_CITIES").c_str(),
			kBuilding.getGlobalCommerceModifier(), true);

	setCommerceChangeHelp(szBuffer, L"", L"",
			gDLL->getText("TXT_KEY_BUILDING_PER_SPECIALIST_ALL_CITIES").c_str(),
			kBuilding.getSpecialistExtraCommerce());

	/*if (ePlayer != NO_PLAYER && GET_PLAYER(ePlayer).getStateReligion() != NO_RELIGION)
		szTempBuffer = gDLL->getText("TXT_KEY_BUILDING_FROM_ALL_REL_BUILDINGS", GC.getInfo(GET_PLAYER(ePlayer).getStateReligion()).getChar());
	else szTempBuffer = gDLL->getText("TXT_KEY_BUILDING_STATE_REL_BUILDINGS");*/ // BtS
	/*  K-Mod, 30/dec/10
		Changed to always say state religion, rather than the particular religion that happens to be the current state religion. */
	szTempBuffer = gDLL->getText("TXT_KEY_BUILDING_STATE_REL_BUILDINGS");

	// dpoc: culture level happiness
	if (kBuilding.getCultureHappiness() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_CULTURE_LEVEL_HAPPINESS",
				abs(kBuilding.getCultureHappiness()),
				kBuilding.getCultureHappiness() ? gDLL->getSymbolID(HAPPY_CHAR) : gDLL->getSymbolID(UNHAPPY_CHAR)));
	}

	setCommerceChangeHelp(szBuffer, L"", L"", szTempBuffer,
			kBuilding.getStateReligionCommerce());

	FOR_EACH_ENUM(Commerce)
	{
		if (kBuilding.getCommerceHappiness(eLoopCommerce) != 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_PER_LEVEL",
					// UNOFFICIAL_PATCH, Bugfix, 08/28/09, jdog5000 (start): Use absolute value with unhappy face
					((kBuilding.getCommerceHappiness(eLoopCommerce) > 0) ?
					gDLL->getSymbolID(HAPPY_CHAR) : gDLL->getSymbolID(UNHAPPY_CHAR)),
					abs(100 / kBuilding.getCommerceHappiness(eLoopCommerce)),
					GC.getInfo(eLoopCommerce).getChar())); // UNOFFICIAL_PATCH (end)
		}

		if (kBuilding.isCommerceFlexible(eLoopCommerce) != 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_ADJUST_COMM_RATE",
					GC.getInfo(eLoopCommerce).getChar()));
		}
	}
	/*	<advc.opt> Yield arrays - replacing optimization from UNOFFICIAL_PATCH
		(06/27/10, Afforess & jdog5000) */
	FOR_EACH_NON_DEFAULT_PAIR(kBuilding.
		getSpecialistYieldChange(), Specialist, YieldChangeMap)
	{
		SpecialistTypes const eLoopSpecialist = perSpecialistVal.first;
		// <advc.001>
		CvWString szSpecialistLink;
		setSpecialistLink(szSpecialistLink, eLoopSpecialist, true);
		// </advc.001>
		szFirstBuffer = gDLL->getText("TXT_KEY_BUILDING_FROM_IN_ALL_CITIES",
				//GC.getInfo(eLoopSpecialist).getTextKeyWide()
				szSpecialistLink.c_str()); // advc.001
		setYieldChangeHelp(szBuffer, L"", L"", szFirstBuffer,
				perSpecialistVal.second);
	}
	FOR_EACH_NON_DEFAULT_PAIR(kBuilding.
		getBonusYieldModifier(), Bonus, YieldPercentMap)
	{
		BonusTypes const eLoopBonus = perBonusVal.first;
		szFirstBuffer = gDLL->getText("TXT_KEY_BUILDING_WITH_BONUS",
				GC.getInfo(eLoopBonus).getTextKeyWide());
		setYieldChangeHelp(szBuffer, L"", L"", szFirstBuffer,
				perBonusVal.second, true);
	} // </advc.opt>
	// doc: bonus commerce modifier
	FOR_EACH_NON_DEFAULT_PAIR(kBuilding.
		getBonusCommerceModifier(), Bonus, CommercePercentMap)
	{
		BonusTypes const eLoopBonus = perBonusVal.first;
		szFirstBuffer = gDLL->getText("TXT_KEY_BUILDING_WITH_BONUS",
				GC.getInfo(eLoopBonus).getTextKeyWide());
		setCommerceChangeHelp(szBuffer, L"", L"", szFirstBuffer,
				perBonusVal.second, true);
	} // </advc.opt>

	// doc: do not show religion spread
	/*FOR_EACH_NON_DEFAULT_PAIR(kBuilding.
		getReligionChange(), Religion, int)
	{
		if (perReligionVal.second > 0)
		{
			szTempBuffer.Format(L"%s%s", NEWLINE,
					gDLL->getText("TXT_KEY_BUILDING_SPREADS_RELIGION",
					GC.getInfo(perReligionVal.first).getChar()).c_str());
			szBuffer.append(szTempBuffer);
		}
	}*/

	FOR_EACH_ENUM(Specialist)
	{
		if (kBuilding.getSpecialistCount(eLoopSpecialist) != 0)
		{
			bool const bSingular = (kBuilding.getSpecialistCount(eLoopSpecialist) == 1);
			// <advc.001>
			CvWString szSpecialistLink;
			setSpecialistLink(szSpecialistLink, eLoopSpecialist, bSingular); // </advc.001>
			szBuffer.append(NEWLINE);
			if (bSingular)
			{
				szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_TURN_CITIZEN_INTO",
						//GC.getInfo(eLoopSpecialist).getTextKeyWide()
						szSpecialistLink.c_str())); // advc.001
			}
			else
			{
				szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_TURN_CITIZENS_INTO",
						kBuilding.getSpecialistCount(eLoopSpecialist),
						//GC.getInfo(eLoopSpecialist).getTextKeyWide()
						szSpecialistLink.c_str())); // advc.001
			}
		}
		if (kBuilding.getFreeSpecialistCount(eLoopSpecialist) != 0)
		{
			szBuffer.append(NEWLINE);
			// <advc.001>
			CvWString szSpecialistLink;
			setSpecialistLink(szSpecialistLink, eLoopSpecialist); // </advc.001>
			szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_FREE_SPECIALIST",
					kBuilding.getFreeSpecialistCount(eLoopSpecialist),
					//GC.getInfo(eLoopSpecialist).getTextKeyWide()
					szSpecialistLink.c_str())); // advc.001
		}
	}
	{
		int iLast = 0;
		FOR_EACH_NON_DEFAULT_PAIR(kBuilding.
			getImprovementFreeSpecialist(), Improvement, int)
		{
			int const iFreeSpecialists = perImprovementVal.second;
			szFirstBuffer.Format(L"%s%s", NEWLINE,
					gDLL->getText("TXT_KEY_BUILDING_IMPROVEMENT_FREE_SPECIALISTS",
					iFreeSpecialists).GetCString());
			szTempBuffer.Format(L"<link=literal>%s</link>",
					GC.getInfo(perImprovementVal.first).getDescription());
			setListHelp(szBuffer, szFirstBuffer, szTempBuffer, L", ",
					iLast, iFreeSpecialists);
		}
	}

	// doc: improvement happiness percent
	// TODO: refactor
	iLast = 0;
	int iImprovementHappinessPercent;
	CvWString szHappiness;
	for (iI = 0; iI < GC.getNumImprovementInfos(); ++iI)
	{
		iImprovementHappinessPercent = kBuilding.getImprovementHappinessPercent(iI);
		if (iImprovementHappinessPercent != 0)
		{
			szHappiness.Format(L"%.2f", 0.01f * abs(iImprovementHappinessPercent));
			szFirstBuffer.Format(L"%s%s", NEWLINE, gDLL->getText("TXT_KEY_BUILDING_IMPROVEMENT_HAPPINESS", szHappiness.GetCString(), iImprovementHappinessPercent > 0 ? gDLL->getSymbolID(HAPPY_CHAR) : gDLL->getSymbolID(UNHAPPY_CHAR)).GetCString());
			szTempBuffer.Format(L"<link=literal>%s</link>", GC.getImprovementInfo((ImprovementTypes)iI).getDescription());
			setListHelp(szBuffer, szFirstBuffer, szTempBuffer, L", ", (iImprovementHappinessPercent != iLast));
			iLast = iImprovementHappinessPercent;
		}
	}

	// doc: improvement health percent
	// TODO: refactor
	iLast = 0;
	int iImprovementHealthPercent;
	CvWString szHealth;
	for (iI = 0; iI < GC.getNumImprovementInfos(); ++iI)
	{
		iImprovementHealthPercent = kBuilding.getImprovementHealthPercent(iI);
		if (iImprovementHealthPercent != 0)
		{
			szHealth.Format(L"%.2f", 0.01f * abs(iImprovementHealthPercent));
			szFirstBuffer.Format(L"%s%s", NEWLINE, gDLL->getText("TXT_KEY_BUILDING_IMPROVEMENT_HEALTH", szHealth.GetCString(), iImprovementHealthPercent > 0 ? gDLL->getSymbolID(HEALTHY_CHAR) : gDLL->getSymbolID(UNHEALTHY_CHAR)).GetCString());
			szTempBuffer.Format(L"<link=literal>%s</link>", GC.getImprovementInfo((ImprovementTypes)iI).getDescription());
			setListHelp(szBuffer, szFirstBuffer, szTempBuffer, L", ", (iImprovementHealthPercent != iLast));
			iLast = iImprovementHealthPercent;
		}
	}

	/*  advc.004w: Moved these two blocks up so that the (guaranteed) XP from Barracks
		appears above the highly situational happiness from civics. */
	FOR_EACH_NON_DEFAULT_PAIR(kBuilding.
		getUnitCombatFreeExperience(), UnitCombat, int)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_FREE_XP",
				GC.getInfo(perUnitCombatVal.first).getTextKeyWide(),
				perUnitCombatVal.second));
	}
	FOR_EACH_ENUM(Domain)
	{
		if (kBuilding.getDomainFreeExperience(eLoopDomain) != 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_FREE_XP",
					GC.getInfo(eLoopDomain).getTextKeyWide(),
					kBuilding.getDomainFreeExperience(eLoopDomain)));
		}
	}
	{
		int iLast = 0;
		FOR_EACH_NON_DEFAULT_PAIR(kBuilding.
			getBonusHealthChanges(), Bonus, int)
		{
			int const iHealthChange = perBonusVal.second;
			szFirstBuffer.Format(L"%s%s", NEWLINE,
					gDLL->getText("TXT_KEY_BUILDING_HEALTH_HAPPINESS_CHANGE",
					abs(iHealthChange), iHealthChange > 0 ?
					gDLL->getSymbolID(HEALTHY_CHAR) :
					gDLL->getSymbolID(UNHEALTHY_CHAR)).c_str());
			szTempBuffer.Format(L"<link=literal>%s</link>",
					GC.getInfo(perBonusVal.first).getDescription());
			setListHelp(szBuffer, szFirstBuffer, szTempBuffer, L", ",
					iLast, iHealthChange);
		}
	}
	{
		int iLast = 0;
		FOR_EACH_ENUM(Civic)
		{
			int iHealthChange = GC.getInfo(eLoopCivic).
					getBuildingHealthChanges(eBuildingClass);
			if (iHealthChange != 0)
			{
				szFirstBuffer.Format(L"%s%s", NEWLINE,
						gDLL->getText("TXT_KEY_BUILDING_CIVIC_HEALTH_HAPPINESS_CHANGE",
						abs(iHealthChange), iHealthChange > 0 ?
						gDLL->getSymbolID(HEALTHY_CHAR) :
						gDLL->getSymbolID(UNHEALTHY_CHAR)).c_str());
				szTempBuffer.Format(L"<link=literal>%s</link>",
						GC.getInfo(eLoopCivic).getDescription());
				setListHelp(szBuffer, szFirstBuffer, szTempBuffer, L", ",
						iLast, iHealthChange);
			}
		}
	}
	{
		int iLast = 0;
		FOR_EACH_NON_DEFAULT_PAIR(kBuilding.
			getBonusHappinessChanges(), Bonus, int)
		{
			int const iHappyChange = perBonusVal.second;
			szFirstBuffer.Format(L"%s%s", NEWLINE,
					gDLL->getText("TXT_KEY_BUILDING_HEALTH_HAPPINESS_CHANGE",
					abs(iHappyChange), iHappyChange > 0 ?
					gDLL->getSymbolID(HAPPY_CHAR) :
					gDLL->getSymbolID(UNHAPPY_CHAR)).c_str());
			szTempBuffer.Format(L"<link=literal>%s</link>",
					GC.getInfo(perBonusVal.first).getDescription());
			setListHelp(szBuffer, szFirstBuffer, szTempBuffer, L", ",
					iLast, iHappyChange);
		}
	}
	{
		int iLast = 0;
		FOR_EACH_ENUM(Civic)
		{
			int iHappyChange = GC.getInfo(eLoopCivic).
					getBuildingHappinessChanges(eBuildingClass);
			if (iHappyChange != 0)
			{	// <advc.004w>
				bool bParentheses = false;
				if(pCity != NULL)
				{
					// Don't mention bonuses that won't happen in this or the next era
					TechTypes ePrereqTech = GC.getInfo(eLoopCivic).getTechPrereq();
					if(ePrereqTech != NO_TECH &&
						GC.getInfo(ePrereqTech).getEra() - pPlayer->getCurrentEra() > 1)
					{
						continue;
					}
					if(!pPlayer->isCivic(eLoopCivic))
						bParentheses = true;
				} // </advc.004w>
				szFirstBuffer.Format(L"%s%s", NEWLINE, gDLL->getText( // <advc.004w>
						(bParentheses ?
						  "TXT_KEY_BUILDING_CIVIC_HEALTH_HAPPINESS_CHANGE_PAR"
						: "TXT_KEY_BUILDING_CIVIC_HEALTH_HAPPINESS_CHANGE"),
						// </advc.004w>
						abs(iHappyChange), iHappyChange > 0 ?
						gDLL->getSymbolID(HAPPY_CHAR) :
						gDLL->getSymbolID(UNHAPPY_CHAR)).c_str());
				// <advc.004w>
				if(bParentheses)
				{
					szTempBuffer.Format(L"<link=literal>%s)</link>",
							GC.getInfo(eLoopCivic).getDescription());
				}
				else // </advc.004w>
				{
					szTempBuffer.Format(L"<link=literal>%s</link>",
							GC.getInfo(eLoopCivic).getDescription());
				}
				setListHelp(szBuffer, szFirstBuffer, szTempBuffer, L", ",
						iLast, iHappyChange);
			}
		}
	}
	FOR_EACH_ENUM(Domain)
	{
		if (kBuilding.getDomainProductionModifier(eLoopDomain) != 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_BUILDS_FASTER_DOMAIN",
					GC.getInfo(eLoopDomain).getTextKeyWide(),
					kBuilding.getDomainProductionModifier(eLoopDomain)));
		}
	}
	{
		bool bFirst = true;
		FOR_EACH_ENUM(Unit)
		{
			if (GC.getInfo(eLoopUnit).getPrereqBuilding() == eBuilding)
			{
				szFirstBuffer.Format(L"%s%s", NEWLINE,
						gDLL->getText("TXT_KEY_BUILDING_REQUIRED_TO_TRAIN").c_str());
				szTempBuffer.Format( SETCOLR L"<link=literal>%s</link>" ENDCOLR,
						TEXT_COLOR("COLOR_UNIT_TEXT"),
						GC.getInfo(eLoopUnit).getDescription());
				setListHelp(szBuffer, szFirstBuffer, szTempBuffer, L", ", bFirst);
			}
		}
	}
	/*  advc.004w: If in city screen, the player is apparently not constructing
		the building through a Great Person. */
	if(!gDLL->UI().isCityScreenUp())
	{
		bool bFirst = true;
		FOR_EACH_ENUM(Unit)
		{
			// doc (edead): exclude graphical only
			if (GC.getInfo(eLoopUnit).isGraphicalOnly())
				continue;

			if (GC.getInfo(eLoopUnit).getBuildings(eBuilding))
				//|| GC.getInfo(eLoopUnit).getForceBuildings(eBuilding) // advc.003t
			{
				szFirstBuffer.Format(L"%s%s", NEWLINE,
						gDLL->getText("TXT_KEY_UNIT_REQUIRED_TO_BUILD").c_str());
				szTempBuffer.Format( SETCOLR L"<link=literal>%s</link>" ENDCOLR,
						TEXT_COLOR("COLOR_UNIT_TEXT"),
						GC.getInfo(eLoopUnit).getDescription());
				setListHelp(szBuffer, szFirstBuffer, szTempBuffer, L", ", bFirst);
			}
		}
	}
	{
		int iLast = 0;
		FOR_EACH_NON_DEFAULT_PAIR(kBuilding.
			getBuildingHappinessChanges(), BuildingClass, int)
		{
			BuildingClassTypes const eLoopBuildingClass = perBuildingClassVal.first;
			int const iHappyChange = perBuildingClassVal.second;
			szTempBuffer.Format(L"%s%s", NEWLINE, gDLL->getText(
					"TXT_KEY_BUILDING_HAPPINESS_CHANGE",
					/*	UNOFFICIAL_PATCH, Bugfix, 08/28/09, jdog5000 (start):
						Use absolute value with unhappy face */
					abs(iHappyChange), iHappyChange > 0 ?
					gDLL->getSymbolID(HAPPY_CHAR) :
					gDLL->getSymbolID(UNHAPPY_CHAR)).c_str());
					// UNOFFICIAL_PATCH (end)
			CvWString szBuilding;
			if (ePlayer != NO_PLAYER)
			{
				BuildingTypes ePlayerBuilding = pPlayer->getCivilization().
						getBuilding(eLoopBuildingClass);
				if (ePlayerBuilding != NO_BUILDING)
				{
					szBuilding.Format(L"<link=literal>%s</link>",
							GC.getInfo(eLoopBuildingClass).getDescription());
				}
			}
			else
			{
				szBuilding.Format(L"<link=literal>%s</link>",
						GC.getInfo(eLoopBuildingClass).getDescription());
			}
			setListHelp(szBuffer, szTempBuffer, szBuilding, L", ",
					iLast, iHappyChange);
		}
	}
	if (kBuilding.getPowerBonus() != NO_BONUS)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_PROVIDES_POWER_WITH",
				GC.getInfo((BonusTypes)kBuilding.getPowerBonus()).getTextKeyWide()));

		/*if (kBuilding.isDirtyPower() && (GC.getDefineINT(CvGlobals::DIRTY_POWER_HEALTH_CHANGE) != 0)) {
			szTempBuffer.Format(L" (+%d%c)", abs(GC.getDefineINT(CvGlobals::DIRTY_POWER_HEALTH_CHANGE)), ((GC.getDefineINT(CvGlobals::DIRTY_POWER_HEALTH_CHANGE) > 0) ? gDLL->getSymbolID(HEALTHY_CHAR): gDLL->getSymbolID(UNHEALTHY_CHAR)));
			szBuffer.append(szTempBuffer);
		}*/ // BtS
		// K-Mod. Also include base health change from power.
		int iPowerHealth = GC.getDefineINT(CvGlobals::POWER_HEALTH_CHANGE) +
				(!kBuilding.isDirtyPower() ? 0 :
				GC.getDefineINT(CvGlobals::DIRTY_POWER_HEALTH_CHANGE));
		if (iPowerHealth)
		{
			szTempBuffer.Format(L" (+%d%c)", abs(iPowerHealth),
					iPowerHealth > 0 ? gDLL->getSymbolID(HEALTHY_CHAR) :
					gDLL->getSymbolID(UNHEALTHY_CHAR));
			szBuffer.append(szTempBuffer);
		}
		// K-Mod end
	}
	{
		bool bFirst = true;
		FOR_EACH_ENUM(BuildingClass)
		{
			BuildingTypes const eLoopBuilding = (ePlayer != NO_PLAYER ?
					pPlayer->getCivilization().getBuilding(eLoopBuildingClass) :
					GC.getInfo(eLoopBuildingClass).getDefaultBuilding());
			if(eLoopBuilding == NO_BUILDING)
				continue; // advc
			if (GC.getInfo(eLoopBuilding).isBuildingClassNeededInCity(eBuildingClass) &&
				!bInBuildingList) // advc.004w
			{
				if (pCity == NULL || pCity->canConstruct(eLoopBuilding, false, true))
				{
					szFirstBuffer.Format(L"%s%s", NEWLINE,
							gDLL->getText("TXT_KEY_BUILDING_REQUIRED_TO_BUILD").c_str());
					szTempBuffer.Format(SETCOLR L"<link=literal>%s</link>" ENDCOLR,
							TEXT_COLOR("COLOR_BUILDING_TEXT"),
							GC.getInfo(eLoopBuilding).getDescription());
					setListHelp(szBuffer, szFirstBuffer, szTempBuffer, L", ", bFirst);
				}
			}
		}
	}
	// rfc: disable traits
	/*if (bCivilopediaText)
	{
		// (advc.004w: ProductionTraits moved into setProductionSpeedHelp)
		FOR_EACH_NON_DEFAULT_PAIR(kBuilding.
			getHappinessTraits(), Trait, int)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_HAPPINESS_TRAIT",
					perTraitVal.second, GC.getInfo(perTraitVal.first).getTextKeyWide()));
		}
	}*/

	if (bCivilopediaText)
	{
		UnitClassTypes eGPClass = kBuilding.getGreatPeopleUnitClass();
		if (eGPClass != NO_UNITCLASS)
		{
			UnitTypes eGreatPeopleUnit = NO_UNIT; // advc
			if (ePlayer != NO_PLAYER)
				eGreatPeopleUnit = pPlayer->getCivilization().getUnit(eGPClass);
			else eGreatPeopleUnit = GC.getInfo(eGPClass).getDefaultUnit();

			if (eGreatPeopleUnit!= NO_UNIT)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_LIKELY_TO_GENERATE",
						GC.getInfo(eGreatPeopleUnit).getTextKeyWide()));
			}
		}
		// advc.004w: Commented out
		/*if (kBuilding.getFreeStartEra() != NO_ERA) {
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_FREE_START_ERA", GC.getInfo((EraTypes)kBuilding.getFreeStartEra()).getTextKeyWide()));
		}*/
	}

	// doc: stability impact
	if (GC.getInfo(eDefaultBuilding).getMaintenanceModifier() != 0)
	{
		if (pCity != NULL && !pCity->plot()->isCore(ePlayer))
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_EXPANSION_STABILITY"));
		}
	}

	if (!CvWString(kBuilding.getHelp()).empty())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(kBuilding.getHelp());
	}
	if(!bInBuildingList) // advc.004w
	{
		buildBuildingRequiresString(szBuffer, eBuilding, bCivilopediaText,
				bTechChooserText, pCity);
	}
	if (pCity != NULL /* advc.004w: */ && !bInBuildingList)
	{
		if (!GC.getInfo(eBuildingClass).isNoLimit())
		{
			if (kBuilding.isWorldWonder())
			{
				if (pCity->isWorldWondersMaxed())
				{
					// doc: culture level determines wonder limit
					int iWonderLimit = GC.getInfo(pCity->getCultureLevel()).getWonderLimit();
					if (pCity->isCapital())
						iWonderLimit++;

					szBuffer.append(NEWLINE);
					if (iWonderLimit > 0)
						szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_WORLD_WONDERS_PER_CULTURE_LEVEL",
							iWonderLimit,
							GC.getInfo(pCity->getCultureLevel()).getTextKeyWide()));
					else
						szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_WORLD_WONDERS_NONE_FOR_CULTURE_LEVEL",
							GC.getInfo(pCity->getCultureLevel()).getTextKeyWide()));
				}
			}
			else if (kBuilding.isTeamWonder())
			{
				if (pCity->isTeamWondersMaxed())
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_TEAM_WONDERS_PER_CITY",
							GC.getDefineINT(CvGlobals::MAX_TEAM_WONDERS_PER_CITY)));
				}
			}
			else if (kBuilding.isNationalWonder())
			{
				if (pCity->isNationalWondersMaxed())
				{
					// doc: culture level determines national wonder limit
					int iNationalWonderLimit = GC.getInfo(pCity->getCultureLevel()).getNationalWonderLimit();

					szBuffer.append(NEWLINE);
					if (iNationalWonderLimit > 0)
						szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_NATIONAL_WONDERS_PER_CULTURE_LEVEL",
								iNationalWonderLimit, GC.getInfo(pCity->getCultureLevel()).getTextKeyWide()));
					else
						szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_NATIONAL_WONDERS_NONE_FOR_CULTURE_LEVEL",
								GC.getInfo(pCity->getCultureLevel()).getTextKeyWide()));
				}
			}
			else
			{
				if (pCity->isBuildingsMaxed())
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_NUM_PER_CITY",
							GC.getDefineINT("MAX_BUILDINGS_PER_CITY")));
				}
			}
		}
	} /* <advc.004> Show this right before the cost in Civilopedia text and
		 otherwise (i.e. in hover text) after the cost */
	if(bCivilopediaText)
	{
		setProductionSpeedHelp<ORDER_CONSTRUCT>(szBuffer,
				eBuilding, kBuilding.getSpecialBuildingType(),
				pCity, true);
	} // </advc.004w>
	/*if ((pCity == NULL) || pCity->getNumRealBuilding(eBuilding) < GC.getCITY_MAX_NUM_BUILDINGS()){
		if (!bCivilopediaText) { */
	/*  advc.004w: Replacing the above. inBuildingList is based on getNumBuilding,
		which, I think, makes more sense than getNumRealBuilding. */
	if(!bInBuildingList)
	{
		if (pCity == NULL)
		{
			if (kBuilding.getProductionCost() > 0 /* advc.004y: */ && !bCivilopediaText)
			{
				szTempBuffer.Format(L"\n%d%c",
						(ePlayer == NO_PLAYER ? kBuilding.getProductionCost() : // advc
						pPlayer->getProductionNeeded(eBuilding)), GC.getInfo(YIELD_PRODUCTION).getChar());
				szBuffer.append(szTempBuffer);
			}
		}
		else
		{
			// BUG - Building Actual Effects (edited and moved by K-Mod) - start
			if (bActual && (GC.altKey() || BUGOption::isEnabled("MiscHover__BuildingActualEffects", false)) &&
				(pCity->isActiveOwned() || //gDLL->getChtLvl() > 0))
				GC.getGame().isDebugMode())) // advc.135c
			{
				setBuildingNetEffectsHelp(szBuffer, eBuilding, pCity);
			} // BUG - Building Actual Effects - end

			szBuffer.append(NEWLINE);
			int iTurns = pCity->getProductionTurnsLeft(eBuilding,
					(GC.ctrlKey() || !GC.shiftKey()) ? 0 : pCity->getOrderQueueLength());
			if (iTurns < MAX_INT) // advc.004x
			{
				szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_NUM_TURNS", iTurns));
				szBuffer.append(L" - "); // advc.004x: Moved up
			}

			int iProduction = pCity->getBuildingProduction(eBuilding);
			int iProductionNeeded = pCity->getProductionNeeded(eBuilding);
			if (iProduction > 0)
			{
				szTempBuffer.Format(L"%d/%d%c", iProduction, iProductionNeeded,
						GC.getInfo(YIELD_PRODUCTION).getChar());
				szBuffer.append(szTempBuffer);
			}
			else
			{
				szTempBuffer.Format(L"%d%c", iProductionNeeded,
						GC.getInfo(YIELD_PRODUCTION).getChar());
				szBuffer.append(szTempBuffer);
			}
			// BULL - Production Decay - start
			// advc.094: No separate ProductionDecayHover option
			if (BUGOption::isEnabled("CityScreen__ProductionDecayQueue", false) &&
				pCity->isActiveOwned()) // advc.094: Don't show this in foreign cities
			{
				setProductionDecayHelp(szBuffer,
						pCity->getBuildingProductionDecayTurns(eBuilding),
						// advc.094: No separate ProductionDecayHoverBuildingtThreshold option
						BUGOption::getValue("CityScreen__ProductionDecayQueueBuildingThreshold", 10),
						pCity->getBuildingProductionDecay(eBuilding),
						pCity->getProductionBuilding() == eBuilding);
			} // BULL - Production Decay - end
		}
		// <advc.004w> BonusProductionModifier moved into subroutine
		if(!bCivilopediaText)
		{
			setProductionSpeedHelp<ORDER_CONSTRUCT>(szBuffer,
					eBuilding, kBuilding.getSpecialBuildingType(),
					pCity, false);

		// doc: ivic production modifier
		// TODO: move to setProductionSpeedHelp
		for (int iI = 0; iI < GC.getNumCivicInfos(); ++iI)
		{
			CivicTypes eCivic = (CivicTypes)iI;
			int iProductionModifier = GC.getCivicInfo(eCivic).getBuildingProductionModifier(kBuilding.getBuildingClassType());
			if (iProductionModifier != 0)
			{
				if (pCity != NULL)
				{
					if (GET_PLAYER(pCity->getOwnerINLINE()).hasCivic(eCivic))
					{
						szBuffer.append(gDLL->getText("TXT_KEY_COLOR_POSITIVE"));
					}
					else
					{
						szBuffer.append(gDLL->getText("TXT_KEY_COLOR_NEGATIVE"));
					}
				}
				if (!bCivilopediaText)
				{
					szBuffer.append(L" (");
				}
				else
				{
					szTempBuffer.Format(L"\n%c", gDLL->getSymbolID(BULLET_CHAR), szTempBuffer);
					szBuffer.append(szTempBuffer);
				}
				if (iProductionModifier == 100)
				{
					szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_DOUBLE_SPEED_WITH", GC.getCivicInfo(eCivic).getTextKeyWide()));
				}
				else
				{
					szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_BUILDS_FASTER_WITH", iProductionModifier, GC.getCivicInfo(eCivic).getTextKeyWide()));
				}
				if (!bCivilopediaText)
				{
					szBuffer.append(L')');
				}
				if (pCity != NULL)
				{
					szBuffer.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));
				}
			}
		}

		// doc: civics capital building production modifier
		// TODO: move to setProductionSpeedHelp
		if (pCity != NULL && !bCivilopediaText)
		{
			CvCity* pCapital = GET_PLAYER(GC.getGameINLINE().getActivePlayer()).getCapitalCity();
			int iCapitalBuildingProductionModifier = GET_PLAYER(GC.getGameINLINE().getActivePlayer()).getCapitalBuildingProductionModifier();
			if (pCapital != NULL && iCapitalBuildingProductionModifier != 0)
			{
				if (!isNationalWonderClass((BuildingClassTypes)kBuilding.getBuildingClassType()) && !isWorldWonderClass((BuildingClassTypes)kBuilding.getBuildingClassType()) && kBuilding.getProductionCost() > 0)
				{
					szBuffer.append(gDLL->getText(pCapital->isHasRealBuilding(eBuilding) ? "TXT_KEY_COLOR_POSITIVE" : "TXT_KEY_COLOR_NEGATIVE"));
					szBuffer.append(L" (");
					szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_BUILDS_FASTER_WITH_CAPITAL_BUILDING", iCapitalBuildingProductionModifier, kBuilding.getText(), pCapital->getName().c_str()));
					szBuffer.append(L")");
					szBuffer.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));
				}
			}
		}

		} // </advc.004w>
		if (kBuilding.getObsoleteTech() != NO_TECH)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText(/* advc.004w: */ szObsoleteWithTag,
					GC.getInfo(kBuilding.getObsoleteTech()).getTextKeyWide()));

			if (kBuilding.getDefenseModifier() != 0 ||
				kBuilding.getBombardDefenseModifier() != 0 ||
				kBuilding.get(CvBuildingInfo::RaiseDefense) > 0) // advc.004c
			{
				szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_OBSOLETE_EXCEPT"));
			}
		}

		if (kBuilding.getSpecialBuildingType() != NO_SPECIALBUILDING &&
			GC.getInfo(kBuilding.getSpecialBuildingType()).getObsoleteTech() != NO_TECH)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText(/* advc.004w: */ szObsoleteWithTag,
					GC.getInfo(GC.getInfo(kBuilding.getSpecialBuildingType()).
					getObsoleteTech()).getTextKeyWide()));
		}
	} // <advc.004w>
	else if(bObsolete)
	{
		// Copy-pasted from above
		if(kBuilding.getObsoleteTech() != NO_TECH)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText(szObsoleteWithTag,
					GC.getInfo(kBuilding.getObsoleteTech()).getTextKeyWide()));
			if(kBuilding.getDefenseModifier() != 0 ||
				kBuilding.getBombardDefenseModifier() != 0 ||
				kBuilding.get(CvBuildingInfo::RaiseDefense) > 0) // advc.004c
			{
				szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_OBSOLETE_EXCEPT"));
			}
		}
		if(kBuilding.getSpecialBuildingType() != NO_SPECIALBUILDING)
		{
			if(GC.getInfo(kBuilding.getSpecialBuildingType()).getObsoleteTech() != NO_TECH)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText(szObsoleteWithTag,
						GC.getInfo(GC.getInfo(kBuilding.getSpecialBuildingType()).
						getObsoleteTech()).getTextKeyWide()));
			}
		}
	} // </advc.004w>
	// K-Mod. Moved from inside that }, above.
	if (pCity != NULL && //gDLL->getChtLvl() > 0
		GC.getGame().isDebugMode() && // advc.135c
		GC.ctrlKey())
	{
		if (GC.ctrlKey())
		{
			int iBuildingValue = pCity->AI().AI_buildingValue(
					eBuilding, 0, 0, true);
			szBuffer.append(CvWString::format(L"\nAI Building Value = %d",
					iBuildingValue));
		} // K-Mod end
		// <advc.007>
		else if (GC.altKey())
			szBuffer.append(CvWString::format(L"id=%d\n", eBuilding));
	} // </advc.007>

	// rfc: disable
	/*if (bStrategyText)
	{
		if (!CvWString(kBuilding.getStrategy()).empty())
		{
			if (pPlayer->isOption(PLAYEROPTION_ADVISOR_HELP))
			{
				szBuffer.append(SEPARATOR);
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_SIDS_TIPS"));
				szBuffer.append(L'\"');
				szBuffer.append(kBuilding.getStrategy());
				szBuffer.append(L'\"');
			}
		}
	}*/

	if (bCivilopediaText && eDefaultBuilding == eBuilding)
	{
		FOR_EACH_ENUM(Building)
		{
			if (eLoopBuilding != eBuilding)
			{
				if (eBuildingClass == GC.getInfo(eLoopBuilding).getBuildingClassType() &&
					!GC.getInfo(eLoopBuilding).isGraphicalOnly()) // doc (edead): exclude graphical only
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_REPLACED_BY_BUILDING",
							GC.getInfo(eLoopBuilding).getTextKeyWide()));
				}
			}
		}
	}
}


void CvGameTextMgr::buildBuildingRequiresString(CvWStringBuffer& szBuffer,
	BuildingTypes eBuilding, bool bCivilopediaText, bool bTechChooserText, const CvCity* pCity)
{
	if (pCity != NULL && pCity->canConstruct(eBuilding))
		return;
	/*	K-mod note. I've made a couple of style adjustments throughout this function
		to make it easier for me to read & maintain. */
	CvBuildingInfo const& kBuilding = GC.getInfo(eBuilding);
	PlayerTypes const ePlayer = (pCity != NULL ? pCity->getOwner() : getActivePlayer());

	if (kBuilding.getHolyCity() != NO_RELIGION)
	{
		if (pCity == NULL || !pCity->isHolyCity((ReligionTypes)(kBuilding.getHolyCity())))
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_ACTION_ONLY_HOLY_CONSTRUCT",
					GC.getInfo((ReligionTypes) kBuilding.getHolyCity()).getChar()));
		}
	}
	{
		bool bFirst = true;
		if (kBuilding.getSpecialBuildingType() != NO_SPECIALBUILDING)
		{
			if (pCity == NULL ||
				!GC.getGame().isSpecialBuildingValid(kBuilding.getSpecialBuildingType()))
			{
				FOR_EACH_ENUM(Project)
				{
					if (GC.getInfo(eLoopProject).getEveryoneSpecialBuilding() ==
						kBuilding.getSpecialBuildingType())
					{
						CvWString szTempBuffer;
						szTempBuffer.Format(L"%s%s", NEWLINE,
								gDLL->getText("TXT_KEY_REQUIRES").c_str());
						CvWString szProject;
						szProject.Format(L"<link=literal>%s</link>",
								GC.getInfo(eLoopProject).getDescription());
						setListHelp(szBuffer, szTempBuffer, szProject,
								gDLL->getText("TXT_KEY_OR").c_str(), bFirst);
					}
				}
			}
		}
		if (!bFirst)
			szBuffer.append(ENDCOLR);
	}
	if (kBuilding.getSpecialBuildingType() != NO_SPECIALBUILDING)
	{
		if (pCity == NULL ||
			!GC.getGame().isSpecialBuildingValid(kBuilding.getSpecialBuildingType()))
		{
			TechTypes eTech = GC.getInfo(kBuilding.getSpecialBuildingType()).
					getTechPrereqAnyone();
			if (eTech != NO_TECH)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_REQUIRES_TECH_ANYONE",
						GC.getInfo(eTech).getTextKeyWide()));
			}
		}
	}

	FOR_EACH_ENUM(BuildingClass)
	{
		/*	K-Mod note: I've rearranged the conditions in the following block.
			Originally it was something like this: */
		//if (ePlayer == NO_PLAYER && kBuilding.getPrereqNumOfBuildingClass((BuildingClassTypes)iI) > 0)
		//else if (ePlayer != NO_PLAYER && GET_PLAYER(ePlayer).getBuildingClassPrereqBuilding(eBuilding, ((BuildingClassTypes)iI)) > 0)
		//
		/*	K-Mod. Check that we can actually build this class of building.
			(Previously this was checked in every single block below.) */
		BuildingTypes const eLoopBuilding = (ePlayer == NO_PLAYER ?
				GC.getInfo(eLoopBuildingClass).getDefaultBuilding() :
				GET_PLAYER(ePlayer).getCivilization().getBuilding(eLoopBuildingClass));
		if (eLoopBuilding == NO_BUILDING)
			continue;
		// K-Mod end

		/*  UNOFFICIAL_PATCH, Bugfix, 06/10/10, EmperorFool:
			show "Requires Hospital" if "Requires Hospital (x/5)" requirement has been met */
		bool bShowedPrereq = false;
		if (kBuilding.getPrereqNumOfBuildingClass(eLoopBuildingClass) > 0)
		{
			if (ePlayer == NO_PLAYER)
			{	// <advc.004y>
				int iLow = kBuilding.getPrereqNumOfBuildingClass(eLoopBuildingClass);
				WorldSizeTypes const eWorld = (WorldSizeTypes)(GC.getNumWorldInfos() - 1);
				int iHigh = iLow * std::max(0, (GC.getInfo(eWorld).
						getBuildingClassPrereqModifier() + 100));
				iHigh = (int)::ceil(iHigh / 100.0); // advc.140
				// </advc.004y>
				CvWString szTempBuffer;
				szTempBuffer.Format(L"%s%s", NEWLINE, gDLL->getText(
						// <advc.004y>
						(iLow == iHigh ?
						"TXT_KEY_BUILDING_REQ_BUILDINGS_NOCITY" :
						"TXT_KEY_BUILDING_REQ_BUILDINGS_NOCITY_RANGE"),
						// </advc.004y>
						GC.getInfo(eLoopBuilding).getTextKeyWide(),
						iLow, iHigh // advc.004y
					).c_str());

				szBuffer.append(szTempBuffer);
				bShowedPrereq = true; // UNOFFICIAL_PATCH, Bugfix, 06/10/10, EmperorFool
			}
			else
			{
				//if (pCity == NULL || (GET_PLAYER(ePlayer).getBuildingClassCount(eLoopBuildingClass) < GET_PLAYER(ePlayer).getBuildingClassPrereqBuilding(eBuilding, eLoopBuildingClass)))
				/*	K-Mod. In the city screen, include in the prereqs calculation
					the number of eBuilding under construction. But in the civilopedia,
					don't even include the number we have already built! */
				CvPlayer const& kPlayer = GET_PLAYER(ePlayer);
				int const iNeeded = kPlayer.getBuildingClassPrereqBuilding(
						eBuilding, eLoopBuildingClass,
						bCivilopediaText ?
						-kPlayer.getBuildingClassCount(kBuilding.getBuildingClassType()) :
						kPlayer.getBuildingClassMaking(kBuilding.getBuildingClassType()));
				FAssert(iNeeded > 0);
				// K-Mod end

				CvWString szTempBuffer;
				if (pCity != NULL)
				{
					szTempBuffer.Format(L"%s%s", NEWLINE, gDLL->getText(
							"TXT_KEY_BUILDING_REQUIRES_NUM_SPECIAL_BUILDINGS",
							GC.getInfo(eLoopBuilding).getTextKeyWide(),
							kPlayer.getBuildingClassCount(eLoopBuildingClass),
							iNeeded).c_str()); // K-Mod
				}
				else
				{
					szTempBuffer.Format(L"%s%s", NEWLINE, gDLL->getText(
							"TXT_KEY_BUILDING_REQUIRES_NUM_SPECIAL_BUILDINGS_NO_CITY",
							GC.getInfo(eLoopBuilding).getTextKeyWide(),
							iNeeded).c_str()); // K-Mod
				}
				szBuffer.append(szTempBuffer);
				bShowedPrereq = true; // UNOFFICIAL_PATCH, Bugfix, 06/10/10, EmperorFool
			}
		}
		// UNOFFICIAL_PATCH, Bugfix (bShowedPrereq), 06/10/10, EmperorFool: START
		if (!bShowedPrereq &&
			kBuilding.isBuildingClassNeededInCity(eLoopBuildingClass))
		{
			if (pCity == NULL || pCity->getNumBuilding(eLoopBuilding) <= 0)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_REQUIRES_STRING",
						GC.getInfo(eLoopBuilding).getTextKeyWide()));
			}
		} // UNOFFICIAL_PATCH: END
	}

	// doc: civic requirements
	if (kBuilding.getPrereqCivic() != NO_CIVIC)
	{
		if (NULL != pCity && NO_PLAYER != ePlayer &&
			!GET_PLAYER(ePlayer).hasCivic(kBuilding.getPrereqCivic()))
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_REQUIRES_CIVIC",
					GC.getInfo(kBuilding.getPrereqCivic()).getText()));
		}
	}

	if (kBuilding.isStateReligion())
	{
		if (pCity == NULL || NO_PLAYER == ePlayer ||
			GET_PLAYER(ePlayer).getStateReligion() == NO_RELIGION ||
			!pCity->isHasReligion(GET_PLAYER(ePlayer).getStateReligion()))
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_REQUIRES_STATE_RELIGION"));
		}
	}
	// <advc.179>
	if(bCivilopediaText || ePlayer == NO_PLAYER)
		buildBuildingReligionYieldString(szBuffer, kBuilding);
	bool bEligibilityDone = false;
	/*	Moved Triggered Election and Eligibility down so that the
		VoteSource stuff appears in one place. */
	// </advc.179>
	FOR_EACH_ENUM(VoteSource)
	{
		if (kBuilding.getVoteSourceType() != eLoopVoteSource)
			continue;
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_DIPLO_VOTE",
				GC.getInfo(eLoopVoteSource).getTextKeyWide()));
		// <advc.179> Put eligiblity in the same line
		if(kBuilding.isForceTeamVoteEligible())
		{
			szBuffer.append(L" " + gDLL->getText(
					"TXT_KEY_BUILDING_ELECTION_ELIGIBILITY_SHORT"));
			bEligibilityDone = true;
		} // </advc.179>
	}
	if (kBuilding.isForceTeamVoteEligible() /* advc.179: */ && !bEligibilityDone)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_ELECTION_ELIGIBILITY"));
	}

	// doc: pagan religion requirement
	if (kBuilding.isPagan())
	{
		if (NULL == pCity || NO_PLAYER == ePlayer || NO_RELIGION != GET_PLAYER(ePlayer).getStateReligion() || pCity->getReligionCount() > 0)
		{
			CvWString szPaganReligionName = gDLL->getText("TXT_KEY_RELIGION_PAGANISM");
			if (NO_PLAYER != ePlayer && !GET_PLAYER(ePlayer).isMinorCiv())
				szPaganReligionName = GC.getInfo(GC.getInfo(GET_PLAYER(ePlayer).getCivilizationType()).getPaganReligion()).getDescription());

			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_REQUIRES_PAGAN_RELIGION",
				szPaganReligionName.GetCString()));
		}
	}

	if (kBuilding.getNumCitiesPrereq() > 0)
	{
		if (ePlayer == NO_PLAYER ||
			GET_PLAYER(ePlayer).getNumCities() < kBuilding.getNumCitiesPrereq())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_REQUIRES_NUM_CITIES",
					kBuilding.getNumCitiesPrereq()));
		}
	}

	// doc: number of colonies requirement
	if (kBuilding.getNumColoniesPrereq() > 0)
	{
		if (NULL == pCity || NO_PLAYER == ePlayer ||
			GET_PLAYER(ePlayer).countColonies() < kBuilding.getNumColoniesPrereq())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_REQUIRES_NUM_COLONIES",
					kBuilding.getNumColoniesPrereq()));
		}
	}

	if (kBuilding.getUnitLevelPrereq() > 0)
	{
		if (ePlayer == NO_PLAYER ||
			GET_PLAYER(ePlayer).getHighestUnitLevel() < kBuilding.getUnitLevelPrereq())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_REQUIRES_UNIT_LEVEL",
					kBuilding.getUnitLevelPrereq()));
		}
	}

	if (kBuilding.getMinLatitude() > 0)
	{
		if (pCity == NULL ||
			pCity->getPlot().getLatitude() < kBuilding.getMinLatitude())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_MIN_LATITUDE",
					kBuilding.getMinLatitude()));
		}
	}

	if (kBuilding.getMaxLatitude() < 90)
	{
		if (pCity == NULL ||
			pCity->getPlot().getLatitude() > kBuilding.getMaxLatitude())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_MAX_LATITUDE",
					kBuilding.getMaxLatitude()));
		}
	}

	if (pCity != NULL && GC.getGame().isNoNukes() && kBuilding.isAllowsNukes())
	{
		FOR_EACH_ENUM(Unit)
		{
			if (GC.getInfo(eLoopUnit).isNuke())
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_NO_NUKES"));
				break;
			}
		}
	}

	if (bCivilopediaText)
	{	// advc.008a: Moved this block up a bit
		if (kBuilding.getNumTeamsPrereq() > 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_REQUIRES_NUM_TEAMS",
					kBuilding.getNumTeamsPrereq()));
		}
		if (kBuilding.getVictoryPrereq() != NO_VICTORY)
		{	// <advc.008a>
			if(ePlayer == NO_PLAYER ||
				!GC.getGame().isVictoryValid(kBuilding.getVictoryPrereq()))
			{
				if(ePlayer != NO_PLAYER)
					szBuffer.append(gDLL->getText("TXT_KEY_COLOR_NEGATIVE"));
				// </advc.008a>
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_REQUIRES_VICTORY",
						GC.getInfo(kBuilding.getVictoryPrereq()).getTextKeyWide()));
				// <advc.008a>
				if(ePlayer != NO_PLAYER)
					szBuffer.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));
			} // </advc.008a>
		}

		if (kBuilding.getMaxStartEra() != NO_ERA)
		{	// <advc.008a>
			TechTypes const eTechReq = kBuilding.getPrereqAndTech();
			bool const bUnavailable = (ePlayer != NO_PLAYER &&
					GC.getGame().getStartEra() >
					kBuilding.getMaxStartEra()); // TODO: disable max start era
			if(bUnavailable || (ePlayer == NO_PLAYER &&
				(eTechReq == NO_TECH ||
				GC.getInfo(eTechReq).getEra() != kBuilding.getMaxStartEra() - 1)))
				// </advc.008a>
			{
				szBuffer.append(NEWLINE);
				// <advc.008a>
				if(bUnavailable)
					szBuffer.append(gDLL->getText("TXT_KEY_COLOR_NEGATIVE"));
				// </advc.008a>
				szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_MAX_START_ERA",
						GC.getInfo(kBuilding.getMaxStartEra()).getTextKeyWide()));
				// <advc.008a>
				if(bUnavailable)
					szBuffer.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));
				// </advc.008a>
			}
		}
		// advc.008a: REQUIRES_NUM_TEAMS moved up
	}
	else
	{
		if (!bTechChooserText && kBuilding.getPrereqAndTech() != NO_TECH)
		{
			if (ePlayer == NO_PLAYER ||
				!GET_TEAM(ePlayer).isHasTech(kBuilding.getPrereqAndTech()))
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_REQUIRES_STRING",
						GC.getInfo(kBuilding.getPrereqAndTech()).getTextKeyWide()));
			}
		}
		{
			bool bFirst = true;
			for (int i = 0; i < kBuilding.getNumPrereqAndTechs(); i++)
			{
				if (bTechChooserText || ePlayer == NO_PLAYER ||
					!GET_TEAM(ePlayer).isHasTech(kBuilding.getPrereqAndTechs(i)))
				{
					CvWString szTempBuffer;
					szTempBuffer.Format(L"%s%s", NEWLINE,
							gDLL->getText("TXT_KEY_REQUIRES").c_str());
					setListHelp(szBuffer, szTempBuffer,
							GC.getInfo(kBuilding.getPrereqAndTechs(i)).getDescription(),
							gDLL->getText("TXT_KEY_AND").c_str(), bFirst);
				}
			}
			// <advc.004w> Based on code copied from above
			if(kBuilding.getSpecialBuildingType() != NO_SPECIALBUILDING)
			{
				SpecialBuildingTypes eSpecial = kBuilding.getSpecialBuildingType();
				if(pCity == NULL || !GC.getGame().isSpecialBuildingValid(eSpecial))
				{
					TechTypes const eTechReq = GC.getInfo(eSpecial).getTechPrereq();
					if(eTechReq != NO_TECH)
					{
						szBuffer.append(NEWLINE);
						szBuffer.append(gDLL->getText("TXT_KEY_REQUIRES"));
						szBuffer.append(GC.getInfo(eTechReq).getDescription());
						szBuffer.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));
					}
				}
			} // </advc.004w>
			if (!bFirst)
				szBuffer.append(ENDCOLR);
		}
		{
			BonusTypes const ePrereqBonus = kBuilding.getPrereqAndBonus();
			if (ePrereqBonus != NO_BONUS)
			{
				if (pCity == NULL || !pCity->hasBonus(ePrereqBonus))
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_UNIT_REQUIRES_STRING",
							GC.getInfo(ePrereqBonus).getTextKeyWide()));
				}
			}
		}
		CvWStringBuffer szBonusList;
		bool bFirst = true;
		for (int i = 0; i < kBuilding.getNumPrereqOrBonuses(); i++)
		{
			BonusTypes const ePrereqBonus = kBuilding.getPrereqOrBonuses(i);
			if (pCity == NULL || !pCity->hasBonus(ePrereqBonus))
			{
				CvWString szTempBuffer;
				szTempBuffer.Format(L"%s%s", NEWLINE,
						gDLL->getText("TXT_KEY_REQUIRES").c_str());
				setListHelp(szBonusList, szTempBuffer,
						GC.getInfo(ePrereqBonus).getDescription(),
						gDLL->getText("TXT_KEY_OR").c_str(), bFirst);
			}
			else if (NULL != pCity)
			{
				bFirst = true;
				break;
			}
		}
		if (!bFirst)
		{
			szBonusList.append(ENDCOLR);
			szBuffer.append(szBonusList);
		}
		if (kBuilding.getFoundsCorporation() != NO_CORPORATION)
		{
			bFirst = true;
			szBonusList.clear();
			for (int i = 0; i < GC.getInfo(kBuilding.getFoundsCorporation()).
				getNumPrereqBonuses(); i++)
			{
				BonusTypes const eBonus = GC.getInfo(kBuilding.getFoundsCorporation()).
						getPrereqBonus(i);
				if (pCity == NULL || !pCity->hasBonus(eBonus))
				{
					CvWString szTempBuffer, szFirstBuffer;
					szFirstBuffer.Format(L"%s%s", NEWLINE,
							gDLL->getText("TXT_KEY_REQUIRES").c_str());
					szTempBuffer.Format(L"<link=literal>%s</link>",
							GC.getInfo(eBonus).getDescription());
					setListHelp(szBonusList, szFirstBuffer, szTempBuffer,
							gDLL->getText("TXT_KEY_OR"), bFirst);
				}
				else if (pCity != NULL)
				{
					bFirst = true;
					break;
				}
			}
			if (!bFirst)
			{
				szBonusList.append(ENDCOLR);
				szBuffer.append(szBonusList);
			}
		}
	}
}

// advc.179:
void CvGameTextMgr::buildBuildingReligionYieldString(CvWStringBuffer& szBuffer,
	CvBuildingInfo const& kBuilding)
{
	if (kBuilding.getVoteSourceType() == NO_VOTESOURCE)
		return;
	setYieldChangeHelp(szBuffer, L"", L"",
			L" " + gDLL->getText("TXT_KEY_BUILDING_RELIGION_YIELD",
			kBuilding.getDescription()),
			GC.getInfo(kBuilding.getVoteSourceType()).getReligionYield());
}


void CvGameTextMgr::setProjectHelp(CvWStringBuffer &szBuffer, ProjectTypes eProject,
	bool bCivilopediaText, CvCity* pCity)
{
	PROFILE_FUNC();

	if (eProject == NO_PROJECT)
		return;

	CvProjectInfo& kProject = GC.getInfo(eProject);
	PlayerTypes ePlayer = NO_PLAYER;
	if (pCity != NULL)
		ePlayer = pCity->getOwner();
	else ePlayer = getActivePlayer();

	CvWString szTempBuffer;

	if (!bCivilopediaText) // advc
	{
		szTempBuffer.Format( SETCOLR L"<link=literal>%s</link>" ENDCOLR,
				TEXT_COLOR("COLOR_PROJECT_TEXT"), kProject.getDescription());
		szBuffer.append(szTempBuffer);
	}
	if (!bCivilopediaText &&
		ePlayer != NO_PLAYER) // advc.004w: Civilopedia from opening menu
	{
		int iMaking = GET_TEAM(ePlayer).getProjectMaking(eProject); // advc.004w
		if (kProject.isWorldProject())
		{	// <advc.004w>
			int iMaxGlobal = kProject.getMaxGlobalInstances();
			szBuffer.append(NEWLINE); // newline in any case </advc.004w>
			if (pCity == NULL)
			{	// <advc.004w>
				if(iMaxGlobal == 1)
					szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_WORLD1"));
				else
				{
					szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_WORLD_NUM_ALLOWED",
						iMaxGlobal)); // </advc.004w>
				}
			}
			else
			{	// <advc.004w>
				if(iMaxGlobal == 1)
					szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_WORLD1"));
				else
				{
					szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_WORLD_NUM_LEFT",
						iMaxGlobal - GC.getGame().getProjectCreatedCount(eProject) -
						iMaking)); // </advc.004w>
				}
			}
		}
		if (kProject.isTeamProject())
		{	// <advc.004w>
			int iMaxTeam = kProject.getMaxTeamInstances();
			szBuffer.append(NEWLINE); // newline in any case </advc.004w>
			if (pCity == NULL)
			{	// <advc.004w>
				if(iMaxTeam == 1)
					szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_TEAM1"));
				else
				{
					szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_TEAM_NUM_ALLOWED",
							iMaxTeam)); // </advc.004w>
				}
			}
			else
			{	// <advc.004w>
				if(iMaxTeam == 1)
					szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_TEAM1"));
				else
				{
					szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_TEAM_NUM_LEFT",
							iMaxTeam - GET_TEAM(ePlayer).getProjectCount(eProject) -
							iMaking)); // </advc.004w>
				}
			}
		}
	}
	if (kProject.getNukeInterception() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_CHANCE_INTERCEPT_NUKES",
				kProject.getNukeInterception()));
	}
	if (kProject.getTechShare() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_TECH_SHARE",
				kProject.getTechShare()));
	}
	// doc: air experience
	if (kProject.getAirExperience() != 0)
	{
		szBuffer.append(NEWLINE);
		szTempBuffer.Format(L"%s%d", kProject.getAirExperience() > 0 ? L"+" : L"",
				kProject.getAirExperience());
		szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_AIR_EXPERIENCE",
				szTempBuffer.c_str()));
	}
	// doc: first air experience
	if (kProject.getFirstAirExperience() != 0)
	{
		szBuffer.append(NEWLINE);
		szTempBuffer.Format(L"%s%d", kProject.getFirstAirExperience() > 0 ? L"+" : L"",
				kProject.getFirstAirExperience());
		szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_FIRST_AIR_EXPERIENCE",
				szTempBuffer.c_str()));
	}
	if (kProject.isAllowsNukes())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_ENABLES_NUKES"));
	}
	// doc: satellite intercept
	if (kProject.isSatelliteIntercept())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_SATELLITE_INTERCEPT"));
	}
	// doc: satellite attack
	if (kProject.isSatelliteAttack())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_SATELLITE_ATTACK"));
	}
	// doc: golden age
	if (kProject.isGoldenAge())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_GOLDEN_AGE"));
	}
	// doc: first enemy anarchy
	if (kProject.isFirstEnemyAnarchy())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_FIRST_ENEMY_ANARCHY"));
	}
	// doc: reveals map
	if (kProject.isRevealsMap())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_REVEALS_MAP"));
	}
	// doc: enables special unit
	if (kProject.getSpecialUnit() != NO_SPECIALUNIT)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_ENABLES_SPECIAL_PLAYER",
				GC.getInfo(kProject.getSpecialUnit()).getTextKeyWide()));
	}
	if (kProject.getEveryoneSpecialUnit() != NO_SPECIALUNIT)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_ENABLES_SPECIAL",
				GC.getInfo(kProject.getEveryoneSpecialUnit()).getTextKeyWide()));
	}
	if (kProject.getEveryoneSpecialBuilding() != NO_SPECIALBUILDING)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_ENABLES_SPECIAL",
				GC.getInfo(kProject.getEveryoneSpecialBuilding()).getTextKeyWide()));
	}
	// doc: first free unit
	if (kProject.getFirstFreeUnit() != NO_UNIT)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_FIRST_FREE_UNIT",
				GC.getInfo(kProject.getFirstFreeUnit()).getTextKeyWide()));
	}
	// doc: free promotion
	if (kProject.getFreePromotion() != NO_PROMOTION)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_FREE_PROMOTION",
				GC.getInfo(kProject.getFreePromotion()).getTextKeyWide()));
	}
	// doc: Golden Record effect
	if (eProject == PROJECT_GOLDEN_RECORD)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_GOLDEN_RECORD_HELP"));
	}
	// doc: The Internet effect
	if (eProject == PROJECT_THE_INTERNET)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_THE_INTERNET_HELP"));
	}
	// doc: Human Genome Project effect
	if (eProject == PROJECT_HUMAN_GENOME_PROJECT)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_HUMAN_GENOME_PROJECT_HELP"));
	}
	// doc: International Space Station effect
	if (eProject == PROJECT_INTERNATIONAL_SPACE_STATION)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_INTERNATIONAL_SPACE_STATION_HELP"));
	}
	// doc: Great Firewall effect
	if (eProject == PROJECT_GREAT_FIREWALL)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_GREAT_FIREWALL_HELP"));
	}
	// doc: Lunar Colony effect
	if (eProject == PROJECT_LUNAR_COLONY)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_SPACESHIP_MOD_ALL_CITIES", 100));

		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_LUNAR_COLONY_HELP"));
	}
	FOR_EACH_NON_DEFAULT_PAIR(kProject.
		getVictoryThreshold(), Victory, int)
	{
		VictoryTypes const eLoopVictory = perVictoryVal.first;
		int const iThreshold = perVictoryVal.second;
		if (iThreshold == kProject.getVictoryMinThreshold(eLoopVictory))
			szTempBuffer.Format(L"%d", iThreshold);
		else
		{
			szTempBuffer.Format(L"%d-%d",
					kProject.getVictoryMinThreshold(eLoopVictory), iThreshold);
		}
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_REQUIRED_FOR_VICTORY",
				szTempBuffer.GetCString(),
				GC.getInfo(eLoopVictory).getTextKeyWide()));
	}
	CvWString szFirstBuffer;
	{
		bool bFirst = true;
		FOR_EACH_ENUM(Project)
		{
			if (GC.getInfo(eLoopProject).getAnyoneProjectPrereq() == eProject)
			{
				szFirstBuffer.Format(L"%s%s", NEWLINE, gDLL->getText(
						"TXT_KEY_PROJECT_REQUIRED_TO_CREATE_ANYONE").c_str());
				szTempBuffer.Format(SETCOLR L"<link=literal>%s</link>" ENDCOLR,
						TEXT_COLOR("COLOR_PROJECT_TEXT"), GC.getInfo(
						eLoopProject).getDescription());
				setListHelp(szBuffer, szFirstBuffer, szTempBuffer, L", ", bFirst);
			}
		}
	}
	{
		bool bFirst = true;
		FOR_EACH_ENUM(Project)
		{
			if (GC.getInfo(eLoopProject).getProjectsNeeded(eProject) > 0)
			{
				if (pCity == NULL || pCity->canCreate(eLoopProject, false, true))
				{
					szFirstBuffer.Format(L"%s%s", NEWLINE, gDLL->getText(
							"TXT_KEY_PROJECT_REQUIRED_TO_CREATE").c_str());
					szTempBuffer.Format(SETCOLR L"<link=literal>%s</link>" ENDCOLR,
							TEXT_COLOR("COLOR_PROJECT_TEXT"),
							GC.getInfo(eLoopProject).getDescription());
					setListHelp(szBuffer, szFirstBuffer, szTempBuffer, L", ", bFirst);
				}
			}
		}
	}
	if (pCity == NULL || !pCity->canCreate(eProject))
	{
		if (pCity != NULL && GC.getGame().isNoNukes() && kProject.isAllowsNukes())
		{
			FOR_EACH_ENUM(Unit)
			{
				if (GC.getInfo(eLoopUnit).isNuke())
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_NO_NUKES"));
					break;
				}
			}
		}
		if (kProject.getAnyoneProjectPrereq() != NO_PROJECT)
		{
			ProjectTypes eAnyonePrereq = (ProjectTypes)kProject.getAnyoneProjectPrereq();
			if (pCity == NULL || GC.getGame().getProjectCreatedCount(eAnyonePrereq) == 0)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_REQUIRES_ANYONE",
						GC.getInfo(eAnyonePrereq).getTextKeyWide()));
			}
		}
		FOR_EACH_NON_DEFAULT_PAIR(kProject.
			getProjectsNeeded(), Project, int)
		{
			ProjectTypes const eLoopProject = perProjectVal.first;
			int const iNeeded = perProjectVal.second;
			if (pCity == NULL || (GET_TEAM(ePlayer).getProjectCount(
				eLoopProject) < iNeeded))
			{
				if (pCity != NULL)
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_REQUIRES",
							GC.getInfo(eLoopProject).getTextKeyWide(),
							GET_TEAM(ePlayer).getProjectCount(eLoopProject),
							iNeeded));
				}
				else
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_REQUIRES_NO_CITY",
							GC.getInfo(eLoopProject).getTextKeyWide(),
							iNeeded));
				}
			}
		}
		if (bCivilopediaText)
		{
			if (kProject.getVictoryPrereq() != NO_VICTORY)
			{	// <advc.008a>
				if(ePlayer == NO_PLAYER ||
					!GC.getGame().isVictoryValid(kProject.getVictoryPrereq()))
				{
					if(ePlayer != NO_PLAYER)
						szBuffer.append(gDLL->getText("TXT_KEY_COLOR_NEGATIVE"));
					// </advc.008a>
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_REQUIRES_STRING_VICTORY",
							GC.getInfo(kProject.getVictoryPrereq()).getTextKeyWide()));
					// <advc.008a>
					if(ePlayer != NO_PLAYER)
						szBuffer.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));
					// </advc.008a>
				}
			}
		}
	}
	if (pCity == NULL)
	{
		if (!bCivilopediaText) // advc.004y
		{
			int iCost=-1; // advc.251
			if (ePlayer != NO_PLAYER)
				iCost = GET_PLAYER(ePlayer).getProductionNeeded(eProject);
			else
			{
				// <advc.251>
				int const iBaseCost = kProject.getProductionCost();
				iCost = iBaseCost;
				iCost *= GC.getDefineINT("PROJECT_PRODUCTION_PERCENT");
				iCost /= 100;
				// To match CvPlayer::getProductionNeeded
				iCost = fmath::roundToMultiple(iCost, iBaseCost > 500 ? 50 : 5);
				// </advc.251>
			}
			szTempBuffer.Format(L"\n%d%c", iCost,
					GC.getInfo(YIELD_PRODUCTION).getChar());
			szBuffer.append(szTempBuffer);
		}
	}
	else
	{
		szBuffer.append(NEWLINE);
		int iTurns = pCity->getProductionTurnsLeft(eProject,
				(GC.ctrlKey() || !GC.shiftKey()) ? 0 :
				pCity->getOrderQueueLength());
		if(iTurns < MAX_INT) // advc.004x
		{
			szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_NUM_TURNS", iTurns));
			szBuffer.append(L" - "); // advc.004x: Moved up
		}

		int iProduction = pCity->getProjectProduction(eProject);
		if (iProduction > 0)
		{
			szTempBuffer.Format(L"%d/%d%c", iProduction,
					pCity->getProductionNeeded(eProject),
					GC.getInfo(YIELD_PRODUCTION).getChar());
		}
		else
		{
			szTempBuffer.Format(L"%d%c",
					pCity->getProductionNeeded(eProject),
					GC.getInfo(YIELD_PRODUCTION).getChar());
		}
		szBuffer.append(szTempBuffer);
	}
	// doc: existing building production modifier
	if (kProject.getExistingProductionModifier() != 0)
	{
		if (GC.getGame().isFinalInitialized() && GC.getGame().getProjectCreatedCount(eProject) > 0)
			szBuffer.append(gDLL->getText("TXT_KEY_COLOR_POSITIVE"));
		else szBuffer.append(gDLL->getText("TXT_KEY_COLOR_NEGATIVE"));

		if (!bCivilopediaText)
			szBuffer.append(L" (");
		else
		{
			szTempBuffer.Format(L"%s%c", NEWLINE, gDLL->getSymbolID(BULLET_CHAR), szTempBuffer);
			szBuffer.append(szTempBuffer);
		}

		if (kProject.getExistingProductionModifier() == 100)
			szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_DOUBLE_SPEED_EXISTING"));
		else
			szBuffer.append(gDLL->getText("TXT_KEY_PROJECT_BUILDS_FASTER_EXISTING", kProject.getExistingProductionModifier()));

		if (!bCivilopediaText)
			szBuffer.append(L')');
		if (pCity != NULL)
			szBuffer.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));
	}
	FOR_EACH_NON_DEFAULT_PAIR(kProject.
		getBonusProductionModifier(), Bonus, int)
	{
		if (pCity != NULL)
		{
			if (pCity->hasBonus(perBonusVal.first))
				szBuffer.append(gDLL->getText("TXT_KEY_COLOR_POSITIVE"));
			else szBuffer.append(gDLL->getText("TXT_KEY_COLOR_NEGATIVE"));
		}
		if (!bCivilopediaText)
			szBuffer.append(L" (");
		else
		{
			szTempBuffer.Format(L"%s%c", NEWLINE, gDLL->getSymbolID(BULLET_CHAR));
			szBuffer.append(szTempBuffer);
		}
		if (perBonusVal.second == 100)
		{
			szBuffer.append(gDLL->getText(
					//"TXT_KEY_PROJECT_DOUBLE_SPEED_WITH",
					"TXT_KEY_DOUBLE_PRODUCTION_WITH", // advc.004w
					GC.getInfo(perBonusVal.first).getTextKeyWide()));
		}
		else
		{
			szBuffer.append(gDLL->getText(
					//TXT_KEY_PROJECT_BUILDS_FASTER_WITH",
					"TXT_KEY_FASTER_PRODUCTION_WITH", // advc.004w
					perBonusVal.second,
					GC.getInfo(perBonusVal.first).getTextKeyWide()));
		}
		if (!bCivilopediaText)
			szBuffer.append(L')');
		if (pCity != NULL)
			szBuffer.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));
	}
	// K-Mod
	if (pCity != NULL && //gDLL->getChtLvl() > 0
		GC.getGame().isDebugMode() && // advc.135c
		GC.ctrlKey())
	{
		CvCityAI const& kCityAI = pCity->AI();
		int iValue = kCityAI.AI_projectValue(eProject);
		szBuffer.append(CvWString::format(L"\nProject Value (base) = %d", iValue));

		ProjectTypes eBestProject = kCityAI.AI_bestProject(&iValue,
				true); // advc.001n
		if (eBestProject == eProject)
		{
			szBuffer.append(CvWString::format(
					SETCOLR L"\n(Best project value (scaled) = %d)" ENDCOLR,
					TEXT_COLOR("COLOR_LIGHT_GREY"), iValue));
		}
	} // K-Mod end
}


void CvGameTextMgr::setProcessHelp(CvWStringBuffer &szBuffer, ProcessTypes eProcess)
{
	szBuffer.append(GC.getInfo(eProcess).getDescription());
	FOR_EACH_ENUM(Commerce)
	{
		int iProductionToCommerceModifier = GC.getInfo(eProcess).getProductionToCommerceModifier(eLoopCommerce);
		if (iProductionToCommerceModifier != 0)
		{
			// doc: process modifier
			if (eActivePlayer != NO_PLAYER)
				iProductionToCommerceModifier += GET_PLAYER(eActivePlayer).getProcessModifier();

			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_PROCESS_CONVERTS",
					iProductionToCommerceModifier,
					GC.getInfo(YIELD_PRODUCTION).getChar(),
					GC.getInfo(eLoopCommerce).getChar()));
		}
	}
}

// BULL - Production Decay: (advc.094)
void CvGameTextMgr::setProductionDecayHelp(CvWStringBuffer &szBuffer,
	int iTurnsLeft, int iThreshold, int iDecay, bool bProducing)
{
	if (iTurnsLeft <= 1)
	{
		if (bProducing)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_PRODUCTION_DECAY_PRODUCING",
					iDecay));
		}
		else
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_PRODUCTION_DECAY",
					iDecay));
		}
	}
	else
	{
		if (iTurnsLeft <= iThreshold)
		{
			if (bProducing)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_PRODUCTION_DECAY_TURNS_PRODUCING",
						iDecay, iTurnsLeft));
			}
			else
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_PRODUCTION_DECAY_TURNS",
						iDecay, iTurnsLeft));
			}
		}
	}
}

// advc.901: Based on code cut from setBadHealthHelp, setGoodHealthHelp.
namespace
{
	/*	If all health from surroundings of iSign can be attributed to one type
		of feature, return that feature type, otherwise NO_FEATURE. */
	FeatureTypes getSurroundingHealthFeature(CvCity const& kCity, int iSign,
		bool& bOnlyFeatureHealth)
	{
		bOnlyFeatureHealth = false;
		FeatureTypes eHealthFeature = NO_FEATURE;
		bool bMultipleHealthFeatures = false;
		for (CityPlotIter it(kCity); it.hasNext(); ++it)
		{
			CvPlot const& kPlot = *it;
			ImprovementTypes const eImprov = kPlot.getImprovementType();
			int iImprovHealthPercent = 0;
			if (eImprov != NO_IMPROVEMENT)
			{
				iImprovHealthPercent = GC.getInfo(eImprov).get(
						CvImprovementInfo::HealthPercent);
				if (!GET_TEAM(getActiveTeam()).canAccessHappyHealth(kPlot,
					iImprovHealthPercent))
				{
					iImprovHealthPercent = 0;
				}
			}
			FeatureTypes const eFeature = kPlot.getFeatureType();
			int iFeatureHealthPercent = 0;
			if (eFeature != NO_FEATURE)
			{
				iFeatureHealthPercent = GC.getInfo(eFeature).getHealthPercent();
				if (!GET_TEAM(getActiveTeam()).canAccessHappyHealth(kPlot,
					iFeatureHealthPercent))
				{
					iFeatureHealthPercent = 0;
				}
			}
			/*	Improvements on top of a feature can be lumped together under the
				feature's name if the signs match. Not improvements w/o feature. */
			if (iImprovHealthPercent != 0 && iFeatureHealthPercent * iImprovHealthPercent <= 0)
			{
				bOnlyFeatureHealth = false;
				return NO_FEATURE;
			}
			/*	Require iSign. Note that good and bad surrounding health are
				tallied and rounded separately. */
			if (iFeatureHealthPercent * iSign > 0 &&
				/*	If improv and feature have the same sign (Preserved Forest),
					we can attribute it all to the feature. Not if signs are
					opposed (Preserved Jungle). */
				iFeatureHealthPercent * iImprovHealthPercent >= 0)
			{
				if (eHealthFeature == NO_FEATURE)
				{	/*	Found a relevant feature,
						but it might not be the only one. */
					eHealthFeature = kPlot.getFeatureType();
				}
				else if (eHealthFeature != kPlot.getFeatureType())
					bMultipleHealthFeatures = true;
			}
		}
		bOnlyFeatureHealth = (eHealthFeature != NO_FEATURE);
		if (bMultipleHealthFeatures)
			return NO_FEATURE;
		return eHealthFeature;
	}
}


void CvGameTextMgr::setBadHealthHelp(CvWStringBuffer &szBuffer, CvCity const& kCity)
{
	if (kCity.badHealth() <= 0)
		return;
	{
		int iHealth = kCity.getFreshWaterBadHealth();
		if (iHealth < 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_FROM_FRESH_WATER", -iHealth));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int iHealth = kCity.getSurroundingBadHealth();
		if (iHealth < 0)
		{	// <advc.901>
			bool bOnlyFeatures;
			FeatureTypes eFeature = getSurroundingHealthFeature(kCity, iHealth,
					bOnlyFeatures); // </advc.901>
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_FEAT_HEALTH", -iHealth,
					/* <advc.901> */ (eFeature == NO_FEATURE ?
					(bOnlyFeatures ? L"TXT_KEY_MISC_FEATURES" :
					L"TXT_KEY_MISC_SURROUNDINGS") : // </advc.901>
					GC.getInfo(eFeature).getTextKeyWide())));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int iBadHealth = kCity.getEspionageHealthCounter();
		if (iBadHealth > 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HEALTH_FROM_ESPIONAGE", iBadHealth));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int iHealth = kCity.getPowerBadHealth();
		if (iHealth < 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HEALTH_FROM_POWER", -iHealth));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int iHealth = kCity.getBonusBadHealth();
		if (iHealth < 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HEALTH_FROM_BONUSES", -iHealth));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int iHealth = kCity.totalBadBuildingHealth();
		if (iHealth < 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HEALTH_FROM_BUILDINGS", -iHealth));
			szBuffer.append(NEWLINE);
		}
	}
	// doc: improvement health
	{
		iHealth = city.getImprovementHealth();
		if (iHealth < 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HEALTH_FROM_IMPROVEMENTS", -iHealth));
			szBuffer.append(NEWLINE);
		}
	}
	// Leoreth
	{
		iHealth = city.getCorporationUnhealth();
		if (iHealth < 0)
		{
			iTotalHealth += iHealth;
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HEALTH_FROM_CORPORATIONS", -iHealth));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int iHealth = GET_PLAYER(kCity.getOwner()).getExtraHealth();
		if (iHealth < 0)
		{
			//szBuffer.append(gDLL->getText("TXT_KEY_MISC_HEALTH_FROM_CIV", -iHealth));
			// <advc.004g>
			szBuffer.append(CvWString::format(L"%d%c ", -iHealth,
					gDLL->getSymbolID(UNHEALTHY_CHAR)));
			szBuffer.append(gDLL->getText("TXT_KEY_FROM_TRAIT")); // </advc.004g>
			szBuffer.append(NEWLINE);
		}
	}
	{
		int iHealth = kCity.getExtraHealth();
		if (iHealth < 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_UNHEALTH_EXTRA", -iHealth));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int iHealth = GC.getInfo(kCity.getHandicapType()).getHealthBonusByID(city.getOwner()); // rfc: civilization based health modifier
		if (iHealth < 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HEALTH_FROM_HANDICAP", -iHealth));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int iBadHealth = kCity.unhealthyPopulation();
		if (iBadHealth > 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HEALTH_FROM_POP", iBadHealth));
			// K-Mod, 29/dec/10: added modifier text
			if (kCity.getUnhealthyPopulationModifier() != 0)
			{
				wchar szTempBuffer[1024];
				swprintf(szTempBuffer, 1024, L" (%+d%%)",
						kCity.getUnhealthyPopulationModifier());
				szBuffer.append(szTempBuffer);
			} // K-Mod end
			szBuffer.append(NEWLINE);
		}
	}
	szBuffer.append(L"-----------------------\n");
	szBuffer.append(gDLL->getText("TXT_KEY_MISC_TOTAL_UNHEALTHY", kCity.badHealth()));
}


void CvGameTextMgr::setGoodHealthHelp(CvWStringBuffer &szBuffer, CvCity const& kCity)
{
	if (kCity.goodHealth() <= 0)
		return;
	{
		int iHealth = kCity.getFreshWaterGoodHealth();
		if (iHealth > 0)
		{
			szBuffer.append(gDLL->getText(
					"TXT_KEY_MISC_HEALTH_FROM_FRESH_WATER", iHealth));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int iHealth = kCity.getSurroundingGoodHealth();
		if (iHealth > 0)
		{	// <advc.901>
			bool bOnlyFeatures;
			FeatureTypes eFeature = getSurroundingHealthFeature(kCity, iHealth,
					bOnlyFeatures); // </advc.901>
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_FEAT_GOOD_HEALTH", iHealth,
					/* <advc.901> */ (eFeature == NO_FEATURE ?
					(bOnlyFeatures ? L"TXT_KEY_MISC_FEATURES" :
					L"TXT_KEY_MISC_SURROUNDINGS") : // </advc.901>
					GC.getInfo(eFeature).getTextKeyWide())));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int iHealth = kCity.getPowerGoodHealth();
		if (iHealth > 0)
		{
			szBuffer.append(gDLL->getText(
					"TXT_KEY_MISC_GOOD_HEALTH_FROM_POWER", iHealth));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int iHealth = kCity.getBonusGoodHealth();
		if (iHealth > 0)
		{
			szBuffer.append(gDLL->getText(
					"TXT_KEY_MISC_GOOD_HEALTH_FROM_BONUSES", iHealth));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int iHealth = kCity.totalGoodBuildingHealth();
		if (iHealth > 0)
		{
			szBuffer.append(gDLL->getText(
					"TXT_KEY_MISC_GOOD_HEALTH_FROM_BUILDINGS", iHealth));
			szBuffer.append(NEWLINE);
		}
	}
	// doc: corporation health
	{
		int iHealth = city.getCorporationHealth();
		if (iHealth > 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HEALTH_GOOD_HEALTH_FROM_CORPORATIONS", iHealth));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int iHealth = GET_PLAYER(kCity.getOwner()).getExtraHealth();
		if (iHealth > 0)
		{
			//szBuffer.append(gDLL->getText("TXT_KEY_MISC_GOOD_HEALTH_FROM_CIV", iHealth));
			// <advc.004g>
			szBuffer.append(CvWString::format(L"+%d%c ",
					iHealth, gDLL->getSymbolID(HEALTHY_CHAR)));
			szBuffer.append(gDLL->getText("TXT_KEY_FROM_TRAIT")); // </advc.004g>
			szBuffer.append(NEWLINE);
		}
	}
	{
		int iHealth = kCity.getExtraHealth();
		if (iHealth > 0)
		{
			szBuffer.append(gDLL->getText(
					"TXT_KEY_MISC_HEALTH_EXTRA", iHealth));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int iHealth = GC.getInfo(kCity.getHandicapType()).getHealthBonusByID(city.getOwner()); // rfc: civilization based health modifier
		if (iHealth > 0)
		{
			szBuffer.append(gDLL->getText(
					"TXT_KEY_MISC_GOOD_HEALTH_FROM_HANDICAP", iHealth));
			szBuffer.append(NEWLINE);
		}
	}
	szBuffer.append(L"-----------------------\n");
	szBuffer.append(gDLL->getText("TXT_KEY_MISC_TOTAL_HEALTHY", kCity.goodHealth()));
}

// <advc.004b>
void CvGameTextMgr::setFoundHealthHelp(CvWStringBuffer& szBuffer, CvPlot const& kCityPlot)
{
	int iGoodHealthPercent = 0;
	int iBadHealthPercent = 0;
	// bIncludeCityPlot=false b/c feature gets removed upon founding
	for (CityPlotIter it(kCityPlot, false); it.hasNext(); ++it)
	{
		CvPlot const& p = *it;
		if (!p.isFeature() || !p.isRevealed(getActiveTeam()))
			continue;
		int iHealthPercent = GC.getInfo(p.getFeatureType()).getHealthPercent();
		if (!GET_TEAM(getActiveTeam()).canAccessHappyHealth(p, iHealthPercent))
			continue;
		if (iHealthPercent > 0)
			iGoodHealthPercent += iHealthPercent;
		else iBadHealthPercent -= iHealthPercent;
	}
	if (kCityPlot.isFreshWater())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_HEALTH_FROM_FRESH_WATER",
				GC.getDefineINT(CvGlobals::FRESH_WATER_HEALTH_CHANGE)));
	}
	int iGoodHealth = iGoodHealthPercent / 100;
	int iBadHealth = iBadHealthPercent / 100;
	if (iGoodHealth > 0 || iBadHealth > 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(L"+");
		int iIcon = 0;
		if (iGoodHealth > 0)
		{
			iIcon = gDLL->getSymbolID(HEALTHY_CHAR);
			/*  Turns out good and bad health are rounded individually;
				no need, then, to show fractions. */
			// float fGoodHealth = iGoodHealthPercent / 100.0f;
			//szRetVal.append(CvWString::format((iGoodHealthPercent % 10 == 0 ?
			//		L"%.1f%c" : L"%.2f%c"), fGoodHealth, iIcon));
			szBuffer.append(CvWString::format(L"%d%c", iGoodHealth, iIcon));
		}
		if (iBadHealth > 0)
		{
			if (iGoodHealth > 0)
				szBuffer.append(CvWString::format(L", "));
			iIcon = gDLL->getSymbolID(UNHEALTHY_CHAR);
			szBuffer.append(CvWString::format(L"%d%c", iBadHealth, iIcon));
		}
		szBuffer.append(gDLL->getText("TXT_KEY_FROM_FEATURES"));
	}
	int iExtraHealth = GET_PLAYER(getActivePlayer()).getExtraHealth();
	if (iExtraHealth != 0)
	{
		szBuffer.append(NEWLINE);
		int iIcon = 0;
		szBuffer.append(L"+");
		if (iExtraHealth > 0)
		{
			iIcon = gDLL->getSymbolID(HEALTHY_CHAR);
			szBuffer.append(CvWString::format(L"%d%c", iExtraHealth, iIcon));
		}
		else
		{
			iIcon = gDLL->getSymbolID(UNHEALTHY_CHAR);
			szBuffer.append(CvWString::format(L"%d%c", iBadHealth, iIcon));
		}
		szBuffer.append(gDLL->getText("TXT_KEY_FROM_TRAIT"));
	}
}


void CvGameTextMgr::setFoundCostHelp(CvWStringBuffer& szBuffer, CvPlot const& kCityPlot)
{
	CvPlayer const& kPlayer = GET_PLAYER(getActivePlayer());
	if (kPlayer.isAnarchy())
		return;
	int iProjPreInfl = 0;
	// New city increases other cities' maintenance
	FOR_EACH_CITY (c, kPlayer)
	{
		if (c->isDisorder()) // Can't account for these
			continue;
		int iProjected = // Distance and corp. maintenance stay the same
				c->calculateDistanceMaintenanceTimes100() +
				c->calculateCorporationMaintenanceTimes100() +
				CvCity::calculateNumCitiesMaintenanceTimes100(*c->plot(),
				kPlayer.getID(), c->getPopulation(), 1) +
				CvCity::calculateColonyMaintenanceTimes100(*c->plot(),
				kPlayer.getID(), c->getPopulation(), 1);
		// Snippet from CvCity::updateMaintenance
		iProjPreInfl += (iProjected *
				std::max(0, c->getMaintenanceModifier() + 100)) / 100;
	}
	int iNewCityMaint =
			CvCity::calculateDistanceMaintenanceTimes100(
			kCityPlot, kPlayer.getID()) +
			// Last param: +1 for the newly founded city
			CvCity::calculateNumCitiesMaintenanceTimes100(
			kCityPlot, kPlayer.getID(), -1, 1) +
			CvCity::calculateColonyMaintenanceTimes100(
			kCityPlot, kPlayer.getID());
	iProjPreInfl += iNewCityMaint;
	iProjPreInfl /= 100;
	// Civic upkeep
	iProjPreInfl += kPlayer.getCivicUpkeep(NULL, true, 1);
	// Unit cost (new city increases free units, Settler unit goes away)
	iProjPreInfl += kPlayer.calculateUnitCost(CvCity::initialPopulation(), -1);
	// Unit supply (Settler unit goes away)
	if (kPlayer.calculateUnitSupply(kCityPlot.getOwner() != kPlayer.getID()))
		iProjPreInfl--;
	// Inflation
	int iCost = (iProjPreInfl * (kPlayer.calculateInflationRate() + 100)) / 100;
	// Difference from current expenses
	iCost -= kPlayer.calculateInflatedCosts();
	/* Could, in theory, be negative due to unit cost. Don't output
	   a negative cost (too confusing). */
	iCost = std::max(0, iCost);
	szBuffer.append(NEWLINE);
	CvWString szCostStr = CvWString::format(L"%d", iCost);
	szBuffer.append(gDLL->getText("TXT_KEY_PROJECTED_COST", szCostStr.c_str()));
}


void CvGameTextMgr::setHomePlotYieldHelp(CvWStringBuffer& szBuffer, CvPlot const& kCityPlot)
{
	szBuffer.append(NEWLINE);
	szBuffer.append(gDLL->getText("TXT_KEY_HOME_TILE_YIELD"));
	FOR_EACH_ENUM(Yield)
	{
		int iYieldRate = kCityPlot.calculateNatureYield(
				eLoopYield, getActiveTeam(), true);
		CvYieldInfo const& kLoopYield = GC.getInfo(eLoopYield);
		iYieldRate = std::max(iYieldRate, kLoopYield.getMinCity());
		if (iYieldRate == 0)
			continue;
		CvWString szYield = CvWString::format(L", %d%c", iYieldRate, kLoopYield.getChar());
		szBuffer.append(szYield);
	}
} // </advc.004b>

// BUG - Building Additional Health - start
bool CvGameTextMgr::setBuildingAdditionalHealthHelp(CvWStringBuffer &szBuffer, const CvCity& city, const CvWString& szStart, bool bStarted)
{
	CvWString szLabel;

	CvCivilization const& kCiv = city.getCivilization(); // advc.003w
	for (int i = 0; i < kCiv.getNumBuildings(); i++)
	{
		BuildingTypes eBuilding = kCiv.buildingAt(i);
		if (city.canConstruct(eBuilding, false, true, false))
		{
			int iGood = 0, iBad = 0;
			//int iChange = // advc: unused
			  city.getAdditionalHealthByBuilding(eBuilding, iGood, iBad);

			if (iGood != 0 || iBad != 0)
			{
				int iSpoiledFood = city.getAdditionalSpoiledFood(iGood, iBad);
				int iStarvation = city.getAdditionalStarvation(iSpoiledFood);

				if (!bStarted)
				{
					szBuffer.append(szStart);
					bStarted = true;
				}

				szLabel.Format(SETCOLR L"%s" ENDCOLR, TEXT_COLOR("COLOR_BUILDING_TEXT"), GC.getInfo(eBuilding).getDescription());
				bool bStartedLine = setGoodBadChangeHelp(szBuffer, szLabel, L": ", L"", iGood, gDLL->getSymbolID(HEALTHY_CHAR), iBad,
						gDLL->getSymbolID(UNHEALTHY_CHAR), false, true);
				setValueChangeHelp(szBuffer, szLabel, L": ", L"", iSpoiledFood, gDLL->getSymbolID(EATEN_FOOD_CHAR), false, true, bStartedLine);
				setValueChangeHelp(szBuffer, szLabel, L": ", L"", iStarvation, gDLL->getSymbolID(BAD_FOOD_CHAR), false, true, bStartedLine);
			}
		}
	}

	return bStarted;
}
// BUG - Building Additional Health - end

void CvGameTextMgr::setAngerHelp(CvWStringBuffer &szBuffer, CvCity const& kCity)
{
	if (kCity.isOccupation())
	{
		szBuffer.append(gDLL->getText("TXT_KEY_ANGER_RESISTANCE"));
		return;
	}
	if (GET_PLAYER(kCity.getOwner()).isAnarchy())
	{
		szBuffer.append(gDLL->getText("TXT_KEY_ANGER_ANARCHY"));
		return;
	}
	int const iUnhappy = kCity.unhappyLevel();
	if (iUnhappy <= 0)
		return;

	int iNewAngerPercent = 0;
	int iNewAnger = 0;
	// K-Mod, 5/jan/11: all anger perecent bits were like this:
	//iNewAnger += (((iNewAngerPercent * kCity.getPopulation()) / GC.getPERCENT_ANGER_DIVISOR()) - ((iOldAngerPercent * kCity.getPopulation()) / GC.getDefineINT("PERCENT_ANGER_DIVISOR")));
	// I've changed it to use GC.getPERCENT_ANGER_DIVISOR() for both parts.
	// XXX decomp these???
	{
		int const iOldAngerPercent = 0;
		int const iOldAnger = 0;
		iNewAngerPercent += kCity.getOvercrowdingPercentAnger();
		iNewAnger += (iNewAngerPercent * kCity.getPopulation()) / GC.getPERCENT_ANGER_DIVISOR()
				- (iOldAngerPercent * kCity.getPopulation()) / GC.getPERCENT_ANGER_DIVISOR();
		int iAnger = iNewAnger - iOldAnger + std::min(0, iOldAnger);
		if (iAnger > 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ANGER_OVERCROWDING", iAnger));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int const iOldAngerPercent = iNewAngerPercent;
		int const iOldAnger = iNewAnger;
		iNewAngerPercent += kCity.getNoMilitaryPercentAnger();
		iNewAnger += (iNewAngerPercent * kCity.getPopulation()) / GC.getPERCENT_ANGER_DIVISOR()
				- (iOldAngerPercent * kCity.getPopulation()) / GC.getPERCENT_ANGER_DIVISOR();
		int iAnger = iNewAnger - iOldAnger + std::min(0, iOldAnger);
		if (iAnger > 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ANGER_MILITARY_PROTECTION", iAnger));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int const iOldAngerPercent = iNewAngerPercent;
		int const iOldAnger = iNewAnger;
		iNewAngerPercent += kCity.getCulturePercentAnger();
		iNewAnger += (iNewAngerPercent * kCity.getPopulation()) / GC.getPERCENT_ANGER_DIVISOR()
				- (iOldAngerPercent * kCity.getPopulation()) / GC.getPERCENT_ANGER_DIVISOR();
		int iAnger = iNewAnger - iOldAnger + std::min(0, iOldAnger);
		if (iAnger > 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ANGER_OCCUPIED", iAnger));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int const iOldAngerPercent = iNewAngerPercent;
		int const iOldAnger = iNewAnger;
		iNewAngerPercent += kCity.getReligionPercentAnger();
		iNewAnger += (iNewAngerPercent * kCity.getPopulation()) / GC.getPERCENT_ANGER_DIVISOR()
				- (iOldAngerPercent * kCity.getPopulation()) / GC.getPERCENT_ANGER_DIVISOR();
		int iAnger = iNewAnger - iOldAnger + std::min(0, iOldAnger);
		if (iAnger > 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ANGER_RELIGION_FIGHT", iAnger));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int const iOldAngerPercent = iNewAngerPercent;
		int const iOldAnger = iNewAnger;
		iNewAngerPercent += kCity.getHurryPercentAnger();
		iNewAnger += (iNewAngerPercent * kCity.getPopulation()) / GC.getPERCENT_ANGER_DIVISOR()
				- (iOldAngerPercent * kCity.getPopulation()) / GC.getPERCENT_ANGER_DIVISOR();
		int iAnger = iNewAnger - iOldAnger + std::min(0, iOldAnger);
		if (iAnger > 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ANGER_OPPRESSION", iAnger,
					kCity.getHurryAngerTimer())); // advc.188
			szBuffer.append(NEWLINE);
		}
	}
	{
		int const iOldAngerPercent = iNewAngerPercent;
		int const iOldAnger = iNewAnger;
		iNewAngerPercent += kCity.getConscriptPercentAnger();
		iNewAnger += (iNewAngerPercent * kCity.getPopulation()) / GC.getPERCENT_ANGER_DIVISOR()
				- (iOldAngerPercent * kCity.getPopulation()) / GC.getPERCENT_ANGER_DIVISOR();
		int iAnger = iNewAnger - iOldAnger + std::min(0, iOldAnger);
		if (iAnger > 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ANGER_DRAFT", iAnger,
					kCity.getConscriptAngerTimer())); // advc.188
			szBuffer.append(NEWLINE);
		}
	}
	{
		int const iOldAngerPercent = iNewAngerPercent;
		int const iOldAnger = iNewAnger;
		iNewAngerPercent += kCity.getDefyResolutionPercentAnger();
		iNewAnger += (iNewAngerPercent * kCity.getPopulation()) / GC.getPERCENT_ANGER_DIVISOR()
				- (iOldAngerPercent * kCity.getPopulation()) / GC.getPERCENT_ANGER_DIVISOR();
		int iAnger = iNewAnger - iOldAnger + std::min(0, iOldAnger);
		if (iAnger > 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ANGER_DEFY_RESOLUTION", iAnger,
					kCity.getDefyResolutionAngerTimer())); // advc.188
			szBuffer.append(NEWLINE);
		}
	}
	{
		int const iOldAngerPercent = iNewAngerPercent;
		int const iOldAnger = iNewAnger;
		iNewAngerPercent += kCity.getWarWearinessPercentAnger();
		iNewAnger += (iNewAngerPercent * kCity.getPopulation()) / GC.getPERCENT_ANGER_DIVISOR()
				- (iOldAngerPercent * kCity.getPopulation()) / GC.getPERCENT_ANGER_DIVISOR();
		int iAnger = iNewAnger - iOldAnger + std::min(0, iOldAnger);
		if (iAnger > 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ANGER_WAR_WEAR", iAnger));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int const iOldAngerPercent = iNewAngerPercent;
		int const iOldAnger = iNewAnger;
		/*	K-Mod, 30/dec/10, Global warming unhappiness (start)
			when I say 'percent' I mean 1/100. Unfortunately,
			people who made the rest of the game meant something else...
			so I have to multiply my GwPercentAnger by 10 to make it fit in. */
		iNewAngerPercent += std::max(0,
				GET_PLAYER(kCity.getOwner()).getGwPercentAnger() * 10);
		iNewAnger += (iNewAngerPercent * kCity.getPopulation()) / GC.getPERCENT_ANGER_DIVISOR()
				- (iOldAngerPercent * kCity.getPopulation()) / GC.getPERCENT_ANGER_DIVISOR();
		int iAnger = iNewAnger - iOldAnger + std::min(0, iOldAnger);
		if (iAnger > 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ANGER_GLOBAL_WARMING", iAnger));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int const iOldAnger = iNewAnger;
		// K-Mod end
		iNewAnger += std::max(0, kCity.getVassalUnhappiness());
		int iAnger = iNewAnger - iOldAnger + std::min(0, iOldAnger);
		if (iAnger > 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_UNHAPPY_VASSAL", iAnger));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int const iOldAnger = iNewAnger;
		iNewAnger += std::max(0, kCity.getEspionageHappinessCounter());
		int iAnger = iNewAnger - iOldAnger + std::min(0, iOldAnger);
		if (iAnger > 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ANGER_ESPIONAGE", iAnger));
			szBuffer.append(NEWLINE);
		}
	}

	FOR_EACH_ENUM(Civic)
	{
		int const iOldAngerPercent = iNewAngerPercent;
		int const iOldAnger = iNewAnger;
		iNewAngerPercent += GET_PLAYER(kCity.getOwner()).getCivicPercentAnger(eLoopCivic);
		iNewAnger += (iNewAngerPercent * kCity.getPopulation()) / GC.getPERCENT_ANGER_DIVISOR()
				- (iOldAngerPercent * kCity.getPopulation()) / GC.getPERCENT_ANGER_DIVISOR();
		int iAnger = iNewAnger - iOldAnger + std::min(0, iOldAnger);
		if (iAnger > 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ANGER_DEMAND_CIVIC", iAnger,
					GC.getInfo(eLoopCivic).getTextKeyWide()));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int const iOldAnger = iNewAnger;
		iNewAnger -= std::min(0, kCity.getLargestCityHappiness());
		int iAnger = iNewAnger - iOldAnger + std::min(0, iOldAnger);
		if (iAnger > 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ANGER_BIG_CITY", iAnger));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int const iOldAnger = iNewAnger;
		iNewAnger -= std::min(0, kCity.getMilitaryHappiness());
		int iAnger = iNewAnger - iOldAnger + std::min(0, iOldAnger);
		if (iAnger > 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ANGER_MILITARY_PRESENCE", iAnger));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int const iOldAnger = iNewAnger;
		iNewAnger -= std::min(0, kCity.getCurrentStateReligionHappiness());
		int iAnger = iNewAnger - iOldAnger + std::min(0, iOldAnger);
		if (iAnger > 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ANGER_STATE_RELIGION", iAnger));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int const iOldAnger = iNewAnger;
		iNewAnger -= std::min(0,
				kCity.getBuildingBadHappiness() + kCity.getExtraBuildingBadHappiness());
		int iAnger = iNewAnger - iOldAnger + std::min(0, iOldAnger);
		if (iAnger > 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ANGER_BUILDINGS", iAnger));
			szBuffer.append(NEWLINE);
		}
	}
	// doc: improvement happiness
	// TODO: redundant with surrounding happiness?
	{
		int const iOldAnger = iNewAnger;

		iNewAnger -= std::min(0, city.getImprovementHappiness());
		iAnger = ((iNewAnger - iOldAnger) + std::min(0, iOldAnger));
		if (iAnger > 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ANGER_IMPROVEMENTS", iAnger));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int const iOldAnger = iNewAnger;
		iNewAnger -= std::min(0, kCity.getSurroundingBadHappiness());
		int iAnger = iNewAnger - iOldAnger + std::min(0, iOldAnger);
		if (iAnger > 0)
		{
			// advc.059: Text key was ..._FEATURES
			szBuffer.append(gDLL->getText("TXT_KEY_ANGER_SURROUNDINGS", iAnger));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int const iOldAnger = iNewAnger;
		iNewAnger -= std::min(0, kCity.getBonusBadHappiness());
		int iAnger = iNewAnger - iOldAnger + std::min(0, iOldAnger);
		if (iAnger > 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ANGER_BONUS", iAnger));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int const iOldAnger = iNewAnger;
		iNewAnger -= std::min(0, kCity.getReligionBadHappiness());
		int const iAnger = iNewAnger - iOldAnger + std::min(0, iOldAnger);
		if (iAnger > 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ANGER_RELIGIOUS_FREEDOM", iAnger));
			szBuffer.append(NEWLINE);
		}
	}
	// doc: specialist happiness
	{
		int const iOldAnger = iNewAnger;
		iNewAnger -= city.getSpecialistBadHappiness();
		int const iAnger = iNewAnger - iOldAnger + std::min(0, iOldAnger);
		if (iAnger > 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ANGER_SPECIALISTS", iAnger));
			szBuffer.append(NEWLINE);
		}
	}
	// doc: corporation happiness
	{
		int const iOldAnger = iNewAnger;
		iNewAnger -= city.getCorporationBadHappiness();
		int const iAnger = iNewAnger - iOldAnger + std::min(0, iOldAnger);
		if (iAnger > 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ANGER_CORPORATION", iAnger));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int const iOldAnger = iNewAnger;
		iNewAnger -= std::min(0, kCity.getCommerceHappiness());
		int const iAnger = iNewAnger - iOldAnger + std::min(0, iOldAnger);
		if (iAnger > 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ANGER_BAD_ENTERTAINMENT", iAnger));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int const iOldAnger = iNewAnger;
		iNewAnger -= std::min(0, kCity.getArea().getBuildingHappiness(kCity.getOwner()));
		int iAnger = iNewAnger - iOldAnger + std::min(0, iOldAnger);
		if (iAnger > 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ANGER_BUILDINGS", iAnger));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int const iOldAnger = iNewAnger;
		iNewAnger -= std::min(0, GET_PLAYER(kCity.getOwner()).getBuildingHappiness());
		int iAnger = iNewAnger - iOldAnger + std::min(0, iOldAnger);
		if (iAnger > 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ANGER_BUILDINGS", iAnger));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int const iOldAnger = iNewAnger;
		iNewAnger -= std::min(0,
				kCity.getExtraHappiness() + GET_PLAYER(kCity.getOwner()).getExtraHappiness());
		int iAnger = iNewAnger - iOldAnger + std::min(0, iOldAnger);
		if (iAnger > 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ANGER_ARGH", iAnger));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int const iOldAnger = iNewAnger;
		iNewAnger -= std::min(0, GC.getInfo(kCity.getHandicapType()).getHappyBonus());
		int iAnger = iNewAnger - iOldAnger + std::min(0, iOldAnger);
		if (iAnger > 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ANGER_HANDICAP", iAnger));
			szBuffer.append(NEWLINE);
		}
	}
	szBuffer.append(L"-----------------------\n");
	szBuffer.append(gDLL->getText("TXT_KEY_ANGER_TOTAL_UNHAPPY", iNewAnger));
	FAssert(iNewAnger == iUnhappy);
}


void CvGameTextMgr::setHappyHelp(CvWStringBuffer &szBuffer, CvCity const& kCity)
{
	if (kCity.isOccupation() || GET_PLAYER(kCity.getOwner()).isAnarchy())
		return;
	int const iHappyLevel = kCity.happyLevel();
	if (iHappyLevel <= 0)
		return;

	int iTotalHappy = 0;
	{
		int iHappy = kCity.getLargestCityHappiness();
		if (iHappy > 0)
		{
			iTotalHappy += iHappy;
			szBuffer.append(gDLL->getText("TXT_KEY_HAPPY_BIG_CITY", iHappy));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int iHappy = kCity.getMilitaryHappiness();
		if (iHappy > 0)
		{
			iTotalHappy += iHappy;
			szBuffer.append(gDLL->getText("TXT_KEY_HAPPY_MILITARY_PRESENCE", iHappy));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int iHappy = kCity.getVassalHappiness();
		if (iHappy > 0)
		{
			iTotalHappy += iHappy;
			szBuffer.append(gDLL->getText("TXT_KEY_HAPPY_VASSAL", iHappy));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int iHappy = kCity.getCurrentStateReligionHappiness();
		if (iHappy > 0)
		{
			iTotalHappy += iHappy;
			szBuffer.append(gDLL->getText("TXT_KEY_HAPPY_STATE_RELIGION", iHappy));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int iHappy = kCity.getBuildingGoodHappiness() +
				kCity.getExtraBuildingGoodHappiness();
		if (iHappy > 0)
		{
			iTotalHappy += iHappy;
			szBuffer.append(gDLL->getText("TXT_KEY_HAPPY_BUILDINGS", iHappy));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int iHappy = kCity.getSurroundingGoodHappiness();
		if (iHappy > 0)
		{
			iTotalHappy += iHappy;
			// advc.059: Text key was ..._FEATURES
			szBuffer.append(gDLL->getText("TXT_KEY_HAPPY_SURROUNDINGS", iHappy));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int iHappy = kCity.getBonusGoodHappiness();
		if (iHappy > 0)
		{
			iTotalHappy += iHappy;
			szBuffer.append(gDLL->getText("TXT_KEY_HAPPY_BONUS", iHappy));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int iHappy = kCity.getReligionGoodHappiness();
		if (iHappy > 0)
		{
			iTotalHappy += iHappy;
			szBuffer.append(gDLL->getText("TXT_KEY_HAPPY_RELIGIOUS_FREEDOM", iHappy));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int iHappy = kCity.getCommerceHappiness();
		if (iHappy > 0)
		{
			iTotalHappy += iHappy;
			szBuffer.append(gDLL->getText("TXT_KEY_HAPPY_ENTERTAINMENT", iHappy));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int iHappy = kCity.getArea().getBuildingHappiness(kCity.getOwner());
		if (iHappy > 0)
		{
			iTotalHappy += iHappy;
			szBuffer.append(gDLL->getText(
					"TXT_KEY_HAPPY_BUILDINGS_AREA", // advc.004g
					iHappy));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int iHappy = GET_PLAYER(kCity.getOwner()).getBuildingHappiness();
		if (iHappy > 0)
		{
			iTotalHappy += iHappy;
			szBuffer.append(gDLL->getText("TXT_KEY_HAPPY_BUILDINGS", iHappy));
			szBuffer.append(NEWLINE);
		}
	}
	{
		int iHappy = kCity.getExtraHappiness() +
				GET_PLAYER(kCity.getOwner()).getExtraHappiness();
		if (iHappy > 0)
		{
			iTotalHappy += iHappy;
			szBuffer.append(gDLL->getText("TXT_KEY_HAPPY_YEAH", iHappy));
			szBuffer.append(NEWLINE);
		}
	}
	if (kCity.getHappinessTimer() > 0)
	{
		int iHappy = GC.getDefineINT("TEMP_HAPPY");
		iTotalHappy += iHappy;
		szBuffer.append(gDLL->getText("TXT_KEY_HAPPY_TEMP", iHappy,
				kCity.getHappinessTimer()));
		szBuffer.append(NEWLINE);
	}
	{
		int iHappy = GC.getInfo(kCity.getHandicapType()).getHappyBonus();
		if (iHappy > 0)
		{
			iTotalHappy += iHappy;
			szBuffer.append(gDLL->getText("TXT_KEY_HAPPY_HANDICAP", iHappy));
			szBuffer.append(NEWLINE);
		}
	}
	szBuffer.append(L"-----------------------\n");
	szBuffer.append(gDLL->getText("TXT_KEY_HAPPY_TOTAL_HAPPY", iTotalHappy));
	FAssert(iTotalHappy == iHappyLevel);
}

// BUG - Building Additional Happiness - start
bool CvGameTextMgr::setBuildingAdditionalHappinessHelp(CvWStringBuffer &szBuffer,
	const CvCity& kCity, const CvWString& szStart, bool bStarted)
{
	CvWString szLabel;

	CvCivilization const& kCiv = kCity.getCivilization(); // advc.003w
	for (int i = 0; i < kCiv.getNumBuildings(); i++)
	{
		BuildingTypes eBuilding = kCiv.buildingAt(i);
		if (kCity.canConstruct(eBuilding, false, true, false))
		{
			int iGood = 0, iBad = 0;
			//int iChange = // advc: unused
			  kCity.getAdditionalHappinessByBuilding(eBuilding, iGood, iBad);

			if (iGood != 0 || iBad != 0)
			{
				int iAngryPop = kCity.getAdditionalAngryPopuplation(iGood, iBad);

				if (!bStarted)
				{
					szBuffer.append(szStart);
					bStarted = true;
				}

				szLabel.Format(SETCOLR L"%s" ENDCOLR, TEXT_COLOR("COLOR_BUILDING_TEXT"),
						GC.getInfo(eBuilding).getDescription());
				bool bStartedLine = setGoodBadChangeHelp(szBuffer, szLabel,
						L": ", L"", iGood, gDLL->getSymbolID(HAPPY_CHAR), iBad,
						gDLL->getSymbolID(UNHAPPY_CHAR), false, true);
				setValueChangeHelp(szBuffer, szLabel, L": ", L"", iAngryPop,
						gDLL->getSymbolID(ANGRY_POP_CHAR), false, true, bStartedLine);
			}
		}
	}

	return bStarted;
}
// BUG - Building Additional Happiness - end

/* replaced by BUG
void CvGameTextMgr::setYieldChangeHelp(CvWStringBuffer &szBuffer, const CvWString& szStart, const CvWString& szSpace, const CvWString& szEnd, const int* piYieldChange, bool bPercent, bool bNewLine)
{
	// (advc: deleted in July 2020)
}

void CvGameTextMgr::setCommerceChangeHelp(CvWStringBuffer &szBuffer, const CvWString& szStart, const CvWString& szSpace, const CvWString& szEnd, const int* piCommerceChange, bool bPercent, bool bNewLine)
{
	// (advc: deleted in July 2020)
}*/

/*	BUG - Resumable Value Change Help - start  (advc: refactored)
	Adding the ability to pass in and get back the value of bStarted so that
	set...ChangeHelp can be combined on a single line. */
template<class YieldChanges> // advc.003t
bool CvGameTextMgr::setYieldChangeHelp(CvWStringBuffer &szBuffer,
	const CvWString& szStart, const CvWString& szSpace, const CvWString& szEnd,
	YieldChanges aiYieldChange, bool bPercent, bool bNewLine, bool bStarted)
{
	CvWString szTempBuffer;

	FOR_EACH_ENUM(Yield)
	{
		if (aiYieldChange[eLoopYield] == 0)
			continue;
		if (!bStarted)
		{
			if (bNewLine)
				szTempBuffer.Format(L"\n%c", gDLL->getSymbolID(BULLET_CHAR));
			szTempBuffer += CvWString::format(L"%s%s%s%d%s%c",
					szStart.GetCString(), szSpace.GetCString(),
					aiYieldChange[eLoopYield] > 0 ? L"+" : L"",
					aiYieldChange[eLoopYield],
					bPercent ? L"%" : L"",
					GC.getInfo(eLoopYield).getChar());
		}
		else
		{
			szTempBuffer.Format(L", %s%d%s%c",
					aiYieldChange[eLoopYield] > 0 ? L"+" : L"",
					aiYieldChange[eLoopYield],
					bPercent ? L"%" : L"",
					GC.getInfo(eLoopYield).getChar());
		}
		szBuffer.append(szTempBuffer);
		bStarted = true;
	}

	if (bStarted)
		szBuffer.append(szEnd);

	return bStarted;
}
// <advc.003t> Explicit instantiations
template bool CvGameTextMgr::setYieldChangeHelp(CvWStringBuffer&,
		CvWString const&, CvWString const&, CvWString const&,
		int const*, bool, bool, bool);
template bool CvGameTextMgr::setYieldChangeHelp(CvWStringBuffer&,
		CvWString const&, CvWString const&, CvWString const&,
		YieldChangeMap const&, bool, bool, bool); // </advc.003t>

template<class CommerceChanges> // advc.003t
bool CvGameTextMgr::setCommerceChangeHelp(CvWStringBuffer &szBuffer,
	const CvWString& szStart, const CvWString& szSpace, const CvWString& szEnd,
	CommerceChanges aiCommerceChange, bool bPercent, bool bNewLine, bool bStarted)
{
	CvWString szTempBuffer;

	FOR_EACH_ENUM(Commerce)
	{
		if (aiCommerceChange[eLoopCommerce] == 0)
			continue;
		if (!bStarted)
		{
			if (bNewLine)
				szTempBuffer.Format(L"\n%c", gDLL->getSymbolID(BULLET_CHAR));
			szTempBuffer += CvWString::format(L"%s%s%s%d%s%c", szStart.GetCString(),
					szSpace.GetCString(), aiCommerceChange[eLoopCommerce] > 0 ? L"+" : L"",
					aiCommerceChange[eLoopCommerce], bPercent ? L"%" : L"",
					GC.getInfo(eLoopCommerce).getChar());
		}
		else
		{
			szTempBuffer.Format(L", %s%d%s%c",
					aiCommerceChange[eLoopCommerce] > 0 ? L"+" : L"",
					aiCommerceChange[eLoopCommerce], bPercent ? L"%" : L"",
					GC.getInfo(eLoopCommerce).getChar());
		}
		szBuffer.append(szTempBuffer);
		bStarted = true;
	}

	if (bStarted)
		szBuffer.append(szEnd);

	return bStarted;
}
// <advc.003t>
template bool CvGameTextMgr::setCommerceChangeHelp(CvWStringBuffer&,
		CvWString const&, CvWString const&, CvWString const&,
		int const*, bool, bool, bool);
template bool CvGameTextMgr::setCommerceChangeHelp(CvWStringBuffer&,
		CvWString const&, CvWString const&, CvWString const&,
		CommerceChangeMap const&, bool, bool, bool); // </advc.003t>

// Displays float values by dividing each value by 100
template<class CommercePercentChanges> // advc.003t
bool CvGameTextMgr::setCommerceTimes100ChangeHelp(CvWStringBuffer &szBuffer,
	const CvWString& szStart, const CvWString& szSpace, const CvWString& szEnd,
	CommercePercentChanges aiCommerceChange, bool bNewLine, bool bStarted)
{
	CvWString szTempBuffer;

	FOR_EACH_ENUM(Commerce)
	{
		int iChange = aiCommerceChange[eLoopCommerce];
		if (iChange == 0)
			continue;
		if (!bStarted)
		{
			if (bNewLine)
				szTempBuffer.Format(L"\n%c", gDLL->getSymbolID(BULLET_CHAR));
			szTempBuffer += CvWString::format(L"%s%s",
					szStart.GetCString(), szSpace.GetCString());
			bStarted = true;
		}
		else szTempBuffer.Format(L", ");
		szBuffer.append(szTempBuffer);

		if (iChange % 100 == 0)
		{
			szTempBuffer.Format(L"%+d%c", iChange / 100,
					GC.getInfo(eLoopCommerce).getChar());
		}
		else
		{
			if (iChange >= 0)
				szBuffer.append(L"+");
			else
			{
				iChange = - iChange;
				szBuffer.append(L"-");
			}
			szTempBuffer.Format(L"%d.%02d%c", iChange / 100,
					iChange % 100, GC.getInfo(eLoopCommerce).getChar());
		}
		szBuffer.append(szTempBuffer);
	}

	if (bStarted)
		szBuffer.append(szEnd);

	return bStarted;
}
// <advc.003t>
template bool CvGameTextMgr::setCommerceTimes100ChangeHelp(CvWStringBuffer&,
		CvWString const&, CvWString const&, CvWString const&,
		int const*, bool, bool);
template bool CvGameTextMgr::setCommerceTimes100ChangeHelp(CvWStringBuffer&,
		CvWString const&, CvWString const&, CvWString const&,
		CommercePercentMap const&, bool, bool); // </advc.003t>

bool CvGameTextMgr::setGoodBadChangeHelp(CvWStringBuffer &szBuffer,
	const CvWString& szStart, const CvWString& szSpace, const CvWString& szEnd,
	int iGood, int iGoodSymbol, int iBad, int iBadSymbol, bool bPercent,
	bool bNewLine, bool bStarted)
{
	bStarted = setValueChangeHelp(szBuffer, szStart, szSpace, szEnd,
			iGood, iGoodSymbol, bPercent, bNewLine, bStarted);
	bStarted = setValueChangeHelp(szBuffer, szStart, szSpace, szEnd,
			iBad, iBadSymbol, bPercent, bNewLine, bStarted);

	return bStarted;
}

bool CvGameTextMgr::setValueChangeHelp(CvWStringBuffer &szBuffer,
	const CvWString& szStart, const CvWString& szSpace, const CvWString& szEnd,
	int iValue, int iSymbol, bool bPercent, bool bNewLine, bool bStarted)
{
	if (iValue == 0)
		return bStarted;

	CvWString szTempBuffer;

	if (!bStarted)
	{
		if (bNewLine)
			szTempBuffer.Format(L"\n%c", gDLL->getSymbolID(BULLET_CHAR));
		szTempBuffer += CvWString::format(L"%s%s", szStart.GetCString(),
				szSpace.GetCString());
	}
	else szTempBuffer = L", ";

	szBuffer.append(szTempBuffer);

	szTempBuffer.Format(L"%+d%s%c", iValue, bPercent ? L"%" : L"", iSymbol);
	szBuffer.append(szTempBuffer);

	bStarted = true;

	return bStarted;
}

bool CvGameTextMgr::setValueTimes100ChangeHelp(CvWStringBuffer &szBuffer,
	const CvWString& szStart, const CvWString& szSpace, const CvWString& szEnd,
	int iValue, int iSymbol, bool bNewLine, bool bStarted)
{
	if (iValue == 0)
		return bStarted;

	CvWString szTempBuffer;

	if (!bStarted)
	{
		if (bNewLine)
			szTempBuffer.Format(L"\n%c", gDLL->getSymbolID(BULLET_CHAR));
		szTempBuffer += CvWString::format(L"%s%s", szStart.GetCString(), szSpace.GetCString());
	}
	else szTempBuffer = L", ";
	szBuffer.append(szTempBuffer);

	if (iValue % 100 == 0)
		szTempBuffer.Format(L"%+d%c", iValue / 100, iSymbol);
	else
	{
		if (iValue >= 0)
			szBuffer.append(L"+");
		else
		{
			iValue = - iValue;
			szBuffer.append(L"-");
		}
		szTempBuffer.Format(L"%d.%02d%c", iValue / 100, iValue % 100, iSymbol);
	}
	szBuffer.append(szTempBuffer);

	bStarted = true;

	return bStarted;
}
// BUG - Resumable Value Change Help - end

void CvGameTextMgr::setBonusHelp(CvWStringBuffer &szBuffer, BonusTypes eBonus, bool bCivilopediaText)
{
  // BULL - Trade Denial - start  (advc.073: bImport param added)
	setBonusTradeHelp(szBuffer, eBonus, bCivilopediaText, NO_PLAYER, false, false);
}

// This function has been effectly rewritten for K-Mod. (there were a lot of things to change.)
void CvGameTextMgr::setBonusTradeHelp(CvWStringBuffer &szBuffer, BonusTypes eBonus,
	bool bCivilopediaText, PlayerTypes eTradePlayer,
  // BULL - Trade Denial - end
	bool bImport, bool bForeignAdvisor) // advc.073
{
	if (eBonus == NO_BONUS)
		return;
	CvGame const& kGame = GC.getGame();
	PlayerTypes const eActivePlayer = getActivePlayer();
	CvPlayerAI const* pActivePlayer = (eActivePlayer == NO_PLAYER ? NULL:
			&GET_PLAYER(eActivePlayer));

	/*	When both Foreign Advisor and Trade Screen are open,
		the Foreign Advisor will be in the foreground. */
	bool const bDiplo = (!bForeignAdvisor && (kGame.isGameMultiPlayer() ?
			// gDLL->isMPDiplomacy() does sth. else, apparently.
			gDLL->isMPDiplomacyScreenUp() : gDLL->isDiplomacy()));
	CvCity const* pCity = (gDLL->UI().isCityScreenUp() ?
			/*  A city can also be selected without the city screen being up;
				don't want that here. */
			gDLL->UI().getHeadSelectedCity() : NULL);

	int const iHappiness = GC.getInfo(eBonus).getHappiness();
	int const iHealth = GC.getInfo(eBonus).getHealth();

	if (bCivilopediaText)
	{
		// K-Mod. for the civilopedia text, display the basic bonuses as individual bullet points.
		// (they are displayed beside the name of the bonus when outside of the civilopedia.)
		if (iHappiness != 0)
		{
			szBuffer.append(CvWString::format(L"\n%c+%d%c",
					gDLL->getSymbolID(BULLET_CHAR), abs(iHappiness), iHappiness > 0 ?
					gDLL->getSymbolID(HAPPY_CHAR) : gDLL->getSymbolID(UNHAPPY_CHAR)));
		}
		if (iHealth != 0)
		{
			szBuffer.append(CvWString::format(L"\n%c+%d%c",
					gDLL->getSymbolID(BULLET_CHAR), abs(iHealth), iHealth > 0 ?
					gDLL->getSymbolID(HEALTHY_CHAR) : gDLL->getSymbolID(UNHEALTHY_CHAR)));
		}
	}
	else
	{
		szBuffer.append(CvWString::format( SETCOLR L"%s" ENDCOLR,
				TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
				GC.getInfo(eBonus).getDescription()));
		// advc.004w: Don't omit the basic effect in opening menu Civilopedia hovers
		//if (NO_PLAYER != eActivePlayer)

		/*	K-Mod. Bonuses now display "(Obsolete)" instead of
			"(player has 0)" when the bonus is obsolete. */
		if (eActivePlayer != NO_PLAYER && // advc.004w
			GET_TEAM(eActivePlayer).isBonusObsolete(eBonus))
		{
			szBuffer.append(gDLL->getText("TXT_KEY_BONUS_OBSOLETE"));
		}
		else
		{
			// display the basic bonuses next to the name of the bonus
			if (iHappiness != 0)
			{
				szBuffer.append(CvWString::format(L", +%d%c", abs(iHappiness),
						iHappiness > 0 ? gDLL->getSymbolID(HAPPY_CHAR) :
						gDLL->getSymbolID(UNHAPPY_CHAR)));
			}
			if (iHealth != 0)
			{
				szBuffer.append(CvWString::format(L", +%d%c", abs(iHealth),
						iHealth > 0 ? gDLL->getSymbolID(HEALTHY_CHAR) :
						gDLL->getSymbolID(UNHEALTHY_CHAR)));
			}
			if(eActivePlayer != NO_PLAYER) // advc.004w: Moved from above
			{
				// <advc.004w>
				int iAvailable = pActivePlayer->getNumAvailableBonuses(eBonus);
				if(bDiplo || // Trade screen, domestic resources box or import column
					(eTradePlayer != NO_PLAYER &&
					(eTradePlayer == eActivePlayer || bImport)))
				{	// </advc.004w>
					szBuffer.append(gDLL->getText("TXT_KEY_BONUS_AVAILABLE_PLAYER",
							iAvailable, pActivePlayer->getNameKey()));
				} // <advc.004w> Show their amount in the export columns
				else if(eTradePlayer != NO_PLAYER &&
						eTradePlayer != eActivePlayer && !bImport)
				{
					szBuffer.append(gDLL->getText("TXT_KEY_BONUS_AVAILABLE_PLAYER",
							GET_PLAYER(eTradePlayer).getNumAvailableBonuses(eBonus),
							GET_PLAYER(eTradePlayer).getNameKey()));
				} // Don't show amount on city screen if it's 1
				else if(iAvailable != 1 || pCity == NULL)
				{
					// When not trading, this should be clear enough:
					szBuffer.append(gDLL->getText("TXT_KEY_BONUS_AVAILABLE_US",
							iAvailable));
				} // </advc.004w>
				FOR_EACH_ENUM(Corporation)
				{
					bool bCorpBonus = false;
					if (pActivePlayer->getHasCorporationCount(eLoopCorporation) > 0)
					{
						for (int i = 0;
							i < GC.getInfo(eLoopCorporation).getNumPrereqBonuses() &&
							!bCorpBonus; i++)
						{
							bCorpBonus = (eBonus == GC.getInfo(eLoopCorporation).getPrereqBonus(i));
						}
					}
					if (bCorpBonus)
						szBuffer.append(GC.getInfo(eLoopCorporation).getChar());
				}
			}
		}
		// <advc.004w>
		if(eActivePlayer == NO_PLAYER ||
			(!bDiplo && !gDLL->UI().isCityScreenUp() &&
			eTradePlayer == NO_PLAYER)) // </advc.004w>
		{
			setYieldChangeHelp(szBuffer, L"", L"", gDLL->getText("TXT_KEY_BONUS_ON_PLOT"),
					GC.getInfo(eBonus).getYieldChangeArray());
		}
		// <advc.004w> Only show reveal tech if we don't have it yet
		TechTypes eRevealTech = (TechTypes)GC.getInfo(eBonus).getTechReveal();
		if (eRevealTech != NO_TECH && (eActivePlayer == NO_PLAYER ||
			!GET_TEAM(eActivePlayer).isHasTech(eRevealTech))) // </advc.004w>
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_BONUS_REVEALED_BY",
					GC.getInfo(GC.getInfo(eBonus).getTechReveal()).getTextKeyWide()));
		}
	}

	if(bCivilopediaText || eActivePlayer == NO_PLAYER ||
		// K-Mod. Only display the perks of the bonus if it is not already obsolete
		!GET_TEAM(eActivePlayer).isBonusObsolete(eBonus))
	{
		// advc.004w: Effects from buildings, projects and units in a subroutine
		setBonusExtraHelp(szBuffer, eBonus, bCivilopediaText, eTradePlayer, bDiplo, pCity);
	}

	// BULL - Trade Denial - start  (advc.073: refactored; BugOption check removed)
	if (eTradePlayer == NO_PLAYER || eActivePlayer == NO_PLAYER)
		return; // advc

	TradeData resourceTrade(TRADE_RESOURCES, eBonus);
	TradeData gptTrade(TRADE_GOLD_PER_TURN, 1);
	bool const bHuman = GET_PLAYER(eTradePlayer).isHuman(); // advc.073
	// <advc.073>
	int const iGoldChar = GC.getInfo(COMMERCE_GOLD).getChar(); // advc.036
	if(eTradePlayer == eActivePlayer)
	{
		FAssert(!bImport);
		/*  This means we're hovering over a surplus resource of the
			active player and all takers need to be listed. */
		std::vector<PlayerTypes> aTakers;

		for (PlayerAIIter<MAJOR_CIV,KNOWN_TO> it(TEAMID(eActivePlayer));
			it.hasNext(); ++it)
		{
			CvPlayerAI const& kTaker = *it;
			if (kTaker.getID() == eActivePlayer || kTaker.isHuman())
				continue;
			if(pActivePlayer->canTradeItem(kTaker.getID(), resourceTrade, true) &&
				kTaker.AI_isWillingToTalk(eActivePlayer, true))
			{
				aTakers.push_back(kTaker.getID());
			}
		}
		if(aTakers.empty())
			return;
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_WILL_IMPORT"
				// Better not to repeat the resource name
				/*,GC.getInfo(eBonus).getTextKeyWide()*/));
		szBuffer.append(/*L": "*/L":\n");
		/*  Should perhaps sort by the gold they're willing to give, but that's
			tedious to implement, and using player id also has merit as the
			portraits on the Resources tab are ordered by id. */
		for(size_t i = 0; i < aTakers.size(); i++)
		{
			CvPlayerAI const& kTaker = GET_PLAYER(aTakers[i]);
			szBuffer.append(kTaker.getName());
			if(kTaker.canTradeItem(eActivePlayer, gptTrade, false))
			{
				int iGold = kTaker.AI_goldForBonus(eBonus, eActivePlayer);
				if(iGold > 0)
					szBuffer.append(CvWString::format(L" (%d%c)", iGold, iGoldChar));
			}
			if(i < aTakers.size() - 1)
				szBuffer.append(L", ");
		}
		return;
	}
	if (!bImport && // </advc.073>
		GET_PLAYER(eTradePlayer).canTradeItem(eActivePlayer, resourceTrade, false))
	{
		DenialTypes eDenial = GET_PLAYER(eTradePlayer).getTradeDenial(
				eActivePlayer, resourceTrade);
		if (eDenial != NO_DENIAL /* advc.073: */ && eDenial != DENIAL_JOKING)
		{
			CvWString szTempBuffer;
			szTempBuffer.Format(SETCOLR L"%s" ENDCOLR,
					TEXT_COLOR("COLOR_NEGATIVE_TEXT"),
					GC.getInfo(eDenial).getDescription());
			szBuffer.append(NEWLINE);
			szBuffer.append(szTempBuffer);
			// <advc.036>
			return;
		}
		else if(eDenial == NO_DENIAL && !bHuman)
		{
			if(GET_PLAYER(eTradePlayer).AI_isWillingToTalk(eActivePlayer, true))
			{
				if(pActivePlayer->canTradeItem(eTradePlayer, gptTrade, false))
				{
					int iGold = pActivePlayer->AI_goldForBonus(eBonus, eTradePlayer);
					if(iGold > 0)
					{
						szBuffer.append(NEWLINE);
						szBuffer.append(CvWString::format(L"%s %d%c",
								gDLL->getText("TXT_KEY_MISC_WILL_ASK").GetCString(),
								iGold, iGoldChar));
						return;
					}
				}
			}
			else
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_REFUSES_TO_TALK"));
			}
		}
	}
	if(bImport && !bHuman)
	{
		bool bWillTalk = GET_PLAYER(eTradePlayer).AI_isWillingToTalk(eActivePlayer, true);
		if(bWillTalk && pActivePlayer->canTradeItem(eTradePlayer, resourceTrade, true))
		{
			if(GET_PLAYER(eTradePlayer).canTradeItem(eActivePlayer, gptTrade, false))
			{
				int iGold = GET_PLAYER(eTradePlayer).AI_goldForBonus(eBonus, eActivePlayer);
				if(iGold > 0)
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(CvWString::format(L"%s %d%c",
							gDLL->getText("TXT_KEY_MISC_WILL_PAY").GetCString(),
							iGold, iGoldChar));
				}
			}
		}
		else if(!bWillTalk)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_REFUSES_TO_TALK"));
		}
	} // </advc.036>
	// BULL - Trade Denial - end
}

// advc.004w: Some code cut from setBonusHelp, but mostly new code.
void CvGameTextMgr::setBonusExtraHelp(CvWStringBuffer &szBuffer, BonusTypes eBonus,
	bool bCivilopediaText, PlayerTypes eTradePlayer, bool bDiplo, CvCity const* pCity)
{
	PROFILE_FUNC();
	CvGame const& kGame = GC.getGame();
	CivilizationTypes const eCivilization = kGame.getActiveCivilizationType();
	PlayerTypes const eActivePlayer = getActivePlayer();
	// NULL when in opening-menu Civilopedia
	CvPlayerAI const* pActivePlayer = NULL;
	int iCurrentEra = 0;
	if(eActivePlayer != NO_PLAYER)
	{
		pActivePlayer = &GET_PLAYER(eActivePlayer);
		iCurrentEra = pActivePlayer->getCurrentEra();
	}
	FOR_EACH_ENUM2(BuildingClass, eBuildingClass)
	{
		BuildingTypes eBuilding = (eCivilization == NO_CIVILIZATION ?
				GC.getInfo(eBuildingClass).getDefaultBuilding() :
				GC.getInfo(eCivilization).getCivilizationBuildings(eBuildingClass));
		if(eBuilding == NO_BUILDING)
			continue;
		// <advc.004w> Don't list impossibilities
		bool bCanEverConstruct = true;
		if(eActivePlayer != NO_PLAYER && !kGame.canConstruct(eBuilding, true, true))
			bCanEverConstruct = false;
		// Don't list remote possibilities
		CvBuildingInfo& kBuilding = GC.getInfo(eBuilding);
		int iTechEraDelta = 0;
		if(bCanEverConstruct && !bCivilopediaText && eActivePlayer != NO_PLAYER)
		{
			ReligionTypes eReligion = kBuilding.getPrereqReligion();
			if(eReligion != NO_RELIGION && !pActivePlayer->canDoReligion(eReligion))
				bCanEverConstruct = false;
			if(bCanEverConstruct)
			{
				TechTypes eTech = kBuilding.getPrereqAndTech();
				if(eTech == NO_TECH)
				{
					SpecialBuildingTypes eSpecial = (SpecialBuildingTypes)kBuilding.getSpecialBuildingType();
					if(eSpecial != NO_SPECIALBUILDING)
						eTech = GC.getInfo(eSpecial).getTechPrereq();
				}
				if(eTech != NO_TECH)
					iTechEraDelta = GC.getInfo(eTech).getEra() - iCurrentEra;
				if(iTechEraDelta >= 2 || (iTechEraDelta >= 1 &&
						// Special treatment for the very early game
						iCurrentEra <= 0 && pActivePlayer->getNumCities() <= 2))
					bCanEverConstruct = false;
			}
			if(bCanEverConstruct && GET_TEAM(eActivePlayer).isObsoleteBuilding(eBuilding))
				bCanEverConstruct = false;
			if(bCanEverConstruct)
			{
				VictoryTypes eVict = kBuilding.getVictoryPrereq();
				if(eVict != NO_VICTORY && !kGame.isVictoryValid(eVict))
					bCanEverConstruct = false;
			}
			if(bCanEverConstruct &&
				(GET_TEAM(eActivePlayer).isBuildingClassMaxedOut(eBuildingClass) ||
				pActivePlayer->isBuildingClassMaxedOut(eBuildingClass)))
			{
				bCanEverConstruct = false;
			}
			if(bCanEverConstruct)
			{
				// CvCity::canConstruct would be too strict, even with the bIgnore flags.
				if(pCity != NULL && !pCity->getPlot().canConstruct(eBuilding))
					bCanEverConstruct = false;
			}
		}
		// Don't skip e.g. active wonders
		if(!bCanEverConstruct && pActivePlayer->getBuildingClassCount(eBuildingClass) <= 0)
			continue;
		// </advc.004w>
		int const iBonusHappyChange = kBuilding.getBonusHappinessChanges(eBonus);
		if(iBonusHappyChange != 0)
		{
			szBuffer.append(CvWString::format(L"\n%s",
					gDLL->getText("TXT_KEY_BUILDING_CIVIC_HEALTH_HAPPINESS_CHANGE",
					abs(iBonusHappyChange),
					iBonusHappyChange > 0 ? gDLL->getSymbolID(HAPPY_CHAR) :
					gDLL->getSymbolID(UNHAPPY_CHAR)).c_str()));
			//szBuffer.append(szBuildingDescr); // advc.004w: Handled below
		}
		int const iBonusHealthChange = kBuilding.getBonusHealthChanges(eBonus);
		if(iBonusHealthChange != 0)
		{
			szBuffer.append(CvWString::format(L"\n%s",
					gDLL->getText("TXT_KEY_BUILDING_CIVIC_HEALTH_HAPPINESS_CHANGE",
					abs(iBonusHealthChange),
					iBonusHealthChange > 0 ? gDLL->getSymbolID(HEALTHY_CHAR) :
					gDLL->getSymbolID(UNHEALTHY_CHAR)).c_str()));
			//szBuffer.append(szBuildingDescr); // advc.004w: Handled below
		} // <advc.004w>
		if(iBonusHappyChange != 0 || iBonusHealthChange != 0)
		{
			CvWString szDescr(kBuilding.getDescription());
			if(pCity != NULL)
			{
				::applyColorToString(szDescr,
						pCity->getNumActiveBuilding(eBuilding) > 0 ?
						"COLOR_POSITIVE_TEXT" : "COLOR_NEGATIVE_TEXT");
			}
			szBuffer.append(szDescr);
		}
		/*  Not much room in the "Effects" box of Civilopedia. Put only health
			and happiness effects there. */
		if(bCivilopediaText)
			continue;
		bool bWonder = kBuilding.isLimited();
		// Similar to setBuildingHelpActual, but that's from the building's pov.
		if(eActivePlayer != NO_PLAYER && ((pCity == NULL &&
			// Show yield modifiers of wonders only if we already have them
			(!bWonder || pActivePlayer->getBuildingClassCount(eBuildingClass) > 0)) ||
			(pCity != NULL && pCity->getNumActiveBuilding(eBuilding) > 0)))
		{
			if (kBuilding.getBonusYieldModifier().isAnyNonDefault())
			{
				YieldPercentMap yieldMap = kBuilding.getBonusYieldModifier(eBonus);
				FOR_EACH_ENUM(Yield)
				{
					if (yieldMap[eLoopYield] == 0)
						continue;
					CvWString szStart(kBuilding.getDescription());
					szStart.append(L": ");
					setYieldChangeHelp(szBuffer, szStart, L"", L"", yieldMap, true);
					break;
				}
			}
		}
		// Only construction effects remain
		if(!bCanEverConstruct)
			continue;
		// Stricter check than the one for happiness/health effects above
		if(pCity != NULL && !pCity->canConstruct(eBuilding, false, true, true))
			continue;

		// Highlight building name when it's under construction
		bool bConstructing = false;
		if(pCity != NULL)
		{
			CLLNode<OrderData>* pOrderNode = pCity->headOrderQueueNode();
			if(pOrderNode != NULL && pOrderNode->m_data.eOrderType == ORDER_CONSTRUCT &&
				pOrderNode->m_data.iData1 == eBuilding)
			{
				bConstructing = true;
			}
		}
		bool bHighlight = (bConstructing ||
				(eActivePlayer != NO_PLAYER && pCity == NULL &&
				/*  I.e. not on the main interface b/c it's too difficult to
					keep those texts updated */
				(eTradePlayer != NO_PLAYER || bDiplo) &&
				pActivePlayer->getBuildingClassMaking(eBuildingClass) > 0));

		// These are unused, but I'd like to use them someday.
		bool bBonusReq = (kBuilding.getPrereqAndBonus() == eBonus);
		if(!bBonusReq)
		{
			for(int i = 0; i < kBuilding.getNumPrereqOrBonuses(); i++)
			{
				if(kBuilding.getPrereqOrBonuses(i) == eBonus)
				{
					bBonusReq = true;
					break;
				}
			}
		}
		if(bBonusReq)
		{
			CvWString szDescr(kBuilding.getDescription());
			if(bHighlight)
				::applyColorToString(szDescr, "COLOR_HIGHLIGHT_TEXT");
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_TECH_CAN_CONSTRUCT"));
			szBuffer.append(szDescr);
		}
		if(eActivePlayer == NO_PLAYER)
			continue;
		// Don't show wonder production bonuses for future eras
		if(!bWonder || iTechEraDelta <= 0)
		{
			int iProductionMod = kBuilding.getBonusProductionModifier(eBonus);
			if(iProductionMod != 0)
			{
				szBuffer.append(NEWLINE);
				CvWString szDescr(kBuilding.getDescription());
				if(bHighlight)
					::applyColorToString(szDescr, "COLOR_HIGHLIGHT_TEXT");
				szBuffer.append(CvWString::format(L"%c%s%d%% %s",
						gDLL->getSymbolID(BULLET_CHAR),
						iProductionMod > 0 ? "+" : "", iProductionMod,
						gDLL->getText("TXT_KEY_BONUS_SPEED_FOR",
						szDescr.GetCString()).GetCString()));
			}
		}
	}
	if(bCivilopediaText)
		return;
	if(eActivePlayer != NO_PLAYER)
	{
		// Based on the loop above
		FOR_EACH_ENUM2(Project, eProject)
		{
			CvProjectInfo const& kProject = GC.getInfo(eProject);
			int iProductionMod = kProject.getBonusProductionModifier(eBonus);
			if(iProductionMod == 0)
				continue;
			if(pCity == NULL)
			{
				TechTypes eTech = kProject.getTechPrereq();
				if(eTech != NO_TECH &&
					GC.getInfo(eTech).getEra() >
					iCurrentEra + (kProject.isWorldProject() ? 0 : 1))
				{
					continue;
				}
				VictoryTypes eVict = kProject.getVictoryPrereq();
				if(eVict != NO_VICTORY && !kGame.isVictoryValid(eVict))
					continue;
				if(kGame.isProjectMaxedOut(eProject) && GET_TEAM(eActivePlayer).
					getProjectCount(eProject) <= 0)
				{
					continue;
				}
				if(kProject.isSpaceship() && (!pActivePlayer->hasCapital() ||
					!pActivePlayer->getCapital()->canCreate(eProject, false, true)))
				{
					continue;
				}
			}
			else if(!pCity->canCreate(eProject, false, true))
				continue;
			// Copy-paste from the building loop
			szBuffer.append(NEWLINE);
			szBuffer.append(CvWString::format(L"%c%s%d%% %s",
					gDLL->getSymbolID(BULLET_CHAR),
					iProductionMod > 0 ? "+" : "",
					iProductionMod, gDLL->getText("TXT_KEY_BONUS_SPEED_FOR",
					kProject.getDescription()).GetCString()));
		}
		// To weed out obsolete units
		CvCity const* pTrainCity = pCity;
		if(pTrainCity == NULL)
			pTrainCity = pActivePlayer->getCapital();
		std::vector<CvUnitInfo*> aEnables;
		CvCivilization const& kCiv = *GC.getGame().getActiveCivilization();
		for (int i = 0; i < kCiv.getNumUnits(); i++)
		{
			UnitTypes eLoopUnit = kCiv.unitAt(i);
			CvUnitInfo& kUnit = GC.getInfo(eLoopUnit);
			// <advc.905b>
			int iSpeed = 0;
			for (int j = 0; j < kUnit.getNumSpeedBonuses(); j++)
			{
				iSpeed = kUnit.getExtraMoves(j);
			} // </advc.905b>
			bool bBonusReq = (kUnit.getPrereqAndBonus() == eBonus);
			if (!bBonusReq)
			{
				for (int j = 0; j < kUnit.getNumPrereqOrBonuses(); j++)
				{
					if (kUnit.getPrereqOrBonuses(j) == eBonus)
					{
						bBonusReq = true;
						break;
					}
				}
			}
			if (!bBonusReq && iSpeed == 0)
				continue;
			if (pTrainCity == NULL)
			{
				if (!pActivePlayer->canTrain(eLoopUnit, false, true, true))
					continue;
			}
			else if (!pTrainCity->canTrain(eLoopUnit, false, true, true, false, false))
				continue;
			if (bBonusReq)
				aEnables.push_back(&kUnit);
			if (iSpeed != 0)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(CvWString::format(L"%c%s%d%c: ",
						gDLL->getSymbolID(BULLET_CHAR), iSpeed > 0 ? "+" : "",
						iSpeed, gDLL->getSymbolID(MOVES_CHAR)));
				szBuffer.append(kUnit.getDescription());
			}
		}
		/*  The capital can be NULL and it's not necessarily going to be coastal.
			Address these cases through an era threshold (b/c checking upgrade paths
			without a CvCity object is too complicated). */
		int iEraThresh = std::max(0, iCurrentEra - 3);
		int iCount = aEnables.size();
		while (iCount > 5 && iEraThresh < iCurrentEra)
		{
			iCount = aEnables.size();
			for (size_t i = 0; i < aEnables.size(); i++)
			{
				TechTypes eTech = aEnables[i]->getPrereqAndTech();
				if (eTech != NO_TECH && GC.getInfo(eTech).getEra() <= iEraThresh)
					iCount--;
			}
			iEraThresh++;
		}
		if (iCount <= 0) // Show too many units rather than none
			iEraThresh = 0;
		for (size_t i = 0; i < aEnables.size(); i++)
		{
			TechTypes eTech = aEnables[i]->getPrereqAndTech();
			bool bSea = (DOMAIN_SEA == aEnables[i]->getDomainType());
			bool bUseEraThresh = (eTech != NO_TECH && (pTrainCity == NULL ||
					(bSea != pTrainCity->isCoastal())));
			if (!bUseEraThresh || GC.getInfo(eTech).getEra() >= iEraThresh)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_TECH_CAN_TRAIN"));
				szBuffer.append(aEnables[i]->getDescription());
			}
		}
	} // </advc.004w>
	if (!CvWString(GC.getInfo(eBonus).getHelp()).empty())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(GC.getInfo(eBonus).getHelp());
	}
}

// advc.111: Cut from CvDLLWidgetData::parseActionHelp
bool CvGameTextMgr::setPillageHelp(CvWStringBuffer &szBuffer, ImprovementTypes eImprovement)
{
	if (eImprovement == NO_IMPROVEMENT)
		return false;
	szBuffer.append(NEWLINE);
	szBuffer.append(gDLL->getText("TXT_KEY_ACTION_DESTROY_IMP",
			GC.getInfo(eImprovement).getTextKeyWide()));
	return true;
}

// advc.111: Cut from CvDLLWidgetData::parseActionHelp
bool CvGameTextMgr::setPillageHelp(CvWStringBuffer &szBuffer, RouteTypes eRoute)
{
	if (eRoute == NO_ROUTE)
		return false;
	szBuffer.append(NEWLINE);
	szBuffer.append(gDLL->getText("TXT_KEY_ACTION_DESTROY_IMP",
			GC.getInfo(eRoute).getTextKeyWide()));
	return true;
}


void CvGameTextMgr::setReligionHelp(CvWStringBuffer &szBuffer, ReligionTypes eReligion, bool bCivilopedia)
{
	if (eReligion == NO_RELIGION)
		return;

	CvReligionInfo const& kReligion = GC.getInfo(eReligion);
	if (!bCivilopedia)
	{
		szBuffer.append(CvWString::format(SETCOLR L"%s" ENDCOLR,
				TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"), kReligion.getDescription()));
	}

	/*setCommerceChangeHelp(szBuffer, gDLL->getText("TXT_KEY_RELIGION_HOLY_CITY").c_str(),
			L": ", L"", kReligion.getHolyCityCommerceArray());
	setCommerceChangeHelp(szBuffer, gDLL->getText("TXT_KEY_RELIGION_ALL_CITIES").c_str(),
			L": ", L"", kReligion.getStateReligionCommerceArray());*/
	// <advc.172>
	FOR_EACH_ENUM(Commerce)
	{
		int iBaseRate = kReligion.getStateReligionCommerce(eLoopCommerce);
		int iHolyCityRate = iBaseRate + kReligion.getHolyCityCommerce(eLoopCommerce);
		if (iBaseRate == 0 && iHolyCityRate == 0)
			continue;
		szBuffer.append(NEWLINE);
		szBuffer.append(CvWString::format(L"%c ", gDLL->getSymbolID(BULLET_CHAR)));
		bool bParentheses = false;
		if (iBaseRate != 0)
		{
			szBuffer.append(CvWString::format(L"%d%c", iBaseRate,
					GC.getInfo(eLoopCommerce).getChar()));
			if (iHolyCityRate != iBaseRate)
				bParentheses = true;
		}
		if (iHolyCityRate != iBaseRate)
		{
			if (bParentheses)
				szBuffer.append(L" (");
			szBuffer.append(CvWString::format(L"%d%c ", iHolyCityRate,
					GC.getInfo(eLoopCommerce).getChar()));
			szBuffer.append(gDLL->getText("TXT_KEY_RELIGION_IN_HOLY_CITY"));
			if (bParentheses)
				szBuffer.append(L")");
		}
		szBuffer.append(NEWLINE);
		szBuffer.append(L"    ");
		szBuffer.append(gDLL->getText("TXT_KEY_RELIGION_NOT_CUMULATIVE"));
	} // </advc.172>

	if (!bCivilopedia)
	{
		if (kReligion.getTechPrereq() != NO_TECH)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_RELIGION_FOUNDED_FIRST",
					GC.getInfo(kReligion.getTechPrereq()).getTextKeyWide()));
		}
	}

	UnitClassTypes eFreeUnitClass = kReligion.getFreeUnitClass(); // advc
	if (eFreeUnitClass != NO_UNITCLASS)
	{
		UnitTypes eFreeUnit = (getActivePlayer() != NO_PLAYER ?
				GC.getGame().getActiveCivilization()->getUnit(eFreeUnitClass) :
				GC.getInfo(eFreeUnitClass).getDefaultUnit());
		if (eFreeUnit != NO_UNIT)
		{
			if (kReligion.getNumFreeUnits() > 1)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_RELIGION_FOUNDER_RECEIVES_NUM",
						GC.getInfo(eFreeUnit).getTextKeyWide(),
						kReligion.getNumFreeUnits()));
			}
			else if (kReligion.getNumFreeUnits() > 0)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_RELIGION_FOUNDER_RECEIVES",
						GC.getInfo(eFreeUnit).getTextKeyWide()));
			}
		}
	}
}

void CvGameTextMgr::setReligionHelpCity(CvWStringBuffer &szBuffer, ReligionTypes eReligion,
	CvCity* pCity, bool bCityScreen, bool bForceReligion, bool bForceState, bool bNoStateReligion)
{
	if(pCity == NULL)
		return;
	CvWString szTempBuffer;

	ReligionTypes eStateReligion = NO_RELIGION;
	if (!bNoStateReligion)
		eStateReligion = GET_PLAYER(pCity->getOwner()).getStateReligion();
	// <advc.172> bForceState can now also mean that eReligion must be treated as non-state
	if (bForceState)
	{
		if (eStateReligion == eReligion)
			eStateReligion = NO_RELIGION;
		else eStateReligion = eReligion;
	} // </advc.172>
	if (bCityScreen)
	{
		szBuffer.append(CvWString::format(SETCOLR L"%s" ENDCOLR,
				TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
				GC.getInfo(eReligion).getDescription()));
		szBuffer.append(NEWLINE);

		if (!GC.getGame().isReligionFounded(eReligion) &&
			!GC.getGame().isOption(GAMEOPTION_PICK_RELIGION))
		{
			if (GC.getInfo(eReligion).getTechPrereq() != NO_TECH)
			{
				szBuffer.append(gDLL->getText("TXT_KEY_RELIGION_FOUNDED_FIRST",
						GC.getInfo(GC.getInfo(eReligion).getTechPrereq()).
						getTextKeyWide()));
			}
		}
	}
	// K-Mod
	if (GC.getGame().isReligionFounded(eReligion) && pCity && //gDLL->getChtLvl() > 0
		GC.getGame().isDebugMode() && // advc.135c
		GC.ctrlKey())
	{
		szBuffer.append(CvWString::format(L"grip: %d", pCity->getReligionGrip(eReligion)));
		szBuffer.append(NEWLINE);
	} // K-Mod end

	if (!bForceReligion && !pCity->isHasReligion(eReligion))
		return;

	bool bFirst = true;
	//if (eStateReligion == eReligion || eStateReligion == NO_RELIGION || bForceState)
	// <advc.172>
	/*	Don't show commerce on Religion Advisor - not helpful anymore for choosing
		a state religion b/c the commerce isn't affected by the state religion. */
	if (bCityScreen || bForceReligion)
	{
		std::vector<ReligionTypes> aeReligions;
		/*	(On the Religion Advisor, the order doesn't matter, but an
			inconsistent order between calls leads to undercounting.) */
		if (eStateReligion != NO_RELIGION && bCityScreen)
			aeReligions.push_back(eStateReligion);
		FOR_EACH_ENUM(Religion)
		{
			if (aeReligions.empty() || eLoopReligion != aeReligions[0])
				aeReligions.push_back(eLoopReligion);
		}
		FOR_EACH_ENUM(Commerce)
		{
			ReligionTypes eMaxReligion = NO_RELIGION;
			int iMaxRate = 0;
			for (size_t i = 0; i < aeReligions.size(); i++)
			{
				int iRate = pCity->getReligionCommerceByReligion(
						eLoopCommerce, aeReligions[i]);
				if (iRate > iMaxRate)
				{
					iMaxRate = iRate;
					eMaxReligion = aeReligions[i];
				}
			}
			if (eReligion == eMaxReligion ||
				(eMaxReligion == NO_RELIGION && bForceReligion))
			{	// </advc.172>
				// <advc> Replacing redundant BtS code
				int iRate = pCity->getReligionCommerceByReligion(
						eLoopCommerce, eReligion, bForceReligion); // </advc>
				if (iRate != 0)
				{
					if (!bFirst)
						szBuffer.append(L", ");
					bFirst = false;
					szTempBuffer.Format(L"%s%d%c", iRate > 0 ? "+" : "",
							iRate, GC.getInfo(eLoopCommerce).getChar());
					szBuffer.append(szTempBuffer);
				}
			}
		}
	}
	if (eStateReligion == eReligion/* || bForceState*/)
	{
		int iHappiness = (pCity->getStateReligionHappiness(eReligion) +
				GET_PLAYER(pCity->getOwner()).getStateReligionHappiness());
		if (iHappiness != 0)
		{
			if (!bFirst)
				szBuffer.append(L", ");
			bFirst = false;
			szTempBuffer.Format(L"%d%c",
					/*	UNOFFICIAL_PATCH (Bugfix, 08/28/09, jdog5000): start
						Use absolute value with unhappy face */
					abs(iHappiness), (iHappiness > 0 ?
					gDLL->getSymbolID(HAPPY_CHAR) :
					gDLL->getSymbolID(UNHAPPY_CHAR))); // UNOFFICIAL_PATCH: end
			szBuffer.append(szTempBuffer);
		}
		int iProductionModifier = GET_PLAYER(pCity->getOwner()).
				getStateReligionBuildingProductionModifier();
		if (iProductionModifier != 0)
		{
			if (!bFirst)
				szBuffer.append(L", ");
			bFirst = false;
			szBuffer.append(gDLL->getText("TXT_KEY_RELIGION_BUILDING_PROD_MOD",
					iProductionModifier));
		}
		iProductionModifier = GET_PLAYER(pCity->getOwner()).
				getStateReligionUnitProductionModifier();
		if (iProductionModifier != 0)
		{
			if (!bFirst)
				szBuffer.append(L", ");
			bFirst = false;
			szBuffer.append(gDLL->getText("TXT_KEY_RELIGION_UNIT_PROD_MOD",
					iProductionModifier));
		}
		int iFreeExperience = GET_PLAYER(pCity->getOwner()).
				getStateReligionFreeExperience();
		if (iFreeExperience != 0)
		{
			if (!bFirst)
				szBuffer.append(L", ");
			bFirst = false;
			szBuffer.append(gDLL->getText("TXT_KEY_RELIGION_FREE_XP",
					iFreeExperience));
		}
		int iGreatPeopleRateModifier = GET_PLAYER(pCity->getOwner()).
				getStateReligionGreatPeopleRateModifier();
		if (iGreatPeopleRateModifier != 0)
		{
			if (!bFirst)
				szBuffer.append(L", ");
			//bFirst = false;
			szBuffer.append(gDLL->getText("TXT_KEY_RELIGION_BIRTH_RATE_MOD",
					iGreatPeopleRateModifier));
		}
	}
}

void CvGameTextMgr::setCorporationHelp(CvWStringBuffer &szBuffer,
	CorporationTypes eCorporation, bool bCivilopedia)
{
	if (eCorporation == NO_CORPORATION)
		return;

	CvCorporationInfo& kCorporation = GC.getInfo(eCorporation);

	if (!bCivilopedia)
	{
		szBuffer.append(CvWString::format(SETCOLR L"%s" ENDCOLR,
				TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"), kCorporation.getDescription()));
	}

	CvWString szTempBuffer;
	FOR_EACH_ENUM(Yield)
	{
		int iYieldProduced = GC.getInfo(eCorporation).
				getYieldProduced(eLoopYield);
		if (getActivePlayer() != NO_PLAYER)
		{
			iYieldProduced *= GC.getInfo(GC.getMap().getWorldSize()).
					getCorporationMaintenancePercent();
			iYieldProduced /= 100;
		}

		if (iYieldProduced != 0)
		{
			if (!szTempBuffer.empty())
				szTempBuffer += L", ";
			if (iYieldProduced % 100 == 0)
			{
				szTempBuffer += CvWString::format(L"%s%d%c",
					iYieldProduced > 0 ? L"+" : L"",
					iYieldProduced / 100,
					GC.getInfo(eLoopYield).getChar());
			}
			else
			{
				szTempBuffer += CvWString::format(L"%s%.2f%c",
					iYieldProduced > 0 ? L"+" : L"",
					0.01f * abs(iYieldProduced),
					GC.getInfo(eLoopYield).getChar());
			}
		}
	}

	if (!szTempBuffer.empty())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_CORPORATION_ALL_CITIES",
				szTempBuffer.GetCString()));
	}

	szTempBuffer.clear();
	FOR_EACH_ENUM(Commerce)
	{
		int iCommerceProduced = GC.getInfo(eCorporation).
				getCommerceProduced(eLoopCommerce);
		if (getActivePlayer() != NO_PLAYER)
		{
			iCommerceProduced *= GC.getInfo(GC.getMap().getWorldSize()).
					getCorporationMaintenancePercent();
			iCommerceProduced /= 100;
		}
		if (iCommerceProduced != 0)
		{
			if (!szTempBuffer.empty())
				szTempBuffer += L", ";

			if (iCommerceProduced % 100 == 0)
			{
				szTempBuffer += CvWString::format(L"%s%d%c",
					iCommerceProduced > 0 ? L"+" : L"",
					iCommerceProduced / 100,
					GC.getInfo(eLoopCommerce).getChar());
			}
			else
			{
				szTempBuffer += CvWString::format(L"%s%.2f%c",
					iCommerceProduced > 0 ? L"+" : L"",
					0.01f * abs(iCommerceProduced),
					GC.getInfo(eLoopCommerce).getChar());
			}

		}
	}
	if (!szTempBuffer.empty())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_CORPORATION_ALL_CITIES",
				szTempBuffer.GetCString()));
	}
	if (!bCivilopedia)
	{
		if (kCorporation.getTechPrereq() != NO_TECH)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_CORPORATION_FOUNDED_FIRST",
					GC.getInfo(kCorporation.getTechPrereq()).getTextKeyWide()));
		}
	}
	szBuffer.append(NEWLINE);
	szBuffer.append(gDLL->getText("TXT_KEY_CORPORATION_BONUS_REQUIRED"));
	bool bFirst = true;
	for (int i = 0; i < kCorporation.getNumPrereqBonuses(); ++i)
	{
		if (bFirst)
			bFirst = false;
		else szBuffer.append(L", ");
		szBuffer.append(CvWString::format(L"%c",
				GC.getInfo(kCorporation.getPrereqBonus(i)).getChar()));
	}

	if (kCorporation.getBonusProduced() != NO_BONUS)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_CORPORATION_BONUS_PRODUCED",
				GC.getInfo(kCorporation.getBonusProduced()).getChar()));
	}
	{
		UnitClassTypes const eFreeUnitClass = kCorporation.getFreeUnitClass();
		if (eFreeUnitClass != NO_UNITCLASS)
		{
			UnitTypes eFreeUnit = (getActivePlayer() != NO_PLAYER ?
					GC.getGame().getActiveCivilization()->getUnit(eFreeUnitClass) :
					GC.getInfo(eFreeUnitClass).getDefaultUnit());
			if (eFreeUnit != NO_UNIT)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_RELIGION_FOUNDER_RECEIVES",
						GC.getInfo(eFreeUnit).getTextKeyWide()));
			}
		}
	}
	std::vector<CorporationTypes> aCompetingCorps;
	bFirst = true;
	FOR_EACH_ENUM2(Corporation, eLoopCorp)
	{
		if (eLoopCorp == eCorporation)
			continue;
		CvCorporationInfo const& kLoopCorp = GC.getInfo(eLoopCorp);
		bool bCompeting = false;
		for (int i = 0; i < kLoopCorp.getNumPrereqBonuses(); ++i)
		{
			for (int j = 0; j < kCorporation.getNumPrereqBonuses(); ++j)
			{
				if (kLoopCorp.getPrereqBonus(i) == kCorporation.getPrereqBonus(j))
				{
					bCompeting = true;
					break;
				}
			}
			if (bCompeting)
				break;
		}
		if (bCompeting)
		{
			CvWString szTemp;
			//szTemp = CvWString::format(L"<link=literal>%s</link>", kLoopCorp.getDescription());
			setCorporationLink(szTemp, eLoopCorp); // advc.001
			setListHelp(szBuffer,
					gDLL->getText("TXT_KEY_CORPORATION_COMPETES").c_str(),
					szTemp.c_str(), L", ", bFirst);
		}
	}
}

void CvGameTextMgr::setCorporationHelpCity(CvWStringBuffer &szBuffer,
	CorporationTypes eCorporation, CvCity *pCity, bool bCityScreen, bool bForceCorporation)
{
	if (pCity == NULL)
		return;

	CvCorporationInfo const& kCorporation = GC.getInfo(eCorporation);

	if (bCityScreen)
	{
		szBuffer.append(CvWString::format(SETCOLR L"%s" ENDCOLR,
				TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"), kCorporation.getDescription()));
		szBuffer.append(NEWLINE);

		if (!GC.getGame().isCorporationFounded(eCorporation) &&
			GC.getInfo(eCorporation).getTechPrereq() != NO_TECH)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_CORPORATION_FOUNDED_FIRST",
					GC.getInfo(kCorporation.getTechPrereq()).getTextKeyWide()));
		}
	}

	if (!bForceCorporation)
	{
		if (!pCity->isHasCorporation(eCorporation))
			return;
	}

	int iNumResources = 0;
	for (int i = 0; i < kCorporation.getNumPrereqBonuses(); ++i)
	{
		iNumResources += pCity->getNumBonuses(kCorporation.getPrereqBonus(i));
	}

	bool const bActive = (pCity->isActiveCorporation(eCorporation) ||
			(bForceCorporation && iNumResources > 0));
	{
		bool bHandled = false;
		FOR_EACH_ENUM(Yield)
		{
			int iYieldRate = 0;
			if (bActive)
			{
				iYieldRate += (iNumResources *
						kCorporation.getYieldProduced(eLoopYield) *
						GC.getInfo(GC.getMap().getWorldSize()).
						getCorporationMaintenancePercent()) / 100;
			}
			if (iYieldRate != 0)
			{
				if (bHandled)
					szBuffer.append(L", ");
				CvWString szTempBuffer;
				szTempBuffer.Format(L"%s%d%c", iYieldRate > 0 ? "+" : "",
						(iYieldRate + 99) / 100,
						GC.getInfo(eLoopYield).getChar());
				szBuffer.append(szTempBuffer);
				bHandled = true;
			}
		}
	}

	bool bHandled = false;
	FOR_EACH_ENUM(Commerce)
	{
		int iCommerceRate = 0;
		if (bActive)
		{
			iCommerceRate += (iNumResources *
					kCorporation.getCommerceProduced(eLoopCommerce) *
					GC.getInfo(GC.getMap().getWorldSize()).
					getCorporationMaintenancePercent()) / 100;
		}
		if (iCommerceRate != 0)
		{
			if (bHandled)
				szBuffer.append(L", ");
			CvWString szTempBuffer;
			szTempBuffer.Format(L"%s%d%c", iCommerceRate > 0 ? "+" : "",
					(iCommerceRate + 99) / 100,
					GC.getInfo(eLoopCommerce).getChar());
			szBuffer.append(szTempBuffer);
			bHandled = true;
		}
	}

	int iMaintenance = 0;

	if (bActive)
	{
		iMaintenance += pCity->calculateCorporationMaintenanceTimes100(eCorporation);
		iMaintenance *= 100 + pCity->getMaintenanceModifier();
		iMaintenance /= 100;
		// <K-Mod>
		iMaintenance = ((100 + GET_PLAYER(pCity->getOwner()).calculateInflationRate()) *
				iMaintenance) / 100; // </K-Mod>
	}

	if (iMaintenance != 0)
	{
		if (bHandled)
			szBuffer.append(L", ");
		CvWString szTempBuffer;
		szTempBuffer.Format(L"%d%c", -iMaintenance / 100, GC.getInfo(COMMERCE_GOLD).getChar());
		szBuffer.append(szTempBuffer);
		bHandled = true;
	}

	if (bCityScreen)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_CORPORATION_BONUS_REQUIRED"));
		bool bFirst = true;
		for (int i = 0; i < kCorporation.getNumPrereqBonuses(); ++i)
		{
			if (bFirst)
				bFirst = false;
			else szBuffer.append(L", ");
			szBuffer.append(CvWString::format(L"%c", GC.getInfo((BonusTypes)
					kCorporation.getPrereqBonus(i)).getChar()));
		}

		if (kCorporation.getBonusProduced() != NO_BONUS && bActive)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_CORPORATION_BONUS_PRODUCED",
					GC.getInfo(kCorporation.getBonusProduced()).getChar()));
		}
	}
	else
	{
		if (kCorporation.getBonusProduced() != NO_BONUS && bActive)
		{
			if (bHandled)
				szBuffer.append(L", ");
			szBuffer.append(CvWString::format(L"%c",
					GC.getInfo(kCorporation.getBonusProduced()).getChar()));
		}
	}
}

void CvGameTextMgr::buildObsoleteString(CvWStringBuffer &szBuffer, int iItem, bool bList, bool bPlayerContext)
{
	if (bList)
		szBuffer.append(NEWLINE);
	szBuffer.append(gDLL->getText("TXT_KEY_TECH_OBSOLETES",
			GC.getInfo((BuildingTypes)iItem).getTextKeyWide()));
}

void CvGameTextMgr::buildObsoleteBonusString(CvWStringBuffer &szBuffer, int iItem, bool bList, bool bPlayerContext)
{
	if (bList)
		szBuffer.append(NEWLINE);
	szBuffer.append(gDLL->getText("TXT_KEY_TECH_OBSOLETES",
			GC.getInfo((BonusTypes)iItem).getTextKeyWide()));
}

void CvGameTextMgr::buildObsoleteSpecialString(CvWStringBuffer &szBuffer, int iItem, bool bList, bool bPlayerContext)
{
	if (bList)
		szBuffer.append(NEWLINE);
	szBuffer.append(gDLL->getText("TXT_KEY_TECH_OBSOLETES_NO_LINK",
			GC.getInfo((SpecialBuildingTypes)iItem).getTextKeyWide()));
}

void CvGameTextMgr::buildMoveString(CvWStringBuffer &szBuffer,
	TechTypes eTech, bool bList, bool bPlayerContext)
{
	FOR_EACH_ENUM(Route)
	{
		// <advc> (This was all in one line)
		int iMoveDiff = (GC.getMOVE_DENOMINATOR() / std::max(1,
				GC.getInfo(eLoopRoute).getMovementCost() +
				(!bPlayerContext ? 0 :
				GET_TEAM(getActiveTeam()).getRouteChange(eLoopRoute))));
		iMoveDiff -= GC.getMOVE_DENOMINATOR() / std::max(1,
				GC.getInfo(eLoopRoute).getMovementCost() +
				(!bPlayerContext ? 0 :
				GET_TEAM(getActiveTeam()).getRouteChange(eLoopRoute)) +
				GC.getInfo(eLoopRoute).getTechMovementChange(eTech)); // </advc>
		if (iMoveDiff != 0)
		{
			if (bList)
				szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_MOVEMENT", -iMoveDiff,
					GC.getInfo(eLoopRoute).getTextKeyWide()));
			bList = true;
		}
	}
}

void CvGameTextMgr::buildFreeUnitString(CvWStringBuffer &szBuffer,
	TechTypes eTech, bool bList, bool bPlayerContext)
{
	UnitTypes eFreeUnit = NO_UNIT;
	if (getActivePlayer() != NO_PLAYER)
		eFreeUnit = GET_PLAYER(getActivePlayer()).getTechFreeUnit(eTech);
	else
	{
		if (GC.getInfo(eTech).getFirstFreeUnitClass() != NO_UNITCLASS)
		{
			eFreeUnit = GC.getInfo((UnitClassTypes)GC.getInfo(eTech).
					getFirstFreeUnitClass()).getDefaultUnit();
		}
	}

	if (eFreeUnit != NO_UNIT)
	{
		if (!bPlayerContext || (GC.getGame().countKnownTechNumTeams(eTech) == 0))
		{
			if (bList)
				szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_TECH_FIRST_RECEIVES",
					GC.getInfo(eFreeUnit).getTextKeyWide()));
		}
	}
}

void CvGameTextMgr::buildFeatureProductionString(CvWStringBuffer &szBuffer,
	TechTypes eTech, bool bList, bool bPlayerContext)
{
	if (GC.getInfo(eTech).getFeatureProductionModifier() != 0)
	{
		if (bList)
			szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_FEATURE_PRODUCTION_MODIFIER",
				GC.getInfo(eTech).getFeatureProductionModifier()));
	}
}

void CvGameTextMgr::buildWorkerRateString(CvWStringBuffer &szBuffer,
	TechTypes eTech, bool bList, bool bPlayerContext)
{
	if (GC.getInfo(eTech).getWorkerSpeedModifier() != 0)
	{
		if (bList)
			szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_WORKERS_FASTER",
				GC.getInfo(eTech).getWorkerSpeedModifier()));
	}
}

void CvGameTextMgr::buildTradeRouteString(CvWStringBuffer &szBuffer,
	TechTypes eTech, bool bList, bool bPlayerContext)
{
	if (GC.getInfo(eTech).getTradeRoutes() != 0)
	{
		if (bList)
			szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_TRADE_ROUTES",
				GC.getInfo(eTech).getTradeRoutes()));
	}
}

void CvGameTextMgr::buildHealthRateString(CvWStringBuffer &szBuffer,
	TechTypes eTech, bool bList, bool bPlayerContext)
{
	if (GC.getInfo(eTech).getHealth() != 0)
	{
		if (bList)
			szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_HEALTH_ALL_CITIES",
				abs(GC.getInfo(eTech).getHealth()),
				GC.getInfo(eTech).getHealth() > 0 ?
				gDLL->getSymbolID(HEALTHY_CHAR) :
				gDLL->getSymbolID(UNHEALTHY_CHAR)));
	}
}

void CvGameTextMgr::buildHappinessRateString(CvWStringBuffer &szBuffer,
	TechTypes eTech, bool bList, bool bPlayerContext)
{
	if (GC.getInfo(eTech).getHappiness() != 0)
	{
		if (bList)
			szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_HAPPINESS_ALL_CITIES",
				abs(GC.getInfo(eTech).getHappiness()),
				GC.getInfo(eTech).getHappiness() > 0 ?
				gDLL->getSymbolID(HAPPY_CHAR): gDLL->getSymbolID(UNHAPPY_CHAR)));
	}
}

void CvGameTextMgr::buildFreeTechString(CvWStringBuffer &szBuffer,
	TechTypes eTech, bool bList, bool bPlayerContext)
{
	if (GC.getInfo(eTech).getFirstFreeTechs() > 0)
	{
		if (!bPlayerContext || (GC.getGame().countKnownTechNumTeams(eTech) == 0))
		{
			if (bList)
				szBuffer.append(NEWLINE);
			if (GC.getInfo(eTech).getFirstFreeTechs() == 1)
				szBuffer.append(gDLL->getText("TXT_KEY_TECH_FIRST_FREE_TECH"));
			else
			{
				szBuffer.append(gDLL->getText("TXT_KEY_TECH_FIRST_FREE_TECHS",
						GC.getInfo(eTech).getFirstFreeTechs()));
			}
		}
	}
}

// advc.500c:
void CvGameTextMgr::buildNoFearForSafetyString(CvWStringBuffer &szBuffer,
	TechTypes eTech, bool bList, bool bPlayerContext)
{
	if (!GC.getInfo(eTech).get(CvTechInfo::NoFearForSafety))
		return;
	if (bList)
		szBuffer.append(NEWLINE);
	szBuffer.append(gDLL->getText("TXT_KEY_TECH_NO_FEAR_FOR_SAFETY"));
}

void CvGameTextMgr::buildLOSString(CvWStringBuffer &szBuffer,
	TechTypes eTech, bool bList, bool bPlayerContext)
{
	if (GC.getInfo(eTech).isExtraWaterSeeFrom() &&
		(!bPlayerContext || !(GET_TEAM(getActiveTeam()).isExtraWaterSeeFrom())))
	{
		if (bList)
			szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_EXTRA_SIGHT"));
	}
}

void CvGameTextMgr::buildMapCenterString(CvWStringBuffer &szBuffer,
	TechTypes eTech, bool bList, bool bPlayerContext)
{
	if (GC.getInfo(eTech).isMapCentering() &&
		(!bPlayerContext || !(GET_TEAM(getActiveTeam()).isMapCentering())))
	{
		if (bList)
			szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_CENTERS_MAP"));
	}
}

void CvGameTextMgr::buildMapRevealString(CvWStringBuffer &szBuffer,
	TechTypes eTech, bool bList)
{
	if (GC.getInfo(eTech).isMapVisible())
	{
		if (bList)
			szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_REVEALS_MAP"));
	}
}

void CvGameTextMgr::buildMapTradeString(CvWStringBuffer &szBuffer,
	TechTypes eTech, bool bList, bool bPlayerContext)
{
	if (GC.getInfo(eTech).isMapTrading() &&
		(!bPlayerContext || !(GET_TEAM(getActiveTeam()).isMapTrading())))
	{
		if (bList)
			szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_ENABLES_MAP_TRADING"));
	}
}

void CvGameTextMgr::buildTechTradeString(CvWStringBuffer &szBuffer,
	TechTypes eTech, bool bList, bool bPlayerContext)
{
	if (GC.getInfo(eTech).isTechTrading() &&
		(!bPlayerContext || !(GET_TEAM(getActiveTeam()).isTechTrading())))
	{
		if (bList)
			szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_ENABLES_TECH_TRADING"));
	}
}

void CvGameTextMgr::buildGoldTradeString(CvWStringBuffer &szBuffer,
	TechTypes eTech, bool bList, bool bPlayerContext)
{
	if (GC.getInfo(eTech).isGoldTrading() &&
		(!bPlayerContext || !GET_TEAM(getActiveTeam()).isGoldTrading()))
	{
		if (bList)
			szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_ENABLES_GOLD_TRADING"));
	}
}

void CvGameTextMgr::buildOpenBordersString(CvWStringBuffer &szBuffer,
	TechTypes eTech, bool bList, bool bPlayerContext)
{
	if (GC.getInfo(eTech).isOpenBordersTrading() &&
		(!bPlayerContext || !(GET_TEAM(getActiveTeam()).isOpenBordersTrading())))
	{
		if (bList)
			szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_ENABLES_OPEN_BORDERS"));
	}
}

void CvGameTextMgr::buildDefensivePactString(CvWStringBuffer &szBuffer,
	TechTypes eTech, bool bList, bool bPlayerContext)
{
	if (GC.getInfo(eTech).isDefensivePactTrading() &&
		(!bPlayerContext || !(GET_TEAM(getActiveTeam()).isDefensivePactTrading())))
	{
		if (bList)
			szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_ENABLES_DEFENSIVE_PACTS"));
	}
}

void CvGameTextMgr::buildPermanentAllianceString(CvWStringBuffer &szBuffer,
	TechTypes eTech, bool bList, bool bPlayerContext)
{
	if (GC.getInfo(eTech).isPermanentAllianceTrading() &&
		(!bPlayerContext ||
		(!GET_TEAM(getActiveTeam()).isPermanentAllianceTrading() &&
		GC.getGame().isOption(GAMEOPTION_PERMANENT_ALLIANCES))))
	{
		if (bList)
			szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_ENABLES_PERM_ALLIANCES"));
	}
}

void CvGameTextMgr::buildVassalStateString(CvWStringBuffer &szBuffer,
	TechTypes eTech, bool bList, bool bPlayerContext)
{
	if (GC.getInfo(eTech).isVassalStateTrading() &&
		(!bPlayerContext ||
		(!GET_TEAM(getActiveTeam()).isVassalStateTrading() &&
		GC.getGame().isOption(GAMEOPTION_NO_VASSAL_STATES))))
	{
		if (bList)
			szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_ENABLES_VASSAL_STATES"));
	}
}

void CvGameTextMgr::buildBridgeString(CvWStringBuffer &szBuffer,
	TechTypes eTech, bool bList, bool bPlayerContext)
{
	if (GC.getInfo(eTech).isBridgeBuilding() &&
		(!bPlayerContext || !GET_TEAM(getActiveTeam()).isBridgeBuilding()))
	{
		if (bList)
			szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_ENABLES_BRIDGE_BUILDING"));
	}
}

void CvGameTextMgr::buildIrrigationString(CvWStringBuffer &szBuffer,
	TechTypes eTech, bool bList, bool bPlayerContext)
{
	if (GC.getInfo(eTech).isIrrigation() &&
		(!bPlayerContext || !GET_TEAM(getActiveTeam()).isIrrigation()))
	{
		if (bList)
			szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_SPREAD_IRRIGATION"));
	}
}

void CvGameTextMgr::buildIgnoreIrrigationString(CvWStringBuffer &szBuffer,
	TechTypes eTech, bool bList, bool bPlayerContext)
{
	if (GC.getInfo(eTech).isIgnoreIrrigation() &&
		(!bPlayerContext || !GET_TEAM(getActiveTeam()).isIgnoreIrrigation()))
	{
		if (bList)
			szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_IRRIGATION_ANYWHERE"));
	}
}

void CvGameTextMgr::buildWaterWorkString(CvWStringBuffer &szBuffer,
	TechTypes eTech, bool bList, bool bPlayerContext)
{
	if (GC.getInfo(eTech).isWaterWork() &&
		(!bPlayerContext || !GET_TEAM(getActiveTeam()).isWaterWork()))
	{
		if (bList)
			szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_WATER_WORK"));
	}
}

void CvGameTextMgr::buildImprovementString(CvWStringBuffer &szBuffer, TechTypes eTech,
	BuildTypes eBuild, bool bList, bool bPlayerContext) // advc: eBuild param was 'int iImprovement'
{
    // doc: exclude graphical only
    if (GC.getInfo(eBuild).isGraphicalOnly())
        return;

	bool bTechFound = false;

	if (GC.getInfo(eBuild).getTechPrereq() == NO_TECH)
	{
		FOR_EACH_ENUM(Feature)
		{
			if (GC.getInfo(eBuild).getFeatureTech(eLoopFeature) == eTech)
				bTechFound = true;
		}
	}
	else
	{
		if (GC.getInfo(eBuild).getTechPrereq() == eTech)
			bTechFound = true;
	}

	if (bTechFound)
	{
		if (bList)
			szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_CAN_BUILD_IMPROVEMENT",
				GC.getInfo(eBuild).getTextKeyWide()));
	}
}

void CvGameTextMgr::buildDomainExtraMovesString(CvWStringBuffer &szBuffer, TechTypes eTech,
	DomainTypes eDomain, bool bList, bool bPlayerContext) // advc: domain param was int
{
	if (GC.getInfo(eTech).getDomainExtraMoves(eDomain) != 0)
	{
		if (bList)
			szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_EXTRA_MOVES",
				GC.getInfo(eTech).getDomainExtraMoves(eDomain),
				GC.getInfo(eDomain).getTextKeyWide()));
	}
}

void CvGameTextMgr::buildAdjustString(CvWStringBuffer &szBuffer, TechTypes eTech,
	CommerceTypes eCommerce, bool bList, bool bPlayerContext) // advc: commerce param was int
{
	if (GC.getInfo(eTech).isCommerceFlexible(eCommerce) &&
		(!bPlayerContext || !GET_TEAM(getActiveTeam()).isCommerceFlexible(eCommerce)))
	{
		if (bList)
			szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_ADJUST_COMMERCE_RATE",
				GC.getInfo(eCommerce).getChar()));
		// <advc.120c>
		if(!bList && eCommerce == COMMERCE_ESPIONAGE &&
			BUGOption::isEnabled("MainInterface__Hide_EspSlider", true))
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_ADJUST_ON_ESPIONGAE_SCREEN"));
		} // </advc.120c>
	}
}

void CvGameTextMgr::buildTerrainTradeString(CvWStringBuffer &szBuffer, TechTypes eTech,
	TerrainTypes eTerrain, bool bList, bool bPlayerContext) // advc: terrain param was int
{
	if (GC.getInfo(eTech).isTerrainTrade(eTerrain) &&
		(!bPlayerContext || !GET_TEAM(getActiveTeam()).isTerrainTrade(eTerrain)))
	{
		if (bList)
			szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_ENABLES_ON_TERRAIN",
				gDLL->getSymbolID(TRADE_CHAR),
				GC.getInfo(eTerrain).getTextKeyWide()));
	}
}

void CvGameTextMgr::buildRiverTradeString(CvWStringBuffer &szBuffer, TechTypes eTech,
	bool bList, bool bPlayerContext)
{
	if (GC.getInfo(eTech).isRiverTrade() &&
		(!bPlayerContext || !GET_TEAM(getActiveTeam()).isRiverTrade()))
	{
		if (bList)
			szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_ENABLES_ON_TERRAIN",
				gDLL->getSymbolID(TRADE_CHAR),
				gDLL->getText("TXT_KEY_MISC_RIVERS").GetCString()));
	}
}

void CvGameTextMgr::buildSpecialBuildingString(CvWStringBuffer &szBuffer, TechTypes eTech,
	SpecialBuildingTypes eSpecial, bool bList, bool bPlayerContext) // special param was 'int iBuildingType'
{
	if (GC.getInfo(eSpecial).getTechPrereq() == eTech)
	{
		if (bList)
			szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_CAN_CONSTRUCT_BUILDING",
				GC.getInfo(eSpecial).getTextKeyWide()));
	}

	if (GC.getInfo(eSpecial).getTechPrereqAnyone() == eTech)
	{
		if (bList)
			szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_CAN_CONSTRUCT_BUILDING_ANYONE",
				GC.getInfo(eSpecial).getTextKeyWide()));
	}
}

void CvGameTextMgr::buildYieldChangeString(CvWStringBuffer &szBuffer, TechTypes eTech,
	ImprovementTypes eImprov, bool bList, bool bPlayerContext) // advc: improv param was 'int iYieldType'
{
	CvWString szTempBuffer;
	CvImprovementInfo const& kImprov = GC.getInfo(eImprov);
	if (bList)
		szTempBuffer.Format(L"<link=literal>%s</link>", kImprov.getDescription());
	else
	{
		szTempBuffer.Format(L"%c<link=literal>%s</link>",
				gDLL->getSymbolID(BULLET_CHAR), kImprov.getDescription());
	}
	setYieldChangeHelp(szBuffer, szTempBuffer, L": ", L"",
			kImprov.getTechYieldChangesArray(eTech), false, bList);
}

bool CvGameTextMgr::buildBonusRevealString(CvWStringBuffer &szBuffer, TechTypes eTech,
	BonusTypes eBonus, bool bFirst, bool bList, bool bPlayerContext) // advc: bonus param was int
{
	if (GC.getInfo(eBonus).getTechReveal() == eTech)
	{
		if (bList && bFirst)
			szBuffer.append(NEWLINE);
		CvWString szTempBuffer;
		szTempBuffer.Format( SETCOLR L"<link=literal>%s</link>" ENDCOLR,
				TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
				GC.getInfo(eBonus).getDescription());
		setListHelp(szBuffer, gDLL->getText("TXT_KEY_MISC_REVEALS").c_str(),
				szTempBuffer, L", ", bFirst);
	}
	return bFirst;
}

bool CvGameTextMgr::buildCivicRevealString(CvWStringBuffer &szBuffer, TechTypes eTech,
	CivicTypes eCivic, bool bFirst, bool bList, bool bPlayerContext) // advc: civic param was int
{

	if (GC.getInfo(eCivic).getTechPrereq() == eTech)
	{
		if (bList && bFirst)
			szBuffer.append(NEWLINE);
		CvWString szTempBuffer;
		szTempBuffer.Format( SETCOLR L"<link=literal>%s</link>" ENDCOLR,
				TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
				GC.getInfo(eCivic).getDescription());
		setListHelp(szBuffer, gDLL->getText("TXT_KEY_MISC_ENABLES").c_str(),
				szTempBuffer, L", ", bFirst);
	}
	return bFirst;
}

bool CvGameTextMgr::buildProcessInfoString(CvWStringBuffer &szBuffer, TechTypes eTech,
	ProcessTypes eProcess, bool bFirst, bool bList, bool bPlayerContext) // advc: process param was int
{

	if (GC.getInfo(eProcess).getTechPrereq() == eTech)
	{
		if (bList && bFirst)
			szBuffer.append(NEWLINE);
		CvWString szTempBuffer;
		szTempBuffer.Format( SETCOLR L"<link=literal>%s</link>" ENDCOLR,
				TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
				GC.getInfo(eProcess).getDescription());
		setListHelp(szBuffer, gDLL->getText("TXT_KEY_MISC_CAN_BUILD").c_str(),
				szTempBuffer, L", ", bFirst);
	}
	return bFirst;
}

bool CvGameTextMgr::buildFoundReligionString(CvWStringBuffer &szBuffer, TechTypes eTech,
	ReligionTypes eReligion, bool bFirst, bool bList, bool bPlayerContext) // advc: religion param was int
{
    // doc: special founding condition for Protestantism
	if (GC.getInfo(eReligion).getTechPrereq() != eTech && !(eTech == ACADEMIA && eReligion == PROTESTANTISM))
		return bFirst; // advc
	if (!bPlayerContext || (GC.getGame().countKnownTechNumTeams(eTech) == 0))
	{
		if (bList && bFirst)
			szBuffer.append(NEWLINE);
		CvWString szTempBuffer;
		if (GC.getGame().isOption(GAMEOPTION_PICK_RELIGION))
			szTempBuffer = gDLL->getText("TXT_KEY_RELIGION_UNKNOWN");
		else
		{
			szTempBuffer.Format( SETCOLR L"<link=literal>%s</link>" ENDCOLR,
					TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
					GC.getInfo(eReligion).getDescription());
		}
		setListHelp(szBuffer, gDLL->getText("TXT_KEY_MISC_FIRST_DISCOVER_FOUNDS").c_str(),
				szTempBuffer, L", ", bFirst);
	}
	return bFirst;
}

bool CvGameTextMgr::buildFoundCorporationString(CvWStringBuffer &szBuffer, TechTypes eTech,
	CorporationTypes eCorp, bool bFirst, bool bList, bool bPlayerContext) // advc: corp param was int
{
	if (GC.getInfo(eCorp).getTechPrereq() != eTech)
		return bFirst; // advc
	if (!bPlayerContext || (GC.getGame().countKnownTechNumTeams(eTech) == 0))
	{
		if (bList && bFirst)
			szBuffer.append(NEWLINE);
		CvWString szTempBuffer;
		szTempBuffer.Format( SETCOLR L"<link=literal>%s</link>" ENDCOLR,
				TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
				GC.getInfo(eCorp).getDescription());
		setListHelp(szBuffer, gDLL->getText("TXT_KEY_MISC_FIRST_DISCOVER_INCORPORATES").c_str(),
				szTempBuffer, L", ", bFirst);
	}
	return bFirst;
}

bool CvGameTextMgr::buildPromotionString(CvWStringBuffer &szBuffer, TechTypes eTech,
	PromotionTypes ePromo, bool bFirst, bool bList, bool bPlayerContext) // advc: promo param was int
{
	if (GC.getInfo(ePromo).getTechPrereq() != eTech)
		return bFirst; // advc
	if (bList && bFirst)
		szBuffer.append(NEWLINE);
	CvWString szTempBuffer;
	szTempBuffer.Format( SETCOLR L"<link=literal>%s</link>" ENDCOLR,
			TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
			GC.getInfo(ePromo).getDescription());
	setListHelp(szBuffer, gDLL->getText("TXT_KEY_MISC_ENABLES").c_str(),
			szTempBuffer, L", ", bFirst);
	return bFirst;
}

// advc.910: Not much BtS code left unchanged here
void CvGameTextMgr::buildSingleLineTechTreeString(CvWStringBuffer &szBuffer,
	TechTypes eTech, bool bPlayerContext)
{
	FAssert(eTech != NO_TECH);
	/*  Separate containers for
		- techs that eTech will immediately enable,
		- techs that have an additional requirement which is yet unmet
		and - not listed by BtS -
		- techs that are merely sped up by eTech (OR req. already met),
		- techs that would speed up eTech if we had them (but we don't).
		Put the tech cost in the first component b/c I want to sort by that. */
	std::vector<std::pair<int,TechTypes> > aieImmediate, aieLater,
			aieSpeedsUp, aieMissingSpeedUps;
	int iORReqsSatisfied = 0;
	if (bPlayerContext)
	{
		PlayerTypes const eActivePlayer = getActivePlayer();
		if (!GET_TEAM(eActivePlayer).isHasTech(eTech) &&
			GET_PLAYER(eActivePlayer).canResearch(eTech))
		{
			for(int i = 0; i < GC.getInfo(eTech).getNumOrTechPrereqs(); i++)
			{
				TechTypes eORReq = GC.getInfo(eTech).getPrereqOrTechs(i);
				if (GET_TEAM(eActivePlayer).isHasTech(eORReq))
					iORReqsSatisfied++;
				else
				{
					aieMissingSpeedUps.push_back(std::make_pair(
							GC.getInfo(eORReq).getResearchCost(), eORReq));
				}
			}
		}
	}
	FOR_EACH_ENUM2(Tech, eLeadsTo)
	{
		bool bCanAlreadyResearch = false;
		bool bAlreadyHas = false;
		if (bPlayerContext)
		{
			PlayerTypes eActivePlayer = getActivePlayer();
			bAlreadyHas = GET_TEAM(eActivePlayer).isHasTech(eLeadsTo);
			bCanAlreadyResearch = (!bAlreadyHas &&
					GET_PLAYER(eActivePlayer).canResearch(eLeadsTo));
		}
		if (bAlreadyHas)
			continue;
		CvTechInfo const& kLeadsTo = GC.getInfo(eLeadsTo);
		bool bTechFound = false;
		bool bAlreadyMetOR = false;
		bool bMeetsOR = false;
		bool bAnyOR = false;
		for (int i = 0; i < kLeadsTo.getNumOrTechPrereqs(); i++)
		{
			TechTypes eOrTech = kLeadsTo.getPrereqOrTechs(i);
			bAnyOR = true;
			if (eOrTech == eTech)
			{
				bTechFound = true;
				bMeetsOR = true;
			}
			else if (bPlayerContext)
			{
				if (GET_TEAM(getActiveTeam()).isHasTech(eOrTech))
					bAlreadyMetOR = true;
			}
		}
		if (!bTechFound && !bCanAlreadyResearch)
		{
			for (int i = 0; i < kLeadsTo.getNumAndTechPrereqs(); i++)
			{
				if (kLeadsTo.getPrereqAndTechs(i) == eTech)
				{
					bTechFound = true;
					FAssertMsg(!bMeetsOR, "The same tech shouldn't be both AND and OR req.");
					break;
				}
			}
		}
		if (!bTechFound)
			continue;
		bool bImmediate = (bAlreadyMetOR || bMeetsOR || !bAnyOR || !bPlayerContext);
		if (bImmediate && bPlayerContext)
		{
			CvTeam const& kActiveTeam = GET_TEAM(getActiveTeam());
			for (int i = 0; i < kLeadsTo.getNumAndTechPrereqs(); i++)
			{
				TechTypes eAndTech = kLeadsTo.getPrereqAndTechs(i);
				if (!kActiveTeam.isHasTech(eAndTech))
				{
					if (bMeetsOR ||
						GC.getInfo(eAndTech).getEra() <= GC.getInfo(eLeadsTo).getEra())
					{
						bImmediate = false;
						break;
					}
				}
			}
		}
		std::pair<int,TechTypes> ieLeadsTo = std::make_pair(
				kLeadsTo.getResearchCost(), eLeadsTo);
		if (bMeetsOR && bAlreadyMetOR)
			aieSpeedsUp.push_back(ieLeadsTo);
		else if (bImmediate)
			aieImmediate.push_back(ieLeadsTo);
		else aieLater.push_back(ieLeadsTo);

	}
	std::sort(aieImmediate.begin(), aieImmediate.end());
	std::sort(aieLater.begin(), aieLater.end());
	std::sort(aieSpeedsUp.begin(), aieSpeedsUp.end());
	std::sort(aieMissingSpeedUps.begin(), aieMissingSpeedUps.end());
	CvWString szTempBuffer;
	bool bFirst = true;
	for (size_t i = 0; i < aieImmediate.size(); i++)
	{
		TechTypes eLeadsTo = aieImmediate[i].second;
		// Mostly as in BtS
		szTempBuffer.Format(SETCOLR L"<link=literal>%s</link>" ENDCOLR,
				TEXT_COLOR("COLOR_TECH_TEXT"),
				GC.getInfo(eLeadsTo).getDescription());
		setListHelp(szBuffer, gDLL->getText("TXT_KEY_MISC_LEADS_TO").c_str(),
				szTempBuffer, L", ", bFirst);
	}
	bFirst = true;
	for (size_t i = 0; i < aieLater.size(); i++)
	{
		TechTypes eLeadsTo = aieLater[i].second;
		// No color
		szTempBuffer.Format(L"<link=literal>%s</link>",
				GC.getInfo(eLeadsTo).getDescription());
		setListHelp(szBuffer, gDLL->getText(aieImmediate.empty() ?
				"TXT_KEY_MISC_LATER_LEADS_TO" :
				"TXT_KEY_MISC_AND_LATER").c_str(), szTempBuffer, L", ", bFirst);
	}
	FAssert(GC.getDefineINT(CvGlobals::TECH_COST_FIRST_KNOWN_PREREQ_MODIFIER) == 0); // Not accounted for above
	int iSpeedUpPercent = GC.getDefineINT(CvGlobals::TECH_COST_KNOWN_PREREQ_MODIFIER);
	if (iSpeedUpPercent <= 0)
	{
		FAssert(iSpeedUpPercent > 0);
		return;
	}
	bFirst = true;
	for (size_t i = 0; i < aieSpeedsUp.size(); i++)
	{
		TechTypes eLeadsTo = aieSpeedsUp[i].second;
		szTempBuffer.Format(SETCOLR L"<link=literal>%s</link>" ENDCOLR,
				TEXT_COLOR("COLOR_TECH_TEXT"),
				GC.getInfo(eLeadsTo).getDescription());
		setListHelp(szBuffer, gDLL->getText("TXT_KEY_MISC_SPEEDS_UP").c_str(),
				szTempBuffer, L", ", bFirst);
	}
	if (!aieSpeedsUp.empty())
	{
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_SPEED_UP_BY_PERCENT",
				iSpeedUpPercent));
	}
	bFirst = true;
	for (size_t i = 0; i < aieMissingSpeedUps.size(); i++)
	{
		TechTypes eORReq = aieMissingSpeedUps[i].second;
		szTempBuffer.Format(SETCOLR L"<link=literal>%s</link>" ENDCOLR,
				TEXT_COLOR("COLOR_TECH_TEXT"),
				GC.getInfo(eORReq).getDescription());
		setListHelp(szBuffer, gDLL->getText("TXT_KEY_MISC_CAN_BE_SPED_UP_BY").c_str(),
				szTempBuffer, L", ", bFirst);
	}
	if (!aieMissingSpeedUps.empty())
	{
		szBuffer.append(gDLL->getText(aieMissingSpeedUps.size() > 1 ?
				"TXT_KEY_MISC_CAN_BE_SPED_UP_BY_PERCENT_EACH" :
				(iORReqsSatisfied > 1 ?
				"TXT_KEY_MISC_CAN_BE_SPED_UP_BY_ANOTHER_PERCENT" :
				"TXT_KEY_MISC_CAN_BE_SPED_UP_BY_PERCENT"),
				iSpeedUpPercent));
	}
}

// Information about other prerequisite technologies to eTech besides eFromTech
void CvGameTextMgr::buildTechTreeString(CvWStringBuffer &szBuffer, TechTypes eTech,
	bool bPlayerContext, TechTypes eFromTech)
{
	CvWString szTempBuffer;	// Formatting

	if (eTech == NO_TECH || eFromTech == NO_TECH)
	{
		FErrorMsg("Can this happen?"); // advc.test
		return;
	}
	szTempBuffer.Format(SETCOLR L"%s" ENDCOLR, TEXT_COLOR("COLOR_TECH_TEXT"),
			GC.getInfo(eTech).getDescription());
	szBuffer.append(szTempBuffer);

	// Loop through OR prerequisites to make list
	CvWString szOtherOrTechs;
	int iOtherOrTechs = 0;
	bool bOrTechFound = false;
	bool bFirstOtherOrTech = true;
	for (int i = 0; i < GC.getInfo(eTech).getNumOrTechPrereqs(); i++)
	{
		TechTypes const eTestTech = GC.getInfo(eTech).getPrereqOrTechs(i);
		bool bTechAlreadyResearched = false;
		if (bPlayerContext)
			bTechAlreadyResearched = GET_TEAM(getActiveTeam()).isHasTech(eTestTech);
		if (!bTechAlreadyResearched)
		{
			if (eTestTech == eFromTech)
				bOrTechFound = true;
			else
			{
				szTempBuffer.Format( SETCOLR L"%s" ENDCOLR,
						TEXT_COLOR("COLOR_TECH_TEXT"),
						GC.getInfo(eTestTech).getDescription());
				setListHelp(szOtherOrTechs, L"", szTempBuffer,
						gDLL->getText("TXT_KEY_OR").c_str(), bFirstOtherOrTech);
				iOtherOrTechs++;
			}
		}
	}

	// Loop through AND prerequisites to make list
	CvWString szOtherAndTechs;
	int iOtherAndTechs = 0;
	bool bAndTechFound = false;
	bool bFirstOtherAndTech = true;
	for (int i = 0; i < GC.getInfo(eTech).getNumAndTechPrereqs(); i++)
	{
		TechTypes const eTestTech = GC.getInfo(eTech).getPrereqAndTechs(i);
		bool bTechAlreadyResearched = false;
		if (bPlayerContext)
			bTechAlreadyResearched = GET_TEAM(getActiveTeam()).isHasTech(eTestTech);
		if (!bTechAlreadyResearched)
		{
			if (eTestTech == eFromTech)
				bAndTechFound = true;
			else
			{
				szTempBuffer.Format( SETCOLR L"%s" ENDCOLR,
						TEXT_COLOR("COLOR_TECH_TEXT"),
						GC.getInfo(eTestTech).getDescription());
				setListHelp(szOtherAndTechs, L"", szTempBuffer,
						L", ", bFirstOtherAndTech);
				iOtherAndTechs++;
			}
		}
	}

	if ((bOrTechFound || bAndTechFound) &&
		(iOtherAndTechs > 0 || iOtherOrTechs > 0))
	{
		szBuffer.append(L' ');
		if (iOtherAndTechs > 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_WITH_SPACE"));
			szBuffer.append(szOtherAndTechs);
		}
		if (iOtherOrTechs > 0)
		{
			if (bAndTechFound)
			{
				if (iOtherAndTechs > 0)
					szBuffer.append(gDLL->getText("TXT_KEY_AND_SPACE"));
				else szBuffer.append(gDLL->getText("TXT_KEY_WITH_SPACE"));
				szBuffer.append(szOtherOrTechs);
			}
			else if (bOrTechFound)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_ALTERNATIVELY_DERIVED",
						GC.getInfo(eTech).getTextKeyWide(), szOtherOrTechs.GetCString()));
			}
		}
	}
}

// advc.034:
void CvGameTextMgr::buildDisengageString(CvWString& szString, PlayerTypes ePlayer,
	PlayerTypes eOther)
{
	int iTurns = 0;
	FOR_EACH_DEAL(d)
	{
		if(d->isDisengage() && d->isBetween(ePlayer, eOther))
		{
			iTurns = d->turnsToCancel();
			break;
		}
	}
	FAssert(iTurns >= 0);
	// This is "%s1 (%d2 [NUM2:Turn:Turns])", just what I need.
	szString.append(gDLL->getText("INTERFACE_CITY_PRODUCTION",
			gDLL->getText("TXT_KEY_MISC_OPEN_BORDERS").GetCString(), iTurns));
}


void CvGameTextMgr::setPromotionHelp(CvWStringBuffer &szBuffer,
	PromotionTypes ePromotion, bool bCivilopediaText)
{
	if (!bCivilopediaText)
	{
		CvWString szTempBuffer;
		if (ePromotion == NO_PROMOTION)
			return;
		CvPromotionInfo const& kPromo = GC.getInfo(ePromotion);
		szTempBuffer.Format( SETCOLR L"%s" ENDCOLR ,
				TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
				kPromo.getDescription());
		szBuffer.append(szTempBuffer);
	}
	parsePromotionHelp(szBuffer, ePromotion);
}

void CvGameTextMgr::setUnitCombatHelp(CvWStringBuffer &szBuffer, UnitCombatTypes eUnitCombat)
{
	szBuffer.append(GC.getInfo(eUnitCombat).getDescription());
}

void CvGameTextMgr::setImprovementHelp(CvWStringBuffer &szBuffer, ImprovementTypes eImprovement, bool bCivilopediaText)
{
	if(eImprovement == NO_IMPROVEMENT)
	{
		FAssertMsg(eImprovement != NO_IMPROVEMENT, "Can this happen?"); // advc.test
		return;
	}
	CvWString szTempBuffer;
	CvWString szFirstBuffer;

	CvImprovementInfo const& kImprov = GC.getInfo(eImprovement);
	if (!bCivilopediaText) // advc (note): Redundantly implemented in Pedia
	{
		szTempBuffer.Format( SETCOLR L"%s" ENDCOLR, TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
				kImprov.getDescription());
		szBuffer.append(szTempBuffer);

		setYieldChangeHelp(szBuffer, L", ", L"", L"", kImprov.getYieldChangeArray(), false, false);

		setYieldChangeHelp(szBuffer, L"", L"",
				gDLL->getText("TXT_KEY_MISC_WITH_IRRIGATION").c_str(),
				kImprov.getIrrigatedYieldChangeArray());
		setYieldChangeHelp(szBuffer, L"", L"",
				gDLL->getText("TXT_KEY_MISC_ON_HILLS").c_str(),
				kImprov.getHillsYieldChangeArray());
		setYieldChangeHelp(szBuffer, L"", L"",
				gDLL->getText("TXT_KEY_MISC_ALONG_RIVER").c_str(),
				kImprov.getRiverSideYieldChangeArray());
        // doc: coastal yield change
		setYieldChangeHelp(szBuffer, L"", L"",
		        gDLL->getText("TXT_KEY_MISC_COASTAL").c_str(),
		        kImprov.getCoastalYieldChangeArray());

		FOR_EACH_ENUM(Tech)
		{
			FOR_EACH_ENUM(Yield)
			{
				int iYieldChange = kImprov.getTechYieldChanges(eLoopTech, eLoopYield);
				if (iYieldChange != 0)
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_IMPROVEMENT_WITH_TECH",
							iYieldChange, GC.getInfo(eLoopYield).getChar(),
							GC.getInfo(eLoopTech).getTextKeyWide()));
				}
			}
		}  // <advc.004> Based on Python code in Pedia
		FOR_EACH_ENUM(Route)
		{
			FOR_EACH_ENUM(Yield)
			{
				int iYieldChange = kImprov.getRouteYieldChanges(eLoopRoute, eLoopYield);
				if (iYieldChange != 0)
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_IMPROVEMENT_WITH_ROUTE",
							iYieldChange, GC.getInfo(eLoopYield).getChar(),
							GC.getInfo(eLoopRoute).getTextKeyWide()));
				}
			}
		} // </advc.004>
		FOR_EACH_ENUM(Civic)
		{
			FOR_EACH_ENUM(Yield)
			{
				int iYieldChange = GC.getInfo(eLoopCivic).getImprovementYieldChanges(
						eImprovement, eLoopYield);
				if (iYieldChange != 0)
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_CIVIC_IMPROVEMENT_YIELD_CHANGE",
							iYieldChange, GC.getInfo(eLoopYield).getChar()));
					szTempBuffer.Format( SETCOLR L"%s" ENDCOLR ,
							TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
							GC.getInfo(eLoopCivic).getDescription());
					szBuffer.append(szTempBuffer);
				}
			}
		}
	}

	if (kImprov.isRequiresRiverSide())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_IMPROVEMENT_REQUIRES_RIVER"));
	}
	if (kImprov.isCarriesIrrigation())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_IMPROVEMENT_CARRIES_IRRIGATION"));
	}
	if (bCivilopediaText)
	{
		if (kImprov.isNoFreshWater())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_IMPROVEMENT_NO_BUILD_FRESH_WATER"));
		}
		if (kImprov.isWater())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_IMPROVEMENT_BUILD_ONLY_WATER"));
		}
		if (kImprov.isRequiresFlatlands())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_IMPROVEMENT_ONLY_BUILD_FLATLANDS"));
		}
	}

	if (kImprov.getImprovementUpgrade() != NO_IMPROVEMENT)
	{
		int iTurns = GC.getGame().getImprovementUpgradeTime(eImprovement);

		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_IMPROVEMENT_EVOLVES",
				GC.getInfo(kImprov.getImprovementUpgrade()).getTextKeyWide(), iTurns));
	}
	{
		/*	advc: Was iLast. Since we're not showing the chance of discovery,
			we may as well put all resources in one list even if they
			don't all have the same chance of discovery. */
		bool bFirst = true;
		FOR_EACH_ENUM(Bonus)
		{
			if (kImprov.getImprovementBonusDiscoverRand(eLoopBonus) > 0)
			{
				szFirstBuffer.Format(L"%s%s", NEWLINE,
						gDLL->getText("TXT_KEY_IMPROVEMENT_CHANCE_DISCOVER").c_str());
				szTempBuffer.Format(L"%c", GC.getInfo(eLoopBonus).getChar());
				setListHelp(szBuffer, szFirstBuffer, szTempBuffer, L", ", bFirst);
			}
		}
	}
	if (kImprov.getDefenseModifier() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_IMPROVEMENT_DEFENSE_MODIFIER",
				kImprov.getDefenseModifier()));
	}
	{
		int iHappiness = kImprov.getHappiness();
		if (iHappiness != 0)
		{
			szBuffer.append(NEWLINE);
			szTempBuffer.Format(L"%d", abs(iHappiness)); // advc.901
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_ICON_CHANGE_NEARBY_CITIES",
					szTempBuffer.GetCString(), // advc.901: Pass number as string
					/*	UNOFFICIAL_PATCH, Bugfix, 08/28/09, jdog5000:
						se absolute value with unhappy face */
					gDLL->getSymbolID(iHappiness > 0 ? HAPPY_CHAR :UNHAPPY_CHAR)));
		}
	}  // <advc.901>
	{
		int iHealthPercent = kImprov.get(CvImprovementInfo::HealthPercent);
		if (iHealthPercent != 0)
		{
			szBuffer.append(NEWLINE);
			float fAbsHealth = abs(iHealthPercent) / 100.0f;
			if (iHealthPercent % 10 == 0)
				szTempBuffer.Format(L"%.1f", fAbsHealth);
			else szTempBuffer.Format(L"%.2f", fAbsHealth);
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_ICON_CHANGE_NEARBY_CITIES",
					szTempBuffer.GetCString(),
					iHealthPercent > 0 ? gDLL->getSymbolID(HEALTHY_CHAR) :
					gDLL->getSymbolID(UNHEALTHY_CHAR)));
		}
	} // </advc.901>
	if (kImprov.isActsAsCity())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_IMPROVEMENT_DEFENSE_MODIFIER_EXTRA"));
	}
	int iGWFeatureProtection = kImprov.get(CvImprovementInfo::GWFeatureProtection); // advc.055
	if (kImprov.getFeatureGrowthProbability() > 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_IMPROVEMENT_MORE_GROWTH"));
		// <advc.055>
		if (iGWFeatureProtection >= 100)
		{
			szBuffer.append(L" ");
			szBuffer.append(gDLL->getText("TXT_KEY_IMPROVEMENT_AND_PROTECT_FROM_GW"));
			iGWFeatureProtection = 0; // Don't display again
		} // </advc.055>
	}
	else if (kImprov.getFeatureGrowthProbability() < 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_IMPROVEMENT_LESS_GROWTH"));
	}  // <advc.055>
	if (iGWFeatureProtection > 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_IMPROVEMENT_PROTECTS_FEATURE_FROM_GW",
				iGWFeatureProtection));
	} // </advc.055>
	if (bCivilopediaText)
	{
		if (kImprov.getPillageGold() > 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_IMPROVEMENT_PILLAGE_YIELDS", kImprov.getPillageGold()));
		}
	}
}

// advc: Merge of two getDealString functions. One was just a wrapper.
void CvGameTextMgr::getDealString(CvWStringBuffer& szBuffer, CvDeal const& kDeal,
	PlayerTypes ePlayerPerspective,  // <advc.004w>
	bool bCancel)
{
	int const iTurnsToCancel = (bCancel ? -1 : kDeal.turnsToCancel()); // </advc.004w>
	CvPlayer const& kFirstPlayer = GET_PLAYER(kDeal.getFirstPlayer());
	CvPlayer const& kSecondPlayer = GET_PLAYER(kDeal.getSecondPlayer());
	bool const bFirstPerspective = (kFirstPlayer.getID() == ePlayerPerspective);
	bool const bSecondPerspective = (kSecondPlayer.getID() == ePlayerPerspective);
	bool const bThirdPerspective = (!bFirstPerspective && !bSecondPerspective);

	CvWStringBuffer szDealOne;
	if (kDeal.getLengthFirst() > 0)
	{
		bool bFirst = true;
		FOR_EACH_TRADE_ITEM(kDeal.getFirstList())
		{
			CvWStringBuffer szTrade;
			getTradeString(szTrade, *pItem, kFirstPlayer.getID(), kSecondPlayer.getID(),
					iTurnsToCancel); // advc.004w
			setListHelp(szDealOne, L"", szTrade.getCString(), L", ", bFirst);
		}
	}

	CvWStringBuffer szDealTwo;
	if (kDeal.getLengthSecond() > 0)
	{
		bool bFirst = true;
		FOR_EACH_TRADE_ITEM(kDeal.getSecondList())
		{
			CvWStringBuffer szTrade;
			getTradeString(szTrade, *pItem, kSecondPlayer.getID(), kFirstPlayer.getID(),
					iTurnsToCancel); // advc.004w
			setListHelp(szDealTwo, L"", szTrade.getCString(), L", ", bFirst);
		}
	}
	// <advc.004w>
	if (!bThirdPerspective && kDeal.isAllDual())
	{
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_DEAL_DUAL",
				szDealOne.getCString(), (bFirstPerspective ?
				kSecondPlayer.getNameKey() : kFirstPlayer.getNameKey())));
	}
	else // </advc.004w>
	if (!szDealOne.isEmpty())
	{
		if (!szDealTwo.isEmpty())
		{
			if (bFirstPerspective)
			{
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_OUR_DEAL",
						szDealOne.getCString(), kSecondPlayer.getNameKey(),
						szDealTwo.getCString()));
			}
			else if (bSecondPerspective)
			{
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_OUR_DEAL",
						szDealTwo.getCString(), kFirstPlayer.getNameKey(),
						szDealOne.getCString()));
			}
			else
			{
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_DEAL",
						kFirstPlayer.getNameKey(), szDealOne.getCString(),
						kSecondPlayer.getNameKey(), szDealTwo.getCString()));
			}
		}
		else
		{
			if (bFirstPerspective)
			{
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_DEAL_ONESIDED_OURS",
						szDealOne.getCString(), kSecondPlayer.getNameKey()));
			}
			else if (bSecondPerspective)
			{
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_DEAL_ONESIDED_THEIRS",
						szDealOne.getCString(), kFirstPlayer.getNameKey()));
			}
			else
			{
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_DEAL_ONESIDED",
						kFirstPlayer.getNameKey(), szDealOne.getCString(),
						kSecondPlayer.getNameKey()));
			}
		}
	}
	else if (!szDealTwo.isEmpty())
	{
		if (bFirstPerspective)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_DEAL_ONESIDED_THEIRS",
					szDealTwo.getCString(), kSecondPlayer.getNameKey()));
		}
		else if (bSecondPerspective)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_DEAL_ONESIDED_OURS",
					szDealTwo.getCString(), kFirstPlayer.getNameKey()));
		}
		else
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_DEAL_ONESIDED",
				kSecondPlayer.getNameKey(), szDealTwo.getCString(),
				kFirstPlayer.getNameKey()));
		}
	}
}


void CvGameTextMgr::getWarplanString(CvWStringBuffer& szString, WarPlanTypes eWarPlan)
{
	switch (eWarPlan)
	{
		case WARPLAN_ATTACKED_RECENT: szString.assign(L"new defensive war"); break;
		case WARPLAN_ATTACKED: szString.assign(L"defensive war"); break;
		case WARPLAN_PREPARING_LIMITED: szString.assign(L"preparing limited war"); break;
		case WARPLAN_PREPARING_TOTAL: szString.assign(L"preparing total war"); break;
		case WARPLAN_LIMITED: szString.assign(L"limited war"); break;
		case WARPLAN_TOTAL: szString.assign(L"total war"); break;
		case WARPLAN_DOGPILE: szString.assign(L"dogpile war"); break;
		case NO_WARPLAN: szString.assign(L"no warplan"); break;
		default:  szString.assign(L"unknown warplan"); break;
	}
}

// advc: Auxiliary function; cut from getAttitudeString.
void CvGameTextMgr::appendToAttitudeBreakdown(CvWStringBuffer& szBreakdown, int iPass,
	int iAttitudeChange, int& iTotal, char const* szTextKey, char const* szTextKeyAlt)
{
	if ((iPass == 0) ? (iAttitudeChange > 0) : (iAttitudeChange < 0))
	{
		CvWString szTempBuffer;
		szTempBuffer.Format(SETCOLR L"%s" ENDCOLR,
				TEXT_COLOR(iAttitudeChange > 0 ?
				"COLOR_POSITIVE_TEXT" : "COLOR_NEGATIVE_TEXT"),
				gDLL->getText(iAttitudeChange > 0 || szTextKeyAlt == NULL ?
				szTextKey : szTextKeyAlt, iAttitudeChange).GetCString());
		szBreakdown.append(NEWLINE);
		szBreakdown.append(szTempBuffer);
		iTotal += iAttitudeChange;
	}
}


void CvGameTextMgr::getAttitudeString(CvWStringBuffer& szBuffer, PlayerTypes ePlayer,
	PlayerTypes eTargetPlayer, /* advc.sha: */ bool bConstCache)
{
	CvPlayerAI& kPlayer = GET_PLAYER(ePlayer);
	if (kPlayer.isHuman())
		return; // K-Mod

	CvGame const& kGame = GC.getGame();
	CvWString szTempBuffer;
	CvWStringBuffer szBreakdown; // advc.sha
	// <advc.sha>
	bool bSHowHiddenAttitude = (GC.getDefineBOOL("SHOW_HIDDEN_ATTITUDE") ||
			kGame.isDebugMode()); // </advc.sha>
	// <advc.004q>
	bool bObscurePersonality = (kGame.isOption(GAMEOPTION_RANDOM_PERSONALITIES) &&
			!kGame.isDebugMode());
	// ATTITUDE_TOWARDS moved to the end of this function // </advc.004q>
	// (K-Mod note: vassal information has been moved from here to a new function)

	// Attitude breakdown ...
	int iTotal = 0; // advc.sha
	for (int iPass = 0; iPass < 2; iPass++)
	{
		// advc: Use an auxiliary function
		appendToAttitudeBreakdown(szBreakdown, iPass,
				kPlayer.AI_getCloseBordersAttitude(eTargetPlayer), iTotal,
				"TXT_KEY_MISC_ATTITUDE_LAND_TARGET");
		// (advc.sha: WarAttitude, PeaceAttitude moved down)
		appendToAttitudeBreakdown(szBreakdown, iPass,
				kPlayer.AI_getSameReligionAttitude(eTargetPlayer), iTotal,
				"TXT_KEY_MISC_ATTITUDE_SAME_RELIGION");
		appendToAttitudeBreakdown(szBreakdown, iPass,
				kPlayer.AI_getDifferentReligionAttitude(eTargetPlayer), iTotal,
				"TXT_KEY_MISC_ATTITUDE_DIFFERENT_RELIGION");
		appendToAttitudeBreakdown(szBreakdown, iPass,
				kPlayer.AI_getBonusTradeAttitude(eTargetPlayer), iTotal,
				"TXT_KEY_MISC_ATTITUDE_BONUS_TRADE");
		appendToAttitudeBreakdown(szBreakdown, iPass,
				kPlayer.AI_getOpenBordersAttitude(eTargetPlayer), iTotal,
				"TXT_KEY_MISC_ATTITUDE_OPEN_BORDERS");
		appendToAttitudeBreakdown(szBreakdown, iPass,
				kPlayer.AI_getDefensivePactAttitude(eTargetPlayer), iTotal,
				"TXT_KEY_MISC_ATTITUDE_DEFENSIVE_PACT");
		appendToAttitudeBreakdown(szBreakdown, iPass,
				kPlayer.AI_getRivalDefensivePactAttitude(eTargetPlayer), iTotal,
				"TXT_KEY_MISC_ATTITUDE_RIVAL_DEFENSIVE_PACT");
		appendToAttitudeBreakdown(szBreakdown, iPass,
				kPlayer.AI_getRivalVassalAttitude(eTargetPlayer), iTotal,
				"TXT_KEY_MISC_ATTITUDE_RIVAL_VASSAL");
		// <advc.130w>
		appendToAttitudeBreakdown(szBreakdown, iPass,
				kPlayer.AI_getExpansionistAttitude(eTargetPlayer), iTotal,
				"TXT_KEY_MISC_ATTITUDE_EXPANSIONIST"); // </advc.130w>
		{
			// advc.130m:
			bool bPastTense = !GET_TEAM(kPlayer.getTeam()).AI_shareWar(TEAMID(eTargetPlayer));
			appendToAttitudeBreakdown(szBreakdown, iPass,
					kPlayer.AI_getShareWarAttitude(eTargetPlayer), iTotal,
					bPastTense ? "TXT_KEY_MISC_ATTITUDE_SHARED_WAR" : // advc.130m
					"TXT_KEY_MISC_ATTITUDE_SHARE_WAR");
		}
		appendToAttitudeBreakdown(szBreakdown, iPass,
				kPlayer.AI_getFavoriteCivicAttitude(eTargetPlayer), iTotal,
				"TXT_KEY_MISC_ATTITUDE_FAVORITE_CIVIC");
		appendToAttitudeBreakdown(szBreakdown, iPass,
				kPlayer.AI_getTradeAttitude(eTargetPlayer), iTotal,
				"TXT_KEY_MISC_ATTITUDE_TRADE");
		appendToAttitudeBreakdown(szBreakdown, iPass,
				kPlayer.AI_getRivalTradeAttitude(eTargetPlayer), iTotal,
				"TXT_KEY_MISC_ATTITUDE_RIVAL_TRADE");
		// advc.130r: Commented out
		/*appendToAttitudeBreakdown(szBreakdown, iPass,
				kPlayer.AI_getColonyAttitude(eTargetPlayer), iTotal,
				"TXT_KEY_MISC_ATTITUDE_FREEDOM");*/
		appendToAttitudeBreakdown(szBreakdown, iPass,
				kPlayer.AI_getAttitudeExtra(eTargetPlayer), iTotal,
				"TXT_KEY_MISC_ATTITUDE_EXTRA_GOOD",
				"TXT_KEY_MISC_ATTITUDE_EXTRA_BAD");
		// <advc.sha> (based on: Show Hidden Attitude Mod 01/22/2010)
		if (bSHowHiddenAttitude)
		{
			appendToAttitudeBreakdown(szBreakdown, iPass,
					kPlayer.AI_getTeamSizeAttitude(eTargetPlayer), iTotal,
					"TXT_KEY_MISC_ATTITUDE_TEAM_SIZE");
			if (!bObscurePersonality) // advc: Moved this check from CvPlayerAI
			{
				appendToAttitudeBreakdown(szBreakdown, iPass,
						kPlayer.AI_getRankDifferenceAttitude(eTargetPlayer), iTotal,
						kGame.getPlayerRank(ePlayer) < kGame.getPlayerRank(eTargetPlayer) ?
						"TXT_KEY_MISC_ATTITUDE_BETTER_RANK" :
						"TXT_KEY_MISC_ATTITUDE_WORSE_RANK");
				appendToAttitudeBreakdown(szBreakdown, iPass,
						kPlayer.AI_getFirstImpressionAttitude(eTargetPlayer), iTotal,
						"TXT_KEY_MISC_ATTITUDE_FIRST_IMPRESSION");
			}
			// Lost-war attitude: now included in WarAttitude (see below)
			/*appendToAttitudeBreakdown(szBreakdown, iPass,
						kPlayer.AI_getLostWarAttitude(eTargetPlayer), iTotal,
						"TXT_KEY_MISC_ATTITUDE_LOST_WAR");*/
		} // </advc.sha>
		// <advc.004q>
		static MemoryTypes aeObscureMemoryTypes[] =
		{
			MEMORY_DENIED_STOP_TRADING, MEMORY_DENIED_JOIN_WAR,
			MEMORY_ACCEPTED_CIVIC, MEMORY_DENIED_CIVIC,
			MEMORY_ACCEPTED_RELIGION, MEMORY_DENIED_RELIGION,
			MEMORY_REJECTED_DEMAND, MEMORY_ACCEPT_DEMAND,
			MEMORY_REFUSED_HELP, MEMORY_GIVE_HELP,
			MEMORY_SPY_CAUGHT, MEMORY_ACCEPTED_STOP_TRADING,
			MEMORY_NUKED_FRIEND, MEMORY_DECLARED_WAR_ON_FRIEND,
		};
		int const iNumObscureMemoryTypes = ARRAYSIZE(aeObscureMemoryTypes);
		// </advc.004q>
		FOR_EACH_ENUM(Memory)
		{
			int iAttitudeChange = kPlayer.AI_getMemoryAttitude(eTargetPlayer, eLoopMemory);
			if ((iPass == 0) ? (iAttitudeChange > 0) : (iAttitudeChange < 0))
			{	/*  <advc.004q> Cap attitude change at 1 for memory types that
					can give away a leader's hidden personality. */
				int iAbsAttitudeChange = std::abs(iAttitudeChange);
				if (iAbsAttitudeChange > 1 && bObscurePersonality &&
					kPlayer.AI_getMemoryCount(eTargetPlayer, eLoopMemory) <= 2)
				{
					for (int i = 0; i < iNumObscureMemoryTypes; i++)
					{
						if (eLoopMemory == aeObscureMemoryTypes[i])
						{
							iAbsAttitudeChange = 1;
							break;
						}
					}
					iAttitudeChange = (iAttitudeChange > 0 ?
							iAbsAttitudeChange : -iAbsAttitudeChange);
				} // </advc.004q>
				szTempBuffer.Format(SETCOLR L"%s" ENDCOLR, TEXT_COLOR(
						(iAttitudeChange > 0) ? "COLOR_POSITIVE_TEXT" : "COLOR_NEGATIVE_TEXT"),
						gDLL->getText("TXT_KEY_MISC_ATTITUDE_MEMORY", iAttitudeChange,
						GC.getInfo(eLoopMemory).getDescription()).GetCString());
				szBreakdown.append(NEWLINE);
				szBreakdown.append(szTempBuffer);
				iTotal += iAttitudeChange;
			}
		}
		// advc.sha: Moved down along with WarAttitude (see below); keep these together.
		appendToAttitudeBreakdown(szBreakdown, iPass,
				kPlayer.AI_getPeaceAttitude(eTargetPlayer), iTotal,
				"TXT_KEY_MISC_ATTITUDE_PEACE");
		// advc.sha: Moved down so that the correct iTotal can be passed along
		appendToAttitudeBreakdown(szBreakdown, iPass,
				kPlayer.AI_getWarAttitude(eTargetPlayer, iTotal), iTotal,
				"TXT_KEY_MISC_ATTITUDE_WAR");
	}
	// <advc.004q>
#ifndef ENABLE_REPRO_TEST
	int iTotalCached = kPlayer.AI_getAttitudeVal(eTargetPlayer, false);
	if (!bConstCache && bSHowHiddenAttitude && !bObscurePersonality &&
		iTotal != iTotalCached && !kGame.isNetworkMultiPlayer() &&
		// advc.130u: bForced=false is ignored among teammates
		kPlayer.getTeam() != TEAMID(eTargetPlayer))
	{
		FAssertMsg(iTotal == iTotalCached, "Attitude cache out of date "
				"(OK after loading a save created prior to AdvCiv 0.98)");
		kPlayer.AI_updateAttitude(eTargetPlayer, true);
		// Try again, this time without recursion. szBuffer hasn't been changed yet.
		getAttitudeString(szBuffer, ePlayer, eTargetPlayer, true);
		return;
	}
#endif
	// Attitude string - append this to szBuffer before appending the breakdown
	szBuffer.append(NEWLINE);
	//szBuffer.append(gDLL->getText("TXT_KEY_ATTITUDE_TOWARDS", GC.getInfo(kPlayer.AI_getAttitude(eTargetPlayer)).getTextKeyWide(), GET_PLAYER(eTargetPlayer).getNameKey()));
	// Replacing the BtS line above
	wchar const* szAttitude = GC.getInfo(
			kPlayer.AI_getAttitude(eTargetPlayer)).getTextKeyWide();
	wchar const* szTargetName = GET_PLAYER(eTargetPlayer).getCivilizationShortDescription(); // rfc
	AttitudeTypes eAttitudeCached = kPlayer.AI_getAttitudeFromValue(iTotal);
	if(eAttitudeCached == ATTITUDE_CAUTIOUS)
	{
		if(iTotal == 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ZERO_ATTITUDE_TOWARDS",
					szAttitude, szTargetName));
		}
		else if(iTotal > 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_POSITIVE_NEUTRAL_ATTITUDE_TOWARDS",
				szAttitude, iTotal, szTargetName));
		}
		else szBuffer.append(gDLL->getText("TXT_KEY_NEGATIVE_NEUTRAL_ATTITUDE_TOWARDS",
				szAttitude, iTotal, szTargetName));
	}
	else if(eAttitudeCached > ATTITUDE_CAUTIOUS)
	{
		szBuffer.append(gDLL->getText("TXT_KEY_GOOD_ATTITUDE_TOWARDS",
				szAttitude, iTotal, szTargetName));
	}
	else szBuffer.append(gDLL->getText("TXT_KEY_BAD_ATTITUDE_TOWARDS",
			szAttitude, iTotal, szTargetName));

	szBuffer.append(szBreakdown);
	// </advc.004q>
	/*if (NO_PLAYER != eTargetPlayer) {
		int iWarWeariness = GET_PLAYER(eTargetPlayer).getModifiedWarWearinessPercentAnger(GET_TEAM(GET_PLAYER(eTargetPlayer).getTeam()).getWarWeariness(eTeam) * std::max(0, 100 + kTeam.getEnemyWarWearinessModifier()));
		if (iWarWeariness / 10000 > 0) {
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_WAR_WEAR_HELP", iWarWeariness / 10000));
		}
	}*/ // K-Mod, I've moved this to a new function
}

// K-Mod:
void CvGameTextMgr::getVassalInfoString(CvWStringBuffer& szBuffer, PlayerTypes ePlayer)
{
	FAssert(ePlayer != NO_PLAYER);

	CvTeam const& kTeam = GET_TEAM(ePlayer);
	if (kTeam.isAVassal())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(CvWString::format(SETCOLR, TEXT_COLOR("COLOR_LIGHT_GREY")));
		CvTeam const& kMaster = GET_TEAM(kTeam.getMasterTeam());
		// <advc.130v>
		if (kTeam.isCapitulated())
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ATTITUDE_VASSAL_CAP_OF",
					kMaster.getName().GetCString()));
		}
		else // </advc.130v>
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ATTITUDE_VASSAL_OF",
					kMaster.getName().GetCString()));
		}
		setVassalRevoltHelp(szBuffer, kMaster.getID(), kTeam.getID());
		szBuffer.append(ENDCOLR);
		return;
	}
	for (TeamIter<CIV_ALIVE,VASSAL_OF> itVassal(kTeam.getID());
		itVassal.hasNext(); ++itVassal)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(CvWString::format(SETCOLR, TEXT_COLOR("COLOR_LIGHT_GREY")));
		szBuffer.append(gDLL->getText("TXT_KEY_ATTITUDE_MASTER_OF",
				itVassal->getName().GetCString()));
		szBuffer.append(ENDCOLR);
	}
}

// K-Mod:
void CvGameTextMgr::getWarWearinessString(CvWStringBuffer& szBuffer,
	PlayerTypes ePlayer, PlayerTypes eTargetPlayer) const
{
	FAssert(ePlayer != NO_PLAYER);
	/*	Show ePlayer's war weariness towards eTargetPlayer.
		(note: this is the reverse of what was shown in the original code.)
		War weariness should be shown in it natural units -
		it's a percentage of population */
	CvPlayer const& kPlayer = GET_PLAYER(ePlayer);

	int iWarWeariness = 0;
	if (eTargetPlayer == NO_PLAYER || eTargetPlayer == ePlayer)
	{
		/*	If eTargetPlayer == NO_PLAYER, show ePlayer's total war weariness?
			There are a couple of problems with displaying the total war weariness:
			information leak, out-of-date information...
			lets do it only for the active player. */
		if (getActivePlayer() == ePlayer)
			iWarWeariness = kPlayer.getWarWearinessPercentAnger();
	}
	else
	{
		CvPlayer const& kTargetPlayer = GET_PLAYER(eTargetPlayer);
		if (atWar(kPlayer.getTeam(), kTargetPlayer.getTeam()) &&
			(GC.getGame().isDebugMode() ||
			GET_PLAYER(getActivePlayer()).canSeeDemographics(ePlayer)))
		{
			iWarWeariness = kPlayer.getModifiedWarWearinessPercentAnger(
					GET_TEAM(kPlayer.getTeam()).getWarWeariness(
					kTargetPlayer.getTeam(), true)
					/ 100);
		}
	}

	iWarWeariness *= 100;
	iWarWeariness /= GC.getPERCENT_ANGER_DIVISOR();

	if (iWarWeariness != 0)
	{
		szBuffer.append(CvWString::format(L"\n%s: %d%%",
				gDLL->getText("TXT_KEY_WAR_WEAR_HELP").GetCString(), iWarWeariness));
	}
}


/*void CvGameTextMgr::getEspionageString(CvWStringBuffer& szBuffer, PlayerTypes ePlayer, PlayerTypes eTargetPlayer)
{
	if (!GC.getGame().isOption(GAMEOPTION_NO_ESPIONAGE))
	{
		CvPlayer& kPlayer = GET_PLAYER(ePlayer);
		TeamTypes eTeam = (TeamTypes) kPlayer.getTeam();
		CvTeam& kTeam = GET_TEAM(eTeam);
		CvPlayer& kTargetPlayer = GET_PLAYER(eTargetPlayer);
		szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_AGAINST_PLAYER",
				kTargetPlayer.getNameKey(),
				kTeam.getEspionagePointsAgainstTeam(kTargetPlayer.getTeam()),
				GET_TEAM(kTargetPlayer.getTeam()).getEspionagePointsAgainstTeam(kPlayer.getTeam())));
	}
}*/ // advc: Obsolete according to a K-Mod comment


void CvGameTextMgr::getTradeString(CvWStringBuffer& szBuffer, const TradeData& tradeData,
	PlayerTypes ePlayer1, PlayerTypes ePlayer2,
	int iTurnsToCancel) // advc.004w
{
	switch (tradeData.m_eItemType)
	{
	case TRADE_GOLD:
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_GOLD", tradeData.m_iData));
		break;
	case TRADE_GOLD_PER_TURN:
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_GOLD_PER_TURN", tradeData.m_iData));
		break;
	case TRADE_MAPS:
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_WORLD_MAP"));
		break;
	case TRADE_SURRENDER:
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_CAPITULATE"));
		break;
	case TRADE_VASSAL:
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_VASSAL"));
		break;
	case TRADE_OPEN_BORDERS:
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_OPEN_BORDERS"));
		break;
	case TRADE_DEFENSIVE_PACT:
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_DEFENSIVE_PACT"));
		break;
	case TRADE_PERMANENT_ALLIANCE:
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_PERMANENT_ALLIANCE"));
		break;
	case TRADE_PEACE_TREATY:
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_PEACE_TREATY",
				// <advc.004w>
				(iTurnsToCancel < 0 ? GC.getDefineINT(CvGlobals::PEACE_TREATY_LENGTH) :
				iTurnsToCancel))); // </advc.004w>
		break;
	case TRADE_TECHNOLOGIES:
		szBuffer.assign(CvWString::format(L"%s", GC.getInfo((TechTypes)tradeData.m_iData).getDescription()));
		break;
	case TRADE_RESOURCES:
		szBuffer.assign(CvWString::format(L"%s", GC.getInfo((BonusTypes)tradeData.m_iData).getDescription()));
		break;
	case TRADE_CITIES:
		szBuffer.assign(CvWString::format(L"%s", GET_PLAYER(ePlayer1).getCity(tradeData.m_iData)->getName().GetCString()));
		break;
	case TRADE_PEACE:
	case TRADE_WAR:
	case TRADE_EMBARGO:
		szBuffer.assign(CvWString::format(L"%s", GET_TEAM((TeamTypes)tradeData.m_iData).getName().GetCString()));
		break;
	case TRADE_CIVIC:
		szBuffer.assign(CvWString::format(L"%s", GC.getInfo((CivicTypes)tradeData.m_iData).getDescription()));
		break;
	case TRADE_RELIGION:
		szBuffer.assign(CvWString::format(L"%s", GC.getInfo((ReligionTypes)tradeData.m_iData).getDescription()));
		break; // <advc.034>
	// doc (edead): relic trade
	case TRADE_SLAVE:
		szBuffer.assign(CvWString::format(L"%s", GET_PLAYER(ePlayer1).getUnit(tradeData.m_iData)->getName().GetCString()));
		break;
	case TRADE_DISENGAGE:
	{
		CvWString szString;
		buildDisengageString(szString, ePlayer1, ePlayer2);
		szBuffer.append(szString);
		break;
	} // </advc.034>
	default:
		FAssert(false);
		break;
	}
}

void CvGameTextMgr::setFeatureHelp(CvWStringBuffer &szBuffer, FeatureTypes eFeature, bool bCivilopediaText)
{
	if (eFeature == NO_FEATURE)
		return;

	CvFeatureInfo const& kFeature = GC.getInfo(eFeature);

	int aiYields[NUM_YIELD_TYPES];
	if (!bCivilopediaText)
	{
		szBuffer.append(kFeature.getDescription());

		for (int iI = 0; iI < NUM_YIELD_TYPES; ++iI)
		{
			aiYields[iI] = kFeature.getYieldChange(iI);
		}
		setYieldChangeHelp(szBuffer, L"", L"", L"", aiYields);
	}
	for (int iI = 0; iI < NUM_YIELD_TYPES; ++iI)
	{
		aiYields[iI] = kFeature.getRiverYieldChange(iI);
	}
	setYieldChangeHelp(szBuffer, L"", L"", gDLL->getText("TXT_KEY_TERRAIN_NEXT_TO_RIVER"), aiYields);

	for (int iI = 0; iI < NUM_YIELD_TYPES; ++iI)
	{
		aiYields[iI] = kFeature.getHillsYieldChange(iI);
	}
	setYieldChangeHelp(szBuffer, L"", L"", gDLL->getText("TXT_KEY_TERRAIN_ON_HILLS"), aiYields);

	if (kFeature.getMovementCost() != 1)
	{
		szBuffer.append(gDLL->getText("TXT_KEY_TERRAIN_MOVEMENT_COST", kFeature.getMovementCost()));
	}

	CvWString szHealth;
	szHealth.Format(L"%.2f", 0.01f * abs(kFeature.getHealthPercent()));
	if (kFeature.getHealthPercent() > 0)
	{
		szBuffer.append(gDLL->getText("TXT_KEY_FEATURE_GOOD_HEALTH", szHealth.GetCString()));
	}
	else if (kFeature.getHealthPercent() < 0)
	{
		szBuffer.append(gDLL->getText("TXT_KEY_FEATURE_BAD_HEALTH", szHealth.GetCString()));
	}

	if (kFeature.getDefenseModifier() != 0)
	{
		szBuffer.append(gDLL->getText("TXT_KEY_TERRAIN_DEFENSE_MODIFIER", kFeature.getDefenseModifier()));
	}
	// UNOFFICIAL_PATCH, Bugfix (FeatureDamageFix), 06/02/10, LunarMongoose: START
	if (kFeature.getTurnDamage() > 0)
	{
		szBuffer.append(gDLL->getText("TXT_KEY_TERRAIN_TURN_DAMAGE", kFeature.getTurnDamage()));
	}
	else if (kFeature.getTurnDamage() < 0)
	{
		szBuffer.append(gDLL->getText("TXT_KEY_TERRAIN_TURN_HEALING", -kFeature.getTurnDamage()));
	} // UNOFFICIAL_PATCH: END

	if (kFeature.isAddsFreshWater())
	{
		szBuffer.append(gDLL->getText("TXT_KEY_FEATURE_ADDS_FRESH_WATER"));
	}

	if (kFeature.isImpassable())
	{
		szBuffer.append(gDLL->getText("TXT_KEY_TERRAIN_IMPASSABLE"));
	}

    // doc: default impassable features
	if (eFeature == FEATURE_JUNGLE || eFeature == FEATURE_RAINFOREST || eFeature == FEATURE_MARSH)
	{
		szBuffer.append(gDLL->getText("TXT_KEY_TERRAIN_IMPASSABLE_MOST_UNITS"));
	}

	if (kFeature.isNoCity())
	{
		szBuffer.append(gDLL->getText("TXT_KEY_TERRAIN_NO_CITIES"));
	}

	if (kFeature.isNoImprovement())
	{
		szBuffer.append(gDLL->getText("TXT_KEY_FEATURE_NO_IMPROVEMENT"));
	}

}


void CvGameTextMgr::setTerrainHelp(CvWStringBuffer &szBuffer, TerrainTypes eTerrain, bool bCivilopediaText)
{
	if (eTerrain == NO_TERRAIN)
		return;

	CvTerrainInfo& kTerrain = GC.getInfo(eTerrain);

	int aiYields[NUM_YIELD_TYPES];
	if (!bCivilopediaText)
	{
		szBuffer.append(kTerrain.getDescription());

		for (int iI = 0; iI < NUM_YIELD_TYPES; ++iI)
		{
			aiYields[iI] = kTerrain.getYield(iI);
		}
		setYieldChangeHelp(szBuffer, L"", L"", L"", aiYields);
	}
	for (int iI = 0; iI < NUM_YIELD_TYPES; ++iI)
	{
		aiYields[iI] = kTerrain.getRiverYieldChange(iI);
	}
	setYieldChangeHelp(szBuffer, L"", L"",
			gDLL->getText("TXT_KEY_TERRAIN_NEXT_TO_RIVER"), aiYields);

	for (int iI = 0; iI < NUM_YIELD_TYPES; ++iI)
	{
		aiYields[iI] = kTerrain.getHillsYieldChange(iI);
	}
	setYieldChangeHelp(szBuffer, L"", L"",
			gDLL->getText("TXT_KEY_TERRAIN_ON_HILLS"), aiYields);

	if (kTerrain.getMovementCost() != 1)
	{
		szBuffer.append(gDLL->getText("TXT_KEY_TERRAIN_MOVEMENT_COST",
				kTerrain.getMovementCost()));
	}

	if (kTerrain.getBuildModifier() != 0)
	{
		szBuffer.append(gDLL->getText("TXT_KEY_TERRAIN_BUILD_MODIFIER",
				kTerrain.getBuildModifier()));
	}

	if (kTerrain.getDefenseModifier() != 0)
	{
		szBuffer.append(gDLL->getText("TXT_KEY_TERRAIN_DEFENSE_MODIFIER",
				kTerrain.getDefenseModifier()));
	}

	if (kTerrain.isImpassable())
	{
		szBuffer.append(gDLL->getText("TXT_KEY_TERRAIN_IMPASSABLE"));
	}
    // doc: default impassable terrain
	if (eTerrain == TERRAIN_DESERT || eTerrain == TERRAIN_TUNDRA || eTerrain == TERRAIN_SNOW)
	{
		szBuffer.append(gDLL->getText("TXT_KEY_TERRAIN_IMPASSABLE_MOST_UNITS"));
	}
	if (!kTerrain.isFound())
	{
		szBuffer.append(gDLL->getText("TXT_KEY_TERRAIN_NO_CITIES"));
		bool bFirst = true;
		if (kTerrain.isFoundCoast())
		{
			szBuffer.append(gDLL->getText("TXT_KEY_TERRAIN_COASTAL_CITIES"));
			bFirst = false;
		}
		if (!bFirst)
			szBuffer.append(gDLL->getText("TXT_KEY_OR"));
		if (kTerrain.isFoundFreshWater())
		{
			szBuffer.append(gDLL->getText("TXT_KEY_TERRAIN_FRESH_WATER_CITIES"));
			//bFirst = false;
		}
	}
}

void CvGameTextMgr::buildFinanceInflationString(CvWStringBuffer& szBuffer, PlayerTypes ePlayer)
{
	if (NO_PLAYER == ePlayer)
		return;
	CvPlayer& kPlayer = GET_PLAYER(ePlayer);

	int iInflationRate = kPlayer.calculateInflationRate();
	//if (iInflationRate != 0)
	{
		int iPreInflation = kPlayer.calculatePreInflatedCosts();
		CvWString szTmp; // advc.086: Get rid of newline set in XML
		szTmp.append(NEWLINE);
		szTmp.append(gDLL->getText("TXT_KEY_FINANCE_ADVISOR_INFLATION",
				iPreInflation, iInflationRate, iInflationRate, iPreInflation,
				iPreInflation * iInflationRate / 100));
		// <advc.086>
		if(szBuffer.isEmpty())
			szBuffer.assign(szTmp.substr(2, szTmp.length()));
		else szBuffer.append(szTmp); // </advc.086>
	}
}

void CvGameTextMgr::buildFinanceUnitCostString(CvWStringBuffer& szBuffer, PlayerTypes ePlayer)
{
	if (NO_PLAYER == ePlayer)
		return;
	CvPlayer const& kPlayer = GET_PLAYER(ePlayer);

	int iFreeUnits = 0;
	int iFreeMilitaryUnits = 0;
	int iUnits = kPlayer.getNumUnits();
	int iMilitaryUnits = kPlayer.getNumMilitaryUnits();
	int iPaidUnits = iUnits;
	int iPaidMilitaryUnits = iMilitaryUnits;
	int iMilitaryCost = 0;
	int iUnitCost = 0; // was called "base unit cost"
	int iExtraCost = 0;
	int iCost = kPlayer.calculateUnitCost(iFreeUnits, iFreeMilitaryUnits, iPaidUnits,
			iPaidMilitaryUnits, iUnitCost, iMilitaryCost, iExtraCost);
	int iHandicap = iCost-iUnitCost-iMilitaryCost-iExtraCost;

	// K-Mod include inflation
	int const iInflFactor = 100 + kPlayer.calculateInflationRate();
	{
		using namespace intdiv;
		iCost = round(iCost * iInflFactor, 100);
		iUnitCost = round(iUnitCost * iInflFactor, 100);
		iMilitaryCost = round(iMilitaryCost * iInflFactor, 100);
		iHandicap = round(iHandicap * iInflFactor, 100);
	}	// K-Mod end
	CvWString szTmp; // advc.086
	szTmp.append(NEWLINE);
	szTmp.append(gDLL->getText("TXT_KEY_FINANCE_ADVISOR_UNIT_COST",
			//iPaidUnits, iFreeUnits, iBaseUnitCost
			iUnits, iFreeUnits, iUnitCost)); // K-Mod
	// <advc.086>
	if(szBuffer.isEmpty())
		szBuffer.assign(szTmp.substr(2, szTmp.length()));
	else szBuffer.append(szTmp); // </advc.086>
	//if (iPaidMilitaryUnits != 0)
	if (iMilitaryCost != 0) // K-Mod
	{
		szBuffer.append(gDLL->getText("TXT_KEY_FINANCE_ADVISOR_UNIT_COST_2",
				//iPaidMilitaryUnits, iFreeMilitaryUnits, iMilitaryCost
				iMilitaryUnits, iFreeMilitaryUnits, iMilitaryCost)); // K-Mod
	}
	if (iExtraCost != 0)
		szBuffer.append(gDLL->getText("TXT_KEY_FINANCE_ADVISOR_UNIT_COST_3", iExtraCost));
	if (iHandicap != 0)
	{
		FErrorMsg("not all unit costs were accounted for"); // K-Mod (handicap modifier are now rolled into the other costs)
		szBuffer.append(gDLL->getText("TXT_KEY_FINANCE_ADVISOR_HANDICAP_COST", iHandicap));
		szBuffer.append(CvWString::format(L" (%+d%%)", GC.getInfo(kPlayer.getHandicapType()).getUnitCostPercent() - 100)); // K-Mod
	}
	szBuffer.append(gDLL->getText("TXT_KEY_FINANCE_ADVISOR_UNIT_COST_4", iCost));
}

void CvGameTextMgr::buildFinanceAwaySupplyString(CvWStringBuffer& szBuffer, PlayerTypes ePlayer)
{
	if (ePlayer == NO_PLAYER)
		return;
	CvPlayer const& kPlayer = GET_PLAYER(ePlayer);

	int iPaidUnits = 0;
	int iBaseCost = 0;
	int iCost = kPlayer.calculateUnitSupply(iPaidUnits, iBaseCost);
	int iHandicap = iCost - iBaseCost;
	// K-Mod include inflation
	int const iInflFactor = 100 + kPlayer.calculateInflationRate();
	iCost = intdiv::round(iCost * iInflFactor, 100);
	iBaseCost = intdiv::round(iBaseCost * iInflFactor, 100);
	iHandicap = intdiv::round(iHandicap * iInflFactor, 100);
	// K-Mod end

	CvWString szHandicap;
	if (iHandicap != 0)
	{	// K-Mod (handicap modifiers are now rolled into the other costs)
		FAssertMsg(
			!kPlayer.isHuman(), // advc.001d
			"not all supply costs were accounted for");
		szHandicap = gDLL->getText("TXT_KEY_FINANCE_ADVISOR_HANDICAP_COST", iHandicap);
	}
	CvWString szTmp; // advc.086
	szTmp.append(NEWLINE);
	szTmp.append(gDLL->getText("TXT_KEY_FINANCE_ADVISOR_SUPPLY_COST",
			//iPaidUnits, GC.getDefineINT("INITIAL_FREE_OUTSIDE_UNITS"),
			// K-Mod:
			kPlayer.getNumOutsideUnits(), kPlayer.getNumOutsideUnits() - iPaidUnits,
			iBaseCost, szHandicap.GetCString(), iCost));
	// <advc.086>
	if(szBuffer.isEmpty())
		szBuffer.assign(szTmp.substr(2, szTmp.length()));
	else szBuffer.append(szTmp); // </advc.086>
}

void CvGameTextMgr::buildFinanceCityMaintString(CvWStringBuffer& szBuffer, PlayerTypes ePlayer)
{
	if (NO_PLAYER == ePlayer)
		return;

	/*	advc: Improve precision a bit. (Rules-wise, costs get rounded down -
		but only after adding all components up. Don't want to round down in
		the breakdown, and K-Mod had already been using ROUND_DIVIDE.) */
	scaled rDistanceMaint;
	scaled rColonyMaint;
	scaled rCorpMaint;
	CvPlayer const& kPlayer = GET_PLAYER(ePlayer);
	FOR_EACH_CITY(pCity, kPlayer)
	{
		if (!pCity->isNoMaintenance()) // K-Mod, 06/sep/10 (bugfix)
		{
			rDistanceMaint += per100(pCity->calculateDistanceMaintenanceTimes100()) *
					per100(std::max(0, pCity->getMaintenanceModifier() + 100));
			rColonyMaint += per100(pCity->calculateColonyMaintenanceTimes100()) *
					per100(std::max(0, pCity->getMaintenanceModifier() + 100));
			rCorpMaint += per100(pCity->calculateCorporationMaintenanceTimes100()) *
					per100(std::max(0, pCity->getMaintenanceModifier() + 100));
		}
	}
	// K-Mod. Changed to include the effects of inflation.
	int const iInflationFactorTimes100 = kPlayer.calculateInflationRate() + 100;
	scaled const rInflationFactor = per100(iInflationFactorTimes100);

	rDistanceMaint *= rInflationFactor;
	rColonyMaint *= rInflationFactor;
	rCorpMaint *= rInflationFactor;
	/*	Note: currently, calculateCorporationMaintenanceTimes100
		includes the inverse of this factor. */

	int iDistanceMaint = rDistanceMaint.round();
	int iColonyMaint = rColonyMaint.round();
	int iCorpMaint = rCorpMaint.round();

	int iNumCityMaint = (kPlayer.getTotalMaintenance() * rInflationFactor).round() -
			iDistanceMaint - iColonyMaint - iCorpMaint;
	CvWString szTmp; // advc.086
	szTmp.append(NEWLINE);
	szTmp.append(gDLL->getText("TXT_KEY_FINANCE_ADVISOR_CITY_MAINT_COST",
			iDistanceMaint, iNumCityMaint, iColonyMaint, iCorpMaint,
			(kPlayer.getTotalMaintenance() * iInflationFactorTimes100) / 100));
	// <advc.086>
	if(szBuffer.isEmpty())
		szBuffer.assign(szTmp.substr(2, szTmp.length()));
	else szBuffer.append(szTmp); // </advc.086>

}

void CvGameTextMgr::buildFinanceCivicUpkeepString(CvWStringBuffer& szBuffer, PlayerTypes ePlayer)
{
	if (ePlayer == NO_PLAYER)
		return;
	CvPlayer const& kPlayer = GET_PLAYER(ePlayer);
	CvWString szCivicOptionCosts;

	int iInflFactor = 100 + kPlayer.calculateInflationRate();

	FOR_EACH_ENUM(CivicOption)
	{
		CivicTypes eCivic = kPlayer.getCivics(eLoopCivicOption);
		if (NO_CIVIC != eCivic)
		{
			CvWString szTemp;
			szTemp.Format(L"%d%c: %s",
					// K-Mod:
					intdiv::round(kPlayer.getSingleCivicUpkeep(eCivic) * iInflFactor, 100),
					GC.getInfo(COMMERCE_GOLD).getChar(), GC.getInfo(eCivic).getDescription());
			szCivicOptionCosts += NEWLINE + szTemp;
		}
	}
	CvWString szTmp; // advc.086
	szTmp.append(NEWLINE);
	szTmp.append(gDLL->getText("TXT_KEY_FINANCE_ADVISOR_CIVIC_UPKEEP_COST",
			szCivicOptionCosts.GetCString(),
			//player.getCivicUpkeep()));
			intdiv::round(kPlayer.getCivicUpkeep() * iInflFactor, 100))); // K-Mod
	// <advc.086>
	if(szBuffer.isEmpty())
		szBuffer.assign(szTmp.substr(2, szTmp.length()));
	else szBuffer.append(szTmp); // </advc.086>
}

void CvGameTextMgr::buildFinanceForeignIncomeString(CvWStringBuffer& szBuffer, PlayerTypes ePlayer)
{
	if (NO_PLAYER == ePlayer)
		return;
	CvPlayer const& kPlayer = GET_PLAYER(ePlayer);

	CvWString szPlayerIncome;
	for (PlayerIter<CIV_ALIVE> it; it.hasNext(); ++it)
	{
		CvPlayer const& kOtherPlayer = *it;
		if (kPlayer.getGoldPerTurnByPlayer(kOtherPlayer.getID()) != 0)
		{
			CvWString szTemp;
			szTemp.Format(L"%d%c: %s", kPlayer.getGoldPerTurnByPlayer(
					kOtherPlayer.getID()), GC.getInfo(COMMERCE_GOLD).getChar(),
					kOtherPlayer.getCivilizationShortDescription());
			szPlayerIncome += NEWLINE + szTemp;
		}
	}
	if (!szPlayerIncome.empty())
	{
		CvWString szTmp; // advc.086
		szTmp.append(NEWLINE);
		szTmp.append(gDLL->getText("TXT_KEY_FINANCE_ADVISOR_FOREIGN_INCOME",
				szPlayerIncome.GetCString(), kPlayer.getGoldPerTurn()));
		// <advc.086>
		if(szBuffer.isEmpty())
			szBuffer.assign(szTmp.substr(2, szTmp.length()));
		else szBuffer.append(szTmp); // </advc.086>
	}
}

// doc: stability display
void CvGameTextMgr::buildStabilityString(CvWStringBuffer& szBuffer, int iStabilityChange)
{
	CvWString szStability;
	CvWString szTemp;

	if (iStabilityChange < 0)
	{
		szTemp.Format(SETCOLR, TEXT_COLOR("COLOR_RED"));
		szStability += szTemp;

		szTemp.Format(gDLL->getText("TXT_KEY_STABILITY_CHANGE_NEGATIVE"));
		szStability += szTemp;

		szTemp.Format(ENDCOLR);
		szStability += szTemp;
	}
	else if (iStabilityChange > 0)
	{
		szTemp.Format(gDLL->getText("TXT_KEY_STABILITY_CHANGE_POSITIVE"));
		szStability += szTemp;
	}
	else
	{
		szTemp.Format(gDLL->getText("TXT_KEY_STABILITY_NO_CHANGE"));
		szStability += szTemp;
	}

	szBuffer.append(szStability.GetCString());
}

// doc: stability display
void CvGameTextMgr::buildStabilityParameterString(CvWStringBuffer& szBuffer, int iStabilityCategory)
{
	CvWString szStabilityParameters;
	CvWString szStabilityType;
	CvWString szColor;
	CvPlayer& player = GET_PLAYER(GC.getGameINLINE().getActivePlayer());
	int iTotalStability = 0;

	// Expansion
	if (iStabilityCategory == 0)
	{
		int iParameterCorePeriphery = player.getStabilityParameter(PARAMETER_CORE_PERIPHERY);
		int iParameterAdministration = player.getStabilityParameter(PARAMETER_ADMINISTRATION);
		int iParameterSeparatism = player.getStabilityParameter(PARAMETER_SEPARATISM);
		int iParameterRecentExpansion = player.getStabilityParameter(PARAMETER_RECENT_EXPANSION);
		int iParameterRazedCities = player.getStabilityParameter(PARAMETER_RAZED_CITIES);
		int iParameterIsolationism = player.getStabilityParameter(PARAMETER_ISOLATIONISM);

		iTotalStability = iParameterCorePeriphery + iParameterRecentExpansion;

		szStabilityType = gDLL->getText("TXT_KEY_STABILITY_CATEGORY_EXPANSION");

		szColor.Format(SETCOLR, TEXT_COLOR("COLOR_GREEN"));
		szStabilityParameters += szColor;

		if (iParameterRecentExpansion > 0)
		{
			CvWString szTemp;
			szTemp.Format(L"+%d: %s", iParameterRecentExpansion, gDLL->getText("TXT_KEY_STABILITY_RECENT_EXPANSION").GetCString());
			szStabilityParameters += NEWLINE + szTemp;
		}

		if (iParameterIsolationism > 0)
		{
			CvWString szTemp;
			szTemp.Format(L"+%d: %s", iParameterIsolationism, gDLL->getText("TXT_KEY_STABILITY_ISOLATIONISM").GetCString());
			szStabilityParameters += NEWLINE + szTemp;
		}

		if (iParameterCorePeriphery >= 0)
		{
			CvWString szTemp;
			szTemp.Format(L"%s: %d / %d", gDLL->getText("TXT_KEY_STABILITY_CORE_PERIPHERY_INFO").GetCString(), iParameterSeparatism, iParameterAdministration);
			//szTemp.Format(L"+%d: %s (%d / %d)", iParameterCorePeriphery, gDLL->getText("TXT_KEY_STABILITY_CORE_PERIPHERY_POSITIVE").GetCString(), iParameterPeripheryScore, iParameterCoreScore);
			szStabilityParameters += NEWLINE + szTemp;
		}

		szColor.Format(ENDCOLR SETCOLR, TEXT_COLOR("COLOR_RED"));
		szStabilityParameters += szColor;

		if (iParameterCorePeriphery < 0)
		{
			CvWString szTemp;
			szTemp.Format(L"%d: %s (%d / %d)", iParameterCorePeriphery, gDLL->getText("TXT_KEY_STABILITY_CORE_PERIPHERY_NEGATIVE").GetCString(), iParameterSeparatism, iParameterAdministration);
			szStabilityParameters += NEWLINE + szTemp;
		}

		if (iParameterRazedCities < 0)
		{
			CvWString szTemp;
			szTemp.Format(L"%d: %s", iParameterRazedCities, gDLL->getText("TXT_KEY_STABILITY_RAZED_CITIES").GetCString());
			szStabilityParameters += NEWLINE + szTemp;
		}

		szColor.Format(ENDCOLR);
		szStabilityParameters += szColor;
	}

	// Economy
	else if (iStabilityCategory == 1)
	{
		int iParameterEconomicGrowth = player.getStabilityParameter(PARAMETER_ECONOMIC_GROWTH);
		int iParameterTrade = player.getStabilityParameter(PARAMETER_TRADE);
		int iParameterMercantilism = player.getStabilityParameter(PARAMETER_MERCANTILISM);
		int iParameterCentralPlanning = player.getStabilityParameter(PARAMETER_CENTRAL_PLANNING);

		iTotalStability = iParameterEconomicGrowth + iParameterTrade + iParameterMercantilism + iParameterCentralPlanning;

		szStabilityType = gDLL->getText("TXT_KEY_STABILITY_CATEGORY_ECONOMY");

		szColor.Format(SETCOLR, TEXT_COLOR("COLOR_GREEN"));
		szStabilityParameters += szColor;

		if (iParameterEconomicGrowth > 0)
		{
			CvWString szTemp;
			szTemp.Format(L"+%d: %s", iParameterEconomicGrowth, gDLL->getText("TXT_KEY_STABILITY_ECONOMIC_GROWTH").GetCString());
			szStabilityParameters += NEWLINE + szTemp;
		}

		if (iParameterTrade > 0)
		{
			CvWString szTemp;
			szTemp.Format(L"+%d: %s", iParameterTrade, gDLL->getText("TXT_KEY_STABILITY_TRADE").GetCString());
			szStabilityParameters += NEWLINE + szTemp;
		}

		szColor.Format(SETCOLR, TEXT_COLOR("COLOR_RED"));
		szStabilityParameters += szColor;

		if (iParameterEconomicGrowth < 0)
		{
			CvWString szTemp;
			szTemp.Format(L"%d: %s", iParameterEconomicGrowth, gDLL->getText("TXT_KEY_STABILITY_ECONOMIC_DECLINE").GetCString());
			szStabilityParameters += NEWLINE + szTemp;
		}

		if (iParameterTrade < 0)
		{
			CvWString szTemp;
			szTemp.Format(L"%d: %s", iParameterTrade, gDLL->getText("TXT_KEY_STABILITY_INSUFFICIENT_TRADE").GetCString());
			szStabilityParameters += NEWLINE + szTemp;
		}

		/*if (iParameterEconomicGrowth != 0 && iParameterPercentChange > iParameterBaselinePercent)
		{
			CvWString szTemp;
			szTemp.Format(L"+%d: %s (%d / %d)", iParameterEconomicGrowth, gDLL->getText("TXT_KEY_STABILITY_ECONOMIC_GROWTH").GetCString(), iParameterPercentChange, iParameterBaselinePercent);
			szStabilityParameters += NEWLINE + szTemp;
		}

		szColor.Format(ENDCOLR SETCOLR, TEXT_COLOR("COLOR_RED"));
		szStabilityParameters += szColor;

		if (iParameterEconomicGrowth != 0 && iParameterPercentChange <= iParameterBaselinePercent)
		{
			if (iParameterPercentChange >= 0)
			{
				CvWString szTemp;
				szTemp.Format(L"%d: %s (%d / %d)", iParameterEconomicGrowth, gDLL->getText("TXT_KEY_STABILITY_ECONOMIC_STAGNATION").GetCString(), iParameterPercentChange, iParameterBaselinePercent);
				szStabilityParameters += NEWLINE + szTemp;
			}
			else
			{
				CvWString szTemp;
				szTemp.Format(L"%d: %s (%d / %d)", iParameterEconomicGrowth, gDLL->getText("TXT_KEY_STABILITY_ECONOMIC_DECLINE").GetCString(), iParameterPercentChange, iParameterBaselinePercent);
				szStabilityParameters += NEWLINE + szTemp;
			}
		}*/

		if (iParameterMercantilism < 0)
		{
			CvWString szTemp;
			szTemp.Format(L"%d: %s", iParameterMercantilism, gDLL->getText("TXT_KEY_STABILITY_MERCANTILISM_TRADE_RICHER").GetCString());
			szStabilityParameters += NEWLINE + szTemp;
		}

		if (iParameterCentralPlanning < 0)
		{
			CvWString szTemp;
			szTemp.Format(L"%d: %s", iParameterCentralPlanning, gDLL->getText("TXT_KEY_STABILITY_CENTRAL_PLANNING_TRADE_FREE_MARKET").GetCString());
			szStabilityParameters += NEWLINE + szTemp;
		}

		szColor.Format(ENDCOLR);
		szStabilityParameters += szColor;
	}

	// Domestic
	else if (iStabilityCategory == 2)
	{
		int iParameterHappiness = player.getStabilityParameter(PARAMETER_HAPPINESS);
		int iParameterCivicCombinations = player.getStabilityParameter(PARAMETER_CIVIC_COMBINATIONS);
		int iParameterCivicsEraTech = player.getStabilityParameter(PARAMETER_CIVICS_ERA_TECH);
		int iParameterReligion = player.getStabilityParameter(PARAMETER_RELIGION);

		iTotalStability = iParameterHappiness + iParameterCivicCombinations + iParameterCivicsEraTech + iParameterReligion;

		szStabilityType = gDLL->getText("TXT_KEY_STABILITY_CATEGORY_DOMESTIC");

		szColor.Format(SETCOLR, TEXT_COLOR("COLOR_GREEN"));
		szStabilityParameters += szColor;

		if (iParameterHappiness > 0)
		{
			CvWString szTemp;
			szTemp.Format(L"+%d: %s", iParameterHappiness, gDLL->getText("TXT_KEY_STABILITY_HAPPINESS").GetCString());
			szStabilityParameters += NEWLINE + szTemp;
		}

		if (iParameterCivicCombinations > 0)
		{
			CvWString szTemp;
			szTemp.Format(L"+%d: %s", iParameterCivicCombinations, gDLL->getText("TXT_KEY_STABILITY_COMPATIBLE_CIVICS").GetCString());
			szStabilityParameters += NEWLINE + szTemp;
		}

		if (iParameterCivicsEraTech > 0)
		{
			CvWString szTemp;
			szTemp.Format(L"+%d: %s", iParameterCivicsEraTech, gDLL->getText("TXT_KEY_STABILITY_CONTEMPORARY_CIVICS").GetCString());
			szStabilityParameters += NEWLINE + szTemp;
		}

		if (iParameterReligion > 0)
		{
			CvWString szTemp;
			szTemp.Format(L"+%d: %s", iParameterReligion, gDLL->getText("TXT_KEY_STABILITY_RELIGIOUS_UNITY").GetCString());
			szStabilityParameters += NEWLINE + szTemp;
		}

		szColor.Format(ENDCOLR SETCOLR, TEXT_COLOR("COLOR_RED"));
		szStabilityParameters += szColor;

		if (iParameterHappiness < 0)
		{
			CvWString szTemp;
			szTemp.Format(L"%d: %s", iParameterHappiness, gDLL->getText("TXT_KEY_STABILITY_UNHAPPINESS").GetCString());
			szStabilityParameters += NEWLINE + szTemp;
		}

		if (iParameterCivicCombinations < 0)
		{
			CvWString szTemp;
			szTemp.Format(L"%d: %s", iParameterCivicCombinations, gDLL->getText("TXT_KEY_STABILITY_INCOMPATIBLE_CIVICS").GetCString());
			szStabilityParameters += NEWLINE + szTemp;
		}

		if (iParameterCivicsEraTech < 0)
		{
			CvWString szTemp;
			szTemp.Format(L"%d: %s", iParameterCivicsEraTech, gDLL->getText("TXT_KEY_STABILITY_OUTDATED_CIVICS").GetCString());
			szStabilityParameters += NEWLINE + szTemp;
		}

		if (iParameterReligion < 0)
		{
			CvWString szTemp;
			szTemp.Format(L"%d: %s", iParameterReligion, gDLL->getText("TXT_KEY_STABILITY_RELIGIOUS_DISUNITY").GetCString());
			szStabilityParameters += NEWLINE + szTemp;
		}

		szColor.Format(ENDCOLR);
		szStabilityParameters += szColor;
	}

	// Foreign
	else if (iStabilityCategory == 3)
	{
		int iParameterVassals = player.getStabilityParameter(PARAMETER_VASSALS);
		int iParameterDefensivePacts = player.getStabilityParameter(PARAMETER_DEFENSIVE_PACTS);
		int iParameterRelations = player.getStabilityParameter(PARAMETER_RELATIONS);
		int iParameterNationhood = player.getStabilityParameter(PARAMETER_NATIONHOOD);
		int iParameterFanaticism = player.getStabilityParameter(PARAMETER_FANATICISM);
		int iParameterMultilateralism = player.getStabilityParameter(PARAMETER_MULTILATERALISM);

		iTotalStability = iParameterVassals + iParameterDefensivePacts + iParameterRelations + iParameterNationhood + iParameterFanaticism + iParameterMultilateralism;

		szStabilityType = gDLL->getText("TXT_KEY_STABILITY_CATEGORY_FOREIGN");

		szColor.Format(SETCOLR, TEXT_COLOR("COLOR_GREEN"));
		szStabilityParameters += szColor;

		if (iParameterVassals > 0)
		{
			CvWString szTemp;
			szTemp.Format(L"+%d: %s", iParameterVassals, gDLL->getText("TXT_KEY_STABILITY_STABLE_VASSALS").GetCString());
			szStabilityParameters += NEWLINE + szTemp;
		}

		if (iParameterRelations > 0)
		{
			CvWString szTemp;
			szTemp.Format(L"+%d: %s", iParameterRelations, gDLL->getText("TXT_KEY_STABILITY_GOOD_RELATIONS").GetCString());
			szStabilityParameters += NEWLINE + szTemp;
		}

		if (iParameterDefensivePacts > 0)
		{
			CvWString szTemp;
			szTemp.Format(L"+%d: %s", iParameterDefensivePacts, gDLL->getText("TXT_KEY_STABILITY_DEFENSIVE_PACTS").GetCString());
			szStabilityParameters += NEWLINE + szTemp;
		}

		if (iParameterNationhood > 0)
		{
			CvWString szTemp;
			szTemp.Format(L"+%d: %s", iParameterNationhood, gDLL->getText("TXT_KEY_STABILITY_WARS_NATIONHOOD").GetCString());
			szStabilityParameters += NEWLINE + szTemp;
		}

		if (iParameterFanaticism > 0)
		{
			CvWString szTemp;
			szTemp.Format(L"+%d: %s", iParameterFanaticism, gDLL->getText("TXT_KEY_STABILITY_WARS_HEATHENS").GetCString());
			szStabilityParameters += NEWLINE + szTemp;
		}

		szColor.Format(ENDCOLR SETCOLR, TEXT_COLOR("COLOR_RED"));
		szStabilityParameters += szColor;

		if (iParameterVassals < 0)
		{
			CvWString szTemp;
			szTemp.Format(L"%d: %s", iParameterVassals, gDLL->getText("TXT_KEY_STABILITY_UNSTABLE_VASSALS").GetCString());
			szStabilityParameters += NEWLINE + szTemp;
		}

		if (iParameterRelations < 0)
		{
			CvWString szTemp;
			szTemp.Format(L"%d: %s", iParameterRelations, gDLL->getText("TXT_KEY_STABILITY_BAD_RELATIONS").GetCString());
			szStabilityParameters += NEWLINE + szTemp;
		}

		if (iParameterFanaticism < 0)
		{
			CvWString szTemp;
			szTemp.Format(L"%d: %s", iParameterFanaticism, gDLL->getText("TXT_KEY_STABILITY_WARS_BROTHERS_OF_FAITH").GetCString());
			szStabilityParameters += NEWLINE + szTemp;
		}

		if (iParameterMultilateralism < 0)
		{
			CvWString szTemp;
			szTemp.Format(L"%d: %s", iParameterMultilateralism, gDLL->getText("TXT_KEY_STABILITY_WARS_MULTILATERALISM").GetCString());
			szStabilityParameters += NEWLINE + szTemp;
		}

		szColor.Format(ENDCOLR);
		szStabilityParameters += szColor;
	}

	// Military
	else if (iStabilityCategory == 4)
	{
		int iParameterWarSuccess = player.getStabilityParameter(PARAMETER_WAR_SUCCESS);
		int iParameterWarWeariness = player.getStabilityParameter(PARAMETER_WAR_WEARINESS);
		int iParameterBarbarianLosses = player.getStabilityParameter(PARAMETER_BARBARIAN_LOSSES);

		iTotalStability = iParameterWarSuccess + iParameterWarWeariness + iParameterBarbarianLosses;

		szStabilityType = gDLL->getText("TXT_KEY_STABILITY_CATEGORY_MILITARY");

		szColor.Format(SETCOLR, TEXT_COLOR("COLOR_GREEN"));
		szStabilityParameters += szColor;

		if (iParameterWarSuccess > 0)
		{
			CvWString szTemp;
			szTemp.Format(L"+%d: %s", iParameterWarSuccess, gDLL->getText("TXT_KEY_STABILITY_WINNING_WARS").GetCString());
			szStabilityParameters += NEWLINE + szTemp;
		}

		szColor.Format(ENDCOLR SETCOLR, TEXT_COLOR("COLOR_RED"));
		szStabilityParameters += szColor;

		if (iParameterWarSuccess < 0)
		{
			CvWString szTemp;
			szTemp.Format(L"%d: %s", iParameterWarSuccess, gDLL->getText("TXT_KEY_STABILITY_LOSING_WARS").GetCString());
			szStabilityParameters += NEWLINE + szTemp;
		}

		if (iParameterWarWeariness < 0)
		{
			CvWString szTemp;
			szTemp.Format(L"%d: %s", iParameterWarWeariness, gDLL->getText("TXT_KEY_STABILITY_WAR_WEARINESS").GetCString());
			szStabilityParameters += NEWLINE + szTemp;
		}

		if (iParameterBarbarianLosses < 0)
		{
			CvWString szTemp;
			szTemp.Format(L"%d: %s", iParameterBarbarianLosses, gDLL->getText("TXT_KEY_STABILITY_BARBARIAN_LOSSES").GetCString());
			szStabilityParameters += NEWLINE + szTemp;
		}

		szColor.Format(ENDCOLR);
		szStabilityParameters += szColor;
	}

	szBuffer.append(gDLL->getText("TXT_KEY_FINANCE_ADVISOR_STABILITY_HEAD", szStabilityType.GetCString()));

	szBuffer.append(NEWLINE);
	szBuffer.append(gDLL->getText("TXT_KEY_FINANCE_ADVISOR_STABILITY", szStabilityParameters.GetCString(), szStabilityType.GetCString(), (iTotalStability > 0 ? "+" : ""), iTotalStability));
}

// BUG - Building Additional Yield - start
bool CvGameTextMgr::setBuildingAdditionalYieldHelp(CvWStringBuffer &szBuffer, const CvCity& kCity, YieldTypes eIndex, const CvWString& szStart, bool bStarted)
{
	CvYieldInfo& info = GC.getInfo(eIndex);
	CvWString szLabel;

	CvCivilization const& kCiv = kCity.getCivilization(); // advc.003w
	for (int i = 0; i < kCiv.getNumBuildings(); i++)
	{
		BuildingTypes eBuilding = kCiv.buildingAt(i);
		if (kCity.canConstruct(eBuilding, false, true, false))
		{
			int iChange = kCity.getAdditionalYieldByBuilding(eIndex, eBuilding);
			if (iChange != 0)
			{
				if (!bStarted)
				{
					szBuffer.append(szStart);
					bStarted = true;
				}

				szLabel.Format(SETCOLR L"%s" ENDCOLR, TEXT_COLOR("COLOR_BUILDING_TEXT"), GC.getInfo(eBuilding).getDescription());
				setValueChangeHelp(szBuffer, szLabel, L": ", L"", iChange, info.getChar(), false, true);
			}
		}
	}

	return bStarted;
} // BUG - Building Additional Yield - end

// BUG - Building Additional Commerce - start
bool CvGameTextMgr::setBuildingAdditionalCommerceHelp(CvWStringBuffer &szBuffer, const CvCity& kCity, CommerceTypes eIndex, const CvWString& szStart, bool bStarted)
{
	CvCommerceInfo& info = GC.getInfo(eIndex);
	CvWString szLabel;

	CvCivilization const& kCiv = kCity.getCivilization(); // advc.003w
	for (int i = 0; i < kCiv.getNumBuildings(); i++)
	{
		BuildingTypes eBuilding = kCiv.buildingAt(i);
		if (kCity.canConstruct(eBuilding, false, true, false))
		{
			int iChange = kCity.getAdditionalCommerceTimes100ByBuilding(eIndex, eBuilding);
			if (iChange != 0)
			{
				if (!bStarted)
				{
					szBuffer.append(szStart);
					bStarted = true;
				}

				szLabel.Format(SETCOLR L"%s" ENDCOLR, TEXT_COLOR("COLOR_BUILDING_TEXT"), GC.getInfo(eBuilding).getDescription());
				setValueTimes100ChangeHelp(szBuffer, szLabel, L": ", L"", iChange, info.getChar(), true);
			}
		}
	}

	return bStarted;
} // BUG - Building Additional Commerce - end

// BUG - Building Saved Maintenance - start
bool CvGameTextMgr::setBuildingSavedMaintenanceHelp(CvWStringBuffer &szBuffer, const CvCity& kCity, const CvWString& szStart, bool bStarted)
{
	CvCommerceInfo& info = GC.getInfo(COMMERCE_GOLD);
	CvWString szLabel;

	CvCivilization const& kCiv = kCity.getCivilization(); // advc.003w
	for (int i = 0; i < kCiv.getNumBuildings(); i++)
	{
		BuildingTypes eBuilding = kCiv.buildingAt(i);
		if (kCity.canConstruct(eBuilding, false, true, false))
		{
			int iChange = kCity.getSavedMaintenanceTimes100ByBuilding(eBuilding);

			if (iChange != 0)
			{
				if (!bStarted)
				{
					szBuffer.append(szStart);
					bStarted = true;
				}

				szLabel.Format(SETCOLR L"%s" ENDCOLR, TEXT_COLOR("COLOR_BUILDING_TEXT"), GC.getInfo(eBuilding).getDescription());
				setValueTimes100ChangeHelp(szBuffer, szLabel, L": ", L"", iChange, info.getChar(), true);
			}
		}
	}

	return bStarted;
} // BUG - Building Saved Maintenance - end


void CvGameTextMgr::setProductionHelp(CvWStringBuffer &szBuffer, CvCity const& kCity)
{
	bool bProcess = kCity.isProductionProcess();
	// advc.064b: To be displayed at the end; iPastOverflow also moved.
	int iFromChopsUnused = kCity.getFeatureProduction();
	// <advc.064b>
	int iFromChops = 0;
	kCity.getCurrentProductionDifference(false, !bProcess, false, false, false, &iFromChops);
	if(!kCity.isProduction())
		iFromChops = iFromChopsUnused;
	iFromChopsUnused -= iFromChops; // </advc.064b>
	if (iFromChops != 0)
	{
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_PROD_CHOPS", iFromChops));
		szBuffer.append(NEWLINE);
	}

	//if (kCity.getCurrentProductionDifference(false, true) == 0)
	// BUG - Building Additional Production - start
	bool bBuildingAdditionalYield = (BUGOption::isEnabled("MiscHover__BuildingAdditionalProduction", false) ||
			GC.altKey()); // advc.063
	if (kCity.getCurrentProductionDifference(false, true) == 0 && !bBuildingAdditionalYield)
	// BUG - Building Additional Production - end
	{
		return;
	}

	setYieldHelp(szBuffer, kCity, YIELD_PRODUCTION);

	/*  advc.064b: Moved down b/c the generic bonuses in setYieldHelp no longer
		apply to iPastOverflow */
	int iPastOverflow = kCity.getOverflowProduction();
	if (iPastOverflow != 0 && !bProcess) // advc.064b: Display it later if bProcess
	{
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_PROD_OVERFLOW", iPastOverflow));
		szBuffer.append(NEWLINE);
	}
	// advc.064b: Don't add iOverflow yet
	int iBaseProduction = kCity.getBaseYieldRate(YIELD_PRODUCTION) + iFromChops;
	/*  advc (note): This is the sum of all modifiers that apply to iBaseProduction
		(not to food production) */
	int iBaseModifier = kCity.getBaseYieldRateModifier(YIELD_PRODUCTION);

	CvPlayer const& kOwner = GET_PLAYER(kCity.getOwner());
	ReligionTypes const eStateReligion = kOwner.getStateReligion();
	UnitTypes eUnit = kCity.getProductionUnit();
	if (eUnit != NO_UNIT)
	{
		CvUnitInfo const& kUnit = GC.getInfo(eUnit);

		DomainTypes eDomain = kUnit.getDomainType();
		int iDomainMod = kCity.getDomainProductionModifier(eDomain);
		if (iDomainMod != 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_PROD_DOMAIN",
					iDomainMod, GC.getInfo(eDomain).getTextKeyWide()));
			szBuffer.append(NEWLINE);
			iBaseModifier += iDomainMod;
		}

		if (kUnit.isMilitaryProduction())
		{
			int iMilitaryMod = kCity.getMilitaryProductionModifier() +
					kOwner.getMilitaryProductionModifier();
			if (iMilitaryMod != 0)
			{
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_PROD_MILITARY", iMilitaryMod));
				szBuffer.append(NEWLINE);
				iBaseModifier += iMilitaryMod;
			}
		}

		FOR_EACH_ENUM(Bonus)
		{
			if (!kCity.hasBonus(eLoopBonus))
				continue;
			int iBonusMod = kUnit.getBonusProductionModifier(eLoopBonus);
			if (iBonusMod != 0)
			{
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_PROD_MOD_BONUS", iBonusMod,
						kUnit.getTextKeyWide(), GC.getInfo(eLoopBonus).getTextKeyWide()));
				szBuffer.append(NEWLINE);
				iBaseModifier += iBonusMod;
			}
		}

		FOR_EACH_ENUM(Trait)
		{
			if (!kCity.hasTrait(eLoopTrait))
				continue;
			int iTraitMod = kUnit.getProductionTraits(eLoopTrait);
			if (kUnit.getSpecialUnitType() != NO_SPECIALUNIT)
			{
				iTraitMod += GC.getInfo(kUnit.getSpecialUnitType()).
						getProductionTraits(eLoopTrait);
			}
			if (iTraitMod != 0)
			{
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_PROD_TRAIT", iTraitMod,
						kUnit.getTextKeyWide(), GC.getInfo(eLoopTrait).getTextKeyWide()));
				szBuffer.append(NEWLINE);
				iBaseModifier += iTraitMod;
			}
		}

		if (eStateReligion != NO_RELIGION && kCity.isHasReligion(eStateReligion))
		{
			int iReligionMod = kOwner.getStateReligionUnitProductionModifier();
			if (iReligionMod != 0)
			{
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_PROD_RELIGION", iReligionMod,
						GC.getInfo(eStateReligion).getTextKeyWide()));
				szBuffer.append(NEWLINE);
				iBaseModifier += iReligionMod;
			}
		}
	}

	BuildingTypes eBuilding = kCity.getProductionBuilding();
	if (eBuilding != NO_BUILDING)
	{
		CvBuildingInfo const& kBuilding = GC.getInfo(eBuilding);
		FOR_EACH_ENUM(Bonus)
		{
			if (!kCity.hasBonus(eLoopBonus))
				continue;
			int iBonusMod = kBuilding.getBonusProductionModifier(eLoopBonus);
			if (iBonusMod != 0)
			{
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_PROD_MOD_BONUS", iBonusMod,
						kBuilding.getTextKeyWide(), GC.getInfo(eLoopBonus).getTextKeyWide()));
				szBuffer.append(NEWLINE);
				iBaseModifier += iBonusMod;
			}
		}

		FOR_EACH_ENUM(Trait)
		{
			if (!kCity.hasTrait(eLoopTrait))
				continue;
			int iTraitMod = kBuilding.getProductionTraits(eLoopTrait);
			if (kBuilding.getSpecialBuildingType() != NO_SPECIALBUILDING)
			{
				iTraitMod += GC.getInfo(kBuilding.getSpecialBuildingType()).
						getProductionTraits(eLoopTrait);
			}
			if (iTraitMod != 0)
			{
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_PROD_TRAIT", iTraitMod,
						kBuilding.getTextKeyWide(), GC.getInfo(eLoopTrait).getTextKeyWide()));
				szBuffer.append(NEWLINE);
				iBaseModifier += iTraitMod;
			}
		}

        // doc: civic modifier
        int iCivicMod = kOwner.getBuildingProductionModifier(eBuilding);
        if (iCivicMod != 0)
        {
            szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_PROD_CIVIC",
                    iCivicMod,
                    building.getTextKeyWide()));
            szBuffer.append(NEWLINE);
            iBaseModifier += iCivicMod;
        }

		if (kBuilding.isWorldWonder())
		{
			int iWonderMod = kOwner.getMaxGlobalBuildingProductionModifier();
			if (iWonderMod != 0)
			{
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_PROD_WONDER", iWonderMod));
				szBuffer.append(NEWLINE);
				iBaseModifier += iWonderMod;
			}
		}

		if (kBuilding.isTeamWonder())
		{
			int iWonderMod = kOwner.getMaxTeamBuildingProductionModifier();
			if (iWonderMod != 0)
			{
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_PROD_TEAM_WONDER", iWonderMod));
				szBuffer.append(NEWLINE);
				iBaseModifier += iWonderMod;
			}
		}

		if (kBuilding.isNationalWonder())
		{
			int iWonderMod = kOwner.getMaxPlayerBuildingProductionModifier();
			if (iWonderMod != 0)
			{
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_PROD_NATIONAL_WONDER", iWonderMod));
				szBuffer.append(NEWLINE);
				iBaseModifier += iWonderMod;
			}
		}

		if (eStateReligion != NO_RELIGION && kCity.isHasReligion(eStateReligion))
		{
			int iReligionMod = kOwner.getStateReligionBuildingProductionModifier();
			if (iReligionMod != 0)
			{
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_PROD_RELIGION", iReligionMod,
						GC.getInfo(eStateReligion).getTextKeyWide()));
				szBuffer.append(NEWLINE);
				iBaseModifier += iReligionMod;
			}
		}

        // doc: capital building production
        if (kOwner.getCapitalCity() != NULL && kOwner.getCapitalCity()->isHasRealBuilding(eBuilding))
        {
            int iCapitalBuildingMod = kOwner.getCapitalBuildingProductionModifier();
            if (iCapitalBuildingMod != 0)
            {
                szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_PROD_CAPITAL_BUILDING", iCapitalBuildingMod));
                szBuffer.append(NEWLINE);
                iBaseModifier += iCapitalBuildingMod;
            }
        }

        // doc: Holy Roman UP
        if (city.getCivilizationType() == HOLY_ROME)
        {
            if (kBuilding.getPrereqReligion() != NO_RELIGION && GC.getInfo(kBuilding.getBuildingClassType()).getMaxGlobalInstances() != 1)
            {
                if (kBuilding.getPrereqReligion() == kOwner.getStateReligion())
                {
                    szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_PROD_HOLY_ROME", 100));
                    szBuffer.append(NEWLINE);
                    iBaseModifier += 100;
                }
            }
        }
	}

	ProjectTypes eProject = kCity.getProductionProject();
	if (eProject != NO_PROJECT)
	{
		CvProjectInfo& kProject = GC.getInfo(eProject);

        // doc: existing projects
        if (GC.getGame().getProjectCreatedCount(eProject) > 0)
        {
            int iExistingMod = project.getExistingProductionModifier();
            if (0 != iExistingMod)
            {
                szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_PROD_EXISTING_PROJECT", iExistingMod));
                szBuffer.append(NEWLINE);
                iBaseModifier += iExistingMod;
            }
        }

		if (kProject.isSpaceship())
		{
			int iSpaceshipMod = kCity.getSpaceProductionModifier();
			iSpaceshipMod += kOwner.getSpaceProductionModifier();
			if (iSpaceshipMod != 0)
			{
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_PROD_SPACESHIP", iSpaceshipMod));
				szBuffer.append(NEWLINE);
				iBaseModifier += iSpaceshipMod;
			}
		}

		FOR_EACH_NON_DEFAULT_PAIR(kProject.
			getBonusProductionModifier(), Bonus, int)
		{
			if (kCity.hasBonus(perBonusVal.first))
			{
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_PROD_MOD_BONUS",
						perBonusVal.second, kProject.getTextKeyWide(),
						GC.getInfo(perBonusVal.first).getTextKeyWide()));
				szBuffer.append(NEWLINE);
				iBaseModifier += perBonusVal.second;
			}
		}
	}

	int iFoodProduction = (kCity.isFoodProduction() ?
			std::max(0, (kCity.getYieldRate(YIELD_FOOD) -
			kCity.foodConsumption(true))) : 0);
	if (iFoodProduction > 0)
	{
	    // doc: food production modifier
	    iFoodProduction *= 100 + kOwner.getFoodProductionModifier();
	    iFoodProduction /= 100;

		szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_PROD_FOOD", iFoodProduction, iFoodProduction));
		szBuffer.append(NEWLINE);
	} // advc.064b: To match the change in CvCity::getProductionDifference
	int iOverflowModifier = iBaseModifier - kCity.getBaseYieldRateModifier(YIELD_PRODUCTION);
	int iModProduction = iFoodProduction + (iBaseModifier * iBaseProduction
			// advc.064b:
			+ (bProcess ? 0 : (iPastOverflow * (100 + iOverflowModifier)))) / 100;
	FAssertMsg(iModProduction == kCity.getCurrentProductionDifference(false, !bProcess)
			// advc.064b: Display and rules don't quite align when no production chosen
			+ (kCity.isProduction() ? 0 : kCity.getFeatureProduction()),
			"Modified Production does not match actual value");

	szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_PROD_FINAL_YIELD", iModProduction));
	// <advc.064b>
	OrderTypes eOrderType = kCity.getOrderData(0).eOrderType;
	int iNewOverflow = 0;
	if(eOrderType != NO_ORDER && !bProcess)
	{
		iNewOverflow = iModProduction + kCity.getProduction() - kCity.getProductionNeeded();
		int iProductionGold = 0;
		int iLostProduction = 0;
		FAssertMsg((eUnit != NO_UNIT && iOverflowModifier == kCity.getProductionModifier(eUnit)) ||
				(eBuilding != NO_BUILDING && iOverflowModifier == kCity.getProductionModifier(eBuilding)) ||
				(eProject != NO_PROJECT && iOverflowModifier == kCity.getProductionModifier(eProject)),
				"Displayed modifier inconsistent with the one computed by CvCity");
		iNewOverflow = kCity.computeOverflow(iNewOverflow, iOverflowModifier,
				eOrderType, &iProductionGold, &iLostProduction);
		if(iLostProduction > 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_PROD_GOLD",
					iLostProduction, iProductionGold));
		}
	}
	else if(eOrderType != NO_ORDER)
		iNewOverflow = iPastOverflow;
	if(iNewOverflow > 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_PROD_NEW_OVERFLOW",
				iNewOverflow));
	}
	if(iFromChopsUnused != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_PROD_CHOPS_UNUSED",
				iFromChopsUnused));
	} // </advc.064b>
	// BUG - Building Additional Production - start
	if (bBuildingAdditionalYield && kCity.isActiveOwned())
		setBuildingAdditionalYieldHelp(szBuffer, kCity, YIELD_PRODUCTION, DOUBLE_SEPARATOR);
	// BUG - Building Additional Production - end
}


void CvGameTextMgr::parsePlayerTraits(CvWStringBuffer &szBuffer, PlayerTypes ePlayer)
{
	bool bFirst = true;

	for (int iTrait = 0; iTrait < GC.getNumTraitInfos(); ++iTrait)
	{
		if (GET_PLAYER(ePlayer).hasTrait((TraitTypes)iTrait))
		{
			if (bFirst)
			{
				szBuffer.append(L" (");
				bFirst = false;
			}
			else
			{
				szBuffer.append(L", ");
			}
			szBuffer.append(GC.getInfo((TraitTypes)iTrait).getDescription());
		}
	}

	if (!bFirst)
	{
		szBuffer.append(L")");
	}
}

// K-Mod. I've rewritten most of this function.
void CvGameTextMgr::parseLeaderHeadHelp(CvWStringBuffer &szBuffer,
	PlayerTypes eThisPlayer, PlayerTypes eOtherPlayer)
{
	if (eThisPlayer == NO_PLAYER)
		return;

	CvPlayerAI const& kPlayer = GET_PLAYER(eThisPlayer);

	szBuffer.append(CvWString::format(SETCOLR L"%s" ENDCOLR,
			TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"), kPlayer.getName()));

	parsePlayerTraits(szBuffer, eThisPlayer);

	// Some debug info: found-site traits, and AI flavours
	if (/*gDLL->getChtLvl() > 0*/ GC.getGame().isDebugMode() &&// advc.135c
		GC.altKey())
	{
		szBuffer.append(CvWString::format(SETCOLR SEPARATOR NEWLINE,
				TEXT_COLOR("COLOR_LIGHT_GREY")));
		// <advc.007>
		szBuffer.append(CvWString::format(L"id=%d\n", eThisPlayer));
		if (GC.getGame().isOption(GAMEOPTION_RANDOM_PERSONALITIES))
		{
			szBuffer.append(L"Personality: ");
			szBuffer.append(GC.getInfo(kPlayer.getPersonalityType()).getDescription());
			szBuffer.append(NEWLINE);
		} // </advc.007>
		CitySiteEvaluator citySiteEval(kPlayer);

		bool bFirst = true;

#define trait_info(x) do { \
	if (citySiteEval.is##x()) \
	{ \
		szBuffer.append(CvWString::format(L"%s"L#x, bFirst? L"" : L", ")); \
		bFirst = false; \
	} \
} while (0)

		trait_info(Ambitious);
		trait_info(Defensive);
		trait_info(EasyCulture);
		trait_info(Expansive);
		trait_info(ExtraYieldThreshold); // advc.031c: Renamed from "Financial"
		trait_info(ExtraYieldNaturalThreshold); // advc.908a
		trait_info(Seafaring);

#undef trait_info

#define flavour_info(x) do { \
	if (kPlayer.AI_getFlavorValue(FLAVOR_##x)) \
	{ \
		szBuffer.append(CvWString::format(L"%s"L#x L"=%d", bFirst? L"" : L", ", \
				kPlayer.AI_getFlavorValue(FLAVOR_##x))); \
		bFirst = false; \
	} \
} while (0)

		flavour_info(MILITARY);
		flavour_info(RELIGION);
		flavour_info(PRODUCTION);
		flavour_info(GOLD);
		flavour_info(SCIENCE);
		flavour_info(CULTURE);
		flavour_info(GROWTH);

#undef flavour_info

		szBuffer.append(SEPARATOR ENDCOLR);
	}

	//szBuffer.append(L"\n");

	if (eOtherPlayer == NO_PLAYER)
	{
		getWarWearinessString(szBuffer, eThisPlayer, NO_PLAYER); // total ww
		return; // advc
	}
	CvTeam& kThisTeam = GET_TEAM(kPlayer.getTeam());
	TeamTypes eOtherTeam = GET_PLAYER(eOtherPlayer).getTeam();
	if (!kThisTeam.isHasMet(eOtherTeam))
		return;
	getVassalInfoString(szBuffer, eThisPlayer); // K-Mod
	/*	disabled by K-Mod. (The player should not be told
		exactly how many espionage points everyone has.) */
	//getEspionageString(szBuffer, eThisPlayer, eOtherPlayer);
	if (eOtherPlayer != eThisPlayer)
	{
		getAttitudeString(szBuffer, eThisPlayer, eOtherPlayer);
		getActiveDealsString(szBuffer, eThisPlayer, eOtherPlayer);
	}
	getWarWearinessString(szBuffer, eThisPlayer, eOtherPlayer);
	/*	K-Mod. Allow the "other relations string" to display
		even if eOtherPlayer == eThisPlayer. It's useful info. */
	getOtherRelationsString(szBuffer, eThisPlayer, eOtherPlayer);
}

// advc.152:
void CvGameTextMgr::parseWarTradesHelp(CvWStringBuffer& szBuffer,
	PlayerTypes eThisPlayer, PlayerTypes eOtherPlayer)
{
	/*  Same checks as in getAttitudeText (AttitudeUtil.py), which displays
		the fist icon. */
	PlayerTypes const eActivePlayer = getActivePlayer();
	if (TEAMID(eOtherPlayer) == TEAMID(eActivePlayer) ||
		eOtherPlayer == NO_PLAYER || TEAMID(eThisPlayer) == TEAMID(eActivePlayer) ||
		TEAMID(eThisPlayer) == TEAMID(eOtherPlayer) || eThisPlayer == NO_PLAYER ||
		GET_TEAM(eThisPlayer).isAtWar(TEAMID(eOtherPlayer)) ||
		GET_TEAM(eOtherPlayer).isHuman())
	{
		return;
	}
	if (GET_TEAM(eThisPlayer).AI_declareWarTrade(TEAMID(eOtherPlayer),
		TEAMID(eActivePlayer)) == NO_DENIAL)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_WILLING_START_WAR",
				GET_PLAYER(eOtherPlayer).getName()));
	}
}


void CvGameTextMgr::parseLeaderLineHelp(CvWStringBuffer &szBuffer,
	PlayerTypes eThisPlayer, PlayerTypes eOtherPlayer)
{
	// advc: This is apparently dead code
	FErrorMsg("Just checking if this function is ever even called");
	if (eThisPlayer == NO_PLAYER || eOtherPlayer == NO_PLAYER)
		return;

	CvTeam& thisTeam = GET_TEAM(eThisPlayer);
	CvTeam& otherTeam = GET_TEAM(eOtherPlayer);

	if (thisTeam.getID() == otherTeam.getID())
	{
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_PERMANENT_ALLIANCE"));
		szBuffer.append(NEWLINE);
	}
	else if (thisTeam.isAtWar(otherTeam.getID()))
	{
		szBuffer.append(gDLL->getText("TXT_KEY_CONCEPT_WAR"));
		szBuffer.append(NEWLINE);
	}
	else
	{
		if (thisTeam.isDefensivePact(otherTeam.getID()))
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_DEFENSIVE_PACT"));
			szBuffer.append(NEWLINE);
		}
		if (thisTeam.isOpenBorders(otherTeam.getID()))
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_OPEN_BORDERS"));
			szBuffer.append(NEWLINE);
		} // <advc.034>
		else if(thisTeam.isDisengage(otherTeam.getID()))
		{
			CvWString szString;
			buildDisengageString(szString, eThisPlayer, eOtherPlayer);
			szBuffer.append(szString);
			szBuffer.append(NEWLINE);
		} // </advc.034>
		if (thisTeam.isVassal(otherTeam.getID()))
		{	// <advc.130v> Make clearer when a vassal is capitulated
			if(thisTeam.isCapitulated())
				szBuffer.append(gDLL->getText("TXT_KEY_ATTITUDE_VASSAL_CAP_OF",
						GET_TEAM(thisTeam.getMasterTeam()).getName().GetCString()));
			else szBuffer.append(gDLL->getText("TXT_KEY_ATTITUDE_VASSAL_OF",
					GET_TEAM(thisTeam.getMasterTeam()).getName().GetCString()));
			//szBuffer.append(gDLL->getText("TXT_KEY_MISC_VASSAL")); // </advc.130v>
			szBuffer.append(NEWLINE);
		}
	}
}


void CvGameTextMgr::getActiveDealsString(CvWStringBuffer &szBuffer,
	PlayerTypes eThisPlayer, PlayerTypes eOtherPlayer, /* advc.087: */ bool bExludeDual)
{
	FOR_EACH_DEAL(pDeal)
	{
		if (!pDeal->isBetween(eThisPlayer, eOtherPlayer))
			continue;
		// <advc.087>
		if(bExludeDual && pDeal->isAllDual())
			continue; // </advc.087>
		szBuffer.append(NEWLINE);
		szBuffer.append(CvWString::format(L"%c", gDLL->getSymbolID(BULLET_CHAR)));
		getDealString(szBuffer, *pDeal, eThisPlayer);
	}
}


void CvGameTextMgr::buildHintsList(CvWStringBuffer& szBuffer)
{
	/*  <avdc.008d> Hints are no longer guaranteed to be unique, and this is
		bad when listing them in Civilopedia. Cleaner solution would be to keep
		them unique in XML, but add a frequency tag. However, I don't think the
		code that shows hints while loading is in the SDK, so this doesn't work,
		and the only way I see to affect the frequency is to define some hints
		multiple times in XML. */
	/*  Hopefully this uses a decent hash function, but, since it's only called
		when opening the Hints section of Civilopedia, it doesn't really matter. */
	std::set<CvWString> uniqueHints;
	for(int i = 0; i < GC.getNumHintInfos(); i++)
		uniqueHints.insert(CvWString(GC.getHintInfo(i).getText()));
	for(std::set<CvWString>::const_iterator it = uniqueHints.begin(); // </advc.008d>
		it != uniqueHints.end(); ++it)
	{
		szBuffer.append(CvWString::format(L"%c%s", gDLL->getSymbolID(BULLET_CHAR),
				it->c_str())); //GC.getHints(i).getText())); // advc.008d
		szBuffer.append(NEWLINE);
		szBuffer.append(NEWLINE);
	}
}

void CvGameTextMgr::setCommerceHelp(CvWStringBuffer &szBuffer, CvCity const& kCity,
	CommerceTypes eCommerce)
{
	// BUG - Building Additional Commerce - start
	bool const bBuildingAdditionalCommerce =
			(BUGOption::isEnabled("MiscHover__BuildingAdditionalCommerce", false) ||
			GC.altKey()); // advc.063
	if ((kCity.getCommerceRateTimes100(eCommerce) == 0 &&
		!bBuildingAdditionalCommerce) ||
	// BUG - Building Additional Commerce - end
		kCity.isDisorder()) // advc.001
	{
		return;
	}
	CvCommerceInfo const& kCommerce = GC.getInfo(eCommerce);
	int const iCommerceChar = kCommerce.getChar();
	CvPlayer const& kOwner = GET_PLAYER(kCity.getOwner());

	// <advc.004p>
	int iBaseCommerceRate = 0;
	CvWString szRate;
	if (kOwner.getCommercePercent(eCommerce) > 0) // </advc.004p>
	{
		setYieldHelp(szBuffer, kCity, YIELD_COMMERCE);
		// Slider
		iBaseCommerceRate = kCity.getCommerceFromPercent(eCommerce,
				kCity.getYieldRate(YIELD_COMMERCE) * 100);
		szRate = CvWString::format(L"%d.%02d",
				iBaseCommerceRate / 100, iBaseCommerceRate % 100);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_SLIDER_PERCENT_FLOAT",
				kOwner.getCommercePercent(eCommerce), kCity.getYieldRate(YIELD_COMMERCE),
				szRate.GetCString(), iCommerceChar));
		szBuffer.append(NEWLINE);
	} // advc.004p

	bool bNeedSubtotal = false; // BUG - Base Commerce
	{
		int iSpecialistCommerce = kCity.getSpecialistCommerce(eCommerce) +
				(kCity.getSpecialistPopulation() + kCity.getNumGreatPeople() city.countNoGlobalEffectsFreeSpecialists()) * // doc: certain specialists do not get effects
				kOwner.getSpecialistExtraCommerce(eCommerce);
		if (iSpecialistCommerce != 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_SPECIALIST_COMMERCE",
					iSpecialistCommerce, iCommerceChar, L"TXT_KEY_CONCEPT_SPECIALISTS"));
			szBuffer.append(NEWLINE);
			iBaseCommerceRate += 100 * iSpecialistCommerce;
			bNeedSubtotal = true; // BUG - Base Commerce
		}
	}
	{
		int iReligionCommerce = kCity.getReligionCommerce(eCommerce);
		if (iReligionCommerce != 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_RELIGION_COMMERCE",
					iReligionCommerce, iCommerceChar));
			szBuffer.append(NEWLINE);
			iBaseCommerceRate += 100 * iReligionCommerce;
			bNeedSubtotal = true; // BUG - Base Commerce
		}
	}
	{
		int iCorporationCommerce = kCity.getCorporationCommerce(eCommerce);
		if (iCorporationCommerce != 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_CORPORATION_COMMERCE",
					iCorporationCommerce, iCommerceChar));
			szBuffer.append(NEWLINE);
			iBaseCommerceRate += 100 * iCorporationCommerce;
			bNeedSubtotal = true; // BUG - Base Commerce
		}
	}
	{
		int iBuildingCommerce = kCity.getBuildingCommerce(eCommerce);
		if (iBuildingCommerce != 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_BUILDING_COMMERCE",
					iBuildingCommerce, iCommerceChar));
			szBuffer.append(NEWLINE);
			iBaseCommerceRate += 100 * iBuildingCommerce;
			bNeedSubtotal = true; // BUG - Base Commerce
		}
	}
	{
		int iFreeCityCommerce = kOwner.getFreeCityCommerce(eCommerce);
		if (iFreeCityCommerce != 0)
		{
			/*szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_FREE_CITY_COMMERCE",
					iFreeCityCommerce, iCommerceChar));*/
			// <advc.004g>
			szBuffer.append(CvWString::format(L"%c", gDLL->getSymbolID(BULLET_CHAR)));
			if (iFreeCityCommerce > 0)
				szBuffer.append(L"+");
			szBuffer.append(CvWString::format(L"%d%c ",
					iFreeCityCommerce, iCommerceChar));
			szBuffer.append(gDLL->getText("TXT_KEY_FROM_TRAIT"));
			// </advc.004g>
			szBuffer.append(NEWLINE);
			iBaseCommerceRate += 100 * iFreeCityCommerce;
			bNeedSubtotal = true; // BUG - Base Commerce
		}
	}
	// doc: Himeji Castle effect
	{
	    if (eCommerceType == COMMERCE_CULTURE && city.isHasBuildingEffect(HIMEJI_CASTLE))
	    {
	        int iUnitCulture = 0;
            FOR_EACH_UNIT_IN(pUnit, city.getPlot())
            {
                // TODO: refactor
                if (pUnit->getOwner() == city.getOwner() && pUnit->isFortifyble() && pUnit->getFortifyTurns() >= GC.getDefinNT("MAX_FORTIFY_TURNS"))
                    iUnitCulture += pUnit->getLevel();
            }

            if (iUnitCulture != 0)
            {
                szBuffer.append(NEWLINE);
                szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_HIMEJI_UNIT_CULTURE",
                        iUnitCulture,
                        info.getChar()));
                iBaseCommerceRate += 100 * iUnitCulture;
                bNeedSubtotal = true;
            }
	    }

        // Leoreth: Himeji Castle effect
        int iUnitCulture = 0;
        if (eCommerceType == COMMERCE_CULTURE && city.isHasRealBuilding(HIMEJI_CASTLE) && GET_PLAYER(city.getOwner()).isHasBuildingEffect(HIMEJI_CASTLE))
        {
            CvUnit* pUnit;
            for (int i = 0; i < city.plot()->getNumUnits(); i++)
            {
                pUnit = city.plot()->getUnitByIndex(i);

                if (pUnit->getOwner() == city.getOwner() && pUnit->isFortifyable() && pUnit->getFortifyTurns() >= GC.getDefineINT("MAX_FORTIFY_TURNS"))
                {
                    iUnitCulture += pUnit->getLevel();
                }
            }
        }

        if (0 != iUnitCulture)
        {
            szBuffer.append(NEWLINE);
            szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_HIMEJI_UNIT_CULTURE", iUnitCulture, info.getChar()));
            iBaseCommerceRate += 100 * iUnitCulture;
            bNeedSubtotal = true;
        }
	}
	// BUG - Base Commerce - start
	if (bNeedSubtotal && kCity.getCommerceRateModifier(eCommerce) != 0
		// advc.065: No longer optional
		/*&& BUGOption::isEnabled("MiscHover__BaseCommerce", false)*/)
	{
		CvWString szYield = CvWString::format(L"%d.%02d",
				iBaseCommerceRate / 100, iBaseCommerceRate % 100);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_COMMERCE_SUBTOTAL_YIELD_FLOAT",
				kCommerce.getTextKeyWide(), szYield.GetCString(), iCommerceChar));
		szBuffer.append(NEWLINE);
	} // BUG - Base Commerce - end

	FAssertMsg(kCity.getBaseCommerceRateTimes100(eCommerce) == iBaseCommerceRate,
			"Base Commerce rate does not agree with actual value");

	int iModifier = 100;
	{
		int iBuildingMod = 0;
		FOR_EACH_ENUM2(Building, eBuilding)
		{
			if (GET_TEAM(kOwner.getTeam()).isObsoleteBuilding(eBuilding))
				continue;
			CvBuildingInfo const& kBuilding = GC.getInfo(eBuilding);
			iBuildingMod += kBuilding.getCommerceModifier(eCommerce) *
					kCity.getNumBuilding(eBuilding);

            // doc: Himeji Castle effect: defense modifier counts as culture modifier
            if (eBuilding == HIMEJI_CASTLE && city.isHasBuildingEffect(eBuilding) && eCommerceType == COMMERCE_CULTURE)
                iBuildingMod += kBuilding.getDefenseModifier();

			for (MemberIter itMember(kOwner.getTeam()); itMember.hasNext(); ++itMember)
			{
				FOR_EACH_CITY(pLoopCity, *itMember)
				{
					iBuildingMod += kBuilding.getGlobalCommerceModifier(eCommerce) *
							pLoopCity->getNumBuilding(eBuilding);
				}
			}
		}
		if (iBuildingMod != 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_YIELD_BUILDINGS",
					iBuildingMod, iCommerceChar));
			szBuffer.append(NEWLINE);
			iModifier += iBuildingMod;
		}
	}
    // doc: bonus commerce rate modifier
	{
	    int iBonusCommerceMod = city.getBonusCommerceRateModifier(eCommerce);
        if (iBuildingMod != 0)
        {
            szBuffer.append(NEWLINE);
            szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_YIELD_BUILDINGS",
                    iBuildingMod, info.getChar()));
            iModifier += iBuildingMod;
        }
	}
	// doc: culture level commerce modifier
	{
        int iCultureMod = city.getCultureLevel() * city.getCultureCommerceRateModifier(eCommerce);
        if (iCultureMod != 0)
        {
            szBuffer.append(NEWLINE);
            szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_YIELD_CULTURE",
                    iCultureMod, info.getChar()));
            iModifier += iCultureMod;
        }
	}
	// doc: power commerce modifier
	{
	    if (city.isPower())
        {
            int iPowerMod = city.getPowerCommerceRateModifier(eCommerce);
            if (iPowerMod != 0)
            {
                szBuffer.append(NEWLINE);
                szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_YIELD_POWER",
                        iPowerMod, info.getChar()));
                iModifier += iPowerMod;
            }
        }
	}
    // doc: Golden Record effect: spaceship production modifies culture rate
    {
        if (eCommerceType == COMMERCE_CULTURE && GET_TEAM(city.getTeam()).getProjectCount(PROJECT_GOLDEN_RECORD) > 0)
        {
            int iSpaceshipMod = city.getSpaceProductionModifier() / 2;
            if (iSpaceshipMod != 0)
            {
                szBuffer.append(NEWLINE);
                szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_COMMERCE_SPACE_PRODUCTION",
                        iSpaceshipMod, info.getChar()));
                iModifier += iSpaceshipMod;
            }
        }
    }

	FOR_EACH_ENUM(Trait)
	{
		if (!kCity.hasTrait(eLoopTrait))
			continue;
		CvTraitInfo const& kTrait = GC.getInfo(eLoopTrait);
		int iTraitMod = kTrait.getCommerceModifier(eCommerce);
		if (iTraitMod != 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_COMMERCE_TRAIT", iTraitMod,
					iCommerceChar, kTrait.getTextKeyWide()));
			szBuffer.append(NEWLINE);
			iModifier += iTraitMod;
		}
	}
	{
		int iCapitalMod = (!kCity.isCapital() ? 0 :
				kOwner.getCapitalCommerceRateModifier(eCommerce));
		if (iCapitalMod != 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_YIELD_CAPITAL",
					iCapitalMod, iCommerceChar));
			szBuffer.append(NEWLINE);
			iModifier += iCapitalMod;
		}
	}
	{
		int iCivicMod = 0;
		FOR_EACH_ENUM(CivicOption)
		{
			if (kOwner.getCivics(eLoopCivicOption) != NO_CIVIC)
			{
				iCivicMod += GC.getInfo(kOwner.getCivics(eLoopCivicOption)).
						getCommerceModifier(eCommerce);
			}
		}
		if (iCivicMod != 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_YIELD_CIVICS",
					iCivicMod, iCommerceChar));
			szBuffer.append(NEWLINE);
			iModifier += iCivicMod;
		}
	}
	// Techs (K-Mod)
	/* Rather than counting just tech modifiers, we might as well just have a
		generic case which supports other sources too. */
	/*{int iTechMod = 0;
	FOR_EACH_ENUM(Tech) {
		if (GET_TEAM(kOwner.getTeam()).isHasTech(eLoopTech))
			iTechMod += GC.getInfo(eLoopTech).getCommerceModifier(eCommerce);
	} if (iTechMod != 0) {
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_MODIFIER_FROM_CIV", iTechMod, iCommerceChar));
		szBuffer.append(NEWLINE);
		iModifier += iCivicMod;
	}}*/
	// Left over modifiers!
	{
		int iUnaccountedModifiers = kCity.getTotalCommerceRateModifier(eCommerce)
				- iModifier;
		if (iUnaccountedModifiers != 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_MODIFIER_FROM_CIV",
					iUnaccountedModifiers, iCommerceChar));
			szBuffer.append(NEWLINE);
			iModifier += iUnaccountedModifiers;
		}
	} // K-Mod end
	int iModYield = (iModifier * iBaseCommerceRate) / 100;
	{
		int iProductionToCommerce = kCity.getProductionToCommerceModifier(eCommerce) *
				kCity.getYieldRate(YIELD_PRODUCTION);
		if (iProductionToCommerce != 0)
		{
			if (iProductionToCommerce % 100 == 0)
			{
				szBuffer.append(
						gDLL->getText("TXT_KEY_MISC_HELP_PRODUCTION_TO_COMMERCE",
						iProductionToCommerce / 100, iCommerceChar));
			}
			else
			{
				szRate = CvWString::format(L"+%d.%02d",
						iProductionToCommerce / 100, iProductionToCommerce % 100);
				szBuffer.append(
						gDLL->getText("TXT_KEY_MISC_HELP_PRODUCTION_TO_COMMERCE_FLOAT",
						szRate.GetCString(), iCommerceChar));
			}
			szBuffer.append(NEWLINE);
			iModYield += iProductionToCommerce;
		}
	}
	if (eCommerce == COMMERCE_CULTURE &&
		GC.getGame().isOption(GAMEOPTION_NO_ESPIONAGE))
	{
		int iEspionageToCommerce = kCity.getCommerceRateTimes100(COMMERCE_CULTURE)
				- iModYield;
		if (iEspionageToCommerce != 0)
		{
			if (iEspionageToCommerce % 100 == 0)
			{
				szBuffer.append(
						gDLL->getText("TXT_KEY_MISC_HELP_COMMERCE_TO_COMMERCE",
						iEspionageToCommerce / 100, iCommerceChar,
						GC.getInfo(COMMERCE_ESPIONAGE).getChar()));
				szBuffer.append(NEWLINE);
			}
			else
			{
				szRate = CvWString::format(L"+%d.%02d",
						iEspionageToCommerce / 100, iEspionageToCommerce % 100);
				szBuffer.append(
						gDLL->getText("TXT_KEY_MISC_HELP_COMMERCE_TO_COMMERCE_FLOAT",
						szRate.GetCString(), iCommerceChar,
						GC.getInfo(COMMERCE_ESPIONAGE).getChar()));
				szBuffer.append(NEWLINE);
			}
			iModYield += iEspionageToCommerce;
		}
	}
	FAssertMsg(iModYield == kCity.getCommerceRateTimes100(eCommerce),
			"Commerce yield does not match actual value");

    // doc: civilization culture modifier
    int iFinalModYield = iModYield;
    if (eCommerce == COMMERCE_CULTURE)
    {
		int iCultureModifier = kOwner.getModifier(MODIFIER_CULTURE);
		if (iCultureModifier != 100)
		{
			iFinalModYield = iModYield * iCultureModifier / 100;

			szBuffer.append(SEPARATOR);
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_CIVILIZATION_CULTURE_MODIFIER",
			        iCultureModifier - 100, info.getChar()));
		}
    }

	CvWString szYield = CvWString::format(L"%d.%02d", iFinalModYield / 100, iFinalModYield % 100);
	szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_COMMERCE_FINAL_YIELD_FLOAT",
			kCommerce.getTextKeyWide(), szYield.GetCString(), iCommerceChar));
	// BUG - Building Additional Commerce - start
	if (bBuildingAdditionalCommerce && kCity.isActiveOwned())
		setBuildingAdditionalCommerceHelp(szBuffer, kCity, eCommerce, DOUBLE_SEPARATOR);
	// BUG - Building Additional Commerce - end
}

void CvGameTextMgr::setYieldHelp(CvWStringBuffer &szBuffer, CvCity const& kCity, YieldTypes eYield)
{
	CvYieldInfo const & kYield = GC.getInfo(eYield);
	int const iYieldChar = kYield.getChar();
	CvPlayer const& kOwner = GET_PLAYER(kCity.getOwner());

	int iBaseYieldRate = kCity.getBaseYieldRate(eYield);
	szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_BASE_YIELD",
			kYield.getTextKeyWide(), iBaseYieldRate, iYieldChar));
	szBuffer.append(NEWLINE);

	if (eYieldType == YIELD_FOOD)
	{
		// doc: Harappan UP: positive health contributes to city growth in Ancient era
		if (city.getCivilizationType() == HARAPPA && kOwner.getCurrentEra() == ERA_ANCIENT)
		{
			if (!city.isFoodProduction() && city.getBaseYieldRate(YIELD_FOOD) * city.getBaseYieldRateModifier(YIELD_FOOD) - city.foodConsumption() * 100 > 1 && city.goodHealth() > city.badHealth())
				iBaseProduction += city.goodHealth() - city.badHealth();
		}

		// doc: Khmer UP: extra food from building production in capital
		if (city.getCivilizationType() == KHMER && city.isCapital() && city.isProductionBuilding() && !city.isFoodProduction())
			iBaseProduction += city.getYieldRate(YIELD_PRODUCTION) * (100 + city.getProductionModifier(city.getProductionBuilding())) / 100 / 5;

		// doc: Lotus Temple effect
		if (kOwner.isHasBuildingEffect(LOTUS_TEMPLE))
			iBaseProduction += city.getReligionCount() - (kOwner.getStateReligion() != NO_RELIGION && city.isHasReligion(GET_PLAYER(city.getOwnerINLINE()).getStateReligion()) ? 1 : 0);
	}

	int iBaseModifier = 100;
	{
		int iBuildingMod = 0;
		FOR_EACH_ENUM2(Building, eBuilding)
		{
			CvBuildingInfo const& kBuilding = GC.getInfo(eBuilding);
			if (GET_TEAM(kOwner.getTeam()).isObsoleteBuilding(eBuilding))
				continue;
			iBuildingMod += kBuilding.getYieldModifier(eYield) *
					kCity.getNumBuilding(eBuilding);
			for (MemberIter itMember(kOwner.getTeam()); itMember.hasNext(); ++itMember)
			{
				FOR_EACH_CITY(pLoopCity, *itMember)
				{
						iBuildingMod += kBuilding.getGlobalYieldModifier(eYield) *
								pLoopCity->getNumBuilding(eBuilding);
				}
			}
		}
		// doc: continent effects apply to nearby landmasses
		iBuildingMod += kCity.continentArea().getYieldRateModifier(kOwner.getID(), eYield);
		if (iBuildingMod != 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_YIELD_BUILDINGS",
					iBuildingMod, iYieldChar));
			szBuffer.append(NEWLINE);
			iBaseModifier += iBuildingMod;
		}
	}
	if (kCity.isPower())
	{
		int iPowerMod = kCity.getPowerYieldRateModifier(eYield);
		if (iPowerMod != 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_YIELD_POWER",
					iPowerMod, iYieldChar));
			szBuffer.append(NEWLINE);
			iBaseModifier += iPowerMod;
		}
	}
	{
		int iBonusMod = kCity.getBonusYieldRateModifier(eYield);
		if (iBonusMod != 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_YIELD_BONUS",
					iBonusMod, iYieldChar));
			szBuffer.append(NEWLINE);
			iBaseModifier += iBonusMod;
		}
	}
	if (kCity.isCapital())
	{
		int iCapitalMod = kOwner.getCapitalYieldRateModifier(eYield);
		if (iCapitalMod != 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_YIELD_CAPITAL",
					iCapitalMod, iYieldChar));
			szBuffer.append(NEWLINE);
			iBaseModifier += iCapitalMod;
		}
	}
	{
		int iCivicMod = 0;
		FOR_EACH_ENUM(CivicOption)
		{
			if (kOwner.getCivics(eLoopCivicOption) != NO_CIVIC)
			{
				iCivicMod += GC.getInfo(kOwner.getCivics(eLoopCivicOption)).
						getYieldModifier(eYield);
			}
		}
		if (iCivicMod != 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_YIELD_CIVICS",
					iCivicMod, iYieldChar));
			szBuffer.append(NEWLINE);
			iBaseModifier += iCivicMod;
		}
	}
	FAssertMsg((iBaseModifier * iBaseYieldRate) / 100 == kCity.getYieldRate(eYield),
			"Yield Modifier in setProductionHelp does not agree with actual value");
}

void CvGameTextMgr::setConvertHelp(CvWStringBuffer& szBuffer, PlayerTypes ePlayer, ReligionTypes eReligion)
{
	CvWString szReligion = L"TXT_KEY_MISC_NO_STATE_RELIGION";

	if (eReligion != NO_RELIGION)
	{
		szReligion = GC.getInfo(eReligion).getTextKeyWide();
	}
	// doc: pagan religion name
	else if (GET_PLAYER(ePlayer).isStateReligion())
	{
		CvWString szPaganReligionName = GC.getInfo(GC.getInfo(GET_PLAYER(ePlayer).getCivilizationType()).getPaganReligion()).getDescription();
		if (!szPaganReligionName.length() == 0)
		{
			szReligion = szPaganReligionName;
		}
	}

	szBuffer.assign(gDLL->getText("TXT_KEY_MISC_CANNOT_CONVERT_TO", szReligion.GetCString()));

	if (GET_PLAYER(ePlayer).isAnarchy())
	{
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_WHILE_IN_ANARCHY"));
	}
	else if (GET_PLAYER(ePlayer).getStateReligion() == eReligion)
	{
		szBuffer.append(L". ");
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_ALREADY_STATE_REL"));
		szBuffer.append(L"."); // advc.004g
	}
	else if (GET_PLAYER(ePlayer).getConversionTimer() > 0)
	{
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_ANOTHER_REVOLUTION_RECENTLY"));
		szBuffer.append(L". ");
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_WAIT_MORE_TURNS", GET_PLAYER(ePlayer).getConversionTimer()));
		szBuffer.append(L"."); // advc.004g
	}
}

void CvGameTextMgr::setRevolutionHelp(CvWStringBuffer& szBuffer, PlayerTypes ePlayer)
{
	szBuffer.assign(gDLL->getText("TXT_KEY_MISC_CANNOT_CHANGE_CIVICS"));

	if (GET_PLAYER(ePlayer).isAnarchy())
	{
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_WHILE_IN_ANARCHY"));
	}
	else if (GET_PLAYER(ePlayer).getRevolutionTimer() > 0)
	{
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_ANOTHER_REVOLUTION_RECENTLY"));
		szBuffer.append(L" : ");
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_WAIT_MORE_TURNS", GET_PLAYER(ePlayer).getRevolutionTimer()));
	}
}

void CvGameTextMgr::setVassalRevoltHelp(CvWStringBuffer& szBuffer, TeamTypes eMaster, TeamTypes eVassal)
{
	if (NO_TEAM == eMaster || NO_TEAM == eVassal)
	{
		return;
	}

	if (!GET_TEAM(eVassal).isCapitulated())
	{
		return;
	}

	if (GET_TEAM(eMaster).isParent(eVassal))
	{
		return;
	}

	CvTeam& kMaster = GET_TEAM(eMaster);
	CvTeam& kVassal = GET_TEAM(eVassal);

	int iMasterLand = kMaster.getTotalLand(false);
	// advc.112: Lower bound added
	int iVassalLand = std::max(10, kVassal.getTotalLand(false));
	if (iMasterLand > 0 && GC.getDefineINT("FREE_VASSAL_LAND_PERCENT") >= 0)
	{
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_VASSAL_LAND_STATS", (iVassalLand * 100) / iMasterLand, GC.getDefineINT("FREE_VASSAL_LAND_PERCENT")));
	}

	int iMasterPop = kMaster.getTotalPopulation(false);
	int iVassalPop = kVassal.getTotalPopulation(false);
	if (iMasterPop > 0 && GC.getDefineINT("FREE_VASSAL_POPULATION_PERCENT") >= 0)
	{
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_VASSAL_POPULATION_STATS", (iVassalPop * 100) / iMasterPop, GC.getDefineINT("FREE_VASSAL_POPULATION_PERCENT")));
	}

	if (GC.getDefineINT("VASSAL_REVOLT_OWN_LOSSES_FACTOR") > 0 && kVassal.getVassalPower() > 0)
	{
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_VASSAL_AREA_LOSS", (iVassalLand * 100) / kVassal.getVassalPower(), GC.getDefineINT("VASSAL_REVOLT_OWN_LOSSES_FACTOR")));
	}

	if (GC.getDefineINT("VASSAL_REVOLT_MASTER_LOSSES_FACTOR") > 0 && kVassal.getMasterPower() > 0)
	{
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_MASTER_AREA_LOSS", (iMasterLand * 100) / kVassal.getMasterPower(), GC.getDefineINT("VASSAL_REVOLT_MASTER_LOSSES_FACTOR")));
	}
}

void CvGameTextMgr::parseGreatPeopleHelp(CvWStringBuffer &szBuffer, CvCity const& kCity)
{
	if (kCity.getOwner() == NO_PLAYER)
		return;
	CvPlayer const& kOwner = GET_PLAYER(kCity.getOwner());
	szBuffer.assign(gDLL->getText("TXT_KEY_MISC_GREAT_PERSON", kCity.getGreatPeopleProgress(),
			kOwner.greatPeopleThreshold(false)));
	int iTurnsLeft = kCity.GPTurnsLeft(); // advc.001c
	int const iGPRate = kCity.getGreatPeopleRate();
	if (iGPRate > 0)
	{
		int iGPPLeft = kOwner.greatPeopleThreshold(false) - kCity.getGreatPeopleProgress();
		if (iGPPLeft > 0)
		{	// advc.001c: Moved into CvCity::GPTurnsLeft
			/*iTurnsLeft = iGPPLeft / iGPRate;
			if (iTurnsLeft * kCity.getGreatPeopleRate() <  iGPPLeft)
				iTurnsLeft++;*/
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("INTERFACE_CITY_TURNS",
					std::max(1, iTurnsLeft)));
		}
	}

	int iTotalGreatPeopleUnitProgress = 0;
	FOR_EACH_ENUM2(Unit, eGPType)
	{
		iTotalGreatPeopleUnitProgress += kCity.getGreatPeopleUnitProgress(eGPType);
		// advc.001c:
		iTotalGreatPeopleUnitProgress += kCity.getGreatPeopleUnitRate(eGPType);
	}

	if (iTotalGreatPeopleUnitProgress > 0)
	{
		szBuffer.append(SEPARATOR);
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_PROB"));

		std::vector<std::pair<UnitTypes,int> > aUnitProgress;
		// advc.001c: BtS code moved into CvCity::GPProjection
		kCity.GPProjection(aUnitProgress);
		for (size_t i = 0; i < aUnitProgress.size(); i++)
		{
			szBuffer.append(CvWString::format(L"%s%s - %d%%", NEWLINE,
					GC.getInfo(aUnitProgress[i].first).getDescription(),
					aUnitProgress[i].second));
		}
	}
	// BUG - Building Additional Great People - start
	bool bBuildingAdditionalGreatPeople =
			(BUGOption::isEnabled("MiscHover__BuildingAdditionalGreatPeople", false) ||
			GC.altKey()); // advc.063
	if (iGPRate == 0 && !bBuildingAdditionalGreatPeople)
	// BUG - Building Additional Great People - end
		return;
	// BULL - Great People Rate Breakdown - start (advc.078)
	//if (BUGOption::isEnabled("MiscHover__GreatPeopleRateBreakdown", true))
	{
		bool bFirst = true;
		{
			int iRate = 0;
			FOR_EACH_ENUM(Specialist)
			{
				iRate += (kCity.getSpecialistCount(eLoopSpecialist) +
						kCity.getFreeSpecialistCount(eLoopSpecialist)) *
						GC.getInfo(eLoopSpecialist).getGreatPeopleRateChange();
			}
			if (iRate > 0)
			{
				if (bFirst)
				{
					szBuffer.append(SEPARATOR);
					bFirst = false;
				}
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_SPECIALIST_COMMERCE",
						iRate, gDLL->getSymbolID(GREAT_PEOPLE_CHAR),
						L"TXT_KEY_CONCEPT_SPECIALISTS"));
			}
		}
		{
			int iRate = 0;
			FOR_EACH_ENUM2(Building, eBuilding)
			{
				if (kCity.getNumBuilding(eBuilding) > 0 &&
					// advc (future-proofing):
					!GET_TEAM(kCity.getTeam()).isObsoleteBuilding(eBuilding))
				{
					iRate += kCity.getNumBuilding(eBuilding) *
							GC.getInfo(eBuilding).getGreatPeopleRateChange();
				}
			}
			if (iRate > 0)
			{
				if (bFirst)
				{
					szBuffer.append(SEPARATOR);
					bFirst = false;
				}
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_BUILDING_COMMERCE",
						iRate, gDLL->getSymbolID(GREAT_PEOPLE_CHAR)));
			}
		}
	} // BULL - Great People Rate Breakdown - end
	szBuffer.append(SEPARATOR);
	szBuffer.append(NEWLINE);
	// <advc.004> Skip base rate if final rate will be the same
	int const iTotalGreatPeopleRateModifier = kCity.getTotalGreatPeopleRateModifier();
	if (iTotalGreatPeopleRateModifier != 100) // </advc.004>
	{
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_GREATPEOPLE_BASE_RATE",
				kCity.getBaseGreatPeopleRate()));
		szBuffer.append(NEWLINE);
	}
	int iModifier = 100;
	{
		int iBuildingMod = 0;
		FOR_EACH_ENUM2(Building, eBuilding)
		{
			CvBuildingInfo const& kBuilding = GC.getInfo(eBuilding);
			if (kCity.getNumBuilding(eBuilding) > 0 &&
				!GET_TEAM(kCity.getTeam()).isObsoleteBuilding(eBuilding))
			{
				iBuildingMod += kCity.getNumBuilding(eBuilding) *
						kBuilding.getGreatPeopleRateModifier();
			}
			for (MemberIter itMember(kOwner.getTeam()); itMember.hasNext(); ++itMember)
			{
				FOR_EACH_CITY(pLoopCity, *itMember)
				{
					if (pLoopCity->getNumBuilding(eBuilding) > 0 &&
						!GET_TEAM(pLoopCity->getTeam()).isObsoleteBuilding(eBuilding))
					{
						iBuildingMod += pLoopCity->getNumBuilding(eBuilding) *
								kBuilding.getGlobalGreatPeopleRateModifier();
					}
				}
			}
		}
		if (iBuildingMod != 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_GREATPEOPLE_BUILDINGS",
					iBuildingMod));
			szBuffer.append(NEWLINE);
			iModifier += iBuildingMod;
		}
	}
	// doc: culture level great people rate modifier
	{
        int iCultureMod = city.getCultureGreatPeopleRateModifier() * city.getCultureLevel();
        if (iCultureMod != 0)
        {
            szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_GREATPEOPLE_CULTURE_LEVEL",
                    iCultureMod));
            szBuffer.append(NEWLINE);
            iModifier += iCultureMod;
        }
	}
	{
		int iCivicMod = 0;
		FOR_EACH_ENUM(CivicOption)
		{
			if (kOwner.getCivics(eLoopCivicOption) != NO_CIVIC)
			{
				CvCivicInfo const& kCivic = GC.getInfo(kOwner.getCivics(eLoopCivicOption));
				iCivicMod += kCivic.getGreatPeopleRateModifier();
				if (kOwner.getStateReligion() != NO_RELIGION &&
					kCity.isHasReligion(kOwner.getStateReligion()))
				{
					iCivicMod += kCivic.getStateReligionGreatPeopleRateModifier();
				}
			}
		}
		if (iCivicMod != 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_GREATPEOPLE_CIVICS",
					iCivicMod));
			szBuffer.append(NEWLINE);
			iModifier += iCivicMod;
		}
	}
	FOR_EACH_ENUM2(Trait, eTrait)
	{
		if (kCity.hasTrait(eTrait))
		{
			CvTraitInfo const& kTrait = GC.getInfo(eTrait);
			int iTraitMod = kTrait.getGreatPeopleRateModifier();
			if (iTraitMod != 0)
			{
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_GREATPEOPLE_TRAIT",
						iTraitMod, kTrait.getTextKeyWide()));
				szBuffer.append(NEWLINE);
				iModifier += iTraitMod;
			}
		}
	}

	// doc: Shwedagon Paya effect
	if (city.isHasBuildingEffect(SHWEDAGON_PAYA))
	{
		if (kOwner.getCommercePercent(COMMERCE_GOLD) > 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_GREATPEOPLE_FROM_GOLD_RATE",
			        kOwner.getCommercePercent(COMMERCE_GOLD)));
			szBuffer.append(NEWLINE);
			iModifier += kOwner.getCommercePercent(COMMERCE_GOLD);
		}
	}

	// doc: Greek UP: +150% great people rate before the Medieval era
	if (city.getCivilizationType() == GREECE && kOwner.getCurrentEra() <= ERA_CLASSICAL)
	{
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_GREATPEOPLE_UNIQUE_POWER", 150));
		szBuffer.append(NEWLINE);
		iModifier += 150;
	}

	// doc: Swedish UP: +50% great people rate if city is celebrating
	if (city.getCivilizationType() == SWEDEN && city.isWeLoveTheKingDay())
	{
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_GREATPEOPLE_UNIQUE_POWER", 50));
		szBuffer.append(NEWLINE);
		iModifier += 50;
	}

	if (kOwner.isGoldenAge())
	{
		int iGoldenAgeMod = GC.getDefineINT("GOLDEN_AGE_GREAT_PEOPLE_MODIFIER");
		if (iGoldenAgeMod != 0)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_GREATPEOPLE_GOLDEN_AGE",
					iGoldenAgeMod));
			szBuffer.append(NEWLINE);
			iModifier += iGoldenAgeMod;
		}
	}
	FAssert(iModifier == iTotalGreatPeopleRateModifier); // advc
	int iModGreatPeople = (iModifier * kCity.getBaseGreatPeopleRate()) / 100;
	FAssertMsg(iModGreatPeople == kCity.getGreatPeopleRate(), "Great person rate does not match actual value");

	szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_GREATPEOPLE_FINAL", iModGreatPeople));
	//szBuffer.append(NEWLINE);
	// BUG - Building Additional Great People - start
	if (bBuildingAdditionalGreatPeople && kCity.isActiveOwned())
		setBuildingAdditionalGreatPeopleHelp(szBuffer, kCity, DOUBLE_SEPARATOR);
	// BUG - Building Additional Great People - end
}

// BUG - Building Additional Great People - start
bool CvGameTextMgr::setBuildingAdditionalGreatPeopleHelp(CvWStringBuffer
	&szBuffer, const CvCity& city, const CvWString& szStart, bool bStarted)
{
	CvWString szLabel;

	CvCivilization const& kCiv = city.getCivilization(); // advc.003w
	for (int i = 0; i < kCiv.getNumBuildings(); i++)
	{
		BuildingTypes eBuilding = kCiv.buildingAt(i);
		if (city.canConstruct(eBuilding, false, true, false))
		{
			int iChange = city.getAdditionalGreatPeopleRateByBuilding(eBuilding);
			if (iChange != 0)
			{
				if (!bStarted)
				{
					szBuffer.append(szStart);
					bStarted = true;
				}

				szLabel.Format(SETCOLR L"%s" ENDCOLR, TEXT_COLOR("COLOR_BUILDING_TEXT"), GC.getInfo(eBuilding).getDescription());
				setValueChangeHelp(szBuffer, szLabel, L": ", L"", iChange, gDLL->getSymbolID(GREAT_PEOPLE_CHAR), false, true);
			}
		}
	}

	return bStarted;
}
// BUG - Building Additional Great People - end

void CvGameTextMgr::parseGreatGeneralHelp(CvWStringBuffer &szBuffer, CvPlayer& kPlayer)
{
	szBuffer.assign(gDLL->getText("TXT_KEY_MISC_GREAT_GENERAL", kPlayer.getCombatExperience(), kPlayer.greatPeopleThreshold(true)));
}


// doc: Great Spy from spy experience
void CvGameTextMgr::parseGreatSpyHelp(CvWStringBuffer &szBuffer, CvPlayer& kPlayer)
{
	szBuffer.assign(gDLL->getText("TXT_KEY_MISC_GREAT_SPY", kPlayer.getEspionageExperience(), kPlayer.greatSpyThreshold()));
}


void CvGameTextMgr::buildCityBillboardIconString( CvWStringBuffer& szBuffer, CvCity* pCity)
{
	szBuffer.clear();
	if (pCity->isGovernmentCenter() && !(pCity->isCapital()))
		szBuffer.append(CvWString::format(L"%c", gDLL->getSymbolID(SILVER_STAR_CHAR)));
	// <advc.101>
	if (pCity->getPlot().isActiveVisible(true))
	{
		if (!pCity->isOccupation() && pCity->revoltProbability() > 0 &&
			BUGOption::isEnabled("MainInterface__RevoltChanceIcon", false))
		{
			szBuffer.append(CvWString::format(L"%c", gDLL->getSymbolID(OCCUPATION_CHAR)));
		}
	} // </advc.101>
	if (pCity->canBeSelected())
	{	// <advc.002f>
		if (pCity->AI().AI_isEmphasizeAvoidGrowth() &&
			BUGOption::isEnabled("MainInterface__AvoidGrowthIcon", false))
		{
			szBuffer.append(CvWString::format(L"%c", gDLL->getSymbolID(BAD_FOOD_CHAR)));
		} // </advc.002f>
		if (pCity->angryPopulation() > 0)
			szBuffer.append(CvWString::format(L"%c", gDLL->getSymbolID(UNHAPPY_CHAR)));
		if (pCity->healthRate() < 0)
			szBuffer.append(CvWString::format(L"%c", gDLL->getSymbolID(UNHEALTHY_CHAR)));
		// advc.076: Disabled
		/*if (gDLL->getGraphicOption(GRAPHICOPTION_CITY_DETAIL)) {
			if (GET_PLAYER(pCity->getOwner()).getNumCities() > 2) {*/
		// <advc.002f> Replacement
		if (GET_PLAYER(pCity->getOwner()).getNumCities() > 1)
		{
			bool const bTopIcons = BUGOption::isEnabled("MainInterface__TopCityIcons", false);
			if ((bTopIcons || BUGOption::isEnabled("MainInterface__TopProductionIcon", false)) &&
				pCity->getYieldRate(YIELD_PRODUCTION) >= 10 &&
				pCity->findYieldRateRank(YIELD_PRODUCTION) == 1)
			{
				szBuffer.append(CvWString::format(L"%c",
						GC.getInfo(YIELD_PRODUCTION).getChar()));
			}
			FOR_EACH_ENUM(Commerce)
			{
				bool bValid = true;
				CvString szOptionId("MainInterface__Top");
				switch(eLoopCommerce)
				{
				case COMMERCE_GOLD: szOptionId += "Gold"; break;
				case COMMERCE_RESEARCH: szOptionId += "Research"; break;
				case COMMERCE_ESPIONAGE: szOptionId += "Espionage"; break;
				default:
					bValid = false;
				}
				if (!bValid)
					continue;
				szOptionId += "Icon";
				if (pCity->getCommerceRate(eLoopCommerce) >= 10 &&
					pCity->findCommerceRateRank(eLoopCommerce) == 1 &&
					(bTopIcons || BUGOption::isEnabled(szOptionId.c_str(), false)))
				{
					szBuffer.append(CvWString::format(L"%c",
							GC.getInfo(eLoopCommerce).getChar()));
				}
			}
			if (bTopIcons || BUGOption::isEnabled("MainInterface__TopXPIcon", false))
			{
				CvCity const* pMaxXPCity = NULL;
				int iMaxXP = 0;
				FOR_EACH_CITY(pLoopCity, GET_PLAYER(pCity->getOwner()))
				{
					int iXP = pLoopCity->getProductionExperience(NO_UNIT, true);
					if (iXP > iMaxXP)
					{
						pMaxXPCity = pLoopCity;
						iMaxXP = iXP;
					}
				}
				if (iMaxXP >= 2 && pMaxXPCity == pCity)
				{
					szBuffer.append(CvWString::format(L"%c",
							gDLL->getSymbolID(GREAT_GENERAL_CHAR)));
				}
			}
			if (BUGOption::isEnabled("MainInterface__NextGPIcon", false))
			{
				CvCity const* pNextGPCity = NULL;
				int iMinTurns = MAX_INT;
				/*	Break ties in favor of pCity - so that all cities receive the
					icon when tied. Not consistent with the other icons, but seems
					(more) important for usability. */
				std::vector<CvCity const*> apCities;
				apCities.push_back(pCity);
				FOR_EACH_CITY(pLoopCity, GET_PLAYER(pCity->getOwner()))
				{
					if (pLoopCity != pCity)
						apCities.push_back(pLoopCity);
				}
				for (size_t i = 0; i < apCities.size(); i++)
				{
					CvCity const* pLoopCity = apCities[i];
					int iTurns = pLoopCity->GPTurnsLeft();
					if (iTurns >= 0 && iTurns < iMinTurns)
					{
						pNextGPCity = pLoopCity;
						iMinTurns = iTurns;
					}
				}
				if (iMinTurns < MAX_INT && pNextGPCity == pCity)
				{
					szBuffer.append(CvWString::format(L"%c",
							gDLL->getSymbolID(GREAT_PEOPLE_CHAR)));
				}
			}
		}
		if (pCity->isNoUnhappiness() &&
			BUGOption::isEnabled("MainInterface__NoUnhappyIcon", false))
		{
			szBuffer.append(CvWString::format(L"%c", gDLL->getSymbolID(HAPPY_CHAR)));
		}
		if (pCity->getUnhealthyPopulationModifier() <= -100 &&
			BUGOption::isEnabled("MainInterface__NoBadHealthIcon", false))
		{
			szBuffer.append(CvWString::format(L"%c", gDLL->getSymbolID(HEALTHY_CHAR)));
		} // </advc.002f>
		if (pCity->isConnectedToCapital() &&
			BUGOption::isEnabled("MainInterface__CityNetworkIcon", false)) // advc.002f
		{
			if (GET_PLAYER(pCity->getOwner()).countNumCitiesConnectedToCapital() > 1)
				szBuffer.append(CvWString::format(L"%c", gDLL->getSymbolID(TRADE_CHAR)));
		}
		// <advc.002f>

		// rfc: plague
		if (pCity->isHasRealBuilding(BUILDING_PLAGUE))
			szBuffer.append(CvWString::format(L"%c", gDLL->getSymbolID(PLAGUE_CHAR)));

		// BUG - Airport Icon - start
		if (BUGOption::isEnabled("MainInterface__AirportIcon", true))
		{
			BuildingClassTypes eAirportClass = (BuildingClassTypes)
					GC.getInfoTypeForString("BUILDINGCLASS_AIRPORT"
					// Mod-mods that don't have an airport should set bHideAssert:
					/*,true*/);
			if (eAirportClass != NO_BUILDINGCLASS)
			{
				BuildingTypes eAirport = pCity->getCivilization().
						getBuilding(eAirportClass);
				if (eAirport != NO_BUILDING && pCity->getNumBuilding(eAirport) > 0)
				{
					szBuffer.append(CvWString::format(L"%c",
							gDLL->getSymbolID(AIRPORT_CHAR)));
				}
			}
		} // BUG - Airport Icon - end
		// </advc.002f>
	}
	FOR_EACH_ENUM(Religion)
	{
		if (pCity->isHasReligion(eLoopReligion))
		{
			if (pCity->isHolyCity(eLoopReligion))
			{
				szBuffer.append(CvWString::format(L"%c",
						GC.getInfo(eLoopReligion).getHolyCityChar()));
			}
			else
			{
				szBuffer.append(CvWString::format(L"%c",
						GC.getInfo(eLoopReligion).getChar()));
			}
		}
	}
	FOR_EACH_ENUM2(Corporation, eLoopCorp)
	{
		if (pCity->isHeadquarters(eLoopCorp))
		{
			if (pCity->isHasCorporation(eLoopCorp))
			{
				szBuffer.append(CvWString::format(L"%c",
						GC.getInfo(eLoopCorp).getHeadquarterChar()));
			}
		}
		else
		{
			if (pCity->isActiveCorporation(eLoopCorp))
			{
				szBuffer.append(CvWString::format(L"%c",
						GC.getInfo(eLoopCorp).getChar()));
			}
		}
	}
	// doc: dirty vs clean power
	if (pCity->isActiveTeam())
	{
		if (pCity->isDirtyPower())
			szBuffer.append(CvWString::format(L"%c", gDLL->getSymbolID(POWER_CHAR)));
		else if (pCity->isPower())
			szBuffer.append(CvWString::format(L"%c", gDLL->getSymbolID(CLEAN_POWER_CHAR)));
	}
	if (pCity->isOccupation()) // XXX out this in bottom bar???
	{
		szBuffer.append(CvWString::format(L" (%c:%d)",
				gDLL->getSymbolID(OCCUPATION_CHAR), pCity->getOccupationTimer()));
	}
	// defense icon and text
	//if (!pCity->isActiveTeam()) {
	if (pCity->isVisible(getActiveTeam(), true))
	{
		int iDefenseModifier = pCity->getDefenseModifier(
				GC.getGame().selectionListIgnoreBuildingDefense());
		if (iDefenseModifier != 0)
		{
			//szBuffer.append(CvWString::format(L" %c:%s%d%%", gDLL->getSymbolID(DEFENSE_CHAR), ((iDefenseModifier > 0) ? "+" : ""), iDefenseModifier));
			// <advc.002f>
			szBuffer.append(CvWString::format(L"   " SETCOLR L"%s%d%%" ENDCOLR L"%c",
					// I've tried some other colors, but they're no easier to read.
					TEXT_COLOR("COLOR_WHITE"),
					((iDefenseModifier > 0) ? "+" : ""),
					iDefenseModifier,
					gDLL->getSymbolID(DEFENSE_CHAR))); // </advc.002f>
		}
	}
}

void CvGameTextMgr::buildCityBillboardCityNameString(CvWStringBuffer& szBuffer, CvCity* pCity)
{
	szBuffer.assign(pCity->getName());
	if (pCity->canBeSelected() &&
		gDLL->getGraphicOption(GRAPHICOPTION_CITY_DETAIL) /*&&
		pCity->foodDifference() > 0*/) // advc.189
	{
		int iTurns = pCity->getFoodTurnsLeft();
		if (abs(iTurns) > 1 || !pCity->AI().AI_isEmphasizeAvoidGrowth())
		{
			if (iTurns < MAX_INT)
			{
				szBuffer.append(CvWString::format(L" (%d)",
						/*	advc.189: Absolute value. Red color would be nice,
							but not possible here. */
						abs(iTurns)));
			}
		}
	}
}

void CvGameTextMgr::buildCityBillboardProductionString(CvWStringBuffer& szBuffer, CvCity* pCity)
{
	if (pCity->getOrderQueueLength() <= 0)
	{
		szBuffer.clear();
		return;
	}

	szBuffer.assign(pCity->getProductionName());
	if (gDLL->getGraphicOption(GRAPHICOPTION_CITY_DETAIL))
	{
		int iTurns = pCity->getProductionTurnsLeft();
		if (iTurns < MAX_INT)
			szBuffer.append(CvWString::format(L" (%d)", iTurns));
	}
}


void CvGameTextMgr::buildCityBillboardCitySizeString( CvWStringBuffer& szBuffer, CvCity* pCity, const NiColorA& kColor)
{
#define CAPARAMS(c) (int)((c).r * 255.0f), (int)((c).g * 255.0f), (int)((c).b * 255.0f), (int)((c).a * 255.0f)
	szBuffer.assign(CvWString::format(SETCOLR L"%d" ENDCOLR, CAPARAMS(kColor), pCity->getPopulation()));
#undef CAPARAMS
}

void CvGameTextMgr::getCityBillboardFoodbarColors(CvCity* pCity, std::vector<NiColorA>& aColors)
{
	aColors.resize(NUM_INFOBAR_TYPES);
	aColors[INFOBAR_STORED] = GC.getInfo((ColorTypes)(GC.getInfo(YIELD_FOOD).getColorType())).getColor();
	aColors[INFOBAR_RATE] = aColors[INFOBAR_STORED];
	aColors[INFOBAR_RATE].a = 0.5f;
	aColors[INFOBAR_RATE_EXTRA] = GC.getInfo(GC.getColorType("NEGATIVE_RATE")).getColor();
	aColors[INFOBAR_EMPTY] = GC.getInfo(GC.getColorType("EMPTY")).getColor();
}

void CvGameTextMgr::getCityBillboardProductionbarColors(CvCity* pCity, std::vector<NiColorA>& aColors)
{
	aColors.resize(NUM_INFOBAR_TYPES);
	aColors[INFOBAR_STORED] = GC.getInfo((ColorTypes)GC.getInfo(YIELD_PRODUCTION).getColorType()).getColor();
	aColors[INFOBAR_RATE] = aColors[INFOBAR_STORED];
	aColors[INFOBAR_RATE].a = 0.5f;
	aColors[INFOBAR_RATE_EXTRA] = GC.getInfo((ColorTypes)GC.getInfo(YIELD_FOOD).getColorType()).getColor();
	aColors[INFOBAR_RATE_EXTRA].a = 0.5f;
	aColors[INFOBAR_EMPTY] = GC.getInfo(GC.getColorType("EMPTY")).getColor();
}

// advc (caveat): Needs to be consistent with CvPlayer::calculateScore
void CvGameTextMgr::setScoreHelp(CvWStringBuffer &szString, PlayerTypes ePlayer)
{
	if (ePlayer == NO_PLAYER)
		return;

	CvPlayer& kPlayer = GET_PLAYER(ePlayer);

	int iPop = kPlayer.getPopScore();
	int iMaxPop = GC.getGame().getMaxPopulation();
	int iPopScore = 0;
	if (iMaxPop > 0)
	{
		iPopScore = intdiv::round( // advc.003y: round
				GC.getDefineINT("SCORE_POPULATION_FACTOR") * iPop, iMaxPop);
	}
	int iLand = kPlayer.getLandScore();
	int iMaxLand = GC.getGame().getMaxLand();
	int iLandScore = 0;
	if (iMaxLand > 0)
	{
		iLandScore = intdiv::round( // advc.003y
				GC.getDefineINT("SCORE_LAND_FACTOR") * iLand, iMaxLand);
	}
	int iTech = kPlayer.getTechScore();
	int iMaxTech = GC.getGame().getMaxTech();
	int iTechScore = 0;
	if (iMaxTech > 0) // BETTER_BTS_AI_MOD, Bugfix, 02/24/10, jdog5000
	{
		iTechScore = intdiv::round( // advc.003y
				GC.getDefineINT("SCORE_TECH_FACTOR") * iTech, iMaxTech);
	}
	int iWonders = kPlayer.getWondersScore();
	int iMaxWonders = GC.getGame().getMaxWonders();
	int iWondersScore = 0;
	if (iMaxWonders > 0) // BETTER_BTS_AI_MOD, Bugfix, 02/24/10, jdog5000
	{
		iWondersScore = intdiv::round( // advc.003y
				GC.getDefineINT("SCORE_WONDER_FACTOR") * iWonders, iMaxWonders);
	}
	int iTotalScore = iPopScore + iLandScore + iTechScore + iWondersScore;
	int iVictoryScore = kPlayer.calculateScore(true, true);
	// <advc.250c> Show leader name while in Advanced Start
	if(GC.getGame().isInAdvancedStart())
	{
		szString.append(GC.getInfo(kPlayer.getLeaderType()).getText());
		szString.append(L"\n");
	} // </advc.250c>
	if (iTotalScore == kPlayer.calculateScore())
	{	// <advc.703> Advertise the Score Tab
		if(GC.getGame().isOption(GAMEOPTION_RISE_FALL))
		{
			szString.append(gDLL->getText("TXT_KEY_RF_CIV_SCORE_BREAKDOWN",
					iPopScore, iPop, iMaxPop, iLandScore, iLand, iMaxLand,
					iTechScore, iTech, iMaxTech,
					iWondersScore, iWonders, iMaxWonders, iTotalScore));
		}
		else // </advc.703>
		{
			szString.append(gDLL->getText("TXT_KEY_SCORE_BREAKDOWN",
					iPopScore, iPop, iMaxPop, iLandScore, iLand, iMaxLand,
					iTechScore, iTech, iMaxTech, iWondersScore,
					iWonders, iMaxWonders, iTotalScore, iVictoryScore));
		}
	}
}


void CvGameTextMgr::setEventHelp(CvWStringBuffer& szBuffer,
	EventTypes eEvent, int iEventTriggeredId, PlayerTypes ePlayer)
{
	if (eEvent == NO_EVENT || ePlayer == NO_PLAYER)
		return;

	CvEventInfo& kEvent = GC.getInfo(eEvent);
	CvPlayer& kActivePlayer = GET_PLAYER(ePlayer);
	CvCivilization const& kCiv = kActivePlayer.getCivilization(); // advc.003w
	EventTriggeredData* pTriggeredData = kActivePlayer.getEventTriggered(iEventTriggeredId);

	if (pTriggeredData == NULL)
		return;

	CvCity const* pCity = kActivePlayer.getCity(pTriggeredData->m_iCityId);
	CvCity const* pOtherPlayerCity = NULL;
	CvPlot const* pPlot = GC.getMap().plot(pTriggeredData->m_iPlotX, pTriggeredData->m_iPlotY);
	CvUnit const* pUnit = kActivePlayer.getUnit(pTriggeredData->m_iUnitId);

	if (pTriggeredData->m_eOtherPlayer != NO_PLAYER)
	{
		pOtherPlayerCity = GET_PLAYER(pTriggeredData->m_eOtherPlayer).
				getCity(pTriggeredData->m_iOtherPlayerCityId);
	}

	CvWString szCity = gDLL->getText("TXT_KEY_EVENT_THE_CITY");
	if (pCity != NULL && kEvent.isCityEffect())
		szCity = pCity->getNameKey();
	else if (pOtherPlayerCity != NULL && kEvent.isOtherPlayerCityEffect())
		szCity = pOtherPlayerCity->getNameKey();

	CvWString szUnit = gDLL->getText("TXT_KEY_EVENT_THE_UNIT");
	if (pUnit != NULL)
		szUnit = pUnit->getNameKey();

	CvWString szReligion = gDLL->getText("TXT_KEY_EVENT_THE_RELIGION");
	if (pTriggeredData->m_eReligion != NO_RELIGION)
		szReligion = GC.getInfo(pTriggeredData->m_eReligion).getTextKeyWide();

	eventGoldHelp(szBuffer, eEvent, ePlayer, pTriggeredData->m_eOtherPlayer);

	eventTechHelp(szBuffer, eEvent,
			kActivePlayer.getBestEventTech(
			eEvent, pTriggeredData->m_eOtherPlayer),
			ePlayer, pTriggeredData->m_eOtherPlayer);

	if (pTriggeredData->m_eOtherPlayer != NO_PLAYER &&
		kEvent.getBonusGift() != NO_BONUS)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_EVENT_GIFT_BONUS_TO_PLAYER",
				GC.getInfo((BonusTypes)kEvent.getBonusGift()).getTextKeyWide(),
				GET_PLAYER(pTriggeredData->m_eOtherPlayer).getCivilizationShortDescription())); // rfc
	}

	if (kEvent.getHappy() != 0)
	{
		if (NO_PLAYER != pTriggeredData->m_eOtherPlayer)
		{
			if (kEvent.getHappy() > 0)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_EVENT_HAPPY_FROM_PLAYER",
						kEvent.getHappy(), kEvent.getHappy(),
						GET_PLAYER(pTriggeredData->m_eOtherPlayer).getCivilizationShortDescription())); // rfc
			}
			else
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_EVENT_HAPPY_TO_PLAYER",
						-kEvent.getHappy(), -kEvent.getHappy(),
						GET_PLAYER(pTriggeredData->m_eOtherPlayer).getCivilizationShortDescription())); // rfc
			}
		}
		else
		{
			if (kEvent.getHappy() > 0)
			{
				if (kEvent.isCityEffect() || kEvent.isOtherPlayerCityEffect())
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_EVENT_HAPPY_CITY",
							kEvent.getHappy(), szCity.GetCString()));
				}
				else
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_EVENT_HAPPY",
							kEvent.getHappy()));
				}
			}
			else
			{
				if (kEvent.isCityEffect() || kEvent.isOtherPlayerCityEffect())
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_EVENT_UNHAPPY_CITY",
							-kEvent.getHappy(), szCity.GetCString()));
				}
				else
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_EVENT_UNHAPPY",
							-kEvent.getHappy()));
				}
			}
		}
	}

	if (kEvent.getHealth() != 0)
	{
		if (NO_PLAYER != pTriggeredData->m_eOtherPlayer)
		{
			if (kEvent.getHealth() > 0)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_EVENT_HEALTH_FROM_PLAYER",
						kEvent.getHealth(), kEvent.getHealth(),
						GET_PLAYER(pTriggeredData->m_eOtherPlayer).getCivilizationShortDescription())); // rfc
			}
			else
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_EVENT_HEALTH_TO_PLAYER",
						-kEvent.getHealth(), -kEvent.getHealth(),
						GET_PLAYER(pTriggeredData->m_eOtherPlayer).getCivilizationShortDescription())); // rfc
			}
		}
		else
		{
			if (kEvent.getHealth() > 0)
			{
				if (kEvent.isCityEffect() || kEvent.isOtherPlayerCityEffect())
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_EVENT_HEALTH_CITY",
							kEvent.getHealth(), szCity.GetCString()));
				}
				else
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_EVENT_HEALTH",
							kEvent.getHealth()));
				}
			}
			else
			{
				if (kEvent.isCityEffect() || kEvent.isOtherPlayerCityEffect())
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_EVENT_UNHEALTH",
							-kEvent.getHealth(), szCity.GetCString()));
				}
				else
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_EVENT_UNHEALTH_CITY",
							-kEvent.getHealth()));
				}
			}
		}
	}

	if (kEvent.getHurryAnger() != 0)
	{
		if (kEvent.isCityEffect() || kEvent.isOtherPlayerCityEffect())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_EVENT_HURRY_ANGER_CITY",
					kEvent.getHurryAnger(), szCity.GetCString()));
		}
		else
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_EVENT_HURRY_ANGER",
					kEvent.getHurryAnger()));
		}
	}

	if (kEvent.getHappyTurns() > 0)
	{
		if (kEvent.isCityEffect() || kEvent.isOtherPlayerCityEffect())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_EVENT_TEMP_HAPPY_CITY",
					GC.getDefineINT("TEMP_HAPPY"), kEvent.getHappyTurns(),
					szCity.GetCString()));
		}
		else
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_EVENT_TEMP_HAPPY",
					GC.getDefineINT("TEMP_HAPPY"), kEvent.getHappyTurns()));
		}
	}

	if (kEvent.getFood() != 0)
	{
		if (kEvent.isCityEffect() || kEvent.isOtherPlayerCityEffect())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_EVENT_FOOD_CITY",
					kEvent.getFood(), szCity.GetCString()));
		}
		else
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_EVENT_FOOD",
					kEvent.getFood()));
		}
	}

	if (kEvent.getFoodPercent() != 0)
	{
		if (kEvent.isCityEffect() || kEvent.isOtherPlayerCityEffect())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_EVENT_FOOD_PERCENT_CITY",
					kEvent.getFoodPercent(), szCity.GetCString()));
		}
		else
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_EVENT_FOOD_PERCENT",
					kEvent.getFoodPercent()));
		}
	}

	if (kEvent.getRevoltTurns() > 0)
	{
		if (kEvent.isCityEffect() || kEvent.isOtherPlayerCityEffect())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_EVENT_REVOLT_TURNS",
					kEvent.getRevoltTurns(), szCity.GetCString()));
		}
	}

	if (kEvent.getSpaceProductionModifier() != 0)
	{
		if (kEvent.isCityEffect() || kEvent.isOtherPlayerCityEffect())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_EVENT_SPACE_PRODUCTION_CITY",
					kEvent.getSpaceProductionModifier(), szCity.GetCString()));
		}
		else
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_SPACESHIP_MOD_ALL_CITIES",
					kEvent.getSpaceProductionModifier()));
		}
	}

	if (kEvent.getMaxPillage() > 0)
	{
		if (kEvent.isCityEffect() || kEvent.isOtherPlayerCityEffect())
		{
			if (kEvent.getMaxPillage() == kEvent.getMinPillage())
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_EVENT_PILLAGE_CITY",
						kEvent.getMinPillage(), szCity.GetCString()));
			}
			else
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_EVENT_PILLAGE_RANGE_CITY",
						kEvent.getMinPillage(), kEvent.getMaxPillage(),
						szCity.GetCString()));
			}
		}
		else
		{
			if (kEvent.getMaxPillage() == kEvent.getMinPillage())
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_EVENT_PILLAGE",
						kEvent.getMinPillage()));
			}
			else
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_EVENT_PILLAGE_RANGE",
						kEvent.getMinPillage(), kEvent.getMaxPillage()));
			}
		}
	}

	FOR_EACH_ENUM(Specialist)
	{
		if (kEvent.getFreeSpecialistCount(eLoopSpecialist) <= 0)
			continue;
		if (kEvent.isCityEffect() || kEvent.isOtherPlayerCityEffect())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_EVENT_FREE_SPECIALIST",
					kEvent.getFreeSpecialistCount(eLoopSpecialist),
					GC.getInfo(eLoopSpecialist).getTextKeyWide(),
					szCity.GetCString()));
		}
	}

	if (kEvent.getPopulationChange() != 0)
	{
		if (kEvent.isCityEffect() || kEvent.isOtherPlayerCityEffect())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_EVENT_POPULATION_CHANGE_CITY",
					kEvent.getPopulationChange(), szCity.GetCString()));
		}
		else
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_EVENT_POPULATION_CHANGE",
					kEvent.getPopulationChange()));
		}
	}

	if (kEvent.getCulture() != 0)
	{
		if (kEvent.isCityEffect() || kEvent.isOtherPlayerCityEffect())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_EVENT_CULTURE_CITY",
					kEvent.getCulture(), szCity.GetCString()));
		}
		else
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_EVENT_CULTURE",
					kEvent.getCulture()));
		}
	}
	/*	<advc> Not sure if this can actually not be true,
		but let's at least not check it over and over. */
	CivilizationTypes const eActiveCiv = kActivePlayer.getCivilizationType();
	if (eActiveCiv != NO_CIVILIZATION)
	{
		if (kEvent.getUnitClass() != NO_UNITCLASS)
		{
			UnitTypes eUnit = GC.getInfo(eActiveCiv).
					getCivilizationUnits(kEvent.getUnitClass());
			if (eUnit != NO_UNIT)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_EVENT_BONUS_UNIT",
						kEvent.getNumUnits(), GC.getInfo(eUnit).getTextKeyWide()));
			}
		}
		BuildingClassTypes const eBuildingClass = (BuildingClassTypes)
				kEvent.getBuildingClass();
		if (eBuildingClass != NO_BUILDINGCLASS)
		{
			BuildingTypes eBuilding = kActivePlayer.getCivilization().
					getBuilding(eBuildingClass);
			if (eBuilding != NO_BUILDING)
			{
				if (kEvent.getBuildingChange() > 0)
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_EVENT_BONUS_BUILDING",
							GC.getInfo(eBuilding).getTextKeyWide()));
				}
				else if (kEvent.getBuildingChange() < 0)
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_EVENT_REMOVE_BUILDING",
							GC.getInfo(eBuilding).getTextKeyWide()));
				}
			}
		}
		CvWStringBuffer szTmp;
		FOR_EACH_NON_DEFAULT_PAIR(kEvent.
			getBuildingYieldChange(), BuildingClass, YieldChangeMap)
		{
			BuildingTypes eBuilding = GC.getInfo(eActiveCiv).
					getCivilizationBuildings(perBuildingClassVal.first);
			if (eBuilding == NO_BUILDING)
				continue;
			szTmp.clear();
			setYieldChangeHelp(szTmp, L"", L"", L"",
					perBuildingClassVal.second, false, false);
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_EVENT_YIELD_CHANGE_BUILDING",
					GC.getInfo(eBuilding).getTextKeyWide(), szTmp.getCString()));
		}
		FOR_EACH_NON_DEFAULT_PAIR(kEvent.
			getBuildingCommerceChange(), BuildingClass, CommerceChangeMap)
		{
			BuildingTypes eBuilding = GC.getInfo(eActiveCiv).
					getCivilizationBuildings(perBuildingClassVal.first);
			if (eBuilding == NO_BUILDING)
				continue;
			szTmp.clear();
			setCommerceChangeHelp(szTmp, L"", L"", L"",
					perBuildingClassVal.second, false, false);
			szBuffer.append(NEWLINE);
			// advc (note): It's the same text key for yield and commerce
			szBuffer.append(gDLL->getText("TXT_KEY_EVENT_YIELD_CHANGE_BUILDING",
					GC.getInfo(eBuilding).getTextKeyWide(), szTmp.getCString()));
		}
		FOR_EACH_NON_DEFAULT_PAIR(kEvent.
			getBuildingHappyChange(), BuildingClass, int)
		{
			int iHappy = perBuildingClassVal.second;
			BuildingTypes const eBuilding = kCiv.getBuilding(perBuildingClassVal.first);
			if (eBuilding == NO_BUILDING)
				continue;
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_EVENT_HAPPY_BUILDING",
					GC.getInfo(eBuilding).getTextKeyWide(), abs(iHappy),
					gDLL->getSymbolID(iHappy > 0 ? HAPPY_CHAR : UNHAPPY_CHAR)));
		}
		FOR_EACH_NON_DEFAULT_PAIR(kEvent.
			getBuildingHealthChange(), BuildingClass, int)
		{
			int iHealth = perBuildingClassVal.second;
			BuildingTypes const eBuilding = kCiv.getBuilding(perBuildingClassVal.first);
			if (eBuilding == NO_BUILDING)
				continue;
			szBuffer.append(NEWLINE);
			// advc (note): It's the same text key for happiness and health
			szBuffer.append(gDLL->getText("TXT_KEY_EVENT_HAPPY_BUILDING",
					GC.getInfo(eBuilding).getTextKeyWide(), abs(iHealth),
					gDLL->getSymbolID(iHealth > 0 ? HEALTHY_CHAR : UNHEALTHY_CHAR)));
		}
	}
	if (kEvent.getFeatureChange() > 0)
	{
		if (kEvent.getFeature() != NO_FEATURE)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_EVENT_FEATURE_GROWTH",
					GC.getInfo((FeatureTypes)kEvent.getFeature()).
					getTextKeyWide()));
		}
	}
	else if (kEvent.getFeatureChange() < 0)
	{
		if (pPlot != NULL && NO_FEATURE != pPlot->getFeatureType())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_EVENT_FEATURE_REMOVE",
					GC.getInfo(pPlot->getFeatureType()).getTextKeyWide()));
		}
	}

	if (kEvent.getImprovementChange() > 0)
	{
		if (kEvent.getImprovement() != NO_IMPROVEMENT)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_EVENT_IMPROVEMENT_GROWTH",
					GC.getInfo((ImprovementTypes)kEvent.getImprovement()).
					getTextKeyWide()));
		}
	}
	else if (kEvent.getImprovementChange() < 0)
	{
		if (pPlot != NULL && pPlot->isImproved())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_EVENT_IMPROVEMENT_REMOVE",
					GC.getInfo(pPlot->getImprovementType()).getTextKeyWide()));
		}
	}

	if (kEvent.getBonusChange() > 0)
	{
		if (kEvent.getBonus() != NO_BONUS)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_EVENT_BONUS_GROWTH",
					GC.getInfo((BonusTypes)kEvent.getBonus()).getTextKeyWide()));
		}
	}
	else if (kEvent.getBonusChange() < 0)
	{
		if (NULL != pPlot && NO_BONUS != pPlot->getBonusType())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_EVENT_BONUS_REMOVE",
					GC.getInfo(pPlot->getBonusType()).getTextKeyWide()));
		}
	}

	if (kEvent.getRouteChange() > 0)
	{
		if (kEvent.getRoute() != NO_ROUTE)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_EVENT_ROUTE_GROWTH",
					GC.getInfo((RouteTypes)kEvent.getRoute()).getTextKeyWide()));
		}
	}
	else if (kEvent.getRouteChange() < 0)
	{
		if (pPlot != NULL && pPlot->isRoute())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_EVENT_ROUTE_REMOVE",
					GC.getInfo(pPlot->getRouteType()).getTextKeyWide()));
		}
	}

	int aiYields[NUM_YIELD_TYPES];
	FOR_EACH_ENUM(Yield)
	{
		aiYields[eLoopYield] = kEvent.getPlotExtraYield(eLoopYield);
	}

	CvWStringBuffer szYield;
	setYieldChangeHelp(szYield, L"", L"", L"", aiYields, false, false);
	if (!szYield.isEmpty())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_EVENT_YIELD_CHANGE_PLOT",
				szYield.getCString()));
	}

	if (kEvent.getBonusRevealed() != NO_BONUS)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_EVENT_BONUS_REVEALED",
				GC.getInfo((BonusTypes)kEvent.getBonusRevealed()).getTextKeyWide()));
	}

	if (kEvent.getUnitExperience() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_EVENT_UNIT_EXPERIENCE",
				kEvent.getUnitExperience(), szUnit.GetCString()));
	}

	if (kEvent.isDisbandUnit() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_EVENT_UNIT_DISBAND",
				szUnit.GetCString()));
	}

	if (NO_PROMOTION != kEvent.getUnitPromotion())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_EVENT_UNIT_PROMOTION",
				szUnit.GetCString(),
				GC.getInfo((PromotionTypes)kEvent.getUnitPromotion()).
				getTextKeyWide()));
	}

	FOR_EACH_ENUM(UnitCombat)
	{
		if (kEvent.getUnitCombatPromotion(eLoopUnitCombat) != NO_PROMOTION)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_EVENT_UNIT_COMBAT_PROMOTION",
					GC.getInfo(eLoopUnitCombat).getTextKeyWide(),
					GC.getInfo((PromotionTypes)
					kEvent.getUnitCombatPromotion(eLoopUnitCombat)).
					getTextKeyWide()));
		}
	}

	for (int i = 0; i < kCiv.getNumUnits(); i++)
	{
		UnitTypes ePromotedUnit = kCiv.unitAt(i);
		UnitClassTypes ePromotedUnitClass = kCiv.unitClassAt(i);
		if (kEvent.getUnitClassPromotion(ePromotedUnitClass) != NO_PROMOTION)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_EVENT_UNIT_CLASS_PROMOTION",
					GC.getInfo(ePromotedUnit).getTextKeyWide(),
					GC.getInfo((PromotionTypes)kEvent.
					getUnitClassPromotion(ePromotedUnitClass)).getTextKeyWide()));
		}
	}

	if (kEvent.getConvertOwnCities() > 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_EVENT_CONVERT_OWN_CITIES",
				kEvent.getConvertOwnCities(), szReligion.GetCString()));
	}

	if (kEvent.getConvertOtherCities() > 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_EVENT_CONVERT_OTHER_CITIES",
				kEvent.getConvertOtherCities(), szReligion.GetCString()));
	}

	if (pTriggeredData->m_eOtherPlayer != NO_PLAYER)
	{
		if (kEvent.getAttitudeModifier() > 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_EVENT_ATTITUDE_GOOD",
					kEvent.getAttitudeModifier(),
					GET_PLAYER(pTriggeredData->m_eOtherPlayer).getCivilizationShortDescription())); // rfc
		}
		else if (kEvent.getAttitudeModifier() < 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_EVENT_ATTITUDE_BAD",
					kEvent.getAttitudeModifier(),
					GET_PLAYER(pTriggeredData->m_eOtherPlayer).getCivilizationShortDescription())); // rfc
		}
	}

	if (pTriggeredData->m_eOtherPlayer != NO_PLAYER)
	{
		TeamTypes eWorstEnemy = GET_TEAM(pTriggeredData->m_eOtherPlayer).
				AI_getWorstEnemy();
		if (eWorstEnemy != NO_TEAM)
		{
			if (kEvent.getTheirEnemyAttitudeModifier() > 0)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_EVENT_ATTITUDE_GOOD",
						kEvent.getTheirEnemyAttitudeModifier(),
						GET_TEAM(eWorstEnemy).getName().GetCString()));
			}
			else if (kEvent.getTheirEnemyAttitudeModifier() < 0)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_EVENT_ATTITUDE_BAD",
						kEvent.getTheirEnemyAttitudeModifier(),
						GET_TEAM(eWorstEnemy).getName().GetCString()));
			}
		}
	}

	if (pTriggeredData->m_eOtherPlayer != NO_PLAYER)
	{
		if (kEvent.getEspionagePoints() > 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_EVENT_ESPIONAGE_POINTS",
					kEvent.getEspionagePoints(),
					GET_PLAYER(pTriggeredData->m_eOtherPlayer).getCivilizationShortDescription())); // rfc
		}
		else if (kEvent.getEspionagePoints() < 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_EVENT_ESPIONAGE_COST",
					-kEvent.getEspionagePoints()));
		}
	}

	if (kEvent.isGoldenAge())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_EVENT_GOLDEN_AGE"));
	}

	if (kEvent.getFreeUnitSupport() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_EVENT_FREE_UNIT_SUPPORT",
				kEvent.getFreeUnitSupport()));
	}

	if (kEvent.getInflationModifier() != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_EVENT_INFLATION_MODIFIER",
				kEvent.getInflationModifier()));
	}

	if (kEvent.isDeclareWar())
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_EVENT_DECLARE_WAR",
				GET_PLAYER(pTriggeredData->m_eOtherPlayer).
				getCivilizationAdjectiveKey()));
	}

	if (kEvent.getUnitImmobileTurns() > 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_EVENT_IMMOBILE_UNIT",
				kEvent.getUnitImmobileTurns(), szUnit.GetCString()));
	}

	szBuffer.append(GC.getPythonCaller()->eventHelp(eEvent, pTriggeredData));

	CvWStringBuffer szTemp;
	FOR_EACH_ENUM(Event)
	{
		if (kEvent.getAdditionalEventTime(eLoopEvent) == 0)
		{
			if (kEvent.getAdditionalEventChance(eLoopEvent) > 0 &&
				GET_PLAYER(getActivePlayer()).canDoEvent(eLoopEvent, *pTriggeredData))
			{
				szTemp.clear();
				setEventHelp(szTemp, eLoopEvent, iEventTriggeredId, ePlayer);
				if (!szTemp.isEmpty())
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_EVENT_ADDITIONAL_CHANCE",
							kEvent.getAdditionalEventChance(eLoopEvent), L""));
					szBuffer.append(NEWLINE);
					szBuffer.append(szTemp);
				}
			}
		}
		else
		{
			szTemp.clear();
			setEventHelp(szTemp, eLoopEvent, iEventTriggeredId, ePlayer);
			if (!szTemp.isEmpty())
			{
				CvWString szDelay = gDLL->getText("TXT_KEY_EVENT_DELAY_TURNS",
						(GC.getGame().getSpeedPercent() *
						kEvent.getAdditionalEventTime(eLoopEvent)) / 100);
				if (kEvent.getAdditionalEventChance(eLoopEvent) > 0)
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_EVENT_ADDITIONAL_CHANCE",
							kEvent.getAdditionalEventChance(eLoopEvent),
							szDelay.GetCString()));
				}
				else
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_EVENT_DELAY",
							szDelay.GetCString()));
				}
				szBuffer.append(NEWLINE);
				szBuffer.append(szTemp);
			}
		}
	}

	if (kEvent.getPrereqTech() != NO_TECH)
	{
		if (!GET_TEAM(kActivePlayer.getTeam()).isHasTech((TechTypes)
			kEvent.getPrereqTech()))
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_REQUIRES_STRING",
					GC.getInfo((TechTypes)(kEvent.getPrereqTech())).getTextKeyWide()));
		}
	}

	bool bDone = false;
	while (!bDone)
	{
		bDone = true;
		if(!szBuffer.isEmpty())
		{
			wchar const* wcp = szBuffer.getCString();
			if (wcp[0] == L'\n')
			{
				CvWString tempString(&wcp[1]);
				szBuffer.clear();
				szBuffer.append(tempString);
				bDone = false;
			}
		}
	}
}

void CvGameTextMgr::eventTechHelp(CvWStringBuffer& szBuffer,
	EventTypes eEvent, TechTypes eTech,
	PlayerTypes eActivePlayer, PlayerTypes eOtherPlayer)
{
	CvEventInfo& kEvent = GC.getInfo(eEvent);

	if (eTech != NO_TECH)
	{
		if (100 == kEvent.getTechPercent())
		{
			if (NO_PLAYER != eOtherPlayer)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_EVENT_TECH_GAINED_FROM_PLAYER", GC.getInfo(eTech).getTextKeyWide(), GET_PLAYER(eOtherPlayer).getCivilizationShortDescription())); // rfc
			}
			else
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_EVENT_TECH_GAINED", GC.getInfo(eTech).getTextKeyWide()));
			}
		}
		else if (kEvent.getTechPercent() != 0)
		{
			CvTeam& kTeam = GET_TEAM(GET_PLAYER(eActivePlayer).getTeam());
			int iBeakers = (kTeam.getResearchCost(eTech) * kEvent.getTechPercent()) / 100;
			if (kEvent.getTechPercent() > 0)
			{
				iBeakers = std::min(kTeam.getResearchLeft(eTech), iBeakers);
			}
			else if (kEvent.getTechPercent() < 0)
			{
				iBeakers = std::max(kTeam.getResearchLeft(eTech) - kTeam.getResearchCost(eTech), iBeakers);
			}

			if (NO_PLAYER != eOtherPlayer)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_EVENT_TECH_GAINED_FROM_PLAYER_PERCENT", iBeakers, GC.getInfo(eTech).getTextKeyWide(), GET_PLAYER(eOtherPlayer).getCivilizationShortDescription())); // rfc
			}
			else
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_EVENT_TECH_GAINED_PERCENT", iBeakers, GC.getInfo(eTech).getTextKeyWide()));
			}
		}
	}
}

void CvGameTextMgr::eventGoldHelp(CvWStringBuffer& szBuffer, EventTypes eEvent, PlayerTypes ePlayer, PlayerTypes eOtherPlayer)
{
	CvEventInfo& kEvent = GC.getInfo(eEvent);
	CvPlayer& kPlayer = GET_PLAYER(ePlayer);

	int iGold1 = kPlayer.getEventCost(eEvent, eOtherPlayer, false);
	int iGold2 = kPlayer.getEventCost(eEvent, eOtherPlayer, true);

	if (iGold1 != 0 || iGold2 != 0)
	{
		if (iGold1 == iGold2)
		{
			if (NO_PLAYER != eOtherPlayer && kEvent.isGoldToPlayer())
			{
				if (iGold1 > 0)
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_EVENT_GOLD_FROM_PLAYER", iGold1, GET_PLAYER(eOtherPlayer).getCivilizationShortDescriptionKey())); // rfc
				}
				else
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_EVENT_GOLD_TO_PLAYER", -iGold1, GET_PLAYER(eOtherPlayer).getCivilizationShortDescriptionKey())); // rfc
				}
			}
			else
			{
				if (iGold1 > 0)
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_EVENT_GOLD_GAINED", iGold1));
				}
				else
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_EVENT_GOLD_LOST", -iGold1));
				}
			}
		}
		else
		{
			if (NO_PLAYER != eOtherPlayer && kEvent.isGoldToPlayer())
			{
				if (iGold1 > 0)
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_EVENT_GOLD_RANGE_FROM_PLAYER", iGold1, iGold2, GET_PLAYER(eOtherPlayer).getCivilizationShortDescriptionKey())); // rfc
				}
				else
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_EVENT_GOLD_RANGE_TO_PLAYER", -iGold1, -iGold2, GET_PLAYER(eOtherPlayer).getCivilizationShortDescriptionKey())); // rfc
				}
			}
			else
			{
				if (iGold1 > 0)
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_EVENT_GOLD_RANGE_GAINED", iGold1, iGold2));
				}
				else
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_EVENT_GOLD_RANGE_LOST", -iGold1, iGold2));
				}
			}
		}
	}
}

void CvGameTextMgr::setTradeRouteHelp(CvWStringBuffer &szBuffer, int iRoute, CvCity* pCity)
{
	if (pCity == NULL)
	{
		FAssertMsg(pCity != NULL, "Can this actually happen?"); // advc.test
		return;
	}
	CvCity const* pOtherCity = pCity->getTradeCity(iRoute);
	if (pOtherCity == NULL)
	{
		FAssertMsg(pCity != NULL, "Can this actually happen?"); // advc.test
		return;
	}
	szBuffer.append(pOtherCity->getName());
	int iProfit = pCity->getBaseTradeProfit(pOtherCity);
	{
		szBuffer.append(NEWLINE);
		CvWString szBaseProfit;
		szBaseProfit.Format(L"%d.%02d", iProfit/100, iProfit%100);
		szBuffer.append(gDLL->getText("TXT_KEY_TRADE_ROUTE_HELP_BASE", szBaseProfit.GetCString()));
	}
	int iTotalModifier = 100;
	{
		CvCivilization const& kCiv = pCity->getCivilization();
		for (int i = 0; i < kCiv.getNumBuildings(); i++)
		{
			BuildingTypes const eBuilding = kCiv.buildingAt(i);
			int iActive = pCity->getNumActiveBuilding(eBuilding);
			if (iActive <= 0)
				continue;
			int iModifier = iActive * GC.getInfo(eBuilding).getTradeRouteModifier();
			if (iModifier != 0)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_TRADE_ROUTE_MOD_BUILDING",
						GC.getInfo(eBuilding).getTextKeyWide(), iModifier));
				iTotalModifier += iModifier;
			}
		}
	}
	{
		int iModifier = pCity->getPopulationTradeModifier();
		if (iModifier != 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_TRADE_ROUTE_MOD_POPULATION", iModifier));
			iTotalModifier += iModifier;
		}
	}
	if (pCity->isConnectedToCapital())
	{
		int iModifier = GC.getDefineINT("CAPITAL_TRADE_MODIFIER");
		if (iModifier != 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_TRADE_ROUTE_MOD_CAPITAL", iModifier));
			iTotalModifier += iModifier;
		}
	}
	// TODO: should use continentArea
	if (!pCity->sameArea(*pOtherCity))
	{
		int iModifier = GC.getDefineINT("OVERSEAS_TRADE_MODIFIER");
		if (iModifier != 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_TRADE_ROUTE_MOD_OVERSEAS", iModifier));
			iTotalModifier += iModifier;
		}
	}
	if (pCity->getTeam() != pOtherCity->getTeam())
	{
		{
			int iModifier = pCity->getForeignTradeRouteModifier();
			if (iModifier != 0)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_TRADE_ROUTE_MOD_FOREIGN",
						iModifier));
				iTotalModifier += iModifier;
			}
		}
		{
			int iModifier = pCity->getPeaceTradeModifier(pOtherCity->getTeam());
			if (iModifier != 0)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_TRADE_ROUTE_MOD_PEACE", iModifier));
				iTotalModifier += iModifier;
			}
		}
	    // doc: Dravidian UP: +10% foreign trade yield per traded resource
	    {
            if (pCity->getCivilizationType() == DRAVIDIA)
            {
                iNewMod = 10 * (GET_PLAYER(pCity->getOwnerINLINE()).getNumTradeBonusImports(pOtherCity->getOwner()) + GET_PLAYER(pCity->getOwnerINLINE()).getNumTradeBonusExports(pOtherCity->getOwner()));
                if (iNewMod != 0)
                {
                    szBuffer.append(NEWLINE);
                    szBuffer.append(gDLL->getText("TXT_KEY_TRADE_ROUTE_MOD_TRADED_RESOURCES", iNewMod));
                    iTotalModifier += iNewMod;
                }
            }
	    }
        // Leoreth: Channel Tunnel effect
        {
            if (GET_PLAYER(pCity->getOwnerINLINE()).isHasBuildingEffect(CHANNEL_TUNNEL))
            {
                if (GET_PLAYER(pOtherCity->getOwnerINLINE()).AI_getAttitude(pCity->getOwnerINLINE()) >= ATTITUDE_FRIENDLY)
                {
                    iNewMod = 100;
                    if (iNewMod != 0)
                    {
                        szBuffer.append(NEWLINE);
                        szBuffer.append(gDLL->getText("TXT_KEY_TRADE_ROUTE_MOD_FRIENDLY_RELATION", iNewMod));
                        iTotalModifier += iNewMod;
                    }
                }
            }
		}
		// doc: distance modifier
		{
            iNewMod = pCity->getDistanceTradeModifier(pOtherCity);
            if (iNewMod != 0)
            {
                szBuffer.append(NEWLINE);
                szBuffer.append(gDLL->getText("TXT_KEY_TRADE_ROUTE_MOD_DISTANCE", iNewMod));
                iTotalModifier += iNewMod;
            }
		}
		// doc: defensive pact modifier
		{
            iNewMod = pCity->getDefensivePactTradeModifier(pOtherCity);
            if (iNewMod != 0)
            {
                szBuffer.append(NEWLINE);
                szBuffer.append(gDLL->getText("TXT_KEY_TRADE_ROUTE_MOD_DEFENSIVE_PACT", iNewMod));
                iTotalModifier += iNewMod;
            }
		}
		// doc: vassal trade modifier
		{
            iNewMod = pCity->getVassalTradeModifier(pOtherCity);
            if (iNewMod != 0)
            {
                szBuffer.append(NEWLINE);
                szBuffer.append(gDLL->getText("TXT_KEY_TRADE_ROUTE_MOD_VASSAL", iNewMod));
                iTotalModifier += iNewMod;
            }
		}
	}
	FAssert(pCity->totalTradeModifier(pOtherCity) == iTotalModifier);
	iProfit *= iTotalModifier;
	iProfit /= 10000;
	FAssert(iProfit == pCity->calculateTradeProfit(pOtherCity));
	szBuffer.append(SEPARATOR);
	/*	<advc.004> Not part of CvCity::totalTradeModifier, showing it under the
		separator hopefully makes that clear enough. Want to show this modifier
		somewhere (although it is unused in BtS and AdvCiv). But only for commerce;
		I don't think profit of other yield types has any UI support. */
	CvPlayer const& kOwner = GET_PLAYER(pCity->getOwner());
	int const iTradeYieldModifier = kOwner.getTradeYieldModifier(YIELD_COMMERCE);
	if (iTradeYieldModifier != 100)
	{
		int iTotalModifier = 0;
		{
			int iModifier = GC.getInfo(YIELD_COMMERCE).getTradeModifier();
			iTotalModifier += iModifier;
			iModifier -= 100; // 100 is normal
			if (iModifier != 0)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(CvWString::format(L"%s%d%% ",
						iModifier > 0 ? L"+" : L"", iModifier));
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_FROM"));
				szBuffer.append(L" ");
				// Well, it's sth. a mod might change, for balance reasons or so.
				CvWString szModName(GC.getModName().getName());
				szBuffer.append(szModName);
			}
		}
		{
			int iModifier = 0;
			FOR_EACH_ENUM(Trait)
			{
				if (kOwner.hasTrait(eLoopTrait))
				{
					iModifier += GC.getInfo(eLoopTrait).
							getTradeYieldModifier(YIELD_COMMERCE);
				}
			}
			if (iModifier != 0)
			{
				iTotalModifier += iModifier;
				szBuffer.append(NEWLINE);
				szBuffer.append(CvWString::format(L"%s%d%% ",
						iModifier > 0 ? L"+" : L"", iModifier));
				szBuffer.append(gDLL->getText("TXT_KEY_FROM_TRAIT"));
			}
		}
		{
			int iModifier = 0;
			FOR_EACH_ENUM(Civic)
			{
				if (kOwner.isCivic(eLoopCivic))
				{
					iModifier += GC.getInfo(eLoopCivic).
							getTradeYieldModifier(YIELD_COMMERCE);
				}
			}
			if (iModifier != 0)
			{
				iTotalModifier += iModifier;
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_YIELD_MODIFIER_CIVICS",
						iModifier));
			}
		}
		FAssert(iTotalModifier == iTradeYieldModifier);
		iProfit *= iTradeYieldModifier;
		iProfit /= 100;
	} // </advc.004>
	szBuffer.append(NEWLINE);
	szBuffer.append(gDLL->getText("TXT_KEY_TRADE_ROUTE_TOTAL", iProfit));
}

void CvGameTextMgr::setEspionageCostHelp(CvWStringBuffer &szBuffer,
	EspionageMissionTypes eMission, PlayerTypes eTargetPlayer,
	CvPlot const* pPlot, int iExtraData, CvUnit const* pSpyUnit)
{
	CvPlayer const& kPlayer = GET_PLAYER(getActivePlayer());
	CvEspionageMissionInfo const& kMission = GC.getInfo(eMission);

	//szBuffer.assign(kMission.getDescription());

	int iMissionCost = kPlayer.getEspionageMissionBaseCost(
			eMission, eTargetPlayer, pPlot, iExtraData, pSpyUnit);
	//iMissionCost *= GET_TEAM(kPlayer.getTeam()).getNumMembers(); // K-Mod
	// kekm.33/advc:
	iMissionCost = kPlayer.adjustMissionCostToTeamSize(iMissionCost, eTargetPlayer);

	if (kMission.isDestroyImprovement() && pPlot != NULL && pPlot->isImproved())
	{
		szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_HELP_DESTROY_IMPROVEMENT",
				GC.getInfo(pPlot->getImprovementType()).getTextKeyWide()));
		szBuffer.append(NEWLINE);

        // SuperSpies (TSHEEP): add Radiation Help
        if (NULL != pSpyUnit)
        {
            if (pSpyUnit->isAmphib())
            {
                szBuffer.append(NEWLINE);
                szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_HELP_DESTROY_IMPROVEMENT_RADIATION",
                    GC.getInfo(pPlot->getImprovementType()).getTextKeyWide()));
            }
        }
	}
	if (kMission.getDestroyBuildingCostFactor() > 0 && pPlot != NULL)
	{
		CvCity const* pCity = pPlot->getPlotCity();
		if (pCity != NULL)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_HELP_DESTROY_IMPROVEMENT",
					GC.getInfo((BuildingTypes)iExtraData).getTextKeyWide()));
			szBuffer.append(NEWLINE);
		}
	}
	if (kMission.getDestroyProjectCostFactor() > 0 && pPlot != NULL)
	{
		CvCity const* pCity = pPlot->getPlotCity();
		if (pCity != NULL)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_HELP_DESTROY_IMPROVEMENT",
					GC.getInfo((ProjectTypes)iExtraData).getTextKeyWide()));
			szBuffer.append(NEWLINE);
		}
	}
	if (kMission.getDestroyProductionCostFactor() > 0 && pPlot != NULL)
	{
		CvCity const* pCity = pPlot->getPlotCity();
		if (pCity != NULL)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_HELP_DESTROY_PRODUCTION",
					pCity->getProduction()));
			szBuffer.append(NEWLINE);
		}
	}
	if (kMission.getDestroyUnitCostFactor() > 0 && eTargetPlayer != NO_PLAYER)
	{
	    // SuperSpies: assassinate specialist
		int iSpecialist = iExtraData;
        if (iSpecialist != NO_SPECIALIST)
        {
            CvSpecialistInfo& kSpecialist = GC.getSpecialistInfo((SpecialistTypes)iSpecialist);
            szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_HELP_DESTROY_UNIT",
                    kSpecialist.getDescription()));
            szBuffer.append(NEWLINE);
        }
	}
	if (kMission.getBuyUnitCostFactor() > 0 && eTargetPlayer != NO_PLAYER)
	{
		int iTargetUnitID = iExtraData;
		CvUnit const* pUnit = GET_PLAYER(eTargetPlayer).getUnit(iTargetUnitID);
		if (pUnit != NULL)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_HELP_BRIBE",
					pUnit->getNameKey()));
			szBuffer.append(NEWLINE);
		}
	}

	if (kMission.getBuyCityCostFactor() > 0 && pPlot != NULL)
	{
		CvCity const* pCity = pPlot->getPlotCity();
		if (pCity != NULL)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_HELP_BRIBE",
					pCity->getNameKey()));
			szBuffer.append(NEWLINE);
		}
	}
	if (kMission.getCityInsertCultureCostFactor() > 0 && pPlot != NULL)
	{
		CvCity const* pCity = pPlot->getPlotCity();
		if (pCity != NULL && pPlot->getCulture(kPlayer.getID()) > 0)
		{
			int iCultureAmount = pCity->cultureTimes100InsertedByMission(eMission) / 100;
			szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_HELP_INSERT_CULTURE",
					pCity->getNameKey(), iCultureAmount,
					kMission.getCityInsertCultureAmountFactor()));
			szBuffer.append(NEWLINE);
		}
	}
	if (kMission.getCityPoisonWaterCounter() > 0 && pPlot != NULL)
	{
		CvCity const* pCity = pPlot->getPlotCity();
		if (pCity != NULL)
		{
		    // SuperSpies (TSHEEP): display bonus unhealthiness
		    int iPoisonWaterCounter = kMission.getCityPoisonWaterCounter();
		    if (pSpyUnit != NULL)
		    {
		        iPoisonWaterCounter *= 100 + pSpyUnit.getExtraFriendlyHeal();
		        iPoisonWaterCounter /= 100;
		    }

			szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_HELP_POISON",
					iPoisonWaterCounter,
					gDLL->getSymbolID(UNHEALTHY_CHAR), pCity->getNameKey(),
					iPoisonWaterCounter));
			szBuffer.append(NEWLINE);
		}
	}
	if (kMission.getCityUnhappinessCounter() > 0 && pPlot != NULL)
	{
		CvCity const * pCity = pPlot->getPlotCity();
		if (pCity != NULL)
		{
		    // SuperSpies (TSHEEP): display bonus unrest modifier
		    int iCityUnhappinessCounter = kMission.getCityUnhappinessCounter();
		    if (pSpyUnit != NULL)
		    {
		        iCityUnhappinessCounter *= 100 + pSpyUnit.getExtraEnemyHeal();
		        iCityUnhappinessCounter /= 100;
		    }

			szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_HELP_POISON",
					iCityUnhappinessCounter,
					gDLL->getSymbolID(UNHAPPY_CHAR), pCity->getNameKey(),
					iCityUnhappinessCounter));
			szBuffer.append(NEWLINE);
		}
	}
	if (kMission.getCityRevoltCounter() > 0 && pPlot != NULL)
	{
		CvCity const* pCity = pPlot->getPlotCity();
		if (pCity != NULL)
		{
		    int iCityRevoltCounter = kMission.getCityRevoltCounter();
		    if (pSpyUnit != NULL)
		    {
		        iCityRevoltCounter *= 100 + pSpyUnit.getExtraNeutralHeal();
		        iCityRevoltCounter /= 100;
		    }

			szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_HELP_REVOLT",
					pCity->getNameKey(), iCityRevoltCounter));
			szBuffer.append(NEWLINE);
		}
	}
	if (kMission.getStolenGoldPercent() > 0 && eTargetPlayer != NO_PLAYER)
	{
		int iNumTotalGold /* kmodx: initialize */ = 0;
		if (pPlot != NULL)
		{
			CvCity const* pCity = pPlot->getPlotCity();
			if (pCity != NULL)
			{
				/*iNumTotalGold *= pCity->getPopulation();
				iNumTotalGold /= std::max(1, GET_PLAYER(eTargetPlayer).getTotalPopulation());*/
				// K-Mod:
				iNumTotalGold = kPlayer.getEspionageGoldQuantity(eMission, eTargetPlayer, pCity);
			}
		}
		szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_HELP_STEAL_TREASURY",
				iNumTotalGold, GET_PLAYER(eTargetPlayer).getCivilizationAdjectiveKey()));
		szBuffer.append(NEWLINE);
	}
	if (kMission.getBuyTechCostFactor() > 0)
	{
		szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_HELP_STEAL_TECH",
				GC.getInfo((TechTypes)iExtraData).getTextKeyWide()));
		szBuffer.append(NEWLINE);
	}
	if (kMission.getSwitchCivicCostFactor() > 0)
	{
		if (eTargetPlayer != NO_PLAYER)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_HELP_SWITCH_CIVIC",
					GET_PLAYER(eTargetPlayer).getNameKey(),
					GC.getInfo((CivicTypes)iExtraData).getTextKeyWide()));
			szBuffer.append(NEWLINE);
		}
	}
	if (kMission.getSwitchReligionCostFactor() > 0)
	{
		if (eTargetPlayer != NO_PLAYER)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_HELP_SWITCH_CIVIC",
					GET_PLAYER(eTargetPlayer).getNameKey(),
					GC.getInfo((ReligionTypes)iExtraData).getTextKeyWide()));
			szBuffer.append(NEWLINE);
		}
	}
	if (kMission.getPlayerAnarchyCounter() > 0)
	{
		if (eTargetPlayer != NO_PLAYER)
		{
			int iTurns = (kMission.getPlayerAnarchyCounter() *
					GC.getInfo(GC.getGame().getGameSpeedType()).getAnarchyPercent()) / 100;
			szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_HELP_ANARCHY",
					GET_PLAYER(eTargetPlayer).getNameKey(), iTurns));
			szBuffer.append(NEWLINE);
		}
	}
	if (kMission.getCounterespionageNumTurns() > 0 &&
		kMission.getCounterespionageMod() > 0)
	{
		if (eTargetPlayer != NO_PLAYER)
		{
			int iTurns = (kMission.getCounterespionageNumTurns() *
					GC.getInfo(GC.getGame().getGameSpeedType()).getResearchPercent()) / 100;

            // SuperSpies (TSHEEP): display counterespionage modifier
            int iCounterEspionageMod = kMission.getCounterespionageMod();
            if (pSpyUnit != NULL)
                iCounterEspionageMod += pSpyUnit->currInterceptionProbability() * 5;

			szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_HELP_COUNTERESPIONAGE",
					iCounterEspionageMod,
					GET_PLAYER(eTargetPlayer).getCivilizationAdjectiveKey(), iTurns));
			szBuffer.append(NEWLINE);
		}
	}
	// <advc.103>
	if(kMission.isInvestigateCity() && pPlot != NULL)
	{
		CvCity const* pCity = pPlot->getPlotCity();
		if (pCity != NULL)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_HELP_INVESTIGATE",
					pCity->getNameKey()));
			szBuffer.append(NEWLINE);
		}
	}
	if (!kMission.isReturnToCapital() || kPlayer.getCapital() == NULL)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_HELP_NO_RETURN"));
		szBuffer.append(NEWLINE);
	}
	// </advc.103>
	szBuffer.append(NEWLINE);
	szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_BASE_COST", iMissionCost));

	if (kPlayer.getEspionageMissionCost(eMission, eTargetPlayer, pPlot, iExtraData, pSpyUnit) > 0)
	{
		/*	<advc.132> Normally no mission-specific cost breakdown here; mention
			the effect of own civics/ religion only to reassure the player that
			the mission is deliberately allowed when civic/ religion doesn't match. */
		if (eTargetPlayer != NO_PLAYER &&
			((kMission.getSwitchCivicCostFactor() > 0 &&
			!kPlayer.isCivic((CivicTypes)iExtraData)) ||
			(kMission.getSwitchReligionCostFactor() > 0 &&
			kPlayer.getStateReligion() != iExtraData)))
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_CIVIC_RELIGION_MOD",
					kMission.getSwitchCivicCostFactor() > 0 ?
					GC.getInfo((CivicTypes)iExtraData).getTextKeyWide() :
					GC.getInfo((ReligionTypes)iExtraData).getTextKeyWide()));
		} // </advc.132>
		int iModifier = 100;
		int iTempModifier = 0;
		CvCity const* pCity = (pPlot == NULL ? NULL : pPlot->getPlotCity());
		if (pCity != NULL && kMission.isTargetsCity())
		{
			iTempModifier = GC.getDefineINT("ESPIONAGE_CITY_POP_EACH_MOD") *
					(pCity->getPopulation() - 1);
			if (iTempModifier != 0)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_POPULATION_MOD",
						iTempModifier));
				iModifier *= 100 + iTempModifier;
				iModifier /= 100;
			}
			if (pCity->isTradeRoute(kPlayer.getID()))
			{
				iTempModifier = GC.getDefineINT("ESPIONAGE_CITY_TRADE_ROUTE_MOD");
				if (iTempModifier != 0)
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_TRADE_ROUTE_MOD",
							iTempModifier));
					iModifier *= 100 + iTempModifier;
					iModifier /= 100;
				}
			}
			ReligionTypes eReligion = kPlayer.getStateReligion();
			if (eReligion != NO_RELIGION)
			{
				iTempModifier = 0;
				if (pCity->isHasReligion(eReligion))
				{
					if (GET_PLAYER(eTargetPlayer).getStateReligion() != eReligion)
						iTempModifier += GC.getDefineINT("ESPIONAGE_CITY_RELIGION_STATE_MOD");
					if (kPlayer.hasHolyCity(eReligion))
						iTempModifier += GC.getDefineINT("ESPIONAGE_CITY_HOLY_CITY_MOD");
				}
				if (iTempModifier != 0)
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_RELIGION_MOD",
							iTempModifier));
					iModifier *= 100 + iTempModifier;
					iModifier /= 100;
				}
			}

			// City's culture affects cost
			/*iTempModifier = - (pCity->getCultureTimes100(kPlayer.getID()) * GC.getDefineINT("ESPIONAGE_CULTURE_MULTIPLIER_MOD")) / std::max(1, pCity->getCultureTimes100(eTargetPlayer) + pCity->getCultureTimes100(kPlayer.getID()));
			if (iTempModifier != 0) {
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_CULTURE_MOD", iTempModifier));
				iModifier *= 100 + iTempModifier;
				iModifier /= 100;
			}*/ // BtS (moved and changed by K-Mod)

			iTempModifier = pCity->getEspionageDefenseModifier();
			if (iTempModifier != 0)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_DEFENSE_MOD", iTempModifier));
				iModifier *= 100 + iTempModifier;
				iModifier /= 100;
			}
		}

		if (pPlot != NULL)
		{
			// K-Mod. Culture Mod. (Based on plot culture rather than city culture.)
			if (kMission.isSelectPlot() || kMission.isTargetsCity())
			{
				iTempModifier = - (pPlot->getCulture(kPlayer.getID()) * GC.getDefineINT("ESPIONAGE_CULTURE_MULTIPLIER_MOD")) / std::max(1, pPlot->getCulture(eTargetPlayer) + pPlot->getCulture(kPlayer.getID()));
				if (iTempModifier != 0)
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_CULTURE_MOD", iTempModifier));
					iModifier *= 100 + iTempModifier;
					iModifier /= 100;
				}
			}
			// K-Mod end

			// Distance mod
			int iDistance = GC.getMap().maxTypicalDistance(); // advc.140: was maxPlotDistance

			CvCity const* pOurCapital = kPlayer.getCapital();
			if (pOurCapital != NULL)
			{
				if (kMission.isSelectPlot() || kMission.isTargetsCity())
				{
					iDistance = plotDistance(pOurCapital->getX(), pOurCapital->getY(),
							pPlot->getX(), pPlot->getY());
				}
				else
				{
					CvCity const* pTheirCapital = GET_PLAYER(eTargetPlayer).getCapitalCity();
					if (pTheirCapital != NULL)
					{
						iDistance = plotDistance(pOurCapital->getX(), pOurCapital->getY(),
								pTheirCapital->getX(), pTheirCapital->getY());
					}
				}
			}
			// <advc.140> (was maxPlotDistance)
			iTempModifier = (iDistance + GC.getMap().maxTypicalDistance()) *
					GC.getDefineINT("ESPIONAGE_DISTANCE_MULTIPLIER_MOD") /
					GC.getMap().maxTypicalDistance() - 100; // </advc.140>
			if (iTempModifier != 0)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_DISTANCE_MOD", iTempModifier));
				iModifier *= 100 + iTempModifier;
				iModifier /= 100;
			}
		}

		// Spy presence mission cost alteration
		if (pSpyUnit != NULL)
		{
		    // SuperSpies (TSHEEP): display preparation modifier
			iTempModifier = -(std::min(5, pSpyUnit->getFortifyTurns() + SpyUnit->getUpgradeDiscount() / 5) *
					GC.getDefineINT("ESPIONAGE_EACH_TURN_UNIT_COST_DECREASE"));
			if (iTempModifier != 0)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_SPY_STATIONARY_MOD", iTempModifier));
				iModifier *= 100 + iTempModifier;
				iModifier /= 100;
			}
		}

        // doc: display relative espionage modifier
		// My points VS. Your points to mod cost
		/*iTempModifier = GET_TEAM(kPlayer.getTeam()).getEspionageModifier(
				TEAMID(eTargetPlayer)) - 100;
		if (iTempModifier != 0)
		{
			szBuffer.append(SEPARATOR);
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_EP_RATIO_MOD", iTempModifier));
			iModifier *= 100 + iTempModifier;
			iModifier /= 100;
		}*/

		// Counterespionage Mission Mod
		CvTeam& kTargetTeam = GET_TEAM(GET_PLAYER(eTargetPlayer).getTeam());
		if (kTargetTeam.getCounterespionageModAgainstTeam(kPlayer.getTeam()) > 0)
		{
			//iTempModifier = kTargetTeam.getCounterespionageModAgainstTeam(kPlayer.getTeam()) - 100;
			// K-Mod:
			iTempModifier = std::max(-100, kTargetTeam.getCounterespionageModAgainstTeam(kPlayer.getTeam()));
			if (iTempModifier != 0)
			{
				szBuffer.append(SEPARATOR);
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_COUNTERESPIONAGE_MOD", iTempModifier));
				iModifier *= 100 + iTempModifier;
				iModifier /= 100;
			}
		}

		FAssert(iModifier == kPlayer.getEspionageMissionCostModifier(eMission, eTargetPlayer, pPlot, iExtraData, pSpyUnit));

		iMissionCost *= iModifier;
		iMissionCost /= 100;

		FAssert(iMissionCost == kPlayer.getEspionageMissionCost(eMission, eTargetPlayer, pPlot, iExtraData, pSpyUnit));

		szBuffer.append(SEPARATOR);

		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_COST_TOTAL", iMissionCost));


		if (pSpyUnit != NULL)
		{
			int iInterceptChance =
					(pSpyUnit->getSpyInterceptPercent(GET_PLAYER(eTargetPlayer).getTeam(), true) *
					(100 + kMission.getDifficultyMod())) / 100;
			szBuffer.append(NEWLINE);
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_ESPIONAGE_CHANCE_OF_SUCCESS",
					std::min(100, std::max(0, 100 - iInterceptChance))));
		}
	}
}

void CvGameTextMgr::getTradeScreenTitleIcon(CvString& szButton, CvWidgetDataStruct& widgetData, PlayerTypes ePlayer)
{
	szButton.clear();

	ReligionTypes eReligion = GET_PLAYER(ePlayer).getStateReligion();
	if (eReligion != NO_RELIGION)
	{
		szButton = GC.getInfo(eReligion).getButton();
		widgetData.m_eWidgetType = WIDGET_HELP_RELIGION;
		widgetData.m_iData1 = eReligion;
		widgetData.m_iData2 = -1;
		widgetData.m_bOption = false;
	}
}

void CvGameTextMgr::getTradeScreenIcons(std::vector< std::pair<CvString, CvWidgetDataStruct> >& aIconInfos, PlayerTypes ePlayer)
{
	aIconInfos.clear();
	for (int i = 0; i < GC.getNumCivicOptionInfos(); i++)
	{
		CivicTypes eCivic = GET_PLAYER(ePlayer).getCivics((CivicOptionTypes)i);
		CvWidgetDataStruct widgetData;
		widgetData.m_eWidgetType = WIDGET_PEDIA_JUMP_TO_CIVIC;
		widgetData.m_iData1 = eCivic;
		widgetData.m_iData2 = -1;
		widgetData.m_bOption = false;
		aIconInfos.push_back(std::make_pair(GC.getInfo(eCivic).getButton(), widgetData));
	}

}

void CvGameTextMgr::getTradeScreenHeader(CvWString& szHeader, PlayerTypes ePlayer,
	PlayerTypes eOtherPlayer, bool bAttitude)
{
	CvPlayerAI const& kPlayer = GET_PLAYER(ePlayer);
	szHeader.Format(L"%s - %s", CvWString(kPlayer.getName()).GetCString(),
			CvWString(kPlayer.getCivilizationDescription()).GetCString());
	if (bAttitude)
	{
		szHeader += CvWString::format(L" (%s)", GC.getInfo(
				kPlayer.AI_getAttitude(eOtherPlayer)).getDescription());
	}
}
// BULL - Finance Advisor - start
void CvGameTextMgr::buildFinanceSpecialistGoldString(CvWStringBuffer& szBuffer,
	PlayerTypes ePlayer)
{
	if(ePlayer == NO_PLAYER)
		return;
	CvPlayer const& kPlayer = GET_PLAYER(ePlayer);
	EagerEnumMap<SpecialistTypes,int> aiSpecialistCounts;
	FOR_EACH_CITY(pCity, kPlayer)
	{
		if (!pCity->isDisorder())
		{
			FOR_EACH_ENUM(Specialist)
			{
				aiSpecialistCounts.add(eLoopSpecialist,
						pCity->getSpecialistCount(eLoopSpecialist) +
						pCity->getFreeSpecialistCount(eLoopSpecialist));
			}
		}
	}
	//bool bFirst = true; // advc.086
	int iTotal = 0;
	FOR_EACH_ENUM(Specialist)
	{
		int iGold = aiSpecialistCounts.get(eLoopSpecialist) *
				kPlayer.specialistCommerce(eLoopSpecialist, COMMERCE_GOLD);
		if (iGold != 0)
		{
			/*if(bFirst) {
				szBuffer.append(NEWLINE);
				bFirst = false;
			}*/
			szBuffer.append(gDLL->getText("TXT_KEY_BUG_FINANCIAL_ADVISOR_SPECIALIST_GOLD",
					iGold, aiSpecialistCounts.get(eLoopSpecialist),
					GC.getInfo(eLoopSpecialist).getDescription()));
			szBuffer.append(NEWLINE); // advc.086
			iTotal += iGold;
		}
	}
	szBuffer.append(gDLL->getText(
			"TXT_KEY_BUG_FINANCIAL_ADVISOR_SPECIALIST_TOTAL_GOLD", iTotal));
}

void CvGameTextMgr::buildDomesticTradeString(CvWStringBuffer& szBuffer, PlayerTypes ePlayer)
{
	//buildTradeString(szBuffer, ePlayer, NO_PLAYER, true, false, false);
	// <advc.086>
	if(ePlayer == NO_PLAYER)
		return;
	int iDummy1 = 0, iDummy2 = 0;
	int iDomesticRoutes = 0, iDomesticYield = 0;
	GET_PLAYER(ePlayer).calculateTradeTotals(YIELD_COMMERCE, iDomesticYield, iDomesticRoutes,
			iDummy1, iDummy2, NO_PLAYER);
	if(iDomesticRoutes > 1)
	{
		szBuffer.assign(gDLL->getText("TXT_KEY_BUG_FINANCIAL_ADVISOR_DOMESTIC_TRADE",
				iDomesticYield, iDomesticRoutes));
	} // </advc.086>
}

void CvGameTextMgr::buildForeignTradeString(CvWStringBuffer& szBuffer, PlayerTypes ePlayer)
{
	//buildTradeString(szBuffer, ePlayer, NO_PLAYER, false, true, false);
	// <advc.086>
	if(ePlayer == NO_PLAYER)
		return;
	int iDummy1 = 0, iDummy2 = 0;
	int iForeignRoutes = 0, iForeignYield = 0;
	GET_PLAYER(ePlayer).calculateTradeTotals(YIELD_COMMERCE, iDummy1, iDummy2,
			iForeignYield, iForeignRoutes, NO_PLAYER);
	if(iForeignRoutes > 1)
	{
		szBuffer.assign(gDLL->getText("TXT_KEY_BUG_FINANCIAL_ADVISOR_FOREIGN_TRADE",
				iForeignYield, iForeignRoutes));
	} // </advc.086>
} // BULL - Finance Advisor - end
// BULL - Trade Hover - start  // advc: _MOD_FRACTRADE removed
void CvGameTextMgr::buildTradeString(CvWStringBuffer& szBuffer, PlayerTypes ePlayer,
	PlayerTypes eWithPlayer, bool bDomestic, bool bForeign, bool bHeading)
{
	if(ePlayer == NO_PLAYER)
		return;
	CvPlayer const& kPlayer = GET_PLAYER(ePlayer);
	if(bHeading)
	{
		if(ePlayer == eWithPlayer)
			szBuffer.append(gDLL->getText("TXT_KEY_BUG_DOMESTIC_TRADE_HEADING"));
		else if(eWithPlayer != NO_PLAYER)
		{
			CvPlayer const& kWithPlayer = GET_PLAYER(eWithPlayer);
			if(kPlayer.canHaveTradeRoutesWith(eWithPlayer))
			{
				szBuffer.append(gDLL->getText("TXT_KEY_BUG_FOREIGN_TRADE_HEADING",
						// advc: 2nd param takes up too much room
						kWithPlayer.getNameKey()/*, kWithPlayer.getCivilizationShortDescription()*/));
			}
			else
			{
				szBuffer.append(gDLL->getText("TXT_KEY_BUG_CANNOT_TRADE_HEADING",
						kWithPlayer.getNameKey()/*, kWithPlayer.getCivilizationShortDescription()*/));
			}
		}
		else szBuffer.append(gDLL->getText("TXT_KEY_BUG_TRADE_HEADING"));
		//szBuffer.append(NEWLINE); // advc.087: removed
	}

	if(eWithPlayer != NO_PLAYER)
	{
		bDomestic = (ePlayer == eWithPlayer);
		bForeign = (ePlayer != eWithPlayer);
		if(bForeign && !kPlayer.canHaveTradeRoutesWith(eWithPlayer))
		{
			CvPlayer const& kWithPlayer = GET_PLAYER(eWithPlayer);
			bool bCanTrade = true;
			if(!kWithPlayer.isAlive())
			{
				szBuffer.append(gDLL->getText("TXT_KEY_BUG_CANNOT_TRADE_DEAD"));
				return;
			}
			if(!kPlayer.canTradeNetworkWith(eWithPlayer))
			{
				szBuffer.append(gDLL->getText("TXT_KEY_BUG_CANNOT_TRADE_NETWORK_NOT_CONNECTED"));
				bCanTrade = false;
			}
			if(!GET_TEAM(kPlayer.getTeam()).isFreeTrade(kWithPlayer.getTeam()))
			{
				szBuffer.append(gDLL->getText("TXT_KEY_BUG_CANNOT_TRADE_CLOSED_BORDERS"));
				bCanTrade = false;
			}
			if(kPlayer.isNoForeignTrade())
			{
				szBuffer.append(gDLL->getText("TXT_KEY_BUG_CANNOT_TRADE_FOREIGN_YOU"));
				bCanTrade = false;
			}
			if(kWithPlayer.isNoForeignTrade())
			{
				szBuffer.append(gDLL->getText("TXT_KEY_BUG_CANNOT_TRADE_FOREIGN_THEM"));
				bCanTrade = false;
			}
			// <advc.124>
			bool bAnyCityKnown = false;
			FOR_EACH_CITY(pLoopCity, kWithPlayer)
			{
				if(pLoopCity->isRevealed(kPlayer.getTeam()))
				{
					bAnyCityKnown = true;
					break;
				}
			}
			if(!bAnyCityKnown)
			{
				szBuffer.append(gDLL->getText("TXT_KEY_BUG_CANNOT_TRADE_NO_KNOWN_CITIES"));
				bCanTrade = false;
			} // </advc.124>
			if (!bCanTrade)
				return;
		}
	}
	int iDomesticYield = 0;
	int iDomesticRoutes = 0;
	int iForeignYield = 0;
	int iForeignRoutes = 0;
	kPlayer.calculateTradeTotals(YIELD_COMMERCE, iDomesticYield, iDomesticRoutes,
			iForeignYield, iForeignRoutes, eWithPlayer);
	int iTotalYield = 0;
	int iTotalRoutes = 0;
	if(bDomestic)
	{
		iTotalYield += iDomesticYield;
		iTotalRoutes += iDomesticRoutes;
	}
	if(bForeign)
	{
		iTotalYield += iForeignYield;
		iTotalRoutes += iForeignRoutes;
	}
	CvWString szYield;
	szYield.Format(L"%d", iTotalYield);
	/*szBuffer.append(gDLL->getText("TXT_KEY_BUG_TOTAL_TRADE_YIELD", szYield.GetCString()));
	szBuffer.append(gDLL->getText("TXT_KEY_BUG_TOTAL_TRADE_ROUTES", iTotalRoutes));
	if(iTotalRoutes > 0) {
		int iAverage = 100 * iTotalYield / iTotalRoutes;
		CvWString szAverage;
		szAverage.Format(L"%d.%02d", iAverage / 100, iAverage % 100);
		szBuffer.append(gDLL->getText("TXT_KEY_BUG_AVERAGE_TRADE_YIELD", szAverage.GetCString()));
	}*/
	// <advc.086> Shorter:
	szBuffer.append(NEWLINE);
	szBuffer.append(gDLL->getText("TXT_KEY_BUG_COMMERCE_FROM_ROUTES", iTotalYield, iTotalRoutes));
	// </advc.086>
} // BULL - Trade Hover - end
// BULL - Leaderhead Relations - start
// Displays the relations between two leaders only. This is used by the F4:GLANCE and F5:SIT-REP tabs.
void CvGameTextMgr::parseLeaderHeadRelationsHelp(CvWStringBuffer &szBuffer,
	PlayerTypes eThisPlayer, PlayerTypes eOtherPlayer)
{
	if(eThisPlayer == NO_PLAYER)
		return;
	if(eOtherPlayer == NO_PLAYER)
	{
		parseLeaderHeadHelp(szBuffer, eThisPlayer, NO_PLAYER);
		return;
	}
	szBuffer.append(CvWString::format(L"%s", GET_PLAYER(eThisPlayer).getName()));
	parsePlayerTraits(szBuffer, eThisPlayer);
	//szBuffer.append(NEWLINE); // advc: removed
	PlayerTypes eActivePlayer = getActivePlayer();
	TeamTypes eThisTeam = GET_PLAYER(eThisPlayer).getTeam();
	CvTeam const& kThisTeam = GET_TEAM(eThisTeam);
	if(eThisPlayer != eOtherPlayer && kThisTeam.isHasMet(TEAMID(eOtherPlayer)))
	{
		// advc: K-Mod keeps this secret
		//getEspionageString(szBuffer, eThisPlayer, eOtherPlayer);
		getAttitudeString(szBuffer, eThisPlayer, eOtherPlayer);
		getActiveDealsString(szBuffer, eThisPlayer, eOtherPlayer);
		if(eOtherPlayer == eActivePlayer)
			getActiveTeamRelationsString(szBuffer, eThisTeam);
		else getOtherRelationsString(szBuffer, eThisPlayer, eOtherPlayer);
	}
	else getAllRelationsString(szBuffer, eThisTeam);
} // BULL - Leaderhead Relations - end
// BUG - Food Rate Hover - start
/*
	+14 from Worked Tiles
	+2 from Specialists
	+5 from Corporations
	+1 from Buildings
	----------------------- |
	Base Food Produced: 22  |-- only if there are modifiers
	+25% from Buildings     |
	-----------------------
	Total Food Produced: 27
	=======================
	+16 for Population
	+2 for Health
	-----------------------
	Total Food Consumed: 18
	=======================
	Net Food: +9            or
	Net Food for Settler: 9
	=======================
	* Lighthouse: +3
	* Supermarket: +1
*/
void CvGameTextMgr::setFoodHelp(CvWStringBuffer &szBuffer, CvCity const& kCity)
{
	CvYieldInfo const& kFood = GC.getInfo(YIELD_FOOD);
	int iBaseRate = 0;
	bool bSimple = true; // advc.087

	// Worked Tiles
	int iTileFood = 0;
	for (WorkingPlotIter it(kCity); it.hasNext(); ++it)
	{
		iTileFood += it->getYield(YIELD_FOOD);
	}
	if(iTileFood != 0)
	{
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_WORKED_TILES_YIELD",
				iTileFood, kFood.getChar()));
		iBaseRate += iTileFood;
	}
	// Trade
	int iTradeFood = kCity.getTradeYield(YIELD_FOOD);
	if(iTradeFood != 0)
	{
		bSimple = false; // advc.087
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_SPECIALIST_COMMERCE",
				iTradeFood, kFood.getChar(), L"TXT_KEY_HEADING_TRADEROUTE_LIST"));
		iBaseRate += iTradeFood;
	}
	// Specialists
	int iSpecialistFood = 0;
	for(int i = 0; i < GC.getNumSpecialistInfos(); i++)
	{
		iSpecialistFood += GET_PLAYER(kCity.getOwner()).specialistYield(
				(SpecialistTypes)i, YIELD_FOOD) *
				(kCity.getSpecialistCount((SpecialistTypes)i) +
				kCity.getFreeSpecialistCount((SpecialistTypes)i));
	}
	if(iSpecialistFood != 0)
	{
		bSimple = false; // advc.087
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_SPECIALIST_COMMERCE",
				iSpecialistFood, kFood.getChar(), L"TXT_KEY_CONCEPT_SPECIALISTS"));
		iBaseRate += iSpecialistFood;
	}
	// Corporations
	int iCorporationFood = kCity.getCorporationYield(YIELD_FOOD);
	if(iCorporationFood != 0)
	{
		bSimple = false; // advc.087
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_CORPORATION_COMMERCE",
				iCorporationFood, kFood.getChar()));
		iBaseRate += iCorporationFood;
	}
	// Buildings
	int iBuildingFood = 0;
	for(int i = 0; i < GC.getNumBuildingInfos(); i++)
	{
		int iCount = kCity.getNumActiveBuilding((BuildingTypes)i);
		if(iCount > 0)
		{
			CvBuildingInfo& kBuilding = GC.getInfo((BuildingTypes)i);
			iBuildingFood += iCount * (kBuilding.getYieldChange(YIELD_FOOD) +
					kCity.getBuildingYieldChange(kBuilding.getBuildingClassType(), YIELD_FOOD));
		}
	}
	if(iBuildingFood != 0)
	{
		bSimple = false; // advc.087
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_BUILDING_COMMERCE",
				iBuildingFood, kFood.getChar()));
		iBaseRate += iBuildingFood;
	}
	// Base and modifiers (only if there are modifiers since total is always shown)
	if(kCity.getBaseYieldRateModifier(YIELD_FOOD) != 100)
	{
		bSimple = false; // advc.087
		szBuffer.append(SEPARATOR);
		szBuffer.append(NEWLINE);
		setYieldHelp(szBuffer, kCity, YIELD_FOOD); // shows Base Food and lists all modifiers
	}
	else szBuffer.append(NEWLINE);
	// Total Produced
	int iBaseModifier = kCity.getBaseYieldRateModifier(YIELD_FOOD);
	int iRate = iBaseRate;
	if(iBaseModifier != 100)
	{
		bSimple = false; // advc.087
		iRate *= iBaseModifier;
		iRate /= 100;
	}
	szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_TOTAL_FOOD_PRODUCED", iRate));
	// ==========================
	szBuffer.append(DOUBLE_SEPARATOR);

	int iFoodConsumed = 0; // Eaten
	int iEatenFood = kCity.getPopulation() * GC.getFOOD_CONSUMPTION_PER_POPULATION();
	if(iEatenFood != 0)
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_EATEN_FOOD", iEatenFood));
		iFoodConsumed += iEatenFood;
	}
	// Health
	int iSpoiledFood = - kCity.healthRate();
	if (iSpoiledFood != 0)
	{
		bSimple = false; // advc.087
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_SPOILED_FOOD", iSpoiledFood));
		iFoodConsumed += iSpoiledFood;
	}
	// Total Consumed
	szBuffer.append(NEWLINE);
	szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_TOTAL_FOOD_CONSUMED", iFoodConsumed));
	// ==========================
	szBuffer.append(DOUBLE_SEPARATOR NEWLINE);
	iRate -= iFoodConsumed;
	// Production
	if(kCity.isFoodProduction() && iRate > 0)
	{
		//bSimple = false; // advc.087
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_NET_FOOD_PRODUCTION",
				iRate, kCity.getProductionNameKey()));
	}
	else
	{
		// cannot starve a size 1 city with no food in
		if(iRate < 0 && kCity.getPopulation() == 1 && kCity.getFood() == 0)
		{
			bSimple = false; // advc.087
			iRate = 0;
		} // <advc.087>
		if(bSimple) // Overwrite all the text appended so far
		{
			szBuffer.assign(gDLL->getText("TXT_KEY_MISC_HELP_WORKED_TILES_EATEN",
					iTileFood, iEatenFood));
			szBuffer.append(SEPARATOR);
			szBuffer.append(NEWLINE);
		} // </advc.087>
		// Net Food
		if(iRate > 0)
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_NET_FOOD_GROW", iRate));
		else if (iRate < 0)
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_NET_FOOD_SHRINK", iRate));
		else szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_NET_FOOD_STAGNATE"));
	}
	// BULL - Building Additional Food - start
	if(kCity.isActiveOwned() &&
		(BUGOption::isEnabled("MiscHover__BuildingAdditionalFood", false) || GC.altKey()))
	{
		// ==========================
		setBuildingAdditionalYieldHelp(szBuffer, kCity, YIELD_FOOD, DOUBLE_SEPARATOR);
	} // BULL - Building Additional Food - end
} // BULL - Food Rate Hover - end
// advc.154:
void CvGameTextMgr::setCycleUnitHelp(CvWStringBuffer &szBuffer,
	bool bWorkers, CvUnit const& kUnit)
{
	CvWString szHotKey(GC.getInfo(bWorkers ?
			CONTROL_CYCLEWORKER : CONTROL_CYCLEUNIT_ALT).
			getHotKeyShortDesc());
	int const iGroupUnits = kUnit.getGroup()->getNumUnits();
	bool const bSingular = (iGroupUnits == 1);
	if (!bWorkers && bSingular)
	{
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_CYCLE_UNIT",
				szHotKey.c_str(), kUnit.getNameKey()));
	}
	else if (bWorkers && bSingular)
	{
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_CYCLE_WORKER",
				kUnit.getNameKey(), szHotKey.c_str()));
	}
	else if (!bWorkers)
	{
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_CYCLE_UNIT_GROUP",
				szHotKey.c_str(), kUnit.getNameKey(), iGroupUnits));
	}
	else
	{
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_CYCLE_WORKER_GROUP",
				kUnit.getNameKey(), szHotKey.c_str(), iGroupUnits));
	}
}

// advc.154:
void CvGameTextMgr::setUnselectUnitHelp(CvWStringBuffer &szBuffer)
{
	CvWString szHotKey(GC.getInfo(CONTROL_UNSELECT_ALL).getHotKeyShortDesc());
	szBuffer.append(gDLL->getText("TXT_KEY_ACTION_UNSELECT_ALL_HELP", szHotKey.c_str()));
}

õvoid CvGameTextMgr::getGlobeLayerName(GlobeLayerTypes eType, int iOption, CvWString& strName)
{
	switch (eType)
	{
	case GLOBE_LAYER_STRATEGY:
		switch(iOption)
		{
		case 0:
			strName = gDLL->getText("TXT_KEY_GLOBELAYER_STRATEGY_VIEW");
			break;
		case 1:
			strName = gDLL->getText("TXT_KEY_GLOBELAYER_STRATEGY_NEW_LINE");
			break;
		case 2:
			strName = gDLL->getText("TXT_KEY_GLOBELAYER_STRATEGY_NEW_SIGN");
			break;
		case 3:
			strName = gDLL->getText("TXT_KEY_GLOBELAYER_STRATEGY_DELETE");
			break;
		case 4:
			strName = gDLL->getText("TXT_KEY_GLOBELAYER_STRATEGY_DELETE_LINES");
			break;
		}
		break;
	case GLOBE_LAYER_UNIT:
		switch(iOption)
		{
		case SHOW_ALL_MILITARY:
			strName = gDLL->getText("TXT_KEY_GLOBELAYER_UNITS_ALLMILITARY");
			break;
		case SHOW_TEAM_MILITARY:
			strName = gDLL->getText("TXT_KEY_GLOBELAYER_UNITS_TEAMMILITARY");
			break;
		case SHOW_ENEMIES_IN_TERRITORY:
			strName = gDLL->getText("TXT_KEY_GLOBELAYER_UNITS_ENEMY_TERRITORY_MILITARY");
			break;
		case SHOW_ENEMIES:
			strName = gDLL->getText("TXT_KEY_GLOBELAYER_UNITS_ENEMYMILITARY");
			break;
		case SHOW_PLAYER_DOMESTICS:
			strName = gDLL->getText("TXT_KEY_GLOBELAYER_UNITS_DOMESTICS");
			break;
		}
		break;
	case GLOBE_LAYER_RESOURCE:
		switch(iOption)
		{
		case SHOW_ALL_RESOURCES:
			strName = gDLL->getText("TXT_KEY_GLOBELAYER_RESOURCES_EVERYTHING");
			break;
		case SHOW_STRATEGIC_RESOURCES:
			strName = gDLL->getText("TXT_KEY_GLOBELAYER_RESOURCES_GENERAL");
			break;
		case SHOW_HAPPY_RESOURCES:
			strName = gDLL->getText("TXT_KEY_GLOBELAYER_RESOURCES_LUXURIES");
			break;
		case SHOW_HEALTH_RESOURCES:
			strName = gDLL->getText("TXT_KEY_GLOBELAYER_RESOURCES_FOOD");
			break;
		}
		break;
	case GLOBE_LAYER_RELIGION:
		strName = GC.getInfo((ReligionTypes) iOption).getDescription();
		break;
	case GLOBE_LAYER_CULTURE:
	case GLOBE_LAYER_TRADE:
		// these have no sub-options
		strName.clear();
		break;
	}
}

void CvGameTextMgr::getPlotHelp(CvPlot* pMouseOverPlot,
	CvCity* pCity, CvPlot* pFlagPlot, bool bAlt, CvWStringBuffer& strHelp)
{
	TeamTypes const eActiveTeam = getActiveTeam();
	CvDLLInterfaceIFaceBase& kUI = gDLL->UI();
	if (kUI.isCityScreenUp())
	{
		if (pMouseOverPlot != NULL)
		{
			CvCity* pHeadSelectedCity = kUI.getHeadSelectedCity();
			if (pHeadSelectedCity != NULL &&
				pMouseOverPlot->getWorkingCity() == pHeadSelectedCity &&
				pMouseOverPlot->isRevealed(eActiveTeam, true))
			{
				setPlotHelp(strHelp, *pMouseOverPlot);
			}
		}
	}
	else
	{
		if (pCity != NULL)
			setCityBarHelp(strHelp, *pCity);
		else if (pFlagPlot != NULL)
			setPlotListHelp(strHelp, *pFlagPlot, false, true);
		/*	<advc.010> Convenient to generate capture help along with
			combat help, but I want to show capture help a little later. */
		bool bCaptureHelp = false;
		CvWStringBuffer szCombatHelp; // </advc.010>
		if (strHelp.isEmpty() && pMouseOverPlot != NULL)
		{
			if (pMouseOverPlot == kUI.getGotoPlot() ||
				// K-Mod. (Alt does something else in cheat mode)
				(bAlt && //gDLL->getChtLvl() == 0))
				!GC.getGame().isDebugMode())) // advc.135c
			{
				if (pMouseOverPlot->isActiveVisible(true))
				{
					//setCombatPlotHelp(strHelp, pMouseOverPlot);
					// <advc.010>
					bCaptureHelp = setCombatPlotHelp(szCombatHelp, pMouseOverPlot);
					if (!bCaptureHelp)
						strHelp.append(szCombatHelp); // </advc.010>
				}
			}
		}
		if (strHelp.isEmpty() && pMouseOverPlot != NULL &&
			pMouseOverPlot->isRevealed(eActiveTeam, true))
		{
			if (pMouseOverPlot->isActiveVisible(true))
			{
				setPlotListHelp(strHelp, *pMouseOverPlot, true, false);
				if (!strHelp.isEmpty())
					strHelp.append(NEWLINE);
			}
			// <advc.010>
			if (bCaptureHelp && !szCombatHelp.isEmpty())
			{
				strHelp.append(szCombatHelp);
				strHelp.append(NEWLINE);
			} // </advc.010>
			setPlotHelp(strHelp, *pMouseOverPlot);
		}

		InterfaceModeTypes eInterfaceMode = kUI.getInterfaceMode();
		// <advc.057>
		if (pMouseOverPlot != NULL &&
			(eInterfaceMode == INTERFACEMODE_GO_TO || pMouseOverPlot == kUI.getGotoPlot()))
		{
			CvUnit const* pSelectedUnit = kUI.getHeadSelectedUnit();
			if (!bAlt && pSelectedUnit != NULL && pMouseOverPlot->isRevealed(eActiveTeam) &&
				pMouseOverPlot->getTeam() != eActiveTeam)
			{
				TerrainTypes const eTerrain = pMouseOverPlot->getTerrainType();
				// Check if any selected unit is unable to enter eTerrain
				bool bCanAllEnter = true;
				CvPlot const& kUnitPlot = pSelectedUnit->getPlot();
				FOR_EACH_UNIT_IN(pUnit, kUnitPlot)
				{
					if (!pUnit->IsSelected())
						continue;
					CvUnitInfo const& kInfo = pUnit->getUnitInfo();
					if (pMouseOverPlot->isImpassable() && !kInfo.canMoveImpassable())
						continue;
					if (!kInfo.getTerrainImpassable(eTerrain))
						continue;
					bCanAllEnter = false;
					TechTypes eReqTech = kInfo.getTerrainPassableTech(eTerrain);
					if (eReqTech != NO_TECH && !GET_TEAM(eActiveTeam).isHasTech(eReqTech) &&
						GC.getInfo(eReqTech).getEra() -
						GET_PLAYER(pSelectedUnit->getOwner()).getCurrentEra() <=
						GC.getDefineINT("SHOW_IMPASSABLE_TECH_ERA_DIFFERENCE"))
					{
						if (!strHelp.isEmpty())
							strHelp.append(NEWLINE);
						strHelp.append(gDLL->getText("TXT_KEY_REQUIRES_TECH_TO_ENTER",
								GC.getInfo(eReqTech).getDescription()));
						return;
					}
				}
				if (!bCanAllEnter && // and no tech will allow it either
					// If it's too far off the coast, then it can't be owned.
					(!pMouseOverPlot->isWater() || pMouseOverPlot->isPotentialCityWork()))
				{
					if (!strHelp.isEmpty())
						strHelp.append(NEWLINE);
					strHelp.append(gDLL->getText("TXT_KEY_REQUIRES_OWNERSHIP_TO_ENTER"));
				}
				return;
			}
		} // </advc.057>
		if (eInterfaceMode != INTERFACEMODE_SELECTION)
		{
			CvWString szTempBuffer;
			szTempBuffer.Format(SETCOLR L"%s" ENDCOLR NEWLINE, TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
					GC.getInfo(eInterfaceMode).getDescription());
			// <advc> Cut from getNukePlotHelp
			CvUnit* pHeadSelectedUnit = gDLL->UI().getHeadSelectedUnit();
			if (pMouseOverPlot != NULL && pHeadSelectedUnit != NULL) // </advc>
			{
				switch (eInterfaceMode)
				{
				case INTERFACEMODE_REBASE:
					getRebasePlotHelp(*pMouseOverPlot, *pHeadSelectedUnit, szTempBuffer);
					break;
				case INTERFACEMODE_NUKE:
					getNukePlotHelp(*pMouseOverPlot, *pHeadSelectedUnit, szTempBuffer);
					szTempBuffer.append(NEWLINE); // kekm.7
					break;
				// <advc.004c>
				case INTERFACEMODE_AIRBOMB:
					getAirBombPlotHelp(*pMouseOverPlot, *pHeadSelectedUnit, szTempBuffer);
					break;
				case INTERFACEMODE_AIRSTRIKE:
					getAirStrikePlotHelp(*pMouseOverPlot, *pHeadSelectedUnit, szTempBuffer);
					break;
				case INTERFACEMODE_PARADROP:
					getParadropPlotHelp(*pMouseOverPlot, *pHeadSelectedUnit, szTempBuffer);
					break;
				// </advc.004c>
				}
			}
			szTempBuffer += strHelp.getCString();
			strHelp.assign(szTempBuffer);
		}
	}
}

void CvGameTextMgr::getRebasePlotHelp(CvPlot const& kPlot,
	CvUnit& kHeadSelectedUnit, CvWString& szHelp)
{
	CvCity const* pCity = kPlot.getPlotCity();
	if (pCity == NULL)
		return;
	//if (!pPlot->isFriendlyCity(*pHeadSelectedUnit, true))
	if (!kHeadSelectedUnit.isRevealedPlotValid(kPlot)) // advc
		return;
	TeamTypes const eActiveTeam = getActiveTeam();
	int const iUnits = pCity->getPlot().countNumAirUnits(eActiveTeam);
	bool const bFull = (iUnits >= pCity->getAirUnitCapacity(eActiveTeam));
	if (bFull)
		szHelp += CvWString::format(SETCOLR, TEXT_COLOR("COLOR_WARNING_TEXT"));
	// advc.187: Handled by setPlotHelp now
	/*szHelp += NEWLINE + gDLL->getText("TXT_KEY_CITY_BAR_AIR_UNIT_CAPACITY",
			iUnits, pCity->getAirUnitCapacity(eActiveTeam));*/
	if (bFull)
		szHelp += ENDCOLR;
	szHelp += NEWLINE;
}

void CvGameTextMgr::getNukePlotHelp(CvPlot const& kPlot,
	CvUnit& kNuke, CvWString& szHelp)
{
	if (kNuke.canNukeAt(kNuke.getPlot(), kPlot.getX(), kPlot.getY(),
		kNuke.getTeam())) // kekm.7 (advc)
	{	// <advc.650>
		TeamTypes eInterceptTeam=NO_TEAM;
		int iInterceptChance = kNuke.nukeInterceptionChance(
				kPlot, kNuke.getTeam(), &eInterceptTeam);
		if (eInterceptTeam != NO_TEAM)
		{
			FAssert(iInterceptChance > 0);
			szHelp.append(gDLL->getText("TXT_KEY_NUKE_INTERCEPT_CHANCE",
					// Should perhaps show the team only when its not directly affected?
					GET_TEAM(eInterceptTeam).getName().c_str(), iInterceptChance));
		} // </advc.650>
		return; // advc
	}
	// <kekm.7> (advc)
	CvWString szExplain;
	// To prevent info leaks
	for (SquareIter it(kPlot, kNuke.nukeRange());
		it.hasNext() && szExplain.empty(); ++it)
	{
		if (!it->isRevealed(kNuke.getTeam()))
			szExplain.append(gDLL->getText("TXT_KEY_CANT_NUKE_UNREVEALED"));
	}
	// Prioritize the explanations
	for (int iPass = 0; iPass < 4 && szExplain.empty(); iPass++) // </kekm.7>
	{
		for (TeamIter<ALIVE> it; it.hasNext(); ++it)
		{
			TeamTypes const eVictimTeam = it->getID();
			if (!kNuke.isNukeVictim(&kPlot, eVictimTeam, kNuke.getTeam()))
				continue;
			// <kekm.7> (advc)
			if (kNuke.isEnemy(eVictimTeam))
			{
				if (iPass <= 1)
				{
					bool bCityFound = false;
					for (SquareIter it(kPlot, kNuke.nukeRange()); it.hasNext(); ++it)
					{
						if (it->isCity() &&
							(iPass == 0 ?
							(kNuke.isEnemy(it->getTeam()) &&
							it->calculateFriendlyCulturePercent(kNuke.getTeam()) >=
							GC.getDefineINT(CvGlobals::CITY_NUKE_CULTURE_THRESH)) :
							!GET_TEAM(it->calculateCulturalOwner(true)).
							isAtWar(kNuke.getTeam())))
						{
							bCityFound = true;
							break;
						}
					}
					if (bCityFound)
					{
						szExplain.append(iPass == 0 ?
								gDLL->getText("TXT_KEY_CANT_NUKE_OWN_POP",
								GC.getDefineINT(CvGlobals::CITY_NUKE_CULTURE_THRESH)) :
								gDLL->getText("TXT_KEY_CANT_NUKE_NEUTRAL_POP"));
						break;
					}
				}
			}
			else
			{
				if (eVictimTeam == kNuke.getTeam())
				{
					if (iPass == 3)
						szExplain.append(gDLL->getText("TXT_KEY_CANT_NUKE_OWN_TEAM"));
				}
				else if (iPass == 2) // </kekm.7>
					szExplain.append(gDLL->getText("TXT_KEY_CANT_NUKE_FRIENDS"));
				break;
			}
		}
	}
	szHelp.append(szExplain);
}

/*	advc.004c: (Beginning based on getNukePlotHelp; the defense damage part is akin
	to the MISSION_BOMBARD case in CvDLLWidgetData::parseActionHelp_Mission.) */
void CvGameTextMgr::getAirBombPlotHelp(CvPlot const& kPlot,
	CvUnit& kHeadSelectedUnit, CvWString& szHelp)
{
	CvUnit const* pBestSelectedUnit = gDLL->UI().getSelectionList()->AI().
			AI_bestUnitForMission(MISSION_AIRBOMB, &kPlot);
	if (pBestSelectedUnit == NULL || !pBestSelectedUnit->canAirBombAt(kPlot))
		return;
	setInterceptPlotHelp(kPlot, *pBestSelectedUnit, szHelp);

	TeamTypes const eActiveTeam = getActiveTeam();
	CvCity const* pBombardCity = kPlot.getPlotCity();
	if (pBombardCity != NULL && pBombardCity->isRevealed(eActiveTeam))
	{
		int const iMaxDamage = (pBombardCity->isVisible(eActiveTeam) ?
				pBombardCity->getDefenseModifier(true) : MAX_INT);
		int iDamage = 0;
		for (CLLNode<IDInfo> const* pNode = gDLL->UI().headSelectionListNode();
			pNode != NULL; pNode = gDLL->UI().nextSelectionListNode(pNode))
		{
			CvUnit const& kSelectedUnit = *::getUnit(pNode->m_data);
			iDamage += kSelectedUnit.airBombDefenseDamage(*pBombardCity);
			if (iDamage >= iMaxDamage)
			{
				iDamage = iMaxDamage;
				break;
			}
		}
		if (iDamage > 0)
		{
			szHelp.append(gDLL->getText("TXT_KEY_AIR_BOMB_MODE_HELP_CITY_DEFENSE",
					pBombardCity->getNameKey(), iDamage));
		}
		else szHelp.append(gDLL->getText("TXT_KEY_AIR_BOMB_MODE_HELP_CITY_DEFENSE_NO_DAMAGE",
					pBombardCity->getNameKey()));
		szHelp.append(NEWLINE);
		return;
	}
	// <advc.255>
	CvUnit::StructureTypes const eStructure = kHeadSelectedUnit.
			getDestructibleStructureAt(kPlot, true, /* advc.111: */ GC.ctrlKey());
	if (eStructure == CvUnit::NO_STRUCTURE)
		return; // </advc.255>
	// Formula matches dice roll in CvUnit::airBomb
	int const iAttack = pBestSelectedUnit->airBombCurrRate();
	bool const bRoute = (eStructure == CvUnit::STRUCTURE_ROUTE); // advc.255
	ImprovementTypes const eImprov = kPlot.getRevealedImprovementType(eActiveTeam);
	RouteTypes const eRoute = kPlot.getRevealedRouteType(eActiveTeam); // advc.255
	int const iDefense = /* <advc.255> */ (bRoute ?
			GC.getInfo(eRoute).get(CvRouteInfo::AirBombDefense) : // </advc.255>
			GC.getInfo(eImprov).getAirBombDefense());
	scaled rSuccessProb = 1;
	if (iDefense > 0)
	{
		if (iAttack <= 0)
			rSuccessProb = 0;
		else
		{	/*	Probability of iAttack-sided die rolling greater than
				or equal to iDefense-sided die */
			rSuccessProb = (iAttack > iDefense ?
					1 - scaled(iDefense - 1, 2 * iAttack) :
					scaled(iAttack + 1, 2 * iDefense));
		}
	}
	if (rSuccessProb > 0)
	{
		int iPercent = rSuccessProb.getPercent();
		if (iPercent == 0) // Don't show uncertain outcome as certain
			iPercent++;
		if (iPercent == 100 && rSuccessProb < 1)
			iPercent--;
		szHelp.append(gDLL->getText("TXT_KEY_AIR_BOMB_MODE_HELP_DESTR_IMPROV",
				bRoute ? GC.getInfo(eRoute).getDescription() : // advc.255
				GC.getInfo(eImprov).getDescription(),
				iPercent));
		szHelp.append(NEWLINE);
	}
}

// advc.004c:
void CvGameTextMgr::getAirStrikePlotHelp(CvPlot const& kPlot,
	CvUnit& kHeadSelectedUnit, CvWString& szHelp)
{
	int iOddsDummy=-1;
	bool const bMaxSurvival = GC.altKey(); // advc.048
	// Matching the call in CvSelectionGroup::groupAttack
	CvUnit const* pBestSelectedUnit = gDLL->UI().getSelectionList()->AI().
			AI_getBestGroupAttacker(&kPlot,
			false, iOddsDummy, false, false,
			!bMaxSurvival, bMaxSurvival); // advc.048
	if (pBestSelectedUnit != NULL && pBestSelectedUnit->canAirStrike(kPlot))
		setInterceptPlotHelp(kPlot, *pBestSelectedUnit, szHelp);
}

// advc.004c:
void CvGameTextMgr::getParadropPlotHelp(CvPlot const& kPlot,
	CvUnit& kHeadSelectedUnit, CvWString& szHelp)
{
	CvUnit const* pBestSelectedUnit = NULL;
	int iMaxEvasionProb = MIN_INT;
	FOR_EACH_UNIT_IN(pUnit, *gDLL->UI().getSelectionList())
	{
		int iLoopProb = pUnit->evasionProbability();
		if (iLoopProb > iMaxEvasionProb)
		{
			iMaxEvasionProb = iLoopProb;
			pBestSelectedUnit = pUnit;
		}
	}
	if (pBestSelectedUnit != NULL &&
		pBestSelectedUnit->canParadropAt(
		pBestSelectedUnit->plot(), kPlot.getX(), kPlot.getY()))
	{
		setInterceptPlotHelp(kPlot, *pBestSelectedUnit, szHelp);
	}
}

void CvGameTextMgr::getInterfaceCenterText(CvWString& strText)
{
	strText.clear();
	if (!gDLL->UI().isCityScreenUp())
	{
	    // doc: disable victory text
		/*if (GC.getGame().getWinner() != NO_TEAM)
		{
			strText = gDLL->getText("TXT_KEY_MISC_WINS_VICTORY",
					GET_TEAM(GC.getGame().getWinner()).getName().GetCString(),
					GC.getInfo(GC.getGame().getVictory()).getTextKeyWide());
		}*/

	    if (!GET_PLAYER(getActivePlayer()).isAlive())
			strText = gDLL->getText("TXT_KEY_MISC_DEFEAT");
	}
}

void CvGameTextMgr::getTurnTimerText(CvWString& strText)
{
	strText.clear();
	CvGame const& kGame = GC.getGame();
	if (gDLL->UI().getShowInterface() == INTERFACE_SHOW ||
		gDLL->UI().getShowInterface() == INTERFACE_ADVANCED_START)
	{
		if (kGame.isMPOption(MPOPTION_TURN_TIMER))
		{
			// Get number of turn slices remaining until end-of-turn
			int iTurnSlicesRemaining = kGame.getTurnSlicesRemaining();

			if (iTurnSlicesRemaining > 0)
			{
				// Get number of seconds remaining
				int iTurnSecondsRemaining = ((int)floorf((float)(iTurnSlicesRemaining-1) * ((float)gDLL->getMillisecsPerTurn()/1000.0f)) + 1);
				int iTurnMinutesRemaining = (int)(iTurnSecondsRemaining/60);
				iTurnSecondsRemaining = (iTurnSecondsRemaining%60);
				int iTurnHoursRemaining = (int)(iTurnMinutesRemaining/60);
				iTurnMinutesRemaining = (iTurnMinutesRemaining%60);

				// Display time remaining
				CvWString szTempBuffer;
				szTempBuffer.Format(L"%d:%02d:%02d", iTurnHoursRemaining, iTurnMinutesRemaining, iTurnSecondsRemaining);
				strText += szTempBuffer;
			}
			else
			{
				// Flash zeroes
				if (iTurnSlicesRemaining % 2 == 0)
				{
					// Display 0
					strText+=L"0:00";
				}
			}
		}
		if (kGame.getGameState() == GAMESTATE_ON)
		{	// <advc.700> Top priority for Auto Play timer
			if(kGame.isOption(GAMEOPTION_RISE_FALL))
			{
				int autoPlayCountdown = kGame.getRiseFall().getAutoPlayCountdown();
				if(autoPlayCountdown > 0)
				{
					strText = gDLL->getText("TXT_KEY_RF_INTERLUDE_COUNTDOWN",
							autoPlayCountdown);
					return;
				}
			} // </advc.700>
			int iMinVictoryTurns = MAX_INT;
			FOR_EACH_ENUM(Victory)
			{
				TeamTypes eActiveTeam = getActiveTeam();
				if (eActiveTeam != NO_TEAM)
				{
					int iCountdown = GET_TEAM(eActiveTeam).
							getVictoryCountdown(eLoopVictory);
					if (iCountdown > 0 && iCountdown < iMinVictoryTurns)
						iMinVictoryTurns = iCountdown;
				}
			}

			if (kGame.isOption(GAMEOPTION_ADVANCED_START) &&
				!kGame.isOption(GAMEOPTION_ALWAYS_WAR) &&
				kGame.getElapsedGameTurns() <=
				GC.getDefineINT(CvGlobals::PEACE_TREATY_LENGTH) &&
				/*  advc.250b: No need to (constantly) remind human of
					"universal" peace when the AI civs have big headstarts. */
				!kGame.isOption(GAMEOPTION_SPAH))
			{
				if(!strText.empty())
					strText += L" -- ";
				strText += gDLL->getText("TXT_KEY_MISC_ADVANCED_START_PEACE_REMAINING",
						GC.getDefineINT(CvGlobals::PEACE_TREATY_LENGTH) - kGame.getElapsedGameTurns());
			}
			else if (iMinVictoryTurns < MAX_INT)
			{
				if (!strText.empty())
					strText += L" -- ";
				strText += gDLL->getText("TXT_KEY_MISC_TURNS_LEFT_TO_VICTORY", iMinVictoryTurns);
			} /* <advc> Merged these two conditions so that more else-if
				clauses can be added below */
			else if (kGame.getMaxTurns() > 0 && (kGame.getElapsedGameTurns() >= kGame.getMaxTurns() -
				20 // advc.004: was 100 // doc: reduced from 30 to 20
				&& kGame.getElapsedGameTurns() < kGame.getMaxTurns())) // </advc>
			{
				if(!strText.empty())
					strText += L" -- ";
				strText += gDLL->getText("TXT_KEY_MISC_TURNS_LEFT",
						kGame.getMaxTurns() - kGame.getElapsedGameTurns());
			} // <advc.700> The other countdowns take precedence
			else if(kGame.isOption(GAMEOPTION_RISE_FALL))
			{
				std::pair<int,int> rfCountdown = kGame.getRiseFall().
						getChapterCountdown();
				/*  Only show it toward the end of a chapter. A permanent countdown
					would have to be placed elsewhere b/c the font is too large and
					its size appears to be set outside the SDK. */
				if(rfCountdown.second >= 0 && rfCountdown.second - rfCountdown.first < 3)
				{
					strText = gDLL->getText("TXT_KEY_RF_CHAPTER_COUNTDOWN",
							rfCountdown.first, rfCountdown.second);
				}
			} // </advc.700>
		}
	}
}

void CvGameTextMgr::getFontSymbols(std::vector< std::vector<wchar> >& aacSymbols,
	std::vector<int>& aiMaxNumRows)
{
	aacSymbols.push_back(std::vector<wchar>());
	aiMaxNumRows.push_back(1);
	FOR_EACH_ENUM(Yield)
	{
		aacSymbols[aacSymbols.size() - 1].push_back(GC.getInfo(eLoopYield).getChar());
	}

	aacSymbols.push_back(std::vector<wchar>());
	aiMaxNumRows.push_back(2);
	FOR_EACH_ENUM(Commerce)
	{
		aacSymbols[aacSymbols.size() - 1].push_back(GC.getInfo(eLoopCommerce).getChar());
	}

	aacSymbols.push_back(std::vector<wchar>());
	aiMaxNumRows.push_back(2);
	FOR_EACH_ENUM(Religion)
	{
		aacSymbols[aacSymbols.size() - 1].push_back(GC.getInfo(eLoopReligion).getChar());
		aacSymbols[aacSymbols.size() - 1].push_back(GC.getInfo(eLoopReligion).getHolyCityChar());
	}
	FOR_EACH_ENUM(Corporation)
	{
		aacSymbols[aacSymbols.size() - 1].push_back(GC.getInfo(eLoopCorporation).getChar());
		aacSymbols[aacSymbols.size() - 1].push_back(GC.getInfo(eLoopCorporation).getHeadquarterChar());
	}

	aacSymbols.push_back(std::vector<wchar>());
	aiMaxNumRows.push_back(3);
	FOR_EACH_ENUM(Bonus)
	{
		aacSymbols[aacSymbols.size() - 1].push_back(GC.getInfo(eLoopBonus).getChar());
	}

	aacSymbols.push_back(std::vector<wchar>());
	aiMaxNumRows.push_back(3);
	for (int i = 0; i < MAX_NUM_SYMBOLS; i++)
	{
		aacSymbols[aacSymbols.size() - 1].push_back((wchar)gDLL->getSymbolID(i));
	}
}

void CvGameTextMgr::assignFontIds(int iFirstSymbolCode, int iPadAmount)
{
	/*	advc.make: safeIntCast calls added throughout so that the info classes
		can store the symbol as a wchar. */

	int iSymbol = iFirstSymbolCode;

	// set yield symbols
	FOR_EACH_ENUM(Yield)
	{
		GC.getInfo(eLoopYield).setChar(safeIntCast<wchar>(iSymbol));
		iSymbol++;
	}

	do
	{
		iSymbol++;
	} while (iSymbol % iPadAmount != 0);

	// set commerce symbols
	FOR_EACH_ENUM(Commerce)
	{
		GC.getInfo(eLoopCommerce).setChar(safeIntCast<wchar>(iSymbol));
		iSymbol++;
	}

	do
	{
		iSymbol++;
	} while (iSymbol % iPadAmount != 0);

	if (NUM_COMMERCE_TYPES < iPadAmount)
	{
		do
		{
			iSymbol++;
		} while (iSymbol % iPadAmount != 0);
	}

	FOR_EACH_ENUM(Religion)
	{
		GC.getInfo(eLoopReligion).setChar(safeIntCast<wchar>(iSymbol));
		iSymbol++;
		GC.getInfo(eLoopReligion).setHolyCityChar(safeIntCast<wchar>(iSymbol));
		iSymbol++;
	}
	FOR_EACH_ENUM(Corporation)
	{
		GC.getInfo(eLoopCorporation).setChar(safeIntCast<wchar>(iSymbol));
		iSymbol++;
		GC.getInfo(eLoopCorporation).setHeadquarterChar(safeIntCast<wchar>(iSymbol));
		iSymbol++;
	}

	do
	{
		iSymbol++;
	} while (iSymbol % iPadAmount != 0);

	if (2 * (GC.getNumReligionInfos() + GC.getNumCorporationInfos()) < iPadAmount)
	{
		do
		{
			iSymbol++;
		} while (iSymbol % iPadAmount != 0);
	}

	// set bonus symbols
	int iBonusBase = iSymbol;

	/*  UNOFFICIAL_PATCH, Bugfix (GameFontFix), 06/02/10, LunarMongoose
		this erroneous extra increment command was breaking GameFont.tga files
		when using exactly 49 or 74 resource types in a mod */
	//iSymbol++;
	FOR_EACH_ENUM(Bonus)
	{
		int iBonus = iBonusBase + GC.getInfo(eLoopBonus).getArtInfo()->getFontButtonIndex();
		GC.getInfo(eLoopBonus).setChar(safeIntCast<wchar>(iBonus));
		iSymbol++;
	}

	do
	{
		iSymbol++;
	} while (iSymbol % iPadAmount != 0);

	if (GC.getNumBonusInfos() < iPadAmount)
	{
		do
		{
			iSymbol++;
		} while (iSymbol % iPadAmount != 0);
	}

	if (GC.getNumBonusInfos() < 2 * iPadAmount)
	{
		do
		{
			iSymbol++;
		} while (iSymbol % iPadAmount != 0);
	}

	// set extra symbols
	for (int i = 0; i < MAX_NUM_SYMBOLS; i++)
	{
		gDLL->setSymbolID(i, iSymbol);
		iSymbol++;
	}

    // doc: fonts loaded event
	CvEventReporter::getInstance().fontsLoaded();
}

void CvGameTextMgr::getCityDataForAS(std::vector<CvWBData>& mapCityList,
	std::vector<CvWBData>& mapBuildingList, std::vector<CvWBData>& mapAutomateList)
{
	CvPlayer const& kActivePlayer = GET_PLAYER(getActivePlayer());

	CvWString szHelp;
	int iCost = kActivePlayer.getAdvancedStartCityCost(true);
	if (iCost > 0)
	{
		szHelp = gDLL->getText("TXT_KEY_CITY");
		szHelp += gDLL->getText("TXT_KEY_AS_UNREMOVABLE");
		mapCityList.push_back(CvWBData(0, szHelp,
				ARTFILEMGR.getInterfaceArtInfo("INTERFACE_BUTTONS_CITYSELECTION")->getPath()));
	}

	iCost = kActivePlayer.getAdvancedStartPopCost(true);
	if (iCost > 0)
	{
		szHelp = gDLL->getText("TXT_KEY_WB_AS_POPULATION");
		mapCityList.push_back(CvWBData(1, szHelp,
				ARTFILEMGR.getInterfaceArtInfo("INTERFACE_ANGRYCITIZEN_TEXTURE")->getPath()));
	}

	iCost = kActivePlayer.getAdvancedStartCultureCost(true);
	if (iCost > 0)
	{
		szHelp = gDLL->getText("TXT_KEY_ADVISOR_CULTURE");
		szHelp += gDLL->getText("TXT_KEY_AS_UNREMOVABLE");
		mapCityList.push_back(CvWBData(2, szHelp,
				ARTFILEMGR.getInterfaceArtInfo("CULTURE_BUTTON")->getPath()));
	}

	CvWStringBuffer szBuffer;
	CvCivilization const& kCiv = kActivePlayer.getCivilization(); // advc.003w
	for (int i = 0; i < kCiv.getNumBuildings(); i++)
	{
		BuildingTypes eBuilding = kCiv.buildingAt(i);
		if(!GC.getGame().isFreeStartEraBuilding(eBuilding)) // advc
		{
			// Building cost -1 denotes unit which may not be purchased
			iCost = kActivePlayer.getAdvancedStartBuildingCost(eBuilding, true);
			if (iCost > 0)
			{
				szBuffer.clear();
				setBuildingHelp(szBuffer, eBuilding);
				szBuffer.append(gDLL->getText("TXT_KEY_AS_UNREMOVABLE")); // advc.250c
				mapBuildingList.push_back(CvWBData(eBuilding, szBuffer.getCString(),
						GC.getInfo(eBuilding).getButton()));
			}
		}
	}

	szHelp = gDLL->getText("TXT_KEY_ACTION_AUTOMATE_BUILD");
	mapAutomateList.push_back(CvWBData(0, szHelp,
			ARTFILEMGR.getInterfaceArtInfo("INTERFACE_AUTOMATE")->getPath()));
}

void CvGameTextMgr::getUnitDataForAS(std::vector<CvWBData>& mapUnitList)
{
	CvPlayer const& kActivePlayer = GET_PLAYER(getActivePlayer());

	CvWStringBuffer szBuffer;
	CvCivilization const& kCiv = kActivePlayer.getCivilization(); // advc.003w
	for (int i = 0; i < kCiv.getNumUnits(); i++)
	{
		UnitTypes eUnit = kCiv.unitAt(i);
		// Unit cost -1 denotes unit which may not be purchased
		int iCost = kActivePlayer.getAdvancedStartUnitCost(eUnit, true);
		if (iCost > 0)
		{
			szBuffer.clear();
			setUnitHelp(szBuffer, eUnit);

			int iMaxUnitsPerCity = GC.getDefineINT("ADVANCED_START_MAX_UNITS_PER_CITY");
			if (iMaxUnitsPerCity >= 0 && GC.getInfo(eUnit).isMilitarySupport())
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_WB_AS_MAX_UNITS_PER_CITY",
					iMaxUnitsPerCity));
			}
			mapUnitList.push_back(CvWBData(eUnit, szBuffer.getCString(),
					kActivePlayer.getUnitButton(eUnit)));
		}
	}
}

void CvGameTextMgr::getImprovementDataForAS(std::vector<CvWBData>& mapImprovementList,
	std::vector<CvWBData>& mapRouteList)
{
	CvPlayer const& kActivePlayer = GET_PLAYER(getActivePlayer());

	FOR_EACH_ENUM(Route)
	{
		int iCost = kActivePlayer.getAdvancedStartRouteCost(eLoopRoute, true);
		if (iCost > 0) // Cost -1 denotes route which may not be purchased
		{
			mapRouteList.push_back(CvWBData(
					eLoopRoute,
					GC.getInfo(eLoopRoute).getDescription(),
					GC.getInfo(eLoopRoute).getButton()));
		}
	}

	CvWStringBuffer szBuffer;
	FOR_EACH_ENUM(Improvement)
	{
		int iCost = kActivePlayer.getAdvancedStartImprovementCost(eLoopImprovement, true);
		// Cost -1 denotes Improvement which may not be purchased
		if (iCost > 0)
		{
			szBuffer.clear();
			setImprovementHelp(szBuffer, eLoopImprovement);
			mapImprovementList.push_back(CvWBData(
					eLoopImprovement,
					szBuffer.getCString(),
					GC.getInfo(eLoopImprovement).getButton()));
		}
	}
}

void CvGameTextMgr::getVisibilityDataForAS(std::vector<CvWBData>& mapVisibilityList)
{
	// Unit cost -1 denotes unit which may not be purchased
	int iCost = GET_PLAYER(getActivePlayer()).getAdvancedStartVisibilityCost(true);
	if (iCost > 0)
	{
		CvWString szHelp = gDLL->getText("TXT_KEY_WB_AS_VISIBILITY");
		szHelp += gDLL->getText("TXT_KEY_AS_UNREMOVABLE", iCost);
		mapVisibilityList.push_back(CvWBData(0, szHelp,
				ARTFILEMGR.getInterfaceArtInfo("INTERFACE_TECH_LOS")->getPath()));
	}
}

void CvGameTextMgr::getTechDataForAS(std::vector<CvWBData>& mapTechList)
{
	static CvWString szTechHelp = // advc.250c
				CvWString(gDLL->getText("TXT_KEY_WB_AS_TECH")) +
				gDLL->getText("TXT_KEY_AS_UNREMOVABLE"); // advc.250c
	mapTechList.push_back(CvWBData(0, szTechHelp.c_str(),
			ARTFILEMGR.getInterfaceArtInfo("INTERFACE_BTN_TECH")->getPath()));
}

void CvGameTextMgr::getUnitDataForWB(std::vector<CvWBData>& mapUnitData)
{
	CvWStringBuffer szBuffer;
	FOR_EACH_ENUM(Unit)
	{
		szBuffer.clear();
		setUnitHelp(szBuffer, eLoopUnit);
		mapUnitData.push_back(CvWBData(
				eLoopUnit,
				szBuffer.getCString(),
				GC.getInfo(eLoopUnit).getButton()));
	}
}

void CvGameTextMgr::getBuildingDataForWB(bool bStickyButton, std::vector<CvWBData>& mapBuildingData)
{
	int iCount = 0;
	if (!bStickyButton)
	{
		mapBuildingData.push_back(CvWBData(
				iCount++,
				GC.getInfo(MISSION_FOUND).getDescription(),
				GC.getInfo(MISSION_FOUND).getButton()));
	}

	CvWStringBuffer szBuffer;
	FOR_EACH_ENUM(Building)
	{
		szBuffer.clear();
		setBuildingHelp(szBuffer, eLoopBuilding);
		mapBuildingData.push_back(CvWBData(
				iCount++,
				szBuffer.getCString(),
				GC.getInfo(eLoopBuilding).getButton()));
	}
}

void CvGameTextMgr::getTerrainDataForWB(std::vector<CvWBData>& mapTerrainData,
	std::vector<CvWBData>& mapFeatureData, std::vector<CvWBData>& mapPlotData,
	std::vector<CvWBData>& mapRouteData)
{
	CvWStringBuffer szBuffer;

	FOR_EACH_ENUM(Terrain)
	{
		if (!GC.getInfo(eLoopTerrain).isGraphicalOnly())
		{
			szBuffer.clear();
			setTerrainHelp(szBuffer, eLoopTerrain);
			mapTerrainData.push_back(CvWBData(
					eLoopTerrain,
					szBuffer.getCString(),
					GC.getInfo(eLoopTerrain).getButton()));
		}
	}

	FOR_EACH_ENUM(Feature)
	{
		for (int i = 0; i < GC.getInfo(eLoopFeature).getArtInfo()->
			getNumVarieties(); i++)
		{
			szBuffer.clear();
			setFeatureHelp(szBuffer, eLoopFeature);
			mapFeatureData.push_back(CvWBData(
					eLoopFeature + GC.getNumFeatureInfos() * i,
					szBuffer.getCString(),
					GC.getInfo(eLoopFeature).getArtInfo()->
					getVariety(i).getVarietyButton()));
		}
	}

	mapPlotData.push_back(CvWBData(0, gDLL->getText("TXT_KEY_WB_PLOT_TYPE_MOUNTAIN"), ARTFILEMGR.getInterfaceArtInfo("WORLDBUILDER_PLOT_TYPE_MOUNTAIN")->getPath()));
	mapPlotData.push_back(CvWBData(1, gDLL->getText("TXT_KEY_WB_PLOT_TYPE_HILL"), ARTFILEMGR.getInterfaceArtInfo("WORLDBUILDER_PLOT_TYPE_HILL")->getPath()));
	mapPlotData.push_back(CvWBData(2, gDLL->getText("TXT_KEY_WB_PLOT_TYPE_PLAINS"), ARTFILEMGR.getInterfaceArtInfo("WORLDBUILDER_PLOT_TYPE_PLAINS")->getPath()));
	mapPlotData.push_back(CvWBData(3, gDLL->getText("TXT_KEY_WB_PLOT_TYPE_OCEAN"), ARTFILEMGR.getInterfaceArtInfo("WORLDBUILDER_PLOT_TYPE_OCEAN")->getPath()));

	FOR_EACH_ENUM(Route)
	{
		mapRouteData.push_back(CvWBData(
				eLoopRoute,
				GC.getInfo(eLoopRoute).getDescription(),
				GC.getInfo(eLoopRoute).getButton()));
	}
	mapRouteData.push_back(CvWBData(GC.getNumRouteInfos(),
			gDLL->getText("TXT_KEY_WB_RIVER_PLACEMENT"),
			ARTFILEMGR.getInterfaceArtInfo("WORLDBUILDER_RIVER_PLACEMENT")->getPath()));
}

void CvGameTextMgr::getTerritoryDataForWB(std::vector<CvWBData>& mapTerritoryData)
{
	for (int i = 0; i <= MAX_CIV_PLAYERS; i++)
	{
		CvWString szName = gDLL->getText("TXT_KEY_MAIN_MENU_NONE");
		CvString szButton = GC.getInfo(GET_PLAYER(BARBARIAN_PLAYER).getCivilizationType()).getButton();

		if (GET_PLAYER((PlayerTypes) i).isEverAlive())
		{
			szName = GET_PLAYER((PlayerTypes)i).getName();
			szButton = GC.getInfo(GET_PLAYER((PlayerTypes)i).getCivilizationType()).getButton();
		}
		mapTerritoryData.push_back(CvWBData(i, szName, szButton));
	}
}


void CvGameTextMgr::getTechDataForWB(std::vector<CvWBData>& mapTechData)
{
	CvWStringBuffer szBuffer;
	FOR_EACH_ENUM(Tech)
	{
		szBuffer.clear();
		setTechHelp(szBuffer, eLoopTech);
		mapTechData.push_back(CvWBData(
				eLoopTech,
				szBuffer.getCString(),
				GC.getInfo(eLoopTech).getButton()));
	}
}

void CvGameTextMgr::getPromotionDataForWB(std::vector<CvWBData>& mapPromotionData)
{
	CvWStringBuffer szBuffer;
	for (int i=0; i < GC.getNumPromotionInfos(); i++)
	{
		szBuffer.clear();
		setPromotionHelp(szBuffer, (PromotionTypes) i, false);
		mapPromotionData.push_back(CvWBData(i, szBuffer.getCString(), GC.getInfo((PromotionTypes) i).getButton()));
	}
}

void CvGameTextMgr::getBonusDataForWB(std::vector<CvWBData>& mapBonusData)
{
	CvWStringBuffer szBuffer;
	for (int i=0; i < GC.getNumBonusInfos(); i++)
	{
		szBuffer.clear();
		setBonusHelp(szBuffer, (BonusTypes)i);
		mapBonusData.push_back(CvWBData(i, szBuffer.getCString(), GC.getInfo((BonusTypes) i).getButton()));
	}
}

void CvGameTextMgr::getImprovementDataForWB(std::vector<CvWBData>& mapImprovementData)
{
	CvWStringBuffer szBuffer;
	for (int i=0; i < GC.getNumImprovementInfos(); i++)
	{
		CvImprovementInfo& kInfo = GC.getInfo((ImprovementTypes) i);
		if (!kInfo.isGraphicalOnly())
		{
			szBuffer.clear();
			setImprovementHelp(szBuffer, (ImprovementTypes) i);
			mapImprovementData.push_back(CvWBData(i, szBuffer.getCString(), kInfo.getButton()));
		}
	}
}

void CvGameTextMgr::getReligionDataForWB(bool bHolyCity, std::vector<CvWBData>& mapReligionData)
{
	for (int i = 0; i < GC.getNumReligionInfos(); ++i)
	{
		CvReligionInfo& kInfo = GC.getInfo((ReligionTypes) i);
		CvWString strDescription = kInfo.getDescription();
		if (bHolyCity)
		{
			strDescription = gDLL->getText("TXT_KEY_WB_HOLYCITY", strDescription.GetCString());
		}
		mapReligionData.push_back(CvWBData(i, strDescription, kInfo.getButton()));
	}
}


void CvGameTextMgr::getCorporationDataForWB(bool bHeadquarters, std::vector<CvWBData>& mapCorporationData)
{
	for (int i = 0; i < GC.getNumCorporationInfos(); ++i)
	{
		CvCorporationInfo& kInfo = GC.getInfo((CorporationTypes) i);
		CvWString strDescription = kInfo.getDescription();
		if (bHeadquarters)
		{
			strDescription = gDLL->getText("TXT_KEY_CORPORATION_HEADQUARTERS", strDescription.GetCString());
		}
		mapCorporationData.push_back(CvWBData(i, strDescription, kInfo.getButton()));
	}
}

// <advc> Based on BtS and ACO code originally in setCombatPlotHelp
void CvGameTextMgr::appendCombatModifiers(CvWStringBuffer& szBuffer,
	CvPlot const& kPlot, CvUnit const& kAttacker, CvUnit const& kDefender,
	bool bAttackModifiers, bool bACOEnabled,
	bool bOnlyGeneric, bool bOnlyNonGeneric)
{
	CombatModifierOutputParams params;
	params.m_bACOEnabled = bACOEnabled;
	params.m_bAttackModifier = bAttackModifiers;
	params.m_bGenericModifier = true;
	if (bAttackModifiers)
	{
		if (!bOnlyNonGeneric)
		{
			appendCombatModifier(szBuffer,
					kAttacker.getExtraCombatPercent(),
					params, "TXT_KEY_COMBAT_PLOT_EXTRA_STRENGTH");
		}
		if (bOnlyGeneric)
			return;
		params.m_bGenericModifier = false;
		appendCombatModifier(szBuffer,
				kAttacker.unitClassAttackModifier(kDefender.getUnitClassType()),
				params, "TXT_KEY_COMBAT_PLOT_MOD_VS_TYPE",
				GC.getInfo(kDefender.getUnitClassType()).getTextKeyWide());
		if (kDefender.getUnitCombatType() != NO_UNITCOMBAT)
		{
			appendCombatModifier(szBuffer,
					kAttacker.unitCombatModifier(kDefender.getUnitCombatType()),
					params, "TXT_KEY_COMBAT_PLOT_MOD_VS_TYPE",
					GC.getInfo(kDefender.getUnitCombatType()).getTextKeyWide());
		}
		appendCombatModifier(szBuffer, kAttacker.domainModifier(
				kDefender.getDomainType()),
				params, "TXT_KEY_COMBAT_PLOT_MOD_VS_TYPE",
				GC.getInfo(kDefender.getDomainType()).getTextKeyWide());
		if (GET_TEAM(kDefender.getTeam()).isCityDefense(kPlot, // advc: was isCity
			kAttacker.getTeam())) // advc.183
		{
			appendCombatModifier(szBuffer,
					kAttacker.cityAttackModifier(),
					params, "TXT_KEY_COMBAT_PLOT_CITY_MOD");
		}
		if (kPlot.isHills())
		{
			appendCombatModifier(szBuffer,
					kAttacker.hillsAttackModifier(),
					params, "TXT_KEY_COMBAT_PLOT_HILLS_MOD");
		}
		if (kPlot.isFeature())
		{
			appendCombatModifier(szBuffer,
					kAttacker.featureAttackModifier(kPlot.getFeatureType()),
					params, "TXT_KEY_COMBAT_PLOT_UNIT_MOD",
					GC.getInfo(kPlot.getFeatureType()).getTextKeyWide());
		}
		else
		{
			appendCombatModifier(szBuffer,
					kAttacker.terrainAttackModifier(kPlot.getTerrainType()),
					params, "TXT_KEY_COMBAT_PLOT_UNIT_MOD",
					GC.getInfo(kPlot.getTerrainType()).getTextKeyWide());
		}
		appendCombatModifier(szBuffer,
				kAttacker.getKamikazePercent(),
				params, "TXT_KEY_COMBAT_KAMIKAZE_MOD");
		if (kDefender.isAnimal())
		{
			int iModifier = kAttacker.getUnitInfo().getAnimalCombatModifier();
			// advc.315c: Moved into the isBarbarian block below
			//iModifier -= GC.getInfo(GC.getGame().getHandicapType()).getAnimalCombatModifier();
			appendCombatModifier(szBuffer, iModifier,
					params, "TXT_KEY_UNIT_ANIMAL_COMBAT_MOD");
		}
		if (kDefender.isBarbarian())
		{
			appendCombatModifier(szBuffer,
					kAttacker.getUnitInfo().getBarbarianCombatModifier(), // advc.315c
					params, "TXT_KEY_UNIT_BARBARIAN_COMBAT_MOD");
			// <advc.315c> Show modifier from difficulty separately from unit abilities
			int iModifier = -GC.getInfo(
					GET_PLAYER(kAttacker.getOwner()). // K-Mod
					getHandicapType()).getBarbarianCombatModifier();
			// Moved from the isAnimal block above
			if (kDefender.isAnimal())
			{
				iModifier -= GC.getInfo(
						GET_PLAYER(kAttacker.getOwner()). // K-Mod
						getHandicapType()).getAnimalCombatModifier();
			}
			// <advc.313>
			if (kDefender.isKnownSeaBarbarian())
			{
				iModifier -= GC.getInfo(
						GET_PLAYER(kAttacker.getOwner()).
						getHandicapType()).get(CvHandicapInfo::SeaBarbarianBonus);
			} // </advc.313>
			appendCombatModifier(szBuffer, iModifier,
					params, "TXT_KEY_MISC_FROM_HANDICAP");
			// </advc.315c>
		}
		// As in BtS - display modifiers that are typically negative last (river, amphib)
		if (!kAttacker.isRiver() &&
			// advc.opt: isRiverCrossing is no longer supposed to handle non-adjacent tiles
			stepDistance(kAttacker.plot(), &kPlot) == 1 &&
			kAttacker.getPlot().isRiverCrossing(directionXY(kAttacker.getPlot(), kPlot)))
		{
			appendCombatModifier(szBuffer,
					GC.getDefineINT(CvGlobals::RIVER_ATTACK_MODIFIER),
					params, "TXT_KEY_COMBAT_PLOT_RIVER_MOD",
					GC.getInfo(kPlot.getTerrainType()).getTextKeyWide());
		}
		if (!kAttacker.isAmphib() && !kPlot.isWater() && kAttacker.getPlot().isWater())
		{
			appendCombatModifier(szBuffer,
					GC.getDefineINT(CvGlobals::AMPHIB_ATTACK_MODIFIER),
					params, "TXT_KEY_COMBAT_PLOT_AMPHIB_MOD",
					GC.getInfo(kPlot.getTerrainType()).getTextKeyWide());
		}
		return;
	}
	if (!bOnlyNonGeneric)
	{
		appendCombatModifier(szBuffer,
				kDefender.getExtraCombatPercent(),
				params, "TXT_KEY_COMBAT_PLOT_EXTRA_STRENGTH");
	}
	if (bOnlyGeneric)
		return;
	params.m_bGenericModifier = false;
	appendCombatModifier(szBuffer,
			kDefender.unitClassDefenseModifier(kAttacker.getUnitClassType()),
			params, "TXT_KEY_COMBAT_PLOT_MOD_VS_TYPE",
			GC.getInfo(kAttacker.getUnitClassType()).getTextKeyWide());
	if (kAttacker.getUnitCombatType() != NO_UNITCOMBAT)
	{
		appendCombatModifier(szBuffer,
				kDefender.unitCombatModifier(kAttacker.getUnitCombatType()),
				params, "TXT_KEY_COMBAT_PLOT_MOD_VS_TYPE",
				GC.getInfo(kAttacker.getUnitCombatType()).getTextKeyWide());
	}
	appendCombatModifier(szBuffer,
			kDefender.domainModifier(kAttacker.getDomainType()),
			params, "TXT_KEY_COMBAT_PLOT_MOD_VS_TYPE",
			GC.getInfo(kAttacker.getDomainType()).getTextKeyWide());
	if (!kDefender.noDefensiveBonus())
	{
		appendCombatModifier(szBuffer,
				// <advc.012> Show feature defense unless in a hostile tile
				kPlot.defenseModifier(kDefender.getTeam(),
				kAttacker.ignoreBuildingDefense(), kAttacker.getTeam()),
				// </advc.012>
				params, "TXT_KEY_COMBAT_PLOT_TILE_MOD");
	}
	appendCombatModifier(szBuffer,
			kDefender.fortifyModifier(),
			params, "TXT_KEY_COMBAT_PLOT_FORTIFY_MOD");
	if (GET_TEAM(kDefender.getTeam()).isCityDefense(kPlot, // advc: was isCity
		kAttacker.getTeam())) // advc.183
	{
		appendCombatModifier(szBuffer,
				kDefender.cityDefenseModifier(),
				params, "TXT_KEY_COMBAT_PLOT_CITY_MOD");
	}
	if (kPlot.isHills())
	{
		appendCombatModifier(szBuffer,
				kDefender.hillsDefenseModifier(),
				params, "TXT_KEY_COMBAT_PLOT_HILLS_MOD");
	}
	if (kPlot.isFeature())
	{
		appendCombatModifier(szBuffer,
				kDefender.featureDefenseModifier(kPlot.getFeatureType()),
				params, "TXT_KEY_COMBAT_PLOT_UNIT_MOD",
				GC.getInfo(kPlot.getFeatureType()).getTextKeyWide());
	}
	else
	{
		appendCombatModifier(szBuffer,
				kDefender.terrainDefenseModifier(kPlot.getTerrainType()),
				params, "TXT_KEY_COMBAT_PLOT_UNIT_MOD",
				GC.getInfo(kPlot.getTerrainType()).getTextKeyWide());
	}
}


void CvGameTextMgr::appendCombatModifier(CvWStringBuffer& szBuffer,
	int iModifier, CombatModifierOutputParams const& kParams,
	char const* szTextKey, wchar const* szTextArg)
{
	if (iModifier == 0)
		return;
	bool bNegativeColor = !kParams.m_bAttackModifier;
	/*	Use green for modifiers that _favor_ the attacker, red for
		modifiers that favor the defender. */
	if (iModifier < 0)
		bNegativeColor = !bNegativeColor;
	// advc.048: Let's always show the sign in the way that it actually works
	if (//kParams.m_bACOEnabled &&
		kParams.m_bAttackModifier && !kParams.m_bGenericModifier)
	{
		/*	Non-generic modifiers of the attacker apply
			-with inverted sign- to the defender. */
		iModifier *= -1;
	}
	szBuffer.append(NEWLINE);
	szBuffer.append(gDLL->getText(bNegativeColor ? "TXT_KEY_COLOR_NEGATIVE" :
			"TXT_KEY_COLOR_POSITIVE"));
	szBuffer.append(szTextArg == NULL ? gDLL->getText(szTextKey, iModifier) :
			gDLL->getText(szTextKey, iModifier, szTextArg));
	szBuffer.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));
}


void CvGameTextMgr::appendFirstStrikes(CvWStringBuffer& szBuffer,
	CvUnit const& kFirstStriker, CvUnit const& kOther, bool bNegativeColor)
{
	if (kOther.immuneToFirstStrikes() || kFirstStriker.maxFirstStrikes() <= 0)
		return;
	szBuffer.append(gDLL->getText(bNegativeColor ? "TXT_KEY_COLOR_NEGATIVE" :
			"TXT_KEY_COLOR_POSITIVE"));
	if (kFirstStriker.firstStrikes() == kFirstStriker.maxFirstStrikes())
	{
		if (kFirstStriker.firstStrikes() == 1)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_ONE_FIRST_STRIKE"));
		}
		else
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_UNIT_NUM_FIRST_STRIKES",
					kFirstStriker.firstStrikes()));
		}
	}
	else
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_UNIT_FIRST_STRIKE_CHANCES",
				kFirstStriker.firstStrikes(), kFirstStriker.maxFirstStrikes()));
	}
	szBuffer.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));
} // </advc>

/*  advc.004w: Based on code cut from setUnitHelp and setBasicUnitHelp (and deleted from
	setBuildingHelpActual). Units and buildings have the same production speed bonuses. */
template<OrderTypes eORDER, typename ORDER_DATA1, typename ORDER_DATA2>
void CvGameTextMgr::setProductionSpeedHelp(CvWStringBuffer& szBuffer,
	ORDER_DATA1 eData1, ORDER_DATA2 eData2,
	CvCity const* pCity, bool bCivilopediaText)
{
	BOOST_STATIC_ASSERT(eORDER == ORDER_TRAIN || eORDER == ORDER_CONSTRUCT);
	BOOST_STATIC_ASSERT((eORDER == ORDER_TRAIN) == (is_same_type<ORDER_DATA1,UnitTypes>::value));
	BOOST_STATIC_ASSERT((eORDER == ORDER_CONSTRUCT) == (is_same_type<ORDER_DATA1,BuildingTypes>::value));
	BOOST_STATIC_ASSERT((eORDER == ORDER_TRAIN) == (is_same_type<ORDER_DATA2,SpecialUnitTypes>::value));
	BOOST_STATIC_ASSERT((eORDER == ORDER_CONSTRUCT) == (is_same_type<ORDER_DATA2,SpecialBuildingTypes>::value));
	FOR_EACH_ENUM2(Bonus, eBonus)
	{
		int iProductionModifier = 0;
		if (eORDER == ORDER_TRAIN)
			iProductionModifier = GC.getInfo(eData1).getBonusProductionModifier(eBonus);
		else if (eORDER == ORDER_CONSTRUCT)
			iProductionModifier = GC.getInfo(eData1).getBonusProductionModifier(eBonus);
		if (iProductionModifier == 0)
			continue;
		if (pCity != NULL)
		{
			bool bHasBonus = pCity->hasBonus(eBonus);
			if (iProductionModifier > 0 ? bHasBonus : !bHasBonus)
				szBuffer.append(gDLL->getText("TXT_KEY_COLOR_POSITIVE"));
			else szBuffer.append(gDLL->getText("TXT_KEY_COLOR_NEGATIVE"));
		}
		if (!bCivilopediaText)
			szBuffer.append(L" (");
		else
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(CvWString::format(L"%c", gDLL->getSymbolID(BULLET_CHAR)));
		}
		wchar const* szBonus = GC.getInfo(eBonus).getTextKeyWide();
		if (iProductionModifier == 100)
		{
			szBuffer.append(gDLL->getText(bCivilopediaText ?
					"TXT_KEY_DOUBLE_PRODUCTION_WITH" :
					"TXT_KEY_DOUBLE_PRODUCTION_WITH_SHORT", szBonus));
		}
		else
		{
			szBuffer.append(gDLL->getText("TXT_KEY_FASTER_PRODUCTION_WITH",
					iProductionModifier, szBonus));
		}
		if(!bCivilopediaText)
			szBuffer.append(L")");
		if(pCity != NULL)
			szBuffer.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));
	}
	PlayerTypes eActivePlayer = getActivePlayer();
	if (!bCivilopediaText && eActivePlayer == NO_PLAYER)
		return;
	FOR_EACH_ENUM2(Trait, eTrait)
	{
		if (!bCivilopediaText)
		{
			if(!GC.getInfo(GET_PLAYER(eActivePlayer).getLeaderType()).hasTrait(eTrait))
				continue;
		}
		int iProductionModifier = 0;
		if (eORDER == ORDER_TRAIN)
		{
			iProductionModifier = GC.getInfo(eData1).getProductionTraits(eTrait);
			if (eData2 != NO_SPECIALUNIT)
				iProductionModifier += GC.getInfo(eData2).getProductionTraits(eTrait);
		}
		else if (eORDER == ORDER_CONSTRUCT)
		{
			iProductionModifier = GC.getInfo(eData1).getProductionTraits(eTrait);
			if (eData2 != NO_SPECIALBUILDING)
				iProductionModifier += GC.getInfo(eData2).getProductionTraits(eTrait);
		}
		if (iProductionModifier == 0)
			continue;
		if (!bCivilopediaText)
		{
			if(iProductionModifier > 0)
				szBuffer.append(gDLL->getText("TXT_KEY_COLOR_POSITIVE"));
			else szBuffer.append(gDLL->getText("TXT_KEY_COLOR_NEGATIVE"));
		}
		if (!bCivilopediaText)
		{
			/*  Not nice when more than one speed modifier applies (e.g. Wall).
				Should put each modifier on a separate line then. Also, "+100%"
				would be better than "double" in that case b/c the modifiers are
				additive. Awkward to implement though. :( */
			szBuffer.append(L" (");
		}
		else
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(CvWString::format(L"%c", gDLL->getSymbolID(BULLET_CHAR)));
		}
		wchar const* szTrait = GC.getInfo(eTrait).getTextKeyWide();
		if (iProductionModifier == 100)
		{
			szBuffer.append(gDLL->getText(bCivilopediaText ?
					"TXT_KEY_DOUBLE_SPEED_TRAIT" :
					"TXT_KEY_DOUBLE_SPEED_TRAIT_SHORT", szTrait));
		}
		else
		{
			szBuffer.append(gDLL->getText("TXT_KEY_PRODUCTION_MODIFIER_TRAIT",
				iProductionModifier, szTrait));
		}
		if (!bCivilopediaText)
		{
			szBuffer.append(L")");
			szBuffer.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));
		}
	}
}

/*	advc.001: Need to link explicitly to the specialist type so that SPECIALIST_SPY
	gets used and not UNIT_SPY. */
void CvGameTextMgr::setSpecialistLink(CvWString& szBuffer, SpecialistTypes eSpecialist,
	bool bPlural)
{
	CvWString szSpecialistType = GC.getInfo(eSpecialist).getType();
	wchar const* szSpecialistDescr = GC.getInfo(eSpecialist).getDescription();
	szBuffer.append(CvWString::format(L"<link=%s>%s</link>",
				(!bPlural ? szSpecialistType :
				gDLL->getText("TXT_KEY_SPECIALIST_PLURAL", szSpecialistType.c_str())).
				c_str(), szSpecialistDescr));
}

// advc.001: Link to corporation, not to building of the same name.
void CvGameTextMgr::setCorporationLink(CvWString& szBuffer, CorporationTypes eCorp)
{
	CvWString szCorpType = GC.getInfo(eCorp).getType();
	szBuffer.append(CvWString::format(L"<link=%s>%s</link>",
			szCorpType.c_str(), GC.getInfo(eCorp).getDescription()));
}
