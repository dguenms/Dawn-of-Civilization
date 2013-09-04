## AttitudeUtil
##
## Utility functions for dealing with AI Attitudes.
##
## Notes
##   - Must be initialized externally by calling init()
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: Ruff_hi, EmperorFool

from CvPythonExtensions import *
import BugUtil
import FontUtil
import PlayerUtil
import re

NUM_ATTITUDES = 5

DEFAULT_COLORS = (
	"COLOR_RED", 
	"COLOR_CYAN", 
	"COLOR_CLEAR", 
	"COLOR_GREEN", 
	"COLOR_YELLOW",
)

ATTITUDE_KEYS = (
	"furious", 
	"annoyed", 
	"cautious", 
	"pleased", 
	"friendly", 
)
ATTITUDE_COLORS = None
ATTITUDE_ICONS = None

# These are also defaults; XML will override
ATTITUDE_MODIFIERS = (
	"TXT_KEY_MISC_ATTITUDE_LAND_TARGET",
	"TXT_KEY_MISC_ATTITUDE_WAR",
	"TXT_KEY_MISC_ATTITUDE_PEACE",
	"TXT_KEY_MISC_ATTITUDE_SAME_RELIGION",
	"TXT_KEY_MISC_ATTITUDE_DIFFERENT_RELIGION",
	"TXT_KEY_MISC_ATTITUDE_BONUS_TRADE",
	"TXT_KEY_MISC_ATTITUDE_OPEN_BORDERS",
	"TXT_KEY_MISC_ATTITUDE_DEFENSIVE_PACT",
	"TXT_KEY_MISC_ATTITUDE_RIVAL_DEFENSIVE_PACT",
	"TXT_KEY_MISC_ATTITUDE_RIVAL_VASSAL",
	"TXT_KEY_MISC_ATTITUDE_SHARE_WAR",
	"TXT_KEY_MISC_ATTITUDE_FAVORITE_CIVIC",
	"TXT_KEY_MISC_ATTITUDE_TRADE",
	"TXT_KEY_MISC_ATTITUDE_RIVAL_TRADE",
	"TXT_KEY_MISC_ATTITUDE_FREEDOM",
	"TXT_KEY_MISC_ATTITUDE_EXTRA_GOOD",
# Show Hidden Attitudes in BULL
	"TXT_KEY_MISC_ATTITUDE_FIRST_IMPRESSION",
	"TXT_KEY_MISC_ATTITUDE_TEAM_SIZE",
	"TXT_KEY_MISC_ATTITUDE_BETTER_RANK",
	"TXT_KEY_MISC_ATTITUDE_WORSE_RANK",
	"TXT_KEY_MISC_ATTITUDE_LOW_RANK",
	"TXT_KEY_MISC_ATTITUDE_LOST_WAR",
)
MODIFIER_STRING_TO_KEY = None

gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()


## Initialization

def init (colors=DEFAULT_COLORS, modifiers=None):
	"""Initializes this module, raising ConfigError if any problems occur."""
	# create font icons for each attitude level
	global ATTITUDE_ICONS
	ATTITUDE_ICONS = [FontUtil.getChar(key) for key in ATTITUDE_KEYS]
	if len(ATTITUDE_ICONS) != NUM_ATTITUDES:
		raise BugUtil.ConfigError("Failed to create attitude icons")
	
	# convert colors to type IDs
	if len(colors) != NUM_ATTITUDES:
		raise BugUtil.ConfigError("Expected %d colors" % NUM_ATTITUDES)
	global ATTITUDE_COLORS
	ATTITUDE_COLORS = map(gc.getInfoTypeForString, colors)
	invalidCount = ATTITUDE_COLORS.count(-1)
	if invalidCount > 0:
		invalid = []
		for id, color in zip(ATTITUDE_COLORS, colors):
			if id == -1:
				invalid.append(color)
		raise BugUtil.ConfigError("Given %d invalid colors: %s" % (invalidCount, str(invalid)))

	# init modifiers, overriding default list as necessary
	if modifiers is not None and (isinstance(modifiers, list) or isinstance(modifiers, tuple)):
		global ATTITUDE_MODIFIERS
		ATTITUDE_MODIFIERS = tuple(modifiers)
	initModifiers()


## Attitude

def hasAttitude (nPlayer, nTarget):
	"""Returns True if nTarget can see nPlayer's attitude toward them."""
	return (nPlayer != -1 and nTarget != -1 and nPlayer != nTarget
	        and gc.getTeam(gc.getPlayer(nPlayer).getTeam()).isHasMet(gc.getPlayer(nTarget).getTeam()))

def getAttitudeString (nPlayer, nTarget):
	"""Returns the full hover text with attitude modifiers nPlayer has toward nTarget."""
	if hasAttitude(nPlayer, nTarget):
		return CyGameTextMgr().getAttitudeString(nPlayer, nTarget)
	return None

