# Rhye's and Fall of Civilization - Barbarian units and cities

from CvPythonExtensions import *
import CvUtil
import PyHelpers	# LOQ
#import Popup
#import cPickle as pickle
from RFCUtils import utils
from Consts import *
from StoredData import data
import Stability as sta

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer	# LOQ

# Spawning cities (Leoreth)
# Year, coordinates, owner, name, population, unit type, unit number, religions, forced spawn
tMinorCities = (
(-3000, (73, 38), iIndependent, 'Yerushalayim', 2, iArcher, 3),	# Jerusalem
(-3000, (79, 40), iIndependent2, 'Shushan', 1, iArcher, 1),		# Susa
(-2000, (85, 47), iIndependent, 'Afrasiyab', 1, iArcher, 1),	# Samarkand
(-1600, (90, 40), iIndependent, 'Indraprastha', 1, iMilitia, 1),	# Delhi
(-1000, (102, 47), iIndependent, 'Zhongdu', 2, iSpearman, 1),	# Beijing
(-1000, (72, 44), iIndependent, 'Ankuwash', 2, iArcher, 2),		# Ankara
(-400, (19, 35), iNative, 'Danibaan', 2, iHolkan, 2),	# Monte Alb�n
(-325, (92, 33), iIndependent, 'Kanchipuram', 2, iArcher, 1),	# Madras
(-300, (105, 49), iBarbarian, 'Simiyan hoton', 2, iChariot, 2),	# Shenyang
(-300, (91, 31), iIndependent, 'Tanjapuri', 1, iWarElephant, 1),	# Thanjavur
(-250, (19, 35), iNative, 'Danibaan', 2, iHolkan, 1),	# Monte Alb�n
(-190, (77, 44), iIndependent2, 'Artashat', 1, -1, -1),			# Artaxata
(-100, (95, 47), iBarbarian, 'Dunhuang', 2, iArcher, 1),		# Dunhuang
(-75, (89, 46), iBarbarian, 'Kashgar', 2, iArcher, 1),		# Kashgar
(100, (76, 30), iIndependent, "Sana'a", 2, iArcher, 2),			# Sana'a
(107, (99, 38), iIndependent2, 'Pagan', 2, -1, -1),			# Pagan
(200, (75, 28), iIndependent2, 'Barbara', 2, iArcher, 2),	# Berbera
(633, (96, 43), iBarbarian, 'Rasa', 2, iKhampa, 1),		# Lhasa
(680, (51, 37), iIndependent, 'Marrakus', 1, iCrossbowman, 1),	# Marrakesh
(800, tVienna, iIndependent, 'Vindobona', 1, iCrossbowman, 1),	# Wien
(830, (59, 54), iIndependent, 'Hamburg', 2, iCrossbowman, 1),	# Hamburg
(830, (60, 54), iIndependent, 'L&#252;beck', 2, iCrossbowman, 1),	# L�beck
(840, (52, 59), iIndependent2, 'D&#249;n &#200;ideann', 1, iCrossbowman, 2),			# Edinburgh
(866, (101, 37), iBarbarian, 'Hanoi', 2, -1, -1),			# Hanoi
(899, (78, 36), iIndependent, 'Bahrein', 2, iArcher, 2),			# Qarmatians (Abu Sa'id al-Jannabi)
(900, (24, 28), iNative, 'Tucume', 2, iPictaAucac, 2),			# Tucume
(900, (74, 25), iIndependent, 'Muqdisho', 3, iCrossbowman, 2),	# Mogadishu
(990, (49, 56), iIndependent, '&#193;th Cliath', 1, iArcher, 2),			# Dublin
(1000, (61, 63), iIndependent2, 'Nidaros', 1, iHuscarl, 1),	# Trondheim
(1000, (71, 17), iNative, 'Quelimane', 1, iImpi, 1),		# Quelimane
(1100, (71, 20), iNative, 'Mombasa', 1, iImpi, 1),		# Mombasa
(1200, (77, 55), iBarbarian, 'Qazan', 2, iHorseArcher, 1),		# Kazan
(1400, (104, 33), iIndependent, 'Saigon', 5, iCrossbowman, 3),	# Saigon
(1483, (62, 20), iNative, 'Mbanza Kongo', 1, iPombos, 1),	# Mbanza Kongo
)

