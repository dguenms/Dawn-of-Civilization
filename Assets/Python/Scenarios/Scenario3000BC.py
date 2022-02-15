from Civilizations import initScenarioTechs
from Core import *


class Scenario(object):
	
	iStartYear = -3000
	lInitialCivs = [iEgypt, iBabylonia, iHarappa]
	fileName = "RFC_3000BC"
	
	@staticmethod
	def initScenario():
		initScenarioTechs()
