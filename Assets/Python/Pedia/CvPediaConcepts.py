from CvPythonExtensions import *
import CvUtil
import CvScreenEnums

gc = CyGlobalContext()



class CvPediaConcepts:
	def __init__(self, main):
		self.top = main

		self.X_TEXT = self.top.X_PEDIA_PAGE
		self.Y_TEXT = self.top.Y_PEDIA_PAGE
		self.H_TEXT = self.top.H_PEDIA_PAGE
		self.W_TEXT = self.top.W_PEDIA_PAGE



	def interfaceScreen(self, iEntry):
		self.placeText(iEntry)



	def placeText(self, iEntry):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		text = self.top.getNextWidgetName()


		if self.top.iCategory == CvScreenEnums.PEDIA_CONCEPTS:
			szText = "<font=2>" + gc.getConceptInfo(iEntry).getCivilopedia() + "</font>"
		else:
			szText = gc.getNewConceptInfo(iEntry).getCivilopedia()

		screen.addPanel(panel, "", "", True, True, self.X_TEXT, self.Y_TEXT, self.W_TEXT, self.H_TEXT, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addMultilineText(text, szText, self.X_TEXT + 10, self.Y_TEXT + 10, self.W_TEXT - 10, self.H_TEXT - 20, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def handleInput(self, inputClass):
		return 0
