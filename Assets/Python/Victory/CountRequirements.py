from Core import *
from BaseRequirements import *

from Civics import isCommunist
from Arguments import base_building


# Second Ethiopian UHV goal
# Third Holy Roman UHV goal
# Third Russian UHV goal
# Third Jewish URV goal
# First Confucian URV goal
class AttitudeCount(ThresholdRequirement):

	TYPES = (ATTITUDE, COUNT)
	
	DESC_KEY = "TXT_KEY_VICTORY_DESC_ATTITUDE_COUNT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_ATTITUDE_COUNT"
	
	def __init__(self, iAttitude, iRequired, civs=None, iReligion=None, iStateReligion=None, bIndependent=False, bCommunist=False, **options):
		ThresholdRequirement.__init__(self, as_int(iAttitude), iRequired, civs=civs, iReligion=iReligion, iStateReligion=iStateReligion, bIndependent=bIndependent, bCommunist=bCommunist, **options)
		
		self.civs = civs
		self.iReligion = iReligion
		self.iStateReligion = iStateReligion
		self.bIndependent = bIndependent
		self.bCommunist = bCommunist
		
	def valid(self, iPlayer, iOtherPlayer, iAttitude):
		if not player(iPlayer).canContact(iOtherPlayer):
			return False
		
		if self.bIndependent and team(iOtherPlayer).isAVassal():
			return False
		
		if self.bCommunist and not isCommunist(iOtherPlayer):
			return False
		
		if self.civs and civ(iOtherPlayer) not in self.civs:
			return False
		
		if self.iReligion is not None and not cities.owner(iOtherPlayer).religion(self.iReligion):
			return False
		
		if self.iStateReligion is not None:
			if isinstance(self.iStateReligion, Aggregate):
				lStateReligions = self.iStateReligion.items
			else:
				lStateReligions = [self.iStateReligion]
			
			if player(iOtherPlayer).getStateReligion() not in lStateReligions:
				return False
		
		return player(iOtherPlayer).AI_getAttitude(iPlayer) >= iAttitude
	
	def value(self, iPlayer, iAttitude):
		return players.major().alive().where(lambda p: self.valid(iPlayer, p, iAttitude)).count()
	
	def additional_formats(self):
		civilizations = text("TXT_KEY_VICTORY_CIVILIZATIONS")
		civilizations = qualify(civilizations, "TXT_KEY_VICTORY_COMMUNIST", self.bCommunist)
		civilizations = qualify(civilizations, "TXT_KEY_VICTORY_INDEPENDENT", self.bIndependent)
		civilizations = qualify_adjective(civilizations, RELIGION_ADJECTIVE, self.iStateReligion)
		civilizations = in_area(civilizations, self.civs)
		civilizations = with_religion_in_cities(civilizations, self.iReligion)
		
		return [civilizations]


# Second Khmer UHV goal
class AveragePopulation(ThresholdRequirement):

	TYPES = (COUNT,)
	
	DESC_KEY = "TXT_KEY_VICTORY_DESC_AVERAGE_POPULATION"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_AVERAGE_POPULATION"
	
	def value(self, iPlayer):
		iNumCities = player(iPlayer).getNumCities()
		if iNumCities <= 0:
			return 0
		
		return player(iPlayer).getTotalPopulation() / iNumCities


