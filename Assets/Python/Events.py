from BugEventManager import g_eventManager as events
import inspect

from Core import *

from GoalHandlers import event_handler_registry


victory_handlers = appenddict()


def handler(event):
	def handler_decorator(func):
		arg_names = inspect.getargspec(func)[0]
		
		def handler_func(args):
			return func(*args[:len(arg_names)])
			
		handler_func.__name__ = func.__name__
		handler_func.__module__ = func.__module__
		handler_func.func_name = func.func_name
				
		events.addEventHandler(event, handler_func)
		return handler_func
		
	return handler_decorator
	
	
def noop(*args, **kwargs):
	pass


def popup_handler(event_id):
	def handler_decorator(func):
		events.addCustomEvent(event_id, func.__name__, func, noop)
		return func
		
	return handler_decorator


def register_victory_handler(event, handler):
	victory_handlers[event].append(handler)
	events.addEventHandler(event, handler)
	

def reset_victory_handlers():
	global victory_handlers
	for event, handlers in victory_handlers.items():
		for handler in handlers:
			if events.hasEventHandler(event, handler):
				events.removeEventHandler(event, handler)
	
	victory_handlers = appenddict()


events.addEvent("firstCity")
events.addEvent("capitalMoved")
events.addEvent("wonderBuilt")
events.addEvent("immigration")
events.addEvent("collapse")
events.addEvent("periodChange")
events.addEvent("playerPeriodChange")
events.addEvent("birth")
events.addEvent("resurrection")
events.addEvent("switch")
events.addEvent("enslave")
events.addEvent("combatGold")
events.addEvent("combatFood")
events.addEvent("sacrificeHappiness")
events.addEvent("prepareBirth")
events.addEvent("flip")
events.addEvent("conquerors")


@handler("buildingBuilt")
def capitalMovedOnPalaceBuilt(city, iBuilding):
	if iBuilding == iPalace:
		events.fireEvent("capitalMoved", city)


@handler("firstCity")
def capitalMovedOnFirstCity(city):
	events.fireEvent("capitalMoved", city)


@handler("cityAcquired")
def capitalMovedOnCityAcquired(iOwner, iNewOwner, city):
	capital_city = capital(iOwner)
	if capital_city and not at(capital_city, city):
		events.fireEvent("capitalMoved", capital_city)


@handler("cityAcquiredAndKept")
def firstCityOnCityAcquiredAndKept(iPlayer, city):
	if city.isCapital():
		events.fireEvent("firstCity", city)


@handler("cityBuilt")
def firstCityOnCityBuilt(city):
	if city.isCapital():
		events.fireEvent("firstCity", city)


@handler("buildingBuilt")
def wonderBuiltOnBuildingBuilt(city, iBuilding):
	if isWorldWonderClass(infos.building(iBuilding).getBuildingClassType()):
		events.fireEvent("wonderBuilt", city, iBuilding)
		

@handler("PythonReloaded")
def resetHandlersOnPythonReloaded():
	event_handler_registry.reset()


@handler("OnLoad")
def resetHandlersOnLoad():
	event_handler_registry.reset()