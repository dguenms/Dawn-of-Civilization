# coding: utf-8

from Core import *
from CityNameTranslations import *

from RFCUtils import canEverRespawn
from Files import FileMap
from Events import handler


### CSV CITY NAME MAP ###

city_names = FileMap("Cities.csv")


### CONSTANTS ###

dBaseLanguages = {
	iEgypt: (iEgyptian,),
	iBabylonia: (iBabylonian,),
	iHarappa: (iHarappan, iIndian),
	iAssyria: (iBabylonian,),
	iChina: (iChinese,),
	iHittites: (iHittite,),
	iNubia: (iNubian, iEgyptian,),
	iGreece: (iGreek,),
	iIndia: (iIndian, iDravidian),
	iPhoenicia: (iPhoenician,),
	iPolynesia: (iPolynesian,),
	iPersia: (iPersian,),
	iCelts: (iCeltic,),
	iRome: (iLatin, iGreek),
	iMaya: (iMayan,),
	iDravidia: (iDravidian, iIndian),
	iEthiopia: (iEthiopian,),
	iToltecs: (iToltec, iNahuatl),
	iKushans: (iKushan, iTurkish, iGreek),
	iKorea: (iKorean,),
	iKhmer: (iKhmerian, iIndian),
	iMali: (iMande, iBerber, iArabic),
	iByzantium: (iByzantine, iGreek, iLatin),
	iFrance: (iFrench,),
	iMalays: (iMalay, iIndian),
	iJapan: (iJapanese,),
	iNorse: (iNordic,),
	iTurks: (iTurkish, iPersian, iArabic),
	iArabia: (iArabic,),
	iTibet: (iTibetan,),
	iMoors: (iArabic, iBerber),
	iJava: (iJavanese, iMalay, iIndian),
	iSpain: (iSpanish,),
	iEngland: (iEnglish,),
	iHolyRome: (iGerman,),
	iBurma: (iBurmese,),
	iRus: (iUkrainian, iRussian),
	iVietnam: (iVietnamese, iIndian),
	iSwahili: (iKiswahili, iArabic),
	iPoland: (iPolish,),
	iPortugal: (iPortuguese,),
	iInca: (iQuechua,),
	iItaly: (iItalian,),
	iMongols: (iMongol, iTurkish),
	iAztecs: (iNahuatl,),
	iMughals: (iPersian, iIndian, iDravidian),
	iRussia: (iRussian,),
	iOttomans: (iOttoman, iTurkish),
	iThailand: (iThai,),
	iSweden: (iSwedish, iNordic),
	iCongo: (iCongolese,),
	iIran: (iPersian,),
	iNetherlands: (iDutch,),
	iGermany: (iGerman,),
	iAmerica: (iAmerican, iEnglish),
	iMexico: (iMexican, iSpanish),
	iArgentina: (iArgentinian, iSpanish),
	iColombia: (iSpanish,),
	iBrazil: (iBrazilian, iPortuguese),
	iCanada: (iEnglish, iFrench),
}


### EVENT HANDLERS ###

@handler("cityBuilt")
def onCityBuilt(city):
	checkName(city, bFound=True)


@handler("cityAcquired")
def onCityAcquired(iOwner, iPlayer, city):
	clearPlayerRenamed(city)
	checkName(city)


@handler("cityRazed")
def onCityRazed(city):
	clearChanges(city)


@handler("playerCityRename")
def onCityRename(city, name):
	if name:
		applyPlayerRenamed(city)
	else:
		clearPlayerRenamed(city)
		checkName(city)


@handler("techAcquired")
def onTechAcquired(iTech, iTeam, iPlayer):
	if infos.techs().where(lambda t: infos.tech(iTech).getEra() == infos.tech(t).getEra()).count() == 1:
		updateNames(iPlayer)


@handler("playerChangeStateReligion")
def onStateReligionChange(iPlayer, iReligion):
	updateNames(iPlayer)


@handler("revolution")
def onRevolution(iPlayer):
	updateNames(iPlayer)


@handler("playerPeriodChange")
def onPeriodChange(iPlayer, iPeriod):
	updateNames(iPlayer)


@handler("greatPersonBorn")
def onGreatPersonBorn(unit, iPlayer):
	updateNames(iPlayer)


### SCENARIOS ###


