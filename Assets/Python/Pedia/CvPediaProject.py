from CvPythonExtensions import *
import CvUtil

gc = CyGlobalContext()



class CvPediaProject:
	def __init__(self, main):
		self.iProject = -1
		self.top = main

		self.X_INFO_PANE = self.top.X_PEDIA_PAGE
		self.Y_INFO_PANE = self.top.Y_PEDIA_PAGE
		self.W_INFO_PANE = 380 #290
		self.H_INFO_PANE = 120

		self.W_ICON = 100
		self.H_ICON = 100
		self.X_ICON = self.X_INFO_PANE + 10
		self.Y_ICON = self.Y_INFO_PANE + 10
		self.ICON_SIZE = 64

		self.X_INFO_TEXT = self.X_INFO_PANE + 110
		self.Y_INFO_TEXT = self.Y_ICON + 15
		self.W_INFO_TEXT = self.W_INFO_PANE - 70
		self.H_INFO_TEXT = self.H_INFO_PANE - 20

		self.X_REQUIRES = self.X_INFO_PANE + self.W_INFO_PANE + 10
		self.W_REQUIRES = self.top.R_PEDIA_PAGE - self.X_REQUIRES
		self.H_REQUIRES = 110
		self.Y_REQUIRES = self.Y_INFO_PANE + self.H_INFO_PANE - self.H_REQUIRES

		self.X_DETAILS = self.X_INFO_PANE
		self.Y_DETAILS = self.Y_INFO_PANE + self.H_INFO_PANE + 10
		self.W_DETAILS = self.top.R_PEDIA_PAGE - self.X_DETAILS
		self.H_DETAILS = 210

		self.X_HISTORY = self.X_DETAILS
		self.W_HISTORY = self.top.R_PEDIA_PAGE - self.X_HISTORY
		self.Y_HISTORY = self.Y_DETAILS + self.H_DETAILS + 10
		self.H_HISTORY = self.top.B_PEDIA_PAGE - self.Y_HISTORY



	def interfaceScreen(self, iProject):
		self.iProject = iProject
		screen = self.top.getScreen()

		self.placeInfo()
		self.placeRequires()
		self.placeDetails()
		self.placeHistory()


	def placeInfo(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		info = gc.getProjectInfo(self.iProject)

		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_INFO_PANE, self.Y_INFO_PANE, self.W_INFO_PANE, self.H_INFO_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), info.getButton(), self.X_ICON + self.W_ICON / 2 - self.ICON_SIZE / 2, self.Y_ICON + self.H_ICON / 2 - self.ICON_SIZE / 2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.addListBoxGFC(panel, "", self.X_INFO_TEXT, self.Y_INFO_TEXT, self.W_INFO_TEXT, self.H_INFO_TEXT, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panel, False)
		screen.appendListBoxString(panel, u"<font=4b>" + info.getDescription() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
		screen.appendListBoxString(panel, u"<font=3>Project</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		if info.getProductionCost() >= 0:
			if self.top.iActivePlayer == -1:
				iCost = (info.getProductionCost() * gc.getDefineINT('PROJECT_PRODUCTION_PERCENT')) / 100
			else:
				iCost = gc.getActivePlayer().getProjectProductionNeeded(self.iProject)

			szCost = u"Cost: %d%c" % (iCost, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar())
			screen.appendListBoxString(panel, u"<font=3>" + szCost + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)



	def placeRequires(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		info = gc.getProjectInfo(self.iProject)

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_PEDIA_REQUIRES", ()), "", False, True, self.X_REQUIRES, self.Y_REQUIRES, self.W_REQUIRES, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panel, "", "  ")

		iTech = info.getTechPrereq()
		if iTech >= -1:
			screen.attachImageButton(panel, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False)

		iAnyoneProjectPrereq = info.getAnyoneProjectPrereq()
		if iAnyoneProjectPrereq != -1:
			screen.attachImageButton(panel, "", gc.getProjectInfo(iAnyoneProjectPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, iAnyoneProjectPrereq, 1, False)
			
		for iProject in range(gc.getNumProjectInfos()):
			if info.getProjectsNeeded(iProject) > 0:
				screen.attachImageButton(panel, "", gc.getProjectInfo(iProject).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, iProject, 1, False)		

	def placeDetails(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		text = self.top.getNextWidgetName()
		info = gc.getProjectInfo(self.iProject)

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_PEDIA_DETAILS", ()), "", True, False, self.X_DETAILS, self.Y_DETAILS, self.W_DETAILS, self.H_DETAILS, PanelStyles.PANEL_STYLE_BLUE50)

		szText = CyGameTextMgr().getProjectHelp(self.iProject, True, None)[1:]
		screen.addMultilineText(text, szText, self.X_DETAILS + 5, self.Y_DETAILS + 30, self.W_DETAILS - 10, self.H_DETAILS - 35, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def placeHistory(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		text = self.top.getNextWidgetName()
		info = gc.getProjectInfo(self.iProject)

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", True, True, self.X_HISTORY, self.Y_HISTORY, self.W_HISTORY, self.H_HISTORY, PanelStyles.PANEL_STYLE_BLUE50 )

		szText = info.getCivilopedia()
		screen.addMultilineText(text, szText, self.X_HISTORY + 10, self.Y_HISTORY + 30, self.W_HISTORY - 20, self.H_HISTORY - 40, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def handleInput (self, inputClass):
		return 0
