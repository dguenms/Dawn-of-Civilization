from Consts import *
from RFCUtils import utils

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
	
def techs(lEraTechs, lExtraTechs=[]):
	lTechs = list(lEraTechs)
	lTechs.extend(lExtraTechs)
	return lTechs

### General functions ###
		
def initBirthYear(iPlayer):
	gc.getPlayer(iPlayer).setBirthYear(tBirth[iPlayer])

def init():
	for iPlayer in range(iNumPlayers):
		initBirthYear(iPlayer)

### Starting technologies ###

lMedievalTechs = [iFishing, iWheel, iAgriculture, iHunting, iMysticism, iMining, iSailing, iPottery, iAnimalHusbandry, iArchery, 
		  iMeditation, iPolytheism, iMasonry, iHorsebackRiding, iPriesthood, iMonotheism, iBronzeWorking, iWriting, iMetalCasting, iIronWorking,
		  iAesthetics, iMathematics, iAlphabet, iMonarchy, iCompass, iLiterature, iCalendar, iConstruction, iCurrency, iMachinery,
		  iDrama, iEngineering, iCodeOfLaws, iFeudalism, iMusic, iPhilosophy, iCivilService, iTheology, iOptics, iPatronage, 
		  iDivineRight, iPaper, iGuilds, iEducation, iBanking, iGunpowder]

lStartingTechs = [
{
iCivNative : 	[iHunting, iArchery],
iCivIndia : 	[iMysticism, iFishing, iWheel, iAgriculture, iPottery, iHunting, iMining, iWriting, iMeditation, iAnimalHusbandry,
		 iBronzeWorking, iArchery, iSailing],
iCivGreece :	[iMining, iBronzeWorking, iMysticism, iPolytheism, iFishing, iSailing, iWheel, iPottery, iWriting, iHunting],
iCivPersia : 	[iMining, iBronzeWorking, iMysticism, iPolytheism, iPriesthood, iMasonry, iFishing, iSailing, iMonotheism, iMonarchy,
		 iWheel, iPottery, iWriting, iHunting, iArchery, iHorsebackRiding],
iCivPhoenicia : 	[iMining, iBronzeWorking, iMysticism, iPolytheism, iPriesthood, iMasonry, iFishing, iSailing, iWheel, iPottery, 
		 iWriting, iHunting, iArchery, iAnimalHusbandry, iAlphabet],
iCivPolynesia :	[iMysticism, iFishing, iPottery, iHunting, iSailing],
iCivRome : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMysticism, iPolytheism, iPriesthood, iMasonry, iFishing, iSailing, 
		 iWheel, iPottery, iWriting, iAlphabet, iHunting, iAnimalHusbandry, iMathematics],
iCivTamils : 	[iMining, iBronzeWorking, iMysticism, iPolytheism, iMeditation, iPriesthood, iMasonry, iFishing, iSailing, iMonarchy, 
		 iWheel, iPottery, iWriting, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iAgriculture, iAesthetics, iIronWorking],
iCivEthiopia : 	[iMining, iBronzeWorking, iMysticism, iPolytheism, iMeditation, iPriesthood, iMonotheism, iMasonry, iFishing, iSailing, 
		 iMonarchy, iWheel, iPottery, iWriting, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding],
iCivKorea : 	[iMining, iBronzeWorking, iIronWorking, iMysticism, iPolytheism, iMeditation, iPriesthood, iMasonry, iMonarchy, iFishing, 
		 iSailing, iWheel, iPottery, iAgriculture, iWriting, iMathematics, iCalendar, iConstruction, iCurrency, iCodeOfLaws, 
		 iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iAesthetics],	 
iCivMaya : 	[iMining, iMysticism, iPolytheism, iMeditation, iPriesthood, iMasonry, iFishing, iWheel, iPottery, iAgriculture, iWriting, 
		 iHunting],
iCivByzantium :	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iTheology, iMonarchy, iFishing, iSailing, iWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, iAlphabet, 
		 iMathematics, iConstruction, iCurrency, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iLiterature, iDrama, iAesthetics,
		 iCalendar, iMeditation],
iCivJapan :	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMeditation, iPriesthood, iMasonry, 
		 iMonarchy, iFishing, iSailing, iWheel, iPottery, iAgriculture, iWriting, iMathematics, iConstruction, iCurrency, 
		 iCodeOfLaws, iCivilService, iHunting, iArchery, iAnimalHusbandry, iCalendar],
iCivVikings :	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonarchy, 
		 iFishing, iSailing, iWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, iFeudalism, iAlphabet, iMathematics, 
		 iConstruction, iCurrency, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding],
