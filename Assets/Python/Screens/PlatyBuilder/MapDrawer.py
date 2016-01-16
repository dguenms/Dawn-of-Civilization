from CvPythonExtensions import *
from Consts import *
import RFCUtils
import csv
import Popup as PyPopup
import Areas
import SettlerMaps

IMAGE_LOCATION = "D:\Documents\My Games\Beyond the Sword\Doc Export Maps"

gc = CyGlobalContext()
utils = RFCUtils.RFCUtils()

bAutoWater = True
bAutoPeak = True
lPeakExceptions = [(31, 13), (32, 19), (27, 29), (88, 47), (40, 66)]

def changeCore(iPlayer, tPlot):
	x, y = tPlot
	bCore = gc.getMap().plot(x, y).isCore(iPlayer)
	gc.getMap().plot(x, y).setCore(iPlayer, not bCore)
	
def changeCoreForce(iPlayer, tPlot, bAdd):
	x, y = tPlot
	gc.getMap().plot(x, y).setCore(iPlayer, bAdd)
	
def changeFlip(iPlayer, tPlot):
	return
	bFlip = tPlot in getFlipPlotList(iPlayer)
	lChangedFlipTiles[iPlayer][tPlot] = not bFlip
		
def changeFlipForce(iPlayer, tPlot, bAdd):
	return
	lChangedFlipTiles[iPlayer][tPlot] = bAdd
	
def changeSettlerValue(iPlayer, tPlot, iValue):
	x, y = tPlot
	gc.getMap().plot(x, y).setSettlerValue(iPlayer, iValue)
	
def getSettlerValue(iPlayer, tPlot):
	x, y = tPlot
	return gc.getMap().plot(x, y).getSettlerValue(iPlayer)

def resetCore(iPlayer):
	Areas.updateCore(iPlayer)
			
def resetFlip(iPlayer):
	return
	lRemovePlots = []
	for (x, y) in lChangedFlipTiles[iPlayer]:
		lRemovePlots.append((x, y))
	for tPlot in lRemovePlots:
		del lChangedFlipTiles[iPlayer][tPlot]

def resetSettler(iPlayer):
	SettlerMaps.updateMap(iPlayer)
	
def export():
	lChangedCivCores = []
	lChangedCivFlipzones = []
	lChangedCivSettlerValues = []
	
	for iPlayer in range(iNumPlayers):
		iCiv = gc.getPlayer(iPlayer).getCivilizationType()
		sName = gc.getCivilizationInfo(iCiv).getShortDescription(0)
		
		# Core plots
		lCorePlotList = Areas.getCoreArea(iPlayer)
		bCoreChanged = False
		for x in range(iWorldX):
			for y in range(iWorldY):
				bOldCore = (x, y) in lCorePlotList
				if gc.getMap().plot(x, y).isCore(iPlayer) != bOldCore:
					bCoreChanged = True
					break
		if bCoreChanged:
			lChangedCivCores.append(sName)
			file = open(IMAGE_LOCATION + "\Cores\\" + sName, 'wt')
			try:
				writer = csv.writer(file)
				for y in reversed(range(iWorldY)):
					lRow = []
					for x in range(iWorldX):
						if gc.getMap().plot(x, y).isCore(iPlayer): lRow.append(1)
						else: lRow.append(0)
					writer.writerow(lRow)
			finally:
				file.close()
		
		# lFlipPlotList = getFlipPlotList(iPlayer)
		# if lChangedFlipTiles[iPlayer]:
			# lChangedCivFlipzones.append(sName)
			# file = open(IMAGE_LOCATION + "\Flipzones\\" + sName, 'wt')
			# try:
				# writer = csv.writer(file)
				# for y in reversed(range(iWorldY)):
					# lRow = []
					# for x in range(iWorldX):
						# if (x, y) in lFlipPlotList: lRow.append(1)
						# else: lRow.append(0)
					# writer.writerow(lRow)
			# finally:
				# file.close()
				
		bSettlerValueChanged = False
		for x in range(iWorldX):
			for y in range(iWorldY):
				if getSettlerValue(iPlayer, (x, y)) != SettlerMaps.getMapValue(iCiv, x, y):
					bSettlerValueChanged = True
					break
		if bSettlerValueChanged:
			lChangedCivSettlerValues.append(sName)
			file = open(IMAGE_LOCATION + "\SettlerValues\\" + sName, 'wt')
			try:
				writer = csv.writer(file)
				for y in reversed(range(iWorldY)):
					lRow = []
					for x in range(iWorldX):
						plot = gc.getMap().plot(x, y)
						if plot.isWater() and bAutoWater: lRow.append(20); continue
						if plot.isPeak() and bAutoPeak and (x, y) not in lPeakExceptions: lRow.append(20); continue
						lRow.append(getSettlerValue(iPlayer, (x, y)))
					writer.writerow(lRow)
			finally:
				file.close()
	
	# popup which files have been created
	popup = PyPopup.PyPopup()
	sText = "The following maps have been created.\n\nCore:"
	if lChangedCivCores:
		for sName in lChangedCivCores:
			sText += "\n"+sName
	else:
		sText += "\nNo Civ"
	sText += "\n\nFlipzones:"
	if lChangedCivFlipzones:
		for sName in lChangedCivFlipzones:
			sText += "\n"+sName
	else:
		sText += "\nNo Civ"
	sText += "\n\nSettlerMaps:"
	if lChangedCivSettlerValues:
		for sName in lChangedCivSettlerValues:
			sText += "\n"+sName
	else:
		sText += "\nNo Civ"
	popup.setBodyString(sText)
	popup.launch(True, PopupStates.POPUPSTATE_IMMEDIATE)