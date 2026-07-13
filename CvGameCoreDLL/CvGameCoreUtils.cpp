#include "CvGameCoreDLL.h"
#include "CvGameCoreUtils.h"
#include "CoreAI.h"
#include "CvUnitAI.h"
#include "CvSelectionGroupAI.h"
#include "CityPlotIterator.h"
#include "BBAILog.h" // advc.007
#include "CvInfo_GameOption.h"


// advc.035:
void contestedPlots(std::vector<CvPlot*>& r, TeamTypes t1, TeamTypes t2)
{
	if(!GC.getDefineBOOL(CvGlobals::OWN_EXCLUSIVE_RADIUS))
		return;
	// Sufficient to check plots around the teams' cities
	std::vector<CvCity const*> apCities;
	for (MemberIter itMember1(t1); itMember1.hasNext(); ++itMember1)
	{
		FOR_EACH_CITY(c, *itMember1)
			apCities.push_back(c);
	}
	for (MemberIter itMember2(t2); itMember2.hasNext(); ++itMember2)
	{
		FOR_EACH_CITY(c, *itMember2)
			apCities.push_back(c);
	}
	std::set<int> seenPlots; // To avoid duplicates
	for(size_t i = 0; i < apCities.size(); i++)
	{
		CvCity const& c = *apCities[i];
		for(CityPlotIter it(c, false); it.hasNext(); ++it)
		{
			CvPlot& p = *it;
			if(p.isCity())
				continue;
			PlayerTypes eSecondOwner = p.getSecondOwner();
			PlayerTypes eOwner = p.getOwner();
			if(eOwner == NO_PLAYER || eSecondOwner == NO_PLAYER)
				continue;
			TeamTypes eTeam = TEAMID(eOwner);
			TeamTypes eSecondTeam = TEAMID(eSecondOwner);
			if(eTeam == eSecondTeam)
				continue;
			if((eTeam == t1 && eSecondTeam == t2) || (eTeam == t2 && eSecondTeam == t1))
			{
				int iPlotID = p.getX() * 1000 + p.getY();
				if(seenPlots.count(iPlotID) <= 0)
				{
					seenPlots.insert(iPlotID);
					r.push_back(&p);
				}
			}
		}
	}
}
// advc.004w: I'm not positive that there isn't already a function like this somewhere
void applyColorToString(CvWString& s, char const* szColor, bool bLink)
{
	if(bLink)
		s.Format(L"<link=literal>%s</link>", s.GetCString());
	s.Format(SETCOLR L"%s" ENDCOLR, TEXT_COLOR(szColor), s.GetCString());
}

// advc.002i: Formula by T. Riemersma (CompuPhase.com) via Wikipedia ("Color difference")
float colorDifference(NiColorA const& c1, NiColorA const& c2)
{
	float channelWeights[] = { 2, 4, 3 }; // R, G, B
	if (c1.r + c2.r > 1)
		std::swap(channelWeights[0], channelWeights[2]);
	float fDiff = 0;
	fDiff += SQR(c1.r - c2.r) * channelWeights[0];
	fDiff += SQR(c1.g - c2.g) * channelWeights[1];
	fDiff += SQR(c1.b - c2.b) * channelWeights[2];
	return fDiff;
}

DirectionTypes cardinalDirectionToDirection(CardinalDirectionTypes eCard)
{
	switch (eCard)
	{
	case CARDINALDIRECTION_NORTH:
		return DIRECTION_NORTH;
	case CARDINALDIRECTION_EAST:
		return DIRECTION_EAST;
	case CARDINALDIRECTION_SOUTH:
		return DIRECTION_SOUTH;
	case CARDINALDIRECTION_WEST:
		return DIRECTION_WEST;
	}
	return NO_DIRECTION;
}

DirectionTypes estimateDirection(int iDX, int iDY)
{
	const int displacementSize = 8;
	static float sqrt2 = 1 / sqrt(2.0f);
	//													N			NE			E			SE				S			SW				W			NW
	static float displacements[displacementSize][2] = {{0, 1}, {sqrt2, sqrt2}, {1, 0}, {sqrt2, -sqrt2}, {0, -1}, {-sqrt2, -sqrt2}, {-1, 0}, {-sqrt2, sqrt2}};
	float maximum = 0;
	int maximumIndex = -1;
	for(int i=0;i<displacementSize;i++)
	{
		float dotProduct = iDX * displacements[i][0] + iDY * displacements[i][1];
		if(dotProduct > maximum)
		{
			maximum = dotProduct;
			maximumIndex = i;
		}
	}

	return (DirectionTypes) maximumIndex;
}

DirectionTypes estimateDirection(const CvPlot* pFromPlot, const CvPlot* pToPlot)
{
	CvMap const& m = GC.getMap();
	return estimateDirection(
			m.dxWrap(pToPlot->getX() - pFromPlot->getX()),
			m.dyWrap(pToPlot->getY() - pFromPlot->getY()));
}

/*	advc: Cut from CvXMLLoadUtility.cpp, renamed
	from "CreateHotKeyFromDescription"; nothing is "created" here. */
CvWString hotkeyDescr::hotKeyFromDescription(TCHAR const* szDescr,
	bool bShift, bool bAlt, bool bCtrl)
{
	// Example: "Delete <COLOR:140,255,40,255>Shift+Delete</COLOR>"
	CvWString szHotKey;
	if (szDescr != NULL && strcmp(szDescr, "") != 0)
	{
		szHotKey += L" <color=140,255,40,255>";
		szHotKey += L"&lt;";

		if (bShift)
			szHotKey += gDLL->getText("TXT_KEY_SHIFT");

		if (bAlt)
			szHotKey += gDLL->getText("TXT_KEY_ALT");

		if (bCtrl)
			szHotKey += gDLL->getText("TXT_KEY_CTRL");

		szHotKey += keyStringFromKBCode(szDescr);
		szHotKey += L">";
		szHotKey += L"</color>";
	}
	return szHotKey;
}

