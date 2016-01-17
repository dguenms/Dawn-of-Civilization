from Consts import *
from RFCUtils import utils

import CvEraMovieScreen

### Starting tech methods ###

def getScenarioTechs(iScenario, iPlayer):
	iCivilization = gc.getPlayer(iPlayer).getCivilizationType()
	for iScenarioType in reversed(range(iScenario+1)):
		if iCivilization in lStartingTechs[iScenarioType]:
			return lStartingTechs[iScenarioType][iCivilization]
			
def getStartingTechs(iPlayer):
	return getScenarioTechs(utils.getScenario(), iPlayer)
	
def initScenarioTechs(iScenario):
	for iPlayer in range(iNumTotalPlayers):
		iCivilization = gc.getPlayer(iPlayer).getCivilizationType()
		if iCivilization in lStartingTechs[iScenario]:
			initTechs(iPlayer, lStartingTechs[iScenario][iCivilization])
			
def initPlayerTechs(iPlayer):
	initTechs(iPlayer, getStartingTechs(iPlayer))
				
def initTechs(iPlayer, lTechs):
	pPlayer = gc.getPlayer(iPlayer)

	for iTech in lTechs:
		gc.getTeam(pPlayer.getTeam()).setHasTech(iTech, True, iPlayer, False, False)
	
	iCurrentEra = pPlayer.getCurrentEra()
	pPlayer.setStartingEra(iCurrentEra)
	
	if pPlayer.isHuman() and iCurrentEra > 0:
		CvEraMovieScreen.CvEraMovieScreen().interfaceScreen(iCurrentEra)
		
def techs(lEraTechs, lExtraTechs=[]):
	lTechs = list(lEraTechs)
	lTechs.extend(lExtraTechs)
	return lTechs
	
### Religion spread factors ###

def getSpreadFactor(iPlayer, iReligion):
	return dSpreadFactors[gc.getPlayer(iPlayer).getCivilizationType()][iReligion]
	
def setSpreadFactor(iPlayer, iReligion, iNewValue):
	gc.getPlayer(iPlayer).setSpreadFactor(iReligion, iNewValue)
	
def initSpreadFactors(iPlayer):
	for iReligion in range(iNumReligions):
		setSpreadFactor(iPlayer, iReligion, getSpreadFactor(iPlayer, iReligion))
		
### General functions ###
		
def initBirthYear(iPlayer):
	gc.getPlayer(iPlayer).setBirthYear(tBirth[iPlayer])

def init():
	for iPlayer in range(iNumPlayers):
		initBirthYear(iPlayer)
		initSpreadFactors(iPlayer)

### Starting technologies ###

lMedievalTechs = [iFishing, iTheWheel, iAgriculture, iHunting, iMysticism, iMining, iSailing, iPottery, iAnimalHusbandry, iArchery, 
		  iMeditation, iPolytheism, iMasonry, iHorsebackRiding, iPriesthood, iMonotheism, iBronzeWorking, iWriting, iMetalCasting, iIronWorking,
		  iAesthetics, iMathematics, iAlphabet, iMonarchy, iCompass, iLiterature, iCalendar, iConstruction, iCurrency, iMachinery,
		  iDrama, iEngineering, iCodeOfLaws, iFeudalism, iMusic, iPhilosophy, iCivilService, iTheology, iOptics, iPatronage, 
		  iDivineRight, iPaper, iGuilds, iEducation, iBanking, iGunpowder]

