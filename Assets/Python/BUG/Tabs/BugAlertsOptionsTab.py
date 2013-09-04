## BugAlertsOptionsTab
##
## Tab for the BUG Civ4lerts and Reminders Options.
##
## Copyright (c) 2007-2008 The BUG Mod.
##
## Author: EmperorFool

import BugOptionsTab

class BugAlertsOptionsTab(BugOptionsTab.BugOptionsTab):
	"BUG NJAGC Options Screen Tab"
	
	def __init__(self, screen):
		BugOptionsTab.BugOptionsTab.__init__(self, "Alerts", "Alerts")

	def create(self, screen):
		tab = self.createTab(screen)
		panel = self.createMainPanel(screen)
		column = self.addOneColumnLayout(screen, panel)
		
		# Civ4lerts
		self.addCheckbox(screen, column, "Civ4lerts__Enabled")
		left, center, right = self.addThreeColumnLayout(screen, column, "Civ4lerts", True)
		
		# Cities
		self.addLabel(screen, left, "Alerts_City", "Cities:")
		leftL, leftR = self.addTwoColumnLayout(screen, left, "Civ4lerts_TableGrowth")		
		self.addCheckbox(screen, leftL, "Civ4lerts__CityPendingGrowth")
		self.addCheckbox(screen, leftR, "Civ4lerts__CityGrowth")		
		self.addCheckbox(screen, leftL, "Civ4lerts__CityPendingHealthiness")
		self.addCheckbox(screen, leftR, "Civ4lerts__CityHealthiness")		
		self.addCheckbox(screen, leftL, "Civ4lerts__CityPendingHappiness")
		self.addCheckbox(screen, leftR, "Civ4lerts__CityHappiness")		
		self.addCheckbox(screen, leftL, "Civ4lerts__CityPendingOccupation")
		self.addCheckbox(screen, leftR, "Civ4lerts__CityOccupation")
		
		self.addCheckbox(screen, left, "MoreCiv4lerts__CityPendingBorderExpansion")
		self.addCheckbox(screen, left, "Civ4lerts__CityCanHurryPop")
		self.addCheckbox(screen, left, "Civ4lerts__CityCanHurryGold")
		self.addCheckbox(screen, left, "MoreCiv4lerts__CityFounded")
		
		# Diplomacy
		self.addLabel(screen, center, "Alerts_Diplomacy", "Diplomacy:")
		self.addCheckbox(screen, center, "Civ4lerts__RefusesToTalk")
		self.addCheckbox(screen, center, "Civ4lerts__WorstEnemy")
		self.addCheckbox(screen, center, "MoreCiv4lerts__OpenBordersTrade")
		self.addCheckbox(screen, center, "MoreCiv4lerts__DefensivePactTrade")
		self.addCheckbox(screen, center, "MoreCiv4lerts__PermanentAllianceTrade")
		self.addCheckbox(screen, center, "MoreCiv4lerts__VassalTrade")
		self.addCheckbox(screen, center, "MoreCiv4lerts__PeaceTrade")
		self.addCheckbox(screen, center, "MoreCiv4lerts__SurrenderTrade")
		
		# Trades
		self.addLabel(screen, right, "Alerts_Trade", "Trading:")
		self.addCheckbox(screen, right, "MoreCiv4lerts__TechTrade")
		self.addCheckbox(screen, right, "MoreCiv4lerts__BonusTrade")
		self.addCheckbox(screen, right, "MoreCiv4lerts__MapTrade")
		
		rightL, rightR = self.addTwoColumnLayout(screen, right, "Alerts_Trade_Column")
		self.addCheckboxIntDropdown(screen, rightL, rightR, "Civ4lerts__GoldTrade", "Civ4lerts__GoldTradeThresh", "LAYOUT_LEFT")
		self.addCheckboxIntDropdown(screen, rightL, rightR, "Civ4lerts__GoldPerTurnTrade", "Civ4lerts__GoldPerTurnTradeThresh", "LAYOUT_LEFT")
		
		# Victories
		self.addLabel(screen, right, "Alerts_Victory", "Victory:")
		
		rightL, rightR = self.addTwoColumnLayout(screen, right, "Alerts_Victory_Column")
		self.addCheckboxFloatDropdown(screen, rightL, rightR, "MoreCiv4lerts__DomPop", "MoreCiv4lerts__DomPopThresh", "LAYOUT_LEFT")
		self.addCheckboxFloatDropdown(screen, rightL, rightR, "MoreCiv4lerts__DomLand", "MoreCiv4lerts__DomLandThresh", "LAYOUT_LEFT")
		
		screen.attachHSeparator(column, column + "Sep")
		
		# Reminders
		left, right = self.addTwoColumnLayout(screen, column, "Main")
		self.addCheckbox(screen, left, "Reminder__Enabled")
		self.addCheckbox(screen, left, "Reminder__Autolog")
		self.addTextDropdown(screen, left, left, "Reminder__DisplayMethod")