iCivArabia : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iTheology, iMonarchy, iDivineRight, iFishing, iWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, iFeudalism, 
		 iAlphabet, iMathematics, iConstruction, iCurrency, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iMeditation],
iCivTibet : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iMonarchy, iFishing, iWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, iMathematics, iConstruction, iCurrency, 
		 iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iCalendar, iMeditation, iSailing, iTheology],
iCivKhmer : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iMeditation, iPriesthood, 
		 iMonotheism, iMonarchy, iFishing, iWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, iMathematics, iConstruction,
		 iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding],
iCivIndonesia :	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iMeditation, iPriesthood, 
		 iMonotheism, iMonarchy, iFishing, iWheel, iPottery, iAgriculture, iWriting, iSailing, iCodeOfLaws, iMathematics, 
		 iConstruction, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding],
iCivMoors : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iTheology, iMonarchy, iFishing, iWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, iAlphabet, iMathematics, 
		 iConstruction, iCurrency, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iLiterature, iAesthetics, iCalendar, iMeditation, 
		 iSailing, iPhilosophy],
iCivSpain : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iTheology, iMonarchy, iFishing, iSailing, iWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, iFeudalism, 
		 iAlphabet, iMathematics, iConstruction, iCurrency, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iCalendar, iMeditation],
iCivFrance : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iTheology, iMonarchy, iFishing, iSailing, iWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, iFeudalism, 
		 iAlphabet, iMathematics, iConstruction, iCurrency, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iCalendar, iMeditation],
iCivEngland : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iTheology, iMonarchy, iFishing, iSailing, iWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, iFeudalism, 
		 iAlphabet, iMathematics, iConstruction, iCurrency, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iCalendar, iMeditation],
iCivHolyRome :	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iTheology, iMonarchy, iFishing, iWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, iFeudalism, iAlphabet, 
		 iMathematics, iConstruction, iCurrency, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iFeudalism, iCalendar, iMeditation, 
		 iSailing],
iCivRussia : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iTheology, iMonarchy, iWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, iFeudalism, iAlphabet, iMathematics, 
		 iConstruction, iCurrency, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iCalendar, iMeditation, iFishing, iSailing],
iCivMali : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, iTheology, 
		 iMonarchy, iDivineRight, iWheel, iPottery, iAgriculture, iWriting, iAlphabet, iMathematics, iConstruction, iCurrency,
		 iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding],
iCivPoland : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iTheology, iMonarchy, iFishing, iSailing, iWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, iFeudalism,
		 iAlphabet, iMathematics, iConstruction, iCurrency, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iMeditation, iAesthetics, 
		 iLiterature, iCalendar, iCivilService],
iCivSeljuks : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iTheology, iMonarchy, iDivineRight, iFishing, iWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, iFeudalism, 
		 iAlphabet, iMathematics, iConstruction, iCurrency, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iLiterature, iDrama, 
		 iAesthetics, iMusic, iCalendar],
iCivPortugal : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iTheology, iMonarchy, iDivineRight, iFishing, iSailing, iWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, 
		 iFeudalism, iGuilds, iAlphabet, iMathematics, iConstruction, iEngineering, iCurrency, iHunting, iArchery, iAnimalHusbandry,
		 iHorsebackRiding, iCalendar, iMeditation],
iCivInca : 	[iMining, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonarchy, iFishing, iWheel, iPottery, iAgriculture, 
		 iWriting, iCodeOfLaws, iMathematics, iCurrency, iHunting, iArchery, iAnimalHusbandry],
iCivMongolia : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMeditation, iPriesthood, iMasonry, 
		 iMonarchy, iFishing, iWheel, iPottery, iAgriculture, iWriting, iMathematics, iCodeOfLaws, iFeudalism, iMathematics, 
		 iConstruction, iEngineering, iGuilds, iCurrency, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iGunpowder],
iCivAztecs : 	[iMining, iBronzeWorking, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonarchy, iFishing, iWheel, iPottery, 
		 iAgriculture, iWriting, iCodeOfLaws, iMathematics, iCalendar, iCurrency, iHunting, iArchery],
iCivItaly : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iTheology, iMonarchy, iFishing, iSailing, iWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, iFeudalism, 
		 iGuilds, iAlphabet, iMathematics, iCalendar, iConstruction, iEngineering, iCurrency, iHunting, iArchery, iAnimalHusbandry,
		 iHorsebackRiding, iAesthetics, iLiterature, iCompass, iCivilService, iMeditation],