lStartingTechs = [
{
iCivNative : 	[iHunting, iArchery],
iCivIndia : 	[iMysticism, iFishing, iTheWheel, iAgriculture, iPottery, iHunting, iMining, iWriting, iMeditation, iAnimalHusbandry,
		 iBronzeWorking, iArchery, iSailing],
iCivGreece :	[iMining, iBronzeWorking, iMysticism, iPolytheism, iFishing, iSailing, iTheWheel, iPottery, iWriting, iHunting],
iCivPersia : 	[iMining, iBronzeWorking, iMysticism, iPolytheism, iPriesthood, iMasonry, iFishing, iSailing, iMonotheism, iMonarchy,
		 iTheWheel, iPottery, iWriting, iHunting, iArchery, iHorsebackRiding],
iCivCarthage : 	[iMining, iBronzeWorking, iMysticism, iPolytheism, iPriesthood, iMasonry, iFishing, iSailing, iTheWheel, iPottery, 
		 iWriting, iHunting, iArchery, iAnimalHusbandry, iAlphabet],
iCivPolynesia :	[iMysticism, iFishing, iPottery, iHunting, iSailing],
iCivRome : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMysticism, iPolytheism, iPriesthood, iMasonry, iFishing, iSailing, 
		 iTheWheel, iPottery, iWriting, iAlphabet, iHunting, iAnimalHusbandry, iMathematics],
iCivTamils : 	[iMining, iBronzeWorking, iMysticism, iPolytheism, iMeditation, iPriesthood, iMasonry, iFishing, iSailing, iMonarchy, 
		 iTheWheel, iPottery, iWriting, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iAgriculture, iAesthetics, iIronWorking],
iCivEthiopia : 	[iMining, iBronzeWorking, iMysticism, iPolytheism, iMeditation, iPriesthood, iMonotheism, iMasonry, iFishing, iSailing, 
		 iMonarchy, iTheWheel, iPottery, iWriting, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding],
iCivKorea : 	[iMining, iBronzeWorking, iIronWorking, iMysticism, iPolytheism, iMeditation, iPriesthood, iMasonry, iMonarchy, iFishing, 
		 iSailing, iTheWheel, iPottery, iAgriculture, iWriting, iMathematics, iCalendar, iConstruction, iCurrency, iCodeOfLaws, 
		 iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iAesthetics],	 
iCivMaya : 	[iMining, iMysticism, iPolytheism, iMeditation, iPriesthood, iMasonry, iFishing, iTheWheel, iPottery, iAgriculture, iWriting, 
		 iHunting],
iCivByzantium :	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iTheology, iMonarchy, iFishing, iSailing, iTheWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, iAlphabet, 
		 iMathematics, iConstruction, iCurrency, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iLiterature, iDrama, iAesthetics,
		 iCalendar, iMeditation],
iCivJapan :	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMeditation, iPriesthood, iMasonry, 
		 iMonarchy, iFishing, iSailing, iTheWheel, iPottery, iAgriculture, iWriting, iMathematics, iConstruction, iCurrency, 
		 iCodeOfLaws, iCivilService, iHunting, iArchery, iAnimalHusbandry, iCalendar],
iCivVikings :	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonarchy, 
		 iFishing, iSailing, iTheWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, iFeudalism, iAlphabet, iMathematics, 
		 iConstruction, iCurrency, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding],
iCivArabia : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iTheology, iMonarchy, iDivineRight, iFishing, iTheWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, iFeudalism, 
		 iAlphabet, iMathematics, iConstruction, iCurrency, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iMeditation],
iCivTibet : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iMonarchy, iFishing, iTheWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, iMathematics, iConstruction, iCurrency, 
		 iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iCalendar, iMeditation, iSailing, iTheology],
iCivKhmer : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iMeditation, iPriesthood, 
		 iMonotheism, iMonarchy, iFishing, iTheWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, iMathematics, iConstruction,
		 iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding],
iCivIndonesia :	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iMeditation, iPriesthood, 
		 iMonotheism, iMonarchy, iFishing, iTheWheel, iPottery, iAgriculture, iWriting, iSailing, iCodeOfLaws, iMathematics, 
		 iConstruction, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding],
iCivMoors : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iTheology, iMonarchy, iFishing, iTheWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, iAlphabet, iMathematics, 
		 iConstruction, iCurrency, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iLiterature, iAesthetics, iCalendar, iMeditation, 
		 iSailing, iPhilosophy],
iCivSpain : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iTheology, iMonarchy, iFishing, iSailing, iTheWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, iFeudalism, 
		 iAlphabet, iMathematics, iConstruction, iCurrency, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iCalendar, iMeditation],
