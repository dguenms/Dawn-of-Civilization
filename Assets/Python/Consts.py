# Rhye's and Fall of Civilization - Constants
# globals

from CvPythonExtensions import *
from DataStructures import *
from CoreTypes import *

gc = CyGlobalContext()

iWorldX = 150
iWorldY = 80

iNumPlayers = gc.getMAX_PLAYERS()

# civilizations, not players
iNumCivs = 74
(iAmerica, iArabia, iArgentina, iAssyria, iAustralia, iAztecs, iBabylonia, iBelgium, iBrazil, iBurma, 
iByzantium, iCanada, iCarthage, iCelts, iChina, iColombia, iDravidia, iEgypt, iEngland, iEthiopia, 
iFrance, iGermany, iGreece, iHarappa, iHittites, iHolyRome, iInca, iIndia, iIran, iItaly, 
iJapan, iJava, iKhmer, iCongo, iKorea, iKushans, iMalays, iMali, iManchuria, iMaya, 
iMexico, iMisr, iMongols, iMoors, iMughals, iNativeAmericans, iNetherlands, iNorse, iNubia, iOttomans, 
iPersia, iPoland, iPolynesia, iPortugal, iRome, iRus, iRussia, iSaudis, iSpain, iSumeria, 
iSwahili, iSweden, iTatars, iThailand, iTibet, iToltecs, iTurks, iVietnam, iZulu, iIndependent, 
iIndependent2, iNative, iMinor, iBarbarian) = tuple(Civ(i) for i in range(iNumCivs))

iPhoenicia = iCarthage

lBirthOrder = [
	iEgypt,
	iBabylonia,
	iHarappa,
	iAssyria,
	iNubia,
	iChina,
	iHittites,
	iGreece,
	iIndia,
	iCarthage,
	iPolynesia,
	iPersia,
	iCelts,
	iRome,
	iMaya,
	iDravidia,
	iEthiopia,
	iToltecs,
	iKushans,
	iKorea,
	iKhmer,
	iMali,
	iByzantium,
	iFrance,
	iMalays,
	iJapan,
	iNorse,
	iTurks,
	iArabia,
	iTibet,
	iMoors,
	iJava,
	iSpain,
	iEngland,
	iHolyRome,
	iBurma,
	iRus,
	iVietnam,
	iSwahili,
	iMisr,
	iPoland,
	iPortugal,
	iInca,
	iItaly,
	iMongols,
	iAztecs,
	iMughals,
	iThailand,
	iSweden,
	iTatars,
	iRussia,
	iOttomans,
	iCongo,
	iIran,
	iNetherlands,
	iManchuria,
	iGermany,
	iSaudis,
	iAmerica,
	iArgentina,
	iMexico,
	iColombia,
	iBrazil,
	iBelgium,
	iAustralia,
	iCanada
]

lCivOrder = lBirthOrder + [
	iIndependent,
	iIndependent2,
	iNative,
	iBarbarian
]

# used in: Congresses, DynamicCivs, Plague, RFCUtils, UniquePowers, Victory
# a civilisation can be in multiple civ groups
iNumCivGroups = 6
(iCivGroupEurope, iCivGroupEastAsia, iCivGroupSouthAsia, iCivGroupMiddleEast, iCivGroupAfrica, iCivGroupAmerica) = range(iNumCivGroups)

dCivGroups = {
iCivGroupEurope : [iGreece, iRome, iCelts, iByzantium, iFrance, iNorse, iSpain, iEngland, iHolyRome, iRus, iItaly, iPoland, iPortugal, iSweden, iRussia, iTatars, iNetherlands, iGermany, iBelgium],
iCivGroupEastAsia : [iChina, iJapan, iKorea, iTibet, iVietnam, iMongols, iRussia, iTurks, iManchuria],
iCivGroupSouthAsia : [iIndia, iHarappa, iPolynesia, iDravidia, iKushans, iKhmer, iMalays, iJava, iBurma, iVietnam, iMughals, iThailand, iAustralia],
iCivGroupMiddleEast : [iEgypt, iBabylonia, iAssyria, iHittites, iPersia, iKushans, iByzantium, iArabia, iMoors, iSwahili, iMisr, iOttomans, iCarthage, iTurks, iTatars, iIran, iSaudis],
iCivGroupAfrica : [iEgypt, iNubia, iCarthage, iEthiopia, iMali, iMoors, iMisr, iSwahili, iCongo],
iCivGroupAmerica : [iMaya, iToltecs, iInca, iAztecs, iAmerica, iArgentina, iMexico, iColombia, iBrazil, iCanada],
}

# used in: Stability
# tech groups share techs within each other on respawn
iNumTechGroups = 4
(iTechGroupWestern, iTechGroupMiddleEast, iTechGroupFarEast, iTechGroupNativeAmerica) = range(iNumTechGroups)

dTechGroups = {
iTechGroupWestern : [iRome, iGreece, iCelts, iByzantium, iFrance, iNorse, iSpain, iEngland, iHolyRome, iRus, iPoland, iPortugal, iItaly, iSweden, iRussia, iNetherlands, iGermany, iAmerica, iArgentina, iMexico, iColombia, iBrazil, iBelgium, iAustralia, iCanada],
iTechGroupMiddleEast : [iEgypt, iBabylonia, iHarappa, iAssyria, iNubia, iHittites, iIndia, iCarthage, iPersia, iEthiopia, iKushans, iMali, iArabia, iMoors, iSwahili, iMisr, iOttomans, iTatars, iMughals, iDravidia, iCongo, iTurks, iIran, iSaudis],
iTechGroupFarEast : [iChina, iKorea, iKhmer, iMalays, iJapan, iJava, iTibet, iBurma, iVietnam, iMongols, iThailand, iManchuria],
iTechGroupNativeAmerica : [iPolynesia, iMaya, iToltecs, iInca, iAztecs],
}

lBioNewWorld = [iMaya, iToltecs, iInca, iAztecs]
lBioOldWorld = [iCiv for iCiv in lBirthOrder if iCiv not in lBioNewWorld]

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

# scripted conquerors
iNumConquests = 14

