from Core import *
from Maps import Map
from Events import handler

iNumReligionMapTypes = 5
(iNone, iMinority, iPeriphery, iHistorical, iCore) = range(iNumReligionMapTypes)

def getSpreadFactor(iReligion, plot):
	iRegion = plot.getRegionID()
	if iRegion < 0: 
		return -1
	
	return next((iFactor for iFactor, lRegions in tSpreadFactors[iReligion].items() if iRegion in lRegions), iNone)
	
def updateRegionMap():
	for (x, y), iRegion in Map.read("Regions.csv"):
		plot(x, y).setRegionID(iRegion)

	map.recalculateAreas()
			
def updateReligionSpread(iReligion):
	for plot in plots.all():
		plot.setSpreadFactor(iReligion, getSpreadFactor(iReligion, plot))

def init():
	updateRegionMap()
	for iReligion in range(iNumReligions):
		updateReligionSpread(iReligion)
				

# TODO: revisit
tSpreadFactors = (
# Judaism
{
	iMinority :	[rBritain, rFrance, rIberia, rItaly, rLowerGermany, rCentralEurope, rBalkans, rGreece, rPoland, rRuthenia, rLevant, rMesopotamia, rAnatolia, rCaucasus, rArabia, rEgypt, rMaghreb, rPersia, rEthiopia, rAtlanticSeaboard, rMidwest, rCalifornia, rOntario, rQuebec, rMaritimes]
},
# Orthodoxy
{
	iCore :		[rRuthenia, rEthiopia, rGreece, rCaucasus],
	iHistorical : 	[rBalkans, rAnatolia, rLevant, rMesopotamia, rEgypt, rNubia, rEuropeanArctic, rUrals, rSiberia],
	iPeriphery : 	[rMaghreb, rItaly, rPonticSteppe, rAmericanArctic, rCentralAsianSteppe],
	iMinority :	[rBaltics, rPoland, rPersia, rKhorasan, rTransoxiana, rTarimBasin, rNorthChina],
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
	iPeriphery :	[rFrance, rOceania, rCape, rZambezi],
	iMinority : 	[rPoland, rCentralEurope, rBrazil, rKorea]
},
# Islam
{
	iCore : 	[rArabia, rMesopotamia, rEgypt, rLevant],
	iHistorical : 	[rPersia, rKhorasan, rSindh, rPunjab, rTransoxiana, rMaghreb, rIndonesia, rSahel, rSahara, rHornOfAfrica],
	iPeriphery : 	[rNubia, rIberia, rAnatolia, rBalkans, rHindustan, rRajputana, rBengal, rDeccan, rPonticSteppe, rCentralAsianSteppe, rSwahiliCoast],
	iMinority : 	[rUrals, rSiberia, rCaucasus, rTarimBasin, rMongolia],
},
# Hinduism
{
	iCore : 	[rHindustan, rRajputana, rDeccan, rBengal, rDravida],
	iHistorical : 	[rPunjab, rSindh, rIndochina, rIndonesia, rPhilippines],
},
# Buddhism
{
	iCore : 	[rHindustan, rRajputana, rBengal, rTibet, rIndochina],
	iHistorical : 	[rDeccan, rDravida, rPunjab, rSindh, rTarimBasin, rMongolia, rNorthChina, rSouthChina, rKorea, rJapan, rIndonesia, rKhorasan],
	iMinority :	[rTransoxiana, rKhorasan],
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
	iPeriphery : 	[rKhorasan, rMesopotamia, rTransoxiana, rLevant],
	iMinority : 	[rSindh, rRajputana],
},
)