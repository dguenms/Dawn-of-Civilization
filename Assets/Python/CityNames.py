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
	iNative: (iLocal,),
	iAssyria: (iAssyrian, iBabylonian),
	iChina: (iChinese,),
	iHittites: (iHittite,),
	iNubia: (iNubian, iEgyptian,),
	iGreece: (iGreek,),
	iIndia: (iIndian, iDravidian),
	iPhoenicia: (iPhoenician, iBabylonian),
	iPolynesia: (iPolynesian,),
	iPersia: (iPersian,),
	iCelts: (iCeltic,),
	iRome: (iLatin, iGreek),
	iMaya: (iMayan,),
	iDravidia: (iDravidian, iIndian),
	iEthiopia: (iEthiopian, iArabic),
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
			"Kandarpapura": "Indrapura",
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
			"Chalchihuites": "Guadalajara",
			"Golkonda": "Hyderabad",
			"Indrapura": "Cua Han",
			"Kalhu": "Al-Mawsil",
			"Khersonesos": "Kaffa",
			"Kissonde": "Lwanda",
			"Pagan": "Awa",
			"Pushkalavati": "Peshawar",
			"Raga": "Tehran",
			"Ravenna": "Venezia",
			"Santa Isabel": u"São Tomé",
			"Shurparaka": "Mumbai",
			"Sukadana": "Pontianak",
			"Tarragona": "Barcelona",
			"Tarsus": "Adana",
			"Ujjain": "Dhar",
			"Yarghol": "Turpan",
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
		if player(identifier).getStateReligion() == iIslam:
			return iEgyptianArabic, iArabic
		
		elif player(identifier).getStateReligion() in [iOrthodoxy, iCatholicism]:
			return iCoptic, iEgyptian
		
		elif player(identifier).getPeriod() == iPeriodPtolemaicEgypt:
			return iGreek, iEgyptian, iNubian
	
	elif iCiv == iChina:
		if player(identifier).getPeriod() == iPeriodYuan:
			return iChinese, iMongol
		
		elif player(identifier).getCurrentEra() == iIndustrial:
			return iChinese, iManchu
	
	elif iCiv == iNubia:
		if player(identifier).getStateReligion() in [iOrthodoxy, iCatholicism]:
			return iNubian, iCoptic
	
	elif iCiv == iGreece:
		if player(identifier).getPeriod() == iPeriodModernGreece:
			return iModernGreek, iGreek
	
	elif iCiv == iInca:
		if player(identifier).getPeriod() == iPeriodPeru:
			return iSpanish, iQuechua
	
	elif iCiv in [iMaya, iToltecs, iAztecs]:
		if player(identifier).getStateReligion() in [iOrthodoxy, iCatholicism, iProtestantism] or team(identifier).isAVassal():
			return (iSpanish,) + dBaseLanguages.get(iCiv, tuple())
	
	return dBaseLanguages.get(iCiv, tuple())


def getLocalLanguages(tile):
	iRegion = plot_(tile).getRegionID()
	
	if iRegion == rHornOfAfrica:
		return iSomali, iLocal
	
	elif iRegion == rManchuria:
		return iManchu, iLocal
	
	elif iRegion in [rMaghreb, rSahara]:
		return iBerber, iLocal
	
	return (iLocal,)


