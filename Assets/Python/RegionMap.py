from Consts import *
from RFCUtils import utils

(iNone, iMinority, iPeriphery, iHistorical, iCore) = range(5)

def getMapValue(tRegionMap, x, y):
	return tRegionMap[iWorldY-1-y][x]
	
def getSpreadFactor(iReligion, x, y):
	iRegion = gc.getMap().plot(x, y).getRegionID()
	if iRegion < 0: return -1
	
	for iFactor in tSpreadFactors[iReligion].keys():
		if iRegion in tSpreadFactors[iReligion][iFactor]:
			return iFactor
	
	return iNone
	
def updateRegionMap():
	tRegionMap = utils.readNumberMap('Regions')

	for x in range(iWorldX):
		for y in range(iWorldY):
			gc.getMap().plot(x, y).setRegionID(getMapValue(tRegionMap, x, y))
			
	gc.getMap().recalculateAreas()

def updateReligionSpread(iReligion):
	for x in range(iWorldX):
		for y in range(iWorldY):
			gc.getMap().plot(x, y).setSpreadFactor(iReligion, getSpreadFactor(iReligion, x, y))
				
def init():
	updateRegionMap()
	for iReligion in range(iNumReligions):
		updateReligionSpread(iReligion)


tSpreadFactors = (
# Judaism
{
	iMinority :	[rMaghreb, rEgypt, rNubia, rEthiopia, rLevant, rMesopotamia, rPersia, rKhorasan, rCaucasus, rAnatolia, rBalkans, rItaly, rIberia, rCentralEurope, rPoland, rLowerGermany, rFrance, rRuthenia, rPonticSteppe, rBritain, rAtlanticSeaboard, rMidwest, rMaritimes, rOntario, rCalifornia],
},
# Orthodoxy
{
	iCore :		[rRuthenia, rEthiopia, rGreece, rCaucasus],
	iHistorical : 	[rBalkans, rAnatolia, rLevant, rMesopotamia, rEgypt, rNubia, rEuropeanArctic, rUrals, rSiberia],
	iPeriphery : 	[rMaghreb, rItaly, rPonticSteppe, rCaucasus, rAmericanArctic, rCentralAsianSteppe],
	iMinority :	[rBaltics],
},
# Catholicism
{
	iCore :		[rFrance, rCentralEurope, rPoland, rIreland, rItaly, rIberia],
	iHistorical :	[rBritain, rScandinavia, rLowerGermany, rQuebec, rMaritimes, rAtlanticSeaboard, rCaribbean, rAridoamerica, rMesoamerica, rCentralAmerica, rNewGranada, rAndes, rAmazonia, rBrazil, rSouthernCone, rCape, rPhilippines],
	iPeriphery :	[rBalkans, rGreece, rAmericanArctic, rOntario, rMidwest, rDeepSouth, rGreatPlains, rCalifornia, rAustralia, rOceania, rGuinea, rCongo, rSwahiliCoast, rMadagascar],
},
# Protestantism
{
	iCore :		[rBritain, rLowerGermany, rScandinavia, rAtlanticSeaboard, rMidwest, rOntario, rGreatPlains, rDeepSouth, rMaritimes],
	iHistorical :	[rCalifornia, rCascadia, rAmericanArctic, rAustralia],
	iPeriphery :	[rOceania, rCape, rZambezi],
	iMinority : 	[rFrance, rPoland, rCentralEurope, rBrazil, rKorea]
},
# Islam
{
	iCore : 	[rArabia, rMesopotamia, rEgypt],
	iHistorical : 	[rPersia, rKhorasan, rSindh, rPunjab, rTransoxiana, rMaghreb, rIndonesia, rSahel, rSahara, rHornOfAfrica],
	iPeriphery : 	[rNubia, rIberia, rAnatolia, rBalkans, rHindustan, rRajputana, rBengal, rDeccan, rPonticSteppe, rCentralAsianSteppe, rSwahiliCoast],
	iMinority : 	[rUrals, rSiberia, rCaucasus, rTarimBasin, rMongolia],
},
# Hinduism
{
	iCore : 	[rHindustan, rPunjab, rSindh, rRajputana, rDeccan, rBengal, rDravida],
	iHistorical : 	[rIndochina, rIndonesia, rPhilippines],
},
# Buddhism
{
	iCore : 	[rHindustan, rRajputana, rBengal, rTibet, rIndochina],
	iHistorical : 	[rDeccan, rDravida, rPunjab, rSindh, rTarimBasin, rMongolia, rNorthChina, rSouthChina, rKorea, rJapan, rIndonesia, rKhorasan],
	iMinority :	[rTransoxiana],
},
# Confucianism
{
	iCore : 	[rNorthChina, rSouthChina, rManchuria],
	iHistorical :	[rKorea],
	iPeriphery : 	[rMongolia, rTibet],
	iMinority : 	[rJapan, rIndonesia, rIndochina, rAustralia],
},
# Taoism
{
	iCore : 	[rNorthChina, rSouthChina],
	iHistorical : 	[rManchuria],
	iPeriphery : 	[rTibet, rMongolia],
},
# Zoroastrianism
{
	iCore :		[rPersia],
	iPeriphery : 	[rKhorasan, rMesopotamia],
	iMinority : 	[rSindh, rRajputana],
},
)