# Second Harappan UHV goal
# First Chinese UHV goal
# First Indian UHV goal
# Second Indian UHV goal
# Second Persian UHV goal
# Third Persian UHV goal
# First Roman UHV goal
# Second Ethiopian UHV goal
# First Korean UHV goal
# First Khmer UHV goal
# First Holy Roman UHV goal
# Third Polish UHV goal
# First Inca UHV goal
# Second Aztec UHV goal
# First Mughal UHV goal
# First Mexican UHV goal
# First Orthodox URV goal
# Second Catholic URV goal
# Third Islamic URV goal
# First Secular URV goal
# Second Secular URV goal
# First Pagan URV goal
# Third Olympian URV goal
class BuildingCount(ThresholdRequirement):

	TYPES = (BUILDING, COUNT)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CONTROL"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_COUNT"
	
	SUBJECT_DESC_KEYS = {
		WORLD: "TXT_KEY_VICTORY_DESC_MAKE_SURE_IN_THE_WORLD"
	}
	
	def __init__(self, iBuilding, *args, **options):
		ThresholdRequirement.__init__(self, iBuilding, *args, **options)
		
		self.iBuilding = base_building(iBuilding)
		
		self.handle("cityAcquired", self.check)
		self.handle("buildingBuilt", self.check_building_built)
	
	def check_building_built(self, goal, city, iBuilding):
		if base_building(iBuilding) == self.iBuilding:
			goal.check()
	
	def value(self, iPlayer, iBuilding):
		if iBuilding is NON_EXISTING:
			return 0
	
		return player(iPlayer).countNumBuildings(unique_building(iPlayer, iBuilding))
	
	def description(self):
		if not isinstance(self.iBuilding, (Aggregate, DeferredArgument)) and isWonder(self.iBuilding):
			return BUILDING.format(self.iBuilding)
	
		return Requirement.description(self, bPlural=self.bPlural)
		
	def progress(self, evaluator):
		if not self.bPlural:
			return "%s %s" % (self.indicator(evaluator), capitalize(BUILDING.format(self.iBuilding)))
		
		return "%s %s: %s" % (self.indicator(evaluator), text(self.PROGR_KEY, capitalize(BUILDING.format(self.iBuilding, bPlural=True))), self.progress_value(evaluator))


# First Phoenician UHV goal
# First Ottoman UHV goal
# Third Brazilian UHV goal
# Second Confucian URV goal
class CityBuildingCount(ThresholdRequirement):

	GLOBAL_TYPES = (CITY,)
	TYPES = (BUILDING, COUNT)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_BUILD_IN_CITY"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_CITY_BUILDING_COUNT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_CITY_BUILDING_COUNT"
	
	IN_DESC_KEY = "TXT_KEY_VICTORY_DESC_HAVE_IN_CITY"
	
	def __init__(self, city, iBuilding, iRequired, **options):
		ThresholdRequirement.__init__(self, city, iBuilding, iRequired, **options)
		
		self.city = city
		self.iBuilding = iBuilding
		
		self.handle("cityAcquired", self.check_city_acquired)
		self.handle("buildingBuilt", self.check_building_built)
		self.expire("buildingBuilt", self.expire_building_built)
	
	def check_city_acquired(self, goal, city, bConquest):
		if self.city == city:
			goal.check()
	
	def check_building_built(self, goal, city, iBuilding):
		if self.city == city and self.iBuilding == base_building(iBuilding):
			goal.check()
	
	def expire_building_built(self, goal, city, iBuilding):
		if not isinstance(self.iBuilding, Aggregate) and self.iBuilding == iBuilding and isWonder(iBuilding):
			goal.announce_failure_cause(city.getOwner(), "TXT_KEY_VICTORY_ANNOUNCE_FIRST_BUILDING", BUILDING.format(iBuilding))
			goal.expire()
	
	def value(self, iPlayer, city, iBuilding):
		if city and city.getOwner() == iPlayer and city.isHasBuilding(unique_building(city.getOwner(), iBuilding)):
			return 1
		
		return 0
	
	def description(self):
		if not isinstance(self.iBuilding, Aggregate) and isWonder(self.iBuilding):
			return BUILDING.format(self.iBuilding)
		
		return Requirement.description(self)
	
	def progress(self, evaluator, **options):
		city = self.city.get(evaluator.iPlayer)
		
		if not city or city.isNone():
			return "%s %s" % (indicator(False), text("TXT_KEY_VICTORY_NO_CITY"))
		
		progress_key = city.getOwner() in evaluator and "TXT_KEY_VICTORY_PROGRESS_IN_CITY" or "TXT_KEY_VICTORY_PROGRESS_IN_CITY_DIFFERENT_OWNER"
		
		if self.iRequired > 1:
			return "%s %s: %d / %d" % (self.indicator(evaluator), text(progress_key, self.progress_text(**options), city.getName(), name(city.getOwner())), self.evaluate(evaluator), self.iRequired)
		
		return "%s %s" % (self.indicator(evaluator), text(progress_key, self.progress_text(**options), city.getName(), name(city.getOwner())))


