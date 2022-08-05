from Core import *

from inspect import ismethod

from Events import events


class Handlers(object):

	def __init__(self):
		self.handlers = []
		self.other_handlers = []
		self.any_handlers = []
		
	def __len__(self):
		return len(self.handlers) + len(self.other_handlers) + len(self.any_handlers)
	
	def add(self, event, func):
		self.handlers.append((event, func))
	
	def add_other(self, event, func):
		self.other_handlers.append((event, func))
	
	def add_any(self, event, func):
		self.any_handlers.append((event, func))


class EventHandlerRegistry(object):

	def __init__(self):
		self.registered = appenddict()

	def applicable(self, goal, iPlayer):
		return iPlayer in goal.evaluator
	
	def applicable_other(self, goal, iPlayer):
		return iPlayer not in goal.evaluator
	
	def applicable_any(self, goal, iPlayer):
		return True

	def get(self, goal, applicable, event, func):
		if hasattr(self, event):
			handler_func = getattr(self, event)
			if ismethod(handler_func):
				return handler_func(goal, applicable, func)
		
		raise ValueError("No handler available for event '%s'" % event)
		
	def register_handlers(self, instance, handlers, goal, applicable):
		for event, handler in handlers:
			handler_func = self.get(goal, applicable, event, handler)
			self.registered[instance].append((event, handler_func))
			
			events.addEventHandler(event, handler_func)
	
	def register(self, instance, goal):
		self.register_handlers(instance, instance.handlers.handlers, goal, self.applicable)
		self.register_handlers(instance, instance.handlers.other_handlers, goal, self.applicable_other)
		self.register_handlers(instance, instance.handlers.any_handlers, goal, self.applicable_any)
		
	def deregister(self, instance):
		if instance in self.registered:
			for event, handler_func in self.registered[instance]:
				events.removeEventHandler(event, handler_func)
			
			del self.registered[instance]
	
	def BeginPlayerTurn(self, goal, applicable, func):
		def BeginPlayerTurn((iGameTurn, iPlayer)):
			if applicable(goal, iPlayer):
				func(goal, iGameTurn, iPlayer)
		
		return BeginPlayerTurn
	
	def blockade(self, goal, applicable, func):
		def blockade((iPlayer, iGold)):
			if applicable(goal, iPlayer):
				func(goal, iGold)
		
		return blockade
		
	def buildingBuilt(self, goal, applicable, func):
		def buildingBuilt((city, iBuilding)):
			if applicable(goal, city.getOwner()):
				func(goal, city, iBuilding)
		
		return buildingBuilt
	
	def cityAcquired(self, goal, applicable, func):
		def cityAcquired((iOwner, iPlayer, city, bConquest, bTrade)):
			if applicable(goal, iPlayer):
				func(goal, city, bConquest)
		
		return cityAcquired
		
	def cityAcquiredAndKept(self, goal, applicable, func):
		def cityAcquiredAndKept((iPlayer, city)):
			if applicable(goal, iPlayer):
				func(goal, city)
		
		return cityAcquiredAndKept
	
	def cityBuilt(self, goal, applicable, func):
		def cityBuilt((city,)):
			if applicable(goal, city.getOwner()):
				func(goal, city)
		
		return cityBuilt
	
	def cityCaptureGold(self, goal, applicable, func):
		def cityCaptureGold((city, iPlayer, iGold)):
			if applicable(goal, iPlayer):
				func(goal, iGold)
		
		return cityCaptureGold
	
	def cityLost(self, goal, applicable, func):
		def cityLost((city,)):
			if applicable(goal, city.getOwner()):
				func(goal)

		return cityLost
		
	def cityRazed(self, goal, applicable, func):
		def cityRazed((city, iPlayer)):
			if applicable(goal, iPlayer):
				func(goal)
		
		return cityRazed
	
	def combatFood(self, goal, applicable, func):
		def combatFood((iPlayer, unit, iFood)):
			if applicable(goal, iPlayer):
				func(goal, iFood)
		
		return combatFood
	
	def combatGold(self, goal, applicable, func):
		def combatGold((iPlayer, unit, iGold)):
			if applicable(goal, iPlayer):
				func(goal, iGold)
		
		return combatGold
	
	def combatResult(self, goal, applicable, func):
		def combatResult((winningUnit, losingUnit)):
			if applicable(goal, winningUnit.getOwner()):
				func(goal, losingUnit)
		
		return combatResult
	
	def corporationSpread(self, goal, applicable, func):
		def corporationSpread((iCorporation, iPlayer, city)):
			if applicable(goal, iPlayer):
				func(goal, iCorporation)
		
		return corporationSpread
	
	def enslave(self, goal, applicable, func):
		def enslave((iPlayer, losingUnit)):
			if applicable(goal, iPlayer):
				func(goal, losingUnit)
		
		return enslave
	
	def firstContact(self, goal, applicable, func):
		def firstContact((iTeam, iHasMetTeam)):
			if applicable(goal, team(iTeam).getLeaderID()):
				func(goal, team(iHasMetTeam).getLeaderID())
		
		return firstContact
	
	def greatPersonBorn(self, goal, applicable, func):
		def greatPersonBorn((unit, iPlayer, city)):
			if applicable(goal, iPlayer):
				func(goal, unit)
		
		return greatPersonBorn
	
	def peaceBrokered(self, goal, applicable, func):
		def peaceBrokered((iBroker, iPlayer1, iPlayer2)):
			if applicable(goal, iBroker):
				func(goal)
		
		return peaceBrokered
	
	def playerChangeStateReligion(self, goal, applicable, func):
		def playerChangeStateReligion((iPlayer, iNewReligion, iOldReligion)):
			if applicable(goal, iPlayer):
				func(goal, iNewReligion)
		
		return playerChangeStateReligion
	
	def playerGoldTrade(self, goal, applicable, func):
		def playerGoldTrade((iFrom, iTo, iGold)):
			if applicable(goal, iTo):
				func(goal, iGold)
		
		return playerGoldTrade
	
	def playerSlaveTrade(self, goal, applicable, func):
		def playerSlaveTrade((iPlayer, iGold)):
			if applicable(goal, iPlayer):
				func(goal, iGold)
		
		return playerSlaveTrade
	
	def projectBuilt(self, goal, applicable, func):
		def projectBuilt((city, iProject)):
			if applicable(goal, city.getOwner()):
				func(goal, iProject)
		
		return projectBuilt
	
	def sacrificeHappiness(self, goal, applicable, func):
		def sacrificeHappiness((iPlayer, city)):
			if applicable(goal, iPlayer):
				func(goal)
		
		return sacrificeHappiness
	
	def techAcquired(self, goal, applicable, func):
		def techAcquired((iTech, iTeam, iPlayer, bAnnounce)):
			if applicable(goal, iPlayer):
				func(goal, iTech)
	
		return techAcquired
	
	def tradeMission(self, goal, applicable, func):
		def tradeMission((iUnit, iPlayer, iX, iY, iGold)):
			if applicable(goal, iPlayer):
				func(goal, (iX, iY), iGold)
		
		return tradeMission
	
	def unitPillage(self, goal, applicable, func):
		def unitPillage((unit, iImprovement, iRoute, iPlayer, iGold)):
			if applicable(goal, iPlayer):
				func(goal, iGold)
		
		return unitPillage
	
	def vassalState(self, goal, applicable, func):
		def vassalState((iMaster, iVassal, bVassal, bCapitulated)):
			if applicable(goal, team(iMaster).getLeaderID()):
				func(goal)
		
		return vassalState
		
		
		
event_handler_registry = EventHandlerRegistry()