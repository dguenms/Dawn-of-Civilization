# Rhye's and Fall of Civilization - Barbarian units and cities

from CvPythonExtensions import *
import CvUtil
import PyHelpers	# LOQ
#import Popup
#import cPickle as pickle
import RFCUtils
import Consts as con
from StoredData import sd

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer	# LOQ
utils = RFCUtils.RFCUtils()

### Constants ###

iIndependent = con.iIndependent
iIndependent2 = con.iIndependent2
iNative = con.iNative
iCeltia = con.iCeltia
iCarthage = con.iCarthage
pIndependent = gc.getPlayer(iIndependent)
pIndependent2 = gc.getPlayer(iIndependent2)
pNative = gc.getPlayer(iNative)
pCeltia = gc.getPlayer(iCeltia)
pCarthage = gc.getPlayer(iCarthage)
teamIndependent = gc.getTeam(pIndependent.getTeam())
teamIndependent2 = gc.getTeam(pIndependent2.getTeam())
teamNative = gc.getTeam(pNative.getTeam())
teamCeltia = gc.getTeam(pCeltia.getTeam())

iBarbarian = con.iBarbarian
pBarbarian = gc.getPlayer(iBarbarian)
teamBarbarian = gc.getTeam(pBarbarian.getTeam())

# Spawning cities (Leoreth)
# Year, coordinates, owner, name, population, unit type, unit number, religions, forced spawn
tMinorCities = (
(-3000, (73, 38), iIndependent, 'Yerushalayim', 2, con.iArcher, 3),	# Jerusalem
(-3000, (79, 40), iIndependent2, 'Shushan', 1, con.iArcher, 1), 	# Susa
(-2000, (85, 47), iIndependent, 'Afrasiyab', 1, con.iArcher, 1), 	# Samarkand
#(-2000, (92, 39), iIndependent, 'Varanasi', 1, con.iWarrior, 1), 	# Varanasi
(-1600, (90, 40), iIndependent, 'Indraprastha', 1, con.iWarrior, 1),	# Delhi
(-1000, (102, 47), iIndependent, 'Zhongdu', 2, con.iSpearman, 1),	# Beijing
(-1000, (72, 44), iIndependent, 'Ankuwash', 2, con.iArcher, 2),		# Ankara
(-760, (59, 47), iCeltia, 'Melpum', 2, con.iArcher, 2),			# Milan
(-350, (56, 47), iCeltia, 'Lugodunon', 2, -1, -1),			# Lyon
(-325, (92, 33), iIndependent, 'Kanchipuram', 2, con.iArcher, 1),	# Madras
(-300, (105, 49), iBarbarian, 'Simiyan hoton', 2, con.iChariot, 2),	# Shenyang
(-300, (53, 48), iCeltia, 'Burdigala', 2, -1, -1),			# Bordeaux
(-300, (91, 31), iIndependent, 'Tanjapuri', 1, con.iWarElephant, 1),	# Thanjavur
(-190, (77, 44), iIndependent2, 'Artashat', 1, -1, -1),			# Artaxata
(-100, (95, 47), iBarbarian, 'Dunhuang', 2, con.iArcher, 1),		# Dunhuang
(-100, (19, 35), iNative, 'Danni B&#225;a', 2, con.iMayanHolkan, 2),	# Monte Albán
(-75, (89, 46), iBarbarian, 'Kashgar', 2, con.iArcher, 1),		# Kashgar
(-50, (55, 50), iCeltia, 'Lutetia', 2, -1, -1),				# Paris
(100, (76, 30), iIndependent, "Sana'a", 2, -1, -1),			# Sana'a
(107, (98, 36), iIndependent2, 'Pagan', 2, -1, -1),			# Pagan
(633, (96, 43), iBarbarian, 'Rasa', 2, con.iTibetanKhampa, 1),		# Lhasa
(680, (51, 37), iIndependent, 'Marrakus', 1, con.iCrossbowman, 1),	# Marrakesh
(700, (30, 20), iNative, 'Tiwanaku', 1, -1, -1),			# Tihuanaco
(800, con.tVienna, iIndependent, 'Vindobona', 1, con.iLongbowman, 1),	# Wien
(830, (59, 54), iIndependent, 'Hamburg', 2, con.iCrossbowman, 1),	# Hamburg
(830, (60, 54), iIndependent, 'L&#252;beck', 2, con.iCrossbowman, 1),	# Lübeck
(866, (101, 37), iBarbarian, 'Hanoi', 2, -1, -1),			# Hanoi
(880, (65, 48), iIndependent2, 'Buda', 3, con.iHorseArcher, 5),		# Budapest
(900, (24, 26), iNative, 'Tucume', 1, con.iArcher, 2),			# Tucume
(900, (25, 23), iNative, 'Chan Chan', 2, con.iArcher, 2),		# Chan Chan
(900, (69, 52), iIndependent, 'Kyiv', 2, con.iLongbowman, 2),		# Kiev
(990, (49, 56), iCeltia, '&#193;th Cliath', 1, -1, -1),			# Dublin
(1000, (61, 63), iIndependent2, 'Nidaros', 1, con.iVikingHuscarl, 1),	# Trondheim
(1000, (71, 17), iNative, 'Quelimane', 1, con.iZuluImpi, 1),		# Quelimane
(1100, (71, 20), iNative, 'Mombasa', 1, con.iZuluImpi, 1),		# Mombasa
(1200, (77, 55), iBarbarian, 'Qazan', 2, con.iHorseArcher, 1),		# Kazan
(1400, (104, 33), iIndependent, 'Saigon', 5, con.iLongbowman, 3),	# Saigon
(1483, (62, 20), iNative, 'Mbanza Kongo', 1, con.iCongolesePombos, 1),	# Mbanza Kongo
)

