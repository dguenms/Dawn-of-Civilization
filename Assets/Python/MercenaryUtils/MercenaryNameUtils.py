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
PyPlayer = PyHelpers.PyPlayer

lCivGroups = con.lCivGroups #Rhye


# The following two lists: mercenaryFirstNames and mercenaryLastNames was generated using a app called NameMage.
# NameMage
# Version 1.02
# www.mapmage.com

# categories
## North Africa ancient
## Europe ancient
## Middle East ancient
## East Asia ancient
## India ancient
## Mesoamerica
## North America
## South America
## Middle East medieval
## Europe medieval
## East Asia medieval
## India medieval
## South East Asia medieval
## Subsaharan Africa

iNumMercenaryNames = 96
(iNameNubian, iNameNumidian, iNameBerber, iNameHyksos, iNameSabean, iNameGaulish, iNameCeltic, iNameBriton, iNameIberian, iNameIllyrian, 
iNameDacian, iNameThracian, iNameEtruscan, iNameKimmerian, iNameGothic, iNameBurgundian, iNameVandal, iNameMinoan, iNameAssyrian, iNameSumerian, 
iNameJudean, iNameNabatean, iNameHittite, iNameHurrian, iNameKassite, iNameElamite, iNamePhilistine, iNameLydian, iNameParthian, iNameBactrian, 
iNameXiongnu, iNameYuezhi, iNameHan, iNameManchu, iNameAinu, iNameYamato, iNameTibetan, iNameAryan, iNameHarappan, iNameDravidian, 
iNameKushan, iNameBactrian, iNameTamil, iNameToltec, iNameZapotec, iNameOlmec, iNameApache, iNameCheyenne, iNameSioux, iNameIroquois, 
iNameChanChan, iNameGuarani, iNameNazcan, iNameCircassian, iNameArabian, iNameIraqi, iNameKhwarezmid, iNameKhazar, iNameOmani, iNameSeljuk, 
iNameIranian, iNameKurdish, iNameMoorish, iNameVarangian, iNameRus, iNameSwiss, iNameScots, iNameIrish, iNameSicilian, iNameNorman, 
iNameBohemian, iNameHungarian, iNamePolish, iNameLombard, iNameOccitan, iNameCatalan, iNameSlav, iNameBulgar, iNameTartar, iNameUzbek, 
iNameBurmese, iNameThai, iNameKhmer, iNameMalay, iNameJavanese, iNamePolynesian, iNameVietnamese, iNameRajput, iNamePasthun, iNameSikh,
iNameBengal, iNameZulu, iNameBantu, iNameSuaheli, iNameAshanti, iNameSonghai) = range(iNumMercenaryNames)

mercenaryNamesNorthAfricaAncient = [
iNameNubian,
iNameNumidian,
iNameBerber,
iNameHyksos,
iNameSabean,]

mercenaryNamesEuropeAncient = [
iNameGaulish,
iNameCeltic,
iNameBriton,
iNameIberian,
iNameIllyrian,
iNameDacian,
iNameThracian,
iNameEtruscan,
iNameKimmerian,
iNameGothic,
iNameBurgundian,
iNameVandal,
iNameMinoan,]

mercenaryNamesMiddleEastAncient = [
iNameAssyrian,
iNameSumerian,
iNameJudean,
iNameNabatean,
iNameHittite,
iNameHurrian,
iNameKassite,
iNameElamite,
iNamePhilistine,
iNameLydian,
iNameParthian,
iNameBactrian]

mercenaryNamesEastAsiaAncient = [
iNameXiongnu,
iNameYuezhi,
iNameHan,
iNameManchu,
iNameAinu,
iNameYamato,
iNameTibetan,]

mercenaryNamesIndiaAncient = [
iNameAryan,
iNameHarappan,
iNameDravidian,
iNameKushan,
iNameBactrian,
iNameTamil]

mercenaryNamesMesoamerica = [
iNameToltec,
iNameZapotec,
iNameOlmec,]

mercenaryNamesNorthAmerica = [
iNameApache,
iNameCheyenne,
iNameSioux,
iNameIroquois,]

mercenaryNamesSouthAmerica = [
iNameChanChan,
iNameGuarani,
iNameNazcan,]

