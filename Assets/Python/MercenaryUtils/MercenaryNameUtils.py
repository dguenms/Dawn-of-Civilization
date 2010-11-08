#
# Mercenaries Mod
# By: The Lopez
# MercenaryNameUtils
# 

from CvPythonExtensions import *

import CvUtil
import sys
import PyHelpers
import math

import cPickle as pickle
import Consts as con #Rhye
import CvTranslator #Rhye

################# SD-UTILITY-PACK ###################
import SdToolKit
sdEcho         = SdToolKit.sdEcho
sdModInit      = SdToolKit.sdModInit
sdModLoad      = SdToolKit.sdModLoad
sdModSave      = SdToolKit.sdModSave
sdEntityInit   = SdToolKit.sdEntityInit
sdEntityExists = SdToolKit.sdEntityExists
sdGetVal       = SdToolKit.sdGetVal
sdSetVal       = SdToolKit.sdSetVal

gc = CyGlobalContext()	

lCivGroups = con.lCivGroups #Rhye


# The following two lists: mercenaryFirstNames and mercenaryLastNames was generated using a app called NameMage.
# NameMage
# Version 1.02
# www.mapmage.com

mercenaryAfricanNames = [
"TXT_KEY_CITY_NAME_NUBIAN",
"TXT_KEY_CITY_NAME_NUMIDIAN",
"TXT_KEY_CITY_NAME_BANTU",
"TXT_KEY_CITY_NAME_LIBYAN",
"TXT_KEY_CITY_NAME_KHOISAN",
"TXT_KEY_MERC_ZULU_ADJECTIVE"]

mercenaryAmericanNames = [
"TXT_KEY_CITY_NAME_CHEROKEE",
"TXT_KEY_CITY_NAME_ANASAZI",
"TXT_KEY_CITY_NAME_TEOIHUACAN",
"TXT_KEY_CITY_NAME_OLMEC",
"TXT_KEY_CITY_NAME_ZAPOTEC",
"TXT_KEY_CITY_NAME_CHINOOK",
"TXT_KEY_CITY_NAME_APACHE",
"TXT_KEY_CITY_NAME_CHEHALIS",
"TXT_KEY_CITY_NAME_ILLINOIS",
"TXT_KEY_CITY_NAME_NAVAJO",
"TXT_KEY_CITY_NAME_CARIB"]


mercenaryMiddleEasternNames = [
"TXT_KEY_CITY_NAME_SARMATIAN",
"TXT_KEY_CITY_NAME_SCYTHIAN",
"TXT_KEY_CITY_NAME_ASSYRIAN",
"TXT_KEY_CITY_NAME_HITTITE",
"TXT_KEY_CITY_NAME_HARAPPAN",
"TXT_KEY_CITY_NAME_PARTHIAN",
"TXT_KEY_CITY_NAME_HARAPPAN",
"TXT_KEY_CITY_NAME_BACTRIAN",
"TXT_KEY_CITY_NAME_CIRCASSIAN",
"TXT_KEY_CITY_NAME_CUMAN",
"TXT_KEY_CITY_NAME_HURRIAN",
"TXT_KEY_CITY_NAME_KASSITE",
"TXT_KEY_CITY_NAME_HUN",
"TXT_KEY_CITY_NAME_PHEONICIAN",
"TXT_KEY_CITY_NAME_PHRYGIAN"]


mercenaryAsianNames = [
"TXT_KEY_CITY_NAME_SHANGIAN",
"TXT_KEY_CITY_NAME_YAYOI",
"TXT_KEY_CITY_NAME_ZHOU",
"TXT_KEY_CITY_NAME_AINU",
"TXT_KEY_CITY_NAME_POLYNESIAN",
"TXT_KEY_CITY_NAME_ARYAN",
"TXT_KEY_CITY_NAME_AVAR",
"TXT_KEY_CITY_NAME_GHUZZ",
"TXT_KEY_CITY_NAME_HSUNGNU",
"TXT_KEY_CITY_NAME_KUSHANS",
"TXT_KEY_CITY_NAME_YUECHI",
"TXT_KEY_CITY_NAME_SAKAE",
"TXT_KEY_CITY_NAME_UZBEK",
"TXT_KEY_CITY_NAME_TARTAR",
"TXT_KEY_CITY_NAME_MAURYAN",
"TXT_KEY_MERC_KOREA_ADJECTIVE"]


