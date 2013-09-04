## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
## EventSigns.py for the BUG Mod by Dresden
##
## Keeps track of plot signs created by the EventSigns random
## event interface and displays them once the plot is visible.
##

from CvPythonExtensions import *

import BugUtil
import CvUtil
import PlayerUtil
import CvRandomEventInterface
import SdToolKit

# Bug Options
import BugCore
EventSignsOpt = BugCore.game.EventSigns

# BUG - Mac Support - start
BugUtil.fixSets(globals())
# BUG - Mac Support - end

# civ globals
gc = CyGlobalContext()
engine = CyEngine()
localText = CyTranslator()
map = CyMap()

# for sdtoolkit
SD_MOD_ID = "EventSigns"
SD_VAR_ID = "savedSigns"

# globals for data
gSavedSigns = None
gCurrentSigns = None
g_bShowSigns = False
g_bForceUpdate = False

# Module-level access functions
def initData ():
	""" Initialize the internal plot-caption data structure, clearing all previous data. """
	BugUtil.debug("EventSigns.initData() initializing gSavedSigns")
	global gSavedSigns
	gSavedSigns = MapSigns()
	return True

def initOptions ():
	""" Initialization based upon BUG Options. """
	global g_bShowSigns
	g_bShowSigns = EventSignsOpt.isEnabled()
	BugUtil.debug("EventSigns.initOptions() initializing. g_bShowSigns is %s." %(g_bShowSigns))
	return True

def enabledOptionChanged (pIniObject, bNewValue):
	""" Handler function for processing changes to the Enabled option. """
	BugUtil.debug("EventSigns.enabledOptionsChanged(%s, %s) resetting g_bShowSigns." %(str(pIniObject), str(bNewValue)))
	global g_bShowSigns
	if g_bShowSigns != bNewValue:
		g_bShowSigns = bNewValue
		if gSavedSigns == None:
			initData()
		gSavedSigns.processSigns(g_bShowSigns)
	return True

def addSign (pPlot, ePlayer, szCaption):
	""" Wrapper for CyEngine.addSign() which stores sign data. 
	If -1 is passed for ePlayer, the sign is assumed to be a landmark that everyone can see.
	"""
	#BugUtil.debug("EventSigns.addSign(pPlot = %s, ePlayer = %s, szCaption = %s)" % (str(pPlot), str(ePlayer), szCaption))
	if not pPlot or pPlot.isNone():
		BugUtil.warn("EventSigns.addSign() was passed an invalid plot: %s" % (str(pPlot)))
		return False
	if gSavedSigns == None:
		BugUtil.warn("EventSigns.addSign() gSavedSigns is not initialized!")
		return False
	gSavedSigns.storeSign(pPlot, ePlayer, szCaption)
	gSavedSigns.displaySign(pPlot, ePlayer)
	SdToolKit.sdSetGlobal(SD_MOD_ID, SD_VAR_ID, gSavedSigns)
	return True

def updateCurrentSigns ():
	""" Updates gCurrentSigns global with all current signs on map. Remember to clear when done."""
	global gCurrentSigns
	gCurrentSigns = MapSigns()
	for iSign in range(engine.getNumSigns()):
		pSign = engine.getSignByIndex(iSign)
		pPlot = pSign.getPlot()
		ePlayer = pSign.getPlayerType()
		szCaption = pSign.getCaption()
		if not gCurrentSigns.hasPlotSigns(pPlot):
			gCurrentSigns[pPlot] = PlotSigns(pPlot)
		gCurrentSigns[pPlot].setSign(ePlayer, szCaption)
	BugUtil.debug("EventSigns.updateCurrentSigns() finished.\n %s" % (str(gCurrentSigns)))
	return True

def clearCurrentSigns ():
	""" Resets gCurrentSigns global; should always be called when finished after an update. """
	global gCurrentSigns
	gCurrentSigns = None


