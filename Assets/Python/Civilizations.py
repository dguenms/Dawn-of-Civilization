from Consts import *
from RFCUtils import *
from sets import Set
from StoredData import data
import Victory as vic
from Religions import rel

### Class for easier tech specification ###

# TODO: cover this in Core
class Techs:

	def __init__(self, techs=[], column=0, era=-1, exceptions=[]):
		self.column = column
		self.era = era
		self.techs = techs
		self.exceptions = exceptions
		
	def list(self):
		lTechs = Set()
		lTechs.update([i for i in range(iNumTechs) if infos.tech(i).getGridX() <= self.column])
		lTechs.update([i for i in range(iNumTechs) if infos.tech(i).getEra() <= self.era])
		lTechs.update(self.techs)
		lTechs.difference_update(self.exceptions)
		
		return list(lTechs)

### Starting tech methods ###

def getScenarioTechs(iScenario, iPlayer):
	iCivilization = civ(iPlayer)
	for iScenarioType in reversed(range(iScenario+1)):
		if iCivilization in lStartingTechs[iScenarioType]:
			return lStartingTechs[iScenarioType][iCivilization].list()
			
def getStartingTechs(iPlayer):
	return getScenarioTechs(scenario(), iPlayer)
	
def initScenarioTechs(iScenario):
	for iPlayer in players.major():
		iCiv = civ(iPlayer)
		if dBirth[iCiv] > scenarioStartYear(): continue
	
		if iCiv in lStartingTechs[iScenario]:
			initTechs(iPlayer, lStartingTechs[iScenario][iCiv].list())
			
def initPlayerTechs(iPlayer):
	initTechs(iPlayer, getStartingTechs(iPlayer))
	
	if civ(iPlayer) == iChina and scenario() == i3000BC and not player(iPlayer).isHuman():
		initTech(iPlayer, iProperty)
		initTech(iPlayer, iAlloys)
				
def initTechs(iPlayer, lTechs):
	pPlayer = player(iPlayer)

	for iTech in lTechs:
		initTech(iPlayer, iTech)
	
	iCurrentEra = pPlayer.getCurrentEra()
	pPlayer.setStartingEra(iCurrentEra)
	
def initTech(iPlayer, iTech):
	team(iPlayer).setHasTech(iTech, True, iPlayer, False, False)
	vic.onTechAcquired(iPlayer, iTech)
	rel.onTechAcquired(iPlayer, iTech)

### Tech preference functions ###

def getDictValue(dDict, key):
	if key not in dDict: return 0
	
	return dDict[key]

def getTechPreferences(iPlayer):
	dPreferences = {}
	iCivilization = civ(iPlayer)
	
	if iCivilization not in dTechPreferences:
		return dPreferences
		
	for iTech, iValue in dTechPreferences[iCivilization].items():
		dPreferences[iTech] = iValue
		
	for iTech, iValue in dTechPreferences[iCivilization].items():
		for i in range(4):
			iOrPrereq = infos.tech(iTech).getPrereqOrTechs(i)
			iAndPrereq = infos.tech(iTech).getPrereqAndTechs(i)
			
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
		player(iPlayer).setTechPreference(iTech, iValue)

### Wonder preference methods ###

def initBuildingPreferences(iPlayer):
	pPlayer = player(iPlayer)
	iCiv = civ(iPlayer)
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
	player(iPlayer).setInitialBirthTurn(year(dBirth[iPlayer]))

def init():
	for iPlayer in players.major():
		initBirthYear(iPlayer)
		initPlayerTechPreferences(iPlayer)
		initBuildingPreferences(iPlayer)

### Starting technologies ###

