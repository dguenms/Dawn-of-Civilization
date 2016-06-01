# Rhye's and Fall of Civilization - Utilities

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import Popup
import Consts as con
#import cPickle as pickle
from StoredData import sd
import BugCore
import Areas
import SettlerMaps
import WarMaps
import CvScreenEnums


# globals
MainOpt = BugCore.game.MainInterface
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

iNumPlayers = con.iNumPlayers
iNumMajorPlayers = con.iNumMajorPlayers
iNumActivePlayers = con.iNumActivePlayers
iIndependent = con.iIndependent
iIndependent2 = con.iIndependent2
iNumTotalPlayers = con.iNumTotalPlayers
iBarbarian = con.iBarbarian

iSettler = con.iSettler

iNumBuildingsPlague = con.iNumBuildingsPlague

tCol = (
'255,255,255',
'200,200,200',
'150,150,150',
'128,128,128')

lChineseCities = [(102, 47), (103, 44), (103, 43), (106, 44), (107, 43), (105, 39), (104, 39)]
# Beijing, Kaifeng, Luoyang, Shanghai, Hangzhou, Guangzhou, Haojing

class RFCUtils:
	bStabilityOverlay = False

	#Rise and fall, stability
	def getLastTurnAlive( self, iCiv ):
		return sd.scriptDict['lLastTurnAlive'][iCiv]

	def setLastTurnAlive( self, iCiv, iNewValue ):
		sd.scriptDict['lLastTurnAlive'][iCiv] = iNewValue

	def getCivsWithNationalism( self ):
		return sd.scriptDict['iCivsWithNationalism']

	#Victory
	def getGoal( self, i, j ):
		return sd.scriptDict['lGoals'][i][j]

	def setGoal( self, i, j, iNewValue ):
		sd.scriptDict['lGoals'][i][j] = iNewValue

	#Stability
	
	def getTempFlippingCity( self ):
		return sd.scriptDict['tempFlippingCity']

	def setTempFlippingCity( self, tNewValue ):
		sd.scriptDict['tempFlippingCity'] = tNewValue
		
	#Plague
	def getPlagueCountdown( self, iCiv ):
		return sd.scriptDict['lPlagueCountdown'][iCiv]

	def setPlagueCountdown( self, iCiv, iNewValue ):
		sd.scriptDict['lPlagueCountdown'][iCiv] = iNewValue

	#Communications
	def getSeed( self ):
		return sd.scriptDict['iSeed']
		
	def setTempEventList( self, lTempEventList ):
		sd.scriptDict['lTempEventList'] = lTempEventList
		
	def getTempEventList( self ):
		return sd.scriptDict['lTempEventList']
		
	def setPlayerEnabled(self, iCiv, bNewValue):
		sd.scriptDict['lPlayerEnabled'][con.lSecondaryCivs.index(iCiv)] = bNewValue
		
	def getPlayerEnabled(self, iCiv):
		return sd.scriptDict['lPlayerEnabled'][con.lSecondaryCivs.index(iCiv)]

#######################################
			    
	#Victory
	def countAchievedGoals(self, iPlayer):
		iResult = 0
		for j in range(3):			
			#iTemp = self.getGoal(iPlayer, j)
			#if (iTemp < 0):
			#	iTemp = 0
			#iResult += iTemp
			if (self.getGoal(iPlayer, j) == 1):
				iResult += 1
		return iResult
		
	def getGoalsColor(self, iPlayer): #by CyberChrist
		iCol = 0
		for j in range(3):
			if (self.getGoal(iPlayer, j) == 0):
				iCol += 1
		return tCol[iCol]

	    
	#Plague
	def getRandomCity(self, iPlayer):
		cityList = []
		apCityList = PyPlayer(iPlayer).getCityList()
		for pCity in apCityList:
			cityList.append(pCity.GetCy())
		if (len(cityList)):	   
			return cityList[gc.getGame().getSorenRandNum(len(cityList), 'random city')]
		else:
			return -1

	# Leoreth - finds an adjacent land plot without enemy units that's closest to the player's capital (for the Roman UP)
	def findNearestLandPlot(self, tPlot, iPlayer):
		x, y = tPlot
		plotList = []

		for i in range(x - 1, x + 2):	
			for j in range(y - 1, y + 2):	
				pCurrent = gc.getMap().plot( i, j )
				if (not pCurrent.isWater() and not pCurrent.isPeak()):
					if ( not pCurrent.isUnit() ):
						plotList.append(pCurrent)

		#if (len(plotList) > 0):
		#	iDistance = 1000
		#	pCapital = gc.getPlayer(iPlayer).getCapitalCity()
		#	iCapX = pCapital.getX()
		#	iCapY = pCapital.getY()
		#	for plot in plotList:
		#		plotX = plot.getX()
		#		plotY = plot.getY()
		#		iTempDist = self.calculateDistance(iCapX, plotX, iCapY, plotY)
