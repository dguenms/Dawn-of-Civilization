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
		lCivics=[iDespotism, iMeritocracy, iManorialism, iRegulatedTrade, iMonasticism, iIsolationism],
		techs=techs.column(10).including(iHorticulture, iUrbanPlanning).without(iExploration, iOptics, iAcademia),
		dAttitudes={iKorea: 2}
	),
	Civilization(
		iIndia,
		iLeader=iShivaji,
		iGold=400,
		iStateReligion=iHinduism,
		lCivics=[iMonarchy, iVassalage, iCasteSystem, iRegulatedTrade, iMonasticism, iConquest],
		techs=techs.column(10).including(iCombinedArms, iUrbanPlanning).without(iExploration),
		dAttitudes={iMughals: -2}
	),
	Civilization(
		iIran,
		iLeader=iAbbas,
		iGold=200,
		iStateReligion=iIslam,
		lCivics=[iMonarchy, iVassalage, iSlavery, iMerchantTrade, iTheocracy, iConquest],
		techs=techs.column(10).including(iCombinedArms, iGeography, iUrbanPlanning, iHorticulture),
		dAttitudes={iMughals: -2, iOttomans: -4}
	),
	Civilization(
		iTamils,
		iLeader=iKrishnaDevaRaya,
		sLeaderName="TXT_KEY_LEADER_TIPU_SULTAN",
		iGold=400,
		iStateReligion=iHinduism,
		lCivics=[iMonarchy, iCentralism, iCasteSystem, iMerchantTrade, iMonasticism, iConquest],
		techs=techs.column(10).including(iCombinedArms, iUrbanPlanning).without(iExploration, iOptics),
	),
	Civilization(
		iKorea,
		iLeader=iSejong,
		iGold=200,
		iStateReligion=iConfucianism,
		lCivics=[iDespotism, iMeritocracy, iCasteSystem, iRegulatedTrade, iMonasticism, iIsolationism],
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
		iVikings, # Sweden
		iLeader=iGustav,
		iGold=150,
		iStateReligion=iProtestantism,
		lCivics=[iMonarchy, iCentralism, iManorialism, iRegulatedTrade, iClergy],
		techs=techs.column(11).without(iEconomics, iHorticulture),
		dAttitudes={iRussia: -2, iPoland: -2}
	),
	Civilization(
		iTurks, # Uzbeks
		iLeader=iTamerlane,
		iGold=50,
		iStateReligion=iIslam,
		lCivics=[iDespotism, iVassalage, iSlavery, iMerchantTrade, iClergy, iTributaries],
		techs=techs.column(9).including(iFirearms, iLogistics, iHeritage),
	),
	Civilization(
		iSpain,
		iLeader=iPhilip,
		iGold=400,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iCentralism, iManorialism, iRegulatedTrade, iTheocracy, iColonialism],
		techs=techs.column(10).including(iCombinedArms, iGeography, iHorticulture),
		dAttitudes={iPortugal: 2}
	),
	Civilization(
		iFrance,
		iLeader=iLouis,
		iGold=400,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iCentralism, iIndividualism, iRegulatedTrade, iClergy, iColonialism],
		techs=techs.column(11).without(iUrbanPlanning, iEconomics),
		dAttitudes={iEngland: -4, iHolyRome: -2, iOttomans: -2, iNetherlands: 2}
	),
	Civilization(
		iEngland,
		iLeader=iVictoria,
		iGold=600,
		iStateReligion=iProtestantism,
		lCivics=[iMonarchy, iCentralism, iIndividualism, iFreeEnterprise, iTolerance, iColonialism],
		techs=techs.column(11).without(iUrbanPlanning, iHorticulture),
		dAttitudes={iFrance: -4, iPortugal: 2, iMughals: -2, iOttomans: -2}
	),
	Civilization(
		iHolyRome, # Austria
		iLeader=iFrancis,
		iGold=150,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iVassalage, iManorialism, iRegulatedTrade, iClergy],
		techs=techs.column(10).including(iCombinedArms, iUrbanPlanning, iHorticulture).without(iExploration),
		dAttitudes={iFrance: -2, iOttomans: -4}
	),
	Civilization(
		iRussia,
		iLeader=iPeter,
		iGold=350,
		iStateReligion=iOrthodoxy,
		lCivics=[iDespotism, iCentralism, iManorialism, iRegulatedTrade, iTheocracy],
		techs=techs.column(10).including(iCombinedArms, iUrbanPlanning).without(iExploration, iOptics),
		dAttitudes={iVikings: -2, iOttomans: -4}
	),
	Civilization(
		iPoland,
		iLeader=iSobieski,
		iGold=200,
		iStateReligion=iCatholicism,
		lCivics=[iElective, iCentralism, iManorialism, iRegulatedTrade, iClergy],
		techs=techs.column(11).without(iEconomics, iGeography, iHorticulture, iUrbanPlanning),
	),
	Civilization(
		iPortugal,
		iLeader=iJoao,
		iGold=450,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iCentralism, iManorialism, iRegulatedTrade, iClergy, iColonialism],
		techs=techs.column(10).including(iGeography, iHorticulture),
		dAttitudes={iSpain: 2, iEngland: 2, iNetherlands: -2}
	),
	Civilization(
		iMughals,
		iLeader=iAkbar,
		iGold=200,
		iStateReligion=iIslam,
		lCivics=[iDespotism, iVassalage, iManorialism, iRegulatedTrade, iClergy, iTributaries],
		techs=techs.column(10).including(iUrbanPlanning, iHorticulture).without(iExploration, iOptics),
		dAttitudes={iEngland: -2, iIndia: -2, iIran: -2}
	),
	Civilization(
		iOttomans,
		iLeader=iSuleiman,
		iGold=200,
		iStateReligion=iIslam,
		lCivics=[iDespotism, iMeritocracy, iSlavery, iRegulatedTrade, iTheocracy, iTributaries],
		techs=techs.column(10).including(iUrbanPlanning, iHorticulture).without(iExploration),
		dAttitudes={iIran: -4, iHolyRome: -4, iRussia: -4, iPoland: -2, iFrance: -2, iEngland: -2, iNetherlands: -2}
	),
	Civilization(
		iThailand,
		iLeader=iNaresuan,
		iGold=300,
		iStateReligion=iBuddhism,
		lCivics=[iMonarchy, iVassalage, iCasteSystem, iRegulatedTrade, iMonasticism, iTributaries],
		techs=techs.column(10).without(iExploration, iOptics),
	),
	Civilization(
		iCongo,
		iLeader=iMbemba,
		iGold=300,
		iStateReligion=iCatholicism,
		lCivics=[iElective, iVassalage, iSlavery, iRegulatedTrade, iClergy],
		techs=techs.column(8).including(iCartography, iJudiciary),
	),
	Civilization(
		iNetherlands,
		iLeader=iWilliam,
		iGold=800,
		iStateReligion=iProtestantism,
		lCivics=[iRepublic, iCentralism, iIndividualism, iFreeEnterprise, iTolerance, iColonialism],
		techs=techs.column(11).without(iHorticulture, iScientificMethod),
		dAttitudes={iFrance: 2, iPortugal: -2, iOttomans: -2}
	),
	Civilization(
		iGermany,
		iLeader=iFrederick,
		iGold=800,
		iStateReligion=iProtestantism,
		lCivics=[iMonarchy, iCentralism, iManorialism, iRegulatedTrade, iClergy, iConquest],
		techs=techs.column(11).without(iGeography, iCivilLiberties, iHorticulture, iUrbanPlanning),
	),
	Civilization(
		iIndependent,
		iGold=500,
		techs=techs.column(10)
	),
	Civilization(
		iIndependent2,
		iGold=500,
		techs=techs.column(10)
	),
	Civilization(
		iNative,
		iGold=300,
		techs=techs.column(7)
	),
]
	

