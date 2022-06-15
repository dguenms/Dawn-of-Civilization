from Core import *
from VictoryTypes import *
from BaseRequirements import *

from Civics import isCommunist

import heapq


# Third Spanish UHV goal
class AreaNoStateReligion(Requirement):

	TYPES = (AREA, RELIGION_ADJECTIVE)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_ALLOW"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_AREA_NO_STATE_RELIGION"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_AREA_NO_STATE_RELIGION"
	
	def __init__(self, area, iReligion, **options):
		Requirement.__init__(self, area, iReligion, **options)
		
		self.area = area
		self.iReligion = iReligion
	
	def fulfilled(self, evaluator):
		return self.area.cities().none(lambda city: player(city).getStateReligion() == self.iReligion)


# Third Russian UHV goal
class Communist(Requirement):

	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_ADOPT"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_COMMUNIST"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_COMMUNIST"

	def fulfilled(self, evaluator):
		return evaluator.any(lambda p: isCommunist(p))
	

# Second Greek UHV goal
# Second Phoenician UHV goal
# Second Tamil UHV goal
# Second Japanese UHV goal
# First Viking UHV goal
# Second Arabian UHV goal
class Control(Requirement):
	
	TYPES = (AREA,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CONTROL"
	
	def __init__(self, area, **options):
		Requirement.__init__(self, area, **options)
		
		self.area = area
	
	def fulfilled(self, evaluator):
		return self.area.cities().all_if_any(lambda city: city.getOwner() in evaluator)


# Third Ethiopian UHV goal
class MoreReligion(Requirement):

	TYPES = (AREA, RELIGION_ADJECTIVE, RELIGION_ADJECTIVE)

	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_ENSURE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_MORE_RELIGION"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_MORE_RELIGION"
	
	def __init__(self, area, iOurReligion, iOtherReligion, **options):
		Requirement.__init__(self, area, iOurReligion, iOtherReligion, **options)
		
		self.area = area
		self.iOurReligion = iOurReligion
		self.iOtherReligion = iOtherReligion
		
	def count_religion_cities(self, iReligion):
		return self.area.cities().religion(iReligion).count()
	
	def fulfilled(self, evaluator):
		return self.count_religion_cities(self.iOurReligion) > self.count_religion_cities(self.iOtherReligion)
		
	def progress_text_religion(self, iReligion):
		return "%s: %d" % (text(self.PROGR_KEY, RELIGION_ADJECTIVE.format(iReligion)), self.count_religion_cities(iReligion))
	
	def progress_text(self, **options):
		return "%s %s" % (self.progress_text_religion(self.iOurReligion), self.progress_text_religion(self.iOtherReligion))


# Second Russian UHV goal
class Project(Requirement):

	TYPES = (PROJECT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_FIRST_COMPLETE"
	
	def __init__(self, iProject, **options):
		Requirement.__init__(self, iProject, **options)
		
		self.iProject = iProject
		
		self.handle("projectBuilt", self.check_project_built)
		self.expire("projectBuilt", self.expire_project_built)
	
	def check_project_built(self, goal, iProject):
		if self.iProject == iProject:
			goal.check()
	
	def expire_project_built(self, goal, iProject):
		if self.iProject == iProject:
			goal.expire()
	
	def fulfilled(self, evaluator):
		return evaluator.any(lambda p: team(p).getProjectCount(self.iProject) > 0)


# First Inca UHV goal
class Route(Requirement):

	TYPES = (AREA, ROUTES)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_BUILD"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_ROUTE"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_ROUTE"
	
	def __init__(self, area, routes, **options):
		Requirement.__init__(self, area, routes, **options)
		
		self.area = area
		self.routes = routes
	
	def fulfilled(self, evaluator):
		return self.area.create().all(lambda p: p.getOwner() in evaluator and p.getRouteType() in self.routes)


# Second Turkic UHV goal
# First Russian UHV goal
class RouteConnection(Requirement):

	GLOBAL_TYPES = (ROUTES, AREA)
	TYPES = (AREA,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CREATE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_ROUTE_CONNECTION"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_ROUTE_CONNECTION"
	
	def __init__(self, routes, starts, targets, start_owners=False, **options):
		Requirement.__init__(self, routes, starts, targets, **options)
		
		self.routes = routes
		self.starts = starts
		self.targets = targets
		
		self.start_owners = start_owners
	
	def fulfilled(self, evaluator):
		if not evaluator.any(lambda iPlayer: any(team(iPlayer).isHasTech(self.route_tech(iRoute)) for iRoute in self.routes)):
			return False
		
		return any(self.connected(start.plot(), evaluator) for start in self.starts.cities())
		
	def route_tech(self, iRoute):
		iBuild = infos.builds().where(lambda iBuild: infos.build(iBuild).getRoute() == iRoute).first()
		return infos.build(iBuild).getTechPrereq()
	
	def connected(self, start, evaluator):
		if not self.valid(start, evaluator):
			return False
		
		if start in self.targets:
			return True
		
		targets = self.targets.where(lambda plot: self.valid(plot, evaluator))
		if not targets:
			return False
		
		nodes = [(targets.closest_distance(start), location(start))]
		heapq.heapify(nodes)
		
		visited = set()
		
		while nodes:
			heuristic, node = heapq.heappop(nodes)
			visited.add((heuristic, node))
			
			for plot in plots_.surrounding(node).where(lambda p: self.valid(p, evaluator)):
				if plot.isCity() and plot.getOwner() in evaluator and plot in targets:
					return True
				
				tuple = (targets.closest_distance(plot), location(plot))
				if tuple not in visited and tuple not in nodes:
					heapq.heappush(nodes, tuple)
		
		return False
	
	def valid_owner(self, plot, evaluator):
		if plot.getOwner() in evaluator:
			return True
		
		if self.start_owners and plot.getOwner() in self.starts.cities().owners():
			return True
		
		return False
		
	def valid(self, plot, evaluator):
		return self.valid_owner(plot, evaluator) and (plot.isCity() or plot.getRouteType() in self.routes)
		
		
# First Harappan UHV goal
class TradeConnection(Requirement):

	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_ESTABLISH"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_TRADE_CONNECTION"
	
	def fulfilled(self, evaluator):
		other_players = players.major().alive().without(evaluator.players())
		return evaluator.any(lambda iPlayer: other_players.any(lambda iOtherPlayer: player(iPlayer).canContact(iOtherPlayer) and player(iPlayer).canTradeNetworkWith(iOtherPlayer)))


# Second Egyptian UHV goal
# Third Greek UHV goal
# Third Polynesian UHV goal
# Second Mayan UHV goal
# Second Moorish UHV goal
# Third French UHV goal
# First Khmer UHV goal
# Second Mandinka UHV goal
# First Italian UHV goal
class Wonder(Requirement):

	TYPES = (BUILDING,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_BUILD"
	
	def __init__(self, iBuilding, **options):
		Requirement.__init__(self, iBuilding, **options)
		
		self.iBuilding = iBuilding
		
		self.handle("buildingBuilt", self.check_building_built)
		self.expire("buildingBuilt", self.expire_building_built)
	
	def check_building_built(self, goal, city, iBuilding):
		if self.iBuilding == iBuilding:
			goal.check()
	
	def expire_building_built(self, goal, city, iBuilding):
		if self.iBuilding == iBuilding:
			goal.expire()
	
	def fulfilled(self, evaluator):
		return evaluator.any(lambda iPlayer: player(iPlayer).isHasBuilding(self.iBuilding))