mercenaryNamesMiddleEastMedieval = [
iNameCircassian,
iNameNubian,
iNameBerber,
iNameArabian,
iNameIraqi,
iNameKhwarezmid,
iNameKhazar,
iNameOmani,
iNameSeljuk,
iNameIranian,
iNameKurdish,
iNameMoorish]

mercenaryNamesEuropeMedieval = [
iNameVarangian,
iNameRus,
iNameSwiss,
iNameScots,
iNameIrish,
iNameSicilian,
iNameNorman,
iNameBohemian,
iNameHungarian,
iNamePolish,
iNameLombard,
iNameOccitan,
iNameCatalan,
iNameSlav,
iNameBulgar]

mercenaryNamesEastAsiaMedieval = [
iNameXiongnu,
iNameTartar,
iNameUzbek,
iNameHan,
iNameYamato,
iNameManchu,
iNameTibetan,]

mercenaryNamesSouthEastAsiaMedieval = [
iNameBurmese,
iNameThai,
iNameKhmer,
iNameMalay,
iNameJavanese,
iNamePolynesian,
iNameVietnamese,]

mercenaryNamesIndiaMedieval = [
iNameRajput,
iNamePasthun,
iNameSikh,
iNameTamil,
iNameBengal,]

mercenaryNamesSubsahara = [
iNameZulu,
iNameBantu,
iNameSuaheli,
iNameAshanti,
iNameSonghai]