lNeighbours = [
	(iEgypt, iBabylonia),
	(iEgypt, iAssyria),
	(iEgypt, iNubia),
	(iEgypt, iHittites),
	(iEgypt, iGreece),
	(iEgypt, iPersia),
	(iEgypt, iCarthage),
	(iEgypt, iRome),
	(iEgypt, iEthiopia),
	(iEgypt, iByzantium),
	(iEgypt, iArabia),
	(iEgypt, iMoors),
	(iEgypt, iMisr),
	(iEgypt, iOttomans),
	(iEgypt, iSaudis),
	(iBabylonia, iAssyria),
	(iBabylonia, iHittites),
	(iBabylonia, iGreece),
	(iBabylonia, iPersia),
	(iBabylonia, iTurks),
	(iBabylonia, iArabia),
	(iBabylonia, iOttomans),
	(iBabylonia, iMongols),
	(iBabylonia, iCarthage),
	(iBabylonia, iByzantium),
	(iBabylonia, iMisr),
	(iBabylonia, iIran),
	(iBabylonia, iSaudis),
	(iHarappa, iIndia),
	(iHarappa, iPersia),
	(iHarappa, iDravidia),
	(iHarappa, iKushans),
	(iHarappa, iTibet),
	(iHarappa, iMughals),
	(iHarappa, iIran),
	(iAssyria, iHittites),
	(iAssyria, iCarthage),
	(iAssyria, iGreece),
	(iAssyria, iPersia),
	(iAssyria, iByzantium),
	(iAssyria, iTurks),
	(iAssyria, iArabia),
	(iAssyria, iMisr),
	(iAssyria, iOttomans),
	(iAssyria, iIran),
	(iChina, iVietnam),
	(iChina, iKushans),
	(iChina, iJapan),
	(iChina, iKorea),
	(iChina, iTurks),
	(iChina, iTibet),
	(iChina, iBurma),
	(iChina, iMongols),
	(iChina, iManchuria),
	(iHittites, iGreece),
	(iHittites, iCarthage),
	(iHittites, iPersia),
	(iHittites, iCelts),
	(iHittites, iByzantium),
	(iHittites, iArabia),
	(iHittites, iMisr),
	(iHittites, iOttomans),
	(iHittites, iIran),
	(iGreece, iPersia),
	(iGreece, iCarthage),
	(iGreece, iRome),
	(iGreece, iCelts),
	(iGreece, iByzantium),
	(iGreece, iOttomans),
	(iGreece, iItaly),
	(iIndia, iPersia),
	(iIndia, iDravidia),
	(iIndia, iKushans),
	(iIndia, iMalays),
	(iIndia, iTibet),
	(iIndia, iJava),
	(iIndia, iKhmer),
	(iIndia, iBurma),
	(iIndia, iMughals),
	(iIndia, iIran),
	(iCarthage, iRome),
	(iCarthage, iSpain),
	(iCarthage, iMali),
	(iCarthage, iPersia),
	(iCarthage, iArabia),
	(iCarthage, iMoors),
	(iCarthage, iMisr),
	(iCarthage, iOttomans),
	(iCarthage, iItaly),
	(iPolynesia, iAustralia),
	(iNubia, iEthiopia),
	(iNubia, iArabia),
	(iNubia, iMisr),
	(iPersia, iRome),
	(iPersia, iKushans),
	(iPersia, iTurks),
	(iPersia, iByzantium),
	(iPersia, iOttomans),
	(iPersia, iMongols),
	(iPersia, iMughals),
	(iPersia, iTatars),
	(iPersia, iRussia),
	(iPersia, iIran),
	(iPersia, iSaudis),
	(iCelts, iRome),
	(iCelts, iNorse),
	(iCelts, iSpain),
	(iCelts, iFrance),
	(iCelts, iEngland),
	(iCelts, iHolyRome),
	(iCelts, iGermany),
	(iRome, iSpain),
	(iRome, iByzantium),
	(iRome, iFrance),
	(iRome, iHolyRome),
	(iRome, iItaly),
	(iRome, iGermany),
	(iRome, iMoors),
	(iDravidia, iKushans),
	(iDravidia, iMalays),
	(iDravidia, iJava),
	(iDravidia, iKhmer),
	(iDravidia, iBurma),
	(iDravidia, iMughals),
	(iEthiopia, iArabia),
	(iEthiopia, iSwahili),
	(iToltecs, iAztecs),
	(iToltecs, iAmerica),
	(iToltecs, iMexico),
	(iToltecs, iColombia),
	(iKushans, iTurks),
	(iKushans, iMongols),
	(iKushans, iMughals),
	(iKushans, iIran),
	(iKorea, iMongols),
	(iKorea, iJapan),
	(iKorea, iManchuria),
	(iKhmer, iMalays),
	(iKhmer, iJava),
	(iKhmer, iBurma),
	(iKhmer, iVietnam),
	(iKhmer, iThailand),
	(iMali, iMoors),
	(iMali, iCongo),
	(iMaya, iToltecs),
	(iMaya, iAztecs),
	(iMaya, iMexico),
	(iMaya, iColombia),
	(iByzantium, iTurks),
	(iByzantium, iArabia),
	(iByzantium, iRus),
	(iByzantium, iMisr),
	(iByzantium, iMongols),
	(iByzantium, iTatars),
	(iByzantium, iRussia),
	(iByzantium, iOttomans),
	(iByzantium, iIran),
	(iFrance, iNorse),
	(iFrance, iEngland),
	(iFrance, iHolyRome),
	(iFrance, iNetherlands),
	(iFrance, iItaly),
	(iFrance, iGermany),
	(iFrance, iBelgium),
	(iMalays, iJava),
	(iMalays, iVietnam),
	(iMalays, iThailand),
	(iJapan, iMongols),
	(iJapan, iManchuria),
	(iNorse, iEngland),
	(iNorse, iHolyRome),
	(iNorse, iRus),
	(iNorse, iPoland),
	(iNorse, iSweden),
	(iNorse, iRussia),
	(iNorse, iNetherlands),
	(iNorse, iGermany),
	(iTurks, iTibet),
	(iTurks, iArabia),
	(iTurks, iRus),
	(iTurks, iMisr),
	(iTurks, iMongols),
	(iTurks, iMughals),
	(iTurks, iTatars),
	(iTurks, iOttomans),
	(iTurks, iIran),
	(iArabia, iMoors),
	(iArabia, iSwahili),
	(iArabia, iMisr),
	(iArabia, iMongols),
	(iArabia, iOttomans),
	(iArabia, iIran),
	(iArabia, iSaudis),
	(iTibet, iBurma),
	(iTibet, iMongols),
	(iTibet, iMughals),
	(iMoors, iSpain),
	(iMoors, iMisr),
	(iMoors, iPortugal),
	(iJava, iThailand),
	(iJava, iAustralia),
	(iSpain, iFrance),
	(iSpain, iPortugal),
	(iSpain, iItaly),
	(iEngland, iNetherlands),
	(iEngland, iBelgium),
	(iHolyRome, iItaly),
	(iHolyRome, iPoland),
	(iHolyRome, iSweden),
	(iHolyRome, iNetherlands),
	(iHolyRome, iGermany),
	(iHolyRome, iBelgium),
	(iRus, iPoland),
	(iRus, iMongols),
	(iRus, iTatars),
	(iRus, iSweden),
	(iRus, iRussia),
	(iRus, iOttomans),
	(iMisr, iOttomans),
	(iMisr, iIran),
	(iMisr, iSaudis),
	(iVietnam, iBurma),
	(iVietnam, iThailand),
	(iBurma, iThailand),
	(iPoland, iTatars),
	(iPoland, iSweden),
	(iPoland, iRussia),
	(iPoland, iGermany),
	(iInca, iArgentina),
	(iInca, iColombia),
	(iInca, iBrazil),
	(iMongols, iRussia),
	(iMongols, iOttomans),
	(iMongols, iTatars),
	(iMongols, iManchuria),
	(iMongols, iIran),
	(iAztecs, iAmerica),
	(iAztecs, iMexico),
	(iAztecs, iColombia),
	(iMughals, iIran),
	(iSweden, iRussia),
	(iSweden, iGermany),
	(iTatars, iRussia),
	(iTatars, iOttomans),
	(iRussia, iOttomans),
	(iRussia, iGermany),	
	(iOttomans, iIran),
	(iOttomans, iSaudis),
	(iIran, iSaudis),
	(iNetherlands, iBelgium),
	(iGermany, iBelgium),
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
	(iPhoenicia, iCelts),
	(iPhoenicia, iByzantium),
	(iPhoenicia, iTurks),
	(iPhoenicia, iIran),
	(iPersia, iArabia),
	(iPersia, iSwahili),
	(iRome, iOttomans),
	(iMaya, iSpain),
	(iDravidia, iEngland),
	(iDravidia, iSwahili),
	(iDravidia, iNetherlands),
	(iVietnam, iJapan),
	(iVietnam, iFrance),
	(iVietnam, iAmerica),
	(iKhmer, iJapan),
	(iMalays, iJapan),
	(iMalays, iPortugal),
	(iMalays, iNetherlands),
	(iJava, iJapan),
	(iJava, iNetherlands),
	(iArabia, iBabylonia),
	(iArabia, iGreece),
	(iArabia, iPersia),
	(iTibet, iManchuria),
	(iSpain, iArabia),
	(iSpain, iOttomans),
	(iEngland, iBurma),
	(iEngland, iAustralia),
	(iHolyRome, iOttomans),
	(iMisr, iMongols),
	(iMisr, iTatars),
	(iInca, iSpain),
	(iItaly, iOttomans),
	(iAztecs, iSpain),
	(iMughals, iEngland),
	(iOttomans, iRome),
	(iRussia, iManchuria),
	(iThailand, iJapan),
	(iCongo, iPortugal),
	(iCongo, iBelgium),
	(iNetherlands, iSpain),
	(iNetherlands, iAustralia),
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
	(iAmerica, iSaudis),
]

