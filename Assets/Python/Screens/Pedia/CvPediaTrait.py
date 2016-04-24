from CvPythonExtensions import *
import CvUtil

gc = CyGlobalContext()



class CvPediaTrait:
	def __init__(self, main):
		self.iTrait = -1
		self.top = main

		self.X_INFO_PANE = self.top.X_PEDIA_PAGE
		self.Y_INFO_PANE = self.top.Y_PEDIA_PAGE
		self.W_INFO_PANE = (self.top.W_PEDIA_PAGE / 2) - 5
		self.H_INFO_PANE = 120

		self.W_ICON = 100
		self.H_ICON = 100
		self.X_ICON = self.X_INFO_PANE + 10
		self.Y_ICON = self.Y_INFO_PANE + 10
		self.ICON_SIZE = 64

		self.X_INFO_TEXT = self.X_INFO_PANE + 110
		self.Y_INFO_TEXT = self.Y_ICON + 10
		self.W_INFO_TEXT = 200
		self.H_INFO_TEXT = self.H_INFO_PANE - 20

		self.X_EFFECTS = self.X_INFO_PANE
		self.Y_EFFECTS = self.Y_INFO_PANE + self.H_INFO_PANE + 10
		self.W_EFFECTS = self.top.R_PEDIA_PAGE - self.X_EFFECTS
		self.H_EFFECTS = 200

		self.X_LEADERS = self.X_EFFECTS
		self.Y_LEADERS = self.Y_EFFECTS + self.H_EFFECTS + 10
		self.W_LEADERS = self.top.R_PEDIA_PAGE - self.X_LEADERS
		self.H_LEADERS = self.top.B_PEDIA_PAGE - self.Y_LEADERS



	def interfaceScreen(self, iConcept):
		self.iLeader = -1
		self.iConcept = iConcept
		sKey = gc.getNewConceptInfo(iConcept).getType()
		sKey = sKey[sKey.find("TRAIT_"):]
		self.iTrait = gc.getInfoTypeForString(sKey)

		self.placeInfo()
		self.placeLeaders() # must call before placeEffects()
		self.placeEffects()




	def placeInfo(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		TraitInfo = gc.getTraitInfo(self.iTrait)

		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_INFO_PANE, self.Y_INFO_PANE, self.W_INFO_PANE, self.H_INFO_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), "Art/Interface/Buttons/Button_Trait.dds", self.X_ICON + self.W_ICON / 2 - self.ICON_SIZE / 2, self.Y_ICON + self.H_ICON / 2 - self.ICON_SIZE / 2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.addListBoxGFC(panel, "", self.X_INFO_TEXT, self.Y_INFO_TEXT, self.W_INFO_TEXT, self.H_INFO_TEXT, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panel, False)
		screen.appendListBoxString(panel, u"<font=4b>" + TraitInfo.getDescription() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
		screen.appendListBoxString(panel, u"<font=3>Trait</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)



	def placeEffects(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		list = self.top.getNextWidgetName()

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_PEDIA_EFFECTS", ()), "", True, False, self.X_EFFECTS, self.Y_EFFECTS, self.W_EFFECTS, self.H_EFFECTS, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachListBoxGFC(panel, list, "", TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(list, False)

		def append(text):
			screen.appendListBoxString(list, text, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		if self.iLeader != -1:
			LeaderInfo = gc.getLeaderHeadInfo(self.iLeader)
			TraitInfo = gc.getTraitInfo(self.iTrait)
			szHelp = CyGameTextMgr().parseLeaderTraits(self.iLeader, -1, False, True)
			szEffects = u""

			bFirst = True
			bFound = False
			bSkip = True
			for line in szHelp.splitlines():
				if not line.startswith(" "):
					if line.find(">%s<" % LeaderInfo.getDescription()) != -1:
						continue
					elif line.find(">%s<" % TraitInfo.getDescription()) != -1:
						bFound = True
						bSkip = False
					else:
						if bFound:
							break
						bSkip = True
				else:
					if not bSkip:
						if bFirst:
							bFirst = False
						else:
							szEffects += "\n"
						szEffects += line[2:]
			if bFound:
				screen.addMultilineText(list, szEffects, self.X_EFFECTS + 5, self.Y_EFFECTS + 30, self.W_EFFECTS - 10, self.H_EFFECTS - 35, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def placeLeaders(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		list = self.top.getNextWidgetName()

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_CONCEPT_LEADERS", ()), "", False, True, self.X_LEADERS, self.Y_LEADERS, self.W_LEADERS, self.H_LEADERS, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addMultiListControlGFC(list, "", self.X_LEADERS + 5, self.Y_LEADERS + 30, self.W_LEADERS - 10, self.H_LEADERS - 30, 1, self.ICON_SIZE, self.ICON_SIZE, TableStyles.TABLE_STYLE_STANDARD)

		for iLeader in xrange(gc.getNumLeaderHeadInfos()):
			LeaderInfo = gc.getLeaderHeadInfo(iLeader)
			if LeaderInfo.hasTrait(self.iTrait):
				self.iLeader = iLeader
				screen.appendMultiListButton(list, LeaderInfo.getButton(), 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_LEADER, iLeader, 1, False)



	def handleInput (self, inputClass):
		return 0
