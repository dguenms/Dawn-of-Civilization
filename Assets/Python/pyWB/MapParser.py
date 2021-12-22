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
		print "MapParser read"
		fileName = os.path.normpath(fileName)
		fileName, ext = os.path.splitext(fileName)
		
		if not ext:
			ext = getWBSaveExtension()
		
		print "fileName=%s, ext=%s" % (fileName, ext)
		
		if not os.path.isfile(fileName + ext):
			print "abort: not file"
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
			print "abort: wrong version"
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
		print "done mapparser read"
		return 0
	
	def prepare(self):
		print "Create game"
		self.gameDesc.apply()
		
		print "Rebuild map"
		worldSizeType = CvUtil.findInfoTypeNum(gc.getWorldInfo, gc.getNumWorldInfos(), self.mapDesc.worldSize)
		climateType = CvUtil.findInfoTypeNum(gc.getClimateInfo, gc.getNumClimateInfos(), self.mapDesc.climate)
		seaLevelType = CvUtil.findInfoTypeNum(gc.getSeaLevelInfo, gc.getNumSeaLevelInfos(), self.mapDesc.seaLevel)
		map.rebuild(self.mapDesc.iGridW, self.mapDesc.iGridH, self.mapDesc.iPrimeMeridian, self.mapDesc.iEquator, self.mapDesc.iTopLatitude, self.mapDesc.iBottomLatitude, self.mapDesc.bWrapX, self.mapDesc.bWrapY, WorldSizeTypes(worldSizeType), ClimateTypes(climateType), SeaLevelTypes(seaLevelType), 0, None)
	
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
		
		print "Apply plots"
		for plotDesc in self.plotDesc:
			plotDesc.apply()
		
		return 0
		
		
		
		
		
		
		
		
		
		
		
		
		
		