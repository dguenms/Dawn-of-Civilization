#include "CvGameCoreDLL.h"
#include "CvGameTextMgr.h"
#include "CombatOdds.h"
#include "CvUnit.h"
#include "CvPlayer.h"
#include "CvBugOptions.h"

/*	advc: Cut from CvGameTextMgr.cpp
	(whereas getCombatOddsSpecific has moved to CombatOdds.h)
	Code from ADVANCED COMBAT ODDS v2.0, 3/11/09, PieceOfMind */

using namespace combat_odds;

// advc: Cut from setCombatPlotHelp
void CvGameTextMgr::setACOPlotHelp(CvWStringBuffer &szString,
	CvPlot const& kPlot, CvUnit const& kAttacker, CvUnit const& kDefender,
	int iView, /* advc.048: */ bool bBestOddsHelp)
{
	CvWString szTempBuffer;
	CvWString szTempBuffer2;
	// <advc.312>
	int iMaxXPAtt = GC.getDefineINT(CvGlobals::MAX_EXPERIENCE_PER_COMBAT);
	int iMaxXPDef = iMaxXPAtt;
	if (kAttacker.isBarbarian())
		iMaxXPDef -= 4;
	if(kDefender.isBarbarian())
		iMaxXPAtt -= 4;
	// </advc.312>
	/*	Change this to true when you need to spot errors,
		particular in the expected hit points calculations */
	bool const ACO_debug = BUGOption::isEnabled("ACO__Debug", false);

	/** phungus start **/
	/*bool bctrl; bctrl = GC.ctrlKey();
	if (bctrl) {// SWITCHAROO IS DISABLED IN V1.0.  Hopefully it will be available in the next version.
	 // At the moment is has issues when modifiers are present.
	CvUnit* swap = pAttacker; pAttacker = pDefender; pDefender = swap;
	CvPlot* pAttackerPlot = pAttacker->plot();
	CvPlot* pDefenderPlot = pDefender->plot(); }*/
	int iAttackerExperienceModifier = 0;
	int iDefenderExperienceModifier = 0;
	FOR_EACH_ENUM(Promotion)
	{
		if (kAttacker.isHasPromotion(eLoopPromotion) &&
			GC.getInfo(eLoopPromotion).getExperiencePercent() != 0)
		{
			iAttackerExperienceModifier += GC.getInfo(eLoopPromotion).getExperiencePercent();
		}
	}
	FOR_EACH_ENUM(Promotion)
	{
		if (kDefender.isHasPromotion(eLoopPromotion) &&
			GC.getInfo(eLoopPromotion).getExperiencePercent() != 0)
		{
			iDefenderExperienceModifier += GC.getInfo(eLoopPromotion).getExperiencePercent();
		}
	} /** phungus end **/ //thanks to phungus420

	/*	<advc> Get rid of some duplicate code, and make sure that it's consistent
		with change advc.001l. */
	Combatant att, def;
	bool const bHideFreeWins = BUGOption::isEnabled("ACO__IgnoreBarbFreeWins", false);
	initCombatants(kAttacker, kDefender, att, def, bHideFreeWins); // </advc>

	/** Many thanks to DanF5771 for some of these calculations! **/
	int const iDefenderHitLimit = std::max(0,
			kDefender.maxHitPoints() - kAttacker.combatLimit());

	// Barbarian related code
	//Are we not going to ignore barb free wins? If not, skip this section...
	/*	advc.001: Uh-huh. If we ignore/ hide the free wins,
		then no special treatment is needed here. */
	if (!bHideFreeWins)
	{
		CvPlayer const& kAttackerOwner = GET_PLAYER(kAttacker.getOwner());
		if (kDefender.isBarbarian())
		{
			if (!kAttackerOwner.isBarbarian() &&
				kAttackerOwner.getWinsVsBarbs() <
				kAttackerOwner.getFreeWinsVsBarbs())
			{
				szTempBuffer.Format(SETCOLR L"%d\n" ENDCOLR,
						TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
						kAttackerOwner.getFreeWinsVsBarbs()
						- kAttackerOwner.getWinsVsBarbs());
				szString.append(gDLL->getText("TXT_ACO_BarbFreeWinsLeft"));
				szString.append(szTempBuffer.GetCString());
			}
		}
		else
		{
			if (kAttacker.isBarbarian())
			{
				CvPlayer const& kDefenderOwner = GET_PLAYER(kDefender.getOwner());
				if (!kDefenderOwner.isBarbarian() &&
					kDefenderOwner.getWinsVsBarbs() <
					kDefenderOwner.getFreeWinsVsBarbs())
				{
					szTempBuffer.Format(SETCOLR L"%d\n" ENDCOLR,
							TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
							kDefenderOwner.getFreeWinsVsBarbs()
							- kDefenderOwner.getWinsVsBarbs());
					szString.append(gDLL->getText("TXT_ACO_BarbFreeWinsLeft"));
					szString.append(szTempBuffer.GetCString());
				}
			}
		}
	}


	//XP calculations
	int iExperience;
	if (kAttacker.combatLimit() < 100)
		iExperience = GC.getDefineINT(CvGlobals::EXPERIENCE_FROM_WITHDRAWL);
	else
	{
		iExperience = (kDefender.attackXPValue() * def.strength()) / att.strength();
		iExperience = ::range(iExperience, GC.getDefineINT(CvGlobals::MIN_EXPERIENCE_PER_COMBAT),
				iMaxXPAtt); // advc.312
	}
	//thanks to phungus420
	int iWithdrawXP = GC.getDefineINT(CvGlobals::EXPERIENCE_FROM_WITHDRAWL);

	int iDefExperienceKill = (kAttacker.defenseXPValue() * att.strength()) /
			def.strength();
	iDefExperienceKill = ::range(iDefExperienceKill,
			GC.getDefineINT(CvGlobals::MIN_EXPERIENCE_PER_COMBAT),
			iMaxXPDef); // advc.312

	int iBonusAttackerXP = (iExperience * iAttackerExperienceModifier) / 100;
	int iBonusDefenderXP = (iDefExperienceKill * iDefenderExperienceModifier) / 100;
	int iBonusWithdrawXP = (GC.getDefineINT(CvGlobals::EXPERIENCE_FROM_WITHDRAWL) *
			iAttackerExperienceModifier) / 100;


	/*	The following code adjusts the XP for barbarian encounters.
		In standard game, barb and animal xp cap is 10,5 respectively. */
	/**Thanks to phungus420 for the following block of code! **/ // advc (from MNAI): simplified
	if (kDefender.isBarbarian())
	{
		if (kDefender.isAnimal())
		{
			int iMaxExtraXP = std::max(0,
				GC.getDefineINT("ANIMAL_MAX_XP_VALUE") - kAttacker.getExperience());
			iExperience = range(iExperience, 0, iMaxExtraXP);
			iWithdrawXP = range(iWithdrawXP, 0, iMaxExtraXP);
			iBonusAttackerXP = range(iBonusAttackerXP, 0, iMaxExtraXP + iExperience);
			iBonusWithdrawXP = range(iBonusWithdrawXP, 0, iMaxExtraXP + iWithdrawXP);
		}
		else
		{
			int iMaxExtraXP = std::max(0,
				GC.getDefineINT("BARBARIAN_MAX_XP_VALUE") - kAttacker.getExperience());
			iExperience = range(iExperience, 0, iMaxExtraXP);
			iWithdrawXP = range(iWithdrawXP, 0, iMaxExtraXP);
			iBonusAttackerXP = range(iBonusAttackerXP, 0, iMaxExtraXP + iExperience);
			iBonusWithdrawXP = range(iBonusWithdrawXP, 0, iMaxExtraXP + iWithdrawXP);
		}
	}

	//szTempBuffer.Format(L"iNeededRoundsAttacker = %d\niNeededRoundsDefender = %d",iNeededRoundsAttacker,iNeededRoundsDefender);
	//szString.append(NEWLINE);szString.append(szTempBuffer.GetCString());
	//szTempBuffer.Format(L"kDefender.currHitPoints = %d\n-kDefender.maxHitPOints = %d\n + kAttacker.combatLimit = %d\n - 1 if\npAttackercomBatlimit equals kDefender.maxHitpoints\n=(%d == %d)\nall over iDamageToDefender = %d\n+1 = ...",
	//kDefender.currHitPoints(),kDefender.maxHitPoints(),kAttacker.combatLimit(),kAttacker.combatLimit(),kDefender.maxHitPoints(),iDamageToDefender);
	//szString.append(NEWLINE);szString.append(szTempBuffer.GetCString());


	//NOW WE CALCULATE SOME INTERESTING STUFF :)

	float E_HP_Att = 0;//expected damage dealt to attacker
	float E_HP_Def = 0;
	//Expected hitpoints for attacker if attacker withdraws (not the same as retreat)
	float E_HP_Att_Withdraw=0;
	//Expected hitpoints for attacker if attacker kills defender
	float E_HP_Att_Victory=0;
	//this one is predetermined easily
	int E_HP_Att_Retreat = kAttacker.currHitPoints() -
			(def.hitsToWin() - 1) * def.damagePerRound();
	float E_HP_Def_Withdraw=0;
	float E_HP_Def_Defeat=0; // if attacker dies
	//Note E_HP_Def is the same for if the attacker withdraws or dies

	float AttackerUnharmed = getCombatOddsSpecific(
			kAttacker, kDefender, 0, att.hitsToWin());
	float DefenderUnharmed = getCombatOddsSpecific(
			kAttacker, kDefender, def.hitsToWin(), 0);
	//attacker withdraws or retreats
	DefenderUnharmed += getCombatOddsSpecific(
			kAttacker, kDefender, def.hitsToWin() - 1, 0);
	// The probability the attacker exits combat with min HP
	float prob_bottom_Att_HP=0;
	// The probability the defender exits combat with min HP
	float prob_bottom_Def_HP=0;

	if (ACO_debug)
	{
		szTempBuffer.Format(L"E[HP ATTACKER]");
		//szString.append(NEWLINE);
		szString.append(szTempBuffer.GetCString());
	}
	// already covers both possibility of defender not being killed AND being killed
	for (int iHitsByDef = 0; iHitsByDef < def.hitsToWin(); iHitsByDef++)
	{
		//prob_attack[iHitsByDef] = getCombatOddsSpecific(pAttacker,pDefender,iHitsByDef,att.hitsToWin());
		E_HP_Att += (kAttacker.currHitPoints() - iHitsByDef * def.damagePerRound()) *
				getCombatOddsSpecific(
				kAttacker, kDefender, iHitsByDef, att.hitsToWin());
		if (ACO_debug)
		{
			szTempBuffer.Format(L"+%d * %.2f%%  (Def %d) (%d:%d)",
					kAttacker.currHitPoints() - iHitsByDef * def.damagePerRound(),
					100.0f * getCombatOddsSpecific(
					kAttacker, kDefender, iHitsByDef, att.hitsToWin()),
					iDefenderHitLimit, iHitsByDef, att.hitsToWin());
			szString.append(NEWLINE);
			szString.append(szTempBuffer.GetCString());
		}
	}
	E_HP_Att_Victory = E_HP_Att;//NOT YET NORMALISED
	E_HP_Att_Withdraw = E_HP_Att;//NOT YET NORMALIZED
	prob_bottom_Att_HP = getCombatOddsSpecific(
			kAttacker, kDefender, def.hitsToWin() - 1, att.hitsToWin());
	if(kAttacker.withdrawalProbability() > 0)
	{
		// if withdraw odds involved
		if (ACO_debug)
		{
			szTempBuffer.Format(L"Attacker retreat odds");
			szString.append(NEWLINE);
			szString.append(szTempBuffer.GetCString());
		}
		for (int iHitsByAtt = 0; iHitsByAtt < att.hitsToWin(); iHitsByAtt++)
		{
			E_HP_Att += ( (kAttacker.currHitPoints()) -
					(def.hitsToWin() - 1) * def.damagePerRound()) *
					getCombatOddsSpecific(
					kAttacker, kDefender, def.hitsToWin() - 1, iHitsByAtt);
			prob_bottom_Att_HP += getCombatOddsSpecific(
					kAttacker, kDefender, def.hitsToWin() - 1, iHitsByAtt);
			if (ACO_debug)
			{
				szTempBuffer.Format(L"+%d * %.2f%%  (Def %d) (%d:%d)",
						kAttacker.currHitPoints() -
						(def.hitsToWin() - 1) * def.damagePerRound(),
						100.0f * getCombatOddsSpecific(
						kAttacker, kDefender, def.hitsToWin() - 1, iHitsByAtt),
						kDefender.currHitPoints() - iHitsByAtt * att.damagePerRound(),
						def.hitsToWin() - 1, iHitsByAtt);
				szString.append(NEWLINE);
				szString.append(szTempBuffer.GetCString());
			}
		}
	}
	// finished with the attacker HP I think.

	if (ACO_debug)
	{
		szTempBuffer.Format(L"E[HP DEFENDER]\nOdds that attacker dies or retreats");
		szString.append(NEWLINE);
		szString.append(szTempBuffer.GetCString());
	}
	for (int iHitsByAtt = 0; iHitsByAtt < att.hitsToWin(); iHitsByAtt++)
	{
		//prob_defend[iHitsByAtt] = getCombatOddsSpecific(pAttacker,pDefender,def.hitsToWin(),iHitsByAtt);//attacker dies
		//prob_defend[iHitsByAtt] += getCombatOddsSpecific(pAttacker,pDefender,def.hitsToWin()-1,iHitsByAtt);//attacker retreats
		E_HP_Def += (kDefender.currHitPoints() - iHitsByAtt * att.damagePerRound()) *
				(getCombatOddsSpecific(
				kAttacker, kDefender, def.hitsToWin(), iHitsByAtt) +
				getCombatOddsSpecific(
				kAttacker, kDefender, def.hitsToWin() - 1, iHitsByAtt));
		if (ACO_debug)
		{
			szTempBuffer.Format(L"+%d * %.2f%%  (Att 0 or %d) (%d:%d)",
					kDefender.currHitPoints() - iHitsByAtt * att.damagePerRound(),
					100.0f * (getCombatOddsSpecific(
					kAttacker, kDefender, def.hitsToWin(), iHitsByAtt) +
					getCombatOddsSpecific(
					kAttacker, kDefender, def.hitsToWin() - 1, iHitsByAtt)),
					kAttacker.currHitPoints()- (def.hitsToWin() - 1)*
					def.damagePerRound(), def.hitsToWin(), iHitsByAtt);
			szString.append(NEWLINE);
			szString.append(szTempBuffer.GetCString());
		}
	}
	prob_bottom_Def_HP = getCombatOddsSpecific(
			kAttacker, kDefender, def.hitsToWin(), att.hitsToWin() - 1);
	//prob_bottom_Def_HP += getCombatOddsSpecific(kAttacker,kDefender,def.hitsToWin()-1,att.hitsToWin()-1);
	E_HP_Def_Defeat = E_HP_Def;
	E_HP_Def_Withdraw = 0;
	//if attacker has a combatLimit (eg. catapult)
	if (kAttacker.combatLimit() < kDefender.maxHitPoints())
	{
#if 0 // advc.001l: This can no longer occur
		if (kAttacker.combatLimit() == att.damagePerRound() * (att.hitsToWin() - 1))
		{
			/*	Then we have an odd situation because the last successful hit
				by an attacker will do 0 damage, and doing either iNeededRoundsAttacker
				or iNeededRoundsAttacker - 1 will cause the same damage */
			if (ACO_debug)
			{
				szTempBuffer.Format(L"Odds that attacker withdraws at combatLimit (abnormal)");
				szString.append(NEWLINE);
				szString.append(szTempBuffer.GetCString());
			}
			for (int iHitsByDef = 0; iHitsByDef < def.hitsToWin(); iHitsByDef++)
			{
				//prob_defend[iNeededRoundsAttacker-1] += getCombatOddsSpecific(pAttacker,pDefender,iHitsByDef,att.hitsToWin());//this is the defender at the combatLimit
				E_HP_Def += iDefenderHitLimit * getCombatOddsSpecific(
						kAttacker, kDefender, iHitsByDef, att.hitsToWin());
				//should be the same as
				//E_HP_Def += ( (kDefender.currHitPoints()) - (att.hitsToWIn()-1)*iDamageToDefender) * getCombatOddsSpecific(pAttacker,pDefender,iHitsByDef,att.hitsToWin());
				E_HP_Def_Withdraw += iDefenderHitLimit * getCombatOddsSpecific(
						kAttacker, kDefender, iHitsByDef, att.hitsToWin());
				prob_bottom_Def_HP += getCombatOddsSpecific(
						kAttacker, kDefender, iHitsByDef, att.hitsToWin());
				if (ACO_debug)
				{
					szTempBuffer.Format(L"+%d * %.2f%%  (Att %d) (%d:%d)",
							iDefenderHitLimit, 100.0f * getCombatOddsSpecific(
							kAttacker, kDefender, iHitsByDef, att.hitsToWin()),
							100 - iHitsByDef * def.damagePerRound(), iHitsByDef, att.hitsToWin());
					szString.append(NEWLINE);
					szString.append(szTempBuffer.GetCString());
				}
			}
		}
		else // normal situation
#else
		FAssert(kAttacker.combatLimit() != att.damagePerRound() * (att.hitsToWin() - 1));
#endif // advc.001l
		{
			if (ACO_debug)
			{
				szTempBuffer.Format(L"Odds that attacker withdraws at combatLimit (normal)",
						kAttacker.combatLimit());
				szString.append(NEWLINE);
				szString.append(szTempBuffer.GetCString());
			}

			for (int iHitsByDef = 0; iHitsByDef < def.hitsToWin(); iHitsByDef++)
			{

				E_HP_Def += iDefenderHitLimit * getCombatOddsSpecific(
						kAttacker, kDefender, iHitsByDef, att.hitsToWin());
				E_HP_Def_Withdraw += iDefenderHitLimit * getCombatOddsSpecific(
						kAttacker, kDefender, iHitsByDef, att.hitsToWin());
				prob_bottom_Def_HP += getCombatOddsSpecific(
						kAttacker, kDefender, iHitsByDef, att.hitsToWin());
				if (ACO_debug)
				{
					szTempBuffer.Format(L"+%d * %.2f%%  (Att %d) (%d:%d)",
							iDefenderHitLimit, 100.0f * getCombatOddsSpecific(
							kAttacker, kDefender, iHitsByDef, att.hitsToWin()),
							GC.getMAX_HIT_POINTS() - iHitsByDef * def.damagePerRound(),
							iHitsByDef, att.hitsToWin());
					szString.append(NEWLINE);
					szString.append(szTempBuffer.GetCString());
				}
			}
		}
	}
	if (ACO_debug)
		szString.append(NEWLINE);

	float Scaling_Factor = 1.6f;//how many pixels per 1% of odds

	float AttackerKillOdds = 0;
	float PullOutOdds = 0;//Withdraw odds
	float RetreatOdds = 0;
	float DefenderKillOdds = 0;

	// THE ALL-IMPORTANT COMBATRATIO
	float const CombatRatio = kAttacker.currCombatStr(NULL, NULL) /
			(float)kDefender.currCombatStr(&kPlot, &kAttacker);

	// These two values are simply for the Unrounded XP display
	float const AttXP = kDefender.attackXPValue() / CombatRatio;
	float const DefXP = kAttacker.defenseXPValue() * CombatRatio;

	// General odds
	//ie. we can kill the defender... I hope this is the most general form
	if (kAttacker.combatLimit() >= kDefender.maxHitPoints())
	{
		//float AttackerKillOdds = 0.0f;
		for (int iHitsByDef = 0; iHitsByDef < def.hitsToWin(); iHitsByDef++)
		{
			AttackerKillOdds += getCombatOddsSpecific(
					kAttacker, kDefender, iHitsByDef, att.hitsToWin());
		}
	}
	else
	{
		// else we cannot kill the defender (eg. catapults attacking)
		for (int iHitsByDef = 0; iHitsByDef < def.hitsToWin(); iHitsByDef++)
		{
			PullOutOdds += getCombatOddsSpecific(
					kAttacker, kDefender, iHitsByDef, att.hitsToWin());
		}
	}
	if (kAttacker.withdrawalProbability() > 0)
	{
		for (int iHitsByAtt = 0; iHitsByAtt < att.hitsToWin(); iHitsByAtt++)
		{
			RetreatOdds += getCombatOddsSpecific(
					kAttacker, kDefender, def.hitsToWin() - 1, iHitsByAtt);
		}
	}
	for (int iHitsByAtt = 0; iHitsByAtt < att.hitsToWin(); iHitsByAtt++)
	{
		DefenderKillOdds += getCombatOddsSpecific(
				kAttacker, kDefender, def.hitsToWin(), iHitsByAtt);
	}
	//this gives slight negative numbers sometimes, I think
	//DefenderKillOdds = 1.0f - (AttackerKillOdds + RetreatOdds + PullOutOdds);

	if (iView & BUGOption::getValue("ACO__ShowSurvivalOdds", 0))
	{
		szTempBuffer.Format(L"%.2f%%", 100.0f * (AttackerKillOdds + RetreatOdds + PullOutOdds));
		szTempBuffer2.Format(L"%.2f%%", 100.0f * (RetreatOdds + PullOutOdds + DefenderKillOdds));
		szString.append(gDLL->getText("TXT_ACO_SurvivalOdds"));
		szString.append(gDLL->getText("TXT_ACO_VS",
				szTempBuffer.GetCString(), szTempBuffer2.GetCString()));
		szString.append(NEWLINE);
	}

	if (kAttacker.withdrawalProbability() >= 100)
	{
		// a rare situation indeed
		szString.append(gDLL->getText("TXT_ACO_SurvivalGuaranteed"));
		szString.append(NEWLINE);
	}

	float const prob1 = 100.0f * (AttackerKillOdds + PullOutOdds);//up to win odds
	float const prob2 = prob1 + 100.0f * RetreatOdds;//up to retreat odds

	//float prob = 100.0f * (AttackerKillOdds+RetreatOdds + PullOutOdds); // advc: unused
	{
		int pixels_left = 199;// 1 less than 200 to account for right end bar
		// 1% per pixel // subtracting one to account for left end bar
		int pixels = (2 * ((int)(prob1 + 0.5)))-1;
		{
			int fullBlocks = pixels / 10;
			int lastBlock = pixels % 10;

			szString.append(L"<img=Art/ACO/green_bar_left_end.dds>");
			for (int i = 0; i < fullBlocks; ++i)
			{
				szString.append(L"<img=Art/ACO/green_bar_10.dds>");
				pixels_left -= 10;
			}
			if (lastBlock > 0)
			{
				szTempBuffer2.Format(L"<img=Art/ACO/green_bar_%d.dds>", lastBlock);
				szString.append(szTempBuffer2);
				pixels_left-= lastBlock;
			}
		}
		{	/*	advc (comment): I wonder if this is really as intended.
			'pixels' doesn't normally get reused. (Note that I've placed
			the surrounding braces; they're not in the original code.) */
			pixels = 2 * ((int)(prob2 + 0.5)) - (pixels+1);//the number up to the next one...
			int fullBlocks = pixels / 10;
			int lastBlock = pixels % 10;
			for (int i = 0; i < fullBlocks; ++i)
			{
				szString.append(L"<img=Art/ACO/yellow_bar_10.dds>");
				pixels_left -= 10;
			}
			if (lastBlock > 0)
			{
				szTempBuffer2.Format(L"<img=Art/ACO/yellow_bar_%d.dds>", lastBlock);
				szString.append(szTempBuffer2);
				pixels_left-= lastBlock;
			}

			fullBlocks = pixels_left / 10;
			lastBlock = pixels_left % 10;
			for (int i = 0; i < fullBlocks; ++i)
			{
				szString.append(L"<img=Art/ACO/red_bar_10.dds>");
			}
			if (lastBlock > 0)
			{
				szTempBuffer2.Format(L"<img=Art/ACO/red_bar_%d.dds>", lastBlock);
				szString.append(szTempBuffer2);
			}
		}
	}
	szString.append(L"<img=Art/ACO/red_bar_right_end.dds> ");


	szString.append(NEWLINE);
	if (kAttacker.combatLimit() >= kDefender.maxHitPoints())
	{
		szTempBuffer.Format(L": " SETCOLR L"%.2f%% " L"%d" ENDCOLR,
				TEXT_COLOR("COLOR_POSITIVE_TEXT"),
				100.0f * AttackerKillOdds, iExperience);
		szString.append(gDLL->getText("TXT_ACO_Victory"));
		szString.append(szTempBuffer.GetCString());
		if (iAttackerExperienceModifier > 0)
		{
			szTempBuffer.Format(SETCOLR L"+%d" ENDCOLR, TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
					iBonusAttackerXP);
			szString.append(szTempBuffer.GetCString());
		}

		szString.append(gDLL->getText("TXT_KEY_COLOR_POSITIVE"));
		szString.append(gDLL->getText("TXT_ACO_XP"));
		szString.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));
		szString.append("  (");
		szString.append(gDLL->getText("TXT_KEY_COLOR_POSITIVE"));
		szTempBuffer.Format(L"%.1f",
				E_HP_Att_Victory/AttackerKillOdds);
		szString.append(szTempBuffer.GetCString());
		szString.append(gDLL->getText("TXT_ACO_HP"));
		szString.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));
	}
	else
	{
		szTempBuffer.Format(L": " SETCOLR L"%.2f%% " L"%d" ENDCOLR,
				TEXT_COLOR("COLOR_POSITIVE_TEXT"),
				100.0f * PullOutOdds,
				GC.getDefineINT(CvGlobals::EXPERIENCE_FROM_WITHDRAWL));
		//iExperience,TEXT_COLOR("COLOR_POSITIVE_TEXT"), E_HP_Att_Victory/AttackerKillOdds);
		szString.append(gDLL->getText("TXT_ACO_Withdraw"));
		szString.append(szTempBuffer.GetCString());
		if (iAttackerExperienceModifier > 0)
		{
			szTempBuffer.Format(SETCOLR L"+%d" ENDCOLR,
					TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"), iBonusWithdrawXP);
			szString.append(szTempBuffer.GetCString());
		}

		szString.append(gDLL->getText("TXT_KEY_COLOR_POSITIVE"));
		szString.append(gDLL->getText("TXT_ACO_XP"));
		szString.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));
		szString.append("  (");
		szString.append(gDLL->getText("TXT_KEY_COLOR_POSITIVE"));
		szTempBuffer.Format(L"%.1f",E_HP_Att_Withdraw/PullOutOdds);
		szString.append(szTempBuffer.GetCString());
		szString.append(gDLL->getText("TXT_ACO_HP"));
		szString.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));
		szString.append(",");
		szString.append(gDLL->getText("TXT_KEY_COLOR_NEGATIVE"));
		szTempBuffer.Format(L"%d",iDefenderHitLimit);
		szString.append(szTempBuffer.GetCString());
		szString.append(gDLL->getText("TXT_ACO_HP"));
		szString.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));
	}
	szString.append(")");

	if (def.odds() == 0)
	{
		szString.append(gDLL->getText("TXT_ACO_GuaranteedNoDefenderHit"));
		DefenderKillOdds = 0.0f;
	}

	if (kAttacker.withdrawalProbability() > 0)//if there are retreat odds
	{
		szString.append(NEWLINE);
		//szString.append(gDLL->getText("TXT_ACO_Retreat"));
		szString.append(gDLL->getText("TXT_ACO_Retreat")); // advc.048b
		szTempBuffer.Format(L": " SETCOLR L"%.2f%% " ENDCOLR SETCOLR L"%d" ENDCOLR,
				TEXT_COLOR("COLOR_UNIT_TEXT"),
				100.0f * RetreatOdds,
				TEXT_COLOR("COLOR_POSITIVE_TEXT"),
				GC.getDefineINT(CvGlobals::EXPERIENCE_FROM_WITHDRAWL));
		szString.append(szTempBuffer.GetCString());
		if (iAttackerExperienceModifier > 0)
		{
			szTempBuffer.Format(SETCOLR L"+%d" ENDCOLR,
					TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"), iBonusWithdrawXP);
			szString.append(szTempBuffer.GetCString());
		}
		szString.append(gDLL->getText("TXT_KEY_COLOR_POSITIVE"));
		szString.append(gDLL->getText("TXT_ACO_XP"));
		szString.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));
		szString.append("  (");
		szTempBuffer.Format(SETCOLR L"%d" ENDCOLR ,
				TEXT_COLOR("COLOR_UNIT_TEXT"),E_HP_Att_Retreat);
		szString.append(szTempBuffer.GetCString());
		szString.append(gDLL->getText("TXT_ACO_HP_NEUTRAL"));
		szString.append(")");
		//szString.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));
	}

	szString.append(NEWLINE);
	szTempBuffer.Format(L": " SETCOLR L"%.2f%% " L"%d" ENDCOLR,
			TEXT_COLOR("COLOR_NEGATIVE_TEXT"),
			100.0f*DefenderKillOdds, iDefExperienceKill);
	szString.append(gDLL->getText("TXT_ACO_Defeat"));
	szString.append(szTempBuffer.GetCString());
	if (iDefenderExperienceModifier > 0)
	{
		szTempBuffer.Format(SETCOLR L"+%d" ENDCOLR,TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
				iBonusDefenderXP);
		szString.append(szTempBuffer.GetCString());
	}
	szString.append(gDLL->getText("TXT_KEY_COLOR_NEGATIVE"));
	szString.append(gDLL->getText("TXT_ACO_XP"));
	szString.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));
	szString.append("  (");
	szString.append(gDLL->getText("TXT_KEY_COLOR_NEGATIVE"));
	szTempBuffer.Format(L"%.1f",
			(def.odds() != 0 ? E_HP_Def_Defeat /
			(RetreatOdds + DefenderKillOdds) : 0.0));
	szString.append(szTempBuffer.GetCString());
	szString.append(gDLL->getText("TXT_ACO_HP"));
	szString.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));
	szString.append(")");

	// <advc.048> XP details moved up so that it appears right after the basic XP info above
	bool const bDoRange = ((iView & BUGOption::getValue("ACO__ShowExperienceRange", 0)) &&
			kAttacker.combatLimit() >= kDefender.maxHitPoints()); //medium and high only
	/*  Had to leave behind the part that shows the combat ratio; don't want
	that this early. */
	if(bDoRange) // </advc.048>
	{
		//we do an XP range display
		//This should hopefully now work for any max and min XP values.

		if (kAttacker.combatLimit() >= kDefender.maxHitPoints())
		{
			FAssert(/* advc.312: */ iMaxXPAtt
					//ensuring the differences is at least 1
					> GC.getDefineINT(CvGlobals::MIN_EXPERIENCE_PER_COMBAT));
			int const size = /* advc.312: */ iMaxXPAtt
					- GC.getDefineINT(CvGlobals::MIN_EXPERIENCE_PER_COMBAT);
			// advc.001 (based on kmodx): Dynamic array had leaked memory
			std::vector<float> CombatRatioThresholds(size, 0);
			for (int i = 0; i < size; i++) //setup the array
			{
				CombatRatioThresholds[i] = kDefender.attackXPValue()/(float)(
						/* <advc.312> */ iMaxXPAtt /* </advc.132> */ - i);
				//For standard game, this is the list created:
				//  {4/10, 4/9, 4/8,
				//   4/7, 4/6, 4/5,
				//   4/4, 4/3, 4/2}
			}
			for (int i = size - 1; i >= 0; i--) // find which range we are in
			{
				//starting at i = 8, going through to i = 0
				if (CombatRatio>CombatRatioThresholds[i])
				{
					if (i == size - 1)//highest XP value already
					{
						szString.append(NEWLINE);
						szTempBuffer.Format(L"(%.2f:%d",
								CombatRatioThresholds[i],
								GC.getDefineINT(CvGlobals::MIN_EXPERIENCE_PER_COMBAT) + 1);
						szString.append(szTempBuffer.GetCString());
						szString.append(gDLL->getText("TXT_ACO_XP"));
						szTempBuffer.Format(L"), (R=" SETCOLR L"%.2f" ENDCOLR
								L":" SETCOLR L"%d" ENDCOLR, // advc.048
								TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
								CombatRatio,
								TEXT_COLOR("COLOR_POSITIVE_TEXT"), // advc.048
								iExperience);
						szString.append(szTempBuffer.GetCString());
						szString.append(gDLL->getText("TXT_ACO_XP"));
						szString.append(")");
					}
					else // normal situation
					{
						szString.append(NEWLINE);
						szTempBuffer.Format(L"(%.2f:%d",
								CombatRatioThresholds[i],
								iMaxXPAtt // advc.312
								-i);
						szString.append(szTempBuffer.GetCString());
						szString.append(gDLL->getText("TXT_ACO_XP"));
						szTempBuffer.Format(L"), (R=" SETCOLR L"%.2f" ENDCOLR
								L":" SETCOLR L"%d" ENDCOLR, // advc.048
								TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
								CombatRatio,
								TEXT_COLOR("COLOR_POSITIVE_TEXT"), // advc.048
								iMaxXPAtt // advc.312
								-(i+1));
						szString.append(szTempBuffer.GetCString());
						szString.append(gDLL->getText("TXT_ACO_XP"));
						szTempBuffer.Format(L"), (>%.2f:%d",
								CombatRatioThresholds[i+1],
								iMaxXPAtt // advc.312
								-(i+2));
						szString.append(szTempBuffer.GetCString());
						szString.append(gDLL->getText("TXT_ACO_XP"));
						szString.append(")");
					}
					break;

				}
				else//very rare (ratio less than or equal to 0.4)
				{
					if (i==0)//maximum XP
					{
						szString.append(NEWLINE);
						szTempBuffer.Format(L"(R=" SETCOLR L"%.2f" ENDCOLR
								// <advc.048>
								L":" SETCOLR L"%d" ENDCOLR,
								/*  Was COLOR_POSITIVE_TEXT; reserve that
								for the XP. */
								TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
								// </advc.048>
								CombatRatio,
								TEXT_COLOR("COLOR_POSITIVE_TEXT"), // advc.048
								iMaxXPAtt); // advc.312
						szString.append(szTempBuffer.GetCString());

						szTempBuffer.Format(L"), (>%.2f:%d",
								CombatRatioThresholds[i],
								iMaxXPAtt // advc.312
								-1);
						szString.append(szTempBuffer.GetCString());
						szString.append(gDLL->getText("TXT_ACO_XP"));
						szString.append(")");
						break;
					}//if
				}// else if
			}//for
			//throw away the array
		}//if
	} // else if
	//Finished Showing XP range display
	// advc.048: Moved up so that it's shown right after the XP range
	if (iView & BUGOption::getValue("ACO__ShowUnroundedExperience", 2))
	{
		szTempBuffer.Format(L"%.2f", AttXP);
		szTempBuffer2.Format(L"%.2f", DefXP);
		szString.append(gDLL->getText("TXT_ACO_UnroundedXP"));
		szString.append(gDLL->getText("TXT_ACO_VS",
				szTempBuffer.GetCString(), szTempBuffer2.GetCString()));
	}
	/*	Probabilities lower than this (in percent) will
		not be shown individually for the HP detail section. */
	float HP_percent_cutoff = 0.5f;
	if (!BUGOption::isEnabled("ACO__MergeShortBars", true))
		HP_percent_cutoff = 0.0f;

	int last_combined_HP /* advc: */ = 0;
	float combined_HP_sum = 0;
	BOOL bCondensed = false;

	//START ATTACKER DETAIL HP HERE
	// Individual bars for each attacker HP outcome.
	if (iView & BUGOption::getValue("ACO__ShowAttackerHealthBars", 1))
	{
		int first_combined_HP_Att = 0;
		for (int iHitsByDef = 0; iHitsByDef < def.hitsToWin() - 1; iHitsByDef++)
		{
			float prob = 100.0f * getCombatOddsSpecific(
					kAttacker, kDefender, iHitsByDef, att.hitsToWin());
			if (prob > HP_percent_cutoff || iHitsByDef == 0)
			{
				if (bCondensed) // then we need to print the prev ones
				{
					{
						int pixels = (int)(Scaling_Factor*combined_HP_sum + 0.5);  // 1% per pixel
						int fullBlocks = (pixels) / 10;
						int lastBlock = (pixels) % 10;
						//if(pixels>=2) {szString.append(L"<img=Art/ACO/green_bar_left_end.dds>");}
						szString.append(NEWLINE);
						szString.append(L"<img=Art/ACO/green_bar_left_end.dds>");
						for (int iI = 0; iI < fullBlocks; ++iI)
						{
							szString.append(L"<img=Art/ACO/green_bar_10.dds>");
						}
						if (lastBlock > 0)
						{
							szTempBuffer2.Format(L"<img=Art/ACO/green_bar_%d.dds>", lastBlock);
							szString.append(szTempBuffer2);
						}
					}
					szString.append(L"<img=Art/ACO/green_bar_right_end.dds>");
					szString.append(L" ");

					szString.append(gDLL->getText("TXT_KEY_COLOR_POSITIVE"));
					if (last_combined_HP!=first_combined_HP_Att)
					{
						szTempBuffer.Format(L"%d",last_combined_HP);
						szString.append(szTempBuffer.GetCString());
						szString.append(gDLL->getText("TXT_ACO_HP"));
						szString.append(gDLL->getText("-"));
					}

					szTempBuffer.Format(L"%d",first_combined_HP_Att);
					szString.append(szTempBuffer.GetCString());
					szString.append(gDLL->getText("TXT_ACO_HP"));
					szString.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));
					szTempBuffer.Format(L" %.2f%%",combined_HP_sum);
					szString.append(szTempBuffer.GetCString());

					bCondensed = false;//resetting
					combined_HP_sum = 0.0f;//resetting this variable
					last_combined_HP = 0;
				}

				szString.append(NEWLINE);
				{
					int pixels = (int)(Scaling_Factor*prob + 0.5);  // 1% per pixel
					int fullBlocks = (pixels) / 10;
					int lastBlock = (pixels) % 10;
					szString.append(L"<img=Art/ACO/green_bar_left_end.dds>");
					for (int iI = 0; iI < fullBlocks; ++iI)
					{
						szString.append(L"<img=Art/ACO/green_bar_10.dds>");
					}
					if (lastBlock > 0)
					{
						szTempBuffer2.Format(L"<img=Art/ACO/green_bar_%d.dds>", lastBlock);
						szString.append(szTempBuffer2);
					}
				}
				szString.append(L"<img=Art/ACO/green_bar_right_end.dds>");
				szString.append(L" ");

				szString.append(gDLL->getText("TXT_KEY_COLOR_POSITIVE"));
				szTempBuffer.Format(L"%d",
						((kAttacker.currHitPoints()) - iHitsByDef * def.damagePerRound()));
				szString.append(szTempBuffer.GetCString());
				szString.append(gDLL->getText("TXT_ACO_HP"));
				szString.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));
				szTempBuffer.Format(L" %.2f%%", prob);
				szString.append(szTempBuffer.GetCString());
			}
			else // we add to the condensed list
			{
				bCondensed = true;
				first_combined_HP_Att = std::max(first_combined_HP_Att,
						(kAttacker.currHitPoints() - iHitsByDef * def.damagePerRound()));
				last_combined_HP = kAttacker.currHitPoints()
						- iHitsByDef * def.damagePerRound();
				combined_HP_sum += prob;
			}
		}

		if (bCondensed) // then we need to print the prev ones
		{
			szString.append(NEWLINE);
			{
				int pixels = (int)(Scaling_Factor * combined_HP_sum + 0.5);  // 1% per pixel
				int fullBlocks = (pixels) / 10;
				int lastBlock = (pixels) % 10;
				szString.append(L"<img=Art/ACO/green_bar_left_end.dds>");
				for (int iI = 0; iI < fullBlocks; ++iI)
				{
					szString.append(L"<img=Art/ACO/green_bar_10.dds>");
				}
				if (lastBlock > 0)
				{
					szTempBuffer2.Format(L"<img=Art/ACO/green_bar_%d.dds>", lastBlock);
					szString.append(szTempBuffer2);
				}
			}
			szString.append(L"<img=Art/ACO/green_bar_right_end.dds>");
			szString.append(L" ");

			szString.append(gDLL->getText("TXT_KEY_COLOR_POSITIVE"));
			if (last_combined_HP!=first_combined_HP_Att)
			{
				szTempBuffer.Format(L"%d",last_combined_HP);
				szString.append(szTempBuffer.GetCString());
				szString.append(gDLL->getText("TXT_ACO_HP"));
				szString.append(gDLL->getText("-"));
			}
			szTempBuffer.Format(L"%d",first_combined_HP_Att);
			szString.append(szTempBuffer.GetCString());
			szString.append(gDLL->getText("TXT_ACO_HP"));
			szString.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));
			szTempBuffer.Format(L" %.2f%%",combined_HP_sum);
			szString.append(szTempBuffer.GetCString());

			bCondensed = false;//resetting
			combined_HP_sum = 0;//resetting this variable
			last_combined_HP = 0;
		}
		/*  At the moment I am not allowing the lowest Attacker HP value to be condensed,
		as it would be confusing if it includes retreat odds.
		I may include this in the future though, but probably only if retreat odds are zero. */

		float const prob_victory = 100.0f * getCombatOddsSpecific(
				kAttacker, kDefender, def.hitsToWin() - 1, att.hitsToWin());
		float const prob_retreat = 100.0f * RetreatOdds;

		szString.append(NEWLINE);
		int green_pixels = (int)(Scaling_Factor*prob_victory + 0.5);
		/*	makes the total length of the bar more accurate -
			more important than the length of the pieces */
		int yellow_pixels = (int)(Scaling_Factor*(prob_retreat+prob_victory) + 0.5)
				- green_pixels;
		//we put an extra 2 on every one of the bar pixel counts
		green_pixels++;
		if (yellow_pixels>=1)
			yellow_pixels++;
		else green_pixels++;
		szString.append(L"<img=Art/ACO/green_bar_left_end.dds>");
		green_pixels--;

		green_pixels--;//subtracting off the right end
		{
			int fullBlocks = green_pixels / 10;
			int lastBlock = green_pixels % 10;
			for (int iI = 0; iI < fullBlocks; ++iI)
			{
				szString.append(L"<img=Art/ACO/green_bar_10.dds>");
			}
			if (lastBlock > 0)
			{
				szTempBuffer2.Format(L"<img=Art/ACO/green_bar_%d.dds>", lastBlock);
				szString.append(szTempBuffer2);
			}
		}
		if (yellow_pixels >= 1)// then there will at least be a right end yellow pixel
		{
			yellow_pixels--;//subtracting off right end
			int fullBlocks = yellow_pixels / 10;
			int lastBlock = yellow_pixels % 10;
			for (int iI = 0; iI < fullBlocks; ++iI)
			{
				szString.append(L"<img=Art/ACO/yellow_bar_10.dds>");
			}
			if (lastBlock > 0)
			{
				szTempBuffer2.Format(L"<img=Art/ACO/yellow_bar_%d.dds>", lastBlock);
				szString.append(szTempBuffer2);
			}
			szString.append(L"<img=Art/ACO/yellow_bar_right_end.dds>");
		}
		else szString.append(L"<img=Art/ACO/green_bar_right_end.dds>");

		szString.append(L" ");
		szString.append(gDLL->getText("TXT_KEY_COLOR_POSITIVE"));
		szTempBuffer.Format(L"%d", kAttacker.currHitPoints()
				- (def.hitsToWin() - 1) * def.damagePerRound());
		szString.append(szTempBuffer.GetCString());
		szString.append(gDLL->getText("TXT_ACO_HP"));
		szString.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));
		szTempBuffer.Format(L" %.2f%%", prob_victory + prob_retreat);
		szString.append(szTempBuffer.GetCString());
	}
	//END ATTACKER DETAIL HP HERE


	//START DEFENDER DETAIL HP HERE
	if (iView & BUGOption::getValue("ACO__ShowDefenderHealthBars", 2))
	{
		int first_combined_HP_Def = kDefender.currHitPoints();
		float prob = 0.0f;
		for (int iHitsByAtt = att.hitsToWin(); iHitsByAtt >= 1; iHitsByAtt--)//
		{	// a unit with a combat limit
			if (kAttacker.combatLimit() >= kDefender.maxHitPoints())
			{
				if (iHitsByAtt == att.hitsToWin())
					iHitsByAtt--;//we don't need to do HP for when the unit is dead.
			}

			int def_HP = std::max((kDefender.currHitPoints()) -
					iHitsByAtt * att.damagePerRound(),
					kDefender.maxHitPoints() - kAttacker.combatLimit());

			if ((kDefender.maxHitPoints() - kAttacker.combatLimit()) ==
				kDefender.currHitPoints() - (iHitsByAtt - 1) * att.damagePerRound())
			{
				// if abnormal
				if (iHitsByAtt == att.hitsToWin())
				{
					iHitsByAtt--;
					def_HP = (kDefender.maxHitPoints()  - kAttacker.combatLimit());
					prob += 100.0f*PullOutOdds;
					prob += 100.0f*(getCombatOddsSpecific(
						kAttacker, kDefender, def.hitsToWin(), iHitsByAtt)+
						getCombatOddsSpecific(
						kAttacker, kDefender, def.hitsToWin() - 1, iHitsByAtt));
				}
			}
			else
			{
				//not abnormal
				if (iHitsByAtt == att.hitsToWin())
					prob += 100.0f*PullOutOdds;
				else
				{
					prob += 100.0f * (getCombatOddsSpecific(
							kAttacker, kDefender, def.hitsToWin(), iHitsByAtt) +
							getCombatOddsSpecific(
							kAttacker, kDefender, def.hitsToWin() - 1, iHitsByAtt));
				}
			}

			if (prob > HP_percent_cutoff ||
				(kAttacker.combatLimit() < kDefender.maxHitPoints() &&
				iHitsByAtt == att.hitsToWin()))
			{
				if (bCondensed) // then we need to print the prev ones
				{
					szString.append(NEWLINE);
					{
						int pixels = (int)(Scaling_Factor*combined_HP_sum + 0.5);  // 1% per pixel
						int fullBlocks = (pixels) / 10;
						int lastBlock = (pixels) % 10;
						szString.append(L"<img=Art/ACO/red_bar_left_end.dds>");
						for (int i = 0; i < fullBlocks; i++)
						{
							szString.append(L"<img=Art/ACO/red_bar_10.dds>");
						}
						if (lastBlock > 0)
						{
							szTempBuffer2.Format(L"<img=Art/ACO/red_bar_%d.dds>", lastBlock);
							szString.append(szTempBuffer2);
						}
					}
					szString.append(L"<img=Art/ACO/red_bar_right_end.dds>");
					szString.append(L" ");
					szString.append(gDLL->getText("TXT_KEY_COLOR_NEGATIVE"));
					szTempBuffer.Format(L"%dHP",first_combined_HP_Def);
					szString.append(szTempBuffer.GetCString());
					szString.append(gDLL->getText("TXT_ACO_HP"));
					if (first_combined_HP_Def!=last_combined_HP)
					{
						szString.append("-");
						szTempBuffer.Format(L"%d",last_combined_HP);
						szString.append(szTempBuffer.GetCString());
						szString.append(gDLL->getText("TXT_ACO_HP"));
					}
					szString.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));
					szTempBuffer.Format(L" %.2f%%",
						combined_HP_sum);
					szString.append(szTempBuffer.GetCString());

					bCondensed = false;//resetting
					combined_HP_sum = 0.0f;//resetting this variable
				}

				szString.append(NEWLINE);
				{
					int pixels = (int)(Scaling_Factor * prob + 0.5);  // 1% per pixel
					int fullBlocks = pixels / 10;
					int lastBlock = pixels % 10;
					//if(pixels>=2) // this is now guaranteed by the way we define number of pixels
					//{
					szString.append(L"<img=Art/ACO/red_bar_left_end.dds>");
					for (int i = 0; i < fullBlocks; i++)
					{
						szString.append(L"<img=Art/ACO/red_bar_10.dds>");
					}
					if (lastBlock > 0)
					{
						szTempBuffer2.Format(L"<img=Art/ACO/red_bar_%d.dds>", lastBlock);
						szString.append(szTempBuffer2);
					}
				}
				szString.append(L"<img=Art/ACO/red_bar_right_end.dds>");

				szString.append(L" ");

				szTempBuffer.Format(SETCOLR L"%d" ENDCOLR,
					TEXT_COLOR("COLOR_NEGATIVE_TEXT"),def_HP);
				szString.append(szTempBuffer.GetCString());
				szString.append(gDLL->getText("TXT_KEY_COLOR_NEGATIVE"));
				szString.append(gDLL->getText("TXT_ACO_HP"));
				szString.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));
				szTempBuffer.Format(L" %.2f%%",prob);
				szString.append(szTempBuffer.GetCString());
			}
			else
			{
				bCondensed = true;
				first_combined_HP_Def = std::min(first_combined_HP_Def,def_HP);
				last_combined_HP = std::max(((kDefender.currHitPoints()) -
						iHitsByAtt * att.damagePerRound()), kDefender.maxHitPoints() -
						kAttacker.combatLimit());
				combined_HP_sum += prob;
			}
			prob = 0.0f;
		}

		if (bCondensed && att.hitsToWin() > 1) // then we need to print the prev ones
		/*	the reason we need att.hitsToWin() to be greater than 1 is
			that if it's equal to 1 then we end up with the
			defender detailed HP bar show up twice
			because it will also get printed below */
		{
			szString.append(NEWLINE);
			{
				int pixels = (int)(Scaling_Factor * combined_HP_sum + 0.5);  // 1% per pixel
				int fullBlocks = (pixels) / 10;
				int lastBlock = (pixels) % 10;
				//if(pixels>=2) {szString.append(L"<img=Art/ACO/green_bar_left_end.dds>");}
				szString.append(L"<img=Art/ACO/red_bar_left_end.dds>");
				for (int iI = 0; iI < fullBlocks; ++iI)
				{
					szString.append(L"<img=Art/ACO/red_bar_10.dds>");
				}
				if (lastBlock > 0)
				{
					szTempBuffer2.Format(L"<img=Art/ACO/red_bar_%d.dds>", lastBlock);
					szString.append(szTempBuffer2);
				}
			}
			szString.append(L"<img=Art/ACO/red_bar_right_end.dds>");
			szString.append(L" ");
			szString.append(gDLL->getText("TXT_KEY_COLOR_NEGATIVE"));
			szTempBuffer.Format(L"%d",first_combined_HP_Def);
			szString.append(szTempBuffer.GetCString());
			szString.append(gDLL->getText("TXT_ACO_HP"));
			if (first_combined_HP_Def != last_combined_HP)
			{
				szTempBuffer.Format(L"-%d",last_combined_HP);
				szString.append(szTempBuffer.GetCString());
				szString.append(gDLL->getText("TXT_ACO_HP"));
			}
			szString.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));
			szTempBuffer.Format(L" %.2f%%",combined_HP_sum);
			szString.append(szTempBuffer.GetCString());

			bCondensed = false;//resetting
			combined_HP_sum = 0.0f;//resetting this variable
		}

		//print the unhurt value...always

		prob = 100.0f * (getCombatOddsSpecific(
				kAttacker, kDefender, def.hitsToWin(), 0)+
				getCombatOddsSpecific(
				kAttacker, kDefender, def.hitsToWin() - 1,0));
		{
			int pixels = (int)(Scaling_Factor*prob + 0.5);  // 1% per pixel
			int fullBlocks = (pixels) / 10;
			int lastBlock = (pixels) % 10;
			szString.append(NEWLINE);
			szString.append(L"<img=Art/ACO/red_bar_left_end.dds>");
			for (int iI = 0; iI < fullBlocks; ++iI)
			{
				szString.append(L"<img=Art/ACO/red_bar_10.dds>");
			}
			if (lastBlock > 0)
			{
				szTempBuffer2.Format(L"<img=Art/ACO/red_bar_%d.dds>", lastBlock);
				szString.append(szTempBuffer2);
			}
		}
		szString.append(L"<img=Art/ACO/red_bar_right_end.dds>");
		szString.append(L" ");
		szString.append(gDLL->getText("TXT_KEY_COLOR_NEGATIVE"));
		szTempBuffer.Format(L"%d", kDefender.currHitPoints());
		szString.append(szTempBuffer.GetCString());
		szString.append(gDLL->getText("TXT_ACO_HP"));
		szString.append(gDLL->getText("TXT_KEY_COLOR_REVERT"));
		szTempBuffer.Format(L" %.2f%%",prob);
		szString.append(szTempBuffer.GetCString());
	}
	//END DEFENDER DETAIL HP HERE

	// advc.048: Avg. health and unharmed odds move up; placed right after bar diagrams.
	if (iView & BUGOption::getValue("ACO__ShowAverageHealth", 2))
	{
		szTempBuffer.Format(L"%.1f",E_HP_Att);
		szTempBuffer2.Format(L"%.1f",E_HP_Def);
		szString.append(gDLL->getText("TXT_ACO_AverageHP"));
		szString.append(gDLL->getText("TXT_ACO_VS", szTempBuffer.GetCString(),
			szTempBuffer2.GetCString()));
	}
	if (iView & BUGOption::getValue("ACO__ShowUnharmedOdds", 0))
	{
		szTempBuffer.Format(L"%.2f%%",100.0f*AttackerUnharmed);
		szTempBuffer2.Format(L"%.2f%%",100.0f*DefenderUnharmed);
		szString.append(gDLL->getText("TXT_ACO_Unharmed"));
		szString.append(gDLL->getText("TXT_ACO_VS", szTempBuffer.GetCString(),
			szTempBuffer2.GetCString()));
	}

	if (iView & BUGOption::getValue("ACO__ShowBasicInfo", 2))
	{	// advc.048: Opening parenthesis added
		szTempBuffer.Format(L"(" SETCOLR L"%d" ENDCOLR L", " SETCOLR L"%d " ENDCOLR,
				TEXT_COLOR("COLOR_POSITIVE_TEXT"), att.damagePerRound(),
				TEXT_COLOR("COLOR_NEGATIVE_TEXT"), def.damagePerRound());
		szString.append(NEWLINE);
		szString.append(szTempBuffer.GetCString());
		szString.append(gDLL->getText("TXT_ACO_HP"));
		szString.append(") "); // advc.048: Closing parenthesis added
		szString.append(gDLL->getText("TXT_ACO_MULTIPLY"));
		// advc.048: Opening parenthesis added
		szTempBuffer.Format(L" (" SETCOLR L"%d" ENDCOLR L", " SETCOLR L"%d " ENDCOLR,
				TEXT_COLOR("COLOR_POSITIVE_TEXT"), att.hitsToWin(),
				TEXT_COLOR("COLOR_NEGATIVE_TEXT"), def.hitsToWin());
		szString.append(szTempBuffer.GetCString());
		szString.append(gDLL->getText("TXT_ACO_HitsAt"));
		// advc.048: Closing parenthesis added
		szTempBuffer.Format(L")" SETCOLR L" %.1f%%" ENDCOLR,
				TEXT_COLOR("COLOR_POSITIVE_TEXT"),
				att.odds() * 100.0f / GC.getCOMBAT_DIE_SIDES());
		szString.append(szTempBuffer.GetCString());
	}
	/*  advc.048: The else branch of this conditional contained the XP range code,
		which has moved (way) up. */
	if(!bDoRange)
	{
		if (iView & BUGOption::getValue("ACO__ShowBasicInfo", 2))
		{	// advc.048: Semicolon instead of period
			szTempBuffer.Format(L"; R=" SETCOLR L"%.2f" ENDCOLR,
					TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),CombatRatio);
			szString.append(szTempBuffer.GetCString());
		}
	}
	// (advc.048: XP info, avg. health and unharmed odds moved up)
	szString.append(NEWLINE);

	if (iView & BUGOption::getValue("ACO__ShowShiftInstructions", 1))
	{	// <advc.048>
		CvWString szShiftHelp(gDLL->getText("TXT_ACO_PressSHIFT"));
		szString.append(szShiftHelp);
		if (bBestOddsHelp)
		{
			CvWString szAltHelp(gDLL->getText("TXT_ACO_PressALT"));
			/*  The translations don't fit in one line. 60 for the color tags,
			which don't take up space. */
			if(szShiftHelp.length() + szAltHelp.length() >= 50 + 60)
				szString.append(NEWLINE);
			else // Separator
			{
				szTempBuffer.Format(SETCOLR L", " ENDCOLR,
					TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"));
				szString.append(szTempBuffer.GetCString());
			}
			szString.append(szAltHelp);
		} // </advc.048>
		szString.append(NEWLINE);
	}
}

