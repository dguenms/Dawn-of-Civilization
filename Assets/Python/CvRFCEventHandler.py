from CvPythonExtensions import *
import CvUtil
import CvEventManager #Mercenaries
import sys #Mercenaries
import PyHelpers 
import CvMainInterface #Mercenaries
import CvMercenaryManager #Mercenaries
import MercenaryUtils #Mercenaries
import CvScreenEnums  #Mercenaries
#import CvConfigParser #Mercenaries #Rhye
import Popup as PyPopup 

#import StoredData
from StoredData import sd # edead
import RiseAndFall        
import Barbs                
import Religions        
import Resources        
import CityNameManager  
import UniquePowers     
import AIWars           
import Congresses
import Consts as con 
import RFCUtils
utils = RFCUtils.RFCUtils()
import CvScreenEnums #Mercenaries, Rhye
import Victory
import Stability
import Plague
import Communications
import Companies
import DynamicCivs
        
gc = CyGlobalContext()        
#iBetrayalCheaters = 15


#Rhye - start
iEgypt = con.iEgypt
iIndia = con.iIndia
iChina = con.iChina
iBabylonia = con.iBabylonia
iGreece = con.iGreece
iPersia = con.iPersia
iCarthage = con.iCarthage
iRome = con.iRome
iJapan = con.iJapan
iEthiopia = con.iEthiopia
iKorea = con.iKorea
iMaya = con.iMaya
iByzantium = con.iByzantium
iVikings = con.iVikings
iArabia = con.iArabia
iKhmer = con.iKhmer
iIndonesia = con.iIndonesia
iSpain = con.iSpain
iFrance = con.iFrance
iEngland = con.iEngland
iHolyRome = con.iHolyRome
iRussia = con.iRussia
iNetherlands = con.iNetherlands
iHolland = con.iHolland
iMali = con.iMali
iPortugal = con.iPortugal
iInca = con.iInca
iItaly = con.iItaly
iMongolia = con.iMongolia
iAztecs = con.iAztecs
iMughals = con.iMughals
iTurkey = con.iTurkey
iThailand = con.iThailand
iGermany = con.iGermany
iAmerica = con.iAmerica
iNumPlayers = con.iNumPlayers
iNumMajorPlayers = con.iNumMajorPlayers
iNumActivePlayers = con.iNumActivePlayers
iIndependent = con.iIndependent
iIndependent2 = con.iIndependent2
iNative = con.iNative
iCeltia = con.iCeltia
iSeljuks = con.iSeljuks
iBarbarian = con.iBarbarian
iNumTotalPlayers = con.iNumTotalPlayers
#Rhye - end



#Mercenaries - start
objMercenaryUtils = MercenaryUtils.MercenaryUtils()

PyPlayer = PyHelpers.PyPlayer
PyGame = PyHelpers.PyGame()
PyInfo = PyHelpers.PyInfo

# Set g_bGameTurnMercenaryCreation to true if mercenary creation should happen during the 
# onBeginGameTurn method, false if it should happen during the onBeginPlayerTurn method
# Default value is true
g_bGameTurnMercenaryCreation = true

# Set g_bDisplayMercenaryManagerOnBeginPlayerTurn to true if the "Mercenary Manager" 
# screen should be displayed at the beginning of every player turn. 
# Default value is false
g_bDisplayMercenaryManagerOnBeginPlayerTurn = false

# This value also controls the "Mercenary Manager" button and when it should be displayed.
# Default value is "ERA_ANCIENT"
#Rhye - start (was causing an assert)
#g_iStartingEra = gc.getInfoTypeForString("ERA_ANCIENT")
g_iStartingEra = 0
#Rhye - end

# Change this to false if mercenaries should be removed from the global mercenary pool 
# at the beginning of the game turn. When set to true a number of mercenaries will 
# wander away from the global mercenary pool. This is another variable used to control 
# the load time for the "Mercenary Manager" screen.
# Default valus is true
g_bWanderlustMercenaries = true

# Change this to increase the max number of mercenaries that may wander away from the
# global mercenary pool.
# Default valus is 3
g_iWanderlustMercenariesMaximum = 7 #Rhye

# Default valus is 0 
g_iWanderlustMercenariesMinimum = 2 #Rhye

# Change this to false to supress the mercenary messages.
# Default value is true
g_bDisplayMercenaryMessages = false #Rhye

# Set to true to print out debug messages in the logs
g_bDebug = false

# Default valus is 1 
g_bUpdatePeriod = 5 #Rhye

# Default valus is 1 
g_bAIThinkPeriod = 6 #Rhye (5 in Warlords, 4 in vanilla)

# globals

#Mercenaries - end


###################################################
class CvRFCEventHandler:



        mercenaryManager = None #Mercenaries


        def __init__(self, eventManager):

                self.EventKeyDown=6 #Mercenaries

                # initialize base class
                eventManager.addEventHandler("GameStart", self.onGameStart) #Stability
                eventManager.addEventHandler("BeginGameTurn", self.onBeginGameTurn) #Stability
                eventManager.addEventHandler("cityAcquired", self.onCityAcquired) #Stability
                eventManager.addEventHandler("cityRazed", self.onCityRazed) #Stability
                eventManager.addEventHandler("cityBuilt", self.onCityBuilt) #Stability
                eventManager.addEventHandler("combatResult", self.onCombatResult) #Stability
                #eventManager.addEventHandler("changeWar", self.onChangeWar)
                eventManager.addEventHandler("religionFounded",self.onReligionFounded) #Victory
                eventManager.addEventHandler("buildingBuilt",self.onBuildingBuilt) #Victory
                eventManager.addEventHandler("projectBuilt",self.onProjectBuilt) #Victory
                eventManager.addEventHandler("BeginPlayerTurn", self.onBeginPlayerTurn) #Mercenaries
                eventManager.addEventHandler("EndPlayerTurn", self.onEndPlayerTurn)
                eventManager.addEventHandler("EndGameTurn", self.onEndGameTurn) #Stability
                eventManager.addEventHandler("kbdEvent",self.onKbdEvent) #Mercenaries
                eventManager.addEventHandler("unitLost",self.onUnitLost) #Mercenaries
                eventManager.addEventHandler("unitKilled",self.onUnitKilled) #Mercenaries
                eventManager.addEventHandler("OnLoad",self.onLoadGame) #Mercenaries, StoredData-edead
                eventManager.addEventHandler("unitPromoted",self.onUnitPromoted) #Mercenaries
                eventManager.addEventHandler("techAcquired",self.onTechAcquired) #Mercenaries, Rhye #Stability
                #eventManager.addEventHandler("improvementDestroyed",self.onImprovementDestroyed) #Stability
                eventManager.addEventHandler("religionSpread",self.onReligionSpread) #Stability
                eventManager.addEventHandler("firstContact",self.onFirstContact)
                eventManager.addEventHandler("corporationFounded",self.onCorporationFounded) #Stability
                eventManager.addEventHandler("OnPreSave",self.onPreSave) #StoredData-edead
		eventManager.addEventHandler("playerChangeStateReligion", self.onPlayerChangeStateReligion)
		eventManager.addEventHandler("vassalState", self.onVassalState)
		eventManager.addEventHandler("revolution", self.onRevolution)
		eventManager.addEventHandler("cityGrowth", self.onCityGrowth)
		eventManager.addEventHandler("unitPillage", self.onUnitPillage)
		eventManager.addEventHandler("cityCaptureGold", self.onCityCaptureGold)
		
		#Leoreth: stability events
		eventManager.addEventHandler("greatDepression", self.onGreatDepression)
		eventManager.addEventHandler("postCommunism", self.onPostCommunism)
		eventManager.addEventHandler("democracyTransition", self.onDemocracyTransition)
                
		#Leoreth
		eventManager.addEventHandler("greatPersonBorn", self.onGreatPersonBorn)
               
                self.eventManager = eventManager

                #self.data = StoredData.StoredData()
                self.rnf = RiseAndFall.RiseAndFall()
                self.barb = Barbs.Barbs()
                self.rel = Religions.Religions()
                self.res = Resources.Resources()
                self.cnm = CityNameManager.CityNameManager()
                self.up = UniquePowers.UniquePowers()
                self.aiw = AIWars.AIWars()
                self.cong = Congresses.Congresses()
                self.vic = Victory.Victory()
                self.sta = Stability.Stability()
                self.pla = Plague.Plague()
                self.com = Communications.Communications()
                self.corp = Companies.Companies()
		self.dc = DynamicCivs.DynamicCivs()
                
                #Mercenaries - start
                
                self.mercenaryManager = CvMercenaryManager.CvMercenaryManager(CvScreenEnums.MERCENARY_MANAGER)        

                global g_bGameTurnMercenaryCreation
                global g_bDisplayMercenaryManagerOnBeginPlayerTurn
                global g_iStartingEra
                global g_bWanderlustMercenaries
                global g_iWanderlustMercenariesMaximum
                global g_bDisplayMercenaryMessages 

		#Rhye - start comment
