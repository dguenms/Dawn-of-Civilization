# coding: utf-8

from Core import *
from Files import *

from Events import handler


### CONSTANTS ###

iNumLanguages = 40
(iLangAmerican, iLangArabic, iLangBabylonian, iLangByzantine, iLangCeltic, 
iLangChinese, iLangCongolese, iLangDutch, iLangEgyptian, iLangEgyptianArabic, 
iLangEnglish, iLangEthiopian, iLangFrench, iLangGerman, iLangGreek, 
iLangHittite, iLangIndian, iLangIndonesian, iLangItalian, iLangJapanese, 
iLangKhmer, iLangKorean, iLangLatin, iLangMande, iLangMayan, 
iLangMongolian, iLangNahuatl, iLangNubian, iLangPersian, iLangPhoenician, 
iLangPolish, iLangPolynesian, iLangPortuguese, iLangQuechua, iLangRussian, 
iLangSpanish, iLangThai, iLangTibetan, iLangTurkish, iLangViking) = range(iNumLanguages)

dLanguages = {
	iEgypt:	[iLangEgyptian],
	iBabylonia: [iLangBabylonian],
	iHarappa: [iLangIndian],
	iAssyria: [iLangBabylonian],
	iChina: [iLangChinese],
	iHittites: [iLangHittite, iLangBabylonian],
	iGreece: [iLangGreek],
	iIndia: [iLangIndian],
	iPhoenicia: [iLangPhoenician],
	iNubia: [iLangNubian, iLangEgyptian],
	iPolynesia: [iLangPolynesian],
	iPersia: [iLangPersian],
	iRome: [iLangLatin],
	iMaya: [iLangMayan, iLangNahuatl],
	iTamils: [iLangIndian],
	iEthiopia: [iLangEthiopian],
	iKorea: [iLangKorean, iLangChinese],
	iByzantium: [iLangByzantine],
	iJapan: [iLangJapanese],
	iVikings: [iLangViking],
	iTurks: [iLangTurkish, iLangPersian, iLangArabic],
	iArabia: [iLangArabic],
	iTibet: [iLangTibetan, iLangChinese],
	iKhmer: [iLangKhmer, iLangIndonesian],
	iIndonesia: [iLangIndonesian, iLangKhmer],
	iMoors: [iLangArabic],
	iSpain: [iLangSpanish],
	iFrance: [iLangFrench],
	iEngland: [iLangEnglish],
	iHolyRome: [iLangGerman],
	iRussia: [iLangRussian],
	iMali: [iLangMande],
	iPoland: [iLangPolish, iLangRussian], 
	iPortugal: [iLangPortuguese, iLangSpanish],
	iInca: [iLangQuechua],
	iItaly: [iLangItalian],
	iMongols: [iLangMongolian, iLangTurkish, iLangChinese],
	iAztecs: [iLangNahuatl],
	iMughals: [iLangPersian, iLangArabic, iLangIndian],
	iOttomans: [iLangTurkish, iLangArabic],
	iThailand: [iLangThai, iLangKhmer, iLangIndonesian],
	iCongo: [iLangCongolese],
	iIran: [iLangArabic, iLangPersian],
	iNetherlands: [iLangDutch],
	iGermany: [iLangGerman],
	iAmerica: [iLangAmerican, iLangEnglish],
	iArgentina: [iLangSpanish],
	iMexico: [iLangSpanish],
	iColombia: [iLangSpanish],
	iBrazil: [iLangPortuguese, iLangSpanish],
	iCanada: [iLangAmerican, iLangEnglish, iLangFrench],
	iCelts: [iLangCeltic],
}


### CSV CITY NAME MAP ###

city_names = FileMap("Cities.csv")


### TRANSLATION DICTIONARIES ###