#
		#		if iTempDist < iDistance:
		#			nearestPlot = plot
		#			iDistance = iTempDist

		#	return nearestPlot

		#return (None)

		if (len(plotList) > 0):
			rndNum = gc.getGame().getSorenRandNum(len(plotList), 'land plot')
			result = plotList[rndNum]
			if (result):							
				return ((result.getX(), result.getY()))
		# if no plot is found, return that player's capital
		return Areas.getCapital(iPlayer)



	def isMortalUnit(self, unit):
		if unit.getUpgradeDiscount() >= 100: return False
		
		if gc.getUnitInfo(unit.getUnitType()).isMechUnit(): return False
		
		if not unit.canFight(): return False
		
		return True

	def isDefenderUnit(self, unit):
		iUnitType = unit.getUnitType()
		if (iUnitType >= con.iSpearman and iUnitType <= con.iChineseChokonu):
			return True
		return False

	#AIWars
	def checkUnitsInEnemyTerritory(self, iCiv1, iCiv2): 
		unitList = PyPlayer(iCiv1).getUnitList()
		if(len(unitList)):
			for unit in unitList:
				iX = unit.getX()
				iY = unit.getY()
				if (gc.getMap().plot( iX, iY ).getOwner() == iCiv2):
					return True
		return False

	#AIWars
	def restorePeaceAI(self, iMinorCiv, bOpenBorders):
		teamMinor = gc.getTeam(gc.getPlayer(iMinorCiv).getTeam())
		for iActiveCiv in range( iNumActivePlayers ):
			if (gc.getPlayer(iActiveCiv).isAlive() and not gc.getPlayer(iActiveCiv).isHuman()):
				if (teamMinor.isAtWar(iActiveCiv)):
					bActiveUnitsInIndependentTerritory = self.checkUnitsInEnemyTerritory(iActiveCiv, iMinorCiv)
					bIndependentUnitsInActiveTerritory = self.checkUnitsInEnemyTerritory(iMinorCiv, iActiveCiv)								  
					if (not bActiveUnitsInIndependentTerritory and not bIndependentUnitsInActiveTerritory):	    
						teamMinor.makePeace(iActiveCiv)
						if (bOpenBorders):
							teamMinor.signOpenBorders(iActiveCiv)
	#AIWars
	def restorePeaceHuman(self, iMinorCiv, bOpenBorders): 
		teamMinor = gc.getTeam(gc.getPlayer(iMinorCiv).getTeam())
		for iActiveCiv in range( iNumActivePlayers ):
			if (gc.getPlayer(iActiveCiv).isHuman()):
				if (gc.getPlayer(iActiveCiv).isAlive()):
					if (teamMinor.isAtWar(iActiveCiv)):
						bActiveUnitsInIndependentTerritory = self.checkUnitsInEnemyTerritory(iActiveCiv, iMinorCiv)
						bIndependentUnitsInActiveTerritory = self.checkUnitsInEnemyTerritory(iMinorCiv, iActiveCiv)								  
						if (not bActiveUnitsInIndependentTerritory and not bIndependentUnitsInActiveTerritory):	    
							teamMinor.makePeace(iActiveCiv)
				return
	#AIWars
	def minorWars(self, iMinorCiv):
		teamMinor = gc.getTeam(gc.getPlayer(iMinorCiv).getTeam())
		apCityList = PyPlayer(iMinorCiv).getCityList()
		for pCity in apCityList:
			city = pCity.GetCy()
			x = city.getX()
			y = city.getY()
			for iActiveCiv in range( iNumActivePlayers ):
				if (gc.getPlayer(iActiveCiv).isAlive() and not gc.getPlayer(iActiveCiv).isHuman()):
					if (gc.getPlayer(iActiveCiv).getSettlerValue(x, y) >= 90 or gc.getPlayer(iActiveCiv).getWarValue(x, y) >= 6):
						if (not teamMinor.isAtWar(iActiveCiv)):
							teamMinor.declareWar(iActiveCiv, False, WarPlanTypes.WARPLAN_LIMITED)
							print ("Minor war", city.getName(), gc.getPlayer(iActiveCiv).getCivilizationAdjective(0))



	    
	#RiseAndFall, Stability
	def calculateDistance(self, x1, y1, x2, y2):
		dx = abs(x2-x1)
		dy = abs(y2-y1)
		return max(dx, dy)

	def calculateDistanceTuples(self, t1, t2):
		return self.calculateDistance(t1[0], t1[1], t2[0], t2[1])

	    
	#RiseAndFall
	def debugTextPopup(self, strText):
		if MainOpt.isShowDebugPopups():
			self.show(strText)

	def show(self, message):
		popup = Popup.PyPopup()
		popup.setBodyString(message)
		popup.launch()

	def popup(self, title, message, labels):
		popup = Popup.PyPopup()
		popup.setHeaderString(title)
		popup.setBodyString(message)
		for i in labels:
		    popup.addButton( i )
		popup.launch(len(labels) == 0)

	#RiseAndFall
	def updateMinorTechs( self, iMinorCiv, iMajorCiv):		
		for t in range(con.iNumTechs):
			if (gc.getTeam(gc.getPlayer(iMajorCiv).getTeam()).isHasTech(t)):
				    gc.getTeam(gc.getPlayer(iMinorCiv).getTeam()).setHasTech(t, True, iMinorCiv, False, False)


	#RiseAndFall, Religions, Congresses, UniquePowers
	def makeUnit(self, iUnit, iPlayer, tCoords, iNum, sAdj="", iExp = 0): #by LOQ
		'Makes iNum units for player iPlayer of the type iUnit at tCoords.'
		for i in range(iNum):
			player = gc.getPlayer(iPlayer)
			unit = player.initUnit(iUnit, tCoords[0], tCoords[1], UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			if sAdj != "":
				unit.setName(CyTranslator().getText(sAdj, ()) + ' ' + unit.getName())
			if iExp > 0:
				unit.changeExperience(iExp, 100, False, False, False)
				
		#return unit

	def makeUnitAI(self, iUnit, iPlayer, tCoords, iAI, iNum, sAdj=""): #by LOQ, modified by Leoreth
		'Makes iNum units for player iPlayer of the type iUnit at tCoords.'
		for i in range(iNum):
			player = gc.getPlayer(iPlayer)
			unit = player.initUnit(iUnit, tCoords[0], tCoords[1], iAI, DirectionTypes.DIRECTION_SOUTH)
			if sAdj != "":
				unit.setName(CyTranslator().getText(sAdj, ()) + ' ' + unit.getName())
				

	#RiseAndFall, Religions, Congresses
	def getHumanID(self):
##		for iCiv in range(iNumPlayers):
##			if (gc.getPlayer(iCiv).isHuman()):
##				return iCiv     
		return gc.getGame().getActivePlayer()



	#RiseAndFall
	def flipUnitsInCityBefore(self, tCityPlot, iNewOwner, iOldOwner):
		#print ("tCityPlot Before", tCityPlot)
		plotCity = gc.getMap().plot(tCityPlot[0], tCityPlot[1])
		city = plotCity.getPlotCity()    
		iNumUnitsInAPlot = plotCity.getNumUnits()
		j = 0
		for i in range(iNumUnitsInAPlot):			
			unit = plotCity.getUnit(j)
			unitType = unit.getUnitType()
			if (unit.getOwner() == iOldOwner):
				unit.kill(False, con.iBarbarian)
				if (iNewOwner < con.iNumActivePlayers or unitType > con.iSettler):
					self.makeUnit(unitType, iNewOwner, [0, 67], 1)
			else:
				j += 1
	#RiseAndFall
	def flipUnitsInCityAfter(self, tCityPlot, iCiv):
		#moves new units back in their place
		print ("tCityPlot After", tCityPlot)
		tempPlot = gc.getMap().plot(0,67)
		if (tempPlot.getNumUnits() != 0):
			iNumUnitsInAPlot = tempPlot.getNumUnits()
			#print ("iNumUnitsInAPlot", iNumUnitsInAPlot)			
			for i in range(iNumUnitsInAPlot):
				unit = tempPlot.getUnit(0)
				unit.setXYOld(tCityPlot[0],tCityPlot[1])
		#cover plots revealed
		gc.getMap().plot(0, 67).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(0, 66).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(1, 66).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(1, 67).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(123, 67).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(123, 66).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(2, 67).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(2, 66).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(2, 65).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(1, 65).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(0, 65).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(122, 67).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(122, 66).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(122, 65).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(123, 65).setRevealed(iCiv, False, True, -1);

	def killUnitsInArea(self, iPlayer, lPlots):
		for (x, y) in lPlots:
			lUnits = []
			plot = gc.getMap().plot(x, y)
			iNumUnits = plot.getNumUnits()
			if iNumUnits > 0:
				for i in range(iNumUnits):
					unit = plot.getUnit(i)
					if unit.getOwner() == iPlayer:
						lUnits.append(unit)
			for unit in lUnits:
				unit.kill(False, con.iBarbarian)
							
	#RiseAndFall
	def flipUnitsInArea(self, lPlots, iNewOwner, iOldOwner, bSkipPlotCity, bKillSettlers):
		"""Deletes, recreates units in 0,67 and moves them to the previous tile.
		If there are units belonging to others in that plot and the new owner is barbarian, the units aren't recreated.
		Settlers aren't created.
		If bSkipPlotCity is True, units in a city won't flip. This is to avoid converting barbarian units that would capture a city before the flip delay"""
		for (x, y) in lPlots:
			killPlot = gc.getMap().plot(x,y)
			iNumUnitsInAPlot = killPlot.getNumUnits()
			if (iNumUnitsInAPlot):
				bRevealedZero = False
				if (gc.getMap().plot(0, 67).isRevealed(iNewOwner, False)):
					bRevealedZero = True
				#print ("killplot", x, y)
				if (bSkipPlotCity == True) and (killPlot.isCity()):
					#print (killPlot.isCity())
					#print 'do nothing'
					pass
				else:
					j = 0
					oldCapital = gc.getPlayer(iOldOwner).getCapitalCity()
					for i in range(iNumUnitsInAPlot):							
						unit = killPlot.getUnit(j)
						#print ("killplot", x, y, unit.getUnitType(), unit.getOwner(), "j", j)
						if (unit.getOwner() == iOldOwner):
							# Leoreth: Italy shouldn't flip so it doesn't get too strong by absorbing French or German armies attacking Rome
							if iNewOwner == con.iItaly and iOldOwner < con.iNumPlayers:
								unit.setXYOld(oldCapital.getX(), oldCapital.getY())
							else:
								unit.kill(False, con.iBarbarian)
								
								# Leoreth: can't flip naval units anymore
								if unit.getDomainType() == DomainTypes.DOMAIN_SEA:
									continue
									
								# Leoreth: ignore workers as well
								if unit.getUnitType() in [con.iWorker, con.iIndianPunjabiWorker, con.iBrazilianMadeireiro]:
									continue
								
								if not (unit.isFound() and not bKillSettlers) and not unit.isAnimal():
									self.makeUnit(unit.getUnitType(), iNewOwner, [0, 67], 1)
						else:
							j += 1
					tempPlot = gc.getMap().plot(0,67)
					#moves new units back in their place
					if (tempPlot.getNumUnits() != 0):
						iNumUnitsInAPlot = tempPlot.getNumUnits()
						for i in range(iNumUnitsInAPlot):
							unit = tempPlot.getUnit(0)
							unit.setXYOld(x,y)
						iCiv = iNewOwner
						if (bRevealedZero == False):
							gc.getMap().plot(0, 67).setRevealed(iCiv, False, True, -1);
							gc.getMap().plot(0, 66).setRevealed(iCiv, False, True, -1);
							gc.getMap().plot(1, 66).setRevealed(iCiv, False, True, -1);
							gc.getMap().plot(1, 67).setRevealed(iCiv, False, True, -1);
							gc.getMap().plot(123, 67).setRevealed(iCiv, False, True, -1);
							gc.getMap().plot(123, 66).setRevealed(iCiv, False, True, -1);
							gc.getMap().plot(2, 67).setRevealed(iCiv, False, True, -1);
							gc.getMap().plot(2, 66).setRevealed(iCiv, False, True, -1);
							gc.getMap().plot(2, 65).setRevealed(iCiv, False, True, -1);
							gc.getMap().plot(1, 65).setRevealed(iCiv, False, True, -1);
							gc.getMap().plot(0, 65).setRevealed(iCiv, False, True, -1);
							gc.getMap().plot(122, 67).setRevealed(iCiv, False, True, -1);
							gc.getMap().plot(122, 66).setRevealed(iCiv, False, True, -1);
							gc.getMap().plot(122, 65).setRevealed(iCiv, False, True, -1);
							gc.getMap().plot(123, 65).setRevealed(iCiv, False, True, -1);
			




	#Congresses, RiseAndFall
	def flipCity(self, tCityPlot, bFlipType, bKillUnits, iNewOwner, iOldOwners):
		"""Changes owner of city specified by tCityPlot.
		bFlipType specifies if it's conquered or traded.
		If bKillUnits != 0 all the units in the city will be killed.
		iRetainCulture will determine the split of the current culture between old and new owner. -1 will skip
		iOldOwners is a list. Flip happens only if the old owner is in the list.
		An empty list will cause the flip to always happen."""
		pNewOwner = gc.getPlayer(iNewOwner)
		city = gc.getMap().plot(tCityPlot[0], tCityPlot[1]).getPlotCity()
		if (gc.getMap().plot(tCityPlot[0], tCityPlot[1]).isCity()):
			if not city.isNone():
				iOldOwner = city.getOwner()
				if (iOldOwner in iOldOwners or not iOldOwners):

					if (bKillUnits):
						killPlot = gc.getMap().plot( tCityPlot[0], tCityPlot[1] )
						for i in range(killPlot.getNumUnits()):
							unit = killPlot.getUnit(0)
							unit.kill(False, iNewOwner)
							
					if (bFlipType): #conquest
						if (city.getPopulation() == 2):
							city.setPopulation(3)
						if (city.getPopulation() == 1):
							city.setPopulation(2)
						pNewOwner.acquireCity(city, True, False)
					else: #trade
						pNewOwner.acquireCity(city, False, True)
						
					# Leoreth: reset unhappiness timers
					#iHurryAngerTime = city.getHurryAngerTimer()
					#iConscriptAngerTime = city.getConscriptAngerTimer()
					
					#if iHurryAngerTime > 0:
					#	city.changeHurryAngerTimer(-iHurryAngerTime)
						
					#if iConscriptAngerTime > 0:
					#	city.changeConscriptAngerTimer(-iConscriptAngerTime)
					
					city.setInfoDirty(True)
					city.setLayoutDirty(True)
						
					return True
		return False


	#Congresses, RiseAndFall
	def cultureManager(self, tCityPlot, iCulturePercent, iNewOwner, iOldOwner, bBarbarian2x2Decay, bBarbarian2x2Conversion, bAlwaysOwnPlots):
		"""Converts the culture of the city and of the surrounding plots to the new owner of a city.
		iCulturePercent determine the percentage that goes to the new owner.
		If old owner is barbarian, all the culture is converted"""

		pCity = gc.getMap().plot(tCityPlot[0], tCityPlot[1])
		city = pCity.getPlotCity()		

		#city
		if (pCity.isCity()):
			iCurrentCityCulture = city.getCulture(iOldOwner)
			city.setCulture(iOldOwner, iCurrentCityCulture*(100-iCulturePercent)/100, False)
			if (iNewOwner != con.iBarbarian):
				city.setCulture(con.iBarbarian, 0, True)
			city.setCulture(iNewOwner, iCurrentCityCulture*iCulturePercent/100, False)
			if (city.getCulture(iNewOwner) <= 10):
				city.setCulture(iNewOwner, 20, False)

		#halve barbarian culture in a broader area
		if (bBarbarian2x2Decay or bBarbarian2x2Conversion):
			if (iNewOwner != con.iBarbarian and iNewOwner != con.iIndependent and iNewOwner != con.iIndependent2):
				for x in range(tCityPlot[0]-2, tCityPlot[0]+3):	# from x-2 to x+2
					for y in range(tCityPlot[1]-2, tCityPlot[1]+3):	# from y-2 to y+2				
						iPlotBarbCulture = gc.getMap().plot(x, y).getCulture(con.iBarbarian)
						if (iPlotBarbCulture > 0):
							if (gc.getMap().plot(x, y).getPlotCity().isNone() or (x==tCityPlot[0] and y==tCityPlot[1])):
								if (bBarbarian2x2Decay):
									gc.getMap().plot(x, y).setCulture(con.iBarbarian, iPlotBarbCulture/4, True)
								if (bBarbarian2x2Conversion):
									gc.getMap().plot(x, y).setCulture(con.iBarbarian, 0, True)
									gc.getMap().plot(x, y).setCulture(iNewOwner, iPlotBarbCulture, True)
						iPlotIndependentCulture = gc.getMap().plot(x, y).getCulture(con.iIndependent)
						if (iPlotIndependentCulture > 0):
							if (gc.getMap().plot(x, y).getPlotCity().isNone() or (x==tCityPlot[0] and y==tCityPlot[1])):
								if (bBarbarian2x2Decay):
									gc.getMap().plot(x, y).setCulture(con.iIndependent, iPlotIndependentCulture/4, True)
								if (bBarbarian2x2Conversion):
									gc.getMap().plot(x, y).setCulture(con.iIndependent, 0, True)
									gc.getMap().plot(x, y).setCulture(iNewOwner, iPlotIndependentCulture, True)
						iPlotIndependent2Culture = gc.getMap().plot(x, y).getCulture(con.iIndependent2)
						if (iPlotIndependent2Culture > 0):
							if (gc.getMap().plot(x, y).getPlotCity().isNone() or (x==tCityPlot[0] and y==tCityPlot[1])):
								if (bBarbarian2x2Decay):
									gc.getMap().plot(x, y).setCulture(con.iIndependent2, iPlotIndependent2Culture/4, True)
								if (bBarbarian2x2Conversion):
									gc.getMap().plot(x, y).setCulture(con.iIndependent2, 0, True)
									gc.getMap().plot(x, y).setCulture(iNewOwner, iPlotIndependent2Culture, True)
									
		#plot			       
		for x in range(tCityPlot[0]-1, tCityPlot[0]+2):	# from x-1 to x+1
			for y in range(tCityPlot[1]-1, tCityPlot[1]+2):	# from y-1 to y+1
				pCurrent = gc.getMap().plot(x, y)
				
				iCurrentPlotCulture = pCurrent.getCulture(iOldOwner)

				if (pCurrent.isCity()):				
					pCurrent.setCulture(iNewOwner, iCurrentPlotCulture*iCulturePercent/100, True)
					pCurrent.setCulture(iOldOwner, iCurrentPlotCulture*(100-iCulturePercent)/100, True)
				else:
					pCurrent.setCulture(iNewOwner, iCurrentPlotCulture*iCulturePercent/3/100, True)
					pCurrent.setCulture(iOldOwner, iCurrentPlotCulture*(100-iCulturePercent/3)/100, True)

				#cut other players culture
##				for iCiv in range(iNumPlayers):
##					if (iCiv != iNewOwner and iCiv != iOldOwner):
##						iPlotCulture = gc.getMap().plot(x, y).getCulture(iCiv)
##						if (iPlotCulture > 0):
##							gc.getMap().plot(x, y).setCulture(iCiv, iPlotCulture/3, True)
							
				#print (x, y, pCurrent.getCulture(iNewOwner), ">", pCurrent.getCulture(iOldOwner))

				if (not pCurrent.isCity()):
					if (bAlwaysOwnPlots):
						pCurrent.setOwner(iNewOwner)
					else:
						if (pCurrent.getCulture(iNewOwner)*4 > pCurrent.getCulture(iOldOwner)):
							pCurrent.setOwner(iNewOwner)					
					#print ("NewOwner", pCurrent.getOwner())



	#handler
	def spreadMajorCulture(self, iMajorCiv, iX, iY):  
		
		for x in range(iX-3, iX+4):	# from x-4 to x+4
			for y in range(iY-3, iY+4):	# from y-4 to y+4
				pCurrent = gc.getMap().plot(x, y)
				if (pCurrent.isCity()):
					city = pCurrent.getPlotCity()
					if (city.getOwner() >= iNumMajorPlayers):
						iMinor = city.getOwner()
						iDen = 25
						if (gc.getPlayer(iMajorCiv).getSettlerValue(x, y) >= 400):
							iDen = 10
						elif (gc.getPlayer(iMajorCiv).getSettlerValue(x, y) >= 150):
							iDen = 15
							
						iMinorCityCulture = city.getCulture(iMinor)
						city.setCulture(iMajorCiv, iMinorCityCulture/iDen, True)
						
						iMinorPlotCulture = pCurrent.getCulture(iMinor)
						pCurrent.setCulture(iMajorCiv, iMinorPlotCulture/iDen, True)
						
		#plot = gc.getMap().plot(iX, iY)
		#if plot.isCity():
		#	city = plot.getPlotCity()
		#	iCityCulture = 0
		#	iPlotCulture = 0
		#	for iMinor in range(con.iNumPlayers, con.iNumTotalPlayersB):
		#		iCityCulture += city.getCulture(iMinor)
		#		iPlotCulture += plot.getCulture(iMinor)
		#		city.setCulture(iMinor, 0, True)
		#		plot.setCulture(iMinor, 0, True)
		#	city.changeCulture(iMajorCiv, iCityCulture, True)
		#	plot.changeCulture(iMajorCiv, iPlotCulture, True)

	#UniquePowers
	def convertPlotCulture(self, plot, iPlayer, iPercent, bOwner):
	
		if plot.isCity():
			city = plot.getPlotCity()
			iConvertedCulture = 0
			for iLoopPlayer in range(iNumTotalPlayers):
				if iLoopPlayer != iPlayer:
					iLoopCulture = city.getCulture(iLoopPlayer)
					iConvertedCulture += iLoopCulture * iPercent / 100
					city.setCulture(iLoopPlayer, iLoopCulture * (100-iPercent) / 100, True)
					
			city.changeCulture(iPlayer, iConvertedCulture, True)
	
		iConvertedCulture = 0	
		for iLoopPlayer in range(iNumTotalPlayers):
			if iLoopPlayer != iPlayer:
				iLoopCulture = plot.getCulture(iLoopPlayer)
				iConvertedCulture += iLoopCulture * iPercent / 100
				plot.setCulture(iLoopPlayer, iLoopCulture * (100-iPercent) / 100, True)
				
		plot.changeCulture(iPlayer, iConvertedCulture, True)
		
		if bOwner: plot.setOwner(iPlayer)
		
		#if (pCurrent.isCity()):
		#	city = pCurrent.getPlotCity()
		#	iCivCulture = city.getCulture(iCiv)
		#	iLoopCivCulture = 0
		#	for iLoopCiv in range(iNumTotalPlayers):
		#		if (iLoopCiv != iCiv):
		#			iLoopCivCulture += city.getCulture(iLoopCiv)				
		#			city.setCulture(iLoopCiv, city.getCulture(iLoopCiv)*(100-iPercent)/100, True)
		#	city.setCulture(iCiv, iCivCulture + iLoopCivCulture, True)  
	
##		for iLoopCiv in range(iNumTotalPlayers):
##			if (iLoopCiv != iCiv):
##				iLoopCivCulture = pCurrent.getCulture(iLoopCiv)
##				iCivCulture = pCurrent.getCulture(iCiv)
##				pCurrent.setCulture(iLoopCiv, iLoopCivCulture*(100-iPercent)/100, True)
##				pCurrent.setCulture(iCiv, iCivCulture + iLoopCivCulture*iPercent/100, True)
		#iCivCulture = pCurrent.getCulture(iCiv)
		#iLoopCivCulture = 0
		#for iLoopCiv in range(iNumTotalPlayers):
		#	if (iLoopCiv != iCiv):
		#		iLoopCivCulture += pCurrent.getCulture(iLoopCiv)				
		#		pCurrent.setCulture(iLoopCiv, pCurrent.getCulture(iLoopCiv)*(100-iPercent)/100, True)
		#pCurrent.setCulture(iCiv, iCivCulture + iLoopCivCulture, True)				
		#if (bOwner == True):
		#	pCurrent.setOwner(iCiv)

	#DynamicCivs
	def getMaster(self, iCiv):
		team = gc.getTeam(gc.getPlayer(iCiv).getTeam())
		for iMaster in range(iNumTotalPlayers):
			if team.isVassal(iMaster):
				return iMaster
		return -1



				




	#Congresses, RiseAndFall
	def pushOutGarrisons(self, tCityPlot, iOldOwner):
		tDestination = (-1, -1)
		for x in range(tCityPlot[0]-2, tCityPlot[0]+3):
			for y in range(tCityPlot[1]-2, tCityPlot[1]+3):
				pDestination = gc.getMap().plot(x, y)
				if (pDestination.getOwner() == iOldOwner and (not pDestination.isWater()) and (not pDestination.isImpassable())):
					tDestination = (x, y)
					break
					break
		if (tDestination != (-1, -1)):
			plotCity = gc.getMap().plot(tCityPlot[0], tCityPlot[1])
			iNumUnitsInAPlot = plotCity.getNumUnits()
			j = 0
			for i in range(iNumUnitsInAPlot):			
				unit = plotCity.getUnit(j)
				if (unit.getDomainType() == 2): #land unit
					unit.setXYOld(tDestination[0], tDestination[1])
				else:
					j += 1

	def relocateGarrisons(self, tCityPlot, iOldOwner):
		if iOldOwner < con.iNumPlayers:
			pCity = self.getRandomCity(iOldOwner)
			if pCity != -1:
				plot = gc.getMap().plot(tCityPlot[0],tCityPlot[1])
				iNumUnits = plot.getNumUnits()
				j = 0
				for i in range(iNumUnits):
					unit = plot.getUnit(j)
					if (unit.getDomainType() == 2): #land
						unit.setXYOld(pCity.getX(), pCity.getY())
					else:
						j += 1
		else:
			plot = gc.getMap().plot(tCityPlot[0], tCityPlot[1])
			iNumUnits = plot.getNumUnits()
			for i in range(iNumUnits):
				unit = plot.getUnit(i)
				unit.kill(False, iOldOwner)
				
	def removeCoreUnits(self, iPlayer):
		for (x, y) in Areas.getBirthArea(iPlayer):
			plot = gc.getMap().plot(x, y)
			if plot.isCity():
				pCity = plot.getPlotCity()
				if pCity.getOwner() != iPlayer:
					x = pCity.getX()
					y = pCity.getY()
					self.relocateGarrisons((x,y), pCity.getOwner())
					self.relocateSeaGarrisons((x,y), pCity.getOwner())
					self.createGarrisons((x,y), pCity.getOwner(), 2)
			else:
				iNumUnits = plot.getNumUnits()
				j = 0
				for i in range(iNumUnits):
					unit = plot.getUnit(j)
					iOwner = unit.getOwner()
					if iOwner < con.iNumPlayers and iOwner != iPlayer:
						capital = gc.getPlayer(iOwner).getCapitalCity()
						if capital.getX() != -1 and capital.getY() != -1:
							unit.setXYOld(capital.getX(), capital.getY())
					else:
						j += 1
				
	#Congresses, RiseAndFall
	def relocateSeaGarrisons(self, tCityPlot, iOldOwner):
		tDestination = (-1, -1)
		for city in self.getCityList(iOldOwner):
			if (city.isCoastalOld()):
				tDestination = (city.getX(), city.getY())
		if (tDestination == (-1, -1)):		    
			for x in range(tCityPlot[0]-12, tCityPlot[0]+12):
				for y in range(tCityPlot[1]-12, tCityPlot[1]+12):
					pDestination = gc.getMap().plot(x, y)
					if (pDestination.isWater()):
						tDestination = (x, y)
						break
						break
		if (tDestination != (-1, -1)):
			plotCity = gc.getMap().plot(tCityPlot[0], tCityPlot[1])
			iNumUnitsInAPlot = plotCity.getNumUnits()
			j = 0
			for i in range(iNumUnitsInAPlot):
				unit = plotCity.getUnit(j)
				if (unit.getDomainType() == 0): #sea unit
					unit.setXYOld(tDestination[0], tDestination[1])
				else:
					j += 1


	#Congresses, RiseAndFall
	def createGarrisons(self, tCityPlot, iNewOwner, iNumUnits):
		plotCity = gc.getMap().plot(tCityPlot[0], tCityPlot[1])
		city = plotCity.getPlotCity()    
		iNumUnitsInAPlot = plotCity.getNumUnits()
		pCiv = gc.getPlayer(iNewOwner)

		iUnitType = self.getBestDefender(iNewOwner)

		self.makeUnit(iUnitType, iNewOwner, [tCityPlot[0], tCityPlot[1]], iNumUnits)

		
	def resetUHV(self, iPlayer):
		if (iPlayer < iNumMajorPlayers):
			if (self.getGoal(iPlayer, 0) == -1):
				self.setGoal(iPlayer, 0, 0)
			if (self.getGoal(iPlayer, 1) == -1):
				self.setGoal(iPlayer, 1, 0)
			if (self.getGoal(iPlayer, 2) == -1):
				self.setGoal(iPlayer, 2, 0)

	def clearPlague(self, iCiv):
		for pyCity in PyPlayer(iCiv).getCityList():
			if (pyCity.GetCy().hasBuilding(con.iPlague)):
				pyCity.GetCy().setHasRealBuilding(con.iPlague, False)




	#AIWars, by CyberChrist

	def isNoVassal(self, iCiv):
		for iMaster in range(iNumTotalPlayers):
			if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isVassal(iMaster)):
				return False
		return True

	def isAVassal(self, iCiv):
		for iMaster in range(iNumTotalPlayers):
			if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isVassal(iMaster)):
				return True
		return False

	#Barbs, RiseAndFall
	def squareSearch( self, tTopLeft, tBottomRight, function, argsList, tExceptions = () ): #by LOQ
		"""Searches all tile in the square from tTopLeft to tBottomRight and calls function for
		every tile, passing argsList. The function called must return a tuple: (1) a result, (2) if
		a plot should be painted and (3) if the search should continue."""
		tPaintedList = []
		result = None
		for x in range(tTopLeft[0], tBottomRight[0]+1):
			for y in range(tTopLeft[1], tBottomRight[1]+1):
				result, bPaintPlot, bContinueSearch = function((x, y), result, argsList)
				if bPaintPlot:			# paint plot
					tPaintedList.append((x, y))
				if not bContinueSearch:		# goal reached, so stop
					return result, tPaintedList
		return result, tPaintedList

	#Barbs, RiseAndFall
	def outerInvasion( self, tCoords, result, argsList ):
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it's hill or flatlands, it isn't marsh or jungle, it isn't occupied by a unit or city and if it isn't a civ's territory"""
		bPaint = True
		bContinue = True
		pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
		if ( pCurrent.isHills() or pCurrent.isFlatlands() ):
			if (pCurrent.getTerrainType() != con.iMarsh) and (pCurrent.getFeatureType() != con.iJungle):
				if ( not pCurrent.isCity() and not pCurrent.isUnit() ):
					if (pCurrent.countTotalCulture() == 0 ):
						# this is a good plot, so paint it and continue search
						return (None, bPaint, bContinue)
		# not a good plot, so don't paint it but continue search
		return (None, not bPaint, bContinue)

	#Barbs
	def innerSeaSpawn( self, tCoords, result, argsList ):
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it's water and it isn't occupied by any unit. Unit check extended to adjacent plots"""
		bPaint = True
		bContinue = True
		pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
		if ( pCurrent.isWater()):
			if ( not pCurrent.isCity() and not pCurrent.isUnit() and pCurrent.area().getNumTiles() > 10 ):
				iClean = 0
				for x in range(tCoords[0] - 1, tCoords[0] + 2):	# from x-1 to x+1
					for y in range(tCoords[1] - 1, tCoords[1] + 2):	# from y-1 to y+1
						if (pCurrent.getNumUnits() != 0):
							iClean += 1
				if ( iClean == 0 ):   
					# this is a good plot, so paint it and continue search
					return (None, bPaint, bContinue)
		# not a good plot, so don't paint it but continue search
		return (None, not bPaint, bContinue)

	#Barbs
	def outerSeaSpawn( self, tCoords, result, argsList ):
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it's water and it isn't occupied by any unit and if it isn't a civ's territory. Unit check extended to adjacent plots"""
		bPaint = True
		bContinue = True
		pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
		if ( pCurrent.isWater()):
			if ( not pCurrent.isCity() and not pCurrent.isUnit() and pCurrent.area().getNumTiles() > 10):
				if (pCurrent.countTotalCulture() == 0 ):
					iClean = 0
					for x in range(tCoords[0] - 1, tCoords[0] + 2):	# from x-1 to x+1
						for y in range(tCoords[1] - 1, tCoords[1] + 2):	# from y-1 to y+1
							if (pCurrent.getNumUnits() != 0):
								iClean += 1
					if ( iClean == 0 ):   
						# this is a good plot, so paint it and continue search
						return (None, bPaint, bContinue)
		# not a good plot, so don't paint it but continue search
		return (None, not bPaint, bContinue)

	def outerCoastSpawn( self, tCoords, result, argsList ):
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it's water and it isn't occupied by any unit and if it isn't a civ's territory. Unit check extended to adjacent plots"""
		bPaint = True
		bContinue = True
		pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
		if ( pCurrent.getTerrainType() == con.iCoast):
			if ( not pCurrent.isCity() and not pCurrent.isUnit() and pCurrent.area().getNumTiles() > 10 ):
				if (pCurrent.countTotalCulture() == 0 ):
					iClean = 0
					for x in range(tCoords[0] - 1, tCoords[0] + 2):	# from x-1 to x+1
						for y in range(tCoords[1] - 1, tCoords[1] + 2):	# from y-1 to y+1
							if (pCurrent.getNumUnits() != 0):
								iClean += 1
					if ( iClean == 0 ):   
						# this is a good plot, so paint it and continue search
						return (None, bPaint, bContinue)
		# not a good plot, so don't paint it but continue search
		return (None, not bPaint, bContinue)

	#Barbs
	def outerSpawn( self, tCoords, result, argsList ):
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it's hill or flatlands, it isn't marsh or jungle, it isn't occupied by a unit or city and if it isn't a civ's territory.
		Unit check extended to adjacent plots"""
		bPaint = True
		bContinue = True
		pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
		if ( pCurrent.isHills() or pCurrent.isFlatlands() ):
			if (pCurrent.getTerrainType() != con.iMarsh) and (pCurrent.getFeatureType() != con.iJungle):
				if ( not pCurrent.isCity() and not pCurrent.isUnit() ):
					iClean = 0
					for x in range(tCoords[0] - 1, tCoords[0] + 2):	# from x-1 to x+1
						for y in range(tCoords[1] - 1, tCoords[1] + 2):	# from y-1 to y+1
							if (pCurrent.getNumUnits() != 0):
								iClean += 1
					if ( iClean == 0 ):
						if (pCurrent.countTotalCulture() == 0 ):
							# this is a good plot, so paint it and continue search
							return (None, bPaint, bContinue)
		# not a good plot, so don't paint it but continue search
		return (None, not bPaint, bContinue)					

	#RiseAndFall
	def innerInvasion( self, tCoords, result, argsList ):
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it's hill or flatlands, it isn't marsh or jungle, it isn't occupied by a unit or city and if it isn't a civ's territory"""
		bPaint = True
		bContinue = True
		pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
		if ( pCurrent.isHills() or pCurrent.isFlatlands() ):
			if (pCurrent.getTerrainType() != con.iMarsh) and (pCurrent.getFeatureType() != con.iJungle):
				if ( not pCurrent.isCity() and not pCurrent.isUnit() ):
					if (pCurrent.getOwner() in argsList ):
						# this is a good plot, so paint it and continue search
						return (None, bPaint, bContinue)
		# not a good plot, so don't paint it but continue search
		return (None, not bPaint, bContinue)

	def internalInvasion(self, tCoords, result, argsList):
		"""Like inner invasion, but ignores territory, to allow for more barbarians"""
		bPaint = True
		bContinue = True
		pCurrent = gc.getMap().plot(tCoords[0], tCoords[1])
		if pCurrent.isHills() or pCurrent.isFlatlands():
			if pCurrent.getTerrainType() != con.iMarsh and pCurrent.getFeatureType() != con.iJungle:
				if not pCurrent.isCity() and not pCurrent.isUnit():
					return (None, bPaint, bContinue)
		return (None, not bPaint, bContinue)
	    
	def innerSpawn( self, tCoords, result, argsList ):
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it's hill or flatlands, it isn't marsh or jungle, it isn't occupied by a unit or city and if it isn't a civ's territory"""
		bPaint = True
		bContinue = True
		pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
		if ( pCurrent.isHills() or pCurrent.isFlatlands() ):
			if (pCurrent.getTerrainType() != con.iMarsh) and (pCurrent.getFeatureType() != con.iJungle):
				if ( not pCurrent.isCity() and not pCurrent.isUnit() ):
					iClean = 0
					for x in range(tCoords[0] - 1, tCoords[0] + 2):	# from x-1 to x+1
						for y in range(tCoords[1] - 1, tCoords[1] + 2):	# from y-1 to y+1
							if (pCurrent.getNumUnits() != 0):
								iClean += 1
					if ( iClean == 0 ):  
						if (pCurrent.getOwner() in argsList ):
							# this is a good plot, so paint it and continue search
							return (None, bPaint, bContinue)
		# not a good plot, so don't paint it but continue search
		return (None, not bPaint, bContinue)

	#RiseAndFall
	def goodPlots( self, tCoords, result, argsList ):
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it's hill or flatlands, it isn't desert, tundra, marsh or jungle; it isn't occupied by a unit or city and if it isn't a civ's territory.
		Unit check extended to adjacent plots"""
		bPaint = True
		bContinue = True
		pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
		if ( pCurrent.isHills() or pCurrent.isFlatlands() ):
			if ( not pCurrent.isImpassable()):
				if ( not pCurrent.isUnit() ):
					if (pCurrent.getTerrainType() != con.iDesert) and (pCurrent.getTerrainType() != con.iTundra) and (pCurrent.getTerrainType() != con.iMarsh) and (pCurrent.getFeatureType() != con.iJungle):
						if (pCurrent.countTotalCulture() == 0 ):
							# this is a good plot, so paint it and continue search
							return (None, bPaint, bContinue)
		# not a good plot, so don't paint it but continue search
		return (None, not bPaint, bContinue)

	#RiseAndFall
	def cityPlots(self, tCoords, result, argsList):
		bPaint = True
		bContinue = True
		pCurrent = gc.getMap().plot(tCoords[0], tCoords[1])
		if pCurrent.isCity():
			return (None, bPaint, bContinue)
		return (None, not bPaint, bContinue)

	def ownedCityPlots( self, tCoords, result, argsList ):
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it contains a city belonging to the civ"""
		bPaint = True
		bContinue = True
		pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
		if (pCurrent.getOwner() == argsList ):
			if (pCurrent.isCity()):
				# this is a good plot, so paint it and continue search
				return (None, bPaint, bContinue)
		# not a good plot, so don't paint it but continue search
		return (None, not bPaint, bContinue)

	def ownedCityPlotsAdjacentArea( self, tCoords, result, argsList ):
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it contains a city belonging to the civ"""
		bPaint = True
		bContinue = True
		pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
		#print(tCoords[0], tCoords[1], pCurrent.isCity(), pCurrent.getOwner() == argsList[0], pCurrent.isAdjacentToArea(gc.getMap().plot(argsList[1][0],argsList[1][1]).area()))
		if (pCurrent.getOwner() == argsList[0] and pCurrent.isAdjacentToArea(gc.getMap().plot(argsList[1][0],argsList[1][1]).area())):
			if (pCurrent.isCity()):
				# this is a good plot, so paint it and continue search
				return (None, bPaint, bContinue)
		# not a good plot, so don't paint it but continue search
		return (None, not bPaint, bContinue)

	def foundedCityPlots( self, tCoords, result, argsList ):
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it contains a city belonging to the civ"""
		bPaint = True
		bContinue = True
		pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
		if (pCurrent.isCity()):
			if (pCurrent.getPlotCity().getOriginalOwner() == argsList ):			
				# this is a good plot, so paint it and continue search
				return (None, bPaint, bContinue)
		# not a good plot, so don't paint it but continue search
		return (None, not bPaint, bContinue)    

	def ownedPlots( self, tCoords, result, argsList ):
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it is in civ's territory."""
		bPaint = True
		bContinue = True
		pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
		if (pCurrent.getOwner() == argsList ):
			# this is a good plot, so paint it and continue search
			return (None, bPaint, bContinue)
		# not a good plot, so don't paint it but continue search
		return (None, not bPaint, bContinue)

	def goodOwnedPlots( self, tCoords, result, argsList ):
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it's hill or flatlands; it isn't marsh or jungle, it isn't occupied by a unit and if it is in civ's territory."""
		bPaint = True
		bContinue = True
		pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
		if ( pCurrent.isHills() or pCurrent.isFlatlands() ):
			if (pCurrent.getTerrainType() != con.iMarsh) and (pCurrent.getFeatureType() != con.iJungle):
				if ( not pCurrent.isCity() and not pCurrent.isUnit() ):
					    if (pCurrent.getOwner() == argsList ):
						    # this is a good plot, so paint it and continue search
						    return (None, bPaint, bContinue)
		# not a good plot, so don't paint it but continue search
		return (None, not bPaint, bContinue)

	def getTurns(self, turns): # edead
		"""Returns the amount of turns modified adequately for the game's speed.
		Values are based on CIV4GameSpeedInfos.xml. Use this only for durations, intervals etc.; 
		for year->turn conversions, use the DLL function getTurnForYear(int year)."""
		iGameSpeed = gc.getGame().getGameSpeedType()
		if iGameSpeed == 2: return turns # normal
		elif iGameSpeed == 1: # epic
			if turns == 3: return 5 # getTurns(6) must be a multiple of getTurns(3) for turn divisors in Stability.py
			elif turns == 6: return 10
			else: return turns*3/2
		elif iGameSpeed == 0: return turns*3 # marathon
		#elif iGameSpeed == 3: return turns*2/3 # quick
		return turns

	# Leoreth - RiseAndFall
	def clearCatapult(self, iCiv):
		plotZero = gc.getMap().plot( 0, 0 )			
		if (plotZero.getNumUnits()):
		       catapult = plotZero.getUnit(0)
		       catapult.kill(False, iCiv)
		gc.getMap().plot(0, 0).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(0, 1).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(1, 1).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(1, 0).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(123, 0).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(123, 1).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(2, 0).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(2, 1).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(2, 2).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(1, 2).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(0, 2).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(122, 0).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(122, 1).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(122, 2).setRevealed(iCiv, False, True, -1);
		gc.getMap().plot(123, 2).setRevealed(iCiv, False, True, -1);

	# Leoreth
	def getReborn(self, iCiv):
		return gc.getPlayer(iCiv).getReborn()

	# Leoreth
	def getCoreCityList(self, iCiv, bReborn):
		cityList = []
		for (x, y) in Areas.getCoreArea(iCiv, bReborn):
			plot = gc.getMap().plot(x, y)
			if plot.isCity():
				cityList.append(plot.getPlotCity())
		return cityList

	# Leoreth
	def getCoreUnitList(self, iCiv, reborn):
		unitList = []
		for (x, y) in Areas.getCoreArea(iCiv, bReborn):
			plot = gc.getMap().plot(x,y)
			if not plot.isCity():
				for i in range(plot.getNumUnits()):
					unitList.append(plot.getUnit(i))
		return unitList

	def getCivRectangleCities(self, iCiv, TopLeft, BottomRight):
		cityList = []
		for x in range(TopLeft[0], BottomRight[0]+1):
			for y in range(TopLeft[1], BottomRight[1]+1):
				plot = gc.getMap().plot(x,y)
				if plot.isCity():
					cityList.append(plot.getPlotCity())
		return cityList

	

	def removeReligionByArea(self, lPlotList, iReligion):
		lCityList = []
		for city in self.getAreaCities(lPlotList):
			if city.isHasReligion(iReligion) and not city.isHolyCity():
				city.setHasReligion(iReligion, False, False, False)
			if city.hasBuilding(con.iTemple + iReligion*4):
				city.setHasRealBuilding((con.iTemple + iReligion*4), False)
			if city.hasBuilding(con.iCathedral + iReligion*4):
				city.setHasRealBuilding((con.iCathedral + iReligion*4), False)
			if city.hasBuilding(con.iMonastery + iReligion*4):
				city.setHasRealBuilding((con.iMonastery + iReligion*4), False)

	def getEasternmostCity(self, iCiv):
		pPlayer = gc.getPlayer(iCiv)
		pResultCity = pPlayer.getCapitalCity()
		for i in range(pPlayer.getNumCities()):
			if pPlayer.getCity(i).getX() > pResultCity.getX():
				pResultCity = pPlayer.getCity(i)
		return pResultCity

	def getNorthernmostCity(self, iCiv):
		pPlayer = gc.getPlayer(iCiv)
		pResultCity = pPlayer.getCapitalCity()
		for i in range(pPlayer.getNumCities()):
			if pPlayer.getCity(i).getY() > pResultCity.getY():
				pResultCity = pPlayer.getCity(i)
		return pResultCity

	def getWesternmostCity(self, iCiv):
		pPlayer = gc.getPlayer(iCiv)
		pResultCity = pPlayer.getCapitalCity()
		for i in range(pPlayer.getNumCities()):
			if pPlayer.getCity(i).getX() < pResultCity.getX():
				pResultCity = pPlayer.getCity(i)
		return pResultCity

	def getFreeNeighborPlot(self, tPlot):
		x, y = tPlot
		plotList = []
		for i in range(x-1, x+2):
			for j in range(y-1, y+2):
				if (i, j) != (x, y):
					plot = gc.getMap().plot(i, j)
					if (not plot.isPeak()) and (not plot.isWater()) and (not plot.isCity()) and (not plot.isUnit()):
						plotList.append((i, j))
		iRand = gc.getGame().getSorenRandNum(len(plotList), '')
		return plotList[iRand]

	def colonialConquest(self, iCiv, x, y):
		bRifling = gc.getTeam(iCiv).isHasTech(con.iRifling)
		iTargetCiv = gc.getMap().plot(x,y).getPlotCity().getOwner()
		lFreePlots = []
		
		for i in range(x-1, x+2):
			for j in range(y-1, y+2):
				current = gc.getMap().plot(i, j)
				if not current.isCity() and not current.isPeak() and not current.isWater():
					#if not current.getFeatureType() == con.iJungle and not current.getTerrainType() == con.iMarsh:
					lFreePlots.append((i,j))
					
		if iTargetCiv != -1 and not gc.getTeam(iCiv).isAtWar(iTargetCiv):
			gc.getTeam(iCiv).declareWar(iTargetCiv, True, WarPlanTypes.WARPLAN_TOTAL)
			
		# independents too so the conquerors don't get pushed out in case the target collapses
		if not gc.getTeam(iCiv).isAtWar(con.iIndependent): gc.getTeam(iCiv).declareWar(con.iIndependent, True, WarPlanTypes.WARPLAN_LIMITED)
		if not gc.getTeam(iCiv).isAtWar(con.iIndependent2): gc.getTeam(iCiv).declareWar(con.iIndependent2, True, WarPlanTypes.WARPLAN_LIMITED)
			
		iRand = gc.getGame().getSorenRandNum(len(lFreePlots), 'random plot')
		tPlot = lFreePlots[iRand]
		
		if iCiv in [con.iSpain, con.iPortugal, con.iNetherlands]:
			iNumUnits = 2
		elif iCiv in [con.iFrance, con.iEngland]:
			iNumUnits = 3
			
		iSiege = self.getBestSiege(iCiv)
		iInfantry = self.getBestInfantry(iCiv)
		
		iExp = 0
		if self.getHumanID() != iCiv: iExp = 2
		
		if iSiege:
			self.makeUnit(iSiege, iCiv, tPlot, iNumUnits, '', 2)
			
		if iInfantry:
			self.makeUnit(iInfantry, iCiv, tPlot, 2*iNumUnits, '', 2)


	def colonialAcquisition(self, iCiv, x, y):
		if iCiv in [con.iPortugal, con.iSpain]:
			iNumUnits = 1
		elif iCiv in [con.iFrance, con.iEngland, con.iNetherlands]:
			iNumUnits = 2
		if gc.getMap().plot(x,y).isCity():
			self.flipCity((x,y), False, True, iCiv, [])
			self.makeUnit(con.iWorker, iCiv, (x,y), iNumUnits)
			iInfantry = self.getBestInfantry(iCiv)
			if iInfantry:
				self.makeUnit(iInfantry, iCiv, (x,y), iNumUnits)
			if gc.getPlayer(iCiv).getStateReligion() != -1:
				self.makeUnit(con.iMissionary+gc.getPlayer(iCiv).getStateReligion(), iCiv, (x,y), 1)
		else:
			gc.getMap().plot(x,y).setCulture(iCiv, 10, True)
			gc.getMap().plot(x,y).setOwner(iCiv)
			if self.getHumanID() == iCiv:
				self.makeUnit(con.iSettler, iCiv, (x,y), 1)
			else:
				gc.getPlayer(iCiv).found(x, y)
			self.makeUnit(con.iWorker, iCiv, (x,y), 2)
			iInfantry = self.getBestInfantry(iCiv)
			if iInfantry:
				self.makeUnit(iInfantry, iCiv, (x,y), 2)
			if gc.getPlayer(iCiv).getStateReligion() != -1:
				self.makeUnit(con.iMissionary+gc.getPlayer(iCiv).getStateReligion(), iCiv, (x,y), 1)

	def getColonialTargets(self, iPlayer, bEmpty=False):
		if iPlayer == con.iSpain or iPlayer == con.iFrance:
			iNumCities = 1
		else:
			iNumCities = 3
			
		if iPlayer == con.iPortugal and self.getHumanID() != con.iPortugal:
			iNumCities = 5

		lCivList = [con.iSpain, con.iFrance, con.iEngland, con.iPortugal, con.iNetherlands]
		id = lCivList.index(iPlayer)

		lPlotList = con.tTradingCompanyPlotLists[id]

		cityList = []
		for tPlot in lPlotList:
			x, y = tPlot
			if gc.getMap().plot(x, y).isCity():
				if gc.getMap().plot(x, y).getPlotCity().getOwner() != iPlayer:
					cityList.append((x, y))

		targetList = []

		if len(cityList) != 0:
			for i in range(iNumCities):
				iRand = gc.getGame().getSorenRandNum(len(cityList), 'Random city')
				print 'iRand = '+str(iRand)
				if len(cityList) > 0 and cityList[iRand] not in targetList:
					targetList.append(cityList[iRand])
					cityList.remove(cityList[iRand])

		if bEmpty:
			while len(targetList) < iNumCities and len(lPlotList) > 0:
				iRand = gc.getGame().getSorenRandNum(len(lPlotList), 'Random free plot')
				x, y = lPlotList[iRand]
				bValid = True
				for i in range(x-1, x+2):
					for j in range(y-1, y+2):
						if gc.getMap().plot(i, j).isCity():
							bValid = False
							break
							break
							
				if bValid:
					targetList.append(lPlotList[iRand])
				
				lPlotList.remove(lPlotList[iRand])

		return targetList

	# Leoreth: tests if the plot is a part of the civs border in the specified direction
	#	  returns list containing the plot if that's the case, empty list otherwise
	#	  iDirection = -1 tests all directions
	def testBorderPlot(self, tPlot, iCiv, iDirection):
		x, y = tPlot
		if gc.getMap().plot(x, y).getOwner() != iCiv or gc.getMap().plot(x, y).isWater() or gc.getMap().plot(x, y).isPeak() or gc.getMap().plot(x, y).isCity():
			return []

		lDirectionList = []
		if iDirection == -1 or iDirection == DirectionTypes.DIRECTION_NORTH:
			if y < 68:
				lDirectionList.append((0, 1))
		if iDirection == -1 or iDirection == DirectionTypes.DIRECTION_SOUTH:
			if y > 0:
				lDirectionList.append((0, -1))
		if iDirection == -1 or iDirection == DirectionTypes.DIRECTION_EAST:
			if x < 124:
				lDirectionList.append((1, 0))
			else:
				lDirectionList.append((-124, 0))
		if iDirection == -1 or iDirection == DirectionTypes.DIRECTION_WEST:
			if x > 0:
				lDirectionList.append((-1, 0))
			else:
				lDirectionList.append((124, 0))

		for tDirection in lDirectionList:
			dx, dy = tDirection
			nx = x + dx
			ny = y + dy
			if gc.getMap().plot(nx, ny).getOwner() != iCiv:
				return [tPlot]

		return []

	# Leoreth: return list of border plots in a given direction, -1 means all directions
	def getBorderPlotList(self, iCiv, iDirection):
		lPlotList = []

		for x in range(124):
			for y in range(68):
				if gc.getMap().plot(x, y).getOwner() == iCiv:
					lPlotList.extend(self.testBorderPlot((x, y), iCiv, iDirection))

		# exclude Mediterranean islands
		for tPlot in [(68, 39), (69, 39), (71, 40)]:
			if tPlot in lPlotList:
				lPlotList.remove(tPlot)

		return lPlotList
		
	def isPlotInArea(self, tPlot, tTopLeft, tBottomRight, lExceptions=()):
		return tPlot in self.getPlotList(tTopLeft, tBottomRight, lExceptions)
		
	def isPlotInCore(self, iPlayer, tPlot):
		return tPlot in Areas.getCoreArea(iPlayer)
		
	def isPlotInNormal(self, iPlayer, tPlot):
		return tPlot in Areas.getNormalArea(iPlayer)
		
	def relocateCapital(self, iPlayer, newCapital):
		oldCapital = gc.getPlayer(iPlayer).getCapitalCity()
		
		if (oldCapital.getX(), oldCapital.getY()) == Areas.getNewCapital(iPlayer): return
		
		newCapital.setHasRealBuilding(con.iPalace, True)
		oldCapital.setHasRealBuilding(con.iPalace, False)
		
	def getFreePlot(self, x, y):
		pPlot = gc.getMap().plot(x, y)
		lFreePlots = []
		
		if not (pPlot.isCity() or pPlot.isPeak() or pPlot.isWater()):
			return (x, y)
			
		for i in range(x-1, x+2):
			for j in range(y-1, y+2):
				pPlot = gc.getMap().plot(i, j)
				if not (pPlot.isCity() or pPlot.isPeak() or pPlot.isWater()):
					lFreePlots.append((i, j))
					
		iRand = gc.getGame().getSorenRandNum(len(lFreePlots), 'random plot')
		return lFreePlots[iRand]
		
	def handleChineseCities(self, pUnit):
		iRand = gc.getGame().getSorenRandNum(len(lChineseCities), 'Random city')
		
		for i in range(len(lChineseCities)):
			iIndex = (iRand + i) % len(lChineseCities)
			tPlot = lChineseCities[iIndex]
			
			x, y = tPlot
			bFree = True
			for j in range(x-1, x+2):
				for k in range(y-1, y+2):
					if gc.getMap().plot(j, k).isCity():
						bFree = False
						
			if bFree:
				gc.getPlayer(con.iChina).found(x, y)
				pUnit.kill(False, con.iBarbarian)
				return
				
	def foundCapital(self, iPlayer, tPlot, sName, iSize, iCulture, lBuildings=[], lReligions=[], iScenario=False):
	
		if iScenario:
			if self.getScenario() != iScenario: return
		
		#if gc.getGame().getGameTurn() > getTurnForYear(con.tBirth[iPlayer])+3: return
		
		x, y = tPlot
		gc.getPlayer(iPlayer).found(x, y)
		
		city = gc.getMap().plot(x, y).getPlotCity()
		
		city.setCulture(iPlayer, iCulture, True)
		city.setName(sName, False)
	
		if city.getPopulation() < iSize:
			city.setPopulation(iSize)
			
		for iReligion in lReligions:
			city.setHasReligion(iReligion, True, False, False)
			
		for iBuilding in lBuildings:
			city.setHasRealBuilding(iBuilding, True)
			
		return city
			
	def getCivName(self, iCiv):
		return CyTranslator().getText(str(gc.getPlayer(iCiv).getCivilizationShortDescriptionKey()), ())
		
	def moveSlaveToNewWorld(self, iPlayer, unit):
		lEurope = [con.rBritain, con.rIberia, con.rEurope, con.rItaly, con.rScandinavia, con.rRussia, con.rBalkans, con.rAnatolia, con.rMaghreb]
		
		lColonies = []
		for city in PyPlayer(iPlayer).getCityList():
			if city.GetCy().getRegionID() not in lEurope:
				lColonies.append(city)
				
		if len(lColonies) == 0: return
		
		iRand = gc.getGame().getSorenRandNum(len(lColonies), 'random colony')
		city = lColonies[iRand].GetCy()
		
		unit.setXYOld(city.getX(), city.getY())
		
	def clearSlaves(self, iPlayer):
		for x in range(124):
			for y in range(68):
				plot = gc.getMap().plot(x, y)
				if plot.getOwner() == iPlayer:
					if plot.getImprovementType() == gc.getInfoTypeForString("IMPROVEMENT_SLAVE_PLANTATION"):
						plot.setImprovementType(gc.getInfoTypeForString("IMPROVEMENT_PLANTATION"))
					if plot.isCity():
						self.removeSlaves(plot.getPlotCity())
						
		lSlaves = []
		for unit in PyPlayer(iPlayer).getUnitList():
			if unit.getUnitClassType() == gc.getInfoTypeForString("UNITCLASS_SLAVE"):
				lSlaves.append(unit)
				
		for slave in lSlaves:
			slave.kill(con.iBarbarian, False)
			
	def removeSlaves(self, city):
		city.setFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_SLAVE"), 0)
		
	def freeSlaves(self, city, iPlayer):
		iNumSlaves = city.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_SLAVE"))
		if iNumSlaves > 0:
			city.setFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_SLAVE"), 0)
			self.makeUnit(gc.getUnitClassInfo(gc.getUnitInfo(con.iSlave).getUnitClassType()).getDefaultUnitIndex(), iPlayer, (city.getX(), city.getY()), iNumSlaves)
		
	def getRandomEntry(self, list):
		if len(list) == 0: return False
		
		return list[gc.getGame().getSorenRandNum(len(list), 'Random entry')]
			
	def getUniqueUnitType(self, iPlayer, iUnitClass):
		pPlayer = gc.getPlayer(iPlayer)
		return gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationUnits(iUnitClass)
		
	def getUniqueUnit(self, iPlayer, iUnit):
		pPlayer = gc.getPlayer(iPlayer)
		return gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationUnits(gc.getUnitInfo(iUnit).getUnitClassType())
		
	def getBaseUnit(self, iUnit):
		return gc.getUnitClassInfo(gc.getUnitInfo(iUnit).getUnitClassType()).getDefaultUnitIndex()
		
	def replace(self, unit, iUnitType):
		newUnit = gc.getPlayer(unit.getOwner()).initUnit(iUnitType, unit.getX(), unit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.convert(unit)
		return newUnit
		
	def getBestInfantry(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		lInfantryList = [con.iInfantry, con.iRifleman, con.iMusketman, con.iHeavySwordsman, con.iCrossbowman, con.iSwordsman, con.iAxeman, con.iWarrior]
		
		for iBaseUnit in lInfantryList:
			iUnit = self.getUniqueUnitType(iPlayer, gc.getUnitInfo(iBaseUnit).getUnitClassType())
			if pPlayer.canTrain(iUnit, False, False):
				return iUnit
				
		return con.iWarrior
		
	def getBestCavalry(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		lCavalryList = [con.iCavalry, con.iCuirassier, con.iKnight, con.iHorseArcher, con.iChariot]
		
		for iBaseUnit in lCavalryList:
			iUnit = self.getUniqueUnitType(iPlayer, gc.getUnitInfo(iBaseUnit).getUnitClassType())
			if pPlayer.canTrain(iUnit, False, False):
				return iUnit
				
		return con.iWarrior
		
	def getBestSiege(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		lSiegeList = [con.iCannon, con.iBombard, con.iTrebuchet, con.iCatapult]
		
		for iBaseUnit in lSiegeList:
			iUnit = self.getUniqueUnitType(iPlayer, gc.getUnitInfo(iBaseUnit).getUnitClassType())
			if pPlayer.canTrain(iUnit, False, False):
				return iUnit
				
		return con.iWarrior
				
	def getBestCounter(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		lCounterList = [con.iMarine, con.iGrenadier, con.iPikeman, con.iSpearman]
		
		for iBaseUnit in lCounterList:
			iUnit = self.getUniqueUnitType(iPlayer, gc.getUnitInfo(iBaseUnit).getUnitClassType())
			if pPlayer.canTrain(iUnit, False, False):
				return iUnit
				
		return con.iWarrior
		
	def getBestDefender(self, iPlayer):
		# Leoreth: there is a C++ error for barbarians for some reason, workaround by simply using independents
		if iPlayer == con.iBarbarian: iPlayer = con.iIndependent
		
		pPlayer = gc.getPlayer(iPlayer)
		lDefenderList = [con.iInfantry, con.iMachineGun, con.iRifleman, con.iLongbowman, con.iCrossbowman, con.iArcher, con.iWarrior]
		
		for iBaseUnit in lDefenderList:
			iUnit = self.getUniqueUnitType(iPlayer, gc.getUnitInfo(iBaseUnit).getUnitClassType())
			if pPlayer.canTrain(iUnit, False, False):
				return iUnit
				
		return con.iWarrior
		
	def getPlotList(self, tTL, tBR, tExceptions=()):
		return [(x, y) for x in range(tTL[0], tBR[0]+1) for y in range(tTL[1], tBR[1]+1) if (x, y) not in tExceptions]
		
	def getAreaCities(self, lPlots):
		lCities = []
		
		for tPlot in lPlots:
			x, y = tPlot
			plot = gc.getMap().plot(x, y)
			if plot.isCity(): lCities.append(plot.getPlotCity())
		return lCities
		
	def getAreaCitiesCiv(self, iCiv, lPlots):
		lCities = []
		for city in self.getAreaCities(lPlots):
			if city.getOwner() == iCiv:
				lCities.append(city)
		return lCities
		
	def completeCityFlip(self, x, y, iCiv, iOwner, iCultureChange, bBarbarianDecay = True, bBarbarianConversion = False, bAlwaysOwnPlots = False, bFlipUnits = False):
	
		plot = gc.getMap().plot(x, y)
		plot.setRevealed(iCiv, False, True, -1)
	
		self.cultureManager((x, y), iCultureChange, iCiv, iOwner, bBarbarianDecay, bBarbarianConversion, bAlwaysOwnPlots)
		
		if bFlipUnits: 
			self.flipUnitsInCityBefore((x, y), iCiv, iOwner)
		else:
			self.pushOutGarrisons((x, y), iOwner)
			self.relocateSeaGarrisons((x, y), iOwner)
		
		self.setTempFlippingCity((x, y))
		self.flipCity((x, y), 0, 0, iCiv, [iOwner])
		
		if bFlipUnits: 
			self.flipUnitsInCityAfter(self.getTempFlippingCity(), iCiv)
		else:
			self.createGarrisons(self.getTempFlippingCity(), iCiv, 2)
		
		plot.setRevealed(iCiv, True, True, -1)
	
	def isPastBirth(self, iCiv):
		return (gc.getGame().getGameTurn() >= getTurnForYear(con.tBirth[iCiv]))
		
	def getCityList(self, iCiv):
		if iCiv is None: return []
		return [pCity.GetCy() for pCity in PyPlayer(iCiv).getCityList()]
		
	def getAllCities(self):
		lCities = []
		for iPlayer in range(con.iNumPlayers):
			lCities.extend(self.getCityList(iPlayer))
		return lCities
		
	def isNeighbor(self, iCiv1, iCiv2):
		return gc.getGame().isNeighbors(iCiv1, iCiv2)
						
	def isUniqueBuilding(self, iBuilding):
		if (isWorldWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())):
			return true			

		if (isTeamWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())):
			return true

		if (isNationalWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())): #Rhye - should be changed to move embassies to regular buildings
			return true

		# Regular building
		return false
		
	def isReborn(self, iPlayer):
		return gc.getPlayer(iPlayer).isReborn()
		
	def moveCapital(self, iPlayer, tPlot):
		x, y = tPlot
		plot = gc.getMap().plot(x, y)
		
		if plot.isCity():
			newCapital = plot.getPlotCity()
		else:
			return
			
		if newCapital.getOwner() != iPlayer: return
	
		oldCapital = gc.getPlayer(iPlayer).getCapitalCity()
			
		if newCapital.getID() == oldCapital.getID(): return
		
		oldCapital.setHasRealBuilding(con.iPalace, False)
		newCapital.setHasRealBuilding(con.iPalace, True)
		
	def createSettlers(self, iPlayer, iTargetCities):
		iNumCities = 0
		bCapital = False
						
		for (x, y) in Areas.getBirthArea(iPlayer):
			if gc.getMap().plot(x, y).isCity():
				iNumCities += 1
						
		x, y = Areas.getCapital(iPlayer)
		if gc.getMap().plot(x, y).isCity(): bCapital = True
		
		if iNumCities < iTargetCities:
			self.makeUnit(iSettler, iPlayer, (x, y), iTargetCities - iNumCities)
		else:
			if not bCapital: self.makeUnit(iSettler, iPlayer, (x, y), 1)
			
	def createMissionaries(self, iPlayer, iNumUnits, iReligion=None):
		if iReligion == None:
			iReligion = gc.getPlayer(iPlayer).getStateReligion()
			if iReligion < 0: return
			
		if not gc.getGame().isReligionFounded(iReligion): return
		
		self.makeUnit(con.iMissionary + iReligion, iPlayer, Areas.getCapital(iPlayer), iNumUnits)
			
	def getSortedList(self, lList, function, bReverse = False):
		return sorted(lList, key=lambda element: function(element), reverse=bReverse)
		
	def getHighestEntry(self, lList, function = lambda x: x):
		if not lList: return None
		lSortedList = self.getSortedList(lList, function, True)
		return lSortedList[0]
		
	def getHighestIndex(self, lList, function = lambda x: x):
		if not lList: return None
		lSortedList = self.getSortedList(lList, function, True)
		return lList.index(lSortedList[0])
		
	def getColonyPlayer(self, iCiv):
		lCities = self.getAreaCities(Areas.getBirthArea(iCiv))
		lPlayers = []
		lPlayerNumbers = [0 for i in range(con.iNumPlayers)]
		
		for city in lCities: lPlayers.append(city.getOwner())
		
		for i in range(len(lPlayerNumbers)): lPlayerNumbers[i] = lPlayers.count(i)
		
		iHighestEntry = self.getHighestEntry(lPlayerNumbers, lambda x: x)
		
		if iHighestEntry == 0: return -1
		
		return lPlayerNumbers.index(iHighestEntry)
		
	def getScenario(self):
		if gc.getPlayer(con.iEgypt).isPlayable(): return con.i3000BC
		
		if gc.getPlayer(con.iByzantium).isPlayable(): return con.i600AD
		
		return con.i1700AD
		
	def getScenarioStartYear(self):
		lStartYears = [-3000, 600, 1700]
		return lStartYears[self.getScenario()]
		
	def getScenarioStartTurn(self):
		return getTurnForYear(self.getScenarioStartYear())
		
	def hasCivic(self, iPlayer, iCivic):
		return (gc.getPlayer(iPlayer).getCivics(iCivic % 6) == iCivic)
		
	def getUniqueBuildingType(self, iPlayer, iBuildingClass):
		return gc.getCivilizationInfo(gc.getPlayer(iPlayer).getCivilizationType()).getCivilizationBuildings(iBuildingClass)
		
	def getUniqueBuilding(self, iPlayer, iBuilding):
		return gc.getCivilizationInfo(gc.getPlayer(iPlayer).getCivilizationType()).getCivilizationBuildings(gc.getBuildingInfo(iBuilding).getBuildingClassType())
		
	def getStabilityLevel(self, iPlayer):
		return sd.getStabilityLevel(iPlayer)
		
	def setStabilityLevel(self, iPlayer, iNewValue):
		sd.setStabilityLevel(iPlayer, iNewValue)
		
	def showPopup(self, popupID, title, message, labels):
		popup = Popup.PyPopup(popupID, EventContextTypes.EVENTCONTEXT_ALL)
		popup.setHeaderString(title)
		popup.setBodyString(message)
		for i in labels:
		    popup.addButton( i )
		popup.launch(False)
		
	def cityConquestCulture(self, city, iPlayer, iPreviousOwner):
		x = city.getX()
		y = city.getY()
		for i in range(x-1, x+2):
			for j in range(y-1, y+2):
				plot = gc.getMap().plot(i, j)
				if (i, j) == (x, y):
					self.convertPlotCulture(plot, iPlayer, 25, False)
				elif plot.getOwner() == iPreviousOwner:
					self.convertPlotCulture(plot, iPlayer, 50, True)
				else:
					self.convertPlotCulture(plot, iPlayer, 25, True)
					
	def getAllDeals(self, iFirstPlayer, iSecondPlayer):
		lDeals = []
		pGame = gc.getGame()
		
		for i in range(pGame.getNumDeals()):
			pDeal = pGame.getDeal(i)
			if (pDeal.getFirstPlayer() == iFirstPlayer and pDeal.getSecondPlayer() == iSecondPlayer) or (pDeal.getFirstPlayer() == iSecondPlayer and pDeal.getSecondPlayer() == iFirstPlayer):
				lDeals.append(pDeal)
				
		return lDeals
		
	def getAllDealsType(self, iFirstPlayer, iSecondPlayer, iTradeableItem):
		lDeals = []
	
		for pDeal in self.getAllDeals(iFirstPlayer, iSecondPlayer):
			for j in range(pDeal.getLengthFirstTrades()):
				if pDeal.getFirstTrade(j).ItemType == iTradeableItem:
					lDeals.append(pDeal)
					
		return lDeals
		
	def getReligiousVictoryType(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		iStateReligion = pPlayer.getStateReligion()
		
		if iStateReligion >= 0:
			return iStateReligion
		elif pPlayer.getCivics(4) == con.iCivicPantheon:
			return con.iVictoryPolytheism
		elif pPlayer.getCivics(4) == con.iCivicSecularism:
			return con.iVictorySecularism
			
		return -1
		
	def getApprovalRating(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		
		if not pPlayer.isAlive(): return 0
		
		iHappy = pPlayer.calculateTotalCityHappiness()
		iUnhappy = pPlayer.calculateTotalCityUnhappiness()
		
		return (iHappy * 100) / max(1, iHappy + iUnhappy)
		
	def getLifeExpectancyRating(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		
		if not pPlayer.isAlive(): return 0
		
		iHealthy = pPlayer.calculateTotalCityHealthiness()
		iUnhealthy = pPlayer.calculateTotalCityUnhealthiness()
		
		return (iHealthy * 100) / max(1, iHealthy + iUnhealthy)
		
	# Leoreth: Byzantine UP: bribe barbarian units
	def doByzantineBribery(self, spy):
		localText = CyTranslator()
		plot = CyMap().plot(spy.getX(), spy.getY())
		unitList = [plot.getUnit(i) for i in range(plot.getNumUnits())]
		targetList = []
		iTreasury = gc.getPlayer(con.iByzantium).getGold()
		
		# get pairs of units with their bribe costs
		for unit in unitList:
			iCost = gc.getUnitInfo(unit.getUnitType()).getProductionCost() * 2
			if unit.getOwner() == con.iBarbarian and iCost <= iTreasury:
				targetList.append((unit, iCost))
				
		# only once per turn
		spy.finishMoves()
				
		# launch popup
		popup = Popup.PyPopup(7629, EventContextTypes.EVENTCONTEXT_ALL)
		sd.setByzantineBribes(targetList)
		popup.setHeaderString(localText.getText("TXT_KEY_BYZANTINE_UP_TITLE", ()))
		popup.setBodyString(localText.getText("TXT_KEY_BYZANTINE_UP_BODY", ()))
		
		for tTuple in targetList:
			unit, iCost = tTuple
			popup.addButton(localText.getText("TXT_KEY_BYZANTINE_UP_BUTTON", (unit.getName(), iCost)))
			
		popup.addButton(localText.getText("TXT_KEY_BYZANTINE_UP_BUTTON_NONE", ()))

		popup.launch(False)
		
	def linreg(self, lTuples):
		n = len(lTuples)
		
		if n < 2: return 0.0, 0.0
		
		Sx = Sy = Sxx = Syy = Sxy = 0.0
		for x, y in lTuples:
			Sx += x
			Sy += y
			Sxx += x*x
			Syy += y*y
			Sxy += x*y
			
		det = n * Sxx - Sx * Sx		
		a, b = (n * Sxy - Sy * Sx) / det, (Sxx * Sy - Sx * Sxy) / det
		
		#meanerror = residual = 0.0
		#for x, y in zip(lx, ly):
		#	meanerror += (y - Sy/n)**2
		#	residual += (y - a * x - b)**2
			
		#RR = 1 - residual/meanerror
		
		return a, b
		
	def canRespawn(self, iPlayer):
		iGameTurn = gc.getGame().getGameTurn()
		bPossible = False
		
		# no respawn before spawn
		if iGameTurn < getTurnForYear(con.tBirth[iPlayer]) + 10: return False
		
		# only dead civ need to check for resurrection
		if gc.getPlayer(iPlayer).isAlive(): return False
			
		# check if only recently died
		if iGameTurn - self.getLastTurnAlive(iPlayer) < self.getTurns(10): return False
		
		# check if the civ can be reborn at this date
		if len(con.tResurrectionIntervals[iPlayer]) > 0:
			for tInterval in con.tResurrectionIntervals[iPlayer]:
				iStart, iEnd = tInterval
				if getTurnForYear(iStart) <= iGameTurn <= getTurnForYear(iEnd):
					bPossible = True
					break
					
		# Thailand cannot respawn when Khmer is alive and vice versa
		if iPlayer == con.iThailand and gc.getPlayer(con.iKhmer).isAlive(): bPossible = False
		if iPlayer == con.iKhmer and gc.getPlayer(con.iThailand).isAlive(): bPossible = False
		
		# Rome cannot respawn when Italy is alive and vice versa
		if iPlayer == con.iRome and gc.getPlayer(con.iItaly).isAlive(): bPossible = False
		if iPlayer == con.iItaly and gc.getPlayer(con.iRome).isAlive(): bPossible = False
		
		# Greece cannot respawn when Byzantium is alive and vice versa
		if iPlayer == con.iGreece and gc.getPlayer(con.iByzantium).isAlive(): bPossible = False
		if iPlayer == con.iByzantium and gc.getPlayer(con.iGreece).isAlive(): bPossible = False
		
		# India cannot respawn when Mughals are alive (not vice versa -> Pakistan)
		if iPlayer == con.iIndia and gc.getPlayer(con.iMughals).isAlive(): bPossible = False
		
		if bPossible and not gc.getPlayer(iPlayer).isAlive() and iGameTurn > self.getLastTurnAlive(iPlayer) + self.getTurns(20):
			if con.tRebirth[iPlayer] == -1 or iGameTurn > getTurnForYear(con.tRebirth[iPlayer]) + 10:
				return True
				
		return False
		
	def canEverRespawn(self, iPlayer, iGameTurn = gc.getGame().getGameTurn()):
		iNumIntervals = len(con.tResurrectionIntervals[iPlayer])
		
		if iNumIntervals == 0:
			return False
		else:
			iStart, iEnd = con.tResurrectionIntervals[iPlayer][iNumIntervals-1]
			if getTurnForYear(iEnd) < iGameTurn:
				return False
				
		return True

	# Leoreth: returns True if function returns True for at least one member, otherwise False	
	def satisfies(self, lList, function):
		for element in lList:
			if function(element): return True
		return False
		
	def moveToClosestCity(self, unit):
		city = gc.getMap().findCity(unit.getX(), unit.getY(), unit.getOwner(), TeamTypes.NO_TEAM, False, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, CyCity())
		x = city.getX()
		y = city.getY()
		
		if x < 0 or y < 0: unit.kill(False, -1)
		else: unit.setXY(x, y, False, True, False)
		
	def evacuate(self, tPlot):
		x, y = tPlot		
		lUnits = []
		for i in (x-1, x, x+1):
			for j in (y-1, y, y+1):
				plot = gc.getMap().plot(i, j)
				for k in range(plot.getNumUnits()):
					unit = plot.getUnit(k)
					lUnits.append(unit)
			
		for unit in lUnits:
			self.moveToClosestCity(unit)
			
	def getWonderList():
		return [i for i in range(iNumBuildings) if isWorldWonderClass(gc.getBuildingInfo(i).getBuildingClassType())]
		
	def getOrElse(self, dDictionary, key, default):
		if key in dDictionary: return dDictionary[key]
		return default
		
	def setReborn(self, iPlayer, bReborn):
		pPlayer = gc.getPlayer(iPlayer)
		
		if pPlayer.isReborn() == bReborn: return
	
		pPlayer.setReborn(bReborn)
		
		Areas.updateCore(iPlayer)
		SettlerMaps.updateMap(iPlayer, bReborn)
		WarMaps.updateMap(iPlayer, bReborn)

	def toggleStabilityOverlay(self, iPlayer = -1):
		engine = CyEngine()
		map = CyMap()

		bWB = False
		if iPlayer == -1:
			iPlayer = self.getHumanID()
		else:
			bWB = True
			
		self.removeStabilityOverlay()
			
		if self.bStabilityOverlay and not bWB:
			self.bStabilityOverlay = False
			CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE).setState("StabilityOverlay", False)
			return

		self.bStabilityOverlay = True
		CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE).setState("StabilityOverlay", True)

		iTeam = gc.getPlayer(iPlayer).getTeam()

		# apply the highlight
		for i in range(map.numPlots()):
			plot = map.plotByIndex(i)
			tPlot = (plot.getX(), plot.getY())
			if gc.getGame().isDebugMode() or plot.isRevealed(iTeam, False):
				if plot.isWater(): continue
				if plot.isCore(iPlayer):
					iPlotType = con.iCore
				else:
					iSettlerValue = plot.getSettlerValue(iPlayer)
					if bWB and iSettlerValue == 3:
						iPlotType = con.iAIForbidden
					elif iSettlerValue >= 90:
						if Areas.isForeignCore(iPlayer, tPlot):
							iPlotType = con.iContest
						else:
							iPlotType = con.iHistorical
					elif Areas.isForeignCore(iPlayer, tPlot):
						iPlotType = con.iForeignCore
					else:
						iPlotType = -1
				if iPlotType != -1:
					szColor = con.lStabilityColors[iPlotType]
					engine.fillAreaBorderPlotAlt(plot.getX(), plot.getY(), 1000+iPlotType, szColor, 0.7)
					
	def removeStabilityOverlay(self):
		engine = CyEngine()
		# clear the highlight
		for i in range(max(con.iNumPlotStabilityTypes, con.iMaxWarValue/2)):
			engine.clearAreaBorderPlots(1000+i)
			
	def getRegionCities(self, lRegions):
		lCities = []
		for (x, y) in [(x, y) for x in range(con.iWorldX) for y in range(con.iWorldY)]:
			plot = gc.getMap().plot(x, y)
			if plot.getRegionID() in lRegions and plot.isCity():
				lCities.append(plot.getPlotCity())
		return lCities
		
	def getAdvisorString(self, iBuilding):
		''
		iAdvisor = gc.getBuildingInfo(iBuilding).getAdvisorType()

		if iAdvisor == 0:
			return "Military"
		elif iAdvisor == 1:
			return "Religious"
		elif iAdvisor == 2:
			return "Economy"
		elif iAdvisor == 3:
			return "Science"
		elif iAdvisor == 4:
			return "Culture"
		elif iAdvisor == 5:
			return "Growth"

		return ""
		
	def getBuildingCategory(self, iBuilding):
		'0 = Building'
		'1 = Religious Building'
		'2 = Unique Building'
		'3 = National Wonder'
		'4 = World Wonder'

		BuildingInfo = gc.getBuildingInfo(iBuilding)
		if BuildingInfo.isGraphicalOnly():
			return -1
		elif BuildingInfo.getReligionType() > -1:
			return 1
		elif isWorldWonderClass(BuildingInfo.getBuildingClassType()):
			return 4
		else:
			iBuildingClass = BuildingInfo.getBuildingClassType()
			iDefaultBuilding = gc.getBuildingClassInfo(iBuildingClass).getDefaultBuildingIndex()
			if isNationalWonderClass(iBuildingClass):
				return 3
			else:
				if iDefaultBuilding > -1 and iDefaultBuilding != iBuilding:
					return 2
				else:
					return 0
					
	def getLeaderCiv(self, iLeader):
		for iCiv in range(gc.getNumCivilizationInfos()):
			civ = gc.getCivilizationInfo(iCiv)
			if civ.isLeaders(iLeader):
				return iCiv
		return None
		
	def setStateReligionBeforeBirth(self, lPlayers, iReligion):
		for iPlayer in lPlayers:
			if gc.getGame().getGameTurn() < getTurnForYear(con.tBirth[iPlayer]) and gc.getPlayer(iPlayer).getStateReligion() != iReligion:
				gc.getPlayer(iPlayer).setLastStateReligion(iReligion)
				
	def playerNames(self, lPlayers):
		return str([gc.getPlayer(iPlayer).getCivilizationShortDescription(0) for iPlayer in lPlayers])

utils = RFCUtils()