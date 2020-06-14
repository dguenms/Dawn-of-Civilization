from Consts import *
from BugEventManager import g_eventManager as events
import inspect


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


events.addEvent("firstCity")
events.addEvent("capitalMoved")
events.addEvent("wonderBuilt")
events.addEvent("immigration")
events.addEvent("collapse")


@handler("buildingBuilt")
def capitalMovedOnPalaceBuilt(city, iBuilding):
	if iBuilding == iPalace:
		events.fireEvent("capitalMoved", city)


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