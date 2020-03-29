from CvPythonExtensions import *
from Consts import *
from Core import *
from RFCUtils import *
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

def getTLBR(lPlots):
	lPlotX = [x for (x, y) in lPlots]
	lPlotY = [y for (x, y) in lPlots]
	TL = (min(lPlotX), min(lPlotY))
	BR = (max(lPlotX), max(lPlotY))
	return TL, BR

def exportFlip(iPlayer, dFlipZoneEdits):
	if iPlayer not in dFlipZoneEdits.keys():
		sText = "No changes between current flipzone and flipzone defined in python"
		popup = PyPopup.PyPopup()
		popup.setBodyString(sText)
		popup.launch(True, PopupStates.POPUPSTATE_IMMEDIATE)
		return

	iCiv = gc.getPlayer(iPlayer).getCivilizationType()
	sName = gc.getCivilizationInfo(iCiv).getShortDescription(0)
	if iCiv == iCivHolyRome:
		sName = "HolyRome"
	elif iCiv == iCivAztecs:
		sName = "Aztecs"

	lNewFlipPlotList, lNewAIPlotList = dFlipZoneEdits[iPlayer]
	lOldFlipPlotList = Areas.getBirthArea(iCiv)
	bFlipChanged = len(lOldFlipPlotList) != len(lNewFlipPlotList)
	if not bFlipChanged:
		for tPlot in lNewFlipPlotList:
			if tPlot not in lOldFlipPlotList:
				bFlipChanged = True
				break
		else:
			if iPlayer in Areas.dExtendedBirthArea:
				tTL, tBR = Areas.getBirthRectangle(iCiv, True)
				lOldAIPlotList = plots.start(tTL).end(tBR).without(Areas.dBirthAreaExceptions[iCiv]).without(lOldFlipPlotList)
			else:
				lOldAIPlotList = []
			bFlipChanged = len(lOldAIPlotList) != len(lNewAIPlotList)
			if not bFlipChanged:
				for tPlot in lNewAIPlotList:
					if tPlot not in lOldAIPlotList:
						bFlipChanged = True
						break

	if bFlipChanged:
		lPlots = [tPlot for tPlot in lNewFlipPlotList if tPlot not in lNewAIPlotList]
		BL, TR = getTLBR(lPlots)

		lExceptions = []
		for plot in plots.start(BL).end(TR).without(lNewFlipPlotList):
			lExceptions.append(location(plot))

		if lNewAIPlotList:
			lPlots = lNewAIPlotList+lNewFlipPlotList
			BLAI, TRAI = getTLBR(lPlots)

		file = open(IMAGE_LOCATION + "\FlipZones\\" + sName + ".txt", 'wt')
		try:
			if not player(iPlayer).isReborn():
				file.write("# tBirthArea\n")
				file.write("("+ str(BL) + ",\t" + str(TR) + "),\t# " + sName)
				if lExceptions:
					file.write("\n\n# dBirthAreaExceptions\n")
					file.write("i" + sName + " : " + str(lExceptions) + ",")
			else:
				file.write("# dRebirthArea\n")
				file.write("i" + sName + " : " "("+ str(BL) + ",\t" + str(TR) + "),")
				if lExceptions:
					file.write("\n\n# dRebirthAreaExceptions\n")
					file.write("i" + sName + " : " + str(lExceptions) + ",")

			if lNewAIPlotList:
				if not player(iPlayer).isReborn():
					file.write("\n\n# dExtendedBirthArea\n")
					file.write("("+ str(BLAI) + ",\t" + str(TRAI) + "),\t# " + sName)
		finally:
			file.close()
		sText = "Flipzone map of %s exported" %sName
	else:
		sText = "No changes between current flipzone and flipzone defined in python"
	popup = PyPopup.PyPopup()
	popup.setBodyString(sText)
	popup.launch(True, PopupStates.POPUPSTATE_IMMEDIATE)