// advc: Cut from setCombatPlotHelp
void CvGameTextMgr::setACOModifiersPlotHelp(CvWStringBuffer &szString,
	CvPlot const& kPlot, CvUnit const& kAttacker, CvUnit const& kDefender,
	int iView)
{
	if (!szString.isEmpty()) // advc.001: for right click hover with air unit
		szString.append(NEWLINE);
	CvWString szTempBuffer;
	CvWString szTempBuffer2;
	szTempBuffer.Format(L"%.2f",
			kAttacker.getDomainType() == DOMAIN_AIR ?
			kAttacker.airCurrCombatStrFloat(&kDefender) :
			kAttacker.currCombatStrFloat(NULL, NULL));
	if (kAttacker.isHurt())
	{
		szTempBuffer.append(L" (");
		szTempBuffer.append(gDLL->getText("TXT_ACO_INJURED_HP",
				kAttacker.currHitPoints(),
				kAttacker.maxHitPoints()));
		szTempBuffer.append(L")");
	}
	szTempBuffer2.Format(L"%.2f",
			kDefender.currCombatStrFloat(&kPlot, &kAttacker));
	if (kDefender.isHurt())
	{
		szTempBuffer2.append(L" (");
		szTempBuffer2.append(gDLL->getText("TXT_ACO_INJURED_HP",
				kDefender.currHitPoints(),
				kDefender.maxHitPoints()));
		szTempBuffer2.append(L")");
	}
	szString.append(gDLL->getText("TXT_ACO_VS", szTempBuffer.GetCString(),
			szTempBuffer2.GetCString()));
	// advc.048: Moved attacker info above the modifier label
	if ((iView & BUGOption::getValue("ACO__ShowAttackerInfo", 3)))
	{
		szString.append(NEWLINE);
		setUnitHelp(szString, &kAttacker, true, true, /* advc.048: */ true);
	}
	if ((!kDefender.immuneToFirstStrikes() && kAttacker.maxFirstStrikes() > 0) ||
		kAttacker.maxCombatStr(NULL,NULL) != kAttacker.baseCombatStr() * 100)
	{
		/*	if attacker uninjured strength is not the same as base strength
			(i.e. modifiers are in effect) or first strikes exist, then ... */
		if (BUGOption::isEnabled("ACO__ShowModifierLabels", false))
			szString.append(gDLL->getText("TXT_ACO_AttackModifiers"));
	}
	//int iModifier = kAttacker.getExtraCombatPercent();
	/*	advc: (Generic modifiers of the attacker are the only ones that
		affect the attacker's combat strength) */
	appendCombatModifiers(szString, kPlot, kAttacker, kDefender, true, true, true);
	// <advc.048> Modifiers before 1st strikes (as in BtS)
	appendFirstStrikes(szString, kAttacker, kDefender, false);
	// Moved defender info above the modifier label ... // </advc.048>
	if (iView & BUGOption::getValue("ACO__ShowDefenderInfo", 3))
	{
		szString.append(NEWLINE);
		setUnitHelp(szString, &kDefender, true, true, /* advc.048: */ true);
	}
	if ((!kAttacker.immuneToFirstStrikes() && kDefender.maxFirstStrikes() > 0) ||
		kDefender.maxCombatStr(&kPlot, &kAttacker) != kDefender.baseCombatStr() * 100)
	{
		/*	if attacker uninjured strength is not the same as base strength
			(i.e. modifiers are in effect) or first strikes exist, then ... */
		if (BUGOption::isEnabled("ACO__ShowModifierLabels", false))
			szString.append(gDLL->getText("TXT_ACO_DefenseModifiers"));
	}

	if (iView & BUGOption::getValue("ACO__ShowDefenseModifiers", 3))
	{
		/*	advc: Use the same functions for ACO and BtS combat modifiers.
			(Replacing code that had been copy-pasted and slightly modified.) */
		/*	<advc.048> ACO shows modifiers tied to the defender's abilities first;
			I'm starting with the attacker (as in BtS). */
		appendCombatModifiers(szString, kPlot, kAttacker, kDefender,
				true, true, false, true);
		appendCombatModifiers(szString, kPlot, kAttacker, kDefender,
				false, true);
		appendFirstStrikes(szString, kDefender, kAttacker, true);
		// </advc.048>
	}
	if (iView & BUGOption::getValue("ACO__ShowTotalDefenseModifier", 2))
	{
		//szString.append(L' ');//XXX
		if (kDefender.maxCombatStr(&kPlot, &kAttacker) >
			kDefender.baseCombatStr() * 100)
		{	// modifier is positive
			szTempBuffer.Format(SETCOLR L"%d%%" ENDCOLR,
				TEXT_COLOR("COLOR_NEGATIVE_TEXT"),
				kDefender.maxCombatStr(&kPlot, &kAttacker) /
				kDefender.baseCombatStr() - 100);
		}
		else   // modifier is negative
		{
			szTempBuffer.Format(SETCOLR L"%d%%" ENDCOLR,
					TEXT_COLOR("COLOR_POSITIVE_TEXT"),
					100 - (kDefender.baseCombatStr() * 10000) /
					kDefender.maxCombatStr(&kPlot, &kAttacker));
		}

		szString.append(gDLL->getText("TXT_ACO_TotalDefenseModifier"));
		szString.append(szTempBuffer.GetCString());
	}
}