def getAttitudeCategory (nPlayer, nTarget):
	"""Returns the attitude level nPlayer has toward nTarget [0,4]."""
	if hasAttitude(nPlayer, nTarget):
		return gc.getPlayer(nPlayer).AI_getAttitude(nTarget)
	return None

def getAttitudeColor (nPlayer, nTarget):
	"""Returns the color of the attitude nPlayer has toward nTarget."""
	iCategory = getAttitudeCategory(nPlayer, nTarget)
	if iCategory is not None:
		return ATTITUDE_COLORS[iCategory]
	return -1

def getAttitudeIcon (nPlayer, nTarget):
	"""Returns the font icon of the attitude nPlayer has toward nTarget."""
	iCategory = getAttitudeCategory(nPlayer, nTarget)
	if iCategory is not None:
		return ATTITUDE_ICONS[iCategory]
	return ""

def getAttitudeCount (nPlayer, nTarget):
	"""Returns the total attitude modifiers nPlayer has toward nTarget."""
	sAttStr = getAttitudeString(nPlayer, nTarget)
	if sAttStr == None:
		return
	nAtt = 0
	# TODO: Replace with simple line-by-line handling
	#	    so it doesn't get tricked by leader names (": " fixes issue)
	ltPlusAndMinuses = re.findall ("[-+][0-9]+\s?: ", sAttStr)
	for i in range (len (ltPlusAndMinuses)):
		nAtt += int (ltPlusAndMinuses[i][:-2])
	return nAtt


def getAttitudeText (nPlayer, nTarget, bNumber, bSmily, bWorstEnemy, bWarPeace):
	"""Returns a string describing the attitude nPlayer has toward nTarget."""
	nAttitude = getAttitudeCount (nPlayer, nTarget)
	if nAttitude == None:
		return None
	
	szText = []
	if bSmily:
		szText.append(getAttitudeIcon(nPlayer, nTarget))
	if bNumber:
		szText.append(BugUtil.colorText(u"%+d" % nAttitude, getAttitudeColor(nPlayer, nTarget)))
	
	szIcons = u""
	pPlayer = gc.getPlayer(nPlayer)
	pTarget = gc.getPlayer(nTarget)
	if bWorstEnemy and isWorstEnemy(pPlayer, pTarget):
		szIcons += FontUtil.getChar("angrypop")
	
	if bWarPeace:
		nTeam = pPlayer.getTeam()
		pTeam = gc.getTeam(nTeam)
		nTargetTeam = pTarget.getTeam()
		pTargetTeam = gc.getTeam(nTargetTeam)
		if pTeam.isAtWar(nTargetTeam):
			szIcons += FontUtil.getChar("war")
		elif gc.getGame().getActiveTeam() in (nTeam, nTargetTeam):
			bPeace = False
			if pTeam.isForcePeace(nTargetTeam):
				bPeace = True
			elif pTargetTeam.isAVassal():
				for nOwnerTeam in range(gc.getMAX_TEAMS()):
					if pTargetTeam.isVassal(nOwnerTeam) and pTeam.isForcePeace(nOwnerTeam):
						bPeace = True
						break
			if bPeace:
				szIcons += FontUtil.getChar("peace")
	if szIcons:
		szText.append(szIcons)
	
	return u" ".join(szText)

def initModifiers (argsList=None):
	""" Creates the dictionary that maps strings to modifier keys. """
	global MODIFIER_STRING_TO_KEY
	MODIFIER_STRING_TO_KEY = {}
	for sKey in ATTITUDE_MODIFIERS:
		sStr = BugUtil.getPlainText(sKey, "NONE")
		if (sStr != "NONE"):
			# These modifier strings should contain the '%d: ' prefix
			# so we need to extract just the portion in quotes.
			pMatch = re.match(u"^.*(\".+\")", sStr, re.UNICODE)
			if (pMatch):
				MODIFIER_STRING_TO_KEY[unicode(pMatch.group(1))] = sKey
	for iMemType in range(MemoryTypes.NUM_MEMORY_TYPES):
		sKey = str(gc.getMemoryInfo(iMemType).getTextKey())
		sStr = BugUtil.getPlainText(sKey, "NONE")
		if (sStr != "NONE"):
			# These modifier strings have no extra text and so
			# we can use them directly
			MODIFIER_STRING_TO_KEY[unicode(sStr)] = sKey
	#BugUtil.debug(u"initModifiers() MODIFIER_STRING_TO_KEY = %s" % str(MODIFIER_STRING_TO_KEY))

