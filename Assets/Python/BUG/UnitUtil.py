## UnitUtil
##
## Utilities for dealing with Civ4 Units and their related objects.
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *
import BugUtil
import PlayerUtil

# BUG - Mac Support - start
BugUtil.fixSets(globals())
# BUG - Mac Support - end

gc = CyGlobalContext()

NUM_UNITS = 0
NUM_CLASSES = 0
NUM_OR_BONUSES = 0
NUM_AND_TECHS = 0

TRAIN_CAN = 0
TRAIN_CANNOT = 1
TRAIN_LACK_BONUS = 2

# units that don't require any resources to build
unitsWithoutBonuses = set()
# units that require at least one resource to build
unitsWithBonuses = set()
# bonuses that are required to build at least one unit
strategicBonuses = set()
# unit ID -> set of tech IDs
unitTechs = dict()

# unit ID -> tuple ( set of units which can upgrade to it, 
#                    set of units to which it can be upgraded )
# e.g. Bowman -> ( (Archer),
#                  (Longbowman, Crossbowman, Rifleman, ...) )
genericUnits = set()
genericUnitIDs = dict()

upgradeUnits = dict()
genericUpgradeUnits = dict()

olderUnits = dict()
newerUnits = dict()

def init():
	"""
	Segregates units into two sets: those that require resources and those that don't.
	Creates a map of units from ID to the set of tech prerequisites.
	"""
	global NUM_UNITS, NUM_CLASSES
	NUM_UNITS = gc.getNumUnitInfos()
	NUM_CLASSES = gc.getNumUnitClassInfos()
	global NUM_OR_BONUSES, NUM_AND_TECHS
	NUM_OR_BONUSES = gc.getNUM_UNIT_PREREQ_OR_BONUSES()
	NUM_AND_TECHS = gc.getNUM_UNIT_AND_TECH_PREREQS()
	for eUnit in range(NUM_UNITS):
		unitInfo = gc.getUnitInfo(eUnit)
		BugUtil.debug("==== %s ====", unitInfo.getDescription())
		
		# generic unit
		classInfo = gc.getUnitClassInfo(unitInfo.getUnitClassType())
		eGenericUnit = classInfo.getDefaultUnitIndex()
		genericUnitIDs[eUnit] = eGenericUnit
		if eUnit == eGenericUnit:
			genericUnits.add(eUnit)
		else:
			BugUtil.debug("  unique of %s",
					gc.getUnitInfo(eGenericUnit).getDescription())
		
		# resource sets
		found = False
		eBonus = unitInfo.getPrereqAndBonus()
		if eBonus != -1:
			found = True
			strategicBonuses.add(eBonus)
			BugUtil.debug("  requires %s", gc.getBonusInfo(eBonus).getDescription())
		for i in range(NUM_OR_BONUSES):
			eBonus = unitInfo.getPrereqOrBonuses(i)
			if eBonus != -1:
				found = True
				strategicBonuses.add(eBonus)
				BugUtil.debug("  requires %s", gc.getBonusInfo(eBonus).getDescription())
		if found:
			unitsWithBonuses.add(eUnit)
		else:
			unitsWithoutBonuses.add(eUnit)
		
		# tech map
		techs = set()
		unitTechs[eUnit] = techs
		eTech = unitInfo.getPrereqAndTech()
		if eTech != -1:
			techs.add(eTech)
		for i in range(NUM_AND_TECHS):
			eTech = unitInfo.getPrereqAndTechs(i)
			if eTech != -1:
				techs.add(eTech)
		for eTech in techs:
			BugUtil.debug("  requires %s", gc.getTechInfo(eTech).getDescription())
		
	# upgrade maps
	for eUnit in range(NUM_UNITS):
		getOlderUnits(eUnit)
		getNewerUnits(eUnit)
	
	initOrders()

def unitInfos():
	"""Iterates through all CvUnitInfos."""
	for eUnit in range(NUM_UNITS):
		yield gc.getUnitInfo(eUnit)

def unitClassInfos():
	"""Iterates through all CvUnitClassInfos."""
	for eClass in range(NUM_CLASSES):
		yield gc.getUnitClassInfo(eClass)