##		# Load the Mercenaries Mod Config INI file containing all of the configuration information		
##		config = CvConfigParser.CvConfigParser("Mercenaries Mod Config.ini")
##
##		# If we actually were able to open the "Mercenaries Mod Config.ini" file then read in the values.
##		# otherwise we'll keep the default values that were set at the top of this file.
##		if(config != None):
##			g_bGameTurnMercenaryCreation = config.getboolean("Mercenaries Mod", "Game Turn Mercenary Creation", true)
##			g_bDisplayMercenaryManagerOnBeginPlayerTurn = config.getboolean("Mercenaries Mod", "Display Mercenary Manager On Begin Player Turn", false)
##			g_iStartingEra = gc.getInfoTypeForString(config.get("Mercenaries Mod","Starting Era","ERA_ANCIENT"))
##			g_bWanderlustMercenaries = config.getboolean("Mercenaries Mod", "Wanderlust Mercenaries", true)
##			g_iWanderlustMercenariesMaximum = config.getint("Mercenaries Mod","Wanderlust Mercenaries Maximum", 5)
##			g_bDisplayMercenaryMessages = config.getboolean("Mercenaries Mod", "Display Mercenary Messages", true)
		#Rhye - end comment

                objMercenaryUtils = MercenaryUtils.MercenaryUtils()
                #Mercenaries - end


        def onGameStart(self, argsList):
                'Called at the start of the game'
                #self.data.setupScriptData()
		
		print "Topkapi Palace ID: "+str(con.iTopkapiPalace)
		print "Class Plague ID: "+str(gc.getInfoTypeForString("BUILDINGCLASS_PLAGUE"))
		
                sd.setup() # edead
                self.rnf.setup()
                self.rel.setup()
                self.pla.setup()
		self.dc.setup()
                self.sta.setup()
                self.aiw.setup()
                self.rnf.warOnSpawn()

		s = ""
		for y in range(68):
			for x in range(124):
				s += str(gc.getMap().plot(x,68-y).getArea()) + ", "
			print s
			s = ""
			
		iCount = 0
		for x in range(con.tEuropeTL[0], con.tEuropeBR[0]+1):
			for y in range(con.tEuropeTL[1], con.tEuropeBR[1]+1):
				if not gc.getMap().plot(x, y).isWater(): iCount += 1
		
		if iCount != con.iEuropeTiles:
			utils.debugTextPopup('Europe: '+str(iCount))
			
		iCount = 0
		for x in range(con.tEasternEuropeTL[0], con.tEasternEuropeBR[0]+1):
			for y in range(con.tEasternEuropeTL[1], con.tEasternEuropeBR[1]+1):
				if not gc.getMap().plot(x, y).isWater(): iCount += 1
			
		if iCount != con.iEasternEuropeTiles:
			utils.debugTextPopup('Eastern Europe: '+str(iCount))
			
		iCount = 0
		for x in range(con.tNorthAmericaTL[0], con.tNorthAmericaBR[0]+1):
			for y in range(con.tNorthAmericaTL[1], con.tNorthAmericaBR[1]+1):
				if not gc.getMap().plot(x, y).isWater(): iCount += 1
			
		if iCount != con.iNorthAmericaTiles:
			utils.debugTextPopup('North America: '+str(iCount))
                

                #Mercenaries - start
                global objMercenaryUtils        
                objMercenaryUtils = MercenaryUtils.MercenaryUtils()
                #Mercenaries - end
                
                return 0


        def onCityAcquired(self, argsList):
                #'City Acquired'
                owner,playerType,city,bConquest,bTrade = argsList
		lTradingCompanyList = [con.iSpain, con.iFrance, con.iEngland, con.iPortugal, con.iNetherlands]
                #CvUtil.pyPrint('City Acquired Event: %s' %(city.getName()))
                self.cnm.renameCities(city, playerType)
                
                if (playerType == con.iArabia):
                        self.up.arabianUP(city)
                elif (playerType == con.iTurkey):
                        self.up.turkishUP(city, playerType, owner)
		elif (playerType == con.iMongolia and bConquest):
			self.up.mongolUP(city)
		elif (playerType == con.iMughals and utils.getHumanID() != con.iMughals):
			self.up.mughalUP(city)
		elif (playerType == con.iSeljuks):
			self.up.seljukUP(city)
			self.up.turkishUP(city, playerType, owner)
		elif playerType in lTradingCompanyList:
			if (city.getX(), city.getY()) in con.tTradingCompanyPlotLists[lTradingCompanyList.index(playerType)]:
				self.up.turkishUP(city, playerType, owner)

                if (playerType < iNumMajorPlayers):
                         utils.spreadMajorCulture(playerType, city.getX(), city.getY())

                self.sta.onCityAcquired(owner,playerType,city,bConquest,bTrade)

		#kill Byzantium
		if owner == iByzantium and gc.getPlayer(iByzantium).isAlive():
			if city.getX() == 68 and city.getY() == 45:
				if self.sta.getStability(iByzantium) < -40:
                                	print ("COLLAPSE: CIVIL WAR", gc.getPlayer(iByzantium).getCivilizationAdjective(0))
                                	if (owner != utils.getHumanID()):
                                		if (gc.getPlayer(utils.getHumanID()).canContact(iByzantium)):
                                        		CyInterface().addMessage(utils.getHumanID(), False, con.iDuration, gc.getPlayer(owner).getCivilizationDescription(0) + " " + CyTranslator().getText("TXT_KEY_STABILITY_CIVILWAR", ()), "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
                                        	if (gc.getGame().getGameTurn() < getTurnForYear(1400)):
                                                	utils.pickFragmentation(iByzantium, iIndependent, iIndependent2, iBarbarian, False)
                                        	else:
                                                	utils.pickFragmentation(iByzantium, iIndependent, iIndependent2, -1, False)
                                        else:
                                        	if (gc.getPlayer(iByzantium).getNumCities() > 1):
                                        		CyInterface().addMessage(iByzantium, True, con.iDuration, CyTranslator().getText("TXT_KEY_STABILITY_CIVILWAR_HUMAN", ()), "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
                                                	utils.pickFragmentation(iByzantium, iIndependent, iIndependent2, -1, True)
                                                	utils.setStartingStabilityParameters(iByzantium)
                                                	sd.scriptDict['lGNPold'][iByzantium] = 0
                                                	sd.scriptDict['lGNPnew'][iByzantium] = 0

                #kill byzantium
                #if (not gc.getPlayer(0).isPlayable()):  #late start condition
                #        if (owner == iCeltia and gc.getPlayer(iCeltia).isAlive()):
                #                if ((city.getX() == 68 and city.getY() == 45) or gc.getPlayer(iCeltia).getNumCities() <= 2): #constantinopolis captured or empire size <=2
                #                        print ("killed Byzantium")
                #                        utils.killAndFragmentCiv(iCeltia, iIndependent, iIndependent2, -1, False)

		#kill Seljuks
		if owner == iSeljuks and gc.getPlayer(iSeljuks).isAlive():
			if city.isCapital() or gc.getPlayer(iSeljuks).getNumCities() <= 2:
				print "Killed Seljuks"
				utils.killAndFragmentCiv(iSeljuks, iIndependent, iIndependent2, -1, False)
				
		# Leoreth: relocate capital for AI if reacquired:
		if utils.getHumanID() != playerType and playerType < con.iNumPlayers:
			if sd.scriptDict['lResurrections'][playerType] == 0:
				if (city.getX(), city.getY()) == con.tCapitals[utils.getReborn(playerType)][playerType]:
					utils.relocateCapital(playerType, city)
			else:
				if (city.getX(), city.getY()) == con.tRespawnCapitals[playerType]:
					utils.relocateCapital(playerType, city)

                
                if (bConquest):
                        #self.rnf.collapseCapitals(owner, city, playerType)
                        if (owner == utils.getHumanID() and playerType != con.iBarbarian):
                                self.rnf.collapseHuman(owner, city, playerType)
                        #print ("exile data:", self.rnf.getExileData(0), city.getX(), self.rnf.getExileData(1), city.getY(), self.rnf.getExileData(2))
                        if (self.rnf.getExileData(0) == city.getX() and self.rnf.getExileData(1) == city.getY()):
                                if (playerType == utils.getHumanID() and self.rnf.getExileData(2) != -1):
                                        self.rnf.escape(city)
                if (bTrade):
                        for i in range (con.iScotlandYard +1 - con.iHeroicEpic):
                                iNationalWonder = i + con.iHeroicEpic
                                if (city.hasBuilding(iNationalWonder)):
                                        city.setHasRealBuilding((iNationalWonder), False)

                self.pla.onCityAcquired(owner,playerType,city) #Plague

                self.com.onCityAcquired(city) #Communications

                self.vic.onCityAcquired(owner, playerType, bConquest, city) #Victory

		self.corp.onCityAcquired(argsList) #Companies

		self.dc.onCityAcquired(argsList) #DynamicCivs
                
                return 0

        def onCityRazed(self, argsList):
                #'City Razed'
                city, iPlayer = argsList

                self.sta.onCityRazed(city.getOwner(),iPlayer,city)
		self.dc.onCityRazed(argsList)
		
#                if (iPlayer == con.iMongolia):
#                        self.up.setLatestRazeData(0, gc.getGame().getGameTurn())
#                        owner = city.getOwner()
#                        if (city.getOwner() == iPlayer):
#                                if (city.getPreviousOwner() != -1):
#                                        owner = city.getPreviousOwner()                        
#                        self.up.setLatestRazeData(1, owner)
#                        self.up.setLatestRazeData(2, city.getPopulation())
#                        self.up.setLatestRazeData(3, city.getX())
#                        self.up.setLatestRazeData(4, city.getY())
#                        print ("city.getPopulation()", city.getPopulation())
#                        print ("prev", city.getPreviousOwner(), "curr", city.getOwner())
#                        self.up.setMongolAI()

                self.pla.onCityRazed(city,iPlayer) #Plague
                        
                if (iPlayer == con.iMongolia):
                        self.vic.onCityRazed(iPlayer) #Victory



        def onCityBuilt(self, argsList):
                'City Built'
                city = argsList[0]
                
                iOwner = city.getOwner()
                
                if (iOwner < con.iNumActivePlayers): 
                        self.cnm.assignName(city)


                #Rhye - delete culture of barbs and minor civs to prevent weird unhappiness
                pCurrent = gc.getMap().plot( city.getX(), city.getY() )
                for i in range(con.iNumTotalPlayers - con.iNumActivePlayers):
                        iMinorCiv = i + con.iNumActivePlayers
                        pCurrent.setCulture(iMinorCiv, 0, True)
                pCurrent.setCulture(con.iBarbarian, 0, True)

                if (iOwner < iNumMajorPlayers):
                        utils.spreadMajorCulture(iOwner, city.getX(), city.getY())


                if (iOwner == con.iTurkey):
                        self.up.turkishUP(city, iOwner, -1)
			
		if (iOwner == con.iCarthage):
			if city.getX() == 58 and city.getY() == 39:
				if not gc.getPlayer(con.iCarthage).isHuman():
					x = gc.getPlayer(con.iCarthage).getCapitalCity().getX()
					y = gc.getPlayer(con.iCarthage).getCapitalCity().getY()
					gc.getMap().plot(58,39).getPlotCity().setHasRealBuilding(con.iPalace, True)
					gc.getMap().plot(x,y).getPlotCity().setHasRealBuilding(con.iPalace, False)
				self.dc.setCivAdjective(iOwner, "TXT_KEY_CIV_CARTHAGE_ADJECTIVE")
				self.dc.setCivShortDesc(iOwner, "TXT_KEY_CIV_CARTHAGE_SHORT_DESC")


                if (self.vic.getNewWorld(0) == -1):
                        if (iOwner not in con.lCivGroups[5] and iOwner < iNumActivePlayers):
                                if (city.getX() >= con.tAmericasTL[0] and city.getX() <= con.tAmericasBR[0] and city.getY() >= con.tAmericasTL[1] and city.getY() <= con.tAmericasBR[1]):
                                        self.vic.setNewWorld(0, iOwner)
                                        if (iOwner != iVikings):
                                                self.vic.setGoal(iVikings, 2, 0)
                                        if (iOwner != iSpain):
                                                self.vic.setGoal(iSpain, 0, 0) 

                if (iOwner == con.iRussia or \
                    iOwner == con.iFrance or \
                    iOwner == con.iEngland or \
                    iOwner == con.iSpain or \
                    #iOwner == con.iCarthage or \
                    iOwner == con.iVikings or \
                    iOwner == con.iPortugal or \
                    iOwner == con.iNetherlands):    
                        self.vic.onCityBuilt(city, iOwner) #Victory

                if (iOwner < con.iNumPlayers):
                        self.sta.onCityBuilt(iOwner, city.getX(), city.getY() )
			self.dc.onCityBuilt(iOwner)

		if iOwner == con.iArabia:
			if not gc.getGame().isReligionFounded(con.iIslam):
				if (city.getX(), city.getY()) == (75, 33):
					self.rel.foundReligion((75, 33), con.iIslam)

        def onPlayerChangeStateReligion(self, argsList):
		'Player changes his state religion'
		iPlayer, iNewReligion, iOldReligion = argsList
		
		if iPlayer < iNumPlayers:
			self.dc.onPlayerChangeStateReligion(argsList)

        def onCombatResult(self, argsList):
                self.up.aztecUP(argsList)
		#self.up.romanCombatUP(argsList)
                self.vic.onCombatResult(argsList)
                self.sta.onCombatResult(argsList)
                self.rnf.immuneMode(argsList)
		self.up.vikingUP(argsList)



##        def onChangeWar(self, argsList):
##                print ("No cheaters1")
##                if (bIsWar):
##                        print ("No cheaters2")
##                        if (argsList[1] == utils.getHumanID() and gc.getGame().getGameTurn() <= con.tBirth[argsList[1]] + iBetrayalCheaters):
##                                print ("No cheaters3")
##                                self.rnf.setNewCivFlip(argsList[1])
##                                self.rnf.setTempTopLeft(rnf.tCoreAreasTL[argsList[1]])
##                                self.rnf.setTempBottomRight(rnf.tCoreAreasBR[argsList[1]])
##                                self.rnf.setBetrayalTurns(rnf.iBetrayalPeriod)
##                                self.rnf.initBetrayal()

        def onReligionFounded(self, argsList):
                'Religion Founded'
                iReligion, iFounder = argsList

		print 'Religion founded: '+str(iReligion)

                if (not gc.getPlayer(0).isPlayable() and gc.getGame().getGameTurn() == getTurnForYear(600)): #late start condition
                        return
        
                self.vic.onReligionFounded(iReligion, iFounder)
        
                if (iFounder < con.iNumPlayers):
                        self.sta.onReligionFounded(iFounder)


	def onCorporationFounded(self, argsList):
		'Corporation Founded'
		iCorporation, iFounder = argsList
		#player = PyPlayer(iFounder)
		
                if (iFounder < con.iNumPlayers):
                        self.sta.onCorporationFounded(iFounder)

        def onVassalState(self, argsList):
		'Vassal State'
		print "Check 1 passed"
		iMaster, iVassal, bVassal, bCapitulated = argsList
		
		if iVassal == con.iAztecs:
			gc.getPlayer(con.iAztecs).setReborn()
		elif iVassal == con.iInca:
			gc.getPlayer(con.iInca).setReborn()
		
		self.dc.onVassalState(argsList)
		
		if bCapitulated:
			self.sta.onVassalState(iVassal, bCapitulated)
		
		if iMaster == iHolyRome:
			self.vic.onVassalState(iMaster, iVassal)

	def onRevolution(self, argsList):
		'Called at the start of a revolution'
		iPlayer = argsList[0]
		
		if iPlayer < iNumPlayers:
			self.dc.onRevolution(iPlayer)
			
	def onCityGrowth(self, argsList):
		'City Population Growth'
		pCity = argsList[0]
		iPlayer = argsList[1]
		
		# Leoreth/Voyhkah: Empire State Building effect
		if pCity.isHasRealBuilding(con.iEmpireState):
                        iPop = pCity.getPopulation()
                        pCity.setBuildingCommerceChange(gc.getInfoTypeForString("BUILDINGCLASS_EMPIRE_STATE"), 0, iPop)
			
	def onGreatDepression(self, argsList):
		iPlayer = argsList[0]
		bAcquired = argsList[1]
		
		if bAcquired:
			CyInterface().addMessage(iPlayer, False, con.iDuration, CyTranslator().getText("TXT_KEY_STABILITY_GREAT_DEPRESSION_INFLUENCE", (gc.getPlayer(iLoopCiv).getCivilizationDescription(0),)), "", 0, "", ColorTypes(con.iOrange), -1, -1, True, True)
		else:
			CyInterface().addMessage(iPlayer, False, con.iDuration, CyTranslator().getText("TXT_KEY_STABILITY_PERIOD", ()) + " " + CyTranslator().getText("TXT_KEY_STABILITY_GREAT_DEPRESSION", ()), "", 0, "", ColorTypes(con.iOrange), -1, -1, True, True)
	
	def onPostCommunism(self, argsList):
		iPlayer = argsList[0]
		
		CyInterface().addMessage(iPlayer, False, con.iDuration, CyTranslator().getText("TXT_KEY_STABILITY_PERIOD", ()) + " " + CyTranslator().getText("TXT_KEY_STABILITY_POST_COMMUNISM", ()), "", 0, "", ColorTypes(con.iOrange), -1, -1, True, True)
		
	def onDemocracyTransition(self, argsList):
		iPlayer = argsList[0]
		
		CyInterface().addMessage(iPlayer, False, con.iDuration, CyTranslator().getText("TXT_KEY_STABILITY_PERIOD", ()) + " " + CyTranslator().getText("TXT_KEY_STABILITY_DEMOCRACY", ()), "", 0, "", ColorTypes(con.iOrange), -1, -1, True, True)

	def onUnitPillage(self, argsList):
		unit, iImprovement, iRoute, iPlayer, iGold = argsList
		
		if iPlayer == con.iVikings and iGold > 0:
			self.vic.onUnitPillage(iPlayer, iGold)
			
	def onCityCaptureGold(self, argsList):
		city, iPlayer, iGold = argsList
		
		if iPlayer == con.iVikings and iGold > 0:
			self.vic.onCityCaptureGold(iPlayer, iGold)
			
	
		
        def onBuildingBuilt(self, argsList):
                city, iBuildingType = argsList
                iOwner = city.getOwner()
                self.vic.onBuildingBuilt(city.getOwner(), iBuildingType)
                if (city.getOwner() < con.iNumPlayers):
                        self.sta.onBuildingBuilt(iOwner, iBuildingType, city)
                        self.com.onBuildingBuilt(iOwner, iBuildingType, city)
                self.cong.onBuildingBuilt(iOwner, iBuildingType, city)

		# Leoreth: Apostolic Palace moves holy city
		if iBuildingType == con.iApostolicPalace:
			print "Found Orthodoxy"
			self.rel.foundOrthodoxy(iOwner)
			gc.getGame().setHolyCity(con.iChristianity, city, False)

		# Leoreth: update trade routes when Porcelain Tower is built to start its effect
		if iBuildingType == con.iPorcelainTower:
			gc.getPlayer(iOwner).updateTradeRoutes()

		# Leoreth/Voyhkah: Empire State Building
		if iBuildingType == con.iEmpireState:
			iPop = city.getPopulation()
			city.setBuildingCommerceChange(gc.getInfoTypeForString("BUILDINGCLASS_EMPIRE_STATE"), 0, iPop)

		# Leoreth: found Buddhism when a Hindu temple is built
		if iBuildingType == con.iHinduTemple:
			self.rel.foundBuddhism(city)


        def onProjectBuilt(self, argsList):
                city, iProjectType = argsList
                self.vic.onProjectBuilt(city.getOwner(), iProjectType)
                if (city.getOwner() < con.iNumPlayers):
                        self.sta.onProjectBuilt(city.getOwner(), iProjectType)
			
		self.rnf.onProjectBuilt(city, iProjectType)

        def onImprovementDestroyed(self, argsList):
                pass
                #iImprovement, iOwner, iX, iY = argsList
                #if (iOwner < con.iNumPlayers):
                #        self.sta.onImprovementDestroyed(iOwner)           
                
        def onBeginGameTurn(self, argsList):
                iGameTurn = argsList[0]

                print ("iGameTurn", iGameTurn)
                self.printDebug(iGameTurn)

                #debug - stop autoplay
                #utils.makeUnit(con.iAxeman, con.iAmerica, (0,0), 1)
                #if (iGameTurn == 300):
                #        utils.makeUnit(con.iAxeman, con.iAmerica, (0,0), 1)

                
                self.rnf.checkTurn(iGameTurn)
                self.barb.checkTurn(iGameTurn)
                self.rel.checkTurn(iGameTurn)
                self.res.checkTurn(iGameTurn)
                self.up.checkTurn(iGameTurn)
                self.aiw.checkTurn(iGameTurn)
                self.cong.checkTurn(iGameTurn)
                self.pla.checkTurn(iGameTurn)
                self.vic.checkTurn(iGameTurn)
                self.sta.checkTurn(iGameTurn)
                self.com.checkTurn(iGameTurn)
		self.corp.checkTurn(iGameTurn)
		if iGameTurn % 10 == 0:
                        self.dc.checkTurn(iGameTurn)

                #Mercenaries - start

                if ((not gc.getTeam(gc.getActivePlayer().getTeam()).isHasTech(con.iNationalism)) and gc.getGame().getGameTurn() >= getTurnForYear(con.tBirth[utils.getHumanID()])):
                        
                        # Get the list of active players in the game
                        playerList = PyGame.getCivPlayerList()
                        
                        # Go through each of the players and deduct their mercenary maintenance amount from their gold
                        for i in range(len(playerList)):
                                playerList[i].setGold(playerList[i].getGold()-objMercenaryUtils.getPlayerMercenaryMaintenanceCost(playerList[i].getID()))
                                playerList[i].setGold(playerList[i].getGold()+objMercenaryUtils.getPlayerMercenaryContractIncome(playerList[i].getID()))
                
                        # Have some mercenaries wander away from the global mercenary pool if 
                        # g_bWanderlustMercenaries is set to true.        
                        if(g_bWanderlustMercenaries):

                                #Rhye - start (less frequent updates)
                                #wanderingMercenaryCount = gc.getGame().getMapRand().get(g_iWanderlustMercenariesMaximum, "Random Num")
                                #objMercenaryUtils.removeMercenariesFromPool(wanderingMercenaryCount)
                                teamPlayer = gc.getTeam(gc.getActivePlayer().getTeam())
                                if (not teamPlayer.isHasTech(con.iNationalism)):                     
                                        if (iGameTurn % g_bUpdatePeriod == (g_bUpdatePeriod-1)):
                                                wanderingMercenaryCount = gc.getGame().getMapRand().get(g_iWanderlustMercenariesMaximum, "Random Num") + g_iWanderlustMercenariesMinimum
                                                objMercenaryUtils.removeMercenariesFromPool(wanderingMercenaryCount)
                                #Rhye - end
                            
                                
                        # Add the mercenaries to the global mercenary pool if the g_bGameTurnMercenaryCreation 
                        # is set to true
                        if(g_bGameTurnMercenaryCreation):
                            
                                #Rhye - start (less frequent updates)
                                #objMercenaryUtils.addMercenariesToPool()                  
                                if (iGameTurn % g_bUpdatePeriod == (g_bUpdatePeriod-1)):
                                        objMercenaryUtils.addMercenariesToPool()
                                #Rhye - end                
                return 0



        def onBeginPlayerTurn(self, argsList):        
                iGameTurn, iPlayer = argsList

                print ("PLAYER", iPlayer, gc.getGame().getGameTurnYear())
                #if (iPlayer == con.iMongolia):
                #        if (iGameTurn == self.up.getLatestRazeData(0) +1):
                #                self.up.setMongolAI()
                
                #debug - stop autoplay
                #utils.makeUnit(con.iAxeman, iAmerica, (0,0), 1)

                if (self.rnf.getDeleteMode(0) != -1):
                        self.rnf.deleteMode(iPlayer)
                        
                self.pla.checkPlayerTurn(iGameTurn, iPlayer)
		#self.cnm.checkPlayerTurn(iGameTurn, iPlayer)

                if (gc.getPlayer(iPlayer).isAlive()):
                        self.vic.checkPlayerTurn(iGameTurn, iPlayer)


                if (gc.getPlayer(iPlayer).isAlive() and iPlayer < con.iNumPlayers and gc.getPlayer(iPlayer).getNumCities() > 0):
                        self.sta.updateBaseStability(iGameTurn, iPlayer)

                if (gc.getPlayer(iPlayer).isAlive() and iPlayer < con.iNumPlayers and not gc.getPlayer(iPlayer).isHuman()):
                        self.rnf.checkPlayerTurn(iGameTurn, iPlayer) #for leaders switch

                #Mercenaries - start
        
                # This method will add mercenaries to the global mercenary pool, display the mercenary manager screen
                # and provide the logic to make the computer players think.
                player = gc.getPlayer(iPlayer)

                if ((not gc.getTeam(gc.getActivePlayer().getTeam()).isHasTech(con.iNationalism)) and gc.getGame().getGameTurn() >= getTurnForYear(con.tBirth[utils.getHumanID()])): #Rhye

                        # Debug code - start
                        if(g_bDebug):
                                CvUtil.pyPrint(player.getName() + " Gold: " + str(player.getGold()) + " is human: " + str(player.isHuman()))
                        # Debug code - end        
                        
                        # Add the mercenaries to the global mercenary pool if the 
                        # g_bGameTurnMercenaryCreation is set to false
                        if(not g_bGameTurnMercenaryCreation):
                                objMercenaryUtils.addMercenariesToPool()

                        # if g_bDisplayMercenaryManagerOnBeginPlayerTurn is true the the player is human
                        # then display the mercenary manager screen
                        if(g_bDisplayMercenaryManagerOnBeginPlayerTurn and player.isHuman()):
                                self.mercenaryManager.interfaceScreen()

                        # if the player is not human then run the think method
                        if(not player.isHuman()):
                            
                                #Rhye - start
                                #objMercenaryUtils.computerPlayerThink(iPlayer)                                        
                                if (player.isAlive()):
                                        if (iPlayer % (g_bAIThinkPeriod) == iGameTurn % (g_bAIThinkPeriod) and not gc.getTeam(player.getTeam()).isHasTech(con.iNationalism)):
                                                print ("AI thinking (Mercenaries)", iPlayer) #Rhye
                                                objMercenaryUtils.computerPlayerThink(iPlayer)                                                                
                                #Rhye - end
                
                        # Place any mercenaries that might be ready to be placed.
                        objMercenaryUtils.placeMercenaries(iPlayer)
                print ("PLAYER FINE", iPlayer)

        
        def onEndPlayerTurn(self, argsList):

                iGameTurn, iPlayer = argsList
                print ("END PLAYER", iPlayer)
                
                'Called at the end of a players turn'

##                if ((not gc.getTeam(gc.getActivePlayer().getTeam()).isHasTech(con.iNationalism)) and gc.getGame().getGameTurn() >= getTurnForYear(con.tBirth[utils.getHumanID()])): #Rhye
##                
##                        iGameTurn, iPlayer = argsList
##                        
##                        player = gc.getPlayer(iPlayer)
##
##                        CyInterface().addImmediateMessage(player.getName(),"")
##                #print ("END PLAYER FINE", iPlayer)

	def onGreatPersonBorn(self, argsList):
		'Great Person Born'
		pUnit, iPlayer, pCity = argsList
		player = PyPlayer(iPlayer)
		infoUnit = pUnit.getUnitClassType()

		self.vic.onGreatPersonBorn(argsList)
		
		# Check if we should even show the popup:
		if pUnit.isNone() or pCity.isNone():
			return
		
		#if(len(pUnit.getNameNoDesc()) == 0): # Rename units with no names - important to avoid confusion with event log
			
		#iCivilizationType = player.player.getCivilizationType()
		# Pass the civilization and unit type along to the renamer
		#pUnit.setName(CivSpecificGreatPeopleModNameUtils.generateCivilizationName(iCivilizationType, infoUnit))


        def onEndGameTurn(self, argsList):
            
                iGameTurn = argsList[0]
                self.sta.checkImplosion(iGameTurn)
		
		# Leoreth: test stability on divergences every 5 turns
		if iGameTurn % utils.getTurns(5) == 0:
			for iPlayer in range(con.iNumPlayers):
				if gc.getPlayer(iPlayer).isAlive():
					print "PYTHON: Player " + str(iPlayer) + " base stability: " + str(self.sta.getBaseStabilityLastTurn(iPlayer))
					print "DLL: Player " + str(iPlayer) + " base stability: " + str(gc.getPlayer(iPlayer).getBaseStabilityLastTurn())
					#lStabilityList = gc.getPlayer(iPlayer).getStabilityList()
					#for tStabilityTuple in lStabilityList:
					#	print str(tStabilityTuple)


        def onReligionSpread(self, argsList):
            
                iReligion, iOwner, pSpreadCity = argsList
                self.sta.onReligionSpread(iReligion, iOwner)

		#Leoreth: if state religion spreads, pagan temples are replaced with its temple. For other religions, they're simply removed.         
		if pSpreadCity.isHasBuilding(con.iObelisk):
			pSpreadCity.setHasRealBuilding(con.iObelisk, False)
			if gc.getPlayer(iOwner).getCivics(4) != con.iPantheon and gc.getPlayer(iOwner).getStateReligion() == iReligion and gc.getTeam(iOwner).isHasTech(con.iPriesthood):
				pSpreadCity.setHasRealBuilding(con.iJewishTemple+4*iReligion, True)
                                CyInterface().addMessage(iOwner, True, con.iDuration, CyTranslator().getText("TXT_KEY_PAGAN_TEMPLE_REPLACED", (str(gc.getReligionInfo(iReligion).getText()), str(pSpreadCity.getName()), str(gc.getBuildingInfo(con.iJewishTemple+4*iReligion).getText()))), "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)
			else:
				CyInterface().addMessage(iOwner, True, con.iDuration, CyTranslator().getText("TXT_KEY_PAGAN_TEMPLE_REMOVED", (str(gc.getReligionInfo(iReligion).getText()), str(pSpreadCity.getName()))), "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)


        def onFirstContact(self, argsList):
            
                iTeamX,iHasMetTeamY = argsList
		print("Team "+str(iTeamX)+" has made first contact with team "+str(iHasMetTeamY)+".")
                self.rnf.onFirstContact(iTeamX, iHasMetTeamY)
                self.pla.onFirstContact(iTeamX, iHasMetTeamY)

        #Rhye - start
        def onTechAcquired(self, argsList):

                #print ("onTechAcquired", argsList)
                iPlayer = argsList[2]

                iHuman = utils.getHumanID()
                
                if (not gc.getPlayer(0).isPlayable() and gc.getGame().getGameTurn() == getTurnForYear(600)): #late start condition
                        return
                
                if (gc.getGame().getGameTurn() > getTurnForYear(con.tBirth[iPlayer])):                            
                	self.vic.onTechAcquired(argsList[0], argsList[2])
                        self.cnm.onTechAcquired(argsList[2])

                if (gc.getPlayer(iPlayer).isAlive() and gc.getGame().getGameTurn() > getTurnForYear(con.tBirth[iPlayer]) and iPlayer < con.iNumPlayers):
                        self.rel.onTechAcquired(argsList[0], argsList[2])
                
                if (gc.getPlayer(iPlayer).isAlive() and gc.getGame().getGameTurn() > getTurnForYear(con.tBirth[iPlayer]) and iPlayer < con.iNumPlayers):
                        self.sta.onTechAcquired(argsList[0], argsList[2])

                        if (gc.getGame().getGameTurn() > getTurnForYear(1700)):
                                self.aiw.forgetMemory(argsList[0], argsList[2])

                if (gc.getGame().getGameTurn() > getTurnForYear(1000)):
                        self.cong.onTechAcquired(argsList[0], argsList[2])

                if (argsList[0] == con.iAstronomy):
			self.rnf.onAstronomyDiscovered(argsList[2])
                        if (iPlayer == con.iSpain or \
                            iPlayer == con.iFrance or \
                            iPlayer == con.iEngland or \
                            iPlayer == con.iGermany or \
                            iPlayer == con.iVikings or \
                            iPlayer == con.iNetherlands or \
                            iPlayer == con.iPortugal):  
                                self.rnf.setAstronomyTurn(iPlayer, gc.getGame().getGameTurn())
                if (argsList[0] == con.iCompass):
                        if (iPlayer == con.iVikings):
                                gc.getMap().plot(49, 62).setTerrainType(con.iCoast, True, True)
                if (argsList[0] == con.iMedicine):
                        self.pla.onTechAcquired(argsList[0], argsList[2])

		if (argsList[0] == con.iEconomics):
			self.rnf.onEconomicsDiscovered(argsList[2])
			
		if argsList[0] == con.iRailroad:
			self.rnf.onRailroadDiscovered(argsList[2])
                    
                if (gc.getGame().getGameTurn() >= getTurnForYear(con.tBirth[iHuman])):

                        if (argsList[0] == con.iNationalism):
                                if (argsList[2] == iHuman):
                                        for iLoopCiv in range (con.iNumPlayers):
                                    
                                                mercenaryDict = objMercenaryUtils.getPlayerMercenaries(iLoopCiv)
                                                mercenary = objMercenaryUtils.getHighestMaintenanceMercenary(mercenaryDict)

                                                while(mercenary != None):
                                                        # Get the mercenary with the highest maintenance cost
                                                        mercenaryDict = objMercenaryUtils.getPlayerMercenaries(iLoopCiv)
                                                        mercenary = objMercenaryUtils.getHighestMaintenanceMercenary(mercenaryDict)
                                                        # Have the computer fire the mercenary
                                                        if(mercenary != None):
                                                                objMercenaryUtils.fireMercenary(mercenary.getName(), iLoopCiv)
                                        screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
                                        screen.hide("MercenaryManagerButton")
                                        CyInterface().addMessage(iHuman, False, con.iDuration, CyTranslator().getText("TXT_KEY_MERCENARIES_DISABLED", ()), "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)
                                
        #Rhye - end
                

        def onPreSave(self, argsList):
                'called before a game is actually saved'
                sd.save() # edead: pickle & save script data


        # This method creates a new instance of the MercenaryUtils class to be used later
        def onLoadGame(self, argsList):

                sd.load() # edead: load & unpickle script data

                if ((not gc.getTeam(gc.getActivePlayer().getTeam()).isHasTech(con.iNationalism)) and gc.getGame().getGameTurn() >= getTurnForYear(con.tBirth[utils.getHumanID()])): #Rhye

                        global objMercenaryUtils

                        objMercenaryUtils = MercenaryUtils.MercenaryUtils()



        # This method will redraw the main interface once a unit is promoted. This way the 
        # gold/turn information will be updated.        
        def onUnitPromoted(self, argsList):
                'Unit Promoted'

                if ((not gc.getTeam(gc.getActivePlayer().getTeam()).isHasTech(con.iNationalism)) and gc.getGame().getGameTurn() >= getTurnForYear(con.tBirth[utils.getHumanID()])): #Rhye        
                        pUnit, iPromotion = argsList
                        player = PyPlayer(pUnit.getOwner())

                        if(objMercenaryUtils.isMercenary(pUnit)):
                                CyInterface().setDirty(InterfaceDirtyBits.GameData_DIRTY_BIT, True)




        # This method will remove a mercenary unit from the game if it is killed
        def onUnitKilled(self, argsList):
                'Unit Killed'

                if ((not gc.getTeam(gc.getActivePlayer().getTeam()).isHasTech(con.iNationalism)) and gc.getGame().getGameTurn() >= getTurnForYear(con.tBirth[utils.getHumanID()])): #Rhye
                    
                        unit, iAttacker = argsList
                        
                        mercenary = objMercenaryUtils.getMercenary(unit.getNameNoDesc())

                        if(mercenary != None and g_bDisplayMercenaryMessages and mercenary.getBuilder() != -1 and unit.isDead()):
                                strMessage = mercenary.getName() + " has died under " + gc.getPlayer(mercenary.getOwner()).getName() + "'s service."
                                # Inform the player that the mercenary has died.
                                CyInterface().addMessage(mercenary.getBuilder(), True, 20, strMessage, "", 0, "", ColorTypes(0), -1, -1, True, True) 

                        objMercenaryUtils.removePlayerMercenary(unit)


        # This method will remove a mercenary unit from the game if it is lost
        def onUnitLost(self, argsList):
                'Unit Lost'

                if ((not gc.getTeam(gc.getActivePlayer().getTeam()).isHasTech(con.iNationalism)) and gc.getGame().getGameTurn() >= getTurnForYear(con.tBirth[utils.getHumanID()])): #Rhye
        
                        unit = argsList[0]
                        
                        # Debug code - start
                        if(g_bDebug):
                                CvUtil.pyPrint("lost: " + unit.getName())
                        # Debug code - end
                        
                        # If the unit being lost is a mercenary, check to see if they have been
                        # replaced by an upgraded version of themselves. If they are then save
                        # the new upgraded version of themselves and return immediately.
                        if(objMercenaryUtils.isMercenary(unit)):

                                # Debug code - start
                                if(g_bDebug):        
                                        CvUtil.pyPrint("mercenary unit lost: " + unit.getName())
                                # Debug code - end
                                        
                                # Get the active player ID
                                iPlayer = gc.getGame().getActivePlayer()
                                
                                # Get the reference of the actual player
                                pyPlayer = PyPlayer(iPlayer)

                                # Get the list of units for the player
                                unitList = pyPlayer.getUnitList()
                                        
                                # Go through the list of units to see if an upgraded version of 
                                # the unit has been added. If it exists then save it and return
                                # immediately.
                                for unit in unitList:

                                        if(unit.getUnitType() != argsList[0].getUnitType() and unit.getNameNoDesc() == argsList[0].getNameNoDesc()):

                                                # Debug code - start
                                                if(g_bDebug):        
                                                        CvUtil.pyPrint("mercenary unit upgraded: " + unit.getName())
                                                # Debug code - end
                                                
                                                tmpMerc = objMercenaryUtils.createBlankMercenary()
                                                tmpMerc.loadUnitData(unit)
                                                tmpMerc.iBuilder = -1
                                                objMercenaryUtils.saveMercenary(tmpMerc)
                                                return
                                                
                        mercenary = objMercenaryUtils.getMercenary(unit.getNameNoDesc())

                        if(mercenary != None and g_bDisplayMercenaryMessages and mercenary.getBuilder() != -1 and unit.isDead()):
                                strMessage = mercenary.getName() + " was lost under " + gc.getPlayer(mercenary.getOwner()).getName() + "'s service."
                                # Inform the player that the mercenary has died.
                                CyInterface().addMessage(mercenary.getBuilder(), True, 20, strMessage, "", 0, "", ColorTypes(0), -1, -1, True, True) 
                        unit = argsList[0]
                        
                        # Debug code - start
                        if(g_bDebug):        
                                CvUtil.pyPrint("lost??: " + unit.getNameNoDesc())        
                        # Debug code - end

                        objMercenaryUtils.removePlayerMercenary(unit)


        # This method handles the key input and will bring up the mercenary manager screen if the 
        # player has at least one city and presses the 'M' key.
        def onKbdEvent(self, argsList):
                'keypress handler - return 1 if the event was consumed'

                if ((not gc.getTeam(gc.getActivePlayer().getTeam()).isHasTech(con.iNationalism)) and gc.getGame().getGameTurn() >= getTurnForYear(con.tBirth[utils.getHumanID()])): #Rhye
                
                        # TO DO: REMOVE THE FOLLOWING LINE BEFORE RELEASE.
                        #gc.getPlayer(0).setGold(20000)
                        eventType,key,mx,my,px,py = argsList
                                
                        theKey=int(key)

                        if ( eventType == self.EventKeyDown and theKey == int(InputTypes.KB_M) and self.eventManager.bAlt and gc.getActivePlayer().getNumCities() > 0 and gc.getActivePlayer().getCurrentEra() >= g_iStartingEra):

                                self.mercenaryManager.interfaceScreen()

                #Rhye - start debug
                eventType,key,mx,my,px,py = argsList
                        
                theKey=int(key)

                if ( eventType == self.EventKeyDown and theKey == int(InputTypes.KB_B) and self.eventManager.bAlt):


                        iHuman = utils.getHumanID()
                        iGameTurn = gc.getGame().getGameTurn()

                        
##                        print("fava", gc.getGame().getGameTurn())
##                        print(self.rnf.getNewCiv(), self.rnf.getNewCivFlip(), self.rnf.getSpawnDelay(con.iPersia), self.rnf.getFlipsDelay(con.iPersia))

                        #print(self.aiw.getNextTurnAIWar())
                        #self.aiw.setNextTurnAIWar(gc.getGame().getGameTurn())
                        #self.aiw.checkTurn(gc.getGame().getGameTurn())
                        #print(self.aiw.getNextTurnAIWar())
                        #for i in range(iNumPlayers):
                        #        print(i,gc.getPlayer(i).getGold())
                        #        self.aiw.checkGrid(i)
                        
                        
                        #gc.getGame().setGameTurn(400)
                        #gc.getPlayer(iGermany).setLeader(con.iFrederick)
                        
                        #iCiv = iFrance
                        #self.rnf.setColonistsAlreadyGiven(iCiv,self.rnf.getColonistsAlreadyGiven(iCiv)-1)
                        #self.rnf.giveColonists(iCiv, con.tBroaderAreasTL[iCiv], con.tBroaderAreasBR[iCiv])
                        

                        #for a in range(1):
                                #self.sta.test1(gc.getGame().getGameTurn())
                                #self.sta.test2(gc.getGame().getGameTurn())

                        #for a in range(iNumMajorPlayers):
                        #        if (gc.getPlayer(a).isAlive()):
                                        #self.sta.updateBaseStabilityTestOld(gc.getGame().getGameTurn(), a)
                                        #self.sta.updateBaseStabilityTest(gc.getGame().getGameTurn(), a)
                        
                        #gc.getTeam(gc.getPlayer(con.iCarthage).getTeam()).setVassal(con.iMongolia, True, True)
                        #gc.getTeam(gc.getPlayer(iEngland).getTeam()).signDefensivePact(iJapan)
                        #gc.getTeam(gc.getPlayer(iInca).getTeam()).declareWar(iMongolia, True, -1)                        
                        #gc.getGame().setActivePlayer(con.iEngland, False)
                        #unit = gc.getMap().plot(56, 54).getUnit(0)
                        #print(unit.generatePath( gc.getMap().plot(41, 25), 0, False, null))
                        #self.rnf.giveColonists(iAmerica, (10,44), (36,55))
                        #gc.getTeam(gc.getPlayer(iAztecs).getTeam()).makePeace(iMongolia)

                        
                        #utils.killCiv(con.iVikings, con.iRussia)
                        #self.sta.checkTurn(gc.getGame().getGameTurn())
                        #self.rnf.resurrection(gc.getGame().getGameTurn())
                        #self.rnf.secession(gc.getGame().getGameTurn())
                        
                        #gc.getTeam(gc.getPlayer(iTurkey).getTeam()).setNoTradeTech(con.iGunpowder, True)

                        #utils.setStability(iArabia, utils.getStability(iArabia) -50)
                        #utils.setParameter(iArabia, 9, True, -50)
                        #objMercenaryUtils.addMercenariesToPool()

##                        gc.getMap().plot(27, 30).setFeatureType(-1, 0)
##                        gc.getMap().plot(28, 31).setFeatureType(-1, 0)
##                        

                        #print(gc.getMap().plot(68, 45).area().getID())
                        #asiaID = gc.getMap().plot(69, 44).area().getID()
                        #print(asiaID)
                        #gc.getMap().plot(68, 45).setArea(asiaID)
                        #print(gc.getMap().plot(68, 45).area().getID())
                        #gc.getPlayer(iChina).AI_setAttitudeExtra(con.iEthiopia, 20)

                        #self.com.decay(con.iTurkey)                
                        #self.data.setupScriptData()
                        #gc.getGame().setWinner(con.iEgypt, 0)
                        #if (len(lLeaders[iDeadCiv]) > 1):
                        #gc.getTeam(gc.getPlayer(con.iIndia).getTeam()).signOpenBorders(con.iChina)
                        #print ("CC1", gc.getTeam(gc.getPlayer(con.iIndia).getTeam()).canContact(con.iEgypt))
                        #print ("ME1", gc.getTeam(gc.getPlayer(con.iIndia).getTeam()).isHasMet(con.iEgypt))
                        #gc.getTeam(gc.getPlayer(con.iJapan).getTeam()).cutContact(con.iChina)
                        #gc.getTeam(gc.getPlayer(con.iChina).getTeam()).cutContact(con.iJapan)
                        #print ("CC2", gc.getTeam(gc.getPlayer(con.iIndia).getTeam()).canContact(con.iEgypt))
                        #print ("ME2", gc.getTeam(gc.getPlayer(con.iIndia).getTeam()).isHasMet(con.iEgypt))
                        #for i in range (con.iNumPlayers):
                        #        gc.getTeam(gc.getPlayer(con.iInca).getTeam()).cutContact(i)
                        #gc.getTeam(gc.getPlayer(con.iChina).getTeam()).setVassal(con.iJapan, True, True)
                        #gc.getGame().changePlayer(con.iChina, 0, 22, con.iChina, False, True)
                        #gc.getPlayer(con.iBabylonia).setLeader(24)
                        #gc.getPlayer(con.iEgypt).changeGold(3000)
                        #gc.getMap().plot(72, 32).getPlotCity().changeBuildingProduction(con.iBroadway,639)
                        #print ("CC2", gc.getTeam(gc.getPlayer(con.iEgypt).getTeam()).canContact(con.iNative))
                        #newCivDesc = CyTranslator().getText("TXT_KEY_NAM_CHI1", ())
##                        newCivDesc = "TXT_KEY_NAM_CHI1"
##                        newDesc = newCivDesc.encode('latin-1')
##                        gc.getPlayer(con.iChina).setCivDescription(newDesc)
##                        print (gc.getPlayer(con.iChina).getCivilizationDescription(0), gc.getPlayer(con.iChina).getCivilizationDescriptionKey(), gc.getPlayer(con.iChina).getCivilizationAdjective(0), gc.getPlayer(con.iChina).getCivilizationAdjectiveKey())
##                        print (gc.getPlayer(con.iIndia).getCivilizationDescription(0), gc.getPlayer(con.iIndia).getCivilizationDescriptionKey(), gc.getPlayer(con.iIndia).getCivilizationAdjective(0), gc.getPlayer(con.iIndia).getCivilizationAdjectiveKey())
##                        self.rnf.showPopup(7614, CyTranslator().getText("TXT_KEY_NEWCIV_TITLE", ()), CyTranslator().getText("TXT_KEY_NEWCIV_MESSAGE", (gc.getPlayer(con.iChina).getCivilizationDescriptionKey(),)), (CyTranslator().getText("TXT_KEY_POPUP_YES", ()), CyTranslator().getText("TXT_KEY_POPUP_NO", ())))

                        #gc.getTeam(gc.getPlayer(con.iChina).getTeam()).setVassal(con.iArabia, True, True)

                        
                        #invasion attempt
                        #if (iGameTurn == 100):
                        #        utils.makeUnit(con.iAxeman, iGermany, con.tCapitals[iGermany], 3)
                        #        utils.makeUnit(con.iSwordsman, iGermany, con.tCapitals[iGermany], 3)
                        
                        #for iCiv in range(iNumPlayers):
                        #        for pyCity in PyPlayer(iCiv).getCityList():
                        #                print (pyCity.GetCy().getName())

                        #debug - kills every unit
                        #for x in range(40, 123):
                        #        for y in range(0, 67):
                        #                pCurrent = gc.getMap().plot( x, y )
                        #                if (pCurrent.getNumUnits() > 0):
                        #                        for i in range (pCurrent.getNumUnits()):
                        #                                unit = pCurrent.getUnit(0)
                        #                                unit.kill(False, con.iBarbarian)


##                        if (gc.getPlayer(utils.getHumanID()).getNumCities() > 1):
##                                CyInterface().addImmediateMessage(CyTranslator().getText("TXT_KEY_STABILITY_CIVILWAR_HUMAN", ()), "")
##                                utils.killAndFragmentCiv(utils.getHumanID(), iIndependent, iIndependent2, iBarbarian, True)
##                                utils.setStability(utils.getHumanID(), -15)


                        #self.pla.setGenericPlagueDates(0, 96)
                        #self.pla.spreadPlague(con.iJapan)
                        #self.pla.stopPlague(con.iJapan)
                        #self.pla.infectCity(utils.getRandomCity(con.iJapan))
                        #print ("Countdown", self.pla.getPlagueCountdown( con.iJapan ))

                        #utils.setStability(con.iJapan, -50)
                        #self.sta.checkImplosion(405)
                        #self.rnf.collapseMotherland(gc.getGame().getGameTurn())
                        
                        #utils.killAndFragmentCiv(con.iEngland, iIndependent, iIndependent2, -1, False)
                        #self.rnf.resurrection(302)
                        
                        #utils.killAndFragmentCiv(con.iRome, iIndependent, iIndependent2, -1, True)
                        #gc.getGame().setActivePlayer(con.iEgypt, False)
                        #teamEgypt.changeResearchProgress(con.iNationalism, 3299, iEgypt)
                        #teamAztecs.changeResearchProgress(con.iSteel, 3399, iAztecs)
                        
                        #self.sta.normalization(200)
                        #gc.getGame().setActivePlayer(con.iFrance, False)
                        
                        #CyInterface().addImmediateMessage(CyTranslator().getText("TXT_KEY_PLAGUE_SPREAD_CITY", ()), "")
                        #CyInterface().addMessage(utils.getHumanID(), False, con.iDuration, CyTranslator().getText("TXT_KEY_EMBASSY_ESTABLISHED", (gc.getPlayer(con.iRussia).getCivilizationAdjectiveKey(),)) + " " + "Citta di prova", "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)

                        #CyInterface().addMessage(iHuman, False, con.iDuration, CyTranslator().getText("TXT_KEY_STABILITY_PERIOD", ()) + " " + CyTranslator().getText("TXT_KEY_STABILITY_GREAT_DEPRESSION", ()), "", 0, "", ColorTypes(con.iOrange), -1, -1, True, True)
                        #CyInterface().addMessage(utils.getHumanID(), True, 5, CyTranslator().getText("TXT_KEY_CONGRESS_NOTIFY_YES2", ()), "", 0, "", ColorTypes(100), -1, -1, True, True)
##                        for i in range(128):
##                                CyInterface().addMessage(utils.getHumanID(), True, 1, "i", "", 0, "", ColorTypes(i), -1, -1, False, True)
##                                if (i % 10 == 0):
##                                         CyInterface().addMessage(utils.getHumanID(), True, 1, "10", "", 0, "", ColorTypes(0), -1, -1, False, True)
                        #print ("vic", self.vic.getNumSinks())

                        #dummy, plotList = utils.squareSearch( (29,28), (31,31), utils.outerInvasion, [])
                        #print (plotList)
                        #utils.setStability(con.iChina, -25)
                        
                        #city = gc.getMap().plot( 79, 40 ).getPlotCity() 
                        #self.pla.infectCity(city)
                        #self.pla.spreadPlague(con.iPersia)
                        #self.pla.processPlague(con.iPersia)

                        #print(1/3,4/3,-1/3,-4/3,-3/3)
                        #objMercenaryUtils.addMercenariesToPool()
                        #self.com.decay(con.iTurkey)

                        #city = gc.getMap().plot( 90, 40 ).getPlotCity()
                        #print ("9040", city.getCulture(con.iIndia), 4000 + 2000*gc.getPlayer(con.iIndia).getCurrentEra())

                        
                        #CyInterface().DoSoundtrack("AS2D_R_F_C")
                        #if (gc.getPlayer(con.iNetherlands).countOwnedBonuses(con.iSpices) + gc.getPlayer(con.iNetherlands).getBonusImport(con.iSpices) >= 5):
                        #        self.vic.setGoal(iNetherlands, 2, 0)
                        #print(self.vic.getNumSinks())
                        #utils.setLastRecordedStabilityStuff(2, 0)
                        #utils.setLastRecordedStabilityStuff(1, 40)

                        #print("base", gc.getHandicapInfo(1).getResearchPercent())
                        #for a in range(iNumMajorPlayers):
                        #        print(a, gc.getHandicapInfo(1).getResearchPercentByIDdebug(a))

                        #print(self.vic.checkFoundedArea(iEngland, (24, 3), (43, 32), 3))
##                        print(gc.getPlayer(iChina).countOwnedBonuses(con.iRice))
##                        print(gc.getPlayer(iChina).getBonusImport(con.iRice))
##                        print(gc.getPlayer(iChina).getNumAvailableBonuses(con.iRice))
                        #print(self.vic.checkOwnedAreaAdjacentArea(iTurkey, (67, 44), (76, 50), 4, (71,47)))

##                        #print (CyGame().getCurrentLanguage())
##                        popup = PyPopup.PyPopup()
##                        popup.setHeaderString(CyTranslator().getText("TXT_KEY_EXILE_TITLE", ()))          
##                        popup.setBodyString( CyTranslator().getText("TXT_KEY_EXILE_TEXT", (gc.getPlayer(con.iGermany).getCivilizationAdjectiveKey(), gc.getPlayer(con.iSpain).getCivilizationShortDescription(0))))
####                        popup.setHeaderString(CyTranslator().getText("TXT_KEY_ESCAPE_TITLE", ()))          
####                        popup.setBodyString( CyTranslator().getText("TXT_KEY_ESCAPE_TEXT", (gc.getPlayer(con.iGermany).getCivilizationAdjectiveKey(),)))
##                        popup.launch()
##
##                        CyInterface().addMessage(utils.getHumanID(), True, con.iDuration/2, ("XXX" + " " + \
##                                                                                   CyTranslator().getText("TXT_KEY_CONGRESS_NOTIFY_YES", (gc.getPlayer(con.iSpain).getCivilizationAdjectiveKey(),))), \
##                                                                                   "", 0, "", ColorTypes(con.iCyan), -1, -1, True, True)
##                        self.rnf.newCivPopup(con.iSpain)
##
##                        self.rnf.showPopup(7622, CyTranslator().getText("TXT_KEY_REBELLION_TITLE", ()), \
##                               CyTranslator().getText("TXT_KEY_REBELLION_TEXT", (gc.getPlayer(con.iGermany).getCivilizationAdjectiveKey(),)), \
##                               (CyTranslator().getText("TXT_KEY_POPUP_YES", ()), \
##                                CyTranslator().getText("TXT_KEY_POPUP_NO", ())))
##
##                        CyInterface().addMessage(utils.getHumanID(), False, con.iDuration, \
##                                                                                 CyTranslator().getText("TXT_KEY_STABILITY_GREAT_DEPRESSION_INFLUENCE", (gc.getPlayer(con.iSpain).getCivilizationDescription(0),)), \
##                                                                                 "", 0, "", ColorTypes(con.iOrange), -1, -1, True, True)
##
####                        CyInterface().addMessage(utils.getHumanID(), True, con.iDuration, \
####                                                        (CyTranslator().getText("TXT_KEY_INDEPENDENCE_TEXT", (gc.getPlayer(con.iGermany).getCivilizationAdjectiveKey(),))), "", 0, "", ColorTypes(con.iGreen), -1, -1, True, True)
##                                
                        #print ("ERA", gc.getInfoTypeForString("ERA_CLASSICAL"))
##                        for iEuroCiv in range(iNumPlayers):
##                                if (iEuroCiv in con.lCivGroups[0]):
##                                        if (not self.vic.checkNotOwnedArea_Skip(iEuroCiv, (24, 3), (43, 32), (32,14), (43,30))):
##                                                CyInterface().addImmediateMessage(CyTranslator().getText("TXT_KEY_STABILITY_CIVILWAR_HUMAN", ()), "")

##                        for x in range(0, 123):
##                                for y in range(0, 67):
##                                        pCurrent = gc.getMap().plot( x, y )
##                                        if (pCurrent.isWater()):
##                                                pCurrent.setOwner(-1)

                        
                        pass


                if ( eventType == self.EventKeyDown and theKey == int(InputTypes.KB_N) and self.eventManager.bAlt):

                        print("ALT-N")
                        
                        self.printEmbassyDebug()
                        self.printPlotsDebug()
                        self.printStabilityDebug()


                if ( eventType == self.EventKeyDown and theKey == int(InputTypes.KB_C) and self.eventManager.bAlt and self.eventManager.bShift):
                        print("SHIFT-ALT-C") #picks a dead civ so that autoplay can be started with game.AIplay xx
                        iDebugDeadCiv = iCarthage #default iCarthage: often dead in 3000BC
                        gc.getTeam(gc.getPlayer(iDebugDeadCiv).getTeam()).setHasTech(con.iCalendar, True, iDebugDeadCiv, False, False)
                        utils.makeUnit(con.iAxeman, iDebugDeadCiv, (0,0), 1)
                        gc.getGame().setActivePlayer(iDebugDeadCiv, False)
                        gc.getPlayer(iDebugDeadCiv).setPlayable(True)

                if ( eventType == self.EventKeyDown and theKey == int(InputTypes.KB_E) and self.eventManager.bAlt and self.eventManager.bShift):
                        print("SHIFT-ALT-E") #picks a dead civ so that autoplay can be started with game.AIplay xx
                        iDebugDeadCiv = iEthiopia #default iEthiopia: always dead in 600AD
                        gc.getTeam(gc.getPlayer(iDebugDeadCiv).getTeam()).setHasTech(con.iCalendar, True, iDebugDeadCiv, False, False)
                        utils.makeUnit(con.iAxeman, iDebugDeadCiv, (0,0), 1)
                        gc.getGame().setActivePlayer(iDebugDeadCiv, False)
                        gc.getPlayer(iDebugDeadCiv).setPlayable(True)

                if ( eventType == self.EventKeyDown and theKey == int(InputTypes.KB_M) and self.eventManager.bAlt and self.eventManager.bShift):
                        print("SHIFT-ALT-M") 
                        iDebugDeadCiv = iMaya
                        gc.getTeam(gc.getPlayer(iDebugDeadCiv).getTeam()).setHasTech(con.iCalendar, True, iDebugDeadCiv, False, False)
                        utils.makeUnit(con.iCatapult, iDebugDeadCiv, (0,0), 1)
                        startPlot = gc.getMap().plot(22,35)
                        iNumUnitsInAPlot = startPlot.getNumUnits()
                        if (iNumUnitsInAPlot):                                                                  
                                for i in range(iNumUnitsInAPlot):                                                
                                        startPlot.getUnit(0).kill(False, iBarbarian)
                        gc.getGame().setActivePlayer(iDebugDeadCiv, False)
                        gc.getPlayer(iDebugDeadCiv).setPlayable(True)
                        
                if ( eventType == self.EventKeyDown and theKey == int(InputTypes.KB_Q) and self.eventManager.bAlt and self.eventManager.bShift):
                        print("SHIFT-ALT-Q") #enables squatting
                        self.rnf.setCheatMode(True);
                        CyInterface().addMessage(utils.getHumanID(), True, con.iDuration, "EXPLOITER!!! ;)", "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)

                #Stability Cheat
                if self.rnf.getCheatMode() and theKey == int(InputTypes.KB_S) and self.eventManager.bAlt and self.eventManager.bShift:
                        print("SHIFT-ALT-S") #boosts stability by +10 for the human player
                        utils.setStability(utils.getHumanID(), utils.getStability(utils.getHumanID())+10)
			gc.getPlayer(utils.getHumanID()).changeStability(10) # test DLL

                        
                #Rhye - end debug
        
        #Mercenaries - end



        #Rhye - start
        def printDebug(self, iGameTurn):

                
                if (iGameTurn %50 == 1):
                        self.printEmbassyDebug()

                if (iGameTurn %20 == 0):
                        self.printPlotsDebug()

                if (iGameTurn %10 == 0): 
                        self.printStabilityDebug()


                        
        def printPlotsDebug(self):

##                for i in range(124):
##                        for j in range(68):
##                                print (i, j, gc.getMap().plot(i,j).getArea())
            
                #countTotalUnits
                iTotal = 0
                iTotalCities = 0
##                lType = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
##                lOwner = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                
                #lOwnerLongbow = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                #         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                #         0, 0, 0, 0, 0, 0, 0]
                #lOwnerCannon = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                #         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                #         0, 0, 0, 0, 0, 0, 0]
##                lPlotOwner = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                              0, 0]
                #lPlotOwner2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                #              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                #              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                #              0, 0]
##                lCityOwner2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
##                              0, 0]
                #lCityOwner_sb = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                #              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                #              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                #              0, 0]
                for x in range(0, 123):
                        for y in range(0, 67):
                                pCurrent = gc.getMap().plot( x, y )
                                iTotal += pCurrent.getNumUnits()
##                                if (pCurrent.getNumUnits() > 0):
##                                        for i in range (pCurrent.getNumUnits()):
##                                                unit = pCurrent.getUnit(i)
##                                                lType[unit.getUnitType()] += 1
##                                                lOwner[unit.getOwner()] += 1
                                                #if (unit.getUnitType() == con.iLongbowman):
                                                #       lOwnerLongbow[unit.getOwner()] += 1
                                                #if (unit.getUnitType() == con.iCannon):
                                                #       lOwnerCannon[unit.getOwner()] += 1

                                if ( pCurrent.isCity()):
                                        iTotalCities += 1
                                        
                print ("TOTAL UNITS", iTotal)  
                print ("TOTAL CITIES", iTotalCities)

##                print ("Unit types")
##                for i in range (len(lType)):
##                        print (i, lType[i])
##                print ("Unit owners")
##                for i in range (len(lOwner)):
##                        print (i, lOwner[i])
                #print ("LB owners")
                #for j in range (len(lOwnerLongbow)):
                #        print (j, lOwnerLongbow[j])               
                #print ("Cannon owners")
                #for j in range (len(lOwnerCannon)):
                #        print (j, lOwnerCannon[j])               
        
                pass

        def printEmbassyDebug(self):
                for i in range(con.iNumPlayers):
                        if (gc.getPlayer(i).isAlive()):
                                apCityList = PyPlayer(i).getCityList()
                                print (gc.getPlayer(i).getCivilizationShortDescription(0), gc.getTeam(gc.getPlayer(i).getTeam()).isHasTech(con.iCivilService), gc.getTeam(gc.getPlayer(i).getTeam()).isHasTech(con.iPaper))                                                                                     
                                for j in range(con.iNumPlayers):
                                        if (gc.getTeam(gc.getPlayer(i).getTeam()).canContact(j)):   
                                                bEmb = False
                                                for pCity in apCityList:
                                                        city = pCity.GetCy()
                                                        if (city.hasBuilding(con.iNumBuildingsPlague+j)):
                                                                print (city.getName(), "HAS EMBASSY", gc.getPlayer(j).getCivilizationAdjective(0))
                                                                bEmb = True
                                                                break
                                                if (bEmb == False):
                                                        print ("NO EMBASSY", gc.getPlayer(j).getCivilizationAdjective(0))


        def printStabilityDebug(self):
                print ("Stability")
                for iCiv in range(con.iNumPlayers):
                        if (gc.getPlayer(iCiv).isAlive()):
                                print ("Base:", utils.getBaseStabilityLastTurn(iCiv), "Modifier:", utils.getStability(iCiv)-utils.getBaseStabilityLastTurn(iCiv), "Total:", utils.getStability(iCiv), "civic", gc.getPlayer(iCiv).getCivics(5), gc.getPlayer(iCiv).getCivilizationDescription(0))
                        else:
                                print ("dead", iCiv)
                for i in range(con.iNumStabilityParameters):
                        print("Parameter", i, utils.getStabilityParameters(i))
                #for i in range(con.iNumPlayers):
                        #print (gc.getPlayer(i).getCivilizationShortDescription(0), "PLOT OWNERSHIP ABROAD:", self.sta.getOwnedPlotsLastTurn(i), "CITY OWNERSHIP LOST:", self.sta.getOwnedCitiesLastTurn(i) )