// KB code to string; e.g. KB_DELETE -> "Delete"
// advc: Cut from CvXMLLoadUtility.cpp, renamed from "CreateKeyStringFromKBCode".
CvWString hotkeyDescr::keyStringFromKBCode(TCHAR const* szDescr)
{
	PROFILE_FUNC();

	struct CvKeyBoardMapping
	{
		TCHAR szDefineString[25];
		CvWString szKeyString;
	};

	// TODO - this should be a stl map instead of looping strcmp
	const int iNumKeyBoardMappings=108;
	const CvKeyBoardMapping asCvKeyBoardMapping[iNumKeyBoardMappings] =
	{
		{"KB_ESCAPE", gDLL->getText("TXT_KEY_KEYBOARD_ESCAPE")},
		{"KB_0","0"},
		{"KB_1","1"},
		{"KB_2","2"},
		{"KB_3","3"},
		{"KB_4","4"},
		{"KB_5","5"},
		{"KB_6","6"},
		{"KB_7","7"},
		{"KB_8","8"},
		{"KB_9","9"},
		{"KB_MINUS","-"},	    /* - on main keyboard */
		{"KB_A","A"},
		{"KB_B","B"},
		{"KB_C","C"},
		{"KB_D","D"},
		{"KB_E","E"},
		{"KB_F","F"},
		{"KB_G","G"},
		{"KB_H","H"},
		{"KB_I","I"},
		{"KB_J","J"},
		{"KB_K","K"},
		{"KB_L","L"},
		{"KB_M","M"},
		{"KB_N","N"},
		{"KB_O","O"},
		{"KB_P","P"},
		{"KB_Q","Q"},
		{"KB_R","R"},
		{"KB_S","S"},
		{"KB_T","T"},
		{"KB_U","U"},
		{"KB_V","V"},
		{"KB_W","W"},
		{"KB_X","X"},
		{"KB_Y","Y"},
		{"KB_Z","Z"},
		{"KB_EQUALS","="},
		{"KB_BACKSPACE",gDLL->getText("TXT_KEY_KEYBOARD_BACKSPACE")},
		{"KB_TAB","TAB"},
		{"KB_LBRACKET","["},
		{"KB_RBRACKET","]"},
		{"KB_RETURN",gDLL->getText("TXT_KEY_KEYBOARD_ENTER")},		/* Enter on main keyboard */
		{"KB_LCONTROL",gDLL->getText("TXT_KEY_KEYBOARD_LEFT_CONTROL_KEY")},
		{"KB_SEMICOLON",";"},
		{"KB_APOSTROPHE","'"},
		{"KB_GRAVE","`"},		/* accent grave */
		{"KB_LSHIFT",gDLL->getText("TXT_KEY_KEYBOARD_LEFT_SHIFT_KEY")},
		{"KB_BACKSLASH","\\"},
		{"KB_COMMA",","},
		{"KB_PERIOD","."},
		{"KB_SLASH","/"},
		{"KB_RSHIFT",gDLL->getText("TXT_KEY_KEYBOARD_RIGHT_SHIFT_KEY")},
		{"KB_NUMPADSTAR",gDLL->getText("TXT_KEY_KEYBOARD_NUM_PAD_STAR")},
		{"KB_LALT",gDLL->getText("TXT_KEY_KEYBOARD_LEFT_ALT_KEY")},
		{"KB_SPACE",gDLL->getText("TXT_KEY_KEYBOARD_SPACE_KEY")},
		{"KB_CAPSLOCK",gDLL->getText("TXT_KEY_KEYBOARD_CAPS_LOCK")},
		{"KB_F1","F1"},
		{"KB_F2","F2"},
		{"KB_F3","F3"},
		{"KB_F4","F4"},
		{"KB_F5","F5"},
		{"KB_F6","F6"},
		{"KB_F7","F7"},
		{"KB_F8","F8"},
		{"KB_F9","F9"},
		{"KB_F10","F10"},
		{"KB_NUMLOCK",gDLL->getText("TXT_KEY_KEYBOARD_NUM_LOCK")},
		{"KB_SCROLL",gDLL->getText("TXT_KEY_KEYBOARD_SCROLL_KEY")},
		{"KB_NUMPAD7",gDLL->getText("TXT_KEY_KEYBOARD_NUMPAD_NUMBER", 7)},
		{"KB_NUMPAD8",gDLL->getText("TXT_KEY_KEYBOARD_NUMPAD_NUMBER", 8)},
		{"KB_NUMPAD9",gDLL->getText("TXT_KEY_KEYBOARD_NUMPAD_NUMBER", 9)},
		{"KB_NUMPADMINUS",gDLL->getText("TXT_KEY_KEYBOARD_NUMPAD_MINUS")},
		{"KB_NUMPAD4",gDLL->getText("TXT_KEY_KEYBOARD_NUMPAD_NUMBER", 4)},
		{"KB_NUMPAD5",gDLL->getText("TXT_KEY_KEYBOARD_NUMPAD_NUMBER", 5)},
		{"KB_NUMPAD6",gDLL->getText("TXT_KEY_KEYBOARD_NUMPAD_NUMBER", 6)},
		{"KB_NUMPADPLUS",gDLL->getText("TXT_KEY_KEYBOARD_NUMPAD_PLUS")},
		{"KB_NUMPAD1",gDLL->getText("TXT_KEY_KEYBOARD_NUMPAD_NUMBER", 1)},
		{"KB_NUMPAD2",gDLL->getText("TXT_KEY_KEYBOARD_NUMPAD_NUMBER", 2)},
		{"KB_NUMPAD3",gDLL->getText("TXT_KEY_KEYBOARD_NUMPAD_NUMBER", 3)},
		{"KB_NUMPAD0",gDLL->getText("TXT_KEY_KEYBOARD_NUMPAD_NUMBER", 0)},
		{"KB_NUMPADPERIOD",gDLL->getText("TXT_KEY_KEYBOARD_NUMPAD_PERIOD")},
		{"KB_F11","F11"},
		{"KB_F12","F12"},
		{"KB_NUMPADEQUALS",gDLL->getText("TXT_KEY_KEYBOARD_NUMPAD_EQUALS")},
		{"KB_AT","@"},
		{"KB_UNDERLINE","_"},
		{"KB_COLON",":"},
		{"KB_NUMPADENTER",gDLL->getText("TXT_KEY_KEYBOARD_NUMPAD_ENTER_KEY")},
		{"KB_RCONTROL",gDLL->getText("TXT_KEY_KEYBOARD_RIGHT_CONTROL_KEY")},
		{"KB_VOLUMEDOWN",gDLL->getText("TXT_KEY_KEYBOARD_VOLUME_DOWN")},
		{"KB_VOLUMEUP",gDLL->getText("TXT_KEY_KEYBOARD_VOLUME_UP")},
		{"KB_NUMPADCOMMA",gDLL->getText("TXT_KEY_KEYBOARD_NUMPAD_COMMA")},
		{"KB_NUMPADSLASH",gDLL->getText("TXT_KEY_KEYBOARD_NUMPAD_SLASH")},
		{"KB_SYSRQ",gDLL->getText("TXT_KEY_KEYBOARD_SYSRQ")},
		{"KB_RALT",gDLL->getText("TXT_KEY_KEYBOARD_RIGHT_ALT_KEY")},
		{"KB_PAUSE",gDLL->getText("TXT_KEY_KEYBOARD_PAUSE_KEY")},
		{"KB_HOME",gDLL->getText("TXT_KEY_KEYBOARD_HOME_KEY")},
		{"KB_UP",gDLL->getText("TXT_KEY_KEYBOARD_UP_ARROW")},
		{"KB_PGUP",gDLL->getText("TXT_KEY_KEYBOARD_PAGE_UP")},
		{"KB_LEFT",gDLL->getText("TXT_KEY_KEYBOARD_LEFT_ARROW")},
		{"KB_RIGHT",gDLL->getText("TXT_KEY_KEYBOARD_RIGHT_ARROW")},
		{"KB_END",gDLL->getText("TXT_KEY_KEYBOARD_END_KEY")},
		{"KB_DOWN",gDLL->getText("TXT_KEY_KEYBOARD_DOWN_ARROW")},
		{"KB_PGDN",gDLL->getText("TXT_KEY_KEYBOARD_PAGE_DOWN")},
		{"KB_INSERT",gDLL->getText("TXT_KEY_KEYBOARD_INSERT_KEY")},
		{"KB_DELETE",gDLL->getText("TXT_KEY_KEYBOARD_DELETE_KEY")},
	};

	for (int i = 0; i < iNumKeyBoardMappings; i++)
	{
		if (strcmp(asCvKeyBoardMapping[i].szDefineString, szDescr) == 0)
			return asCvKeyBoardMapping[i].szKeyString;
	}

	return "";
}


bool atWar(TeamTypes eTeamA, TeamTypes eTeamB)
{
	return (eTeamA != NO_TEAM && eTeamB != NO_TEAM && GET_TEAM(eTeamA).isAtWar(eTeamB));
}
// advc: No longer needed
/*bool isPotentialEnemy(TeamTypes eOurTeam, TeamTypes eTheirTeam)
{
	FAssert(eOurTeam != NO_TEAM);
	if (eTheirTeam == NO_TEAM)
		return false;
	// advc: Moved into new CvTeamAI function
	return GET_TEAM(eOurTeam).AI_mayAttack(eTheirTeam);
}*/

