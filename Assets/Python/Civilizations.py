from Consts import *
from RFCUtils import utils
from sets import Set
from StoredData import data
import Victory as vic
from Religions import rel

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
	
	if iPlayer == iChina and utils.getScenario() == i3000BC and utils.getHumanID() != iPlayer:
		initTech(iPlayer, iProperty)
		initTech(iPlayer, iAlloys)
				
def initTechs(iPlayer, lTechs):
	pPlayer = gc.getPlayer(iPlayer)

	for iTech in lTechs:
		initTech(iPlayer, iTech)
	
	iCurrentEra = pPlayer.getCurrentEra()
	pPlayer.setStartingEra(iCurrentEra)
	
def initTech(iPlayer, iTech):
	gc.getTeam(gc.getPlayer(iPlayer).getTeam()).setHasTech(iTech, True, iPlayer, False, False)
	vic.onTechAcquired(iPlayer, iTech)
	rel.onTechAcquired(iPlayer, iTech)

### Tech preference functions ###

def getDictValue(dDict, key):
	if key not in dDict: return 0
	
	return dDict[key]

def getTechPreferences(iPlayer):
	dPreferences = {}
	iCivilization = gc.getPlayer(iPlayer).getCivilizationType()
	
	if iCivilization not in dTechPreferences:
		return dPreferences
		
	for iTech, iValue in dTechPreferences[iCivilization].items():
		dPreferences[iTech] = iValue
		
	for iTech, iValue in dTechPreferences[iCivilization].items():
		for i in range(4):
			iOrPrereq = gc.getTechInfo(iTech).getPrereqOrTechs(i)
			iAndPrereq = gc.getTechInfo(iTech).getPrereqAndTechs(i)
			
			if iOrPrereq < 0 and iAndPrereq < 0: break
			
			updatePrereqPreference(dPreferences, iOrPrereq, iValue)
			updatePrereqPreference(dPreferences, iAndPrereq, iValue)
	
	return dPreferences
	
def updatePrereqPreference(dPreferences, iPrereqTech, iValue):
	if iPrereqTech < 0: return
	
	iPrereqValue = getDictValue(dPreferences, iPrereqTech)
	
	if iValue > 0 and iPrereqValue >= 0:
		iPrereqValue = min(max(iPrereqValue, iValue), iPrereqValue + iValue / 2)
		
	elif iValue < 0 and iPrereqValue <= 0:
		iPrereqValue = max(min(iPrereqValue, iValue), iPrereqValue + iValue / 2)
		
	dPreferences[iPrereqTech] = iPrereqValue
	
def initPlayerTechPreferences(iPlayer):
	initTechPreferences(iPlayer, getTechPreferences(iPlayer))
	
def initTechPreferences(iPlayer, dPreferences):
	for iTech, iValue in dPreferences.items():
		gc.getPlayer(iPlayer).setTechPreference(iTech, iValue)

### Wonder preference methods ###

