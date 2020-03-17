# Rhye's and Fall of Civilization - Constants
# globals

from CvPythonExtensions import *
from DataStructures import *
gc = CyGlobalContext()

iWorldX = 124
iWorldY = 68

# initialise player variables to player IDs from WBS
iNumPlayers = 45
(iEgypt, iBabylonia, iHarappa, iChina, iGreece, iIndia, iCarthage, iPolynesia, iPersia, iRome, 
iMaya, iTamils, iEthiopia, iKorea, iByzantium, iJapan, iVikings, iTurks, iArabia, iTibet, 
iIndonesia, iMoors, iSpain, iFrance, iKhmer, iEngland, iHolyRome, iRussia, iMali, iPoland, 
iPortugal, iInca, iItaly, iMongolia, iAztecs, iMughals, iOttomans, iThailand, iCongo, iNetherlands, 
iGermany, iAmerica, iArgentina, iBrazil, iCanada) = range(iNumPlayers)

(pEgypt, pBabylonia, pHarappa, pChina, pGreece, pIndia, pPhoenicia, pPolynesia, pPersia, pRome, 
pMaya, pTamils, pEthiopia, pKorea, pByzantium, pJapan, pVikings, pTurks, pArabia, pTibet, 
pIndonesia, pMoors, pSpain, pFrance, pKhmer, pEngland, pHolyRome, pRussia, pMali, pPoland, 
pPortugal, pInca, pItaly, pMongolia, pAztecs, pMughals, pOttomans, pThailand, pCongo, pNetherlands, 
pGermany, pAmerica, pArgentina, pBrazil, pCanada) = [gc.getPlayer(i) for i in range(iNumPlayers)]

(teamEgypt, teamBabylonia, teamHarappa, teamChina, teamGreece, teamIndia, teamCarthage, teamPolynesia, teamPersia, teamRome, 
teamMaya, teamTamils, teamEthiopia, teamKorea, teamByzantium, teamJapan, teamVikings, teamTurks, teamArabia, teamTibet, 
teamIndonesia, teamMoors, teamSpain, teamFrance, teamKhmer, teamEngland, teamHolyRome, teamRussia, teamMali, teamPoland, 
teamPortugal, teamInca, teamItaly, teamMongolia, teamAztecs, teamMughals, teamOttomans, teamThailand, teamCongo, teamNetherlands, 
teamGermany, teamAmerica, teamArgentina, teamBrazil, teamCanada) = [gc.getTeam(i) for i in range(iNumPlayers)]

iHolland = iNetherlands
iDelhi = iMughals
iSiam = iThailand
iPhoenicia = iCarthage
iHRE = iHolyRome
iAustria = iHolyRome
iPrussia = iGermany

iNumMajorPlayers = iNumPlayers
iNumActivePlayers = iNumPlayers

iIndependent = iNumPlayers
iIndependent2 = iNumPlayers+1
iNative = iNumPlayers+2
iCeltia = iNumPlayers+3
iNumTotalPlayers = iNumPlayers+4
iBarbarian = iNumPlayers+4
iNumTotalPlayersB = iBarbarian+1

(pIndependent, pIndependent2, pNative, pCeltia, pBarbarian) = [gc.getPlayer(i) for i in range(iIndependent, iNumTotalPlayersB)]
(teamIndependent, teamIndependent2, teamNative, teamCeltia, teamBarbarian) = [gc.getTeam(i) for i in range(iIndependent, iNumTotalPlayersB)]

# civilizations, not players
iNumCivs = 57
(iCivAmerica, iCivArabia, iCivArgentina, iCivAztec, iCivBabylonia, iCivBrazil, iCivByzantium, iCivCanada, iCivCarthage, iCivCelt, 
iCivChina, iCivColombia, iCivEgypt, iCivEngland, iCivEthiopia, iCivFrance, iCivGermany, iCivGreece, iCivHarappa, iCivHolyRome, 
iCivInca, iCivIndia, iCivIndonesia, iCivIran, iCivItaly, iCivJapan, iCivKhmer, iCivKongo, iCivKorea, iCivMali, 
iCivMaya, iCivMexico, iCivMongols, iCivMoors, iCivMughals, iCivNativeAmericans, iCivNetherlands, iCivOttomans, iCivPersia, iCivPoland, 
iCivPolynesia, iCivPortugal, iCivRome, iCivRussia, iCivSpain, iCivSumeria, iCivTamils, iCivThailand, iCivTibet, iCivTurks,
iCivVikings, iCivZulu, iCivIndependent, iCivIndependent2, iCivNative, iCivMinor, iCivBarbarian) = range(iNumCivs)

iCivPhoenicia = iCivCarthage
iCivCongo = iCivKongo
iCivAztecs = iCivAztec
iCivCeltia = iCivCelt

# TODO: add iCivIran, iCivMexico, iCivColombia everywhere

# slot order
lCivOrder = [iCivEgypt, iCivBabylonia, iCivHarappa, iCivChina, iCivGreece, iCivIndia, iCivCarthage, iCivPolynesia, iCivPersia, iCivRome, iCivMaya, iCivTamils, iCivEthiopia, iCivKorea, iCivByzantium, iCivJapan, iCivVikings, iCivTurks, iCivArabia, iCivTibet, iCivIndonesia, iCivMoors, iCivSpain, iCivFrance, iCivKhmer, iCivEngland, iCivHolyRome, iCivRussia, iCivMali, iCivPoland, iCivPortugal, iCivInca, iCivItaly, iCivMongols, iCivAztecs, iCivMughals, iCivOttomans, iCivThailand, iCivCongo, iCivIran, iCivNetherlands, iCivGermany, iCivAmerica, iCivArgentina, iCivMexico, iCivColombia, iCivBrazil, iCivCanada, iCivIndependent, iCivIndependent2, iCivNative, iCivCeltia, iCivBarbarian]

# used in: Congresses, DynamicCivs, Plague, RFCUtils, UniquePowers, Victory
# a civilisation can be in multiple civ groups
iNumCivGroups = 6
(iCivGroupEurope, iCivGroupAsia, iCivGroupMiddleEast, iCivGroupMediterranean, iCivGroupAfrica, iCivGroupAmerica) = range(iNumCivGroups)

dCivGroups = {
iCivGroupEurope : [iCivGreece, iCivRome, iCivByzantium, iCivVikings, iCivMoors, iCivSpain, iCivFrance, iCivEngland, iCivHolyRome, iCivRussia, iCivNetherlands, iCivItaly, iCivPoland, iCivPortugal, iCivGermany],
iCivGroupAsia : [iCivIndia, iCivChina, iCivHarappa, iCivPolynesia, iCivPersia, iCivJapan, iCivTamils, iCivKorea, iCivByzantium, iCivTibet, iCivKhmer, iCivIndonesia, iCivRussia, iCivMongolia, iCivMughals, iCivThailand, iCivTurks],
iCivGroupMiddleEast : [iCivEgypt, iCivBabylonia, iCivPersia, iCivByzantium, iCivArabia, iCivOttomans, iCivCarthage, iCivTurks],
iCivGroupAfrica : [iCivEgypt, iCivCarthage, iCivEthiopia, iCivMali, iCivCongo],
iCivGroupAmerica : [iCivMaya, iCivInca, iCivAztecs, iCivAmerica, iCivArgentina, iCivBrazil, iCivCanada],
}

# used in: Stability
# tech groups share techs within each other on respawn
iNumTechGroups = 4
(iTechGroupWestern, iTechGroupMiddleEast, iTechGroupFarEast, iTechGroupNativeAmerica) = range(iNumTechGroupe)

