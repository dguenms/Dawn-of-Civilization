## BugScoreOptionsTab
##
## Tab for the BUG Scoreboard Options.
##
## Copyright (c) 2007-2008 The BUG Mod.
##
## Author: EmperorFool

import BugOptionsTab

class BugScoreOptionsTab(BugOptionsTab.BugOptionsTab):
	"BUG Scores Options Screen Tab"
	
	def __init__(self, screen):
		BugOptionsTab.BugOptionsTab.__init__(self, "Scores", "Scoreboard")

	def create(self, screen):
		tab = self.createTab(screen)
		panel = self.createMainPanel(screen)
		column = self.addOneColumnLayout(screen, panel)
		
		left, right = self.addTwoColumnLayout(screen, column, "Alerts", True)
		self.addLabel(screen, left, "Scores_General", "General:")
		self.addTextDropdown(screen, left, left, "Scores__DisplayName")
		self.addCheckbox(screen, left, "Scores__UsePlayerName")
		self.addCheckbox(screen, left, "Scores__ShowMinor")
		
		self.addLabel(screen, left, "Scores_Dead_Civs", "Dead Civilizations:")
		self.addCheckbox(screen, left, "Scores__ShowDead")
		self.addCheckbox(screen, left, "Scores__TagDead")
		self.addCheckbox(screen, left, "Scores__GreyDead")
		
		self.addLabel(screen, right, "Scores_New_Columns", "Additional Columns:")
		col1L, col1R, col2, col3 = self.addMultiColumnLayout(screen, right, 4, "Scores_Power_Column")
		self.addCheckboxTextDropdown(screen, col1L, col1R, "Scores__Power", "Scores__PowerFormula", "LAYOUT_LEFT")
		self.addIntDropdown(screen, col1L, col1R, "Scores__PowerDecimals", True, "LAYOUT_LEFT")
		self.addColorDropdown(screen, col1L, col1R, "Scores__PowerColor", True, "LAYOUT_LEFT")
		self.addFloatDropdown(screen, col1L, col1R, "Scores__PowerHighRatio", True, "LAYOUT_LEFT")
		self.addColorDropdown(screen, col1L, col1R, "Scores__PowerHighColor", True, "LAYOUT_LEFT")
		self.addFloatDropdown(screen, col1L, col1R, "Scores__PowerLowRatio", True, "LAYOUT_LEFT")
		self.addColorDropdown(screen, col1L, col1R, "Scores__PowerLowColor", True, "LAYOUT_LEFT")
		
		self.addSpacer(screen, col2, "Scores_New_Columns", 3)
		
		self.addCheckbox(screen, col3, "Scores__Delta")
		self.addCheckbox(screen, col3, "Scores__DeltaIncludeCurrent")
		self.addLabel(screen, col3, "Scores_Icons", "Icons:")
		self.addCheckbox(screen, col3, "Scores__Attitude")
		self.addCheckbox(screen, col3, "Scores__WorstEnemy")
		self.addCheckbox(screen, col3, "Scores__WHEOOH")
		self.addCheckbox(screen, col3, "Scores__Cities")
		
		screen.attachHSeparator(column, column + "Sep")
		
		left, space, center, right = self.addMultiColumnLayout(screen, column, 4, "Advanced_Scores_Column")
		self.addLabel(screen, left, "Scores_Grid", "Advanced Layout:")
		self.addCheckbox(screen, left, "Scores__AlignIcons")
		self.addCheckbox(screen, left, "Scores__GroupVassals")
		self.addCheckbox(screen, left, "Scores__LeftAlignName")
		self.addCheckboxIntDropdown(screen, left, left, "Scores__ResearchIcons", "Scores__ResearchIconSize")
		
		self.addSpacer(screen, space, "Scores_Grid", 3)
		
		self.addSpacer(screen, center, "Scoreboard_Tab")
		#self.addLabel(screen, center, "Scores_Order", "Column Order:")		
		self.addTextEdit(screen, center, center, "Scores__DisplayOrder")
		centerL, centerR = self.addTwoColumnLayout(screen, center, "Scores")
		self.addIntDropdown(screen, centerL, centerR, "Scores__DefaultSpacing", True, "LAYOUT_LEFT")
		self.addIntDropdown(screen, centerL, centerR, "Scores__MaxPlayers", True, "LAYOUT_LEFT")
		self.addIntDropdown(screen, centerL, centerR, "Scores__LineHeight", True, "LAYOUT_LEFT")
