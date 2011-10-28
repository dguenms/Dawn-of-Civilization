# Rhye's and Fall of Civilization - Barbarian units and cities

from CvPythonExtensions import *
import CvUtil
import PyHelpers        # LOQ
#import Popup
#import cPickle as pickle
import RFCUtils
import Consts as con

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
      

# city coordinates, spawn 1st turn and retries
# converted to years (3rd col.), last col. stays the same(turns) - edead
lUr = [77, 38, -3000, 0] #0
lJerusalem = [73, 38, -3000, 0] #0
lBabylon = [76, 40, -3000, 0] #0
lSusa = [79, 40, -3000, 0] #0
lTyre = [73, 40, -3000, 0] #0 / 2700BC #turn10
lKnossos = [69, 39, -2600, 0] #13
lHattusas = [73, 43, -2000, 0] #34
lSamarkand = [85, 47, -2000, 0] #34
lNineveh = [76, 42, -1800, 0] #42
lGadir = [51, 40, -1100, 0] #70
lLepcis = [61, 37, -1100, 0] #70
lBeijing = [102, 47, -1000, 0]
lCarthage = [58, 39, -814, 0] #86
lGordion = [71, 43, -800, 0] #87
lPalermo = [60, 40, -760, 0] #94-5
lMilan = [59, 47, -760, 0] #94-5
lAugsburg = [60, 49, -760, 0] #94-5
lRusadir = [54, 38, -650, 0] #97
lLyon = [56, 47, -350, 0] #117
#lAxum = [72, 29, -300, 0] #121
lShenyang = [105, 49, -300, 0]
lBordeaux = [53, 48, -300, 0] #121
lThanjavur = [91, 31, -300, 0]
lMadras = [92, 33, -300, 0]
lCartagena = [54, 42, -230, 0] #125
lArtaxata = [77, 44, -190,0] #128
lDunhuang = [95, 47, -100, 0] #133 Orka
lKashgar = [89, 46, -75, 0] #133 Orka
lLutetia = [55, 50, -50, 0] #137
#lSeoul = [109, 46, -25, 0] #139
#lTikal = [22, 35, 60, 0] #145
lSanaa = [76, 30, 100, 0] #147
lPagan = [98, 36, 107, 0] #148
#lInverness = [52, 60, 400, 0] #167
#lEdinburgh = [52, 59, 400, 0] #167
#lChichenItza = [23, 37, 445, 0] #170
lBaku = [77, 45, 600, 0] #180
lLhasa = [96, 43, 633, 0] #184
#lAngkor = [102, 34, 802, 0] #201
lHanoi = [101, 37, 866, 0] #208
lTucume = [24, 26, 900, 0] #211
lKiev = [69, 52, 900, 0] #211
lJelling = [59, 55, 980, 0] #219
lDublin = [49, 56, 990, 0] #220
lNidaros = [61, 62, 1000, 0] #221
lZimbabwe = [69, 15, 1000, 0] #221
lQuelimane = [71, 17, 1000, 0] #221
lUppsala = [63, 58, 1070, 0] #228
lMombasa = [71, 22, 1100, 0] #231
lKazan = [77, 55, 1200, 0] #241
lKongo = [62, 20, 1483, 0] #278



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
                iHandicap = (gc.getGame().getHandicapType() - 1)

		# Leoreth: Tibet
		if iGameTurn == getTurnForYear(lLhasa[2]):
			x, y = lLhasa[0], lLhasa[1]
			if not gc.getMap().plot(x, y).isCity():
				gc.getMap().plot(x, y).setOwner(iBarbarian)
				gc.getPlayer(iBarbarian).found(x, y)
			if gc.getMap().plot(x, y).isCity():
				if gc.getMap().plot(x, y).getPlotCity().getOwner() == iBarbarian:
					gc.getMap().plot(x, y).getPlotCity().setCulture(iBarbarian, 1000, True)
					gc.getMap().plot(x, y).getPlotCity().setName("Lhasa", False)

			lTibet = [(93, 42), (93, 43), (93, 44), (94, 42), (94, 43), (94, 44), (95, 42), (95, 43), (95, 44), (96, 42), (96, 43), (96, 44), (92, 43), (95, 45), (96, 45), (97, 45), (97, 44), (97, 43)]
			for tPlot in lTibet:
				x, y = tPlot
				utils.convertPlotCulture(gc.getMap().plot(x, y), con.iBarbarian, 100, False)

                #debug
                #if (iGameTurn % 50 == 1):
                #        print ("iHandicap", iHandicap)
                #        print ("iHandicapOld", iHandicapOld)

                if (iGameTurn >= getTurnForYear(-3000) and iGameTurn <= getTurnForYear(-850)):
                        if (iHandicap >= 0):
                                self.spawnUnits( iBarbarian, (76, 46), (99, 53), con.iWarrior, 1, iGameTurn, 5, 0, utils.outerInvasion, 0)
                        self.spawnUnits( iBarbarian, (75, 54), (104, 64), con.iWolf, 1, iGameTurn, 5, 2, utils.outerInvasion, 0)
                        self.spawnUnits( iBarbarian, (75, 54), (104, 64), con.iBear, 1, iGameTurn, 5, 4, utils.outerInvasion, 0)
                        self.spawnUnits( iBarbarian, (55, 10), (72, 29), con.iLion, 1, iGameTurn, 4, 1, utils.outerInvasion, 0)
                        self.spawnUnits( iBarbarian, (55, 10), (72, 29), con.iPanther, 1, iGameTurn, 4, 3, utils.outerInvasion, 0)

                        
                #celts
                if (iGameTurn >= getTurnForYear(-650) and iGameTurn <= getTurnForYear(-110)):
                        self.spawnUnits( iCeltia, (49, 46), (65, 52), con.iCelticGallicWarrior, 1, iGameTurn, 7, 0, utils.outerInvasion, 0)
                        if (iHandicap >= 0):
                                self.spawnUnits( iCeltia, (49, 46), (65, 52), con.iAxeman, 1, iGameTurn, 9, 6, utils.outerInvasion, 0)  

                #norse
                if (iGameTurn >= getTurnForYear(-650) and iGameTurn <= getTurnForYear(550)):
                        self.spawnUnits( iCeltia, (50, 49), (61, 65), con.iGalley, 1, iGameTurn, 25, 0, utils.outerSeaSpawn, 2)
                        
                #mongolia
                if (iGameTurn >= getTurnForYear(-210) and iGameTurn < getTurnForYear(300)):
                        self.spawnUnits( iBarbarian, (94, 48), (107, 54), con.iHorseArcher, 2 + iHandicap*2, iGameTurn, 8, 0, utils.outerInvasion, 0)
                if (iGameTurn >= getTurnForYear(300) and iGameTurn <= getTurnForYear(900)):
                        self.spawnUnits( iBarbarian, (91, 50), (107, 54), con.iHorseArcher, 3 + iHandicap*2, iGameTurn, 7, 0, utils.outerInvasion, 0)
                if (iGameTurn > getTurnForYear(900) and iGameTurn <= getTurnForYear(1100)):
                        self.spawnUnits( iBarbarian, (94, 48), (107, 54), con.iHorseArcher, 2 + iHandicap, iGameTurn, 6, 0, utils.outerInvasion, 0)
                        
                #tibet
                if (iGameTurn >= getTurnForYear(-350) and iGameTurn <= getTurnForYear(1100)):
                        self.spawnUnits( iBarbarian, (92, 41), (99, 45), con.iSwordsman, 1 + iHandicap, iGameTurn, 10-iHandicap, 3, utils.outerInvasion, 0)

                #elephants in india pre-khmer
                if (iGameTurn >= getTurnForYear(-210) and iGameTurn <= getTurnForYear(700)):
                        self.spawnUnits( iBarbarian, (86, 31), (100, 41), con.iWarElephant, 1, iGameTurn, 6-iHandicap, 4, utils.outerInvasion, 0)

		#Indo-Scythians
		if iGameTurn >= getTurnForYear(-200) and iGameTurn <= getTurnForYear(400):
			self.spawnUnits(iBarbarian, (84, 40), (87, 43), con.iHorseArcher, 2, iGameTurn, 10-iHandicap, 4, utils.internalInvasion, 0)

		#Kushana
		if iGameTurn >= getTurnForYear(30) and iGameTurn <= getTurnForYear(220):
			self.spawnUnits(iBarbarian, (84, 40), (87, 43), con.iSwordsman, 1, iGameTurn, 6-iHandicap, 3, utils.internalInvasion, 0)

		#Hephtalites
		if iGameTurn >= getTurnForYear(400) and iGameTurn <= getTurnForYear(550):
			self.spawnUnits(iBarbarian, (84, 40), (87, 43), con.iHorseArcher, 2+iHandicap, iGameTurn, 6-iHandicap, 3, utils.internalInvasion, 0)

       
                        
                #pirates in Mediterranean
                if (iGameTurn >= getTurnForYear(-210) and iGameTurn <= getTurnForYear(50)):
                        self.spawnUnits( iBarbarian, (49, 37), (72, 44), con.iTrireme, 1, iGameTurn, 8, 0, utils.outerSeaSpawn, 2)
                #pirates in Barbary coast
                if (iGameTurn >= getTurnForYear(50) and iGameTurn <= getTurnForYear(700)):
                        self.spawnUnits( iBarbarian, (46, 30), (62, 39), con.iTrireme, 1, iGameTurn, 18, 0, utils.outerCoastSpawn, 2)
                if (iGameTurn >= getTurnForYear(700) and iGameTurn <= getTurnForYear(1400)):
                        self.spawnUnits( iBarbarian, (46, 30), (62, 39), con.iTrireme, 1, iGameTurn, 8, 0, utils.outerCoastSpawn, 2)
                if (iGameTurn >= getTurnForYear(1400) and iGameTurn <= getTurnForYear(1700)):
                        self.spawnUnits( iBarbarian, (46, 30), (62, 39), con.iTrireme, 1, iGameTurn, 12, 0, utils.outerCoastSpawn, 2)
                #pirates in Indian ocean
                if (iGameTurn >= getTurnForYear(-650) and iGameTurn <= getTurnForYear(700)):
                        self.spawnUnits( iBarbarian, (72, 20), (91, 36), con.iTrireme, 1, iGameTurn, 18, 0, utils.outerCoastSpawn, 2)
                if (iGameTurn >= getTurnForYear(700) and iGameTurn <= getTurnForYear(1700)):
                        self.spawnUnits( iBarbarian, (72, 20), (91, 36), con.iTrireme, 1, iGameTurn, 8, 0, utils.outerCoastSpawn, 2)



		# Leoreth: Barbarians in Anatolia (Hittites), replace Hattusas spawn
		if (iGameTurn >= getTurnForYear(-2000) and iGameTurn <= getTurnForYear(-800)):
			self.spawnUnits( iBarbarian, (68, 42), (74, 45), con.iChariot, 2 + iHandicap, iGameTurn, 14, 0, utils.outerInvasion, 1)
                        
                #barbarians in europe
                if (iGameTurn >= getTurnForYear(-210) and iGameTurn <= getTurnForYear(470)):
                        self.spawnUnits( iBarbarian, (50, 45), (63, 52), con.iAxeman, 3 + iHandicap, iGameTurn, 12, 0, utils.outerInvasion, 0)
                        self.spawnUnits( iBarbarian, (64, 49), (69, 55), con.iAxeman, 2 + iHandicap, iGameTurn, 14, 2, utils.outerInvasion, 0)
		# Leoreth: begins 200 AD instead of 50 AD
                if (iGameTurn >= getTurnForYear(200) and iGameTurn <= getTurnForYear(470)):
                        self.spawnUnits( iBarbarian, (58, 45), (70, 55), con.iSwordsman, 3, iGameTurn, 10, 5, utils.outerInvasion, 0)                       
                if (iGameTurn >= getTurnForYear(300) and iGameTurn <= getTurnForYear(550)):
                        self.spawnUnits( iBarbarian, (49, 41), (56, 52), con.iAxeman, 4 + iHandicap, iGameTurn, 6, 4, utils.outerInvasion, 0)
                        self.spawnUnits( iBarbarian, (49, 41), (57, 52), con.iSwordsman, 4 + iHandicap, iGameTurn, 6, 2, utils.outerInvasion, 0)
                        self.spawnUnits( iBarbarian, (55, 49), (65, 53), con.iHorseArcher, 3, iGameTurn, 6, 0, utils.outerInvasion, 0)
                if (iGameTurn >= getTurnForYear(300) and iGameTurn <= getTurnForYear(700)):
                        self.spawnUnits( iBarbarian, (58, 50), (88, 53), con.iHorseArcher, 3 + iHandicap, iGameTurn, 4, 2, utils.outerInvasion, 0)

		#Leoreth: barbarians in Balkans / Black Sea until the High Middle Ages (Bulgarians, Cumans, Pechenegs)
		if (iGameTurn >= getTurnForYear(680) and iGameTurn <= getTurnForYear(1000)):
			if (gc.getPlayer(0).isPlayable()):
				self.spawnUnits(iBarbarian, (64, 45), (69, 49), con.iHorseArcher, 3 + iHandicap, iGameTurn, 6, 2, utils.internalInvasion, 0)
		if (iGameTurn >= getTurnForYear(900) and iGameTurn <= getTurnForYear(1200)):
			if (gc.getPlayer(0).isPlayable()):
				self.spawnUnits(iBarbarian, (68, 48), (78, 50), con.iHorseArcher, 3 + iHandicap, iGameTurn, 10, 5, utils.internalInvasion, 0)

                #last barbarians in east europe and caucasus
                if (iGameTurn >= getTurnForYear(690) and iGameTurn <= getTurnForYear(1100)):
                        if (gc.getPlayer(0).isPlayable()):  #late start condition
                                self.spawnUnits( iBarbarian, (67, 45), (79, 50), con.iHorseArcher, 3 + iHandicap, iGameTurn, 6, 0, utils.outerInvasion, 0)

                #barbarians in central asia
                if (iGameTurn >= getTurnForYear(-1600) and iGameTurn < getTurnForYear(-850)):
                        self.spawnUnits( iBarbarian, (74, 34), (68, 48), con.iChariot, 2 + iHandicap, iGameTurn, 6-iHandicap, 2, utils.outerInvasion, 0)
                if (iGameTurn >= getTurnForYear(-850) and iGameTurn < getTurnForYear(300)):
                        self.spawnUnits( iBarbarian, (73, 34), (79, 49), con.iChariot, 1 + iHandicap, iGameTurn, 7-iHandicap, 2, utils.outerInvasion, 0)
                        self.spawnUnits( iBarbarian, (73, 34), (79, 49), con.iHorseArcher, 1 + iHandicap, iGameTurn, 7-iHandicap, 2, utils.outerInvasion, 0)
                if (iGameTurn >= getTurnForYear(300) and iGameTurn <= getTurnForYear(700)):
                        if (gc.getPlayer(0).isPlayable()):  #late start condition
                                self.spawnUnits( iBarbarian, (78, 42), (88, 50), con.iHorseArcher, 3 + iHandicap, iGameTurn, 8-iHandicap, 2, utils.outerInvasion, 0)
                if (iGameTurn > getTurnForYear(700) and iGameTurn <= getTurnForYear(1400)):
                        if (gc.getPlayer(0).isPlayable()):  #late start condition
                                self.spawnUnits( iBarbarian, (78, 42), (90, 52), con.iHorseArcher, 2 + iHandicap, iGameTurn, 6-iHandicap, 2, utils.outerInvasion, 0)
                        
                #barbarians in Elam
                if (iGameTurn >= getTurnForYear(-1600) and iGameTurn < getTurnForYear(-1000)):
                        self.spawnUnits( iBarbarian, (81, 37), (87, 45), con.iChariot, 2, iGameTurn, 7-iHandicap, 0, utils.outerInvasion, 0)

                #barbarians in north africa
                if (iGameTurn >= getTurnForYear(-210) and iGameTurn < getTurnForYear(50)):
                        self.spawnUnits( iBarbarian, (54, 31), (67, 35), con.iHorseArcher, 1, iGameTurn, 9-iHandicap, 3, utils.outerInvasion, 0)
                if (iGameTurn >= getTurnForYear(50) and iGameTurn < getTurnForYear(900)):
                        if (gc.getPlayer(0).isPlayable()):  #late start condition
                                self.spawnUnits( iBarbarian, (54, 31), (67, 35), con.iHorseArcher, 2, iGameTurn, 10-iHandicap, 5, utils.outerInvasion, 0)
                                self.spawnUnits( iBarbarian, (56, 29), (70, 33), con.iCamelArcher, 2 + iHandicap, iGameTurn, 10, 0, utils.outerInvasion, 0)
                if (iGameTurn >= getTurnForYear(900) and iGameTurn <= getTurnForYear(1800)):
                        self.spawnUnits( iBarbarian, (54, 27), (67, 35), con.iCamelArcher, 1, iGameTurn, 8-iHandicap, 4, utils.outerInvasion, 0)
                        
                #camels in arabia
                #if (iGameTurn >= getTurnForYear(-850) and iGameTurn <= getTurnForYear(190)):
                #        self.spawnUnits( iBarbarian, (73, 30), (82, 36), con.iCamelArcher, 1, iGameTurn, 12-iHandicap, 3, utils.outerInvasion, 0)
                if (iGameTurn >= getTurnForYear(190) and iGameTurn <= getTurnForYear(550)):
                        self.spawnUnits( iBarbarian, (73, 30), (82, 36), con.iCamelArcher, 2, iGameTurn, 9-iHandicap, 7, utils.outerInvasion, 0)

                #African natives
                if (gc.getPlayer(0).isPlayable()):  #late start condition
                        if (iGameTurn >= getTurnForYear(50) and iGameTurn <= getTurnForYear(690)):
                                self.spawnUnits( iNative, (58, 24), (72, 31), con.iZuluImpi, 3 + iHandicap, iGameTurn, 6, 4, utils.outerInvasion, 1)
                if (iGameTurn >= getTurnForYear(450) and iGameTurn <= getTurnForYear(1700)):
                        if (gc.getPlayer(0).isPlayable()):  #late start condition
                                self.spawnUnits( iNative, (60, 10), (72, 27), con.iZuluImpi, 3 + iHandicap, iGameTurn, 10, 4, utils.outerInvasion, 1)
                        else:
                                self.spawnUnits( iNative, (60, 10), (72, 27), con.iZuluImpi, 3 + iHandicap, iGameTurn, 15, 4, utils.outerInvasion, 1)
                #west africa
                if (iGameTurn >= getTurnForYear(450) and iGameTurn <= getTurnForYear(1700)):
                        self.spawnUnits( iBarbarian, (48, 26), (65, 37), con.iWarElephant, 2, iGameTurn, 16, 4, utils.outerInvasion, 1)
                        self.spawnUnits( iBarbarian, (48, 22), (63, 33), con.iZuluImpi, 2, iGameTurn, 16, 10, utils.outerInvasion, 1)

                #American natives
                if (iGameTurn >= getTurnForYear(600) and iGameTurn <= getTurnForYear(1100)):
                        self.spawnUnits( iBarbarian, (15, 38), (24, 47), con.iNativeAmericaDogSoldier, 2 + iHandicap, iGameTurn, 20, 0, utils.outerInvasion, 1)
                        if (gc.getPlayer(0).isPlayable()):  #late start condition
                                self.spawnUnits( iBarbarian, (15, 38), (24, 47), con.iAztecJaguar, 3, iGameTurn, 16 - 2*iHandicap, 10, utils.outerInvasion, 0)
                        else:  #late start condition
                                self.spawnUnits( iBarbarian, (15, 38), (24, 47), con.iAztecJaguar, 2, iGameTurn, 16 - 2*iHandicap, 10, utils.outerInvasion, 0)
                if (iGameTurn >= getTurnForYear(1300) and iGameTurn <= getTurnForYear(1600)):
                        self.spawnUnits( iBarbarian, (15, 38), (24, 47), con.iNativeAmericaDogSoldier, 3 + iHandicap, iGameTurn, 8, 0, utils.outerInvasion, 1)
                if (iGameTurn >= getTurnForYear(1400) and iGameTurn <= getTurnForYear(1800)):
                        self.spawnUnits( iNative, (11, 44), (33, 51), con.iNativeAmericaDogSoldier, 3 + iHandicap, iGameTurn, 8, 0, utils.outerInvasion, 1)
                        self.spawnUnits( iNative, (11, 44), (33, 51), con.iNativeAmericaDogSoldier, 3 + iHandicap, iGameTurn, 8, 4, utils.outerInvasion, 1)
                if (iGameTurn >= getTurnForYear(1300) and iGameTurn <= getTurnForYear(1600)):
                        if (iGameTurn % 18 == 0):
                                if (gc.getMap().plot(27, 29).getNumUnits() == 0):
                                        self.makeUnit(con.iNativeAmericaDogSoldier, iBarbarian, (27, 29), 3 + iHandicap, 1)
                        if (iGameTurn % 18 == 9):
                                if (gc.getMap().plot(30, 13).getNumUnits() == 0):
                                        self.makeUnit(con.iNativeAmericaDogSoldier, iBarbarian, (30, 13), 3 + iHandicap, 1)
                        
                #pirates in the Caribbean
                if (iGameTurn >= getTurnForYear(1600) and iGameTurn <= getTurnForYear(1800)):
                        self.spawnUnits( iBarbarian, (24, 32), (35, 46), con.iPrivateer, 1, iGameTurn, 5, 0, utils.outerSeaSpawn, 0)
                #pirates in Asia
                if (iGameTurn >= getTurnForYear(1500) and iGameTurn <= getTurnForYear(1900)):
                        self.spawnUnits( iBarbarian, (72, 24), (110, 36), con.iPrivateer, 1, iGameTurn, 8, 0, utils.outerSeaSpawn, 0)



                #self.foundCity(iIndependent, lUr, "Ur", iGameTurn, 1, con.iWarrior, 1)
                #self.foundCity(iIndependent2, lTyre, "Sur", iGameTurn, 1, con.iArcher, 1)
                self.foundCity(iIndependent, lJerusalem, "Yerushalayim", iGameTurn, 2, con.iArcher, 3)                        
                #self.foundCity(lBabylon, "Babel", iGameTurn, 1, con.iArcher, 1)
                self.foundCity(iIndependent2, lSusa, "Shushan", iGameTurn, 1, con.iArcher, 1)
                #self.foundCity(iIndependent, lKnossos, "Knossos", iGameTurn, 1, con.iWarrior, 0)                
                #self.foundCity(iBarbarian, lHattusas, "Hattusas", iGameTurn, 1, con.iChariot, 2)
                self.foundCity(iIndependent, lSamarkand, "Afrasiyab", iGameTurn, 1, con.iArcher, 1)
                #self.foundCity(iBarbarian, lNineveh, "Nineveh", iGameTurn, 1, -1, -1)
                #self.foundCity(lGadir, "Qart-Gadir", iGameTurn, 1, -1, -1)
                #self.foundCity(lLepcis, "Lpqy", iGameTurn, 2, -1, -1)
                #self.foundCity(lCarthage, "Qart-Hadasht", iGameTurn, 2, -1, -1)
                #self.foundCity(iBarbarian, lGordion, "Gordion", iGameTurn, 1, con.iChariot, 1)
                #self.foundCity(lPalermo, "Ziz", iGameTurn, 2, con.iArcher, 1)
                self.foundCity(iCeltia, lMilan, "Melpum", iGameTurn, 2, con.iArcher, 2)
                #self.foundCity(iBarbarian, lAugsburg, "Damasia", iGameTurn, 1, -1, -1)
                #self.foundCity(lRusadir, "Rusadir", iGameTurn, 2, -1, -1)
                self.foundCity(iCeltia, lLyon, "Lugodunon", iGameTurn, 2, -1, -1)
                #self.foundCity(iIndependent, lAxum, "Axum", iGameTurn, 1, -1, -1)
                self.foundCity(iCeltia, lBordeaux, "Burdigala", iGameTurn, 2, -1, -1)
                #self.foundCity(lCartagena, "Qart Hadasht", iGameTurn, 1, -1, -1)
                #self.foundCity(iIndependent, lSeoul, "Hanseong", iGameTurn, 2, -1, -1)
                self.foundCity(iIndependent2, lArtaxata, "Artashat", iGameTurn, 1, -1, -1)
                self.foundCity(iCeltia, lLutetia, "Lutetia", iGameTurn, 2, -1, -1)
                #self.foundCity(iNative, lTikal, "Tikal", iGameTurn, 1, -1, -1)
                self.foundCity(iIndependent, lSanaa, "Sana'a", iGameTurn, 1, -1, -1)
                self.foundCity(iIndependent2, lPagan, "Pagan", iGameTurn, 2, -1, -1)
                #self.foundCity(iCeltia, lInverness, "Inbhir Nis", iGameTurn, 2, -1, -1)
		#self.foundCity(iCeltia, lEdinburgh, "Dun Eideann", iGameTurn, 2, -1, -1)
                #self.foundCity(iNative, lChichenItza, "Chichen Itza", iGameTurn, 1, -1, -1)
                self.foundCity(iBarbarian, lBaku, "Bak&#252;", iGameTurn, 2, con.iArcher, -1)
                self.foundCity(iBarbarian, lLhasa, "Lasa", iGameTurn, 2, -1, -1)
                #bLhasaResult = self.foundCity(iBarbarian, lLhasa, "Lasa", iGameTurn, 2, -1, -1)
                #if (bLhasaResult == False):
                #        self.foundCity(iBarbarian, (lLhasa[0] - 1, lLhasa[1] - 1, lLhasa[2], lLhasa[3]), "Lhasa", iGameTurn, 2, -1, -1) #try to found it nearby
                #self.foundCity(iIndependent2, lAngkor, "Angkor", iGameTurn, 1, -1, -1)
                self.foundCity(iBarbarian, lHanoi, "Hanoi", iGameTurn, 2, -1, -1)
                self.foundCity(iNative, lTucume, "Tucume", iGameTurn, 1, -1, -1)
		self.foundCity(iIndependent, lKiev, "Kyiv", iGameTurn, 2, con.iLongbowman, 2)
                #self.foundCity(lJelling, "Jelling", iGameTurn, 1, -1, -1)
                if (gc.getPlayer(0).isPlayable()):  #late start condition
                        self.foundCity(iCeltia, lDublin, "&#193;th Cliath", iGameTurn, 1, -1, -1)
                else:
                        self.foundCity(iIndependent, lDublin, "&#193;th Cliath", iGameTurn, 1, -1, -1)
                #self.foundCity(lNidaros, "Nidaros", iGameTurn, 1, -1, -1)
                #self.foundCity(iNative, lZimbabwe, "Zimbabwe", iGameTurn, 1, con.iZuluImpi, 1)
                self.foundCity(iNative, lQuelimane, "Quelimane", iGameTurn, 1, con.iZuluImpi, 1)
                #self.foundCity(lUppsala, "Upsala", iGameTurn, 1, -1, -1)
                self.foundCity(iNative, lMombasa, "Mombasa", iGameTurn, 1, con.iZuluImpi, 1)
                self.foundCity(iBarbarian, lKazan, "Kazan", iGameTurn, 2, con.iHorseArcher, 1)
                self.foundCity(iNative, lKongo, "Mbanza Kongo", iGameTurn, 1, con.iZuluImpi, 1)

		self.foundCity(iIndependent, lThanjavur, "Thanjavur", iGameTurn, 1, con.iWarElephant, 1)
		self.foundCity(iIndependent, lMadras, "Madarasapatinam", iGameTurn, 2, con.iWarElephant, 2)

                if ( self.foundCity(iBarbarian, lDunhuang, "Dunhuang", iGameTurn, 1, con.iArcher, 1) ): #Orka                    
                        if (not gc.getPlayer(con.iChina).isHuman()): #Orka     
                                self.makeUnit(con.iHorseArcher, con.iChina, (99, 46), 3, 1)     
                self.foundCity(iBarbarian, lKashgar, "Kashgar", iGameTurn, 1, con.iArcher, 1) #Orka

		if utils.getHumanID() != con.iChina:
			self.foundCity(iIndependent, lBeijing, "Zhongdu", iGameTurn, 2, con.iSpearman, 1)

		self.foundCity(iBarbarian, lShenyang, "Simiyan hoton", iGameTurn, 2, con.iChariot, 2)


                #self.foundCity(iBarbarian, [59, 50, 146, 0], "Germanii", iGameTurn, 1, con.iArcher, 1)
                #self.foundCity(iBarbarian, [62, 51, 146, 0], "Goti", iGameTurn, 1, con.iArcher, 1)

		if iGameTurn == getTurnForYear(-3000):
			gc.getMap().plot(lJerusalem[0], lJerusalem[1]).getPlotCity().setHasRealBuilding(con.iTempleOfSalomon, True)



        def getCity(self, tCoords): #by LOQ
                'Returns a city at coordinates tCoords.'
                return CyGlobalContext().getMap().plot(tCoords[0], tCoords[1]).getPlotCity()

        def foundCity(self, iCiv, lCity, name, iTurn, iPopulation, iUnitType, iNumUnits):
                if ((iTurn == getTurnForYear(lCity[2]) + lCity[3]) and (lCity[3]<10)): # conversion from years - edead
                        #print self.checkRegion(tUr)
                        bResult, lCity[3] = self.checkRegion(lCity)
			print ("bResult: "+repr(bResult))
                        if (bResult == True):
                                pCiv = gc.getPlayer(iCiv)
				print ("Attempting to found city "+name+" with "+repr(lCity))
				# the code gets to this point, then crashes
                                pCiv.found(lCity[0], lCity[1])
				# this point is not reached anymore
				print "City founded"
                                self.getCity((lCity[0], lCity[1])).setName(name, False)
				print "Name set"
                                if (iPopulation != 1):
                                        self.getCity((lCity[0], lCity[1])).setPopulation(iPopulation)
					print "Population set"
                                if (iNumUnits > 0):
                                        self.makeUnit(iUnitType, iCiv, (lCity[0], lCity[1]), iNumUnits, 0)
					print "Units created"
                                return True
                        if (bResult == False) and (lCity[3] == -1):
                                return False
                               

        def checkRegion(self, tCity):
                cityPlot = gc.getMap().plot(tCity[0], tCity[1])
                iNumUnitsInAPlot = cityPlot.getNumUnits()
##                print iNumUnitsInAPlot
                
                #checks if the plot already belongs to someone
                if (cityPlot.isOwned()):
                        if (cityPlot.getOwner() != iBarbarian ):
                                return (False, -1)
                    
##                #checks if there's a unit on the plot
                if (iNumUnitsInAPlot):
                        for i in range(iNumUnitsInAPlot):
                                unit = cityPlot.getUnit(i)
                                iOwner = unit.getOwner()
                                if (iOwner == iBarbarian):
                                        return (False, tCity[3]+1) 
                                #pOwner = gc.getPlayer(iOwner)
                                #if (pOwner.isHuman()):
                                #        return (False, tCity[3]+1)                    

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
                for x in range(tCoords[0]-1, tCoords[0]+2):        # from x-1 to x+1
                        for y in range(tCoords[1]-1, tCoords[1]+2):	# from y-1 to y+1
                                killPlot = CyMap().getPlot(x, y)
                                for i in range(killPlot.getNumUnits()):
                                        unit = killPlot.getUnit(0)	# 0 instead of i because killing units changes the indices
                                        unit.kill(False, iBarbarian)