dTechGroups = {
iTechGroupWestern : [iCivRome, iCivGreece, iCivByzantium, iCivVikings, iCivSpain, iCivFrance, iCivEngland, iCivHolyRome, iCivRussia, iCivNetherlands, iCivPoland, iCivPortugal, iCivItaly, iCivGermany, iCivAmerica, iCivArgentina, iCivBrazil, iCivCanada],
iTechGroupMiddleEast : [iCivEgypt, iCivBabylonia, iCivHarappa, iCivIndia, iCivCarthage, iCivPersia, iCivEthiopia, iCivArabia, iCivMoors, iCivMali, iCivOttomans, iCivMughals, iCivTamils, iCivCongo, iCivTurks],
iTechGroupFarEast : [iCivChina, iCivKorea, iCivJapan, iCivTibet, iCivKhmer, iCivIndonesia, iCivMongolia, iCivThailand],
iTechGroupNativeAmerica : [iCivPolynesia, iCivMaya, iCivInca, iCivAztecs],
}

lBioNewWorld = [iCivMaya, iCivInca, iCivAztecs]


#for Victory and the handler
tAmericasTL = (3, 0)
tAmericasBR = (43, 63)

# Colombian UP
tSouthCentralAmericaTL = (13, 3)
tSouthCentralAmericaBR = (43, 39)

# English colonists
tCanadaTL = (10, 49)
tCanadaBR = (37, 58)
tAustraliaTL = (103, 5)
tAustraliaBR = (123, 22)

# new capital locations
tVienna = (62, 49)
tWarsaw = (65, 52)
tStockholm = (63, 59)
tIstanbul = (68, 45)
tBeijing = (102, 47)
tEsfahan = (81, 41)
tHamburg = (59, 53)
tMilan = (59, 47)
tBaghdad = (77, 40)
tMumbai = (88, 34)
tMysore = (90, 31)

#for messages
iDuration = 14
iWhite = 0
iRed = 7
iGreen = 8
iBlue = 9
iLightBlue = 10
iYellow = 11
iDarkPink = 12
iLightRed = 20
iPurple = 25
iCyan = 44
iBrown = 55
iOrange = 88
iTan = 90
iLime = 100

# independent cities
iNumMinorCities = 40

# scripted conquerors
iNumConquests = 13

dNeighbours = appenddict({
iCivEypt : [iCivBabylonia, iCivGreece, iCivPersia, iCivCarthage, iCivRome, iCivEthiopia, iCivByzantium, iCivArabia, iCivMoors, iCivOttomans],
iCivBabylonia : [iCivEgypt, iCivGreece, iCivPersia, iCivTurks, iCivOttomans, iCivMongolia, iCivCarthage, iCivByzantium],
iCivHarappa : [iCivIndia, iCivPersia, iCivTamils, iCivTibet, iCivMughals],
iCivChina : [iCivIndia, iCivJapan, iCivKorea, iCivTurks, iCivTibet, iCivKhmer, iCivMongolia, iCivThailand],
iCivGreece : [iCivPersia, iCivCarthage, iCivRome, iCivByzantium, iCivHolyRome, iCivRussia, iCivOttomans, iCivItaly],
iCivIndia : [iCivChina, iCivHarappa, iCivPersia, iCivTamils, iCivTibet, iCivKhmer, iCivMongolia, iCivMughals, iCivThailand],
iCivCarthage : [iCivEgypt, iCivGreece, iCivRome, iCivSpain, iCivMali, iCivPortugal, iCivBabylonia, iCivPersia, iCivArabia, iCivMoors, iCivOttomans, iCivItaly],
iCivPersia : [iCivIndia, iCivBabylonia, iCivHarappa, iCivGreece, iCivTurks, iCivByzantium, iCivOttomans, iCivMongolia, iCivCarthage, iCivMughals],
iCivRome : [iCivEgypt, iCivBabylonia, iCivGreece, iCivCarthage, iCivSpain, iCivFrance, iCivHolyRome, iCivPortugal, iCivItaly, iCivGermany],
iCivTamils : [iCivHarappa, iCivIndia, iCivKhmer, iCivIndonesia, iCivMughals, iCivThailand],
iCivEthiopia : [iCivEgypt, iCivArabia, iCivMali, iCivCongo],
iCivKorea : [iCivChina, iCivKorea, iCivMongolia],
iCivMaya : [iCivSpain, iCivInca, iCivAztecs, iCivAmerica],
iCivByzantium : [iCivEgypt, iCivBabylonia, iCivGreece, iCivPersia, iCivArabia, iCivRussia, iCivOttomans, iCivTurks],
iCivJapan : [iCivChina, iCivKorea, iCivKhmer, iCivMongolia, iCivThailand],
iCivVikings : [iCivFrance, iCivEngland, iCivHolyRome, iCivRussia, iCivPoland, iCivNetherlands, iCivGermany],
iCivTurks : [iCivChina, iCivBabylonia, iCivPersia, iCivMughals, iCivOttomans, iCivByzantium, iCivMongolia, iCivTibet],
iCivArabia : [iCivEgypt, iCivBabylonia, iCivPersia, iCivEthiopia, iCivByzantium, iCivOttomans, iCivCarthage],
iCivTibet : [iCivChina, iCivHarappa, iCivIndia, iCivMongolia, iCivMughals, iCivTurks],
iCivIndonesia : [iCivIndia, iCivJapan, iCivKhmer, iCivThailand, iCivTamils],
iCivMoors : [iCivEgypt, iCivSpain, iCivPortugal, iCivMali],
iCivSpain : [iCivCarthage, iCivRome, iCivMoors, iCivFrance, iCivEngland, iCivPortugal],
iCivFrance : [iCivRome, iCivVikings, iCivSpain, iCivEngland, iCivHolyRome, iCivNetherlands, iCivPortugal, iCivItaly, iCivGermany],
iCivKhmer : [iCivIndia, iCivChina, iCivTamils, iCivJapan, iCivIndonesia, iCivThailand],
iCivEngland : [iCivRome, iCivVikings, iCivSpain, iCivFrance, iCivHolyRome, iCivNetherlands, iCivGermany],
iCivHolyRome : [iCivRome, iCivVikings, iCivFrance, iCivEngland, iCivNetherlands, iCivItaly, iCivPoland, iCivGermany],
iCivRussia : [iCivPersia, iCivByzantium, iCivVikings, iCivPoland, iCivOttomans, iCivMongolia, iCivGermany],
iCivMali : [iCivEgypt, iCivCarthage, iCivEthiopia, iCivMoors, iCivCongo],
iCivPoland : [iCivVikings, iCivHolyRome, iCivRussia, iCivGermany],
iCivPortugal : [iCivCarthage, iCivRome, iCivSpain, iCivFrance],
iCivInca : [iCivSpain, iCivAztecs, iCivAmerica, iCivArgentina, iCivBrazil],
iCivItaly : [iCivGreece, iCivCarthage, iCivRome, iCivFrance, iCivHolyRome],
iCivMongols : [iCivIndia, iCivChina, iCivPersia, iCivJapan, iCivKorea, iCivTibet, iCivRussia, iCivOttomans, iCivTurks],
iCivAztecs : [iCivSpain, iCivInca, iCivAmerica],
iCivMughals : [iCivHarappa, iCivIndia, iCivPersia, iCivTamils, iCivTibet, iCivTurks],
iCivOttomans : [iCivBabylonia, iCivGreece, iCivPersia, iCivByzantium, iCivRussia, iCivMongolia, iCivCarthage, iCivTurks],
iCivThailand : [iCivIndia, iCivChina, iCivJapan, iCivIndonesia, iCivKhmer, iCivTamils],
iCivCongo : [iCivEthiopia, iCivMali],
iCivNetherlands : [iCivVikings, iCivFrance, iCivEngland, iCivHolyRome, iCivGermany],
iCivGermany : [iCivRome, iCivVikings, iCivFrance, iCivEngland, iCivHolyRome, iCivRussia, iCivPoland, iCivNetherlands],
iCivAmerica : [iCivJapan, iCivSpain, iCivFrance, iCivEngland, iCivRussia, iCivInca, iCivAztecs],
iCivArgentina : [iCivSpain, iCivPortugal, iCivInca, iCivBrazil],
iCivBrazil : [iCivSpain, iCivPortugal, iCivInca, iCivArgentina],
iCivCanada : [iCivAmerica],
})