# do some research on dates here
tMinorStates = (
	(633, 1400, 96, 43, [con.iArcher, con.iSwordsman]),	# Tibet
	(-75, 1600, 89, 46, [con.iHorseArcher]),		# Kashgar
	(-75, 1600, 85, 47, [con.iHorseArcher]),		# Samarkand
	(-300, 600, 91, 31, [con.iArcher, con.iSwordsman, con.iWarElephant]), # Chola
	(-300, 600, 92, 33, [con.iArcher, con.iSwordsman, con.iWarElephant]), # Chola
	(-300, 900, 105, 49, [con.iHorseArcher, con.iSwordsman]), # Jurchen
	(1100, 1500, 60, 44, [con.iPikeman, con.iLongbowman]), # Rome late
	(0, 1100, 60, 44, [con.iSpearman, con.iArcher]), # Rome early
)

#handicap level modifier
iHandicapOld = (gc.getGame().getHandicapType() - 1)

class Barbs:

	def makeUnit(self, iUnit, iPlayer, tCoords, iNum, iForceAttack):
		'Makes iNum units for player iPlayer of the type iUnit at tCoords.'
		for i in range(iNum):
			player = gc.getPlayer(iPlayer)
			if (iForceAttack == 0):
				player.initUnit(iUnit, tCoords[0], tCoords[1], UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			elif (iForceAttack == 1):
				player.initUnit(iUnit, tCoords[0], tCoords[1], UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)				  
			elif (iForceAttack == 2):
				player.initUnit(iUnit, tCoords[0], tCoords[1], UnitAITypes.UNITAI_ATTACK_SEA, DirectionTypes.DIRECTION_SOUTH)



		
	def checkTurn(self, iGameTurn):
		
		#handicap level modifier
		iHandicap = gc.getHandicapInfo(gc.getGame().getHandicapType()).getBarbarianSpawnModifier()
		
		# Leoreth: buff certain cities if independent / barbarian (imported from SoI)
		if iGameTurn % 20 == 10:
			for tMinorCity in tMinorStates:
				if iGameTurn > getTurnForYear(tMinorCity[0]) and iGameTurn < getTurnForYear(tMinorCity[1]):
					plot = gc.getMap().plot(tMinorCity[2], tMinorCity[3])
					iOwner = plot.getOwner()
					if plot.isCity() and plot.getNumUnits() < 4 and iOwner >= con.iNumPlayers:
						lUnitList = tMinorCity[4]
						iRand = gc.getGame().getSorenRandNum(len(lUnitList), 'random unit')
						iUnit = lUnitList[iRand]
						utils.makeUnit(iUnit, iOwner, (tMinorCity[2], tMinorCity[3]), 1)

		if (iGameTurn >= getTurnForYear(-3000) and iGameTurn <= getTurnForYear(-850)):
			if (iHandicap >= 0):
				self.checkSpawn(iBarbarian, con.iWarrior, 1, (76, 46), (99, 53), self.spawnMinors, iGameTurn, 5, 0)
			
			self.checkSpawn(iBarbarian, con.iWolf, 1, (75, 54), (104, 64), self.spawnNatives, iGameTurn, 5, 2)
			self.checkSpawn(iBarbarian, con.iBear, 1, (75, 54), (104, 64), self.spawnNatives, iGameTurn, 5, 4)
			self.checkSpawn(iBarbarian, con.iLion, 1, (55, 10), (72, 29), self.spawnNatives, iGameTurn, 4, 1)
			self.checkSpawn(iBarbarian, con.iPanther, 1, (55, 10), (72, 29), self.spawnNatives, iGameTurn, 4, 3)

			
		#celts
		if (iGameTurn >= getTurnForYear(-650) and iGameTurn <= getTurnForYear(-110)):
			self.checkSpawn(iCeltia, con.iCelticGallicWarrior, 1, (49, 46), (65, 52), self.spawnMinors, iGameTurn, 6, 0)
			if (iHandicap >= 0):
				self.checkSpawn(iCeltia, con.iAxeman, 1, (49, 46), (65, 52), self.spawnMinors, iGameTurn, 8, 5, ["TXT_KEY_ADJECTIVE_GAUL"])

		#norse
		if (iGameTurn >= getTurnForYear(-650) and iGameTurn <= getTurnForYear(550)):
			self.checkSpawn(iBarbarian, con.iGalley, 1, (50, 49), (61, 55), self.spawnPirates, iGameTurn, 20, 0, ["TXT_KEY_ADJECTIVE_NORSE"])
			
		#mongolia
		if (iGameTurn >= getTurnForYear(-210) and iGameTurn < getTurnForYear(300)):
			self.checkSpawn(iBarbarian, con.iHorseArcher, 3 + iHandicap, (94, 48), (107, 54), self.spawnNomads, iGameTurn, 8-iHandicap, 0, ["TXT_KEY_ADJECTIVE_XIONGNU"])
		if (iGameTurn >= getTurnForYear(300) and iGameTurn <= getTurnForYear(900)):
			iNumUnits = 2 + iHandicap
			self.checkSpawn(iBarbarian, con.iHorseArcher, iNumUnits, (91, 50), (107, 54), self.spawnNomads, iGameTurn, 7-iHandicap, 0, ["TXT_KEY_ADJECTIVE_GOKTURK", "TXT_KEY_ADJECTIVE_UIGHUR"])
		if (iGameTurn > getTurnForYear(900) and iGameTurn <= getTurnForYear(1100)):
			iNumUnits = 1 + iHandicap
			self.checkSpawn(iBarbarian, con.iMongolianKeshik, iNumUnits, (94, 48), (107, 54), self.spawnInvaders, iGameTurn, 6, 0, ["TXT_KEY_ADJECTIVE_JURCHEN", "TXT_KEY_ADJECTIVE_KHITAN"])
			
		#tibet
		if (iGameTurn >= getTurnForYear(-350) and iGameTurn <= getTurnForYear(1100)):
			self.checkSpawn(iBarbarian, con.iSwordsman, 1 + iHandicap, (92, 41), (99, 45), self.spawnMinors, iGameTurn, 10-iHandicap, 3, ["TXT_KEY_ADJECTIVE_TIBETAN"])

		# Deccan barbarians
		if iGameTurn >= getTurnForYear(-1000) and iGameTurn <= getTurnForYear(1200):
			iUnit = con.iArcher
			iStrength = iHandicap
			if iGameTurn >= getTurnForYear(-500): iUnit = con.iAxeman
			if iGameTurn >= getTurnForYear(0): iStrength += 1
			if iGameTurn >= getTurnForYear(200): iUnit = con.iSwordsman
			
			self.checkSpawn(iBarbarian, iUnit, iStrength, (87, 23), (96, 37), self.spawnInvaders, iGameTurn, 8-iHandicap, 0, ["Hindi"])
			
		# elephants in india pre-khmer
		if (iGameTurn >= getTurnForYear(-210) and iGameTurn <= getTurnForYear(700)):
			self.checkSpawn(iBarbarian, con.iWarElephant, 1, (86, 31), (100, 41), self.spawnInvaders, iGameTurn, 8-iHandicap, 4)

		#Indo-Scythians
		if iGameTurn >= getTurnForYear(-200) and iGameTurn <= getTurnForYear(400):
			self.checkSpawn(iBarbarian, con.iHorseArcher, 2, (84, 40), (89, 43), self.spawnNomads, iGameTurn, 8-iHandicap, 4, ["TXT_KEY_ADJECTIVE_INDO_SCYTHIAN"])

		#Kushana
		if iGameTurn >= getTurnForYear(30) and iGameTurn <= getTurnForYear(220):
			self.checkSpawn(iBarbarian, con.iKushanAsvaka, 3+iHandicap, (84, 40), (89, 43), self.spawnInvaders, iGameTurn, 8, 3, ["TXT_KEY_ADJECTIVE_KUSHANA"])

		#Hephtalites
		if iGameTurn >= getTurnForYear(400) and iGameTurn <= getTurnForYear(550):
			self.checkSpawn(iBarbarian, con.iHorseArcher, 2+iHandicap, (84, 40), (89, 43), self.spawnInvaders, iGameTurn, 5-iHandicap, 2, ["TXT_KEY_ADJECTIVE_HEPHTHALITE"])

		# Holkans in classical Mesoamerica
		if iGameTurn >= getTurnForYear(100) and iGameTurn <= getTurnForYear(600):
			self.checkSpawn(iBarbarian, con.iMayanHolkan, 1, (17, 31), (25, 37), self.spawnUprising, iGameTurn, 6, 4)
			
		if iGameTurn >= getTurnForYear(600) and iGameTurn <= getTurnForYear(1000):
			self.checkSpawn(iBarbarian, con.iMayanHolkan, 1, (17, 31), (25, 37), self.spawnUprising, iGameTurn, 4, 2)
			
		#pirates in Mediterranean
		if (iGameTurn >= getTurnForYear(-210) and iGameTurn <= getTurnForYear(50)):
			self.checkSpawn(iBarbarian, con.iTrireme, 1, (49, 37), (72, 44), self.spawnPirates, iGameTurn, 8, 0)
		#pirates in Barbary coast
		if not gc.getPlayer(con.iMoors).isAlive():
			if (iGameTurn >= getTurnForYear(50) and iGameTurn <= getTurnForYear(700)):
				self.checkSpawn(iBarbarian, con.iTrireme, 1, (46, 30), (62, 39), self.spawnPirates, iGameTurn, 18, 0)
			if (iGameTurn >= getTurnForYear(700) and iGameTurn <= getTurnForYear(1400)):
				self.checkSpawn(iBarbarian, con.iTrireme, 1, (46, 30), (62, 39), self.spawnPirates, iGameTurn, 8, 0)
		#pirates in Indian ocean
		if (iGameTurn >= getTurnForYear(-650) and iGameTurn <= getTurnForYear(700)):
			self.checkSpawn(iBarbarian, con.iTrireme, 1, (72, 20), (91, 36), self.spawnPirates, iGameTurn, 18, 0)
		if (iGameTurn >= getTurnForYear(700) and iGameTurn <= getTurnForYear(1700)):
			self.checkSpawn(iBarbarian, con.iTrireme, 1, (72, 20), (91, 36), self.spawnPirates, iGameTurn, 10, 0)

		# Leoreth: Barbarians in Anatolia (Hittites), replace Hattusas spawn
		if (iGameTurn >= getTurnForYear(-2000) and iGameTurn <= getTurnForYear(-800)):
			self.checkSpawn(iBarbarian, con.iHittiteHuluganni, 1 + iHandicap, (68, 42), (74, 45), self.spawnInvaders, iGameTurn, 16, 0, ["TXT_KEY_ADJECTIVE_HITTITE"])
			
		#barbarians in europe
		if (iGameTurn >= getTurnForYear(-210) and iGameTurn <= getTurnForYear(470)):
			self.checkSpawn(iBarbarian, con.iAxeman, 3 + iHandicap, (50, 45), (63, 52), self.spawnInvaders, iGameTurn, 10, 0, ["TXT_KEY_ADJECTIVE_GERMANIC"])
			self.checkSpawn(iBarbarian, con.iAxeman, 2 + iHandicap, (64, 49), (69, 55), self.spawnInvaders, iGameTurn, 12, 2, ["TXT_KEY_ADJECTIVE_GERMANIC"])
		# Leoreth: begins 100 AD instead of 50 AD
		if (iGameTurn >= getTurnForYear(100) and iGameTurn <= getTurnForYear(470)):
			self.checkSpawn(iBarbarian, con.iSwordsman, 3, (58, 45), (70, 55), self.spawnInvaders, iGameTurn, 8, 5, ["TXT_KEY_ADJECTIVE_GERMANIC"])
		if (iGameTurn >= getTurnForYear(300) and iGameTurn <= getTurnForYear(550)):
			self.checkSpawn(iBarbarian, con.iAxeman, 4 + iHandicap, (49, 41), (56, 52), self.spawnInvaders, iGameTurn, 5, 4, ["TXT_KEY_ADJECTIVE_VISIGOTHIC"])
			self.checkSpawn(iBarbarian, con.iSwordsman, 4 + iHandicap, (49, 41), (57, 52), self.spawnInvaders, iGameTurn, 5, 2, ["TXT_KEY_ADJECTIVE_VISIGOTHIC"])
			self.checkSpawn(iBarbarian, con.iHorseArcher, 3, (55, 49), (65, 53), self.spawnInvaders, iGameTurn, 5, 0, ["TXT_KEY_ADJECTIVE_HUNNIC"])
		if (iGameTurn >= getTurnForYear(300) and iGameTurn <= getTurnForYear(700)):
			self.checkSpawn(iBarbarian, con.iHorseArcher, 3 + iHandicap, (58, 50), (88, 53), self.spawnInvaders, iGameTurn, 3, 2, ["TXT_KEY_ADJECTIVE_HUNNIC"])

		#Leoreth: barbarians in Balkans / Black Sea until the High Middle Ages (Bulgarians, Cumans, Pechenegs)
		if (iGameTurn >= getTurnForYear(680) and iGameTurn <= getTurnForYear(1000)):
			self.checkSpawn(iBarbarian, con.iHorseArcher, 3 + iHandicap, (64, 45), (69, 49), self.spawnInvaders, iGameTurn, 6, 2, ["TXT_KEY_ADJECTIVE_AVAR", "TXT_KEY_ADJECTIVE_BULGAR"])
		if (iGameTurn >= getTurnForYear(900) and iGameTurn <= getTurnForYear(1200)):
			self.checkSpawn(iBarbarian, con.iHorseArcher, 3 + iHandicap, (68, 48), (78, 50), self.spawnInvaders, iGameTurn, 8, 5, ["TXT_KEY_ADJECTIVE_CUMAN"])
			
		#barbarians in central asia
		if (iGameTurn >= getTurnForYear(-1600) and iGameTurn < getTurnForYear(-850)):
			self.checkSpawn(iBarbarian, con.iSumerianVulture, 1, (74, 34), (78, 44), self.spawnNomads, iGameTurn, 6-iHandicap, 2, ["TXT_KEY_ADJECTIVE_ASSYRIAN"])
		if (iGameTurn >= getTurnForYear(-850) and iGameTurn < getTurnForYear(300)):
			self.checkSpawn(iBarbarian, con.iSumerianVulture, 1, (73, 38), (78, 44), self.spawnNomads, iGameTurn, 8-iHandicap, 2, ["TXT_KEY_ADJECTIVE_ASSYRIAN"])
			self.checkSpawn(iBarbarian, con.iHorseArcher, 2 + iHandicap, (79, 41), (84, 49), self.spawnInvaders, iGameTurn, 7-iHandicap, 2, ["TXT_KEY_ADJECTIVE_PARTHIAN"])
		if (iGameTurn >= getTurnForYear(300) and iGameTurn <= getTurnForYear(700)):
			#if utils.getScenario() == con.i3000BC:  #late start condition
			self.checkSpawn(iBarbarian, con.iHorseArcher, 2 + iHandicap, (78, 42), (88, 50), self.spawnNomads, iGameTurn, 8-iHandicap, 2, ["TXT_KEY_ADJECTIVE_TURKIC"])
		if (iGameTurn > getTurnForYear(700) and iGameTurn <= getTurnForYear(1040)):
			#if utils.getScenario() == con.i3000BC:  #late start condition
			self.checkSpawn(iBarbarian, con.iHorseArcher, 2 + iHandicap, (78, 42), (90, 52), self.spawnNomads, iGameTurn, 6-iHandicap, 2, ["TXT_KEY_ADJECTIVE_TURKIC"])

		# late Central Asian barbarians
		iSteppeUnit = con.iMongolianKeshik
		iExtra = iHandicap
		if iGameTurn >= getTurnForYear(1600): 
			iSteppeUnit = con.iCuirassier
			iExtra += 1
		
		if iGameTurn >= getTurnForYear(1200) and iGameTurn <= getTurnForYear(1650):
			if not utils.getAreaCitiesCiv(con.iMongolia, utils.getPlotList((70, 48), (80, 59))):
				self.checkSpawn(iBarbarian, iSteppeUnit, 2 + iExtra, (74, 47), (81, 47), self.spawnNomads, iGameTurn, 10-iHandicap, 5, ["TXT_KEY_ADJECTIVE_TATAR", "TXT_KEY_ADJECTIVE_NOGAI"])
		if iGameTurn >= getTurnForYear(1400) and iGameTurn <= getTurnForYear(1700):
			if utils.getAreaCities(utils.getPlotList((80, 47), (88, 53))):
				self.checkSpawn(iBarbarian, iSteppeUnit, 1 + iExtra, (80, 47), (88, 53), self.spawnNomads, iGameTurn, 10-2*iHandicap, 2, ["TXT_KEY_ADJECTIVE_UZBEK", "TXT_KEY_ADJECTIVE_KAZAKH"])
		if iGameTurn >= getTurnForYear(1500) and iGameTurn <= getTurnForYear(1800):
			if utils.getAreaCities(utils.getPlotList((82, 53), (92, 60))):
				self.checkSpawn(iBarbarian, iSteppeUnit, 1 + iExtra, (82, 53), (92, 60), self.spawnNomads, iGameTurn, 8-iHandicap, 2, ["TXT_KEY_ADJECTIVE_SIBIR"])
			
		#barbarians in Elam
		if (iGameTurn >= getTurnForYear(-1600) and iGameTurn < getTurnForYear(-1000)):
			self.checkSpawn(iBarbarian, con.iChariot, 1, (81, 37), (87, 45), self.spawnMinors, iGameTurn, 9-iHandicap, 0, ["TXT_KEY_ADJECTIVE_ELAMITE"])

		#barbarians in north africa
		if (iGameTurn >= getTurnForYear(-210) and iGameTurn < getTurnForYear(50)):
			self.checkSpawn(iBarbarian, con.iNumidianCavalry, 1, (54, 31), (67, 35), self.spawnNomads, iGameTurn, 9-iHandicap, 3, ["TXT_KEY_ADJECTIVE_BERBER"])
		if (iGameTurn >= getTurnForYear(50) and iGameTurn < getTurnForYear(900)):
			if utils.getScenario() == con.i3000BC:  #late start condition
				self.checkSpawn(iBarbarian, con.iNumidianCavalry, 3 + iHandicap, (54, 31), (67, 35), self.spawnNomads, iGameTurn, 10-iHandicap, 5, ["TXT_KEY_ADJECTIVE_BERBER"])
		if (iGameTurn >= getTurnForYear(900) and iGameTurn <= getTurnForYear(1800)):
			self.checkSpawn(iBarbarian, con.iArabianCamelArcher, 1, (54, 27), (67, 35), self.spawnNomads, iGameTurn, 8-iHandicap, 4, ["TXT_KEY_ADJECTIVE_BERBER"])
			
		#camels in arabia
		if (iGameTurn >= getTurnForYear(190) and iGameTurn <= getTurnForYear(550)):
			self.checkSpawn(iBarbarian, con.iArabianCamelArcher, 2, (73, 30), (82, 36), self.spawnNomads, iGameTurn, 9-iHandicap, 7, ["TXT_KEY_ADJECTIVE_BEDOUIN"])
		if iGameTurn >= getTurnForYear(-800) and iGameTurn <= getTurnForYear(1300):
			iNumUnits = iHandicap
			if utils.getScenario() == con.i3000BC: iNumUnits += 1
			if iGameTurn >= getTurnForYear(400): iNumUnits += 2
			self.checkSpawn(iBarbarian, con.iNubianMedjay, iNumUnits, (66, 28), (71, 34), self.spawnUprising, iGameTurn, 12, 4, ["TXT_KEY_ADJECTIVE_NUBIAN"])
		if (iGameTurn >= getTurnForYear(450) and iGameTurn <= getTurnForYear(1600)):
			if utils.getScenario() == con.i3000BC:
				self.checkSpawn(iNative, con.iZuluImpi, 2 + iHandicap, (60, 10), (72, 27), self.spawnNatives, iGameTurn, 10, 4)
			else:
				self.checkSpawn(iNative, con.iZuluImpi, 2 + iHandicap, (60, 10), (72, 27), self.spawnNatives, iGameTurn, 15, 4)
		if iGameTurn >= getTurnForYear(1600) and iGameTurn <= getTurnForYear(1800):
			self.checkSpawn(iNative, con.iCongolesePombos, 2 + iHandicap, (60, 10), (72, 27), self.spawnNatives, iGameTurn, 10, 4)
			
		#west africa
		if (iGameTurn >= getTurnForYear(450) and iGameTurn <= getTurnForYear(1700)):
			if iGameTurn < getTurnForYear(1300):
				sAdj = ["TXT_KEY_ADJECTIVE_GHANAIAN"]
			else:
				sAdj = ["TXT_KEY_ADJECTIVE_SONGHAI"]
			self.checkSpawn(iBarbarian, con.iMandeFarari, 1, (48, 26), (65, 37), self.spawnMinors, iGameTurn, 16, 4, sAdj)
			self.checkSpawn(iBarbarian, con.iZuluImpi, 2, (48, 22), (63, 29), self.spawnMinors, iGameTurn, 16, 10, sAdj)

		#American natives
		if (iGameTurn >= getTurnForYear(600) and iGameTurn <= getTurnForYear(1100)):
			self.checkSpawn(iBarbarian, con.iNativeAmericanDogSoldier, 1 + iHandicap, (15, 38), (24, 47), self.spawnNatives, iGameTurn, 20, 0)
			if utils.getScenario() == con.i3000BC:  #late start condition
				self.checkSpawn(iBarbarian, con.iAztecJaguar, 3, (15, 38), (24, 47), self.spawnNatives, iGameTurn, 16 - 2*iHandicap, 10)
			else:  #late start condition
				self.checkSpawn(iBarbarian, con.iAztecJaguar, 2, (15, 38), (24, 47), self.spawnNatives, iGameTurn, 16 - 2*iHandicap, 10)
		if (iGameTurn >= getTurnForYear(1300) and iGameTurn <= getTurnForYear(1600)):
			self.checkSpawn(iBarbarian, con.iNativeAmericanDogSoldier, 2 + iHandicap, (15, 38), (24, 47), self.spawnNatives, iGameTurn, 8, 0)
		if (iGameTurn >= getTurnForYear(1400) and iGameTurn <= getTurnForYear(1800)):
			self.checkSpawn(iBarbarian, con.iNativeAmericanDogSoldier, 1 + iHandicap, (11, 44), (33, 51), self.spawnUprising, iGameTurn, 12, 0)
			self.checkSpawn(iBarbarian, con.iNativeAmericanDogSoldier, 1 + iHandicap, (11, 44), (33, 51), self.spawnUprising, iGameTurn, 12, 6)
		if (iGameTurn >= getTurnForYear(1300) and iGameTurn <= getTurnForYear(1600)):
			if (iGameTurn % 18 == 0):
				if (gc.getMap().plot(27, 29).getNumUnits() == 0):
					self.makeUnit(con.iNativeAmericanDogSoldier, iBarbarian, (27, 29), 3 + iHandicap, 1)
			if (iGameTurn % 18 == 9):
				if (gc.getMap().plot(30, 13).getNumUnits() == 0):
					self.makeUnit(con.iNativeAmericanDogSoldier, iBarbarian, (30, 13), 3 + iHandicap, 1)
		
		if iGameTurn >= getTurnForYear(1700) and iGameTurn <= getTurnForYear(1900):
			self.checkSpawn(iBarbarian, con.iSiouxMountedBrave, 1 + iHandicap, (15, 44), (24, 52), self.spawnUprising, iGameTurn, 12 - iHandicap, 2)
			
		if iGameTurn >= getTurnForYear(1500) and iGameTurn <= getTurnForYear(1850):
			self.checkSpawn(iBarbarian, con.iIroquoisMohawk, 2 + iHandicap, (24, 46), (30, 51), self.spawnUprising, iGameTurn, 8 - iHandicap, 4)
				
		#pirates in the Caribbean
		if (iGameTurn >= getTurnForYear(1600) and iGameTurn <= getTurnForYear(1800)):
			self.checkSpawn(iBarbarian, con.iPrivateer, 1, (24, 32), (35, 46), self.spawnPirates, iGameTurn, 5, 0)
		#pirates in Asia
		if (iGameTurn >= getTurnForYear(1500) and iGameTurn <= getTurnForYear(1900)):
			self.checkSpawn(iBarbarian, con.iPrivateer, 1, (72, 24), (110, 36), self.spawnPirates, iGameTurn, 8, 0)

		if iGameTurn < getTurnForYear(tMinorCities[len(tMinorCities)-1][0])+10:
			self.foundMinorCities(iGameTurn)
			
		if iGameTurn == getTurnForYear(con.tBirth[con.iInca]):
			if utils.getHumanID() == con.iInca:
				utils.makeUnit(con.iIncanAucac, iNative, (24, 26), 1)
				utils.makeUnit(con.iIncanAucac, iNative, (25, 23), 1)
				
	def foundMinorCities(self, iGameTurn):
		for i in range(len(tMinorCities)):
			iYear, tPlot, iPlayer, sName, iPopulation, iUnitType, iNumUnits = tMinorCities[i]
			if iGameTurn < getTurnForYear(iYear): return
			if iGameTurn > getTurnForYear(iYear)+10: continue
			
			if sd.isMinorCityFounded(i): continue
			
			x, y = tPlot
			plot = gc.getMap().plot(x, y)
			if plot.isCity(): continue
			
			# special cases
			if not self.canFoundCity(sName): continue
			
			lReligions = []
			bForceSpawn = False
			
			if sName == 'Kyiv': lReligions = [con.iOrthodoxy, con.iCatholicism]
			if iPlayer == iCeltia and utils.getScenario() != con.i3000BC: iPlayer = iIndependent
			if sName == 'Buda': bForceSpawn = True
			
			if not self.isFreePlot(tPlot, bForceSpawn): continue
			
			utils.evacuate(tPlot)
		
			if self.foundCity(iPlayer, tPlot, sName, iPopulation, iUnitType, iNumUnits, lReligions):
				sd.setMinorCityFounded(i, True)
		
	def canFoundCity(self, sName):
		if sName == 'Kanchipuram' and utils.getHumanID() == con.iTamils: return False
		elif sName == 'Tanjapuri' and gc.getPlayer(con.iTamils).isAlive(): return False
		elif sName == 'Zhongdu' and utils.getHumanID() == con.iChina: return False
		elif sName == 'Hamburg' and (utils.getHumanID() == con.iHolyRome or utils.getSeed() % 4 == 0): return False
		elif sName == 'L&#252;beck' and (utils.getHumanID() == con.iHolyRome or utils.getSeed() % 4 != 0): return False
		elif sName == 'Rasa' and gc.getPlayer(con.iTibet).isAlive(): return False
		#elif sName == 'Marrakus' and utils.getScenario() != con.i3000BC: return False
		
		return True
	
	def foundCity(self, iPlayer, tPlot, sName, iPopulation, iUnitType = -1, iNumUnits = -1, lReligions = []):
		pPlayer = gc.getPlayer(iPlayer)
		x, y = tPlot
		plot = gc.getMap().plot(x, y)
		plot.setOwner(iPlayer)
		pPlayer.found(x, y)
		
		if plot.isCity():
			city = gc.getMap().plot(x, y).getPlotCity()
			
			city.setName(sName, False)
			city.setPopulation(iPopulation)
			
			plot.changeCulture(iPlayer, 10 * (gc.getGame().getCurrentEra() + 1), True)
			city.changeCulture(iPlayer, 10 * (gc.getGame().getCurrentEra() + 1), True)
			
			if iNumUnits > 0 and iUnitType > 0:
				utils.makeUnit(iUnitType, iPlayer, tPlot, iNumUnits)
				
			for iReligion in lReligions:
				if gc.getGame().isReligionFounded(iReligion):
					city.setHasReligion(iReligion, True, False, False)
					
			return True
		
		return False
					
	def clearUnits(self, iPlayer, tPlot):	
		lHumanUnits = []
		lOtherUnits = []
	
		for x in range(tPlot[0], tPlot[0]+1):
			for y in range(tPlot[1], tPlot[1]+1):
				plot = gc.getMap().plot(x, y)
				
				for iUnit in range(plot.getNumUnits()):
					unit = plot.getUnit(iUnit)
					
					if unit.getOwner() == utils.getHumanID():
						lHumanUnits.append(unit)
					else:
						lOtherUnits.append(unit)
						
		capital = gc.getPlayer(utils.getHumanID()).getCapitalCity()
		for unit in lHumanUnits:
			unit.setXY(capital.getX(), capital.getY())
			
		for unit in lOtherUnits:
			utils.makeUnit(unit.getUnitType(), iPlayer, tPlot, 1)
			unit.kill(False, con.iBarbarian)
				
	def isFreePlot(self, tPlot, bIgnoreCulture = False):
		x, y = tPlot
		plot = gc.getMap().plot(x, y)
		
		# no cultural control over the tile
		if plot.isOwned() and plot.getOwner() < con.iNumPlayers and not bIgnoreCulture:
			return False
				
		# no city in adjacent tiles
		for i in range(x-1, x+2):
			for j in range(y-1, y+2):
				currentPlot = gc.getMap().plot(x, y)
				if currentPlot.isCity(): return False
						
		return True
			
	def checkRegion(self, tCity):
		cityPlot = gc.getMap().plot(tCity[0], tCity[1])
		iNumUnitsInAPlot = cityPlot.getNumUnits()
##		print iNumUnitsInAPlot
		
		#checks if the plot already belongs to someone
		if (cityPlot.isOwned()):
			if (cityPlot.getOwner() != iBarbarian ):
				return (False, -1)
		
##		#checks if there's a unit on the plot
		if (iNumUnitsInAPlot):
			for i in range(iNumUnitsInAPlot):
				unit = cityPlot.getUnit(i)
				iOwner = unit.getOwner()
				if (iOwner == iBarbarian):
					return (False, tCity[3]+1) 
				#pOwner = gc.getPlayer(iOwner)
				#if (pOwner.isHuman()):
				#	return (False, tCity[3]+1)

		#checks the surroundings and allows only AI units
		for x in range(tCity[0]-1, tCity[0]+2):
			for y in range(tCity[1]-1, tCity[1]+2):
				currentPlot=gc.getMap().plot(x,y)
				if (currentPlot.isCity()):
					return (False, -1)
				iNumUnitsInAPlot = currentPlot.getNumUnits()
				if (iNumUnitsInAPlot):
					for i in range(iNumUnitsInAPlot):
						unit = currentPlot.getUnit(i)
						iOwner = unit.getOwner()
						pOwner = gc.getPlayer(iOwner)
						if (pOwner.isHuman()):
							return (False, tCity[3]+1)
		return (True, tCity[3])



	def spawnUnits(self, iCiv, tTopLeft, tBottomRight, iUnitType, iNumUnits, iTurn, iPeriod, iRest, function, iForceAttack):
		if (iTurn % utils.getTurns(iPeriod) == iRest):
			dummy, plotList = utils.squareSearch( tTopLeft, tBottomRight, function, [] )
			if (len(plotList)):
				rndNum = gc.getGame().getSorenRandNum(len(plotList), 'Spawn units')
				result = plotList[rndNum]
				if (result):
					self.makeUnit(iUnitType, iCiv, result, iNumUnits, iForceAttack)
				


	    
	def killNeighbours(self, tCoords):
		'Kills all units in the neigbbouring tiles of plot (as well as plot itself) so late starters have some space.'
		for x in range(tCoords[0]-1, tCoords[0]+2):	# from x-1 to x+1
			for y in range(tCoords[1]-1, tCoords[1]+2):	# from y-1 to y+1
				killPlot = CyMap().getPlot(x, y)
				for i in range(killPlot.getNumUnits()):
					unit = killPlot.getUnit(0)	# 0 instead of i because killing units changes the indices
					unit.kill(False, iBarbarian)
					
	#Leoreth: new ways to spawn barbarians
	def checkSpawn(self, iPlayer, iUnitType, iNumUnits, tTL, tBR, spawnFunction, iTurn, iPeriod, iRest, lAdj=[]):
	
		if len(lAdj) == 0:
			sAdj = ""
		else:
			sAdj = utils.getRandomEntry(lAdj)
	
		if iTurn % utils.getTurns(iPeriod) == iRest:
			spawnFunction(iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj)
			
	def getFreeWaterTiles(self, tTL, tBR, bTerritory=False, bOcean=False):
	
		plotList = []
	
		for x in range(tTL[0], tBR[0]+1):
			for y in range(tTL[1], tBR[1]+1):
				plot = gc.getMap().plot(x,y)
				if plot.getTerrainType() == con.iCoast or (bOcean and plot.getTerrainType() == con.iOcean):
					if not plot.isUnit() and plot.area().getNumTiles() > 10:
						if not (bTerritory and plot.getOwner() != -1):
							plotList.append((x,y))
							
		return plotList
		
	def getFreeLandTiles(self, tTL, tBR, bTerritory=False, bJungle=False):
		plotList = []
	
		for x in range(tTL[0], tBR[0]+1):
			for y in range(tTL[1], tBR[1]+1):
				plot = gc.getMap().plot(x,y)
				if plot.isHills() or plot.isFlatlands():
					if plot.getTerrainType() != con.iMarsh and (bJungle or plot.getFeatureType() != con.iJungle):
						if not plot.isUnit() and not plot.isCity():
							bClear = True
							for i in range(x-1, x+2):
								for j in range(y-1, y+2):
									if gc.getMap().plot(i,j).isCity(): bClear = False
								
							if bClear and not (bTerritory and plot.getOwner() != -1):
								plotList.append((x,y))
							
		return plotList
		
	def getTargetCities(self, tTL, tBR):
		cityPlotList = []
		
		for x in range(tTL[0], tBR[0]+1):
			for y in range(tTL[1], tBR[1]+1):
				plot = gc.getMap().plot(x,y)
				if plot.isCity():
					city = plot.getPlotCity()
					if city.getOwner() < con.iNumPlayers and (city.getPopulation() > 1 or city.getCultureLevel() > 0):
						cityPlotList.append((city.getX(), city.getY()))
						
		return cityPlotList
		
	def getCitySpawnPlot(self, tPlot):
		x, y = tPlot
		plotList = []
		
		for i in range(x-2, x+3):
			for j in range(y-2, y+3):
				if abs(x-i) == 2 or abs(y-j) == 2:
					plot = gc.getMap().plot(i,j)
					if not plot.isUnit() and not plot.isWater() and not plot.isPeak() and not plot.isCity():
						plotList.append((i,j))
						
		return utils.getRandomEntry(plotList)

	def spawnPirates(self, iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
		'''Leoreth: spawns all ships at the same coastal spot, out to pillage and disrupt trade, can spawn inside borders'''
	
		plotList = self.getFreeWaterTiles(tTL, tBR, False, False)
		tPlot = utils.getRandomEntry(plotList)
		
		if tPlot:
			utils.makeUnitAI(iUnitType, iPlayer, tPlot, UnitAITypes.UNITAI_PIRATE_SEA, iNumUnits, sAdj)
		
	def spawnNatives(self, iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
		'''Leoreth: outside of territory, in jungles, all dispersed on several plots, out to pillage'''
		
		plotList = self.getFreeLandTiles(tTL, tBR, True, True)
		
		for i in range(iNumUnits):
			tPlot = utils.getRandomEntry(plotList)
			if not tPlot: break
			
			plotList.remove(tPlot)
			utils.makeUnitAI(iUnitType, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK, 1, sAdj)
			
	def spawnMinors(self, iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
		'''Leoreth: represents minor states without ingame cities
			    outside of territory, not in jungles, in groups, passive'''
			    
		plotList = self.getFreeLandTiles(tTL, tBR, True, False)
		tPlot = utils.getRandomEntry(plotList)
		
		if tPlot:
			utils.makeUnitAI(iUnitType, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK, iNumUnits, sAdj)
		
	def spawnNomads(self, iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
		'''Leoreth: represents aggressive steppe nomads etc.
			    outside of territory, not in jungles, in small groups, target cities'''
			    
		plotList = self.getFreeLandTiles(tTL, tBR, True, False)
		tPlot = utils.getRandomEntry(plotList)
		
		if tPlot:
			utils.makeUnitAI(iUnitType, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK, iNumUnits, sAdj)
			
	def spawnInvaders(self, iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
		'''Leoreth: represents large invasion forces and migration movements
			    inside of territory, not in jungles, in groups, target cities'''
			    
		plotList = self.getFreeLandTiles(tTL, tBR, False, False)
		tPlot = utils.getRandomEntry(plotList)
		
		if tPlot:
			utils.makeUnitAI(iUnitType, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK, iNumUnits, sAdj)
			
	def spawnUprising(self, iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
		''' Leoreth: represents uprisings of Natives against colonial settlements, especially North America
			     spawns units in a free plot in the second ring of a random target city in the area
			     (also used for units from warring city states in classical Mesoamerica)'''
			     
		targetCityList = self.getTargetCities(tTL, tBR)
		tCity = utils.getRandomEntry(targetCityList)
		
		if tCity:
			tPlot = self.getCitySpawnPlot(tCity)
			
			if tPlot:
				utils.makeUnitAI(iUnitType, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK, iNumUnits, sAdj)