# Dynamic Civs - edead

from CvPythonExtensions import *
import CvUtil
import PyHelpers
from Consts import *
import Victory as vic
from StoredData import sd
import RFCUtils
import CityNameManager as cnm
utils = RFCUtils.RFCUtils()
import time

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo
localText = CyTranslator()

tBrazilTL = (32, 14)
tBrazilBR = (43, 30)
tNCAmericaTL = (3, 33)
tNCAmericaBR = (37, 63)

### Dictionaries with text keys

dDefaultNames = {
	iEgypt : "TXT_KEY_CIV_EGYPT_DEFAULT",
	iIndia : "TXT_KEY_CIV_INDIA_DEFAULT",
	iChina : "TXT_KEY_CIV_CHINA_DEFAULT",
	iBabylonia : "TXT_KEY_CIV_BABYLONIA_DEFAULT",
	iHarappa : "TXT_KEY_CIV_HARAPPA_DEFAULT",
	iGreece : "TXT_KEY_CIV_GREECE_DEFAULT",
	iPersia : "TXT_KEY_CIV_PERSIA_DEFAULT",
	iCarthage : "TXT_KEY_CIV_PHOENICIA_DEFAULT",
	iPolynesia : "TXT_KEY_CIV_POLYNESIA_DEFAULT",
	iRome : "TXT_KEY_CIV_ROME_DEFAULT",
	iJapan : "TXT_KEY_CIV_JAPAN_DEFAULT",
	iTamils : "TXT_KEY_CIV_TAMILS_DEFAULT",
	iEthiopia : "TXT_KEY_CIV_ETHIOPIA_DEFAULT",
	iKorea : "TXT_KEY_CIV_KOREA_DEFAULT",
	iMaya : "TXT_KEY_CIV_MAYA_DEFAULT",
	iByzantium : "TXT_KEY_CIV_BYZANTIUM_DEFAULT",
	iVikings : "TXT_KEY_CIV_VIKINGS_DEFAULT",
	iArabia : "TXT_KEY_CIV_ARABIA_DEFAULT",
	iTibet : "TXT_KEY_CIV_TIBET_DEFAULT",
	iKhmer : "TXT_KEY_CIV_KHMER_DEFAULT",
	iIndonesia : "TXT_KEY_CIV_INDONESIA_DEFAULT",
	iMoors : "TXT_KEY_CIV_MOORS_DEFAULT",
	iSpain : "TXT_KEY_CIV_SPAIN_DEFAULT",
	iFrance : "TXT_KEY_CIV_FRANCE_DEFAULT",
	iEngland : "TXT_KEY_CIV_ENGLAND_DEFAULT",
	iHolyRome : "TXT_KEY_CIV_HOLY_ROME_DEFAULT",
	iRussia : "TXT_KEY_CIV_RUSSIA_DEFAULT",
	iNetherlands : "TXT_KEY_CIV_NETHERLANDS_DEFAULT",
	iMali : "TXT_KEY_CIV_MALI_DEFAULT",
	iPoland : "TXT_KEY_CIV_POLAND_DEFAULT",
	iPortugal : "TXT_KEY_CIV_PORTUGAL_DEFAULT",
	iInca : "TXT_KEY_CIV_INCA_DEFAULT",
	iItaly : "TXT_KEY_CIV_ITALY_DEFAULT",
	iMongolia : "TXT_KEY_CIV_MONGOLIA_DEFAULT",
	iAztecs : "TXT_KEY_CIV_AZTECS_DEFAULT",
	iMughals : "TXT_KEY_CIV_MUGHALS_DEFAULT",
	iTurkey : "TXT_KEY_CIV_TURKEY_DEFAULT",
	iThailand : "TXT_KEY_CIV_THAILAND_DEFAULT",
	iCongo : "TXT_KEY_CIV_CONGO_DEFAULT",
	iGermany : "TXT_KEY_CIV_GERMANY_DEFAULT",
	iAmerica : "TXT_KEY_CIV_AMERICA_DEFAULT",
	iArgentina : "TXT_KEY_CIV_ARGENTINA_DEFAULT",
	iBrazil : "TXT_KEY_CIV_BRAZIL_DEFAULT",
	iCanada : "TXT_KEY_CIV_CANADA_DEFAULT",
}

### Utility methods for standard player names

def text(sTextKey, tInput=()):
	return localText.getText(sTextKey, tInput)
	
def name(iPlayer, sTextKey="%s1"):
	return text(sTextKey, (short(iPlayer), adjective(iPlayer)))

def short(iPlayer):
	return gc.getPlayer(iPlayer).getCivilizationShortDescription()
	
def long(iPlayer):
	return gc.getPlayer(iPlayer).getCivilizationDescription()

def adjective(iPlayer):
	return gc.getPlayer(iPlayer).getCivilizationAdjective()
	
### Naming methods

def defaultName(iPlayer):
	if iPlayer in dDefaultNames: return name(dDefaultNames[iPlayer], iPlayer)

	return long(iPlayer)
	
def peoplesName(iPlayer):
	if iPlayer in dPeopleNames: return 

