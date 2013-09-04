## BugAutologOptionsTab
##
## Tab for the BUG Autolog Options.
##
## Copyright (c) 2007-2008 The BUG Mod.
##
## Author: EmperorFool

import BugOptionsTab

class BugAutologOptionsTab(BugOptionsTab.BugOptionsTab):
	"BUG Autolog Options Screen Tab"
	
	def __init__(self, screen):
		BugOptionsTab.BugOptionsTab.__init__(self, "Autolog", "Logging")

	def create(self, screen):
		tab = self.createTab(screen)
		panel = self.createMainPanel(screen)
		column = self.addOneColumnLayout(screen, panel)
		
		left, right = self.addTwoColumnLayout(screen, column, "Autolog")
		self.addCheckbox(screen, left, "Autolog__Enabled")
		self.addCheckbox(screen, right, "Autolog__Silent")		
		
		# File and Format
		screen.attachHSeparator(column, column + "Sep1")
		left, right = self.addTwoColumnLayout(screen, column, "Options")
		
		self.addIntDropdown(screen, left, left, "Autolog__4000BC")
		self.addCheckbox(screen, left, "Autolog__DefaultFileName")
		self.addCheckbox(screen, left, "Autolog__IBT")
		self.addCheckbox(screen, left, "Autolog__ColorCoding")
		
		rightL, rightR = self.addTwoColumnLayout(screen, right, "File_Column")
		self.addTextEdit(screen, rightL, rightR, "Autolog__FilePath")
		self.addTextEdit(screen, rightL, rightR, "Autolog__FileName")
		self.addTextEdit(screen, rightL, rightR, "Autolog__Prefix")
		self.addTextDropdown(screen, rightL, rightR, "Autolog__Format")
		
		# What to Log
		screen.attachHSeparator(column, column + "Sep2")
		#col1, col1, col2, col3, col4 = self.addMultiColumnLayout(screen, column, 4, "Events")
		left, right = self.addTwoColumnLayout(screen, column, "Events", False)
		
		self.addLabel(screen, left, "Autolog_Builds", "Research and Builds:")
		col1, col2, col3, col4 = self.addMultiColumnLayout(screen, right, 4, "Builds")
		self.addCheckbox(screen, col1, "Autolog__LogTech")
		self.addCheckbox(screen, col2, "Autolog__LogBuildStarted")
		self.addCheckbox(screen, col3, "Autolog__LogBuildCompleted")
		self.addSpacer(screen, left, "Builds1")
		self.addCheckbox(screen, col1, "Autolog__LogProjects")
		self.addCheckbox(screen, col2, "Autolog__LogImprovements")
		self.addCheckbox(screen, col3, "Autolog__LogSliders")
		
		screen.attachHSeparator(right, right + "Sep3a")
		screen.attachHSeparator(left, left + "Sep3b")
		
		self.addLabel(screen, left, "Autolog_Cities", "Cities:")
		col1, col2, col3, col4 = self.addMultiColumnLayout(screen, right, 4, "Cities")
		self.addCheckbox(screen, col1, "Autolog__LogCityFounded")
		self.addCheckbox(screen, col2, "Autolog__LogCityGrowth")
		self.addCheckbox(screen, col3, "Autolog__LogCityBorders")		
		self.addCheckbox(screen, col4, "Autolog__LogCityOwner")
		self.addSpacer(screen, left, "Cities1")
		self.addCheckbox(screen, col1, "Autolog__LogCityRazed")
		self.addCheckbox(screen, col2, "Autolog__LogCityWhipStatus")
		
		screen.attachHSeparator(right, right + "Sep4a")
		screen.attachHSeparator(left, left + "Sep4b")

		self.addLabel(screen, left, "Autolog_Events", "Events:")
		col1, col2, col3, col4 = self.addMultiColumnLayout(screen, right, 4, "Events")
		self.addCheckbox(screen, col1, "Autolog__LogGoodies")
		self.addCheckbox(screen, col2, "Autolog__LogReligion")
		self.addCheckbox(screen, col3, "Autolog__LogCorporation")		
		self.addSpacer(screen, left, "Events1")
		self.addCheckbox(screen, col1, "Autolog__LogGP")
		self.addCheckbox(screen, col2, "Autolog__LogGA")
		
		screen.attachHSeparator(right, right + "Sep5a")
		screen.attachHSeparator(left, left + "Sep5b")
		
		self.addLabel(screen, left, "Autolog_Trade", "Trade and Demands:")
		col1, col2, col3, col4 = self.addMultiColumnLayout(screen, right, 4, "Trade")
		self.addCheckbox(screen, col1, "Autolog__LogTradeOffer")
		self.addCheckbox(screen, col2, "Autolog__LogTributeDemand")
		self.addCheckbox(screen, col3, "Autolog__LogReligionDemand")
		self.addSpacer(screen, left, "Trade1")		
		self.addCheckbox(screen, col1, "Autolog__LogCivicDemand")
		self.addCheckbox(screen, col2, "Autolog__LogWarDemand")
		self.addCheckbox(screen, col3, "Autolog__LogEmbargoDemand")
		
		screen.attachHSeparator(right, right + "Sep6a")
		screen.attachHSeparator(left, left + "Sep6b")
		
		self.addLabel(screen, left, "Autolog_Politics", "Diplomacy:")
		col1, col2, col3, col4, col5 = self.addMultiColumnLayout(screen, right, 5, "Diplomacy")
		self.addCheckbox(screen, col1, "Autolog__LogContact")
		self.addCheckbox(screen, col2, "Autolog__LogAttitude")
		self.addCheckbox(screen, col3, "Autolog__LogWar")
		self.addCheckbox(screen, col4, "Autolog__LogVassals")
		self.addCheckbox(screen, col5, "Autolog__LogCivics")
		#self.addCheckbox(screen, col3, "Autolog__LogTradeAll")
		
		screen.attachHSeparator(right, right + "Sep7a")
		screen.attachHSeparator(left, left + "Sep7b")
		
		self.addLabel(screen, left, "Autolog_Combat", "Combat:")
		col1, col2, col3, col4 = self.addMultiColumnLayout(screen, right, 4, "Combat")
		self.addCheckbox(screen, col1, "Autolog__LogCombat")
		self.addCheckbox(screen, col2, "Autolog__LogPromotions")
		self.addCheckbox(screen, col3, "Autolog__LogPillage")