mercenaryNames = {
iNameNubian 	:	"TXT_KEY_MERCENARY_NUBIAN",
iNameNumidian	:	"TXT_KEY_MERCENARY_NUMIDIAN",
iNameBerber	:	"TXT_KEY_MERCENARY_BERBER",
iNameHyksos	:	"TXT_KEY_MERCENARY_HYKSOS",
iNameSabean	:	"TXT_KEY_MERCENARY_SABEAN",
iNameGaulish	:	"TXT_KEY_MERCENARY_GAULISH",
iNameCeltic	:	"TXT_KEY_MERCENARY_CELTIC",
iNameBriton	:	"TXT_KEY_MERCENARY_BRITON",
iNameIberian	:	"TXT_KEY_MERCENARY_IBERIAN",
iNameIllyrian	:	"TXT_KEY_MERCENARY_ILLYRIAN",
iNameDacian	:	"TXT_KEY_MERCENARY_DACIAN",
iNameThracian	:	"TXT_KEY_MERCENARY_THRACIAN",
iNameEtruscan	:	"TXT_KEY_MERCENARY_ETRUSCAN",
iNameKimmerian	:	"TXT_KEY_MERCENARY_KIMMERIAN",
iNameGothic	:	"TXT_KEY_MERCENARY_GOTHIC",
iNameBurgundian	:	"TXT_KEY_MERCENARY_BURGUNDIAN",
iNameVandal	:	"TXT_KEY_MERCENARY_VANDAL",
iNameMinoan	:	"TXT_KEY_MERCENARY_MINOAN",
iNameAssyrian	:	"TXT_KEY_MERCENARY_ASSYRIAN",
iNameSumerian	:	"TXT_KEY_MERCENARY_SUMERIAN",
iNameJudean	:	"TXT_KEY_MERCENARY_JUDEAN",
iNameNabatean	:	"TXT_KEY_MERCENARY_NABATEAN",
iNameHittite	:	"TXT_KEY_MERCENARY_HITTITE",
iNameHurrian	:	"TXT_KEY_MERCENARY_HURRIAN",
iNameKassite	:	"TXT_KEY_MERCENARY_KASSITE",
iNameElamite	:	"TXT_KEY_MERCENARY_ELAMITE",
iNamePhilistine	:	"TXT_KEY_MERCENARY_PHILISTINE",
iNameLydian	:	"TXT_KEY_MERCENARY_LYDIAN",
iNameParthian	:	"TXT_KEY_MERCENARY_PARTHIAN",
iNameBactrian	:	"TXT_KEY_MERCENARY_BACTRIAN",
iNameXiongnu	:	"TXT_KEY_MERCENARY_XIONGNU",
iNameYuezhi	:	"TXT_KEY_MERCENARY_YUEZHI",
iNameHan	:	"TXT_KEY_MERCENARY_HAN",
iNameManchu	:	"TXT_KEY_MERCENARY_MANCHU",
iNameAinu	:	"TXT_KEY_MERCENARY_AINU",
iNameYamato	:	"TXT_KEY_MERCENARY_YAMATO",
iNameTibetan	:	"TXT_KEY_MERCENARY_TIBETAN",
iNameAryan	:	"TXT_KEY_MERCENARY_ARYAN",
iNameHarappan	:	"TXT_KEY_MERCENARY_HARAPPAN",
iNameDravidian	:	"TXT_KEY_MERCENARY_DRAVIDIAN",
iNameKushan	:	"TXT_KEY_MERCENARY_KUSHAN",
iNameBactrian	:	"TXT_KEY_MERCENARY_BACTRIAN",
iNameTamil	:	"TXT_KEY_MERCENARY_TAMIL",
iNameToltec	:	"TXT_KEY_MERCENARY_TOLTEC",
iNameZapotec	:	"TXT_KEY_MERCENARY_ZAPOTEC",
iNameOlmec	:	"TXT_KEY_MERCENARY_OLMEC",
iNameApache	:	"TXT_KEY_MERCENARY_APACHE",
iNameCheyenne	:	"TXT_KEY_MERCENARY_CHEYENNE",
iNameSioux	:	"TXT_KEY_MERCENARY_SIOUX",
iNameIroquois	:	"TXT_KEY_MERCENARY_IROQUOIS",
iNameChanChan	:	"TXT_KEY_MERCENARY_CHAN_CHAN",
iNameGuarani	:	"TXT_KEY_MERCENARY_GUARANI",
iNameNazcan	:	"TXT_KEY_MERCENARY_NAZCAN",
iNameCircassian	:	"TXT_KEY_MERCENARY_CIRCASSIAN",
iNameArabian	:	"TXT_KEY_MERCENARY_ARABIAN",
iNameIraqi	:	"TXT_KEY_MERCENARY_IRAQI",
iNameKhwarezmid	:	"TXT_KEY_MERCENARY_KHWAREZMID",
iNameKhazar	:	"TXT_KEY_MERCENARY_KHAZAR",
iNameOmani	:	"TXT_KEY_MERCENARY_OMANI",
iNameSeljuk	:	"TXT_KEY_MERCENARY_SELJUK",
iNameIranian	:	"TXT_KEY_MERCENARY_IRANIAN",
iNameKurdish	:	"TXT_KEY_MERCENARY_KURDISH",
iNameMoorish	:	"TXT_KEY_MERCENARY_MOORISH",
iNameVarangian	:	"TXT_KEY_MERCENARY_VARANGIAN",
iNameRus	:	"TXT_KEY_MERCENARY_RUS",
iNameSwiss	:	"TXT_KEY_MERCENARY_SWISS",
iNameScots	:	"TXT_KEY_MERCENARY_SCOTS",
iNameIrish	:	"TXT_KEY_MERCENARY_IRISH",
iNameSicilian	:	"TXT_KEY_MERCENARY_SICILIAN",
iNameNorman	:	"TXT_KEY_MERCENARY_NORMAN",
iNameBohemian	:	"TXT_KEY_MERCENARY_BOHEMIAN",
iNameHungarian	:	"TXT_KEY_MERCENARY_HUNGARIAN",
iNamePolish	:	"TXT_KEY_MERCENARY_POLISH",
iNameLombard	:	"TXT_KEY_MERCENARY_LOMBARD",
iNameOccitan	:	"TXT_KEY_MERCENARY_OCCITAN",
iNameCatalan	:	"TXT_KEY_MERCENARY_CATALAN",
iNameSlav	:	"TXT_KEY_MERCENARY_SLAVIC",
iNameBulgar	:	"TXT_KEY_MERCENARY_BULGAR",
iNameTartar	:	"TXT_KEY_MERCENARY_TARTAR",
iNameUzbek	:	"TXT_KEY_MERCENARY_UZBEK",
iNameBurmese	:	"TXT_KEY_MERCENARY_BURMESE",
iNameThai	:	"TXT_KEY_MERCENARY_THAI",
iNameKhmer	:	"TXT_KEY_MERCENARY_KHMER",
iNameMalay	:	"TXT_KEY_MERCENARY_MALAY",
iNameJavanese	:	"TXT_KEY_MERCENARY_JAVANESE",
iNamePolynesian	:	"TXT_KEY_MERCENARY_POLYNESIAN",
iNameVietnamese	:	"TXT_KEY_MERCENARY_VIETNAMESE",
iNameRajput	:	"TXT_KEY_MERCENARY_RAJPUT",
iNamePasthun	:	"TXT_KEY_MERCENARY_PASHTUN",
iNameSikh	:	"TXT_KEY_MERCENARY_SIKH",
iNameBengal	:	"TXT_KEY_MERCENARY_BENGAL",
iNameZulu	:	"TXT_KEY_MERCENARY_ZULU",
iNameBantu	:	"TXT_KEY_MERCENARY_BANTU",
iNameSuaheli	:	"TXT_KEY_MERCENARY_SUAHELI",
iNameAshanti	:	"TXT_KEY_MERCENARY_ASHANTI",
iNameSonghai	:	"TXT_KEY_MERCENARY_SONGHAI"}

