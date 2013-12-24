// CvTextScreen.cpp

#include "CvGameCoreDLL.h"
#include "CvGameCoreUtils.h"
//#include "CvTextMgr.h"
#include "CvGlobals.h"

using namespace std;
typedef pair<int,int> intPair;

#define TEXT_COLOR_HIGHLIGHT 				((int)(GC.getColorInfo()[COLOR_HIGHLIGHT_TEXT].m_Color.r * 255)), ((int)(GC.getColorInfo()[COLOR_HIGHLIGHT_TEXT].m_Color.g * 255)), ((int)(GC.getColorInfo()[COLOR_HIGHLIGHT_TEXT].m_Color.b * 255)), ((int)(GC.getColorInfo()[COLOR_HIGHLIGHT_TEXT].m_Color.a * 255))
#define TEXT_COLOR_ALT_HIGHLIGHT		((int)(GC.getColorInfo()[COLOR_ALT_HIGHLIGHT_TEXT].m_Color.r * 255)), ((int)(GC.getColorInfo()[COLOR_ALT_HIGHLIGHT_TEXT].m_Color.g * 255)), ((int)(GC.getColorInfo()[COLOR_ALT_HIGHLIGHT_TEXT].m_Color.b * 255)), ((int)(GC.getColorInfo()[COLOR_ALT_HIGHLIGHT_TEXT].m_Color.a * 255))
#define FC_BULLETPOINT									gDLL->getSymbolID(BULLET_CHAR)
#define FC_HEALTHY										gDLL->getSymbolID(HEALTHY_CHAR)
#define FC_UNHEALTHY									gDLL->getSymbolID(UNHEALTHY_CHAR)
#define FC_ANGRY_POP_CHAR						gDLL->getSymbolID(ANGRY_POP_CHAR)
#define FC_GREAT_PERSON								gDLL->getSymbolID(GREAT_PERSON_CHAR)
#define FC_RELIGION										gDLL->getSymbolID(RELIGION_CHAR)
#define FC_BULLETPOINT									gDLL->getSymbolID(BULLET_CHAR)



#define SET_TEXT_HIGHLIGHT(helpString, colorFormat, colorValues, titleText) \
{ \
	sprintf(helpString, colorFormat, colorValues, titleText);		\
}


// IMPORTANT INFO
//
// When using sprintf() and strcat(), you should use a TCHAR. You must also initialize the TCHAR in order for it to work. ie: TCHAR szHelpString[1024];
// Remember to sprintf to handle formatting and save the formatted text to a buffer and then strcat() it to the return string - ie: szHelpString
// 
// ALWAYS SET THE BASE TCHAR PRIOR TO USING STRCAT