def createStartingUnits():
	# Japan
	capital = plots.capital(iJapan)
	if not player(iJapan).isHuman():
		createRoleUnit(iJapan, capital, iSettle)


scenario1700AD = Scenario(
	iStartYear = 1700,
	iStartTurn = 321,
	fileName = "RFC_1700AD",
	
	lCivilizations = lCivilizations,
	
	dOwnedTiles = {
		iHolyRome : [(62, 51)],
		iRussia : [(69, 54), (69, 55)],
		iPortugal : [(47, 45), (48, 45), (49, 40), (50, 42), (50, 43), (50, 44)],
		iPoland : [(64, 53), (65, 56), (66, 55), (66, 56), (68, 53), (68, 54), (68, 56)],
		iNetherlands : [(58, 52), (58, 53)],
		iGermany : [(58, 49), (59, 49), (60, 49)],
	},
	iOwnerBaseCulture = 100,
	
	dGreatPeopleCreated = {
		iChina: 12,
		iIndia: 8,
		iPersia: 4,
		iTamils: 5,
		iKorea: 6,
		iJapan: 6,
		iVikings: 8,
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
		iTamils: 2,
		iKorea: 3,
		iJapan: 3,
		iVikings: 3,
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
		iVikings : 1,
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
	
	greatWall = GreatWall(
		tGraphicsTL = (99, 46),
		tGraphicsBR = (106, 49),
		lGraphicsExceptions = [(99, 47), (99, 48), (99, 49), (100, 49), (101, 49), (104, 49)],
		lBorderExceptions = [(99, 45)],
		lClearCulture = [(103, 50), (104, 50), (105, 50), (106, 50)],
		
		lEffectAreas = [((99, 40), (104, 49)), ((103, 39), (107, 45))],
	),
	
	createStartingUnits = createStartingUnits,
)