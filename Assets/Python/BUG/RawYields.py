## RawYields
##
## Calculates the raw yields of food, production and commerce for a city
## and displays them in the trade table when enabled.
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *
import CvUtil
import BugUtil
import TradeUtil

gc = CyGlobalContext()

# Types
NUM_TYPES = 11
(
	WORKED_TILES,
	CITY_TILES,
	OWNED_TILES,
	ALL_TILES,
	
	DOMESTIC_TRADE,
	FOREIGN_TRADE, # excludes overseas trade
	
	BUILDINGS,
	CORPORATIONS,
	SPECIALISTS,
	
	# Hold the percents, not the actual yield values
	BASE_MODIFIER,
	PRODUCTION_MODIFIER,
) = range(NUM_TYPES)

# Leave these for later when we have icons for each
#DOMAIN_MODIFIER
#MILITARY_MODIFIER
#TRAIT_MODIFIER
#CIVIC_MODIFIER
#RELIGION_MODIFIER
#BONUS_MODIFIER
#WONDER_MODIFIER
#...

# Labels
LABEL_KEYS = ("TXT_KEY_CONCEPT_WORKED_TILES",
			  "TXT_KEY_CONCEPT_CITY_TILES",
			  "TXT_KEY_CONCEPT_OWNED_TILES",
			  "TXT_KEY_CONCEPT_ALL_TILES",
			  "TXT_KEY_CONCEPT_DOMESTIC_TRADE",
			  "TXT_KEY_CONCEPT_FOREIGN_TRADE",
			  "TXT_KEY_CONCEPT_BUILDINGS",
			  "TXT_KEY_CONCEPT_CORPORATIONS",
			  "TXT_KEY_CONCEPT_SPECIALISTS",
			  "TXT_KEY_CONCEPT_BASE_MODIFIER",
			  "TXT_KEY_CONCEPT_PRODUCTION_MODIFIER")

# Yields
YIELDS = (YieldTypes.YIELD_FOOD, YieldTypes.YIELD_PRODUCTION, YieldTypes.YIELD_COMMERCE)

# Tiles
TILES = (WORKED_TILES, CITY_TILES, OWNED_TILES, ALL_TILES)

# Table
HEADING_COLUMN = 0
VALUE_COLUMN = 1
TOTAL_COLUMN = 2

def getViewAndType(iView):
	"""Returns the view boolean and YieldTypes enum given the give number 0-3."""
	if iView == 0:
		return (False, YieldTypes.YIELD_FOOD)
	elif iView in (1, 2, 3):
		return (True, YIELDS[iView - 1])
	else:
		BugUtil.error("RawYields - invalid view number %d", iView)
		return (False, YieldTypes.YIELD_FOOD)

