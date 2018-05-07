from Consts import *
from RFCUtils import utils
from sets import Set
from StoredData import data
import Victory as vic

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
		initTech(iPlayer, iTech)
	
	iCurrentEra = pPlayer.getCurrentEra()
	pPlayer.setStartingEra(iCurrentEra)
	
def initTech(iPlayer, iTech):
	gc.getTeam(gc.getPlayer(iPlayer).getTeam()).setHasTech(iTech, True, iPlayer, False, False)
	vic.onTechAcquired(iPlayer, iTech)
	
### General functions ###
		
def initBirthYear(iPlayer):
	gc.getPlayer(iPlayer).setBirthYear(tBirth[iPlayer])

def init():
	for iPlayer in range(iNumPlayers):
		initBirthYear(iPlayer)

### Starting technologies ###

lStartingTechs = [
{
iCivNative : 	Techs([iTanning, iMythology]),
iCivEgypt :	Techs([iMining, iPottery, iAgriculture]),
iCivHarappa : 	Techs([iMining, iPottery, iAgriculture]),
iCivChina :	Techs([iTanning, iMining, iAgriculture]),
iCivBabylonia :	Techs([iPottery, iPastoralism, iAgriculture]),
iCivIndia :	Techs([iAlloys, iWriting, iCalendar], column=2, exceptions=[iSeafaring]),
iCivGreece :	Techs([iAlloys, iArithmetics, iWriting], column=2),
iCivPersia :	Techs([iBloomery, iPriesthood], column=3, exceptions=[iSeafaring, iShipbuilding]),
iCivCarthage :	Techs([iAlloys, iWriting, iShipbuilding], column=2),
iCivPolynesia :	Techs([iTanning, iMythology, iSailing, iSeafaring]),
iCivRome : 	Techs([iBloomery, iCement, iMathematics, iLiterature], column=3, exceptions=[iRiding, iCalendar, iShipbuilding]),
iCivTamils :	Techs([iBloomery, iMathematics, iContract, iPriesthood], column=3),
iCivEthiopia :	Techs([iAlloys, iWriting, iCalendar, iPriesthood], column=2),
iCivKorea :	Techs(column=5, exceptions=[iGeneralship, iEngineering, iCurrency]),
iCivMaya :	Techs([iProperty, iLeverage, iMasonry, iSmelting, iCeremony], column=1, exceptions=[iSailing]),
iCivByzantium :	Techs([iArchitecture, iPolitics, iEthics], column=5),
iCivJapan :	Techs([iNobility, iSteel, iArtisanry, iPolitics], column=5),
iCivVikings : 	Techs([iNobility, iSteel, iArtisanry, iPolitics, iScholarship, iArchitecture, iGuilds], column=5),
iCivTurks :	Techs([iNobility, iSteel], column=5, exceptions=[iNavigation, iMedicine, iPhilosophy]),
iCivArabia :	Techs([iAlchemy, iTheology], column=6, exceptions=[iPolitics]),
iCivTibet :	Techs([iNobility, iScholarship, iEthics], column=5),
iCivIndonesia :	Techs([iEthics], column=5, exceptions=[iGeneralship]),
iCivMoors :	Techs([iMachinery, iAlchemy, iTheology], column=6, exceptions=[iPolitics]),
iCivSpain : 	Techs([iFeudalism, iAlchemy, iGuilds], column=6),
iCivFrance :	Techs([iFeudalism, iTheology], column=6),
iCivKhmer :	Techs([iNobility, iArchitecture, iArtisanry, iScholarship, iEthics], column=5),
iCivEngland :	Techs([iFeudalism, iTheology], column=6),
iCivHolyRome :	Techs([iFeudalism, iTheology], column=6),
iCivRussia :	Techs([iFeudalism], column=6, exceptions=[iPolitics, iScholarship, iEthics]),
iCivMali : 	Techs([iTheology], column=6),
iCivPoland : 	Techs([iFeudalism, iFortification, iCivilService, iTheology], column=6),
iCivPortugal :	Techs([iPatronage], column=7),
iCivInca : 	Techs([iMathematics, iContract, iLiterature, iPriesthood], column=3, exceptions=[iSeafaring, iAlloys, iRiding, iShipbuilding]),
iCivMongols :	Techs([iPaper, iCompass], column=7, exceptions=[iTheology]),
iCivAztecs :	Techs([iMathematics, iContract, iLiterature, iPriesthood, iGeneralship, iAesthetics, iCurrency, iLaw], column=3, exceptions=[iSeafaring, iAlloys, iRiding, iShipbuilding]),
iCivItaly : 	Techs([iCommune, iPaper, iCompass, iDoctrine], column=7),
iCivMughals :	Techs([iCommune, iCropRotation, iDoctrine, iGunpowder], column=7),
iCivOttomans :	Techs([iCommune, iCropRotation, iPaper, iDoctrine, iGunpowder], column=7),
iCivCongo : 	Techs([iMachinery, iCivilService, iTheology], column=6),
iCivThailand : 	Techs(column=8, exceptions=[iCompass, iDoctrine, iCommune, iPatronage]),
iCivIran : 	Techs([iHeritage, iFirearms], column=9),
iCivNetherlands:Techs(column=10),
iCivGermany :	Techs([iReplaceableParts], column=11),
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
iCivKorea :	Techs([iMachinery], column=6, exceptions=[iScholarship]),
iCivByzantium :	Techs([iFortification,iMachinery, iCivilService], column=6),
iCivJapan :	Techs(column=6, exceptions=[iScholarship]),
iCivVikings :	Techs([iGuilds], column=6),
iCivTurks :	Techs([iNobility, iSteel], column=5, exceptions=[iNavigation, iMedicine, iPhilosophy]),
},
{
iCivIndependent:Techs(column=10),
iCivIndependent2:Techs(column=10),
iCivChina :	Techs([iHorticulture, iUrbanPlanning], column=10, exceptions=[iExploration, iOptics, iAcademia]),
iCivIndia : 	Techs([iCombinedArms, iUrbanPlanning], column=10, exceptions=[iExploration]),
iCivTamils :	Techs([iCombinedArms, iUrbanPlanning], column=10, exceptions=[iExploration, iOptics]),
iCivIran :	Techs([iCombinedArms, iUrbanPlanning, iHorticulture], column=10, exceptions=[iExploration]),
iCivKorea :	Techs(column=10, exceptions=[iExploration, iOptics, iAcademia]),
iCivJapan :	Techs([iCombinedArms, iUrbanPlanning], column=10, exceptions=[iExploration, iOptics]),
iCivVikings :	Techs(column=11, exceptions=[iEconomics, iHorticulture]),
iCivSpain :	Techs([iCombinedArms, iGeography, iHorticulture], column=10),
iCivFrance :	Techs([iReplaceableParts], column=11),
iCivEngland :	Techs([iReplaceableParts, iPhysics], column=11),
iCivHolyRome :	Techs([iCombinedArms, iUrbanPlanning, iHorticulture], column=10, exceptions=[iExploration]),
iCivRussia : 	Techs([iCombinedArms, iUrbanPlanning], column=10, exceptions=[iExploration, iOptics]),
iCivPoland :	Techs(column=11, exceptions=[iEconomics, iGeography]),
iCivPortugal :	Techs([iCombinedArms, iGeography, iHorticulture], column=10),
iCivOttomans :	Techs([iCombinedArms, iUrbanPlanning, iHorticulture], column=10, exceptions=[iExploration]),
iCivMughals :	Techs([iCombinedArms, iUrbanPlanning, iHorticulture], column=10, exceptions=[iExploration, iOptics]),
iCivThailand :	Techs(column=10, exceptions=[iExploration, iOptics]),
iCivCongo :	Techs([iCartography, iJudiciary], column=8),
iCivNetherlands:Techs([iReplaceableParts, iHydraulics], column=11),
iCivGermany :	Techs([iReplaceableParts], column=11),
}]