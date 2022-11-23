# Rhye's and Fall of Civilization - Constants
# globals

from CvPythonExtensions import *
from DataStructures import *
from CoreTypes import *

gc = CyGlobalContext()

iWorldX = 124
iWorldY = 68

iNumPlayers = gc.getMAX_PLAYERS()

# civilizations, not players
iNumCivs = 57
(iAmerica, iArabia, iArgentina, iAztecs, iBabylonia, iBrazil, iByzantium, iCanada, iCarthage, iCelts, 
iChina, iColombia, iEgypt, iEngland, iEthiopia, iFrance, iGermany, iGreece, iHarappa, iHolyRome, 
iInca, iIndia, iIndonesia, iIran, iItaly, iJapan, iKhmer, iCongo, iKorea, iMali, 
iMaya, iMexico, iMongols, iMoors, iMughals, iNativeAmericans, iNetherlands, iOttomans, iPersia, iPoland, 
iPolynesia, iPortugal, iRome, iRussia, iSpain, iSumeria, iTamils, iThailand, iTibet, iTurks,
iVikings, iZulu, iIndependent, iIndependent2, iNative, iMinor, iBarbarian) = tuple(Civ(i) for i in range(iNumCivs))

iPhoenicia = iCarthage

lBirthOrder = [
	iEgypt,
	iBabylonia,
	iHarappa,
	iChina,
	iGreece,
	iIndia,
	iCarthage,
	iPolynesia,
	iPersia,
	iRome,
	iMaya,
	iTamils,
	iEthiopia,
	iKorea,
	iByzantium,
	iJapan,
	iVikings,
	iTurks,
	iArabia,
	iTibet,
	iIndonesia,
	iMoors,
	iSpain,
	iFrance,
	iKhmer,
	iEngland,
	iHolyRome,
	iRussia,
	iMali,
	iPoland,
	iPortugal,
	iInca,
	iItaly,
	iMongols,
	iAztecs,
	iMughals,
	iOttomans,
	iThailand,
	iCongo,
	iIran,
	iNetherlands,
	iGermany,
	iAmerica,
	iArgentina,
	iMexico,
	iColombia,
	iBrazil,
	iCanada
]

lCivOrder = lBirthOrder + [
	iIndependent,
	iIndependent2,
	iNative,
	iCelts,
	iBarbarian
]

# used in: Congresses, DynamicCivs, Plague, RFCUtils, UniquePowers, Victory
# a civilisation can be in multiple civ groups
iNumCivGroups = 6
(iCivGroupEurope, iCivGroupAsia, iCivGroupMiddleEast, iCivGroupMediterranean, iCivGroupAfrica, iCivGroupAmerica) = range(iNumCivGroups)

dCivGroups = {
iCivGroupEurope : [iGreece, iRome, iByzantium, iVikings, iSpain, iFrance, iEngland, iHolyRome, iRussia, iNetherlands, iItaly, iPoland, iPortugal, iGermany],
iCivGroupAsia : [iIndia, iChina, iHarappa, iPolynesia, iPersia, iJapan, iTamils, iKorea, iByzantium, iTibet, iKhmer, iIndonesia, iRussia, iMongols, iMughals, iThailand, iTurks],
iCivGroupMiddleEast : [iEgypt, iBabylonia, iPersia, iByzantium, iArabia, iMoors, iOttomans, iCarthage, iTurks, iIran],
iCivGroupAfrica : [iEgypt, iCarthage, iEthiopia, iMali, iCongo],
iCivGroupAmerica : [iMaya, iInca, iAztecs, iAmerica, iArgentina, iMexico, iColombia, iBrazil, iCanada],
}

# used in: Stability
# tech groups share techs within each other on respawn
iNumTechGroups = 4
(iTechGroupWestern, iTechGroupMiddleEast, iTechGroupFarEast, iTechGroupNativeAmerica) = range(iNumTechGroups)

