from Core import *
from Areas import *

import BugPath as path
import csv


engine = CyEngine()

MAPS_PATH = "Assets/Maps"


### Generic Landmark Functions ###

def createLandmarks(dLandmarks):
	for tile, label in dLandmarks.items():
		engine.addLandmark(plot(tile), label.encode("latin-1"))


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
			file.write(content)
	finally:
		file.close()
		
		
### Specific marker functions ###

def markCapitals():
	dBirthPlots = dict((tile, infos.civ(iCiv).getShortDescription(0)) for iCiv, tile in dCapitals.items())
	createLandmarks(dBirthPlots)