dBirth = {
iCivEgypt : -3000,
iCivBabylonia : -3000,
iCivHarappa : -3000,
iCivChina : -2070,
iCivGreece : -1600,
iCivIndia : -1500,
iCivPhoenicia : -1200,
iCivPolynesia : -1000,
iCivPersia : -850,
iCivRome : -753,
iCivMaya : -400,
iCivTamils : -300,
iCivEthiopia : -290,
iCivKorea : -50,
iCivByzantium : 330,
iCivJapan : 525,
iCivVikings : 551,
iCivTurks : 552,
iCivArabia : 620,
iCivTibet : 630,
iCivIndonesia : 650,
iCivMoors : 711,
iCivSpain : 722,
iCivFrance : 750,
iCivKhmer : 800,
iCivEngland : 820,
iCivHolyRome : 840,
iCivRussia : 860,
iCivMali : 989,
iCivPoland : 1025,
iCivPortugal : 1130,
iCivInca : 1150,
iCivItaly : 1167,
iCivMongolia : 1190,
iCivAztecs : 1195,
iCivMughals : 1206,
iCivOttomans : 1280,
iCivThailand : 1350,
iCivCongo : 1390,
iCivNetherlands : 1580,
iCivGermany : 1700,
iCivAmerica : 1776,
iCivArgentina : 1810,
iCivBrazil : 1822,
iCivCanada : 1867,
}

dFall = {
iCivEgypt : -343,
iCivBabylonia : -539,
iCivHarappa : -1700,
iCivChina : 1127,
iCivGreece : -146,
iCivIndia : 600,
iCivPhoenicia : -146,
iCivPolynesia : 1200,
iCivPersia : 651,
iCivRome : 235,
iCivMaya : 900,
iCivTamils : 1000,
iCivEthiopia : 960,
iCivKorea : 1255,
iCivByzantium : 1204,
iCivVikings : 1300,
iCivTurks : 1507,
iCivArabia : 900,
iCivTibet : 1500,
iCivIndonesia : 1500,
iCivMoors : 1500,
iCivKhmer : 1200,
iCivMali : 1600,
iCivPoland : 1650,
iCivInca : 1533,
iCivMongols : 1368,
iCivAztecs : 1521,
iCivMughals : 1640,
iCivCongo : 1800,
}

dVictoryYears = {
iCivEgypt : (-850, -100, 170),
iCivBabylonia : (-1, -850, -700),
iCivHarappa : (-1600, -1500, -800),
iCivChina : (1000, -1, 1800),
iCivGreece : (-1, -330, -250),
iCivIndia : (-100, 700, 1200),
iCivCarthage : (-300, -100, 200),
iCivPolynesia : (800, 1000, 1200),
iCivPersia : (140, 350, 350),
iCivRome : (100, 320, -1),
iCivMaya : (200, 900, -1),
iCivTamils : (800, 1000, 1200),
iCivEthiopia : (400, 1200, 1500),
iCivKorea : (1200, -1, -1),
iCivByzantium : (1000, 1200, 1450),
iCivJapan : (1600, 1940, -1),
iCivVikings : (1050, 1100, 1500),
iCivTurks : (900, 1100, 1400),
iCivArabia : (1300, 1300, -1),
iCivTibet : (1000, 1400, 1700),
iCivIndonesia : (1300, 1500, 1940),
iCivMoors : (1200, 1300, 1650),
iCivSpain : (-1, 1650, 1650),
iCivFrance : (1700, 1800, 1900),
iCivKhmer : (1200, 1450, 1450),
iCivEngland : (1730, 1800, -1),
iCivHolyRome : (1550, 1650, 1850),
iCivRussia : (1920, -1, 1950),
iCivMali : (1350, 1500, 1700),
iCivPoland : (1400, -1, 1600),
iCivPortugal : (1550, 1650, 1700),
iCivInca : (1500, 1550, 1700),
iCivItaly : (1500, 1600, 1930),
iCivMongols : (1300, -1, 1500),
iCivAztec : (1520, 1650, -1),
iCivMughals : (1500, 1660, 1750),
iCivOttomans : (1550, 1700, 1800),
iCivThailand : (1650, 1700, 1900),
iCivCongo : (1650, 1800, -1),
iCivIran : (1650, 1750, 1800),
iCivNetherlands : (1745, 1745, 1775),
iCivGermany : (1900, 1940, -1),
iCivAmerica : (1900, 1950, 2000),
iCivMexico : (1880, 1940, 1960),
iCivArgentina : (1930, 1960, 2000),
iCivColombia : (1870, 1920, 1950),
iCivBrazil : (1880, -1, 1950),
iCivCanada : (1920, 1950, 2000),
}

# Leoreth: date-triggered respawn for certain civs
dRebirth = {
iCivPersia : 1501,		# Iran
iCivMaya : 1814,		# Colombia
iCivAztecs : 1810,		# Mexico
}

dRebirthCiv = {
iCivPersia : iCivIran,
iCivMaya : iCivColombia,
iCivAztecs : iCivMexico,
}

dResurrections = appenddict({
iCivEgypt : [(900, 1300), (1800, 2020)],
iCivBabylonia : [(-3000, -500)],
iCivChina : [(600, 2020)],
iCivGreece : [(1800, 2020)],
iCivIndia : [(1600, 1800), (1900, 2020)],
iCivPhoenicia : [(-1000, -150)],
iCivPersia : [(220, 650)],
iCivRome : [(-750, 450)],
iCivMaya : [(0, 800)],
iCivTamils : [(-300, 600), (1300, 1650)],
iCivEthiopia : [(1270, 1520), (1850, 2020)],
iCivKorea : [(1800, 2020)],
iCivByzantium : [(1100, 1280)],
iCivJapan : [(1800, 2020)],
iCivVikings : [(1520, 2020)],
iCivTurks : [(1350, 1500)],
iCivArabia : [(1900, 2020)],
iCivIndonesia : [(1900, 2020)],
iCivMoors : [(1000, 2020)],
iCivSpain : [(1700, 2020)],
iCivFrance : [(1700, 2020)],
iCivKhmer : [(1950, 2020)],
iCivEngland : [(1700, 2020)],
iCivHolyRome : [(1800, 2020)],
iCivRussia : [(1280, 1550), (1700, 2020)],
iCivMali : [(1340, 1590)],
iCivPoland : [(1920, 2020)],
iCivPortugal : [(1700, 2020)],
iCivInca : [(1800, 1930)],
iCivItaly : [(1820, 2020)],
iCivMongols : [(1910, 2020)],
iCivMughals : [(1940, 2020)],
iCivOttomans : [(1700, 2020)],
iCivThailand : [(1700, 2020)],
iCivIran : [(1500, 2020)],
iCivNetherlands : [(1700, 2020)],
iCivGermany : [(1840, 2020)],
iCivAmerica : [(1776, 2020)],
iCivArgentina : [(1810, 2020)],
iCivMexico : [(1810, 2020)],
iCivColombia : [(1810, 2020)],
iCivBrazil : [(1820, 2020)],
iCivCanada : [(1867, 2020)],
})

