# encoding: utf-8

from CvPythonExtensions import *
from Consts import *
from RFCUtils import utils

gc = CyGlobalContext()
localText = CyTranslator()

lTypes = [iGreatProphet, iGreatArtist, iGreatScientist, iGreatMerchant, iGreatEngineer, iGreatStatesman, iGreatGeneral, iGreatSpy]

lGreatPeople = [[[] for j in lTypes] for i in range(iNumCivilizations)]
lOffsets = [[[0 for i in range(iNumEras)] for j in lTypes] for i in range(iNumCivilizations)]

def testunit(iPlayer, iUnit):
	unit = gc.getPlayer(iPlayer).initUnit(utils.getUniqueUnit(iPlayer, iUnit), 0, 0, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	print getName(unit)
	
def create(iPlayer, iUnit, (x, y)):
	gc.getPlayer(iPlayer).createGreatPeople(utils.getUniqueUnit(iPlayer, iUnit), True, True, x, y)

def getAlias(iCiv, iType):
	if iCiv in [iCivHarappa, iCivTamils]: return iCivIndia
	elif iCiv == iCivHolyRome: return iCivGermany
	elif iCiv == iCivMaya: return iCivAztecs
	elif iCiv == iCivMoors: return iCivArabia
	elif iCiv == iCivThailand: return iCivKhmer
	elif iCiv == iCivTibet and iType != lTypes.index(iGreatProphet): return iCivChina
	
	return iCiv
	
def getType(iUnit):
	iUnitType = utils.getBaseUnit(iUnit)
	if iUnitType in lTypes: return lTypes.index(iUnitType)
	return -1

def getAvailableNames(iPlayer, iType):
	pPlayer = gc.getPlayer(iPlayer)
	iCiv = getAlias(pPlayer.getCivilizationType(), iType)
	iEra = pPlayer.getCurrentEra()
	
	return getEraNames(iCiv, iType, iEra)

def getEraNames(iCiv, iType, iEra):
	lNames = lGreatPeople[iCiv][iType]
	
	iOffset = lOffsets[iCiv][iType][iEra]
	iNextOffset = len(lNames)
	if iEra + 1 < iNumEras: iNextOffset = lOffsets[iCiv][iType][iEra+1]
	
	iSpread = max(iNextOffset - iOffset, iEra+2)
	
	print "Offset: " + str(iOffset)
	print "Spread: " + str(iSpread)
	
	lBefore = [sName for sName in lNames[:iOffset] if not gc.getGame().isGreatPersonBorn(sName)]
	lAfter = [sName for sName in lNames[iOffset:] if not gc.getGame().isGreatPersonBorn(sName)]
	
	print "lBefore: " + str(lBefore)
	print "lAfter: " + str(lAfter)
	
	if len(lAfter) >= iSpread:
		print "Only after offset: " + str(lAfter[:iSpread])
		return lAfter[:iSpread]
	
	iSpread -= len(lAfter)
	print "Include before: " + str(lBefore[:-iSpread] + lAfter)
	return lBefore[:-iSpread] + lAfter
	
def getName(unit):
	iType = getType(unit.getUnitType())
	if iType < 0: return None
	
	lAvailableNames = getAvailableNames(unit.getOwner(), iType)
	if not lAvailableNames: return None
	
	return utils.getRandomEntry(lAvailableNames)
	
def onGreatPersonBorn(unit, iPlayer, city):
	sName = getName(unit)
	if sName:
		gc.getGame().addGreatPersonBornName(sName)
		
		# Leoreth: replace graphics for female GP names
		if sName[0] == "f":
			sName = sName[1:]
			unit = utils.replace(unit, dFemaleGreatPeople[utils.getBaseUnit(unit.getUnitType())])
			
		unit.setName(sName)
		
	# Leoreth: display notification
	if iPlayer not in [iIndependent, iIndependent2, iBarbarian]:
		pDisplayCity = city
		if pDisplayCity.isNone(): pDisplayCity = gc.getMap().findCity(unit.getX(), unit.getY(), PlayerTypes.NO_PLAYER, TeamTypes.NO_TEAM, False, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, CyCity())
			
		sCity = "%s (%s)" % (pDisplayCity.getName(), gc.getPlayer(pDisplayCity.getOwner()).getCivilizationShortDescription(0))
		sMessage = localText.getText("TXT_KEY_MISC_GP_BORN", (unit.getName(), sCity))
		sUnrevealedMessage = localText.getText("TXT_KEY_MISC_GP_BORN_SOMEWHERE", (unit.getName(),))
		
		if city.isNone(): sMessage = localText.getText("TXT_KEY_MISC_GP_BORN_OUTSIDE", (unit.getName(), sCity))
	
		for iLoopPlayer in range(iNumPlayers):
			if gc.getPlayer(iLoopPlayer).isAlive():
				if unit.plot().isRevealed(gc.getPlayer(iLoopPlayer).getTeam(), False):
					CyInterface().addMessage(iLoopPlayer, False, iDuration, sMessage, "AS2D_UNIT_GREATPEOPLE", InterfaceMessageTypes.MESSAGE_TYPE_MAJOR_EVENT, unit.getButton(), ColorTypes(gc.getInfoTypeForString("COLOR_UNIT_TEXT")), unit.getX(), unit.getY(), True, True)
				else:
					CyInterface().addMessage(iLoopPlayer, False, iDuration, sUnrevealedMessage, "AS2D_UNIT_GREATPEOPLE", InterfaceMessageTypes.MESSAGE_TYPE_MAJOR_EVENT, "", ColorTypes(gc.getInfoTypeForString("COLOR_UNIT_TEXT")), -1, -1, False, False)

def setup():
	for iCiv in dGreatPeople.keys():
		for iType in dGreatPeople[iCiv].keys():
			lEntries = dGreatPeople[iCiv][iType]
			for i in range(len(lEntries)):
				entry = lEntries[i]
				if entry in range(iNumEras): lOffsets[iCiv][lTypes.index(iType)][entry] = i
				else: lGreatPeople[iCiv][lTypes.index(iType)].append(entry)
				
			lCurrentOffsets = lOffsets[iCiv][lTypes.index(iType)]
			for i in range(1, len(lCurrentOffsets)):
				if lCurrentOffsets[i] < lCurrentOffsets[i-1]: lCurrentOffsets[i] = lCurrentOffsets[i-1]
				
			lCurrentOffsets[iFuture] = len(lEntries)
				
	print lGreatPeople

		
dGreatPeople = {
iCivChina : {
	iGreatProphet : [
		"Lao Tzu", # 6th BC
		"Kong Fuzi", # 5th BC
		"Meng Zi", # 4th BC
		"Zhuangzi", # 4th BC
		"Han Fei", # 3rd BC
		iMedieval,
		"fLin Moniang", # 10th
		"fSun Bu'er", # 12th
	],
	iGreatArtist : [
		"Ling Lun", # legendary
		"Su Shi", # 11th BC
		iClassical,
		"Li Bo", # 8th BC
		"Du Fu", # 8th BC
		"Wang Xizhi", # 4th BC
		"fCai Wenji", # 1st
		iMedieval,
		"fShangguan Wan'er", # 7th
	],
	iGreatScientist : [
		"Li Fan", # 1st
		"fBan Zhao", # 1st
		"Liu Hui", # 3rd
		"Zu Chongzhi", # 5th
		iMedieval,
		"Zhu Shijie", # 14th
		iRenaissance,
		"fTan Yunxian", # 16th
		iIndustrial,
		"Li Yuanzhe", # 20th
		"Chen Ning Yang", # 20th
	],
	iGreatMerchant : [
		"Zhang Qian", # 2nd BC
		iMedieval,
		"Xuanzang", # 7th
		"Wang Anshi", # 11th
		iRenaissance,
		"Zheng He", # 15th
		iModern,
		"Deng Xiaoping", # 20th
	],
	iGreatEngineer : [
		"fLeizu", # 27th BC
		iClassical,
		"Cai Lun", # 1st
		"Zhang Heng", # 2nd
		iMedieval,
		"Bi Sheng", # 11th
		iModern,
		"Li Siguang", # 20th
		"fWu Jianxiong", # 20th
	],
	iGreatStatesman : [
		"Li Si", # 3rd BC
		"Xiao He", # 2nd BC
		iMedieval,
		"Fang Yuanling", # 7th
		"Di Renjie", # 7th
		iRenaissance,
		"Zhang Juzheng", # 16th
		iIndustrial,
		"Li Hongzhang", # 19th
		"Sun Yat-sen", # 19th
		iModern,
		"Zhou Enlai", # 20th
	],
	iGreatGeneral : [
		"Sun Tzu", # 6th BC
		"Cao Cao", # 2nd
		"Zhuge Liang", # 3rd
		iMedieval,
		"fPingyang Gongzhu", # 7th
		"Guo Ziyi", # 8th
		iRenaissance,
		"Shi Lang", # 17th
		iIndustrial,
		"fChing Shih", # 19th
		iModern,
		"Zhang Zuolin", # 20th
	],
},
iCivIndia : {
	iGreatProphet : [
		"Mahavira", # 6th BC
		"Siddharta Gautama", # 6th BC
		"Ananda", # 6th BC
		"Mahakashyapa", # 6th BC
		iMedieval,
		"Adi Shankara", # 9th
		"Atisha", # 11th
		iRenaissance,
		"fMeera", # 16th
		iIndustrial,
		"Tipu Sultan", # 18th
		iModern,
		"fAnjeze Gonxhe Bojaxhiu", # 20th
	],
	iGreatArtist : [
		"Kalidasa", # 5th BC
		"Valmiki", # 4th BC
		iRenaissance,
		"Basawan", # 16th
		iModern,
		"Raja Rao", # 20th
		"Rabindranath Tagore", # 20th
	],
	iGreatScientist : [
		"Aryabhata", # 5th
		"Brahmagupta", # 7th
		iMedieval,
		"Bhaskara", # 12th
		"Madhava", # 14th
		iRenaissance,
		"Nilakantha Somayaji", # 15th
		"Kamalakara", # 17th
		iModern,
		"fAsima Chatterjee", # 20th
	],
	iGreatMerchant : [
		"Todar Mal", # 16th
		"Shah Jahan", # 17th
		iIndustrial,
		"Jamshetji Tata", # 19th
		"Ardeshir Godrej", # 19th
		iModern,
		"fIndra Nooyi", # 20th
	],
	iGreatEngineer : [
		"Baudhayana", # 8th BC
		"Lagadha", # 1st
		iIndustrial,
		"Jagadish Chandra Bose", # 19th
		iModern,
		"Chandrasekhara Venkata Raman", # 20th
	],
	iGreatStatesman : [
		"Chanakya", # 4th BC
		iMedieval,
		"Rajaraja Chola", # 10th
		iRenaissance,
		"Krishna Devaraya", # 16th
		"Shivaji Bhosle", # 17th
		"Tipu Sultan", # 18th
		iIndustrial,
		"Ram Mohan Roy", # 19th
		"Ranjit Singh", # 19th
	],
	iGreatGeneral : [
		"Chandragupta Maurya", # 4th BC
		"Samudragupta", # 4th BC
		iMedieval,
		"Rajaraja Chola", # 12th
		iRenaissance,
		"fRani Durgavati", # 16th
		"Shivaji Bhosle", # 17th
		iIndustrial,
		"fRani Lakshmibai", # 19th
	],
},
iCivBabylonia : {
	iGreatProphet : [
		"Utnapishtim", # legendary
		"Gilgamesh", # legendary
	],
	iGreatArtist : [
		"fEn-hedu-ana", # 23rd BC
		"Gudea", # 22nd BC
		"Samsu-ditana", # 17th BC
	],
	iGreatScientist : [
		"Tapputi", # legendary
		"Sin-leqi-unninni", # 13th BC
		iClassical,
		"Nabu-rimanni", # 6th BC
		"Kidinnu", # 4th BC
		"Sudines", # 3rd BC
	],
	iGreatMerchant : [
		"Burna-Buriash", # 14th BC
		"Kadashman-Enlil", # 14th BC
	],
	iGreatEngineer : [
		"Naram-Sin", # 22nd BC
		"Ur-Nammu", # 21st BC
		iClassical,
		"Nabopolassar", # 7th BC
	],
	iGreatStatesman : [
		"Urukagina", # 24th BC
		"Ur-Nammu", # 21st BC
		"Bilalama", # 20th BC
		"Lipit-Ishtar", # 19th BC
		iClassical,
		"fShammuramat", # 9th BC
	],
	iGreatGeneral : [
		"Tiglath-Pileser", # 10th BC
		iClassical,
		"Sennacherib", # 7th BC
		"Nebukanezar", # 7th BC
		"Shalmaneser", # 7th BC
	],
},
iCivEgypt : {
	iGreatProphet : [
		"Ptah-Hotep", # 25th BC
		"Meryre", # 15th BC
		"Akhenaten", # 14th BC
		"fHatshepsut", # 14th BC
		"Moses", # 13th BC
		"fNefertiti", # 13th BC
		iClassical,
		"Petiese", # 7th BC
	],
	iGreatArtist : [
		"Khafra", # 26th BC
		"Nefertari", # 23th BC
		"Amenhotep", # 15th BC
		"Anena", # 15th BC
		"Amenemhat", # 15th BC
		"Yuny", # 13th BC
		"Khaemweset", # 12th BC
	],
	iGreatScientist : [
		"fMerit-Ptah", # 27th BC
		iClassical,
		"Manetho", # 3rd BC
		"Ptolemaios", # 2nd
		"Diophantos", # 3rd
		"fHypatia", # 4th
	],
	iGreatMerchant : [
		"Harkhuf", # 23rd BC
		"Ahmose", # 16th BC
		"Maya", # 13th BC
		"fTiye", # 13th BC
		iClassical,
		"Piye", # 8th BC
		"Alara", # 8th BC
	],
	iGreatEngineer : [
		"Imhotep", # 27th BC
		"Djoser", # 27th BC
		"Sneferu", # 27th BC
		"Senenmut", # 17th BC
	],
	iGreatStatesman : [
		"Kagemni", # 26th BC
		"Amenemhat", # 20th BC
		"fHatshepsut", # 15th BC
		"Amenemope", # 12th BC
		"Herihor", # 11th BC
	],
	iGreatGeneral : [
		"Narmer", # 32nd BC
		"Menes", # 30th BC
		"Khufu", # 26th BC
		"Mentuhotep", # 21st BC
		"Thutmosis", # 15th BC
		"Sethi", # 13th BC
	],
},
iCivGreece : {
	iGreatProphet : [
		"Herakleitos", # 6th BC
		"Anacharsis", # 6th BC
		"Parmenides", # 5th BC
		"Philolaos", # 5th BC
		"Epikouros", # 4th BC
	],
	iGreatArtist : [
		"Homeros", # 8th BC
		"fSappho", # 6th BC
		"Sophokles", # 5th BC
		"Thoukydides", # 5th BC
		"Euripides", # 5th BC
		"Herodotos", # 5th BC
		"Aischylos", # 5th BC
		"Anyte Tegeatis", # 3rd BC
	],
	iGreatScientist : [
		"Pythagoras", # 6th BC
		"Sokrates", # 5th BC
		"Demokritos", # 5th BC
		"Anaxagoras", # 5th BC
		"Hippokrates", # 5th BC
		iClassical,
		"Aristoteles", # 4th BC
		"Platon", # 4th BC
		"Eukleides", # 3rd BC
		"Eratosthenes", # 3rd BC
		"Galenos", # 2nd BC
		"fAglaonike", # 2nd BC
		"fHypatia", # 4th
	],
	iGreatMerchant : [
		"Kroisos", # 6th BC
		"Pytheas", # 4th BC
		"Androsthenes", # 4th BC
		"Megasthenes", # 4th BC
	],
	iGreatEngineer : [
		"Thales", # 6th BC
		"Empedokles", # 5th BC
		"Zenon", # 4th BC
		"Satyros", # 4th BC
		"Archimedes", # 3rd BC
		"Heron", # 1st
	],
	iGreatStatesman : [
		"Solon", # 6th BC
		"Kleisthenes", # 6th BC
		"Alkibiades", # 5th BC
		"Kimon", # 5th BC
		"Isokrates", # 4th BC
		"Aresteides", # 4th BC
		iIndustrial,
		"Eleftherios Venizelos", # 19th AD
	],
	iGreatGeneral : [
		"Hektor", # legendary
		iClassical,
		"Leonidas", # 6th BC
		"Themistokles", # 5th BC
		"Lysandros", # 5th BC
		"Philippos", # 4th BC
		"Pyrrhos", # 3rd BC
		"fArtemisia", # 4th
	],
},
iCivPhoenicia : {
	iGreatProphet : [
		"Acherbas", # legendary
		iClassical,
		"Tertullian", # 2nd
		"Cyprian", # 3rd
		"Donatus", # 4th
	],
	iGreatArtist : [
		"Kartobal", # ?
		"Ortobal", # ?
		"Sophonisba", # 3rd BC
		"Micipsa", # 2nd BC
		"Oxynthas", # ?
	],
	iGreatScientist : [
		"Hiram", # 10th BC
		"Mago", # 4th BC
		"Bomilcar", # 3rd BC
		"Eshmuniaton", # ?
		"Tanit", # ?
	],
	iGreatMerchant : [
		"Hanno", # 5th BC
		"Himilco", # 5th BC
		"Adherbal", # 2nd BC
		"Bocchus", # 2nd BC
	],
	iGreatEngineer : [
		"Gala", # 3rd BC
		"Zelalsen", # ?
		"Malchus", # ?
		"Gauda", # ?
	],
	iGreatStatesman : [
		"Astarymus", # 9th BC
		"Pygmalion", # 9th BC
		"fElishat", # 8th BC
		"Hanno", # 5th BC
		"Azelmicus", # 4th BC
	],
	iGreatGeneral : [
		"Hasdrubal Barca", # 3rd BC
		"Hamilcar Barca", # 3rd BC
		"Mago Barca", # 3rd BC
		"Maharbal", # 2nd BC
		"Cathalo", # ?
	],
},
iCivPersia : {
	iGreatProphet : [
		"Zoroaster", # 18-10th BC
		iClassical,
		"Mani", # 3rd
		"Mazdak", # 4th
		iMedieval,
		"Al-Ghazali", # 11th
		"Mevlana", # 13th
		iRenaissance,
		"Mulla Sadra", # 17th
	],
	iGreatArtist : [
		"Firdausi", # 10th
		"fRabia Balkhi", # 10th
		"Safi al-Din", # 13th
		"Saadi", # 13th
		iRenaissance,
		"Kamal ud-Din Behzad", # 15th
		"Reza Abbasi", # 16th
	],
	iGreatScientist : [
		"Ardashir", # 4th
		iMedieval,
		"Al-Khwarizmi", # 9th
		"Al-Razi", # 9th
		"Ibn Sina", # 10th
		"Abd al-Rahman al-Sufi", # 10th
		"Al-Farisi", # 13th
	],
	iGreatMerchant : [
		"Kavadh", # 5th
		iMedieval,
		"Ahmad ibn Rustah", # 10th
		"Istakhri", # 10th
	],
	iGreatEngineer : [
		"Artaxerxes", # 5th BC
		"Bahram", # 3rd
		iMedieval,
		"Al-Khujandi", # 10th
		"Ibn al-Haitham", # 10th
	],
	iGreatStatesman : [
		"Tissaphernes", # 5th BC
		"Tiribazus", # 4th BC
		"fMania", # 4th BC
	],
	iGreatGeneral : [
		"Achaemenes", # 7th BC
		"Xerxes", # 5th BC
		"Mehrdad", # 2nd BC
		"Shapur", # 3rd
		iRenaissance,
		"Abbas", # 16th
	],
},
iCivRome : {
	iGreatProphet : [
		"Augustinus", # 4th
		"Aurelius Ambrosius", # 4th
		"Eusebius", # 4th
		"fMarcella", # 4th
	],
	iGreatArtist : [
		"Vergilius", # 1st BC
		"Livius", # 1st
		"Ovidius", # 1st
		"Plutarchus", # 1st
		"Iuvenalis", # 2nd
	],
	iGreatScientist : [
		"Cato", # 1st BC
		"Cicero", # 1st BC
		"Sosigenes", # 1st BC
		"Plinius", # 1st
		"Strabo", # 1st
		"Seneca", # 1st
	],
	iGreatMerchant : [
		"Marcus Crassus", # 1st BC
		"Iucundus", # ?
		"Atticus", # ?
		"Sittius", # ?
	],
	iGreatEngineer : [
		"Apollodorus", # 2nd BC
		"Vitruvius", # 1st BC
		"Agrippa", # 1st BC
		"Hitarius", # ?
	],
	iGreatStatesman : [
		"Publicola", # 6th BC
		"Cincinnatus", # 5th BC
		"Quintus Hortensius", # 3rd BC
		"Cato", # 2nd BC
		"Cicero", # 1st BC
		"Sulla", # 1st BC
		"fLivia Drusilla", # 1st BC
		"fFulvia", # 1st AD
		"Diocletianus", # 3rd
	],
	iGreatGeneral : [
		"Scipio Africanus", # 2nd BC
		"Gaius Marius", # 2nd BC
		"Pompeius", # 1st BC
		"Vaspasianus", # 1st
		"Traianus", # 1st
		"fAgrippina", # 1st AD
		"Hadrianus", # 2nd
		"fAlbia Dominica", # 4th AD
	],
},
iCivJapan : {
	iGreatProphet : [
		"Kobo Daishi", # 8th
		"Eisai Zenji", # 12th
		"Shinran", # 13th
		"Nikko Shonin", # 13th
		iRenaissance,
		"Takuan Soho", # 17th
		iIndustrial,
		"Uchimura Kanzo", # 19th
	],
	iGreatArtist : [
		"fMurasaki Shikibu", # 10th
		"Saigyo Hoshi", # 12th
		iRenaissance,
		"Kano Eitoku", # 16th
		iIndustrial,
		"Toshusai Sharaku", # 18th
		"Katsushika Hokusai", # 18th
		"Utagawa Hiroshige", # 19th
		iModern,
		"Toro Okamoto", # Contest Reward
	],
	iGreatScientist : [
		"Yoshida Mitsuyoshi", # 17th
		"Aida Yasuaki", # 18th
		iModern,
		"Kiyoshi Ito", # 20th
		"Hideki Yukawa", # 20th
		"Masatoshi Koshiba", # 20th
		"Kenkichi Iwasawa", # 20th
	],
	iGreatMerchant : [
		"Torakusu Yamaha", # 19th
		"Otano Kozui", # 19th
		iModern,
		"Masahisa Fujita", # 20th
		"Kiichiro Toyoda", # 20th
		"Soichiro Honda", # 20th
		"Yoshitaka Fukuda", # 20th
	],
	iGreatEngineer : [
		"Tanaka Hisashige", # 19th
		"Katayama Tokuma", # 19th
		"Takeda Ayasaburo", # 19th
		iModern,
		"Kotaro Honda", # 20th
		"Ken Sakamura", # 20th
		"Kyota Sugimoto", # 20th
		"Hidetsugu Yagi", # 20th
		"Shigeru Miyamoto", # 20th
	],
	iGreatStatesman : [
		"Shoutouku Taishi", # 6th
		iMedieval,
		"Taira no Kiyomori", # 12th
		iRenaissance,
		"Tokugawa Ieyasu", # 16th
		"Arai Hakuseki", # 17th
		iIndustrial,
		"Sakamoto Ryouma", # 19th
		"Oukubo Toshimichi", # 19th
		iModern,
		"Shigeru Yoshida", # 20th
	],
	iGreatGeneral : [
		"Fujiwara no Kamatari", # 7th
		iMedieval,
		"Minamoto no Yoritomo", # 12th
		"Ashikaga Takauji", # 14th
		iRenaissance,
		"Toyotomi Hideyoshi", # 16th
		iIndustrial,
		"fNakano Takeko", # 19th
		"Togo Heihachiro", # 19th
		iModern,
		"Isoroku Yamamoto", # 20th
		"Tomoyuki Yamashita", # 20th
	],
},
iCivEthiopia : {
	iGreatProphet : [
		"Gabra Manfas Qeddus", # legendary
		"Yared", # 6th
		iMedieval,
		"Ewostatewos", # 14th
		"Abba Samuel", # 14th
		iModern,
		"Abune Tewophilos", # 20th
	],
	iGreatArtist : [
		"Gebre Kristos Desta", # 19th
		iModern,
		"Tsegaye Gabre-Medhin", # 20th
		"Adamu Tesfaw", # 20th
		"Afeworq Tekle", # 20th
		"Alexander Boghossian", # 20th
	],
	iGreatScientist : [
		"Abba Bahrey", # 16th
		iModern,
		"Aklilu Lemma", # 20th
		"Kitaw Ejigu", # 20th
		"Sossina Haile", # 20th
		"Gebisa Ejeta", # 20th
	],
	iGreatMerchant : [
		"Nigiste Saba", # legendary
		iModern,
		"Berhanu Nega", # 20th
		"Eleni Gebre-Medhin", # 20th
		"Mohammed Al Amoudi", # 20th
	],
	iGreatEngineer : [
		"Ezana", # 4th
		iMedieval,
		"Gebre Mesqel Lalibela", # 13th
		iRenaissance,
		"Alam Sagad", # 17th
	],
	iGreatStatesman : [
		"Ezana", # 4th
		iRenaissance,
		"Susenyos", # 17th
		iIndustrial,
		"Tewodros", # 19th
		"Menelik", # 19th
		iModern,
		"Mengistu Haile Mariam", # 20th
	],
	iGreatGeneral : [
		"fGudit", # 10th
		"Yekuno Amlak", # 13th
		"Amda Seyon", # 14th
		"Eskender", # 15th
		"Tewodros", # 15th
		iRenaissance,
		"Iyasu", # 17th
		iIndustrial,
		"Yohannes", # 19th
	],
},
iCivKorea : {
	iGreatProphet : [
		"Jinul", # 12th
		"Uicheon", # 12th
		"Baegun", # 13th
		iRenaissance,
		"fHeo Nanseolheon", # 16th
	],
	iGreatArtist : [
		"Damjing", # 7th
		"Yi Nyeong", # 9th
		"Yi Je-hyeon", # 9th
		iRenaissance,
		"Hwang Jip-jung", # 16th
		"Yan Duseo", # 17th
		"Kim Hong-do", # 18th
		"Jeong Seon", # 18th
		"Shin Yun-bok", # 18th
	],
	iGreatScientist : [
		"Uisan", # 7th
		"Wonhyo", # 7th
		iRenaissance,
		"Jeong Inji", # 15th
		"Seong Sammun", # 15th
		"Yu Seong-won", # 15th
		"Heo Jun", # 16th
		iModern,
		"Hwang Woo-Suk", # 20th
	],
	iGreatMerchant : [
		"Kim Sa-hyeong", # 15th
		"Yi Mu", # 15th
		"Yi Hoe", # 15th
	],
	iGreatEngineer : [
		"Choe Yun-ui", # 13th
		"Choe Mu-seon", # 14th
		iRenaissance,
		"Jang Yeong-sil", # 15th
		"Song I-yeong", # 16th
	],
	iGreatStatesman : [
		"Myeongnim Dap-bo", # 2nd
		"fSeondeok", # 7th
		"Kim Bu-sik", # 12th
		iRenaissance,
		"Yi Hwang", # 16th
		iIndustrial,
		"Kim Ok-gyun", # 19th
		"fMyeongseong", # 19th
		iModern,
		"Kim Gu", # 20th
		"Kim Dae-jung", # 20th
	],
	iGreatGeneral : [
		"Gang Gam-chan", # 11th
		"Choe Woo", # 13th
		"Yi Seong-gye", # 14th
		iRenaissance,
		"Yi Sun-sin", # 16th
	],
},
iCivByzantium : {
	iGreatProphet : [
		"fTheodora", # 6th
		"Kyrillos", # 9th
		"Methodios", # 9th
		"Photios", # 9th
		"Nikolaos Mystikos", # 10th
		"Ioannes Xiphilinos", # 11th
	],
	iGreatArtist : [
		"Theophylaktos Simokates", # 7th
		"Theodoros Prodromos", # 12th
		"Eulalios", # 12th
		"Manuel Chrysoloras", # 14th
		"Georgios Plethon", # 14th
		"Theophanes Strelitzas", # 16th
	],
	iGreatScientist : [
		"Stephanos Alexandrinos", # 7th
		"Michael Psellos", # 11th
		"Nikephoros Blemmydes", # 13th
		"Niketas Choniates", # 13th
		"Nikephoros Gregoras", # 14th
		"Gregorios Gemistos", # 15th
	],
	iGreatMerchant : [
		"Hierokles", # 6th
		"Zemarchos", # 6th
		"Georgios Kyprios", # 7th
		"Danielis", # 9th
	],
	iGreatEngineer : [
		"Anthemios", # 6th
		"Isidoros", # 6th
		"Eutokios", # 6th
		"Kallinikos", # 7th
	],
	iGreatStatesman : [
		"Theodosios", # 4th
		"Tribonianos", # 6th
		"fEirene", # 6th
		"Irakleios", # 7th
		"Leon", # 9th
		"Michael Palaiologos", # 13th
	],
	iGreatGeneral : [
		"Belisarios", # 6th
		"Ioannis Tzimiskes", # 10th
		"Basileios Bulgaroktonos", # 11th
		"Georgios Maniakes", # 11th
		"Michael Palaiologos", # 12th
		"Nikephoros Bryennios", # 12th
		"Andronikos Kontostephanos", # 12th
		"Alexios Strategopoulos", # 13th
	],
},
iCivVikings : {
	iGreatProphet : [
		"Ansgar", # 9th
		u"Haraldr Blátonn", # 10th
		u"Sveinn Tjúguskegg", # 10th
		"Birgitta Birgersdotter", # 13th
	],
	iGreatArtist : [
		"Nils Hakansson", # 14th swedish
		iRenaissance,
		"Johan Nordahl Brun", # 18th
		iIndustrial,
		"Hans Christian Andersen", # 19th
		"Olav Duun", # 19th
		"Johan Ludvig Runeberg", # 19th finnish
		"fJohanna Maria Lind", # 19th
		iModern,
		"fAstrid Lindgren", # 20th
	],
	iGreatScientist : [
		"Tycho Brahe", # 16th
		"fSophia Brahe", # 16th
		"Mikael Agrocola", # 16th finnish
		u"Ole Rømer", # 17th
		"Anders Celsius", # 18th swedish
		iIndustrial,
		"Johannes Rydberg", # 19th swedish
		"Anders Angstrom", # 19th swedish
		iModern,
		"Niels Bohr", # 20th
	],
	iGreatMerchant : [
		"Eirikr Raudhi", # 10th
		"Leifr Eiriksson", # 10th
		"Haakon Sigurdsson", # 10th
		iModern,
		"Ingvar Kamprad", # 20th swedish
		"Roald Amundsen", # 20th
	],
	iGreatEngineer : [
		"Hercules von Oberberg", # 16th
		iIndustrial,
		"Niels Abel", # 19th
		"Alfred Nobel", # 19th swedish
		iModern,
		"Ivar Giaever", # 20th
	],
	iGreatStatesman : [
		"Gorm den Gamle", # 10th
		"Erik den Helige", # 11th
		"fMargrete", # 14th
		iRenaissance,
		"Gustav Vasa", # 16th
		iIndustrial,
		"NFS Grundtvig", # 19th
		iModern,
		u"Dag Hammarskjöld", # 20th
	],
	iGreatGeneral : [
		u"Eiríkr Blóðøx", # 10th
		u"Harald Harðráði", # 11th
		"Knutr", # 11th
		"Birger Jarl", # 13th swedish
		iRenaissance,
		"Gustav Vasa", # 16th swedish
		iIndustrial,
		"fIngela Gathenhielm", # 19th
	],
},
iCivArabia : {
	iGreatProphet : [
		"Ali ibn Abi Talib", # 7th
		"Hasan ibn Ali", # 7th
		"Uthman ibn Affan", # 7th
		"Umar ibn al-Kattab", # 7th
		"fRabia Basri", # 9th
		"Al-Baqilanni", # 10th
	],
	iGreatArtist : [
		"Ibn Muqlah", # 10th
		"Ibn al-Nadim", # 10th
		"Al-Mutanabbi", # 10th
		"Ibn Quzman", # 12th
		"Yaqut al-Hamawi", # 13th
		iRenaissance,
		"Ibn Furtu", # 16th
	],
	iGreatScientist : [
		"Al-Kindi", # 9th
		"Al-Farabi", # 10th
		"Ibrahim ibn Sinan", # 10th
		"Ibn al-Jazzar", # 10th
		"Al-Zarqali", # 11th
		"Ibn al-Haytam", # 11th
	],
	iGreatMerchant : [
		"Ibn Hawqal", # 10th
		"Al-Idrisi", # 12th
		"Ibn Jubayr", # 12th
		"Ibn Battuta", # 14th
		"Ahmad ibn Majid", # 15th
	],
	iGreatEngineer : [
		"Jabir ibn Hayyan", # 8th
		"Abbas ibn Firnas", # 9th
		"Ibn Wahshiyah", # 10th
		"Al-Jazari", # 12th
	],
	iGreatStatesman : [
		"fFatimah bint Muhammad", # 7th
		"Al-Jahiz", # 9th
		"Izz al-Din Usama", # 12th
		"Ibn al-Khatib", # 14th
		"Ibn Khaldun", # 14th
		iIndustrial,
		"Muhammad ibn Saud", # 18th
		iModern,
		"Yasser Arafat", # 20th
	],
	iGreatGeneral : [
		"Khalid ibn al-Walid", # 7th
		"Muawiyah", # 7th
		"Ziyad ibn Abihi", # 7th
		"Amr ibn al-As", # 7th
		"fKhawla bint al-Azwar", # 7th
		"Nur ad-Din Zengi", # 12th
		"Yusuf ibn Tashfin", # 12th
		iRenaissance,
		"Ahmah al-Mansur", # 16th
	],
},
iCivKhmer : {
	iGreatProphet : [
		"Kirtipandita", # 10th x
		"Tamalinda", # 12th
		iIndustrial,
		"Chuon Nath", # 19th
		iModern,
		"Maha Ghosananda", # 20th
	],
	iGreatArtist : [
		"Thammaracha", # 16th
		iIndustrial,
		"Ang Duong", # 19th
		iModern,
		"Vann Nath", # 20th
		"Chath Piersath", # 20th
		"Chhim Sothy", # 20th
	],
	iGreatScientist : [
		"Jayavarman", # 10th
		"fSaptadevakula Prana", # 10th
		iModern,
		"Krisana Kraisintu", # 20th
		"Shaiwatna Kupratakul", # 20th
	],
	iGreatMerchant : [
		"Srindravarman", # 14th
		"Uthong", # 14th
		"fDaun Penh",
		iRenaissance,
		"Chey Chettha", # 16th
		"Srei Meara", # 17th
		iModern,
		"Teng Bunma", # 20th
	],
	iGreatEngineer : [
		"Indravarman", # 9th
		"Yasovarman", # 9th
		"fJahavi", # 10th
		iModern,
		"Vann Molyvann", # 20th
	],
	iGreatStatesman : [
		"Jayavarman", # 9th
		"Harshavarman", # 10th
		iIndustrial,
		"Norodom", # 19th
		iModern,
		"Tou Samouth", # 20th
	],
	iGreatGeneral : [
		"fTrieu Thi Trinh", # 3rd
		"Bhavavarman", # 6th
		"Vinyanandana", # 9th
		"Rajendravarman", # 10th
		iModern,
		"Sak Sutsakhan", # 20th
		"Dien Del", # 20th
	],
},
iCivIndonesia : {
	iGreatProphet : [
		"Maha Rsi Agastya", # 5th
		"Buddha Pahyien", # 4th
		"Sakyakirti", #7th
		"fGayatri Rajapatni", # 14th 
		iRenaissance,
		"Sunan Giri", # 15th 
		"Sunan Gunung Jati", # 16th 
	],
	iGreatArtist : [
		"Asep Sunandar Sunarya", #20th
		"I Made Sidia", #20th
                "Ismail Marzuki", #20th
	],
	iGreatScientist : [
		"Jayabaya", # 12th
		"Empu Tantular", #14th
	],
	iGreatMerchant : [
                "Dewawarman", #1st
		"fCri Kahulunnan", #9th
		iRenaissance,
                "Nahkoda Muda", #18th
	],
	iGreatEngineer : [
                "Gunadharma" #9th
		"Samaratungga", #9th
		"Rakai Pikatan", #9th
	],
	iGreatStatesman : [
		"Gajah Mada", # 14th 
		"Parmeswara", # 14th 
		iIndustrial,
		"Mahmud Badaruddin", # 19th 
		"fRaden Ayu Kartini", # 19th 
		iModern,
		"Sukarno", # 20th 
		"Agus Salim", # 20th 
		"Chep the Magnificent", # Contest Reward 
	],
	iGreatGeneral : [
		"Dharmawangsa", #10th
		"Airlangga", #11th
		"Ken Arok", #12th
		"Raden Wijaya", #13th
		"fTribhuwana Vijayatunggadewi", # 14th
		iRenaissance,
		"fMalahayati" #16th
		"fMartha Christina Tiahahu" #18th
                "Pattimura" #18th
	],
},
iCivSpain : {
	iGreatProphet : [
		"Ignacio de Loyola", # 16th
		u"Juan de Sepúlveda", # 16th
		u"fTeresa de Ávila", # 16th
		u"Francisco Suárez", # 16th
		u"Bartolomé de Las Casas", # 16th
		iIndustrial,
		u"Junípero Serra", # 18th
	],
	iGreatArtist : [
		"Miguel de Cervantes", # 16th
		"Garcilaso de la Vega", # 16th
		u"fJuana Inés de la Cruz", # 17th
		u"Diego de Silva Velázquez", # 17th
		iModern,
		"Pablo Picasso", # 20th
		u"Salvador Dalí", # 20th
	],
	iGreatScientist : [
		"Juan de Ortega", # 11th
		"Gerardo de Cremona", # 12th
		iIndustrial,
		"Antonio de Ulloa", # 18th
		u"Santiago Ramón y Cajal", # 19th
	],
	iGreatMerchant : [
		u"Cristóbal Colón", # 15th
		"Fernando de Magallanes", # 15th
		"Hernando de Soto", # 16th
		iIndustrial,
		"Salvador Fidalgo", # 18th
	],
	iGreatEngineer : [
		"Juan de Herrera", # 16th
		iIndustrial,
		u"Agustín de Betancourt", # 18th
		"Alberto de Palacio y Elissague", # 19th
		"Esteban Terradas i Illa", # 19th
		iModern,
		"Juan de la Cierva", # 20th
	],
	iGreatStatesman : [
		u"Francisco Jiménez de Cisneros", # 15th
		"Francisco de Vitoria", # 16th
		iIndustrial,
		u"José de Gálvez", # 18th
		u"José Moniño", # 18th
		"Juan Prim", # 19th
	],
	iGreatGeneral : [
		"El Cid", # 11th
		iRenaissance,
		"Francisco Coronado", # 16th
		u"Hernán Cortés", # 16th
		"Francisco Pizarro", # 16th
		u"Álvaro de Bazán", # 16th
		u"fMaría Pacheco", # 16th
		u"Ambrosio Spínola Doria", # 17th
	],
},
iCivFrance : {
	iGreatProphet : [
		u"Pierre Abélard", # 12th
		"Louis IX", # 13th
		"fJeanne d'Arc", # 15th
		iRenaissance,
		"Jean Calvin", # 16th
		iIndustrial,
		u"fThérèse de Lisieux", # 19th
		iModern,
		"Albert Schweitzer", # 20th
		u"Marcel Légaut", # 20th
	],
	iGreatArtist : [
		u"Chrétien de Troyes", # 12th
		"fChristine de Pizan", # 15th
		iRenaissance,
		"Charles Le Brun", # 17th
		"Jean-Baptiste Lully", # 17th
		"Jean-Antoine Watteau", # 17th
		iIndustrial,
		"Victor Hugo", # 19th
		"Claude Monet", # 19th
		"Henri Matisse", # 19th
		"Claude Debussy", # 19th
		"fGeorge Sand", # 19th
		"Alexandre Dumas", # 19th
		iModern,
		"fEdith Piaf", # 20th
	],
	iGreatScientist : [
		"Nicole Oresme", # 14th
		iRenaissance,
		"Rene Descartes", # 17th
		"Pierre de Fermat", # 17th
		"Antoine Lavoisier", # 18th
		u"fÉmilie du Châtelet", # 18th
		"Pierre-Simon Laplace", # 18th
		iIndustrial,
		"Louis Pasteur", # 19th
		"fMarie-Sophie Germain", # 19th
		"fMarie Curie", # 19th
		iModern,
		"Antoine Henri Becquerel", # 20th
	],
	iGreatMerchant : [
		"Jacques Cartier", # 16th
		"Samuel de Champlain", # 17th
		iIndustrial,
		u"fThérèse de Couagne", # 18th
		iModern,
		"fCoco Chanel", # 20th
		"Marcel Dessault", # 20th
	],
	iGreatEngineer : [
		"Jules Hardouin Mansart", # 17th
		"Blaise Pascal", # 17th
		"Claude Perrault", # 17th
		"Charles Augustin de Coulomb", # 18th
		"Joseph-Michel Montgolfier", # 18th
		iIndustrial,
		"Alexandre Gustave Eiffel", # 19th
		iModern,
		"fMarie Marvingt", # 20th
	],
	iGreatStatesman : [
		u"fAliénor d'Aquitaine", # 12th
		"Philippe de Beaumanoir", # 13th
		iRenaissance,
		"Jean Bodin", # 16th
		"Armand Jean du Plessis", # 17th
		"Jean-Baptiste Colbert", # 17th
		u"fAnne Marie Louise d'Orléans", # 17th
		u"Charles-Maurice de Talleyrand-Périgord", # 18th
		"Montesquieu", # 18th
		"Voltaire", # 18th
		iIndustrial,
		"Pierre-Joseph Proudhon", # 19th
		iModern,
		"fSimone de Beauvoir", # 20th
	],
	iGreatGeneral : [
		"Charles Martel", # 8th
		"Godefroy de Bouillon", # 11th
		"Charles V", # 14th
		"fJeanne d'Arc", # 15th
		iRenaissance,
		"Louis-Joseph de Montcalm", # 18th
		"Louis-Rene de Latouche Treville", # 18th
		"Louis-Nicolas Davout", # 18th
		iIndustrial,
		"Gilbert de Lafayette", # 19th
	],
},
iCivEngland : {
	iGreatProphet : [
		"Bede the Venerable", # 8th
		"Anselm of Canterbury", # 11th
		"Thomas Becket", # 12th
		iRenaissance,
		"Thomas More", # 16th
		"John Newton", # 18th
		iIndustrial,
		"William Booth", # 19th
	],
	iGreatArtist : [
		"William Shakespeare", # 17th
		"John Milton", # 17th
		"John Vanbrugh", # 17th
		"George Frideric Handel", # 18th
		"fMary Wollstonecraft", # 18th
		iIndustrial,
		"Charles Dickens", # 19th
		"Arthur Conan Doyle", # 19th
		"fMary Shelley", # 19th
		iModern,
		"fAgatha Christie", # 20th
		"John Lennon", # 20th
	],
	iGreatScientist : [
		"Francis Bacon", # 16th
		"Isaac Newton", # 17th
		iIndustrial,
		"John Dalton", # 19th
		"Charles Darwin", # 19th
		"James Clerk Maxwell", # 19th
		"fMary Anning", # 19th
		iModern,
		"Ernest Rutherford", # 20th
		"fRosalind Franklin", # 20th
		"Stephen Hawking", # 20th
	],
	iGreatMerchant : [
		"Francis Drake", # 16th
		"James Cook", # 18th
		"Adam Smith", # 18th
		iModern,
		"John Maynard Keynes", # 20th
	],
	iGreatEngineer : [
		"Christopher Wren", # 17th
		"James Watt", # 18th
		iIndustrial,
		"Henry Bessemer", # 19th
		"Charles Babbage", # 19th
		"fAda Lovelace", # 19th
		iModern,
		"Alan Turing", # 20th
	],
	iGreatStatesman : [
		"Thomas Beckett", # 12th
		iRenaissance,
		"William Cecil", # 16th
		"John Locke", # 17th
		"Thomas Hobbes", # 17th
		"Robert Walpole", # 18th
		"William Pitt", # 18th
		iIndustrial,
		"William Gladstone", # 19th
		"Benjamin Disraeli", # 19th
		iModern,
		"Clement Atlee", # 20th
	],
	iGreatGeneral : [
		"William the Conqueror", # 11th
		"Richard the Lionheart", # 12th
		"Edward III", # 14th
		iRenaissance,
		"Oliver Cromwell", # 17th
		"Horatio Nelson", # 18th
		iIndustrial,
		"Arthur Wellington", # 19th
		iModern,
		"Bernard Law Montgomery", # 20th
	],
},
iCivGermany : {
	iGreatProphet : [
		"fHildegard von Bingen", # 12th
		"Albertus Magnus", # 13th
		"Jan Hus", # 14th
		iRenaissance,
		"Martin Luther", # 16th
		"Philip Melanchthon", # 16th
		iModern,
		"Dietrich Bonhoeffer", # 20th
		"fEdith Stein", # 20th
	],
	iGreatArtist : [
		"fRoswitha von Gandersheim", # 10th
		u"Albrecht Dürer", # 15th
		iRenaissance,
		"Johann Sebastian Bach", # 17th
		"Ludwig van Beethoven", # 18th
		"Wolfgang Amadeus Mozart", # 18th
		"Johann Wolfgang von Goethe", # 18th
		"Friedrich Schiller", # 18th
		iIndustrial,
		"fClara Schumann", # 19th
		iModern,
		"fLeni Riefenstahl", # 20th
		"Leoreth", # 20th
	],
	iGreatScientist : [
		"Johannes Kepler", # 17th
		"Gottfried Leibniz", # 17th
		iIndustrial,
		u"Carl Friedrich Gauß", # 19th
		iModern,
		"Albert Einstein", # 20th
		"Werner Heisenberg", # 20th
		"fEmmy Noether", # 20th
		"Max Planck", # 20th
		u"Erwin Schrödinger", # 20th
		"fLise Meitner", # 20th
	],
	iGreatMerchant : [
		"Jakob Fugger", # 15th
		"Gerhard Mercator", # 16th
		"fBarbara Uthmann", # 16th
		iIndustrial,
		"Carl Benz", # 19th
		"Alfred Krupp", # 19th
		iModern,
		"Ferdinand Porsche", # 20th
		"August Horch", # 20th
		"fMelitta Bentz", # 20th
	],
	iGreatEngineer : [
		"Jakob Fugger", # 15th
		"Gerhard Mercator", # 16th
		"fBarbara Uthmann", # 16th
		iIndustrial,
		"Carl Benz", # 19th
		"Alfred Krupp", # 19th
		iModern,
		"Ferdinand Porsche", # 20th
		"August Horch", # 20th
		"fMelitta Bentz", # 20th
	],
	iGreatStatesman : [
		"Immanuel Kant", # 18th
		iIndustrial,
		"Heinrich Friedrich Karl vom Stein", # 19th
		"Klemens von Metternich", # 19th
		"Karl Marx", # 19th
		"fBertha von Suttner", # 19th
		"Wilhelm Liebknecht", # 19th
		"Friedrich Ebert", # 19th
		"fRosa Luxemburg", # 19th
		iModern,
		"Konrad Adenauer", # 20th
		"fHannah Arendt", # 20th
		"Helmut Kohl", # 20th
	],
	iGreatGeneral : [
		u"Otto der Große", # 10th
		iRenaissance,
		"Albrecht von Wallenstein", # 17th
		u"Gebhard Leberecht von Blücher", # 18th
		iIndustrial,
		"Carl von Clausewitz", # 19th
		"Paul von Hindenburg", # 19th
		iModern,
		"Erwin Rommel", # 20th
		"Heinz Guderian", # 20th
	],
},
iCivRussia : {
	iGreatProphet : [
		"Paisiy Yaroslavov", # 15th
		"Feofan Prokopovich", # 18th
		iIndustrial,
		"fHelena Blavatsky", # 19th
		iModern,
		"Nikolai Berdyaev", # 20th
		"Georges Florovsky", # 20th
		"Alexei Losev", # 20th
	],
	iGreatArtist : [
		"Fyodor Dostoyevsky", # 19th
		"Leo Tolstoy", # 19th
		"Pyotr Ilyich Tchaikovsky", # 19th
		"Modest Mussorgsky", # 19th
		"Anton Chekov", # 19th
		iModern,
		"fNatalia Goncharova", # 20th
		"fAnna Pavlova", # 20th
	],
	iGreatScientist : [
		"Mikhail Lomonosov", # 18th
		iIndustrial,
		"Dmitri Mendeleyev", # 19th
		"Nikolai Lobachevsky", # 19th
		iModern,
		"Pavel Cherenkov", # 20th
		"Mikhail Ostrogradsky", # 20th
		"fMaria Kovalevskaya",
	],
	iGreatMerchant : [
		"Afanasiy Nikitin", # 15th
		iRenaissance,
		"Vitus Bering", # 18th
		iIndustrial,
		"Ivan Kruzenshtern", # 19th
	],
	iGreatEngineer : [
		"Ivan Starov", # 18th
		iModern,
		"Sergei Korolev", # 20th
		"Andrey Tupolev", # 20th
		"Leon Theremin", # 20th
		"Vladimir Zworykin", # 20th
		"Igor Sikorsky", # 20th
		"fValentina Tereshkova", # 20th
	],
	iGreatStatesman : [
		"Vladimir Sviatoslavich", # 11th
		"Ivan Vasilyevich", # 15th
		iRenaissance,
		"Vasily Tatishchev", # 18th
		"Nikita Panin", # 18th
		iIndustrial,
		"Mikhail Speransky", # 19th
		"Vladimir Lenin", # 19th
		iModern,
		"Leon Trotsky", # 20th
		"fAlexandra Kollontai", # 20th
	],
	iGreatGeneral : [
		"Alexander Nevsky", # 13th
		"Ivan Grozny", # 15th
		iRenaissance,
		"Mikhail Romanov", # 17th
		"Alexander Suvorov", # 18th
		iIndustrial,
		"Pavel Nakhimov", # 19th
		"Mikhail Skobelev", # 19th
		"fVasilisa Kozhina", # 19th
		"fNadezhda Durova", # 19th
		iModern,
		"Georgy Zhukov", # 20th
		"Vasily Chuikov", # 20th
	],
},
iCivMali : {
	iGreatProphet : [
		"Wali Keita", # 13th
		"Sidi Yahya", # 15th
		iRenaissance,
		"Seku Amadu", # 18th
		"Ali Coulibaly", # 18th
	],
	iGreatArtist : [
		"Nare Maghann Konate", # 13th
		iModern,
		"Lobi Traore", # 20th
		"Ibrahim Aya", # 20th
	],
	iGreatScientist : [
		"Gaoussou Diawara", # 14th
		"Abu al Baraaka", # 12-16th
		iRenaissance,
		"Ahmed Baba", # 16th
		iIndustrial,
		"Ag Mohammed Kawen", # 19th
	],
	iGreatMerchant : [
		"Tunka Manin", # 11th
		"Abubakari", # 13th
		"Abu Bakr ibn Ahmad Biru", # 12-16th
		iModern,
		"Moctar Ouane", # 20th
	],
	iGreatEngineer : [
		"Sakura", # 13th
		"Al-Qadi Aqib ibn Umar", # 13th
		"Abu Es Haq es Saheli", # 14th
		"Mohammed Naddah", # 15th
		iRenaissance,
		"Mohammed Bagayogo", # 16th
	],
	iGreatStatesman : [
		"Askia Muhammad", # 15th
		iRenaissance,
		u"Bitòn Coulibaly", # 18th
		iIndustrial,
		u"Samori Touré", # 19th
		iModern,
		"Modibo Keita", # 20th
		u"Alpha Oumar Konaré", # 20th
	],
	iGreatGeneral : [
		"Sundiata Keita", # 13th
		"Askia Muhammad", # 15th
		"Sunni Ali", # 15th
		iRenaissance,
		"Askia Daoud", # 16th
		"Ngolo Diarra", # 18th
		iIndustrial,
		"fSeh-Dong-Hong-Beh", # 19th
	],
},
iCivPortugal : {
	iGreatProphet : [
		u"António de Lisboa", # 13th
		u"Isabel de Aragão", # 14th
		iRenaissance,
		u"João de Deus", # 16th
		u"João de Brito", # 17th
	],
	iGreatArtist : [
		u"Fernão Lopes", # 15th
		u"Nuno Gonçalves", # 15th
		iRenaissance,
		u"Luís de Camões", # 16th
		u"António Ferreira", # 16th
		u"João de Barros", # 16th
		"Machado de Castro", # 18th
	],
	iGreatScientist : [
		"Garcia de Orta", # 16th
		"Pedro Nunes", # 16th
		"Bartolomeu de Gusmao", # 18th
		"Jacob de Castro Sarmento", # 18th
		iModern,
		"Abel Salazar", # 20th
		u"António Egas Moniz", # 20th
	],
	iGreatMerchant : [
		"Vasco da Gama", # 15th
		"Francisco de Almeida", # 15th
		"Henrique o Navegador", # 15th
		"Bartolomeu Dias", # 15th
		iRenaissance,
		"fGracia Mendes Nasi", # 16th
		u"Pedro Álvares Cabral", # 15th
		u"Fernão Mendes Pinto", # 16th
	],
	iGreatEngineer : [
		"Mateus Fernandes", # 15th
		iRenaissance,
		"Diogo de Boitaca", # 16th
		u"João Antunes", # 17th
		iModern,
		u"Álvaro Siza Vieira", # 20th
	],
	iGreatStatesman : [
		"Henrique de Avis", # 15th
		iRenaissance,
		u"Sebastião José de Carvalho e Melo", # 18th
		iModern,
		"Afonso Costa", # 20th
		u"António de Oliveria Salazar", # 20th
	],
	iGreatGeneral : [
		u"Nuno Álvares Pereira", # 14th
		"Afonso de Albuquerque", # 15th
		"Alvaro Vaz de Almada", # 15th
		iModern,
		"Otelo Saraiva de Carvalho", # 20th
	],
},
iCivInca : {
	iGreatProphet : [
		"Yahuar Huacac", # 14th
	],
	iGreatArtist : [
		"Viracocha", # legendary
		"Ninan Cuyochi", # 16th
		"fPalla Chimpu Ocllo", # 16th
	],
	iGreatScientist : [
		"Sinchi Roca", # 12th
		"Mayta Qhapaq Inka", # 13th
		"Manqu Qhapaq", # 13th
		"Inka Roq'a", # 14th
		"Waskar Inka", # 16th
		"Titu Cusi", # 16th
	],
	iGreatMerchant : [
		"Tupaq Inka Yupanki", # 15th
		"Felipillo", # 16th
	],
	iGreatEngineer : [
		"Qhapaq Yunpanki Inka", # 14th
		"Sayri Tupaq Inka", # 16th
	],
	iGreatStatesman : [
		u"Mayta Cápac", # 14th
		iRenaissance,
		"Manco Inca Yupanqui", # 16th
		"fMama Huaco", # 16th
		u"Tápac Amaru", # 18th
	],
	iGreatGeneral : [
		"Pachakutiq Inka Yupanki", # 15th
		"Atawallpa", # 16th
		"Manqu Inka Yupanki", # 16th
		"Thupaq Amaru", # 16th
		"Chalcuchimaq", # 16th
		"Quisquis", # 16th
		iRenaissance,
		"fBartolina Sisa", # 18th
		iIndustrial,
		"fJuana Azurduy de Padilla", # 19th
	],
},
iCivItaly : {
	iGreatProphet : [
		"Thomas Aquinas", # 13th
		"Francesco d'Assisi", # 13th
		"fGuglielma", # 13th
		"fCaterina di Giacomo di Benincasa", # 14th
		"Giuliano della Rovere", # 15th
		iRenaissance,
		"Camillo Borghese", # 16th
		"Giulio de' Medici", # 16th
	],
	iGreatArtist : [
		"Dante Alighieri", # 13th
		"Giovanni Boccaccio", # 14th
		u"Niccolò Machiavelli", # 15th
		"Donatello", # 15th
		iRenaissance,
		"Michelangelo", # 16th
		"Raphael", # 16th
		"fSofonisba Anguissola", # 16th
		"fArtemisia Gentileschi", # 17th
		iModern,
		"fGrazia Deledda", # 20th
		"Gabriele Trovato", # 20th
		u"Gian Maria Volontè", # Contest Reward
	],
	iGreatScientist : [
		"fTrotula di Salerno", # 12th
		"Francesco Petrarca", # 14th
		"Pico della Mirandola", # 15th
		iRenaissance,
		"Giordano Bruno", # 16th
		"Galileo Galilei", # 16th
		"Luigi Galvani", # 18th
		"Alessandro Volta", # 18th
		"fMaria Gaetana Agnesi", # 18th
		iModern,
		"Enrico Fermi", # 20th
		"fRita Levi-Montalcini", # 20th
	],
	iGreatMerchant : [
		"Marco Polo", # 13th
		"Simone de' Bardi", # 13th
		"Giovanni de' Medici", # 14th
		"Donato Peruzzi", # 14th
		"Ciriaco de Ancona", # 15th
		iRenaissance,
		"fTullia d'Aragona", # 16th
	],
	iGreatEngineer : [
		"Leonardo da Vinci", # 15th
		"Taccola", # 15th
		"Donato Bramante", # 15th
		"Filippo Brunelleschi", # 15th
		iModern,
		"Guglielmo Marconi", # 20th
	],
	iGreatStatesman : [
		u"Niccolò Machiavelli", # 15th
		iRenaissance,
		"fIsabelle d'Este", # 16th
		"Francesco Guicciardini", # 16th
		"Giambattista Vico", # 18th
		"Cesare Beccaria", # 18th
		iIndustrial,
		"Giuseppe Garibaldi", # 19th
		"Giuseppe Mazzini", # 19th
		iModern,
		"Antonio Gramsci", # 20th
	],
	iGreatGeneral : [
		"Enrico Dandolo", # 13th
		"Simone Boccanegra", # 14th
		"Francesco Sforza", # 15th
		iIndustrial,
		"Giuseppe Garibaldi", # 19th
	],
},
iCivMongolia : {
	iGreatProphet : [
		"Abaqa", # 13th
		"Arghun", # 13th
		"Sartaq", # 13th
		iRenaissance,
		"Zanabazar", # 17th
	],
	iGreatArtist : [
		"Oghul Qaimish", # 13th
		"Tolui", # 13th
		"Uzbeg", # 14th
		iModern,
		"Siqin Gaowa", # 20th
	],
	iGreatScientist : [
		"Kaidu", # 13th
		"Ulugh Beg", # 15th
		"Mandukhai", # 15th
		iRenaissance,
		"Nurhaci", # 16th
	],
	iGreatMerchant : [
		"Hulagu", # 13th
		u"Güyük", # 13th
		"Mengu-Timur", # 13th
		"Gaykhatu", # 13th
		iRenaissance,
		"Altan", # 16th
	],
	iGreatEngineer : [
		"Duwa", # 13th
		"Zhang Wenqian", # 13th
		"Toqta", # 14th
		iModern,
		"Li Siguang", # 20th
	],
	iGreatStatesman : [
		"Batu Khan", # 13th
		"Urtu Saqal", # 13th
		"fOrghana", # 13th
		"Ghazan", # 13th
		u"Temür Khan", # 13th
		"Dayan Khan", # 15th
		iIndustrial,
		"Balingiin Tserendorj", # 19th
	],
	iGreatGeneral : [
		"Toghril", # 12th
		"Ogodei", # 13th
		"Chagatai", # 13th
		u"Möngke", # 13th
		"Timur-e Lang", # 14th
	],
},
iCivAztecs : {
	iGreatProphet : [
		"Tenoch", # 14th
		"Tlacateotl", # 15th
		"fPapantzin", # 15th
		"Ixtlilxochitl", # 15th
		"fYacotzin", # 16th
	],
	iGreatArtist : [
		"Techotlalatzin", # 14th
		"Ihuitemotzin", # 16th
	],
	iGreatScientist : [
		"Axayacatl", # 15th
		"Ixtlilxochitl", # 15th
		"Coanacoch", # 16th
	],
	iGreatMerchant : [
		"Cuauhtemoc", # 16th
		"Tlacotzin", # 16th
		"fTechichpotzin", # 16th
	],
	iGreatEngineer : [
		"Jasaw Chan K'awiil", # 8th 
		"Itzcatl", # 15th
		"Tlacaelel", # 15th
		"Moquihuix", # 15th
	],
	iGreatStatesman : [
		"Acamapichtli", # 14th
		"Quaquapitzahuac", # 15th
		"Tezozomoctli", # 15th
		"Nezahualcoyotl", # 15th
		"Nezahualpilli", # 15th
		iModern,
		"fRigoberta Mench&#250;", # 20th
	],
	iGreatGeneral : [
		"Tezozomoc", # 14th
		"Ahuitzotl", # 15th
		"Itzcoatl", # 15th
		"Maxtla", # 15th
		"Huitzilhuitl", # 15th
		"Chimalpopoca", # 15th
	],
},
iCivMughals : {
	iGreatProphet : [
		"Rajah Birbal", # 16th
		"Guru Ram Das", # 16th
		"Guru Arjan", # 16th
		"Hiravijaya ji", # 16th
		"Shah Abdul Latif Bhittai", # 18th
		"Bulleh Shah", # 18th
	],
	iGreatArtist : [
		"fShahzadi Gulbadan Begum", # 16th
		"Abu al-Faiz ibn Mubarak", # 16th
		"Abd al-Samad", # 16th
		"Ustad Mansur", # 17th
	],
	iGreatScientist : [
		"Ali Kashmiri ibn Luqman", # 16th
		"Abu al-Faiz ibn Mubarak", # 16th
		"Abd-ul-Qadir Bada'uni", # 16th
		"Muhammad Salih Tahtawi", # 17th
		"Sawai Jai Singh", # 18th
		iIndustrial,
		"Khwaja Nizam-ud-Din Ahmad", # 19th
	],
	iGreatMerchant : [
		"Sher Shah Suri", # 16th
		"Raja Todar Mal", # 16th
		"Mir Jumla", # 17th
		"Yahya Saleh", # 16th
		"Khan Alam", # 18th
		iModern,
		"Mian Muhammad Mansha", # 20th
	],
	iGreatEngineer : [
		"Fathullah Shirazi", # 16th
		"Ustad Ahmad Lahauri", # 17th
		iModern,
		"Abdur Rahman Hye", # 20th
		"Abdul Qadeer Khan", # 20th
		"Munir Ahmad Khan", # 20th
		"fYasmeen Lari", # 20th
	],
	iGreatStatesman : [
		"fRazia Sultana", # 13th
		iRenaissance,
		"Babur", # 16th
		"Abu'l-Fazl ibn Muhammad", # 16th
		iModern,
		"Muhammad Ali Jinnah", # 20th
		"Choudhry Ali", # 20th
	],
	iGreatGeneral : [
		"Zahir-ud-din Muhammad Babur", # 15th
		"Mir Baqi", # 15th
		"Bayram Khan", # 16th
		"Abul Muzaffar Aurangzeb", # 17th
		"Abudullah Khan Barha", # 18th
		"Ali Vardi Khan", # 18th
		iIndustrial,
		"fBegum Hazrat Mahal", # 19th
	],
},
iCivTurkey : {
	iGreatProphet : [
		"Sheikh Bedreddin", # 14th
		iRenaissance,
		"Sabatai Zevi", # 17th
		"Yaakov Culi", # 18th
		iModern,
		"Mustada Cagrici", # 20th
	],
	iGreatArtist : [
		"Yunus Emre", # 13th
		iRenaissance,
		u"Hayâlî", # 16th
		u"Gül Baba", # 16th
		iModern,
		"Mehmet Akif Ersoy", # 20th
	],
	iGreatScientist : [
		"Qazi Zada", # 14th
		iModern,
		"Cahit Arf", # 20th
		"Oktay Sinanoglu", # 20th
		u"Feza Gürsey", # 20th
		"Aziz Sancar", # 21th
	],
	iGreatMerchant : [
		"Evliya Celebi", # 17th
		iIndustrial,
		u"Abdülmecid", # 19th
		iModern,
		"Hormuzd Rassam", # 20th
		"Nejat Eczacibashi", # 20th
		"Aydin Dogan", # 20th
	],
	iGreatEngineer : [
		"Atik Sinan", # 15th
		"Davud Aga", # 15th
		"Mimar Sinan", # 15th
		iModern,
		"Ekmel Ozbay", # 20th
	],
	iGreatStatesman : [
		"Sheikh Edebali", # 13th
		iRenaissance,
		"Pargali Ibrahim Pasha", # 16th
		"Sokollu Mehmet Pasha", # 16th
		iModern,
		u"Ismet Inönü", # 20th
		u"Süleyman Demirel", # 20th
	],
	iGreatGeneral : [
		"Orhan", # 14th
		iRenaissance,
		"Hayreddin Barbarossa", # 16th
		"Selim", # 16th
		"Turgut Reis", # 16th
		"Kara Mustafa Pasha", # 17th
		iModern,
		"Ismail Enver", # 20th
	],
},
iCivNetherlands : {
	iGreatProphet : [
		"Geert Grote", # 14th
		iRenaissance,
		"Desiderius Erasmus", # 16th
		"Baruch Spinoza", # 17th
		iIndustrial,
		"Abraham Kuyper", # 19th
		"fAletta Jacobs", # 19th
		iModern,
		"fAlida Bosshardt", # 20th
	],
	iGreatArtist : [
		"Hendrick de Keyser", # 16th
		"Rembrandt van Rijn", # 17th
		"Johannes Vermeer", # 17th
		"Pieter Corneliszoon Hooft", # 17th
		"fTitia Bergsma", # 18th
		iIndustrial,
		"Vincent van Gogh", # 19th
	],
	iGreatScientist : [
		"Willebrord Snel van Royen", # 16th
		"Christiaan Huygens", # 17th
		"Antonie van Leeuwenhoek", # 17th
		"Govert Bidloo", # 17th
		"fAnna Maria van Schurman", # 18th
		iModern,
		"Jan Hendrik Oort", # 20th
		"Gerrit Pieter Kuiper", # 20th
	],
	iGreatMerchant : [
		"Willem Barentsz", # 16th
		"Cornelis de Houtman", # 16th
		"fKenau Simonsdochter Hasselaer", # 16th
		"Antony van Diemen", # 17th
		"Abel Tasman", # 17th
		"Pieter Stuyvesant", # 17th
		"Jan van Riebeeck", # 17th
		"Jan Coen", # 17th
		iIndustrial,
		"Clemens Brenninkmeijer", # 19th
		"August Kessler", # 19th
		iModern,
		"Freddy Heineken", # 20th
	],
	iGreatEngineer : [
		"Simon Stevin", # 16th
		"Cornelis Corneliszoon", # 16th
		"Jan Leeghwater", # 17th
		iIndustrial,
		"Adolphe Sax", # 19th
		iModern,
		"Frits Philips", # 20th
	],
	iGreatStatesman : [
		"Desiderius Erasmus", # 16th
		"Johan van Oldenbarnevelt", # 16th
		"Johan de Witt", # 17th
		"Adriaen van der Donck", # 17th
		"Hugo Grotius", # 17th
		"Cornelis de Graeff", # 17th
		iIndustrial,
		"Johan Thorbecke", # 19th
		"Cornelis Lely", # 19th
		iModern,
		"Willem Drees", # 20th
	],
	iGreatGeneral : [
		"Maurits van Nassau", # 16th
		"Michiel de Ruyter", # 17th
		"Frederik Hendrik", # 17th
		"Cornelis Tromp", # 17th
		iIndustrial,
		"Henri Winkelman", # 20th
	],
},
iCivAmerica : {
	iGreatProphet : [
		"Roger Williams", # 17th
		"fAnne Hutchinson", # 17th
		"William Penn", # 18th
		"Jonathan Edwards", # 18th
		"fAnn Lee", # 18th
		iIndustrial,
		"Joseph Smith", # 19th
	],
	iGreatArtist : [
		"Edgar Allan Poe", # 19th
		"Mark Twain", # 19th
		"fEmily Dickinson", # 19th
		"Herman Melville", # 19th
		"fMary Cassatt", # 19th
		iModern,
		"Ernest Hemingway", # 20th
		"Charlie Chaplin", # 20th
		"Elvis Presley", # 20th
		"fHarper Lee", # 20th
		"Miles Davis", # 20th
		"Jimi Hendrix", # 20th
	],
	iGreatScientist : [
		"fNettie Stevens", # 19th
		iModern,
		"Arthur Compton", # 20th
		"Edwin Hubble", # 20th
		"John von Neumann", # 20th
		"Glenn Seaborg", # 20th
		"Robert Oppenheimer", # 20th
		"Richard Feynman", # 20th
		"fBarbara McClintock", # 20th
		"fGrace Hopper", # 20th
	],
	iGreatMerchant : [
		"Cornelius Vanderbilt", # 19th
		"John D. Rockefeller", # 19th
		"Andrew Carnegie", # 19th
		"fHetty Green", # 19th
		iModern,
		"fHelena Rubinstein", # 20th
		"William Edward Boeing", # 20th
		"Bill Gates", # 20th
	],
	iGreatEngineer : [
		"Benjamin Franklin", # 18th
		"Thomas Edison", # 19th
		"Nichola Tesla", # 19th
		"Henry Ford", # 19th
		"Charles Goodyear", # 19th
		iModern,
		"Orville Wright", # 20th
		"fLillian Moller Gilbreth", # 20th
		"fHedy Lamarr", # 20th
		"fMargaret Hutchinson Rousseau", # 20th
	],
	iGreatStatesman : [
		"Thomas Paine", # 18th
		"Thomas Jefferson", # 18th
		"Benjamin Franklin", # 18th
		iIndustrial,
		"Andrew Jackson", # 19th
		"Frederick Douglass", # 19th
		"fSojourner Truth", # 19th
		"fVictoria Claflin Woodhull", # 19th
		"fJane Addams", # 19th
		iModern,
		"fEleanor Roosevelt", # 20th
		"George Kennan", # 20th
	],
	iGreatGeneral : [
		"Andrew Jackson", # 19th
		"Ulysses S. Grant", # 19th
		"Robert E. Lee", # 19th
		iModern,
		"Dwight D. Eisenhower", # 20th
		"George Patton", # 20th
		"Douglas MacArthur", # 20th
	],
},
iCivIran : {
	iGreatProphet : [
		"Mulla Sadra", # 16th
		"Muhammad Baqir Majlisi", # 17th
		"Muhammad Baqir Behbahani", # 18th
		iIndustrial,
		u"Bahá'u'lláh", # 19th
		u"Báb", # 19th
		iModern,
		"Ayatollah Mohammad Taqi", # 20th
	],
	iGreatArtist : [
		"Shaykh-i Baha'i", # 16th
		"Reza Abbasi", # 16th
		"Ustad Mirza Shirazi", # 18thth
		iIndustrial,
		"Mihr 'Ali", # 19th
		iModern,
		"fForough Farrokhzad", # 20th
		"Hossein Amanat", # 20th
		"fHayedeh", # 20th
	],
	iGreatScientist : [
		"Al-Birjandi", # 16th
		"Qazi Sa'id Qumi", # 17th
		"Alavi Shirazi", # 17th
		iModern,
		"Mahmoud Hessaby", # 20th
		"Ali Javan", # 20th
		"Cumrun Vafa", # 20th
	],
	iGreatMerchant : [
		"Manny Mashouf", # 20th
		"Nasser David Khalili", # 20th
		"Omid Kordestani", # 20th
		"Amir Ansari", # 20th
		"Pierre Omidyar", # 20th
	],
	iGreatEngineer : [
		"Firouz Naderi", # 20th
		"Gholam Reza Aghazadeh", # 20th
		"Caro Lucas", # 20th
		"Siavash Alamouti", # 20th
		"fAnousheh Ansari", # 20th
	],
	iGreatStatesman : [
		"Ismail", # 15th
		"Tahmasp", # 16th
		iIndustrial,
		"Ebrahim Khan Kalantar", # 19th
		"Kuchik Khan", # 19th
		"Amir Kabir", # 19th
		iModern,
		"Reza Shah Pahlavi", # 20th
		"Mohammad Mossadegh", # 20th
	],
	iGreatGeneral : [
		"Abbas I", # 16th
		"Mohammad Khan Qajar", # 18th
		iIndustrial,
		"Ahmad Amir-Ahmadi", # 19th
		iModern,
		"Bahram Aryana", # 20th
		"Muhammad-Husayn Ayrom", # 20th
		"Ali-Reza Asgari", # 20th
		"Mohammad Ali Jafari", # 20th
	],
},
iCivTibet : {
	iGreatProphet : [
		"Gendun Drup", # 15th
		"Gendun Gyatso", # 15-16th
		"Sonam Gyatso", # 16th
		"Yonten Gyatso", # 16-17th
		"Tsangyang Gyatso", # 17th
		iModern,
		"Tenzin Gyatso", # 20th
	],
},
iCivPoland : {
	iGreatProphet : [
		"Wojciech", # 10th
		"Stanislaw", # 11th
		"fJadwiga", # 14th
		iModern,
		"Karol Wojtyla", # 20th
	],
	iGreatArtist : [
		"Jan Matejko", # 19th
		"Fryderyk Chopin", # 19th
		iModern,
		"Witold Lutoslawski", # 20th
	],
	iGreatScientist : [
		"Witelo", # 13th
		iRenaissance,
		"Mikolaj Kopernik", # 16th
		"Jan Brozek", # 17th
		"Stanislaw Staszic", # 18th
		"fMaria Sklodowska", # 19th
	],
	iGreatMerchant : [
		"Leopold Kronenberg", # 19th
		iModern,
		"Jan Kulczyk", # 20th
	],
	iGreatEngineer : [
		"Ignacy Lukasiewicz", # 19th
		iModern,
		"Kasimiersz Proszynski", # 20th
		"Tadeusz Sendzimir", # 20th
	],
	iGreatStatesman : [
		"Wladyslaw Lokietek", # 14th
		iRenaissance,
		"Andrzej Frycz Modrzewski", # 16th
		"Jan Zamoyski", # 16th
		"Stanislaw Staszic", # 18th
		iModern,
		"Ignacy Daszynski", # 20th
		"Jozef Pilsudski", # 20th
		"Wladyslaw Sikorski", # 20th
		"Lech Walesa", # 20th
	],
	iGreatGeneral : [
		"Wladyslaw Jagiello", # 15th
		"Jan Tarnowski", # 16th
		"Tadeusz Kosciuszko", # 18th
		iIndustrial,
		"fEmilia Plater", # 19th
		iModern,
		"Wladyslaw Sikorski", # 20th
	],
},
iCivCongo : {
	iGreatStatesman : [
		"Mwata Yamvo", # 16th
		"Ng'anga Bilonda", # 16th
		"Kalala Ilunga", # 17th
		iIndustrial,
		"Msiri", # 19th
		iModern,
		"Patrice Lumumba", # 20th
		"Joseph Kasa-Vubu", # 20th
	],
},
iCivArgentina : {
	iGreatProphet : [
		"Gauchito Gil", # 19th
		iModern,
		"Jorge Mario Bergoglio", # 20th
	],
	iGreatArtist : [
		"Jose Hernandez", # 19th
		iModern,
		"Carlos Gardel", # 20th
		"fGabriela Mistral", # 20th
		u"fEva Perón", # 20th
		"Jorge Luis Borges", # 20th
		"Antonio Berni", # 20th
		"Daniel Barenboim", # 20th
		u"Juan José Campanella", # 20th
		"Gustavo Cerati", # 20th
	],
	iGreatScientist : [
		"Francisco Moreno", # 19th
		iModern,
		"Luis Federico Leloir", # 20th
		u"László Bíró", # 20th
		u"René Favaloro", # 20th
	],
	iGreatMerchant : [
		"Juan Las Heras", # 19th
		iModern,
		u"José ber Gelbard", # 20th
		"Roberto Alemann", # 20th
		"Jorge Wehbe", # 20th
		"Aldo Ferrer", # 20th
		"Antonio Cafiero", # 20th
	],
	iGreatEngineer : [
		"Luis Huergo", # 19th
		iModern,
		"Amancio Williams", # 20th
		u"César Pelli", # 20th
		"Clorindo Testa", # 20th
	],
	iGreatStatesman : [
		"Estanislao Zeballos", # 19th
		iModern,
		"Carlos Saavedra Lamas", # 20th
		"Juan Atilio Bramuglia", # 20th
		"fEstela Barnes de Carlotto", # 20th
	],
	iGreatGeneral : [
		"Cornelio Saavedra", # 18th
		"Manuel Belgrano", # 18th
		u"Juan José Castelli", # 18th
		u"Martín Miguel de Güemes", # 18th
		u"José Gervasio Artigas", # 19th
	],
},
iCivBrazil : {
	iGreatProphet : [
		u"António Conselheiro", # 19th
		iModern,
		u"Hélder Câmara", # 20th
		u"fIrmã Dulce Pontes", # 20th
		"Chico Xavier", # 20th
		"Edir Macedo", # 20th
	],
	iGreatArtist : [
		"Aleijadinho", # 18th
		u"António Carlos Gomes", # 19th
		"Machado de Assis", # 19th
		iModern,
		"fTarsila do Amaral", # 20th
		"fCarmen Miranda", # 20th
		"Tom Jobim", # 20th
		"Romero Britto", # 20th
	],
	iGreatScientist : [
		"Oswaldo Cruz", # 19th
		"Carlos Chagas", # 19th
		iModern,
		"Alberto Santos-Dumont", # 20th
		"Urbano Ernesto Stumpf", # 20th
		u"Aziz Ab'Sáber", # 20th
		"Marcelo Gleiser", # 20th
	],
	iGreatMerchant : [
		"Roberto Marinho", # 20th
		"Jorge Lemann", # 20th
		"Eike Batista", # 20th
	],
	iGreatEngineer : [
		u"André Rebouças", # 19th
		iModern,
		u"Cândido Rondon", # 20th
		"Oscar Niemeyer", # 20th
		"Norberto Odebrecht", # 20th
	],
	iGreatStatesman : [
		u"José Bonifácio de Andrada", # 18th
		iIndustrial,
		"Rodrigo Augusto da Silva", # 19th
		u"José Paranhos", # 19th
		u"Isabel Bragança", # 19th
		"Miguel Reale", # 19th
		iModern,
		"Roberto Mangabeira Unger", # 20th
	],
	iGreatGeneral : [
		u"Luís Alves de Lima e Silva", # 19th 
		"Joaquim Marques Lisboa", # 19th
		u"fMaria Quitéria", # 19th
		iModern,
		u"João Baptista Mascarenhas de Morais", # 20th
		"Eurico Gaspar Dutra", # 20th
		"Artur da Costa e Silva", # 20th
	],
},
iCivColombia : {
	iGreatProphet : [
		u"Félix Restrepo Mejía", # 20th
		"Camilo Torres Restrepo", # 20th
		u"Alfonso López Trujillo", # 20th
		u"Julio Enrique Dávila", # 20th
		u"fMaría Luisa Piraquive", # 20th
		u"César Castellanos", # 20th
	],
	iGreatArtist : [
		"Gabriel Garcia Marquez", # 20th
		"Rodrigo Arenas", # 20th
		u"Álvaro Mutis", # 20th
		"Fernando Botero", # 20th
		"Rafael Orozco", # 20th
		"Rodrigo Garcia", # 20th
		"fShakira", # 20th
	],
	iGreatScientist : [
		u"José Jéronimo Triana", # 19th
		"Julio Garavito Armero", # 19th
		iModern,
		u"Rodolfo Llinás", # 20th
		"Jorge Reynolds Pombo", # 20th
	],
	iGreatMerchant : [
		"Julio Mario Santo Domingo", # 20th
		u"Carlos Ardila Lülle", # 20th
		"Luis Carlos Sarmiento Angulo", # 20th
	],
	iGreatEngineer : [
		"Rogelio Salmona", # 20th
	],
	iGreatStatesman : [
		u"Rafael Núñez", # 19th
		iModern,
		"Jorge Eliécer Gaitán", # 20th
		u"Nicolás Gómez Dávila", # 20th
		u"Mario Lanserna Pinzón", # 20th
	],
	iGreatGeneral : [
		"fAntonia Santos", # 19th
		u"Antonio Nariño", # 19th
		"Francisco de Paula Santander", # 19th
	],
},
iCivMexico : {
	iGreatProphet : [
		"Juan Diego", # 16th
		"Francisco Javier Clavijero", # 18th
		u"Cristóbal Magallanes Jara", # 19th
		iModern,
		u"Rafael Guízar Valencia", # 20th
		"Miguel Pro", # 20th
		"Samuel Ruiz", # 20th
		u"Javier Lozano Barragán", # 20th
	],
	iGreatArtist : [
		u"fÁngela Peralta", # 19th
		iModern,
		u"José Clemente Orozco", # 20th
		"Diego Rivera", # 20th
		"fFrida Kahlo", # 20th
		"Octavio Paz", # 20th
		"fRemedios Varo", # 20th
		u"fDolores del Río", # 20th
		"Pedro Infante", # 20th
		"Carlos Fuentes", # 20th
		u"Vicente Fernández", # 20th
	],
	iGreatScientist : [
		"Gabino Barreda", # 19th
		u"Lucas Alamán", # 19th
		iModern,
		"Manuel Sandoval Vallarta", # 20th
		"Ricardo Miledi", # 20th
		u"Mario José Molina", # 20th
		"Rodolfo Neri Vela", # 20th
	],
	iGreatMerchant : [
		u"Víctor Urquidi", # 20th
		u"Jerónimo Arango", # 20th
		"Carlos Slim", # 20th
		"Everardo Elizondo", # 20th
		u"Alberto Baillères", # 20th
		u"Emilio Azcárraga Jean", # 20th
	],
	iGreatEngineer : [
		u"José Villagrán García", # 20th
		u"Luis Barragán", # 20th
		"Juan O'Gorman", # 20th
		"Mario Pani", # 20th
		u"Pedro Ramírez Vázquez", # 20th
		"Bernardo Quintana Arrioja", # 20th
	],
	iGreatStatesman : [
		u"José María Pino Suárez", # 19th
		"Pascual Orozco", # 19th
		iModern,
		u"José Vasconcelos", # 20th
		"Octavio Paz", # 20th
		"fElvia Carrillo Puerto", # 20th
		"fRosario Castellanos", # 20th
		u"Alfonso García Robles", # 20th
		u"Gilberto Bosques Saldívar", # 20th
	],
	iGreatGeneral : [
		"Miguel Hidalgo", # 18th
		u"Agustín de Iturbide", # 19th
		u"fJosefa Ortiz de Domínguez", # 19th
		u"Porfirio Díaz", # 19th
		"Pancho Villa", # 19th
		"Emiliano Zapata Salazar", # 19th
	],
},
iCivCanada : {
	iGreatProphet : [
		u"André Bessette", # 19th
	],
	iGreatArtist : [
		"Tom Thomson", # 19th
		iModern,
		"Lawren Harris", # 20th
		"Emily Carr", # 20th
		"Neil Young", # 20th
	],
	iGreatScientist : [
		"Frederick Banting", # 20th
		"Norman Bethune", # 20th
		"Andrew McNaughton", # 20th
		"fShirley Tilghman", # 20th
		"Ted Rogers", # 20th
		"David Suzuki", # 20th
	],
	iGreatMerchant : [
		"Timothy Eaton", # 19th
		iModern,
		"fElizabeth Arden", # 20th
		u"Guy Laliberté", # 20th
	],
	iGreatEngineer : [
		"Sandford Fleming", # 19th
		"William Cornelius Van Horne", # 19th
		iModern,
		"Joseph-Armand Bombardier", # 20th
		"fElsie MacGill", # 20th
	],
	iGreatStatesman : [
		"John A Macdonald", # 19th
		u"George-Étienne Cartier", # 19th
		"Louis Riel", # 19th
		iModern,
		"Lester B Pearson", # 20th
		"fEmily Murphy", # 20th
		"fNellie McClung", # 20th
		"Rene Levesque", # 20th
		"Romeo Dallaire", # 20th
	],
	iGreatGeneral : [
		"Arthur Currie", # 19th
	],
},
}

setup()