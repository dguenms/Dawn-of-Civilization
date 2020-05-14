# coding: utf-8

from CvPythonExtensions import *
import CvUtil
import PyHelpers
from Consts import *
import Victory as vic
from StoredData import data
from RFCUtils import utils
import CityNameManager as cnm
import Areas

### Constants ###

gc = CyGlobalContext()
localText = CyTranslator()

encoding = "utf-8"

tBrazilTL = (32, 14)
tBrazilBR = (43, 30)
tNCAmericaTL = (3, 33)
tNCAmericaBR = (37, 63)

tBritainTL = (48, 53)
tBritainBR = (54, 60)

tEuropeanRussiaTL = (68, 50)
tEuropeanRussiaBR = (80, 62)
tEuropeanRussiaExceptions = ((68, 59), (68, 60), (68, 61), (68, 62))

tAnatoliaTL = (69, 41)
tAnatoliaBR = (75, 45)
iTurkicEastWestBorder = 89

tColombiaTL = (24, 26)
tColombiaBR = (28, 32)

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
	iBoers : "TXT_KEY_CIV_BOER_SOUTH_AFRICA",
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
	iChina : {
		iKorea : "TXT_KEY_CIV_CHINESE_KOREA",
		iTurks : "TXT_KEY_CIV_CHINESE_TURKS",
		iMongolia : "TXT_KEY_CIV_CHINESE_MONGOLIA",
	},
	iGreece : {
		iIndia : "TXT_KEY_CIV_GREEK_INDIA",
		iEgypt : "TXT_KEY_CIV_GREEK_EGYPT",
		iPersia : "TXT_KEY_CIV_GREEK_PERSIA",
		iRome : "TXT_KEY_CIV_GREEK_ROME",
	},
	iIndia : {
		iAztecs: "TXT_KEY_CIV_INDIAN_AZTECS",
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
		iIndia : "TXT_KEY_CIV_JAPANESE_INDIA",
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
		iMamluks : "TXT_KEY_CIV_BYZANTINE_EGYPT",
	},
	iVikings : {
		iEngland : "TXT_KEY_CIV_VIKING_ENGLAND",
		iRussia : "TXT_KEY_CIV_VIKING_RUSSIA",
	},
	iArabia : {
		iOttomans : "TXT_KEY_CIV_ARABIAN_OTTOMANS",
		iMughals : "TXT_KEY_CIV_ARABIAN_MUGHALS",
		iIsrael : "TXT_KEY_CIV_ARABIAN_ISRAEL",
	},
	iMoors : {
		iArabia : "TXT_KEY_CIV_MOORISH_ARABIA",
		iMali : "TXT_KEY_CIV_MOORISH_MALI",
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
		iMamluks : "TXT_KEY_MANDATE_OF",
		iMali : "TXT_KEY_CIV_FRENCH_MALI",
		iPortugal : "TXT_KEY_CIV_FRANCE_DEPARTEMENTS_OF",
		iInca : "TXT_KEY_CIV_FRENCH_INCA",
		iNigeria : "TXT_KEY_CIV_FRENCH_NIGERIA",
		iAztecs : "TXT_KEY_CIV_FRENCH_AZTECS",
		iMughals : "TXT_KEY_MANDATE_OF",
		iCongo : "TXT_KEY_ADJECTIVE_TITLE",
		iOttomans : "TXT_KEY_MANDATE_OF",
		iAmerica : "TXT_KEY_CIV_FRENCH_AMERICA",
		iIsrael : "TXT_KEY_CIV_FRENCH_ISRAEL",
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
		iIndonesia : "TXT_KEY_CIV_ENGLISH_INDONESIA",
		iFrance : "TXT_KEY_CIV_ENGLISH_FRANCE",
		iHolyRome : "TXT_KEY_CIV_ENGLISH_HOLY_ROME",
		iNigeria : "TXT_KEY_CIV_ENGLISH_NIGERIA",
		iGermany : "TXT_KEY_CIV_ENGLISH_GERMANY",
		iNetherlands : "TXT_KEY_CIV_ENGLISH_NETHERLANDS",
		iMamluks : "TXT_KEY_MANDATE_OF",
		iMali : "TXT_KEY_CIV_ENGLISH_MALI",
		iOttomans : "TXT_KEY_MANDATE_OF",
		iAmerica : "TXT_KEY_CIV_ENGLISH_AMERICA",
		iZimbabwe : "TXT_KEY_CIV_ENGLISH_ZIMBABWE",
		iIsrael : "TXT_KEY_CIV_ENGLISH_ISRAEL",
	},
	iHolyRome : {
		iItaly : "TXT_KEY_CIV_HOLY_ROMAN_ITALY",
		iFrance : "TXT_KEY_CIV_HOLY_ROMAN_FRANCE",
		iNetherlands : "TXT_KEY_CIV_HOLY_ROMAN_NETHERLANDS",
		iByzantium : "TXT_KEY_CIV_HOLY_ROMAN_BYZANTIUM",
		iPoland : "TXT_KEY_CIV_HOLY_ROMAN_POLAND",
	},
	iRussia : {
		iTurks : "TXT_KEY_ADJECTIVE_TITLE",
		iPoland : "TXT_KEY_CIV_RUSSIAN_POLAND",
		iAmerica : "TXT_KEY_ADJECTIVE_TITLE",
	},
	iNetherlands : {
		iIndonesia : "TXT_KEY_CIV_DUTCH_INDONESIA",
		iMali : "TXT_KEY_CIV_DUTCH_MALI",
		iEthiopia : "TXT_KEY_CIV_DUTCH_ETHIOPIA",
		iCongo : "TXT_KEY_CIV_DUTCH_CONGO",
		iAmerica : "TXT_KEY_CIV_DUTCH_AMERICA",
		iBrazil : "TXT_KEY_CIV_DUTCH_BRAZIL",
	},
	iPortugal : {
		iIndia : "TXT_KEY_CIV_PORTUGUESE_INDIA",
		iIndonesia : "TXT_KEY_CIV_PORTUGUESE_INDIA",
		iMali : "TXT_KEY_CIV_PORTUGUESE_MALI",
		iCongo : "TXT_KEY_CIV_PORTUGUESE_CONGO",
		iBrazil : "TXT_KEY_CIV_PORTUGUESE_BRAZIL",
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
		iOttomans : "TXT_KEY_CIV_MONGOL_OTTOMANS",
		iMughals : "TXT_KEY_CIV_MONGOL_MUGHALS",
		iMamluks : "TXT_KEY_CIV_MONGOL_ILKHANATE",
	},
	iMughals : {
		iIndia : "TXT_KEY_CIV_MUGHAL_INDIA",
	},
	iOttomans : {
		iEgypt : "TXT_KEY_CIV_OTTOMAN_EGYPT",
		iBabylonia : "TXT_KEY_CIV_OTTOMAN_BABYLONIA",
		iPersia : "TXT_KEY_CIV_OTTOMAN_PERSIA",
		iGreece : "TXT_KEY_CIV_OTTOMAN_GREECE",
		iPhoenicia : "TXT_KEY_CIV_OTTOMAN_PHOENICIA",
		iEthiopia : "TXT_KEY_CIV_OTTOMAN_ETHIOPIA",
		iByzantium : "TXT_KEY_CIV_OTTOMAN_BYZANTIUM",
		iArabia : "TXT_KEY_CIV_OTTOMAN_ARABIA",
		iIndonesia : "TXT_KEY_CIV_OTTOMAN_INDONESIA",
		iRussia : "TXT_KEY_CIV_OTTOMAN_RUSSIA",
		iKievanRus : "TXT_KEY_CIV_OTTOMAN_RUS'",
		iHungary : "TXT_KEY_CIV_OTTOMAN_HUNGARY",
		iIsrael : "TXT_KEY_CIV_OTTOMAN_ISRAEL",
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
	iYemen : {
		iEngland : "TXT_KEY_CIV_YEMEN_ENGLAND",
		iArabia : "TXT_KEY_CIV_YEMEN_ARABIA",
	},
	iBoers	: {
		iEngland : "TXT_KEY_CIV_BOER_ENGLAND",
		iNetherlands : "TXT_KEY_CIV_BOER_NETHERLANDS",
	}
}

dMasterTitles = {
	iChina : "TXT_KEY_CIV_CHINESE_VASSAL",
	iIndia : "TXT_KEY_CIV_INDIAN_VASSAL",
	iPersia : "TXT_KEY_CIV_PERSIAN_VASSAL",
	iRome : "TXT_KEY_CIV_ROMAN_VASSAL",
	iJapan : "TXT_KEY_CIV_JAPANESE_VASSAL",
	iByzantium : "TXT_KEY_CIV_BYZANTINE_VASSAL",
	iTurks : "TXT_KEY_CIV_TURKIC_VASSAL",
	iArabia : "TXT_KEY_CIV_ARABIAN_VASSAL",
	iTibet : "TXT_KEY_CIV_TIBETAN_VASSAL",
	iIndonesia : "TXT_KEY_CIV_INDONESIAN_VASSAL",
	iMoors : "TXT_KEY_CIV_ARABIAN_VASSAL",
	iSpain : "TXT_KEY_CIV_SPANISH_VASSAL",
	iFrance : "TXT_KEY_ADJECTIVE_TITLE",
	iEngland : "TXT_KEY_CIV_ENGLISH_VASSAL",
	iRussia : "TXT_KEY_CIV_RUSSIAN_VASSAL",
	iNetherlands : "TXT_KEY_ADJECTIVE_TITLE",
	iPortugal : "TXT_KEY_ADJECTIVE_TITLE",
	iMongolia : "TXT_KEY_CIV_MONGOL_VASSAL",
	iMughals : "TXT_KEY_CIV_MUGHAL_VASSAL",
	iOttomans : "TXT_KEY_CIV_OTTOMAN_VASSAL",
	iThailand : "TXT_KEY_CIV_THAI_VASSAL",
}

dCommunistVassalTitlesGeneric = {
	iRussia : "TXT_KEY_CIV_RUSSIA_SOVIET",
}

dCommunistVassalTitles = {
	iRussia : {
		iChina : "TXT_KEY_CIV_RUSSIA_SOVIET_REPUBLIC_ADJECTIVE",
		iTurks : "TXT_KEY_CIV_RUSSIA_SOVIET_TURKS",
		iJapan : "TXT_KEY_CIV_RUSSIA_SOVIET_JAPAN",
		iOttomans : "TXT_KEY_CIV_RUSSIA_SOVIET_OTTOMANS",
		iGermany : "TXT_KEY_CIV_RUSSIA_SOVIET_GERMANY",
		iKievanRus : "TXT_KEY_CIV_RUSSIA_RUS'",
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
		iMamluks : "TXT_KEY_CIV_GERMANY_REICHSPROTEKTORAT",
		iMali : "TXT_KEY_CIV_GERMANY_NAZI_MALI",
		iPoland : "TXT_KEY_CIV_GERMANY_NAZI_POLAND",
		iPortugal : "TXT_KEY_CIV_GERMANY_REICHSKOMMISSARIAT",
		iMughals : "TXT_KEY_CIV_GERMANY_NAZI_MUGHALS",
		iOttomans : "TXT_KEY_CIV_GERMANY_REICHSKOMMISSARIAT",
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
		iIndonesia : "TXT_KEY_CIV_CHINESE_ADJECTIVE_INDONESIA",
		iMongolia : "TXT_KEY_CIV_CHINESE_ADJECTIVE_MONGOLIA",
		iOttomans : "TXT_KEY_CIV_CHINESE_ADJECTIVE_OTTOMANS",
		iTibet : "TXT_KEY_CIV_CHINESE_ADJECTIVE_TIBET",
		iMamluks : "TXT_KEY_CIV_CHINESE_ADJECTIVE_EGYPT",
		iVietnam : "TXT_KEY_CIV_CHINESE_ADJECTIVE_VIETNAM",
	},
}

