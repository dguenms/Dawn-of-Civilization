# Rhye's and Fall of Civilization - Utilities

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import Popup
from Consts import *
from StoredData import data
import BugCore
import Areas
import SettlerMaps
import WarMaps
import CvScreenEnums

# globals
MainOpt = BugCore.game.MainInterface
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
localText = CyTranslator()

tCol = (
'255,255,255',
'200,200,200',
'150,150,150',
'128,128,128'
)

lChineseCities = [(102, 47), (103, 44), (103, 43), (106, 44), (107, 43), (105, 39), (104, 39)]
# Beijing, Kaifeng, Luoyang, Shanghai, Hangzhou, Guangzhou, Haojing

class RFCUtils:
	bStabilityOverlay = False

	#Victory
	def countAchievedGoals(self, iPlayer):
		iResult = 0
		for iGoal in range(3):
			if data.players[iPlayer].lGoals[iGoal] == 1:
				iResult += 1
		return iResult


	#Plague
	def getRandomCity(self, iPlayer):
		return self.getRandomEntry(self.getCityList(iPlayer))

	# Leoreth - finds an adjacent land plot without enemy units that's closest to the player's capital (for the Roman UP)
	def findNearestLandPlot(self, tPlot, iPlayer):
		plotList = []

		for (x, y) in self.surroundingPlots(tPlot):
			pPlot = gc.getMap().plot(x, y)
			if not pPlot.isWater() and not pPlot.isPeak():
				if not pPlot.isUnit():
					plotList.append((x, y))

		if plotList:
			return self.getRandomEntry(plotList)
		# if no plot is found, return that player's capital
		return Areas.getCapital(iPlayer)



	def isMortalUnit(self, unit):
		if unit.getUpgradeDiscount() >= 100: return False
		
		if gc.getUnitInfo(unit.getUnitType()).isMechUnit(): return False
		
		if not unit.canFight(): return False
		
		return True

	def isDefenderUnit(self, unit):
		iUnitType = unit.getUnitType()
		pUnitInfo = gc.getUnitInfo(iUnitType)
		
		if not pUnitInfo: return False
		
		# Archery units with city defense
		if pUnitInfo.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_ARCHER") and pUnitInfo.getCityDefenseModifier() > 0:
			return True
			
		# Melee units with mounted modifiers
		if pUnitInfo.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_MELEE") and pUnitInfo.getUnitCombatModifier(gc.getInfoTypeForString("UNITCOMBAT_HEAVY_CAVALRY")) > 0:
			return True
			
		# Conscriptable gunpowder units
		if pUnitInfo.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_GUN") and pUnitInfo.getConscriptionValue() > 1:
			return True
			
		return False

	#AIWars
	def checkUnitsInEnemyTerritory(self, iCiv1, iCiv2): 
		unitList = PyPlayer(iCiv1).getUnitList()
		if unitList:
			for unit in unitList:
				iX = unit.getX()
				iY = unit.getY()
				if gc.getMap().plot( iX, iY ).getOwner() == iCiv2:
					return True
		return False

	#AIWars
	def restorePeaceAI(self, iMinorCiv, bOpenBorders):
		teamMinor = gc.getTeam(gc.getPlayer(iMinorCiv).getTeam())
		for iActiveCiv in range(iNumActivePlayers):
			if gc.getPlayer(iActiveCiv).isAlive() and not gc.getPlayer(iActiveCiv).isHuman():
				if teamMinor.isAtWar(iActiveCiv):
					bActiveUnitsInIndependentTerritory = self.checkUnitsInEnemyTerritory(iActiveCiv, iMinorCiv)
					bIndependentUnitsInActiveTerritory = self.checkUnitsInEnemyTerritory(iMinorCiv, iActiveCiv)
					if not bActiveUnitsInIndependentTerritory and not bIndependentUnitsInActiveTerritory:
						teamMinor.makePeace(iActiveCiv)
						if bOpenBorders:
							teamMinor.signOpenBorders(iActiveCiv)
	
	#AIWars
	def restorePeaceHuman(self, iMinorCiv, bOpenBorders): 
		teamMinor = gc.getTeam(gc.getPlayer(iMinorCiv).getTeam())
		iHuman = self.getHumanID()
		if gc.getPlayer(iHuman).isAlive():
			if teamMinor.isAtWar(iHuman):
				bActiveUnitsInIndependentTerritory = self.checkUnitsInEnemyTerritory(iHuman, iMinorCiv)
				bIndependentUnitsInActiveTerritory = self.checkUnitsInEnemyTerritory(iMinorCiv, iHuman)
				if not bActiveUnitsInIndependentTerritory and not bIndependentUnitsInActiveTerritory:
					teamMinor.makePeace(iHuman)
	
	#AIWars
	def minorWars(self, iMinorCiv):
		teamMinor = gc.getTeam(gc.getPlayer(iMinorCiv).getTeam())
		for city in self.getCityList(iMinorCiv):
			x = city.getX()
			y = city.getY()
			for iActiveCiv in range(iNumActivePlayers):
				if gc.getPlayer(iActiveCiv).isAlive() and not gc.getPlayer(iActiveCiv).isHuman():
					if gc.getPlayer(iActiveCiv).getSettlerValue(x, y) >= 90 or gc.getPlayer(iActiveCiv).getWarValue(x, y) >= 6:
						if not teamMinor.isAtWar(iActiveCiv):
							teamMinor.declareWar(iActiveCiv, False, WarPlanTypes.WARPLAN_LIMITED)
							print ("Minor war", city.getName(), gc.getPlayer(iActiveCiv).getCivilizationAdjective(0))


	#RiseAndFall, Stability
	def calculateDistance(self, x1, y1, x2, y2):
		dx = abs(x2-x1)
		dy = abs(y2-y1)
		return max(dx, dy)

	def calculateDistanceTuples(self, t1, t2):
		return self.calculateDistance(t1[0], t1[1], t2[0], t2[1])
		
	def minimalDistance(self, tuple, list, entryFunction = lambda x: True):
		return self.getHighestEntry([self.calculateDistanceTuples(tuple, x) for x in list if entryFunction(x)], lambda x: -x)

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
		for iTech in range(iNumTechs):
			if gc.getTeam(gc.getPlayer(iMajorCiv).getTeam()).isHasTech(iTech):
					gc.getTeam(gc.getPlayer(iMinorCiv).getTeam()).setHasTech(iTech, True, iMinorCiv, False, False)


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

	def makeUnitAI(self, iUnit, iPlayer, tCoords, iAI, iNum, sAdj=""): #by LOQ, modified by Leoreth
		'Makes iNum units for player iPlayer of the type iUnit at tCoords.'
		for i in range(iNum):
			player = gc.getPlayer(iPlayer)
			unit = player.initUnit(iUnit, tCoords[0], tCoords[1], iAI, DirectionTypes.DIRECTION_SOUTH)
			if sAdj != "":
				unit.setName(CyTranslator().getText(sAdj, ()) + ' ' + unit.getName())

	#RiseAndFall, Religions, Congresses
	def getHumanID(self):
		return gc.getGame().getActivePlayer()



	#RiseAndFall
	def flipUnitsInCityBefore(self, tCityPlot, iNewOwner, iOldOwner):
		#print ("tCityPlot Before", tCityPlot)
		plotCity = gc.getMap().plot(tCityPlot[0], tCityPlot[1])
		iNumUnitsInAPlot = plotCity.getNumUnits()
		if iNumUnitsInAPlot > 0:
			lFlipUnits = []
			for iUnit in reversed(range(iNumUnitsInAPlot)):
				unit = plotCity.getUnit(iUnit)
				iUnitType = unit.getUnitType()
				if unit.getOwner() == iOldOwner:
					unit.kill(False, iBarbarian)
					if iNewOwner < iNumActivePlayers or iUnitType > iSettler:
						lFlipUnits.append(iUnitType)
			data.lFlippingUnits = lFlipUnits

	#RiseAndFall
	def flipUnitsInCityAfter(self, tCityPlot, iCiv):
		#moves new units back in their place
		print ("tCityPlot After", tCityPlot)
		lFlipUnits = data.lFlippingUnits
		if lFlipUnits:
			for iUnitType in lFlipUnits:
				self.makeUnit(iUnitType, iCiv, tCityPlot, 1)
			data.lFlippingUnits = []

	def killUnitsInArea(self, iPlayer, lPlots):
		for (x, y) in lPlots:
			lUnits = []
			plot = gc.getMap().plot(x, y)
			iNumUnits = plot.getNumUnits()
			if iNumUnits > 0:
				for iUnit in range(iNumUnits):
					unit = plot.getUnit(iUnit)
					if unit.getOwner() == iPlayer:
						lUnits.append(unit)
			for unit in lUnits:
				unit.kill(False, iBarbarian)

	#RiseAndFall
	def flipUnitsInArea(self, lPlots, iNewOwner, iOldOwner, bSkipPlotCity, bKillSettlers):
		"""Creates a list of all flipping units, deletes old ones and places new ones
		If bSkipPlotCity is True, units in a city won't flip. This is to avoid converting barbarian units that would capture a city before the flip delay"""
		oldCapital = gc.getPlayer(iOldOwner).getCapitalCity()
		
		for (x, y) in lPlots:
			killPlot = gc.getMap().plot(x, y)
			if bSkipPlotCity and killPlot.isCity():
				#print (killPlot.isCity())
				#print 'do nothing'
				continue
			lPlotUnits = []
			iNumUnitsInAPlot = killPlot.getNumUnits()
			if iNumUnitsInAPlot > 0:
				#print ("killplot", x, y)
				for iUnit in reversed(range(iNumUnitsInAPlot)):
					unit = killPlot.getUnit(iUnit)
					#print ("killplot", x, y, unit.getUnitType(), unit.getOwner(), "j", j)
					if unit.getOwner() == iOldOwner:
						# Leoreth: Italy shouldn't flip so it doesn't get too strong by absorbing French or German armies attacking Rome
						if iNewOwner == iItaly and iOldOwner < iNumPlayers:
							unit.setXY(oldCapital.getX(), oldCapital.getY(), False, True, False)
						else:
							unit.kill(False, iBarbarian)
							
							# Leoreth: can't flip naval units anymore
							if unit.getDomainType() == DomainTypes.DOMAIN_SEA:
								continue
								
							# Leoreth: ignore workers as well
							if utils.getBaseUnit(unit.getUnitType()) in [iWorker, iLabourer]:
								continue
							
							if not (unit.isFound() and not bKillSettlers) and not unit.isAnimal():
								lPlotUnits.append(unit.getUnitType())
			if lPlotUnits:
				for iUnit in lPlotUnits:
					self.makeUnit(iUnit, iNewOwner, (x, y), 1)

	#Congresses, RiseAndFall
	def flipCity(self, tCityPlot, bFlipType, bKillUnits, iNewOwner, iOldOwners):
		"""Changes owner of city specified by tCityPlot.
		bFlipType specifies if it's conquered or traded.
		If bKillUnits != 0 all the units in the city will be killed.
		iRetainCulture will determine the split of the current culture between old and new owner. -1 will skip
		iOldOwners is a list. Flip happens only if the old owner is in the list.
		An empty list will cause the flip to always happen."""
		pNewOwner = gc.getPlayer(iNewOwner)
		if gc.getMap().plot(tCityPlot[0], tCityPlot[1]).isCity():
			city = gc.getMap().plot(tCityPlot[0], tCityPlot[1]).getPlotCity()
			if not city.isNone():
				iOldOwner = city.getOwner()
				if iOldOwner in iOldOwners or not iOldOwners:

					if bKillUnits:
						killPlot = gc.getMap().plot( tCityPlot[0], tCityPlot[1] )
						for i in range(killPlot.getNumUnits()):
							unit = killPlot.getUnit(0)
							unit.kill(False, iNewOwner)
							
					if bFlipType: #conquest
						if city.getPopulation() <= 2:
							city.changePopulation(1)
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

		#city
		if gc.getMap().plot(tCityPlot[0], tCityPlot[1]).isCity():
			city = gc.getMap().plot(tCityPlot[0], tCityPlot[1]).getPlotCity()
			iCurrentCityCulture = city.getCulture(iOldOwner)
			city.setCulture(iOldOwner, iCurrentCityCulture*(100-iCulturePercent)/100, False)
			if iNewOwner != iBarbarian:
				city.setCulture(iBarbarian, 0, True)
			city.setCulture(iNewOwner, iCurrentCityCulture*iCulturePercent/100, False)
			if city.getCulture(iNewOwner) <= 10:
				city.setCulture(iNewOwner, 20, False)

		#halve barbarian culture in a broader area
		if bBarbarian2x2Decay or bBarbarian2x2Conversion:
			if iNewOwner not in [iBarbarian, iIndependent, iIndependent2]:
				for (x, y) in self.surroundingPlots(tCityPlot, 2):
					bCity = gc.getMap().plot(x, y).getPlotCity().isNone() or (x, y) == tCityPlot
					if bCity:
						for iMinor in [iBarbarian, iIndependent, iIndependent2]:
							iMinorCulture = gc.getMap().plot(x, y).getCulture(iMinor)
							if iMinorCulture > 0:
								if bBarbarian2x2Decay:
									gc.getMap().plot(x, y).setCulture(iMinor, iMinorCulture/4, True)
								if bBarbarian2x2Conversion:
									gc.getMap().plot(x, y).setCulture(iMinor, 0, True)
									gc.getMap().plot(x, y).setCulture(iNewOwner, iMinorCulture, True)
									
		#plot
		for (x, y) in self.surroundingPlots(tCityPlot):
			pPlot = gc.getMap().plot(x, y)
			
			iCurrentPlotCulture = pPlot.getCulture(iOldOwner)

			if pPlot.isCity():
				pPlot.setCulture(iNewOwner, iCurrentPlotCulture*iCulturePercent/100, True)
				pPlot.setCulture(iOldOwner, iCurrentPlotCulture*(100-iCulturePercent)/100, True)
			else:
				pPlot.setCulture(iNewOwner, iCurrentPlotCulture*iCulturePercent/3/100, True)
				pPlot.setCulture(iOldOwner, iCurrentPlotCulture*(100-iCulturePercent/3)/100, True)
				
				if bAlwaysOwnPlots:
					pPlot.setOwner(iNewOwner)
				else:
					if pPlot.getCulture(iNewOwner)*4 > pPlot.getCulture(iOldOwner):
						pPlot.setOwner(iNewOwner)
				#print ("NewOwner", pPlot.getOwner())
						
			#print (x, y, pPlot.getCulture(iNewOwner), ">", pPlot.getCulture(iOldOwner))



	#handler
	def spreadMajorCulture(self, iMajorCiv, tPlot):
		for (x, y) in self.surroundingPlots(tPlot, 3):
			pPlot = gc.getMap().plot(x, y)
			if pPlot.isCity():
				city = pPlot.getPlotCity()
				if city.getOwner() >= iNumMajorPlayers:
					iMinor = city.getOwner()
					iDen = 25
					if gc.getPlayer(iMajorCiv).getSettlerValue(x, y) >= 400:
						iDen = 10
					elif gc.getPlayer(iMajorCiv).getSettlerValue(x, y) >= 150:
						iDen = 15
						
					iMinorCityCulture = city.getCulture(iMinor)
					city.setCulture(iMajorCiv, iMinorCityCulture/iDen, True)
					
					iMinorPlotCulture = pPlot.getCulture(iMinor)
					pPlot.setCulture(iMajorCiv, iMinorPlotCulture/iDen, True)

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
		
		if bOwner:
			plot.setOwner(iPlayer)

	#DynamicCivs
	def getMaster(self, iCiv):
		team = gc.getTeam(gc.getPlayer(iCiv).getTeam())
		if team.isAVassal():
			for iMaster in range(iNumTotalPlayers):
				if team.isVassal(iMaster):
					return iMaster
		return -1


	#Congresses, RiseAndFall
	def pushOutGarrisons(self, tCityPlot, iOldOwner):
		x, y = tCityPlot
		tDestination = (-1, -1)
		for (i, j) in self.surroundingPlots(tCityPlot, 2, lambda tPlot: tPlot == tCityPlot):
			pDestination = gc.getMap().plot(i, j)
			if pDestination.getOwner() == iOldOwner and not pDestination.isWater() and not pDestination.isImpassable():
				tDestination = (i, j)
				break
		if tDestination != (-1, -1):
			plotCity = gc.getMap().plot(x, y)
			iNumUnitsInAPlot = plotCity.getNumUnits()
			for iUnit in reversed(range(iNumUnitsInAPlot)):
				unit = plotCity.getUnit(iUnit)
				if unit.getDomainType() == DomainTypes.DOMAIN_LAND:
					unit.setXY(tDestination[0], tDestination[1], False, True, False)

	def relocateGarrisons(self, tCityPlot, iOldOwner):
		x, y = tCityPlot
		if iOldOwner < iNumPlayers:
			pCity = self.getRandomEntry([city for city in self.getCityList(iOldOwner) if (city.getX(), city.getY()) != tCityPlot])
			if pCity:
				plot = gc.getMap().plot(x, y)
				iNumUnits = plot.getNumUnits()
				for iUnit in reversed(range(iNumUnits)):
					unit = plot.getUnit(iUnit)
					if unit.getDomainType() == DomainTypes.DOMAIN_LAND:
						unit.setXY(pCity.getX(), pCity.getY(), False, True, False)
		else:
			plot = gc.getMap().plot(x, y)
			iNumUnits = plot.getNumUnits()
			for i in range(iNumUnits):
				unit = plot.getUnit(0)
				unit.kill(False, iOldOwner)
				
	def removeCoreUnits(self, iPlayer):
		for (x, y) in Areas.getBirthArea(iPlayer):
			plot = gc.getMap().plot(x, y)
			if plot.isCity():
				pCity = plot.getPlotCity()
				if pCity.getOwner() != iPlayer:
					self.relocateGarrisons((x, y), pCity.getOwner())
					self.relocateSeaGarrisons((x, y), pCity.getOwner())
					self.createGarrisons((x, y), pCity.getOwner(), 2)
			else:
				iNumUnits = plot.getNumUnits()
				for iUnit in reversed(range(iNumUnits)):
					unit = plot.getUnit(iUnit)
					iOwner = unit.getOwner()
					if iOwner < iNumPlayers and iOwner != iPlayer:
						capital = gc.getPlayer(iOwner).getCapitalCity()
						if capital.getX() != -1 and capital.getY() != -1:
							print "SETXY utils 4"
							unit.setXY(capital.getX(), capital.getY(), False, True, False)
				
	#Congresses, RiseAndFall
	def relocateSeaGarrisons(self, tCityPlot, iOldOwner):
		x, y = tCityPlot
		tDestination = (-1, -1)
		for city in self.getCityList(iOldOwner):
			if city.isCoastalOld() and (city.getX(), city.getY()) != tCityPlot:
				tDestination = (city.getX(), city.getY())
		if tDestination != (-1, -1):
			plotCity = gc.getMap().plot(x, y)
			iNumUnitsInAPlot = plotCity.getNumUnits()
			for iUnit in reversed(range(iNumUnitsInAPlot)):
				unit = plotCity.getUnit(iUnit)
				if unit.getOwner() == iOldOwner and unit.getDomainType() == DomainTypes.DOMAIN_SEA:
					unit.setXY(tDestination[0], tDestination[1], False, True, False)


	#Congresses, RiseAndFall
	def createGarrisons(self, tCityPlot, iNewOwner, iNumUnits):
		x, y = tCityPlot
		#plotCity = gc.getMap().plot(x, y)
		#iNumUnitsInAPlot = plotCity.getNumUnits()

		iUnitType = self.getBestDefender(iNewOwner)

		self.makeUnit(iUnitType, iNewOwner, (x, y), iNumUnits)


	def resetUHV(self, iPlayer):
		if iPlayer < iNumMajorPlayers:
			for i in range(3):
				if data.players[iPlayer].lGoals[i] == -1:
					data.players[iPlayer].lGoals[i] = 0

	def clearPlague(self, iCiv):
		for city in self.getCityList(iCiv):
			if city.hasBuilding(iPlague):
				city.setHasRealBuilding(iPlague, False)


	#AIWars, by CyberChrist

	def isAVassal(self, iCiv):
		return gc.getTeam(gc.getPlayer(iCiv).getTeam()).isAVassal()

	#Barbs, RiseAndFall
	def squareSearch(self, tTopLeft, tBottomRight, function, argsList, tExceptions = ()): #by LOQ
		"""Searches all tile in the square from tTopLeft to tBottomRight and calls function for
		every tile, passing argsList. The function called must return a tuple: (1) a (2) if
		a plot should be painted and (3) if the search should continue."""
		return self.listSearch(self.getPlotList(tTopLeft, tBottomRight, tExceptions), function, argsList)
		
	def listSearch(self, lPlots, function, argsList):
		tPaintedList = []
		for tPlot in lPlots:
			bPaintPlot = function(tPlot, argsList)
			if bPaintPlot: # paint plot
				tPaintedList.append(tPlot)
		return tPaintedList

	#Barbs, RiseAndFall
	def outerInvasion(self, tCoords, argsList):
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it's hill or flatlands, it isn't marsh or jungle, it isn't occupied by a unit or city and if it isn't a civ's territory"""
		return self.invasion(tCoords, argsList, True)
	
	def invasion(self, tCoords, argsList, bOuter):
		x, y = tCoords
		pPlot = gc.getMap().plot(x, y)
		if pPlot.isHills() or pPlot.isFlatlands():
			if pPlot.getTerrainType() != iMarsh and pPlot.getFeatureType() != iJungle:
				if not pPlot.isCity() and not pPlot.isUnit():
					if not (bOuter and pPlot.countTotalCulture() != 0):
						return True
		return False

	#Barbs
	def innerSeaSpawn(self, tCoords, argsList): # Unused
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it's water and it isn't occupied by any unit. Unit check extended to adjacent plots"""
		return self.seaSpawn(tCoords, argsList, False)

	def outerSeaSpawn(self, tCoords, argsList): # Unused
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it's water and it isn't occupied by any unit and if it isn't a civ's territory. Unit check extended to adjacent plots"""
		return self.seaSpawn(tCoords, argsList, True)
	
	def seaSpawn(self, tCoords, argsList, bOuter): # Used by unused functions
		x, y = tCoords
		pPlot = gc.getMap().plot(x, y)
		if pPlot.isWater():
			if not pPlot.isUnit() and pPlot.area().getNumTiles() > 10:
				if not (bOuter and pPlot.countTotalCulture() != 0):
					for (x, y) in self.surroundingPlots(tCoords):
						if pPlot.isUnit():
							return False
					return True
		return False

	def outerCoastSpawn(self, tCoords, argsList): # Unused
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it's water and it isn't occupied by any unit and if it isn't a civ's territory. Unit check extended to adjacent plots"""
		x, y = tCoords
		pPlot = gc.getMap().plot(x, y)
		if pPlot.getTerrainType() == iCoast:
			if not pPlot.isUnit() and pPlot.area().getNumTiles() > 10:
				if pPlot.countTotalCulture() == 0:
					for (x, y) in self.surroundingPlots(tCoords):
						if pPlot.isUnit():
							return False
					return True
		return False

	#Barbs
	def outerSpawn(self, tCoords, argsList): # Unused
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it's hill or flatlands, it isn't marsh or jungle, it isn't occupied by a unit or city and if it isn't a civ's territory.
		Unit check extended to adjacent plots"""
		return self.landSpawn(tCoords, argsList, True)
		
	def landSpawn(self, tCoords, argsList, bOuter):
		x, y = tCoords
		pPlot = gc.getMap().plot(x, y)
		if pPlot.isHills() or pPlot.isFlatlands():
			if pPlot.getTerrainType() != iMarsh and pPlot.getFeatureType() != iJungle:
				if not pPlot.isCity() and not pPlot.isUnit():
					for (x, y) in self.surroundingPlots(tCoords):
						if pPlot.isUnit():
							return False
					if bOuter:
						if pPlot.countTotalCulture() == 0:
							return True
					else:
						if pPlot.getOwner() in argsList:
							return True
		return False

	#RiseAndFall
	def innerInvasion(self, tCoords, argsList):
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it's hill or flatlands, it isn't marsh or jungle, it isn't occupied by a unit or city and if it isn't a civ's territory"""
		return self.invasion(tCoords, argsList, False)

	def internalInvasion(self, tCoords, argsList): # Unused
		"""Like inner invasion, but ignores territory, to allow for more barbarians"""
		x, y = tCoords
		pPlot = gc.getMap().plot(x, y)
		if pPlot.isHills() or pPlot.isFlatlands():
			if pPlot.getTerrainType() != iMarsh and pPlot.getFeatureType() != iJungle:
				if not pPlot.isCity() and not pPlot.isUnit():
					return True
		return False

	def innerSpawn(self, tCoords, argsList):
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it's hill or flatlands, it isn't marsh or jungle, it isn't occupied by a unit or city and if it isn't a civ's territory"""
		return self.landSpawn(tCoords, argsList, False)

	#RiseAndFall
	def goodPlots(self, tCoords, argsList):
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it's hill or flatlands, it isn't desert, tundra, marsh or jungle; it isn't occupied by a unit or city and if it isn't a civ's territory.
		Unit check extended to adjacent plots"""
		x, y = tCoords
		pPlot = gc.getMap().plot(x, y)
		if pPlot.isHills() or pPlot.isFlatlands():
			if not pPlot.isImpassable():
				if not pPlot.isUnit():
					if pPlot.getTerrainType() not in [iDesert, iTundra, iMarsh] and pPlot.getFeatureType() != iJungle:
						if pPlot.countTotalCulture() == 0:
							return True
		return False

	#RiseAndFall
	def cityPlots(self, tCoords, argsList):
		x, y = tCoords
		pPlot = gc.getMap().plot(x, y)
		if pPlot.isCity():
			return True
		return False

	def ownedCityPlots(self, tCoords, argsList):
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it contains a city belonging to the civ"""
		x, y = tCoords
		pPlot = gc.getMap().plot(x, y)
		if pPlot.getOwner() == argsList:
			if pPlot.isCity():
				return True
		return False

	def ownedCityPlotsAdjacentArea(self, tCoords, argsList): # Unused
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it contains a city belonging to the civ"""
		x, y = tCoords
		pPlot = gc.getMap().plot(x, y)
		#print(tCoords[0], tCoords[1], pPlot.isCity(), pPlot.getOwner() == argsList[0], pPlot.isAdjacentToArea(gc.getMap().plot(argsList[1][0],argsList[1][1]).area()))
		if pPlot.getOwner() == argsList[0] and pPlot.isAdjacentToArea(gc.getMap().plot(argsList[1][0],argsList[1][1]).area()):
			if pPlot.isCity():
				return True
		return False

	def foundedCityPlots(self, tCoords, argsList): # Unused
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it contains a city belonging to the civ"""
		x, y = tCoords
		pPlot = gc.getMap().plot(x, y)
		if pPlot.isCity():
			if pPlot.getPlotCity().getOriginalOwner() == argsList:
				return True
		return False

	def ownedPlots(self, tCoords, argsList): # Unused
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it is in civ's territory."""
		x, y = tCoords
		pPlot = gc.getMap().plot(x, y)
		if pPlot.getOwner() == argsList:
			return True
		return False

	def goodOwnedPlots(self, tCoords, argsList): # Unused
		"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
		Plot is valid if it's hill or flatlands; it isn't marsh or jungle, it isn't occupied by a unit and if it is in civ's territory."""
		x, y = tCoords
		pPlot = gc.getMap().plot(x, y)
		if pPlot.isHills() or pPlot.isFlatlands():
			if pPlot.getTerrainType() != iMarsh and pPlot.getFeatureType() != iJungle:
				if not pPlot.isCity() and not pPlot.isUnit():
						if pPlot.getOwner() == argsList:
							return True
		return False

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
		plotZero = gc.getMap().plot(0, 0)
		if plotZero.isUnit():
			catapult = plotZero.getUnit(0)
			catapult.kill(False, iCiv)
		for (x, y) in self.surroundingPlots((0, 0), 2):
			gc.getMap().plot(x, y).setRevealed(iCiv, False, True, -1)

	# Leoreth
	def getReborn(self, iCiv):
		return gc.getPlayer(iCiv).getReborn()

	# Leoreth
	def getCitiesInCore(self, iPlayer, bReborn=None):
		lCities = []
		for (x, y) in Areas.getCoreArea(iPlayer, bReborn):
			plot = gc.getMap().plot(x, y)
			if plot.isCity():
				lCities.append(plot.getPlotCity())
		return lCities
		
	def getOwnedCoreCities(self, iPlayer, bReborn=None):
		return [city for city in self.getCitiesInCore(iPlayer, bReborn) if city.getOwner() == iPlayer]

	# Leoreth
	def getCoreUnitList(self, iCiv, reborn):
		unitList = []
		for (x, y) in Areas.getCoreArea(iCiv, bReborn):
			plot = gc.getMap().plot(x,y)
			if not plot.isCity():
				for i in range(plot.getNumUnits()):
					unitList.append(plot.getUnit(i))
		return unitList

	def getCivRectangleCities(self, iCiv, tTL, tBR):
		cityList = []
		for (x, y) in self.getPlotList(tTL, tBR):
			plot = gc.getMap().plot(x,y)
			if plot.isCity():
				cityList.append(plot.getPlotCity())
		return cityList


	def removeReligionByArea(self, lPlotList, iReligion):
		lCityList = []
		for city in self.getAreaCities(lPlotList):
			if city.isHasReligion(iReligion) and not city.isHolyCity():
				city.setHasReligion(iReligion, False, False, False)
			if city.hasBuilding(iTemple + iReligion*4):
				city.setHasRealBuilding((iTemple + iReligion*4), False)
			if city.hasBuilding(iCathedral + iReligion*4):
				city.setHasRealBuilding((iCathedral + iReligion*4), False)
			if city.hasBuilding(iMonastery + iReligion*4):
				city.setHasRealBuilding((iMonastery + iReligion*4), False)

	def getEasternmostCity(self, iCiv):
		pResultCity = pPlayer.getCapitalCity()
		for city in self.getCityList(iCiv):
			if city.getX() > pResultCity.getX():
				pResultCity = city
		return pResultCity

	def getNorthernmostCity(self, iCiv):
		pResultCity = pPlayer.getCapitalCity()
		for city in self.getCityList(iCiv):
			if city.getY() > pResultCity.getY():
				pResultCity = city
		return pResultCity

	def getWesternmostCity(self, iCiv):
		pResultCity = pPlayer.getCapitalCity()
		for city in self.getCityList(iCiv):
			if city.getX() < pResultCity.getX():
				pResultCity = city
		return pResultCity

	def getFreeNeighborPlot(self, tPlot):
		plotList = []
		for (x, y) in self.surroundingPlots(tPlot):
			if (x, y) != tPlot:
				plot = gc.getMap().plot(x, y)
				if not plot.isPeak() and not plot.isWater() and not plot.isCity() and not plot.isUnit():
					plotList.append((x, y))
		return self.getRandomEntry(plotList)

	def colonialConquest(self, iCiv, tPlot):
		x, y = tPlot
		iTargetCiv = gc.getMap().plot(x, y).getPlotCity().getOwner()
		lFreePlots = []
		
		for (i, j) in self.surroundingPlots(tPlot):
			current = gc.getMap().plot(i, j)
			if not current.isCity() and not current.isPeak() and not current.isWater():
				#if not current.getFeatureType() == iJungle and not current.getTerrainType() == iMarsh:
				lFreePlots.append((i,j))
					
		if iTargetCiv != -1 and not gc.getTeam(iCiv).isAtWar(iTargetCiv):
			gc.getTeam(iCiv).declareWar(iTargetCiv, True, WarPlanTypes.WARPLAN_TOTAL)
			
		# independents too so the conquerors don't get pushed out in case the target collapses
		if not gc.getTeam(iCiv).isAtWar(iIndependent): gc.getTeam(iCiv).declareWar(iIndependent, True, WarPlanTypes.WARPLAN_LIMITED)
		if not gc.getTeam(iCiv).isAtWar(iIndependent2): gc.getTeam(iCiv).declareWar(iIndependent2, True, WarPlanTypes.WARPLAN_LIMITED)
			
		tTargetPlot = self.getRandomEntry(lFreePlots)
		
		if iCiv in [iSpain, iPortugal, iNetherlands]:
			iNumUnits = 2
		elif iCiv in [iFrance, iEngland]:
			iNumUnits = 3
			
		iSiege = self.getBestSiege(iCiv)
		iInfantry = self.getBestInfantry(iCiv)
		
		iExp = 0
		if self.getHumanID() != iCiv: iExp = 2
		
		if iSiege:
			self.makeUnit(iSiege, iCiv, tTargetPlot, iNumUnits, '', 2)
			
		if iInfantry:
			self.makeUnit(iInfantry, iCiv, tTargetPlot, 2*iNumUnits, '', 2)


	def colonialAcquisition(self, iCiv, tPlot):
		x, y = tPlot
		if iCiv in [iPortugal, iSpain]:
			iNumUnits = 1
		elif iCiv in [iFrance, iEngland, iNetherlands]:
			iNumUnits = 2
		if gc.getMap().plot(x, y).isCity():
			self.flipCity(tPlot, False, True, iCiv, [])
			self.makeUnit(iWorker, iCiv, tPlot, iNumUnits)
			iInfantry = self.getBestInfantry(iCiv)
			if iInfantry:
				self.makeUnit(iInfantry, iCiv, tPlot, iNumUnits)
			if gc.getPlayer(iCiv).getStateReligion() != -1:
				self.makeUnit(iMissionary+gc.getPlayer(iCiv).getStateReligion(), iCiv, (x, y), 1)
		else:
			gc.getMap().plot(x, y).setCulture(iCiv, 10, True)
			gc.getMap().plot(x, y).setOwner(iCiv)
			
			for (i, j) in utils.surroundingPlots((x, y)):
				plot = gc.getMap().plot(i, j)
				if (x, y) == (i, j):
					self.convertPlotCulture(plot, iCiv, 80, True)
				else:
					self.convertPlotCulture(plot, iCiv, 60, True)
					
			gc.getPlayer(iCiv).found(x, y)
			
			self.makeUnit(iWorker, iCiv, tPlot, 2)
			iInfantry = self.getBestInfantry(iCiv)
			if iInfantry:
				self.makeUnit(iInfantry, iCiv, tPlot, 2)
			if gc.getPlayer(iCiv).getStateReligion() != -1:
				self.makeUnit(iMissionary+gc.getPlayer(iCiv).getStateReligion(), iCiv, tPlot, 1)

	def getColonialTargets(self, iPlayer, bEmpty=False):
		if iPlayer == iSpain or iPlayer == iFrance:
			iNumCities = 1
		else:
			iNumCities = 3
			
		if iPlayer == iPortugal and self.getHumanID() != iPortugal:
			iNumCities = 5

		lCivList = [iSpain, iFrance, iEngland, iPortugal, iNetherlands]
		id = lCivList.index(iPlayer)

		lPlotList = tTradingCompanyPlotLists[id][:]

		cityList = []
		for tPlot in lPlotList:
			x, y = tPlot
			if gc.getMap().plot(x, y).isCity():
				if gc.getMap().plot(x, y).getPlotCity().getOwner() != iPlayer:
					cityList.append(tPlot)

		targetList = []

		if cityList:
			for i in range(iNumCities):
				iRand = gc.getGame().getSorenRandNum(len(cityList), 'Random city')
				print 'iRand = '+str(iRand)
				if len(cityList) > 0 and cityList[iRand] not in targetList:
					targetList.append(cityList[iRand])
					cityList.remove(cityList[iRand])

		if bEmpty:
			while len(targetList) < iNumCities and len(lPlotList) > 0:
				bValid = True
				iRand = gc.getGame().getSorenRandNum(len(lPlotList), 'Random free plot')
				tPlot = lPlotList[iRand]
				for (i, j) in self.surroundingPlots(tPlot):
					if gc.getMap().plot(i, j).isCity():
						bValid = False
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
		
	def getBorderPlots(self, iPlayer, tTL, tBR, iDirection = DirectionTypes.NO_DIRECTION, iNumPlots = 1):
		dConstraints = {
			DirectionTypes.NO_DIRECTION : lambda (x, y): 0,
			DirectionTypes.DIRECTION_EAST : lambda (x, y): x,
			DirectionTypes.DIRECTION_WEST : lambda (x, y): -x,
			DirectionTypes.DIRECTION_NORTH : lambda (x, y): y,
			DirectionTypes.DIRECTION_SOUTH : lambda (x, y): -y
		}
		
		constraint = dConstraints[iDirection]
	
		lPlots = self.getPlotList(tTL, tBR)
		lCities = self.getSortedList([city for city in self.getAreaCities(lPlots) if city.getOwner() == iPlayer], lambda city: constraint((city.getX(), city.getY())))
		
		lTargetCities = lCities[:iNumPlots]
		
		return [self.getPlotNearCityInDirection(city, constraint) for city in lTargetCities]
		
	def getPlotNearCityInDirection(self, city, constraint):
		tCityPlot = (city.getX(), city.getY())
		lFirstRing = self.surroundingPlots(tCityPlot)
		lSecondRing = [tPlot for tPlot in self.surroundingPlots(tCityPlot, 2) if not tPlot in lFirstRing and not gc.getMap().plot(tPlot[0], tPlot[1]).isCity()]
		
		lBorderPlots = [tPlot for tPlot in lSecondRing if constraint(tPlot) >= constraint(tCityPlot)and not gc.getMap().plot(tPlot[0], tPlot[1]).isWater()]
		
		return self.getRandomEntry(lBorderPlots)

	# Leoreth: return list of border plots in a given direction, -1 means all directions
	def getBorderPlotList(self, iCiv, iDirection):
		lPlotList = []
		
		for (x, y) in self.getWorldPlotsList():
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
		
		newCapital.setHasRealBuilding(iPalace, True)
		oldCapital.setHasRealBuilding(iPalace, False)
		
	def getFreePlot(self, tPlot):
		x, y = tPlot
		pPlot = gc.getMap().plot(x, y)
		lFreePlots = []
		
		if not (pPlot.isCity() or pPlot.isPeak() or pPlot.isWater()):
			return tPlot
			
		for (i, j) in self.surroundingPlots(tPlot):
			pPlot = gc.getMap().plot(i, j)
			if not (pPlot.isCity() or pPlot.isPeak() or pPlot.isWater()):
				lFreePlots.append((i, j))
		
		return self.getRandomEntry(lFreePlots)
		
	def surroundingPlots(self, tPlot, iRadius=1, filter=lambda (x, y): False):
		x, y = tPlot
		return [(i % iWorldX, j) for i in range(x-iRadius, x+iRadius+1) for j in range(y-iRadius, y+iRadius+1) if 0 <= j < iWorldY and not filter((i, j))]
		
	def getUnitList(self, tPlot):
		x, y = tPlot
		plot = gc.getMap().plot(x, y)
		
		return [plot.getUnit(i) for i in range(plot.getNumUnits())]
		
	def hasEnemyUnit(self, iPlayer, tPlot):
		for unit in self.getUnitList(tPlot):
			if gc.getTeam(gc.getPlayer(iPlayer).getTeam()).isAtWar(unit.getTeam()): return True
			
		return False
		
	def isFree(self, iPlayer, tPlot, bNoCity=False, bNoEnemyUnit=False, bCanEnter=False):
		x, y = tPlot
		plot = gc.getMap().plot(x, y)
		
		if bNoCity:
			isCity = lambda (i, j): gc.getMap().plot(i, j).isCity()
			if self.surroundingPlots(tPlot, filter=isCity):
				return False
				
		if bNoEnemyUnit:
			hasEnemyUnit = lambda (i, j): self.hasEnemyUnit(iPlayer, (i, j))
			if self.surroundingPlots(tPlot, filter=hasEnemyUnit):
				return False
			
		if bCanEnter:
			if plot.isPeak(): return False
			if plot.isWater(): return False
			if plot.getFeatureType() in [iMarsh, iJungle]: return False
			
		return True
		
	def handleChineseCities(self, pUnit):
		lCities = [(x, y) for (x, y) in lChineseCities if self.isFree(iChina, (x, y), True, True, True)]

		if lCities:
			x, y = self.getRandomEntry(lCities)
			gc.getPlayer(iChina).found(x, y)
			pUnit.kill(False, iBarbarian)
				
	def foundCapital(self, iPlayer, tPlot, sName, iSize, iCulture, lBuildings=[], lReligions=[], iScenario=False):
	
		if iScenario:
			if self.getScenario() != iScenario: return
		
		#if gc.getGame().getGameTurn() > getTurnForYear(tBirth[iPlayer])+3: return
		
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
		lEurope = [rBritain, rIberia, rEurope, rItaly, rScandinavia, rRussia, rBalkans, rAnatolia, rMaghreb]
		
		lColonies = []
		for city in self.getCityList(iPlayer):
			if city.getRegionID() not in lEurope:
				lColonies.append(city)
				
		if len(lColonies) == 0: return
		
		city = self.getRandomEnty(lColonies)
		
		unit.setXYOld(city.getX(), city.getY())
		
	def checkSlaves(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		
		if not pPlayer.canUseSlaves():
			for (x, y) in self.getWorldPlotsList():
				plot = gc.getMap().plot(x, y)
				if plot.getOwner() == iPlayer:
					if plot.getImprovementType() == iSlavePlantation:
						plot.setImprovementType(iPlantation)
					if plot.isCity():
						self.removeSlaves(plot.getPlotCity())
										
			lSlaves = []
			for unit in PyPlayer(iPlayer).getUnitList():
				if unit.getUnitClassType() == gc.getInfoTypeForString("UNITCLASS_SLAVE"):
					lSlaves.append(unit)
					
			for slave in lSlaves:
				slave.kill(False, iBarbarian)
			
	def removeSlaves(self, city):
		city.setFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_SLAVE"), 0)
		
	def freeSlaves(self, city, iPlayer):
		iNumSlaves = city.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_SLAVE"))
		if iNumSlaves > 0:
			city.setFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_SLAVE"), 0)
			self.makeUnit(gc.getUnitClassInfo(gc.getUnitInfo(iSlave).getUnitClassType()).getDefaultUnitIndex(), iPlayer, (city.getX(), city.getY()), iNumSlaves)
		
	def getRandomEntry(self, list):
		if not list: return None
		
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
		lInfantryList = [iInfantry, iRifleman, iMusketman, iArquebusier, iPikeman, iHeavySwordsman, iCrossbowman, iSwordsman, iLightSwordsman, iMilitia]
		
		for iBaseUnit in lInfantryList:
			iUnit = self.getUniqueUnitType(iPlayer, gc.getUnitInfo(iBaseUnit).getUnitClassType())
			if pPlayer.canTrain(iUnit, False, False):
				return iUnit
				
		return iMilitia
		
	def getBestCavalry(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		lCavalryList = [iCavalry, iDragoon, iHussar, iCuirassier, iPistolier, iLancer, iHorseArcher, iHorseman, iChariot]
		
		for iBaseUnit in lCavalryList:
			iUnit = self.getUniqueUnitType(iPlayer, gc.getUnitInfo(iBaseUnit).getUnitClassType())
			if pPlayer.canTrain(iUnit, False, False):
				return iUnit
				
		return iMilitia
		
	def getBestSiege(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		lSiegeList = [iHowitzer, iArtillery, iCannon, iBombard, iTrebuchet, iCatapult]
		
		for iBaseUnit in lSiegeList:
			iUnit = self.getUniqueUnitType(iPlayer, gc.getUnitInfo(iBaseUnit).getUnitClassType())
			if pPlayer.canTrain(iUnit, False, False):
				return iUnit
				
		return iMilitia
				
	def getBestCounter(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		lCounterList = [iMarine, iGrenadier, iPikeman, iHeavySpearman, iSpearman]
		
		for iBaseUnit in lCounterList:
			iUnit = self.getUniqueUnitType(iPlayer, gc.getUnitInfo(iBaseUnit).getUnitClassType())
			if pPlayer.canTrain(iUnit, False, False):
				return iUnit
				
		return iMilitia
		
	def getBestDefender(self, iPlayer):
		# Leoreth: there is a C++ error for barbarians for some reason, workaround by simply using independents
		if iPlayer == iBarbarian: iPlayer = iIndependent
		
		pPlayer = gc.getPlayer(iPlayer)
		lDefenderList = [iInfantry, iMachineGun, iRifleman, iMusketman, iArquebusier, iCrossbowman, iArcher, iMilitia]
		
		for iBaseUnit in lDefenderList:
			iUnit = self.getUniqueUnitType(iPlayer, gc.getUnitInfo(iBaseUnit).getUnitClassType())
			if pPlayer.canTrain(iUnit, False, False):
				return iUnit
				
		return iMilitia
		
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
		return [city for city in self.getAreaCities(lPlots) if city.getOwner() == iCiv]
		
	def completeCityFlip(self, x, y, iCiv, iOwner, iCultureChange, bBarbarianDecay = True, bBarbarianConversion = False, bAlwaysOwnPlots = False, bFlipUnits = False):
		tPlot = (x, y)
		plot = gc.getMap().plot(x, y)
		
		plot.setRevealed(iCiv, False, True, -1)
	
		self.cultureManager((x, y), iCultureChange, iCiv, iOwner, bBarbarianDecay, bBarbarianConversion, bAlwaysOwnPlots)
		
		if bFlipUnits: 
			self.flipUnitsInCityBefore(tPlot, iCiv, iOwner)
		else:
			self.pushOutGarrisons(tPlot, iOwner)
			self.relocateSeaGarrisons(tPlot, iOwner)
		
		self.flipCity(tPlot, 0, 0, iCiv, [iOwner])
		
		if bFlipUnits: 
			self.flipUnitsInCityAfter(tPlot, iCiv)
		else:
			self.createGarrisons(tPlot, iCiv, 2)
		
		plot.setRevealed(iCiv, True, True, -1)
	
	def isPastBirth(self, iCiv):
		return (gc.getGame().getGameTurn() >= getTurnForYear(tBirth[iCiv]))
		
	def getCityList(self, iCiv):
		if iCiv is None: return []
		return [pCity.GetCy() for pCity in PyPlayer(iCiv).getCityList()]
		
	def getAllCities(self):
		lCities = []
		for iPlayer in range(iNumPlayers):
			lCities.extend(self.getCityList(iPlayer))
		return lCities
		
	def isNeighbor(self, iCiv1, iCiv2):
		return gc.getGame().isNeighbors(iCiv1, iCiv2)
						
	def isUniqueBuilding(self, iBuilding):
		if isWorldWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType()):
			return true			

		if isTeamWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType()):
			return true

		if isNationalWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType()):
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
		
		oldCapital.setHasRealBuilding(iPalace, False)
		newCapital.setHasRealBuilding(iPalace, True)
		
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
		
		self.makeUnit(iMissionary + iReligion, iPlayer, Areas.getCapital(iPlayer), iNumUnits)
			
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
		lPlayerNumbers = [0 for i in range(iNumPlayers)]
		
		for city in lCities: lPlayers.append(city.getOwner())
		
		for i in range(len(lPlayerNumbers)): lPlayerNumbers[i] = lPlayers.count(i)
		
		iHighestEntry = self.getHighestEntry(lPlayerNumbers, lambda x: x)
		
		if iHighestEntry == 0: return -1
		
		return lPlayerNumbers.index(iHighestEntry)
		
	def getScenario(self):
		if gc.getPlayer(iEgypt).isPlayable(): return i3000BC
		
		if gc.getPlayer(iByzantium).isPlayable(): return i600AD
		
		return i1700AD
		
	def getScenarioStartYear(self):
		lStartYears = [-3000, 600, 1700]
		return lStartYears[self.getScenario()]
		
	def getScenarioStartTurn(self):
		return getTurnForYear(self.getScenarioStartYear())
		
	def hasCivic(self, iPlayer, iCivic):
		return (gc.getPlayer(iPlayer).getCivics(iCivic % 7) == iCivic)
		
	def getUniqueBuildingType(self, iPlayer, iBuildingClass):
		return gc.getCivilizationInfo(gc.getPlayer(iPlayer).getCivilizationType()).getCivilizationBuildings(iBuildingClass)
		
	def getUniqueBuilding(self, iPlayer, iBuilding):
		if iPlayer < 0: return gc.getBuildingClassInfo(gc.getBuildingInfo(iBuilding).getBuildingClassType()).getDefaultBuildingIndex()
		return gc.getCivilizationInfo(gc.getPlayer(iPlayer).getCivilizationType()).getCivilizationBuildings(gc.getBuildingInfo(iBuilding).getBuildingClassType())
		
	def getStabilityLevel(self, iPlayer):
		return data.players[iPlayer].iStabilityLevel
		
	def setStabilityLevel(self, iPlayer, iNewValue):
		data.players[iPlayer].iStabilityLevel = iNewValue
		
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
		for (i, j) in self.surroundingPlots((x, y)):
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
		elif pPlayer.getLastStateReligion() == -1:
			return iVictoryPaganism
		elif not pPlayer.isStateReligion():
			return iVictorySecularism
			
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
	def getByzantineBriberyUnits(self, spy):
		plot = gc.getMap().plot(spy.getX(), spy.getY())
		iTreasury = gc.getPlayer(spy.getOwner()).getGold()
		lTargets = []
		
		for unit in [plot.getUnit(i) for i in range(plot.getNumUnits())]:
			iCost = gc.getUnitInfo(unit.getUnitType()).getProductionCost() * 2
			if unit.getOwner() == iBarbarian and iCost <= iTreasury:
				lTargets.append((unit, iCost))
				
		return lTargets
		
	def canDoByzantineBribery(self, spy):
		if spy.getMoves() >= spy.maxMoves(): return False
		
		if not self.getByzantineBriberyUnits(spy): return False
		
		return True
	
	def doByzantineBribery(self, spy):
		localText = CyTranslator()
		
		lTargets = self.getByzantineBriberyUnits(spy)
				
		# only once per turn
		spy.finishMoves()
				
		# launch popup
		popup = Popup.PyPopup(7629, EventContextTypes.EVENTCONTEXT_ALL)
		data.lByzantineBribes = lTargets
		popup.setHeaderString(localText.getText("TXT_KEY_BYZANTINE_UP_TITLE", ()))
		popup.setBodyString(localText.getText("TXT_KEY_BYZANTINE_UP_BODY", ()))
		
		for tTuple in lTargets:
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
		
		# no respawn before spawn
		if iGameTurn < getTurnForYear(tBirth[iPlayer]) + 10: return False
		
		# only dead civ need to check for resurrection
		if gc.getPlayer(iPlayer).isAlive(): return False
			
		# check if only recently died
		if iGameTurn - data.players[iPlayer].iLastTurnAlive < self.getTurns(10): return False
		
		# check if the civ can be reborn at this date		
		if tResurrectionIntervals[iPlayer]:
			for tInterval in tResurrectionIntervals[iPlayer]:
				iStart, iEnd = tInterval
				if getTurnForYear(iStart) <= iGameTurn <= getTurnForYear(iEnd):
					break
			else:
				return False
		else:
			return False
					
		# Thailand cannot respawn when Khmer is alive and vice versa
		if iPlayer == iThailand and gc.getPlayer(iKhmer).isAlive(): return False
		if iPlayer == iKhmer and gc.getPlayer(iThailand).isAlive(): return False
		
		# Rome cannot respawn when Italy is alive and vice versa
		if iPlayer == iRome and gc.getPlayer(iItaly).isAlive(): return False
		if iPlayer == iItaly and gc.getPlayer(iRome).isAlive(): return False
		
		# Greece cannot respawn when Byzantium is alive and vice versa
		if iPlayer == iGreece and gc.getPlayer(iByzantium).isAlive(): return False
		if iPlayer == iByzantium and gc.getPlayer(iGreece).isAlive(): return False
		
		# India cannot respawn when Mughals are alive (not vice versa -> Pakistan)
		if iPlayer == iIndia and gc.getPlayer(iMughals).isAlive(): return False
		
		# Exception during Japanese UHV
		if self.getHumanID() == iJapan and iGameTurn >= getTurnForYear(1920) and iGameTurn <= getTurnForYear(1945):
			if iPlayer in [iChina, iKorea, iIndonesia, iThailand]:
				return False
		
		if not gc.getPlayer(iPlayer).isAlive() and iGameTurn > data.players[iPlayer].iLastTurnAlive + self.getTurns(20):
			if iPlayer not in dRebirth or iGameTurn > getTurnForYear(dRebirth[iPlayer]) + 10:
				return True
				
		return False
		
	def canEverRespawn(self, iPlayer, iGameTurn = gc.getGame().getGameTurn()):
		iNumIntervals = len(tResurrectionIntervals[iPlayer])
		
		if iNumIntervals == 0:
			return False
		else:
			iStart, iEnd = tResurrectionIntervals[iPlayer][iNumIntervals-1]
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
		for tLoopPlot in self.surroundingPlots(tPlot):
			for unit in self.getUnitList(tLoopPlot):
				lPossibleTiles = self.surroundingPlots(tLoopPlot, 2, lambda (x, y): self.isFree(unit.getOwner(), (x, y), bNoEnemyUnit=True, bCanEnter=True) and tPlot == (x, y))
				tTargetPlot = self.getRandomEntry(lPossibleTiles)
				if tTargetPlot:
					x, y = tTargetPlot
					unit.setXY(x, y, False, True, False)
			
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
		bReturn = self.bStabilityOverlay
		self.removeStabilityOverlay()

		if bReturn:
			return

		bWB = (iPlayer != -1)
		if iPlayer == -1:
			iPlayer = self.getHumanID()

		self.bStabilityOverlay = True
		CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE).setState("StabilityOverlay", True)

		iTeam = gc.getPlayer(iPlayer).getTeam()

		engine = CyEngine()
		map = CyMap()

		# apply the highlight
		for i in range(map.numPlots()):
			plot = map.plotByIndex(i)
			tPlot = (plot.getX(), plot.getY())
			if gc.getGame().isDebugMode() or plot.isRevealed(iTeam, False):
				if plot.isWater(): continue
				if plot.isCore(iPlayer):
					iPlotType = iCore
				else:
					iSettlerValue = plot.getSettlerValue(iPlayer)
					if bWB and iSettlerValue == 3:
						iPlotType = iAIForbidden
					elif iSettlerValue >= 90:
						if Areas.isForeignCore(iPlayer, tPlot):
							iPlotType = iContest
						else:
							iPlotType = iHistorical
					elif Areas.isForeignCore(iPlayer, tPlot):
						iPlotType = iForeignCore
					else:
						iPlotType = -1
				if iPlotType != -1:
					szColor = lStabilityColors[iPlotType]
					engine.fillAreaBorderPlotAlt(plot.getX(), plot.getY(), 1000+iPlotType, szColor, 0.7)
					
	def removeStabilityOverlay(self):
		engine = CyEngine()
		# clear the highlight
		for i in range(10):
			engine.clearAreaBorderPlots(1000+i)
		self.bStabilityOverlay = False
		CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE).setState("StabilityOverlay", False)
			
	def getRegionCities(self, lRegions):
		lCities = []
		for (x, y) in self.getWorldPlotsList():
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
		
	def isGreatPeopleBuilding(self, iBuilding):
		for iUnit in lGreatPeopleUnits:
			unit = gc.getUnitInfo(iUnit)
			if unit.getBuildings(iBuilding):
				return True
				
		return False
		
	def getBuildingCategory(self, iBuilding):
		'0 = Building'
		'1 = Religious Building'
		'2 = Unique Building'
		'3 = Great People Building'
		'4 = National Wonder'
		'5 = World Wonder'

		BuildingInfo = gc.getBuildingInfo(iBuilding)
		if BuildingInfo.getReligionType() > -1:
			return 1
		elif isWorldWonderClass(BuildingInfo.getBuildingClassType()):
			return 5
		else:
			iBuildingClass = BuildingInfo.getBuildingClassType()
			iDefaultBuilding = gc.getBuildingClassInfo(iBuildingClass).getDefaultBuildingIndex()
			if isNationalWonderClass(iBuildingClass):
				return 4
			elif self.isGreatPeopleBuilding(iBuilding):
				return 3
			else:
				if iDefaultBuilding > -1 and iDefaultBuilding != iBuilding:
					if gc.getBuildingInfo(iBuilding).isGraphicalOnly():
						return 0
					return 2
				else:
					if gc.getBuildingInfo(iBuilding).isGraphicalOnly():
						return -1
					return 0
					
	def getLeaderCiv(self, iLeader):
		for iCiv in range(gc.getNumCivilizationInfos()):
			civ = gc.getCivilizationInfo(iCiv)
			if civ.isLeaders(iLeader):
				return iCiv
		return None
		
	def setStateReligionBeforeBirth(self, lPlayers, iReligion):
		for iPlayer in lPlayers:
			if gc.getGame().getGameTurn() < getTurnForYear(tBirth[iPlayer]) and gc.getPlayer(iPlayer).getStateReligion() != iReligion:
				gc.getPlayer(iPlayer).setLastStateReligion(iReligion)
				
	def playerNames(self, lPlayers):
		return str([gc.getPlayer(iPlayer).getCivilizationShortDescription(0) for iPlayer in lPlayers])
		
	def isYearIn(self, iStartYear, iEndYear):
		iGameTurn = gc.getGame().getGameTurn()
		return getTurnForYear(iStartYear) <= iGameTurn <= getTurnForYear(iEndYear)
		
	def getWorldPlotsList(self):
		return [(x, y) for x in range(iWorldX) for y in range(iWorldY)]
		
	def captureUnit(self, pLosingUnit, pWinningUnit, iUnit, iChance):
		if pLosingUnit.isAnimal(): return
		
		if pLosingUnit.getDomainType() != DomainTypes.DOMAIN_LAND: return
		
		if gc.getUnitInfo(pLosingUnit.getUnitType()).getCombat() == 0: return
		
		iPlayer = pWinningUnit.getOwner()
		
		iRand = gc.getGame().getSorenRandNum(100, "capture slaves")
		if iRand < iChance:
			self.makeUnitAI(iUnit, iPlayer, (pWinningUnit.getX(), pWinningUnit.getY()), UnitAITypes.UNITAI_WORKER, 1)
			CyInterface().addMessage(pWinningUnit.getOwner(), True, 15, CyTranslator().getText("TXT_KEY_UP_ENSLAVE_WIN", ()), 'SND_REVOLTEND', 1, gc.getUnitInfo(iUnit).getButton(), ColorTypes(8), pWinningUnit.getX(), pWinningUnit.getY(), True, True)
			CyInterface().addMessage(pLosingUnit.getOwner(), True, 15, CyTranslator().getText("TXT_KEY_UP_ENSLAVE_LOSE", ()), 'SND_REVOLTEND', 1, gc.getUnitInfo(iUnit).getButton(), ColorTypes(7), pWinningUnit.getX(), pWinningUnit.getY(), True, True)
			
			if iPlayer == iAztecs:
				if pLosingUnit.getOwner() not in lCivGroups[5] and pLosingUnit.getOwner() < iNumPlayers:
					data.iAztecSlaves += 1
					
	def triggerMeltdown(self, iPlayer, iCity):
		print "trigger meltdown"
		
		pCity = gc.getPlayer(iPlayer).getCity(iCity)
		pCity.triggerMeltdown(iNuclearPlant)
		
	def getCitySiteList(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		return [pPlayer.AI_getCitySite(i) for i in range(pPlayer.AI_getNumCitySites())]
		
	def getAreaUnits(self, iPlayer, tTL, tBR):
		lUnits = []
		for tPlot in self.getPlotList(tTL, tBR):
			lUnits.extend([unit for unit in self.getUnitList(tPlot) if unit.getOwner() == iPlayer])
		return lUnits
		
	def variation(self, iVariation):
		return gc.getGame().getSorenRandNum(2 * iVariation, 'Variation') - iVariation
		
	def relocateGarrisonToClosestCity(self, city):
		closestCity = gc.getMap().findCity(city.getX(), city.getY(), city.getOwner(), TeamTypes.NO_TEAM, False, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, city)
		x, y = (closestCity.getX(), closestCity.getY())
		
		for tPlot in self.surroundingPlots((city.getX(), city.getY()), 2):
			for unit in self.getUnitList(tPlot):
				if unit.getOwner() == city.getOwner():
					if x >= 0 or y >= 0: unit.setXY(x, y, False, True, False)

	def flipOrRelocateGarrison(self, city, iNumDefenders):
		x = city.getX()
		y = city.getY()
		
		lRelocatedUnits = []
		lFlippedUnits = []
		
		for tPlot in self.surroundingPlots((x, y), 2):
			for unit in self.getUnitList(tPlot):
				if unit.getOwner() == city.getOwner() and unit.getDomainType() == DomainTypes.DOMAIN_LAND:
					if len(lFlippedUnits) < iNumDefenders:
						lFlippedUnits.append(unit)
					else:
						lRelocatedUnits.append(unit)
						
		return lFlippedUnits, lRelocatedUnits
		
	def flipUnits(self, lUnits, iNewOwner, tPlot):
		for unit in lUnits:
			self.flipUnit(unit, iNewOwner, tPlot)
			
	def flipUnit(self, unit, iNewOwner, tPlot):
		iUnitType = unit.getUnitType()
		if unit.getX() >= 0 and unit.getY() >= 0:
			unit.kill(False, iBarbarian)
			self.makeUnit(iUnitType, iNewOwner, tPlot, 1)
		
	def relocateUnitsToCore(self, iPlayer, lUnits):
		lCoreCities = self.getOwnedCoreCities(iPlayer)
		dUnits = {}
		
		if not lCoreCities:
			self.killUnits(lUnits)
			return
		
		for unit in lUnits:
			iUnitType = unit.getUnitType()
			if iUnitType in dUnits:
				if unit not in dUnits[iUnitType]: dUnits[iUnitType].append(unit)
			else:
				dUnits[iUnitType] = [unit]
				
		for iUnitType in dUnits:
			for i, unit in enumerate(dUnits[iUnitType]):
				index = i % (len(lCoreCities) * 2)
				if index < len(lCoreCities):
					city = lCoreCities[index]
					if unit.getX() >= 0 and unit.getY() >= 0 and (unit.getX(), unit.getY()) != (city.getX(), city.getY()):
						unit.setXY(city.getX(), city.getY(), False, True, False)
					
	def flipOrCreateDefenders(self, iNewOwner, lUnits, tPlot, iNumDefenders):
		self.flipUnits(lUnits, iNewOwner, tPlot)
	
		if len(lUnits) < iNumDefenders and utils.getHumanID() != iNewOwner:
			self.makeUnit(self.getBestDefender(iNewOwner), iNewOwner, tPlot, iNumDefenders - len(lUnits))
			
	def killUnits(self, lUnits):
		for unit in lUnits:
			if unit.getX() >= 0 and unit.getY() >= 0:
				unit.kill(False, iBarbarian)
				
	def ensureDefenders(self, iPlayer, tPlot, iNumDefenders):
		lUnits = [unit for unit in self.getUnitList(tPlot) if unit.getOwner() == iPlayer and unit.canFight()]
		if len(lUnits) < iNumDefenders:
			self.makeUnit(self.getBestDefender(iPlayer), iPlayer, tPlot, iNumDefenders - len(lUnits))
			
	def getGoalText(self, iPlayer, iGoal, bTitle = False):
		iCiv = gc.getPlayer(iPlayer).getCivilizationType()
		iGameSpeed = gc.getGame().getGameSpeedType()
		
		baseKey = "TXT_KEY_UHV_" + gc.getCivilizationInfo(iCiv).getIdentifier() + str(iGoal+1)
		
		fullKey = baseKey
		
		if bTitle:
			fullKey += "_TITLE"
		elif iGameSpeed < 2:
			fullKey += "_" + gc.getGameSpeedInfo(iGameSpeed).getText().upper()
			
		translation = localText.getText(str(fullKey), ())
		
		if translation != fullKey: return translation
		
		return localText.getText(str(baseKey), ())
		
	def getReligiousGoalText(self, iReligion, iGoal, bTitle = False):
		iGameSpeed = gc.getGame().getGameSpeedType()
	
		if iReligion < iNumReligions:
			religionKey = gc.getReligionInfo(iReligion).getText()[:3].upper()
		elif iReligion == iNumReligions:
			religionKey = "POL"
		elif iReligion == iNumReligions+1:
			religionKey = "SEC"
			
		baseKey = "TXT_KEY_URV_" + religionKey + str(iGoal+1)
		
		fullKey = baseKey
		
		if bTitle:
			fullKey += "_TITLE"
		elif iGameSpeed < 2:
			fullKey += "_" + gc.getGameSpeedInfo(iGameSpeed).getText().upper()
			
		translation = localText.getText(str(fullKey), ())
		
		if translation != fullKey: return translation
		
		return localText.getText(str(baseKey), ())
		
	def getDawnOfManText(self, iPlayer):
		iScenario = self.getScenario()
		
		baseKey = "TXT_KEY_DOM_" + gc.getPlayer(iPlayer).getCivilizationShortDescription(0).replace(" ", "_").upper()
		
		fullKey = baseKey
		
		if iScenario == i600AD: fullKey += "_600AD"
		elif iScenario == i1700AD: fullKey += "_1700AD"
		
		translation = localText.getText(str(fullKey), ())
		
		if translation != fullKey: return translation
		
		return localText.getText(str(baseKey), ())
		
	def plot(self, tuple):
		return gc.getMap().plot(tuple[0], tuple[1])
		
	def isAreaControlled(self, iPlayer, tTL, tBR, tExceptions=()):
		lPlots = self.getPlotList(tTL, tBR, tExceptions)
		return len(self.getAreaCitiesCiv(iPlayer, lPlots)) >= len(self.getAreaCities(lPlots))
		
	def breakAutoplay(self):
		iHuman = self.getHumanID()
		if gc.getGame().getGameTurnYear() < tBirth[iHuman]:
			self.makeUnit(iSettler, iHuman, (0, 0), 1)
			
	def getBuildingEffectCity(self, iBuilding):
		if gc.getGame().getBuildingClassCreatedCount(gc.getBuildingInfo(iBuilding).getBuildingClassType()) == 0:
			return None
			
		for iPlayer in range(iNumTotalPlayersB):
			if gc.getPlayer(iPlayer).isHasBuildingEffect(iBuilding):
				for city in self.getCityList(iPlayer):
					if city.isHasBuildingEffect(iBuilding):
						return city
						
		return None
			
utils = RFCUtils()