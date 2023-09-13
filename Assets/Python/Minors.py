# coding: utf-8

from Core import *
from RFCUtils import *
from Events import handler


def periodic(iTurns, seed):
	return (turn() + hash(seed)) % turns(iTurns) == 0


def best_civ_of_group(iGroup):
	return civs.of(*dTechGroups[iGroup]).alive().maximum(lambda c: player(c).getScoreHistory(turn()))


def best_civ_of_same_tech_group(iCiv):
	iTechGroup = next(iGroup for iGroup in dTechGroups if iCiv in dTechGroups[iGroup])
	return best_civ_of_group(iTechGroup)


def add_city_buildings(tile, iCiv):
	city(tile).rebuild(player(iCiv).getCurrentEra())
	return
		
	for iDefensiveBuilding in infos.buildings().where(isDefensiveBuilding):
		if player(iCiv).canConstruct(iDefensiveBuilding, False, False, False):
			city(tile).setHasRealBuilding(iDefensiveBuilding, True)


class MinorCity(object):

	def __init__(self, iYear, iOwner, tile, name, iPopulation=1, iTechGroup=None, iCulture=0, units={}, adjective=None, condition=lambda: True):
		self.iYear = iYear
		self.iOwner = iOwner
		self.tile = tile
		self.name = name
		self.iPopulation = iPopulation
		self.iTechGroup = iTechGroup
		self.iCulture = iCulture
		self.units = units
		self.adjective = adjective
		self.condition = condition
	
	def check(self):
		if self.canFound():
			self.found()
		
		return
		
		city = city_(self.tile)
		if not city:
			return
		
		if not is_minor(city.getOwner()):
			return
		
		if self.every(10):
			self.add_unit()
		
		if self.every(25):
			self.add_buildings()
	
	def canFound(self):
		if plot(self.tile).getImprovementType() == iCityRuins:
			return False
	
		if year() < year(self.iYear):
			return False
		
		if year() >= year(self.iYear) + turns(10):
			return False
		
		if not self.condition():
			return False
		
		if not isFree(self.iOwner, self.tile, bNoCity=True, bNoCulture=True):
			return False
		
		return True
		
	def get_tech_civ(self):
		if self.iTechGroup is not None:
			iTechCiv = best_civ_of_group(self.iTechGroup)
			if iTechCiv >= 0:
				return iTechCiv
		
		return self.iOwner
	
	def found(self):
		x, y = location(self.tile)
		
		expelUnits(self.iOwner, plots.surrounding(x, y))
		
		player(self.iOwner).found(x, y)
		founded = city(x, y)
		
		if founded:
			iTechEra = player(self.get_tech_civ()).getCurrentEra()
			
			founded.setName(self.name, False)
			founded.setPopulation(self.iPopulation)
			founded.setCulture(founded.getOwner(), scale(self.iCulture) + iTechEra * scale(100), True)
			
			self.add_buildings()
			self.create_units()
			
	def every(self, iTurns):
		return periodic(iTurns, self)
	
	def get_units(self):
		iUnitCiv = self.get_tech_civ()
		
		for iRole, iNumUnits in self.units.items():
			for iUnit, iUnitAI in getUnitsForRole(iUnitCiv, iRole):
				try:
					yield base_unit(iUnit), iNumUnits, iUnitAI
				except TypeError, e:
					raise Exception("Error creating unit for iRole=%s, name=%s: %s" % (iRole, self.name, e))
	
	def make_units(self, iUnit, iUnitAI, iNumUnits=1):
		units = makeUnits(self.iOwner, iUnit, self.tile, iNumUnits, iUnitAI)
		
		if self.adjective:
			units.adjective(self.adjective)
	
	def create_units(self):
		for iUnit, iNumUnits, iUnitAI in self.get_units():
			self.make_units(iUnit, iUnitAI, iNumUnits)
	
	def add_unit(self):
		iTechCiv = self.get_tech_civ()
	
		for iUnit, iNumUnits, iUnitAI in self.get_units():
			if units.at(self.tile).type(iUnit).count() < iNumUnits + max(0, player(iTechCiv).getCurrentEra() - 1):
				self.make_units(iUnit, iUnitAI)
	
	def add_buildings(self):
		iTechCiv = self.get_tech_civ()
		add_city_buildings(self.tile, iTechCiv)


NUM_BARBARIAN_TYPES = 7
(ANIMALS, NOMADS, MINORS, INVADERS, NATIVES, SEA_INVADERS, PIRATES) = range(NUM_BARBARIAN_TYPES)


