## FavoriteCivicDetector
##
## Keeps track of changing Diplomacy modifiers to guess what an
## AI's favorite civic is. The intended use is for the Foreign Advisor
## to figure out and then display the correct favorite civic of an
## AI leader when playing with the Random Personalities option.
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: Dresden

from CvPythonExtensions import *

import AttitudeUtil
import BugUtil
import PlayerUtil
import SdToolKit

# BUG - Mac Support - start
BugUtil.fixSets(globals())
# BUG - Mac Support - end

# globals
gc = CyGlobalContext()

# for sdtoolkit
SD_MOD_ID = "FavoriteCivicDetector"
SD_VAR_ID = "data"

# globals for data
gFavoriteByPlayer = None
gCivicsByCategory = None
gDetectionNecessary = False

# Module-level access functions
def isDetectionNecessary ():
	""" Do we need to bother going through all this fuss?

	It should only be necessary when playing under Random Personalities.
	initHelpers() actually sets the global Boolean; this just returns it.
	"""
	return gDetectionNecessary

def getFavoriteCivicInfo (iPlayer):
	""" Returns the FavoriteCivic object for the given player. 

	If we aren't detecting favorite civic info, creates and returns a new object 
	with the correct data. If the player ID isn't valid or there was some other 
	problem, None is returned.
	"""
	favorite = None
	if gDetectionNecessary:
		if iPlayer in gFavoriteByPlayer:
			favorite = gFavoriteByPlayer[iPlayer]
	else:
		pPlayer = gc.getPlayer(iPlayer)
		if ( pPlayer and (not pPlayer.isNone()) and pPlayer.isAlive() and (not pPlayer.isHuman())
			 and (not pPlayer.isBarbarian()) and (not pPlayer.isMinorCiv()) ):
			favorite = FavoriteCivic(iPlayer)
			favorite.setFavorite(gc.getLeaderHeadInfo(pPlayer.getPersonalityType()).getFavoriteCivic())
	return favorite

