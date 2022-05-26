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
		for event, handler_func in self.registered[instance]:
			events.removeEventHandler(event, handler_func)
	
	def BeginPlayerTurn(self, goal, applicable, func):
		def BeginPlayerTurn((iGameTurn, iPlayer)):
			if applicable(goal, iPlayer):
				func(goal, iGameTurn)
		
		return BeginPlayerTurn
		
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
	
	def peaceBrokered(self, goal, applicable, func):
		def peaceBrokered((iBroker, iPlayer1, iPlayer2)):
			if applicable(goal, iBroker):
				func(goal)
		
		return peaceBrokered
	
	def techAcquired(self, goal, applicable, func):
		def techAcquired((iTech, iTeam, iPlayer, bAnnounce)):
			if applicable(goal, iPlayer):
				func(goal, iTech)
	
		return techAcquired
		
		
		
event_handler_registry = EventHandlerRegistry()