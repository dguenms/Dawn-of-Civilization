# coding: utf-8

from RFCUtils import *
from Events import handler
from Core import *

import BugCore

AlertOpt = BugCore.game.MoreCiv4lerts


lTypes = [iGreatProphet, iGreatArtist, iGreatScientist, iGreatMerchant, iGreatEngineer, iGreatStatesman, iGreatGeneral, iGreatSpy]

tGreatPeople = None
tOffsets = None


@handler("greatPersonBorn")
def onGreatPersonBorn(unit, iPlayer, city):
	assignGreatPersonName(unit, iPlayer, city)

def assignGreatPersonName(unit, iPlayer, city, bAnnounceBirth = True):
	sName = getName(unit)
	if sName:
		game.addGreatPersonBornName(sName)
		
		# Leoreth: replace graphics for female GP names
		if sName[0] == "f":
			sName = sName[1:]
			unit = replace(unit, dFemaleGreatPeople[base_unit(unit)])
		
		unit.setName(sName)
		
	# Leoreth: display notification
	if bAnnounceBirth:
		if not player(iPlayer).isMinorCiv() and not player(iPlayer).isBarbarian():
			text_key = 'TXT_KEY_MISC_GP_BORN'
			if city.isNone():
				text_key = 'TXT_KEY_MISC_GP_BORN_OUTSIDE'
				city = closestCity(unit)
		
			for iLoopPlayer in players.major().existing():
				if AlertOpt.isGreatPeopleOurs() and iPlayer != iLoopPlayer:
					continue
			
				if AlertOpt.isGreatPeopleKnown() and iPlayer != iLoopPlayer and not player(iLoopPlayer).canContact(iPlayer):
					continue
				
				if AlertOpt.isGreatPeopleNearby() and not game.isNeighbors(iPlayer, iLoopPlayer):
					continue
			
				if unit.plot().isRevealed(player(iLoopPlayer).getTeam(), False):
					message(iLoopPlayer, text_key, unit.getName(), '%s (%s)' % (city.getName(), name(city)), event=InterfaceMessageTypes.MESSAGE_TYPE_MAJOR_EVENT, button=unit.getButton(), color=infos.type('COLOR_UNIT_TEXT'), location=unit)
				else:
					message(iLoopPlayer, 'TXT_KEY_MISC_GP_BORN_SOMEWHERE', unit.getName(), event=InterfaceMessageTypes.MESSAGE_TYPE_MAJOR_EVENT, color=infos.type('COLOR_UNIT_TEXT'))

def create(iPlayer, iUnit, tile):
	x, y = location(tile)
	player(iPlayer).createGreatPeople(unique_unit(iPlayer, iUnit), True, True, x, y)

def getAlias(iCiv, iType, iEra):
	if iCiv in [iHarappa, iDravidia]: return iIndia
	elif iCiv == iEgypt and player(iCiv).getStateReligion() == iIslam: return iArabia
	elif iCiv == iIran: return iPersia
	
	return iCiv
	
def getType(iUnit):
	iUnitType = base_unit(iUnit)
	if iUnitType in lTypes: return lTypes.index(iUnitType)
	return -1

def getAvailableNames(iPlayer, iType):
	pPlayer = player(iPlayer)
	iEra = pPlayer.getCurrentEra()
	iCiv = getAlias(civ(iPlayer), iType, iEra)
	
	return getEraNames(iCiv, iType, iEra)

def getEraNames(iCiv, iType, iEra):
	lNames = tGreatPeople[iCiv][iType]
	
	iOffset = tOffsets[iCiv][iType][iEra]
	iNextOffset = len(lNames)
	if iEra + 1 < iNumEras: iNextOffset = tOffsets[iCiv][iType][iEra+1]
	
	iSpread = max(iNextOffset - iOffset, min(iEra+2, 5))
	
	lBefore = [sName for sName in lNames[:iOffset] if not game.isGreatPersonBorn(sName)]
	lAfter = [sName for sName in lNames[iOffset:] if not game.isGreatPersonBorn(sName)]
	
	if len(lAfter) >= iSpread:
		return lAfter[:iSpread]
	
	iSpread -= len(lAfter)
	return lBefore[-iSpread:] + lAfter
	
def getName(unit):
	iType = getType(unit.getUnitType())
	if iType < 0: return None
	
	lAvailableNames = getAvailableNames(unit.getOwner(), iType)
	
	return random_entry(lAvailableNames)

		