def setupScenario():
	dRelocated = {}
	dRenamed = {}
	
	if scenario() == i600AD:
		dRelocated = {
			u"Babilû": "Seleukeia",
			"Huiji": "Dunhuang",
			"Ka-ba": "Djoboro",
			"Kalhu": "Al-Mawsil",
			"Mayapan": "Uuc Yabnal",
			"Messana": "Syracusae",
			"Parsa": "Estakhr",
			"Pella": "Thessaloniki",
			"Ravenna": "Venezia",
			"Tarragona": "Barcelona",
			"Yarghol": "Turpan",
		}
		
		dRenamed = {
			"Ra-Kedet": "Alexandreia",
			"Seleukeia": "Tysfwn",
		}
	
	elif scenario() == i1700AD:
		dRelocated = {
			"Anuratapuram": "Colombo",
			"Golkonda": "Hyderabad",
			"Indrapura": "Cua Han",
			"Kalhu": "Al-Mawsil",
			"Khersonesos": "Kaffa",
			"Kissonde": "Lwanda",
			"Pagan": "Awa",
			"Pushkalavati": "Peshawar",
			"Raga": "Tehran",
			"Ravenna": "Venezia",
			"Shurparaka": "Mumbai",
			"Sukadana": "Pontianak",
			"Tarragona": "Barcelona",
			"Tarsus": "Adana",
			"Ujjain": "Dhar",
			"Yashodharapura": "Phnom Penh",
		}
		
		dRenamed = {
			"Byzantion": "Constantinopolis",
			"Mahabalipuram": "Madras",
			"Ra-Kedet": "Alexandreia",
		}
	
	data.dRelocatedCities.update(dRelocated)
	data.dRenamedCities.update(dRenamed)


### LANGUAGES ###

def getPrimaryLanguages(identifier):
	iCiv = civ(identifier)
	
	if iCiv == iEgypt:
		if player(iCiv).getStateReligion() == iIslam:
			return iEgyptianArabic, iArabic
		
		elif player(iCiv).getStateReligion() in [iOrthodoxy, iCatholicism]:
			return iCoptic, iEgyptian
	
	elif iCiv == iChina:
		if period(iCiv) == iPeriodYuan:
			return iChinese, iMongol
		
		elif player(iCiv).getCurrentEra() == iIndustrial:
			return iChinese, iManchu
	
	elif iCiv == iNubia:
		if player(iCiv).getStateReligion() in [iOrthodoxy, iCatholicism]:
			return iNubian, iCoptic
	
	elif iCiv == iGreece:
		if period(iCiv) == iPeriodModernGreece:
			return iModernGreek, iGreek
	
	elif iCiv == iInca:
		if period(iCiv) == iPeriodPeru:
			return iSpanish, iQuechua
	
	elif iCiv in [iMaya, iToltecs, iAztecs]:
		if player(iCiv).getStateReligion() in [iOrthodoxy, iCatholicism, iProtestantism] or team(iCiv).isAVassal():
			return (iSpanish,) + dBaseLanguages[iCiv]
	
	return dBaseLanguages.get(iCiv, tuple())


def getLocalLanguages(tile):
	iRegion = plot(tile).getRegionID()
	
	if iRegion == rHornOfAfrica:
		return iSomali, iLocal
	
	elif iRegion == rManchuria:
		return iManchu, iLocal
	
	elif iRegion in [rMaghreb, rSahara]:
		return iBerber, iLocal
	
	return (iLocal,)


def getLanguages(identifier, tile):
	iCiv = civ(identifier)
	
	for iLanguage in getPrimaryLanguages(iCiv):
		yield iLanguage
	
	plot = plot_(tile)
	local_civs = civs.major().past_birth().where(lambda c: plot.getSettlerValue(c) > 1)
	local_civs = local_civs.where(lambda c: (is_minor(identifier) and plot.getSettlerValue(c) >= 5) or year() < year(dFall[c]) or canEverRespawn(c))
	
	if plot.getRegionID() in lAmerica and True not in data.dFirstContactConquerors:
		local_civs = local_civs.group(iCivGroupAmerica)
	
	lGroupCivs = next((lCivs for lCivs in dCivGroups.values() if iCiv in lCivs), [])
	similar_civs, different_civs = local_civs.split(lambda c: c in lGroupCivs or c in dNeighbours[iCiv] or c in dInfluences[iCiv] or (is_minor(identifier) and plot.isCity() and city_(plot).isEverOwnedCiv(c)))
	
	for iCiv in similar_civs.sort(lambda c: (plot.getSettlerValue(c) > 0, c in lGroupCivs, c in dNeighbours[iCiv], plot.getSettlerValue(c)), reverse=True):
		for iLanguage in getPrimaryLanguages(iCiv):
			yield iLanguage
	
	for iLanguage in getLocalLanguages(tile):
		yield iLanguage
	
	for iCiv in different_civs.sort(lambda c: (c in lGroupCivs, c in dNeighbours[iCiv], plot.getSettlerValue(c)), reverse=True):
		for iLanguage in getPrimaryLanguages(iCiv):
			yield iLanguage


### NAMES ###

def getTileNames(tile):
	base_name = city_names[tile]
	
	# relocated cities
	relocated_name = data.dRelocatedCities.get(base_name, base_name)
	
	# renamed cities
	renamed_name = data.dRenamedCities.get(relocated_name, relocated_name)
	
	return relocated_name, renamed_name


