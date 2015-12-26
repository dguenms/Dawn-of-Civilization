from CvPythonExtensions import *
from Consts import *
import RFCUtils
import csv
import Popup as PyPopup

IMAGE_LOCATION = "D:\Documents\My Games\Beyond the Sword\Doc Export Maps"

gc = CyGlobalContext()
utils = RFCUtils.RFCUtils()

lChangedCoreTiles = [{} for i in range(iNumPlayers)]
lChangedFlipTiles = [{} for i in range(iNumPlayers)]
lChangedSettlerValueTiles = [{} for i in range(iNumPlayers)]

bAutoWater = True
bAutoPeak = True
lPeakExceptions = [(31, 13), (32, 19), (27, 29), (88, 47), (40, 66)]

def changeCore(iPlayer, tPlot):
	bCore = tPlot in getCorePlotList(iPlayer)
	lChangedCoreTiles[iPlayer][tPlot] = not bCore
	
def changeCoreForce(iPlayer, tPlot, bAdd):
	lChangedCoreTiles[iPlayer][tPlot] = bAdd
	
def getCorePlotList(iPlayer):
	iReborn = utils.getReborn(iPlayer)
	lPlotList = utils.getPlotList(tCoreAreasTL[iReborn][iPlayer], tCoreAreasBR[iReborn][iPlayer], tExceptions[iReborn][iPlayer])
	lRemovePlots = []
	for (x, y) in lChangedCoreTiles[iPlayer]:
		if lChangedCoreTiles[iPlayer][(x, y)]:
			if (x, y) not in lPlotList:
				lPlotList.append((x, y))
			else:
				lRemovePlots.append((x, y))
		elif not lChangedCoreTiles[iPlayer][(x, y)]:
			if (x, y) in lPlotList:
				lPlotList.remove((x, y))
			else:
				lRemovePlots.append((x, y))
	for tPlot in lRemovePlots:
		del lChangedCoreTiles[iPlayer][tPlot]
	return lPlotList
	
def changeFlip(iPlayer, tPlot):
	bFlip = tPlot in getFlipPlotList(iPlayer)
	lChangedFlipTiles[iPlayer][tPlot] = not bFlip
		
def changeFlipForce(iPlayer, tPlot, bAdd):
	lChangedFlipTiles[iPlayer][tPlot] = bAdd
		
def getFlipPlotList(iPlayer):
	iReborn = utils.getReborn(iPlayer)
	if iReborn == 0:
		lFlipzonePlots = utils.getPlotList(tBirthAreaTL[iPlayer], tBirthAreaBR[iPlayer], tBirthAreaExceptions[iPlayer])
	else:
		tRebirthExceptions = ()
		if iPlayer in dRebirthExceptions: tRebirthExceptions = dRebirthExceptions[iPlayer]
		lFlipzonePlots = utils.getPlotList(tRebirthArea[iPlayer][0], tRebirthArea[iPlayer][1], tRebirthExceptions)
	lRemovePlots = []
	for (x, y) in lChangedFlipTiles[iPlayer]:
		if lChangedFlipTiles[iPlayer][(x, y)]:
			if (x, y) not in lFlipzonePlots:
				lFlipzonePlots.append((x, y))
			else:
				lRemovePlots.append((x, y))
		elif not lChangedFlipTiles[iPlayer][(x, y)]:
			if (x, y) in lFlipzonePlots:
				lFlipzonePlots.remove((x, y))
			else:
				lRemovePlots.append((x, y))
	for tPlot in lRemovePlots:
		del lChangedFlipTiles[iPlayer][tPlot]
	return lFlipzonePlots
	
def changeSettlerValue(iPlayer, tPlot, iValue):
	lChangedSettlerValueTiles[iPlayer][tPlot] = iValue

def getSettlerValue(iPlayer, tPlot):
	iReborn = utils.getReborn(iPlayer)
	lRemovePlots = []
	for (x, y) in lChangedSettlerValueTiles[iPlayer]:
		iSettlerValue = getSettlerMapValue(iPlayer, iReborn, x, iWorldY-y-1)
		if lChangedSettlerValueTiles[iPlayer][(x, y)] == iSettlerValue:
			lRemovePlots.append((x, y))
	for tPlot in lRemovePlots:
		del lChangedSettlerValueTiles[iPlayer][tPlot]
	if tPlot in lChangedSettlerValueTiles[iPlayer]:
		return lChangedSettlerValueTiles[iPlayer][tPlot]
	iReborn = utils.getReborn(iPlayer)
	return getSettlerMapValue(iPlayer, iReborn, tPlot[0], iWorldY-tPlot[1]-1)