dTechGroups = {
iTechGroupWestern : [iRome, iGreece, iByzantium, iVikings, iSpain, iFrance, iEngland, iHolyRome, iRussia, iNetherlands, iPoland, iPortugal, iItaly, iGermany, iAmerica, iArgentina, iMexico, iColombia, iBrazil, iCanada],
iTechGroupMiddleEast : [iEgypt, iBabylonia, iHarappa, iIndia, iCarthage, iPersia, iEthiopia, iArabia, iMoors, iMali, iOttomans, iMughals, iTamils, iCongo, iTurks, iIran],
iTechGroupFarEast : [iChina, iKorea, iJapan, iTibet, iKhmer, iIndonesia, iMongols, iThailand],
iTechGroupNativeAmerica : [iPolynesia, iMaya, iInca, iAztecs],
}

lBioNewWorld = [iMaya, iInca, iAztecs]

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

lNeighbours = [
	(iEgypt, iBabylonia),
	(iEgypt, iGreece),
	(iEgypt, iPersia),
	(iEgypt, iCarthage),
	(iEgypt, iRome),
	(iEgypt, iEthiopia),
	(iEgypt, iByzantium),
	(iEgypt, iArabia),
	(iEgypt, iMoors),
	(iEgypt, iOttomans),
	(iBabylonia, iGreece),
	(iBabylonia, iPersia),
	(iBabylonia, iTurks),
	(iBabylonia, iOttomans),
	(iBabylonia, iMongols),
	(iBabylonia, iCarthage),
	(iBabylonia, iByzantium),
	(iBabylonia, iIran),
	(iHarappa, iIndia),
	(iHarappa, iPersia),
	(iHarappa, iTamils),
	(iHarappa, iTibet),
	(iHarappa, iMughals),
	(iHarappa, iIran),
	(iChina, iJapan),
	(iChina, iKorea),
	(iChina, iTurks),
	(iChina, iTibet),
	(iChina, iMongols),
	(iGreece, iPersia),
	(iGreece, iCarthage),
	(iGreece, iRome),
	(iGreece, iByzantium),
	(iGreece, iOttomans),
	(iGreece, iItaly),
	(iIndia, iPersia),
	(iIndia, iTamils),
	(iIndia, iTibet),
	(iIndia, iKhmer),
	(iIndia, iIndonesia),
	(iIndia, iMughals),
	(iIndia, iIran),
	(iCarthage, iRome),
	(iCarthage, iSpain),
	(iCarthage, iMali),
	(iCarthage, iPersia),
	(iCarthage, iArabia),
	(iCarthage, iMoors),
	(iCarthage, iOttomans),
	(iCarthage, iItaly),
	(iPersia, iTurks),
	(iPersia, iByzantium),
	(iPersia, iOttomans),
	(iPersia, iMongols),
	(iPersia, iRome),
	(iPersia, iMughals),
	(iPersia, iIran),
	(iRome, iSpain),
	(iRome, iByzantium),
	(iRome, iFrance),
	(iRome, iHolyRome),
	(iRome, iItaly),
	(iRome, iGermany),
	(iRome, iMoors),
	(iTamils, iKhmer),
	(iTamils, iIndonesia),
	(iTamils, iMughals),
	(iEthiopia, iArabia),
	(iKorea, iMongols),
	(iKorea, iJapan),
	(iMaya, iAztecs),
	(iMaya, iMexico),
	(iMaya, iColombia),
	(iByzantium, iArabia),
	(iByzantium, iRussia),
	(iByzantium, iTurks),
	(iByzantium, iOttomans),
	(iByzantium, iMongols),
	(iByzantium, iIran),
	(iJapan, iMongols),
	(iVikings, iFrance),
	(iVikings, iEngland),
	(iVikings, iHolyRome),
	(iVikings, iRussia),
	(iVikings, iPoland),
	(iVikings, iNetherlands),
	(iVikings, iGermany),
	(iTurks, iMughals),
	(iTurks, iOttomans),
	(iTurks, iMongols),
	(iTurks, iIran),
	(iTurks, iTibet),
	(iTurks, iArabia),
	(iArabia, iMoors),
	(iArabia, iMongols),
	(iArabia, iOttomans),
	(iArabia, iIran),
	(iTibet, iMongols),
	(iTibet, iMughals),
	(iIndonesia, iKhmer),
	(iIndonesia, iThailand),
	(iMoors, iSpain),
	(iMoors, iPortugal),
	(iMoors, iMali),
	(iSpain, iFrance),
	(iSpain, iPortugal),
	(iSpain, iItaly),
	(iFrance, iEngland),
	(iFrance, iHolyRome),
	(iFrance, iNetherlands),
	(iFrance, iItaly),
	(iFrance, iGermany),
	(iKhmer, iThailand),
	(iEngland, iNetherlands),
	(iHolyRome, iNetherlands),
	(iHolyRome, iItaly),
	(iHolyRome, iPoland),
	(iHolyRome, iGermany),
	(iRussia, iPoland),
	(iRussia, iOttomans),
	(iRussia, iMongols),
	(iRussia, iGermany),
	(iMali, iCongo),
	(iPoland, iGermany),
	(iInca, iArgentina),
	(iInca, iColombia),
	(iInca, iBrazil),
	(iMongols, iOttomans),
	(iMongols, iIran),
	(iAztecs, iAmerica),
	(iAztecs, iMexico),
	(iAztecs, iColombia),
	(iMughals, iIran),
	(iOttomans, iIran),
	(iAmerica, iMexico),
	(iAmerica, iCanada),
	(iArgentina, iBrazil),
	(iMexico, iColombia),
]

