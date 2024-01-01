from Scenario import *
from Core import *


lCivilizations = [
	Civilization(
		iEgypt,
		lCivics=[iMonarchy, iRedistribution, iDeification],
		techs=techs.of(iMining, iPottery, iAgriculture, iMythology)
	),
	Civilization(
		iBabylonia,
		techs=techs.of(iPottery, iPastoralism, iAgriculture, iMythology)
	),
	Civilization(
		iHarappa,
		techs=techs.of(iMining, iPottery, iAgriculture, iSailing)
	),
	Civilization(
		iNative,
		techs=techs.of(iTanning, iMythology)
	),
	Civilization(
		iCelts
	),
	Civilization(
		iIndependent2
	),
	Civilization(
		iIndependent
	),
]

lTribalVillages = [
	((121, 42), (129, 48)), # South China
	((71, 56), (78, 61)), # Balkans
	((80, 51), (87, 55)), # Anatolia
]


scenario3000BC = Scenario(
	iStartYear = -3000,
	fileName = "RFC_3000BC",
	
	lCivilizations = lCivilizations,
	lTribalVillages = lTribalVillages,
)