lStartingTechs = [
{
iNative : 	Techs([iTanning, iMythology]),
iEgypt :	Techs([iMining, iPottery, iAgriculture]),
iBabylonia :	Techs([iPottery, iPastoralism, iAgriculture]),
iHarappa : 	Techs([iMining, iPottery, iAgriculture]),
iChina :	Techs([iTanning, iMining, iAgriculture, iPastoralism, iPottery, iMythology, iSmelting, iLeverage]),
iIndia :	Techs([iAlloys, iWriting, iCalendar], column=2, exceptions=[iSeafaring]),
iGreece :	Techs([iAlloys, iArithmetics, iWriting], column=2),
iPersia :	Techs([iBloomery, iPriesthood], column=3, exceptions=[iSeafaring, iShipbuilding]),
iCarthage :	Techs([iAlloys, iWriting, iShipbuilding], column=2),
iPolynesia :	Techs([iTanning, iMythology, iSailing, iSeafaring]),
iRome : 	Techs([iBloomery, iCement, iMathematics, iLiterature], column=3, exceptions=[iRiding, iCalendar, iShipbuilding]),
iMaya :	Techs([iProperty, iMasonry, iSmelting, iCeremony], column=1, exceptions=[iSailing]),
iTamils :	Techs([iBloomery, iMathematics, iContract, iPriesthood], column=3),
iEthiopia :	Techs([iAlloys, iWriting, iCalendar, iPriesthood], column=2),
iKorea :	Techs(column=5, exceptions=[iGeneralship, iEngineering, iCurrency]),
iByzantium :	Techs([iArchitecture, iPolitics, iEthics], column=5),
iJapan :	Techs([iNobility, iSteel, iArtisanry, iPolitics], column=5),
iVikings : 	Techs([iNobility, iSteel, iArtisanry, iPolitics, iScholarship, iArchitecture, iGuilds], column=5),
iTurks :	Techs([iNobility, iSteel], column=5, exceptions=[iNavigation, iMedicine, iPhilosophy]),
iArabia :	Techs([iAlchemy, iTheology], column=6, exceptions=[iPolitics]),
iTibet :	Techs([iNobility, iScholarship, iEthics], column=5),
iIndonesia :	Techs([iEthics], column=5, exceptions=[iGeneralship]),
iMoors :	Techs([iMachinery, iAlchemy, iTheology], column=6, exceptions=[iPolitics]),
iSpain : 	Techs([iFeudalism, iAlchemy, iGuilds], column=6),
iFrance :	Techs([iFeudalism, iTheology], column=6),
iKhmer :	Techs([iNobility, iArchitecture, iArtisanry, iScholarship, iEthics], column=5),
iEngland :	Techs([iFeudalism, iTheology], column=6),
iHolyRome :	Techs([iFeudalism, iTheology], column=6),
iRussia :	Techs([iFeudalism], column=6, exceptions=[iPolitics, iScholarship, iEthics]),
iMali : 	Techs([iTheology], column=6),
iPoland : 	Techs([iFeudalism, iFortification, iCivilService, iTheology], column=6),
iPortugal :	Techs([iPatronage], column=7),
iInca : 	Techs([iMathematics, iContract, iLiterature, iPriesthood], column=3, exceptions=[iSeafaring, iAlloys, iRiding, iShipbuilding]),
iMongols :	Techs([iPaper, iCompass], column=7, exceptions=[iTheology]),
iAztecs :	Techs([iMathematics, iContract, iLiterature, iPriesthood, iGeneralship, iAesthetics, iCurrency, iLaw], column=3, exceptions=[iSeafaring, iAlloys, iRiding, iShipbuilding]),
iItaly : 	Techs([iCommune, iPaper, iCompass, iDoctrine], column=7),
iMughals :	Techs([iCommune, iCropRotation, iDoctrine, iGunpowder], column=7),
iOttomans :	Techs([iCommune, iCropRotation, iPaper, iDoctrine, iGunpowder], column=7),
iCongo : 	Techs([iMachinery, iCivilService, iTheology], column=6),
iThailand : 	Techs(column=8, exceptions=[iCompass, iDoctrine, iCommune, iPatronage]),
iIran : 	Techs([iHeritage, iFirearms], column=9),
iNetherlands:Techs(column=10),
iGermany :	Techs(column=11, exceptions=[iGeography, iCivilLiberties, iHorticulture, iUrbanPlanning]),
iAmerica :	Techs([iRepresentation, iChemistry], column=12),
iArgentina :	Techs([iRepresentation, iNationalism], column=12),
iMexico :	Techs([iRepresentation, iNationalism], column=12),
iColombia :	Techs([iRepresentation, iNationalism], column=12),
iBrazil :	Techs([iRepresentation, iNationalism, iBiology], column=12),
iCanada :	Techs([iBallistics, iEngine, iRailroad, iJournalism], column=13),
},
{
iIndependent:Techs(column=5),
iIndependent2:Techs(column=5),
iChina :	Techs([iMachinery, iAlchemy, iCivilService], column=6, exceptions=[iNobility]),
iKorea :	Techs([iMachinery], column=6, exceptions=[iScholarship]),
iByzantium :	Techs([iFortification,iMachinery, iCivilService], column=6),
iJapan :	Techs(column=6, exceptions=[iScholarship]),
iVikings :	Techs([iGuilds], column=6),
iTurks :	Techs([iNobility, iSteel], column=5, exceptions=[iNavigation, iMedicine, iPhilosophy]),
},
{
iIndependent:Techs(column=10),
iIndependent2:Techs(column=10),
iChina :	Techs([iHorticulture, iUrbanPlanning], column=10, exceptions=[iExploration, iOptics, iAcademia]),
iIndia : 	Techs([iCombinedArms, iUrbanPlanning], column=10, exceptions=[iExploration]),
iTamils :	Techs([iCombinedArms, iUrbanPlanning], column=10, exceptions=[iExploration, iOptics]),
iIran :	Techs([iCombinedArms, iGeography, iUrbanPlanning, iHorticulture], column=10),
iKorea :	Techs(column=10, exceptions=[iExploration, iOptics, iAcademia]),
iJapan :	Techs([iCombinedArms, iUrbanPlanning], column=10, exceptions=[iExploration, iOptics]),
iVikings :	Techs(column=11, exceptions=[iEconomics, iHorticulture]),
iTurks :	Techs([iFirearms, iLogistics, iHeritage], column=9),
iSpain :	Techs([iCombinedArms, iGeography, iHorticulture], column=10),
iFrance :	Techs(column=11, exceptions=[iUrbanPlanning, iEconomics]),
iEngland :	Techs(column=11, exceptions=[iUrbanPlanning, iHorticulture]),
iHolyRome :	Techs([iCombinedArms, iUrbanPlanning, iHorticulture], column=10, exceptions=[iExploration]),
iRussia : 	Techs([iCombinedArms, iUrbanPlanning], column=10, exceptions=[iExploration, iOptics]),
iPoland :	Techs(column=11, exceptions=[iEconomics, iGeography, iHorticulture, iUrbanPlanning]),
iPortugal :	Techs([iGeography, iHorticulture], column=10),
iOttomans :	Techs([iUrbanPlanning, iHorticulture], column=10, exceptions=[iExploration]),
iMughals :	Techs([iUrbanPlanning, iHorticulture], column=10, exceptions=[iExploration, iOptics]),
iThailand :	Techs(column=10, exceptions=[iExploration, iOptics]),
iCongo :	Techs([iCartography, iJudiciary], column=8),
iNetherlands:Techs(column=11, exceptions=[iHorticulture, iScientificMethod, iUrbanPlanning]),
iGermany :	Techs(column=11, exceptions=[iGeography, iCivilLiberties, iHorticulture, iUrbanPlanning]),
}]