lInfluences = [
	(iEgypt, iEngland),
	(iBabylonia, iRome),
	(iBabylonia, iArabia),
	(iIndia, iEngland),
	(iPhoenicia, iByzantium),
	(iPhoenicia, iTurks),
	(iPhoenicia, iIran),
	(iPersia, iArabia),
	(iRome, iOttomans),
	(iMaya, iSpain),
	(iTamils, iEngland),
	(iTamils, iNetherlands),
	(iArabia, iBabylonia),
	(iArabia, iGreece),
	(iArabia, iPersia),
	(iIndonesia, iJapan),
	(iSpain, iArabia),
	(iSpain, iOttomans),
	(iKhmer, iJapan),
	(iHolyRome, iOttomans),
	(iInca, iSpain),
	(iItaly, iOttomans),
	(iAztecs, iSpain),
	(iMughals, iEngland),
	(iOttomans, iRome),
	(iThailand, iJapan),
	(iCongo, iPortugal),
	(iNetherlands, iSpain),
	(iAmerica, iEngland),
	(iAmerica, iFrance),
	(iAmerica, iNetherlands),
	(iArgentina, iSpain),
	(iMexico, iSpain),
	(iMexico, iFrance),
	(iColombia, iSpain),
	(iBrazil, iPortugal),
	(iBrazil, iCongo),
	(iCanada, iFrance),
	(iCanada, iEngland),
]

dBirth = CivDict({
iEgypt : -3000,
iBabylonia : -3000,
iHarappa : -3000,
iChina : -2070,
iGreece : -1600,
iIndia : -1500,
iPhoenicia : -1200,
iPolynesia : -1000,
iPersia : -850,
iRome : -753,
iMaya : -400,
iTamils : -300,
iEthiopia : -290,
iKorea : -50,
iByzantium : 330,
iJapan : 525,
iVikings : 551,
iTurks : 552,
iArabia : 620,
iTibet : 630,
iIndonesia : 650,
iMoors : 711,
iSpain : 722,
iFrance : 750,
iKhmer : 800,
iEngland : 820,
iHolyRome : 840,
iRussia : 860,
iMali : 989,
iPoland : 1025,
iPortugal : 1130,
iInca : 1150,
iItaly : 1167,
iMongols : 1190,
iAztecs : 1195,
iMughals : 1206,
iOttomans : 1280,
iThailand : 1350,
iCongo : 1390,
iIran : 1501,
iNetherlands : 1580,
iGermany : 1700,
iAmerica : 1776,
iArgentina : 1810,
iMexico : 1810,
iColombia : 1814,
iBrazil : 1822,
iCanada : 1867,
}, -3000)

lBirthCivs = dBirth.keys()

dFall = CivDict({
iEgypt : -343,
iBabylonia : -539,
iHarappa : -1700,
iChina : 1127,
iGreece : -146,
iIndia : 600,
iPhoenicia : -146,
iPolynesia : 1200,
iPersia : 651,
iRome : 235,
iMaya : 900,
iTamils : 1000,
iEthiopia : 960,
iKorea : 1255,
iByzantium : 1204,
iVikings : 1300,
iTurks : 1507,
iArabia : 900,
iTibet : 1500,
iIndonesia : 1500,
iMoors : 1500,
iKhmer : 1200,
iMali : 1600,
iPoland : 1650,
iInca : 1533,
iMongols : 1368,
iAztecs : 1521,
iMughals : 1640,
iCongo : 1800,
}, 2020)

