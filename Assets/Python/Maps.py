from Core import *
from Areas import *

import Locations

from CvScreensInterface import worldBuilderScreen as worldBuilder

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


def paintPlots(lPlots, index=1000, color="COLOR_CYAN"):
	engine.clearAreaBorderPlots(index)
	for (x, y) in lPlots:
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


def exportArea():
	area = worldBuilder.TempInfo[:]
	if not area:
		return
	
	min_x = min(t[0] for t in area)
	min_y = min(t[1] for t in area)
	max_x = max(t[0] for t in area)
	max_y = max(t[1] for t in area)
	
	exceptions = [location(p) for p in plots.rectangle((min_x, min_y), (max_x, max_y)) if location(p) not in area and not p.isWater()]

	file_path = "%s/%s/%s" % (path.getModDir(), MAPS_PATH, "Export/Area.txt")
	file = open(file_path, "w")
	
	try:
		content = "rectangle = %s\nexceptions = %s" % (((min_x, min_y), (max_x, max_y)), exceptions)
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
	
		
### Specific marker functions ###

def markCapitals():
	createCivLandmarks(dCapitals)