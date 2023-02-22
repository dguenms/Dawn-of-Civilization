from Core import *
from Areas import *

import Locations

from CvScreensInterface import worldBuilderScreen as worldBuilder
from CvPlatyBuilderScreen import CvWorldBuilderScreen

import BugPath as path
import csv


engine = CyEngine()

MAPS_PATH = "Assets/Maps"


### Generic Landmark Functions ###

def createLandmark(tile, label):
	engine.addLandmark(plot(tile), label.encode("latin-1"))


def createLandmarks(dLandmarks):
	for tile, label in dLandmarks.items():
		createLandmark(tile, label)


def createCivLandmarks(dPlots):
	dLandmarks = dict((tile, infos.civ(iCiv).getShortDescription(0)) for iCiv, tile in dPlots.items())
	createLandmarks(dLandmarks)


def createRectangleLandmarks(label, tTL, tBR):
	dLandmarks = {
		tTL: "%s TL" % label,
		tBR: "%s BR" % label,
	}
	createLandmarks(dLandmarks)


def paintArea(area, index=1000, color="COLOR_CYAN"):
	engine.clearAreaBorderPlots(index)
	for p in area:
		x, y = location(p)
		engine.fillAreaBorderPlotAlt(x, y, index, color, 0.7)	


def getLandmarks():
	for iSign in range(engine.getNumSigns()):
		sign = engine.getSignByIndex(iSign)
		if sign.getPlayerType() == -1:
			yield sign.getPlot(), sign.getCaption().encode("latin-1")


def exportLandmarks():
	file_path = "%s/%s/%s" % (path.getModDir(), MAPS_PATH, "Export/Landmarks.txt")
	file = open(file_path, "w")
	
	try:
		for plot, caption in getLandmarks():
			content = '"%s":\t\t%s\n' % (caption, location(plot))
			print content
			file.write(content)
	finally:
		file.close()


def getCorners(area):
	tiles = [location(p) for p in area]
	x_coords, y_coords = zip(*tiles)
	return (min(x_coords), min(y_coords)), (max(x_coords), max(y_coords))


def exportArea():
	area = worldBuilder.TempInfo[:]
	if not area:
		return
		
	tBL, tTR = getCorners(area)
	
	exceptions = [location(p) for p in plots.rectangle(tBL, tTR) if location(p) not in area and not p.isWater()]

	file_path = "%s/%s/%s" % (path.getModDir(), MAPS_PATH, "Export/Area.txt")
	file = open(file_path, "w")
	
	try:
		content = "rectangle = (%s,\t%s)\nexceptions = %s" % (tBL, tTR, exceptions)
		print content
		file.write(content)
	finally:
		file.close()


def exportPlotList():
	area = worldBuilder.TempInfo[:]
	if not area:
		return
		
	file_path = "%s/%s/%s" % (path.getModDir(), MAPS_PATH, "Export/PlotList.txt")
	file = open(file_path, "w")
	
	try:
		content = "plotList = %s" % (area,)
		print content
		file.write(content)
	finally:
		file.close()


def importArea(area):
	worldBuilder.TempInfo = [location(p) for p in area]
	worldBuilder.showAreaExportOverlay()


def importRectangle(tCorners):
	importArea(plots.rectangle(*tCorners))
	
		
### Specific marker functions ###

def markCapitals():
	createCivLandmarks(dCapitals)


def markLocationTiles():
	for name, value in Locations.__dict__.items():
		if name.startswith("_"):
			continue
		
		if isinstance(value, tuple) and len(value) == 2 and all(isinstance(item, int) for item in value):
			createLandmark(value, name)


def markLocationAreas():
	for name, value in Locations.__dict__.items():
		if name.startswith("_"):
			continue
		
		if isinstance(value, tuple) and len(value) == 2 and all(isinstance(item, tuple) for item in value):
			area = plots.rectangle(*value)
			paintArea(area)
			
			tBL, tTR = getCorners(area)
			createLandmark(tBL, name)
			createLandmark(tTR, name)