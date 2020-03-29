# coding: utf-8

from CvPythonExtensions import *
import CvUtil
import PyHelpers
from Consts import *
import Victory as vic
from StoredData import data
from RFCUtils import *
import CityNameManager as cnm
import Areas

from Core import *


### Constants ###

encoding = "utf-8"

tBrazilTL = (32, 14)
tBrazilBR = (43, 30)
tNCAmericaTL = (3, 33)
tNCAmericaBR = (37, 63)

tBritainTL = (48, 53)
tBritainBR = (54, 60)

tEuropeanRussiaTL = (68, 50)
tEuropeanRussiaBR = (80, 62)
lEuropeanRussiaExceptions = [(68, 59), (68, 60), (68, 61), (68, 62)]

tKhazariaTL = (71, 46)
tKhazariaBR = (79, 53)
tAnatoliaTL = (69, 41)
tAnatoliaBR = (75, 45)
iTurkicEastWestBorder = 89

tColombiaTL = (24, 26)
tColombiaBR = (28, 32)

### Setup methods ###

def findCapitalLocations(dCapitals):
	dLocations = {}
	for iCiv in dCapitals:
		for sCapital in dCapitals[iCiv]:
			dLocations[sCapital] = cnm.findLocations(slot(iCiv), sCapital)
	return dLocations

### Dictionaries with text keys

dDefaultInsertNames = {
	iCivVikings : "TXT_KEY_CIV_VIKINGS_SCANDINAVIA",
	iCivKhmer : "TXT_KEY_CIV_KHMER_KAMPUCHEA",
	iCivNetherlands : "TXT_KEY_CIV_NETHERLANDS_ARTICLE",
	iCivTamils : "TXT_KEY_CIV_TAMILS_TAMIL_NADU",
	iCivMaya : "TXT_KEY_CIV_MAYA_YUCATAN",
	iCivThailand : "TXT_KEY_CIV_THAILAND_SIAM",
	iCivMoors : "TXT_KEY_CIV_MOORS_MOROCCO",
	iCivMughals : "TXT_KEY_CIV_MUGHALS_DELHI",
	iCivHarappa : "TXT_KEY_CIV_HARAPPA_INDUS",
}

dDefaultInsertAdjectives = {
	iCivVikings : "TXT_KEY_CIV_VIKINGS_SCANDINAVIAN",
	iCivKhmer : "TXT_KEY_CIV_KHMER_KAMPUCHEAN",
	iCivThailand : "TXT_KEY_CIV_THAILAND_SIAMESE",
	iCivMoors : "TXT_KEY_CIV_MOORS_MOROCCAN",
}

dSpecificVassalTitles = deepdict({
	iCivEgypt : {
		iCivPhoenicia : "TXT_KEY_CIV_EGYPTIAN_PHOENICIA",
		iCivEthiopia : "TXT_KEY_CIV_EGYPTIAN_ETHIOPIA",
	},
	iCivBabylonia : {
		iCivPhoenicia : "TXT_KEY_ADJECTIVE_TITLE",
	},
	iCivChina : {
		iCivKorea : "TXT_KEY_CIV_CHINESE_KOREA",
		iCivTurks : "TXT_KEY_CIV_CHINESE_TURKS",
		iCivMongols : "TXT_KEY_CIV_CHINESE_MONGOLIA",
	},
	iCivGreece : {
		iCivIndia : "TXT_KEY_CIV_GREEK_INDIA",
		iCivEgypt : "TXT_KEY_CIV_GREEK_EGYPT",
		iCivPersia : "TXT_KEY_CIV_GREEK_PERSIA",
		iCivRome : "TXT_KEY_CIV_GREEK_ROME",
	},
	iCivIndia : {
		iCivAztecs: "TXT_KEY_CIV_INDIAN_AZTECS",
	},
	iCivPersia : {
		iCivEgypt : "TXT_KEY_CIV_PERSIAN_EGYPT",
		iCivIndia : "TXT_KEY_CIV_PERSIAN_INDIA",
		iCivBabylonia : "TXT_KEY_CIV_PERSIAN_BABYLONIA",
		iCivGreece : "TXT_KEY_CIV_PERSIAN_GREECE",
		iCivEthiopia : "TXT_KEY_CIV_PERSIAN_ETHIOPIA",
		iCivArabia : "TXT_KEY_CIV_PERSIAN_ARABIA",
		iCivMongols : "TXT_KEY_CIV_PERSIAN_MONGOLIA",
	},
	iCivJapan : {
		iCivChina : "TXT_KEY_CIV_JAPANESE_CHINA",
		iCivIndia : "TXT_KEY_CIV_JAPANESE_INDIA",
		iCivKorea : "TXT_KEY_CIV_JAPANESE_KOREA",
		iCivMongols : "TXT_KEY_CIV_JAPANESE_MONGOLIA",
	},
	iCivByzantium : {
		iCivEgypt : "TXT_KEY_CIV_BYZANTINE_EGYPT",
		iCivBabylonia : "TXT_KEY_CIV_BYZANTINE_BABYLONIA",
		iCivGreece : "TXT_KEY_CIV_BYZANTINE_GREECE",
		iCivPhoenicia : "TXT_KEY_CIV_BYZANTINE_CARTHAGE",
		iCivPersia : "TXT_KEY_CIV_BYZANTINE_PERSIA",
		iCivRome : "TXT_KEY_CIV_BYZANTINE_ROME",
		iCivSpain : "TXT_KEY_CIV_BYZANTINE_SPAIN",
	},
	iCivVikings : {
		iCivEngland : "TXT_KEY_CIV_VIKING_ENGLAND",
		iCivRussia : "TXT_KEY_CIV_VIKING_RUSSIA",
	},
	iCivArabia : {
		iCivOttomans : "TXT_KEY_CIV_ARABIAN_OTTOMANS",
		iCivMughals : "TXT_KEY_CIV_ARABIAN_MUGHALS",
	},
	iCivMoors : {
		iCivArabia : "TXT_KEY_CIV_MOORISH_ARABIA",
		iCivMali : "TXT_KEY_CIV_MOORISH_MALI",
	},
	iCivSpain : {
		iCivPhoenicia : "TXT_KEY_CIV_SPANISH_CARTHAGE",
		iCivEthiopia : "TXT_KEY_CIV_SPANISH_ETHIOPIA",
		iCivMaya : "TXT_KEY_CIV_SPANISH_MAYA",
		iCivByzantium : "TXT_KEY_CIV_SPANISH_BYZANTIUM",
		iCivIndonesia : "TXT_KEY_CIV_SPANISH_INDONESIA",
		iCivMoors : "TXT_KEY_CIV_SPANISH_MOORS",
		iCivFrance : "TXT_KEY_CIV_SPANISH_FRANCE",
		iCivNetherlands : "TXT_KEY_ADJECTIVE_TITLE",
		iCivMali : "TXT_KEY_CIV_SPANISH_MALI",
		iCivPortugal : "TXT_KEY_CIV_SPANISH_PORTUGAL",
		iCivAmerica : "TXT_KEY_CIV_SPANISH_AMERICA",
		iCivArgentina : "TXT_KEY_CIV_SPANISH_ARGENTINA",
		iCivColombia : "TXT_KEY_CIV_SPANISH_COLOMBIA",
	},
	iCivFrance : {
		iCivEgypt : "TXT_KEY_MANDATE_OF",
		iCivBabylonia : "TXT_KEY_CIV_FRENCH_BABYLONIA",
		iCivGreece : "TXT_KEY_CIV_FRANCE_DEPARTEMENTS_OF",
		iCivPersia : "TXT_KEY_MANDATE_OF",
		iCivPhoenicia : "TXT_KEY_CIV_FRENCH_PHOENICIA",
		iCivItaly : "TXT_KEY_CIV_FRENCH_ITALY",
		iCivEthiopia : "TXT_KEY_CIV_FRENCH_ETHIOPIA",
		iCivByzantium : "TXT_KEY_CIV_FRENCH_BYZANTIUM",
		iCivVikings : "TXT_KEY_CIV_FRANCE_DEPARTEMENTS_OF",
		iCivArabia : "TXT_KEY_MANDATE_OF",
		iCivEngland : "TXT_KEY_CIV_FRENCH_ENGLAND",
		iCivSpain : "TXT_KEY_CIV_FRENCH_SPAIN",
		iCivHolyRome : "TXT_KEY_CIV_FRENCH_HOLY_ROME",
		iCivRussia : "TXT_KEY_CIV_FRANCE_DEPARTEMENTS_OF",
		iCivPoland : "TXT_KEY_CIV_FRENCH_POLAND",
		iCivNetherlands : "TXT_KEY_CIV_FRENCH_NETHERLANDS",
		iCivMali : "TXT_KEY_CIV_FRENCH_MALI",
		iCivPortugal : "TXT_KEY_CIV_FRANCE_DEPARTEMENTS_OF",
		iCivInca : "TXT_KEY_CIV_FRENCH_INCA",
		iCivAztecs : "TXT_KEY_CIV_FRENCH_AZTECS",
		iCivMughals : "TXT_KEY_MANDATE_OF",
		iCivCongo : "TXT_KEY_ADJECTIVE_TITLE",
		iCivOttomans : "TXT_KEY_MANDATE_OF",
		iCivAmerica : "TXT_KEY_CIV_FRENCH_AMERICA",
	},
	iCivEngland : {
		iCivEgypt : "TXT_KEY_MANDATE_OF",
		iCivIndia : "TXT_KEY_CIV_ENGLISH_INDIA",
		iCivBabylonia : "TXT_KEY_CIV_ENGLISH_BABYLONIA",
		iCivPersia : "TXT_KEY_MANDATE_OF",
		iCivPhoenicia : "TXT_KEY_CIV_ENGLISH_PHOENICIA",
		iCivEthiopia : "TXT_KEY_CIV_ENGLISH_ETHIOPIA",
		iCivMaya : "TXT_KEY_CIV_ENGLISH_MAYA",
		iCivByzantium : "TXT_KEY_CIV_ENGLISH_BYZANTIUM",
		iCivVikings : "TXT_KEY_CIV_ENGLISH_VIKINGS",
		iCivArabia : "TXT_KEY_MANDATE_OF",
		iCivIndonesia : "TXT_KEY_CIV_ENGLISH_INDONESIA",
		iCivFrance : "TXT_KEY_CIV_ENGLISH_FRANCE",
		iCivHolyRome : "TXT_KEY_CIV_ENGLISH_HOLY_ROME",
		iCivGermany : "TXT_KEY_CIV_ENGLISH_GERMANY",
		iCivNetherlands : "TXT_KEY_CIV_ENGLISH_NETHERLANDS",
		iCivMali : "TXT_KEY_CIV_ENGLISH_MALI",
		iCivOttomans : "TXT_KEY_MANDATE_OF",
		iCivAmerica : "TXT_KEY_CIV_ENGLISH_AMERICA",
	},
	iCivHolyRome : {
		iCivItaly : "TXT_KEY_CIV_HOLY_ROMAN_ITALY",
		iCivFrance : "TXT_KEY_CIV_HOLY_ROMAN_FRANCE",
		iCivNetherlands : "TXT_KEY_CIV_HOLY_ROMAN_NETHERLANDS",
		iCivByzantium : "TXT_KEY_CIV_HOLY_ROMAN_BYZANTIUM",
		iCivPoland : "TXT_KEY_CIV_HOLY_ROMAN_POLAND",
	},
	iCivRussia : {
		iCivTurks : "TXT_KEY_ADJECTIVE_TITLE",
		iCivPoland : "TXT_KEY_CIV_RUSSIAN_POLAND",
		iCivAmerica : "TXT_KEY_ADJECTIVE_TITLE",
	},
	iCivNetherlands : {
		iCivIndonesia : "TXT_KEY_CIV_DUTCH_INDONESIA",
		iCivMali : "TXT_KEY_CIV_DUTCH_MALI",
		iCivEthiopia : "TXT_KEY_CIV_DUTCH_ETHIOPIA",
		iCivCongo : "TXT_KEY_CIV_DUTCH_CONGO",
		iCivAmerica : "TXT_KEY_CIV_DUTCH_AMERICA",
		iCivBrazil : "TXT_KEY_CIV_DUTCH_BRAZIL",
	},
	iCivPortugal : {
		iCivIndia : "TXT_KEY_CIV_PORTUGUESE_INDIA",
		iCivIndonesia : "TXT_KEY_CIV_PORTUGUESE_INDIA",
		iCivMali : "TXT_KEY_CIV_PORTUGUESE_MALI",
		iCivCongo : "TXT_KEY_CIV_PORTUGUESE_CONGO",
		iCivBrazil : "TXT_KEY_CIV_PORTUGUESE_BRAZIL",
	},
	iCivMongols : {
		iCivEgypt : "TXT_KEY_CIV_MONGOL_ILKHANATE",
		iCivChina : "TXT_KEY_CIV_MONGOL_CHINA",
		iCivBabylonia : "TXT_KEY_CIV_MONGOL_BABYLONIA",
		iCivGreece : "TXT_KEY_CIV_MONGOL_ILKHANATE",
		iCivPersia : "TXT_KEY_CIV_MONGOL_ILKHANATE",
		iCivPhoenicia : "TXT_KEY_CIV_MONGOL_PHOENICIA",
		iCivRome : "TXT_KEY_CIV_MONGOL_ILKHANATE",
		iCivByzantium : "TXT_KEY_CIV_MONGOL_BYZANTIUM",
		iCivRussia : "TXT_KEY_CIV_MONGOL_RUSSIA",
		iCivOttomans : "TXT_KEY_CIV_MONGOL_OTTOMANS",
		iCivMughals : "TXT_KEY_CIV_MONGOL_MUGHALS",
	},
	iCivMughals : {
		iCivIndia : "TXT_KEY_CIV_MUGHAL_INDIA",
	},
	iCivOttomans : {
		iCivEgypt : "TXT_KEY_CIV_OTTOMAN_EGYPT",
		iCivBabylonia : "TXT_KEY_CIV_OTTOMAN_BABYLONIA",
		iCivPersia : "TXT_KEY_CIV_OTTOMAN_PERSIA",
		iCivGreece : "TXT_KEY_CIV_OTTOMAN_GREECE",
		iCivPhoenicia : "TXT_KEY_CIV_OTTOMAN_PHOENICIA",
		iCivEthiopia : "TXT_KEY_CIV_OTTOMAN_ETHIOPIA",
		iCivByzantium : "TXT_KEY_CIV_OTTOMAN_BYZANTIUM",
		iCivArabia : "TXT_KEY_CIV_OTTOMAN_ARABIA",
		iCivIndonesia : "TXT_KEY_CIV_OTTOMAN_INDONESIA",
		iCivRussia : "TXT_KEY_CIV_OTTOMAN_RUSSIA",
	},
	iCivGermany : {
		iCivHolyRome : "TXT_KEY_CIV_GERMAN_HOLY_ROME",
		iCivMali : "TXT_KEY_CIV_GERMAN_MALI",
		iCivEthiopia : "TXT_KEY_CIV_GERMAN_ETHIOPIA",
		iCivPoland : "TXT_KEY_CIV_GERMAN_POLAND",
	},
	iCivAmerica : {
		iCivEngland : "TXT_KEY_CIV_AMERICAN_ENGLAND",
		iCivJapan : "TXT_KEY_CIV_AMERICAN_JAPAN",
		iCivGermany : "TXT_KEY_CIV_AMERICAN_GERMANY",
		iCivAztecs : "TXT_KEY_CIV_AMERICAN_MEXICO",
		iCivMaya : "TXT_KEY_CIV_AMERICAN_MAYA",
		iCivKorea : "TXT_KEY_CIV_AMERICAN_KOREA",
	},
	iCivBrazil : {
		iCivArgentina : "TXT_KEY_CIV_BRAZILIAN_ARGENTINA",
	},
})