iCivFrance : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iTheology, iMonarchy, iFishing, iSailing, iTheWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, iFeudalism, 
		 iAlphabet, iMathematics, iConstruction, iCurrency, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iCalendar, iMeditation],
iCivEngland : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iTheology, iMonarchy, iFishing, iSailing, iTheWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, iFeudalism, 
		 iAlphabet, iMathematics, iConstruction, iCurrency, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iCalendar, iMeditation],
iCivHolyRome :	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iTheology, iMonarchy, iFishing, iTheWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, iFeudalism, iAlphabet, 
		 iMathematics, iConstruction, iCurrency, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iFeudalism, iCalendar, iMeditation, 
		 iSailing],
iCivRussia : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iTheology, iMonarchy, iTheWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, iFeudalism, iAlphabet, iMathematics, 
		 iConstruction, iCurrency, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iCalendar, iMeditation, iFishing, iSailing],
iCivMali : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, iTheology, 
		 iMonarchy, iDivineRight, iTheWheel, iPottery, iAgriculture, iWriting, iAlphabet, iMathematics, iConstruction, iCurrency,
		 iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding],
iCivPoland : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iTheology, iMonarchy, iFishing, iSailing, iTheWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, iFeudalism,
		 iAlphabet, iMathematics, iConstruction, iCurrency, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iMeditation, iAesthetics, 
		 iLiterature, iCalendar, iCivilService],
iCivSeljuks : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iTheology, iMonarchy, iDivineRight, iFishing, iTheWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, iFeudalism, 
		 iAlphabet, iMathematics, iConstruction, iCurrency, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iLiterature, iDrama, 
		 iAesthetics, iMusic, iCalendar],
iCivPortugal : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iTheology, iMonarchy, iDivineRight, iFishing, iSailing, iTheWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, 
		 iFeudalism, iGuilds, iAlphabet, iMathematics, iConstruction, iEngineering, iCurrency, iHunting, iArchery, iAnimalHusbandry,
		 iHorsebackRiding, iCalendar, iMeditation],
iCivInca : 	[iMining, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonarchy, iFishing, iTheWheel, iPottery, iAgriculture, 
		 iWriting, iCodeOfLaws, iMathematics, iCurrency, iHunting, iArchery, iAnimalHusbandry],
iCivMongols : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMeditation, iPriesthood, iMasonry, 
		 iMonarchy, iFishing, iTheWheel, iPottery, iAgriculture, iWriting, iMathematics, iCodeOfLaws, iFeudalism, iMathematics, 
		 iConstruction, iEngineering, iGuilds, iCurrency, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iGunpowder],
iCivAztecs : 	[iMining, iBronzeWorking, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonarchy, iFishing, iTheWheel, iPottery, 
		 iAgriculture, iWriting, iCodeOfLaws, iMathematics, iCalendar, iCurrency, iHunting, iArchery],
iCivItaly : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iTheology, iMonarchy, iFishing, iSailing, iTheWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, iFeudalism, 
		 iGuilds, iAlphabet, iMathematics, iCalendar, iConstruction, iEngineering, iCurrency, iHunting, iArchery, iAnimalHusbandry,
		 iHorsebackRiding, iAesthetics, iLiterature, iCompass, iCivilService, iMeditation],
iCivMughals : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iTheology, iMonarchy, iDivineRight, iFishing, iSailing, iTheWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, 
		 iCivilService, iGunpowder, iAlphabet, iMathematics, iCalendar, iConstruction, iCurrency, iHunting, iArchery, iAnimalHusbandry, 
		 iHorsebackRiding, iGuilds, iAesthetics, iLiterature],
iCivTurkey : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iTheology, iMonarchy, iDivineRight, iFishing, iSailing, iTheWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, 
		 iFeudalism, iCivilService, iGuilds, iGunpowder, iAlphabet, iMathematics, iCalendar, iConstruction, iEngineering, iCurrency, 
		 iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iMeditation],
iCivCongo : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, iTheology, 
		 iMonarchy, iTheWheel, iPottery, iAgriculture, iWriting, iAlphabet, iMathematics, iConstruction, iCurrency, iHunting,
		 iArchery, iAnimalHusbandry, iMachinery, iCivilService, iFishing, iCodeOfLaws],
