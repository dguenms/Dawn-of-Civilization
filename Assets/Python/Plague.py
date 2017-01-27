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
		
		if utils.getScenario() == i3000BC:  #early start condition
			data.lGenericPlagueDates[0] = getTurnForYear(400) + gc.getGame().getSorenRandNum(40, 'Variation') - 20
		else:
			data.lGenericPlagueDates[0] = 80
			
		data.lGenericPlagueDates[1] = getTurnForYear(1300) + gc.getGame().getSorenRandNum(40, 'Variation') - 20
		if utils.getScenario != i1700AD:
			data.lGenericPlagueDates[2] = getTurnForYear(1650) + gc.getGame().getSorenRandNum(40, 'Variation') - 20
		else:
			data.lGenericPlagueDates[2] = 300 # Safe value to prevent plague at start of 1700 scenario
		data.lGenericPlagueDates[3] = getTurnForYear(1850) + gc.getGame().getSorenRandNum(40, 'Variation') - 20

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


	def processPlague(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		#first spread to close locations
		cityList = [] #see below
		lInfectedCities = []
		lNotInfectedCities = []
		for city in utils.getCityList(iPlayer):
			cityList.append(city) #see below
			if city.hasBuilding(iPlague):
				lInfectedCities.append(city)
				#print ("plague in city", city.getName())
				if city.getPopulation() > 1:
					#print("healthRate in city", 35 + 5*city.healthRate(False, 0))
					if gc.getGame().getSorenRandNum(100, 'roll') > 40 + 5*city.healthRate(False, 0):
						city.changePopulation(-1)
				if city.isCapital(): #delete in vanilla
					if data.players[iPlayer].iPlagueCountdown > 2: #don't spread the last turns
						if not data.players[iPlayer].bFirstContactPlague: #don't infect if first contact plague
							for iLoopCiv in range(iNumMajorPlayers):
								if gc.getTeam(pPlayer.getTeam()).isVassal(iLoopCiv) or gc.getTeam(gc.getPlayer(iLoopCiv).getTeam()).isVassal(iPlayer):
									if gc.getPlayer(iLoopCiv).getNumCities() > 0: #this check is needed, otherwise game crashes
										capital = gc.getPlayer(iLoopCiv).getCapitalCity()
										if self.isVulnerable(iLoopCiv):
											self.spreadPlague(iLoopCiv)
											self.infectCity(capital)
											#print ("infect master/vassal", city.getName(), "to", capital.getName())
				for (x, y) in utils.surroundingPlots((city.getX(), city.getY()), 2):
					##print ("plagueXY", x, y)
					pPlot = gc.getMap().plot( x, y )
					if pPlot.getOwner() != iPlayer and pPlot.getOwner() >= 0:
						if not data.players[iPlayer].bFirstContactPlague: #don't infect if first contact plague
							if data.players[iPlayer].iPlagueCountdown > 2: #don't spread the last turns
								if self.isVulnerable(pPlot.getOwner()):
									self.spreadPlague(pPlot.getOwner())
									self.infectCitiesNear(pPlot.getOwner(), x, y)
									#print ("infect foreign near", city.getName())
					else:
						if pPlot.isCity() and not (city.getX(), city.getY()) == (x, y):
							#print ("is city", x, y)
							cityNear = pPlot.getPlotCity() 
							if not cityNear.hasBuilding(iPlague):
								if data.players[iPlayer].iPlagueCountdown > 2: #don't spread the last turns
									self.infectCity(cityNear)
									#print ("infect near", city.getName(), "to", cityNear.getName())
						else:
							if (city.getX(), city.getY()) == (x, y):
								self.killUnitsByPlague(city, pPlot, 0, 42, 2)
							else:
								if pPlot.isRoute():
									self.killUnitsByPlague(city, pPlot, 10, 35, 0)
								elif pPlot.isWater():
									self.killUnitsByPlague(city, pPlot, 30, 35, 0)
								else:
									self.killUnitsByPlague(city, pPlot, 30, 35, 0)
				for (x, y) in utils.surroundingPlots((city.getX(), city.getY()), 3):
					pPlot = gc.getMap().plot(x, y)
					if pPlot.getOwner() == iPlayer or not pPlot.isOwned():
						if not pPlot.isCity():
							if pPlot.isRoute() or pPlot.isWater():
								self.killUnitsByPlague(city, pPlot, 30, 35, 0)


				if not data.players[iPlayer].bFirstContactPlague: #don't infect if first contact plague
					#spread to trade route cities
					if data.players[iPlayer].iPlagueCountdown > 2: #don't spread the last turns
						for iRoute in range(city.getTradeRoutes()):
							loopCity = city.getTradeCity(iRoute)
							if not loopCity.isNone():
								if not loopCity.hasBuilding(iPlague):
									iOwner = loopCity.getOwner()
									if iPlayer == iOwner:
										self.infectCity(loopCity)
										#print ("infect by trade route", city.getName(), "to", loopCity.getName())
									elif gc.getTeam(pPlayer.getTeam()).isOpenBorders(iOwner) or \
										gc.getTeam(pPlayer.getTeam()).isVassal(iOwner) or \
										gc.getTeam(gc.getPlayer(iOwner).getTeam()).isVassal(iPlayer): #own city, or open borders, or vassal
										if self.isVulnerable(iOwner):
											self.spreadPlague(iOwner)
											self.infectCity(loopCity)
											#print ("infect by trade route", city.getName(), "to", loopCity.getName())
											self.announceForeignPlagueSpread(city)
			else:
				lNotInfectedCities.append(city)

		#spread to other cities of the empire
		if lNotInfectedCities:
			if data.players[iPlayer].iPlagueCountdown > 2: #don't spread the last turns
				random.shuffle(lInfectedCities)
				for infectedCity in lInfectedCities:
					lPossibleCities = [city for city in lNotInfectedCities if city.isConnectedTo(infectedCity) and utils.calculateDistance(city.getX(), city.getY(), infectedCity.getX(), infectedCity.getY()) <= 6]
					if lPossibleCities:
						self.infectCity(utils.getRandomEntry(lPossibleCities))
						return


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
			for iUnit in range(iNumUnitsInAPlot):
				i = iNumUnitsInAPlot - iUnit - 1
				unit = pPlot.getUnit(i)
				if gc.getPlayer(unit.getOwner()).isHuman():
					#print ("iPreserveHumanDefenders", iPreserveHumanDefenders)
					if iPreserveHumanDefenders > 0:
						if utils.isDefenderUnit(unit):
							iPreserveHumanDefenders -= 1
							if pPlot.getNumUnits() > iPreserveDefenders:
								pass
							else:
								# Leoreth: keep units at 50% minimum
								unit.setDamage(min(50, unit.getDamage() + iDamage - 20), iBarbarian)
							#print ("preserve")
							continue
				else:
					if iPreserveDefenders > 0:
						if utils.isDefenderUnit(unit):
							iPreserveDefenders -= 1
							if pPlot.getNumUnits() > iPreserveDefenders or gc.getTeam(gc.getPlayer(unit.getOwner()).getTeam()).isAtWar(iHuman):
								pass
							else:
								# Leoreth: keep units at 50% minimum
								unit.setDamage(min(50, unit.getDamage() + iDamage - 20), iBarbarian)
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
						unit.setDamage(min(50, unit.getDamage() + iDamage - unit.getExperience()/10 - unit.baseCombatStr()/2), iBarbarian)
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
			pPlot.setUpgradeProgress(0)
			iImprovement = pPlot.getImprovementType()
			if iImprovement == iTown:
				pPlot.setImprovementType(iVillage)
			if pPlot.isCity():
				if (city.getX(), city.getY()) == (x, y):
					self.killUnitsByPlague(city, pPlot, 0, 100, 0)


	def isVulnerable(self, iPlayer):
		if iPlayer >= iNumMajorPlayers:
			if -10 < data.players[iPlayer].iPlagueCountdown <= 0: #more vulnerable
				return True
		else:
			pPlayer = gc.getPlayer(iPlayer)
			if data.players[iPlayer].iPlagueCountdown: #vulnerable
				if not gc.getTeam(pPlayer.getTeam()).isHasTech(iMedicine):
					iHealth = self.calculateHealth(iPlayer)
					if iHealth < 14: #no spread for iHealth >= 74 years
						return True
					else:
						#print ("immune", iPlayer)
						pass
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
					if not gc.getTeam(gc.getPlayer(iNewOwner).getTeam()).isHasTech(iMedicine): #but not permanent immunity
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
					if (otherCity.getX(), otherCity.getY()) != (x, y): #because the city razed still has the plague
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