// TODO: removed by advciv find new location
int getWorldSizeMaxConscript(CivicTypes eCivic)
{
	int iMaxConscript;

	iMaxConscript = GC.getCivicInfo(eCivic).getMaxConscript();

	/* Leoreth: better control it manually
	iMaxConscript *= std::max(0, (GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getMaxConscriptModifier() + 100));
	iMaxConscript /= 100;*/

	return iMaxConscript;
}

// K-Mod: (advc - Where do we move this? Should not be global.)
int estimateCollateralWeight(CvPlot const* pPlot, TeamTypes eAttackTeam,
	TeamTypes eDefenseTeam)
{
	int iBaseCollateral = GC.getDefineINT(CvGlobals::COLLATERAL_COMBAT_DAMAGE); // normally 10
	if (pPlot == NULL)
		return iBaseCollateral * 110;

	/*	Collateral damage does not depend on any kind of strength bonus -
		so when a unit takes collateral damage, their bonuses are effectively wasted.
		Therefore, I'm going to inflate the value of collateral damage based
		on a rough estimate of the defenders bonuses. */

	TeamTypes ePlotBonusTeam = eDefenseTeam;
	if (ePlotBonusTeam == NO_TEAM)
		ePlotBonusTeam = (pPlot->getTeam() == eAttackTeam ? NO_TEAM : pPlot->getTeam());

	iBaseCollateral *= (pPlot->isCity() ? 130 : 110) +
			pPlot->defenseModifier(ePlotBonusTeam, false,
			eAttackTeam); // advc.012

	// Estimate the average collateral damage reduction of the units on the plot
	int iResistanceSum = 0;
	int iUnits = 0;

	FOR_EACH_UNIT_IN(pUnit, *pPlot)
	{
		if (!pUnit->canDefend(pPlot))
			continue;
		if (eDefenseTeam != NO_TEAM && pUnit->getTeam() != eDefenseTeam)
			continue;
		if (eAttackTeam != NO_TEAM && pUnit->getTeam() == eAttackTeam)
			continue;

		iUnits++;
		/*	Kludge! I'm only checking for immunity against the unit's own combat type.
			Ideally we'd know what kind of collateral damage we're expecting to be hit by,
			and check for immunity vs that.
			Or we could check all types... But the reality is, there are always
			going to be mods and fringe cases where the esitmate is inaccurate.
			And currently in K-Mod, all instances of immunity are to the unit's own type anyway.
			Whichever way we do the estimate, cho-ku-nu is going to mess it up anyway.
			(Unless I change the game mechanics.) */
		if ( // advc.001: Animals have no unit combat type (K146 also fixes this)
			pUnit->getUnitCombatType() != NO_UNITCOMBAT &&
			pUnit->getUnitInfo().getUnitCombatCollateralImmune(pUnit->getUnitCombatType()))
		{
			iResistanceSum += 100;
		}
		else iResistanceSum += pUnit->getCollateralDamageProtection();
	}
	if (iUnits > 0)
	{
		iBaseCollateral = iBaseCollateral * (iUnits * 100 - iResistanceSum) /
				(iUnits * 100);
	}

	return iBaseCollateral; // note, a factor of 100 is included in the result.
}


void setTradeItem(TradeData* pItem, TradeableItems eItemType, int iData)
{
	pItem->m_eItemType = eItemType;
	pItem->m_iData = iData;
	pItem->m_bOffering = false;
	pItem->m_bHidden = false;
}


void setListHelp(CvWString& szBuffer, wchar const* szStart, wchar const* szItem,
	wchar const* szSeparator, bool& bFirst) // advc: bool&
{
	if (bFirst)
		szBuffer += szStart;
	else szBuffer += szSeparator;
	szBuffer += szItem;
	bFirst = false; // advc: And deleted this line from every call location
}

// TODO: removed by advciv, find new location
int getDiscoverResearch(UnitTypes eUnit, PlayerTypes ePlayer, TechTypes eTech)
{
	int iResearch;
	CvUnitInfo& kUnitInfo = GC.getUnitInfo(eUnit);
	CvPlayer& kPlayer = GET_PLAYER(ePlayer);

	// Leoreth: slight base discover scaling
	iResearch = (kUnitInfo.getBaseDiscover() + (std::max(0, kPlayer.getCurrentEra()-1) * kUnitInfo.getBaseDiscover() / 2) + (kUnitInfo.getDiscoverMultiplier() * GET_TEAM(kPlayer.getTeam()).getTotalPopulation()));

	iResearch *= GC.getGameSpeedInfo(GC.getGame().getGameSpeedType()).getUnitDiscoverPercent();
	iResearch /= 100;

	return std::max(0, iResearch);
}

void setListHelp(CvWStringBuffer& szBuffer, wchar const* szStart, wchar const* szItem,
	wchar const* szSeparator, bool& bFirst) // advc: bool&
{
	if (bFirst)
		szBuffer.append(szStart);
	else szBuffer.append(szSeparator);
	szBuffer.append(szItem);
	bFirst = false; // advc: And deleted this line from every call location
}

// <advc> Based on the above
void setListHelp(CvWString& szBuffer, wchar const* szStart, wchar const* szItem,
	wchar const* szSeparator, int& iLastListID, int iListID)
{
	if (iLastListID != iListID)
		szBuffer += szStart;
	else szBuffer += szSeparator;
	szBuffer += szItem;
	iLastListID = iListID; // advc: And deleted this line from every call location
}

void setListHelp(CvWStringBuffer& szBuffer, wchar const* szStart, wchar const* szItem,
	wchar const* szSeparator, int& iLastListID, int iListID)
{
	if (iLastListID != iListID)
		szBuffer.append(szStart);
	else szBuffer.append(szSeparator);
	szBuffer.append(szItem);
	iLastListID = iListID; // advc: And deleted this line from every call location
} // </advc>

bool PUF_isGroupHead(CvUnit const* pUnit, int iDummy1, int iDummy2)
{
	FAssert(iDummy1 == -1 && iDummy2 == -1);
	return pUnit->isGroupHead();
}

bool PUF_isPlayer(CvUnit const* pUnit, int iOwner, int iForTeam)
{	// advc.061: rewritten
	TeamTypes eForTeam = (TeamTypes)iForTeam;
	PlayerTypes eOwner = (PlayerTypes)iOwner;
	FAssertEnumBounds(eOwner);
	if(eForTeam == NO_TEAM || eForTeam == TEAMID(eOwner))
		return (pUnit->getOwner() == eOwner);
	FAssertEnumBounds(eForTeam);
	return (pUnit->getOwner() == eOwner && !pUnit->isInvisible(eForTeam, false) &&
			!pUnit->getUnitInfo().isHiddenNationality());
}

bool PUF_isTeam(CvUnit const* pUnit, int iTeam, int iDummy)
{
	FAssert(iDummy == -1);
	TeamTypes eTeam = (TeamTypes)iTeam;
	FAssertEnumBounds(eTeam);
	return (pUnit->getTeam() == eTeam);
}

bool PUF_isCombatTeam(CvUnit const* pUnit, int iTeam, int iForTeam)
{
	TeamTypes eTeam = (TeamTypes)iTeam;
	FAssertEnumBounds(eTeam);
	TeamTypes eForTeam = (TeamTypes)iForTeam;
	FAssertEnumBounds(eForTeam);
	return (TEAMID(pUnit->getCombatOwner(eForTeam, pUnit->getPlot())) ==
			eTeam && !pUnit->isInvisible(eForTeam, false, false));
}

bool PUF_isOtherPlayer(CvUnit const* pUnit, int iPlayer, int iDummy)
{
	FAssert(iDummy == -1);
	PlayerTypes ePlayer = (PlayerTypes)iPlayer;
	FAssertEnumBounds(ePlayer);
	return (pUnit->getOwner() != ePlayer);
}