class CityBuilding(CityBuildingCount):

	GLOBAL_TYPES = (CITY,)
	TYPES = (BUILDING,)
	
	DESC_KEY = "TXT_KEY_VICTORY_DESC_CITY_BUILDING"
	
	def __init__(self, city, iBuilding, **options):
		CityBuildingCount.__init__(self, city, iBuilding, 1, **options)


# Second Roman UHV goal
# Third Byzantine UHV goal
# First Moorish UHV goal
# First English UHV goal
# Third Portuguese UHV goal
class CityCount(ThresholdRequirement):

	TYPES = (AREA, COUNT)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CONTROL"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_CITY_COUNT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_CITY_COUNT"
	
	def __init__(self, *parameters, **options):
		ThresholdRequirement.__init__(self, *parameters, **options)
		
		self.bPlural = True
		
		self.handle("cityBuilt", self.check)
		self.handle("cityAcquiredAndKept", self.check)
	
	def description(self):
		if self.iRequired == 1:
			return text("TXT_KEY_VICTORY_DESC_CITY_COUNT_SINGLE", *self.format_parameters())
		
		return ThresholdRequirement.description(self)
		
	def value(self, iPlayer, area):
		return area.cities().owner(iPlayer).count()


# Second Spanish UHV goal
class ControlledResourceCount(ThresholdRequirement):

	TYPES = (RESOURCE, COUNT)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CONTROL"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_CONTROLLED_RESOURCE_COUNT"
	
	SUBJECT_DESC_KEYS = {
		VASSALS: "TXT_KEY_VICTORY_DESC_CONTROL_DIRECTLY_OR_THROUGH_VASSALS"
	}
	
	def value(self, iPlayer, iResource):
		return player(iPlayer).getNumAvailableBonuses(iResource) - player(iPlayer).getBonusImport(iResource) + player(iPlayer).getBonusExport(iResource)


# Second Turkic UHV goal
class CorporationCount(ThresholdRequirement):

	TYPES = (CORPORATION, COUNT)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_SPREAD"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_CORPORATION_COUNT"
	
	def __init__(self, iCorporation, *args, **options):
		ThresholdRequirement.__init__(self, iCorporation, *args, **options)
		
		self.iCorporation = iCorporation
		
		self.handle("corporationSpread", self.check_corporation_spread)
	
	def check_corporation_spread(self, goal, iCorporation):
		if self.iCorporation == iCorporation:
			goal.check()
	
	def value(self, iPlayer, iCorporation):
		return player(iPlayer).countCorporations(iCorporation)


# Third Iranian UHV goal
class CultureCity(ThresholdRequirement):

	TYPES = (AMOUNT,)
	
	DESC_KEY = "TXT_KEY_VICTORY_DESC_CULTURE_CITY"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_CULTURE_CITY"
	
	def __init__(self, iRequired, **options):
		ThresholdRequirement.__init__(self, iRequired, **options)
		
	def value(self, iPlayer):
		city = self.best_city(iPlayer)
		if not city:
			return 0
		return self.value_func(city)
	
	def value_func(self, city):
		return city.getCulture(city.getOwner())
	
	def best_city(self, iPlayer):
		return cities.owner(iPlayer).maximum(self.value_func)
		
	def progress(self, evaluator):
		best_city = self.best_city(evaluator.iPlayer)
		
		if not best_city:
			return "%s %s" % (indicator(False), text("TXT_KEY_VICTORY_PROGRESS_NO_CITIES"))
		
		return "%s %s: %d / %d" % (self.indicator(evaluator), text(self.PROGR_KEY, best_city.getName()), self.value_func(best_city), scale(self.iRequired))


