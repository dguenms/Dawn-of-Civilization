# Rhye's and Fall of Civilization - Historical Victory Goals


from CvPythonExtensions import *
import CvUtil
import PyHelpers
#import Popup
#import cPickle as pickle
from Consts import *
from StoredData import data #edead
from RFCUtils import utils
import random

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

iDuration = 6

class Plague:

######################################
### Main methods (Event-Triggered) ###
######################################


	def setup(self):
		for iPlayer in range(iNumMajorPlayers):
			data.players[iPlayer].iPlagueCountdown = -utils.getTurns(iImmunity)
			
		data.lGenericPlagueDates[0] = 80
		data.lGenericPlagueDates[2] = 300 # safe value to prevent plague at start of 1700 AD scenario
		
		if utils.getScenario() == i3000BC:
			data.lGenericPlagueDates[0] = getTurnForYear(400) + utils.variation(20)
			
		data.lGenericPlagueDates[1] = getTurnForYear(1300) + utils.variation(20)
		
		# Avoid interfering with the Indian UHV
		if utils.getHumanID() == iIndia and data.lGenericPlagueDates[1] <= getTurnForYear(1200):
			data.lGenericPlagueDates[1] = getTurnForYear(1200) + 1
		
		if utils.getScenario != i1700AD:
			data.lGenericPlagueDates[2] = getTurnForYear(1650) + utils.variation(20)
			
		data.lGenericPlagueDates[3] = getTurnForYear(1850) + utils.variation(20)

		undoPlague = gc.getGame().getSorenRandNum(8, 'undo')
		if undoPlague <= 3:
			data.lGenericPlagueDates[undoPlague] = -1
			
	


	def checkTurn(self, iGameTurn):
		if data.bNoPlagues:
			return

		for iPlayer in range(iNumTotalPlayersB):
			if gc.getPlayer(iPlayer).isAlive():
				if data.players[iPlayer].iPlagueCountdown > 0:
					data.players[iPlayer].iPlagueCountdown -= 1
					if data.players[iPlayer].iPlagueCountdown == 2:
						self.preStopPlague(iPlayer)
					elif data.players[iPlayer].iPlagueCountdown == 0:
						self.stopPlague(iPlayer)
				elif data.players[iPlayer].iPlagueCountdown < 0:
					data.players[iPlayer].iPlagueCountdown += 1

		for iPlague, iPlagueDate in enumerate(data.lGenericPlagueDates):
			if iGameTurn == iPlagueDate:
				#print ("new plague")
				self.startPlague(iPlague)
			if iPlague >= 1:
				#retry if the epidemic is dead too quickly
				if iGameTurn == iPlagueDate + 4:
					iInfectedCounter = 0
					for iPlayer in range(iNumTotalPlayersB):
						if data.players[iPlayer].iPlagueCountdown > 0:
							iInfectedCounter += 1
					if iInfectedCounter == 1:
						#print ("new plague again1")
						self.startPlague(iPlague)
			if iPlague == 2 or iPlague == 3:
				if iGameTurn == iPlagueDate + 8:
					iInfectedCounter = 0
					for iPlayer in range(iNumTotalPlayersB):
						if data.players[iPlayer].iPlagueCountdown > 0:
							iInfectedCounter += 1
					if iInfectedCounter <= 2:
						#print ("new plague again2")
						self.startPlague(iPlague)

	def checkPlayerTurn(self, iGameTurn, iPlayer):
		if data.bNoPlagues:
			return

		if iPlayer < iNumTotalPlayersB:
			if data.players[iPlayer].iPlagueCountdown > 0:
				self.processPlague(iPlayer)



	def startPlague(self, iPlagueCounter):
		iWorstCiv = -1
		iWorstHealth = 200
		for iPlayer in range(iNumMajorPlayers):
			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer.isAlive():
				if self.isVulnerable(iPlayer):
					iHealth = self.calculateHealth(iPlayer) / 2
					if pPlayer.calculateTotalCityHealthiness() > 0:
						iHealth += gc.getGame().getSorenRandNum(40, 'random modifier')
						#print ("starting plague", "civ:", iPlayer, "iHealth:", iHealth)
						if iPlagueCounter == 2: #medieval black death
							if iPlayer in lCivGroups[0]:
								iHealth -= 5 
					if iHealth < iWorstHealth:
						iWorstHealth = iHealth
						iWorstCiv = iPlayer
		if iWorstCiv != -1:
			print ("worstCiv", iWorstCiv)
			pWorstCiv = gc.getPlayer(iWorstCiv)
			city = utils.getRandomCity(iWorstCiv)
			if city:
				self.spreadPlague(iWorstCiv)
				self.infectCity(city)
				self.announceForeignPlagueSpread(city)


	def preStopPlague(self, iPlayer):
		cityList = [city for city in utils.getCityList(iPlayer) if city.hasBuilding(iPlague)]
		if cityList:
			iModifier = 0
			for city in cityList:
				if gc.getGame().getSorenRandNum(100, 'roll') > 30 - 5*city.healthRate(False, 0) + iModifier:
					city.setHasRealBuilding(iPlague, False)
					iModifier += 5 #not every city should quit


	def stopPlague(self, iPlayer):
		data.players[iPlayer].iPlagueCountdown = -utils.getTurns(iImmunity)
		if data.players[iPlayer].bFirstContactPlague:
			data.players[iPlayer].iPlagueCountdown = -utils.getTurns(iImmunity-30)
		data.players[iPlayer].bFirstContactPlague = False
		for city in utils.getCityList(iPlayer):
			city.setHasRealBuilding(iPlague, False)
			
	def losePopulation(self, city):
		if city.getPopulation() <= 1: return
		
		iRand = gc.getGame().getSorenRandNum(100, "Lose population from plague")
		iHealth = city.healthRate(False, 0)
		
		if iRand > 40 + 5 * iHealth:
			city.changePopulation(-1)
			
	def spreadToVassals(self, iPlayer):
		if data.players[iPlayer].bFirstContactPlague: return
		
		for iLoopPlayer in range(iNumMajorPlayers):
			if gc.getTeam(gc.getPlayer(iPlayer).getTeam()).isVassal(iLoopPlayer) or gc.getTeam(gc.getPlayer(iLoopPlayer).getTeam()).isVassal(iPlayer):
				if self.isVulnerable(iLoopPlayer) and data.players[iLoopPlayer].iPlagueCountdown > 2:
					if gc.getPlayer(iLoopPlayer).getNumCities() > 0:
						capital = gc.getPlayer(iLoopPlayer).getCapitalCity()
						self.spreadPlague(iLoopPlayer)
						self.infectCity(capital)
						
	def spreadToSurroundings(self, city):
		iPlayer = city.getOwner()
		
		# do not spread if plague is almost over
		if data.players[iPlayer].iPlagueCountdown <= 2: return
	
		for (x, y) in utils.surroundingPlots((city.getX(), city.getY()), 2):
			plot = gc.getMap().plot(x, y)
			
			if not plot.isOwned(): continue
			if (city.getX(), city.getY()) == (x, y): continue
			
			if plot.getOwner() == iPlayer:
				if plot.isCity():
					plotCity = plot.getPlotCity()
					if not plotCity.isHasRealBuilding(iPlague):
						self.infectCity(plotCity)
			
			else:
				if data.players[iPlayer].bFirstContactPlague: continue
				
				if self.isVulnerable(plot.getOwner()):
					self.spreadPlague(plot.getOwner())
					self.infectCitiesNear(plot.getOwner(), x, y)
					
	def damageNearbyUnits(self, city):
		for (x, y) in utils.surroundingPlots((city.getX(), city.getY()), 3):
			plot = gc.getMap().plot(x, y)
			iDistance = utils.calculateDistance(city.getX(), city.getY(), x, y)
			
			if iDistance == 0:
				self.killUnitsByPlague(city, plot, 0, 42, 2)
			elif not plot.isCity():
				if iDistance < 3:
					if plot.isRoute():
						self.killUnitsByPlague(city, plot, 10, 35, 0)
					else:
						self.killUnitsByPlague(city, plot, 30, 35, 0)
				else:
					if plot.isRoute() or plot.isWater():
						self.killUnitsByPlague(city, plot, 30, 35, 0)
		
	def spreadAlongTradeRoutes(self, city):
		iPlayer = city.getOwner()
		
		if data.players[iPlayer].bFirstContactPlague: return
		if data.players[iPlayer].iPlagueCountdown <= 2: return
		
		for iTradeRoute in range(city.getTradeRoutes()):
			tradeCity = city.getTradeCity(iTradeRoute)
			if not tradeCity.isNone():
				iOwner = tradeCity.getOwner()
				if not tradeCity.isHasRealBuilding(iPlague):
					if iPlayer == iOwner:
						self.infectCity(tradeCity)
					elif self.isVulnerable(iOwner):
						self.spreadPlague(iOwner)
						self.infectCity(tradeCity)
						self.announceForeignPlagueSpread(city)
						
	def spreadBetweenCities(self, iPlayer, lSourceCities, lTargetCities):
		if data.players[iPlayer].iPlagueCountdown <= 2: return
		
		random.shuffle(lTargetCities)
		for targetCity in lTargetCities:
			if [city for city in lSourceCities if targetCity.isConnectedTo(city) and utils.calculateDistance(targetCity.getX(), targetCity.getY(), city.getX(), city.getY()) <= 6]:
				self.infectCity(targetCity)
				return

	def processPlague(self, iPlayer):
		
		# collect cities with and without plague
		lInfectedCities = [city for city in utils.getCityList(iPlayer) if city.isHasRealBuilding(iPlague)]
		lUninfectedCities = [city for city in utils.getCityList(iPlayer) if not city.isHasRealBuilding(iPlague)]
			
		for city in lInfectedCities:
			
			# let plague affect city
			self.losePopulation(city)
			
			# let plague spread to vassals
			if city.isCapital():
				self.spreadToVassals(iPlayer)
				
			# let plague affect surrounding area
			self.spreadToSurroundings(city)
			
			# let plague damage nearby units
			self.damageNearbyUnits(city)
			
			# let plague spread through trade routes
			self.spreadAlongTradeRoutes(city)
			
		# spread within the civilization
		self.spreadBetweenCities(iPlayer, lInfectedCities, lUninfectedCities)


	def killUnitsByPlague(self, city, pPlot, baseValue, iDamage, iPreserveDefenders):
		iOwner = city.getOwner()
		pOwner = gc.getPlayer(iOwner)
		teamOwner = gc.getTeam(gc.getPlayer(city.getOwner()).getTeam())
		
		#deadly plague when human player isn't born yet, will speed up the loading
		if gc.getGame().getGameTurn() < getTurnForYear(tBirth[utils.getHumanID()]) + utils.getTurns(20):
			iDamage += 10
			baseValue -= 5


		#print (city.getX(), city.getY())
		iNumUnitsInAPlot = pPlot.getNumUnits()
		#iPreserveHumanDefenders = iPreserveDefenders -1 #human handicap
		iPreserveHumanDefenders = iPreserveDefenders
		iHuman = utils.getHumanID()
		if iPreserveDefenders > 0: #cities only
			#handicap for civs distant from human player too
			if not pOwner.isHuman(): #if not human and close or at war
				#iPreserveDefenders -= 1
				if teamOwner.isAtWar(iHuman):
					iPreserveDefenders += 2
				else:
					for iCivGroups in range(len(lCivGroups)):
						if iOwner in lCivGroups[iCivGroups] and utils.getHumanID() in lCivGroups[iCivGroups]:
							iPreserveDefenders += 1
							break
		if iNumUnitsInAPlot > 0:
			for iUnit in reversed(range(iNumUnitsInAPlot)):
				unit = pPlot.getUnit(iUnit)
				if gc.getPlayer(unit.getOwner()).isHuman():
					#print ("iPreserveHumanDefenders", iPreserveHumanDefenders)
					if iPreserveHumanDefenders > 0:
						if utils.isDefenderUnit(unit):
							iPreserveHumanDefenders -= 1
							if pPlot.getNumUnits() > iPreserveDefenders:
								pass
							else:
								iMaxDamage = 50
								if unit.workRate(100) > 0 and not unit.canFight(): iMaxDamage = 100
								
								unit.setDamage(min(iMaxDamage, unit.getDamage() + iDamage - 20), iBarbarian)
							#print ("preserve")
							continue
				else:
					if iPreserveDefenders > 0:
						if utils.isDefenderUnit(unit):
							iPreserveDefenders -= 1
							if pPlot.getNumUnits() > iPreserveDefenders or gc.getTeam(gc.getPlayer(unit.getOwner()).getTeam()).isAtWar(iHuman):
								pass
							else:
								iMaxDamage = 50
								if unit.workRate(100) > 0 and not unit.canFight(): iMaxDamage = 100
								
								unit.setDamage(min(iMaxDamage, unit.getDamage() + iDamage - 20), iBarbarian)
							#print ("preserve")
							continue
				if utils.isMortalUnit(unit): #another human handicap inside
					iThreshold = baseValue + 5*city.healthRate(False, 0)
					#print ("iThreshold", iThreshold)

					if teamOwner.isAtWar(iHuman) and iOwner < iNumMajorPlayers:
						if unit.getOwner() == iOwner:
							iDamage *= 3
							iDamage /= 4
					
					if data.players[city.getOwner()].bFirstContactPlague:
						if unit.getOwner() in lCivBioOldWorld:
							iDamage /= 2
					
					if gc.getGame().getSorenRandNum(100, 'roll') > iThreshold:
						if iDamage - unit.getExperience()/10 - unit.baseCombatStr()*3/7 >= 100 - unit.getDamage():
							if unit.getOwner() != iOwner and gc.getPlayer(unit.getOwner()).isHuman():
								CyInterface().addMessage(unit.getOwner(), False, iDuration/2, CyTranslator().getText("TXT_KEY_PLAGUE_PROCESS_UNIT", ()) + " " + city.getName(), "AS2D_PLAGUE", 0, "", ColorTypes(iLime), -1, -1, True, True)
						#Leoreth: keep units at 50% minimum
						iMaxDamage = 50
						if unit.workRate(100) > 0 and not unit.canFight(): iMaxDamage = 100
						unit.setDamage(min(iMaxDamage, unit.getDamage() + iDamage - unit.getExperience()/10 - unit.baseCombatStr()/2), iBarbarian)
						#print ("process")
						break


	def infectCity(self, city):
		if city.getOwner() == iCongo and gc.getGame().getGameTurnYear() <= 1650: return	# Leoreth: don't let plague mess up the UHV
		elif city.getOwner() == iMali and gc.getGame().getGameTurnYear() <= 1500: return	# same for Mali
		#print ("infected", city.getName())
		city.setHasRealBuilding(iPlague, True)
		if gc.getPlayer(city.getOwner()).isHuman():
			CyInterface().addMessage(city.getOwner(), True, iDuration/2, CyTranslator().getText("TXT_KEY_PLAGUE_SPREAD_CITY", ()) + " " + city.getName() + "!", "AS2D_PLAGUE", 0, "", ColorTypes(iLime), -1, -1, True, True)
		for (x, y) in utils.surroundingPlots((city.getX(), city.getY()), 2):
			pPlot = gc.getMap().plot( x, y )
			if pPlot.getUpgradeProgress() > 0:
				pPlot.setUpgradeProgress(0)
				iImprovement = pPlot.getImprovementType()
				if iImprovement == iTown:
					pPlot.setImprovementType(iVillage)
				#elif iImprovement == iVillage:
				#	pPlot.setImprovementType(iHamlet)
				#elif iImprovement == iHamlet:
				#	pPlot.setImprovementType(iCottage)
				#elif iImprovement == iCottage:
				#	pPlot.setImprovementType(-1)
				if pPlot.isCity():
					if (city.getX(), city.getY()) == (x, y):
						self.killUnitsByPlague(city, pPlot, 0, 100, 0)


	def isVulnerable(self, iPlayer):
		if iPlayer >= iNumMajorPlayers:
			if -10 < data.players[iPlayer].iPlagueCountdown <= 0: #more vulnerable
				return True
				
		pPlayer = gc.getPlayer(iPlayer)
			
		if gc.getTeam(pPlayer.getTeam()).isHasTech(iMicrobiology): return False
		
		if iPlayer in lCivBioNewWorld and not data.lFirstContactConquerors[lCivBioNewWorld.index(iPlayer)]: return False
			
		if data.players[iPlayer].iPlagueCountdown == 0: #vulnerable
			if not gc.getTeam(pPlayer.getTeam()).isHasTech(iMicrobiology):
				iHealth = self.calculateHealth(iPlayer)
				if iHealth < 14: #no spread for iHealth >= 74 years
					return True
					
		return False


	def spreadPlague(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		iHealth = self.calculateHealth(iPlayer) / 7 #duration range will be -4 to +4 for 30 to 90
		data.players[iPlayer].iPlagueCountdown = min(9, iDuration - iHealth)
		print ("spreading plague to", iPlayer)


	def calculateHealth(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.calculateTotalCityHealthiness() > 0:
			return int((1.0 * pPlayer.calculateTotalCityHealthiness()) / (pPlayer.calculateTotalCityHealthiness() + \
				pPlayer.calculateTotalCityUnhealthiness()) * 100) - 60
		return -30


	def infectCitiesNear(self, iPlayer, startingX, startingY):
		for city in utils.getCityList(iPlayer):
			if utils.calculateDistance(city.getX(), city.getY(), startingX, startingY) <= 3:
				self.infectCity(city)
				self.announceForeignPlagueSpread(city)


	def onCityAcquired(self, iOldOwner, iNewOwner, city):
		if city.hasBuilding(iPlague):
			if not data.players[iOldOwner].bFirstContactPlague: #don't infect if first contact plague
				if data.players[iNewOwner].iPlagueCountdown <= 0 and gc.getGame().getGameTurn() > getTurnForYear(tBirth[iNewOwner]) + utils.getTurns(iImmunity): #skip immunity in this case (to prevent expoiting of being immune to conquer weak civs), but not for the new born civs
					if not gc.getTeam(gc.getPlayer(iNewOwner).getTeam()).isHasTech(iMicrobiology): #but not permanent immunity
						print("acquiring plague")
						self.spreadPlague(iNewOwner)
						self.infectCitiesNear(iNewOwner, city.getX(), city.getY())
						return
			city.setHasRealBuilding(iPlague, False)


	def onCityRazed(self, city, iNewOwner):
		if city.hasBuilding(iPlague):
			if data.players[iNewOwner].iPlagueCountdown > 0:
				iNumCitiesInfected = 0
				for otherCity in utils.getCityList(iNewOwner):
					if (otherCity.getX(), otherCity.getY()) != (city.getX(), city.getY()): #because the city razed still has the plague
						if otherCity.hasBuilding(iPlague):
							iNumCitiesInfected += 1
				print ("iNumCitiesInfected", iNumCitiesInfected)
				if iNumCitiesInfected == 0:
					data.players[iNewOwner].iPlagueCountdown = 0 #undo spreadPlague called in onCityAcquired()


	def onFirstContact(self, iTeamX, iHasMetTeamY):
		if data.bNoPlagues:
			return

		if gc.getGame().getGameTurn() > getTurnForYear(tBirth[iAztecs]) + 2 and gc.getGame().getGameTurn() < getTurnForYear(1800):
			iOldWorldCiv = -1
			iNewWorldCiv = -1
			if iTeamX in lCivBioNewWorld and iHasMetTeamY in lCivBioOldWorld:
				iNewWorldCiv = iTeamX
				iOldWorldCiv = iHasMetTeamY
			if iOldWorldCiv != -1 and iNewWorldCiv != -1:
				pNewWorldCiv = gc.getPlayer(iNewWorldCiv)
				if data.players[iNewWorldCiv].iPlagueCountdown == 0: #vulnerable
					#print ("vulnerable", iNewWorldCiv)
					if not gc.getTeam(pNewWorldCiv.getTeam()).isHasTech(iBiology):
						city = utils.getRandomCity(iNewWorldCiv)
						if city:
							iHealth = self.calculateHealth(iNewWorldCiv)
							if iHealth < 10: #no spread for iHealth >= 70 years
								iHealth /= 10
								if gc.getGame().getSorenRandNum(100, 'roll') > 30 + 5*iHealth:
									data.players[iNewWorldCiv].iPlagueCountdown = iDuration - iHealth
									data.players[iNewWorldCiv].bFirstContactPlague = True
									#print ("spreading (through first contact) plague to", iNewWorldCiv)
									self.infectCity(city)
									self.announceForeignPlagueSpread(city)


	def announceForeignPlagueSpread(self, city):
		iOwner = city.getOwner()
		iHuman = utils.getHumanID()
		if gc.getPlayer(iHuman).canContact(iOwner) and iHuman != iOwner and city.isRevealed(iHuman, False):
			CyInterface().addMessage(iHuman, False, iDuration/2, CyTranslator().getText("TXT_KEY_PLAGUE_SPREAD_CITY", ()) + " " + city.getName() + " (" + gc.getPlayer(iOwner).getCivilizationAdjective(0) + ")", "AS2D_PLAGUE", 0, "", ColorTypes(iLime), -1, -1, True, True)


	def onTechAcquired(self, iTech, iPlayer):
		if data.players[iPlayer].iPlagueCountdown > 1:
			data.players[iPlayer].iPlagueCountdown = 1