def doUpdate ():
	""" Goes through the current diplomacy situation to determine potential favorite civics for each civ. """
	if gDetectionNecessary:
		BugUtil.debug("FavoriteCivicDetector.doUpdate() START")
		pActivePlayer = gc.getActivePlayer()
		pActiveTeam = gc.getTeam(pActivePlayer.getTeam())
		for iPlayer in range(gc.getMAX_PLAYERS()):
			pPlayer = gc.getPlayer(iPlayer)
			# Player we are updating must be a valid, living, non-human, full-fledged civ.
			if ( pPlayer and (not pPlayer.isNone()) and pPlayer.isAlive() and (not pPlayer.isHuman())
				 and (not pPlayer.isBarbarian()) and (not pPlayer.isMinorCiv()) ):
				BugUtil.debug("Updating Info for Player %d (%s)" % (iPlayer, pPlayer.getName()))
				iTeam = pPlayer.getTeam()
				pTeam = gc.getTeam(iTeam)
				# Team assumed valid, living, etc. since the player was.
				if (not pActiveTeam.isHasMet(iTeam)):
					BugUtil.debug(" -- Skipping; active team has not met team we are updating")
					continue
				favorite = gFavoriteByPlayer[iPlayer]
				# Check Diplomacy first (if necessary)
				if not favorite.isKnown():
					if PlayerUtil.isGivingFavoriteCivicDenial(pPlayer, pActivePlayer):
						BugUtil.debug(" -- Player showing FAVORITE_CIVIC trade denial; must be running his/her favorite." )
						for eCategory in range(gc.getNumCivicOptionInfos()):
							eCivic = pPlayer.getCivics(eCategory)
							for eOtherCivic in gCivicsByCategory[eCategory]:
								if (eOtherCivic != eCivic):
									favorite.removePossible(eOtherCivic)
				# Now take Attitude survey (if necessary)
				if not favorite.isKnown():
					for iOtherPlayer in range(gc.getMAX_PLAYERS()):
						pOtherPlayer = gc.getPlayer(iOtherPlayer)
						# Test attitude against other valid, living, full-fledged civs; these can be human
						if ( pOtherPlayer and (iOtherPlayer != iPlayer) 
							 and (not pOtherPlayer.isNone()) and pOtherPlayer.isAlive() 
							 and (not pOtherPlayer.isBarbarian()) and (not pOtherPlayer.isMinorCiv()) ):
							BugUtil.debug(" -- Testing against Player %d (%s)" % (iOtherPlayer, pOtherPlayer.getName()))
							iOtherTeam = pOtherPlayer.getTeam()
							if ( (not pActiveTeam.isHasMet(iOtherTeam)) or (not pTeam.isHasMet(iOtherTeam)) ):
								BugUtil.debug("     -- Skipping; either active team or updating team has not met test team")
								continue
							pAttitude = AttitudeUtil.Attitude(iPlayer, iOtherPlayer)
							bFoundPossibleFavorite = pAttitude.hasModifier("TXT_KEY_MISC_ATTITUDE_FAVORITE_CIVIC")
							for eCategory in range(gc.getNumCivicOptionInfos()):
								eCivic = pPlayer.getCivics(eCategory)
								if (eCivic == pOtherPlayer.getCivics(eCategory)):
									if bFoundPossibleFavorite:
										BugUtil.debug("     -- Players share civic %d (%s) and %s is giving the diplo modifier." 
													  % (eCivic, gc.getCivicInfo(eCivic).getText(), pPlayer.getName()))
										BugUtil.debug("         -- This is the only possible favorite in category %d (%s)." 
													  % (eCategory, gc.getCivicOptionInfo(eCategory).getText()))
										for eOtherCivic in gCivicsByCategory[eCategory]:
											if (eOtherCivic != eCivic):
												favorite.removePossible(eOtherCivic)
									else:
										BugUtil.debug("     -- Players share civic %d (%s) but %s is NOT giving the diplo modifier." 
													  % (eCivic, gc.getCivicInfo(eCivic).getText(), pPlayer.getName()))
										BugUtil.debug("         -- This one must be ruled out as a possible favorite.")
										favorite.removePossible(eCivic)
								else:
									if bFoundPossibleFavorite:
										BugUtil.debug("     -- Players do NOT share civic %d (%s) but %s is giving the diplo modifier." 
													  % (eCivic, gc.getCivicInfo(eCivic).getText(), pPlayer.getName()))
										BugUtil.debug("         -- All civics in category %d (%s) must be ruled out." 
													  % (eCategory, gc.getCivicOptionInfo(eCategory).getText()))
										for eOtherCivic in gCivicsByCategory[eCategory]:
											favorite.removePossible(eOtherCivic)
									else:
										BugUtil.debug("     -- Players do NOT share civic %d (%s) and %s is NOT giving the diplo modifier." 
													  % (eCivic, gc.getCivicInfo(eCivic).getText(), pPlayer.getName()))
										BugUtil.debug("         -- This doesn't tell us anything new.") 
				BugUtil.debug(" -- Finished update for %s: %s" % (pPlayer.getName(), str(favorite)))
		#dump()

def initData ():
	""" Initialize the internal civic-tracking data structure, clearing all previous data. """
	if gDetectionNecessary:
		BugUtil.debug("FavoriteCivicDetector.initData() initializing gFavoriteByPlayer")
		global gFavoriteByPlayer
		gFavoriteByPlayer = {}
		for iPlayer in range(gc.getMAX_PLAYERS()):
			gFavoriteByPlayer[iPlayer] = FavoriteCivic(iPlayer)

def initHelpers ():
	""" Initialize the helper data structures, clearing all previous data. 

	Because most of the functions in this module always start out checking
	whether detection is necessary, this is stored in a global Boolean which
	is set here based on game options and then directly accessed everywhere
	else; it can be also accessed outside the module via an accessor function.

	The other helper which is setup here is a dict of civics keyed on their
	category. This is useful because the civic detection algorithms often
	need to exclude either an entire category or all but one civic in a
	given category. This data structure allows us to simply iterate over a 
	specific category instead of having to iterate over all civics each time.
	"""
	global gDetectionNecessary
	gDetectionNecessary = gc.getGame().isOption(GameOptionTypes.GAMEOPTION_RANDOM_PERSONALITIES)
	BugUtil.debug("FavoriteCivicDetector.initHelpers() gDetectionNecessary: %s" % (str(gDetectionNecessary)))
	if gDetectionNecessary:
		BugUtil.debug("FavoriteCivicDetector.initHelpers() initializing gCivicsByCategory")
		global gCivicsByCategory
		gCivicsByCategory = {}
		for eCategory in range(gc.getNumCivicOptionInfos()):
			gCivicsByCategory[eCategory] = set()
		for eCivic in range(gc.getNumCivicInfos()):
			gCivicsByCategory[gc.getCivicInfo(eCivic).getCivicOptionType()].add(eCivic)