iCivThailand :	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iTheology, iMonarchy, iDivineRight, iFishing, iSailing, iTheWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, 
		 iCivilService, iMeditation, iGunpowder, iAlphabet, iMathematics, iCalendar, iConstruction, iCurrency, iHunting, iArchery, 
		 iAnimalHusbandry, iHorsebackRiding, iAesthetics, iPaper, iDrama, iMusic],
iCivIran :	[iMysticism, iMeditation, iPolytheism, iPriesthood, iMonotheism, iMonarchy, iLiterature, iCodeOfLaws, iFeudalism, iTheology, 
		 iMusic, iCivilService, iGuilds, iDivineRight, iFishing, iTheWheel, iAgriculture, iPottery, iAesthetics, iSailing,
		 iWriting, iMathematics, iAlphabet, iCalendar, iCurrency, iPhilosophy, iPaper, iHunting, iMining, iArchery,
		 iMasonry, iAnimalHusbandry, iBronzeWorking, iHorsebackRiding, iIronWorking, iMetalCasting, iCompass, iConstruction, iMachinery, iEngineering, 
		 iGunpowder],
iCivNetherlands:[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iTheology, iMonarchy, iDivineRight, iFishing, iSailing, iTheWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, 
		 iFeudalism, iGuilds, iAlphabet, iMathematics, iConstruction, iEngineering, iCurrency, iHunting, iArchery, iAnimalHusbandry,
		 iHorsebackRiding, iMeditation, iCalendar, iBanking, iOptics, iCivilService, iCompass, iGunpowder, iPhilosophy, iEducation,
		 iPaper, iAstronomy, iAesthetics, iLiterature, iDrama, iMusic, iPatronage],
iCivGermany : 	[iMysticism, iMeditation, iPolytheism, iPriesthood, iMonotheism, iMonarchy, iLiterature, iCodeOfLaws, iDrama, iFeudalism, 
		 iTheology, iMusic, iCivilService, iGuilds, iDivineRight, iMilitaryTradition, iConstitution, iLiberalism, iFishing, iTheWheel, 
		 iAgriculture, iPottery, iPrintingPress, iEconomics, iAstronomy, iAesthetics, iSailing, iWriting, iMathematics, iAlphabet, 
		 iCalendar, iCurrency, iPhilosophy, iPaper, iBanking, iEducation, iHunting, iMining, iArchery, iMasonry, 
		 iAnimalHusbandry, iBronzeWorking, iHorsebackRiding, iIronWorking, iMetalCasting, iCompass, iConstruction, iMachinery, iEngineering, 
		 iOptics, iGunpowder, iReplaceableParts, iMilitaryScience, iRifling, iPatronage],
iCivAmerica : 	[iMysticism, iMeditation, iPolytheism, iPriesthood, iMonotheism, iMonarchy, iLiterature, iCodeOfLaws, iDrama, iFeudalism,
		 iTheology, iMusic, iCivilService, iGuilds, iDivineRight, iPatronage, iNationalism, iMilitaryTradition, iConstitution, iLiberalism,
		 iFishing, iTheWheel, iAgriculture, iPottery, iAesthetics, iSailing, iWriting, iMathematics, iAlphabet, iCalendar, 
		 iCurrency, iPhilosophy, iPaper, iBanking, iEducation, iPrintingPress, iEconomics, iAstronomy, iChemistry, iHunting, 
		 iMining, iArchery, iMasonry, iAnimalHusbandry, iBronzeWorking, iHorsebackRiding, iIronWorking, iMetalCasting, iCompass, iConstruction, 
		 iMachinery, iEngineering, iOptics, iGunpowder, iReplaceableParts, iMilitaryScience, iRifling, iSteamPower, iScientificMethod],
