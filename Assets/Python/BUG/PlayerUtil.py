## PlayerUtil
##
## Utilities for dealing with Players and their Teams, Cities and Units.
##
## All functions in thie module that take a playerOrID or teamOrID as their
## parameter will accept either the CyPlayer/CyTeam object or its ID.
## Many of them will probably also accept a PyPlayer/PyTeam wrapper, but I
## recommend that you use getCy() on the object instead.
##
##   getPlayer(playerOrID)
##     Returns the CyPlayer given an ID or CyPlayer
##   getPlayerID(playerOrID)
##     Returns the ID given an ID or CyPlayer
##   getPlayerAndID(playerOrID)
##     Returns the ID and CyPlayer given an ID or CyPlayer
##
## Similar functions exist for Teams, Players and Teams together, and active
## versions that don't require an ID or object, using the active player instead.
## All of them return -1 and/or None if given -1 or None for playerOrId.
##
##   players(), teams(), teamPlayers(teamOrID)
##     Loops over players and teams matching various criteria.
##     Only valid objects that were alive at some point are returned, and they can
##     be filtered further by alive, human, barbarian, and/or minor status.
##
##   playerUnits(playerOrID, testFunc), playerCities(playerOrID, testFunc)
##     Loops over a player's units or cities.
##   getPlayerUnits(playerOrID, testFunc), getPlayerCities(playerOrID, testFunc)
##     Returns a list of a player's units or cities.
##
##   isSaltWaterPort(city, eAskingTeam)
##     Returns True if (asking team knows) the CyCity has an adjacent saltwater plot.
##
##   getStateReligion(playerOrID)
##   getFavoriteCivic(playerOrID)
##   getWorstEnemy(playerOrID, askingPlayerOrID)
##     Returns a single piece of information about the given player.
##
##   getVassals(playerOrID, askingPlayerOrID)
##   getDefensivePacts(playerOrID, askingPlayerOrID)
##     Returns lists of players with whom the given player has certain relationships.
##
##   getPossibleEmbargos(playerOrID, askingPlayerOrID)
##   getActiveWars(playerOrID, askingPlayerOrID)
##   getPossibleWars(playerOrID, askingPlayerOrID)
##   isWHEOOH(playerOrID, askingPlayerOrID)
##     Returns various information regarding the war situation for the given player.
##
## Visibility
##
##   canSeeCityList(playerOrID, askingPlayerOrID)
##     Returns True if askingPlayerOrID can see the list of playerOrID's cities.
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *
import TradeUtil
import GameUtil

gc = CyGlobalContext()

## Players and Teams - Getting IDs and Cy objects 

def getPlayer(playerOrID):
	"""Returns the CyPlayer for the given player."""
	if playerOrID is None or playerOrID == -1:
		return None
	if isinstance(playerOrID, int):
		return gc.getPlayer(playerOrID)
	return playerOrID

def getPlayerID(playerOrID):
	"""Returns the Player ID for the given player."""
	if playerOrID is None or playerOrID == -1:
		return -1
	if isinstance(playerOrID, int):
		return playerOrID
	return playerOrID.getID()

def getPlayerAndID(playerOrID):
	"""Returns the Player ID and CyPlayer for the given player."""
	if playerOrID is None or playerOrID == -1:
		return -1, None
	if isinstance(playerOrID, int):
		return playerOrID, gc.getPlayer(playerOrID)
	return playerOrID.getID(), playerOrID


def getTeam(teamOrID):
	"""Returns the CyTeam for the given team."""
	if teamOrID is None or teamOrID == -1:
		return None
	if isinstance(teamOrID, int):
		return gc.getTeam(teamOrID)
	return teamOrID

def getTeamID(teamOrID):
	"""Returns the Team ID for the given team."""
	if teamOrID is None or teamOrID == -1:
		return -1
	if isinstance(teamOrID, int):
		return teamOrID
	return teamOrID.getID()