dForeignNames = {
	iGreece : {
		iTurks : "TXT_KEY_CIV_GREEK_NAME_TURKS",
	},
	iPersia : {
		iByzantium : "TXT_KEY_CIV_PERSIAN_NAME_BYZANTIUM",
		iTurks : "TXT_KEY_CIV_PERSIAN_NAME_TURKS",
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
		iTurks : "TXT_KEY_CIV_ROMAN_NAME_TURKS",
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
		iOttomans : "TXT_KEY_CIV_ROMAN_NAME_OTTOMANS",
		iThailand : "TXT_KEY_CIV_ROMAN_NAME_THAILAND",
		iMamluks : "TXT_KEY_CIV_ROMAN_NAME_EGYPT",
	},
	iArabia : {
		iEgypt : "TXT_KEY_CIV_ARABIAN_NAME_EGYPT",
		iBabylonia : "TXT_KEY_CIV_ARABIAN_NAME_BABYLONIA",
		iPersia : "TXT_KEY_CIV_ARABIAN_NAME_PERSIA",
		iPhoenicia : "TXT_KEY_CIV_ARABIAN_NAME_CARTHAGE",
		iRome : "TXT_KEY_CIV_ARABIAN_NAME_ROME",
		iEthiopia : "TXT_KEY_CIV_ARABIAN_NAME_ETHIOPIA",
		iByzantium : "TXT_KEY_CIV_ARABIAN_NAME_BYZANTIUM",
		iTurks : "TXT_KEY_CIV_ARABIAN_NAME_TURKS",
		iArabia : "TXT_KEY_CIV_ARABIAN_NAME_ARABIA",
		iIndonesia : "TXT_KEY_CIV_ARABIAN_NAME_INDONESIA",
		iMoors : "TXT_KEY_CIV_ARABIAN_NAME_MOORS",
		iSpain : "TXT_KEY_CIV_ARABIAN_NAME_SPAIN",
		iPortugal : "TXT_KEY_CIV_ARABIAN_NAME_PORTUGAL",
		iMamluks : "TXT_KEY_CIV_ARABIAN_NAME_EGYPT",
	},
	iTibet : {
		iChina : "TXT_KEY_CIV_TIBETAN_NAME_CHINA",
		iIndia : "TXT_KEY_CIV_TIBETAN_NAME_INDIA",
		iTurks : "TXT_KEY_CIV_TIBETAN_NAME_TURKS",
		iMongolia : "TXT_KEY_CIV_TIBETAN_NAME_MONGOLIA",
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
		iPortugal : "TXT_KEY_CIV_ARABIAN_NAME_PORTUGAL",
		iMamluks : "TXT_KEY_CIV_ARABIAN_NAME_EGYPT",
	},
	iSpain : {
		iKhmer : "TXT_KEY_CIV_SPANISH_NAME_KHMER",
		iAztecs : "TXT_KEY_CIV_SPANISH_NAME_AZTECS",
		iMughals : "TXT_KEY_CIV_SPANISH_NAME_MUGHALS",
	},
	iFrance : {
		iKhmer : "TXT_KEY_CIV_FRENCH_NAME_KHMER",
		iMughals : "TXT_KEY_CIV_FRENCH_NAME_MUGHALS",
		iVietnam : "TXT_KEY_CIV_FRENCH_NAME_VIETNAM",
	},
	iEngland : {
		iKhmer : "TXT_KEY_CIV_ENGLISH_NAME_KHMER",
		iMughals : "TXT_KEY_CIV_ENGLISH_NAME_MUGHALS",
	},
	iRussia : {
		iPersia : "TXT_KEY_CIV_RUSSIAN_NAME_PERSIA",
	},
	iMongolia : {
		iTurks : "TXT_KEY_CIV_MONGOL_NAME_TURKS"
	},
	iGermany : {
		iMoors : "TXT_KEY_CIV_GERMAN_NAME_MOORS",
	},
}

lRepublicOf = [iEgypt, iIndia, iChina, iPersia, iJapan, iEthiopia, iKorea, iVikings, iTurks, iKhazars, iTibet, iIndonesia, iKhmer, iHolyRome, iMali, iPoland, iMughals, iOttomans, iThailand, iMamluks, iPhilippines, iBoers, iVietnam, iZimbabwe, iSwahili, iSweden, iNigeria, iOman, iChad, iCeltia]
lRepublicAdj = [iBabylonia, iRome, iMoors, iSpain, iFrance, iPortugal, iInca, iItaly, iAztecs, iArgentina, iAustralia, iManchuria, iHungary]

lSocialistRepublicOf = [iMoors, iHolyRome, iBrazil, iVikings, iMamluks, iPhilippines, iBoers, iVietnam, iZimbabwe, iSwahili, iSweden, iNigeria]
lSocialistRepublicAdj = [iPersia, iTurks, iKhazars, iItaly, iAztecs, iArgentina, iAustralia]

lPeoplesRepublicOf = [iIndia, iChina, iPolynesia, iJapan, iTibet, iIndonesia, iMali, iPoland, iMughals, iThailand, iCongo, iMamluks, iPhilippines, iBoers, iVietnam, iZimbabwe, iSwahili, iSweden, iNigeria, iOman, iChad]
lPeoplesRepublicAdj = [iTamils, iByzantium, iMongolia, iAustralia, iManchuria, iKievanRus, iHungary]

lIslamicRepublicOf = [iIndia, iPersia, iMali, iMughals]

lCityStatesStart = [iRome, iCarthage, iGreece, iIndia, iMaya, iAztecs]

dEmpireThreshold = {
	iNubia: 3,
	iCarthage : 4,
	iIndonesia : 4,
	iBurma : 2,
	iKhazars : 6,
	iTeotihuacan : 3,
	iKorea : 4,
	iRussia : 8,
	iHolyRome : 3,
	iGermany : 4,
	iItaly : 4,
	iInca : 3,
	iMongolia : 6,
	iPoland : 3,
	iChad : 2,
	iMoors : 3,
	iOman : 4,
	iTibet : 2,
	iPolynesia : 3,
	iTamils : 3,
	iNigeria : 3,
	iSwahili : 4,
}

lChristianity = [iCatholicism, iOrthodoxy, iProtestantism]

lRespawnNameChanges = [iHolyRome, iInca, iAztecs, iMali, iKievanRus, iCarthage]
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
	iMoors : "TXT_KEY_CIV_MOROCCO_SHORT_DESC",
	iBurma : "TXT_KEY_CIV_BURMA_MYANMAR_SHORT_DESC",
	iKievanRus : "TXT_KEY_CIV_UKRAINE_SHORT_DESC",
	iMississippi : "TXT_KEY_CIV_HOPEWELL_SHORT_DESC",
}

dAdjectiveChanges = {
	iPhoenicia : "TXT_KEY_CIV_CARTHAGE_ADJECTIVE",
	iAztecs : "TXT_KEY_CIV_MEXICO_ADJECTIVE",
	iInca : "TXT_KEY_CIV_PERU_ADJECTIVE",
	iHolyRome : "TXT_KEY_CIV_AUSTRIA_ADJECTIVE",
	iMali : "TXT_KEY_CIV_SONGHAI_ADJECTIVE",
	iMughals : "TXT_KEY_CIV_PAKISTAN_ADJECTIVE",
	iMoors : "TXT_KEY_CIV_MOROCCO_ADJECTIVE",
	iKievanRus : "TXT_KEY_CIV_UKRAINE_ADJECTIVE",
	iMississippi : "TXT_KEY_CIV_HOPEWELL_ADJECTIVE",
}

dCapitals = {
	iPolynesia : ["Kaua'i", "O'ahu", "Maui", "Manu'a", "Niue"],
	iBabylonia : ["Ninua", "Kalhu"],
	iCeltia : ["Hallstat", "La Tene", "&#193;th Cliath", "D&#249;n &#200;ideann", "Dublin", "Edinburgh"],
	iTeotihuacan : ["Tollan"],
	iByzantium : ["Dyrrachion", "Athena", "Konstantinoupolis"],
	iVikings : ["Oslo", "Nidaros", "Roskilde"],
	iKhmer : ["Pagan", "Dali", "Angkor"],
	iHolyRome : ["Buda"],
	iRussia : ["Moskva", "Kiev"],
	iItaly : ["Fiorenza", "Roma"],
	iTamils : ["Madurai", "Thiruvananthapuram", "Cochin", "Kozhikode"],
	iArabia : ["Dimashq"],
	iSpain : ["La Paz", "Barcelona", "Valencia"],
	iPhilippines : ["Tondo", "Butuan"],
	iPoland : ["Kowno", "Medvegalis", "Wilno", "Ryga"],
	iNigeria : ["Oyo", "Ife", "Njimi", "Igbo-Ukwu", "Wukari"],
	iNetherlands : ["Brussels", "Antwerpen"],
	iBoers : ["Pretoria", "Johannesburg", "Pietermaritzburg", "Durban"],
	iNubia : ["Kerma"]
}

dCapitalLocations = findCapitalLocations(dCapitals)

dStartingLeaders = [
# 3000 BC
{
	iEgypt : iRamesses,
	iIndia : iAsoka,
	iBabylonia : iSargon,
	iHarappa : iVatavelli,
	iNorteChico : iWiracocha,
	iNubia : iPiye,
	iChina : iQinShiHuang,
	iGreece : iPericles,
	iOlmecs : iTezcatlipoca,
	iPersia : iCyrus,
	iCarthage : iHiram,
	iPolynesia : iAhoeitu,
	iCeltia : iBrennus,
	iRome : iJuliusCaesar,
	iMaya : iPacal,
	iJapan : iKammu,
	iTamils : iRajendra,
	iEthiopia : iEzana,
	iVietnam : iTrung,
	iTeotihuacan : iAtlatlCauac,
	iInuit : iAua,
	iMississippi : iRedHorn,
	iKorea : iWangKon,
	iTiwanaku : iMalkuHuyustus,
	iByzantium : iJustinian,
	iWari : iWariCapac,
	iVikings : iRagnar,
	iTurks : iBumin,
	iArabia : iHarun,
	iTibet : iSongtsen,
	iKhmer : iSuryavarman,
	iMuisca : iSacuamanchica,
	iIndonesia : iDharmasetu,
	iBurma : iAnawrahta,
	iKhazars : iBulan,
	iChad : iDunama,
	iMoors : iRahman,
	iSpain : iIsabella,
	iFrance : iCharlemagne,
	iOman : iSaif,
	iYemen : iArwa,
	iEngland : iAlfred,
	iHolyRome : iBarbarossa,
	iKievanRus : iYaroslav,
	iHungary : iIstvan,
	iRussia : iIvan,
	iNetherlands : iWillemVanOranje,
	iPhilippines : iLapuLapu,
	iChimu : iTacaynamo,
	iSwahili : iShirazi,
	iMamluks : iSaladin,
	iMali : iMansaMusa,
	iPoland : iCasimir,
	iZimbabwe : iRusvingo,
	iPortugal : iAfonso,
	iInca : iHuaynaCapac,
	iItaly : iLorenzo,
	iNigeria : iOduduwa,
	iMongolia : iGenghisKhan,
	iAztecs : iMontezuma,
	iMughals : iTughluq,
	iOttomans : iMehmed,
	iThailand : iNaresuan,
	iCongo : iMbemba,
	iSweden : iGustavVasa,
	iManchuria : iKangxi,
	iGermany : iFrederick,
	iAmerica : iWashington,
	iAustralia : iCurtin,
	iArgentina : iSanMartin,
	iBrazil : iPedro,
	iBoers : iKruger,
	iCanada : iMacDonald,
	iIsrael : iBenGurion,
},
# 600 AD
{
	iChina : iTaizong,
	iCeltia : iRobert,
},
# 1700 AD
{
	iChina : iHongwu,
	iIndia : iShahuji,
	iCeltia : iCollins,
	iPersia : iAbbas,
	iTamils : iKrishnaDevaRaya,
	iKorea : iSejong,
	iVietnam : iHoChiMinh,
	iJapan : iOdaNobunaga,
	iTurks : iTamerlane,
	iVikings : iChristian,
	iBurma : iBayinnuang,
	iMoors: iYaqub,
	iSpain : iPhilip,
	iFrance : iLouis,
	iEngland : iVictoria,
	iHolyRome : iFrancis,
	iKievanRus : iBohdan,
	iRussia : iPeter,
	iSweden : iKarl,
	iNetherlands : iWilliam,
	iPoland : iSobieski,
	iPortugal : iJoao,
	iMughals : iAkbar,
	iOttomans : iSuleiman,
	iGermany : iFrederick,
}]