dGreatPeople = {
	iEgypt : {
		iGreatProphet : (
			"Meryre", # 14th BC
			"Akhenaten", # 14th BC
			"fNefertiti", # 13th BC
			"Khaemwaset", # 12th BC
			"Ramessesnakht", # 12th BC
			iClassical,
			"fNitiqret", # 7th BC
			"Petosiris", # 4th BC
		),
		iGreatArtist : (
			"Pehen-Ptah", # 27th BC
			"Sedjemnetjeru", # 17th BC
			"Thutmose", # 14th BC
			"Bek", # 14th BC
			"Ipuki", # 14th BC
			"Sennedjem", # 13th BC
			"Amenemope", # 12th BC
			iClassical,
			"fHelena", # 4th BC
		),
		iGreatScientist : (
			"fMerit-Ptah", # 27th BC
			"Hesy-Ra", # 27th BC
			"fPeseshet", # 26th BC
			"Ahmose", # 17th BC
			iClassical,
			"Harkhebi", # 3rd BC
			"Manetho", # 3rd BC
			"Eratosthenes", # 3rd BC
			"Ptolemaios", # 2nd
			"Diophantos", # 3rd
			"fHypatia", # 4th
		),
		iGreatMerchant : (
			"Harkhuf", # 23rd BC
			"Yuya", # 14th BC
			"Maya", # 13th BC
			"fTiye", # 13th BC
			iClassical,
			"Piye", # 8th BC
			"Alara", # 8th BC
			"Eudoxos", # 2nd BC
		),
		iGreatEngineer : (
			"Imhotep", # 27th BC
			"Sneferu", # 27th BC
			"Hemiunu", # 26th BC
			"Senenmut", # 17th BC
			"Ineni", # 15th BC
			"Amenhotep", # 14th BC
			iClassical,
			"Heron", # 1st AD
		),
		iGreatStatesman : (
			"Kagemni", # 26th BC
			"Ptahhotep", # 25th BC
			"Amenemhat", # 20th BC
			"fHatshepsut", # 15th BC
			"Herihor", # 11th BC
			iClassical,
			"fBerenice Euergetis", # 3rd BC
		),
		iGreatGeneral : (
			"Narmer", # 32nd BC
			"Menes", # 30th BC
			"Khufu", # 26th BC
			"Mentuhotep", # 21st BC
			"fAhhotep", # 16th BC
			"Thutmosis", # 15th BC
			"Sethi", # 13th BC
			iClassical,
			"Ptolemaios Euergetes", # 3rd BC
		),
	},
	iBabylonia : {
		iGreatProphet : (
			"Utnapishtim", # legendary
			"Gilgamesh", # legendary
			"fAmat-Mamu", # 18th BC
			iClassical,
			"fAdad-guppi", # 6th BC
			"Nabonidus", # 6th BC
			"Daniyyel", # 6th BC
			"Ezra", # 5th BC
		),
		iGreatArtist : (
			"fEnheduanna", # 23rd BC
			"Gudea", # 22nd BC
			"Samsu-ditana", # 17th BC
			"Sin-leqi-unninni", # 13th BC
			"Saggil-kinam-ubbib", # 11th BC
		),
		iGreatScientist : (
			"fTapputi", # legendary
			"Esagil-kin-apli", # 11th BC
			iClassical,
			"fEnnigaldi", # 6th BC
			"Nabu-rimanni", # 6th BC
			"Kidinnu", # 4th BC
			"Sudines", # 3rd BC
			"Bel-reu-su", # 3rd BC
		),
		iGreatMerchant : (
			"fIltani", # 18th BC
			"Ea-nasir", # 18th BC
			"Burna-Buriash", # 14th BC
			"Kadashman-Enlil", # 14th BC
			iClassical,
			"Itti-Marduk-balatu", # 6th BC
			"fBa'u-asitu", # 6th BC
		),
		iGreatEngineer : (
			"Enmebaragesi", # 30th BC
			"Naram-Sin", # 22nd BC
			"Ur-Nammu", # 21st BC
			"Kurigalzu", # 14th BC
			"Kudur-Enlil", # 13th BC
			iClassical,
			"Nabopolassar", # 7th BC
			"fNitocris", # 6th BC
		),
		iGreatStatesman : (
			"Urukagina", # 24th BC
			"Bilalama", # 20th BC
			"Lipit-Ishtar", # 19th BC
			"Dadusha", # 18th BC
			"Marduk-shapik-zeri", # 11th BC
		),
		iGreatGeneral : (
			"Enshakushanna", # 25th BC
			"Eannatum", # 25th BC
			"Naram-Sin", # 23rd BC
			iClassical,
			"Nebukanezar", # 7th BC
			"Neriglissar", # 6th BC
		),
		iGreatSpy : (
			"Bel-shar-usur", # 6th BC
		),
	},
	iAssyria : {
		iGreatProphet : (
			"Tudiya", # legendary
			"Bel-bani", # 17th BC
			"Ashurnasirpal", # 11th BC
			iClassical,
			"Nahum", # 7th BC
			"fAdad-guppi", # 6th BC
			iMedieval,
			"Babay Rabba", # 7th
		),
		iGreatArtist : (
			"Nabu-zuqup-kena", # 8th BC
			"Ahiqar", # 7th BC
			"Tatian", # 2nd
			iMedieval,
			"Toma bar Yaqub", # 9th
		),
		iGreatScientist : (
			"Samsi-Addu-tukuld", # 18th BC
			"Ashur-bel-kala", # 11th BC
			iClassical,
			"Gabbu-ilani-eresh", # 9th BC
			"Bardaisan", # 2nd
			iMedieval,
			"Masawaiyh", # 9th
			"Jabril ibn Bukhtishu", # 9th
		),
		iGreatMerchant : (
			"Erishum", # 20th BC
			"Ili-pada", # 12th BC
			iClassical,
			"Ashur-dan", # 10th BC
			"Tobias", # 8th BC
		),
		iGreatEngineer : (
			"Shalim-ahum", # 20th BC
			"Shalmaneser", # 13th BC
			iClassical,
			"fNaqi'a", # 7th BC
			"Esarhaddon", # 7th BC
		),
		iGreatStatesman : (
			"Puzur-Ashur", # 21st BC
			"Babu-aha-iddina", # 13th BC
			"Tiglath-Pileser", # 10th BC
			iClassical,
			"fShammuramat", # 9th BC
			"fLibbali-sarrat", # 7th BC
		),
		iGreatGeneral : (
			"Onnes", # legendary
			"Shamshi-Adad", # 18th BC
			"Tukulti-Ninurta", # 13th BC
			"Tiglath-Pileser", # 11th BC
			iClassical,
			"Arbaces", # 9th BC
			"Dayyan-Assur", # 9th BC
			"Shalmaneser", # 8th BC
			"Sargon", # 8th BC
			"Shamshi-ilu", # 8th BC
			"Sennacherib", # 7th BC
		),
		iGreatSpy : (
			"Arda-Mulissu", # 7th BC
			"Nabu-shar-usur", # 7th BC
		),
	},
	iNubia : {
		iGreatProphet : (
			"Alara", # 8th BC
			"fAmenirdis", # 8th BC
			"fShepenupet", # 7th BC
			iMedieval,
			"Georgios", # 11th
			"Timotheos", # 14th
			iIndustrial,
			"Muhammad Ahmad", # 19th
		),
		iGreatEngineer : (
			"Aspelta", # 7th-6th BC
			"Arnekhamani", # 3rd BC
			iMedieval,
			"Rafael", # 11th
		),
		iGreatStatesman : (
			"Shabaka", # 7th BC
			"fAmanitore", # 1st AD
			"Natakamani", # 1st AD
		),
		iGreatGeneral : (
			"Piye", # 8th BC
			"Harsiotef", # 5-4th BC
			"fAmanirenas", # 1st BC
			iMedieval,
			"Qalidurut", # 7th
		),
	},
	iChina : {
		iGreatProphet : (
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
		),
		iGreatArtist : (
			"Ling Lun", # legendary
			iClassical,
			"Li Bo", # 8th BC
			"Du Fu", # 8th BC
			"Wang Xizhi", # 4th BC
			"fCai Wenji", # 1st
			"Gu Kaizhi", # 4th
			iMedieval,
			"Yan Liben", # 7th
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
			"Xu Beihong", # 20th
			"Lin Yutang", # 20th
			"Wu Guanzhong", # 20th
		),
		iGreatScientist : (
			"Li Fan", # 1st
			"fBan Zhao", # 1st
			"Liu Hui", # 3rd
			"Zu Chongzhi", # 5th
			iMedieval,
			"Shen Kuo", # 11th
			"Zhu Shijie", # 14th
			iRenaissance,
			"Li Shizhen", # 16th
			"fTan Yunxian", # 16th
			"Xu Guangqi", # 17th
			"Song Yingxing", # 17th
			"fWang Zhenyi", # 18th
			iGlobal,
			"Li Siguang", # 20th
			"fWu Jianxiong", # 20th
			"Yang Zhenning", # 20th
			"fTu Youyou", # 20th
			"Li Yuanzhe", # 20th
		),
		iGreatMerchant : (
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
			iIndustrial,
			"Wu Bingjian", # 19th
			"Sheng Xuanhuai", # 19th
			iGlobal,
			"Zeng Junchen", # 20th
			"Deng Xiaoping", # 20th
		),
		iGreatEngineer : (
			"fLeizu", # 27th BC
			iClassical,
			"Lu Ban", # 5th BC
			"Li Bing", # 3rd BC
			"Cai Lun", # 1st
			"Zhang Heng", # 2nd
			"Ma Jun", # 3rd
			iMedieval,
			"Yi Xing", # 8th
			"Yu Hao", # 10th
			"Zhang Sixun", # 10th
			"Bi Sheng", # 11th
			"Su Song", # 11th
			"Wang Zhen", # 14th
			iGlobal,
			"Liang Sicheng", # 20th
			"fLin Huiyin", # 20th
			"Ieoh Ming Pei", # 20th
			"fLin Lanying", # 20th
			"Charles Kao Kuen", # 20th
		),
		iGreatStatesman : (
			"Gongsun Yang", # 4th BC
			"Li Si", # 3rd BC
			"Xiao He", # 2nd BC
			iMedieval,
			"Fang Xuanling", # 7th
			"fWu Zetian", # 7th
			"Di Renjie", # 7th
			"fShangguan Wan'er", # 7th
			"Fan Zhongyan", # 11th
			"Liu Bowen", # 14th
			iRenaissance,
			"Zhang Juzheng", # 16th
			"Zhang Tingyu", # 18th
			iIndustrial,
			"Lin Zexu", # 19th
			"Li Hongzhang", # 19th
			"Sun Yat-sen", # 19th
			iGlobal,
			"Zhou Enlai", # 20th
			"fJiang Qing", # 20th
		),
		iGreatGeneral : (
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
			"fQin Liangyu", # 17th
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
		),
		iGreatSpy : (
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
			"fZheng Pingru", # 20th
		),
	},
	iHittites : {
		iGreatProphet : (
			"fHannahanna", # mythological
			"fArinna", # mythological
			"Tarhunna", # mythological
			"Murshili", # 14th BC
			"fPuduhepa", # 13th BC
			"fMaathorneferure", # 13th BC
		),
		iGreatArtist : (
			"Hasameli", # mythological
			"Apaliunas", # mythological
			"Kikkuli", # 15th BC
		),
		iGreatScientist : (
			"fKamrusepa", # mythological
			"fHalki", # mythological
			"Hrpsr", # 13th BC
		),
		iGreatMerchant : (
			"Aruna", # mythological
			"Appu", # mythological
			"Zita", # 14th BC
			"Zannanza", # 14th BC
		),
		iGreatEngineer : (
			"Tudhaliya", # 13th BC
			"Katuwa", # 9th BC
			"Astiruwa", # 9th BC
			"Kamani", # 8th BC
		),
		iGreatStatesman : (
			"Telipinu", # 16th BC
			"Hattushili", # 13th BC
		),
		iGreatGeneral : (
			"Hattusili", # 17th BC
			"Tudhaliya", # 14th BC
			"Kisnapili", # 14th BC
			"Suppiluliuma", # 14th BC
			"Madduwatta", # 14th BC
			"Muwatalli", # 13th BC
			"Piyamaradu", # 13th BC
		),
		iGreatSpy : (
			"Zidanta", # 16th BC
		),
	},
	iGreece : {
		iGreatProphet : (
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
		),
		iGreatArtist : (
			"Homeros", # 8th BC
			iClassical,
			"fSappho", # 6th BC
			"Exekias", # 6th BC
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
		),
		iGreatScientist : (
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
		),
		iGreatMerchant : (
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
		),
		iGreatEngineer : (
			"Thales", # 6th BC
			"Empedokles", # 5th BC
			"Zenon", # 4th BC
			"Satyros", # 4th BC
			"Archimedes", # 3rd BC
			"Sostratos", # 3rd BC
			"Heron", # 1st
			iIndustrial,
			"Ernestos Tsiller", # 19th
			iGlobal,
			"Alexandros Issigonis", # 20th
			"Ioannis Travlos", # 20th
			"Ioannis Argyris", # 20th
		),
		iGreatStatesman : (
			"Lykourgos", # 9th BC
			iClassical,
			"Solon", # 6th BC
			"Kleisthenes", # 6th BC
			"fGorgo", # 5th BC
			"Alkibiades", # 5th BC
			"Aresteides", # 5th BC
			"Kimon", # 5th BC
			"Epaminondas", # 4th BC
			"Isokrates", # 4th BC
			"Polybios", # 2nd BC
			"Arrianos", # 2nd
			iIndustrial,
			"Adamantios Korais", # 19th
			"Ioannis Kapodistrias", # 19th
			"Eleftherios Venizelos", # 19th
			iGlobal,
			"Ioannis Metaxas", # 20th
			"Konstantinos Karamanlis", # 20th
			"Michael Christodoulou Mouskos", # 20th
			"Andreas Papandreou", # 20th
		),
		iGreatGeneral : (
			"Hektor", # legendary
			iClassical,
			"Leonidas", # 6th BC
			"Themistokles", # 5th BC
			"Lysandros", # 5th BC
			"Philippos", # 4th BC
			"fArtemisia", # 4th BC
			"Pyrrhos", # 3rd BC
			"Antiochos Megas", # 3rd BC
			iIndustrial,
			"fLaskarina Bouboulina", # 19th
			"Alexandros Ypsilantis", # 19th
			"Theodoros Kolokotronis", # 19th
			iGlobal,
			"Konstantinos Bakopoulos", # 20th
			"Alexandros Papagos", # 20th
		),
	},
	iIndia : {
		iGreatProphet : (
			"Mahavira", # 6th BC
			"Siddharta Gautama", # 6th BC
			"Ananda", # 6th BC
			"Mahakashyapa", # 6th BC
			"Nagarjuna", # 2nd
			iMedieval,
			"Atisha", # 11th
			"Ramanuja", # 11th
			"Basava", # 12th
			"Kabir", # 15th
			iRenaissance,
			"Chaitanya Mahaprabhu", # 16th
			"fMeera", # 16th
			iIndustrial,
			"Lalon", # 19th
			"Ramakrishna", # 19th
			"Swami Vivekananda", # 19th
			"Shirdi Sai Baba", # 19th
			iGlobal,
			"Paramahansa Yogananda", # 20th
			"fAnandamayi Ma", # 20th
			"fAnjeze Gonxhe Bojaxhiu", # 20th
			"Maharishi Mahesh Yogi", # 20th
			"fNirmala Srivastava", # 20th
		),
		iGreatArtist : (
			"Valmiki", # 4th BC
			"Asvaghosa", # 1st
			"Kalidasa", # 5th
			iMedieval, 
			"Gunadhya", # 6th
			"Abhinavagupta", # 10th
			"Bilhana", # 11th
			"Roda", # 12th
			"fKanhopatra", # 15th
			iRenaissance,
			"Tansen", # 16th
			"Nainsukh", # 18th
			u"Nihâl Chand", # 18th
			iIndustrial,
			"Mola Ram", # 19th
			"Muthuswami Dikshitar", # 19th
			"Raja Ravi Varma", # 19th
			iGlobal,
			"Rabindranath Tagore", # 20th
			"fGauhar Jaan", # 20th
			"Kazi Nazrul Islam", # 20th
			"Raja Rao", # 20th
			"fAmrita Sher-Gil", # 20th
			"fMadurai Shanmukhavadivu Subbulakshmi", # 20th
			"Satyajit Ray", # 20th
			"Ravi Shankar", # 20th
		),
		iGreatScientist : (
			"Yajnavalkya", # 8th BC
			"Panini", # 6th or 5th BC
			"Charaka", # 6th to 2nd BC
			"Pingala", # 3rd or 2nd BC
			iMedieval,
			"Aryabhata", # 6th
			"Dignaga", # 6th
			"Dharmakirti", # 6th or 7th
			"Brahmagupta", # 7th
			"Bhoja", # 11th
			"Bhaskara", # 12th
			"Madhava", # 14th
			iRenaissance,
			"Ganesa Daivajna", # 16th
			"Kamalakara", # 17th
			iIndustrial,
			"Jagadish Chandra Bose", # 19th
			"Indumadhab Mallick", # 19th
			iGlobal,
			"Har Gobind Khorana", # 20th
			"Satyendra Nath Bose", # 20th
			"fAsima Chatterjee", # 20th
		),
		iGreatMerchant : (
			"Nattal Sahu", # 12th
			"Jagadu", # 13th
			iIndustrial,
			"Jamsetjee Jejeebhoy", # 19th
			"Jamsetji Tata", # 19th
			"Ardeshir Godrej", # 19th
			iGlobal,
			"Jehangir Ratanji Dadabhoy Tata", # 20th
			"Amartya Sen", # 20th
			"fIndra Nooyi", # 20th
		),
		iGreatEngineer : (
			"Baudhayana", # 8th BC
			"Lagadha", # 1st
			iMedieval, 
			"Gundan Anivaritachari", # 7th
			"Ruvari Malithamma", # 12th
			iRenaissance, 
			"Vidyadhar Bhattacharya", # 18th
			"Ram Singh Malam", # 18th
			iIndustrial,
			"Bhai Ram Singh", # 19th
			"Jamsetji Tata", # 19th
			iGlobal,
			"Avul Pakir Jainulabdeen Abdul Kalam", # 20th
			"fEulie Chowdhury", # 20th
			"Satish Dhawan", # 20th
			"Charles Correa", # 20th
		),
		iGreatStatesman : (
			"Vishnu Sharma", # 12th BC to 3rd AD
			"Chanakya", # 4th BC
			iMedieval,
			"Harshavardhana", # 7th
			"Dharmapala", # 8th
			"Chavundaraya", # 10th
			iRenaissance,
			"Nana Fadnavis", # 18th
			"fBegum Samru", # 18th
			iIndustrial,
			"Ram Mohan Roy", # 19th
			"Ranjit Singh", # 19th
			"Ishwar Chandra Vidyasagar", # 19th
			iGlobal,
			"Vallabhbhai Patel", # 20th
			"fSarojini Naidu", # 20th
			"Sarvepalli Radhakrishnan", # 20th
			"Bhimrao Ramji Ambedkar", # 20th
			"Jawaharlal Nehru", # 20th
			"Sheikh Mujibur Rahman", # 20th
		),
		iGreatGeneral : (
			"Chandragupta Maurya", # 4th BC
			"Samudragupta", # 4th BC
			iMedieval,
			"Dhruva Dharavarsha", # 8th
			"Mihira Bhoja", # 9th
			iRenaissance,
			"fRani Durgavati", # 16th
			"Kanhoji Angre", # 17th
			iIndustrial,
			"Nana Sahib", # 19th
			"fRani Lakshmibai", # 19th
			iGlobal, 
			"Kodandera M. Cariappa", # 20th
			"Sam Manekshaw", # 20th
		),
		iGreatSpy : (
			"Bahirji Naik", # 17th
			"fSharan Kaur Pabla", # 17th
			iIndustrial,
			"Sarat Chandra Das", # 19th
			iGlobal,
			"fNoor Inayat Khan", # 20th
			"Rameshwarnath Kao", # 20th
			"Ravindra Kaushik", # 20th
		),
	},
	iCarthage : {
		iGreatProphet : (
			"Sakun-yaton", # unknown date
			"fJezebel", # 9th BC
			iClassical,
			"Tertullianus", # 2nd
			"Cyprianus", # 3rd
			"Donatus", # 4th
		),
		iGreatArtist : (
			"fSapanbaal", # 3rd BC
			"Micipsa", # 2nd BC
			"Ennion", # 1st AD
		),
		iGreatScientist : (
			"Mochus", # 14th BC
			"Hiram", # 10th BC
			"Sakun-yaton", # unknown date
			iClassical,
			"Mago", # 4th BC
			"Hasdrubal Clitomachus", # 2nd BC
			"Abba", # 3rd
		),
		iGreatMerchant : (
			"Acerbas", # 9th BC / legendary
			iClassical,
			"Hanno", # 5th BC
			"Himilco", # 5th BC
			"Abdashtart", # 4th BC
			"Adherbal", # 2nd BC
			"Bocchus", # 2nd BC
		),
		iGreatEngineer : (
			"Gala", # 3rd BC
			"Zelalsen", # ?
			"Malchus", # ?
			"Gauda", # ?
		),
		iGreatStatesman : (
			"Ashtar-rom", # 9th BC
			"Ithobaal", # 9th BC
			"Pu'mayyaton", # 9th BC
			"fElishat", # 8th BC
			iClassical,
			"Hanno", # 4th BC
			"Eshmuniaton", # 4th BC
			"Azelmelek", # 4th BC
			"Bomilcar", # 3rd BC
		),
		iGreatGeneral : (
			"Hasdrubal Barca", # 3rd BC
			"Hamilcar Barca", # 3rd BC
			"Mago Barca", # 3rd BC
			"Carthalo", # 3rd BC
			"Maharbal", # 2nd BC
		),
		iGreatSpy : (
			"Aristo", # 3rd BC
		),
	},
	iPolynesia : {
		iGreatProphet : (
			"Maui", # legendary
			"Kuamo'o Mo'okini", # 12th
			iIndustrial,
			"Te Kooti", # 19th
			"fAngata", # 19th
			"Rua Kenana Hepetipa", # 19th
		),
		iGreatArtist : (
			"Hawaiiloa", # legendary
			"Hotu Matu'a", # 4th-7th
			"Ui-te-Rangiora", # 7th
			"Kupe", # 10th-14th
			iIndustrial,
			"fKawena", # 20th
			"Uiliami Leilua Vi", # 20th
			"Rangi Hetet", # 20th
		),
		iGreatScientist : (
			"Nga'ara", # 19th
			"Te Rangi Hiroa", # 20th
			"Mau Piailug", # 20th
		),
		iGreatMerchant : (
			"Tupaia", # 18th
			"Mai", # 18th
			iIndustrial,
			"fPiipi Raumati", # 19th
			"Tuilaepa Aiono Sailele Malielegaoi", # 20th
		),
		iGreatEngineer : (
			"Olisihpa", # 12th
			"Tu'itatui", # 12th
			"Uluakimata", # 16th
		),
		iGreatStatesman : (
			"Talatama", # 12th
			"fSalamasina", # 15th
			"fKa'ahumanu", # 18th
			iIndustrial,
			"Haalilio", # 19th
			"fMeri Te Tai Mangakahia", # 19th
			"Apirana Ngata", # 19th
			"Wiremu Toetoe", # 19th
			"Hemara Rerehau Paraone", # 19th
		),
		iGreatGeneral : (
			"fNafanua", # legendary
			"Momo", # 11th
			iRenaissance,
			"Kamehameha", # 18th
			iIndustrial,
			"Te Rauparaha", # 19th
			"Hone Heke", # 19th
			"Seru Epenisa Cakobau", # 19th
		),
	},
	iPersia : {
		iGreatProphet : (
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
			"Sultan Sahak", # 14th
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
		),
		iGreatArtist : (
			"Sarkash", # 7th
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
			"Sani al Mulk", # 19th
			"Mirza Abdollah", # 19th
			"Kamal-ol-Molk", # 19th
			iGlobal,
			"fForough Farrokhzad", # 20th
			"Hossein Amanat", # 20th
			"fHayedeh", # 20th
		),
		iGreatScientist : (
			"Ktesias", # 5th BC
			"Ardashir", # 4th
			"Borzuya", # 6th
			"Paulos-e irani", # 6th
			"Anania Shirakatsi", # 7th
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
		),
		iGreatMerchant : (
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
		),
		iGreatEngineer : (
			"Artakhshathra", # 4th BC
			"Bahram", # 3rd
			"Mihr Narseh", # 5th
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
		),
		iGreatStatesman : (
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
		),
		iGreatGeneral : (
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
		),
		iGreatSpy : (
			"Mihr Narseh", # 5th
			"Yazdgushnasp", # 6th
			"Fariburz", # 6th
			iMedieval,
			"Hassan-i Sabbah", # 11th (also Arabian)
			iGlobal,
			"Teymur Bakhtiar", # 20th
			"Mansur Rafizadeh", # 20th
			"Qasem Soleimani", # 20th
		),
	},
	iRome : {
		iGreatProphet : (
			"fClaudia Quinta", # 3rd BC
			"Petrus", # 1st
			"Paulus Tarsensis", # 1st
			"Irenaeus", # 2nd
			"Tertullianus", # 2nd
			"Arius", # 3rd
			"Aurelius Augustinus Hipponensis", # 4th
			"Aurelius Ambrosius", # 4th
			"Eusebius Pamphili", # 4th
			"fMarcella", # 4th
		),
		iGreatArtist : (
			"Quintus Ennius", # 3rd BC
			"Titus Maccius Plautus", # 3rd BC
			"Publius Vergilius Maro", # 1st BC
			"fIaia", # 1st BC
			"Quintus Horatius Flaccus", # 1st BC
			"Titus Livius", # 1st
			"Publius Ovidius Naso", # 1st
			"Lucius Mestrius Plutarchus", # 1st
			"Marcus Annaeus Lucanus", # 1st
			"Decimus Iunius Iuvenalis", # 2nd
		),
		iGreatScientist : (
			"Marcus Terentius Varro", # 1st BC
			"Titus Lucretius Carus", # 1st BC
			"Sosigenes", # 1st BC
			"Gaius Iulius Iuba", # 1st BC
			"Antonius Castor", # 1st
			"Gaius Plinius Secundus", # 1st
			"Strabo", # 1st
			"Lucius Annaeus Seneca", # 1st
			"Columella", # 1st
			"Plotinus", # 3rd
			"Cassiodorus", # 6th
		),
		iGreatMerchant : (
			"Marcus Crassus", # 1st BC
			"Publius Sittius", # 1st BC
			"Titus Pomponius Atticus", # 1st BC
			"Sergius Orata", # 1st BC
			"Lucius Caecilius Iucundus", # 1st
			"Pomponius Mela", # 1st
			"fViria Acte", # 1st
			"Annius Plocamus", # 1st
			"Marcus Iulius Alexander", # 1st
			"Aulus Umbricis Scaurus", # 1st
			"fUmbricia Fortunata", # 1st
			"fFlavia Seia Isaurica", # 2nd
		),
		iGreatEngineer : (
			"Sergius Orata", # 2nd BC
			"Marcus Vitruvius Pollio", # 1st BC
			"Celer", # 1st AD
			"Marcus Vipsanius Agrippa", # 1st AD
			"Sextus Julius Frontinus", # 1st AD
			"Apollodorus Damascenus", # 2nd AD
		),
		iGreatStatesman : (
			"Publius Valerius Publicola", # 6th BC
			"Lucius Quinctius Cincinnatus", # 5th BC
			"Quintus Hortensius", # 3rd BC
			"Marcus Porcius Cato", # 2nd BC
			"Tiberius Sempronius Gracchus", # 2nd BC
			"Marcus Tullius Cicero", # 1st BC
			"Lucius Cornelius Sulla", # 1st BC
			"fLivia Drusilla", # 1st BC
			"Marcus Vipsanius Agrippa", # 1st BC
			"Publius Cornelius Tacitus", # 1st
			"fFulvia", # 1st
			"Lucius Cassius Dio", # 2nd
			"Diocletianus", # 3rd
		),
		iGreatGeneral : (
			"Scipio Africanus", # 2nd BC
			"Gaius Marius", # 2nd BC
			"Gnaeus Pompeius Magnus", # 1st BC
			"Germanicus", # 1st
			"Vespasianus", # 1st
			"Traianus", # 1st
			"fAgrippina", # 1st AD
			"Hadrianus", # 2nd
			"fAlbia Dominica", # 4th AD
			"Flavius Aetius", # 5th AD
		),
		iGreatSpy : (
			"Gaius Flavius Fimbria", # 1st BC
			"fLocusta", # 1st AD
			"Lucius Blassius Nigellio", # 3rd
			"Paulus Catena", # 4th
		),
	},
	iCelts : {
		iGreatProphet : (
			"fCamma", # 1st BC
			"Diviciacus", # 1st BC
			"Adiatorix", # 1st BC
			iMedieval,
			u"Pádraig", # 5th
			"Brigit", # 5-6th
			"Colm Cille", # 6th
			"Iarlaithe mac Loga", # 6th
			"Brendan of Clonfert", # 6th
			"Margaret of Scotland", # 11th
		),
		iGreatArtist : (
			"Calgacus", # 1st
			"Adna mac Uthidir", # 1st
			iMedieval,
			u"Torna Éices", # 5th
			"Dubthach maccu Lugair", # 5th
			"Taliesin", # 6th
			u"Dallán Forgaill", # 7th
			"Ferdomnach", # 9th
			"Nennius", # 9th
		),
		iGreatScientist : (
			"Pompeius Trogus", # 1st BC
			"Catius", # 1st BC
			"Gnipho", # 1st BC
			"Agroecius", # 5th
			iMedieval,
			"John Scotus Eriugena", # 9th
		),
		iGreatMerchant : (
			"Onomaris", # 4th BC
			iMedieval,
			"Madoc ab Owain Gwynedd", # 12th
		),
		iGreatEngineer : (
			"Ternan", # 5th/6th
			"Colm Cille", # 6th
			iMedieval,
			"Roolwer", # 11th
		),
		iGreatStatesman : (
			"Deiotarus", # 1st BC
			"Gaius Valerius Troucillus", # 1st BC
			"Cartimandua", # 1st
			"Cormac mac Airt", # 2nd
			iMedieval,
			"Niall Noigiallach", # Disputed
			u"Adomnán", # 5th/6th
			"Hywel Dda", # 10th
			"Brian Boru", # 11th
			"Llywelyn", # 13th
			"Robert", # 14th
		),
		iGreatGeneral : (
			"Autaritus" , # 3rd BC
			"Cassivellaunus", # 1st BC
			"Vercingetorix", # 1st BC
			"Ambiorix", # 1st BC
			"fBoudica", # 1st
			"Caratacus", # 1st
			"Ambrosius Aurelianus", # 5th
			iMedieval,
			"Owain Glyndwr", # 14th
		),
		iGreatSpy : (
			"Apaturius", # 3rd BC
			iMedieval,
			u"Máel Brigte", # 9th
		),
	},
	iMaya : {
		iGreatProphet : (
			"Junajpu", # mythological
			"Xb'alanke", # mythological
			"Jasaw Chan K'awiil", # 8th
			"Kukulkan", # 10th, named after the god
		),
		iGreatArtist : (
			"Uaxaclajuun Ub'aah K'awiil", # 8th
			"Chakalte'", # 8th
			"Jun Nat Omootz", # 8th
			"Asan Winik Tu'ub", # 8th
			"Chan Ch'ok Wayib Xok", # 8th
			"Waj Tan Chak", # 8th
			"K'ak' Tiliw Chan Chaak", # 8th
			iGlobal,
			"fMarisol Ceh Moo", # 20th
			u"Miguel Ángel Asturias", # 20th
		),
		iGreatScientist : (
			"Itzamna", # mythological
		),
		iGreatMerchant : (
			"Ek Chuaj", # mythological
			"Apoxpalon", # 16th
			"Tabscoob", # 16th
		),
		iGreatEngineer : (
			"Chan Imix K'awiil", # 7th
			"K'inich Kan Bahlam", # 7th
			"fK'ab'al Xook", # 8th
			"Ha' K'in Xook", # 8th
			"Itzam K'an Ahk", # 8th
			"K'inich Yat Ahk", # 8th
			"K'inich Ahkal Mo' Nahb", # 8th
			"Chan Chak K'ak'nal Ajaw", # 10th
		),
		iGreatStatesman : (
			"Yax Ehb Xook", # 1st
			"fYohl Ik'nal", # 6th
			"Yuknoom Ch'een", # 7th
			"Jasaw Chan K'awiil", # 8th
			"Apoch'waal", # 8th
			iGlobal,
			u"fRigoberta Menchú", # 20th
		),
		iGreatGeneral : (
			"Uneh Chan", # 6th
			"K'inich Yo'nal Ahk", # 7th
			"Wak Chanil Ajaw", # 8th
			"Hunac Ceel", # 12th
			iRenaissance,
			"Napuc Chi", # 16th
			"Tecun Uman", # 16th
		),
	},
	iDravidia : {
		iGreatProphet : (
			"Iyarpagai Nayanar", # 3rd BC
			iMedieval,
			"fKaraikkal Ammaiyar", # 5th
			"Sambandar", # 7th
			"Adi Shankara", # 8th (disputed)
			"Manikkavacakar", # 9th
			"Ramanuja", # 11th
			"Jayatirtha", # 14th
			iRenaissance,
			"Vallabha", # 15-16th
			"Nayakanahatti Thipperudra Swamy", # 15-16th
			"Vyasatirtha", # 15-16th
			"Raghuttama Tirtha", # 16th
			"Raghavendra Tirtha", # 17th
			iIndustrial,
			"Migettuwatte Gunananda Thera", # 19th
		),
		iGreatArtist : (
			"Kapilar", # 1st
			"fAvvaiyar", # 1st
			"Ilango Adigal", # 2nd
			iMedieval,
			"Nakkirar", # medieval
			"Chithalai Chathanar", # 6th
			"Sambandar", # 7th
			"fAvvaiyar", # 12th
			"Raghavanka", # 12-13th
			"Srinatha", # 14th
			"Annamacharya", # 15th
			iRenaissance,
			"Purandara Dasa", # 16th
			"Lakshmisa", # 16-17th
			iIndustrial,
			"Subramania Bharati", # 19-20th
			iGlobal,
			"Kuvempu", # 20th
		),
		iGreatScientist : (
			"Haridatta", # 7th
			"Mahavira", # 9th
			"Govinda Bhattathiri", # 13th
			"Vedanta Desika", # 14th
			"Parameshvara Nambudiri", # 14-15th
			"Nilakantha Somayaji", # 15th
			iRenaissance,
			"Jyesthadeva", # 16th
			"Melpathur Narayana Bhattathiri", # 16-17th
			iGlobal,
			"Srinivasa Ramanujan", # 20th
			"Chandrasekhara Venkata Raman", # 20th
			"Gopalasamudram Narayanan Ramachandran", # 20th
			"Calyampudi Radhakrishna Rao", # 20th
		),
		iGreatMerchant : (
			"Malayaman", # 6th-3rd BC
			"Alangudi Vanganar", # 1st
			iMedieval,
			"Kulottunga", # 11th
			"Kunje-setti", # 13th
			"Kandanambi-setti", # 14th
			iRenaissance,
			"fRani Chennabhairadevi", # 16th
			iIndustrial,
			"Yele Mallappa Shetty", # 19th	
			iGlobal,
			"Kappalottiya Tamizhan", # 20th
		),
		iGreatEngineer : (
			"Karikala", # 2nd
			"Mahasena", # 3rd
			iMedieval,
			"Narasimhavarman", # 6th
			"Mahendravarman", # 7th
			"fSembiyan Mahadevi", # 10th
			"Parakramabahu", # 12th
			"Kulothunga", # 12-13th
			"Deva Raya", # 15th
			iRenaissance,
			"fMangammal", # 17th
			iIndustrial,
			"Mokshagundam Visvesvaraya", # 19th
			"Ali Nawaz Jung Bahadur", # 19th
		),
		iGreatStatesman : (
			"Thiruvalluvar", # 4th BC to 7th AD	
			"Ellalan", # 2nd BC
			"Kharavela", # 1st BC
			"Athiyaman Neduman Anci", # 1st
			"Cenkuttuvan", # 3rd
			iMedieval,
			"Pulakeshin", # 7th
			"Amoghavarsha", # 9th
			"Rajaraja Chola", # 10th
			"Vikramaditya", # 12th
			"Jatavarman Sundara Pandyan", # 13th
			"Deva Raya", # 15th
			iRenaissance,
			"Ariyanatha Mudaliar", # 16th	
		),
		iGreatGeneral : (
			"Nedunjeliyan", # 3rd BC
			iMedieval,
			"Simhavishnu", # 6th
			"Narasimhavarman", # 7th
			"Yenathinatha Nayanar" # 6-8th
			"Rajaraja Chola", # 10th
			"Karunakara Tondaiman", # 12th
			"Rudrama Devi", # 13th
			iRenaissance,
			"Abbakka Chowta", # 16th
			iIndustrial,
			"Marthanda Varma", # 18th
			"Hyder Ali", # 18th
			"Kittur Chennamma", # 19th
		),
		iGreatSpy : (
			"Uttama", # 10th
		),
	},
	iEthiopia : {
		iGreatProphet : (
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
			"Abba Enbaqom", # 16th
			"fWalatta Petros", # 17th
			iGlobal,
			"Haile Selassie", # 20th
			"Abune Tewophilos", # 20th
		),
		iGreatArtist : (
			"Yared", # 6th
			iMedieval,
			"Giyorgis Saglawi", # 14th
			iIndustrial,
			"Gebre Hanna", # 19th
			"Afevork Ghevre Jesus", # 19th
			iGlobal,
			"Haddis Alemayehu", # 20th
			"Adamu Tesfaw", # 20th
			"Gebre Kristos Desta", # 20th
			"Afewerk Tekle", # 20th
			"Tsegaye Gabre-Medhin", # 20th
			"Alexander Boghossian", # 20th
		),
		iGreatScientist : (
			"Zar'a Ya'aqob", # 16th
			"Abba Bahriy", # 16th
			"Walda Heywat", # 17th
			"Abba Gorgoryos", # 17th
			iGlobal,
			"Aklilu Lemma", # 20th
			"Kitaw Ejigu", # 20th
			"Sossina Haile", # 20th
			"Gebisa Ejeta", # 20th
		),
		iGreatMerchant : (
			"Nigiste Saba", # legendary
			"Endubis", # 3rd
			iMedieval,
			"Yusuf bin Ahmad al-Kawneyn", # 13th
			iGlobal,
			"Berhanu Nega", # 20th
			"fEleni Gebre-Medhin", # 20th
			"Mohammed Al Amoudi", # 20th
		),
		iGreatEngineer : (
			"Gebre Mesqel Lalibela", # 13th
			iRenaissance,
			"Sarsa Dengel", # 16th
			"Fasiladas", # 17th
			iGlobal,
			"Simegnew Bekele", # 20th
			"fSossina Haile", # 20th
		),
		iGreatStatesman : (
			"Kaleb Ella Asbeha", # 6th
			iRenaissance,
			"fEleni", # 16th
			"Susenyos", # 17th
			iIndustrial,
			"Tewodros", # 19th
			"fTaytu Betul", # 19th
			"fZewditu", # 20th
			u"Gäbre-Heywät Baykädañ", # 20th
			iGlobal,
			"Mengistu Haile Mariam", # 20th
			"Meles Zenawi", # 20th
		),
		iGreatGeneral : (
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
			"Habte Giyorgis Dinagde", # 20th
			"Aman Andom", # 20th
		),
	},
	iKorea : {
		iGreatProphet : (
			"Marananta", # 4th
			iMedieval,
			"Uisang", # 7th
			"Doseon", # 9th
			"Jinul", # 12th
			"An Hyang", # 13th
			"Gil Jae", # 14th
			"Bo-u", # 14th
			iRenaissance,
			"Yi Hwang", # 16th
			"Yi I", # 16th
			"Jo Shik", # 16th
			"Song Si-yeol", # 17th
			"Yi Seung-hun", # 18th
			iIndustrial,
			"Choe Je-u", # 19th
			iGlobal,
			"Moon Sun-myung", # 20th
			"Kim Su-hwan", #20th
		),
		iGreatArtist : (
			"fYeo Ok", # Gojoseon era
			"Sol Geo", # Silla
			iMedieval,
			"Damjing", # 7th
			"Yi Nyeong", # 9th
			"Yi Je-hyeon", # 9th
			"Yangnyeong", # 15th
			"Anpyeong", # 15th
			iRenaissance,
			"fHwang Jini", # 16th
			"fSin Saimdang", # 16th
			"fHeo Nanseolheon", # 16th
			"Yun Duseo", # 17th
			"Kim Hong-do", # 18th
			"Jeong Seon", # 18th
			"Shin Yun-bok", # 18th
			iIndustrial,
			"Kim Jeong-hui", # 19th
			"Jang Seung-eop", # 19th
			iGlobal,
			"Paik Nam-jun", # 20th
			"fNa Hye-sok", # 20th
			"Im Kwon-taek", # 20th
			"Seo Taeji", # 20th
			iDigital,
			"Bong Joon-ho", # 21st
		),
		iGreatScientist : (
			"Wonhyo", # 7th
			"Kim Am", # 8th
			"Seo Gyung-deok", # 15th
			"Jeong Inji", # 15th
			"Seong Sammun", # 15th
			iRenaissance,
			"Heo Jun", # 16th
			"Choi Seok-jeong", # 17th
			"Hong Jeong-ha", # 17th
			"fSeo Yeongsuhap", # 18th
			"Hong Dae-yong", # 18th
			"Park Jiwon", # 18th
			iIndustrial,
			"Jeong Yak-yong", # 19th
			iGlobal,
			"Woo Jang-choon", # 20th
		),
		iGreatMerchant : (
			"Hyecho", # 8th
			"Uicheon", # 12th
			"Kim Sa-hyeong", # 15th
			"Yi Mu", # 15th
			"Yi Hoe", # 15th
			iRenaissance,
			"fKim Man-deok", # 18th
			"Im Sang-ok", # 18th
			"Park Jega", #1 8th
			iIndustrial, 
			"Kim Jeong-ho", # 19th
			"fPaek Son-haeng", # 19th
			iGlobal,
			"Yu Il-Han", # 20th
			"Lee Byung-chul", # 20th
			"Chung Ju-yung", # 20th
		),
		iGreatEngineer : (
			"Choe Yun-ui", # 13th
			"Choe Mu-seon", # 14th
			"Park Ja-cheong", # 14th
			iRenaissance,
			"Munjong", # 15th
			"Jang Yeong-sil", # 15th
			"Song I-yeong", # 16th
			iGlobal, 
			"Ri Sung-gi", # 20th
			"Kim Swoo-geun", # 20th
		),
		iGreatStatesman : (
			"fSeondeok", # 7th
			"Choe Chiwon", # 9th
			"Seo Hui", # 10th
			"Kim Bu-sik", # 12th
			"Jeong Dojeon", # 14th
			"Yi Saek", # 14th
			"Jeong Mongju", # 14th
			iRenaissance,
			"Hwang Hui", # 15th
			"Ryu Seong-ryong", # 16th
			"Yi Won-ik", # 16th
			"Che Je-gong", # 18th
			iIndustrial,
			"Heungseon Daewongun", # 19th
			"Kim Ok-gyun", # 19th
			"fMyeongseong", # 19th
			iGlobal,
			"Sin Chaeho", # 20th
			"Soh Jaipil", # 20th
			"fRyu Gwansun", # 20th
			"Rhee Syngman", # 20th
			"Kim Gu", # 20th
			"Kim Dae-jung", # 20th
			"Kim Young-sam", # 20th
		),
		iGreatGeneral : (
			"Gwanggaeto", # 4th
			"Kim Yu-sin", # 7th
			"Gyebaek", # 7th
			"Eulji Mundeok", # 7th
			"Yeon Gaesomun", # 7th
			"Jang Bogo", # 8th
			"Gang Gam-chan", # 11th
			"Yun Gwan", # 12th
			"Choe Young", # 14th
			"Yi Seong-gye", # 14th
			iRenaissance,
			"Nam I", # 15th
			"Gwon Ryul", # 16th
			"Yi Sun-shin", # 16th
			"Gwak Jae-woo", # 16th
			iGlobal,
			"Kim Jwa-jin", # 20th
			"Hong Beom-do", # 20th
			"Choe Hyon", # 20th
			"Paik Sun-yup", # 20th
		),
		iGreatSpy : (
			"Park Je-sang", # 4th
			"Moon Ik-jeom", # 14th
			"Nongae", # 16th
			iRenaissance,
			"Park Mun-soo", # 18th
			iGlobal,
			"An Jung-geun", # 20th
			"Yi Bong-chang", # 20th
			"Kim Jae-gyu", # 20th
		),
	},
	iToltecs : {
		iGreatScientist : (
			"Huetmatzin", # 8th
			"Papantzin", # 9th
		),
		iGreatStatesman : (
			"Chalchiuhtlatonac", # legend
			"fXiuhtlaltzin", # 10th
			"Huemac", # 11th
		),
		iGreatGeneral : (
			"Siyaj K'ak'", # 4th
			"Jatz'om Kuy", # 4th-5th
			"fXochitl", # 9th
			u"Iya Nacuaa Teyusi Ñaña", # 11th
			u"fÑuñuu Dzico-Coo-Yodzo", # 11th
		),
		iGreatSpy : (
			"Nauhyotl", # 12th
		),
	},
	iKushans : {
		iGreatProphet : (
			"Ashvaghosha", # 1st
			"Amitabha", # 2nd
			"Vasudeva", # 3rd
			"Dronala", # 3rd
		),
		iGreatArtist : (
			"fMadhurika", # 3rd
			"fVidyamati", # 3rd
		),
		iGreatScientist : (
			"Eiiomano", # 2nd
			"Mihramano", # 2nd
		),
		iGreatMerchant : (
			"fArdoksho", # mythological
			"Oesho", # mythological
			"Vima Takto", # 1st
		),
		iGreatEngineer : (
			"Nokonzoko", # 2nd
			"Xirgomano", # 2nd
			"Borzomioro", # 2nd
			"Dashavhara", # 3rd
		),
		iGreatStatesman : (
			"Kujula Kadphises", # 1st
			"Huvishka", # 2nd
		),
		iGreatGeneral : (
			"Heraios", # 1st
			"Vima Kadphises", # 2nd
			"Grumbates", # 4th
			"Kidara", # 4th
		),
		iGreatSpy : (
			"Hormizd", # 3rd
		),
	},
	iByzantium : {
		iGreatProphet : (
			"Anathasius Alexandrinus", # 4th
			"Nestorios", # 5th
			"fTheodora", # 6th
			"Ioannis o Damaskinos", # 8th
			"Kyrillos", # 9th
			"Methodios", # 9th
			"Photios", # 9th
			"Nikolaos Mystikos", # 10th
			"Athanasios o Athonites", # 10th
			"Ioannes Xiphilinos", # 11th
		),
		iGreatArtist : (
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
		),
		iGreatScientist : (
			"fHypatia", # 4th
			"Paulos Aiginitis", # 7th
			"Stephanos Alexandrinos", # 7th
			"Theophylaktos Simokates", # 7th
			"Leon o Mathematikos", # 9th
			"Michael Psellos", # 11th
			"fAnna Komnene", # 12th
			"Nikephoros Blemmydes", # 13th
			"Niketas Choniates", # 13th
			"Nikephoros Gregoras", # 14th
			"Georgios Plethon", # 15th
		),
		iGreatMerchant : (
			"Hierokles", # 6th
			"Zemarchos", # 6th
			"Kosmas Indikopleustes", # 6th
			"Georgios Kyprios", # 7th
			"fDanielis", # 9th
		),
		iGreatEngineer : (
			"Anthemios", # 6th
			"Isidoros", # 6th
			"Eutokios", # 6th
			"Kallinikos", # 7th
			"Petronas Kamateros", # 9th
			"Tiridates", # 10th
		),
		iGreatStatesman : (
			"Theodosios", # 4th
			"Tribonianos", # 6th
			"fEirene", # 6th
			"Irakleios", # 7th
			"Leon", # 9th
			"Michael Palaiologos", # 13th
		),
		iGreatGeneral : (
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
		),
		iGreatSpy : (
			"Palladios", # 5th
			"fTheodora", # 6th
			"Staurakios", # 8th
			"Samonas", # 9th
			"Nikolaos", # 10th
		),
	},
	iMalays : {
		iGreatProphet : (
			"Sakyakirti", # 7th
			"Mudzaffar Shah", # 12th
			"Sang Nila Utama", # 14th
			"Sharif Ali", # 15th
			iRenaissance,
			"Abdul Kahar", # 16th
			"Nuruddin al-Raniri", # 17th
			iIndustrial,
			"Sisingamangaraja", # 19th
			"Imam Bonjol", # 19th
		),
		iGreatArtist : (
			"Hamzah Fansuri", # 15th
			iRenaissance,
			"Tun Sri Lanang", # 16-17th
			iIndustrial,
			"Abdullah Abdul Kadir", # 19th
			"Raja Ali Haji", # 19th
			iGlobal,
			"Sudirman", # 20th
			"Zainal Abidin Ahmad", # 20th
		),
		iGreatScientist : (
			"Willem Iskander", # 19th
			"Wu Lien-teh", # 20th
		),
		iGreatMerchant : (
			"Sri Maravijayottunggavarman", # 11th
			"Muhammad Shah", # 13th
			"Muhammad Jiwa Zainal Adilin", # 15th
			"Mansur Shah", # 15th
			iRenaissance,
			"Raja Mudaliar", # 16th
			"Mahmud Shah", # 16th
			iIndustrial,
			"Aji Muhammad Alimuddin", # 19th
		),
		iGreatEngineer : (
			"Muhammad Jiwa Zainal Adilin", # 18th
			"Yap Ah Loy", # 19th
		),
		iGreatStatesman : (
			"Cudamani Warmadewa", # 10-11th
			"Parmeswara", # 14th
			"Bolkiah", # 15th
			iRenaissance,
			"Muhammad Hasan", # 16th
			"Muhammad Kudarat", # 17th
			iIndustrial,
			"Abu Bakar", # 19th
			"Mahmud Badaruddin", # 19th
			iGlobal,
			"Tunku Abdul Rahman", # 20th
		),
		iGreatGeneral : (
			"Hang Tuah", # 15th
			iRenaissance,
			"fMalahayati", # 16th
			"Ali Mughayat Syah", # 16th
			"Bendahara Sakam", # 16th
			"Hang Nadim", # 16th
			"Siti Wan Kembang", # 17th
			"Tun Abdul Jamil", # 17th
			iIndustrial,
			"Rentap", # 19th
			"fCut Nyak Dhien", # 19th
			iGlobal,
			"Adnan Saidi", # 20th
		),
		iGreatSpy : (
			"Alauddin Riayat Shah", # 15th
			iIndustrial,
			"Lela Pandak Lam", # 19th
			iGlobal,
			"Rosli Dhobi", # 20th
		),
	},
	iJapan : {
		iGreatProphet : (
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
		),
		iGreatArtist : (
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
		),
		iGreatScientist : (
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
		),
		iGreatMerchant : (
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
		),
		iGreatEngineer : (
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
		),
		iGreatStatesman : (
			"Shoutouku Taishi", # 6th
			"Fujiwara no Kamatari", # 7th
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
		),
		iGreatGeneral : (
			"Sakanoue no Tamuramaro", # 8th
			"Taira no Masakado", # 10th
			"Minamoto no Yoritomo", # 12th
			"fTomoe Gozen", # 12th
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
			"Heihachirou Tougou", # 19th
			iGlobal,
			"Isoroku Yamamoto", # 20th
			"Tomoyuki Yamashita", # 20th
			"Tadamichi Kuribayashi", # 20th
		),
		iGreatSpy : (
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
		),
	},
	iNorse : {
		iGreatProphet : (
			"Ansgar", # 9th swedish
			u"Haraldr Blátonn", # 10th danish
			u"Óláfr Haraldsson", # 11th Norwegian
			u"Knútr Sveinsson", # 11th Danish
			u"Þórlákr Þórhallsson", # 12th Icelandic
			"Erik Jedvardsson", # 12th Swedish
			iRenaissance,
			"Hans Tausen", # 16th Danish
			"Peder Palladius", # 16th Danish
			u"Jón lærði Guðmundsson", # 17th Icelandic
			"Hans Egede", # 18th Norwegian
			iIndustrial,
			"Hans Nielsen Hauge", # 19th norwegian
			u"Søren Kierkegaard", # 19th danish
			iGlobal,
			u"Knud Eljer Løgstrup", # 20th Danish
			"Kaj Munk", # 20th Danish
			u"Sveinbjörn Beinteinsson", # 20th icelandic
		),
		iGreatArtist : (
			"Bragi Boddason", # 9th norwegian
			u"fJórunn skáldmær", # 10th norwegian
			u"Egill Skallagrímsson", # 10th Icelandic
			u"Ofæigr Øpir", # 11th swedish
			"Saxo Grammaticus", # 12th Danish
			"Snorri Sturluson", # 13th icelandic
			u"Magnús Þórhallsson", # 14th Icelandic
			iRenaissance,
			"Johan Nordahl Brun", # 18th norwegian
			"Ludvig Holberg", # 18th Norwegian/Danish
			iIndustrial,
			"Hans Christian Andersen", # 19th danish
			"Edvard Munch", # 19th norwegian
			"Edvard Grieg", # 19th norwegian
			"Henrik Ibsen", # 19th Norwegian
			iGlobal,
			"fKaren Blixen", # 20th danish
			"Henrik Pontoppidan", # 20th Danish
			"Olav Duun", # 20th Norwegian
			"fSigrid Undset", # 20th Norwegian/Danish
			u"Einar Jónsson" # 20th Icelandic
			u"Halldór Laxness", # 20th icelandic
		),
		iGreatScientist : (
			u"Þorsteinn Surtr", # 10th Icelandic
			u"Stjörnu-Oddi Helgason", # 12th Icelandic
			iRenaissance,
			"Tycho Brahe", # 16th danish
			"fSophia Brahe", # 16th danish
			"Ole Worm", # 17th Danish
			u"Ole Rømer", # 17th  danish
			iIndustrial,
			"Niels Henrik Abel", # 19th norwegian			
			"Rasmus Rask", # 19th Danish
			"Karl Verner", # 19th Danish
			"Niels Ryberg Finsen", # 19th faroese
			iGlobal,
			"Niels Bohr", # 20th danish
			"Aage Bohr", # 20th Danish
			"Vilhelm Bjerknes", # 20th Norwegian
			"Ole-Johan Dahl", # 20th Norwegian
		),
		iGreatMerchant : (
			u"Håkon Sigurdsson", # 10th norwegian
			u"Eiríkr Rauði", # 10th norwegian
			u"Leifr Eiríksson", # 10th icelandic
			iRenaissance,
			"fSigbrit Willoms", # 16th danish
			"Magnus Heinason", # 16th faroese
			iIndustrial,
			"Roald Amundsen", # 20th norwegian
			iGlobal,
			"Ole Kirk Christiansen", # 20th danish
			"Ragnar Frisch", # 20th norwegian
			
			u"Óttarr frá Hálogaland", # 9th Norwegian
			u"fGuðriðr Þorbjarnardóttir", # 10th Icelandic
			u"Óláfr pái Höskuldsson", # 10th Icelandic
			u"Yngvarr Víðförli", # 11th Swedish
			"Constantin Brun", # 18th
			"fLaura Aller", # 19th Danish
			"Jacob Christian Jacobsen", # 19th Danish
			u"fÞuríður Einarsdóttir", # 19th Icelandic
			"Thor Heyerdahl", # 20th Norwegian
			u"Arnold Peter Møller", # 20th Danish
		),
		iGreatEngineer : (
			u"Gøtrik", # 9th Danish
			iRenaissance,
			"Hercules von Oberberg", # 16th danish
			"Hans van Steenwinckel" # 17th Danish
			"Caspar Frederik Harsdorff", # 18th Danish
			iIndustrial,
			"fSophy Adolfine Christensen", # 19th Danish
			"Christian Hansen", # 19th Danish
			"Peter Andreas Blix", # 19th Norwegian
			iGlobal,
			"Arne Jacobsen", # 20th danish
			u"Jørn Utzon", # 20th danish
			u"Ivar Giæver", # 20th norwegian
			u"Rasmus Sørnes", # 20th Norwegian
			u"Guðjón Samúelsson", # 20th Icelandic
		),
		iGreatStatesman : (
			"Awair Strabain", # 9th Gutnish
			"Gormr Gamli", # 10th Danish
			u"fGunnhildr Gormsdóttir", # 10th norwegian
			u"Njáll Þorgeirsson", # 10th Icelandic
			u"Jón Loptsson", # 12th Icelandic
			"fMargrete Valdemarsdatter", # 14th danish
			iRenaissance,
			"Niels Kaas", # 16th Danish
			iIndustrial,
			"Nikolaj Frederik Severin Grundtvig", # 19th danish
			u"Jón Sigurðsson", # 19th Icelandic
			iGlobal,
			"Trygve Lie", # 20th norwegian
			u"Ólafur Thors", # 20th Icelandic
		),
		iGreatGeneral : (
			u"fHlaðgerðr", # 9th danish
			u"Hásteinn", # 9th Danish
			u"Ívarr inn Beinlausi", # 9th Swedish
			u"Haraldr Hárfagri", # 9th Norwegian
			u"Eiríkr Blóðøx", # 10th norwegian
			u"Sveinn Tjúguskegg", # 10th danish
			u"Knútr inn Ríki", # 11th Danish
			u"Harald Harðráði", # 11th norwegian
			"Knutr", # 11th danish
			u"Sigurðr Jórsalafari", # 12th Norwegian
			iRenaissance,
			"Johan Rantzau", # 16th
			"Peter Tordenskjold", # 18th norwegian
			iGlobal,
			"Steen Andersen Bille", # 19th Danish
			"Hans Henrik Rode", # 19th Norwegian
			"Carl Gustav Fleischer", # 20th norwegian	
		),
		iGreatSpy : (
			u"Gísli Súrsson", # 10th Icelandic
			u"Grettir Ásmundarson", # 11th Icelandic
			"Niels Ebbesen", # 14th Danish
			"fBirgitte Olufsdatter Thott", # 15th Danish/Swedish
			iRenaissance,
			"Corfitz Ulfeldt", # 17th Danish
			"fDina Vinhofvers", # 17th Danish
			iIndustrial,
			u"Jørgen Jørgensen", # 19th danish
			"Walter Christmas", # 19th Danish
			iGlobal,
			"Kai Henning Bothildsen Nielsen", # 20th danish
			u"fAstrid Døvle", # 20th norwegian
			"Arne Treholt", # 20th Norwegian
		),
	},
	iTurks : {
		iGreatProphet : (
			"Tatpar Qaghan", # 6th
			"Bulan", # 9th
			"Abu Mansur al-Maturidi", # 9th
			"Muhammad al-Bukhari", # 9th
			"Al-Ghazali", # 11th (also Persian)
			"Ahmad Yasawi", # 12th
			"fFatima al-Samarqandi", # 12th
			"Haji Bektash Veli", # 13th
		),
		iGreatArtist : (
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
		),
		iGreatScientist : (
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
		),
		iGreatMerchant : (
			"Maniakh", # 6th
			"Muqan Qaghan", # 6th
			"Sheguy", # 7th
			"Ahmad ibn Rustah", # 10th
			"Bar Sauma", # 13th 
			"Yahballaha", # 13th
		),
		iGreatEngineer : (
			"Omurtag", # 9th
			"Abu-Mahmud Khojandi", # 10th
			"Al-Biruni", # 11th 
			"fSaray Mulk", # 14th
			iGlobal,
			"Kanysh Satbayev", # 20th
		),
		iGreatStatesman : (
			u"Istämi", # 6th
			"Ishbara Qaghan", # 6th
			"Ashina Simo", # 7th
			"Nizam al-Mulk", # 11th (also Persian)
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
		),
		iGreatGeneral : (
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
		),
	},
	iArabia : {
		iGreatProphet : (
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
			"Abd al-Rahman al-Kawakibi", # 19th
		),
		iGreatArtist : (
			"Al-Asma'i", # 8th
			"fFatima al-Suqutriyya", # 9th
			"Ibn Muqla", # 10th
			"Ibn al-Nadim", # 10th
			"Al-Mutanabbi", # 10th
			"Muhammad ibn al-Zayn", # 14th
			iRenaissance,
			"Ibn Furtu", # 16th
			iGlobal,
			"Muhammad al-Maghut", # 20th
		),
		iGreatScientist : (
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
		),
		iGreatMerchant : (
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
		),
		iGreatEngineer : (
			"Jabir ibn Hayyan", # 8th
			"Mashallah ibn Athari", # 8th
			"Banu Musa", # 9th
			"Ibn Wahshiyah", # 10th
			"fMariam al-Astrulabi", # 10th
			"Al-Jazari", # 12th
			iGlobal,
			"Hassan Fathy", # 20th
			"fZaha Hadid", # 20th
		),
		iGreatStatesman : (
			"fFatimah bint Muhammad", # 7th
			"Ziyad ibn Abih", # 7th
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
		),
		iGreatGeneral : (
			"Khalid ibn al-Walid", # 7th
			"Muawiyah", # 7th
			"Amr ibn al-As", # 7th
			"fKhawla bint al-Azwar", # 7th
			"Nur ad-Din Zengi", # 12th
			iRenaissance,
			"Rahmah ibn Jabir Al Jalhami", # 18th
			iGlobal, 
			"Yusuf al-'Azma", # 20th
			"Abd al-Karim Qasim", # 20th
		),
		iGreatSpy : (
			"fSitt al-Mulk", # 11th
			"Hassan-i Sabbah", # 11th (also Persian)
			"Rashid ad-Din Sinan", # 12th
			iGlobal, 
			"Ali Hassan al-Majid", # 20th
		),
	},
	iTibet : {
		iGreatProphet : (
			"Gendun Drup", # 15th
			"Gendun Gyatso", # 15-16th
			"Sonam Gyatso", # 16th
			"Yonten Gyatso", # 16-17th
			"Tsangyang Gyatso", # 17th
			iGlobal,
			"Tenzin Gyatso", # 20th
		),
		iGreatArtist : (
			"fYeshe Tsogyal", # 8th
			"Milarepa", # 11th
			iRenaissance,
			u"Chöying Dorje", # 17th
			"Situ Panchen", # 18th
			iIndustrial,
			u"Gendün Chöphel", # 20th
		),
		iGreatScientist : (
			"Thonmi Sambhota", # 7th
			"Yuthog Yontan Gonpo", # 8th and 12th
			"Tsongkhapa", # 14th
			iRenaissance,
			"Kunkhyen Pema Karpo", # 16h
			iIndustrial,
			"Khyenrab Norbu", # 20th
		),
		iGreatMerchant : (
			"Sonam Rapten", # 17th
			iIndustrial,
			"Tsarong", # 20th
		),
		iGreatEngineer : (
			"Rinchen Zangpo", # 10th
			"Thang Tong Gyalpo", # 15th
			iRenaissance,
			"Desi Sangye Gyatso", # 17th
		),
		iGreatStatesman : (
			u"fThrimalö", # 7th
			u"Gar Tongsten Yülsung", # 7th
			iIndustrial,
			"Paljor Dorje Shatra", # 19th
			"Lhalu Tsewang Dorje", # 20th
		),
		iGreatGeneral : (
			"Gar Trinring Tsendro", # 7th
			"Chimshang Gyalsig Shuteng", # 8th
			"Nganlam Takdra Lukhong", # 8th
			"Nanam Shang Gyaltsen Lhanang", # 8th
			iRenaissance,
			"Ngawang Namgyal", # 17th
		),
	},
	iJava : {
		iGreatProphet : (
			"Buddha Pahyien", # 4th
			"Maha Rsi Agastya", # 5th
			"Sawerigading", # 6th
			"Sakyakirti", # 7th
			"Jayabaya", # 12th
			"fGayatri Rajapatni", # 14th
			"Sunan Kalijaga", # 15th
			"Raden Abdul Jalil", # 15th
			iRenaissance,
			"Sunan Giri", # 15th
			"Sunan Gunung Jati", # 16th
			iIndustrial, 
			"Ahmad Dahlan", # 19th
			"Ranggawarsita", # 19th
			iGlobal,
			"Albertus Soegijapranata", # 20th
			"Idham Chalid", # 20th
			"Hasyim Asyari", # 20th
		),
		iGreatArtist : (
			"Empu Dharmaja", # 12th			
			"Mpu Prapanca", # 14th
			iIndustrial,
			"Raden Saleh", # 19th
			"Colliq Pujie", # 19th
			"Affandi", # 20th
			"Tengku Amir Hamzah", # 20th
			"Ismail Marzuki", # 20th
			"Pramoedya Ananta Toer", # 20th
			"Asep Sunandar Sunarya", # 20th
			"I Made Sidia", # 20th
		),
		iGreatScientist : (
			"Empu Tantular", # 14th
			iRenaissance,
			"Karaeng Pattingalloang", # 17th
			iIndustrial,
			"Wahidin Soedirohoesodo", # 19th
			iGlobal,
			"Herman Johannes", # 20th
			"Suwardi Suryaningrat", # 20th
			"Soetomo", # 20th
			"Wahidin Sudirohusodo", # 20th
			"Wilhelmus Zakaria Johannes", # 20th
			"Johannes Leimena", # 20th
		),
		iGreatMerchant : (
			"Dewawarman", # 1st
			"fSri Kahulunnan", # 9th
			iIndustrial,
			"Nahkoda Muda", # 18th
			"Low Lan Pak", # 18th
			"Oei Tiong Ham", # 19th
			"Suria Kusumah Adinata", # 19th
			"Hamengkubuwana", # 19th
			iGlobal,
			"Samanhudi", # 20th
			"Liem Sioe Liong", # 20th
		),
		iGreatEngineer : (
			"Gunadharma", # 9th
			"Samaratungga", # 9th
			"Rakai Pikatan", # 9th
			iRenaissance,
			"Ageng Tirtayasa", # 17th
			iGlobal, 
			"Liem Bwan Tjie", # 20th
			"Soejoedi Wirjoatmodjo", # 20th
			"Friedrich Silaban", # 20th
			"Sedyatmo", # 20th
		),
		iGreatStatesman : (
			"Gajah Mada", # 14th
			"fTribhuwana Vijayatunggadewi", # 14th
			"Raden Patah", # 15th
			iRenaissance,
			"Siliwangi", # 16th
			"Baabullah", # 16th
			"Sultan Agung Anyakrakusuma", # 17th
			iIndustrial,
			"Hamengkubuwana", # 18th
			"Mahmud Badaruddin", # 19th
			"fRaden Ayu Kartini", # 19th
			"Suria Atmaja", # 19th
			iGlobal,
			"Sukarno", # 20th
			"Agus Salim", # 20th
			"Supomo", # 20th
			"Mohammad Yamin", # 20th
			"Chep the Magnificent", # Contest Reward
		),
		iGreatGeneral : (
			"Dharmawangsa", # 10th
			"Airlangga", # 11th
			"Ken Arok", # 12th
			"Raden Wijaya", # 13th
			iRenaissance,			
			"fRatu Kalinyamat", # 16th
			"Arung Palakka", # 17th
			"fMartha Christina Tiahahu", # 18th
			"Pattimura", # 18th
			"Mangkunegara", # 18th
			iIndustrial, 
			"Dipanegara", # 19th
			iGlobal, 
			"Oerip Soemohardjo", # 20th
			"Sudirman", # 20th
		),
		iGreatSpy : (
			"fNyimas Utari Sandijayaningsih", # 17th
			iGlobal,
			"fMarie Zumariyah", # 20th
			"Subandrio", # 20th
			"Tan Malaka", # 20th
		),
	},
	iMoors : {
		iGreatProphet : (
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
		),
		iGreatArtist : (
			"Ziryab", # 9th
			"fWallada bint al-Mustakfi", # 11th
			"fQasmuna", # 12th
			"Ibn Tufail", # 12th
			"Ibn Quzman", # 12th
			"Al-Shustari", # 13th
			"Ibn Sahl", # 13th
			iRenaissance,
			"Ahmad Ibn al-Qadi", # 16th
			"Mohammed Awzal", # 18th
			iIndustrial, 
			"Kaddour El Alamy", # 19th
			iGlobal,
			"Abdessadeq Cheqara", # 20th
		),
		iGreatScientist : (
			"Al-Zahrawi", # 10th
			"Ibn Zuhr", # 12th
			"Jabir bin Aflah", # 12th
			"Ibn Rushd", # 12th
			"Ibn Bajja", # 12th
			"Abu al-Salt", # 12th
			"Al-Qalasadi", # 15th
			iRenaissance, 
			"Abul Qasim ibn Mohammed al-Ghassani", # 16th
		),
		iGreatMerchant : (
			"Ibrahim ibn Yaqub", # 10th
			"Al-Bakri", # 11th
			"Al-Idrisi", # 12th
			"Ibn Jubayr", # 12th
			"Ibn Battuta", # 14th
			iRenaissance,
			"Hassan al-Wazzan", # 16th
		),
		iGreatEngineer : (
			"Abbas ibn Firnas", # 9th
			"Ibn Bassal", # 11th
			"Al-Zarqali", # 11th
			"Al-Muradi", # 11th
			iRenaissance,
			"Ahmed el Inglizi", # 18th
		),
		iGreatStatesman : (
			"fZaynab an-Nafzawiyyah", # 11h
			"Ibn al-Khatib", # 14th
			"Ibn Khaldun", # 14th
			iRenaissance, 
			"fLalla Aisha Mubarka", # 17th
			"Abu al-Qasim al-Zayyani", # 18th
			iGlobal,
			"Habib Bourguiba", # 20th
		),
		iGreatGeneral : (
			"Tariq ibn Ziyad", # 8th
			"Muhammad ibn Abi Aamir", # 10th
			"Yusuf ibn Tashfin", # 11th
			"Abd al-Mu'min", # 12th
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
		),
	},
	iSpain : {
		iGreatProphet : (
			"Juan de Ortega", # 11th
			u"Domingo de Guzmán", # 12th
			iRenaissance,
			"Ignacio de Loyola", # 16th
			u"Juan de Sepúlveda", # 16th
			"Francisco Javier", # 16th
			u"fTeresa de Ávila", # 16th
			u"Francisco Suárez", # 16th
			u"Bartolomé de Las Casas", # 16th
			iIndustrial,
			u"Junípero Serra", # 18th
			"fJoaquima de Vedruna", # 19th
			iGlobal, 
			u"Josemaría Escrivá", # 20th
		),
		iGreatArtist : (
			"Gonzalo de Berceo", # 13th
			"Juan Manuel", # 14th
			iRenaissance,
			"Miguel de Cervantes", # 16th
			"Garcilaso de la Vega", # 16th
			u"Tomás Luis de Victoria", # 16th
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
		),
		iGreatScientist : (
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
		),
		iGreatMerchant : (
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
		),
		iGreatEngineer : (
			"Juan Bautista de Toledo", # 16th
			"Juan de Herrera", # 16th
			iIndustrial,
			u"Agustín de Betancourt", # 18th
			u"Lluís Domènech i Montaner", # 19th
			u"Antoni Gaudí", # 19th
			"Leonardo Torres y Quevedo", # 19th
			"Alberto de Palacio y Elissague", # 19th
			iGlobal,
			"Esteban Terradas i Illa", # 20th
			"Juan de la Cierva", # 20th
			"Ricardo Bofill", # 20th
		),
		iGreatStatesman : (
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
		),
		iGreatGeneral : (
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
		),
		iGreatSpy : (
			u"Tomás de Torquemada", # 15th
			"Bernardino de Mendoza", # 17th
			u"fManuela Desvalls Vergós", # 18th
			"Ali Bey el Abbassi", # 18th 
			iGlobal,
			u"Juan Pujol García", # 20th
			u"Ramón Mercader", # 20th
		),
	},
	iFrance : {
		iGreatProphet : (
			u"Pierre Abélard", # 12th
			u"Pierre Vaudès", # 12th
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
		),
		iGreatArtist : (
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
		),
		iGreatScientist : (
			"Gerbert d'Aurillac", # 10th
			"Guy de Chauliac", # 14th
			"Nicole Oresme", # 14th
			iRenaissance,
			"Marin Mersenne", # 17th
			u"René Descartes", # 17th
			"Pierre de Fermat", # 17th
			"Blaise Pascal", # 17th
			"Antoine Lavoisier", # 18th
			u"fÉmilie du Châtelet", # 18th
			iIndustrial,
			"Pierre-Simon Laplace", # 18th
			"Georges Cuvier", # 19th
			"Louis Pasteur", # 19th
			"fMarie-Sophie Germain", # 19th
			"fMarie Curie", # 19th
			"Antoine Henri Becquerel", # 19th
			u"Henri Poincaré", # 19th
			iGlobal,
			u"fIrène Joliot-Curie", # 20th
			"Jacques Monod", # 20th
			u"Benoît Mandelbrot", # 20th
			"Alexandre Grothendieck", # 20th
		),
		iGreatMerchant : (
			u"Éloi de Noyon", # 7th
			u"fJeanne la Fouacière", # 13th
			iRenaissance,
			"Jacques Cartier", # 16th
			"Samuel de Champlain", # 17th
			"Pierre Le Moyne d'Iberville", # 17th
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
		),
		iGreatEngineer : (
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
			"Sadi Carnot", # 19th
			"Louis Daguerre", # 19th
			"Norbert Rillieux", # 19th
			"Alexandre Gustave Eiffel", # 19th
			iGlobal,
			u"Louis Lumière", # 20th
			"Le Corbusier", # 20th
		),
		iGreatStatesman : (
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
		),
		iGreatGeneral : (
			"Charles Martel", # 8th
			"Godefroy de Bouillon", # 11th
			"fJeanne de Flandre", # 14th
			"Charles V", # 14th
			"fJeanne d'Arc", # 15th
			iRenaissance,
			u"Louis de Bourbon-Condé", # 17th
			"Turenne", # 17th
			"Maurice de Saxe", # 18th
			"Louis-Joseph de Montcalm", # 18th
			u"Louis-René de Latouche-Tréville", # 18th
			"Lazare Carnot", # 18th
			iIndustrial,
			u"André Masséna", # 18th
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
		),
		iGreatSpy : (
			u"Bertrandon de la Broquière", # 15th
			"fAntoinette de Maignelais", # 15th
			iRenaissance,
			"fCharlotte de Sauve", # 16th
			u"fMarie Anne de La Trémoille", # 17th
			"fCharlotte Corday", # 18th
			"Pierre Beaumarchais", # 18th
			u"Chevalier d'Éon", # 18th
			iIndustrial,
			"fMichelle de Bonneuil", # 19th
			"Charles Schulmeister", # 19th
			iGlobal,
			u"fJoséphine Baker", # 20th
			"Gilbert Renault", # 20th
		),
	},
	iKhmer : {
		iGreatProphet : (
			"Sanghapala", # 6th
			"Kirtipandita", # 10th
			"Suryavarman I", # 11th
			"fJayarajadevi", # 12th
			"Tamalinda", # 12th
			iGlobal,
			"Chuon Nath", # 20th
			"Maha Ghosananda", # 20th
		),
		iGreatArtist : (
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
		),
		iGreatScientist : (
			"Semahatata", # 7th
			"Jayavarman V", # 10th
			"Yajnavaraha", # 10th
			"fSaptadevakula Prana", # 10th
			iGlobal,
			"Keng Vannsak", # 20th
		),
		iGreatMerchant : (
			"Jayavarman IV", # 10th
			"Srindravarman", # 14th
			"fDaun Penh", # 14th
			iRenaissance,
			"Chey Chettha", # 16th
			"Srei Meara", # 17th
			iGlobal,
			"Teng Bunma", # 20th
		),
		iGreatEngineer : (
			"Indravarman I", # 9th
			"Yasovarman I", # 9th
			"fJahavi", # 10th
			"Udayadityavarman II", # 11th
			"Jayavarman VII", # 12th 
			iGlobal,
			"Vann Molyvann", # 20th
		),
		iGreatStatesman : (
			"Jayavarman II", # 9th
			"Harshavarman", # 10th
			iIndustrial,
			"Norodom", # 19th
			iGlobal,
			"Tou Samouth", # 20th
		),
		iGreatGeneral : (
			"Bhavavarman", # 6th
			"Rajendravarman II", # 10th
			"Sangrama", # 11th
			"Vidyanandana", # 12th
			iGlobal,
			"Sak Sutsakhan", # 20th
			"Dien Del", # 20th
		),
		iGreatSpy : (
			"fYun Yat", # 20th
		),
	},
	iEngland : {
		iGreatProphet : (
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
		),
		iGreatArtist : (
			u"Ælfric of Eynsham", # 10th
			"Geoffrey Chaucer", # 14th
			"Thomas Malory", # 15th
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
			"fGeorge Eliot", # 19th
			"Arthur Conan Doyle", # 19th
			iGlobal,
			"fVirginia Woolf", # 20th
			"James Joyce", # 20th
			"fAgatha Christie", # 20th
			"John R. R. Tolkien", # 20th
			"Alfred Hitchcock", # 20th
			"John Lennon", # 20th
		),
		iGreatScientist : (
			"Byrhtferth", # 10th
			"Robert Grosseteste", # 13th
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
			"fMary Somerville", # 19th
			"Michael Faraday", # 19th
			"fMary Anning", # 19th
			"Charles Darwin", # 19th
			"fAda Lovelace", # 19th
			"James Clerk Maxwell", # 19th
			iGlobal,
			"Ernest Rutherford", # 20th
			"Alexander Fleming", # 20th
			"Alan Turing", # 20th
			"fRosalind Franklin", # 20th
			"Stephen Hawking", # 20th
		),
		iGreatMerchant : (
			"Alan Rufus", # 11th
			"Aaron of Lincoln", # 12th
			"William Caxton", # 15th
			iRenaissance,
			"Francis Drake", # 16th
			"William Petty", # 17th
			"James Cook", # 18th
			"Adam Smith", # 18th
			iIndustrial,
			"David Ricardo", # 18th
			"George Hudson", # 19th
			"Richard Francis Burton", # 19th
			"Thomas Sutherland", # 19th
			"Cecil Rhodes", # 19th
			iGlobal,
			"John Maynard Keynes", # 20th
		),
		iGreatEngineer : (
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
			"Charles Babbage", # 19th
			"Isambard Kingdom Brunel", # 19th
			"Henry Bessemer", # 19th
			"William Thomson Kelvin", # 19th
			iGlobal,
			"John Logie Baird", # 20th
			"fVictoria Drummond", # 20th
			"Frank Whittle", # 20th
			"Tim Berners-Lee", # 20th
		),
		iGreatStatesman : (
			"Thomas Becket", # 12th
			iRenaissance,
			"William Cecil", # 16th
			"John Locke", # 17th
			"Thomas Hobbes", # 17th
			"Robert Walpole", # 18th
			"William Pitt", # 18th
			"fMary Wollstonecraft", # 18th
			iIndustrial,
			"Jeremy Bentham", # 18th
			"John Stuart Mill", # 19th
			"William Gladstone", # 19th
			"Benjamin Disraeli", # 19th
			"Robert Gascoyne-Cecil Salisbury", # 19th
			iGlobal,
			"Thomas Edward Lawrence", # 20th
			"fEmmeline Pankhurst", # 20th
			"Clement Atlee", # 20th
			"fDiana Spencer", # 20th
		),
		iGreatGeneral : (
			"William the Conqueror", # 11th
			"Richard the Lionheart", # 12th
			"Edward III", # 14th
			"fMargaret of Anjou", # 15th
			iRenaissance,
			"Oliver Cromwell", # 17th
			"John Churchill Marlborough", # 17th
			"Jeffery Amherst", # 18th
			"Horatio Nelson", # 18th
			iIndustrial,
			"John Jervis", # 18th
			"Arthur Wellesley Wellington", # 19th
			"Edmund Lyons", # 19th
			iGlobal,
			"Edmund Allenby", # 19th
			"Hugh Dowding", # 20th
			"Bernard Law Montgomery", # 20th
			"William Slim", # 20th
			"Harold Alexander", # 20th
		),
		iGreatSpy : (
			"Francis Walsingham", # 16th
			"Guy Fawkes", # 16th
			"Robert Poley", # 16th
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
		),
	},
	iHolyRome : {
		iGreatProphet : (
			"fHildegard von Bingen", # 12th
			"Albertus Magnus", # 13th
			"fGertrud von Helfta", # 13th
			"Jan Hus", # 14th
			iRenaissance,
			"Martin Luther", # 16th
			"fArgula von Grumbach", # 16th
			"Philip Melanchthon", # 16th
			"fAnne Catherine Emmerich", # 18th
			iIndustrial,
			"Theodor Herzl", # 19th
			"Rudolf Steiner", # 19th
			iGlobal,
			u"Franz König", # 20th
		),
		iGreatArtist : (
			"fRoswitha von Gandersheim", # 10th
			"Wolfram von Eschenbach", # 12th
			"Walther von der Vogelweide", # 13th
			u"Albrecht Dürer", # 15th
			iRenaissance,
			"Johann Sebastian Bach", # 18th
			"Joseph Haydn", # 18th
			"Ludwig van Beethoven", # 18th
			"Wolfgang Amadeus Mozart", # 18th
			"Johann Wolfgang von Goethe", # 18th
			"Friedrich Schiller", # 18th
			iIndustrial,
			"Franz Liszt", # 19th
			"Johann Strauss", # 19th
			u"Antonín Dvorák", # 19th
			"Gustav Mahler", # 19th
			"Gustav Klimt", # 19th
			iGlobal,
			u"Arnold Schönberg", # 20th
			"Rainer Maria Rilke", # 20th
			"Franz Kafka", # 20th
			"Stefan Zweig", # 20th
			"Egon Schiele", # 20th
			"Fritz Lang", # 20th
		),
		iGreatScientist : (
			"Hrabanus Maurus", # 9th
			"Regiomontanus", # 15th
			"Konrad Celtes", # 15th
			"Johannes Trithemius", # 15th
			iRenaissance,
			"Theophrastus von Hohenheim", # 16th
			"Gerhard Mercator", # 16th
			"Johannes Kepler", # 17th
			"Gottfried Leibniz", # 17th
			"fCaroline Herschel", # 18th
			iIndustrial,
			"Ignaz Semmelweis", # 19th
			"Gregor Mendel", # 19th
			"Sigmund Freud", # 19th
			iGlobal,
			"fLise Meitner", # 20th
			u"Erwin Schrödinger", # 20th
			"Ludwig Wittgenstein", # 20th
			u"Albert Szent-Györgyi", # 20th
			"Wolfgang Pauli", # 20th
			u"Kurt Gödel", # 20th
			u"Paul Erdös", # 20th
		),
		iGreatMerchant : (
			"Hildebrand Veckinchusen", # 14th
			"Jakob Fugger", # 15th
			iRenaissance,
			"Bartholomeus Welser", # 16th
			"fBarbara Uthmann", # 16th
			"Johann Hinrich Gossler", # 18th
			"Mayer Amschel Rothschild", # 18th
			iIndustrial,
			"Friedrich List", # 19th
			"Carl Menger", # 19th
			iGlobal,
			"Joseph Schumpeter", # 20th
			"Ludwig von Mises", # 20th
			"Ferdinand Anton Ernst Porsche", # 20th
		),
		iGreatEngineer : (
			"fSabina von Steinbach", # 13th
			"Heinrich Parler", # 14th
			"Peter Parler", # 14th
			"Johannes Gutenberg", # 15th
			"Benedikt Ried", # 15th
			iRenaissance,
			"Elias Holl", # 17th
			"Johann Bernhard Fischer von Erlach", # 17th
			"Balthasar Neumann", # 18th
			"Johann Lukas von Hildebrandt", # 18th
			iIndustrial,
			u"Ányos Jedlik", # 20th
			"Alois Negrelli", # 19th
			"Carl Auer von Welsbach", # 19th
			iGlobal,
			u"Oszkár Asboth", # 20th
			u"fMargarete Schütte-Lihotzky", # 20th
			"Friedensreich Hundertwasser", # 20th
		),
		iGreatStatesman : (
			"Heinrich der Vogler", # 10th
			"Hermann von Salza", # 12th
			"Nikolaus von Kues", # 15th
			iRenaissance,
			"Nikolaus Georg von Reigersberg", # 17th
			u"Heinrich von Brühl", # 18th
			"Wenzel Anton von Kaunitz-Rietberg", # 18th
			iIndustrial,
			u"István Széchenyi", # 19th
			"Klemens von Metternich", # 19th
			"Lajos Kossuth", # 19th
			"Friedrich Ferdinand von Beust", # 19th
			"fBertha von Suttner", # 19th
			iGlobal,
			"Karl Renner", # 20th
			"Richard von Coudenhove-Kalergi", # 20th
			"Kurt Waldheim", # 20th
		),
		iGreatGeneral : (
			u"Otto der Große", # 10th
			u"Heinrich der Löwe", # 12th
			iRenaissance,
			u"Götz von Berlichingen", # 16th
			"Albrecht von Wallenstein", # 17th
			"Eugen von Savoyen", # 17th
			"Gideon Ernst von Laudon", # 18th
			iIndustrial,
			"Josef Wenzel Radetzky von Radetz", # 19th
			u"Karl von Österreich-Teschen", # 19th
			"Wilhelm von Tegetthoff", # 19th
			iGlobal,
			u"Franz Conrad von Hötzendorf", # 20th
		),
		iGreatSpy : (
			"fAgnes Le Louchier", # 17th
			iIndustrial,
			"Alfred Redl", # 19th
			iGlobal,
			"fStephanie von Hohenlohe", # 20th
			"Wilhelm Franz von Habsburg-Lothringen", # 20th
		),
	},
	iMali : {
		iGreatProphet : (
			"Wali Keita", # 13th
			"Sidi Yahya", # 15th
			iRenaissance,
			"Seku Amadu", # 18th
			"Ali Coulibaly", # 18th
		),
		iGreatArtist : (
			"Nare Maghann Konate", # 13th
			iGlobal,
			"Lobi Traore", # 20th
			"Ibrahim Aya", # 20th
		),
		iGreatScientist : (
			"Gaoussou Diawara", # 14th
			"Abu al Baraaka", # 12-16th
			iRenaissance,
			"Mohammed Bagayogo", # 16th
			"Ahmed Baba", # 16th
			iIndustrial,
			"Ag Mohammed Kawen", # 19th
		),
		iGreatMerchant : (
			"Tunka Manin", # 11th
			"Abubakari", # 13th
			"Abu Bakr ibn Ahmad Biru", # 12-16th
			iGlobal,
			u"Mandé Sidibé", # 20th
		),
		iGreatEngineer : (
			"Sakura", # 13th
			"Al-Qadi Aqib ibn Umar", # 13th
			"Abu Es Haq es Saheli", # 14th
			"Mohammed Naddah", # 15th
			iRenaissance,
			"Mohammed Bagayogo", # 16th
		),
		iGreatStatesman : (
			"Askia Muhammad", # 15th
			iRenaissance,
			u"Bitòn Coulibaly", # 18th
			iIndustrial,
			u"Samori Touré", # 19th
			iGlobal,
			"Modibo Keita", # 20th
			u"Alpha Oumar Konaré", # 20th
		),
		iGreatGeneral : (
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
		),
	},
	iBurma : {
		iGreatProphet : (
			"Kyiso", # 11th
			"Shin Arahan", # 11th
			"Shin Ditha Pamauk", # 13th
			iIndustrial,
			"Ledi Sayadaw", # 19th
			iGlobal,
			"fMya Nan Nwe", # 20th
			"U Wisara", # 20th
		),
		iGreatArtist : (
			"Shin Mahasilavamsa", # 15th
			"Shin Ratthasara", # 15th
			iGlobal,
			"San Win", # 20th
			"Ngwe Gaing", # 20th
			"Lun Gywe", # 20th
		),
		iGreatScientist : (
			"Shaw Loo", # 19th
		),
		iGreatEngineer : (
			"Nyaung-u Sawrahan", # 10th
			"fSaw Mon Hla", # 11th
			"Alaungsithu", # 12th
			iGlobal,
			"Sayadaw U Narada", # 20th
		),
		iGreatStatesman : (
			"Pyinbya", # 9th
			"Kyansittha", # 11th
			"Narapatisithu", # 12th
			iRenaissance,
			"Tabinshwehti", # 16th
			"Thalun", # 17th
			"Alaungpaya", # 18th
			iIndustrial,
			"Mindon Min", # 19th
			"Kanaung Mintha", # 19th
			iGlobal,
			"U Thant", # 20th
			"U Nu", # 20th
			"fAung San Suu Kyi", # 20th
		),
		iGreatGeneral : (
			"Athinkhaya", # 13th
			"Yazathingyan", # 13th
			"Thihathu", # 13th
			"Thilawa", # 14th
			iRenaissance,
			"Binnya Dala", # 16th
			"Hsinbyushin", # 18th
			iIndustrial,
			"Maha Bandula", # 18-19th
			"Saya San", # 19-20th
		),
		iGreatSpy : (
			"Sale Ngahkwe", # 10th
			"Lagun Ein", # 14th
		),
	},
	iRus : {
		iGreatProphet : (
			"fOlga", # 10th
			"Volodymyr Sviatoslavych", # 10th
			"Nastas Korsunyanyn", # 10th
			"Gleb", # 11th
			"Danyyil Palomnyk", # 11th
			"Kiryla Turawski", # 12th
			"Kuksha Pecherskyy", # 12th
			iRenaissance,
			"Petro Mohyla", # 17th
			iGlobal,
			"Andrii Sheptytsky", # 20th
			"fKuksha Odeskyy", # 20th
		),
		iGreatArtist : (
			"Boyan", # 11th
			"Ilarion", # 11th
			"Alipiy Pecherskyy", # 12th
			iRenaissance,
			"Ivan Rutkovych", # 17th
			"Anton Losenko", # 18th
			"Ivan Kotliarevsky", # 18th
			iIndustrial,
			"Taras Shevchenko", # 19th
			"Ivan Franko", # 19th
			"Marko Kropyvnytsky", # 19th
			iGlobal,
			"fLesia Ukrainka", # 20th
			"Mykola Leontovych", # 20th
			"Oleksandr Dovzhenko", # 20th
			"Volodymyr Sosiura", # 20th
			"Vasyl Stus", # 20th
		),
		iGreatScientist : (
			"Kyrylo", # 10th
			"Mefodiy", # 10th
			"Nestor Litopysets", # 11th
			iRenaissance,
			"Ivan Fedorov", # 16th
			"Hryhorii Skovoroda", # 18th
			iIndustrial,
			"Ivan Pulyuy", # 19th
			"Illya Mechnykov", # 19th
			iGlobal,
			"Volodymyr Vernadsky", # 20th
			"Mykola Amosov", # 20th
		),
		iGreatMerchant : (
			"Sadko", # legendary
			iRenaissance,
			"Kostiantyn Ostrovsky", # 16th
			"Fedir Symyrenko", # 18th
			iIndustrial,
			"Mykola Tereshchenko", # 19th
			"Bohdan Hanenko", # 19th
			"Varvara Hanenko", # 19th
			iGlobal,
			"Bohdan Havrylyshyn", # 20th
		),
		iGreatEngineer : (
			"Petro Milonih", # 12th
			"Oleksa", # 13th
			iRenaissance,
			"Ivan Hryhorovych-Barsky", # 18th
			iIndustrial,
			"Volodymyr Shukhov", # 19th
			"Vladyslav Horodetsky", # 19th
			iGlobal,
			"Serhii Koroliov", # 20th
			"Ihor Sikorsky", # 20th
			"Yevhen Paton", # 20th
			"Borys Paton", # 20th
			"Oleh Antonov", # 20th
			"Oleksandr Ivchenko", # 20th
		),
		iGreatStatesman : (
			"Volodymyr Sviatoslavych", # 11th	
			"Rurik", # 9th
			"Volodymyr Monomakh", # 12th
			"Danylo Halytskyy", # 13th
			iRenaissance,
			"Petro Sahaydachnyy", # 16th
			"Bohdan Khmelnytskyy", # 17th
			"Pylyp Orlyk", # 18th
			iGlobal,
			"Mykhailo Hrushevskyi", # 20th
			"Pavlo Skoropadskyy", # 20th
			"V'yacheslav Chornovil", # 20th
		),
		iGreatGeneral : (
			"Oleh Vishchyy", # 10th
			"Svyatoslav Ihorovych", # 10th
			"Sveneld", # 10th
			"Ihor Svyatoslavych", # 12th
			"Oleksandr Nevskyy", # 13th
			"Evpaty Kolovrat", # 13th
			iRenaissance,
			"Dmytro Vyshnevetskyy", # 16th
			"Ivan Sirko", # 17th
			"Petro Kalnyshevskyy", # 18th
			iIndustrial,
			"Ivan Paskevych", # 19th
			iGlobal,
			"Pavlo Skoropadskyy", # 20th
			"Symon Petlyura", # 20th
		),
		iGreatSpy : (
			"fRoksolana", # 16th
			"Ivan Mazepa", # 18th
			"Oleksa Dovbush", # 18th
			iGlobal,
			"Nestor Makhno", # 20th
		),
	},
	iVietnam : {
		iGreatProphet : (
			u"Tù Dao Hanh", # 11th
			u"Giác Hài", # 11th
			u"fDiêu Nhân", # 11th
			u"Tuê Trung", # 13th
			u"Lê Quát", # 14th
			iRenaissance,
			u"Nguyên Bình Khiêm", # 16th
			iGlobal,
			u"Ngô Van Chiêu", # 20th
			u"Lê Van Trung", # 20th
			u"Huynh Phú Sô", # 20th
			u"Thích Nhât Hanh", # 20th
			"fChing Hai", # 20th
		),
		iGreatArtist : (
			u"Khuông Viêt", # 10th
			"Dang Dung", # 14th
			iRenaissance,
			u"fDoàn Thi Diem", # 18th
			u"Nguyên Du", # 18th
			iIndustrial,
			u"fHó Xuân Huong", # 18-19th
			u"Nguyên Công Trú", # 19th
			u"Nguyên Thi Bích", # 19th
			u"fNguyên Khuyên", # 19th
			iGlobal,
			u"Nguyên Phan Chánh", # 20th
		),
		iGreatScientist : (
			u"Lê Van Huu", # 13th
			"Chu Van An", # 14th
			"Mac Dinh Chi", # 14th
			u"Ngô Si Liên", # 15th
			iRenaissance,
			u"fNguyên Thi Duê", # 16th
			u"Lê Quý Dôn", # 18th
			iGlobal,
			u"Ngô Bao Châu", # 20th
		),
		iGreatMerchant : (
			u"Vo Van Kiêt", # 20th
		),
		iGreatEngineer : (
			u"Nguyên An", # 15th
			u"Hô Nguyên Trùng", # 15th
			iGlobal,
			u"Trân Dai Nghia", # 20th
			u"André Truong Trong Thi", # 20th
		),
		iGreatStatesman : (
			u"Lý Dao Thành", # 11th
			"fY Lan", # 11th
			u"Lý Nhân Tông", # 11th
			u"Nguyên Trãi", # 15th
			iGlobal,
			u"Hô Chi Minh", # 20th
			u"Nguyên Van Linh", # 20th
			u"Lê Ðúc Tho", # 20th
		),
		iGreatGeneral : (
			u"Ngô Quyên", # 10th
			u"Lý Thuòng Kiêt", # 11th
			u"Trân Hung Dao", # 13th
			u"Trân Thánh Tông", # 13th
			u"Trân Nhán Tông", # 13th
			iRenaissance,
			u"fBùi Thi Xuân", # 18th
			"Gia Long", # 18th
			"Quang Trung", # 18th
			iIndustrial,
			u"Phan Dình Phùng", # 19th
			iGlobal,
			u"Vo Nguyên Giáp", # 20th
			u"Cao Van Viên", # 20th
		),
		iGreatSpy : (
			u"Pham Ngoc Thào", # 20th
			u"Pham Xuân Ân", # 20th
		),
	},
	iSwahili : {
		iGreatProphet : (
			"Mtswa Mwindza", # 7th
			"Ahmed Bin Abdulrahman Bin Uthman", # 10th or 11th Somali
			"Sheikh Hussein", # 13th Somali
			"Shehe Mvita", # 14th
			iIndustrial,
			"Maalim Mtondo", # 19th
			"Uways al-Barawi", # 19th Somali
			"fDada Masiti", # 19th
			iGlobal,
			"Kinjikitile Ngwale", # 20th
			"Laurean Rugambwa", # 20th
		),
		iGreatArtist : (
			"Fumo Liyongo", # 9-13th
			iRenaissance,
			"Bwana Mwengo wa Athman", # 18th
			iIndustrial,
			"fMwana Kupona", # 19th
			iGlobal,
			"Shaaban bin Robert", # 20th
			"Muhammed Said Abdulla", # 20th
			"Michael Enoch", # 20th
			"Bi Kidude", # 20th
			iDigital,
			"Abdulrazak Gurnah", # 21st
		),
		iGreatScientist : (
			"Fakhr al-Din al-Zayla'i", # 14th Somali
			iRenaissance,
			"Hassan al-Jabarti", # 18th Somali
			iIndustrial,
			"Shaykh Sufi", # 19th Somali
			iGlobal,
			"fAdelaida Kleti Semesi", # 20th
			"fWangari Maathai", # 20th
		),
		iGreatMerchant : (
			"Mohammed wa Joka", # legendary
			"Zhengjiani", # 11th
			"Dawud ibn Suleiman", # 12th
			"Sa'iid min Maqadishu", # 14th Somali
			"Mussa bin Bique", # 15th
			iIndustrial,
			"Sharmarke Ali Saleh", # 18-19th Somali
			"Tippu Tip", # 19th
			iGlobal,
			"Jayantilal Keshavji Chande", # 20th
			"Ali Mufuruki", # 20th
		),
		iGreatEngineer : (
			"Abu Bakr Fakr ad-Din", # 10th Somali
			"Al-Hasan ibn Sulaiman", # 14th
			"Suleiman ibn Muhammad", # 15th
			iRenaissance,
			"Fumo Madi ibn Abi Bakr", # 18th
		),
		iGreatStatesman : (
			"Ali ibn al-Hassan Shirazi", # 10th
			"Ali ibn Dawud", # 11th
			"Badlay ibn Sa'ad ad-Din", # 15th Somali
			iRenaissance,
			"Ahmad ibn Ibrahim al-Ghazi", # 16th Somali
			"Yusuf Mahamud Ibrahim", # 18th Somali
			iIndustrial,
			"Mohammed Abdullah Hassan", # 19th Somali
			iGlobal,
			"Abeid Karume", # 20th
			"Ahmed Abdallah Abderemane", # 20th
			"Julius Nyerere", # 20th
		),
		iGreatGeneral : (
			"Rubiya", # mythological
			"fAbanoye", # mythological
			"Al-Hassan ibn Talut", # 13th
			"Matan ibn Uthman Al Somali", # 15th Somali
			iRenaissance,
			"Ahmed Girri Bin Hussein Al Somali", # 16th Somali
			"Caaqil Dheryodhoobe", # 17th Somali
			"fFatuma binti Yusuf al-Alawi", # 18th
			iGlobal,
			"Samora Machel", # 20th
			"Mohammed Siad Barre", # 20th
		),
		iGreatSpy : (
			"Suleiman ibn Suleiman", # 12-13th
			"Daudi Mringwari", # 14-17th
			"Emir Muhammad Kiwabi", # 15th
		),
	},
	iPoland : {
		iGreatProphet : (
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
		),
		iGreatArtist : (
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
		),
		iGreatScientist : (
			"Witelon", # 13th
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
			"Jan Czochralski", # 20th
			"Alfred Tarski", # 20th
			u"Józef Rotblat", # 20th
		),
		iGreatMerchant : (
			"Konstanty Korniakt", # 16th
			"Antoni Protazy Potocki", # 18th
			iIndustrial,
			"Henryk Lubienski", # 19th
			"Leopold Kronenberg", # 19th
			"Franciszek Ksawery Branicki", # 19th"
			iGlobal,
			"Maksymilian Faktorowicz", # 20th
			"Jan Kulczyk", # 20th
		),
		iGreatEngineer : (
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
		),
		iGreatStatesman : (
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
		),
		iGreatGeneral : (
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
		),
		iGreatSpy : (
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
		),
	},
	iPortugal : {
		iGreatProphet : (
			u"António de Lisboa", # 13th
			u"fIsabel de Aragão", # 14th
			iRenaissance,
			u"João de Deus", # 16th
			u"João de Brito", # 17th
			iIndustrial, 
			"fRita Lopes de Almeida", # 19th
			iGlobal, 
			"Agostinho da Silva", # 20th
		),
		iGreatArtist : (
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
		),
		iGreatScientist : (
			"Garcia de Orta", # 16th
			"Pedro Nunes", # 16th
			"Amato Lusitano", # 16th
			"Jacob de Castro Sarmento", # 18th
			iGlobal,
			"Froilano de Mello", # 20th
			"Abel Salazar", # 20th
			u"António Egas Moniz", # 20th
		),
		iGreatMerchant : (
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
		),
		iGreatEngineer : (
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
		),
		iGreatStatesman : (
			"Henrique de Avis", # 15th
			iRenaissance,
			u"Tristão da Cunha", # 16th
			u"João o Restaurador", # 17th
			u"fLuisa de Guzmán", # 17th
			u"Alexandre de Gusmão", # 18th
			u"Sebastião José de Carvalho e Melo", # 18th
			iIndustrial,
			"Mouzinho da Silveira", # 19th
			u"António Luís de Seabra", # 19th
			iGlobal,
			"Afonso Costa", # 20th
			u"António de Oliveria Salazar", # 20th
			u"António Guterres", # 20th
		),
		iGreatGeneral : (
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
		),
		iGreatSpy : (
			"Roderigo Lopez", # 16th
			iGlobal,
			u"Agostinho Lourenço", # 20th
		),
	},
	iInca : {
		iGreatProphet : (
			"Yahuar Huacac", # 14th
			"fAsarpay", # 16th
		),
		iGreatArtist : (
			"Viracocha", # legendary
			"Ninan Cuyochi", # 16th
			"fPalla Chimpu Ocllo", # 16th
		),
		iGreatScientist : (
			"Sinchi Roca", # 12th
			"Mayta Qhapaq Inka", # 13th
			"Manqu Qhapaq", # 13th
			"Inka Roq'a", # 14th
			"Waskar Inka", # 16th
			"Titu Cusi", # 16th
		),
		iGreatMerchant : (
			"Tupaq Inka Yupanki", # 15th
			"Felipillo", # 16th
		),
		iGreatEngineer : (
			"Qhapaq Yunpanki Inka", # 14th
			"Sayri Tupaq Inka", # 16th
		),
		iGreatStatesman : (
			u"Mayta Cápac", # 14th
			iRenaissance,
			"Manco Inca Yupanqui", # 16th
			"fMama Huaco", # 16th
			u"Tápac Amaru", # 18th
		),
		iGreatGeneral : (
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
		),
	},
	iItaly : {
		iGreatProphet : (
			"Alberto Avogadro", # 12th
			"Bonaventura da Bagnoregio", # 13th
			"Tommaso d'Aquino", # 13th
			"Francesco d'Assisi", # 13th
			"fGuglielma", # 13th
			"fAngela da Foligno", # 13th
			"fChiara d'Assisi", # 13th
			"Pietro Angelerio", # 13th
			"fCaterina Benincasa", # 14th
			iRenaissance,
			"Giuliano della Rovere", # 15th
			"Giovanni da Capestrano", # 15th
			"fAngela Merici", # 16th
			"Camillo Borghese", # 16th
			"Giulio de' Medici", # 16th
			"Carlo Borromeo", # 16th
			"Matteo Ricci", # 16th
			"Gerolamo Emiliani", # 16th
			"Roberto Bellarmino", # 16th
			"Camillo de Lellis", # 16th
			"fAngela Merici", # 16th
			"Prospero Lorenzo Lambertini", # 18th
			"Alfonso Maria de' Liguori", # 18th
			iIndustrial,
			"Giovanni Maria Mastai-Ferretti", # 19th
			"Giovanni Bosco", # 19th
			"fVincenza Gerosa", # 19th
			iGlobal,
			"Angelo Giuseppe Roncalli", # 20th
			"Pio da Pietrelcina", # 20th
			"Giovanni Battista Enrico Antonio Maria Montini", # 20th
		),
		iGreatArtist : (
			"Dante Alighieri", # 13th
			"Giotto di Bondone", # 14th
			"Giovanni Boccaccio", # 14th
			"Donatello", # 15th
			iRenaissance,
			"Sandro Botticelli", # 15th
			"Michelangelo Buonarroti", # 16th
			"Raffaello Sanzio", # 16th
			"Giovanni Pierluigi da Palestrina", # 16th
			"fSofonisba Anguissola", # 16th
			"Michelangelo Merisi da Caravaggio", # 16th
			"Tiziano Vecellio", # 16th
			"Claudio Monteverdi", # 17th
			"fArtemisia Gentileschi", # 17th
			"Antonio Vivaldi", # 18th
			iIndustrial,
			"Alessandro Manzoni", # 19th
			"Giuseppe Verdi", # 19th
			"Giacomo Puccini", # 19th
			"Vincenzo Bellini", # 19th
			"Francesco Hayez", # 19th
			iGlobal,
			"Umberto Boccioni", # 20th
			"fGrazia Deledda", # 20th
			"Federico Fellini", # 20th
			"Giuseppe Ungaretti", # 20th
			u"Gian Maria Volontè", # Contest Reward
		),
		iGreatScientist : (
			"fTrotula di Salerno", # 12th
			"Tommaso d'Aquino", # 13th
			"Francesco Petrarca", # 14th
			iRenaissance,
			"Pico della Mirandola", # 15th
			"Leon Battista Alberti", # 15th
			"Giordano Bruno", # 16th
			"Galileo Galilei", # 16th
			"Gabriele Falloppio", # 16th
			"fElena Cornaro Piscopia", # 17th
			"Evangelisto Torricelli", # 17th
			"Luigi Galvani", # 18th
			"Alessandro Volta", # 18th
			"fMaria Gaetana Agnesi", # 18th
			"Giovanni Battista Venturi", # 18th
			iIndustrial,
			"Leonardo Ximenes", # 18th
			"Amedeo Avogadro", # 19th
			"Camillo Golgi", # 19th
			"Giuseppe Mercalli", # 19th
			"Ulisse Dini", # 19th
			iGlobal,
			"fMaria Montessori", # 20th
			"Enrico Fermi", # 20th
			"fRita Levi-Montalcini", # 20th
			"Giulio Natta", # 20th
		),
		iGreatMerchant : (
			"Domini Guardato", # 12th
			"Marco Polo", # 13th
			"Simone de' Bardi", # 13th
			"Giovanni de' Medici", # 14th
			"Donato Peruzzi", # 14th
			"Ciriaco de Ancona", # 15th
			iRenaissance,
			"Giovanni Caboto", # 15th
			"Amerigo Vespucci", # 15th
			"Paladino Gondola", # 15th
			"fTullia d'Aragona", # 16th
			"Pietro Verri", # 18th
			"Alessandro Malaspina", # 18th
			iIndustrial,
			"Giovanni Agnelli", # 19th
			iGlobal,
			"Enzo Ferrari", # 20th
			"Gianni Versace", # 20th
			"Enrico Mattei", # 20th
			"Franco Modigliani", # 20th
			"Adriano Olivetti", # 20th
			"Ferruccio Lamborghini", # 20th
			"Pietro Ferrero", # 20th
		),
		iGreatEngineer : (
			"Giovanni Pisano", # 13th
			"Andrea Pisano", # 14th
			"Taccola", # 15th
			"Filippo Brunelleschi", # 15th
			"Giovanni Fontana", # 15th
			iRenaissance,
			"Leon Battista Alberti", # 15th
			"Leonardo da Vinci", # 15th
			"Donato Bramante", # 15th
			"Andrea Palladio", # 16th
			"Giorgio Vasari", # 16th
			u"Niccolò Fontana Tartaglia", # 16th
			"Bernardo Buontalenti", # 16th
			"Gian Lorenzo Bernini", # 17th
			"Francesco Borromini", # 17th
			iIndustrial, 
			"Luigi Vanvitelli", # 18th
			"Alois Negrelli", # 19th
			"Antonio Meucci", # 19th
			iGlobal,
			"Guglielmo Marconi", # 20th
			"Giovanni Battista Caproni", # 20th
			"Angiolo Mazzoni", # 20th
			"Mario Tchou", # 20th
			"Nicola Materazzi", # 20th
			"Gabriele Trovato", # 20th
		),
		iGreatStatesman : (
			"Giovanni Villani", # 13th
			"Guglielmo Boccanegra", # 13th
			"Gian Galeazzo Visconti", # 14th
			iRenaissance,
			"fLucrezia Borgia", # 15th
			u"Niccolò Machiavelli", # 15th
			"Ludovico Sforza", # 15th
			"Leonardo Loredan", # 15th
			"Lorenzo de' Medici", # 15th
			"fIsabella d'Este", # 16th
			"Francesco Guicciardini", # 16th
			"Carlo Emanuele di Savoia", # 16th
			"Giambattista Vico", # 18th
			"Cesare Beccaria", # 18th
			"Pasquale Paoli", # 18th
			iIndustrial,
			"Giuseppe Garibaldi", # 19th
			"Giuseppe Mazzini", # 19th
			"Francesco Crispi", # 19th
			"Benedetto Croce", # 20th
			iGlobal,
			"Antonio Gramsci", # 20th
			"Alcide de Gasperi", # 20th
		),
		iGreatGeneral : (
			"fMatilde di Canossa", # 11th
			"Guglielmo Embriaco", # 11th
			"Guido da Landriano", # 12th
			"Ruggero d'Altavilla", # 12th
			"Enrico Dandolo", # 13th
			"Simone Boccanegra", # 14th
			"Francesco Sforza", # 15th
			iRenaissance, 
			"Cesare Borgia", # 15th
			"Bartolomeo Colleoni", # 15th
			"Federico da Montefeltro", # 15th
			"Andrea Doria", # 16th
			"Sebastiano Venier", # 16th
			"Alessandro Farnese", # 16th
			iIndustrial,
			"Alessandro Ferrero La Marmora", # 19th
			"Giuseppe Garibaldi", # 19th
			iGlobal,
			"Rodolfo Graziani", # 20th
			"Giovanni Messe", # 20th
		),
		iGreatSpy : (
			"Andrea Gritti", # 15th
			"Petros Lantzas", # 16th
			"fGiulia Tofana", # 17th
			"Gaspar Graziani", # 17th
			"Giacomo Casanova", # 18th
			iGlobal,
			"fLuisa Zeni", # 20th
			"Maurizio Giglio", # 20th
			"Rodolfo Siviero", # 20th
		),
	},
	iMongols : {
		iGreatProphet : (
			"Qiu Chuji", # 12th (also Chinese)
			"Berke", # 13th
			u"Özbeg", # 13th
			"Adud al-Din al-Iji", # 13th
			u"Drogön Chögyal Phagpa", # 13th
			iRenaissance,
			"Zanabazar", # 17th
			"Zaya Pandita", # 17th
			iGlobal,
			"Bogd Khan", # 20th
		),
		iGreatArtist : (
			"Huang Gongwang", # 13th (also Chinese)
			"Zhao Mengfu", # 13th
			"fGuan Daosheng", # 13th
			"Guan Hanqing", # 13th
			"Abu Sulayman Banakati", # 13th
			"Saadi Shirazi", # 13th
			u"Tugh Temür", # 14th
			iIndustrial, 
			"Dulduityn Danzanravjaa", # 19th
			iGlobal,
			"Marzan Sharav", # 20th
			"Byambyn Rinchen", # 20th
			"fSiqin Gaowa", # 20th
		),
		iGreatScientist : (
			"Isa Khelmerchi", # 13th
			"Nasir al-Din al-Tusi", # 13th (also Persian)
			"Mu'ayyad al-Din al-Urdi", # 13th
			"Jamal ad-Din Bukhari", # 13th
			"Guo Shoujing", # 13th
			"fZhu Shijie", # 13th
			iRenaissance,
			"Minggatu", # 18th
			iGlobal, 
			"Jamsrangiin Tseveen", # 20th
		),
		iGreatMerchant : (
			"Mahmud Yalavach", # 13th
			"Mengu Timur", # 13th
			"Gaykhatu", # 13th
			"Qawsun", # 13th
			"Bolad", # 13th
			"Pu Shougeng", # 13th
			"Sa'ad al-Dawla", # 13th
			"Wang Dayuan", # 14th
			iRenaissance,
			"Altan", # 16th
		),
		iGreatEngineer : (
			"Guillaume Boucher", # 13th
			"Liu Bingzhong", # 13th
			"Zhang Wenqian", # 13th
			"Araniko", # 13th
			"Ismail", # 14th
			"Wang Zhen", # 14th
			iGlobal,
			"Li Siguang", # 20th
		),
		iGreatStatesman : (
			"fSorghaghtani Beki", # 13th
			"Batu Khan", # 13th
			"Urtu Saqal", # 13th
			"fOrghana", # 13th
			"Ghazan", # 13th
			u"Temür Khan", # 13th
			"Toqto'a", # 14th
			"Dayan Khan", # 15th
			iIndustrial,
			"Balingiin Tserendorj", # 19th
			iGlobal, 
			u"Damdin Sükhbaatar", # 20th
			"Tsakhiagiin Elbegdorj", # 20th
		),
		iGreatGeneral : (
			"Toghril", # 12th
			"Subutai", # 13th
			u"Ögodei", # 13th
			"Chagatai", # 13th
			"Tolui", # 13th
			u"Möngke", # 13th
			"Hulagu", # 13th
			"Bayan", # 13th
			"fKhutulun", # 13th
			u"Köke Temür", # 14th
			"Tokhtamysh", # 14th
			"Esen Taishi", # 15th
			"fMandukhai", # 15th
			iRenaissance,
			"fAnu Qatun", # 17th
			iGlobal, 
			u"Damdin Sükhbaatar", # 20th
		),
	},
	iAztecs : {
		iGreatProphet : (
			"Mexitli" # legendary
			"Tenoch", # 14th
			"Tlacateotl", # 15th
			"fPapantzin", # 15th
			"Ixtlilxochitl", # 15th
			"fYacotzin", # 16th
		),
		iGreatArtist : (
			"Nezahualcoyotl", # 15th
			"Cuacuauhtzin", # 15th
			"Aquiauhtzin", # 15th
			"fMacuilxochitzin", # 15th
			"Xayacamach", # 15th
			"Ayocuan Cuetzpaltzin", # 15th
			"Quecholcohuatl", # 16th
		),
		iGreatScientist : (
			"Nezahualcoyotl", # 15th
			"Axayacatl", # 15th
			"Ixtlilxochitl", # 16th
			"Coanacochtzin", # 16th
		),
		iGreatMerchant : (
			"Cuauhtemoc", # 16th
			"Tlacotzin", # 16th
			"fTecuichpoch Ixcaxochitzin", # 16th
		),
		iGreatEngineer : (
			"Itzcoatl", # 15th
			"Tlacaelel", # 15th
			"Nezahualcoyotl", # 15th
			"Moquihuix", # 15th
		),
		iGreatStatesman : (
			"Acamapichtli", # 14th
			"Quaquapitzahuac", # 14th
			"Nezahualcoyotl", # 15th
			"fAtotoztli", # 15th
			"Tezozomoctli", # 15th
			"Nezahualpilli", # 15th
		),
		iGreatGeneral : (
			"Tezozomoc", # 14th
			"Ahuitzotl", # 15th
			"Itzcoatl", # 15th
			"Maxtla", # 15th
			"Huitzilhuitl", # 15th
			"Qualpopoca", # 15th
		),
	},
	iMughals : {
		iGreatProphet : (
			"Guru Ram Das", # 16th
			"Guru Arjan", # 16th
			"Hiravijaya ji", # 16th
			"Shah Abdul Latif Bhittai", # 18th
			"Bulleh Shah", # 18th
			iIndustrial,
			"Mirza Ghulam Ahmad", # 19th
		),
		iGreatArtist : (
			"Amir Khusrow Dehlavi", # 13th
			iRenaissance,
			"Basawan", # 16th
			"fShahzadi Gulbadan Begum", # 16th
			"Abu al-Faiz ibn Mubarak", # 16th
			"Abd al-Samad", # 16th
			"Bishandas", # 17th
			"Abu'l-Hasan", # 17th
			"Ustad Mansur", # 17th
			iIndustrial,
			"Ghulam Murtaza Khan", # 19th
			"Ghulam Ali Khan", # 19th
			iGlobal,
			"Muhammad Iqbal", # 20th
		),
		iGreatScientist : (
			"Ali Kashmiri ibn Luqman", # 16th
			"Abu al-Faiz ibn Mubarak", # 16th
			"Abd-ul-Qadir Bada'uni", # 16th
			"Muhammad Salih Tahtawi", # 17th
			"Sawai Jai Singh", # 18th
			iIndustrial,
			"Khwaja Nizam-ud-Din Ahmad", # 19th
			iGlobal,
			"Abdus Salam", # 20th
		),
		iGreatMerchant : (
			"Raja Todar Mal", # 16th
			"Virji Vora", # 17th
			"Mir Jumla", # 17th
			"Yahya Saleh", # 16th
			"Khan Alam", # 18th
			iGlobal,
			"Mian Muhammad Mansha", # 20th
		),
		iGreatEngineer : (
			"Fathullah Shirazi", # 16th
			"Ustad Ahmad Lahauri", # 17th
			"Muhammad Saleh Thattvi", # 17th
			iGlobal,
			"Abdur Rahman Hye", # 20th
			"Abdul Qadeer Khan", # 20th
			"Munir Ahmad Khan", # 20th
			"fYasmeen Lari", # 20th
		),
		iGreatStatesman : (
			"fRazia Sultana", # 13th
			"Ziauddin Barani", # 14th
			iRenaissance,
			"Raja Birbal", # 16th
			"fMaham Anga", # 16th
			"Babur", # 16th
			"Abu'l-Fazl ibn Muhammad", # 16th
			"Shaista Khan", # 17th
			"I'tisam-ud-Din", # 18th
			iGlobal,
			"Muhammad Ali Jinnah", # 20th
			"Choudhry Ali", # 20th
		),
		iGreatGeneral : (
			"Zahir-ud-din Muhammad Babur", # 15th
			"Mir Baqi", # 15th
			"Sher Shah Suri", # 16th
			"Bayram Khan", # 16th
			"Abul Muzaffar Aurangzeb", # 17th
			"Abudullah Khan Barha", # 18th
			"Ali Vardi Khan", # 18th
			iIndustrial,
			"fBegum Hazrat Mahal", # 19th
		),
		iGreatSpy : (
			"Hamid Gul", # 20th
		),
	},
	iRussia : {
		iGreatProphet : (
			"Sergiy Radonezhsky", # 14th
			"Paisiy Yaroslavov", # 15th
			iRenaissance,
			"Silvestr", # 16th
			"Nikon", # 17th
			"Feofan Prokopovich", # 18th
			"Seraphim Sarovsky", # 18th
			iIndustrial,
			"fHelena Blavatsky", # 19th
			"Grigori Rasputin", # 19th
			"Nikolai Rerikh", # 19th
			"Ivan Ilyich Sergiyev", # 19th
			iGlobal,
			"Nikolai Berdyaev", # 20th
			"Georges Florovsky", # 20th
			"Alexei Losev", # 20th
		),
		iGreatArtist : (
			"Feofan Grek", # 14th
			"Andrei Rublev", # 15th
			iRenaissance,
			"Antiokh Kantemir", # 18th
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
			"Igor Stravinsky", # 20th
			"Boris Pasternak", # 20th
			"Sergei Eisenstein", # 20th
		),
		iGreatScientist : (
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
			"Ivan Pavlov", # 20th
			"Lev Landau", # 20th
			"Pyotr Kapitsa", # 20th
		),
		iGreatMerchant : (
			"Afanasiy Nikitin", # 15th
			iRenaissance,
			"Anikey Stroganov", # 16th
			"Akinfiy Nikitich Demidov", # 17th
			"Vitus Bering", # 18th
			"Grigory Shelikhov", # 18th
			"Pavel Lebedev-Lastochkin", # 18th
			iIndustrial,
			"Ivan Kruzenshtern", # 19th
			"Nikolai Chukmaldin", # 19th
			"Karl Faberzhe", # 19th
			iGlobal,
			"Nikolai Kondratiev", # 20th
			"Leonid Kantorovich", # 20th
		),
		iGreatEngineer : (
			"Lazar Serb", # 15th
			iRenaissance,
			"Postnik Yakovlev", # 16th
			"Vasily Bazhenov", # 18th
			"Ivan Starov", # 18th
			"Nikolay Lvov", # 18th
			iIndustrial,
			"Vladimir Shukhov", # 19th
			"Sergey Prokudin-Gorsky", # 19th
			iGlobal,
			"Mikhail Kalashnikov", # 20th
			"Sergei Korolev", # 20th
			"Andrey Tupolev", # 20th
			"Lev Termen", # 20th
			"Vladimir Zvorykin", # 20th
			"Igor Sikorsky", # 20th
			"fValentina Tereshkova", # 20th
		),
		iGreatStatesman : (
			"Daniil Aleksandrovich", # 13th
			"fMarfa Posadnitsa", # 15th
			iRenaissance,
			"Vasily Tatishchev", # 18th
			"Nikita Panin", # 18th
			"fYekaterina Vorontsova-Dashkova", # 18th
			iIndustrial,
			"Mikhail Speransky", # 19th
			"Mikhail Bakunin", # 19th
			"Pyotr Stolypin", # 19th
			"Vladimir Lenin", # 19th
			iGlobal,
			"Leon Trotsky", # 20th
			"fAlexandra Kollontai", # 20th
			"Andrei Sakharov", # 20th
			"Mikhail Gorbachev", # 20th
			"Yegor Gaidar", # 20th
		),
		iGreatGeneral : (
			"Dmitry Donskoy", # 14th
			iRenaissance,
			"Mikhail Romanov", # 17th
			"Alexander Suvorov", # 18th
			"Grigory Potemkin", # 18th
			"Mikhail Kutuzov", # 18th
			iIndustrial,
			"Pavel Nakhimov", # 19th
			"Mikhail Skobelev", # 19th
			"fVasilisa Kozhina", # 19th
			"fNadezhda Durova", # 19th
			"Aleksei Brusilov", # 20th
			iGlobal,
			"Mikhail Tukhachevsky", # 20th
			"Georgy Zhukov", # 20th
			"Konstantin Rokossovsky", # 20th
			"Vasily Chuikov", # 20th
		),
		iGreatSpy : (
			"Fyodor Romodanovsky", # 17th
			iIndustrial,
			"Alexander Benkendorf", # 19th
			"Pyotr Rachkovsky", # 19th
			iGlobal,
			"Ilie Catarau", # 20th
			"Felix Dzerzhinsky", # 20th
			"Richard Sorge", # 20th
			"Ivan Serov", # 20th
			u"Sándor Goldberger", # 20th
			"Lavrentiy Beria", # 20th
			"Oleg Gordievsky", # 20th
		),
	},
	iSweden : {
		iGreatProphet : (
			"fBirgitta Birgersdotter", # 14th
			"fKatarina av Vadstena", # 14th
			iRenaissance,
			"Olaus Petri", # 16th
			"Mikael Agricola", # 16th Finnish
			"Johannes Campanius", # 17th
			"Emanuel Swedenborg", # 18th
			iIndustrial,
			u"Lars Levi Læstadius", # 19th Sámi
			"Carl Olof Rosenius", # 19th
			"Peter Weiselgren", # 19th
			iGlobal,
			u"Nathan Söderblom", # 20th
			"Lewi Pethrus", # 20th
			"fElizabeth Hesselblad", # 20th
			"fMargit Sahlin", # 20th
		),
		iGreatArtist : (
			u"Nils Håkansson", # 14th
			u"Albert Målare", # 15th
			iRenaissance,
			"Georg Stiernhielm", # 17th
			"Carl Michael Bellman", # 18th
			iIndustrial,
			"Johan Ludvig Runeberg", # 19th Finnish
			u"Elias Lönnrot", # 19th Finnish
			"fJenny Lind", # 19th
			"August Strindberg", # 19th
			"Anders Zorn", # 19th
			iGlobal,
			u"fSelma Lagerlöf", # 20th
			"fHilma af Klint", # 20th
			"fAstrid Lindgren", # 20th
			"Ingmar Bergman", # 20th
			"Erik Axel Karlfeldt", # 20th
			"fGreta Garbo", # 20th
			"Jean Sibelius", # 20th Finnish
			"fTove Jansson", # 20th Finnish
			u"Frans Eemil Sillanpää", # 20th Finnish
		),
		iGreatScientist : (
			"Nils Ragvaldsson", # 15th
			iRenaissance,
			"Olof Rudbeck", # 17th
			"Anders Celsius", # 18th
			u"Carl von Linné", # 18th
			"fEva Ekeblad", # 18th
			"Carl Wilhelm Scheele", # 18th
			iIndustrial,
			u"Jöns Jacob Berzelius", # 19th
			"Johannes Rydberg", # 19th
			u"Anders Ångström", # 19th
			"Svante Arrhenius", # 19th
			iGlobal,
			u"Hannes Alfvén", # 20th
			"Theodor Svedberg", # 20th
			"Ulf von Euler", # 20th
			"Lars Ahlfors", # 20th Finnish
			"Ragnar Granit", # 20th Finnish
		),
		iGreatMerchant : (
			"Bo Jonsson Grip", # 14th
			iRenaissance,
			u"Johan Björnsson Printz", # 17th
			"fChristina Piper", # 18th
			"Niclas Sahlgren", # 18th
			"Rutger Macklean", # 18th
			iIndustrial,
			u"Adolf Erik Nordenskiöld", # 19th Finnish
			"Sven Hedin", # 19th
			"fJohanna Petersson", # 19th
			"Lars Magnus Ericsson", # 19th
			u"André Oscar Wallenberg", # 19th
			iGlobal,
			"Ingvar Kamprad", # 20th
			"Ivar Kreuger", # 20th
			"Assar Gabrielsson", # 20th
			"Erling Persson", # 20th
			"Gunnar Myrdal", # 20th
			"Marcus Wallenberg Jr.", # 20th
		),
		iGreatEngineer : (
			"Englika", # 14th
			iRenaissance,
			"Nicodemus Tessin", # 17th
			"Erik Dahlbergh", # 17th
			"Christopher Polhem", # 18th
			iIndustrial,
			"Johan Ericsson", # 19th
			"Per Georg Scheutz", # 19th
			"Gustaf de Laval", # 19th
			"Carl Edvard Johansson", # 19th
			"Alfred Nobel", # 19th
			iGlobal,
			u"Gustaf Dalén", # 20th
			"Gunnar Asplund", # 20th
			"Carl Munters", # 20th
			"Nils Bohlin", # 20th
			"Alvar Aalto", # 20th Finnish
		),
		iGreatStatesman : (
			"Birger Jarl", # 13th
			u"Magnus Ladulås", # 13th
			"Sten Sture", # 15th
			iRenaissance,
			"Axel Oxenstierna", # 17th
			"fKristina", # 17th
			"Karl XI", # 17th
			"Peter Estenberg", # 18th
			"Arvid Horn", # 18th
			"Anders Chydenius", # 18th Finnish
			iIndustrial,
			"Gustaf Mauritz Armfelt", # 19th Finnish
			"Louis Gerhard De Geer", # 19th
			"Oscar II", # 19th
			"August Palm", # 19th
			iGlobal,
			"fElsa Laula Renberg", # 20th Sámi
			"Folke Bernadotte", # 20th
			u"Dag Hammarskjöld", # 20th
			"fAlva Myrdal", # 20th
			"Olof Palme", # 20th
		),
		iGreatGeneral : (
			"Tyrgils Knutsson", # 13th
			"Erik Magnusson", # 14th
			iRenaissance,
			"Gustav Vasa", # 16th
			"Gustaf Horn", # 17th Finnish
			"Lennart Torstensson", # 17th
			"Carl Gustaf Wrangel", # 17th
			u"Carl Gustaf Rehnskiöld", # 18th
			"Karl XII", # 18th
			"fIngela Gathenhielm", # 18th
			iIndustrial,
			"Karl XIV Johan", # 19th
			iGlobal,
			"Carl Gustaf Emil Mannerheim", # 20th Finnish
			"Adolf Ehrnrooth", # 20th Finnish
		),
		iGreatSpy : (
			"Engelbrekt Engelbrektsson", # 15th
			"fBrita Olovsdotter Tott", # 15th Swedish/Danish
			iRenaissance,
			"fAnna Maria Clodt", # 17th
			"fCharlotte Eckerman", # 18th
			u"fEva Löwen", # 18th
			"Jean Grossaint De la Roche-yon", # 18th
			iIndustrial,
			"Carl Johan Ingman", # 19th
			iGlobal,
			"Carlos Adlercreutz", # 20th
			u"Stig Wennerström", # 20th
			"Stig Berglig", # 20th
		),
	},
	iOttomans : {
		iGreatProphet : (
			"Sheikh Bedreddin", # 14th
			"Akshamsaddin", # 15th
			"Otman Baba", # 15th
			iRenaissance,
			"Ebussuud Effendi", # 16th
			"Sabbatai Zevi", # 17th
			"Yaakov Culi", # 18th
			iGlobal,
			"Bartholomeos", # 20th
			u"Fethullah Gülen", # 20th
			u"Mustafa Çagrici", # 20th
		),
		iGreatArtist : (
			"Yunus Emre", # 13th
			iRenaissance,
			u"Hayâlî", # 16th
			u"Fuzûlî", # 16th
			u"Gül Baba", # 16th
			u"Ahmet Nedîm Efendi", # 18th
			"Abdullah Buhari", # 18th
			iIndustrial,
			"Hamparsum Limonciyan", # 19th
			"Osman Hamdi Bey", # 19th
			"fFatma Aliye Topuz", # 19th
			iGlobal,
			"Mehmet Akif Ersoy", # 20th
			"fHalide Edib Adivar", # 20th
			u"Nâzim Hikmet Ran", # 20th
		),
		iGreatScientist : (
			"Qazi Zada", # 14th
			"Serafeddin Sabuncuoglu", # 15th
			u"Ali Kusçu", # 15th
			iRenaissance,
			u"Matrakçi Nasuh", # 16th
			u"Takiyüddin", # 16th
			u"Ibrahim Müteferrika", # 18th
			iIndustrial, 
			"Hasan Tahsini", # 19th
			iGlobal,
			"Cahit Arf", # 20th
			"Oktay Sinanoglu", # 20th
			u"Feza Gürsey", # 20th
			"Aziz Sancar", # 20th
		),
		iGreatMerchant : (
			"Piri Reis", # 16th
			"Seydi Ali Reis", # 16th
			"Michael Kantakouzenos Seytanoglu", # 16th
			"fEsther Handali", # 16th
			u"Evliya Çelebi", # 17th
			iIndustrial,
			"Ahmed Fethi", # 19th
			"Calouste Gulbenkian", # 19th
			iGlobal,
			"Hormuzd Rassam", # 20th
			"Nejat Eczacibashi", # 20th
			"Aydin Dogan", # 20th
		),
		iGreatEngineer : (
			"Orban", # 15th
			"Atik Sinan", # 15th
			iRenaissance,
			"Mimar Sinan", # 16th
			"Davud Aga", # 16th
			u"Takiyüddin", # 16th
			iIndustrial,
			"Ishak Efendi", # 19th
			"Garabet Amira Balyan", # 19th
			iGlobal,
			"Mimar Kemaleddin", # 20th
			u"Ekmel Özbay", # 20th
		),
		iGreatStatesman : (
			"Sheikh Edebali", # 13th
			iRenaissance,
			"Pargali Ibrahim", # 16th
			"fHurrem Sultan", # 16th
			"Sokollu Mehmet", # 16th
			u"Köprülü Mehmed", # 17th
			u"fKösem Sultan", # 17th
			iIndustrial,
			"Mustafa Resid", # 19th
			u"Abdülmecid", # 19th
			u"Mehmed Emin Âli", # 19th
			"Ahmed Cevdet", # 19th
			iGlobal,
			u"Ismet Inönü", # 20th
			u"Süleyman Demirel", # 20th
		),
		iGreatGeneral : (
			"Orhan", # 14th
			"Birinci Selim", # 15th
			iRenaissance,
			"Barbaros Hayreddin", # 16th
			"Turgut Reis", # 16th
			"Kara Mustafa", # 17th
			iIndustrial, 
			"Muhammad Ali", # 19th
			"Omar Latas", # 19th
			"Osman Nuri", # 19th
			iGlobal,
			u"Fevzi Çakmak", # 20th
			"fKara Fatma", # 20th
			"Ismail Enver", # 20th
		),
		iGreatSpy : (
			"Petar Ovcarevic", # 16th
			iGlobal,
			u"Süleyman Askerî", # 20th
			u"Mustafa Mümin Aksoy", # 20th
			"Ahmet Esat Tomruk", # 20th
			"fDespina Storch", # 20th
		),
	},
	iThailand : {
		iGreatProphet : (
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
		),
		iGreatArtist : (
			"Si Prat", # 17th
			"Thammathibet", # 18th
			iIndustrial,
			"Khrua In Khong", # 19th
			"Phra Phutthaloetla Naphalai", # 19th (Rama II)
			"Sunthorn Phu", # 19th
			iGlobal,
			"Pin Malakul", # 20th
		),
		iGreatScientist : (
			"Ramkhamhaeng", # 13th
			iIndustrial,
			"Dan Beach Bradley", # 19th
			"Damrong Rajanubhab", # 19th
			iGlobal,
			"Mahidol Adulyadej", # 20th
			"Phraya Anuman Rajadhon", # 20th
			"fKrisana Kraisintu", # 20th
			"Shaiwatna Kupratakul", # 20th
		),
		iGreatMerchant : (
			"Uthong", # 14th
			"Yamada Nagamasa", # 17th
			iIndustrial,
			"Low Kiok Chiang", # 19th
			iGlobal,
			"Puey Ungphakorn", # 20th
			"fLursakdi Sampatisiri", # 20th
		),
		iGreatEngineer : (
			"Chettathirat", # 16th
			"Tok Kayan", # 17th
			iGlobal,
			"Ravi Ravendro", # 20th (a.k.a. Karl Döhring)
			"Ercole Manfredi", # 20th
			"Purachatra Jayakara", # 20th
			"Punya Thitimajshima", # 20th
		),
		iGreatStatesman : (
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
		),
		iGreatGeneral : (
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
		),
		iGreatSpy : (
			"fThao Suranari", # 19th
		),
	},
	iCongo : {
		iGreatProphet : (
			"Nzinga a Nkuwu", # 15th
			"Kinu a Mvemba", # 16th
			"Ilunga Mbili", # 16th
			iRenaissance,
			"Nkanga a Lukeni a Nzenze a Ntumba", # 17th
			"fKimpa Vita", # 17th
		),
		iGreatMerchant : (
			"N'Gangue M'voumbe Niambi", # 17th
		),
		iGreatStatesman : (
			"Mwata Yamvo", # 16th
			"Ng'anga Bilonda", # 16th
			"Kalala Ilunga", # 17th
			"fNzinga", # 17th
			iGlobal,
			"Patrice Lumumba", # 20th
			"Joseph Kasa-Vubu", # 20th
		),
		iGreatGeneral : (
			"Lukeni lua Nimi", # 14th
			iRenaissance,
			"fNzinga", # 17th
			"Nusamu a Mvemba", # 18th
			"fKangala Kingwanda", # 18th
			iIndustrial,
			"Mwenda Msiri Ngelengwa Shitambi", # 19th
		),
	},
	iNetherlands : {
		iGreatProphet : (
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
		),
		iGreatArtist : (
			"Orlande de Lassus", # 16th
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
		),
		iGreatScientist : (
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
		),
		iGreatMerchant : (
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
			"Jan Tinbergen", # 20th
			"Freddy Heineken", # 20th
		),
		iGreatEngineer : (
			"Simon Stevin", # 16th
			"Cornelis Corneliszoon", # 16th
			"Hendrick de Keyser", # 16th
			"Cornelis Drebbel", # 17th
			"Jan Leeghwater", # 17th
			"Menno van Coehoorn", # 17th
			iIndustrial,
			"Adolphe Sax", # 19th
			"Cornelis Lely", # 19th
			"Hendrik Petrus Berlage", # 19th
			"Anthony Fokker", # 19th
			iGlobal,
			"Anton Philips", # 20th
			"Gerrit Rietveld", # 20th
		),
		iGreatStatesman : (
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
		),
		iGreatGeneral : (
			"Maurits van Nassau", # 16th
			"Piet Pieterszoon Hein", # 16th
			"Michiel de Ruyter", # 17th
			"Frederik Hendrik", # 17th
			"Cornelis Tromp", # 17th
			iIndustrial,
			"Joannes Benedictus van Heutsz", # 19th
			"Henri Winkelman", # 20th
		),
		iGreatSpy : (
			"fSophie Harmansdochter", # 16th
			"fEtta Palm d'Aelders", # 18th
			iIndustrial,
			"fJohanna Brandt", # 19th
			"Christiaan Snouck Hurgronje", # 19th
			iGlobal,
			"fMata Hari", # 20th
			"Dirk Klop", # 20th
			u"François van 't Sant", # 20th
		),
	},
	iGermany : {
		iGreatProphet : (
			"Moses Mendelssohn", # 18th
			"Friedrich Schleiermacher", # 18th
			"fAnne Catherine Emmerich", # 18th
			iIndustrial,
			"Friedrich Nietzsche", # 19th
			"Adolph Kolping", # 19th
			iGlobal,
			"Dietrich Bonhoeffer", # 20th
			"fEdith Stein", # 20th
			"Joseph Ratzinger", # 20th
		),
		iGreatArtist : (
			"Johann Sebastian Bach", # 18th
			"Carl Philipp Emanuel Bach", # 18th
			"Gotthold Ephraim Lessing", # 18th
			"Johann Wolfgang von Goethe", # 18th
			"Friedrich Schiller", # 18th
			iIndustrial,
			"Caspar David Friedrich", # 19th
			"Felix Mendelssohn", # 19th
			"fClara Schumann", # 19th
			"Richard Wagner", # 19th
			iGlobal,
			"Thomas Mann", # 20th
			"Hermann Hesse", # 20th
			"Paul Klee", # 20th
			"fLeni Riefenstahl", # 20th
			u"Günter Grass", # 20th
			"Leoreth", # 21st
		),
		iGreatScientist : (
			"Leonhard Euler", # 18th
			"Johann Heinrich Lambert", # 18th
			"fCaroline Herschel", # 18th
			iIndustrial,
			"Alexander von Humboldt", # 19th
			"Georg Wilhelm Friedrich Hegel", # 19th
			u"Carl Friedrich Gauß", # 19th
			"Ernst Haeckel", # 19th
			u"Wilhelm Röntgen", # 19th
			iGlobal,
			"Albert Einstein", # 20th
			"Werner Heisenberg", # 20th
			"fEmmy Noether", # 20th
			"Max Planck", # 20th
		),
		iGreatMerchant : (
			"Johann Philipp Graumann", # 18th
			"Johann Ernst Gotzkowsky", # 18th
			"Mayer Amschel Rothschild", # 18th
			iIndustrial,
			"Nathan Mayer Rothschild", # 19th
			u"Gerson von Bleichröder", # 19th
			"Marcus Goldman", # 19th
			iGlobal,
			"fMelitta Bentz", # 20th
			"Adolf Dassler", # 20th
			"Philip Rosenthal", # 20th
		),
		iGreatEngineer : (
			"Georg Wenzeslaus von Knobelsdorff", # 18th
			"Carl Gotthard Langhans", # 18th
			iIndustrial,
			"Alfred Krupp", # 19th
			"Werner von Siemens", # 19th
			"Nikolaus Otto", # 19th
			"Gottlieb Daimler", # 19th
			"Carl Benz", # 19th
			iGlobal,
			"Ferdinand Porsche", # 20th
			"August Horch", # 20th
			"Ludwig Mies van der Rohe", # 20th
			"Konrad Zuse", # 20th
			"Wernher von Braun", # 20th
		),
		iGreatStatesman : (
			"Jakob Friedrich von Bielfeld", # 18th
			"Immanuel Kant", # 18th
			"Heinrich Friedrich Karl vom Stein", # 18th
			iIndustrial,
			"Wilhelm von Humboldt", # 19th
			"Karl Marx", # 19th
			"Wilhelm Liebknecht", # 19th
			"Friedrich Ebert", # 19th
			"fRosa Luxemburg", # 19th
			iGlobal,
			"Konrad Adenauer", # 20th
			"fHannah Arendt", # 20th
			"Willy Brandt", # 20th
			"Helmut Kohl", # 20th
		),
		iGreatGeneral : (
			u"Gebhard Leberecht von Blücher", # 18th
			"Gerhard von Scharnhorst", # 18th
			iIndustrial,
			"Carl von Clausewitz", # 19th
			"Helmuth von Moltke", # 19th
			"Paul von Hindenburg", # 19th
			iGlobal,
			"Erich Ludendorff", # 20th
			"Erich von Manstein", # 20th
			"Erwin Rommel", # 20th
			"Heinz Guderian", # 20th
		),
		iGreatSpy : (
			u"Christian Andreas Käsebier", # 18th
			"Georg Klindworth", # 19th
			"Wilhelm Stieber", # 19th
			"fMaria de Victorica", # 19th
			iGlobal,
			u"fElsbeth Schragmüller", # 20th
			"Wilhelm Canaris", # 20th
			"Fritz Joubert Duquesne", # 20th
			"Klaus Fuchs", # 20th
			"Markus Wolf", # 20th
		),
	},
	iAmerica : {
		iGreatProphet : (
			"Joseph Smith", # 19th
			"fMary Baker Eddy", # 19th
			"fEllen G. White", # 19th
			"Charles Taze Russell", # 19th
			iGlobal,
			"Menachem Mendel Schneerson", # 20th
			"L. Ron Hubbard", # 20th
			"Billy Graham", # 20th
			"Malcolm Little", # 20th
		),
		iGreatArtist : (
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
		),
		iGreatScientist : (
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
		),
		iGreatMerchant : (
			"Stephen Girard", # 18th
			"Nathaniel Bowditch", # 18th
			iIndustrial,
			"Cornelius Vanderbilt", # 19th
			"Cyrus W. Field", # 19th
			"Andrew Carnegie", # 19th
			"John D. Rockefeller", # 19th
			"fHetty Green", # 19th
			"John Pierpont Morgan", # 19th
			iGlobal,
			"fHelena Rubinstein", # 20th
			"William Edward Boeing", # 20th
			"Walt Disney", # 20th
			"Ray Kroc", # 20th
			"Thomas Watson", # 20th
			"Sam Walton", # 20th
			"Bill Gates", # 20th
		),
		iGreatEngineer : (
			"Samuel Morse", # 19th
			"Charles Goodyear", # 19th
			"Thomas Edison", # 19th
			"Nikola Tesla", # 19th
			"Louis Sullivan", # 19th
			"Henry Ford", # 19th
			iGlobal,
			"Orville Wright", # 20th
			"Frank Lloyd Wright", # 20th
			"fLillian Moller Gilbreth", # 20th
			"Robert Moses", # 20th
			"Eero Saarinen", # 20th
			"fMargaret Hutchinson Rousseau", # 20th
			"fHedy Lamarr", # 20th
			"Frank Gehry", # 20th
		),
		iGreatStatesman : (
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
		),
		iGreatGeneral : (
			"Andrew Jackson", # 19th
			"Winfield Scott", # 19th
			"Ulysses S. Grant", # 19th
			"Robert E. Lee", # 19th
			iGlobal,
			"John J. Pershing", # 20th
			"Dwight D. Eisenhower", # 20th
			"George Patton", # 20th
			"Douglas MacArthur", # 20th
			"Matthew Ridgway", # 20th
			"Norman Schwarzkopf", # 20th
		),
		iGreatSpy : (
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
		),
	},
	iMexico : {
		iGreatProphet : (
			"Juan Diego", # 16th
			"Francisco Javier Clavijero", # 18th
			u"Cristóbal Magallanes Jara", # 19th
			iGlobal,
			u"Rafael Guízar Valencia", # 20th
			"Miguel Pro", # 20th
			"Samuel Ruiz", # 20th
			u"Javier Lozano Barragán", # 20th
		),
		iGreatArtist : (
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
		),
		iGreatScientist : (
			"Gabino Barreda", # 19th
			u"Lucas Alamán", # 19th
			iGlobal,
			"Manuel Sandoval Vallarta", # 20th
			"Ricardo Miledi", # 20th
			u"Mario José Molina", # 20th
			"Rodolfo Neri Vela", # 20th
		),
		iGreatMerchant : (
			u"Víctor Urquidi", # 20th
			u"Jerónimo Arango", # 20th
			"Carlos Slim", # 20th
			"Everardo Elizondo", # 20th
			u"Alberto Baillères", # 20th
			u"Emilio Azcárraga Jean", # 20th
		),
		iGreatEngineer : (
			u"José Villagrán García", # 20th
			u"Luis Barragán", # 20th
			"Juan O'Gorman", # 20th
			"Mario Pani", # 20th
			u"Pedro Ramírez Vázquez", # 20th
			"Bernardo Quintana Arrioja", # 20th
		),
		iGreatStatesman : (
			u"José María Pino Suárez", # 19th
			"Pascual Orozco", # 19th
			iGlobal,
			u"José Vasconcelos", # 20th
			"Octavio Paz", # 20th
			"fElvia Carrillo Puerto", # 20th
			"fRosario Castellanos", # 20th
			u"Alfonso García Robles", # 20th
			u"Gilberto Bosques Saldívar", # 20th
		),
		iGreatGeneral : (
			"Miguel Hidalgo", # 18th
			u"Agustín de Iturbide", # 19th
			u"fJosefa Ortiz de Domínguez", # 19th
			u"Porfirio Díaz", # 19th
			"Pancho Villa", # 19th
			"Emiliano Zapata Salazar", # 19th
		),
		iGreatSpy : (
			"fMargarita Ortega", # 19th
		),
	},
	iArgentina : {
		iGreatProphet : (
			"Gauchito Gil", # 19th
			iGlobal,
			"Enrique Angelelli", # 20th
			"Carlos Mugica", # 20th
			"Jorge Mario Bergoglio", # 20th
		),
		iGreatArtist : (
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
		),
		iGreatScientist : (
			"Francisco Moreno", # 19th
			"Florentino Ameghino", # 19th
			iGlobal,
			"Luis Federico Leloir", # 20th
			u"László Bíró", # 20th
			u"René Favaloro", # 20th
		),
		iGreatMerchant : (
			"Juan Las Heras", # 19th
			"Otto Bemberg", # 19th
			"Ernesto Tornquist", # 19th
			iGlobal,
			u"José Ber Gelbard", # 20th
			"Roberto Alemann", # 20th
			"Jorge Wehbe", # 20th
			"Aldo Ferrer", # 20th
			"Antonio Cafiero", # 20th
		),
		iGreatEngineer : (
			"Luis Huergo", # 19th
			"Jorge Newbery", # 19th
			iGlobal,
			"Amancio Williams", # 20th
			"Livio Dante Porta", # 20th
			"Clorindo Testa", # 20th
			u"César Pelli", # 20th
		),
		iGreatStatesman : (
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
		),
		iGreatGeneral : (
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
		),
		iGreatSpy : (
			"Emilio Eduardo Massera", # 20th
			"Guillermo Gaede", # 20th
		),
	},
	iColombia : {
		iGreatProphet : (
			"fLaura Montoya", # 20th
			u"Félix Restrepo Mejía", # 20th
			"Camilo Torres Restrepo", # 20th
			u"Alfonso López Trujillo", # 20th
			u"Julio Enrique Dávila", # 20th
			u"fMaría Luisa Piraquive", # 20th
			u"César Castellanos", # 20th
		),
		iGreatArtist : (
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
		),
		iGreatScientist : (
			u"José Jéronimo Triana", # 19th
			"Julio Garavito Armero", # 19th
			iGlobal,
			u"Rodolfo Llinás", # 20th
			"Jorge Reynolds Pombo", # 20th
		),
		iGreatMerchant : (
			"James Martin Eder", # 19th
			iGlobal,
			"Julio Mario Santo Domingo", # 20th
			u"Carlos Ardila Lülle", # 20th
			"Luis Carlos Sarmiento Angulo", # 20th
			"Pablo Escobar", # 20th
		),
		iGreatEngineer : (
			u"Carlos Albán", # 19th
			iGlobal, 
			u"Carlos Raúl Villanueva", # 20th
			"Rogelio Salmona", # 20th
		),
		iGreatStatesman : (
			u"Tomás Cipriano de Mosquera", # 19th
			u"Rafael Núñez", # 19th
			iGlobal,
			u"Jorge Eliécer Gaitán", # 20th
			u"Nicolás Gómez Dávila", # 20th
			u"Mario Lanserna Pinzón", # 20th
		),
		iGreatGeneral : (
			"fAntonia Santos", # 19th
			u"Antonio Nariño", # 19th
			"Francisco de Paula Santander", # 19th
		),
		iGreatSpy : (
			"fPolicarpa Salavarrieta", # 19th
			u"fManuela Sáenz", # 19th
		),
	},
	iBrazil : {
		iGreatProphet : (
			u"António Conselheiro", # 19th
			iGlobal,
			u"Hélder Câmara", # 20th
			u"fIrmã Dulce Pontes", # 20th
			"Chico Xavier", # 20th
			"Edir Macedo", # 20th
		),
		iGreatArtist : (
			"Aleijadinho", # 18th
			u"António Carlos Gomes", # 19th
			"Machado de Assis", # 19th
			iGlobal,
			"fTarsila do Amaral", # 20th
			"fCarmen Miranda", # 20th
			"Tom Jobim", # 20th
			"Romero Britto", # 20th
		),
		iGreatScientist : (
			"Oswaldo Cruz", # 19th
			"Carlos Chagas", # 19th
			iGlobal,
			"Alberto Santos-Dumont", # 20th
			"Urbano Ernesto Stumpf", # 20th
			u"Aziz Ab'Sáber", # 20th
			"Marcelo Gleiser", # 20th
		),
		iGreatMerchant : (
			"Roberto Marinho", # 20th
			"Jorge Lemann", # 20th
			"Eike Batista", # 20th
		),
		iGreatEngineer : (
			u"André Rebouças", # 19th
			iGlobal,
			u"Cândido Rondon", # 20th
			"Oscar Niemeyer", # 20th
			"Norberto Odebrecht", # 20th
		),
		iGreatStatesman : (
			u"José Bonifácio de Andrada", # 18th
			iIndustrial,
			"Rodrigo Augusto da Silva", # 19th
			u"José Paranhos", # 19th
			u"fIsabel Bragança", # 19th
			"Miguel Reale", # 19th
			iGlobal,
			"Roberto Mangabeira Unger", # 20th
		),
		iGreatGeneral : (
			u"Luís Alves de Lima e Silva", # 19th
			"Joaquim Marques Lisboa", # 19th
			u"fMaria Quitéria", # 19th
			iGlobal,
			u"João Baptista Mascarenhas de Morais", # 20th
			"Eurico Gaspar Dutra", # 20th
			"Artur da Costa e Silva", # 20th
		),
	},
	iCanada : {
		iGreatProphet : (
			"Ignace Bourget", # 19th
			u"André Bessette", # 20th
			iGlobal,
			"Lionel Groulx", # 20th
			"George C. Pidgeon", # 20th
			u"fRúhíyyih Khánum", # 20th
			"Marshall McLuhan", # 20th
		),
		iGreatArtist : (
			"Cornelius Krieghoff", # 19th
			u"Calixa Lavallée", # 19th
			"Tom Thomson", # 19th
			u"Émile Nelligan", # 19th
			iGlobal,
			"fLucy Maud Montgomery", # 20th
			"Lawren Harris", # 20th
			"fEmily Carr", # 20th
			"Jean-Paul Riopelle", # 20th
			"Neil Young", # 20th
			"fGabrielle Roy", # 20th
			"fAlice Munro", # 20th
		),
		iGreatScientist : (
			"John William Dawson", # 19th
			"fMaude Abbott", # 19th
			iGlobal,
			"Frederick Banting", # 20th
			"Norman Bethune", # 20th
			"Wilder Penfield", # 20th
			"Pierre Dansereau", # 20th
			"fShirley Tilghman", # 20th
			"David Suzuki", # 20th
		),
		iGreatMerchant : (
			"William McMaster", # 19th
			"Timothy Eaton", # 19th
			"Alphonse Desjardins", # 19th
			iGlobal,
			"fElizabeth Arden", # 20th
			"Max Aitken", # 20th
			"Ted Rogers", # 20th
			u"Guy Laliberté", # 20th
		),
		iGreatEngineer : (
			"Sandford Fleming", # 19th
			"William Cornelius Van Horne", # 19th
			"Alexander Graham Bell", # 19th
			"Reginald Fessenden", # 19th
			iGlobal,
			"Ernest Cormier", # 20th
			"Joseph-Armand Bombardier", # 20th
			"fElsie MacGill", # 20th
		),
		iGreatStatesman : (
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
		),
		iGreatGeneral : (
			"Arthur Currie", # 20th
			"Andrew McNaughton", # 20th
			"Billy Bishop", # 20th
			u"Roméo Dallaire", # 20th
		),
		iGreatSpy : (
			"William Stephenson", # 20th
			"Guy D'Artois", # 20th
			"Igor Gouzenko", # 20th
		),
	},
}