class Attitude:
	""" Holds summary of attitude that this player has toward target player.

	If the two IDs are the same or the two players have not met, the
	class will be filled with generic default values. We also check to see
	that the active player has met both players, and the accessor functions
	will react differently depending on if this is the case. 
	"""
	def __init__ (self, iThisPlayer, iTargetPlayer):
		pActiveTeam = gc.getTeam(gc.getActivePlayer().getTeam())
		iThisTeam = gc.getPlayer(iThisPlayer).getTeam()
		pThisTeam = gc.getTeam(iThisTeam)
		iTargetTeam = gc.getPlayer(iTargetPlayer).getTeam()
		self.iThisPlayer = iThisPlayer
		self.iTargetPlayer = iTargetPlayer
		self.iAttitudeSum = 0
		self.iAttitudeModifiers = {}
		self.bHasActiveMetBoth = CyGame().isDebugMode() or (pActiveTeam.isHasMet(iThisTeam) and pActiveTeam.isHasMet(iTargetTeam)) 
		self.eAttitudeType = AttitudeTypes.NO_ATTITUDE
		# This might be better off being something descriptive such as
		# "players have not met" or "players are the same"
		self.sAttitudeString = ""
		if (iThisPlayer != iTargetPlayer and pThisTeam.isHasMet(iTargetTeam)):
			self.eAttitudeType = gc.getPlayer(iThisPlayer).AI_getAttitude(iTargetPlayer)
			self.sAttitudeString = CyGameTextMgr().getAttitudeString(iThisPlayer, iTargetPlayer)
			for sLine in self.sAttitudeString.split("\n"):
				#BugUtil.debug(u"LINE: %s" % (sLine))
				pMatch = re.match("^.*>([-\+]\d+)\s?:\s+(\".+\")<.*$", sLine, re.UNICODE)
				if (pMatch):
					#BugUtil.debug(u"MATCH: (%s) (%s)" %(pMatch.group(1), pMatch.group(2)))
					iValue = int(pMatch.group(1))
					sString = unicode(pMatch.group(2))
					self.iAttitudeSum += iValue
					if sString in MODIFIER_STRING_TO_KEY:
						self.iAttitudeModifiers[MODIFIER_STRING_TO_KEY[sString]] = iValue
						#BugUtil.debug(u"Attitude::init() - Added to dict: %s" % (sString))
					else:
						BugUtil.debug(u"Attitude::init() - Attitude string contains unknown modifier text: %s" % (sString))
		#BugUtil.debug(u"Attitude::init() complete.")
		BugUtil.debug(u"%s"  % (self))

	def __str__ (self):
		""" String representation of class instance. """
		return (u"Attitude { 'iThisPlayer': %d, 'iTargetPlayer': %d, 'iAttitudeSum': %d, 'eAttitudeType': %d, 'bHasActiveMetBoth': %s,\n 'iAttitudeModifiers': %s,\n 'sAttitudeString': %s }" 
				% (self.iThisPlayer, self.iTargetPlayer, self.iAttitudeSum, self.eAttitudeType,
				   self.bHasActiveMetBoth, str(self.iAttitudeModifiers), self.sAttitudeString))

	def hasModifier (self, sKey):
		""" Does the attitude contain given modifier? """
		if self.bHasActiveMetBoth:
			return (sKey in self.iAttitudeModifiers)
		return False

	def getModifier (self, sKey):
		""" Returns integer value of given attitude modifer. """
		if self.bHasActiveMetBoth:
			if sKey in self.iAttitudeModifiers:
				return self.iAttitudeModifiers[sKey]
		return 0

	def hasAttitude (self):
		""" Does this player have any attitude toward the target? """
		if self.bHasActiveMetBoth:
			return (not self.eAttitudeType == AttitudeTypes.NO_ATTITUDE)
		return False

	def getCount (self):
		""" Returns total (visible) count of attitude modifiers. """
		if self.bHasActiveMetBoth:
			return self.iAttitudeSum
		return 0

	def getCategory (self):
		""" Returns attitude category as an AttitudeTypes enum. """
		if self.bHasActiveMetBoth:
			return self.eAttitudeType
		return AttitudeTypes.NO_ATTITUDE

	def getString (self):
		""" Returns full diplomacy text string. """
		if self.bHasActiveMetBoth:
			return self.sAttitudeString
		return ""

	def getIcon (self):
		""" Returns smilie icon string based on attitude type. """
		if self.bHasActiveMetBoth:
			eCategory = self.getCategory()
			if eCategory != AttitudeTypes.NO_ATTITUDE:
				return ATTITUDE_ICONS[int(eCategory)]
		return ""

	def getColor (self):
		""" Returns the color of the attitude this player has toward target. """
		if self.bHasActiveMetBoth:
			eCategory = self.getCategory()
			if eCategory != AttitudeTypes.NO_ATTITUDE:
				return ATTITUDE_COLORS[int(eCategory)]
		return -1
	
	def getText (self, bNumber, bSmily, bWorstEnemy, bWarPeace):
		""" Returns a string describing the attitude this player has toward target. """
		if self.bHasActiveMetBoth:
			nAttitude = self.getCount()

			if bNumber:
				szText = str (nAttitude)
				if nAttitude > 0:
					szText = "+" + szText
				if bSmily:
					szText = "[" + szText + "] "
				else:
					szText = "<font=3>   " + szText + "</font> "
			else:
				szText = ""

			iColor = self.getColor()
			szText = BugUtil.colorText(szText, iColor)
			if bSmily:
				szText = self.getIcon() + " " + szText

			pThisPlayer = gc.getPlayer(self.iThisPlayer)
			pTargetPlayer = gc.getPlayer(self.iTargetPlayer)
			if bWorstEnemy and isWorstEnemy(pThisPlayer, pTargetPlayer):
				szText +=  u"%c" %(CyGame().getSymbolID(FontSymbols.ANGRY_POP_CHAR))

			if bWarPeace:
				iThisTeam = pThisPlayer.getTeam()
				pThisTeam = gc.getTeam(iThisTeam)
				iTargetTeam = pTargetPlayer.getTeam()
				pTargetTeam = gc.getTeam(iTargetTeam)
				if pThisTeam.isAtWar(iTargetTeam):
					szText += u"%c" % (gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar() + 25)
				elif gc.getGame().getActiveTeam() in (iThisTeam, iTargetTeam):
					bPeace = False
					if pThisTeam.isForcePeace(iTargetTeam):
						bPeace = True
					elif pTargetTeam.isAVassal():
						for iOwnerTeam in range(gc.getMAX_TEAMS()):
							if pTargetTeam.isVassal(iOwnerTeam) and pThisTeam.isForcePeace(iOwnerTeam):
								bPeace = True
								break
					if bPeace:
						szText += u"%c" % (gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar() + 26)
		
			return szText
		return ""
	

