from Consts import *
from RFCUtils import utils
from sets import Set

### Class for easier tech specification ###

class Techs:

	def __init__(self, techs=[], column=0, era=-1, exceptions=[]):
		self.column = column
		self.era = era
		self.techs = techs
		self.exceptions = exceptions
		
	def list(self):
		lTechs = Set()
		lTechs.update([i for i in range(iNumTechs) if gc.getTechInfo(i).getGridX() <= self.column])
		lTechs.update([i for i in range(iNumTechs) if gc.getTechInfo(i).getEra() <= self.era])
		lTechs.update(self.techs)
		lTechs.difference_update(self.exceptions)
		
		return list(lTechs)

### Starting tech methods ###

def getScenarioTechs(iScenario, iPlayer):

	iCivilization = gc.getPlayer(iPlayer).getCivilizationType()
	for iScenarioType in reversed(range(iScenario+1)):
		if iCivilization in lStartingTechs[iScenarioType]:
			return lStartingTechs[iScenarioType][iCivilization].list()
			
def getStartingTechs(iPlayer):
	return getScenarioTechs(utils.getScenario(), iPlayer)
	
def initScenarioTechs(iScenario):
	for iPlayer in range(iNumTotalPlayers):
		if tBirth[iPlayer] > utils.getScenarioStartYear(): continue
	
		iCivilization = gc.getPlayer(iPlayer).getCivilizationType()
		if iCivilization in lStartingTechs[iScenario]:
			initTechs(iPlayer, lStartingTechs[iScenario][iCivilization].list())
			
def initPlayerTechs(iPlayer):
	initTechs(iPlayer, getStartingTechs(iPlayer))
				
def initTechs(iPlayer, lTechs):
	pPlayer = gc.getPlayer(iPlayer)

	for iTech in lTechs:
		gc.getTeam(pPlayer.getTeam()).setHasTech(iTech, True, iPlayer, False, False)
	
	iCurrentEra = pPlayer.getCurrentEra()
	pPlayer.setStartingEra(iCurrentEra)
	
### General functions ###
		
def initBirthYear(iPlayer):
	gc.getPlayer(iPlayer).setBirthYear(tBirth[iPlayer])

def init():
	for iPlayer in range(iNumPlayers):
		initBirthYear(iPlayer)

### Starting technologies ###