bool PUF_isOtherTeam(CvUnit const* pUnit, int iPlayer, int iDummy)
{
	FAssert(iDummy == -1);
	PlayerTypes ePlayer = (PlayerTypes)iPlayer;
	FAssertEnumBounds(ePlayer);
	TeamTypes eTeam = TEAMID(ePlayer);
	if (pUnit->canCoexistWithEnemyUnit(eTeam))
		return false;
	return (pUnit->getTeam() != eTeam);
}

bool PUF_canDefend(CvUnit const* pUnit, int iDummy1, int iDummy2)
{
	FAssert(iDummy1 == -1 && iDummy2 == -1);
	return pUnit->canDefend();
}

bool PUF_cannotDefend(const CvUnit* pUnit, int iDummy1, int iDummy2)
{
	FAssert(iDummy1 == -1 && iDummy2 == -1);
	return !pUnit->canDefend();
}

bool PUF_canDefendGroupHead(CvUnit const* pUnit, int iDummy1, int iDummy2)
{
	return (PUF_canDefend(pUnit, iDummy1, iDummy2) &&
			PUF_isGroupHead(pUnit, iDummy1, iDummy2));
}

bool PUF_canDefendPotentialEnemy(CvUnit const* pUnit, int iPlayer, BOOL iAlwaysHostile)
{
	return (PUF_canDefend(pUnit) && PUF_isPotentialEnemy(pUnit, iPlayer, iAlwaysHostile));
}

bool PUF_canDefendEnemy(CvUnit const* pUnit, int iPlayer, BOOL iAlwaysHostile)
{
	return (PUF_canDefend(pUnit) && PUF_isEnemy(pUnit, iPlayer, iAlwaysHostile));
}

bool PUF_isPotentialEnemy(CvUnit const* pUnit, int iPlayer, BOOL iAlwaysHostile)
{
	PlayerTypes ePlayer = (PlayerTypes)iPlayer;
	FAssertEnumBounds(ePlayer);
	FAssertBOOL(iAlwaysHostile);
	bool bAlwaysHostile = iAlwaysHostile;
	// advc: Switched the Our/Other variable names. It's iPlayer whose war plans matter.
	TeamTypes eOurTeam = TEAMID(ePlayer);
	TeamTypes eOtherTeam = TEAMID(pUnit->getCombatOwner(eOurTeam));
	if (pUnit->canCoexistWithEnemyUnit(eOurTeam))
		return false;
	return (bAlwaysHostile ? eOurTeam != eOtherTeam :
			GET_TEAM(eOurTeam).AI_mayAttack(eOtherTeam));
}

bool PUF_isEnemy(CvUnit const* pUnit, int iPlayer, BOOL iAlwaysHostile)
{
	PlayerTypes ePlayer = (PlayerTypes)iPlayer;
	FAssertEnumBounds(ePlayer);
	FAssertBOOL(iAlwaysHostile);
	bool bAlwaysHostile = iAlwaysHostile;
	// advc: Switched the Our/Other variable names
	TeamTypes eOurTeam = TEAMID(ePlayer);
	TeamTypes eOtherTeam = TEAMID(pUnit->getCombatOwner(eOurTeam));
	if (pUnit->canCoexistWithEnemyUnit(eOurTeam))
		return false;
	return (bAlwaysHostile ? eOurTeam != eOtherTeam :
			GET_TEAM(eOurTeam).isAtWar(eOtherTeam));
}

bool PUF_canDeclareWar(CvUnit const* pUnit, int iPlayer, BOOL iAlwaysHostile)
{
	PlayerTypes ePlayer = (PlayerTypes)iPlayer;
	FAssertEnumBounds(ePlayer);
	FAssertBOOL(iAlwaysHostile);
	bool bAlwaysHostile = iAlwaysHostile;
	/*	advc: Switched the Our/Other variable names. This function says whether
		iPlayer can declare war on the combat owner of pUnit. */
	TeamTypes eOurTeam = TEAMID(ePlayer);
	TeamTypes eOtherTeam = TEAMID(pUnit->getCombatOwner(eOurTeam));
	if (pUnit->canCoexistWithEnemyUnit(eOurTeam))
		return false;
	return (bAlwaysHostile ? false : GET_TEAM(eOurTeam).canDeclareWar(eOtherTeam));
}
// advc.ctr:
bool PUF_isEnemyCityAttacker(CvUnit const* pUnit, int iPlayer, int iAssumePeaceTeam)
{
	TeamTypes eAssumePeaceTeam = (TeamTypes)iAssumePeaceTeam;
	if (eAssumePeaceTeam != NO_TEAM)
	{
		FAssertEnumBounds(eAssumePeaceTeam);
		if (GET_TEAM(pUnit->getTeam()).getMasterTeam() == GET_TEAM(eAssumePeaceTeam).getMasterTeam())
			return false;
	}
	CvUnitInfo& u = pUnit->getUnitInfo();
	if (u.getCargoSpace() <= 0 || u.getSpecialCargo() != NO_SPECIALUNIT)
	{
		if (u.getDomainType() != DOMAIN_LAND)
			return false;
		if (u.isOnlyDefensive() || u.getCombat() <= 0)
			return false;
	}
	return PUF_isEnemy(pUnit, iPlayer, false);
}

// doc
// TODO: make sure this is used where appropriate
bool PUF_canDefendAgainst(const CvUnit* pUnit, int iData1, int iData2)
{
	// doc: Turkic UP
	if (pUnit->isBarbarian() && GET_PLAYER((PlayerTypes)iData1).getCivilizationType() == TURKS && GET_TEAM(GET_PLAYER((PlayerTypes)iData1).getTeam()).isAtWarWithMajorPlayer())
	{
		if (pUnit->getUnitCombatType() == 2 || pUnit->getUnitCombatType() == 3)
		{
			return false;
		}
	}

	return pUnit->canDefend();
}

bool PUF_isVisible(CvUnit const* pUnit, int iPlayer, int iDummy)
{
	FAssert(iDummy == -1);
	PlayerTypes ePlayer = (PlayerTypes)iPlayer;
	FAssertEnumBounds(ePlayer);
	return !pUnit->isInvisible(TEAMID(ePlayer), false);
}

bool PUF_isVisibleDebug(CvUnit const* pUnit, int iPlayer, int iDummy)
{
	FAssert(iDummy == -1);
	PlayerTypes ePlayer = (PlayerTypes)iPlayer;
	FAssertEnumBounds(ePlayer);
	return !pUnit->isInvisible(TEAMID(ePlayer), true);
}
// advc.298:
bool PUF_isLethal(CvUnit const* pUnit, int iDummy1, int iDummy2)
{
	FAssert(iDummy1 == -1 && iDummy2 == -1);
	return (pUnit->canAttack() && pUnit->combatLimit() >= 100);
}

bool PUF_canSiege(CvUnit const* pUnit, int iTargetPlayer, int iDummy)
{
	FAssert(iDummy == -1);
	PlayerTypes eTargetPlayer = (PlayerTypes)iTargetPlayer;
	FAssertEnumBounds(eTargetPlayer);
	return pUnit->canSiege(TEAMID(eTargetPlayer));
}

bool PUF_canAirAttack(CvUnit const* pUnit, int iDummy1, int iDummy2)
{
	FAssert(iDummy1 == -1 && iDummy2 == -1);
	return pUnit->canAirAttack();
}