# Leoreth: determine neighbour lists from pairwise neighbours for easier lookup
dNeighbours = dictFromEdges(lBirthCivs, lNeighbours)

# Leoreth: determine influence lists from pairwise influences for easier lookup
dInfluences = dictFromEdges(lBirthCivs, lInfluences)

dResurrections = CivDict({
iEgypt : [(900, 1300), (1800, 2020)],
iBabylonia : [(-3000, -500)],
iChina : [(600, 2020)],
iGreece : [(1800, 2020)],
iIndia : [(1600, 1800), (1900, 2020)],
iPhoenicia : [(-1000, -150)],
iPersia : [(220, 650)],
iRome : [(-750, 450)],
iMaya : [(0, 800)],
iTamils : [(-300, 600), (1300, 1650)],
iEthiopia : [(1270, 1520), (1850, 2020)],
iKorea : [(1800, 2020)],
iByzantium : [(1100, 1280)],
iJapan : [(1800, 2020)],
iVikings : [(1520, 2020)],
iTurks : [(1350, 1500)],
iArabia : [(1900, 2020)],
iIndonesia : [(1900, 2020)],
iMoors : [(1000, 2020)],
iSpain : [(1700, 2020)],
iFrance : [(1700, 2020)],
iKhmer : [(1950, 2020)],
iEngland : [(1700, 2020)],
iHolyRome : [(1800, 2020)],
iRussia : [(1280, 1550), (1700, 2020)],
iMali : [(1340, 1590)],
iPoland : [(1920, 2020)],
iPortugal : [(1700, 2020)],
iInca : [(1800, 1930)],
iItaly : [(1820, 2020)],
iMongols : [(1910, 2020)],
iMughals : [(1940, 2020)],
iOttomans : [(1700, 2020)],
iThailand : [(1700, 2020)],
iIran : [(1500, 2020)],
iNetherlands : [(1700, 2020)],
iGermany : [(1840, 2020)],
iAmerica : [(1776, 2020)],
iArgentina : [(1810, 2020)],
iMexico : [(1810, 2020)],
iColombia : [(1810, 2020)],
iBrazil : [(1820, 2020)],
iCanada : [(1867, 2020)],
}, [])

dEnemyCivsOnSpawn = CivDict({
iBabylonia : [iIndependent, iIndependent2],
iChina : [iIndependent, iIndependent2, iIndependent2],
iGreece : [iIndependent, iIndependent2, iBabylonia],
iPersia : [iBabylonia, iBabylonia, iGreece, iCarthage, iCarthage],
iByzantium : [iGreece, iPersia],
iVikings : [iEngland, iEngland, iFrance, iIndependent, iIndependent2],
iTurks : [iChina, iChina, iPersia, iPersia, iIndependent, iIndependent, iIndependent2, iIndependent2],
iArabia : [iEgypt, iEgypt, iEgypt, iBabylonia, iBabylonia, iGreece, iPersia, iCarthage, iRome, iByzantium, iByzantium, iSpain, iFrance, iCelts, iCelts, iIndependent, iIndependent2],
iIndonesia : [iKhmer, iKhmer],
iArabia : [iRome, iArabia, iArabia],
iMongols : [iChina, iChina, iChina, iKorea, iKorea, iTurks, iTurks, iTurks, iIndependent, iIndependent, iIndependent2, iIndependent2],
iAztecs : [iMaya],
iMughals : [iIndia, iIndia],
iOttomans : [iEgypt, iEgypt, iBabylonia, iGreece, iGreece, iArabia, iArabia, iArabia, iByzantium, iByzantium, iByzantium],
iThailand : [iKhmer, iKhmer, iKhmer],
iGermany : [iHolyRome, iPoland],
iAmerica : [iIndependent, iIndependent2],
iArgentina : [iSpain, iSpain, iIndependent, iIndependent2],
iMexico : [iSpain, iSpain, iIndependent, iIndependent2],
iColombia : [iSpain, iSpain, iIndependent, iIndependent2],
iBrazil : [iIndependent, iIndependent2],
}, [])

