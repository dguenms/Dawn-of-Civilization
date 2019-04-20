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
	if iPlayer == iHolyRome:
		sName = "HolyRome"
	elif iPlayer == iAztecs:
		sName = "Aztecs"

	lNewFlipPlotList, lNewAIPlotList = dFlipZoneEdits[iPlayer]
	if utils.isReborn(iPlayer):
		lOldFlipPlotList = Areas.getRebirthArea(iPlayer)
	else:
		lOldFlipPlotList = Areas.getBirthArea(iPlayer)
	bFlipChanged = len(lOldFlipPlotList) != len(lNewFlipPlotList)
	if not bFlipChanged:
		for tPlot in lNewFlipPlotList:
			if tPlot not in lOldFlipPlotList:
				bFlipChanged = True
				break
		else:
			if iPlayer in Areas.dChangedBirthArea:
				tTL, tBR = Areas.getBirthRectangle(iPlayer, True)
				lOldAIPlotList = [tPlot for tPlot in utils.getPlotList(tTL, tBR, utils.getOrElse(Areas.dBirthAreaExceptions, iPlayer, [])) if tPlot not in lOldFlipPlotList]
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
		for tPlot in utils.getPlotList(BL, TR):
			if tPlot not in lNewFlipPlotList:
				lExceptions.append(tPlot)

		if lNewAIPlotList:
			lPlots = lNewAIPlotList+lNewFlipPlotList
			BLAI, TRAI = getTLBR(lPlots)

		file = open(IMAGE_LOCATION + "\FlipZones\\" + sName + ".txt", 'wt')
		try:
			if not utils.isReborn(iPlayer):
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
				if not utils.isReborn(iPlayer):
					file.write("\n\n# dChangedBirthArea\n")
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
	for iPlayer in range(iNumPlayers):
		iCiv = gc.getPlayer(iPlayer).getCivilizationType()
		sName = gc.getCivilizationInfo(iCiv).getShortDescription(0)
		if iPlayer == iHolyRome:
			sName = "HolyRome"
		elif iPlayer == iAztecs:
			sName = "Aztecs"
			
		if iPlayer in dFlipZoneEdits.keys():
			lNewFlipPlotList, lNewAIPlotList = dFlipZoneEdits[iPlayer]
		else:
			if utils.isReborn(iPlayer):
				lNewFlipPlotList = Areas.getRebirthArea(iPlayer)
			else:
				lNewFlipPlotList = Areas.getBirthArea(iPlayer)
			if iPlayer in Areas.dChangedBirthArea:
				tTL, tBR = Areas.getBirthRectangle(iPlayer, True)
				lNewAIPlotList = [tPlot for tPlot in utils.getPlotList(tTL, tBR, utils.getOrElse(Areas.dBirthAreaExceptions, iPlayer, [])) if tPlot not in lNewFlipPlotList]
			else:
				lNewAIPlotList = []

		lPlots = [tPlot for tPlot in lNewFlipPlotList if tPlot not in lNewAIPlotList]
		BL, TR = getTLBR(lPlots)

		lExceptions = []
		for tPlot in utils.getPlotList(BL, TR):
			if tPlot not in lNewFlipPlotList:
				lExceptions.append(tPlot)

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
			file.write("\n\ndChangedBirthArea = {\n")
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
		lCorePlots = [(x, y) for (x, y) in utils.getWorldPlotsList() if gc.getMap().plot(x, y).isCore(iPlayer)]
		BL, TR = getTLBR(lCorePlots)

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

		lCorePlots = [(x, y) for (x, y) in utils.getWorldPlotsList() if gc.getMap().plot(x, y).isCore(iPlayer)]
		BL, TR = getTLBR(lCorePlots)

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
			plot = gc.getMap().plot(x, y)
			if plot.getSettlerValue(iPlayer) != SettlerMaps.getMapValue(iCiv, x, y):
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
			plot = gc.getMap().plot(x, y)
			if plot.getWarValue(iPlayer) != WarMaps.getMapValue(iCiv, x, y):
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
	if bAll:
		if iPlayer == iNumPlayers-1:
			sText = "Warmaps of all Civs exported"
		else:
			return
	popup = PyPopup.PyPopup()
	popup.setBodyString(sText)
	popup.launch(True, PopupStates.POPUPSTATE_IMMEDIATE)

def exportRegionMap(bForce = False):
	bAutoWater = True

	bMapChanged = bForce
	if not bMapChanged:
		for (x, y) in utils.getWorldPlotsList():
			plot = gc.getMap().plot(x, y)
			if plot.getRegionID() != RegionMap.getMapValue(x, y):
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
		lExceptions = [(x, y) for (x, y) in utils.getPlotList(BL, TR) if (x, y) not in lPlots and (bWaterException and gc.getMap().plot(x, y).isWater()) and (bPeakException and gc.getMap().plot(x, y).isPeak())]
		
		if bWaterException:
			lExceptions.extend([(x, y) for (x, y) in lPlots if gc.getMap().plot(x, y).isWater() and (x, y) not in lExceptions])
		if bPeakException:
			lExceptions.extend([(x, y) for (x, y) in lPlots if gc.getMap().plot(x, y).isPeak() and (x, y) not in lExceptions])

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