iCivArgentina :	[iMysticism, iMeditation, iPolytheism, iPriesthood, iMonotheism, iMonarchy, iLiterature, iCodeOfLaws, iDrama, iFeudalism,
		 iTheology, iMusic, iCivilService, iGuilds, iDivineRight, iMilitaryTradition, iConstitution, iLiberalism, iFishing, iTheWheel, 
		 iAgriculture, iPottery, iPrintingPress, iEconomics, iAstronomy, iScientificMethod, iChemistry, iAesthetics, iSailing, iWriting, 
		 iMathematics, iAlphabet, iCalendar, iCurrency, iPhilosophy, iPaper, iBanking, iEducation, iHunting, iMining, 
		 iArchery, iMasonry, iAnimalHusbandry, iBronzeWorking, iHorsebackRiding, iIronWorking, iMetalCasting, iCompass, iConstruction, iMachinery, 
		 iEngineering, iOptics, iGunpowder, iReplaceableParts, iMilitaryScience, iRifling, iPatronage, iNationalism, iDemocracy, iSteamPower],
iCivMexico : 	[iMysticism, iMeditation, iPolytheism, iPriesthood, iMonotheism, iMonarchy, iLiterature, iCodeOfLaws, iDrama, iFeudalism, 
		 iTheology, iMusic, iCivilService, iGuilds, iDivineRight, iMilitaryTradition, iConstitution, iLiberalism, iFishing, iTheWheel, 
		 iAgriculture, iPottery, iPrintingPress, iEconomics, iAstronomy, iScientificMethod, iChemistry, iAesthetics, iSailing, iWriting, 
		 iMathematics, iAlphabet, iCalendar, iCurrency, iPhilosophy, iPaper, iBanking, iEducation, iHunting, iMining, 
		 iArchery, iMasonry, iAnimalHusbandry, iBronzeWorking, iHorsebackRiding, iIronWorking, iMetalCasting, iCompass, iConstruction, iMachinery, 
		 iEngineering, iOptics, iGunpowder, iReplaceableParts, iMilitaryScience, iRifling, iPatronage],
iCivColombia : 	[iMysticism, iMeditation, iPolytheism, iPriesthood, iMonotheism, iMonarchy, iLiterature, iCodeOfLaws, iDrama, iFeudalism,
		 iTheology, iMusic, iCivilService, iGuilds, iDivineRight, iMilitaryTradition, iConstitution, iLiberalism, iFishing, iTheWheel, 
		 iAgriculture, iPottery, iPrintingPress, iEconomics, iAstronomy, iScientificMethod, iChemistry, iAesthetics, iSailing, iWriting, 
		 iMathematics, iAlphabet, iCalendar, iCurrency, iPhilosophy, iPaper, iBanking, iEducation, iHunting, iMining, 
		 iArchery, iMasonry, iAnimalHusbandry, iBronzeWorking, iHorsebackRiding, iIronWorking, iMetalCasting, iCompass, iConstruction, iMachinery, 
		 iEngineering, iOptics, iGunpowder, iReplaceableParts, iMilitaryScience, iRifling, iPatronage, iNationalism, iSteamPower, iDemocracy],
iCivCanada : 	[iMysticism, iMeditation, iPolytheism, iPriesthood, iMonotheism, iMonarchy, iLiterature, iCodeOfLaws, iDrama, iFeudalism, 
		 iTheology, iMusic, iCivilService, iGuilds, iDivineRight, iMilitaryTradition, iConstitution, iLiberalism, iFishing, iTheWheel, 
		 iAgriculture, iPottery, iPrintingPress, iEconomics, iAstronomy, iScientificMethod, iChemistry, iAesthetics, iSailing, iWriting, 
		 iMathematics, iAlphabet, iCalendar, iCurrency, iPhilosophy, iPaper, iBanking, iEducation, iHunting, iMining, 
		 iArchery, iMasonry, iAnimalHusbandry, iBronzeWorking, iHorsebackRiding, iIronWorking, iMetalCasting, iCompass, iConstruction, iMachinery, 
		 iEngineering, iOptics, iGunpowder, iReplaceableParts, iMilitaryScience, iRifling, iPatronage, iNationalism, iDemocracy, iSteamPower, 
		 iSteel, iRailroad],