iCivMughals : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iTheology, iMonarchy, iDivineRight, iFishing, iSailing, iWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, 
		 iCivilService, iGunpowder, iAlphabet, iMathematics, iCalendar, iConstruction, iCurrency, iHunting, iArchery, iAnimalHusbandry, 
		 iHorsebackRiding, iGuilds, iAesthetics, iLiterature],
iCivTurkey : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iTheology, iMonarchy, iDivineRight, iFishing, iSailing, iWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, 
		 iFeudalism, iCivilService, iGuilds, iGunpowder, iAlphabet, iMathematics, iCalendar, iConstruction, iEngineering, iCurrency, 
		 iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iMeditation],
iCivCongo : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, iTheology, 
		 iMonarchy, iWheel, iPottery, iAgriculture, iWriting, iAlphabet, iMathematics, iConstruction, iCurrency, iHunting,
		 iArchery, iAnimalHusbandry, iMachinery, iCivilService, iFishing, iCodeOfLaws],
iCivThailand :	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iTheology, iMonarchy, iDivineRight, iFishing, iSailing, iWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, 
		 iCivilService, iMeditation, iGunpowder, iAlphabet, iMathematics, iCalendar, iConstruction, iCurrency, iHunting, iArchery, 
		 iAnimalHusbandry, iHorsebackRiding, iAesthetics, iPaper, iDrama, iMusic],
iCivIran :	[iMysticism, iMeditation, iPolytheism, iPriesthood, iMonotheism, iMonarchy, iLiterature, iCodeOfLaws, iFeudalism, iTheology, 
		 iMusic, iCivilService, iGuilds, iDivineRight, iFishing, iWheel, iAgriculture, iPottery, iAesthetics, iSailing,
		 iWriting, iMathematics, iAlphabet, iCalendar, iCurrency, iPhilosophy, iPaper, iHunting, iMining, iArchery,
		 iMasonry, iAnimalHusbandry, iBronzeWorking, iHorsebackRiding, iIronWorking, iMetalCasting, iCompass, iConstruction, iMachinery, iEngineering, 
		 iGunpowder, iOptics, iDrama, iPatronage],
iCivNetherlands:[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iTheology, iMonarchy, iDivineRight, iFishing, iSailing, iWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, 
		 iFeudalism, iGuilds, iAlphabet, iMathematics, iConstruction, iEngineering, iCurrency, iHunting, iArchery, iAnimalHusbandry,
		 iHorsebackRiding, iMeditation, iCalendar, iBanking, iOptics, iCivilService, iCompass, iGunpowder, iPhilosophy, iEducation,
		 iPaper, iAstronomy, iAesthetics, iLiterature, iDrama, iMusic, iPatronage],
iCivGermany : 	[iMysticism, iMeditation, iPolytheism, iPriesthood, iMonotheism, iMonarchy, iLiterature, iCodeOfLaws, iDrama, iFeudalism, 
		 iTheology, iMusic, iCivilService, iGuilds, iDivineRight, iMilitaryTradition, iConstitution, iLiberalism, iFishing, iWheel, 
		 iAgriculture, iPottery, iPrintingPress, iEconomics, iAstronomy, iAesthetics, iSailing, iWriting, iMathematics, iAlphabet, 
		 iCalendar, iCurrency, iPhilosophy, iPaper, iBanking, iEducation, iHunting, iMining, iArchery, iMasonry, 
		 iAnimalHusbandry, iBronzeWorking, iHorsebackRiding, iIronWorking, iMetalCasting, iCompass, iConstruction, iMachinery, iEngineering, 
		 iOptics, iGunpowder, iReplaceableParts, iMilitaryScience, iRifling, iPatronage],
iCivAmerica : 	[iMysticism, iMeditation, iPolytheism, iPriesthood, iMonotheism, iMonarchy, iLiterature, iCodeOfLaws, iDrama, iFeudalism,
		 iTheology, iMusic, iCivilService, iGuilds, iDivineRight, iPatronage, iNationalism, iMilitaryTradition, iConstitution, iLiberalism,
		 iFishing, iWheel, iAgriculture, iPottery, iAesthetics, iSailing, iWriting, iMathematics, iAlphabet, iCalendar, 
		 iCurrency, iPhilosophy, iPaper, iBanking, iEducation, iPrintingPress, iEconomics, iAstronomy, iChemistry, iHunting, 
		 iMining, iArchery, iMasonry, iAnimalHusbandry, iBronzeWorking, iHorsebackRiding, iIronWorking, iMetalCasting, iCompass, iConstruction, 
		 iMachinery, iEngineering, iOptics, iGunpowder, iReplaceableParts, iMilitaryScience, iRifling, iSteamPower, iScientificMethod],
