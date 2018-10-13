# coding: utf-8

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

def getAlias(iCiv, iType, iEra):
	if iCiv in [iCivHarappa, iCivTamils]: return iCivIndia
	elif iCiv == iCivHolyRome: return iCivGermany
	elif iCiv == iCivIran: return iCivPersia
	
	return iCiv
	
def getType(iUnit):
	iUnitType = utils.getBaseUnit(iUnit)
	if iUnitType in lTypes: return lTypes.index(iUnitType)
	return -1

def getAvailableNames(iPlayer, iType):
	pPlayer = gc.getPlayer(iPlayer)
	iEra = pPlayer.getCurrentEra()
	iCiv = getAlias(pPlayer.getCivilizationType(), iType, iEra)
	
	return getEraNames(iCiv, iType, iEra)

def getEraNames(iCiv, iType, iEra):
	lNames = lGreatPeople[iCiv][iType]
	
	iOffset = lOffsets[iCiv][iType][iEra]
	iNextOffset = len(lNames)
	if iEra + 1 < iNumEras: iNextOffset = lOffsets[iCiv][iType][iEra+1]
	
	iSpread = max(iNextOffset - iOffset, min(iEra+2, 5))
	
	lBefore = [sName for sName in lNames[:iOffset] if not gc.getGame().isGreatPersonBorn(sName)]
	lAfter = [sName for sName in lNames[iOffset:] if not gc.getGame().isGreatPersonBorn(sName)]
	
	if len(lAfter) >= iSpread:
		return lAfter[:iSpread]
	
	iSpread -= len(lAfter)
	return lBefore[-iSpread:] + lAfter
	
def getName(unit):
	iType = getType(unit.getUnitType())
	if iType < 0: return None
	
	lAvailableNames = getAvailableNames(unit.getOwner(), iType)
	if not lAvailableNames: return None
	
	return utils.getRandomEntry(lAvailableNames)
	
def onGreatPersonBorn(unit, iPlayer, city, bAnnounceBirth = True):
	sName = getName(unit)
	if sName:
		gc.getGame().addGreatPersonBornName(sName)
		
		# Leoreth: replace graphics for female GP names
		if sName[0] == "f":
			sName = sName[1:]
			unit = utils.replace(unit, dFemaleGreatPeople[utils.getBaseUnit(unit.getUnitType())])
			
		unit.setName(sName)
		
	# Leoreth: display notification
	if bAnnounceBirth:
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
			iOffsets = 0
			
			for i, entry in enumerate(dGreatPeople[iCiv][iType]):
				if entry in range(iNumEras): 
					lOffsets[iCiv][lTypes.index(iType)][entry] = i - iOffsets
					iOffsets += 1
				else: 
					lGreatPeople[iCiv][lTypes.index(iType)].append(entry)
				
			lCurrentOffsets = lOffsets[iCiv][lTypes.index(iType)]
			for i in range(1, len(lCurrentOffsets)):
				if lCurrentOffsets[i] < lCurrentOffsets[i-1]: lCurrentOffsets[i] = lCurrentOffsets[i-1]
				
			lCurrentOffsets[iDigital] = len(lGreatPeople[iCiv][lTypes.index(iType)])
				
	print lGreatPeople

		