### Event handlers

def setup():			
	iScenario = utils.getScenario()
	
	if iScenario == i600AD:
		data.players[iChina].iAnarchyTurns += 3
		
	elif iScenario == i1700AD:
		utils.setReborn(iNubia, True)
		utils.setReborn(iChad, True)
		# data.players[iEgypt].iResurrections += 1
		
		for iPlayer in [iMoors, iKievanRus]:
			nameChange(iPlayer)
			adjectiveChange(iPlayer)
	
	for iPlayer in range(iNumPlayers):
		setDesc(iPlayer, peoplesName(iPlayer))
		
		if gc.getPlayer(iPlayer).getNumCities() > 0:
			checkName(iPlayer)
		
		if (tBirth[iPlayer] >= gc.getGame().getGameTurnYear() or gc.getPlayer(iPlayer).getNumCities() > 0) and not gc.getPlayer(iPlayer).isHuman():
			setLeader(iPlayer, startingLeader(iPlayer))
		
def onCivRespawn(iPlayer, tOriginalOwners):
	data.players[iPlayer].iResurrections += 1
	
	if iPlayer in lRespawnNameChanges:
	
		nameChange(iPlayer)
		adjectiveChange(iPlayer)
		
		if iPlayer == iCarthage:
			if gc.getGame().getGameTurnYear() >= 1956:
				setShort(iPlayer, text("TXT_KEY_CIV_TUNISIA_SHORT_DESC"))
				setAdjective(iPlayer, text("TXT_KEY_CIV_TUNISIA_ADJECTIVE"))
				
	setDesc(iPlayer, defaultTitle(iPlayer))
	checkName(iPlayer)
	checkLeader(iPlayer)
	
def onVassalState(iMaster, iVassal):
	if iVassal in lVassalNameChanges:
		if iVassal == iMughals and iMaster not in lCivGroups[0]: return
	
		data.players[iVassal].iResurrections += 1
		nameChange(iVassal)
		adjectiveChange(iVassal)
		
	checkName(iVassal)
	
def onPlayerChangeStateReligion(iPlayer, iReligion):
	if iPlayer in lChristianityNameChanges and iReligion in lChristianity:
		data.players[iPlayer].iResurrections += 1
		nameChange(iPlayer)
		adjectiveChange(iPlayer)
		
	checkName(iPlayer)
	
def onRevolution(iPlayer):
	data.players[iPlayer].iAnarchyTurns += 1
	
	if iPlayer == iMughals and isRepublic(iPlayer):
		nameChange(iPlayer)
	
	if iPlayer == iBurma:
		if isCommunist(iPlayer) or isFascist(iPlayer) or isRepublic(iPlayer):
			utils.setReborn(iPlayer, True)
		iGovernment, iLegitimacy, _, _, _, _ = getCivics(iPlayer)
		if iGovernment == iDespotism and iLegitimacy in [iCentralism, iRevolutionism, iConstitution]:
			nameChange(iPlayer)
			
	if iPlayer == iNubia:
		if not pNubia.isReborn() and pNubia.getStateReligion() == iIslam:
			utils.setReborn(iPlayer, True)
			
	checkName(iPlayer)
	
	for iLoopPlayer in range(iNumPlayers):
		if gc.getTeam(iLoopPlayer).isVassal(iPlayer):
			checkName(iLoopPlayer)
	
def onCityAcquired(iPreviousOwner, iNewOwner):
	checkName(iPreviousOwner)
	checkName(iNewOwner)
	
def onCityRazed(iOwner):
	checkName(iOwner)
	
def onCityBuilt(iOwner, city):
	checkName(iOwner)
	
def onTechAcquired(iPlayer, iTech):
	iEra = gc.getTechInfo(iTech).getEra()
	
	if iPlayer == iVikings:
		if iEra == iRenaissance:
			if isCapital(iPlayer, ["Oslo", "Nidaros"]):
				setShort(iVikings, text("TXT_KEY_CIV_NORWAY_SHORT_DESC"))
				setAdjective(iVikings, text("TXT_KEY_CIV_NORWAY_ADJECTIVE"))
			
			elif isCapital(iPlayer, ["Roskilde"]):
				setShort(iVikings, text("TXT_KEY_CIV_DENMARK_SHORT_DESC"))
				setAdjective(iVikings, text("TXT_KEY_CIV_DENMARK_ADJECTIVE"))
				
	elif iPlayer == iMoors:
		if iEra == iIndustrial:
			capital = gc.getPlayer(iPlayer).getCapitalCity()
			
			if capital and capital.getRegionID() != rIberia:
				nameChange(iPlayer)
				adjectiveChange(iPlayer)
			else:
				setShort(iPlayer, short(iPlayer))
				setAdjective(iPlayer, civAdjective(iPlayer))
				
	checkName(iPlayer)
	
def onPalaceMoved(iPlayer):
	capital = gc.getPlayer(iPlayer).getCapitalCity()
	iEra = gc.getPlayer(iPlayer).getCurrentEra()

	if iPlayer == iPhoenicia:
		if capital.getRegionID() not in [rMesopotamia, rAnatolia]:
			nameChange(iPlayer)
			adjectiveChange(iPlayer)
		else:
			setShort(iPlayer, short(iPlayer))
			setAdjective(iPlayer, civAdjective(iPlayer))
			
	elif iPlayer == iVikings:
		if iEra >= iRenaissance:
			if isCapital(iPlayer, ["Oslo", "Nidaros"]):
				setShort(iVikings, text("TXT_KEY_CIV_NORWAY_SHORT_DESC"))
				setAdjective(iVikings, text("TXT_KEY_CIV_NORWAY_ADJECTIVE"))
			
			elif isCapital(iPlayer, ["Roskilde"]):
				setShort(iVikings, text("TXT_KEY_CIV_DENMARK_SHORT_DESC"))
				setAdjective(iVikings, text("TXT_KEY_CIV_DENMARK_ADJECTIVE"))
				
	elif iPlayer == iMoors:
		if iEra >= iIndustrial:
			if capital.getRegionID() != rIberia:
				nameChange(iPlayer)
				adjectiveChange(iPlayer)
			else:
				setShort(iPlayer, short(iPlayer))
				setAdjective(iPlayer, civAdjective(iPlayer))
			
	checkName(iPlayer)
	
def onReligionFounded(iPlayer):
	checkName(iPlayer)
	
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
	try:
		gc.getPlayer(iPlayer).setCivDescription(sName)
	except:
		pass
	
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
	return localText.getText(sTextKey.encode(encoding), tInput)
	
def desc(iPlayer, sTextKey=str("%s1")):
	if isVassal(iPlayer): return text(sTextKey, (name(iPlayer), adjective(iPlayer), name(iPlayer, True), adjective(iPlayer, True)))

	return text(sTextKey, (name(iPlayer), adjective(iPlayer)))

def short(iPlayer):
	return gc.getPlayer(iPlayer).getCivilizationShortDescription(0)
	
def civAdjective(iPlayer):
	return gc.getPlayer(iPlayer).getCivilizationAdjective(0)

def capitalName(iPlayer):
	capital = gc.getPlayer(iPlayer).getCapitalCity()
	if capital: 
		sCapitalName = capital.getName()
		if iPlayer not in [iBurma, iNubia]:
			sCapitalName = cnm.getRenameName(iEngland, sCapitalName)
		if sCapitalName: return sCapitalName
		else: return capital.getName()
	
	return short(iPlayer)
	
def nameChange(iPlayer):
	if iPlayer in dNameChanges:
		setShort(iPlayer, text(dNameChanges[iPlayer]))
	
def adjectiveChange(iPlayer):
	if iPlayer in dAdjectiveChanges:
		setAdjective(iPlayer, text(dAdjectiveChanges[iPlayer]))
	
def getColumn(iPlayer):
	lTechs = [gc.getTechInfo(iTech).getGridX() for iTech in range(iNumTechs) if gc.getTeam(iPlayer).isHasTech(iTech)]
	if not lTechs: return 0
	return max(lTechs)
	
### Utility methods for civilization status ###