iCivArgentina :	[iMysticism, iMeditation, iPolytheism, iPriesthood, iMonotheism, iMonarchy, iLiterature, iCodeOfLaws, iDrama, iFeudalism,
		 iTheology, iMusic, iCivilService, iGuilds, iDivineRight, iMilitaryTradition, iConstitution, iLiberalism, iFishing, iWheel, 
		 iAgriculture, iPottery, iPrintingPress, iEconomics, iAstronomy, iScientificMethod, iChemistry, iAesthetics, iSailing, iWriting, 
		 iMathematics, iAlphabet, iCalendar, iCurrency, iPhilosophy, iPaper, iBanking, iEducation, iHunting, iMining, 
		 iArchery, iMasonry, iAnimalHusbandry, iBronzeWorking, iHorsebackRiding, iIronWorking, iMetalCasting, iCompass, iConstruction, iMachinery, 
		 iEngineering, iOptics, iGunpowder, iReplaceableParts, iMilitaryScience, iRifling, iPatronage, iNationalism, iDemocracy, iSteamPower],
iCivMexico : 	[iMysticism, iMeditation, iPolytheism, iPriesthood, iMonotheism, iMonarchy, iLiterature, iCodeOfLaws, iDrama, iFeudalism, 
		 iTheology, iMusic, iCivilService, iGuilds, iDivineRight, iMilitaryTradition, iConstitution, iLiberalism, iFishing, iWheel, 
		 iAgriculture, iPottery, iPrintingPress, iEconomics, iAstronomy, iScientificMethod, iChemistry, iAesthetics, iSailing, iWriting, 
		 iMathematics, iAlphabet, iCalendar, iCurrency, iPhilosophy, iPaper, iBanking, iEducation, iHunting, iMining, 
		 iArchery, iMasonry, iAnimalHusbandry, iBronzeWorking, iHorsebackRiding, iIronWorking, iMetalCasting, iCompass, iConstruction, iMachinery, 
		 iEngineering, iOptics, iGunpowder, iReplaceableParts, iMilitaryScience, iRifling, iPatronage],
iCivColombia : 	[iMysticism, iMeditation, iPolytheism, iPriesthood, iMonotheism, iMonarchy, iLiterature, iCodeOfLaws, iDrama, iFeudalism,
		 iTheology, iMusic, iCivilService, iGuilds, iDivineRight, iMilitaryTradition, iConstitution, iLiberalism, iFishing, iWheel, 
		 iAgriculture, iPottery, iPrintingPress, iEconomics, iAstronomy, iScientificMethod, iChemistry, iAesthetics, iSailing, iWriting, 
		 iMathematics, iAlphabet, iCalendar, iCurrency, iPhilosophy, iPaper, iBanking, iEducation, iHunting, iMining, 
		 iArchery, iMasonry, iAnimalHusbandry, iBronzeWorking, iHorsebackRiding, iIronWorking, iMetalCasting, iCompass, iConstruction, iMachinery, 
		 iEngineering, iOptics, iGunpowder, iReplaceableParts, iMilitaryScience, iRifling, iPatronage, iNationalism, iSteamPower, iDemocracy],
iCivCanada : 	[iMysticism, iMeditation, iPolytheism, iPriesthood, iMonotheism, iMonarchy, iLiterature, iCodeOfLaws, iDrama, iFeudalism, 
		 iTheology, iMusic, iCivilService, iGuilds, iDivineRight, iMilitaryTradition, iConstitution, iLiberalism, iFishing, iWheel, 
		 iAgriculture, iPottery, iPrintingPress, iEconomics, iAstronomy, iScientificMethod, iChemistry, iAesthetics, iSailing, iWriting, 
		 iMathematics, iAlphabet, iCalendar, iCurrency, iPhilosophy, iPaper, iBanking, iEducation, iHunting, iMining, 
		 iArchery, iMasonry, iAnimalHusbandry, iBronzeWorking, iHorsebackRiding, iIronWorking, iMetalCasting, iCompass, iConstruction, iMachinery, 
		 iEngineering, iOptics, iGunpowder, iReplaceableParts, iMilitaryScience, iRifling, iPatronage, iNationalism, iDemocracy, iSteamPower, 
		 iSteel, iRailroad],
