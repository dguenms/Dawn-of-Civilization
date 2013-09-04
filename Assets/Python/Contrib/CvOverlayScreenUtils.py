## CvOverlayScreenUtils
##
## Controls the Strategy Overlay and provides as-yet unused sign overlay.
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: Del69, EmperorFool

from CvPythonExtensions import *
import CvDotMapOverlayScreen
import BugUtil
import CvUtil

## Constants

STRATEGY_OVERLAY_SCREEN = CvUtil.getNewScreenID()
#GROUP_SIGNTXT = 0

## Globals

gc = CyGlobalContext()
keys = None

overlayScreen = CvDotMapOverlayScreen.CvDotMapOverlayScreen(STRATEGY_OVERLAY_SCREEN)

def showOverlayScreen():
	"""
	Shows the Overlay Screen from CvDotMapOverlayScreen.py
	"""
	overlayScreen.interfaceScreen()

def hideOverlayScreen():
	"""
	Hides the Overlay Screen from CvDotMapOverlayScreen.py
	"""
	overlayScreen.hideScreen()


#def beginAddSignEvent(argsList):
#	"""
#	Starts the popup for the OverlayAddSign Event
#	"""
#	localTxt = CyTranslator()
#	artMgr = CyArtFileMgr()
#	hdrTxt = localTxt.getText("TXT_KEY_STRATOVERLAY_ADDSIGN_TITLE",())
#	bodyTxt = localTxt.getText("TXT_KEY_STRATOVERLAY_ADDSIGN_BODY",())
#	editboxHelp = localTxt.getText("TXT_KEY_STRATOVERLAY_ADDSIGN_EDITBOX_HELP",())
#
#	popup = CyPopup(CvDotMapOverlayScreen.EventOverlayAddSign, EventContextTypes.EVENTCONTEXT_ALL,True)
#	popup.setUserData( argsList )
#	popup.setHeaderString(hdrTxt, CvUtil.FONT_CENTER_JUSTIFY)
#	popup.setBodyString(bodyTxt, CvUtil.FONT_CENTER_JUSTIFY)
#
#	popup.createPythonEditBox("", editboxHelp, GROUP_SIGNTXT)
#	popup.launch(True, PopupStates.POPUPSTATE_IMMEDIATE)

#def applyAddSignEvent(playerID, userData, popupReturn):
#	"""
#	Applys the popup for OverlayAddSign Event
#	"""
#	signText = popupReturn.getEditBoxString(GROUP_SIGNTXT)
#	signText = CvUtil.convertToStr(signText)
#	x,y = userData
#	if gc.getMap().isPlot(x,y):
#		plot = gc.getMap().plot(x,y)
#		player = gc.getGame().getActivePlayer()
#		CyEngine().addSign(plot, player, signText)
#		overlayScreen.saveSign(x, y, signText, player)
#	else:
#		BugUtil.debug("Invalid sign x,y")