def getTeamAndID(teamOrID):
	"""Returns the Team ID and CyTeam for the given team."""
	if teamOrID is None or teamOrID == -1:
		return -1, None
	if isinstance(teamOrID, int):
		return teamOrID, gc.getTeam(teamOrID)
	return teamOrID.getID(), teamOrID


def getPlayerTeam(playerOrID):
	"""Returns the CyTeam for the given player."""
	player = getPlayer(playerOrID)
	if player:
		return gc.getTeam(player.getTeam())
	return None

def getPlayerTeamID(playerOrID):
	"""Returns the Team ID for the given player."""
	player = getPlayer(playerOrID)
	if player:
		return player.getTeam()
	return -1

def getPlayerTeamAndID(playerOrID):
	"""Returns the Team ID and CyTeam for the given player."""
	player = getPlayer(playerOrID)
	if player:
		eTeam = player.getTeam()
		return eTeam, gc.getTeam(eTeam)
	return -1, None


def getPlayerAndTeam(playerOrID):
	"""Returns the CyPlayer and CyTeam for the given player."""
	player = getPlayer(playerOrID)
	if player:
		return player, gc.getTeam(player.getTeam())
	return None, None

def getPlayerAndTeamIDs(playerOrID):
	"""Returns the Player ID and Team ID for the given player."""
	ePlayer, player = getPlayer(playerOrID)
	if player:
		return ePlayer, player.getTeam()
	return -1, -1

def getPlayerAndTeamAndIDs(playerOrID):
	"""Returns the Player ID, CyPlayer, Team ID and CyTeam for the given player."""
	ePlayer, player = getPlayerAndID(playerOrID)
	if player:
		eTeam = player.getTeam()
		return ePlayer, player, eTeam, gc.getTeam(eTeam)
	return -1, None, -1, None


def getActivePlayer():
	"""Returns the CyPlayer for the active player."""
	return gc.getActivePlayer()

def getActivePlayerID():
	"""Returns the Player ID for the active player."""
	return gc.getGame().getActivePlayer()

def getActivePlayerAndID():
	"""Returns the Player ID and CyPlayer for the active player."""
	return gc.getGame().getActivePlayer(), gc.getActivePlayer()


def getActiveTeam():
	"""Returns the CyTeam for the active player."""
	return getTeam(getActiveTeamID())

def getActiveTeamID():
	"""Returns the Team ID for the active player."""
	return gc.getGame().getActiveTeam()

def getActiveTeamAndID():
	"""Returns the Team ID and CyTeam for the active player."""
	return getActiveTeamID(), getActiveTeam()


def getActivePlayerAndTeam():
	"""Returns the CyPlayer and CyTeam for the active player."""
	return getActivePlayer(), getActiveTeam()

def getActivePlayerAndTeamIDs():
	"""Returns the Player ID and Team ID for the active player."""
	return getActivePlayerID(), getActiveTeamID()

def getActivePlayerAndTeamAndIDs():
	"""Returns the Player ID, CyPlayer, Team ID and CyTeam for the active player."""
	return getActivePlayerAndID() + getActiveTeamAndID()


## Players and Teams - Iteration

def players(alive=None, human=None, barbarian=None, minor=None, active=None):
	"""
	Creates an iterator for all valid CyPlayers that were ever alive.
	
	Pass in True or False for alive to limit to alive or dead players, respectively.
	Pass in True or False for human to limit to human or AI players, respectively.
	Pass in True or False for barbarian to limit to/from barbarian players, respectively.
	Pass in True or False for minor to limit to/from minor players, respectively.
	Pass in True or False for active to limit to/from players that can ever be active, respectively.
	
	for player in PlayerUtil.players():
		...
	"""
	for ePlayer in range(gc.getMAX_PLAYERS()):
		player = gc.getPlayer(ePlayer)
		if not player.isNone() and player.isEverAlive():
			if matchPlayerOrTeam(player, alive, human, barbarian, minor, active):
				yield player