dMasterTitles = {
	iCivChina : "TXT_KEY_CIV_CHINESE_VASSAL",
	iCivIndia : "TXT_KEY_CIV_INDIAN_VASSAL",
	iCivPersia : "TXT_KEY_CIV_PERSIAN_VASSAL",
	iCivRome : "TXT_KEY_CIV_ROMAN_VASSAL",
	iCivJapan : "TXT_KEY_CIV_JAPANESE_VASSAL",
	iCivByzantium : "TXT_KEY_CIV_BYZANTINE_VASSAL",
	iCivTurks : "TXT_KEY_CIV_TURKIC_VASSAL",
	iCivArabia : "TXT_KEY_CIV_ARABIAN_VASSAL",
	iCivTibet : "TXT_KEY_CIV_TIBETAN_VASSAL",
	iCivIndonesia : "TXT_KEY_CIV_INDONESIAN_VASSAL",
	iCivMoors : "TXT_KEY_CIV_ARABIAN_VASSAL",
	iCivSpain : "TXT_KEY_CIV_SPANISH_VASSAL",
	iCivFrance : "TXT_KEY_ADJECTIVE_TITLE",
	iCivEngland : "TXT_KEY_CIV_ENGLISH_VASSAL",
	iCivRussia : "TXT_KEY_CIV_RUSSIAN_VASSAL",
	iCivNetherlands : "TXT_KEY_ADJECTIVE_TITLE",
	iCivPortugal : "TXT_KEY_ADJECTIVE_TITLE",
	iCivMongols : "TXT_KEY_CIV_MONGOL_VASSAL",
	iCivMughals : "TXT_KEY_CIV_MUGHAL_VASSAL",
	iCivOttomans : "TXT_KEY_CIV_OTTOMAN_VASSAL",
	iCivThailand : "TXT_KEY_CIV_THAI_VASSAL",
}

dCommunistVassalTitlesGeneric = {
	iCivRussia : "TXT_KEY_CIV_RUSSIA_SOVIET",
}

dCommunistVassalTitles = deepdict({
	iCivRussia : {
		iCivChina : "TXT_KEY_CIV_RUSSIA_SOVIET_REPUBLIC_ADJECTIVE",
		iCivTurks : "TXT_KEY_CIV_RUSSIA_SOVIET_TURKS",
		iCivJapan : "TXT_KEY_CIV_RUSSIA_SOVIET_JAPAN",
		iCivOttomans : "TXT_KEY_CIV_RUSSIA_SOVIET_OTTOMANS",
		iCivGermany : "TXT_KEY_CIV_RUSSIA_SOVIET_GERMANY",
	},
})

dFascistVassalTitlesGeneric = {
	iCivGermany : "TXT_KEY_ADJECTIVE_TITLE"
}

dFascistVassalTitles = deepdict({
	iCivGermany : {
		iCivEgypt : "TXT_KEY_CIV_GERMANY_REICHSPROTEKTORAT",
		iCivChina : "TXT_KEY_CIV_GERMANY_REICHSKOMMISSARIAT",
		iCivGreece : "TXT_KEY_CIV_GERMANY_NAZI_GREECE",
		iCivPhoenicia : "TXT_KEY_CIV_GERMANY_REICHSKOMMISSARIAT",
		iCivRome : "TXT_KEY_CIV_GERMANY_REICHSPROTEKTORAT",
		iCivEthiopia : "TXT_KEY_CIV_GERMANY_NAZI_ETHIOPIA",
		iCivByzantium : "TXT_KEY_CIV_GERMANY_NAZI_BYZANTIUM",
		iCivSpain : "TXT_KEY_CIV_GERMANY_REICHSKOMMISSARIAT",
		iCivFrance : "TXT_KEY_CIV_GERMANY_NAZI_FRANCE",
		iCivEngland : "TXT_KEY_CIV_GERMANY_REICHSKOMMISSARIAT",
		iCivHolyRome : "TXT_KEY_CIV_GERMANY_NAZI_HOLY_ROME",
		iCivRussia : "TXT_KEY_CIV_GERMANY_NAZI_RUSSIA",
		iCivNetherlands : "TXT_KEY_CIV_GERMANY_NAZI_NETHERLANDS",
		iCivMali : "TXT_KEY_CIV_GERMANY_NAZI_MALI",
		iCivPoland : "TXT_KEY_CIV_GERMANY_NAZI_POLAND",
		iCivPortugal : "TXT_KEY_CIV_GERMANY_REICHSKOMMISSARIAT",
		iCivMughals : "TXT_KEY_CIV_GERMANY_NAZI_MUGHALS",
		iCivOttomans : "TXT_KEY_CIV_GERMANY_REICHSKOMMISSARIAT",
		iCivCanada : "TXT_KEY_CIV_GERMANY_NAZI_CANADA",
	},
})

dForeignAdjectives = deepdict({
	iCivChina : {
		iCivEgypt : "TXT_KEY_CIV_CHINESE_ADJECTIVE_EGYPT",
		iCivIndia : "TXT_KEY_CIV_CHINESE_ADJECTIVE_INDIA",
		iCivBabylonia : "TXT_KEY_CIV_CHINESE_ADJECTIVE_BABYLONIA",
		iCivPersia : "TXT_KEY_CIV_CHINESE_ADJECTIVE_PERSIA",
		iCivRome : "TXT_KEY_CIV_CHINESE_ADJECTIVE_ROME",
		iCivJapan : "TXT_KEY_CIV_CHINESE_ADJECTIVE_JAPAN",
		iCivKorea : "TXT_KEY_CIV_CHINESE_ADJECTIVE_KOREA",
		iCivByzantium : "TXT_KEY_CIV_CHINESE_ADJECTIVE_BYZANTIUM",
		iCivArabia : "TXT_KEY_CIV_CHINESE_ADJECTIVE_ARABIA",
		iCivKhmer : "TXT_KEY_CIV_CHINESE_ADJECTIVE_KHMER",
		iCivIndonesia : "TXT_KEY_CIV_CHINESE_ADJECTIVE_INDONESIA",
		iCivMongols : "TXT_KEY_CIV_CHINESE_ADJECTIVE_MONGOLIA",
		iCivOttomans : "TXT_KEY_CIV_CHINESE_ADJECTIVE_OTTOMANS",
		iCivTibet : "TXT_KEY_CIV_CHINESE_ADJECTIVE_TIBET",
	},
})

