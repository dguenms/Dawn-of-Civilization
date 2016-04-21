# Dynamic Civs - edead

from CvPythonExtensions import *
import CvUtil
import PyHelpers
from Consts import *
import Victory as vic
from StoredData import sd
from RFCUtils import utils
import CityNameManager as cnm
import Areas

### Constants ###

gc = CyGlobalContext()
localText = CyTranslator()

tBrazilTL = (32, 14)
tBrazilBR = (43, 30)
tNCAmericaTL = (3, 33)
tNCAmericaBR = (37, 63)

tBritainTL = (48, 53)
tBritainBR = (54, 60)

tEuropeanRussiaTL = (68, 50)
tEuropeanRussiaBR = (80, 62)
tEuropeanRussiaExceptions = ((68, 59), (68, 60), (68, 61), (68, 62))
	
### Setup methods ###

def findCapitalLocations(dCapitals):
	dLocations = {}
	for iPlayer in dCapitals:
		for sCapital in dCapitals[iPlayer]:
			dLocations[sCapital] = cnm.findLocations(iPlayer, sCapital)
	return dLocations

### Dictionaries with text keys

dDefaultInsertNames = {
	iVikings : "TXT_KEY_CIV_VIKINGS_SCANDINAVIA",
	iKhmer : "TXT_KEY_CIV_KHMER_KAMPUCHEA",
	iNetherlands : "TXT_KEY_CIV_NETHERLANDS_ARTICLE",
	iTamils : "TXT_KEY_CIV_TAMILS_TAMIL_NADU",
	iMaya : "TXT_KEY_CIV_MAYA_YUCATAN",
	iThailand : "TXT_KEY_CIV_THAILAND_SIAM",
	iMoors : "TXT_KEY_CIV_MOORS_MOROCCO",
	iMughals : "TXT_KEY_CIV_MUGHALS_DELHI",
	iHarappa : "TXT_KEY_CIV_HARAPPA_INDUS",
}

dDefaultInsertAdjectives = {
	iVikings : "TXT_KEY_CIV_VIKINGS_SCANDINAVIAN",
	iKhmer : "TXT_KEY_CIV_KHMER_KAMPUCHEAN",
	iThailand : "TXT_KEY_CIV_THAILAND_SIAMESE",
	iMoors : "TXT_KEY_CIV_MOORS_MOROCCAN",
}

dSpecificVassalTitles = {
	iEgypt : {
		iPhoenicia : "TXT_KEY_CIV_EGYPTIAN_PHOENICIA",
		iEthiopia : "TXT_KEY_CIV_EGYPTIAN_ETHIOPIA",
	},
	iBabylonia : {
		iPhoenicia : "TXT_KEY_ADJECTIVE_TITLE",
	},
	iGreece : {
		iIndia : "TXT_KEY_CIV_GREEK_INDIA",
		iEgypt : "TXT_KEY_CIV_GREEK_EGYPT",
		iPersia : "TXT_KEY_CIV_GREEK_PERSIA",
	},
	iPersia : {
		iEgypt : "TXT_KEY_CIV_PERSIAN_EGYPT",
		iIndia : "TXT_KEY_CIV_PERSIAN_INDIA",
		iBabylonia : "TXT_KEY_CIV_PERSIAN_BABYLONIA",
		iGreece : "TXT_KEY_CIV_PERSIAN_GREECE",
		iEthiopia : "TXT_KEY_CIV_PERSIAN_ETHIOPIA",
		iArabia : "TXT_KEY_CIV_PERSIAN_ARABIA",
		iMongolia : "TXT_KEY_CIV_PERSIAN_MONGOLIA",
	},
	iJapan : {
		iChina : "TXT_KEY_CIV_JAPANESE_CHINA",
		iKorea : "TXT_KEY_CIV_JAPANESE_KOREA",
		iMongolia : "TXT_KEY_CIV_JAPANESE_MONGOLIA",
	},
	iByzantium : {
		iEgypt : "TXT_KEY_CIV_BYZANTINE_EGYPT",
		iBabylonia : "TXT_KEY_CIV_BYZANTINE_BABYLONIA",
		iGreece : "TXT_KEY_CIV_BYZANTINE_GREECE",
		iPhoenicia : "TXT_KEY_CIV_BYZANTINE_CARTHAGE",
		iPersia : "TXT_KEY_CIV_BYZANTINE_PERSIA",
		iRome : "TXT_KEY_CIV_BYZANTINE_ROME",
		iSpain : "TXT_KEY_CIV_BYZANTINE_SPAIN",
	},
	iVikings : {
		iEngland : "TXT_KEY_CIV_VIKING_ENGLAND",
		iRussia : "TXT_KEY_CIV_VIKING_RUSSIA",
	},
	iArabia : {
		iTurkey : "TXT_KEY_CIV_ARABIAN_TURKEY",
		iMughals : "TXT_KEY_CIV_ARABIAN_MUGHALS",
	},
	iSpain : {
		iPhoenicia : "TXT_KEY_CIV_SPANISH_CARTHAGE",
		iEthiopia : "TXT_KEY_CIV_SPANISH_ETHIOPIA",
		iMaya : "TXT_KEY_CIV_SPANISH_MAYA",
		iByzantium : "TXT_KEY_CIV_SPANISH_BYZANTIUM",
		iIndonesia : "TXT_KEY_CIV_SPANISH_INDONESIA",
		iMoors : "TXT_KEY_CIV_SPANISH_MOORS",
		iFrance : "TXT_KEY_CIV_SPANISH_FRANCE",
		iNetherlands : "TXT_KEY_ADJECTIVE_TITLE",
		iMali : "TXT_KEY_CIV_SPANISH_MALI",
		iPortugal : "TXT_KEY_CIV_SPANISH_PORTUGAL",
		iAmerica : "TXT_KEY_CIV_SPANISH_AMERICA",
		iArgentina : "TXT_KEY_CIV_SPANISH_ARGENTINA",
	},
	iFrance : {
		iEgypt : "TXT_KEY_MANDATE_OF",
		iBabylonia : "TXT_KEY_CIV_FRENCH_BABYLONIA",
		iGreece : "TXT_KEY_CIV_FRANCE_DEPARTEMENTS_OF",
		iPersia : "TXT_KEY_MANDATE_OF",
		iPhoenicia : "TXT_KEY_CIV_FRENCH_PHOENICIA",
		iItaly : "TXT_KEY_CIV_FRENCH_ITALY",
		iEthiopia : "TXT_KEY_CIV_FRENCH_ETHIOPIA",
		iByzantium : "TXT_KEY_CIV_FRENCH_BYZANTIUM",
		iVikings : "TXT_KEY_CIV_FRANCE_DEPARTEMENTS_OF",
		iArabia : "TXT_KEY_MANDATE_OF",
		iEngland : "TXT_KEY_CIV_FRENCH_ENGLAND",
		iSpain : "TXT_KEY_CIV_FRENCH_SPAIN",
		iHolyRome : "TXT_KEY_CIV_FRENCH_HOLY_ROME",
		iRussia : "TXT_KEY_CIV_FRANCE_DEPARTEMENTS_OF",
		iPoland : "TXT_KEY_CIV_FRENCH_POLAND",
		iNetherlands : "TXT_KEY_CIV_FRENCH_NETHERLANDS",
		iMali : "TXT_KEY_CIV_FRENCH_MALI",
		iPortugal : "TXT_KEY_CIV_FRANCE_DEPARTEMENTS_OF",
		iInca : "TXT_KEY_CIV_FRENCH_INCA",
		iAztecs : "TXT_KEY_CIV_FRENCH_AZTECS",
		iMughals : "TXT_KEY_MANDATE_OF",
		iTurkey : "TXT_KEY_MANDATE_OF",
		iAmerica : "TXT_KEY_CIV_FRENCH_AMERICA",
	},
	iEngland : {
		iEgypt : "TXT_KEY_MANDATE_OF",
		iIndia : "TXT_KEY_CIV_ENGLISH_INDIA",
		iBabylonia : "TXT_KEY_CIV_ENGLISH_BABYLONIA",
		iPersia : "TXT_KEY_MANDATE_OF",
		iPhoenicia : "TXT_KEY_CIV_ENGLISH_PHOENICIA",
		iEthiopia : "TXT_KEY_CIV_ENGLISH_ETHIOPIA",
		iMaya : "TXT_KEY_CIV_ENGLISH_MAYA",
		iByzantium : "TXT_KEY_CIV_ENGLISH_BYZANTIUM",
		iVikings : "TXT_KEY_CIV_ENGLISH_VIKINGS",
		iArabia : "TXT_KEY_MANDATE_OF",
		iFrance : "TXT_KEY_CIV_ENGLISH_FRANCE",
		iHolyRome : "TXT_KEY_CIV_ENGLISH_HOLY_ROME",
		iGermany : "TXT_KEY_CIV_ENGLISH_GERMANY",
		iNetherlands : "TXT_KEY_CIV_ENGLISH_NETHERLANDS",
		iMali : "TXT_KEY_CIV_ENGLISH_MALI",
		iTurkey : "TXT_KEY_MANDATE_OF",
		iAmerica : "TXT_KEY_CIV_ENGLISH_AMERICA",
	},
	iHolyRome : {
		iItaly : "TXT_KEY_CIV_HOLY_ROMAN_ITALY",
		iFrance : "TXT_KEY_CIV_HOLY_ROMAN_FRANCE",
		iNetherlands : "TXT_KEY_CIV_HOLY_ROMAN_NETHERLANDS",
		iByzantium : "TXT_KEY_CIV_HOLY_ROMAN_BYZANTIUM",
		iPoland : "TXT_KEY_CIV_HOLY_ROMAN_POLAND",
	},
	iRussia : {
		iPoland : "TXT_KEY_CIV_RUSSIAN_POLAND",
		iAmerica : "TXT_KEY_ADJECTIVE_TITLE",
	},
	iNetherlands : {
		iIndonesia : "TXT_KEY_CIV_DUTCH_INDONESIA",
		iMali : "TXT_KEY_CIV_DUTCH_MALI",
		iEthiopia : "TXT_KEY_CIV_DUTCH_ETHIOPIA",
	},
	iPortugal : {
		iIndia : "TXT_KEY_CIV_PORTUGUESE_INDIA",
		iIndonesia : "TXT_KEY_CIV_PORTUGUESE_INDIA",
	},
	iMongolia : {
		iEgypt : "TXT_KEY_CIV_MONGOL_ILKHANATE",
		iChina : "TXT_KEY_CIV_MONGOL_CHINA",
		iBabylonia : "TXT_KEY_CIV_MONGOL_BABYLONIA",
		iGreece : "TXT_KEY_CIV_MONGOL_ILKHANATE",
		iPersia : "TXT_KEY_CIV_MONGOL_ILKHANATE",
		iPhoenicia : "TXT_KEY_CIV_MONGOL_PHOENICIA",
		iRome : "TXT_KEY_CIV_MONGOL_ILKHANATE",
		iByzantium : "TXT_KEY_CIV_MONGOL_BYZANTIUM",
		iRussia : "TXT_KEY_CIV_MONGOL_RUSSIA",
		iTurkey : "TXT_KEY_CIV_MONGOL_TURKEY",
		iMughals : "TXT_KEY_CIV_MONGOL_MUGHALS",
	},
	iMughals : {
		iIndia : "TXT_KEY_CIV_MUGHAL_INDIA",
	},
	iTurkey : {
		iEgypt : "TXT_KEY_CIV_TURKISH_EGYPT",
		iBabylonia : "TXT_KEY_CIV_TURKISH_BABYLONIA",
		iPersia : "TXT_KEY_CIV_TURKISH_PERSIA",
		iGreece : "TXT_KEY_CIV_TURKISH_GREECE",
		iPhoenicia : "TXT_KEY_CIV_TURKISH_PHOENICIA",
		iEthiopia : "TXT_KEY_CIV_TURKISH_ETHIOPIA",
		iByzantium : "TXT_KEY_CIV_TURKISH_BYZANTIUM",
		iArabia : "TXT_KEY_CIV_TURKISH_ARABIA",
		iRussia : "TXT_KEY_CIV_TURKISH_RUSSIA",
	},
	iGermany : {
		iHolyRome : "TXT_KEY_CIV_GERMAN_HOLY_ROME",
		iMali : "TXT_KEY_CIV_GERMAN_MALI",
		iEthiopia : "TXT_KEY_CIV_GERMAN_ETHIOPIA",
		iPoland : "TXT_KEY_CIV_GERMAN_POLAND",
	},
	iAmerica : {
		iEngland : "TXT_KEY_CIV_AMERICAN_ENGLAND",
		iJapan : "TXT_KEY_CIV_AMERICAN_JAPAN",
		iGermany : "TXT_KEY_CIV_AMERICAN_GERMANY",
		iAztecs : "TXT_KEY_CIV_AMERICAN_MEXICO",
		iMaya : "TXT_KEY_CIV_AMERICAN_MAYA",
		iKorea : "TXT_KEY_CIV_AMERICAN_KOREA",
	},
	iBrazil : {
		iArgentina : "TXT_KEY_CIV_BRAZILIAN_ARGENTINA",
	},
}

