from CvPythonExtensions import *
from Consts import *
from RFCUtils import utils
import Popup as PyPopup
import Areas
import SettlerMaps
import WarMaps
import os

IMAGE_LOCATION = os.getcwd() + "\Mods\\RFC Dawn of Civilization\\Export"

gc = CyGlobalContext()

def changeCore(iPlayer, tPlot):
	x, y = tPlot
	bCore = gc.getMap().plot(x, y).isCore(iPlayer)
	plot = gc.getMap().plot(x, y)
	if plot.isWater() or (plot.isPeak() and tPlot not in Areas.lPeakExceptions): return
	plot.setCore(iPlayer, not bCore)
	
def changeCoreForce(iPlayer, tPlot, bAdd):
	x, y = tPlot
	plot = gc.getMap().plot(x, y)
	if plot.isWater() or (plot.isPeak() and tPlot not in Areas.lPeakExceptions): return
	plot.setCore(iPlayer, bAdd)
	
def changeSettlerValue(iPlayer, tPlot, iValue):
	x, y = tPlot
	plot = gc.getMap().plot(x, y)
	if plot.isWater() or (plot.isPeak() and tPlot not in Areas.lPeakExceptions): return
	plot.setSettlerValue(iPlayer, iValue)
	
def getSettlerValue(iPlayer, tPlot):
	x, y = tPlot
	return gc.getMap().plot(x, y).getSettlerValue(iPlayer)

def changeWarValue(iPlayer, tPlot, iValue):
	x, y = tPlot
	plot = gc.getMap().plot(x, y)
	if plot.isWater() or (plot.isPeak() and tPlot not in Areas.lPeakExceptions): return
	plot.setWarValue(iPlayer, iValue)

def getWarValue(iPlayer, tPlot):
	x, y = tPlot
	return gc.getMap().plot(x, y).getWarValue(iPlayer)

def resetCore(iPlayer):
	Areas.updateCore(iPlayer)

def resetSettler(iPlayer):
	SettlerMaps.updateMap(iPlayer)

def resetWarMap(iPlayer):
	WarMaps.updateMap(iPlayer)

def exportCore(iPlayer, bForce = False):
	iCiv = gc.getPlayer(iPlayer).getCivilizationType()
	sName = gc.getCivilizationInfo(iCiv).getShortDescription(0)
	if iPlayer == iHolyRome:
		sName = "HolyRome"
	elif iPlayer == iAztecs:
		sName = "Aztecs"
	
	lCorePlotList = Areas.getCoreArea(iPlayer)
	bCoreChanged = bForce
	if not bCoreChanged:
		for x in range(iWorldX):
			for y in range(iWorldY):
				bOldCore = (x, y) in lCorePlotList
				if gc.getMap().plot(x, y).isCore(iPlayer) != bOldCore:
					bCoreChanged = True
					break
			if bCoreChanged:
				break
	if bCoreChanged:
		Bottom = iWorldY
		Top = 0
		Left = iWorldX
		Right = 0
		for x in range(iWorldX):
			for y in range(iWorldY):
				if gc.getMap().plot(x, y).isCore(iPlayer):
					if x < Left:
						Left = x
					if x > Right:
						Right = x
					if y < Bottom:
						Bottom = y
					if y > Top:
						Top = y
		BL = (Left, Bottom)
		TR = (Right, Top)

		lExceptions = []
		for x in range(BL[0], TR[0]+1):
			for y in range(BL[1], TR[1]+1):
				plot = gc.getMap().plot(x, y)
				if not plot.isCore(iPlayer) and not (plot.isWater() or (plot.isPeak() and (x, y) not in Areas.lPeakExceptions)):
					lExceptions.append((x, y))

		file = open(IMAGE_LOCATION + "\Cores\\" + sName + ".txt", 'wt')
		try:
			if not utils.isReborn(iPlayer):
				file.write("# tCoreArea\n")
				file.write("("+ str(BL) + ",\t" + str(TR) + "),\t# " + sName)
				if lExceptions:
					file.write("\n\n# dCoreAreaExceptions\n")
					file.write("i" + sName + " : " + str(lExceptions) + ",")
			else:
				file.write("# dChangedCoreArea\n")
					file.write("i" + sName + " : " "("+ str(BL) + ",\t" + str(TR) + "),")
				if lExceptions:
					file.write("\n\n# dChangedCoreAreaExceptions\n")
					file.write("i" + sName + " : " + str(lExceptions) + ",")
		finally:
			file.close()
		sText = "Core map of %s exported" %sName
	else:
		sText = "No changes between current core and core defined in python"
	popup = PyPopup.PyPopup()
	popup.setBodyString(sText)
	popup.launch(True, PopupStates.POPUPSTATE_IMMEDIATE)
	
def exportSettlerMap(iPlayer, bForce = False):
	iCiv = gc.getPlayer(iPlayer).getCivilizationType()
	sName = gc.getCivilizationInfo(iCiv).getShortDescription(0)
	if iPlayer == iHolyRome:
		sName = "HolyRome"
	elif iPlayer == iAztecs:
		sName = "Aztecs"
		
	bSettlerValueChanged = bForce
	if not bSettlerValueChanged:
		for x in range(iWorldX):
			for y in range(iWorldY):
				if getSettlerValue(iPlayer, (x, y)) != SettlerMaps.getMapValue(iCiv, x, y):
					bSettlerValueChanged = True
					break
			if bSettlerValueChanged:
				break
	if bSettlerValueChanged:
		file = open(IMAGE_LOCATION + "\SettlerValues\\" + sName + ".txt", 'wt')
		try:
			file.write("(")
			for y in reversed(range(iWorldY)):
				sLine = "(\t"
				for x in range(iWorldX):
					sLine += "%d,\t" % getSettlerValue(iPlayer, (x, y))
				if y == 0:
					sLine += ")),"
				else:
					sLine += "),\n"
				file.write(sLine)
		finally:
			file.close()
		sText = "Settlermap of %s exported" %sName
	else:
		sText = "No changes between current settlervalues and values defined in python"
	popup = PyPopup.PyPopup()
	popup.setBodyString(sText)
	popup.launch(True, PopupStates.POPUPSTATE_IMMEDIATE)

def exportWarMap(iPlayer, bForce = False):
	iCiv = gc.getPlayer(iPlayer).getCivilizationType()
	sName = gc.getCivilizationInfo(iCiv).getShortDescription(0)
	if iPlayer == iHolyRome:
		sName = "HolyRome"
	elif iPlayer == iAztecs:
		sName = "Aztecs"
		
	bWarMapChanged = bForce
	if not bWarMapChanged:
		for x in range(iWorldX):
			for y in range(iWorldY):
				if getWarValue(iPlayer, (x, y)) != WarMaps.getMapValue(iCiv, x, y):
					bWarMapChanged = True
					break
			if bWarMapChanged:
				break
	if bWarMapChanged:
		file = open(IMAGE_LOCATION + "\WarMaps\\" + sName + ".txt", 'wt')
		try:
			file.write("(")
			for y in reversed(range(iWorldY)):
				sLine = "(\t"
				for x in range(iWorldX):
					sLine += "%d,\t" % getWarValue(iPlayer, (x, y))
				if y == 0:
					sLine += ")),"
				else:
					sLine += "),\n"
				file.write(sLine)
		finally:
			file.close()
		sText = "Warmap of %s exported" %sName
	else:
		sText = "No changes between current warvalues and values defined in python"
	popup = PyPopup.PyPopup()
	popup.setBodyString(sText)
	popup.launch(True, PopupStates.POPUPSTATE_IMMEDIATE)