class CvOverlayScreenUtils:
	"""
	Derived CvScreenUtils class for custom handling of mod screens
	@cvar HandleInputMap: Maps the screen's enum to its class for passing off input handlers for widget events
	"""

	HandleInputMap = {
		STRATEGY_OVERLAY_SCREEN : overlayScreen, # Pass off input to the overlay screen for it to handle
	}

	def leftMouseDown (self, argsList):
		# return 1 to consume the input
		screenEnum = argsList[0]
		return 0

	def rightMouseDown (self, argsList):
		# return 1 to consume the input
		screenEnum = argsList[0]

		return 0

	def mouseOverPlot(self, argsList):
		# return 1 to consume the input
		# CyInterface().addImmediateMessage("Mouse Over Plot called", "")
		screenEnum = argsList[0]
		# consuming the input would probably prevent the engine from highlighting the square
		if (screenEnum == STRATEGY_OVERLAY_SCREEN):
			overlayScreen.onMouseOverPlot(argsList)
		return 0

	def update(self, argsList):
		"""
		Updates a screen

		@param argsList: First item is the screen's enum value, second one is passed to the screens update method
		@return: 0 to let the event keep going, 1 to consume it
		"""
		screenEnum = argsList[0]
		if (screenEnum == STRATEGY_OVERLAY_SCREEN):
			overlayScreen.update(argsList)
		return 0

	def handleInput (self, argsList):
		"""
		Called when a screen is up
		Gets the active screen from the HandleInputMap Dictionary and calls the handle input on that screen
		"""
		screenEnum, inputClass = argsList
		if (self.HandleInputMap and inputClass and self.HandleInputMap.has_key(screenEnum)):
			# get the screen that is active from the HandleInputMap Dictionary
			screen = self.HandleInputMap.get( inputClass.getPythonFile() )

			# call handle input on that screen
			if ( screen ):
				# return 1 to consume input
				return screen.handleInput(inputClass)
		return 0

	# Screen closing
	def onClose (self, argsList):
		screenEnum = argsList[0]
		return 0

	# Forced screen update
	def forceScreenUpdate (self, argsList):
		screenEnum = argsList[0]
		# place call to update function here
		return 0

	# Forced redraw
	def forceScreenRedraw (self, argsList):
		screenEnum = argsList[0]
		# place call to redraw function here

		return 0

	# Minimap Clicked
	def minimapClicked(self, argsList):
		screenEnum = argsList[0]
		# place call to mini map function here
		return 0

SYMBOL = 0
COMMERCE = 1
BONUS = 2
ICON_TYPES = {
	SYMBOL : "SymbolIcon",
	COMMERCE : "CommerceIcon",
	BONUS : "BonusIcon",
}

g_bEventDefined = False

class OverlaySign:
	"""
	Holds a overlay signs data
	"""
	def __init__(self,x,y,text=""):
		self.plotX = x
		self.plotY = y
		self.text = text
		self.playerType = None
		self.plot = None
		self.WAR_ICON = u"%c" % (gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar() + 25)
		self.PEACE_ICON = u"%c" % (gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar() + 26)
		self.isAdded = False
		global g_bEventDefined
		if not g_bEventDefined:
			g_bEventDefined = True

	def addText(self, text):
		"""
		Adds text to the sign
		"""
		self.text += text

	def addIcon(self,iconIndex,iconType):
		"""
		Adds an icon to the end of the signs string
		"""
		game = gc.getGame()
		for iconIndex in ICON_TYPES:
			if iconType == iconIndex:
				function = "add" + ICON_TYPES[iconType]
				function(iconIndex)

	def addBonusIcon(self, bonusIndex):
		"""
		Adds a bonus icon to the signs string
		"""
		self.text += u"%c" % gc.getBonusInfo(bonusIndex).getChar()

	def addSymbolIcon(self, symbolIndex):
		"""
		Adds a symbol icon to the sign
		"""
		self.text += u"%c" % gc.getGame().getSymbolID(symbolIndex)

	def addCommerceIcon(self, commerceIndex):
		"""
		Adds a Commerce Icon to the sign
		"""
		self.text += u"%c" % gc.getCommerceInfo(commerceIndex).getChar()

	def addSign(self):
		"""
		Puts sign down on game interface
		"""
		if not self.isAdded:
			if gc.getMap().plot(self.plotX,self.plotY):
				self.plot = gc.getMap().plot(self.plotX,self.plotY)
			else:
				BugUtil.debug("Invalid Plot for sign at " + str(self.plotX) + "," + str(self.plotY))
			self.playerType = gc.getGame().getActivePlayer()
			CyEngine().addSign(self.plot,self.playerType,self.text)
			self.isAdded = True
		else:
			BugUtil.debug("Tried to add sign already added to interface")

	def removeSign(self):
		"""
		Removes sign from the interface
		"""
		if self.isAdded:
			CyEngine().removeSign(self.plot, self.playerType)
			self.isAdded = False
		else:
			BugUtil.debug("Tried to remove sign not added to interface")