dMasterTitles = {
	iChina : "TXT_KEY_CIV_CHINESE_VASSAL",
	iPersia : "TXT_KEY_CIV_PERSIAN_VASSAL",
	iRome : "TXT_KEY_CIV_ROMAN_VASSAL",
	iJapan : "TXT_KEY_CIV_JAPANESE_VASSAL",
	iByzantium : "TXT_KEY_CIV_BYZANTINE_VASSAL",
	iArabia : "TXT_KEY_CIV_ARABIAN_VASSAL",
	iMoors : "TXT_KEY_CIV_ARABIAN_VASSAL",
	iSpain : "TXT_KEY_CIV_SPANISH_VASSAL",
	iFrance : "TXT_KEY_ADJECTIVE_TITLE",
	iEngland : "TXT_KEY_CIV_ENGLISH_VASSAL",
	iNetherlands : "TXT_KEY_ADJECTIVE_TITLE",
	iPortugal : "TXT_KEY_ADJECTIVE_TITLE",
	iMongolia : "TXT_KEY_CIV_MONGOL_VASSAL",
	iTurkey : "TXT_KEY_CIV_TURKISH_VASSAL",
}

dCommunistVassalTitlesGeneric = {
	iRussia : "TXT_KEY_CIV_RUSSIA_SOVIET",
}

dCommunistVassalTitles = {
	iRussia : {
		iChina : "TXT_KEY_CIV_RUSSIA_SOVIET_REPUBLIC_ADJECTIVE",
		iJapan : "TXT_KEY_CIV_RUSSIA_SOVIET_JAPAN",
		iTurkey : "TXT_KEY_CIV_RUSSIA_SOVIET_TURKEY",
		iGermany : "TXT_KEY_CIV_RUSSIA_SOVIET_GERMANY",
	},
}

dFascistVassalTitlesGeneric = {
	iGermany : "TXT_KEY_ADJECTIVE_TITLE"
}

dFascistVassalTitles = {
	iGermany : {
		iEgypt : "TXT_KEY_CIV_GERMANY_REICHSPROTEKTORAT",
		iChina : "TXT_KEY_CIV_GERMANY_REICHSKOMMISSARIAT",
		iGreece : "TXT_KEY_CIV_GERMANY_NAZI_GREECE",
		iPhoenicia : "TXT_KEY_CIV_GERMANY_REICHSKOMMISSARIAT",
		iRome : "TXT_KEY_CIV_GERMANY_REICHSPROTEKTORAT",
		iEthiopia : "TXT_KEY_CIV_GERMANY_NAZI_ETHIOPIA",
		iByzantium : "TXT_KEY_CIV_GERMANY_NAZI_BYZANTIUM",
		iSpain : "TXT_KEY_CIV_GERMANY_REICHSKOMMISSARIAT",
		iFrance : "TXT_KEY_CIV_GERMANY_NAZI_FRANCE",
		iEngland : "TXT_KEY_CIV_GERMANY_REICHSKOMMISSARIAT",
		iHolyRome : "TXT_KEY_CIV_GERMANY_NAZI_HOLY_ROME",
		iRussia : "TXT_KEY_CIV_GERMANY_NAZI_RUSSIA",
		iNetherlands : "TXT_KEY_CIV_GERMANY_NAZI_NETHERLANDS",
		iMali : "TXT_KEY_CIV_GERMANY_NAZI_MALI",
		iPoland : "TXT_KEY_CIV_GERMANY_NAZI_POLAND",
		iPortugal : "TXT_KEY_CIV_GERMANY_REICHSKOMMISSARIAT",
		iMughals : "TXT_KEY_CIV_GERMANY_NAZI_MUGHALS",
		iTurkey : "TXT_KEY_CIV_GERMANY_REICHSKOMMISSARIAT",
		iCanada : "TXT_KEY_CIV_GERMANY_NAZI_CANADA",
	},
}

dForeignAdjectives = {
	iChina : {
		iEgypt : "TXT_KEY_CIV_CHINESE_ADJECTIVE_EGYPT",
		iIndia : "TXT_KEY_CIV_CHINESE_ADJECTIVE_INDIA",
		iBabylonia : "TXT_KEY_CIV_CHINESE_ADJECTIVE_BABYLONIA",
		iPersia : "TXT_KEY_CIV_CHINESE_ADJECTIVE_PERSIA",
		iRome : "TXT_KEY_CIV_CHINESE_ADJECTIVE_ROME",
		iJapan : "TXT_KEY_CIV_CHINESE_ADJECTIVE_JAPAN",
		iKorea : "TXT_KEY_CIV_CHINESE_ADJECTIVE_KOREA",
		iByzantium : "TXT_KEY_CIV_CHINESE_ADJECTIVE_BYZANTIUM",
		iArabia : "TXT_KEY_CIV_CHINESE_ADJECTIVE_ARABIA",
		iKhmer : "TXT_KEY_CIV_CHINESE_ADJECTIVE_KHMER",
		iMongolia : "TXT_KEY_CIV_CHINESE_ADJECTIVE_MONGOLIA",
		iTurkey : "TXT_KEY_CIV_CHINESE_ADJECTIVE_TURKEY",
		iTibet : "TXT_KEY_CIV_CHINESE_ADJECTIVE_TIBET",
	},
}

dForeignNames = {
	iPersia : {
		iByzantium : "TXT_KEY_CIV_PERSIAN_NAME_BYZANTIUM",
		iIndonesia : "TXT_KEY_CIV_PERSIAN_NAME_INDONESIA",
	},
	iRome : {
		iEgypt : "TXT_KEY_CIV_ROMAN_NAME_EGYPT",
		iChina : "TXT_KEY_CIV_ROMAN_NAME_CHINA",
		iBabylonia : "TXT_KEY_CIV_ROMAN_NAME_BABYLONIA",
		iGreece : "TXT_KEY_CIV_ROMAN_NAME_GREECE",
		iPersia : "TXT_KEY_CIV_ROMAN_NAME_PERSIA",
		iPhoenicia : "TXT_KEY_CIV_ROMAN_NAME_PHOENICIA",
		iEthiopia : "TXT_KEY_CIV_ROMAN_NAME_ETHIOPIA",
		iByzantium : "TXT_KEY_CIV_ROMAN_NAME_BYZANTIUM",
		iVikings : "TXT_KEY_CIV_ROMAN_NAME_VIKINGS",
		iKhmer : "TXT_KEY_CIV_ROMAN_NAME_KHMER",
		iSpain : "TXT_KEY_CIV_ROMAN_NAME_SPAIN",
		iFrance : "TXT_KEY_CIV_ROMAN_NAME_FRANCE",
		iEngland : "TXT_KEY_CIV_ROMAN_NAME_ENGLAND",
		iHolyRome : "TXT_KEY_CIV_ROMAN_NAME_HOLY_ROME",
		iGermany : "TXT_KEY_CIV_ROMAN_NAME_GERMANY",
		iRussia : "TXT_KEY_CIV_ROMAN_NAME_RUSSIA",
		iNetherlands : "TXT_KEY_CIV_ROMAN_NAME_NETHERLANDS",
		iMali : "TXT_KEY_CIV_ROMAN_NAME_MALI",
		iPortugal : "TXT_KEY_CIV_ROMAN_NAME_PORTUGAL",
		iMongolia : "TXT_KEY_CIV_ROMAN_NAME_MONGOLIA",
		iTurkey : "TXT_KEY_CIV_ROMAN_NAME_TURKEY",
		iThailand : "TXT_KEY_CIV_ROMAN_NAME_THAILAND",
	},
	iArabia : {
		iEgypt : "TXT_KEY_CIV_ARABIAN_NAME_EGYPT",
		iBabylonia : "TXT_KEY_CIV_ARABIAN_NAME_BABYLONIA",
		iPersia : "TXT_KEY_CIV_ARABIAN_NAME_PERSIA",
		iPhoenicia : "TXT_KEY_CIV_ARABIAN_NAME_CARTHAGE",
		iRome : "TXT_KEY_CIV_ARABIAN_NAME_ROME",
		iEthiopia : "TXT_KEY_CIV_ARABIAN_NAME_ETHIOPIA",
		iByzantium : "TXT_KEY_CIV_ARABIAN_NAME_BYZANTIUM",
		iArabia : "TXT_KEY_CIV_ARABIAN_NAME_ARABIA",
		iMoors : "TXT_KEY_CIV_ARABIAN_NAME_MOORS",
		iSpain : "TXT_KEY_CIV_ARABIAN_NAME_SPAIN",
	},
	iMoors : {
		iEgypt : "TXT_KEY_CIV_ARABIAN_NAME_EGYPT",
		iBabylonia : "TXT_KEY_CIV_ARABIAN_NAME_BABYLONIA",
		iPersia : "TXT_KEY_CIV_ARABIAN_NAME_PERSIA",
		iPhoenicia : "TXT_KEY_CIV_ARABIAN_NAME_CARTHAGE",
		iRome : "TXT_KEY_CIV_ARABIAN_NAME_ROME",
		iEthiopia : "TXT_KEY_CIV_ARABIAN_NAME_ETHIOPIA",
		iByzantium : "TXT_KEY_CIV_ARABIAN_NAME_BYZANTIUM",
		iArabia : "TXT_KEY_CIV_ARABIAN_NAME_ARABIA",
		iMoors : "TXT_KEY_CIV_ARABIAN_NAME_MOORS",
		iSpain : "TXT_KEY_CIV_ARABIAN_NAME_SPAIN",
	},
	iSpain : {
		iKhmer : "TXT_KEY_CIV_SPANISH_NAME_KHMER",
		iAztecs : "TXT_KEY_CIV_SPANISH_NAME_AZTECS",
		iMughals : "TXT_KEY_CIV_SPANISH_NAME_MUGHALS",
	},
	iFrance : {
		iKhmer : "TXT_KEY_CIV_FRENCH_NAME_KHMER",
		iMughals : "TXT_KEY_CIV_FRENCH_NAME_MUGHALS",
	},
	iEngland : {
		iKhmer : "TXT_KEY_CIV_ENGLISH_NAME_KHMER",
		iMughals : "TXT_KEY_CIV_ENGLISH_NAME_MUGHALS",
	},
	iRussia : {
		iPersia : "TXT_KEY_CIV_RUSSIAN_NAME_PERSIA",
	},
	iGermany : {
		iMoors : "TXT_KEY_CIV_GERMAN_NAME_MOORS",
	},
}

