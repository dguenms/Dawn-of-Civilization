from Core import *
from VictoryTypes import *
from BaseRequirements import *

from Civics import isCommunist


# Third Holy Roman UHV goal
# Third Russian UHV goal
# Third Jewish URV goal
# First Confucian URV goal
class AttitudeCount(ThresholdRequirement):

	TYPES = (ATTITUDE, COUNT)
	
	DESC_KEY = "TXT_KEY_VICTORY_DESC_ATTITUDE_COUNT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_ATTITUDE_COUNT"
	
	def __init__(self, iAttitude, iRequired, civs=None, iReligion=None, bIndependent=False, bCommunist=False, **options):
		ThresholdRequirement.__init__(self, int(iAttitude), iRequired, **options)
		
		self.civs = civs
		self.iReligion = iReligion
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
		
		return player(iOtherPlayer).AI_getAttitude(iPlayer) >= iAttitude
	
	def value(self, iPlayer, iAttitude):
		return players.major().alive().where(lambda p: self.valid(iPlayer, p, iAttitude)).count()
	
	def additional_formats(self):
		civilizations = text("TXT_KEY_VICTORY_CIVILIZATIONS")
		civilizations = qualify(civilizations, "TXT_KEY_VICTORY_COMMUNIST", self.bCommunist)
		civilizations = qualify(civilizations, "TXT_KEY_VICTORY_INDEPENDENT", self.bIndependent)
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
class BuildingCount(ThresholdRequirement):

	TYPES = (BUILDING, COUNT)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CONTROL"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_COUNT"
	
	def __init__(self, iBuilding, *args, **options):
		ThresholdRequirement.__init__(self, iBuilding, *args, **options)
		
		self.iBuilding = iBuilding
		
		self.handle("cityAcquired", self.check)
		self.handle("buildingBuilt", self.check_building_built)
	
	def check_building_built(self, goal, city, iBuilding):
		if base_building(iBuilding) == self.iBuilding:
			goal.check()
	
	def value(self, iPlayer, iBuilding):
		return player(iPlayer).countNumBuildings(unique_building(iPlayer, iBuilding))
	
	def description(self):
		return Requirement.description(self, bPlural=self.bPlural)
		
	def progress(self, evaluator):
		if not self.bPlural:
			return BUILDING.format(self.iBuilding)
		
		return "%s %s: %s" % (self.indicator(evaluator), text(self.PROGR_KEY, BUILDING.format(self.iBuilding, bPlural=True)), self.progress_value(evaluator))


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
		
		self.handle("cityBuilt", self.check)
		self.handle("cityAcquiredAndKept", self.check)
		
	def value(self, iPlayer, area):
		return area.cities().owner(iPlayer).count()


# Second Spanish UHV goal
class ControlledResourceCount(ThresholdRequirement):

	TYPES = (RESOURCE, COUNT)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CONTROL"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_CONTROLLED_RESOURCE_COUNT"
	
	def value(self, iPlayer, iResource):
		return player(iPlayer).getNumAvailableBonuses(iResource) - player(iPlayer).getBonusImport(iResource)


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

	TYPES = (COUNT,)
	
	DESC_KEY = "TXT_KEY_VICTORY_DESC_CULTURE_CITY"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_CULTURE_CITY"
	
	def __init__(self, iRequired, **options):
		ThresholdRequirement.__init__(self, scale(iRequired), **options)
		
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
		
		return "%s %s: %d / %d" % (self.indicator(evaluator), text(self.PROGR_KEY, best_city.getName()), self.value_func(best_city), self.iRequired)


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


# First Brazilian UHV goal
# Third Brazilian UHV goal
class ImprovementCount(ThresholdRequirement):

	TYPES = (IMPROVEMENT, COUNT)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CONTROL"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_IMPROVEMENT_COUNT"
	
	def __init__(self, iImprovement, *parameters, **options):
		ThresholdRequirement.__init__(self, iImprovement, *parameters, **options)
		
		self.iImprovement = iImprovement
	
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
		ThresholdRequirement.__init__(self, iRequired, **options)
		
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


# First Ethiopian UHV goal
# Second Indonesian UHV goal
# Second Portuguese UHV goal
# Third Dutch UHV goal
# First Zoroastrian URV goal
class ResourceCount(ThresholdRequirement):

	TYPES = (RESOURCE, COUNT)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_ACQUIRE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_RESOURCE_COUNT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_RESOURCE_COUNT"
	
	def value(self, iPlayer, iResource):
		return player(iPlayer).getNumAvailableBonuses(iResource)


# Second Ethiopian UHV goal
# First Jewish URV goal
# Second Catholic URV goal
# Second Protestant URV goal
class SpecialistCount(ThresholdRequirement):

	TYPES = (SPECIALIST, COUNT)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_SETTLE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_SPECIALIST_COUNT"
	
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


# Third Confucian URV goal
class UnitCombatCount(ThresholdRequirement):

	TYPES = (UNITCOMBAT, COUNT)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CONTROL"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_UNIT_COMBAT_COUNT"
	
	def __init__(self, iUnitCombat, iRequired, **options):
		ThresholdRequirement.__init__(self, int(iUnitCombat), iRequired, **options)
	
	def value(self, iPlayer, iUnitCombat):
		if not capital(iPlayer):
			return 0
		
		return units.owner(iPlayer).combat(iUnitCombat).where(lambda unit: capital(iPlayer).allUpgradesAvailable(unit.getUnitType(), 0) < 0).count()
	

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


# Second Holy Roman UHV goal
class VassalCount(ThresholdRequirement):

	TYPES = (COUNT,)
	
	DESC_KEY = "TXT_KEY_VICTORY_DESC_VASSAL_COUNT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_VASSAL_COUNT"
	
	def __init__(self, iRequired, civs=None, iStateReligion=None, **options):
		ThresholdRequirement.__init__(self, iRequired, **options)
		
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
