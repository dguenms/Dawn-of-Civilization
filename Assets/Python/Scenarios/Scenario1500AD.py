from Resources import setupScenarioResources

from Scenario import *
from Locations import *
from RFCUtils import *
from Core import *


lCivilizations = [
	Civilization(
		iChina,
		iLeader=iHongwu,
		iStateReligion=iConfucianism,
		iGold=100,
		lCivics=[iMonarchy, iBureaucracy, iManorialism, iRegulatedTrade, iSyncretism, iIsolationism],
		techs=techs.column(9).without(iFinance, iHumanities).including(iFirearms, iLogistics, iStatecraft),
		dAttitudes={iKorea: 2},
	),
	Civilization(
		iDravidia,
		iLeader=iKrishnaDevaRaya,
		iStateReligion=iHinduism,
		iGold=200,
		lCivics=[iMonarchy, iVassalage, iCasteSystem, iMerchantTrade, iMonasticism, iThalassocracy],
		techs=techs.column(8).including(iGunpowder, iCompanies, iCartography),
		dMemories={
			iMughals: {MemoryTypes.MEMORY_DECLARED_WAR: 2},
		},
	),
	Civilization(
		iEthiopia,
		iLeader=iZaraYaqob,
		iStateReligion=iOrthodoxy,
		iGold=40,
		lCivics=[iMonarchy, iVassalage, iManorialism, iRedistribution, iClergy, iKinship],
		techs=techs.column(8).without(iPaper, iCompass).including(iCompanies),
	),
	Civilization(
		iKorea,
		iLeader=iSejong,
		iStateReligion=iConfucianism,
		iGold=100,
		lCivics=[iMonarchy, iBureaucracy, iCasteSystem, iRegulatedTrade, iMonasticism, iThalassocracy],
		techs=techs.column(8).including(iGunpowder, iCompanies, iCartography, iPrinting, iJudiciary).including(iFirearms, iStatecraft),
		dAttitudes={iChina: 2},
	),
	Civilization(
		iMali,
		iLeader=iMansaMusa,
		iStateReligion=iIslam,
		iGold=50,
		lCivics=[iElective, iVassalage, iSlavery, iMerchantTrade, iClergy, iHegemony],
		techs=techs.column(8).without(iCompass, iPatronage),
		dMemories={
			iMoors: {MemoryTypes.MEMORY_DECLARED_WAR: 2},
		},
	),
	Civilization(
		iFrance,
		iLeader=iLouis,
		iStateReligion=iCatholicism,
		iGold=400,
		lCivics=[iMonarchy, iVassalage, iManorialism, iRegulatedTrade, iClergy, iHegemony],
		techs=techs.column(9).including(iFirearms, iLogistics, iExploration),
		dMemories={
			iEngland: {MemoryTypes.MEMORY_DECLARED_WAR: 2},
			iHolyRome: {MemoryTypes.MEMORY_DECLARED_WAR: 3},
		},
	),
	Civilization(
		iMalays,
		iLeader=iTunPerak,
		iStateReligion=iIslam,
		iGold=200,
		lCivics=[iDespotism, iCitizenship, iCasteSystem, iMerchantTrade, iClergy, iThalassocracy],
		techs=techs.column(8).without(iPatronage).including(iGunpowder),
		dAttitudes={iOttomans: 2},
	),
	Civilization(
		iJapan,
		iLeader=iOdaNobunaga,
		iStateReligion=iBuddhism,
		iGold=100,
		lCivics=[iMonarchy, iVassalage, iCasteSystem, iRedistribution, iMonasticism, iThalassocracy],
		techs=techs.column(9).without(iFinance).including(iStatecraft, iHeritage),
	),
	Civilization(
		iNorse,
		iLeader=iChristian,
		iStateReligion=iCatholicism,
		iGold=100,
		lCivics=[iMonarchy, iVassalage, iManorialism, iMerchantTrade, iClergy, iThalassocracy],
		techs=techs.column(9).without(iCompanies, iFinance, iHumanities),
		dAttitudes={iHolyRome: 2},
		dMemories={
			iSweden: {MemoryTypes.MEMORY_REJECTED_DEMAND: 2},
		},
	),
	Civilization(
		iTurks,
		iLeader=iTamerlane,
		iStateReligion=iIslam,
		lCivics=[iDespotism, iVassalage, iSlavery, iMerchantTrade, iClergy, iHegemony],
		techs=techs.column(8).without(iCropRotation).including(iGunpowder),
		dMemories={
			iIran: {MemoryTypes.MEMORY_DECLARED_WAR: 2},
		},
	),
	Civilization(
		iMoors,
		iLeader=iYaqub,
		iStateReligion=iIslam,
		iGold=100,
		lCivics=[iMonarchy, iTheocracy, iSlavery, iMerchantTrade, iClergy, iHegemony],
		techs=techs.column(8).including(iGunpowder, iFinance, iCartography),
		dMemories={
			iSpain: {MemoryTypes.MEMORY_DECLARED_WAR: 4},
		},
	),
	Civilization(
		iJava,
		iLeader=iHayamWuruk,
		iStateReligion=iIslam,
		iGold=100,
		lCivics=[iMonarchy, iVassalage, iCasteSystem, iMerchantTrade, iClergy, iThalassocracy],
		techs=techs.column(8).without(iEducation, iPatronage).including(iGunpowder, iCompanies),
	),
	Civilization(
		iSpain,
		iLeader=iPhilip,
		iStateReligion=iCatholicism,
		iGold=300,
		lCivics=[iMonarchy, iVassalage, iManorialism, iRegulatedTrade, iClergy, iColonialism],
		techs=techs.column(9).without(iHumanities, iJudiciary).including(iFirearms, iExploration),
		dAttitudes={iPortugal: 2},
		dMemories={
			iMoors: {MemoryTypes.MEMORY_DENIED_RELIGION: 4},
		},
	),
	Civilization(
		iEngland,
		iLeader=iElizabeth,
		iStateReligion=iCatholicism,
		iGold=400,
		lCivics=[iMonarchy, iVassalage, iManorialism, iRegulatedTrade, iClergy, iColonialism],
		techs=techs.column(9).including(iFirearms, iExploration),
		dMemories={
			iFrance: {MemoryTypes.MEMORY_DECLARED_WAR: 3},
		},
	),
	Civilization(
		iHolyRome,
		iLeader=iCharles,
		iStateReligion=iCatholicism,
		iGold=250,
		lCivics=[iElective, iVassalage, iManorialism, iRegulatedTrade, iClergy, iHegemony],
		techs=techs.column(9).including(iFirearms, iStatecraft),
		dAttitudes={iNorse: 2},
		dMemories={
			iFrance: {MemoryTypes.MEMORY_DECLARED_WAR: 4},
			iOttomans: {MemoryTypes.MEMORY_DECLARED_WAR: 4, MemoryTypes.MEMORY_DENIED_RELIGION: 4},
		},
	),
	Civilization(
		iBurma,
		iLeader=iBayinnaung,
		iStateReligion=iBuddhism,
		iGold=150,
		lCivics=[iDespotism, iVassalage, iCasteSystem, iMerchantTrade, iMonasticism, iHegemony],
		techs=techs.column(8).without(iCompass, iPatronage).including(iGunpowder),
		dMemories={
			iThailand: {MemoryTypes.MEMORY_REJECTED_DEMAND: 2},
		},
	),
	Civilization(
		iVietnam,
		iLeader=iLeLoi,
		iStateReligion=iConfucianism,
		iGold=100,
		lCivics=[iMonarchy, iVassalage, iCasteSystem, iRedistribution, iMonasticism, iThalassocracy],
		techs=techs.column(8).including(iGunpowder, iPrinting, iJudiciary),
		dAttitudes={iChina: 2},
	),
	Civilization(
		iMisr,
		iLeader=iBaibars,
		iStateReligion=iIslam,
		lCivics=[iDespotism, iVassalage, iSlavery, iMerchantTrade, iClergy, iHegemony],
		techs=techs.column(8).including(iGunpowder, iJudiciary),
		dMemories={
			iOttomans: {MemoryTypes.MEMORY_REJECTED_DEMAND: 4},
		},
	),
	Civilization(
		iPoland,
		iLeader=iSobieski,
		iStateReligion=iCatholicism,
		iGold=200,
		lCivics=[iElective, iVassalage, iManorialism, iMerchantTrade, iClergy, iHegemony],
		techs=techs.column(9).without(iFinance, iCartography),
		dMemories={
			iRussia: {MemoryTypes.MEMORY_DENIED_RELIGION: 2},
			iHolyRome: {MemoryTypes.MEMORY_DECLARED_WAR: 2},
			iOttomans: {MemoryTypes.MEMORY_DENIED_RELIGION: 4},
		},
	),
	Civilization(
		iPortugal,
		iLeader=iJoao,
		iStateReligion=iCatholicism,
		iGold=200,
		lCivics=[iMonarchy, iVassalage, iManorialism, iRegulatedTrade, iClergy, iColonialism],
		techs=techs.column(9).without(iHumanities, iJudiciary).including(iFirearms, iExploration, iOptics),
		dAttitudes={iSpain: 2},
		dMemories={
			iMoors: {MemoryTypes.MEMORY_DENIED_RELIGION: 2},
		},
	),
	Civilization(
		iInca,
		iLeader=iHuaynaCapac,
		iGold=100,
		lCivics=[iMonarchy, iCitizenship, iCasteSystem, iRedistribution, iDeification, iHegemony],
		techs=techs.column(5).including(iArchitecture, iArtisanry, iPolitics),
	),
	Civilization(
		iItaly,
		iLeader=iLorenzo,
		iStateReligion=iCatholicism,
		iGold=200,
		lCivics=[iRepublic, iCitizenship, iManorialism, iMerchantTrade, iClergy, iThalassocracy],
		techs=techs.column(9).including(iOptics, iHeritage),
		dMemories={
			iHolyRome: {MemoryTypes.MEMORY_DECLARED_WAR: 4},
			iFrance: {MemoryTypes.MEMORY_DECLARED_WAR: 4},
		},
	),
	Civilization(
		iAztecs,
		iLeader=iMontezuma,
		iGold=100,
		lCivics=[iDespotism, iCitizenship, iSlavery, iRedistribution, iDeification, iHegemony],
		techs=techs.column(6).without(iNobility, iSteel).including(iCivilService),
	),
	Civilization(
		iMughals,
		iLeader=iTughluq,
		iStateReligion=iIslam,
		iGold=200,
		lCivics=[iDespotism, iVassalage, iSlavery, iRegulatedTrade, iClergy, iHegemony],
		techs=techs.column(8).including(iGunpowder, iCompanies, iHumanities, iJudiciary),
		dMemories={
			iDravidia: {MemoryTypes.MEMORY_DENIED_RELIGION: 2},
		},
	),
	Civilization(
		iThailand,
		iLeader=iNaresuan,
		iStateReligion=iBuddhism,
		iGold=150,
		lCivics=[iMonarchy, iVassalage, iCasteSystem, iRedistribution, iMonasticism, iHegemony],
		techs=techs.column(8).without(iCompass, iDoctrine).including(iCompanies, iHumanities),
		dAttitudes={iBurma: -2},
	),
	Civilization(
		iSweden,
		iLeader=iGustav,
		iStateReligion=iCatholicism,
		iGold=100,
		lCivics=[iMonarchy, iVassalage, iManorialism, iRegulatedTrade, iClergy, iHegemony],
		techs=techs.column(9).without(iCartography, iCartography).including(iFirearms, iLogistics),
		dAttitudes={iRussia: -2},
		dMemories={
			iNorse: {MemoryTypes.MEMORY_DECLARED_WAR: 2},
		},
	),
	Civilization(
		iRussia,
		iLeader=iIvan,
		iStateReligion=iOrthodoxy,
		iGold=200,
		lCivics=[iDespotism, iVassalage, iManorialism, iRegulatedTrade, iClergy, iHegemony],
		techs=techs.column(8).including(iGunpowder, iCompanies, iJudiciary, iPrinting, iFirearms),
		dAttitudes={iSweden: -2},
		dMemories={
			iPoland: {MemoryTypes.MEMORY_DECLARED_WAR: 4},
			iOttomans: {MemoryTypes.MEMORY_DENIED_RELIGION: 2},
		},
	),
	Civilization(
		iOttomans,
		iLeader=iSuleiman,
		iStateReligion=iIslam,
		iGold=500,
		lCivics=[iMonarchy, iVassalage, iSlavery, iRegulatedTrade, iClergy, iHegemony],
		techs=techs.column(8).including(iGunpowder, iCompanies, iJudiciary, iFirearms, iLogistics),
		dAttitudes={iRussia: -2},
		dMemories={
			iHolyRome: {MemoryTypes.MEMORY_DECLARED_WAR: 4},
			iPoland: {MemoryTypes.MEMORY_DECLARED_WAR: 4},
			iMisr: {MemoryTypes.MEMORY_REJECTED_DEMAND: 4},
			iIran: {MemoryTypes.MEMORY_DENIED_RELIGION: 2},
		},
	),
	Civilization(
		iCongo,
		iLeader=iMbemba,
		iStateReligion=iCatholicism,
		iGold=50,
		lCivics=[iElective, iVassalage, iSlavery, iMerchantTrade, iClergy, iKinship],
		techs=techs.column(7).without(iFortification, iMachinery, iAlchemy),
	),
	Civilization(
		iIran,
		iLeader=iAbbas,
		iStateReligion=iIslam,
		iGold=250,
		lCivics=[iMonarchy, iTheocracy, iSlavery, iMerchantTrade, iFanaticism, iHegemony],
		techs=techs.column(9).without(iFinance, iCartography, iPrinting).including(iFirearms),
		dMemories={
			iOttomans: {MemoryTypes.MEMORY_DENIED_RELIGION: 2},
		},
	),
	Civilization(
		iNative,
		techs=techs.column(5),
	),
	Civilization(
		iIndependent2,
		techs=techs.column(7),
	),
	Civilization(
		iIndependent,
		techs=techs.column(7),
	),
]