lRepublicOf = [iEgypt, iIndia, iChina, iPersia, iJapan, iEthiopia, iKorea, iVikings, iTibet, iKhmer, iIndonesia, iHolyRome, iMali, iPoland, iMughals, iTurkey, iThailand]
lRepublicAdj = [iBabylonia, iRome, iMoors, iSpain, iFrance, iPortugal, iInca, iItaly, iAztecs, iArgentina]

lSocialistRepublicOf = [iMoors, iHolyRome, iBrazil]
lSocialistRepublicAdj = [iPersia, iItaly, iAztecs, iArgentina]

lPeoplesRepublicOf = [iIndia, iChina, iPolynesia, iRome, iJapan, iTibet, iIndonesia, iMali, iPoland, iMughals, iThailand, iCongo]
lPeoplesRepublicAdj = [iTamils, iByzantium, iMongolia]

lIslamicRepublicOf = [iIndia, iPersia, iMali, iMughals]

lCityStatesStart = [iRome, iCarthage, iGreece, iIndia, iMaya, iAztecs]

dEmpireThreshold = {
	iCarthage : 4,
	iIndonesia : 4,
	iKorea : 4,
	iRussia : 8,
	iHolyRome : 3,
	iGermany : 4,
	iItaly : 4,
	iInca : 3,
	iMongolia : 6,
	iPoland : 3,
	iMoors : 3,
	iTibet : 2,
	iPolynesia : 3,
	iTamils : 3,
}

lChristianity = [iCatholicism, iOrthodoxy, iProtestantism]

lRespawnNameChanges = [iHolyRome, iInca, iAztecs, iMali]
lVassalNameChanges = [iInca, iAztecs, iMughals]
lChristianityNameChanges = [iInca, iAztecs]

lRebirths = [iAztecs, iMaya, iPersia]
lColonies = [iMali, iEthiopia, iCongo, iAztecs, iInca, iMaya]

dNameChanges = {
	iPhoenicia : "TXT_KEY_CIV_CARTHAGE_SHORT_DESC",
	iAztecs : "TXT_KEY_CIV_MEXICO_SHORT_DESC",
	iInca : "TXT_KEY_CIV_PERU_SHORT_DESC",
	iHolyRome : "TXT_KEY_CIV_AUSTRIA_SHORT_DESC",
	iMali : "TXT_KEY_CIV_SONGHAI_SHORT_DESC",
	iMughals : "TXT_KEY_CIV_PAKISTAN_SHORT_DESC",
}

dAdjectiveChanges = {
	iPhoenicia : "TXT_KEY_CIV_CARTHAGE_ADJECTIVE",
	iAztecs : "TXT_KEY_CIV_MEXICO_ADJECTIVE",
	iInca : "TXT_KEY_CIV_PERU_ADJECTIVE",
	iHolyRome : "TXT_KEY_CIV_AUSTRIA_ADJECTIVE",
	iMali : "TXT_KEY_CIV_SONGHAI_ADJECTIVE",
	iMughals : "TXT_KEY_CIV_PAKISTAN_ADJECTIVE",
}

dCapitals = {
	iPolynesia : ["Kaua'i", "O'ahu", "Maui", "Manu'a", "Niue"],
	iBabylonia : ["Ninua", "Kalhu"],
	iByzantium : ["Dyrrachion", "Athena", "Konstantinoupolis"],
	iVikings : ["Stockholm", "Oslo", "Nidaros", "Kalmar", "Roskilde"],
	iKhmer : ["Pagan", "Dali", "Angkor", "Hanoi"],
	iRussia : ["Moskva"],
	iItaly : ["Fiorenza", "Roma"],
	iTamils : ["Madurai", "Thiruvananthapuram", "Cochin", "Kozhikode"],
	iArabia : ["Dimashq"],
	iSpain : ["La Paz", "Barcelona", "Valencia"],
	iPoland : ["Kowno", "Medvegalis", "Wilno", "Ryga"],
}

dCapitalLocations = findCapitalLocations(dCapitals)

dStartingLeaders = [
# 3000 BC
{
	iEgypt : iRamesses,
	iIndia : iAsoka,
	iChina : iQinShiHuang,
	iBabylonia : iSargon,
	iHarappa : iVatavelli,
	iGreece : iPericles,
	iPersia : iCyrus,
	iCarthage : iHiram,
	iPolynesia : iAhoeitu,
	iRome : iJuliusCaesar,
	iJapan : iKammu,
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
	iRussia : iIvan,
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
	iBrazil : iPedro,
	iCanada : iMacDonald,
},
# 600 AD
{
	iChina : iTaizong,
},
# 1700 AD
{
	iChina : iHongwu,
	iIndia : iShahuji,
	iPersia : iAbbas,
	iJapan : iOdaNobunaga,
	iVikings : iGustav,
	iSpain : iPhilip,
	iFrance : iLouis,
	iEngland : iVictoria,
	iHolyRome : iFrancis,
	iRussia : iPeter,
	iNetherlands : iWilliam,
	iPoland : iSobieski,
	iPortugal : iJoao,
	iMughals : iAkbar,
	iTurkey : iSuleiman,
	iGermany : iFrederick,
}]

### Event handlers

def setup():			
	iScenario = utils.getScenario()
	
	if iScenario == i600AD:
		sd.changeAnarchyTurns(iChina, 3)
		
	elif iScenario == i1700AD:
		sd.changeResurrections(iEgypt, 1)
	
	for iPlayer in range(iNumPlayers):	
		setDesc(iPlayer, peoplesName(iPlayer))
		
		if gc.getPlayer(iPlayer).getNumCities() > 0:
			checkName(iPlayer)
		
		if not gc.getPlayer(iPlayer).isHuman():
			setLeader(iPlayer, startingLeader(iPlayer))
		
def onCivRespawn(iPlayer, tOriginalOwners):
	sd.changeResurrections(iPlayer, 1)
	
	if iPlayer in lRespawnNameChanges:
		setShort(iPlayer, text(dNameChanges[iPlayer]))
		setAdjective(iPlayer, text(dAdjectiveChanges[iPlayer]))
		
	setDesc(iPlayer, defaultTitle(iPlayer))
	checkName(iPlayer)
	checkLeader(iPlayer)
	
def onVassalState(iVassal):
	if iVassal in lVassalNameChanges:
		sd.changeResurrections(iVassal, 1)
		setShort(iVassal, text(dNameChanges[iVassal]))
		setAdjective(iVassal, text(dAdjectiveChanges[iVassal]))
		
	checkName(iVassal)
	
def onPlayerChangeStateReligion(iPlayer, iReligion):
	if iPlayer in lChristianityNameChanges and iReligion in lChristianity:
		sd.changeResurrections(iPlayer, 1)
		setShort(iPlayer, text(dNameChanges[iPlayer]))
		setAdjective(iPlayer, text(dAdjectiveChanges[iPlayer]))
		
	checkName(iPlayer)
	
def onRevolution(iPlayer):
	sd.changeAnarchyTurns(iPlayer, 1)
	checkName(iPlayer)
	
def onCityAcquired(iPreviousOwner, iNewOwner):
	checkName(iPreviousOwner)
	checkName(iNewOwner)
	
def onCityRazed(iOwner):
	checkName(iOwner)
	
def onCityBuilt(iOwner):
	checkName(iOwner)
	
def onPalaceMoved(iPlayer):
	capital = gc.getPlayer(iPlayer).getCapitalCity()

	if iPlayer == iPhoenicia:
		if capital.getRegionID() not in [rMesopotamia, rAnatolia]:
			setShort(iPlayer, text(dNameChanges[iPlayer]))
			setAdjective(iPlayer, text(dAdjectiveChanges[iPlayer]))
		else:
			setShort(iPlayer, short(iPlayer))
			setAdjective(iPlayer, civAdjective(iPlayer))
			
	#checkName(iPlayer)
	
def checkTurn(iGameTurn):
	for iPlayer in range(iNumPlayers):
		checkName(iPlayer)
		checkLeader(iPlayer)
		
