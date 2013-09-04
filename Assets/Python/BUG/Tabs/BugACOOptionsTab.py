## BugGeneralOptionsTab
##
## Tab for the BUG Advanced Combat Odds Options.
##
## Copyright (c) 2007-2008 The BUG Mod.
##
## Author: EmperorFool

import BugOptionsTab

class BugACOOptionsTab(BugOptionsTab.BugOptionsTab):
	"BUG ACO Options Screen Tab"
	
	def __init__(self, screen):
		BugOptionsTab.BugOptionsTab.__init__(self, "ACO", "Advanced Combat Odds")

	def create(self, screen):
		tab = self.createTab(screen)
		panel = self.createMainPanel(screen)
		column = self.addOneColumnLayout(screen, panel)
		
		left, right = self.addTwoColumnLayout(screen, column, "Page", True)
		
		#self.addLabel(screen, left, "ACO", "Advanced Combat Odds:")
		self.addCheckbox(screen, left, "ACO__Enabled")
		self.addSpacer(screen, left, "ACO_Tab0")
		
		self.addCheckbox(screen, left, "ACO__ForceOriginalOdds")
		self.addCheckbox(screen, left, "ACO__IgnoreBarbFreeWins")
		
		self.addCheckbox(screen, left, "ACO__SwapViews")
		self.addCheckbox(screen, left, "ACO__MergeShortBars")
		self.addCheckbox(screen, left, "ACO__ShowModifierLabels")
		
		self.addSpacer(screen, left, "ACO_Tab1")
		leftL, leftR =  self.addTwoColumnLayout(screen, left, "ACO1")
		self.addTextDropdown(screen, leftL, leftR, "ACO__ShowBasicInfo")
		self.addTextDropdown(screen, leftL, leftR, "ACO__ShowAttackerInfo")
		self.addTextDropdown(screen, leftL, leftR, "ACO__ShowDefenderInfo")
		
		self.addSpacer(screen, leftL, "ACO_Tab1.1")
		self.addSpacer(screen, leftR, "ACO_Tab1.2")
		self.addTextDropdown(screen, leftL, leftR, "ACO__ShowShiftInstructions")
		
		self.addSpacer(screen, right, "ACO_Tab2")
		rightL, rightR =  self.addTwoColumnLayout(screen, right, "ACO2")
		self.addTextDropdown(screen, rightL, rightR, "ACO__ShowSurvivalOdds")
		self.addTextDropdown(screen, rightL, rightR, "ACO__ShowUnharmedOdds")
		
		self.addSpacer(screen, rightL, "ACO_Tab2.1")
		self.addSpacer(screen, rightR, "ACO_Tab2.2")
		self.addTextDropdown(screen, rightL, rightR, "ACO__ShowAverageHealth")
		self.addTextDropdown(screen, rightL, rightR, "ACO__ShowAttackerHealthBars")
		self.addTextDropdown(screen, rightL, rightR, "ACO__ShowDedenderHealthBars")
		
		self.addSpacer(screen, rightL, "ACO_Tab3.1")
		self.addSpacer(screen, rightR, "ACO_Tab3.2")
		self.addTextDropdown(screen, rightL, rightR, "ACO__ShowUnroundedExperience")
		self.addTextDropdown(screen, rightL, rightR, "ACO__ShowExperienceRange")
		
		self.addSpacer(screen, rightL, "ACO_Tab4.1")
		self.addSpacer(screen, rightR, "ACO_Tab4.2")
		self.addTextDropdown(screen, rightL, rightR, "ACO__ShowDefenseModifiers")
		self.addTextDropdown(screen, rightL, rightR, "ACO__ShowTotalDefenseModifier")
		