### Tech Preferences ###

dTechPreferences = {
	iEgypt : {
		iMasonry: 30,
		iDivination: 20,
		iPhilosophy: 20,
		iPriesthood: 20,
		
		iAlloys: -20,
		iBloomery: -50,
	},
	iBabylonia : {
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
	iHarappa : {
		iMasonry: 20,
		iPastoralism: 20,
		iPottery: 20,
		
		iMythology: -50,
		iDivination: -50,
		iCeremony: -50,
	},
	iChina : {
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
	iGreece : {
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
	iIndia : {
		iCeremony: 200,
		iPriesthood: 200,
		iPhilosophy: 50,
		
		iEngineering: -20,
		iTheology: -20,
		iCivilService: -20,
	},
	iCarthage : {
		iNavigation: 40,
		iRiding: 30,
		iCurrency: 30,
		iCompass: 20,
	},
	iPolynesia : {
		iCompass: 20,
		iDivination: 20,
		iMasonry: 20,
		
		iAlloys: -30,
		iBloomery: -30,
	},
	iPersia : {
		iFission: 15,
	
		iTheology: -40,
	},
	iRome : {
		iTheology: 30,
		iCurrency: 20,
		iLaw: 20,
		iPolitics: 20,
		iConstruction: 15,
		iEngineering: 15,
		
		iCalendar: -20,
	},
	iMaya : {
		iCalendar: 40,
		iAesthetics: 30,
	},
	iTamils : {
		iCement: 20,
		iCompass: 20,
		iCalendar: 20,
		
		iScientificMethod: -20,
		iAcademia: -20,
		iReplaceableParts: -20,
	},
	iKorea : {
		iPrinting: 30,
		iGunpowder: 30,
	
		iOptics: -40,
		iExploration: -40,
		iReplaceableParts: -40,
		iScientificMethod: -40,
	},
	iByzantium : {
		iFinance: -50,
		iOptics: -20,
		iFirearms: -20,
		iExploration: -20,
	},
	iJapan : {
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
	iVikings : {
		iMachinery: 30,
		iCivilService: 30,
		iCompass: 20,
		iCombinedArms: 20,
	},
	iArabia : {
		iScholarship: 30,
		iAlchemy: 30,
		
		iFinance: -50,
		iFirearms: -50,
		iCompanies: -50,
		iPaper: -20,
	},
	iTibet : {
		iPhilosophy: 30,
		iEngineering: 20,
		iPaper: 20,
		iTheology: 20,
		iDoctrine: 20,
	},
	iIndonesia : {
		iAesthetics: 30,
		iArtisanry: 30,
		iExploration: -20,
	},
	iMoors : {
		iCivilService: 20,
	
		iExploration: -40,
		iGuilds: -40,
	},
	iSpain : {
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
	iFrance : {
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
	iKhmer : {
		iPhilosophy: 30,
		iSailing: 30,
		iCalendar: 30,
		iCivilService: 30,
		iAesthetics: 20,
		
		iCurrency: -30,
		iExploration: -30,
	},
	iEngland : {
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
	iHolyRome : {
		iAcademia: 50,
		iPrinting: 50,
		iFirearms: 20,
		iReplaceableParts: 20,
		iEducation: 15,
		iGuilds: 15,
		iOptics: 15,
		iFission: 12,
	},
	iRussia : {
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
	iMali : {
		iEducation: 30,
	},
	iMughals : {
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
	iPoland : {
		iCombinedArms: 30,
		iCivilLiberties: 30,
		iSocialContract: 20,
		iOptics: 20,
	},
	iPortugal : {
		iCartography: 100,
		iExploration: 100,
		iGeography: 100,
		iCompass: 100,
		iFirearms: 100,
		iCompanies: 50,
		iPatronage: 50,
		iReplaceableParts: 20,
	},
	iInca : {
		iConstruction: 40,
		iCalendar: 40,
		
		iFeudalism: -40,
		iMachinery: -20,
		iGunpowder: -20,
		iGuilds: -20,
	},
	iItaly : {
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
	iMongols : {
		iPaper: 15,
		
		iFirearms: -40,
		iCombinedArms: -40,
	},
	iAztecs : {
		iConstruction: 40,
		iLiterature: 20,
		
		iGuilds: -40,
		iFeudalism: -20,
		iMachinery: -20,
		iGunpowder: -20,
	},
	iOttomans : {
		iGunpowder: 30,
		iFirearms: 30,
		iCombinedArms: 30,
		iJudiciary: 20,
	},
	iThailand : {
		iCartography: -50,
		iExploration: -50,
	},
	iNetherlands : {
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
	iGermany : {
		iEngine: 20,
		iInfrastructure: 20,
		iChemistry: 20,
		iAssemblyLine: 20,
		iPsychology: 20,
		iSociology: 20,
		iSynthetics: 20,
		iFission: 12,
	},
	iAmerica : {
		iRailroad: 30,
		iRepresentation: 30,
		iEconomics: 20,
		iAssemblyLine: 20,
		iFission: 12,
	},
	iArgentina : {
		iRefrigeration: 30,
		iTelevision: 20,
		iElectricity: 20,
		iPsychology: 20,
	},
	iBrazil : {
		iRadio: 20,
		iSynthetics: 20,
		iElectricity: 20,
		iEngine: 20,
	},
}

### Building Preferences ###

dDefaultWonderPreferences = {
	iEgypt: -15,
	iBabylonia: -40,
	iGreece: -15,
	iIndia: -15,
	iRome: -20,
	iArabia: -15,
	iIndonesia: -15,
	iFrance: -12,
	iKhmer: -15,
	iEngland: -12,
	iRussia: -12,
	iThailand: -15,
	iCongo: -20,
	iNetherlands: -12,
	iAmerica: -12,
}

dBuildingPreferences = {
	iEgypt : {
		iPyramids: 100,
		iGreatLibrary: 30,
		iGreatLighthouse: 30,
		iGreatSphinx: 30,
	},
	iBabylonia : {
		iHangingGardens: 50,
		iIshtarGate: 50,
		iSpiralMinaret: 20,
		iGreatMausoleum: 15,
		
		iPyramids: 0,
		iGreatSphinx: 0,
		
		iOracle: -60,
	},
	iChina : {
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
	iGreece : {
		iColossus: 30,
		iOracle: 30,
		iParthenon: 30,
		iTempleOfArtemis: 30,
		iStatueOfZeus: 30,
		iGreatMausoleum: 20,
		iMountAthos: 20,
		iHagiaSophia: 20,
		iAlKhazneh: 15,
		iGreatLibrary: 15,
		iGreatLighthouse: 15,
		
		iPyramids: -100,
		iGreatCothon: -80,
	},
	iIndia : {
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
	iCarthage : {
		iGreatCothon: 30,
		iGreatLighthouse: 15,
		iColossus: 15,
		
		iPyramids: -50,
	},
	iPolynesia : {
		iMoaiStatues: 30,
	},
	iPersia : {
		iApadanaPalace: 30,
		iGreatMausoleum: 30,
		iGondeshapur: 30,
		iAlamut: 30,
		iHangingGardens: 15,
		iColossus: 15,
		iOracle: 15,
	},
	iRome : {
		iFlavianAmphitheatre: 30,
		iAquaAppia: 30,
		iSantaMariaDelFiore: 30,
		iSistineChapel: 30,
		iSanMarcoBasilica: 30,
		iAlKhazneh: 20,
		
		iGreatWall: -100,
	},
	iMaya : {
		iTempleOfKukulkan: 40,
	},
	iTamils : {
		iJetavanaramaya: 30,
		iKhajuraho: 20,
	},
	iEthiopia : {
		iMonolithicChurch: 40,
	},
	iKorea : {
		iCheomseongdae: 30,
	},
	iByzantium : {
		iHagiaSophia: 40,
		iTheodosianWalls: 30,
		iMountAthos: 30,
		
		iNotreDame: -20,
		iSistineChapel: -20,
	},
	iJapan : {
		iItsukushimaShrine: 30,
		iHimejiCastle: 30,
		iTsukijiFishMarket: 30,
		iSkytree: 30,
	
		iGreatWall: -100,
	},
	iTurks : {
		iGurEAmir: 40,
		iSalsalBuddha: 20,
		iImageOfTheWorldSquare: 20,
	},
	iVikings : {
		iNobelPrize: 30,
		iGlobalSeedVault: 30,
		iCERN: 15,
	},
	iArabia: {
		iSpiralMinaret: 40,
		iDomeOfTheRock: 40,
		iHouseOfWisdom: 40,
		iBurjKhalifa: 40,
		iAlamut: 30,
	
		iTopkapiPalace: -80,
		iMezquita: -50,
	},
	iTibet : {
		iPotalaPalace: 40,
	},
	iIndonesia : {
		iBorobudur: 40,
		iPrambanan: 40,
		iGardensByTheBay: 40,
		iShwedagonPaya: 20,
		iWatPreahPisnulok: 20,
		iNalanda: 20,
	},
	iMoors : {
		iMezquita: 100,
		
		iUniversityOfSankore: -40,
		iSpiralMinaret: -40,
		iTopkapiPalace: -40,
		iBlueMosque: -40,
	},
	iSpain : {
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
	iFrance : {
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
	iKhmer : {
		iWatPreahPisnulok: 30,
		iShwedagonPaya: 30,
		iTajMahal: 20,
		iBorobudur: 20,
		iPrambanan: 20,
		iNalanda: 20,
	},
	iEngland : {
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
	iHolyRome : {
		iSaintThomasChurch: 30,
		iKrakDesChevaliers: 20,
		iNeuschwanstein: 20,
		iPalaceOfNations: 20,
		iNotreDame: 15,
	},
	iRussia : {
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
	iMali : {
		iUniversityOfSankore: 40,
	},
	iPoland : {
		iSaltCathedral: 30,
		iOldSynagogue: 30,
	},
	iPortugal : {
		iCristoRedentor: 40,
		iTorreDeBelem: 40,
		iIberianTradingCompanyBuilding: 40,
		iWembley: 20,
		iEscorial: 20,
		iNotreDame: 15,
	},
	iInca : {
		iMachuPicchu: 40,
		iTempleOfKukulkan: 20,
	},
	iItaly : {
		iFlavianAmphitheatre: 30,
		iSantaMariaDelFiore: 30,
		iSistineChapel: 30,
		iSanMarcoBasilica: 30,
		iMoleAntonelliana: 30,
	},
	iMongols : {
		iSilverTreeFountain: 40,
	},
	iOttomans : {
		iTopkapiPalace: 60,
		iBlueMosque: 60,
		iHagiaSophia: 20,
		iGurEAmir: 20,
		
		iTajMahal: -40,
		iRedFort: -40,
		iSaintBasilsCathedral: -40,
	},
	iAztecs : {
		iFloatingGardens: 40,
		iTempleOfKukulkan: 30,
		
		iMachuPicchu: -40,
	},
	iMughals : {
		iTajMahal: 40,
		iRedFort: 40,
		iShalimarGardens: 40,
		iHarmandirSahib: 20,
		iVijayaStambha: 20,
		
		iBlueMosque: -80,
		iTopkapiPalace: -80,
		iMezquita: -50,
	},
	iThailand : {
		iEmeraldBuddha: 40,
		iWatPreahPisnulok: 30,
		iShwedagonPaya: 30,
		iTajMahal: 20,
		iBorobudur: 20,
		iGreatCothon: 15,
	},
	iIran: {
		iImageOfTheWorldSquare: 30,
		iShalimarGardens: 20,
	},
	iNetherlands : {
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
	iGermany : {
		iBrandenburgGate: 40,
		iAmberRoom: 30,
		iNeuschwanstein: 30,
		iWembley: 20,
		iCERN: 20,
		iIronworks: 15,
	},
	iAmerica : {
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
	iMexico : {
		iGuadalupeBasilica: 40,
		iChapultepecCastle: 40,
		iLasLajasSanctuary: 20,
	},
	iArgentina : {
		iGuadalupeBasilica: 30,
		iLasLajasSanctuary: 30,
		iWembley: 20,
	},
	iColombia : {
		iLasLajasSanctuary: 40,
		iGuadalupeBasilica: 30,
	},
	iBrazil : {
		iCristoRedentor: 30,
		iItaipuDam: 30,
		iWembley: 20,
	},
	iCanada : {
		iFrontenac: 30,
		iCNTower: 30,
	}
}