class Tracker:
	
	def __init__(self):
		"""Creates a table to hold all of the tracked values for each yield type."""
		self.values = {}
		for eYield in range(YieldTypes.NUM_YIELD_TYPES):
			self.values[eYield] = {}
			for eType in range(NUM_TYPES):
				self.values[eYield][eType] = 0
		self.tileCounts = [0, 0, 0, 0]
	
	
	def getYield(self, eYield, eType):
		return self.values[eYield][eType]
	
	def _addYield(self, eYield, eType, iValue):
		"""Adds the given yield value to the given type in the table."""
		self.values[eYield][eType] += iValue
	
	
	def addBuilding(self, eYield, iValue):
		self._addYield(eYield, BUILDINGS, iValue)
	
	def addDomesticTrade(self, iValue):
		self._addYield(YieldTypes.YIELD_COMMERCE, DOMESTIC_TRADE, iValue)
	
	def addForeignTrade(self, iValue):
		self._addYield(YieldTypes.YIELD_COMMERCE, FOREIGN_TRADE, iValue)
	
	def processCity(self, pCity):
		"""
		Calculates the yields for the given city's tiles, specialists, corporations and multipliers.
		The building and trade yields are calculated by CvMainInterface.
		"""
		self.calculateTiles(pCity)
		self.calculateSpecialists(pCity)
		self.calculateCorporations(pCity)
		self.calculateModifiers(pCity)
	
	def calculateTiles(self, pCity):
		"""Calculates the yields for all tiles of the given CyCity."""
		for i in range(gc.getNUM_CITY_PLOTS()):
			pPlot = pCity.getCityIndexPlot(i)
			if pPlot and not pPlot.isNone() and pPlot.hasYield():
				if pCity.isWorkingPlot(pPlot):
					self._addTile(WORKED_TILES, pPlot)
				elif pCity.canWork(pPlot):
					self._addTile(CITY_TILES, pPlot)
				elif pPlot.getOwner() == pCity.getOwner():
					self._addTile(OWNED_TILES, pPlot)
				else:
					self._addTile(ALL_TILES, pPlot)
	
	def _addTile(self, eFirstTileType, pPlot):
		for eYield in YIELDS:
			iValue = pPlot.getYield(eYield)
			for eType in range(eFirstTileType, ALL_TILES + 1):
				self._addYield(eYield, eType, iValue)
		for eType in range(eFirstTileType, ALL_TILES + 1):
			self.tileCounts[eType] += 1
	
	def calculateSpecialists(self, pCity):
		pPlayer = gc.getPlayer(pCity.getOwner())
		for eYield in range(YieldTypes.NUM_YIELD_TYPES):
			iValue = 0
			for eSpec in range(gc.getNumSpecialistInfos()):
				iValue += pPlayer.specialistYield(eSpec, eYield) * (pCity.getSpecialistCount(eSpec) + pCity.getFreeSpecialistCount(eSpec))
			self.addSpecialist(eYield, iValue)
	
	def addSpecialist(self, eYield, iValue):
		self._addYield(eYield, SPECIALISTS, iValue)
		
	def calculateCorporations(self, pCity):
		for eYield in range(YieldTypes.NUM_YIELD_TYPES):
			iValue = 0
			for eCorp in range(gc.getNumCorporationInfos()):
				if (pCity.isHasCorporation(eCorp)):
					iValue += pCity.getCorporationYieldByCorporation(eYield, eCorp)
			self.addCorporation(eYield, iValue)
	
	def addCorporation(self, eYield, iValue):
		self._addYield(eYield, CORPORATIONS, iValue)
	
	def calculateModifiers(self, pCity):
		for eYield in range(YieldTypes.NUM_YIELD_TYPES):
			iValue = pCity.getBaseYieldRateModifier(eYield, 0) - 100
			self._addYield(eYield, BASE_MODIFIER, iValue)
		
		# Depends on the item being built
		self.iProductionModifier = pCity.getProductionModifier()
		if self.iProductionModifier != 0:
			self.sModifierDetail = pCity.getProductionName()
	
	
	def fillTable(self, screen, table, eYield, eTileType):
		"""Fills the given GFC table control with the chosen yield values."""
		self.iRow = 0
		# Tiles
		iTotal = self.getYield(eYield, eTileType)
		self.appendTable(screen, table, False, BugUtil.getText(LABEL_KEYS[eTileType], (self.tileCounts[eTileType],)), eYield, iTotal)
		
		# Trade
		for eType in (DOMESTIC_TRADE, FOREIGN_TRADE):
			iValue = self.getYield(eYield, eType)
			if iValue != 0:
				self.appendTable(screen, table, False, BugUtil.getPlainText(LABEL_KEYS[eType]), eYield, iValue, TradeUtil.isFractionalTrade())
		iValue = self.getYield(eYield, DOMESTIC_TRADE) + self.getYield(eYield, FOREIGN_TRADE)
		if TradeUtil.isFractionalTrade():
			iValue //= 100
		iTotal += iValue
		
		# Buildings, Corporations, Specialists
		for eType in (BUILDINGS, CORPORATIONS, SPECIALISTS):
			iValue = self.getYield(eYield, eType)
			if iValue != 0:
				iTotal += iValue
				self.appendTable(screen, table, False, BugUtil.getPlainText(LABEL_KEYS[eType]), eYield, iValue)
		
		# Subtotal and Base Modifiers
		iModifier = self.getYield(eYield, BASE_MODIFIER)
		if iModifier != 0:
			# Subtotal
			self.appendTableTotal(screen, table, eYield, iTotal)
			#self.appendTable(screen, table, True, BugUtil.getPlainText("TXT_KEY_CONCEPT_SUBTOTAL"), eYield, iTotal)
			# Modifier
			iValue = (iTotal * (iModifier + 100) // 100) - iTotal
			iSubtotal = iTotal + iValue
			self.appendTable(screen, table, False, BugUtil.getText("TXT_KEY_CONCEPT_BASE_MODIFIER", (iModifier,)), eYield, iValue)
		else:
			iSubtotal = iTotal
		
		# Subtotal and Production Modifiers
		if eYield == YieldTypes.YIELD_PRODUCTION and self.iProductionModifier != 0:
			# Subtotal
			self.appendTableTotal(screen, table, eYield, iSubtotal)
			#self.appendTable(screen, table, True, BugUtil.getPlainText("TXT_KEY_CONCEPT_SUBTOTAL"), eYield, iSubtotal)
			# Total
			iTotal = iTotal * (iModifier + self.iProductionModifier + 100) // 100
			# Modifier
			iValue = iTotal - iSubtotal
			self.appendTable(screen, table, False, BugUtil.getText("TXT_KEY_CONCEPT_PRODUCTION_MODIFIER", (self.sModifierDetail, self.iProductionModifier)), eYield, iValue)
		else:
			iTotal = iSubtotal
		
		# Total
		self.appendTableTotal(screen, table, eYield, iTotal)
		#self.appendTable(screen, table, True, BugUtil.getPlainText("TXT_KEY_CONCEPT_TOTAL"), eYield, iTotal)
	
	def appendTable(self, screen, table, bTotal, heading, eYield, iValue, bFraction=False):
		"""
		Appends the given yield value to the table control.
		If bTotal is True, the heading is colored yellow and there's no + sign on the value.
		"""
		cYield = gc.getYieldInfo(eYield).getChar()
		screen.appendTableRow(table)
		if bTotal:
			heading = u"<color=205,180,55,255>%s</color>" % heading
			value = u"<color=205,180,55,255>%d</color>" % iValue
			if bFraction:
				# showing fraction doesn't fit in column
				value = u"<color=205,180,55,255>%d</color>" % (iValue // 100)
			else:
				value = u"<color=205,180,55,255>%d</color>" % iValue
		else:
			if bFraction:
				# showing fraction doesn't fit in column
				value = u"%+d" % (iValue // 100)
			else:
				value = u"%+d" % iValue
		screen.setTableText(table, HEADING_COLUMN, self.iRow, u"<font=1>%s</font>" % (heading), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(table, VALUE_COLUMN, self.iRow, u"<font=1>%s%c</font>" % (value, cYield), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		self.iRow += 1

	def appendTableTotal(self, screen, table, eYield, iValue):
		"""
		Appends the given yield total to the table control's 3rd running total column.
		"""
		if self.iRow > 0:
			cYield = gc.getYieldInfo(eYield).getChar()
			value = u"<color=205,180,55,255>%d</color>" % iValue
			screen.setTableText(table, TOTAL_COLUMN, self.iRow - 1, u"<font=1>%s%c</font>" % (value, cYield), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