def clearSignsAndLandmarks(pPlot):
	""" Removes any current landmarks or signs from a plot.

	In order to place a new sign or landmark I'd like to remove any pre-existing sign
	or landmark on the plot. However, there seems to be some delay or synch issue.
	Every attempt I have thus far made would remove the old one but the new one would
	not show up. So for now, I am not removing old signs/landmarks and thus the event
	will only place the sign/landmark on a plot if there isn't already one there.
	If I could resolve that issue, this function would actually be used. ;)
	"""
	for iPlayer in range(gc.getMAX_PLAYERS()):
		engine.removeSign(pPlot, iPlayer)
	engine.removeLandmark(pPlot)
	# Don't even know what this does; it was the last of my failed attempts to force the signs to show.
	#engine.setDirty(EngineDirtyBits.GlobeTexture_DIRTY_BIT, True)
	return true

def placeLandmark(pPlot, sEventType, iFood, iProd, iComm, bIsSign, iSignOwner):
	""" Places a landmark on a plot identifying a yield change with a short description.

	Parameters:
	* pPlot is the CyPlot object for the plot to mark.
	* sEventType is the str key for the event which is used to get the sign's descriptive caption.
	* iFood, iProd, and iComm are the integer yield changes which will be noted on the caption.
	* bIsSign will be True if we want a team-specific sign and False if we want a generic landmark.
	* iSignOwner is the player number for the visibility of the sign. If it's -1, all players get one.
	Note that iSignOwner is unused if bIsSign is False since everyone can see landmarks.
	"""
	# Bail out early if EventSigns are disabled
	if not EventSignsOpt.isEnabled(): return False
	
	# Bail out if there are no yield changes
	if iFood == 0 and iProd == 0 and iComm == 0: return False

	# This next bit is unused; see the docstring at the start of that function for why.
	#clearSignsAndLandmarks(pPlot)

	sCaptionFood = ""
	sCaptionProd = ""
	sCaptionComm = ""
	sCaptionDesc = localText.getText("TXT_KEY_SIGN_" + sEventType, ())

	# Note the extra spaces added for separation after each yield adjustment; you can remove them
	# if you want a more condensed sign; the reason they are here instead of in the XML formats
	# is because I couldn't come up with a simple way to make them appear only if the yield changes.
	if (iFood != 0):
		sCaptionFood = localText.getText("TXT_KEY_SIGN_FORMAT_FOOD", (iFood, )) + u" "
	if (iProd != 0):
		sCaptionProd = localText.getText("TXT_KEY_SIGN_FORMAT_PROD", (iProd, )) + u" "
	if (iComm != 0):
		sCaptionComm = localText.getText("TXT_KEY_SIGN_FORMAT_COMM", (iComm, )) + u" "

	sCaption = localText.getText("TXT_KEY_SIGN_FORMAT_OVERVIEW", (sCaptionFood, sCaptionProd, sCaptionComm, sCaptionDesc))

	if (bIsSign):
		if (iSignOwner == -1):
			# add signs for all valid human players who are still alive.
			for pPlayer in PlayerUtil.players(human=True, alive=True):
				addSign(pPlot, pPlayer.getID(), sCaption)
		else:
			addSign(pPlot, iSignOwner, sCaption)
	else:
		engine.addLandmark(pPlot, sCaption)

	return True

def applyLandmarkFromEvent(argsList):
	""" Generic event callback function to place signs/landmarks when event changes plot yields """
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	event = gc.getEventInfo(iEvent)
	iFood = event.getPlotExtraYield(YieldTypes.YIELD_FOOD)
	iProd = event.getPlotExtraYield(YieldTypes.YIELD_PRODUCTION)
	iComm = event.getPlotExtraYield(YieldTypes.YIELD_COMMERCE)

	if ( (iFood != 0) or (iProd != 0) or (iComm != 0) ):
		pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
		placeLandmark(pPlot, event.getType(), iFood, iProd, iComm, True, -1)

	return True


