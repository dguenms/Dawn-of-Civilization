from CvPythonExtensions import *
from Consts import *
import Areas
from SettlerMaps import *
from RFCUtils import *
import csv

IMAGE_LOCATION = "D:\DoC Maps"

DISPLAY_FOREIGN_CORE = False
DISPLAY_CONTESTED = True

(LAND, WATER, PEAK, CORE, HISTORICAL, CONTESTED, FOREIGN, FOREIGN_CORE, FLIPZONE) = range(9)

gc = CyGlobalContext()

def createMaps():
	for iPlayer in range(iNumPlayers):
		createMap(iPlayer, 0)
		if civ(iPlayer) in dRebirth:
			createMap(iPlayer, 1)
			
	print 'Maps Created'
			
def createMap(iPlayer, iReborn):
	iCivilization = player(iPlayer).getCivilizationType()
	if iReborn == 1: iCivilization = dRebirthCiv[iCivilization]
	sName = infos.civ(iCivilization).getShortDescription(0)
	
	file = open(IMAGE_LOCATION + "\Stability\\" + sName, 'wt')

	lCorePlots = Areas.getCoreArea(iCivilization)
	lForeignCorePlots = getForeignCorePlots(iPlayer, iReborn)
	
	try:
		writer = csv.writer(file)
		for y in reversed(range(iWorldY)):
			lRow = []
			for x in range(iWorldX):
				plot = plot_(x, y)
				iSettlerValue = getMapValue(iPlayer, (x, y))
				bForeignCore = ((x, y) in lForeignCorePlots)
			
				if plot.isWater(): lRow.append(WATER)
				elif plot.isPeak(): lRow.append(PEAK)
				elif (x, y) in lCorePlots: lRow.append(CORE)
				elif iSettlerValue >= 90 and (not bForeignCore or not DISPLAY_CONTESTED): lRow.append(HISTORICAL)
				elif iSettlerValue >= 90 and bForeignCore: lRow.append(CONTESTED)
				elif iSettlerValue < 90 and (not bForeignCore or not DISPLAY_FOREIGN_CORE): lRow.append(FOREIGN)
				elif iSettlerValue < 90 and bForeignCore: lRow.append(FOREIGN_CORE)
				else: lRow.append(LAND)
			writer.writerow(lRow)
	finally:
		file.close()
		
	file = open(IMAGE_LOCATION + "\Spawns\\" + sName, 'wt')
	
	lFlipzonePlots = Areas.getBirthArea(iCivilization)
		
	try:
		writer = csv.writer(file)
		writer.writerow((player(iPlayer).getPlayerTextColorR(), player(iPlayer).getPlayerTextColorG(), player(iPlayer).getPlayerTextColorB()))
		
		for y in reversed(range(iWorldY)):
			lRow = []
			for x in range(iWorldX):
				plot = plot_(x, y)
				if plot.isWater(): lRow.append(0)
				elif (x, y) in lFlipzonePlots: lRow.append(1)
				else: lRow.append(0)
			writer.writerow(lRow)
	finally:
		file.close()
		
	file = open(IMAGE_LOCATION + "\ExtendedCores\\" + sName, 'wt')
	
	# TODO: respect periods here
	"""
	lExtendedCorePlots = []
	
	if iReborn == 0 and civ(iPlayer) in dRebirth:
		lExtendedCorePlots = Areas.getCoreArea(iPlayer, True)
		
	try:
		writer = csv.writer(file)
		
		for y in reversed(range(iWorldY)):
			lRow = []
			for x in range(iWorldX):
				plot = plot_(x, y)
				if (x, y) in lExtendedCorePlots and (x, y) not in lCorePlots and not plot.isWater(): lRow.append(1)
				else: lRow.append(0)
			writer.writerow(lRow)
	finally:
		file.close()
	"""
			
			
def getForeignCorePlots(iPlayer, iReborn):
	lForeignCorePlots = []
	iSpawnDate = dBirth[civ(iPlayer)]
	if iReborn == 1: iSpawnDate = dRebirth[civ(iPlayer)]
	
	for iLoopPlayer in range(iNumPlayers):
		if iLoopPlayer != iPlayer:
			if canEverRespawn(iLoopPlayer, year(iSpawnDate)) or dBirth[civ(iLoopPlayer)] > iSpawnDate:
				for tPlot in Areas.getCoreArea(civ(iLoopPlayer)):
					if not tPlot in lForeignCorePlots:
						lForeignCorePlots.append(tPlot)
						
	return lForeignCorePlots