dForeignNames = deepdict({
	iCivGreece : {
		iCivTurks : "TXT_KEY_CIV_GREEK_NAME_TURKS",
	},
	iCivPersia : {
		iCivByzantium : "TXT_KEY_CIV_PERSIAN_NAME_BYZANTIUM",
		iCivTurks : "TXT_KEY_CIV_PERSIAN_NAME_TURKS",
		iCivIndonesia : "TXT_KEY_CIV_PERSIAN_NAME_INDONESIA",
	},
	iCivRome : {
		iCivEgypt : "TXT_KEY_CIV_ROMAN_NAME_EGYPT",
		iCivChina : "TXT_KEY_CIV_ROMAN_NAME_CHINA",
		iCivBabylonia : "TXT_KEY_CIV_ROMAN_NAME_BABYLONIA",
		iCivGreece : "TXT_KEY_CIV_ROMAN_NAME_GREECE",
		iCivPersia : "TXT_KEY_CIV_ROMAN_NAME_PERSIA",
		iCivPhoenicia : "TXT_KEY_CIV_ROMAN_NAME_PHOENICIA",
		iCivEthiopia : "TXT_KEY_CIV_ROMAN_NAME_ETHIOPIA",
		iCivByzantium : "TXT_KEY_CIV_ROMAN_NAME_BYZANTIUM",
		iCivVikings : "TXT_KEY_CIV_ROMAN_NAME_VIKINGS",
		iCivTurks : "TXT_KEY_CIV_ROMAN_NAME_TURKS",
		iCivKhmer : "TXT_KEY_CIV_ROMAN_NAME_KHMER",
		iCivSpain : "TXT_KEY_CIV_ROMAN_NAME_SPAIN",
		iCivFrance : "TXT_KEY_CIV_ROMAN_NAME_FRANCE",
		iCivEngland : "TXT_KEY_CIV_ROMAN_NAME_ENGLAND",
		iCivHolyRome : "TXT_KEY_CIV_ROMAN_NAME_HOLY_ROME",
		iCivGermany : "TXT_KEY_CIV_ROMAN_NAME_GERMANY",
		iCivRussia : "TXT_KEY_CIV_ROMAN_NAME_RUSSIA",
		iCivNetherlands : "TXT_KEY_CIV_ROMAN_NAME_NETHERLANDS",
		iCivMali : "TXT_KEY_CIV_ROMAN_NAME_MALI",
		iCivPortugal : "TXT_KEY_CIV_ROMAN_NAME_PORTUGAL",
		iCivMongols : "TXT_KEY_CIV_ROMAN_NAME_MONGOLIA",
		iCivOttomans : "TXT_KEY_CIV_ROMAN_NAME_OTTOMANS",
		iCivThailand : "TXT_KEY_CIV_ROMAN_NAME_THAILAND",
	},
	iCivArabia : {
		iCivEgypt : "TXT_KEY_CIV_ARABIAN_NAME_EGYPT",
		iCivBabylonia : "TXT_KEY_CIV_ARABIAN_NAME_BABYLONIA",
		iCivPersia : "TXT_KEY_CIV_ARABIAN_NAME_PERSIA",
		iCivPhoenicia : "TXT_KEY_CIV_ARABIAN_NAME_CARTHAGE",
		iCivRome : "TXT_KEY_CIV_ARABIAN_NAME_ROME",
		iCivEthiopia : "TXT_KEY_CIV_ARABIAN_NAME_ETHIOPIA",
		iCivByzantium : "TXT_KEY_CIV_ARABIAN_NAME_BYZANTIUM",
		iCivTurks : "TXT_KEY_CIV_ARABIAN_NAME_TURKS",
		iCivArabia : "TXT_KEY_CIV_ARABIAN_NAME_ARABIA",
		iCivIndonesia : "TXT_KEY_CIV_ARABIAN_NAME_INDONESIA",
		iCivMoors : "TXT_KEY_CIV_ARABIAN_NAME_MOORS",
		iCivSpain : "TXT_KEY_CIV_ARABIAN_NAME_SPAIN",
		iCivPortugal : "TXT_KEY_CIV_ARABIAN_NAME_PORTUGAL",
	},
	iCivTibet : {
		iCivChina : "TXT_KEY_CIV_TIBETAN_NAME_CHINA",
		iCivIndia : "TXT_KEY_CIV_TIBETAN_NAME_INDIA",
		iCivTurks : "TXT_KEY_CIV_TIBETAN_NAME_TURKS",
		iCivMongols : "TXT_KEY_CIV_TIBETAN_NAME_MONGOLIA",
	},
	iCivMoors : {
		iCivEgypt : "TXT_KEY_CIV_ARABIAN_NAME_EGYPT",
		iCivBabylonia : "TXT_KEY_CIV_ARABIAN_NAME_BABYLONIA",
		iCivPersia : "TXT_KEY_CIV_ARABIAN_NAME_PERSIA",
		iCivPhoenicia : "TXT_KEY_CIV_ARABIAN_NAME_CARTHAGE",
		iCivRome : "TXT_KEY_CIV_ARABIAN_NAME_ROME",
		iCivEthiopia : "TXT_KEY_CIV_ARABIAN_NAME_ETHIOPIA",
		iCivByzantium : "TXT_KEY_CIV_ARABIAN_NAME_BYZANTIUM",
		iCivArabia : "TXT_KEY_CIV_ARABIAN_NAME_ARABIA",
		iCivMoors : "TXT_KEY_CIV_ARABIAN_NAME_MOORS",
		iCivSpain : "TXT_KEY_CIV_ARABIAN_NAME_SPAIN",
		iCivPortugal : "TXT_KEY_CIV_ARABIAN_NAME_PORTUGAL",
	},
	iCivSpain : {
		iCivKhmer : "TXT_KEY_CIV_SPANISH_NAME_KHMER",
		iCivAztecs : "TXT_KEY_CIV_SPANISH_NAME_AZTECS",
		iCivMughals : "TXT_KEY_CIV_SPANISH_NAME_MUGHALS",
	},
	iCivFrance : {
		iCivKhmer : "TXT_KEY_CIV_FRENCH_NAME_KHMER",
		iCivMughals : "TXT_KEY_CIV_FRENCH_NAME_MUGHALS",
	},
	iCivEngland : {
		iCivKhmer : "TXT_KEY_CIV_ENGLISH_NAME_KHMER",
		iCivMughals : "TXT_KEY_CIV_ENGLISH_NAME_MUGHALS",
	},
	iCivRussia : {
		iCivPersia : "TXT_KEY_CIV_RUSSIAN_NAME_PERSIA",
	},
	iCivMongols : {
		iCivTurks : "TXT_KEY_CIV_MONGOL_NAME_TURKS"
	},
	iCivGermany : {
		iCivMoors : "TXT_KEY_CIV_GERMAN_NAME_MOORS",
	},
})

lRepublicOf = [iCivEgypt, iCivIndia, iCivChina, iCivPersia, iCivJapan, iCivEthiopia, iCivKorea, iCivVikings, iCivTurks, iCivTibet, iCivIndonesia, iCivKhmer, iCivHolyRome, iCivMali, iCivPoland, iCivMughals, iCivOttomans, iCivThailand]
lRepublicAdj = [iCivBabylonia, iCivRome, iCivMoors, iCivSpain, iCivFrance, iCivPortugal, iCivInca, iCivItaly, iCivAztecs, iCivArgentina]

lSocialistRepublicOf = [iCivMoors, iCivHolyRome, iCivBrazil, iCivVikings]
lSocialistRepublicAdj = [iCivPersia, iCivTurks, iCivItaly, iCivAztecs, iCivArgentina]

lPeoplesRepublicOf = [iCivIndia, iCivChina, iCivPolynesia, iCivJapan, iCivTibet, iCivIndonesia, iCivMali, iCivPoland, iCivMughals, iCivThailand, iCivCongo]
lPeoplesRepublicAdj = [iCivTamils, iCivByzantium, iCivMongols]

lIslamicRepublicOf = [iCivIndia, iCivPersia, iCivMali, iCivMughals]

lCityStatesStart = [iCivRome, iCivCarthage, iCivGreece, iCivIndia, iCivMaya, iCivAztecs]

dEmpireThreshold = {
	iCivCarthage : 4,
	iCivIndonesia : 4,
	iCivKorea : 4,
	iCivRussia : 8,
	iCivHolyRome : 3,
	iCivGermany : 4,
	iCivItaly : 4,
	iCivInca : 3,
	iCivMongols : 6,
	iCivPoland : 3,
	iCivMoors : 3,
	iCivTibet : 2,
	iCivPolynesia : 3,
	iCivTamils : 3,
	iCivIran : 4,
}

lChristianity = [iCatholicism, iOrthodoxy, iProtestantism]

lRespawnNameChanges = [iCivHolyRome, iCivInca, iCivAztecs, iCivMali] # TODO: this should be covered by period
lVassalNameChanges = [iCivInca, iCivAztecs, iCivMughals] # TODO: this should be covered by period
lChristianityNameChanges = [iCivInca, iCivAztecs] # TODO: this should be covered by period

lColonies = [iCivMali, iCivEthiopia, iCivCongo, iCivAztecs, iCivInca, iCivMaya] # TODO: could be covered by more granular continental regions

dNameChanges = { # TODO: this should be covered by period
	iCivPhoenicia : "TXT_KEY_CIV_CARTHAGE_SHORT_DESC",
	iCivAztecs : "TXT_KEY_CIV_MEXICO_SHORT_DESC",
	iCivInca : "TXT_KEY_CIV_PERU_SHORT_DESC",
	iCivHolyRome : "TXT_KEY_CIV_AUSTRIA_SHORT_DESC",
	iCivMali : "TXT_KEY_CIV_SONGHAI_SHORT_DESC",
	iCivMughals : "TXT_KEY_CIV_PAKISTAN_SHORT_DESC",
	iCivVikings : "TXT_KEY_CIV_SWEDEN_SHORT_DESC",
	iCivMoors : "TXT_KEY_CIV_MOROCCO_SHORT_DESC",
}

dAdjectiveChanges = {
	iCivPhoenicia : "TXT_KEY_CIV_CARTHAGE_ADJECTIVE",
	iCivAztecs : "TXT_KEY_CIV_MEXICO_ADJECTIVE",
	iCivInca : "TXT_KEY_CIV_PERU_ADJECTIVE",
	iCivHolyRome : "TXT_KEY_CIV_AUSTRIA_ADJECTIVE",
	iCivMali : "TXT_KEY_CIV_SONGHAI_ADJECTIVE",
	iCivMughals : "TXT_KEY_CIV_PAKISTAN_ADJECTIVE",
	iCivVikings : "TXT_KEY_CIV_SWEDEN_ADJECTIVE",
	iCivMoors : "TXT_KEY_CIV_MOROCCO_ADJECTIVE",
}

dCapitals = {
	iCivPolynesia : ["Kaua'i", "O'ahu", "Maui", "Manu'a", "Niue"],
	iCivBabylonia : ["Ninua", "Kalhu"],
	iCivByzantium : ["Dyrrachion", "Athena", "Konstantinoupolis"],
	iCivVikings : ["Stockholm", "Oslo", "Nidaros", "Kalmar", "Roskilde"],
	iCivKhmer : ["Pagan", "Dali", "Angkor", "Hanoi"],
	iCivHolyRome : ["Buda"],
	iCivRussia : ["Moskva", "Kiev"],
	iCivItaly : ["Fiorenza", "Roma"],
	iCivTamils : ["Madurai", "Thiruvananthapuram", "Cochin", "Kozhikode"],
	iCivArabia : ["Dimashq"],
	iCivSpain : ["La Paz", "Barcelona", "Valencia"],
	iCivPoland : ["Kowno", "Medvegalis", "Wilno", "Ryga"],
	iCivNetherlands : ["Brussels", "Antwerpen"], # TODO: no matches for Brussels
}

dStartingLeaders = [
# 3000 BC
{
	iCivEgypt : iRamesses,
	iCivIndia : iAsoka,
	iCivBabylonia : iSargon,
	iCivHarappa : iVatavelli,
	iCivChina : iQinShiHuang,
	iCivGreece : iPericles,
	iCivPersia : iCyrus,
	iCivCarthage : iHiram,
	iCivPolynesia : iAhoeitu,
	iCivRome : iJuliusCaesar,
	iCivMaya : iPacal,
	iCivJapan : iKammu,
	iCivTamils : iRajendra,
	iCivEthiopia : iEzana,
	iCivKorea : iWangKon,
	iCivByzantium : iJustinian,
	iCivVikings : iRagnar,
	iCivTurks : iBumin,
	iCivArabia : iHarun,
	iCivTibet : iSongtsen,
	iCivKhmer : iSuryavarman,
	iCivIndonesia : iDharmasetu,
	iCivMoors : iRahman,
	iCivSpain : iIsabella,
	iCivFrance : iCharlemagne,
	iCivEngland : iAlfred,
	iCivHolyRome : iBarbarossa,
	iCivRussia : iIvan,
	iCivNetherlands : iWillemVanOranje,
	iCivMali : iMansaMusa,
	iCivPoland : iCasimir,
	iCivPortugal : iAfonso,
	iCivInca : iHuaynaCapac,
	iCivItaly : iLorenzo,
	iCivMongols : iGenghisKhan,
	iCivAztecs : iMontezuma,
	iCivMughals : iTughluq,
	iCivOttomans : iMehmed,
	iCivThailand : iNaresuan,
	iCivCongo : iMbemba,
	iCivIran : iAbbas,
	iCivGermany : iFrederick,
	iCivAmerica : iWashington,
	iCivArgentina : iSanMartin,
	iCivMexico : iJuarez,
	iCivColombia : iBolivar,
	iCivBrazil : iPedro,
	iCivCanada : iMacDonald,
},
# 600 AD
{
	iCivChina : iTaizong,
},
# 1700 AD
{
	iCivChina : iHongwu,
	iCivIndia : iShahuji,
	iCivIran : iAbbas,
	iCivTamils : iKrishnaDevaRaya,
	iCivKorea : iSejong,
	iCivJapan : iOdaNobunaga,
	iCivTurks : iTamerlane,
	iCivVikings : iGustav,
	iCivSpain : iPhilip,
	iCivFrance : iLouis,
	iCivEngland : iVictoria,
	iCivHolyRome : iFrancis,
	iCivRussia : iPeter,
	iCivNetherlands : iWilliam,
	iCivPoland : iSobieski,
	iCivPortugal : iJoao,
	iCivMughals : iAkbar,
	iCivOttomans : iSuleiman,
	iCivGermany : iFrederick,
}]

### Event handlers

def setup():
	data.dCapitalLocations = findCapitalLocations(dCapitals)
	
	iScenario = scenario()
	
	if iScenario == i600AD:
		data.players[slot(iCivChina)].iAnarchyTurns += 3
		
	elif iScenario == i1700AD:
		data.players[slot(iCivEgypt)].iResurrections += 1
		
		for iCiv in [iCivVikings, iCivMoors]:
			nameChange(slot(iCiv))
			adjectiveChange(slot(iCiv))
	
	for iPlayer in players.major():
		setDesc(iPlayer, peoplesName(iPlayer))
		
		if player(iPlayer).getNumCities() > 0:
			checkName(iPlayer)
		
		if (year(dBirth[iPlayer]) >= year() or player(iPlayer).getNumCities() > 0) and not player(iPlayer).isHuman():
			setLeader(iPlayer, startingLeader(iPlayer))
		
def onCivRespawn(iPlayer, tOriginalOwners):
	data.players[iPlayer].iResurrections += 1
	
	if civ(iPlayer) in lRespawnNameChanges:
		nameChange(iPlayer)
		adjectiveChange(iPlayer)
		
	setDesc(iPlayer, defaultTitle(iPlayer))
	checkName(iPlayer)
	checkLeader(iPlayer)
	