class Barbarians(object):

	SPAWN_LIMITS = {
		ANIMALS: 3,
		NOMADS: 3,
		MINORS: 5,
		NATIVES: 3,
		PIRATES: 3,
	}
	
	SPAWN_NOTIFICATIONS = {
		ANIMALS: "TXT_KEY_BARBARIAN_NOTIFICATION_ANIMALS",
		NOMADS: "TXT_KEY_BARBARIAN_NOTIFICATION_NOMADS",
		MINORS: "TXT_KEY_BARBARIAN_NOTIFICATION_MINORS",
		INVADERS: "TXT_KEY_BARBARIAN_NOTIFICATION_INVADERS",
		NATIVES: "TXT_KEY_BARBARIAN_NOTIFICATION_NATIVES",
		SEA_INVADERS: "TXT_KEY_BARBARIAN_NOTIFICATION_SEA_INVADERS",
		PIRATES: "TXT_KEY_BARBARIAN_NOTIFICATION_PIRATES"
	}

	def __init__(self, iStart, iEnd, units, area, iInterval, pattern, iOwner=iBarbarian, target_area=None, adjective=None):
		self.iStart = iStart
		self.iEnd = iEnd
		self.units = units
		self.area = area
		self.iInterval = iInterval
		self.pattern = pattern
		self.iOwner = iOwner
		self.target_area = target_area
		self.adjective = adjective
		
		if self.target_area is None:
			self.target_area = area
	
	def __repr__(self):
		return "%s barbarians: %s" % (text(self.adjective), format_separators(self.units.keys(), ", ", text("TXT_KEY_AND"), format=lambda iUnit: infos.unit(iUnit).getText()))
	
	def spawn_data(self):
		data = {
			"iStart": self.iStart,
			"iEnd": self.iEnd,
			"units": self.units,
			"iInterval": self.iInterval,
		}
		return data
	
	def check(self):
		if self.can_notify():
			self.notify()
	
		if self.can_spawn():
			self.spawn()
	
	def can_notify(self):
		if self.iStart == turn():
			affected_area = plots.rectangle(self.area) + plots.rectangle(self.area)
			if affected_area.expand(3).owner(active()):
				return True
		
		return False
	
	def notify(self):
		adjective_text = text_if_exists(self.adjective, otherwise="TXT_KEY_ADJECTIVE_BARBARIAN")
		unit = infos.unit(self.units.items()[0][0])
		location = plots.rectangle(self.area).closest(capital(active()))
		
		message(active(), self.SPAWN_NOTIFICATIONS[self.pattern], adjective_text, iColor=iRed, button=unit.getButton(), location=location)
	
	def can_spawn(self):
		if not (year(self.iStart) <= year() <= year(self.iEnd)):
			return False
		
		if not self.every():
			return False
	
		if self.pattern in [NOMADS, INVADERS, SEA_INVADERS]:
			if not self.valid_targets():
				return False
		
		if self.spawn_limit():
			return False
		
		if self.pattern == MINORS:
			if plots.rectangle(self.area).land().all(lambda p: p.isOwned() and not owner(p, self.get_owner())):
				return False
	
		return True
	
	def every(self):
		return periodic(self.iInterval, self)
	
	def spawn(self):
		for iUnit, plot in zip(self.get_spawn_units(), self.get_spawn_plots()):
			unit = makeUnit(self.get_owner(), iUnit, plot, self.get_unit_ai(iUnit, plot))
			
			data.units[unit].spawn_data = self.spawn_data()
			
			if self.adjective:
				set_unit_adjective(unit, self.adjective)
	
	def get_owner(self):
		if self.pattern == MINORS:
			minor_city = cities.rectangle(self.area).where(lambda city: is_minor(city.getOwner())).first()
			if minor_city:
				return civ(minor_city.getOwner())
		
		return self.iOwner
	
	def valid_targets(self):
		return cities.rectangle(self.target_area).any(lambda city: not is_minor(city.getOwner()))
	
	def count_existing(self, iUnit):
		return units.owner(self.iOwner).type(iUnit).where(lambda unit: data.units[unit].spawn_data == self.spawn_data()).count()
	
	def spawn_limit(self):
		iLimit = self.SPAWN_LIMITS.get(self.pattern)
		
		if iLimit is None:
			return False
			
		for iUnit, iNumUnits in self.units.items():
			if self.count_existing(iUnit) >= iLimit * iNumUnits:
				return True
		
		return False
		
	def get_spawn_units(self):
		return sum(([iUnit] * iNumUnits for iUnit, iNumUnits in self.units.items()), [])
	
	def get_spawn_plots(self):
		spawn_area = plots.rectangle(self.area).passable().where(self.valid_spawn)
		iNumUnits = sum(self.units.values())
		
		if not spawn_area:
			return []
		
		if self.pattern == MINORS:
			minor_city = spawn_area.cities().owner(self.get_owner()).random()
			if minor_city:
				return [minor_city] * iNumUnits
			
			return [spawn_area.random()] * iNumUnits
		
		elif self.pattern in [INVADERS, SEA_INVADERS]:
			return [spawn_area.random()] * iNumUnits
		
		else:
			return spawn_area.sample(iNumUnits)
	
	def get_unit_ai(self, iUnit, plot):
		if plot.isCity():
			return UnitAITypes.UNITAI_CITY_DEFENSE
	
		if self.pattern == PIRATES:
			return UnitAITypes.UNITAI_PIRATE_SEA
		
		elif self.pattern == NATIVES:
			return UnitAITypes.UNITAI_PILLAGE
		
		elif self.pattern == ANIMALS:
			return UnitAITypes.UNITAI_ANIMAL
		
		elif self.pattern == SEA_INVADERS:
			if infos.unit(iUnit).getDomainType() == DomainTypes.DOMAIN_SEA:
				return UnitAITypes.UNITAI_ASSAULT_SEA
		
		return UnitAITypes.UNITAI_ATTACK		
	
	def valid_spawn(self, plot):
		if self.pattern in [SEA_INVADERS, PIRATES]:
			if not plot.isWater():
				return False
				
		else:
			if plot.isWater():
				return False
		
			if map.getArea(plot.getArea()).getNumCities() == 0:
				return False
		
		if units.at(plot).notowner(self.get_owner()):
			return False
		
		if cities.surrounding(plot):
			return False
		
		if self.pattern in [ANIMALS, NOMADS, MINORS, PIRATES]:
			if plot.isOwned():
				return False
		
		if self.pattern == ANIMALS:
			if cities.surrounding(plot, radius=3):
				return False
		
		if self.pattern == INVADERS:
			if not plots.surrounding(plot).notowner(plot.getOwner()):
				return False
		
		return True


