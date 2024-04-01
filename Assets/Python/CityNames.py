# coding: utf-8

from Core import *
from Files import *

from Events import handler


### CONSTANTS ###

iNumLanguages = 43
(iLangAmerican, iLangArabic, iLangBabylonian, iLangBurmese, iLangByzantine, 
iLangCeltic, iLangChinese, iLangCongolese, iLangDutch, iLangEgyptian, 
iLangEgyptianArabic, iLangEnglish, iLangEthiopian, iLangFrench, iLangGerman, 
iLangGreek, iLangHittite, iLangIndian, iLangIndonesian, iLangItalian, 
iLangJapanese, iLangKhmer, iLangKorean, iLangLatin, iLangMande, 
iLangMayan, iLangMongolian, iLangNahuatl, iLangNorse, iLangNubian, 
iLangPersian, iLangPhoenician, iLangPolish, iLangPolynesian, iLangPortuguese, 
iLangQuechua, iLangRussian, iLangSpanish, iLangSwedish, iLangThai, 
iLangTibetan, iLangTurkish, iLangVietnamese) = range(iNumLanguages)

dLanguages = CivDict({
	iEgypt:	[iLangEgyptian],
	iBabylonia: [iLangBabylonian],
	iHarappa: [iLangIndian],
	iAssyria: [iLangBabylonian],
	iChina: [iLangChinese],
	iHittites: [iLangHittite, iLangBabylonian],
	iNubia: [iLangNubian, iLangEgyptian],
	iGreece: [iLangGreek],
	iIndia: [iLangIndian],
	iPhoenicia: [iLangPhoenician],
	iPolynesia: [iLangPolynesian],
	iPersia: [iLangPersian],
	iRome: [iLangLatin],
	iCelts: [iLangCeltic],
	iMaya: [iLangMayan, iLangNahuatl],
	iDravidia: [iLangIndian],
	iEthiopia: [iLangEthiopian],
	iToltecs: [iLangNahuatl],
	iKushans: [iLangIndian, iLangGreek, iLangTurkish],
	iKorea: [iLangKorean, iLangChinese],
	iByzantium: [iLangByzantine],
	iMalays: [iLangIndonesian, iLangKhmer],
	iJapan: [iLangJapanese],
	iNorse: [iLangNorse],
	iTurks: [iLangTurkish, iLangPersian, iLangArabic],
	iArabia: [iLangArabic],
	iTibet: [iLangTibetan, iLangChinese],
	iKhmer: [iLangKhmer, iLangIndonesian],
	iMoors: [iLangArabic],
	iJava: [iLangIndonesian, iLangKhmer],
	iSpain: [iLangSpanish],
	iFrance: [iLangFrench],
	iEngland: [iLangEnglish],
	iHolyRome: [iLangGerman],
	iBurma: [iLangBurmese, iLangIndian],
	iVietnam: [iLangVietnamese, iLangChinese],
	iRus: [iLangRussian],
	iSwahili: [iLangArabic],
	iMali: [iLangMande],
	iPoland: [iLangPolish, iLangRussian], 
	iPortugal: [iLangPortuguese, iLangSpanish],
	iInca: [iLangQuechua],
	iItaly: [iLangItalian],
	iMongols: [iLangMongolian, iLangTurkish, iLangChinese],
	iAztecs: [iLangNahuatl],
	iMughals: [iLangPersian, iLangArabic, iLangIndian],
	iThailand: [iLangThai, iLangKhmer, iLangIndonesian],
	iSweden: [iLangSwedish, iLangNorse],
	iRussia: [iLangRussian],
	iOttomans: [iLangTurkish, iLangArabic],
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
}, [])


### CSV CITY NAME MAP ###

city_names = FileMap("Cities.csv")


### TRANSLATION DICTIONARIES ###

dLanguageNames = {
	iLangAmerican: "American",
	iLangArabic: "Arabic",
	iLangBabylonian: "Babylonian",
	iLangBurmese: "Burmese",
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
	iLangNorse: "Norse",
	iLangNubian: "Nubian",
	iLangPersian: "Persian",
	iLangPhoenician: "Phoenician",
	iLangPolish: "Polish",
	iLangPolynesian: "Polynesian",
	iLangPortuguese: "Portuguese",
	iLangQuechua: "Quechua",
	iLangRussian: "Russian",
	iLangSpanish: "Spanish",
	iLangSwedish: "Swedish",
	iLangThai: "Thai",
	iLangTibetan: "Tibetan",
	iLangTurkish: "Turkish",
	iLangVietnamese: "Vietnamese",
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
	if not game.isFinalInitialized():
		return

	if is_minor(city):
		return

	iCiv = civ(city)
	name = getName(iCiv, city)
	
	if name and city.getName() != name:
		city.setName(name, False)


def getName(identifier, tile):
	iCiv = civ(identifier)

	name = city_names[tile]
	
	name = data.dChangedCities.get(name, name)
	name = data.dRenamedCities.get(name, name)
	
	name = getCivicRenames(iCiv).get(name, name)
	
	name = translateName(iCiv, name)
	
	return name


def translateName(identifier, name):
	for iLanguage in getLanguages(identifier):
		if name in dTranslations[iLanguage]:
			return dTranslations[iLanguage][name]
		
		if name in dTranslations[iLanguage].values():
			return name
	
	return name


def getLanguages(identifier):
	return getSpecialLanguages(identifier) or dLanguages[identifier]


def getSpecialLanguages(identifier):
	iCiv = civ(identifier)
	if player(identifier).getID() < 0:
		return None
	
	if iCiv == iEgypt:
		if player(identifier).getStateReligion() == iIslam:
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
