#
# Mercenaries Mod
# By: The Lopez
# MercenaryUtils
# 

from CvPythonExtensions import *
import MercenaryNameUtils

import CvUtil

import CvEventManager
import sys
import PyHelpers
import CvMainInterface
#import CvConfigParser #Rhye
import math

import cPickle as pickle

import Consts as con #Rhye
import RFCUtils #Rhye

from StoredData import sd

################# SD-UTILITY-PACK ###################
import SdToolKit
sdEcho         = SdToolKit.sdEcho
sdModInit      = SdToolKit.sdModInit
sdModLoad      = SdToolKit.sdModLoad
sdModSave      = SdToolKit.sdModSave
sdEntityInit   = SdToolKit.sdEntityInit
sdEntityExists = SdToolKit.sdEntityExists
sdGetVal       = SdToolKit.sdGetVal
sdSetVal       = SdToolKit.sdSetVal


# globals
###################################################
gc = CyGlobalContext()	

utils = RFCUtils.RFCUtils() #Rhye

PyPlayer = PyHelpers.PyPlayer
PyGame = PyHelpers.PyGame()
PyInfo = PyHelpers.PyInfo

AVAILABLE_MERCENARIES = "AvailableMercenaries"
HIRED_MERCENARIES = "HiredMercenaries"
MERCENARY_GROUPS = "MercenaryGroups"
MERCENARY_NAMES = "MercenaryNames"
UNPLACED_MERCENARIES = "UnplacedMercenaries"



#Rhye - start
lForbiddenUnits = ("UNIT_LION",
          "UNIT_BEAR",
          "UNIT_PANTHER",
          "UNIT_WOLF",
          "UNIT_SCOUT",
          "UNIT_SPY",
          "UNIT_INCAN_QUECHUA",
          "UNIT_AZTEC_JAGUAR",
          "UNIT_CELTIC_GALLIC_WARRIOR",     
          "UNIT_ROME_PRAETORIAN",
          "UNIT_JAPAN_SAMURAI",
          #"UNIT_VIKING_BESERKER",
          "UNIT_MAYA_HOLKAN",
          "UNIT_GREEK_PHALANX",
          "UNIT_FRENCH_MUSKETEER",
          "UNIT_OTTOMAN_JANISSARY",
          "UNIT_ETHIOPIAN_OROMO_WARRIOR",
          "UNIT_ENGLISH_REDCOAT",
          "UNIT_BABYLON_BOWMAN",
          "UNIT_CHINA_CHOKONU",
          "UNIT_PERSIA_IMMORTAL",
	  "UNIT_THAILAND_CHANG_SUEK",
          "UNIT_HORSE_ARCHER",
          "UNIT_MONGOL_KESHIK",
          "UNIT_SPANISH_CONQUISTADOR",
          "UNIT_RUSSIA_COSSACK",
          "UNIT_KHMER_BALLISTA_ELEPHANT",
          "UNIT_TANK",
          "UNIT_GERMAN_PANZER",
          "UNIT_MODERN_ARMOR",
          "UNIT_CATAPULT",
          "UNIT_KOREAN_HWACHA",
          "UNIT_TREBUCHET", 
          "UNIT_CANNON",
          "UNIT_MACHINE_GUN",
          "UNIT_ARTILLERY",)
#Rhye - end
          
          
          
          



							
# Change this if you want to increase the min number of mercenaries that will be added 
# to the global mercenary pool each turn.
# Default value is 1
g_iMinMercenaryCreationCount = 3 #Rhye

# Change this if you want to increase the max number of mercenaries that will be added 
# to the global mercenary pool each turn.
# Default value is 5
g_iMaxMercenaryCreationCount = 6 #Rhye

# Set this to true if the max player era should be used to create mercenaries, false if 
# the player's era should be used to create the mercenaries. The player's era will only 
# be used if bGameTurnMercenaryCreation is also set to false. This setting will be 
# ignored if g_bEraAppropriateMercenaries is set to false.
# Default value is true
g_bMaxPlayerGameEra = true

# Set this to true if era appropriate mercenaries should be created, false if mercenaries
# from any era should be created. WARNING: If set to false there could be time traveling 
# mercenaries from future eras appearing in the Ancient Era. You have been warned!!! 
# Default value is true
g_bEraAppropriateMercenaries = true

# Change this to the era that mercenaries should be available in the game. The era used
# to determine the starting point depends on the value of g_bMaxPlayerGameEra. If 
# g_bMaxPlayerGameEra is set to true then the era used to determine the starting point 
# will be the max era from the active players in the game. If g_bMaxPlayerGameEra is set 
# to false then the starting point will be the current era of the player during the 
# onBeginPlayerTurn method call.
# Default value is "ERA_ANCIENT"
#Rhye - start (was causing an assert)
#g_iStartingEra = gc.getInfoTypeForString("ERA_ANCIENT")
g_iStartingEra = 0
#Rhye - end

# Change this to increase or decrease the chance that a mercenary will get a promotion.
# The default value of 10 means that the mercenary has a 10% chance of getting one of
# their promotions.
# Default value is 10
g_iMercenaryPromotionChance = 6 #Rhye

# Change this to true to give mercenaries the prereq promotions when it is set to true 
# and the mercenary is given a promotion with unmet prereqs. Mercenaries that can have 
# combat 1 - 5 and were given combat 5 would automaticallly be given combat 1-4 if the 
# value is set to true. WARNING: Setting this value to true will cause hire and 
# maintenance costs to go up for mercenaries.
# Default value is true
g_bBackfillPrereqPromotions = true

# Change this to either increase or decrease mercenary hiring costs. For example if 
# mercenaries should cost 50% less then the value should be set to 0.5. If mercenaries
# should cost 50% more then the value should be set to 1.5.
# Default value is 0.8
g_dHireCostModifier = 0.20 #Rhye

g_dBaseHireCost = 15 #Rhye

# Change this to either increase or decrease mercenary maintenace costs. For example if 
# mercenary maintenace should cost 50% less then the value should be set to 0.5. If 
# mercenary maintenace should cost 50% more then the value should be set to 1.5.
# Default value is 1.0
g_dMaintenanceCostModifier = 0.15 #Rhye

g_dBaseMaintenanceCost = 2 #Rhye

# Change this to change the location where mercenaries should be placed when hired by
# players. Currently there are 3 static possible options plus one dynamic option. The
# three static options are:
#                           - Capital City
#                           - Civilization Edge
#                           - Random
# The "Civilization Edge" option will place hired mercenaries in the farthest city 
# from the players capital city. The last possible value for the mercenary starting
# location is a comma separated list of building types. When set mercenaries will only
# start in a city with one or more of the specified buildings. The more buildings in 
# the city, the bigger the chance that the mercenary will be placed there when they
# are hired by the player. An example of such a list is:
# "BUILDING_PALACE,BUILDING_CASTLE,BUILDING_BARRACKS". When the mercenary starting
# location is set to this value then the starting location for hired mercenaries will
# be a random city containing one of the buildings specified. If a city cannot is not
# found with any of those buildings then the mercenary will be placed in a random
# city.
# Default value is "Civilization Edge"
g_strMercenaryStartingLocation = "Capital City" #Rhye

# Change this to increase or decrease the minimum number of promotions each mercenary 
# should have when initially added to the global mercenary pool by the game.
# Default value is 1
g_iMinimumStartingMercenaryPromotionCount = 1

# The max size of the global mercenary pool. No more mercenaries will be added by the
# game to the pool if the max number is reached. This feature does not disable the
# fire mercenary feature. This variable is used to control the load time for the 
# "Mercenary Manager" screen. 
# Default valus is 100
g_iMaxGlobalMercenaryPoolSize = 12 #Rhye

# Change this number to increase or decrease the ratio between the number of 
# mercenaries and units in the game. For instance setting the value to 10 means that
# there will be 10 mercenaries available in the game for every 100 units (a 1:10
# ratio). Setting the value to 4 means that there will be 4 mercenaries available in
# the game for every 100 units (a 1:25 ratio). 
# Default value is 10
g_iRatioMercenariesToRegulars = 10

# Change this to true if mercenary moves should be consumed when they are hired and
# added to the game.
# Default value is true
g_bConsumeMercenaryMovesOnHire = true

# Change this to true to delay the placement of hired mercenaries in player's cities
# by the amount indicated in "Mercenary Placement Delay Amount". The value set to 
# "Consume Mercenary Moves On Hire" will be treated as if set to false if "Delay 
# Mercenary Placement" is set to true.
# Default value is true
g_bDelayMercenaryPlacement = true

# Change this to increase or decrease the time that will be used to delay the placement
# of hired mercenaries.
# Default value is 3
g_iMercenaryPlacementDelayAmount = 0 #Rhye

# Change this to true if unit moves should be consumed when they return from being 
# contracted out as mercenaries
# Default value is true
g_bConsumeUnitMovesOnReturn = true

# Change this to true to delay the return of contracted out units to player's cities
# by the amount indicated in "Unit Return Delay Amount". The value set to "Consume Unit 
# Moves On Return" will be treated as if set to false if "Delay Mercenary Placement" is 
# set to true.
# Default value is true
g_bDelayUnitReturn = true

# Change this to increase or decrease the time that will be used to delay the return
# of units contracted out as mercenaries.
# Default value is 3
g_iUnitReturnDelayAmount = 3 #Rhye

# Change this to false to supress the mercenary messages.
# Default value is true
g_bDisplayMercenaryMessages = true

# The list containing the building info types if the g_strMercenaryStartingLocation
# is set to a comma delimited string of building types
g_buildingInfoTypeList = []

# This is the dictionary used to filter out the mercenaries that will be added to the global
# mercenary pool.
g_unitFilterDictionary = {}

# Set to true to print out debug messages in the logs
g_bDebug = false


# Default value is 100
g_iAIHireCostPercent = 100 - (gc.getGame().getHandicapType())*25 #Rhye

# Default value is 100
g_iAIMaintenanceCostPercent = 100 - (gc.getGame().getHandicapType())*25 #Rhye


class MercenaryUtils:

	# The constructor for the MercenaryUtils class. First we check to see if the 
	# data has been setup using pickle. Then we try to read in the configuration 
	# information from the INI config file.
	def __init__(self):
		self.firsttime = true
		
		# Setup the mercenary data structure if it hasn't been setup yet.
		if(sdEntityExists("Mercenaries Mod","MercenaryData") == False):
			self.setupMercenaryData()

		global g_iMinMercenaryCreationCount
		global g_iMaxMercenaryCreationCount
		global g_bMaxPlayerGameEra
		global g_bEraAppropriateMercenaries
		global g_iStartingEra
		global g_iMercenaryPromotionChance
		global g_bBackfillPrereqPromotions
		global g_dHireCostModifier
		global g_dMaintenanceCostModifier
		global g_strMercenaryStartingLocation
		global g_iMinimumStartingMercenaryPromotionCount
		global g_iMaxGlobalMercenaryPoolSize
		global g_iRatioMercenariesToRegulars
		global g_bConsumeMercenaryMovesOnHire
		global g_bDelayMercenaryPlacement
		global g_iMercenaryPlacementDelayAmount
		global g_bConsumeUnitMovesOnReturn
		global g_bDelayUnitReturn
		global g_iUnitReturnDelayAmount
		global g_buildingInfoTypeList
		global g_UnitFilterDictionary
		global g_bDisplayMercenaryMessages

		#Rhye - start comment