dTotalWarOnSpawn = CivDict({
iPersia : [iBabylonia, iCarthage],
iRome : [iGreece],
iByzantium : [iGreece],
iArabia : [iEgypt, iBabylonia, iCarthage, iPersia],
iSpain : [iMoors],
iHolyRome : [iRome],
iMongols : [iChina],
iAztecs : [iMaya],
iMughals : [iIndia],
iOttomans : [iArabia, iEgypt],
iThailand : [iKhmer],
}, [])

dAggressionLevel = CivDict({
iBabylonia : 1,
iChina : 1,
iGreece : 2,
iPersia : 3,
iRome : 3,
iMaya : 1,
iTamils : 1,
iByzantium : 1,
iJapan : 1,
iVikings : 2,
iTurks : 2,
iArabia : 2,
iTibet : 1,
iIndonesia : 1,
iMoors : 1,
iSpain : 2,
iFrance : 1,
iKhmer : 2,
iEngland : 1,
iHolyRome : 1,
iRussia : 1,
iPoland : 1,
iInca : 1,
iMongols : 3,
iAztecs : 2,
iMughals : 1,
iOttomans : 2,
iIran : 1,
iGermany : 2,
iAmerica : 2,
iColombia : 2,
iMexico : 1,
iArgentina : 1,
}, 0)

dWarOnFlipProbability = CivDict({
iEgypt: 20,
iBabylonia: 50,
iHarappa: 50,
iChina: 40,
iGreece: 50,
iIndia: 20,
iPhoenicia: 20,
iPolynesia: 20,
iPersia: 30,
iRome: 20,
iMaya: 20,
iTamils: 20,
iEthiopia: 20,
iKorea: 20,
iByzantium: 20,
iJapan: 20,
iVikings: 20,
iTurks: 50,
iArabia: 20,
iTibet: 20,
iIndonesia: 20,
iMoors: 20,
iSpain: 20,
iFrance: 20,
iKhmer: 20,
iEngland: 50,
iHolyRome: 20,
iRussia: 50,
iMali: 30,
iPoland: 60,
iPortugal: 60,
iInca: 30,
iItaly: 40,
iMongols: 30,
iAztecs: 50,
iMughals: 30,
iOttomans: 30,
iThailand: 20,
iCongo: 20,
iIran: 20,
iNetherlands: 60,
iGermany: 20,
iAmerica: 50,
iArgentina: 40,
iMexico: 40,
iColombia: 40,
iBrazil: 40,
iCanada: 40,
}, 0)

dResurrectionProbability = CivDict({
iEgypt : 25,
iBabylonia : 40,
iHarappa : 0,
iChina : 100,
iGreece : 60,
iIndia : 50,
iPhoenicia : 30,
iPolynesia : 40,
iPersia : 70,
iRome : 65,
iMaya : 30,
iTamils : 10,
iEthiopia : 80,
iKorea : 80,
iByzantium : 65,
iJapan : 100,
iVikings : 60,
iTurks : 30,
iArabia : 100,
iTibet : 60,
iIndonesia : 80,
iMoors : 70,
iSpain : 100,
iFrance : 100,
iKhmer : 60,
iEngland : 100,
iHolyRome : 80,
iRussia : 100,
iMali : 30,
iPoland : 65,
iPortugal : 100,
iInca : 70,
iItaly : 100,
iMongols : 80,
iAztecs : 70,
iMughals : 80,
iOttomans : 100,
iThailand : 100,
iCongo : 20,
iIran : 100,
iNetherlands : 100,
iGermany : 100,
iAmerica : 100,
iArgentina : 100,
iMexico : 100,
iColombia : 80,
iBrazil : 100,
iCanada : 100,
})