# Second Italian UHV goal
class CultureLevelCityCount(ThresholdRequirement):

	TYPES = (CULTURELEVEL, COUNT)
	
	DESC_KEY = "TXT_KEY_VICTORY_DESC_CULTURE_LEVEL_CITY_COUNT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_CULTURE_LEVEL_CITY_COUNT"
	
	def __init__(self, iCultureLevel, iRequired, **options):
		ThresholdRequirement.__init__(self, iCultureLevel, iRequired, **options)
		
		self.iCultureLevel = iCultureLevel
	
	def value(self, iPlayer, iCultureLevel):
		return cities.owner(iPlayer).where(self.valid_city).count()
	
	def value_func(self, city):
		return city.getCultureLevel()
	
	def valid_city(self, city):
		return self.value_func(city) >= self.iCultureLevel
		
	def progress_entries(self, iPlayer):
		best_cities = cities.owner(iPlayer).highest(self.iRequired, self.value_func)
		
		if not best_cities:
			yield "%s %s" % (indicator(False), text("TXT_KEY_VICTORY_PROGRESS_NO_CITIES"))
			return
		
		for index, city in enumerate(best_cities.take(self.iRequired)):
			if city:
				yield "%s %s: %d / %d" % (indicator(self.valid_city(city)), text(self.PROGR_KEY, city.getName()), city.getCulture(city.getOwner()), game.getCultureThreshold(self.iCultureLevel))
			else:
				yield "%s %s" % (indicator(False), text("TXT_KEY_VICTORY_PROGRESS_MISSING_CITY", ordinal_word(index+1)))
	
	def progress(self, evaluator):
		return list(self.progress_entries(evaluator.iPlayer))


# Third Druidist URV goal
class FeatureCount(ThresholdRequirement):

	TYPES = (FEATURE, COUNT)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CONTROL"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_FEATURE_COUNT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_FEATURE_COUNT"
	
	def value(self, iPlayer, iFeature):
		return plots.owner(iPlayer).where(lambda plot: plot.getFeatureType() == iFeature).count()


class HappyCityPopulation(ThresholdRequirement):

	TYPES = (COUNT,)
	
	DESC_KEY = "TXT_KEY_VICTORY_DESC_HAPPY_CITY_POPULATION"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_HAPPY_CITY_POPULATION"
	
	def value(self, iPlayer):
		return cities.owner(iPlayer).where(lambda city: city.angryPopulation(0) <= 0).sum(CyCity.getPopulation)


# First Brazilian UHV goal
# Third Brazilian UHV goal
class ImprovementCount(ThresholdRequirement):

	TYPES = (IMPROVEMENT, COUNT)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CONTROL"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_IMPROVEMENT_COUNT"
	
	def __init__(self, iImprovement, *parameters, **options):
		ThresholdRequirement.__init__(self, iImprovement, *parameters, **options)
		
		self.iImprovement = iImprovement
		
		self.handle("improvementBuilt", self.check_improvement_built)
	
	def check_improvement_built(self, goal, iImprovement):
		if self.iImprovement == iImprovement:
			goal.check()
	
	def value(self, iPlayer, iImprovement):
		return player(iPlayer).getImprovementCount(iImprovement)
	
	def description(self):
		return ThresholdRequirement.description(self, bPlural=self.bPlural)
	
	def progress(self, evaluator):
		if not self.bPlural:
			return IMPROVEMENT.format(self.iImprovement)
		
		return "%s %s: %s" % (self.indicator(evaluator), text(self.PROGR_KEY, IMPROVEMENT.format(self.iImprovement, bPlural=True)), self.progress_value(evaluator))
		
		