iCivBrazil : 	[iMysticism, iMeditation, iPolytheism, iPriesthood, iMonotheism, iMonarchy, iLiterature, iCodeOfLaws, iDrama, iFeudalism,
		 iTheology, iMusic, iCivilService, iGuilds, iDivineRight, iMilitaryTradition, iConstitution, iLiberalism, iFishing, iTheWheel, 
		 iAgriculture, iPottery, iPrintingPress, iEconomics, iAstronomy, iScientificMethod, iChemistry, iAesthetics, iSailing, iWriting, 
		 iMathematics, iAlphabet, iCalendar, iCurrency, iPhilosophy, iPaper, iBanking, iEducation, iHunting, iMining, 
		 iArchery, iMasonry, iAnimalHusbandry, iBronzeWorking, iHorsebackRiding, iIronWorking, iMetalCasting, iCompass, iConstruction, iMachinery, 
		 iEngineering, iOptics, iGunpowder, iReplaceableParts, iMilitaryScience, iRifling, iPatronage, iNationalism, iDemocracy, iSteamPower],
},
{
iCivIndependent:[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMysticism, iPolytheism, iMeditation, iMasonry, iPriesthood, iMonarchy, 
		 iFishing, iSailing, iTheWheel, iPottery, iAgriculture, iWriting, iPottery, iAgriculture, iWriting, iAlphabet, 
		 iMathematics, iCurrency, iHunting, iArchery, iAnimalHusbandry],
iCivIndependent2:[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMysticism, iPolytheism, iMeditation, iMasonry, iPriesthood, iMonarchy, 
		 iFishing, iSailing, iTheWheel, iPottery, iAgriculture, iWriting, iPottery, iAgriculture, iWriting, iAlphabet, 
		 iMathematics, iCurrency, iHunting, iArchery, iAnimalHusbandry],
iCivChina : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMeditation, iPriesthood, iMasonry, 
		 iMonarchy, iFishing, iSailing, iTheWheel, iPottery, iAgriculture, iWriting, iMathematics, iCalendar, iConstruction,
		 iCurrency, iCodeOfLaws, iCivilService, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iAesthetics, iDrama, iMusic],
iCivKorea : 	[iMining, iBronzeWorking, iIronWorking, iMysticism, iPolytheism, iMeditation, iPriesthood, iMasonry, iMonarchy, iFishing, 
		 iSailing, iTheWheel, iPottery, iAgriculture, iWriting, iMathematics, iCalendar, iConstruction, iCurrency, iCodeOfLaws, 
		 iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iAesthetics, iMetalCasting, iMachinery, iDrama, iMonotheism],
iCivByzantium :	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iTheology, iMonarchy, iFishing, iSailing, iTheWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, iAlphabet, 
		 iMathematics, iConstruction, iCurrency, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iLiterature, iDrama, iAesthetics,
		 iCalendar, iMeditation],
iCivJapan :	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMeditation, iPriesthood, iMasonry, 
		 iMonarchy, iFishing, iSailing, iTheWheel, iPottery, iAgriculture, iWriting, iMathematics, iConstruction, iCurrency, 
		 iCodeOfLaws, iCivilService, iHunting, iArchery, iAnimalHusbandry, iCalendar, iAesthetics],
