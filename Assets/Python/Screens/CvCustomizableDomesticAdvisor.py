#
## Customizable Domestic Advisor Mod v 0.91
## for Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
#
#  Created by Lee Reeves, AKA Taelis on civfanatics.com

## REQUIRES Civilization 4 - Beyond the Sword - PATCH 3.02

## Ported to BtS and modified for BUG by EmperorFool
#
#    - Added BtS columns (e.g. corporations and espionage) and "Liberate Colony" button.
#    - Added other new columns (e.g. turns until culture growth and great person birth).
#    - Added a set of building class columns that show the building type for the civ you're playing.
#    - Added a second set of building type/class columns that show if you have the building or not
#      instead of the effects of the building. These columns are narrower than the originals.
#    - Changed most building columns to use the building's icon instead of its name.
#    - Resource columns now show their icon as the header and their effects as the value.
#    - Fixed crash caused when you have more than 20 or so cities.
#    - Added page switching buttons that wrap around.
#    - Added buttons to move pages while customizing.
#    - Added a button to toggle whether or not to display the controls for changing specialists.
#    - Added base experience for units in production and optional icons/coloring for the producing list.
#
## Credits
#
#    This advisor was inspired by the fantastic work of Homegrown and Requies of civfanatics.com, and all
#    those who contributed to their work. I'd like to thank:
#
#      Cammagno - for extensive help with beta testing, and for developing a complete, optimized configuration file
#
#      Homegrown - for the original domestic advisor mod with its many improvements
#
#      Requies - for the "Special" Domestic Advisor, the basis of this mod. Credits from his mod include:
#
#        terrasol - "for the changes to the color of the text to indicate problem values and for changes 
#                    which fix the non-English language problems and additional small changes"
#        Arkeide - "for the base code to jumping to a city on the list."
#        rendermad - "for the suggestion of making garrison colored when < 1"
#        =DOCTOR= - "for the suggestion of putting in Culture and GP Thresholds"
#        Tubby Rower - "for the unfortunately unimplementable mouseover idea"
#        eotinb - "for the suggestion of putting in the city automation information and for some general 
#                  comments and ideas"
#        sportybrian - "for the suggestion of highlighting with different colors for the 0, and very positive levels."
#
#     Fixaxis, of course, for making CivIV and stealing months of my life. ;)

## Legal Stuff
#
#  THIS MATERIAL IS NOT MADE, GUARANTEED OR SUPPORTED BY THE PUBLISHER OF THE SOFTWARE OR ITS AFFILIATES.
#  THIS MATERIAL IS RELEASED AS-IS. IN NO EVENT WILL THE AUTHOR BE LIABLE FOR SPECIAL, INCIDENTAL OR 
#  CONSEQUENTIAL DAMAGES RESULTING FROM POSSESSION, USE OR MALFUNCTION OF THE SOFTWARE, INCLUDING 
#  DAMAGES TO PROPERTY, LOSS OF GOODWILL, COMPUTER FAILURE OR MALFUNCTION AND, TO THE EXTENT PERMITTED 
#  BY LAW, DAMAGES FOR PERSONAL INJURIES, EVEN IF THE AUTHOR HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH 
#  DAMAGES. THE AUTHOR’S LIABILITY SHALL NOT EXCEED THE ACTUAL PRICE PAID FOR USE OF THE MATERIAL. SOME 
#  STATES/COUNTRIES DO NOT ALLOW LIMITATIONS ON HOW LONG AN IMPLIED WARRANTY LASTS AND/OR THE EXCLUSION 
#  OR LIMITATION OF INCIDENTAL OR CONSEQUENTIAL DAMAGES, SO THE ABOVE LIMITATIONS AND/OR EXCLUSION OR 
#  LIMITATION OF LIABILITY MAY NOT APPLY TO YOU. THIS WARRANTY GIVES YOU SPECIFIC LEGAL RIGHTS, AND 
#  YOU MAY HAVE OTHER RIGHTS THAT VARY FROM JURISDICTION TO JURISDICTION.

###############################################################################################################

from CvPythonExtensions import *

import PyHelpers
import CvUtil
import CvScreenEnums
import CvEventInterface
import Popup as PyPopup

import BugConfigTracker
import BugCore
import BugPath
import BugUtil
import FontUtil
import GameUtil

# BUG - Mac Support - start
BugUtil.fixSets(globals())
# BUG - Mac Support - end

import math

PyPlayer = PyHelpers.PyPlayer

CityScreenOpt = BugCore.game.CityScreen
AdvisorOpt = BugCore.game.CustDomAdv
MainOpt = BugCore.game.MainInterface

# Needed to save changes
import pickle

# Needed to check for non-numbers (specially search function)
import re

import time

gc = CyGlobalContext()

#	IMPORTANT INFORMATION
#	
#	All widget names MUST be unique when creating screens.  If you create
#	a widget named 'Hello', and then try to create another named 'Hello', it
#	will modify the first hello.
#
#	Also, when attaching widgets, 'Background' is a reserve word meant for
#	the background widget.  Do NOT use 'Background' to name any widget, but
#	when attaching to the background, please use the 'Background' keyword.

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

# Reposition if resolution (or language) changes
g_bMustCreatePositions = True
def forcePositionCalc (*args):
	global g_bMustCreatePositions
	g_bMustCreatePositions = True

# used to access the customizing flag
g_advisor = None
def isCustomizing():
	return g_advisor.customizing

# widget help text
def getEditHelpText(eWidgetType, iData1, iData2, bOption):
	if isCustomizing():
		return BugUtil.getPlainText("TXT_KEY_CDA_STOP_EDITING")
	else:
		return BugUtil.getPlainText("TXT_KEY_CDA_START_EDITING")


# Class CvDomesticAdvisor

class CvCustomizableDomesticAdvisor:
	"""Special Domestic Advisor Screen"""

	def __init__(self):
		"""
		Basic init function.
		Called when cIV is first booted up and everytime you switch into cIV
		"""

		self.isFlavorful = True

		self.PICKLED_VERSION = 1

		self.NO_CITY = -1

		self.runtimeInitDone = False

		self.listSelectedCities = []

		# An event context for renaming pages
		self.renameEventContext = None

		# All size information moved to self.createPositions because they are now
		# all based on the screen resolution and the screen isn't available yet.

		# Names of Widgets
		self.SCREEN_NAME = "DomesticAdvisor"
		self.EXIT_NAME = "DomesticExit"
		self.BACKGROUND_ID = "DomesticAdvisorBG"
		self.PAGES_DD_NAME = "DomPagesDD"

		self.CULTURE_TEXT_NAME = "DomCultureText"
		self.GP_TEXT_NAME = "DomGPText"
		self.NUMBER_TEXT = "NUM"

		self.SPECIALIST_IMAGE_NAME = "DomCitizenImage"
		self.SPECIALIST_PLUS_NAME = "DomIncreaseSpecialist"
		self.SPECIALIST_MINUS_NAME = "DomDecreaseSpecialist"
		self.SPECIALIST_TEXT_NAME = "DomSpecialistText"

		self.CUSTOMIZE_PAGE = "DomCustomize"
		self.COLUMNS_LIST_PAGE = "DomColumnsList"
		
		self.PREV_PAGE_NAME = "DomPagePrevButton"
		self.NEXT_PAGE_NAME = "DomPageNextButton"
		self.START_CUSTOMIZING_NAME = "DomStartCustomizing"
		self.RENAME_PAGE_NAME = "DomRenamePage"
		self.ADD_PAGE_NAME = "DomAddPageButton"
		self.DEL_PAGE_NAME = "DomDelPageButton"
		self.PAGE_UP_NAME = "DomPageUpButton"
		self.PAGE_DOWN_NAME = "DomPageDownButton"
		self.SAVE_NAME = "DomSaveButton"
		self.RELOAD_PAGES_NAME = "DomReloadPages"

		self.COLUMN_SHRINK_NAME = "DomColShrink"
		self.COLUMN_WIDEN_NAME = "DomColWiden"
		self.ADDCOLUMN_NAME = "DomAddCol"
		self.DELCOLUMN_NAME = "DomDelCol"
		self.COLUMNUP_NAME = "DomColUp"
		self.COLUMNDN_NAME = "DomColDn"
		
		self.TOGGLE_SPECS_NAME = "ToggleSpecsCB"

		self.customizing = False
		self.currentPageNum = 0
		
		global g_advisor
		g_advisor = self

		# Special Class variables

		# The currently active page
		self.currentPage = None
		self.visiblePage = None

		self.COLUMNS_LIST = [
				# Name                      Width    Type   CyCityFunction0			CyCityFunction1			Arg									selfFunction							Arg							Title

				("NAME",					95,		"text",	CyCity.getName,			None,					0,									None,									None,						"localText.getText(\"TXT_KEY_DOMESTIC_ADVISOR_NAME\", ()).upper()"),
				("ADVISE_CULTURE",			150,	"text",	None,					None,					0,									self.advise,							"Culture",					"localText.getText(\"TXT_KEY_CONCEPT_CULTURE\", ()).upper()"),
				("ADVISE_MILITARY",			150,	"text",	None,					None,					0,									self.advise,							"Military",					"localText.getText(\"TXT_KEY_ADVISOR_MILITARY\", ()).upper()"),
				("ADVISE_NUTTY",			150,	"text",	None,					None,					0,									self.advise,							"Nutty",					"u\"NUTTY\""),
				("ADVISE_RELIGION",			150,	"text",	None,					None,					0,									self.advise,							"Religion",					"localText.getText(\"TXT_KEY_CONCEPT_RELIGION\", ()).upper()"),
				("ADVISE_RESEARCH",			150,	"text",	None,					None,					0,									self.advise,							"Research",					"localText.getText(\"TXT_KEY_COMMERCE_RESEARCH\", ()).upper()"),
				("ADVISE_SPACESHIP",		150,	"text",	None,					None,					0,									self.advise,							"Spaceship",				"localText.getText(\"TXT_KEY_CONCEPT_SPACESHIP\", ()).upper()"),
				("AUTOMATION",				80,		"text",	None,					None,					0,									self.calculateAutomation,				None,						"u\"AUTO\""),
				("BASE_COMMERCE",			38,		"int",	None,					CyCity.getBaseYieldRate, YieldTypes.YIELD_COMMERCE,			None,									None,						"u\"B\" + self.commerceIcon"),
				("BASE_FOOD",				38,		"int",	None,					CyCity.getBaseYieldRate, YieldTypes.YIELD_FOOD,				None,									None,						"u\"B\" + self.foodIcon"),
				("BASE_PRODUCTION",			38,		"int",	None,					CyCity.getBaseYieldRate, YieldTypes.YIELD_PRODUCTION,		None,									None,						"u\"B\" + self.hammerIcon"),
				("CONSCRIPT_ANGER",			38,		"int",	None,					None,					0,									self.calculateConscriptAnger,			None,						"u\"D\" + self.unhappyIcon"),
				("CONSCRIPT_UNIT",			90,		"text",	None,					None,					0,									self.calculateConscriptUnit,			None,						"localText.getText(\"TXT_KEY_CONCEPT_DRAFT\", ()).upper()"),
				("COULD_CONSCRIPT_UNIT",	90,		"text",	None,					None,					0,									self.calculatePotentialConscriptUnit,	None,						"localText.getText(\"TXT_KEY_CONCEPT_DRAFT\", ()).upper() + u\"#\""),
				("CORPORATIONS",			90,		"text",	None,					None,					0,									self.calculateCorporations,				None,						"localText.getText(\"TXT_KEY_CONCEPT_CORPORATIONS\", ()).upper()"),
				("CULTURE",					53,		"int",	None,					None,					0,									self.calculateTotalCulture,				None,						"self.cultureIcon"),
				("CULTURE_RATE",			38,		"int",	None,					CyCity.getCommerceRate, CommerceTypes.COMMERCE_CULTURE,		None,									None,						"self.cultureIcon + u\"R\""),
				("CULTURE_TURNS",			38,		"int",	None,					None,					None,								self.calculateCultureTurns,				None,						"self.cultureIcon + u\"T\""),
				("DEFENSE",					60,		"int",	None,					None,					0,									self.calculateDefense,					None,						"self.defenseIcon"),
				("ESPIONAGE",			    38,		"int",	None,					CyCity.getCommerceRate, CommerceTypes.COMMERCE_ESPIONAGE,	None,									None,						"self.espionageIcon"),
				("ESPIONAGE_DEF",			60,		"int",	CyCity.getEspionageDefenseModifier,	None,		0,									self.calculateEspionageDefense,			None,						"self.espionageIcon + u\"%\""),
				("FEATURES",				106,	"text",	None,					None,					0,									self.calculateFeatures,					None,						"localText.getText(\"TXT_KEY_MISC_FEATURES\", ())"),
				("FOOD",					35,		"int",	None,					None,					0,									self.calculateFood,						None,						"self.foodIcon"),
				("FOUNDED",					80,		"date",	None,					None,					0,									self.calculateFounded,					None,						"localText.getText(\"TXT_KEY_DOMESTIC_ADVISOR_FOUNDED\", ()).upper()"),
				("FREE_EXPERIENCE_LAND",	30,		"int",	None,					None,					0,									self.calculateFreeExperience,			"L",						"self.landIcon"),
				("FREE_EXPERIENCE_SEA",		30,		"int",	None,					None,					0,									self.calculateFreeExperience,			"S",						"self.seaIcon"),
				("FREE_EXPERIENCE_AIR",		30,		"int",	None,					None,					0,									self.calculateFreeExperience,			"A",						"self.airIcon"),
				("GARRISON",				30,		"int",	CyCity.getMilitaryHappinessUnits,	None,		0,									None,									None,						"self.militaryIcon"),
				("GOLD",					38,		"int",	None,					CyCity.getCommerceRate, CommerceTypes.COMMERCE_GOLD,		None,									None,						"self.goldIcon"),
				("GRANK_BASE_COMMERCE",		42,		"int",	None,					None,					0,									self.findGlobalBaseYieldRateRank, YieldTypes.YIELD_COMMERCE,		"u\"B\" + self.commerceIcon + u\"g\""),
				("GRANK_BASE_FOOD",			42,		"int",	None,					None,					0,									self.findGlobalBaseYieldRateRank, YieldTypes.YIELD_FOOD,			"u\"B\" + self.foodIcon + u\"g\""),
				("GRANK_BASE_PRODUCTION",	42,		"int",	None,					None,					0,									self.findGlobalBaseYieldRateRank, YieldTypes.YIELD_PRODUCTION,		"u\"B\" + self.hammerIcon + u\"g\""),
				("GRANK_COMMERCE",			38,		"int",	None,					None,					0,									self.findGlobalYieldRateRank, YieldTypes.YIELD_COMMERCE,			"self.commerceIcon + u\"g\""),
				("GRANK_FOOD",				38,		"int",	None,					None,					0,									self.findGlobalYieldRateRank, YieldTypes.YIELD_FOOD,				"self.foodIcon + u\"g\""),
				("GRANK_PRODUCTION",		38,		"int",	None,					None,					0,									self.findGlobalYieldRateRank, YieldTypes.YIELD_PRODUCTION,			"self.hammerIcon + u\"g\""),
				("GRANK_CULTURE",			38,		"int",	None,					None,					0,									self.findGlobalCommerceRateRank, CommerceTypes.COMMERCE_CULTURE,	"self.cultureIcon + u\"g\""),
				("GRANK_GOLD",				38,		"int",	None,					None,					0,									self.findGlobalCommerceRateRank, CommerceTypes.COMMERCE_GOLD,		"self.goldIcon + u\"g\""),
				("GRANK_RESEARCH",			38,		"int",	None,					None,					0,									self.findGlobalCommerceRateRank, CommerceTypes.COMMERCE_RESEARCH,	"self.researchIcon + u\"g\""),
				("GREATPEOPLE",				45,		"int",	CyCity.getGreatPeopleProgress,	None,			0,									None,									None,						"self.figureheadIcon"),
				("GREATPEOPLE_RATE",		38,		"int",	CyCity.getGreatPeopleRate,		None,			0,									None,									None,						"self.figureheadIcon + u\"R\""),
				("GREATPEOPLE_TURNS",		38,		"int",	None,					None,					None,								self.calculateGreatPeopleTurns,			None,						"self.figureheadIcon + u\"T\""),
				("GROWTH",					35,		"int",	None,					None,					0,									self.calculateGrowth,					None,						"self.redfoodIcon"),
				("HAPPY",					30,		"int",	None,					None,					0,									self.calculateNetHappiness,				None,						"self.happyIcon"),
				("HEALTH",					30,		"int",	None,					None,					0,									self.calculateNetHealth,				None,						"self.healthIcon"),
				("HURRY_GOLD",				38,		"int",	None,					None,					0,									self.calculateHurryGoldCost,			None,						"u\"H\" + self.goldIcon"),
				("HURRY_POP",				38,		"int",	None,					None,					0,									self.calculateWhipPopulation,			None,						"u\"H\" + self.angryIcon"),
				("HURRY_POP_EXTRA",			38,		"int",	None,					None,					0,									self.calculateWhipOverflowProduction,	None,						"u\"H\" + self.hammerIcon"),
				("HURRY_POP_GOLD",			38,		"int",	None,					None,					0,									self.calculateWhipOverflowGold,			None,						"u\"H\" + self.goldIcon"),
				("HURRY_POP_ANGER",			38,		"int",	None,					None,					0,									self.calculateWhipAnger,				None,						"u\"H\" + self.unhappyIcon"),
				("LIBERATE",				35,		"int",	None,					None,					0,									self.canLiberate,						None,						"self.fistIcon"),
				("LOCATION_X",				50,		"int",	CyCity.getX,			None,					0,									None,									None,						"u\"X\""),
				("LOCATION_Y",				50,		"int",	CyCity.getY,			None,					0,									None,									None,						"u\"Y\""),
				("MAINTENANCE",				30,		"int",	CyCity.getMaintenance,	None,					0,									None,									None,						"self.redGoldIcon"),
				("NRANK_BASE_COMMERCE",		42,		"int",	None,					CyCity.findBaseYieldRateRank, YieldTypes.YIELD_COMMERCE,	None,									None,						"u\"B\" + self.commerceIcon + u\"n\""),
				("NRANK_BASE_FOOD",			42,		"int",	None,					CyCity.findBaseYieldRateRank, YieldTypes.YIELD_FOOD,		None,									None,						"u\"B\" + self.foodIcon + u\"n\""),
				("NRANK_BASE_PRODUCTION",	42,		"int",	None,					CyCity.findBaseYieldRateRank, YieldTypes.YIELD_PRODUCTION,	None,									None,						"u\"B\" + self.hammerIcon + u\"n\""),
				("NRANK_COMMERCE",			38,		"int",	None,					CyCity.findYieldRateRank, YieldTypes.YIELD_COMMERCE,		None,									None,						"self.commerceIcon + u\"n\""),
				("NRANK_FOOD",				38,		"int",	None,					CyCity.findYieldRateRank, YieldTypes.YIELD_FOOD,			None,									None,						"self.foodIcon + u\"n\""),
				("NRANK_PRODUCTION",		38,		"int",	None,					CyCity.findYieldRateRank, YieldTypes.YIELD_PRODUCTION,		None,									None,						"self.hammerIcon + u\"n\""),
				("NRANK_CULTURE",			38,		"int",	None,					CyCity.findCommerceRateRank, CommerceTypes.COMMERCE_CULTURE,	None,								None,						"self.cultureIcon + u\"n\""),
				("NRANK_GOLD",				38,		"int",	None,					CyCity.findCommerceRateRank, CommerceTypes.COMMERCE_GOLD,	None,									None,						"self.goldIcon + u\"n\""),
				("NRANK_RESEARCH",			38,		"int",	None,					CyCity.findCommerceRateRank, CommerceTypes.COMMERCE_RESEARCH,	None,								None,						"self.researchIcon + u\"n\""),
				("NUM_SPECIALIST_GG",		30,		"int",	None,					None,					0,									self.countFreeSpecialists,				"GREAT_GENERAL",			"self.milInstructorIcon"),
				("POPULATION",				35,		"int",	CyCity.getPopulation,	None,					0,									None,									None,						"localText.getText(\"TXT_KEY_POPULATION\", ()).upper()"),
				("POPULATION_REAL",			65,		"int",	CyCity.getRealPopulation,	None,				0,									None,									None,						"localText.getText(\"TXT_KEY_POPULATION\", ()).upper() + u\"#\""),
				("POWER",					50,		"text",	None,					None,					0,									self.calculatePower,					None,						"self.powerIcon"),
				("PRODUCING",				90,		"text",	None,					None,					0,									self.calculateProducing,				None,						"localText.getText(\"TXT_KEY_DOMESTIC_ADVISOR_PRODUCING\", ())"),
				("PRODUCING_TURNS",			33,		"int",	None,					None,					0,									self.calculateProducingTurns,			None,						"self.hammerIcon + u\"T\""),
				("PRODUCTION",				38,		"int",	None,					None,					0,									self.calculateProduction,				None,						"self.hammerIcon"),
				("RELIGIONS",				90,		"text",	None,					None,					0,									self.calculateReligions,				None,						"localText.getText(\"TXT_KEY_ADVISOR_RELIGION\", ()).upper()"),
				("RESEARCH",				38,		"int",	None,					CyCity.getCommerceRate, CommerceTypes.COMMERCE_RESEARCH,	None,									None,						"self.researchIcon"),
				("SPECIALISTS",				209,	"text",	None,					None,					0,									self.calculateSpecialists,				None,						"localText.getText(\"TXT_KEY_CONCEPT_SPECIALISTS\", ()).upper()"),
				("THREATS",					60,		"text",	None,					None,					0,									self.calculateThreats,					None,						"u\"Threats\""),
				("TRADE",					30,		"int",	None,					None,					0,									self.calculateTrade,					None,						"self.tradeIcon"),
				("TRADE_DOMESTIC",			30,		"int",	None,					None,					0,									self.calculateTrade,					"D",						"u\"D\" + self.tradeIcon"),
				("TRADE_FOREIGN",			30,		"int",	None,					None,					0,									self.calculateTrade,					"F",						"u\"F\" + self.tradeIcon"),
				("TRADE_ROUTES",			30,		"int",	None,					None,					0,									self.countTradeRoutes,					None,						"u\"#\" + self.tradeIcon"),
				("TRADE_ROUTES_DOMESTIC",	30,		"int",	None,					None,					0,									self.countTradeRoutes,					"D",						"u\"D#\" + self.tradeIcon"),
				("TRADE_ROUTES_FOREIGN",	30,		"int",	None,					None,					0,									self.countTradeRoutes,					"F",						"u\"F#\" + self.tradeIcon"),
			]

		# Values to check to see if we need to color the number as a problem
		self.PROBLEM_VALUES_DICT = {
			"GARRISON" : 0,
			"HAPPY" : -1,
			"HEALTH" : -1,
			"GROWTH" : -1,
			"FOOD" : -1,
			"HURRY_POP_ANGER" : 1,
			}

		# Values to check to see if we need to color the number as neutral
		self.NEUTRAL_VALUES_DICT = {
			"HAPPY" : 0,
			"HEALTH" : 0,
			"GROWTH" : 0,
			"FOOD" : 0,
			}

		# Values to check to see if we need to color the number as great
		self.GREAT_VALUES_DICT = {
			"HAPPY" : 6,
			"HEALTH" : 6,
			"FOOD" : 8,
			}

		# Values for whom coloring comparison is reversed; i.e. higher numbers are worse
		self.COMPARISON_REVERSED = [
			"HURRY_POP_ANGER",
			]

		# Dictionary of the coloring dictionaries!
		self.COLOR_DICT_DICT = {
			"PROBLEM": self.PROBLEM_VALUES_DICT,
			"NEUTRAL": self.NEUTRAL_VALUES_DICT,
			"GREAT": self.GREAT_VALUES_DICT,			
			}


		# This creates the set of ALL coloring keys.
		# Do NOT touch.
		self.COLOR_SET = set()
		for clDict in self.COLOR_DICT_DICT.values():
			self.COLOR_SET.update (clDict.keys())

		# Values to change on an update
		# (True indicates update when we DON'T switch to/from food production)
		# Most of this MIGHT change because the computer might be switching
		# plots it's working or creating/removing specialists.

		self.UPDATE_DICT = {
			"HAPPY": False,
			"GROWTH" : False,
			"FOOD": False,
			"PRODUCTION": True,
			"BASE_COMMERCE": False,
			"GOLD": False,
			"RESEARCH": False,
			"CULTURE_RATE": False,
			"CULTURE_TURNS": False,
			"ESPIONAGE": False,
			"GREATPEOPLE_RATE": False,
			"GREATPEOPLE_TURNS": False,
			"PRODUCING": True,
			"PRODUCING_TURNS": True,
			"SPECIALISTS": False,
			"AUTOMATION": True
			}

		self.HEADER_DICT = None
		self.SPECIALIST_ICON_DICT = None
		self.AUTOMATION_ICON_DICT = None
		self.COLOR_DICT = None