def checkName(iPlayer):
	if not gc.getPlayer(iPlayer).isAlive(): return
	if iPlayer >= iNumPlayers: return
	if gc.getPlayer(iPlayer).getNumCities() == 0: return
	setDesc(iPlayer, desc(iPlayer, title(iPlayer)))
	
def checkLeader(iPlayer):
	if not gc.getPlayer(iPlayer).isAlive(): return
	if iPlayer >= iNumPlayers: return
	setLeader(iPlayer, leader(iPlayer))
	setLeaderName(iPlayer, leaderName(iPlayer))

### Setter methods for player object ###

def setDesc(iPlayer, sName):
	gc.getPlayer(iPlayer).setCivDescription(sName)
	
def setShort(iPlayer, sShort):
	gc.getPlayer(iPlayer).setCivShortDescription(sShort)
	
def setAdjective(iPlayer, sAdj):
	gc.getPlayer(iPlayer).setCivAdjective(sAdj)
	
def setLeader(iPlayer, iLeader):
	if not iLeader: return
	if gc.getPlayer(iPlayer).getLeader() == iLeader: return
	gc.getPlayer(iPlayer).setLeader(iLeader)
	
def setLeaderName(iPlayer, sName):
	if not sName: return
	if gc.getLeaderHeadInfo(gc.getPlayer(iPlayer).getLeader()).getText() != sName:
		gc.getPlayer(iPlayer).setLeaderName(sName)

### Utility methods ###

def getOrElse(dDictionary, iPlayer, sDefault=None):
	if iPlayer in dDictionary: return dDictionary[iPlayer]
	return sDefault

def key(iPlayer, sSuffix):
	if sSuffix: sSuffix = "_" + sSuffix
	return "TXT_KEY_CIV_" + short(iPlayer).replace(" ", "_").upper() + sSuffix

def text(sTextKey, tInput=()):
	return localText.getText(str(sTextKey), tInput)
	
def desc(iPlayer, sTextKey=str("%s1")):
	return text(sTextKey, (name(iPlayer), adjective(iPlayer)))

def short(iPlayer):
	return gc.getCivilizationInfo(gc.getPlayer(iPlayer).getCivilizationType()).getShortDescription(0)
	
def civAdjective(iPlayer):
	return gc.getCivilizationInfo(gc.getPlayer(iPlayer).getCivilizationType()).getAdjective(0)

def capitalName(iPlayer):
	capital = gc.getPlayer(iPlayer).getCapitalCity()
	if capital: 
		sCapitalName = cnm.getRenameName(iEngland, capital.getName())
		if sCapitalName: return sCapitalName
		else: return capital.getName()
	
	return short(iPlayer)
	
def nameChange(iPlayer):
	setShort(iPlayer, text(dNameChanges[iPlayer]))
	
def adjectiveChange(iPlayer):
	setAdjective(iPlayer, text(dAdjectiveChanges[iPlayer]))
	
### Utility methods for civilization status ###