dEnemyCivsOnSpawn = appenddict({
iCivBabylonia : [iCivIndependent, iCivIndependent2],
iCivChina : [iCivIndependent, iCivIndependent2, iCivIndependent2],
iCivGreece : [iCivIndependent, iCivIndependent2, iCivBabylonia],
iCivPersia : [iCivBabylonia, iCivBabylonia, iCivGreece, iCivCarthage, iCivCarthage],
iCivByzantium : [iCivGreece, iCivPersia],
iCivVikings : [iCivEngland, iCivEngland, iCivFrance, iCivIndependent, iCivIndependent2],
iCivTurks : [iCivChina, iCivChina, iCivPersia, iCivPersia, iCivIndependent, iCivIndependent, iCivIndependent2, iCivIndependent2],
iCivArabia : [iCivEgypt, iCivEgypt, iCivEgypt, iCivBabylonia, iCivBabylonia, iCivGreece, iCivPersia, iCivCarthage, iCivRome, iCivByzantium, iCivByzantium, iCivSpain, iCivFrance, iCivCeltia, iCivCeltia, iCivIndependent, iCivIndependent2],
iCivIndonesia : [iCivKhmer, iCivKhmer],
iCivArabia : [iCivRome, iCivArabia, iCivArabia],
iCivMongols : [iCivChina, iCivChina, iCivChina, iCivKorea, iCivKorea, iCivTurks, iCivTurks, iCivTurks, iCivIndependent, iCivIndependent, iCivIndependent2, iCivIndependent2],
iCivAztecs : [iCivMaya],
iCivMughals : [iCivIndia, iCivIndia],
iCivOttomans : [iCivEgypt, iCivEgypt, iCivBabylonia, iCivGreece, iCivGreece, iCivArabia, iCivArabia, iCivArabia, iCivByzantium, iCivByzantium, iCivByzantium],
iCivThailand : [iCivKhmer, iCivKhmer, iCivKhmer],
iCivGermany : [iCivHolyRome, iCivPoland],
iCivAmerica : [iCivIndependent, iCivIndependent2],
iCivArgentina : [iCivSpain, iCivSpain, iCivIndependent, iCivIndependent2],
iCivMexico : [iCivSpain, iCivSpain, iCivIndependent, iCivIndependent2],
iCivColombia : [iCivSpain, iCivSpain, iCivIndependent, iCivIndependent2],
iCivBrazil : [iCivIndependent, iCivIndependent2],
})

dTotalWarOnSpawn = appenddict({
iCivPersia : [iiCivBabylonia, iCivCarthage],
iCivRome : [iCivGreece],
iCivByzantium : [iCivGreece],
iCivArabia : [iCivEgypt, iCivBabylonia, iCivCarthage, iCivPersia],
iCivSpain : [iCivMoors],
iCivHolyRome : [iCivRome],
iCivMongols : [iCivChina],
iCivAztecs : [iCivMaya],
iCivMughals : [iCivIndia],
iCivOttomans : [iCivArabia, iCivEgypt],
iCivThailand : [iCivKhmer],
})

dAggressionLevel = defaultdict({
iCivBabylonia : 1,
iCivChina : 1,
iCivGreece : 2,
iCivPersia : 3,
iCivRome : 3,
iCivMaya : 1,
iCivTamils : 1,
iCivByzantium : 1,
iCivJapan : 1,
iCivViking : 2,
iCivTurks : 2,
iCivArabia : 2,
iCivTibet : 1,
iCivIndonesia : 1,
iCivMoors : 1,
iCivSpain : 2,
iCivFrance : 1,
iCivKhmer : 2,
iCivEngland : 1,
iCivHolyRome : 1,
iCivRussia : 1,
iCivPoland : 1,
iCivInca : 1,
iCivMongols : 3,
iCivAztecs : 2,
iCivMughals : 1,
iCivOttomans : 2,
iCivIran : 1,
iCivGermany : 2,
iCivAmerica : 2,
iCivColombia : 2,
iCivMexico : 1,
iCivArgentina : 1,
}, 0)

dAIStopBirthThreshold = defaultdict({
iCivEgypt : 80,
iCivBabylonia : 50,
iCivHarappa : 50,
iCivChina : 60,
iCivGreece : 50,
iCivIndia : 80,
iCivCarthage : 80,
iCivPolynesia : 80,
iCivPersia : 70,
iCivRome : 80,
iCivMaya : 80,
iCivTamils : 80,
iCivEthiopia : 80,
iCivKorea : 80,
iCivByzantium : 80,
iCivJapan : 80,
iCivVikings : 80,
iCivTurks : 50,
iCivArabia : 80,
iCivTibet : 80,
iCivIndonesia : 80,
iCivMoors : 80,
iCivSpain : 80,
iCivFrance : 80,
iCivKhmer : 80,
iCivEngland : 50,
iCivHolyRome : 80,
iCivRussia : 50,
iCivMali : 70,
iCivPoland : 40,
iCivPortugal : 40,
iCivInca : 70,
iCivItaly : 60,
iCivMongols : 70,
iCivAztecs : 50,
iCivMughals : 70,
iCivOttomans : 70,
iCivThailand : 80,
iCivCongo : 80,
iCivIran : 80,
iCivNetherlands : 40,
iCivGermany : 80,
iCivAmerica : 50,
iCivArgentina : 60,
iCivMexico : 60,
iCivColombia : 60,
iCivBrazil : 60,
iCivCanada : 60,
}, 100)

dResurrectionProbability = {
iCivEgypt : 25,
iCivBabylonia : 40,
iCivHarappa : 0,
iCivChina : 100,
iCivGreece : 60,
iCivIndia : 50,
iCivPhoenicia : 30,
iCivPolynesia : 40,
iCivPersia : 70,
iCivRome : 65,
iCivMaya : 30,
iCivTamils : 10,
iCivEthiopia : 80,
iCivKorea : 80,
iCivByzantium : 65,
iCivJapan : 100,
iCivVikings : 60,
iCivTurks : 30,
iCivArabia : 100,
iCivTibet : 60,
iCivIndonesia : 80,
iCivMoors : 70,
iCivSpain : 100,
iCivFrance : 100,
iCivKhmer : 60,
iCivEngland : 100,
iCivHolyRome : 80,
iCivRussia : 100,
iCivMali : 30,
iCivPoland : 65,
iCivPortugal : 100,
iCivInca : 70,
iCivItaly : 100,
iCivMongols : 80,
iCivAztecs : 70,
iCivMughals : 80,
iCivOttomans : 100,
iCivThailand : 100,
iCivCongo : 20,
iCivIran : 100,
iCivNetherlands : 100,
iCivGermany : 100,
iCivAmerica : 100,
iCivArgentina : 100,
iCivMexico : 100,
iCivColombia : 80,
iCivBrazil : 100,
iCivCanada : 100,
}

dPatienceThreshold = defaultdict({
iCivEgypt : 30,
iCivBabylonia : 30,
iCivHarappa : 30,
iCivChina : 30,
iCivGreece : 35,
iCivIndia : 50,
iCivPhoenicia : 35,
iCivPolynesia : 50,
iCivPersia : 30,
iCivRome : 25,
iCivMaya : 35,
iCivTamils : 45,
iCivEthiopia : 20,
iCivKorea : 25,
iCivByzantium : 25,
iCivJapan : 25,
iCivVikings : 30,
iCivTurks : 30,
iCivArabia : 30,
iCivTibet : 50,
iCivIndonesia : 30,
iCivMoors : 20,
iCivSpain : 20,
iCivFrance : 20,
iCivKhmer : 30,
iCivEngland : 20,
iCivHolyRome : 20,
iCivRussia : 30,
iCivMali : 35,
iCivPoland : 20,
iCivPortugal : 30,
iCivInca : 35,
iCivItaly : 25,
iCivMongols : 20,
iCivAztecs : 30,
iCivMughals : 35,
iCivOttomans : 35,
iCivThailand : 30,
iCivCongo : 20,
iCivIran : 30,
iCivNetherlands : 30,
iCivGermany : 20,
iCivAmerica : 30,
iCivArgentina : 40,
iCivMexico : 40,
iCivColombia : 30,
iCivBrazil : 40,
iCivCanada : 40,
}, 100)

