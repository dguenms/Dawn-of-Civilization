# coding: utf-8

from Core import *
from Areas import *
from Files import *
from CityNames import *
from Resources import *

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


def removeLandmarks():
	for plot, caption in getLandmarks():
		engine.removeLandmark(plot)


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
	
	values = [(location(p), "0") for p, value in FileMap.read("Export/BaseTerrain.csv") if value > 0] + [(tile, "1") for tile in area] + [(location(p), str(value)) for p, value in getLandmarks()]
	
	map.update(values)
	map.export()


def importArea(area):
	worldBuilder.TempInfo = [location(p) for p in area]
	worldBuilder.showAreaExportOverlay()


def importRectangle(tCorners):
	importArea(plots.rectangle(*tCorners))


def importCore(iCiv):
	importArea(plots.core(iCiv))


def importMap(path, iCiv):
	area = [tile for tile, value in FileMap.read("%s/%s.csv" % (path, civ_name(iCiv))) if value and not plot(tile).isWater()]
	importArea(area)
	
	landmarks = dict((tile, str(value)) for tile, value in FileMap.read("%s/%s.csv" % (path, civ_name(iCiv))) if int(value) > 1)
	createLandmarks(landmarks)


def importSettlerMap(iCiv):
	importMap("Settler", iCiv)


def importWarMap(iCiv):
	importMap("War", iCiv)
	

def showSettlerValues(iCiv):
	values = dict((p, p.getSettlerValue(iCiv)) for p in plots.all().land() if p.getSettlerValue(iCiv) > 0)
	importArea(values.keys())
	createLandmarks(dict((key, str(value)) for key, value in values.items() if value > 1))


def clearMap(iIndex=1000):
	removeLandmarks()
	engine.clearAreaBorderPlots(iIndex)


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


def markResource(iResource):
	name = infos.bonus(iResource).getText()
	
	for p in plots.all():
		if p.getBonusType(-1) == iResource:
			if p.getBonusVarietyType(-1) != -1:
				createLandmark(p, infos.bonus(p.getBonusVarietyType(-1)).getText())
			else:
				createLandmark(p, name)


def markResourceSpawns(iResource):
	name = infos.bonus(iResource).getText()
	
	for tile, (iYear, iResourceSpawn) in dResourcesDict.items():
		if iResource == iResourceSpawn:
			createLandmark(tile, "%s %s" % (name, iYear))


def markAllResourceSpawns():
	for iResource in range(iNumBonuses):
		markResourceSpawns(iResource)


def markTerrainSpawns():
	for tile, (iYear, iResource) in dResourcesDict.items():
		createLandmark(tile, "%s %s" % (infos.bonus(iResource).getText(), iYear))
	
	for tile, (iCiv, iResource) in dSpawnResourcesDict.items():
		createLandmark(tile, "%s %s start" % (infos.bonus(iResource).getText(), infos.civ(iCiv).getShortDescription(0)))
	
	for tile, iYear in dRemovedResourcesDict.items():
		iResource = plot(tile).getBonusType(-1)
		createLandmark(tile, iResource >= 0 and "(%s %s)" % (infos.bonus(iResource).getText(), iYear) or "(%s)" % iYear)
	
	for tile, (iYear, iFeature) in dFeaturesDict.items():
		createLandmark(tile, "%s %s" % (infos.feature(iFeature).getText(), iYear))
	
	for tile, iYear in dRemovedFeaturesDict.items():
		iFeature = plot(tile).getFeatureType()
		createLandmark(tile, iFeature >= 0 and "(%s %s)" % (infos.feature(iFeature).getText(), iYear) or "(%s)" % iYear)
	
	for tile, (iCiv, iPlotType) in dConquerorPlotTypesDict.items():
		createLandmark(tile, "%s %s conquerors" % (iPlotType, infos.civ(iCiv).getShortDescription(0)))


def markRegions():
	for plot in plots.all():
		createLandmark(plot, str(plot.getRegionID()))


