from Resources import setupScenarioResources

from Scenario import *
from Locations import *
from RFCUtils import *
from Core import *

	
lCivilizations = [
	Civilization(
		iIndia,
		iLeader=iShivaji,
		iGold=200,
		iStateReligion=iHinduism,
		lCivics=[iMonarchy, iTheocracy, iCasteSystem, iRegulatedTrade, iMonasticism, iHegemony],
		techs=techs.column(10).including(iCombinedArms, iUrbanPlanning, iHorticulture).without(iExploration),
		dMemories={
			iEngland: {MemoryTypes.MEMORY_DECLARED_WAR: 3},
		},
	),
	Civilization(
		iKorea,
		iLeader=iSejong,
		iGold=200,
		iStateReligion=iConfucianism,
		lCivics=[iDespotism, iBureaucracy, iCasteSystem, iIsolationism, iSyncretism, iIsolationism],
		techs=techs.column(10).including(iCombinedArms, iUrbanPlanning, iHorticulture),
		dAttitudes={iManchuria: 2}
	),
	Civilization(
		iJapan,
		iLeader=iOdaNobunaga,
		iGold=800,
		iStateReligion=iBuddhism,
		lCivics=[iMonarchy, iVassalage, iManorialism, iIsolationism, iMonasticism, iIsolationism],
		techs=techs.column(11).without(iScientificMethod, iCivilLiberties),
		dAttitudes={iKorea: -2},
	),
	Civilization(
		iNorse, # Denmark
		iLeader=iChristian,
		iGold=150,
		iStateReligion=iProtestantism,
		lCivics=[iMonarchy, iBureaucracy, iManorialism, iRegulatedTrade, iClergy, iThalassocracy],
		techs=techs.column(12).including(iChemistry, iBiology),
		dAttitudes={iSweden: -2},
	),
	Civilization(
		iTurks, # Uzbeks
		iLeader=iTamerlane,
		iGold=50,
		iStateReligion=iIslam,
		lCivics=[iDespotism, iVassalage, iSlavery, iMerchantTrade, iClergy, iHegemony],
		techs=techs.column(10).without(iExploration).including(iCombinedArms, iHorticulture),
	),
	Civilization(
		iSpain,
		iLeader=iPhilip,
		iGold=200,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iBureaucracy, iManorialism, iRegulatedTrade, iClergy, iColonialism],
		techs=techs.column(12).without(iHydraulics, iGeology).including(iNationalism),
		dMemories={
			iFrance: {MemoryTypes.MEMORY_DECLARED_WAR: 1},
		},
	),
	Civilization(
		iFrance,
		iLeader=iNapoleon,
		iGold=800,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iBureaucracy, iIndividualism, iFreeEnterprise, iClergy, iNationhood],
		techs=techs.column(13).without(iThermodynamics, iMetallurgy),
		dMemories={
			iEngland: {MemoryTypes.MEMORY_DECLARED_WAR: 2},
			iHolyRome: {MemoryTypes.MEMORY_DECLARED_WAR: 1},
			iRussia: {MemoryTypes.MEMORY_DECLARED_WAR: 2},
			iGermany: {MemoryTypes.MEMORY_DECLARED_WAR: 2},
		},
	),
	Civilization(
		iEngland,
		iLeader=iVictoria,
		iGold=300,
		iStateReligion=iProtestantism,
		lCivics=[iMonarchy, iConstitution, iIndividualism, iFreeEnterprise, iClergy, iColonialism],
		techs=techs.column(13).without(iBiology, iNationalism),
		dAttitudes={iPortugal: 2, iBurma: -2, iIndia: -3},
		dMemories={
			iFrance: {MemoryTypes.MEMORY_DECLARED_WAR: 2},
			iRussia: {MemoryTypes.MEMORY_DENIED_RELIGION: 1},
		},
	),
	Civilization(
		iHolyRome, # Austria
		iLeader=iFrancis,
		iGold=150,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iBureaucracy, iManorialism, iRegulatedTrade, iClergy, iHegemony],
		techs=techs.column(12).including(iThermodynamics, iBiology),
		dAttitudes={iItaly: -2, iGermany: -2},
		dMemories={
			iFrance: {MemoryTypes.MEMORY_DECLARED_WAR: 3},
			iOttomans: {MemoryTypes.MEMORY_DECLARED_WAR: 2},
		},
	),
	Civilization(
		iBurma,
		iLeader=iBayinnaung,
		iGold=100,
		iStateReligion=iBuddhism,
		lCivics=[iDespotism, iVassalage, iCasteSystem, iRegulatedTrade, iMonasticism, iHegemony],
		techs=techs.column(10).without(iExploration, iOptics, iAcademia).including(iCombinedArms, iHorticulture),
		dAttitudes={iThailand: -2},
		dMemories={
			iManchuria: {MemoryTypes.MEMORY_DECLARED_WAR: 2},
		},
	),
	Civilization(
		iVietnam,
		iLeader=iLeLoi,
		iGold=150,
		iStateReligion=iConfucianism,
		lCivics=[iMonarchy, iBureaucracy, iCasteSystem, iRegulatedTrade, iSyncretism, iThalassocracy],
		techs=techs.column(11).without(iEconomics, iScientificMethod, iCivilLiberties),
		dAttitudes={iManchuria: 2},
	),
	Civilization(
		iMisr,
		iLeader=iMuhammadAli,
		iGold=500,
		iStateReligion=iIslam,
		lCivics=[iMonarchy, iBureaucracy, iManorialism, iRegulatedTrade, iClergy, iHegemony],
		techs=techs.column(12).without(iPhysics, iGeology, iSociology),
		dAttitudes={iEngland: 2},
		dMemories={
			iOttomans: {MemoryTypes.MEMORY_DECLARED_WAR: 2},
		},
	),
	Civilization(
		iPortugal,
		iLeader=iJoao,
		iGold=150,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iBureaucracy, iManorialism, iRegulatedTrade, iClergy, iColonialism],
		techs=techs.column(12).without(iGeology, iSociology),
		dAttitudes={iEngland: 2},
		dMemories={
			iFrance: {MemoryTypes.MEMORY_DECLARED_WAR: 2},
			iSpain: {MemoryTypes.MEMORY_DECLARED_WAR: 1},
		},
	),
	Civilization(
		iItaly,
		iLeader=iCavour,
		iGold=200,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iBureaucracy, iManorialism, iRegulatedTrade, iClergy, iThalassocracy],
		techs=techs.column(12).including(iMetallurgy, iChemistry, iNationalism),
		dAttitudes={iHolyRome: -2},
	),
	Civilization(
		iSweden,
		iLeader=iGustav,
		iGold=250,
		iStateReligion=iProtestantism,
		lCivics=[iMonarchy, iConstitution, iManorialism, iRegulatedTrade, iClergy, iHegemony],
		techs=techs.column(12).including(iChemistry, iBiology, iRepresentation),
		dAttitudes={iNorse: -2},
		dMemories={
			iRussia: {MemoryTypes.MEMORY_DECLARED_WAR: 2},
		},
	),
	Civilization(
		iRussia,
		iLeader=iAlexanderI,
		iGold=500,
		iStateReligion=iOrthodoxy,
		lCivics=[iDespotism, iBureaucracy, iManorialism, iRegulatedTrade, iClergy, iHegemony],
		techs=techs.column(12).without(iHydraulics, iSocialContract),
		dAttitudes={iSweden: -1, iOttomans: -2},
		dMemories={
			iFrance: {MemoryTypes.MEMORY_DECLARED_WAR: 2},
			iSweden: {MemoryTypes.MEMORY_DECLARED_WAR: 2},
			iOttomans: {MemoryTypes.MEMORY_DENIED_RELIGION: 2},
			iIran: {MemoryTypes.MEMORY_DENIED_RELIGION: 2},
		},
	),
	Civilization(
		iOttomans,
		iLeader=iSuleiman,
		iGold=100,
		iStateReligion=iIslam,
		lCivics=[iDespotism, iBureaucracy, iSlavery, iRegulatedTrade, iSyncretism, iHegemony],
		techs=techs.column(12).without(iScientificMethod).including(iSocialContract),
		dMemories={
			iIran: {MemoryTypes.MEMORY_DECLARED_WAR: 2},
			iHolyRome: {MemoryTypes.MEMORY_DENIED_RELIGION: 2},
			iRussia: {MemoryTypes.MEMORY_DECLARED_WAR: 3},
			iFrance: {MemoryTypes.MEMORY_DECLARED_WAR: 2},
		},
	),
	Civilization(
		iThailand,
		iLeader=iMongkut,
		iGold=200,
		iStateReligion=iBuddhism,
		lCivics=[iMonarchy, iVassalage, iCasteSystem, iRegulatedTrade, iMonasticism, iThalassocracy],
		techs=techs.column(10).including(iCombinedArms, iEconomics, iUrbanPlanning, iHorticulture),
		dMemories={
			iBurma: {MemoryTypes.MEMORY_DECLARED_WAR: 2},
		},
	),
	Civilization(
		iCongo,
		iLeader=iMbemba,
		iGold=200,
		iStateReligion=iCatholicism,
		lCivics=[iElective, iVassalage, iSlavery, iRedistribution, iClergy],
		techs=techs.column(9).including(iFirearms, iStatecraft),
	),
	Civilization(
		iIran,
		iLeader=iAbbas,
		iGold=300,
		iStateReligion=iIslam,
		lCivics=[iMonarchy, iTheocracy, iSlavery, iRegulatedTrade, iFanaticism, iHegemony],
		techs=techs.column(11).without(iScientificMethod, iCivilLiberties).including(iHydraulics),
		dMemories={
			iOttomans: {MemoryTypes.MEMORY_DECLARED_WAR: 2},
			iRussia: {MemoryTypes.MEMORY_DECLARED_WAR: 2},
		},
	),
	Civilization(
		iManchuria,
		iLeader=iKangxi,
		iGold=250,
		iStateReligion=iConfucianism,
		lCivics=[iDespotism, iBureaucracy, iManorialism, iRegulatedTrade, iSyncretism, iIsolationism],
		techs=techs.column(11).without(iScientificMethod, iCivilLiberties),
		dAttitudes={iKorea: 2, iVietnam: 2, iBurma: -2}
	),
	Civilization(
		iNetherlands,
		iLeader=iWilliam,
		iGold=300,
		iStateReligion=iProtestantism,
		lCivics=[iMonarchy, iBureaucracy, iIndividualism, iFreeEnterprise, iSyncretism, iColonialism],
		techs=techs.column(12).including(iThermodynamics, iChemistry, iBiology),
		dMemories={
			iEngland: {MemoryTypes.MEMORY_DECLARED_WAR: 1},
			iFrance: {MemoryTypes.MEMORY_DECLARED_WAR: 2},
		},
	),
	Civilization(
		iGermany,
		iLeader=iFrederick,
		iGold=600,
		iStateReligion=iProtestantism,
		lCivics=[iMonarchy, iBureaucracy, iManorialism, iRegulatedTrade, iSyncretism, iHegemony],
		techs=techs.column(13).without(iThermodynamics, iBiology, iRepresentation),
		dAttitudes={iHolyRome: -2},
		dMemories={
			iFrance: {MemoryTypes.MEMORY_DECLARED_WAR: 3},
		},
	),
	Civilization(
		iAmerica,
		iGold=1000,
		iLeader=iWashington,
		iStateReligion=iProtestantism,
		lCivics=[iDemocracy, iConstitution, iIndividualism, iFreeEnterprise, iSecularism, iIsolationism],
		techs=techs.column(13).without(iMetallurgy, iBiology, iNationalism),
		dAttitudes={iFrance: 2, iMexico: -2},
		dMemories={
			iEngland: {MemoryTypes.MEMORY_DECLARED_WAR: 2},
		},
	),
	Civilization(
		iArgentina,
		iGold=1200,
		iLeader=iSanMartin,
		iStateReligion=iCatholicism,
		lCivics=[iDemocracy, iConstitution, iIndividualism, iFreeEnterprise, iSecularism, iNationhood],
		techs=techs.column(12).including(iBiology, iRepresentation, iNationalism),
		dMemories={
			iSpain: {MemoryTypes.MEMORY_DECLARED_WAR: 2},
		},
	),
	Civilization(
		iMexico,
		iGold=500,
		iLeader=iSantaAnna,
		iStateReligion=iCatholicism,
		lCivics=[iDespotism, iConstitution, iIndividualism, iRegulatedTrade, iClergy, iNationhood],
		techs=techs.column(12).including(iRepresentation, iNationalism),
		dMemories={
			iSpain: {MemoryTypes.MEMORY_DECLARED_WAR: 2},
		},
	),
	Civilization(
		iColombia,
		iGold=750,
		iLeader=iBolivar,
		iStateReligion=iCatholicism,
		lCivics=[iDespotism, iConstitution, iIndividualism, iRegulatedTrade, iClergy, iNationhood],
		techs=techs.column(12).including(iRepresentation, iNationalism),
		dMemories={
			iSpain: {MemoryTypes.MEMORY_DECLARED_WAR: 2},
		},
	),
	Civilization(
		iNative,
		iGold=400,
		techs=techs.column(9)
	),
	Civilization(
		iIndependent2,
		iGold=800,
		techs=techs.column(11)
	),
	Civilization(
		iIndependent,
		iGold=800,
		techs=techs.column(11)
	),
]