dMaxColonists = {
iCivVikings : 1,
iCivSpain : 7,
iCivFrance : 5,
iCivEngland : 6,
iCivPortugal : 6, 
iCivNetherlands : 6,
iCivGermany : 2
}

# initialise religion variables to religion indices from XML
iNumReligions = 10
(iJudaism, iOrthodoxy, iCatholicism, iProtestantism, iIslam, iHinduism, iBuddhism, iConfucianism, iTaoism, iZoroastrianism) = range(iNumReligions)

#Persecution preference
tPersecutionPreference = (
(iHinduism, iBuddhism, iTaoism, iConfucianism, iZoroastrianism, iIslam, iProtestantism, iCatholicism, iOrthodoxy), # Judaism
(iIslam, iProtestantism, iCatholicism, iJudaism, iZoroastrianism, iHinduism, iBuddhism, iTaoism, iConfucianism), # Orthodoxy
(iIslam, iProtestantism, iOrthodoxy, iJudaism, iZoroastrianism, iHinduism, iBuddhism, iTaoism, iConfucianism), # Catholicism
(iIslam, iCatholicism, iOrthodoxy, iJudaism, iZoroastrianism, iHinduism, iBuddhism, iTaoism, iConfucianism), # Protestantism
(iHinduism, iProtestantism, iCatholicism, iOrthodoxy, iJudaism, iTaoism, iConfucianism, iZoroastrianism, iBuddhism), # Islam
(iIslam, iCatholicism, iProtestantism, iOrthodoxy, iJudaism, iZoroastrianism, iTaoism, iConfucianism, iBuddhism), # Hinduism
(iCatholicism, iProtestantism, iOrthodoxy, iJudaism, iZoroastrianism, iTaoism, iIslam, iConfucianism, iHinduism), # Buddhism
(iIslam, iCatholicism, iProtestantism, iOrthodoxy, iJudaism, iZoroastrianism, iHinduism, iBuddhism, iTaoism), # Confucianism
(iIslam, iCatholicism, iProtestantism, iOrthodoxy, iJudaism, iZoroastrianism, iHinduism, iBuddhism, iConfucianism), # Taoism
(iIslam, iCatholicism, iProtestantism, iOrthodoxy, iJudaism, iBuddhism, iHinduism, iTaoism, iConfucianism), # Zoroastrianism
)

lCatholicStart = [iSpain, iFrance, iEngland, iHolyRome, iPoland, iPortugal, iItaly, iNetherlands, iGermany, iAmerica, iArgentina, iBrazil, iCanada]
lProtestantStart = [iNetherlands, iGermany, iAmerica]

# corporations
iNumCorporations = 9
(iSilkRoute, iTradingCompany, iCerealIndustry, iFishingIndustry, iTextileIndustry, iSteelIndustry, iOilIndustry, iLuxuryIndustry, iComputerIndustry) = range(iNumCorporations)

# initialise tech variables to unit indices from XML

iNumTechs = 141
(iTanning, iMining, iPottery, iPastoralism, iAgriculture, iMythology, iSailing,
iSmelting, iMasonry, iLeverage, iProperty, iCeremony, iDivination, iSeafaring,
iAlloys, iConstruction, iRiding, iArithmetics, iWriting, iCalendar, iShipbuilding,
iBloomery, iCement, iMathematics, iContract, iLiterature, iPriesthood, iNavigation,
iGeneralship, iEngineering, iAesthetics, iCurrency, iLaw, iPhilosophy, iMedicine,
iNobility, iSteel, iArchitecture, iArtisanry, iPolitics, iScholarship, iEthics,
iFeudalism, iFortification, iMachinery, iAlchemy, iGuilds, iCivilService, iTheology,
iCommune, iCropRotation, iPaper, iCompass, iPatronage, iEducation, iDoctrine,
iGunpowder, iCompanies, iFinance, iCartography, iHumanities, iPrinting, iJudiciary,
iFirearms, iLogistics, iExploration, iOptics, iAcademia, iStatecraft, iHeritage,
iCombinedArms, iEconomics, iGeography, iScientificMethod, iUrbanPlanning, iCivilLiberties, iHorticulture,
iReplaceableParts, iHydraulics, iPhysics, iGeology, iMeasurement, iSociology, iSocialContract,
iMachineTools, iThermodynamics, iMetallurgy, iChemistry, iBiology, iRepresentation, iNationalism,
iBallistics, iEngine, iRailroad, iElectricity, iRefrigeration, iLabourUnions, iJournalism,
iPneumatics, iAssemblyLine, iRefining, iFilm, iMicrobiology, iConsumerism, iCivilRights,
iInfrastructure, iFlight, iSynthetics, iRadio, iPsychology, iMacroeconomics, iSocialServices,
iAviation, iRocketry, iFission, iElectronics, iTelevision, iPowerProjection, iGlobalism,
iRadar, iSpaceflight, iNuclearPower, iLaser, iComputers, iTourism, iEcology,
iAerodynamics, iSatellites, iSuperconductors, iRobotics, iTelecommunications, iRenewableEnergy, iGenetics,
iSupermaterials, iFusion, iNanotechnology, iAutomation, iBiotechnology,
iUnifiedTheory, iArtificialIntelligence,
iTranshumanism) = range(iNumTechs)

# initialise unit variables to unit indices from XML

iNumUnits = 209
(iLion, iBear, iPanther, iWolf, iSettler, iCityBuilder, iPioneer, iWorker, iPunjabiWorker, iLabourer, 
iMadeireiro, iScout, iExplorer, iBandeirante, iSpy, iReligiousPersecutor, iJewishMissionary, iOrthodoxMissionary, iCatholicMissionary, iProtestantMissionary, 
iIslamicMissionary, iHinduMissionary, iBuddhistMissionary, iConfucianMissionary, iTaoistMissionary, iZoroastrianMissionary, iWarrior, iMilitia, iAxeman, iLightSwordsman, 
iVulture, iDogSoldier, iSwordsman, iJaguar, iLegion, iGallicWarrior, iAucac, iShotelai, iHeavySwordsman, iSamurai, 
iHuscarl, iGhazi, iPombos, iSpearman, iHoplite, iSacredBand, iImmortal, iImpi, iHeavySpearman, iPikeman, 
iLandsknecht, iArquebusier, iFirelancer, iTercio, iStrelets, iJanissary, iOromoWarrior, iQizilbash, iMohawk, iMusketeer, 
iRedcoat, iFusilier, iMinuteman, iRifleman, iMehalSefari, iGrenadier, iRocketeer, iGrenzer, iAlbionLegion, iAntiTank, 
iInfantry, iSamInfantry, iMobileSam, iMarine, iNavySeal, iParatrooper, iMechanizedInfantry, iArcher, iAsharittuBowman, iMedjay, 
iSkirmisher, iHolkan, iKelebolo, iLongbowman, iPatiyodha, iCrossbowman, iChokonu, iBalestriere, iChariot, iWarChariot, 
iHuluganni, iCidainh, iHorseman, iCompanion, iNumidianCavalry, iAsvaka, iCamelRider, iHorseArcher, iMangudai, iKhampa, 
iOghuz, iCamelArcher, iLancer, iVaru, iSavaran, iMobileGuard, iKeshik, iCataphract, iChangSuek, iFarari, 
iPistolier, iMountedBrave, iCamelGunner, iCuirassier, iGendarme, iConquistador, iWingedHussar, iHussar, iCossack, iLlanero, 
iDragoon, iGuard, iGrenadierCavalry, iCavalry, iRural, iWarElephant, iBallistaElephant, iTank, iPanzer, iMainBattleTank, 
iGunship, iCatapult, iBallista, iTrebuchet, iBombard, iHwacha, iSiegeElephant, iGreatBombard,iCannon, iArtillery, 
iMachineGun, iHowitzer, iMobileArtillery, iWorkboat, iGalley, iWaka, iBireme, iWarGalley, iHeavyGalley, iDromon, 
iLongship, iCog, iDharani, iGalleass, iDjong, iKobukson, iLanternas, iCaravel, iCarrack, iGalleon, 
iEastIndiaman, iPrivateer, iCorsair, iFrigate, iShipOfTheLine, iManOfWar, iSteamship, iIronclad, iTorpedoBoat, iCruiser, 
iTransport, iDestroyer, iCorvette, iBattleship, iMissileCruiser, iStealthDestroyer, iSubmarine, iNuclearSubmarine, iCarrier, iBiplane, 
iFighter, iZero, iJetFighter, iBomber, iStealthBomber, iGuidedMissile, iDrone, iNuclearBomber, iICBM, iSatellite, 
iGreatProphet, iGreatArtist, iGreatScientist, iGreatMerchant, iGreatEngineer, iGreatStatesman, iGreatGeneral, iArgentineGreatGeneral, iGreatSpy, iFemaleGreatProphet, 
iFemaleGreatArtist, iFemaleGreatScientist, iFemaleGreatMerchant, iFemaleGreatEngineer, iFemaleGreatStatesman, iFemaleGreatGeneral, iFemaleGreatSpy, iSlave, iAztecSlave) = range(iNumUnits)