def getCivics(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	return pPlayer.getCivics(0), pPlayer.getCivics(1), pPlayer.getCivics(2), pPlayer.getCivics(3), pPlayer.getCivics(4)

def isCommunist(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	iGovernment, iOrganization, c, iEconomy, e = getCivics(iPlayer)
	
	if iEconomy != iCivicCentralPlanning:
		return False
	
	if iGovernment == iCivicTheocracy:
		return False
		
	if iOrganization in [iCivicVassalage, iCivicAbsolutism]:
		return False
		
	return True
	
def isFascist(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	a, iOrganization, c, d, e = getCivics(iPlayer)
	
	if iOrganization == iCivicTotalitarianism:
		return True
		
	return False
	
def isRepublic(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	iGovernment, iOrganization, c, d, e = getCivics(iPlayer)
	
	if iGovernment == iCivicRepublic: 
		return True
	if iGovernment == iCivicAutocracy and iOrganization in [iCivicRepresentation, iCivicEgalitarianism]:
		return True
		
	return False
	
def isVassal(iPlayer):
	return utils.isAVassal(iPlayer)
	
def isCapitulated(iPlayer):
	return isVassal(iPlayer) and gc.getTeam(iPlayer).isCapitulated()
	
def getMaster(iPlayer):
	return utils.getMaster(iPlayer)
	
def isEmpire(iPlayer):
	iThreshold = getEmpireThreshold(iPlayer)
	return gc.getPlayer(iPlayer).getNumCities() >= iThreshold
	
def getEmpireThreshold(iPlayer):
	if iPlayer in dEmpireThreshold: return dEmpireThreshold[iPlayer]
	
	if gc.getPlayer(iPlayer).isReborn():
		if iPlayer == iPersia: return 4
		
	return 5
	
def isAtWar(iPlayer):
	for iTarget in range(iNumPlayers):
		if gc.getTeam(iPlayer).isAtWar(iTarget):
			return True
	return False
	
def isCapital(iPlayer, lNames):
	capital = gc.getPlayer(iPlayer).getCapitalCity()
	if not capital: return False
	
	tLocation = (capital.getX(), capital.getY())
	
	for sName in lNames:
		if tLocation in dCapitalLocations[sName]:
			return True
			
	return False
	
def countAreaCities(tTL, tBR, tExceptions=()):
	return len(utils.getAreaCities(utils.getPlotList(tTL, tBR, tExceptions)))
	
def countPlayerAreaCities(iPlayer, tTL, tBR, tExceptions=()):
	return len(utils.getAreaCitiesCiv(iPlayer, utils.getPlotList(tTL, tBR, tExceptions)))
	
def isAreaControlled(iPlayer, tTL, tBR, iMinCities=1, tExceptions=()):
	iTotalCities = countAreaCities(tTL, tBR, tExceptions)
	iPlayerCities = countPlayerAreaCities(iPlayer, tTL, tBR, tExceptions)
	
	if iPlayerCities < iTotalCities: return False
	if iPlayerCities < iMinCities: return False
	
	return True
	
def capitalCoords(iPlayer):
	capital = gc.getPlayer(iPlayer).getCapitalCity()
	if capital: return (capital.getX(), capital.getY())
	
	return (-1, -1)
	
### Naming methods ###

def name(iPlayer):
	if isCapitulated(iPlayer):
		sVassalName = vassalName(iPlayer, getMaster(iPlayer))
		if sVassalName: return sVassalName
		
	if isCommunist(iPlayer) or isFascist(iPlayer) or isRepublic(iPlayer):
		sRepublicName = republicName(iPlayer)
		if sRepublicName: return sRepublicName
		
	sSpecificName = specificName(iPlayer)
	if sSpecificName: return sSpecificName
	
	sDefaultInsertName = getOrElse(dDefaultInsertNames, iPlayer)
	if sDefaultInsertName: return sDefaultInsertName
	
	return short(iPlayer)
	
def vassalName(iPlayer, iMaster):
	if iMaster == iRome and short(iPlayer) == "Carthage":
		return "TXT_KEY_CIV_ROMAN_NAME_CARTHAGE"

	sSpecificName = getOrElse(getOrElse(dForeignNames, iMaster, {}), iPlayer)
	if sSpecificName: return sSpecificName
	
	return None
	
def republicName(iPlayer):
	if iPlayer in [iMoors, iEngland]: return None
	
	if iPlayer == iInca and sd.getResurrections(iPlayer) > 0: return None

	return short(iPlayer)
	
def peoplesName(iPlayer):
	return desc(iPlayer, key(iPlayer, "PEOPLES"))
	
def specificName(iPlayer):
	iGameTurn = gc.getGame().getGameTurn()
	pPlayer = gc.getPlayer(iPlayer)
	tPlayer = gc.getTeam(pPlayer.getTeam())
	iCivicGovernment, iCivicOrganization, iCivicLabor, iCivicEconomy, iCivicReligion = getCivics(iPlayer)
	
	iNumCities = pPlayer.getNumCities()
	if iNumCities == 0: return short(iPlayer)
	
	bReborn = pPlayer.isReborn()
	iReligion = pPlayer.getStateReligion()
	capital = gc.getPlayer(iPlayer).getCapitalCity()
	tCapitalCoords = capitalCoords(iPlayer)
	bAnarchy = pPlayer.isAnarchy()
	bEmpire = isEmpire(iPlayer)
	bCityStates = (iCivicGovernment == iCivicCityStates)
	bTheocracy = (iCivicGovernment == iCivicTheocracy)
	bResurrected = (sd.getResurrections(iPlayer) > 0)
	bCapitulated = isCapitulated(iPlayer)
	iAnarchyTurns = sd.getAnarchyTurns(iPlayer)
	iEra = pPlayer.getCurrentEra()
	iGameEra = gc.getGame().getCurrentEra()
	bWar = isAtWar(iPlayer)
	
	if iPlayer == iChina:
		if iEra >= iIndustrial or utils.getScenario() == i1700AD:
			return "TXT_KEY_CIV_CHINA_QING"
			
		if iEra == iRenaissance and iGameTurn >= getTurnForYear(1400):
			return "TXT_KEY_CIV_CHINA_MING"
			
	elif iPlayer == iBabylonia:
		if isCapital(iPlayer, ["Ninua", "Kalhu"]):
			return "TXT_KEY_CIV_BABYLONIA_ASSYRIA"
			
	elif iPlayer == iGreece:
		if not bCityStates and bEmpire and iEra <= iClassical:
			return
			
	elif iPlayer == iPolynesia:
		if isCapital(iPlayer, ["Kaua'i", "O'ahu", "Maui"]):
			return "TXT_KEY_CIV_POLYNESIA_HAWAII"
			
		if isCapital(iPlayer, ["Manu'a"]):
			return "TXT_KEY_CIV_POLYNESIA_SAMOA"
			
		if isCapital(iPlayer, ["Niue"]):
			return "TXT_KEY_CIV_POLYNESIA_NIUE"
			
		return "TXT_KEY_CIV_POLYNESIA_TONGA"
		
	elif iPlayer == iTamils:
		if iEra >= iRenaissance:
			return "TXT_KEY_CIV_TAMILS_MYSORE"
			
		if iEra >= iMedieval:
			return "TXT_KEY_CIV_TAMILS_VIJAYANAGARA"
			
	elif iPlayer == iEthiopia:
		if not gc.getGame().isReligionFounded(iIslam):
			return "TXT_KEY_CIV_ETHIOPIA_AKSUM"
			
	elif iPlayer == iKorea:
		if iEra == iClassical:
			if bEmpire:
				return "TXT_KEY_CIV_KOREA_GOGURYEO"
				
		if iEra <= iMedieval:
			return "TXT_KEY_CIV_KOREA_GORYEO"
			
		return "TXT_KEY_CIV_KOREA_JOSEON"
		
	elif iPlayer == iByzantium:
		if isCapital(iPlayer, ["Dyrrachion"]):
			return "TXT_KEY_CIV_BYZANTIUM_EPIRUS"
			
		if isCapital(iPlayer, ["Athena"]):
			return "TXT_KEY_CIV_BYZANTIUM_MOREA"
	
		if not isCapital(iPlayer, ["Konstantinoupolis"]):
			return capitalName(iPlayer)
			
	elif iPlayer == iVikings:
		if bEmpire:
			if not isCapital(iPlayer, ["Stockholm"]) or iEra != iRenaissance:
				return "TXT_KEY_CIV_VIKINGS_DENMARK_NORWAY"
	
		if isCapital(iPlayer, ["Oslo", "Nidaros"]):
			return "TXT_KEY_CIV_VIKINGS_NORWAY"
			
		if isCapital(iPlayer, ["Stockholm", "Kalmar"]):
			return "TXT_KEY_CIV_VIKINGS_SWEDEN"
			
		if isCapital(iPlayer, ["Roskilde"]):
			return "TXT_KEY_CIV_VIKINGS_DENMARK"
			
		return "TXT_KEY_CIV_VIKINGS_SCANDINAVIA"
		
	elif iPlayer == iArabia:
		if bResurrected:
			return "TXT_KEY_CIV_ARABIA_SAUDI"
			
	elif iPlayer == iKhmer:
		if isCapital(iPlayer, ["Pagan"]):
			return "TXT_KEY_CIV_KHMER_BURMA"
			
		if isCapital(iPlayer, ["Dali"]):
			return "TXT_KEY_CIV_KHMER_NANZHAO"
			
	elif iPlayer == iIndonesia:
		if iReligion == iIslam:
			return "TXT_KEY_CIV_INDONESIA_MATARAM"
			
		if iEra <= iRenaissance:
			if bEmpire:
				return "TXT_KEY_CIV_INDONESIA_MAJAPAHIT"
				
			return "TXT_KEY_CIV_INDONESIA_SRIVIJAYA"
			
	elif iPlayer == iMoors:	
		if utils.isPlotInArea(tCapitalCoords, vic.tIberiaTL, vic.tIberiaBR):
			return capitalName(iPlayer)
			
		return "TXT_KEY_CIV_MOORS_MOROCCO"
		
	elif iPlayer == iSpain:
		if iReligion == iIslam:
			return "TXT_KEY_CIV_SPAIN_AL_ANDALUS"
	
		bSpain = not pMoors.isAlive() or not utils.isPlotInArea(capitalCoords(iMoors), vic.tIberiaTL, vic.tIberiaBR)
	
		if bSpain:
			if not pPortugal.isAlive() or getMaster(iPortugal) == iPlayer or not utils.isPlotInArea(capitalCoords(iPortugal), vic.tIberiaTL, vic.tIberiaBR):
				return "TXT_KEY_CIV_SPAIN_IBERIA"
			
		if isCapital(iPlayer, ["Barcelona", "Valencia"]):
			return "TXT_KEY_CIV_SPAIN_ARAGON"
			
		if not bSpain:
			return "TXT_KEY_CIV_SPAIN_CASTILE"
			
	elif iPlayer == iFrance:
		if iEra == iMedieval and not pHolyRome.isAlive():
			return "TXT_KEY_CIV_FRANCE_FRANCIA"
			
	elif iPlayer == iEngland:
		if tPlayer.isHasTech(iConstitution) and isAreaControlled(iPlayer, tBritainTL, tBritainBR, 3):
			return "TXT_KEY_CIV_ENGLAND_GREAT_BRITAIN"
			
	elif iPlayer == iHolyRome:
		if not bEmpire and iGameTurn < getTurnForYear(tBirth[iGermany]):
			return "TXT_KEY_CIV_HOLY_ROME_GERMANY"
			
	elif iPlayer == iRussia:
		if not bEmpire and not isAreaControlled(iPlayer, tEuropeanRussiaTL, tEuropeanRussiaBR, 5, tEuropeanRussiaExceptions):
			if isCapital(iPlayer, ["Moskva"]):
				return "TXT_KEY_CIV_RUSSIA_MUSCOVY"
				
			return capitalName(iPlayer)
			
	elif iPlayer == iInca:
		if bResurrected:
			if isCapital(iPlayer, ["La Paz"]):
				return "TXT_KEY_CIV_INCA_BOLIVIA"
				
		if not bEmpire:
			return capitalName(iPlayer)
			
	elif iPlayer == iItaly:
		if not bResurrected and not bEmpire and not bCityStates:
			if isCapital(iPlayer, ["Fiorenza"]):
				return "TXT_KEY_CIV_ITALY_TUSCANY"
				
			return capitalName(iPlayer)
			
	elif iPlayer == iThailand:
		if iEra <= iRenaissance:
			return "TXT_KEY_CIV_THAILAND_AYUTTHAYA"
	
def adjective(iPlayer):
	if isCapitulated(iPlayer):
		sForeignAdjective = getOrElse(getOrElse(dForeignAdjectives, getMaster(iPlayer), {}), iPlayer)
		if sForeignAdjective: return sForeignAdjective
		
		return adjective(getMaster(iPlayer))
		
	if isCommunist(iPlayer) or isFascist(iPlayer) or isRepublic(iPlayer):
		sRepublicAdjective = republicAdjective(iPlayer)
		if sRepublicAdjective: return sRepublicAdjective
		
	sSpecificAdjective = specificAdjective(iPlayer)
	if sSpecificAdjective: return sSpecificAdjective
	
	#sDefaultInsertAdjective = getOrElse(dDefaultInsertAdjectives, iPlayer)
	#if sDefaultInsertAdjective: return sDefaultInsertAdjective
	
	return gc.getPlayer(iPlayer).getCivilizationAdjective(0)
	
def republicAdjective(iPlayer):
	if iPlayer == iRome:
		if pByzantium.isAlive(): return None

	if iPlayer == iByzantium:
		if pRome.isAlive(): return None
		
	if iPlayer in [iMoors, iEngland]: return None
	
	if iPlayer == iInca and sd.getResurrections(iPlayer) > 0: return None
		
	return gc.getPlayer(iPlayer).getCivilizationAdjective(0)
	
def specificAdjective(iPlayer):
	iGameTurn = gc.getGame().getGameTurn()
	pPlayer = gc.getPlayer(iPlayer)
	tPlayer = gc.getTeam(pPlayer.getTeam())
	iCivicGovernment, iCivicOrganization, iCivicLabor, iCivicEconomy, iCivicReligion = getCivics(iPlayer)
	
	iNumCities = pPlayer.getNumCities()
	if iNumCities == 0: return gc.getPlayer(iPlayer).getCivilizationAdjective(0)
	
	bReborn = pPlayer.isReborn()
	iReligion = pPlayer.getStateReligion()
	capital = gc.getPlayer(iPlayer).getCapitalCity()
	tCapitalCoords = capitalCoords(iPlayer)
	bAnarchy = pPlayer.isAnarchy()
	bEmpire = isEmpire(iPlayer)
	bCityStates = (iCivicGovernment == iCivicCityStates)
	bTheocracy = (iCivicGovernment == iCivicTheocracy)
	bResurrected = (sd.getResurrections(iPlayer) > 0)
	bCapitulated = isCapitulated(iPlayer)
	iAnarchyTurns = sd.getAnarchyTurns(iPlayer)
	iEra = pPlayer.getCurrentEra()
	iGameEra = gc.getGame().getCurrentEra()
	bWar = isAtWar(iPlayer)
	
	bMonarchy = not isCommunist(iPlayer) and not isFascist(iPlayer) and not isRepublic(iPlayer)
	
	if iPlayer == iEgypt:
		if bMonarchy:
			if bResurrected:
				if tPlayer.isHasTech(iGunpowder):
					return "TXT_KEY_CIV_EGYPT_MAMLUK"
		
				if pArabia.isAlive():
					return "TXT_KEY_CIV_EGYPT_FATIMID"
			
				return "TXT_KEY_CIV_EGYPT_AYYUBID"
			
	elif iPlayer == iIndia:
		if bMonarchy and not bCityStates:
			if iEra >= iRenaissance:
				return "TXT_KEY_CIV_INDIA_MARATHA"
			
			if iEra >= iMedieval:
				return "TXT_KEY_CIV_INDIA_PALA"
			
			if iReligion == iBuddhism:
				return "TXT_KEY_CIV_INDIA_MAURYA"
			
			if iReligion == iHinduism:
				return "TXT_KEY_CIV_INDIA_GUPTA"
			
	elif iPlayer == iChina:
		if bMonarchy:
			if bResurrected:
				return "TXT_KEY_CIV_CHINA_SONG"
		
			if iEra == iMedieval:
				if tPlayer.isHasTech(iPaper) and tPlayer.isHasTech(iGunpowder):
					return "TXT_KEY_CIV_CHINA_SONG"
			
				if iGameTurn >= getTurnForYear(600):
					return "TXT_KEY_CIV_CHINA_TANG"
				
				return "TXT_KEY_CIV_CHINA_SUI"
			
			if iEra == iClassical:
				if iGameTurn >= getTurnForYear(0):
					return "TXT_KEY_CIV_CHINA_HAN"
				
				return "TXT_KEY_CIV_CHINA_QIN"
			
			return "TXT_KEY_CIV_CHINA_ZHOU"
			
	elif iPlayer == iBabylonia:
		if bCityStates and not bEmpire:
			return "TXT_KEY_CIV_BABYLONIA_MESOPOTAMIAN"
			
		if isCapital(iPlayer, ["Ninua", "Kalhu"]):
			return "TXT_KEY_CIV_BABYLONIA_ASSYRIAN"
			
	elif iPlayer == iGreece:
		if not bCityStates and bEmpire and iEra <= iClassical:
			return "TXT_KEY_CIV_GREECE_MACEDONIAN"
			
	elif iPlayer == iPersia:
		if bEmpire:
			if bReborn:
				if iEra <= iRenaissance:
					return "TXT_KEY_CIV_PERSIA_SAFAVID"
			
				if iEra == iIndustrial:
					return "TXT_KEY_CIV_PERSIA_QAJAR"
			
				return "TXT_KEY_CIV_PERSIA_PAHLAVI"
			
			if iEra <= iClassical:
				if bResurrected:
					return "TXT_KEY_CIV_PERSIA_PARTHIAN"
					
				return "TXT_KEY_CIV_PERSIA_ACHAEMENID"
			
			if iEra == iMedieval:
				return "TXT_KEY_CIV_PERSIA_SASSANID"
				
	elif iPlayer == iPolynesia:
		if isCapital(iPlayer, ["Manu'a"]):
			return "TXT_KEY_CIV_POLYNESIA_TUI_MANUA"
			
		return "TXT_KEY_CIV_POLYNESIA_TUI_TONGA"
		
	elif iPlayer == iRome:
		if pByzantium.isAlive():
			return "TXT_KEY_CIV_ROME_WESTERN"
			
	elif iPlayer == iTamils:
		if iEra <= iClassical:
			if isCapital(iPlayer, ["Madurai", "Thiruvananthapuram"]):
				return "TXT_KEY_CIV_TAMILS_PANDYAN"
				
			if isCapital(iPlayer, ["Cochin", "Kozhikode"]):
				return "TXT_KEY_CIV_TAMILS_CHERA"
				
			return "TXT_KEY_CIV_TAMILS_CHOLA"
			
	elif iPlayer == iVikings:
		if bEmpire:
			return "TXT_KEY_CIV_VIKINGS_SWEDISH"
			
	elif iPlayer == iArabia:
		if bTheocracy and iReligion == iIslam:
			if not bEmpire:
				return "TXT_KEY_CIV_ARABIA_RASHIDUN"
				
			if isCapital(iPlayer, ["Dimashq"]):
				return "TXT_KEY_CIV_ARABIA_UMMAYAD"
				
			return "TXT_KEY_CIV_ARABIA_ABBASID"
			
	elif iPlayer == iMoors:
			
		if bEmpire and iEra <= iRenaissance:
			return "TXT_KEY_CIV_MOORS_ALMOHAD"
			
		if not utils.isPlotInArea(tCapitalCoords, vic.tIberiaTL, vic.tIberiaBR):
			return "TXT_KEY_CIV_MOORS_MOROCCAN"
			
	elif iPlayer == iSpain:
		bSpain = not pMoors.isAlive() or not utils.isPlotInArea(capitalCoords(iMoors), vic.tIberiaTL, vic.tIberiaBR)
	
		if bSpain:
			if not pPortugal.isAlive() or getMaster(iPortugal) == iPlayer or not utils.isPlotInArea(capitalCoords(iPortugal), vic.tIberiaTL, vic.tIberiaBR):
				return "TXT_KEY_CIV_SPAIN_IBERIAN"
			
		if isCapital(iPlayer, ["Barcelona", "Valencia"]):
			return "TXT_KEY_CIV_SPAIN_ARAGONESE"
			
		if not bSpain:
			return "TXT_KEY_CIV_SPAIN_CASTILIAN"
			
	elif iPlayer == iFrance:
		if iEra == iMedieval and not pHolyRome.isAlive():
			return "TXT_KEY_CIV_FRANCE_FRANKISH"
			
	elif iPlayer == iEngland:
		if tPlayer.isHasTech(iConstitution) and isAreaControlled(iPlayer, tBritainTL, tBritainBR, 3):
			return "TXT_KEY_CIV_ENGLAND_BRITISH"
			
	elif iPlayer == iHolyRome:
		if pGermany.isAlive() and iCivicOrganization == iCivicRepresentation:
			return "TXT_KEY_CIV_HOLY_ROME_AUSTRO_HUNGARIAN"
			
		iVassals = 0
		for iLoopPlayer in lCivGroups[0]:
			if getMaster(iLoopPlayer) == iPlayer:
				iVassals += 1
				
		if iVassals >= 2:
			return "TXT_KEY_CIV_HOLY_ROME_HABSBURG"
			
		if not bEmpire and iGameTurn < getTurnForYear(tBirth[iGermany]):
			return "TXT_KEY_CIV_HOLY_ROME_GERMAN"
			
	elif iPlayer == iInca:
		if bResurrected:
			if isCapital(iPlayer, ["La Paz"]):
				return "TXT_KEY_CIV_INCA_BOLIVIAN"
				
	elif iPlayer == iItaly:
		if bCityStates and bWar:
			if not bEmpire:
				return "TXT_KEY_CIV_ITALY_LOMBARD"
				
	elif iPlayer == iMongolia:
		if not bEmpire and iEra <= iRenaissance:
			if capital.getRegionID() == rChina:
				return "TXT_KEY_CIV_MONGOLIA_YUAN"
				
			if capital.getRegionID() == rPersia:
				return "TXT_KEY_CIV_MONGOLIA_TIMURID"
				
			if capital.getRegionID() == rCentralAsia:
				if iReligion == iIslam:
					return "TXT_KEY_CIV_MONGOLIA_TIMURID"
					
				return "TXT_KEY_CIV_MONGOLIA_CHAGATAI"
				
		if bMonarchy:
			return "TXT_KEY_CIV_MONGOLIA_MONGOL"
				
	elif iPlayer == iTurkey:
		if iReligion == iIslam:
			return "TXT_KEY_CIV_TURKEY_OTTOMAN"
	
### Title methods ###

def title(iPlayer):
	if isCapitulated(iPlayer):
		sVassalTitle = vassalTitle(iPlayer, getMaster(iPlayer))
		if sVassalTitle: return sVassalTitle
		
	if isCommunist(iPlayer):
		sCommunistTitle = communistTitle(iPlayer)
		if sCommunistTitle: return sCommunistTitle
		
	if isFascist(iPlayer):
		sFascistTitle = fascistTitle(iPlayer)
		if sFascistTitle: return sFascistTitle
		
	if isRepublic(iPlayer):
		sRepublicTitle = republicTitle(iPlayer)
		if sRepublicTitle: return sRepublicTitle
		
	sSpecificTitle = specificTitle(iPlayer)
	if sSpecificTitle: return sSpecificTitle
	
	return defaultTitle(iPlayer)
	
def vassalTitle(iPlayer, iMaster):
	if isCommunist(iMaster):
		sCommunistTitle = getOrElse(getOrElse(dCommunistVassalTitles, iMaster, {}), iPlayer)
		if sCommunistTitle: return sCommunistTitle
		
		sCommunistTitle = getOrElse(dCommunistVassalTitlesGeneric, iMaster)
		if sCommunistTitle: return sCommunistTitle
		
	if isFascist(iMaster):
		sFascistTitle = getOrElse(getOrElse(dFascistVassalTitles, iMaster, {}), iPlayer)
		if sFascistTitle: return sFascistTitle
		
		sFascistTitle = getOrElse(dFascistVassalTitlesGeneric, iMaster)
		if sFascistTitle: return sFascistTitle
				
	if short(iMaster) == "Austria" and iPlayer == iPoland:
		return "TXT_KEY_CIV_AUSTRIAN_POLAND"
		
	if iMaster == iEngland and iPlayer == iMughals:
		if not pIndia.isAlive():
			return vassalTitle(iIndia, iEngland)
			
	if iMaster == iSpain and short(iPlayer) == "Colombia":
		return "TXT_KEY_CIV_SPANISH_COLOMBIA"

	if iMaster not in lRebirths or not gc.getPlayer(iMaster).isReborn():
		sSpecificTitle = getOrElse(getOrElse(dSpecificVassalTitles, iMaster, {}), iPlayer)
		if sSpecificTitle: return sSpecificTitle
	
		sMasterTitle = getOrElse(dMasterTitles, iMaster)
		if sMasterTitle: return sMasterTitle
		
	if iPlayer in lColonies:
		return "TXT_KEY_COLONY_OF"
	
	return "TXT_KEY_PROTECTORATE_OF"
	
def communistTitle(iPlayer):
	if iPlayer in lSocialistRepublicOf: return "TXT_KEY_SOCIALIST_REPUBLIC_OF"
	if iPlayer in lSocialistRepublicAdj: return "TXT_KEY_SOCIALIST_REPUBLIC_ADJECTIVE"
	if iPlayer in lPeoplesRepublicOf: return "TXT_KEY_PEOPLES_REPUBLIC_OF"
	if iPlayer in lPeoplesRepublicAdj: return "TXT_KEY_PEOPLES_REPUBLIC_ADJECTIVE"

	return key(iPlayer, "COMMUNIST")
	
def fascistTitle(iPlayer):
	return key(iPlayer, "FASCIST")
	
def republicTitle(iPlayer):
	if gc.getPlayer(iPlayer).getStateReligion() == iIslam:
		if iPlayer in lIslamicRepublicOf: return "TXT_KEY_ISLAMIC_REPUBLIC_OF"

		if iPlayer == iTurkey: return key(iPlayer, "ISLAMIC_REPUBLIC")
		
	if iPlayer in lRepublicOf: return "TXT_KEY_REPUBLIC_OF"
	if iPlayer in lRepublicAdj: return "TXT_KEY_REPUBLIC_ADJECTIVE"
	
	if iPlayer == iPoland:
		if gc.getPlayer(iPlayer).getCurrentEra() <= iIndustrial:
			return key(iPlayer, "EMPIRE")
			
	if iPlayer == iAmerica:
		a, b, iCivicLabor, d, e = getCivics(iPlayer)
		if iCivicLabor in [iCivicAgrarianism, iCivicSlavery]:
			return key(iPlayer, "CSA")
	
	return key(iPlayer, "REPUBLIC")

def defaultTitle(iPlayer):
	return desc(iPlayer, key(iPlayer, "DEFAULT"))
	
def specificTitle(iPlayer, lPreviousOwners=[]):
	iGameTurn = gc.getGame().getGameTurn()
	pPlayer = gc.getPlayer(iPlayer)
	tPlayer = gc.getTeam(pPlayer.getTeam())
	iCivicGovernment, iCivicOrganization, iCivicLabor, iCivicEconomy, iCivicReligion = getCivics(iPlayer)
	
	iNumCities = pPlayer.getNumCities()
	if iNumCities == 0: return defaultTitle(iPlayer)
	
	bReborn = pPlayer.isReborn()
	iReligion = pPlayer.getStateReligion()
	capital = gc.getPlayer(iPlayer).getCapitalCity()
	tCapitalCoords = capitalCoords(iPlayer)
	bAnarchy = pPlayer.isAnarchy()
	bEmpire = isEmpire(iPlayer)
	bCityStates = (iCivicGovernment == iCivicCityStates)
	bTheocracy = (iCivicGovernment == iCivicTheocracy)
	bResurrected = (sd.getResurrections(iPlayer) > 0)
	bCapitulated = isCapitulated(iPlayer)
	iAnarchyTurns = sd.getAnarchyTurns(iPlayer)
	iEra = pPlayer.getCurrentEra()
	iGameEra = gc.getGame().getCurrentEra()
	bWar = isAtWar(iPlayer)
	
	if iPlayer in lCityStatesStart:
		if not tPlayer.isHasTech(iAlphabet):
			bCityStates = True

	if iPlayer == iEgypt:
		if bResurrected:
			if sd.getResurrections(iPlayer) < 2:
				if iReligion == iIslam:
					if bTheocracy: return "TXT_KEY_CALIPHATE_ADJECTIVE"
					return "TXT_KEY_SULTANATE_ADJECTIVE"
				return "TXT_KEY_KINGDOM_ADJECTIVE"
				
		if iGreece in lPreviousOwners:
			return "TXT_KEY_CIV_EGYPT_PTOLEMAIC"
			
		if bCityStates:
			return "TXT_KEY_CITY_STATES_ADJECTIVE"
				
		if iEra == iAncient:
			if iAnarchyTurns == 0: return "TXT_KEY_CIV_EGYPT_OLD_KINGDOM"
			if iAnarchyTurns == 1: return "TXT_KEY_CIV_EGYPT_MIDDLE_KINGDOM"
			return "TXT_KEY_CIV_EGYPT_NEW_KINGDOM"
		
		if iEra == iClassical:
			return "TXT_KEY_CIV_EGYPT_NEW_KINGDOM"
			
	elif iPlayer == iIndia:
		if iReligion == iIslam:
			return "TXT_KEY_SULTANATE_OF"
			
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if iEra >= iRenaissance:
			return "TXT_KEY_CONFEDERACY_ADJECTIVE"
			
		if bCityStates:
			return "TXT_KEY_CIV_INDIA_MAHAJANAPADAS"
			
	elif iPlayer == iChina:
		if bEmpire:
			if iEra >= iIndustrial or utils.getScenario() == i1700AD:
				return "TXT_KEY_EMPIRE_OF"
			
			if iEra == iRenaissance and iGameTurn >= getTurnForYear(1400):
				return "TXT_KEY_EMPIRE_OF"
				
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iPlayer == iBabylonia:
		if bCityStates and not bEmpire:
			return "TXT_KEY_CITY_STATES_ADJECTIVE"
			
		if bEmpire and iEra > iAncient:
			return "TXT_KEY_CIV_BABYLONIA_NEO_EMPIRE"
			
	elif iPlayer == iGreece:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
	
		if bCityStates:				
			if bWar:
				return "TXT_KEY_CIV_GREECE_LEAGUE"
				
			return "TXT_KEY_CITY_STATES_ADJECTIVE"
			
	elif iPlayer == iPersia:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iPlayer == iPhoenicia:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if bCityStates:
			return "TXT_KEY_CITY_STATES_ADJECTIVE"
			
	elif iPlayer == iPolynesia:
		if isCapital(iPlayer, ["Kaua'i", "O'ahu", "Maui"]):
			return "TXT_KEY_KINGDOM_OF"
			
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iPlayer == iRome:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if bCityStates:
			return "TXT_KEY_REPUBLIC_ADJECTIVE"
			
	elif iPlayer == iJapan:
		if bEmpire:
			return "TXT_KEY_EMPIRE_OF"
			
		if iCivicOrganization == iCivicAbsolutism:
			return "TXT_KEY_EMPIRE_OF"
			
		if iEra >= iIndustrialism:
			return "TXT_KEY_EMPIRE_OF"
			
	elif iPlayer == iTamils:
		if iEra >= iMedieval:
			return "TXT_KEY_KINGDOM_OF"
		
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iPlayer == iEthiopia:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
	
	elif iPlayer == iKorea:
		if iEra >= iIndustrial:
			if bEmpire:
				return "TXT_KEY_EMPIRE_ADJECTIVE"
				
		if iEra == iClassical:
			if bEmpire:
				return "TXT_KEY_EMPIRE_OF"
				
		if iReligion >= 0:
			return "TXT_KEY_KINGDOM_OF"
			
	elif iPlayer == iMaya:
		if bReborn:
			if bEmpire:
				return "TXT_KEY_CIV_COLOMBIA_EMPIRE"
			
	elif iPlayer == iByzantium:
		if capital.getRegionID() != rAnatolia and tCapitalCoords != Areas.getCapital(iPlayer):
			return "TXT_KEY_CIV_BYZANTIUM_DESPOTATE"
		
		if not isCapital(iPlayer, ["Konstantinoupolis"]):
			return "TXT_KEY_EMPIRE_OF"
			
	elif iPlayer == iVikings:
		if iReligion < 0 and not tPlayer.isHasTech(iLiberalism):
			return "TXT_KEY_CIV_VIKINGS_NORSE_KINGDOMS"
			
		if bEmpire:
			if iEra <= iMedieval:
				return "TXT_KEY_CIV_VIKINGS_KALMAR_UNION"
				
			if iEra == iRenaissance or isCapital(iPlayer, ["Stockholm"]):
				return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iPlayer == iArabia:
		if bResurrected:
			return "TXT_KEY_KINGDOM_OF"
			
		if iReligion == iIslam and bTheocracy:
			return "TXT_KEY_CALIPHATE_ADJECTIVE"
			
	elif iPlayer == iTibet:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iPlayer == iKhmer:
		if iEra <= iRenaissance and isCapital(iPlayer, ["Angkor"]):
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if isCapital(iPlayer, ["Hanoi"]):
			return "TXT_KEY_CIV_KHMER_DAI_VIET"
			
	elif iPlayer == iIndonesia:
		if iReligion == iIslam:
			return "TXT_KEY_SULTANATE_OF"
			
	elif iPlayer == iMoors:
		if bCityStates:
			return "TXT_KEY_CIV_MOORS_TAIFAS"
			
		if utils.isPlotInArea(tCapitalCoords, vic.tIberiaTL, vic.tIberiaBR):
			if bEmpire:
				return "TXT_KEY_CALIPHATE_OF"
				
			return "TXT_KEY_CIV_MOORS_EMIRATE_OF"
			
		if bEmpire and iEra <= iRenaissance:
			if iReligion == iIslam and bTheocracy:
				return "TXT_KEY_CALIPHATE_ADJECTIVE"
				
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iPlayer == iSpain:
		if iReligion == iIslam:
			return "TXT_KEY_SULTANATE_OF"
			
		if bEmpire and iEra > iMedieval:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if iEra == iMedieval and isCapital(iPlayer, ["Barcelona", "Valencia"]):
			return "TXT_KEY_CIV_SPAIN_CROWN_OF"
			
	elif iPlayer == iFrance:
		if not tCapitalCoords in Areas.getNormalArea(iPlayer):
			return "TXT_KEY_CIV_FRANCE_EXILE"
			
		if iEra >= iIndustrial and bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if iCivicGovernment == iCivicAutocracy:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if not pHolyRome.isAlive() and iEra == iMedieval:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iPlayer == iEngland:
		if not utils.isPlotInCore(iPlayer, tCapitalCoords):
			return "TXT_KEY_CIV_ENGLAND_EXILE"
			
		if iEra == iMedieval and getMaster(iFrance) == iEngland:
			return "TXT_KEY_CIV_ENGLAND_ANGEVIN_EMPIRE"
			
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if tPlayer.isHasTech(iConstitution) and isAreaControlled(iPlayer, tBritainTL, tBritainBR, 3):
			return "TXT_KEY_CIV_ENGLAND_UNITED_KINGDOM_OF"
			
	elif iPlayer == iHolyRome:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if pGermany.isAlive():
			return "TXT_KEY_CIV_HOLY_ROME_ARCHDUCHY_OF"
		
	elif iPlayer == iRussia:
		if bEmpire and iEra >= iRenaissance:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if isAreaControlled(iPlayer, tEuropeanRussiaTL, tEuropeanRussiaBR, 5, tEuropeanRussiaExceptions):
			return "TXT_KEY_CIV_RUSSIA_TSARDOM_OF"

	elif iPlayer == iNetherlands:
		if bCityStates:
			return "TXT_KEY_CIV_NETHERLANDS_REPUBLIC"
			
		if not utils.isPlotInCore(iPlayer, tCapitalCoords):
			return "TXT_KEY_CIV_NETHERLANDS_EXILE"
			
		if bEmpire:
			if iEra >= iIndustrial:
				return "TXT_KEY_EMPIRE_ADJECTIVE"
				
			return "TXT_KEY_CIV_NETHERLANDS_UNITED_KINGDOM_OF"
			
	# Nothing for Mali
	
	elif iPlayer == iPoland:
		if iEra >= iRenaissance and bEmpire:
			return "TXT_KEY_CIV_POLAND_COMMONWEALTH"
			
		if isCapital(iPlayer, ["Kowno", "Medvegalis", "Wilno", "Ryga"]):
			return "TXT_KEY_CIV_POLAND_GRAND_DUCHY_OF"
			
	elif iPlayer == iPortugal:
		if utils.isPlotInCore(iBrazil, tCapitalCoords) and not pBrazil.isAlive():
			return "TXT_KEY_CIV_PORTUGAL_BRAZIL"
			
		if not utils.isPlotInArea(tCapitalCoords, vic.tIberiaTL, vic.tIberiaBR):
			return "TXT_KEY_CIV_PORTUGAL_EXILE"
			
		if bEmpire and iEra >= iIndustrial:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iPlayer == iInca:
		if not bResurrected:
			if bEmpire:
				return "TXT_KEY_CIV_INCA_FOUR_REGIONS"
				
	elif iPlayer == iItaly:
		if bCityStates:
			if bWar:
				return "TXT_KEY_CIV_ITALY_LEAGUE"
				
			return "TXT_KEY_CIV_ITALY_MARITIME_REPUBLICS"
			
		if not bResurrected:
			if iReligion == iCatholicism:
				if bTheocracy:
					return "TXT_KEY_CIV_ITALY_PAPAL_STATES"
				
				if isCapital(iItaly, ["Roma"]):
					return "TXT_KEY_CIV_ITALY_PAPAL_STATES"
					
			if not bEmpire:
				return "TXT_KEY_CIV_ITALY_DUCHY_OF"
			
	elif iPlayer == iMongolia:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if iEra <= iRenaissance:
			if iNumCities <= 3:
				return "TXT_KEY_CIV_MONGOLIA_KHAMAG"
				
			return "TXT_KEY_CIV_MONGOLIA_KHANATE"
			
	elif iPlayer == iAztecs:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if bCityStates:
			return "TXT_KEY_CIV_AZTECS_ALTEPETL"
				
	elif iPlayer == iMughals:
		if iEra == iMedieval and not bEmpire:
			return "TXT_KEY_SULTANATE_OF"
			
	elif iPlayer == iTurkey:
		if iReligion == iIslam:
			if bTheocracy:
				return "TXT_KEY_CALIPHATE_ADJECTIVE"
				
			if bEmpire:
				return "TXT_KEY_EMPIRE_ADJECTIVE"
				
			return "TXT_KEY_SULTANATE_ADJECTIVE"
			
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iPlayer == iThailand:
		if iEra >= iIndustrial and bEmpire:
			return "TXT_KEY_EMPIRE_OF"
			
	elif iPlayer == iGermany:
		if iEra >= iIndustrial and bEmpire:
			if getMaster(iHolyRome) == iGermany:
				return "TXT_KEY_CIV_GERMANY_GREATER_EMPIRE"
				
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iPlayer == iAmerica:
		if iCivicLabor == iCivicSlavery:
			return "TXT_KEY_CIV_AMERICA_CSA"
			
		if iCivicLabor == iCivicAgrarianism:
			return "TXT_KEY_CIV_AMERICA_CSA"
			
	elif iPlayer == iArgentina:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if tCapitalCoords != Areas.getCapital(iPlayer):
			return "TXT_KEY_CIV_ARGENTINA_CONFEDERATION"
			
	elif iPlayer == iBrazil:
		if bEmpire:
			return "TXT_KEY_EMPIRE_OF"
			
	return None
			
### Leader methods ###

def startingLeader(iPlayer):
	if iPlayer in dStartingLeaders[utils.getScenario()]: return dStartingLeaders[utils.getScenario()][iPlayer]
	
	return dStartingLeaders[i3000BC][iPlayer]
	
def leader(iPlayer):
	if iPlayer >= iNumPlayers: return None
	
	if not gc.getPlayer(iPlayer).isAlive(): return None
	
	if gc.getPlayer(iPlayer).isHuman(): return None
	
	pPlayer = gc.getPlayer(iPlayer)
	tPlayer = gc.getTeam(pPlayer.getTeam())
	bReborn = pPlayer.isReborn()
	iReligion = pPlayer.getStateReligion()
	capital = gc.getPlayer(iPlayer).getCapitalCity()
	tCapitalCoords = (capital.getX(), capital.getY())
	iCivicGovernment, iCivicOrganization, iCivicLabor, iCivicEconomy, iCivicReligion = getCivics(iPlayer)
	iGameTurn = gc.getGame().getGameTurn()
	bEmpire = isEmpire(iPlayer)
	bCityStates = (iCivicGovernment == iCivicCityStates or not gc.getTeam(pPlayer.getTeam()).isHasTech(iCodeOfLaws))
	bTheocracy = (iCivicGovernment == iCivicTheocracy)
	bResurrected = (sd.getResurrections(iPlayer) > 0)
	bMonarchy = not (isCommunist(iPlayer) or isFascist(iPlayer) or isRepublic(iPlayer))
	iAnarchyTurns = sd.getAnarchyTurns(iPlayer)
	iEra = pPlayer.getCurrentEra()
	iGameEra = gc.getGame().getCurrentEra()
	
	if iPlayer == iEgypt:
		if not bMonarchy and iEra >= iModern: return iNasser
		
		if bResurrected or utils.getScenario() >= i600AD: return iBaibars
		
		if tPlayer.isHasTech(iLiterature): return iCleopatra
		
	elif iPlayer == iIndia:
		if not bMonarchy and iEra >= iModern: return iGandhi
		
		if iEra >= iRenaissance: return iShahuji
		
		if tPlayer.isHasTech(iCurrency): return iChandragupta
		
	elif iPlayer == iChina:
		if isCommunist(iPlayer) or isRepublic(iPlayer) and iEra >= iIndustrial: return iMao
			
		if iEra >= iRenaissance and iGameTurn >= getTurnForYear(1400): return iHongwu
	
		if bResurrected: return iHongwu
		
		if utils.getScenario() >= i1700AD: return iHongwu
		
		if iEra >= iMedieval: return iTaizong
		
	elif iPlayer == iBabylonia:
		if iGameTurn >= getTurnForYear(-1600): return iHammurabi
		
	elif iPlayer == iGreece:
		if iEra >= iIndustrial: return iGeorge
		
		if bResurrected and iGameTurn >= getTurnForYear(1600): return iGeorge
	
		if bEmpire: return iAlexander
		
		if not bCityStates: return iAlexander
		
	elif iPlayer == iPersia:
		if bReborn:
			if iEra >= iModern: return iKhomeini
			
			return iAbbas
			
		if bEmpire:
			return iDarius
			
	elif iPlayer == iPhoenicia:
		if not bCityStates: return iHannibal
		
		if capital.getRegionID() not in [rMesopotamia, rAnatolia]: return iHannibal
		
	elif iPlayer == iRome:
		if not bEmpire and not bCityStates: return iAugustus
		
	elif iPlayer == iKorea:		
		if iEra >= iRenaissance: return iSejong
		
		if utils.getScenario() >= i1700AD: return iSejong
	
	elif iPlayer == iMaya:
		if bReborn:
			return iBolivar
		
	elif iPlayer == iJapan:
		if iEra >= iIndustrial: return iMeiji
		
		if tPlayer.isHasTech(iFeudalism): return iOdaNobunaga
		
	elif iPlayer == iEthiopia:
		if iEra >= iIndustrial: return iHaileSelassie
		
	elif iPlayer == iTamils:
		if iEra >= iRenaissance: return iKrishnaDevaRaya
		
	elif iPlayer == iByzantium:
		if iGameTurn >= getTurnForYear(1000): return iBasil
		
	elif iPlayer == iVikings:
		if iEra >= iModern: return iGerhardsen
		
		if iEra >= iRenaissance: return iGustav
		
	elif iPlayer == iArabia:
		if iGameTurn >= getTurnForYear(1000): return iSaladin
		
	elif iPlayer == iTibet:
		if iGameTurn >= getTurnForYear(1500): return iLobsangGyatso
		
	elif iPlayer == iIndonesia:
		if iEra >= iModern: return iSuharto
		
		if bEmpire: return iHayamWuruk
		
	elif iPlayer == iMoors:
		if not utils.isPlotInArea(tCapitalCoords, vic.tIberiaTL, vic.tIberiaBR): return iYaqub
		
	elif iPlayer == iSpain:
		if isFascist(iPlayer): return iFranco
		
		if 1 in sd.scriptDict['lFirstContactConquerors']: return iPhilip
		
	elif iPlayer == iFrance:
		if iEra >= iModern: return iDeGaulle
		
		if iEra >= iIndustrial: return iNapoleon
		
		if tPlayer.isHasTech(iNationalism): return iNapoleon
		
		if iEra >= iRenaissance: return iLouis
		
	elif iPlayer == iEngland:
		if iEra >= iModern: return iChurchill
		
		if iEra >= iIndustrial: return iVictoria
		
		if utils.getScenario() == i1700AD: return iVictoria
		
		if iEra >= iRenaissance: return iElizabeth
		
	elif iPlayer == iHolyRome:
		if iEra >= iIndustrial: return iFrancis
		
		if utils.getScenario() == i1700AD: return iFrancis
		
		if iEra >= iRenaissance: return iCharles
		
	elif iPlayer == iRussia:
		if iEra >= iIndustrial:
			if not bMonarchy: return iStalin
			
			return iNicholas
			
		if iEra >= iRenaissance:
			if iGameTurn >= getTurnForYear(1750): return iCatherine
			
			return iPeter
		
	elif iPlayer == iNetherlands:
		if iGameTurn >= getTurnForYear(1650): return iWilliam
			
	elif iPlayer == iPoland:
		if iEra >= iModern: return iWalesa
		
		if isFascist(iPlayer) or isCommunist(iPlayer): return iPilsudski
	
		if iEra >= iRenaissance: return iSobieski
		
		if utils.getScenario() == i1700AD: return iSobieski
		
	elif iPlayer == iPortugal:
		if iEra >= iIndustrial: return iMaria
		
		if tPlayer.isHasTech(iOptics): return iJoao
		
	elif iPlayer == iInca:
		if iEra >= iIndustrial: return iCastilla
		
		if bResurrected and iGameTurn >= getTurnForYear(1600): return iCastilla
	
	elif iPlayer == iItaly:
		if isFascist(iPlayer): return iMussolini
	
		if iEra >= iIndustrial: return iCavour
		
	elif iPlayer == iMongolia:
		if iGameTurn >= getTurnForYear(1400): return iKublaiKhan
		
	elif iPlayer == iAztecs:
		if bReborn:
			if bMonarchy: return iSantaAnna
			
			if isFascist(iPlayer): return iSantaAnna
			
			if iEra >= iModern: return iCardenas
			
			return iJuarez
			
	elif iPlayer == iMughals:
		if iEra >= iModern: return iBhutto
	
		if tPlayer.isHasTech(iPatronage): return iAkbar
		
	elif iPlayer == iTurkey:
		if not bMonarchy and iEra >= iIndustrial: return iAtaturk
		
		if tPlayer.isHasTech(iPatronage): return iSuleiman
				
	elif iPlayer == iThailand:
		if iEra >= iIndustrial: return iMongkut

	elif iPlayer == iGermany:
		if isFascist(iPlayer): return iHitler
		
		if tPlayer.isHasTech(iNationalism): return iBismarck
		
	elif iPlayer == iAmerica:
		if iEra >= iModern: return iRoosevelt
		
		if iGameTurn >= getTurnForYear(1850): return iLincoln
		
	elif iPlayer == iArgentina:
		if iEra >= iModern: return iPeron
	
	elif iPlayer == iBrazil:
		if iEra >= iModern: return iVargas
		
	elif iPlayer == iCanada:
		if iEra >= iModern: return iTrudeau
		
	return startingLeader(iPlayer)
		
	
def leaderName(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = pPlayer.getLeader()
	
	iGameTurn = gc.getGame().getGameTurn()
	
	if iPlayer == iChina:
		if iLeader == iHongwu:
			if iGameTurn >= getTurnForYear(1700):
				return "TXT_KEY_LEADER_KANGXI"
				
	elif iPlayer == iIndia:
		if iLeader == iKrishnaDevaRaya:
			if iGameTurn >= getTurnForYear(1700):
				return "TXT_KEY_LEADER_TIPU_SULTAN"
				
	return None