# do some research on dates here
tMinorStates = (
	(633, 1400, (96, 43), [iArcher, iSwordsman]),	# Tibet
	(-75, 600, (89, 46), [iHorseman]),		# Kashgar early
	(600, 1600, (89, 46), [iHorseArcher]),		# Kashgar late
	(-75, 600, (85, 47), [iHorseman]),		# Samarkand early
	(600, 1600, (85, 47), [iHorseArcher]),		# Samarkand late
	(-300, 600, (91, 31), [iArcher, iSwordsman, iWarElephant]), # Chola
	(-300, 600, (92, 33), [iArcher, iSwordsman, iWarElephant]), # Chola
	(-300, 900, (105, 49), [iHorseArcher, iSwordsman]), # Jurchen
	(1100, 1500, (60, 44), [iPikeman, iCrossbowman]), # Rome late
	(0, 1100, (60, 44), [iSpearman, iArcher]), # Rome early
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

		if utils.isYearIn(-100, 1600):
			# Brown Bear in Chukchi
			self.checkLimitedSpawn(iBarbarian, iBear, 1, 5, (115, 53), (123, 64), self.spawnBears, iGameTurn, 10, 1)
			# Brown Bear and American Black Bear in Alaska and Western Canada
			self.checkLimitedSpawn(iBarbarian, iBear, 1, 5,  (3, 58), (20, 67), self.spawnBears, iGameTurn, 5, 3)
			# Polar Bear in Greenland and Eastern Canada
			self.checkLimitedSpawn(iBarbarian, iPolarBear, 1, 5, (21, 53), (44, 67), self.spawnBears, iGameTurn, 5, 5)

		if utils.isYearIn(-3000, -850):
			if iHandicap >= 0:
				self.checkSpawn(iBarbarian, iWarrior, 1, (76, 46), (99, 53), self.spawnMinors, iGameTurn, 5, 0)
			
			# Wolves and Brown Bears in Russia and Siberia
			self.checkSpawn(iBarbarian, iWolf, 1, (75, 54), (104, 64), self.spawnNatives, iGameTurn, 5, 2)
			self.checkSpawn(iBarbarian, iBear, 1, (75, 54), (104, 64), self.spawnNatives, iGameTurn, 5, 4)
			
			# Panthers, Hyenas, and Lions in South Africa
			self.checkLimitedSpawn(iBarbarian, iLion, 1, 5, (60, 10), (72, 28), self.spawnNatives, iGameTurn, 5, 1)
			self.checkLimitedSpawn(iBarbarian, iPanther, 1, 5, (60, 10), (72, 28), self.spawnNatives, iGameTurn, 5, 3)
			self.checkLimitedSpawn(iBarbarian, iHyena, 1, 5, (60, 10), (72, 28), self.spawnNatives, iGameTurn, 5, 3)
			
			# Panthers and Tigers in India, South China, Indochina, and Indonesia
			self.checkLimitedSpawn(iBarbarian, iPanther, 1, 5, (88, 24), (107, 41), self.spawnNatives, iGameTurn, 5, 1)
			self.checkLimitedSpawn(iBarbarian, iTiger, 1, 5, (88, 24), (107, 41), self.spawnNatives, iGameTurn, 5, 1)
			
			#Asian Black Bears in China, Japan, Manchuria, Vietnam, and Korea
			self.checkLimitedSpawn(iBarbarian, iBear, 1, 5, (100, 36), (116, 56), self.spawnNatives, iGameTurn, 5, 3)
			
			# Jaguars in Brazil, Colombia, and Mesoamerica
			self.checkLimitedSpawn(iBarbarian, iJaguarAnimal, 1, 5, (32, 14), (43, 31), self.spawnNatives, iGameTurn, 5, 1)
			self.checkLimitedSpawn(iBarbarian, iJaguarAnimal, 1, 5, (29, 21), (33, 32), self.spawnNatives, iGameTurn, 5, 3)
			self.checkLimitedSpawn(iBarbarian, iJaguarAnimal, 1, 5, (15, 31), (24, 41), self.spawnNatives, iGameTurn, 5, 3)

			
		#celts
		#if utils.isYearIn(-650, -110):
		#	self.checkSpawn(iCeltia, iGallicWarrior, 1, (49, 46), (65, 52), self.spawnMinors, iGameTurn, 6, 0)
		#	if iHandicap >= 0:
		#		self.checkSpawn(iCeltia, iAxeman, 1, (49, 46), (65, 52), self.spawnMinors, iGameTurn, 8, 5, ["TXT_KEY_ADJECTIVE_GAUL"])

		#norse
		if utils.isYearIn(-650, 550):
			self.checkSpawn(iBarbarian, iGalley, 1, (50, 49), (61, 55), self.spawnPirates, iGameTurn, 20, 0, ["TXT_KEY_ADJECTIVE_NORSE"])
			
		#mongolia
		if utils.isYearIn(-210, 400):
			self.checkSpawn(iBarbarian, iHorseArcher, 3 + iHandicap, (94, 48), (107, 54), self.spawnNomads, iGameTurn, 7-iHandicap, 0, ["TXT_KEY_ADJECTIVE_XIONGNU"])
		elif utils.isYearIn(400, 900):
			iNumUnits = 3 + iHandicap
			self.checkSpawn(iBarbarian, iHorseArcher, iNumUnits, (91, 50), (107, 54), self.spawnNomads, iGameTurn, 6-iHandicap, 0, ["TXT_KEY_ADJECTIVE_GOKTURK", "TXT_KEY_ADJECTIVE_UIGHUR"])
		elif utils.isYearIn(900, 1100):
			iNumUnits = 3 + iHandicap
			self.checkSpawn(iBarbarian, iKeshik, iNumUnits, (94, 48), (107, 54), self.spawnInvaders, iGameTurn, 6, 0, ["TXT_KEY_ADJECTIVE_JURCHEN", "TXT_KEY_ADJECTIVE_KHITAN"])
			
		#tibet
		if utils.isYearIn(-350, 200):
			self.checkSpawn(iBarbarian, iLightSwordsman, 1 + iHandicap, (92, 41), (99, 45), self.spawnMinors, iGameTurn, 10-iHandicap, 3, ["TXT_KEY_ADJECTIVE_TIBETAN"])
		elif utils.isYearIn(200, 1100):
			self.checkSpawn(iBarbarian, iSwordsman, 1 + iHandicap, (92, 41), (99, 45), self.spawnMinors, iGameTurn, 10-iHandicap, 3, ["TXT_KEY_ADJECTIVE_TIBETAN"])

		# Deccan barbarians
		if utils.isYearIn(-1000, 1200):
			iUnit = iArcher
			iStrength = iHandicap
			if iGameTurn >= getTurnForYear(-500): iUnit = iAxeman
			if iGameTurn >= getTurnForYear(0): iStrength += 1
			if iGameTurn >= getTurnForYear(200): iUnit = iSwordsman
			
			self.checkSpawn(iBarbarian, iUnit, iStrength, (87, 23), (96, 37), self.spawnInvaders, iGameTurn, 8-iHandicap, 0, ["Hindi"])
			
		# elephants in india pre-khmer
		if utils.isYearIn(-210, 700):
			self.checkSpawn(iBarbarian, iWarElephant, 1, (86, 31), (100, 41), self.spawnInvaders, iGameTurn, 8-iHandicap, 4)

		#Indo-Scythians
		if utils.isYearIn(-200, 400):
			self.checkSpawn(iBarbarian, iHorseman, 2, (84, 40), (89, 43), self.spawnNomads, iGameTurn, 8-iHandicap, 4, ["TXT_KEY_ADJECTIVE_INDO_SCYTHIAN"])

		#Kushana
		if utils.isYearIn(30, 220):
			self.checkSpawn(iBarbarian, iAsvaka, 3+iHandicap, (84, 40), (89, 43), self.spawnInvaders, iGameTurn, 8, 3, ["TXT_KEY_ADJECTIVE_KUSHANA"])

		#Hephtalites
		if utils.isYearIn(400, 550):
			self.checkSpawn(iBarbarian, iHorseArcher, 2+iHandicap, (84, 40), (89, 43), self.spawnInvaders, iGameTurn, 5-iHandicap, 2, ["TXT_KEY_ADJECTIVE_HEPHTHALITE"])

		# Holkans in classical Mesoamerica
		if utils.isYearIn(-200, 100):
			self.checkSpawn(iBarbarian, iHolkan, 1, (17, 31), (25, 37), self.spawnUprising, iGameTurn, 7, 5)
		if utils.isYearIn(100, 600):
			self.checkSpawn(iBarbarian, iHolkan, 1, (17, 31), (25, 37), self.spawnUprising, iGameTurn, 6, 4)	
		elif utils.isYearIn(600, 1000):
			self.checkSpawn(iBarbarian, iHolkan, 1, (17, 31), (25, 37), self.spawnUprising, iGameTurn, 4, 2)
		
		# Picta Aucacs in pre-Incan Andes
		if utils.isYearIn(800, 1100):
			self.checkSpawn(iBarbarian, iPictaAucac, 1, (-1, -1), (-1, -1), self.spawnUprising, iGameTurn, 4, 2)
		
		# Jaguars in classical Mesoamerica
		if utils.isYearIn(150, 500):
			self.checkSpawn(iBarbarian, iJaguar, 1, (15, 36), (20, 41), self.spawnUprising, iGameTurn, 6, 4)	
		elif utils.isYearIn(500, 1150):
			self.checkSpawn(iBarbarian, iJaguar, 1, (15, 36), (20, 41), self.spawnUprising, iGameTurn, 4, 2)
			
		#pirates in Mediterranean
		if utils.isYearIn(-210, 50):
			self.checkSpawn(iBarbarian, iWarGalley, 1, (49, 37), (72, 44), self.spawnPirates, iGameTurn, 8, 0)
		#pirates in Barbary coast
		if not gc.getPlayer(iMoors).isAlive():
			if utils.isYearIn(-50, 700):
				self.checkSpawn(iBarbarian, iWarGalley, 1, (46, 30), (62, 39), self.spawnPirates, iGameTurn, 18, 0)
			elif utils.isYearIn(700, 1400):
				self.checkSpawn(iBarbarian, iWarGalley, 1, (46, 30), (62, 39), self.spawnPirates, iGameTurn, 8, 0)
		#pirates in Indian ocean
		if utils.isYearIn(-650, 700):
			self.checkSpawn(iBarbarian, iWarGalley, 1, (72, 20), (91, 36), self.spawnPirates, iGameTurn, 18, 0)
		elif utils.isYearIn(700, 1700):
			self.checkSpawn(iBarbarian, iHeavyGalley, 1, (72, 20), (91, 36), self.spawnPirates, iGameTurn, 10, 0)

		# Leoreth: Barbarians in Anatolia (Hittites), replace Hattusas spawn
		if utils.isYearIn(-2000, -800):
			self.checkSpawn(iBarbarian, iHuluganni, 1 + iHandicap, (68, 42), (74, 45), self.spawnInvaders, iGameTurn, 16, 0, ["TXT_KEY_ADJECTIVE_HITTITE"])

		#barbarians in europe
		if utils.isYearIn(-210, 470):
			self.checkSpawn(iBarbarian, iAxeman, 3 + iHandicap, (50, 45), (63, 52), self.spawnInvaders, iGameTurn, 10, 0, ["TXT_KEY_ADJECTIVE_GERMANIC"])
			self.checkSpawn(iBarbarian, iAxeman, 2 + iHandicap, (64, 49), (69, 55), self.spawnInvaders, iGameTurn, 12, 2, ["TXT_KEY_ADJECTIVE_GERMANIC"])
		# Leoreth: begins 100 AD instead of 50 AD
		if utils.isYearIn(100, 470):
			self.checkSpawn(iBarbarian, iSwordsman, 3, (58, 45), (70, 55), self.spawnInvaders, iGameTurn, 8, 5, ["TXT_KEY_ADJECTIVE_GERMANIC"])
		if utils.isYearIn(300, 550):
			self.checkSpawn(iBarbarian, iAxeman, 4 + iHandicap, (49, 41), (56, 52), self.spawnInvaders, iGameTurn, 5, 4, ["TXT_KEY_ADJECTIVE_VISIGOTHIC"])
			self.checkSpawn(iBarbarian, iSwordsman, 4 + iHandicap, (49, 41), (57, 52), self.spawnInvaders, iGameTurn, 5, 2, ["TXT_KEY_ADJECTIVE_VISIGOTHIC"])
			self.checkSpawn(iBarbarian, iHorseArcher, 3, (55, 49), (65, 53), self.spawnInvaders, iGameTurn, 5, 0, ["TXT_KEY_ADJECTIVE_HUNNIC"])
		if utils.isYearIn(300, 700):
			self.checkSpawn(iBarbarian, iHorseArcher, 3 + iHandicap, (58, 50), (88, 53), self.spawnInvaders, iGameTurn, 3, 2, ["TXT_KEY_ADJECTIVE_HUNNIC"])

		#Leoreth: barbarians in Balkans / Black Sea until the High Middle Ages (Bulgarians, Cumans, Pechenegs)
		if utils.isYearIn(680, 1000):
			self.checkSpawn(iBarbarian, iHorseArcher, 3 + iHandicap, (64, 45), (69, 49), self.spawnInvaders, iGameTurn, 6, 2, ["TXT_KEY_ADJECTIVE_AVAR", "TXT_KEY_ADJECTIVE_BULGAR"])
		if utils.isYearIn(900, 1200) and utils.getHumanID() != iKhazars:
			self.checkSpawn(iKhazars, iHorseArcher, 1 + iHandicap, (68, 48), (78, 50), self.spawnInvaders, iGameTurn, 8, 5, ["TXT_KEY_ADJECTIVE_CUMAN"])
			
		#1SDAN: Qarmatians (Abu Tahir al-Jannabi)
		if utils.isYearIn(900, 1000):
			self.checkSpawn(iBarbarian, iHorseArcher, 3 + iHandicap, (76, 34), (79, 37), self.spawnInvaders, iGameTurn, 3, 2, ["TXT_KEY_ADJECTIVE_QARMATIAN"])
			
		#barbarians in central asia
		if utils.isYearIn(-1600, -850):
			self.checkLimitedSpawn(iBarbarian, iVulture, 1, 3, (74, 34), (78, 44), self.spawnNomads, iGameTurn, 8-iHandicap, 2, ["TXT_KEY_ADJECTIVE_ASSYRIAN"])
		elif utils.isYearIn(-850, -200):
			self.checkSpawn(iBarbarian, iHorseman, 1 + iHandicap, (79, 41), (84, 49), self.spawnInvaders, iGameTurn, 10-2*iHandicap, 3, ["TXT_KEY_ADJECTIVE_SCYTHIAN"])
		elif utils.isYearIn(-200, 600):
			self.checkSpawn(iBarbarian, iHorseman, 2 + iHandicap, (79, 41), (84, 49), self.spawnInvaders, iGameTurn, 7-iHandicap, 2, ["TXT_KEY_ADJECTIVE_PARTHIAN"])
		elif utils.isYearIn(600, 900):
			#if utils.getScenario() == i3000BC:  #late start condition
			self.checkSpawn(iBarbarian, iOghuz, 2 + iHandicap, (78, 42), (88, 50), self.spawnNomads, iGameTurn, 8-iHandicap, 2)
		elif utils.isYearIn(900, 1040):
			#if utils.getScenario() == i3000BC:  #late start condition
			self.checkSpawn(iBarbarian, iOghuz, 2 + iHandicap, (78, 42), (90, 52), self.spawnNomads, iGameTurn, 6-iHandicap, 2)

		# late Central Asian barbarians
		if utils.isYearIn(1200, 1600):
			if not utils.getAreaCitiesCiv(iMongolia, utils.getPlotList((70, 48), (80, 59))):
				self.checkSpawn(iBarbarian, iKeshik, 1 + iHandicap, (74, 47), (81, 47), self.spawnNomads, iGameTurn, 10-iHandicap, 5, ["TXT_KEY_ADJECTIVE_TATAR", "TXT_KEY_ADJECTIVE_NOGAI"])
		if utils.isYearIn(1400, 1700):
			if utils.getAreaCities(utils.getPlotList((80, 47), (88, 53))):
				self.checkSpawn(iBarbarian, iKeshik, 1 + iHandicap, (80, 47), (88, 53), self.spawnNomads, iGameTurn, 10-2*iHandicap, 2, ["TXT_KEY_ADJECTIVE_UZBEK", "TXT_KEY_ADJECTIVE_KAZAKH"])
			
		#barbarians in Elam
		if utils.isYearIn(-1600, -1000):
			self.checkSpawn(iBarbarian, iChariot, 1, (81, 37), (87, 45), self.spawnMinors, iGameTurn, 9-iHandicap, 0, ["TXT_KEY_ADJECTIVE_ELAMITE"])

		#barbarians in north africa
		if utils.isYearIn(-210, 50):
			self.checkSpawn(iBarbarian, iCamelRider, 1, (54, 31), (67, 35), self.spawnNomads, iGameTurn, 9-iHandicap, 3, ["TXT_KEY_ADJECTIVE_BERBER"])
		elif utils.isYearIn(50, 900):
			if utils.getScenario() == i3000BC:  #late start condition
				self.checkSpawn(iBarbarian, iCamelRider, 1 + iHandicap, (54, 31), (67, 35), self.spawnNomads, iGameTurn, 10-iHandicap, 5, ["TXT_KEY_ADJECTIVE_BERBER"])
		elif utils.isYearIn(900, 1800):
			self.checkSpawn(iBarbarian, iCamelArcher, 1, (54, 27), (67, 35), self.spawnNomads, iGameTurn, 10-iHandicap, 4, ["TXT_KEY_ADJECTIVE_BERBER"])
			
		#camels in arabia
		if utils.isYearIn(190, 550):
			self.checkSpawn(iBarbarian, iCamelArcher, 1, (73, 30), (82, 36), self.spawnNomads, iGameTurn, 9-iHandicap, 7, ["TXT_KEY_ADJECTIVE_BEDOUIN"])
		if utils.isYearIn(450, 1600):
			if utils.getScenario() == i3000BC:
				self.checkSpawn(iNative, iImpi, 2 + iHandicap, (60, 10), (72, 27), self.spawnNatives, iGameTurn, 10, 4)
			else:
				self.checkSpawn(iNative, iImpi, 2 + iHandicap, (60, 10), (72, 27), self.spawnNatives, iGameTurn, 15, 4)
		elif utils.isYearIn(1600, 1800):
			self.checkSpawn(iNative, iPombos, 2 + iHandicap, (60, 10), (72, 27), self.spawnNatives, iGameTurn, 10, 4)
			
		#west africa
		if utils.isYearIn(450, 1700):
			if iGameTurn < getTurnForYear(1300):
				sAdj = ["TXT_KEY_ADJECTIVE_GHANAIAN"]
			else:
				sAdj = ["TXT_KEY_ADJECTIVE_SONGHAI"]
			self.checkSpawn(iNative, iImpi, 2, (48, 22), (63, 29), self.spawnMinors, iGameTurn, 16, 10, sAdj)
			
		if utils.isYearIn(1200, 1700):
			self.checkSpawn(iBarbarian, iFarari, 1, (48, 26), (65, 37), self.spawnMinors, iGameTurn, 16, 4, sAdj)

		#bulala in Chad
		if iGameTurn == getTurnForYear(1200):
			teamNative.declareWar(iChad, false, WarPlanTypes.NO_WARPLAN)
		if utils.isYearIn(1210, 1571):
			self.checkSpawn(iNative, iLongbowman, 1, (61, 27), (66, 34), self.spawnNatives, iGameTurn, 12, 8, ["TXT_KEY_ADJECTIVE_BULALA"])

		#American natives
		if utils.isYearIn(-100, 400):
			self.checkSpawn(iNative, iDogSoldier, 2 + iHandicap, (15, 38), (24, 47), self.spawnNatives, iGameTurn, 20, 0)
		if utils.isYearIn(400, 1100):
			self.checkSpawn(iNative, iDogSoldier, 1 + iHandicap, (15, 38), (24, 47), self.spawnNatives, iGameTurn, 20, 0)
			if utils.getScenario() == i3000BC:  #late start condition
				self.checkSpawn(iNative, iJaguar, 3, (15, 38), (24, 47), self.spawnNatives, iGameTurn, 16 - 2*iHandicap, 10)
			else:  #late start condition
				self.checkSpawn(iNative, iJaguar, 2, (15, 38), (24, 47), self.spawnNatives, iGameTurn, 16 - 2*iHandicap, 10)
		if utils.isYearIn(1300, 1600):
			self.checkSpawn(iNative, iDogSoldier, 2 + iHandicap, (15, 38), (24, 47), self.spawnNatives, iGameTurn, 8, 0)
		if utils.isYearIn(1400, 1800):
			self.checkSpawn(iNative, iDogSoldier, 1 + iHandicap, (11, 44), (33, 51), self.spawnUprising, iGameTurn, 12, 0)
			self.checkSpawn(iNative, iDogSoldier, 1 + iHandicap, (11, 44), (33, 51), self.spawnUprising, iGameTurn, 12, 6)
		if utils.isYearIn(1300, 1600):
			if iGameTurn % 18 == 0:
				if not gc.getMap().plot(27, 29).isUnit():
					utils.makeUnitAI(iChimuSuchucChiquiAucac, iNative, (27, 29), UnitAITypes.UNITAI_ATTACK, 2 + iHandicap)
			elif iGameTurn % 18 == 9:
				if not gc.getMap().plot(30, 13).isUnit():
					utils.makeUnitAI(iPictaAucac, iNative, (30, 13), UnitAITypes.UNITAI_ATTACK, 2 + iHandicap)
		
		if self.includesActiveHuman([iAmerica, iEngland, iFrance, iMississippi]):
			if utils.isYearIn(1700, 1900):
				self.checkSpawn(iNative, iMountedBrave, 1 + iHandicap, (15, 44), (24, 52), self.spawnNomads, iGameTurn, 12 - iHandicap, 2)
			
			if utils.isYearIn(1500, 1850):
				self.checkSpawn(iNative, iMohawk, 1, (24, 46), (30, 51), self.spawnUprising, iGameTurn, 8, 4)
			
		# Rabbits in Australia
		if iGameTurn >= getTurnForYear(1860):
			self.checkSpawn(iBarbarian, iRabbit, 2 + iHandicap, (103, 10), (118, 22), self.spawnRabbits, iGameTurn, 8, 4)
				
		# if iGameTurn == getTurnForYear(-500):
		# 	gc.getMap().plot(19, 35).setImprovementType(iHut)
		# 	utils.makeUnitAI(iHolkan, iNative, (19, 35), UnitAITypes.UNITAI_ATTACK, 2)
			
		# Oromos in the Horn of Africa
		if utils.isYearIn(1500, 1700):
			iNumUnits = 1
			if pEthiopia.isAlive():
				iNumUnits += 1
				if utils.isYearIn(1600, 1700): iNumUnits += 1
			self.checkSpawn(iBarbarian, iOromoWarrior, iNumUnits, (69, 25), (74, 28), self.spawnInvaders, iGameTurn, 8, 3)
				
		#pirates in the Caribbean
		if utils.isYearIn(1600, 1800):
			self.checkSpawn(iNative, iPrivateer, 1, (24, 32), (35, 46), self.spawnPirates, iGameTurn, 5, 0)
		#pirates in Asia
		if utils.isYearIn(1500, 1900):
			self.checkSpawn(iNative, iPrivateer, 1, (72, 24), (110, 36), self.spawnPirates, iGameTurn, 8, 0)

		if iGameTurn < getTurnForYear(tMinorCities[len(tMinorCities)-1][0])+10:
			self.foundMinorCities(iGameTurn)
			
		if iGameTurn == getTurnForYear(tBirth[iInca]):
			if utils.getHumanID() == iInca:
				utils.makeUnit(iAucac, iNative, (24, 26), 1)
				utils.makeUnit(iAucac, iNative, (25, 23), 1)
				
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
			
			if sName == 'Kyiv': lReligions = [iOrthodoxy]
			if iPlayer == iCeltia and utils.getHumanID() == iCeltia: continue
			if iPlayer == iCeltia: iPlayer = iIndependent
			if sName in ['Buda', 'Tucume']: bForceSpawn = True
			if sName in ['Muqdisho', 'Bahrein']: lReligions = [iIslam]
			
			if not self.isFreePlot(tPlot, bForceSpawn): continue
			
			utils.evacuate(iPlayer, tPlot)
		
			if self.foundCity(iPlayer, tPlot, sName, iPopulation, iUnitType, iNumUnits, lReligions):
				data.lMinorCityFounded[i] = True
		
	def canFoundCity(self, sName):
		if sName == 'Kanchipuram' and utils.getHumanID() == iTamils: return False
		elif sName == 'Tanjapuri' and gc.getPlayer(iTamils).isAlive(): return False
		elif sName == 'Zhongdu' and utils.getHumanID() == iChina: return False
		elif sName == 'Hamburg' and (utils.getHumanID() == iHolyRome or data.iSeed % 4 == 0): return False
		elif sName == 'L&#252;beck' and (utils.getHumanID() == iHolyRome or data.iSeed % 4 != 0): return False
		elif sName == 'Rasa' and gc.getPlayer(iTibet).isAlive(): return False
		elif sName == 'Quelimane' and gc.getPlayer(iSwahili).isAlive(): return False
		elif sName == 'Mombasa' and gc.getPlayer(iSwahili).isAlive(): return False
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
			
			if sName in ['Tucume'] : 
				utils.makeUnit(iWorker, iPlayer, tPlot, 1)
				plot.changeCulture(iPlayer, 20 * (gc.getGame().getCurrentEra() + 1), True)
				city.changeCulture(iPlayer, 20 * (gc.getGame().getCurrentEra() + 1), True)
				utils.makeUnit(iChimuSuchucChiquiAucac, iPlayer, tPlot, 2)
				
			elif sName == 'Bahrein':
				city.setHasRealBuilding(iIslamicTemple, True)
				city.setHasRealBuilding(iLighthouse, True)
				city.setHasRealBuilding(iBarracks, True)
				plot.changeCulture(iPlayer, 20 * (gc.getGame().getCurrentEra() + 1), True)
				city.changeCulture(iPlayer, 20 * (gc.getGame().getCurrentEra() + 1), True)
			else:
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
			print "SETXY barbs 1"
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

	def spawnBears(self, iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
		''' 1SDAN: inside territory, dispersed over several plots, attacking'''
		lPlots = self.possibleTiles(tTL, tBR, bTerritory=True, bNearCity=True)
		
		for i in range(iNumUnits):
			tPlot = utils.getRandomEntry(lPlots)
			if not tPlot: break
			
			lPlots.remove(tPlot)
			utils.makeUnitAI(iUnitType, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK, 1, sAdj)

	def spawnRabbits(self, iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
		''' Merijn: inside territory, dispersed over several plots, pillaging'''
		lPlots = self.possibleTiles(tTL, tBR, bTerritory=True, bNearCity=True)
		
		for i in range(iNumUnits):
			tPlot = utils.getRandomEntry(lPlots)
			if not tPlot: break
			
			lPlots.remove(tPlot)
			utils.makeUnitAI(iUnitType, iPlayer, tPlot, UnitAITypes.UNITAI_PILLAGE, 1, sAdj)