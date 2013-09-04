## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
import CvUtil
from CvPythonExtensions import *

class PyPopup:
	############## S E T U P    F U N C T I O N S ###################
	def __init__(self, popupID=-1, contextType=EventContextTypes.NO_EVENTCONTEXT, bDynamic = True):
		self.ID = popupID
		self.popup = CyPopup(popupID, contextType, bDynamic)

	# Misc!	

	def isNone(self):
		"verifies valid instance"
		return self.popup.isNone()
	
	def launch(self, bCreateOkButton = True, eState = PopupStates.POPUPSTATE_IMMEDIATE):
		"sets attributes to the popup launch"
		self.popup.launch(bCreateOkButton, eState)
	
	def setUserData(self, userData):
		"sets userData that is passed to OnOkClicked"
		self.popup.setUserData(userData)
	
	def setPosition(self, iX, iY):
		"set the location of the popup"
		self.popup.setPosition(iX, iY)
	
	def setSize(self, iXS, iYS):
		"sets the popups size"
		self.popup.setSize(iXS, iYS)
	
	def addSeparator(self):
		"adds a separator"
		self.popup.addSeparator()
	
	# Header String
	def	setHeaderString( self, strText, uiFlags = CvUtil.FONT_CENTER_JUSTIFY ):
		"sets the header text"
		self.popup.setHeaderString( strText, uiFlags )
	
	# Body String
	def	setBodyString( self, strText, uiFlags = CvUtil.FONT_LEFT_JUSTIFY ):
		"sets the body text"
		self.popup.setBodyString( strText, uiFlags )
	
	def setPythonBodyString( self, strText, strName, strHelpText, uiFlags = CvUtil.FONT_LEFT_JUSTIFY ):
		"PYTHON - sets a body string with help text"
		self.popup.setPythonBodyString( strText, strName, strHelpText, uiFlags )
	
	def setPythonBodyStringXY( self, strText, strName, strHelpText, iX = -1, iY = -1, uiFlags = CvUtil.FONT_LEFT_JUSTIFY ):
		self.popup.setPythonBodyStringXY( strText, strName, strHelpText, iX, iY, uiFlags )
	
	# Radio Buttons
	def	createRadioButtons( self, iNumButtons, iGroup = 0 ):
		"creates radio buttons - only 1 set allowed per popup"
		self.popup.createRadioButtons( iNumButtons, iGroup )
	
	def	setRadioButtonText( self, iRadioButtonID, strText, iGroup = 0 ):
		"sets radio button text - 0 based IDs"
		self.popup.setRadioButtonText( iRadioButtonID, strText, iGroup )

	def	createPythonRadioButtons( self, iNumButtons, iGroup = 0 ):
		"creates python radio buttons - only 1 set allowed per popup"
		self.popup.createPythonRadioButtons( iNumButtons, iGroup )
	
	def	setPythonRadioButtonText( self, iRadioButtonID, strText, strHelpText, iGroup = 0 ):
		"sets python radio button text - 0 based IDs"
		self.popup.setPythonRadioButtonText( iRadioButtonID, strText, strHelpText, iGroup )
	
	# Check Boxes
	def	createCheckBoxes( self, iNumBoxes, iGroup = 0 ):
		"creates check boxes - only 1 set allowed per popup"
		self.popup.createCheckBoxes( iNumBoxes, iGroup )
		
	def	setCheckBoxText( self, iCheckBoxID, strText, iGroup = 0 ):
		"sets the check box text"
		self.popup.setCheckBoxText( iCheckBoxID, strText, iGroup )

	def	createPythonCheckBoxes( self, iNumBoxes, iGroup = 0 ):
		"creates Python check boxes - only 1 set allowed per popup"
		self.popup.createPythonCheckBoxes( iNumBoxes, iGroup )
		
	def	setPythonCheckBoxText( self, iCheckBoxID, strText, strHelpText, iGroup = 0 ):
		"sets the Python check box text"
		self.popup.setPythonCheckBoxText( iCheckBoxID, strText, strHelpText, iGroup )
		
	# Edit Boxes
	def	createEditBox( self, strText, iGroup = 0):
		"adds an edit box"
		self.popup.createEditBox( strText, iGroup )

	def	createEditBoxXY( self, strText, iX = -1, iY = -1, iGroup = 0):
		"adds an edit box at XY"
		self.popup.createEditBox( strText, iX, iY, iGroup )
	
	def	createPythonEditBox( self, strText, strHelpText, iGroup = 0):
		"adds an Python edit box"
		self.popup.createPythonEditBox( strText, strHelpText, iGroup )

	def	createPythonEditBoxXY( self, strText, strHelpText, iGroup = 0, iX = -1, iY = -1 ):
		"adds an Python edit box at XY"
		self.popup.createPythonEditBoxXY( strText, strHelpText, iGroup, iX, iY )

	def setEditBoxMaxCharCount( self, maxCharCount, preferredCharCount = 32, iGroup = 0 ):
		"set the max character count and the preferred character count of the edit box"
		self.popup.setEditBoxMaxCharCount( maxCharCount, preferredCharCount, iGroup )
	
	# Pull Down 
	def	createPullDown( self, iGroup = 0 ):
		"creates a pulldown menu"
		self.popup.createPullDown( iGroup )
	
	def	createPullDownXY( self, iGroup = 0, iX = -1, iY = -1 ):
		"creates a pulldown menu at XY"
		self.popup.createPullDownXY( iGroup, iX, iY )
	
	def	addPullDownString( self, strText, iID, iGroup = 0 ):
		"adds text to the pulldown"
		self.popup.addPullDownString( strText, iID, iGroup )
	
	def	createPythonPullDown( self, strHelpText, iGroup = 0 ):
		"creates a Python pulldown menu"
		self.popup.createPythonPullDown( strHelpText, iGroup )
	
	def	createPythonPullDownXY( self, strHelpText, iGroup = 0, iX = -1, iY = -1 ):
		"creates a Python pulldown menu at XY"
		self.popup.createPythonPullDownXY( strHelpText, iGroup, iX, iY )
	
	# List Box
	def	createListBox( self, iGroup = 0 ):
		"creates a listbox"
		self.popup.createListBox( iGroup )

	def	createListBoxXY( self, iGroup = 0, iX = -1, iY = -1 ):
		"creates a listbox at XY"
		self.popup.createListBoxXY( iGroup, iX, iY )

	def	addListBoxString( self, strText, iID, iGroup = 0 ):
		"adds list box IDs"
		self.popup.addListBoxString( strText, iID, iGroup )

	def	createPythonListBox( self, strHelpText, iGroup = 0 ):
		"creates a Python listbox"
		self.popup.createPythonListBox( strHelpText, iGroup )

	def	createPythonListBoxXY( self, strHelpText, iGroup = 0, iX = -1, iY = -1 ):
		"creates a Python listbox at XY"
		self.popup.createPythonListBoxXY( strHelpText, iGroup, iX, iY )
	
	# spin Box
	def	createSpinBox( self, iIndex, strHelpText, iDefault, iIncrement, iMax, iMin ):
		"creates a listbox"
		self.popup.createSpinBox( iIndex, strHelpText, iDefault, iIncrement, iMax, iMin )

	# Buttons
	def	addButton( self, strText ):
		"adds a Button"
		self.popup.addButton( strText )

	def	addButtonXY( self, strText, iX = -1, iY = -1 ):
		"adds a Button at XY"
		self.popup.addButtonXY( strText, iX, iY )
	
	def addPythonButton( self, strFunctionName, strButtonText, strHelpText, strArtPointer = "Art\Interface\Popups\PopupRadioButton.kfm", iData1 = -1, iData2 = -1, bOption = True):
		"adds a python button"
		self.popup.addPythonButton( strFunctionName, strButtonText, strHelpText, strArtPointer, iData1, iData2, bOption )
	
	def addPythonButtonXY( self, strFunctionName, strButtonText, strHelpText, strArtPointer = "Art\Interface\Popups\PopupRadioButton.kfm", iData1 = -1, iData2 = -1, bOption = True, iX = -1, iY = -1 ):
		"adds a python button at XY"
		# Unofficial Patch begin
		self.popup.addPythonButtonXY( strFunctionName, strButtonText, strHelpText, strArtPointer, iData1, iData2, bOption, iX, iY )	
		# Unofficial Patch end

	# Graphics		
	def	addDDS( self, strImageLocation, iX, iY, iWidth, iHeight ):
		"adds a DDS"
		self.popup.addDDS( strImageLocation, iX, iY, iWidth, iHeight )
			
	def	addPythonDDS( self, strImageLocation, strHelpText, iX, iY, iWidth, iHeight ):
		"adds a DDS"
		self.popup.addPythonDDS( strImageLocation, strHelpText, iX, iY, iWidth, iHeight )
		
	############## T A B L E    F U N C T I O N S ###################
	
	def createTable( self, iRows, iColumns, iGroup = 0 ):
		"creates a table that is size X, Y with GroupID"
		self.popup.createTable( iRows, iColumns, iGroup )
		#CvUtil.pyPrint( "py.Popup createTable( %d, %d )" %(iRows, iColumns) )
	
	def setTableCellSize( self, iCol, iPixels, iGroup = 0 ):
		"set the size of the Cell - required before info is added"
		self.popup.setTableCellSize( iCol, iPixels, iGroup )
	
	def setTableYSize( self, iRow, iSize, iGroup = 0 ):
		"sets the size of the Row"
		self.popup.setTableYSize( iRow, iSize, iGroup )
		
	def addTableCellText( self, iRow, iCol, strText, iGroup = 0):
		"adds text to a Cell"
		if strText == 0 or strText == False or strText == 'None':
			self.addTableBlank( iRow, iCol, iGroup )
			return
		self.popup.addTableCellText( iRow, iCol, unicode(strText), iGroup )		
	
	def addTableBlank( self, iRow, iCol, iGroup = 0 ):
		"adds a blank entry to a table"
		self.addTableCellText( iRow, iCol, "", iGroup )
	
	def addTableCellImage( self, iRow, iCol, strImageLocation, iGroup = 0 ):
		"sets a table cell to locate a cell in the table and have it use an image"
		if strImageLocation:
			self.popup.addTableCellImage( iRow, iCol, str(strImageLocation), iGroup )
			return
		self.addTableBlank( iRow, iCol, iGroup )
	
	def addTableCellDDS( self, iRow, iCol, strImageLocation, iX = 5, iY = 5, iWidth = 20, iHeight = 20, iGroup = 0 ):
		"adds a DDS image to the popup - iX/iY are location, iWidth/iHeight adjust the DDS size"
		if strImageLocation:
			self.popup.addTableCellDDS( iRow, iCol, str(strImageLocation), iX, iY, iWidth, iHeight, iGroup )
			return
		self.addTableBlank( iRow, iCol, iGroup )
	
	def	completeTableAndAttach( self, iGroup = 0, iX = -1, iY = -1 ):
		"completes a Table and Adds it to the popup - iX,iY are for the Tables Location"
		self.popup.completeTableAndAttach( iGroup )
	
	