##		# Load the Mercenaries Mod Config INI file containing all of the configuration information
##		config = CvConfigParser.CvConfigParser("Mercenaries Mod Config.ini")
##		
##		# If we actually were able to open the "Mercenaries Mod Config.ini" file then read in the values.
##		# otherwise we'll keep the default values that were set at the top of this file.
##		if(config != None):
##			g_iMinMercenaryCreationCount = config.getint("Mercenaries Mod","Min Mercenary Creation Count", 1)
##			g_iMaxMercenaryCreationCount = config.getint("Mercenaries Mod","Max Mercenary Creation Count", 5)
##			g_bMaxPlayerGameEra = config.getboolean("Mercenaries Mod", "Max Player Game Era", true)
##			g_bEraAppropriateMercenaries = config.getboolean("Mercenaries Mod", "Era Appropriate Mercenaries", true)
##			g_iStartingEra = gc.getInfoTypeForString(config.get("Mercenaries Mod","Starting Era","ERA_ANCIENT"))
##			g_iMercenaryPromotionChance = config.getint("Mercenaries Mod","Mercenary Promotion Chance", 10)
##			g_bBackfillPrereqPromotions = config.getboolean("Mercenaries Mod", "Backfill Prereq Promotions", true)
##			g_dHireCostModifier = config.getfloat("Mercenaries Mod","Hire Cost Modifier", 0.8)
##			g_dMaintenanceCostModifier = config.getfloat("Mercenaries Mod","Maintenance Cost Modifier", 1.0)
##			g_strMercenaryStartingLocation = config.get("Mercenaries Mod","Mercenary Starting Location","Civilization Edge")	
##			g_iMinimumStartingMercenaryPromotionCount = config.getint("Mercenaries Mod","Minimum Starting Mercenary Promotion Count", 1)
##			g_iMaxGlobalMercenaryPoolSize = config.getint("Mercenaries Mod","Max Global Mercenary Pool Size", 100)
##			g_iRatioMercenariesToRegulars = config.getint("Mercenaries Mod","Ratio Mercenaries To Regulars", 10)
##			g_bConsumeMercenaryMovesOnHire = config.getboolean("Mercenaries Mod", "Consume Mercenary Moves On Hire", true)
##			g_bDelayMercenaryPlacement = config.getboolean("Mercenaries Mod", "Delay Mercenary Placement", true)
##			g_iMercenaryPlacementDelayAmount = config.getint("Mercenaries Mod","Mercenary Placement Delay Amount", 3)
##			g_bConsumeUnitMovesOnReturn = config.getboolean("Mercenaries Mod", "Consume Unit Moves On Return", true)
##			g_bDelayUnitReturn = config.getboolean("Mercenaries Mod", "Delay Unit Return", true)
##			g_iUnitReturnDelayAmount = config.getint("Mercenaries Mod","Unit Return Delay Amount", 3)
##			g_bDisplayMercenaryMessages = config.getboolean("Mercenaries Mod", "Display Mercenary Messages", true)
##			
##			# Setup the mercenary starting location. If the starting location isn't "Capital City", "Civilization Edge" or 
##			# "Random" and it's length is greater than 0 then assume that it is a list of buildings and parse it.
##			if(g_strMercenaryStartingLocation != "Capital City" and g_strMercenaryStartingLocation != "Civilization Edge" and g_strMercenaryStartingLocation != "Random" and len(g_strMercenaryStartingLocation) > 0):
##
##				# Split the starting location using ',' as the delimiting character.
##				g_buildingInfoTypeList = g_strMercenaryStartingLocation.split(",")
##
##				# Go through the resulting list and get the info type value for each one.
##				for i in range(len(g_buildingInfoTypeList)):
##					g_buildingInfoTypeList[i] = gc.getInfoTypeForString(g_buildingInfoTypeList[i])
##
##			# Go through each of the units defined for the game and	check to see if they need to be excluded from
##			# the possible mercenaries that can be added to the game.
##			for i in range(gc.getNumUnitInfos()):
##				unitType = gc.getUnitInfo(i).getType()
##				tmpBool = config.getboolean("Mercenaries Mod",unitType,false)
##				
##				# Add the excluded unit to the filter dictionary so it won't appear in the game.
##				if(tmpBool):
##					g_unitFilterDictionary[unitType] = unitType		
##
##			# Debug code - start
##			if(g_bDebug):
##				CvUtil.pyPrint(str(len(g_unitFilterDictionary)) + " units will not be allowed in the game as mercenaries")
##				if(len(g_unitFilterDictionary) > 0): 
##					CvUtil.pyPrint("They are: ")
##					for unitType in g_unitFilterDictionary:
##						CvUtil.pyPrint("    "+unitType)
##			# Debug code - end
		#Rhye - end comment
			
	# Randomly returns a barbarian unit for any era defined in the game.
	def getRandomMercenary(self):
		'Mercenary - the mercenary'
		
		# Setup the mercenary data structure if it hasn't been setup yet.		
		if(sdEntityExists("Mercenaries Mod","MercenaryData") == False):
			self.setupMercenaryData()
					
		# Get the current active player, this use to get the barbarian player but
		# it had to be changed since barbarians will not always exist in games.
		# Yes, I know I should change the variable name, but alas I am lazy ...
		# well maybe not so lazy since I at least took the time to document this
		# and I could have used the time instead to change the variable name but
		# I did not ... so live with it.
		# barbarianPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
		barbarianPlayer = gc.getPlayer(gc.getGame().getActivePlayer())
		
		promotionList = []
		
		# Loop until we get a unit with at least some promotions
		while(len(promotionList) < g_iMinimumStartingMercenaryPromotionCount):
			promotionList = []

			# The random type of unit that will be created
			iUnitType = gc.getGame().getMapRand().get(gc.getNumUnitInfos(), "Random Unit Info")

			# Get the PyUnitInfo for the iUnitType
			pUnitInfo = PyInfo.UnitInfo(iUnitType)
			
			# If we can't contract out the unit then continue			
			if(not self.canContractOutUnit(pUnitInfo.info)):
				continue
			
			plot = barbarianPlayer.getStartingPlot()
						
			# Create the mercenary unit
			tmpUnit = barbarianPlayer.initUnit(iUnitType, plot.getX(), plot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			
			# The following two statements can be written as:
			# promotionList = self.getMercenaryPromotions(self.getUnitPromotionList(tmpUnit))
			# to improve performance. I have provided the code in two lines to improve readability 
			# of the code.
			# Get all of the possible promotions for the mercenary
			promotionList = self.getUnitPromotionList(tmpUnit)
			
			# Get a random subset of promotions that the mercenary will have.
			promotionList = self.getMercenaryPromotions(promotionList)
					
			# Set the initial level and experience level for the mercenary
			self.setInitialMercenaryExperience(tmpUnit, promotionList)
						
			# Create the actual mercenary object, we do not pass in the tmpUnit object itself 
			# because we do not want to accidentally set it as the CyUnit in the Mercenary class
                        #Rhye - start
			#mercenary = Mercenary(MercenaryNameUtils.getRandomMercenaryName(), gc.getUnitInfo(iUnitType), promotionList, tmpUnit.getExperience(), tmpUnit.experienceNeeded())
                        mercenary = Mercenary(MercenaryNameUtils.getRandomMercenaryName(gc.getGame().getActivePlayer(), iUnitType, False), gc.getUnitInfo(iUnitType), promotionList, tmpUnit.getExperience(), tmpUnit.experienceNeeded())
                        #Rhye - end

			# Kill off the tmpUnit since it does not need to exist in the game until someone hires the 
			# mercenary
			tmpUnit.kill(false,PlayerTypes.NO_PLAYER)
		
		# Saves the mercenary in the global mercenary pool
		self.saveMercenary(mercenary)
	
		# Finally return the mercenary
		return mercenary
			

	# Returns a random mercenary for the era specified by iEra 
	def getEraAppropriateRandomMercenary(self, iEra):
		' Mercenary - the mercenary'
		
		# Setup the mercenary data structure if it hasn't been setup yet.		
		if(sdEntityExists("Mercenaries Mod","MercenaryData") == False):
			self.setupMercenaryData()
				
		# return immediately if the iEra doesn't contain a valid value for an era
		if(gc.getEraInfo(iEra) == None):
			return

		# Initialize the prereqTechEra so it doesn't equal the iEra
		prereqTechEra = iEra * -1

		# If iEra is set to 0 then the game just began and set the prereqTechEra 
		# to -1
		if(prereqTechEra == iEra):
			prereqTechEra = -1

		# Get the current active player, this use to get the barbarian player but
		# it had to be changed since barbarians will not always exist in games.
		# Yes, I know I should change the variable name, but alas I am lazy ...
		# well maybe not so lazy since I at least took the time to document this
		# and I could have used the time instead to change the variable name but
		# I did not ... so live with it.
		barbarianPlayer = gc.getPlayer(gc.getGame().getActivePlayer())

		iUnitType = -1

		mercenary = None

		promotionList = []
		
		# Loop until we get a unit with at least some promotions
		while(len(promotionList) < g_iMinimumStartingMercenaryPromotionCount):

                        bLoop = True #Rhye
                        iLoopCounter = 0 #Rhye
			# Loop until we get a unit that matches the required era
			#while(prereqTechEra != iEra): #Rhye
                        while(bLoop): #Rhye
				promotionList = []

				#Rhye - start loopfix (infinite loop happens if renaissance+ techs that offer no units are enabled by WB while in the ancient age)
				iLoopCounter += 1
				if (iLoopCounter > 10000):
                                        return None
                                #Rhye - end
				
				# The random type of unit that will be created
				iUnitType = gc.getGame().getMapRand().get(gc.getNumUnitInfos(), "Random Unit Info")

				# Get the PyUnitInfo for the iUnitType
				pUnitInfo = PyInfo.UnitInfo(iUnitType)

				# If we can't contract out the unit then continue			
				if(not self.canContractOutUnit(pUnitInfo.info)):
					continue
				
				# Get the list of prereq technologies required for the unit
				unitTechPrereqList = self.getUnitPrereqTechs(pUnitInfo)

				#Rhye - start (at least half of the alive civs must have the techs for that unit - no more anachronitic units)
				bContinue = False
				#print ("unit type:", iUnitType)
				#print ("gc.getGame().countCivPlayersAlive()", gc.getGame().countCivPlayersAlive())
				for i in range(len(unitTechPrereqList)):
					#print ("prerequisite", i, unitTechPrereqList[i])
					iCounter = 0
					for iCiv in range(con.iNumPlayers):
						pCiv = gc.getPlayer(iCiv)
						if (pCiv.isAlive()):
							if (gc.getTeam(pCiv.getTeam()).isHasTech(unitTechPrereqList[i])):
								iCounter += 1
					#print ("iCounter", iCounter)
					if ((iCounter+1)*2 < gc.getGame().countCivPlayersAlive()):
						#print ("break & continue")
						bContinue = True
						break
				if (self.getMaxTechEra(unitTechPrereqList) < iEra-2): #accept current and previous 2 eras only, no more warriors in later ages
                                        #print ("insufficient era", self.getMaxTechEra(unitTechPrereqList), iEra-2)
                                        bContinue = True
					    
				if (bContinue):
					continue
				else:
                                        bLoop = False
					#print ("passed")
				
				# If the unitTechPrereqList is empty start from the beginning
##				if(len(unitTechPrereqList) == 0):
##					continue
				
				# Get the era from the list of prereq. technologies
				#prereqTechEra = self.getMaxTechEra(unitTechPrereqList)

                                        
				#Rhye - end

				
			# Create the mercenary unit if we have a valid iUnitType value
			if(iUnitType != -1):

                                #Rhye - start bugfix
				# Create the mercenary unit
				tmpUnit = barbarianPlayer.initUnit(iUnitType, 20, 0, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

##				plot = barbarianPlayer.getStartingPlot()
##							
##				# Create the mercenary unit
##				tmpUnit = barbarianPlayer.initUnit(iUnitType, plot.getX(), plot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
##			        #Rhye - end
				
				# The following two statements can be written as:
				# promotionList = self.getMercenaryPromotions(self.getUnitPromotionList(tmpUnit, iEra))
				# to improve performance. I have provided the code in two lines to improve readability 
				# of the code.
				# Get all of the possible promotions for the mercenary for the give era
				promotionList = self.getEraAppropriateUnitPromotionList(tmpUnit, iEra)
				
				# Get a random subset of promotions that the mercenary will have.
				promotionList = self.getMercenaryPromotions(promotionList)

				# Set the initial level and experience level for the mercenary
				self.setInitialMercenaryExperience(tmpUnit, promotionList)
								
				# Create the actual mercenary object, we do not pass in the tmpUnit object itself 
				# because we do not want to accidentally set it as the CyUnit in the Mercenary class
				#Rhye - start
				#mercenary = Mercenary(MercenaryNameUtils.getRandomMercenaryName(), gc.getUnitInfo(iUnitType), promotionList, tmpUnit.getExperience(), tmpUnit.experienceNeeded())
                                mercenary = Mercenary(MercenaryNameUtils.getRandomMercenaryName(gc.getGame().getActivePlayer() ,iUnitType, False), gc.getUnitInfo(iUnitType), promotionList, tmpUnit.getExperience(), tmpUnit.experienceNeeded())
                                #Rhye - end
				# Kill off the tmpUnit since it does not need to exist in the game until someone hires the 
				# mercenary
				tmpUnit.kill(false,PlayerTypes.NO_PLAYER)

				#Rhye - start
                                gc.getMap().plot(20, 0).setRevealed(gc.getGame().getActivePlayer(), False, True, -1);
                                gc.getMap().plot(20, 1).setRevealed(gc.getGame().getActivePlayer(), False, True, -1);
                                gc.getMap().plot(21, 1).setRevealed(gc.getGame().getActivePlayer(), False, True, -1);
                                gc.getMap().plot(21, 0).setRevealed(gc.getGame().getActivePlayer(), False, True, -1);
                                gc.getMap().plot(19, 0).setRevealed(gc.getGame().getActivePlayer(), False, True, -1);
                                gc.getMap().plot(19, 1).setRevealed(gc.getGame().getActivePlayer(), False, True, -1);
                                gc.getMap().plot(22, 0).setRevealed(gc.getGame().getActivePlayer(), False, True, -1);
                                gc.getMap().plot(22, 1).setRevealed(gc.getGame().getActivePlayer(), False, True, -1);
                                gc.getMap().plot(22, 2).setRevealed(gc.getGame().getActivePlayer(), False, True, -1);
                                gc.getMap().plot(21, 2).setRevealed(gc.getGame().getActivePlayer(), False, True, -1);
                                gc.getMap().plot(20, 2).setRevealed(gc.getGame().getActivePlayer(), False, True, -1);
                                gc.getMap().plot(18, 0).setRevealed(gc.getGame().getActivePlayer(), False, True, -1);
                                gc.getMap().plot(18, 1).setRevealed(gc.getGame().getActivePlayer(), False, True, -1);
                                gc.getMap().plot(18, 2).setRevealed(gc.getGame().getActivePlayer(), False, True, -1);
                                gc.getMap().plot(18, 2).setRevealed(gc.getGame().getActivePlayer(), False, True, -1);
                                #Rhye - end


				

		# Debug code - start		
		if(g_bDebug):
			self.printMercenaryDataToLog(mercenary)
		# Debug code - end
		
		# Saves the mercenary in the global mercenary pool
		self.saveMercenary(mercenary)
		
		# Finally return the mercenary
		return mercenary

		
	# This method will set the initial the mercenary experience and levels by using the 
	# number of promotions retrieved from calling getMercenaryPromotions(...) method
	def setInitialMercenaryExperience(self, objMercenary, promotionList):
	
		# Return immediately if the objMercenary is not set
		if(objMercenary == None):
			return
			
		# Return immediately if the promotionList os not set
		if(promotionList == None):
			return
												
		# Get the number of promotions in the promotion list
		iPromotionCount = len(promotionList)
		
		# Set the level of the mercenary to promotion count - 1
		objMercenary.setLevel(iPromotionCount-1)
		
		# Get the experience level of the mercenary
		iMercenaryExperience = objMercenary.experienceNeeded()

		# Reset the mercenary level to their real level
		objMercenary.setLevel(iPromotionCount)
	
		iRandomBonusExperience = 0
	
		# Get a random experience amount 	
		if(iMercenaryExperience < objMercenary.experienceNeeded()):
			iRandomBonusExperience = gc.getGame().getMapRand().get(objMercenary.experienceNeeded()-iMercenaryExperience, "Random Bonus XP")

		# Set the experience level for the mercenary
		objMercenary.setExperience(iMercenaryExperience+iRandomBonusExperience,objMercenary.experienceNeeded())
		
		
	# This method will return the max era from the techList
	def getMaxTechEra(self, techList):
		' iEra - the youngest era in the techList'
		
		# Return ERA_ANCIENT immediately if the techList is not set
		if(techList == None):
                        #Rhye - start
			#return EraTypes.ERA_ANCIENT
                        return 0
                        #Rhye - end
			
		# Return ERA_ANCIENT immediately if the techList is empty
		if(len(techList) == 0):
			return 0
			
		# If the techList contains only one TechInfo then return its era information
		if(len(techList) == 1):
			return gc.getTechInfo(techList[0]).getEra()
									
		eraList = []
		
		# Go through each TechInfo in the techList and get its era information and
		# append it to the end of the eraList
		for i in range(len(techList)):
			eraList.append(gc.getTechInfo(techList[i]).getEra())
		
		# Sort the eraList and reverse its order. This is done to get the max era value
		# as the first item of the list.
		eraList.sort()
		eraList.reverse()
		
		return eraList[0]
	
	
	# This was developed to fetch the prereq techs for a unit in one call instead of having
	# to call the PyHelpers.py file UnitInfo getTechPrereqID and getPrereqOrTechIDList methods
	# which is quite silly since if there are two prereq techs for a UnitInfo you have to
	# call getTechPrereqID to get the first one and getPrereqOrTechIDList to get the second
	# one instead of just being able to call getPrereqOrTechIDList.
	def getUnitPrereqTechs(self, objUnitInfo):
		' list - the list of prereq techs'

		unitTechPrereqList = []

		# Return immediately if an invalid objUnitInfo was passed in
		if(objUnitInfo == None):
			return []

		# Return immediately if the unit doesn't have a tech prereq 
		if(objUnitInfo.getTechPrereqID() == -1):
			return unitTechPrereqList

		# Append the objUnitInfos first tech prereq
		unitTechPrereqList.append(objUnitInfo.getTechPrereqID())

		i = 0
		
		# Get the rest of objUnitInfos tech prereqs
		result = objUnitInfo.info.getPrereqAndTechs(i)
	
		# Return if there aren't any more prereq techs.
		if(result == -1):
			return unitTechPrereqList
	
		# Go through the tech prereqs and append them to the unitTechPrereqList
		while(result > -1):
			unitTechPrereqList.append(result)
			i = i + 1
			# get the next prereq tech
			result = objUnitInfo.info.getPrereqAndTechs(i)

		return unitTechPrereqList


	# Returns the list of possible promotions that the objUnit can have
	def getUnitPromotionList(self, objUnit):
		' objList - the list of possible promotions the mercenary can have'

		# Return immediately if objUnit was not set
		if(objUnit == None):
			return

		objUnitInfo = gc.getUnitInfo(objUnit.getUnitType())
							
		promotionList = []
		
		# Go through the list of the promotions defined in the game and check to see if the
		# CyUnit passed in as objUnit can have them
		for i in range(gc.getNumPromotionInfos()):

			# Get the promotion information
			promotionInfo = gc.getPromotionInfo(i)

			# Get the PromotionType integer value
			iPromotionInfoType = gc.getInfoTypeForString(gc.getPromotionInfo(i).getType())

			# If the CyUnit can have the promotion then append it to the end of promotionList
			if (isPromotionValid(iPromotionInfoType, objUnit.getUnitType(), False)):
				promotionList.append(promotionInfo)
		
		# Debug code - start		
		if(g_bDebug):
			promotions = objUnit.getName() + " : "
			for i in range(len(promotionList)):
				promotions = promotions + promotionList[i].getType() + ", "		

			# Debug print statement
			CvUtil.pyPrint(promotions)
		# Debug code - end
		
		return promotionList
		
		
	# Returns the list of possible promotions that the objUnit can have up to the given
	# era through iEra
	def getEraAppropriateUnitPromotionList(self, objUnit, iEra):
		' objList - the list of possible promotions the mercenary can have'

		# Return immediately if objUnit was not set
		if(objUnit == None):
			return
		
		# return immediately if the iEra doesn't contain a valid value for an era
		if(gc.getEraInfo(iEra) == None):
			return

		promotionList = []
		
		objUnitInfo = gc.getUnitInfo(objUnit.getUnitType())

		for i in range(gc.getNumPromotionInfos()):
			# Get the promotion information
			promotionInfo = gc.getPromotionInfo(i)

			# Get the PromotionType integer value
			iPromotionInfoType = gc.getInfoTypeForString(gc.getPromotionInfo(i).getType())

			# Get the prereq tech for the promotion
			iTechInfo = promotionInfo.getTechPrereq()
			bEraMatch = false
			
			# Set bEraMatch to true if there is a tech prereq. for the promotion and the
			# tech prereq. era matches the era passed through iEra or if there is no
			# tech prereq.
			if(iTechInfo >= 0 and gc.getTechInfo(iTechInfo).getEra() <= iEra):
				bEraMatch = true
			else:
				bEraMatch = true

                        #Rhye - start (less super-units)
			#vanilla array
			#lPromotionOdds = [100, 80, 60, 40, 20, 80, 80, 80, 60, 60, 60, 60, 20, 40, 20, 80, 60, 100, 80, 100, 80, 100, 80, 60, 100, 80, 60, 100, 80, 60, 40, 100, 80, 60, 60, 100, 80, 20, 60, 80, 60, 100, 100, 100, 100]
                        #                                                                                       #guerilla                                                                     #flanking                #self pres.    #mercenary
                        #warlords array
			#lPromotionOdds = [100, 80, 60, 40, 20, 80, 80, 80, 60, 60, 60, 60, 20, 40, 20, 80, 60, 100, 80, 60, 100, 80, 100, 80, 60, 100, 80, 60, 100, 80, 60, 40, 100, 80, 60, 60, 100, 80, 20, 60, 80, 60, 0, 0, 0, 0, 0, 0, 100, 100, 100, 100]
                        #                                                                                      #guerilla                                                                         #flanking                 #leader           #self pres.    #mercenary
                        #bts array
			lPromotionOdds = [100, 80, 60, 40, 20, 80, 80, 80, 60, 60, 60, 60, 20, 40, 20, 80, 60, 100, 80, 60, 100, 80, 60, 100, 80, 60, 100, 80, 60, 100, 80, 60, 40, 100, 80, 60, 60, 100, 80, 20, 60, 80, 60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100]#, 100, 100, 100]
                                                                                                              #guerilla              #woodsman3                                                     #flanking                 #leader           #range1        #mercenary #buggy self pres. commented
                        iRndNum = gc.getGame().getSorenRandNum(100, 'random')
                        #print (gc.getNumPromotionInfos(), len(lPromotionOdds))
                        if (iRndNum > lPromotionOdds[i]):
                                bEraMatch = false #skip this promotion
                        #Rhye - end

                        #Rhye - start (no anti-... before correct era)
                        if ((i == 7 or i == 24 or i == 34) and gc.getActivePlayer().getCurrentEra() < con.iRenaissance):
                                bEraMatch = false
                        if (i == 10 and gc.getActivePlayer().getCurrentEra() < con.iIndustrial):
                                bEraMatch = false
                        if (i == 9 and gc.getActivePlayer().getCurrentEra() < con.iClassical):
                                bEraMatch = false
                        #Rhye - end	
				
			# If the CyUnit can have the promotion and the era matched then append it to the end 
			# of promotionList
			if(isPromotionValid(iPromotionInfoType, objUnit.getUnitType(), False) and bEraMatch):
				promotionList.append(promotionInfo)
				
		return promotionList		
	
	
	# Returns a reduced set of promotions that the mercenary will have when it is actually
	# placed in the game.
	def getMercenaryPromotions(self, rawPromotionList):
		' objList - list of promotions that the mercenary will have.'
		
		# Return immediately if the rawPromotionList passed in is invalid
		if(rawPromotionList == None):
			return []

		# Return immediately if an empty rawPromotionList was passed in
		if(rawPromotionList == 0):
			return []		
			
		mercenaryPromotionList = []

                iMercenaryPromotionChance = g_iMercenaryPromotionChance + gc.getActivePlayer().getCurrentEra() #Rhye (stronger mercenaries later in the game)
		#print (iMercenaryPromotionChance) #Rhye
		
		# Go through the raw promotion list
		for i in range(len(rawPromotionList)):
			randVal = gc.getGame().getMapRand().get(100, "Unit Count")
			
			# If we beat the odds then append the promotion to the list containing the promotions
			# that mercenary will have
			#if(randVal < g_iMercenaryPromotionChance): #Rhye
			if(randVal < iMercenaryPromotionChance): #Rhye
				mercenaryPromotionList.append(rawPromotionList[i])
	
		# Backfill the prereq promotions if the variable is set and return the resulting list
		# of promotions
		if(g_bBackfillPrereqPromotions):
			return self.getBackfillPrereqPromotions(mercenaryPromotionList)

		return mercenaryPromotionList


	# Returns a list containing all of the promotions including the prereq promotions
	# for the promotion list passed in.
	def getBackfillPrereqPromotions(self, promotionList):
		' promoDict - the dictionary containing the full set of promotions '

		# Return immediately if the promotionList passed in is invalid
		if(promotionList == None):
			return []
			
		# Get the length of the promotionList passed in.
		listLength = len(promotionList)
		
		# Return immediately if an empty promotionList was passed in
		if(listLength == 0):
			return []		

		promoDict = {}

		# Go through the promotion list and populate the current set of promotions
		# in the promotion dictionary
		for i in range(listLength):
			promoDict[gc.getInfoTypeForString(promotionList[i].getType())] = promotionList[i]

		i = 0

		# Go through the promotionList until we get all of the prereq promotions
		while(i < listLength):
			promotionInfo = promotionList[i]

			# If the first promotion prereq is set and it hasn't been added to the promotion dictionary then process it
			if(promotionInfo.getPrereqOrPromotion1() != -1 and not promoDict.has_key(promotionInfo.getPrereqOrPromotion1())):

				# Append the first promotion prereq to the promotion list
				promotionList.append(gc.getPromotionInfo(promotionInfo.getPrereqOrPromotion1()))

				# Set the first promotion prereq to the promotion dictionary
				promoDict[promotionInfo.getPrereqOrPromotion1()] = gc.getPromotionInfo(promotionInfo.getPrereqOrPromotion1())
				
			# If the second promotion prereq is set and it hasn't been added to the promotion dictionary then process it
			if(promotionInfo.getPrereqOrPromotion2() != -1 and not promoDict.has_key(promotionInfo.getPrereqOrPromotion2())):

				# Append the second promotion prereq to the promotion list
				promotionList.append(gc.getPromotionInfo(promotionInfo.getPrereqOrPromotion2()))

				# Set the second promotion prereq to the promotion dictionary
				promoDict[promotionInfo.getPrereqOrPromotion2()] = gc.getPromotionInfo(promotionInfo.getPrereqOrPromotion2())
				
			i = i + 1
			
			# Get the new length of the promotion list since it might have changed
			listLength = len(promotionList)


		# Debug code - start
		if(g_bDebug):
			promotionList = promoDict.values()
			promotions = ""
			for i in range(len(promotionList)):
				promotions = promotions + promotionList[i].getType() + ", "		

			CvUtil.pyPrint(promotions)
		# Debug code - end
	
		# Return the new list of promotions 	
		return promoDict.values()
		
		
	# Returns the mercenaries available for hire.
	def getAvailableMercenaries(self):
		' mercenaryDict - the dictionary containing the mercenaries that are available for hire by players '
		
		# Setup the global mercenary pool if it doesn't exist
		if(sdEntityExists("Mercenaries Mod","MercenaryData") == False):
			self.setupMercenaryData()

		mercenaryDict = {}
	
		# Get the global mercenary pool
		mercenaries = sdGetVal("Mercenaries Mod", "MercenaryData", AVAILABLE_MERCENARIES)
				
		# Go through all of the mercenaries in the global mercenary pools and
		# add the ones not hired to the mercenaryDict dictionary
		for mercenaryName, mercenary in mercenaries.iteritems():

			# Create a blank mercenary
			tmpMercenary = self.createBlankMercenary()

			# Load the pseudo mercenary information into the mercenary 
			tmpMercenary.loadData(mercenary)
						
			# Add the mercenary into the mercenaryDict
			mercenaryDict[tmpMercenary.getName()] = tmpMercenary
			
		return mercenaryDict
	
	
	# Returns the income brought in by mercenaries that are units contracted out by a player
	def getPlayerMercenaryContractIncome(self, iPlayer):
		' totalMercenaryContractIncome - the income brought in by mercenaries that are units contracted out by a player '

		totalMercenaryContractIncome = 0

		# Get the units contracted out as mercenaries by the player		
		contractedUnitDictionary = self.getContractedOutUnits(iPlayer)
		
		# Go through the dictionary of units contracted out as mercenaries
		for mercenary in contractedUnitDictionary.itervalues():
		
			# Add the total maintenance cost of the mercenary to the totalMercenaryContractIncome
			if(mercenary.getOwner() != -1 and mercenary.isPlaced()):
				totalMercenaryContractIncome = totalMercenaryContractIncome + mercenary.getMercenaryMaintenanceCost()
				
		return totalMercenaryContractIncome
		
		
	# Returns the total amount of gold it costs to maintain the mercenaries the player has
	# hired.
	def getPlayerMercenaryMaintenanceCost(self, iPlayer):
		' totalMercenaryMaintenanceCost - the total amount of gold it costs to maintain the mercenaries the player has hired. '
		
		totalMercenaryMaintenanceCost = 0

		# Setup the global mercenary pool if it doesn't exist
		if(sdEntityExists("Mercenaries Mod","MercenaryData") == False):
			self.setupMercenaryData()

		# Get the global mercenary pool
		mercenaries = sdGetVal("Mercenaries Mod", "MercenaryData", HIRED_MERCENARIES)

		# Return immediately if an invalid value is passed for iPlayer
		if(not mercenaries.has_key(iPlayer)):
			return 0
					
		mercenaries = mercenaries[iPlayer]
		
		# Go through all of the mercenaries in the global mercenary pools and
		# get their maintenance cost.
		for mercenaryName, mercenary in mercenaries.iteritems():
			
			# Create a blank mercenary
			tmpMercenary = self.createBlankMercenary()

			# Load the pseudo mercenary information into the mercenary 
			tmpMercenary.loadData(mercenary)			
						
			# Add the mercenary maintenance cost to the total mercenary maintenance cost

			#Rhye - start Carthaginian UP
			#totalMercenaryMaintenanceCost = totalMercenaryMaintenanceCost + tmpMercenary.getMercenaryMaintenanceCost()
                        totalMercenaryMaintenanceCost = totalMercenaryMaintenanceCost + tmpMercenary.getMercenaryMaintenanceCostXPlayer(iPlayer)
                        #Rhye - end UP

			

		#Rhye - start
		if (not gc.getPlayer(iPlayer).isHuman()):
			totalMercenaryMaintenanceCost *= g_iAIMaintenanceCostPercent
			totalMercenaryMaintenanceCost /= 100
		#Rhye - end
			
			
		return totalMercenaryMaintenanceCost
	
	
	# Gets all of the hired mercenaries in the game.
	def getHiredMercenaries(self):
		' mercenaryDict - the dictionary containing all of the hired mercenaries in the game '
		
		# Setup the global mercenary pool if it doesn't exist
		if(sdEntityExists("Mercenaries Mod","MercenaryData") == False):
			self.setupMercenaryData()

		# Get the hired mercenaries from the global mercenary pool						
		mercenaries = sdGetVal("Mercenaries Mod", "MercenaryData", HIRED_MERCENARIES)	
		
		mercenaryDict = {}

		# Go through all of the mercenaries in the global mercenary pools and
		# add the ones hired to the mercenaryDict dictionary		
		for iPlayer in mercenaries.iterkeys():
		
			# Get the mercenaries for the player represented by iPlayer
			hiredMercenaries = mercenaries[iPlayer]
			
			for mercenary in hiredMercenaries.itervalues():
						
				# Create a blank mercenary
				tmpMercenary = self.createBlankMercenary()

				# Load the pseudo mercenary information into the mercenary 
				tmpMercenary.loadData(mercenary)

				# Add the mercenary into the mercenaryDict				
				mercenaryDict[tmpMercenary.getName()] = tmpMercenary
			
		return mercenaryDict
		
		
	# Returns all of the unplaced contracted out units for a player
	def getUnplacedContractedOutUnits(self, iPlayer):
		' mercenaryDict - the dictionary containing all of the unplaced contracted out units for a player '
		
		# Setup the global mercenary pool if it doesn't exist
		if(sdEntityExists("Mercenaries Mod","MercenaryData") == False):
			self.setupMercenaryData()
			return {}
			
		# Get the global mercenary pool
		mercenaries = sdGetVal("Mercenaries Mod", "MercenaryData", UNPLACED_MERCENARIES)
	
		mercenaryDict = {}
	
		for mercenary in mercenaries.itervalues():
			
			# Continue if the unplaced mercenary wasn't hired by the player
			if(mercenary["iBuilder"] != iPlayer):
				continue

			# Create a blank mercenary
			tmpMercenary = self.createBlankMercenary()

			# Load the pseudo mercenary information into the mercenary 
			tmpMercenary.loadData(mercenary)

			# Add the mercenary into the mercenaryDict				
			mercenaryDict[tmpMercenary.getName()] = tmpMercenary

		return mercenaryDict
			
		
	# Returns all of the unplaced contracted out units for a player	
	def getUnplacedPlayerMercenaries(self, iPlayer):
		' mercenaryDict - the dictionary containing all of the unplaced units contracted out by a player '
		
		# Setup the global mercenary pool if it doesn't exist
		if(sdEntityExists("Mercenaries Mod","MercenaryData") == False):
			self.setupMercenaryData()
			return {}
			
		# Get the global mercenary pool
		mercenaries = sdGetVal("Mercenaries Mod", "MercenaryData", UNPLACED_MERCENARIES)
	
		mercenaryDict = {}
	
		# Go through all of the unplaced mercenaries in the game
		for mercenary in mercenaries.itervalues():
			
			# Continue if the unplaced mercenary wasn't hired by the player
			if(mercenary["iOwner"] != iPlayer):
				continue

			# Create a blank mercenary
			tmpMercenary = self.createBlankMercenary()

			# Load the pseudo mercenary information into the mercenary 
			tmpMercenary.loadData(mercenary)

			# Add the mercenary into the mercenaryDict				
			mercenaryDict[tmpMercenary.getName()] = tmpMercenary

		return mercenaryDict
		
			
	# Gets the mercenaries hired by the player indicated in the iPlayer
	# variable.
	def getPlayerMercenaries(self, iPlayer):
		' mercenaryDict - the mercenaries hired by the player '
		
		# Setup the global mercenary pool if it doesn't exist
		if(sdEntityExists("Mercenaries Mod","MercenaryData") == False):
			self.setupMercenaryData()
			return
			
		# Get the global mercenary pool
		mercenaries = sdGetVal("Mercenaries Mod", "MercenaryData", HIRED_MERCENARIES)

		# Return immediately if an invalid value is passed for iPlayer
		if(not mercenaries.has_key(iPlayer)):
			return {}

		# Get the hired mercenaries for the player represented by iPlayer
		mercenaries = mercenaries[iPlayer]

		mercenaryDict = {}

		# Go through all of the mercenaries in the global mercenary pools and
		# add the ones hired by the player to the mercenaryDict dictionary		
		for mercenaryName, mercenary in mercenaries.iteritems():
			
			# Create a blank mercenary
			tmpMercenary = self.createBlankMercenary()

			# Load the pseudo mercenary information into the mercenary 
			tmpMercenary.loadData(mercenary)

			# Debug code - start
			if(g_bDebug):
				self.printMercenaryDataToLog(tmpMercenary)	
			# Debug code - end

			# Add the mercenary into the mercenaryDict				
			mercenaryDict[tmpMercenary.getName()] = tmpMercenary

		# Get all of the players unplaced mercenaries they have hired			
		tmpMercenaryDict = self.getUnplacedPlayerMercenaries(iPlayer)
		
		
		# Go through all of the players unplaced mercenaries they have hired and
		# add them to the mercenaryDict
		for mercenary in tmpMercenaryDict.itervalues():
		
			mercenaryDict[mercenary.getName()] = mercenary
			
		return mercenaryDict

		
	# Get the mercenary from the global mercenary pool with the name passed in	
	def getAvailableMercenary(self, mercenaryName):
		'objMercenary - the mercenary from the global mercenary pool with the name passed in.'
		
		# Setup the global mercenary pool if it doesn't exist
		if(sdEntityExists("Mercenaries Mod","MercenaryData") == False):
			self.setupMercenaryData()

		mercenaries = sdGetVal("Mercenaries Mod", "MercenaryData", AVAILABLE_MERCENARIES)	

		# Return immediately if the mercenary does not exist.
		if(not mercenaries.has_key(mercenaryName)):
			return None

		mercenary = mercenaries[mercenaryName]

		# Create a blank mercenary
		tmpMercenary = self.createBlankMercenary()

		# Load the pseudo mercenary information into the mercenary 
		tmpMercenary.loadData(mercenary)

		# Debug code - start		
		if(g_bDebug):
			self.printMercenaryDataToLog(tmpMercenary)	
		# Debug code - end
			
		return tmpMercenary


	# Gets the mercenary hired by the player indicated in the mercenaryName 
	# and iPlayer variables
	def getPlayerMercenary(self, mercenaryName, iPlayer):
			
		mercenary = None
			
		# Setup the global mercenary pool if it doesn't exist
		if(sdEntityExists("Mercenaries Mod","MercenaryData") == False):
			self.setupMercenaryData()

		# Get the global mercenary pool
		mercenaries = sdGetVal("Mercenaries Mod", "MercenaryData", HIRED_MERCENARIES)	

		# Return immediately if the iPlayer passed in is invalid
		if(not mercenaries.has_key(iPlayer)):
			return None
			
		mercenaries = mercenaries[iPlayer]

		# If we couldn't find the mercenary in the players hired pool, then lets check the 
		# unplaced hire mercenary pool, if it isn't there then return immediately.
		if(not mercenaries.has_key(mercenaryName)):
			mercenaries = self.getUnplacedPlayerMercenaries(iPlayer)
			
			if(not mercenaries.has_key(mercenaryName)):
				return None
		
			tmpMercenary = mercenaries[mercenaryName]

		else:
			# Get the mercenary hired by the player
			mercenary = mercenaries[mercenaryName]

			# Create a blank mercenary
			tmpMercenary = self.createBlankMercenary()

			# Load the pseudo mercenary information into the mercenary 
			tmpMercenary.loadData(mercenary)

			# Debug code - start
			if(g_bDebug):
				self.printMercenaryDataToLog(tmpMercenary)	
			# Debug code - end
					
		return tmpMercenary

	
	# Gets the mercenary from the global mercenary pool with the name given in 
	# mercenary name.
	def getMercenary(self, mercenaryName):
		' objMercenary - the instance of the Mercenary class that represents the mercenary '

		mercenary = None
		
		# Setup the global mercenary pool if it doesn't exist
		if(sdEntityExists("Mercenaries Mod","MercenaryData") == False):
			self.setupMercenaryData()
			return None
			
		# Get the global mercenary pool
		mercenaries = sdGetVal("Mercenaries Mod", "MercenaryData", AVAILABLE_MERCENARIES)

		# Return immediately if mercenaryName was not set
		if(mercenaryName == None):
			return None
			
		# If the mercenary was found then get the pseudo mercenary information from the 
		# global mercenary pool
		if(mercenaries.has_key(mercenaryName)):
			mercenary = mercenaries[mercenaryName]

		# If the mercenary was set to None after checking the available mercenaries
		# try to find the mercenary in the unplaced mercenaries dictionary
		if(mercenary == None):
		
			# Get the hired mercenaries from the global mercenary pool						
			mercenaries = sdGetVal("Mercenaries Mod", "MercenaryData", UNPLACED_MERCENARIES)
			
			if(mercenaries.has_key(mercenaryName)):
				mercenary = mercenaries[mercenaryName]
			
		# If the mercenary was set to None after checking the available mercenaries
		# try to find the mercenary in the hired mercenaries dictionaries for each
		# player
		if(mercenary == None):
		
			# Get the hired mercenaries from the global mercenary pool						
			mercenaries = sdGetVal("Mercenaries Mod", "MercenaryData", HIRED_MERCENARIES)	
		
			# Go through all of the mercenaries in the global mercenary pools and
			# try to find the mercenary in there
			for iPlayer in mercenaries.iterkeys():
		
				# Get the mercenaries for the player represented by iPlayer
				hiredMercenaries = mercenaries[iPlayer]

				# If we found the mercenary, break out of the loop
				if(hiredMercenaries.has_key(mercenaryName)):			
					mercenary = hiredMercenaries[mercenaryName]
					break
		
		# Return immediately if we were unable to find the mercenary
		if(mercenary == None):
			return None

		# Create a blank mercenary
		objMercenary = self.createBlankMercenary()

		# Load the pseudo mercenary information into the mercenary 
		objMercenary.loadData(mercenary)

		return objMercenary
		
		
	# Prints out the mercenary information into the debug log. Wooot!!!
	def printMercenaryDataToLog(self, objMercenary):
		CvUtil.pyPrint("__________________ Mercenary Data Dump Start __________________")
		CvUtil.pyPrint("          Name: " + objMercenary.strMercenaryName)

		CvUtil.pyPrint("     Unit Type: " + objMercenary.getUnitInfo().getDescription())
		CvUtil.pyPrint("     Hire Cost: " + str(objMercenary.getHireCost()))
		CvUtil.pyPrint("   Maint. Cost: " + str(objMercenary.getMercenaryMaintenanceCost()))
		CvUtil.pyPrint("         Level: " + str(objMercenary.iLevel))
		CvUtil.pyPrint("            XP: " + str(objMercenary.iExperienceLevel))
		CvUtil.pyPrint("Promotion List: ")

		# Loop through the mercenary's promotion list and print them out to the log.
		for i in range(len(objMercenary.promotionList)):
			CvUtil.pyPrint("               " + objMercenary.promotionList[i].getDescription())
			
		CvUtil.pyPrint("")		
		CvUtil.pyPrint("      Is Hired: " + str(objMercenary.bHired))

		# If the mercenary is hired show the information.
		if(objMercenary.bHired):
			CvUtil.pyPrint("      Hired by: " + gc.getPlayer(objMercenary.iOwner).getName())
		else:
			CvUtil.pyPrint("      Hired by: None")
		
		if(objMercenary.iBuilder != -1):
			CvUtil.pyPrint("      Built by: " + gc.getPlayer(objMercenary.iBuilder).getName())
		else:
			CvUtil.pyPrint("      Built by: None")

		if(objMercenary.iPlacementTurn != -1):
			CvUtil.pyPrint("To be Placed on: " + str(objMercenary.iPlacementTurn))  
		else:
			CvUtil.pyPrint("To be Placed on: already placed")  
		
		CvUtil.pyPrint("__________________ Mercenary Data Dump End   __________________")
		CvUtil.pyPrint("")
		

	# Creates and returns a blank instance of the Mercenary class
	def createBlankMercenary(self):
		return Mercenary("",None,[],-1,-1)
		
		
	# Fires the mercenary from their current employeer and makes them available to be hired
	# by other players
	def fireMercenary(self, mercenaryName, iPlayer):
		
		# Get the global mercenary pool
		mercenaries = sdGetVal("Mercenaries Mod", "MercenaryData", HIRED_MERCENARIES)	

		# Setup the global mercenary pool if it doesn't exist and return immediately
		if(sdEntityExists("Mercenaries Mod","MercenaryData") == False):
			self.setupMercenaryData()
			return
			
		# Return immediately if the iPlayer passed in is invalid
		if(not mercenaries.has_key(iPlayer)):
			return None

		mercenaries = mercenaries[iPlayer]

		# Return immediately if the mercenary wasn't hired by the player
		if(not mercenaries.has_key(mercenaryName)):
			return
			
		# Get the mercenary hired by the player
		mercenary = mercenaries[mercenaryName]

		# Return immediately if the mercenary was not retrieved from the global
		# mercenary pool
		if(mercenary == None):
			return 
		
		# Create a blank mercenary
		tmpMercenary = self.createBlankMercenary()

		# Load the pseudo mercenary information into the mercenary 
		tmpMercenary.loadData(mercenary)

		# Debug code - start
		if(g_bDebug):
			self.printMercenaryDataToLog(tmpMercenary)	
		# Debug code - end
				
		# Fires the mercenary from their current employeer, removes them from the game and
		# makes them available in the available mercenary pool
		tmpMercenary.fire()

		# Remove the mercenary from the player's mercenary pool
		del mercenaries[mercenaryName]
		
		playerMercenaries = sdGetVal("Mercenaries Mod", "MercenaryData", HIRED_MERCENARIES)

		playerMercenaries[iPlayer] = mercenaries
		sdSetVal("Mercenaries Mod", "MercenaryData", HIRED_MERCENARIES, playerMercenaries)		
		playerMercenaries = sdGetVal("Mercenaries Mod", "MercenaryData", HIRED_MERCENARIES)

		# Debug code - start
		if(g_bDebug):
			self.printMercenaryDataToLog(tmpMercenary)	
		# Debug code - end

		# Saves the mercenary in the global mercenary pool
		self.saveMercenary(tmpMercenary)
	
	
	# This method acts as a proxy to the hire method in the Mercenary class. It will
	# get the mercenary object in the global mercenary pool
	def hireMercenary(self, mercenaryName, iPlayer):
		' bSaved - returns true if the objMercenary was successfully hired'
		
		city = None
		
		# Return immediately if the player specified in iPlayer is not alive
		if(not gc.getPlayer(iPlayer).isAlive()):
			return false
			
		# Get the mercenary from the global mercenary pool
		mercenary = self.getMercenary(mercenaryName)
				
		# Return immediately if the mercenary was not retrieved from the global
		# mercenary pool
		if(mercenary == None):
			return false
		
		mercenaries = sdGetVal("Mercenaries Mod", "MercenaryData", AVAILABLE_MERCENARIES)
		
		# Remove the mercenary from the global mercenary pool
		del mercenaries[mercenaryName]
		
		sdSetVal("Mercenaries Mod", "MercenaryData", AVAILABLE_MERCENARIES, mercenaries)		
	
		# Get the starting location for the mercenary if we are not delaying their
		# placement	
		if(not g_bDelayMercenaryPlacement):
			city = self.getMercenaryStartingLocation(iPlayer)

                #Rhye - start
		if (iPlayer != utils.getHumanID()):
                        mercenary.setName(MercenaryNameUtils.getRandomMercenaryName(iPlayer, mercenary.getUnitInfoID(), False))
                #debug
                #if (iPlayer == utils.getHumanID()):
                #        mercenary.setName(MercenaryNameUtils.getRandomMercenaryName(con.iAmerica, mercenary.getUnitInfoID(), False))
                #Rhye - end
                
		mercenary.hire(iPlayer, city)

		print("Mercenary hired by: " + gc.getPlayer(mercenary.iOwner).getName()) #Rhye
	
		# Debug code - start
		if(g_bDebug):
			self.printMercenaryDataToLog(mercenary)	
		# Debug code - end
		
		# Saves the mercenary in the global mercenary pool
		self.saveMercenary(mercenary)

	
	# Places mercenaries in the game that have reached their game turn.
	def placeMercenaries(self, iPlayer):
	
		# Get the current game turn
		iGameTurn = gc.getGame().getGameTurn()
		
		mercenaries = sdGetVal("Mercenaries Mod", "MercenaryData", UNPLACED_MERCENARIES)
		
		mercenariesToPlace = []
		
		# Go through all of the unplaced mercenaries and check to see if they need to be 
		# placed in the game.
		for mercenary in mercenaries.itervalues():

			# Place the mercenary immediately if the placement turn isn't set in the 
			# mercenary, the mercenary has an owner and the mercenary isn't in the game.
			if(mercenary["iPlacementTurn"] == -1 and mercenary["iOwner"] == iPlayer and mercenary["iUnitID"] == -1):
				mercenariesToPlace.append(mercenary)

			# If the game turn matches the mercenaries placement turn then place them
			# in the game.			
			elif(mercenary["iPlacementTurn"] <= iGameTurn and mercenary["iOwner"] == iPlayer):
				mercenariesToPlace.append(mercenary)
			
			# If the game turn matches the mercenaries placement turn then place them
			# in the game.			
			elif(mercenary["iPlacementTurn"] <= iGameTurn and mercenary["iOwner"] == -1 and mercenary["iBuilder"] == iPlayer):
				mercenariesToPlace.append(mercenary)
			
						
		# Go through the mercenaries to be placed and place them.
		for mercenary in mercenariesToPlace:
		
			# Create a blank mercenary
			tmpMercenary = self.createBlankMercenary()

			# Load the pseudo mercenary information into the mercenary 
			tmpMercenary.loadData(mercenary)

			# Remove the mercenary to be placed from the unplaced mercenaries dictionary			
			del mercenaries[tmpMercenary.getName()]
			
			# Get the starting location for the mercenary
			objCity = self.getMercenaryStartingLocation(iPlayer)

			# Place the mercenary in the game
			tmpMercenary.place(objCity)
			
			if(tmpMercenary.iBuilder != tmpMercenary.iOwner and tmpMercenary.iOwner != -1):
				# Save the mercenary 
				self.saveMercenary(tmpMercenary)

		# Save the modified unplaced mercenary dictionary						
		sdSetVal("Mercenaries Mod", "MercenaryData", UNPLACED_MERCENARIES, mercenaries)
		
		
	# Saves the mercenary passed in the objMercenary object in the global mercenary
	# pool.	returns true if the objMercenary was successfully saved, otherwise it will return
	# false.
	def saveMercenary(self, objMercenary):
		' bSaved - returns true if the objMercenary was successfully saved'
		
		# Return immediately if the objMercenary object passed in was not set to
		# anything
		if(objMercenary == None):
			return false
			
		# Return immediately if the objMercenary object passed in was not instance of
		# the Mercenary class
		if(not isinstance(objMercenary, Mercenary)):
			return false

		# Setup the global mercenary pool if it doesn't exist
		if(sdEntityExists("Mercenaries Mod","MercenaryData") == False):
			self.setupMercenaryData()

		# Check to see if the mercenary has been placed or not
		if(objMercenary.iPlacementTurn != -1):
			# If the mercenary wasn't placed then get the unplaced mercenaries pool
			mercenaries = sdGetVal("Mercenaries Mod", "MercenaryData", UNPLACED_MERCENARIES)
		elif(objMercenary.getOwner() == -1):
			# Get the mercenaries from the global data
			mercenaries = sdGetVal("Mercenaries Mod", "MercenaryData", AVAILABLE_MERCENARIES)
		else:
			mercenaries = sdGetVal("Mercenaries Mod", "MercenaryData", HIRED_MERCENARIES)
			mercenaries = mercenaries[objMercenary.getOwner()]

		# Debug code - start
		if(g_bDebug):

			CvUtil.pyPrint(" Saving: " + objMercenary.getName())
			self.printMercenaryDataToLog(objMercenary)
		# Debug code - end
				
		# Save the mercenary information using the dictionary representation of the mercenary
		# so there are no conflicts using pickle.
		mercenaries[objMercenary.strMercenaryName] = objMercenary.getDictionaryRepresentation()

		# Debug code - start
		if(g_bDebug):
			self.printMercenaryDataToLog(objMercenary)	
		# Debug code - end

		if(objMercenary.iPlacementTurn != -1):
			return sdSetVal("Mercenaries Mod", "MercenaryData", UNPLACED_MERCENARIES, mercenaries)					
		elif(objMercenary.getOwner() != -1):
			playerMercenaries = sdGetVal("Mercenaries Mod", "MercenaryData", HIRED_MERCENARIES)
			playerMercenaries[objMercenary.getOwner()] = mercenaries
			return sdSetVal("Mercenaries Mod", "MercenaryData", HIRED_MERCENARIES, playerMercenaries)		
		else:
			# Save the updated mercenaries information in the global data. I don't think this step
			# is necessary, but after some testing I found that it might be. TO DO: test this line
			# to make sure it is really necessary to do.
			return sdSetVal("Mercenaries Mod", "MercenaryData", AVAILABLE_MERCENARIES, mercenaries)		


	# Gets the max era from the players in the game.
	def getMaxGameEra(self):
		iEra = 0
		
		# Get the active players in the game
		playerList = PyGame.getCivPlayerList()
		
		# Go through the active players in the game
		for pPlayer in playerList:
		
			# If the current player's era is bigger than the current value of iEra
			# set it as the value of iEra
			if(pPlayer.CyGet().getCurrentEra() > iEra):
				iEra = pPlayer.CyGet().getCurrentEra()
		
		return iEra

		
	# Returns the total number of military units in the game
	def getMilitaryUnitCount(self):

		totalMilitaryUnits = 0
		
		# Get the active players in the game
		playerList = PyGame.getCivPlayerList()

		# Go through the active players in the game
		for pPlayer in playerList:
		
			# Add the player's total number of military units to the total
			totalMilitaryUnits = totalMilitaryUnits + pPlayer.CyGet().getNumMilitaryUnits()
			
		return totalMilitaryUnits
		

	# Creates a random the number of mercenaries at most being the value passed in the 
	# g_iMaxMercenaryCreationCount variable.
	def addMercenariesToPool(self):

		mercenaries = {}
		mercenaryNames = {}
		objMercenary = None
		
		# Get the era for the current active player
		iEra = gc.getActivePlayer().getCurrentEra()		

		# Get the era that is the latest era from the players in the game if g_bMaxPlayerGameEra is
		# true
		if(g_bMaxPlayerGameEra):
			iEra = self.getMaxGameEra()
		
		# This conditional should never be true since the "Mercenary Manager" button should
		# not be displayed when the current player era is less than the g_iStartingEra value
		# but just to make sure we'll test the condition
		if(iEra < g_iStartingEra):
			return	    
		
		# Setup the global mercenary pool if it doesn't exist
		if(sdEntityExists("Mercenaries Mod","MercenaryData") == False):
			self.setupMercenaryData()
		
		# Get the mercenaries from the global data
		mercenaries = sdGetVal("Mercenaries Mod", "MercenaryData", AVAILABLE_MERCENARIES)
		mercenaryNames  = sdGetVal("Mercenaries Mod", "MercenaryData", MERCENARY_NAMES)
		
		regularCount = self.getMilitaryUnitCount()
		availableMercenaryCount = len(mercenaries)
				
		# Return immediately if the current mercenary to regulars ratio is larger than the
		# configured amount
		if(availableMercenaryCount > 0 and (float(availableMercenaryCount)/float(regularCount)) >= (float(g_iRatioMercenariesToRegulars)/float(100))):
			strMerc = "No new mercenaries added to the pool. The current ratio is: %f the configured ratio is: %f" %((float(availableMercenaryCount)/float(regularCount)), (float(g_iRatioMercenariesToRegulars)/float(100)))

			# Debug code - start
			if(g_bDebug):
				CvUtil.pyPrint(strMerc)
			# Debug code - end
			
			return
			
		# Return immediately if the size of the global mercenary pool is larger than the
		# value set in the g_iMaxGlobalMercenaryPoolSize variable
		if(availableMercenaryCount >= g_iMaxGlobalMercenaryPoolSize):

			# Debug code - start
			if(g_bDebug):
				CvUtil.pyPrint("No new mercenaries added to the pool. There are currently: " + str(len(mercenaries)) + " in the global mercenary pool")
			# Debug code - end
			
			return
		
		# Get the number of mercenaries to add to the global mercenary pool. 
		maxMercenaryCount = gc.getGame().getMapRand().get(g_iMaxMercenaryCreationCount, "Max Mercenary Count") + g_iMinMercenaryCreationCount 

		# Create the mercenaries
		for i in range(maxMercenaryCount):
			if(g_bEraAppropriateMercenaries):
				objMercenary = self.getEraAppropriateRandomMercenary(iEra)
			else:
				objMercenary = self.getRandomMercenary()
				
			# Record the mercenary name so it won't be used for future mercenaries.
			#Rhye - start
			#mercenaryNames[objMercenary.getName()] = objMercenary.getName()
			if (objMercenary != None):
                                mercenaryNames[objMercenary.getName()] = objMercenary.getName()
                        #Rhye - end
                	
			
		sdSetVal("Mercenaries Mod", "MercenaryData", MERCENARY_NAMES, mercenaryNames)
		#print("Mercenaries Mod", "MercenaryData", MERCENARY_NAMES, mercenaryNames)
		
		CyInterface().addMessage(gc.getActivePlayer().getID(), False, con.iDuration, CyTranslator().getText("TXT_KEY_NEW_MERCENARIES", ()), "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)

	# Removes the number of mercenaries	specified by iCount
	def removeMercenariesFromPool(self, iCount):

		# Setup the global mercenary pool if it doesn't exist and return immediately
		if(sdEntityExists("Mercenaries Mod","MercenaryData") == False):
			self.setupMercenaryData()
			return
		
		# Return immediately if the number of mercenaries to remove is less than
		# or equal to zero
		if(iCount <= 0):
			return

		# Get the mercenaries from the global mercenary pool		
		mercenaries = sdGetVal("Mercenaries Mod", "MercenaryData", AVAILABLE_MERCENARIES)

		# Return immediately if there are no available mercenaries in the global mercenary
		# pool
		if(len(mercenaries) <= 0):
			return

		mercenariesToRemove = []
		
		# Goes through the mercenaries and removes the number of mercenaries specified by iCount
		for mercenaryName in mercenaries:
		
			# Do not remove player build mercenaries from the global mercenary pool
			if(mercenaries[mercenaryName]["iBuilder"] != -1):
				continue
				
			# Debug code - start
			if(g_bDebug):
				CvUtil.pyPrint("Removing: " + mercenaryName + " from the global mercenary pool.")
			# Debug code - end

			# Append the mercenary name to be removed from the global mercenary pool
			mercenariesToRemove.append(mercenaryName)

			# Break out of the for loop if we have the correct of mercenaries to remove from the
			# global mercenary pool
			if(len(mercenariesToRemove) == iCount):
				break
		
		# Remove the mercenaries from the mercenary dictionary
		for mercenaryName in mercenariesToRemove:
			del mercenaries[mercenaryName]

		# Save the new global mercenary pool			
		sdSetVal("Mercenaries Mod", "MercenaryData", AVAILABLE_MERCENARIES, mercenaries)		
		

	# Removes the mercenary from the game				
	def removePlayerMercenary(self, objUnit):

		# Setup the global mercenary pool if it doesn't exist
		if(sdEntityExists("Mercenaries Mod","MercenaryData") == False):
			self.setupMercenaryData()
			return
			
		# Return immediately if an invalid objUnit was passed in
		if(objUnit == None):
			return
			
		# Get the owner of the unit
		iPlayer = objUnit.getOwner()

		# Get the actual name of the mercenary
		mercenaryName = objUnit.getNameNoDesc()
		
		mercenaries = sdGetVal("Mercenaries Mod", "MercenaryData", HIRED_MERCENARIES)

		# Return immediately if iPlayer value is invalid
		if(not mercenaries.has_key(iPlayer)):
			return

		mercenaries = mercenaries[iPlayer]

		# Return immediately if the mercenary isn't hired by the player
		if(not mercenaries.has_key(mercenaryName)):
			return
		
		# Get the mercenary from the players mercenary pool
		mercenary = mercenaries[mercenaryName]

		# Remove the mercenary from the player's mercenary pool			
		del mercenaries[mercenaryName]
					
		playerMercenaries = sdGetVal("Mercenaries Mod", "MercenaryData", HIRED_MERCENARIES)

		playerMercenaries[iPlayer] = mercenaries
		sdSetVal("Mercenaries Mod", "MercenaryData", HIRED_MERCENARIES, playerMercenaries)		
		playerMercenaries = sdGetVal("Mercenaries Mod", "MercenaryData", HIRED_MERCENARIES)
		CvUtil.pyPrint("Removed mercenary %s" %(mercenaryName))
	
	
	# Returns the starting city for a player's mercenary
	def getMercenaryStartingLocation(self, iPlayer):
		' CyCity - the starting city for hired mercenaries'
		player = gc.getPlayer(iPlayer)
		
		objCity = None
		
		if(g_strMercenaryStartingLocation == "Capital City"):
			objCity = player.getCapitalCity()

		elif(g_strMercenaryStartingLocation == "Civilization Edge"):
			objCity = self.getCivilizationEdgeCity(iPlayer)

		elif(g_strMercenaryStartingLocation == "Random"):
			objCity = player.getCity(gc.getGame().getMapRand().get(player.getNumCities(), "Random City"))

		elif(len(g_strMercenaryStartingLocation) > 0):
			objCity = self.getRandomCityWithBuildings(iPlayer)			

		else:
			objCity = player.getCity(gc.getGame().getMapRand().get(player.getNumCities(), "Random City"))
		
		if(objCity == None):
			objCity = player.getCity(gc.getGame().getMapRand().get(player.getNumCities(), "Random City"))

		return objCity


	# Returns a random city that has one or more buildings set in the g_buildingInfoTypeList
	# variable
	def getRandomCityWithBuildings(self, iPlayer):
		'CyCity - the city containing at least one or more buildings set in the g_buildingInfoTypeList variable'
		# Get the player
		pyPlayer = PyPlayer(iPlayer)

		# Get the player's cities
		cityList = pyPlayer.getCityList()

		possibleCityList = []			

		# Go through the player's cities and get the ones that contain one or more buildings
		# set in the g_buildingInfoTypeList variable.			
		for city in cityList:
		
			# Go through the buildings set in the g_buildingInfoTypeList
			for buildingInfoTypeID in g_buildingInfoTypeList:

				# Append the city to the possibleCityList for each match found
				# this way the cities that are matched more have a better chance
				# of being the city where the mercenary will appear.
				if(city.hasBuilding(buildingInfoTypeID)):
					possibleCityList.append(city)
					
		# If no cities were found containing one or more buildings set in the 
		# g_buildingInfoTypeList variable then return None
		if(len(possibleCityList) == 0):
			return None

		# return a random city containing one or more buildings set in the 
		# g_buildingInfoTypeList variable.
		return possibleCityList[gc.getGame().getMapRand().get(len(possibleCityList), "Random City")].GetCy()
	
				
	# Returns the city that is the farthest away from the players capital city.				
	def getCivilizationEdgeCity(self, iPlayer):
		'CyCity - the farthest city away from the players capital city'

		# Get the player
		pyPlayer = PyPlayer(iPlayer)

		# Get the player's cities
		cityList = pyPlayer.getCityList()
		
		# Get the player's capital city
		capitalCity = pyPlayer.CyGet().getCapitalCity()
		
		maxEdgeDistance = 0
		edgeCity = None
		
		# Go through each one of the player's cities
		for city in cityList:
		
			# Get the distance of the city from the capital city
			edgeDistance = self.getCityDistance(capitalCity, city)

			# If the cities distance is longer than the current max distance
			if(edgeDistance >= maxEdgeDistance):
				
				# Set the city and the edgeCity
				edgeCity = city

				# set the cities distance from the player's capital city as the 
				# maxEdgeDistance 
				maxEdgeDistance = edgeDistance
		
		if(edgeCity == None):
			return None
			
		# Return the farthest city away from the players capital city	
		return edgeCity.GetCy()
	
		
	# Returns the distance between city A and city B
	def getCityDistance(self, objCityA, objCityB):
		' int - the distance between objCityA and objCityB'

		# Return zero immediately if city a passed in is invalid	
		if(objCityA == None):
			return 0

		# Return zero immediately if city b passed in is invalid
		if(objCityB == None):
			return 0
			
		return self.getPlotDistance(objCityA.plot(), objCityB.plot())
		
		
	# Calculates the distance between two plots using the formula:
	# MAX(ABS(X2-X1), ABS(Y2-Y1))
	def getPlotDistance(self, objPlotA, objPlotB):

		# Return zero immediately if plot a passed in is invalid	
		if(objPlotA == None):
			return 0

		# Return zero immediately if plot b passed in is invalid
		if(objPlotB == None):
			return 0
			
		' iDist - the distance between objPlotA and objPlotB'
		dX = abs(objPlotB.getX()-objPlotA.getX())
		dY = abs(objPlotB.getY()-objPlotA.getY())
		dist = max(dX, dY)

		# if you want it in one line to avoid variable assignments: 
		# return max(abs(objPlotB.getX()-objPlotA.getX()), abs(objPlotB.getY()-objPlotA.getY()))
		return dist
	
	
	# Returns the mercenary that is the costliest to maintain from the dictionary passed in
	def getHighestMaintenanceMercenary(self, mercenaryDict):
	
		maintenanceCost = 0
		highestMaintenanceMercenary = None
		
		# Go through the dictionary
		for mercenaryName in mercenaryDict:
		
			# If the current mercenary is the most expensive to maintain then save the
			# information
			if(mercenaryDict[mercenaryName].getMercenaryMaintenanceCost() > maintenanceCost):
				maintenanceCost = mercenaryDict[mercenaryName].getMercenaryMaintenanceCost()
				highestMaintenanceMercenary = mercenaryDict[mercenaryName]

		return highestMaintenanceMercenary
		
	
	# Returns the list of civilizations the player passed in is at war with.
	def getAtWarCivilizations(self, iPlayer):
		
		# Get the player reference
		player = gc.getPlayer(iPlayer)
		
		# Return immediately an empty list if the player reference is set
		# to None
		if(gc.getPlayer(iPlayer) == None):
			return []

		# Get the player's team
		iPlayerTeam = player.getTeam()
		playerTeam = gc.getTeam(iPlayerTeam)
		
		enemyPlayersList = []
		
		# Get the list of players in the game
		playerList = PyGame.getCivPlayerList()
		
		# Go through the list of players in the game
		for pyPlayer in playerList:
			cyPlayer = pyPlayer.CyGet()
	
			# If the player passed in is at war with the current player
			# being processed then add them to the enemyPlayersList		
			if(playerTeam.isAtWar(cyPlayer.getTeam())):
                                #Rhye - start
				#enemyPlayersList.append(cyPlayer)
                                if ((cyPlayer.getID() < con.iNumPlayers and gc.getTeam(gc.getPlayer(iPlayer).getTeam()).canContact(cyPlayer.getID())) or (cyPlayer.getID() >= con.iNumPlayers and gc.getGame().getGameTurn() >= getTurnForYear(-650) and gc.getGame().getGameTurn() <= getTurnForYear(-690))):
                                        enemyPlayersList.append(cyPlayer)
                                #Rhye - end
				

		return enemyPlayersList
		
	
	# Returns the number of players more powerful than the one passed in			
	def getMorePowerfulPlayerCount(self, iPlayer):
		
		playerCount = 0

		# Get the player reference
		player = gc.getPlayer(iPlayer)
		
		# Return immediately an empty list if the player reference is set
		# to None
		if(gc.getPlayer(iPlayer) == None):
			return 0
		
		# Get the list of players in the game
		playerList = PyGame.getCivPlayerList()
		
		# Go through the list of players in the game
		for pyPlayer in playerList:
			cyPlayer = pyPlayer.CyGet()
	
			# If the other player is more powerful increment playerCount
			if(cyPlayer.getPower() > player.getPower()):
				playerCount = playerCount + 1

		return playerCount
		
						
	# Currently returns the most expensive mercenary that is less expensive than the iGold value passed in.
	# This method needs to be rewritten to get the best mercenary with better definitions		
	def getBestAvailableMercenary(self, iGold, iPlayer):

		hireCost = 0
		
		mercenary = None
		
		# Get the available mercenaries from the global mercenary pool
		mercenaryDict = self.getAvailableMercenaries()

		# Go through the available mercenaries						
		for mercenaryName in mercenaryDict:

			# Calculate how much gold the player will have after hiring the mercenary.
			#Rhye - start Carthaginian UP
			#tmpGold = iGold - mercenaryDict[mercenaryName].getHireCost()
			tmpGold = iGold - mercenaryDict[mercenaryName].getHireCostXPlayer(iPlayer)
			#Rhye - end Carthaginian UP
			
			# Continue immediately if the player can't support the mercenary
			if(tmpGold <= 0):
				continue

			#Rhye - start continents
			if (not mercenaryDict[mercenaryName].canHireUnit(iPlayer)):
                                continue
			#Rhye - end
				
			# Get the proposed mercenary maintenance cost
			#Rhye - start Carthaginian UP
			#proposedMercenaryMaintenanceCost = (mercenaryDict[mercenaryName].getMercenaryMaintenanceCost()+self.getPlayerMercenaryMaintenanceCost(iPlayer))
                        proposedMercenaryMaintenanceCost = (mercenaryDict[mercenaryName].getMercenaryMaintenanceCostXPlayer(iPlayer)+self.getPlayerMercenaryMaintenanceCost(iPlayer))
                        #Rhye - end
                        
			# If the proposed mercenary maintenance cost is 0 then set it to 1
			# to avoid divide by zero errors.
			if(proposedMercenaryMaintenanceCost == 0):
				proposedMercenaryMaintenanceCost = 1
				
			# Calculate how many turns the player will be able to support the mercenary 
			# when hired. 
			supportTurns = tmpGold/proposedMercenaryMaintenanceCost
			
			# Get the cost to hire the mercenary
			#Rhye - start Carthaginian UP
			#mercenaryHireCost = mercenaryDict[mercenaryName].getHireCost()
			mercenaryHireCost = mercenaryDict[mercenaryName].getHireCostXPlayer(iPlayer)
			#Rhye - end Carthaginian UP

			# Debug code - start
			if(g_bDebug):
				CvUtil.pyPrint(gc.getPlayer(iPlayer).getName() + " mercenaryHireCost:" + str(mercenaryHireCost) + " hireCost:" + str(hireCost) + " iGold:" + str(iGold) + " mercenaryHireCost:" + str(mercenaryHireCost) + " supportTurns:" + str(supportTurns)) 
			# Debug code - end
					
			# Set the mercenary as the best mercenary if it has the highest cost 
			# but is less expensive than the iGold value passed in and it can 
			# support the mercenary for at least 5 turns. Why 5 turns? Well if
			# someone comes up with a better number please let me know. Otherwise
			if(mercenaryHireCost > hireCost and iGold > mercenaryHireCost and supportTurns >= 5):
                                #Rhye - start Carthaginian UP
				#hireCost = mercenaryDict[mercenaryName].getHireCost()
                                hireCost = mercenaryDict[mercenaryName].getHireCostXPlayer(iPlayer)
				#Rhye - end Carthaginian UP
				mercenary = mercenaryDict[mercenaryName]
				
				# Debug code - start
				if(g_bDebug):
					CvUtil.pyPrint("Potential mercenary for " + gc.getPlayer(iPlayer).getName() + " is " + mercenary.getName())
				# Debug code - end
				
		# Debug code - start
		if(g_bDebug and mercenary != None):
			CvUtil.pyPrint("Best mercenary for " + gc.getPlayer(iPlayer).getName() + " is " + mercenary.getName())
		# Debug code - end
		
		return mercenary
		
		
	# Performs the thinking for the computer players in regards to the mercenaries mod functionality.
	# It will:
	#   - Fire mercenaries
	#   - Hire mercenaries	
	# It needs to be more complex but for right now it works
	def computerPlayerThink(self, iPlayer):

                #pass
            
		# Get the player
		player = gc.getPlayer(iPlayer)
		
		# Return immediately if the player is a filthy human :p
		if(player.isHuman()):
			return

		# Return immediately if the player is a barbarian
		if(player.isBarbarian()):
			return

		# Get the current gold for the player			
		currentGold = player.getGold()

		# Get the computer's current mercenary maintenance costs
		mercenaryMaintenanceCost = self.getPlayerMercenaryMaintenanceCost(iPlayer)

		# Get the computer's current mercenaries
		mercenaryDict = self.getPlayerMercenaries(iPlayer)

		mercenary = None

		# Debug code - start
		if(g_bDebug):
			CvUtil.pyPrint(player.getName() + " current gold: " + str(currentGold) + " mercenary maintenance cost: " + str(mercenaryMaintenanceCost))
		# Debug code - end
		
		# Before having the computer hire more mercenaries check to see if they 
		# have enough money to support their current mercenaries, if they don't 
		# fire some until they can support their current mercenaries
		if(currentGold - mercenaryMaintenanceCost < 0):
			while(currentGold - mercenaryMaintenanceCost < 0):

				# Get the mercenary with the highest maintenance cost
				mercenary = self.getHighestMaintenanceMercenary(mercenaryDict)

				# Return immediately if no mercenary wasn't returned
				if(mercenary == None):
					return

				# Have the computer fire the mercenary
				self.fireMercenary(mercenary.getName(), iPlayer)
				del mercenaryDict[mercenary.getName()]
				mercenaryMaintenanceCost = self.getPlayerMercenaryMaintenanceCost(iPlayer)

			# Return since the computer player won't be able to support any new mercenaries in their
			# army.
			return
		
		# Don't let players with no cities hire mercenaries
		if(gc.getPlayer(iPlayer).getNumCities() <= 0):
			return

		#Rhye - start
                iHireOdds = gc.getGame().getSorenRandNum(100, 'odds')
                if (iHireOdds < con.tHire[iPlayer]):
                        return
		#Rhye - end

		
		# Get all of the players at war with the player
		enemyPlayersList = self.getAtWarCivilizations(iPlayer)

		#Rhye - start
		print (iPlayer, "enemyPlayersList", len(enemyPlayersList))
		if (not enemyPlayersList):
			return
		#Rhye - end

		# This will be the multiplier for how many mercenaries will 
		iMorePowerfulEnemies = 0
		
		# Go through all of the players enemies
		for ePlayer in enemyPlayersList:

			# If the current players enemies is more powerful then increment
			# iMorePowerfulEnemies
			if(player.getPower() < ePlayer.getPower()):
				iMorePowerfulEnemies = iMorePowerfulEnemies + 1

                mercenaryCount = (iMorePowerfulEnemies * len(enemyPlayersList)) + self.getMorePowerfulPlayerCount(iPlayer)
                
                # Get the random number of mercenaries that the player will get
                #Rhye - start bugfix		
		#randomMercCount = gc.getGame().getMapRand().get(mercenaryCount, "Random Merc Count")
		randomMercCount = gc.getGame().getSorenRandNum(mercenaryCount, 'Random Merc Count')
		#Rhye - end
		
		# Debug code - start
		if(g_bDebug):
			CvUtil.pyPrint(player.getName() + " will try to get: " + str(randomMercCount) + " mercenaries out of " + str(mercenaryCount))
		# Debug code - end

		# Hire the random number of mercenaries
		for i in range(randomMercCount):

			# Get the best available mercenary
			mercenary = self.getBestAvailableMercenary(currentGold, iPlayer)

			# Return immediately if a mercenary wasn't returned
			if(mercenary == None):
				return

			# Have the computer hire the mercenary			
			self.hireMercenary(mercenary.getName(), iPlayer)

			# Debug code - start
			if(g_bDebug):
				CvUtil.pyPrint(player.getName() + " current gold: " + str(currentGold) + " Hired " + mercenary.getName())
			# Debug code - end

			# deduct the hire cost from the computer players gold
			#Rhye - start Carthaginian UP
			#currentGold = currentGold - mercenary.getHireCost()
			currentGold = currentGold - mercenary.getHireCostXPlayer(iPlayer)
			#Rhye - end Carthaginian UP

			#Rhye - start
			currentGold *= g_iAIHireCostPercent
			currentGold /= 100
			#Rhye - end

			# Set the new modified gold amount
			player.setGold(currentGold)
		

	# Returns true if the objUnit is a mercenary, false otherwise.
	def isMercenary(self, objUnit):

		# Setup the global mercenary pool if it doesn't exist and return immediately
		if(sdEntityExists("Mercenaries Mod","MercenaryData") == False):
			self.setupMercenaryData()
			return false
		
		# Return immediately if the objUnit passed in is not valid
		if(objUnit == None):
			return false
		
		mercenary = self.getMercenary(objUnit.getNameNoDesc())

		return (mercenary != None)		
			

	# Contracts out the unit as a mercenary. This method will also remove the unit
	# from the game and make it unavailable for use by the player until they cancel
	# the unit's contract	
	def contractOutUnit(self, objUnit):

		# Return immediately if an invalid objUnit was passed in.
		if(objUnit == None):
			return

		# Create a blank mercenary
		mercenary = self.createBlankMercenary()

		# Load the unit information into the blank mercenary.
		mercenary.loadUnitData(objUnit)

		self.printMercenaryDataToLog(mercenary)
		
		# If the name isn't set for the unit then get a random name, if it is then
		# we know that they have potentially been a mercenary so use that name instead.
		if(len(objUnit.getNameNoDesc()) == 0):
                        #Rhye - start
			#mercenary.strMercenaryName = MercenaryNameUtils.getRandomMercenaryName()
			mercenary.strMercenaryName = MercenaryNameUtils.getRandomMercenaryName(gc.getGame().getActivePlayer(), objUnit.getUnitType(), True)
                        #Rhye - end
		else:
			mercenary.strMercenaryName = objUnit.getNameNoDesc()
			
		# Fire the mercenary from its current owner
		mercenary.fire()

		# Save the mercenary.
		self.saveMercenary(mercenary)
		
		return mercenary

	
	# Cancels the contract for a unit contracted out by a player and returns them to 
	# the player's civilization
	def cancelContract(self, iPlayer, mercenaryName):

		# Get the mercenary 			
		mercenary = self.getMercenary(mercenaryName)

		
		# Debug code - start
		if(g_bDebug):
			CvUtil.pyPrint("Cancelling the contract for: " + mercenary.getName())
			self.printMercenaryDataToLog(mercenary)
		# Debug code - end
				
		# Return immediately if the mercenary wasn't found
		if(mercenary == None):
			return None

		# Fire the mercenary from their current employeer if they have one					
		if(mercenary.iOwner != -1):
			self.fireMercenary(mercenaryName, mercenary.iOwner)
	
		mercenaries = sdGetVal("Mercenaries Mod", "MercenaryData", AVAILABLE_MERCENARIES)

		# Remove the mercenary from the global mercenary pool
		del mercenaries[mercenaryName]
		sdSetVal("Mercenaries Mod", "MercenaryData", AVAILABLE_MERCENARIES, mercenaries)		
			
		# Get a starting location for the unit
		city = self.getMercenaryStartingLocation(iPlayer)

		# Inform the unit that their contract was cancelled
		mercenary.contractCancelled(iPlayer, city)

		# If we are delaying the units return then save them to the appropriate pool
		if(g_bDelayUnitReturn):
			self.saveMercenary(mercenary)
		
		return mercenary
		
				
	# Returns the list of units contracted out by the player as mercenaries
	def getContractedOutUnits(self, iPlayer):
		
		# Setup the global mercenary pool if it doesn't exist
		if(sdEntityExists("Mercenaries Mod","MercenaryData") == False):
			self.setupMercenaryData()
			return {}
			
		contractedOutUnitsDict = {}
		
		mercenaries = sdGetVal("Mercenaries Mod", "MercenaryData", AVAILABLE_MERCENARIES)
			
		# Go through the list of available mercenaries
		for mercenary in mercenaries.itervalues():

			if(mercenary["iBuilder"] == iPlayer):
				# Create a blank mercenary
				tmpMercenary = self.createBlankMercenary()

				# Load the pseudo mercenary information into the mercenary 
				tmpMercenary.loadData(mercenary)
							
				# Add the mercenary into the contractedOutUnitsDict
				contractedOutUnitsDict[tmpMercenary.getName()] = tmpMercenary
					
	
		mercenaries = sdGetVal("Mercenaries Mod", "MercenaryData", HIRED_MERCENARIES)

		# Go through all of the mercenaries in the global mercenary pools and
		# add the ones built by the iPlayer to the contractedOutUnitsDict
		for playerID in mercenaries.iterkeys():

			# Don't check the iPlayer's mercenaries
			if(playerID == iPlayer):
				continue

			# Get the mercenaries for the player represented by iPlayer
			hiredMercenaries = mercenaries[playerID]

			# Go through the hired mercenaries				
			for mercenary in hiredMercenaries.itervalues():
				if(mercenary["iBuilder"] == iPlayer):
					# Create a blank mercenary
					tmpMercenary = self.createBlankMercenary()

					# Load the pseudo mercenary information into the mercenary 
					tmpMercenary.loadData(mercenary)
								
					# Add the mercenary into the contractedOutUnitsDict
					contractedOutUnitsDict[tmpMercenary.getName()] = tmpMercenary		
		
		# Get the unplaced mercenaries for the player
		mercenaries = self.getUnplacedContractedOutUnits(iPlayer)
		
		# Go through the list of unplaced mercenaries
		for mercenary in mercenaries.itervalues():

			# Add the mercenary into the contractedOutUnitsDict
			contractedOutUnitsDict[mercenary.getName()] = mercenary
		
		return contractedOutUnitsDict
		
		
	# Returns the list of units that are available to contract out as mercenaries
	def getAvailableUnits(self, iPlayer):

		# Get the player
		pyPlayer = PyPlayer(iPlayer)

		# Get the list of units for the player
		unitList = pyPlayer.getUnitList()

		# Return immediately if the player has no units
		if(len(unitList) == 0):
			return {}
			
		availableUnitDict = {}
		
		# Go through the list of units
		for unit in unitList:
			unitInfo = gc.getUnitInfo(unit.getUnitType())
			
			# If we can't contract out the unit then continue
			if(not self.canContractOutUnit(unitInfo)):
				continue

			# Don't allow units that are already mercenaries
			if(self.isMercenary(unit)):
				continue
							
			if(len(unit.getNameNoDesc()) > 0):			
				availableUnitDict[unit.getNameNoDesc() + "-" + str(unit.getID())] = unit
					
			else:
				# Add the unit to the dictionary that will be returned.	
				availableUnitDict[unit.getName() + "-" + str(unit.getID())] = unit
		
		return availableUnitDict
		
		
	# Returns true if the unit with the objUnitInfo can be contracted out as a 
	# mercenary, false otherwise
	def canContractOutUnit(self, objUnitInfo):
			
		# Only allow combat units as mercenaries
		if(objUnitInfo.getCombat() == 0):
			return false

		# Only allow land-based units as mercenaries
		if(objUnitInfo.getDomainType() != gc.getInfoTypeForString("DOMAIN_LAND")):
			return false

		# Don't allow a unit if it has been included in the INI file
		if(g_unitFilterDictionary.has_key(objUnitInfo.getType())):
			return false


                #Rhye - start
		if(objUnitInfo.isAnimal()):
			return false
		if(objUnitInfo.getType() in lForbiddenUnits):
			return false		    
                #Rhye - end

		return true
			
			
	# This method will setup the appropriate datastructures using the SD-Toolkit to maintain
	# the mercenary data.
	def setupMercenaryData(self):
	
		# The dictionary of available mercenaries. The keys will be the name of the mercenary
		# the value will be dictionary representations of Mercenary objects.
		availableMercenaries = {}
		
		# The dictionary of hired mercenaries. The keys will be the player ID and the values
		# will be the dictionaries containing the mercenaries.
		hiredMercenaries = {}
		
		playerList = PyGame.getCivPlayerList()
		
		for player in playerList:
			hiredMercenaries[player.getID()] = {}
		
		# Lets enable the barbarian
		hiredMercenaries[gc.getBARBARIAN_PLAYER()] = {}
		
		# The dictionary of unplaced mercenaries. The keys will be the name of the mercenary
		# the value will be dictionary representations of Mercenary Objects
		unplacedMercenaries = {}
					
		# The dictionary of mercenary groups. The keys will be the name of the mercenary group
		# the value will be MercenaryGroup objects.
		mercenaryGroups = {}
		
		# The dictionary of used mercenary names.
		mercenaryNames = {}
		
		mercenaryData = {
							AVAILABLE_MERCENARIES : availableMercenaries,
							HIRED_MERCENARIES : hiredMercenaries,
							MERCENARY_NAMES: mercenaryNames,
							MERCENARY_GROUPS : mercenaryGroups,
							UNPLACED_MERCENARIES : unplacedMercenaries }
							
		sdEntityInit("Mercenaries Mod", "MercenaryData", mercenaryData)
		
				
##########################
# Mercenary Class		
# By: The Lopez
# This class provides the structure needed to represent mercenaries in the game.

class Mercenary:
	# The name of the mercenary
	strMercenaryName = ""

	# The list of promotions
	promotionList = []
	
	# The cost to hire the mercenary
	iHireCost = -1
	
	# The reference to the mercenary group that the mercenary belongs to
	objMercenaryGroup = None
	
	# The boolean variable indicating if the mercenary is hired by a player or not
	bHired = false
	
	# The reference to the CyUnit object representing the mercenary in the game when hired
	# by a player
	objUnit = None
	
	# The Reference to the CvUnitInfo object representing the mercenary info 
	objUnitInfo = None
	
	# The ID for the CvUnitInfo
	iUnitInfo = -1
	
	# The ID for the player that hired the mercenary
	iOwner = -1

	# The ID for the player that originally built the unit
	iBuilder = -1
	
	# The current experience for the mercenary
	iExperienceLevel = -1
	
	# The amount of experience needed for the next level
	iNextExperienceLevel = -1
	
	# The current level for the mercenary
	iLevel = -1
	
	# The turn the unit was/should be placed in the game
	iPlacementTurn = -1
	
			
	def __init__(self, mercenaryName, objUnitInfo, promotionList, iExperienceLevel, iNextExperienceLevel):
		self.strMercenaryName = mercenaryName
		self.promotionList = promotionList
		
		self.objUnitInfo = objUnitInfo
		if(self.objUnitInfo != None):
			self.iUnitInfo = gc.getInfoTypeForString(self.objUnitInfo.getType())
			
		self.iLevel = len(promotionList)
		self.iExperienceLevel = iExperienceLevel
		self.iNextExperienceLevel = iNextExperienceLevel
		#self.promotionList.append(gc.getPromotionInfo(gc.getInfoTypeForString("PROMOTION_SELFPRESERVATION1")))
		self.promotionList.append(gc.getPromotionInfo(gc.getInfoTypeForString("PROMOTION_MERCENARY")))
		self.iHireCost = self.getHireCost()


	# This method should be used for setting the instance of the Mercenary class
	# with the data from a CyUnit
	def loadUnitData(self, objUnit):

		# Return immediately if the objUnit is not valid
		if(objUnit == None):
			return
	
		self.objUnit = objUnit
	
		self.getCurrentPromotionList()	

		self.getExperienceLevel()

		self.getNextExperienceLevel()

		self.getLevel()

		self.getHireCost()

		self.getOwner()

		self.getUnitInfo()
	
		if(self.iBuilder == -1):
			self.iBuilder = objUnit.getOwner()
		
		if(len(objUnit.getNameNoDesc())>0):
			self.strMercenaryName = objUnit.getNameNoDesc()
		
						
	# This method should be used for setting the instance of the Mercenary class 
	# with the data retrieved using the Sd-Toolkit
	def loadData(self, objDict):
		self.strMercenaryName = objDict["strMercenaryName"]
		
		self.promotionList = []
		
		# Retrieve all of the actual PromotionInfo objects
		
		promotionList = objDict["promotionList"]
		promotionList.sort()
		
		for i in range(len(promotionList)):
			self.promotionList.append(gc.getPromotionInfo(objDict["promotionList"][i]))
			
		self.iHireCost = objDict["iHireCost"]
		
		self.iOwner = objDict["iOwner"]

		# if the owner is set for the mercenary then set the hired flag and get the reference to the
		# unit that represents the mercenary in the game.
		if(self.iOwner != -1):
			self.bHired = true
			
		if(objDict["iUnitID"] != -1):
			self.objUnit = gc.getPlayer(self.iOwner).getUnit(objDict["iUnitID"])
		else:	
			self.objUnit = None

		self.objUnitInfo = gc.getUnitInfo(objDict["iUnitInfo"])

		self.iUnitInfo = objDict["iUnitInfo"]

		self.iExperienceLevel = objDict["iExperienceLevel"]

		self.iNextExperienceLevel = objDict["iNextExperienceLevel"]

		self.iLevel = objDict["iLevel"]
		
		self.iBuilder = objDict["iBuilder"]
	
		self.iPlacementTurn = objDict["iPlacementTurn"]	

		#TO DO: add mercenary group support

		
	# This method builds a dictionary that is used to represent the mercenary in the global mercenary pool.		
	def getDictionaryRepresentation(self):
	
		objDict = {}
		objDict["strMercenaryName"] = self.strMercenaryName

		tmpPromotionList = []
		
		# Add all of the promotions into the tmpPromotionList using their promotion type ID number
		for i in range (len(self.promotionList)):
			if(gc.getInfoTypeForString(self.promotionList[i].getType()) not in tmpPromotionList):
				tmpPromotionList.append(gc.getInfoTypeForString(self.promotionList[i].getType()))
	
		objDict["promotionList"] = tmpPromotionList
				
		objDict["iHireCost"] = self.iHireCost

		objDict["bHired"] = self.bHired

		objDict["iOwner"] = self.iOwner

		if(self.iOwner != -1 and self.objUnit != None):
			objDict["iUnitID"] = self.objUnit.getID()
		else:	
			objDict["iUnitID"] = -1

		objDict["iUnitInfo"] = gc.getInfoTypeForString(self.objUnitInfo.getType())
		
		objDict["iExperienceLevel"] = self.iExperienceLevel

		objDict["iNextExperienceLevel"] = self.iNextExperienceLevel
		
		objDict["iLevel"] = self.iLevel

		objDict["iBuilder"] = self.iBuilder

		objDict["iPlacementTurn"] = self.iPlacementTurn
		
		return objDict
					

	# Returns true if the mercenary is in a group, false otherwise.
	def isInMercenaryGroup(self):
		' true - if the mercenary is in a mercenary group '
		return (self.objMercenaryGroup != None)
		
		
	# Places the mercenary in the city specified by the objCity variable
	def place(self, objCity):
	
		# Return immediately if the mercenary is already in the game
		if(self.objUnit != None):
			return

		# get the player instance
		player = gc.getPlayer(self.iOwner)
		
		# return nothing if the player is an invalid value
		if(player == None):
			player = gc.getPlayer(self.iBuilder)
			if(player == None):
				return
			
		# return nothing if the player is dead
		if(player.isAlive() == false):
			return

		unitType = gc.getInfoTypeForString(self.objUnitInfo.getType())

		# Create the unit and place it in the game		
		self.objUnit = player.initUnit(unitType, objCity.getX(), objCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

		if(g_bDisplayMercenaryMessages):
			strMessage = self.getName() + " has arrived at " + objCity.getName()
			# Inform the player that the mercenary has arrived.
			CyInterface().addMessage(self.iOwner, False, 20, strMessage, "", 0, self.objUnitInfo.getButton(), ColorTypes(0), objCity.getX(), objCity.getY(), True, True) 
			
		# Apply of the promotions to the mercenary in the game
		self.applyPromotions()

		# Set the mercenaries experience
		self.setExperience()		

		# Set the mercenaries unique name
		self.objUnit.setName(self.strMercenaryName)

		# Set the iPlacement turn to -1 so they don't get accidentally placed again.		
		self.iPlacementTurn = -1
	
		# Remove the mercenary identifying trait if the mercenary has a builder
		if(self.iBuilder != -1):
			self.objUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_MERCENARY"), false)
	
	
	# Tells the mercenary that their contract was cancelled and returns them
	# to their builders civilization
	def contractCancelled(self, iPlayer, objCity):

		# get the player instance
		player = gc.getPlayer(iPlayer)
		
		# return nothing if the iPlayer is an invalid value
		if(player == None):
			return
			
		# return nothing if the player is dead
		if(player.isAlive() == false):
			return

		# Set the player as the owner of the mercenary.	
		self.iOwner = -1
		
		# Set the mercenary as not hired
		self.bHired = false
		
		unitType = gc.getInfoTypeForString(self.objUnitInfo.getType())

		# If we are delaying the units return then set the iPlacementTurn
		if(g_bDelayUnitReturn):
			self.iPlacementTurn = (gc.getGame().getGameTurn() + g_iUnitReturnDelayAmount)

		else:
			# Create the unit and place it in the game		
			self.objUnit = player.initUnit(unitType, objCity.getX(), objCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

			# If g_bConsumeMercenaryMovesOnHire is set to true then use up all of the 
			# mercenaries moves, otherwise just select the mercenary.
			if(g_bConsumeUnitMovesOnReturn):
				self.objUnit.finishMoves()
			elif(CyGame().isNetworkMultiPlayer()):
				self.objUnit.finishMoves()
			else:
				CyInterface().selectUnit(self.objUnit, true, false, false)

			if(g_bDisplayMercenaryMessages):
				strMessage = self.getName() + " has arrived at " + objCity.getName()
				# Inform the player that the mercenary has arrived.
				CyInterface().addMessage(self.iOwner, False, 20, strMessage, "", 0, self.objUnitInfo.getButton(), ColorTypes(0), objCity.getX(), objCity.getY(), True, True) 
					
			# Apply of the promotions to the mercenary in the game
			self.applyPromotions()

			# Set the mercenaries experience
			self.setExperience()		

			# Set the mercenaries unique name
			self.objUnit.setName(self.strMercenaryName)
			
			self.objUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_MERCENARY"), false)
			
			self.iPlacementTurn = -1


	# Returns the instance of the mercenary in the game as a CyUnit
	def hire(self, iPlayer, objCity):
		' CyUnit - the instance of the mercenary in the game '

		# get the player instance
		player = gc.getPlayer(iPlayer)
		
		# return nothing if the iPlayer is an invalid value
		if(player == None):
			return
			
		# return nothing if the player is dead
		if(player.isAlive() == false):
			return

		# Set the player as the owner of the mercenary.	
		self.iOwner = iPlayer
		
		# Set the mercenary as hired
		self.bHired = true
		
		unitType = gc.getInfoTypeForString(self.objUnitInfo.getType())

		# If we are delaying the mercenaries placement then set the iPlacementTurn
		if(g_bDelayMercenaryPlacement):
			self.iPlacementTurn = (gc.getGame().getGameTurn() + g_iMercenaryPlacementDelayAmount)
		else:
			# Create the unit and place it in the game		
			self.objUnit = player.initUnit(unitType, objCity.getX(), objCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

			# If g_bConsumeMercenaryMovesOnHire is set to true then use up all of the 
			# mercenaries moves, otherwise just select the mercenary.
			if(g_bConsumeMercenaryMovesOnHire):
				self.objUnit.finishMoves()
			elif(CyGame().isNetworkMultiPlayer()):
				self.objUnit.finishMoves()
			else:
				CyInterface().selectUnit(self.objUnit, true, false, false)

			if(g_bDisplayMercenaryMessages):
				strMessage = self.getName() + " has arrived at " + objCity.getName()
				# Inform the player that the mercenary has arrived.
				CyInterface().addMessage(self.iOwner, False, 20, strMessage, "", 0, self.objUnitInfo.getButton(), ColorTypes(0), objCity.getX(), objCity.getY(), True, True) 
				
			# Apply of the promotions to the mercenary in the game
			self.applyPromotions()

			# Set the mercenaries experience
			self.setExperience()		

			# Set the mercenaries unique name
			self.objUnit.setName(self.strMercenaryName)

			self.iPlacementTurn = -1

		if(g_bDisplayMercenaryMessages and self.iBuilder != -1):
			strMessage = self.getName() + " has been hired by " + gc.getPlayer(self.iOwner).getName()
			# Inform the player that the mercenary has been hired.
			CyInterface().addMessage(self.iBuilder, True, 20, strMessage, "", 0, "", ColorTypes(0), -1, -1, True, True) 
	
		# Subtract cost to hire from player current cash
		if(self.iOwner != self.iBuilder):
                        #Rhye - start Carthaginian UP
			#player.setGold(player.getGold()-self.getHireCost())
			player.setGold(player.getGold()-self.getHireCostXPlayer(iPlayer))
			#Rhye - end Carthaginian UP
		
		if(self.iBuilder != -1 and self.iOwner != self.iBuilder):
                        #Rhye - start Carthaginian UP
			#gc.getPlayer(self.iBuilder).setGold(gc.getPlayer(self.iBuilder).getGold() + self.getHireCost())
			gc.getPlayer(self.iBuilder).setGold(gc.getPlayer(self.iBuilder).getGold() + self.getHireCostXPlayer(iPlayer))
			#Rhye - end Carthaginian UP
			
			
	# Tells the mercenary that the player no longer needs their services and performs the 
	# necessary operations to remove the mercenary from the game and make them available to
	# other players
	def fire(self):
		if(self.objUnit == None):
			CvUtil.pyPrint("We should never reach this point, why did the player have access to this mercenary?")
			return

		# if the mercenary is in a group do not allow the player to fire the mercenary independantly,
		# all for one and one for all, in fact, the mercenary manager should not display the individual
		# mercenaries from groups in the hired mercenary list.
		if(self.objMercenaryGroup != None):
			CvUtil.pyPrint("We should never reach this point, mercenary groups are not implemented!!")
			return

		if(g_bDisplayMercenaryMessages and self.iBuilder != -1 and self.iBuilder != self.iOwner):
			strMessage = self.getName() + " is no longer needed by " + gc.getPlayer(self.iOwner).getName()
			# Inform the player that the mercenary has been fired.
			CyInterface().addMessage(self.iBuilder, True, 20, strMessage, "", 0, "", ColorTypes(0), -1, -1, True, True) 
						
		# Set the mercenaries promotion list before removing the mercenary from the game
		self.promotionList = self.getCurrentPromotionList()
		
		# Set the mercenary's hire cost before removing the mercenary from the game
		self.iHireCost = self.getHireCost()
		
		# Set the mercenary's experience level before removing the mercenary from the game
		self.iExperienceLevel = self.getExperienceLevel()
		
		# Set the mercenary's level before removing the mercenary from the game
		self.iLevel = self.getLevel()
		
		# Set the hired flag to false before removing the mercenary from the game
		self.bHired = false
		
		# Set the mercenaries owner to -1 before removing the mercenary from the game
		self.iOwner = -1
		
		# Remove the unit from the game
		self.objUnit.kill(false,PlayerTypes.NO_PLAYER)
	
		# Make sure that we get rid of the reference to the unit
		self.objUnit = None
		

	# Returns the list of current promotions the mercenary has. If the objUnit is set to
	# a non-None value then the method will rebuild the promotion list and return the
	# promotion list.		
	def getCurrentPromotionList(self):
		' promotionList - the mercenarys current list of promotions '
		
		# If the self.objUnit is actually set then rebuild the self.promotionList from the
		# self.objUnit to get their current promotion list.
		if(self.objUnit != None):
		
			self.promotionList = []			
			
			# Go through each of the promotions defined in the game.
			for i in range(gc.getNumPromotionInfos()):				
				# If the unit has the promotion add it to the promotion list
				if(self.objUnit.isHasPromotion(i)):
					self.promotionList.append(gc.getPromotionInfo(i))

		return self.promotionList


	# Returns the cost to hire the mercenary. If objUnit is non-none then the 
	# iHireCost will be updated
	def getHireCost(self):
		' iHireCost - the cost to hire the mercenary'
		
		modifier = 0
			
		# if the self.objUnitInfo is actually set then get the latest cost to hire the mercenary.
		if(self.objUnitInfo != None):
			self.iHireCost = (self.objUnitInfo.getProductionCost() * (self.getLevel()+1)) + ((self.getLevel()+1) * int(math.fabs(self.getExperienceLevel() - self.getNextExperienceLevel())))
	
		#return int(self.iHireCost*g_dHireCostModifier)
		#return int(self.iHireCost*g_dHireCostModifier) + g_dBaseHireCost #Rhye	
		return int(self.iHireCost*g_dHireCostModifier) + g_dBaseHireCost*gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getTrainPercent()/100; #edead: speed scaling

	# The cost returned by this method should fluctuate up as the mercenary gains experience
	# levels and promotions.

        #Rhye - start Carthaginian UP
	def getHireCostXPlayer(self, iPlayer):
		' iHireCost - the cost to hire the mercenary'
		
		modifier = 0
			
		# if the self.objUnitInfo is actually set then get the latest cost to hire the mercenary.
		if(self.objUnitInfo != None):
			self.iHireCost = (self.objUnitInfo.getProductionCost() * (self.getLevel()+1)) + ((self.getLevel()+1) * int(math.fabs(self.getExperienceLevel() - self.getNextExperienceLevel())))
	
		#return int(self.iHireCost*g_dHireCostModifier)
		iResult = int(self.iHireCost*g_dHireCostModifier) + g_dBaseHireCost #Rhye
		# Leoreth - removed Carthaginian UP
		return iResult	
        #Rhye - end Carthaginian UP


        #Rhye - start continents
	def canHireUnit(self, iPlayer):
                #return True
                #teamPlayer = gc.getTeam(gc.getPlayer(iPlayer).getTeam())
                #for iLoopGroup in range (len(con.lCivGroups)):
                #        if (iPlayer in con.lCivGroups[iLoopGroup]):
                #                for iLoopCiv in range (con.iNumMajorPlayers):
                #                        bValid = False
                #                        if (iLoopCiv in con.lCivGroups[iLoopGroup]):
                #                                bValid = True
                #                        else:
                #                                if (teamPlayer.canContact(iLoopCiv)):
                #                                        if (iPlayer in con.lCivBioOldWorld):
                #                                                if (iLoopCiv in con.lCivBioOldWorld):
                #                                                        bValid = True
                #                                        elif (iPlayer in con.lCivBioNewWorld):
                #                                                if (iLoopCiv in con.lCivBioOldWorld):
                #                                                        apCityList = PyPlayer(iLoopCiv).getCityList()
                #                                                        for pCity in apCityList:
                #                                                                if (pCity.GetCy().getX() <= 43): #beginning of Americas
                #                                                                        if (gc.getGame().getGameTurn() >= pCity.GetCy().getGameTurnFounded() + 15):
                #                                                                                bValid = True
                ##                        if (bValid):
                #                                apCityList = PyPlayer(iLoopCiv).getCityList()
                #                                for pCity in apCityList:			
                #                                        if (pCity.GetCy().canTrain(self.getUnitInfoID(),False,False) or (iPlayer in con.lCivBioOldWorld and self.getUnitInfoID() == con.iHolyRomanLandsknecht and pCity.GetCy().canTrain(con.iPikeman,False,False))):
                #                                                #print ("city true", pCity.GetCy().getName(),self.getUnitInfoID())
                #                                                return True
		
		# Leoreth: special treatment for new world and unique units, similar to SoI
		
		unitType = self.getUnitInfoID()
		iStateReligion = gc.getPlayer(iPlayer).getStateReligion()
		bNewWorldDiscovered = (sd.scriptDict['lNewWorld'][0] != -1)
		
		regionList = []
		cityList = PyPlayer(iPlayer).getCityList()
		for pCity in cityList:
			city = pCity.GetCy()
			regionList.append(city.getRegionID())
			
		bNewWorldOnly = True
		for iRegion in regionList:
			if iRegion not in con.mercRegions[con.iArea_SouthAmerica] or iRegion not in con.mercRegions[con.iArea_NorthAmerica]:
				bNewWorldOnly = False
				
		if bNewWorldOnly and not bNewWorldDiscovered:
			if not gc.getPlayer(iPlayer).canTrain(unitType, False, False):
				return False
				
		if unitType == con.iIncanQuechua:
			return con.rPeru in regionList or (gc.getPlayer(iPlayer).canContact(con.iInca) and (bNewWorldOnly or bNewWorldDiscovered))
		elif unitType == con.iAztecJaguar:
			return con.rMesoamerica in regionList or (gc.getPlayer(iPlayer).canContact(con.iAztecs) and (bNewWorldOnly or bNewWorldDiscovered))
		elif unitType == con.iMayaHolkan:
			return con.rMesoamerica in regionList or (gc.getPlayer(iPlayer).canContact(con.iMaya) and (bNewWorldOnly or bNewWorldDiscovered))
			
		elif unitType in [con.iCelticGallicWarrior, con.iVikingBerserker, con.iHolyRomanLandsknecht, con.iFrenchMusketeer]:
			return set(regionList) & con.mercRegions[con.iArea_Europe]
		elif unitType == con.iRomePraetorian:
			return (gc.getPlayer(con.iRome).isAlive() or gc.getPlayer(con.iByzantium).isAlive()) and (set(regionList) & con.mercRegions[con.iArea_Europe] or con.rAnatolia in regionList)
		elif unitType == con.iGreekPhalanx:
			return gc.getPlayer(con.iGreece).isAlive() and set(regionList) & con.mercRegions[con.iArea_Europe]
		elif unitType in [con.iSumerianVulture, con.iBabylonBowman]:
			return gc.getPlayer(con.iBabylonia).isAlive() and con.rMesopotamia in regionList
		elif unitType == con.iNativeAmericaDogSoldier:
			return set(regionList) & con.mercRegions[con.iArea_NorthAmerica]
		elif unitType in [con.iJapanSamurai, con.iChinaChokonu, con.iThaiChangSuek, con.iKhmerBallistaElephant]:
			return set(regionList) & con.mercRegions[con.iArea_EastAsia]
		elif unitType in [con.iIranianQizilbash, con.iOttomanJanissary, con.iArabiaCamelarcher, con.iSeljukGhulamWarrior]:
			return iStateReligion == con.iIslam and set(regionList) & con.mercRegions[con.iArea_MiddleEast]
		elif unitType in [con.iZuluImpi, con.iEthiopianOromoWarrior, con.iMaliSkirmisher]:
			return set(regionList) & con.mercRegions[con.iArea_Africa]
		elif unitType == con.iEgyptWarChariot:
			return gc.getPlayer(con.iEgypt).isAlive() and (con.rEgypt in regionList or con.rMesopotamia in regionList or con.rMaghreb in regionList)
		elif unitType == con.iPersiaImmortal:
			return gc.getPlayer(con.iPersia).isAlive() and set(regionList) & con.mercRegions[con.iArea_MiddleEast]
		elif unitType == con.iCarthageNumidianCavalry:
			return con.rMaghreb in regionList or con.rEgypt in regionList
		elif unitType == con.iMongolKeshik:
			return gc.getPlayer(con.iMongolia).isAlive()
		elif unitType == con.iByzantineCataphract:
			return iStateReligion in [con.iCatholicism, con.iOrthodoxy] and (set(regionList) & con.mercRegions[con.iArea_Europe] or con.rAnatolia in regionList)
		elif unitType == con.iSpanishConquistador:
			return iStateReligion == con.iCatholicism and bNewWorldDiscovered
		elif unitType == con.iRussiaCossack:
			return con.rRussia in regionList or con.rSiberia in regionList
		elif unitType == con.iMughalSiegeElephant:
			return set(regionList) & con.mercRegions[con.iArea_India]
		elif unitType == con.iWarElephant:
			return gc.getPlayer(iPlayer).getCurrentEra() <= con.iClassical or set(regionList) & con.mercRegions[con.iArea_MiddleEast] or set(regionList) & con.mercRegions[con.iArea_EastAsia] or set(regionList) & con.mercRegions[con.iArea_Africa]
			
		elif unitType in [con.iEnglishRedcoat, con.iAmericanNavySeal, con.iFrenchHeavyCannon, con.iGermanPanzer, con.iKoreanHwacha, con.iThaiChangSuek]:
			return False
		
                return True
        #Rhye - end
	
	def getMercenaryMaintenanceCost(self):
		' iMaintenanceCost - the cost to maintain the mercenary'

                #dMaintenanceCostModifier = g_dMaintenanceCostModifier + (float(gc.getActivePlayer().getCurrentEra())/20) #Rhye
                dMaintenanceCostModifier = g_dMaintenanceCostModifier + (float(gc.getActivePlayer().getCurrentEra())/30) #Rhye
                #print (dMaintenanceCostModifier) #Rhye

		# Let the mercenary value be at least the their level times pi, common let the mercenary have his share
		# of the pi
		#return int((math.ceil(self.getLevel() * math.pi) + math.ceil(self.getHireCost() * 0.05))*g_dMaintenanceCostModifier) #Rhye
		return int((math.ceil(self.getLevel() * 3) + math.ceil(self.getHireCost() * 0.05))*dMaintenanceCostModifier) + g_dBaseMaintenanceCost #Rhye
				

        #Rhye - start Carthaginian UP
	def getMercenaryMaintenanceCostXPlayer(self, iPlayer):
		' iMaintenanceCost - the cost to maintain the mercenary'

                #dMaintenanceCostModifier = g_dMaintenanceCostModifier + (float(gc.getActivePlayer().getCurrentEra())/20) #Rhye
                dMaintenanceCostModifier = g_dMaintenanceCostModifier + (float(gc.getActivePlayer().getCurrentEra())/30) #Rhye
                #print (dMaintenanceCostModifier) #Rhye

		# Let the mercenary value be at least the their level times pi, common let the mercenary have his share
		# of the pi
		#return int((math.ceil(self.getLevel() * math.pi) + math.ceil(self.getHireCost() * 0.05))*g_dMaintenanceCostModifier)
		#iResult = int((math.ceil(self.getLevel() * math.pi) + math.ceil(self.getHireCost() * 0.05))*dMaintenanceCostModifier) + g_dBaseMaintenanceCost #Rhye
		iResult = int((math.ceil(self.getLevel() * 3) + math.ceil(self.getHireCostXPlayer(iPlayer) * 0.05))*dMaintenanceCostModifier) + g_dBaseMaintenanceCost #Rhye
		# Leoreth - removed Carthaginian UP
		return iResult
        #Rhye - end Carthaginian UP


				
	# Returns true if the mercenary is already hired by a player, false otherwise.
	def isHired(self):
		' True - if the mercenary is hired by a player '

		# if the self.objUnit is actually set then set the hired flag and get the reference to the
		# unit that represents the mercenary in the game.		
		if(self.objUnit != None and self.objUnit.getOwner() != self.iBuilder):
			self.bHired = true
			self.iOwner = self.objUnit.getOwner()
		elif(self.iOwner != -1 and self.iOwner != self.iBuilder):
			self.bHired = true
		else:
			self.bHired = false
			self.iOwner = -1
			
		return self.bHired
		

	# Returns true if the mercenary is placed in the game, false otherwise
	def isPlaced(self):
		return (self.iPlacementTurn == -1)

	
	# Returns the number of turns until the mercenary is placed in the game or
	# it will return -1 if the mercenary is already placed in the game.	
	def getPlacementTurns(self):

		# Return -1 immediately if the mercenary is already in the game
		if(self.objUnit != None):
			return -1

		return (self.iPlacementTurn - gc.getGame().getGameTurn()) 


	# Returns the mercenary's current experience level. If objUnit is non-none then the 
	# iExperienceLevel will be updated		
	def getExperienceLevel(self):
		' iExperience - the current mercenary experience level'
		
		# if the self.objUnit is actually set then get the mercenary's current experience level		
		if(self.objUnit != None):
			self.iExperienceLevel = self.objUnit.getExperience()
			
		return self.iExperienceLevel
		

	# Returns the mercenary's next experience level. If objUnit is non-none then the 
	# iNextExperienceLevel will be updated		
	def getNextExperienceLevel(self):
		' iNextExperienceLevel - the next mercenary experience level'
		
		# if the self.objUnit is actually set then get the mercenary's experience required to 
		# get to the next level
		if(self.objUnit != None):
			self.iNextExperienceLevel = self.objUnit.experienceNeeded()
			
		return self.iNextExperienceLevel		
		
		
	# Returns the mercenary's current level. If objUnit is non-none then the 
	# iLevel will be updated		
	def getLevel(self):
		' iLevel - the current mercenarys level'
		
		# if the self.objUnit is actually set then get the mercenary's current level
		if(self.objUnit != None):
			self.iLevel = self.objUnit.getLevel()
			
		return self.iLevel
		
		
	# Returns the mercenary's current owner ID. If objUnit is non-none then the 
	# iOwner and bHired will be updated				
	def getOwner(self):
		' iOwner - the iPlayer value of the owner of the mercenary'

		# if the self.objUnit is actually set then set the hired flag and get the reference to the
		# unit that represents the mercenary in the game.		
		if(self.objUnit != None):
			self.bHired = true
			self.iOwner = self.objUnit.getOwner()
		elif(self.iPlacementTurn != -1):
			self.bHired = true
		else:
			self.bHired = false
			self.iOwner = -1
	
		return self.iOwner
	

	# Applies the promotions from the promotionList to the mercenary represent by objUnit 
	def applyPromotions(self):

		# Return immediately if the self.objUnit is not set.
		if(self.objUnit == None):
			return
					
		for i in range(len(self.promotionList)):
			self.objUnit.setHasPromotion(gc.getInfoTypeForString(self.promotionList[i].getType()),true)
		
		# Give the mercenary the new mercenary promotion "Self Preservation"
		self.objUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_MERCENARY"),true)
	
	
	# This method will set the initial the mercenary experience and level
	def setExperience(self):

		# Return immediately if the self.objUnit is not set.
		if(self.objUnit == None):
			return

		#level = self.iLevel - 1
		
		#if(level < 0):
		#	level = 0
			
		#self.objUnit.setLevel(level)
		
		#experienceNeeded = self.objUnit.experienceNeeded()
		
		self.objUnit.setLevel(self.iLevel)
		
		# FIX: 03/07/06 - setExperience does not work as expected if you pass in the experience points
		# you want and the number of experience points for the next level. Instead we need to pass in
		# the experience points you want as the value for both parameters.
		#self.objUnit.setExperience(self.iExperienceLevel,self.iNextExperienceLevel)	
		self.objUnit.setExperience(self.iExperienceLevel,self.iExperienceLevel)	


	# Returns the mercenary's name		
	def getName(self):
		return self.strMercenaryName


	# Sets the name for the mercenary
	def setName(self, strMercenaryName):

		# Return immediately if the name passed in is not set	
		if(strMercenaryName == None):
			return

		# Return immediately if the name passed in has a length of 0
		if(len(strMercenaryName) == 0):
			return
			
		self.strMercenaryName = strMercenaryName

		
	# Returns the mercenary's UnitInfo object		
	def getUnitInfo(self):
		
		if(self.objUnitInfo == None and self.objUnit != None):
			self.iUnitInfo = self.objUnit.getUnitType()
			self.objUnitInfo = gc.getUnitInfo(self.iUnitInfo)
			
		# Set the self.iUnitInfo if it hasn't been set and the self.objUnit is set.
		elif(self.iUnitInfo == -1 and self.objUnit != None):
			self.iUnitInfo = self.objUnit.getUnitType()
			
		# Set the self.iUnitInfo if it hasn't been set and the self.objUnitInfo is set.
		elif(self.iUnitInfo == -1 and self.objUnitInfo != None):
			self.iUnitInfo = gc.getInfoTypeForString(self.objUnitInfo.getType())

		return self.objUnitInfo
	
	
	# Returns the UnitInfoID for the mercenary					
	def getUnitInfoID(self):
	
		# Set the self.iUnitInfo if it hasn't been set and the self.objUnit is set.
		if(self.iUnitInfo == -1 and self.objUnit != None):
			self.iUnitInfo = self.objUnit.getUnitType()

		# Set the self.iUnitInfo if it hasn't been set and the self.objUnitInfo is set.
		elif(self.iUnitInfo == -1 and self.objUnitInfo != None):
			self.iUnitInfo = gc.getInfoTypeForString(self.objUnitInfo.getType())
		#print ("self.iUnitInfo", self.iUnitInfo)
			
		return self.iUnitInfo

		
	# Returns the builder ID of the mercenary
	def getBuilder(self):
		return self.iBuilder
	
	
# TO DO: Remove before initial release, but retain in dev copy to finish implementation for mercenary groups feature	
class MercenaryGroup:
	
	# The name of the mercenary group
	strMercenaryGroupName = ""
	
	# The list of mercenaries belonging to the mercenary group
	listMercenaries = []