# BUG - Production Grouping - start
		self.PROD_COLOR_DICT = None
# BUG - Production Grouping - end

		# Input handling functions
		self.DomesticScreenInputMap = {
			self.SPECIALIST_PLUS_NAME	: self.HandleSpecialistPlus,
			self.SPECIALIST_MINUS_NAME	: self.HandleSpecialistMinus,
			self.EXIT_NAME				: self.DomesticExit,
			
			self.ADDCOLUMN_NAME			: self.AddCol,
			self.DELCOLUMN_NAME			: self.DelCol,
			self.COLUMNUP_NAME			: self.MoveColUp,
			self.COLUMNDN_NAME			: self.MoveColDn,
			self.COLUMN_SHRINK_NAME		: self.shrinkCol,
			self.COLUMN_WIDEN_NAME		: self.widenCol,
			
			self.START_CUSTOMIZING_NAME	: self.ModifyPage,
			self.SAVE_NAME				: self.save,
			self.ADD_PAGE_NAME			: self.addPage,
			self.DEL_PAGE_NAME			: self.delPage,
			self.PREV_PAGE_NAME			: self.previousPage,
			self.NEXT_PAGE_NAME			: self.nextPage,
			self.PAGE_UP_NAME			: self.upPage,
			self.PAGE_DOWN_NAME			: self.downPage,
			
			self.TOGGLE_SPECS_NAME		: self.toggleShowSpecialistControls,

			self.RELOAD_PAGES_NAME		: self.reloadPages,
			self.RENAME_PAGE_NAME		: self.renamePage,

			}

	def createDictionaries(self):
		"""
		Creates Dictionaries we couldn't on init.
		"""

		if(self.runtimeInitDone):
			return
		
		self.HURRY_TYPE_POP = gc.getInfoTypeForString("HURRY_POPULATION")
		self.HURRY_TYPE_GOLD = gc.getInfoTypeForString("HURRY_GOLD")
		
		self.angryIcon = u"%c" % CyGame().getSymbolID(FontSymbols.ANGRY_POP_CHAR)
		self.commerceIcon = u"%c" %(gc.getYieldInfo(YieldTypes.YIELD_COMMERCE).getChar())
		self.cultureIcon = u"%c" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar())
		self.defenseIcon = u"%c" % CyGame().getSymbolID(FontSymbols.DEFENSE_CHAR)
		self.espionageIcon = u"%c" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_ESPIONAGE).getChar())
		self.fistIcon = u"%c" % CyGame().getSymbolID(FontSymbols.OCCUPATION_CHAR)
		self.foodIcon = u"%c" %(gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar())
		self.footIcon = u"%c" % CyGame().getSymbolID(FontSymbols.MOVES_CHAR)
		self.goldIcon = u"%c" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())
		self.redGoldIcon = u"%c" % CyGame().getSymbolID(FontSymbols.BAD_GOLD_CHAR)
		self.figureheadIcon = u"%c" % CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR)
		self.hammerIcon = u"%c" %(gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar())
		self.happyIcon = u"%c" % CyGame().getSymbolID(FontSymbols.HAPPY_CHAR)
		self.healthIcon = u"%c" % CyGame().getSymbolID(FontSymbols.HEALTHY_CHAR)
		self.lawIcon = u"%c" % CyGame().getSymbolID(FontSymbols.DEFENSIVE_PACT_CHAR)
		self.militaryIcon = u"%c" % CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR)
		self.powerIcon = u"%c" % CyGame().getSymbolID(FontSymbols.POWER_CHAR)
		self.redfoodIcon = u"%c" % CyGame().getSymbolID(FontSymbols.BAD_FOOD_CHAR)
		self.religionIcon = u"%c" % CyGame().getSymbolID(FontSymbols.RELIGION_CHAR)
		self.researchIcon = u"%c" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_RESEARCH).getChar())
		self.sickIcon = u"%c" % CyGame().getSymbolID(FontSymbols.UNHEALTHY_CHAR)
		self.tradeIcon = u"%c" % CyGame().getSymbolID(FontSymbols.TRADE_CHAR)
		self.unhappyIcon = u"%c" % CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR)
		
		self.yieldIcons = {}
		for eYieldType in range(YieldTypes.NUM_YIELD_TYPES):
			info = gc.getYieldInfo(eYieldType)
			self.yieldIcons[eYieldType] = u"%c" % info.getChar()
		
		self.commerceIcons = {}
		for eCommerceType in range(CommerceTypes.NUM_COMMERCE_TYPES):
			info = gc.getCommerceInfo(eCommerceType)
			self.commerceIcons[eCommerceType] = u"%c" % info.getChar()

		self.starIcon = u"%c" % CyGame().getSymbolID(FontSymbols.STAR_CHAR)
		self.silverStarIcon = u"%c" % CyGame().getSymbolID(FontSymbols.SILVER_STAR_CHAR)
		self.bulletIcon = u"%c" % CyGame().getSymbolID(FontSymbols.BULLET_CHAR)

		self.milInstructorIcon = FontUtil.getChar(FontSymbols.MILITARY_INSTRUCTOR_CHAR)
		self.landIcon = FontUtil.getChar(FontSymbols.DOMAIN_LAND_CHAR)
		self.seaIcon = FontUtil.getChar(FontSymbols.DOMAIN_SEA_CHAR)
		self.airIcon = FontUtil.getChar(FontSymbols.DOMAIN_AIR_CHAR)
		self.cancelIcon = FontUtil.getChar(FontSymbols.CANCEL_CHAR)

		# Special symbols for building, wonder and project views
		self.objectIsPresent = "x"
		self.objectIsNotPresent = "-"
		self.objectCanBeBuild = "o"
		self.objectUnderConstruction = self.hammerIcon
		
		# add the colors dependant on the statuses
		self.objectHave = localText.changeTextColor (self.objectIsPresent, gc.getInfoTypeForString("COLOR_GREEN")) #"x"
		self.objectNotPossible = localText.changeTextColor (self.objectIsNotPresent, gc.getInfoTypeForString("COLOR_RED")) #"-"
		self.objectPossible = localText.changeTextColor (self.objectCanBeBuild, gc.getInfoTypeForString("COLOR_BLUE")) #"o"
		self.objectHaveObsolete = localText.changeTextColor (self.objectIsPresent, gc.getInfoTypeForString("COLOR_WHITE")) #"x"
		self.objectNotPossibleConcurrent = localText.changeTextColor (self.objectIsNotPresent, gc.getInfoTypeForString("COLOR_YELLOW")) #"-"
		self.objectPossibleConcurrent = localText.changeTextColor (self.objectCanBeBuild, gc.getInfoTypeForString("COLOR_YELLOW")) #"o"		
		
		# Corporation Yield and Commerce values by Bonus
		# Maps are { bonus -> { yield/commerce -> { corporation -> value } } }
		self.corpMaintPercent = gc.getWorldInfo(gc.getMap().getWorldSize()).getCorporationMaintenancePercent()
		self.bonusCorpYields = {}
		self.bonusCorpCommerces = {}
		for eCorp in range(gc.getNumCorporationInfos()):
			info = gc.getCorporationInfo(eCorp)
			for i in range(gc.getNUM_CORPORATION_PREREQ_BONUSES()):
				eBonus = info.getPrereqBonus(i)
				if (eBonus >= 0):
					for eYield in range(YieldTypes.NUM_YIELD_TYPES):
						iYieldValue = info.getYieldProduced(eYield)
						if (iYieldValue != 0):
							if (not self.bonusCorpYields.has_key(eBonus)):
								self.bonusCorpYields[eBonus] = {}
							if (not self.bonusCorpYields[eBonus].has_key(eYield)):
								self.bonusCorpYields[eBonus][eYield] = {}
							if (not self.bonusCorpYields[eBonus][eYield].has_key(eCorp)):
								self.bonusCorpYields[eBonus][eYield][eCorp] = iYieldValue
						
					for eCommerce in range(CommerceTypes.NUM_COMMERCE_TYPES):
						iCommerceValue = info.getCommerceProduced(eCommerce)
						if (iCommerceValue != 0):
							if (not self.bonusCorpCommerces.has_key(eBonus)):
								self.bonusCorpCommerces[eBonus] = {}
							if (not self.bonusCorpCommerces[eBonus].has_key(eCommerce)):
								self.bonusCorpCommerces[eBonus][eCommerce] = {}
							if (not self.bonusCorpCommerces[eBonus][eCommerce].has_key(eCorp)):
								self.bonusCorpCommerces[eBonus][eCommerce][eCorp] = iCommerceValue

		self.loadPages()

		self.BUILDING_ICONS_DICT = { }
		self.BUILDING_DICT = { }
		self.BUILDING_INFO_LIST = []

#		extraBldgColumns = []
		for i in range(gc.getNumBuildingInfos()):
			info = gc.getBuildingInfo(i)
			desc = info.getDescription()
			key = self.getBuildingKey(i)

			self.BUILDING_DICT[key] = i
			self.BUILDING_INFO_LIST.append(info)

			icon = u""

			if info.isCapital() > 0:
				icon += self.starIcon
			elif info.isGovernmentCenter() > 0:
				icon += self.silverStarIcon

			if info.getReligionType() != -1:
				if info.getHolyCity() != -1:
					icon += u"%c" %(gc.getReligionInfo(info.getReligionType()).getHolyCityChar())
				else:
					icon += u"%c" %(gc.getReligionInfo(info.getReligionType()).getChar())
			
			if info.getFoodKept() > 0 or info.getSeaPlotYieldChange(YieldTypes.YIELD_FOOD) > 0:
				icon += self.foodIcon

			if info.getFreeExperience() > 0 or \
				info.getFreePromotion() != -1 or \
				info.getGlobalFreeExperience() > 0 or \
				info.getDomainFreeExperience(DomainTypes.DOMAIN_LAND) > 0 or \
				info.getDomainFreeExperience(DomainTypes.DOMAIN_SEA) > 0 or \
				info.getDomainFreeExperience(DomainTypes.DOMAIN_AIR) > 0:
				icon += self.militaryIcon

			if info.getDefenseModifier() > 0 or \
				info.getAllCityDefenseModifier() > 0 or \
				info.getNukeModifier() < 0 or \
				info.getAirModifier() < 0:
				icon += self.defenseIcon

			if info.isPower() or info.isDirtyPower() or info.isAreaCleanPower():
				icon += self.powerIcon

			if info.getWarWearinessModifier() < 0 or info.getAnarchyModifier() > 0 or info.getGlobalWarWearinessModifier() < 0:
				icon += "[" + self.angryIcon + "]"

			if info.getCommerceModifier(CommerceTypes.COMMERCE_CULTURE) > 0:
				icon += self.cultureIcon

			if info.getCommerceModifier(CommerceTypes.COMMERCE_GOLD) > 0:
				icon += self.goldIcon

			if info.getCommerceModifier(CommerceTypes.COMMERCE_RESEARCH) > 0:
				icon += self.researchIcon

			if info.getCommerceModifier(CommerceTypes.COMMERCE_ESPIONAGE) > 0:
				icon += self.espionageIcon

			if info.getSpaceProductionModifier() > 0 \
				or info.getDomainProductionModifier(DomainTypes.DOMAIN_LAND) > 0 \
				or info.getDomainProductionModifier(DomainTypes.DOMAIN_SEA) > 0 \
				or info.getDomainProductionModifier(DomainTypes.DOMAIN_AIR) > 0 \
				or info.getYieldChange(YieldTypes.YIELD_PRODUCTION) > 0:
				icon += self.hammerIcon

			if info.getTradeRouteModifier() > 0 or info.getTradeRoutes() > 0 or info.getCoastalTradeRoutes() > 0 \
			or info.getGlobalTradeRoutes() > 0 or info.getForeignTradeRouteModifier() > 0:
				icon += self.tradeIcon

			if info.getMaintenanceModifier() < 0:
				icon += self.commerceIcon

			if info.isNoUnhappiness():
				icon += self.happyIcon

			if info.isBuildingOnlyHealthy():
				icon += self.healthIcon

			if info.getHealth() < 0 or info.getGlobalHealth() < 0:
				icon += self.sickIcon

			if info.getGreatPeopleRateChange() > 0 or info.getGreatPeopleRateModifier() > 0:
				icon += self.figureheadIcon
			
			if info.getMovie():
				icon += self.starIcon

			self.COLUMNS_LIST.append((key, 50 + 15 * len(icon), "text", None, None, 0, self.calculateValue, None, u"u\"" + desc + u"\""))
			self.BUILDING_ICONS_DICT[key] = icon