bool PUF_canAirDefend(CvUnit const* pUnit, int iDummy1, int iDummy2)
{
	FAssert(iDummy1 == -1 && iDummy2 == -1);
	return pUnit->canAirDefend();
}
// K-Mod:
bool PUF_isAirIntercept(CvUnit const* pUnit, int iDummy1, int iDummy2)
{
	FAssert(iDummy1 == -1 && iDummy2 == -1);
	return (pUnit->getDomainType() == DOMAIN_AIR &&
			pUnit->getGroup()->getActivityType() == ACTIVITY_INTERCEPT);
}

bool PUF_isFighting(CvUnit const* pUnit, int iDummy1, int iDummy2)
{
	FAssert(iDummy1 == -1 && iDummy2 == -1);
	return pUnit->isFighting();
}

bool PUF_isAnimal(CvUnit const* pUnit, int iDummy1, int iDummy2)
{
	FAssert(iDummy1 == -1 && iDummy2 == -1);
	return pUnit->isAnimal();
}

bool PUF_isMilitaryHappiness(CvUnit const* pUnit, int iData1, int iDummy2)
{
	FAssert(iDummy2 == -1);
	// doc: only city owner units provide military happiness
	return (pUnit->isMilitaryHappiness() && (iData1 == -1 || pUnit->getOwner() == (PlayerTypes)iData1));
}

bool PUF_isInvestigate(CvUnit const* pUnit, int iDummy1, int iDummy2)
{
	FAssert(iDummy1 == -1 && iDummy2 == -1);
	// <advc.103>
	if(pUnit->hasMoved())
		return false; // </advc.103>
	return pUnit->isInvestigate();
}

bool PUF_isCounterSpy(CvUnit const* pUnit, int iDummy1, int iDummy2)
{
	FAssert(iDummy1 == -1 && iDummy2 == -1);
	return pUnit->isCounterSpy();
}

bool PUF_isSpy(CvUnit const* pUnit, int iDummy1, int iDummy2)
{
	FAssert(iDummy1 == -1 && iDummy2 == -1);
	return pUnit->isSpy();
}

bool PUF_isDomainType(CvUnit const* pUnit, int iDomain, int iDummy)
{
	FAssert(iDummy == -1);
	DomainTypes eDomain = (DomainTypes)iDomain;
	FAssertEnumBounds(eDomain);
	return (pUnit->getDomainType() == eDomain);
}

bool PUF_isUnitType(CvUnit const* pUnit, int iUnit, int iDummy)
{
	FAssert(iDummy == -1);
	UnitTypes eUnit = (UnitTypes)iUnit;
	FAssertEnumBounds(eUnit);
	return (pUnit->getUnitType() == eUnit);
}

bool PUF_isUnitAIType(CvUnit const* pUnit, int iUnitAI, int iDummy)
{
	FAssert(iDummy == -1);
	UnitAITypes eUnitAI = (UnitAITypes)iUnitAI;
	FAssertEnumBounds(eUnitAI);
	return (pUnit->AI_getUnitAIType() == eUnitAI);
}
// K-Mod:
bool PUF_isMissionAIType(CvUnit const* pUnit, int iMissionAI, int iDummy)
{
	FAssert(iDummy == -1);
	MissionAITypes eMissionAI = (MissionAITypes)iMissionAI;
	FAssertEnumBounds(eMissionAI);
	return (pUnit->AI().AI_getGroup()->AI_getMissionAIType() == eMissionAI);
}

bool PUF_isCityAIType(CvUnit const* pUnit, int iDummy1, int iDummy2)
{
	FAssert(iDummy1 == -1 && iDummy2 == -1);
	return pUnit->AI().AI_isCityAIType();
}

bool PUF_isNotCityAIType(CvUnit const* pUnit, int iDummy1, int iDummy2)
{
	return !PUF_isCityAIType(pUnit);
}
// advc.003j (comment): unused
bool PUF_isSelected(CvUnit const* pUnit, int iDummy1, int iDummy2)
{
	FAssert(iDummy1 == -1 && iDummy2 == -1);
	return pUnit->IsSelected();
}

/*bool PUF_isNoMission(CvUnit const* pUnit, int iDummy1, int iDummy2)
{
	FAssert(iDummy1 == -1 && iDummy2 == -1);
	//return (pUnit->getGroup()->getActivityType() != ACTIVITY_MISSION); // BtS
	return (pUnit->getGroup()->AI_getMissionAIType() == NO_MISSIONAI); // K-Mod
}*/
/*  advc.113b: The above won't do for counting the workers available to a city:
	Doesn't count retreated workers and does count workers in cargo. */
/*  Replacement: Count pUnit if its mission plot has the given city as its
	working city. If pUnit has no mission, then it's counted if its current plot
	has the given city as its working city. */
bool PUF_isMissionPlotWorkingCity(CvUnit const* pUnit, int iCity, int iCityOwner)
{
	CvCity* pCity = GET_PLAYER((PlayerTypes)iCityOwner).getCity(iCity);
	if(pCity == NULL || pUnit->isCargo())
		return false;
	CvPlot* pMissionPlot = pUnit->AI().AI_getGroup()->AI_getMissionAIPlot();
	if(pMissionPlot == NULL)
		pMissionPlot = pUnit->plot();
	return (pMissionPlot->getWorkingCity() == pCity);
}

bool PUF_isFiniteRange(CvUnit const* pUnit, int iDummy1, int iDummy2)
{
	FAssert(iDummy1 == -1 && iDummy2 == -1);
	return (pUnit->getDomainType() != DOMAIN_AIR || pUnit->getUnitInfo().getAirRange() > 0);
}
// BETTER_BTS_AI_MOD, General AI, 01/15/09, jdog5000: START
bool PUF_isAvailableUnitAITypeGroupie(CvUnit const* pUnit, int iUnitAI, int iDummy)
{	// (advc: Removed unnecessary helper function)
	return (PUF_isUnitAIType(pUnit->getGroup()->getHeadUnit(), iUnitAI) &&
			!pUnit->isCargo());
}

bool PUF_isFiniteRangeAndNotJustProduced(CvUnit const* pUnit, int iDummy1, int iDummy2)
{
	return (PUF_isFiniteRange(pUnit) &&
			GC.getGame().getGameTurn() - pUnit->getGameTurnCreated() > 1);
} // BETTER_BTS_AI_MOD: END

bool PUF_makeInfoBarDirty(CvUnit* pUnit, int iDummy1, int iDummy2)
{
	FAssert(iDummy1 == -1 && iDummy2 == -1);
	pUnit->setInfoBarDirty(true);
	return true;
}

// advc.003j (comment): Unused
int baseYieldToSymbol(int iNumYieldTypes, int iYieldStack)
{
	return iNumYieldTypes * GC.getDefineINT("MAX_YIELD_STACK") + iYieldStack;
}
/*  advc.003j: Vanilla Civ 4 function that used to be a DLLExport;
	certainly unused since BtS, and doesn't sound too useful. */
/*bool isPickableName(const TCHAR* szName) {
	if (szName) {
		int iLen = _tcslen(szName);
		if (!_tcsicmp(&szName[iLen-6], "NOPICK"))
			return false;
	}
	return true;
}*/

/*	advc: Akin to natGetDeterministicRandom (deleted from CvCity.cpp). For reference,
	the implementation of that function was:
	srand(7297 * iSeedX + 2909  * iSeedY);
	return (rand() % (iMax - iMin)) + iMin; */
int intHash(std::vector<int> const& kInputs, PlayerTypes ePlayer)
{
	int const iPrime = 31;
	int iHashVal = 0;
	for (size_t i = 0; i < kInputs.size(); i++)
	{
		iHashVal += kInputs[i];
		iHashVal *= iPrime;
	}
	int iCapitalIndex = -1;
	if (ePlayer != NO_PLAYER)
	{
		CvCity const* pCapital = GET_PLAYER(ePlayer).getCapital();
		if (pCapital != NULL)
			iCapitalIndex = pCapital->plotNum();
	}
	if (iCapitalIndex >= 0)
	{
		iHashVal += iCapitalIndex;
		iHashVal *= iPrime;
	}
	return iHashVal;
}