class MapSigns:
	""" A collection of PlotSigns, organized by plot. """

	def __init__ (self):
		""" Class initialization. """
		self.reset()

	def reset (self):
		""" Resets data for this instance to defaults. """
		self.plotDict = {}

	def isEmpty (self):
		""" Check to see if object has any PlotSigns data. """
		return (len(self.plotDict) == 0)

	def getPlotSigns (self, pPlot):
		""" Returns PlotSigns object for given Plot. """
		thisKey = self.__getKey(pPlot)
		if thisKey in self.plotDict:
			return self.plotDict[thisKey]
		else:
			return None

	def __getitem__ (self, pPlot):
		""" Special method to allow access like pPlotSigns = pMapSigns[pPlot] """
		return self.getPlotSigns(pPlot)

	def setPlotSigns (self, pPlot, pPlotSigns):
		""" Sets PlotSigns object for given Plot. """
		thisKey = self.__getKey(pPlot)
		self.plotDict[thisKey] = pPlotSigns
		return None

	def __setitem__ (self, pPlot, pPlotSigns):
		""" Special method to allow access like pMapSigns[pPlot] = pPlotSigns """
		return self.setPlotSigns(pPlot, pPlotSigns)

	def removePlotSigns(self, pPlot):
		""" Removes PlotSigns object for given Plot. """
		thisKey = self.__getKey(pPlot)
		if thisKey in self.plotDict:
			del self.plotDict[thisKey]
			return True
		return False

	def __delitem__ (self, pPlot):
		""" Special method to allow access like del pMapSigns[pPlot] """
		return self.removePlotSigns(pPlot)

	def hasPlotSigns (self, pPlot):
		""" Do we have a PlotSigns element corresponding to that plot? """
		thisKey = self.__getKey(pPlot)
		if thisKey in self.plotDict:
			return True
		return False

	def __str__ (self):
		""" String representation of class instance. """
		#return "MapSigns { plotDict=%s }" % (str(self.plotDict))
		# The above doesn't seem to propagate the %s to the PlotSigns, so we do it the long way
		szText = "MapSigns { plotDict = {"
		for key in self.plotDict:
			pPlotSigns = self.plotDict[key]
			szText = szText + "\n\t" + str(key) + ": " + str(pPlotSigns) + ", "
		szText = szText + " } }"
		return szText

	def storeSign (self, pPlot, ePlayer, szCaption):
		""" Stores sign data in the appropraite PlotSigns element. """
		thisKey = self.__getKey(pPlot)
		if not thisKey:
			BugUtil.warn("MapSigns.storeSign() could not determine valid keyname for Plot %s." % (str(pPlot)))
			return False
		if not thisKey in self.plotDict:
			self.plotDict[thisKey] = PlotSigns(pPlot)
		self.plotDict[thisKey].setSign(ePlayer, szCaption)

	def displaySign (self, pPlot, ePlayer):
		""" Displays stored sign for given player at given plot based on revealed status.
		If there's a pre-existing sign, engine.addSign will silently fail, leaving the plot unchanged.
		"""
		if not g_bShowSigns:
			BugUtil.debug("MapSigns.displaySign() called but EventSigns is disabled.")
			return False
		if not pPlot or pPlot.isNone():
			BugUtil.warn("MapSigns.displaySign() was passed an invalid plot: %s" % (str(pPlot)))
			return False
		thisKey = self.__getKey(pPlot)
		szCaption = ""
		if self.hasPlotSigns(pPlot):
			szCaption = self.plotDict[thisKey].getSign(ePlayer)
		else:
			#BugUtil.debug("MapSigns.displaySign() could not show sign; we don't have any saved signs on plot %s" % (str(thisKey)))
			return False
		if not szCaption:
			BugUtil.debug("MapSigns.displaySign() could not show sign; no caption found for player %d on plot %s" % (ePlayer, str(thisKey)))
			return False
		if ePlayer == -1:
			BugUtil.debug("MapSigns.displaySign() landmark (%s) shown on plot %s" % (szCaption, ePlayer, str(thisKey)))
			engine.addLandmark(pPlot, szCaption.encode('latin_1'))
		else:
			pPlayer = gc.getPlayer(ePlayer)
			if not pPlayer or pPlayer.isNone():
				BugUtil.warn("MapSigns.displaySign() was passed an invalid player id: %s" % (str(ePlayer)))
				return False
			eTeam = pPlayer.getTeam()
			if pPlot.isRevealed(eTeam, False):
				BugUtil.debug("MapSigns.displaySign() sign (%s) shown for player %d on plot %s" % (szCaption, ePlayer, str(thisKey)))
				engine.addSign(pPlot, ePlayer, szCaption.encode('latin_1'))
				return True
			else:
				BugUtil.debug("MapSigns.displaySign() could not show sign; player %d cannot see plot %s" % (ePlayer, str(thisKey)))
		return False

	def hideSign (self, pPlot, ePlayer):
		""" Hides sign for given player at given plot if there's a current sign the same as the stored one. 
		Note that this function assumes gCurrentSigns is up-to-date so make sure you've updated first.
		"""
		if not pPlot or pPlot.isNone():
			BugUtil.warn("MapSigns.hideSign() was passed an invalid plot: %s" % (str(pPlot)))
			return False
		thisKey = self.__getKey(pPlot)
		if gCurrentSigns == None:
			BugUtil.debug("MapSigns.hideSign() finds no current signs so there's nothing to hide.")
			return False
		if self.hasPlotSigns(pPlot):
			szCaption = self.plotDict[thisKey].getSign(ePlayer)
			if gCurrentSigns.hasPlotSigns(pPlot):
				szExistingCaption = gCurrentSigns[pPlot].getSign(ePlayer)
				if szCaption and szCaption == szExistingCaption:
					BugUtil.debug("MapSigns.hideSign() found matching sign (%s) for player %d on plot %s; will remove it" % (szCaption, ePlayer, str(thisKey)))
					if ePlayer == -1:
						engine.removeLandmark(pPlot)
					else:
						engine.removeSign(pPlot, ePlayer)
					return True
				else:
					BugUtil.debug("MapSigns.hideSign() found sign for player %d saying (%s) instead of (%s) on plot %s; will leave alone." % (ePlayer, szExistingCaption, szCaption, str(thisKey)))
			else:
				BugUtil.debug("MapSigns.hideSign() found no sign on plot %s to remove" % (str(thisKey)))
		else:
			BugUtil.debug("MapSigns.hideSign() found no saved signs at all for plot %s" % (str(thisKey)))
		return False

	def removeSign (self, pPlot, ePlayer):
		""" Removes sign for given player at given plot from storage. """
		if self.hasPlotSigns(pPlot):
			thisKey = self.__getKey(pPlot)
			self.plotDict[thisKey].removeSign(ePlayer)
			# If that was the last caption stored, clean up after ourselves
			if self.plotDict[thisKey].isEmpty():
				del self.plotDict[thisKey]
				return True
		return False

	def processSigns (self, bShow = None):
		""" Shows or hides all signs based on boolean argument which defaults to global g_bShowSigns. """
		BugUtil.debug("MapSigns.processSigns() starting. bShow = %s and g_bShowSigns = %s" % (str(bShow), str(g_bShowSigns)))
		updateCurrentSigns()
		if bShow == None:
			bShow = g_bShowSigns
		for pSign in self.plotDict.itervalues():
			pPlot = pSign.getPlot()
			BugUtil.debug("MapSigns.processSigns() Found saved sign data for plot %d, %d ..." % (pPlot.getX(), pPlot.getY()))
			for ePlayer in pSign.getPlayers():
				BugUtil.debug("MapSigns.processSigns() ... and caption for player %d" % (ePlayer))
				if (bShow):
					self.displaySign(pPlot, ePlayer)
				else:
					self.hideSign(pPlot, ePlayer)
		clearCurrentSigns()
		return True

	# Private Methods

	def __getKey(self, pPlot):
		""" Gets keyname used to access this plot object. """
		thisKey = None
		if pPlot and not pPlot.isNone():
			thisKey = (pPlot.getX(), pPlot.getY())
		return thisKey