def teamPlayers(teamOrID, alive=None, human=None, barbarian=None, minor=None, active=None):
	"""
	Creates an iterator for the CyPlayers on the given team.
	
	Pass in True or False for alive to limit to alive or dead players, respectively.
	Pass in True or False for human to limit to human or AI players, respectively.
	Pass in True or False for barbarian to limit to/from barbarian players, respectively.
	Pass in True or False for minor to limit to/from minor players, respectively.
	Pass in True or False for active to limit to/from players that can ever be active, respectively.
	These restrictions are first applied to the CyTeam itself.
	
	for player in PlayerUtil.teamPlayers(PlayerUtil.getActiveTeamID()):
		...
	"""
	eTeam, team = getTeamAndID(teamOrID)
	if matchPlayerOrTeam(team, alive, human, barbarian, minor):
		for player in players(alive, human, barbarian, minor):
			if player.getTeam() == eTeam:
				yield player

def teams(alive=None, human=None, barbarian=None, minor=None, active=None):
	"""
	Creates an iterator for all valid CyTeams that were ever alive.
	
	Pass in True or False for alive to limit to alive or dead teams, respectively.
	Pass in True or False for human to limit to human or AI teams, respectively.
	Pass in True or False for barbarian to limit to/from barbarian teams, respectively.
	Pass in True or False for minor to limit to/from minor players, respectively.
	Pass in True or False for active to limit to/from players that can ever be active, respectively.
	
	for team in PlayerUtil.teams():
		...
	"""
	for eTeam in range(gc.getMAX_TEAMS()):
		team = gc.getTeam(eTeam)
		if (not team.isNone() and team.isEverAlive() 
				and matchPlayerOrTeam(team, alive, human, barbarian, minor)):
			yield team

def matchPlayerOrTeam(teamOrPlayer, alive=None, human=None, barbarian=None, minor=None, active=None):
	"""
	Returns True of the CyPlayer or CyTeam matches the selected filters.
	
	Pass in True or False for alive to limit to alive or dead teams, respectively.
	Pass in True or False for human to limit to human or AI teams, respectively.
	Pass in True or False for barbarian to limit to/from barbarian teams, respectively.
	Pass in True or False for minor to limit to/from minor players, respectively.
	Pass in True or False for active to limit to/from players that can ever be active, respectively.
	
	Pass None (or leave out) for any filter to ignore it.
	"""
	return ((alive is None or alive == teamOrPlayer.isAlive())
			and (human is None or human == teamOrPlayer.isHuman())
			and (barbarian is None or barbarian == teamOrPlayer.isBarbarian())
			and (minor is None or minor == teamOrPlayer.isMinorCiv())
			and (active is None or active == isEverActive(teamOrPlayer)))

def isEverActive(teamOrPlayer):
	"""
	Returns True if the given team/player can ever be the active team/player.
	
	For HotSeat games this includes all human players/teams. For all other game types there is only one.
	"""
	return ((gc.getGame().isHotSeat() and teamOrPlayer.isHuman()) 
			or (isinstance(teamOrPlayer, CyPlayer) and teamOrPlayer.getID() == getActivePlayerID())
			or (isinstance(teamOrPlayer, CyTeam) and teamOrPlayer.getID() == getActiveTeamID()))


## Player Information

def getStateReligion(playerOrID):
	"""Returns the state religion of the given player or -1 if none."""
	player = getPlayer(playerOrID)
	return player.getStateReligion()

def getFavoriteCivic(playerOrID):
	"""
	Returns the favorite civic of the given player's leader or -1 if none.
	
	This works even when the Random Personalities option is enabled.
	"""
	eLeaderType = getPlayer(playerOrID).getPersonalityType()
	if eLeaderType != -1:
		leader = gc.getLeaderHeadInfo(eLeaderType)
		if leader:
			return leader.getFavoriteCivic()
	return CivicTypes.NO_CIVIC