lTribalVillages = [
	((130, 20), (141, 23)), # Northern Australia
	((138, 9), (143, 17)), # Eastern Australia
	((0, 6), (2, 12)), # New Zealand
	((69, 29), (78, 33)), # Central Africa
]
	

def setupGoals(iCiv, goals):
	# English tech goal
	if iCiv == iEngland:
		goals[2].requirements[0].accumulate(8)


def updateData():
	data.dFirstContactConquerors = {iMaya: True, iToltecs: True, iAztecs: True, iInca: True}
	
	for iCiv in lTradingCompanyCivs:
		data.civs[iCiv].bTradingCompanyConquerors = False
	
	data.civs[iChina].iResurrections = 2
	data.civs[iIndia].iResurrections = 1
	data.civs[iDravidia].iResurrections = 1
	data.civs[iMisr].iResurrections = 1
	data.civs[iItaly].iResurrections = 1


scenario1815AD = Scenario(
	iStartYear = 1815,
	fileName = "RFC_1815AD",
	
	lCivilizations = lCivilizations,
	lTribalVillages = lTribalVillages,
	
	dCivilizationDescriptions = {
		iTurks: "TXT_KEY_CIV_UZBEKS_DESC",
		iNorse: "TXT_KEY_CIV_DENMARK_DESC",
		iHolyRome: "TXT_KEY_CIV_AUSTRIA_DESC",
		iEngland: "TXT_KEY_CIV_BRITAIN_DESC",
		iMisr: "TXT_KEY_CIV_EGYPT_DESC",
		iManchuria: "TXT_KEY_CIV_CHINA_DESC",
		iGermany: "TXT_KEY_CIV_HOLY_ROMAN_DESC",
	},
	
	dOwnedTiles = {
		iFrance: [(59, 55)],
		iHolyRome: [(70, 61), (71, 61)],
		iBurma: [(115, 43), (115, 44)],
		iItaly: [(65, 57), (65, 56), (66, 55), (67, 55), (68, 57), (68, 56), (68, 55), (70, 53), (69, 52), (69, 51), (68, 50), (68, 49), (69, 48)],
		iPortugal: [(53, 52), (54, 52), (55, 52), (55, 51), (55, 50), (54, 48), (40, 17), (41, 18)],
		iSweden: [(70, 68)],
		iRussia: [(75, 64)],
		iThailand: [(119, 39)],
		iNetherlands: [(62, 62), (63, 62)],
		iGermany: [(72, 61), (73, 62)],
		iIndependent: [(122, 38)],
		iIndependent2: [(119, 42), (120, 41), (121, 40)],
	},
	iCultureTurns = 150,
	
	dRevealed = {
		iCivGroupEurope: Revealed(
			lLandRegions=lEurope + lNorthAfrica + lAsia + lAmerica, 
			lCoastRegions=lSubSaharanAfrica + lAsia + lAmerica,
			lSeaRegions=[rAtlanticOcean, rPacificOcean, rIndianOcean, rSeaOfJapan, rEastChinaSea, rSouthChinaSea, rAustralasianSea, rBayOfBengal, rPersianGulf, rArabianSea, rNorthSea, rMediterraneanSea, rBlackSea, rCaribbeanSea, rGulfOfMexico],
		),
		iCivGroupEastAsia: Revealed(
			lLandRegions=lAsia,
			lCoastRegions=lEurope + lAfrica + lAmerica,
			lSeaRegions=[rSeaOfJapan, rEastChinaSea, rSouthChinaSea, rAustralasianSea, rBayOfBengal],
		),
		iCivGroupSouthAsia: Revealed(
			lLandRegions=lAsia,
			lCoastRegions=lEurope + lAfrica + lAmerica,
			lSeaRegions=[rSouthChinaSea, rAustralasianSea, rBayOfBengal, rArabianSea, rPersianGulf, rRedSea],
		),
		iCivGroupMiddleEast: Revealed(
			lLandRegions=lEurope + lAsia + lNorthAfrica + [rSahel, rSahara, rEthiopia, rHornOfAfrica, rSwahiliCoast],
			lCoastRegions=lAfrica + lAmerica,
			lSeaRegions=[rIndianOcean, rMediterraneanSea, rRedSea, rArabianSea, rPersianGulf, rBayOfBengal, rAustralasianSea],
		),
		iCivGroupAfrica: Revealed(
			lLandRegions=lAfrica,
			lCoastRegions=lAfrica,
			lSeaRegions=[rMediterraneanSea, rRedSea],
		),
		iCivGroupAmerica: Revealed(
			lLandRegions=lEurope + lNorthAfrica + lAsia + lAmerica, 
			lCoastRegions=lSubSaharanAfrica + lAsia + lAmerica,
			lSeaRegions=[rAtlanticOcean, rPacificOcean, rIndianOcean, rSeaOfJapan, rEastChinaSea, rSouthChinaSea, rAustralasianSea, rBayOfBengal, rPersianGulf, rArabianSea, rNorthSea, rMediterraneanSea, rBlackSea, rCaribbeanSea, rGulfOfMexico],
		),
	},
	
	dGreatPeopleCreated = {
		iChina: 12,
		iIndia: 8,
		iPersia: 4,
		iDravidia: 5,
		iKorea: 8,
		iJapan: 8,
		iNorse: 8,
		iTurks: 4,
		iSpain: 8,
		iFrance: 10,
		iEngland: 12,
		iHolyRome: 10,
		iPoland: 8,
		iPortugal: 10,
		iMughals: 10,
		iOttomans: 12,
		iThailand: 8,
		iCongo: 4,
		iNetherlands: 8,
		iGermany: 2,
		iAmerica: 2,
	},
	dGreatGeneralsCreated = {
		iChina: 4,
		iIndia: 3,
		iPersia: 2,
		iDravidia: 2,
		iKorea: 4,
		iJapan: 4,
		iNorse: 3,
		iTurks: 3,
		iSpain: 5,
		iFrance: 6,
		iEngland: 4,
		iHolyRome: 6,
		iPoland: 3,
		iPortugal: 4,
		iMughals: 4,
		iOttomans: 6,
		iThailand: 4,
		iCongo: 2,
		iNetherlands: 4,
		iGermany: 2,
		iAmerica: 1,
	},
	
	dColonistsAlreadyGiven = {
		iSweden : 1,
		iSpain : 7,
		iFrance : 5,
		iEngland : 6,
		iPortugal : 6,
		iNetherlands : 6,
	},
	
	lWorkingCities = [
		(tTokyo, [(139, 52), (139, 56), (140, 56), (141, 56)]),
		(tMadrid, [(56, 53), (57, 53), (58, 53)]),
		(tCalcutta, [(112, 40), (111, 44), (112, 44), (112, 43), (113, 41)]),
		(tVienna, [(70, 57)]),
		(tCairo, [(78, 45), (78, 44), (77, 43), (77, 42), (78, 41), (79, 41), (80, 42), (81, 42)]),
		(tBeloHorizonte, [(47, 22)]),
		(tConstantinople, [(77, 55), (77, 54), (78, 53), (79, 53), (80, 53), (81, 54), (81, 55), (81, 56)]),
		(tKoenigsberg, [(74, 64)]),
		(tMunich, [(66, 60)]),
		(tNewYork, [(30, 58), (32, 57)]),
		(tAtlanta, [(24, 50)]),
	],
	
	lUnexpiredWonders = [iLasLajasSanctuary],
	
	lAllGoalsFailed = [iIndia, iKorea, iFrance, iNorse, iTurks, iSpain, iHolyRome, iBurma, iVietnam, iMisr, iPortugal, iItaly, iThailand, iSweden, iRussia, iOttomans, iCongo, iIran, iNetherlands, iManchuria],
	lGoalsSucceeded = [(iJapan, 0), (iEngland, 0)],
	setupGoals = setupGoals,
	
	updateData = updateData,
	
	greatWall = GreatWall(
		tGraphicsTL = (118, 54),
		tGraphicsBR = (128, 58),
		lClearCulture = [(122, 57), (125, 59), (126, 59), (127, 59), (128, 59), (129, 57), (129, 58), (129, 59), (121, 58), (122, 58), (122, 59), (123, 59), (124, 59), (117, 55), (117, 56), (117, 57), (118, 57), (119, 57), (117, 58), (117, 59), (123, 58), (122, 56), (118, 55), (119, 55), (117, 54)],
		lGraphicsExceptions = [(118, 55), (118, 56), (118, 57), (118, 58), (119, 55), (119, 56), (119, 57), (119, 58), (120, 56), (120, 57), (120, 58), (121, 56), (121, 57), (121, 58), (122, 56), (122, 57), (122, 58), (123, 58)],
		
		lEffectAreas = [((118, 44), (129, 53)), ((117, 47), (117, 50)), ((123, 43), (125, 43)), ((119, 54), (128, 54)), ((120, 55), (125, 55)), ((123, 56), (128, 57)), ((124, 58), (128, 58))],
	),
)