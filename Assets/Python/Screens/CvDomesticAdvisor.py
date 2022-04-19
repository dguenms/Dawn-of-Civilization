## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums

from Stability import calculateAdministration, calculateSeparatism

#	IMPORTANT INFORMATION
#	
#	All widget names MUST be unique when creating screens.  If you create
#	a widget named 'Hello', and then try to create another named 'Hello', it
#	will modify the first hello.
#
#	Also, when attaching widgets, 'Background' is a reserve word meant for
#	the background widget.  Do NOT use 'Background' to name any widget, but
#	when attaching to the background, please use the 'Background' keyword.

#  Thanks to Lee Reeves, AKA Taelis on civfanatics.com
#  Thanks to Solver


# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvDomesticAdvisor:
	"Domestic Advisor Screen"
	def __init__(self):
		self.listSelectedCities = []
		
	# Screen construction function
	def interfaceScreen(self):
	
		player = gc.getPlayer(gc.getGame().getActivePlayer())
		
		# Create a new screen, called DomesticAdvisur, using the file CvDomesticAdvisor.py for input
		screen = CyGInterfaceScreen( "DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR )

		self.nScreenWidth = screen.getXResolution() - 30
		self.nScreenHeight = screen.getYResolution() - 250
		self.nTableWidth = self.nScreenWidth - 35
		self.nTableHeight = self.nScreenHeight - 85
		self.nNormalizedTableWidth = 970

		self.nFirstSpecialistX = 30
		self.nSpecialistY = self.nScreenHeight - 55
		self.nSpecialistWidth = 32
		self.nSpecialistLength = 32
		self.nSpecialistDistance = 100

		# Offset from Specialist Image/Size for the Specialist Plus/Minus buttons
		self.nPlusOffsetX = -4
		self.nMinusOffsetX = 16
		self.nPlusOffsetY = self.nMinusOffsetY = 30
		self.nPlusWidth = self.nPlusHeight = self.nMinusWidth = self.nMinusHeight = 20

		# Offset from Specialist Image for the Specialist Text
		self.nSpecTextOffsetX = 40
		self.nSpecTextOffsetY = 10

		screen.setRenderInterfaceOnly(True)
		screen.setDimensions(15, 100, self.nScreenWidth, self.nScreenHeight)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
	
		# Here we set the background widget and exit button, and we show the screen
		screen.addPanel( "DomesticAdvisorBG", u"", u"", True, False, 0, 0, self.nScreenWidth, self.nScreenHeight, PanelStyles.PANEL_STYLE_MAIN )
		screen.setText("DomesticExit", "Background", localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper(), CvUtil.FONT_RIGHT_JUSTIFY, self.nScreenWidth - 25, self.nScreenHeight - 45, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

		#bCanLiberate = false
		#(loopCity, iter) = player.firstCity(false)
		#while(loopCity):
		#	if loopCity.getLiberationPlayer(false) != -1:
		#		bCanLiberate = true
		#		break
		#	(loopCity, iter) = player.nextCity(iter, false)
		
		#if (bCanLiberate or gc.getPlayer(gc.getGame().getActivePlayer()).canSplitEmpire()):
		screen.setImageButton( "DomesticSplit", "", self.nScreenWidth - 110, self.nScreenHeight - 45, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_FREE_COLONY).getActionInfoIndex(), -1 )
		screen.setStyle( "DomesticSplit", "Button_HUDAdvisorVictory_Style" )
	
		# Erase the flag?
		CyInterface().setDirty(InterfaceDirtyBits.MiscButtons_DIRTY_BIT, True)

		# Draw the city list...
		self.drawContents( )
		
	# headers...
	def drawHeaders( self ):

		# Get the screen and the player
		screen = CyGInterfaceScreen( "DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR )
		
		# Zoom to City
		screen.setTableColumnHeader( "CityListBackground", 0, "", (30 * self.nTableWidth) / self.nNormalizedTableWidth )
		
		# Name Column
		screen.setTableColumnHeader( "CityListBackground", 1, "<font=2>" + localText.getText("TXT_KEY_DOMESTIC_ADVISOR_NAME", ()) + "</font>", (221 * self.nTableWidth) / self.nNormalizedTableWidth )
		
		# Population Column
		screen.setTableColumnHeader( "CityListBackground", 2, "<font=2>" + localText.getText("TXT_KEY_POPULATION", ()) + "</font>", (40 * self.nTableWidth) / self.nNormalizedTableWidth )
		
		# Happiness Column
		screen.setTableColumnHeader( "CityListBackground", 3, "<font=2>" + (u"%c" % CyGame().getSymbolID(FontSymbols.HAPPY_CHAR)) + "</font>", (40 * self.nTableWidth) / self.nNormalizedTableWidth )
		
		# Health Column
		screen.setTableColumnHeader( "CityListBackground", 4, "<font=2>" + (u"%c" % CyGame().getSymbolID(FontSymbols.HEALTHY_CHAR)) + "</font>", (40 * self.nTableWidth) / self.nNormalizedTableWidth )
		
		# Food Column
		screen.setTableColumnHeader( "CityListBackground", 5, "<font=2>" + (u"%c" % gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar()) + "</font>", (40 * self.nTableWidth) / self.nNormalizedTableWidth )
		
		# Production Column
		screen.setTableColumnHeader( "CityListBackground", 6, "<font=2>" + (u"%c" % gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar()) + "</font>", (40 * self.nTableWidth) / self.nNormalizedTableWidth )
		
		# Gold Column
		screen.setTableColumnHeader( "CityListBackground", 7, "<font=2>" + (u"%c" % gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar()) + "</font>", (40 * self.nTableWidth) / self.nNormalizedTableWidth )
		
		# Research Column
		szText = u"%c" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_RESEARCH).getChar())
		screen.setTableColumnHeader( "CityListBackground", 8, "<font=2>" + szText, (40 * self.nTableWidth) / self.nNormalizedTableWidth )
		
		# Espionage Column
		szText = u"%c" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_ESPIONAGE).getChar())
		screen.setTableColumnHeader( "CityListBackground", 9, "<font=2>" + szText, (40 * self.nTableWidth) / self.nNormalizedTableWidth )
		
		# Culture Column
		screen.setTableColumnHeader( "CityListBackground", 10, "<font=2>" + (u"%c" % gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar()) + "</font>", (70 * self.nTableWidth) / self.nNormalizedTableWidth )
				
		# Trade Column
		screen.setTableColumnHeader( "CityListBackground", 11, "<font=2>" + (u"%c" % CyGame().getSymbolID(FontSymbols.TRADE_CHAR)) + "</font>", (35 * self.nTableWidth) / self.nNormalizedTableWidth )
				
		# Maintenance Column
		screen.setTableColumnHeader( "CityListBackground", 12, "<font=2>" + (u"%c" % CyGame().getSymbolID(FontSymbols.BAD_GOLD_CHAR)) + "</font>", (40 * self.nTableWidth) / self.nNormalizedTableWidth )
		
		# Great Person Column
		screen.setTableColumnHeader( "CityListBackground", 13, "<font=2>" + (u"%c" % CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR)) + "</font>", (70 * self.nTableWidth) / self.nNormalizedTableWidth )
				
		# Garrison Column
		screen.setTableColumnHeader( "CityListBackground", 14, "<font=2>" + (u"%c" % CyGame().getSymbolID(FontSymbols.DEFENSE_CHAR)) + "</font>", (35 * self.nTableWidth) / self.nNormalizedTableWidth )
		
		# Expansion Column
		screen.setTableColumnHeader( "CityListBackground", 15, "<font=2>" + (u"%c" % CyGame().getSymbolID(FontSymbols.SCALES_CHAR)) + "</font>", (35 * self.nTableWidth) / self.nNormalizedTableWidth )
		
		# Production Column
		screen.setTableColumnHeader( "CityListBackground", 16, "<font=2>" + localText.getText("TXT_KEY_DOMESTIC_ADVISOR_PRODUCING", ()) + "</font>", (132 * self.nTableWidth) / self.nNormalizedTableWidth )	

		# Liberate Column
		screen.setTableColumnHeader( "CityListBackground", 17, "", (25 * self.nTableWidth) / self.nNormalizedTableWidth )

	# Function to draw the contents of the cityList passed in
	def drawContents (self):
	
		# Get the screen and the player
		screen = CyGInterfaceScreen( "DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR )
		player = gc.getPlayer(CyGame().getActivePlayer())
		
		screen.moveToFront( "Background" )
		
		# Build the table	
		screen.addTableControlGFC( "CityListBackground", 19, 18, 21, self.nTableWidth, self.nTableHeight, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
		screen.enableSelect( "CityListBackground", True )
		screen.enableSort( "CityListBackground" )
		screen.setStyle("CityListBackground", "Table_StandardCiv_Style")

		# Loop through the cities
		i = 0
		(pLoopCity, iter) = player.firstCity(false)
		while(pLoopCity):
			screen.appendTableRow( "CityListBackground" )
			if (pLoopCity.getName() in self.listSelectedCities):
				screen.selectRow( "CityListBackground", i, True )
			self.updateTable(pLoopCity, i)
			i += 1
			(pLoopCity, iter) = player.nextCity(iter, false)
		
		self.drawHeaders()
		
		self.drawSpecialists()
		
		screen.moveToBack( "DomesticAdvisorBG" )
		
		self.updateAppropriateCitySelection()
		
		CyInterface().setDirty(InterfaceDirtyBits.Domestic_Advisor_DIRTY_BIT, true)

	def updateTable(self, pLoopCity, i):

		screen = CyGInterfaceScreen( "DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR )

		screen.setTableText( "CityListBackground", 0, i, "", ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CITYSELECTION").getPath(), WidgetTypes.WIDGET_ZOOM_CITY, pLoopCity.getOwner(), pLoopCity.getID(), CvUtil.FONT_LEFT_JUSTIFY);

		szName = pLoopCity.getName()
		if pLoopCity.isCapital():
			szName += (u"%c" % CyGame().getSymbolID(FontSymbols.STAR_CHAR))
		elif pLoopCity.isGovernmentCenter():
			szName += (u"%c" % CyGame().getSymbolID(FontSymbols.SILVER_STAR_CHAR))
		
		for iReligion in range(gc.getNumReligionInfos()):
			if pLoopCity.isHasReligion(iReligion):
				if pLoopCity.isHolyCityByType(iReligion):
					szName += (u"%c" % gc.getReligionInfo(iReligion).getHolyCityChar())
				else:
					szName += (u"%c" % gc.getReligionInfo(iReligion).getChar())
						
		for iCorporation in range(gc.getNumCorporationInfos()):
			if pLoopCity.isHeadquartersByType(iCorporation):
				szName += (u"%c" % gc.getCorporationInfo(iCorporation).getHeadquarterChar())
			elif pLoopCity.isActiveCorporation(iCorporation):
				szName += (u"%c" % gc.getCorporationInfo(iCorporation).getChar())
					
		# City name...
		screen.setTableText( "CityListBackground", 1, i, szName, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		
		# Population
		screen.setTableInt( "CityListBackground", 2, i, unicode(pLoopCity.getPopulation()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		# Happiness...
		iNetHappy = pLoopCity.happyLevel() - pLoopCity.unhappyLevel(0)
		szText = unicode(iNetHappy)
		if iNetHappy > 0:
			szText = localText.getText("TXT_KEY_COLOR_POSITIVE", ()) + szText + localText.getText("TXT_KEY_COLOR_REVERT", ())
		elif iNetHappy < 0:
			szText = localText.getText("TXT_KEY_COLOR_NEGATIVE", ()) + szText + localText.getText("TXT_KEY_COLOR_REVERT", ())
		screen.setTableInt( "CityListBackground", 3, i, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		# Health...
		iNetHealth = pLoopCity.goodHealth() - pLoopCity.badHealth(0)
		szText = unicode(iNetHealth)
		if iNetHealth > 0:
			szText = localText.getText("TXT_KEY_COLOR_POSITIVE", ()) + szText + localText.getText("TXT_KEY_COLOR_REVERT", ())
		elif iNetHealth < 0:
			szText = localText.getText("TXT_KEY_COLOR_NEGATIVE", ()) + szText + localText.getText("TXT_KEY_COLOR_REVERT", ())
		screen.setTableInt( "CityListBackground", 4, i, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		# Food status...
		iNetFood = pLoopCity.foodDifference(true)
		szText = unicode(iNetFood)
		if iNetFood > 0:
			szText = localText.getText("TXT_KEY_COLOR_POSITIVE", ()) + szText + localText.getText("TXT_KEY_COLOR_REVERT", ())
		elif iNetFood < 0:
			szText = localText.getText("TXT_KEY_COLOR_NEGATIVE", ()) + szText + localText.getText("TXT_KEY_COLOR_REVERT", ())
		screen.setTableInt( "CityListBackground", 5, i, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		
		# Production status...
		screen.setTableInt( "CityListBackground", 6, i, unicode(pLoopCity.getYieldRate(YieldTypes.YIELD_PRODUCTION)), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		# Gold status...
		screen.setTableInt( "CityListBackground", 7, i, unicode(pLoopCity.getCommerceRate(CommerceTypes.COMMERCE_GOLD)), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		# Science rate...
		screen.setTableInt( "CityListBackground", 8, i, unicode(pLoopCity.getCommerceRate(CommerceTypes.COMMERCE_RESEARCH)), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		# Espionage rate...
		screen.setTableInt( "CityListBackground", 9, i, unicode(pLoopCity.getCommerceRate(CommerceTypes.COMMERCE_ESPIONAGE)), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		# Culture status...
		szCulture = unicode(pLoopCity.getCommerceRate(CommerceTypes.COMMERCE_CULTURE))
		iCultureTimes100 = pLoopCity.getCultureTimes100(CyGame().getActivePlayer())
		iCultureRateTimes100 = pLoopCity.getCommerceRateTimes100(CommerceTypes.COMMERCE_CULTURE)
		if iCultureRateTimes100 > 0:
			iCultureLeftTimes100 = 100 * pLoopCity.getCultureThreshold() - iCultureTimes100
			if iCultureLeftTimes100 > 0:
				szCulture += u" (" + unicode((iCultureLeftTimes100  + iCultureRateTimes100 - 1) / iCultureRateTimes100) + u")"

		screen.setTableInt( "CityListBackground", 10, i, szCulture, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		# Trade
		screen.setTableInt( "CityListBackground", 11, i, unicode(pLoopCity.getTradeYield(YieldTypes.YIELD_COMMERCE)), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		# Maintenance...
		screen.setTableInt( "CityListBackground", 12, i, unicode(pLoopCity.getMaintenance()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		# Great Person
		iGreatPersonRate = pLoopCity.getGreatPeopleRate()
		szGreatPerson = unicode(iGreatPersonRate)
		if iGreatPersonRate > 0:
			iGPPLeft = gc.getPlayer(gc.getGame().getActivePlayer()).greatPeopleThreshold(false) - pLoopCity.getGreatPeopleProgress()
			if iGPPLeft > 0:
				iTurnsLeft = iGPPLeft / pLoopCity.getGreatPeopleRate()
				if iTurnsLeft * pLoopCity.getGreatPeopleRate() <  iGPPLeft:
					iTurnsLeft += 1
				szGreatPerson += u" (" + unicode(iTurnsLeft) + u")"
		
		screen.setTableInt( "CityListBackground", 13, i, szGreatPerson, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		
		# Garrison
		screen.setTableInt( "CityListBackground", 14, i, unicode(pLoopCity.plot().getNumDefenders(pLoopCity.getOwner())), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		# Expansion
		screen.setTableInt( "CityListBackground", 15, i, unicode(pLoopCity.isOwnerCore() and calculateAdministration(pLoopCity) or -calculateSeparatism(pLoopCity)), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		# Producing	
		screen.setTableText( "CityListBackground", 16, i, pLoopCity.getProductionName() + " (" + str(pLoopCity.getGeneralProductionTurnsLeft()) + ")", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		# Liberation
		if pLoopCity.getLiberationPlayer(false) != -1:			
			screen.setTableText( "CityListBackground", 17, i, "<font=2>" + (u"%c" % CyGame().getSymbolID(FontSymbols.OCCUPATION_CHAR)) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		
		
	# Draw the specialist and their increase and decrease buttons
	def drawSpecialists(self):
		screen = CyGInterfaceScreen( "DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR )

		for i in range( gc.getNumSpecialistInfos() ):
			if (gc.getSpecialistInfo(i).isVisible()):			
				szName = "SpecialistImage" + str(i)
				screen.setImageButton( szName, gc.getSpecialistInfo(i).getTexture(), self.nFirstSpecialistX + (self.nSpecialistDistance * i), self.nSpecialistY, self.nSpecialistWidth, self.nSpecialistLength, WidgetTypes.WIDGET_CITIZEN, i, -1 )
				screen.hide(szName)

				szName = "SpecialistPlus" + str(i)
				screen.setButtonGFC( szName, u"", "", self.nFirstSpecialistX + (self.nSpecialistDistance * i) + self.nPlusOffsetX, self.nSpecialistY + self.nPlusOffsetY, self.nPlusWidth, self.nPlusHeight, WidgetTypes.WIDGET_CHANGE_SPECIALIST, i, 1, ButtonStyles.BUTTON_STYLE_CITY_PLUS )
				screen.hide(szName)

				szName = "SpecialistMinus" + str(i)
				screen.setButtonGFC( szName, u"", "", self.nFirstSpecialistX + (self.nSpecialistDistance * i) + self.nMinusOffsetX, self.nSpecialistY + self.nMinusOffsetY, self.nMinusWidth, self.nMinusHeight, WidgetTypes.WIDGET_CHANGE_SPECIALIST, i, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS )
				screen.hide(szName)

				szName = "SpecialistText" + str(i)
				screen.setLabel(szName, "Background", "", CvUtil.FONT_LEFT_JUSTIFY, self.nFirstSpecialistX + (self.nSpecialistDistance * i) + self.nSpecTextOffsetX, self.nSpecialistY + self.nSpecTextOffsetY, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.hide(szName)

	def hideSpecialists(self):
		screen = CyGInterfaceScreen( "DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR )
		for i in range( gc.getNumSpecialistInfos() ):
			if (gc.getSpecialistInfo(i).isVisible()):			
				screen.hide("SpecialistImage" + str(i))
				screen.hide("SpecialistPlus" + str(i))
				screen.hide("SpecialistMinus" + str(i))
				screen.hide("SpecialistText" + str(i))
				
	def updateSpecialists(self):
		""" Function which shows the specialists."""
		screen = CyGInterfaceScreen( "DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR )

		if (CyInterface().isOneCitySelected()):
		
			city = CyInterface().getHeadSelectedCity()
			nPopulation = city.getPopulation()
			nFreeSpecial = city.totalFreeSpecialists()

			for i in range( gc.getNumSpecialistInfos() ):
				if (gc.getSpecialistInfo(i).isVisible()):	
					szName = "SpecialistImage" + str(i)
					screen.show(szName)
					
					szName = "SpecialistText" + str(i)
					screen.setLabel(szName, "Background", str (city.getSpecialistCount(i)) + "/" + str(city.getMaxSpecialistCount(i)), CvUtil.FONT_LEFT_JUSTIFY, self.nFirstSpecialistX + (self.nSpecialistDistance * i) + self.nSpecTextOffsetX, self.nSpecialistY + self.nSpecTextOffsetY, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
					screen.show(szName)

					# If the specialist is valid and we can increase it
					szName = "SpecialistPlus" + str(i)
					if (city.isSpecialistValid(i, 1) and (city.getForceSpecialistCount(i) < (nPopulation + nFreeSpecial))):
						screen.show(szName)
					else:
						screen.hide(szName)

					# if we HAVE specialists already and they're not forced.
					szName = "SpecialistMinus" + str(i)
					if (city.getSpecialistCount(i) > 0 or city.getForceSpecialistCount(i) > 0):
						screen.show(szName)
					else:
						screen.hide(szName)
		else:
			self.hideSpecialists()
				
	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		' Calls function mapped in DomesticAdvisorInputMap'
		# only get from the map if it has the key
		
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED ):
			if (inputClass.getMouseX() == 0):
				screen = CyGInterfaceScreen( "DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR )
				screen.hideScreen()
				
				CyInterface().selectCity(gc.getPlayer(inputClass.getData1()).getCity(inputClass.getData2()), true);
				
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
				popupInfo.setText(u"showDomesticAdvisor")
				popupInfo.addPopup(inputClass.getData1())		
			else:
				self.updateAppropriateCitySelection()
				self.updateSpecialists()
		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (inputClass.getFunctionName() == "DomesticSplit"):
				screen = CyGInterfaceScreen( "DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR )
				screen.hideScreen()
			
		return 0
	
	def updateAppropriateCitySelection(self):
		nCities = gc.getPlayer(gc.getGame().getActivePlayer()).getNumCities()
		screen = CyGInterfaceScreen( "DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR )
		screen.updateAppropriateCitySelection( "CityListBackground", nCities, 1 )
		self.listSelectedCities = []
		for i in range(nCities):
			if screen.isRowSelected("CityListBackground", i):
				self.listSelectedCities.append(screen.getTableText("CityListBackground", 2, i))
								
	def update(self, fDelta):
		if (CyInterface().isDirty(InterfaceDirtyBits.Domestic_Advisor_DIRTY_BIT) == True):
			CyInterface().setDirty(InterfaceDirtyBits.Domestic_Advisor_DIRTY_BIT, False)
			
			screen = CyGInterfaceScreen( "DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR )
			player = gc.getPlayer(CyGame().getActivePlayer())

			i = 0
			(pLoopCity, iter) = player.firstCity(false)
			while(pLoopCity):
				self.updateTable(pLoopCity, i)
				i += 1
				(pLoopCity, iter) = player.nextCity(iter, false)
			
			self.updateSpecialists()
		
		return