def getWorstEnemy(playerOrID, askingPlayerOrID=None):
	"""
	Returns the CyPlayer who is the worst enemy of playerOrID or None.
	
	If askingPlayerOrID is given, the check is restricted to players they have met.
	"""
	name = getPlayer(playerOrID).getWorstEnemyName()
	if name:
		for player in players(alive=True, barbarian=False, minor=False):
			if player.getName() == name:
				if askingPlayerOrID is not None:
					askingTeam = getPlayerTeam(askingPlayerOrID)
					if (askingTeam and (askingTeam.isHasMet(player.getTeam())
							or gc.getGame().isDebugMode())):
						return player
					return None
				return player
	return None


## Vassalage and other Diplomatic Agreements

def getVassals(playerOrID, askingPlayerOrID):
	"""
	Returns a list of CyPlayers who are vassals of playerOrID.
	
	The askingPlayerOrID is used to limit the list to players they have met.
	"""
	vassals = []
	askedPlayer, askedTeam = getPlayerAndTeam(playerOrID)
	askingPlayer, askingTeam = getPlayerAndTeam(askingPlayerOrID)
	for player in players(alive=True, barbarian=False, minor=False):
		if (askedPlayer.getTeam() != player.getTeam() and 
				(askingTeam.isHasMet(player.getTeam()) or gc.getGame().isDebugMode())):
			team = getPlayerTeam(player)
			if team.isAVassal() and team.isVassal(askedTeam.getID()):
				vassals.append(player)
	return vassals

def getDefensivePacts(playerOrID, askingPlayerOrID):
	"""
	Returns a list of CyPlayers who have a Defensive Pact with playerOrID.
	
	The askingPlayerOrID is used to limit the list to players they have met.
	"""
	pacts = []
	askedPlayer, askedTeam = getPlayerAndTeam(playerOrID)
	askingPlayer, askingTeam = getPlayerAndTeam(askingPlayerOrID)
	for player in players(alive=True, barbarian=False, minor=False):
		if (askedPlayer.getTeam() != player.getTeam() and 
				(askingTeam.isHasMet(player.getTeam()) or gc.getGame().isDebugMode())):
			if askedTeam.isDefensivePact(player.getTeam()):
				pacts.append(player)
	return pacts

def getPossibleEmbargos(playerOrID, askingPlayerOrID):
	"""
	Returns a list of all CyPlayers with which playerOrID will stop trading.
	
	The askingPlayerOrID is used to limit the list to players they have met.
	"""
	askedPlayer, askedTeam = getPlayerAndTeam(playerOrID)
	askingPlayer, askingTeam = getPlayerAndTeam(askingPlayerOrID)
	if not TradeUtil.canTrade(askingPlayer, askedPlayer):
		return ()
	embargos = []
	tradeData = TradeData()
	tradeData.ItemType = TradeableItems.TRADE_EMBARGO
	for player in players(alive=True, barbarian=False, minor=False):
		eTeam = player.getTeam()
		if eTeam == askingPlayer.getTeam() or eTeam == askedPlayer.getTeam() or askedTeam.isAtWar(eTeam):
			# won't embargo your team, their team, or a team they are fighting
			continue
		if not ((askingTeam.isHasMet(eTeam) and askedTeam.isHasMet(eTeam)) or gc.getGame().isDebugMode()):
			# won't embargo someone you or they haven't met
			continue
		tradeData.iData = eTeam
		if askedPlayer.canTradeItem(askingPlayer.getID(), tradeData, True):
			embargos.append(player)
	return embargos


## Wars and WHEOOH

def getActiveWars(playerOrID, askingPlayerOrID):
	"""
	Returns a list of CyPlayers who are at war with playerOrID.
	
	The askingPlayerOrID is used to limit the list to players they have met.
	"""
	wars = []
	askedPlayer, askedTeam = getPlayerAndTeam(playerOrID)
	askingPlayer, askingTeam = getPlayerAndTeam(askingPlayerOrID)
	for player in players(alive=True, barbarian=False, minor=False):
		if askingTeam.isHasMet(player.getTeam()) or gc.getGame().isDebugMode():
			if askedTeam.isAtWar(player.getTeam()):
				wars.append(player)
	return wars

