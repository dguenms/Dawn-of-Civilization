from CvWBDesc import *
from Core import *


class MapParser:

	def __init__(self):
		self.gameDesc = CvGameDesc()
		self.mapDesc = CvMapDesc()
		self.lPlotDescs = []
	
	def getVersion(self):
		return version
	
	def getDescFileName(self, fileName):
		return fileName + getWBSaveExtension()
		
	def read(self, fileName):
		fileName = os.path.normpath(fileName)
		fileName, ext = os.path.splitext(fileName)
		
		if not ext:
			ext = getWBSaveExtension()
		
		if not os.path.isfile(fileName + ext):
			return -1
		
		f = file(fileName + ext, "r")
		
		parser = CvWBParser()
		position = f.tell()
		
		line = parser.getNextLine(f)
		if line.find("Platy") > -1:
			iNumPlayers = gc.getMAX_PLAYERS()
			iNumTeams = gc.getMAX_TEAMS()
		else:
			f.seek(position)
		
		position = f.tell()
		line = parser.getNextLine(f)
		f.seek(position)
		
		version = int(parser.findNextTokenValue(f, "Version"))
		if version != self.getVersion():
			return -1
		
		self.gameDesc.read(f)
		self.mapDesc.read(f)
		
		for _ in range(self.mapDesc.numPlotsWritten):
			plotDesc = CvPlotDesc()
			if plotDesc.read(f):
				self.lPlotDescs.append(plotDesc)
			else:
				break
		
		f.close()
		return 0
	
	def prepare(self):
		self.gameDesc.apply()
		
		worldSizeType = CvUtil.findInfoTypeNum(gc.getWorldInfo, gc.getNumWorldInfos(), self.mapDesc.worldSize)
		climateType = CvUtil.findInfoTypeNum(gc.getClimateInfo, gc.getNumClimateInfos(), self.mapDesc.climate)
		seaLevelType = CvUtil.findInfoTypeNum(gc.getSeaLevelInfo, gc.getNumSeaLevelInfos(), self.mapDesc.seaLevel)
		iNumCustomMapOptions = map.getNumCustomMapOptions()
		map.rebuild(self.mapDesc.iGridW, self.mapDesc.iGridH, self.mapDesc.iPrimeMeridian, self.mapDesc.iEquator, self.mapDesc.iTopLatitude, self.mapDesc.iBottomLatitude, self.mapDesc.bWrapX, self.mapDesc.bWrapY, WorldSizeTypes(worldSizeType), ClimateTypes(climateType), SeaLevelTypes(seaLevelType), iNumCustomMapOptions, None)
	
	def applyPlotTypes(self):
		for plotDesc in self.lPlotDescs:
			plotDesc.applyPlotType()
		
		map.recalculateAreas()
	
	def applyTerrainTypes(self):
		for plotDesc in self.lPlotDescs:
			plotDesc.applyTerrainType()
	
	def applyFeatures(self):
		for plotDesc in self.lPlotDescs:
			plotDesc.applyFeature()
	
	def applyBonuses(self):
		for plotDesc in self.lPlotDescs:
			plotDesc.applyBonus()
	
	def applyRivers(self):
		for plotDesc in self.lPlotDescs:
			plotDesc.applyRivers()
	
	def applyMap(self):
		self.prepare()
		self.applyPlotTypes()
		self.applyTerrainTypes()
		
		for plotDesc in self.plotDesc:
			plotDesc.apply()
		
		return 0
