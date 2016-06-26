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

# lMedievalTechs = [iFishing, iTheWheel, iAgriculture, iHunting, iMysticism, iMining, iSailing, iPottery, iAnimalHusbandry, iArchery, 
		  # iMeditation, iPolytheism, iMasonry, iHorsebackRiding, iPriesthood, iMonotheism, iBronzeWorking, iWriting, iMetalCasting, iIronWorking,
		  # iAesthetics, iMathematics, iAlphabet, iMonarchy, iCompass, iLiterature, iCalendar, iConstruction, iCurrency, iMachinery,
		  # iDrama, iEngineering, iCodeOfLaws, iFeudalism, iMusic, iPhilosophy, iCivilService, iTheology, iOptics, iPatronage, 
		  # iDivineRight, iPaper, iGuilds, iEducation, iBanking, iGunpowder]

lStartingTechs = [
{
iCivNative : 	[iTanning],
iCivGreece :	[iTanning, iMining, iPottery, iWorship, iSailing,
				iSmelting, iLeverage, iDivination, iSeafaring,
				iAlloys],
iCivIndia :		[iTanning, iMining, iPottery, iPastoralism, iAgriculture, iWorship, iSailing, 
				iSmelting, iLeverage, iCeremony, iDivination, iSeafaring],
iCivCarthage :	[iTanning, iMining, iPottery, iPastoralism, iAgriculture, iWorship, iSailing, 
				iSmelting, iMasonry, iLeverage, iProperty, iCeremony, iDivination, iSeafaring,
				iTradition],
iCivPolynesia : [iTanning, iPottery, iPastoralism, iWorship, iSailing, iSeafaring],
iCivPersia : 	[iTanning, iMining, iPottery, iPastoralism, iWorship, iSailing, 
				iSmelting, iMasonry, iLeverage, iProperty, iCeremony, iDivination, iSeafaring,
				iAlloys, iConstruction, iRiding, iTradition,
				iWriting, iPriesthood],
iCivRome :		[iTanning, iMining, iPottery, iPastoralism, iWorship, iSailing, 
				iSmelting, iMasonry, iLeverage, iProperty, iCeremony, iDivination, iSeafaring,
				iAlloys, iConstruction, iArithmetics, iTradition, iCalendar, iShipbuilding,
				iBloomery, iMetalCasting, iGeometry, iWriting, iPriesthood],
iCivTamils : 	[iTanning, iMining, iPottery, iPastoralism, iAgriculture, iWorship, iSailing, 
				iSmelting, iMasonry, iLeverage, iProperty, iCeremony, iDivination, iSeafaring,
				iAlloys, iConstruction, iRiding, iTradition, iShipbuilding,
				iBloomery, iContract, iWriting, iPriesthood],
iCivEthiopia :	[iTanning, iMining, iPottery, iPastoralism, iWorship, iSailing, 
				iSmelting, iMasonry, iLeverage, iProperty, iCeremony, iDivination, iSeafaring,
				iAlloys, iConstruction, iRiding, iTradition,
				iBloomery, iWriting, iPriesthood],
iCivKorea : 	techs(lAncientTechs, [iBloomery, iMetalCasting, iGeometry, iContract, iWriting, iPriesthood, iAstrolabe,
				iGeneralship, iAesthetics, iCurrency, iLaw, iPhilosophy]),
iCivMaya : 		[iTanning, iMining, iPottery, iAgriculture, iWorship, iSailing,
				iMasonry, iLeverage, iProperty, iCeremony, iDivination,
				iConstruction],
iCivByzantium :	techs(lAncientTechs, [iBloomery, iMetalCasting, iGeometry, iContract, iWriting, iPriesthood, iAstrolabe,
				iGeneralship, iEngineering, iAesthetics, iCurrency, iLaw, iPhilosophy, iSanitation,
				iSteel, iArchitecture, iPolitics,
				iMachinery, iTheology]),
iCivJapan : 	techs(lAncientTechs, [iBloomery, iMetalCasting, iGeometry, iContract, iWriting, iPriesthood, iAstrolabe,
				iGeneralship, iEngineering, iCurrency, iLaw, iPhilosophy,
				iSteel, iArchitecture, iArtisanry, iPolitics, iEthics,
				iMachinery, iCivilService]),
iCivVikings : 	techs(lAncientTechs, [iBloomery, iMetalCasting, iGeometry, iContract, iWriting, iPriesthood, iAstrolabe,
				iGeneralship, iEngineering, iCurrency, iLaw,
				iSteel, iArtisanry, iPolitics,
				iFeudalism, iMachinery]),
iCivArabia : 	techs(lAncientTechs, [iBloomery, iMetalCasting, iGeometry, iContract, iWriting, iPriesthood, iAstrolabe,
				iGeneralship, iEngineering, iCurrency, iLaw, 
				iSteel, iNobility, iArtisanry, iPolitics, iEthics,
				iMachinery, iAlchemy, iTheology, iClergy]),
iCivTibet :		techs(lAncientTechs, [iBloomery, iMetalCasting, iGeometry, iContract, iWriting, iPriesthood, iAstrolabe,
				iGeneralship, iEngineering, iCurrency, iLaw, iPhilosophy,
				iSteel, iNobility, iArchitecture, iScholarship, iEthics,
				iMachinery, iTheology]),
iCivKhmer : 	techs([iTech for iTech in lAncientTechs if iTech != iShipbuilding],
				[iBloomery, iMetalCasting, iGeometry, iContract, iWriting, iPriesthood, iAstrolabe,
				iGeneralship, iEngineering, iCurrency, iLaw, iSanitation,
				iSteel, iNobility, iArchitecture, iPolitics, iEthics,
				iMachinery, iTheology]),
iCivIndonesia :	techs(lAncientTechs, [iBloomery, iMetalCasting, iGeometry, iContract, iWriting, iPriesthood, iAstrolabe,
				iGeneralship, iEngineering, iCurrency, iLaw, iSanitation,
				iSteel, iNobility, iArchitecture, iArtisanry, iEthics,
				iMachinery, iJudiciary]),
iCivMoors : 	techs(lAncientTechs, [iBloomery, iMetalCasting, iGeometry, iContract, iWriting, iPriesthood, iAstrolabe,
				iGeneralship, iEngineering, iAesthetics, iCurrency, iLaw, iPhilosophy, iSanitation,
				iSteel, iArchitecture, iArtisanry, iEthics,
				iMachinery, iAlchemy, iTheology,
				iClergy]),
iCivSpain : 	techs(lAncientTechs, [iBloomery, iMetalCasting, iGeometry, iContract, iWriting, iPriesthood, iAstrolabe,
				iGeneralship, iEngineering, iCurrency, iLaw, iPhilosophy,
				iSteel, iNobility, iArchitecture, iArtisanry, iPolitics, iEthics,
				iWarriorCode, iFeudalism, iMachinery, iTheology,
				iClergy]),
iCivFrance : 	techs(lAncientTechs, [iBloomery, iMetalCasting, iGeometry, iContract, iWriting, iPriesthood, iAstrolabe,
				iGeneralship, iEngineering, iCurrency, iLaw, iPhilosophy,
				iSteel, iNobility, iArchitecture, iArtisanry, iPolitics, iEthics,
				iWarriorCode, iFeudalism, iMachinery, iTheology,
				iClergy]),
iCivEngland : 	techs(lAncientTechs, [iBloomery, iMetalCasting, iGeometry, iContract, iWriting, iPriesthood, iAstrolabe,
				iGeneralship, iEngineering, iCurrency, iLaw, iPhilosophy,
				iSteel, iNobility, iArchitecture, iArtisanry, iPolitics, iEthics,
				iWarriorCode, iFeudalism, iMachinery, iTheology,
				iClergy]),
iCivHolyRome : 	techs(lAncientTechs, [iBloomery, iMetalCasting, iGeometry, iContract, iWriting, iPriesthood, iAstrolabe,
				iGeneralship, iEngineering, iCurrency, iLaw, iPhilosophy,
				iSteel, iNobility, iArchitecture, iArtisanry, iPolitics, iEthics,
				iWarriorCode, iFeudalism, iMachinery, iTheology,
				iClergy]),
iCivRussia : 	techs(lAncientTechs, [iBloomery, iMetalCasting, iGeometry, iContract, iWriting, iPriesthood, iAstrolabe,
				iGeneralship, iEngineering, iCurrency, iLaw, iPhilosophy,
				iSteel, iNobility, iArchitecture, iArtisanry, iPolitics, iEthics,
				iWarriorCode, iFeudalism, iMachinery, iTheology,
				iClergy]),
iCivMali :		[iTanning, iMining, iPottery, iPastoralism, iAgriculture, iWorship,
				iSmelting, iMasonry, iLeverage, iProperty, iCeremony, iDivination,
				iAlloys, iConstruction, iRiding, iArithmetics, iTradition,
				iBloomery, iMetalCasting, iGeometry, iContract, iWriting, iPriesthood,
				iGeneralship, iEngineering, iLaw,
				iSteel, iNobility, iArchitecture, iArtisanry, iPolitics,
				iTheology],
iCivPoland : 	techs(lAncientTechs, [iBloomery, iMetalCasting, iGeometry, iContract, iWriting, iPriesthood, iAstrolabe,
				iGeneralship, iEngineering, iAesthetics, iCurrency, iLaw, iPhilosophy, iSanitation,
				iSteel, iNobility, iArchitecture, iArtisanry, iPolitics, iScholarship, iEthics,
				iWarriorCode, iFeudalism, iMachinery, iAlchemy, iCivilService, iTheology,
				iClergy]),
iCivSeljuks :	techs([iTech for iTech in lAncientTechs if iTech != iShipbuilding], 
				[iBloomery, iMetalCasting, iGeometry, iContract, iWriting, iPriesthood, iAstrolabe,
				iGeneralship, iEngineering, iAesthetics, iCurrency, iLaw, iPhilosophy, iSanitation,
				iSteel, iNobility, iArchitecture, iArtisanry, iPolitics, iScholarship, iEthics,
				iWarriorCode, iFeudalism, iMachinery, iAlchemy, iTheology,
				iPaper, iClergy]),
iCivPortugal :	techs([iTech for iTech in lClassicalTechs if iTech != iArchitecture],
				[iWarriorCode, iFeudalism, iMachinery, iAlchemy, iCivilService, iTheology,
				iGuilds, iPaper, iClergy,]),
iCivInca : 		[iTanning, iMining, iPottery, iPastoralism, iAgriculture, iWorship, iSailing,
				iSmelting, iMasonry, iLeverage, iProperty, iCeremony, iDivination,
				iConstruction, iArithmetics, iTradition,
				iGeometry, iContract, iWriting, iPriesthood,
				iEngineering, iCurrency, iLaw],
iCivMongols :	techs([iTech for iTech in lAncientTechs if iTech != iShipbuilding], 
				[iBloomery, iMetalCasting, iGeometry, iContract, iWriting, iPriesthood,
				iGeneralship, iEngineering, iCurrency, iLaw, iPhilosophy, iSanitation,
				iSteel, iNobility, iArtisanry, iPolitics,
				iWarriorCode, iFeudalism, iMachinery, iAlchemy, 
				iSiegecraft, iCropRotation, iGuilds,
				iGunpowder]),
iCivAztecs :	[iTanning, iMining, iPottery, iPastoralism, iAgriculture, iWorship, iSailing,
				iSmelting, iMasonry, iLeverage, iProperty, iCeremony, iDivination,
				iAlloys, iConstruction, iArithmetics, iTradition, iCalendar, 
				iGeometry, iContract, iWriting, iPriesthood,
				iEngineering, iCurrency, iLaw],	
iCivItaly :		techs(lClassicalTechs, [iWarriorCode, iFeudalism, iMachinery, iAlchemy, iCivilService, iJudiciary, iTheology,
				iSiegecraft, iCropRotation, iGuilds, iCompass, iClergy,
				iLiterature]),
iCivMughals : 	techs(lClassicalTechs, [iWarriorCode, iFeudalism, iMachinery, iAlchemy, iCivilService, iJudiciary, iTheology,
				iCropRotation, iGuilds, iPaper, iClergy,
				iGunpowder, iLiterature]),
iCivTurkey : 	techs(lClassicalTechs, [iWarriorCode, iFeudalism, iMachinery, iAlchemy, iCivilService, iJudiciary, iTheology,
				iSiegecraft, iCropRotation, iGuilds, iClergy,
				iGunpowder, iLiterature]),
iCivCongo : 	[iTanning, iMining, iPottery, iPastoralism, iAgriculture, iWorship, iSailing,
				iSmelting, iMasonry, iLeverage, iProperty, iCeremony, iDivination,
				iAlloys, iConstruction, iArithmetics, iTradition,
				iBloomery, iMetalCasting, iGeometry, iContract, iWriting, iPriesthood,
				iGeneralship, iCurrency, iLaw,
				iNobility, iArtisanry,
				iMachinery, iCivilService, iTheology],
iCivThailand : 	techs(lAncientTechs, [iBloomery, iMetalCasting, iGeometry, iContract, iWriting, iPriesthood,
				iGeneralship, iEngineering, iAesthetics, iCurrency, iLaw, iPhilosophy, iSanitation,
				iSteel, iNobility, iArchitecture, iArtisanry, iPolitics, iEthics,
				iWarriorCode, iMachinery, iCivilService, iJudiciary, iTheology,
				iCropRotation, iPaper, iPatronage,
				iLiterature]),
iCivIran : 		techs(lClassicalTechs, [iWarriorCode, iFeudalism, iMachinery, iAlchemy, iCivilService, iJudiciary, iTheology,
				iSiegecraft, iCropRotation, iGuilds, iCompass, iPaper, iPatronage, iClergy,
				iGunpowder, iCartography, iEducation, iLiterature,
				iFirearms, iOptics, iHeritage]),
iCivNetherlands:techs(lMedievalTechs, [iFirearms, iExploration, iOptics, iHumanities, iPatronage,
				iAstronomy, iHorticulture]),
iCivGermany :	techs(lMedievalTechs, [iFirearms, iEconomics, iExploration, iOptics, iHumanities, iStatecraft, iHeritage,
				iLogistics, iAstronomy, iCivilLiberties, iHorticulture,
				iReplaceableParts, iPhysics, iConstitution]),
iCivAmerica : 	[iTech for iTech in lRenaissanceTechs if iTech not in [iHydraulics, iSocialSciences]].append(iNationalism),
iCivArgentina :	techs(lRenaissanceTechs, [iThermodynamics, iChemistry, iRepresentation, iNationalism]),
iCivMexico : 	techs(lRenaissanceTechs, [iThermodynamics, iChemistry, iRepresentation, iNationalism]),
iCivColombia : 	techs(lRenaissanceTechs, [iThermodynamics, iChemistry, iRepresentation, iNationalism]),
iCivBrazil : 	techs(lRenaissanceTechs, [iThermodynamics, iChemistry, iRepresentation, iNationalism]),
iCivCanada : 	techs(lRenaissanceTechs, [iMachineTools, iThermodynamics, iMetallurgy, iChemistry, iBiology, iRepresentation, iNationalism,
				iMedicine, iLaborUnions, iJournalism]),
},
{
iCivIndependent : 	techs(lAncientTechs, [iBloomery, iMetalCasting, iGeometry, iContract, iWriting, iPriesthood, iAstrolabe,
					iGeneralship, iEngineering, iAesthetics, iCurrency, iLaw, iSanitation,
					iSteel, iNobility, iArchitecture, iArtisanry]),
iCivIndependent2 : 	techs(lAncientTechs, [iBloomery, iMetalCasting, iGeometry, iContract, iWriting, iPriesthood, iAstrolabe,
					iGeneralship, iEngineering, iAesthetics, iCurrency, iLaw, iSanitation,
					iSteel, iNobility, iArchitecture, iArtisanry]),
iCivChina : 	techs(lClassicalTechs, [iWarriorCode, iMachinery, iAlchemy, iCivilService]),
iCivKorea :		techs([iTech for iTech in lClassicalTechs if iTech != iScholarship],
				[iWarriorCode, iMachinery, iAlchemy]),
iCivByzantium :	techs(lClassicalTechs, [iWarriorCode, iMachinery, iAlchemy, iJudiciary, iTheology]),
iCivJapan : 	techs(lAncientTechs, [iBloomery, iMetalCasting, iGeometry, iContract, iWriting, iPriesthood, iAstrolabe,
				iGeneralship, iEngineering, iAesthetics, iCurrency, iLaw, iPhilosophy, iSanitation,
				iSteel, iNobility, iArchitecture, iArtisanry, iPolitics, iEthics,
				iWarriorCode, iMachinery, iCivilService]),
iCivVikings :	techs(lAncientTechs, [iBloomery, iMetalCasting, iGeometry, iContract, iWriting, iPriesthood, iAstrolabe,
				iGeneralship, iEngineering, iCurrency, iLaw,
				iSteel, iNobility, iArtisanry, iPolitics, iEthics,
				iWarriorCode, iFeudalism, iMachinery]),
},
{
}]
	