def exportAllFlip(dFlipZoneEdits):
	lAllFlips = []
	lAllExceptions = []
	lAllAIPlots = []
	for iPlayer in players.major():
		iCiv = gc.getPlayer(iPlayer).getCivilizationType()
		sName = gc.getCivilizationInfo(iCiv).getShortDescription(0)
		if iCiv == iCivHolyRome:
			sName = "HolyRome"
		elif iCiv == iCivAztecs:
			sName = "Aztecs"
			
		if iPlayer in dFlipZoneEdits.keys():
			lNewFlipPlotList, lNewAIPlotList = dFlipZoneEdits[iPlayer]
		else:
			lNewFlipPlotList = Areas.getBirthArea(iCiv)
			
			if iPlayer in Areas.dExtendedBirthArea:
				tTL, tBR = Areas.getBirthRectangle(iCiv, True)
				lNewAIPlotList = plots.start(tTL).end(tBR).without(Areas.dBirthAreaExceptions[iCiv]).without(lNewFlipPlotList)
			else:
				lNewAIPlotList = []

		lPlots = [tPlot for tPlot in lNewFlipPlotList if tPlot not in lNewAIPlotList]
		BL, TR = getTLBR(lPlots)

		lExceptions = []
		for plot in plots.start(BL).end(TR):
			lExceptions.append(location(plot))

		if lNewAIPlotList:
			lPlots = [tPlot for tPlot in lNewAIPlotList+lNewFlipPlotList if tPlot not in lExceptions]
			BLAI, TRAI = getTLBR(lPlots)

		lAllFlips.append("("+ str(BL) + ",\t" + str(TR) + "),\t# " + sName)
		if lExceptions:
			lAllExceptions.append("i" + sName + " : " + str(lExceptions) + ",")
		if lNewAIPlotList:
			lAllAIPlots.append("i" + sName + " : (" + str(BLAI) + ",\t" + str(TRAI) + "),")

	file = open(IMAGE_LOCATION + "\FlipZones\\AllFlipZones.txt", 'wt')
	try:
		file.write("tBirthArea = (\n")
		for sString in lAllFlips:
			file.write(sString + "\n")
		file.write(")")
		if lAllAIPlots:
			file.write("\n\ndExtendedBirthArea = {\n")
			for sString in lAllAIPlots:
				file.write(sString + "\n")
			file.write("}")
		if lAllExceptions:
			file.write("\n\ndBirthAreaExceptions = {\n")
			for sString in lAllExceptions:
				file.write(sString + "\n")
			file.write("}")
	finally:
		file.close()
	sText = "All flipzone maps exported"
	popup = PyPopup.PyPopup()
	popup.setBodyString(sText)
	popup.launch(True, PopupStates.POPUPSTATE_IMMEDIATE)

def exportCore(iPlayer, bForce = False):
	iCiv = gc.getPlayer(iPlayer).getCivilizationType()
	sName = gc.getCivilizationInfo(iCiv).getShortDescription(0)
	if iCiv == iCivHolyRome:
		sName = "HolyRome"
	elif iCiv == iCivAztecs:
		sName = "Aztecs"

	lCorePlotList = Areas.getCoreArea(iCiv)
	bCoreChanged = bForce
	if not bCoreChanged:
		for plot in plots.all():
			bOldCore = (x, y) in lCorePlotList
			if plot.isCore(iPlayer) != bOldCore:
				bCoreChanged = True
				break
	if bCoreChanged:
		lCorePlots = plots.all().core(iPlayer)
		BL, TR = getTLBR(lCorePlots)

		lExceptions = []
		for plot in plots.start(BL).end(TR):
			if not plot.isCore(iPlayer) and not (plot.isWater() or (plot.isPeak() and (x, y) not in Areas.lPeakExceptions)):
				lExceptions.append(location(plot))

		file = open(IMAGE_LOCATION + "\Cores\\" + sName + ".txt", 'wt')
		try:
			file.write("# tCoreArea\n")
			file.write("("+ str(BL) + ",\t" + str(TR) + "),\t# " + sName)
			if lExceptions:
				file.write("\n\n# dCoreAreaExceptions\n")
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
	for iPlayer in players.major():
		iCiv = gc.getPlayer(iPlayer).getCivilizationType()
		sName = gc.getCivilizationInfo(iCiv).getShortDescription(0)
		if iCiv == iCivHolyRome:
			sName = "HolyRome"
		elif iCiv == iCivAztecs:
			sName = "Aztecs"

		lCorePlots = plots.all().core(iPlayer)
		BL, TR = getTLBR(lCorePlots)

		lExceptions = []
		for plot in plots.start(BL).end(TR):
			if not plot.isCore(iPlayer) and not (plot.isWater() or (plot.isPeak() and (x, y) not in Areas.lPeakExceptions)):
				lExceptions.append(location(plot))

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