#			extraBldgColumns.append(("BLDG_" + key, 22, "bldg", None, None, 0, self.calculateBuilding, i, "u\"%s\"" % desc))
		
		# Duplicate building columns
#		self.COLUMNS_LIST += extraBldgColumns

		# Building classes
		for i in range(gc.getNumBuildingClassInfos()):
			info = gc.getBuildingClassInfo(i)
			key = "BLDGCLASS_" + info.getType()
			desc = info.getDescription()
			self.COLUMNS_LIST.append((key, 22, "bldgclass", None, None, 0, self.calculateBuildingClass, i, "u\"%s\"" % desc))

		# Civ-Specific Buildings
		for i in range(gc.getNumBuildingInfos()):
			info = gc.getBuildingInfo(i)
			classInfo = gc.getBuildingClassInfo(info.getBuildingClassType())
			if (classInfo.getDefaultBuildingIndex() != i):
				# Assume civ-specific if it isn't default building for its class
				key = "BLDGCIV_" + info.getType()
				desc = info.getDescription()
				self.COLUMNS_LIST.append((key, 22, "bldg", None, None, 0, self.calculateBuilding, i, "u\"%s\"" % desc))

		# Hurry types
		for i in range(gc.getNumHurryInfos()):
			header = "self.hammerIcon"
			name = "CAN_HURRY_"
			info = gc.getHurryInfo(i)
			if info.getGoldPerProduction() > 0:
				header += " + self.goldIcon"
				name += "GOLD"
			if info.getProductionPerPopulation() > 0 and info.isAnger():
				header += " + self.angryIcon"
				name += "WHIP"
			elif info.getProductionPerPopulation() > 0:
				header += " + self.happyIcon"
				name += "VOLUNTEERS"

			self.COLUMNS_LIST.append((name, 50, "text", None, None, 0, self.canHurry, i, header))

		# Resources ("bonuses") -- presence
		for i in range(gc.getNumBonusInfos()):
			info = gc.getBonusInfo(i)
			desc = u"%c" % info.getChar()
			key = "HAS_" + self.getBonusKey(i)

			self.COLUMNS_LIST.append((key, 24, "bonus", None, None, 0, self.calculateHasBonus, i, "u\"" + desc + "\""))

		# Resources ("bonuses") -- effects
		for i in range(gc.getNumBonusInfos()):
			info = gc.getBonusInfo(i)
			desc = u"%c" % info.getChar()
			key = self.getBonusKey(i)

			self.COLUMNS_LIST.append((key, 50, "text", None, None, 0, self.calculateBonus, i, "u\"" + desc + "\""))

		self.COLUMNS_INDEX = { }
		self.HEADER_DICT = { }

		for i, column in enumerate(self.COLUMNS_LIST):
			self.COLUMNS_INDEX[column[0]] = i
			self.HEADER_DICT[column[0]] = eval(column[8], globals(), locals())
					
		if self.SPECIALIST_ICON_DICT == None:
			# Specialist Icon Information (Must be here, because C++ functions aren't
			# available upon startup of CIV)
			self.SPECIALIST_ICON_DICT = {
				0 : self.bulletIcon, # Citizen
				1 : self.happyIcon, # Priest
				2 : self.cultureIcon, # Artist
				3 : self.researchIcon, # Scientist
				4 : self.goldIcon, # Merchant
				5 : self.hammerIcon, # Engineer
				6 : self.espionageIcon, # Engineer
				}

		if self.AUTOMATION_ICON_DICT == None:
			# Automation Information (Must be here, because C++ functions aren't
			# available upon startup of CIV)
			self.AUTOMATION_ICON_DICT = {
				0 : self.foodIcon, # Emphasize Food
				1 : self.hammerIcon, # Emphasize Production
				2 : self.goldIcon, # Emphasize Gold?
				3 : self.researchIcon, # Emphasize Research
				4 : self.figureheadIcon, # Emphasize GP
				5 : self.redfoodIcon, # Emphasize Avoid Growth
				}

		if self.COLOR_DICT == None:
			# Colors to highlight with for each type of number (Must be here,
			#  because C++ functions aren't available upon startup of CIV)
			self.COLOR_DICT = {
				"PROBLEM": gc.getInfoTypeForString("COLOR_RED"),
				"NEUTRAL": gc.getInfoTypeForString("COLOR_YELLOW"),
				"GREAT": gc.getInfoTypeForString("COLOR_GREEN"),
				}

# BUG - Production Grouping - start
		if self.PROD_COLOR_DICT == None:
			# Colors to use for color-coding of production items.
			# ["DEFAULT"] is used if color-coding is off.
			self.PROD_COLOR_DICT = {
				"DEFAULT": gc.getInfoTypeForString("COLOR_WHITE"),
				"NOTHING": gc.getInfoTypeForString("COLOR_RED"),
				"BUILDING": gc.getInfoTypeForString("COLOR_WHITE"),
				"WONDER": gc.getInfoTypeForString("COLOR_CYAN"), 
				"WEALTH": gc.getInfoTypeForString("COLOR_YELLOW"),
				"RESEARCH": gc.getInfoTypeForString("COLOR_GREEN"),
				"CULTURE": gc.getInfoTypeForString("COLOR_MAGENTA"), 
				"PROJECT": gc.getInfoTypeForString("COLOR_CYAN"),
				"UNIT": gc.getInfoTypeForString("COLOR_YIELD_FOOD"),
				}
# BUG - Production Grouping - end

		self.switchPage(self.PAGES[0]["name"])

		self.runtimeInitDone = True

	def createPositions (self, screen):
		""" Calculates the basic positions to draw on. """

		# Borders from BUG Options
		nBorderTop = [0, 23, 52, 105][AdvisorOpt.getSpaceTop()]
		nBorderBottom = 177
		# If the min/max commerce buttons are shown, we need more space on the left
		nBorderLeft = 110
		if (MainOpt.isShowMinMaxCommerceButtons()):
			nBorderLeft = 150
		nBorderLeft = [0, 20, 40, nBorderLeft, nBorderLeft][AdvisorOpt.getSpaceSides()]
		nBorderRight = [0, 20, 40, nBorderLeft, 20][AdvisorOpt.getSpaceSides()]

		# Location/Size of the Overall Screen
		self.nScreenX = nBorderLeft
		self.nScreenWidth = screen.getXResolution() - nBorderLeft - nBorderRight
		self.nScreenY = nBorderTop
		self.nScreenLength = screen.getYResolution() - nBorderTop - nBorderBottom

		# Location/Size of the Panel
		# Panel no longer needs to be offset from screen since borders taken care of already.
		self.nPanelX = 0
		self.nPanelY = 0
		self.nPanelWidth = self.nScreenWidth #- (2 * self.nPanelX)
		self.nPanelLength = self.nScreenLength #- (2 * self.nPanelY)

		# Dimension of the table
		tableXOffset = 12
		tableYOffset = 13
		self.nTableX = self.nPanelX + tableXOffset
		self.nTableY = self.nPanelY + tableYOffset
		self.nTableWidth = self.nPanelWidth - (2 * tableXOffset)
		self.nTableLength = self.nPanelLength - 40 - tableYOffset
		self.nShortTableLength = self.nPanelY + self.nPanelLength - 140 # was 400 when nPanelLength was 562

		self.nSecondHalfTableX = self.nTableX + self.nTableWidth / 2 + 10
		self.nHalfTableWidth = self.nTableWidth / 2 - 10

		self.nCustomizeControlY = self.nPanelY + self.nPanelLength - 120 # was 450 when nPanelLength was 562

		BugUtil.debug("CDA Screen: %d x %d from (%d, %d) to (%d, %d)" %(self.nScreenWidth, self.nScreenLength, self.nScreenX, self.nScreenY, self.nScreenX + self.nScreenWidth, self.nScreenY + self.nScreenLength))
		BugUtil.debug("CDA Panel: %d x %d from (%d, %d) to (%d, %d)" %(self.nPanelWidth, self.nPanelLength, self.nPanelX, self.nPanelY, self.nPanelX + self.nPanelWidth, self.nPanelY + self.nPanelLength))
		BugUtil.debug("CDA Table: %d x %d from (%d, %d) to (%d, %d)" %(self.nTableWidth, self.nTableLength, self.nTableX, self.nTableY, self.nTableX + self.nTableWidth, self.nTableY + self.nTableLength))

		# Location of Text Buttons
		self.X_EXIT = self.nTableX + self.nTableWidth
		self.Y_EXIT = self.nPanelLength + self.nPanelY - 32
		self.Y_TEXT = self.nPanelLength + self.nPanelY - 27
		self.Z_TEXT = -0.1
		self.DX_TEXT = -200

# BUG - Colony Split - start

		# Location of Split Empire Button; make sure it leaves enough room for exit text
		self.SPLIT_NAME = "DomesticSplit"
		nExitTextWidth = CyInterface().determineWidth(localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper())
		self.X_SPLIT = self.X_EXIT - 50 - nExitTextWidth
		self.Y_SPLIT = self.Y_TEXT - 8

# BUG - Colony Split - end

		# Building Button Headers
		self.BUILDING_BUTTON_X_SIZE = 24
		self.BUILDING_BUTTON_Y_SIZE = 24

		# Location of Specialist Toggle Button
		self.X_SPECIAL = self.nTableX
		self.Y_SPECIAL = self.Y_TEXT - 10
		
		# Width of page dropdown
		self.PAGES_DD_W = 300

		# Location of Culture Threshold Info
		self.nCultureLevelX = self.nPanelX + self.nPanelWidth - 354 # was 670 when nPanelWidth was 1024
		self.nCultureLevelY = self.nPanelY + self.nPanelLength - 120 # was 450 when nPanelLength was 562
		self.nCultureLevelDistance = 15
		self.nCultureLevelTextOffset = 110

		# Location of next GP Threshold Info
		self.nGPLevelX = self.nPanelX + self.nPanelWidth - 154 # was 870 when nPanelWidth was 1024
		self.nGPLevelY = self.nPanelY + self.nPanelLength - 120 # was 450 when nPanelLength was 562
		self.nGPLevelDistance = 30

		self.nControlSize = 28

		# Location/Size of the Specialist Images
		self.nFirstSpecialistX = self.nPanelX + 30
		self.nSpecialistY = self.nPanelY + self.nPanelLength - 120 # was 450 when nPanelLength was 562
		self.nSpecialistWidth = 32
		self.nSpecialistLength = 32
		self.nSpecialistDistance = 70

		# Offset from Specialist Image/Size for the Specialist Plus/Minus buttons
		self.nPlusOffsetX = -4
		self.nMinusOffsetX = 16
		self.nPlusOffsetY = self.nMinusOffsetY = 30
		self.nPlusWidth = self.nPlusHeight = self.nMinusWidth = self.nMinusHeight = 20

		# Offset from Specialist Image for the Specialist Text
		self.nSpecTextOffsetX = 0
		self.nSpecTextOffsetY = 50

		# Flag so that we only do this again if really necessary
		global g_bMustCreatePositions
		g_bMustCreatePositions = False

	def getScreen(self):
		""" Return the screen we draw with. """
		return CyGInterfaceScreen(self.SCREEN_NAME, CvScreenEnums.DOMESTIC_ADVISOR)

	def getCurrentCity (self):
		""" Get the current selected city."""
		screen = self.getScreen()
		iPlayer = PyPlayer(CyGame().getActivePlayer())
		cityList = iPlayer.getCityList()
		for i in range(len(cityList)):
			if screen.isRowSelected(self.currentPage, i):
				for j in range(len(cityList)):
					if(cityList[j].getName() == screen.getTableText(self.currentPage, 1, i)):
						return cityList[j].city

		return None

	def getNumSpecialistInfos (self):
		""" Get the number of specialist types (that WE deal with)."""
		try:
			return len (self.SPECIALIST_ICON_DICT)
		except TypeError:
			return 0

	def getNumEmphasizeInfos (self):
		""" Get the number of emphasis types (that WE deal with)."""
		return len (self.AUTOMATION_ICON_DICT)

	def interfaceScreen(self):
		"""
		Screen construction function.
		This is the function that's called whenever F1 is pressed.
		"""

		# Initialize all the stuff we couldn't in the init function
		self.createDictionaries()

		screen = self.getScreen()
#		screen.setForcedRedraw (True)

		# createPositions determines our size/positions and should only
		# be called if something has changed.
		if g_bMustCreatePositions:
			self.createPositions (screen)

		screen.setDimensions (self.nScreenX, self.nScreenY, self.nScreenWidth, self.nScreenLength)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
	
		# Draw the basic screen
		self.drawBasicScreen()

		# Draw the table and the rest based on the mode
		self.drawScreen (self.currentPage)
		
# BUG - Colony Split - start

		player = gc.getActivePlayer()
		if (player.canSplitEmpire()):
			self.bCanLiberate = true
		else:
			self.bCanLiberate = false
			(loopCity, iter) = player.firstCity(false)
			while (loopCity):
				if loopCity.getLiberationPlayer(false) != -1:
					self.bCanLiberate = true
					break
				(loopCity, iter) = player.nextCity(iter, false)
		
		if (self.bCanLiberate):
			screen.setImageButton( self.SPLIT_NAME, "", self.X_SPLIT, self.Y_SPLIT, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_FREE_COLONY).getActionInfoIndex(), -1 )
			screen.setStyle( self.SPLIT_NAME, "Button_HUDAdvisorVictory_Style" )