def resetCore(iPlayer):
	lRemovePlots = []
	for (x, y) in lChangedCoreTiles[iPlayer]:
		lRemovePlots.append((x, y))
	for tPlot in lRemovePlots:
		del lChangedCoreTiles[iPlayer][tPlot]
			
def resetFlip(iPlayer):
	lRemovePlots = []
	for (x, y) in lChangedFlipTiles[iPlayer]:
		lRemovePlots.append((x, y))
	for tPlot in lRemovePlots:
		del lChangedFlipTiles[iPlayer][tPlot]

def resetSettler(iPlayer):
	lRemovePlots = []
	for (x, y) in lChangedSettlerValueTiles[iPlayer]:
		lRemovePlots.append((x, y))
	for tPlot in lRemovePlots:
		del lChangedSettlerValueTiles[iPlayer][tPlot]
	
def export():
	lChangedCivCores = []
	lChangedCivFlipzones = []
	lChangedCivSettlerValues = []
	for iPlayer in range(iNumPlayers):
		iCivilization = gc.getPlayer(iPlayer).getCivilizationType()
		sName = gc.getCivilizationInfo(iCivilization).getShortDescription(0)
	
		lCorePlotList = getCorePlotList(iPlayer)
		lFlipPlotList = getFlipPlotList(iPlayer)
		getSettlerValue(iPlayer, (0,0)) #Filter
		
		if lChangedCoreTiles[iPlayer]:
			lChangedCivCores.append(sName)
			file = open(IMAGE_LOCATION + "\Cores\\" + sName, 'wt')
			try:
				writer = csv.writer(file)
				for y in reversed(range(iWorldY)):
					lRow = []
					for x in range(iWorldX):
						if (x, y) in lCorePlotList: lRow.append(1)
						else: lRow.append(0)
					writer.writerow(lRow)
			finally:
				file.close()
		if lChangedFlipTiles[iPlayer]:
			lChangedCivFlipzones.append(sName)
			file = open(IMAGE_LOCATION + "\Flipzones\\" + sName, 'wt')
			try:
				writer = csv.writer(file)
				for y in reversed(range(iWorldY)):
					lRow = []
					for x in range(iWorldX):
						if (x, y) in lFlipPlotList: lRow.append(1)
						else: lRow.append(0)
					writer.writerow(lRow)
			finally:
				file.close()
		if lChangedSettlerValueTiles[iPlayer]:
			lChangedCivSettlerValues.append(sName)
			file = open(IMAGE_LOCATION + "\SettlerValues\\" + sName, 'wt')
			iReborn = utils.getReborn(iPlayer)
			try:
				writer = csv.writer(file)
				for y in reversed(range(iWorldY)):
					lRow = []
					for x in range(iWorldX):
						plot = gc.getMap().plot(x, y)
						if plot.isWater() and bAutoWater: lRow.append(20); continue
						if plot.isPeak() and bAutoPeak and (x, y) not in lPeakExceptions: lRow.append(20); continue
						if (x, y) in lChangedSettlerValueTiles[iPlayer]: lRow.append(lChangedSettlerValueTiles[iPlayer][(x, y)])
						else: lRow.append(getSettlerMapValue(iPlayer, iReborn, x, iWorldY-y-1))
					writer.writerow(lRow)
			finally:
				file.close()
	
	# popup which files have been created
	popup = PyPopup.PyPopup()
	sText = "The following maps have been created.\n\nCore:"
	for sName in lChangedCivCores:
		sText += "\n"+sName
	else:
		sText += "\nNo Civ"
	sText += "\n\nFlipzones:"
	for sName in lChangedCivFlipzones:
		sText += "\n"+sName
	else:
		sText += "\nNo Civ"
	sText += "\n\nSettlerMaps:"
	for sName in lChangedCivSettlerValues:
		sText += "\n"+sName
	else:
		sText += "\nNo Civ"
	popup.setBodyString(sText)
	popup.launch(True, PopupStates.POPUPSTATE_IMMEDIATE)