# Rhye's and Fall of Civilization - Barbarian units and cities

from CvPythonExtensions import *
import CvUtil
import PyHelpers	# LOQ
#import Popup
#import cPickle as pickle
from RFCUtils import utils
from Consts import *
from StoredData import data

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer	# LOQ

# Spawning cities (Leoreth)
# Year, coordinates, owner, name, population, unit type, unit number, religions, forced spawn
tMinorCities = (
(-3000, (84, 45), iIndependent, 'Yerushalayim', 2, iArcher, 3),	# Jerusalem
(-3000, (92, 46), iIndependent, 'Shushan', 1, iArcher, 1), 		# Susa
(-3000, (88, 50), iIndependent2, 'Ashur', 2, iArcher, 2), 		# Assur
(-2500, (78, 37), iBarbarian, 'Kerma', 2, iArcher, 2), 			# Kerma
(-2000, (100, 54), iIndependent, 'Afrasiyab', 1, iArcher, 1), 	# Samarkand
#(-2000, (92, 39), iIndependent, 'Varanasi', 1, iMilitia, 1), 	# Varanasi
(-1600, (105, 46), iIndependent, 'Indraprastha', 1, iMilitia, 1),	# Delhi
(-1000, (124, 56), iIndependent, 'Zhongdu', 2, iSpearman, 1),	# Beijing
(-1000, (83, 53), iIndependent, 'Ankuwash', 2, iArcher, 2),		# Ankara
(-760, (67, 57), iCeltia, 'Melpum', 2, iArcher, 2),				# Milan
(-500, (96, 56), iIndependent, 'K&#246;ne&#252;rgen&#231;', 1, iArcher, 2), 	# Urgench
(-350, (64, 58), iCeltia, 'Lugodunon', 2, -1, -1),				# Lyon
(-325, (107, 35), iIndependent, 'Kanchipuram', 2, iArcher, 1),	# Madras
(-300, (128, 58), iBarbarian, 'Simiyan hoton', 2, iChariot, 2),	# Shenyang
(-300, (60, 56), iCeltia, 'Burdigala', 2, -1, -1),				# Bordeaux
(-300, (106, 33), iIndependent, 'Tanjapuri', 1, iWarElephant, 1),	# Thanjavur
(-190, (89, 54), iIndependent2, 'Artashat', 1, -1, -1),			# Artaxata
(-100, (114, 57), iBarbarian, 'Dunhuang', 2, iArcher, 1),		# Dunhuang
(-100, (109, 56), iBarbarian, 'Kuqa', 2, iArcher, 1),			# Kuqa
(-100, (19, 41), iNative, 'Danni B&#225;a', 2, iHolkan, 2),		# Monte Albán
(-75, (105, 55), iBarbarian, 'Kashgar', 2, iArcher, 1),			# Kashgar
(-50, (62, 60), iCeltia, 'Lutetia', 2, -1, -1),					# Paris
(100, (88, 36), iIndependent, "Sana'a", 2, -1, -1),				# Sana'a
(107, (117, 41), iIndependent2, 'Pagan', 2, -1, -1),			# Pagan
(500, (124, 38), iIndependent, 'Indrapura', 2, iArcher, 1),		# Indrapura
(633, (113, 48), iBarbarian, 'Rasa', 2, iKhampa, 1),			# Lhasa
(680, (58, 44), iIndependent, 'Marrakus', 1, iCrossbowman, 1),	# Marrakesh
(700, (34, 22), iNative, 'Tiwanaku', 1, -1, -1),				# Tihuanaco
(738, (119, 45), iIndependent2, 'Taihe', 2, iArcher, 1),		# Dali
(800, tVienna, iIndependent, 'Vindobona', 1, iCrossbowman, 1),	# Wien
(830, (67, 65), iIndependent, 'Hamburg', 2, iCrossbowman, 1),	# Hamburg
(830, (68, 65), iIndependent, 'L&#252;beck', 2, iCrossbowman, 1),	# Lübeck
(866, (122, 42), iBarbarian, 'Hanoi', 2, -1, -1),				# Hanoi
(880, (75, 59), iIndependent2, 'Buda', 3, iHorseArcher, 5),		# Budapest
(900, (25, 23), iNative, 'Pachakamaq', 1, iArcher, 2),			# Pachacamac
(900, (27, 28), iNative, 'Chan Chan', 2, iArcher, 2),			# Chan Chan
(900, (81, 62), iIndependent, 'Kyiv', 2, iCrossbowman, 2),		# Kiev
(990, (55, 64), iCeltia, '&#193;th Cliath', 1, -1, -1),			# Dublin
(1000, (69, 74), iIndependent2, 'Nidaros', 1, iHuscarl, 1),		# Trondheim
(1000, (87, 30), iNative, 'Muqdisho', 1, iImpi, 1),				# Mogadishu
(1000, (83, 20), iNative, 'Quelimane', 1, iImpi, 1),			# Quelimane
(1050, (84, 27), iNative, 'Mombasa', 1, iImpi, 1),				# Mombasa
(1100, (83, 24), iNative, 'Kilwa', 1, iImpi, 1),				# Kilwa
(1200, (92, 65), iBarbarian, 'Qazan', 2, iHorseArcher, 1),		# Kazan
(1400, (123, 35), iIndependent, 'Saigon', 5, iCrossbowman, 3),	# Saigon
(1483, (70, 24), iNative, 'Mbanza Kongo', 1, iPombos, 1),		# Mbanza Kongo
)