def onVassalState(iMaster, iVassal):
	iMasterCiv = civ(iMaster)
	iVassalCiv = civ(iVassal)

	if iVassalCiv in lVassalNameChanges:
		if iVassalCiv == iCivMughals and iMasterCiv not in dCivGroups[iCivGroupEurope]: return
	
		data.players[iVassal].iResurrections += 1
		nameChange(iVassal)
		adjectiveChange(iVassal)
		
	checkName(iVassal)
	
def onPlayerChangeStateReligion(iPlayer, iReligion):
	if civ(iPlayer) in lChristianityNameChanges and iReligion in lChristianity:
		data.players[iPlayer].iResurrections += 1
		nameChange(iPlayer)
		adjectiveChange(iPlayer)
		
	checkName(iPlayer)
	
def onRevolution(iPlayer):
	data.players[iPlayer].iAnarchyTurns += 1
	
	if civ(iPlayer) == iCivMughals and isRepublic(iPlayer):
		nameChange(iPlayer)
	
	checkName(iPlayer)
	
	for iLoopPlayer in players.vassals(iPlayer):
		checkName(iLoopPlayer)
	
def onCityAcquired(iPreviousOwner, iNewOwner):
	checkName(iPreviousOwner)
	checkName(iNewOwner)
	
def onCityRazed(iOwner):
	checkName(iOwner)
	
def onCityBuilt(iOwner):
	checkName(iOwner)
	
def onTechAcquired(iPlayer, iTech):
	iEra = infos.tech(iTech).getEra()
	iCiv = civ(iPlayer)
	
	if iCiv == iCivVikings:
		if iEra == iRenaissance:
			if isCapital(iPlayer, ["Stockholm", "Kalmar"]):
				setShort(iPlayer, text("TXT_KEY_CIV_SWEDEN_SHORT_DESC"))
				setAdjective(iPlayer, text("TXT_KEY_CIV_SWEDEN_ADJECTIVE"))
			
			elif isCapital(iPlayer, ["Oslo", "Nidaros"]):
				setShort(iPlayer, text("TXT_KEY_CIV_NORWAY_SHORT_DESC"))
				setAdjective(iPlayer, text("TXT_KEY_CIV_NORWAY_ADJECTIVE"))
			
			elif isCapital(iPlayer, ["Roskilde"]):
				setShort(iPlayer, text("TXT_KEY_CIV_DENMARK_SHORT_DESC"))
				setAdjective(iPlayer, text("TXT_KEY_CIV_DENMARK_ADJECTIVE"))
				
	elif iCiv == iCivMoors:
		if iEra == iIndustrial:
			capital = player(iPlayer).getCapitalCity()
			
			if capital and capital.getRegionID() != rIberia:
				nameChange(iPlayer)
				adjectiveChange(iPlayer)
			else:
				setShort(iPlayer, short(iPlayer))
				setAdjective(iPlayer, civAdjective(iPlayer))
				
	checkName(iPlayer)
	
def onPalaceMoved(iPlayer):
	capital = player(iPlayer).getCapitalCity()
	iEra = player(iPlayer).getCurrentEra()
	iCiv = civ(iPlayer)

	if iCiv == iCivPhoenicia:
		if capital.getRegionID() not in [rMesopotamia, rAnatolia]:
			nameChange(iPlayer)
			adjectiveChange(iPlayer)
		else:
			setShort(iPlayer, short(iPlayer))
			setAdjective(iPlayer, civAdjective(iPlayer))
			
	elif iCiv == iCivVikings:
		if iEra >= iRenaissance:
			if isCapital(iPlayer, ["Stockholm", "Kalmar"]):
				setShort(iPlayer, text("TXT_KEY_CIV_SWEDEN_SHORT_DESC"))
				setAdjective(iPlayer, text("TXT_KEY_CIV_SWEDEN_ADJECTIVE"))
			
			elif isCapital(iPlayer, ["Oslo", "Nidaros"]):
				setShort(iPlayer, text("TXT_KEY_CIV_NORWAY_SHORT_DESC"))
				setAdjective(iPlayer, text("TXT_KEY_CIV_NORWAY_ADJECTIVE"))
			
			elif isCapital(iPlayer, ["Roskilde"]):
				setShort(iPlayer, text("TXT_KEY_CIV_DENMARK_SHORT_DESC"))
				setAdjective(iPlayer, text("TXT_KEY_CIV_DENMARK_ADJECTIVE"))
				
	elif iCiv == iCivMoors:
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
	for iPlayer in players.major():
		checkName(iPlayer)
		checkLeader(iPlayer)
		
def checkName(iPlayer):
	if not player(iPlayer).isAlive(): return
	if is_minor(iPlayer): return
	if player(iPlayer).getNumCities() == 0: return
	setDesc(iPlayer, desc(iPlayer, title(iPlayer)))
	
def checkLeader(iPlayer):
	if not player(iPlayer).isAlive(): return
	if is_minor(iPlayer): return
	setLeader(iPlayer, leader(iPlayer))
	setLeaderName(iPlayer, leaderName(iPlayer))

### Setter methods for player object ###

def setDesc(iPlayer, sName):
	try:
		player(iPlayer).setCivDescription(sName)
	except:
		pass
	
def setShort(iPlayer, sShort):
	player(iPlayer).setCivShortDescription(sShort)
	
def setAdjective(iPlayer, sAdj):
	player(iPlayer).setCivAdjective(sAdj)
	
def setLeader(iPlayer, iLeader):
	if not iLeader: return
	if player(iPlayer).getLeader() == iLeader: return
	player(iPlayer).setLeader(iLeader)
	
def setLeaderName(iPlayer, sName):
	if not sName: return
	if infos.leader(player(iPlayer)).getText() != sName:
		player(iPlayer).setLeaderName(sName)

### Utility methods ###

def key(iPlayer, sSuffix):
	if sSuffix: sSuffix = "_%s" % sSuffix
	return "TXT_KEY_CIV_%s%s" % (str(short(iPlayer).replace(" ", "_").upper()), sSuffix)
	
def desc(iPlayer, sTextKey=str("%s1")):
	if team(iPlayer).isAVassal():
		return text(sTextKey, name(iPlayer), adjective(iPlayer), name(iPlayer, True), adjective(iPlayer, True))

	return text(sTextKey, name(iPlayer), adjective(iPlayer))

# TODO: overlap with name()
def short(iPlayer):
	return player(iPlayer).getCivilizationShortDescription(0)

# TODO: overlap with adjective()
def civAdjective(iPlayer):
	return player(iPlayer).getCivilizationAdjective(0)

def capitalName(iPlayer):
	capital = player(iPlayer).getCapitalCity()
	if capital: 
		sCapitalName = cnm.getLanguageRename(cnm.iLangEnglish, capital.getName()) # TODO
		if sCapitalName: return sCapitalName
		else: return capital.getName()
	
	return short(iPlayer)
	
def nameChange(iPlayer):
	iCiv = civ(iPlayer)

	if iCiv in dNameChanges:
		setShort(iPlayer, text(dNameChanges[iCiv]))
	
def adjectiveChange(iPlayer):
	iCiv = civ(iPlayer)
	if iCiv in dAdjectiveChanges:
		setAdjective(iPlayer, text(dAdjectiveChanges[iCiv]))
	
def getColumn(iPlayer):
	lTechs = [infos.tech(iTech).getGridX() for iTech in range(iNumTechs) if team(iPlayer).isHasTech(iTech)]
	if not lTechs: return 0
	return max(lTechs)
	
### Utility methods for civilization status ###

# TODO: use container object?
def getCivics(iPlayer):
	pPlayer = player(iPlayer)
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
	
	if iGovernment == iChiefdom and civ(iPlayer) in lCityStatesStart: return True
	
	return False
	
def isCapitulated(iPlayer):
	return team(iPlayer).isAVassal() and team(iPlayer).isCapitulated()
	
def isEmpire(iPlayer):
	if team(iPlayer).isAVassal(): return False

	return player(iPlayer).getNumCities() >= getEmpireThreshold(iPlayer)
	
def getEmpireThreshold(iPlayer):
	iCiv = civ(iPlayer)

	if iCiv in dEmpireThreshold: return dEmpireThreshold[iCiv]
	
	if iCiv == iCivEthiopia and not game.isReligionFounded(iIslam):
		return 4
		
	return 5
	
def isAtWar(iPlayer):
	for iTarget in players.major():
		if team(iPlayer).isAtWar(iTarget):
			return True
	return False
	
def isCapital(iPlayer, lNames):
	capital = player(iPlayer).getCapitalCity()
	if not capital: return False
	
	tLocation = location(capital)
	
	for sName in lNames:
		if tLocation in data.dCapitalLocations[sName]:
			return True
			
	return False
	
def countAreaCities(lPlots):
	return cities.of(lPlots).count()
	
def countPlayerAreaCities(iPlayer, lPlots):
	return cities.of(lPlots).owner(iPlayer).count()
	
def isAreaControlled(iPlayer, tTL, tBR, iMinCities=1, lExceptions=[]):
	return isControlled(iPlayer, plots.start(tTL).end(tBR).without(lExceptions), iMinCities)
	
def isRegionControlled(iPlayer, iRegion, iMinCities=1):
	return isControlled(iPlayer, plots.region(iRegion), iMinCities)
	
def isControlled(iPlayer, area, iMinCities=1):
	iTotalCities = area.cities().count()
	iPlayerCities = area.cities().owner(iPlayer).count()
	
	if iPlayerCities < iTotalCities: return False
	if iPlayerCities < iMinCities: return False
	
	return True
	
def capitalCoords(iPlayer):
	capital = player(iPlayer).getCapitalCity()
	if capital: return location(capital)
	
	return (-1, -1)
	
def controlsHolyCity(iPlayer, iReligion):
	holyCity = game.getHolyCity(iReligion)
	if holyCity and holyCity.getOwner() == iPlayer: return True
	
	return False
	
def controlsCity(iPlayer, (x, y)):
	plot = plot_(x, y)
	return plot.isCity() and plot.getPlotCity().getOwner() == iPlayer
	
### Naming methods ###

def name(iPlayer, bIgnoreVassal = False):
	iCiv = civ(iPlayer)

	if isCapitulated(iPlayer) and not bIgnoreVassal:
		sVassalName = vassalName(iPlayer, getMaster(iPlayer))
		if sVassalName: return sVassalName
		
	if isCommunist(iPlayer) or isFascist(iPlayer) or isRepublic(iPlayer):
		sRepublicName = republicName(iPlayer)
		if sRepublicName: return sRepublicName
		
	sSpecificName = specificName(iPlayer)
	if sSpecificName: return sSpecificName
	
	sDefaultInsertName = dDefaultInsertNames.get(iCiv)
	if sDefaultInsertName: return sDefaultInsertName
	
	return short(iPlayer)
	
def vassalName(iPlayer, iMaster):
	iMasterCiv = civ(iMaster)
	iCiv = civ(iPlayer)

	if iMasterCiv == iCivRome and player(iPlayer).getPeriod() == iPeriodCarthage:
		return "TXT_KEY_CIV_ROMAN_NAME_CARTHAGE"
		
	if iCiv == iCivNetherlands: return short(iPlayer)

	sSpecificName = dForeignNames[iMasterCiv].get(iCiv)
	if sSpecificName: return sSpecificName
	
	return None
	
def republicName(iPlayer):
	iCiv = civ(iPlayer)

	if iCiv in [iCivMoors, iCivEngland]: return None
	
	if iCiv == iCivInca and data.players[iPlayer].iResurrections > 0: return None
	
	if iCiv == iCivNetherlands and isCommunist(iPlayer): return "TXT_KEY_CIV_NETHERLANDS_ARTICLE"
	
	if iCiv == iCivTurks: return "TXT_KEY_CIV_TURKS_UZBEKISTAN"

	return short(iPlayer)
	
def peoplesName(iPlayer):
	return desc(iPlayer, key(iPlayer, "PEOPLES"))
	