minor_cities = [
	MinorCity(-3000, iIndependent2, (92, 46), "Shushan", iPopulation=1, iTechGroup=iTechGroupMiddleEast, units={iDefend: 1}, iCulture=10, adjective="TXT_KEY_ADJECTIVE_ELAMITE"),
	MinorCity(-3000, iIndependent, (90, 45), "Unug", iPopulation=1, iTechGroup=iTechGroupMiddleEast, units={iDefend: 2}, iCulture=10, adjective="TXT_KEY_ADJECTIVE_SUMERIAN"),
	MinorCity(-2200, iIndependent2, (86, 50), "Halab", iPopulation=1, iTechGroup=iTechGroupMiddleEast, units={iDefend: 1}, adjective="TXT_KEY_ADJECTIVE_MARIOTE"),
	MinorCity(-2000, iIndependent, (118, 49), "Sanxingdui", iPopulation=2, iTechGroup=iTechGroupFarEast, units={iDefend: 2}, adjective="TXT_KEY_ADJECTIVE_SHU"),
	MinorCity(-1600, iIndependent, (84, 45), "Yerushalayim", iPopulation=2, iTechGroup=iTechGroupMiddleEast, units={iDefend: 3}, adjective="TXT_KEY_ADJECTIVE_ISRAELITE"),
	MinorCity(-900, iIndependent2, (89, 53), "Tushpa", iPopulation=1, iTechGroup=iTechGroupMiddleEast, units={iDefend: 2}, adjective="TXT_KEY_ADJECTIVE_ARMENIAN"),
	MinorCity(-800, iIndependent, (100, 54), u"Smárkath", iPopulation=1, iTechGroup=iTechGroupMiddleEast, units={iDefend: 1}, adjective="TXT_KEY_ADJECTIVE_SOGDIAN"),
	MinorCity(-680, iIndependent, (92, 50), "Hagmatana", iPopulation=2, iTechGroup=iTechGroupMiddleEast, units={iDefend: 2, iShock: 2}, adjective="TXT_KEY_ADJECTIVE_MEDIAN"),
	MinorCity(-600, iIndependent, (97, 53), "Margu", iPopulation=1, iTechGroup=iTechGroupMiddleEast, units={iDefend: 1}, adjective="TXT_KEY_ADJECTIVE_SOGDIAN"),
	MinorCity(-500, iNative, (19, 41), "Danibaan", iPopulation=2, iTechGroup=iTechGroupNativeAmerica, units={iSkirmish: 1}, adjective="TXT_KEY_ADJECTIVE_ZAPOTEC"),
	MinorCity(-200, iIndependent, (125, 43), "Panyu", iPopulation=2, iTechGroup=iTechGroupFarEast, units={iDefend: 2}, adjective="TXT_KEY_ADJECTIVE_NANYUE"),
	MinorCity(-75, iIndependent, (105, 55), "Kash", iPopulation=2, iTechGroup=iTechGroupMiddleEast, units={iDefend: 1}, adjective="TXT_KEY_ADJECTIVE_UIGHUR"),
	MinorCity(300, iIndependent2, (89, 37), "Sana'a", iPopulation=2, iTechGroup=iTechGroupMiddleEast, units={iDefend: 2}, adjective="TXT_KEY_ADJECTIVE_YEMENI"),
	MinorCity(400, iIndependent2, (118, 45), "Dali", iPopulation=4, iTechGroup=iTechGroupFarEast, units={iDefend: 3, iShock: 1}, adjective="TXT_KEY_ADJECTIVE_BAI"),
	MinorCity(400, iIndependent, (123, 39), "Indrapura", iPopulation=3, iTechGroup=iTechGroupFarEast, units={iDefend: 4}, adjective="TXT_KEY_ADJECTIVE_CHAM"),
	MinorCity(400, iIndependent2, (123, 25), "Sunda Kelapa", iPopulation=3, iTechGroup=iTechGroupFarEast, units={iDefend: 2}, adjective="TXT_KEY_ADJECTIVE_SUNDANESE"),
	MinorCity(700, iNative, (34, 22), "Tiwanaku", iPopulation=1, iTechGroup=iTechGroupNativeAmerica, adjective="TXT_KEY_ADJECTIVE_AYMARA"),
	MinorCity(700, iIndependent2, (71, 36), "Njimi", iPopulation=1, iTechGroup=iTechGroupMiddleEast, units={iHarass: 1}, adjective="TXT_KEY_ADJECTIVE_KANURI"),
	MinorCity(750, iIndependent, (91, 60), "Atil", iPopulation=2, iTechGroup=iTechGroupMiddleEast, units={iHarass: 3}, adjective="TXT_KEY_ADJECTIVE_KHAZAR"),
	MinorCity(800, iNative, (30, 34), u"Bacatá", iPopulation=1, iTechGroup=iTechGroupNativeAmerica, units={iDefend: 1}, adjective="TXT_KEY_ADJECTIVE_MUISCA"),
	MinorCity(840, iIndependent, (54, 65), u"Áth Cliath", iPopulation=1, iTechGroup=iTechGroupWestern, units={iDefend: 2}, adjective="TXT_KEY_ADJECTIVE_IRISH"),
	MinorCity(840, iIndependent, (57, 69), u"Sgàin", iPopulation=2, iTechGroup=iTechGroupWestern, units={iDefend: 2, iCounter: 1}, adjective="TXT_KEY_ADJECTIVE_SCOTTISH"),
	MinorCity(880, iIndependent2, (74, 59), "Buda", iPopulation=3, iTechGroup=iTechGroupWestern, units={iHarass: 5}, adjective="TXT_KEY_ADJECTIVE_MAGYAR"),
	MinorCity(900, iNative, (27, 28), u"Túcume", iPopulation=1, iTechGroup=iTechGroupNativeAmerica, units={iDefend: 2}, adjective="TXT_KEY_ADJECTIVE_CHIMU"),
	MinorCity(900, iNative, (28, 25), "Chan Chan", iPopulation=2, iTechGroup=iTechGroupNativeAmerica, units={iDefend: 2}, adjective="TXT_KEY_ADJECTIVE_CHIMU"),
	MinorCity(900, iIndependent, (85, 28), "Muqdisho", iPopulation=3, iTechGroup=iTechGroupMiddleEast, units={iDefend: 2}, adjective="TXT_KEY_ADJECTIVE_SOMALI"),
	MinorCity(900, iNative, (79, 18), "Zimbabwe", iPopulation=2, units={iDefend: 1}, adjective="TXT_KEY_ADJECTIVE_SHONA"),
	MinorCity(1000, iBarbarian, (92, 66), "Qazan", iPopulation=2, iTechGroup=iTechGroupMiddleEast, units={iHarass: 3}, adjective="TXT_KEY_ADJECTIVE_BULGAR"),
	MinorCity(1000, iNative, (67, 34), "Kano", iPopulation=2, iTechGroup=iTechGroupMiddleEast, units={iDefend: 2}, adjective="TXT_KEY_ADJECTIVE_HAUSA"),
	MinorCity(1100, iIndependent, (144, 33), "Nan Madol", iPopulation=1),
	MinorCity(1180, iNative, (66, 31), "Edo", iPopulation=3, iTechGroup=iTechGroupMiddleEast, units={iDefend: 2}, adjective="TXT_KEY_ADJECTIVE_EDO"),
	MinorCity(1300, iNative, (15, 44), "Ts'intsuntsani", iPopulation=3, iTechGroup=iTechGroupNativeAmerica, units={iDefend: 3, iAttack:2}, adjective="TXT_KEY_ADJECTIVE_PUREPECHA"),
	MinorCity(1350, iIndependent2, (81, 32), "Bonga", iPopulation=3, iTechGroup=iTechGroupMiddleEast, units={iDefend: 3}),
	MinorCity(1585, iNative, (74, 23), "Mwimbele", iPopulation=1, units={iSkirmish: 2}, adjective="TXT_KEY_ADJECTIVE_LUBA"),
	MinorCity(1610, iNative, (89, 18), "Antananarivo", iPopulation=1, units={iDefend: 2}, adjective="TXT_KEY_ADJECTIVE_MALAGASY"),
]

