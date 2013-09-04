## TraitUtil
##
## Utilities for dealing with Traits and TraitInfos.
##
## Notes
##   - Must be initialized externally by calling init()
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *

GENERIC_ICON = "*"
TRAIT_ICONS = {}

GENERIC_BUTTON = "Art/Interface/Buttons/TechTree/"
TRAIT_BUTTONS = {}

gc = CyGlobalContext()

def init():
	"Performs one-time initialization after the game starts up."
	game = gc.getGame()
	global GENERIC_ICON
	GENERIC_ICON = u"%c" % game.getSymbolID(FontSymbols.MAP_CHAR)
	
	addTrait("AGGRESSIVE", game.getSymbolID(FontSymbols.STRENGTH_CHAR), "Art/Interface/Buttons/Promotions/Combat1.dds")
	addTrait("CHARISMATIC", game.getSymbolID(FontSymbols.HAPPY_CHAR), "Art/Interface/Buttons/TechTree/MassMedia.dds")
	addTrait("CREATIVE", gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar(), "Art/Interface/Buttons/TechTree/Music.dds")
	addTrait("EXPANSIVE", game.getSymbolID(FontSymbols.HEALTHY_CHAR), "Art/Interface/Buttons/Actions/Heal.dds")
	addTrait("FINANCIAL", gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar(), "Art/Interface/Buttons/TechTree/Banking.dds")
	addTrait("IMPERIALIST", game.getSymbolID(FontSymbols.OCCUPATION_CHAR), "Art/Interface/Buttons/Actions/FoundCity.dds")
	addTrait("INDUSTRIOUS", gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar(), "Art/Interface/Buttons/TechTree/Industrialism.dds")
	addTrait("ORGANIZED", game.getSymbolID(FontSymbols.TRADE_CHAR), "Art/Interface/Buttons/Buildings/Courthouse.dds")
	addTrait("PHILOSOPHICAL", game.getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR), "Art/Interface/Buttons/TechTree/Philosophy.dds")
	addTrait("PROTECTIVE", game.getSymbolID(FontSymbols.DEFENSE_CHAR), "Art/Interface/Buttons/Promotions/CityGarrison1.dds")
	addTrait("SPIRITUAL", game.getSymbolID(FontSymbols.RELIGION_CHAR), "Art/Interface/Buttons/TechTree/Meditation.dds")

def addTrait(trait, icon, button):
	eTrait = gc.getInfoTypeForString("TRAIT_" + trait)
	if eTrait != -1:
		if icon is not None:
			TRAIT_ICONS[eTrait] = u"%c" % icon
		if button is not None:
			TRAIT_BUTTONS[eTrait] = button


def getIcon(eTrait):
	if eTrait in TRAIT_ICONS:
		return TRAIT_ICONS[eTrait]
	else:
		return GENERIC_ICON

def getButton(eTrait):
	if eTrait in TRAIT_BUTTONS:
		return TRAIT_BUTTONS[eTrait]
	else:
		return GENERIC_BUTTON
