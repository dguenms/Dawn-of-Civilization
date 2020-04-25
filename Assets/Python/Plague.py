# Rhye's and Fall of Civilization - Historical Victory Goals


from CvPythonExtensions import *
import CvUtil
import PyHelpers
#import Popup
#import cPickle as pickle
from Consts import *
from StoredData import data #edead
from RFCUtils import *
import random

from Core import *

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

iDuration = 6

class Plague:

######################################
### Main methods (Event-Triggered) ###
######################################


	def setup(self):
		for iPlayer in players.major():
			data.players[iPlayer].iPlagueCountdown = -turns(iImmunity)
			
		data.lGenericPlagueDates[0] = 80
		data.lGenericPlagueDates[2] = 300 # safe value to prevent plague at start of 1700 AD scenario
		
		if scenario() == i3000BC:
			data.lGenericPlagueDates[0] = year(400).deviate(20)
			
		data.lGenericPlagueDates[1] = year(1300).deviate(20)
		
		# Avoid interfering with the Indian UHV
		if player(iIndia).isHuman() and data.lGenericPlagueDates[1] <= year(1200):
			data.lGenericPlagueDates[1] = year(1200) + 1
		
		if scenario() != i1700AD:
			data.lGenericPlagueDates[2] = year(1650).deviate(20)
			
		data.lGenericPlagueDates[3] = year(1850).deviate(20)

		undoPlague = rand(8)
		if undoPlague <= 3:
			data.lGenericPlagueDates[undoPlague] = -1
			
	


	def checkTurn(self, iGameTurn):
		if data.bNoPlagues:
			return

		for iPlayer in players.all().barbarian():
			if player(iPlayer).isAlive():
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
					for iPlayer in players.all().barbarian():
						if data.players[iPlayer].iPlagueCountdown > 0:
							iInfectedCounter += 1
					if iInfectedCounter == 1:
						#print ("new plague again1")
						self.startPlague(iPlague)
			if iPlague == 2 or iPlague == 3:
				if iGameTurn == iPlagueDate + 8:
					iInfectedCounter = 0
					for iPlayer in players.all().barbarian():
						if data.players[iPlayer].iPlagueCountdown > 0:
							iInfectedCounter += 1
					if iInfectedCounter <= 2:
						#print ("new plague again2")
						self.startPlague(iPlague)

	def checkPlayerTurn(self, iGameTurn, iPlayer):
		if data.bNoPlagues:
			return

		if iPlayer in players.all():
			if data.players[iPlayer].iPlagueCountdown > 0:
				self.processPlague(iPlayer)



	def startPlague(self, iPlagueCounter):
		iWorstPlayer = -1
		iWorstHealth = 200
		
		for iPlayer in players.major().alive().where(self.isVulnerable):
			pPlayer = player(iPlayer)
			iHealth = self.calculateHealth(iPlayer) / 2
			
			if pPlayer.calculateTotalCityHealthiness() > 0:
				iHealth += rand(40)
				if iPlagueCounter == 2: #medieval black death
					if civ(iPlayer) in dCivGroups[iCivGroupEurope]:
						iHealth -= 5
						
			if iHealth < iWorstHealth:
				iWorstHealth = iHealth
				iWorstPlayer = iPlayer
				
		if iWorstPlayer != -1:
			city = cities.owner(iWorstPlayer).random()
			if city:
				self.spreadPlague(iWorstPlayer)
				self.infectCity(city)
				self.announceForeignPlagueSpread(city)


	def preStopPlague(self, iPlayer):
		iModifier = 0
		for city in cities.owner(iPlayer).where(lambda city: city.hasBuilding(iPlague)):
			if rand(100) > 30 - 5 * city.healthRate(False, 0) + iModifier:
				city.setHasRealBuilding(iPlague, False)
				iModifier += 5


	def stopPlague(self, iPlayer):
		data.players[iPlayer].iPlagueCountdown = -turns(iImmunity)
		if data.players[iPlayer].bFirstContactPlague:
			data.players[iPlayer].iPlagueCountdown = -turns(iImmunity-30)
		data.players[iPlayer].bFirstContactPlague = False
		for city in cities.owner(iPlayer):
			city.setHasRealBuilding(iPlague, False)
			
	def losePopulation(self, city):
		if city.getPopulation() <= 1: return
		
		iHealth = city.healthRate(False, 0)	
		if rand(100) > 40 + 5 * iHealth:
			city.changePopulation(-1)
			
	def spreadToVassals(self, iPlayer):
		if data.players[iPlayer].bFirstContactPlague: return
		
		for iLoopPlayer in players.major().where(self.isVulnerable):
			if team(iPlayer).isVassal(iLoopPlayer) or team(iLoopPlayer).isVassal(iPlayer):
				if data.players[iLoopPlayer].iPlagueCountdown > 2:
					if player(iLoopPlayer).getNumCities() > 0:
						capital = player(iLoopPlayer).getCapitalCity()
						self.spreadPlague(iLoopPlayer)
						self.infectCity(capital)
						
	def spreadToSurroundings(self, city):
		iPlayer = city.getOwner()
		
		# do not spread if plague is almost over
		if data.players[iPlayer].iPlagueCountdown <= 2: return
	
		for plot in plots.surrounding(city, radius=2):
			if not plot.isOwned(): continue
			if location(city) == location(plot): continue
			
			if plot.getOwner() == iPlayer:
				if plot.isCity():
					plotCity = plot.getPlotCity()
					if not plotCity.isHasRealBuilding(iPlague):
						self.infectCity(plotCity)
			
			else:
				if data.players[iPlayer].bFirstContactPlague: continue
				
				if self.isVulnerable(plot.getOwner()):
					self.spreadPlague(plot.getOwner())
					self.infectCitiesNear(plot.getOwner(), plot)
					
	def damageNearbyUnits(self, city):
		for plot in plots.surrounding(city, radius=3):
			iDistance = distance(city, plot)
			
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
						
	def spreadBetweenCities(self, iPlayer, sourceCities, targetCities):
		if data.players[iPlayer].iPlagueCountdown <= 2: return
		
		target = targetCities.where(lambda city: sourceCities.any(lambda source: source.isConnectedTo(city) and distance(source, city) <= 6)).random()
		if target:
			self.infectCity(target)

	def processPlague(self, iPlayer):
		# collect cities with and without plague
		infectedCities, uninfectedCities = cities.owner(iPlayer).split(lambda city: city.isHasRealBuilding(iPlague))
			
		for city in infectedCities:
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
		self.spreadBetweenCities(iPlayer, infectedCities, uninfectedCities)


	def killUnitsByPlague(self, city, pPlot, baseValue, iDamage, iPreserveDefenders):
		iOwner = city.getOwner()
		pOwner = player(city)
		teamOwner = team(city)
		
		#deadly plague when human player isn't born yet, will speed up the loading
		if turn() < year(dBirth[active()]) + turns(20):
			iDamage += 10
			baseValue -= 5

		iPreserveHumanDefenders = iPreserveDefenders
		if iPreserveDefenders > 0:
			if not pOwner.isHuman():
				if teamOwner.isAtWar(active()):
					iPreserveDefenders += 2
				elif any(civ(iOwner) in lCivGroup and civ() in lCivGroup for lCivGroup in dCivGroups.values()):
					iPreserveDefenders += 1
							
		# TODO: look from overlap
		for unit in units.at(pPlot):
			if player(unit).isHuman():
				if iPreserveHumanDefenders > 0:
					if isDefenderUnit(unit):
						iPreserveHumanDefenders -= 1
						if pPlot.getNumUnits() <= iPreserveDefenders:
							iMaxDamage = 50
							if unit.workRate(100) > 0 and not unit.canFight(): iMaxDamage = 100
							unit.setDamage(min(iMaxDamage, unit.getDamage() + iDamage - 20), iBarbarianPlayer)
						continue
			elif iPreserveDefenders > 0:
				if isDefenderUnit(unit):
					iPreserveDefenders -= 1
					if pPlot.getNumUnits() <= iPreserveDefenders and team(unit).isAtWar(active()):
						iMaxDamage = 50
						if unit.workRate(100) > 0 and not unit.canFight(): iMaxDamage = 100
						unit.setDamage(min(iMaxDamage, unit.getDamage() + iDamage - 20), iBarbarianPlayer)
					continue
					
			if isMortalUnit(unit):
				iThreshold = baseValue + 5 * city.healthRate(False, 0)
				
				if teamOwner.isAtWar(active()) and not is_minor(iOwner):
					if unit.getOwner() == iOwner:
						iDamage *= 3
						iDamage /= 4
					
				if data.players[city.getOwner()].bFirstContactPlague:
					if civ(unit) not in lNewOldWorld and not is_minor(unit):
						iDamage /= 2
						
				if rand(100) > iThreshold:
					iMaxDamage = 50
					if unit.workRate(100) > 0 and not unit.canFight(): iMaxDamage = 100
					unit.setDamage(min(iMaxDamage, unit.getDamage() + iDamage - unit.getExperience()/10 - unit.baseCombatStr()/2), iBarbarianPlayer)
					break


	def infectCity(self, city):
		if civ(city) == iCongo and year() <= year(1650): return	# Leoreth: don't let plague mess up the UHV
		elif civ(city) == iMali and year() <= year(1500): return	# same for Mali
		
		city.setHasRealBuilding(iPlague, True)
		message(city.getOwner(), 'TXT_KEY_PLAGUE_SPREAD_CITY', city.getName(), sound='AS2D_PLAGUE', color=iLime)
		
		for pPlot in plots.surrounding(city, radius=2):
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
				
				if location(pPlot) == location(city):
					self.killUnitsByPlague(city, pPlot, 0, 100, 0)


	def isVulnerable(self, iPlayer):
		if is_minor(iPlayer) and -10 < data.players[iPlayer].iPlagueCountdown <= 0: #more vulnerable
			return True
				
		pPlayer = player(iPlayer)
			
		if team(iPlayer).isHasTech(iMicrobiology): return False
		
		if civ(iPlayer) in lBioNewWorld and not data.lFirstContactConquerors[lBioNewWorld.index(civ(iPlayer))]: return False
			
		if data.players[iPlayer].iPlagueCountdown == 0: #vulnerable
			if not team(iPlayer).isHasTech(iMicrobiology):
				iHealth = self.calculateHealth(iPlayer)
				if iHealth < 14: #no spread for iHealth >= 74 years
					return True
					
		return False


	def spreadPlague(self, iPlayer):
		pPlayer = player(iPlayer)
		iHealth = self.calculateHealth(iPlayer) / 7 #duration range will be -4 to +4 for 30 to 90
		data.players[iPlayer].iPlagueCountdown = min(9, iDuration - iHealth)
		print ("spreading plague to", iPlayer)


	def calculateHealth(self, iPlayer):
		pPlayer = player(iPlayer)
		if pPlayer.calculateTotalCityHealthiness() > 0:
			return int((1.0 * pPlayer.calculateTotalCityHealthiness()) / (pPlayer.calculateTotalCityHealthiness() + \
				pPlayer.calculateTotalCityUnhealthiness()) * 100) - 60
		return -30


	def infectCitiesNear(self, iPlayer, tile):
		for city in cities.owner(iPlayer):
			if distance(city, tile) <= 3:
				self.infectCity(city)
				self.announceForeignPlagueSpread(city)


	def onCityAcquired(self, iOldOwner, iNewOwner, city):
		if city.hasBuilding(iPlague):
			if not data.players[iOldOwner].bFirstContactPlague: #don't infect if first contact plague
				if data.players[iNewOwner].iPlagueCountdown <= 0 and year() > year(dBirth[iNewOwner]) + turns(iImmunity): #skip immunity in this case (to prevent expoiting of being immune to conquer weak civs), but not for the new born civs
					if not team(iNewOwner).isHasTech(iMicrobiology): #but not permanent immunity
						print("acquiring plague")
						self.spreadPlague(iNewOwner)
						self.infectCitiesNear(iNewOwner, city)
						return
			city.setHasRealBuilding(iPlague, False)


	def onCityRazed(self, city, iNewOwner):
		if city.hasBuilding(iPlague):
			if data.players[iNewOwner].iPlagueCountdown > 0:
				if cities.owner(iNewOwner).without(city).none(lambda other: other.hasBuilding(iPlague)):
					data.players[iNewOwner].iPlagueCountdown = 0


	def onFirstContact(self, iTeamX, iHasMetTeamY):
		if data.bNoPlagues:
			return

		if year() > year(dBirth[iAztecs]) + turns(2) and year() < year(1800):
			iOldWorldCiv = -1
			iNewWorldCiv = -1
			if civ(iTeamX) in lBioNewWorld and civ(iHasMetTeamY) not in lBioNewWorld and not is_minor(iHasMetTeamY):
				iNewWorldCiv = iTeamX
				iOldWorldCiv = iHasMetTeamY
			if iOldWorldCiv != -1 and iNewWorldCiv != -1:
				pNewWorldCiv = player(iNewWorldCiv)
				if data.players[iNewWorldCiv].iPlagueCountdown == 0: #vulnerable
					#print ("vulnerable", iNewWorldCiv)
					if not team(iNewWorldCiv).isHasTech(iBiology):
						city = cities.owner(iNewWorldCiv).random()
						if city:
							iHealth = self.calculateHealth(iNewWorldCiv)
							if iHealth < 10: #no spread for iHealth >= 70 years
								iHealth /= 10
								if rand(100) > 30 + 5*iHealth:
									data.players[iNewWorldCiv].iPlagueCountdown = iDuration - iHealth
									data.players[iNewWorldCiv].bFirstContactPlague = True
									#print ("spreading (through first contact) plague to", iNewWorldCiv)
									self.infectCity(city)
									self.announceForeignPlagueSpread(city)


	def announceForeignPlagueSpread(self, city):
		iOwner = city.getOwner()
		if player().canContact(iOwner) and active() != iOwner and city.isRevealed(active(), False):
			message(active(), 'TXT_KEY_PLAGUE_SPREAD_CITY', '%s (%s)' % (city.getName(), adjective(iOwner)), sound='AS2D_PLAGUE', color=iLime)


	def onTechAcquired(self, iTech, iPlayer):
		if data.players[iPlayer].iPlagueCountdown > 1:
			data.players[iPlayer].iPlagueCountdown = 1