# do some research on dates here
tMinorStates = (
	(633, 1400, (113, 48), [iArcher, iSwordsman]),	# Tibet
	(-2500, -600, (88, 50), [iVulture]),		# Assyria
	(-75, 600, (105, 55), [iHorseman]),		# Kashgar early
	(600, 1600, (105, 55), [iHorseArcher]),		# Kashgar late
	(-75, 600, (100, 54), [iHorseman]),		# Samarkand early
	(600, 1600, (100, 54), [iHorseArcher]),		# Samarkand late
	(-300, 600, (106, 33), [iArcher, iSwordsman, iWarElephant]), # Chola
	(-300, 600, (107, 35), [iArcher, iSwordsman, iWarElephant]), # Chola
	(-300, 900, (128, 58), [iHorseArcher, iSwordsman]), # Jurchen
	(1100, 1500, (69, 54), [iPikeman, iLongbowman]), # Rome late
	(0, 1100, (69, 54), [iSpearman, iArcher]), # Rome early
)

#handicap level modifier
iHandicapOld = (gc.getGame().getHandicapType() - 1)

class Barbs:
		
	def checkTurn(self, iGameTurn):
		
		#handicap level modifier
		iHandicap = gc.getHandicapInfo(gc.getGame().getHandicapType()).getBarbarianSpawnModifier()
		
		# Leoreth: buff certain cities if independent / barbarian (imported from SoI)
		if iGameTurn % 20 == 10:
			for tMinorState in tMinorStates:
				iStartYear, iEndYear, tPlot, lUnitList = tMinorState
				if utils.isYearIn(iStartYear, iEndYear):
					x, y = tPlot
					plot = gc.getMap().plot(x, y)
					iOwner = plot.getOwner()
					if plot.isCity() and plot.getNumUnits() < 4 and iOwner >= iNumPlayers:
						iUnit = utils.getRandomEntry(lUnitList)
						utils.makeUnit(iUnit, iOwner, tPlot, 1)

		if utils.isYearIn(-3000, -850):
			if iHandicap >= 0:
				self.checkSpawn(iBarbarian, iWarrior, 1, (92, 53), (116, 62), self.spawnMinors, iGameTurn, 5, 0)
			
			self.checkSpawn(iBarbarian, iWolf, 1, (89, 66), (125, 75), self.spawnNatives, iGameTurn, 5, 2)
			self.checkSpawn(iBarbarian, iBear, 1, (89, 66), (125, 75), self.spawnNatives, iGameTurn, 5, 4)
			self.checkSpawn(iBarbarian, iLion, 1, (67, 12), (84, 34), self.spawnNatives, iGameTurn, 4, 1)
			self.checkSpawn(iBarbarian, iPanther, 1, (67, 12), (84, 34), self.spawnNatives, iGameTurn, 4, 3)

		#celts
		if utils.isYearIn(-650, -110):
			self.checkSpawn(iCeltia, iGallicWarrior, 1, (57, 56), (76, 61), self.spawnMinors, iGameTurn, 6, 0)
			if iHandicap >= 0:
				self.checkSpawn(iCeltia, iAxeman, 1, (57, 56), (76, 61), self.spawnMinors, iGameTurn, 8, 5, ["TXT_KEY_ADJECTIVE_GAUL"])

		#norse
		if utils.isYearIn(-650, 550):
			self.checkSpawn(iBarbarian, iGalley, 1, (55, 59), (66, 68), self.spawnPirates, iGameTurn, 20, 0, ["TXT_KEY_ADJECTIVE_NORSE"])
			
		#mongolia
		if utils.isYearIn(-210, 300):
			self.checkSpawn(iBarbarian, iHorseArcher, 3 + iHandicap, (110, 58), (129, 65), self.spawnNomads, iGameTurn, 8-iHandicap, 0, ["TXT_KEY_ADJECTIVE_XIONGNU"])
		elif utils.isYearIn(300, 900):
			iNumUnits = 2 + iHandicap
			self.checkSpawn(iBarbarian, iHorseArcher, iNumUnits, (110, 58), (129, 65), self.spawnNomads, iGameTurn, 7-iHandicap, 0, ["TXT_KEY_ADJECTIVE_GOKTURK", "TXT_KEY_ADJECTIVE_UIGHUR"])
		elif utils.isYearIn(900, 1100):
			iNumUnits = 2 + iHandicap
			self.checkSpawn(iBarbarian, iKeshik, iNumUnits, (110, 58), (129, 65), self.spawnInvaders, iGameTurn, 6, 0, ["TXT_KEY_ADJECTIVE_JURCHEN", "TXT_KEY_ADJECTIVE_KHITAN"])
			
		#tibet
		if utils.isYearIn(-350, 200):
			self.checkSpawn(iBarbarian, iLightSwordsman, 1 + iHandicap, (107, 48), (116, 52), self.spawnMinors, iGameTurn, 10-iHandicap, 3, ["TXT_KEY_ADJECTIVE_TIBETAN"])
		elif utils.isYearIn(200, 1100):
			self.checkSpawn(iBarbarian, iSwordsman, 1 + iHandicap, (107, 48), (116, 52), self.spawnMinors, iGameTurn, 10-iHandicap, 3, ["TXT_KEY_ADJECTIVE_TIBETAN"])

		# Deccan barbarians
		if utils.isYearIn(-1000, 1200):
			iUnit = iArcher
			iStrength = iHandicap
			if iGameTurn >= getTurnForYear(-500): iUnit = iAxeman
			if iGameTurn >= getTurnForYear(0): iStrength += 1
			if iGameTurn >= getTurnForYear(200): iUnit = iSwordsman
			
			self.checkSpawn(iBarbarian, iUnit, iStrength, (101, 31), (111, 42), self.spawnInvaders, iGameTurn, 8-iHandicap, 0, ["Hindi"])
			
		# elephants in india pre-khmer
		if utils.isYearIn(-210, 700):
			self.checkSpawn(iBarbarian, iWarElephant, 1, (103, 35), (117, 45), self.spawnInvaders, iGameTurn, 8-iHandicap, 4)

		#Indo-Scythians
		if utils.isYearIn(-200, 400):
			self.checkSpawn(iBarbarian, iHorseman, 2, (97, 47), (104, 51), self.spawnNomads, iGameTurn, 8-iHandicap, 4, ["TXT_KEY_ADJECTIVE_INDO_SCYTHIAN"])

		#Kushana
		if utils.isYearIn(30, 220):
			self.checkSpawn(iBarbarian, iAsvaka, 3+iHandicap, (97, 47), (104, 51), self.spawnInvaders, iGameTurn, 8, 3, ["TXT_KEY_ADJECTIVE_KUSHANA"])

		#Hephtalites
		if utils.isYearIn(400, 550):
			self.checkSpawn(iBarbarian, iHorseArcher, 2+iHandicap, (97, 47), (104, 51), self.spawnInvaders, iGameTurn, 5-iHandicap, 2, ["TXT_KEY_ADJECTIVE_HEPHTHALITE"])

		# Holkans in classical Mesoamerica
		if utils.isYearIn(100, 600):
			self.checkSpawn(iBarbarian, iHolkan, 1, (15, 36), (27, 44), self.spawnUprising, iGameTurn, 6, 4)
		elif utils.isYearIn(600, 1000):
			self.checkSpawn(iBarbarian, iHolkan, 1, (15, 36), (27, 44), self.spawnUprising, iGameTurn, 4, 2)
			
		#pirates in Mediterranean
		if utils.isYearIn(-210, 50):
			self.checkSpawn(iBarbarian, iWarGalley, 1, (55, 44), (84, 54), self.spawnPirates, iGameTurn, 8, 0)

		#pirates in Barbary coast
		if not gc.getPlayer(iMoors).isAlive():
			if utils.isYearIn(-50, 700):
				self.checkSpawn(iBarbarian, iWarGalley, 1, (52, 41), (72, 49), self.spawnPirates, iGameTurn, 18, 0)
			elif utils.isYearIn(700, 1400):
				self.checkSpawn(iBarbarian, iWarGalley, 1, (52, 41), (72, 49), self.spawnPirates, iGameTurn, 8, 0)
		#pirates in Indian ocean
		if utils.isYearIn(-650, 700):
			self.checkSpawn(iBarbarian, iWarGalley, 1, (84, 24), (106, 42), self.spawnPirates, iGameTurn, 18, 0)
		elif utils.isYearIn(700, 1700):
			self.checkSpawn(iBarbarian, iHeavyGalley, 1, (84, 24), (106, 42), self.spawnPirates, iGameTurn, 10, 0)

		# Leoreth: Barbarians in Anatolia (Hittites), replace Hattusas spawn
		if utils.isYearIn(-2000, -800):
			self.checkSpawn(iBarbarian, iHuluganni, 1 + iHandicap, (81, 51), (86, 55), self.spawnInvaders, iGameTurn, 16, 0, ["TXT_KEY_ADJECTIVE_HITTITE"])

		#barbarians in europe
		if utils.isYearIn(-210, 470):
			self.checkSpawn(iBarbarian, iAxeman, 3 + iHandicap, (57, 55), (74, 61), self.spawnInvaders, iGameTurn, 10, 0, ["TXT_KEY_ADJECTIVE_GERMANIC"])
			self.checkSpawn(iBarbarian, iAxeman, 2 + iHandicap, (74, 58), (81, 66), self.spawnInvaders, iGameTurn, 12, 2, ["TXT_KEY_ADJECTIVE_GERMANIC"])
		# Leoreth: begins 100 AD instead of 50 AD
		if utils.isYearIn(100, 470):
			self.checkSpawn(iBarbarian, iSwordsman, 3, (66, 55), (82, 66), self.spawnInvaders, iGameTurn, 8, 5, ["TXT_KEY_ADJECTIVE_GERMANIC"])
		if utils.isYearIn(300, 550):
			self.checkSpawn(iBarbarian, iAxeman, 4 + iHandicap, (55, 49), (63, 61), self.spawnInvaders, iGameTurn, 5, 4, ["TXT_KEY_ADJECTIVE_VISIGOTHIC"])
			self.checkSpawn(iBarbarian, iSwordsman, 4 + iHandicap, (55, 49), (63, 61), self.spawnInvaders, iGameTurn, 5, 2, ["TXT_KEY_ADJECTIVE_VISIGOTHIC"])
			self.checkSpawn(iBarbarian, iHorseArcher, 3, (62, 58), (76, 64), self.spawnInvaders, iGameTurn, 5, 0, ["TXT_KEY_ADJECTIVE_HUNNIC"])
		if utils.isYearIn(300, 700):
			self.checkSpawn(iBarbarian, iHorseArcher, 3 + iHandicap, (65, 60), (106, 63), self.spawnInvaders, iGameTurn, 3, 2, ["TXT_KEY_ADJECTIVE_HUNNIC"])

		#Leoreth: barbarians in Balkans / Black Sea until the High Middle Ages (Bulgarians, Cumans, Pechenegs)
		if utils.isYearIn(680, 1000):
			self.checkSpawn(iBarbarian, iHorseArcher, 3 + iHandicap, (73, 55), (81, 60), self.spawnInvaders, iGameTurn, 6, 2, ["TXT_KEY_ADJECTIVE_AVAR", "TXT_KEY_ADJECTIVE_BULGAR"])
		if utils.isYearIn(900, 1200):
			self.checkSpawn(iBarbarian, iHorseArcher, 3 + iHandicap, (79, 58), (92, 61), self.spawnInvaders, iGameTurn, 8, 5, ["TXT_KEY_ADJECTIVE_CUMAN"])

		#barbarians in central asia
		if utils.isYearIn(-1600, -850):
			self.checkLimitedSpawn(iBarbarian, iVulture, 1, 3, (74, 34), (78, 44), self.spawnNomads, iGameTurn, 8-iHandicap, 2, ["TXT_KEY_ADJECTIVE_ASSYRIAN"])
		elif utils.isYearIn(-850, 600):
			self.checkSpawn(iBarbarian, iHorseman, 2 + iHandicap, (92, 49), (98, 59), self.spawnInvaders, iGameTurn, 7-iHandicap, 2, ["TXT_KEY_ADJECTIVE_PARTHIAN"])
		elif utils.isYearIn(600, 900):
			#if utils.getScenario() == i3000BC:  #late start condition
			self.checkSpawn(iBarbarian, iOghuz, 2 + iHandicap, (91, 50), (103, 58), self.spawnNomads, iGameTurn, 8-iHandicap, 2, ["TXT_KEY_ADJECTIVE_TURKIC"])
		elif utils.isYearIn(900, 1040):
			#if utils.getScenario() == i3000BC:  #late start condition
			self.checkSpawn(iBarbarian, iOghuz, 2 + iHandicap, (91, 50), (106, 62), self.spawnNomads, iGameTurn, 6-iHandicap, 2, ["TXT_KEY_ADJECTIVE_TURKIC"])

		# late Central Asian barbarians
		if utils.isYearIn(1200, 1600):
			if not utils.getAreaCitiesCiv(iMongolia, utils.getPlotList((82, 58), (95, 70))):
				self.checkSpawn(iBarbarian, iKeshik, 1 + iHandicap, (88, 57), (94, 61), self.spawnNomads, iGameTurn, 10-iHandicap, 5, ["TXT_KEY_ADJECTIVE_TATAR", "TXT_KEY_ADJECTIVE_NOGAI"])
		if utils.isYearIn(1400, 1700):
			if utils.getAreaCities(utils.getPlotList((91, 58), (106, 62))):
				self.checkSpawn(iBarbarian, iKeshik, 1 + iHandicap, (91, 58), (106, 62), self.spawnNomads, iGameTurn, 10-2*iHandicap, 2, ["TXT_KEY_ADJECTIVE_UZBEK", "TXT_KEY_ADJECTIVE_KAZAKH"])
	
		#barbarians in Elam
		if utils.isYearIn(-1600, -1000):
			self.checkSpawn(iBarbarian, iChariot, 1, (92, 43), (99, 50), self.spawnMinors, iGameTurn, 9-iHandicap, 0, ["TXT_KEY_ADJECTIVE_ELAMITE"])

		#barbarians in north africa
		if utils.isYearIn(-210, 50):
			self.checkSpawn(iBarbarian, iNumidianCavalry, 1, (60, 38), (78, 42), self.spawnNomads, iGameTurn, 9-iHandicap, 3, ["TXT_KEY_ADJECTIVE_BERBER"])
		elif utils.isYearIn(50, 900):
			if utils.getScenario() == i3000BC:  #late start condition
				self.checkSpawn(iBarbarian, iNumidianCavalry, 1 + iHandicap, (60, 38), (78, 42), self.spawnNomads, iGameTurn, 10-iHandicap, 5, ["TXT_KEY_ADJECTIVE_BERBER"])
		elif utils.isYearIn(900, 1800):
			self.checkSpawn(iBarbarian, iCamelArcher, 1, (60, 33), (78, 42), self.spawnNomads, iGameTurn, 10-iHandicap, 4, ["TXT_KEY_ADJECTIVE_BERBER"])
			
		#camels in arabia
		if utils.isYearIn(190, 550):
			self.checkSpawn(iBarbarian, iCamelArcher, 1, (85, 36), (96, 42), self.spawnNomads, iGameTurn, 9-iHandicap, 7, ["TXT_KEY_ADJECTIVE_BEDOUIN"])
		if utils.isYearIn(-800, 1300) and self.includesActiveHuman([iEgypt, iArabia]):
			iNumUnits = iHandicap
			if utils.getScenario() == i3000BC: iNumUnits += 1
			self.checkSpawn(iBarbarian, iMedjay, iNumUnits, (78, 33), (82, 41), self.spawnUprising, iGameTurn, 12, 4, ["TXT_KEY_ADJECTIVE_NUBIAN"])
		if utils.isYearIn(450, 1600):
			if utils.getScenario() == i3000BC:
				self.checkSpawn(iNative, iImpi, 2 + iHandicap, (68, 12), (85, 31), self.spawnNatives, iGameTurn, 10, 4)
			else:
				self.checkSpawn(iNative, iImpi, 2 + iHandicap, (68, 12), (85, 31), self.spawnNatives, iGameTurn, 15, 4)
		elif utils.isYearIn(1600, 1800):
			self.checkSpawn(iNative, iPombos, 2 + iHandicap, (68, 12), (85, 31), self.spawnNatives, iGameTurn, 10, 4)
			
		#west africa
		if utils.isYearIn(450, 1700):
			if iGameTurn < getTurnForYear(1300):
				sAdj = ["TXT_KEY_ADJECTIVE_GHANAIAN"]
			else:
				sAdj = ["TXT_KEY_ADJECTIVE_SONGHAI"]
			self.checkSpawn(iNative, iImpi, 2, (55, 28), (70, 34), self.spawnMinors, iGameTurn, 16, 10, sAdj)
			
		if utils.isYearIn(1200, 1700):
			self.checkSpawn(iBarbarian, iFarari, 1, (54, 31), (76, 43), self.spawnMinors, iGameTurn, 16, 4, sAdj)

		#American natives
		if utils.isYearIn(600, 1100):
			self.checkSpawn(iNative, iDogSoldier, 1 + iHandicap, (15, 38), (24, 47), self.spawnNatives, iGameTurn, 20, 0)
			if utils.getScenario() == i3000BC:  #late start condition
				self.checkSpawn(iNative, iJaguar, 3, (12, 45), (24, 55), self.spawnNatives, iGameTurn, 16 - 2*iHandicap, 10)
			else:  #late start condition
				self.checkSpawn(iNative, iJaguar, 2, (12, 45), (24, 55), self.spawnNatives, iGameTurn, 16 - 2*iHandicap, 10)
		if utils.isYearIn(1300, 1600):
			self.checkSpawn(iNative, iDogSoldier, 2 + iHandicap, (12, 45), (24, 55), self.spawnNatives, iGameTurn, 8, 0)
		if utils.isYearIn(1400, 1800):
			self.checkSpawn(iNative, iDogSoldier, 1 + iHandicap, (8, 50), (34, 60), self.spawnUprising, iGameTurn, 12, 0)
			self.checkSpawn(iNative, iDogSoldier, 1 + iHandicap, (8, 50), (34, 60), self.spawnUprising, iGameTurn, 12, 6)
		if utils.isYearIn(1300, 1600):
			if iGameTurn % 18 == 0:
				if not gc.getMap().plot(29, 34).isUnit():
					utils.makeUnitAI(iDogSoldier, iNative, (29, 34), UnitAITypes.UNITAI_ATTACK, 2 + iHandicap)
			elif iGameTurn % 18 == 9:
				if not gc.getMap().plot(30, 13).isUnit():
					utils.makeUnitAI(iDogSoldier, iNative, (33, 12), UnitAITypes.UNITAI_ATTACK, 2 + iHandicap)
		
		if self.includesActiveHuman([iAmerica, iEngland, iFrance]):
			if utils.isYearIn(1700, 1900):
				self.checkSpawn(iNative, iMountedBrave, 1 + iHandicap, (14, 52), (23, 62), self.spawnNomads, iGameTurn, 12 - iHandicap, 2)
			
			if utils.isYearIn(1500, 1850):
				self.checkSpawn(iNative, iMohawk, 1, (24, 54), (31, 61), self.spawnUprising, iGameTurn, 8, 4)
				
		#pirates in the Caribbean
		if utils.isYearIn(1600, 1800):
			self.checkSpawn(iNative, iPrivateer, 1, (25, 37), (38, 53), self.spawnPirates, iGameTurn, 5, 0)
		#pirates in Asia
		if utils.isYearIn(1500, 1900):
			self.checkSpawn(iNative, iPrivateer, 1, (83, 24), (133, 42), self.spawnPirates, iGameTurn, 8, 0)

		if iGameTurn < getTurnForYear(tMinorCities[len(tMinorCities)-1][0])+10:
			self.foundMinorCities(iGameTurn)

		if iGameTurn == getTurnForYear(tBirth[iInca]):
			if utils.getHumanID() == iInca:
				utils.makeUnit(iAucac, iNative, (27, 28), 1)
				utils.makeUnit(iAucac, iNative, (28, 25), 1)
				
	def foundMinorCities(self, iGameTurn):
		for i in range(len(tMinorCities)):
			iYear, tPlot, iPlayer, sName, iPopulation, iUnitType, iNumUnits = tMinorCities[i]
			if iGameTurn < getTurnForYear(iYear): return
			if iGameTurn > getTurnForYear(iYear)+10: continue
			
			if data.lMinorCityFounded[i]: continue
			
			x, y = tPlot
			plot = gc.getMap().plot(x, y)
			if plot.isCity(): continue
			
			# special cases
			if not self.canFoundCity(sName): continue
			
			lReligions = []
			bForceSpawn = False
			
			if sName == 'Kyiv': lReligions = [iOrthodoxy, iCatholicism]
			if sName == 'Kilwa': lReligions = [iIslam]
			if iPlayer == iCeltia and utils.getScenario() != i3000BC: iPlayer = iIndependent
			if sName == 'Buda': bForceSpawn = True
			
			if not self.isFreePlot(tPlot, bForceSpawn): continue
			
			utils.evacuate(tPlot)
		
			if self.foundCity(iPlayer, tPlot, sName, iPopulation, iUnitType, iNumUnits, lReligions):
				data.lMinorCityFounded[i] = True
		
	def canFoundCity(self, sName):
		if sName == 'Kanchipuram' and utils.getHumanID() == iTamils: return False
		elif sName == 'Tanjapuri' and gc.getPlayer(iTamils).isAlive(): return False
		elif sName == 'Zhongdu' and utils.getHumanID() == iChina: return False
		elif sName == 'Hamburg' and (utils.getHumanID() == iHolyRome or data.iSeed % 4 == 0): return False
		elif sName == 'L&#252;beck' and (utils.getHumanID() == iHolyRome or data.iSeed % 4 != 0): return False
		elif sName == 'Rasa' and gc.getPlayer(iTibet).isAlive(): return False
		#elif sName == 'Marrakus' and utils.getScenario() != i3000BC: return False
		
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
					
	def clearUnits(self, iPlayer, tPlot): # Unused
		lHumanUnits = []
		lOtherUnits = []
	
		for (x, y) in utils.surroundingPlots(tPlot):
			plot = gc.getMap().plot(x, y)
			
			for iUnit in range(plot.getNumUnits()):
				unit = plot.getUnit(iUnit)
				
				if unit.getOwner() == utils.getHumanID():
					lHumanUnits.append(unit)
				else:
					lOtherUnits.append(unit)
						
		capital = gc.getPlayer(utils.getHumanID()).getCapitalCity()
		for unit in lHumanUnits:
			unit.setXY(capital.getX(), capital.getY(), False, True, False)
			
		for unit in lOtherUnits:
			utils.makeUnit(unit.getUnitType(), iPlayer, tPlot, 1)
			unit.kill(False, iBarbarian)
				
	def isFreePlot(self, tPlot, bIgnoreCulture = False):
		x, y = tPlot
		plot = gc.getMap().plot(x, y)
		
		# no cultural control over the tile
		if plot.isOwned() and plot.getOwner() < iNumPlayers and not bIgnoreCulture:
			return False
				
		# no city in adjacent tiles
		for (i, j) in utils.surroundingPlots(tPlot):
			currentPlot = gc.getMap().plot(i, j)
			if currentPlot.isCity(): return False
						
		return True
			
	def checkRegion(self, tCity): # Unusued
		cityPlot = gc.getMap().plot(tCity[0], tCity[1])
		iNumUnitsInAPlot = cityPlot.getNumUnits()
