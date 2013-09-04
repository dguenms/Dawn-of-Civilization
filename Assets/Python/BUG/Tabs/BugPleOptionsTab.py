## BugPleOptionsTab
##
## Tab for the BUG PLE Options.
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

import BugOptionsTab

class BugPleOptionsTab(BugOptionsTab.BugOptionsTab):
	"Plot List Enhancement Tab"
	
	def __init__(self, screen):
		BugOptionsTab.BugOptionsTab.__init__(self, "PLE", "Plot List")

	def create(self, screen):
		tab = self.createTab(screen)
		panel = self.createMainPanel(screen)
		left, center, right = self.addThreeColumnLayout(screen, panel, panel, True)

		#self.addCheckbox(screen, left, "PLE__Enabled")
		self.addCheckbox(screen, left, "PLE__PLE_Style")

		self.addCheckbox(screen, left, "PLE__Show_Buttons")
		leftL, leftR = self.addTwoColumnLayout(screen, left, "Show_Buttons_Column")
		self.addTextDropdown(screen, leftL, leftR, "PLE__Draw_Method", True, "LAYOUT_LEFT")
		self.addTextDropdown(screen, leftL, leftR, "PLE__Default_View_Mode", True, "LAYOUT_LEFT")
		self.addTextDropdown(screen, leftL, leftR, "PLE__Default_Group_Mode", True, "LAYOUT_LEFT")
		self.addTextDropdown(screen, leftL, leftR, "PLE__Filter_Behavior", True, "LAYOUT_LEFT")

		self.addSpacer(screen, left, "PLE_Indicators", 1)
		self.addLabel(screen, left, "PLE_Indicators")
		self.addCheckbox(screen, left, "PLE__Wounded_Indicator")
		self.addCheckbox(screen, left, "PLE__Lead_By_GG_Indicator")
		self.addCheckbox(screen, left, "PLE__Promotion_Indicator")
		self.addCheckbox(screen, left, "PLE__Upgrade_Indicator")
		self.addCheckbox(screen, left, "PLE__Mission_Info")
		self.addSpacer(screen, left, "PLE_Tab")

		#self.addSpacer(screen, left, "PLE__Spacing")
		#self.addTextEdit(screen, left, left, "PLE__Horizontal_Spacing")
		#self.addTextEdit(screen, left, left, "PLE__Vertical_Spacing")
		
		
		self.addCheckbox(screen, center, "PLE__Health_Bar")
		centerL, centerR = self.addTwoColumnLayout(screen, center, "Health_Bar_Column")
		self.addColorDropdown(screen, centerL, centerR, "PLE__Healthy_Color")
		self.addColorDropdown(screen, centerL, centerR, "PLE__Wounded_Color")
		self.addCheckbox(screen, center, "PLE__Hide_Health_Fighting")
		
		self.addSpacer(screen, center, "PLE__Bars", 1)
		self.addCheckbox(screen, center, "PLE__Move_Bar")
		centerL, centerR = self.addTwoColumnLayout(screen, center, "Move_Bar_Column")
		self.addColorDropdown(screen, centerL, centerR, "PLE__Full_Movement_Color")
		self.addColorDropdown(screen, centerL, centerR, "PLE__Has_Moved_Color")
		self.addColorDropdown(screen, centerL, centerR, "PLE__No_Movement_Color")
		
		
		self.addLabel(screen, right, "PLE_Unit_Info_Tooltip")
		#self.addCheckbox(screen, right, "PLE__Info_Pane")  # EF: Can't get it to work
		#self.addTextEdit(screen, right, right, "PLE__Info_Pane_X")
		#self.addTextEdit(screen, right, right, "PLE__Info_Pane_Y")
		self.addIntDropdown(screen, right, right, "PLE__Info_Pane_Promo_Icon_Offset_Y")
		self.addColorDropdown(screen, right, right, "PLE__Unit_Name_Color")
		
		self.addLabel(screen, right, "PLE_Upgrade_Cost")
		rightL, rightR = self.addTwoColumnLayout(screen, right, "PLE_Upgrade_Cost_Column")
		self.addColorDropdown(screen, rightL, rightR, "PLE__Upgrade_Possible_Color")
		self.addColorDropdown(screen, rightL, rightR, "PLE__Upgrade_Not_Possible_Color")
		
		self.addLabel(screen, right, "PLE_Specialties")
		rightL, rightR = self.addTwoColumnLayout(screen, right, "PLE_Specialties_Column")
		self.addColorDropdown(screen, rightL, rightR, "PLE__Unit_Type_Specialties_Color")
		self.addColorDropdown(screen, rightL, rightR, "PLE__Promotion_Specialties_Color")

		self.addSpacer(screen, right, "PLE_Move_Highlighter", 1)
 		self.addCheckbox(screen, right, "PLE__Move_Highlighter")