def isGeneric(eUnit):
	"""Returns True if the given unit is generic and valid."""
	return eUnit in genericUnits

def isUnique(eUnit):
	"""Returns True if the given unit is unique and valid."""
	return eUnit not in genericUnits and eUnit != -1

def getGeneric(eUnit):
	"""
	Returns the generic unit counterpart to the given unique unit or the same
	unit if it's not unique.
	"""
	return genericUnitIDs[eUnit]

def getGenerics(units):
	"""
	Returns a set of the generic units which are counterparts to the unique units
	in the given set. Generic units in the set are not returned.
	"""
	generics = set()
	for eUnit in units:
		eGenericUnit = genericUnitIDs[eUnit]
		if eGenericUnit != eUnit:
			generics.add(eGenericUnit)
	return generics

def getGenericUpgrades(eUnit):
	"""Returns the set of all generic units to which eUnit can upgrade."""
	return genericUpgradeUnits[eUnit]

def getUpgrades(eUnit):
	"""Returns the set of all units to which eUnit can upgrade."""
	return upgradeUnits[eUnit]

def getOlderUnits(eUnit):
	"""Returns the set of all units from which eUnit can upgrade."""
	if eUnit in olderUnits:
		return olderUnits[eUnit]
	unitInfo = gc.getUnitInfo(eUnit)
	eClass = unitInfo.getUnitClassType()
	units = set()
	olderUnits[eUnit] = units
	for eOldUnit in range(NUM_UNITS):
		oldUnitInfo = gc.getUnitInfo(eOldUnit)
		if oldUnitInfo.getUpgradeUnitClass(eClass):
			#BugUtil.debug("%s -> %s", oldUnitInfo.getDescription(), unitInfo.getDescription())
			units.add(eOldUnit)
			units |= getOlderUnits(eOldUnit)
	return units

def getNewerUnits(eUnit):
	"""Returns the set of all units to which eUnit can upgrade."""
	if eUnit in newerUnits:
		return newerUnits[eUnit]
	unitInfo = gc.getUnitInfo(eUnit)
	upgrades = set()
	upgradeUnits[eUnit] = upgrades
	genericUpgrades = set()
	genericUpgradeUnits[eUnit] = genericUpgrades
	newer = set()
	newerUnits[eUnit] = newer
	for eNewUnit in range(NUM_UNITS):
		newUnitInfo = gc.getUnitInfo(eNewUnit)
		if unitInfo.getUpgradeUnitClass(newUnitInfo.getUnitClassType()):
			#BugUtil.debug("%s -> %s", unitInfo.getDescription(), newUnitInfo.getDescription())
			upgrades.add(eNewUnit)
			if isGeneric(eNewUnit):
				genericUpgrades.add(eNewUnit)
			newer.add(eNewUnit)
			newer |= getNewerUnits(eNewUnit)
	return newer

def isUnitOrUpgradeInSet(eUnit, units):
	"""
	Returns True if eUnit is in the given set of units or can be upgraded
	to at least one unit in it.
	"""
	return eUnit in units or len(getNewerUnits(eUnit) & units) > 0

def areUpgradesInSet(eUnit, units):
	"""
	Returns True if every immediate upgrade of eUnit is in the given set.
	
	This ignores transitive upgrades (Warrior doesn't check for Macemen).
	
	Need to take UUs into consideration.
	"""
	upgrades = getUpgrades(eUnit)
	return upgrades <= units

def replaceUniqueUnits(units):
	"""
	Replaces unique units with their generic counterparts in the given set.
	"""
	uniques = set()
	generics = set()
	for eUnit in units:
		if isUnique(eUnit):
			uniques.add(eUnit)
			generics.add(getGeneric(eUnit))
	units -= uniques
	units += generics

def findObsoleteUnits(units):
	"""
	Returns a set containing the units whose immediate upgrades are all in the set,
	taking unique units into consideration.
	
	For example, if the set contains Maceman and Redcoat, neither is returned,
	but if it contains Grenadier as well, Maceman is returned.
	"""
	#result = units.copy()
	generics = getGenerics(units)
	obsoletes = set()
	for eUnit in units:
#		unitInfo = gc.getUnitInfo(eUnit)
		upgrades = getGenericUpgrades(eUnit)
		if upgrades:
			for eUpgradeUnit in upgrades:
				if eUpgradeUnit not in units and eUpgradeUnit not in generics:
#					BugUtil.debug("findObsoleteUnits - %s, cannot build %s", 
#							unitInfo.getDescription(),
#							gc.getUnitInfo(eUpgradeUnit).getDescription())
					break
			else:
				obsoletes.add(eUnit)
	return obsoletes

def getKnownUnits(playerOrID):
	player, team = PlayerUtil.getPlayerAndTeam(playerOrID)
	units = set()
	for eUnit in range(NUM_UNITS):
		for eTech in unitTechs[eUnit]:
			if team.isHasTech(eTech):
				units.add(eUnit)
	return units

def getKnowableUnits(playerOrID):
	player, team = PlayerUtil.getPlayerAndTeam(playerOrID)
	units = set()
	for eUnit in range(NUM_UNITS):
		for eTech in unitTechs[eUnit]:
			if not (team.isHasTech(eTech) or player.canResearch(eTech, False)):
				break
		else:
			units.add(eUnit)
	return units

def getTrainableUnits(playerOrID, knowableUnits, checkCities=True, military=None):
	"""
	Returns the set of all units the player can train, including obsolete ones.
	"""
	game = CyGame()
	player, team = PlayerUtil.getPlayerAndTeam(playerOrID)
	civInfo = gc.getCivilizationInfo(player.getCivilizationType())
	if checkCities:
		cities = PlayerUtil.getPlayerCities(player)
	else:
		cities = None
	units = set()
	BugUtil.debug("%s =========", player.getName())
	for eClass in range(NUM_CLASSES):
		eUnit = civInfo.getCivilizationUnits(eClass)
		if eUnit == -1 or eUnit not in knowableUnits:
			#BugUtil.debug("  %s -> unknowable", gc.getUnitClassInfo(eClass).getDescription())
			continue
		unitInfo = gc.getUnitInfo(eUnit)
		# military
		if military is not None:
			combat = (unitInfo.getUnitCombatType() > 0 or unitInfo.getNukeRange() != -1
					or unitInfo.getAirCombat() > 0)
			if military != combat:
				#BugUtil.debug("  %s -> combat is %s", unitInfo.getDescription(), combat)
				continue
		# OCC and Settlers
		if game.isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE) and unitInfo.isFound():
			BugUtil.debug("  %s -> no founding units in OCC", unitInfo.getDescription())
			continue
		# techs
		for eTech in unitTechs[eUnit]:
			if not team.isHasTech(eTech):
				BugUtil.debug("  %s -> doesn't know %s", unitInfo.getDescription(), 
						gc.getTechInfo(eTech).getDescription())
				missing = True
				break
		else:
			missing = False
		if missing:
			continue
		# state religion
		eReligion = unitInfo.getStateReligion()
		if eReligion != -1 and player.getStateReligion() != eReligion:
			BugUtil.debug("  %s -> wrong state religion", unitInfo.getDescription())
			continue
		# nukes
		if (game.isNoNukes() or not game.isNukesValid()) and unitInfo.getNukeRange() != -1:
			BugUtil.debug("  %s -> no nukes", unitInfo.getDescription())
			continue
		# getSpecialUnitType, game.isSpecialUnitValid
		eSpecialType = unitInfo.getSpecialUnitType()
		if eSpecialType != -1 and not game.isSpecialUnitValid(eSpecialType):
			BugUtil.debug("  %s -> special unit type %s invalid", unitInfo.getDescription(),
					gc.getSpecialUnitInfo(eSpecialType).getDescription())
			continue
		# cities
		if cities and not canAnyCityBuildUnit(eUnit, cities, -1, True):
			BugUtil.debug("  %s -> no city can train unit", unitInfo.getDescription())
			continue
		BugUtil.debug("  %s", unitInfo.getDescription())
		units.add(eUnit)
	return units