class PlotSigns:
	""" Sign information for all players for a given plot. """

	def __init__(self, pPlot):
		""" Class initialization. Parameter is Plot Object. """
		if pPlot and not pPlot.isNone():
			self.reset()
			self.iX = pPlot.getX()
			self.iY = pPlot.getY()

	def reset(self):
		""" Resets data for this instance to defaults. """
		self.iX = -1
		self.iY = -1
		self.signDict = {}

	def isEmpty(self):
		""" Check to see if object has any caption data. """
		return (len(self.signDict) == 0)

	def getPlot(self):
		""" Returns plot object. """
		return map.plot(self.iX, self.iY)

	def setPlot(self, pPlot):
		""" Assigns plot object. """
		if pPlot and not pPlot.isNone():
			self.iX = pPlot.getX()
			self.iY = pPlot.getY()

	def getPlayers(self):
		""" Returns a set of player IDs corresponding to stored signs. """
		ePlayerSet = set()
		for ePlayer in self.signDict:
			ePlayerSet.add(ePlayer)
		return ePlayerSet

	def getSign(self, ePlayer):
		""" Returns Caption for a given player on this plot. """
		szCaption = ""
		if ePlayer in self.signDict:
			szCaption = self.signDict[ePlayer] 
		return szCaption

	def setSign(self, ePlayer, szCaption):
		""" Sets Caption for a given player on this plot. """
		if ePlayer in ([-1] + range(gc.getMAX_PLAYERS())):
			self.signDict[ePlayer] = szCaption
		else:
			BugUtil.warn("EventSigns PlotSigns.setSign() was passed an invalid Player ID %s at Plot (%d,%d)" % (str(ePlayer), self.iX, self.iY))

	def removeSign(self, ePlayer):
		""" Removes Caption for a given player on this plot. """
		if ePlayer in self.signDict:
			del self.signDict[ePlayer] 
		else:
			BugUtil.warn("EventSigns PlotSigns.removeSign() failed to find a caption for Player %d at Plot (%d,%d)" % (ePlayer, self.iX, self.iY))

	def __str__ (self):
		""" String representation of class instance. """
		return "PlotSigns { iX = %d, iY = %d, signDict = %s }" % (self.iX, self.iY, str(self.signDict))