# First Portuguese UHV goal
# First Thai UHV goal
# First Iranian UHV goal
class OpenBorderCount(ThresholdRequirement):

	TYPES = (COUNT,)
	
	DESC_KEY = "TXT_KEY_VICTORY_DESC_OPEN_BORDER_COUNT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_OPEN_BORDER_COUNT"
	
	def __init__(self, iRequired, civs=None, **options):
		ThresholdRequirement.__init__(self, iRequired, civs=civs, **options)
		
		self.civs = civs
	
	def value(self, iPlayer):
		return players.major().alive().without(iPlayer).where(lambda p: self.valid(iPlayer, p)).count()
	
	def valid(self, iPlayer, iOther):
		if self.civs and civ(iOther) not in self.civs:
			return False
		
		return team(iPlayer).isOpenBorders(player(iOther).getTeam())
	
	def additional_formats(self):
		civilizations = text("TXT_KEY_VICTORY_CIVILIZATIONS")
		civilizations = qualify_adjective(civilizations, CIVS, self.civs)
		
		return [civilizations]


# Third Bon URV goal
class PeakCount(ThresholdRequirement):

	TYPES = (COUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CONTROL"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_PEAK_COUNT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_PEAK_COUNT"
	
	def value(self, iPlayer):
		return plots.owner(iPlayer).where(CyPlot.isPeak).count()


# Third Dravidian UHV goal
class PopulationCity(ThresholdRequirement):

	TYPES = (COUNT,)
	
	DESC_KEY = "TXT_KEY_VICTORY_DESC_POPULATION_CITY"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_POPULATION_CITY"
	
	def __init__(self, iRequired, **options):
		ThresholdRequirement.__init__(self, iRequired, **options)
		
	def value(self, iPlayer):
		city = self.best_city(iPlayer)
		if not city:
			return 0
		return self.value_func(city)
	
	def value_func(self, city):
		return city.getPopulation()
	
	def best_city(self, iPlayer):
		return cities.owner(iPlayer).maximum(self.value_func)
		
	def progress(self, evaluator):
		best_city = self.best_city(evaluator.iPlayer)
		
		if not best_city:
			return "%s %s" % (indicator(False), text("TXT_KEY_VICTORY_PROGRESS_NO_CITIES"))
		
		return "%s %s: %d / %d" % (self.indicator(evaluator), text(self.PROGR_KEY, best_city.getName()), self.value_func(best_city), scale(self.iRequired))


# First Polish UHV goal
class PopulationCityCount(ThresholdRequirement):

	TYPES = (COUNT, COUNT)
	
	DESC_KEY = "TXT_KEY_VICTORY_DESC_POPULATION_CITY_COUNT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_POPULATION_CITY_COUNT"
	
	def __init__(self, iPopulation, iRequired, **options):
		ThresholdRequirement.__init__(self, iPopulation, iRequired, **options)
		
		self.iPopulation = iPopulation
	
	def value(self, iPlayer, iPopulation):
		return cities.owner(iPlayer).where(self.valid_city).count()
	
	def value_func(self, city):
		return city.getPopulation()
	
	def valid_city(self, city):
		return self.value_func(city) >= self.iPopulation
		
	def progress_entries(self, iPlayer):
		best_cities = cities.owner(iPlayer).highest(self.iRequired, self.value_func)
		
		if not best_cities:
			yield "%s %s" % (indicator(False), text("TXT_KEY_VICTORY_PROGRESS_NO_CITIES"))
			return
		
		for index, city in enumerate(best_cities.take(self.iRequired)):
			if city:
				yield "%s %s: %d / %d" % (indicator(self.valid_city(city)), text(self.PROGR_KEY, city.getName()), self.value_func(city), self.iPopulation)
			else:
				yield "%s %s" % (indicator(False), text("TXT_KEY_VICTORY_PROGRESS_MISSING_CITY", ordinal_word(index+1)))
	
	def progress(self, evaluator):
		return list(self.progress_entries(evaluator.iPlayer))


# Third Harappan UHV goal
class PopulationCount(ThresholdRequirement):

	TYPES = (COUNT,)
	
	DESC_KEY = "TXT_KEY_VICTORY_DESC_POPULATION"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_POPULATION"
	
	def value(self, iPlayer):
		return player(iPlayer).getTotalPopulation()


class ReligionPopulationCount(ThresholdRequirement):

	TYPES = (RELIGION_ADJECTIVE, COUNT)
	
	DESC_KEY = "TXT_KEY_VICTORY_DESC_RELIGION_POPULATION"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_RELIGION_POPULATION"
	
	def value(self, iPlayer, iReligion):
		return player(iPlayer).getReligionPopulation(iReligion)


# First Ethiopian UHV goal
# Second Indonesian UHV goal
# Second Portuguese UHV goal
# Third Dutch UHV goal
# First Zoroastrian URV goal
# Third Atua URV goal
# Third Mazdaist URV goal
# Third Rodnovery URV goal
# Third Tengri URV goal
# Third Yoruba URV goal
class ResourceCount(ThresholdRequirement):

	TYPES = (RESOURCE, COUNT)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_ACQUIRE_RESOURCES"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_RESOURCE_COUNT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_RESOURCE_COUNT"
	
	def value(self, iPlayer, iResource):
		return player(iPlayer).getNumAvailableBonuses(iResource)


# Second Ethiopian UHV goal
# First Jewish URV goal
# Second Catholic URV goal
# Second Protestant URV goal
# Second Secular URV goal
class SpecialistCount(ThresholdRequirement):

	TYPES = (SPECIALIST, COUNT)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_SETTLE_IN_CITIES"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_SPECIALIST_COUNT"
	
	SUBJECT_DESC_KEYS = {
		STATE_RELIGION: "TXT_KEY_VICTORY_DESC_SETTLE_IN_RELIGION_CITIES",
		SECULAR: "TXT_KEY_VICTORY_DESC_SETTLE_IN_SECULAR_CITIES",
	}
	
	def __init__(self, iSpecialist, iRequired, **options):
		ThresholdRequirement.__init__(self, iSpecialist, iRequired, **options)
		
		self.iSpecialist = iSpecialist
	
	def value(self, iPlayer, iSpecialist):
		return cities.owner(iPlayer).sum(lambda city: city.getFreeSpecialistCount(iSpecialist))
	
	def description(self):
		return Requirement.description(self, bPlural=self.bPlural)
	
	def progress(self, evaluator):
		if not self.bPlural:
			return SPECIALIST.format(self.iSpecialist)
		
		return "%s %s: %s" % (self.indicator(evaluator), text(self.PROGR_KEY, SPECIALIST.format(self.iSpecialist, bPlural=True)), self.progress_value(evaluator))


# Third Atua URV goal
class TerrainCount(ThresholdRequirement):

	TYPES = (TERRAIN, COUNT)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CONTROL"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_TERRAIN_COUNT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_TERRAIN_COUNT"
	
	def value(self, iPlayer, iTerrain):
		return plots.owner(iPlayer).where(lambda plot: plot.getTerrainType() == iTerrain).count()


class TradeRouteCount(ThresholdRequirement):

	TYPES = (COUNT,)
	
	DESC_KEY = "TXT_KEY_VICTORY_DESC_TRADE_ROUTE_COUNT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_TRADE_ROUTE_COUNT"
	
	def count_trade_routes(self, city):
		return count(city.getTradeCity(i) and not city.getTradeCity(i).isNone() for i in range(city.getTradeRoutes()))
	
	def value(self, iPlayer):
		return cities.owner(iPlayer).sum(self.count_trade_routes)


# Third Confucian URV goal
class UnitCombatCount(ThresholdRequirement):

	TYPES = (UNITCOMBAT, COUNT)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CONTROL"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_UNIT_COMBAT_COUNT"
	
	def __init__(self, iUnitCombat, iRequired, **options):
		ThresholdRequirement.__init__(self, as_int(iUnitCombat), iRequired, **options)
	
	def value(self, iPlayer, iUnitCombat):
		if not capital(iPlayer):
			return 0
		
		return units.owner(iPlayer).combat(iUnitCombat).where(lambda unit: capital(iPlayer).allUpgradesAvailable(unit.getUnitType(), 0) < 0).count()


class UnitCombatLevelCount(ThresholdRequirement):

	TYPES = (UNITCOMBAT, COUNT, COUNT)
	
	DESC_KEY = "TXT_KEY_VICTORY_DESC_UNIT_COMBAT_LEVEL_COUNT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_UNIT_COMBAT_LEVEL_COUNT"
	
	def __init__(self, iUnitCombat, iLevel, iRequired, **options):
		ThresholdRequirement.__init__(self, as_int(iUnitCombat), iLevel, iRequired, **options)
	
	def value(self, iPlayer, iUnitCombat, iLevel):
		if not capital(iPlayer):
			return 0
	
		return units.owner(iPlayer).combat(iUnitCombat).where(lambda unit: capital(iPlayer).allUpgradesAvailable(unit.getUnitType(), 0) < 0).where(lambda unit: unit.getLevel() >= iLevel).count()
	

# Second English UHV goal
class UnitCount(ThresholdRequirement):

	TYPES = (UNIT, COUNT)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CONTROL"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_UNIT_COUNT"
	
	def __init__(self, iUnit, iRequired, **options):
		ThresholdRequirement.__init__(self, iUnit, iRequired, **options)
		
		self.iUnit = iUnit
	
	def value(self, iPlayer, iUnit):
		return player(iPlayer).getUnitClassCount(infos.unit(iUnit).getUnitClassType())
	
	def description(self, **options):
		return Requirement.description(self, bPlural=self.bPlural, **options)

	def progress_text(self, **options):
		return Requirement.progress_text(self, bPlural=self.bPlural, **options)


# Third Asatru URV goal
class UnitLevelCount(ThresholdRequirement):

	TYPES = (COUNT, COUNT)
	
	DESC_KEY = "TXT_KEY_VICTORY_DESC_UNIT_LEVEL_COUNT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_UNIT_LEVEL_COUNT"
	
	def value(self, iPlayer, iLevel):
		return units.owner(iPlayer).where(lambda unit: unit.getLevel() >= iLevel).count()


# Second Holy Roman UHV goal
class VassalCount(ThresholdRequirement):

	TYPES = (COUNT,)
	
	DESC_KEY = "TXT_KEY_VICTORY_DESC_VASSAL_COUNT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_VASSAL_COUNT"
	
	def __init__(self, iRequired, civs=None, iStateReligion=None, **options):
		ThresholdRequirement.__init__(self, iRequired, civs=civs, iStateReligion=iStateReligion, **options)
		
		self.civs = civs
		self.iStateReligion = iStateReligion
		
		self.handle_any("playerChangeStateReligion", self.check_state_religion)
		self.handle_any("vassalState", self.check_vassal)
		
	def check_state_religion(self, goal, iNewReligion):
		if self.iStateReligion == iNewReligion:
			goal.check()
	
	def check_vassal(self, goal):
		goal.check()
		
	def valid_vassal(self, iPlayer, iVassal):
		if self.civs and civ(iVassal) not in self.civs:
			return False
		
		if self.iStateReligion is not None and player(iVassal).getStateReligion() != self.iStateReligion:
			return False
	
		return team(iVassal).isVassal(player(iPlayer).getTeam())
		
	def value(self, iPlayer):
		return players.major().alive().where(lambda p: self.valid_vassal(iPlayer, p)).count()
		
	def additional_formats(self):
		vassal = text("TXT_KEY_VICTORY_VASSALS")
		vassal = in_area(vassal, self.civs)
		vassal = religion_adjective(vassal, self.iStateReligion)
		
		return [vassal]