def specificName(iPlayer):
	iCiv = civ(iPlayer)
	pPlayer = player(iPlayer)
	tPlayer = team(iPlayer)
	iCivicGovernment, iCivicLegitimacy, iCivicSociety, iCivicEconomy, iCivicReligion, iCivicTerritory = getCivics(iPlayer)
	
	iNumCities = pPlayer.getNumCities()
	if iNumCities == 0: return short(iPlayer)
	
	bReborn = pPlayer.isReborn()
	iReligion = pPlayer.getStateReligion()
	capital = player(iPlayer).getCapitalCity()
	tCapitalCoords = capitalCoords(iPlayer)
	bAnarchy = pPlayer.isAnarchy()
	bEmpire = isEmpire(iPlayer)
	bCityStates = isCityStates(iPlayer)
	bTheocracy = (iCivicReligion == iTheocracy)
	bResurrected = data.players[iPlayer].iResurrections > 0
	bCapitulated = isCapitulated(iPlayer)
	iAnarchyTurns = data.players[iPlayer].iAnarchyTurns
	iEra = pPlayer.getCurrentEra()
	iGameEra = game.getCurrentEra()
	bWar = isAtWar(iPlayer)
			
	if iCiv == iCivBabylonia:
		if isCapital(iPlayer, ["Ninua", "Kalhu"]):
			return "TXT_KEY_CIV_BABYLONIA_ASSYRIA"
	
	elif iCiv == iCivChina:
		if bEmpire:
			if iEra >= iIndustrial or scenario() == i1700AD:
				return "TXT_KEY_CIV_CHINA_QING"
			
			if iEra == iRenaissance and turn() >= year(1400):
				return "TXT_KEY_CIV_CHINA_MING"
			
	elif iCiv == iCivGreece:
		if not bCityStates and bEmpire and iEra <= iClassical:
			return "TXT_KEY_CIV_GREECE_MACEDONIA"
			
	elif iCiv == iCivPolynesia:
		if isCapital(iPlayer, ["Kaua'i", "O'ahu", "Maui"]):
			return "TXT_KEY_CIV_POLYNESIA_HAWAII"
			
		if isCapital(iPlayer, ["Manu'a"]):
			return "TXT_KEY_CIV_POLYNESIA_SAMOA"
			
		if isCapital(iPlayer, ["Niue"]):
			return "TXT_KEY_CIV_POLYNESIA_NIUE"
			
		return "TXT_KEY_CIV_POLYNESIA_TONGA"
		
	elif iCiv == iCivTamils:
		if iEra >= iRenaissance:
			return "TXT_KEY_CIV_TAMILS_MYSORE"
			
		if iEra >= iMedieval:
			return "TXT_KEY_CIV_TAMILS_VIJAYANAGARA"
			
	elif iCiv == iCivEthiopia:
		if not game.isReligionFounded(iIslam):
			return "TXT_KEY_CIV_ETHIOPIA_AKSUM"
			
	elif iCiv == iCivKorea:
		if iEra == iClassical:
			if bEmpire:
				return "TXT_KEY_CIV_KOREA_GOGURYEO"
				
		if iEra <= iMedieval:
			return "TXT_KEY_CIV_KOREA_GORYEO"
			
		return "TXT_KEY_CIV_KOREA_JOSEON"
		
	elif iCiv == iCivByzantium:
		if iReligion == iIslam:
			return "TXT_KEY_CIV_BYZANTIUM_RUM"
	
		if not bEmpire:
			if isCapital(iPlayer, ["Dyrrachion"]):
				return "TXT_KEY_CIV_BYZANTIUM_EPIRUS"
			
			if isCapital(iPlayer, ["Athena"]):
				return "TXT_KEY_CIV_BYZANTIUM_MOREA"
	
			if not isCapital(iPlayer, ["Konstantinoupolis"]):
				return capitalName(iPlayer)
			
	elif iCiv == iCivVikings:	
		if bEmpire:
			if not isCapital(iPlayer, ["Stockholm", "Kalmar"]) or iEra > iRenaissance:
				return "TXT_KEY_CIV_VIKINGS_DENMARK_NORWAY"
	
		if isCapital(iPlayer, ["Oslo", "Nidaros"]):
			return "TXT_KEY_CIV_VIKINGS_NORWAY"
			
		if isCapital(iPlayer, ["Stockholm", "Kalmar"]):
			return "TXT_KEY_CIV_VIKINGS_SWEDEN"
			
		if isCapital(iPlayer, ["Roskilde"]):
			return "TXT_KEY_CIV_VIKINGS_DENMARK"
			
		return "TXT_KEY_CIV_VIKINGS_SCANDINAVIA"
		
	elif iCiv == iCivTurks:
		if capital in plots.start(tKhazariaTL).end(tKhazariaBR):
			return "TXT_KEY_CIV_TURKS_KHAZARIA"
	
		if capital in plots.start(tAnatoliaTL).end(tAnatoliaBR):
			return "TXT_KEY_CIV_TURKS_RUM"
			
		if iEra >= iRenaissance and not tPlayer.isAVassal():
			if bEmpire:
				return "TXT_KEY_CIV_TURKS_UZBEKISTAN"
				
			return capitalName(iPlayer)
		
	elif iCiv == iCivArabia:
		if bResurrected:
			return "TXT_KEY_CIV_ARABIA_SAUDI"
			
	elif iCiv == iCivKhmer:
		if isCapital(iPlayer, ["Pagan"]):
			return "TXT_KEY_CIV_KHMER_BURMA"
			
		if isCapital(iPlayer, ["Dali"]):
			return "TXT_KEY_CIV_KHMER_NANZHAO"
			
	elif iCiv == iCivIndonesia:
		if iReligion == iIslam:
			return "TXT_KEY_CIV_INDONESIA_MATARAM"
			
		if iEra <= iRenaissance:
			if bEmpire:
				return "TXT_KEY_CIV_INDONESIA_MAJAPAHIT"
				
			return "TXT_KEY_CIV_INDONESIA_SRIVIJAYA"
			
	elif iCiv == iCivMoors:	
		if capital in plots.rectangle(vic.tIberiaTL, vic.tIberiaBR):
			return capitalName(iPlayer)
			
		return "TXT_KEY_CIV_MOORS_MOROCCO"
		
	elif iCiv == iCivSpain:
		if iReligion == iIslam:
			return "TXT_KEY_CIV_SPAIN_AL_ANDALUS"
	
		bSpain = not player(iCivMoors).isAlive() or not player(iCivMoors).getCapitalCity() in plots.start(vic.tIberiaTL).end(vic.tIberiaBR)
	
		if bSpain:
			if not player(iCivPortugal).isAlive() or not player(iCivPortugal).getCapitalCity() in plots.start(vic.tIberiaTL).end(vic.tIberiaBR):
				return "TXT_KEY_CIV_SPAIN_IBERIA"
			
		if isCapital(iPlayer, ["Barcelona", "Valencia"]):
			return "TXT_KEY_CIV_SPAIN_ARAGON"
			
		if not bSpain:
			return "TXT_KEY_CIV_SPAIN_CASTILE"
			
	elif iCiv == iCivFrance:
		if iEra == iMedieval and not player(iCivHolyRome).isAlive():
			return "TXT_KEY_CIV_FRANCE_FRANCIA"
			
	elif iCiv == iCivEngland:
		if getColumn(iPlayer) >= 11 and cities.start(tBritainTL).end(tBritainBR).owner(iPlayer) >= 3:
			return "TXT_KEY_CIV_ENGLAND_GREAT_BRITAIN"
			
	elif iCiv == iCivHolyRome:
		if isCapital(iPlayer, ["Buda"]):
			return "TXT_KEY_CIV_HOLY_ROME_HUNGARY"
	
		if not bEmpire:
			if year() < year(dBirth[iCivGermany]):
				return "TXT_KEY_CIV_HOLY_ROME_GERMANY"
			else:
				return "TXT_KEY_CIV_AUSTRIA_SHORT_DESC"
			
	elif iCiv == iCivRussia:
		if not (bEmpire and iEra >= iRenaissance) and not isAreaControlled(iPlayer, tEuropeanRussiaTL, tEuropeanRussiaBR, 5, lEuropeanRussiaExceptions):
			if not bCityStates and isCapital(iPlayer, ["Moskva"]):
				return "TXT_KEY_CIV_RUSSIA_MUSCOVY"
				
			return capitalName(iPlayer)
			
	elif iCiv == iCivInca:
		if bResurrected:
			if isCapital(iPlayer, ["La Paz"]):
				return "TXT_KEY_CIV_INCA_BOLIVIA"
				
		else:
			if not bEmpire:
				return capitalName(iPlayer)
			
	elif iCiv == iCivItaly:
		if not bResurrected and not bEmpire and not bCityStates:
			if isCapital(iPlayer, ["Fiorenza"]):
				return "TXT_KEY_CIV_ITALY_TUSCANY"
				
			return capitalName(iPlayer)
			
	elif iCiv == iCivThailand:
		if iEra <= iRenaissance:
			return "TXT_KEY_CIV_THAILAND_AYUTTHAYA"
			
	elif iCiv == iCivNetherlands:
		if bCityStates:
			return short(iPlayer)
			
		if isCapital(iPlayer, ["Brussels", "Antwerpen"]):
			return "TXT_KEY_CIV_NETHERLANDS_BELGIUM"
			
	elif iCiv == iCivGermany:
		if getColumn(iPlayer) <= 14 and pPlayer.isAlive() and (not player(iCivHolyRome).isAlive() or not team(iCivHolyRome).isVassal(iPlayer)):
			return "TXT_KEY_CIV_GERMANY_PRUSSIA"
	
def adjective(iPlayer, bIgnoreVassal = False):
	iCiv = civ(iPlayer)

	if isCapitulated(iPlayer):
		iMaster = getMaster(iPlayer)
	
		sForeignAdjective = dForeignAdjectives[civ(iMaster)].get(iPlayer)
		if sForeignAdjective: return sForeignAdjective
		
		if not bIgnoreVassal: return player(iMaster).getCivilizationAdjective(0)
		
	if isCommunist(iPlayer) or isFascist(iPlayer) or isRepublic(iPlayer):
		sRepublicAdjective = republicAdjective(iPlayer)
		if sRepublicAdjective: return sRepublicAdjective
		
	sSpecificAdjective = specificAdjective(iPlayer)
	if sSpecificAdjective: return sSpecificAdjective
	
	sDefaultInsertAdjective = dDefaultInsertAdjectives.get(iCiv)
	if sDefaultInsertAdjective: return sDefaultInsertAdjective
	
	return player(iPlayer).getCivilizationAdjective(0)
	
def republicAdjective(iPlayer):
	iCiv = civ(iPlayer)

	if iCiv == iCivRome:
		if player(iCivByzantium).isAlive(): return None

	if iCiv == iCivByzantium:
		if player(iCivRome).isAlive(): return None
		
	if iCiv in [iCivMoors, iCivEngland]: return None
	
	if iCiv == iCivInca and data.players[iPlayer].iResurrections > 0: return None
		
	return player(iPlayer).getCivilizationAdjective(0)
	
