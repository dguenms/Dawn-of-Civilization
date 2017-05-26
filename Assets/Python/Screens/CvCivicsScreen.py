from CvPythonExtensions import *
import CvUtil
import CvScreenEnums
import CvScreensInterface
from Consts import *
import Stability

# Globals
gc = CyGlobalContext()



class CvCivicsScreen:
	'Civics Screen'
	def __init__(self):
		self.W_SCREEN = 1024
		self.H_SCREEN = 680

		self.W_TOP_PANEL = self.W_SCREEN
		self.H_TOP_PANEL = 55
		self.X_TOP_PANEL = 0
		self.Y_TOP_PANEL = -2

		self.W_BOTTOM_PANEL = self.W_SCREEN
		self.H_BOTTOM_PANEL = 55
		self.X_BOTTOM_PANEL = 0
		self.Y_BOTTOM_PANEL = self.H_SCREEN - self.H_BOTTOM_PANEL

		self.X_TITLE = self.X_TOP_PANEL + (self.W_TOP_PANEL / 2)
		self.Y_TITLE = self.Y_TOP_PANEL + 12

		self.X_FLAG = 25
		self.Y_FLAG = 25
		self.W_FLAG = 120
		self.H_FLAG = 450

		self.BUTTON_SMALL = 24
		self.BUTTON_LARGE = 64
		self.LINE = 28
		self.MARGIN = 10

		self.nCategories = 5
		self.nCategoryCivics = 6
		self.nColumns = 2

		self.X_CIVIC_CATEGORY = self.MARGIN
		self.Y_CIVIC_CATEGORY = self.Y_TOP_PANEL + self.H_TOP_PANEL + self.MARGIN
		self.W_CIVIC_CATEGORY = ((self.W_SCREEN - self.X_CIVIC_CATEGORY) / self.nColumns) - self.MARGIN
		self.H_CIVIC_CATEGORY = (self.nCategoryCivics * self.LINE) + self.MARGIN

		self.W_CIVIC_TEXT = self.W_CIVIC_CATEGORY - 250
		self.H_CIVIC_TEXT = self.H_CIVIC_CATEGORY - (self.MARGIN * 2)

		self.X_TURNS = 25
		self.Y_TURNS = self.Y_BOTTOM_PANEL + 20

		self.X_MAINTENANCE = self.W_BOTTOM_PANEL / 2 + 25
		self.Y_MAINTENANCE = self.Y_BOTTOM_PANEL + 20

		self.X_DISSENT = (self.W_BOTTOM_PANEL / 2) + 25
		self.Y_DISSENT = self.Y_BOTTOM_PANEL + 20

		self.X_REVOLUTION = self.W_BOTTOM_PANEL - 150
		self.Y_REVOLUTION = self.Y_BOTTOM_PANEL + 20

		self.X_CANCEL =  self.W_BOTTOM_PANEL - 25
		self.Y_CANCEL = self.Y_BOTTOM_PANEL + 20

		self.X_EXIT = self.W_BOTTOM_PANEL - 25
		self.Y_EXIT = self.Y_BOTTOM_PANEL + 20

		self.iActivePlayer = -1

		self.Categories = []
		self.PlayerCivics = []
		self.SelectedCivics = []
		self.DisplayedCivics = []



	def getScreen(self):
		return CyGInterfaceScreen("CivicsScreen", CvScreenEnums.CIVICS_SCREEN)


	def interfaceScreen (self):
		''
		screen = self.getScreen()
		if screen.isActive():
			return

		self.setActivePlayer(gc.getGame().getActivePlayer())

		del self.Categories[:]
		for iCategory in xrange(gc.getNumCivicOptionInfos()):
			self.Categories.append(iCategory)

		screen.setRenderInterfaceOnly(True)
		screen.setDimensions((screen.getXResolution() / 2) - (self.W_SCREEN / 2), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		screen.addDDSGFC("CivicsBackground", CyArtFileMgr().getInterfaceArtInfo('MAINMENU_SLIDESHOW_LOAD').getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addPanel("CivicsTopPanel", u"", u"", True, False, self.X_TOP_PANEL, self.Y_TOP_PANEL, self.W_TOP_PANEL, self.H_TOP_PANEL, PanelStyles.PANEL_STYLE_TOPBAR)
		screen.addPanel("CivicsBottomPanel", u"", u"", True, False, self.X_BOTTOM_PANEL, self.Y_BOTTOM_PANEL, self.W_BOTTOM_PANEL, self.H_BOTTOM_PANEL, PanelStyles.PANEL_STYLE_BOTTOMBAR)
		screen.setLabel("CivicsTitle", "Background", u"<font=4b>CIVICS</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_TITLE, self.Y_TITLE, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setText("RevolutionButton", "Background", u"<font=4>REVOLUTION</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_REVOLUTION, self.Y_REVOLUTION, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_REVOLUTION, 1, 0)
		screen.setText("CancelButton", "Background", u"<font=4>CANCEL</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_CANCEL, self.Y_CANCEL, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setText("ExitButton", "Background",  u"<font=4>EXIT</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, 1, -1)

		#if self.nCategories % 2 > 0 and self.nColumns % 2 == 0:
		#	screen.addFlagWidgetGFC("LeftFlag", self.X_FLAG, self.Y_FLAG, self.W_FLAG, self.H_FLAG, self.iActivePlayer, WidgetTypes.WIDGET_GENERAL, -1, -1)
		#	screen.addFlagWidgetGFC("RightFlag", self.W_SCREEN - self.X_FLAG - self.W_FLAG, self.Y_FLAG, self.W_FLAG, self.H_FLAG, self.iActivePlayer, WidgetTypes.WIDGET_GENERAL, -1, -1)

		if CyGame().isDebugMode():
			screen.addDropDownBoxGFC("DebugMenu", 22, 12, 300, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
			for iPlayer in xrange(gc.getMAX_PLAYERS()):
				if gc.getPlayer(iPlayer).isAlive():
					screen.addPullDownString("DebugMenu", gc.getPlayer(iPlayer).getName(), iPlayer, iPlayer, False)

		self.placeContents()
		self.updateCivicCosts()
		self.updateRevolution()



	def placeContents(self):
		''
		player = gc.getPlayer(self.iActivePlayer)
		screen = self.getScreen()

		for i in xrange(len(self.Categories)):
			iCategory = self.Categories[i]
			iX, iY = self.getPosition(iCategory)
			iSpacing = 8

			sName = "CivicCategoryPanel" + str(iCategory)
			screen.addDDSGFC(sName, CyArtFileMgr().getInterfaceArtInfo('SCREEN_BG').getPath(), iX, iY, self.W_CIVIC_CATEGORY, self.H_CIVIC_CATEGORY, WidgetTypes.WIDGET_GENERAL, -1, -1)

			sName = "CivicTextPanel" + str(iCategory)
			screen.addPanel(sName, "", "", True, True, iX + self.BUTTON_LARGE + (iSpacing * 2), iY + self.MARGIN, self.W_CIVIC_TEXT, self.H_CIVIC_TEXT, PanelStyles.PANEL_STYLE_IN)

			self.updateCivicOptions(iCategory)
			self.showCivic(iCategory)



	def showCivic(self, iCategory):
		''
		player = gc.getPlayer(self.iActivePlayer)
		screen = self.getScreen()
		iCivic = self.DisplayedCivics[iCategory]
		iX, iY = self.getPosition(iCategory)
		iSpacing = 8

		sName = "CivicIcon" + str(iCategory)
		#print gc.getCivicInfo(iCivic).getText()
		sButton = gc.getCivicInfo(iCivic).getButton()
		#print "Button works"
		screen.setImageButton(sName, sButton, iX + iSpacing , iY + iSpacing, self.BUTTON_LARGE, self.BUTTON_LARGE, WidgetTypes.WIDGET_GENERAL, iCivic, 1)

		sName = "CivicCost" + str(iCategory)
		if gc.getCivicInfo(iCivic).getUpkeep() != -1 and not player.isNoCivicUpkeep(gc.getCivicInfo(iCivic).getCivicOptionType()):
			sUpkeep = gc.getUpkeepInfo(gc.getCivicInfo(iCivic).getUpkeep()).getDescription()
			sUpkeep = sUpkeep.replace("Medium", "Med")
			sUpkeep = sUpkeep.replace(" Upkeep", "")
			sText = u"%c%s" % (gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar(), sUpkeep)
		else:
			sText = u"%cNone" % gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar()

		screen.addMultilineText(sName, sText, iX + iSpacing, iY + self.BUTTON_LARGE + 20, self.BUTTON_LARGE + iSpacing, self.H_CIVIC_CATEGORY - self.BUTTON_LARGE - (iSpacing * 2), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		sName = "CivicText" + str(iCategory)
		sText = u"<font=4b>" + gc.getCivicInfo(iCivic).getDescription() + u"</font>"
		sText += u"\n" + gc.getCivicOptionInfo(gc.getCivicInfo(iCivic).getCivicOptionType()).getDescription()
		sText += u"<font=2>" + CyGameTextMgr().parseCivicInfo(iCivic, False, True, True) + "</font>"
		screen.addMultilineText(sName, sText, iX + self.BUTTON_LARGE + (iSpacing * 2), iY + self.MARGIN, self.W_CIVIC_TEXT, self.H_CIVIC_TEXT, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def selectCivic(self, iCivic):
		''
		screen = self.getScreen()
		player = gc.getPlayer(self.iActivePlayer)
		if not player.canDoCivics(iCivic):
			return 0

		iCategory = gc.getCivicInfo(iCivic).getCivicOptionType()
		iPrevious = self.SelectedCivics[iCategory]

		# Switch the widgets
		self.SelectedCivics[iCategory] = iCivic

		# Unhighlight the previous choice
		self.hoverCivic(iPrevious, False)
		self.getScreen().setState("CivicButton" + str(iPrevious), False)

		# Highlight the new choice
		self.hoverCivic(iCivic, True)
		self.getScreen().setState("CivicButton" + str(iCivic), True)

		self.updateCivicOptions(iCategory)



	def hoverCivic(self, iCivic, bHover):
		''
		iCategory = gc.getCivicInfo(iCivic).getCivicOptionType()

		if bHover:
			if self.DisplayedCivics[iCategory] != iCivic:
				self.DisplayedCivics[iCategory] = iCivic
				return True

		elif self.DisplayedCivics[iCategory] != self.SelectedCivics[iCategory]:
			self.DisplayedCivics[iCategory] = self.SelectedCivics[iCategory]
			return True

		return False



	def updateCivicOptions(self, iCategory):
		''
		player = gc.getPlayer(self.iActivePlayer)
		screen = self.getScreen()
		iX, iY = self.getPosition(iCategory)

		iLine = iY + self.MARGIN
		
		for iCivic in xrange(gc.getNumCivicInfos()):
			if gc.getCivicInfo(iCivic).getCivicOptionType() == iCategory:
				if iCivic % 7 == 0: continue
			
				sName = "CivicButton" + str(iCivic)
				sButton = gc.getCivicInfo(iCivic).getButton()
				xPos = iX + self.W_CIVIC_CATEGORY - self.BUTTON_SMALL - self.MARGIN
				screen.addCheckBoxGFC(sName, sButton, CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), xPos, iLine - 2, self.BUTTON_SMALL, self.BUTTON_SMALL, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL)

				sName = "CivicName" + str(iCivic)
				sText = gc.getCivicInfo(iCivic).getDescription()
				screen.setState("CivicButton" + str(iCivic), self.SelectedCivics[iCategory] == iCivic)
				if self.SelectedCivics[iCategory] == iCivic:
					screen.show("CivicButton" + str(iCivic))
					sText = CyTranslator().changeTextColor(sText, gc.getInfoTypeForString('COLOR_YELLOW'))
				elif player.canDoCivics(iCivic):
					screen.show("CivicButton" + str(iCivic))
				else:
					screen.hide("CivicButton" + str(iCivic))
					sText = CyTranslator().changeTextColor(sText, gc.getInfoTypeForString('COLOR_LIGHT_GREY'))

				screen.setText(sName, "", sText, CvUtil.FONT_RIGHT_JUSTIFY, xPos - self.MARGIN, iLine, 0, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				iLine += self.LINE



	def updateCivicCosts(self):
		''
		screen = self.getScreen()
		player = gc.getPlayer(self.iActivePlayer)

		# Maintenance
		szText = CyTranslator().getText("TXT_KEY_CIVIC_SCREEN_UPKEEP", (player.getCivicUpkeep(self.DisplayedCivics, True), ))
		screen.setLabel("UpkeepText", "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_MAINTENANCE, self.Y_MAINTENANCE, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)


	def updateRevolution(self):
		''
		screen = self.getScreen()
		player = gc.getPlayer(self.iActivePlayer)

		bSelection = False
		for i in self.Categories:
			if self.SelectedCivics[i] != self.PlayerCivics[i]:
				bSelection = True
				break

		sAnarchy = ""
		if player.canRevolution(0):
			iTurns = player.getCivicAnarchyLength(self.DisplayedCivics)
			if iTurns > 0:
				#sAnarchy = CyTranslator().getText('TXT_KEY_CIVIC_SCREEN_ANARCHY_TIMER', (iTurns, ))
				sAnarchy = CyTranslator().getText('TXT_KEY_ANARCHY_TURNS', (iTurns, ))
				
			if bSelection:
				screen.show("RevolutionButton")

		else:
			screen.hide("RevolutionButton")
			iTurns = player.getRevolutionTimer()
			if iTurns > 0:
				#sAnarchy = CyTranslator().getText('TXT_KEY_CIVIC_SCREEN_REVOLUTION_TIMER', (iTurns, ))
				sAnarchy = CyGameTextMgr().setRevolutionHelp(self.iActivePlayer)

		screen.setLabel("AnarchyTurns", "Background", u"<font=3>" + sAnarchy + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_TURNS, self.Y_TURNS, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		if bSelection:
			screen.hide("ExitButton")
			screen.show("CancelButton")
		else:
			screen.hide("RevolutionButton")
			screen.hide("CancelButton")
			screen.show("ExitButton")



	def doRevolution(self):
		'Change civics to player selection'
		player = gc.getPlayer(self.iActivePlayer)
		screen = self.getScreen()

		CyMessageControl().sendUpdateCivics(self.DisplayedCivics)
		screen.hideScreen()



	def getPosition(self, iCategory):
		'Returns top left coordinates of the specified category panel'
		i = self.Categories.index(iCategory)
		#if self.nCategories % 2 > 0 and self.nColumns % 2 == 0:
		#	i += 1

		iX = self.X_CIVIC_CATEGORY + ((i % self.nColumns) * (self.W_CIVIC_CATEGORY + self.MARGIN))
		iY = self.Y_CIVIC_CATEGORY + ((i / self.nColumns) * (self.H_CIVIC_CATEGORY + self.MARGIN))

		#if self.nCategories % 2 > 0 and self.nColumns % 2 == 0:
		#	if i == 1:
		#		iX -= (self.W_CIVIC_CATEGORY + self.MARGIN) / 2

		return iX, iY



	def setActivePlayer(self, iPlayer):
		'Change player in debug mode'
		self.iActivePlayer = iPlayer
		pPlayer = gc.getPlayer(iPlayer)

		self.PlayerCivics = []
		self.SelectedCivics = []
		self.DisplayedCivics = []
		for iCategory in xrange(gc.getNumCivicOptionInfos()):
			self.PlayerCivics.append(pPlayer.getCivics(iCategory))
			self.SelectedCivics.append(pPlayer.getCivics(iCategory))
			self.DisplayedCivics.append(pPlayer.getCivics(iCategory))



	def colorCivicTexts(self, iHoverCivic, bHoverOn):
		screen = self.getScreen()
		player = gc.getPlayer(self.iActivePlayer)
		iHoverCategory = gc.getCivicInfo(iHoverCivic).getCivicOptionType()
		
		for iCivic in range(iNumCivics):
			if iCivic % 7 == 0: continue
		
			iCategory = gc.getCivicInfo(iCivic).getCivicOptionType()
			if iCategory == iHoverCategory:
				continue
			iX, iY = self.getPosition(iCategory)
			xPos = iX + self.W_CIVIC_CATEGORY - self.BUTTON_SMALL - self.MARGIN
			iLine = iY + self.MARGIN + (iCivic % 7 - 1) * self.LINE
			
			sName = "CivicName" + str(iCivic)
			sText = gc.getCivicInfo(iCivic).getDescription()
			iCombovalue = Stability.getCivicStability(self.iActivePlayer, [iHoverCivic, iCivic])
			bGood = iCombovalue > 0
			bBad = iCombovalue < 0
			
			if bHoverOn:
				if bGood:
					if player.canDoCivics(iCivic):
						sText = CyTranslator().changeTextColor(sText, gc.getInfoTypeForString('COLOR_GREEN'))
					else:
						sText = CyTranslator().changeTextColor(sText, gc.getInfoTypeForString('COLOR_PLAYER_MIDDLE_GREEN'))
				elif bBad:
					if player.canDoCivics(iCivic):
						sText = CyTranslator().changeTextColor(sText, gc.getInfoTypeForString('COLOR_RED'))
					else:
						sText = CyTranslator().changeTextColor(sText, gc.getInfoTypeForString('COLOR_PLAYER_CANADA_RED'))
				else:
					if player.canDoCivics(iCivic):
						sText = CyTranslator().changeTextColor(sText, gc.getInfoTypeForString('WHITE'))
					else:
						sText = CyTranslator().changeTextColor(sText, gc.getInfoTypeForString('COLOR_LIGHT_GREY'))
			else:
				if self.SelectedCivics[iCategory] == iCivic:
					screen.show("CivicButton" + str(iCivic))
					sText = CyTranslator().changeTextColor(sText, gc.getInfoTypeForString('COLOR_YELLOW'))
				elif player.canDoCivics(iCivic):
					screen.show("CivicButton" + str(iCivic))
					sText = CyTranslator().changeTextColor(sText, gc.getInfoTypeForString('COLOR_WHITE'))
				else:
					screen.hide("CivicButton" + str(iCivic))
					sText = CyTranslator().changeTextColor(sText, gc.getInfoTypeForString('COLOR_LIGHT_GREY'))
			screen.setText(sName, "", sText, CvUtil.FONT_RIGHT_JUSTIFY, xPos - self.MARGIN, iLine, 0, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)



	def handleInput(self, inputClass):
		'Handles input for this screen'
		if inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED:
			screen = self.getScreen()
			iIndex = screen.getSelectedPullDownID("DebugMenu")
			self.setActivePlayer(screen.getPullDownData("DebugMenu", iIndex))
			self.placeContents()
			self.updateCivicCosts()
			self.updateRevolution()
			return 1

		elif inputClass.getFunctionName().startswith("CivicButton") or inputClass.getFunctionName().startswith("CivicName"):
			if inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED:
				if inputClass.getFlags() & MouseFlags.MOUSE_RBUTTONUP:
					CvScreensInterface.pediaJumpToCivic((inputClass.getID(), ))
				else:
					# Select civic
					self.selectCivic(inputClass.getID())
					self.showCivic(gc.getCivicInfo(inputClass.getID()).getCivicOptionType())
					self.updateCivicCosts()
					self.updateRevolution()

			elif inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON:
				self.colorCivicTexts(inputClass.getID(), True)
				if self.hoverCivic(inputClass.getID(), True):
					# Highlight button
					self.showCivic(gc.getCivicInfo(inputClass.getID()).getCivicOptionType())
					self.updateCivicCosts()
					self.updateRevolution()

			elif inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF:
				self.colorCivicTexts(inputClass.getID(), False)
				if self.hoverCivic(inputClass.getID(), False):
					# Unhighlight button
					self.showCivic(gc.getCivicInfo(inputClass.getID()).getCivicOptionType())
					self.updateCivicCosts()
					self.updateRevolution()

			return 1

		elif inputClass.getFunctionName().startswith("CivicIcon"):
			if inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED:
				CvScreensInterface.pediaJumpToCivic((inputClass.getData1(), ))

		elif inputClass.getFunctionName() == "RevolutionButton":
			self.doRevolution()
			return 1

		elif inputClass.getFunctionName() == "CancelButton":
			for i in xrange(gc.getNumCivicOptionInfos()):
				self.SelectedCivics[i] = self.PlayerCivics[i]
				self.DisplayedCivics[i] = self.PlayerCivics[i]

			self.placeContents()
			self.updateCivicCosts()
			self.updateRevolution()
			return 1

		return 0



	def update(self, fDelta):
		return