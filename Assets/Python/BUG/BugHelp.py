## BugHelp
##
## Opens BUG's help file, "BUG Mod Help.chm", or the online version, for the user's language.
##
## TODO:
##   Move to configuration XML
##   Support multiple help files and shortcuts
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *
import Popup as PyPopup
import BugPath
import BugUtil

def launch(argsList=None):
	"""
	Opens the mod's help file or web page externally if it can be found or displays an error alert.
	
	On Windows this opens the compiled HTML help file (CHM).
	On Mac this opens a browser window to the online help file.
	"""
	if BugPath.isMac():
		sLang = ["ENG", "ENG", "DEU", "ITA", "ENG"]
		url = "http://civ4bug.sourceforge.net/BUGModHelp/%s/index.htm" % sLang[CyGame().getCurrentLanguage()]
		try:
			import webbrowser
			showLaunchMessage()
			webbrowser.open(url, new=1, autoraise=1)
			return True
		except:
			showErrorAlert(BugUtil.getPlainText("TXT_KEY_BUG_HELP_CANNOT_OPEN_BROWSER_TITLE"), 
					BugUtil.getText("TXT_KEY_BUG_HELP_CANNOT_OPEN_BROWSER_BODY", (url,)))		
	else:
		sLang = ["ENG", "FRA", "DEU", "ITA", "ESP"]
		name = "BUG Mod Help-%s.chm" % (sLang[CyGame().getCurrentLanguage()])
		file = BugPath.findInfoFile(name)
		if file:
			import os
			message = BugUtil.getPlainText("TXT_KEY_BUG_HELP_OPENING")
			CyInterface().addImmediateMessage(message, "")
			os.startfile(file)
			return True
		else:
			showErrorAlert(BugUtil.getPlainText("TXT_KEY_BUG_HELP_MISSING_TITLE"), 
					BugUtil.getText("TXT_KEY_BUG_HELP_MISSING_BODY", (name,)))
	return False

def showLaunchMessage():
	"""
	Shows an "opening..." alert message in the event log.
	"""
	BugUtil.alert(BugUtil.getPlainText("TXT_KEY_BUG_HELP_OPENING"))

def showErrorAlert(title, body):
	"""
	Opens a popup window showing the given error message.
	"""
	popup = PyPopup.PyPopup()
	popup.setHeaderString(title)
	popup.setBodyString(body)
	popup.launch()