def setup():
	global dGreatPeople
	
	global tGreatPeople
	tGreatPeople = tuple(determineGreatPeopleNames(dGreatPeople.get(iCiv, {})) for iCiv in range(iNumCivs))
	
	global tOffsets
	tOffsets = tuple(calculateOffsets(dGreatPeople.get(iCiv, {})) for iCiv in range(iNumCivs))
	
	del dGreatPeople

			
def determineGreatPeopleNames(dCivGreatPeople):
	return tuple(determineTypeGreatPeopleNames(dCivGreatPeople.get(iType, [])) for iType in lTypes)

def determineTypeGreatPeopleNames(tEntries):
	return tuple(entry for entry in tEntries if entry not in range(iNumEras))

def calculateOffsets(dCivGreatPeople):
	return tuple(calculateTypeOffsets(dCivGreatPeople.get(iType, [])) for iType in lTypes)

def calculateTypeOffsets(tEntries):
	dOffsets = dict((entry, index) for index, entry in enumerate(tEntries) if entry in range(iNumEras))
	iCount = 0
	
	lOffsets = []
	for iEra in range(iNumEras):
		if iEra in dOffsets:
			iOffset = dOffsets[iEra] - iCount
			iCount += 1
		elif iEra == iAncient:
			iOffset = 0
		else:
			iOffset = lOffsets[-1]
		
		lOffsets.append(iOffset)
	
	return tuple(lOffsets)


setup()