# {
# iCivIndependent : techs(lMedievalTechs),
# iCivIndependent2: techs(lMedievalTechs),
# iCivChina :	techs(lMedievalTechs, [iPrintingPress, iAstronomy]),
# iCivIndia : 	techs(lMedievalTechs, [iPrintingPress, iAstronomy, iLiberalism, iMilitaryScience, iMilitaryTradition, iReplaceableParts]),
# iCivTamils : 	techs(lMedievalTechs, [iPrintingPress, iAstronomy, iMilitaryScience, iMilitaryTradition, iReplaceableParts]),
# iCivIran : 	techs(lMedievalTechs, [iMilitaryTradition, iPrintingPress, iAstronomy, iLiberalism]),
# iCivKorea : 	techs(lMedievalTechs, [iPrintingPress]),
# iCivJapan : 	techs(lMedievalTechs, [iMilitaryTradition, iPrintingPress]),
# iCivVikings : 	techs(lMedievalTechs, [iPrintingPress, iMilitaryTradition, iMilitaryScience, iReplaceableParts, iLiberalism, iAstronomy]),
# iCivSpain : 	techs(lMedievalTechs, [iPrintingPress, iMilitaryTradition, iMilitaryScience, iReplaceableParts, iLiberalism, iAstronomy]),
# iCivFrance : 	techs(lMedievalTechs, [iPrintingPress, iMilitaryTradition, iMilitaryScience, iReplaceableParts, iRifling, iLiberalism, iAstronomy, iConstitution]),
# iCivEngland :	techs(lMedievalTechs, [iPrintingPress, iMilitaryScience, iReplaceableParts, iRifling, iLiberalism, iConstitution, iAstronomy]),
# iCivHolyRome : 	techs(lMedievalTechs, [iPrintingPress, iMilitaryTradition, iMilitaryScience, iReplaceableParts, iRifling, iAstronomy]),
# iCivRussia :	techs(lMedievalTechs, [iPrintingPress]),
# iCivPoland : 	techs(lMedievalTechs, [iPrintingPress, iMilitaryTradition, iAstronomy, iLiberalism, iConstitution]),
# iCivPortugal : 	techs(lMedievalTechs, [iPrintingPress, iMilitaryScience, iReplaceableParts, iAstronomy, iLiberalism]),
# iCivMughals :	techs(lMedievalTechs, [iPrintingPress, iAstronomy, iLiberalism, iConstitution]),
# iCivTurkey : 	techs(lMedievalTechs, [iPrintingPress, iMilitaryScience, iReplaceableParts, iMilitaryTradition]),
# iCivThailand :	techs(lMedievalTechs, [iPrintingPress]),
# iCivCongo :	[iTech for iTech in lMedievalTechs if iTech not in [iBanking, iEducation, iGunpowder, iDivineRight, iOptics]],
# iCivNetherlands:techs(lMedievalTechs, [iPrintingPress, iMilitaryScience, iReplaceableParts, iRifling, iLiberalism, iConstitution, iAstronomy]),
# iCivGermany : 	techs(lMedievalTechs, [iPrintingPress, iMilitaryTradition, iMilitaryScience, iReplaceableParts, iRifling, iLiberalism, iConstitution, iAstronomy, iEconomics]),
# }]