dPatienceThreshold = CivDict({
iEgypt : 30,
iBabylonia : 30,
iHarappa : 30,
iChina : 30,
iGreece : 35,
iIndia : 50,
iPhoenicia : 35,
iPolynesia : 50,
iPersia : 30,
iRome : 25,
iMaya : 35,
iTamils : 45,
iEthiopia : 20,
iKorea : 25,
iByzantium : 25,
iJapan : 25,
iVikings : 30,
iTurks : 30,
iArabia : 30,
iTibet : 50,
iIndonesia : 30,
iMoors : 20,
iSpain : 20,
iFrance : 20,
iKhmer : 30,
iEngland : 20,
iHolyRome : 20,
iRussia : 30,
iMali : 35,
iPoland : 20,
iPortugal : 30,
iInca : 35,
iItaly : 25,
iMongols : 20,
iAztecs : 30,
iMughals : 35,
iOttomans : 35,
iThailand : 30,
iCongo : 20,
iIran : 30,
iNetherlands : 30,
iGermany : 20,
iAmerica : 30,
iArgentina : 40,
iMexico : 40,
iColombia : 30,
iBrazil : 40,
iCanada : 40,
}, 100)

dMaxColonists = CivDict({
iVikings : 1,
iSpain : 7,
iFrance : 5,
iEngland : 6,
iPortugal : 6, 
iNetherlands : 6,
iGermany : 2
})

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

# pagan religions
iNumPaganReligions = 19
(iAnunnaki, iAsatru, iAtua, iBaalism, iBon, iDruidism, iInti, iMazdaism, iMugyo, iOlympianism, 
iPesedjet, iRodnovery, iShendao, iShinto, iTengri, iTeotlMaya, iTeotlAztec, iVedism, iYoruba) = range(iNumPaganReligions)

iPaganVictory = iNumReligions
iSecularVictory = iNumReligions + 1

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

iNumUnits = 211
(iLion, iBear, iPanther, iWolf, iSettler, iCityBuilder, iPioneer, iWorker, iPunjabiWorker, iLabourer, 
iMadeireiro, iScout, iExplorer, iBandeirante, iSpy, iReligiousPersecutor, iJewishMissionary, iOrthodoxMissionary, iCatholicMissionary, iProtestantMissionary, 
iIslamicMissionary, iHinduMissionary, iBuddhistMissionary, iConfucianMissionary, iTaoistMissionary, iZoroastrianMissionary, iWarrior, iNativeWarrior, iMilitia, iAxeman, 
iLightSwordsman, iVulture, iDogSoldier, iSwordsman, iJaguar, iLegion, iGallicWarrior, iAucac, iShotelai, iHeavySwordsman, 
iSamurai, iHuscarl, iGhazi, iPombos, iSpearman, iHoplite, iSacredBand, iImmortal, iNativeRaider, iHeavySpearman, 
iPikeman, iLandsknecht, iArquebusier, iFirelancer, iTercio, iStrelets, iJanissary, iOromoWarrior, iQizilbash, iMohawk, 
iMusketeer, iRedcoat, iFusilier, iMinuteman, iRifleman, iMehalSefari, iGrenadier, iRocketeer, iGrenzer, iAlbionLegion, 
iAntiTank, iInfantry, iSamInfantry, iMobileSam, iMarine, iNavySeal, iParatrooper, iMechanizedInfantry, iArcher, iAsharittuBowman, 
iMedjay, iNativeArcher, iSkirmisher, iHolkan, iKelebolo, iLongbowman, iPatiyodha, iCrossbowman, iChokonu, iBalestriere, 
iChariot, iWarChariot, iHuluganni, iCidainh, iHorseman, iCompanion, iNumidianCavalry, iAsvaka, iCamelRider, iHorseArcher, 
iMangudai, iKhampa, iOghuz, iCamelArcher, iLancer, iVaru, iSavaran, iMobileGuard, iKeshik, iCataphract, 
iChangSuek, iFarari, iPistolier, iMountedBrave, iCamelGunner, iCuirassier, iGendarme, iConquistador, iWingedHussar, iHussar, 
iCossack, iLlanero, iDragoon, iGuard, iGrenadierCavalry, iCavalry, iRural, iWarElephant, iBallistaElephant, iTank, 
iPanzer, iMainBattleTank, iGunship, iCatapult, iBallista, iTrebuchet, iBombard, iHwacha, iSiegeElephant, iGreatBombard,
iCannon, iArtillery, iMachineGun, iHowitzer, iMobileArtillery, iWorkboat, iGalley, iWaka, iBireme, iWarGalley, 
iHeavyGalley, iDromon, iLongship, iCog, iDharani, iGalleass, iDjong, iKobukson, iLanternas, iCaravel, 
iCarrack, iGalleon, iEastIndiaman, iPrivateer, iCorsair, iFrigate, iShipOfTheLine, iManOfWar, iSteamship, iIronclad, 
iTorpedoBoat, iCruiser, iTransport, iDestroyer, iCorvette, iBattleship, iMissileCruiser, iStealthDestroyer, iSubmarine, iNuclearSubmarine, 
iCarrier, iBiplane, iFighter, iZero, iJetFighter, iBomber, iStealthBomber, iGuidedMissile, iDrone, iNuclearBomber, 
iICBM, iSatellite, iGreatProphet, iGreatArtist, iGreatScientist, iGreatMerchant, iGreatEngineer, iGreatStatesman, iGreatGeneral, iArgentineGreatGeneral, 
iGreatSpy, iFemaleGreatProphet, iFemaleGreatArtist, iFemaleGreatScientist, iFemaleGreatMerchant, iFemaleGreatEngineer, iFemaleGreatStatesman, iFemaleGreatGeneral, iFemaleGreatSpy, iSlave, 
iAztecSlave) = range(iNumUnits)

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

