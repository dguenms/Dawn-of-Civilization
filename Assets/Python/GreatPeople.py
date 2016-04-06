# encoding: utf-8

from CvPythonExtensions import *
from Consts import *
from RFCUtils import utils

gc = CyGlobalContext()
localText = CyTranslator()

lTypes = [iGreatProphet, iGreatArtist, iGreatScientist, iGreatMerchant, iGreatEngineer, iGreatStatesman, iGreatGeneral, iGreatSpy]

lGreatPeople = [[[] for j in lTypes] for i in range(iNumCivilizations)]
lOffsets = [[tuple(0 for i in range(iNumEras)) for j in lTypes] for i in range(iNumCivilizations)]

def testunit(iPlayer, iUnit):
	unit = gc.getPlayer(iPlayer).initUnit(utils.getUniqueUnit(iPlayer, iUnit), 0, 0, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	print getName(unit)
	
def create(iPlayer, iUnit, (x, y)):
	gc.getPlayer(iPlayer).createGreatPeople(utils.getUniqueUnit(iPlayer, iUnit), True, True, x, y)

def getAlias(iCiv, iType):
	if iCiv in [iCivHarappa, iCivTamils]: return iCivIndia
	elif iCiv == iCivHolyRome: return iCivGermany
	elif iCiv == iCivMaya: return iCivAztec
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
	
	iSpread = max(iNextOffset - iOffset, iEra+1)
	
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
				
	print lGreatPeople

		
dGreatPeople = {
iCivChina : {
	iGreatProphet : [
		"Lao Tzu", # 6th BC
		"Kong Fuzi", # 5th BC 
		"Meng Zi", # 4th BC 
		"Zhuangzi", # 4th BC 
		"Han Fei", # 3rd BC 
		"fLin Moniang", # 10th 
		"fSun Bu'er", # 12th 
	],
	iGreatArtist : [
		"Ling Lun", # legendary 
		"Su Shi", # 11th BC 
		"Li Bo", # 8th BC 
		"Du Fu", # 8th BC 
		"Wang Xizhi", # 4th BC 
		"fCai Wenji", # 1st 
		"fShangguan Wan'er", # 7th 
	],
	iGreatScientist : [
		"Li Fan", # 1st 
		"fBan Zhao", # 1st 
		"Liu Hui", # 3rd 
		"Zu Chongzhi", # 5th 
		"Zhu Shijie", # 14th 
		"fTan Yunxian", # 16th 
		"Li Yuanzhe", # 20th 
		"Chen Ning Yang", # 20th 
	],
	iGreatMerchant : [
		"Zhang Qian", # 2nd BC 
		"Xuanzang", # 7th 
		"Wang Anshi", # 11th 
		"Zheng He", # 15th 
		"Deng Xiaoping", # 20th 
	],
	iGreatEngineer : [
		"fLeizu", # 27th BC 
		"Cai Lun", # 1st 
		"Zhang Heng", # 2nd 
		"Bi Sheng", # 11th 
		"Li Siguang", # 20th 
		"fWu Jianxiong", # 20th 
	],
	iGreatStatesman : [
		"Li Si", # 3rd BC 
		"Xiao He", # 2nd BC 
		"Fang Yuanling", # 7th 
		"Di Renjie", # 7th 
		"Zhang Juzheng", # 16th 
		"Li Hongzhang", # 19th 
		"Sun Yat-sen", # 19th 
		"Zhou Enlai", # 20th 
	],
	iGreatGeneral : [
		"Sun Tzu", # 6th BC 
		"Cao Cao", # 2nd 
		"Zhuge Liang", # 3rd 
		"fPingyang Gongzhu", # 7th 
		"Guo Ziyi", # 8th 
		"Shi Lang", # 17th 
		"fChing Shih", # 19th 
		"Zhang Zuolin", # 20th 
	],
},
iCivIndia : {
	iGreatProphet : [
		"Mahavira", # 6th BC 
		"Siddharta Gautama", # 6th BC 
		"Ananda", # 6th BC 
		"Mahakashyapa", # 6th BC 
		"Adi Shankara", # 9th 
		"Atisha", # 11th 
		"fMeera", # 16th 
		"Tipu Sultan", # 18th 
		"fAnjeze Gonxhe Bojaxhiu", # 20th 
	],
	iGreatArtist : [
		"Kalidasa", # 5th BC 
		"Valmiki", # 4th BC 
		"Basawan", # 16th 
		"Raja Rao", # 20th 
		"Rabindranath Tagore", # 20th 
	],
	iGreatScientist : [
		"Aryabhata", # 5th 
		"Brahmagupta", # 7th 
		"Bhaskara", # 12th 
		"Madhava", # 14th 
		"Nilakantha Somayaji", # 15th 
		"Kamalakara", # 17th 
		"fAsima Chatterjee", # 20th 
	],
	iGreatMerchant : [
		"Todar Mal", # 16th 
		"Shah Jahan", # 17th 
		"Jamshetji Tata", # 19th 
		"Ardeshir Godrej", # 19th 
		"fIndra Nooyi", # 20th 
	],
	iGreatEngineer : [
		"Baudhayana", # 8th BC 
		"Lagadha", # 1st 
		"Jagadish Chandra Bose", # 19th 
		"Chandrasekhara Venkata Raman", # 20th 
	],
	iGreatStatesman : [
		"Chanakya", # 4th BC 
		"Rajaraja Chola", # 10th 
		"Krishna Devaraya", # 16th 
		"Shivaji Bhosle", # 17th 
		"Tipu Sultan", # 18th 
		"Ram Mohan Roy", # 19th 
		"Ranjit Singh", # 19th 
	],
	iGreatGeneral : [
		"Chandragupta Maurya", # 4th BC 
		"Samudragupta", # 4th BC 
		"Rajaraja Chola", # 12th 
		"fRani Durgavati", # 16th 
		"Shivaji Bhosle", # 17th 
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
		"Nabopolassar", # 7th BC 
	],
	iGreatStatesman : [
		"Urukagina", # 24th BC 
		"Ur-Nammu", # 21st BC 
		"Bilalama", # 20th BC 
		"Lipit-Ishtar", # 19th BC 
		"fShammuramat", # 9th BC 
	],
	iGreatGeneral : [
		"Tiglath-Pileser", # 10th BC 
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
		"Eleftherios Venizelos", # 19th AD 
	],
	iGreatGeneral : [
		"Hektor", # legendary 
		"Leonidas", # 6th BC 
		"Themistokles", # 5th BC 
		"Lysandros", # 5th BC 
		"Philippos", # 4th BC 
		"Pyrrhos", # 3rd BC 
		"fArtemisia", # 4th 
	],
},
iCivCarthage : {
	iGreatProphet : [
		"Acherbas", # legendary 
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
		"Mani", # 3rd 
		"Mazdak", # 4th 
		"Al-Ghazali", # 11th 
		"Mevlana", # 13th 
		"Mulla Sadra", # 17th 
	],
	iGreatArtist : [
		"Firdausi", # 10th 
		"fRabia Balkhi", # 10th 
		"Safi al-Din", # 13th 
		"Saadi", # 13th 
		"Kamal ud-Din Behzad", # 15th 
		"Reza Abbasi", # 16th 
	],
	iGreatScientist : [
		"Ardashir", # 4th 
		"Al-Khwarizmi", # 9th 
		"Al-Razi", # 9th 
		"Ibn Sina", # 10th 
		"Abd al-Rahman al-Sufi", # 10th 
		"Al-Farisi", # 13th 
	],
	iGreatMerchant : [
		"Kavadh", # 5th 
		"Ahmad ibn Rustah", # 10th 
		"Istakhri", # 10th 
	],
	iGreatEngineer : [
		"Artaxerxes", # 5th BC 
		"Bahram", # 3rd 
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
		"Takuan Soho", # 17th 
		"Uchimura Kanzo", # 19th 
	],
	iGreatArtist : [
		"fMurasaki Shikibu", # 10th 
		"Saigyo Hoshi", # 12th 
		"Kano Eitoku", # 16th 
		"Toshusai Sharaku", # 18th 
		"Katsushika Hokusai", # 18th 
		"Utagawa Hiroshige", # 19th 
		"Toro Okamoto", # Contest Reward 
	],
	iGreatScientist : [
		"Yoshida Mitsuyoshi", # 17th 
		"Aida Yasuaki", # 18th 
		"Kiyoshi Ito", # 20th 
		"Hideki Yukawa", # 20th 
		"Masatoshi Koshiba", # 20th 
		"Kenkichi Iwasawa", # 20th 
	],
	iGreatMerchant : [
		"Torakusu Yamaha", # 19th 
		"Otano Kozui", # 19th 
		"Masahisa Fujita", # 20th 
		"Kiichiro Toyoda", # 20th 
		"Soichiro Honda", # 20th 
		"Yoshitaka Fukuda", # 20th 
	],
	iGreatEngineer : [
		"Tanaka Hisashige", # 19th 
		"Katayama Tokuma", # 19th 
		"Takeda Ayasaburo", # 19th 
		"Kotaro Honda", # 20th 
		"Ken Sakamura", # 20th 
		"Kyota Sugimoto", # 20th 
		"Hidetsugu Yagi", # 20th 
		"Shigeru Miyamoto", # 20th 
	],
	iGreatStatesman : [
		"Shoutouku Taishi", # 6th 
		"Taira no Kiyomori", # 12th 
		"Tokugawa Ieyasu", # 16th 
		"Arai Hakuseki", # 17th 
		"Sakamoto Ryouma", # 19th 
		"Oukubo Toshimichi", # 19th 
		"Shigeru Yoshida", # 20th 
	],
	iGreatGeneral : [
		"Fujiwara no Kamatari", # 7th 
		"Minamoto no Yoritomo", # 12th 
		"Ashikaga Takauji", # 14th 
		"Toyotomi Hideyoshi", # 16th 
		"fNakano Takeko", # 19th 
		"Togo Heihachiro", # 19th 
		"Isoroku Yamamoto", # 20th 
		"Tomoyuki Yamashita", # 20th 
	],
},
iCivEthiopia : {
	iGreatProphet : [
		"Gabra Manfas Qeddus", # legendary 
		"Yared", # 6th 
		"Ewostatewos", # 14th 
		"Abba Samuel", # 14th 
		"Abune Tewophilos", # 20th 
	],
	iGreatArtist : [
		"Gebre Kristos Desta", # 19th 
		"Tsegaye Gabre-Medhin", # 20th 
		"Adamu Tesfaw", # 20th 
		"Afeworq Tekle", # 20th 
		"Alexander Boghossian", # 20th 
	],
	iGreatScientist : [
		"Abba Bahrey", # 16th 
		"Aklilu Lemma", # 20th 
		"Kitaw Ejigu", # 20th 
		"Sossina Haile", # 20th 
		"Gebisa Ejeta", # 20th 
	],
	iGreatMerchant : [
		"Nigiste Saba", # legendary 
		"Berhanu Nega", # 20th 
		"Eleni Gebre-Medhin", # 20th 
		"Mohammed Al Amoudi", # 20th 
	],
	iGreatEngineer : [
		"Ezana", # 4th 
		"Gebre Mesqel Lalibela", # 13th 
		"Alam Sagad", # 17th 
	],
	iGreatStatesman : [
		"Ezana", # 4th 
		"Susenyos", # 17th 
		"Tewodros", # 19th 
		"Menelik", # 19th 
		"Mengistu Haile Mariam", # 20th 
	],
	iGreatGeneral : [
		"fGudit", # 10th 
		"Yekuno Amlak", # 13th 
		"Amda Seyon", # 14th 
		"Eskender", # 15th 
		"Tewodros", # 15th 
		"Iyasu", # 17th 
		"Yohannes", # 19th 
	],
},
iCivKorea : {
	iGreatProphet : [
		"Jinul", # 12th 
		"Uicheon", # 12th 
		"Baegun", # 13th 
		"fHeo Nanseolheon", # 16th 
	],
	iGreatArtist : [
		"Damjing", # 7th 
		"Yi Nyeong", # 9th 
		"Yi Je-hyeon", # 9th 
		"Hwang Jip-jung", # 16th 
		"Yan Duseo", # 17th 
		"Kim Hong-do", # 18th 
		"Jeong Seon", # 18th 
		"Shin Yun-bok", # 18th 
	],
	iGreatScientist : [
		"Uisan", # 7th 
		"Wonhyo", # 7th 
		"Jeong Inji", # 15th 
		"Seong Sammun", # 15th 
		"Yu Seong-won", # 15th 
		"Heo Jun", # 16th 
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
		"Jang Yeong-sil", # 15th 
		"Song I-yeong", # 16th 
	],
	iGreatStatesman : [
		"Myeongnim Dap-bo", # 2nd 
		"fSeondeok", # 7th 
		"Kim Bu-sik", # 12th 
		"Yi Hwang", # 16th 
		"Kim Ok-gyun", # 19th 
		"fMyeongseong", # 19th 
		"Kim Gu", # 20th 
		"Kim Dae-jung", # 20th 
	],
	iGreatGeneral : [
		"Gang Gam-chan", # 11th 
		"Choe Woo", # 13th 
		"Yi Seong-gye", # 14th 
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
		"Johan Nordahl Brun", # 18th 
		"Hans Christian Andersen", # 19th 
		"Olav Duun", # 19th 
		"Johan Ludvig Runeberg", # 19th finnish 
		"fJohanna Maria Lind", # 19th 
		"fAstrid Lindgren", # 20th 
	],
	iGreatScientist : [
		"Tycho Brahe", # 16th 
		"fSophia Brahe", # 16th 
		"Mikael Agrocola", # 16th finnish 
		u"Ole Rømer", # 17th 
		"Anders Celsius", # 18th swedish 
		"Johannes Rydberg", # 19th swedish 
		"Anders Angstrom", # 19th swedish 
		"Niels Bohr", # 20th 
	],
	iGreatMerchant : [
		"Eirikr Raudhi", # 10th 
		"Leifr Eiriksson", # 10th 
		"Haakon Sigurdsson", # 10th 
		"Ingvar Kamprad", # 20th swedish 
		"Roald Amundsen", # 20th 
	],
	iGreatEngineer : [
		"Hercules von Oberberg", # 16th 
		"Niels Abel", # 19th 
		"Alfred Nobel", # 19th swedish 
		"Ivar Giaever", # 20th 
	],
	iGreatStatesman : [
		"Gorm den Gamle", # 10th 
		"Erik den Helige", # 11th 
		"fMargrete", # 14th 
		"Gustav Vasa", # 16th 
		"NFS Grundtvig", # 19th 
		u"Dag Hammarskjöld", # 20th 
	],
	iGreatGeneral : [
		u"Eiríkr Blóðøx", # 10th 
		u"Harald Harðráði", # 11th 
		"Knutr", # 11th 
		"Birger Jarl", # 13th swedish 
		"Gustav Vasa", # 16th swedish 
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
		"Muhammad ibn Saud", # 18th 
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
		"Ahmah al-Mansur", # 16th 
	],
},
iCivKhmer : {
	iGreatProphet : [
		"Kirtipandita", # 10th x 
		"Tamalinda", # 12th 
		"Chuon Nath", # 19th 
		"Maha Ghosananda", # 20th 
	],
	iGreatArtist : [
		"Thammaracha", # 16th 
		"Ang Duong", # 19th 
		"Vann Nath", # 20th 
		"Chath Piersath", # 20th 
		"Chhim Sothy", # 20th 
	],
	iGreatScientist : [
		"Jayavarman", # 10th 
		"fSaptadevakula Prana", # 10th 
		"Krisana Kraisintu", # 20th 
		"Shaiwatna Kupratakul", # 20th 
	],
	iGreatMerchant : [
		"Srindravarman", # 14th 
		"Uthong", # 14th 
		"fDaun Penh", 
		"Chey Chettha", # 16th 
		"Srei Meara", # 17th 
		"Teng Bunma", # 20th 
	],
	iGreatEngineer : [
		"Indravarman", # 9th 
		"Yasovarman", # 9th 
		"fJahavi", # 10th 
		"Vann Molyvann", # 20th 
	],
	iGreatStatesman : [
		"Jayavarman", # 9th 
		"Harshavarman", # 10th 
		"Norodom", # 19th 
		"Tou Samouth", # 20th 
	],
	iGreatGeneral : [
		"fTrieu Thi Trinh", # 3rd 
		"Bhavavarman", # 6th 
		"Vinyanandana", # 9th 
		"Rajendravarman", # 10th 
		"Sak Sutsakhan", # 20th 
		"Dien Del", # 20th 
	],
},
iCivIndonesia : {
	iGreatProphet : [
		"Batara Guru Dwipayana",
		"Buddha Pahyien",
		"Sakyakirti",
		"fGayatri Rajapatni", # 14th 
		"Sunan Giri", # 15th 
		"Sunan Gunung Jati", # 16th 
	],
	iGreatArtist : [
		"Asep Sunandar Sunarya",
		"I Made Sidia",
	],
	iGreatScientist : [
		"Jayabaya",
		"Empu Tantular",
	],
	iGreatMerchant : [
		"Cri Kahulunnan",
	],
	iGreatEngineer : [
		"Samaratungga",
		"Nini Haji Rakryan Sanjiwana",
		"Rakai Pikatan",
		"Lokapala",
		"Pikatan",
	],
	iGreatStatesman : [
		"Gajah Mada", # 14th 
		"Parmeswara", # 14th 
		"Mahmud Badaruddin", # 19th 
		"fRaden Ayu Kartini", # 19th 
		"Sukarno", # 20th 
		"Agus Salim", # 20th 
		"Chep the Magnificent", # Contest Reward 
	],
	iGreatGeneral : [
		"Dharmawangsa",
		"Airlangga",
		"fTribhuwana Vijayatunggwadewi", # 14th 
		"Raden Wijaya",
		"Ken Dedes",
	],
},
iCivSpain : {
	iGreatProphet : [
		"Ignacio de Loyola", # 16th 
		u"Juan de Sepúlveda", # 16th 
		u"fTeresa de Ávila", # 16th 
		u"Francisco Suárez", # 16th 
		u"Bartolomé de Las Casas", # 16th 
		u"Junípero Serra", # 18th 
	],
	iGreatArtist : [
		"Miguel de Cervantes", # 16th 
		"Garcilaso de la Vega", # 16th 
		u"fJuana Inés de la Cruz", # 17th 
		u"Diego de Silva Velázquez", # 17th 
		"Pablo Picasso", # 20th 
		u"Salvador Dalí", # 20th 
	],
	iGreatScientist : [
		"Juan de Ortega", # 11th 
		"Gerardo de Cremona", # 12th 
		"Antonio de Ulloa", # 18th 
		u"Santiago Ramón y Cajal", # 19th 
	],
	iGreatMerchant : [
		u"Cristóbal Colón", # 15th 
		"Fernando de Magallanes", # 15th 
		"Hernando de Soto", # 16th 
		"Salvador Fidalgo", # 18th 
	],
	iGreatEngineer : [
		"Juan de Herrera", # 16th 
		u"Agustín de Betancourt", # 18th 
		"Alberto de Palacio y Elissague", # 19th 
		"Esteban Terradas i Illa", # 19th 
		"Juan de la Cierva", # 20th 
	],
	iGreatStatesman : [
		u"Francisco Jiménez de Cisneros", # 15th 
		"Francisco de Vitoria", # 16th 
		u"José de Gálvez", # 18th 
		u"José Moniño", # 18th 
		"Juan Prim", # 19th 
	],
	iGreatGeneral : [
		"El Cid", # 11th 
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
		"Jean Calvin", # 16th 
		u"fThérèse de Lisieux", # 19th 
		"Albert Schweitzer", # 20th 
		u"Marcel Légaut", # 20th 
	],
	iGreatArtist : [
		u"Chrétien de Troyes", # 12th 
		"fChristine de Pizan", # 15th 
		"Charles Le Brun", # 17th 
		"Jean-Baptiste Lully", # 17th 
		"Jean-Antoine Watteau", # 17th 
		"Victor Hugo", # 19th 
		"Claude Monet", # 19th 
		"Henri Matisse", # 19th 
		"Claude Debussy", # 19th 
		"fGeorge Sand", # 19th 
		"Alexandre Dumas", # 19th 
		"fEdith Piaf", # 20th 
	],
	iGreatScientist : [
		"Nicole Oresme", # 14th 
		"Rene Descartes", # 17th 
		"Pierre de Fermat", # 17th 
		"Antoine Lavoisier", # 18th 
		u"fÉmilie du Châtelet", # 18th 
		"Pierre-Simon Laplace", # 18th 
		"Louis Pasteur", # 19th 
		"fMarie-Sophie Germain", # 19th 
		"fMarie Curie", # 19th 
		"Antoine Henri Becquerel", # 20th 
	],
	iGreatMerchant : [
		"Jacques Cartier", # 16th 
		"Samuel de Champlain", # 17th 
		u"fThérèse de Couagne", # 18th 
		"fCoco Chanel", # 20th 
		"Marcel Dessault", # 20th 
	],
	iGreatEngineer : [
		"Jules Hardouin Mansart", # 17th 
		"Blaise Pascal", # 17th 
		"Claude Perrault", # 17th 
		"Charles Augustin de Coulomb", # 18th 
		"Joseph-Michel Montgolfier", # 18th 
		"Alexandre Gustave Eiffel", # 19th 
		"fMarie Marvingt", # 20th 
	],
	iGreatStatesman : [
		u"fAliénor d'Aquitaine", # 12th 
		"Philippe de Beaumanoir", # 13th 
		"Jean Bodin", # 16th 
		"Armand Jean du Plessis", # 17th 
		"Jean-Baptiste Colbert", # 17th 
		u"fAnne Marie Louise d'Orléans", # 17th 
		u"Charles-Maurice de Talleyrand-Périgord", # 18th 
		"Montesquieu", # 18th 
		"Voltaire", # 18th 
		"Pierre-Joseph Proudhon", # 19th 
		"fSimone de Beauvoir", # 20th 
	],
	iGreatGeneral : [
		"Charles Martel", # 8th 
		"Godefroy de Bouillon", # 11th 
		"Charles V", # 14th 
		"fJeanne d'Arc", # 15th 
		"Louis-Joseph de Montcalm", # 18th 
		"Louis-Rene de Latouche Treville", # 18th 
		"Louis-Nicolas Davout", # 18th 
		"Gilbert de Lafayette", # 19th 
	],
},
iCivEngland : {
	iGreatProphet : [
		"Bede the Venerable", # 8th 
		"Anselm of Canterbury", # 11th 
		"Thomas Becket", # 12th 
		"Thomas More", # 16th 
		"John Newton", # 18th 
		"William Booth", # 19th 
	],
	iGreatArtist : [
		"William Shakespeare", # 17th 
		"John Milton", # 17th 
		"John Vanbrugh", # 17th 
		"George Frideric Handel", # 18th 
		"fMary Wollstonecraft", # 18th 
		"Charles Dickens", # 19th 
		"Arthur Conan Doyle", # 19th 
		"fMary Shelley", # 19th 
		"fAgatha Christie", # 20th 
		"John Lennon", # 20th 
	],
	iGreatScientist : [
		"Francis Bacon", # 16th 
		"Isaac Newton", # 17th 
		"John Dalton", # 19th 
		"Charles Darwin", # 19th 
		"James Clerk Maxwell", # 19th 
		"fMary Anning", # 19th 
		"Ernest Rutherford", # 20th 
		"fRosalind Franklin", # 20th 
		"Stephen Hawking", # 20th 
	],
	iGreatMerchant : [
		"Francis Drake", # 16th 
		"James Cook", # 18th 
		"Adam Smith", # 18th 
		"John Maynard Keynes", # 20th 
	],
	iGreatEngineer : [
		"Christopher Wren", # 17th 
		"James Watt", # 18th 
		"Henry Bessemer", # 19th 
		"Charles Babbage", # 19th 
		"fAda Lovelace", # 19th 
		"Alan Turing", # 20th 
	],
	iGreatStatesman : [
		"Thomas Beckett", # 12th 
		"William Cecil", # 16th 
		"John Locke", # 17th 
		"Thomas Hobbes", # 17th 
		"Robert Walpole", # 18th 
		"William Pitt", # 18th 
		"William Gladstone", # 19th 
		"Benjamin Disraeli", # 19th 
		"Clement Atlee", # 20th 
	],
	iGreatGeneral : [
		"William the Conqueror", # 11th 
		"Richard the Lionheart", # 12th 
		"Edward III", # 14th 
		"Oliver Cromwell", # 17th 
		"Horatio Nelson", # 18th 
		"Arthur Wellington", # 19th 
		"Bernard Law Montgomery", # 20th 
	],
},
iCivGermany : {
	iGreatProphet : [
		"fHildegard von Bingen", # 12th 
		"Albertus Magnus", # 13th 
		"Jan Hus", # 14th 
		"Martin Luther", # 16th 
		"Philip Melanchthon", # 16th 
		"Dietrich Bonhoeffer", # 20th 
		"fEdith Stein", # 20th 
	],
	iGreatArtist : [
		"fRoswitha von Gandersheim", # 10th 
		u"Albrecht Dürer", # 15th 
		"Johann Sebastian Bach", # 17th 
		"Ludwig van Beethoven", # 18th 
		"Wolfgang Amadeus Mozart", # 18th 
		"Johann Wolfgang von Goethe", # 18th 
		"Friedrich Schiller", # 18th 
		"fClara Schumann", # 19th 
		"fLeni Riefenstahl", # 20th 
		"Leoreth", # 20th 
	],
	iGreatScientist : [
		"Johannes Kepler", # 17th 
		"Gottfried Leibniz", # 17th 
		u"Carl Friedrich Gauß", # 19th 
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
		"Carl Benz", # 19th 
		"Alfred Krupp", # 19th 
		"Ferdinand Porsche", # 20th 
		"August Horch", # 20th 
		"fMelitta Bentz", # 20th 
	],
	iGreatEngineer : [
		"Jakob Fugger", # 15th 
		"Gerhard Mercator", # 16th 
		"fBarbara Uthmann", # 16th 
		"Carl Benz", # 19th 
		"Alfred Krupp", # 19th 
		"Ferdinand Porsche", # 20th 
		"August Horch", # 20th 
		"fMelitta Bentz", # 20th 
	],
	iGreatStatesman : [
		"Immanuel Kant", # 18th 
		"Heinrich Friedrich Karl vom Stein", # 19th 
		"Klemens von Metternich", # 19th 
		"Karl Marx", # 19th 
		"fBertha von Suttner", # 19th 
		"Wilhelm Liebknecht", # 19th 
		"Friedrich Ebert", # 19th 
		"fRosa Luxemburg", # 19th 
		"Konrad Adenauer", # 20th 
		"fHannah Arendt", # 20th 
		"Helmut Kohl", # 20th 
	],
	iGreatGeneral : [
		u"Otto der Große", # 10th 
		"Albrecht von Wallenstein", # 17th 
		u"Gebhard Leberecht von Blücher", # 18th 
		"Carl von Clausewitz", # 19th 
		"Paul von Hindenburg", # 19th 
		"Erwin Rommel", # 20th 
		"Heinz Guderian", # 20th 
	],
},
iCivRussia : {
	iGreatProphet : [
		"Paisiy Yaroslavov", # 15th 
		"Feofan Prokopovich", # 18th 
		"fHelena Blavatsky", # 19th 
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
		"fNatalia Goncharova", # 20th 
		"fAnna Pavlova", # 20th 
	],
	iGreatScientist : [
		"Mikhail Lomonosov", # 18th 
		"Dmitri Mendeleyev", # 19th 
		"Nikolai Lobachevsky", # 19th 
		"Pavel Cherenkov", # 20th 
		"Mikhail Ostrogradsky", # 20th 
		"fMaria Kovalevskaya", 
	],
	iGreatMerchant : [
		"Afanasiy Nikitin", # 15th 
		"Vitus Bering", # 18th 
		"Ivan Kruzenshtern", # 19th 
	],
	iGreatEngineer : [
		"Ivan Starov", # 18th 
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
		"Vasily Tatishchev", # 18th 
		"Nikita Panin", # 18th 
		"Mikhail Speransky", # 19th 
		"Vladimir Lenin", # 19th 
		"Leon Trotsky", # 20th 
		"fAlexandra Kollontai", # 20th 
	],
	iGreatGeneral : [
		"Alexander Nevsky", # 13th 
		"Ivan Grozny", # 15th 
		"Mikhail Romanov", # 17th 
		"Alexander Suvorov", # 18th 
		"Pavel Nakhimov", # 19th 
		"Mikhail Skobelev", # 19th 
		"fVasilisa Kozhina", # 19th 
		"fNadezhda Durova", # 19th 
		"Georgy Zhukov", # 20th 
		"Vasily Chuikov", # 20th 
	],
},
iCivMali : {
	iGreatProphet : [
		"Wali Keita", # 13th 
		"Sidi Yahya", # 15th 
		"Seku Amadu", # 18th 
		"Ali Coulibaly", # 18th 
	],
	iGreatArtist : [
		"Nare Maghann Konate", # 13th 
		"Lobi Traore", # 20th 
		"Ibrahim Aya", # 20th 
	],
	iGreatScientist : [
		"Gaoussou Diawara", # 14th 
		"Abu al Baraaka", # 12-16th 
		"Ahmed Baba", # 16th 
		"Ag Mohammed Kawen", # 19th 
	],
	iGreatMerchant : [
		"Tunka Manin", # 11th 
		"Abubakari", # 13th 
		"Abu Bakr ibn Ahmad Biru", # 12-16th 
		"Moctar Ouane", # 20th 
	],
	iGreatEngineer : [
		"Sakura", # 13th 
		"Al-Qadi Aqib ibn Umar", # 13th 
		"Abu Es Haq es Saheli", # 14th 
		"Mohammed Naddah", # 15th 
		"Mohammed Bagayogo", # 16th 
	],
	iGreatStatesman : [
		"Askia Muhammad", # 15th 
		u"Bitòn Coulibaly", # 18th 
		u"Samori Touré", # 19th 
		"Modibo Keita", # 20th 
		u"Alpha Oumar Konaré", # 20th 
	],
	iGreatGeneral : [
		"Sundiata Keita", # 13th 
		"Askia Muhammad", # 15th 
		"Sunni Ali", # 15th 
		"Askia Daoud", # 16th 
		"Ngolo Diarra", # 18th 
		"fSeh-Dong-Hong-Beh", # 19th 
	],
},
iCivPortugal : {
	iGreatProphet : [
		u"António de Lisboa", # 13th 
		u"Isabel de Aragão", # 14th 
		u"João de Deus", # 16th 
		u"João de Brito", # 17th 
	],
	iGreatArtist : [
		u"Fernão Lopes", # 15th 
		u"Nuno Gonçalves", # 15th 
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
		"Abel Salazar", # 20th 
		u"António Egas Moniz", # 20th 
	],
	iGreatMerchant : [
		"Vasco da Gama", # 15th 
		"Francisco de Almeida", # 15th 
		"Henrique o Navegador", # 15th 
		"Bartolomeu Dias", # 15th 
		"fGracia Mendes Nasi", # 16th 
		u"Pedro Álvares Cabral", # 15th 
		u"Fernão Mendes Pinto", # 16th 
	],
	iGreatEngineer : [
		"Mateus Fernandes", # 15th 
		"Diogo de Boitaca", # 16th 
		u"João Antunes", # 17th 
		u"Álvaro Siza Vieira", # 20th 
	],
	iGreatStatesman : [
		"Henrique de Avis", # 15th 
		u"Sebastião José de Carvalho e Melo", # 18th 
		"Afonso Costa", # 20th 
		u"António de Oliveria Salazar", # 20th 
	],
	iGreatGeneral : [
		u"Nuno Álvares Pereira", # 14th 
		"Afonso de Albuquerque", # 15th 
		"Alvaro Vaz de Almada", # 15th 
		"Otelo Saraiva de Carvalho", # 20th 
	],
},
iCivInca : {
	iGreatProphet : [
		"Guyasuta", 
		"Yahuar Huacac", 
	],
	iGreatArtist : [
		"Ah Cacao", 
		"Viracocha", 
		"Ninan Cuyochi", 
		"Ocllo", 
	],
	iGreatScientist : [
		"Sinchi Roca",
		"Maita Capac", 
		"Huascar", 
		"Titu Cusi", 
		"Manco Capac", 
		"Ibca Roca", 
	],
	iGreatMerchant : [
		"Tupa Inca-Yupanqui", 
		"Felipillo", 
		"Quetzal-Macau", 
	],
	iGreatEngineer : [
		"Kenu Curaua", 
		"Capac Yupanqui", 
		"Mana-Paoa", 
		"Sipan-Itchi", 
		"Sayri Tupa Inca", 
	],
	iGreatStatesman : [
		u"Mayta Cápac", # 14th 
		"Manco Inca Yupanqui", # 16th 
		"fMama Huaco", # 16th 
		u"Tápac Amaru", # 18th 
	],
	iGreatGeneral : [
		"Pachacuti", 
		"Atahualpa", 
		"Manco Inca", 
		"Tupa Amaru", 
		"Chalicuchima", 
		"Quisquis", 
		"fBartolina Sisa", # 18th 
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
		"Camillo Borghese", # 16th 
		"Giulio de' Medici", # 16th 
	],
	iGreatArtist : [
		"Dante Alighieri", # 13th 
		"Giovanni Boccaccio", # 14th 
		u"Niccolò Machiavelli", # 15th 
		"Donatello", # 15th 
		"Michelangelo", # 16th 
		"Raphael", # 16th 
		"fSofonisba Anguissola", # 16th 
		"fArtemisia Gentileschi", # 17th 
		"fGrazia Deledda", # 20th 
		"Gabriele Trovato", # 20th 
		"Gian Maria Volontè", # Contest Reward 
	],
	iGreatScientist : [
		"fTrotula di Salerno", # 12th 
		"Francesco Petrarca", # 14th 
		"Pico della Mirandola", # 15th 
		"Giordano Bruno", # 16th 
		"Galileo Galilei", # 16th 
		"Luigi Galvani", # 18th 
		"Alessandro Volta", # 18th 
		"fMaria Gaetana Agnesi", # 18th 
		"Enrico Fermi", # 20th 
		"fRita Levi-Montalcini", # 20th 
	],
	iGreatMerchant : [
		"Marco Polo", # 13th 
		"Simone de' Bardi", # 13th 
		"Giovanni de' Medici", # 14th 
		"Donato Peruzzi", # 14th 
		"Ciriaco de Ancona", # 15th 
		"fTullia d'Aragona", # 16th 
	],
	iGreatEngineer : [
		"Leonardo da Vinci", # 15th 
		"Taccola", # 15th 
		"Donato Bramante", # 15th 
		"Filippo Brunelleschi", # 15th 
		"Guglielmo Marconi", # 20th 
	],
	iGreatStatesman : [
		u"Niccolò Machiavelli", # 15th 
		"fIsabelle d'Este", # 16th 
		"Francesco Guicciardini", # 16th 
		"Giambattista Vico", # 18th 
		"Cesare Beccaria", # 18th 
		"Giuseppe Garibaldi", # 19th 
		"Giuseppe Mazzini", # 19th 
		"Antonio Gramsci", # 20th 
	],
	iGreatGeneral : [
		"Enrico Dandolo", # 13th 
		"Simone Boccanegra", # 14th 
		"Francesco Sforza", # 15th 
		"Giuseppe Garibaldi", # 19th 
	],
},
iCivMongols : {
	iGreatProphet : [
		"Abaqa", # 13th 
		"Arghun", # 13th 
		"Sartaq", # 13th 
		"Zanabazar", # 17th 
	],
	iGreatArtist : [
		"Oghul Qaimish", # 13th 
		"Tolui", # 13th 
		"Uzbeg", # 14th 
		"Siqin Gaowa", # 20th 
	],
	iGreatScientist : [
		"Kaidu", # 13th 
		"Ulugh Beg", # 15th 
		"Mandukhai", # 15th 
		"Nurhaci", # 16th 
	],
	iGreatMerchant : [
		"Hulagu", # 13th 
		u"Güyük", # 13th 
		"Mengu-Timur", # 13th 
		"Gaykhatu", # 13th 
		"Altan", # 16th 
	],
	iGreatEngineer : [
		"Duwa", # 13th 
		"Zhang Wenqian", # 13th 
		"Toqta", # 14th 
		"Li Siguang", # 20th 
	],
	iGreatStatesman : [
		"Batu Khan", # 13th 
		"Urtu Saqal", # 13th 
		"fOrghana", # 13th 
		"Ghazan", # 13th 
		u"Temür Khan", # 13th 
		"Dayan Khan", # 15th 
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
		"Tlacateotl", 
		"Tenoch", 
		"Papantzin", 
		"Yacotzin", 
		"Ixtlilxochitl", 
	],
	iGreatArtist : [
		"Cipactli", 
		"Oxomoco", 
		"Huitzilopochtli", 
		"Techotlalatzin", 
		"Ihuitemotzin", 
		"fMacuilxochitzin", 
	],
	iGreatScientist : [
		"Chichatoyotl", 
		"Textalatzin", 
		"Axayacatl", 
		"Ixtlilxochitl", 
		"Coanacochtzin", 
	],
	iGreatMerchant : [
		"Cuauhtemoc", 
		"Tlacotzin", 
		"Chak-Mol", 
		"Atlante", 
		"Techichpotzin", 
	],
	iGreatEngineer : [
		"Xolotl", 
		"Itzcatl", 
		"Mixcoatl", 
		"Tlacaelel", 
		"Moquihuix", 
	],
	iGreatStatesman : [
		"Acamapichtli", # 14th 
		"Quaquapitzahuac", # 15th 
		"Tezozomoctli", # 15th 
		"Nezahualcoyotl", # 15th 
		"Nezahualpilli", # 15th 
		"fRigoberta Mench&#250;", # 20th 
	],
	iGreatGeneral : [
		"Ahuitzotl", 
		"Itzcoatl", 
		"Tezozomoc", 
		"Maxtla", 
		"Huitzilhuitl", 
		"Chimalpopoca", 
	],
},
iCivMughals : {
	iGreatProphet : [
		"Rajah Birbal",
		"Guru Ram Das",
		"Guru Arjan",
		"Hiravijaya ji",
		"Shah Abdul Latif Bhittai",
		"Bulleh Shah",
	],
	iGreatArtist : [
		"Gulbadan Begum",
		"Shaikh Abu al-Faiz ibn Mubarak",
		"'Abd al-Samad",
		"Ustad Mansur",
		"Govardhan",
		"Jafar Zatalli",
	],
	iGreatScientist : [
		"Kashmiri ibn Luqman",
		"Abu al-Fazid ibn Mubarak",
		"Muhammad Salih Tahtawi",
		"'Abd-ul-Qadir Bada'uni",
		"Maharaja Sawai Jai Singh II",
		"Khwaja Nizam-ud-Din Ahmad",
	],
	iGreatMerchant : [
		"Sher Shah Suri",
		"Raja Todar Mal",
		"Mir Jumla II",
		"Yahya Saleh",
		"Khan 'Alam",
		"Mian Muhammad Mansha",
	],
	iGreatEngineer : [
		"Ustad Ahmad Lahauri",
		"Fathullah Shirazi",
		"Abdur Rahman Hye",
		"Abdul Qadeer Khan",
		"Munir Ahmad Khan",
		"fYasmeen Lari",
	],
	iGreatStatesman : [
		"fRazia Sultana", # 13th 
		"Babur", # 16th 
		"Abu'l-Fazl ibn Muhammad", # 16th 
		"Muhammad Ali Jinnah", # 20th 
		"Choudhry Ali", # 20th 
	],
	iGreatGeneral : [
		"Zahir-ud-din Muhammad Babur",
		"Bayram Khan",
		"Mir Baqi",
		"Abudullah Khan Barha",
		"Abul Muzaffar Aurangzeb",
		"Ali Vardi Khan", 
		"fBegum Hazrat Mahal", # 19th 
	],
},
iCivTurkey : {
	iGreatProphet : [
		"Sheikh Bedreddin", # 14th 
		"Sabatai Zevi", # 17th 
		"Yaakov Culi", # 18th 
		"Mustada Cagrici", # 20th 
	],
	iGreatArtist : [
		"Yunus Emre", # 13th 
		u"Hayâlî", # 16th 
		u"Gül Baba", # 16th 
		"Mehmet Akif Ersoy", # 20th 
	],
	iGreatScientist : [
		"Qazi Zada", # 14th 
		"Cahit Arf", # 20th 
		"Oktay Sinanoglu", # 20th 
		u"Feza Gürsey", # 20th 
		"Aziz Sancar", # 21th 
	],
	iGreatMerchant : [
		"Evliya Celebi", # 17th 
		u"Abdülmecid", # 19th 
		"Hormuzd Rassam", # 20th 
		"Nejat Eczacibashi", # 20th 
		"Aydin Dogan", # 20th 
	],
	iGreatEngineer : [
		"Atik Sinan", # 15th 
		"Davud Aga", # 15th 
		"Mimar Sinan", # 15th 
		"Ekmel Ozbay", # 20th 
	],
	iGreatStatesman : [
		"Sheikh Edebali", # 13th 
		"Pargali Ibrahim Pasha", # 16th 
		"Sokollu Mehmet Pasha", # 16th 
		u"Ismet Inönü", # 20th 
		u"Süleyman Demirel", # 20th 
	],
	iGreatGeneral : [
		"Orhan", # 14th 
		"Hayreddin Barbarossa", # 16th 
		"Selim", # 16th 
		"Turgut Reis", # 16th 
		"Kara Mustafa Pasha", # 17th 
		"Ismail Enver", # 20th 
	],
},
iCivNetherlands : {
	iGreatProphet : [
		"Geert Grote", # 14th 
		"Erasmus van Rotterdam", # 16th 
		"Abraham Kuyper", # 19th 
		"fAlida Bosshardt", # 20th 
	],
	iGreatArtist : [
		"Hendrick de Keyser", # 16th 
		"Rembrandt van Rijn", # 17th 
		"Johannes Vermeer", # 17th 
		"Pieter Corneliszoon Hooft", # 17th 
		"fTitia Bergsma", # 18th 
		"Vincent van Gogh", # 19th 
	],
	iGreatScientist : [
		"Simon Stevin", # 16th 
		"Christiaan Huygens", # 17th 
		"Govert Bidloo", # 17th 
		"fAnna Maria van Schurman", # 18th 
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
	],
	iGreatEngineer : [
		"Cornelis Corneliszoon", # 16th 
		"Antonie van Leeuwenhoek", # 17th 
		"Jan Leeghwater", # 17th 
	],
	iGreatStatesman : [
		"Desiderius Erasmus", # 16th 
		"Johan van Oldenbarnevelt", # 16th 
		"Johan de Witt", # 17th 
		"Adriaen van der Donck", # 17th 
		"Hugo Grotius", # 17th 
		"Cornelis de Graeff", # 17th 
		"Johan Thorbecke", # 19th 
		"Cornelis Lely", # 19th 
		"Willem Drees", # 20th 
	],
	iGreatGeneral : [
		"Maurits van Nassau", # 16th 
		"Michiel de Ruyter", # 17th 
		"Frederik Hendrik", # 17th 
		"Cornelis Tromp", # 17th 
	],
},
iCivAmerica : {
	iGreatProphet : [
		"Roger Williams", # 17th 
		"fAnne Hutchinson", # 17th 
		"William Penn", # 18th 
		"Jonathan Edwards", # 18th 
		"fAnn Lee", # 18th 
		"Joseph Smith", # 19th 
	],
	iGreatArtist : [
		"Edgar Allan Poe", # 19th 
		"Mark Twain", # 19th 
		"fEmily Dickinson", # 19th 
		"Herman Melville", # 19th 
		"fMary Cassatt", # 19th 
		"Ernest Hemingway", # 20th 
		"Charlie Chaplin", # 20th 
		"Elvis Presley", # 20th 
		"fHarper Lee", # 20th 
		"Miles Davis", # 20th 
		"Jimi Hendrix", # 20th 
	],
	iGreatScientist : [
		"fNettie Stevens", # 19th 
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
		"Wright Brothers", # 20th 
		"fLillian Moller Gilbreth", # 20th 
		"fHedy Lamarr", # 20th 
		"fMargaret Hutchinson Rousseau", # 20th 
	],
	iGreatStatesman : [
		"Thomas Paine", # 18th 
		"Thomas Jefferson", # 18th 
		"Benjamin Franklin", # 18th 
		"Andrew Jackson", # 19th 
		"Frederick Douglass", # 19th 
		"fSojourner Truth", # 19th 
		"fVictoria Claflin Woodhull", # 19th 
		"fJane Addams", # 19th 
		"fEleanor Roosevelt", # 20th 
		"George Kennan", # 20th 
	],
	iGreatGeneral : [
		"Andrew Jackson", # 19th 
		"Ulysses S. Grant", # 19th 
		"Robert E. Lee", # 19th 
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
		u"Bahá'u'lláh", # 19th 
		u"Báb", # 19th 
		"Ayatollah Mohammad Taqi", # 20th 
	],
	iGreatArtist : [
		"Shaykh-i Baha'i", # 16th 
		"Reza Abbasi", # 16th 
		"Ustad Mirza Shirazi", # 18thth 
		"Mihr 'Ali", # 19th 
		"fForough Farrokhzad", # 20th 
		"Hossein Amanat", # 20th 
		"fHayedeh", # 20th 
	],
	iGreatScientist : [
		"Al-Birjandi", # 16th 
		"Qazi Sa'id Qumi", # 17th 
		"Alavi Shirazi", # 17th 
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
		"Ebrahim Khan Kalantar", # 19th 
		"Kuchik Khan", # 19th 
		"Amir Kabir", # 19th 
		"Reza Shah Pahlavi", # 20th 
		"Mohammad Mossadegh", # 20th 
	],
	iGreatGeneral : [
		"Abbas I", # 16th 
		"Mohammad Khan Qajar", # 18th 
		"Ahmad Amir-Ahmadi", # 19th 
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
		"Tenzin Gyatso", # 20th 
	],
},
iCivPoland : {
	iGreatProphet : [
		"Wojciech",
		"Stanislaw",
		"fJadwiga",
		"Karol Wojtyla",
	],
	iGreatArtist : [
		"Jan Matejko",
		"Frederic Chopin",
		"Witold Lutoslawski",
	],
	iGreatScientist : [
		"Witelo",
		"Mikolaj Kopernik",
		"Jan Brozek",
		"Stanislaw Staszic",
		"fMaria Sklodowska",
	],
	iGreatMerchant : [
		"Leopold Kronenberg",
		"Jan Kulczyk",
		"Steve Wozniak",
	],
	iGreatEngineer : [
		"Tadeusz Sendzimir",
		"Ignacy Lukasiewicz",
		"Kasimiersz Proszynski",
	],
	iGreatStatesman : [
		"Wladyslaw Lokietek", # 14th 
		"Andrzej Frycz Modrzewski", # 16th 
		"Jan Zamoyski", # 16th 
		"Stanislaw Staszic", # 18th 
		"Ignacy Daszynski", # 20th 
		"Jozef Pilsudski", # 20th 
		"Wladyslaw Sikorski", # 20th 
		"Lech Walesa", # 20th 
	],
	iGreatGeneral : [
		"Wladyslaw Jagiello",
		"Jan Tarnowski",
		"Tadeusz Kosciuszko", # 18th 
		"fEmilia Plater", # 19th 
		"Wladyslaw Sikorski",
	],
},
iCivCongo : {
	iGreatStatesman : [
		"Mwata Yamvo", # 16th 
		"Ng'anga Bilonda", # 16th 
		"Kalala Ilunga", # 17th 
		"Msiri", # 19th 
		"Patrice Lumumba", # 20th 
		"Joseph Kasa-Vubu", # 20th 
	],
},
iCivArgentina : {
	iGreatProphet : [
		"Gauchito Gil",
		"Jorge Mario Bergoglio",
	],
	iGreatArtist : [
		"Jose Hernandez",
		"Carlos Gardel",
		"fGabriela Mistral", # 20th 
		u"fEva Perón",
		"Jorge Luis Borges",
		"Antonio Berni",
		"Daniel Barenboim",
		u"Juan José Campanella",
		"Gustavo Cerati",
	],
	iGreatScientist : [
		"Francisco Moreno",
		"Luis Federico Leloir",
		u"László Bíró",
		u"René Favaloro",
	],
	iGreatMerchant : [
		u"José ber Gelbard",
		"Roberto Aleman",
		"Jorge Wehbe",
		"Aldo Ferrer",
		"Antonio Cafiero",
		"Juan Las Heras",
	],
	iGreatEngineer : [
		"Luis Huergo",
		"Amancio Williams",
		u"César Pelli",
		"Clorindo Testa",
	],
	iGreatStatesman : [
		"Estanislao Zeballos", # 19th 
		"Carlos Saavedra Lamas", # 20th 
		"Juan Atilio Bramuglia", # 20th 
		"fEstela Barnes de Carlotto", # 20th 
	],
	iGreatGeneral : [
		"Cornelio Saavedra",
		"Manuel Belgrano",
		u"Juan José Castelli",
		u"Martín Miguel de Güemes",
		u"José Gervasio Artigas",
	],
},
iCivBrazil : {
	iGreatProphet : [
		u"António Conselheiro",
		u"Hélder Câmara",
		u"fIrmã Dulce Pontes", # 20th 
		"Chico Xavier",
		"Edir Macedo",
	],
	iGreatArtist : [
		"Aleijadinho",
		u"António Carlos Gomes",
		"Machado de Assis",
		"fTarsila do Amaral", # 20th 
		"fCarmen Miranda", # 20th 
		"Tom Jobim",
		"Romero Britto",
	],
	iGreatScientist : [
		"Oswaldo Cruz",
		"Carlos Chagas",
		"Alberto Santos-Dumont",
		"Urbano Ernesto Stumpf",
		u"Aziz Ab'Sáber",
		"Marcelo Gleiser",
	],
	iGreatMerchant : [
		"Francesco Matarazzo",
		"Roberto Marinho",
		"Jorge Lemann",
		"Eike Batista",
	],
	iGreatEngineer : [
		u"André Rebouças",
		u"Cândido Rondon",
		"Oscar Niemeyer",
		"Norberto Odebrecht",
	],
	iGreatStatesman : [
		u"José Bonifácio de Andrada", # 18th 
		"Rodrigo Augusto da Silva", # 19th 
		u"José Paranhos", # 19th 
		u"Isabel Bragança", # 19th 
		"Miguel Reale", # 19th 
		"Roberto Mangabeira Unger", # 20th 
	],
	iGreatGeneral : [
		"Duque de Caxias",
		u"Almirante Tamandaré",
		u"fMaria Quitéria", # 19th 
		"Mascarenhas de Morais",
		"Eurico Gaspar Dutra",
		"Artur da Costa e Silva",
	],
},
iCivColombia : {
	iGreatProphet : [
		u"Félix Restrepo Mejía",
		"Camillo Torres Restrepo",
		u"Alfonso López Trujillo",
		u"Julio Enrique Dávila",
		u"fMaría Luisa Piraquive",
		u"César Castellanos",
	],
	iGreatArtist : [
		"Gabriel Garcia Marquez",
		"Rodrigo Arenas",
		u"Álvaro Mutis",
		"Fernando Botero",
		"Rafael Orozco",
		"Rodrigo Garcia",
		"fShakira",
	],
	iGreatScientist : [
		u"José Jéronimo Triana",
		"Julio Garavito Armero",
		u"Rodolfo Llinás",
		"Jorge Reynolds Pombo",
	],
	iGreatMerchant : [
		"Julio Mario Santo Domingo Pumarejo",
		u"Carlos Ardila Lülle",
		"Luis Carlos Sarmiento Angulo",
	],
	iGreatEngineer : [
		"Fray Domingo de Petres",
		"Rogelio Salmona",
		"Roswell Garavito Pearl",
	],
	iGreatStatesman : [
		u"Rafael Núñez", # 19th 
		"Jorge Eliécer Gaitán", # 20th 
		u"Nicolás Gómez Dávila", # 20th 
		u"Mario Lanserna Pinzón", # 20th 
	],
	iGreatGeneral : [
		"Antonia Santos",
		u"Antonio Nariño",
		"Francisco de Paula Santander",
	],
},
iCivMexico : {
	iGreatProphet : [
		"Juan Diego",
		u"Felipe de Jesús",
		"Francisco Javier Clavijero",
		u"Rafael Guízar Valencia",
		u"Cristóbal Magallanes Jara",
		"Miguel Pro",
		"Samuel Ruiz",
		u"Javier Lozano Barragán",
	],
	iGreatArtist : [
		u"José Clemente Orozco",
		u"fÁngela Peralta", # 19th 
		"Diego Rivera",
		"fFrida Kahlo",
		"Octavio Paz",
		"fRemedios Varo", # 20th 
		u"fDolores del Río", # 20th 
		"Pedro Infante",
		"Carlos Fuentes",
		u"Vicente Fernández",
	],
	iGreatScientist : [
		"Gabino Barreda",
		"Manuel Sandoval Vallarta",
		"Ricardo Miledi",
		u"Mario José Molina",
		"Rodolfo Neri Vela",
	],
	iGreatMerchant : [
		u"Lucas Alamán",
		u"Víctor Urquidi",
		u"Jerónimo Arango",
		"Carlos Slim",
		"Everardo Elizondo",
		u"Alberto Baillères",
		u"Emilio Azcárraga Jean",
	],
	iGreatEngineer : [
		u"José Villagrán García",
		u"Luis Barragán",
		"Juan O'Gorman",
		"Mario Pani",
		u"Pedro Ramírez Vázquez",
		"Bernardo Quintana Arrioja",
	],
	iGreatStatesman : [
		u"José María Pino Suárez", # 19th 
		"Pascual Orozco", # 19th 
		u"José Vasconcelos", # 20th 
		"Octavio Paz", # 20th 
		"fElvia Carrillo Puerto", # 20th 
		"fRosario Castellanos", # 20th 
		u"Alfonso García Robles", # 20th 
		u"Gilberto Bosques Saldívar", # 20th 
	],
	iGreatGeneral : [
		"Miguel Hidalgo",
		u"Agustín de Iturbide",
		u"fJosefa Ortiz de Domínguez", # 19th 
		u"Porfirio Díaz",
		"Pancho Villa",
		"Emiliano Zapata Salazar",
	],
},
iCivCanada : {
	iGreatProphet : [
		u"André Bessette", # 19th 
	],
	iGreatArtist : [
		"Tom Thomson", # 19th 
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
		"fElizabeth Arden", # 20th 
		u"Guy Laliberté", # 20th 
	],
	iGreatEngineer : [
		"Sandford Fleming", # 19th 
		"William Cornelius Van Horne", # 19th 
		"Joseph-Armand Bombardier", # 20th 
		"fElsie MacGill", # 20th 
	],
	iGreatStatesman : [
		"John A Macdonald", # 19th 
		u"George-Étienne Cartier", # 19th 
		"Louis Riel", # 19th 
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