mercenaryEuropeanNames = [
"TXT_KEY_CITY_NAME_SAXON",
"TXT_KEY_CITY_NAME_VANDAL",
"TXT_KEY_CITY_NAME_GOTH",
"TXT_KEY_CITY_NAME_ANGLE",
"TXT_KEY_CITY_NAME_MAGYAR",
"TXT_KEY_CITY_NAME_KHAZAK",
"TXT_KEY_CITY_NAME_BULGAR",
"TXT_KEY_CITY_NAME_ALEMANNI",
"TXT_KEY_CITY_NAME_BURGUNDIAN",
"TXT_KEY_CITY_NAME_GEPID",
"TXT_KEY_CITY_NAME_JUTE",
"TXT_KEY_CITY_NAME_ESTRUSCAN",
"TXT_KEY_CITY_NAME_THRACIAN",
"TXT_KEY_CITY_NAME_GAUL",
"TXT_KEY_CITY_NAME_MINOAN",
"TXT_KEY_CITY_NAME_CIMMERIAN",
"TXT_KEY_CITY_NAME_LIGURIAN",
"TXT_KEY_CITY_NAME_VISIGOTH",
"TXT_KEY_MERC_CELT_ADJECTIVE"]



# Returns a random unique name not found in the global mercenary pool
def getRandomMercenaryName(iCiv, iUnitType, bContractOut): #Rhye

	mercenaryName = ""
	
	# return any name if the global mercenary pool does not exist
	if(sdEntityExists("Mercenaries Mod","MercenaryData") == False):
		return mercenaryFirstNames[gc.getGame().getMapRand().get(len(mercenaryEuropeanNames), "Random Name")] + " " + gc.getUnitInfo(iUnitType).getDescription()	
	mercenaries = sdGetVal("Mercenaries Mod", "MercenaryData", "MercenaryNames")


	if (bContractOut):
                firstName = gc.getPlayer(iCiv).getCivilizationAdjective(0)
	else:
		if (iCiv in lCivGroups[4]):
			firstTempName = mercenaryAfricanNames[gc.getGame().getMapRand().get(len(mercenaryAfricanNames), "Random Name")]
		elif (iCiv in lCivGroups[5]):
			firstTempName = mercenaryAmericanNames[gc.getGame().getMapRand().get(len(mercenaryAmericanNames), "Random Name")]
		elif (iCiv in lCivGroups[2]):
			firstTempName = mercenaryMiddleEasternNames[gc.getGame().getMapRand().get(len(mercenaryMiddleEasternNames), "Random Name")]
		elif (iCiv in lCivGroups[1]):
			firstTempName = mercenaryAsianNames[gc.getGame().getMapRand().get(len(mercenaryAsianNames), "Random Name")]
		else:
			firstTempName = mercenaryEuropeanNames[gc.getGame().getMapRand().get(len(mercenaryEuropeanNames), "Random Name")]

		firstName = CyTranslator().getText(firstTempName, ())
		
	lastName = gc.getUnitInfo(iUnitType).getDescription()

	mercenaryName = firstName + " " + lastName
	iLanguage = CyGame().getCurrentLanguage()
	if (iLanguage == 1 or iLanguage == 3 or iLanguage == 4): #fra, ita, esp
                mercenaryName = lastName + " " + firstName

	# Keep trying to get a name until we get a unique one.
	while(mercenaries.has_key(mercenaryName)):
        	mercenaryName = mercenaryName + " "

	return mercenaryName
	