def exportSettlerMap(iPlayer, bForce = False):
	iCiv = gc.getPlayer(iPlayer).getCivilizationType()
	sName = gc.getCivilizationInfo(iCiv).getShortDescription(0)
	if iCiv == iCivHolyRome:
		sName = "HolyRome"
	elif iCiv == iCivAztecs:
		sName = "Aztecs"

	bSettlerValueChanged = bForce
	if not bSettlerValueChanged:
		for plot in plots.all():
			if plot.getSettlerValue(iPlayer) != SettlerMaps.getMapValue(iPlayer, location(plot)):
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
						iValue = plot.getSettlerValue(iPlayer)
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

def exportWarMap(iPlayer, bForce = False):
	iCiv = gc.getPlayer(iPlayer).getCivilizationType()
	sName = gc.getCivilizationInfo(iCiv).getShortDescription(0)
	if iCiv == iCivHolyRome:
		sName = "HolyRome"
	elif iCiv == iCivAztecs:
		sName = "Aztecs"

	bWarMapChanged = bForce
	if not bWarMapChanged:
		for plot in plots.all():
			if plot.getWarValue(iPlayer) != WarMaps.getMapValue(iPlayer, location(plot)):
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
						iValue = max(8, plot.getWarValue(iPlayer))
					else:
						iValue = plot.getWarValue(iPlayer)
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

def exportRegionMap(bForce = False):
	bAutoWater = True

	bMapChanged = bForce
	if not bMapChanged:
		for plot in plots.all():
			if plot.getRegionID() != RegionMap.getMapValue(plot.getX(), plot.getY()):
				bMapChanged = True
				break
	if bMapChanged:
		file = open(IMAGE_LOCATION + "\Other\\RegionMap.txt", 'wt')
		try:
			file.write("tRegionMap = ( \n")
			for y in reversed(range(iWorldY)):
				sLine = "(\t"
				for x in range(iWorldX):
					plot = gc.getMap().plot(x, y)
					if plot.isWater() and bAutoWater:
						iValue = -1
					else:
						iValue = plot.getRegionID()
					sLine += "%d,\t" % iValue
				sLine += "),\n"
				file.write(sLine)
			file.write(")")
		finally:
			file.close()
		sText = "Regionmap exported"
	else:
		sText = "No changes between current regionmap and values defined in python"
	popup = PyPopup.PyPopup()
	popup.setBodyString(sText)
	popup.launch(True, PopupStates.POPUPSTATE_IMMEDIATE)

def exportAreaExport(lPlots, bWaterException, bPeakException):
	if lPlots:
		BL, TR = getTLBR(lPlots)
		lExceptions = [plot for plot in plots.start(BL).end(TR) if location(plot) not in lPlots and (bWaterException and plot.isWater()) and (bPeakException and plot.isPeak())]
		
		if bWaterException:
			lExceptions.extend([(x, y) for (x, y) in lPlots if plot(x, y).isWater() and (x, y) not in lExceptions])
		if bPeakException:
			lExceptions.extend([(x, y) for (x, y) in lPlots if plot(x, y).isPeak() and (x, y) not in lExceptions])

		file = open(IMAGE_LOCATION + "\Other\\NewArea.txt", 'wt')
		try:
			file.write("# tBL, tTR\n")
			file.write("("+ str(BL) + ",\t" + str(TR) + ")")
			if lExceptions:
				file.write("\n\n# lExceptions\n")
				file.write(str(lExceptions))
		finally:
			file.close()
		sText = "Area exported"
	else:
		sText = "No area selected"
	popup = PyPopup.PyPopup()
	popup.setBodyString(sText)
	popup.launch(True, PopupStates.POPUPSTATE_IMMEDIATE)