class PlotCaptions:
	""" Fake class needed to load games made with first development version. """
	def __init__ (self):
		self.iX = None
		self.iY = None
		self.teamDict = None


class EventSignsEventHandler:
	""" Event Handler for this module. """

	def __init__(self, eventManager):
		BugUtil.debug("EventSigns EventSignsEventHandler.__init__(). Resetting data and initing event manager.")
		initOptions()
		initData()
		## Init event handlers
		eventManager.addEventHandler("GameStart", self.onGameStart)
		eventManager.addEventHandler("OnLoad", self.onLoadGame)
		eventManager.addEventHandler("OnPreSave", self.onPreSave)
		eventManager.addEventHandler("plotRevealed", self.onPlotRevealed)
		eventManager.addEventHandler("BeginActivePlayerTurn", self.onBeginActivePlayerTurn)

	def onGameStart(self, argsList):
		""" Called when a new game is started """
		#BugUtil.debug("EventSignsEventHandler.onGameStart()")
		initOptions()
		initData()

	def onLoadGame(self, argsList):
		""" Called when a game is loaded """
		BugUtil.debug("EventSignsEventHandler.onLoadGame()")
		initOptions()
		data = SdToolKit.sdGetGlobal(SD_MOD_ID, SD_VAR_ID)
		if (data):
			global gSavedSigns
			gSavedSigns = data
			BugUtil.debug("EventSigns Data Loaded:\n %s" % (gSavedSigns))
		else:
			BugUtil.debug("EventSigns has no saved data. Initializing new data.")
			initData()
		# Hey guess what? The map isn't fully loaded yet so we can't update the signs yet. Super.
		global g_bForceUpdate
		g_bForceUpdate = True

	def onPreSave(self, argsList):
		""" Called before a game is actually saved """
		#BugUtil.debug("EventSignsEventHandler.onPreSave()")
