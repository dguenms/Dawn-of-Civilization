## BugOptionsScreen
##
## Displays the BUG Options Screen and its tabs.
##
## For input handlers see CvOptionsScreenCallbackInterface in Python/EntryPoints.
##
## Notes
##   - Must be initialized when the module loads
##
## Copyright (c) 2007 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *
import CvEventInterface
import BugConfig
import BugCore
import BugErrorOptionsTab
import BugHelp
import BugOptions
import BugUtil


## Globals

g_optionsScreen = None

CoreOpt = BugCore.game.Core
MainOpt = BugCore.game.MainInterface


## Using and Showing

def getOptionsScreen():
	return g_optionsScreen

def showOptionsScreen(argsList=None):
	if not CoreOpt.isOptionsScreenOpened():
		# the first time the Options screen is opened, disable the shortcut reminder
		CoreOpt.setOptionsScreenOpened(True)
		MainOpt.setShowOptionsKeyReminder(False)
	getOptionsScreen().interfaceScreen()


## Event Handlers

def clearAllTranslations(argsList=None):
	g_optionsScreen.clearAllTranslations()


## Control Callback Handlers

def handleBugExitButtonInput(argsList):
	"Exits the screen after saving the options to disk"
	#szName = argsList[0]
	getOptionsScreen().close()
	return 1
		
def handleBugHelpButtonInput(argsList):
	"Opens the BUG help file"
	#szName = argsList[0]
	BugHelp.launch()
	return 1

def handleBugCheckboxClicked(argsList):
	value, name = argsList
	getOptionsScreen().setOptionValue(name, value)
	return 1

def handleBugTextEditChange(argsList):
	value, name = argsList
	getOptionsScreen().setOptionValue(name, value)
	return 1

def handleBugDropdownChange(argsList):
	iIndex, name = argsList
	getOptionsScreen().setOptionIndex(name, iIndex)
	return 1

def handleBugIntDropdownChange(argsList):
	iIndex, name = argsList
	getOptionsScreen().setOptionIndex(name, iIndex)
	return 1

def handleBugFloatDropdownChange(argsList):
	iIndex, name = argsList
	getOptionsScreen().setOptionIndex(name, iIndex)
	return 1

def handleBugColorDropdownChange(argsList):
	iIndex, name = argsList
	getOptionsScreen().setOptionIndex(name, iIndex)
	return 1

def handleBugSliderChanged(argsList):
	value, name = argsList
	getOptionsScreen().setOptionValue(name, value)
	return 1

def handleLanguagesDropdownBoxInput(argsList):
	value, name = argsList
	CvEventInterface.getEventManager().fireEvent("LanguageChanged", value)
	return 1

def handleResolutionDropdownInput(argsList):
	value, name = argsList
	CvEventInterface.getEventManager().fireEvent("ResolutionChanged", value)
	return 1


## Class

class BugOptionsScreen:
	"BUG Mod Options Screen"
	
	def __init__(self):
		self.iScreenHeight = 50
		self.options = BugOptions.getOptions()
		self.tabs = []
		self.reopen = False

	def addTab(self, tab):
		self.tabs.append(tab)
		tab.setOptions(self.options)

	def getTabControl(self):
		return self.pTabControl

	def refreshScreen(self):
		return 1		

	def interfaceScreen(self):
		"Initial creation of the screen"
		title = BugUtil.getPlainText("TXT_KEY_BUG_OPT_TITLE", "BUG Mod Options")
		self.pTabControl = CyGTabCtrl(title, False, False)
		self.pTabControl.setModal(1)
		self.pTabControl.setSize(950, 715)
		self.pTabControl.setControlsExpanding(False)
		self.pTabControl.setColumnLength(self.iScreenHeight)
		
		if self.options.isLoaded():
			self.createTabs()
		else:
			BugErrorOptionsTab.BugErrorOptionsTab(self).create(self.pTabControl)

	def createTabs(self):
		for i, tab in enumerate(self.tabs):
			if not self.reopen or i % 2:
				tab.create(self.pTabControl)

	def clearAllTranslations(self):
		"Clear the translations of all tabs in response to the user choosing a language"
		for tab in self.tabs:
			tab.clearTranslation()
	
	def close(self):
		# TODO: check for error
		self.options.write()
		self.pTabControl.destroy()
		self.pTabControl = None
		if self.reopen:
			self.reopen = False
			self.interfaceScreen()
	
	def setOptionValue(self, name, value):
		option = self.options.getOption(name)
		if (option is not None):
			option.setValue(value)
	
	def setOptionIndex(self, name, index):
		option = self.options.getOption(name)
		if (option is not None):
			option.setIndex(index)


## Configuration

class ScreenConfig:
	
	def __init__(self, id):
		self.id = id
		self.tabs = []
	
	def addTab(self, tab):
		self.tabs.append(tab)

class ScreenHandler(BugConfig.Handler):
	
	TAG = "screen"
	
	def __init__(self):
		BugConfig.Handler.__init__(self, ScreenHandler.TAG, "id", TabHandler.TAG)
		self.addAttribute("id", True)
	
	def handle(self, element, id):
		screen = ScreenConfig(id)
		element.setState("options-screen", screen)
		BugCore.game._addScreen(screen)

class TabHandler(BugConfig.Handler):
	
	TAG = "tab"
	
	def __init__(self):
		BugConfig.Handler.__init__(self, TabHandler.TAG, "id screen module class")
		self.addAttribute("screen")
		self.addAttribute("module", True, True)
		self.addAttribute("class", True, False, None, "module")
		self.addAttribute("id", True, False, None, "module")
	
	def handle(self, element, screenId, module, clazz, id):
		if screenId:
			screen = BugCore.game._getScreen(screenId)
		else:
			screen = element.getState("options-screen")
		if not screen:
			raise BugUtil.ConfigError("Element <%s> %s must be in <screen> or have screen attribute", id, element.tag)
		screen.addTab(id)
		tab = BugUtil.callFunction(module, clazz, g_optionsScreen)
		g_optionsScreen.addTab(tab)


## Initialization

def init():
	global g_optionsScreen
	g_optionsScreen = BugOptionsScreen()

init()