//
//	Build Leader Help Text
//
CvString CvTextScreen::buildLeaderInfoHelp( LeaderTypes eLeader, CivilizationTypes eCivilization )
{
	CvLeaderHeadInfo &pLeaderInfo = GC.getLeaderHeadInfo()[eLeader];
	CvCivilizationInfo &pCivInfo = GC.getCivilizationInfo()[eCivilization];
	vector<int> LeaderTraits;
	vector<int>::iterator traitIter;
	
	TCHAR szHelpString[1024];		// Final String Storage
	TCHAR szTempBuffer[1024];	// Formatting
	int iI; 

	//	Build help string
	if (eLeader != NO_LEADER)
	{
		SET_TEXT_HIGHLIGHT(szHelpString, "<COLOR:%d,%d,%d,%d>%s<REVERTCOLOR>", TEXT_COLOR_HIGHLIGHT, pLeaderInfo.getDescription());
		
		FAssert((GC.getNumTraitInfos() > 0) && 
			"GC.getNumTraitInfos() is less than or equal to zero but is expected to be larger than zero in CvSimpleCivPicker::setLeaderText");
		
		// Reserve enough slots for the total number of traits
		LeaderTraits.reserve(GC.getNumTraitInfos());
		// Build an int vector list of available trait infos
		for (iI = 0; iI < GC.getNumTraitInfos(); iI++)
		{
			if (pLeaderInfo.m_pbTraits[iI])
			{
				LeaderTraits.push_back(iI);
			}
		}

		// Check for no Traits and exit if that is the case
		if (LeaderTraits.empty())
		{
			strcat(szHelpString, "No Traits.");
			return CvString(szHelpString);
		}

		//	Add in here to this help string any info you want about the traits
		for (traitIter = LeaderTraits.begin(); traitIter != LeaderTraits.end(); ++traitIter)
		{
			// Loop Variables
			CvTraitInfo &pTraitInfo = GC.getTraitInfo()[*traitIter];	// Local version of TraitInfo
			vector<intPair> PromotionInfos;												// intPair Vector for handling Promotion Infos
			vector<intPair>::iterator promotionIter;								// its iterator
			BuildingTypes eLoopBuilding;
			UnitTypes eLoopUnit;
			int iLastPromotion = -1;
			int iLast;
			int iI, iJ;

			// Leader Name
			sprintf(szTempBuffer, "\n<COLOR:%d,%d,%d,%d>%s<REVERTCOLOR>", TEXT_COLOR_ALT_HIGHLIGHT, pTraitInfo.getDescription());
			strcat(szHelpString, szTempBuffer);
			
			// iHealth
			if (pTraitInfo.m_iHealth != 0)
			{
				sprintf(szTempBuffer, "\n %c+%d%c/City", FC_BULLETPOINT,  abs(pTraitInfo.m_iHealth), ((pTraitInfo.m_iHealth > 0) ? FC_HEALTHY : FC_UNHEALTHY));
				strcat(szHelpString, szTempBuffer);
			}

			// iMaxAnarchy
			if (pTraitInfo.m_iMaxAnarchy != -1)
			{
				if (pTraitInfo.m_iMaxAnarchy == 0)
				{
					sprintf(szTempBuffer, "\n  %cNo Anarchy %c", FC_BULLETPOINT, FC_ANGRY_POP_CHAR);
					strcat(szHelpString, szTempBuffer);
				}
				else
				{
					sprintf(szTempBuffer, "\n  %cMax %d turn%c of Anarchy", FC_BULLETPOINT, (pTraitInfo.m_iMaxAnarchy), ((pTraitInfo.m_iMaxAnarchy > 1) ? "s" : ""));
					strcat(szHelpString, szTempBuffer);
				}
			}

			// iGreatPersonRateModifier
			if (pTraitInfo.m_iGreatPersonRateModifier != 0)
			{
				sprintf(szTempBuffer, "\n  %c%s%d%% %c Birth Rate", FC_BULLETPOINT, 
					((pTraitInfo.m_iGreatPersonRateModifier > 0) ? "+" : ""), pTraitInfo.m_iGreatPersonRateModifier, FC_GREAT_PERSON);
				strcat(szHelpString, szTempBuffer);
			}

			// Wonder Production Effects
			if ((pTraitInfo.m_iMaxGlobalBuildingProductionModifier != 0) 
				|| (pTraitInfo.m_iMaxTeamBuildingProductionModifier != 0) 
				|| (pTraitInfo.m_iMaxPlayerBuildingProductionModifier != 0))
			{
				if ((pTraitInfo.m_iMaxGlobalBuildingProductionModifier == pTraitInfo.m_iMaxTeamBuildingProductionModifier) 
					&& 	(pTraitInfo.m_iMaxGlobalBuildingProductionModifier == pTraitInfo.m_iMaxPlayerBuildingProductionModifier))
				{
					sprintf(szTempBuffer, "\n  %c%s%d%% Wonder Production", FC_BULLETPOINT, 
						((pTraitInfo.m_iMaxGlobalBuildingProductionModifier > 0) ? "+" : ""), pTraitInfo.m_iMaxGlobalBuildingProductionModifier);
					strcat(szHelpString, szTempBuffer);
				}
				else
				{
					if (pTraitInfo.m_iMaxGlobalBuildingProductionModifier != 0)
					{
						sprintf(szTempBuffer, "\n  %c%s%d Great Wonder Production", FC_BULLETPOINT, 
							((pTraitInfo.m_iMaxGlobalBuildingProductionModifier > 0) ? "+" : ""), pTraitInfo.m_iMaxGlobalBuildingProductionModifier);
						strcat(szHelpString, szTempBuffer);
					}

					if (pTraitInfo.m_iMaxTeamBuildingProductionModifier != 0)
					{
						sprintf(szTempBuffer, "\n  %c%s%d Team Wonder Production", FC_BULLETPOINT, 
							((pTraitInfo.m_iMaxTeamBuildingProductionModifier > 0) ? "+" : ""), pTraitInfo.m_iMaxTeamBuildingProductionModifier);
						strcat(szHelpString, szTempBuffer);
					}

					if (pTraitInfo.m_iMaxPlayerBuildingProductionModifier != 0)
					{
						sprintf(szTempBuffer, "\n  %c%s%d National Wonder Production", FC_BULLETPOINT, 
							((pTraitInfo.m_iMaxPlayerBuildingProductionModifier > 0) ? "+" : ""), pTraitInfo.m_iMaxPlayerBuildingProductionModifier);
						strcat(szHelpString, szTempBuffer);
					}
				}
			}	
			// iReligionResearchModifier
			if (pTraitInfo.m_iReligiousResearchModifier != 0)
			{
				if (pTraitInfo.m_iReligiousResearchModifier == 100)
				{
					sprintf(szTempBuffer, "\n  %cHalf Cost %c Technologies", FC_BULLETPOINT, FC_RELIGION);
					strcat(szHelpString, szTempBuffer);
				}
				else
				{
					sprintf(szTempBuffer, 
						"\n  %cResearch %c Techs %d%% Faster", FC_BULLETPOINT, FC_RELIGION, 
						pTraitInfo.m_iReligiousResearchModifier);
					strcat(szHelpString, szTempBuffer);
				}
			}
			// bNoReligionMaintenance
			if (pTraitInfo.m_bNoReligionMaintenance)
			{
				sprintf(szTempBuffer, 
					"\n  %cNo State %c Maintenance", FC_BULLETPOINT, FC_RELIGION);
				strcat(szHelpString, szTempBuffer);
			}
			// ExtraYieldThresholds
			for (iI = 0; iI < NUM_YIELD_TYPES; iI++)
			{
				if (pTraitInfo.m_paiExtraYieldThreshold[iI] > 0)
				{
					sprintf(szTempBuffer, "\n  %c%s%d%c/Plot with %d%c", FC_BULLETPOINT, 
						((GC.getEXTRA_YIELD() > 0) ? "+" : ""), GC.getEXTRA_YIELD(), GC.getYieldInfo()[iI].m_iChar, 
						pTraitInfo.m_paiExtraYieldThreshold[iI], GC.getYieldInfo()[iI].m_iChar);
					strcat(szHelpString, szTempBuffer);
				}

				if (pTraitInfo.m_paiTradeYieldModifier[iI] != 0)
				{
					sprintf(szTempBuffer, "\n  %c%s%d%%%c from Trade", FC_BULLETPOINT, 
						((pTraitInfo.m_paiTradeYieldModifier[iI] > 0) ? "+" : ""), pTraitInfo.m_paiTradeYieldModifier[iI], GC.getYieldInfo()[iI].m_iChar);
					strcat(szHelpString, szTempBuffer);
				}
			}
			// CommerceChanges
			for (iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
			{
				if (pTraitInfo.m_paiCommerceChange[iI] != 0)
				{
					sprintf(szTempBuffer, "\n  %c%s%d%c/City", FC_BULLETPOINT, 
						((pTraitInfo.m_paiCommerceChange[iI] > 0) ? "+" : ""), pTraitInfo.m_paiCommerceChange[iI], GC.getCommerceInfo()[iI].m_iChar);
					strcat(szHelpString, szTempBuffer);
				}

				if (pTraitInfo.m_paiCommerceModifier[iI] != 0)
				{
					sprintf(szTempBuffer, "\n  %c%s%d%%%c", FC_BULLETPOINT, 
						((pTraitInfo.m_paiCommerceModifier[iI] > 0) ? "+" : ""), pTraitInfo.m_paiCommerceModifier[iI], GC.getCommerceInfo()[iI].m_iChar);
					strcat(szHelpString, szTempBuffer);
				}
			}
			// Free Promotions
			PromotionInfos.reserve(GC.getNumPromotionInfos());
			for (iI = 0; iI < GC.getNumPromotionInfos(); iI++)
			{
				if (pTraitInfo.m_pabFreePromotion[iI])
				{
					for (iJ = 0; iJ < GC.getNumUnitCombatInfos(); iJ++)
					{
						if (pTraitInfo.m_pabFreePromotionUnitCombat[iJ])
						{
							PromotionInfos.push_back(intPair(iI,iJ));
						}
					}
				}
			}
			// Adding Promotion Text
			if (!PromotionInfos.empty())
			{
				for (promotionIter = PromotionInfos.begin(); promotionIter != PromotionInfos.end(); ++promotionIter)
				{
					int iLoopPromotion = promotionIter->first;
					int iLoopUnitCombat = promotionIter->second;
					if (iLastPromotion == iLoopPromotion)
					{
						sprintf(szTempBuffer, "\n    %c%s", FC_BULLETPOINT, 
							GC.getUnitCombatInfo()[iLoopUnitCombat].getDescription());
						strcat(szHelpString, szTempBuffer);
					}
					else
					{
						sprintf(szTempBuffer, "\n  %cFree Promotion (%s)\n    %c%s", FC_BULLETPOINT, 
							GC.getPromotionInfo()[iLoopPromotion].getDescription(), 
							FC_BULLETPOINT,
							GC.getUnitCombatInfo()[iLoopUnitCombat].getDescription());
						strcat(szHelpString, szTempBuffer);
						iLastPromotion = iLoopPromotion;
					}
				}
			}
			// No Civic Maintenance
			for (iI = 0; iI < GC.getNumCivicOptionInfos(); iI++)
			{
				if (GC.getCivicOptionInfo()[iI].m_pabTraitNoMaintenance[*traitIter])
				{
					sprintf(szTempBuffer, "\n  %cNo Maintenance Cost for %s Civics", FC_BULLETPOINT, 
						GC.getCivicDescription(iI)); 
					strcat(szHelpString, szTempBuffer);
				}
			}
			// Increase Building/Unit Production Speeds
			iLast = 0;
			for (iI = 0; iI < GC.getNumSpecialUnitInfos(); iI++)
			{
				if (GC.getSpecialUnitInfo()[iI].m_piProductionTraits[*traitIter] != 0)
				{
					if (GC.getSpecialUnitInfo()[iI].m_piProductionTraits[*traitIter] == 100)
					{
						sprintf(szTempBuffer, "\n  %cHalf Cost ", FC_BULLETPOINT);
					}
					else
					{
						sprintf(szTempBuffer, "\n  %c%d%% Faster Construction ", FC_BULLETPOINT, 
							GC.getSpecialUnitInfo()[iI].m_piProductionTraits[*traitIter]);
					}
					setListHelp(szHelpString, szTempBuffer, 
						GC.getSpecialUnitInfo()[iI].getDescription(), ", ", 
						(GC.getSpecialUnitInfo()[iI].m_piProductionTraits[*traitIter] != iLast));
					iLast = GC.getSpecialUnitInfo()[iI].m_piProductionTraits[*traitIter];
				}
			}
			// Unit Classes
			if (eCivilization != NO_CIVILIZATION)
			{
				for (iI = 0; iI < GC.getNumUnitClassInfos();iI++)
				{
					eLoopUnit = ((UnitTypes)(GC.getCivilizationInfo()[eCivilization].m_piCivilizationUnits[iI]));

					if (eLoopUnit != NO_BUILDING)
					{
						if (GC.getUnitInfo()[eLoopUnit].m_piProductionTraits[*traitIter] != 0)
						{
							if (GC.getUnitInfo()[eLoopUnit].m_piProductionTraits[*traitIter] == 100)
							{
								sprintf(szTempBuffer, "\n  %cHalf Cost ", FC_BULLETPOINT);
							}
							else
							{
								sprintf(szTempBuffer, "\n  %c%d%% Faster Construction ", FC_BULLETPOINT, 
									GC.getUnitInfo()[eLoopUnit].m_piProductionTraits[*traitIter]);
							}
							setListHelp(szHelpString, szTempBuffer, 
								GC.getUnitInfo()[eLoopUnit].getDescription(), ", ", 
								(GC.getUnitInfo()[eLoopUnit].m_piProductionTraits[*traitIter] != iLast));
							iLast = GC.getUnitInfo()[eLoopUnit].m_piProductionTraits[*traitIter];
						}
					}
				}
			}
			iLast = 0;
			// SpecialBuildings
			for (iI = 0; iI < GC.getNumSpecialBuildingInfos(); iI++)
			{
				if (GC.getSpecialBuildingInfo()[iI].m_piProductionTraits[*traitIter] != 0)
				{
					if (GC.getSpecialBuildingInfo()[iI].m_piProductionTraits[*traitIter] == 100)
					{
						sprintf(szTempBuffer, "\n  %cHalf Cost ", FC_BULLETPOINT);
					}
					else
					{
						sprintf(szTempBuffer, "\n  %c%d%% Faster Construction ", FC_BULLETPOINT, 
							GC.getSpecialBuildingInfo()[iI].m_piProductionTraits[*traitIter]);
					}
					setListHelp(szHelpString, szTempBuffer, GC.getSpecialBuildingInfo()[iI].getDescription(), ", ", (GC.getSpecialBuildingInfo()[iI].m_piProductionTraits[*traitIter] != iLast));
					iLast = GC.getSpecialBuildingInfo()[iI].m_piProductionTraits[*traitIter];
				}
			}
			// Buildings
			if (eCivilization != NO_CIVILIZATION)
			{
				for (iI = 0; iI < GC.getNumBuildingClassInfos(); iI++)
				{
					eLoopBuilding = ((BuildingTypes)(GC.getCivilizationInfo()[eCivilization].m_piCivilizationBuildings[*traitIter]));

					if (eLoopBuilding != NO_BUILDING)
					{
						if (GC.getBuildingInfo()[eLoopBuilding].m_piProductionTraits[*traitIter] != 0)
						{
							if (GC.getBuildingInfo()[eLoopBuilding].m_piProductionTraits[*traitIter] == 100)
							{
								sprintf(szTempBuffer, "\n  %cHalf Cost ", FC_BULLETPOINT);
							}
							else
							{
								sprintf(szTempBuffer, "\n  %c%d%% Faster Construction ", FC_BULLETPOINT, 
									GC.getBuildingInfo()[eLoopBuilding].m_piProductionTraits[*traitIter]);
							}
							setListHelp(szHelpString, szTempBuffer, GC.getBuildingInfo()[eLoopBuilding].getDescription(), ", ", (GC.getBuildingInfo()[eLoopBuilding].m_piProductionTraits[*traitIter] != iLast));
							iLast = GC.getBuildingInfo()[eLoopBuilding].m_piProductionTraits[*traitIter];
						}
					}
				}
			}
		}
	}
	else
	{
		//	Random leader
		sprintf(szHelpString, "<COLOR:%d,%d,%d,%d>Unknown<REVERTCOLOR>", TEXT_COLOR_HIGHLIGHT);
	}

	return CvString(szHelpString);
}

//
// Build Civilization Info Help Text
//
CvString CvTextScreen::buildCivInfoHelp(CivilizationTypes eCivilization)
{
	CvCivilizationInfo &pCivInfo = GC.getCivilizationInfo()[eCivilization];
	TCHAR szInfoText[1024];
	TCHAR szBuffer[1024];
	
	if (eCivilization != NO_CIVILIZATION)
	{
		if (eCivilization != RANDOM_CIV)
		{
			// Civ Name
			sprintf(szInfoText, "<COLOR:%d,%d,%d,%d>%s<REVERTCOLOR>", TEXT_COLOR_HIGHLIGHT, pCivInfo.getDescription());

			// Free Techs
			sprintf(szBuffer, "\n\n<COLOR:%d,%d,%d,%d>Starting Techs:<REVERTCOLOR>", TEXT_COLOR_ALT_HIGHLIGHT);
			strcat(szInfoText, szBuffer);

			int iCounter = 0;
			for ( int iI = 0; iI < GC.getNumTechInfos(); iI++)
			{
				if (GC.getCivilizationInfo()[eCivilization].isCivilizationFreeTech(iI))
				{
					iCounter++;
					// Add Tech
					sprintf(szBuffer, "\n  %c%s", FC_BULLETPOINT, 
						GC.getTechInfo()[iI].getDescription());
					strcat(szInfoText, szBuffer);
				}
			}
			if (iCounter == 0)
			{
				strcat(szInfoText, "\n  No Free Techs");
			}
			// Free Units
			sprintf(szBuffer, 
				"\n\n<COLOR:%d,%d,%d,%d>Free Units:   (Replaces)<REVERTCOLOR>", TEXT_COLOR_ALT_HIGHLIGHT);
			strcat(szInfoText, szBuffer);

			iCounter = 0;
			for ( iI = 0; iI < GC.getNumUnitClassInfos(); iI++)
			{
				if (GC.getCivilizationInfo()[eCivilization].getCivilizationUnits(iI) != GC.getUnitClassInfo()[iI].m_iDefaultUnitIndex)
				{
					iCounter++;
					// Add Unit
					sprintf(szBuffer, "\n  %c%s - (%s)\n", FC_BULLETPOINT, 
						GC.getUnitInfo()[GC.getCivilizationInfo()[eCivilization].getCivilizationUnits(iI)].getDescription(),
						GC.getUnitInfo()[GC.getUnitClassInfo()[iI].m_iDefaultUnitIndex].getDescription());
					strcat(szInfoText, szBuffer);
				}
			}
			if (iCounter == 0)
			{
				strcat(szInfoText, "\n  No Free Techs");
			}
		}
		else
		{
			//	This is a random civ, let us know here...
			return CvString("The civilization chosen is random.  You will start the game with techs and units based on the civilization that is chosen for you.");
		}
	}
	return CvString(szInfoText);
}