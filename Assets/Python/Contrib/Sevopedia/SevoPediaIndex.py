# SevoPediaIndex
#
# Copyright (c) 2008 The BUG Mod.
#
# EF: Converted from Civilopedia version by fitchn.


from CvPythonExtensions import *
import CvUtil
import ScreenInput
import SevoScreenEnums
import BugUtil

gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class SevoPediaIndex:

	def __init__(self, main):
		self.top = main
		
		self.LIST_BUTTON_SIZE = 24
		self.X_INDEX = self.top.X_CATEGORIES
		self.Y_INDEX = self.top.Y_CATEGORIES
		self.W_INDEX = self.top.W_SCREEN - 2 * self.top.X_CATEGORIES
		self.H_INDEX = self.top.H_CATEGORIES
		
		self.X_LETTER = main.X_INDEX + 130  # position of first letter button
		self.Y_LETTER = main.Y_INDEX
		self.W_LETTER = 20
		
		self.index = None
		self.letterTextIDs = None

	def interfaceScreen(self):
		self.buildIndex()
		self.placeIndex()

	def buildIndex(self):
		if self.index: return
		
		techList = self.top.getTechList()
		unitList = self.top.getUnitList()
		unitCombatList = self.top.getUnitCategoryList()
		promotionList = self.top.getPromotionList()
		
		buildingList = self.top.getBuildingList()
		nationalWonderList = self.top.getNationalWonderList()
		greatWonderList = self.top.getGreatWonderList()
		projectList = self.top.getProjectList()
		specialistList = self.top.getSpecialistList()
		
		terrainList = self.top.getTerrainList()
		featureList = self.top.getFeatureList()
		bonusList = self.top.getBonusList()
		improvementList = self.top.getImprovementList()
		
		civList = self.top.getCivilizationList()
		leaderList = self.top.getLeaderList()
		traitList = self.top.getTraitList()
		
		civicList = self.top.getCivicList()
		religionList = self.top.getReligionList()
		corporationList = self.top.getCorporationList()
		
		conceptList = self.top.getConceptList()
		newConceptList = self.top.getNewConceptList()
		
		list=[]
		for item in techList:
			if (item[0][0:4]=="The "):
				list.append([item[0][4:]+","+item[0][0:3],"Tech",item])
			else:
				list.append([item[0],"Tech",item])
		for item in unitList:
			if (item[0][:13]=="TXT_KEY_UNIT_"):
				list.append([item[0][13:].capitalize(),"Unit",item])
			else:
				list.append([item[0],"Unit",item])
		for item in unitCombatList:
			list.append([item[0],"UnitCombat",item])
		for item in promotionList:
			if (item[0][:18]=="TXT_KEY_PROMOTION_"):
				list.append([item[0][18:].capitalize(),"Promo",item])
			else:
				list.append([item[0],"Promo",item])
		
		for item in buildingList:
			if (item[0][:17]=="TXT_KEY_BUILDING_"):
				list.append([item[0][17:].capitalize(),"Building",item])
			else:
				list.append([item[0],"Building",item])
		for item in nationalWonderList:
			if (item[0][0:4]=="The "):
				list.append([item[0][4:]+","+item[0][0:3],"Wonder",item])
			elif (item[0][:17]=="TXT_KEY_BUILDING_"):
				list.append([item[0][17:].capitalize(),"Wonder",item])
			else:
				list.append([item[0],"Wonder",item])
		for item in greatWonderList:
			if (item[0][0:4]=="The "):
				list.append([item[0][4:]+","+item[0][0:3],"Wonder",item])
			elif (item[0][:17]=="TXT_KEY_BUILDING_"):
				list.append([item[0][17:].capitalize(),"Wonder",item])
			else:
				list.append([item[0],"Wonder",item])
		for item in projectList:
			if (item[0][0:4]=="The "):
				list.append([item[0][4:]+","+item[0][0:3],"Project",item])
			else:
				list.append([item[0],"Project",item])
		for item in specialistList:
			if (item[0][:19]=="TXT_KEY_SPECIALIST_"):
				list.append([item[0][19:].capitalize(),"Specialist",item])
			else:
				list.append([item[0],"Specialist",item])
		
		for item in terrainList:
			list.append([item[0],"Terrain",item])
		for item in featureList:
			list.append([item[0],"Feature",item])
		for item in bonusList:
			list.append([item[0],"Bonus",item])
		for item in improvementList:
			list.append([item[0],"Improv",item])
		
		for item in civList:
			list.append([item[0],"Civ",item])
		for item in leaderList:
			list.append([item[0],"Leader",item])
		for item in traitList:
			list.append([item[0][2:],"Trait",item])
		
		for item in religionList:
			list.append([item[0],"Religion",item])
		for item in civicList:
			if (item[0][:14]=="TXT_KEY_CIVIC_"):
				list.append([item[0][14:].capitalize(),"Civic",item])
			else:
				list.append([item[0],"Civic",item])
		
		for item in conceptList:
			list.append([item[0],"Concept",item])
		for item in newConceptList:
			list.append([item[0],"NewConcept",item])
		
		list.sort()
		self.index = list
		
	def placeIndex(self):
		screen = self.top.getScreen()
		CONCEPT_CHAR = gc.getYieldInfo(YieldTypes.YIELD_COMMERCE).getChar()
		
		nColumns = 3
		self.tableName = self.top.getNextWidgetName()
		screen.addTableControlGFC(self.tableName, nColumns, self.X_INDEX, self.Y_INDEX, self.W_INDEX, self.H_INDEX, False, False, self.LIST_BUTTON_SIZE, self.LIST_BUTTON_SIZE, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect(self.tableName, False)
		for i in range(nColumns):
			screen.setTableColumnHeader(self.tableName, i, "", (self.W_INDEX - 10) / nColumns)
		
		iRow = -1
		iColumn = 0
		sLetter = "#"
		iX = self.X_LETTER
		self.letterTextIDs = {}
		for name, type, item in self.index:
			if (name[:1] != sLetter):
				sLetter = name[:1]
				screen.appendTableRow(self.tableName)
				iRow += 1
				screen.setTableText(self.tableName, 1, iRow, u"<font=4>- " + sLetter + u" -</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
				screen.appendTableRow(self.tableName)
				# create letter button
				textName = self.top.getNextWidgetName()
				letterText = u"<font=4>%s</font>" % sLetter
				screen.setText(textName, "Background", letterText, CvUtil.FONT_CENTER_JUSTIFY, 
						iX, self.Y_LETTER, 0, FontTypes.TITLE_FONT, 
						WidgetTypes.WIDGET_GENERAL, iRow, -1)
				self.letterTextIDs[textName] = iRow
				iX += self.W_LETTER
				iRow += 1
				iColumn = 0
			else:
				iColumn += 1
				if (iColumn >= nColumns):
					screen.appendTableRow(self.tableName)
					iRow += 1
					iColumn = 0
			
			sText = u"<font=3>" + item[0] + u"</font>"
			sButton = ""
			eWidget = None
			iData1 = item[1]
			iData2 = 1
			if (type == "Tech"):
				screen.setTableText(self.tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getTechInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			elif (type == "Unit"):
				screen.setTableText(self.tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getUnitInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			elif (type == "UnitCombat"):
				screen.setTableText(self.tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getUnitCombatInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			elif (type == "Promo"):
				screen.setTableText(self.tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getPromotionInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			
			elif (type == "Building"):
				screen.setTableText(self.tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getBuildingInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			elif (type == "Wonder"):
				screen.setTableText(self.tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getBuildingInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			elif (type == "Project"):
				screen.setTableText(self.tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getProjectInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			elif (type == "Specialist"):
				screen.setTableText(self.tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getSpecialistInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPECIALIST, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			
			elif (type == "Terrain"):
				screen.setTableText(self.tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getTerrainInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_TERRAIN, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			elif (type == "Feature"):
				screen.setTableText(self.tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getFeatureInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_FEATURE, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			elif (type == "Bonus"):
				screen.setTableText(self.tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getBonusInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			elif (type == "Improv"):
				screen.setTableText(self.tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getImprovementInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			
			elif (type == "Civ"):
				screen.setTableText(self.tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getCivilizationInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			elif (type == "Leader"):
				screen.setTableText(self.tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getLeaderHeadInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_LEADER, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			elif (type == "Trait"):
				screen.setTableText(self.tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getConceptInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_DESCRIPTION, CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT_NEW, item[1], CvUtil.FONT_LEFT_JUSTIFY)
			
			elif (type == "Civic"):
				screen.setTableText(self.tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getCivicInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			elif (type == "Religion"):
				screen.setTableText(self.tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getReligionInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			elif (type == "Corporation"):
				screen.setTableText(self.tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getReligionInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_CORPORATION, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			
			elif (type == "Concept"):
				screen.setTableText(self.tableName, iColumn, iRow, u"<font=3>%c %s</font>" % (CONCEPT_CHAR, item[0]), gc.getConceptInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_DESCRIPTION, CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT, item[1], CvUtil.FONT_LEFT_JUSTIFY)
			elif (type == "NewConcept"):
				screen.setTableText(self.tableName, iColumn, iRow, u"<font=3>%c %s</font>" % (CONCEPT_CHAR, item[0]), gc.getConceptInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_DESCRIPTION, CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT_NEW, item[1], CvUtil.FONT_LEFT_JUSTIFY)
		
		self.iLastRow = iRow

	def handleInput (self, inputClass):
		BugUtil.debugInput(inputClass)
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED 
				and inputClass.getFunctionName() + str(inputClass.getID()) in self.letterTextIDs):
			screen = self.top.getScreen()
			screen.selectRow(self.tableName, self.iLastRow, True)
			screen.selectRow(self.tableName, inputClass.getData1(), True)
		return 0