class DynamicCivs:


        def __init__(self):

                
		
		self.peopleNames = {
                        iEgypt : "TXT_KEY_CIV_EGYPT_DESC_PEOPLES",
                        iIndia : "TXT_KEY_CIV_INDIA_DESC_PEOPLES",
                        iChina : "TXT_KEY_CIV_CHINA_DESC_PEOPLES",
                        iBabylonia : "TXT_KEY_CIV_BABYLONIA_DESC_PEOPLES",
			iHarappa : "TXT_KEY_CIV_HARAPPA_DESC_PEOPLES",
                        iGreece : "TXT_KEY_CIV_GREECE_DESC_PEOPLES",
                        iPersia : "TXT_KEY_CIV_PERSIA_DESC_PEOPLES",
                        iCarthage : "TXT_KEY_CIV_PHOENICIA_DESC_PEOPLES",
			iPolynesia : "TXT_KEY_CIV_POLYNESIA_DESC_PEOPLES",
                        iRome : "TXT_KEY_CIV_ROME_DESC_PEOPLES",
                        iJapan : "TXT_KEY_CIV_JAPAN_DESC_PEOPLES",
			iTamils : "TXT_KEY_CIV_TAMILS_DESC_PEOPLES",
                        iEthiopia : "TXT_KEY_CIV_ETHIOPIA_DESC_PEOPLES",
                        iKorea : "TXT_KEY_CIV_KOREA_DESC_PEOPLES",
                        iMaya : "TXT_KEY_CIV_MAYA_DESC_PEOPLES",
                        iByzantium : "TXT_KEY_CIV_BYZANTIUM_DESC_PEOPLES",
                        iVikings : "TXT_KEY_CIV_VIKINGS_DESC_PEOPLES",
                        iArabia : "TXT_KEY_CIV_ARABIA_DESC_PEOPLES",
			iTibet : "TXT_KEY_CIV_TIBET_DESC_PEOPLES",
                        iKhmer : "TXT_KEY_CIV_KHMER_DESC_PEOPLES",
                        iIndonesia : "TXT_KEY_CIV_INDONESIA_DESC_PEOPLES",
			iMoors : "TXT_KEY_CIV_MOORS_DESC_PEOPLES",
                        iSpain : "TXT_KEY_CIV_SPAIN_DESC_PEOPLES",
                        iFrance : "TXT_KEY_CIV_FRANCE_DESC_PEOPLES",
                        iEngland : "TXT_KEY_CIV_ENGLAND_DESC_PEOPLES",
                        iHolyRome : "TXT_KEY_CIV_HOLY_ROME_DESC_PEOPLES",
                        iRussia : "TXT_KEY_CIV_RUSSIA_DESC_PEOPLES",
                        iNetherlands : "TXT_KEY_CIV_NETHERLANDS_DESC_PEOPLES",
                        iMali : "TXT_KEY_CIV_MALI_DESC_PEOPLES",
			iPoland : "TXT_KEY_CIV_POLAND_DESC_PEOPLES",
                        iPortugal : "TXT_KEY_CIV_PORTUGAL_DESC_PEOPLES",
                        iInca : "TXT_KEY_CIV_INCA_DESC_PEOPLES",
			iItaly : "TXT_KEY_CIV_ITALY_DESC_PEOPLES",
                        iMongolia : "TXT_KEY_CIV_MONGOLIA_DESC_PEOPLES",
                        iAztecs : "TXT_KEY_CIV_AZTECS_DESC_PEOPLES",
			iMughals : "TXT_KEY_CIV_MUGHALS_DESC_PEOPLES",
                        iTurkey : "TXT_KEY_CIV_TURKEY_DESC_PEOPLES",
			iThailand : "TXT_KEY_CIV_THAILAND_DESC_PEOPLES",
			iCongo : "TXT_KEY_CIV_CONGO_DESC_PEOPLES",
			iGermany : "TXT_KEY_CIV_GERMANY_DESC_PEOPLES",
                        iAmerica : "TXT_KEY_CIV_AMERICA_DESC_PEOPLES",
			iArgentina : "TXT_KEY_CIV_ARGENTINA_DESC_PEOPLES",
			iBrazil : "TXT_KEY_CIV_BRAZIL_DESC_PEOPLES",
			iCanada : "TXT_KEY_CIV_CANADA_DESC_PEOPLES",
                }
				
		self.specificVassalNames = {
			iEgypt : {
				iCarthage : "TXT_KEY_CIV_PHOENICIA_EGYPTIAN_VASSAL",	# Retenu
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_EGYPTIAN_VASSAL"},	# Punt
			#iIndia - none so far
			iChina : {
				iEgypt : "TXT_KEY_CIV_EGYPT_CHINESE_VASSAL",
				iIndia : "TXT_KEY_CIV_INDIA_CHINESE_VASSAL",
				iBabylonia : "TXT_KEY_CIV_BABYLONIA_CHINESE_VASSAL",
				iGreece : "TXT_KEY_CIV_GREECE_CHINESE_VASSAL",
				iPersia : "TXT_KEY_CIV_PERSIA_CHINESE_VASSAL",
				iCarthage : "TXT_KEY_CIV_CARTHAGE_CHINESE_VASSAL",
				iRome : "TXT_KEY_CIV_ROME_CHINESE_VASSAL",
				iJapan : "TXT_KEY_CIV_JAPAN_CHINESE_VASSAL",
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_CHINESE_VASSAL",
				iKorea : "TXT_KEY_CIV_KOREA_CHINESE_VASSAL",
				iMaya : "TXT_KEY_CIV_MAYA_CHINESE_VASSAL",
				iByzantium : "TXT_KEY_CIV_BYZANTIUM_CHINESE_VASSAL",
				iVikings : "TXT_KEY_CIV_VIKINGS_CHINESE_VASSAL",
				iArabia : "TXT_KEY_CIV_ARABIA_CHINESE_VASSAL",
				iTibet : "TXT_KEY_CIV_TIBET_CHINESE_VASSAL",
				iKhmer : "TXT_KEY_CIV_KHMER_CHINESE_VASSAL",
				iIndonesia : "TXT_KEY_CIV_INDONESIA_CHINESE_VASSAL",
				iSpain : "TXT_KEY_CIV_SPAIN_CHINESE_VASSAL",
				iFrance : "TXT_KEY_CIV_FRANCE_CHINESE_VASSAL",
				iEngland : "TXT_KEY_CIV_ENGLAND_CHINESE_VASSAL",
				iHolyRome : "TXT_KEY_CIV_GERMANY_CHINESE_VASSAL",
				iRussia : "TXT_KEY_CIV_RUSSIA_CHINESE_VASSAL",
				iNetherlands : "TXT_KEY_CIV_NETHERLANDS_CHINESE_VASSAL",
				iMali : "TXT_KEY_CIV_MALI_CHINESE_VASSAL",
				iPortugal : "TXT_KEY_CIV_PORTUGAL_CHINESE_VASSAL",
				iInca : "TXT_KEY_CIV_INCA_CHINESE_VASSAL",
				iItaly : "TXT_KEY_CIV_ROME_CHINESE_VASSAL",
				iMongolia : "TXT_KEY_CIV_MONGOLIA_CHINESE_VASSAL",
				iAztecs : "TXT_KEY_CIV_AZTECS_CHINESE_VASSAL",
				iTurkey : "TXT_KEY_CIV_TURKEY_CHINESE_VASSAL",
				iMughals : "TXT_KEY_CIV_MUGHALS_CHINESE_VASSAL",
				iThailand : "TXT_KEY_CIV_THAILAND_CHINESE_VASSAL",
				iGermany : "TXT_KEY_CIV_GERMANY_CHINESE_VASSAL",
				iAmerica : "TXT_KEY_CIV_AMERICA_CHINESE_VASSAL"},
			iBabylonia : {
				iPhoenicia : "TXT_KEY_CIV_PHOENICIA_BABYLONIAN_VASSAL"},	# Babylonian Phoenicia
			iGreece : {
				iIndia : "TXT_KEY_CIV_INDIA_GREEK_VASSAL",	# Greco-Bactrians
				iEgypt : "TXT_KEY_CIV_EGYPT_GREEK_VASSAL",	#  Ptolemaic Egypt
				iPersia : "TXT_KEY_CIV_PERSIA_GREEK_VASSAL"},	# Seleucid Babylonia
			iPersia : {
				iEgypt : "TXT_KEY_CIV_EGYPT_PERSIAN_VASSAL",
				iIndia : "TXT_KEY_CIV_INDIA_PERSIAN_VASSAL",
				iBabylonia : "TXT_KEY_CIV_BABYLONIA_PERSIAN_VASSAL",
				iGreece : "TXT_KEY_CIV_GREECE_PERSIAN_VASSAL",
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_PERSIAN_VASSAL",
				iByzantium : "TXT_KEY_CIV_BYZANTIUM_PERSIAN_VASSAL",
				iVikings : "TXT_KEY_CIV_VIKINGS_PERSIAN_VASSAL",
				iArabia : "TXT_KEY_CIV_ARABIA_PERSIAN_VASSAL",
				iKhmer : "TXT_KEY_CIV_KHMER_PERSIAN_VASSAL",
				iIndonesia : "TXT_KEY_CIV_INDONESIA_PERSIAN_VASSAL",
				iNetherlands : "TXT_KEY_CIV_NETHERLANDS_PERSIAN_VASSAL",
				iMongolia : "TXT_KEY_CIV_MONGOLIA_PERSIAN_VASSAL",
				iAztecs : "TXT_KEY_CIV_AZTECS_PERSIAN_VASSAL",
				iTurkey : "TXT_KEY_CIV_TURKEY_PERSIAN_VASSAL"},
			#iCarthage - none so far
			#iPolynesia - none so far
			iRome : {
				iEgypt : "TXT_KEY_CIV_EGYPT_ROMAN_VASSAL",
				iChina : "TXT_KEY_CIV_CHINA_ROMAN_VASSAL",
				iBabylonia : "TXT_KEY_CIV_BABYLONIA_ROMAN_VASSAL",
				iGreece : "TXT_KEY_CIV_GREECE_ROMAN_VASSAL",
				iPersia : "TXT_KEY_CIV_PERSIA_ROMAN_VASSAL",
				iCarthage : "TXT_KEY_CIV_PHOENICIA_ROMAN_VASSAL",
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_ROMAN_VASSAL",
				iByzantium : "TXT_KEY_CIV_BYZANTIUM_ROMAN_VASSAL",
				iVikings : "TXT_KEY_CIV_VIKINGS_ROMAN_VASSAL",
				iKhmer : "TXT_KEY_CIV_KHMER_ROMAN_VASSAL",
				iSpain : "TXT_KEY_CIV_SPAIN_ROMAN_VASSAL",
				iFrance : "TXT_KEY_CIV_FRANCE_ROMAN_VASSAL",
				iEngland : "TXT_KEY_CIV_ENGLAND_ROMAN_VASSAL",
				iHolyRome : "TXT_KEY_CIV_HOLY_ROME_ROMAN_VASSAL",
				iRussia : "TXT_KEY_CIV_RUSSIA_ROMAN_VASSAL",
				iNetherlands : "TXT_KEY_CIV_NETHERLANDS_ROMAN_VASSAL",
				iMali : "TXT_KEY_CIV_MALI_ROMAN_VASSAL",
				iPortugal : "TXT_KEY_CIV_PORTUGAL_ROMAN_VASSAL",
				iMongolia : "TXT_KEY_CIV_MONGOLIA_ROMAN_VASSAL",
				iAztecs : "TXT_KEY_CIV_AZTECS_ROMAN_VASSAL",
				iTurkey : "TXT_KEY_CIV_TURKEY_ROMAN_VASSAL",
				iGermany : "TXT_KEY_CIV_GERMANY_ROMAN_VASSAL",
				iThailand : "TXT_KEY_CIV_THAILAND_ROMAN_VASSAL",},
			iJapan : {
				iChina : "TXT_KEY_CIV_CHINA_JAPANESE_VASSAL",
				iKorea : "TXT_KEY_CIV_KOREA_JAPANESE_VASSAL",
				iKhmer : "TXT_KEY_CIV_KHMER_JAPANESE_VASSAL",
				iMongolia : "TXT_KEY_CIV_MONGOLIA_JAPANESE_VASSAL",
				iAztecs : "TXT_KEY_CIV_AZTECS_JAPANESE_VASSAL",},
			#iTamils - none so far
			#iEthiopia - none so far
			#iKorea - none so far
			#iMaya - none so far
			iByzantium : {
				iEgypt : "TXT_KEY_CIV_EGYPT_BYZANTINE_VASSAL",
				iBabylonia : "TXT_KEY_CIV_BABYLONIA_BYZANTINE_VASSAL",
				iGreece : "TXT_KEY_CIV_GREECE_BYZANTINE_VASSAL",
				iCarthage : "TXT_KEY_CIV_PHOENICIA_BYZANTINE_VASSAL",
				iPersia : "TXT_KEY_CIV_PERSIA_BYZANTINE_VASSAL",
				iRome : "TXT_KEY_CIV_ROME_BYZANTINE_VASSAL",
				iSpain : "TXT_KEY_CIV_SPAIN_BYZANTINE_VASSAL"},
			iVikings : {
				iEngland : "TXT_KEY_CIV_ENGLAND_VIKING_VASSAL",
				iRussia : "TXT_KEY_CIV_RUSSIA_VIKING_VASSAL"},
			iArabia : {
				iEgypt : "TXT_KEY_CIV_EGYPT_ARABIAN_VASSAL",
				iBabylonia : "TXT_KEY_CIV_BABYLONIA_ARABIAN_VASSAL",
				iPersia : "TXT_KEY_CIV_PERSIA_ARABIAN_VASSAL",
				iCarthage : "TXT_KEY_CIV_PHOENICIA_ARABIAN_VASSAL",
				iRome : "TXT_KEY_CIV_ROME_ARABIAN_VASSAL",
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_ARABIAN_VASSAL",
				iByzantium : "TXT_KEY_CIV_BYZANTIUM_ARABIAN_VASSAL",
				iVikings : "TXT_KEY_CIV_VIKINGS_ARABIAN_VASSAL",
				iKhmer : "TXT_KEY_CIV_KHMER_ARABIAN_VASSAL",
				iMoors : "TXT_KEY_CIV_MOORS_ARABIAN_VASSAL",
				iSpain : "TXT_KEY_CIV_SPAIN_ARABIAN_VASSAL",
				iNetherlands : "TXT_KEY_CIV_NETHERLANDS_ARABIAN_VASSAL",
				iAztecs : "TXT_KEY_CIV_AZTECS_ARABIAN_VASSAL",
				iTurkey : "TXT_KEY_CIV_TURKEY_ARABIAN_VASSAL",
				iMughals : "TXT_KEY_CIV_MUGHALS_ARABIAN_VASSAL",
				iThailand : "TXT_KEY_CIV_THAILAND_ARABIAN_VASSAL",},
			#iTibet - none so far
			#iKhmer - none so far
			#iIndonesia - none so far
			iMoors : {
				iEgypt : "TXT_KEY_CIV_EGYPT_ARABIAN_VASSAL",
				iBabylonia : "TXT_KEY_CIV_BABYLONIA_ARABIAN_VASSAL",
				iPersia : "TXT_KEY_CIV_PERSIA_ARABIAN_VASSAL",
				iCarthage : "TXT_KEY_CIV_PHOENICIA_ARABIAN_VASSAL",
				iRome : "TXT_KEY_CIV_ROME_ARABIAN_VASSAL",
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_ARABIAN_VASSAL",
				iByzantium : "TXT_KEY_CIV_BYZANTIUM_ARABIAN_VASSAL",
				iVikings : "TXT_KEY_CIV_VIKINGS_ARABIAN_VASSAL",
				iKhmer : "TXT_KEY_CIV_KHMER_ARABIAN_VASSAL",
				iMoors : "TXT_KEY_CIV_ARABIA_MOORISH_VASSAL",
				iSpain : "TXT_KEY_CIV_SPAIN_ARABIAN_VASSAL",
				iNetherlands : "TXT_KEY_CIV_NETHERLANDS_ARABIAN_VASSAL",
				iAztecs : "TXT_KEY_CIV_AZTECS_ARABIAN_VASSAL",
				iTurkey : "TXT_KEY_CIV_TURKEY_ARABIAN_VASSAL",
				iMughals : "TXT_KEY_CIV_MUGHALS_ARABIAN_VASSAL",
				iThailand : "TXT_KEY_CIV_THAILAND_ARABIAN_VASSAL",},
			iSpain : {
				iCarthage : "TXT_KEY_CIV_PHOENICIA_SPANISH_VASSAL",
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_SPANISH_VASSAL",
				iMaya : "TXT_KEY_CIV_MAYA_SPANISH_VASSAL",
				iByzantium : "TXT_KEY_CIV_BYZANTIUM_SPANISH_VASSAL",
				iVikings : "TXT_KEY_CIV_VIKINGS_SPANISH_VASSAL",
				iKhmer : "TXT_KEY_CIV_KHMER_SPANISH_VASSAL",
				iIndonesia : "TXT_KEY_CIV_INDONESIA_SPANISH_VASSAL",
				iMoors : "TXT_KEY_CIV_MOORS_SPANISH_VASSAL",
				iFrance : "TXT_KEY_CIV_FRANCE_SPANISH_VASSAL",
				iNetherlands : "TXT_KEY_CIV_NETHERLANDS_SPANISH_VASSAL",
				iMali : "TXT_KEY_CIV_MALI_SPANISH_VASSAL",
				iPortugal : "TXT_KEY_CIV_PORTUGAL_SPANISH_VASSAL",
				iInca : "TXT_KEY_CIV_INCA_SPANISH_VASSAL",
				iAztecs : "TXT_KEY_CIV_AZTECS_SPANISH_VASSAL",
				iMughals : "TXT_KEY_CIV_MUGHALS_SPANISH_VASSAL",
				iThailand : "TXT_KEY_CIV_THAILAND_SPANISH_VASSAL",
				iAmerica : "TXT_KEY_CIV_AMERICA_SPANISH_VASSAL",
				iArgentina : "TXT_KEY_CIV_ARGENTINA_SPANISH_VASSAL"},
			iFrance : {
				iEgypt : "TXT_KEY_CIV_EGYPT_FRENCH_VASSAL",
				iBabylonia : "TXT_KEY_CIV_BABYLONIA_FRENCH_VASSAL",
				iGreece : "TXT_KEY_CIV_GREECE_FRENCH_VASSAL",
				iPersia : "TXT_KEY_CIV_PERSIA_FRENCH_VASSAL",
				iCarthage : "TXT_KEY_CIV_PHOENICIA_FRENCH_VASSAL",
				iRome : "TXT_KEY_CIV_ROME_FRENCH_VASSAL",
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_FRENCH_VASSAL",
				iMaya : "TXT_KEY_CIV_MAYA_FRENCH_VASSAL",
				iByzantium : "TXT_KEY_CIV_BYZANTIUM_FRENCH_VASSAL",
				iVikings : "TXT_KEY_CIV_VIKINGS_FRENCH_VASSAL",
				iArabia : "TXT_KEY_CIV_ARABIA_FRENCH_VASSAL",
				iKhmer : "TXT_KEY_CIV_KHMER_FRENCH_VASSAL",
				iSpain : "TXT_KEY_CIV_SPAIN_FRENCH_VASSAL",
				iEngland : "TXT_KEY_CIV_ENGLAND_FRENCH_VASSAL",
				iHolyRome : "TXT_KEY_CIV_GERMANY_FRENCH_VASSAL",
				iRussia : "TXT_KEY_CIV_RUSSIA_FRENCH_VASSAL",
				iNetherlands : "TXT_KEY_CIV_NETHERLANDS_FRENCH_VASSAL",
				iPoland : "TXT_KEY_CIV_POLAND_FRENCH_VASSAL",
				iMali : "TXT_KEY_CIV_MALI_FRENCH_VASSAL",
				iPortugal : "TXT_KEY_CIV_PORTUGAL_FRENCH_VASSAL",
				iInca : "TXT_KEY_CIV_INCA_FRENCH_VASSAL",
				iItaly : "TXT_KEY_CIV_ROME_FRENCH_VASSAL",
				iAztecs : "TXT_KEY_CIV_AZTECS_FRENCH_VASSAL",
				iMughals : "TXT_KEY_CIV_MUGHALS_FRENCH_VASSAL",
				iTurkey : "TXT_KEY_CIV_TURKEY_FRENCH_VASSAL",
				iThailand : "TXT_KEY_CIV_THAILAND_FRENCH_VASSAL",
				iGermany : "TXT_KEY_CIV_GERMANY_FRENCH_VASSAL",
				iAmerica : "TXT_KEY_CIV_AMERICA_FRENCH_VASSAL"},
			iEngland : {
				iEgypt : "TXT_KEY_CIV_EGYPT_ENGLISH_VASSAL",
				iIndia : "TXT_KEY_CIV_INDIA_ENGLISH_VASSAL",
				iBabylonia : "TXT_KEY_CIV_BABYLONIA_ENGLISH_VASSAL",
				iPersia : "TXT_KEY_CIV_PERSIA_ENGLISH_VASSAL",
				iCarthage : "TXT_KEY_CIV_PHOENICIA_ENGLISH_VASSAL",
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_ENGLISH_VASSAL",
				iMaya : "TXT_KEY_CIV_MAYA_ENGLISH_VASSAL",
				iByzantium : "TXT_KEY_CIV_BYZANTIUM_ENGLISH_VASSAL",
				iVikings : "TXT_KEY_CIV_VIKINGS_ENGLISH_VASSAL",
				iArabia : "TXT_KEY_CIV_ARABIA_ENGLISH_VASSAL",
				iKhmer : "TXT_KEY_CIV_KHMER_ENGLISH_VASSAL",
				iFrance : "TXT_KEY_CIV_FRANCE_ENGLISH_VASSAL",
				iHolyRome : "TXT_KEY_CIV_HOLY_ROME_ENGLISH_VASSAL",
				iNetherlands : "TXT_KEY_CIV_NETHERLANDS_ENGLISH_VASSAL",
				iMali : "TXT_KEY_CIV_MALI_ENGLISH_VASSAL",
				iInca : "TXT_KEY_CIV_INCA_ENGLISH_VASSAL",
				iAztecs : "TXT_KEY_CIV_AZTECS_ENGLISH_VASSAL",
				iTurkey : "TXT_KEY_CIV_TURKEY_ENGLISH_VASSAL",
				iMughals : "TXT_KEY_CIV_MUGHALS_ENGLISH_VASSAL",
				iThailand : "TXT_KEY_CIV_THAILAND_ENGLISH_VASSAL",
				iGermany : "TXT_KEY_CIV_GERMANY_ENGLISH_VASSAL",
				iAmerica : "TXT_KEY_CIV_AMERICA_ENGLISH_VASSAL"},
			iHolyRome : {
				iRome : "TXT_KEY_CIV_ROME_HOLY_ROMAN_VASSAL",
				iFrance : "TXT_KEY_CIV_FRANCE_HOLY_ROMAN_VASSAL",
				iNetherlands : "TXT_KEY_CIV_NETHERLANDS_HOLY_ROMAN_VASSAL",
				iByzantium : "TXT_KEY_CIV_BYZANTIUM_HOLY_ROMAN_VASSAL",
				iItaly : "TXT_KEY_CIV_ITALY_HOLY_ROMAN_VASSAL",
				iPoland : "TXT_KEY_CIV_POLAND_HOLY_ROMAN_VASSAL"},
			iNetherlands : {
				iIndonesia : "TXT_KEY_CIV_INDONESIA_DUTCH_VASSAL",
				iMali : "TXT_KEY_CIV_MALI_DUTCH_VASSAL",
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_DUTCH_VASSAL",
				iAztecs : "TXT_KEY_CIV_AZTECS_DUTCH_VASSAL",
				iMaya : "TXT_KEY_CIV_MAYA_DUTCH_VASSAL",
				iInca : "TXT_KEY_CIV_INCA_DUTCH_VASSAL"},
			iRussia: {
				iAmerica : "TXT_KEY_CIV_AMERICA_RUSSIAN_VASSAL",
				iPoland : "TXT_KEY_CIV_POLAND_RUSSIAN_VASSAL"},
			iPortugal : {
				iIndia : "TXT_KEY_CIV_INDIA_PORTUGUESE_VASSAL",
				iIndonesia : "TXT_KEY_CIV_INDONESIA_PORTUGUESE_VASSAL",
				iAztecs : "TXT_KEY_CIV_AZTECS_PORTUGUESE_VASSAL",
				iInca : "TXT_KEY_CIV_INCA_PORTUGUESE_VASSAL",
				iMaya : "TXT_KEY_CIV_MAYA_PORTUGUESE_VASSAL"},
			#iMali - none so far
			#iPoland - none so far
			#iInca - none so far
			iMongolia : {
				iThailand : "TXT_KEY_CIV_THAILAND_MONGOL_VASSAL",
				iEgypt : "TXT_KEY_CIV_EGYPT_MONGOL_VASSAL",
				iChina : "TXT_KEY_CIV_CHINA_MONGOL_VASSAL",
				iBabylonia : "TXT_KEY_CIV_BABYLONIA_MONGOL_VASSAL",
				iGreece : "TXT_KEY_CIV_GREECE_MONGOL_VASSAL",
				iPersia : "TXT_KEY_CIV_PERSIA_MONGOL_VASSAL",
				iCarthage : "TXT_KEY_CIV_PHOENICIA_MONGOL_VASSAL",
				iRome : "TXT_KEY_CIV_ROME_MONGOL_VASSAL",
				iMaya : "TXT_KEY_CIV_MAYA_MONGOL_VASSAL",
				iByzantium : "TXT_KEY_CIV_BYZANTIUM_MONGOL_VASSAL",
				iVikings : "TXT_KEY_CIV_VIKINGS_MONGOL_VASSAL",
				iKhmer : "TXT_KEY_CIV_KHMER_MONGOL_VASSAL",
				iRussia : "TXT_KEY_CIV_RUSSIA_MONGOL_VASSAL",
				iNetherlands : "TXT_KEY_CIV_NETHERLANDS_MONGOL_VASSAL",
				iInca : "TXT_KEY_CIV_INCA_MONGOL_VASSAL",
				iAztecs : "TXT_KEY_CIV_AZTECS_MONGOL_VASSAL",
				iTurkey : "TXT_KEY_CIV_TURKEY_MONGOL_VASSAL",
				iMughals : "TXT_KEY_CIV_MUGHALS_MONGOL_VASSAL"},
			#iAztecs - none so far
			iTurkey : {
				iThailand : "TXT_KEY_CIV_THAILAND_TURKISH_VASSAL",
				iEgypt : "TXT_KEY_CIV_EGYPT_TURKISH_VASSAL",
				iBabylonia : "TXT_KEY_CIV_BABYLONIA_TURKISH_VASSAL",
				iPersia : "TXT_KEY_CIV_PERSIA_TURKISH_VASSAL",
				iGreece : "TXT_KEY_CIV_GREECE_TURKISH_VASSAL",
				iCarthage : "TXT_KEY_CIV_PHOENICIA_TURKISH_VASSAL",
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_TURKISH_VASSAL",
				iMaya : "TXT_KEY_CIV_MAYA_TURKISH_VASSAL",
				iByzantium : "TXT_KEY_CIV_BYZANTIUM_TURKISH_VASSAL",
				iVikings : "TXT_KEY_CIV_VIKINGS_TURKISH_VASSAL",
				iArabia : "TXT_KEY_CIV_ARABIA_TURKISH_VASSAL",
				iKhmer : "TXT_KEY_CIV_KHMER_TURKISH_VASSAL",
				iRussia : "TXT_KEY_CIV_RUSSIA_TURKISH_VASSAL",
				iNetherlands : "TXT_KEY_CIV_NETHERLANDS_TURKISH_VASSAL",
				iAztecs : "TXT_KEY_CIV_AZTECS_TURKISH_VASSAL",
				iInca : "TXT_KEY_CIV_INCA_TURKISH_VASSAL",
				iMughals : "TXT_KEY_CIV_MUGHALS_TURKISH_VASSAL"},
			iMughals : {
				iIndia : "TXT_KEY_CIV_INDIA_MUGHAL_VASSAL"},
			#iThailand - none so far
			#iCongo - none so far
			iGermany : {
				iHolyRome : "TXT_KEY_CIV_HOLY_ROME_GERMAN_VASSAL",
				iMaya : "TXT_KEY_CIV_MAYA_GERMAN_VASSAL",
				iAztecs : "TXT_KEY_CIV_AZTECS_GERMAN_VASSAL",
				iInca : "TXT_KEY_CIV_INCA_GERMAN_VASSAL",
				iMali : "TXT_KEY_CIV_MALI_GERMAN_VASSAL",
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_GERMAN_VASSAL",
				iPoland : "TXT_KEY_CIV_POLAND_GERMAN_VASSAL"},
			iAmerica : {
				iEngland : "TXT_KEY_CIV_ENGLAND_AMERICAN_VASSAL",
				iJapan : "TXT_KEY_CIV_JAPAN_AMERICAN_VASSAL",
				iGermany : "TXT_KEY_CIV_GERMANY_AMERICAN_VASSAL",
				iMaya : "TXT_KEY_CIV_MAYA_AMERICAN_VASSAL",
				iKorea : "TXT_KEY_CIV_KOREA_AMERICAN_VASSAL",
				iAztecs : "TXT_KEY_CIV_AZTECS_AMERICAN_VASSAL",},
			# Argentina - none so far
			iBrazil : {
				iArgentina : "TXT_KEY_CIV_ARGENTINA_BRAZILIAN_VASSAL",},
		}
		
		self.genericVassalNames = {
			iPersia : "TXT_KEY_CIV_PERSIAN_VASSAL_GENERIC",
			iRome : "TXT_KEY_CIV_ROMAN_VASSAL_GENERIC",
			iJapan : "TXT_KEY_CIV_JAPANESE_VASSAL_GENERIC",
			iByzantium : "TXT_KEY_CIV_BYZANTINE_VASSAL_GENERIC",
			iArabia : "TXT_KEY_CIV_ARABIAN_VASSAL_GENERIC",
			iMoors : "TXT_KEY_CIV_ARABIAN_VASSAL_GENERIC",
			iSpain : "TXT_KEY_CIV_SPANISH_VASSAL_GENERIC",
			iFrance : "TXT_KEY_CIV_FRENCH_VASSAL_GENERIC",
			iEngland : "TXT_KEY_CIV_ENGLISH_VASSAL_GENERIC",
			iMongolia : "TXT_KEY_CIV_MONGOL_VASSAL_GENERIC",
			iTurkey : "TXT_KEY_CIV_TURKISH_VASSAL_GENERIC"
		}
				
		self.sovietVassals = {
                        iEgypt : "TXT_KEY_CIV_EGYPT_SOVIET_VASSAL",
                        iIndia : "TXT_KEY_CIV_INDIA_SOVIET_VASSAL",
                        iChina : "TXT_KEY_CIV_CHINA_SOVIET_VASSAL",
                        iBabylonia : "TXT_KEY_CIV_BABYLONIA_SOVIET_VASSAL",
			iHarappa : "TXT_KEY_CIV_HARAPPA_SOVIET_VASSAL",
                        iGreece : "TXT_KEY_CIV_GREECE_SOVIET_VASSAL",
                        iPersia : "TXT_KEY_CIV_PERSIA_SOVIET_VASSAL",
                        iCarthage : "TXT_KEY_CIV_PHOENICIA_SOVIET_VASSAL",
			iPolynesia : "TXT_KEY_CIV_POLYNESIA_SOVIET_VASSAL",
                        iRome : "TXT_KEY_CIV_ROME_SOVIET_VASSAL",
			iItaly : "TXT_KEY_CIV_ROME_SOVIET_VASSAL",
                        iJapan : "TXT_KEY_CIV_JAPAN_SOVIET_VASSAL",
			iTamils : "TXT_KEY_CIV_TAMILS_SOVIET_VASSAL",
                        iEthiopia : "TXT_KEY_CIV_ETHIOPIA_SOVIET_VASSAL",
                        iKorea : "TXT_KEY_CIV_KOREA_SOVIET_VASSAL",
                        iMaya : "TXT_KEY_CIV_MAYA_SOVIET_VASSAL",
                        iByzantium : "TXT_KEY_CIV_BYZANTIUM_SOVIET_VASSAL",
                        iVikings : "TXT_KEY_CIV_VIKINGS_SOVIET_VASSAL",
                        iArabia : "TXT_KEY_CIV_ARABIA_SOVIET_VASSAL",
                        iKhmer : "TXT_KEY_CIV_KHMER_SOVIET_VASSAL",
			iTibet : "TXT_KEY_CIV_TIBET_SOVIET_VASSAL",
                        iIndonesia : "TXT_KEY_CIV_INDONESIA_SOVIET_VASSAL",
			iMoors : "TXT_KEY_CIV_MOORS_SOVIET_VASSAL",
                        iSpain : "TXT_KEY_CIV_SPAIN_SOVIET_VASSAL",
                        iFrance : "TXT_KEY_CIV_FRANCE_SOVIET_VASSAL",
                        iEngland : "TXT_KEY_CIV_ENGLAND_SOVIET_VASSAL",
                        iHolyRome : "TXT_KEY_CIV_HOLY_ROME_SOVIET_VASSAL",
                        iRussia : "TXT_KEY_CIV_RUSSIA_SOVIET_VASSAL",
                        iNetherlands : "TXT_KEY_CIV_NETHERLANDS_SOVIET_VASSAL",
                        iMali : "TXT_KEY_CIV_MALI_SOVIET_VASSAL",
			iPoland : "TXT_KEY_CIV_POLAND_SOVIET_VASSAL",
                        iPortugal : "TXT_KEY_CIV_PORTUGAL_SOVIET_VASSAL",
                        iInca : "TXT_KEY_CIV_INCA_SOVIET_VASSAL",
                        iMongolia : "TXT_KEY_CIV_MONGOLIA_SOVIET_VASSAL",
                        iAztecs : "TXT_KEY_CIV_AZTECS_SOVIET_VASSAL",
                        iTurkey : "TXT_KEY_CIV_TURKEY_SOVIET_VASSAL",
			iMughals : "TXT_KEY_CIV_MUGHALS_SOVIET_VASSAL",
			iThailand : "TXT_KEY_CIV_THAILAND_SOVIET_VASSAL",
			iCongo : "TXT_KEY_CIV_CONGO_SOVIET_VASSAL",
			iGermany : "TXT_KEY_CIV_GERMANY_SOVIET_VASSAL",
                        iAmerica : "TXT_KEY_CIV_AMERICA_SOVIET_VASSAL",
			iArgentina : "TXT_KEY_CIV_ARGENTINA_SOVIET_VASSAL",
			iBrazil : "TXT_KEY_CIV_BRAZIL_SOVIET_VASSAL",
			iCanada : "TXT_KEY_CIV_CANADA_SOVIET_VASSAL",
                }
		
		self.naziVassals = {
                        iEgypt : "TXT_KEY_CIV_EGYPT_NAZI_VASSAL",
                        iIndia : "TXT_KEY_CIV_INDIA_NAZI_VASSAL",
                        iChina : "TXT_KEY_CIV_CHINA_NAZI_VASSAL",
                        iBabylonia : "TXT_KEY_CIV_BABYLONIA_NAZI_VASSAL",
			iHarappa : "TXT_KEY_CIV_HARAPPA_NAZI_VASSAL",
                        iGreece : "TXT_KEY_CIV_GREECE_NAZI_VASSAL",
                        iPersia : "TXT_KEY_CIV_PERSIA_NAZI_VASSAL",
                        iCarthage : "TXT_KEY_CIV_PHOENICIA_NAZI_VASSAL",
			iPolynesia : "TXT_KEY_CIV_POLYNESIA_NAZI_VASSAL",
                        iRome : "TXT_KEY_CIV_ROME_NAZI_VASSAL",
			iItaly : "TXT_KEY_CIV_ROME_NAZI_VASSAL",
                        iJapan : "TXT_KEY_CIV_JAPAN_NAZI_VASSAL",
			iTamils : "TXT_KEY_CIV_TAMILS_NAZI_VASSAL",
                        iEthiopia : "TXT_KEY_CIV_ETHIOPIA_NAZI_VASSAL",
                        iKorea : "TXT_KEY_CIV_KOREA_NAZI_VASSAL",
                        iMaya : "TXT_KEY_CIV_MAYA_NAZI_VASSAL",
                        iByzantium : "TXT_KEY_CIV_BYZANTIUM_NAZI_VASSAL",
                        iVikings : "TXT_KEY_CIV_VIKINGS_NAZI_VASSAL",
                        iArabia : "TXT_KEY_CIV_ARABIA_NAZI_VASSAL",
			iTibet : "TXT_KEY_CIV_TIBET_NAZI_VASSAL",
                        iKhmer : "TXT_KEY_CIV_KHMER_NAZI_VASSAL",
                        iIndonesia : "TXT_KEY_CIV_INDONESIA_NAZI_VASSAL",
			iMoors : "TXT_KEY_CIV_MOORS_NAZI_VASSAL",
                        iSpain : "TXT_KEY_CIV_SPAIN_NAZI_VASSAL",
                        iFrance : "TXT_KEY_CIV_FRANCE_NAZI_VASSAL",
                        iEngland : "TXT_KEY_CIV_ENGLAND_NAZI_VASSAL",
                        iHolyRome : "TXT_KEY_CIV_HOLY_ROME_NAZI_VASSAL",
                        iRussia : "TXT_KEY_CIV_RUSSIA_NAZI_VASSAL",
                        iNetherlands : "TXT_KEY_CIV_NETHERLANDS_NAZI_VASSAL",
                        iMali : "TXT_KEY_CIV_MALI_NAZI_VASSAL",
			iPoland : "TXT_KEY_CIV_POLAND_NAZI_VASSAL",
                        iPortugal : "TXT_KEY_CIV_PORTUGAL_NAZI_VASSAL",
                        iInca : "TXT_KEY_CIV_INCA_NAZI_VASSAL",
                        iMongolia : "TXT_KEY_CIV_MONGOLIA_NAZI_VASSAL",
                        iAztecs : "TXT_KEY_CIV_AZTECS_NAZI_VASSAL",
                        iTurkey : "TXT_KEY_CIV_TURKEY_NAZI_VASSAL",
			iMughals : "TXT_KEY_CIV_MUGHALS_NAZI_VASSAL",
			iThailand : "TXT_KEY_CIV_THAILAND_NAZI_VASSAL",
			iCongo : "TXT_KEY_CIV_CONGO_NAZI_VASSAL",
			iGermany : "TXT_KEY_CIV_GERMANY_NAZI_VASSAL",
                        iAmerica : "TXT_KEY_CIV_AMERICA_NAZI_VASSAL",
			iArgentina : "TXT_KEY_CIV_ARGENTINA_NAZI_VASSAL",
			iBrazil : "TXT_KEY_CIV_BRAZIL_NAZI_VASSAL",
			iCanada : "TXT_KEY_CIV_CANADA_NAZI_VASSAL",
                }

                self.fascistNames = {
                        iEgypt : "TXT_KEY_CIV_EGYPT_DESC_FASCIST",
                        iIndia : "TXT_KEY_CIV_INDIA_DESC_FASCIST",
                        iChina : "TXT_KEY_CIV_CHINA_DESC_FASCIST",
                        iBabylonia : "TXT_KEY_CIV_BABYLONIA_DESC_FASCIST",
			iHarappa : "TXT_KEY_CIV_HARAPPA_DESC_FASCIST",
                        iGreece : "TXT_KEY_CIV_GREECE_DESC_FASCIST",
                        iPersia : "TXT_KEY_CIV_PERSIA_DESC_FASCIST",
                        iCarthage : "TXT_KEY_CIV_PHOENICIA_DESC_FASCIST",
			iPolynesia : "TXT_KEY_CIV_POLYNESIA_DESC_FASCIST",
                        iRome : "TXT_KEY_CIV_ROME_DESC_FASCIST",
                        iJapan : "TXT_KEY_CIV_JAPAN_DESC_FASCIST",
			iTamils : "TXT_KEY_CIV_TAMILS_DESC_FASCIST",
                        iEthiopia : "TXT_KEY_CIV_ETHIOPIA_DESC_FASCIST",
                        iKorea : "TXT_KEY_CIV_KOREA_DESC_FASCIST",
                        iMaya : "TXT_KEY_CIV_MAYA_DESC_FASCIST",
                        iByzantium : "TXT_KEY_CIV_BYZANTIUM_DESC_FASCIST",
                        iVikings : "TXT_KEY_CIV_VIKINGS_DESC_FASCIST",
                        iArabia : "TXT_KEY_CIV_ARABIA_DESC_FASCIST",
			iTibet : "TXT_KEY_CIV_TIBET_DESC_FASCIST",
                        iKhmer : "TXT_KEY_CIV_KHMER_DESC_FASCIST",
                        iIndonesia : "TXT_KEY_CIV_INDONESIA_DESC_FASCIST",
			iMoors : "TXT_KEY_CIV_MOORS_DESC_FASCIST",
                        iSpain : "TXT_KEY_CIV_SPAIN_DESC_FASCIST",
                        iFrance : "TXT_KEY_CIV_FRANCE_DESC_FASCIST",
                        iEngland : "TXT_KEY_CIV_ENGLAND_DESC_FASCIST",
                        iHolyRome : "TXT_KEY_CIV_HOLY_ROME_DESC_FASCIST",
                        iRussia : "TXT_KEY_CIV_RUSSIA_DESC_FASCIST",
                        iNetherlands : "TXT_KEY_CIV_NETHERLANDS_DESC_FASCIST",
                        iMali : "TXT_KEY_CIV_MALI_DESC_FASCIST",
			iPoland : "TXT_KEY_CIV_POLAND_DESC_FASCIST",
                        iPortugal : "TXT_KEY_CIV_PORTUGAL_DESC_FASCIST",
                        iInca : "TXT_KEY_CIV_INCA_DESC_FASCIST",
			iItaly : "TXT_KEY_CIV_ROME_DESC_FASCIST",
                        iMongolia : "TXT_KEY_CIV_MONGOLIA_DESC_FASCIST",
                        iAztecs : "TXT_KEY_CIV_AZTECS_DESC_FASCIST",
                        iTurkey : "TXT_KEY_CIV_TURKEY_DESC_FASCIST",
			iMughals: "TXT_KEY_CIV_MUGHALS_DESC_FASCIST",
			iThailand : "TXT_KEY_CIV_THAILAND_DESC_FASCIST",
			iCongo : "TXT_KEY_CIV_CONGO_DESC_FASCIST",
			iGermany : "TXT_KEY_CIV_GERMANY_DESC_FASCIST",
                        iAmerica : "TXT_KEY_CIV_AMERICA_DESC_FASCIST",
			iArgentina : "TXT_KEY_CIV_ARGENTINA_DESC_FASCIST",
			iBrazil : "TXT_KEY_CIV_BRAZIL_DESC_FASCIST",
			iCanada : "TXT_KEY_CIV_CANADA_DESC_FASCIST",
                }

                self.communistNames = {
                        iEgypt : "TXT_KEY_CIV_EGYPT_DESC_COMMUNIST",
                        iIndia : "TXT_KEY_CIV_INDIA_DESC_COMMUNIST",
                        iChina : "TXT_KEY_CIV_CHINA_DESC_COMMUNIST",
                        iBabylonia : "TXT_KEY_CIV_BABYLONIA_DESC_COMMUNIST",
			iHarappa : "TXT_KEY_CIV_HARAPPA_DESC_COMMUNIST",
                        iGreece : "TXT_KEY_CIV_GREECE_DESC_COMMUNIST",
                        iPersia : "TXT_KEY_CIV_PERSIA_DESC_COMMUNIST",
                        iCarthage : "TXT_KEY_CIV_PHOENICIA_DESC_COMMUNIST",
			iPolynesia : "TXT_KEY_CIV_POLYNESIA_DESC_COMMUNIST",
                        iRome : "TXT_KEY_CIV_ROME_DESC_COMMUNIST",
                        iJapan : "TXT_KEY_CIV_JAPAN_DESC_COMMUNIST",
			iTamils : "TXT_KEY_CIV_TAMILS_DESC_COMMUNIST",
                        iEthiopia : "TXT_KEY_CIV_ETHIOPIA_DESC_COMMUNIST",
                        iKorea : "TXT_KEY_CIV_KOREA_DESC_COMMUNIST",
                        iMaya : "TXT_KEY_CIV_MAYA_DESC_COMMUNIST",
                        iByzantium : "TXT_KEY_CIV_BYZANTIUM_DESC_COMMUNIST",
                        iVikings : "TXT_KEY_CIV_VIKINGS_DESC_COMMUNIST",
                        iArabia : "TXT_KEY_CIV_ARABIA_DESC_COMMUNIST",
			iTibet : "TXT_KEY_CIV_TIBET_DESC_COMMUNIST",
                        iKhmer : "TXT_KEY_CIV_KHMER_DESC_COMMUNIST",
                        iIndonesia : "TXT_KEY_CIV_INDONESIA_DESC_COMMUNIST",
			iMoors : "TXT_KEY_CIV_MOORS_DESC_COMMUNIST",
                        iSpain : "TXT_KEY_CIV_SPAIN_DESC_COMMUNIST",
                        iFrance : "TXT_KEY_CIV_FRANCE_DESC_COMMUNIST",
                        iEngland : "TXT_KEY_CIV_ENGLAND_DESC_COMMUNIST",
                        iHolyRome : "TXT_KEY_CIV_HOLY_ROME_DESC_COMMUNIST",
                        iRussia : "TXT_KEY_CIV_RUSSIA_DESC_COMMUNIST",
                        iNetherlands : "TXT_KEY_CIV_NETHERLANDS_DESC_COMMUNIST",
                        iMali : "TXT_KEY_CIV_MALI_DESC_COMMUNIST",
			iPoland : "TXT_KEY_CIV_POLAND_DESC_COMMUNIST",
                        iPortugal : "TXT_KEY_CIV_PORTUGAL_DESC_COMMUNIST",
                        iInca : "TXT_KEY_CIV_INCA_DESC_COMMUNIST",
			iItaly : "TXT_KEY_CIV_ROME_DESC_COMMUNIST",
                        iMongolia : "TXT_KEY_CIV_MONGOLIA_DESC_COMMUNIST",
                        iAztecs : "TXT_KEY_CIV_AZTECS_DESC_COMMUNIST",
                        iTurkey : "TXT_KEY_CIV_TURKEY_DESC_COMMUNIST",
			iMughals : "TXT_KEY_CIV_MUGHALS_DESC_COMMUNIST",
			iThailand : "TXT_KEY_CIV_THAILAND_DESC_COMMUNIST",
			iCongo : "TXT_KEY_CIV_CONGO_DESC_COMMUNIST",
			iGermany : "TXT_KEY_CIV_GERMANY_DESC_COMMUNIST",
                        iAmerica : "TXT_KEY_CIV_AMERICA_DESC_COMMUNIST",
			iArgentina : "TXT_KEY_CIV_ARGENTINA_DESC_COMMUNIST",
			iBrazil : "TXT_KEY_CIV_BRAZIL_DESC_COMMUNIST",
			iCanada : "TXT_KEY_CIV_CANADA_DESC_COMMUNIST",
                }

                self.democraticNames = {
                        iEgypt : "TXT_KEY_CIV_EGYPT_DESC_DEMOCRATIC",
                        iIndia : "TXT_KEY_CIV_INDIA_DESC_DEMOCRATIC",
                        iChina : "TXT_KEY_CIV_CHINA_DESC_DEMOCRATIC",
                        iBabylonia : "TXT_KEY_CIV_BABYLONIA_DESC_DEMOCRATIC",
			iHarappa : "TXT_KEY_CIV_HARAPPA_DESC_DEMOCRATIC",
                        iGreece : "TXT_KEY_CIV_GREECE_DESC_DEMOCRATIC",
                        iPersia : "TXT_KEY_CIV_PERSIA_DESC_DEMOCRATIC",
                        iCarthage : "TXT_KEY_CIV_PHOENICIA_DESC_DEMOCRATIC",
			iPolynesia : "TXT_KEY_CIV_POLYNESIA_DESC_DEMOCRATIC",
                        iRome : "TXT_KEY_CIV_ROME_DESC_DEMOCRATIC",
                        iJapan : "TXT_KEY_CIV_JAPAN_DESC_DEMOCRATIC",
			iTamils : "TXT_KEY_CIV_TAMILS_DESC_DEMOCRATIC",
                        iEthiopia : "TXT_KEY_CIV_ETHIOPIA_DESC_DEMOCRATIC",
                        iKorea : "TXT_KEY_CIV_KOREA_DESC_DEMOCRATIC",
                        iMaya : "TXT_KEY_CIV_MAYA_DESC_DEMOCRATIC",
                        iByzantium : "TXT_KEY_CIV_BYZANTIUM_DESC_DEMOCRATIC",
                        iVikings : "TXT_KEY_CIV_VIKINGS_DESC_DEMOCRATIC",
                        iArabia : "TXT_KEY_CIV_ARABIA_DESC_DEMOCRATIC",
			iTibet : "TXT_KEY_CIV_TIBET_DESC_DEMOCRATIC",
                        iKhmer : "TXT_KEY_CIV_KHMER_DESC_DEMOCRATIC",
                        iIndonesia : "TXT_KEY_CIV_INDONESIA_DESC_DEMOCRATIC",
			iMoors : "TXT_KEY_CIV_MOORS_DESC_DEMOCRATIC",
                        iSpain : "TXT_KEY_CIV_SPAIN_DESC_DEMOCRATIC",
                        iFrance : "TXT_KEY_CIV_FRANCE_DESC_DEMOCRATIC",
                        iEngland : "TXT_KEY_CIV_ENGLAND_DESC_DEMOCRATIC",
                        iHolyRome : "TXT_KEY_CIV_HOLY_ROME_DESC_DEMOCRATIC",
                        iRussia : "TXT_KEY_CIV_RUSSIA_DESC_DEMOCRATIC",
                        iNetherlands : "TXT_KEY_CIV_NETHERLANDS_DESC_DEMOCRATIC",
                        iMali : "TXT_KEY_CIV_MALI_DESC_DEMOCRATIC",
			iPoland : "TXT_KEY_CIV_POLAND_DESC_DEMOCRATIC",
                        iPortugal : "TXT_KEY_CIV_PORTUGAL_DESC_DEMOCRATIC",
                        iInca : "TXT_KEY_CIV_INCA_DESC_DEMOCRATIC",
			iItaly : "TXT_KEY_CIV_ROME_DESC_DEMOCRATIC",
                        iMongolia : "TXT_KEY_CIV_MONGOLIA_DESC_DEMOCRATIC",
                        iAztecs : "TXT_KEY_CIV_AZTECS_DESC_DEMOCRATIC",
                        iTurkey : "TXT_KEY_CIV_TURKEY_DESC_DEMOCRATIC",
			iMughals : "TXT_KEY_CIV_MUGHALS_DESC_DEMOCRATIC",
			iThailand : "TXT_KEY_CIV_THAILAND_DESC_DEMOCRATIC",
			iCongo : "TXT_KEY_CIV_CONGO_DESC_DEMOCRATIC",
			iGermany : "TXT_KEY_CIV_GERMANY_DESC_DEMOCRATIC",
                        iAmerica : "TXT_KEY_CIV_AMERICA_DESC_DEMOCRATIC",
			iArgentina : "TXT_KEY_CIV_ARGENTINA_DESC_DEMOCRATIC",
			iBrazil : "TXT_KEY_CIV_BRAZIL_DESC_DEMOCRATIC",
			iCanada : "TXT_KEY_CIV_CANADA_DESC_DEMOCRATIC",
                }
		
		self.modernIslamNames = {
                        iIndia : "TXT_KEY_CIV_INDIA_DESC_ISLAMIC_MODERN",
                        iPersia : "TXT_KEY_CIV_PERSIA_DESC_ISLAMIC_MODERN",
                        iMali : "TXT_KEY_CIV_MALI_DESC_ISLAMIC_MODERN",
                        iTurkey : "TXT_KEY_CIV_TURKEY_DESC_ISLAMIC_MODERN",
			iMughals : "TXT_KEY_CIV_MUGHALS_DESC_ISLAMIC_MODERN",
                }
		
		self.startingLeaders = {
			iEgypt : iRamesses,
			iIndia : iAsoka,
			iChina : iQinShiHuang,
			iBabylonia : iGilgamesh,
			iHarappa : iVatavelli,
			iGreece : iPericles,
			iPersia : iCyrus,
			iCarthage : iHiram,
			iPolynesia : iAhoeitu,
			iRome : iJuliusCaesar,
			iJapan : iJimmu,
			iTamils : iRajendra,
			iEthiopia : iZaraYaqob,
			iKorea : iWangKon,
			iMaya : iPacal,
			iByzantium : iJustinian,
			iVikings : iRagnar,
			iArabia : iHarun,
			iTibet : iSongtsen,
			iKhmer : iSuryavarman,
			iIndonesia : iDharmasetu,
			iMoors : iRahman,
			iSpain : iIsabella,
			iFrance : iCharlemagne,
			iEngland : iAlfred,
			iHolyRome : iBarbarossa,
			iRussia : iYaroslav,
			iNetherlands : iWillemVanOranje,
			iMali : iMansaMusa,
			iPoland : iCasimir,
			iPortugal : iAfonso,
			iInca : iHuaynaCapac,
			iItaly : iLorenzo,
			iMongolia : iGenghisKhan,
			iAztecs : iMontezuma,
			iMughals : iTughluq,
			iTurkey : iMehmed,
			iThailand : iNaresuan,
			iCongo : iMbemba,
			iGermany : iFrederick,
			iAmerica : iWashington,
			iArgentina : iSanMartin,
			iBrazil : iDomPedro,
			iCanada : iTrudeau,
		}
		
		self.lateStartingLeaders = {
			iChina : iTaizong
		}
		
		self.l1700ADLeaders = {
			iChina : iHongwu,
			iIndia : iShivaji,
			iPersia : iAbbas,
			iJapan : iTokugawa,
			iVikings : iGustav,
			iSpain : iPhilip,
			iFrance : iLouis,
			iEngland : iVictoria,
			iHolyRome : iFrancis,
			iRussia : iPeter,
			iPoland : iSobieski,
			iPortugal : iJoao,
			iMughals : iAkbar,
			iTurkey : iSuleiman,
			iGermany : iFrederick,
		}
		
	def getAnarchyTurns(self, iPlayer):
		return sd.scriptDict['lAnarchyTurns'][iPlayer]
		
	def changeAnarchyTurns(self, iPlayer, iAmount):
		sd.scriptDict['lAnarchyTurns'][iPlayer] += iAmount
		
	def getResurrections(self, iPlayer):
		return sd.scriptDict['lResurrections'][iPlayer]
		
	def changeResurrections(self, iPlayer, iAmount):
		sd.scriptDict['lResurrections'][iPlayer] += iAmount
		
	#def getPreviousOwners(self, iPlayer):
        #        return sd.scriptDict['lPreviousOwners']
		
	#def addPreviousOwner(self, iPlayer, iPreviousOwner):
	#	sd.scriptDict['lPreviousOwners'].append(iPreviousOwner)
		
	#def removePreviousOwner(self, iPlayer, iPreviousOwner):
	#	sd.scriptDict['lPreviousOwner'].remove(iPreviousOwner)
                

        def setCivDesc(self, iCiv, sName, sInsert=""):
		if sInsert == "":
			gc.getPlayer(iCiv).setCivDescription(localText.getText(sName, ()))
		else:
			gc.getPlayer(iCiv).setCivDescription(localText.getText(sName, (sInsert,)))
			
	def setCivName(self, iCiv, sName, sShort, sAdjective):
		gc.getPlayer(iCiv).setCivName(localText.getText(sName, ()), localText.getText(sShort, ()), localText.getText(sAdjective, ()))
	
	def setCivAdjective(self, iCiv, sAdj):
		gc.getPlayer(iCiv).setCivAdjective(sAdj)
		
	def setCivShortDesc(self, iCiv, sShort):
		gc.getPlayer(iCiv).setCivShortDescription(sShort)
		
	def setLeader(self, iCiv, iLeader):
		if gc.getPlayer(iCiv).getLeader() != iLeader:
			gc.getPlayer(iCiv).setLeader(iLeader)

        def setup(self):
                for iPlayer in range(iNumPlayers):
                        pPlayer = gc.getPlayer(iPlayer)
                        self.setCivDesc(iPlayer, self.peopleNames[iPlayer])
			
			if not gc.getPlayer(iPlayer).isHuman():
				self.setLeader(iPlayer, self.startingLeaders[iPlayer])
			
				if utils.getScenario() == i600AD and iPlayer in self.lateStartingLeaders:
					self.setLeader(iPlayer, self.lateStartingLeaders[iPlayer])
					
				if utils.getScenario() == i1700AD and iPlayer in self.l1700ADLeaders:
					self.setLeader(iPlayer, self.l1700ADLeaders[iPlayer])
			
		if utils.getScenario() == i600AD:
			self.changeAnarchyTurns(iChina, 3)
			self.setCivDesc(iByzantium, "TXT_KEY_CIV_BYZANTIUM_DESC_DEFAULT")
		elif utils.getScenario() == i1700AD:
			self.changeResurrections(iEgypt, 1)
			
		if utils.getScenario() == i1700AD:
			for iPlayer in [iChina, iIndia, iTamils, iPersia, iKorea, iJapan, iVikings, iSpain, iFrance, iEngland, iHolyRome, iRussia, iPoland, iPortugal, iMughals, iTurkey, iThailand, iCongo, iNetherlands, iGermany]:
				self.checkName(iPlayer)

        def setDetermineds(self, iPlayer, szName="", szFlag=""):
                pPlayer = gc.getPlayer(iPlayer)
                if szName:
                        self.setCivDesc(iPlayer, szName)
                if szFlag:
                        pPlayer.setFlag(szFlag)
			
	def isDemocratic(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		iCivic0 = pPlayer.getCivics(0)
		iCivic1 = pPlayer.getCivics(1)
		
		if iCivic0 == iCivicRepublic:
			return True
		if iCivic0 == iCivicAutocracy and (iCivic1 == iCivicRepresentation or iCivic1 == iCivicEgalitarianism):
			return True
			
		return False
		
	def isCommunist(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		iCivic0 = pPlayer.getCivics(0)
		iCivic1 = pPlayer.getCivics(1)
		iCivic3 = pPlayer.getCivics(3)
		
		if iCivic3 != iCivicCentralPlanning:
			return False
			
		if iCivic0 == iCivicTheocracy:
			return False
			
		if iCivic1 in [iCivicVassalage, iCivicAbsolutism]:
			return False
			
		return True
		
	def isFascist(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		#iCivic0 = pPlayer.getCivics(0)
		iCivic1 = pPlayer.getCivics(1)
		
		if iCivic1 == iCivicTotalitarianism:
			return True
			
		#if iCivic0 == iCivicAutocracy and iCivic1 not in [iCivicRepresentation, iCivicEgalitarianism]:
		#	return True
			
		return False
		
	def isEmpire(self, iPlayer):
		iThreshold = 5
		
		if iPlayer == iCarthage: iThreshold = 4
		elif iPlayer == iIndonesia: iThreshold = 4
		elif iPlayer == iKorea: iThreshold = 4
		elif iPlayer == iRussia: iThreshold = 8
		elif iPlayer == iHolyRome: iThreshold = 3
		elif iPlayer == iGermany: iThreshold = 4
		elif iPlayer == iPersia and pPersia.isReborn(): iThreshold = 4
		elif iPlayer == iItaly: iThreshold = 4
		elif iPlayer == iInca: iThreshold = 3
		elif iPlayer == iMongolia: iThreshold = 6
		elif iPlayer == iPoland: iThreshold = 3
		elif iPlayer == iMoors: iThreshold = 3
		elif iPlayer == iTibet: iThreshold = 2
		elif iPlayer == iPolynesia: iThreshold = 3
		elif iPlayer == iTamils: iThreshold = 3
			
		return gc.getPlayer(iPlayer).getNumCities() >= iThreshold
		
		
        def checkName(self, iPlayer, lPreviousOwners=[]):
        
                if iPlayer >= iNumPlayers: return
		
		if not gc.getPlayer(iPlayer).isAlive(): return
        
                bVassal = utils.isAVassal(iPlayer)
                iMaster = utils.getMaster(iPlayer)
                pPlayer = gc.getPlayer(iPlayer)
                tPlayer = gc.getTeam(pPlayer.getTeam())
                if iMaster != -1:
                        pMasterPlayer = gc.getPlayer(iMaster)
                bReborn = pPlayer.isReborn()
                iReligion = pPlayer.getStateReligion()
                capital = gc.getPlayer(iPlayer).getCapitalCity()
                tCapitalCoords = (capital.getX(), capital.getY())
                iCivic0 = pPlayer.getCivics(0)
                iCivic1 = pPlayer.getCivics(1)
                iCivic2 = pPlayer.getCivics(2)
                iCivic3 = pPlayer.getCivics(3)
                iCivic4 = pPlayer.getCivics(4)
                iGameTurn = gc.getGame().getGameTurn()
                bAnarchy = pPlayer.isAnarchy()
		bEmpire = self.isEmpire(iPlayer)
		bCityStates = (iCivic0 == iCivicCityStates)
		bTheocracy = (iCivic0 == iCivicTheocracy)
		bResurrected = (self.getResurrections(iPlayer) > 0)
		bCapitulated = bVassal and tPlayer.isCapitulated()
		iAnarchyTurns = self.getAnarchyTurns(iPlayer)
		iEra = pPlayer.getCurrentEra()
		iGameEra = gc.getGame().getCurrentEra()
		# count number of resurrections (use to determine transition to medieval Egypt, Saudi-Arabia etc.)
		# count anarchy turns (use for different dynasties, e.g. China or Egypt)
		
		if iPlayer in [iRome, iCarthage, iGreece, iIndia, iMaya, iAztecs]:
			if not gc.getTeam(iPlayer).isHasTech(iCodeOfLaws):
				bCityStates = True
		
                bWar = False
                for iTarget in range(iNumMajorPlayers):
                        if tPlayer.isAtWar(iTarget):
                                bWar = True
				break

		# Leoreth: Vassalage (historical -> generic -> default) -> Civics -> Historical (usually religion -> civics -> size) -> Default
                
                # by vassalage
                if bCapitulated:
			if iMaster == iRussia and pMasterPlayer.getCivics(3) == iCivicCentralPlanning:
				self.setCivDesc(iPlayer, self.sovietVassals[iPlayer])
				return
			if iMaster == iGermany and pMasterPlayer.getCivics(1) == iCivicTotalitarianism:
				self.setCivDesc(iPlayer, self.naziVassals[iPlayer])
				return
				
			# special cases
			if iMaster == iRome and iPlayer == iCarthage and capital.getX() < 73:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_CARTHAGE_ROMAN_VASSAL")
				return
			if iMaster == iHolyRome and iPlayer == iPoland and iGameEra >= iIndustrial:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_POLAND_AUSTRIAN_VASSAL")
				return
			if iMaster == iEngland and iPlayer == iMughals and not gc.getPlayer(iIndia).isAlive():
				self.setCivDesc(iPlayer, self.specificVassalNames[iEngland][iIndia])
				return
			if iMaster == iSpain and iPlayer == iMaya and bReborn:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_COLOMBIA_SPANISH_VASSAL")
				return
			if iMaster == iPersia and pMasterPlayer.isReborn():
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_VASSAL_GENERIC_PROTECTORATE", pPlayer.getCivilizationShortDescriptionKey())
				return
			
			if iMaster in self.specificVassalNames and not pMasterPlayer.isReborn():
				if iPlayer in self.specificVassalNames[iMaster]:
					self.setCivDesc(iPlayer, self.specificVassalNames[iMaster][iPlayer])
					return
					
			if iMaster in self.genericVassalNames:
				self.setCivDesc(iPlayer, self.genericVassalNames[iMaster], pPlayer.getCivilizationShortDescriptionKey())
				return
				
			if iPlayer in [iMali, iEthiopia, iCongo, iAztecs, iInca, iMaya]:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_VASSAL_GENERIC_COLONY", pPlayer.getCivilizationShortDescriptionKey())
				return
				
			self.setCivDesc(iPlayer, "TXT_KEY_CIV_VASSAL_GENERIC_PROTECTORATE", pPlayer.getCivilizationShortDescriptionKey())
			return
		
		# Communism
		if self.isCommunist(iPlayer):
			if iPlayer == iMaya and bReborn:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_COLOMBIA_DESC_COMMUNIST")
				return
			if iPlayer == iCarthage and capital.getX() < 73:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_CARTHAGE_DESC_COMMUNIST")
				return
			if iPlayer in self.communistNames:
				self.setCivDesc(iPlayer, self.communistNames[iPlayer])
				return
				
		# Fascism
		if self.isFascist(iPlayer):
			if iPlayer == iMaya and bReborn:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_COLOMBIA_DESC_FASCIST")
				return
			if iPlayer == iCarthage and capital.getX() < 73:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_CARTHAGE_DESC_FASCIST")
				return
			if iPlayer in self.fascistNames:
				self.setCivDesc(iPlayer, self.fascistNames[iPlayer])
				return
			
		# Democracy (includes Islamic Republics)
		if self.isDemocratic(iPlayer):
			if iPlayer == iMughals:
				if iEra <= iRenaissance:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_MUGHALS_REPUBLIC_MEDIEVAL")
					return
			elif iPlayer == iVikings:
				if capital.getName() == "Stockholm":
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_VIKINGS_SWEDEN_REPUBLIC")
					return
				elif capital.getName() == "Kobenhavn":
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_VIKINGS_DENMARK_REPUBLIC")
					return
			elif iPlayer == iPoland:
				if iEra <= iIndustrial:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_POLAND_EMPIRE")
					return
			elif iPlayer == iAmerica:
				if iCivic2 == iCivicAgrarianism or iCivic2 == iCivicSlavery:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_AMERICA_CSA")
					return
			elif iPlayer == iHolyRome:
				if iGameTurn < getTurnForYear(1700):
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_HOLY_ROME_GERMAN_CONFEDERATION")
					return
			elif iPlayer == iCarthage:
				if capital.getX() < 73:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_CARTHAGE_DESC_DEMOCRATIC")
					return
			elif iPlayer == iMaya:
				if bReborn:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_COLOMBIA_DESC_DEMOCRATIC")
					return
		
		
			if iPlayer in self.democraticNames:
				if iPlayer in self.modernIslamNames and iReligion == iIslam:
					self.setCivDesc(iPlayer, self.modernIslamNames[iPlayer])
				else:
					self.setCivDesc(iPlayer, self.democraticNames[iPlayer])
				return
				
		# Handle other names specifically
		if iPlayer == iEgypt:
			if bResurrected and self.getResurrections(iPlayer) < 2:
				if bTheocracy and iReligion == iIslam:
					if iEra <= iIndustrial:
						if tPlayer.isHasTech(iGunpowder):
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_MAMLUK_CALIPHATE")
						elif pArabia.isAlive():
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_FATIMID_CALIPHATE")
						else:
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_AYYUBID_CALIPHATE")
						return
				elif iReligion == iIslam:
					if iEra <= iIndustrial:
						if tPlayer.isHasTech(iGunpowder):
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_MAMLUK_SULTANATE")
						elif pArabia.isAlive():
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_FATIMID_SULTANATE")
						else:
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_AYYUBID_SULTANATE")
						return
				else:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_COPTIC")
					return
			else:
				if iGreece in lPreviousOwners:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_PTOLEMAIC")
					return
		
				if bCityStates:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_CITY_STATES")
					return
				
				if iEra == iAncient:
					if iAnarchyTurns == 0:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_OLD_KINGDOM")
					elif iAnarchyTurns == 1:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_MIDDLE_KINGDOM")
					else:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_NEW_KINGDOM")
					return
				elif iEra == iClassical:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_NEW_KINGDOM")
					return
					
		elif iPlayer == iIndia:
			if iReligion == iIslam:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_INDIA_SULTANATE")
				return
				
			if bEmpire and iEra <= iClassical:
				if iReligion == iBuddhism:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_INDIA_MAURYA")
					return
				elif iReligion == iHinduism:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_INDIA_GUPTA")
					return
		
			if bCityStates:
				if iEra <= iClassical:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_INDIA_MAHAJANAPADAS")
					return
					
			if bEmpire and iEra == iMedieval:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_INDIA_PALA")
				return
				
			if iEra >= iRenaissance:
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_INDIA_MARATHA_EMPIRE")
					return
					
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_INDIA_MARATHA")
				return
				
		elif iPlayer == iChina:
			if not bResurrected:
				if bEmpire:
					if iEra >= iIndustrial or utils.getScenario() == i1700AD:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_CHINA_QING")
						return
						
					if iEra == iRenaissance and iGameTurn >= getTurnForYear(1400):
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_CHINA_MING")
						return
						
					if iEra == iMedieval:
						#if iAnarchyTurns <= 2:
						#	self.setCivDesc(iPlayer, "TXT_KEY_CIV_CHINA_SUI")
						if teamChina.isHasTech(iPaper) and teamChina.isHasTech(iGunpowder):
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_CHINA_SONG")
						elif iGameTurn >= getTurnForYear(600):
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_CHINA_TANG")
						else:
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_CHINA_SUI")
						return
						
					if iEra == iClassical:
						if iGameTurn < getTurnForYear(0):
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_CHINA_QIN")
						else:
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_CHINA_HAN")
						return
				
					if iEra == iAncient:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_CHINA_ZHOU")
						return
			else:
				if bEmpire:
					if iGameTurn < getTurnForYear(tBirth[iMongolia]):
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_CHINA_SONG")
					elif iEra <= iRenaissance:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_CHINA_MING")
					else:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_CHINA_QING")
					return
					
		elif iPlayer == iBabylonia:
			if bCityStates and not bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_BABYLONIA_CITY_STATES")
				return
		
			if capital.getName() == "Ninova" or capital.getName() == "Kalhu":
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_BABYLONIA_ASSYRIA")
				return
		
			if bEmpire and iEra > iAncient:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_BABYLONIA_NEO_EMPIRE")
				return
				
		elif iPlayer == iGreece:
			if bCityStates:
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_GREECE_EMPIRE")
					return
					
				if bWar:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_GREECE_LEAGUE")
				else:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_GREECE_CITY_STATES")
				return
				
			if iEra <= iClassical:
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_GREECE_MACEDONIA_EMPIRE")
				else:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_GREECE_MACEDONIA_KINGDOM")
				return
				
			if bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_GREECE_EMPIRE")
				return
				
		elif iPlayer == iPersia:
			if not bReborn:
				if bEmpire and iReligion == iZoroastrianism:
					if iGameEra < iMedieval:
						if bResurrected:
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_PERSIA_PARTHIA")
						else:
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_PERSIA_ACHAEMENID")
						return
					elif iGameEra == iMedieval:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_PERSIA_SASSANID")
						return
					else:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_PERSIA_EMPIRE")
						return
			else:
				if bEmpire:
					if iEra <= iRenaissance:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_PERSIA_SAFAVID_EMPIRE")
					elif iEra == iIndustrial:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_PERSIA_QAJAR_EMPIRE")
					else:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_PERSIA_PAHLAVI_EMPIRE")
					return
					
		elif iPlayer == iCarthage:	# change adjectives and short desc here too
			if capital.getX() >= 66:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_PHOENICIA_CITY_STATES")
				self.setCivShortDesc(iPlayer, "TXT_KEY_CIV_PHOENICIA_SHORT_DESC")
				self.setCivAdjective(iPlayer, "TXT_KEY_CIV_PHOENICIA_ADJECTIVE")
				return
				
			self.setCivShortDesc(iPlayer, "TXT_KEY_CIV_CARTHAGE_SHORT_DESC")
			self.setCivAdjective(iPlayer, "TXT_KEY_CIV_CARTHAGE_ADJECTIVE")
				
			if bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_CARTHAGE_EMPIRE")
				return
		
			if bCityStates:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_CARTHAGE_CITY_STATES")
				return
			# make Carthaginian Kingdom default
			
		elif iPlayer == iPolynesia:
			if capital.getName() in ["Kaua'i", "O'ahu", "Maui"]:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_POLYNESIA_HAWAII")
				return
			
			if bEmpire:
				if capital.getName() == "Manu'a": self.setCivDesc(iPlayer, "TXT_KEY_CIV_POLYNESIA_EMPIRE_SAMOA")
				else: self.setCivDesc(iPlayer, "TXT_KEY_CIV_POLYNESIA_EMPIRE")
				return
				
			if capital.getName() == "Manu'a": self.setCivDesc(iPlayer, "TXT_KEY_CIV_POLYNESIA_SAMOA")
			elif capital.getName() == "Niue": self.setCivDesc(iPlayer, "TXT_KEY_CIV_POLYNESIA_NIUE")
			
			# Kingdom of Tonga as default
			
		elif iPlayer == iRome:
			if pByzantium.isAlive():
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_ROME_WESTERN_EMPIRE")
				return
		
			if bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_ROME_EMPIRE")
				return
				
			if bCityStates:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_ROME_REPUBLIC")
				return
					
		elif iPlayer == iJapan:
			if bEmpire or iCivic1 == iCivicAbsolutism or iEra >= iIndustrial: # Absolutism
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_JAPAN_EMPIRE")
				return
				
			# make Shogunate default
			
		elif iPlayer == iTamils:
			if iEra >= iRenaissance:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_TAMILS_MYSORE")
				return
				
			if iEra >= iMedieval:
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_TAMILS_VIJAYANAGARA_EMPIRE")
					return
			
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_TAMILS_VIJAYANAGARA")
				return
				
			if bEmpire:
				if capital.getName() in ["Madurai", "Thiruvananthapuram"]:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_TAMILS_PANDYAN_EMPIRE")
					return
					
				if capital.getName() in ["Cochin", "Kozhikode"]:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_TAMILS_CHERA_EMPIRE")
					return
					
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_TAMILS_CHOLA_EMPIRE")
				return
				
			if capital.getName() in ["Madurai", "Thiruvananthapuram"]:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_TAMILS_PANDYAN_KINGDOM")
				return
				
			if capital.getName() in ["Cochin", "Kozhikode"]:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_TAMILS_CHERA_KINGDOM")
				return
				
			# Chola Kingdom default
				
		elif iPlayer == iEthiopia:
			if not gc.getGame().isReligionFounded(iIslam):
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_ETHIOPIA_AKSUM")
				return
				
			if bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_ETHIOPIA_EMPIRE")
				return
				
			# make Ethiopian Kingdom default
			
		elif iPlayer == iKorea:		# difference Goryeo and Joseon with religion?
			if iEra < iMedieval:
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_KOREA_GOGURYEO")
					return
			if iEra < iRenaissance:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_KOREA_GORYEO")
				return
			else:
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_KOREA_EMPIRE")
				else:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_KOREA_JOSEON")
				return
				
		#elif iPlayer == iMaya: # city states are default
		elif iPlayer == iMaya:
			if bReborn:
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_COLOMBIA_EMPIRE")
					return
					
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_COLOMBIA_DESC_DEFAULT")
				return
				
		elif iPlayer == iByzantium:
			if pRome.isAlive() and not pRome.isReborn():
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_BYZANTIUM_EASTERN_EMPIRE")
				return
				
			if capital.getName() == "Trapezounta":
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_BYZANTIUM_TREBIZOND_EMPIRE")
				return
			elif capital.getName() == "Dyrrachion":
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_BYZANTIUM_EPIRUS_DESPOTATE")
				return
			elif capital.getName() == "Athina":
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_BYZANTIUM_MOREA_DESPOTATE")
				return
			elif capital.getName() != "Konstantinoupolis":
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_BYZANTIUM_NICAEA_EMPIRE")
				return
				
		elif iPlayer == iVikings:
			if iReligion == -1 and not teamVikings.isHasTech(iLiberalism):
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_VIKINGS_NORSE_KINGDOMS")
				return
			else:
				if bEmpire:
					if iEra <= iMedieval:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_VIKINGS_KALMAR_UNION")
					elif iEra == iRenaissance or capital.getName() == "Stockholm":
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_VIKINGS_SWEDISH_EMPIRE")
					else:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_VIKINGS_DENMARK_NORWAY")
					return
				else:
					if capital.getName() == "Oslo" or capital.getName() == "Trondheim" or capital.getName() == "Nidaros":
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_VIKINGS_NORWAY")
						return
					elif capital.getName() == "Stockholm" or capital.getName() == "Kalmar":
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_VIKINGS_SWEDEN")
						return
					elif capital.getName() == "Kobenhavn" or capital.getName() == "Roskilde":
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_VIKINGS_DENMARK")
						return
						
		elif iPlayer == iArabia:
			if bResurrected:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_ARABIA_SAUDI")
				return
		
			if iReligion == iIslam and bTheocracy:
				if not bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_ARABIA_RASHIDUN_CALIPHATE")
				else:
					if capital.getName() == "Dimashq":
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_ARABIA_UMMAYAD_CALIPHATE")
					else:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_ARABIA_ABBASID_CALIPHATE")
				return
				
			# Arabian Sultanates as default, Arabian leaders should prefer Theocracy
			
		elif iPlayer == iTibet:
			if bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_TIBET_EMPIRE")
				return
				
			# Kingdom of Tibet as default
			
		elif iPlayer == iKhmer:
			if iEra <= iRenaissance and capital.getName() == "Angkor":
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_KHMER_EMPIRE")
				return
			elif capital.getName() == "Hanoi":
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_KHMER_VIETNAM")
				return
			elif capital.getName() == "Pagan":
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_KHMER_BURMA")
				return
			elif capital.getName() == "Dali":
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_KHMER_NANZHAO")
				return
				
			# Kingdom of Cambodia default
				
		elif iPlayer == iIndonesia:
			if iReligion == iIslam:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_INDONESIA_MATARAM")
				return
		
			if iEra <= iRenaissance:
				if not bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_INDONESIA_SRIVIJAYA")
				else:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_INDONESIA_MAJAPAHIT")
				return
			
			# generic name as default
			
		elif iPlayer == iMoors:
			bAndalusia = utils.isPlotInArea(tCapitalCoords, vic.tIberiaTL, vic.tIberiaBR)
			
			if bCityStates:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_MOORS_TAIFAS")
				return
				
			if bAndalusia:
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_MOORS_CALIPHATE")
					return
					
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_MOORS_CORDOBA")
				return
				
			if bEmpire and iEra <= iRenaissance:
				if bTheocracy and iReligion == iIslam:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_MOORS_ALMOHAD_CALIPHATE")
					return
					
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_MOORS_ALMOHAD_EMPIRE")
				return
				
			# Kingdom of Morocco as default

		elif iPlayer == iSpain:
			if iReligion == iIslam:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_SPAIN_SULTANATE")
				return
				
			bSpain = True
			if pMoors.isAlive():
				moorishCapital = gc.getPlayer(iMoors).getCapitalCity()
				if utils.isPlotInArea((moorishCapital.getX(), moorishCapital.getY()), vic.tIberiaTL, vic.tIberiaBR):
					bSpain = False
				
			if bEmpire and iEra > iMedieval:
				if bSpain:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_SPAIN_EMPIRE")
					return
					
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_SPAIN_CASTILIAN_EMPIRE")
				return
				
			if (capital.getName() == "Barcelona" or capital.getName() == "Valencia") and iEra == iMedieval:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_SPAIN_ARAGON")
				return
				
			bSpain = True
			if pMoors.isAlive():
				moorishCapital = gc.getPlayer(iMoors).getCapitalCity()
				if utils.isPlotInArea((moorishCapital.getX(), moorishCapital.getY()), vic.tIberiaTL, vic.tIberiaBR):
					bSpain = False
			
			if iGameTurn > getTurnForYear(tBirth[iPortugal]):
				if not pPortugal.isAlive() and bSpain:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_SPAIN_IBERIA")
					return
			
				pPortugueseCapital = gc.getPlayer(iPortugal).getCapitalCity()	
				if not utils.isPlotInArea((pPortugueseCapital.getX(), pPortugueseCapital.getY()), tCoreAreasTL[0][iPortugal], tCoreAreasBR[0][iPortugal], tExceptions[0][iPortugal]) and bSpain:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_SPAIN_IBERIA")
					return
		
			if not bSpain:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_SPAIN_CASTILLE")
				return
				
		elif iPlayer == iFrance:
			#if capital.getName() == "Nouvelle Orl&#233;ans":
			#	self.setCivDesc(iPlayer, "TXT_KEY_CIV_FRANCE_LOUISIANA")
			#	return
				
			#if utils.isPlotInArea(tCapitalCoords, tNCAmericaTL, tNCAmericaBR):
			#	self.setCivDesc(iPlayer, "TXT_KEY_CIV_FRANCE_QUEBEC")
			#	return
		
			if not utils.isPlotInArea(tCapitalCoords, tCoreAreasTL[0][iFrance], tCoreAreasBR[0][iFrance], tExceptions[0][iFrance]):
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_FRANCE_EXILE")
				return
		
			if (iEra > iRenaissance and bEmpire) or iCivic0 == iCivicAutocracy:	# Autocracy
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_FRANCE_EMPIRE")
				return
				
			if not pHolyRome.isAlive() and iEra == iMedieval:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_FRANCE_FRANKISH_EMPIRE")
				return
				
		elif iPlayer == iEngland:
			if not utils.isPlotInArea(tCapitalCoords, tCoreAreasTL[0][iEngland], tCoreAreasBR[0][iEngland], tExceptions[0][iEngland]):
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_ENGLAND_EXILE")
				return
		
			if iEra < iIndustrial:
				if utils.getMaster(iFrance) == iEngland:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_ENGLAND_ANGEVIN_EMPIRE")
					return
			
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_ENGLAND_GREAT_BRITAIN")
					return
			else:
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_ENGLAND_EMPIRE")
				else:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_ENGLAND_UNITED_KINGDOM")
				return
				
		elif iPlayer == iHolyRome:
			if bEmpire:
				if pGermany.isAlive():
					if iCivic1 == iCivicRepresentation:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_HOLY_ROME_AUSTRIA_HUNGARY")
						return
						
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_HOLY_ROME_AUSTRIA_EMPIRE")
					return
					
				lEuroCivs = [iVikings, iSpain, iFrance, iEngland, iRome, iItaly, iPoland, iPortugal, iNetherlands]
				iCounter = 0
				
				for iLoopCiv in lEuroCivs:
					if utils.getMaster(iLoopCiv) == iHolyRome:
						iCounter += 1
						
				if iCounter >= 2:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_HOLY_ROME_HABSBURG_EMPIRE")
					return
				
				if iEra <= iRenaissance:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_HOLY_ROME_HRE")
					return
			
			if pGermany.isAlive():
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_HOLY_ROME_AUSTRIA_ARCHDUCHY")
				return
				
			# Kingdom of Germany as default
			
		elif iPlayer == iRussia:
			if bEmpire and iEra > iMedieval:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_RUSSIA_EMPIRE")
				return
		
			if iEra == iMedieval and not bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_RUSSIA_MUSCOVY")
				return
				
		elif iPlayer == iNetherlands:
			if bCityStates:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_NETHERLANDS_DESC_DEMOCRATIC")
				return
		
			if not utils.isPlotInArea(tCapitalCoords, tCoreAreasTL[0][iNetherlands], tCoreAreasBR[0][iNetherlands], tExceptions[0][iNetherlands]):
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_NETHERLANDS_EXILE")
				return
		
			if iEra < iIndustrial:
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_NETHERLANDS_UNITED_KINGDOM")
					return
			else:
				if bEmpire and not bCityStates:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_NETHERLANDS_EMPIRE")
					return
		
			if bCityStates:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_NETHERLANDS_DESC_DEMOCRATIC")
				return

			# Kingdom as default
			
		elif iPlayer == iMali:
			if bResurrected:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_MALI_SONGHAI")
				return
				
			# Empire as default
			
		elif iPlayer == iPoland:
			if bEmpire and iEra >= iRenaissance:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_POLAND_EMPIRE")
				return
				
			if capital.getName() == 'Kowno' or capital.getName() == 'Medvegalis' or capital.getName() == 'Klajpeda' or capital.getName == 'Wilno' or capital.getName() == 'Riga':
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_POLAND_LITHUANIA")
				return
				
			# Kingdom as default
			
		elif iPlayer == iPortugal:
			if utils.isPlotInArea(tCapitalCoords, tBrazilTL, tBrazilBR) and not gc.getPlayer(iBrazil).isAlive():
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_PORTUGAL_BRAZIL")
				return
				
			if not utils.isPlotInArea(tCapitalCoords, vic.tIberiaTL, vic.tIberiaBR):
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_PORTUGAL_EXILE")
				return
		
			if bEmpire and iEra > iRenaissance:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_PORTUGAL_EMPIRE")
				return
				
			# Kingdom as default
			
		elif iPlayer == iInca:
			if bResurrected:
				if capital.getName() == 'La Paz':
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_INCA_BOLIVIA")
					return
					
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_INCA_PERU")
				return
		
			if bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_INCA_EMPIRE")
				return
				
			# Kingdom of Cuzco as default
			
		elif iPlayer == iItaly:
			if bCityStates:
				if bWar:
					if bEmpire:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_ITALY_ITALIAN_LEAGUE")
					else:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_ITALY_LOMBARD_LEAGUE")
				else:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_ITALY_MARITIME_REPUBLICS")
				return
			else:
				if bEmpire or bResurrected:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_ITALY_KINGDOM")
				else:
					if capital.getName() == "Fiorenza" or capital.getName() == "Firenze":
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_ITALY_DUCHY_TUSCANY")
					elif capital.getName() == "Venezia":
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_ITALY_DUCHY_VENICE")
					elif capital.getName() == "Milano":
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_ITALY_DUCHY_MILAN")
					elif capital.getName() == "Roma":
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_ITALY_PAPAL_STATE")
					else:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_ITALY_KINGDOM")
				return
			
		elif iPlayer == iMongolia:
			if bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_MONGOLIA_EMPIRE")
				return
				
			if capital.getX() >= 99 and capital.getY() <= 43:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_MONGOLIA_YUAN")
				return
				
			if capital.getName() == 'Samarkand' or capital.getName() == 'Samarqand' or capital.getName() == 'Merv' or capital.getName() == 'Marv':
				if pMongolia.getStateReligion() == iIslam:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_MONGOLIA_TIMURID")
				else:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_MONGOLIA_CHAGATAI")
				return
		
			if iEra == iMedieval:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_MONGOLIA_KHAMAG")
				return
					
			# Mongol State as default
			
		elif iPlayer == iAztecs:
			if bResurrected:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_MEXICO_EMPIRE")
				return
		
			if bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_AZTECS_EMPIRE")
				return
		
			if bCityStates:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_AZTECS_ALTEPETL")
				return
				
			# Triple Alliance as default
			
		elif iPlayer == iMughals:
			if iEra == iMedieval and not bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_MUGHALS_DELHI")
				return
				
			# Mughal Empire as default
			
		elif iPlayer == iTurkey:
			if iReligion != iIslam:
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_TURKEY_EMPIRE")
					return
			
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_TURKEY_OTTOMAN_STATE")
				return
		
			if bTheocracy:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_TURKEY_OTTOMAN_CALIPHATE")
				return
				
			if bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_TURKEY_OTTOMAN_EMPIRE")
				return
				
			# Ottoman Sultanate as default
			
		elif iPlayer == iThailand:
			if iEra <= iRenaissance:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_THAILAND_AYUTTHAYA")
				return
			else:
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_THAILAND_EMPIRE")
					return
					
			# Siam as default
			
		elif iPlayer == iGermany:
			if bEmpire and iEra > iRenaissance:
				if utils.getMaster(iHolyRome) == iGermany:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_GERMANY_GREATER_EMPIRE")
					return
					
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_GERMANY_EMPIRE")
				return
				
			# Kingdom of Prussia as default
			
		elif iPlayer == iAmerica:
			if iCivic2 == iCivicSlavery or iCivic2 == iCivicAgrarianism:	# Slavery/Agrarianism
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_AMERICA_CSA")
				return
				
			# Empire of Columbia as default
			
		elif iPlayer == iArgentina:
			if bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_ARGENTINA_EMPIRE")
				return
				
			if tCapitalCoords != tCapitals[0][iArgentina]:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_ARGENTINA_CONFEDERATION")
				return
			
			
		elif iPlayer == iBrazil:
			if bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_BRAZIL_EMPIRE")
				return
		
		#if iPlayer == iCarthage:
		#	self.setCivName(iPlayer, self.defaultNames[iPlayer], "TXT_KEY_CIV_CARTHAGE_SHORT_DESC", "TXT_KEY_CIV_CARTHAGE_ADJECTIVE")
		#elif iPlayer == iHolyRome:
		#	self.setCivName(iPlayer, self.defaultNames[iPlayer], "TXT_KEY_CIV_GERMANY_SHORT_DESC", "TXT_KEY_CIV_GERMANY_ADJECTIVE")
			
		self.setCivDesc(iPlayer, self.defaultNames[iPlayer])
				
	
	def checkLeader(self, iPlayer):
        
                if iPlayer >= iNumPlayers: return
		
		if not gc.getPlayer(iPlayer).isAlive(): return
		
		if gc.getPlayer(iPlayer).isHuman(): return
		
                pPlayer = gc.getPlayer(iPlayer)
                tPlayer = gc.getTeam(pPlayer.getTeam())
                bReborn = pPlayer.isReborn()
                iReligion = pPlayer.getStateReligion()
                capital = gc.getPlayer(iPlayer).getCapitalCity()
                tCapitalCoords = (capital.getX(), capital.getY())
                iCivic0 = pPlayer.getCivics(0)
                iCivic1 = pPlayer.getCivics(1)
                iCivic2 = pPlayer.getCivics(2)
                iCivic3 = pPlayer.getCivics(3)
                iCivic4 = pPlayer.getCivics(4)
                iGameTurn = gc.getGame().getGameTurn()
		bEmpire = self.isEmpire(iPlayer)
		bCityStates = (iCivic0 == iCivicCityStates or not gc.getTeam(pPlayer.getTeam()).isHasTech(iCodeOfLaws))
		bTheocracy = (iCivic0 == iCivicTheocracy)
		bResurrected = (self.getResurrections(iPlayer) > 0)
		bMonarchy = not (self.isCommunist(iPlayer) or self.isFascist(iPlayer) or self.isDemocratic(iPlayer))
		iAnarchyTurns = self.getAnarchyTurns(iPlayer)
		iEra = pPlayer.getCurrentEra()
		iGameEra = gc.getGame().getCurrentEra()
		
		
		if iPlayer == iEgypt:
		
			if not bMonarchy and iEra >= iModern:
				self.setLeader(iPlayer, iNasser)
				return
			
			if bResurrected or utils.getScenario() >= i600AD:
				self.setLeader(iPlayer, iBaibars)
				return
				
			if tPlayer.isHasTech(iLiterature):
				self.setLeader(iPlayer, iCleopatra)
				return
				
		elif iPlayer == iIndia:
		
			if not bMonarchy and iEra >= iModern:
				self.setLeader(iPlayer, iGandhi)
				return
				
			if iEra >= iRenaissance:
				self.setLeader(iPlayer, iShivaji)
				return
				
			if tPlayer.isHasTech(iCurrency):
				self.setLeader(iPlayer, iChandragupta)
				return
				
		elif iPlayer == iChina:
		
			if self.isCommunist(iPlayer) or self.isDemocratic(iPlayer) and iEra >= iIndustrial:
				self.setLeader(iPlayer, iMao)
				return
				
			#if iEra >= iIndustrial:
			#	self.setLeader(iPlayer, iCixi)
			#	return
				
			if (iEra >= iRenaissance and iGameTurn >= getTurnForYear(1400)) or bResurrected:
				self.setLeader(iPlayer, iHongwu)
				return
				
			if iEra >= iMedieval:
				self.setLeader(iPlayer, iTaizong)
				return
				
		elif iPlayer == iBabylonia:
		
			if iGameTurn >= getTurnForYear(-1600):
				self.setLeader(iPlayer, iHammurabi)
				return
				
		elif iPlayer == iGreece:
		
			if bEmpire or not bCityStates:
				self.setLeader(iPlayer, iAlexander)
				return
				
		elif iPlayer == iPersia:
		
			if bReborn:
				if iEra >= iModern:
					self.setLeader(iPlayer, iKhomeini)
					return
					
				self.setLeader(iPlayer, iAbbas)
				return
			else:
				if bEmpire:
					self.setLeader(iPlayer, iDarius)
					return
					
		elif iPlayer == iCarthage:
		
			if capital.getName() == "Qart-Hadasht" or bEmpire or not bCityStates:
				self.setLeader(iPlayer, iHannibal)
				return
				
		elif iPlayer == iRome:
		
			if bReborn:
				self.setLeader(iPlayer, iCavour)
				return
			else:
				if bEmpire or not bCityStates:
					self.setLeader(iPlayer, iAugustus)
					return
				
		elif iPlayer == iJapan:
		
			if iEra >= iIndustrial:
				self.setLeader(iPlayer, iMeiji)
				return
				
			if tPlayer.isHasTech(iFeudalism):
				self.setLeader(iPlayer, iTokugawa)
				return
				
		elif iPlayer == iEthiopia:
		
			if iEra >= iIndustrial:
				self.setLeader(iPlayer, iHaileSelassie)
				return
				
		elif iPlayer == iTamils:
		
			if iEra >= iRenaissance:
				self.setLeader(iPlayer, iKrishnaDevaRaya)
				return
				
		elif iPlayer == iKorea:
			return
			
		elif iPlayer == iMaya:
			return
			
		elif iPlayer == iByzantium:
			
			if iGameTurn >= getTurnForYear(1000):
				self.setLeader(iPlayer, iBasil)
				return
			
		elif iPlayer == iVikings:
		
			if iEra >= iRenaissance:
				self.setLeader(iPlayer, iGustav)
				return
				
		elif iPlayer == iArabia:
		
			if iGameTurn >= getTurnForYear(1000):
				self.setLeader(iPlayer, iSaladin)
				return
				
		elif iPlayer == iTibet:
		
			if iGameTurn >= getTurnForYear(1500):
				self.setLeader(iPlayer, iLobsangGyatso)
				return
				
		elif iPlayer == iKhmer:
			return
			
		elif iPlayer == iIndonesia:
			
			if iEra >= iModern:
				self.setLeader(iPlayer, iSuharto)
				return
				
			if bEmpire:
				self.setLeader(iPlayer, iHayamWuruk)
				return
				
		elif iPlayer == iMoors:
			
			bAndalusia = utils.isPlotInArea(tCapitalCoords, vic.tIberiaTL, vic.tIberiaBR)
			
			if not bAndalusia:
				self.setLeader(iPlayer, iYaqub)
				return
				
		elif iPlayer == iSpain:
		
			if self.isFascist(iPlayer):
				self.setLeader(iPlayer, iFranco)
				return
		
			if sd.scriptDict['lFirstContactConquerors'][0] == 1 or sd.scriptDict['lFirstContactConquerors'][1] == 1 or sd.scriptDict['lFirstContactConquerors'][2] == 1:
				self.setLeader(iPlayer, iPhilip)
				return
				
		elif iPlayer == iFrance:
		
			if iEra >= iModern:
				self.setLeader(iPlayer, iDeGaulle)
				return
				
			if iEra >= iIndustrial or tPlayer.isHasTech(iNationalism):
				self.setLeader(iPlayer, iNapoleon)
				return
				
			if iEra >= iRenaissance:
				self.setLeader(iPlayer, iLouis)
				return
				
		elif iPlayer == iEngland:
		
			if iEra >= iModern:
				self.setLeader(iPlayer, iChurchill)
				return
				
			if iEra >= iIndustrial or utils.getScenario() == i1700AD:
				self.setLeader(iPlayer, iVictoria)
				return
				
			if iEra >= iRenaissance:
				self.setLeader(iPlayer, iElizabeth)
				return
				
		elif iPlayer == iHolyRome:
		
			if iEra >= iIndustrial or utils.getScenario() == i1700AD:
				self.setLeader(iPlayer, iFrancis)
				return
		
			if iEra >= iRenaissance:
				self.setLeader(iPlayer, iCharles)
				return
				
		elif iPlayer == iRussia:
		
			if not bMonarchy and iEra >= iIndustrial:
				self.setLeader(iPlayer, iStalin)
				if self.isCommunist(iPlayer):
                                        cnm.applySovietNames()
				return
				
			if iEra >= iIndustrial:
				self.setLeader(iPlayer, iNicholas)
				return
				
			if iEra >= iRenaissance:
				if iGameTurn >= getTurnForYear(1750):
					self.setLeader(iPlayer, iCatherine)
					return
				
				self.setLeader(iPlayer, iPeter)
				return
				
		elif iPlayer == iNetherlands:
			return
			
		elif iPlayer == iMali:
			return
			
		elif iPlayer == iPoland:
		
			if iEra >= iRenaissance or utils.getScenario() == i1700AD:
				self.setLeader(iPlayer, iSobieski)
				return
			
		elif iPlayer == iPortugal:
		
			if iEra >= iIndustrial:
				self.setLeader(iPlayer, iMaria)
				return
			
			if tPlayer.isHasTech(iOptics):
				self.setLeader(iPlayer, iJoao)
				return
				
		elif iPlayer == iInca:
			return
			
		elif iPlayer == iItaly:
		
			if iEra >= iIndustrial:
				self.setLeader(iPlayer, iCavour)
				return
			
		elif iPlayer == iMongolia:
		
			if iGameTurn >= getTurnForYear(1400):
				self.setLeader(iPlayer, iKublaiKhan)
				return
				
		elif iPlayer == iAztecs:
			
			if pPlayer.isReborn():
				if bMonarchy or self.isFascist(iPlayer):
					self.setLeader(iPlayer, iSantaAnna)
					return
					
				if iEra >= iModern:
					self.setLeader(iPlayer, iCardenas)
					return
					
				self.setLeader(iPlayer, iJuarez)
				return
			
		elif iPlayer == iMughals:
			
			if tPlayer.isHasTech(iPatronage):
				self.setLeader(iPlayer, iAkbar)
				return
			
		elif iPlayer == iTurkey:
		
			if not bMonarchy and iEra >= iIndustrial:
				self.setLeader(iPlayer, iAtaturk)
				return
				
			if tPlayer.isHasTech(iPatronage):
				self.setLeader(iPlayer, iSuleiman)
				return
				
		elif iPlayer == iThailand:
		
			if iEra >= iIndustrial:
				self.setLeader(iPlayer, iMongkut)
				return
				
		elif iPlayer == iGermany:
		
			if self.isFascist(iPlayer):
				self.setLeader(iPlayer, iHitler)
				return
				
			if tPlayer.isHasTech(iNationalism):
				self.setLeader(iPlayer, iBismarck)
				return
				
		elif iPlayer == iAmerica:
		
			if iEra >= iModern:
				self.setLeader(iPlayer, iFranklinRoosevelt)
				return
				
			if iGameTurn >= getTurnForYear(1850):
				self.setLeader(iPlayer, iLincoln)
				return
				
		elif iPlayer == iArgentina:
		
			if iEra >= iModern:
				self.setLeader(iPlayer, iPeron)
				return
				
		elif iPlayer == iBrazil:
			return
				
		if utils.getScenario() == i600AD and iPlayer in self.lateStartingLeaders:
			self.setLeader(iPlayer, self.lateStartingLeaders[iPlayer])
			return
			
		if utils.getScenario() == i1700AD and iPlayer in self.l1700ADLeaders:
			self.setLeader(iPlayer, self.l1700ADLeaders[iPlayer])
			return
				
		self.setLeader(iPlayer, self.startingLeaders[iPlayer])
		

        def onCivRespawn(self, iPlayer, tOriginalOwners):
                #pPlayer = gc.getPlayer(iPlayer)
                #if tRebirthCiv[iPlayer] != -1:
                #        pPlayer.setCivilizationType(tRebirthCiv[iPlayer])
                #pPlayer.setLeader(tRebirthLeaders[iPlayer][0])
		
		print "On Respawn of Civ: "+str(iPlayer)
		
		self.changeResurrections(iPlayer, 1)
		
		if iPlayer == iAztecs:
			self.setCivAdjective(iPlayer, "TXT_KEY_CIV_MEXICO_ADJECTIVE")
			self.setCivShortDesc(iPlayer, "TXT_KEY_CIV_MEXICO_SHORT_DESC")
		elif iPlayer == iInca:
			self.setCivAdjective(iPlayer, "TXT_KEY_CIV_PERU_ADJECTIVE")
			self.setCivShortDesc(iPlayer, "TXT_KEY_CIV_PERU_SHORT_DESC")
		elif iPlayer == iHolyRome:
			self.setCivAdjective(iPlayer, "TXT_KEY_CIV_AUSTRIA_ADJECTIVE")
			self.setCivShortDesc(iPlayer, "TXT_KEY_CIV_AUSTRIA_SHORT_DESC")
			
		
                self.setCivDesc(iPlayer, self.defaultNames[iPlayer])
                self.checkName(iPlayer, tOriginalOwners)
		self.checkLeader(iPlayer)
                
        def onVassalState(self, argsList):
                iMaster, iVassal, bVassal, bCapitulated = argsList
		
		if iVassal == iAztecs:
			self.setCivAdjective(iVassal, "TXT_KEY_CIV_MEXICO_ADJECTIVE")
			self.setCivShortDesc(iVassal, "TXT_KEY_CIV_MEXICO_SHORT_DESC")
		elif iVassal == iInca:
			self.setCivAdjective(iVassal, "TXT_KEY_CIV_PERU_ADJECTIVE")
			self.setCivShortDesc(iVassal, "TXT_KEY_CIV_PERU_SHORT_DESC")
			
                self.checkName(iVassal)
        
        def onPlayerChangeStateReligion(self, argsList):
                iPlayer, iNewReligion, iOldReligion = argsList
		
		if iNewReligion in [iJudaism, iChristianity]:
			if iPlayer == iAztecs:
				self.setCivAdjective(iPlayer, "TXT_KEY_CIV_MEXICO_ADJECTIVE")
				self.setCivShortDesc(iPlayer, "TXT_KEY_CIV_MEXICO_SHORT_DESC")
			elif iPlayer == iInca:
				self.setCivAdjective(iPlayer, "TXT_KEY_CIV_PERU_ADJECTIVE")
				self.setCivShortDesc(iPlayer, "TXT_KEY_CIV_PERU_SHORT_DESC")
			
                self.checkName(iPlayer)

        def onRevolution(self, iPlayer):
		self.changeAnarchyTurns(iPlayer, 1)
	
                self.checkName(iPlayer)
                
        def onCityAcquired(self, argsList):
                iPreviousOwner, iNewOwner, city, bConquest, bTrade = argsList
                
		self.checkName(iPreviousOwner)
		self.checkName(iNewOwner)
		
                #if city.getNumRealBuilding(iPalace):
                #        self.checkName(iPreviousOwner)
                
                #if gc.getPlayer(iNewOwner).getNumCities() in [0, 1, 2, 3, 6]:
                #        self.checkName(iNewOwner)
		
	def onCityRazed(self, argsList):
		city, iPlayer = argsList
		
		self.checkName(iPlayer)
			
	def onCityBuilt(self, iOwner):
		self.checkName(iOwner)

        def checkTurn(self, iGameTurn): # called only once every ten turns
                for iPlayer in range(iNumPlayers):
                        self.checkName(iPlayer)
			self.checkLeader(iPlayer)