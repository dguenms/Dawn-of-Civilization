from Core import *
from Events import handler

iNumReligionMapTypes = 5
(iNone, iMinority, iPeriphery, iHistorical, iCore) = range(iNumReligionMapTypes)

def getMapValue(x, y):
	return tRegionMap[iWorldY-1-y][x]
	
def getSpreadFactor(iReligion, (x, y)):
	iRegion = plot(x, y).getRegionID()
	if iRegion < 0: return -1
	
	for iFactor in tSpreadFactors[iReligion].keys():
		if iRegion in tSpreadFactors[iReligion][iFactor]:
			return iFactor
	
	return iNone
	
def updateRegionMap():
	for plot in plots.all():
		plot.setRegionID(getMapValue(plot.getX(), plot.getY()))
			
	map.recalculateAreas()
			
def updateReligionSpread(iReligion):
	for plot in plots.all():
		plot.setSpreadFactor(iReligion, getSpreadFactor(iReligion, location(plot)))

def init():
	updateRegionMap()
	for iReligion in range(iNumReligions):
		updateReligionSpread(iReligion)
		

tRegionMap = ((-1,) * iWorldX,) * iWorldY
				

tSpreadFactors = (
# Judaism
{
	iMinority :	[rEgypt, rMesopotamia, rPersia, rAnatolia, rBalkans, rItaly, rIberia, rEurope, rRussia, rBritain, rUnitedStates],
},
# Orthodoxy
{
	iCore :		[rRussia, rEthiopia],
	iHistorical : 	[rBalkans, rAnatolia, rMesopotamia, rEgypt, rSiberia],
	iPeriphery : 	[rMaghreb, rItaly, rPersia, rAlaska],
	iMinority :	[rCentralAsia],
},
# Catholicism
{
	iCore :		[rEurope, rItaly, rIberia],
	iHistorical :	[rBritain, rScandinavia, rCanada, rAlaska, rUnitedStates, rCaribbean, rMesoamerica, rColombia, rPeru, rBrazil, rArgentina, rSouthAfrica],
	iPeriphery :	[rBalkans, rAustralia, rOceania, rWestAfrica],
},
# Protestantism
{
	iCore :		[rBritain, rEurope, rScandinavia, rUnitedStates],
	iHistorical :	[rCanada, rAlaska, rAustralia],
	iPeriphery :	[rOceania, rSouthAfrica],
},
# Islam
{
	iCore : 	[rArabia, rMesopotamia, rEgypt],
	iHistorical : 	[rPersia, rMaghreb, rCentralAsia, rIndia, rIndonesia, rWestAfrica],
	iPeriphery : 	[rEthiopia, rItaly, rIberia, rAnatolia, rBalkans, rDeccan],
	iMinority : 	[rRussia, rSiberia],
},
# Hinduism
{
	iCore : 	[rIndia, rDeccan],
	iHistorical : 	[rIndochina, rIndonesia],
},
# Buddhism
{
	iCore : 	[rIndia, rTibet, rIndochina],
	iHistorical : 	[rCentralAsia, rChina, rManchuria, rKorea, rJapan, rIndonesia, rDeccan],
	iPeriphery : [],
	iMinority :	[rPersia],
},
# Confucianism
{
	iCore : 	[rChina, rManchuria],
	iHistorical :	[rKorea],
	iPeriphery : 	[rCentralAsia, rTibet],
	iMinority : 	[rJapan, rIndonesia, rIndochina, rAustralia],
},
# Taoism
{
	iCore : 	[rChina],
	iHistorical : 	[rManchuria],
	iPeriphery : 	[rTibet, rCentralAsia],
},
# Zoroastrianism
{
	iCore :		[rPersia],
	iPeriphery :	[rMesopotamia],
	iMinority : 	[rIndia, rAnatolia, rEgypt, rCentralAsia],
},
)