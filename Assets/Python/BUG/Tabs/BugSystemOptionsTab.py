## BugSystemOptionsTab
##
## Tab for the BUG System Options (logging, updates, SVN, and system paths).
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

import BugOptionsTab
import CvModName
import BugConfigTracker

class BugSystemOptionsTab(BugOptionsTab.BugOptionsTab):
	"BUG System Options Screen Tab"
	
	def __init__(self, screen):
		BugOptionsTab.BugOptionsTab.__init__(self, "System", "System")

	def create(self, screen):
		tab = self.createTab(screen)
		panel = self.createMainPanel(screen)
		column = self.addOneColumnLayout(screen, panel)

		left, right = self.addTwoColumnLayout(screen, column, "Bottom", False)
		self.addCheckbox(screen, left, "MainInterface__OptionsKey")
		self.addCheckbox(screen, left, "MainInterface__OptionsButton")
		screen.setLayoutFlag(right, "LAYOUT_RIGHT")
		screen.setLayoutFlag(right, "LAYOUT_SIZE_HPREFERREDEXPANDING")
		self.addLabel(screen, right, "Version", 
					  CvModName.getDisplayNameAndVersion() + " (" + CvModName.getCivNameAndVersion() + ")")
		
#		screen.attachHSeparator(column, column + "Sep1")		
#		self.addLabel(screen, column, "Subversion", "Subversion (SVN):")
#		self.addCheckbox(screen, column, "Core__CheckForUpdates")
#		columnL, columnR = self.addTwoColumnLayout(screen, column, "Core")
#		self.addTextEdit(screen, columnL, columnR, "Core__LocalRoot")
#		self.addTextEdit(screen, columnL, columnR, "Core__RepositoryUrl")

		screen.attachHSeparator(column, column + "Sep2")
		self.addLabel(screen, column, "Debug_Logging", "Debugging Output:")
		left, center, right = self.addThreeColumnLayout(screen, column)
		self.addTextDropdown(screen, left, left, "Core__ScreenLogLevel")
		self.addTextDropdown(screen, center, center, "Core__FileLogLevel")
		self.addCheckbox(screen, right, "Core__LogTime")
				
		screen.attachHSeparator(column, column + "Sep3")
		items = BugConfigTracker.combine()
		itemNum = 0
#		first = True
		for item in items:
			itemNum += 1
			subitemNum = 0
#			if not first:
#				screen.attachHSeparator(column, "ItemSep-%d" % itemNum)
#			else:
#				first = False
			self.addLabel(screen, column, item[0], item[0])
			for value in item[1]:
				subitemNum += 1
				self.addLabel(screen, column, "ConfigSubitem-%d-%d" % (itemNum, subitemNum), "  - " + value)