barbarians = [
	Barbarians(-3000, -850, {iBear: 1}, ((65, 62), (132, 73)), 5, ANIMALS),
	Barbarians(-3000, -850, {iWolf: 1}, ((65, 62), (132, 73)), 5, ANIMALS),
	Barbarians(-3000, -850, {iPanther: 1}, ((54, 11), (84, 41)), 8, ANIMALS),
	Barbarians(-3000, -850, {iLion: 1}, ((54, 11), (84, 41)), 8, ANIMALS),
	Barbarians(-3000, -850, {iPanther: 1}, ((101, 33), (113, 45)), 10, ANIMALS),
	Barbarians(-3000, -850, {iLion: 1}, ((101, 33), (113, 45)), 10, ANIMALS),
	Barbarians(-3000, -1500, {iWarrior: 2}, ((79, 56), (103, 62)), 8, NOMADS, target_area=((83, 44), (104, 51)), adjective="TXT_KEY_ADJECTIVE_INDO_EUROPEAN"),
	Barbarians(-2000, -1200, {iWarrior: 2}, ((120, 42), (129, 50)), 8, MINORS, adjective="TXT_KEY_ADJECTIVE_YUE"),
	Barbarians(-1800, -1200, {iWarrior: 2}, ((87, 44), (91, 52)), 10, INVADERS, adjective="TXT_KEY_ADJECTIVE_KASSITE"),
	Barbarians(-1800, -1500, {iAxeman: 1}, ((79, 42), (84, 46)), 8, INVADERS, target_area=((77, 39), (82, 45)), adjective="TXT_KEY_ADJECTIVE_HYKSOS"),
	Barbarians(-1600, -1200, {iChariot: 1}, ((85, 50), (90, 54)), 8, MINORS, adjective="TXT_KEY_ADJECTIVE_HURRIAN"),
	Barbarians(-1600, -800, {iChariot: 1, iLightSwordsman: 1}, ((98, 42), (109, 51)), 10, INVADERS, target_area=((99, 41), (113, 46)), adjective="TXT_KEY_ADJECTIVE_VEDIC"),
	Barbarians(-1500, -850, {iChariot: 2}, ((79, 56), (103, 62)), 8, NOMADS, target_area=((83, 44), (104, 51)), adjective="TXT_KEY_ADJECTIVE_IRANIAN"),
	Barbarians(-1500, -300, {iLightSwordsman: 2}, ((120, 42), (129, 50)), 12, MINORS, adjective="TXT_KEY_ADJECTIVE_SHU"),
	Barbarians(-1500, -500, {iArcher: 1}, ((105, 39), (111, 43)), 10, NATIVES, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_GIRIJAN"),
	Barbarians(-1250, -1150, {iGalley: 1, iAxeman: 2}, ((74, 44), (85, 54)), 1, SEA_INVADERS, target_area=((74, 39), (91, 54)), adjective="TXT_KEY_ADJECTIVE_SEA_PEOPLES"),
	Barbarians(-1200, -900, {iVulture: 2}, ((87, 44), (91, 52)), 10, INVADERS, adjective="TXT_KEY_ADJECTIVE_KASSITE"),
	Barbarians(-1200, 400, {iSkirmisher: 1, iLightSwordsman: 1}, ((120, 42), (129, 50)), 8, MINORS, adjective="TXT_KEY_ADJECTIVE_YUE"),
	Barbarians(-1200, -500, {iSkirmisher: 1}, ((84, 44), (88, 52)), 10, NOMADS, target_area=((84, 44), (91, 52)), adjective="TXT_KEY_ADJECTIVE_ARAMEAN"),
	Barbarians(-1100, -600, {iSwordsman: 1}, ((79, 51), (84, 55)), 10, MINORS, adjective="TXT_KEY_ADJECTIVE_PHRYGIAN"),
	Barbarians(-1000, -600, {iHorseman: 1}, ((85, 54), (92, 60)), 10, INVADERS, target_area=((83, 44), (91, 52)), adjective="TXT_KEY_ADJECTIVE_CIMMERIAN"),
	Barbarians(-800, -300, {iHorseman: 2}, ((78, 57), (102, 63)), 8, NOMADS, target_area=((83, 44), (104, 57)), adjective="TXT_KEY_ADJECTIVE_SCYTHIAN"),
	Barbarians(-650, -50, {iGallicWarrior: 1}, ((56, 55), (75, 61)), 6, INVADERS, target_area=((64, 49), (79, 57))),
	Barbarians(-650, -50, {iAxeman: 1}, ((69, 56), (78, 61)), 8, INVADERS, target_area=((73, 49), (84, 55)), adjective="TXT_KEY_ADJECTIVE_GALATIAN"),
	Barbarians(-650, -50, {iLightSwordsman: 1}, ((54, 50), (58, 54)), 10, INVADERS, target_area=((54, 48), (62, 54)), adjective="TXT_KEY_ADJECTIVE_CELTIBERIAN"),
	Barbarians(-500, 200, {iSkirmisher: 1}, ((105, 39), (111, 43)), 10, NATIVES, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_GIRIJAN"),
	Barbarians(-500, 0, {iAxeman: 1}, ((101, 37), (112, 45)), 8, MINORS, adjective="TXT_KEY_ADJECTIVE_HINDI"),
	Barbarians(-400, 200, {iNumidianCavalry: 1}, ((57, 43), (66, 47)), 9, NOMADS, target_area=((57, 43), (70, 48))),
	Barbarians(-350, 200, {iLightSwordsman: 1}, ((113, 47), (117, 54)), 10, MINORS, adjective="TXT_KEY_ADJECTIVE_TIBETAN"),
	Barbarians(-300, 400, {iHorseArcher: 3}, ((113, 55), (128, 62)), 7, NOMADS, target_area=((117, 46), (129, 59)), adjective="TXT_KEY_ADJECTIVE_XIONGNU"),
	Barbarians(-300, 400, {iHorseArcher: 2}, ((79, 58), (88, 63)), 8, NOMADS, target_area=((65, 50), (84, 58)), adjective="TXT_KEY_ADJECTIVE_SARMATIAN"),
	Barbarians(-300, 300, {iCamelRider: 1}, ((86, 38), (91, 45)), 10, NOMADS, target_area=((77, 39), (91, 50)), adjective="TXT_KEY_ADJECTIVE_BEDOUIN"),
	Barbarians(-250, 300, {iAxeman: 3}, ((64, 59), (75, 65)), 10, INVADERS, target_area=((58, 52), (71, 62)), adjective="TXT_KEY_ADJECTIVE_GERMANIC"),
	Barbarians(-250, 300, {iAxeman: 2}, ((64, 59), (75, 65)), 12, INVADERS, target_area=((58, 52), (71, 62)), adjective="TXT_KEY_ADJECTIVE_GERMANIC"),
	Barbarians(-200, 100, {iHolkan: 1}, ((19, 38), (25, 44)), 7, NATIVES, adjective="TXT_KEY_ADJECTIVE_MAYA"),
	Barbarians(-200, 200, {iWarGalley: 1}, ((59, 44), (84, 54)), 8, PIRATES),
	Barbarians(-200, 300, {iCamelRider: 1}, ((56, 39), (76, 44)), 9, NOMADS, target_area=((54, 34), (76, 48)), adjective="TXT_KEY_ADJECTIVE_BERBER"),
	Barbarians(-200, 350, {iHorseArcher: 3}, ((96, 42), (105, 49)), 9, INVADERS, target_area=((98, 42), (112, 49)), adjective="TXT_KEY_ADJECTIVE_INDO_SCYTHIAN"),
	Barbarians(-200, 700, {iWarElephant: 1}, ((103, 37), (118, 42)), 10, MINORS, adjective="TXT_KEY_ADJECTIVE_HINDI"),
	Barbarians(-200, 700, {iWarGalley: 1}, ((84, 22), (95, 37)), 18, PIRATES, adjective="TXT_KEY_ADJECTIVE_SOMALI"),
	Barbarians(-50, 700, {iWarGalley: 1}, ((54, 42), (69, 50)), 18, PIRATES, adjective="TXT_KEY_ADJECTIVE_BARBARY"),
	Barbarians(0, 200, {iAxeman: 2}, ((101, 37), (112, 45)), 8, MINORS, adjective="TXT_KEY_ADJECTIVE_HINDI"),
	Barbarians(100, 300, {iSwordsman: 3}, ((64, 59), (75, 65)), 8, INVADERS, target_area=((58, 52), (71, 62)), adjective="TXT_KEY_ADJECTIVE_GERMANIC"),
	Barbarians(100, 600, {iHolkan: 1}, ((19, 38), (25, 44)), 6, NATIVES, adjective="TXT_KEY_ADJECTIVE_MAYA"),
	Barbarians(200, 1100, {iSwordsman: 1}, ((113, 47), (117, 54)), 10, MINORS, adjective="TXT_KEY_ADJECTIVE_TIBETAN"),
	Barbarians(200, 500, {iSwordsman: 2}, ((101, 37), (112, 45)), 8, MINORS, adjective="TXT_KEY_ADJECTIVE_HINDI"),
	Barbarians(200, 400, {iHorseArcher: 3}, ((64, 58), (79, 65)), 6, INVADERS, target_area=((57, 51), (79, 61)), adjective="TXT_KEY_ADJECTIVE_GOTHIC"),
	Barbarians(300, 1500, {iCamelArcher: 1}, ((56, 39), (76, 44)), 9, NOMADS, target_area=((54, 34), (76, 48)), adjective="TXT_KEY_ADJECTIVE_BERBER"),
	Barbarians(300, 1500, {iCamelArcher: 1}, ((86, 38), (91, 45)), 10, NOMADS, target_area=((77, 39), (91, 50)), adjective="TXT_KEY_ADJECTIVE_BEDOUIN"),
	Barbarians(350, 600, {iHorseArcher: 3}, ((98, 43), (108, 49)), 6, INVADERS, target_area=((98, 42), (112, 49)), adjective="TXT_KEY_ADJECTIVE_HUNA"),
	Barbarians(350, 550, {iSwordsman: 3, iAxeman: 3}, ((59, 59), (65, 65)), 5, INVADERS, target_area=((59, 55), (66, 63)), adjective="TXT_KEY_ADJECTIVE_FRANKISH"),
	Barbarians(350, 550, {iSwordsman: 3, iHorseArcher: 1}, ((66, 53), (73, 58)), 5, INVADERS, target_area=((65, 51), (73, 57)), adjective="TXT_KEY_ADJECTIVE_OSTROGOTHIC"),
	Barbarians(350, 700, {iSwordsman: 3, iAxeman: 2}, ((54, 49), (62, 58)), 6, INVADERS, adjective="TXT_KEY_ADJECTIVE_VISIGOTHIC"),
	Barbarians(350, 450, {iHorseArcher: 3}, ((61, 57), (77, 62)), 3, INVADERS, target_area=((57, 51), (79, 61)), adjective="TXT_KEY_ADJECTIVE_HUNNIC"),
	Barbarians(400, 550, {iGalley: 1, iSwordsman: 2}, ((62, 46), (71, 50)), 6, SEA_INVADERS, target_area=((62, 46), (71, 55)), adjective="TXT_KEY_ADJECTIVE_VANDAL"),
	Barbarians(400, 1000, {iSkirmisher: 2, iSwordsman: 1}, ((120, 42), (129, 50)), 8, MINORS, adjective="TXT_KEY_ADJECTIVE_YUE"),
	Barbarians(400, 1200, {iSwordsman: 2}, ((118, 43), (122, 47)), 12, MINORS, adjective="TXT_KEY_ADJECTIVE_BAI"),
	Barbarians(500, 800, {iHorseArcher: 2}, ((105, 54), (123, 61)), 12, NOMADS, target_area=((117, 46), (129, 59)), adjective="TXT_KEY_ADJECTIVE_UIGHUR"),
	Barbarians(500, 900, {iHorseArcher: 3}, ((98, 55), (123, 62)), 6, NOMADS, target_area=((94, 52), (128, 61)), adjective="TXT_KEY_ADJECTIVE_TURKIC"),
	Barbarians(500, 1800, {iNativeRaider: 2, iNativeArcher: 1, iNativeWarrior: 2}, ((62, 24), (77, 33)), 16, NATIVES, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_BANTU"),
	Barbarians(500, 1900, {iNativeRaider: 2}, ((69, 19), (78, 32)), 10, NATIVES, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_BANTU"),
	Barbarians(550, 850, {iHorseArcher: 2}, ((70, 57), (80, 62)), 9, INVADERS, target_area=((65, 55), (79, 62)), adjective="TXT_KEY_ADJECTIVE_AVAR"),
	Barbarians(600, 1000, {iSwordsman: 2}, ((68, 60), (77, 65)), 10, NOMADS, target_area=((65, 51), (79, 57)), adjective="TXT_KEY_ADJECTIVE_SLAVIC"),
	Barbarians(600, 1000, {iHolkan: 1}, ((19, 38), (25, 44)), 4, NATIVES, adjective="TXT_KEY_ADJECTIVE_MAYA"),
	Barbarians(600, 1100, {iDogSoldier: 1, iJaguar: 2}, ((11, 44), (19, 51)), 20, NOMADS, iOwner=iNative, target_area=((14, 40), (23, 45)), adjective="TXT_KEY_ADJECTIVE_NAHUA"),
	Barbarians(650, 1100, {iHorseArcher: 2, iLancer: 2}, ((74, 54), (81, 60)), 9, INVADERS, target_area=((73, 49), (79, 57)), adjective="TXT_KEY_ADJECTIVE_BULGARIAN"),
	Barbarians(650, 950, {iHorseArcher: 2}, ((85, 57), (92, 63)), 9, MINORS, adjective="TXT_KEY_ADJECTIVE_KHAZAR"),
	Barbarians(700, 1600, {iHeavyGalley: 1}, ((54, 42), (69, 50)), 8, PIRATES, adjective="TXT_KEY_ADJECTIVE_BARBARY"),
	Barbarians(700, 1700, {iHeavyGalley: 1}, ((84, 22), (95, 37)), 18, PIRATES, adjective="TXT_KEY_ADJECTIVE_SOMALI"),
	Barbarians(750, 950, {iLongship: 1, iAxeman: 2}, ((53, 48), (63, 72)), 6, SEA_INVADERS, adjective="TXT_KEY_ADJECTIVE_VIKING"),
	Barbarians(850, 1000, {iHorseArcher: 3}, ((65, 57), (77, 61)), 5, INVADERS, target_area=((64, 56), (72, 65)), adjective="TXT_KEY_ADJECTIVE_MAGYAR"),
	Barbarians(850, 1100, {iHorseArcher: 3}, ((79, 58), (88, 62)), 6, NOMADS, target_area=((73, 49), (84, 66)), adjective="TXT_KEY_ADJECTIVE_PECHENEG"),
	Barbarians(900, 1100, {iKeshik: 3}, ((117, 56), (131, 63)), 6, INVADERS, target_area=((118, 49), (129, 61)), adjective="TXT_KEY_ADJECTIVE_JURCHEN"),
	Barbarians(900, 1200, {iHorseArcher: 2}, ((89, 62), (93, 68)), 9, MINORS, adjective="TXT_KEY_ADJECTIVE_BULGAR"),
	Barbarians(900, 1150, {iSkirmisher: 1}, ((25, 24), (29, 29)), 8, MINORS, adjective="TXT_KEY_ADJECTIVE_CHIMU"),
	Barbarians(950, 1100, {iLongship: 1, iHuscarl: 2}, ((53, 48), (63, 72)), 5, SEA_INVADERS, adjective="TXT_KEY_ADJECTIVE_VIKING"),
	Barbarians(1000, 1200, {iHorseArcher: 2}, ((101, 41), (105, 46)), 8, MINORS, adjective="TXT_KEY_ADJECTIVE_RAJPUT"),
	Barbarians(1000, 1300, {iAxeman: 2}, ((74, 64), (80, 69)), 10, MINORS, adjective="TXT_KEY_ADJECTIVE_BALTIC"),
	Barbarians(1050, 1400, {iAxeman: 1}, ((75, 17), (80, 23)), 10, MINORS, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_SHONA"),
	Barbarians(1100, 1350, {iHorseArcher: 2}, ((115, 38), (120, 45)), 12, INVADERS, adjective="TXT_KEY_ADJECTIVE_SHAN"),
	Barbarians(1100, 1250, {iHorseArcher: 3}, ((79, 58), (105, 63)), 9, NOMADS, target_area=((73, 49), (84, 66)), adjective="TXT_KEY_ADJECTIVE_CUMAN"),
	Barbarians(1150, 1400, {iAucac: 1}, ((25, 24), (29, 29)), 8, MINORS, adjective="TXT_KEY_ADJECTIVE_CHIMU"),
	Barbarians(1200, 1500, {iLancer: 3}, ((101, 41), (105, 46)), 8, MINORS, adjective="TXT_KEY_ADJECTIVE_RAJPUT"),
	Barbarians(1200, 1500, {iKeshik: 2}, ((85, 57), (95, 67)), 8, INVADERS, target_area=((80, 59), (95, 70)), adjective="TXT_KEY_ADJECTIVE_TATAR"),
	Barbarians(1200, 1500, {iLongbowman: 1}, ((87, 69), (96, 74)), 12, NATIVES, adjective="TXT_KEY_ADJECTIVE_KOMI"),
	Barbarians(1200, 1550, {iLongbowman: 2}, ((58, 31), (64, 35)), 12, NATIVES, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_AKAN"),
	Barbarians(1200, 1700, {iFarari: 1}, ((61, 34), (66, 38)), 16, INVADERS, iOwner=iNative, target_area=((54, 33), (66, 39)), adjective="TXT_KEY_ADJECTIVE_SONGHAI"),
	Barbarians(1250, 1450, {iHeavyGalley: 2}, ((125, 44), (134, 57)), 18, PIRATES, adjective="TXT_KEY_ADJECTIVE_WOKOU"),
	Barbarians(1300, 1550, {iJaguar: 2}, ((13, 41), (17, 46)), 12, MINORS, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_PUREPECHA"),
	Barbarians(1300, 1600, {iDogSoldier: 2}, ((11, 44), (19, 51)), 8, INVADERS, iOwner=iNative, target_area=((13, 41), (19, 47)), adjective="TXT_KEY_ADJECTIVE_CHICHIMECA"),
	Barbarians(1300, 1800, {iHeavySwordsman: 1}, ((54, 33), (58, 38)), 12, NATIVES, adjective="TXT_KEY_ADJECTIVE_WOLOF"),
	Barbarians(1400, 1550, {iKeshik: 1}, ((96, 62), (108, 69)), 10, NOMADS, target_area=((80, 59), (95, 70)), adjective="TXT_KEY_ADJECTIVE_TATAR"),
	Barbarians(1400, 1700, {iHeavySwordsman: 1}, ((75, 17), (80, 23)), 10, MINORS, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_SHONA"),
	Barbarians(1400, 1800, {iNativeRaider: 1}, ((71, 11), (81, 17)), 12, NATIVES, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_NGUNI"),
	Barbarians(1400, 1550, {iLongbowman: 2}, ((21, 49), (27, 54)), 12, NATIVES, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_MUSCOGEE"),
	Barbarians(1450, 1600, {iSkirmisher: 1}, ((33, 12), (34, 16)), 15, NATIVES, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_MAPUCHE"),
	Barbarians(1450, 1700, {iGalleass: 2}, ((125, 44), (134, 57)), 12, PIRATES, adjective="TXT_KEY_ADJECTIVE_WOKOU"),
	Barbarians(1450, 1850, {iMohawk: 1}, ((23, 55), (32, 61)), 8, NATIVES, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_IROQUOIS"),
	Barbarians(1500, 1650, {iGalleass: 1}, ((114, 27), (128, 35)), 8, PIRATES),
	Barbarians(1500, 1700, {iOromoWarrior: 2}, ((82, 29), (88, 32)), 10, PIRATES),
	Barbarians(1500, 1750, {iCuirassier: 2}, ((85, 57), (95, 67)), 12, NOMADS, target_area=((80, 59), (95, 70)), adjective="TXT_KEY_ADJECTIVE_TATAR"),
	Barbarians(1500, 1750, {iArcher: 1}, ((40, 17), (47, 26)), 12, NATIVES, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_TUPI"),
	Barbarians(1500, 1800, {iCamelGunner: 1}, ((56, 39), (76, 44)), 9, NOMADS, target_area=((54, 34), (76, 48)), adjective="TXT_KEY_ADJECTIVE_BERBER"),
	Barbarians(1500, 1800, {iCamelGunner: 1}, ((86, 38), (91, 45)), 10, NOMADS, target_area=((77, 39), (91, 50)), adjective="TXT_KEY_ADJECTIVE_BEDOUIN"),
	Barbarians(1550, 1800, {iCuirassier: 1}, ((96, 62), (108, 69)), 10, NOMADS, target_area=((80, 59), (95, 70)), adjective="TXT_KEY_ADJECTIVE_TATAR"),
	Barbarians(1550, 1850, {iArquebusier: 2}, ((21, 49), (27, 54)), 12, NATIVES, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_MUSCOGEE"),
	Barbarians(1550, 1900, {iArquebusier: 2}, ((58, 31), (64, 35)), 10, NATIVES, adjective="TXT_KEY_ADJECTIVE_ASHANTI"),
	Barbarians(1550, 1750, {iCuirassier: 2}, ((124, 58), (132, 64)), 8, INVADERS, target_area=((117, 46), (129, 59)), adjective="TXT_KEY_ADJECTIVE_MANCHU"),
	Barbarians(1600, 1800, {iPombos: 2}, ((70, 20), (77, 25)), 10, INVADERS, iOwner=iNative, target_area=((69, 21), (77, 30)), adjective="TXT_KEY_ADJECTIVE_CHOKWE"),
	Barbarians(1600, 1800, {iPrivateer: 1}, ((23, 39), (38, 47)), 5, PIRATES),
	Barbarians(1600, 1850, {iCuirassier: 2}, ((92, 57), (109, 64)), 10, NOMADS, target_area=((92, 60), (113, 70)), adjective="TXT_KEY_ADJECTIVE_KAZAKH"),
	Barbarians(1600, 1850, {iCorsair: 1}, ((54, 42), (69, 50)), 8, PIRATES, adjective="TXT_KEY_ADJECTIVE_BARBARY"),
	Barbarians(1600, 1900, {iPistolier: 1}, ((32, 10), (37, 15)), 12, NATIVES, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_MAPUCHE"),
	Barbarians(1650, 1900, {iPrivateer: 1}, ((114, 27), (128, 35)), 8, PIRATES),
	Barbarians(1700, 1900, {iMountedBrave: 1}, ((14, 56), (23, 62)), 12, NOMADS, iOwner=iNative, target_area=((15, 51), (26, 62)), adjective="TXT_KEY_ADJECTIVE_SIOUX"),
	Barbarians(1720, 1850, {iCuirassier: 2}, ((58, 33), (69, 38)), 8, INVADERS, adjective="TXT_KEY_ADJECTIVE_FULANI"),
	Barbarians(1800, 1900, {iPikeman: 2}, ((71, 11), (81, 17)), 10, NATIVES, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_ZULU"),
	Barbarians(1800, 1900, {iMountedBrave: 1}, ((12, 62), (22, 65)), 12, NOMADS, iOwner=iNative, target_area=((15, 57), (26, 66)), adjective="TXT_KEY_ADJECTIVE_CREE"),
	Barbarians(1800, 1900, {iMountedBrave: 1}, ((13, 50), (20, 56)), 9, NOMADS, iOwner=iNative, target_area=((15, 51), (26, 62)), adjective="TXT_KEY_ADJECTIVE_COMANCHE"),
]


@handler("BeginGameTurn")
def onBeginGameTurn():
	for minor_city in minor_cities:
		minor_city.check()
	
	for barbarian in barbarians:
		barbarian.check()
	
	maintainFallenCivilizations()


@handler("unitBuilt")
def assignMinorUnitAdjective(city, unit):
	if not is_minor(city.getOwner()):
		return

	minor_city_adjective = next(minor_city.adjective for minor_city in minor_cities if at(city, minor_city.tile))
	if minor_city_adjective:
		set_unit_adjective(unit, minor_city_adjective)


def maintainFallenCivilizations():
	fallen_civs = civs.major().notalive().where(canEverRespawn)
	
	for iFallenCiv in fallen_civs:
		if periodic(20, iFallenCiv):
			fallen_cities = cities.respawn(iFallenCiv).where(is_minor)
			
			if fallen_cities:
				iTechCiv = best_civ_of_same_tech_group(iFallenCiv)
				if iTechCiv < 0:
					iTechCiv = iFallenCiv
				
				if slot(iTechCiv) < 0:
					continue
				
				iNumDesiredUnits = 2 + player(iTechCiv).getCurrentEra()
				iDefender, iDefenseAI = getUnitForRole(iTechCiv, iDefend)
				
				for city in fallen_cities:
					add_city_buildings(city, iTechCiv)
					
					iNumCurrentUnits = units.at(city).where(CyUnit.canFight).count()
					if iNumCurrentUnits < iNumDesiredUnits:
						makeUnits(city.getOwner(), iDefender, city, iNumDesiredUnits-iNumCurrentUnits, iDefenseAI)
				