mercenaryAfricanNames = [
"TXT_KEY_CITY_NAME_NUBIAN",	# Egypt, Ethiopia
"TXT_KEY_CITY_NAME_NUMIDIAN",	# Egypt, Maghreb
"TXT_KEY_CITY_NAME_BANTU",	# South Africa, West Africa
"TXT_KEY_CITY_NAME_LIBYAN",	# --
"TXT_KEY_CITY_NAME_KHOISAN",
"TXT_KEY_MERC_ZULU_ADJECTIVE"]	# South Africa

mercenaryAmericanNames = [
"TXT_KEY_CITY_NAME_CHEROKEE",	# USA
"TXT_KEY_CITY_NAME_ANASAZI",	
"TXT_KEY_CITY_NAME_TEOIHUACAN",	# Mesoamerica
"TXT_KEY_CITY_NAME_OLMEC",	# Mesoamerica
"TXT_KEY_CITY_NAME_ZAPOTEC",	# Mesoamerica
"TXT_KEY_CITY_NAME_CHINOOK",
"TXT_KEY_CITY_NAME_APACHE",	# USA
"TXT_KEY_CITY_NAME_CHEHALIS",
"TXT_KEY_CITY_NAME_ILLINOIS",
"TXT_KEY_CITY_NAME_NAVAJO",
"TXT_KEY_CITY_NAME_CARIB"]


