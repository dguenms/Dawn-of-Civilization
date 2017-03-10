from CvPythonExtensions import *
from Consts import *
from RFCUtils import utils
import Popup as PyPopup
import Areas
import SettlerMaps
import WarMaps
import RegionMap
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

def changeWarValue(iPlayer, tPlot, iValue):
	x, y = tPlot
	plot = gc.getMap().plot(x, y)
	if plot.isWater() or (plot.isPeak() and tPlot not in Areas.lPeakExceptions): return
	plot.setWarValue(iPlayer, iValue)

def changeReligionValue(iReligion, pPlot, iValue):
	if pPlot.isWater(): return
	pPlot.setSpreadFactor(iReligion, iValue)

def changeRegionID(pPlot, iRegion):
	if pPlot.isWater(): return
	pPlot.setRegionID(iRegion)

def resetPlotRegionID(pPlot):
	if pPlot.isWater(): return
	pPlot.setRegionID(RegionMap.getMapValue(pPlot.getX(), pPlot.getY()))

def resetCore(iPlayer):
	Areas.updateCore(iPlayer)

def resetSettler(iPlayer):
	SettlerMaps.updateMap(iPlayer)

def resetWarMap(iPlayer):
	WarMaps.updateMap(iPlayer)

def resetReligionMap(iReligion):
	RegionMap.updateReligionSpread(iReligion)

def resetRegionMap():
	RegionMap.updateRegionMap()

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
		for (x, y) in utils.getWorldPlotsList():
			bOldCore = (x, y) in lCorePlotList
			if gc.getMap().plot(x, y).isCore(iPlayer) != bOldCore:
				bCoreChanged = True
				break
	if bCoreChanged:
		Bottom = iWorldY
		Top = 0
		Left = iWorldX
		Right = 0
		for (x, y) in utils.getWorldPlotsList():
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
		for (x, y) in utils.getPlotList(BL, TR):
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

def exportAllCores():
	lAllCores = []
	lAllExceptions = []
	for iPlayer in range(iNumPlayers):
		iCiv = gc.getPlayer(iPlayer).getCivilizationType()
		sName = gc.getCivilizationInfo(iCiv).getShortDescription(0)
		if iPlayer == iHolyRome:
			sName = "HolyRome"
		elif iPlayer == iAztecs:
			sName = "Aztecs"

		Bottom = iWorldY
		Top = 0
		Left = iWorldX
		Right = 0
		for (x, y) in utils.getWorldPlotsList():
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
		for (x, y) in utils.getPlotList(BL, TR):
			plot = gc.getMap().plot(x, y)
			if not plot.isCore(iPlayer) and not (plot.isWater() or (plot.isPeak() and (x, y) not in Areas.lPeakExceptions)):
				lExceptions.append((x, y))

		lAllCores.append("("+ str(BL) + ",\t" + str(TR) + "),\t# " + sName)
		if lExceptions:
			lAllExceptions.append("i" + sName + " : " + str(lExceptions) + ",")

	file = open(IMAGE_LOCATION + "\Cores\\AllCores.txt", 'wt')
	try:
		file.write("tCoreArea = (\n")
		for sString in lAllCores:
			file.write(sString + "\n")
		file.write(")")
		file.write("\n\ndCoreAreaExceptions = {\n")
		for sString in lAllExceptions:
			file.write(sString + "\n")
		file.write("}")
	finally:
		file.close()
	sText = "All core maps exported"
	popup = PyPopup.PyPopup()
	popup.setBodyString(sText)
	popup.launch(True, PopupStates.POPUPSTATE_IMMEDIATE)

def exportSettlerMap(iPlayer, bForce = False, bAll = False):
	iCiv = gc.getPlayer(iPlayer).getCivilizationType()
	sName = gc.getCivilizationInfo(iCiv).getShortDescription(0)
	if iPlayer == iHolyRome:
		sName = "HolyRome"
	elif iPlayer == iAztecs:
		sName = "Aztecs"

	bSettlerValueChanged = bForce
	if not bSettlerValueChanged:
		for (x, y) in utils.getWorldPlotsList():
			if getSettlerValue(iPlayer, (x, y)) != SettlerMaps.getMapValue(iCiv, x, y):
				bSettlerValueChanged = True
				break
	if bSettlerValueChanged:
		file = open(IMAGE_LOCATION + "\SettlerValues\\" + sName + ".txt", 'wt')
		try:
			file.write("(")
			for y in reversed(range(iWorldY)):
				sLine = "(\t"
				for x in range(iWorldX):
					plot = gc.getMap().plot(x, y)
					if plot.isWater() or (plot.isPeak() and (x, y) not in Areas.lPeakExceptions):
						iValue = 20
					else:
						iValue = getSettlerValue(iPlayer, (x, y))
					sLine += "%d,\t" % iValue
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
	if bAll:
		if iPlayer == iNumPlayers-1:
			sText = "Settlermaps of all Civs exported"
		else:
			return
	popup = PyPopup.PyPopup()
	popup.setBodyString(sText)
	popup.launch(True, PopupStates.POPUPSTATE_IMMEDIATE)

def exportWarMap(iPlayer, bForce = False, bAll = False):
	iCiv = gc.getPlayer(iPlayer).getCivilizationType()
	sName = gc.getCivilizationInfo(iCiv).getShortDescription(0)
	if iPlayer == iHolyRome:
		sName = "HolyRome"
	elif iPlayer == iAztecs:
		sName = "Aztecs"

	bWarMapChanged = bForce
	if not bWarMapChanged:
		for (x, y) in utils.getWorldPlotsList():
			if getWarValue(iPlayer, (x, y)) != WarMaps.getMapValue(iCiv, x, y):
				bWarMapChanged = True
				break
	if bWarMapChanged:
		file = open(IMAGE_LOCATION + "\WarMaps\\" + sName + ".txt", 'wt')
		try:
			file.write("(")
			for y in reversed(range(iWorldY)):
				sLine = "(\t"
				for x in range(iWorldX):
					plot = gc.getMap().plot(x, y)
					if plot.isWater() or (plot.isPeak() and (x, y) not in Areas.lPeakExceptions):
						iValue = 0
					elif plot.isCore(iPlayer):
						iValue = max(8, getWarValue(iPlayer, (x, y)))
					else:
						iValue = getWarValue(iPlayer, (x, y))
					sLine += "%d,\t" % iValue
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
	if bAll:
		if iPlayer == iNumPlayers-1:
			sText = "Warmaps of all Civs exported"
		else:
			return
	popup = PyPopup.PyPopup()
	popup.setBodyString(sText)
	popup.launch(True, PopupStates.POPUPSTATE_IMMEDIATE)