iMissionary = iJewishMissionary # generic

lGreatPeopleUnits = [iGreatProphet, iGreatArtist, iGreatScientist, iGreatMerchant, iGreatEngineer, iGreatStatesman]

dFemaleGreatPeople = {
iGreatProphet : iFemaleGreatProphet,
iGreatArtist : iFemaleGreatArtist,
iGreatScientist : iFemaleGreatScientist,
iGreatMerchant : iFemaleGreatMerchant,
iGreatEngineer : iFemaleGreatEngineer,
iGreatStatesman : iFemaleGreatStatesman,
iGreatGeneral : iFemaleGreatGeneral,
iGreatSpy : iFemaleGreatSpy,
}

# initialise bonuses variables to bonuses IDs from WBS
iNumBonuses = 41
(iAluminium, iCamel, iCoal, iCopper, iHorse, iIron, iMarble, iOil, iStone, iUranium, iBanana, iClam, iCorn, iCow, iCrab,
iDeer, iFish, iPig, iRice, iSheep, iWheat, iCoffee, iCotton, iDye, iFur, iGems, iGold, iIncense, iIvory, iPearls, iSilk, iSilver, iSpices,
iSugar, iTea, iTobacco, iWine, iWhales, iSoccer, iSongs, iMovies) = range(iNumBonuses)
# Buildings

iNumBuildings = 318
(iPalace, iBarracks, iIkhanda, iGranary, iTerrace, iSmokehouse, iPaganTemple, iMonument, iObelisk, iStele,
iCandi, iEdict, iMalae, iTotemPole, iWalls, iDun, iStable, iGer, iLibrary, iEdubba,
iTaixue, iHoTrai, iSangam, iHarbor, iAqueduct, iBaray, iNoria, iStepwell, iTheatre, iOdeon,
iHippodrome, iPavilion, iArena, iBallCourt, iCharreadaArena, iGarden, iLighthouse, iTradingPost, iWeaver, iMbwadi,
iMarket, iForum, iGlassmaker, iJail, iSacrificialAltar, iDivan, iBath, iReservoir, iHammam, iForge, 
iMint, iArtStudio, iCastle, iCitadel, iPharmacy, iApothecary, iAlchemist, iPostOffice, iTambo, iCaravanserai,
iWharf, iCoffeehouse, iSalon, iBank, iRoyalExchange, iConstabulary, iMountedPolice, iCustomsHouse, iFeitoria, iUniversity,
iSeowon, iGompa, iCivicSquare, iRathaus, iSejmik, iSewer, iStarFort, iEstate, iMausoleum, iFazenda, 
iHacienda, iDrydock, iLevee, iDike, iObservatory, iWarehouse, iCourthouse, iFactory, iAssemblyPlant, iZaibatsu, 
iDistillery, iPark, iCoalPlant, iRailwayStation, iLaboratory, iResearchInstitute, iNewsPress, iIndustrialPark, iCinema, iHospital, 
iSupermarket, iColdStoragePlant, iPublicTransportation, iDepartmentStore, iMall, iBroadcastTower, iIntelligenceAgency, iElectricalGrid, iAirport, iBunker, 
iBombShelters, iHydroPlant, iSecurityBureau, iStadium, iContainerTerminal, iNuclearPlant, iSupercomputer, iHotel, iRecyclingCenter, iLogisticsCenter, 
iSolarPlant, iFiberNetwork, iAutomatedFactory, iVerticalFarm, iJewishTemple, iJewishCathedral, iJewishMonastery, iJewishShrine, iOrthodoxTemple, iOrthodoxCathedral, 
iOrthodoxMonastery, iOrthodoxShrine, iCatholicChurch, iCatholicCathedral, iCatholicMonastery, iCatholicShrine, iProtestantTemple, iProtestantCathedral, iProtestantMonastery, iProtestantShrine, 
iIslamicTemple, iIslamicCathedral, iIslamicMonastery, iIslamicShrine, iHinduTemple, iHinduCathedral, iHinduMonastery, iHinduShrine, iBuddhistTemple, iBuddhistCathedral, 
iBuddhistMonastery, iBuddhistShrine, iConfucianTemple, iConfucianCathedral, iConfucianMonastery, iConfucianShrine, iTaoistTemple, iTaoistCathedral, iTaoistMonastery, iTaoistShrine, 
iZoroastrianTemple, iZoroastrianCathedral, iZoroastrianMonastery, iZoroastrianShrine, iAcademy, iAdministrativeCenter, iManufactory, iArmoury, iMuseum, iStockExchange, 
iTradingCompanyBuilding, iIberianTradingCompanyBuilding, iNationalMonument, iNationalTheatre, iNationalGallery, iNationalCollege, iMilitaryAcademy, iSecretService, iIronworks, iRedCross, 
iNationalPark, iCentralBank, iSpaceport, iGreatSphinx, iPyramids, iOracle, iGreatWall, iIshtarGate, iTerracottaArmy, iHangingGardens, 
iGreatCothon, iDujiangyan, iApadanaPalace, iColossus, iStatueOfZeus, iGreatMausoleum, iParthenon, iTempleOfArtemis, iGreatLighthouse, iMoaiStatues, 
iFlavianAmphitheatre, iAquaAppia, iAlKhazneh, iTempleOfKukulkan, iMachuPicchu, iGreatLibrary, iFloatingGardens, iGondeshapur, iJetavanaramaya, iNalanda, 
iTheodosianWalls, iHagiaSophia, iBorobudur, iMezquita, iShwedagonPaya, iMountAthos, iIronPillar, iPrambanan, iSalsalBuddha, iCheomseongdae, 
iHimejiCastle, iGrandCanal, iWatPreahPisnulok, iKhajuraho, iSpiralMinaret, iDomeOfTheRock, iHouseOfWisdom, iKrakDesChevaliers, iMonolithicChurch, iUniversityOfSankore, 
iNotreDame, iOldSynagogue, iSaintSophia, iSilverTreeFountain, iSantaMariaDelFiore, iAlamut, iSanMarcoBasilica, iSistineChapel, iPorcelainTower, iTopkapiPalace, 
iKremlin, iSaintThomasChurch, iVijayaStambha, iGurEAmir, iRedFort, iTajMahal, iForbiddenPalace, iVersailles, iBlueMosque, iEscorial, 
iTorreDeBelem, iPotalaPalace, iOxfordUniversity, iHarmandirSahib, iSaintBasilsCathedral, iBourse, iItsukushimaShrine, iImageOfTheWorldSquare, iLouvre, iEmeraldBuddha, 
iShalimarGardens, iTrafalgarSquare, iHermitage, iGuadalupeBasilica, iSaltCathedral, iAmberRoom, iStatueOfLiberty, iBrandenburgGate, iAbbeyMills, iBellRockLighthouse, 
iChapultepecCastle, iEiffelTower, iWestminsterPalace, iTriumphalArch, iMenloPark, iCrystalPalace, iTsukijiFishMarket, iBrooklynBridge, iHollywood, iEmpireStateBuilding, 
iLasLajasSanctuary, iPalaceOfNations, iMoleAntonelliana, iNeuschwanstein, iFrontenac, iWembley, iLubyanka, iCristoRedentor, iMetropolitain, iNobelPrize, 
iGoldenGateBridge, iBletchleyPark, iSagradaFamilia, iCERN, iItaipuDam, iGraceland, iCNTower, iPentagon, iUnitedNations, iCrystalCathedral, 
iMotherlandCalls, iBerlaymont, iWorldTradeCenter, iAtomium, iIronDome, iHarbourOpera, iLotusTemple, iGlobalSeedVault, iGardensByTheBay, iBurjKhalifa, 
iHubbleSpaceTelescope, iChannelTunnel, iSkytree, iOrientalPearlTower, iDeltaWorks, iSpaceElevator, iLargeHadronCollider, iITER) = range(iNumBuildings)