class Languages(object):
	
	def __init__(self, identifier, tile):
		self.identifier = identifier
		self.tile = tile
		
		# print "get languages for %s on %s" % (name(identifier), getBaseName(tile))
		
	def __iter__(self):
		iPrimaryIdentifier = self.identifier
		if self.city and is_minor(self.identifier):
			if self.city.getPreviousCiv() >= 0:
				iPrimaryIdentifier = Civ(self.city.getPreviousCiv())
		
		for iLanguage in getPrimaryLanguages(iPrimaryIdentifier):
			# print "yield primary: %s" % iLanguage
			yield iLanguage
		
		local_languages = self.getLocalLanguages()
		local_civs = self.getValidLanguageCivs(local_languages)
		
		if not is_minor(self.identifier) and self.plot.getSettlerValue(self.iCiv) > 0 and (not self.city or self.city.getOriginalCiv() == self.iCiv):
			for iLanguage in getLocalLanguages(self.tile):
				yield iLanguage
		
		if self.plot.getRegionID() in lAmerica and civ(self.identifier) in dCivGroups[iCivGroupAmerica] and True not in data.dFirstContactConquerors.values():
			local_civs = local_civs.group(iCivGroupAmerica)
		
		similar_civs, different_civs = local_civs.split(self.isSimilar)
		
		# print "similar: %s" % [(infos.civ(iCiv).getText(), self.getSortingKey(iCiv)) for iCiv in similar_civs.sort(self.getSortingKey, reverse=True)]
		# print "different: %s" % [(infos.civ(iCiv).getText(), self.getSortingKey(iCiv)) for iCiv in different_civs.sort(self.getSortingKey, reverse=True)]
		
		for iSimilarCiv in similar_civs.sort(self.getSortingKey, reverse=True):
			for iLanguage in getPrimaryLanguages(iSimilarCiv):
				# print "yield similar for %s: %s" % (infos.civ(iSimilarCiv).getText(), iLanguage)
				yield iLanguage
		
		for iLanguage in getLocalLanguages(self.tile):
			# print "yield local: %s" % iLanguage
			yield iLanguage
		
		for iDifferentCiv in different_civs.sort(self.getSortingKey, reverse=True):
			for iLanguage in getPrimaryLanguages(iDifferentCiv):
				# print "yield different for %s: %s" % (infos.civ(iDifferentCiv).getText(), iLanguage)
				yield iLanguage
	
	@property
	def iCiv(self):
		return civ(self.identifier)
	
	@property
	def plot(self):
		return plot_(self.tile)
	
	@property
	def city(self):
		return city_(self.tile)
	
	@property
	def player(self):
		return player(identifier)
	
	def getLocalLanguages(self):
		base_name, changed_name = getTileNames(self.tile)
		
		tile_languages = Translations.of(changed_name).getLanguages()
		
		if base_name != changed_name:
			tile_languages |= Translations.of(base_name).getLanguages()
		
		return tile_languages
	
	def getValidLanguageCivs(self, localLanguages):
		local_civs = [iCiv for iCiv, tLanguages in dBaseLanguages.items() if not is_minor(iCiv) and localLanguages & set(tLanguages)]
		
		return civs.of(*local_civs).where(self.isValid)
	
	def isPastBirth(self, iCiv):
		return since(year(dBirth[iCiv])) > 0 or (self.plot.getSettlerValue(iCiv) > 0 and self.isConnected(iCiv))
	
	def isBeforeFall(self, iCiv):
		return until(year(dFall[iCiv])) > 0 or canEverRespawn(iCiv)
	
	def isValidMinor(self, iCiv):
		return is_minor(self.identifier) and self.plot.getSettlerValue(iCiv) >= 5
	
	def isValidCiv(self, iCiv):
		return self.isPastBirth(iCiv) and self.isBeforeFall(iCiv)
	
	def isValid(self, iCiv):
		return self.isValidMinor(iCiv) or self.isValidCiv(iCiv)
	
	def isSameGroup(self, iCiv):
		return any(self.iCiv in group and iCiv in group for group in dCivGroups.values())
	
	def isConnected(self, iCiv):
		return iCiv in dNeighbours[self.iCiv] or iCiv in dInfluences[self.iCiv]
	
	def isEverOwned(self, iCiv):
		return self.city and self.city.isEverOwnedCiv(iCiv)
	
	def isSimilar(self, iCiv):
		return self.isSameGroup(iCiv) or self.isConnected(iCiv) or (is_minor(self.identifier) and self.isEverOwned(iCiv))
	
	def isRegionalCivGroup(self, iCiv):
		return self.isEverOwned(iCiv) or any(iCiv in dCivGroups[iGroup] and self.plot.getRegionID() in dCivGroupRegions[iGroup] for iGroup in range(iNumCivGroups))
	
	def getValue(self, iCiv):
		if player(iCiv).isExisting():
			return self.plot.getSettlerValue(iCiv)
		
		if data.civs[iCiv].iLastTurnAlive > 0:
			return until(data.civs[iCiv].iLastTurnAlive)
		
		return -until(year(dBirth[iCiv]))
	
	def getCulture(self, iCiv):
		return self.city and self.city.getCivCulture(iCiv) or 0
	
	def getSortingKey(self, iCiv):
		return (
			self.plot.getSettlerValue(iCiv) > 0,
			self.isSameGroup(iCiv),
			self.isConnected(iCiv),
			self.isRegionalCivGroup(iCiv),
			self.plot.getSettlerValue(iCiv) > 1,
			self.getValue(iCiv),
			self.getCulture(iCiv),
		)


### NAMES ###

def getTileNames(tile):
	base_name = city_names[tile]
	
	# relocated cities
	relocated_name = data.dRelocatedCities.get(base_name, base_name)
	
	# renamed cities
	renamed_name = data.dRenamedCities.get(relocated_name, relocated_name)
	
	return relocated_name, renamed_name


def getBaseName(tile):
	return city_names[tile]


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
	
	for iLanguage in Languages(identifier, tile):
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
	
	if translation.name == "?":
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
			if translation.isApplicable(identifier, tile, bFound=bFound):
				sequence = [t.name for t in translations[:index] if t.isEraSpecific(bFound=bFound)] + [translation.name]
				if sequence:
					return " -> ".join(reversed([entry for entry in sequence if entry != "?"]))
	
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