## Worst Enemy
##
## Each non-human team has a worst enemy team.
## CyPlayer.getWorstEnemyName() returns the names of everyone on their hated team separated by slashes (/).

def isWorstEnemy(playerOrID, enemyOrID):
	"""
	Returns True if <enemy> is one of the worst enemies of <player>'s team.
	"""
	player, team = PlayerUtil.getPlayerAndTeam(playerOrID)
	enemy, enemyTeam = PlayerUtil.getPlayerAndTeam(enemyOrID)
	return not team.isHuman() and team.getID() != enemyTeam.getID() and getWorstEnemyTeam(player) == enemyTeam.getID()

def getWorstEnemies(playerOrID):
	"""
	Returns a list containing the player IDs that are worst enemies of <player>'s team.
	"""
	eTeam = getWorstEnemyTeam(playerOrID)
	enemies = []
	if eTeam != -1:
		for player in PlayerUtil.teamPlayers(eTeam, alive=True, barbarian=False):
			enemies.append(player.getID())
	return enemies

def getWorstEnemyTeam(playerOrID):
	"""
	Returns the team ID that is the worst enemy of <player>'s team.
	
	If <player>'s team has no worst enemy, returns -1.
	"""
	player, team = PlayerUtil.getPlayerAndTeam(playerOrID)
	if not team.isHuman():
		worstEnemyName = player.getWorstEnemyName()
		if worstEnemyName:
			for team in PlayerUtil.teams(alive=True, barbarian=False):
				if team.getName() == worstEnemyName:
					return team.getID()
	return -1

def getWorstEnemyTeams():
	"""
	Returns a dictionary of the team IDs that are each team's worst enemy.
	
	The key is team ID; the value is the worst enemy team ID.
	If a team has no worst enemy, -1 is stored as its value.
	Ignores dead, human, barbarian, and minor teams.
	
	Loops over players because CyTeam does not have getWorstEnemyName().
	"""
	namesToID = {}
	for team in PlayerUtil.teams(alive=True, barbarian=False, minor=False):
		namesToID[team.getName()] = team.getID()
	enemies = {}
	for team in PlayerUtil.teams(alive=True, human=False, barbarian=False, minor=False):
		eTeam = team.getID()
		eLeader = team.getLeaderID()
		if eLeader != -1:
			player = PlayerUtil.getPlayer(eLeader)
			worstEnemyName = player.getWorstEnemyName()
			if worstEnemyName:
				try:
					enemies[eTeam] = namesToID[worstEnemyName]
				except KeyError:
					BugUtil.debug("Cannot find team \"%s\"", worstEnemyName)
					enemies[eTeam] = -1
			else:
				enemies[eTeam] = -1
	return enemies