def specificAdjective(iPlayer):
	pPlayer = player(iPlayer)
	tPlayer = team(iPlayer)
	iCiv = civ(iPlayer)
	
	iCivicGovernment, iCivicLegitimacy, iCivicSociety, iCivicEconomy, iCivicReligion, iCivicTerritory = getCivics(iPlayer)
	
	iNumCities = pPlayer.getNumCities()
	if iNumCities == 0: return player(iPlayer).getCivilizationAdjective(0)
	
	bReborn = pPlayer.isReborn()
	iReligion = pPlayer.getStateReligion()
	capital = player(iPlayer).getCapitalCity()
	tCapitalCoords = capitalCoords(iPlayer)
	bAnarchy = pPlayer.isAnarchy()
	bEmpire = isEmpire(iPlayer)
	bCityStates = isCityStates(iPlayer)
	bTheocracy = (iCivicReligion == iTheocracy)
	bResurrected = data.players[iPlayer].iResurrections > 0
	bCapitulated = isCapitulated(iPlayer)
	iAnarchyTurns = data.players[iPlayer].iAnarchyTurns
	iEra = pPlayer.getCurrentEra()
	iGameEra = game.getCurrentEra()
	bWar = isAtWar(iPlayer)
	
	bMonarchy = not isCommunist(iPlayer) and not isFascist(iPlayer) and not isRepublic(iPlayer)
	
	if iCiv == iCivEgypt:
		if bMonarchy:
			if bResurrected:
				if tPlayer.isHasTech(iGunpowder):
					return "TXT_KEY_CIV_EGYPT_MAMLUK"
		
				if player(iCivArabia).isAlive():
					return "TXT_KEY_CIV_EGYPT_FATIMID"
			
				return "TXT_KEY_CIV_EGYPT_AYYUBID"
			
	elif iCiv == iCivIndia:
		if bMonarchy and not bCityStates:
			if iEra >= iRenaissance:
				return "TXT_KEY_CIV_INDIA_MARATHA"
			
			if iEra >= iMedieval:
				return "TXT_KEY_CIV_INDIA_PALA"
			
			if iReligion == iBuddhism:
				return "TXT_KEY_CIV_INDIA_MAURYA"
			
			if iReligion == iHinduism:
				return "TXT_KEY_CIV_INDIA_GUPTA"
			
	elif iCiv == iCivChina:
		if bMonarchy:
			if iEra >= iMedieval:
				if tPlayer.isHasTech(iPaper) and tPlayer.isHasTech(iGunpowder):
					return "TXT_KEY_CIV_CHINA_SONG"
			
				if year() >= year(600):
					return "TXT_KEY_CIV_CHINA_TANG"
				
				return "TXT_KEY_CIV_CHINA_SUI"
			
			if iEra == iClassical:
				if year() >= year(0):
					return "TXT_KEY_CIV_CHINA_HAN"
				
				return "TXT_KEY_CIV_CHINA_QIN"
			
			return "TXT_KEY_CIV_CHINA_ZHOU"
			
	elif iCiv == iCivBabylonia:
		if bCityStates and not bEmpire:
			return "TXT_KEY_CIV_BABYLONIA_MESOPOTAMIAN"
			
		if isCapital(iPlayer, ["Ninua", "Kalhu"]):
			return "TXT_KEY_CIV_BABYLONIA_ASSYRIAN"
			
	elif iCiv == iCivGreece:
		if not bCityStates and bEmpire and iEra <= iClassical:
			return "TXT_KEY_CIV_GREECE_MACEDONIAN"
			
	elif iCiv == iCivIran:
		if bEmpire:
			if iEra <= iRenaissance:
				return "TXT_KEY_CIV_PERSIA_SAFAVID"
		
			if iEra == iIndustrial:
				return "TXT_KEY_CIV_PERSIA_QAJAR"
		
			return "TXT_KEY_CIV_PERSIA_PAHLAVI"
		
	elif iCiv == iCivPersia:
		if pPlayer.isStateReligion() and iReligion < 0:
			return "TXT_KEY_CIV_PERSIA_MEDIAN"
	
		if bEmpire:
			if bResurrected:
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
				
	elif iCiv == iCivPolynesia:
		if isCapital(iPlayer, ["Manu'a"]):
			return "TXT_KEY_CIV_POLYNESIA_TUI_MANUA"
			
		return "TXT_KEY_CIV_POLYNESIA_TUI_TONGA"
		
	elif iCiv == iCivRome:
		if player(iCivByzantium).isAlive():
			return "TXT_KEY_CIV_ROME_WESTERN"
			
	elif iCiv == iCivTamils:
		if iReligion == iIslam:
			if iEra in [iMedieval, iRenaissance]:
				return "TXT_KEY_CIV_TAMILS_BAHMANI"
	
		if iEra <= iClassical:
			if isCapital(iPlayer, ["Madurai", "Thiruvananthapuram"]):
				return "TXT_KEY_CIV_TAMILS_PANDYAN"
				
			if isCapital(iPlayer, ["Cochin", "Kozhikode"]):
				return "TXT_KEY_CIV_TAMILS_CHERA"
				
			return "TXT_KEY_CIV_TAMILS_CHOLA"
			
	elif iCiv == iCivEthiopia:
		if iReligion == iIslam:
			return "TXT_KEY_CIV_ETHIOPIA_ADAL"
			
		if not game.isReligionFounded(iIslam):
			return "TXT_KEY_CIV_ETHIOPIA_AKSUMITE"
			
	elif iCiv == iCivByzantium:
		if player(iCivRome).isAlive() and player(iCivRome).getNumCities() > 0:
			return "TXT_KEY_CIV_BYZANTIUM_EASTERN"
			
		if bEmpire and controlsCity(iPlayer, Areas.getCapital(iCivRome)):
			return infos.civ(iCivRome).getAdjective(0) # TODO: can be improved by using Core.adjective
			
	elif iCiv == iCivVikings:
		if bEmpire:
			return "TXT_KEY_CIV_VIKINGS_SWEDISH"
			
	elif iCiv == iCivTurks:
		if bResurrected:
			return "TXT_KEY_CIV_TURKS_TIMURID"
	
		if capital in plots.start(tKhazariaTL).end(tKhazariaBR):
			return "TXT_KEY_CIV_TURKS_KHAZAR"
			
		if isAreaControlled(iPlayer, Areas.dCoreArea[iCivPersia][0], Areas.dCoreArea[iCivPersia][1]):
			return "TXT_KEY_CIV_TURKS_SELJUK"
		
		if capital in plots.rectangle(Areas.dCoreArea[iCivPersia]):
			return "TXT_KEY_CIV_TURKS_SELJUK"
		
		if capital in plots.start(tAnatoliaTL).end(tAnatoliaBR):
			return "TXT_KEY_CIV_TURKS_SELJUK"
			
		if iEra >= iRenaissance:
			if bEmpire:
				return "TXT_KEY_CIV_TURKS_SHAYBANID"
		
			return "TXT_KEY_CIV_TURKS_UZBEK"
		
		if cities.owner(iPlayer).all(lambda city: city.getX() < iTurkicEastWestBorder):
			return "TXT_KEY_CIV_TURKS_WESTERN_TURKIC"
		
		if cities.owner(iPlayer).all(lambda city: city.getY() >= iTurkicEastWestBorder):
			return "TXT_KEY_CIV_TURKS_EASTERN_TURKIC"
			
	elif iCiv == iCivArabia:
		if (bTheocracy or controlsHolyCity(iPlayer, iIslam)) and iReligion == iIslam:
			if not bEmpire:
				return "TXT_KEY_CIV_ARABIA_RASHIDUN"
				
			if isCapital(iPlayer, ["Dimashq"]):
				return "TXT_KEY_CIV_ARABIA_UMMAYAD"
				
			return "TXT_KEY_CIV_ARABIA_ABBASID"
			
	elif iCiv == iCivMoors:
		if bEmpire and iEra <= iRenaissance:
			return "TXT_KEY_CIV_MOORS_ALMOHAD"
			
		if not capital in plots.start(vic.tIberiaTL).end(vic.tIberiaBR):
			return "TXT_KEY_CIV_MOORS_MOROCCAN"
			
	elif iCiv == iCivSpain:
		bSpain = not player(iCivMoors).isAlive() or not player(iCivMoors).getCapitalCity() in plots.start(vic.tIberiaTL).end(vic.tIberiaBR)
	
		if bSpain:
			if not player(iCivPortugal).isAlive() or getMaster(iCivPortugal) == iPlayer or not player(iCivPortugal).getCapitalCity() in plots.start(vic.tIberiaTL).end(vic.tIberiaBR):
				return "TXT_KEY_CIV_SPAIN_IBERIAN"
			
		if isCapital(iPlayer, ["Barcelona", "Valencia"]):
			return "TXT_KEY_CIV_SPAIN_ARAGONESE"
			
		if not bSpain:
			return "TXT_KEY_CIV_SPAIN_CASTILIAN"
			
	elif iCiv == iCivFrance:
		if iEra == iMedieval and not player(iCivHolyRome).isAlive():
			return "TXT_KEY_CIV_FRANCE_FRANKISH"
			
	elif iCiv == iCivEngland:
		if getColumn(iPlayer) >= 11 and cities.start(tBritainTL).end(tBritainBR).owner(iPlayer) >= 3:
			return "TXT_KEY_CIV_ENGLAND_BRITISH"
			
	elif iCiv == iCivHolyRome:
		if isCapital(iPlayer, ["Buda"]):
			return "TXT_KEY_CIV_HOLY_ROME_HUNGARIAN"
	
		if player(iCivGermany).isAlive() and iCivicLegitimacy == iConstitution:
			return "TXT_KEY_CIV_HOLY_ROME_AUSTRO_HUNGARIAN"
			
		iVassals = 0
		for iLoopCiv in dCivGroups[iCivGroupEurope]:
			iLoopPlayer = slot(iLoopCiv)
			if iLoopPlayer >= 0 and getMaster(iLoopPlayer) == iPlayer:
				iVassals += 1
				
		if iVassals >= 2:
			return "TXT_KEY_CIV_HOLY_ROME_HABSBURG"
			
		if not bEmpire and year() < year(dBirth[iCivGermany]):
			return "TXT_KEY_CIV_HOLY_ROME_GERMAN"
			
	elif iCiv == iCivInca:
		if bResurrected:
			if isCapital(iPlayer, ["La Paz"]):
				return "TXT_KEY_CIV_INCA_BOLIVIAN"
				
	elif iCiv == iCivItaly:
		if bCityStates and bWar:
			if not bEmpire:
				return "TXT_KEY_CIV_ITALY_LOMBARD"
				
	elif iCiv == iCivMongols:
		if not bEmpire and iEra <= iRenaissance:
			if capital.getRegionID() == rChina:
				return "TXT_KEY_CIV_MONGOLIA_YUAN"
				
			if capital.getRegionID() == rPersia:
				return "TXT_KEY_CIV_MONGOLIA_HULAGU"
				
			if capital.getRegionID() == rCentralAsia:
				return "TXT_KEY_CIV_MONGOLIA_CHAGATAI"
				
		if bMonarchy:
			return "TXT_KEY_CIV_MONGOLIA_MONGOL"
				
	elif iCiv == iCivOttomans:
		return "TXT_KEY_CIV_OTTOMANS_OTTOMAN"
			
	elif iCiv == iCivNetherlands:
		if isCapital(iPlayer, ["Brussels", "Antwerpen"]):
			return "TXT_KEY_CIV_NETHERLANDS_BELGIAN"
			
	elif iCiv == iCivGermany:
		if getColumn(iPlayer) <= 14 and player(iCivHolyRome).isAlive() and not team(iCivHolyRome).isVassal(iPlayer):
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
	iMasterCiv = civ(iMaster)
	iCiv = civ(iPlayer)

	if isCommunist(iMaster):
		sCommunistTitle = dCommunistVassalTitles[iMasterCiv].get(iCiv)
		if sCommunistTitle: return sCommunistTitle
		
		sCommunistTitle = dCommunistVassalTitlesGeneric.get(iMasterCiv)
		if sCommunistTitle: return sCommunistTitle
		
	if isFascist(iMaster):
		sFascistTitle = dFascistVassalTitles[iMasterCiv].get(iCiv)
		if sFascistTitle: return sFascistTitle
		
		sFascistTitle = dFascistVassalTitlesGeneric.get(iMasterCiv)
		if sFascistTitle: return sFascistTitle
				
	if player(iMaster).getPeriod == iPeriodAustria and iCiv == iCivPoland:
		return "TXT_KEY_CIV_AUSTRIAN_POLAND"
		
	if iMasterCiv == iCivEngland and iCiv == iCivMughals:
		if not player(iCivIndia).isAlive():
			return dSpecificVassalTitles[iCivEngland][iCivIndia]

	sSpecificTitle = dSpecificVassalTitles[iMasterCiv].get(iCiv)
	if sSpecificTitle: return sSpecificTitle

	sMasterTitle = dMasterTitles.get(iMasterCiv)
	if sMasterTitle: return sMasterTitle
		
	if iCiv in lColonies:
		return "TXT_KEY_COLONY_OF"
	
	return "TXT_KEY_PROTECTORATE_OF"
	
def communistTitle(iPlayer):
	iCiv = civ(iPlayer)

	if iCiv in lSocialistRepublicOf: return "TXT_KEY_SOCIALIST_REPUBLIC_OF"
	if iCiv in lSocialistRepublicAdj: return "TXT_KEY_SOCIALIST_REPUBLIC_ADJECTIVE"
	if iCiv in lPeoplesRepublicOf: return "TXT_KEY_PEOPLES_REPUBLIC_OF"
	if iCiv in lPeoplesRepublicAdj: return "TXT_KEY_PEOPLES_REPUBLIC_ADJECTIVE"

	return key(iPlayer, "COMMUNIST")
	
def fascistTitle(iPlayer):
	return key(iPlayer, "FASCIST")
	
def republicTitle(iPlayer):
	iCiv = civ(iPlayer)
	pPlayer = player(iPlayer)

	if iCiv == iCivHolyRome:
		return "TXT_KEY_REPUBLIC_ADJECTIVE"
	
	if iCiv == iCivPoland:
		if pPlayer.getCurrentEra() <= iIndustrial:
			return key(iPlayer, "COMMONWEALTH")
	
	if iCiv == iCivEngland:
		iEra = pPlayer.getCurrentEra()
		if isEmpire(iPlayer) and iEra == iIndustrial:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if iEra >= iGlobal:
			return "TXT_KEY_CIV_ENGLAND_UNITED_REPUBLIC"
	
	if iCiv == iCivAmerica:
		_, _, iCivicSociety, _, _, _ = getCivics(iPlayer)
		if iCivicSociety in [iManorialism, iSlavery]:
			return key(iPlayer, "CSA")
			
	if iCiv == iCivColombia:
		if isRegionControlled(iPlayer, rPeru) and isAreaControlled(iPlayer, tColombiaTL, tColombiaBR):
			return "TXT_KEY_CIV_COLOMBIA_FEDERATION_ANDES"
			
	if pPlayer.getStateReligion() == iIslam:
		if iCiv in lIslamicRepublicOf: return "TXT_KEY_ISLAMIC_REPUBLIC_OF"

		if iCiv == iCivOttomans: return key(iPlayer, "ISLAMIC_REPUBLIC")
		
	if iCiv in lRepublicOf: return "TXT_KEY_REPUBLIC_OF"
	if iCiv in lRepublicAdj: return "TXT_KEY_REPUBLIC_ADJECTIVE"
	
	return key(iPlayer, "REPUBLIC")