dBirth = CivDict({
iEgypt : -3000,
iBabylonia : -3000,
iHarappa : -3000,
iAssyria : -2600,
iNubia : -2200,
iChina : -2070,
iHittites : -1800,
iGreece : -1600,
iIndia : -1500,
iPhoenicia : -1200,
iPolynesia : -1000,
iPersia : -850,
iCelts : -600,
iRome : -509,
iMaya : -400,
iDravidia : -300,
iEthiopia : -290,
iToltecs : -200,
iKushans : -135,
iKorea : -50,
iKhmer : 50,
iMali : 300,
iByzantium : 330,
iFrance : 496,
iMalays : 500,
iJapan : 525,
iNorse : 551,
iTurks : 552,
iArabia : 620,
iTibet : 630,
iMoors : 711,
iJava : 716,
iSpain : 722,
iEngland : 820,
iHolyRome : 840,
iBurma : 849,
iRus : 880,
iVietnam : 938,
iSwahili : 957,
iMisr : 969,
iPoland : 1025,
iPortugal : 1130,
iInca : 1150,
iItaly : 1167,
iMongols : 1190,
iAztecs : 1195,
iMughals : 1206,
iThailand : 1238,
iSweden : 1252,
iTatars : 1259,
iRussia : 1263,
iOttomans : 1280,
iCongo : 1390,
iIran : 1501,
iNetherlands : 1580,
iManchuria : 1586,
iGermany : 1700,
iSaudis : 1744,
iAmerica : 1776,
iArgentina : 1810,
iMexico : 1810,
iColombia : 1814,
iBrazil : 1822,
iBelgium : 1830,
iAustralia : 1851,
iCanada : 1867,
}, -3000)

lBirthCivs = dBirth.keys()

dFall = CivDict({
iEgypt : -343,
iBabylonia : -539,
iHarappa : -1700,
iAssyria : -609,
iNubia : 350,
iChina : 1127,
iHittites : -900,
iGreece : -146,
iIndia : 600,
iPhoenicia : -146,
iPolynesia : 1200,
iPersia : 651,
iCelts : 1169,
iRome : 235,
iMaya : 900,
iDravidia : 1000,
iEthiopia : 960,
iToltecs : 950,
iKushans : 375,
iMalays : 1511,
iKorea : 1255,
iKhmer : 1200,
iMali : 1600,
iByzantium : 1204,
iNorse : 1300,
iTurks : 1507,
iArabia : 900,
iTibet : 1500,
iMoors : 1500,
iJava: 1755,
iBurma : 1885,
iRus : 1300,
iSwahili : 1513,
iMisr : 1517,
iPoland : 1650,
iInca : 1533,
iMongols : 1368,
iAztecs : 1521,
iMughals : 1640,
iTatars : 1502,
iCongo : 1800,
iManchuria : 1860,
}, 2025)

# Leoreth: determine neighbour lists from pairwise neighbours for easier lookup
dNeighbours = dictFromEdges(lBirthCivs, lNeighbours)

# Leoreth: determine influence lists from pairwise influences for easier lookup
dInfluences = dictFromEdges(lBirthCivs, lInfluences)

dResurrections = CivDict({
iEgypt : [(-3000, -50)],
iBabylonia : [(-3000, -500)],
iAssyria : [(-3000, -600)],
iNubia : [(500, 1500)],
iChina : [(600, 2025)],
iHittites : [(-1800, -800)],
iGreece : [(1800, 2025)],
iIndia : [(1600, 1800), (1900, 2025)],
iPhoenicia : [(-1000, -150)],
iPersia : [(220, 580)],
iCelts : [(400, 1150), (1850, 2025)],
iRome : [(-500, 450)],
iMaya : [(0, 800)],
iDravidia : [(-300, 600), (1300, 1650)],
iEthiopia : [(1270, 1520), (1850, 2025)],
iKorea : [(600, 2025)],
iKhmer : [(1950, 2025)],
iMali : [(1340, 1590)],
iByzantium : [(1100, 1280)],
iFrance : [(1700, 2025)],
iMalays : [(500, 1500), (1940, 2025)],
iJapan : [(1800, 2025)],
iNorse : [(1520, 2025)],
iTurks : [(1350, 1500)],
iMoors : [(1000, 2025)],
iJava : [(720, 1755), (1900, 2025)],
iSpain : [(1700, 2025)],
iEngland : [(1700, 2025)],
iHolyRome : [(1800, 2025)],
iBurma : [(850, 1885), (1950, 2025)],
iRus : [(1650, 2025)],
iVietnam : [(950, 2025)],
iSwahili : [(1960, 2025)],
iMisr : [(1800, 2025)],
iPoland : [(1920, 2025)],
iPortugal : [(1700, 2025)],
iInca : [(1800, 1930)],
iItaly : [(1820, 2025)],
iMongols : [(1910, 2025)],
iMughals : [(1940, 2025)],
iThailand : [(1700, 2025)],
iSweden : [(1250, 2025)],
iRussia : [(1280, 1550), (1700, 2025)],
iOttomans : [(1700, 2025)],
iIran : [(1500, 2025)],
iNetherlands : [(1700, 2025)],
iGermany : [(1840, 2025)],
iSaudis : [(1820, 2025)],
iAmerica : [(1776, 2025)],
iArgentina : [(1810, 2025)],
iMexico : [(1810, 2025)],
iColombia : [(1810, 2025)],
iBrazil : [(1820, 2025)],
iBelgium : [(1830, 2025)],
iAustralia : [(1851, 2025)],
iCanada : [(1867, 2025)],
}, [])