############ G R O U P      T A B L E S #########################		
		
	def addTitleData(self, TitleList, SizeYTitle = 34):
		"Takes a list of title data and adds it to the popup - (iType, iSize, Name, Data"
		TEXT = 0
		DDS  = 1
		IMG  = 2
		
		for i in range(len(TitleList)):
			titleType, titleName, titleSize = TitleList[i]
				
			# handle setting title size
			self.setTableCellSize(i, titleSize)
			
			if titleType: # if image type
				strFileLocation = titleName #file location is the 2nd entry
				
				if titleType == DDS:
					# Unoffical Patch start
					#data = loopTitle[3]
					#iX, iY, iWidth, iHeight = data
					iX, iY, iWidth, iHeight = titleSize
					# Unoffical Patch end
					self.addTableCellDDS(0, i, strFileLocation, iX, iY, iWidth, iHeight)
				
				elif titleType == IMG:
					self.popup.addTableCellImage(0, i, strFileLocation)
			
			else:
				self.addTableCellText(0, i, titleName)
		self.setTableYSize(0, SizeYTitle)

	def addTableData(self, TableData):
		'Adds data to the table'
		iLenTable = len(TableData)
		for i in range(iLenTable):
			loopRowData = TableData[i]
			self.addTableCellText(i+1, 0, loopRowData[0])
			for j in range(len(loopRowData[1])):
				self.addTableCellText(i+1, j+1, loopRowData[1][j])
