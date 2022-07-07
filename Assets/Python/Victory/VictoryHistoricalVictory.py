from VictoryDefinitions import *
from Locations import *+


BABYLON = "TXT_KEY_VICTORY_NAME_BABYLON"


dGoals = {
	iEgypt: (
		CultureAmount(500, at=-850),
		Wonders(iPyramids, iGreatLibrary, iGreatLighthouse, by=-100),
		CultureAmount(5000, at=100),
	),
	iBabylonia: (
		FirstDiscover(iConstruction, iArithmetics, iWriting, iCalendar, iContract),
		BestPopulationCity(city(tBabylon).named(BABYLON), at=-850),
		BestCultureCity(city(tBabylon).named(BABYLON), at=-700),
	),
}