def getTrainableAndUntrainableUnits(playerOrID, knowableUnits, military=None):
	player, team = PlayerUtil.getPlayerAndTeam(playerOrID)
	cities = PlayerUtil.getPlayerCities(player)
	# separate units into two groups: yes and no
	units = getTrainableUnits(playerOrID, knowableUnits, False, military)
	yesUnits = set()
	noUnits = set()
	BugUtil.debug("-----------------------")
	for eUnit in units:
		if canAnyCityBuildUnit(eUnit, cities, -1, True):
			BugUtil.debug("  yes %s", gc.getUnitInfo(eUnit).getDescription())
			yesUnits.add(eUnit)
		else:
			BugUtil.debug("  no  %s", gc.getUnitInfo(eUnit).getDescription())
			noUnits.add(eUnit)
	return yesUnits, noUnits

def getKnownTrainableUnits(playerOrID, askingPlayerOrID, knowableUnits, bonuses, military=None):
	player, team = PlayerUtil.getPlayerAndTeam(playerOrID)
	askingPlayer = PlayerUtil.getPlayer(askingPlayerOrID)
	eAskingTeam, askingTeam = PlayerUtil.getPlayerTeamAndID(askingPlayer)
	#trade = player.canTradeNetworkWith(askingPlayer.getID())
	cities = PlayerUtil.getPlayerCities(player, 
			lambda city: city.isRevealed(eAskingTeam, False))
	# separate units into two groups: yes and maybe
	units = getTrainableUnits(playerOrID, knowableUnits, False, military)
	yesUnits = set()
	maybeUnits = set()
	BugUtil.debug("-----------------------")
	for eUnit in units:
		if not canAnyCityBuildUnit(eUnit, cities, eAskingTeam, False):
			BugUtil.debug("  no    %s", gc.getUnitInfo(eUnit).getDescription())
		elif hasBonusesForUnit(eUnit, bonuses):
			BugUtil.debug("  yes   %s", gc.getUnitInfo(eUnit).getDescription())
			yesUnits.add(eUnit)
		elif bonuses is None:
			BugUtil.debug("  maybe %s", gc.getUnitInfo(eUnit).getDescription())
			maybeUnits.add(eUnit)
	return yesUnits, maybeUnits

def hasBonusesForUnit(eUnit, bonuses):
	if eUnit not in unitsWithBonuses:
		return True
	if not bonuses:
		return False
	unitInfo = gc.getUnitInfo(eUnit)
	eBonus = unitInfo.getPrereqAndBonus()
	if eBonus != -1 and eBonus not in bonuses:
		return False
	requiresBonus = False
	for i in range(NUM_OR_BONUSES):
		eBonus = unitInfo.getPrereqOrBonuses(i)
		if eBonus != -1:
			requiresBonus = True
			if eBonus in bonuses:
				break
	else:
		if requiresBonus:
			return False
	return True

def canAnyCityBuildUnit(eUnit, cities=None, askingTeamOrID=-1, checkBonuses=True):
	eAskingTeam = PlayerUtil.getTeamID(askingTeamOrID)
	unitInfo = gc.getUnitInfo(eUnit)
	if cities:
		for city in cities:
			if canCityBuildUnit(unitInfo, city, eAskingTeam, checkBonuses):
				return True
		return False
	else:
		return canCityBuildUnit(unitInfo, None, eAskingTeam, checkBonuses)

def canCityBuildUnit(unitInfo, city, eAskingTeam, checkBonuses=True):
	# religion
	if unitInfo.isPrereqReligion():
		if not city or city.getReligionCount() > 0:
			# EF: Seems odd to enforce NO religions in the city, 
			#     but this is how CvPlot.canTrain() does it.
			#     The function should actually be called isPrereqNoReligion().
			return False
	eReligion = unitInfo.getPrereqReligion()
	if eReligion != -1 and not (city and city.isHasReligion(eReligion)):
		return False
	# corporation
	eCorp = unitInfo.getPrereqCorporation()
	if eCorp != -1 and not (city and city.isActiveCorporation(eCorp)):
		return False
	# skipping isPrereqBonuses as the land part looks broken
	# and we don't want to limit work boats if all resources are covered
	# domain
	if unitInfo.getDomainType() == DomainTypes.DOMAIN_SEA:
		if not (city and PlayerUtil.isSaltWaterPort(city, eAskingTeam)):
			return False
		# EF: this is how CyPlot does it
		#plot = city.plot()
		#if not plot.isWater() or not plot.isCoastalLand(unitInfo.getMinAreaSize()):
		#	continue
	else:
		minArea = unitInfo.getMinAreaSize()
		if minArea != -1:
			if eAskingTeam != -1 or not city or city.plot().area().getNumTiles() < minArea:
				return False
	# holy city
	eReligion = unitInfo.getHolyCity()
	if eReligion != -1 and not (city and city.isHolyCity(eReligion)):
		return False
	# building
	eBuilding = unitInfo.getPrereqBuilding()
	if eBuilding != -1:
		if eAskingTeam != -1 or not city:
			return False
		if city.getNumBuilding(eBuilding) == 0:
			eSpecialBuilding = gc.getBuildingInfo(eBuilding).getSpecialBuildingType()
			if eSpecialBuilding == -1 or not gc.getPlayer(city.getOwner()).isSpecialBuildingNotRequired(eSpecialBuilding):
				return False
	# resources
	if checkBonuses and not cityHasBonusesForUnit(unitInfo, city):
		return False
	# passes all tests for this city
	return True