dAggressionLevel = CivDict({
iBabylonia : 1,
iAssyria : 3,
iChina : 1,
iHittites : 2,
iNubia : 1,
iGreece : 2,
iPersia : 3,
iCelts : 1,
iRome : 3,
iMaya : 1,
iDravidia : 1,
iToltecs: 1,
iKushans : 1,
iKhmer : 2,
iByzantium : 1,
iFrance : 1,
iJapan : 1,
iNorse : 2,
iTurks : 2,
iArabia : 2,
iTibet : 1,
iMoors : 1,
iJava : 1,
iSpain : 2,
iEngland : 1,
iHolyRome : 1,
iBurma : 2,
iVietnam : 1,
iMisr : 1,
iPoland : 1,
iInca : 1,
iMongols : 3,
iAztecs : 2,
iMughals : 1,
iTatars : 2,
iSweden : 1,
iRussia : 1,
iOttomans : 2,
iIran : 1,
iManchuria : 1,
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
iAssyria: 50,
iNubia: 20,
iChina: 40,
iHittites: 50,
iGreece: 50,
iIndia: 20,
iPhoenicia: 20,
iPolynesia: 20,
iPersia: 30,
iCelts: 20,
iRome: 20,
iMaya: 20,
iDravidia: 20,
iEthiopia: 20,
iToltecs: 20,
iKushans: 30,
iMalays: 30,
iKorea: 20,
iKhmer: 20,
iMali: 30,
iByzantium: 20,
iFrance: 20,
iJapan: 20,
iNorse: 20,
iTurks: 50,
iArabia: 20,
iTibet: 20,
iJava: 20,
iMoors: 20,
iSpain: 20,
iEngland: 50,
iHolyRome: 20,
iBurma: 40,
iRus: 20,
iVietnam: 20,
iSwahili: 20,
iMisr: 60,
iPoland: 60,
iPortugal: 60,
iInca: 30,
iItaly: 40,
iMongols: 30,
iAztecs: 50,
iMughals: 30,
iTatars: 30,
iThailand: 20,
iSweden : 30,
iRussia: 50,
iOttomans: 30,
iCongo: 20,
iIran: 20,
iNetherlands: 60,
iManchuria: 30,
iGermany: 20,
iSaudis: 20,
iAmerica: 50,
iArgentina: 40,
iMexico: 40,
iColombia: 40,
iBrazil: 40,
iBelgium: 60,
iAustralia: 40,
iCanada: 40,
}, 0)

dResurrectionProbability = CivDict({
iEgypt : 25,
iBabylonia : 40,
iHarappa : 0,
iAssyria : 40,
iNubia : 20,
iChina : 100,
iHittites : 0,
iNubia : 20,
iGreece : 60,
iIndia : 50,
iPhoenicia : 30,
iPolynesia : 40,
iPersia : 70,
iCelts : 50,
iRome : 65,
iMaya : 30,
iDravidia : 10,
iEthiopia : 80,
iMalays : 60,
iKorea : 80,
iKhmer : 60,
iMali : 30,
iByzantium : 65,
iFrance : 100,
iJapan : 100,
iNorse : 60,
iTurks : 30,
iArabia : 100,
iTibet : 60,
iMoors : 70,
iJava : 80,
iSpain : 100,
iEngland : 100,
iHolyRome : 80,
iBurma : 60,
iVietnam : 60,
iRus: 60,
iSwahili: 40,
iMisr: 80,
iPoland : 65,
iPortugal : 100,
iInca : 70,
iItaly : 100,
iMongols : 80,
iAztecs : 70,
iMughals : 80,
iThailand : 100,
iSweden : 100,
iRussia : 100,
iOttomans : 100,
iCongo : 20,
iIran : 100,
iNetherlands : 100,
iManchuria: 80,
iGermany : 100,
iSaudis : 70,
iAmerica : 100,
iArgentina : 100,
iMexico : 100,
iColombia : 80,
iBrazil : 100,
iBelgium : 100,
iAustralia : 100,
iCanada : 100,
})

dPatienceThreshold = CivDict({
iEgypt : 30,
iBabylonia : 30,
iHarappa : 30,
iAssyria : 25,
iNubia : 30,
iChina : 30,
iHittites : 30,
iGreece : 35,
iIndia : 50,
iPhoenicia : 35,
iPolynesia : 50,
iPersia : 30,
iCelts : 25,
iRome : 25,
iMaya : 35,
iDravidia : 45,
iEthiopia : 20,
iToltecs : 20,
iKushans : 25,
iMalays : 40,
iKorea : 25,
iKhmer : 30,
iMali : 35,
iByzantium : 25,
iFrance : 20,
iJapan : 25,
iNorse : 30,
iTurks : 30,
iArabia : 30,
iTibet : 50,
iMoors : 20,
iJava : 30,
iSpain : 20,
iEngland : 20,
iHolyRome : 20,
iBurma : 30,
iRus : 20,
iVietnam : 20,
iSwahili : 40,
iMisr : 30,
iPoland : 20,
iPortugal : 30,
iInca : 35,
iItaly : 25,
iMongols : 20,
iAztecs : 30,
iMughals : 35,
iTatars : 20,
iThailand : 30,
iSweden : 30,
iRussia : 30,
iOttomans : 35,
iCongo : 20,
iIran : 30,
iNetherlands : 30,
iManchuria: 40,
iGermany : 20,
iSaudis : 30,
iAmerica : 30,
iArgentina : 40,
iMexico : 40,
iColombia : 30,
iBrazil : 40,
iBelgium : 30,
iAustralia : 40,
iCanada : 40,
}, 100)