##		print iNumUnitsInAPlot
		
		#checks if the plot already belongs to someone
		if cityPlot.isOwned():
			if cityPlot.getOwner() != iBarbarian:
				return (False, -1)
		
##		#checks if there's a unit on the plot
		if iNumUnitsInAPlot > 0:
			for i in range(iNumUnitsInAPlot):
				unit = cityPlot.getUnit(i)
				iOwner = unit.getOwner()
				if iOwner == iBarbarian:
					return (False, tCity[3]+1)

		#checks the surroundings and allows only AI units
		for (x, y) in utils.surroundingPlots(tCity[0], tCity[1]):
			currentPlot=gc.getMap().plot(x,y)
			if currentPlot.isCity():
				return (False, -1)
			iNumUnitsInAPlot = currentPlot.getNumUnits()
			if iNumUnitsInAPlot > 0:
				for i in range(iNumUnitsInAPlot):
					unit = currentPlot.getUnit(i)
					iOwner = unit.getOwner()
					pOwner = gc.getPlayer(iOwner)
					if pOwner.isHuman():
						return (False, tCity[3]+1)
		return (True, tCity[3])



	def killNeighbours(self, tCoords): # Unused
		'Kills all units in the neigbbouring tiles of plot (as well as plot itself) so late starters have some space.'
		for (x, y) in utils.surroundingPlots(tCoords):
			killPlot = CyMap().getPlot(x, y)
			for i in range(killPlot.getNumUnits()):
				unit = killPlot.getUnit(0)	# 0 instead of i because killing units changes the indices
				unit.kill(False, iBarbarian)
				
	# Leoreth: check region for number of units first
	def checkLimitedSpawn(self, iPlayer, iUnitType, iNumUnits, iMaxUnits, tTL, tBR, spawnFunction, iTurn, iPeriod, iRest, lAdj=[]):
		if iTurn % utils.getTurns(iPeriod) == iRest:
			lAreaUnits = utils.getAreaUnits(iPlayer, tTL, tBR)
			if len(lAreaUnits) < iMaxUnits:
				self.checkSpawn(iPlayer, iUnitType, iNumUnits, tTL, tBR, spawnFunction, iTurn, iPeriod, iRest, lAdj)
						
	# Leoreth: new ways to spawn barbarians
	def checkSpawn(self, iPlayer, iUnitType, iNumUnits, tTL, tBR, spawnFunction, iTurn, iPeriod, iRest, lAdj=[]):
		if len(lAdj) == 0:
			sAdj = ""
		else:
			sAdj = utils.getRandomEntry(lAdj)
	
		if iTurn % utils.getTurns(iPeriod) == iRest:
			spawnFunction(iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj)
			
	def possibleTiles(self, tTL, tBR, bWater=False, bTerritory=False, bBorder=False, bImpassable=False, bNearCity=False):
		return [tPlot for tPlot in utils.getPlotList(tTL, tBR) if self.possibleTile(tPlot, bWater, bTerritory, bBorder, bImpassable, bNearCity)]
		
	def possibleTile(self, tPlot, bWater, bTerritory, bBorder, bImpassable, bNearCity):
		x, y = tPlot
		plot = gc.getMap().plot(x, y)
		lSurrounding = utils.surroundingPlots(tPlot)
		
		# never on peaks
		if plot.isPeak(): return False
		
		# only land or water
		if bWater != plot.isWater(): return False
		
		# only inside territory if specified
		if not bTerritory and plot.getOwner() >= 0: return False
		
		# never directly next to cities
		if [(i, j) for (i, j) in lSurrounding if gc.getMap().plot(i, j).isCity()]: return False
		
		# never on tiles with units
		if plot.isUnit(): return False
		
		# never in marsh (impassable)
		if plot.getFeatureType() == iMarsh: return False
		
		# allow other impassable terrain (ocean, jungle)
		if not bImpassable:
			if plot.getTerrainType() == iOcean: return False
			if plot.getFeatureType() == iJungle: return False
		
		# restrict to borders if specified
		if bBorder and not [(i, j) for (i, j) in lSurrounding if gc.getMap().plot(i, j).getOwner() != plot.getOwner()]: return False
		
		# near a city if specified (next to cities excluded above)
		if bNearCity and not [(i, j) for (i, j) in utils.surroundingPlots(tPlot, 2, lambda (a, b): not gc.getMap().plot(a, b).isCity())]: return False
		
		# not on landmasses without cities
		if not bWater and gc.getMap().getArea(plot.getArea()).getNumCities() == 0: return False
		
		return True

	def spawnPirates(self, iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
		'''Leoreth: spawns all ships at the same coastal spot, out to pillage and disrupt trade, can spawn inside borders'''
		
		lPlots = self.possibleTiles(tTL, tBR, bWater=True, bTerritory=False)
		tPlot = utils.getRandomEntry(lPlots)
		
		if tPlot:
			utils.makeUnitAI(iUnitType, iPlayer, tPlot, UnitAITypes.UNITAI_PIRATE_SEA, iNumUnits, sAdj)
		
	def spawnNatives(self, iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
		'''Leoreth: outside of territory, in jungles, all dispersed on several plots, out to pillage'''
		
		lPlots = self.possibleTiles(tTL, tBR, bTerritory=False, bImpassable=True)
		
		for i in range(iNumUnits):
			tPlot = utils.getRandomEntry(lPlots)
			if not tPlot: break
			
			lPlots.remove(tPlot)
			utils.makeUnitAI(iUnitType, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK, 1, sAdj)
			
	def spawnMinors(self, iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
		'''Leoreth: represents minor states without ingame cities
			    outside of territory, not in jungles, in groups, passive'''
			    
		lPlots = self.possibleTiles(tTL, tBR, bTerritory=False)
		tPlot = utils.getRandomEntry(lPlots)
		
		if tPlot:
			utils.makeUnitAI(iUnitType, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK, iNumUnits, sAdj)
		
	def spawnNomads(self, iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
		'''Leoreth: represents aggressive steppe nomads etc.
			    outside of territory, not in jungles, in small groups, target cities'''
		
		lPlots = self.possibleTiles(tTL, tBR, bTerritory=False)
		tPlot = utils.getRandomEntry(lPlots)
		
		if tPlot:
			utils.makeUnitAI(iUnitType, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK, iNumUnits, sAdj)
			
	def spawnInvaders(self, iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
		'''Leoreth: represents large invasion forces and migration movements
			    inside of territory, not in jungles, in groups, target cities'''
			    
		lPlots = self.possibleTiles(tTL, tBR, bTerritory=True, bBorder=True)
		tPlot = utils.getRandomEntry(lPlots)
		
		if tPlot:
			utils.makeUnitAI(iUnitType, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK, iNumUnits, sAdj)
			
	def spawnUprising(self, iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
		''' Leoreth: represents uprisings of Natives against colonial settlements, especially North America
			     spawns units in a free plot in the second ring of a random target city in the area
			     (also used for units from warring city states in classical Mesoamerica)'''
		
		lPlots = self.possibleTiles(tTL, tBR, bTerritory=True, bNearCity=True)
		tPlot = utils.getRandomEntry(lPlots)
		
		if tPlot:
			utils.makeUnitAI(iUnitType, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK, iNumUnits, sAdj)
			
	def includesActiveHuman(self, lPlayers):
		return utils.getHumanID() in lPlayers and tBirth[utils.getHumanID()] <= gc.getGame().getGameTurnYear()