lTribalVillages = [
	((137, 59), (140, 62)), # Hokkaido
	((99, 65), (119, 72)), # Siberia
	((75, 11), (81, 18)), # South Africa
	((21, 57), (30, 62)), # Great Lakes
	((15, 51), (21, 64)), # Great Plains
	((36, 29), (44, 33)), # Amazon
	((37, 11), (41, 20)), # Parana
	((25, 42), (33, 46)), # Caribbean
]


def updateData():
	data.civs[iTurks].iResurrections = 1
	
	team(iHolyRome).changeResearchProgress(iAcademia, scale(600), slot(iHolyRome))
	if not player(iHolyRome).isHuman():
		player(iHolyRome).pushResearch(iAcademia, True)
	
	for worker in units.owner(iRussia).type(iWorker):
		worker.setMoves(0)


def setupGoals(iCiv, goals):
	if iCiv == iHolyRome:
		goals[0].requirements[0].succeed()
		goals[0].requirements[1].succeed()
	elif iCiv == iBurma:
		goals[1].requirements[0].accumulate(1)


scenario1500AD = Scenario(
	iStartYear = 1500,
	fileName = "RFC_1500AD",
	
	lCivilizations = lCivilizations,
	lTribalVillages = lTribalVillages,
	
	dCivilizationDescriptions = {
		iTurks: "TXT_KEY_CIV_UZBEKS_DESC",
		iNorse: "TXT_KEY_CIV_DENMARK_DESC",
		iMisr: "TXT_KEY_CIV_EGYPT_DESC",
	},
	
	dRevealed = {
		iCivGroupEurope: Revealed(
			lLandRegions=lEurope + lNorthAfrica + [rAnatolia, rMesopotamia, rArabia, rPersia], 
			lCoastRegions=lSubSaharanAfrica,
			lSeaAreas=[((36, 29),	(53, 52))],
		),
		iCivGroupEastAsia: Revealed(
			lLandRegions=lEastAsia + [rTransoxiana],
			lCoastRegions=[rIndochina, rIndonesia, rPhilippines],
		),
		iCivGroupSouthAsia: Revealed(
			lLandRegions=lIndia + [rIndochina, rIndonesia, rPersia, rKhorasan, rTransoxiana, rTibet, rArabia, rMesopotamia],
			lCoastRegions=[rEthiopia, rSouthChina],
			lSeaAreas=[((79, 23), (97, 32))],
		),
		iCivGroupMiddleEast: Revealed(
			lLandRegions=lMiddleEast + lIndia + lNorthAfrica + [rSahel, rSahara, rEthiopia, rHornOfAfrica, rSwahiliCoast, rIberia, rItaly, rBalkans],
			lCoastRegions=[rBritain, rIreland, rFrance, rLowerGermany, rScandinavia, rPonticSteppe],
			lSeaAreas=[((79, 23), (97, 32))],
		),
		iCivGroupAfrica: Revealed(
			lLandRegions=lSubSaharanAfrica,
			lCoastRegions=lSubSaharanAfrica,
		),
	},
	
	dGreatPeopleCreated = {
		iChina: 10,
		iIndia: 8,
		iPersia: 4,
		iDravidia: 4,
		iKorea: 4,
		iJapan: 4,
		iNorse: 6,
		iTurks: 4,
		iSpain: 6,
		iFrance: 5,
		iEngland: 5,
		iHolyRome: 5,
		iPoland: 5,
		iPortugal: 5,
		iMughals: 5,
		iOttomans: 5,
		iThailand: 5,
		iCongo: 2,
	},
	dGreatGeneralsCreated = {
		iChina: 4,
		iIndia: 3,
		iPersia: 2,
		iDravidia: 2,
		iKorea: 3,
		iJapan: 3,
		iNorse: 3,
		iTurks: 3,
		iSpain: 4,
		iFrance: 3,
		iEngland: 3,
		iHolyRome: 4,
		iPoland: 3,
		iPortugal: 3,
		iMughals: 4,
		iOttomans: 5,
		iThailand: 3,
		iCongo: 2,
		iNetherlands: 3,
	},
	
	dColonistsAlreadyGiven = {
		iSpain : 1,
		iPortugal : 3,
	},
	
	lInitialWars = [
		(iOttomans, iMisr, WarPlanTypes.WARPLAN_TOTAL),
	],
	
	lWorkingCities = [
		(tBeijing, [(125, 54)]),
		(tChangan, [(119, 52)]),
		(tKunming, [(119, 46)]),
		(tCairo, [(78, 41)]),
		(tMilan, [(68, 57)]),
		(tDelhi, [(107, 45)]),
		(tConstantinople, [(80, 53)]),
		(tPersepolis, [(93, 47)]),
		(tPataliputra, [(111, 44)]),
	],
	
	lAllGoalsFailed = [iChina, iDravidia, iEthiopia, iKorea, iKhmer, iMali, iMalays, iJapan, iNorse, iTurks, iTibet, iMoors, iJava, iSwahili, iMisr, iItaly, iAztecs],
	lGoalsSucceeded = [(iSpain, 0), (iBurma, 0), (iVietnam, 0), (iPoland, 0), (iMughals, 0), (iRussia, 0)],
	setupGoals = setupGoals,
	
	updateData = updateData,
	
	greatWall = GreatWall(
		tGraphicsTL = (118, 54),
		tGraphicsBR = (128, 58),
		lClearCulture = [(122, 57), (124, 59), (125, 59), (126, 59), (127, 59), (128, 59), (129, 57), (129, 58), (129, 59)],
		lGraphicsExceptions = [(118, 55), (118, 56), (118, 57), (118, 58), (119, 55), (119, 56), (119, 57), (119, 58), (120, 56), (120, 57), (120, 58), (121, 56), (121, 57), (121, 58), (122, 56), (122, 57), (122, 58), (123, 58)],
		
		lEffectAreas = [((118, 44), (129, 53)), ((117, 47), (117, 50)), ((123, 43), (125, 43)), ((119, 54), (128, 54)), ((120, 55), (125, 55)), ((123, 56), (128, 57)), ((124, 58), (128, 58))],
	),
)
