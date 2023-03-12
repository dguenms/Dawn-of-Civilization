# coding: utf-8

from Core import *
from Areas import *
from Files import *
from CityNames import *

import Locations

from CvScreensInterface import worldBuilderScreen as worldBuilder
from CvPlatyBuilderScreen import CvWorldBuilderScreen

import os
import csv


engine = CyEngine()


### Generic Landmark Functions ###

def createLandmark(tile, label):
	engine.addLandmark(plot(tile), label.encode("latin-1", "xmlcharrefreplace"))


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
			yield sign.getPlot(), sign.getCaption()


def exportLandmarks():
	file = open(getPath("Export/Landmarks.txt"), "w")
	
	try:
		for plot, caption in getLandmarks():
			content = '"%s":\t\t%s\n' % (caption, location(plot))
			print content
			file.write(content)
	finally:
		file.close()


def exportCityNames():
	city_names.update(((location(p), name) for p, name in getLandmarks()))
	city_names.export()


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

	file = open(getPath("Export/Area.txt"), "w")
	
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
		
	file = open(getPath("Export/PlotList.txt"), "w")
	
	try:
		content = "plotList = %s" % (area,)
		print content
		file.write(content)
	finally:
		file.close()


def exportCSV():
	area = worldBuilder.TempInfo[:]
	if not area:
		return
	
	map = FileMap("ExportedArea.csv")
	
	values = [(location(p), str(value)) for p, value in FileMap.read("Export/BaseMap.csv")] + [(tile, "1") for tile in area]
	
	map.update(values)
	map.export()


def importArea(area):
	worldBuilder.TempInfo = [location(p) for p in area]
	worldBuilder.showAreaExportOverlay()


def importRectangle(tCorners):
	importArea(plots.rectangle(*tCorners))


def exportBaseTerrain():
	map = FileMap("BaseTerrain.csv")

	def terrain(p):
		if p.isWater():
			return 1
		elif p.Peak():
			return 2
		else:
			return 0
	
	values = [(location(p), terrain(p)) for p in plots.all()]
	
	map.update(values)
	map.export()
	

def exportBaseSettlerMap():
	map = FileMap("BaseMap.csv")
	
	def terrain(p):
		if p.isWater():
			return ""
		else:
			return "0"
	
	values = [(location(p), terrain(p)) for p in plots.all()]
	
	map.update(values)
	map.export()


def markUnnamedTiles():
	for (x, y), name in city_names:
		p = plot(x, y)
		
		if name == "?":
			if player(0).canFound(x, y):
				createLandmark((x, y), "Unnamed")


def markCityNames():
	for (x, y), name in city_names:
		if name in ["^", "?"]:
			continue
		
		createLandmark((x, y), name)
				
		
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