dLanguageNames = {
	iLangAmerican: "American",
	iLangArabic: "Arabic",
	iLangBabylonian: "Babylonian",
	iLangByzantine: "Byzantine",
	iLangCeltic: "Celtic",
	iLangChinese: "Chinese",
	iLangCongolese: "Congolese",
	iLangDutch: "Dutch",
	iLangEgyptian: "Egyptian",
	iLangEgyptianArabic: "EgyptianArabic",
	iLangEnglish: "English",
	iLangEthiopian: "Ethiopian",
	iLangFrench: "French",
	iLangGerman: "German",
	iLangGreek: "Greek",
	iLangHittite: "Hittite",
	iLangIndian: "Indian",
	iLangIndonesian: "Indonesian",
	iLangItalian: "Italian",
	iLangJapanese: "Japanese",
	iLangKhmer: "Khmer",
	iLangKorean: "Korean",
	iLangLatin: "Latin",
	iLangMande: "Mande",
	iLangMayan: "Mayan",
	iLangMongolian: "Mongolian",
	iLangNahuatl: "Nahuatl",
	iLangNubian: "Nubian",
	iLangPersian: "Persian",
	iLangPhoenician: "Phoenician",
	iLangPolish: "Polish",
	iLangPolynesian: "Polynesian",
	iLangPortuguese: "Portuguese",
	iLangQuechua: "Quechua",
	iLangRussian: "Russian",
	iLangSpanish: "Spanish",
	iLangThai: "Thai",
	iLangTibetan: "Tibetan",
	iLangTurkish: "Turkish",
	iLangViking: "Viking",
}

dTranslations = dict((iLanguage, FileDict("Translations/%s.csv" % dLanguageNames[iLanguage])) for iLanguage in range(iNumLanguages))


### EVENT HANDLERS ###

@handler("cityBuilt")
def onCityBuilt(city):
	updateName(city)


@handler("cityAcquired")
def onCityAcquired(iOwner, iNewOwner, city):
	updateName(city)
	
	# how do we handle fallback languages in case the new owner has no translation
	# and potentially keeps a non-local translation in place


@handler("birth")
def onBirth(iPlayer):
	# update some colonial to Mexican city names
	
	pass
	

@handler("periodChange")
def onPeriodChange(iCiv, iPeriod):
	# Prey Nokor becomes Saigon
	
	updateNames(iCiv)


@handler("religionSpread")
def onReligionSpread(iReligion, iPlayer, city):
	# Yogyakarta changes to Mataram with Islam
	# Budapest is renamed to Buddhapest with Buddhism
	
	updateName(city)


@handler("revolution")
def onRevolution(iPlayer):
	# civic names are handled by a different function, not persistence
	
	updateNames(iPlayer)


@handler("greatPersonBorn")
def onGreatPersonBorn(unit, iPlayer):
	# Pitic changes to Hermosillo when a great general is born
	
	updateNames(iPlayer)



### MAIN FUNCTIONS ###

def updateNames(identifier):
	for city in cities.owner(identifier):
		updateName(city)


def updateName(city):
	if is_minor(city):
		return

	iCiv = civ(city)
	name = getName(iCiv, city)
	
	if city.getName() != name:
		city.setName(name, False)


def getName(identifier, tile):
	iCiv = civ(identifier)

	name = city_names[tile]
	
	name = data.dChangedCities.get(name, name)
	name = data.dRenamedCities.get(name, name)
	
	name = getCivicRenames(iCiv).get(name, name)
	
	name = translateName(iCiv, name)
	
	return name


def translateName(iCiv, name):
	for iLanguage in getLanguages(iCiv):
		if name in dTranslations[iLanguage]:
			return dTranslations[iLanguage][name]
		
		if name in dTranslations[iLanguage].values():
			return name
	
	return name


def getLanguages(iCiv):
	return getSpecialLanguages(iCiv) or dLanguages.get(iCiv)


def getSpecialLanguages(iCiv):
	iPlayer = slot(iCiv)
	if iPlayer < 0:
		return None
	
	if iCiv == iEgypt:
		if player(iPlayer).getStateReligion() == iIslam:
			return [iLangEgyptianArabic, iLangArabic]
	
	elif iCiv == iInca:
		if data.civs[iCiv].iResurrections > 0:
			return [iLangSpanish]
	
	return None


def findLocations(name):
	return plots.all().land().where(lambda p: city_names[p] == name)
	
	
def getCivicRenames(iCiv):
	iPlayer = slot(iCiv)
	if iPlayer < 0:
		return {}
	
	return {}


def renameCity(oldName, newName):
	data.dRenamedCities[oldName] = newName
	
	# how do we announce when a city name has changed for someone who owns the city


def moveCity(oldCity, newCity):
	data.dChangedCities[oldCity] = newCity
	
	# how do we announce when a city has moved for someone who owns the city