mercenaryMiddleEasternNames = [
"TXT_KEY_CITY_NAME_SARMATIAN",	# Europe, Persia, Central Asia, Russia, <= classical
"TXT_KEY_CITY_NAME_SCYTHIAN",	# Europe, Persia, Central Asia, Russia <= classical
"TXT_KEY_CITY_NAME_ASSYRIAN",	# Mesopotamia, Anatolia <= classical
"TXT_KEY_CITY_NAME_HITTITE",	# Mesopotamia, Anatolia <= classical
"TXT_KEY_CITY_NAME_HARAPPAN",	# India, Deccan <= ancient
"TXT_KEY_CITY_NAME_PARTHIAN",	# Persia, Mesopotamia, Anatolia, <= classical
"TXT_KEY_CITY_NAME_HARAPPAN",
"TXT_KEY_CITY_NAME_BACTRIAN",	# Persia, India <= classical
"TXT_KEY_CITY_NAME_CIRCASSIAN",	# Anatolia, Mesopotamia, Arabia, Egypt <= medieval
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

def getUniqueUnitCiv(iUnitType):

	iUnitClassType = gc.getUnitInfo(iUnitType).getUnitClassType()
	for iPlayer in range(con.iNumPlayers):
		if iUnitType == gc.getCivilizationInfo(gc.getPlayer(iPlayer).getCivilizationType()).getCivilizationUnits(iUnitClassType):
			return iPlayer
			
	return -1



# Returns a random unique name not found in the global mercenary pool
def getRandomMercenaryName(iCiv, iUnitType, bContractOut): #Rhye

	mercenaryName = ""
	
	# return any name if the global mercenary pool does not exist
	if(sdEntityExists("Mercenaries Mod","MercenaryData") == False):
		return mercenaryFirstNames[gc.getGame().getMapRand().get(len(mercenaryEuropeanNames), "Random Name")] + " " + gc.getUnitInfo(iUnitType).getDescription()	
	mercenaries = sdGetVal("Mercenaries Mod", "MercenaryData", "MercenaryNames")
	
	iUniqueUnitCiv = getUniqueUnitCiv(iUnitType)


	if (bContractOut):
                firstName = gc.getPlayer(iCiv).getCivilizationAdjective(0)
	#elif iUniqueUnitCiv != -1:
	#	firstName = gc.getPlayer(iUniqueUnitCiv).getCivilizationAdjectiveKey()
	else:
		#if (iCiv in lCivGroups[4]):
		#	firstTempName = mercenaryAfricanNames[gc.getGame().getMapRand().get(len(mercenaryAfricanNames), "Random Name")]
		#elif (iCiv in lCivGroups[5]):
		#	firstTempName = mercenaryAmericanNames[gc.getGame().getMapRand().get(len(mercenaryAmericanNames), "Random Name")]
		#elif (iCiv in lCivGroups[2]):
		#	firstTempName = mercenaryMiddleEasternNames[gc.getGame().getMapRand().get(len(mercenaryMiddleEasternNames), "Random Name")]
		#elif (iCiv in lCivGroups[1]):
		#	firstTempName = mercenaryAsianNames[gc.getGame().getMapRand().get(len(mercenaryAsianNames), "Random Name")]
		#else:
		#	firstTempName = mercenaryEuropeanNames[gc.getGame().getMapRand().get(len(mercenaryEuropeanNames), "Random Name")]

		cityList = PyPlayer(iCiv).getCityList()
		regionList = []
		mercenaryPool = []
		
		for pCity in cityList:
			city = pCity.GetCy()
			iRegion = city.getRegionID()
			if iRegion not in regionList:
				regionList.append(iRegion)
				
		if len(cityList) == 0:
			regionList.append(gc.getMap().plot(con.tCapitals[0][iCiv][0], con.tCapitals[0][iCiv][1]).getRegionID())
				
		if set(regionList) & con.mercRegions[con.iArea_NorthAmerica]:
			mercenaryPool.extend(mercenaryNamesNorthAmerica)
		if set(regionList) & set([con.rMesoamerica, con.rCaribbean]):
			mercenaryPool.extend(mercenaryNamesMesoamerica)
		if set(regionList) & set([con.rBrazil, con.rArgentina, con.rColombia, con.rPeru]):
			mercenaryPool.extend(mercenaryNamesSouthAmerica)
		if set(regionList) & set([con.rEthiopia, con.rWestAfrica, con.rSouthAfrica]):
			mercenaryPool.extend(mercenaryNamesSubsahara)
			
		if gc.getPlayer(iCiv).getCurrentEra() <= con.iClassical:
			if set(regionList) & con.mercRegions[con.iArea_Europe]:
				mercenaryPool.extend(mercenaryNamesEuropeAncient)
			if set(regionList) & con.mercRegions[con.iArea_EastAsia]:
				mercenaryPool.extend(mercenaryNamesEastAsiaAncient)
			if set(regionList) & con.mercRegions[con.iArea_India]:
				mercenaryPool.extend(mercenaryNamesIndiaAncient)
			if set(regionList) & set([con.rEgypt, con.rMaghreb]):
				mercenaryPool.extend(mercenaryNamesNorthAfricaAncient)
			if set(regionList) & set([con.rAnatolia, con.rMesopotamia, con.rArabia, con.rPersia, con.rCentralAsia]):
				mercenaryPool.extend(mercenaryNamesMiddleEastAncient)
		else:
			if set(regionList) & con.mercRegions[con.iArea_Europe]:
				mercenaryPool.extend(mercenaryNamesEuropeMedieval)
			if set(regionList) & set([con.rChina, con.rKorea, con.rManchuria, con.rJapan, con.rTibet]):
				mercenaryPool.extend(mercenaryNamesEastAsiaMedieval)
			if set(regionList) & con.mercRegions[con.iArea_India]:
				mercenaryPool.extend(mercenaryNamesIndiaMedieval)
			if set(regionList) & con.mercRegions[con.iArea_MiddleEast]:
				mercenaryPool.extend(mercenaryNamesMiddleEastMedieval)
			if set(regionList) & set([con.rIndonesia, con.rIndochina]):
				mercenaryPool.extend(mercenaryNamesSouthEastAsiaMedieval)
		
		if len(mercenaryPool) > 0:
			iNameID = mercenaryPool[gc.getGame().getMapRand().get(len(mercenaryPool), 'random mercenary name')]
			firstTempName = mercenaryNames[iNameID]
		else:
			firstTempName = ""
		
		
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
	