def defaultTitle(iPlayer):
	return desc(iPlayer, key(iPlayer, "DEFAULT"))
	
def specificTitle(iPlayer, lPreviousOwners=[]):
	pPlayer = player(iPlayer)
	tPlayer = team(iPlayer)
	iCiv = civ(iPlayer)
	
	iCivicGovernment, iCivicLegitimacy, iCivicSociety, iCivicEconomy, iCivicReligion, iCivicTerritory = getCivics(iPlayer)
	
	iNumCities = pPlayer.getNumCities()
	if iNumCities == 0: return defaultTitle(iPlayer)
	
	bReborn = pPlayer.isReborn()
	iReligion = pPlayer.getStateReligion()
	capital = player(iPlayer).getCapitalCity()
	tCapitalCoords = capitalCoords(iPlayer)
	bAnarchy = pPlayer.isAnarchy()
	bEmpire = isEmpire(iPlayer)
	bCityStates = isCityStates(iPlayer)
	bTheocracy = (iCivicReligion == iTheocracy)
	bResurrected = data.players[iPlayer].iResurrections > 0
	bCapitulated = isCapitulated(iPlayer)
	iAnarchyTurns = data.players[iPlayer].iAnarchyTurns
	iEra = pPlayer.getCurrentEra()
	iGameEra = game.getCurrentEra()
	bWar = isAtWar(iPlayer)

	if iCiv == iCivEgypt:
		if bResurrected or scenario() >= i600AD:
			if iReligion == iIslam:
				if bTheocracy: return "TXT_KEY_CALIPHATE_ADJECTIVE"
				return "TXT_KEY_SULTANATE_ADJECTIVE"
			return "TXT_KEY_KINGDOM_ADJECTIVE"
			
		if slot(iCivGreece) in lPreviousOwners:
			return "TXT_KEY_CIV_EGYPT_PTOLEMAIC"
			
		if bCityStates:
			return "TXT_KEY_CITY_STATES_ADJECTIVE"
				
		if iEra == iAncient:
			if iAnarchyTurns == 0: return "TXT_KEY_CIV_EGYPT_OLD_KINGDOM"
			if iAnarchyTurns == turns(1): return "TXT_KEY_CIV_EGYPT_MIDDLE_KINGDOM"
			return "TXT_KEY_CIV_EGYPT_NEW_KINGDOM"
		
		if iEra == iClassical:
			return "TXT_KEY_CIV_EGYPT_NEW_KINGDOM"
			
	elif iCiv == iCivIndia:
		if iReligion == iIslam:
			return "TXT_KEY_SULTANATE_OF"
			
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if iEra >= iRenaissance:
			return "TXT_KEY_CONFEDERACY_ADJECTIVE"
			
		if bCityStates:
			return "TXT_KEY_CIV_INDIA_MAHAJANAPADAS"
			
	elif iCiv == iCivChina:
		if bEmpire:
			if iEra >= iIndustrial or scenario() == i1700AD:
				return "TXT_KEY_EMPIRE_OF"
			
			if iEra == iRenaissance and year() >= year(1400):
				return "TXT_KEY_EMPIRE_OF"
				
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iCivBabylonia:
		if bCityStates and not bEmpire:
			return "TXT_KEY_CITY_STATES_ADJECTIVE"
			
		if bEmpire and iEra > iAncient:
			return "TXT_KEY_CIV_BABYLONIA_NEO_EMPIRE"
			
	elif iCiv == iCivGreece:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
	
		if bCityStates:				
			if bWar:
				return "TXT_KEY_CIV_GREECE_LEAGUE"
				
			return "TXT_KEY_CITY_STATES_ADJECTIVE"
			
	elif iCiv == iCivPersia:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iCivPhoenicia:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if bCityStates:
			return "TXT_KEY_CITY_STATES_ADJECTIVE"
			
	elif iCiv == iCivPolynesia:
		if isCapital(iPlayer, ["Kaua'i", "O'ahu", "Maui"]):
			return "TXT_KEY_KINGDOM_OF"
			
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iCivRome:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if bCityStates:
			return "TXT_KEY_REPUBLIC_ADJECTIVE"
			
	elif iCiv == iCivColombia:
		if bEmpire:
			if isRegionControlled(iPlayer, rPeru) and isAreaControlled(iPlayer, tColombiaTL, tColombiaBR):
				return "TXT_KEY_CIV_COLOMBIA_EMPIRE_ANDES"
		
			return "TXT_KEY_CIV_COLOMBIA_EMPIRE"
			
	elif iCiv == iCivJapan:
		if bEmpire:
			return "TXT_KEY_EMPIRE_OF"
			
		if iCivicLegitimacy == iCentralism:
			return "TXT_KEY_EMPIRE_OF"
			
		if iEra >= iIndustrial:
			return "TXT_KEY_EMPIRE_OF"
			
	elif iCiv == iCivTamils:
		if iReligion == iIslam:
			return "TXT_KEY_SULTANATE_ADJECTIVE"
	
		if iEra >= iMedieval:
			return "TXT_KEY_KINGDOM_OF"
		
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iCivEthiopia:
		if bCityStates:
			return "TXT_KEY_CITY_STATES_ADJECTIVE"
	
		if iReligion == iIslam:
			return "TXT_KEY_SULTANATE_ADJECTIVE"
	
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
	
	elif iCiv == iCivKorea:
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
			
	elif iCiv == iCivByzantium:
		if iReligion == iIslam:
			return "TXT_KEY_SULTANATE_OF"
			
		if tCapitalCoords != Areas.getCapital(iCiv):
			if capital.getRegionID() == rAnatolia:
				return "TXT_KEY_EMPIRE_OF"
				
			return "TXT_KEY_CIV_BYZANTIUM_DESPOTATE"
			
	elif iCiv == iCivVikings:
		if bCityStates:
			return "TXT_KEY_CIV_VIKINGS_ALTHINGS"
			
		if isAreaControlled(iPlayer, tBritainTL, tBritainBR):
			return "TXT_KEY_CIV_VIKINGS_NORTH_SEA_EMPIRE"
				
		if iReligion < 0 and iEra < iRenaissance:
			return "TXT_KEY_CIV_VIKINGS_NORSE_KINGDOMS"
			
		if bEmpire:
			if iEra <= iMedieval:
				return "TXT_KEY_CIV_VIKINGS_KALMAR_UNION"
				
			if iEra == iRenaissance or isCapital(iPlayer, ["Stockholm"]):
				return "TXT_KEY_EMPIRE_ADJECTIVE"
				
	elif iCiv == iCivTurks:
		if bCityStates or iCivicGovernment == iElective:
			return "TXT_KEY_CIV_TURKS_KURULTAI"
			
		if iReligion >= 0:
			if bEmpire:
				if isAreaControlled(iPlayer, Areas.dCoreArea[iCivPersia][0], Areas.dCoreArea[iCivPersia][1]) and not bResurrected:
					return "TXT_KEY_CIV_TURKS_GREAT_EMPIRE"
			
				return "TXT_KEY_EMPIRE_ADJECTIVE"
				
			if not isAreaControlled(iPlayer, Areas.dCoreArea[iCivPersia][0], Areas.dCoreArea[iCivPersia][1]):
				return "TXT_KEY_CIV_TURKS_KHANATE_OF"
				
			if iReligion == iIslam:
				if isAreaControlled(iPlayer, Areas.dCoreArea[iCivPersia][0], Areas.dCoreArea[iCivPersia][1]):
					return "TXT_KEY_SULTANATE_ADJECTIVE"
			
				return "TXT_KEY_SULTANATE_OF"
				
			return "TXT_KEY_KINGDOM_OF"
			
		if bEmpire:
			return "TXT_KEY_CIV_TURKS_KHAGANATE"
			
	elif iCiv == iCivArabia:
		if bResurrected:
			return "TXT_KEY_KINGDOM_OF"
			
		if iReligion == iIslam and (bTheocracy or controlsHolyCity(iPlayer, iIslam)):
			return "TXT_KEY_CALIPHATE_ADJECTIVE"
			
	elif iCiv == iCivTibet:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iCivKhmer:
		if iEra <= iRenaissance and isCapital(iPlayer, ["Angkor"]):
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if isCapital(iPlayer, ["Hanoi"]):
			return "TXT_KEY_CIV_KHMER_DAI_VIET"
			
	elif iCiv == iCivIndonesia:
		if iReligion == iIslam:
			return "TXT_KEY_SULTANATE_OF"
			
	elif iCiv == iCivMoors:
		if bCityStates:
			return "TXT_KEY_CIV_MOORS_TAIFAS"
			
		if iReligion == iIslam and capital in plots.start(vic.tIberiaTL).end(vic.tIberiaBR):
			if bEmpire:
				return "TXT_KEY_CALIPHATE_OF"
				
			return "TXT_KEY_CIV_MOORS_EMIRATE_OF"
			
		if bEmpire and iEra <= iRenaissance:
			if iReligion == iIslam and bTheocracy:
				return "TXT_KEY_CALIPHATE_ADJECTIVE"
				
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iCivSpain:
		if iReligion == iIslam:
			return "TXT_KEY_SULTANATE_OF"
			
		if bEmpire and iEra > iMedieval:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if iEra == iMedieval and isCapital(iPlayer, ["Barcelona", "Valencia"]):
			return "TXT_KEY_CIV_SPAIN_CROWN_OF"
			
	elif iCiv == iCivFrance:
		if not tCapitalCoords in Areas.getNormalArea(iCivFrance):
			return "TXT_KEY_CIV_FRANCE_EXILE"
			
		if iEra >= iIndustrial and bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if iCivicLegitimacy == iRevolutionism:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if not player(iCivHolyRome).isAlive() and iEra == iMedieval:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iCivEngland:
		if tCapitalCoords not in Areas.getCoreArea(iCivEngland):
			return "TXT_KEY_CIV_ENGLAND_EXILE"
			
		if iEra == iMedieval and player(iCivFrance).isAlive() and team(iCivFrance).isAVassal() and civ(getMaster(iCivFrance)) == iCivEngland:
			return "TXT_KEY_CIV_ENGLAND_ANGEVIN_EMPIRE"
			
		if getColumn(iPlayer) >= 11:
			if bEmpire:
				return "TXT_KEY_EMPIRE_ADJECTIVE"
		
			if cities.start(tBritainTL).end(tBritainBR).owner(iPlayer) >= 3:
				return "TXT_KEY_CIV_ENGLAND_UNITED_KINGDOM_OF"
			
	elif iCiv == iCivHolyRome:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if isCapital(iPlayer, ["Buda"]):
			return "TXT_KEY_KINGDOM_OF"
			
		if player(iCivGermany).isAlive():
			return "TXT_KEY_CIV_HOLY_ROME_ARCHDUCHY_OF"
		
	elif iCiv == iCivRussia:
		if bEmpire and iEra >= iRenaissance:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if bCityStates and iEra <= iMedieval:
			if isCapital(iPlayer, ["Kiev"]):
				return "TXT_KEY_CIV_RUSSIA_KIEVAN_RUS"
				
			return "TXT_KEY_CIV_RUSSIA_RUS"
			
		if isAreaControlled(iPlayer, tEuropeanRussiaTL, tEuropeanRussiaBR, 5, lEuropeanRussiaExceptions):
			return "TXT_KEY_CIV_RUSSIA_TSARDOM_OF"

	elif iCiv == iCivNetherlands:
		if bCityStates:
			return "TXT_KEY_CIV_NETHERLANDS_REPUBLIC"
		
		if tCapitalCoords not in Areas.getCoreArea(iCivNetherlands):
			return "TXT_KEY_CIV_NETHERLANDS_EXILE"
			
		if bEmpire:
			if iEra >= iIndustrial:
				return "TXT_KEY_EMPIRE_ADJECTIVE"
				
			return "TXT_KEY_CIV_NETHERLANDS_UNITED_KINGDOM_OF"
			
	# Nothing for Mali
	
	elif iCiv == iCivPoland:
		if iEra >= iRenaissance and bEmpire:
			return "TXT_KEY_CIV_POLAND_COMMONWEALTH"
			
		if isCapital(iPlayer, ["Kowno", "Medvegalis", "Wilno", "Ryga"]):
			return "TXT_KEY_CIV_POLAND_GRAND_DUCHY_OF"
			
	elif iCiv == iCivPortugal:
		if tCapitalCoords in Areas.getCoreArea(iCivBrazil) and not player(iCivBrazil).isAlive():
			return "TXT_KEY_CIV_PORTUGAL_BRAZIL"
			
		if not capital in plots.start(vic.tIberiaTL).end(vic.tIberiaBR):
			return "TXT_KEY_CIV_PORTUGAL_EXILE"
			
		if bEmpire and iEra >= iRenaissance:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iCivInca:
		if not bResurrected:
			if bEmpire:
				return "TXT_KEY_CIV_INCA_FOUR_REGIONS"
				
	elif iCiv == iCivItaly:
		if bCityStates:
			if bWar:
				return "TXT_KEY_CIV_ITALY_LEAGUE"
				
			return "TXT_KEY_CIV_ITALY_MARITIME_REPUBLICS"
			
		if not bResurrected:
			if iReligion == iCatholicism:
				if bTheocracy:
					return "TXT_KEY_CIV_ITALY_PAPAL_STATES"
				
				if isCapital(iPlayer, ["Roma"]):
					return "TXT_KEY_CIV_ITALY_PAPAL_STATES"
					
			if not bEmpire:
				return "TXT_KEY_CIV_ITALY_DUCHY_OF"
				
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iCivMongols:
		if capital.getRegionID() == rPersia:
			return "TXT_KEY_CIV_MONGOLIA_ILKHANATE"
	
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if iEra <= iRenaissance:
			if iNumCities <= 3:
				return "TXT_KEY_CIV_MONGOLIA_KHAMAG"
				
			return "TXT_KEY_CIV_MONGOLIA_KHANATE"
			
	elif iCiv == iCivAztecs:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if bCityStates:
			return "TXT_KEY_CIV_AZTECS_ALTEPETL"
				
	elif iCiv == iCivMughals:
		if bResurrected:
			if bEmpire:
				return "TXT_KEY_EMPIRE_OF"
				
			return "TXT_KEY_SULTANATE_OF"
	
		if iEra == iMedieval and not bEmpire:
			return "TXT_KEY_SULTANATE_OF"
			
	elif iCiv == iCivOttomans:
		if iReligion == iIslam:
			if bTheocracy and game.getHolyCity(iIslam) and game.getHolyCity(iIslam).getOwner() == iPlayer:
				return "TXT_KEY_CALIPHATE_ADJECTIVE"
				
			if bEmpire:
				return "TXT_KEY_EMPIRE_ADJECTIVE"
				
			return "TXT_KEY_SULTANATE_ADJECTIVE"
			
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iCivThailand:
		if iEra >= iIndustrial and bEmpire:
			return "TXT_KEY_EMPIRE_OF"
			
	elif iCiv == iCivGermany:
		if iEra >= iIndustrial and bEmpire:
			if player(iCivHolyRome).isAlive() and team(iCivHolyRome).isAVassal() and civ(getMaster(iCivHolyRome)) == iCivGermany:
				return "TXT_KEY_CIV_GERMANY_GREATER_EMPIRE"
				
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iCivAmerica:
		if iCivicSociety in [iSlavery, iManorialism]:
			if isRegionControlled(iPlayer, rMesoamerica) and isRegionControlled(iPlayer, rCaribbean):
				return "TXT_KEY_CIV_AMERICA_GOLDEN_CIRCLE"
		
			return "TXT_KEY_CIV_AMERICA_CSA"
			
	elif iCiv == iCivArgentina:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if tCapitalCoords != Areas.getCapital(iCiv):
			return "TXT_KEY_CIV_ARGENTINA_CONFEDERATION"
			
	elif iCiv == iCivBrazil:
		if bEmpire:
			return "TXT_KEY_EMPIRE_OF"
			
	return None
			