def cityHasBonusesForUnit(unitInfo, city):
	if not city:
		return False
	eBonus = unitInfo.getPrereqAndBonus()
	if eBonus != -1 and not city.hasBonus(eBonus):
		return False
	requiresBonus = False
	for i in range(NUM_OR_BONUSES):
		eBonus = unitInfo.getPrereqOrBonuses(i)
		if eBonus != -1:
			requiresBonus = True
			if city.hasBonus(eBonus):
				break
	else:
		if requiresBonus:
			return False
	return True

def getCanTrainUnits(playerOrID, askingPlayerOrID=None, military=None):
	"""
	Returns the set of all units the player can train.
	
	Searches all of the player's cities to find which units can be trained.
	
	If askingPlayerOrID is given, only cities they have seen are checked, and
	only units whose prerequisite techs they know or can research are returned.
	Also, if the two players' trade networks are not connected, units that
	require resources to train are returned in a second set.
	
	If military is provided, only military or civilian units are checked
	depending on its value, True or False, respectively.
	
	*** OBSOLETE ***
	
	"""
	player, team = PlayerUtil.getPlayerAndTeam(playerOrID)
	askingPlayer = PlayerUtil.getPlayer(askingPlayerOrID)
	if askingPlayer:
		eAskingTeam, askingTeam = PlayerUtil.getPlayerTeamAndID(askingPlayer)
		trade = player.canTradeNetworkWith(askingPlayer.getID())
	civInfo = gc.getCivilizationInfo(player.getCivilizationType())
	units = set()
	maybeUnits = set()
	for eClass in range(NUM_CLASSES):
		eUnit = civInfo.getCivilizationUnits(eClass)
		if eUnit == -1:
			classInfo = gc.getUnitClassInfo(eClass)
			BugUtil.debug("%s doesn't have %s", civInfo.getDescription(), classInfo.getDescription())
			eUnit = classInfo.getDefaultUnitIndex()
		unitInfo = gc.getUnitInfo(eUnit)
		if unitInfo:
			if ((military == True and unitInfo.getUnitCombatType() <= 0)
			or (military == False and unitInfo.getUnitCombatType() > 0)):
				BugUtil.debug("skipping (non-)military %s", unitInfo.getDescription())
				continue
			if askingPlayer:
				for eTech in unitTechs[eUnit]:
					if not (askingTeam.isHasTech(eTech) or askingPlayer.canResearch(eTech, False)):
						BugUtil.debug("%s doesn't comprehend %s", askingPlayer.getName(), gc.getTechInfo(eTech).getDescription())
						skip = True
						break
				else:
					skip = False
				if skip:
					BugUtil.debug("skipping unknowable %s", unitInfo.getDescription())
					continue
			for city in PlayerUtil.playerCities(player):
				if askingPlayer:
					if not city.isRevealed(eAskingTeam, False):
						continue
					if city.canTrain(eUnit, False, not trade):
						if eUnit in unitsWithBonuses:
							maybeUnits.add(eUnit)
						else:
							units.add(eUnit)
						break
				else:
					if city.canTrain(eUnit, False, False):
						units.add(eUnit)
						break
	BugUtil.debug("%s can train:", player.getName())
	for eUnit in units:
		unitInfo = gc.getUnitInfo(eUnit)
		BugUtil.debug("  %s", unitInfo.getDescription())
	if askingPlayer:
		BugUtil.debug("%s can maybe train:", player.getName())
		for eUnit in maybeUnits:
			unitInfo = gc.getUnitInfo(eUnit)
			BugUtil.debug("  %s", unitInfo.getDescription())
		return units, maybeUnits
	else:
		return units