def getTranslations(identifier, tile):
	tile_names = getTileNames(tile)
	return getNameTranslations(identifier, tile, tile_name)


def getNameTranslations(identifier, tile, tile_names):
	for iLanguage, translations in getNameTranslationsByLanguage(identifier, tile, tile_names):
		for translation in translations:
			yield translation


def getNameTranslationsByLanguage(identifier, tile, (base_name, tile_name)):
	if base_name == tile_name:
		return getNameTranslationsForTileByLanguage(identifier, tile, tile_name)

	return interleave(
		getNameTranslationsForTileByLanguage(identifier, tile, tile_name), 
		getNameTranslationsForTileByLanguage(identifier, tile, base_name),
	)


def getNameTranslationsForTileByLanguage(identifier, tile, tile_name):
	iCiv = civ(identifier)	
	translations = Translations.of(tile_name)
	
	if translations.isSingle():
		yield translations.getSingle()
		return
	
	for iLanguage in getLanguages(iCiv, tile):
		yield iLanguage, translations[iLanguage]


def getTranslation(identifier, tile, bFound=False):
	tile_names = getTileNames(tile)
	return getNameTranslation(identifier, tile, tile_names, bFound=bFound)


def getNameTranslation(identifier, tile, (base_name, tile_name), bFound=False):
	bRenaming = base_name == tile_name
	for translation in getNameTranslations(identifier, tile, (base_name, tile_name)):
		if translation.isApplicable(identifier, tile, bFound=bFound, bRenaming=bRenaming):
			return translation


def updateAllNames():
	for iPlayer in players.all():
		updateNames(iPlayer)


def updateNames(iPlayer):
	for city in cities.owner(iPlayer):
		checkName(city, bNotify=True)


def checkName(city, bFound=False, bNotify=False):
	if location(city) in data.playerRenamed:
		return
	
	translation = getTranslation(civ(city), city, bFound=bFound)
	if translation:
		applyName(city, translation, bNotify=bNotify)


def applyName(city, translation, bNotify=False):
	current_name = city.getName()	
	if current_name == translation.name:
		return
	
	if translation.bRelocation:
		applyRelocation(city, translation)
		return
	
	if translation.bRenaming:
		applyRenaming(city, translation)
		return
		
	city.setName(translation.name, False)
	
	if bNotify:
		message(city.getOwner(), "TXT_KEY_MESSAGE_CITY_NAME_CHANGE", current_name, translation.name, location=city, button='Art/Interface/Buttons/Actions/FoundCity.dds')


def applyRelocation(city, translation):
	tile_name = city_names[city]
	if tile_name == translation.name:
		return
	
	current_relocated_name = data.dRelocatedCities.get(tile_name, tile_name)
	if current_relocated_name in data.dRenamedCities:
		del data.dRenamedCities[current_relocated_name]
	
	data.dRelocatedCities[tile_name] = translation.name
	checkName(city)


def applyRenaming(city, translation):
	tile_name = city_names[city]
	tile_name = data.dRelocatedCities.get(tile_name, tile_name)
	
	if tile_name == translation.name:
		return
	
	data.dRenamedCities[tile_name] = translation.name
	checkName(city)


def getDisplayName(identifier, tile):
	tile_names = getTileNames(tile)
	return getDisplayNameForName(identifier, tile, tile_names)


def getDisplayNameForName(identifier, tile, tile_names):
	base_name, tile_name = tile_names
	
	bFound = not plot_(tile).isCity()
	translation = getNameTranslation(identifier, tile, (base_name, tile_name), bFound=bFound)
	
	if not translation:
		return ""
	
	if translation.bRenaming or translation.bRelocation:
		if translation.name != tile_name:
			return getDisplayNameForName(identifier, tile, (translation.name, translation.name))
	
	return translation.name


def getNameEvolution(identifier, tile):
	tile_names = getTileNames(tile)
	bFound = not plot_(tile).isCity()
	
	for iLanguage, translations in getNameTranslationsByLanguage(identifier, tile, tile_names):
		translations = list(translations)
		for index, translation in enumerate(translations):
			if translation.isApplicable(identifier, tile):
				sequence = [t.name for t in translations[:index] if t.isEraSpecific(bFound=bFound)] + [translation.name]
				if sequence:
					return " -> ".join(reversed(sequence))
	
	return getDisplayName(identifier, tile)


def clearChanges(city):
	base_name = city_names[city]
	
	if base_name in data.dRelocatedCities:
		del data.dRelocatedCities[base_name]
	
	if base_name in data.dRenamedCities:
		del data.dRenamedCities[base_name]
	
	clearPlayerRenamed(city)


def applyPlayerRenamed(city):
	data.playerRenamed.add(location(city))


def clearPlayerRenamed(city):
	tile = location(city)
	
	if tile in data.playerRenamed:
		data.playerRenamed.remove(tile)