lStartingTechs = [
{
iCivNative : 	Techs([iTanning, iWorship]),
iCivEgypt :	Techs([iMining, iAgriculture, iWorship]),
iCivHarappa : 	Techs([iPottery, iAgriculture, iWorship]),
iCivChina :	Techs([iTanning, iMining, iAgriculture]),
iCivBabylonia :	Techs([iMasonry, iLeverage, iDivination], column=1, exceptions=[iTanning]),
iCivIndia :	Techs([iSmelting, iLeverage, iProperty, iCeremony, iAlloys], column=1),
iCivGreece :	Techs([iWriting], column=2),
iCivPersia :	Techs([iAlloys, iRiding, iWriting], column=2, exceptions=[iSeafaring]),
iCivCarthage :	Techs(column=2),
iCivPolynesia :	Techs([iTanning, iPottery, iWorship, iSailing, iSeafaring]),
iCivRome : 	Techs([iBloomery, iMetalCasting, iGeometry], column=3, exceptions=[iRiding, iCalendar, iShipbuilding]),
iCivTamils :	Techs([iBloomery, iGeometry, iPriesthood], column=3),
iCivEthiopia :	Techs([iAlloys, iWriting, iCalendar, iPriesthood], column=2),
iCivKorea :	Techs(column=5, exceptions=[iGeneralship]),
iCivMaya :	Techs([iProperty, iLeverage, iMasonry], column=1, exceptions=[iSailing]),
iCivByzantium :	Techs([iArchitecture, iPolitics, iEthics], column=5),
iCivJapan :	Techs([iNobility, iSteel, iArtisanry, iPolitics], column=5),
iCivVikings : 	Techs([iNobility, iSteel, iArtisanry], column=5),
iCivArabia :	Techs([iAlchemy, iTheology], column=6, exceptions=[iPolitics]),
iCivTibet :	Techs([iNobility, iScholarship, iEthics], column=5),
iCivKhmer :	Techs([iArtisanry, iEthics], column=5),
iCivIndonesia :	Techs([iEthics], column=5, exceptions=[iGeneralship]),
iCivMoors :	Techs([iMachinery, iAlchemy, iTheology], column=6, exceptions=[iPolitics]),
iCivSpain : 	Techs([iFeudalism, iTheology], column=6),
iCivFrance :	Techs([iFeudalism, iTheology], column=6),
iCivEngland :	Techs([iFeudalism, iTheology], column=6),
iCivHolyRome :	Techs([iFeudalism, iTheology], column=6),
iCivRussia :	Techs([iFeudalism], column=6, exceptions=[iPolitics, iScholarship, iEthics]),
iCivMali : 	Techs([iTheology], column=6),
iCivPoland : 	Techs([iFeudalism, iFortification, iCivilService, iTheology], column=6),
iCivSeljuks :	Techs([iFeudalism, iFortification, iMachinery, iAlchemy, iTheology], column=6),
iCivPortugal :	Techs([iClergy], column=7),
iCivInca : 	Techs([iGeometry, iContract, iTradition, iPriesthood], column=3, exceptions=[iSeafaring, iAlloys, iRiding, iShipbuilding]),
iCivMongols :	Techs([iPaper, iCompass], column=7, exceptions=[iTheology]),
iCivAztecs :	Techs([iGeometry, iContract, iTradition, iPriesthood, iGeneralship, iAesthetics, iCurrency, iLaw], column=3, exceptions=[iSeafaring, iAlloys, iRiding, iShipbuilding]),
iCivItaly : 	Techs([iStandingArmy, iPaper, iCompass, iClergy], column=7),
iCivMughals :	Techs([iStandingArmy, iCropRotation, iClergy, iGunpowder], column=7),
iCivTurkey :	Techs([iStandingArmy, iCropRotation, iPaper, iClergy, iGunpowder], column=7),
iCivCongo : 	Techs([iMachinery, iCivilService, iTheology], column=6),
iCivThailand : 	Techs([iGunpowder], column=8, exceptions=[iCompass, iClergy]),
iCivIran : 	Techs([iHeritage, iFirearms], column=9),
iCivNetherlands:Techs(column=10),
iCivGermany :	Techs([iReplaceableParts, iPhysics, iGeology, iMeasurement], column=11),
iCivAmerica :	Techs([iRepresentation, iChemistry], column=12),
iCivArgentina :	Techs(column=13, exceptions=[iMachineTools]),
iCivMexico :	Techs(column=13, exceptions=[iMachineTools]),
iCivColombia :	Techs(column=13, exceptions=[iMachineTools]),
iCivBrazil :	Techs(column=13),
iCivCanada :	Techs([iBallistics, iEngine, iRailroad, iJournalism], column=13),
},
{
iCivIndependent:Techs(column=5),
iCivIndependent2:Techs(column=5),
iCivChina :	Techs([iMachinery, iAlchemy, iCivilService], column=6, exceptions=[iNobility]),
iCivKorea :	Techs([iMachinery], column=6, exceptions=[iNobility]),
iCivByzantium :	Techs([iFortification, iCivilService, iTheology], column=6),
iCivJapan :	Techs(column=6, exceptions=[iScholarship]),
iCivVikings :	Techs([iFeudalism], column=6),
},
{
iCivIndependent:Techs(column=10),
iCivIndependent2:Techs(column=10),
iCivChina :	Techs([iLogistics, iUrbanPlanning], column=10),
iCivIndia : 	Techs([iReplaceableParts], column=11, exceptions=[iAstronomy, iScientificMethod]),
iCivTamils :	Techs([iReplaceableParts], column=11, exceptions=[iAstronomy, iScientificMethod, iCivilLiberties]),
iCivIran :	Techs(column=11, exceptions=[iScientificMethod]),
iCivKorea :	Techs([iUrbanPlanning], column=10),
iCivJapan :	Techs([iLogistics, iCorporation, iUrbanPlanning], column=10),
iCivVikings :	Techs([iReplaceableParts, iMeasurement], column=11),
iCivSpain :	Techs([iReplaceableParts], column=11),
iCivFrance :	Techs([iReplaceableParts, iGeology, iMeasurement, iConstitution], column=11),
iCivEngland :	Techs([iReplaceableParts, iHydraulics, iPhysics, iConstitution], column=11),
iCivHolyRome :	Techs([iReplaceableParts], column=11),
iCivRussia : 	Techs(column=11, exceptions=[iCivilLiberties]),
iCivPoland :	Techs([iConstitution], column=11),
iCivPortugal :	Techs([iReplaceableParts], column=11),
iCivMughals :	Techs(column=11, exceptions=[iScientificMethod, iCivilLiberties]),
iCivThailand :	Techs([iUrbanPlanning, iHorticulture], column=10),
iCivCongo :	Techs([iCartography, iJudiciary], column=8),
iCivNetherlands:Techs([iReplaceableParts, iHydraulics, iPhysics, iConstitution], column=11),
}]