#		if (gSavedSigns and (not gSavedSigns.isEmpty())):
#			SdToolKit.sdSetGlobal(SD_MOD_ID, SD_VAR_ID, gSavedSigns)

	def onPlotRevealed(self, argsList):
		""" Called when plot is revealed to team. """
		(pPlot, eTeam) = argsList
		#BugUtil.debug("EventSignsEventHandler.onPlotRevealed(pPlot = %s, eTeam = %s)" % (str(pPlot), str(eTeam)))
		if (g_bShowSigns):
			if (gSavedSigns):
				for ePlayer in range(gc.getMAX_PLAYERS()):
					pPlayer = gc.getPlayer(ePlayer)
					if pPlayer.getTeam() == eTeam:
						gSavedSigns.displaySign(pPlot, ePlayer)

	def onBeginActivePlayerTurn(self, argsList):
		""" Called at start of active player's turn """
		#BugUtil.debug("EventSignsEventHandler.onBeginActivePlayerTurn()")
		global g_bForceUpdate
		if g_bForceUpdate:
			gSavedSigns.processSigns(g_bShowSigns)
			g_bForceUpdate = False


## Random Event Callbacks

# This is the only current event which has a pre-defined callback since it may change the
# yields of more than one plot. So in this function we will essentially duplicate what the 
# generic landmark event processor does where necessary here. Additions marked with "EventSigns" comments.

def applySaltpeter(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	# EventSigns start -- setup
	event = gc.getEventInfo(iEvent)
	iFood = event.getPlotExtraYield(YieldTypes.YIELD_FOOD)
	iProd = event.getPlotExtraYield(YieldTypes.YIELD_PRODUCTION)
	iComm = event.getPlotExtraYield(YieldTypes.YIELD_COMMERCE)
	sEventType = event.getType()
	# EventSigns end

	map = gc.getMap()
	
	player = gc.getPlayer(kTriggeredData.ePlayer)

	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if (plot == None):
		return
	# EventSigns start -- Add landmark for initial plot, if there is still a yield change
	placeLandmark(plot, sEventType, iFood, iProd, iComm, True, -1)
	# EventSigns end
		
	iForest = gc.getInfoTypeForString('FEATURE_FOREST')
	
	listPlots = []
	for i in range(map.numPlots()):
		loopPlot = map.plotByIndex(i)
		if (loopPlot.getOwner() == kTriggeredData.ePlayer and loopPlot.getFeatureType() == iForest and loopPlot.isHills()):
			iDistance = plotDistance(kTriggeredData.iPlotX, kTriggeredData.iPlotY, loopPlot.getX(), loopPlot.getY())
			if iDistance > 0:
				listPlots.append((iDistance, loopPlot))

	listPlots.sort()
	
	iCount = CvRandomEventInterface.getSaltpeterNumExtraPlots()
	for loopPlot in listPlots:
		if iCount == 0:
			break
		iCount -= 1
		gc.getGame().setPlotExtraYield(loopPlot[1].getX(), loopPlot[1].getY(), YieldTypes.YIELD_COMMERCE, 1)
		CyInterface().addMessage(kTriggeredData.ePlayer, false, gc.getEVENT_MESSAGE_TIME(), localText.getText("TXT_KEY_EVENT_SALTPETER_DISCOVERED", ()), "", InterfaceMessageTypes.MESSAGE_TYPE_INFO, None, gc.getInfoTypeForString("COLOR_WHITE"), loopPlot[1].getX(), loopPlot[1].getY(), true, true)
		# EventSigns start -- Add landmark for other plots, if there is still a yield change
		placeLandmark(loopPlot[1], sEventType, iFood, iProd, iComm, True, -1)
		# EventSigns end
