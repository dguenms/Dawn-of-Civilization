from CvPythonExtensions import *
from Consts import *
from RFCUtils import utils

import csv

BASE_PATH = 'D:\DoC Maps\%s.csv'

def convertMap(value):
	rows = []

	for y in reversed(range(iWorldY)):
		row = []
		for x in range(iWorldX):
			plot = gc.getMap().plot(x, y)
			row.append(value(plot))
		rows.append(row)
		
	return rows

def printMap(rows, name):
	file = open(BASE_PATH % name, 'wb')
	
	try:
		writer = csv.writer(file)
		for row in rows:
			writer.writerow(row)
	finally:
		file.close()
		

def landOrWater(plot):
	if plot.isWater() or plot.isPeak():
		return ''
		
	return 0