def getCivics(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	return (pPlayer.getCivics(i) for i in range(6))

def isCommunist(iPlayer):
	iGovernment, iLegitimacy, iSociety, iEconomy, _, _ = getCivics(iPlayer)
	
	if iLegitimacy == iVassalage: return False
	
	if iEconomy == iCentralPlanning: return True
	
	if iGovernment == iStateParty and iSociety != iTotalitarianism and iEconomy not in [iMerchantTrade, iFreeEnterprise]: return True
		
	return False
	
def isFascist(iPlayer):
	iGovernment, _, iSociety, _, _, _ = getCivics(iPlayer)
	
	if iSociety == iTotalitarianism: return True
	
	if iGovernment == iStateParty: return True
		
	return False
	
def isRepublic(iPlayer):
	iGovernment, iLegitimacy, _, _, _, _ = getCivics(iPlayer)
	
	if iGovernment == iDemocracy: return True
	
	if iGovernment in [iDespotism, iRepublic, iElective] and iLegitimacy == iConstitution: return True
	
	return False
	
def isCityStates(iPlayer):
	iGovernment, iLegitimacy, _, _, _, _ = getCivics(iPlayer)
	
	if iLegitimacy not in [iAuthority, iCitizenship, iCentralism]: return False
	
	if iGovernment in [iRepublic, iElective, iDemocracy]: return True
	
	if iGovernment == iChiefdom and iPlayer in lCityStatesStart: return True
	
	return False
	
def isVassal(iPlayer):
	return utils.isAVassal(iPlayer)
	
def isCapitulated(iPlayer):
	return isVassal(iPlayer) and gc.getTeam(iPlayer).isCapitulated()
	
def getMaster(iPlayer):
	return utils.getMaster(iPlayer)
	
def isEmpire(iPlayer):
	if isVassal(iPlayer): return False

	return gc.getPlayer(iPlayer).getNumCities() >= getEmpireThreshold(iPlayer)
	
def getEmpireThreshold(iPlayer):
	if iPlayer in dEmpireThreshold: return dEmpireThreshold[iPlayer]
	
	if iPlayer == iEthiopia and not gc.getGame().isReligionFounded(iIslam):
		return 4
	
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
	
def countAreaCities(lPlots):
	return len(utils.getAreaCities(lPlots))
	
def countPlayerAreaCities(iPlayer, lPlots):
	return len(utils.getAreaCitiesCiv(iPlayer, lPlots))
	
def isAreaControlled(iPlayer, tTL, tBR, iMinCities=1, tExceptions=()):
	lPlots = utils.getPlotList(tTL, tBR, tExceptions)
	return isPlotListControlled(iPlayer, lPlots, iMinCities)
	
def isRegionControlled(iPlayer, iRegion, iMinCities=1):
	lPlots = utils.getRegionPlots(iRegion)
	return isPlotListControlled(iPlayer, lPlots, iMinCities)
	
def isPlotListControlled(iPlayer, lPlots, iMinCities=1):
	iTotalCities = countAreaCities(lPlots)
	iPlayerCities = countPlayerAreaCities(iPlayer, lPlots)
	
	if iPlayerCities < iTotalCities: return False
	if iPlayerCities < iMinCities: return False
	
	return True
	
def capitalCoords(iPlayer):
	capital = gc.getPlayer(iPlayer).getCapitalCity()
	if capital: return (capital.getX(), capital.getY())
	
	return (-1, -1)
	
def controlsHolyCity(iPlayer, iReligion):
	holyCity = gc.getGame().getHolyCity(iReligion)
	if holyCity and holyCity.getOwner() == iPlayer: return True
	
	return False
	
def controlsCity(iPlayer, tPlot):
	x, y = tPlot
	plot = gc.getMap().plot(x, y)
	
	return plot.isCity() and plot.getPlotCity().getOwner() == iPlayer
	
### Naming methods ###

def name(iPlayer, bIgnoreVassal = False):
	if isCapitulated(iPlayer) and not bIgnoreVassal:
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
		
	if iPlayer == iNetherlands: return short(iPlayer)
	
	if gc.getPlayer(iPlayer).isReborn(): return short(iPlayer)

	sSpecificName = getOrElse(getOrElse(dForeignNames, iMaster, {}), iPlayer)
	if sSpecificName: return sSpecificName
	
	return None
	
def republicName(iPlayer):
	if iPlayer in [iMoors, iEngland]: return None
	
	if iPlayer == iInca and data.players[iPlayer].iResurrections > 0: return None
	
	if iPlayer == iNetherlands and isCommunist(iPlayer): return "TXT_KEY_CIV_NETHERLANDS_ARTICLE"
	
	if iPlayer == iTurks: return "TXT_KEY_CIV_TURKS_UZBEKISTAN"
	
	if iPlayer == iBoers: return "TXT_KEY_CIV_BOER_SOUTH_AFRICA"

	return short(iPlayer)
	
def peoplesName(iPlayer):
	return desc(iPlayer, key(iPlayer, "PEOPLES"))
	
def specificName(iPlayer):
	iGameTurn = gc.getGame().getGameTurn()
	pPlayer = gc.getPlayer(iPlayer)
	tPlayer = gc.getTeam(pPlayer.getTeam())
	iCivicGovernment, iCivicLegitimacy, iCivicSociety, iCivicEconomy, iCivicReligion, iCivicTerritory = getCivics(iPlayer)
	
	iNumCities = pPlayer.getNumCities()
	if iNumCities == 0: return short(iPlayer)
	
	bReborn = pPlayer.isReborn()
	iReligion = pPlayer.getStateReligion()
	capital = gc.getPlayer(iPlayer).getCapitalCity()
	tCapitalCoords = capitalCoords(iPlayer)
	bAnarchy = pPlayer.isAnarchy()
	bEmpire = isEmpire(iPlayer)
	bCityStates = isCityStates(iPlayer)
	bTheocracy = (iCivicReligion == iTheocracy)
	bResurrected = data.players[iPlayer].iResurrections > 0
	bCapitulated = isCapitulated(iPlayer)
	iAnarchyTurns = data.players[iPlayer].iAnarchyTurns
	iEra = pPlayer.getCurrentEra()
	iGameEra = gc.getGame().getCurrentEra()
	bWar = isAtWar(iPlayer)
			
	if iPlayer == iBabylonia:
		if isCapital(iPlayer, ["Ninua", "Kalhu"]):
			return "TXT_KEY_CIV_BABYLONIA_ASSYRIA"
			
	if iPlayer == iNubia:
		if iEra >= iGlobal:
			return "TXT_KEY_CIV_SUDAN_SHORT_DESC"
			
		elif iReligion in lChristianity:
			return "TXT_KEY_CIV_NUBIA_MAKURIA"
			
		elif iReligion == iIslam:
			return "TXT_KEY_CIV_FUNJ"
			
		elif (iReligion < 0 or iReligion == iJudaism) and pPlayer.isStateReligion():
			if bEmpire:
				return "TXT_KEY_CIV_NUBIA_KUSH"
			return capitalName(iPlayer)
	
	elif iPlayer == iChina:
		if bEmpire:
			# if iEra >= iIndustrial or utils.getScenario() == i1700AD:
				# return "TXT_KEY_CIV_CHINA_QING"
			
			if iEra == iRenaissance and iGameTurn >= getTurnForYear(1400):
				return "TXT_KEY_CIV_CHINA_MING"
			
	elif iPlayer == iGreece:
		if not bCityStates and bEmpire and iEra <= iClassical:
			return "TXT_KEY_CIV_GREECE_MACEDONIA"
			
	elif iPlayer == iPolynesia:
		if isCapital(iPlayer, ["Kaua'i", "O'ahu", "Maui"]):
			return "TXT_KEY_CIV_POLYNESIA_HAWAII"
			
		if isCapital(iPlayer, ["Manu'a"]):
			return "TXT_KEY_CIV_POLYNESIA_SAMOA"
			
		if isCapital(iPlayer, ["Niue"]):
			return "TXT_KEY_CIV_POLYNESIA_NIUE"
			
		return "TXT_KEY_CIV_POLYNESIA_TONGA"
		
	elif iPlayer == iCeltia:
		if bReborn:
			if capital.getRegionID() == rBritain:
				if capital.getX() <= 50:
					return "TXT_KEY_CIV_CELTIA_IRELAND_SHORT_DESC"
				elif capital.getY() >= 48:
					return "TXT_KEY_CIV_CELTIA_SCOTLAND_SHORT_DESC"
		
	elif iPlayer == iTamils:
		if iEra >= iRenaissance:
			return "TXT_KEY_CIV_TAMILS_MYSORE"
			
		if iEra >= iMedieval:
			return "TXT_KEY_CIV_TAMILS_VIJAYANAGARA"
			
	elif iPlayer == iEthiopia:
		if not gc.getGame().isReligionFounded(iIslam):
			return "TXT_KEY_CIV_ETHIOPIA_AKSUM"
			
	elif iPlayer == iVietnam:
		if iEra >= iDigital:
			return "TXT_KEY_CIV_VIETNAM_SHORT_DESC"
		
		if iEra >= iIndustrial:
			return "TXT_KEY_CIV_VIETNAM_VIET_NAM"
			
		if iEra >= iMedieval:
			return "TXT_KEY_CIV_VIETNAM_DAI_VIET"
			
		return "TXT_KEY_CIV_VIETNAM_AU_LAC"
			
	elif iPlayer == iKorea:
		if iEra == iClassical:
			if bEmpire:
				return "TXT_KEY_CIV_KOREA_GOGURYEO"
				
		if iEra <= iMedieval:
			return "TXT_KEY_CIV_KOREA_GORYEO"
			
		return "TXT_KEY_CIV_KOREA_JOSEON"
	
	elif iPlayer == iTeotihuacan:
		if not isCapital(iPlayer, ["Tollan"]):
			return capitalName(iPlayer)
			
		if iGameTurn >= getTurnForYear(800):
			return "TXT_KEY_CIV_TEOTIHUACAN_TULA"
		
	elif iPlayer == iInuit:
		bCanada = False
		for city in utils.getCityList(iPlayer):
			if (city.getRegionID() == rScandinavia and city.getY() <= 63 and city.getX() <= 42):
				return "TXT_KEY_CIV_INUIT_THULE"
		
			if (city.getRegionID() == rCanada):
				bCanada = True
				
		if bCanada: return "TXT_KEY_CIV_INUIT_DORSET"
		
		return "TXT_KEY_CIV_INUIT_BERING_SEA"
		
	elif iPlayer == iByzantium:
		if iReligion == iIslam:
			return "TXT_KEY_CIV_BYZANTIUM_RUM"
	
		if not bEmpire:
			if isCapital(iPlayer, ["Dyrrachion"]):
				return "TXT_KEY_CIV_BYZANTIUM_EPIRUS"
			
			if isCapital(iPlayer, ["Athena"]):
				return "TXT_KEY_CIV_BYZANTIUM_MOREA"
	
			if not isCapital(iPlayer, ["Konstantinoupolis"]):
				return capitalName(iPlayer)
			
	elif iPlayer == iVikings:
		# if bEmpire:
		if iEra >= iRenaissance:
			return "TXT_KEY_CIV_VIKINGS_DENMARK_NORWAY"
	
		if isCapital(iPlayer, ["Oslo", "Nidaros"]):
			return "TXT_KEY_CIV_VIKINGS_NORWAY"
			
		if isCapital(iPlayer, ["Roskilde"]):
			return "TXT_KEY_CIV_VIKINGS_DENMARK"
			
		if not pSweden.isAlive():
			return "TXT_KEY_CIV_VIKINGS_SCANDINAVIA"
			
		return "TXT_KEY_CIV_VIKING_SHORT_DESC"
		
	elif iPlayer == iKhazars:
		if data.players[iPlayer].iResurrections > 1:
			return "TXT_KEY_CIV_KHAZARIA_KAZAKHSTAN"
		if bResurrected:
			return "TXT_KEY_CIV_KHAZARIA_KAZAKH"
		if bEmpire: 
			return "TXT_KEY_CIV_KHAZARIA_CUMANIA"
		
	elif iPlayer == iTurks:
		if utils.isPlotInArea(tCapitalCoords, tAnatoliaTL, tAnatoliaBR):
			return "TXT_KEY_CIV_TURKS_RUM"
			
		if iEra >= iRenaissance and not tPlayer.isAVassal():
			if bEmpire:
				return "TXT_KEY_CIV_TURKS_UZBEKISTAN"
				
			return capitalName(iPlayer)
		
	elif iPlayer == iArabia:
		if bResurrected:
			return "TXT_KEY_CIV_ARABIA_SAUDI"
			
	elif iPlayer == iKhmer:
		if isCapital(iPlayer, ["Dali"]):
			return "TXT_KEY_CIV_KHMER_NANZHAO"
		if isCommunist(iPlayer):
			return "TXT_KEY_CIV_KHMER_KAMPUCHEA"
		if iEra > iRenaissance and iCivicGovernment != iDespotism:
			return "TXT_KEY_CIV_KHMER_CAMBODIA"
			
	elif iPlayer == iIndonesia:
		if iReligion == iIslam:
			return "TXT_KEY_CIV_INDONESIA_MATARAM"
			
		if iEra <= iRenaissance:
			if bEmpire:
				return "TXT_KEY_CIV_INDONESIA_MAJAPAHIT"
				
			return "TXT_KEY_CIV_INDONESIA_SRIVIJAYA"
			
	elif iPlayer == iChad:
		if iEra >= iGlobal:
			return "TXT_KEY_CIV_CHAD_MODERN_SHORT_DESC"
		elif capital.getName == 'Ngazargamu':
			return "TXT_KEY_CIV_CHAD_BORNU"
		elif bEmpire:
			return "TXT_KEY_CIV_CHAD_EMPIRE"
	
	elif iPlayer == iMoors:	
		if utils.isPlotInArea(tCapitalCoords, vic.tIberiaTL, vic.tIberiaBR):
			return capitalName(iPlayer)
			
		return "TXT_KEY_CIV_MOORS_MOROCCO"
		
	elif iPlayer == iSpain:
		if iReligion == iIslam:
			return "TXT_KEY_CIV_SPAIN_AL_ANDALUS"
	
		bSpain = not pMoors.isAlive() or not utils.isPlotInArea(capitalCoords(iMoors), vic.tIberiaTL, vic.tIberiaBR)
	
		if bSpain:
			if not pPortugal.isAlive() or not utils.isPlotInArea(capitalCoords(iPortugal), vic.tIberiaTL, vic.tIberiaBR):
				return "TXT_KEY_CIV_SPAIN_IBERIA"
			
		if isCapital(iPlayer, ["Barcelona", "Valencia"]):
			return "TXT_KEY_CIV_SPAIN_ARAGON"
			
		if not bSpain:
			return "TXT_KEY_CIV_SPAIN_CASTILE"
			
	elif iPlayer == iFrance:
		if iEra == iMedieval and not pHolyRome.isAlive():
			return "TXT_KEY_CIV_FRANCE_FRANCIA"
			
	elif iPlayer == iEngland:
		if getColumn(iEngland) >= 11 and countPlayerAreaCities(iPlayer, utils.getPlotList(tBritainTL, tBritainBR)) >= 3:
			return "TXT_KEY_CIV_ENGLAND_GREAT_BRITAIN"
			
	elif iPlayer == iHolyRome:
		if isCapital(iPlayer, ["Buda"]):
			return "TXT_KEY_CIV_HOLY_ROME_HUNGARY"
	
		if not bEmpire:
			if iGameTurn < getTurnForYear(tBirth[iGermany]):
				return "TXT_KEY_CIV_HOLY_ROME_GERMANY"
			else:
				return "TXT_KEY_CIV_AUSTRIA_SHORT_DESC"
	
	elif iPlayer == iKievanRus:
		if not bResurrected and not isCapital(iPlayer, ["Kiev"]):
			return capitalName(iPlayer)
			
	elif iPlayer == iRussia:
		if not (bEmpire and iEra >= iRenaissance) and not isAreaControlled(iPlayer, tEuropeanRussiaTL, tEuropeanRussiaBR, 5, tEuropeanRussiaExceptions):
			if not bCityStates and isCapital(iPlayer, ["Moskva"]):
				return "TXT_KEY_CIV_RUSSIA_MUSCOVY"
				
			return capitalName(iPlayer)
			
	elif iPlayer == iPhilippines:
		if iEra >= iGlobal:
			return "TXT_KEY_CIV_PHILIPPINES_THE"
	
		if isCapital(iPlayer, ["Tondo"]):
			return "TXT_KEY_CIV_PHILIPPINES_TONDO"
			
		if isCapital(iPlayer, ["Butuan"]):
			return "TXT_KEY_CIV_PHILIPPINES_BUTUAN"
			
	elif iPlayer == iZimbabwe:
		if iEra >= iGlobal:
			return "TXT_KEY_CIV_ZIMBABWE_ZIMBABWE"
	
		if iEra >= iIndustrial:
			return "TXT_KEY_CIV_ZIMBABWE_ROZWI"
		
		if iEra >= iRenaissance:
			return "TXT_KEY_CIV_ZIMBABWE_MUTAPA"
			
		if iGameTurn >= 1220:
			return "TXT_KEY_CIV_ZIMBABWE_GREAT"
			
		return "TXT_KEY_CIV_ZIMBABWE_MAPUNGUBWE"
			
	elif iPlayer == iInca:
		if bResurrected:
			if isCapital(iPlayer, ["La Paz"]):
				return "TXT_KEY_CIV_INCA_BOLIVIA"
				
		else:
			if not bEmpire:
				return capitalName(iPlayer)
			
	elif iPlayer == iItaly:
		if not bResurrected and not bEmpire and not bCityStates:
			if isCapital(iPlayer, ["Fiorenza"]):
				return "TXT_KEY_CIV_ITALY_TUSCANY"
				
			return capitalName(iPlayer)
			
	elif iPlayer == iNigeria:
		if iEra >= iGlobal:
			return "TXT_KEY_CIV_NIGERIA_NIGERIA"
			
		if isCapital(iPlayer, ["Oyo"]):
			return "TXT_KEY_CIV_NIGERIA_OYO"
			
		if isCapital(iPlayer, ["Ife"]):
			return "TXT_KEY_CIV_NIGERIA_IFE"
			
		if isCapital(iPlayer, ["Njimi"]):
			return "TXT_KEY_CIV_NIGERIA_KANEM"
			
		if isCapital(iPlayer, ["Igbo-Ukwu"]):
			return "TXT_KEY_CIV_NIGERIA_NRI"
			
		if isCapital(iPlayer, ["Wukari"]):
			return "TXT_KEY_CIV_NIGERIA_KWARARAFA"
			
		return "TXT_KEY_CIV_NIGERIA_BENIN"
			
	elif iPlayer == iThailand:
		if iEra <= iRenaissance:
			return "TXT_KEY_CIV_THAILAND_AYUTTHAYA"
			
	elif iPlayer == iSweden:
		if iEra >= iIndustrial and (isAreaControlled(iPlayer, (58, 59), (61, 63)) and not pVikings.isAlive()) or getMaster(iVikings) == iPlayer:
			return "TXT_KEY_CIV_SWEDEN_AND_NORWAY"
			
	elif iPlayer == iNetherlands:
		if bCityStates:
			return short(iPlayer)
			
		if isCapital(iPlayer, ["Brussels", "Antwerpen"]):
			return "TXT_KEY_CIV_NETHERLANDS_BELGIUM"
			
	elif iPlayer == iManchuria:
		return "TXT_KEY_CIV_CHINA_QING"
			
	elif iPlayer == iGermany:
		if getColumn(iGermany) <= 14 and pHolyRome.isAlive() and not teamHolyRome.isVassal(iGermany):
			return "TXT_KEY_CIV_GERMANY_PRUSSIA"
	
	elif iPlayer == iIsrael:
		if iReligion == iIslam:
			return "TXT_KEY_CIV_ISRAEL_PALESTINE"
	
def adjective(iPlayer, bIgnoreVassal = False):
	if isCapitulated(iPlayer):
		sForeignAdjective = getOrElse(getOrElse(dForeignAdjectives, getMaster(iPlayer), {}), iPlayer)
		if sForeignAdjective: return sForeignAdjective
		
		if not bIgnoreVassal: return adjective(getMaster(iPlayer))
		
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
	
	if iPlayer == iInca and data.players[iPlayer].iResurrections > 0: return None
		
	return gc.getPlayer(iPlayer).getCivilizationAdjective(0)
	
def specificAdjective(iPlayer):
	iGameTurn = gc.getGame().getGameTurn()
	pPlayer = gc.getPlayer(iPlayer)
	tPlayer = gc.getTeam(pPlayer.getTeam())
	iCivicGovernment, iCivicLegitimacy, iCivicSociety, iCivicEconomy, iCivicReligion, iCivicTerritory = getCivics(iPlayer)
	
	iNumCities = pPlayer.getNumCities()
	if iNumCities == 0: return gc.getPlayer(iPlayer).getCivilizationAdjective(0)
	
	bReborn = pPlayer.isReborn()
	iReligion = pPlayer.getStateReligion()
	capital = gc.getPlayer(iPlayer).getCapitalCity()
	tCapitalCoords = capitalCoords(iPlayer)
	bAnarchy = pPlayer.isAnarchy()
	bEmpire = isEmpire(iPlayer)
	bCityStates = isCityStates(iPlayer)
	bTheocracy = (iCivicReligion == iTheocracy)
	bResurrected = data.players[iPlayer].iResurrections > 0
	bCapitulated = isCapitulated(iPlayer)
	iAnarchyTurns = data.players[iPlayer].iAnarchyTurns
	iEra = pPlayer.getCurrentEra()
	iGameEra = gc.getGame().getCurrentEra()
	bWar = isAtWar(iPlayer)
	
	bMonarchy = not isCommunist(iPlayer) and not isFascist(iPlayer) and not isRepublic(iPlayer)
	
	# if iPlayer == iEgypt:
		# if bMonarchy:
			# if bResurrected:
				# if tPlayer.isHasTech(iGunpowder):
					# return "TXT_KEY_CIV_EGYPT_MAMLUK"
		
				# if pArabia.isAlive():
					# return "TXT_KEY_CIV_EGYPT_FATIMID"
			
				# return "TXT_KEY_CIV_EGYPT_AYYUBID"
			
	if iPlayer == iIndia:
		if bMonarchy and not bCityStates:
			if iEra >= iRenaissance:
				return "TXT_KEY_CIV_INDIA_MARATHA"
			
			if iEra >= iMedieval:
				return "TXT_KEY_CIV_INDIA_PALA"
			
			if iReligion == iBuddhism:
				return "TXT_KEY_CIV_INDIA_MAURYA"
			
			if iReligion == iHinduism:
				return "TXT_KEY_CIV_INDIA_GUPTA"
			
	elif iPlayer == iNubia:
		if iEra >= iGlobal:
			return "TXT_KEY_CIV_SUDAN_ADJECTIVE"
			
	elif iPlayer == iChina:
		if bMonarchy:
			if iEra >= iMedieval:
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
		if pPlayer.isStateReligion() and iReligion < 0:
			return "TXT_KEY_CIV_PERSIA_MEDIAN"
	
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
			
			if getColumn(iPlayer) >= 6: 
				return "TXT_KEY_CIV_PERSIA_SASSANID"
				
	elif iPlayer == iCeltia:
		if bReborn:
			if capital.getRegionID() == rBritain:
				if capital.getX() <= 50:
					return "TXT_KEY_CIV_CELTIA_IRELAND_ADJECTIVE"
				elif capital.getY() >= 48:
					return "TXT_KEY_CIV_CELTIA_SCOTLAND_ADJECTIVE"
					
		elif isCapital(iPlayer, ["Hallstat", "La Tene"]):
			return capitalName(iPlayer)
				
	elif iPlayer == iPolynesia:
		if isCapital(iPlayer, ["Manu'a"]):
			return "TXT_KEY_CIV_POLYNESIA_TUI_MANUA"
			
		return "TXT_KEY_CIV_POLYNESIA_TUI_TONGA"
		
	elif iPlayer == iRome:
		if pByzantium.isAlive():
			return "TXT_KEY_CIV_ROME_WESTERN"
			
	elif iPlayer == iTamils:
		if iReligion == iIslam:
			if iEra in [iMedieval, iRenaissance]:
				return "TXT_KEY_CIV_TAMILS_BAHMANI"
				
		if iEra <= iClassical:
			if isCapital(iPlayer, ["Madurai", "Thiruvananthapuram"]):
				return "TXT_KEY_CIV_TAMILS_PANDYAN"
				
			if isCapital(iPlayer, ["Cochin", "Kozhikode"]):
				return "TXT_KEY_CIV_TAMILS_CHERA"
				
			return "TXT_KEY_CIV_TAMILS_CHOLA"
			
	elif iPlayer == iEthiopia:
		if iReligion == iIslam:
			return "TXT_KEY_CIV_ETHIOPIA_ADAL"
			
		if not gc.getGame().isReligionFounded(iIslam):
			return "TXT_KEY_CIV_ETHIOPIA_AKSUMITE"
			
	elif iPlayer == iTeotihuacan:
		if iGameTurn >= getTurnForYear(800):
			return "TXT_KEY_CIV_TEOTIHUACAN_TOLTEC"
			
	elif iPlayer == iByzantium:
		if pRome.getNumCities() > 0:
			return "TXT_KEY_CIV_BYZANTIUM_EASTERN"
			
		if bEmpire and controlsCity(iPlayer, Areas.getCapital(iRome)):
			return gc.getPlayer(iRome).getCivilizationAdjective(0)
			
	elif iPlayer == iKhazars:
		if bResurrected:
			return "TXT_KEY_CIV_KHAZARIA_KAZAKH"
		if bEmpire: 
			return "TXT_KEY_CIV_KHAZARIA_CUMAN"
			
	elif iPlayer == iTurks:
		if bResurrected:
			return "TXT_KEY_CIV_TURKS_TIMURID"
			
		if isAreaControlled(iTurks, Areas.tCoreArea[iPersia][0], Areas.tCoreArea[iPersia][1]):
			return "TXT_KEY_CIV_TURKS_SELJUK"
			
		if utils.isPlotInArea(iTurks, Areas.tCoreArea[iPersia][0], Areas.tCoreArea[iPersia][0]):
			return "TXT_KEY_CIV_TURKS_SELJUK"
			
		if utils.isPlotInArea(tCapitalCoords, tAnatoliaTL, tAnatoliaBR):
			return "TXT_KEY_CIV_TURKS_SELJUK"
			
		if iEra >= iRenaissance:
			if bEmpire:
				return "TXT_KEY_CIV_TURKS_SHAYBANID"
		
			return "TXT_KEY_CIV_TURKS_UZBEK"
			
		easternmostCity = utils.getHighestEntry(utils.getCityList(iTurks), lambda city: city.getX())
		if easternmostCity and easternmostCity.getX() < iTurkicEastWestBorder:
			return "TXT_KEY_CIV_TURKS_WESTERN_TURKIC"
			
		westernmostCity = utils.getHighestEntry(utils.getCityList(iTurks), lambda city: -city.getX())
		if westernmostCity and westernmostCity.getX() >= iTurkicEastWestBorder:
			return "TXT_KEY_CIV_TURKS_EASTERN_TURKIC"
			
	elif iPlayer == iArabia:
		if (bTheocracy or controlsHolyCity(iArabia, iIslam)) and iReligion == iIslam:
			if not bEmpire:
				return "TXT_KEY_CIV_ARABIA_RASHIDUN"
				
			if isCapital(iPlayer, ["Dimashq"]):
				return "TXT_KEY_CIV_ARABIA_UMMAYAD"
				
			return "TXT_KEY_CIV_ARABIA_ABBASID"
			
	elif iPlayer == iKhmer:
		if isCommunist(iPlayer):
			return "TXT_KEY_CIV_KHMER_KAMPUCHEAN"
		if iEra > iRenaissance and iCivicGovernment != iDespotism:
			return "TXT_KEY_CIV_KHMER_CAMBODIAN"
			
	elif iPlayer == iBurma:
		if (iNumCities > 2 or civAdjective(iBurma) == "Toungoo") and not bReborn:
			return "TXT_KEY_CIV_BURMA_TOUNGOO"
			
		if not iNumCities > 2 and not bReborn:
			return capitalName(iPlayer)
			
	elif iPlayer == iChad:
		if iEra >= iGlobal:
			return "TXT_KEY_CIV_CHAD_MODERN_ADJECTIVE"
			
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
		if getColumn(iEngland) >= 11 and countPlayerAreaCities(iPlayer, utils.getPlotList(tBritainTL, tBritainBR)) >= 3:
			return "TXT_KEY_CIV_ENGLAND_BRITISH"
			
	elif iPlayer == iHolyRome:
		if isCapital(iPlayer, ["Buda"]):
			return "TXT_KEY_CIV_HOLY_ROME_HUNGARIAN"
	
		if pGermany.isAlive() and iCivicLegitimacy == iConstitution:
			return "TXT_KEY_CIV_HOLY_ROME_AUSTRO_HUNGARIAN"
			
		iVassals = 0
		for iLoopPlayer in lCivGroups[0]:
			if getMaster(iLoopPlayer) == iPlayer:
				iVassals += 1
				
		if iVassals >= 2:
			return "TXT_KEY_CIV_HOLY_ROME_HABSBURG"
			
		if not bEmpire and iGameTurn < getTurnForYear(tBirth[iGermany]):
			return "TXT_KEY_CIV_HOLY_ROME_GERMAN"
			
	elif iPlayer == iMamluks:
		if tPlayer.isHasTech(iGunpowder):
			return "TXT_KEY_CIV_MAMLUKS_MAMLUK"

		if pArabia.isAlive():
			return "TXT_KEY_CIV_MAMLUKS_FATIMID"
	
		return "TXT_KEY_CIV_MAMLUKS_AYYUBID"
			
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
				return "TXT_KEY_CIV_MONGOLIA_HULAGU"
				
			if capital.getRegionID() == rCentralAsia:
				return "TXT_KEY_CIV_MONGOLIA_CHAGATAI"
				
		if bMonarchy:
			return "TXT_KEY_CIV_MONGOLIA_MONGOL"
				
	elif iPlayer == iOttomans:
		return "TXT_KEY_CIV_OTTOMANS_OTTOMAN"
			
	elif iPlayer == iNetherlands:
		if isCapital(iPlayer, ["Brussels", "Antwerpen"]):
			return "TXT_KEY_CIV_NETHERLANDS_BELGIAN"
			
	elif iPlayer == iGermany:
		if getColumn(iGermany) <= 14 and pHolyRome.isAlive() and not teamHolyRome.isVassal(iGermany):
			return "TXT_KEY_CIV_GERMANY_PRUSSIAN"
	
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
	if iPlayer == iHolyRome:
		return "TXT_KEY_REPUBLIC_ADJECTIVE"
	
	if iPlayer == iPoland:
		if gc.getPlayer(iPlayer).getCurrentEra() <= iIndustrial:
			return key(iPlayer, "COMMONWEALTH")
	
	if iPlayer == iEngland:
		iEra = gc.getPlayer(iPlayer).getCurrentEra()
		if isEmpire(iEngland) and iEra == iIndustrial:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if iEra >= iGlobal:
			return "TXT_KEY_CIV_ENGLAND_UNITED_REPUBLIC"
	
	if iPlayer == iAmerica:
		_, _, iCivicSociety, _, _, _ = getCivics(iPlayer)
		if iCivicSociety in [iManorialism, iSlavery]:
			return key(iPlayer, "CSA")
			
	if iPlayer == iMaya:
		if gc.getPlayer(iMaya).isReborn():
			if isRegionControlled(iPlayer, rPeru) and isAreaControlled(iPlayer, tColombiaTL, tColombiaBR):
				return "TXT_KEY_CIV_COLOMBIA_FEDERATION_ANDES"
			
	if gc.getPlayer(iPlayer).getStateReligion() == iIslam:
		if iPlayer in lIslamicRepublicOf: return "TXT_KEY_ISLAMIC_REPUBLIC_OF"

		if iPlayer == iOttomans: return key(iPlayer, "ISLAMIC_REPUBLIC")
		
	
	if iPlayer == iBurma:
		if pBurma.isReborn() and not short(iPlayer) == "Myanmar" and not isCommunist(iPlayer):
			return "TXT_KEY_CIV_UNION_OF"
		
	if iPlayer in lRepublicOf: return "TXT_KEY_REPUBLIC_OF"
	if iPlayer in lRepublicAdj: return "TXT_KEY_REPUBLIC_ADJECTIVE"
	
	return key(iPlayer, "REPUBLIC")

def defaultTitle(iPlayer):
	return desc(iPlayer, key(iPlayer, "DEFAULT"))
	
def specificTitle(iPlayer, lPreviousOwners=[]):
	iGameTurn = gc.getGame().getGameTurn()
	pPlayer = gc.getPlayer(iPlayer)
	tPlayer = gc.getTeam(pPlayer.getTeam())
	iCivicGovernment, iCivicLegitimacy, iCivicSociety, iCivicEconomy, iCivicReligion, iCivicTerritory = getCivics(iPlayer)
	
	iNumCities = pPlayer.getNumCities()
	if iNumCities == 0: return defaultTitle(iPlayer)
	
	bReborn = pPlayer.isReborn()
	iReligion = pPlayer.getStateReligion()
	capital = gc.getPlayer(iPlayer).getCapitalCity()
	tCapitalCoords = capitalCoords(iPlayer)
	bAnarchy = pPlayer.isAnarchy()
	bEmpire = isEmpire(iPlayer)
	bCityStates = isCityStates(iPlayer)
	bTheocracy = (iCivicReligion == iTheocracy)
	bResurrected = data.players[iPlayer].iResurrections > 0
	bCapitulated = isCapitulated(iPlayer)
	iAnarchyTurns = data.players[iPlayer].iAnarchyTurns
	iEra = pPlayer.getCurrentEra()
	iGameEra = gc.getGame().getCurrentEra()
	bWar = isAtWar(iPlayer)

	if iPlayer == iEgypt:
		'''
		if bResurrected or utils.getScenario() >= i600AD:
			if iReligion == iIslam:
				if bTheocracy: return "TXT_KEY_CALIPHATE_ADJECTIVE"
				return "TXT_KEY_SULTANATE_ADJECTIVE"
			return "TXT_KEY_KINGDOM_ADJECTIVE"
		'''
		
		if iGreece in lPreviousOwners:
			return "TXT_KEY_CIV_EGYPT_PTOLEMAIC"
			
		if bCityStates:
			return "TXT_KEY_CITY_STATES_ADJECTIVE"
				
		if iEra == iAncient:
			if iAnarchyTurns == 0: return "TXT_KEY_CIV_EGYPT_OLD_KINGDOM"
			if iAnarchyTurns == utils.getTurns(1): return "TXT_KEY_CIV_EGYPT_MIDDLE_KINGDOM"
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
			
	elif iPlayer == iNubia:
		if iReligion == iIslam:
			return "TXT_KEY_SULTANATE_NAME"
			
		if bEmpire or iReligion >= 0 or not pPlayer.isStateReligion() or not isCapital(iPlayer, ["Kerma"]):
			return "TXT_KEY_KINGDOM_OF"
			
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
			
	elif iPlayer == iCeltia:
		if bReborn:
			return "TXT_KEY_KINGDOM_OF"
			
		elif teamCeltia.isVassal(iRome):
			if capital.getRegionID() == rBritain:
				return "TXT_KEY_CIV_CELTIA_ROME_BRITANNIA"
			if capital.getRegionID() == rEurope:
				if capital.getX() < 58:
					return "TXT_KEY_CIV_CELTIA_ROME_GALLIA"
				else:
					return "TXT_KEY_CIV_CELTIA_ROME_GERMANIA"
			
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
			
	elif iPlayer == iMaya:
		if bReborn:
			if bEmpire:
				if isRegionControlled(iPlayer, rPeru) and isAreaControlled(iPlayer, tColombiaTL, tColombiaBR):
					return "TXT_KEY_CIV_COLOMBIA_EMPIRE_ANDES"
			
				return "TXT_KEY_CIV_COLOMBIA_EMPIRE"
			
	elif iPlayer == iJapan:
		if bEmpire:
			return "TXT_KEY_EMPIRE_OF"
			
		if iCivicLegitimacy == iCentralism:
			return "TXT_KEY_EMPIRE_OF"
			
		if iEra >= iIndustrial:
			return "TXT_KEY_EMPIRE_OF"
			
	elif iPlayer == iTamils:
		if iReligion == iIslam:
			return "TXT_KEY_SULTANATE_ADJECTIVE"
			
		if iEra >= iMedieval:
			return "TXT_KEY_KINGDOM_OF"
		
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iPlayer == iEthiopia:
		if bCityStates:
			return "TXT_KEY_CITY_STATES_ADJECTIVE"
	
		if iReligion == iIslam:
			return "TXT_KEY_SULTANATE_ADJECTIVE"
	
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	# elif iPlayer == iVietnam:
		# pass
	
	elif iPlayer == iTeotihuacan:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if bCityStates:
			return "TXT_KEY_CIV_TEOTIHUACAN_ALTEPETL"
				
	elif iPlayer == iInuit:
		if iEra >= iGlobal:
			return "TXT_KEY_CIV_INUIT_COUNCIL"
				
	elif iPlayer == iKorea:
		if iEra >= iIndustrial:
			if bEmpire:
				return "TXT_KEY_EMPIRE_ADJECTIVE"
				
		if iEra == iClassical:
			if bEmpire:
				return "TXT_KEY_EMPIRE_OF"
				
		if bCityStates:
			return "TXT_KEY_CIV_KOREA_SAMHAN"
				
		if iReligion >= 0:
			return "TXT_KEY_KINGDOM_OF"
			
	elif iPlayer == iByzantium:
		if iReligion == iIslam:
			return "TXT_KEY_SULTANATE_OF"
			
		if tCapitalCoords != Areas.getCapital(iPlayer):
			if capital.getRegionID() == rAnatolia:
				return "TXT_KEY_EMPIRE_OF"
				
			return "TXT_KEY_CIV_BYZANTIUM_DESPOTATE"
			
	elif iPlayer == iVikings:
		if bCityStates:
			return "TXT_KEY_CIV_VIKINGS_ALTHINGS"
			
		if isAreaControlled(iPlayer, tBritainTL, tBritainBR):
			return "TXT_KEY_CIV_VIKINGS_NORTH_SEA_EMPIRE"
				
		if iReligion < 0 and iEra < iRenaissance:
			return "TXT_KEY_CIV_VIKINGS_NORSE_KINGDOMS"
			
		if bEmpire:
			if iEra == iRenaissance and utils.getScenario() != i1700AD:
				return "TXT_KEY_EMPIRE_ADJECTIVE"
				
	elif iPlayer == iKhazars:
		if bReborn:
			return "TXT_KEY_CIV_KHAZARIA_KHANATE"
		if bEmpire:
			return "TXT_KEY_CIV_KHAZARIA_CONFEDERATION"
				
	elif iPlayer == iTurks:
		if bCityStates or iCivicGovernment == iElective:
			return "TXT_KEY_CIV_TURKS_KURULTAI"
			
		if iReligion >= 0:
			if bEmpire:
				if isAreaControlled(iTurks, Areas.tCoreArea[iPersia][0], Areas.tCoreArea[iPersia][1]) and not bResurrected:
					return "TXT_KEY_CIV_TURKS_GREAT_EMPIRE"
			
				return "TXT_KEY_EMPIRE_ADJECTIVE"
				
			if not isAreaControlled(iTurks, Areas.tCoreArea[iPersia][0], Areas.tCoreArea[iPersia][1]):
				return "TXT_KEY_CIV_TURKS_KHANATE_OF"
				
			if iReligion == iIslam:
				if isAreaControlled(iTurks, Areas.tCoreArea[iPersia][0], Areas.tCoreArea[iPersia][1]):
					return "TXT_KEY_SULTANATE_ADJECTIVE"
			
				return "TXT_KEY_SULTANATE_OF"
				
			return "TXT_KEY_KINGDOM_OF"
			
		if bEmpire:
			return "TXT_KEY_CIV_TURKS_KHAGANATE"
			
	elif iPlayer == iArabia:
		if bResurrected:
			return "TXT_KEY_KINGDOM_OF"
			
		if iReligion == iIslam and (bTheocracy or controlsHolyCity(iArabia, iIslam)):
			return "TXT_KEY_CALIPHATE_ADJECTIVE"
			
	elif iPlayer == iTibet:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iPlayer == iKhmer:
		if iEra <= iRenaissance and isCapital(iPlayer, ["Angkor"]):
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iPlayer == iYemen:
		if isVassal(iYemen):
			return "TXT_KEY_CIV_YEMEN_SHORT_DESC"
		if gc.getGame().getHolyCity(iIslam).getOwner() == iYemen:
			return "TXT_KEY_CIV_YEMEN_MECCA"
		if iCivicReligion == iTheocracy:
			return "TXT_KEY_CIV_YEMEN_THEOCRACY"
		if not pArabia.isAlive():
			return "TXT_KEY_CIV_YEMEN_DEAD_ARABIA"
		if (iCivicGovernment == iDespotism and iEra >= iGlobal) or iCivicGovernment == iStateParty:
			return "TXT_KEY_CIV_YEMEN_STATE_PARTY"
		return "TXT_KEY_CIV_YEMEN_DEFAULT"
		
	elif iPlayer == iIndonesia:
		if iReligion == iIslam:
			return "TXT_KEY_SULTANATE_OF"
		
	elif iPlayer == iBurma:
		if bCityStates:
			return "TXT_KEY_CIV_BURMA_CITY_STATES"
		if not bReborn and bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iPlayer == iMoors:
		if bCityStates:
			return "TXT_KEY_CIV_MOORS_TAIFAS"
			
		if iReligion == iIslam and utils.isPlotInArea(tCapitalCoords, vic.tIberiaTL, vic.tIberiaBR):
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
			
		if iCivicLegitimacy == iRevolutionism:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if not pHolyRome.isAlive() and iEra == iMedieval:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iPlayer == iOman:
		if iReligion == iIslam and iCivicGovernment == iDespotism:
			return "TXT_KEY_SULTANATE_OF"
		
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iPlayer == iEngland:
		if not utils.isPlotInCore(iPlayer, tCapitalCoords):
			return "TXT_KEY_CIV_ENGLAND_EXILE"
			
		if iEra == iMedieval and getMaster(iFrance) == iEngland:
			return "TXT_KEY_CIV_ENGLAND_ANGEVIN_EMPIRE"
			
		if getColumn(iPlayer) >= 11:
			if bEmpire:
				return "TXT_KEY_EMPIRE_ADJECTIVE"
		
			if countPlayerAreaCities(iPlayer, utils.getPlotList(tBritainTL, tBritainBR)) >= 3:
				return "TXT_KEY_CIV_ENGLAND_UNITED_KINGDOM_OF"
			
	elif iPlayer == iHolyRome:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if isCapital(iPlayer, ["Buda"]):
			return "TXT_KEY_KINGDOM_OF"
			
		if pGermany.isAlive():
			return "TXT_KEY_CIV_HOLY_ROME_ARCHDUCHY_OF"
		
	elif iPlayer == iRussia:
		if bEmpire and iEra >= iRenaissance:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if isAreaControlled(iPlayer, tEuropeanRussiaTL, tEuropeanRussiaBR, 5, tEuropeanRussiaExceptions):
			return "TXT_KEY_CIV_RUSSIA_TSARDOM_OF"
			
	elif iPlayer == iKievanRus:
		if data.players[iPlayer].iResurrections == 0 and not isCapital(iPlayer, ["Kiev"]):
			return "TXT_KEY_CIV_RUS'_OF"
			
	elif iPlayer == iHungary:
		if iReligion != -1 or iCivicReligion == iSecularism:
			return "TXT_KEY_KINGDOM_OF"
			
	elif iPlayer == iPhilippines:
		if iReligion == iHinduism:
			return "TXT_KEY_CIV_PHILIPPINES_RAJAHNATE"
			
	elif iPlayer == iMamluks:
		if iReligion == iIslam:
			if bTheocracy: return "TXT_KEY_CALIPHATE_ADJECTIVE"
			return "TXT_KEY_SULTANATE_ADJECTIVE"
		return "TXT_KEY_KINGDOM_ADJECTIVE"

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
			
	elif iPlayer == iZimbabwe:
		if iEra >= iRenaissance:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iPlayer == iPortugal:
		if utils.isPlotInCore(iBrazil, tCapitalCoords) and not pBrazil.isAlive():
			return "TXT_KEY_CIV_PORTUGAL_BRAZIL"
			
		if not utils.isPlotInArea(tCapitalCoords, vic.tIberiaTL, vic.tIberiaBR):
			return "TXT_KEY_CIV_PORTUGAL_EXILE"
			
		if bEmpire and iEra >= iRenaissance:
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
				
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iPlayer == iNigeria:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if isCapital(iPlayer, ["Wukari"]):
			return "TXT_KEY_CONFEDERATION_OF"
			
		if iGameTurn >= getTurnForYear(1300):
			return "TXT_KEY_KINGDOM_OF"
			
	elif iPlayer == iMongolia:
		if capital.getRegionID() == rPersia:
			return "TXT_KEY_CIV_MONGOLIA_ILKHANATE"
	
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
		if bResurrected:
			if bEmpire:
				return "TXT_KEY_EMPIRE_OF"
				
			return "TXT_KEY_SULTANATE_OF"
	
		if iEra == iMedieval and not bEmpire:
			return "TXT_KEY_SULTANATE_OF"
			
	elif iPlayer == iOttomans:
		if iReligion == iIslam:
			if bTheocracy and gc.getGame().getHolyCity(iIslam) and gc.getGame().getHolyCity(iIslam).getOwner() == iOttomans:
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
		if iCivicSociety in [iSlavery, iManorialism]:
			if isRegionControlled(iAmerica, rMesoamerica) and isRegionControlled(iAmerica, rCaribbean):
				return "TXT_KEY_CIV_AMERICA_GOLDEN_CIRCLE"
		
			return "TXT_KEY_CIV_AMERICA_CSA"
			
	elif iPlayer == iArgentina:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if tCapitalCoords != Areas.getCapital(iPlayer):
			return "TXT_KEY_CIV_ARGENTINA_CONFEDERATION"
			
	elif iPlayer == iBrazil:
		if bEmpire:
			return "TXT_KEY_EMPIRE_OF"
			
	elif iPlayer == iBoers:
		if iEra >= iGlobal:
			return "TXT_KEY_CIV_BOER_UNION"
		
		if bEmpire:
			return "TXT_KEY_CIV_BOER_UNION"
		
		if isCapital(iPlayer, ["Pretoria", "Johannesburg"]):
			return "TXT_KEY_CIV_BOER_TRANSVAAL"
		if isCapital(iPlayer, ["Bloemfontein"]):
			return "TXT_KEY_CIV_BOER_ORANGE_FREE_STATE"
		if isCapital(iPlayer, ["Pietermaritzburg", "Durban"]):
			return "TXT_KEY_CIV_BOER_NATALIA"
			
	return None
			
### Leader methods ###

def startingLeader(iPlayer):
	if iPlayer in dStartingLeaders[utils.getScenario()]: return dStartingLeaders[utils.getScenario()][iPlayer]
	
	return dStartingLeaders[i3000BC][iPlayer]
	
def leader(iPlayer):
	if iPlayer >= iNumPlayers: return None
	
	if not gc.getPlayer(iPlayer).isAlive(): return None
	
	pPlayer = gc.getPlayer(iPlayer)
	tPlayer = gc.getTeam(pPlayer.getTeam())
	iNumCities = pPlayer.getNumCities()
	bReborn = pPlayer.isReborn()
	iReligion = pPlayer.getStateReligion()
	capital = gc.getPlayer(iPlayer).getCapitalCity()
	tCapitalCoords = (capital.getX(), capital.getY())
	iCivicGovernment, iCivicLegitimacy, iCivicSociety, iCivicEconomy, iCivicReligion, iCivicTerritory = getCivics(iPlayer)
	iGameTurn = gc.getGame().getGameTurn()
	bEmpire = isEmpire(iPlayer)
	bCityStates = isCityStates(iPlayer)
	bTheocracy = (iCivicReligion == iTheocracy)
	bResurrected = data.players[iPlayer].iResurrections > 0
	bMonarchy = not (isCommunist(iPlayer) or isFascist(iPlayer) or isRepublic(iPlayer))
	iAnarchyTurns = data.players[iPlayer].iAnarchyTurns
	iEra = pPlayer.getCurrentEra()
	iGameEra = gc.getGame().getCurrentEra()
	iLeader = pPlayer.getLeader()
	
	if iPlayer == iEgypt:
		if getColumn(iPlayer) >= 4: return iCleopatra
		
	elif iPlayer == iIndia:
		if not bMonarchy and iEra >= iGlobal: return iGandhi
		
		if iEra >= iRenaissance: return iShahuji
		
		if getColumn(iPlayer) >= 5: return iChandragupta
		
	elif iPlayer == iChina:
		if isCommunist(iPlayer) or isRepublic(iPlayer) and iEra >= iIndustrial: return iMao
			
		if iEra >= iRenaissance and iGameTurn >= getTurnForYear(1400): return iHongwu
	
		if bResurrected: return iHongwu
		
		if utils.getScenario() >= i1700AD: return iHongwu
		
		if iEra >= iMedieval: return iTaizong
		
	elif iPlayer == iCeltia:
		if capital.getRegionID() == rBritain:
			if capital.getX() <= 50:
				return iCollins
			elif capital.getY() >= 48:
				return iRobert
			else:
				return iBoudica
		
	elif iPlayer == iBabylonia:
		if iGameTurn >= getTurnForYear(-1600): return iHammurabi
		
	elif iPlayer == iGreece:
		if iEra >= iIndustrial: return iGeorge
		
		if bResurrected and getColumn(iPlayer) >= 11: return iGeorge
	
		if bEmpire: return iAlexanderTheGreat
		
		if not bCityStates: return iAlexanderTheGreat
		
	elif iPlayer == iPersia:
		if bReborn:
			if iEra >= iGlobal: return iKhomeini
			
			return iAbbas
		
		if getColumn(iPlayer) >= 6: return iKhosrow
			
		if bEmpire:
			return iDarius
			
	elif iPlayer == iPhoenicia:
		if not bCityStates: return iHannibal
		
		if capital.getRegionID() not in [rMesopotamia, rAnatolia]: return iHannibal
		
	elif iPlayer == iRome:
		if bEmpire or not bCityStates: return iAugustus
	
	elif iPlayer == iMaya:
		if bReborn:
			return iBolivar
		
	elif iPlayer == iKorea:		
		if iEra >= iRenaissance: return iSejong
		
		if utils.getScenario() >= i1700AD: return iSejong
		
	elif iPlayer == iJapan:
		if iEra >= iIndustrial: return iMeiji
		
		if tPlayer.isHasTech(iFeudalism): return iOdaNobunaga
		
	elif iPlayer == iEthiopia:
		if iEra >= iIndustrial: return iMenelik
		
		if iEra >= iMedieval: return iZaraYaqob
		
	elif iPlayer == iVietnam:
		if iEra >= iGlobal: return iHoChiMinh
		
		if iEra >= iMedieval: return iChieuHoang
		
	elif iPlayer == iTamils:
		if iEra >= iRenaissance: return iKrishnaDevaRaya
		
	elif iPlayer == iByzantium:
		if iGameTurn >= getTurnForYear(1000): return iBasil
		
	elif iPlayer == iVikings:
		if iEra >= iGlobal: return iGerhardsen
		
		if iEra >= iRenaissance: return iChristian
		
	elif iPlayer == iTurks:
		if bResurrected or bReborn: return iTamerlane
	
		if iGameTurn >= getTurnForYear(1000): return iAlpArslan
		
	elif iPlayer == iArabia:
		if iGameTurn >= getTurnForYear(1200): return iMustasim
		
	elif iPlayer == iTibet:
		if iGameTurn >= getTurnForYear(1500): return iLobsangGyatso
		
	elif iPlayer == iIndonesia:
		if iEra >= iGlobal: return iSuharto
		
		if bEmpire: return iHayamWuruk
		
	elif iPlayer == iBurma:
		if iNumCities > 2:
			return iBayinnuang
		
	elif iPlayer == iMoors:
		if not utils.isPlotInArea(tCapitalCoords, vic.tIberiaTL, vic.tIberiaBR): return iYaqub
		
	elif iPlayer == iSpain:
		if isFascist(iPlayer): return iFranco
		
		if True in data.lFirstContactConquerors: return iPhilip
		
	elif iPlayer == iFrance:
		if iEra >= iGlobal: return iDeGaulle
		
		if iEra >= iIndustrial: return iNapoleon
		
		if iEra >= iRenaissance: return iLouis
		
	elif iPlayer == iEngland:
		if iEra >= iGlobal: return iChurchill
		
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
			
			return iAlexanderII
			
		if iEra >= iRenaissance:
			if iGameTurn >= getTurnForYear(1750): return iCatherine
			
			return iPeter
			
	elif iPlayer == iKievanRus:
		if data.players[iPlayer].iResurrections > 0:
			return iBohdan
			
	elif iPlayer == iHungary:
		if data.players[iPlayer].iResurrections > 0:
			return iKossuth
			
	elif iPlayer == iSwahili:
		if iEra >= iIndustrial: return iBarghash
		
		if bEmpire: return iDawud
		
	elif iPlayer == iMamluks:
		if not bMonarchy and iEra >= iGlobal: return iNasser
		
		if tPlayer.isHasTech(iGunpowder): return iBaibars
		
	elif iPlayer == iNetherlands:
		if iGameTurn >= getTurnForYear(1650): return iWilliam
			
	elif iPlayer == iPoland:
		if iEra >= iGlobal: return iWalesa
		
		if isFascist(iPlayer) or isCommunist(iPlayer): return iPilsudski
	
		if iEra >= iRenaissance: return iSobieski
		
		if utils.getScenario() == i1700AD: return iSobieski
		
	elif iPlayer == iZimbabwe:
		if iEra >= iRenaissance: return iMutota
		
	elif iPlayer == iPortugal:
		if iEra >= iIndustrial: return iMaria
		
		if tPlayer.isHasTech(iCartography): return iJoao
		
	elif iPlayer == iInca:
		if iEra >= iIndustrial: return iCastilla
		
		if bResurrected and iGameTurn >= getTurnForYear(1600): return iCastilla
	
	elif iPlayer == iItaly:
		if isFascist(iPlayer): return iMussolini
	
		if iEra >= iIndustrial: return iCavour
		
	elif iPlayer == iNigeria:
		if iEra >= iIndustrial: return iAminatu
		
		if iEra >= iRenaissance: return iEwuare
		
	elif iPlayer == iMongolia:
		if iGameTurn >= getTurnForYear(1400): return iKublaiKhan
		
	elif iPlayer == iAztecs:
		if bReborn:
			if bMonarchy: return iSantaAnna
			
			if isFascist(iPlayer): return iSantaAnna
			
			if iEra >= iGlobal: return iCardenas
			
			return iJuarez
			
	elif iPlayer == iMughals:
		if iEra >= iGlobal: return iBhutto
	
		if getColumn(iPlayer) >= 9: return iAkbar
		
	elif iPlayer == iOttomans:
		if not bMonarchy and iEra >= iIndustrial: return iAtaturk
		
		if iEra >= iRenaissance: return iSuleiman
				
	elif iPlayer == iThailand:
		if iEra >= iIndustrial: return iMongkut
		
	elif iPlayer == iSweden:
		if iEra >= iIndustrial: return iKarl
		
		if bEmpire: return iGustav
		
	elif iPlayer == iManchuria:
		if iEra >= iIndustrial: return iCixi

	elif iPlayer == iGermany:
		if isFascist(iPlayer): return iHitler
		
		if getColumn(iPlayer) >= 14: return iBismarck
		
	elif iPlayer == iAmerica:
		if iEra >= iGlobal: return iRoosevelt
		
		if iGameTurn >= getTurnForYear(1850): return iLincoln
		
	elif iPlayer == iArgentina:
		if iEra >= iGlobal: return iPeron
	
	elif iPlayer == iBrazil:
		if iEra >= iGlobal: return iVargas
		
	elif iPlayer == iAustralia:
		if iEra >= iGlobal: return iMenzies
		
	elif iPlayer == iBoers:
		if iEra >= iDigital: return iMandela
		
	elif iPlayer == iCanada:
		if iEra >= iGlobal: return iTrudeau
		
	return startingLeader(iPlayer)
		
	
def leaderName(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = pPlayer.getLeader()
	
	iGameTurn = gc.getGame().getGameTurn()
	
	if iPlayer == iChina:
		if iLeader == iHongwu:
			if iGameTurn >= getTurnForYear(1700):
				return "TXT_KEY_LEADER_KANGXI"
				
	elif iPlayer == iTamils:
		if iLeader == iKrishnaDevaRaya:
			if iGameTurn >= getTurnForYear(1700):
				return "TXT_KEY_LEADER_TIPU_SULTAN"
				
	elif iPlayer == iNubia:
		if pPlayer.getStateReligion() in lChristianity:
			return "TXT_KEY_LEADER_GEORGIOS"
		if pPlayer.getStateReligion() == iIslam:
			return "TXT_KEY_LEADER_BADI"
			
	elif iPlayer == iKazakh:
		if data.players[iPlayer].iResurrections > 1:
			return "TXT_KEY_LEADER_NURSULTAN"
		if data.players[iPlayer].iResurrections > 0:
			return "TXT_KEY_ABLAI_KHAN"
			
	elif iPlayer == iCarthage:
		if gc.getGame().getGameTurnYear() >= 1956:
			return "TXT_KEY_LEADER_BEJI"
				
	return None