def initBuildingPreferences(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	iCiv = pPlayer.getCivilizationType()
	if iCiv in dBuildingPreferences:
		for iBuilding, iValue in dBuildingPreferences[iCiv].iteritems():
			pPlayer.setBuildingPreference(iBuilding, iValue)
			
	if iCiv in dDefaultWonderPreferences:
		iDefaultPreference = dDefaultWonderPreferences[iCiv]
		for iWonder in range(iFirstWonder, iNumBuildings):
			if iCiv not in dBuildingPreferences or iWonder not in dBuildingPreferences[iCiv]:
				pPlayer.setBuildingPreference(iWonder, iDefaultPreference)
	
### General functions ###
		
def initBirthYear(iPlayer):
	gc.getPlayer(iPlayer).setBirthYear(tBirth[iPlayer])

def init():
	for iPlayer in range(iNumPlayers):
		initBirthYear(iPlayer)
		initPlayerTechPreferences(iPlayer)
		initBuildingPreferences(iPlayer)

### Starting technologies ###

lStartingTechs = [
{
iCivNative : 	Techs([iTanning, iMythology]),
iCivEgypt :	Techs([iMining, iPottery, iAgriculture]),
iCivBabylonia :	Techs([iPottery, iPastoralism, iAgriculture]),
iCivHarappa : 	Techs([iMining, iPottery, iAgriculture]),
iCivNorteChico : Techs([iAgriculture, iMythology]),
iCivNubia : 	Techs([iAgriculture, iMythology, iCeremony, iPastoralism, iMining]),
iCivChina :	Techs([iTanning, iMining, iAgriculture, iPastoralism, iPottery, iMythology, iSmelting, iLeverage]),
iCivIndia :	Techs([iAlloys, iWriting, iCalendar], column=2, exceptions=[iSeafaring]),
iCivGreece :	Techs([iAlloys, iArithmetics, iWriting], column=2),
iCivOlmecs : Techs([iTanning, iMining, iAgriculture]),
iCivPersia :	Techs([iBloomery, iPriesthood], column=3, exceptions=[iSeafaring, iShipbuilding]),
iCivCeltia : 	Techs([iAlloys, iBloomery, iCalendar, iConstruction], column=2, exceptions=[iSeafaring, iProperty]),
iCivCarthage :	Techs([iAlloys, iWriting, iShipbuilding], column=2),
iCivPolynesia :	Techs([iTanning, iMythology, iSailing, iSeafaring]),
iCivRome : 	Techs([iBloomery, iCement, iMathematics, iLiterature], column=3, exceptions=[iRiding, iCalendar, iShipbuilding]),
iCivMaya :	Techs([iProperty, iMasonry, iSmelting, iCeremony], column=1, exceptions=[iSailing]),
iCivTamils :	Techs([iBloomery, iMathematics, iContract, iPriesthood], column=3),
iCivEthiopia :	Techs([iAlloys, iWriting, iCalendar, iPriesthood], column=2),
iCivVietnam :	Techs([iAlloys, iWriting, iCalendar, iPriesthood, iBloomery], column=2),
iCivTeotihuacan :	Techs([iProperty, iLeverage, iCeremony], column=1, exceptions=[iSailing]),
iCivInuit : Techs([iSailing, iPottery, iMythology, iTanning]),
iCivMississippi :	Techs([iTanning, iMining, iPottery, iSmelting, iMasonry, iAlloys]),
iCivKorea :	Techs(column=5, exceptions=[iGeneralship, iEngineering, iCurrency]),
iCivTiwanaku :	Techs([iWriting, iCalendar], column=2),
iCivByzantium :	Techs([iArchitecture, iPolitics, iEthics], column=5),
iCivWari :	Techs([iWriting, iCalendar, iPriesthood, iConstruction], column=2),
iCivJapan :	Techs([iNobility, iSteel, iArtisanry, iPolitics], column=5),
iCivVikings : 	Techs([iNobility, iSteel, iArtisanry, iPolitics, iScholarship, iArchitecture, iGuilds], column=5),
iCivTurks :	Techs([iNobility, iSteel], column=5, exceptions=[iNavigation, iMedicine, iPhilosophy]),
iCivArabia :	Techs([iAlchemy, iTheology], column=6, exceptions=[iPolitics]),
iCivTibet :	Techs([iNobility, iScholarship, iEthics], column=5),
iCivIndonesia :	Techs([iEthics], column=5, exceptions=[iGeneralship]),
iCivBurma :		Techs(column=5, exceptions=[iGeneralship]),
iCivKhazars :	Techs([iNobility, iGeneralship, iCurrency], column=4),
iCivChad :	Techs([iFortification], column=6, exceptions=[iEthics, iArchitecture]),
iCivMoors :	Techs([iMachinery, iAlchemy, iTheology], column=6, exceptions=[iPolitics]),
iCivSpain : 	Techs([iFeudalism, iAlchemy, iGuilds], column=6),
iCivFrance :	Techs([iFeudalism, iTheology], column=6),
iCivOman :		Techs([iDoctrine, iTheology, iFeudalism], column=6, exceptions=[iArchitecture, iArtisanry]),
iCivKhmer :	Techs([iNobility, iArchitecture, iArtisanry, iScholarship, iEthics], column=5),
iCivMuisca : Techs([iMining, iPottery, iMasonry]),
iCivYemen :		Techs([iGuilds, iTheology, iFeudalism, iFortification, iCommune], column=6),
iCivEngland :	Techs([iFeudalism, iTheology, iFortification], column=6),
iCivHolyRome :	Techs([iFeudalism, iTheology], column=6),
iCivKievanRus :	Techs([iFeudalism, iTheology, iDoctrine], column=6, exceptions=[iArtisanry, iArchitecture]),
iCivHungary :	Techs([iFeudalism, iFortification, iMachinery], column=6, exceptions=[iPolitics, iScholarship]),
iCivPhilippines : 	Techs(column=6),
iCivChimu : 	Techs([iPriesthood, iMathematics, iLiterature], column=3, exceptions=[iAlloys, iRiding]),
iCivSwahili : 	Techs([iTheology], column=6, exceptions=[iArtisanry, iPolitics]),
iCivMamluks : 	Techs([iTheology], column=6),
iCivMali : 	Techs([iTheology], column=6),
iCivPoland : 	Techs([iFeudalism, iFortification, iCivilService, iTheology], column=6),
iCivZimbabwe : 	Techs([iFeudalism, iFortification], column=6),
iCivPortugal :	Techs([iPatronage], column=7),
iCivInca : 	Techs([iMathematics, iContract, iLiterature, iPriesthood], column=3, exceptions=[iSeafaring, iAlloys, iRiding, iShipbuilding]),
iCivNigeria :	Techs([iPaper, iCompass], column=7, exceptions=[iTheology]),
iCivMongols :	Techs([iPaper, iCompass], column=7, exceptions=[iTheology]),
iCivAztecs :	Techs([iMathematics, iContract, iLiterature, iPriesthood, iGeneralship, iAesthetics, iCurrency, iLaw], column=3, exceptions=[iSeafaring, iAlloys, iRiding, iShipbuilding]),
iCivItaly : 	Techs([iCommune, iPaper, iCompass, iDoctrine], column=7),
iCivMughals :	Techs([iCommune, iCropRotation, iDoctrine, iGunpowder], column=7),
iCivOttomans :	Techs([iCommune, iCropRotation, iPaper, iDoctrine, iGunpowder], column=7),
iCivRussia :	Techs([iCommune, iCropRotation, iPaper, iGunpowder], column=7),
iCivCongo : 	Techs([iMachinery, iCivilService, iTheology], column=6),
iCivThailand : 	Techs(column=8, exceptions=[iCompass, iDoctrine, iCommune, iPatronage]),
iCivIran : 	Techs([iHeritage, iFirearms], column=9),
iCivSweden : 	Techs([iHeritage, iFirearms, iAcademia], column=9),
iCivNetherlands:Techs(column=10),
iCivManchuria:	Techs([iCombinedArms], column=10),
iCivGermany :	Techs(column=11, exceptions=[iGeography, iCivilLiberties, iHorticulture, iUrbanPlanning]),
iCivAmerica :	Techs([iRepresentation, iChemistry], column=12),
iCivArgentina :	Techs([iRepresentation, iNationalism], column=12),
iCivMexico :	Techs([iRepresentation, iNationalism], column=12),
iCivColombia :	Techs([iRepresentation, iNationalism], column=12),
iCivBrazil :	Techs([iRepresentation, iNationalism, iBiology], column=12),
iCivAustralia :	Techs([iBallistics, iEngine, iRailroad, iJournalism], column=13),
iCivBoers :		Techs(column=13),
iCivCanada :	Techs([iBallistics, iEngine, iRailroad, iJournalism], column=13),
iCivIsrael :	Techs([iAviation, iFission, iGlobalism], column=16),
},
{
iCivIndependent:Techs(column=5),
iCivIndependent2:Techs(column=5),
iCivNubia :	Techs([iSteel, iArchitecture, iScholarship], column=5),
iCivPersia :	Techs([iNobility, iSteel, iFeudalism], column=5),
iCivChina :	Techs([iMachinery, iAlchemy, iCivilService], column=6, exceptions=[iNobility]),
iCivMaya : Techs([iAesthetics, iMathematics, iPriesthood], column=3, exceptions=[iAlloys, iRiding]),
iCivTamils :	Techs([iArtisanry, iArchitecture], column=5, exceptions=[iGeneralship, iPhilosophy]),
iCivEthiopia :	Techs([iFortification], column=6, exceptions=[iArtisanry]),
iCivInuit : Techs([iSmelting, iAlloys, iSeafaring, iShipbuilding], column=1, exceptions=[iPastoralism, iAgriculture]),
iCivMississippi :	Techs([iTanning, iMining, iPottery, iSmelting, iMasonry, iAlloys, iMythology, iSailing, iDivination]),
iCivKorea :	Techs([iMachinery], column=6, exceptions=[iScholarship]),
iCivTiwanaku :	Techs([iWriting, iCalendar, iPriesthood, iConstruction, iAlloys, iCement], column=2),
iCivByzantium :	Techs([iFortification,iMachinery, iCivilService], column=6),
iCivWari :	Techs([iWriting, iCalendar, iPriesthood, iConstruction, iArithmetics, iContract], column=2),
iCivJapan :	Techs(column=6, exceptions=[iScholarship]),
iCivVikings :	Techs([iGuilds], column=6),
iCivTurks :	Techs([iNobility, iSteel], column=5, exceptions=[iNavigation, iMedicine, iPhilosophy]),
},
{
iCivIndependent:Techs(column=10),
iCivIndependent2:Techs(column=10),
iCivNubia : 	Techs([iGeography], column=10, exceptions=[iHeritage, iLogistics]),
iCivManchuria :	Techs([iHorticulture, iUrbanPlanning, iCombinedArms], column=10, exceptions=[iExploration, iOptics, iAcademia]),
iCivCeltia :	Techs(column=10, exceptions=[iHeritage, iOptics, iExploration, iLogistics]),
iCivIndia : 	Techs([iCombinedArms, iUrbanPlanning], column=10, exceptions=[iExploration]),
iCivInuit : Techs([iCalendar, iNavigation, iAlloys, iShipbuilding], column=2, exceptions=[iMasonry, iLeverage, iProperty, iPastoralism]),
iCivTamils :	Techs([iCombinedArms, iUrbanPlanning], column=10, exceptions=[iExploration, iOptics]),
iCivIran :	Techs([iCombinedArms, iGeography, iUrbanPlanning, iHorticulture], column=10),
iCivVietnam :	Techs(column=10, exceptions=[iExploration, iOptics]),
iCivKorea :	Techs(column=10, exceptions=[iExploration, iOptics, iAcademia]),
iCivJapan :	Techs([iCombinedArms, iUrbanPlanning], column=10, exceptions=[iExploration, iOptics]),
iCivVikings :	Techs(column=11, exceptions=[iEconomics, iHorticulture]),
iCivTurks :	Techs([iFirearms, iLogistics, iHeritage], column=9),
iCivKazakhs :	Techs([iFirearms, iLogistics, iHeritage], column=9),
iCivBurma :		Techs(column=10, exceptions=[iExploration, iOptics]),
iCivKhmer :	Techs([iUrbanPlanning], column=10, exceptions=[iExploration, iOptics, iHeritage, iLogistics]),
iCivChad :	Techs([iCombinedArms], column=10, exceptions=[iHeritage, iOptics, iExploration, iLogistics]),
iCivMoors :	Techs([iUrbanPlanning], column=10, exceptions=[iExploration, iOptics]),
iCivSpain :	Techs([iCombinedArms, iGeography, iHorticulture], column=10),
iCivFrance :	Techs(column=11, exceptions=[iUrbanPlanning, iEconomics]),
iCivOman :		Techs([iEconomics, iGeography], column=10, exceptions=[iHeritage]),
iCivEngland :	Techs(column=11, exceptions=[iUrbanPlanning, iHorticulture]),
iCivHolyRome :	Techs([iCombinedArms, iUrbanPlanning, iHorticulture], column=10, exceptions=[iExploration]),
iCivPoland :	Techs(column=11, exceptions=[iEconomics, iGeography, iHorticulture, iUrbanPlanning]),
iCivPortugal :	Techs([iGeography, iHorticulture], column=10),
iCivOttomans :	Techs([iUrbanPlanning, iHorticulture], column=10, exceptions=[iExploration]),
iCivRussia : 	Techs([iCombinedArms, iUrbanPlanning], column=10, exceptions=[iExploration, iOptics]),
iCivMughals :	Techs([iUrbanPlanning, iHorticulture], column=10, exceptions=[iExploration, iOptics]),
iCivThailand :	Techs(column=10, exceptions=[iExploration, iOptics]),
iCivCongo :	Techs([iCartography, iJudiciary], column=8),
iCivSweden :	Techs([iReplaceableParts, iMeasurement], column=11),
iCivNetherlands:Techs(column=11, exceptions=[iHorticulture, iScientificMethod, iUrbanPlanning]),
iCivGermany :	Techs(column=11, exceptions=[iGeography, iCivilLiberties, iHorticulture, iUrbanPlanning]),
}]

### Tech Preferences ###

dTechPreferences = {
	iCivEgypt : {
		iMasonry: 30,
		iDivination: 20,
		iPhilosophy: 20,
		iPriesthood: 20,
		iRiding: 40,
		iLeverage: 20,
		
		iAlloys: -20,
		iBloomery: -50,
	},
	iCivBabylonia : {
		iWriting: 30,
		iContract: 30,
		iCalendar: 30,
		iMasonry: 20,
		iProperty: 20,
		iDivination: 20,
		iConstruction: 20,
	
		iPriesthood: -50,
		iMathematics: -30,
		iAlloys: -30,
		iBloomery: -30,
		iSteel: -30,
	},
	iCivHarappa : {
		iMasonry: 20,
		iPastoralism: 20,
		iPottery: 20,
		
		iMythology: -50,
		iDivination: -50,
		iCeremony: -50,
	},
	iCivNorteChico : {
		iWriting : -20,
		iCalendar : -20,
		iPottery : -100,
	},
	iCivNubia : {
		iRiding: 40,
		iTanning: 50,
		iEthics: 20,
		
		iSmelting: -50,
		iAlloys: -20,
	},
	iCivChina : {
		iAesthetics: 40,
		iContract: 40,
		iGunpowder: 20,
		iPrinting: 20,
		iPaper: 20,
		iCompass: 20,
		iConstruction: 20,
		iCivilService: 15,
		
		iCivilLiberties: -100,
		iHumanities: -100,
		iAcademia: -100,
		iFirearms: -50,
		iCompanies: -40,
		iExploration: -40,
		iOptics: -40,
		iGeography: -40,
		iTheology: -40,
		iEducation: -40,
		iLogistics: -40,
		iCombinedArms: -40,
		iDivination: -20,
		iSailing: -20,	
	},
	iCivGreece : {
		iSailing: 40,
		iWriting: 30,
		iPhilosophy: 30,
		iAesthetics: 30,
		iDivination: 30,
		iPhilosophy: 30,
		iLiterature: 30,
		iMedicine: 30,
		iCement: 20,
		iArithmetics: 20,
		iMathematics: 20,
	
		iCalendar: -30,
		iMachinery: -20,
		iPaper: -20,
		iPrinting: -20,
		iTheology: -15,
	},
	iCivOlmecs : {
		iWriting: 30,
		iCalendar: 30,
		iArithmetics: 30,
	},
	iCivIndia : {
		iCeremony: 200,
		iPriesthood: 200,
		iPhilosophy: 50,
		
		iEngineering: -20,
		iTheology: -20,
		iCivilService: -20,
	},
	iCivCarthage : {
		iNavigation: 40,
		iRiding: 30,
		iCurrency: 30,
		iCompass: 20,
	},
	iCivPolynesia : {
		iCompass: 20,
		iDivination: 20,
		iMasonry: 20,
		
		iAlloys: -30,
		iBloomery: -30,
	},
	iCivPersia : {
		iFission: 15,
	
		iTheology: -40,
	},
	iCivCeltia : {
		iPriesthood : 20,
		iFortification: -20,
	},
	iCivRome : {
		iTheology: 30,
		iCurrency: 20,
		iLaw: 20,
		iPolitics: 20,
		iConstruction: 15,
		iEngineering: 15,
		
		iCalendar: -20,
	},
	iCivMaya : {
		iCalendar: 40,
		iAesthetics: 30,
	},
	iCivTamils : {
		iNavigation: 40,
		iCement: 20,
		iCompass: 20,
		iCalendar: 20,
		
		iScientificMethod: -20,
		iAcademia: -20,
		iReplaceableParts: -20,
	},
	iCivVietnam : {
		iCurrency : 20,
		iCommune : 20,
		iHeritage : 20,
		iFortification : 40,
		iOptics : -20,
	},
	iCivTeotihuacan : {
		iMasonry: 30,
		iSmelting: 30,
	},
	iCivKorea : {
		iPrinting: 30,
		iGunpowder: 30,
	
		iOptics: -40,
		iExploration: -40,
		iReplaceableParts: -40,
		iScientificMethod: -40,
	},
	iCivInuit: {
		iMining : 20,
		iSailing : 20,
		iShipbuilding : 20,
		iAgriculture : -20,
		iPastoralism : -20,
		iProperty : -20,
	},
	iCivMississippi : {
		iLeverage : 40,
		iPastoralism : 20,
		iMythology : 20,
		
		iAgriculture : -20,
		iSailing : -40,
	},
	iCivTiwanaku : {
		iPriesthood: 30,
		iMathematics: 30,
	
		iBloomery: -40,
	},
	iCivByzantium : {
		iFinance: -50,
		iDoctrine: -20,
		iOptics: -20,
		iFirearms: -20,
		iExploration: -20,
	},
	iCivWari : {
		iContract : 20,
	
		iBloomery: -40,
	},
	iCivJapan : {
		iFeudalism: 40,
		iFortification: 40,
		iRobotics: 40,
	
		iOptics: -40,
		iExploration: -40,
		iFirearms: -30,
		iMachinery: -20,
		iGuilds: -20,
		iGeography: -20,
		iReplaceableParts: -20,
		iScientificMethod: -20,
	},
	iCivVikings : {
		iMachinery: 30,
		iCivilService: 30,
		iCompass: 20,
		iCombinedArms: 20,
	},
	iCivArabia : {
		iScholarship: 30,
		iAlchemy: 30,
		
		iFinance: -50,
		iFirearms: -50,
		iCompanies: -50,
		iPaper: -20,
	},
	iCivTibet : {
		iPhilosophy: 30,
		iEngineering: 20,
		iPaper: 20,
		iTheology: 20,
		iDoctrine: 20,
	},
	iCivIndonesia : {
		iAesthetics: 30,
		iArtisanry: 30,
		iExploration: -20,
	},
	iCivBurma : {
		iSteel : 30,
		iFortification : 20,
	},
	iCivKhazars : {
		iFortification : 20,
		iCommune : 20,
	},
	iCivChad : {
	},
	iCivMoors : {
		iCivilService: 20,
	
		iExploration: -40,
		iGuilds: -40,
	},
	iCivSpain : {
		iCartography: 100,
		iExploration: 100,
		iCompass: 100,
		iFirearms: 100,
		iPatronage: 50,
		iReplaceableParts: 30,
		iGuilds: 15,
		iGunpowder: 15,
		iChemistry: 15,
	},
	iCivFrance : {
		iReplaceableParts: 30,
		iFirearms: 20,
		iExploration: 20,
		iGeography: 20,
		iLogistics: 20,
		iPatronage: 20,
		iMeasurement: 20,
		iAcademia: 20,
		iEducation: 15,
		iFeudalism: 15,
		iChemistry: 15,
		iSociology: 15,
		iFission: 12,
	},
	iCivOman : {
		iGeography : 20,
		iCartography : 20,
		iEconomics : 20,
		iOptics : 20,
		iCompass: 20,
		iExploration : 20,
	},
	iCivKhmer : {
		iPhilosophy: 30,
		iSailing: 30,
		iCalendar: 30,
		iCivilService: 30,
		iAesthetics: 20,
		
		iCurrency: -30,
		iExploration: -30,
	},
	iCivMuisca : {
		iSmelting : 20,
		iProperty : 20,
	},
	iCivYemen : {
		iGeography : 20,
		iCartography : 20,
		iStatecraft : 20,
		iOptics : 20,
		iCompass: 20,
		iExploration : 20,
	},
	iCivEngland : {
		iExploration: 40,
		iCommune : 40,
		iGeography: 40,
		iFirearms: 40,
		iReplaceableParts: 30,
		iLogistics: 30,
		iGuilds: 30,
		iCivilLiberties: 20,
		iEducation: 15,
		iChemistry: 15,
	},
	iCivHolyRome : {
		iAcademia: 50,
		iPrinting: 50,
		iFirearms: 20,
		iReplaceableParts: 20,
		iEducation: 15,
		iGuilds: 15,
		iOptics: 15,
		iFission: 12,
	},
	iCivKievanRus : {
		iEthics : 20,
		iTheology : 20,
		iDoctrine : 20,
		iEconomics : 20,
	},
	iCivHungary : {
		iCivilLiberties : 20,
	},
	iCivPhilippines : {
		iLogistics : 30,
		iCartography : 40,
		iExploration : 40,
		iOptics : 40,
		iCompass : 40,
	},
	iCivChimu : {
		
	},
	iCivMamluks : {
		iScholarship : 30,
		iAlchemy : 30,
		iFinance : -50,
		iFirearms : -50,
		iCompanies : -50,
		iPaper : -20,
	},
	iCivSwahili : {
	},
	iCivMali : {
		iEducation: 30,
	},
	iCivMughals : {
		iHumanities: 30,
		iPhilosophy: 20,
		iEducation: 20,
		iPaper: 20,
		iPatronage: 20,
		iEngineering: 15,
	
		iReplaceableParts: -30,
		iScientificMethod: -30,
		iCombinedArms: -30,
		iExploration: -30,
	},
	iCivPoland : {
		iCombinedArms: 30,
		iCivilLiberties: 30,
		iSocialContract: 20,
		iOptics: 20,
	},
	iCivZimbabwe : {
	},
	iCivPortugal : {
		iCartography: 100,
		iExploration: 100,
		iGeography: 100,
		iCompass: 100,
		iFirearms: 100,
		iCompanies: 50,
		iPatronage: 50,
		iReplaceableParts: 20,
	},
	iCivInca : {
		iConstruction: 40,
		iCalendar: 40,
		
		iFeudalism: -40,
		iMachinery: -20,
		iGunpowder: -20,
		iGuilds: -20,
	},
	iCivItaly : {
		iRadio: 20,
		iPsychology: 20,
		iFinance: 20,
		iOptics: 20,
		iPatronage: 20,
		iReplaceableParts: 20,
		iHumanities: 20,
		iAcademia: 20,
		iFission: 12,
	},
	iCivNigeria : {
	},
	iCivMongols : {
		iPaper: 15,
		
		iFirearms: -40,
		iCombinedArms: -40,
	},
	iCivAztecs : {
		iConstruction: 40,
		iLiterature: 20,
		
		iGuilds: -40,
		iFeudalism: -20,
		iMachinery: -20,
		iGunpowder: -20,
	},
	iCivOttomans : {
		iGunpowder: 30,
		iFirearms: 30,
		iCombinedArms: 30,
		iJudiciary: 20,
	},
	iCivRussia : {
		iMacroeconomics: 30,
		iCombinedArms: 30,
		iReplaceableParts: 30,
		iHeritage: 15,
		iPatronage: 15,
		iUrbanPlanning: 15,
		iFission: 12,
		
		iPhilosophy: -20,
		iPrinting: -20,
		iCivilLiberties: -20,
		iSocialContract: -20,
		iRepresentation: -20,
	},
	iCivThailand : {
		iCartography: -50,
		iExploration: -50,
	},
	iCivSweden : {
		iMachinery: 30,
		iCivilService: 30,
		iCompass: 20,
		iCombinedArms: 20,
	},
	iCivNetherlands : {
		iExploration: 20,
		iFirearms: 20,
		iOptics: 20,
		iGeography: 20,
		iReplaceableParts: 20,
		iLogistics: 20,
		iEconomics: 20,
		iCivilLiberties: 20,
		iHumanities: 20,
		iAcademia: 20,
		iChemistry: 15,
	},
	iCivManchuria : {
		iAesthetics: 40,
		iContract: 40,
		iGunpowder: 20,
		iPrinting: 20,
		iPaper: 20,
		iCompass: 20,
		iConstruction: 20,
		iCivilService: 15,
		
		iCivilLiberties: -100,
		iHumanities: -100,
		iAcademia: -100,
		iFirearms: -50,
		iCompanies: -40,
		iExploration: -40,
		iOptics: -40,
		iGeography: -40,
		iTheology: -40,
		iEducation: -40,
		iLogistics: -40,
		iCombinedArms: -40,
		iDivination: -20,
		iSailing: -20,	
	},
	iCivGermany : {
		iEngine: 20,
		iInfrastructure: 20,
		iChemistry: 20,
		iAssemblyLine: 20,
		iPsychology: 20,
		iSociology: 20,
		iSynthetics: 20,
		iFission: 12,
	},
	iCivAmerica : {
		iRailroad: 30,
		iRepresentation: 30,
		iEconomics: 20,
		iAssemblyLine: 20,
		iFission: 12,
	},
	iCivArgentina : {
		iRefrigeration: 30,
		iTelevision: 20,
		iElectricity: 20,
		iPsychology: 20,
	},
	iCivBrazil : {
		iRadio: 20,
		iSynthetics: 20,
		iElectricity: 20,
		iEngine: 20,
	},
	iCivAustralia : {
		iRefrigeration : 30,
		iTelevision : 30,
	},
	iCivBoers : {
	},
}

### Building Preferences ###

dDefaultWonderPreferences = {
	iCivEgypt: -15,
	iCivNubia: -15,
	iCivBabylonia: -40,
	iCivHarappa: -15,
	iCivNorteChico: -40,
	iCivGreece: -15,
	iCivIndia: -15,
	iCivCeltia: -40,
	iCivRome: -20,
	iCivInuit: -40,
	iCivArabia: -15,
	iCivIndonesia: -15,
	iCivBurma: -15,
	iCivKhazars: -15,
	iCivFrance: -12,
	iCivOman: -20,
	iCivKhmer: -15,
	iCivMuisca : -10,
	iCivEngland: -12,
	iCivRussia: -12,
	iCivThailand: -15,
	iCivCongo: -20,
	iCivNetherlands: -12,
	iCivAmerica: -12,
}

dBuildingPreferences = {
	iCivEgypt : {
		iPyramids: 50,
		iGreatLibrary: 30,
		iGreatLighthouse: 30,
		iGreatSphinx: 30,
	},
	iCivNubia : {
		iPyramids: 100,
	},
	iCivBabylonia : {
		iHangingGardens: 50,
		iIshtarGate: 50,
		iSpiralMinaret: 20,
		iGreatMausoleum: 15,
		
		iPyramids: 0,
		iGreatSphinx: 0,
		
		iOracle: -60,
	},
	iCivHarappa : {
		iHangingGardens : 20,
		iGreatSphinx : 0,
		
		iPyramids : -50,
	},
	iCivChina : {
		iGreatWall: 80,
		iForbiddenPalace: 40,
		iGrandCanal: 40,
		iOrientalPearlTower: 40,
		iDujiangyan: 30,
		iTerracottaArmy: 30,
		iPorcelainTower: 30,
		
		iHangingGardens: -30,
		iHimejiCastle: -30,
		iBorobudur: -30,
		iBrandenburgGate: -30,
	},
	iCivGreece : {
		iColossus: 30,
		iOracle: 30,
		iParthenon: 30,
		iTempleOfArtemis: 30,
		iStatueOfZeus: 30,
		iGreatMausoleum: 20,
		iMountAthos: 20,
		iHagiaSophia: 20,
		iAlKhazneh: 15,
		
		iPyramids: -100,
		iGreatCothon: -80,
	},
	iCivIndia : {
		iKhajuraho: 30,
		iIronPillar: 30,
		iVijayaStambha: 30,
		iNalanda: 30,
		iLotusTemple: 30,
		iTajMahal: 20,
		iWatPreahPisnulok: 20,
		iShwedagonPaya: 20,
		iHarmandirSahib: 20,
		iJetavanaramaya: 20,
		iSalsalBuddha: 20,
		iPotalaPalace: 20,
		iBorobudur: 15,
		iPrambanan: 15,
		
		iParthenon: -30,
		iStatueOfZeus: -20,
	},
	iCivCarthage : {
		iGreatCothon: 30,
		iGreatLighthouse: 15,
		iColossus: 15,
		
		iPyramids: -50,
	},
	iCivPolynesia : {
		iMoaiStatues: 30,
	},
	iCivPersia : {
		iApadanaPalace: 30,
		iGreatMausoleum: 30,
		iGondeshapur: 30,
		iAlamut: 30,
		iHangingGardens: 15,
		iColossus: 15,
		iOracle: 15,
	},
	iCivCeltia : {
		iParthenon: -20,
	},
	iCivRome : {
		iFlavianAmphitheatre: 30,
		iAquaAppia: 30,
		iSantaMariaDelFiore: 30,
		iSistineChapel: 30,
		iSanMarcoBasilica: 30,
		iAlKhazneh: 20,
		
		iGreatWall: -100,
	},
	iCivMaya : {
		iTempleOfKukulkan: 40,
	},
	iCivTamils : {
		iJetavanaramaya: 30,
		iKhajuraho: 20,
	},
	iCivEthiopia : {
		iMonolithicChurch: 40,
	},
	iCivVietnam : {
	},
	iCivTeotihuacan : {
		iPyramidOfTheSun: 40,
	},
	iCivKorea : {
		iCheomseongdae: 30,
	},
	iCivMississippi : {
		iSerpentMound : 40,
		iGateOfTheSun : -20,
		iPyramidOfTheSun : -20,
		iMachuPicchu : -20,
		iTempleOfKukulkan : -20
	},
	iCivTiwanaku : {
		iGateOfTheSun : 40,
	},
	iCivByzantium : {
		iHagiaSophia: 40,
		iTheodosianWalls: 30,
		iMountAthos: 30,
		
		iNotreDame: -20,
		iSistineChapel: -20,
	},
	iCivWari : {
		iPyramidOfTheSun: 20,
	},
	iCivJapan : {
		iItsukushimaShrine: 30,
		iHimejiCastle: 30,
		iTsukijiFishMarket: 30,
		iSkytree: 30,
	
		iShwedagonPaya: -100,
		iGreatWall: -100,
	},
	iCivTurks : {
		iGurEAmir: 40,
		iSalsalBuddha: 20,
		iImageOfTheWorldSquare: 20,
	},
	iCivVikings : {
		iNobelPrize: 30,
		iGlobalSeedVault: 30,
		iCERN: 15,
	},
	iCivArabia: {
		iSpiralMinaret: 40,
		iDomeOfTheRock: 40,
		iHouseOfWisdom: 40,
		iBurjKhalifa: 40,
		iAlamut: 30,
	
		iTopkapiPalace: -80,
		iMezquita: -50,
	},
	iCivTibet : {
		iPotalaPalace: 40,
	},
	iCivIndonesia : {
		iBorobudur: 40,
		iPrambanan: 40,
		iGardensByTheBay: 40,
		iShwedagonPaya: 20,
		iWatPreahPisnulok: 20,
		iNalanda: 20,
	},
	iCivBurma : {
		iShwedagonPaya: 40,
		iWatPreahPisnulok: 20,
		iTajMahal: 20,
		iBorobudur: 20,
		iPrambanan: 20,
		iNalanda: 20,
	},
	iCivKhazars : {
		
	},
	iCivChad : {
	},
	iCivMoors : {
		iMezquita: 100,
		
		iUniversityOfSankore: -40,
		iSpiralMinaret: -40,
		iTopkapiPalace: -40,
		iBlueMosque: -40,
	},
	iCivSpain : {
		iEscorial: 30,
		iGuadalupeBasilica: 30,
		iChapultepecCastle: 30,
		iSagradaFamilia: 30,
		iCristoRedentor: 20,
		iWembley: 20,
		iIberianTradingCompanyBuilding: 20,
		iTorreDeBelem: 15,
		iNotreDame: 15,
		iMezquita: 15,
	},
	iCivFrance : {
		iTradingCompanyBuilding: 40,
		iNotreDame: 40,
		iEiffelTower: 30,
		iVersailles: 30,
		iLouvre: 30,
		iTriumphalArch: 30,
		iMetropolitain: 30,
		iCERN: 30,
		iKrakDesChevaliers: 30,
		iChannelTunnel: 30,
		iPalaceOfNations: 20,
		iBerlaymont: 20,
		iLargeHadronCollider: 20,
		iITER: 20,
	},
	iCivOman: {
	},
	iCivKhmer : {
		iWatPreahPisnulok: 30,
		iShwedagonPaya: 30,
		iTajMahal: 20,
		iBorobudur: 20,
		iPrambanan: 20,
		iNalanda: 20,
	},
	iCivMuisca : {
	
	},
	iCivEngland : {
		iTradingCompanyBuilding: 50,
		iOxfordUniversity: 30,
		iWembley: 30,
		iWestminsterPalace: 30,
		iTrafalgarSquare: 30,
		iBellRockLighthouse: 30,
		iCrystalPalace: 30,
		iChannelTunnel: 30,
		iBletchleyPark: 20,
		iAbbeyMills: 20,
		iMetropolitain: 20,
		iNationalGallery: 20,
		iKrakDesChevaliers: 20,
		iHarbourOpera: 20,
	},
	iCivHolyRome : {
		iSaintThomasChurch: 30,
		iKrakDesChevaliers: 20,
		iNeuschwanstein: 20,
		iPalaceOfNations: 20,
		iNotreDame: 15,
	},
	iCivKievanRus : {
		iKremlin: 40,
		iSaintBasilsCathedral: 40,
		iLubyanka: 40,
		iHermitage: 40,
		iMotherlandCalls: 30,
		iAmberRoom: 30,
		iSaintSophia: 30,
		iMountAthos: 20,
		iMetropolitain: 20,
	},
	iCivPhilippines : {
	},
	iCivChimu : {
		iGateOfTheSun : -40,
		iPyramidOfTheSun: -40,
		iMachuPicchu: -20,
		iTempleOfKukulkan: -20,
	},
	iCivSwahili : {
	},
	iCivMamluks : {
		iMezquita : -20,
		iTopkapiPalace: -20,
		iUniversityOfSankore : -20,
		iSpiralMinaret : -20,
		iBlueMosque : -20,
		iDomeOfTheRock : -20,
	},
	iCivMali : {
		iUniversityOfSankore: 40,
	},
	iCivPoland : {
		iSaltCathedral: 30,
		iOldSynagogue: 30,
	},
	iCivZimbabwe : {
		iGreatZimbabwe : 30,
	},
	iCivPortugal : {
		iCristoRedentor: 40,
		iTorreDeBelem: 40,
		iIberianTradingCompanyBuilding: 40,
		iWembley: 20,
		iEscorial: 20,
		iNotreDame: 15,
	},
	iCivInca : {
		iMachuPicchu: 40,
		iTempleOfKukulkan: 20,
	},
	iCivItaly : {
		iFlavianAmphitheatre: 30,
		iSantaMariaDelFiore: 30,
		iSistineChapel: 30,
		iSanMarcoBasilica: 30,
		iMoleAntonelliana: 30,
	},
	iCivNigeria: {
	},
	iCivMongols : {
		iSilverTreeFountain: 40,
	},
	iCivOttomans : {
		iTopkapiPalace: 60,
		iBlueMosque: 60,
		iHagiaSophia: 20,
		iGurEAmir: 20,
		
		iTajMahal: -40,
		iRedFort: -40,
		iSaintBasilsCathedral: -40,
	},
	iCivRussia : {
		iKremlin: 40,
		iSaintBasilsCathedral: 40,
		iLubyanka: 40,
		iHermitage: 40,
		iMotherlandCalls: 30,
		iAmberRoom: 30,
		iSaintSophia: 30,
		iMountAthos: 20,
		iMetropolitain: 20,
	},
	iCivAztecs : {
		iFloatingGardens: 40,
		iTempleOfKukulkan: 30,
		
		iMachuPicchu: -40,
	},
	iCivMughals : {
		iTajMahal: 40,
		iRedFort: 40,
		iShalimarGardens: 40,
		iHarmandirSahib: 20,
		iVijayaStambha: 20,
		
		iBlueMosque: -80,
		iTopkapiPalace: -80,
		iMezquita: -50,
	},
	iCivThailand : {
		iEmeraldBuddha: 40,
		iWatPreahPisnulok: 30,
		iShwedagonPaya: 30,
		iTajMahal: 20,
		iBorobudur: 20,
		iGreatCothon: 15,
	},
	iCivIran: {
		iImageOfTheWorldSquare: 30,
		iShalimarGardens: 20,
	},
	iCivSweden: {
		iCERN: 15,
	},
	iCivNetherlands : {
		iTradingCompanyBuilding: 60,
		iBourse: 40,
		iDeltaWorks: 40,
		iAtomium: 30,
		iBerlaymont: 30,
		iNationalGallery: 20,
		iWembley: 20,
		iCERN: 20,
		iPalaceOfNations: 20,
		iNotreDame: 15,
	},
	iCivManchuria: {
		iForbiddenPalace : 40,
		iGrandCanal : 40,
		iGreatWall : 80,
		iTerracottaArmy : 20,
		iPorcelainTower : 20,
		iHangingGardens : -30,
		iHimejiCastle : -30,
		iBorobudur : -30,
		iBrandenburgGate : -30,
	},
	iCivGermany : {
		iBrandenburgGate: 40,
		iAmberRoom: 30,
		iNeuschwanstein: 30,
		iWembley: 20,
		iCERN: 20,
		iIronworks: 15,
	},
	iCivAmerica : {
		iStatueOfLiberty: 30,
		iHollywood: 30,
		iPentagon: 30,
		iEmpireStateBuilding: 30,
		iBrooklynBridge: 30,
		iGoldenGateBridge: 30,
		iWorldTradeCenter: 30,
		iHubbleSpaceTelescope: 20,
		iCrystalCathedral: 20,
		iMenloPark: 20,
		iUnitedNations: 20,
		iGraceland: 20,
		iMetropolitain: 20,
	},
	iCivMexico : {
		iGuadalupeBasilica: 40,
		iChapultepecCastle: 40,
		iLasLajasSanctuary: 20,
	},
	iCivArgentina : {
		iGuadalupeBasilica: 30,
		iLasLajasSanctuary: 30,
		iWembley: 20,
	},
	iCivColombia : {
		iLasLajasSanctuary: 40,
		iGuadalupeBasilica: 30,
	},
	iCivBrazil : {
		iCristoRedentor: 30,
		iItaipuDam: 30,
		iWembley: 20,
	},
	iCivAustralia: {
		iWembley : 20,
		iHarbourOpera : 20,
	},
	iCivBoers: {
	},
	iCivCanada : {
		iFrontenac: 30,
		iCNTower: 30,
	},
}