int getTurnYearForGame(int iGameTurn, int iStartYear, CalendarTypes eCalendar,
	GameSpeedTypes eSpeed)
{
	return getTurnMonthForGame(iGameTurn, iStartYear, eCalendar, eSpeed) /
			std::max(1, GC.getNumMonthInfos()); // advc: max
}


int getTurnMonthForGame(int iGameTurn, int iStartYear, CalendarTypes eCalendar,
	GameSpeedTypes eSpeed)
{
	int iTurnMonth = iStartYear * GC.getNumMonthInfos();
	switch (eCalendar)
	{
	case CALENDAR_DEFAULT:
	{
		int iTurnCount = 0;
		for (int i = 0; i < GC.getInfo(eSpeed).getNumTurnIncrements(); i++)
		{
			GameTurnInfo const& kGameTurn = GC.getInfo(eSpeed).getGameTurnInfo(i);
			if (iGameTurn > iTurnCount + kGameTurn.iNumGameTurnsPerIncrement)
			{
				iTurnMonth += kGameTurn.iMonthIncrement *
						kGameTurn.iNumGameTurnsPerIncrement;
				iTurnCount += kGameTurn.iNumGameTurnsPerIncrement;
			}
			else
			{
				iTurnMonth += kGameTurn.iMonthIncrement * (iGameTurn - iTurnCount);
				iTurnCount += iGameTurn - iTurnCount;
				break;
			}
		}
		if (iGameTurn > iTurnCount)
		{
			iTurnMonth += GC.getInfo(eSpeed).getGameTurnInfo(
					GC.getInfo(eSpeed).getNumTurnIncrements() - 1).
					iMonthIncrement * (iGameTurn - iTurnCount);
		}
		break;
	}
	case CALENDAR_BI_YEARLY:
		iTurnMonth += 2 * iGameTurn * GC.getNumMonthInfos();
		break;

	case CALENDAR_YEARS:
	case CALENDAR_TURNS:
		iTurnMonth += iGameTurn * GC.getNumMonthInfos();
		break;

	case CALENDAR_SEASONS:
		iTurnMonth += (iGameTurn * GC.getNumMonthInfos()) /
				std::max(1, GC.getNumSeasonInfos()); // advc: max
		break;

	case CALENDAR_MONTHS:
		iTurnMonth += iGameTurn;
		break;

	case CALENDAR_WEEKS:
		iTurnMonth += iGameTurn /
				std::max(1, GC.getDefineINT("WEEKS_PER_MONTHS")); // advc: max
		break;

	default:
		FAssert(false);
	}

	return iTurnMonth;
}


// doc (edead): convert normal speed turns to game speed turns
int getTurns(int iTurns)
{
	switch (GC.getGame().getGameSpeedType())
	{
	case GAMESPEED_MARATHON:
		return 3 * iTurns;
	case GAMESPEED_EPIC:
		if (iTurns == 3) return 5;
		else if (iTurns == 6) return 10;
		else return iTurns * 3 / 2;
	}

	return iTurns;
}

// doc (edead): convert year to turn number in current game speed
int getTurnForYear(int iTurnYear)
{
	return (getGameTurnForMonth(iTurnYear * GC.getNumMonthInfos(), GC.getGame().getStartYear(), GC.getGame().getCalendar(), GC.getGame().getGameSpeedType()));
}

// doc (edead): convert year to turn number in current game speed
int getGameTurnForYear(int iTurnYear, int iStartYear, CalendarTypes eCalendar, GameSpeedTypes eSpeed)
{
	return (getGameTurnForMonth(iTurnYear * GC.getNumMonthInfos(), iStartYear, eCalendar, eSpeed));
}

// doc (edead) convert month to turn number in current game speed
int getGameTurnForMonth(int iTurnMonth, int iStartYear, CalendarTypes eCalendar, GameSpeedTypes eSpeed)
{
	int iMonthCount;
	int iTurnCount;
	int iMonthIncrement;
	int iI;
	int iJ;

	iTurnMonth -= iStartYear * GC.getNumMonthInfos();
	iTurnCount = 0;
	iMonthCount = 0;

		for (iI = 0; iI < GC.getGameSpeedInfo(eSpeed).getNumTurnIncrements(); iI++)
		{
			if (iTurnMonth > (iMonthCount + GC.getGameSpeedInfo(eSpeed).getGameTurnInfo(iI).iMonthIncrement * GC.getGameSpeedInfo(eSpeed).getGameTurnInfo(iI).iNumGameTurnsPerIncrement))
			{
				iMonthCount += (GC.getGameSpeedInfo(eSpeed).getGameTurnInfo(iI).iMonthIncrement * GC.getGameSpeedInfo(eSpeed).getGameTurnInfo(iI).iNumGameTurnsPerIncrement);
				iTurnCount += GC.getGameSpeedInfo(eSpeed).getGameTurnInfo(iI).iNumGameTurnsPerIncrement;
			}
			else
			{
				for (iJ = 0; iJ < GC.getGameSpeedInfo(eSpeed).getGameTurnInfo(iI).iNumGameTurnsPerIncrement; iJ++)
				{
					iMonthIncrement = GC.getGameSpeedInfo(eSpeed).getGameTurnInfo(iI).iMonthIncrement;
					iMonthCount += iMonthIncrement;
					if (iMonthCount >= (iTurnMonth + iMonthIncrement/2))
						break;
					iTurnCount++;
				}
				break;
			}
		}

	return iTurnCount;
}

// doc: active scenario
ScenarioTypes getScenario()
{
	return GC.getMap().getScenario();
}

// doc: active scenario start year
int getScenarioStartYear(ScenarioTypes eScenario)
{
	if (eScenario == NO_SCENARIO)
	{
		eScenario = getScenario();
	}

	if (eScenario == SCENARIO_3000BC) return -3000;
	else if (eScenario == SCENARIO_600AD) return 600;
	else return 1700;
}

// doc: active scenario start turn
int getScenarioStartTurn()
{
	return getTurnForYear(getScenarioStartYear());
}

// these string functions should only be used under chipotle cheat code (not internationalized)

void getDirectionTypeString(CvWString& szString, DirectionTypes eDirectionType)
{
	/*  advc.007: Turned this comment
		"these string functions should only be used under chipotle cheat code (not internationalized)"
		into an assertion: */
	FAssertMsg(gLogBBAI || GC.getGame().isDebugMode(), "getDirectionTypeString should only be used for Debug output");
	switch (eDirectionType)
	{
	case NO_DIRECTION: szString = L"NO_DIRECTION"; break;

	case DIRECTION_NORTH: szString = L"north"; break;
	case DIRECTION_NORTHEAST: szString = L"northeast"; break;
	case DIRECTION_EAST: szString = L"east"; break;
	case DIRECTION_SOUTHEAST: szString = L"southeast"; break;
	case DIRECTION_SOUTH: szString = L"south"; break;
	case DIRECTION_SOUTHWEST: szString = L"southwest"; break;
	case DIRECTION_WEST: szString = L"west"; break;
	case DIRECTION_NORTHWEST: szString = L"northwest"; break;

	default: szString = CvWString::format(L"UNKNOWN_DIRECTION(%d)", eDirectionType); break;
	}
}

void getCardinalDirectionTypeString(CvWString& szString, CardinalDirectionTypes eDirectionType)
{
	getDirectionTypeString(szString, cardinalDirectionToDirection(eDirectionType));
}

