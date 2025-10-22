from Resources import setupScenarioResources

from Scenario import *
from Locations import *
from RFCUtils import *
from Core import *

	
lCivilizations = [
	Civilization(
		iChina,
		iLeader=iHongwu,
		sLeaderName="TXT_KEY_LEADER_KANGXI",
		iGold=300,
		iStateReligion=iConfucianism,
		lCivics=[iDespotism, iBureaucracy, iManorialism, iRegulatedTrade, iSyncretism, iIsolationism],
		techs=techs.column(10).including(iHorticulture, iUrbanPlanning).without(iExploration, iOptics, iAcademia),
		dAttitudes={iKorea: 2}
	),
	Civilization(
		iIndia,
		iLeader=iShivaji,
		iGold=400,
		iStateReligion=iHinduism,
		lCivics=[iMonarchy, iTheocracy, iCasteSystem, iRegulatedTrade, iMonasticism, iHegemony],
		techs=techs.column(10).including(iCombinedArms, iUrbanPlanning).without(iExploration),
		dAttitudes={iMughals: -2}
	),
	Civilization(
		iDravidia,
		iLeader=iKrishnaDevaRaya,
		sLeaderName="TXT_KEY_LEADER_TIPU_SULTAN",
		iGold=400,
		iStateReligion=iHinduism,
		lCivics=[iMonarchy, iBureaucracy, iCasteSystem, iMerchantTrade, iMonasticism, iHegemony],
		techs=techs.column(10).including(iCombinedArms, iUrbanPlanning).without(iExploration, iOptics),
	),
	Civilization(
		iKorea,
		iLeader=iSejong,
		iGold=200,
		iStateReligion=iConfucianism,
		lCivics=[iDespotism, iBureaucracy, iCasteSystem, iRegulatedTrade, iSyncretism, iIsolationism],
		techs=techs.column(10).without(iExploration, iOptics, iAcademia),
		dAttitudes={iChina: 2}
	),
	Civilization(
		iJapan,
		iLeader=iOdaNobunaga,
		iGold=400,
		iStateReligion=iBuddhism,
		lCivics=[iMonarchy, iVassalage, iManorialism, iRegulatedTrade, iMonasticism, iIsolationism],
		techs=techs.column(10).including(iCombinedArms, iUrbanPlanning).without(iExploration, iOptics),
	),
	Civilization(
		iNorse, # Denmark
		iLeader=iChristian,
		iGold=150,
		iStateReligion=iProtestantism,
		lCivics=[iMonarchy, iBureaucracy, iManorialism, iRegulatedTrade, iClergy],
		techs=techs.column(10).including(iCombinedArms)
	),
	Civilization(
		iTurks, # Uzbeks
		iLeader=iTamerlane,
		iGold=50,
		iStateReligion=iIslam,
		lCivics=[iDespotism, iVassalage, iSlavery, iMerchantTrade, iClergy, iHegemony],
		techs=techs.column(9).including(iFirearms, iLogistics, iHeritage),
	),
	Civilization(
		iSpain,
		iLeader=iPhilip,
		iGold=400,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iTheocracy, iManorialism, iRegulatedTrade, iClergy, iColonialism],
		techs=techs.column(10).including(iCombinedArms, iGeography, iHorticulture),
		dAttitudes={iPortugal: 2}
	),
	Civilization(
		iFrance,
		iLeader=iLouis,
		iGold=400,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iBureaucracy, iManorialism, iRegulatedTrade, iClergy, iColonialism],
		techs=techs.column(11).without(iUrbanPlanning, iEconomics),
		dAttitudes={iEngland: -4, iHolyRome: -2, iOttomans: -2, iNetherlands: 2}
	),
	Civilization(
		iEngland,
		iLeader=iVictoria,
		iGold=600,
		iStateReligion=iProtestantism,
		lCivics=[iMonarchy, iBureaucracy, iIndividualism, iFreeEnterprise, iClergy, iColonialism],
		techs=techs.column(11).without(iUrbanPlanning, iHorticulture),
		dAttitudes={iFrance: -4, iPortugal: 2, iMughals: -2, iOttomans: -2}
	),
	Civilization(
		iHolyRome, # Austria
		iLeader=iFrancis,
		iGold=150,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iVassalage, iManorialism, iRegulatedTrade, iClergy, iHegemony],
		techs=techs.column(10).including(iCombinedArms, iUrbanPlanning, iHorticulture).without(iExploration),
		dAttitudes={iFrance: -2, iOttomans: -4}
	),
	Civilization(
		iBurma,
		iLeader=iBayinnaung,
		iGold=100,
		iStateReligion=iBuddhism,
		lCivics=[iDespotism, iVassalage, iCasteSystem, iRegulatedTrade, iMonasticism, iHegemony],
		techs=techs.column(9).including(iFirearms, iLogistics),
	),
	Civilization(
		iVietnam,
		iLeader=iLeLoi,
		iGold=150,
		iStateReligion=iConfucianism,
		lCivics=[iMonarchy, iBureaucracy, iCasteSystem, iRegulatedTrade, iSyncretism, iThalassocracy],
		techs=techs.column(9).including(iFirearms, iAcademia, iHeritage, iStatecraft),
	),
	Civilization(
		iPoland,
		iLeader=iSobieski,
		iGold=200,
		iStateReligion=iCatholicism,
		lCivics=[iElective, iVassalage, iManorialism, iRegulatedTrade, iSyncretism],
		techs=techs.column(11).without(iEconomics, iGeography, iHorticulture, iUrbanPlanning),
	),
	Civilization(
		iPortugal,
		iLeader=iJoao,
		iGold=450,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iBureaucracy, iManorialism, iRegulatedTrade, iClergy, iColonialism],
		techs=techs.column(10).including(iGeography, iHorticulture),
		dAttitudes={iSpain: 2, iEngland: 2, iNetherlands: -2}
	),
	Civilization(
		iMughals,
		iLeader=iAkbar,
		iGold=200,
		iStateReligion=iIslam,
		lCivics=[iMonarchy, iBureaucracy, iManorialism, iRegulatedTrade, iSyncretism, iHegemony],
		techs=techs.column(10).including(iUrbanPlanning, iHorticulture).without(iExploration, iOptics),
		dAttitudes={iEngland: -2, iIndia: -2, iIran: -2}
	),
	Civilization(
		iSweden,
		iLeader=iGustav,
		iGold=250,
		iStateReligion=iProtestantism,
		lCivics=[iMonarchy, iBureaucracy, iManorialism, iRegulatedTrade, iClergy, iHegemony],
		techs=techs.column(10).including(iCombinedArms, iScientificMethod, iUrbanPlanning),
		dAttitudes={iRussia: -2, iPoland: -2}
	),
	Civilization(
		iRussia,
		iLeader=iPeter,
		iGold=350,
		iStateReligion=iOrthodoxy,
		lCivics=[iDespotism, iTheocracy, iManorialism, iRegulatedTrade, iClergy, iHegemony],
		techs=techs.column(10).including(iCombinedArms, iUrbanPlanning).without(iExploration, iOptics),
		dAttitudes={iSweden: -2, iOttomans: -4}
	),
	Civilization(
		iOttomans,
		iLeader=iSuleiman,
		iGold=200,
		iStateReligion=iIslam,
		lCivics=[iDespotism, iBureaucracy, iSlavery, iRegulatedTrade, iSyncretism, iHegemony],
		techs=techs.column(10).including(iUrbanPlanning, iHorticulture).without(iExploration),
		dAttitudes={iIran: -4, iHolyRome: -4, iRussia: -4, iPoland: -2, iFrance: -2, iEngland: -2, iNetherlands: -2}
	),
	Civilization(
		iThailand,
		iLeader=iNaresuan,
		iGold=300,
		iStateReligion=iBuddhism,
		lCivics=[iMonarchy, iVassalage, iCasteSystem, iRegulatedTrade, iMonasticism, iThalassocracy],
		techs=techs.column(10).without(iExploration, iOptics),
	),
	Civilization(
		iCongo,
		iLeader=iMbemba,
		iGold=300,
		iStateReligion=iCatholicism,
		lCivics=[iElective, iVassalage, iSlavery, iRedistribution, iClergy],
		techs=techs.column(8).including(iCartography, iJudiciary),
	),
	Civilization(
		iIran,
		iLeader=iAbbas,
		iGold=200,
		iStateReligion=iIslam,
		lCivics=[iMonarchy, iTheocracy, iSlavery, iMerchantTrade, iFanaticism, iHegemony],
		techs=techs.column(10).including(iCombinedArms, iGeography, iUrbanPlanning, iHorticulture),
		dAttitudes={iMughals: -2, iOttomans: -4}
	),
	Civilization(
		iNetherlands,
		iLeader=iWilliam,
		iGold=800,
		iStateReligion=iProtestantism,
		lCivics=[iRepublic, iBureaucracy, iIndividualism, iFreeEnterprise, iSyncretism, iColonialism],
		techs=techs.column(10).including(iCombinedArms, iEconomics, iGeography, iScientificMethod, iCivilLiberties),
		dAttitudes={iFrance: 2, iPortugal: -2, iOttomans: -2}
	),
	Civilization(
		iGermany,
		iLeader=iFrederick,
		iGold=800,
		iStateReligion=iProtestantism,
		lCivics=[iMonarchy, iBureaucracy, iManorialism, iRegulatedTrade, iSyncretism, iHegemony],
		techs=techs.column(10).without(iGeography, iCivilLiberties, iHorticulture),
	),
	Civilization(
		iNative,
		iGold=300,
		techs=techs.column(7)
	),
	Civilization(
		iIndependent2,
		iGold=500,
		techs=techs.column(10)
	),
	Civilization(
		iIndependent,
		iGold=500,
		techs=techs.column(10)
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
		goals[2].requirements[0].accumulate(4)
	
	# Congolese slave trade goal
	if iCiv == iCongo:
		goals[1].requirements[0].accumulate(500)


def updateData():
	data.dFirstContactConquerors = {iMaya: True, iToltecs: True, iAztecs: True, iInca: True}
	
	data.civs[iChina].iResurrections = 2
	data.civs[iIndia].iResurrections = 1
	data.civs[iDravidia].iResurrections = 1


scenario1700AD = Scenario(
	iStartYear = 1700,
	fileName = "RFC_1700AD",
	
	lCivilizations = lCivilizations,
	lTribalVillages = lTribalVillages,
	
	dCivilizationDescriptions = {
		iTurks: "TXT_KEY_CIV_UZBEKS_DESC",
		iNorse: "TXT_KEY_CIV_DENMARK_DESC",
		iHolyRome: "TXT_KEY_CIV_AUSTRIA_DESC",
		iEngland: "TXT_KEY_CIV_BRITAIN_DESC",
		iGermany: "TXT_KEY_CIV_HOLY_ROMAN_DESC",
	},
	
	dOwnedTiles = {
		iFrance: [(59, 55)],
		iPortugal: [(53, 52), (54, 52), (55, 52), (55, 51), (55, 50), (54, 48)],
		iRussia: [(82, 64)],
		iNetherlands: [(62, 62)],
	},
	iCultureTurns = 100,
	
	dRevealed = {
		iCivGroupEurope: Revealed(
			lLandRegions=lEurope + lNorthAfrica + [rAnatolia, rMesopotamia, rArabia, rPersia], 
			lCoastRegions=lIndia + lEastAsia + lSubSaharanAfrica + lAmerica,
			lSeaAreas=[((29, 60), (50, 27)), ((28, 11), (58, 26)), ((79, 23), (97, 32)), ((111, 28), (123, 44)), ((0, 28), (21, 44))],
		),
		iCivGroupEastAsia: Revealed(
			lLandRegions=lEastAsia + [rTransoxiana],
		),
		iCivGroupSouthAsia: Revealed(
			lLandRegions=lIndia + [rIndochina, rIndonesia, rPersia, rKhorasan, rTransoxiana, rTibet, rArabia, rMesopotamia],
			lCoastRegions=[rEthiopia],
			lSeaAreas=[((79, 23), (97, 32))],
		),
		iCivGroupMiddleEast: Revealed(
			lLandRegions=lMiddleEast + lIndia + lNorthAfrica + [rSahel, rSahara, rEthiopia, rHornOfAfrica, rSwahiliCoast, rIberia, rItaly, rBalkans],
			lCoastRegions=lEastAsia + lCentralAmerica + [rCape, rBritain, rIreland, rFrance, rLowerGermany, rScandinavia, rPonticSteppe, rAtlanticSeaboard, rMaritimes, rDeepSouth, rBrazil],
			lSeaAreas=[((79, 23), (97, 32))],
		),
		iCivGroupAfrica: Revealed(
			lLandRegions=lSubSaharanAfrica,
			lCoastRegions=lSubSaharanAfrica,
		),
	},
	
	dGreatPeopleCreated = {
		iChina: 12,
		iIndia: 8,
		iPersia: 4,
		iDravidia: 5,
		iKorea: 6,
		iJapan: 6,
		iNorse: 8,
		iTurks: 4,
		iSpain: 8,
		iFrance: 8,
		iEngland: 8,
		iHolyRome: 8,
		iPoland: 8,
		iPortugal: 8,
		iMughals: 8,
		iOttomans: 8,
		iThailand: 8,
		iCongo: 4,
		iNetherlands: 6,
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
		iNorse : 1,
		iSpain : 7,
		iFrance : 3,
		iEngland : 3,
		iPortugal : 6,
		iNetherlands : 4,
	},
	
	lInitialWars = [
		(iEngland, iMughals, WarPlanTypes.WARPLAN_LIMITED),
		(iIndia, iMughals, WarPlanTypes.WARPLAN_TOTAL)
	],
	
	lAllGoalsFailed = [iChina, iIndia, iDravidia, iKorea, iNorse, iTurks, iSpain, iHolyRome, iBurma, iVietnam, iPoland, iPortugal, iMughals, iSweden, iRussia, iOttomans, iThailand],
	lGoalsSucceeded = [(iIran, 0), (iJapan, 0), (iFrance, 0), (iCongo, 0), (iNetherlands, 1)],
	setupGoals = setupGoals,
	
	updateData = updateData,
	
	greatWall = GreatWall(
		tGraphicsTL = (118, 54),
		tGraphicsBR = (128, 58),
		lClearCulture = [(122, 57), (125, 59), (126, 59), (127, 59), (128, 59), (129, 57), (129, 58), (129, 59)],
		lGraphicsExceptions = [(118, 55), (118, 56), (118, 57), (118, 58), (119, 55), (119, 56), (119, 57), (119, 58), (120, 56), (120, 57), (120, 58), (121, 56), (121, 57), (121, 58), (122, 56), (122, 57), (122, 58), (123, 58)],
		
		lEffectAreas = [((118, 44), (129, 53)), ((117, 47), (117, 50)), ((123, 43), (125, 43)), ((119, 54), (128, 54)), ((120, 55), (125, 55)), ((123, 56), (128, 57)), ((124, 58), (128, 58))],
	),
)