def listResources():
	global_resources = defaultdict(default=0)
	global_spawns = defaultdict(default=0)
	
	regions = list(range(iNumRegions)) + list(range(100, 100 + iNumWaterRegions))
	
	region_resources = dict((iRegion, defaultdict(default=0)) for iRegion in regions)
	region_spawns = dict((iRegion, defaultdict(default=0)) for iRegion in regions)
	
	resource_regions = dict((iResource, defaultdict(default=0)) for iResource in range(iNumBonuses))
	spawn_regions = dict((iResource, defaultdict(default=0)) for iResource in range(iNumBonuses))
	
	for p in plots.all():
		iResource = p.getBonusType(-1)
		iRegion = p.getRegionID()
		
		if iResource >= 0:
			global_resources[iResource] += 1
			
			if iRegion >= 0:
				region_resources[iRegion][iResource] += 1
				resource_regions[iResource][iRegion] += 1
	
	for tile, (_, iResource) in dResourcesDict.items():
		global_spawns[iResource] += 1
		region_spawns[plot(tile).getRegionID()][iResource] += 1
		spawn_regions[iResource][plot(tile).getRegionID()] += 1
	
	for tile, (_, iResource) in dSpawnResourcesDict.items():
		global_spawns[iResource] += 1
		region_spawns[plot(tile).getRegionID()][iResource] += 1
		spawn_regions[iResource][plot(tile).getRegionID()] += 1
	
	for tile in dRemovedResourcesDict.keys():
		iResource = plot(tile).getBonusType(-1)
		if iResource >= 0:
			global_spawns[iResource] -= 1
			region_spawns[plot(tile).getRegionID()][iResource] -= 1
			spawn_regions[iResource][plot(tile).getRegionID()] -= 1
	
	lines = []
	
	lines.append("TOTAL RESOURCES\n")
	
	for iResource in range(iNumBonuses):
		iResources = global_resources.get(iResource, 0)
		iSpawns = global_spawns.get(iResource, 0)
		
		if iResources > 0 or iSpawns != 0:
			if iSpawns != 0:
				lines.append(" * %s: %d (%s%d)\n" % (infos.bonus(iResource).getText(), iResources, iSpawns > 0 and "+" or "", iSpawns))
			else:
				lines.append(" * %s: %d\n" % (infos.bonus(iResource).getText(), iResources))
	
	for iResource in range(iNumBonuses):
		resource_lines = []
		
		for iRegion in regions:
			iResourceRegions = resource_regions[iResource].get(iRegion, 0)
			iSpawnRegions = spawn_regions[iResource].get(iRegion, 0)
			
			if iResourceRegions > 0 or iSpawnRegions != 0:
				if iSpawnRegions != 0:
					resource_lines.append(" * %s: %d (%s%d)\n" % (text("TXT_KEY_REGION_%d" % iRegion), iResourceRegions, iSpawnRegions > 0 and "+" or "", iSpawnRegions))
				else:
					resource_lines.append(" * %s: %d\n" % (text("TXT_KEY_REGION_%d" % iRegion), iResourceRegions))
		
		if resource_lines:
			lines.append("\n")
			lines.append(infos.bonus(iResource).getText().upper() + "\n")
			lines += resource_lines
	
	for iRegion in regions:
		region_lines = []
	
		for iResource in range(iNumBonuses):
			iResources = region_resources[iRegion].get(iResource, 0)
			iSpawns = region_spawns[iRegion].get(iResource, 0)
			
			if iResources > 0 or iSpawns != 0:
				if iSpawns != 0:
					region_lines.append(" * %s: %d (%s%d)\n" % (infos.bonus(iResource).getText(), iResources, iSpawns > 0 and "+" or "", iSpawns))
				else:
					region_lines.append(" * %s: %d\n" % (infos.bonus(iResource).getText(), iResources))
		
		if region_lines:
			lines.append("\n")
			lines.append(text("TXT_KEY_REGION_%d" % iRegion).upper() + "\n")
			lines += region_lines
	
	file = open(getPath("Export/Resources.txt"), "w")
	
	try:
		file.writelines(lines)
	finally:
		file.close()
				
		
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