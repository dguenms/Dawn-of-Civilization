from CvPythonExtensions import *
from Consts import *
from RFCUtils import utils

import csv

def convertMap(value):
	rows = []

	for y in reversed(range(iWorldY)):
		row = []
		for x in range(iWorldX):
			plot = gc.getMap().plot(x, y)
			row.append(value(plot))
		rows.append(row)
		
	return rows
	
def retrieveSigns():
	dSigns = {}
	
	engine = CyEngine()
	for iSign in range(engine.getNumSigns()):
		sign = engine.getSignByIndex(iSign)
		plot = sign.getPlot()
		iPlayer = sign.getPlayerType()
		caption = sign.getCaption()
		
		if iPlayer == -1:
			x, y = plot.getX(), plot.getY()
			dSigns[(x, y)] = caption.encode('latin-1')
			
	def sign(plot):
		x, y = plot.getX(), plot.getY()
		if (x, y) in dSigns: return dSigns[(x, y)]
		return ''
		
	return convertMap(sign)
	
def placeSigns(rows):
	engine = CyEngine()
	for y in range(len(rows)):
		row = rows[y]
		for x in range(len(row)):
			caption = row[x]
			if caption:
				engine.addLandmark(gc.getMap().plot(x, iWorldY-1-y), caption)

def saveCityNames():
	current = utils.readMap('Cities')
	updated = retrieveSigns()
	
	utils.writeMap(updated, 'CitiesDiff')
	
	for y in range(min(iWorldY, len(current))):
		row = current[y]
		for x in range(min(iWorldX, len(row))):
			if not updated[y][x]:
				updated[y][x] = row[x]
	
	utils.writeMap(updated, 'Cities')
	
def loadCityNames():
	rows = utils.readMap('Cities')
	placeSigns(rows)

def landOrWater(plot):
	if plot.isWater() or plot.isPeak():
		return ''
		
	return 0