dMaxColonists = CivDict({
iSweden : 1,
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
iNumPaganReligions = 22
(iAnunnaki, iAsatru, iAtua, iBaalism, iBidaism, iBon, iBukongo, iDruidism, iInti, iMazdaism, 
iMugyo, iOlympianism, iPesedjet, iRodnovery, iShendao, iShinto, iTengri, iTeotlMaya, iTeotlToltec, iTeotlAztec, 
iVedism, iYoruba) = range(iNumPaganReligions)

iPaganVictory = iNumReligions
iSecularVictory = iNumReligions + 1

# corporations
iNumCorporations = 10
(iSilkRoute, iTradingCompany, iCerealIndustry, iFishingIndustry, iTextileIndustry, iSteelIndustry, iOilIndustry, iLuxuryIndustry, iAutomobileIndustry, iComputerIndustry) = range(iNumCorporations)

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
iBallistics, iEngine, iRailroad, iElectricity, iRefrigeration, iCollectivism, iJournalism,
iPneumatics, iAssemblyLine, iRefining, iFilm, iMicrobiology, iConsumerism, iCivilRights,
iInfrastructure, iFlight, iSynthetics, iRadio, iPsychology, iMacroeconomics, iSocialServices,
iAviation, iRocketry, iFission, iElectronics, iTelevision, iPowerProjection, iGeopolitics,
iRadar, iSpaceflight, iNuclearPower, iLaser, iComputers, iTourism, iEcology,
iAerodynamics, iSatellites, iSuperconductors, iRobotics, iTelecommunications, iRenewableEnergy, iGenetics,
iSupermaterials, iFusion, iNanotechnology, iCybernetics, iBiotechnology,
iUnifiedTheory, iArtificialIntelligence,
iTranshumanism) = range(iNumTechs)

# initialise unit variables to unit indices from XML

iNumUnits = 236
(iLion, iBear, iPanther, iWolf, iSettler, iCityBuilder, iPioneer, iWorker, iPunjabiWorker, iLabourer, 
iMadeireiro, iScout, iExplorer, iBandeirante, iSpy, iReligiousPersecutor, iJewishMissionary, iOrthodoxMissionary, iCatholicMissionary, iProtestantMissionary, 
iIslamicMissionary, iHinduMissionary, iBuddhistMissionary, iConfucianMissionary, iTaoistMissionary, iZoroastrianMissionary, iWarrior, iNativeWarrior, iMilitia, iAxeman, 
iLightSwordsman, iVulture, iDogSoldier, iOathsworn, iSwordsman, iJaguar, iLegion, iGallicWarrior, iPendekar, iAucac, 
iShotelai, iHeavySwordsman, iGallowglass, iSamurai, iHuscarl, iGhazi, iDruzhina, iPombos, iSpearman, iAzmaru, 
iHoplite, iSacredBand, iImmortal, iNativeRaider, iHeavySpearman, iKyundaw, iPikeman, iLandsknecht, iArquebusier, iFirelancer, 
iTercio, iStrelets, iJanissary, iOromoWarrior, iQizilbash, iMohawk, iMusketeer, iRedcoat, iCarolean, iFusilier, 
iRifleman, iMehalSefari, iGrenadier, iRocketeer, iGrenzer, iAlbionLegion, iChasseur, iAntiTank, iInfantry, iVietCong, 
iDigger, iSamInfantry, iMobileSam, iMarine, iNavySeal, iParatrooper, iMechanizedInfantry, iArcher, iAsharittuBowman, iMedjay, 
iNativeArcher, iSkirmisher, iHolkan, iAtlatl, iKelebolo, iLongbowman, iPatiyodha, iRattanArcher, iCrossbowman, iChokonu, 
iBalestriere, iChariot, iWarChariot, iHuluganni, iCidainh, iHorseman, iCompanion, iNumidianCavalry, iAsvaka, iCamelRider, 
iHorseArcher, iMangudai, iKhampa, iOghuz, iCamelArcher, iLancer, iSavaran, iFarari, iMobileGuard, iMamluk, 
iKeshik, iCataphract, iChambul, iChangSuek, iPistolier, iHakkapeliitta, iMountedBrave, iCamelGunner, iZamburak, iCuirassier, 
iGendarme, iConquistador, iWingedHussar, iSowar, iBannerman, iHussar, iCossack, iLlanero, iDragoon, iCassay, 
iIkhwan, iGrenadierCavalry, iCavalry, iRural, iLightHorse, iWarElephant, iVaru, iBallistaElephant, iTank, iPanzer, 
iMainBattleTank, iGunship, iCatapult, iSiegeRam, iBallista, iTrebuchet, iBombard, iHwacha, iLantaka, iSiegeElephant, 
iGreatBombard, iCannon, iGribeauval, iArtillery, iMachineGun, iHowitzer, iMobileArtillery, iWorkboat, iGalley, iWaka, 
iBireme, iWarGalley, iHeavyGalley, iDromon, iLongship, iCog, iDharani, iDhow, iGalleass, iDjong, 
iKobukson, iLanternas, iCaravel, iCarrack, iGalleon, iFluyt, iPrivateer, iCorsair, iFrigate, iShipOfTheLine, 
iManOfWar, iSteamship, iIronclad, iTorpedoBoat, iCruiser, iTransport, iDestroyer, iCorvette, iBattleship, iMissileCruiser, 
iStealthDestroyer, iSubmarine, iNuclearSubmarine, iCarrier, iSupercarrier, iBiplane, iFighter, iZero, iJetFighter, iBomber, 
iFlyingFortress, iStealthBomber, iGuidedMissile, iDrone, iNuclearBomber, iICBM, iSatellite, iGreatProphet, iGreatArtist, iGreatScientist, 
iGreatMerchant, iGreatEngineer, iGreatStatesman, iGreatGeneral, iArgentineGreatGeneral, iGreatSpy, iFemaleGreatProphet, iFemaleGreatArtist, iFemaleGreatScientist, iFemaleGreatMerchant, 
iFemaleGreatEngineer, iFemaleGreatStatesman, iFemaleGreatGeneral, iFemaleGreatSpy, iSlave, iAztecSlave) = range(iNumUnits)

lGreatPeopleUnits = [iGreatProphet, iGreatArtist, iGreatScientist, iGreatMerchant, iGreatEngineer, iGreatStatesman, iGreatGeneral, iGreatSpy]

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


iNumUnitRoles = 23
(iBase, iDefend, iAttack, iCounter, iShock, iHarass, iCityAttack, iWorkerSea, iSettle, iSettleSea, 
iAttackSea, iAssaultSea, iFerry, iEscort, iExplore, iShockCity, iSiege, iCitySiege, iExploreSea, iSkirmish, 
iLightEscort, iWork, iMissionary) = range(iNumUnitRoles)

# Promotions
iMercenary = 81
iDesertAdaptation = 82
iSteppeAdaptation = 83
iVolunteer = 84


iNumBonuses = 54
(iAluminium, iAmber, iCamel, iCitrus, iCoal, iCopper, iDates, iHorse, iIron, iMarble,
iOil, iStone, iUranium, iBanana, iClam, iCorn, iCow, iCrab, iDeer, iFish,
iPig, iPotato, iRice, iSheep, iWheat, iCocoa, iCoffee, iCotton, iDye, iFur,
iGems, iGold, iIncense, iIvory, iJade, iMillet, iObsidian, iOlives, iOpium, iPearls,
iRareEarths, iRubber, iSalt, iSilk, iSilver, iSpices, iSugar, iTea, iTobacco, iWine,
iWhales, iSoccer, iSongs, iMovies) = range(iNumBonuses)

iNumBonusVarieties = 19
(iDyeCochineal, iDyeMurex, iDyeHenna, iSpicesCinnamon, iSpicesNutmeg, iSpicesSaffron, iSpicesVanilla, iGemsTurquoise, iGemsDiamonds, iGemsRuby, iGemsSapphire, 
iGemsEmeralds, iSheepLlama, iSheepBlack, iCowBrown, iPigFurry, iIvoryAfrican, iCitrusOranges, iCrabShrimp) = range(iNumBonuses, iNumBonuses + iNumBonusVarieties)


iNumBuildings = 148
(iPalace, iBarracks, iKalliu, iSoldattorp, iIkhanda, iGranary, iTannery, iPaganTemple, iWeaver, iMbwadi, 
iMonument, iObelisk, iMenhir, iStele, iCandi, iEdict, iMalae, iMudbrickPyramid, iTotemPole, iWalls, 
iDun, iStable, iOrtege, iLibrary, iEdubba, iTaixue, iKyaung, iCalmecac, iHarbor, iAqueduct, 
iQanat, iBaray, iNoria, iStepwell, iTheatre, iOdeon, iWaterPuppetTheatre, iHippodrome, iPavilion, iArena, 
iBallCourt, iCharreadaArena, iSambadrome, iGarden, iLighthouse, iGudang, iTradingPost, iVolok, iJeweller, iGlassmaker, 
iObsidianWorkshop, iMarket, iForum, iCaravanserai, iWangara, iSouk, iFloatingMarket, iJail, iDivan, iOstrog, 
iBath, iReservoir, iHammam, iForge, iBloomeryBuilding, iArtStudio, iCastle, iCitadel, iIslandFort, iPharmacy, 
iAlchemist, iGrocer, iPostOffice, iTambo, iWharf, iCoffeehouse, iSalon, iChocolaterie, iBank, iPiaohao, 
iConstabulary, iMountedPolice, iCustomsHouse, iFeitoria, iFunduq, iUniversity, iSeowon, iGompa, iCivicSquare, iGopuram, 
iRathaus, iSejmik, iSewer, iStarFort, iEstate, iMausoleum, iHacienda, iDrydock, iLevee, iPolder, 
iObservatory, iWarehouse, iCourthouse, iExchequer, iFactory, iAssemblyPlant, iZaibatsu, iDistillery, iPark, iBagh, 
iCoalPlant, iRailwayStation, iLaboratory, iCsiro, iAbattoir, iColdStoragePlant, iGrainSilo, iNewsPress, iGasPlant, iIndustrialPark, 
iOilDepot, iCinema, iHospital, iSupermarket, iPublicTransportation, iDepartmentStore, iMall, iBroadcastTower, iIntelligenceAgency, iWaterworks, 
iElectricalGrid, iAirport, iBunker, iBombShelters, iHydroPlant, iSecurityBureau, iStadium, iContainerTerminal, iNuclearPlant, iDiagnosticsCenter, 
iSupercomputer, iHotel, iRecyclingCenter, iLogisticsCenter, iSolarPlant, iFiberNetwork, iAutomatedFactory, iVerticalFarm) = range(iNumBuildings)

iNumReligiousBuildings = 40
iFirstReligiousBuilding = iNumBuildings
iNumBuildings += iNumReligiousBuildings
(iJewishTemple, iJewishCathedral, iJewishMonastery, iJewishShrine, iOrthodoxTemple, iOrthodoxCathedral, iOrthodoxMonastery, iOrthodoxShrine, iCatholicTemple, iCatholicCathedral, 
iCatholicMonastery, iCatholicShrine, iProtestantTemple, iProtestantCathedral, iProtestantMonastery, iProtestantShrine, iIslamicTemple, iIslamicCathedral, iIslamicMonastery, iIslamicShrine, 
iHinduTemple, iHinduCathedral, iHinduMonastery, iHinduShrine, iBuddhistTemple, iBuddhistCathedral, iBuddhistMonastery, iBuddhistShrine, iConfucianTemple, iConfucianCathedral, 
iConfucianMonastery, iConfucianShrine, iTaoistTemple, iTaoistCathedral, iTaoistMonastery, iTaoistShrine, iZoroastrianTemple, iZoroastrianCathedral, iZoroastrianMonastery, iZoroastrianShrine) = range(iFirstReligiousBuilding, iNumBuildings)

iNumNationalWonders = 19
iFirstNationalWonder = iNumBuildings
iNumBuildings += iNumNationalWonders
(iAcademy, iAdministrativeCenter, iManufactory, iArmoury, iMuseum, iStockExchange, iTradingCompanyBuilding, iIberianTradingCompanyBuilding, iNationalMonument, iNationalTheatre, 
iNationalGallery, iNationalCollege, iMilitaryAcademy, iSecretService, iIronworks, iRedCross, iNationalPark, iCentralBank, iSpaceport) = range(iFirstNationalWonder, iNumBuildings)

iNumGreatWonders = 140 # different from DLL constant because that includes national wonders
iFirstWonder = iNumBuildings
iNumBuildings += iNumGreatWonders
(iGreatSphinx, iPyramids, iOracle, iGreatWall, iIshtarGate, iTerracottaArmy, iHangingGardens, iGreatCothon, iDujiangyan, iApadanaPalace, 
iColossus, iGreatMausoleum, iAquaAppia, iParthenon, iPyramidOfTheSun, iStatueOfZeus, iTempleOfArtemis, iGreatLighthouse, iMoaiStatues, iFlavianAmphitheatre, 
iPantheon, iAlKhazneh, iTempleOfKukulkan, iMachuPicchu, iGreatLibrary, iFloatingGardens, iGondeshapur, iJetavanaramaya, iNalanda, iTheodosianWalls, 
iHagiaSophia, iBorobudur, iMezquita, iShwedagonPaya, iMountAthos, iIronPillar, iPrambanan, iSalsalBuddha, iCheomseongdae, iHimejiCastle, 
iGrandCanal, iWatPreahPisnulok, iKhajuraho, iGreatAdobeMosque, iSpiralMinaret, iDomeOfTheRock, iHouseOfWisdom, iKrakDesChevaliers, iMonolithicChurch, iUniversityOfSankore, 
iNotreDame, iOldSynagogue, iSaintSophia, iSilverTreeFountain, iSantaMariaDelFiore, iAlamut, iSanMarcoBasilica, iSistineChapel, iPorcelainTower, iTopkapiPalace, 
iKremlin, iSaintThomasChurch, iVijayaStambha, iGurEAmir, iRedFort, iTajMahal, iForbiddenPalace, iVersailles, iBlueMosque, iEscorial, 
iTorreDeBelem, iPotalaPalace, iOxfordUniversity, iHarmandirSahib, iSaintBasilsCathedral, iBourse, iItsukushimaShrine, iImageOfTheWorldSquare, iLouvre, iEmeraldBuddha, 
iShalimarGardens, iTrafalgarSquare, iHermitage, iGuadalupeBasilica, iSaltCathedral, iAmberRoom, iStatueOfLiberty, iBrandenburgGate, iAbbeyMills, iBellRockLighthouse, 
iChapultepecCastle, iEiffelTower, iWestminsterPalace, iTriumphalArch, iMenloPark, iCrystalPalace, iTsukijiFishMarket, iBrooklynBridge, iHollywood, iEmpireStateBuilding, 
iLasLajasSanctuary, iPalaceOfNations, iMoleAntonelliana, iNeuschwanstein, iFrontenac, iWembley, iLubyanka, iCristoRedentor, iMetropolitain, iNobelPrize, 
iGoldenGateBridge, iBletchleyPark, iSagradaFamilia, iTiananmenSquare, iCERN, iItaipuDam, iGraceland, iCNTower, iPentagon, iUnitedNations, 
iCrystalCathedral, iMotherlandCalls, iBerlaymont, iWorldTradeCenter, iAtomium, iIronDome, iHarbourOpera, iLotusTemple, iFloralisGenerica, iGlobalSeedVault, 
iGardensByTheBay, iBurjKhalifa, iHubbleSpaceTelescope, iChannelTunnel, iSkytree, iOrientalPearlTower, iDeltaWorks, iSpaceElevator, iLargeHadronCollider, iITER) = range(iFirstWonder, iNumBuildings)

iTemple = iJewishTemple #generic
iCathedral = iJewishCathedral #generic
iMonastery = iJewishMonastery #generic
iShrine = iJewishShrine #generic

iPlague = iNumBuildings
iNumBuildingsPlague = iNumBuildings+1

#Civics
iNumCivics = 42
(iChiefdom, iDespotism, iMonarchy, iRepublic, iElective, iStateParty, iDemocracy,
iPersonalism, iCitizenship, iVassalage, iTheocracy, iBureaucracy, iStratocracy, iConstitution,
iTraditionalism, iSlavery, iManorialism, iCasteSystem, iIndividualism, iTotalitarianism, iEgalitarianism,
iReciprocity, iRedistribution, iMerchantTrade, iRegulatedTrade, iFreeEnterprise, iCentralPlanning, iPublicWelfare,
iAnimism, iDeification, iClergy, iSyncretism, iMonasticism, iFanaticism, iSecularism,
iKinship, iThalassocracy, iHegemony, iIsolationism, iColonialism, iNationhood, iMultilateralism) = range(iNumCivics)

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
iParameterVassals, iParameterDefensivePacts, iParameterRelations, iParameterNationhood, iParameterFanaticism, iParameterMultilateralism,			# Foreign
iParameterWarSuccess, iParameterWarWeariness, iParameterBarbarianLosses) = range(iNumStabilityParameters)						# Military

