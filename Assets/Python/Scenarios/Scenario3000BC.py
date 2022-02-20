from Scenario import *
from Core import *


lCivilizations = [
	Civilization(
		iEgypt,
		lCivics = [iMonarchy, iRedistribution, iDeification]
	),
	Civilization(
		iBabylonia
	),
	Civilization(
		iHarappa
	),
	Civilization(
		iCelts
	),
	Civilization(
		iNative
	),
	Civilization(
		iIndependent
	),
	Civilization(
		iIndependent2
	),
]


scenario3000BC = Scenario(
	iStartYear = -3000,
	fileName = "RFC_3000BC",
	
	lCivilizations = lCivilizations,
)
