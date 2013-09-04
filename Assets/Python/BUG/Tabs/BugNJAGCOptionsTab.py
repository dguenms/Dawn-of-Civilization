## BugNJAGCOptionsTab
##
## Tab for the BUG NJAGC Options.
##
## Copyright (c) 2007-2008 The BUG Mod.
##
## Author: EmperorFool

import BugOptionsTab

class BugNJAGCOptionsTab(BugOptionsTab.BugOptionsTab):
	"BUG NJAGC Options Screen Tab"
	
	def __init__(self, screen):
		BugOptionsTab.BugOptionsTab.__init__(self, "NJAGC", "Clock")

	def create(self, screen):
		tab = self.createTab(screen)
		panel = self.createMainPanel(screen)
		upperPanel = self.addOneColumnLayout(screen, panel)
		
		leftPanel, centerPanel, rightPanel = self.addThreeColumnLayout(screen, upperPanel, "EraColors")
		
		self.addCheckbox(screen, leftPanel, "NJAGC__Enabled")
		self.addCheckbox(screen, leftPanel, "NJAGC__ShowEra")
		self.addCheckbox(screen, leftPanel, "NJAGC__ShowEraColor")
		centerPanelL, centerPanelR = self.addTwoColumnLayout(screen, centerPanel, "ShowEraColor_Column")
		self.addColorDropdown(screen, centerPanelL, centerPanelR, "NJAGC__Color_ERA_ANCIENT", True)
		self.addColorDropdown(screen, centerPanelL, centerPanelR, "NJAGC__Color_ERA_CLASSICAL", True)
		self.addColorDropdown(screen, centerPanelL, centerPanelR, "NJAGC__Color_ERA_MEDIEVAL", True)
		self.addColorDropdown(screen, centerPanelL, centerPanelR, "NJAGC__Color_ERA_RENAISSANCE", True)
		rightPanelL, rightPanelR = self.addTwoColumnLayout(screen, rightPanel, "ShowEraColor_Column")
		self.addColorDropdown(screen, rightPanelL, rightPanelR, "NJAGC__Color_ERA_INDUSTRIAL", True)
		self.addColorDropdown(screen, rightPanelL, rightPanelR, "NJAGC__Color_ERA_MODERN", True)
		self.addColorDropdown(screen, rightPanelL, rightPanelR, "NJAGC__Color_ERA_FUTURE", True)
		self.addSpacer(screen, centerPanel, "Clock_Tab")
		
		screen.attachHSeparator(upperPanel, upperPanel + "Sep")
		leftPanel, rightPanel = self.addTwoColumnLayout(screen, upperPanel, "Views")
		
		self.addCheckbox(screen, leftPanel, "NJAGC__AlternateText")
		self.addIntDropdown(screen, rightPanel, rightPanel, "NJAGC__AltTiming")
		
		self.addLabel(screen, leftPanel, "NJAGC_Regular", "Standard View:")
		self.addCheckbox(screen, leftPanel, "NJAGC__ShowTime")
		self.addCheckbox(screen, leftPanel, "NJAGC__ShowCompletedTurns")
		self.addCheckbox(screen, leftPanel, "NJAGC__ShowTotalTurns")
		self.addCheckbox(screen, leftPanel, "NJAGC__ShowCompletedPercent")
		self.addCheckbox(screen, leftPanel, "NJAGC__ShowDate")
		
		self.addLabel(screen, rightPanel, "NJAGC_Alternate", "Alternate View:")
		self.addCheckbox(screen, rightPanel, "NJAGC__ShowAltTime")
		self.addCheckbox(screen, rightPanel, "NJAGC__ShowAltCompletedTurns")
		self.addCheckbox(screen, rightPanel, "NJAGC__ShowAltTotalTurns")
		self.addCheckbox(screen, rightPanel, "NJAGC__ShowAltCompletedPercent")
		self.addCheckbox(screen, rightPanel, "NJAGC__ShowAltDate")
