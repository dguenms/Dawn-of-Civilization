## CityUtil
##
## Collection of utility functions for dealing with cities.
##
## Copyright (c) 2009 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *


## Globals

gc = CyGlobalContext()


## Growth and Starvation

def willGrowThisTurn(city):
	"""
	Returns True if <city> will increase its population due to growth this turn.
	
	Emphasize No Growth must be off for the city, and its food rate plus storage must reach the growth threshold.
	"""
	return not city.AI_isEmphasize(5) and city.getFood() + city.foodDifference(True) >= city.growthThreshold()

def willShrinkThisTurn(city):
	"""
	Returns True if <city> will decrease its population due to starvation this turn.
	
	It must have at least two population, and its food rate plus storage must be negative.
	"""
	return city.getPopulation() > 1 and city.getFood() + city.foodDifference(True) < 0