iBeginWonders = iGreatSphinx # different from DLL constant because that includes national wonders

iTemple = iJewishTemple #generic
iCathedral = iJewishCathedral #generic
iMonastery = iJewishMonastery #generic
iShrine = iJewishShrine #generic

iFirstWonder = iGreatSphinx

iPlague = iNumBuildings
iNumBuildingsPlague = iNumBuildings+1

#Civics
iNumCivics = 42
(iChiefdom, iDespotism, iMonarchy, iRepublic, iElective, iStateParty, iDemocracy,
iAuthority, iCitizenship, iVassalage, iMeritocracy, iCentralism, iRevolutionism, iConstitution,
iTraditionalism, iSlavery, iManorialism, iCasteSystem, iIndividualism, iTotalitarianism, iEgalitarianism,
iReciprocity, iRedistribution, iMerchantTrade, iRegulatedTrade, iFreeEnterprise, iCentralPlanning, iPublicWelfare,
iAnimism, iDeification, iClergy, iMonasticism, iTheocracy, iTolerance, iSecularism,
iSovereignty, iConquest, iTributaries, iIsolationism, iColonialism, iNationhood, iMultilateralism) = range(iNumCivics)

iNumCivicCategories = 6
(iCivicsGovernment, iCivicsLegitimacy, iCivicsSociety, iCivicsEconomy, iCivicsReligion, iCivicsTerritory) = range(iNumCivicCategories)

#Specialists
iNumSpecialists = 19
(iSpecialistCitizen, iSpecialistPriest, iSpecialistArtist, iSpecialistScientist, iSpecialistMerchant, iSpecialistEngineer, iSpecialistStatesman,
iSpecialistGreatProphet, iSpecialistGreatArtist, iSpecialistGreatScientist, iSpecialistGreatMerchant, iSpecialistGreatEngineer, iSpecialistGreatStatesman, iSpecialistGreatGeneral, iSpecialistGreatSpy, 
iSpecialistResearchSatellite, iSpecialistCommercialSatellite, iSpecialistMilitarySatellite, 
iSpecialistSlave) = range(iNumSpecialists)

#Stability Levels
iNumStabilityLevels = 5
(iStabilityCollapsing, iStabilityUnstable, iStabilityShaky, iStabilityStable, iStabilitySolid) = range(iNumStabilityLevels)
StabilityLevelTexts = ["TXT_KEY_STABILITY_COLLAPSING", "TXT_KEY_STABILITY_UNSTABLE", "TXT_KEY_STABILITY_SHAKY", "TXT_KEY_STABILITY_STABLE", "TXT_KEY_STABILITY_SOLID"]

#Stability Types
iNumStabilityTypes = 5
(iStabilityExpansion, iStabilityEconomy, iStabilityDomestic, iStabilityForeign, iStabilityMilitary) = range(iNumStabilityTypes)
StabilityTypesTexts = ["TXT_KEY_STABILITY_CATEGORY_EXPANSION", "TXT_KEY_STABILITY_CATEGORY_ECONOMY", "TXT_KEY_STABILITY_CATEGORY_DOMESTIC", "TXT_KEY_STABILITY_CATEGORY_FOREIGN", "TXT_KEY_STABILITY_CATEGORY_MILITARY"]

#Stability Parameters
iNumStabilityParameters = 23
(iParameterCorePeriphery, iParameterCoreScore, iParameterPeripheryScore, iParameterRecentExpansion, iParameterRazedCities, iParameterIsolationism,	# Expansion
iParameterEconomicGrowth, iParameterTrade, iParameterMercantilism, iParameterCentralPlanning,								# Economy
iParameterHappiness, iParameterCivicCombinations, iParameterCivicsEraTech, iParameterReligion,								# Domestic
iParameterVassals, iParameterDefensivePacts, iParameterRelations, iParameterNationhood, iParameterTheocracy, iParameterMultilateralism,			# Foreign
iParameterWarSuccess, iParameterWarWeariness, iParameterBarbarianLosses) = range(iNumStabilityParameters)						# Military

#Regions
iNumRegions = 38
(rBritain, rIberia, rItaly, rBalkans, rEurope, rScandinavia, rRussia, rAnatolia, rMesopotamia, rArabia, rEgypt, rMaghreb,
rPersia, rIndia, rDeccan, rIndochina, rIndonesia, rChina, rKorea, rJapan, rManchuria, rTibet, rCentralAsia, rSiberia,
rAustralia, rOceania, rEthiopia, rWestAfrica, rSouthAfrica, rCanada, rAlaska, rUnitedStates, rCaribbean, rMesoamerica,
rBrazil, rArgentina, rPeru, rColombia) = range(iNumRegions)

lNewWorld = [rAustralia, rOceania, rCanada, rAlaska, rUnitedStates, rCaribbean, rMesoamerica, rBrazil, rArgentina, rPeru, rColombia]

lEurope = [rBritain, rIberia, rItaly, rBalkans, rEurope, rScandinavia, rRussia]
lMiddleEast = [rAnatolia, rMesopotamia, rArabia, rPersia, rCentralAsia]
lIndia = [rIndia, rDeccan]
lEastAsia = [rIndochina, rIndonesia, rChina, rKorea, rJapan, rManchuria, rTibet]
lNorthAfrica = [rEgypt, rMaghreb]
lSubSaharanAfrica = [rEthiopia, rSouthAfrica, rWestAfrica]
lSouthAmerica = [rCaribbean, rMesoamerica, rBrazil, rArgentina, rPeru, rColombia]
lNorthAmerica = [rCanada, rAlaska, rUnitedStates]
lOceania = [rAustralia, rOceania]

lAfrica = lNorthAfrica + lSubSaharanAfrica
lAsia = lMiddleEast + lIndia + lEastAsia