def dump (*args):
	""" Outputs data for all given player(s); if no players are specified, dumps for everyone. """
	if gDetectionNecessary:
		if not args:
			args = range(gc.getMAX_PLAYERS())
		BugUtil.debug("FavoriteCivicDetector.dump() Dumping data for players %s." % (str(args)))
		for iPlayer in args:
			pPlayer = gc.getPlayer(iPlayer)
			if ( pPlayer and (not pPlayer.isNone()) and pPlayer.isAlive() and (not pPlayer.isHuman())
				 and (not pPlayer.isBarbarian()) and (not pPlayer.isMinorCiv()) ):
				if (iPlayer in gFavoriteByPlayer):
					BugUtil.debug(str(gFavoriteByPlayer[iPlayer]))
				else:
					BugUtil.debug("FavoriteCivicDetector.dump() No data for player %d!" % (iPlayer))
	else:
		BugUtil.debug("FavoriteCivicDetector.dump() Nothing to dump; detection isn't necessary.")

NO_CIVIC = -1
class FavoriteCivic:
	""" The class that handles internal data management of the favorite civics.

	On initialization, the set of possible civics is empty to conserve space; we
	only begin tracking civics and therefore explicitly listing possibilities once
	the active player has met the other player and some knowledge has been gained.

	This means there is some special handling on methods such as isPossible() to 
	show all civics as possible even though the internal data structure is empty.
	"""

	def __init__(self, iPlayer):
		""" Class initialization. Parameter is this player's id. """
		self.iPlayer = iPlayer
		self.eFavorite = NO_CIVIC
		self.possibles = None

	def initPossibles(self):
		""" Initializes set of possible favorites and removes starter civics. """
		self.possibles = set(range(gc.getNumCivicInfos()))
		pPlayer = gc.getPlayer(self.iPlayer)
		if ( pPlayer and (not pPlayer.isNone()) and pPlayer.isAlive() and (not pPlayer.isHuman())
				 and (not pPlayer.isBarbarian()) and (not pPlayer.isMinorCiv()) ):
			# Initially rule out all "starter" civics
			pCiv = gc.getCivilizationInfo(pPlayer.getCivilizationType())
			for eCategory in range(gc.getNumCivicOptionInfos()):
				self.possibles.remove(pCiv.getCivilizationInitialCivics(eCategory))

	def isInitialState(self):
		""" Returns True if this structure is unchanged from initialization. """
		return (self.eFavorite == NO_CIVIC and self.possibles == None)

	def isKnown(self):
		""" Do we know this player's favorite civic? """
		return (self.eFavorite != NO_CIVIC)

	def getPlayer(self):
		""" Returns ID number for this player. """
		return self.iPlayer

	def getFavorite(self):
		""" Returns ID of favorite for this player or NO_CIVIC if not yet known. """
		return self.eFavorite

	def setFavorite(self, eCivic):
		""" Explicitly sets favorite for this player to given civic. """
		#BugUtil.debug("FavoriteCivic.setFavorite() attempting to set player %d favorite civic to %d (%s)"
		#			  % (self.iPlayer, eCivic, gc.getCivicInfo(eCivic).getText()))
		if (eCivic != NO_CIVIC):
			self.eFavorite = eCivic
			self.possibles = None

	def isPossible(self, eCivic):
		""" Returns True if given civic might be this player's favorite. """
		if self.isKnown():
			return (self.eFavorite == eCivic)
		elif self.isInitialState():
			return True
		else:
			return (eCivic in self.possibles)

	def removePossible(self, eCivic):
		""" Removes given civic from the possibilities for this player. """
		if self.isInitialState():
			self.initPossibles()
		if self.isPossible(eCivic):
			self.possibles.remove(eCivic)
			if len(self.possibles) == 1:
				# Favorite has been found; clean up internal data.
				self.eFavorite = self.possibles.pop()
				self.possibles = None

	def getPossibles(self):
		""" Returns tuple of ids for all possible favorite civics for this player. """
		if self.isKnown():
			return (self.eFavorite,)
		elif self.isInitialState():
			return tuple(range(gc.getNumCivicInfos()))
		else:
			return tuple(self.possibles)

	def getNumPossibles(self):
		""" Returns number of possible favorite civics for this player. """
		if (self.isKnown()):
			return 1
		elif self.isInitialState():
			return gc.getNumCivicInfos()
		else:
			return len(self.possibles)

	def __str__ (self):
		""" String representation of class instance. """
		szReturnText = "FavoriteCivic { iPlayer = %d, " % (self.iPlayer)
		szText = "UNKNOWN"
		if self.isKnown():
			szText = gc.getCivicInfo(self.eFavorite).getText()
		szReturnText = szReturnText + "eFavorite: %d (%s), " % (self.eFavorite, szText)
		szReturnText = szReturnText + "possibles: %s }" % (str(self.possibles))
		return szReturnText

