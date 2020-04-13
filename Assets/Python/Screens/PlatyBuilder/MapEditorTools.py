from CvPythonExtensions import *
from Consts import *
from Core import *
from RFCUtils import *
# import Areas
# import SettlerMaps
# import WarMaps
# import RegionMap
import os

IMAGE_LOCATION = os.getcwd() + "\Mods\\RFC Dawn of Civilization\\Export"
iLongestName = len("Netherlands") #Netherlands currently has the longest civ name

gc = CyGlobalContext()

def getTLBR(lPlots):
	lPlotX = [plot.getX() for plot in plots.of(lPlots)]
	lPlotY = [plot.getY() for plot in plots.of(lPlots)]
	TL = (min(lPlotX), min(lPlotY))
	BR = (max(lPlotX), max(lPlotY))
	return TL, BR

def exportFlip(iPlayer, (lHumanFlipPlot, lAIFlipPlots)):
	sLocation = "FlipZones"
	sName = Infos().civ(player(iPlayer)).getShortDescription(0)
	sDictName = "dBirthArea"
	
	BL, TR = getTLBR(lHumanFlipPlot)
	lExtended = lHumanFlipPlot + lAIFlipPlots
	BLai, TRai = getTLBR(lExtended)
	
	tExceptions = None
	lExceptions = plots.start(BLai).end(TRai).without(lExtended)
	if lExceptions:
		tExceptions = ("dBirthAreaExceptions", lExceptions)
	
	lExtraDictList = None
	if lAIFlipPlots:
		lExtraDictList = [("dExtendedBirthArea", (BLai, TRai))]
		
	writeTRBLDictFile(sLocation, sName, (BL, TR), sDictName, tExceptions, lExtraDictList)
	
	show("Flipzone of %s exported" % sName) 

def exportCore(iPlayer):
	sLocation = "Cores"
	sName = Infos().civ(player(iPlayer)).getShortDescription(0)
	sDictName = "dCoreArea"
	
	lCorePlots = plots.all().core(iPlayer)
	BL, TR = getTLBR(lCorePlots)

	tExceptions = None
	lExceptions = plots.start(BL).end(TR).land().where(lambda p: not (p.isPeak() and location(p) not in Areas.lPeakExceptions) and not p.isCore(iPlayer))
	if lExceptions:
		tExceptions = ("dCoreAreaExceptions", lExceptions)
	
	writeTRBLDictFile(sLocation, sName, (BL, TR), sDictName, tExceptions)
	
	show("Core of %s exported" % sName) 

def exportSettlerMap(iPlayer):
	sLocation = "SettlerValues"
	sName = Infos().civ(player(iPlayer)).getShortDescription(0)
	valueFunction = getSettlerValue
	writeMapFile(sLocation, sName, valueFunction, iPlayer = iPlayer, bDictStyle = True)
	
	show("Settlermap of %s exported" % sName)
	
def getSettlerValue(plot, *args, **kwargs):
	iPlayer = kwargs.get('iPlayer', None)
	
	if plot.isWater():
		return 20
	elif plot.isPeak() and location(plot) in Areas.lPeakExceptions:
		return 20
		
	if iPlayer is not None:
		return player(iPlayer).getSettlerValue(plot.getX(), plot.getY())
		
	return 20

def exportWarMap(iPlayer):
	sLocation = "WarMaps"
	sName = Infos().civ(player(iPlayer)).getShortDescription(0)
	valueFunction = getWarValue
	writeMapFile(sLocation, sName, valueFunction, iPlayer = iPlayer, bDictStyle = True)
	
	utilshow("Warmap of %s exported" % sName)
	
def getWarValue(plot, *args, **kwargs):
	iPlayer = kwargs.get('iPlayer', None)
	if iPlayer is not None:
		return player(iPlayer).getWarValue(plot.getX(), plot.getY())
	return 0


#TODO: use export to csv function in map branch when merged
def exportRegionMap():
	sLocation = "other"
	sName = "RegionMap"
	valueFunction = getRegionValue
	writeMapFile(sLocation, sName, valueFunction, sMapName = "tRegionMap")
	
	show("Regionmap exported")
	
def getRegionValue(plot, *args, **kwargs):

	#TODO: bAutoWater should be removed if water features get their own region ID
	bAutoWater = True
	if plot.isWater() and bAutoWater:
		return -1
		
	return plot.getRegionID()


def exportAreaExport(lPlots, bWaterException, bPeakException):
	pass


def writeMapFile(sFileLocaton, sName, valueFunction, *args, **kwargs):
	sMapName = kwargs.get('sMapName', None)
	bDictStyle = kwargs.get('bDictStyle', False)
	
	file = open(IMAGE_LOCATION + "\\" + sFileLocaton + "\\" + sName + ".txt", 'wt')

	try:
		if sMapName:
			file.write(sMapName + " = ( \n")
		else:
			file.write("(")
		for y in reversed(range(iWorldY)):
			sLine = "(\t"
			for x in range(iWorldX):
				plot = plot_(x, y)
				iValue = valueFunction(plot, *args, **kwargs)
				sLine += "%d,\t" % iValue
			if y == 0 and bDictStyle:
				sLine += ")),"
			else:
				sLine += "),\n"
			file.write(sLine)
		if not bDictStyle:
			file.write(")")
	finally:
		file.close()

def writeTRBLDictFile(sFileLocaton, sName, tSquare, sDictName, tExceptions, lExtraDictList = None):
	BL, TR = tSquare
	
	sIdentifier = "i" + sName
	# allign tabs
	iTabs = (iLongestName - len(sName) - 1) // 4 + 1
	sIdentifierText = sIdentifier + " :" + iTabs*"\t"
	
	file = open(IMAGE_LOCATION + "\\" + sFileLocaton + "\\" + sName + ".txt", 'wt')
	try:
		file.write("# " + sDictName + "\n")
		file.write(sIdentifierText + "("+ str(BL) + ",\t" + str(TR) + "),")
		if tExceptions:
			sExceptionName, lExceptions = tExceptions
			file.write("\n\n# " + sExceptionName + "\n")
			file.write(sIdentifierText + str(lExceptions) + ",")
		if lExtraDictList:
			for sListName, lList in lExtraDictList:
				file.write("\n\n# " + sListName + "\n")
				file.write(sIdentifierText + str(lList) + ",")
	finally:
		file.close()