iNumUnitRoles = 22
(iBase, iDefend, iAttack, iCounter, iShock, iHarass, iCityAttack, iWorkerSea, iSettle, iSettleSea, 
iAttackSea, iFerry, iEscort, iExplore, iShockCity, iSiege, iCitySiege, iExploreSea, iSkirmish, iLightEscort,
iWork, iMissionary) = range(iNumUnitRoles)

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
iOrthodoxMonastery, iOrthodoxShrine, iCatholicTemple, iCatholicCathedral, iCatholicMonastery, iCatholicShrine, iProtestantTemple, iProtestantCathedral, iProtestantMonastery, iProtestantShrine, 
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

lGreatSpecialists = [iSpecialistGreatProphet, iSpecialistGreatArtist, iSpecialistGreatScientist, iSpecialistGreatMerchant, iSpecialistGreatEngineer, iSpecialistGreatStatesman, iSpecialistGreatGeneral, iSpecialistGreatSpy]

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
(iParameterCorePeriphery, iParameterAdministration, iParameterSeparatism, iParameterRecentExpansion, iParameterRazedCities, iParameterIsolationism,	# Expansion
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
lSouthAmerica = [rBrazil, rArgentina, rPeru, rColombia]
lCentralAmerica = [rCaribbean, rMesoamerica]
lNorthAmerica = [rCanada, rAlaska, rUnitedStates]
lOceania = [rAustralia, rOceania]

lAfrica = lNorthAfrica + lSubSaharanAfrica
lAsia = lMiddleEast + lIndia + lEastAsia
lAmerica = lSouthAmerica + lCentralAmerica + lNorthAmerica

#Projects

iNumProjects = 21
(iManhattanProject, iTheInternet, iHumanGenome, iSDI, iGPS, iISS, iBallisticMissile, iFirstSatellite, iManInSpace, iLunarLanding,
iGoldenRecord, iMarsMission, iLunarColony, iInterstellarProbe, iMarsFraming, iMarsPowerSource, iMarsExtractor, iMarsHabitat, iMarsHydroponics, iMarsLaboratory, iMarsControlCenter) = range(iNumProjects)

lMarsBaseComponents = [iMarsFraming, iMarsPowerSource, iMarsExtractor, iMarsHabitat, iMarsHydroponics, iMarsLaboratory, iMarsControlCenter]

#Eras

iNumEras = 7
(iAncient, iClassical, iMedieval, iRenaissance, iIndustrial, iGlobal, iDigital) = range (iNumEras)

# Culture

iNumCultureLevels = 7
(iCultureLevelNone, iCultureLevelPoor, iCultureLevelFledgling, iCultureLevelDeveloping, iCultureLevelRefined, iCultureLevelInfluential, iCultureLevelLegendary) = range(iNumCultureLevels)


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
(iLeaderBarbarian, iNativeLeader, iIndependentLeader, iRamesses, iCleopatra, iBaibars, iNasser, iSargon, iHammurabi, iVatavelli,
iQinShiHuang, iTaizong, iHongwu, iMao, iPericles, iAlexanderTheGreat, iGeorge, iAsoka, iChandragupta, iShivaji, 
iGandhi, iHiram, iHannibal, iAhoeitu, iCyrus, iDarius, iKhosrow, iJuliusCaesar, iAugustus, iPacal,
iRajendra, iKrishnaDevaRaya, iEzana, iZaraYaqob, iMenelik, iWangKon, iSejong, iJustinian, iBasil, iKammu,
iOdaNobunaga, iMeiji, iRagnar, iGustav, iGerhardsen, iBumin, iAlpArslan, iTamerlane, iHarun, iSaladin,
iSongtsen, iLobsangGyatso, iDharmasetu, iHayamWuruk, iSuharto, iRahman, iYaqub, iIsabella, iPhilip, iFranco,
iCharlemagne, iLouis, iNapoleon, iDeGaulle, iSuryavarman, iAlfred, iElizabeth, iVictoria, iChurchill, iBarbarossa,
iCharles, iFrancis, iIvan, iPeter, iCatherine, iAlexanderI, iStalin, iMansaMusa, iCasimir, iSobieski,
iPilsudski, iWalesa, iAfonso, iJoao, iMaria, iHuaynaCapac, iCastilla, iLorenzo, iCavour, iMussolini,
iGenghisKhan, iKublaiKhan, iMontezuma, iTughluq, iAkbar, iBhutto, iMehmed, iSuleiman, iAtaturk, iNaresuan,
iMongkut, iMbemba, iAbbas, iKhomeini, iWillemVanOranje, iWilliam, iFrederick, iBismarck, iHitler, iWashington,
iLincoln, iRoosevelt, iSanMartin, iPeron, iJuarez, iSantaAnna, iCardenas, iBolivar, iPedro, iVargas,
iMacDonald, iTrudeau, iBoudica, iBrennus, iSittingBull) = range(iNumLeaders)

dResurrectionLeaders = CivDict({
	iChina : iHongwu,
	iIndia : iShivaji,
	iEgypt : iBaibars,
})

iNumPeriods = 24
(iPeriodMing, iPeriodMaratha, iPeriodModernGreece, iPeriodCarthage, iPeriodVijayanagara,
iPeriodByzantineConstantinople, iPeriodSeljuks, iPeriodMeiji, iPeriodDenmark, iPeriodNorway, 
iPeriodSweden, iPeriodUzbeks, iPeriodSaudi, iPeriodVietnam, iPeriodMorocco, 
iPeriodSpain, iPeriodAustria, iPeriodYuan, iPeriodPeru, iPeriodLateInca, 
iPeriodModernItaly, iPeriodPakistan, iPeriodOttomanConstantinople, iPeriodModernGermany) = range(iNumPeriods)

iNumImpacts = 5
(iImpactMarginal, iImpactLimited, iImpactSignificant, iImpactCritical, iImpactPlayer) = range(iNumImpacts)

dTradingCompanyPlots = CivDict({
iVikings : [],
iSpain : [(109, 33)],
iFrance : [(101, 37), (101, 36), (102, 36), (102, 35), (103, 35), (103, 34), (104, 34), (104, 33)],
iEngland : [(95, 37), (94, 37), (94, 36), (94, 35), (94, 34), (93, 34), (93, 33), (92, 33), (92, 32), (88, 33), (88, 34), (88, 35)],
iPortugal : [(82, 34), (89, 31), (101, 29), (105, 39), (93, 28), (93, 27), (71, 17), (69, 13), (54, 26), (62, 20)],
iNetherlands : [(99, 28), (99, 27), (100, 27), (100, 26), (101, 26), (104, 25), (105, 25), (106, 25), (107, 24), (104, 27), (105, 27), (106, 27), (104, 28), (106, 28), (105, 29), (106, 29)],
iGermany : [],
})

lSecondaryCivs = [iHarappa, iPolynesia, iTamils, iTibet, iMoors, iPoland, iCongo, iArgentina, iBrazil]

lMongolCivs = [iPersia, iByzantium, iArabia, iRussia]

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

newline = "[NEWLINE]"
bullet = "[ICON_BULLET]"
event_bullet = "INTERFACE_EVENT_BULLET"
event_cancel = "INTERFACE_BUTTONS_CANCEL"