iCivBrazil : 	[iMysticism, iMeditation, iPolytheism, iPriesthood, iMonotheism, iMonarchy, iLiterature, iCodeOfLaws, iDrama, iFeudalism,
		 iTheology, iMusic, iCivilService, iGuilds, iDivineRight, iMilitaryTradition, iConstitution, iLiberalism, iFishing, iWheel, 
		 iAgriculture, iPottery, iPrintingPress, iEconomics, iAstronomy, iScientificMethod, iChemistry, iAesthetics, iSailing, iWriting, 
		 iMathematics, iAlphabet, iCalendar, iCurrency, iPhilosophy, iPaper, iBanking, iEducation, iHunting, iMining, 
		 iArchery, iMasonry, iAnimalHusbandry, iBronzeWorking, iHorsebackRiding, iIronWorking, iMetalCasting, iCompass, iConstruction, iMachinery, 
		 iEngineering, iOptics, iGunpowder, iReplaceableParts, iMilitaryScience, iRifling, iPatronage, iNationalism, iDemocracy, iSteamPower],
},
{
iCivIndependent:[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMysticism, iPolytheism, iMeditation, iMasonry, iPriesthood, iMonarchy, 
		 iFishing, iSailing, iWheel, iPottery, iAgriculture, iWriting, iPottery, iAgriculture, iWriting, iAlphabet, 
		 iMathematics, iCurrency, iHunting, iArchery, iAnimalHusbandry],
iCivIndependent2:[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMysticism, iPolytheism, iMeditation, iMasonry, iPriesthood, iMonarchy, 
		 iFishing, iSailing, iWheel, iPottery, iAgriculture, iWriting, iPottery, iAgriculture, iWriting, iAlphabet, 
		 iMathematics, iCurrency, iHunting, iArchery, iAnimalHusbandry],
iCivChina : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMeditation, iPriesthood, iMasonry, 
		 iMonarchy, iFishing, iSailing, iWheel, iPottery, iAgriculture, iWriting, iMathematics, iCalendar, iConstruction,
		 iCurrency, iCodeOfLaws, iCivilService, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iAesthetics, iDrama, iMusic],
iCivKorea : 	[iMining, iBronzeWorking, iIronWorking, iMysticism, iPolytheism, iMeditation, iPriesthood, iMasonry, iMonarchy, iFishing, 
		 iSailing, iWheel, iPottery, iAgriculture, iWriting, iMathematics, iCalendar, iConstruction, iCurrency, iCodeOfLaws, 
		 iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iAesthetics, iMetalCasting, iMachinery, iDrama, iMonotheism],
iCivByzantium :	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonotheism, 
		 iTheology, iMonarchy, iFishing, iSailing, iWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, iAlphabet, 
		 iMathematics, iConstruction, iCurrency, iHunting, iArchery, iAnimalHusbandry, iHorsebackRiding, iLiterature, iDrama, iAesthetics,
		 iCalendar, iMeditation],
iCivJapan :	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMeditation, iPriesthood, iMasonry, 
		 iMonarchy, iFishing, iSailing, iWheel, iPottery, iAgriculture, iWriting, iMathematics, iConstruction, iCurrency, 
		 iCodeOfLaws, iCivilService, iHunting, iArchery, iAnimalHusbandry, iCalendar, iAesthetics],
iCivVikings : 	[iMining, iBronzeWorking, iIronWorking, iMetalCasting, iMachinery, iMysticism, iPolytheism, iMasonry, iPriesthood, iMonarchy, 
		 iFishing, iSailing, iWheel, iPottery, iAgriculture, iWriting, iCodeOfLaws, iFeudalism, iAlphabet, iMathematics, 
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
iCivRussia :	techs(lMedievalTechs, [iPrintingPress]),
iCivPoland : 	techs(lMedievalTechs, [iPrintingPress, iMilitaryTradition, iAstronomy, iLiberalism, iConstitution]),
iCivPortugal : 	techs(lMedievalTechs, [iPrintingPress, iMilitaryScience, iReplaceableParts, iAstronomy, iLiberalism]),
iCivMughals :	techs(lMedievalTechs, [iPrintingPress, iAstronomy, iLiberalism, iConstitution]),
iCivTurkey : 	techs(lMedievalTechs, [iPrintingPress, iMilitaryScience, iReplaceableParts, iMilitaryTradition]),
iCivThailand :	techs(lMedievalTechs, [iPrintingPress]),
iCivCongo :	[iTech for iTech in lMedievalTechs if iTech not in [iBanking, iEducation, iGunpowder, iDivineRight, iOptics]],
iCivNetherlands:techs(lMedievalTechs, [iPrintingPress, iMilitaryScience, iReplaceableParts, iRifling, iLiberalism, iConstitution, iAstronomy]),
iCivGermany : 	techs(lMedievalTechs, [iPrintingPress, iMilitaryTradition, iMilitaryScience, iReplaceableParts, iRifling, iLiberalism, iConstitution, iAstronomy, iEconomics]),
}]