#Regions
iNumRegions = 85
(rBritain, rIreland, rFrance, rIberia, rItaly, rLowerGermany, rCentralEurope, rBalkans, rGreece, rPoland,
rBaltics, rScandinavia, rRuthenia, rPonticSteppe, rEuropeanArctic, rUrals, rAnatolia, rCaucasus, rLevant, rMesopotamia,
rArabia, rEgypt, rNubia, rMaghreb, rPersia, rKhorasan, rTransoxiana, rSindh, rPunjab, rRajputana,
rHindustan, rBengal, rDeccan, rDravida, rIndochina, rIndonesia, rPhilippines, rSouthChina, rNorthChina, rKorea,
rJapan, rTibet, rTarimBasin, rMongolia, rManchuria, rAmur, rCentralAsianSteppe, rSiberia, rAustralia, rOceania,
rEthiopia, rHornOfAfrica, rSwahiliCoast, rGreatLakes, rZambezi, rMadagascar, rCape, rKalahari, rCongo, rGuinea, 
rSahel, rSahara, rAtlanticSeaboard, rDeepSouth, rMidwest, rGreatPlains, rAridoamerica, rCalifornia, rCascadia, rOntario, 
rQuebec, rMaritimes, rAmericanArctic, rCaribbean, rMesoamerica, rCentralAmerica, rNewGranada, rAndes, rAmazonia, rBrazil, 
rSouthernCone, rAntarctica, rHinduKush, rRussia, rVolga) = range(iNumRegions)