iCivVikings : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonarchy, 
		 iFishing, iSailing, iTheWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, iFeudalism, iAlphabet, iMathematics, 
		 iConstruction, iCurrency, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding],
},
{
iCivIndependent : techs(lMedievalTechs),
iCivIndependent2: techs(lMedievalTechs),
iCivChina :	techs(lMedievalTechs, [iPrintingPress, iAstronomy]),
iCivIndia : 	techs(lMedievalTechs, [iPrintingPress, iAstronomy, iLiberalism, iMilitaryScience, iMilitaryTradition, iReplaceableParts]),
iCivTamils : 	techs(lMedievalTechs, [iPrintingPress, iAstronomy, iMilitaryScience, iMilitaryTradition, iReplaceableParts]),
iCivIran : 	techs(lMedievalTechs, [iMilitaryTradition, iPrintingPress, iAstronomy, iLiberalism]),
iCivKorea : 	techs(lMedievalTechs, [iPrintingPress]),
iCivJapan : 	techs(lMedievalTechs, [iMilitaryTradition, iPrintingPress]),
iCivVikings : 	techs(lMedievalTechs, [iPrintingPress, iMilitaryTradition, iMilitaryScience, iReplaceableParts, iLiberalism, iAstronomy]),
iCivSpain : 	techs(lMedievalTechs, [iPrintingPress, iMilitaryTradition, iMilitaryScience, iReplaceableParts, iLiberalism, iAstronomy]),
iCivFrance : 	techs(lMedievalTechs, [iPrintingPress, iMilitaryTradition, iMilitaryScience, iReplaceableParts, iRifling, iLiberalism, iAstronomy, iConstitution]),
iCivEngland :	techs(lMedievalTechs, [iPrintingPress, iMilitaryScience, iReplaceableParts, iRifling, iLiberalism, iConstitution, iAstronomy]),
iCivHolyRome : 	techs(lMedievalTechs, [iPrintingPress, iMilitaryTradition, iMilitaryScience, iReplaceableParts, iRifling, iAstronomy]),
iCivRussia :	techs(lMedievalTechs, [iPrintingPress, iMilitaryTradition, iMilitaryScience, iReplaceableParts]),
iCivPoland : 	techs(lMedievalTechs, [iPrintingPress, iMilitaryTradition, iReplaceableParts, iAstronomy, iLiberalism, iConstitution]),
iCivPortugal : 	techs(lMedievalTechs, [iPrintingPress, iMilitaryScience, iReplaceableParts, iAstronomy, iLiberalism]),
iCivMughals :	techs(lMedievalTechs, [iPrintingPress, iAstronomy, iLiberalism, iConstitution]),
iCivTurkey : 	techs(lMedievalTechs, [iPrintingPress, iMilitaryScience, iReplaceableParts, iMilitaryTradition]),
iCivThailand :	techs(lMedievalTechs, [iPrintingPress]),
iCivCongo :	[iTech for iTech in lMedievalTechs if iTech not in [iBanking, iEducation, iGunpowder, iDivineRight, iOptics]],
iCivNetherlands:techs(lMedievalTechs, [iPrintingPress, iMilitaryScience, iReplaceableParts, iRifling, iLiberalism, iConstitution, iAstronomy]),
iCivGermany : 	techs(lMedievalTechs, [iPrintingPress, iMilitaryTradition, iMilitaryScience, iReplaceableParts, iRifling, iLiberalism, iConstitution, iAstronomy, iEconomics]),
}]

### Religion spread factors ###