### Leader methods ###

def startingLeader(iPlayer):
	iCiv = civ(iPlayer)

	if iCiv in dStartingLeaders[scenario()]: return dStartingLeaders[scenario()][iCiv]
	
	return dStartingLeaders[i3000BC][iCiv]
	
def leader(iPlayer):
	iCiv = civ(iPlayer)

	if is_minor(iPlayer): return None
	
	if not player(iPlayer).isAlive(): return None
	
	if player(iPlayer).isHuman(): return None
	
	pPlayer = player(iPlayer)
	tPlayer = team(iPlayer)
	bReborn = pPlayer.isReborn()
	iReligion = pPlayer.getStateReligion()
	capital = player(iPlayer).getCapitalCity()
	tCapitalCoords = (capital.getX(), capital.getY())
	iCivicGovernment, iCivicLegitimacy, iCivicSociety, iCivicEconomy, iCivicReligion, iCivicTerritory = getCivics(iPlayer)
	bEmpire = isEmpire(iPlayer)
	bCityStates = isCityStates(iPlayer)
	bTheocracy = (iCivicReligion == iTheocracy)
	bResurrected = data.players[iPlayer].iResurrections > 0
	bMonarchy = not (isCommunist(iPlayer) or isFascist(iPlayer) or isRepublic(iPlayer))
	iAnarchyTurns = data.players[iPlayer].iAnarchyTurns
	iEra = pPlayer.getCurrentEra()
	iGameEra = game.getCurrentEra()
	
	if iCiv == iCivEgypt:
		if not bMonarchy and iEra >= iGlobal: return iNasser
		
		if bResurrected or scenario() >= i600AD: return iBaibars
		
		if getColumn(iPlayer) >= 4: return iCleopatra
		
	elif iCiv == iCivIndia:
		if not bMonarchy and iEra >= iGlobal: return iGandhi
		
		if iEra >= iRenaissance: return iShahuji
		
		if getColumn(iPlayer) >= 5: return iChandragupta
		
	elif iCiv == iCivChina:
		if isCommunist(iPlayer) or isRepublic(iPlayer) and iEra >= iIndustrial: return iMao
			
		if iEra >= iRenaissance and year() >= year(1400): return iHongwu
	
		if bResurrected: return iHongwu
		
		if scenario() >= i1700AD: return iHongwu
		
		if iEra >= iMedieval: return iTaizong
		
	elif iCiv == iCivBabylonia:
		if year() >= year(-1600): return iHammurabi
		
	elif iCiv == iCivGreece:
		if iEra >= iIndustrial: return iGeorge
		
		if bResurrected and getColumn(iPlayer) >= 11: return iGeorge
	
		if bEmpire: return iAlexanderTheGreat
		
		if not bCityStates: return iAlexanderTheGreat
		
	elif iCiv == iCivIran:
		if iEra >= iGlobal: return iKhomeini
		
	elif iCiv == iCivPersia:
		if getColumn(iPlayer) >= 6: return iKhosrow
			
		if bEmpire:
			return iDarius
			
	elif iCiv == iCivPhoenicia:
		if not bCityStates: return iHannibal
		
		if capital.getRegionID() not in [rMesopotamia, rAnatolia]: return iHannibal
		
	elif iCiv == iCivRome:
		if bEmpire or not bCityStates: return iAugustus
		
	elif iCiv == iCivKorea:		
		if iEra >= iRenaissance: return iSejong
		
		if scenario() >= i1700AD: return iSejong
		
	elif iCiv == iCivJapan:
		if iEra >= iIndustrial: return iMeiji
		
		if tPlayer.isHasTech(iFeudalism): return iOdaNobunaga
		
	elif iCiv == iCivEthiopia:
		if iEra >= iIndustrial: return iMenelik
		
		if iEra >= iMedieval: return iZaraYaqob
		
	elif iCiv == iCivTamils:
		if iEra >= iRenaissance: return iKrishnaDevaRaya
		
	elif iCiv == iCivByzantium:
		if year() >= year(1000): return iBasil
		
	elif iCiv == iCivVikings:
		if iEra >= iGlobal: return iGerhardsen
		
		if iEra >= iRenaissance: return iGustav
		
	elif iCiv == iCivTurks:
		if bResurrected or pPlayer.getPeriod() == iPeriodSeljuks: return iTamerlane
	
		if year() >= year(1000): return iAlpArslan
		
	elif iCiv == iCivArabia:
		if year() >= year(1000): return iSaladin
		
	elif iCiv == iCivTibet:
		if year() >= year(1500): return iLobsangGyatso
		
	elif iCiv == iCivIndonesia:
		if iEra >= iGlobal: return iSuharto
		
		if bEmpire: return iHayamWuruk
		
	elif iCiv == iCivMoors:
		if not capital in plots.start(vic.tIberiaTL).end(vic.tIberiaBR): return iYaqub
		
	elif iCiv == iCivSpain:
		if isFascist(iPlayer): return iFranco
		
		if True in data.lFirstContactConquerors: return iPhilip
		
	elif iCiv == iCivFrance:
		if iEra >= iGlobal: return iDeGaulle
		
		if iEra >= iIndustrial: return iNapoleon
		
		if iEra >= iRenaissance: return iLouis
		
	elif iCiv == iCivEngland:
		if iEra >= iGlobal: return iChurchill
		
		if iEra >= iIndustrial: return iVictoria
		
		if scenario() == i1700AD: return iVictoria
		
		if iEra >= iRenaissance: return iElizabeth
		
	elif iCiv == iCivHolyRome:
		if iEra >= iIndustrial: return iFrancis
		
		if scenario() == i1700AD: return iFrancis
		
		if iEra >= iRenaissance: return iCharles
		
	elif iCiv == iCivRussia:
		if iEra >= iIndustrial:
			if not bMonarchy: return iStalin
			
			return iAlexanderII
			
		if iEra >= iRenaissance:
			if year() >= year(1750): return iCatherine
			
			return iPeter
		
	elif iCiv == iCivNetherlands:
		if year() >= year(1650): return iWilliam
			
	elif iCiv == iCivPoland:
		if iEra >= iGlobal: return iWalesa
		
		if isFascist(iPlayer) or isCommunist(iPlayer): return iPilsudski
	
		if iEra >= iRenaissance: return iSobieski
		
		if scenario() == i1700AD: return iSobieski
		
	elif iCiv == iCivPortugal:
		if iEra >= iIndustrial: return iMaria
		
		if tPlayer.isHasTech(iCartography): return iJoao
		
	elif iCiv == iCivInca:
		if iEra >= iIndustrial: return iCastilla
		
		if bResurrected and year() >= year(1600): return iCastilla
	
	elif iCiv == iCivItaly:
		if isFascist(iPlayer): return iMussolini
	
		if iEra >= iIndustrial: return iCavour
		
	elif iCiv == iCivMongols:
		if year() >= year(1400): return iKublaiKhan
		
	elif iCiv == iCivMexico:
		if bMonarchy: return iSantaAnna
		
		if isFascist(iPlayer): return iSantaAnna
		
		if iEra >= iGlobal: return iCardenas
			
	elif iCiv == iCivMughals:
		if iEra >= iGlobal: return iBhutto
	
		if getColumn(iPlayer) >= 9: return iAkbar
		
	elif iCiv == iCivOttomans:
		if not bMonarchy and iEra >= iIndustrial: return iAtaturk
		
		if iEra >= iRenaissance: return iSuleiman
				
	elif iCiv == iCivThailand:
		if iEra >= iIndustrial: return iMongkut

	elif iCiv == iCivGermany:
		if isFascist(iPlayer): return iHitler
		
		if getColumn(iPlayer) >= 14: return iBismarck
		
	elif iCiv == iCivAmerica:
		if iEra >= iGlobal: return iRoosevelt
		
		if year() >= year(1850): return iLincoln
		
	elif iCiv == iCivArgentina:
		if iEra >= iGlobal: return iPeron
	
	elif iCiv == iCivBrazil:
		if iEra >= iGlobal: return iVargas
		
	elif iCiv == iCivCanada:
		if iEra >= iGlobal: return iTrudeau
		
	return startingLeader(iPlayer)
		
	
def leaderName(iPlayer):
	iCiv = civ(iPlayer)
	pPlayer = player(iPlayer)
	iLeader = pPlayer.getLeader()
	
	if iCiv == iCivChina:
		if iLeader == iHongwu:
			if year() >= year(1700):
				return "TXT_KEY_LEADER_KANGXI"
				
	elif iCiv == iCivTamils:
		if iLeader == iKrishnaDevaRaya:
			if year() >= year(1700):
				return "TXT_KEY_LEADER_TIPU_SULTAN"
				
	return None