iNumWaterRegions = 87
(rMediterraneanSea, rBlackSea, rCaspianSea, rBalticSea, rNorthSea, rAtlanticOcean, rCaribbeanSea, rGulfOfMexico, rHudsonBay, rArcticOcean,
rRedSea, rArabianSea, rPersianGulf, rBayOfBengal, rIndianOcean, rAustralasianSea, rSouthChinaSea, rEastChinaSea, rSeaOfJapan, rSeaOfOkhotsk, 
rBeringSea, rPacificOcean, rSouthernOcean, rVanern, rVattern, rInari, rPaijanne, rOulu, rSaimaa, rPeipus, 
rLadoga, rOnega, rVan, rSevan, rUrmia, rAralSea, rTengiz, rBalkhash, rIssykKul, rAlakol, 
rZaysan, rUvs, rKhovsgol, rBaikal, rTaymyr, rHulun, rQinghai, rLopNur, rSiling, rDongting, 
rPoyang, rTai, rTonleSap, rSetoInlandSea, rEyre, rChad, rTana, rTurkana, rNyanza, rMwitanzege, 
rRweru, rTanganyika, rMweru, rBangweulu, rRukwa, rMalawi, rGreatBear, rTidee, rAthabasca, rReindeer, 
rDubawt, rBaker, rWinnipeg, rSuperior, rMichigan, rHuron, rErie, rLakeOntario, rMistassini, rLobstick, 
rGreatSalt, rNicaragua, rTiticaca, rMarChiquita, rKhanka, rZabuye, rMaiNdombe) = range(100, 100 + iNumWaterRegions)

lEuropeProper = [rBritain, rIreland, rFrance, rIberia, rItaly, rLowerGermany, rCentralEurope, rBalkans, rGreece, rPoland, rBaltics, rScandinavia, rRuthenia, rPonticSteppe, rRussia, rVolga]
lEuropeAsia = [rEuropeanArctic, rUrals, rSiberia]
lMiddleEast = [rAnatolia, rCaucasus, rLevant, rMesopotamia, rArabia, rPersia, rKhorasan, rTransoxiana]
lIndia = [rSindh, rPunjab, rRajputana, rHindustan, rBengal, rDeccan, rDravida]
lEastAsia = [rSouthChina, rNorthChina, rKorea, rJapan, rTibet, rTarimBasin, rMongolia, rManchuria, rAmur, rCentralAsianSteppe]
lSouthEastAsia = [rIndochina, rIndonesia, rPhilippines]
lNorthAfrica = [rEgypt, rNubia, rMaghreb]
lSubSaharanAfrica = [rEthiopia, rHornOfAfrica, rSwahiliCoast, rGreatLakes, rZambezi, rMadagascar, rCape, rKalahari, rCongo, rGuinea, rSahel, rSahara]
lSouthAmerica = [rNewGranada, rAndes, rAmazonia, rBrazil, rSouthernCone]
lCentralAmerica = [rCaribbean, rMesoamerica, rCentralAmerica]
lNorthAmerica = [rAtlanticSeaboard, rDeepSouth, rMidwest, rGreatPlains, rAridoamerica, rCalifornia, rCascadia, rOntario, rQuebec, rMaritimes, rAmericanArctic]
lOceania = [rAustralia, rOceania]

lEurope = lEuropeProper + lEuropeAsia
lAfrica = lNorthAfrica + lSubSaharanAfrica
lSouthAsia = lIndia + lSouthEastAsia
lAsia = lMiddleEast + lSouthAsia + lEastAsia
lAmerica = lSouthAmerica + lCentralAmerica + lNorthAmerica

lNewWorld = lAmerica + lOceania

lLateColonialRegions = lAfrica + lSouthAsia + lEastAsia + [rLevant, rMesopotamia, rArabia, rPersia, rKhorasan, rTransoxiana]

dCivGroupRegions = {
	iCivGroupEurope: lEurope,
	iCivGroupEastAsia: lEastAsia,
	iCivGroupSouthAsia: lSouthAsia,
	iCivGroupMiddleEast: lMiddleEast,
	iCivGroupAfrica: lAfrica,
	iCivGroupAmerica: lAmerica,
}

#Projects