// advc.007: Removed the "ACTIVITY_" prefix from the strings b/c it takes up too much space.
void getActivityTypeString(CvWString& szString, ActivityTypes eActivityType)
{
	FAssertMsg(gLogBBAI || GC.getGame().isDebugMode(), "getActivityTypeString should only be used for Debug output"); // advc.007
	switch (eActivityType)
	{
	case NO_ACTIVITY: szString = L"NO_ACTIVITY"; break;

	case ACTIVITY_AWAKE: szString = L"AWAKE"; break;
	case ACTIVITY_HOLD: szString = L"HOLD"; break;
	case ACTIVITY_SLEEP: szString = L"SLEEP"; break;
	case ACTIVITY_HEAL: szString = L"HEAL"; break;
	case ACTIVITY_SENTRY: szString = L"SENTRY"; break;
	case ACTIVITY_INTERCEPT: szString = L"INTERCEPT"; break;
	case ACTIVITY_MISSION: szString = L"MISSION"; break;
// K-Mod. There were some missing activity strings...
/*#define case_string(x) case x: szString = L#x; break;
	case_string(ACTIVITY_PATROL)
	case_string(ACTIVITY_PLUNDER)
#undef case_string*/
// K-Mod end
	// <advc.007>
	case ACTIVITY_PATROL: szString = L"PATROL"; break;
	case ACTIVITY_PLUNDER: szString = L"PLUNDER"; break;
	// </advc.007>
	case ACTIVITY_BOARDED: szString = L"BOARDED"; break; // advc.075
	default: szString = CvWString::format(L"UNKNOWN_ACTIVITY(%d)", eActivityType); break;
	}
}

void getMissionTypeString(CvWString& szString, MissionTypes eMissionType)
{
	FAssertMsg(gLogBBAI || GC.getGame().isDebugMode(), "getMissionTypeString should only be used for Debug output"); // advc.007
	switch (eMissionType)
	{
	case NO_MISSION: szString = L"NO_MISSION"; break;

	case MISSION_MOVE_TO: szString = L"MISSION_MOVE_TO"; break;
	case MISSION_ROUTE_TO: szString = L"MISSION_ROUTE_TO"; break;
	case MISSION_MOVE_TO_UNIT: szString = L"MISSION_MOVE_TO_UNIT"; break;
	case MISSION_SKIP: szString = L"MISSION_SKIP"; break;
	case MISSION_SLEEP: szString = L"MISSION_SLEEP"; break;
	case MISSION_FORTIFY: szString = L"MISSION_FORTIFY"; break;
	case MISSION_PLUNDER: szString = L"MISSION_PLUNDER"; break;
	case MISSION_AIRPATROL: szString = L"MISSION_AIRPATROL"; break;
	case MISSION_SEAPATROL: szString = L"MISSION_SEAPATROL"; break;
	case MISSION_HEAL: szString = L"MISSION_HEAL"; break;
	case MISSION_SENTRY_HEAL: szString = L"MISSION_SENTRY_HEAL"; break; // advc.004l
	case MISSION_SENTRY: szString = L"MISSION_SENTRY"; break;
	case MISSION_AIRLIFT: szString = L"MISSION_AIRLIFT"; break;
	case MISSION_NUKE: szString = L"MISSION_NUKE"; break;
	case MISSION_RECON: szString = L"MISSION_RECON"; break;
	case MISSION_PARADROP: szString = L"MISSION_PARADROP"; break;
	case MISSION_AIRBOMB: szString = L"MISSION_AIRBOMB"; break;
	case MISSION_BOMBARD: szString = L"MISSION_BOMBARD"; break;
	case MISSION_PILLAGE: szString = L"MISSION_PILLAGE"; break;
	case MISSION_SABOTAGE: szString = L"MISSION_SABOTAGE"; break;
	case MISSION_DESTROY: szString = L"MISSION_DESTROY"; break;
	case MISSION_STEAL_PLANS: szString = L"MISSION_STEAL_PLANS"; break;
	case MISSION_FOUND: szString = L"MISSION_FOUND"; break;
	case MISSION_SPREAD: szString = L"MISSION_SPREAD"; break;
	case MISSION_SPREAD_CORPORATION: szString = L"MISSION_SPREAD_CORPORATION"; break;
	case MISSION_JOIN: szString = L"MISSION_JOIN"; break;
	case MISSION_CONSTRUCT: szString = L"MISSION_CONSTRUCT"; break;
	case MISSION_DISCOVER: szString = L"MISSION_DISCOVER"; break;
	case MISSION_HURRY: szString = L"MISSION_HURRY"; break;
	case MISSION_TRADE: szString = L"MISSION_TRADE"; break;
	case MISSION_GREAT_WORK: szString = L"MISSION_GREAT_WORK"; break;
	case MISSION_INFILTRATE: szString = L"MISSION_INFILTRATE"; break;
	case MISSION_GOLDEN_AGE: szString = L"MISSION_GOLDEN_AGE"; break;
	case MISSION_BUILD: szString = L"MISSION_BUILD"; break;
	case MISSION_LEAD: szString = L"MISSION_LEAD"; break;
	case MISSION_ESPIONAGE: szString = L"MISSION_ESPIONAGE"; break;
	case MISSION_RESOLVE_CRISIS: szString = L"MISSION_RESOLVE_CRISIS"; break; // doc
	case MISSION_REFORM_GOVERNMENT: szString = L"MISSION_REFORM_GOVERNMENT"; break; // doc
	case MISSION_DIPLOMATIC_MISSION: szString = L"MISSION_DIPLOMATIC_MISSION"; break; // doc
	case MISSION_PERSECUTE: szString = L"MISSION_PERSECUTION"; break; // doc
	case MISSION_GREAT_MISSION: szString = L"MISSION_GREAT_MISSION"; break; // doc
	case MISSION_SATELLITE_ATTACK: szString = L"MISSION_SATELLITE_ATTACK"; break; // doc
	case MISSION_REBUILD: szString = L"MISSION_REBUILD"; break; // doc

	case MISSION_DIE_ANIMATION: szString = L"MISSION_DIE_ANIMATION"; break;

	case MISSION_BEGIN_COMBAT: szString = L"MISSION_BEGIN_COMBAT"; break;
	case MISSION_END_COMBAT: szString = L"MISSION_END_COMBAT"; break;
	case MISSION_AIRSTRIKE: szString = L"MISSION_AIRSTRIKE"; break;
	case MISSION_SURRENDER: szString = L"MISSION_SURRENDER"; break;
	case MISSION_CAPTURED: szString = L"MISSION_CAPTURED"; break;
	case MISSION_IDLE: szString = L"MISSION_IDLE"; break;
	case MISSION_DIE: szString = L"MISSION_DIE"; break;
	case MISSION_DAMAGE: szString = L"MISSION_DAMAGE"; break;
	case MISSION_MULTI_SELECT: szString = L"MISSION_MULTI_SELECT"; break;
	case MISSION_MULTI_DESELECT: szString = L"MISSION_MULTI_DESELECT"; break;

	default: szString = CvWString::format(L"UNKOWN_MISSION(%d)", eMissionType); break;
	}
}