dGreatPeople = {
iCivEgypt : {
	iGreatProphet : [
		"Ptah-Hotep", # 25th BC
		"Meryre", # 15th BC
		"Akhenaten", # 14th BC
		"fNefertiti", # 13th BC
		iClassical,
		"Petiese", # 7th BC
	],
	iGreatArtist : [
		"Pehen-Ptah", # 27th BC
		"Thutmose", # 14th BC
		"Bek", # 14th BC
		"Ipuki", # 14th BC
		"Sennedjem", # 13th
		"Khaemweset", # 12th BC
		"Amenemope", # 12th BC
		iClassical,
		"fHelena", # 4th BC
	],
	iGreatScientist : [
		"fMerit-Ptah", # 27th BC
		"fPeseshet", # 26th BC
		"Ahmose", # 17th BC
		iClassical,
		"Harkhebi", # 3rd BC
		"Manetho", # 3rd BC
		"Ptolemaios", # 2nd
		"Diophantos", # 3rd
		"fHypatia", # 4th
	],
	iGreatMerchant : [
		"Harkhuf", # 23rd BC
		"Maya", # 13th BC
		"fTiye", # 13th BC
		iClassical,
		"Piye", # 8th BC
		"Alara", # 8th BC
	],
	iGreatEngineer : [
		"Imhotep", # 27th BC
		"Sneferu", # 27th BC
		"Senenmut", # 17th BC
		"Ineni", # 15th BC
		"Amenhotep", # 14th BC
		iClassical,
		"Heron", # 1st AD
	],
	iGreatStatesman : [
		"Kagemni", # 26th BC
		"Amenemhat", # 20th BC
		"fHatshepsut", # 15th BC
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
iCivChina : {
	iGreatProphet : [
		"Lao Tzu", # 6th BC
		"Kong Fuzi", # 5th BC
		"Meng Zi", # 4th BC
		"Zhuangzi", # 4th BC
		"Han Fei", # 3rd BC
		iMedieval,
		"Bodhidharma", # 6th
		"Bukong", # 8th
		"fLin Moniang", # 10th
		"Wang Chongyang", # 12th
		"fSun Bu'er", # 12th
		"Zhu Xi", # 12th
		"Qiu Chuji", # 12th
		iRenaissance, 
		"Wang Yangming", # 16th
		iIndustrial, 
		"Hong Xiuquan", # 19th
		"Wang Jueyi", # 19th
		iGlobal,
		"Xiong Shili", # 20th
		"Sheng Yen", # 20th
		"Li Hongzhi", # 20th
	],
	iGreatArtist : [
		"Ling Lun", # legendary
		iClassical,
		"Li Bo", # 8th BC
		"Du Fu", # 8th BC
		"Wang Xizhi", # 4th BC
		"fCai Wenji", # 1st
		"Gu Kaizhi", # 4th
		iMedieval,
		"fShangguan Wan'er", # 7th
		"Han Yu", # 8th
		"Fan Kuan", # 10th
		"Su Shi", # 11th 
		"fLi Qingzhao", # 12th
		"Huang Gongwang", # 14th
		"Luo Guanzhong", # 14th
		iRenaissance,
		"Tang Yin", # 15th
		"Wu Cheng'en", # 16th
		"Cao Xueqin", # 18th
		iGlobal,
		"Qi Baishi", # 20th
		"Lu Xun", # 20th
		"Wu Guanzhong", # 20th
	],
	iGreatScientist : [
		"Li Fan", # 1st
		"fBan Zhao", # 1st
		"Liu Hui", # 3rd
		"Zu Chongzhi", # 5th
		iMedieval,
		"Shen Kuo", # 11th
		"Zhu Shijie", # 14th
		iRenaissance,
		"fTan Yunxian", # 16th
		"Xu Guangqi", # 17th
		"Song Yingxing", # 17th
		"fWang Zhenyi", # 18th
		iGlobal,
		"Li Yuanzhe", # 20th
		"Chen Ning Yang", # 20th
		"fTu Youyou", # 20th
	],
	iGreatMerchant : [
		"Zhang Qian", # 2nd BC
		"Faxian", # 4th
		iMedieval,
		"Xuanzang", # 7th
		"Li Chun'an", # 10th
		"Wang Anshi", # 11th
		iRenaissance,
		"Zheng He", # 15th
		"Yishiha", # 15th
		"Pan Qiguan", # 18th
		iGlobal,
		"Zeng Junchen", # 20th
		"Deng Xiaoping", # 20th
	],
	iGreatEngineer : [
		"fLeizu", # 27th BC
		iClassical,
		"Lu Ban", # 5th BC
		"Cai Lun", # 1st
		"Zhang Heng", # 2nd
		"Ma Jun", # 3rd
		iMedieval,
		"Yi Xing", # 8th
		"Yu Hao", # 10th
		"Bi Sheng", # 11th
		"Su Song", # 11th
		"Wang Zhen", # 14th
		iGlobal,
		"Li Siguang", # 20th
		"fWu Jianxiong", # 20th
	],
	iGreatStatesman : [
		"Gongsun Yang", # 4th BC
		"Li Si", # 3rd BC
		"Xiao He", # 2nd BC
		iMedieval,
		"Fang Xuanling", # 7th
		"fWu Zetian", # 7th
		"Di Renjie", # 7th
		"Fan Zhongyan", # 11th
		"Liu Bowen", # 14th
		iRenaissance,
		"Zhang Juzheng", # 16th
		"Zhang Tingyu", # 18th
		iIndustrial,
		"Li Hongzhang", # 19th
		"Sun Yat-sen", # 19th
		iGlobal,
		"Zhou Enlai", # 20th
		"fJiang Qing", # 20th
	],
	iGreatGeneral : [
		"fFu Hao", # 13th BC
		iClassical,
		"Sun Tzu", # 6th BC
		"Cao Cao", # 2nd
		"Zhuge Liang", # 3rd
		iMedieval,
		"fPingyang Gongzhu", # 7th
		"Guo Ziyi", # 8th
		"Yue Fei", # 12th
		iRenaissance,
		"Qi Jiguang", # 16th
		"Shi Lang", # 17th
		iIndustrial,
		"fChing Shih", # 19th
		"Zeng Guofan", # 19th
		"Zuo Zongtang", # 19th
		iGlobal,
		"Zhang Zuolin", # 20th
		"Zhu De", # 20th
		"Chiang Kai-shek", # 20th
		"Peng Dehuai", # 20th
	],
	iGreatSpy : [
		"Zhou Xing", # 7th
		"Lai Junchen", # 7th
		"Yang Xian", # 14th
		iRenaissance,
		"Liu Jin", # 15th
		"Wei Zhongxian", # 16th
		iGlobal,
		"Dai Li", # 20th
		"Kang Sheng", # 20th
		"fXu Lai", # 20th
		"Li Bai", # 20th
	],
},
iCivBabylonia : {
	iGreatProphet : [
		"Utnapishtim", # legendary
		"Gilgamesh", # legendary
		"fAmat-Mamu", # 18th BC
		iClassical,
		"fAdad-guppi", # 6th BC
		"Ezra", # 5th BC
	],
	iGreatArtist : [
		"fEnheduanna", # 23rd BC
		"Gudea", # 22nd BC
		"Samsu-ditana", # 17th BC
		"Sin-leqi-unninni", # 13th BC
	],
	iGreatScientist : [
		"fTapputi", # legendary
		"Esagil-kin-apli", # 11th BC
		iClassical,
		"fEnnigaldi", # 6th BC
		"Nabu-rimanni", # 6th BC
		"Kidinnu", # 4th BC
		"Sudines", # 3rd BC
		"Bel-reu-su", # 3rd BC
	],
	iGreatMerchant : [
		"fIltani", # 18th BC
		"Burna-Buriash", # 14th BC
		"Kadashman-Enlil", # 14th BC
		iClassical,
		"Itti-Marduk-balatu", # 6th BC
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
iCivGreece : {
	iGreatProphet : [
		"fEritha", # 12th BC
		iClassical,
		"Herakleitos", # 6th BC
		"Anacharsis", # 6th BC
		"Parmenides", # 5th BC
		"Philolaos", # 5th BC
		"fDiotima", # 5th BC
		"Epikouros", # 4th BC
		iIndustrial,
		"Emmanuel Metaxakis", # 19th
		iGlobal,
		"Georgios Karslidis", # 20th
		"Arsenios Eznepidis", # 20th
		"Porphyrios Bairaktaris", # 20th
	],
	iGreatArtist : [
		"Homeros", # 8th BC
		iClassical,
		"fSappho", # 6th BC
		"Sophokles", # 5th BC
		"Thoukydides", # 5th BC
		"Euripides", # 5th BC
		"Herodotos", # 5th BC
		"Aischylos", # 5th BC
		"Pheidias", # 5th BC
		"Anyte Tegeatis", # 3rd BC
		iIndustrial,
		"Dionysios Solomos", # 19th
		"Georgios Jakobides", # 19th
		iGlobal,
		"Nikos Kazantzakis", # 20th
		"fMaria Callas", # 20th
		"Odysseas Elytis", # 20th
		"Iannis Xenakis", # 20th
		"Mikis Theodorakis", # 20th
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
		iIndustrial,
		"Eugenios Voulgaris", # 18th
		iGlobal,
		"Konstantinos Karatheodori", # 20th
		"Georgios Papanikolaou", # 20th
		"Fotis Kafatos", # 20th
	],
	iGreatMerchant : [
		"Kolaios", # 7th BC
		"Sostratos", # 6th BC
		"Pytheas", # 4th BC
		"Androsthenes", # 4th BC
		"Megasthenes", # 4th BC
		"Hippalos", # 1st BC
		"Heroides Attikos", # 2nd
		iIndustrial,
		"fManto Mavrogenous", # 19th
		"Evangelos Zappas", # 19th
		iGlobal,
		"Aristotelis Onasis", # 20th
		"Stavros Niarchos", # 20th
		"fArianna Stasinopoulou", # 20th
	],
	iGreatEngineer : [
		"Thales", # 6th BC
		"Empedokles", # 5th BC
		"Zenon", # 4th BC
		"Satyros", # 4th BC
		"Archimedes", # 3rd BC
		"Heron", # 1st
		iIndustrial,
		"Ernestos Tsiller", # 19th
		iGlobal,
		"Alexandros Issigonis", # 20th
		"Ioannis Travlos", # 20th
		"Ioannis Argyris", # 20th
	],
	iGreatStatesman : [
		"Solon", # 6th BC
		"Kleisthenes", # 6th BC
		"fGorgo", # 5th BC
		"Alkibiades", # 5th BC
		"Kimon", # 5th BC
		"Isokrates", # 4th BC
		"Aresteides", # 4th BC
		iIndustrial,
		"Adamantios Korais", # 19th
		"Ioannis Kapodistrias", # 19th
		"Eleftherios Venizelos", # 19th
		iGlobal,
		"Ioannis Metaxas", # 20th
		"Konstantinos Karamanlis", # 20th
		"Michael Christodoulou Mouskos", # 20th
		"Andreas Papandreou", # 20th
	],
	iGreatGeneral : [
		"Hektor", # legendary
		iClassical,
		"Leonidas", # 6th BC
		"Themistokles", # 5th BC
		"Lysandros", # 5th BC
		"Philippos", # 4th BC
		"Pyrrhos", # 3rd BC
		"fArtemisia", # 4th BC
		iIndustrial,
		"fLaskarina Bouboulina", # 19th
		"Alexandros Ypsilantis", # 19th
		"Theodoros Kolokotronis", # 19th
		iGlobal,
		"Konstantinos Bakopoulos", # 20th
		"Alexandros Papagos", # 20th
	],
},
iCivIndia : {
	iGreatProphet : [
		"Mahavira", # 6th BC
		"Siddharta Gautama", # 6th BC
		"Ananda", # 6th BC
		"Mahakashyapa", # 6th BC
		"Nagarjuna", # 2nd
		iMedieval,
		"Adi Shankara", # 9th
		"Atisha", # 11th
		"Ramanuja", # 11th
		"Basava", # 12th
		"Kabir", # 15th
		iRenaissance,
		"Chaitanya Mahaprabhu", # 16th
		"fMeera", # 16th
		iIndustrial,
		"Ramakrishna", # 19th
		"Swami Vivekananda", # 19th
		"Shirdi Sai Baba", # 19th
		iGlobal,
		"Paramahansa Yogananda", # 20th
		"fAnandamayi Ma", # 20th
		"fAnjeze Gonxhe Bojaxhiu", # 20th
		"Maharishi Mahesh Yogi", # 20th
		"fNirmala Srivastava", # 20th
	],
	iGreatArtist : [
		"Valmiki", # 4th BC
		"Asvaghosa", # 1st
		"Kapilar", # 1st tamil
		"Kalidasa", # 5th
		iMedieval, 
		"Gunadhya", # 6th
		"fAvvaiyar", # 10th tamil
		"Abhinavagupta", # 10th
		"Nakkirar", # medieval tamil
		iRenaissance,
		"Purandara Dasa", # 15th
		"Tansen", # 16th
		"Nainsukh", # 18th
		iIndustrial,
		"Muthuswami Dikshitar", # 19th
		"Raja Ravi Varma", # 19th
		iGlobal,
		"Rabindranath Tagore", # 20th
		"Raja Rao", # 20th
		"fAmrita Sher-Gil", # 20th
		"Satyajit Ray", # 20th
		"Ravi Shankar", # 20th
	],
	iGreatScientist : [
		"Yajnavalkya", # 8th BC
		"Panini", # 6th or 5th BC
		"Charaka", # 6th to 2nd BC
		"Pingala", # 3rd or 2nd BC
		iMedieval,
		"Aryabhata", # 6th
		"Dignaga", # 6th
		"Dharmakirti", # 6th or 7th
		"Brahmagupta", # 7th
		"Bhaskara", # 12th
		"Madhava", # 14th
		iRenaissance,
		"Nilakantha Somayaji", # 15th
		"Kamalakara", # 17th
		iGlobal,
		"Chandrasekhara Venkata Raman", # 20th
		"Satyendra Nath Bose", # 20th
		"fAsima Chatterjee", # 20th
	],
	iGreatMerchant : [
		"Nattal Sahu", # 12th
		"Jagadu", # 13th
		iIndustrial,
		"Jamsetjee Jejeebhoy", # 19th
		"Jamsetji Tata", # 19th
		"Ardeshir Godrej", # 19th
		iGlobal,
		"Kappalottiya Tamizhan", # 20th
		"fIndra Nooyi", # 20th
	],
	iGreatEngineer : [
		"Baudhayana", # 8th BC
		"Lagadha", # 1st
		iMedieval, 
		"Gundan Anivaritachari", # 7th
		iRenaissance, 
		"Vidyadhar Bhattacharya", # 18th
		iIndustrial,
		"Jagadish Chandra Bose", # 19th
		"Mokshagundam Visvesvaraya", # 19th
		"Jamsetji Tata", # 19th
		iGlobal,
		"fEulie Chowdhury", # 20th
		"Satish Dhawan", # 20th
		"Charles Correa", # 20th
	],
	iGreatStatesman : [
		"Vishnu Sharma", # 12th BC to 3rd AD
		"Chanakya", # 4th BC
		"Thiruvalluvar", # 4th BC to 7th AD
		iMedieval,
		"Amoghavarsha", # 9th
		"Chavundaraya", # 10th
		"Rajaraja Chola", # 10th
		iRenaissance,
		"Ariyanatha Mudaliar", # 16th
		"Nana Fadnavis", # 18th
		"fBegum Samru", # 18th
		iIndustrial,
		"Ram Mohan Roy", # 19th
		"Ranjit Singh", # 19th
		iGlobal,
		"fSarojini Naidu", # 20th
		"Sarvepalli Radhakrishnan", # 20th
		"Bhimrao Ramji Ambedkar", # 20th
		"Jawaharlal Nehru", # 20th
	],
	iGreatGeneral : [
		"Chandragupta Maurya", # 4th BC
		"Samudragupta", # 4th BC
		iMedieval,
		"Dhruva Dharavarsha", # 8th
		"Mihira Bhoja", # 9th
		"Rajaraja Chola", # 10th
		iRenaissance,
		"fRani Durgavati", # 16th
		"Shivaji Bhosle", # 17th
		"Kanhoji Angre", # 17th
		"Marthanda Varma", # 18th
		"Hyder Ali", # 18th
		iIndustrial,
		"Nana Sahib", # 19th
		"fRani Lakshmibai", # 19th
		iGlobal, 
		"Kodandera M. Cariappa", # 20th
		"Sam Manekshaw", # 20th
	],
	iGreatSpy : [
		"Bahirji Naik", # 17th
		"fSharan Kaur Pabla", # 17th
		iIndustrial,
		"Sarat Chandra Das", # 19th
		iGlobal,
		"fNoor Inayat Khan", # 20th
		"Rameshwarnath Kao", # 20th
		"Ravindra Kaushik", # 20th
	],
},
iCivCarthage : {
	iGreatProphet : [
		"Sanchuniathon", # unknown date
		"fJezebel", # 9th BC
		iClassical,
		"Tertullianus", # 2nd
		"Cyprianus", # 3rd
		"Donatus", # 4th
	],
	iGreatArtist : [
		"fSapanbaal", # 3rd BC
		"Micipsa", # 2nd BC
		"Ennion", # 1st AD
	],
	iGreatScientist : [
		"Mochus", # 14th BC
		"Hiram", # 10th BC
		"Sanchuniathon", # unknown date
		iClassical,
		"Mago", # 4th BC
		"Hasdrubal Clitomachus", # 2nd BC
		"Abba", # 3rd
	],
	iGreatMerchant : [
		"Acerbas", # 9th BC / legendary
		iClassical,
		"Hanno", # 5th BC
		"Himilco", # 5th BC
		"Abdashtart", # 4th BC
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
		"Ashtar-rom", # 9th BC
		"Ithobaal", # 9th BC
		"Pygmalion", # 9th BC
		"fElishat", # 8th BC
		iClassical,
		"Hanno", # 4th BC
		"Eshmuniaton", # 4th BC
		"Azelmelek", # 4th BC
		"Bomilcar", # 3rd BC
	],
	iGreatGeneral : [
		"Hasdrubal Barca", # 3rd BC
		"Hamilcar Barca", # 3rd BC
		"Mago Barca", # 3rd BC
		"Carthalo", # 3rd BC
		"Maharbal", # 2nd BC
	],
},
iCivPolynesia : {
	iGreatProphet : [
		"Maui", # legendary
		"Kuamo'o Mo'okini", # 12th
		iIndustrial,
		"Te Kooti", # 19th
		"fAngata", # 19th
		"Rua Kenana Hepetipa", # 19th
	],
	iGreatArtist : [
		"Hawaiiloa", # legendary
		"Hotu Matu'a", # 4th-7th
		"Ui-te-Rangiora", # 7th
		"Kupe", # 10th-14th
		iIndustrial,
		"fKawena", # 20th
		"Uiliami Leilua Vi", # 20th
		"Rangi Hetet", # 20th
	],
	iGreatScientist : [
		"Nga'ara", # 19th
		"Te Rangi Hiroa", # 20th
		"Mau Piailug", # 20th
	],
	iGreatMerchant : [
		"Tupaia", # 18th
		"Mai", # 18th
		iIndustrial,
		"fPiipi Raumati", # 19th
		"Tuilaepa Aiono Sailele Malielegaoi", # 20th
	],
	iGreatEngineer : [
		"Olisihpa", # 12th
		"Tu'itatui", # 12th
		"Uluakimata", # 16th
	],
	iGreatStatesman : [
		"Talatama", # 12th
		"fSalamasina", # 15th
		"fKa'ahumanu", # 18th
		iIndustrial,
		"Haalilio", # 19th
		"fMeri Te Tai Mangakahia", # 19th
		"Apirana Ngata", # 19th
	],
	iGreatGeneral : [
		"fNafanua", # legendary
		"Momo", # 11th
		iRenaissance,
		"Kamehameha", # 18th
		iIndustrial,
		"Te Rauparaha", # 19th
		"Hone Heke", # 19th
		"Seru Epenisa Cakobau", # 19th
	],
},
iCivPersia : {
	iGreatProphet : [
		"Mahabad", # legendary
		"Zarathustra", # 18-10th BC
		iClassical,
		"Baga-data", # 3rd BC
		"Mani", # 3rd
		"Kartir", # 3rd
		"Mazdak", # 4th
		"Adurbad-i Mahrspandan", # 4th
		"Mar Aba", # 6th
		iMedieval,
		"Al-Muqanna", # 8th
		"Al-Ghazali", # 11th
		"Mevlana", # 13th
		iRenaissance,
		"Mulla Sadra", # 17th
		"Muhammad Baqir Majlisi", # 17th
		"Muhammad Baqir Behbahani", # 18th
		iIndustrial,
		u"Bahá'u'lláh", # 19th
		u"Báb", # 19th
		iGlobal,
		"Muhammad Husayn Tabataba'i", # 20th
		"Muhammad-Taqi Mesbah-Yazdi", # 20th
	],
	iGreatArtist : [
		"Pahlbod", # 7th
		"fNagisa", # 7th
		"Bamshad", # 7th
		iMedieval,
		"Rudaki", # 9th
		"Ferdowsi", # 10th
		"fRabia Balkhi", # 10th
		"Nizami Ganjavi", # 12th
		"Farid al-Din Attar", # 12th
		"Safi al-Din", # 13th
		"Saadi", # 13th
		"Rumi", # 13th
		"Nur ad-Din Abd ar-Rahman Jami", # 15th
		iRenaissance,
		"Kamal ud-Din Behzad", # 15th
		"Reza Abbasi", # 17th
		"Mesrop", # 17th
		iIndustrial,
		"Mihr 'Ali", # 19th
		iGlobal,
		"fForough Farrokhzad", # 20th
		"Hossein Amanat", # 20th
		"fHayedeh", # 20th
	],
	iGreatScientist : [
		"Ktesias", # 5th BC
		"Ardashir", # 4th
		"Borzuya", # 6th
		"Paulos-e irani", # 6th
		iMedieval,
		"Al-Khwarizmi", # 9th
		"Muhammad ibn Zakariya al-Razi", # 9th
		"Ibn Miskawayh", # 10th
		"Ibn Sina", # 10th
		"Abd al-Rahman al-Sufi", # 10th
		"Omar Khayyam", # 11th
		"Kamal al-Din al-Farisi", # 13th
		"Qutb al-Din al-Shirazi", # 13th
		iRenaissance,
		"Al-Birjandi", # 16th
		"Baha al-din al-Amili", # 16th
		"Qazi Sa'id Qumi", # 17th
		"Alavi Shirazi", # 17th
		iGlobal,
		"Mahmoud Hessaby", # 20th
		"Ali Javan", # 20th
		"Cumrun Vafa", # 20th
	],
	iGreatMerchant : [
		"Kroisos", # 6th BC
		"Athurpat", # 4th BC
		"Kavadh", # 5th
		iMedieval,
		"Ahmad ibn Rustah", # 10th
		"Istakhri", # 10th
		iGlobal,
		"Manny Mashouf", # 20th
		"Nasser David Khalili", # 20th
		"Omid Kordestani", # 20th
		"Amir Ansari", # 20th
		"Pierre Omidyar", # 20th
	],
	iGreatEngineer : [
		"Artakhshathra", # 4th BC
		"Bahram", # 3rd
		"Sanimar", # 6th
		iMedieval,
		"Naubakht", # 8th or 9th
		"Al-Khujandi", # 10th
		"Ibn al-Haitham", # 10th
		"Nasir al-Din al-Tusi", # 13th
		iRenaissance,
		"Sheikh Baha'i", # 16th
		"Ustad Mirza Shirazi", # 18th
		iIndustrial,
		"Abdallah Khan", # 19th
		iGlobal,
		"Firouz Naderi", # 20th
		"Gholam Reza Aghazadeh", # 20th
		"Caro Lucas", # 20th
		"Siavash Alamouti", # 20th
		"fAnousheh Ansari", # 20th
	],
	iGreatStatesman : [
		"Chithrafarna", # 5th BC
		"Tiribazus", # 4th BC
		"Bagoi", # 4th BC
		"Tiridat", # 1st
		"Bozorgmehr", # 6th
		"fPurandokht", # 7th
		iMedieval,
		"Ibn Miskawayh", # 10th
		"Nizam al-Mulk", # 11th
		iRenaissance,
		"Tahmasp", # 16th
		"Mirza Salman Jaberi", # 17th
		"Khalifeh Soltan", # 17th
		iIndustrial,
		"Ebrahim Khan Kalantar", # 19th
		"Kuchik Khan", # 19th
		"Amir Kabir", # 19th
		iGlobal,
		"Reza Shah Pahlavi", # 20th
		"Mohammad Mossadegh", # 20th
	],
	iGreatGeneral : [
		"Haxamanis", # 7th BC
		"Khashayarsha", # 5th BC
		"fMania", # 4th BC
		"Mithradata", # 1st BC
		"Shapur", # 3rd
		"Rostam Farrokhzad", # 7th
		iRenaissance,		
		"Shah Ismail", # 16th
		"Mohammad Khan Qajar", # 18th
		iIndustrial,
		"Ahmad Amir-Ahmadi", # 19th
		iGlobal,
		"Bahram Aryana", # 20th
		"Muhammad-Husayn Ayrom", # 20th
		"Ali-Reza Asgari", # 20th
		"Mohammad Ali Jafari", # 20th
	],
},
iCivRome : {
	iGreatProphet : [
		"fClaudia Quinta", # 3rd BC
		"Petrus", # 1st
		"Paulus Tarsensis", # 1st
		"Augustinus Hipponensis", # 4th
		"Aurelius Ambrosius", # 4th
		"Eusebius Pamphili", # 4th
		"fMarcella", # 4th
	],
	iGreatArtist : [
		"Publius Vergilius Maro", # 1st BC
		"fIaia", # 1st BC
		"Titus Livius", # 1st
		"Publius Ovidius Naso", # 1st
		"Plutarchus", # 1st
		"Decimus Iunius Iuvenalis", # 2nd
	],
	iGreatScientist : [
		"Marcus Terentius Varro", # 1st BC
		"Titus Lucretius Carus", # 1st BC
		"Sosigenes", # 1st BC
		"Antonius Castor", # 1st
		"Gaius Plinius Secundus", # 1st
		"Strabo", # 1st
		"Lucius Annaeus Seneca", # 1st
	],
	iGreatMerchant : [
		"Marcus Crassus", # 1st BC
		"Publius Sittius", # 1st BC
		"Titus Pomponius Atticus", # 1st BC
		"Lucius Caecilius Iucundus", # 1st
	],
	iGreatEngineer : [
		"Sergius Orata", # 2nd BC
		"Marcus Vitruvius Pollio", # 1st BC
		"Celer", # 1st AD
		"Marcus Vipsanius Agrippa", # 1st AD
		"Sextus Julius Frontinus", # 1st AD
		"Apollodorus Damascenus", # 2nd AD
	],
	iGreatStatesman : [
		"Publius Valerius Publicola", # 6th BC
		"Lucius Quinctius Cincinnatus", # 5th BC
		"Quintus Hortensius", # 3rd BC
		"Marcus Porcius Cato", # 2nd BC
		"Marcus Tullius Cicero", # 1st BC
		"Lucius Cornelius Sulla", # 1st BC
		"fLivia Drusilla", # 1st BC
		"fFulvia", # 1st AD
		"Diocletianus", # 3rd
	],
	iGreatGeneral : [
		"Scipio Africanus", # 2nd BC
		"Gaius Marius", # 2nd BC
		"Gnaeus Pompeius Magnus", # 1st BC
		"Vaspasianus", # 1st
		"Traianus", # 1st
		"fAgrippina", # 1st AD
		"Hadrianus", # 2nd
		"fAlbia Dominica", # 4th AD
	],
},
iCivEthiopia : {
	iGreatProphet : [
		"Gabra Manfas Qeddus", # legendary
		"Fremnatos", # 4th
		"Abba Pantelewon", # 5th
		"Abuna Aregawi", # 6th
		iMedieval,
		"Tekle Haymanot", # 13th
		"Ewostatewos", # 14th
		"Abba Samuel", # 14th
		"fKristos Samra", # 15th
		iRenaissance,
		"fWalatta Petros", # 17th
		iGlobal,
		"Abune Tewophilos", # 20th
	],
	iGreatArtist : [
		"Yared", # 6th
		iMedieval,
		"Giyorgis Saglawi", # 14th
		iIndustrial,
		"Gebre Hanna", # 19th
		"Afevork Ghevre Jesus", # 19th
		iGlobal,
		"Gebre Kristos Desta", # 20th
		"Tsegaye Gabre-Medhin", # 20th
		"Adamu Tesfaw", # 20th
		"Afeworq Tekle", # 20th
		"Alexander Boghossian", # 20th
	],
	iGreatScientist : [
		"Zar'a Ya'aqob", # 16th
		"Abba Bahriy", # 16th
		"Walda Heywat", # 17th
		"Abba Gorgoryos", # 17th
		iGlobal,
		"Aklilu Lemma", # 20th
		"Kitaw Ejigu", # 20th
		"Sossina Haile", # 20th
		"Gebisa Ejeta", # 20th
	],
	iGreatMerchant : [
		"Nigiste Saba", # legendary
		"Endubis", # 3rd
		iMedieval,
		"Yusuf bin Ahmad al-Kawneyn", # 13th
		iGlobal,
		"Berhanu Nega", # 20th
		"Eleni Gebre-Medhin", # 20th
		"Mohammed Al Amoudi", # 20th
	],
	iGreatEngineer : [
		"Ezana", # 4th
		iMedieval,
		"Gebre Mesqel Lalibela", # 13th
		iRenaissance,
		"Fasiladas", # 17th
	],
	iGreatStatesman : [
		"Ezana", # 4th
		iRenaissance,
		"fEleni", # 16th
		"Susenyos", # 17th
		iIndustrial,
		"Tewodros", # 19th
		"Menelik", # 19th
		iGlobal,
		"Mengistu Haile Mariam", # 20th
		"Meles Zenawi", # 20th
	],
	iGreatGeneral : [
		"Gadarat", # 2nd or 3rd
		"Abraha", # 6th
		iMedieval,
		"fGudit", # 10th
		"Yekuno Amlak", # 13th
		"Amda Seyon", # 14th
		"Eskender", # 15th
		"Tewodros", # 15th
		iRenaissance,
		"Lebna Dengel", # 16th
		"Iyasu", # 17th
		iIndustrial,
		"Yohannis", # 19th
		"Alula Engida", # 19th
		iGlobal,
		"Aman Andom", # 20th
	],
},
iCivKorea : {
	iGreatProphet : [
		"Jinul", # 12th
		"Uicheon", # 12th
		"Baegun", # 13th
		"An Hyang", # 13th
		iRenaissance,
		"Yi Hwang", # 16th
		"Yi I", # 16th
		iIndustrial,
		"Choe Je-u", # 19th
		iGlobal,
		"Sun Myung Moon", # 20th
	],
	iGreatArtist : [
		"Damjing", # 7th
		"Yi Nyeong", # 9th
		"Yi Je-hyeon", # 9th
		iRenaissance,
		"Hwang Jip-jung", # 16th
		"fHeo Nanseolheon", # 16th
		"Yan Duseo", # 17th
		"Kim Hong-do", # 18th
		"Jeong Seon", # 18th
		"Shin Yun-bok", # 18th
		iGlobal,
		"Im Kwon-taek", # 20th
		"Seo Tae-Ji", # 20th
	],
	iGreatScientist : [
		"Uisan", # 7th
		"Wonhyo", # 7th
		iRenaissance,
		"Jeong Inji", # 15th
		"Seong Sammun", # 15th
		"Yu Seong-won", # 15th
		"Heo Jun", # 16th
		iIndustrial,
		"Jeong Yakyong", # 19th
		iGlobal,
		"Hwang Woo-Suk", # 20th
	],
	iGreatMerchant : [
		"Hyecho", # 8th
		"Kim Sa-hyeong", # 15th
		"Yi Mu", # 15th
		"Yi Hoe", # 15th
		iGlobal,
		"Lee Byung-chul", # 20th
		"Chung Ju-yung", # 20th
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
		"Jeong Dojeon", # 14th
		iRenaissance,
		"Yi Hwang", # 16th
		iIndustrial,
		"Kim Ok-gyun", # 19th
		"fMyeongseong", # 19th
		iGlobal,
		"fRyu Gwansun", # 20th
		"Kim Gu", # 20th
		"Kim Dae-jung", # 20th
	],
	iGreatGeneral : [
		"Gim Yu-sin", # 7th
		"Gang Gam-chan", # 11th
		"Choe Woo", # 13th
		"Yi Seong-gye", # 14th
		iRenaissance,
		"Yi Sun-sin", # 16th
	],
	iGreatSpy : [
		"An Jung-geun", # 20th
		"Kim Chang-ryong", # 20th
	],
},
iCivMaya : {
	iGreatProphet : [
		"Junajpu", # mythological
		"Xb'alanke", # mythological
		"Kukulkan", # 10th, named after the god
		"Ce Acatl Topiltzin", # 10th toltec
	],
	iGreatArtist : [
		"Uaxaclajuun Ub'aah K'awiil", # 8th
		"Chakalte'", # 8th
		"Jun Nat Omootz", # 8th
		"Asan Winik Tu'ub", # 8th
		"Chan Ch'ok Wayib Xok", # 8th
		"Waj Tan Chak", # 8th
		iGlobal,
		"fMarisol Ceh Moo", # 20th
	],
	iGreatScientist : [
		"Itzamna", # mythological
		"Huematzin", # 8th toltec
		"Papantzin", # 9th toltec
	],
	iGreatMerchant : [
		"Ek Chuaj", # mythological
		"Apoxpalon", # 16th
		"Tabscoob", # 16th
	],
	iGreatEngineer : [
		"Chan Imix K'awiil", # 7th
		"fK'ab'al Xook", # 8th
		"Ha' K'in Xook", # 8th
		"Itzam K'an Ahk", # 8th
		"K'inich Yat Ahk", # 8th
	],
	iGreatStatesman : [
		"Yax Ehb Xook", # 1st
		"fYohl Ik'nal", # 6th
		"Yuknoom Ch'een", # 7th
		"Jasaw Chan K'awiil", # 8th
		iGlobal,
		u"fRigoberta Menchú", # 20th
	],
	iGreatGeneral : [
		"Siyaj K'ak'", # 4th teotihuacan
		"K'inich Yo'nal Ahk", # 7th
		"fXochitl", # 9th toltec
		"Hunac Ceel", # 12th
		iRenaissance,
		"Napuc Chi", # 16th
		"Tecun Uman", # 16th
	],
},
iCivByzantium : {
	iGreatProphet : [
		"Nestorios", # 5th
		"fTheodora", # 6th
		"Ioannis o Damaskinos", # 8th
		"Kyrillos", # 9th
		"Methodios", # 9th
		"Photios", # 9th
		"Nikolaos Mystikos", # 10th
		"Athanasios o Athonites", # 10th
		"Ioannes Xiphilinos", # 11th
	],
	iGreatArtist : [
		"fAelia Eudocia", # 5th
		"Romanos o Melodos", # 6th
		"Flauios Dioskoros", # 6th
		"fKassia", # 9th
		"Theodoros Prodromos", # 12th
		"Eulalios", # 12th
		"Manuel Chrysoloras", # 14th
		iRenaissance,
		"Theophanes Strelitzas", # 16th
		"Domenikos Theotokopoulos", # 16th
		"Petros Bereketis", # 17th
	],
	iGreatScientist : [
		"fHypatia", # 4th
		"Stephanos Alexandrinos", # 7th
		"Theophylaktos Simokates", # 7th
		"Leon o Mathematikos", # 9th
		"Michael Psellos", # 11th
		"fAnna Komnene", # 12th
		"Nikephoros Blemmydes", # 13th
		"Niketas Choniates", # 13th
		"Nikephoros Gregoras", # 14th
		"Georgios Plethon", # 15th
	],
	iGreatMerchant : [
		"Hierokles", # 6th
		"Zemarchos", # 6th
		"Kosmas Indikopleustes", # 6th
		"Georgios Kyprios", # 7th
		"fDanielis", # 9th
	],
	iGreatEngineer : [
		"Anthemios", # 6th
		"Isidoros", # 6th
		"Eutokios", # 6th
		"Kallinikos", # 7th
		"Petronas Kamateros", # 9th
		"Tiridates", # 10th
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
		"Nikephoros Phokas", # 10th
		"Ioannis Kourkouas", # 10th 
		"Basileios Bulgaroktonos", # 11th
		"Georgios Maniakes", # 11th
		"Michael Palaiologos", # 12th
		"Nikephoros Bryennios", # 12th
		"Andronikos Kontostephanos", # 12th
		"Alexios Strategopoulos", # 13th
	],
},
iCivJapan : {
	iGreatProphet : [
		"En no Ozunu", # 7th
		"Kuukaii", # 8th
		"Saichou", # 8th
		"Abe no Seimei", # 10th
		"Myouan Eisai", # 12th
		"Shinran", # 13th
		"Nikkou", # 13th
		"Nichiren", # 13th
		iRenaissance,
		"Rennyo", # 15th
		"Ikkyuu Soujun", # 15th
		"Takuan Souhou", # 17th
		"Ryoukan", # 18th
		iIndustrial,
		"Hirata Atsutane", # 19th
		"fMiki Nakayama", # 19th,
		"Kanzou Uchimura", # 19th
	],
	iGreatArtist : [
		"Kakinomoto no Hitomaro", # 7th
		"Yamanoue no Okura", # 7th
		"Ootomo no Yakamochi", # 8th
		"Ki no Tsurayuki", # 9th
		"fMurasaki Shikibu", # 10th
		"Unkei", # 12th
		"Saigyou", # 12th
		"Zeami", # 14th
		"Sesshuu", # 15th
		iRenaissance,
		"Kanou Eitoku", # 16th
		"Sen no Rikyuu", # 16th
		"Ihara Saikaku", # 17th
		"Matsuo Bashou", # 17th
		"Chikamatsu Monzaemon", # 17th
		"Toushuusai Sharaku", # 18th
		"Yosa Buson", # 18th
		"Kobayashi Issa", # 18th
		iIndustrial,
		"Kyokutei Bakin", # 19th
		"Katsushika Hokusai", # 19th
		"Utagawa Hiroshige", # 19th
		"fIchiyou Higuchi", # 19th
		"Masaoka Shiki", # 19th
		iGlobal,
		"fAkiko Yosano", # 20th
		"Osamu Dazai", # 20th
		"Miyazawa Kenji", # 20th
		"Yukio Mishima", # 20th
		"Yasunari Kawabata", # 20th
		"Osamu Tezuka", # 20th
		"Tsuburaya Eiji", # 20th
		"Hayao Miyazaki", # 20th
		"Toro Okamoto", # Contest Reward
	],
	iGreatScientist : [
		"Yoshida Mitsuyoshi", # 17th
		"Takakazu Seki", # 17th
		"Aida Yasuaki", # 18th
		"Sugita Genpaku", # 18th
		iIndustrial,
		"Ogata Kouan", # 19th
		"Shibasaburou Kitasato", # 19th
		iGlobal,
		"Hideyo Noguchi", # 20th
		"Kiyoshi Shiga", # 20th
		"Kumagusu Minakata", # 20th
		"Kiyoshi Itou", # 20th
		"Hideki Yukawa", # 20th
		"Shinichirou Tomonaga", # 20th
		"Masatoshi Koshiba", # 20th
		"Kenkichi Iwasawa", # 20th
	],
	iGreatMerchant : [
		"Ruson Sukezaemon", # 16th
		"Yodoya Juutou", # 17th
		"Mitsui Takatoshi", # 17th
		"Shousuke Tanaka", # 17th
		"Kounoike Zenzaemon", # 17-20th (Zaibatsu hereditary name)
		"Sumitomo Kichizaemon", # 17-20th
		"Takadaya Kahei", # 18th
		iIndustrial,
		"Torakusu Yamaha", # 19th
		"Outano Kouzui", # 19th
		"Yatarou Iwasaki", # 19th 
		"Zenjirou Yasuda", # 19th
		iGlobal,
		"Masahisa Fujita", # 20th
		"Kiichiro Toyoda", # 20th
		"Soichiro Honda", # 20th
		"Yoshitaka Fukuda", # 20th
	],
	iGreatEngineer : [
		"Gyouki", # 8th
		"Yaita Kinbee", # 16th
		"Yasui Douton", # 16th
		"Hiraga Gennai", # 18th
		iIndustrial,
		"Tanaka Hisashige", # 19th
		"Katayama Toukuma", # 19th
		"Takeda Ayasaburou", # 19th
		"Sakichi Toyoda", # 19th
		iGlobal,
		"Koutarou Honda", # 20th
		"Ken Sakamura", # 20th
		"Kyota Sugimoto", # 20th
		"Hidetsugu Yagi", # 20th
		"Shigeru Miyamoto", # 20th
	],
	iGreatStatesman : [
		"Shoutouku Taishi", # 6th
		"Fujiwara no Michinaga", # 11th
		"Taira no Kiyomori", # 12th
		"fHoujou Masako", # 12th
		"Ashikaga Yoshimitsu", # 14th
		iRenaissance,
		"Tokugawa Ieyasu", # 16th
		"Tsunenaga Hasekura", # 17th
		"Arai Hakuseki", # 17th
		"Tanuma Okitsugu", # 18th
		iIndustrial,
		"Sakamoto Ryouma", # 19th
		"Oukubo Toshimichi", # 19th
		"Yukichi Fukuzawa", # 19th
		iGlobal,
		"Yukio Ozaki", # 20th
		"Korekiyo Takahashi", # 20th
		"Shigeru Yoshida", # 20th
		"fSadako Ogata", # 20th
	],
	iGreatGeneral : [
		"Fujiwara no Kamatari", # 7th
		"Sakanoue no Tamuramaro", # 8th
		"Taira no Masakado", # 10th
		"Minamoto no Yoritomo", # 12th
		"Kusunoki Masashige", # 13th
		"Ashikaga Takauji", # 14th
		iRenaissance,
		"Houjou Souun", # 16th
		"Takeda Shingen", # 16th
		"Shimazu Yoshihiro", # 16th
		"fTachibana Ginchiyo", # 16th
		"Toyotomi Hideyoshi", # 16th
		iIndustrial,
		"fNakano Takeko", # 19th
		"Tougou Heihachirou", # 19th
		"Yoshifuru Akiyama", # 19th
		"Gonnohyoue Yamamoto", # 19th
		iGlobal,
		"Isoroku Yamamoto", # 20th
		"Tomoyuki Yamashita", # 20th
	],
	iGreatSpy : [
		"Kagetoki Kajiwara", # 12th
		"Hino Kumawaka", # 14th
		iRenaissance,
		"Hanzou Hattori", # 16th
		"fChiyome Mochizuki", # 16th
		"Ishikawa Goemon", # 16th
		iIndustrial,
		"Mamiya Rinzou", # 18th
		"Nezumi Kozou", # 19th
		"Akashi Motojiro", # 19th
		iGlobal,
		"fYoshiko Kawashima", # 20th
		"Takeo Yoshikawa", # 20th
		"Keiji Suzuki", # 20th
	],
},
iCivVikings : {
	iGreatProphet : [
		"Ansgar", # 9th swedish
		u"Haraldr Blátonn", # 10th danish
		"Erik den Helige", # 11th swedish
		"fBirgitta Birgersdotter", # 13th swedish
		iRenaissance,
		"Johannes Campanius", # 17th swedish
		"Emanuel Swedenborg", # 18th swedish
		iIndustrial,
		u"Søren Kierkegaard", # 19th danish
		iGlobal,
		u"Sveinbjörn Beinteinsson", # 20th icelandic
	],
	iGreatArtist : [
		"Bragi Boddason", # 9th norwegian
		"Snorri Sturluson", # 13th icelandic
		u"Nils Håkansson", # 14th swedish
		iRenaissance,
		"Georg Stiernhielm", # 17th swedish
		"Johan Nordahl Brun", # 18th norwegian
		iIndustrial,
		"Hans Christian Andersen", # 19th danish
		"Olav Duun", # 19th norwegian
		"Johan Ludvig Runeberg", # 19th finnish
		"fJohanna Maria Lind", # 19th swedish
		"Edvard Munch", # 19th norwegian
		"Edvard Grieg", # 19th norwegian
		iGlobal,
		"Jean Sibelius", # 20th finnish
		"fKaren Blixen", # 20th danish
		"fAstrid Lindgren", # 20th swedish
		"Ingmar Bergman", # 20th swedish
	],
	iGreatScientist : [
		"Tycho Brahe", # 16th danish
		"fSophia Brahe", # 16th danish
		"Mikael Agricola", # 16th finnish
		u"Ole Rømer", # 17th  danish
		"Anders Celsius", # 18th swedish
		u"Carl von Linné", # 18th swedish
		iIndustrial,
		u"Jöns Jacob Berzelius", # 19th swedish
		"Niels Henrik Abel", # 19th norwegian
		"Johannes Rydberg", # 19th swedish
		u"Anders Ångström", # 19th swedish
		iGlobal,
		"Niels Bohr", # 20th danish
	],
	iGreatMerchant : [
		u"Eiríkr Rauði", # 10th norwegian
		u"Leifr Eiríksson", # 10th icelandic
		u"Håkon Sigurdsson", # 10th norwegian
		iRenaissance,
		"fSigbrit Willoms", # 16th danish
		"fChristina Piper", # 18th swedish
		"Niclas Sahlgren", # 18th swedish
		"Rutger Macklean", # 18th swedish
		iIndustrial,
		"Sven Hedin", # 19th swedish
		"Roald Amundsen", # 20th norwegian
		iGlobal,
		"Ole Kirk Christiansen", # 20th danish
		"Ingvar Kamprad", # 20th swedish
	],
	iGreatEngineer : [
		"Hercules von Oberberg", # 16th danish
		"Nicodemus Tessin", # 17th swedish
		"Christopher Polhem", # 18th swedish
		iIndustrial,
		"Johan Ericsson", # 19th swedish
		"Per Georg Scheutz", # 19th swedish
		"Alfred Nobel", # 19th swedish
		"Lars Magnus Ericsson", # 19th swedish
		iGlobal,
		"Arne Jacobsen", # 20th danish
		u"Jørn Utzon", # 20th danish
		u"Ivar Giæver", # 20th norwegian
	],
	iGreatStatesman : [
		"Gorm den Gamle", # 10th danish
		"Birger Jarl", # 13th swedish
		"fMargrete Valdemarsdatter", # 14th danish
		iRenaissance,
		"Gustav Vasa", # 16th swedish
		"Axel Oxenstierna", # 17th swedish
		"fKristina", # 17th swedish
		"Peter Estenberg", # 18th swedish
		"Arvid Horn", # 18th swedish
		iIndustrial,
		"Gustaf Mauritz Armfelt", # 19th finnish
		"Nikolaj Frederik Severin Grundtvig", # 19th danish
		iGlobal,
		"Trygve Lie", # 20th norwegian
		u"Dag Hammarskjöld", # 20th swedish
		"Olof Palme", # 20th swedish
	],
	iGreatGeneral : [
		u"Eiríkr Blóðøx", # 10th norwegian
		u"Sveinn Tjúguskegg", # 10th danish
		u"Harald Harðráði", # 11th norwegian
		"Knutr", # 11th danish
		iRenaissance,
		"Gustav Vasa", # 16th swedish
		"Lennart Torstensson", # 17th swedish
		"Peter Tordenskjold", # 18th norwegian
		"fIngela Gathenhielm", # 18th swedish
		iGlobal, 
		"Carl Gustaf Emil Mannerheim", # 20th finnish
		"Carl Gustav Fleischer", # 20th norwegian	
	],
	iGreatSpy : [
		"fBrita Tott", # 15th swedish/danish
		"fCharlotte Eckerman", # 18th swedish
		u"fEva Löwen", # 18th swedish
		iGlobal,
		"Carlos Adlercreutz", # 20th swedish
		"Kai Henning Bothildsen Nielsen", # 20th danish
		u"fAstrid Døvle", # 20th norwegian
		"Stig Bergling", # 20th swedish
	],
},
iCivTurks : {
	iGreatProphet : [
		"Tatpar Qaghan", # 6th
		"Bulan", # 9th
		"Abu Mansur al-Maturidi", # 9th
		"Muhammad al-Bukhari", # 9th
		"Al-Ghazali", # 11th (also Persian)
		"Ahmad Yasawi", # 12th
		"fFatima al-Samarqandi", # 12th
		"Haji Bektash Veli", # 13th
	],
	iGreatArtist : [
		"Yusuf Balasaguni", # 11th
		"Suzani Samarqandi", # 12th
		"Nizami Ganjavi", # 12th (also Persian)
		"Rumi", # 13th (also Persian)
		"Izzeddin Hasanoglu", # 13-14th
		"Imadaddin Nasimi", # 14th
		"Alisher Nava'i", # 15th
		iRenaissance,
		"Khasta Qasim", # 18th
		"Magtymguly Pyragy", # 18th
		iIndustrial,
		"Qurmangazy Sagyrbaiuly", # 19th
		"Abai Qunanbaiuly", # 19th
		"fNodira", # 19th
		iGlobal,
		"Hamza Hakimzade Niyazi", # 20th
		"G'afur G'ulom", # 20th
		"Chinghiz Aitmatov", # 20th
	],
	iGreatScientist : [
		"Al-Farabi", # 10th (also Arab)
		"Ismail ibn Hammad al-Jawhari", # 10th
		"Ibn Sina", # 10th (also Persian)
		"Omar Khayyam", # 11th (also Persian)
		"Mahmud al-Kashgari", # 11th
		"Nizami Aruzi", # 12th
		"Qadi Zada al-Rumi", # 14th
		"Jamshid al-Kashi", # 15th
		"Ulugh Beg", # 15th (also Mongol)
		"Ali Qushji", # 15th (also Ottoman)
		iIndustrial,
		"Shoqan Walikhanov", # 19th
		iGlobal,
		"Kasym Tynystanov", # 20th
	],
	iGreatMerchant : [
		"Maniakh", # 6th
		"Muqan Qaghan", # 6th
		"Sheguy", # 7th
		"Ahmad ibn Rustah", # 10th
		"Bar Sauma", # 13th 
		"Yahballaha", # 13th
	],
	iGreatEngineer : [
		"Omurtag", # 9th
		"Abu-Mahmud Khojandi", # 10th
		"Al-Biruni", # 11th 
		"fSaray Mulk", # 14th
		iGlobal,
		"Kanysh Satbayev", # 20th
	],
	iGreatStatesman : [
		u"Istämi", # 6th
		"Ishbara Qaghan", # 6th
		"Ashina Simo", # 7th
		"Nizam al-Mulk", # 11th
		"fTerken Khatun", # 11th
		"Aq Sunqur al-Hajib", # 11th
		"Abd-al-Razzaq Samarqandi", # 15th
		"Muhammad Shaybani", # 15th
		iRenaissance,
		"Abdullah Khan", # 16th
		iIndustrial,
		"Alikhan Bukeikhanov", # 19th
		iGlobal,
		"Sopubek Begaliev", # 20th
	],
	iGreatGeneral : [
		"Tong Yabghu Qaghan", # 7th
		"Qapaghan Qaghan", # 7th
		u"Kültigin", # 8th
		"Tughril", # 11th (distinct from Mongol Toghril)
		"Anushtegin Gharchai", # 11th
		"Nur ad-Din Zengi", # 13th (also Arab) 
		"Uzun Hasan", # 15th
		iRenaissance,
		"Ablai Khan", # 18th
		"Raiymbek Batyr", # 18th
		iGlobal,
		"Sobir Rakhimov", # 20th
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
		"Ibn al-Jawzi", # 12th
		iRenaissance,
		"Al-Suyuti", # 15th
		"Abdullah ibn Alawi al-Haddad", # 17th
		"Muhammad ibn Abd al-Wahhab", # 18th
		iIndustrial, 
		"Muhammad Abduh", # 19th
	],
	iGreatArtist : [
		"Ibn Muqla", # 10th
		"Ibn al-Nadim", # 10th
		"Al-Mutanabbi", # 10th
		"Muhammad ibn al-Zayn", # 14th
		iRenaissance,
		"Ibn Furtu", # 16th
		iGlobal,
		"Muhammad al-Maghut", # 20th
	],
	iGreatScientist : [
		"Al-Kindi", # 9th
		"Al-Khwarizmi", # 9th (also Persian)
		"Al-Farabi", # 10th
		"Ibrahim ibn Sinan", # 10th
		"Ibn al-Jazzar", # 10th
		"Ibn al-Haytam", # 11th
		"Ibn al-Nafis", # 13th
		iGlobal, 
		"Abdul Jabbar Abdullah", # 20th
		"Ahmed Zewail", # 20th
	],
	iGreatMerchant : [
		"Muhammad ibn al-Zayyat", # 9th
		"Ibn Hawqal", # 10th
		"Abu'l Abbas al-Hijazi", # 12th
		"Yaqut al-Hamawi", # 13th
		iRenaissance,
		"Ahmad ibn Majid", # 15th
		"Sulaiman Al Mahri", # 16th
		iIndustrial, 
		"David Sassoon", # 19th
		"Sassoon Eskell", # 19th
		iGlobal, 
		"Mohammed bin Awad bin Laden", # 20th
	],
	iGreatEngineer : [
		"Jabir ibn Hayyan", # 8th
		"Mashallah ibn Athari", # 8th
		"Banu Musa", # 9th
		"Ibn Wahshiyah", # 10th
		"fMariam al-Astrulabi", # 10th
		"Al-Jazari", # 12th
		iGlobal,
		"Hassan Fathy", # 20th
		"fZaha Hadid", # 20th
	],
	iGreatStatesman : [
		"fFatimah bint Muhammad", # 7th
		"Al-Jahiz", # 9th
		"Al-Mawardi", # 11th
		"Izz al-Din Usama", # 12th
		iRenaissance,
		"Muhammad ibn Saud", # 18th
		iIndustrial,
		"Hussein bin Ali", # 19th
		iGlobal,
		"Zayed bin Sultan Al Nahyan", # 20th
		"Yasser Arafat", # 20th
		"Hisham Nazer", # 20th
	],
	iGreatGeneral : [
		"Khalid ibn al-Walid", # 7th
		"Muawiyah", # 7th
		"Ziyad ibn Abih", # 7th
		"Amr ibn al-As", # 7th
		"fKhawla bint al-Azwar", # 7th
		"Nur ad-Din Zengi", # 12th
		iRenaissance,
		"Rahmah ibn Jabir Al Jalhami", # 18th
		iGlobal, 
		"Abd al-Karim Qasim", # 20th
	],
	iGreatSpy : [
		"Hassan-i Sabbah", # 11th
		"Rashid ad-Din Sinan", # 12th
		iGlobal, 
		"Ali Hassan al-Majid", # 20th
	],
},
iCivTibet : {
	iGreatProphet : [
		"Gendun Drup", # 15th
		"Gendun Gyatso", # 15-16th
		"Sonam Gyatso", # 16th
		"Yonten Gyatso", # 16-17th
		"Tsangyang Gyatso", # 17th
		iGlobal,
		"Tenzin Gyatso", # 20th
	],
	iGreatArtist : [
		"fYeshe Tsogyal", # 8th
		"Milarepa", # 11th
		iRenaissance,
		u"Chöying Dorje", # 17th
		"Situ Panchen", # 18th
		iIndustrial,
		u"Gendün Chöphel", # 20th
	],
	iGreatScientist : [
		"Thonmi Sambhota", # 7th
		"Yuthog Yontan Gonpo", # 8th and 12th
		"Tsongkhapa", # 14th
		iRenaissance,
		"Kunkhyen Pema Karpo", # 16h
		iIndustrial,
		"Khyenrab Norbu", # 20th
	],
	iGreatMerchant : [
		"Sonam Rapten", # 17th
		iIndustrial,
		"Tsarong", # 20th
	],
	iGreatEngineer : [
		"Rinchen Zangpo", # 10th
		"Thang Tong Gyalpo", # 15th
		iRenaissance,
		"Desi Sangye Gyatso", # 17th
	],
	iGreatStatesman : [
		u"fThrimalö", # 7th
		u"Gar Tongsten Yülsung", # 7th
		iIndustrial,
		"Paljor Dorje Shatra", # 19th
		"Lhalu Tsewang Dorje", # 20th
	],
	iGreatGeneral : [
		"Gar Trinring Tsendro", # 7th
		"Chimshang Gyalsig Shuteng", # 8th
		"Nganlam Takdra Lukhong", # 8th
		"Nanam Shang Gyaltsen Lhanang", # 8th
		iRenaissance,
		"Ngawang Namgyal", # 17th
	],
},
iCivIndonesia : {
	iGreatProphet : [
		"Maha Rsi Agastya", # 5th
		"Buddha Pahyien", # 4th
		"Sakyakirti", # 7th
		"fGayatri Rajapatni", # 14th
		iRenaissance,
		"Sunan Giri", # 15th
		"Sunan Gunung Jati", # 16th
		iIndustrial, 
		"Ahmad Dahlan", # 19th
		iGlobal,
		"Albertus Soegijapranata", # 20th
	],
	iGreatArtist : [
		"Abdullah Abdul Kadir", # 19th
		"Raja Ali Haji", # 19th
		iGlobal,
		"Amir Hamzah", # 20th
		"Ismail Marzuki", # 20th
		"Pramoedya Ananta Toer", # 20th
		"Asep Sunandar Sunarya", # 20th
		"I Made Sidia", # 20th
	],
	iGreatScientist : [
		"Jayabaya", # 12th
		"Empu Tantular", # 14th
		iGlobal, 
		"Herman Johannes", # 20th
	],
	iGreatMerchant : [
		"Dewawarman", # 1st
		"fCri Kahulunnan", # 9th
		iRenaissance,
		"Raja Mudaliar", # 16th
		"Nahkoda Muda", # 18th
	],
	iGreatEngineer : [
		"Gunadharma", # 9th
		"Samaratungga", # 9th
		"Rakai Pikatan", # 9th
		iGlobal, 
		"Liem Bwan Tjie", # 20th
		"Soejoedi Wirjoatmodjo", # 20th
	],
	iGreatStatesman : [
		"Gajah Mada", # 14th
		"Parmeswara", # 14th
		iIndustrial,
		"Mahmud Badaruddin", # 19th
		"fRaden Ayu Kartini", # 19th
		iGlobal,
		"Sukarno", # 20th
		"Agus Salim", # 20th
		"Chep the Magnificent", # Contest Reward
	],
	iGreatGeneral : [
		"Dharmawangsa", # 10th
		"Airlangga", # 11th
		"Ken Arok", # 12th
		"Raden Wijaya", # 13th
		"fTribhuwana Vijayatunggadewi", # 14th
		iRenaissance,
		"fMalahayati", # 16th
		"fMartha Christina Tiahahu", # 18th
		"Pattimura", # 18th
		iIndustrial, 
		"fCut Nyak Dhien", # 19th
		iGlobal, 
		"Oerip Soemohardjo", # 20th
		"Sudirman", # 20th
	],
},
iCivMoors : {
	iGreatProphet : [
		"Ibn Masarra", # 10th
		"Ibn Hazm", # 11th
		"Musa bin Maymun", # 12th
		"fFatima bint al-Muthanna", # 12th
		"Ibn Arabi", # 12th
		iRenaissance, 
		"Ahmad Zarruq", # 15th
		"Ahmad ibn Abi Jum'ah", # 15th
		iIndustrial, 
		"Muhammad ibn Ali as-Senussi", # 19th
	],
	iGreatArtist : [
		"Ziryab", # 9th
		"fWallada bint al-Mustakfi", # 11th
		"fQasmuna", # 12th
		"Ibn Tufail", # 12th
		"Ibn Quzman", # 12th
		"Al-Shustari", # 13th
		iRenaissance,
		"Ahmad Ibn al-Qadi", # 16th
		"Mohammed Awzal", # 18th
		iIndustrial, 
		"Kaddour El Alamy", # 19th
		iGlobal,
		"Abdessadeq Cheqara", # 20th
	],
	iGreatScientist : [
		"Al-Zahrawi", # 10th
		"Ibn Zuhr", # 12th
		"Jabir bin Aflah", # 12th
		"Ibn Rushd", # 12th
		"Ibn Bajja", # 12th
		"Abu al-Salt", # 12th
		"Al-Qalasadi", # 15th
		iRenaissance, 
		"Abul Qasim ibn Mohammed al-Ghassani", # 16th
	],
	iGreatMerchant : [
		"Ibrahim ibn Yaqub", # 10th
		"Al-Bakri", # 11th
		"Al-Idrisi", # 12th
		"Ibn Jubayr", # 12th
		"Ibn Battuta", # 14th
		iRenaissance,
		"Hassan al-Wazzan", # 16th
	],
	iGreatEngineer : [
		"Abbas ibn Firnas", # 9th
		"Ibn Bassal", # 11th
		"Al-Zarqali", # 11th
		"Al-Muradi", # 11th
		iRenaissance,
		"Ahmed el Inglizi", # 18th
	],
	iGreatStatesman : [
		"fZaynab an-Nafzawiyyah", # 11h
		"Ibn al-Khatib", # 14th
		"Ibn Khaldun", # 14th
		iRenaissance, 
		"fLalla Aisha Mubarka", # 17th
		"Abu al-Qasim al-Zayyani", # 18th
		iGlobal,
		"Habib Bourguiba", # 20th
	],
	iGreatGeneral : [
		"Tariq ibn Ziyad", # 8th
		"Muhammad ibn Abi Aamir", # 10th
		"Yusuf ibn Tashfin", # 11th
		iRenaissance,
		"fSayyida al Hurra", # 16th
		"Mohammed ash-Sheikh", # 16th
		"Ahmad al-Mansur", # 16th
		"Ismail ibn Sharif", # 17th
		iIndustrial,
		"Abdelkader ibn Muhieddine", # 19th
		iGlobal,
		"Abd el-Krim", # 20th
		"Mohamed Meziane", # 20th
	],
},
iCivSpain : {
	iGreatProphet : [
		"Juan de Ortega", # 11th
		u"Domingo de Guzmán", # 12th
		iRenaissance,
		"Ignacio de Loyola", # 16th
		u"Juan de Sepúlveda", # 16th
		u"fTeresa de Ávila", # 16th
		u"Francisco Suárez", # 16th
		u"Bartolomé de Las Casas", # 16th
		iIndustrial,
		u"Junípero Serra", # 18th
		"fJoaquima de Vedruna", # 19th
		iGlobal, 
		u"Josemaría Escrivá", # 20th
	],
	iGreatArtist : [
		"Gonzalo de Berceo", # 13th
		"Juan Manuel", # 14th
		iRenaissance,
		"Miguel de Cervantes", # 16th
		"Garcilaso de la Vega", # 16th
		"Lope de Vega", # 17th
		u"Diego de Silva Velázquez", # 17th
		u"fJuana Inés de la Cruz", # 17th
		"Francisco de Goya", # 18th
		iIndustrial,
		u"fGertrudis Gómez de Avellaneda", # 19th
		u"Gustavo Adolfo Bécquer", # 19th
		u"fRosalía de Castro", # 19th
		u"Isaac Albéniz", # 19th
		u"Benito Pérez Galdós", # 19th
		iGlobal,
		"Pablo Picasso", # 20th
		u"Joan Miró", # 20th
		u"Luis Buñuel", # 20th
		u"Salvador Dalí", # 20th
	],
	iGreatScientist : [
		"Gerardo de Cremona", # 12th
		"Yehuda ben Moshe", # 13th
		"Ramon Llull", # 13th
		iRenaissance,
		"Miguel Serveto", # 16th
		u"Carlos de Sigüenza y Góngora", # 17th
		"Antonio de Ulloa", # 18th
		iIndustrial,
		u"José Celestino Mutis", # 18th
		u"Santiago Ramón y Cajal", # 19th
		iGlobal, 
		"Severo Ochoa", # 20th
	],
	iGreatMerchant : [
		u"Cristóbal Colón", # 15th
		"Fernando de Magallanes", # 15th
		u"Martín de Azpilcueta", # 16th
		"Hernando de Soto", # 16th
		u"José Penso de la Vega", # 17th
		iIndustrial,
		"Salvador Fidalgo", # 18th
		iGlobal,
		"Juan March Ordinas", # 20th
		"Amancio Ortega", # 20th
	],
	iGreatEngineer : [
		"Juan Bautista de Toledo", # 16th
		"Juan de Herrera", # 16th
		iIndustrial,
		u"Agustín de Betancourt", # 18th
		"Alberto de Palacio y Elissague", # 19th
		"Esteban Terradas i Illa", # 19th
		u"Antoni Gaudí", # 19th
		iGlobal,
		"Leonardo Torres y Quevedo", # 20th
		"Juan de la Cierva", # 20th
	],
	iGreatStatesman : [
		"Alfonso el Sabio", # 13th
		iRenaissance,
		u"Francisco Jiménez de Cisneros", # 15th
		"Francisco de Vitoria", # 16th
		iIndustrial,
		u"José de Gálvez", # 18th
		u"José Moniño", # 18th
		"Juan Prim", # 19th
		iGlobal, 
		u"Lluís Companys", # 20th
		u"fDolores Ibárruri", # 20th
	],
	iGreatGeneral : [
		"El Cid", # 11th
		"Alfonso el Bravo", # 11th
		"Jaume el Conqueridor", # 13th
		iRenaissance,
		"Francisco Coronado", # 16th
		u"Hernán Cortés", # 16th
		"Francisco Pizarro", # 16th
		u"Álvaro de Bazán", # 16th
		u"fMaría Pacheco", # 16th
		u"Fernando Álvarez de Toledo", # 16th
		u"Ambrosio Spínola Doria", # 17th
		u"Bernardo de Gálvez", # 18th
		iIndustrial, 
		u"fAgustina de Aragón", # 19th
		"Fernando Villaamil", # 19th
		iGlobal, 
		"Emilio Mola", # 20th
		"Vicente Rojo Lluch", # 20th
		"Mohamed ben Mizzian", # 20th
	],
	iGreatSpy : [
		u"Tomás de Torquemada", # 15th
		"Bernardino de Mendoza", # 17th
		u"fManuela Desvalls Vergós", # 18th
		"Ali Bey el Abbassi", # 18th 
		iGlobal,
		u"Juan Pujol García", # 20th
		u"Ramón Mercader", # 20th
	],
},
iCivFrance : {
	iGreatProphet : [
		u"Pierre Abélard", # 12th
		"Louis IX", # 13th
		"fJeanne d'Arc", # 15th
		iRenaissance,
		"Jean Calvin", # 16th
		"Vincent de Paul", # 17th
		"fJeanne Mance", # 17th
		"fMarguerite Bourgeoys", # 17th
		u"Jacques-Bénigne Bossuet", # 17th
		iIndustrial,
		u"fThérèse de Lisieux", # 19th
		"Auguste Comte", # 19th
		iGlobal,
		"Albert Schweitzer", # 20th
		u"Marcel Légaut", # 20th
		u"Henri Grouès", # 20th
	],
	iGreatArtist : [
		u"Pérotin", # 12th
		u"Chrétien de Troyes", # 12th
		"fChristine de Pizan", # 15th
		"Jean Fouquet", # 15th
		iRenaissance,
		u"François Rabelais", # 16th
		"Charles Le Brun", # 17th
		"Jean-Baptiste Lully", # 17th
		"Jean Racine", # 17th
		u"Molière", # 17th
		"Antoine Watteau", # 18th
		"Voltaire", # 18th
		u"fÉlisabeth Vigée Le Brun", # 18th
		iIndustrial,
		u"Honoré de Balzac", # 19th
		"Alexandre Dumas", # 19th
		"Victor Hugo", # 19th
		"fGeorge Sand", # 19th
		"Charles Baudelaire", # 19th
		"Auguste Rodin", # 19th
		"Claude Monet", # 19th
		"Claude Debussy", # 19th
		iGlobal,
		"Henri Matisse", # 19th
		"Maurice Ravel", # 20th
		"Marcel Proust", # 20th
		u"fÉdith Piaf", # 20th
		"Albert Camus", # 20th
	],
	iGreatScientist : [
		"Gerbert d'Aurillac", # 10th
		"Nicole Oresme", # 14th
		iRenaissance,
		u"René Descartes", # 17th
		"Pierre de Fermat", # 17th
		"Blaise Pascal", # 17th
		"Antoine Lavoisier", # 18th
		u"fÉmilie du Châtelet", # 18th
		iIndustrial,
		"Pierre-Simon Laplace", # 18th
		"Sadi Carnot", # 19th
		"Louis Pasteur", # 19th
		"fMarie-Sophie Germain", # 19th
		"fMarie Curie", # 19th
		iGlobal,
		"Antoine Henri Becquerel", # 20th
		"Jacques Monod", # 20th
	],
	iGreatMerchant : [
		u"Éloi de Noyon", # 7th
		u"fJeanne la Fouacière", # 13th
		iRenaissance,
		"Jacques Cartier", # 16th
		"Samuel de Champlain", # 17th
		"Antoine de Lamothe-Cadillac", # 18th
		u"fThérèse de Couagne", # 18th
		iIndustrial,
		u"Frédéric Bastiat", # 19th
		"Ferdinand de Lesseps", # 19th
		"Louis Vuitton", # 19th
		iGlobal,
		"fCoco Chanel", # 20th
		"Marcel Dessault", # 20th
		"fMarie Marvingt", # 20th
	],
	iGreatEngineer : [
		"Suger", # 12th
		"Villard de Honnecourt", # 13th
		"Pierre de Montreuil", # 13th
		iRenaissance,
		u"Sébastien Le Prestre de Vauban", # 17th
		"Jules Hardouin-Mansart", # 17th
		"Claude Perrault", # 17th
		"Charles-Augustin Coulomb", # 18th
		"Joseph-Michel Montgolfier", # 18th
		iIndustrial,
		"Joseph Marie Jacquard", # 18th
		"Louis Daguerre", # 19th
		"Norbert Rillieux", # 19th
		"Alexandre Gustave Eiffel", # 19th
		iGlobal,
		u"Louis Lumière", # 20th
		"Le Corbusier", # 20th
	],
	iGreatStatesman : [
		u"fAliénor d'Aquitaine", # 12th
		"Philippe de Beaumanoir", # 13th
		iRenaissance,
		"Jean Bodin", # 16th
		"Armand Jean du Plessis de Richelieu", # 17th
		"Jean-Baptiste Colbert", # 17th
		u"fAnne-Marie-Louise d'Orléans", # 17th
		u"Charles-Maurice de Talleyrand-Périgord", # 18th
		"Montesquieu", # 18th
		"Maximilien Robespierre", # 18th
		iIndustrial,
		"Adolphe Thiers", # 19th
		"Alexis de Tocqueville", # 19th
		"Pierre-Joseph Proudhon", # 19th
		iGlobal,
		u"Léon Blum", # 20th
		"fSimone de Beauvoir", # 20th
	],
	iGreatGeneral : [
		"Charles Martel", # 8th
		"Godefroy de Bouillon", # 11th
		"fJeanne de Flandre", # 14th
		"Charles V", # 14th
		"fJeanne d'Arc", # 15th
		iRenaissance,
		u"Louis de Bourbon-Condé", # 17th
		"Henri de la Tour d'Auvergne", # 17th
		"Louis-Joseph de Montcalm", # 18th
		u"Louis-René de Latouche-Tréville", # 18th
		iIndustrial,
		"Louis-Nicolas Davout", # 18th
		"Joachim Murat", # 18th
		"Louis-Alexandre Berthier", # 19th
		"Gilbert de Lafayette", # 19th
		"Patrice de MacMahon", # 19th
		iGlobal,
		"Ferdinand Foch", # 20th
		"Joseph Joffre", # 20th
		u"Philippe Pétain", # 20th
		"Philippe Leclerc de Hauteclocque", # 20th
	],
	iGreatSpy : [
		u"Bertrandon de la Broquière", # 15th
		iRenaissance,
		"fCharlotte de Sauve", # 16th
		"fCharlotte Corday", # 18th
		"Pierre Beaumarchais", # 18th
		u"Chevalier d'Éon", # 18th
		iIndustrial,
		"fMichelle de Bonneuil", # 19th
		"Charles Schulmeister", # 19th
		iGlobal,
		u"fJoséphine Baker", # 20th
		"Gilbert Renault", # 20th
	],
},
iCivKhmer : {
	iGreatProphet : [
		"Sanghapala", # 6th
		"Kirtipandita", # 10th
		"Suryavarman I", # 11th
		"fJayarajadevi", # 12th
		"Tamalinda", # 12th
		iGlobal,
		"Chuon Nath", # 20th
		"Maha Ghosananda", # 20th
	],
	iGreatArtist : [
		"Udayadityavarman II", # 11th
		"fIndradevi", # 12th
		"Thommaracha", # 17th
		iIndustrial,
		"Ang Duong", # 19th
		"Suttantaprija Ind", # 19th
		iGlobal,
		"Sinn Sisamouth", # 20th
		"Vann Nath", # 20th
		"Chath Piersath", # 20th
		"Chhim Sothy", # 20th
	],
	iGreatScientist : [
		"Semahatata", # 7th
		"Jayavarman V", # 10th
		"Yajnavaraha", # 10th
		"fSaptadevakula Prana", # 10th
		iGlobal,
		"Keng Vannsak", # 20th
	],
	iGreatMerchant : [
		"Jayavarman IV", # 10th
		"Srindravarman", # 14th
		"fDaun Penh", # 14th
		iRenaissance,
		"Chey Chettha", # 16th
		"Srei Meara", # 17th
		iGlobal,
		"Teng Bunma", # 20th
	],
	iGreatEngineer : [
		"Indravarman I", # 9th
		"Yasovarman I", # 9th
		"fJahavi", # 10th
		"Udayadityavarman II", # 11th
		"Jayavarman VII", # 12th 
		iGlobal,
		"Vann Molyvann", # 20th
	],
	iGreatStatesman : [
		"Jayavarman II", # 9th
		"Harshavarman", # 10th
		iIndustrial,
		"Norodom", # 19th
		iGlobal,
		"Tou Samouth", # 20th
	],
	iGreatGeneral : [
		"Bhavavarman", # 6th
		"Rajendravarman II", # 10th
		"Sangrama", # 11th
		"Vidyanandana", # 12th
		iGlobal,
		"Sak Sutsakhan", # 20th
		"Dien Del", # 20th
	],
	iGreatSpy : [
		"fYun Yat", # 20th
	]
},
iCivEngland : {
	iGreatProphet : [
		"Bede the Venerable", # 8th
		"Anselm of Canterbury", # 11th
		"Thomas Becket", # 12th
		iRenaissance,
		"Thomas More", # 16th
		"fAnne Hutchinson", # 17th
		"John Newton", # 18th
		"William Penn", # 18th
		"Jonathan Edwards", # 18th
		"fAnn Lee", # 18th
		"John Wesley", # 18th
		iIndustrial,
		"William Booth", # 19th
		"David Livingstone", # 19th
		iGlobal,
		"Gerald Gardner", # 20th
		"Aleister Crowley", # 20th
		"John Stott", # 20th
	],
	iGreatArtist : [
		"Geoffrey Chaucer", # 14th
		iRenaissance,
		"William Shakespeare", # 17th
		"John Milton", # 17th
		"John Vanbrugh", # 17th
		"George Frideric Handel", # 18th
		"fJane Austen", # 18th
		iIndustrial,
		"William Blake", # 18th
		"fMary Shelley", # 19th
		"Alfred Tennyson", # 19th
		"Charles Dickens", # 19th
		"Arthur Conan Doyle", # 19th
		iGlobal,
		"James Joyce", # 20th
		"fAgatha Christie", # 20th
		"John R. R. Tolkien", # 20th
		"John Lennon", # 20th
	],
	iGreatScientist : [
		"Roger Bacon", # 13th
		"William of Ockham", # 14th
		iRenaissance,
		"Francis Bacon", # 16th
		"Robert Boyle", # 17th
		"Isaac Newton", # 17th
		"David Hume", # 18th
		"William Herschel", # 18th
		iIndustrial,
		"John Dalton", # 19th
		"Michael Faraday", # 19th
		"fMary Anning", # 19th
		"Charles Darwin", # 19th
		"James Clerk Maxwell", # 19th
		iGlobal,
		"Ernest Rutherford", # 20th
		"Alexander Fleming", # 20th
		"Alan Turing", # 20th
		"fRosalind Franklin", # 20th
		"Stephen Hawking", # 20th
	],
	iGreatMerchant : [
		"Alan Rufus", # 11th
		"Aaron of Lincoln", # 12th
		iRenaissance,
		"Francis Drake", # 16th
		"William Petty", # 17th
		"James Cook", # 18th
		"Adam Smith", # 18th
		iIndustrial,
		"George Hudson", # 19th
		"Richard Francis Burton", # 19TH
		"Thomas Sutherland", # 19th
		"Cecil Rhodes", # 19th
		iGlobal,
		"John Maynard Keynes", # 20th
	],
	iGreatEngineer : [
		"Henry Yevele", # 14th
		iRenaissance,
		"Inigo Jones", # 17th
		"Robert Hooke", # 17th
		"Christopher Wren", # 17th
		"William Adam", # 18th
		"John Harrison", # 18th
		iIndustrial,
		"James Watt", # 18th
		"George Stephenson", # 19th
		"Isambard Kingdom Brunel", # 19th
		"Henry Bessemer", # 19th
		"Charles Babbage", # 19th
		"fAda Lovelace", # 19th
		iGlobal,
		"John Logie Baird", # 20th
		"fVictoria Drummond", # 20th
		"Frank Whittle", # 20th
		"Tim Berners-Lee", # 20th
	],
	iGreatStatesman : [
		"Thomas Becket", # 12th
		iRenaissance,
		"William Cecil", # 16th
		"John Locke", # 17th
		"Thomas Hobbes", # 17th
		"Robert Walpole", # 18th
		"William Pitt", # 18th
		"fMary Wollstonecraft", # 18th
		iIndustrial,
		"William Gladstone", # 19th
		"Benjamin Disraeli", # 19th
		"Robert Gascoyne-Cecil Salisbury", # 19th
		iGlobal,
		"Thomas Edward Lawrence", # 20th
		"fEmmeline Pankhurst", # 20th
		"Clement Atlee", # 20th
		"fDiana Spencer", # 20th
	],
	iGreatGeneral : [
		"William the Conqueror", # 11th
		"Richard the Lionheart", # 12th
		"Edward III", # 14th
		"fMargaret of Anjou", # 15th
		iRenaissance,
		"Oliver Cromwell", # 17th
		"John Churchill Marlborough", # 17th
		"Horatio Nelson", # 18th
		iIndustrial,
		"Arthur Wellesley Wellington", # 19th
		"Edmund Lyons", # 19th
		iGlobal,
		"Hugh Dowding", # 20th
		"Bernard Law Montgomery", # 20th
		"Harold Alexander", # 20th
	],
	iGreatSpy : [
		"Francis Walsingham", # 16th
		"Guy Fawkes", # 16th
		"fElizabeth Alkin", # 17th
		u"John André", # 18th
		"Edward Bancroft", # 18th
		iIndustrial,
		"William Wickham", # 19th
		"William Melville", # 19th
		"Mansfield Smith-Cumming", # 19th
		iGlobal,
		"Sidney Reilly", #, 20th
		"fVera Atkins", #, 20th
		"fLise de Baissac", # 20th
		"fMelita Norwood", # 20th
		"Ian Fleming", # 20th
		"Kim Philby", # 20th
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
		iIndustrial,
		"Theodor Herzl", # 19th
		iGlobal,
		"Dietrich Bonhoeffer", # 20th
		"fEdith Stein", # 20th
		"Joseph Ratzinger", # 20th
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
		"Johann Strauss", # 19th
		"Richard Wagner", # 19th
		"Gustav Klimt", # 19th
		iGlobal,
		"Stefan Zweig", # 20th
		"Paul Klee", # 20th
		"fLeni Riefenstahl", # 20th
		"Leoreth", # 21st
	],
	iGreatScientist : [
		"Nikolaus von Kues", # 15th
		iRenaissance,
		"Theophrastus von Hohenheim", # 16th
		"Gerhard Mercator", # 16th
		"Johannes Kepler", # 17th
		"Gottfried Leibniz", # 17th
		"Leonhard Euler", # 18th
		"fCaroline Herschel", # 18th
		iIndustrial,
		"Alexander von Humboldt", # 19th
		u"Carl Friedrich Gauß", # 19th
		"Ignaz Semmelweis", # 19th
		"Gregor Mendel", # 19th
		"Ernst Haeckel", # 19th
		"Sigmund Freud", # 19th
		iGlobal,
		"Albert Einstein", # 20th
		"Werner Heisenberg", # 20th
		"fEmmy Noether", # 20th
		"Max Planck", # 20th
		u"Erwin Schrödinger", # 20th
		"fLise Meitner", # 20th
	],
	iGreatMerchant : [
		"Jakob Fugger", # 15th
		iRenaissance,
		"fBarbara Uthmann", # 16th
		"Johann Hinrich Gossler", # 18th
		"Mayer Amschel Rothschild", # 18th
		iIndustrial,
		"Friedrich List", # 19th
		"Carl Menger", # 19th
		iGlobal,
		"Joseph Schumpeter", # 20th
		"fMelitta Bentz", # 20th
		"Ludwig von Mises", # 20th
	],
	iGreatEngineer : [
		"Heinrich Parler", # 14th
		"Peter Parler", # 14th
		iRenaissance,
		"Johann Lukas von Hildebrandt", # 18th
		iIndustrial,
		"Alfred Krupp", # 19th
		"Nikolaus Otto", # 19th
		"Gottlieb Daimler", # 19th
		"Carl Benz", # 19th
		iGlobal,
		"Ferdinand Porsche", # 20th
		"August Horch", # 20th
		"Ludwig Mies van der Rohe", # 20th
		"Friedensreich Hundertwasser", # 20th
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
		iGlobal,
		"Konrad Adenauer", # 20th
		"fHannah Arendt", # 20th
		"Helmut Kohl", # 20th
	],
	iGreatGeneral : [
		u"Otto der Große", # 10th
		iRenaissance,
		"Albrecht von Wallenstein", # 17th
		"Eugen von Savoyen", # 17th
		u"Gebhard Leberecht von Blücher", # 18th
		iIndustrial,
		"Carl von Clausewitz", # 19th
		"Paul von Hindenburg", # 19th
		iGlobal,
		"Erwin Rommel", # 20th
		"Heinz Guderian", # 20th
	],
	iGreatSpy : [
		u"Christian Andreas Käsebier", # 18th
		iIndustrial,
		"Georg Klindworth", # 19th
		"Wilhelm Stieber", # 19th
		"Alfred Redl", # 19th
		"fMaria de Victorica", # 19th
		iGlobal,
		u"fElsbeth Schragmüller", # 20th
		"Wilhelm Canaris", # 20th
		"Fritz Joubert Duquesne", # 20th
		"Klaus Fuchs", # 20th
		"Markus Wolf", # 20th
	],
},
iCivRussia : {
	iGreatProphet : [
		"fOlga", # 10th
		"Sergey Radonezhsky", # 14th
		"Paisiy Yaroslavov", # 15th
		iRenaissance,
		"Feofan Prokopovich", # 18th
		"Seraphim Sarovsky", # 18th
		iIndustrial,
		"fHelena Blavatsky", # 19th
		"Grigori Rasputin", # 19th
		"Nikolai Rerikh", # 19th
		iGlobal,
		"Nikolai Berdyaev", # 20th
		"Georges Florovsky", # 20th
		"Alexei Losev", # 20th
	],
	iGreatArtist : [
		"Feofan Grek", # 14th
		"Andrei Rublev", # 15th
		iRenaissance,
		"Alexander Sumarokov", # 18th
		"Fedot Shubin", # 18th
		"Gavrila Derzhavin", # 18th
		iIndustrial,
		"Alexander Pushkin", # 19th
		"Fyodor Dostoyevsky", # 19th
		"Leo Tolstoy", # 19th
		"Pyotr Ilyich Tchaikovsky", # 19th
		"Modest Mussorgsky", # 19th
		"Anton Chekov", # 19th
		iGlobal,
		"Wassily Kandinsky", # 20th
		"fAnna Pavlova", # 20th
		"fNatalia Goncharova", # 20th
		"Dmitri Shostakovich", # 20th
	],
	iGreatScientist : [
		"Mikhail Lomonosov", # 18th
		"Andrei Ivanovich Leksel", # 18th
		iIndustrial,
		"Nikolai Lobachevsky", # 19th
		"Mikhail Ostrogradsky", # 20th
		"Dmitri Mendeleyev", # 19th
		"fSofia Kovalevskaya", # 19th
		"Konstantin Tsiolkovsky", # 19th
		iGlobal,
		"Pavel Cherenkov", # 20th
		"Yulii Borisovich Khariton", # 20th
	],
	iGreatMerchant : [
		"Afanasiy Nikitin", # 15th
		iRenaissance,
		"Vitus Bering", # 18th
		"Grigory Shelikhov", # 18th
		"Pavel Lebedev-Lastochkin", # 18th
		iIndustrial,
		"Ivan Kruzenshtern", # 19th
		"Nikolai Chukmaldin", # 19th
		"Karl Faberzhe", # 19th
		iGlobal,
		"Nikolai Kondratiev", # 20th
	],
	iGreatEngineer : [
		"Lazar Serb", # 15th
		iRenaissance,
		"Postnik Yakovlev", # 16th
		"Vasily Bazhenov", # 18th
		"Ivan Starov", # 18th
		iIndustrial,
		"Vladimir Shukhov", # 19th
		"Sergey Prokudin-Gorsky", # 19th
		iGlobal,
		"Mikhail Kalashnikov", # 20th
		"Sergei Korolev", # 20th
		"Andrey Tupolev", # 20th
		u"Léon Theremin", # 20th
		"Vladimir Zvorykin", # 20th
		"Igor Sikorsky", # 20th
		"fValentina Tereshkova", # 20th
	],
	iGreatStatesman : [
		"Vladimir Sviatoslavich", # 11th
		"Yaroslav Mudry", # 11th
		"fMarfa Posadnitsa", # 15th
		"Ivan Vasilyevich", # 15th
		iRenaissance,
		"Vasily Tatishchev", # 18th
		"Nikita Panin", # 18th
		"fYekaterina Vorontsova-Dashkova", # 18th
		iIndustrial,
		"Mikhail Speransky", # 19th
		"Vladimir Lenin", # 19th
		iGlobal,
		"Leon Trotsky", # 20th
		"fAlexandra Kollontai", # 20th
		"Andrei Sakharov", # 20th
		"Mikhail Gorbachev", # 20th
	],
	iGreatGeneral : [
		"Alexander Nevsky", # 13th
		"Ivan Grozny", # 15th
		iRenaissance,
		"Mikhail Romanov", # 17th
		"Alexander Suvorov", # 18th
		"Grigory Potemkin", # 18th
		iIndustrial,
		"Pavel Nakhimov", # 19th
		"Mikhail Skobelev", # 19th
		"fVasilisa Kozhina", # 19th
		"fNadezhda Durova", # 19th
		iGlobal,
		"Mikhail Tukhachevsky", # 20th
		"Georgy Zhukov", # 20th
		"Vasily Chuikov", # 20th
	],
	iGreatSpy : [
		"Fyodor Romodanovsky", # 17th
		iIndustrial,
		"Aleksandr Benkendorf", # 19th
		"Pyotr Rachkovsky", # 19th
		iGlobal,
		"Ilie Catarau", # 20th
		"Felix Dzerzhinsky", # 20th
		"Ivan Serov", # 20th
		u"Sándor Goldberger", # 20th
		"Lavrentiy Beria", # 20th
		"Oleg Gordievsky", # 20th
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
		iGlobal,
		"Lobi Traore", # 20th
		"Ibrahim Aya", # 20th
	],
	iGreatScientist : [
		"Gaoussou Diawara", # 14th
		"Abu al Baraaka", # 12-16th
		iRenaissance,
		"Mohammed Bagayogo", # 16th
		"Ahmed Baba", # 16th
		iIndustrial,
		"Ag Mohammed Kawen", # 19th
	],
	iGreatMerchant : [
		"Tunka Manin", # 11th
		"Abubakari", # 13th
		"Abu Bakr ibn Ahmad Biru", # 12-16th
		iGlobal,
		u"Mandé Sidibé", # 20th
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
		iGlobal,
		"Modibo Keita", # 20th
		u"Alpha Oumar Konaré", # 20th
	],
	iGreatGeneral : [
		"fYennenga", # 12th
		"Sundiata Keita", # 13th
		"Askia Muhammad", # 15th
		"Sunni Ali", # 15th
		iRenaissance,
		"Askia Daoud", # 16th
		"fAminatu", # 16th
		"Ngolo Diarra", # 18th
		iIndustrial,
		"fSeh-Dong-Hong-Beh", # 19th
	],
},
iCivPoland : {
	iGreatProphet : [
		"Wojciech", # 10th
		"Stanislaw Szczepanowski", # 11th
		"fJadwiga", # 14th
		iRenaissance,
		"Piotr z Goniadza", # 16th
		"Piotr Skarga", # 16th
		"Israel Baal Szem Tow", # 18th
		"Eliasz ben Salomon Zalman", # 18th
		u"Jakub Józef Frank", # 18th
		iIndustrial, 
		"Albert Chmielowski", # 19th
		iGlobal,
		u"fUrsula Ledóchowska", # 20th
		"fFaustina Kowalska", # 20th
		"Stefan Wyszynski", # 20th
		"Karol Wojtyla", # 20th
	],
	iGreatArtist : [
		"Jan Kochanowski", # 16th
		"Jan Andrzej Morsztyn", # 17th
		"Ignacy Krasicki", # 18th
		iIndustrial,
		"Adam Mickiewicz", # 19th
		"Fryderyk Chopin", # 19th
		"Jan Matejko", # 19th
		"Stanislaw Wyspianski", # 19th
		u"Józef Konrad Korzeniowski", # 19th
		iGlobal,
		"fTamara de Lempicka", # 20th
		"Witold Lutoslawski", # 20th
		"Andrzej Wajda", # 20th
		"fWislawa Szymborska", # 20th
	],
	iGreatScientist : [
		"Witelo", # 13th
		iRenaissance,
		"Mikolaj Kopernik", # 16th
		u"Michal Sedziwój", # 17th
		"Jan Brozek", # 17th
		"Stanislaw Staszic", # 18th
		iIndustrial,
		"Ludwik Lejzer Zamenhof", # 19th
		"fMaria Sklodowska", # 19th
		iGlobal, 
		"Kazimierz Funk", # 20th
		"Alfred Tarski", # 20th
		u"Józef Rotblat", # 20th
	],
	iGreatMerchant : [
		"Konstanty Korniakt", # 16th
		"Antoni Protazy Potocki", # 18th
		iIndustrial,
		"Henryk Lubienski", # 19th
		"Leopold Kronenberg", # 19th
		"Franciszek Ksawery Branicki", # 19th"
		iGlobal,
		"Maksymilian Faktorowicz", # 20th
		"Jan Kulczyk", # 20th
	],
	iGreatEngineer : [
		"Kazimierz Siemienowicz", # 17th
		"Tylman Gamerski", # 17th
		"Laurynas Gucevicius", # 18th
		iIndustrial,
		"Piotr Steinkeller", # 19th
		"Ignacy Lukasiewicz", # 19th
		"Stefan Drzewiecki", # 19th
		iGlobal,
		"Kasimiersz Proszynski", # 20th
		"Tadeusz Sendzimir", # 20th
		"Stefan Tyszkiewicz", # 20th
	],
	iGreatStatesman : [
		"Wladyslaw Lokietek", # 14th
		iRenaissance,
		"Andrzej Frycz Modrzewski", # 16th
		"Jan Zamoyski", # 16th
		"fElzbieta Sieniawska", # 17th
		"Stanislaw Staszic", # 18th
		"Scipione Piattoli", # 18th
		iIndustrial, 
		"Adam Jerzy Czartoryski", # 19th
		iGlobal,
		"Ignacy Daszynski", # 20th
		"Jozef Pilsudski", # 20th
		"Wladyslaw Sikorski", # 20th
	],
	iGreatGeneral : [
		"Mieszko", # 10th
		"Wladyslaw Jagiello", # 14th
		iRenaissance,
		"Jan Tarnowski", # 16th
		"Stefan Batory", # 16th
		u"Stanislaw Zólkiewski", # 16th
		"Stefan Czarniecki", # 17th
		"Tadeusz Kosciuszko", # 18th
		iIndustrial,
		"Jan Henryk Dabrowski", # 18th
		"Ignacy Pradzynski", # 19th
		u"Józef Bem", # 19th
		"fEmilia Plater", # 19th
		iGlobal,
		"Wladyslaw Sikorski", # 20th
		"Kazimierz Sosnkowski", # 20th
		"Stanislaw Maczek", # 20th
	],
	iGreatSpy : [
		"Jerzy Franciszek Kulczycki", # 17th
		"fZofia Potocka", # 18th
		iIndustrial,
		u"fKarolina Sobanska", # 19th
		iGlobal,
		"Jan Kowalewski", # 20th
		"Jerzy Sosnowski", # 20th
		"Marian Rejewski", # 20th
		"Kazimierz Leski", # 20th
		"fKrystyna Skarbek", # 20th
		u"Ryszard Kuklinski", # 20th
	],
},
iCivPortugal : {
	iGreatProphet : [
		u"António de Lisboa", # 13th
		u"fIsabel de Aragão", # 14th
		iRenaissance,
		u"João de Deus", # 16th
		u"João de Brito", # 17th
		iIndustrial, 
		"fRita Lopes de Almeida", # 19th
		iGlobal, 
		"Agostinho da Silva", # 20th
	],
	iGreatArtist : [
		u"Fernão Lopes", # 15th
		u"Nuno Gonçalves", # 15th
		iRenaissance,
		u"Luís de Camões", # 16th
		u"António Ferreira", # 16th
		u"João de Barros", # 16th
		"Machado de Castro", # 18th
		iIndustrial, 
		"Antero de Quental", # 19th
		u"José Maria de Eça de Queirós", # 19th
		iGlobal,
		"Fernando Pessoa", # 20th
		u"fAmália Rodrigues", # 20th
		u"José Saramago", # 20th
	],
	iGreatScientist : [
		"Garcia de Orta", # 16th
		"Pedro Nunes", # 16th
		"Amato Lusitano", # 16th
		"Bartolomeu de Gusmao", # 18th
		"Jacob de Castro Sarmento", # 18th
		iGlobal,
		"Froilano de Mello", # 20th
		"Abel Salazar", # 20th
		u"António Egas Moniz", # 20th
	],
	iGreatMerchant : [
		"Vasco da Gama", # 15th
		"Francisco de Almeida", # 15th
		"Henrique o Navegador", # 15th
		"Bartolomeu Dias", # 15th
		iRenaissance,
		u"Pedro Álvares Cabral", # 15th
		u"Fernão Pires de Andrade", # 16th
		"fGracia Mendes Nasi", # 16th
		u"Fernão Mendes Pinto", # 16th
		iIndustrial, 
		"fAntonia Ferreira", # 19th
		iGlobal, 
		u"António Champalimaud", # 20th
	],
	iGreatEngineer : [
		"Mateus Fernandes", # 15th
		iRenaissance,
		"Diogo de Arruda", # 16th
		"Diogo de Boitaca", # 16th
		u"João Antunes", # 17th
		u"Bartolomeu de Gusmão", # 18th
		iIndustrial,
		"Carlos Amarante", # 18th
		iGlobal,
		u"José Marques da Silva", # 20th
		u"Álvaro Siza Vieira", # 20th
	],
	iGreatStatesman : [
		"Henrique de Avis", # 15th
		iRenaissance,
		u"Tristão da Cunha", # 16th
		u"João o Restaurador", # 17th
		u"fLuisa de Guzmán", # 17th
		u"Sebastião José de Carvalho e Melo", # 18th
		iGlobal,
		"Afonso Costa", # 20th
		u"António de Oliveria Salazar", # 20th
		u"António Guterres", # 20th
	],
	iGreatGeneral : [
		"Geraldo sem Pavor", # 12th
		u"Nuno Álvares Pereira", # 14th
		u"Álvaro Vaz de Almada", # 15th
		iRenaissance,
		"Afonso de Albuquerque", # 15th
		"Matias de Albuquerque", # 17th
		iIndustrial, 
		u"António José Severim de Noronha", # 19th
		iGlobal,
		"Otelo Saraiva de Carvalho", # 20th
	],
	iGreatSpy : [
		"Roderigo Lopez", # 16th
		iGlobal,
		u"Agostinho Lourenço", # 20th
	],
},
iCivInca : {
	iGreatProphet : [
		"Yahuar Huacac", # 14th
		"fAsarpay", # 16th
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
		u"Túpac Amaru", # 18th
		iIndustrial,
		"fJuana Azurduy de Padilla", # 19th
	],
},
iCivItaly : {
	iGreatProphet : [
		"Tommaso d'Aquino", # 13th
		"Francesco d'Assisi", # 13th
		"fGuglielma", # 13th
		"fCaterina di Giacomo di Benincasa", # 14th
		iRenaissance,
		"Giuliano della Rovere", # 15th
		"Camillo Borghese", # 16th
		"Giulio de' Medici", # 16th
		"Matteo Ricci", # 16th
		iIndustrial,
		"Giovanni Maria Mastai-Ferretti", # 19th
		"Giovanni Bosco", # 19th
	],
	iGreatArtist : [
		"Dante Alighieri", # 13th
		"Giotto di Bondone", # 14th
		"Giovanni Boccaccio", # 14th
		"Donatello", # 15th
		iRenaissance,
		"Michelangelo Buonarroti", # 16th
		"Raffaello Sanzio", # 16th
		"fSofonisba Anguissola", # 16th
		"Michelangelo Merisi da Caravaggio", # 16th
		"Claudio Monteverdi", # 17th
		"fArtemisia Gentileschi", # 17th
		"Antonio Vivaldi", # 18th
		iIndustrial,
		"Alessandro Manzoni", # 19th
		"Giuseppe Verdi", # 19th
		"Giacomo Puccini", # 19th
		iGlobal,
		"Umberto Boccioni", # 20th
		"fGrazia Deledda", # 20th
		"Federico Fellini", # 20th
		u"Gian Maria Volontè", # Contest Reward
	],
	iGreatScientist : [
		"fTrotula di Salerno", # 12th
		"Francesco Petrarca", # 14th
		iRenaissance,
		"Pico della Mirandola", # 15th
		"Giordano Bruno", # 16th
		"Galileo Galilei", # 16th
		"fElena Cornaro Piscopia", # 17th
		"Luigi Galvani", # 18th
		"Alessandro Volta", # 18th
		"fMaria Gaetana Agnesi", # 18th
		iIndustrial,
		"Amedeo Avogadro", # 19th
		"Camillo Golgi", # 19th
		iGlobal,
		"fMaria Montessori", # 20th
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
		"Giovanni Caboto", # 15th
		"Amerigo Vespucci", # 15th
		"fTullia d'Aragona", # 16th
		iGlobal,
		"Enzo Ferrari", # 20th
		"Gianni Versace", # 20th
	],
	iGreatEngineer : [
		"Taccola", # 15th
		"Filippo Brunelleschi", # 15th
		iRenaissance,
		"Leon Battista Alberti", # 15th
		"Leonardo da Vinci", # 15th
		"Donato Bramante", # 15th
		"Andrea Palladio", # 16th
		iIndustrial, 
		"Alois Negrelli", # 19th
		"Antonio Meucci", # 19th
		iGlobal,
		"Guglielmo Marconi", # 20th
		"Giovanni Battista Caproni", # 20th
		"Angiolo Mazzoni", # 20th
		"Gabriele Trovato", # 20th
	],
	iGreatStatesman : [
		"Giovanni Villani", # 13th
		iRenaissance,
		"fLucrezia Borgia", # 15th
		u"Niccolò Machiavelli", # 15th
		"fIsabella d'Este", # 16th
		"Francesco Guicciardini", # 16th
		"Giambattista Vico", # 18th
		"Cesare Beccaria", # 18th
		"Pasquale Paoli", # 18th
		iIndustrial,
		"Giuseppe Garibaldi", # 19th
		"Giuseppe Mazzini", # 19th
		"Francesco Crispi", # 19th
		iGlobal,
		"Antonio Gramsci", # 20th
	],
	iGreatGeneral : [
		"fMatilde di Canossa", # 11th
		"Enrico Dandolo", # 13th
		"Simone Boccanegra", # 14th
		"Francesco Sforza", # 15th
		iRenaissance, 
		"Cesare Borgia", # 15th
		"Andrea Doria", # 16th
		"Sebastiano Venier", # 16th
		iIndustrial,
		"Alessandro Ferrero La Marmora", # 19th
		"Giuseppe Garibaldi", # 19th
		iGlobal,
		"Rodolfo Graziani", # 20th
		"Giovanni Messe", # 20th
	],
	iGreatSpy : [
		"Andrea Gritti", # 15th
		"Gaspar Graziani", # 17th
		"Giacomo Casanova", # 18th
		iGlobal,
		"fLuisa Zeni", # 20th
		"Maurizio Giglio", # 20th
		"Rodolfo Siviero", # 20th
	],
},
iCivMongols : {
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
		iGlobal,
		"Siqin Gaowa", # 20th
	],
	iGreatScientist : [
		"Isa Khelmerchi", # 13th
		"Kaidu", # 13th
		"Nasir al-Din al-Tusi", # 13th (also Persian)
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
		"Qawsun", # 14th
		iRenaissance,
		"Altan", # 16th
	],
	iGreatEngineer : [
		"Duwa", # 13th
		"Zhang Wenqian", # 13th
		"Toqta", # 14th
		"Ismail", # 14th
		iGlobal,
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
		"fKhutulun", # 13th
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
		"Cuacuauhtzin", # 15th
		"Nezahualcoyotl", # 15th
		"Xayacamach", # 15th
		"fMacuilxochitzin", # 15th
	],
	iGreatScientist : [
		"Axayacatl", # 15th
		"Ixtlilxochitl", # 16th
		"Coanacochtzin", # 16th
	],
	iGreatMerchant : [
		"Cuauhtemoc", # 16th
		"Tlacotzin", # 16th
		"fTecuichpoch Ixcaxochitzin", # 16th
	],
	iGreatEngineer : [
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
		"Guru Ram Das", # 16th
		"Guru Arjan", # 16th
		"Hiravijaya ji", # 16th
		"Shah Abdul Latif Bhittai", # 18th
		"Bulleh Shah", # 18th
		iIndustrial,
		"Mirza Ghulam Ahmad", # 19th
	],
	iGreatArtist : [
		"Basawan", # 16th
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
		"Virji Vora", # 17th
		"Mir Jumla", # 17th
		"Yahya Saleh", # 16th
		"Khan Alam", # 18th
		iGlobal,
		"Mian Muhammad Mansha", # 20th
	],
	iGreatEngineer : [
		"Fathullah Shirazi", # 16th
		"Ustad Ahmad Lahauri", # 17th
		"Muhammad Saleh Thattvi", # 17th
		iGlobal,
		"Abdur Rahman Hye", # 20th
		"Abdul Qadeer Khan", # 20th
		"Munir Ahmad Khan", # 20th
		"fYasmeen Lari", # 20th
	],
	iGreatStatesman : [
		"fRazia Sultana", # 13th
		"Ziauddin Barani", # 14th
		iRenaissance,
		"Raja Birbal", # 16th
		"fMaham Anga", # 16th
		"Babur", # 16th
		"Abu'l-Fazl ibn Muhammad", # 16th
		iGlobal,
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
	iGreatSpy : [
		"Hamid Gul", # 20th
	],
},
iCivOttomans : {
	iGreatProphet : [
		"Sheikh Bedreddin", # 14th
		"Akshamsaddin", # 15th
		iRenaissance,
		"Sabatai Zevi", # 17th
		"Yaakov Culi", # 18th
		iGlobal,
		u"Fethullah Gülen", # 20th
		u"Mustafa Çagrici", # 20th
	],
	iGreatArtist : [
		"Yunus Emre", # 13th
		iRenaissance,
		u"Hayâlî", # 16th
		u"Fuzûlî", # 16th
		u"Gül Baba", # 16th
		u"Ahmet Nedîm Efendi", # 18th
		"Abdullah Buhari", # 18th
		iIndustrial,
		"Osman Hamdi Bey", # 19th
		"fFatma Aliye Topuz", # 19th
		iGlobal,
		"fHalide Edib Adivar", # 20th
		"Mehmet Akif Ersoy", # 20th
	],
	iGreatScientist : [
		"Qazi Zada", # 14th
		"Serafeddin Sabuncuoglu", # 15th
		u"Ali Kusçu", # 15th
		iRenaissance,
		u"Matrakçi Nasuh", # 16th
		u"Takiyüddin", # 16th
		u"Ibrahim Müteferrika", # 18th
		iGlobal,
		"Cahit Arf", # 20th
		"Oktay Sinanoglu", # 20th
		u"Feza Gürsey", # 20th
		"Aziz Sancar", # 21th
	],
	iGreatMerchant : [
		"Piri Reis", # 16th
		"Seydi Ali Reis", # 16th
		u"Evliya Çelebi", # 17th
		iIndustrial,
		u"Abdülmecid", # 19th
		iGlobal,
		"Hormuzd Rassam", # 20th
		"Nejat Eczacibashi", # 20th
		"Aydin Dogan", # 20th
	],
	iGreatEngineer : [
		"Orban", # 15th
		"Atik Sinan", # 15th
		iRenaissance,
		"Mimar Sinan", # 16th
		"Davud Aga", # 16th
		u"Takiyüddin", # 16th
		iIndustrial,
		"Ishak Efendi", # 19th
		iGlobal,
		"Mimar Kemaleddin", # 20th
		u"Ekmel Özbay", # 20th
	],
	iGreatStatesman : [
		"Sheikh Edebali", # 13th
		iRenaissance,
		"Pargali Ibrahim Pasha", # 16th
		"fHurrem Sultan", # 16th
		"Sokollu Mehmet Pasha", # 16th
		u"fKösem Sultan", # 17th
		iGlobal,
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
		iGlobal,
		"fKara Fatma", # 20th
		"Ismail Enver", # 20th
	],
	iGreatSpy : [
		u"Süleyman Askerî", # 20th
		"fDespina Storch", # 20th
	],
},
iCivThailand : {
	iGreatProphet : [
		"Lithai", # 14th (Mahathammaracha I)
		"Luang Pu Thuat", # 17th
		"Upali Thera", # 18th
		iIndustrial,
		"Somdej Toh", # 19th
		"Paramanuchitchinorot", # 19th
		"Vajirananavarorasa", # 19th
		iGlobal,
		"Luang Pu Sodh Candasaro", # 20th
		"Phra Dharmakosacarya", # 20th
		"fChandra Khonnokyoong", # 20th
		"Ajahn Chah", # 20th
	],
	iGreatArtist : [
		"Si Prat", # 17th
		"Thammathibet", # 18th
		iIndustrial,
		"Khrua In Khong", # 19th
		"Phra Phutthaloetla Naphalai", # 19th (Rama II)
		"Sunthorn Phu", # 19th
		iGlobal,
		"Pin Malakul", # 20th
	],
	iGreatScientist : [
		"Ramkhamhaeng", # 13th
		iIndustrial,
		"Dan Beach Bradley", # 19th
		"Damrong Rajanubhab", # 19th
		iGlobal,
		"Mahidol Adulyadej", # 20th
		"Phraya Anuman Rajadhon", # 20th
		"fKrisana Kraisintu", # 20th
		"Shaiwatna Kupratakul", # 20th
	],
	iGreatMerchant : [
		"Uthong", # 14th
		"Yamada Nagamasa", # 17th
		iIndustrial,
		"Low Kiok Chiang", # 19th
		iGlobal,
		"Puey Ungphakorn", # 20th
		"fLursakdi Sampatisiri", # 20th
	],
	iGreatEngineer : [
		"Chettathirat", # 16th
		"Tok Kayan", # 17th
		iGlobal,
		"Ravi Ravendro", # 20th (a.k.a. Karl Döhring)
		"Ercole Manfredi", # 20th
		"Purachatra Jayakara", # 20th
		"Punya Thitimajshima", # 20th
	],
	iGreatStatesman : [
		"Borommatrailokkanat", # 15h
		"Narai", # 17th
		"Kosa Pan", # 17th
		"Chaophraya Wichayen", # 17th
		iIndustrial,
		"Prayurawongse", # 19th
		"Sri Suriwongse", # 19th
		"Chulalongkorn", # 19th
		iGlobal,
		"Pridi Banomyong", # 20th
	],
	iGreatGeneral : [
		"Ramesuan", # 16th
		"Chaiyachetthathirat", # 16th
		"Taksin", # 18th
		"Phraya Phichai", # 18th
		iIndustrial,
		"Thongduang", # 19th
		"Bodindecha", # 19th
		iGlobal,
		"Phraya Phahonphonphayuhasena", # 20th
		"Plaek Phibunsongkhram", # 20th
	],
	iGreatSpy : [
		"fThao Suranari", # 19th
	]
},
iCivCongo : {
	iGreatProphet : [
		"Nzinga a Nkuwu", # 15th
		"Kinu a Mvemba", # 16th
		"Ilunga Mbili", # 16th
		iRenaissance,
		"Nkanga a Lukeni a Nzenze a Ntumba", # 17th
		"fKimpa Vita", # 17th
	],
	iGreatMerchant : [
		"N'Gangue M'voumbe Niambi", # 17th
	],
	iGreatStatesman : [
		"Mwata Yamvo", # 16th
		"Ng'anga Bilonda", # 16th
		"Kalala Ilunga", # 17th
		"fNzinga", # 17th
		iGlobal,
		"Patrice Lumumba", # 20th
		"Joseph Kasa-Vubu", # 20th
	],
	iGreatGeneral : [
		"Lukeni lua Nimi", # 14th
		iRenaissance,
		"fNzinga", # 17th
		"Nusamu a Mvemba", # 18th
		"fKangala Kingwanda", # 18th
		iIndustrial,
		"Mwenda Msiri Ngelengwa Shitambi", # 19th
	],
},
iCivNetherlands : {
	iGreatProphet : [
		"Geert Grote", # 14th
		iRenaissance,
		"Desiderius Erasmus", # 16th
		"Menno Simons", # 16th
		"Jakob Hermanszoon", # 16th
		"Baruch Spinoza", # 17th
		iIndustrial,
		"Abraham Kuyper", # 19th
		iGlobal,
		"fAlida Bosshardt", # 20th
	],
	iGreatArtist : [
		"Hendrick de Keyser", # 16th
		"Rembrandt van Rijn", # 17th
		"Johannes Vermeer", # 17th
		"Pieter Corneliszoon Hooft", # 17th
		"fTitia Bergsma", # 18th
		iIndustrial,
		"Multatuli", # 19th
		"Vincent van Gogh", # 19th
		iGlobal,
		"Piet Mondrian", # 20th
		"Maurits Cornelis Escher", # 20th
		"fAnna Maria Geertruida Schmidt", # 20th
	],
	iGreatScientist : [
		"Willebrord Snel van Royen", # 16th
		"Christiaan Huygens", # 17th
		"Antonie van Leeuwenhoek", # 17th
		"Govert Bidloo", # 17th
		"fAnna Maria van Schurman", # 18th
		iIndustrial, 
		"Johannes Diderik van der Waals", # 19th
		"Hendrik Antoon Lorentz", # 19th
		iGlobal,
		"Jan Hendrik Oort", # 20th
		"Gerrit Pieter Kuiper", # 20th
		"Edsger Wybe Dijkstra", # 20th
		"Willem Johan Kolff", # 20th
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
		iGlobal,
		"Freddy Heineken", # 20th
	],
	iGreatEngineer : [
		"Simon Stevin", # 16th
		"Cornelis Corneliszoon", # 16th
		"Cornelis Drebbel", # 17th
		"Jan Leeghwater", # 17th
		"Menno van Coehoorn", # 17th
		iIndustrial,
		"Adolphe Sax", # 19th
		"Cornelis Lely", # 19th
		"Hendrik Petrus Berlage", # 19th
		iGlobal,
		"Anton Philips", # 20th
		"Gerrit Rietveld", # 20th
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
		"fAletta Jacobs", # 19th
		iGlobal,
		"Willem Drees", # 20th
	],
	iGreatGeneral : [
		"Maurits van Nassau", # 16th
		"Piet Pieterszoon Hein", # 16th
		"Michiel de Ruyter", # 17th
		"Frederik Hendrik", # 17th
		"Cornelis Tromp", # 17th
		iIndustrial,
		"Joannes Benedictus van Heutsz", # 19th
		"Henri Winkelman", # 20th
	],
	iGreatSpy : [
		"fJohanna Brandt", # 19th
		"Christiaan Snouck Hurgronje", # 19th
		iGlobal,
		"fMata Hari", # 20th
		"Dirk Klop", # 20th
		u"François van 't Sant", # 20th
	],
},
iCivAmerica : {
	iGreatProphet : [
		"Joseph Smith", # 19th
		"fMary Baker Eddy", # 19th
		"fEllen G. White", # 19th
		"Charles Taze Russell", # 19th
		iGlobal,
		"Menachem Mendel Schneerson", # 20th
		"L. Ron Hubbard", # 20th
		"Billy Graham", # 20th
		"Malcolm Little", # 20th
	],
	iGreatArtist : [
		"Edgar Allan Poe", # 19th
		"Mark Twain", # 19th
		"fEmily Dickinson", # 19th
		"Herman Melville", # 19th
		"fMary Cassatt", # 19th
		iGlobal,
		"Howard Phillips Lovecraft", # 20th
		"Ernest Hemingway", # 20th
		"Charlie Chaplin", # 20th
		"Elvis Presley", # 20th
		"fHarper Lee", # 20th
		"Andy Warhol", # 20th
		"Miles Davis", # 20th
		"Jimi Hendrix", # 20th
	],
	iGreatScientist : [
		"Benjamin Franklin", # 18th
		"fNettie Stevens", # 19th
		iGlobal,
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
		iGlobal,
		"fHelena Rubinstein", # 20th
		"William Edward Boeing", # 20th
		"Bill Gates", # 20th
	],
	iGreatEngineer : [
		"Thomas Edison", # 19th
		"Nikola Tesla", # 19th
		"Henry Ford", # 19th
		"Charles Goodyear", # 19th
		iGlobal,
		"Orville Wright", # 20th
		"Frank Lloyd Wright", # 20th
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
		"fSojourner Truth", # 19th
		"Frederick Douglass", # 19th
		"fVictoria Claflin Woodhull", # 19th
		"fSusan B. Anthony", # 19th
		"fJane Addams", # 19th
		iGlobal,
		"fEleanor Roosevelt", # 20th
		"George Kennan", # 20th
		"Martin Luther King", # 20th
		"Henry Kissinger", # 20th
	],
	iGreatGeneral : [
		"Andrew Jackson", # 19th
		"Ulysses S. Grant", # 19th
		"Robert E. Lee", # 19th
		iGlobal,
		"Dwight D. Eisenhower", # 20th
		"George Patton", # 20th
		"Douglas MacArthur", # 20th
	],
	iGreatSpy : [
		"Benjamin Tallmadge", # 18th
		"Allan Pinkerton", # 19th
		"fBelle Boyd", # 19th
		"fElizabeth Van Lew", # 19th
		iGlobal,
		"William J. Donovan", # 20th
		"J. Edgar Hoover", # 20th
		"James Jesus Angleton", # 20th
		"fVirginia Hall", # 20th
		"fElizabeth Friedman", # 20th
	],
},
iCivMexico : {
	iGreatProphet : [
		"Juan Diego", # 16th
		"Francisco Javier Clavijero", # 18th
		u"Cristóbal Magallanes Jara", # 19th
		iGlobal,
		u"Rafael Guízar Valencia", # 20th
		"Miguel Pro", # 20th
		"Samuel Ruiz", # 20th
		u"Javier Lozano Barragán", # 20th
	],
	iGreatArtist : [
		u"fÁngela Peralta", # 19th
		iGlobal,
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
		iGlobal,
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
		iGlobal,
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
	iGreatSpy : [
		"fMargarita Ortega", # 19th
	],
},
iCivArgentina : {
	iGreatProphet : [
		"Gauchito Gil", # 19th
		iGlobal,
		"Enrique Angelelli", # 20th
		"Carlos Mugica", # 20th
		"Jorge Mario Bergoglio", # 20th
	],
	iGreatArtist : [
		u"José Hernández", # 19th
		"fLola Mora", # 19th
		iGlobal,
		"Carlos Gardel", # 20th
		"fGabriela Mistral", # 20th
		"Jorge Luis Borges", # 20th
		"Antonio Berni", # 20th
		"Daniel Barenboim", # 20th
		u"Juan José Campanella", # 20th
		"Gustavo Cerati", # 20th
	],
	iGreatScientist : [
		"Francisco Moreno", # 19th
		"Florentino Ameghino", # 19th
		iGlobal,
		"Luis Federico Leloir", # 20th
		u"László Bíró", # 20th
		u"René Favaloro", # 20th
	],
	iGreatMerchant : [
		"Juan Las Heras", # 19th
		"Otto Bemberg", # 19th
		"Ernesto Tornquist", # 19th
		iGlobal,
		u"José Ber Gelbard", # 20th
		"Roberto Alemann", # 20th
		"Jorge Wehbe", # 20th
		"Aldo Ferrer", # 20th
		"Antonio Cafiero", # 20th
	],
	iGreatEngineer : [
		"Luis Huergo", # 19th
		"Jorge Newbery", # 19th
		iGlobal,
		"Amancio Williams", # 20th
		"Livio Dante Porta", # 20th
		"Clorindo Testa", # 20th
		u"César Pelli", # 20th
	],
	iGreatStatesman : [
		"Juan Manuel de Rosas", # 19th
		"Domingo Faustino Sarmiento", # 19th
		"Estanislao Zeballos", # 19th
		iGlobal,
		"Carlos Saavedra Lamas", # 20th
		"Juan Atilio Bramuglia", # 20th
		u"fEva Perón", # 20th
		"Ernesto Guevara", # 20th
		u"fIsabel Martínez de Perón", # 20th
		"fEstela Barnes de Carlotto", # 20th
	],
	iGreatGeneral : [
		"Cornelio Saavedra", # 18th
		"Manuel Belgrano", # 18th
		u"Juan José Castelli", # 18th
		u"Martín Miguel de Güemes", # 18th
		u"José Gervasio Artigas", # 19th
		iGlobal, 
		u"Juan Carlos Onganía", # 20th
		"Jorge Rafael Videla", # 20th
		"Leopoldo Galtieri", # 20th
		"Jorge Anaya", # 20th
	],
	iGreatSpy : [
		"Emilio Eduardo Massera", # 20th
		"Guillermo Gaede", # 20th
	],
},
iCivColombia : {
	iGreatProphet : [
		"fLaura Montoya", # 20th
		u"Félix Restrepo Mejía", # 20th
		"Camilo Torres Restrepo", # 20th
		u"Alfonso López Trujillo", # 20th
		u"Julio Enrique Dávila", # 20th
		u"fMaría Luisa Piraquive", # 20th
		u"César Castellanos", # 20th
	],
	iGreatArtist : [
		"Jorge Isaacs", # 19th
		u"Andrés de Santa Maria", # 19th
		iGlobal,
		"Rodrigo Arenas", # 20th
		u"Álvaro Mutis", # 20th
		u"Gabriel García Márquez", # 20th
		"Fernando Botero", # 20th
		"Rafael Orozco", # 20th
		u"Rodrigo García", # 20th
		"fShakira", # 20th
	],
	iGreatScientist : [
		u"José Jéronimo Triana", # 19th
		"Julio Garavito Armero", # 19th
		iGlobal,
		u"Rodolfo Llinás", # 20th
		"Jorge Reynolds Pombo", # 20th
	],
	iGreatMerchant : [
		"James Martin Eder", # 19th
		iGlobal,
		"Julio Mario Santo Domingo", # 20th
		u"Carlos Ardila Lülle", # 20th
		"Luis Carlos Sarmiento Angulo", # 20th
	],
	iGreatEngineer : [
		u"Carlos Albán", # 19th
		iGlobal, 
		u"Carlos Raúl Villanueva", # 20th
		"Rogelio Salmona", # 20th
	],
	iGreatStatesman : [
		u"Tomás Cipriano de Mosquera", # 19th
		u"Rafael Núñez", # 19th
		iGlobal,
		u"Jorge Eliécer Gaitán", # 20th
		u"Nicolás Gómez Dávila", # 20th
		u"Mario Lanserna Pinzón", # 20th
	],
	iGreatGeneral : [
		"fAntonia Santos", # 19th
		u"Antonio Nariño", # 19th
		"Francisco de Paula Santander", # 19th
	],
	iGreatSpy :  [
		u"fManuela Sáenz", # 19th
	]
},
iCivBrazil : {
	iGreatProphet : [
		u"António Conselheiro", # 19th
		iGlobal,
		u"Hélder Câmara", # 20th
		u"fIrmã Dulce Pontes", # 20th
		"Chico Xavier", # 20th
		"Edir Macedo", # 20th
	],
	iGreatArtist : [
		"Aleijadinho", # 18th
		u"António Carlos Gomes", # 19th
		"Machado de Assis", # 19th
		iGlobal,
		"fTarsila do Amaral", # 20th
		"fCarmen Miranda", # 20th
		"Tom Jobim", # 20th
		"Romero Britto", # 20th
	],
	iGreatScientist : [
		"Oswaldo Cruz", # 19th
		"Carlos Chagas", # 19th
		iGlobal,
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
		iGlobal,
		u"Cândido Rondon", # 20th
		"Oscar Niemeyer", # 20th
		"Norberto Odebrecht", # 20th
	],
	iGreatStatesman : [
		u"José Bonifácio de Andrada", # 18th
		iIndustrial,
		"Rodrigo Augusto da Silva", # 19th
		u"José Paranhos", # 19th
		u"fIsabel Bragança", # 19th
		"Miguel Reale", # 19th
		iGlobal,
		"Roberto Mangabeira Unger", # 20th
	],
	iGreatGeneral : [
		u"Luís Alves de Lima e Silva", # 19th
		"Joaquim Marques Lisboa", # 19th
		u"fMaria Quitéria", # 19th
		iGlobal,
		u"João Baptista Mascarenhas de Morais", # 20th
		"Eurico Gaspar Dutra", # 20th
		"Artur da Costa e Silva", # 20th
	],
},
iCivCanada : {
	iGreatProphet : [
		"Ignace Bourget", # 19th
		u"André Bessette", # 20th
		iGlobal,
		"Lionel Groulx", # 20th
		"George C. Pidgeon", # 20th
		u"fRúhíyyih Khánum", # 20th
		"Marshall McLuhan", # 20th
	],
	iGreatArtist : [
		"Cornelius Krieghoff", # 19th
		u"Calixa Lavallée", # 19th
		"Tom Thomson", # 19th
		u"Émile Nelligan", # 19th
		iGlobal,
		"Lawren Harris", # 20th
		"fEmily Carr", # 20th
		"Jean-Paul Riopelle", # 20th
		"Neil Young", # 20th
		"fGabrielle Roy", # 20th
		"fAlice Munro", # 20th
	],
	iGreatScientist : [
		"John William Dawson", # 19th
		"fMaude Abbott", # 19th
		iGlobal,
		"Frederick Banting", # 20th
		"Norman Bethune", # 20th
		"Wilder Penfield", # 20th
		"Pierre Dansereau", # 20th
		"fShirley Tilghman", # 20th
		"David Suzuki", # 20th
	],
	iGreatMerchant : [
		"William McMaster", # 19th
		"Timothy Eaton", # 19th
		"Alphonse Desjardins", # 19th
		iGlobal,
		"fElizabeth Arden", # 20th
		"Max Aitken", # 20th
		"Ted Rogers", # 20th
		u"Guy Laliberté", # 20th
	],
	iGreatEngineer : [
		"Sandford Fleming", # 19th
		"William Cornelius Van Horne", # 19th
		"Alexander Graham Bell", # 19th
		"Reginald Fessenden", # 19th
		iGlobal,
		"Ernest Cormier", # 20th
		"Joseph-Armand Bombardier", # 20th
		"fElsie MacGill", # 20th
	],
	iGreatStatesman : [
		u"George-Étienne Cartier", # 19th
		"Louis Riel", # 19th
		"Henri Bourassa", # 19th
		iGlobal,
		"Lester B. Pearson", # 20th
		"fEmily Murphy", # 20th
		"fNellie McClung", # 20th
		"Tommy Douglas", # 20th
		u"René Lévesque", # 20th
		"fLouise Arbour", # 20th
	],
	iGreatGeneral : [
		"Arthur Currie", # 20th
		"Andrew McNaughton", # 20th
		"Billy Bishop", # 20th
		u"Roméo Dallaire", # 20th
	],
	iGreatSpy : [
		"William Stephenson", # 20th
		"Guy D'Artois", # 20th
		"Igor Gouzenko", # 20th
	],
},
}

setup()