(
	ORDER_NONE,
	
	ORDER_SKIP,
	ORDER_SLEEP,
	ORDER_FORTIFY,
	ORDER_HEAL,
	
	ORDER_SENTRY,
	ORDER_INTERCEPT,
	ORDER_PATROL,
	ORDER_PLUNDER,
	
	ORDER_BUILD,  # improvement
	ORDER_CONSTRUCT,  # building
	ORDER_GOTO,
	ORDER_EXPLORE,
	
	ORDER_AUTO_BUILD,
	ORDER_AUTO_NETWORK,
	ORDER_AUTO_CITY,
	ORDER_AUTO_RELIGION,
) = range(17)

ORDERS_BY_ACTIVITY = {
	ActivityTypes.ACTIVITY_AWAKE: ORDER_NONE,
	ActivityTypes.ACTIVITY_INTERCEPT: ORDER_INTERCEPT,
	ActivityTypes.ACTIVITY_PATROL: ORDER_PATROL,
	ActivityTypes.ACTIVITY_PLUNDER: ORDER_PLUNDER,
	ActivityTypes.ACTIVITY_HEAL: ORDER_HEAL,
	ActivityTypes.ACTIVITY_SENTRY: ORDER_SENTRY,
	ActivityTypes.ACTIVITY_HOLD: ORDER_SKIP,
}
ORDERS_BY_AUTOMATION = {
	AutomateTypes.AUTOMATE_EXPLORE: ORDER_EXPLORE,
	AutomateTypes.AUTOMATE_BUILD: ORDER_AUTO_BUILD,
	AutomateTypes.AUTOMATE_NETWORK: ORDER_AUTO_NETWORK,
	AutomateTypes.AUTOMATE_CITY: ORDER_AUTO_CITY,
	AutomateTypes.AUTOMATE_RELIGION: ORDER_AUTO_RELIGION,
}
MOVE_TO_MISSIONS = [
	MissionTypes.MISSION_MOVE_TO, 
	MissionTypes.MISSION_MOVE_TO_UNIT,
]

def getOrder(unit):
	group = unit.getGroup()
	eActivityType = group.getActivityType()
	if eActivityType in ORDERS_BY_ACTIVITY:
		return ORDERS_BY_ACTIVITY[eActivityType]
	eAutomationType = group.getAutomateType()
	if eAutomationType in ORDERS_BY_AUTOMATION:
		return ORDERS_BY_AUTOMATION[eAutomationType]
	if (group.getLengthMissionQueue() > 0):
		# TODO: loop to find the first non-goto and check in ORDERS_BY_MISSION
		eMissionType = group.getMissionType(0)
		if eMissionType == MissionTypes.MISSION_BUILD:
			return ORDER_BUILD
		elif eMissionType in MOVE_TO_MISSIONS:
			return ORDER_GOTO
	elif (unit.isWaiting()):
		if (unit.isFortifyable()):
			return ORDER_FORTIFY
		else:
			return ORDER_SLEEP
	return ORDER_NONE

def initOrders():
	"""
	Adds orders added by BULL.
	"""
	try:
		ORDERS_BY_ACTIVITY[ActivityTypes.ACTIVITY_SENTRY_WHILE_HEAL] = ORDER_HEAL
		ORDERS_BY_ACTIVITY[ActivityTypes.ACTIVITY_SENTRY_LAND_UNITS] = ORDER_SENTRY
		ORDERS_BY_ACTIVITY[ActivityTypes.ACTIVITY_SENTRY_NAVAL_UNITS] = ORDER_SENTRY
		MOVE_TO_MISSIONS.append(MissionTypes.MISSION_MOVE_TO_SENTRY)
	except:
		pass
