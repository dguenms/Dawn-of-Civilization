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
	
### General functions ###
		
def initBirthYear(iPlayer):
	gc.getPlayer(iPlayer).setBirthYear(tBirth[iPlayer])

def init():
	for iPlayer in range(iNumPlayers):
		initBirthYear(iPlayer)
		initPlayerTechPreferences(iPlayer)

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
iCivTurks :	Techs([iFirearms, iLogistics, iHeritage], column=9),
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

### Tech Preferences ###

dTechPreferences = {
	iCivEgypt : {
		iMasonry: 30,
		iDivination: 20,
		iPhilosophy: 20,
		iPriesthood: 20,
		
		iAlloys: -20,
		iBloomery: -50,
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
	iCivGreece : {
		iSailing: 40,
		iShipbuilding: 40,
		iNavigation: 40,
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
	iCivRome : {
		iTheology: 30,
		iCurrency: 20,
		iLaw: 20,
		iPolitics: 20,
		iConstruction: 15,
		iEngineering: 15,
		
		iCalendar: -20,
	},
	iCivTamils : {
		iCement: 20,
		iCompass: 20,
		iCalendar: 20,
		
		iScientificMethod: -20,
		iAcademia: -20,
		iReplaceableParts: -20,
	},
	iCivKorea : {
		iPrinting: 30,
		iGunpowder: 30,
	
		iOptics: -40,
		iExploration: -40,
		iReplaceableParts: -40,
		iScientificMethod: -40,
	},
	iCivMaya : {
		iCalendar: 40,
		iAesthetics: 30,
	},
	iCivByzantium : {
		iFinance: -50,
		iOptics: -20,
		iFirearms: -20,
		iExploration: -20,
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
	iCivKhmer : {
		iPhilosophy: 30,
		iSailing: 30,
		iCalendar: 30,
		iCivilService: 30,
		iAesthetics: 20,
		
		iCurrency: -30,
		iExploration: -30,
	},
	iCivEngland : {
		iExploration: 40,
		iGeography: 40,
		iFirearms: 40,
		iReplaceableParts: 30,
		iLogistics: 30,
		iCivilLiberties: 20,
		iEducation: 15,
		iGuilds: 15,
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
	iCivThailand : {
		iCartography: -50,
		iExploration: -50,
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
}