iNumProjects = 22
(iManhattanProject, iTheInternet, iHumanGenome, iSDI, iGPS, iGreatFirewall, iISS, iBallisticMissile, iFirstSatellite, iManInSpace, 
iLunarLanding, iGoldenRecord, iMarsMission, iLunarColony, iInterstellarProbe, iMarsFraming, iMarsPowerSource, iMarsExtractor, iMarsHabitat, iMarsHydroponics, 
iMarsLaboratory, iMarsControlCenter) = range(iNumProjects)

lMarsBaseComponents = [iMarsFraming, iMarsPowerSource, iMarsExtractor, iMarsHabitat, iMarsHydroponics, iMarsLaboratory, iMarsControlCenter]

#Eras

iNumEras = 7
(iAncient, iClassical, iMedieval, iRenaissance, iIndustrial, iGlobal, iDigital) = range (iNumEras)

# Culture

iNumCultureLevels = 7
(iCultureLevelNone, iCultureLevelPoor, iCultureLevelFledgling, iCultureLevelDeveloping, iCultureLevelRefined, iCultureLevelInfluential, iCultureLevelLegendary) = range(iNumCultureLevels)


#Improvements

iNumImprovements = 32
(iLandWorked, iWaterWorked, iCityRuins, iHut, iFarm, iPaddyField, iFishingBoats, iHarvestBoats, iOceanFishery, iWhalingBoats, 
iMine, iSlaveMine, iWorkshop, iLumbermill, iWindmill, iWatermill, iPlantation, iSlavePlantation, iQuarry, iPasture, 
iCamp, iWell, iOffshorePlatform, iOrchard, iCottage, iHamlet, iVillage, iTown, iFort, iForestPreserve, 
iMarinePreserve, iSolarCollector) = range(iNumImprovements)

iNumRoutes = 4
(iRouteRoad, iRouteRailroad, iRouteRomanRoad, iRouteHighway) = range(iNumRoutes)

#feature & terrain

iNumFeatures = 12
(iSeaIce, iJungle, iOasis, iFloodPlains, iForest, iMud, iCape, iIslands, iRainforest, iFallout, 
iTaiga, iSavanna) = range(iNumFeatures)

iNumTerrains = 19
(iGrass, iPlains, iDesert, iTundra, iSnow, iCoast, iOcean, iTerrainPeak, iTerrainHill, iMarsh, 
iLagoon, iArcticCoast, iSemidesert, iSteppe, iMoorland, iSaltFlat, iSaltLake, iAtoll, iTerrainSavanna) = range(iNumTerrains)

#Plague
iImmunity = 20

# Victory
iVictoryPaganism = 10
iVictorySecularism = 11


#leaders
iNumLeaders = 154
(iLeaderBarbarian, iNativeLeader, iIndependentLeader, iDjoser, iHatshepsut, iRamesses, iPtolemy, iSargon, iHammurabi, iWentAntu, 
iAshurbanipal, iWu, iTaizong, iHongwu, iMao, iMursili, iPericles, iAlexanderTheGreat, iGeorge, iAsoka, 
iChandragupta, iShivaji, iGandhi, iHiram, iHannibal, iTaharqa, iAmanirena, iAhoeitu, iCyrus, iDarius, 
iShapur, iBrennus, iBoudica, iBrianBoru, iScipio, iJuliusCaesar, iAugustus, iPacal, iRajendra, iKrishnaDevaRaya, 
iEzana, iZaraYaqob, iMenelik, iTopiltzin, iKanishka, iWangKon, iSejong, iNeangNeak, iSuryavarman, iDinga, 
iMansaMusa, iJustinian, iBasil, iCharlemagne, iLouis, iNapoleon, iDeGaulle, iSriJayanasa, iTunPerak, iKammu, 
iOdaNobunaga, iMeiji, iCanute, iHaakon, iChristian, iGerhardsen, iBumin, iAlpArslan, iTamerlane, iHarun, 
iSongtsen, iLobsangGyatso, iRahman, iYaqub, iHayamWuruk, iSuharto, iIsabella, iPhilip, iFranco, iAlfred, 
iElizabeth, iVictoria, iChurchill, iBarbarossa, iCharles, iFrancis, iAnawrahta, iBayinnaung, iYaroslav, iKhmelnytsky, 
iLeLoi, iHoChiMinh, iDawud, iSaladin, iBaibars, iMuhammadAli, iNasser, iCasimir, iSobieski, iPilsudski, 
iWalesa, iAfonso, iJoao, iMaria, iHuaynaCapac, iCastilla, iLorenzo, iCavour, iMussolini, iGenghisKhan, 
iKublaiKhan, iMontezuma, iTughluq, iAkbar, iBhutto, iUzbeg, iNaresuan, iMongkut, iGustav, iErlander, 
iIvan, iPeter, iCatherine, iAlexanderI, iStalin, iMehmed, iSuleiman, iAtaturk, iMbemba, iAbbas, 
iKhomeini, iWillemVanOranje, iWilliam, iKangxi, iFrederick, iBismarck, iHitler, iIbnSaud, iWashington, iLincoln, 
iRoosevelt, iSanMartin, iPeron, iJuarez, iSantaAnna, iCardenas, iBolivar, iPedro, iVargas, iLeopold, 
iCurtin, iMacDonald, iTrudeau, iSittingBull) = range(iNumLeaders)

dResurrectionLeaders = CivDict({
	iChina : iHongwu,
	iIndia : iShivaji,
})

# update DLL constants when this changes
iNumPeriods = 29
(iPeriodPtolemaicEgypt, iPeriodMakuria, iPeriodMing, iPeriodMaratha, iPeriodModernGreece, 
iPeriodCarthage, iPeriodInsularCelts, iPeriodVijayanagara, iPeriodByzantineConstantinople, iPeriodNationalFrance, 
iPeriodMeiji, iPeriodDenmark, iPeriodNorway, iPeriodSeljuks, iPeriodUzbeks, 
iPeriodSaudi, iPeriodMorocco, iPeriodSpain, iPeriodAustria, iPeriodUnitedKingdom, 
iPeriodGreatBritain, iPeriodYuan, iPeriodPeru, iPeriodLateInca, iPeriodModernItaly, 
iPeriodPakistan, iPeriodOttomanConstantinople, iPeriodQing, iPeriodModernGermany) = range(iNumPeriods)

iNumImpacts = 5
(iImpactMarginal, iImpactLimited, iImpactSignificant, iImpactCritical, iImpactPlayer) = range(iNumImpacts)

lTradingCompanyCivs = [iSpain, iFrance, iEngland, iPortugal, iNetherlands]
lLateColonyCivs = lTradingCompanyCivs + [iGermany]

lMongolCivs = [iPersia, iByzantium, iTurks, iArabia, iRus]

iNumScenarios = 5
(i3000BC, i600AD, i1500AD, i1700AD, i1815AD) = range(iNumScenarios)

lScenarioStartYears = [-3000, 600, 1500, 1700, 1815]

# Stability overlay and editor
iNumPlotStabilityTypes = 4
(iCoreArea, iHistoricalArea, iConquestArea, iForeignArea) = range(iNumPlotStabilityTypes)
lStabilityColors = ["COLOR_CYAN", "COLOR_GREEN", "COLOR_YELLOW", "COLOR_RED"]
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