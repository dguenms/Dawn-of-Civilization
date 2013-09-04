## BugOptionsTab
##
## Base class for all tabs in the BUG Options Screen.
##
## Copyright (c) 2007 The BUG Mod.
##
## Author: EmperorFool

import BugOptions
import BugUtil

## Constants

CHECKBOX_INDENT = 2

## Globals

g_options = BugOptions.getOptions()

## Class

class BugOptionsTab:
	"""
	Provides an API for building a single tab on the BUG Options Screen by placing UI controls.
	"""
	
	def __init__(self, name, title):
		self.name = name
		self.tab = self.name + "Tab"
		
		self.title = title
		self.translated = False
		
		# EF: Has to be this module. I tried splitting it out into a new module without success.
		self.callbackIFace = "CvOptionsScreenCallbackInterface"

	def getName (self):
		return self.name

	def getTitle (self):
		if (not self.translated):
			self.translate()
		return self.title
	
	def translate (self):
		xmlKey = "TXT_KEY_BUG_OPTTAB_" + self.name.upper()
		self.title = BugUtil.getPlainText(xmlKey, self.title)
		self.translated = True
	
	def clearTranslation(self):
		"Marks this tab so that it will be translated again the next time it is accessed"
		self.translated = False


	def setOptions (self, options):
		self.options = options

	def getOption (self, name):
		try:
			return g_options.getOption(name)
		except BugUtil.ConfigError:
			return None


	def create (self, screen):
		"Creates the full options screen"
		pass

	def createTab (self, screen):
		"Creates and returns the options tab"
		screen.attachTabItem(self.tab, self.getTitle())
		
		return self.tab

	def createMainPanel (self, screen):
		"Creates and returns the options tab panel with Exit and Help buttons"
		# VBox with two blocks: scrolling control panel and Exit button with separator
		vbox = self.name + "VBox"
		screen.attachVBox(self.tab, vbox)		
		
		# scrollpane
		scrollpane = self.name + "Scroll"
		screen.attachScrollPanel(vbox, scrollpane)
		screen.setLayoutFlag(scrollpane, "LAYOUT_SIZE_HEXPANDING")
		screen.setLayoutFlag(scrollpane, "LAYOUT_SIZE_VEXPANDING")
		
		# panel for option controls
		panel = self.name + "Panel"
		screen.attachPanel(scrollpane, panel)
		screen.setStyle(panel, "Panel_Tan15_Style")
		screen.setLayoutFlag(panel, "LAYOUT_SIZE_HPREFERREDEXPANDING")
		screen.setLayoutFlag(panel, "LAYOUT_SIZE_VPREFERREDEXPANDING")
		
		# panel for Help and Exit buttons
		screen.attachHSeparator(vbox, "RM_ExitSeparator")
		exitPanel = self.name + "ExitBox"
		screen.attachHBox(vbox, exitPanel)
		screen.setLayoutFlag(exitPanel, "LAYOUT_HCENTER")
		
		# Help button
		title = BugUtil.getPlainText("TXT_KEY_BUG_OPTBUTTON_HELP", "Help")
		hover = BugUtil.getPlainText("TXT_KEY_BUG_OPTBUTTON_HELP_HOVER", "Opens the help file. You can hit Shift-F1 from the main interface.")
		helpButton = self.name + "Help"
		self.addButton(screen, exitPanel, helpButton, "handleBugHelpButtonInput", title, hover)
		
		self.addSpacer(screen, exitPanel, exitPanel)
		
		# Exit button
		title = BugUtil.getPlainText("TXT_KEY_PEDIA_SCREEN_EXIT", "Exit")
		hover = BugUtil.getPlainText("TXT_KEY_BUG_OPTBUTTON_EXIT_HOVER", "Exits the BUG Options screen.")
		exitButton = self.name + "Exit"
		self.addButton(screen, exitPanel, exitButton, "handleBugExitButtonInput", title, hover)
		
		return panel

	def addOneColumnLayout (self, screen, parent, panel=None):
		"Creates an HBox containing a single VBox for a list of controls"
		if (panel is None):
			panel = parent
		hbox = panel + "HBox"
		screen.attachHBox(parent, hbox)
		screen.setLayoutFlag(hbox, "LAYOUT_SIZE_HPREFERREDEXPANDING")
		screen.setLayoutFlag(hbox, "LAYOUT_SIZE_VMIN")
		
		column = panel + "VBox"
		screen.attachVBox(hbox, column)
		screen.setLayoutFlag(column, "LAYOUT_SIZE_HMIN")
		screen.setLayoutFlag(column, "LAYOUT_SIZE_VMIN")
		
		return column

	def addTwoColumnLayout (self, screen, parent, panel=None, separator=False):
		"Creates an HBox containing two VBoxes for two lists of controls"
		if (panel is None):
			panel = parent
		hbox = panel + "HBox"
		screen.attachHBox(parent, hbox)
		screen.setLayoutFlag(hbox, "LAYOUT_SIZE_HPREFERREDEXPANDING")
		screen.setLayoutFlag(hbox, "LAYOUT_SIZE_VMIN")
		
		leftColumn = panel + "Left"
		screen.attachVBox(hbox, leftColumn)
		screen.setLayoutFlag(leftColumn, "LAYOUT_SIZE_HMIN")
		screen.setLayoutFlag(leftColumn, "LAYOUT_SIZE_VMIN")
		
		if (separator):
			sep = panel + "Sep"
			screen.attachVSeparator(hbox, sep)
			screen.setLayoutFlag(sep, "LAYOUT_LEFT")
		
		rightColumn = panel + "Right"
		screen.attachVBox(hbox, rightColumn)
		screen.setLayoutFlag(rightColumn, "LAYOUT_SIZE_HMIN")
		screen.setLayoutFlag(rightColumn, "LAYOUT_SIZE_VMIN")
		
		return leftColumn, rightColumn

	def addThreeColumnLayout (self, screen, parent, panel=None, separator=False):
		"Creates an HBox containing three VBoxes for lists of controls"
		return self.addMultiColumnLayout(screen, parent, 3, panel, separator)

	def addMultiColumnLayout (self, screen, parent, count=2, panel=None, separator=False):
		"Creates an HBox containing multiple VBoxes for lists of controls"
		if (count <= 2):
			return self.addTwoColumnLayout(screen, parent, panel, separator)
		
		if (panel is None):
			panel = parent
		hbox = panel + "HBox"
		screen.attachHBox(parent, hbox)
		screen.setLayoutFlag(hbox, "LAYOUT_SIZE_HPREFERREDEXPANDING")
		screen.setLayoutFlag(hbox, "LAYOUT_SIZE_VMIN")
		
		columns = []
		first = True
		for i in range(count):
			if (separator and not first):
				sep = panel + "Sep%d" % i
				screen.attachVSeparator(hbox, sep)
				#screen.setLayoutFlag(sep, "LAYOUT_LEFT")
			first = False
			
			column = panel + "Col%d" % i
			screen.attachVBox(hbox, column)
			screen.setLayoutFlag(column, "LAYOUT_SIZE_HMIN")
			screen.setLayoutFlag(column, "LAYOUT_SIZE_VMIN")
			columns.append(column)
		
		return columns


	def addLabel (self, screen, panel, name, title=None, tooltip=None, spacer=False):
		key = "TXT_KEY_BUG_OPTLABEL_" + name.upper()
		title = BugUtil.getPlainText(key, title)
		#tooltip = BugUtil.getPlainText(key + "_HOVER", tooltip)
		if spacer:
			hbox = name + "HBox"
			screen.attachHBox(panel, hbox)
			#screen.setLayoutFlag(box, "LAYOUT_SIZE_HPREFERREDEXPANDING")
			self.addSpacer(screen, hbox, hbox, CHECKBOX_INDENT)
			panel = hbox
		if (title):
			label = name + "_Label"
			screen.attachLabel(panel, label, title)
			screen.setControlFlag(label, "CF_LABEL_DEFAULTSIZE")
			#if (tooltip):
			#	screen.setToolTip(label, tooltip)
			return label
		return None

	def addSpacer (self, screen, panel, name, size=1):
		spacer = name + "_Spacer"
		screen.attachLabel(panel, spacer, " " * size)
		screen.setControlFlag(spacer, "CF_LABEL_DEFAULTSIZE")
	
	def addButton (self, screen, panel, name, callback, title=None, tooltip=None):
		key = "TXT_KEY_BUG_OPTBUTTON_" + name.upper()
		title = BugUtil.getPlainText(key, title)
		tooltip = BugUtil.getPlainText(key + "_HOVER", tooltip)
		if (title):
			button = name + "_Button"
			screen.attachButton(panel, button, title, self.callbackIFace, callback, button)
			if (tooltip):
				screen.setToolTip(button, tooltip)
			return button
		return None

	def addCheckbox (self, screen, panel, name, spacer=False):
		option = self.getOption(name)
		if (option is not None):
			control = name + "Check"
			value = option.getRealValue()
			if spacer:
				hbox = name + "HBox"
				screen.attachHBox(panel, hbox)
				#screen.setLayoutFlag(box, "LAYOUT_SIZE_HPREFERREDEXPANDING")
				self.addSpacer(screen, hbox, hbox, CHECKBOX_INDENT)
				panel = hbox
			screen.attachCheckBox(panel, control, option.getTitle(), self.callbackIFace, "handleBugCheckboxClicked", name, value)
			screen.setToolTip(control, option.getTooltip())
			if not option.isEnabled():
				screen.setEnabled(control, False)
			return control
		else:
			self.addMissingOption(screen, panel, name)

	def addTextEdit (self, screen, labelPanel, controlPanel, name):
		option = self.getOption(name)
		if (option is not None):
			# create label
			if (labelPanel == controlPanel):
				box = name + "HBox"
				screen.attachHBox(labelPanel, box)
				screen.setLayoutFlag(box, "LAYOUT_SIZE_HPREFERREDEXPANDING")
				labelPanel = box
				controlPanel = box
			if (labelPanel is not None):
				label = name + "Label"
				screen.attachLabel(labelPanel, label, option.getTitle())
				screen.setControlFlag(label, "CF_LABEL_DEFAULTSIZE")
			
			# create textedit
			control = name + "Edit"
			value = str(option.getValue())
			screen.attachEdit(controlPanel, control, value, self.callbackIFace, "handleBugTextEditChange", name)
			screen.setToolTip(control, option.getTooltip())
			screen.setLayoutFlag(control, "LAYOUT_SIZE_HPREFERREDEXPANDING")
			if not option.isEnabled():
				screen.setEnabled(control, False)
			return control
		else:
			self.addMissingOption(screen, labelPanel, name)


	def addDropdown (self, screen, labelPanel, controlPanel, name, spacer, layout, elements, index, callback):
		option = self.getOption(name)
		if (option is not None):
			# create label
			if (labelPanel is not None):
				if (labelPanel == controlPanel or spacer):
					box = name + "HBox"
					screen.attachHBox(labelPanel, box)
					#screen.setLayoutFlag(box, "LAYOUT_SIZE_HPREFERREDEXPANDING")
					if (spacer):
						screen.attachSpacer(box)
					if (labelPanel == controlPanel):
						controlPanel = box
					labelPanel = box
				label = name + "Label"
				screen.attachLabel(labelPanel, label, option.getTitle())
				screen.setControlFlag(label, "CF_LABEL_DEFAULTSIZE")
				
			# create dropdown
			control = name + "Dropdown"
			screen.attachDropDown(controlPanel, control, "", elements, self.callbackIFace, callback, name, index)
			screen.setToolTip(control, option.getTooltip())
			screen.setLayoutFlag(control, "LAYOUT_" + layout.upper())
			if not option.isEnabled():
				screen.setEnabled(control, False)
			return control
		else:
			self.addMissingOption(screen, controlPanel, name)

	def addTextDropdown (self, screen, labelPanel, controlPanel, name, spacer=False, layout="left"):
		option = self.getOption(name)
		if (option is not None):
			index = option.getIndex()
			elements = tuple(option.getDisplayValues())
			return self.addDropdown(screen, labelPanel, controlPanel, name, spacer, layout, elements, index, "handleBugDropdownChange")
		else:
			self.addMissingOption(screen, controlPanel, name)

	def addIntDropdown (self, screen, labelPanel, controlPanel, name, spacer=False, layout="right"):
		option = self.getOption(name)
		if (option is not None):
			index = option.getIndex()
			elements = tuple(option.getDisplayValues())
			return self.addDropdown(screen, labelPanel, controlPanel, name, spacer, layout, elements, index, "handleBugIntDropdownChange")
		else:
			self.addMissingOption(screen, controlPanel, name)

	def addFloatDropdown (self, screen, labelPanel, controlPanel, name, spacer=False, layout="right"):
		option = self.getOption(name)
		if (option is not None):
			index = option.getIndex()
			elements = tuple(option.getDisplayValues())
			return self.addDropdown(screen, labelPanel, controlPanel, name, spacer, layout, elements, index, "handleBugFloatDropdownChange")
		else:
			self.addMissingOption(screen, controlPanel, name)

	def addColorDropdown (self, screen, labelPanel, controlPanel, name, spacer=False, layout="left"):
		option = self.getOption(name)
		if (option is not None):
			index = option.getIndex()
			elements = tuple(option.getDisplayValues())
			return self.addDropdown(screen, labelPanel, controlPanel, name, spacer, layout, elements, index, "handleBugColorDropdownChange")
		else:
			self.addMissingOption(screen, controlPanel, name)
	

	def addCheckboxDropdown (self, screen, checkPanel, dropPanel, checkName, dropName, layout, elements, index, callback, spacer=False):
		"Adds a dropdown with a checkbox for a label."
		checkOption = self.getOption(checkName)
		dropOption = self.getOption(dropName)
		if (checkOption is not None and dropOption is not None):
			# create checkbox
			if (checkPanel == dropPanel):
				box = checkPanel + "HBox"
				screen.attachHBox(checkPanel, box)
				#screen.setLayoutFlag(box, "LAYOUT_SIZE_HPREFERREDEXPANDING")
				checkPanel = box
				dropPanel = box
			checkControl = self.addCheckbox(screen, checkPanel, checkName, spacer)
			
			# create dropdown
			dropControl = dropName + "Dropdown"
			screen.attachDropDown(dropPanel, dropControl, "", elements, self.callbackIFace, callback, dropName, index)
			screen.setToolTip(dropControl, dropOption.getTooltip())
			screen.setLayoutFlag(dropControl, "LAYOUT_" + layout.upper())
			if not dropOption.isEnabled():
				screen.setEnabled(dropControl, False)
			return checkControl, dropControl
		else:
			if (checkOption is None):
				self.addMissingOption(screen, checkPanel, checkOption)
			if (dropOption is None):
				self.addMissingOption(screen, dropPanel, dropOption)

	def addCheckboxTextDropdown (self, screen, checkPanel, dropPanel, checkName, dropName, layout="left", spacer=False):
		checkOption = self.getOption(checkName)
		dropOption = self.getOption(dropName)
		if (checkOption is not None and dropOption is not None):
			index = dropOption.getIndex()
			elements = tuple(dropOption.getDisplayValues())
			checkControl, dropControl = self.addCheckboxDropdown(screen, checkPanel, dropPanel, checkName, dropName, layout, elements, index, "handleBugDropdownChange", spacer)
			return checkControl, dropControl
		else:
			if (checkOption is None):
				self.addMissingOption(screen, checkPanel, checkOption)
			if (dropOption is None):
				self.addMissingOption(screen, dropPanel, dropOption)

	def addCheckboxIntDropdown (self, screen, checkPanel, dropPanel, checkName, dropName, layout="right", spacer=False):
		checkOption = self.getOption(checkName)
		dropOption = self.getOption(dropName)
		if (checkOption is not None and dropOption is not None):
			index = dropOption.getIndex()
			elements = tuple(dropOption.getDisplayValues())
			checkControl, dropControl = self.addCheckboxDropdown(screen, checkPanel, dropPanel, checkName, dropName, layout, elements, index, "handleBugIntDropdownChange", spacer)
			return checkControl, dropControl
		else:
			if (checkOption is None):
				self.addMissingOption(screen, checkPanel, checkOption)
			if (dropOption is None):
				self.addMissingOption(screen, dropPanel, dropOption)

	def addCheckboxFloatDropdown (self, screen, checkPanel, dropPanel, checkName, dropName, layout="right", spacer=False):
		checkOption = self.getOption(checkName)
		dropOption = self.getOption(dropName)
		if (checkOption is not None and dropOption is not None):
			index = dropOption.getIndex()
			elements = tuple(dropOption.getDisplayValues())
			checkControl, dropControl = self.addCheckboxDropdown(screen, checkPanel, dropPanel, checkName, dropName, layout, elements, index, "handleBugFloatDropdownChange", spacer)
			return checkControl, dropControl
		else:
			if (checkOption is None):
				self.addMissingOption(screen, checkPanel, checkOption)
			if (dropOption is None):
				self.addMissingOption(screen, dropPanel, dropOption)
	

	def addSlider (self, screen, labelPanel, controlPanel, name, spacer=False, vertical=False, expanding=True, fill=None, min=0, max=100):
		option = self.getOption(name)
		if (option is not None):
			# create label
			if (labelPanel is not None):
				if (labelPanel == controlPanel or spacer):
					box = name + "HBox"
					screen.attachHBox(labelPanel, box)
					#screen.setLayoutFlag(box, "LAYOUT_SIZE_HPREFERREDEXPANDING")
					if (spacer):
						screen.attachSpacer(box)
					if (labelPanel == controlPanel):
						controlPanel = box
					labelPanel = box
				label = name + "Label"
				screen.attachLabel(labelPanel, label, option.getTitle())
				screen.setControlFlag(label, "CF_LABEL_DEFAULTSIZE")
				
			# create slider
			control = name + "Slider"
			value = option.getRealValue()
			if vertical:
				screen.attachVSlider(controlPanel, control, self.callbackIFace, "handleBugSliderChanged", name, min, max, value)
				if expanding:
					screen.setLayoutFlag(control, "LAYOUT_SIZE_VEXPANDING")
			else:
				screen.attachHSlider(controlPanel, control, self.callbackIFace, "handleBugSliderChanged", name, min, max, value)
				if expanding:
					screen.setLayoutFlag(control, "LAYOUT_SIZE_HEXPANDING")
			if fill:
				screen.setControlFlag(control, "CF_SLIDER_FILL_" + fill.upper())
			screen.setToolTip(control, option.getTooltip())
			if not option.isEnabled():
				screen.setEnabled(control, False)
			return control
		else:
			self.addMissingOption(screen, controlPanel, name)


	def addMissingOption (self, screen, panel, name):
		screen.attachLabel(panel, name + "Missing", "Missing: " + name)