# BUG - Colony Split - end

	def drawBasicScreen (self):
		"""
		Draws the Basic parts common to all Domestic Advisor Screens.
		"""
		screen = self.getScreen()

		# Here we set the background widget and exit button, and we show the screen
		screen.addPanel( self.BACKGROUND_ID, u"", u"", True, False, self.nPanelX, self.nPanelY, self.nPanelWidth, self.nPanelLength, PanelStyles.PANEL_STYLE_MAIN )
		#screen.addDDSGFC( self.BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("SCREEN_BG").getPath(), 0, 29, 1024, 592, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		# Text Buttons
		screen.setText(self.EXIT_NAME, "Background", localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper(), CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, self.Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

		x = self.X_SPECIAL + self.PAGES_DD_W + 10

		# Buttons to switch screens
		screen.setImageButton( self.PREV_PAGE_NAME, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_LEFT").getPath(), x, self.Y_SPECIAL, self.nControlSize, self.nControlSize, WidgetTypes.WIDGET_CDA_PREV_PAGE, -1, -1 )
		x += self.nControlSize + 2
		screen.setImageButton( self.NEXT_PAGE_NAME, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_RIGHT").getPath(), x, self.Y_SPECIAL, self.nControlSize, self.nControlSize, WidgetTypes.WIDGET_CDA_NEXT_PAGE, -1, -1 )
		x += self.nControlSize + 12
		screen.addCheckBoxGFC(self.START_CUSTOMIZING_NAME, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BTN_FOREIGN").getPath(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), x, self.Y_SPECIAL, self.nControlSize, self.nControlSize, WidgetTypes.WIDGET_CDA_EDIT_PAGE, -1, -1, ButtonStyles.BUTTON_STYLE_IMAGE )
		x += self.nControlSize + 2
		screen.setImageButton( self.RENAME_PAGE_NAME, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BTN_EVENT_LOG").getPath(), x, self.Y_SPECIAL, self.nControlSize, self.nControlSize, WidgetTypes.WIDGET_CDA_RENAME_PAGE, -1, -1 )
		x += self.nControlSize + 2
		info = gc.getSpecialistInfo(gc.getInfoTypeForString("SPECIALIST_CITIZEN"))
		screen.addCheckBoxGFC(self.TOGGLE_SPECS_NAME, info.getTexture(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), x, self.Y_SPECIAL, self.nControlSize, self.nControlSize, WidgetTypes.WIDGET_CDA_TOGGLE_SPECIALISTS, -1, -1, ButtonStyles.BUTTON_STYLE_IMAGE )
		x += self.nControlSize + 2
		screen.setImageButton( self.ADD_PAGE_NAME, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_PLUS").getPath(), x, self.Y_SPECIAL, self.nControlSize, self.nControlSize, WidgetTypes.WIDGET_CDA_ADD_PAGE, -1, -1 )
		x += self.nControlSize + 2
		screen.setImageButton( self.DEL_PAGE_NAME, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_MINUS").getPath(), x, self.Y_SPECIAL, self.nControlSize, self.nControlSize, WidgetTypes.WIDGET_CDA_REMOVE_PAGE, -1, -1 )
		x += self.nControlSize + 2
		screen.setImageButton( self.PAGE_UP_NAME, ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_UPARROW").getPath(), x, self.Y_SPECIAL, self.nControlSize, self.nControlSize, WidgetTypes.WIDGET_CDA_MOVE_PAGE_UP, -1, -1 )
		x += self.nControlSize + 2
		screen.setImageButton( self.PAGE_DOWN_NAME, ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_DOWNARROW").getPath(), x, self.Y_SPECIAL, self.nControlSize, self.nControlSize, WidgetTypes.WIDGET_CDA_MOVE_PAGE_DOWN, -1, -1 )
		x += self.nControlSize + 12
		screen.setImageButton( self.SAVE_NAME, ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_MENU_ICON").getPath(), x, self.Y_SPECIAL, self.nControlSize, self.nControlSize, WidgetTypes.WIDGET_CDA_SAVE, -1, -1 )
		x += self.nControlSize + 2
		screen.setImageButton( self.RELOAD_PAGES_NAME, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath(), x, self.Y_SPECIAL, self.nControlSize, self.nControlSize, WidgetTypes.WIDGET_CDA_RELOAD, -1, -1 )
		x += self.nControlSize + 2

		# Cultural Levels Text
		screen.setText (self.CULTURE_TEXT_NAME, "Background", self.cultureIcon, CvUtil.FONT_LEFT_JUSTIFY, self.nCultureLevelX, self.nCultureLevelY, self.Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Start with 2 because we need it farther from the icon.
		iCount = 2
		# For each cultural level
		for i in range (gc.getNumCultureLevelInfos()):
			pCultureLevel = gc.getCultureLevelInfo (i)
			# Get the value
			nValue = GameUtil.getCultureThreshold(i)
			# Only show non-zero levels
			if (nValue != 0):
				# Set text
				screen.setText (self.CULTURE_TEXT_NAME + str(i), "Background", "<font=2>" + pCultureLevel.getText() + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.nCultureLevelX, self.nCultureLevelY + (self.nCultureLevelDistance * iCount), self.Z_TEXT, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				# Set value
				screen.setText (self.CULTURE_TEXT_NAME + self.NUMBER_TEXT + str(i), "Background", "<font=2>" + str(nValue) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.nCultureLevelX + self.nCultureLevelTextOffset, self.nCultureLevelY + (self.nCultureLevelDistance * iCount), self.Z_TEXT, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				# Increment counter
				iCount += 1

		# get Player
		iPlayer = PyPlayer(CyGame().getActivePlayer())

		# GP Level Text
		screen.setText (self.GP_TEXT_NAME, "Background", self.figureheadIcon, CvUtil.FONT_RIGHT_JUSTIFY, self.nGPLevelX, self.nGPLevelY, self.Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setText (self.GP_TEXT_NAME + self.NUMBER_TEXT, "Background", "<font=2>" + str (iPlayer.player.greatPeopleThreshold(false)) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.nGPLevelX, self.nGPLevelY + self.nGPLevelDistance, self.Z_TEXT, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Header...
		#szText = "<font=4>" + localText.getText("TXT_KEY_DOMESTIC_ADVISOR_TITLE", ()).upper() + "</font>"
		#screen.setLabel( "DomesticTitleHeader", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, 472, 40, STANDARD_Z, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		# Draw the specialist (but don't SHOW them)
		self.drawSpecialists()

		# Draw the customization controls (but don't SHOW them)
		self.drawCustomizationControls()

	# Draw the specialist and their increase and decrease buttons
	def drawSpecialists (self):
		""" The function to draw but not show all the specialists."""
		screen = self.getScreen()

		# Citizen Buttons
		for i in range( self.getNumSpecialistInfos() ):
		
			if (gc.getSpecialistInfo(i).isVisible()):
			
				szName = self.SPECIALIST_IMAGE_NAME + str(i)
				screen.setImageButton( szName, gc.getSpecialistInfo(i).getTexture(), self.nFirstSpecialistX + (self.nSpecialistDistance * i), self.nSpecialistY, self.nSpecialistWidth, self.nSpecialistLength, WidgetTypes.WIDGET_CITIZEN, i, -1 )
				screen.hide( szName )

		# Increase Specialists...
		for i in range( self.getNumSpecialistInfos() ):
			if (gc.getSpecialistInfo(i).isVisible()):
				szName = self.SPECIALIST_PLUS_NAME + str(i)
				screen.setButtonGFC( szName, u"", "", self.nFirstSpecialistX + (self.nSpecialistDistance * i) + self.nPlusOffsetX, self.nSpecialistY + self.nPlusOffsetY, self.nPlusWidth, self.nPlusHeight, WidgetTypes.WIDGET_CHANGE_SPECIALIST, i, 1, ButtonStyles.BUTTON_STYLE_CITY_PLUS )
				screen.hide( szName )

		# Decrease specialists
		for i in range( self.getNumSpecialistInfos() ):
			if (gc.getSpecialistInfo(i).isVisible()):
				szName = self.SPECIALIST_MINUS_NAME + str(i)
				screen.setButtonGFC( szName, u"", "", self.nFirstSpecialistX + (self.nSpecialistDistance * i) + self.nMinusOffsetX, self.nSpecialistY + self.nMinusOffsetY, self.nMinusWidth, self.nMinusHeight, WidgetTypes.WIDGET_CHANGE_SPECIALIST, i, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS )
				screen.hide( szName )

		# Specialist text
		for i in range (self.getNumSpecialistInfos()):
			if (gc.getSpecialistInfo(i).isVisible()):
				szName = self.SPECIALIST_TEXT_NAME + str(i)
				screen.setText (szName, "Background", "", CvUtil.FONT_LEFT_JUSTIFY, self.nFirstSpecialistX + (self.nSpecialistDistance * i) + self.nSpecTextOffsetX, self.nSpecialistY + self.nSpecTextOffsetY, self.Z_TEXT, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.hide (szName)

	def showSpecialists (self):
		""" Function which shows the specialists."""
		screen = self.getScreen()

		# First, hide the specialists! :D
		self.hideSpecialists()

		# Get the current city
		city = self.getCurrentCity()
		if (city):
			
			# Get values which we will need for each calculation
			nPopulation = city.getPopulation()
			nFreeSpecial = city.totalFreeSpecialists()

			# For each specialist type
			for i in range( self.getNumSpecialistInfos() ):

				# Show all the specialist images
				szName = self.SPECIALIST_IMAGE_NAME + str(i)
				screen.show( szName )

				# Show all the specialist text
				szName = self.SPECIALIST_TEXT_NAME + str(i)
				screen.setText (szName, "Background", str (city.getSpecialistCount(i)) + "/" + str (city.getMaxSpecialistCount(i)) + u" %c" % self.SPECIALIST_ICON_DICT[i], CvUtil.FONT_LEFT_JUSTIFY, self.nFirstSpecialistX + (self.nSpecialistDistance * i) + self.nSpecTextOffsetX, self.nSpecialistY + self.nSpecTextOffsetY, self.Z_TEXT, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.show (szName)

				# If the specialist is valid and we can increase it
				if (city.isSpecialistValid(i, 1) and (city.getForceSpecialistCount(i) < (nPopulation + nFreeSpecial))):
					# Show the Plus
					szName = self.SPECIALIST_PLUS_NAME + str(i)
					screen.show( szName )

				# if we HAVE specialists already and they're not forced.
				if (city.getSpecialistCount(i) > 0 or city.getForceSpecialistCount(i) > 0 ):
					# Show the Minus
					szName = self.SPECIALIST_MINUS_NAME + str(i)
					screen.show( szName )
							
	def hideSpecialists (self):
		""" Function to hide all the specialists and the accompanying data."""
		screen = self.getScreen()

		# Hide Everything related to specialists
		for i in range( self.getNumSpecialistInfos() ):
			szName = self.SPECIALIST_IMAGE_NAME + str(i)
			screen.hide (szName)
			szName = self.SPECIALIST_PLUS_NAME + str(i)
			screen.hide (szName)
			szName = self.SPECIALIST_MINUS_NAME + str(i)
			screen.hide (szName)
			szName = self.SPECIALIST_TEXT_NAME + str(i)
			screen.hide (szName)

	def showCultureLegend (self):

		screen = self.getScreen()
		screen.show(self.CULTURE_TEXT_NAME)
		# For each cultural level
		for i in range (gc.getNumCultureLevelInfos()):
				screen.show(self.CULTURE_TEXT_NAME + str(i))
				screen.show(self.CULTURE_TEXT_NAME + self.NUMBER_TEXT + str(i))

	def hideCultureLegend (self):

		screen = self.getScreen()
		screen.hide(self.CULTURE_TEXT_NAME)
		# For each cultural level
		for i in range (gc.getNumCultureLevelInfos()):
				screen.hide(self.CULTURE_TEXT_NAME + str(i))
				screen.hide(self.CULTURE_TEXT_NAME + self.NUMBER_TEXT + str(i))

	def showGPLegend(self):

		screen = self.getScreen()
		screen.show(self.GP_TEXT_NAME)
		screen.show(self.GP_TEXT_NAME + self.NUMBER_TEXT)

	def hideGPLegend(self):

		screen = self.getScreen()
		screen.hide(self.GP_TEXT_NAME)
		screen.hide(self.GP_TEXT_NAME + self.NUMBER_TEXT)

	def drawCustomizationControls(self):
		screen = self.getScreen()
		
		x = self.nTableX + self.nHalfTableWidth - self.nControlSize
		screen.setImageButton( self.COLUMNDN_NAME, ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_DOWNARROW").getPath(), x, self.nCustomizeControlY, self.nControlSize, self.nControlSize, WidgetTypes.WIDGET_CDA_MOVE_COLUMN_DOWN, -1, -1 )
		x -= self.nControlSize + 2
		screen.setImageButton( self.COLUMNUP_NAME, ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_UPARROW").getPath(), x, self.nCustomizeControlY, self.nControlSize, self.nControlSize, WidgetTypes.WIDGET_CDA_MOVE_COLUMN_UP, -1, -1 )
		x -= self.nControlSize + 2
		screen.setImageButton( self.DELCOLUMN_NAME, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_MINUS").getPath(), x, self.nCustomizeControlY, self.nControlSize, self.nControlSize, WidgetTypes.WIDGET_CDA_REMOVE_COLUMN, -1, -1 )
		x -= self.nControlSize + 2
		screen.setImageButton( self.ADDCOLUMN_NAME, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_PLUS").getPath(), x, self.nCustomizeControlY, self.nControlSize, self.nControlSize, WidgetTypes.WIDGET_CDA_ADD_COLUMN, -1, -1 )
		x -= self.nControlSize + 2
		screen.setImageButton( self.COLUMN_WIDEN_NAME, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_RIGHT").getPath(), x, self.nCustomizeControlY, self.nControlSize, self.nControlSize, WidgetTypes.WIDGET_CDA_EXPAND_COLUMN, -1, -1 )
		x -= self.nControlSize + 2
		screen.setImageButton( self.COLUMN_SHRINK_NAME, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_LEFT").getPath(), x, self.nCustomizeControlY, self.nControlSize, self.nControlSize, WidgetTypes.WIDGET_CDA_SHRINK_COLUMN, -1, -1 )
		
		self.hideCustomizationControls()

	def showCustomizationControls(self):

		screen = self.getScreen()

		screen.setState(self.START_CUSTOMIZING_NAME, True)

		# No need for screen.show(self.CUSTOMIZE_PAGE) - that table is redrawn.
		screen.show(self.COLUMNS_LIST_PAGE)
		screen.show(self.ADDCOLUMN_NAME)
		screen.show(self.DELCOLUMN_NAME)
		screen.show(self.COLUMNUP_NAME)
		screen.show(self.COLUMNDN_NAME)
		screen.show(self.COLUMN_SHRINK_NAME)
		screen.show(self.COLUMN_WIDEN_NAME)
		
		if self.isFlavorful:

			screen.show(self.RENAME_PAGE_NAME)
			screen.show(self.RENAME_PAGE_NAME)
			screen.show(self.ADD_PAGE_NAME)
			screen.show(self.DEL_PAGE_NAME)
			screen.show(self.PAGE_UP_NAME)
			screen.show(self.PAGE_DOWN_NAME)
			screen.show(self.SAVE_NAME)
			screen.show(self.RELOAD_PAGES_NAME)
			screen.show(self.TOGGLE_SPECS_NAME)
			
			page = self.PAGES[self.currentPageNum]
			screen.setState(self.TOGGLE_SPECS_NAME, page["showSpecControls"])

	def hideCustomizationControls(self):

		screen = self.getScreen()

		screen.setState(self.START_CUSTOMIZING_NAME, False)

		screen.hide(self.CUSTOMIZE_PAGE)
		screen.hide(self.COLUMNS_LIST_PAGE)
		screen.hide(self.ADDCOLUMN_NAME)
		screen.hide(self.DELCOLUMN_NAME)
		screen.hide(self.COLUMNUP_NAME)
		screen.hide(self.COLUMNDN_NAME)
		screen.hide(self.COLUMN_SHRINK_NAME)
		screen.hide(self.COLUMN_WIDEN_NAME)

		if self.isFlavorful:

			screen.hide(self.RENAME_PAGE_NAME)
			screen.hide(self.RENAME_PAGE_NAME)
			screen.hide(self.ADD_PAGE_NAME)
			screen.hide(self.DEL_PAGE_NAME)
			screen.hide(self.PAGE_UP_NAME)
			screen.hide(self.PAGE_DOWN_NAME)
			screen.hide(self.SAVE_NAME)
			screen.hide(self.RELOAD_PAGES_NAME)
			screen.hide(self.TOGGLE_SPECS_NAME)

	def hide (self, screen, page):
		""" Hide function which hides a specific screen."""
		screen.hide (page)
		self.hideSpecialists()
	
	def drawScreen (self, page):
		""" Draw the screen based on which mode we get."""
		screen = self.getScreen()

		# Change the visible page?
		if(not self.customizing and self.visiblePage != self.currentPage):
			if(self.visiblePage):
				screen.hide(self.visiblePage)

			screen.show(self.currentPage)
			self.visiblePage = self.currentPage

		# Hide the menu and Civilopedia buttons
		CyInterface().setDirty(InterfaceDirtyBits.MiscButtons_DIRTY_BIT, True)

		start = time.clock()
		# Draw the city list...
		self.drawContents (page)
		end = time.clock()
		BugUtil.debug("drawContents: " + str(end - start) + "s")

	def calculateFounded (self, city, szKey, arg):

		# City founded date...
		iTurnTime = city.getGameTurnFounded()
		return unicode(CyGameTextMgr().getTimeStr(iTurnTime, false))

	def calculateFeatures (self, city, szKey, arg):

		szReturn = ""

		# First look for Government Centers
		if city.isGovernmentCenter():
			# And distinguish between the Capital and the others (Forbidden Palace
			# and Versailles)
			if city.isCapital():
				szReturn += self.starIcon
			else:
				szReturn += self.silverStarIcon

		# add National Wonders
		for i in range(gc.getNumBuildingInfos()):
			info = gc.getBuildingInfo(i)
			classInfo = gc.getBuildingClassInfo(info.getBuildingClassType())
			if classInfo.getMaxGlobalInstances() == -1 and classInfo.getMaxPlayerInstances() == 1 and city.getNumBuilding(i) > 0 and not info.isCapital():
				# Use bullets as markers for National Wonders
				szReturn += self.bulletIcon

		if city.isDisorder():

			if city.isOccupation():
				szOccu = u"%c" % CyGame().getSymbolID(FontSymbols.OCCUPATION_CHAR)
				szReturn += szOccu +":"+unicode(city.getOccupationTimer())
			else:
				szReturn += self.angryIcon

		pTradeCity = city.getTradeCity(0)
		if (pTradeCity and pTradeCity.getOwner() >= 0):
			szReturn += self.tradeIcon

		return szReturn

	def calculateDefense(self, city, szKey, arg):
		return unicode(city.plot().defenseModifier(-1, True, False)) + u"%"

	def calculateEspionageDefense(self, city, szKey, arg):
		return unicode(city.getEspionageDefenseModifier()) + u"%"

	def calculateThreats(self, city, szKey, arg):

		szReturn = u""

		player = PyPlayer(CyGame().getActivePlayer())

		for i in range(gc.getMAX_PLAYERS()):
			if player.getTeam().isAtWar(gc.getPlayer(i).getTeam()):
				if city.isVisible(gc.getPlayer(i).getTeam(), False):
					szReturn = self.angryIcon
					break

		return szReturn

	def calculateNetHappiness (self, city, szKey="", arg=0):
		return city.happyLevel() - city.unhappyLevel(0)

	def calculateNetHealth (self, city, szKey="", arg=0):
		return city.goodHealth() - city.badHealth(False)

	def calculateGrowth (self, city, szKey, arg):
		szReturn = u""

		# Turns til Growth
 		nFood = city.foodDifference (True)

		# If this is a food production (i.e., worker or settler)
		if (self.isFoodProduction(city.getProductionName())):
			# We need to indicate there's no growth manually
			szReturn = u"-"
		else:
			# Otherwise, just call FoodTurnsLeft
			szReturn = unicode (city.getFoodTurnsLeft())

		# Not enough food, so calculate how many turns until we starve.
		# We put this here because we still starve if building a food production
		if nFood < 0:
			# Use floor divide (//) because we want the number it'll drop below 0
			# (that's also the reason for the additional 1)
			szReturn = unicode ((city.getFood()+1) // nFood)

		return szReturn

	def calculateFood (self, city, szKey, arg):

		# If this is a food production (i.e., worker or settler)
		if (self.isFoodProduction(city.getProductionName())):
			nFood = city.getCurrentProductionDifference (False, False) - city.getCurrentProductionDifference (True, False)
		else:
			nFood = city.foodDifference (True)
		return nFood

	def calculateProduction (self, city, szKey, arg):
		return unicode(city.getCurrentProductionDifference (True, False))

	def calculateMaintenance (self, city, szKey, arg):
		return unicode(city.getMaintenance())

	def calculateTrade (self, city, szKey, arg):
		"""arg: None to sum all, 'D' to count domestic, 'F' to count foreign."""
		nTotalTradeProfit = 0

		# For each trade route possible
		for nTradeRoute in range (gc.getDefineINT("MAX_TRADE_ROUTES")):
			# Get the next trade city
			pTradeCity = city.getTradeCity(nTradeRoute)
			# Not quite sure what this does but it's in the MainInterface
			# and I pretty much C&Ped :p
			if (pTradeCity and pTradeCity.getOwner() >= 0):
				bForeign = city.getOwner() != pTradeCity.getOwner()
				if (not arg or ((arg == "F" and bForeign) or (arg == "D" and not bForeign))):
					for j in range( YieldTypes.NUM_YIELD_TYPES ):
						iTradeProfit = city.calculateTradeYield(j, city.calculateTradeProfit(pTradeCity))
	
						# If the TradeProfit is greater than 0, add it to the total
						if ( iTradeProfit > 0 ):
							nTotalTradeProfit += iTradeProfit

		return unicode(nTotalTradeProfit)

	def countTradeRoutes (self, city, szKey, arg):
		"""arg: None to count all, 'D' to count domestic, 'F' to count foreign."""
		nRoutes = 0

		# For each trade route possible
		for nTradeRoute in range (gc.getDefineINT("MAX_TRADE_ROUTES")):
			# Get the next trade city
			pTradeCity = city.getTradeCity(nTradeRoute)
			# Not quite sure what this does but it's in the MainInterface
			# and I pretty much C&Ped :p
			if (pTradeCity and pTradeCity.getOwner() >= 0):
				bForeign = city.getOwner() != pTradeCity.getOwner()
				if (not arg or ((arg == "F" and bForeign) or (arg == "D" and not bForeign))):
					nRoutes += 1

		return unicode(nRoutes)

	def countSpecialists (self, city, szKey, arg):
		"""arg: specialist type string (excluding "SPECIALIST_") e.g. use "ARTIST" to count artist specialists"""
		szSpecialistType = "SPECIALIST_" + arg
		nCount = city.getSpecialistCount(gc.getInfoTypeForString(szSpecialistType))
		if nCount > 0:
			return unicode(nCount)
		else:
			return u"-"

	def countFreeSpecialists (self, city, szKey, arg):
		"""arg: specialist type string (excluding "SPECIALIST_") e.g. use "ARTIST" to count artist specialists"""
		szSpecialistType = "SPECIALIST_" + arg
		nCount = city.getFreeSpecialistCount(gc.getInfoTypeForString(szSpecialistType))
		if nCount > 0:
			return unicode(nCount)
		else:
			return u"-"

	def calculateProducing (self, city, szKey, arg):

		szReturn = u""
# BUG - Production Grouping - start
		bProdColors = AdvisorOpt.isProductionGroupingColors()
		bProdIcons = AdvisorOpt.isProductionGroupingIcons()
# BUG - Production Grouping - end

		# If there's something in the queue,
		if (city.getOrderQueueLength() > 0):

			# Get the name of whatever it's producing.
			szReturn = city.getProductionName()

# BUG - Base XP for units - start
			# Note this has been separated out so that it is always in effect
			# even if user chooses to disable the production coloring/grouping
			if city.isProductionUnit():
				iUnit = city.getProductionUnit()
				pInfo = gc.getUnitInfo(iUnit)
				if pInfo.getUnitCombatType() != UnitCombatTypes.NO_UNITCOMBAT:
					iExp = city.getProductionExperience(iUnit)
					szReturn = szReturn + u" " + localText.getText("TXT_KEY_CDA_BASE_XP", (iExp,))
# BUG - Base XP for units - end

# BUG - Production Grouping - start
			if (bProdColors or bProdIcons):
				szColorKey = "DEFAULT"
				szIcon = self.hammerIcon
				if city.isProductionBuilding():
					szColorKey = "WONDER"
					pInfo = gc.getBuildingClassInfo(gc.getBuildingInfo(city.getProductionBuilding()).getBuildingClassType())
					if pInfo.getMaxGlobalInstances() != -1:
						szIcon = self.starIcon
					elif pInfo.getMaxTeamInstances() != -1:
						szIcon = self.silverStarIcon
					elif pInfo.getMaxPlayerInstances() != -1:
						szIcon = self.silverStarIcon
					else:
						szColorKey = "BUILDING"
				elif city.isProductionProcess():
					iType = city.getProductionProcess()
					if iType == gc.getInfoTypeForString("PROCESS_WEALTH"):
						szColorKey = "WEALTH"
						szIcon = self.goldIcon
					elif iType == gc.getInfoTypeForString("PROCESS_RESEARCH"):
						szColorKey = "RESEARCH"
						szIcon = self.researchIcon
					elif iType == gc.getInfoTypeForString("PROCESS_CULTURE"):
						szColorKey = "CULTURE"
						szIcon = self.cultureIcon
				elif city.isProductionProject():
					szColorKey = "PROJECT"
					pInfo = gc.getProjectInfo(city.getProductionProject())
					if pInfo.getMaxGlobalInstances() != -1:
						szIcon = self.starIcon
					elif pInfo.getMaxTeamInstances() != -1:
						szIcon = self.silverStarIcon
				elif city.isProductionUnit():
					szColorKey = "UNIT"
					iUnit = city.getProductionUnit()
					pInfo = gc.getUnitInfo(iUnit)
					iType = pInfo.getDomainType()
					if pInfo.getUnitCombatType() != UnitCombatTypes.NO_UNITCOMBAT:
 						szIcon = self.militaryIcon
# 						if iType == DomainTypes.DOMAIN_SEA:
# 							szIcon = self.seaIcon
# 						elif iType == DomainTypes.DOMAIN_LAND:
# 							szIcon = self.landIcon
# 						elif iType == DomainTypes.DOMAIN_AIR:
# 							szIcon = self.airIcon
# 						elif iType == DomainTypes.DOMAIN_IMMOBILE:
# 							szIcon = self.airIcon
					else:
 						szIcon = self.footIcon
				if bProdIcons:
					szReturn = szIcon + szReturn
				if bProdColors:
					szReturn = localText.changeTextColor (szReturn, self.PROD_COLOR_DICT[szColorKey])
# BUG - Production Grouping - end

		# Otherwise we're not producing anything. Leave it blank.
		else:
			szReturn = u"-"
# BUG - Production Grouping - start
			if bProdIcons:
				szReturn = self.cancelIcon + szReturn
			if bProdColors:
				szReturn = localText.changeTextColor (szReturn, self.PROD_COLOR_DICT["NOTHING"])
# BUG - Production Grouping - end

		return szReturn

	def calculateProducingTurns (self, city, szKey, arg):

		szReturn = u""

		# If there's something in the queue,
		if (city.getOrderQueueLength() > 0):

			# If it's not a process (i.e., Wealth, Research, Culture)
			if (not (city.isProductionProcess())):

				szReturn = unicode(city.getProductionTurnsLeft())

		return szReturn

	def calculateWhipPopulation (self, city, szKey, arg):
		
		if (city.canHurry(self.HURRY_TYPE_POP, False)):
			return unicode(city.hurryPopulation(self.HURRY_TYPE_POP))
		else:
			return self.objectNotPossible

	def calculateWhipOverflowProduction (self, city, szKey, arg):
		
		return self.calculateWhipOverflow(city, szKey, arg)[0]

	def calculateWhipOverflowGold (self, city, szKey, arg):
		
		return self.calculateWhipOverflow(city, szKey, arg)[1]

	def calculateWhipOverflow (self, city, szKey, arg):
		
		if (city.canHurry(self.HURRY_TYPE_POP, False)):
			iOverflow = city.hurryProduction(self.HURRY_TYPE_POP) - city.productionLeft()
			if CityScreenOpt.isWhipAssistOverflowCountCurrentProduction():
				iOverflow = iOverflow + city.getCurrentProductionDifference(True, False)
			iMaxOverflow = min(city.getProductionNeeded(), iOverflow)
			iOverflowGold = max(0, iOverflow - iMaxOverflow) * gc.getDefineINT("MAXED_UNIT_GOLD_PERCENT") / 100
			iOverflow =  100 * iMaxOverflow / city.getBaseYieldRateModifier(gc.getInfoTypeForString("YIELD_PRODUCTION"), city.getProductionModifier())
			return unicode(iOverflow), unicode(iOverflowGold)
		else:
			return self.objectNotPossible, self.objectNotPossible

	def calculateWhipAnger (self, city, szKey, arg):
		
		iAnger = city.getHurryAngerTimer()
		if (iAnger > 0 or city.canHurry(self.HURRY_TYPE_POP, False)):
			return iAnger
		else:
			return self.objectNotPossible

	def calculateHurryGoldCost (self, city, szKey, arg):
		
		if (city.canHurry(self.HURRY_TYPE_GOLD, False)):
			return unicode(city.hurryGold(self.HURRY_TYPE_GOLD))
		else:
			return self.objectNotPossible

	def calculateConscriptAnger (self, city, szKey, arg):
		
		iAnger = city.getConscriptAngerTimer()
		if (iAnger > 0 or city.canConscript()):
			return iAnger
		else:
			return self.objectNotPossible

	def calculatePotentialConscriptUnit (self, city, szKey, arg):
		
		szReturn = unicode(gc.getUnitInfo(city.getConscriptUnit()).getDescription() )
		return szReturn

	def calculateConscriptUnit (self, city, szKey, arg):
		
		if(city.canConscript()):
			szReturn = unicode(gc.getUnitInfo(city.getConscriptUnit()).getDescription() )
		else:
			szReturn = u""
		return szReturn

	def calculateReligions (self, city, szKey, arg):

		szReturn = u""

		lHolyCity = []
		lReligions = []
		for i in range(gc.getNumReligionInfos()):
			if city.isHolyCityByType(i):
				lHolyCity.append(i)
			elif city.isHasReligion(i):
				lReligions.append(i)

		for i in range(len(lHolyCity)):
			szReturn += u"%c" %(gc.getReligionInfo(lHolyCity[i]).getHolyCityChar())

		for i in range(len(lReligions)):
			szReturn += u"%c" %(gc.getReligionInfo(lReligions[i]).getChar())

		return szReturn

	def calculateCorporations (self, city, szKey, arg):

		szReturn = u""

		lHeadquarters = []
		lCorps = []
		for i in range(gc.getNumCorporationInfos()):
			if city.isHeadquartersByType(i):
				lHeadquarters.append(i)
			elif city.isHasCorporation(i):
				lCorps.append(i)

		for i in range(len(lHeadquarters)):
			szReturn += u"%c" %(gc.getCorporationInfo(lHeadquarters[i]).getHeadquarterChar())

		for i in range(len(lCorps)):
			szReturn += u"%c" %(gc.getCorporationInfo(lCorps[i]).getChar())

		return szReturn

	def calculateSpecialists (self, city, szKey, arg):

		szReturn = u"<font=1>"

		# For each specialist type
		for i in range( self.getNumSpecialistInfos() ):

			nCount = city.getSpecialistCount (i)
			# If more than one specialist
			if (nCount > 1):
				szReturn += self.SPECIALIST_ICON_DICT[i] + "x" + str(nCount) + " "
			elif (nCount == 1):
				szReturn += self.SPECIALIST_ICON_DICT[i] + " "

		szReturn += u"</font>"

		return szReturn

	def calculateAutomation (self, city, szKey, arg):

		szReturn = u"<font=1>"

		nNumEmphasize = self.getNumEmphasizeInfos()
		if city.isCitizensAutomated():
			szReturn += u"C"
		if city.isProductionAutomated():
			szReturn += u"P"
		for i in range( nNumEmphasize ):
			nNum = nNumEmphasize - i - 1
			if (city.AI_isEmphasize (nNum)):
				szReturn += self.AUTOMATION_ICON_DICT[nNum]

		szReturn += u"</font>"

		return szReturn

	def calculatePower (self, city, szKey, arg):

		szReturn = u""

		if city.isPower():
			szReturn += self.powerIcon

		return szReturn

	def calculateTotalCulture (self, city, szKey, arg):

		return city.getCulture(CyGame().getActivePlayer())

	def calculateCultureTurns (self, city, szKey, arg):

		iCultureTimes100 = city.getCultureTimes100(gc.getGame().getActivePlayer())
		iCultureRateTimes100 = city.getCommerceRateTimes100(CommerceTypes.COMMERCE_CULTURE)
		if iCultureRateTimes100 > 0:
			iCultureLeftTimes100 = 100 * city.getCultureThreshold() - iCultureTimes100
			return (iCultureLeftTimes100 + iCultureRateTimes100 - 1) / iCultureRateTimes100
		else:
			return u"-"

	def calculateGreatPeopleTurns (self, city, szKey, arg):

		iGreatPersonRate = city.getGreatPeopleRate()
		if iGreatPersonRate > 0:
			iGPPLeft = gc.getPlayer(gc.getGame().getActivePlayer()).greatPeopleThreshold(false) - city.getGreatPeopleProgress()
			return (iGPPLeft + iGreatPersonRate - 1) / iGreatPersonRate
		else:
			return u"-"

	def canHurry (self, city, szKey, arg):

		if city.canHurry(arg, False):
			return self.objectHave
		else:
			return self.objectNotPossible

	def canLiberate (self, city, szKey, arg):

		if city.getLiberationPlayer(False) != -1:
			return self.objectHave
		else:
			return self.objectNotPossible

	def calculateValue (self, city, szKey, arg):

		szReturn = u""

		if szKey.find("BUILDING_") == 0:
			if city.getNumActiveBuilding(self.BUILDING_DICT[szKey]) > 0 or city.getProductionName() == self.HEADER_DICT[szKey]:
				# Start with the default icons, and those that never change.
				szReturn += self.BUILDING_ICONS_DICT[szKey]

				buildingNumber = self.BUILDING_DICT[szKey]
				info = self.BUILDING_INFO_LIST[buildingNumber]

				# Indicate bonus military production if applicable
				if info.getMilitaryProductionModifier() > 0 and city.isProductionUnit() and gc.getUnitInfo(city.getProductionUnit()).isMilitaryProduction():
					if szReturn.find(self.hammerIcon) == -1:
						szReturn += self.hammerIcon

				# Calculate health and happiness effects - including that from resources.
				iHealth = city.getBuildingHealth(buildingNumber)
				iHappiness = city.getBuildingHappiness(buildingNumber)

				for i in range(gc.getNumBonusInfos()):
					if city.hasBonus(i):
						iHealth += info.getBonusHealthChanges(i)
						iHappiness += info.getBonusHappinessChanges(i)

				if iHealth > 0:
					szReturn = self.stripStr(szReturn, self.healthIcon)
					szReturn += u"%d%c" %(iHealth, self.healthIcon)
				elif iHealth < 0:
					szReturn = self.stripStr(szReturn, self.sickIcon)
					szReturn += u"%d%c" %( -(iHealth), self.sickIcon )

				# Happiness

				if iHappiness > 0:
					szReturn = self.stripStr(szReturn, self.happyIcon)
					szReturn += u"%d%c" %(iHappiness, self.happyIcon)
				elif iHappiness < 0:
					szReturn = self.stripStr(szReturn, self.unhappyIcon)
					szReturn += u"%d%c" %( -(iHappiness), self.unhappyIcon )

				# Commerce
				for i in range(CommerceTypes.NUM_COMMERCE_TYPES):
					iCommerce = city.getBuildingCommerceByBuilding(i, buildingNumber) 
					if iCommerce > 0:
						szReturn += u"%d%c" %( iCommerce, gc.getCommerceInfo(i).getChar() )

				if szReturn == "":
					szReturn = "+"

				if city.getProductionName() == self.HEADER_DICT[szKey]: # In production
					szReturn = "(" + szReturn + ")"
										
			elif city.getNumBuilding(self.BUILDING_DICT[szKey]) > 0: # Obsolete buildings
				if self.BUILDING_ICONS_DICT[szKey].find(self.cultureIcon):
					szReturn = self.stripStr(szReturn, self.cultureIcon)
					szReturn += self.cultureIcon
				else:
					szReturn += u"X"

			elif not city.canConstruct(self.BUILDING_DICT.get(szKey), False, False, False):
				szReturn += u"-"

			else:
				szReturn += u" "

		# return the final value
		return szReturn

	def calculateBuildingClass (self, city, szKey, arg):
		
		# Turn building class into building
		bldg = gc.getCivilizationInfo(city.getCivilizationType()).getCivilizationBuildings(arg)
		return self.calculateBuilding(city, szKey, bldg)

	def calculateBuilding (self, city, szKey, arg):
		
		# Turn building class into building
		if city.getNumBuilding(arg) > 0:
			if city.getNumActiveBuilding(arg) > 0:
				return self.objectHave
			else:
				return self.objectHaveObsolete
		elif city.getFirstBuildingOrder(arg) != -1:
			return self.objectUnderConstruction
		elif city.canConstruct(arg, False, False, False):
			return self.objectPossible
		elif city.canConstruct(arg, True, False, False):
			return self.objectPossibleConcurrent
		else:
			return self.objectNotPossible

	def calculateHasBonus (self, city, szKey, arg):
		
		# Determine whether or not city has the given bonus
		if (city.hasBonus(arg)):
			return self.objectHave
		else:
			return self.objectNotPossible

	def calculateBonus (self, city, szKey, arg):
		
		# Determine the effects of the given bonus (health, happiness, commerce)
		if (not city.hasBonus(arg)):
			return self.objectNotPossible
		
		szEffects = u""
		iEffect = city.getBonusHappiness(arg)
		if (iEffect == 1):
			szEffects += u"%s " % (self.happyIcon)
		elif (iEffect > 1):
			szEffects += u"%d%s " % (iEffect, self.happyIcon)
		elif (iEffect < 0):
			szEffects += u"%d%s " % (-iEffect, self.unhappyIcon)
		
		iEffect = city.getBonusHealth(arg)
		if (iEffect == 1):
			szEffects += u"%s " % (self.healthIcon)
		elif (iEffect > 1):
			szEffects += u"%d%s " % (iEffect, self.healthIcon)
		elif (iEffect < 0):
			szEffects += u"%d%s " % (-iEffect, self.sickIcon)
		
		for eYieldType in range(YieldTypes.NUM_YIELD_TYPES):
			iEffect = city.getBonusYieldRateModifier(eYieldType, arg)
			if (iEffect > 0):
				szEffects += u"%s " % self.yieldIcons[eYieldType]
#			elif (iEffect > 1 or iEffect < 0):
#				szEffects += u"%d%s " % (iEffect, self.yieldIcons[eYieldType])
		
		iNumBonuses = city.getNumBonuses(arg)
		if (self.bonusCorpYields.has_key(arg)):
			yields = self.bonusCorpYields[arg]
			for eYield in range(YieldTypes.NUM_YIELD_TYPES):
				if (yields.has_key(eYield)):
					iEffect = 0
					for eCorp, iValue in yields[eYield].iteritems():
						if (city.isActiveCorporation(eCorp)):
							iEffect += iValue * iNumBonuses * self.corpMaintPercent / 100
					iEffect = (iEffect + 99) / 100
					if (iEffect == 1):
						szEffects += u"%s " % self.yieldIcons[eYield]
					elif (iEffect > 1 or iEffect < 0):
						szEffects += u"%d%s " % (iEffect, self.yieldIcons[eYield])
		
		if (self.bonusCorpCommerces.has_key(arg)):
			commerces = self.bonusCorpCommerces[arg]
			for eCommerce in range(CommerceTypes.NUM_COMMERCE_TYPES):
				if (commerces.has_key(eCommerce)):
					iEffect = 0
					for eCorp, iValue in commerces[eCommerce].iteritems():
						if (city.isActiveCorporation(eCorp)):
							iEffect += iValue * iNumBonuses * self.corpMaintPercent / 100
					iEffect = (iEffect + 99) / 100
					if (iEffect == 1):
						szEffects += u"%s " % self.commerceIcons[eCommerce]
					elif (iEffect > 1 or iEffect < 0):
						szEffects += u"%d%s " % (iEffect, self.commerceIcons[eCommerce])
		
#		for eYieldType in range(YieldTypes.NUM_YIELD_TYPES):
#			if (city.getCorporationYield(eYieldType) > 0):
#				iEffect = 0
#				for eCorporation in range(gc.getNumCorporationInfos()):
#					if (city.isActiveCorporation(eCorporation)):
#						info = gc.getCorporationInfo(eCorporation)
#						for i in range(gc.getNUM_CORPORATION_PREREQ_BONUSES()):
#							if (info.getPrereqBonus(i) == arg):
#								iEffect += info.getYieldProduced(eYieldType) * city.getNumBonuses(arg) * self.corpMaintPercent / 100
#				iEffect = (iEffect + 99) / 100
#				if (iEffect == 1):
#					szEffects += u"%s " % self.yieldIcons[eYieldType]
#				elif (iEffect > 1 or iEffect < 0):
#					szEffects += u"%d%s " % (iEffect, self.yieldIcons[eYieldType])
#		
#		for eCommerceType in range(CommerceTypes.NUM_COMMERCE_TYPES):
#			if (city.getCorporationCommerce(eCommerceType) > 0):
#				iEffect = 0
#				for eCorporation in range(gc.getNumCorporationInfos()):
#					if (city.isActiveCorporation(eCorporation)):
#						info = gc.getCorporationInfo(eCorporation)
#						for i in range(gc.getNUM_CORPORATION_PREREQ_BONUSES()):
#							if (info.getPrereqBonus(i) == arg):
#								iEffect += info.getCommerceProduced(eCommerceType) * city.getNumBonuses(arg) * self.corpMaintPercent / 100
#				iEffect = (iEffect + 99) / 100
#				if (iEffect == 1):
#					szEffects += u"%s " % self.commerceIcons[eCommerceType]
#				elif (iEffect > 1 or iEffect < 0):
#					szEffects += u"%d%s " % (iEffect, self.commerceIcons[eCommerceType])
		
		iEffect = city.getBonusPower(arg, False) + city.getBonusPower(arg, True)
		if (iEffect == 1):
			szEffects += u"%s " % (self.powerIcon)
		elif (iEffect > 1):
			szEffects += u"%d%s " % (iEffect, self.powerIcon)
		
		if (szEffects == u""):
			return self.objectHave
		return szEffects.strip()

	def calculateFreeExperience (self, city, szKey, arg):
		"""arg: Domain identifier; "L" for Land, "S" for Sea, "A" for Air, "I" for Immobile"""
		# Thanks to MatzeHH for original version of this
		player = gc.getActivePlayer()
		# Generic modifiers first
		freeXP = city.getSpecialistFreeExperience()
		freeXP += city.getFreeExperience()
		freeXP += player.getFreeExperience()
		if (player.getStateReligion() != ReligionTypes.NO_RELIGION):
			if (city.isHasReligion(player.getStateReligion())):
				freeXP += player.getStateReligionFreeExperience()
		# Then tack on the proper domain-based extras
		if (arg == "L"):
			freeXP += city.getDomainFreeExperience(DomainTypes.DOMAIN_LAND)
		elif (arg == "S"):
			freeXP += city.getDomainFreeExperience(DomainTypes.DOMAIN_SEA)
		elif (arg == "A"):
			freeXP += city.getDomainFreeExperience(DomainTypes.DOMAIN_AIR)
		elif (arg == "I"):
			freeXP += city.getDomainFreeExperience(DomainTypes.DOMAIN_IMMOBILE)

		return unicode(freeXP)

	def findGlobalBaseYieldRateRank (self, city, szKey, arg):

		L = []
		for i in range(gc.getMAX_PLAYERS()):
			cl = PyPlayer(i).getCityList()
			for c in cl:
				L.append(c.city.getBaseYieldRate(arg))

		y = city.getBaseYieldRate(arg)
		return len([i for i in L if i > y]) + 1

	def findGlobalYieldRateRank (self, city, szKey, arg):

		L = []
		for i in range(gc.getMAX_PLAYERS()):
			cl = PyPlayer(i).getCityList()
			for c in cl:
				L.append(c.city.getYieldRate(arg))

		y = city.getYieldRate(arg)
		return len([i for i in L if i > y]) + 1

	def findGlobalCommerceRateRank (self, city, szKey, arg):

		L = []
		for i in range(gc.getMAX_PLAYERS()):
			cl = PyPlayer(i).getCityList()
			for c in cl:
				L.append(c.city.getCommerceRate(arg))

		y = city.getCommerceRate(arg)
		return len([i for i in L if i > y]) + 1


	def canAdviseToConstruct(self, city, i):
		
		info = gc.getBuildingInfo(i)
		if not city.canConstruct(i, True, False, False):
			return False
		if info.isGovernmentCenter() or info.isCapital():
			return False

		if info.getObsoleteTech() != TechTypes.NO_TECH and PyPlayer(CyGame().getActivePlayer()).getTeam().isHasTech(info.getObsoleteTech()):
			return False

		sinfo = gc.getSpecialBuildingInfo(info.getSpecialBuildingType())

		if sinfo:
			if sinfo.getObsoleteTech() != TechTypes.NO_TECH and PyPlayer(CyGame().getActivePlayer()).getTeam().isHasTech(sinfo.getObsoleteTech()):
				return False

		return True

	def advise(self, city, szKey, type):

		bestOrder = -1
		bestData = 0.0

		player = PyPlayer(CyGame().getActivePlayer())
		civInfo = gc.getCivilizationInfo(city.getCivilizationType())

		# For all cities, start with growth
		if self.calculateNetHappiness(city) > 2 and self.calculateNetHealth(city) > 2:
			for i in range(gc.getNumBuildingClassInfos()):
				bldg = civInfo.getCivilizationBuildings(i)
				if self.canAdviseToConstruct(city, bldg):
					info = gc.getBuildingInfo(bldg)
					value = info.getFoodKept() / float(info.getProductionCost())
					if(value > bestData):
						bestOrder = bldg
						bestData = value

		# then balancing health and happiness for further growth
		if bestOrder == -1:
			for i in range(gc.getNumBuildingClassInfos()):
				bldg = civInfo.getCivilizationBuildings(i)
				if self.canAdviseToConstruct(city, bldg):
					info = gc.getBuildingInfo(bldg)
					if self.calculateNetHappiness(city) < 3 and self.calculateNetHappiness(city) - self.calculateNetHealth(city) > 2:
						iHealth = info.getHealth()
						for j in range(gc.getNumBonusInfos()):
							if city.hasBonus(j):
								iHealth += info.getBonusHealthChanges(j)
						value = iHealth / float(info.getProductionCost())
						if(value > bestData):
							bestOrder = bldg
							bestData = value
					elif self.calculateNetHealth(city) < 3 and self.calculateNetHealth(city) - self.calculateNetHappiness(city) > 2:
						iHappiness = info.getHappiness()
						for j in range(gc.getNumBonusInfos()):
							if city.hasBonus(j):
								iHappiness += info.getBonusHappinessChanges(j)
						value = iHappiness  / float(info.getProductionCost())
						if(value > bestData):
							bestOrder = bldg
							bestData = value

		# First pass
		if(bestOrder == -1):
			for i in range(gc.getNumBuildingClassInfos()):
				bldg = civInfo.getCivilizationBuildings(i)
				if self.canAdviseToConstruct(city, bldg):
					info = gc.getBuildingInfo(bldg)

					if type == "Culture":
						if city.findBaseYieldRateRank(YieldTypes.YIELD_COMMERCE) < 6:
							value = info.getCommerceModifier(CommerceTypes.COMMERCE_CULTURE) / float(info.getProductionCost())
							if value > bestData:
								bestOrder = bldg
								bestData = value
						else:
							value = info.getPowerValue() / float(info.getProductionCost())
							if value > bestData:
								bestOrder = bldg
								bestData = value
					elif type == "Military":
						value = info.getPowerValue() / float(info.getProductionCost())
						if value > bestData:
							bestOrder = bldg
							bestData = value
					elif type == "Nutty":
						value = math.sin(float(info.getProductionCost()) * city.getBaseYieldRate(YieldTypes.YIELD_COMMERCE)) + 1
						if value > bestData:
							bestOrder = bldg
							bestData = value
					elif type == "Religion":
						bestOrder = -1
					elif type == "Research":
						value = info.getCommerceModifier(CommerceTypes.COMMERCE_RESEARCH) / float(info.getProductionCost())
						if value > bestData:
							bestOrder = bldg
							bestData = value
					elif type == "Spaceship":
						if not city.isPower():
							if info.isPower():
								value = city.getBaseYieldRate(YieldTypes.YIELD_PRODUCTION) / float(info.getProductionCost())
								if value > bestData:
									bestOrder = bldg
									bestData = value
						
						if city.findBaseYieldRateRank(YieldTypes.YIELD_PRODUCTION) < 12:
							value = city.getBaseYieldRate(YieldTypes.YIELD_PRODUCTION) * 2 * info.getYieldModifier(YieldTypes.YIELD_PRODUCTION) / float(info.getProductionCost())
							if value > bestData:
								bestOrder = bldg
								bestData = value
						
						if city.findBaseYieldRateRank(YieldTypes.YIELD_COMMERCE) < player.getNumCities() / 2:
							value = city.getBaseYieldRate(YieldTypes.YIELD_COMMERCE) * info.getCommerceModifier(CommerceTypes.COMMERCE_RESEARCH) / float(info.getProductionCost())
							if value > bestData:
								bestOrder = bldg
								bestData = value
						else:
							bestOrder = -1

		# Second pass
		if(bestOrder == -1):
			for i in range(gc.getNumBuildingClassInfos()):
				bldg = civInfo.getCivilizationBuildings(i)
				if self.canAdviseToConstruct(city, bldg):
					info = gc.getBuildingInfo(bldg)

					if type == "Culture":
						if city.findBaseYieldRateRank(YieldTypes.YIELD_COMMERCE) < 6:
							value = info.getPowerValue() / float(info.getProductionCost())
							if value > bestData:
								bestOrder = bldg
								bestData = value
						else:
							bestOrder = -1  # In a cultural game, build units in the culturally weak cities
					elif type == "Military":
						if city.findBaseYieldRateRank(YieldTypes.YIELD_PRODUCTION) <= 3:
							value = -1 * info.getMilitaryProductionModifier() / float(info.getProductionCost())
							BugUtil.debug(info.getDescription() + ": " + str(value))
							if value > bestData:
								bestOrder = bldg
								bestData = value
						else:
							value = info.getYieldModifier(YieldTypes.YIELD_PRODUCTION) / float(info.getProductionCost())
							if value > bestData:
								bestOrder = bldg
								bestData = value
							if not city.isPower():
								if info.isPower():
									value = 1 / float(info.getProductionCost())
									if value > bestData:
										bestOrder = bldg
										bestData = value

					elif type == "Nutty":
						bestOrder = -1
					elif type == "Religion":
						bestOrder = -1
					elif type == "Research":
						value = info.getCommerceModifier(CommerceTypes.COMMERCE_GOLD) / float(info.getProductionCost())
						if value > bestData:
							bestOrder = bldg
							bestData = value
					elif type == "Spaceship":
						bestOrder = -1

		szReturn = u""
		if bestOrder != -1:
			szReturn = gc.getBuildingInfo(bestOrder).getDescription()

		if szReturn == city.getProductionName():
			szReturn = u""

		return szReturn

	def ColorCityValues (self, nValue, szKey):
		"""Colors city values which we might want to alert the user to."""

		# If the key is one we want to possibly color
		if (szKey in self.COLOR_SET):
			# If we don't have a plain integer
			if (re.search ("[-+]", nValue)):
				# Color it red and return it
				return localText.changeTextColor (nValue, gc.getInfoTypeForString("COLOR_RED"))
			# For each type of comparison
			for szCompareType, clDict in self.COLOR_DICT_DICT.iteritems():
				# Get the color we will use.
				color = self.COLOR_DICT[szCompareType]

				# If the dictionary has the key...
				if (clDict != None and clDict.has_key(szKey)):
					if (szKey in self.COMPARISON_REVERSED):
						# ...and the comparison is appropriate...
						if ((szCompareType == "PROBLEM" and int(nValue) >= clDict[szKey] or szCompareType == "NEUTRAL" and int(nValue) == clDict[szKey] or szCompareType == "GREAT" and int(nValue) <= clDict[szKey])):
							# ...color and return it
							return localText.changeTextColor (nValue, color)
					# ...and the comparison is appropriate...
					elif ((szCompareType == "PROBLEM" and int(nValue) <= clDict[szKey] or szCompareType == "NEUTRAL" and int(nValue) == clDict[szKey] or szCompareType == "GREAT" and int(nValue) >= clDict[szKey])):
						# ...color and return it
						return localText.changeTextColor (nValue, color)

		# Otherwise, just return the regular value
		return nValue

	def drawContents (self, page):
		""" Function to draw the contents of the cityList passed in. """

		screen = self.getScreen()
		iPlayer = PyPlayer(CyGame().getActivePlayer())
		cityList = iPlayer.getCityList()
		
		# Hide building icons
		for i in range(gc.getNumBuildingInfos()):
			szName = "BLDG_BTN_%d" % i
			screen.hide(szName)

		# Fill the pages drop down
		screen.addDropDownBoxGFC(self.PAGES_DD_NAME, self.X_SPECIAL, self.Y_SPECIAL, self.PAGES_DD_W, WidgetTypes.WIDGET_CDA_SELECT_PAGE, -1, -1, FontTypes.GAME_FONT)
		for i, p in enumerate(self.PAGES):
			screen.addPullDownString(self.PAGES_DD_NAME, p["name"], i, i, i == self.currentPageNum )

		if(self.customizing):

			# Build the page definition table
			screen.addTableControlGFC (self.CUSTOMIZE_PAGE, 4, self.nTableX, self.nTableY, self.nHalfTableWidth, self.nShortTableLength, True, False, 32, 32, TableStyles.TABLE_STYLE_STANDARD )
			screen.enableSelect(self.CUSTOMIZE_PAGE, True)
			screen.enableSort (self.CUSTOMIZE_PAGE)
			screen.setStyle(self.CUSTOMIZE_PAGE, "Table_StandardCiv_Style")

			screen.setTableColumnHeader (self.CUSTOMIZE_PAGE, 0, u"<font=2>POS</font>", 40 )
			screen.setTableColumnHeader (self.CUSTOMIZE_PAGE, 1, u"<font=2>NAME</font>", 160 )
			screen.setTableColumnHeader (self.CUSTOMIZE_PAGE, 2, u"<font=2>TITLE</font>", 160 )
			screen.setTableColumnHeader (self.CUSTOMIZE_PAGE, 3, u"<font=2>WIDTH</font>", 80 )

			columns = self.PAGES[self.currentPageNum]["columns"]
			for i, column in enumerate(columns):
				screen.appendTableRow (self.CUSTOMIZE_PAGE)
				screen.setTableInt(self.CUSTOMIZE_PAGE, 0, i, unicode(i+1), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
				screen.setTableText(self.CUSTOMIZE_PAGE, 1, i, unicode(column[0]), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				
				# Catch exceptions generated by missing columns
				try:
					screen.setTableText(self.CUSTOMIZE_PAGE, 2, i, self.HEADER_DICT[column[0]], "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				except KeyError:
					screen.setTableText(self.CUSTOMIZE_PAGE, 2, i, "", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				except TypeError:
					screen.setTableText(self.CUSTOMIZE_PAGE, 2, i, "", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				screen.setTableInt(self.CUSTOMIZE_PAGE, 3, i, unicode(column[1]), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)

			# Build the available columns table
			if(screen.getTableNumRows(self.COLUMNS_LIST_PAGE) != len(self.COLUMNS_LIST)):

				screen.addTableControlGFC (self.COLUMNS_LIST_PAGE, 4, self.nSecondHalfTableX, self.nTableY, self.nHalfTableWidth, self.nShortTableLength, True, False, 32, 32, TableStyles.TABLE_STYLE_STANDARD )
				screen.enableSelect(self.COLUMNS_LIST_PAGE, True)
				screen.enableSort (self.COLUMNS_LIST_PAGE)
				screen.setStyle(self.COLUMNS_LIST_PAGE, "Table_StandardCiv_Style")

				screen.setTableColumnHeader (self.COLUMNS_LIST_PAGE, 0, u"<font=2>ID</font>", 40 )
				screen.setTableColumnHeader (self.COLUMNS_LIST_PAGE, 1, u"<font=2>NAME</font>", 160 )
				screen.setTableColumnHeader (self.COLUMNS_LIST_PAGE, 2, u"<font=2>TITLE</font>", 160 )
				screen.setTableColumnHeader (self.COLUMNS_LIST_PAGE, 3, u"<font=2>WIDTH</font>", 80 )

				columns = self.COLUMNS_LIST
				for i, column in enumerate(columns):
					screen.appendTableRow (self.COLUMNS_LIST_PAGE)
					screen.setTableInt(self.COLUMNS_LIST_PAGE, 0, i, unicode(i), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
					screen.setTableText(self.COLUMNS_LIST_PAGE, 1, i, unicode(column[0]), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					try:
						screen.setTableText(self.COLUMNS_LIST_PAGE, 2, i, unicode(self.HEADER_DICT[column[0]]), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					except TypeError:
						screen.setTableText(self.COLUMNS_LIST_PAGE, 2, i, "", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					except UnicodeDecodeError:
						screen.setTableText(self.COLUMNS_LIST_PAGE, 2, i, "", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

					screen.setTableInt(self.COLUMNS_LIST_PAGE, 3, i, unicode(column[1]), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)

			# This is legacy code. I don't know if it's necessary.
			screen.moveToBack (self.BACKGROUND_ID)

			# Finally, display the customization controls
			self.showCustomizationControls()

			# And hide the regular controls and legends
			screen.hide(self.currentPage)
			self.hideSpecialists()
			self.hideCultureLegend()
			self.hideGPLegend()

		# If displaying the normal advisor screen (not the customization interface)
		else:

			dDict = self.columnDict

			# Bring down the curtain...
			screen.moveToFront( "Background" )

			# Build the table	
			if not self.PAGES[self.currentPageNum]["showSpecControls"] and \
				not self.PAGES[self.currentPageNum]["showCultureLegend"] and \
				not self.PAGES[self.currentPageNum]["showGPLegend"]:
				screen.addTableControlGFC (page, len (dDict) + 1, self.nTableX, self.nTableY, self.nTableWidth, self.nTableLength, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
			else:
				screen.addTableControlGFC (page, len (dDict) + 1, self.nTableX, self.nTableY, self.nTableWidth, self.nShortTableLength, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD )

			screen.enableSelect (page, True)
			screen.enableSort (page)
			screen.setStyle(page, "Table_StandardCiv_Style")

			cityRange = range(len(cityList))

			zoomArt = ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CITYSELECTION").getPath()

			# Add a blank header for the "zoom" column
			screen.setTableColumnHeader (page, 0, "", 30 )

			# Add blank rows to the table
			for i in cityRange:
				screen.appendTableRow (page)
				if (cityList[i].getName() in self.listSelectedCities):
					screen.selectRow( page, i, True )
#				if not self.PAGES[self.currentPageNum]["showSpecControls"]:
#					szWidgetName = "ZoomCity" + str(i)
#					screen.setImageButton( szWidgetName, zoomArt, 0, 0, 24, 24, WidgetTypes.WIDGET_ZOOM_CITY, cityList[i].getOwner(), cityList[i].getID() )
#					screen.attachControlToTableCell( szWidgetName, page, i, 0 )
				screen.setTableText( page, 0, i, "", zoomArt, WidgetTypes.WIDGET_ZOOM_CITY, cityList[i].getOwner(), cityList[i].getID(), CvUtil.FONT_LEFT_JUSTIFY)

			# Order the columns
			columns = []
			for key, value in self.columnDict.iteritems():
				columns.append((value, key))
			columns.sort()

			iBuildingButtonX = self.nTableX + 30
			iBuildingButtonY = self.nTableY
			civInfo = gc.getCivilizationInfo(gc.getActivePlayer().getCivilizationType())
			
			# Loop through the columns first. This is unintuitive, but faster.
			for value, key in columns:
				
				try:
					columnDef = self.COLUMNS_LIST[self.COLUMNS_INDEX[key]]
					type = columnDef[2]
					if (type == "bldg" or type == "bldgclass"):
						if (type == "bldg"):
							building = columnDef[7]
							buildingInfo = self.BUILDING_INFO_LIST[building]
							buildingClass = buildingInfo.getBuildingClassType()
							if (building != civInfo.getCivilizationBuildings(buildingClass)):
								# Skip column if building isn't available for this civ
								continue
						else:
							buildingClass = columnDef[7]
							building = civInfo.getCivilizationBuildings(buildingClass)
							buildingInfo = self.BUILDING_INFO_LIST[building]
						screen.setTableColumnHeader (page, value + 1, "", self.columnWidth[key])
						szName = "BLDG_BTN_%d" % building
						x = iBuildingButtonX + (self.columnWidth[key] - self.BUILDING_BUTTON_X_SIZE) / 2
						screen.setImageButton (szName, buildingInfo.getButton(), 
											   x, iBuildingButtonY, self.BUILDING_BUTTON_X_SIZE, self.BUILDING_BUTTON_Y_SIZE, 
											   WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, building, -1)
					else:
						screen.setTableColumnHeader (page, value + 1, "<font=2>" + self.HEADER_DICT[key] + "</font>", self.columnWidth[key] )

					iBuildingButtonX += self.columnWidth[key]

					# And the correct writing function.
					if (type == "text"):
						funcTableWrite = screen.setTableText
						justify = CvUtil.FONT_LEFT_JUSTIFY
					elif (type == "date"):
						funcTableWrite = screen.setTableDate
						justify = CvUtil.FONT_LEFT_JUSTIFY
					elif (type == "int"):
						funcTableWrite = screen.setTableInt
						justify = CvUtil.FONT_RIGHT_JUSTIFY
					elif (type == "bonus"):
						funcTableWrite = screen.setTableText
						justify = CvUtil.FONT_CENTER_JUSTIFY
					elif (type == "bldg" or type == "bldgclass"):
						funcTableWrite = screen.setTableText
						justify = CvUtil.FONT_CENTER_JUSTIFY
					else:
						return;

					colorFunc = self.ColorCityValues

					if(columnDef[3]):
						calcFunc = columnDef[3]
						# Loop through the cities
						for i in cityRange:
							szValue = colorFunc(unicode(calcFunc(cityList[i].city)), key)
							funcTableWrite (page, value + 1, i, szValue, "", WidgetTypes.WIDGET_GENERAL, -1, -1, justify)
						
					elif(columnDef[4]):
						calcFunc = columnDef[4]
						# Loop through the cities
						for i in cityRange:
							szValue = colorFunc(unicode(calcFunc(cityList[i].city, columnDef[5])), key)
							funcTableWrite (page, value + 1, i, szValue, "", WidgetTypes.WIDGET_GENERAL, -1, -1, justify)

					else:
						calcFunc = columnDef[6]
						
						# Loop through the cities
						for i in cityRange:
							szValue = colorFunc(unicode(calcFunc(cityList[i].city, key, columnDef[7])), key)
							funcTableWrite (page, value + 1, i, szValue, "", WidgetTypes.WIDGET_GENERAL, -1, -1, justify)

				except KeyError:
					continue
				except TypeError:
					continue

			# Finally, display the specialist controls,
			if self.PAGES[self.currentPageNum]["showSpecControls"]:
				self.showSpecialists()
			else:
				self.hideSpecialists()

			# and the legends,
			if self.PAGES[self.currentPageNum]["showCultureLegend"]:
				self.showCultureLegend()
			else:
				self.hideCultureLegend()

			if self.PAGES[self.currentPageNum]["showGPLegend"]:
				self.showGPLegend()
			else:
				self.hideGPLegend()

			# and hide the customization tools.
			self.hideCustomizationControls()

			# Raise the curtain and reveal our masterpiece
			screen.moveToBack (self.BACKGROUND_ID)

			# Now hand off to the C++ API
			self.updateAppropriateCitySelection (page, len( iPlayer.getCityList() ) )

	def HandleSpecialistPlus (self, inputClass):
		""" Handles when any Specialist Plus is pushed."""

		#CyInterface().setDirty(InterfaceDirtyBits.Domestic_Advisor_DIRTY_BIT, True)
		return 0

	def HandleSpecialistMinus (self, inputClass):
		""" Handles when any Specialist Minus is pushed."""

		CyInterface().setDirty(InterfaceDirtyBits.Domestic_Advisor_DIRTY_BIT, True)
		return 0

	def DomesticExit (self, inputClass):
		return 0

	def handleInput (self, inputClass):
		""" Handles the input for this screen..."""

		code = inputClass.getNotifyCode()

		if ( code == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED ):

			szWidget = inputClass.getFunctionName() + str(inputClass.getID())

			# I have no clue why + "0" is required here and not in the elif case. It's a mystery.
			if(szWidget == self.PAGES_DD_NAME + "0"):
				if(self.customizing):
					self.customizingClearSelection()
				self.switchPage(self.PAGES[inputClass.getData()]["name"])
				self.drawScreen(self.currentPage)
				return 1
				
			elif(szWidget == self.currentPage):
				screen = self.getScreen()
				if (inputClass.getMouseX() == 0):
					screen.hideScreen()
					
					CyInterface().selectCity(gc.getPlayer(inputClass.getData1()).getCity(inputClass.getData2()), true);
					
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
					popupInfo.setText(u"showDomesticAdvisor")
					popupInfo.addPopup(inputClass.getData1())
				else:
					city = self.getCurrentCity()
					if (city):
						CyInterface().lookAtCityOffset(city.getID())
					
					if self.PAGES[self.currentPageNum]["showSpecControls"]:
						self.showSpecialists()
					
					# And pass it back to the screen
					self.updateAppropriateCitySelection( self.currentPage, len( PyPlayer(CyGame().getActivePlayer()).getCityList() ) )
					
					return 1

			else:
				BugUtil.debug(szWidget)
				BugUtil.debug(self.currentPage)

		# Is the input from a mapped button?
		elif (code == NotifyCode.NOTIFY_CLICKED and self.DomesticScreenInputMap.has_key(inputClass.getFunctionName())):
			'Calls function mapped in CvSpecDomesticAdvisor'
			# only get from the map if it has the key

			# get bound function from map and call it (return whatever it returns.)
			return self.DomesticScreenInputMap.get(inputClass.getFunctionName())(inputClass)

		# Is the input from a Zoom City button?
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			if ( inputClass.getFunctionName() == "ZoomCity" ):
				screen = CyGInterfaceScreen( "DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR )
				screen.hideScreen()
				
				CyInterface().selectCity(gc.getPlayer(inputClass.getData1()).getCity(inputClass.getData2()), true);
				
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
				popupInfo.setText(u"showDomesticAdvisor")
				popupInfo.addPopup(inputClass.getData1())

# BUG - Colony Split - start

			elif (inputClass.getFunctionName() == self.SPLIT_NAME):
				screen = CyGInterfaceScreen( "DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR )
				screen.hideScreen()

# BUG - Colony Split - end

		# If none of the above, we didn't use the input."
		return 0
	
	def isFoodProduction (self, szProducing):
		""" We determine it's a food production, if it's a worker or settler."""
		return re.search ("Worker|Settler", szProducing)

	def updateScreen(self):
		""" Updates the screen."""

		self.drawContents()

		return

	def update(self, fDelta):
		""" Update the Advisor."""
		if (CyInterface().isDirty(InterfaceDirtyBits.Domestic_Advisor_DIRTY_BIT) == True):
			CyInterface().setDirty(InterfaceDirtyBits.Domestic_Advisor_DIRTY_BIT, False)
			
			self.drawContents(self.currentPage)

		return
			
	def switchPage(self, page):
		
		for i, p in enumerate(self.PAGES):
			if(p["name"] == page):
				self.currentPage = self.getPageID(p["name"])
				self.currentPageNum = i
				self.columnDict = { }
				self.columnWidth = { }
				for i, col in enumerate(p["columns"]):
					self.columnDict[col[0]] = i
					self.columnWidth[col[0]] = col[1]
				break

	def isPageActive(self, page):
		return self.currentPage == self.getPageID(page)

	def getPageID(self, page):
		for i, p in enumerate(self.PAGES):
			if(p["name"] == page):
				id = "CDA_PAGE_%d" % i
				return id
			
	def updateAppropriateCitySelection(self, page, nCities):
		screen = self.getScreen()
		screen.updateAppropriateCitySelection( page, nCities, 1 )

		self.listSelectedCities = []
		for i in range(nCities):
			if screen.isRowSelected(page, i):
				self.listSelectedCities.append(screen.getTableText(page, 1, i))
	
	def save(self, inputClass):
		name = BugPath.findIniFile("CustomDomAdv.txt", "CustomDomAdv")
		if (name):
			file = open(name, 'w')
	
			if(file != 0):
				pickle.dump({ "version" : self.PICKLED_VERSION, "pages" : self.PAGES }, file)
				file.close()

		return 1

	def ModifyPage(self, inputClass):

		screen = self.getScreen()

		if(self.customizing):
			self.customizing = False

			self.switchPage(self.PAGES[self.currentPageNum]["name"]) # Force a dictionary rebuild.

			self.drawScreen(self.currentPage)

		else:
			self.customizing = True

			self.drawScreen(self.currentPage)

		return 1

	def getSortedColumnSelection(self, screen):

		list = []
		
		for i in range(len(self.PAGES[self.currentPageNum]["columns"])):
			if screen.isRowSelected(self.CUSTOMIZE_PAGE, i):
				list.append(int(screen.getTableText(self.CUSTOMIZE_PAGE, 0, i)) - 1)

		list.sort()

		return list

	def getReverseSortedColumnSelection(self, screen):

		list = self.getSortedColumnSelection(screen)
		list.reverse()
		return list

	def AddCol(self, inputClass):

		self.customizingSaveSelection()
		screen = self.getScreen()

		for i in range(len(self.COLUMNS_LIST)):
			if screen.isRowSelected(self.COLUMNS_LIST_PAGE, i):
				col = self.COLUMNS_LIST[int(screen.getTableText(self.COLUMNS_LIST_PAGE, 0, i))]
				self.PAGES[self.currentPageNum]["columns"].append((col[0], col[1], col[2]))

		self.drawScreen(self.currentPage)
		self.customizingRestoreSelection()
		return 1

	def DelCol(self, inputClass):

		self.customizingSaveSelection()
		screen = self.getScreen()
		list = self.getReverseSortedColumnSelection(screen)

		for i in list:
			if(i == 0):
				continue
			else:
				del self.PAGES[self.currentPageNum]["columns"][i]

		self.drawScreen(self.currentPage)
		self.customizingRestoreSelection()
		return 1

	def MoveColUp(self, inputClass):

		self.customizingSaveSelection()

		screen = self.getScreen()

		list = self.getSortedColumnSelection(screen)

		top = 1

		for i in list:
			if(i == 0):
				continue
			elif i == top:
				top += 1
			else:
				col = self.PAGES[self.currentPageNum]["columns"][i]
				del self.PAGES[self.currentPageNum]["columns"][i]
				self.PAGES[self.currentPageNum]["columns"].insert(i - 1, col)

		self.drawScreen(self.currentPage)
		self.customizingRestoreSelection()

		return 1

	def MoveColDn(self, inputClass):

		self.customizingSaveSelection()

		screen = self.getScreen()

		list = self.getReverseSortedColumnSelection(screen)

		bottom = len(self.PAGES[self.currentPageNum]["columns"]) - 1

		for i in list:
			if(i == 0):
				continue
			elif i == bottom:
				bottom -= 1
			else:
				col = self.PAGES[self.currentPageNum]["columns"][i]
				del self.PAGES[self.currentPageNum]["columns"][i]
				self.PAGES[self.currentPageNum]["columns"].insert(i + 1, col)

		self.drawScreen(self.currentPage)
		self.customizingRestoreSelection()

		return 1

	def customizingClearSelection(self):
		self.customizingSelection = []

	def customizingSaveSelection(self):
		screen = self.getScreen()
		self.customizingSelection = []
		for i in range(len(self.PAGES[self.currentPageNum]["columns"])):
			if screen.isRowSelected(self.CUSTOMIZE_PAGE, i):
				self.customizingSelection.append(screen.getTableText(self.CUSTOMIZE_PAGE, 1, i))

	def customizingRestoreSelection(self):
		screen = self.getScreen()
		# Unselect before selecting, so that the selected rows are forced onscreen.
		for i in range(len(self.PAGES[self.currentPageNum]["columns"])):
			if not screen.getTableText(self.CUSTOMIZE_PAGE, 1, i) in self.customizingSelection:
				screen.selectRow(self.CUSTOMIZE_PAGE, i, False)
		for i in range(len(self.PAGES[self.currentPageNum]["columns"])):
			if screen.getTableText(self.CUSTOMIZE_PAGE, 1, i) in self.customizingSelection:
				screen.selectRow(self.CUSTOMIZE_PAGE, i, True)

	def shrinkCol(self, inputClass):

		self.customizingSaveSelection()
		screen = self.getScreen()
		columns = self.PAGES[self.currentPageNum]["columns"]

		list = self.getReverseSortedColumnSelection(screen)
		for i in list:
			col = columns[i]
			if(col[1] < 2):
				continue
			shrunken = (col[0], col[1] - 1, col[2])
			del columns[i]
			columns.insert(i, shrunken)

		self.drawScreen(self.currentPage)
		self.customizingRestoreSelection()

		return 1

	def widenCol(self, inputClass):

		self.customizingSaveSelection()
		screen = self.getScreen()
		columns = self.PAGES[self.currentPageNum]["columns"]

		list = self.getReverseSortedColumnSelection(screen)
		for i in list:
			col = columns[i]
			wider  = (col[0], col[1] + 1, col[2])
			del columns[i]
			columns.insert(i, wider)

		self.drawScreen(self.currentPage)
		self.customizingRestoreSelection()

		return 1
	
	def toggleShowSpecialistControls(self, inputClass):
		"""
		Toggle the page's 'show specialists' field.
		Also toggles the 'show culture/GP legend' fields (one button).
		"""
		page = self.PAGES[self.currentPageNum]
		page["showSpecControls"] = not page["showSpecControls"]
		page["showCultureLegend"] = not page["showCultureLegend"]
		page["showGPLegend"] = not page["showGPLegend"]
#		screen.setState(self.TOGGLE_SPECS_NAME, page["showSpecControls"])
		
		return 1
	
	def toggleShowCultureLegend(self, inputClass):
		"""
		Toggle the page's 'show culture legend' field.
		"""
		page = self.PAGES[self.currentPageNum]
		page["showCultureLegend"] = not page["showCultureLegend"]
		
		return 1
	
	def toggleShowGPLegend(self, inputClass):
		"""
		Toggle the page's 'show GP legend' field.
		"""
		page = self.PAGES[self.currentPageNum]
		page["showGPLegend"] = not page["showGPLegend"]
		
		return 1

	def addPage(self, inputClass):

		screen = self.getScreen()
		self.customizingClearSelection()
		name = "New Page %d" % (len(self.PAGES) + 1)
		self.PAGES.append(
			{
				"name" : name,
				"showSpecControls" : False,
				"showCultureLegend" : False,
				"showGPLegend" : False,
				"columns" : [
					("NAME", 95, "text")
				]
			}
			)
		self.switchPage(name)
		self.drawScreen(self.currentPage)

		return 1

	def delPage(self, inputClass):

		if(len(self.PAGES) > 1):
			screen = self.getScreen()
			self.customizingClearSelection()
			del self.PAGES[self.currentPageNum]
			self.switchPage(self.PAGES[0]["name"])
			self.drawScreen(self.currentPage)

		return 1

	def upPage(self, inputClass):
		
		if (self.currentPageNum < 1):
			# Cannot move first page up
			return 1
		curPage = self.currentPageNum
		prevPage = curPage - 1
		temp = self.PAGES[curPage]
		self.PAGES[curPage] = self.PAGES[prevPage]
		self.PAGES[prevPage] = temp
		if(self.customizing):
			self.customizingClearSelection()
		self.switchPage(temp["name"])
		self.drawScreen(self.currentPage)

		return 1

	def downPage(self, inputClass):
		
		if (self.currentPageNum + 1 >= len(self.PAGES)):
			# Cannot move last page down
			return 1
		curPage = self.currentPageNum
		nextPage = curPage + 1
		temp = self.PAGES[curPage]
		self.PAGES[curPage] = self.PAGES[nextPage]
		self.PAGES[nextPage] = temp
		if(self.customizing):
			self.customizingClearSelection()
		self.switchPage(temp["name"])
		self.drawScreen(self.currentPage)

		return 1

	def previousPage(self, inputClass):
		
		if (self.currentPageNum < 1):
			# Already on first page
			return 1
		if(self.customizing):
			self.customizingClearSelection()
		self.switchPage(self.PAGES[self.currentPageNum - 1]["name"])
		self.drawScreen(self.currentPage)

		return 1

	def nextPage(self, inputClass):
		
		if (self.currentPageNum + 1 >= len(self.PAGES)):
			# Already on last page
			return 1
		if(self.customizing):
			self.customizingClearSelection()
		self.switchPage(self.PAGES[self.currentPageNum + 1]["name"])
		self.drawScreen(self.currentPage)

		return 1


	def reloadPages(self, inputClass):
		
		self.currentPageNum = 0
		self.loadPages()
		self.switchPage(self.getPageID(self.PAGES[0]["name"]))
		self.drawScreen(self.currentPage)

		return 1

	def getBuildingKey(self, index):

		info = gc.getBuildingInfo(index)
		desc = info.getType()
		key = "_"
		key = key.join(desc.split())
		key = key.upper()
		return key

	def getBonusKey(self, index):

		info = gc.getBonusInfo(index)
		type = info.getType()
		key = "_"
		key = key.join(type.split())
		key = key.upper()
		return key

	def loadPages(self):

		self.PAGES = None
		name = BugPath.findIniFile("CustomDomAdv.txt", "CustomDomAdv")
		if (not name):
			name = BugPath.findIniFile("CustomDomAdv.txt")
		if (name):
			BugConfigTracker.add("CDA_Config", name)
			try:
				file = open(name, 'r')
				dict = pickle.load(file)
				version = dict["version"]
				self.PAGES = dict["pages"]
				file.close()
	
				if version == 0:
					for p in self.PAGES:
						newColumns = []
						for c in p["columns"]:
							for i in range(gc.getNumBuildingInfos()):
								info = gc.getBuildingInfo(i)
								desc = info.getDescription()
								key = "_"
								key = key.join(desc.split())
								key = "BUILDING_" + key.upper()
								if c[0] == key:
									c = (self.getBuildingKey(i), c[1], c[2])
									break
							for i in range(gc.getNumBonusInfos()):
								info = gc.getBonusInfo(i)
								desc = info.getDescription()
								key = "_"
								key = key.join(desc.split())
								key = "BONUS_" + key
								if c[0] == key:
									c = (self.getBonusKey(i), c[1], c[2])
									break
							newColumns.append(c)
						p["columns"] = newColumns
	
					# Updated from version 0 to version 1 format. Fall through to update version 1 format in the future
					version = 1						
	
				if(version != self.PICKLED_VERSION):
					self.PAGES = None
	
			except IOError:
				self.PAGES = None
			except IndexError:
				self.PAGES = None
			except ValueError:
				self.PAGES = None
			except TypeError:
				self.PAGES = None

		if(self.PAGES is None):
			if(self.isFlavorful):
				self.PAGES =	[
					{
						"name" : "Executive Summary", 
						"showSpecControls" : False,
						"showCultureLegend" : False,
						"showGPLegend" : False,
						"columns" :	[
							("NAME", 95, "text"),
							("AUTOMATION", 80, "text"),
							("FEATURES", 92, "text"),
							("POPULATION", 35, "int"),
							("GARRISON", 30, "int"),
							("HAPPY", 30, "int"),
							("HEALTH", 30, "int"),
							("GROWTH", 35, "int"),
							("FOOD", 35, "int"),
							("PRODUCTION", 38, "int"),
							("MAINTENANCE", 30, "int"),
							("BASE_COMMERCE", 38, "int"),
							("GOLD", 38, "int"),
							("RESEARCH", 38, "int"),
							("CULTURE_RATE", 38, "int"),
							("CULTURE", 53, "int"),
							("GREATPEOPLE_RATE", 38, "int"),
							("GREATPEOPLE", 45, "int"),
							("PRODUCING", 90, "text"),
							("PRODUCING_TURNS", 33, "int"),
						]
					},
					{
						"name" : "Specialization", 
						"showSpecControls" : True,
						"showCultureLegend" : True,
						"showGPLegend" : True,
						"columns" : [
							("NAME", 95, "text"),
							("FOUNDED", 80, "date"),
							("RELIGIONS", 90, "text"),
							("SPECIALISTS", 159, "text"),
							("HAPPY", 30, "int"),
							("GROWTH", 35, "int"),
							("FOOD", 35, "int"),
							("PRODUCTION", 38, "int"),
							("GOLD", 38, "int"),
							("RESEARCH", 38, "int"),
							("CULTURE_RATE", 38, "int"),
							("CULTURE", 53, "int"),
							("GREATPEOPLE_RATE", 38, "int"),
							("GREATPEOPLE", 45, "int"),
							("PRODUCING", 90, "text"),
							("PRODUCING_TURNS", 33, "int"),
						]
					},
					{
						"name" : "Top Cities - National", 
						"showSpecControls" : False,
						"showCultureLegend" : False,
						"showGPLegend" : False,
						"columns" :	[
							("NAME", 95, "text"),
							("POPULATION", 35, "int"),
							("FEATURES", 92, "text"),
							("RELIGIONS", 90, "text"),
							("GOLD", 38, "int"),
							("NRANK_GOLD",	38, "int"),
							("RESEARCH", 38, "int"),
							("NRANK_RESEARCH", 38, "int"),
							("CULTURE_RATE", 38, "int"),
							("NRANK_CULTURE", 38, "int"),
							("CULTURE", 53, "int"),
							("PRODUCING", 90, "text"),
							("PRODUCING_TURNS", 33, "int"),
						]
					},
					{
						"name" : "Top Cities - Global", 
						"showSpecControls" : False,
						"showCultureLegend" : False,
						"showGPLegend" : False,
						"columns" :	[
							("NAME", 95, "text"),
							("POPULATION", 35, "int"),
							("FEATURES", 92, "text"),
							("RELIGIONS", 90, "text"),
							("GOLD", 38, "int"),
							("GRANK_GOLD",	38, "int"),
							("RESEARCH", 38, "int"),
							("GRANK_RESEARCH", 38, "int"),
							("CULTURE_RATE", 38, "int"),
							("GRANK_CULTURE", 38, "int"),
							("CULTURE", 53, "int"),
							("PRODUCING", 90, "text"),
							("PRODUCING_TURNS", 33, "int"),
						]
					},
					{
						"name" : "Military Overview",
						"showSpecControls" : False,
						"showCultureLegend" : False,
						"showGPLegend" : False,
						"columns" : [
							("NAME", 95, "text"),
							("GARRISON", 30, "int"),
							("DEFENSE", 60, "int"),
							("THREATS", 60, "text"),
							("CONSCRIPT_UNIT", 90, "text"),
							(self.getBuildingKey(3), 70, "text"),
							(self.getBuildingKey(4), 70, "text"),
							(self.getBuildingKey(5), 70, "text"),
							(self.getBuildingKey(6), 70, "text"),
							(self.getBuildingKey(7), 70, "text"),
							("PRODUCING", 90, "text"),
							("PRODUCING_TURNS", 33, "int"),
						]
					}
					]
			else:
				self.PAGES =	[
					{
						"name" : "Default View", 
						"showSpecControls" : False,
						"showCultureLegend" : False,
						"showGPLegend" : False,
						"columns" :	[
							("NAME", 95, "text"),
							("AUTOMATION", 80, "text"),
							("FEATURES", 92, "text"),
							("POPULATION", 35, "int"),
							("GARRISON", 30, "int"),
							("HAPPY", 30, "int"),
							("HEALTH", 30, "int"),
							("GROWTH", 35, "int"),
							("FOOD", 35, "int"),
							("PRODUCTION", 38, "int"),
							("MAINTENANCE", 30, "int"),
							("BASE_COMMERCE", 38, "int"),
							("GOLD", 38, "int"),
							("RESEARCH", 38, "int"),
							("CULTURE_RATE", 38, "int"),
							("CULTURE", 53, "int"),
							("GREATPEOPLE_RATE", 38, "int"),
							("GREATPEOPLE", 45, "int"),
							("PRODUCING", 90, "text"),
							("PRODUCING_TURNS", 33, "int"),
						]
					},
					{
						"name" : "Specialists", 
						"showSpecControls" : True,
						"showCultureLegend" : True,
						"showGPLegend" : True,
						"columns" : [
							("NAME", 95, "text"),
							("FOUNDED", 80, "date"),
							("RELIGIONS", 90, "text"),
							("SPECIALISTS", 159, "text"),
							("HAPPY", 30, "int"),
							("GROWTH", 35, "int"),
							("FOOD", 35, "int"),
							("PRODUCTION", 38, "int"),
							("GOLD", 38, "int"),
							("RESEARCH", 38, "int"),
							("CULTURE_RATE", 38, "int"),
							("CULTURE", 53, "int"),
							("GREATPEOPLE_RATE", 38, "int"),
							("GREATPEOPLE", 45, "int"),
							("PRODUCING", 90, "text"),
							("PRODUCING_TURNS", 33, "int"),
						]
					},
					{
						"name" : "Growth", 
						"showSpecControls" : False,
						"showCultureLegend" : False,
						"showGPLegend" : False,
						"columns" : [
							("NAME", 95, "text"),
							("POPULATION", 35, "int"),
							("HAPPY", 30, "int"),
							("HEALTH", 30, "int"),
							("GROWTH", 35, "int"),
							("FOOD", 35, "int"),
							(self.getBuildingKey(8), 70, "text"),
							(self.getBuildingKey(12), 70, "text"),
							(self.getBuildingKey(9), 70, "text"),
							(self.getBuildingKey(31), 70, "text"),
							(self.getBuildingKey(10), 70, "text"),
							(self.getBuildingKey(11), 70, "text"),
							(self.getBuildingKey(13), 70, "text"),
							(self.getBuildingKey(33), 70, "text"),
							("PRODUCING", 90, "text"),
							("PRODUCING_TURNS", 33, "int"),
						]
					},
					{
						"name" : "Military",
						"showSpecControls" : False,
						"showCultureLegend" : False,
						"showGPLegend" : False,
						"columns" : [
							("NAME", 95, "text"),
							("GARRISON", 30, "int"),
							("DEFENSE", 60, "int"),
							("THREATS", 60, "text"),
							("CONSCRIPT_UNIT", 90, "text"),
							(self.getBuildingKey(3), 70, "text"),
							(self.getBuildingKey(4), 70, "text"),
							(self.getBuildingKey(5), 70, "text"),
							(self.getBuildingKey(6), 70, "text"),
							(self.getBuildingKey(7), 70, "text"),
							("PRODUCING", 90, "text"),
							("PRODUCING_TURNS", 33, "int"),
						]
					}
				]

		# Fix and retain configuration from previous versions, when possible.
		for p in self.PAGES:

			if not p.has_key("name"):
				p["name"] = "Unnamed"

			if not p.has_key("showSpecControls"):
				p["showSpecControls"] = False

			if not p.has_key("showCultureLegend"):
				p["showCultureLegend"] = False

			if not p.has_key("showGPLegend"):
				p["showGPLegend"] = False

			if not p.has_key("columns"):
				p["columns"] = [("NAME", 95, "text")]


	def renamePage(self, inputClass):

		eventManager = CvEventInterface.getEventManager()

		if not self.renameEventContext or self.renameEventContext is None:

			for i in range(5000, 6000):
				if not eventManager.Events.has_key(i):
					self.renameEventContext = i
					eventManager.Events[self.renameEventContext] = ('DomAdvRenamePage', self.renameApply, self.renameBegin)
					CvUtil.SilentEvents.append(self.renameEventContext)
					break

		CvEventInterface.beginEvent(self.renameEventContext)

	def renameBegin(self, argsList):

		popup = PyPopup.PyPopup(self.renameEventContext, EventContextTypes.EVENTCONTEXT_SELF)
		popup.setSize(400,175)
		popup.setUserData( (self.currentPageNum, 0) )
		popup.setHeaderString(u"Rename Domestic Advisor Page")
		popup.setBodyString("Enter a name for this domestic advisor page")
		popup.createEditBox( self.PAGES[self.currentPageNum]["name"], 0 )
		#popup.createRadioButtons(2, 1)
		#popup.setCheckBoxText(0, "Show specialist controls", 1)
		#popup.setCheckBoxText(1, "Hide specialist controls", 1)
		#popup.createRadioButtons(2, 2)
		#popup.setRadioButtonText(0, "Show culture legend", 2)
		#popup.setRadioButtonText(1, "Hide culture legend", 2)
		#popup.createRadioButtons(2, 3)
		#popup.setCheckBoxText(0, "Show great person legend", 3)
		#popup.setCheckBoxText(1, "Hide great person legend", 3)
		popup.launch()

		return 0

	def renameApply(self, playerID, userData, popupReturn):

		pageNum = userData[0]

		self.customizingSaveSelection()
		screen = self.getScreen()

		self.PAGES[pageNum]["name"] = popupReturn.getEditBoxString(0)
		#self.PAGES[pageNum]["showSpecControls"] = bool(popupReturn.getSelectedRadioButton(1))
		#self.PAGES[pageNum]["showCultureLegend"] = bool(popupReturn.getSelectedRadioButton(2))
		#self.PAGES[pageNum]["nshowGPLegendame"] = bool(popupReturn.getSelectedRadioButton(3))

		self.drawScreen(self.currentPage)
		self.customizingRestoreSelection()

		return 0
	
	def stripStr(self, s, out):
		while s.find(out) != -1:
			s = s[0:s.find(out)] + s[s.find(out) + 1:]

		return s