def getPossibleWars(playerOrID, askingPlayerOrID):
	"""
	Returns a tuple containing the WHEOOH status of the given player and 
	a list of all CyPlayers on which playerOrID will declare war in a trade.
	
	The askingPlayerOrID is used to limit the list to players they have met.
	"""
	askedPlayer, askedTeam = getPlayerAndTeam(playerOrID)
	askingPlayer, askingTeam = getPlayerAndTeam(askingPlayerOrID)
	if not TradeUtil.canTrade(askingPlayer, askedPlayer):
		return (False, ())
	wheooh = False
	wars = []
	tradeData = TradeData()
	tradeData.ItemType = TradeableItems.TRADE_WAR
	for player in players(alive=True, barbarian=False, minor=False):
		eTeam = player.getTeam()
		if eTeam == askingPlayer.getTeam() or eTeam == askedPlayer.getTeam() or askedTeam.isAtWar(eTeam):
			# won't DoW your team, their team, or a team they are fighting
			continue
		if not ((askingTeam.isHasMet(eTeam) and askedTeam.isHasMet(eTeam)) or gc.getGame().isDebugMode()):
			# won't DoW someone you or they haven't met
			continue
		tradeData.iData = eTeam
		if askedPlayer.canTradeItem(askingPlayer.getID(), tradeData, False):
			denial = askedPlayer.getTradeDenial(askingPlayer.getID(), tradeData)
			if denial == DenialTypes.NO_DENIAL:
				wars.append(player)
			elif denial == DenialTypes.DENIAL_TOO_MANY_WARS:
				wheooh = True
	return (wheooh, wars)

def isWHEOOH(playerOrID, askingPlayerOrID):
	"""
	Returns True if askingPlayerOrID can see that playerOrID is WHEOOH.
	
	In game terms, this is the case if the player gives the TOO_MANY_WARS denial type
	for a request to go to war against a rival.
	"""
	askedPlayer, askedTeam = getPlayerAndTeam(playerOrID)
	askingPlayer, askingTeam = getPlayerAndTeam(askingPlayerOrID)
	if not TradeUtil.canTrade(askingPlayer, askedPlayer):
		return False
	tradeData = TradeData()
	tradeData.ItemType = TradeableItems.TRADE_WAR
	for player in players(alive=True, barbarian=False, minor=False):
		eTeam = player.getTeam()
		if eTeam == askingPlayer.getTeam() or eTeam == askedPlayer.getTeam() or askedTeam.isAtWar(eTeam):
			# won't DoW your team, their team, or a team they are fighting
			continue
		if not ((askingTeam.isHasMet(eTeam) and askedTeam.isHasMet(eTeam)) or gc.getGame().isDebugMode()):
			# won't DoW someone you or they haven't met
			continue
		tradeData.iData = eTeam
		if askedPlayer.canTradeItem(askingPlayer.getID(), tradeData, False):
			denial = askedPlayer.getTradeDenial(askingPlayer.getID(), tradeData)
			if denial == DenialTypes.DENIAL_TOO_MANY_WARS:
				return True
	return False

def isGivingFavoriteCivicDenial(playerOrID, askingPlayerOrID):
	"""
	Returns True if askingPlayerOrID can see that playerOrID is refusing Civic changes
	because of the "that would go against everything we stand for" FAVORITE_CIVIC denial.
	
	In the unmodified game, this denial type will show for every available civic choice 
	so long as they are running their favorite civic; so we can't tell which civic is the 
	favorite, but we do know that one of their current civics is the favorite one.
	"""
	tradeData = TradeData()
	tradeData.ItemType = TradeableItems.TRADE_CIVIC
	askedPlayer, askedTeam = getPlayerAndTeam(playerOrID)
	askingPlayer, askingTeam = getPlayerAndTeam(askingPlayerOrID)
	if askingTeam.isHasMet(askedTeam.getID()):
		for iCategory in range(gc.getNumCivicOptionInfos()):
			iCivic = askingPlayer.getCivics(iCategory)
			tradeData.iData = iCivic
			if askedPlayer.canTradeItem(askingPlayer.getID(), tradeData, False):
				denial = askedPlayer.getTradeDenial(askingPlayer.getID(), tradeData)
				if denial == DenialTypes.DENIAL_FAVORITE_CIVIC:
					return True
	return False


