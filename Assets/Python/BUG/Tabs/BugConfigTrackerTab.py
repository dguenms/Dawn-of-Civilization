## BugConfigOptionsTab
##
## Tab for the BUG Config Tracker.
##
## Copyright (c) 2007 The BUG Mod.
##
## Author: EmperorFool

import BugOptionsTab
import BugConfigTracker

class BugConfigTrackerTab(BugOptionsTab.BugOptionsTab):
	"BUG Config Tracker Options Screen Tab"
	
	def __init__(self, screen):
		BugOptionsTab.BugOptionsTab.__init__(self, "System", "System")

	def create(self, screen):
		tab = self.createTab(screen)
		panel = self.createMainPanel(screen)
		column = self.addOneColumnLayout(screen, panel)
		
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
