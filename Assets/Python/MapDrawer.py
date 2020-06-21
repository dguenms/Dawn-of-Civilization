# Leoreth: this should be changed to work off civs instead of players

from CvPythonExtensions import *
from Core import *
from SettlerMaps import *
from RFCUtils import *
import csv

IMAGE_LOCATION = "D:\DoC Maps"

DISPLAY_FOREIGN_CORE = False
DISPLAY_CONTESTED = True

(LAND, WATER, PEAK, CORE, HISTORICAL, CONTESTED, FOREIGN, FOREIGN_CORE, FLIPZONE) = range(9)

gc = CyGlobalContext()

def createMaps():
	for iPlayer in players.major():
		createMap(iPlayer, 0)
		if civ(iPlayer) in dRebirth:
			createMap(iPlayer, 1)
			
	print 'Maps Created'
			
def createMap(iPlayer, iReborn):
	iCivilization = civ(iPlayer)
	if iReborn == 1: iCivilization = dRebirthCiv[iCivilization]
	sName = infos.civ(iCivilization).getShortDescription(0)
	
	file = open(IMAGE_LOCATION + "\Stability\\" + sName, 'wt')

	lCorePlots = plots.core(iCivilization)
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
	
	lFlipzonePlots = plots.birth(iCivilization)
		
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
		lExtendedCorePlots = plots.core(iPlayer)
		
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
	iSpawnDate = dBirth[iPlayer]
	if iReborn == 1: iSpawnDate = dRebirth[iPlayer]
	
	for iLoopPlayer in players.major().without(iPlayer):
		if canEverRespawn(iLoopPlayer, year(iSpawnDate)) or dBirth[iLoopPlayer] > iSpawnDate:
			for plot in plots.core(iLoopPlayer):
				if not location(plot) in lForeignCorePlots:
					lForeignCorePlots.append(location(plot))
						
	return lForeignCorePlots