## Cities

def canSeeCityList(playerOrID):
	"""
	Returns True if the active player can see the list of <player>'s cities.
	
	In the unmodified game, this is possible if the players have met and <player>
	is not a vassal of a rival. They must be able to contact (trade with)
	<player>, and OCC must be disabled. You can always see a teammate's cities.
	"""
	if GameUtil.isOCC():
		return False
	askedPlayer, askedTeam = getPlayerAndTeam(playerOrID)
	askingPlayer, askingTeam = getActivePlayerAndTeam()
	if askingPlayer.getTeam() == askedPlayer.getTeam():
		return True
	if askedTeam.isAVassal() and not askedTeam.isVassal(askingTeam.getID()):
		return False
	return TradeUtil.canTrade(askingPlayer, askedPlayer)

def getNumCities(playerOrID):
	"""
	Returns the actual number of cities owned by <player>.
	"""
	return getPlayer(playerOrID).getNumCities()

def getNumRevealedCities(playerOrID):
	"""
	Returns the number of cities owned by <player> that are revealed to the active player.
	
	The capital city is always counted since you can assume it exists.
	"""
	player = getPlayer(playerOrID)
	eActiveTeam = getActiveTeamID()
	count = 0
	for city in playerCities(player):
		if city.isRevealed(eActiveTeam, False):
			count += 1
	if not player.getCapitalCity().isRevealed(eActiveTeam, False):
		count += 1
	return count

def playerCities(playerOrID, testFunc=None):
	"""
	Creates an iterator for the CyCity objects owned by the given player.
	
	If testFunc is given, only cities for which it returns True are returned.
	
	for city in PlayerUtil.playerCities(PlayerUtil.getActivePlayerID()):
		...
	"""
	player = getPlayer(playerOrID)
	city, iter = player.firstCity(False)
	while city:
		if not city.isNone() and (testFunc is None or testFunc(city)):
			yield city
		city, iter = player.nextCity(iter, False)

def getPlayerCities(playerOrID, testFunc=None):
	"""
	Creates and returns a list containing all the CyCitys owned by the given player.
	
	If testFunc is given, only cities for which it returns True are returned.
	"""
	return [city for city in playerCities(playerOrID, testFunc)]

def isSaltWaterPort(city, askingTeamOrID=None):
	"""
	Returns True if the asking team can tell that the CyCity is on the coast
	of the sea.
	
	If askingTeamOrID is None, the result is as if the owner of the city is asking.
	"""
	if city:
		eAskingTeam = getTeamID(askingTeamOrID)
		map = CyMap()
		for eDirection in range(DirectionTypes.NUM_DIRECTION_TYPES):
			plot = plotDirection(city.getX(), city.getY(), DirectionTypes(eDirection))
			if eAskingTeam != -1 and not plot.isRevealed(eAskingTeam, False):
				continue
			if plot.isWater() and not plot.isLake():
				return True
	return False


## Units

def playerUnits(playerOrID, testFunc=None):
	"""
	Creates an iterator for the CyUnits owned by the given player.
	
	If testFunc is given, only units for which it returns True are returned.
	
	for unit in PlayerUtil.playerUnits(PlayerUtil.getActivePlayerID()):
		...
	"""
	player = getPlayer(playerOrID)
	unit, iter = player.firstUnit(False)
	while unit:
		if not unit.isDead() and (testFunc is None or testFunc(unit)):
			yield unit
		unit, iter = player.nextUnit(iter, False)

def getPlayerUnits(playerOrID, testFunc=None):
	"""
	Creates and returns a list containing all the CyUnits owned by the given player.
	
	If testFunc is given, only units for which it returns True are returned.
	"""
	return [unit for unit in playerUnits(playerOrID, testFunc)]