#Projects

iNumProjects = 21
(iManhattanProject, iTheInternet, iHumanGenome, iSDI, iGPS, iISS, iBallisticMissile, iFirstSatellite, iManInSpace, iLunarLanding,
iGoldenRecord, iMarsMission, iLunarColony, iInterstellarProbe, iMarsFraming, iMarsPowerSource, iMarsExtractor, iMarsHabitat, iMarsHydroponics, iMarsLaboratory, iMarsControlCenter) = range(iNumProjects)

lMarsBaseComponents = [iMarsFraming, iMarsPowerSource, iMarsExtractor, iMarsHabitat, iMarsHydroponics, iMarsLaboratory, iMarsControlCenter]

#Eras

iNumEras = 7
(iAncient, iClassical, iMedieval, iRenaissance, iIndustrial, iGlobal, iDigital) = range (iNumEras)


#Improvements

iNumImprovements = 30
(iLandWorked, iWaterWorked, iCityRuins, iHut, iFarm, iPaddyField, iFishingBoats, iOceanFishery, iWhalingBoats, iMine, 
iWorkshop, iLumbermill, iWindmill, iWatermill, iPlantation, iSlavePlantation, iQuarry, iPasture, iCamp, iWell, 
iOffshorePlatform, iWinery, iCottage, iHamlet, iVillage, iTown, iFort, iForestPreserve, iMarinePreserve, iSolarCollector) = range(iNumImprovements)

iNumRoutes = 4
(iRouteRoad, iRouteRailroad, iRouteRomanRoad, iRouteHighway) = range(iNumRoutes)

#feature & terrain

iNumFeatures = 10
(iSeaIce, iJungle, iOasis, iFloodPlains, iForest, iMud, iCape, iIslands, iRainforest, iFallout) = range(iNumFeatures)

iGrass = 0
iPlains = 1
iDesert = 2
iTundra = 3
iSnow = 4
iCoast = 5
iOcean = 6
iTerrainPeak = 7
iTerrainHills = 8
iMarsh = 9

#Plague
iImmunity = 20

# Victory
iVictoryPaganism = 10
iVictorySecularism = 11


#leaders
iNumLeaders = 125
(iLeaderBarbarian, iNativeLeader, iIndependentLeader, iAlexanderTheGreat, iAsoka, iAugustus, iBismarck, iBoudica, iBrennus, iCatherine, 
iCharlemagne, iChurchill, iCyrus, iDarius, iDeGaulle, iElizabeth, iFrederick, iGandhi, iGenghisKhan, iSargon, 
iHammurabi, iHannibal, iCleopatra, iHuaynaCapac, iIsabella, iJoao, iJuliusCaesar, iJustinian, iKublaiKhan, iLincoln, 
iLouis, iMansaMusa, iMao, iMehmed, iMontezuma, iNapoleon, iPacal, iPericles, iPeter, iQinShiHuang, 
iRamesses, iRagnar, iRoosevelt, iSaladin, iSittingBull, iStalin, iSuleiman, iSuryavarman, iOdaNobunaga, iVictoria, 
iWangKon, iWashington, iWillemVanOranje, iZaraYaqob, iKammu, iMeiji, iAkbar, iHiram, iMenelik, iGustav, 
iMongkut, iPhilip, iBarbarossa, iCharles, iFrancis, iIvan, iAfonso, iAtaturk, iMaria, iHitler,
iFranco, iAlexanderII, iCavour, iAbbas, iKhomeini, iTaizong, iHongwu, iDharmasetu, iHayamWuruk, iSuharto, 
iShahuji, iNaresuan, iAlpArslan, iBaibars, iNasser, iAlfred, iTrudeau, iChandragupta, iTughluq, iBasil, 
iRahman, iRajendra, iLobsangGyatso, iSobieski, iVatavelli, iMbemba, iHarun, iSongtsen, iCasimir, iYaqub, 
iLorenzo, iSantaAnna, iJuarez, iCardenas, iPedro, iSanMartin, iPeron, iBolivar, iAhoeitu, iKrishnaDevaRaya, 
iMussolini, iSejong, iBhutto, iPilsudski, iWalesa, iGerhardsen, iVargas, iMacDonald, iCastilla, iWilliam,
iGeorge, iKhosrow, iBumin, iTamerlane, iEzana) = range(iNumLeaders)

dResurrectionLeaders = {
	iCivChina : iHongwu,
	iCivIndia : iShahuji,
	iCivEgypt : iBaibars,
}

dRebirthLeaders = {
	iCivColombia : iBolivar,
	iCivIran : iAbbas,
	iCivMexico : iJuarez,
}

iNumPeriods = 19
(iPeriodMing, iPeriodMaratha, iPeriodModernGreece, iPeriodCarthage, iPeriodVijayanagara,
iPeriodByzantineConstantinople, iPeriodSeljuks, iPeriodMeiji, iPeriodSaudi, iPeriodVietnam,
iPeriodMorocco, iPeriodSpain, iPeriodAustria, iPeriodYuan, iPeriodPeru,
iPeriodModernItaly, iPeriodPakistan, iPeriodOttomanConstantinople, iPeriodModernGermany) = range(iNumPeriods)

tTradingCompanyPlotLists = (
[(109, 33)], #Spain
[(101, 37), (101, 36), (102, 36), (102, 35), (103, 35), (103, 34), (104, 34), (104, 33)], #France
[(95, 37), (94, 37), (94, 36), (94, 35), (94, 34), (93, 34), (93, 33), (92, 33), (92, 32), (88, 33), (88, 34), (88, 35)], #England
[(82, 34), (89, 31), (101, 29), (105, 39), (93, 28), (93, 27), (71, 17), (69, 13), (54, 26), (62, 20)], #Portugal
[(99, 28), (99, 27), (100, 27), (100, 26), (101, 26), (104, 25), (105, 25), (106, 25), (107, 24), (104, 27), (105, 27), (106, 27), (104, 28), (106, 28), (105, 29), (106, 29)] #Netherlands
)

lSecondaryCivs = [iCivHarappa, iCivPolynesia, iCivTamils, iCivTibet, iCivMoors, iCivPoland, iCivCongo, iCivArgentina, iCivBrazil]

lMongolCivs = [iCivPersia, iCivByzantium, iCivArabia, iCivRussia, iCivMughals]

(i3000BC, i600AD, i1700AD) = range(3)

# Stability overlay and editor
iNumPlotStabilityTypes = 5
(iCore, iHistorical, iContest, iForeignCore, iAIForbidden) = range(iNumPlotStabilityTypes)
lStabilityColors = ["COLOR_CYAN", "COLOR_GREEN", "COLOR_YELLOW", "COLOR_RED", "COLOR_PLAYER_LIGHT_PURPLE"]
lPresetValues = [3, 20, 90, 200, 500, 700]

iMaxWarValue = 12
lWarMapColors = ["COLOR_RED", "COLOR_PLAYER_ORANGE", "COLOR_YELLOW", "COLOR_GREEN", "COLOR_PLAYER_DARK_GREEN", "COLOR_BLUE"]

lReligionMapColors = ["COLOR_PLAYER_ORANGE", "COLOR_YELLOW", "COLOR_GREEN", "COLOR_CYAN"]
lReligionMapTexts = ["TXT_KEY_CULTURELEVEL_NONE", "TXT_KEY_WB_RELIGIONMAP_MINORITY", "TXT_KEY_WB_RELIGIONMAP_PERIPHERY", "TXT_KEY_WB_RELIGIONMAP_HISTORICAL", "TXT_KEY_WB_RELIGIONMAP_CORE"]

lNetworkEvents = {
	"CHANGE_COMMERCE_PERCENT" :	1200,
}