// advc.007: Removed the "MISSIONAI_" prefix from the strings b/c it takes up too much space.
void getMissionAIString(CvWString& szString, MissionAITypes eMissionAI)
{
	FAssertMsg(gLogBBAI || GC.getGame().isDebugMode(), "getMissionAIString should only be used for Debug output"); // advc.007
	switch (eMissionAI)
	{
	case NO_MISSIONAI: szString = L"NO_MISSIONAI"; break;

	case MISSIONAI_SHADOW: szString = L"SHADOW"; break;
	case MISSIONAI_GROUP: szString = L"GROUP"; break;
	case MISSIONAI_LOAD_ASSAULT: szString = L"LOAD_ASSAULT"; break;
	case MISSIONAI_LOAD_SETTLER: szString = L"LOAD_SETTLER"; break;
	case MISSIONAI_LOAD_SPECIAL: szString = L"LOAD_SPECIAL"; break;
	case MISSIONAI_GUARD_CITY: szString = L"GUARD_CITY"; break;
	case MISSIONAI_GUARD_BONUS: szString = L"GUARD_BONUS"; break;
	case MISSIONAI_GUARD_SPY: szString = L"GUARD_SPY"; break;
	case MISSIONAI_ATTACK_SPY: szString = L"ATTACK_SPY"; break;
	case MISSIONAI_SPREAD: szString = L"SPREAD"; break;
	case MISSIONAI_CONSTRUCT: szString = L"CONSTRUCT"; break;
	case MISSIONAI_HURRY: szString = L"HURRY"; break;
	case MISSIONAI_GREAT_WORK: szString = L"GREAT_WORK"; break;
	case MISSIONAI_EXPLORE: szString = L"EXPLORE"; break;
	case MISSIONAI_BLOCKADE: szString = L"BLOCKADE"; break;
	case MISSIONAI_PILLAGE: szString = L"PILLAGE"; break;
	case MISSIONAI_FOUND: szString = L"FOUND"; break;
	case MISSIONAI_BUILD: szString = L"BUILD"; break;
	case MISSIONAI_ASSAULT: szString = L"ASSAULT"; break;
	case MISSIONAI_CARRIER: szString = L"CARRIER"; break;
	case MISSIONAI_PICKUP: szString = L"PICKUP"; break;
	case MISSIONAI_CIRCUMNAVIGATE: szString = L"CIRCUMNAVIGATE"; break; // doc
	case MISSIONAI_REBUILD: szString = L"REBUILD"; break; // doc
// K-Mod
#define mission_string(x) case x: szString = L#x; break;
	mission_string(MISSIONAI_GUARD_COAST)
	mission_string(MISSIONAI_REINFORCE)
	mission_string(MISSIONAI_SPREAD_CORPORATION)
	mission_string(MISSIONAI_RECON_SPY)
	mission_string(MISSIONAI_JOIN_CITY)
	mission_string(MISSIONAI_TRADE)
	mission_string(MISSIONAI_INFILTRATE)
	mission_string(MISSIONAI_CHOKE)
	mission_string(MISSIONAI_HEAL)
	mission_string(MISSIONAI_RETREAT)
	mission_string(MISSIONAI_PATROL)
	mission_string(MISSIONAI_DEFEND)
	mission_string(MISSIONAI_COUNTER_ATTACK)
	mission_string(MISSIONAI_UPGRADE)
	mission_string(MISSIONAI_STRANDED)
#undef mission_string
// K-Mod end
	default: szString = CvWString::format(L"UNKOWN_MISSION_AI(%d)", eMissionAI); break;
	}
}

void getUnitAIString(CvWString& szString, UnitAITypes eUnitAI)
{
	FAssertMsg(gLogBBAI || GC.getGame().isDebugMode(), "getUnitAIString should only be used for Debug output"); // advc.007

	// note, GC.getInfo(eUnitAI).getDescription() is a international friendly way to get string (but it will be longer)

	switch (eUnitAI)
	{
	case NO_UNITAI: szString = L"no unitAI"; break;

	case UNITAI_UNKNOWN: szString = L"unknown"; break;
	case UNITAI_ANIMAL: szString = L"animal"; break;
	case UNITAI_SETTLE: szString = L"settle"; break;
	case UNITAI_WORKER: szString = L"worker"; break;
	case UNITAI_ATTACK: szString = L"attack"; break;
	case UNITAI_ATTACK_CITY: szString = L"attack city"; break;
	case UNITAI_COLLATERAL: szString = L"collateral"; break;
	case UNITAI_PILLAGE: szString = L"pillage"; break;
	case UNITAI_RESERVE: szString = L"reserve"; break;
	case UNITAI_COUNTER: szString = L"counter"; break;
	case UNITAI_CITY_DEFENSE: szString = L"city defense"; break;
	case UNITAI_CITY_COUNTER: szString = L"city counter"; break;
	case UNITAI_CITY_SPECIAL: szString = L"city special"; break;
	case UNITAI_EXPLORE: szString = L"explore"; break;
	case UNITAI_MISSIONARY: szString = L"missionary"; break;
	case UNITAI_PROPHET: szString = L"prophet"; break;
	case UNITAI_ARTIST: szString = L"artist"; break;
	case UNITAI_SCIENTIST: szString = L"scientist"; break;
	case UNITAI_GENERAL: szString = L"general"; break;
	case UNITAI_MERCHANT: szString = L"merchant"; break;
	case UNITAI_ENGINEER: szString = L"engineer"; break;
	case UNITAI_GREAT_SPY: szString = L"great spy"; break; // K-Mod
	case UNITAI_SPY: szString = L"spy"; break;
	case UNITAI_ICBM: szString = L"icbm"; break;
	case UNITAI_WORKER_SEA: szString = L"worker sea"; break;
	case UNITAI_ATTACK_SEA: szString = L"attack sea"; break;
	case UNITAI_RESERVE_SEA: szString = L"reserve sea"; break;
	case UNITAI_ESCORT_SEA: szString = L"escort sea"; break;
	case UNITAI_EXPLORE_SEA: szString = L"explore sea"; break;
	case UNITAI_ASSAULT_SEA: szString = L"assault sea"; break;
	case UNITAI_SETTLER_SEA: szString = L"settler sea"; break;
	case UNITAI_MISSIONARY_SEA: szString = L"missionary sea"; break;
	case UNITAI_SPY_SEA: szString = L"spy sea"; break;
	case UNITAI_CARRIER_SEA: szString = L"carrier sea"; break;
	case UNITAI_MISSILE_CARRIER_SEA: szString = L"missile carrier"; break;
	case UNITAI_PIRATE_SEA: szString = L"pirate sea"; break;
	case UNITAI_ATTACK_AIR: szString = L"attack air"; break;
	case UNITAI_DEFENSE_AIR: szString = L"defense air"; break;
	case UNITAI_CARRIER_AIR: szString = L"carrier air"; break;
	case UNITAI_MISSILE_AIR: szString = L"missile air"; break; // K-Mod (this string was missing)
	case UNITAI_PARADROP: szString = L"paradrop"; break;
	case UNITAI_ATTACK_CITY_LEMMING: szString = L"attack city lemming"; break;

	default: szString = CvWString::format(L"unknown(%d)", eUnitAI); break;
	}
}

bool isHumanVictoryWonder(BuildingTypes eBuilding, BuildingTypes eWonder, CivilizationTypes eCivilization)
{
	return eBuilding == eWonder &&
		GC.getGame().getActiveCivilizationType() == eCivilization &&
		GC.getGame().getGameTurn() == getTurnForYear(GC.getInfo(eCivilization).getStartingYear()) + getTurns(5);
}

void log(char* format, ...)
{
	static char buf[2048];
	_vsnprintf(buf, 2048 - 4, format, (char*)(&format + 1));
	gDLL->logMsg("sdkDbg.log", buf);
}

void log(CvWString message)
{
	gDLL->logMsg("sdkDbg.log", CvString(message));
}

void log(CvString logfile, CvString message)
{
	gDLL->logMsg(logfile, message);
}

void setDirty(InterfaceDirtyBits eDirtyBit, bool bNewValue)
{
	gDLL->getInterfaceIFace()->setDirty(eDirtyBit, bNewValue);
}