class FavoriteCivicDetector:
	def __init__(self, eventManager):
		BugUtil.debug("FavoriteCivicDetector.__init__(). Resetting data and initing event manager.")
		initHelpers()
		eventManager.addEventHandler('BeginActivePlayerTurn', self.onBeginActivePlayerTurn)
		eventManager.addEventHandler("GameStart", self.onGameStart)
		eventManager.addEventHandler("OnLoad", self.onLoadGame)
		eventManager.addEventHandler("OnPreSave", self.onPreSave)
		eventManager.addEventHandler("CivicDemanded", self.onCivicDemanded)
		
	def onBeginActivePlayerTurn(self, argsList):
		""" Called when the active player can start making their moves. """
		if gDetectionNecessary:
			iActivePlayer = argsList[0]
			iTurn = argsList[1]
			BugUtil.debug("======================================================================")
			BugUtil.debug("FavoriteCivicDetectorEvent.onBeginActivePlayerTurn() START Turn %d" % (iTurn))
			doUpdate()
			BugUtil.debug("FavoriteCivicDetectorEvent.onBeginActivePlayerTurn() Update Complete.")

	def onGameStart(self, argsList):
		""" Called when a new game is started """
		#BugUtil.debug("FavoriteCivicDetectorEvent.onGameStart()")
		initHelpers()
		if gDetectionNecessary:
			initData()

	def onLoadGame(self, argsList):
		""" Called when a game is loaded """
		#BugUtil.debug("FavoriteCivicDetectorEvent.onLoadGame()")
		initHelpers()
		if gDetectionNecessary:
			data = SdToolKit.sdGetGlobal(SD_MOD_ID, SD_VAR_ID)
			if (data):
				global gFavoriteByPlayer
				gFavoriteByPlayer = data
				#BugUtil.debug("Data Loaded:")
				#dump()
			else:
				#BugUtil.debug("No saved data. Initializing new data.")
				initData()

	def onPreSave(self, argsList):
		""" Called before a game is actually saved """
		#BugUtil.debug("FavoriteCivicDetectorEvent.onPreSave()")
		if gDetectionNecessary:
			if (gFavoriteByPlayer):
				bNeedToSave = False
				for iPlayer in range(gc.getMAX_PLAYERS()):
					if not gFavoriteByPlayer[iPlayer].isInitialState():
						bNeedToSave = True
						break
				if (bNeedToSave):
					SdToolKit.sdSetGlobal(SD_MOD_ID, SD_VAR_ID, gFavoriteByPlayer)
					#BugUtil.debug("Data Saved to sdtoolkit")

	def onCivicDemanded(self, argsList):
		""" Called when AI demands you switch to their favorite civic. """
		ePlayer, eTargetPlayer, eCivic = argsList
		#BugUtil.debug("FavoriteCivicDetectorEvent.onCivicDemanded(ePlayer = %d, eTargetPlayer = %d, eCivic = %d)"
		#			  % (ePlayer, eTargetPlayer, eCivic))
		if gDetectionNecessary:
			kFavorite = getFavoriteCivicInfo(ePlayer)
			kFavorite.setFavorite(eCivic)
