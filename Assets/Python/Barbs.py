from RFCUtils import *
from Consts import *
from StoredData import data

from Events import handler
from Core import *
from Locations import *

# Spawning cities (Leoreth)
# Year, coordinates, owner, name, population, unit type, unit number, religions, forced spawn
tMinorCities = (
(-3000, (73, 38), iIndependent, 'Yerushalayim', 2, iArcher, 3),	# Jerusalem
(-3000, (79, 40), iIndependent2, 'Shushan', 1, iArcher, 1), 	# Susa
(-2000, (85, 47), iIndependent, 'Afrasiyab', 1, iArcher, 1), 	# Samarkand
(-1600, (90, 40), iIndependent, 'Indraprastha', 1, iMilitia, 1),	# Delhi
(-1000, (102, 47), iIndependent, 'Zhongdu', 2, iSpearman, 1),	# Beijing
(-1000, (72, 44), iIndependent, 'Ankuwash', 2, iArcher, 2),		# Ankara
(-770, (59, 47), iCelts, 'Melpum', 2, iArcher, 2),			# Milan
(-350, (56, 47), iCelts, 'Lugodunon', 2, -1, -1),			# Lyon
(-325, (92, 33), iIndependent, 'Kanchipuram', 2, iArcher, 1),	# Madras
(-300, (105, 49), iBarbarian, 'Simiyan hoton', 2, iChariot, 2),	# Shenyang
(-300, (53, 48), iCelts, 'Burdigala', 2, -1, -1),			# Bordeaux
(-300, (91, 31), iIndependent, 'Tanjapuri', 1, iWarElephant, 1),	# Thanjavur
(-250, (19, 35), iNative, 'Danibaan', 2, iHolkan, 1),	# Monte Albán
(-190, (77, 44), iIndependent2, 'Artashat', 1, -1, -1),			# Artaxata
(-100, (95, 47), iBarbarian, 'Dunhuang', 2, iArcher, 1),		# Dunhuang
(100, (18, 37), iBarbarian, 'Tolan', 2, iJaguar, 2),		# Teotihuacan
(-75, (89, 46), iBarbarian, 'Kashgar', 2, iArcher, 1),		# Kashgar
(-50, (55, 50), iCelts, 'Lutetia', 2, -1, -1),				# Paris
(100, (76, 30), iIndependent, "Sana'a", 2, iArcher, 2),			# Sana'a
(107, (98, 36), iIndependent2, 'Pagan', 2, -1, -1),			# Pagan
(200, (75, 28), iIndependent2, 'Barbara', 2, iArcher, 2),	# Berbera
(633, (96, 43), iBarbarian, 'Rasa', 2, iKhampa, 1),		# Lhasa
(680, (51, 37), iIndependent, 'Marrakus', 1, iCrossbowman, 1),	# Marrakesh
(700, (30, 20), iNative, 'Tiwanaku', 1, -1, -1),			# Tihuanaco
(800, tVienna, iIndependent, 'Vindobona', 1, iCrossbowman, 1),	# Wien
(830, (59, 54), iIndependent, 'Hamburg', 2, iCrossbowman, 1),	# Hamburg
(830, (60, 54), iIndependent, 'L&#252;beck', 2, iCrossbowman, 1),	# Lübeck
(866, (101, 37), iBarbarian, 'Dai La', 2, -1, -1),			# Hanoi
(880, (65, 48), iIndependent2, 'Buda', 3, iHorseArcher, 5),		# Budapest
(900, (24, 26), iNative, 'Tucume', 1, iArcher, 2),			# Tucume
(900, (25, 23), iNative, 'Chan Chan', 2, iArcher, 2),		# Chan Chan
(900, (69, 52), iIndependent, 'Kyiv', 2, iCrossbowman, 2),		# Kiev
(900, (74, 25), iIndependent, 'Muqdisho', 3, iCrossbowman, 2),	# Mogadishu
(990, (49, 56), iCelts, '&#193;th Cliath', 1, -1, -1),			# Dublin
(1000, (61, 63), iIndependent2, 'Nidaros', 1, iHuscarl, 1),	# Trondheim
(1000, (71, 17), iNative, 'Quelimane', 1, iNativeRaider, 1),		# Quelimane
(1100, (71, 20), iNative, 'Mombasa', 1, iNativeRaider, 1),		# Mombasa
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
iHandicapOld = (game.getHandicapType() - 1)


@handler("BeginGameTurn")
def helpMinorStates():
	if every(20):
		for iStartYear, iEndYear, tPlot, lUnits in tMinorStates:
			if year().between(iStartYear, iEndYear):
				plot = plot_(tPlot)
				iOwner = plot.getOwner()
				if plot.isCity() and is_minor(iOwner) and plot.getNumUnits() < 4:
					makeUnit(iOwner, random_entry(lUnits), plot)


@handler("BeginGameTurn")
def spawnBarbarians(iGameTurn):
	iHandicap = infos.handicap().getBarbarianSpawnModifier()

	if year().between(-3000, -850):
		if iHandicap >= 0:
			checkSpawn(iBarbarian, iWarrior, 1, (76, 46), (99, 53), spawnMinors, iGameTurn, 5, 0)
		
		checkSpawn(iBarbarian, iWolf, 1, (75, 54), (104, 64), spawnNatives, iGameTurn, 5, 2)
		checkSpawn(iBarbarian, iBear, 1, (75, 54), (104, 64), spawnNatives, iGameTurn, 5, 4)
		checkLimitedSpawn(iBarbarian, iLion, 1, 5, (60, 10), (72, 28), spawnNatives, iGameTurn, 5, 1)
		checkLimitedSpawn(iBarbarian, iPanther, 1, 5, (60, 10), (72, 28), spawnNatives, iGameTurn, 5, 3)
		
	#celts
	if year().between(-650, -110):
		checkSpawn(iCelts, iGallicWarrior, 1, (49, 46), (65, 52), spawnMinors, iGameTurn, 6, 0)
		if iHandicap >= 0:
			checkSpawn(iCelts, iAxeman, 1, (49, 46), (65, 52), spawnMinors, iGameTurn, 8, 5, ["TXT_KEY_ADJECTIVE_GAUL"])

	#norse
	if year().between(-650, 550):
		checkSpawn(iBarbarian, iGalley, 1, (50, 49), (61, 55), spawnPirates, iGameTurn, 20, 0, ["TXT_KEY_ADJECTIVE_NORSE"])
		
	#mongolia
	if year().between(-210, 400):
		checkSpawn(iBarbarian, iHorseArcher, 3 + iHandicap, (94, 48), (107, 54), spawnNomads, iGameTurn, 7-iHandicap, 0, ["TXT_KEY_ADJECTIVE_XIONGNU"])
	elif year().between(400, 900):
		iNumUnits = 3 + iHandicap
		checkSpawn(iBarbarian, iHorseArcher, iNumUnits, (91, 50), (107, 54), spawnNomads, iGameTurn, 6-iHandicap, 0, ["TXT_KEY_ADJECTIVE_GOKTURK", "TXT_KEY_ADJECTIVE_UIGHUR"])
	elif year().between(900, 1100):
		iNumUnits = 3 + iHandicap
		checkSpawn(iBarbarian, iKeshik, iNumUnits, (94, 48), (107, 54), spawnInvaders, iGameTurn, 6, 0, ["TXT_KEY_ADJECTIVE_JURCHEN", "TXT_KEY_ADJECTIVE_KHITAN"])
		
	#tibet
	if year().between(-350, 200):
		checkSpawn(iBarbarian, iLightSwordsman, 1 + iHandicap, (92, 41), (99, 45), spawnMinors, iGameTurn, 10-iHandicap, 3, ["TXT_KEY_ADJECTIVE_TIBETAN"])
	elif year().between(200, 1100):
		checkSpawn(iBarbarian, iSwordsman, 1 + iHandicap, (92, 41), (99, 45), spawnMinors, iGameTurn, 10-iHandicap, 3, ["TXT_KEY_ADJECTIVE_TIBETAN"])

	# Deccan barbarians
	if year().between(-1000, 1200):
		iUnit = iArcher
		iStrength = iHandicap
		if iGameTurn >= year(-500): iUnit = iAxeman
		if iGameTurn >= year(0): iStrength += 1
		if iGameTurn >= year(200): iUnit = iSwordsman
		
		checkSpawn(iBarbarian, iUnit, iStrength, (87, 23), (96, 37), spawnInvaders, iGameTurn, 8-iHandicap, 0, ["Hindi"])
		
	# elephants in india pre-khmer
	if year().between(-210, 700):
		checkSpawn(iBarbarian, iWarElephant, 1, (86, 31), (100, 41), spawnInvaders, iGameTurn, 8-iHandicap, 4)

	#Indo-Scythians
	if year().between(-200, 400):
		checkSpawn(iBarbarian, iHorseman, 2, (84, 40), (89, 43), spawnNomads, iGameTurn, 8-iHandicap, 4, ["TXT_KEY_ADJECTIVE_INDO_SCYTHIAN"])

	#Kushana
	if year().between(30, 220):
		checkSpawn(iBarbarian, iAsvaka, 3+iHandicap, (84, 40), (89, 43), spawnInvaders, iGameTurn, 8, 3, ["TXT_KEY_ADJECTIVE_KUSHANA"])

	#Hephtalites
	if year().between(400, 550):
		checkSpawn(iBarbarian, iHorseArcher, 2+iHandicap, (84, 40), (89, 43), spawnInvaders, iGameTurn, 5-iHandicap, 2, ["TXT_KEY_ADJECTIVE_HEPHTHALITE"])

	# Holkans in classical Mesoamerica
	if year().between(-200, 100):
		checkSpawn(iBarbarian, iHolkan, 1, (17, 31), (25, 37), spawnUprising, iGameTurn, 7, 5)
	if year().between(100, 600):
		checkSpawn(iBarbarian, iHolkan, 1, (17, 31), (25, 37), spawnUprising, iGameTurn, 6, 4)	
	elif year().between(600, 1000):
		checkSpawn(iBarbarian, iHolkan, 1, (17, 31), (25, 37), spawnUprising, iGameTurn, 4, 2)
		
	#pirates in Mediterranean
	if year().between(-210, 50):
		checkSpawn(iBarbarian, iWarGalley, 1, (49, 37), (72, 44), spawnPirates, iGameTurn, 8, 0)
	#pirates in Barbary coast
	if not player(iMoors).isAlive():
		if year().between(-50, 700):
			checkSpawn(iBarbarian, iWarGalley, 1, (46, 30), (62, 39), spawnPirates, iGameTurn, 18, 0)
		elif year().between(700, 1400):
			checkSpawn(iBarbarian, iWarGalley, 1, (46, 30), (62, 39), spawnPirates, iGameTurn, 8, 0)
	#pirates in Indian ocean
	if year().between(-650, 700):
		checkSpawn(iBarbarian, iWarGalley, 1, (72, 20), (91, 36), spawnPirates, iGameTurn, 18, 0)
	elif year().between(700, 1700):
		checkSpawn(iBarbarian, iHeavyGalley, 1, (72, 20), (91, 36), spawnPirates, iGameTurn, 10, 0)

	# Leoreth: Barbarians in Anatolia (Hittites), replace Hattusas spawn
	if year().between(-2000, -800):
		checkSpawn(iBarbarian, iHuluganni, 1 + iHandicap, (68, 42), (74, 45), spawnInvaders, iGameTurn, 16, 0, ["TXT_KEY_ADJECTIVE_HITTITE"])

	#barbarians in europe
	if year().between(-210, 470):
		checkSpawn(iBarbarian, iAxeman, 3 + iHandicap, (50, 45), (63, 52), spawnInvaders, iGameTurn, 10, 0, ["TXT_KEY_ADJECTIVE_GERMANIC"])
		checkSpawn(iBarbarian, iAxeman, 2 + iHandicap, (64, 49), (69, 55), spawnInvaders, iGameTurn, 12, 2, ["TXT_KEY_ADJECTIVE_GERMANIC"])
	# Leoreth: begins 100 AD instead of 50 AD
	if year().between(100, 470):
		checkSpawn(iBarbarian, iSwordsman, 3, (58, 45), (70, 55), spawnInvaders, iGameTurn, 8, 5, ["TXT_KEY_ADJECTIVE_GERMANIC"])
	if year().between(300, 550):
		checkSpawn(iBarbarian, iAxeman, 4 + iHandicap, (49, 41), (56, 52), spawnInvaders, iGameTurn, 5, 4, ["TXT_KEY_ADJECTIVE_VISIGOTHIC"])
		checkSpawn(iBarbarian, iSwordsman, 4 + iHandicap, (49, 41), (57, 52), spawnInvaders, iGameTurn, 5, 2, ["TXT_KEY_ADJECTIVE_VISIGOTHIC"])
		checkSpawn(iBarbarian, iHorseArcher, 3, (55, 49), (65, 53), spawnInvaders, iGameTurn, 5, 0, ["TXT_KEY_ADJECTIVE_HUNNIC"])
	if year().between(300, 700):
		checkSpawn(iBarbarian, iHorseArcher, 3 + iHandicap, (58, 50), (88, 53), spawnInvaders, iGameTurn, 3, 2, ["TXT_KEY_ADJECTIVE_HUNNIC"])

	#Leoreth: barbarians in Balkans / Black Sea until the High Middle Ages (Bulgarians, Cumans, Pechenegs)
	if year().between(680, 1000):
		checkSpawn(iBarbarian, iHorseArcher, 3 + iHandicap, (64, 45), (69, 49), spawnInvaders, iGameTurn, 6, 2, ["TXT_KEY_ADJECTIVE_AVAR", "TXT_KEY_ADJECTIVE_BULGAR"])
	if year().between(900, 1200):
		checkSpawn(iBarbarian, iHorseArcher, 3 + iHandicap, (68, 48), (78, 50), spawnInvaders, iGameTurn, 8, 5, ["TXT_KEY_ADJECTIVE_CUMAN"])
		
	#barbarians in central asia
	if year().between(-1600, -850):
		checkLimitedSpawn(iBarbarian, iVulture, 1, 3, (74, 34), (78, 44), spawnNomads, iGameTurn, 8-iHandicap, 2, ["TXT_KEY_ADJECTIVE_ASSYRIAN"])
	elif year().between(-850, -200):
		checkSpawn(iBarbarian, iHorseman, 1 + iHandicap, (79, 41), (84, 49), spawnInvaders, iGameTurn, 10-2*iHandicap, 3, ["TXT_KEY_ADJECTIVE_SCYTHIAN"])
	elif year().between(-200, 600):
		checkSpawn(iBarbarian, iHorseman, 2 + iHandicap, (79, 41), (84, 49), spawnInvaders, iGameTurn, 7-iHandicap, 2, ["TXT_KEY_ADJECTIVE_PARTHIAN"])
	elif year().between(600, 900):
		checkSpawn(iBarbarian, iOghuz, 2 + iHandicap, (78, 42), (88, 50), spawnNomads, iGameTurn, 8-iHandicap, 2)
	elif year().between(900, 1040):
		checkSpawn(iBarbarian, iOghuz, 2 + iHandicap, (78, 42), (90, 52), spawnNomads, iGameTurn, 6-iHandicap, 2)

	# late Central Asian barbarians
	if year().between(1200, 1600):
		if not cities.start(70, 48).end(80, 59).owner(iMongols):
			checkSpawn(iBarbarian, iKeshik, 1 + iHandicap, (74, 47), (81, 47), spawnNomads, iGameTurn, 10-iHandicap, 5, ["TXT_KEY_ADJECTIVE_TATAR", "TXT_KEY_ADJECTIVE_NOGAI"])
	if year().between(1400, 1700):
		if cities.start(80, 47).end(88, 53):
			checkSpawn(iBarbarian, iKeshik, 1 + iHandicap, (80, 47), (88, 53), spawnNomads, iGameTurn, 10-2*iHandicap, 2, ["TXT_KEY_ADJECTIVE_UZBEK", "TXT_KEY_ADJECTIVE_KAZAKH"])
		
	#barbarians in Elam
	if year().between(-1600, -1000):
		checkSpawn(iBarbarian, iChariot, 1, (81, 37), (87, 45), spawnMinors, iGameTurn, 9-iHandicap, 0, ["TXT_KEY_ADJECTIVE_ELAMITE"])

	#barbarians in north africa
	if year().between(-210, 50):
		checkSpawn(iBarbarian, iCamelRider, 1, (54, 31), (67, 35), spawnNomads, iGameTurn, 9-iHandicap, 3, ["TXT_KEY_ADJECTIVE_BERBER"])
	elif year().between(50, 900):
		if scenario() == i3000BC:  #late start condition
			checkSpawn(iBarbarian, iCamelRider, 1 + iHandicap, (54, 31), (67, 35), spawnNomads, iGameTurn, 10-iHandicap, 5, ["TXT_KEY_ADJECTIVE_BERBER"])
	elif year().between(900, 1800):
		checkSpawn(iBarbarian, iCamelArcher, 1, (54, 27), (67, 35), spawnNomads, iGameTurn, 10-iHandicap, 4, ["TXT_KEY_ADJECTIVE_BERBER"])
		
	#camels in arabia
	if year().between(190, 550):
		checkSpawn(iBarbarian, iCamelArcher, 1, (73, 30), (82, 36), spawnNomads, iGameTurn, 9-iHandicap, 7, ["TXT_KEY_ADJECTIVE_BEDOUIN"])
	if year().between(-800, 1300) and includesActiveHuman(iEgypt, iArabia):
		iNumUnits = iHandicap
		if scenario() == i3000BC: iNumUnits += 1
		checkSpawn(iBarbarian, iMedjay, iNumUnits, (66, 28), (71, 34), spawnUprising, iGameTurn, 12, 4, ["TXT_KEY_ADJECTIVE_NUBIAN"])
	if year().between(450, 1900):
		if scenario() == i3000BC:
			checkSpawn(iNative, iNativeRaider, 2 + iHandicap, (60, 10), (72, 27), spawnNatives, iGameTurn, 10, 4)
		else:
			checkSpawn(iNative, iNativeRaider, 2 + iHandicap, (60, 10), (72, 27), spawnNatives, iGameTurn, 15, 4)
	elif year().between(1600, 1800):
		checkSpawn(iNative, iPombos, 2 + iHandicap, (60, 10), (72, 27), spawnNatives, iGameTurn, 10, 4)
		
	#west africa
	if year().between(450, 1800):
		checkSpawn(iNative, iNativeRaider, 2, (48, 22), (66, 29), spawnNatives, iGameTurn, 16, 10)
		
		checkSpawn(iNative, iNativeArcher, 1, (48, 22), (66, 29), spawnNatives, iGameTurn, 12, 8)
		checkSpawn(iNative, iNativeWarrior, 2, (48, 22), (66, 29), spawnNatives, iGameTurn, 12, 2)
		
	if year().between(1200, 1700):
		checkSpawn(iBarbarian, iFarari, 1, (48, 26), (65, 37), spawnMinors, iGameTurn, 16, 4, ["TXT_KEY_ADJECTIVE_SONGHAI"])

	#American natives
	if year().between(600, 1100):
		checkSpawn(iNative, iDogSoldier, 1 + iHandicap, (15, 38), (24, 47), spawnNatives, iGameTurn, 20, 0)
		if scenario() == i3000BC:  #late start condition
			checkSpawn(iNative, iJaguar, 3, (15, 38), (24, 47), spawnNatives, iGameTurn, 16 - 2*iHandicap, 10)
		else:  #late start condition
			checkSpawn(iNative, iJaguar, 2, (15, 38), (24, 47), spawnNatives, iGameTurn, 16 - 2*iHandicap, 10)
	if year().between(1300, 1600):
		checkSpawn(iNative, iDogSoldier, 2 + iHandicap, (15, 38), (24, 47), spawnNatives, iGameTurn, 8, 0)
	if year().between(1400, 1800):
		checkSpawn(iNative, iDogSoldier, 1 + iHandicap, (11, 44), (33, 51), spawnUprising, iGameTurn, 12, 0)
		checkSpawn(iNative, iDogSoldier, 1 + iHandicap, (11, 44), (33, 51), spawnUprising, iGameTurn, 12, 6)
	if year().between(1300, 1600):
		if iGameTurn % 18 == 0:
			if not plot_(27, 29).isUnit():
				makeUnits(iNative, iDogSoldier, (27, 29), 2 + iHandicap, UnitAITypes.UNITAI_ATTACK)
		elif iGameTurn % 18 == 9:
			if not plot_(30, 13).isUnit():
				makeUnits(iNative, iDogSoldier, (30, 13), 2 + iHandicap, UnitAITypes.UNITAI_ATTACK)
	
	if includesActiveHuman(iAmerica, iEngland, iFrance):
		if year().between(1700, 1900):
			checkSpawn(iNative, iMountedBrave, 1 + iHandicap, (15, 44), (24, 52), spawnNomads, iGameTurn, 12 - iHandicap, 2)
		
		if year().between(1500, 1850):
			checkSpawn(iNative, iMohawk, 1, (24, 46), (30, 51), spawnUprising, iGameTurn, 8, 4)
			
	if iGameTurn == year(-500):
		plot_(19, 35).setImprovementType(iHut)
		makeUnits(iNative, iHolkan, (19, 35), 2, UnitAITypes.UNITAI_ATTACK)
		
	# Oromos in the Horn of Africa
	if year().between(1500, 1700):
		iNumUnits = 1
		if player(iEthiopia).isAlive():
			iNumUnits += 1
			if year().between(1600, 1700): iNumUnits += 1
		checkSpawn(iBarbarian, iOromoWarrior, iNumUnits, (69, 25), (74, 28), spawnInvaders, iGameTurn, 8, 3)
			
	#pirates in the Caribbean
	if year().between(1600, 1800):
		checkSpawn(iNative, iPrivateer, 1, (24, 32), (35, 46), spawnPirates, iGameTurn, 5, 0)
	#pirates in Asia
	if year().between(1500, 1900):
		checkSpawn(iNative, iPrivateer, 1, (72, 24), (110, 36), spawnPirates, iGameTurn, 8, 0)

	if iGameTurn < year(tMinorCities[len(tMinorCities)-1][0])+10:
		foundMinorCities(iGameTurn)

	if iGameTurn == year(dBirth[iInca]):
		if player(iInca).isHuman():
			makeUnit(iNative, iAucac, (24, 26))
			makeUnit(iNative, iAucac, (25, 23))
				
def foundMinorCities(iGameTurn):
	for i, (iYear, tPlot, iCiv, sName, iPopulation, iUnitType, iNumUnits) in enumerate(tMinorCities):
		if iGameTurn < year(iYear): return
		if iGameTurn > year(iYear)+10: continue
		
		if data.lMinorCityFounded[i]: continue
		
		if plot(tPlot).isCity(): continue
		
		# special cases
		if not canFoundCity(sName): continue
		
		lReligions = []
		bForceSpawn = False
		
		if sName == 'Kyiv': lReligions = [iOrthodoxy]
		if iCiv == iCelts and scenario() != i3000BC: iCiv = civ(players.independent().random())
		if sName == 'Buda': bForceSpawn = True
		if sName == 'Muqdisho': lReligions = [iIslam]
		if sName in ['Hamburg', 'L&#252;beck']: bForceSpawn = True
		
		if not isFree(iCiv, tPlot, bNoCity=True, bNoCulture=not bForceSpawn): continue
		
		evacuate(slot(iCiv), tPlot)
	
		if foundCity(iCiv, tPlot, sName, iPopulation, iUnitType, iNumUnits, lReligions):
			data.lMinorCityFounded[i] = True
		
def canFoundCity(sName):
	if sName == 'Kanchipuram' and player(iTamils).isHuman(): return False
	elif sName == 'Tanjapuri' and player(iTamils).isAlive(): return False
	elif sName == 'Zhongdu' and player(iChina).isHuman(): return False
	elif sName == 'Hamburg' and (player(iHolyRome).isHuman() or data.iSeed % 4 == 0): return False
	elif sName == 'L&#252;beck' and (player(iHolyRome).isHuman() or data.iSeed % 4 != 0): return False
	elif sName == 'Rasa' and player(iTibet).isAlive(): return False
	
	return True
	
def foundCity(iCiv, (x, y), sName, iPopulation, iUnitType = -1, iNumUnits = -1, lReligions = []):
	iPlayer = slot(iCiv)
	pPlayer = player(iPlayer)
	plot(x, y).setOwner(iPlayer)
	pPlayer.found(x, y)
	
	founded = city(x, y)
	if founded:
		founded.setName(sName, False)
		founded.setPopulation(iPopulation)
		
		plot(founded).changeCulture(iPlayer, 10 * (game.getCurrentEra() + 1), True)
		founded.changeCulture(iPlayer, 10 * (game.getCurrentEra() + 1), True)
		
		if iNumUnits > 0 and iUnitType > 0:
			makeUnits(iPlayer, iUnitType, founded, iNumUnits)
			
		for iReligion in lReligions:
			if game.isReligionFounded(iReligion):
				founded.setHasReligion(iReligion, True, False, False)
				
		return True
	
	return False

def checkLimitedSpawn(iCiv, iUnitType, iNumUnits, iMaxUnits, tTL, tBR, spawnFunction, iTurn, iPeriod, iRest, lAdj=[]):
	iAreaUnits = plots.start(tTL).end(tBR).units().owner(iCiv).count()
	if iAreaUnits < iMaxUnits:
		checkSpawn(iCiv, iUnitType, iNumUnits, tTL, tBR, spawnFunction, iTurn, iPeriod, iRest, lAdj)
					
# Leoreth: new ways to spawn barbarians
def checkSpawn(iCiv, iUnitType, iNumUnits, tTL, tBR, spawnFunction, iTurn, iPeriod, iRest, lAdj=[]):	
	if periodic(iPeriod):
		spawnFunction(slot(iCiv), iUnitType, iNumUnits, tTL, tBR, random_entry(lAdj))
			
def possibleTiles(tTL, tBR, bWater=False, bTerritory=False, bBorder=False, bImpassable=False, bNearCity=False):
	return plots.start(tTL).end(tBR).where(lambda p: possibleTile(p, bWater, bTerritory, bBorder, bImpassable, bNearCity))
	
def possibleTile(plot, bWater, bTerritory, bBorder, bImpassable, bNearCity):
	# never on peaks
	if plot.isPeak(): return False
	
	# only land or water
	if bWater != plot.isWater(): return False
	
	# only inside territory if specified
	if not bTerritory and plot.isOwned(): return False
	
	# never directly next to cities
	if cities.surrounding(plot): return False
	
	# never on tiles with units
	if plot.isUnit(): return False
	
	# never in marsh (impassable)
	if plot.getFeatureType() == iMarsh: return False
	
	# allow other impassable terrain (ocean, jungle)
	if not bImpassable:
		if plot.getTerrainType() == iOcean: return False
		if plot.getFeatureType() == iJungle: return False
	
	# restrict to borders if specified
	if bBorder and not plots.surrounding(plot).notowner(plot.getOwner()): return False
	
	# near a city if specified (next to cities excluded above)
	if bNearCity and not plots.surrounding(plot, radius=2).where(lambda p: not p.isCity()): return False
	
	# not on landmasses without cities
	if not bWater and map.getArea(plot.getArea()).getNumCities() == 0: return False
	
	return True

def spawnPirates(iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
	'''Leoreth: spawns all ships at the same coastal spot, out to pillage and disrupt trade, can spawn inside borders'''
	plot = possibleTiles(tTL, tBR, bWater=True, bTerritory=False).random()
	
	if plot:
		makeUnits(iPlayer, iUnitType, plot, iNumUnits, UnitAITypes.UNITAI_PIRATE_SEA).adjective(sAdj)
	
def spawnNatives(iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
	'''Leoreth: outside of territory, in jungles, all dispersed on several plots, out to pillage'''
	for plot in possibleTiles(tTL, tBR, bTerritory=False, bImpassable=True).sample(iNumUnits):
		makeUnits(iPlayer, iUnitType, plot, 1, UnitAITypes.UNITAI_ATTACK).adjective(sAdj)
		
def spawnMinors(iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
	'''Leoreth: represents minor states without ingame cities
			outside of territory, not in jungles, in groups, passive'''
	plot = possibleTiles(tTL, tBR, bTerritory=False).random()
	
	if plot:
		makeUnits(iPlayer, iUnitType, plot, iNumUnits, UnitAITypes.UNITAI_ATTACK).adjective(sAdj)
	
def spawnNomads(iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
	'''Leoreth: represents aggressive steppe nomads etc.
			outside of territory, not in jungles, in small groups, target cities'''
	plot = possibleTiles(tTL, tBR, bTerritory=False).random()
	
	if plot:
		makeUnits(iPlayer, iUnitType, plot, iNumUnits, UnitAITypes.UNITAI_ATTACK).adjective(sAdj)
		
def spawnInvaders(iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
	'''Leoreth: represents large invasion forces and migration movements
			inside of territory, not in jungles, in groups, target cities'''
	plot = possibleTiles(tTL, tBR, bTerritory=True, bBorder=True).random()
	
	if plot:
		makeUnits(iPlayer, iUnitType, plot, iNumUnits, UnitAITypes.UNITAI_ATTACK).adjective(sAdj)
		
def spawnUprising(iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
	''' Leoreth: represents uprisings of Natives against colonial settlements, especially North America
			 spawns units in a free plot in the second ring of a random target city in the area
			 (also used for units from warring city states in classical Mesoamerica)'''
	plot = possibleTiles(tTL, tBR, bTerritory=True, bNearCity=True).random()
	
	if plot:
		makeUnits(iPlayer, iUnitType, plot, iNumUnits, UnitAITypes.UNITAI_ATTACK).adjective(sAdj)
		
def includesActiveHuman(*civs):
	return civ() in civs and year(dBirth[active()]) <= year()