dSpreadFactors  = {
#		   PRO  CAT  ORT  ISL  HIN  BUD  CON  TAO  ZOR
iCivEgypt :	(  100, 200, 300, 350,  20,  20,  20,  20,  20 ),
iCivChina :	(   60,  80,  20,  20,  20, 200, 300, 200,  20 ),
iCivBabylonia :	(  100, 200, 200, 350,  20,  20,  20,  20, 300 ),
iCivHarappa :	(   90,  90,  90,  90, 200, 200,  20,  60,  20 ), 
iCivGreece :	(  100, 300, 500,  30,  20,  40,  20,  20,  30 ),
iCivIndia : 	(   90,  90,  90, 180, 300, 500,  20,  60,  20 ),
iCivCarthage :	(  200, 200, 250, 400,  20,  20,  20,  20, 100 ),
iCivPolynesia :	(  100, 100, 100,  20,  20,  20,  20,  20,  20 ),
iCivPersia :	(   20,  20,  90, 300,  40,  40,  20,  20, 300 ),
iCivRome :	(  100, 500,  40,  40,  20,  40,  20,  20,  70 ),
iCivTamils :	(   60,  60,  60, 180, 500, 250,  40,  40,  40 ),
iCivEthiopia :	(  300, 120, 400, 300,  20,  20,  20,  20,  20 ),
iCivKorea :     (   60,  80,  20,  20,  20, 300, 200, 100,  20 ),
iCivMaya : 	(  200, 300,  80,  80,  80,  80,  80,  80,  80 ),
iCivByzantium : (  200, 120, 500,  60,  20,  40,  20,  20,  70 ),
iCivJapan :	(   40,  40,  20,  20,  20, 300, 120, 100,  20 ),
iCivVikings :	(  500, 400,  40,  40,  20,  30,  30,  20,  20 ),
iCivArabia :	(   30,  30,  80, 500,  20,  20,  20,  20,  20 ),
iCivTibet : 	(   20,  20,  20,  20,  20, 500,  20,  20,  20 ),
iCivKhmer :	(   40,  40,  20,  20, 500, 400,  80, 100,  20 ),
iCivIndonesia :	(   40,  40,  40, 500, 300, 400,  40,  40,  20 ),
iCivMoors : 	(   90, 200,  90, 500,  40,  40,  40,  40,  20 ),
iCivSpain :	(  200, 500,  40,  80,  20,  30,  20,  20,  20 ),
iCivFrance :	(  400, 500,  40,  60,  20,  30,  20,  20,  20 ),
iCivEngland : 	(  500, 400,  40,  40,  20,  30,  20,  20,  20 ),
iCivHolyRome :	(  500, 400,  40,  40,  20,  30,  20,  20,  20 ),
iCivRussia : 	(  300,  40, 400,  20,  20,  30,  20,  20,  20 ),
iCivMali : 	(   90,  90,  40, 400,  20,  20,  20,  20,  20 ),
iCivPoland : 	(  400, 500, 500,  20,  20,  20,  20,  20,  20 ),
iCivPortugal :	(  200, 500,  40,  70,  20,  30,  20,  20,  20 ),
iCivInca : 	(  200, 300,  80,  80,  80,  80,  80,  80,  80 ),
iCivItaly : 	(  200, 500,  40,  40,  20,  20,  20,  20,  20 ),
iCivMongols :	(   80,  80,  80,  80,  20, 300, 100,  80,  20 ),
iCivAztecs :	(  200, 400,  90,  90,  90,  90,  90,  90,  90 ),
iCivMughals :	(  100, 100,  80, 400,  90,  90,  90,  90,  90 ),
iCivTurkey :	(   60,  60, 120, 400,  20,  20,  20,  20,  20 ),
iCivThailand : 	(   20,  20,  20,  20,  80, 400,  20,  20,  20 ),
iCivCongo :	(  100, 400,  20, 100,  20,  20,  20,  20,  20 ),
iCivIran :	(   30,  30,  30, 500,  20,  20,  20,  20,  70 ),
iCivNetherlands:(  500, 400,  40,  20,  20,  20,  20,  20,  20 ),
iCivGermany : 	(  500, 400,  40,  40,  20,  30,  20,  20,  20 ),
iCivAmerica :	(  500, 400,  80,  20,  20,  20,  20,  20,  20 ),
iCivArgentina :	(  100, 500,  40,  20,  20,  20,  20,  20,  20 ),
iCivMexico :	(  100, 500,  40,  20,  20,  20,  20,  20,  20 ),
iCivColombia :	(  100, 500,  40,  20,  20,  20,  20,  20,  20 ),
iCivBrazil :	(  100, 500,  40,  20,  20,  20,  20,  20,  20 ),
iCivCanada :	(  300, 300, 100,  75,  50, 100,  20,  20,  20 ),
iCivIndependent:(  250, 250, 250, 250,  50, 100,  50,  40,  20 ),
iCivIndependent2:( 250, 200, 200, 200,  80, 150,  80,  80,  20 ),
iCivNative : 	(  200, 200, 200, 200,  80,  80,  80,  80,  20 ),
iCivCeltia : 	(  300, 300, 300,  80,  20,  40,  20,  20,  20 ),
iCivSeljuks :	(   80,  80,  80, 400,  20,  20,  20,  20,  20 ),
iCivBarbarian :	(  100, 100, 100, 100, 100, 100, 100, 100,  20 ),
}