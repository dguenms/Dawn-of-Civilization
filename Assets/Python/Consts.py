# Rhye's and Fall of Civilization - Constants
# globals

from CvPythonExtensions import *
gc = CyGlobalContext()

iWorldX = 124
iWorldY = 68

# initialise player variables to player IDs from WBS
iNumPlayers = 54
(iEgypt, iChina, iBabylonia, iHarappa, iGreece, iIndia, iCarthage, iPolynesia, iPersia, iRome, 
iTamils, iEthiopia, iVietnam, iKorea, iMaya, iByzantium, iJapan, iVikings, iArabia, iTibet, iIndonesia,
iMoors, iSpain, iFrance, iKhmer, iEngland, iHolyRome, iRussia, iPhilippines, iSwahili, iMamluks, iMali, iPoland, iZimbabwe, iPortugal, 
iInca, iItaly, iNigeria, iMongolia, iAztecs, iMughals, iTurkey, iThailand, iCongo, iSweden, iNetherlands, iManchuria,
iGermany, iAmerica, iArgentina, iBrazil, iAustralia, iBoers, iCanada) = range(iNumPlayers)

(pEgypt, pChina, pBabylonia, pHarappa, pGreece, pIndia, pCarthage, pPolynesia, pPersia, pRome, 
pTamils, pEthiopia, pVietnam, pKorea, pMaya, pByzantium, pJapan, pVikings, pArabia, pTibet, pIndonesia, 
pMoors, pSpain, pFrance, pKhmer, pEngland, pHolyRome, pRussia, pPhilippines, pSwahili, pMamluks, pMali, pPoland, pZimbabwe, pPortugal, 
pInca, pItaly, pNigeria, pMongolia, pAztecs, pMughals, pTurkey, pThailand, pCongo, pSweden, pNetherlands, pManchuria, 
pGermany, pAmerica, pArgentina, pBrazil, pAustralia, pBoers, pCanada) = [gc.getPlayer(i) for i in range(iNumPlayers)]

(teamEgypt, teamChina, teamBabylonia, teamHarappa, teamGreece, teamIndia, teamCarthage, teamPolynesia, teamPersia, teamRome, 
teamTamils, teamEthiopia, teamVietnam, teamKorea, teamMaya, teamByzantium, teamJapan, teamVikings, teamArabia, teamTibet, teamIndonesia,
teamMoors, teamSpain, teamFrance, teamKhmer, teamEngland, teamHolyRome, teamRussia, teamPhilippines, teamSwahili, teamMamluks, teamMali, teamPoland, teamZimbabwe, teamPortugal, 
teamInca, teamItaly, teamNigeria, teamMongolia, teamAztecs, teamMughals, teamTurkey, teamThailand, teamCongo, teamSweden, teamNetherlands, teamManchuria, 
teamGermany, teamAmerica, teamArgentina, teamBrazil, teamAustralia, teamBoers, teamCanada) = [gc.getTeam(i) for i in range(iNumPlayers)]

iHolland = iNetherlands
iDelhi = iMughals
iSiam = iThailand
iPhoenicia = iCarthage
iHRE = iHolyRome
iAustria = iHolyRome
iPrussia = iGermany
iSouthAfrica = iBoers

iNumMajorPlayers = iNumPlayers
iNumActivePlayers = iNumPlayers

iIndependent = iNumPlayers
iIndependent2 = iNumPlayers+1
iNative = iNumPlayers+2
iCeltia = iNumPlayers+3
iSeljuks = iNumPlayers+4
iNumTotalPlayers = iNumPlayers+5
iBarbarian = iNumPlayers+5
iNumTotalPlayersB = iBarbarian+1

(pIndependent, pIndependent2, pNative, pCeltia, pSeljuks, pBarbarian) = [gc.getPlayer(i) for i in range(iIndependent, iNumTotalPlayersB)]
(teamIndependent, teamIndependent2, teamNative, teamCeltia, teamSeljuks, teamBarbarian) = [gc.getTeam(i) for i in range(iIndependent, iNumTotalPlayersB)]

l0Array =       [0 for i in range(iNumPlayers)]
l0ArrayActive = [0 for i in range(iNumPlayers)]
l0ArrayTotal =  [0 for i in range(iNumTotalPlayers)]

lm1Array =      [-1 for i in range(iNumPlayers)]

# civilizations, not players
iNumCivilizations = 67
(iCivAmerica, iCivArabia, iCivArgentina, iCivAustralia, iCivAztec, iCivBabylonia, iCivBoers, iCivBrazil, iCivByzantium, iCivCanada, iCivCarthage, iCivCelt, 
iCivChina, iCivColombia, iCivEgypt, iCivEngland, iCivEthiopia, iCivFrance, iCivGermany, iCivGreece, iCivHarappa, iCivHolyRome, 
iCivInca, iCivIndia, iCivIndonesia, iCivIran, iCivItaly, iCivJapan, iCivKhmer, iCivKongo, iCivKorea, iCivMali, iCivMamluks, iCivManchuria,
iCivMaya, iCivMexico, iCivMongols, iCivMoors, iCivMughals, iCivNativeAmericans, iCivNetherlands, iCivNigeria, iCivOttomans, iCivPersia, iCivPhilippines, iCivPoland, 
iCivPolynesia, iCivPortugal, iCivRome, iCivRussia, iCivSeljuks, iCivSpain, iCivSumeria, iCivSwahili, iCivSweden, iCivTamils, iCivThailand, iCivTibet, iCivVietnam,
iCivVikings, iCivZimbabwe, iCivZulu, iCivIndependent, iCivIndependent2, iCivNative, iCivMinor, iCivBarbarian) = range(iNumCivilizations)

iCivTurkey = iCivOttomans
iCivCongo = iCivKongo
iCivAztecs = iCivAztec
iCivCeltia = iCivCelt
iCivSouthAfrica = iCivBoers

#for Congresses and Victory
lCivGroups = [[iGreece, iRome, iByzantium, iVikings, iMoors, iSpain, iFrance, iEngland, iHolyRome, iRussia, iNetherlands, iItaly, iPoland, iPortugal, iGermany, iSweden],  #Euros
		[iIndia, iChina, iHarappa, iPolynesia, iPersia, iJapan, iTamils, iKorea, iByzantium, iTibet, iKhmer, iIndonesia, iRussia, iMongolia, iMughals, iThailand, iVietnam, iManchuria, iPhilippines], #Asian
		[iEgypt, iBabylonia, iPersia, iByzantium, iArabia, iTurkey, iCarthage, iMamluks], #MiddleEastern
		[iEgypt, iGreece, iCarthage, iRome, iByzantium, iMoors], #Mediterranean
		[iEgypt, iCarthage, iEthiopia, iMali, iCongo, iSwahili, iZimbabwe, iNigeria, iBoers], #African
		[iMaya, iInca, iAztecs, iAmerica, iArgentina, iBrazil, iAustralia, iCanada]] #American

lCivStabilityGroups = [[iVikings, iSpain, iFrance, iEngland, iHolyRome, iRussia, iNetherlands, iPoland, iPortugal, iItaly, iGermany, iSweden],  #Euros
		[iIndia, iChina, iHarappa, iPolynesia, iJapan, iKorea, iTibet, iKhmer, iIndonesia, iMongolia, iThailand, iTamils, iVietnam, iManchuria, iPhilippines], #Asian
		[iBabylonia, iPersia, iArabia, iTurkey, iMughals, iMamluks], #MiddleEastern
		[iEgypt, iGreece, iCarthage, iRome, iEthiopia, iByzantium, iMoors, iMali, iCongo, iZimbabwe, iNigeria, iSwahili, iBoers], #Mediterranean
		[iMaya, iInca, iAztecs, iAmerica, iArgentina, iBrazil, iAustralia, iCanada]] #American
		
lTechGroups = [[iRome, iGreece, iByzantium, iVikings, iSpain, iFrance, iEngland, iHolyRome, iRussia, iNetherlands, iPoland, iPortugal, iItaly, iGermany, iAmerica, iArgentina, iBrazil, iCanada, iSweden, iAustralia, iBoers], #Europe and NA
	       [iEgypt, iBabylonia, iHarappa, iIndia, iCarthage, iPersia, iEthiopia, iArabia, iMoors, iMali, iTurkey, iMughals, iTamils, iCongo, iMamluks, iNigeria, iSwahili, iZimbabwe], #Middle East
	       [iChina, iKorea, iJapan, iTibet, iKhmer, iIndonesia, iMongolia, iThailand, iManchuria, iVietnam, iPhilippines], #Far East
	       [iPolynesia, iMaya, iInca, iAztecs]] #Native America


lCivBioOldWorld = [iEgypt, iIndia, iChina, iBabylonia, iHarappa, iGreece, iPolynesia, iPersia, iCarthage, iRome, iJapan, iTamils, 
		   iEthiopia, iKorea, iByzantium, iVikings, iArabia, iTibet, iKhmer, iIndonesia, iMoors, iSpain, iFrance, iEngland, iHolyRome, iRussia, 
		   iNetherlands, iMali, iTurkey, iPoland, iPortugal, iItaly, iMongolia, iAmerica, iMughals, iThailand, iCongo, iGermany, iSweden,
		   iAustralia, iBoers, iMamluks, iManchuria, iNigeria, iPhilippines, iSwahili, iVietnam, iZimbabwe,
		   iIndependent, iIndependent2, iCeltia, iBarbarian]
lCivBioNewWorld = [iMaya, iInca, iAztecs] #, iNative]


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
iNumMinorCities = 38

# scripted conquerors
iNumConquests = 12

#neighbours
lNeighbours = [
[iBabylonia, iGreece, iPersia, iCarthage, iRome, iEthiopia, iByzantium, iArabia, iMoors, iTurkey, iMamluks], #Egypt
[iIndia, iJapan, iVietnam, iKorea, iTibet, iKhmer, iMongolia, iThailand, iManchuria, iPhilippines], #China
[iEgypt, iGreece, iPersia, iTurkey, iMongolia, iCarthage, iByzantium], #Babylonia
[iIndia, iPersia, iTamils, iTibet, iMughals], #Harappa
[iPersia, iCarthage, iRome, iByzantium, iHolyRome, iRussia, iTurkey, iItaly], #Greece
[iChina, iHarappa, iPersia, iTamils, iTibet, iKhmer, iMongolia, iMughals, iThailand, iVietnam], #India
[iEgypt, iGreece, iRome, iSpain, iMali, iPortugal, iBabylonia, iPersia, iArabia, iMoors, iTurkey, iItaly, iMamluks], #Carthage
[], # Polynesia
[iIndia, iBabylonia, iHarappa, iGreece, iByzantium, iTurkey, iMongolia, iCarthage, iMughals, iMamluks], #Persia
[iEgypt, iBabylonia, iGreece, iCarthage, iSpain, iFrance, iHolyRome, iPortugal, iItaly, iGermany], #Rome
[iHarappa, iIndia, iKhmer, iIndonesia, iMughals, iThailand, iVietnam, iPhilippines], #Tamils
[iEgypt, iArabia, iMali, iCongo, iMamluks, iNigeria, iSwahili, iZimbabwe], #Ethiopia
[iChina, iKhmer, iThailand, iTamils, iIndia, iIndonesia, iTibet, iPhilippines], #Vietnam
[iChina, iKorea, iMongolia, iManchuria], #Korea
[iSpain, iInca, iAztecs, iAmerica], #Maya
[iEgypt, iBabylonia, iGreece, iPersia, iArabia, iRussia, iMamluks], #Byzantium
[iChina, iKorea, iKhmer, iMongolia, iThailand, iManchuria, iPhilippines], #Japan
[iFrance, iEngland, iHolyRome, iRussia, iPoland, iSweden, iNetherlands, iGermany], #Vikings
[iEgypt, iBabylonia, iPersia, iEthiopia, iByzantium, iTurkey, iCarthage, iMamluks], #Arabia
[iChina, iHarappa, iIndia, iMongolia, iMughals, iVietnam], #Tibet
[iIndia, iJapan, iKhmer, iThailand, iTamils, iPhilippines, iVietnam], #Indonesia
[iEgypt, iSpain, iPortugal, iMali, iMamluks], #Moors
[iCarthage, iRome, iMoors, iFrance, iEngland, iPortugal], #Spain
[iRome, iVikings, iSpain, iEngland, iHolyRome, iNetherlands, iPortugal, iItaly, iGermany], #France
[iIndia, iChina, iTamils, iJapan, iIndonesia, iThailand, iPhilippines, iVietnam], #Khmer
[iRome, iVikings, iSpain, iFrance, iHolyRome, iNetherlands, iGermany], #England
[iRome, iVikings, iFrance, iEngland, iNetherlands, iItaly, iPoland, iSweden, iGermany], #Holy Rome
[iPersia, iByzantium, iVikings, iPoland, iTurkey, iMongolia, iSweden, iGermany], #Russia
[iChina, iTamils, iJapan, iIndonesia, iKhmer, iThailand, iVietnam], #Philippines
[iEthiopia, iMali, iCongo, iNigeria, iZimbabwe], # Swahili
[iPersia, iCarthage, iEthiopia, iByzantium, iArabia, iMoors, iTurkey, iEgypt], #Mamluks
[iEgypt, iCarthage, iEthiopia, iMoors, iCongo, iNigeria, iSwahili, iZimbabwe], #Mali
[iVikings, iHolyRome, iRussia, iSweden, iGermany], #Poland
[iEthiopia, iMali, iCongo, iNigeria, iSwahili], #Zimbabwe
[iCarthage, iRome, iSpain, iFrance], #Portugal
[iSpain, iAztecs, iAmerica, iArgentina, iBrazil], #Inca
[iGreece, iCarthage, iRome, iFrance, iHolyRome], #Italy
[iMali, iCongo, iEthiopia, iSwahili, iZimbabwe], #Nigeria
[iIndia, iChina, iPersia, iJapan, iKorea, iTibet, iRussia, iTurkey, iManchuria], #Mongolia
[iSpain, iInca, iAmerica], #Aztec
[iHarappa, iIndia, iPersia, iTamils, iTibet], #Mughals
[iBabylonia, iGreece, iPersia, iByzantium, iRussia, iMongolia, iCarthage, iMamluks], #Turkey
[iIndia, iChina, iJapan, iIndonesia, iKhmer, iTamils, iPhilippines, iVietnam], #Thailand
[iEthiopia, iMali, iSwahili, iNigeria, iZimbabwe], #Congo
[iVikings, iHolyRome, iRussia, iPoland, iGermany], # Sweden
[iVikings, iFrance, iEngland, iHolyRome, iGermany], #Netherlands
[iRome, iVikings, iFrance, iEngland, iHolyRome, iRussia, iPoland, iSweden, iNetherlands], #Germany
[iChina, iKorea, iJapan, iMongolia], #Manchuria
[iRome, iVikings, iFrance, iEngland, iHolyRome, iRussia, iPoland, iNetherlands], #Germany
[iJapan, iSpain, iFrance, iEngland, iRussia, iInca, iAztecs], #America
[iSpain, iPortugal, iInca, iBrazil], #Argentina
[iSpain, iPortugal, iInca, iArgentina], #Brazil
[iJapan, iIndonesia, iEngland, iNetherlands, iAmerica], #Australia
[iCongo, iEngland, iNetherlands, iPortugal, iEthiopia], #Boers
[iAmerica], #Canada
]

#for stability hit on spawn
lOlderNeighbours = [
[], #Egypt
[], #China
[], #Babylonia
[], #Harappa
[iEgypt, iBabylonia], #Greece
[iHarappa], #India
[iEgypt, iBabylonia], #Carthage
[], # Polynesia
[iEgypt, iBabylonia, iHarappa, iGreece], #Persia
[iEgypt, iGreece, iCarthage], #Rome
[iHarappa, iIndia], #Tamils
[iEgypt], #Ethiopia
[], #Vietnam
[iChina], #Korea
[], #Maya
[iGreece], #Byzantium
[iKorea], #Japan
[], #Vikings
[iEgypt, iPersia, iByzantium], #Arabia
[iChina, iHarappa, iIndia, iVietnam], #Tibet
[iKhmer, iVietnam], #Indonesia
[], #Moors
[iCarthage, iRome], #Spain
[iRome], #France
[iIndia, iVietnam], #Khmer
[], #England
[iGreece, iRome, iVikings], #Holy Rome
[iPersia, iGreece, iByzantium], #Russia
[iIndonesia, iKhmer], # Philippines
[iEthiopia], #Swahili
[iByzantium, iEthiopia, iArabia], #Mamluks
[iCarthage, iEthiopia, iArabia, iMoors], #Mali
[iVikings, iHolyRome], #Poland
[], #Zimbabwe
[iCarthage, iRome], #Portugal
[], #Inca
[iByzantium, iHolyRome], #Italy
[iMali], #Nigeria
[iChina, iJapan, iKorea, iArabia, iTibet, iKhmer, iRussia], #Mongolia
[iMaya], #Aztec
[iHarappa, iIndia, iPersia, iArabia, iTibet], #Mughals
[iBabylonia, iGreece, iPersia, iByzantium, iArabia, iMamluks], #Turkey
[iIndia, iChina, iJapan, iKhmer, iIndonesia, iVietnam, iPhilippines], #Thailand
[iNigeria], #Congo
[iVikings], #Sweden
[iRome, iHolyRome], #Netherlands
[iChina, iMongolia], #Manchuria
[iHolyRome, iPoland], #Germany
[iSpain, iFrance, iEngland, iNetherlands, iPortugal, iAztecs, iMaya], #America
[iSpain, iPortugal, iInca], #Argentina
[iSpain, iPortugal, iInca], #Brazil
[iEngland, iNetherlands], # Australia
[iEngland, iNetherlands], #Boers
[iAmerica], #Canada
]

# civ birth dates

# converted to years - edead
tBirth = (
-3000, # 0, #3000BC			# Egypt
-3000, # 0, #3000BC			# China
-3000, # 0, #3000BC			# Babylonia
-3000,					# Harappa
-1600, # 50, #1600BC			# Greece
-1500, # 0, #3000BC			# India
-1200, # 66, #814BC # Leoreth: 1200 BC	# Carthage
-1000,					# Polynesia
-850, # 84, #844BC			# Persia
-753, # 90, #753BC			# Rome
-300,					# Tamils
-290, # 121, #300BC			# Ethiopia
-257,					# Vietnam
-50,					# Korea
65, # 145, #60AD			# Maya
330,					# Byzantium
525, # 97, #660BC			# Japan
551, # 177, #551AD			# Vikings
620, # 183, #622AD			# Arabia
630,					# Tibet
650,					# Indonesia
711,					# Moors
722, # 193, #718AD			# Spain
750, # 196, #751AD			# France
800, # 187, #657AD			# Khmer
820, # 203, #829AD			# England
840, # 205, #843AD			# Holy Rome
860, # 207, #860AD			# Russia
900,						# Philippines
960, # 218					# Swahili
969,						# Mamluks
989, # 220, #989AD			# Mali
1025,					# Poland
1075,					# Zimbabwe
1130, # 234, #1128AD			# Portugal
1150, # 236, #1150AD			# Inca
1167, # Italy				# Italy
1180,						# Nigeria
1190, # 240, #1190AD			# Mongolia
1195, # 241, #1195AD			# Aztecs
1206,					# Mughals
1280, # 249, #1280AD (1071AD)		# Turkey
1350,					# Thailand
1390,					# Congo
1523,					# Sweden
1580, # 281, #922AD # Leoreth: 1500 AD	# Netherlands
1636,					# Manchuria
1700,					# Germany
1775, # 346, #1775AD #332 for 1733AD	# America
1810,					# Argentina
1822,					# Brazil
1850,					# Australia
1852,					# Boers
1867,	#Canada
#1791,	#Canada
-3000, # 0,
-3000, # 0,
-3000, # 0,
-3000, # 0,
-3000, # 0,
-3000
)

# Leoreth: stability penalty from this date on
tFall = (
-343,					# Egypt
1127,					# China
-539,					# Babylonia
-1700,					# Harappa
-146,					# Greece
600, # end of Gupta Empire		# India
-146,					# Phoenicia
1200,					# Polynesia
651,					# Persia
235, # crisis of the third century	# Rome
1000,					# Tamils
960,					# Ethiopia
602,					# Vietnam
1255, #Mongol invasion			# Korea
900,					# Maya
1204, #fourth crusade			# Byzantium
2020,					# Japan
1300,					# Vikings
900,					# Arabia
1500,					# Tibet
1500,					# Indonesia
1500,					# Moors
2020,					# Spain
2020,					# France
1200, # earlier so that the Thai can spawn # Khmer
2020,					# England
2020, #1648,				# Holy Rome
2020,					# Russia
1570,					# Philippines
1600,					# Swahili
1517,					# Mamluks
1600,					# Mali
1650,					# Poland
1760,					# Zimbabwe
2020,					# Portugal
1533,					# Inca
2020,					# Italy
1897,					# Nigeria
1368,					# Mongolia
1521,					# Aztecs
1640,					# Mughals
2020,					# Turkey
2020,					# Thailand
1800,					# Congo
2020,					# Sweden
2020,					# Netherlands
1912,					# Manchuria
2020,					# Germany
2020,					# America
2020,					# Argentina
2020,					# Brazil
2020,					# Australia
2020,					# Boers
2020)					# Canada

dVictoryYears = {
iCivEgypt : (-850, -100, 170),
iCivChina : (1000, -1, 1800),
iCivBabylonia : (-1, -850, -700),
iCivHarappa : (-1600, -1500, -800),
iCivGreece : (-1, -330, -250),
iCivIndia : (-100, 700, 1200),
iCivCarthage : (-300, -100, 200),
iCivPolynesia : (800, 1000, 1200),
iCivPersia : (140, 350, 350),
iCivRome : (100, 320, -1),
iCivTamils : (800, 1000, 1200),
iCivEthiopia : (-1, 600, 1910),
iCivVietnam : (-1, 1500, 1950),
iCivKorea : (1200, -1, -1),
iCivMaya : (600, 900, -1),
iCivByzantium : (1000, 1200, 1450),
iCivJapan : (1600, 1940, -1),
iCivVikings : (1050, 1100, 1500),
iCivArabia : (1300, 1300, -1),
iCivTibet : (1000, 1400, 1700),
iCivIndonesia : (1300, 1500, 1940),
iCivMoors : (1200, 1300, 1650),
iCivSpain : (-1, 1650, 1650),
iCivFrance : (1700, 1800, 1900),
iCivKhmer : (1200, 1450, 1450),
iCivEngland : (1730, 1800, -1),
iCivHolyRome : (1200, -1, 1700),
iCivRussia : (1920, -1, 1950),
iCivPhilippines : (1400, 1500, 1600),
iCivSwahili : (1500, 1500, 1650),
iCivMamluks : (1300, 1380, 1500),
iCivMali : (1350, 1500, 1700),
iCivPoland : (1400, -1, 1600),
iCivZimbabwe : (1400, 1500, 1700),
iCivPortugal : (1550, 1650, 1700),
iCivInca : (1500, 1550, 1700),
iCivItaly : (1500, 1600, 1930),
iCivNigeria : (1600, 1750, 1950),
iCivMongols : (1300, -1, 1500),
iCivAztec : (1520, 1650, -1),
iCivMughals : (1500, 1660, 1750),
iCivTurkey : (1550, 1700, 1800),
iCivThailand : (1650, 1700, 1900),
iCivCongo : (1650, 1800, -1),
iCivIran : (1650, 1750, 1800),
iCivSweden : (1700, 1800, 1970),
iCivNetherlands : (1745, 1745, 1775),
iCivManchuria : (1800, 1850, -1),
iCivGermany : (1900, 1940, -1),
iCivAmerica : (1900, 1950, 2000),
iCivMexico : (1880, 1940, 1960),
iCivArgentina : (1930, 1960, 2000),
iCivColombia : (1870, 1920, 1950),
iCivBrazil : (1880, -1, 1950),
iCivAustralia : (1950, 1950, -1),
iCivBoers : (1920, 1950, 1980),
iCivCanada : (1920, 1950, 2000),
}

# Leoreth: date-triggered respawn for certain civs
tRebirth = (
-1,				# Egypt
-1,				# China
-1,				# Babylonia
-1,				# Harappa
-1,	# Byzantium		# Greece
-1,				# India
-1,				# Phoenicia
-1,				# Polynesia
#1674,	# Maratha Empire
1501,	# Safavid Persia	# Persia
-1, #1167,	# Italy		# Rome
-1,				# Tamils
-1,				# Ethiopia
-1,				# Vietnam
-1,				# Korea
1814,	# Colombia
-1,				# Byzantium
-1,				# Japan
-1,				# Vikings
-1,				# Arabia
-1,				# Tibet
-1,				# Indonesia
-1,				# Moors
-1,				# Spain
-1,				# France
-1,				# Khmer
-1,				# England
-1,				# Holy Rome
-1,				# Russia
-1,				# Philippines
-1,				# Swahili
-1,				# Mamluks
-1,				# Mali
-1,				# Poland
-1,				# Zimbabwe
-1,				# Portugal
-1,				# Inca
-1,				# Italy	
-1,				# Nigeria
-1,				# Mongolia
1810,	# Mexico
-1,				# Mughals
-1,				# Turkey
-1,				# Thailand
-1,				# Congo
-1,				# Sweden
-1,				# Netherlands
-1,				# Manchuria
-1,				# Germany
-1,				# America
-1,				# Argentina
-1,				# Brazil
-1,				# Australia
-1,				# Boers
-1)				# Canada

# Leoreth: ID of the civilization a player is turned into on rebirth
tRebirthCiv = (
-1,		# Egypt
-1,		# China
-1,		# Babylonia
-1,		# Harappa
-1,		# Greece
-1,		# India
-1,		# Phoenicia
-1,		# Polynesia
iCivIran,	# Persia
iCivItaly,	# Rome
-1,		# Tamils
-1,		# Ethiopia
-1,		# Vietnam
-1,		# Korea
iCivColombia,	# Maya
-1,		# Byzantium
-1,		# Japan
-1,		# Vikings
-1,		# Arabia
-1,		# Tibet
-1,		# Indonesia
-1,		# Moors
-1,		# Spain
-1,		# France
-1,		# Khmer
-1,		# England
-1,		# Holy Rome
-1,		# Russia
-1,		# Philippines
-1,		# Swahili
-1,		# Mamluks
-1,		# Mali
-1,		# Poland
-1,		# Zimbabwe
-1,		# Portugal
-1,		# Inca
-1,		# Italy	
-1,		# Nigeria
-1,		# Mongolia
iCivMexico,	# Aztecs
-1,		# Mughals
-1,		# Turkey
-1,		# Thailand
-1,		# Congo
-1,		# Sweden
-1,		# Netherlands
-1,		# Manchuria
-1,		# Germany
-1,		# America
-1,		# Argentina
-1,		# Brazil
-1,		# Australia
-1,		# Boers
-1,		# Canada
)

tResurrectionIntervals = (
[], #Egypt
[(600, 2020)], #China
[(-3000, -500)], #Babylonia
[],		# Harappa
[(1800, 2020)], #Greece
[(1600, 1800), (1900, 2020)], #India
[(-1000, -150)], #Carthage
[],		# Polynesia
[(220, 650), (1500, 2020)], #Persia
[(-750, 450)], #Rome
[(-300, 600), (1300, 1650)], #Tamils
[(1270, 1520), (1850, 2020)], #Ethiopia
[(950, 1400), (1800, 1945)], #Vietnam
[(1800, 2020)], #Korea
[(0, 800)], #Maya
[(1100, 1280)], #Byzantium
[(1800, 2020)], #Japan
[(1520, 2020)], #Vikings
[(1900, 2020)], #Arabia
[],		#Tibet
[(1900, 2020)], #Indonesia
[(1000, 2020)],	#Moors
[(1700, 2020)], #Spain
[(1700, 2020)], #France
[(1950, 2020)], #Khmer
[(1700, 2020)], #England
[(1800, 2020)], #Holy Rome
[(1280, 1550), (1700, 2020)], #Russia
[(1900, 2020)],	#Philippines
[(1850, 1920)],	#Swahili
[(1800, 2020)], #Mamluks
[(1340, 1590)], #Mali
[(1920, 2020)], #Poland
[],		# Zimbabwe
[(1700, 2020)], #Portugal
[(1800, 1930)], #Inca
[(1820, 2020)], #Italy
[(1700, 2020)],		# Nigeria
[(1910, 2020)], #Mongolia
[], 		#Aztec
[(1940, 2020)], #Mughals
[(1700, 2020)], #Turkey
[(1700, 2020)], #Thailand
[],		#Congo
[(1700, 2020)], #Sweden
[(1700, 2020)], #Netherlands
[],	#Manchuria
[(1840, 2020)], #Germany
[(1770, 2020)], #America
[(1810, 2020)], #Argentina
[(1820, 2020)], #Brazil
[(1850, 2020)], #Australia
[(1852, 2020)], #Boers
[(1867, 2020)], #Canada
)
# edead: tGoals[iGameSpeed][iCiv][iGoal]
# Leoreth: tGoals[reborn][iGameSpeed][iCiv][iGoal]
tGoals1 = (
( # Marathon
("TXT_KEY_UHV_EGY1_MARATHON", "TXT_KEY_UHV_EGY2_MARATHON", "TXT_KEY_UHV_EGY3_MARATHON"),
("TXT_KEY_UHV_CHI1", "TXT_KEY_UHV_CHI2", "TXT_KEY_UHV_CHI3"),
("TXT_KEY_UHV_BAB1", "TXT_KEY_UHV_BAB2_MARATHON", "TXT_KEY_UHV_BAB3_MARATHON"),
("TXT_KEY_UHV_HAR1", "TXT_KEY_UHV_HAR2", "TXT_KEY_UHV_HAR3"),
("TXT_KEY_UHV_GRE1", "TXT_KEY_UHV_GRE2_MARATHON", "TXT_KEY_UHV_GRE3_MARATHON"),
("TXT_KEY_UHV_IND1_MARATHON", "TXT_KEY_UHV_IND2", "TXT_KEY_UHV_IND3"),
("TXT_KEY_UHV_CAR1", "TXT_KEY_UHV_CAR2", "TXT_KEY_UHV_CAR3_MARATHON"),
("TXT_KEY_UHV_PLY1", "TXT_KEY_UHV_PLY2", "TXT_KEY_UHV_PLY3"),
("TXT_KEY_UHV_PER1_MARATHON", "TXT_KEY_UHV_PER2_MARATHON", "TXT_KEY_UHV_PER3_MARATHON"),
("TXT_KEY_UHV_ROM1_MARATHON", "TXT_KEY_UHV_ROM2_MARATHON", "TXT_KEY_UHV_ROM3"),
("TXT_KEY_UHV_TAM1_MARATHON", "TXT_KEY_UHV_TAM2", "TXT_KEY_UHV_TAM3_MARATHON"),
("TXT_KEY_UHV_ETH1", "TXT_KEY_UHV_ETH2_MARATHON", "TXT_KEY_UHV_ETH3"),
("TXT_KEY_UHV_VIE1_MARATHON", "TXT_KEY_UHV_VIE2", "TXT_KEY_UHV_VIE3"),
("TXT_KEY_UHV_KOR1", "TXT_KEY_UHV_KOR2", "TXT_KEY_UHV_KOR3"),
("TXT_KEY_UHV_MAY1_MARATHON", "TXT_KEY_UHV_MAY2", "TXT_KEY_UHV_MAY3"),
("TXT_KEY_UHV_BYZ1_MARATHON", "TXT_KEY_UHV_BYZ2", "TXT_KEY_UHV_BYZ3"),
("TXT_KEY_UHV_JAP1_MARATHON", "TXT_KEY_UHV_JAP2", "TXT_KEY_UHV_JAP3"),
("TXT_KEY_UHV_VIK1", "TXT_KEY_UHV_VIK2", "TXT_KEY_UHV_VIK3_MARATHON"),
("TXT_KEY_UHV_ARA1", "TXT_KEY_UHV_ARA2", "TXT_KEY_UHV_ARA3"),
("TXT_KEY_UHV_TIB1", "TXT_KEY_UHV_TIB2", "TXT_KEY_UHV_TIB3"),
("TXT_KEY_UHV_INO1", "TXT_KEY_UHV_INO2", "TXT_KEY_UHV_INO3"),
("TXT_KEY_UHV_MOO1", "TXT_KEY_UHV_MOO2", "TXT_KEY_UHV_MOO3_MARATHON"),
("TXT_KEY_UHV_SPA1", "TXT_KEY_UHV_SPA2", "TXT_KEY_UHV_SPA3"),
("TXT_KEY_UHV_FRA1_MARATHON", "TXT_KEY_UHV_FRA2", "TXT_KEY_UHV_FRA3"),
("TXT_KEY_UHV_KHM1", "TXT_KEY_UHV_KHM2", "TXT_KEY_UHV_KHM3_MARATHON"),
("TXT_KEY_UHV_ENG1", "TXT_KEY_UHV_ENG2", "TXT_KEY_UHV_ENG3"),
("TXT_KEY_UHV_HRE1", "TXT_KEY_UHV_HRE2", "TXT_KEY_UHV_HRE3"),
("TXT_KEY_UHV_RUS1", "TXT_KEY_UHV_RUS2", "TXT_KEY_UHV_RUS3"),
("TXT_KEY_UHV_PHI1", "TXT_KEY_UHV_PHI2", "TXT_KEY_UHV_PHI3_MARATHON"),
("TXT_KEY_UHV_SWA1_MARATHON", "TXT_KEY_UHV_SWA2", "TXT_KEY_UHV_SWA3"),
("TXT_KEY_UHV_MAM1", "TXT_KEY_UHV_MAM2", "TXT_KEY_UHV_MAM3"),
("TXT_KEY_UHV_MAL1", "TXT_KEY_UHV_MAL2", "TXT_KEY_UHV_MAL3_MARATHON"),
("TXT_KEY_UHV_POL1", "TXT_KEY_UHV_POL2", "TXT_KEY_UHV_POL3"),
("TXT_KEY_UHV_ZIM1", "TXT_KEY_UHV_ZIM2", "TXT_KEY_UHV_ZIM3"),
("TXT_KEY_UHV_POR1", "TXT_KEY_UHV_POR2", "TXT_KEY_UHV_POR3"),
("TXT_KEY_UHV_INC1", "TXT_KEY_UHV_INC2_MARATHON", "TXT_KEY_UHV_INC3"),
("TXT_KEY_UHV_ITA1", "TXT_KEY_UHV_ITA2", "TXT_KEY_UHV_ITA3"),
("TXT_KEY_UHV_NIG1", "TXT_KEY_UHV_NIG2_MARATHON", "TXT_KEY_UHV_NIG3"),
("TXT_KEY_UHV_MON1", "TXT_KEY_UHV_MON2", "TXT_KEY_UHV_MON3"),
("TXT_KEY_UHV_AZT1", "TXT_KEY_UHV_AZT2", "TXT_KEY_UHV_AZT3"),
("TXT_KEY_UHV_MUG1", "TXT_KEY_UHV_MUG2", "TXT_KEY_UHV_MUG3_MARATHON"),
("TXT_KEY_UHV_TUR1", "TXT_KEY_UHV_TUR2", "TXT_KEY_UHV_TUR3"),
("TXT_KEY_UHV_THA1", "TXT_KEY_UHV_THA2", "TXT_KEY_UHV_THA3"),
("TXT_KEY_UHV_CON1", "TXT_KEY_UHV_CON2_MARATHON", "TXT_KEY_UHV_CON3"),
("TXT_KEY_UHV_SWE1", "TXT_KEY_UHV_SWE2", "TXT_KEY_UHV_SWE3"),
("TXT_KEY_UHV_HOL1", "TXT_KEY_UHV_HOL2", "TXT_KEY_UHV_HOL3"),
("TXT_KEY_UHV_MAN1", "TXT_KEY_UHV_MAN2", "TXT_KEY_UHV_MAN3"),
("TXT_KEY_UHV_GER1", "TXT_KEY_UHV_GER2", "TXT_KEY_UHV_GER3"),
("TXT_KEY_UHV_AME1", "TXT_KEY_UHV_AME2", "TXT_KEY_UHV_AME3"),
("TXT_KEY_UHV_ARG1", "TXT_KEY_UHV_ARG2_MARATHON", "TXT_KEY_UHV_ARG3"),
("TXT_KEY_UHV_BRA1", "TXT_KEY_UHV_BRA2", "TXT_KEY_UHV_BRA3"),
("TXT_KEY_UHV_AUS1", "TXT_KEY_UHV_AUS2", "TXT_KEY_UHV_AUS3"),
("TXT_KEY_UHV_BOE1", "TXT_KEY_UHV_BOE2", "TXT_KEY_UHV_BOE3"),
("TXT_KEY_UHV_CAN1", "TXT_KEY_UHV_CAN2", "TXT_KEY_UHV_CAN3"),
),
( # Epic
("TXT_KEY_UHV_EGY1_EPIC", "TXT_KEY_UHV_EGY2_EPIC", "TXT_KEY_UHV_EGY3_EPIC"),
("TXT_KEY_UHV_CHI1", "TXT_KEY_UHV_CHI2", "TXT_KEY_UHV_CHI3"),
("TXT_KEY_UHV_BAB1", "TXT_KEY_UHV_BAB2_EPIC", "TXT_KEY_UHV_BAB3_EPIC"),
("TXT_KEY_UHV_HAR1", "TXT_KEY_UHV_HAR2", "TXT_KEY_UHV_HAR3"),
("TXT_KEY_UHV_GRE1", "TXT_KEY_UHV_GRE2_EPIC", "TXT_KEY_UHV_GRE3_EPIC"),
("TXT_KEY_UHV_IND1_EPIC", "TXT_KEY_UHV_IND2", "TXT_KEY_UHV_IND3"),
("TXT_KEY_UHV_CAR1", "TXT_KEY_UHV_CAR2", "TXT_KEY_UHV_CAR3_EPIC"),
("TXT_KEY_UHV_PLY1", "TXT_KEY_UHV_PLY2", "TXT_KEY_UHV_PLY3"),
("TXT_KEY_UHV_PER1_EPIC", "TXT_KEY_UHV_PER2_EPIC", "TXT_KEY_UHV_PER3_EPIC"),
("TXT_KEY_UHV_ROM1_EPIC", "TXT_KEY_UHV_ROM2_EPIC", "TXT_KEY_UHV_ROM3"),
("TXT_KEY_UHV_TAM1_EPIC", "TXT_KEY_UHV_TAM2", "TXT_KEY_UHV_TAM3_EPIC"),
("TXT_KEY_UHV_ETH1", "TXT_KEY_UHV_ETH2_EPIC", "TXT_KEY_UHV_ETH3"),
("TXT_KEY_UHV_VIE1_EPIC", "TXT_KEY_UHV_VIE2", "TXT_KEY_UHV_VIE3"),
("TXT_KEY_UHV_KOR1", "TXT_KEY_UHV_KOR2", "TXT_KEY_UHV_KOR3"),
("TXT_KEY_UHV_MAY1_EPIC", "TXT_KEY_UHV_MAY2", "TXT_KEY_UHV_MAY3"),
("TXT_KEY_UHV_BYZ1_EPIC", "TXT_KEY_UHV_BYZ2", "TXT_KEY_UHV_BYZ3"),
("TXT_KEY_UHV_JAP1_EPIC", "TXT_KEY_UHV_JAP2", "TXT_KEY_UHV_JAP3"),
("TXT_KEY_UHV_VIK1", "TXT_KEY_UHV_VIK2", "TXT_KEY_UHV_VIK3_EPIC"),
("TXT_KEY_UHV_ARA1", "TXT_KEY_UHV_ARA2", "TXT_KEY_UHV_ARA3"),
("TXT_KEY_UHV_TIB1", "TXT_KEY_UHV_TIB2", "TXT_KEY_UHV_TIB3"),
("TXT_KEY_UHV_INO1", "TXT_KEY_UHV_INO2", "TXT_KEY_UHV_INO3"),
("TXT_KEY_UHV_MOO1", "TXT_KEY_UHV_MOO2", "TXT_KEY_UHV_MOO3_EPIC"),
("TXT_KEY_UHV_SPA1", "TXT_KEY_UHV_SPA2", "TXT_KEY_UHV_SPA3"),
("TXT_KEY_UHV_FRA1_EPIC", "TXT_KEY_UHV_FRA2", "TXT_KEY_UHV_FRA3"),
("TXT_KEY_UHV_KHM1", "TXT_KEY_UHV_KHM2", "TXT_KEY_UHV_KHM3_EPIC"),
("TXT_KEY_UHV_ENG1", "TXT_KEY_UHV_ENG2", "TXT_KEY_UHV_ENG3"),
("TXT_KEY_UHV_HRE1", "TXT_KEY_UHV_HRE2", "TXT_KEY_UHV_HRE3"),
("TXT_KEY_UHV_RUS1", "TXT_KEY_UHV_RUS2", "TXT_KEY_UHV_RUS3"),
("TXT_KEY_UHV_PHI1", "TXT_KEY_UHV_PHI2", "TXT_KEY_UHV_PHI3_EPIC"),
("TXT_KEY_UHV_SWA1_EPIC", "TXT_KEY_UHV_SWA2", "TXT_KEY_UHV_SWA3"),
("TXT_KEY_UHV_MAM1", "TXT_KEY_UHV_MAM2", "TXT_KEY_UHV_MAM3"),
("TXT_KEY_UHV_MAL1", "TXT_KEY_UHV_MAL2", "TXT_KEY_UHV_MAL3_EPIC"),
("TXT_KEY_UHV_POL1", "TXT_KEY_UHV_POL2", "TXT_KEY_UHV_POL3"),
("TXT_KEY_UHV_ZIM1", "TXT_KEY_UHV_ZIM2", "TXT_KEY_UHV_ZIM3"),
("TXT_KEY_UHV_POR1", "TXT_KEY_UHV_POR2", "TXT_KEY_UHV_POR3"),
("TXT_KEY_UHV_INC1", "TXT_KEY_UHV_INC2_EPIC", "TXT_KEY_UHV_INC3"),
("TXT_KEY_UHV_ITA1", "TXT_KEY_UHV_ITA2", "TXT_KEY_UHV_ITA3"),
("TXT_KEY_UHV_NIG1", "TXT_KEY_UHV_NIG2_EPIC", "TXT_KEY_UHV_NIG3"),
("TXT_KEY_UHV_MON1", "TXT_KEY_UHV_MON2", "TXT_KEY_UHV_MON3"),
("TXT_KEY_UHV_AZT1", "TXT_KEY_UHV_AZT2", "TXT_KEY_UHV_AZT3"),
("TXT_KEY_UHV_MUG1", "TXT_KEY_UHV_MUG2", "TXT_KEY_UHV_MUG3_EPIC"),
("TXT_KEY_UHV_TUR1", "TXT_KEY_UHV_TUR2", "TXT_KEY_UHV_TUR3"),
("TXT_KEY_UHV_THA1", "TXT_KEY_UHV_THA2", "TXT_KEY_UHV_THA3"),
("TXT_KEY_UHV_CON1", "TXT_KEY_UHV_CON2_EPIC", "TXT_KEY_UHV_CON3"),
("TXT_KEY_UHV_SWE1", "TXT_KEY_UHV_SWE2", "TXT_KEY_UHV_SWE3"),
("TXT_KEY_UHV_HOL1", "TXT_KEY_UHV_HOL2", "TXT_KEY_UHV_HOL3"),
("TXT_KEY_UHV_MAN1", "TXT_KEY_UHV_MAN2", "TXT_KEY_UHV_MAN3"),
("TXT_KEY_UHV_GER1", "TXT_KEY_UHV_GER2", "TXT_KEY_UHV_GER3"),
("TXT_KEY_UHV_AME1", "TXT_KEY_UHV_AME2", "TXT_KEY_UHV_AME3"),
("TXT_KEY_UHV_ARG1", "TXT_KEY_UHV_ARG2_EPIC", "TXT_KEY_UHV_ARG3"),
("TXT_KEY_UHV_BRA1", "TXT_KEY_UHV_BRA2", "TXT_KEY_UHV_BRA3"),
("TXT_KEY_UHV_AUS1", "TXT_KEY_UHV_AUS2", "TXT_KEY_UHV_AUS3"),
("TXT_KEY_UHV_BOE1", "TXT_KEY_UHV_BOE2", "TXT_KEY_UHV_BOE3"),
("TXT_KEY_UHV_CAN1", "TXT_KEY_UHV_CAN2", "TXT_KEY_UHV_CAN3"),
),
( # Normal
("TXT_KEY_UHV_EGY1", "TXT_KEY_UHV_EGY2", "TXT_KEY_UHV_EGY3"),
("TXT_KEY_UHV_CHI1", "TXT_KEY_UHV_CHI2", "TXT_KEY_UHV_CHI3"),
("TXT_KEY_UHV_BAB1", "TXT_KEY_UHV_BAB2", "TXT_KEY_UHV_BAB3"),
("TXT_KEY_UHV_HAR1", "TXT_KEY_UHV_HAR2", "TXT_KEY_UHV_HAR3"),
("TXT_KEY_UHV_GRE1", "TXT_KEY_UHV_GRE2", "TXT_KEY_UHV_GRE3"),
("TXT_KEY_UHV_IND1", "TXT_KEY_UHV_IND2", "TXT_KEY_UHV_IND3"),
("TXT_KEY_UHV_CAR1", "TXT_KEY_UHV_CAR2", "TXT_KEY_UHV_CAR3"),
("TXT_KEY_UHV_PLY1", "TXT_KEY_UHV_PLY2", "TXT_KEY_UHV_PLY3"),
("TXT_KEY_UHV_PER1", "TXT_KEY_UHV_PER2", "TXT_KEY_UHV_PER3"),
("TXT_KEY_UHV_ROM1", "TXT_KEY_UHV_ROM2", "TXT_KEY_UHV_ROM3"),
("TXT_KEY_UHV_TAM1", "TXT_KEY_UHV_TAM2", "TXT_KEY_UHV_TAM3"),
("TXT_KEY_UHV_ETH1", "TXT_KEY_UHV_ETH2", "TXT_KEY_UHV_ETH3"),
("TXT_KEY_UHV_VIE1", "TXT_KEY_UHV_VIE2", "TXT_KEY_UHV_VIE3"),
("TXT_KEY_UHV_KOR1", "TXT_KEY_UHV_KOR2", "TXT_KEY_UHV_KOR3"),
("TXT_KEY_UHV_MAY1", "TXT_KEY_UHV_MAY2", "TXT_KEY_UHV_MAY3"),
("TXT_KEY_UHV_BYZ1", "TXT_KEY_UHV_BYZ2", "TXT_KEY_UHV_BYZ3"),
("TXT_KEY_UHV_JAP1", "TXT_KEY_UHV_JAP2", "TXT_KEY_UHV_JAP3"),
("TXT_KEY_UHV_VIK1", "TXT_KEY_UHV_VIK2", "TXT_KEY_UHV_VIK3"),
("TXT_KEY_UHV_ARA1", "TXT_KEY_UHV_ARA2", "TXT_KEY_UHV_ARA3"),
("TXT_KEY_UHV_TIB1", "TXT_KEY_UHV_TIB2", "TXT_KEY_UHV_TIB3"),
("TXT_KEY_UHV_INO1", "TXT_KEY_UHV_INO2", "TXT_KEY_UHV_INO3"),
("TXT_KEY_UHV_MOO1", "TXT_KEY_UHV_MOO2", "TXT_KEY_UHV_MOO3"),
("TXT_KEY_UHV_SPA1", "TXT_KEY_UHV_SPA2", "TXT_KEY_UHV_SPA3"),
("TXT_KEY_UHV_FRA1", "TXT_KEY_UHV_FRA2", "TXT_KEY_UHV_FRA3"),
("TXT_KEY_UHV_KHM1", "TXT_KEY_UHV_KHM2", "TXT_KEY_UHV_KHM3"),
("TXT_KEY_UHV_ENG1", "TXT_KEY_UHV_ENG2", "TXT_KEY_UHV_ENG3"),
("TXT_KEY_UHV_HRE1", "TXT_KEY_UHV_HRE2", "TXT_KEY_UHV_HRE3"),
("TXT_KEY_UHV_RUS1", "TXT_KEY_UHV_RUS2", "TXT_KEY_UHV_RUS3"),
("TXT_KEY_UHV_PHI1", "TXT_KEY_UHV_PHI2", "TXT_KEY_UHV_PHI3"),
("TXT_KEY_UHV_SWA1", "TXT_KEY_UHV_SWA2", "TXT_KEY_UHV_SWA3"),
("TXT_KEY_UHV_MAM1", "TXT_KEY_UHV_MAM2", "TXT_KEY_UHV_MAM3"),
("TXT_KEY_UHV_MAL1", "TXT_KEY_UHV_MAL2", "TXT_KEY_UHV_MAL3"),
("TXT_KEY_UHV_POL1", "TXT_KEY_UHV_POL2", "TXT_KEY_UHV_POL3"),
("TXT_KEY_UHV_ZIM1", "TXT_KEY_UHV_ZIM2", "TXT_KEY_UHV_ZIM3"),
("TXT_KEY_UHV_POR1", "TXT_KEY_UHV_POR2", "TXT_KEY_UHV_POR3"),
("TXT_KEY_UHV_INC1", "TXT_KEY_UHV_INC2", "TXT_KEY_UHV_INC3"),
("TXT_KEY_UHV_ITA1", "TXT_KEY_UHV_ITA2", "TXT_KEY_UHV_ITA3"),
("TXT_KEY_UHV_NIG1", "TXT_KEY_UHV_NIG2", "TXT_KEY_UHV_NIG3"),
("TXT_KEY_UHV_MON1", "TXT_KEY_UHV_MON2", "TXT_KEY_UHV_MON3"),
("TXT_KEY_UHV_AZT1", "TXT_KEY_UHV_AZT2", "TXT_KEY_UHV_AZT3"),
("TXT_KEY_UHV_MUG1", "TXT_KEY_UHV_MUG2", "TXT_KEY_UHV_MUG3"),
("TXT_KEY_UHV_TUR1", "TXT_KEY_UHV_TUR2", "TXT_KEY_UHV_TUR3"),
("TXT_KEY_UHV_THA1", "TXT_KEY_UHV_THA2", "TXT_KEY_UHV_THA3"),
("TXT_KEY_UHV_CON1", "TXT_KEY_UHV_CON2", "TXT_KEY_UHV_CON3"),
("TXT_KEY_UHV_SWE1", "TXT_KEY_UHV_SWE2", "TXT_KEY_UHV_SWE3"),
("TXT_KEY_UHV_HOL1", "TXT_KEY_UHV_HOL2", "TXT_KEY_UHV_HOL3"),
("TXT_KEY_UHV_MAN1", "TXT_KEY_UHV_MAN2", "TXT_KEY_UHV_MAN3"),
("TXT_KEY_UHV_GER1", "TXT_KEY_UHV_GER2", "TXT_KEY_UHV_GER3"),
("TXT_KEY_UHV_AME1", "TXT_KEY_UHV_AME2", "TXT_KEY_UHV_AME3"),
("TXT_KEY_UHV_ARG1", "TXT_KEY_UHV_ARG2", "TXT_KEY_UHV_ARG3"),
("TXT_KEY_UHV_BRA1", "TXT_KEY_UHV_BRA2", "TXT_KEY_UHV_BRA3"),
("TXT_KEY_UHV_AUS1", "TXT_KEY_UHV_AUS2", "TXT_KEY_UHV_AUS3"),
("TXT_KEY_UHV_BOE1", "TXT_KEY_UHV_BOE2", "TXT_KEY_UHV_BOE3"),
("TXT_KEY_UHV_CAN1", "TXT_KEY_UHV_CAN2", "TXT_KEY_UHV_CAN3"),
)
)

tGoals2 = (
( # Marathon
("TXT_KEY_UHV_EGY1_MARATHON", "TXT_KEY_UHV_EGY2_MARATHON", "TXT_KEY_UHV_EGY3_MARATHON"),
("TXT_KEY_UHV_CHI1", "TXT_KEY_UHV_CHI2", "TXT_KEY_UHV_CHI3"),
("TXT_KEY_UHV_BAB1", "TXT_KEY_UHV_BAB2_NOTURN", "TXT_KEY_UHV_BAB3_NOTURN"),
("TXT_KEY_UHV_HAR1", "TXT_KEY_UHV_HAR2", "TXT_KEY_UHV_HAR3"),
("TXT_KEY_UHV_GRE1", "TXT_KEY_UHV_GRE2_NOTURN", "TXT_KEY_UHV_GRE3"),
("TXT_KEY_UHV_IND1", "TXT_KEY_UHV_IND2", "TXT_KEY_UHV_IND3"),
("TXT_KEY_UHV_CAR1", "TXT_KEY_UHV_CAR2", "TXT_KEY_UHV_CAR3_MARATHON"),
("TXT_KEY_UHV_PLY1", "TXT_KEY_UHV_PLY2", "TXT_KEY_UHV_PLY3"),
("TXT_KEY_UHV_IRA1", "TXT_KEY_UHV_IRA2", "TXT_KEY_UHV_IRA3_MARATHON"),
("TXT_KEY_UHV_ITA1", "TXT_KEY_UHV_ITA2", "TXT_KEY_UHV_ITA3"),
("TXT_KEY_UHV_TAM1_MARATHON", "TXT_KEY_UHV_TAM2", "TXT_KEY_UHV_TAM3_MARATHON"),
("TXT_KEY_UHV_ETH1", "TXT_KEY_UHV_ETH2", "TXT_KEY_UHV_ETH3"),
("TXT_KEY_UHV_VIE1_MARATHON", "TXT_KEY_UHV_VIE2", "TXT_KEY_UHV_VIE3"),
("TXT_KEY_UHV_KOR1", "TXT_KEY_UHV_KOR2", "TXT_KEY_UHV_KOR3"),
("TXT_KEY_UHV_COL1", "TXT_KEY_UHV_COL2", "TXT_KEY_UHV_COL3_MARATHON"),
("TXT_KEY_UHV_BYZ1_MARATHON", "TXT_KEY_UHV_BYZ2", "TXT_KEY_UHV_BYZ3"),
("TXT_KEY_UHV_JAP1_MARATHON", "TXT_KEY_UHV_JAP2", "TXT_KEY_UHV_JAP3"),
("TXT_KEY_UHV_VIK1", "TXT_KEY_UHV_VIK2", "TXT_KEY_UHV_VIK3_MARATHON"),
("TXT_KEY_UHV_ARA1", "TXT_KEY_UHV_ARA2", "TXT_KEY_UHV_ARA3"),
("TXT_KEY_UHV_TIB1", "TXT_KEY_UHV_TIB2", "TXT_KEY_UHV_TIB3"),
("TXT_KEY_UHV_INO1", "TXT_KEY_UHV_INO2", "TXT_KEY_UHV_INO3"),
("TXT_KEY_UHV_MOO1", "TXT_KEY_UHV_MOO2", "TXT_KEY_UHV_MOO3"),
("TXT_KEY_UHV_SPA1", "TXT_KEY_UHV_SPA2", "TXT_KEY_UHV_SPA3"),
("TXT_KEY_UHV_FRA1", "TXT_KEY_UHV_FRA2", "TXT_KEY_UHV_FRA3"),
("TXT_KEY_UHV_KHM1", "TXT_KEY_UHV_KHM2", "TXT_KEY_UHV_KHM3_MARATHON"),
("TXT_KEY_UHV_ENG1", "TXT_KEY_UHV_ENG2", "TXT_KEY_UHV_ENG3"),
("TXT_KEY_UHV_HRE1", "TXT_KEY_UHV_HRE2", "TXT_KEY_UHV_HRE3"),
("TXT_KEY_UHV_RUS1", "TXT_KEY_UHV_RUS2", "TXT_KEY_UHV_RUS3"),
("TXT_KEY_UHV_PHI1", "TXT_KEY_UHV_PHI2", "TXT_KEY_UHV_PHI3_MARATHON"),
("TXT_KEY_UHV_SWA1_MARATHON", "TXT_KEY_UHV_SWA2", "TXT_KEY_UHV_SWA3"),
("TXT_KEY_UHV_MAM1", "TXT_KEY_UHV_MAM2", "TXT_KEY_UHV_MAM3"),
("TXT_KEY_UHV_MAL1", "TXT_KEY_UHV_MAL2_MARATHON", "TXT_KEY_UHV_MAL3_MARATHON"),
("TXT_KEY_UHV_POL1", "TXT_KEY_UHV_POL2", "TXT_KEY_UHV_POL3"),
("TXT_KEY_UHV_ZIM1", "TXT_KEY_UHV_ZIM2", "TXT_KEY_UHV_ZIM3"),
("TXT_KEY_UHV_POR1", "TXT_KEY_UHV_POR2", "TXT_KEY_UHV_POR3"),
("TXT_KEY_UHV_INC1", "TXT_KEY_UHV_INC2_MARATHON", "TXT_KEY_UHV_INC3"),
("TXT_KEY_UHV_ITA1", "TXT_KEY_UHV_ITA2", "TXT_KEY_UHV_ITA3"),
("TXT_KEY_UHV_NIG1", "TXT_KEY_UHV_NIG2_MARATHON", "TXT_KEY_UHV_NIG3"),
("TXT_KEY_UHV_MON1", "TXT_KEY_UHV_MON2", "TXT_KEY_UHV_MON3"),
("TXT_KEY_UHV_MEX1", "TXT_KEY_UHV_MEX2", "TXT_KEY_UHV_MEX3"),
("TXT_KEY_UHV_MUG1", "TXT_KEY_UHV_MUG2", "TXT_KEY_UHV_MUG3_MARATHON"),
("TXT_KEY_UHV_TUR1", "TXT_KEY_UHV_TUR2", "TXT_KEY_UHV_TUR3"),
("TXT_KEY_UHV_THA1", "TXT_KEY_UHV_THA2", "TXT_KEY_UHV_THA3"),
("TXT_KEY_UHV_CON1", "TXT_KEY_UHV_CON2_MARATHON", "TXT_KEY_UHV_CON3"),
("TXT_KEY_UHV_SWE1", "TXT_KEY_UHV_SWE2", "TXT_KEY_UHV_SWE3"),
("TXT_KEY_UHV_HOL1", "TXT_KEY_UHV_HOL2", "TXT_KEY_UHV_HOL3"),
("TXT_KEY_UHV_MAN1", "TXT_KEY_UHV_MAN2", "TXT_KEY_UHV_MAN3"),
("TXT_KEY_UHV_GER1", "TXT_KEY_UHV_GER2", "TXT_KEY_UHV_GER3"),
("TXT_KEY_UHV_AME1", "TXT_KEY_UHV_AME2", "TXT_KEY_UHV_AME3"),
("TXT_KEY_UHV_ARG1", "TXT_KEY_UHV_ARG2_MARATHON", "TXT_KEY_UHV_ARG3"),
("TXT_KEY_UHV_BRA1", "TXT_KEY_UHV_BRA2", "TXT_KEY_UHV_BRA3"),
("TXT_KEY_UHV_AUS1", "TXT_KEY_UHV_AUS2", "TXT_KEY_UHV_AUS3"),
("TXT_KEY_UHV_BOE1", "TXT_KEY_UHV_BOE2", "TXT_KEY_UHV_BOE3"),
("TXT_KEY_UHV_CAN1", "TXT_KEY_UHV_CAN2", "TXT_KEY_UHV_CAN3")
),
( # Epic
("TXT_KEY_UHV_EGY1_EPIC", "TXT_KEY_UHV_EGY2_EPIC", "TXT_KEY_UHV_EGY3_EPIC"),
("TXT_KEY_UHV_CHI1", "TXT_KEY_UHV_CHI2", "TXT_KEY_UHV_CHI3"),
("TXT_KEY_UHV_BAB1", "TXT_KEY_UHV_BAB2_NOTURN", "TXT_KEY_UHV_BAB3_NOTURN"),
("TXT_KEY_UHV_HAR1", "TXT_KEY_UHV_HAR2", "TXT_KEY_UHV_HAR3"),
("TXT_KEY_UHV_GRE1", "TXT_KEY_UHV_GRE2_NOTURN", "TXT_KEY_UHV_GRE3"),
("TXT_KEY_UHV_IND1", "TXT_KEY_UHV_IND2", "TXT_KEY_UHV_IND3"),
("TXT_KEY_UHV_CAR1", "TXT_KEY_UHV_CAR2", "TXT_KEY_UHV_CAR3_EPIC"),
("TXT_KEY_UHV_PLY1", "TXT_KEY_UHV_PLY2", "TXT_KEY_UHV_PLY3"),
("TXT_KEY_UHV_IRA1", "TXT_KEY_UHV_IRA2", "TXT_KEY_UHV_IRA3_EPIC"),
("TXT_KEY_UHV_ITA1", "TXT_KEY_UHV_ITA2", "TXT_KEY_UHV_ITA3"),
("TXT_KEY_UHV_TAM1_EPIC", "TXT_KEY_UHV_TAM2", "TXT_KEY_UHV_TAM3_EPIC"),
("TXT_KEY_UHV_ETH1", "TXT_KEY_UHV_ETH2", "TXT_KEY_UHV_ETH3"),
("TXT_KEY_UHV_VIE1_EPIC", "TXT_KEY_UHV_VIE2", "TXT_KEY_UHV_VIE3"),
("TXT_KEY_UHV_KOR1", "TXT_KEY_UHV_KOR2", "TXT_KEY_UHV_KOR3"),
("TXT_KEY_UHV_COL1", "TXT_KEY_UHV_COL2", "TXT_KEY_UHV_COL3_EPIC"),
("TXT_KEY_UHV_BYZ1_EPIC", "TXT_KEY_UHV_BYZ2", "TXT_KEY_UHV_BYZ3"),
("TXT_KEY_UHV_JAP1_EPIC", "TXT_KEY_UHV_JAP2", "TXT_KEY_UHV_JAP3"),
("TXT_KEY_UHV_VIK1", "TXT_KEY_UHV_VIK2", "TXT_KEY_UHV_VIK3_EPIC"),
("TXT_KEY_UHV_ARA1", "TXT_KEY_UHV_ARA2", "TXT_KEY_UHV_ARA3"),
("TXT_KEY_UHV_TIB1", "TXT_KEY_UHV_TIB2", "TXT_KEY_UHV_TIB3"),
("TXT_KEY_UHV_INO1", "TXT_KEY_UHV_INO2", "TXT_KEY_UHV_INO3"),
("TXT_KEY_UHV_MOO1", "TXT_KEY_UHV_MOO2", "TXT_KEY_UHV_MOO3"),
("TXT_KEY_UHV_SPA1", "TXT_KEY_UHV_SPA2", "TXT_KEY_UHV_SPA3"),
("TXT_KEY_UHV_FRA1", "TXT_KEY_UHV_FRA2", "TXT_KEY_UHV_FRA3"),
("TXT_KEY_UHV_KHM1", "TXT_KEY_UHV_KHM2", "TXT_KEY_UHV_KHM3_EPIC"),
("TXT_KEY_UHV_ENG1", "TXT_KEY_UHV_ENG2", "TXT_KEY_UHV_ENG3"),
("TXT_KEY_UHV_HRE1", "TXT_KEY_UHV_HRE2", "TXT_KEY_UHV_HRE3"),
("TXT_KEY_UHV_RUS1", "TXT_KEY_UHV_RUS2", "TXT_KEY_UHV_RUS3"),
("TXT_KEY_UHV_PHI1", "TXT_KEY_UHV_PHI2", "TXT_KEY_UHV_PHI3_EPIC"),
("TXT_KEY_UHV_SWA1_EPIC", "TXT_KEY_UHV_SWA2", "TXT_KEY_UHV_SWA3"),
("TXT_KEY_UHV_MAM1", "TXT_KEY_UHV_MAM2", "TXT_KEY_UHV_MAM3"),
("TXT_KEY_UHV_MAL1", "TXT_KEY_UHV_MAL2_EPIC", "TXT_KEY_UHV_MAL3_EPIC"),
("TXT_KEY_UHV_POL1", "TXT_KEY_UHV_POL2", "TXT_KEY_UHV_POL3"),
("TXT_KEY_UHV_ZIM1", "TXT_KEY_UHV_ZIM2", "TXT_KEY_UHV_ZIM3"),
("TXT_KEY_UHV_POR1", "TXT_KEY_UHV_POR2", "TXT_KEY_UHV_POR3"),
("TXT_KEY_UHV_INC1", "TXT_KEY_UHV_INC2_EPIC", "TXT_KEY_UHV_INC3"),
("TXT_KEY_UHV_ITA1", "TXT_KEY_UHV_ITA2", "TXT_KEY_UHV_ITA3"),
("TXT_KEY_UHV_NIG1", "TXT_KEY_UHV_NIG2_EPIC", "TXT_KEY_UHV_NIG3"),
("TXT_KEY_UHV_MON1", "TXT_KEY_UHV_MON2", "TXT_KEY_UHV_MON3"),
("TXT_KEY_UHV_MEX1", "TXT_KEY_UHV_MEX2", "TXT_KEY_UHV_MEX3"),
("TXT_KEY_UHV_MUG1", "TXT_KEY_UHV_MUG2", "TXT_KEY_UHV_MUG3_EPIC"),
("TXT_KEY_UHV_TUR1", "TXT_KEY_UHV_TUR2", "TXT_KEY_UHV_TUR3"),
("TXT_KEY_UHV_THA1", "TXT_KEY_UHV_THA2", "TXT_KEY_UHV_THA3"),
("TXT_KEY_UHV_CON1", "TXT_KEY_UHV_CON2_EPIC", "TXT_KEY_UHV_CON3"),
("TXT_KEY_UHV_SWE1", "TXT_KEY_UHV_SWE2", "TXT_KEY_UHV_SWE3"),
("TXT_KEY_UHV_HOL1", "TXT_KEY_UHV_HOL2", "TXT_KEY_UHV_HOL3"),
("TXT_KEY_UHV_MAN1", "TXT_KEY_UHV_MAN2", "TXT_KEY_UHV_MAN3"),
("TXT_KEY_UHV_GER1", "TXT_KEY_UHV_GER2", "TXT_KEY_UHV_GER3"),
("TXT_KEY_UHV_AME1", "TXT_KEY_UHV_AME2", "TXT_KEY_UHV_AME3"),
("TXT_KEY_UHV_ARG1", "TXT_KEY_UHV_ARG2_EPIC", "TXT_KEY_UHV_ARG3"),
("TXT_KEY_UHV_BRA1", "TXT_KEY_UHV_BRA2", "TXT_KEY_UHV_BRA3"),
("TXT_KEY_UHV_AUS1", "TXT_KEY_UHV_AUS2", "TXT_KEY_UHV_AUS3"),
("TXT_KEY_UHV_BOE1", "TXT_KEY_UHV_BOE2", "TXT_KEY_UHV_BOE3"),
("TXT_KEY_UHV_CAN1", "TXT_KEY_UHV_CAN2", "TXT_KEY_UHV_CAN3")
),
( # Normal
("TXT_KEY_UHV_EGY1", "TXT_KEY_UHV_EGY2", "TXT_KEY_UHV_EGY3"),
("TXT_KEY_UHV_CHI1", "TXT_KEY_UHV_CHI2", "TXT_KEY_UHV_CHI3"),
("TXT_KEY_UHV_BAB1", "TXT_KEY_UHV_BAB2", "TXT_KEY_UHV_BAB3"),
("TXT_KEY_UHV_HAR1", "TXT_KEY_UHV_HAR2", "TXT_KEY_UHV_HAR3"),
("TXT_KEY_UHV_GRE1", "TXT_KEY_UHV_GRE2", "TXT_KEY_UHV_GRE3"),
("TXT_KEY_UHV_IND1", "TXT_KEY_UHV_IND2", "TXT_KEY_UHV_IND3"),
("TXT_KEY_UHV_CAR1", "TXT_KEY_UHV_CAR2", "TXT_KEY_UHV_CAR3"),
("TXT_KEY_UHV_PLY1", "TXT_KEY_UHV_PLY2", "TXT_KEY_UHV_PLY3"),
("TXT_KEY_UHV_IRA1", "TXT_KEY_UHV_IRA2", "TXT_KEY_UHV_IRA3"),
("TXT_KEY_UHV_ITA1", "TXT_KEY_UHV_ITA2", "TXT_KEY_UHV_ITA3"),
("TXT_KEY_UHV_TAM1", "TXT_KEY_UHV_TAM2", "TXT_KEY_UHV_TAM3"),
("TXT_KEY_UHV_ETH1", "TXT_KEY_UHV_ETH2", "TXT_KEY_UHV_ETH3"),
("TXT_KEY_UHV_VIE1", "TXT_KEY_UHV_VIE2", "TXT_KEY_UHV_VIE3"),
("TXT_KEY_UHV_KOR1", "TXT_KEY_UHV_KOR2", "TXT_KEY_UHV_KOR3"),
("TXT_KEY_UHV_COL1", "TXT_KEY_UHV_COL2", "TXT_KEY_UHV_COL3"),
("TXT_KEY_UHV_BYZ1", "TXT_KEY_UHV_BYZ2", "TXT_KEY_UHV_BYZ3"),
("TXT_KEY_UHV_JAP1", "TXT_KEY_UHV_JAP2", "TXT_KEY_UHV_JAP3"),
("TXT_KEY_UHV_VIK1", "TXT_KEY_UHV_VIK2", "TXT_KEY_UHV_VIK3"),
("TXT_KEY_UHV_ARA1", "TXT_KEY_UHV_ARA2", "TXT_KEY_UHV_ARA3"),
("TXT_KEY_UHV_TIB1", "TXT_KEY_UHV_TIB2", "TXT_KEY_UHV_TIB3"),
("TXT_KEY_UHV_INO1", "TXT_KEY_UHV_INO2", "TXT_KEY_UHV_INO3"),
("TXT_KEY_UHV_MOO1", "TXT_KEY_UHV_MOO2", "TXT_KEY_UHV_MOO3"),
("TXT_KEY_UHV_SPA1", "TXT_KEY_UHV_SPA2", "TXT_KEY_UHV_SPA3"),
("TXT_KEY_UHV_FRA1", "TXT_KEY_UHV_FRA2", "TXT_KEY_UHV_FRA3"),
("TXT_KEY_UHV_KHM1", "TXT_KEY_UHV_KHM2", "TXT_KEY_UHV_KHM3"),
("TXT_KEY_UHV_ENG1", "TXT_KEY_UHV_ENG2", "TXT_KEY_UHV_ENG3"),
("TXT_KEY_UHV_HRE1", "TXT_KEY_UHV_HRE2", "TXT_KEY_UHV_HRE3"),
("TXT_KEY_UHV_RUS1", "TXT_KEY_UHV_RUS2", "TXT_KEY_UHV_RUS3"),
("TXT_KEY_UHV_PHI1", "TXT_KEY_UHV_PHI2", "TXT_KEY_UHV_PHI3"),
("TXT_KEY_UHV_SWA1", "TXT_KEY_UHV_SWA2", "TXT_KEY_UHV_SWA3"),
("TXT_KEY_UHV_MAM1", "TXT_KEY_UHV_MAM2", "TXT_KEY_UHV_MAM3"),
("TXT_KEY_UHV_MAL1", "TXT_KEY_UHV_MAL2", "TXT_KEY_UHV_MAL3"),
("TXT_KEY_UHV_POL1", "TXT_KEY_UHV_POL2", "TXT_KEY_UHV_POL3"),
("TXT_KEY_UHV_ZIM1", "TXT_KEY_UHV_ZIM2", "TXT_KEY_UHV_ZIM3"),
("TXT_KEY_UHV_POR1", "TXT_KEY_UHV_POR2", "TXT_KEY_UHV_POR3"),
("TXT_KEY_UHV_INC1", "TXT_KEY_UHV_INC2", "TXT_KEY_UHV_INC3"),
("TXT_KEY_UHV_ITA1", "TXT_KEY_UHV_ITA2", "TXT_KEY_UHV_ITA3"),
("TXT_KEY_UHV_NIG1", "TXT_KEY_UHV_NIG2", "TXT_KEY_UHV_NIG3"),
("TXT_KEY_UHV_MON1", "TXT_KEY_UHV_MON2", "TXT_KEY_UHV_MON3"),
("TXT_KEY_UHV_MEX1", "TXT_KEY_UHV_MEX2", "TXT_KEY_UHV_MEX3"),
("TXT_KEY_UHV_MUG1", "TXT_KEY_UHV_MUG2", "TXT_KEY_UHV_MUG3"),
("TXT_KEY_UHV_TUR1", "TXT_KEY_UHV_TUR2", "TXT_KEY_UHV_TUR3"),
("TXT_KEY_UHV_THA1", "TXT_KEY_UHV_THA2", "TXT_KEY_UHV_THA3"),
("TXT_KEY_UHV_CON1", "TXT_KEY_UHV_CON2", "TXT_KEY_UHV_CON3"),
("TXT_KEY_UHV_SWE1", "TXT_KEY_UHV_SWE2", "TXT_KEY_UHV_SWE3"),
("TXT_KEY_UHV_HOL1", "TXT_KEY_UHV_HOL2", "TXT_KEY_UHV_HOL3"),
("TXT_KEY_UHV_MAN1", "TXT_KEY_UHV_MAN2", "TXT_KEY_UHV_MAN3"),
("TXT_KEY_UHV_GER1", "TXT_KEY_UHV_GER2", "TXT_KEY_UHV_GER3"),
("TXT_KEY_UHV_AME1", "TXT_KEY_UHV_AME2", "TXT_KEY_UHV_AME3"),
("TXT_KEY_UHV_ARG1", "TXT_KEY_UHV_ARG2", "TXT_KEY_UHV_ARG3"),
("TXT_KEY_UHV_BRA1", "TXT_KEY_UHV_BRA2", "TXT_KEY_UHV_BRA3"),
("TXT_KEY_UHV_AUS1", "TXT_KEY_UHV_AUS2", "TXT_KEY_UHV_AUS3"),
("TXT_KEY_UHV_BOE1", "TXT_KEY_UHV_BOE2", "TXT_KEY_UHV_BOE3"),
("TXT_KEY_UHV_CAN1", "TXT_KEY_UHV_CAN2", "TXT_KEY_UHV_CAN3")
)
)

tGoals = (tGoals1, tGoals2)

tReligiousGoals = (
# Marathon
(("TXT_KEY_URV_JUD1", "TXT_KEY_URV_JUD2", "TXT_KEY_URV_JUD3"),
("TXT_KEY_URV_ORT1", "TXT_KEY_URV_ORT2", "TXT_KEY_URV_ORT3"),
("TXT_KEY_URV_CAT1_MARATHON", "TXT_KEY_URV_CAT2", "TXT_KEY_URV_CAT3"),
("TXT_KEY_URV_PRO1", "TXT_KEY_URV_PRO2", "TXT_KEY_URV_PRO3"),
("TXT_KEY_URV_ISL1", "TXT_KEY_URV_ISL2", "TXT_KEY_URV_ISL3"),
("TXT_KEY_URV_HIN1", "TXT_KEY_URV_HIN2_MARATHON", "TXT_KEY_URV_HIN3"),
("TXT_KEY_URV_BUD1_MARATHON", "TXT_KEY_URV_BUD2_MARATHON", "TXT_KEY_URV_BUD3"),
("TXT_KEY_URV_CON1", "TXT_KEY_URV_CON2", "TXT_KEY_URV_CON3"),
("TXT_KEY_URV_TAO1_MARATHON", "TXT_KEY_URV_TAO2", "TXT_KEY_URV_TAO3"),
("TXT_KEY_URV_ZOR1", "TXT_KEY_URV_ZOR2", "TXT_KEY_URV_ZOR3"),
("TXT_KEY_URV_POL1", "TXT_KEY_URV_POL2", "TXT_KEY_URV_POL3"),
("TXT_KEY_URV_SEC1", "TXT_KEY_URV_SEC2", "TXT_KEY_URV_SEC3")),
# Epic
(("TXT_KEY_URV_JUD1", "TXT_KEY_URV_JUD2", "TXT_KEY_URV_JUD3"),
("TXT_KEY_URV_ORT1", "TXT_KEY_URV_ORT2", "TXT_KEY_URV_ORT3"),
("TXT_KEY_URV_CAT1_EPIC", "TXT_KEY_URV_CAT2", "TXT_KEY_URV_CAT3"),
("TXT_KEY_URV_PRO1", "TXT_KEY_URV_PRO2", "TXT_KEY_URV_PRO3"),
("TXT_KEY_URV_ISL1", "TXT_KEY_URV_ISL2", "TXT_KEY_URV_ISL3"),
("TXT_KEY_URV_HIN1", "TXT_KEY_URV_HIN2", "TXT_KEY_URV_HIN3"),
("TXT_KEY_URV_BUD1_EPIC", "TXT_KEY_URV_BUD2_EPIC", "TXT_KEY_URV_BUD3"),
("TXT_KEY_URV_CON1", "TXT_KEY_URV_CON2", "TXT_KEY_URV_CON3"),
("TXT_KEY_URV_TAO1_EPIC", "TXT_KEY_URV_TAO2", "TXT_KEY_URV_TAO3"),
("TXT_KEY_URV_ZOR1", "TXT_KEY_URV_ZOR2", "TXT_KEY_URV_ZOR3"),
("TXT_KEY_URV_POL1", "TXT_KEY_URV_POL2", "TXT_KEY_URV_POL3"),
("TXT_KEY_URV_SEC1", "TXT_KEY_URV_SEC2", "TXT_KEY_URV_SEC3")),
# Normal
(("TXT_KEY_URV_JUD1", "TXT_KEY_URV_JUD2", "TXT_KEY_URV_JUD3"),
("TXT_KEY_URV_ORT1", "TXT_KEY_URV_ORT2", "TXT_KEY_URV_ORT3"),
("TXT_KEY_URV_CAT1", "TXT_KEY_URV_CAT2", "TXT_KEY_URV_CAT3"),
("TXT_KEY_URV_PRO1", "TXT_KEY_URV_PRO2", "TXT_KEY_URV_PRO3"),
("TXT_KEY_URV_ISL1", "TXT_KEY_URV_ISL2", "TXT_KEY_URV_ISL3"),
("TXT_KEY_URV_HIN1", "TXT_KEY_URV_HIN2", "TXT_KEY_URV_HIN3"),
("TXT_KEY_URV_BUD1", "TXT_KEY_URV_BUD2", "TXT_KEY_URV_BUD3"),
("TXT_KEY_URV_CON1", "TXT_KEY_URV_CON2", "TXT_KEY_URV_CON3"),
("TXT_KEY_URV_TAO1", "TXT_KEY_URV_TAO2", "TXT_KEY_URV_TAO3"),
("TXT_KEY_URV_ZOR1", "TXT_KEY_URV_ZOR2", "TXT_KEY_URV_ZOR3"),
("TXT_KEY_URV_POL1", "TXT_KEY_URV_POL2", "TXT_KEY_URV_POL3"),
("TXT_KEY_URV_SEC1", "TXT_KEY_URV_SEC2", "TXT_KEY_URV_SEC3")))

# Dawn of Man texts
dawnOfMan3000BC = {
iEgypt		:	"TXT_KEY_DOM_EGYPT",
iIndia		:	"TXT_KEY_DOM_INDIA",
iChina		:	"TXT_KEY_DOM_CHINA",
iHarappa	:	"TXT_KEY_DOM_HARAPPA",
iBabylonia	:	"TXT_KEY_DOM_BABYLONIA",
iGreece		:	"TXT_KEY_DOM_GREECE",
iCarthage	:	"TXT_KEY_DOM_PHOENICIA",
iPolynesia	:	"TXT_KEY_DOM_POLYNESIA",
iPersia		:	"TXT_KEY_DOM_PERSIA",
iRome		:	"TXT_KEY_DOM_ROME",
iTamils		:	"TXT_KEY_DOM_TAMILS",
iEthiopia	:	"TXT_KEY_DOM_ETHIOPIA",
iVietnam	:	"TXT_KEY_DOM_VIETNAM",
iJapan		:	"TXT_KEY_DOM_JAPAN",
iKorea		:	"TXT_KEY_DOM_KOREA",
iMaya		:	"TXT_KEY_DOM_MAYA",
iByzantium	:	"TXT_KEY_DOM_BYZANTIUM",
iVikings	:	"TXT_KEY_DOM_VIKINGS",
iArabia		:	"TXT_KEY_DOM_ARABIA",
iTibet		:	"TXT_KEY_DOM_TIBET",
iIndonesia	:	"TXT_KEY_DOM_INDONESIA",
iMoors		:	"TXT_KEY_DOM_MOORS",
iSpain		:	"TXT_KEY_DOM_SPAIN",
iFrance		:	"TXT_KEY_DOM_FRANCE",
iKhmer		:	"TXT_KEY_DOM_KHMER",
iEngland	:	"TXT_KEY_DOM_ENGLAND",
iHolyRome	:	"TXT_KEY_DOM_HOLY_ROME",
iRussia		:	"TXT_KEY_DOM_RUSSIA",
iPhilippines	: "TXT_KEY_DOM_PHILIPPINES",
iSwahili	:	"TXT_KEY_DOM_SWAHILI",
iMamluks	:	"TXT_KEY_DOM_MAMLUKS",
iMali		:	"TXT_KEY_DOM_MALI",
iPoland		:	"TXT_KEY_DOM_POLAND",
iZimbabwe	:	"TXT_KEY_DOM_ZIMBABWE",
iItaly		:	"TXT_KEY_DOM_ITALY",
iPortugal	:	"TXT_KEY_DOM_PORTUGAL",
iInca		:	"TXT_KEY_DOM_INCA",
iAztecs		:	"TXT_KEY_DOM_AZTECS",
iNigeria	:	"TXT_KEY_DOM_NIGERIA",
iMongolia	:	"TXT_KEY_DOM_MONGOLIA",
iMughals	:	"TXT_KEY_DOM_MUGHALS",
iTurkey		:	"TXT_KEY_DOM_TURKEY",
iThailand	:	"TXT_KEY_DOM_THAILAND",
iCongo		:	"TXT_KEY_DOM_CONGO",
iSweden		:	"TXT_KEY_DOM_SWEDEN",
iNetherlands	:	"TXT_KEY_DOM_NETHERLANDS",
iManchuria	:	"TXT_KEY_DOM_MANCHURIA",
iGermany	:	"TXT_KEY_DOM_GERMANY",
iAmerica	:	"TXT_KEY_DOM_AMERICA",
iArgentina	:	"TXT_KEY_DOM_ARGENTINA",
iBrazil		:	"TXT_KEY_DOM_BRAZIL",
iAustralia	:	"TXT_KEY_DOM_AUSTRALIA",
iBrazil		:	"TXT_KEY_DOM_BOERS",
iCanada		:	"TXT_KEY_DOM_CANADA",
}

dawnOfMan600AD = {
iChina		:	"TXT_KEY_DOM_CHINA_LATE",
iJapan		:	"TXT_KEY_DOM_JAPAN_LATE",
iKorea		:	"TXT_KEY_DOM_KOREA_LATE",
iByzantium	:	"TXT_KEY_DOM_BYZANTIUM_LATE",
iVikings	:	"TXT_KEY_DOM_VIKINGS_LATE",
}

dawnOfMan1700AD = {
iManchuria	:	"TXT_KEY_DOM_CHINA_1700AD",
iIndia		:	"TXT_KEY_DOM_INDIA_1700AD",
iPersia		:	"TXT_KEY_DOM_PERSIA_1700AD",
iTamils		:	"TXT_KEY_DOM_TAMILS_1700AD",
iVietnam	:	"TXT_KEY_DOM_VIETNAM_1700AD",
iKorea		:	"TXT_KEY_DOM_KOREA_1700AD",
iJapan		:	"TXT_KEY_DOM_JAPAN_1700AD",
iVikings	:	"TXT_KEY_DOM_VIKINGS_1700AD",
iSpain		:	"TXT_KEY_DOM_SPAIN_1700AD",
iFrance		:	"TXT_KEY_DOM_FRANCE_1700AD",
iEngland	:	"TXT_KEY_DOM_ENGLAND_1700AD",
iHolyRome	:	"TXT_KEY_DOM_AUSTRIA_1700AD",
iRussia		:	"TXT_KEY_DOM_RUSSIA_1700AD",
iPoland		:	"TXT_KEY_DOM_POLAND_1700AD",
iPortugal	:	"TXT_KEY_DOM_PORTUGAL_1700AD",
iMughals	:	"TXT_KEY_DOM_MUGHALS_1700AD",
iTurkey		:	"TXT_KEY_DOM_TURKEY_1700AD",
iThailand	:	"TXT_KEY_DOM_THAILAND_1700AD",
iCongo		:	"TXT_KEY_DOM_CONGO_1700AD",
iSweden		:	"TXT_KEY_DOM_SWEDEN_1700AD",
iNetherlands	:	"TXT_KEY_DOM_NETHERLANDS_1700AD",
}

lDawnOfMan = [dawnOfMan3000BC, dawnOfMan600AD, dawnOfMan1700AD]


iAreaEurope = gc.getMap().plot(55, 50).getArea()
iAreaAfrica = gc.getMap().plot(72, 29).getArea()
iAreaAsia = gc.getMap().plot(102, 47).getArea()

lMiddleEast = []
lEastIndies = []
lNorthAfrica = []
lConstantinople = []

# North Africa
for i in range(48,65+1):
	for j in range(35,39+1):
		lNorthAfrica.append((i,j))

for i in range(66,71+1):
	for j in range(29,37+1):
		lNorthAfrica.append((i,j))

for i in range(72,73+1):
	for j in range(29,32+1):
		lNorthAfrica.append((i,j))

# Middle East
for i in range(72,86+1):
	for j in range(34,46+1):
		lMiddleEast.append((i,j))

for i in range(69,71+1):
	for j in range(40,45+1):
		lMiddleEast.append((i,j))

for i in range(78,86+1):
	for j in range(47,49+1):
		lMiddleEast.append((i,j))
		

# starting gold in 3000 BC
tStartingGold = (
0,	# Egypt
0,	# China
0,	# Babylonia
0, 	# Harappa
100,	# Greece
80,	# India
200,	# Carthage
0,	# Polynesia
200,	# Persia
100,	# Rome
200,	# Tamils
100,	# Ethiopia
100,	# Vietnam
200,	# Korea
200,	# Maya
400,	# Byzantium
100,	# Japan
150,	# Viking
300,	# Arabia
50,	# Tibet
300,	# Indonesia
200,	# Moors
200,	# Spain
150,	# France
200,	# Khmer
200,	# England
150,	# Holy Rome
200,	# Russia
600,	# Philippines
600,	# Swahili
300,	# Mamluks
600,	# Mali
100,	# Poland
200,	# Zimbabwe
200,	# Portugal
700,	# Inca
350,	# Italy
250,	# Nigeria
250,	# Mongolia
600,	# Aztecs
400,	# Mughals
300,	# Turkey
800,	# Thailand
300,	# Congo
500,	# Sweden
600,	# Netherlands
200,	# Manchu
800,	# Germany
1500,	# America
1200,	# Argentina
1600,	# Brazil
1200,	# Australia
1000,	# Boers
1000,	# Canada
50,	# Independent
50,	# Independent
100,	# Native
0,	# Celtia
0,	# Seljuks
)

dExtraGold600AD = {
iChina : 300,
iJapan : 200,
iIndependent : 50,
iIndependent2 : 50,
iNative : 200,
iSeljuks : 250,
}

dExtraGold1700AD = {
iChina : 300,
iIndia : 320,
iTamils : 200,
iJapan : 300,
iSpain : 200,
iFrance : 250,
iEngland : 400,
iRussia : 150,
iPoland : 100,
iPortugal : 250,
iMughals : -200,
iTurkey : -100,
iThailand : -500,
iSweden : 100,
iNetherlands : 200,
}

#rnf. Some civs have a double entry, for a higher chance
lEnemyCivsOnSpawn = [
[], #Egypt
[iIndependent,iIndependent2,iIndependent2], #China
[iIndependent,iIndependent2], #Babylonia
[], #Harappa
[iIndependent,iIndependent2,iBabylonia], #Greece
[], #India
[], #Carthage
[], #Polynesia
[iBabylonia,iBabylonia,iGreece,iCarthage,iCarthage], #Persia
#[iEgypt,iGreece,iGreece,iCarthage,iCarthage], #Rome
[], # rome for testing
[], #Tamils
[], #Ethiopia
[],	#Vietnam
[], #Korea
[], #Maya
[iGreece, iPersia], #Byzantium
[], #Japan
[iEngland,iEngland,iFrance,iIndependent,iIndependent2], #Vikings
[iEgypt,iEgypt,iEgypt,iBabylonia,iBabylonia,iGreece,iPersia,iCarthage,iRome,iByzantium,iByzantium,iSpain,iFrance,iCeltia,iCeltia,iIndependent,iIndependent2], #Arabia
[], #Tibet
[iKhmer, iKhmer], #Indonesia
[], #Moors
[], #Spain
[], #France
[], #Khmer
[], #England
[iRome,iArabia,iArabia], #Holy Rome
[], #Russia
[],	#Philippines
[],	#Swahili
[iByzantium, iByzantium],	#Mamluks
[], #Mali
[], #Poland
[],	#Zimbabwe
[], #Portugal
[], #Inca
[], #Italy
[],	#Nigeria
[iChina,iChina,iChina,iKorea,iKorea,iIndependent,iIndependent,iIndependent2,iIndependent2], #Mongolia
[iMaya], #Aztec
[iIndia, iIndia], #Mughals
[iEgypt,iEgypt,iBabylonia,iGreece,iGreece,iArabia,iArabia,iArabia,iByzantium,iByzantium,iByzantium], #Turkey
[iKhmer, iKhmer, iKhmer], #Thailand
[], #Congo
[], #Sweden
[], #Netherlands
[iChina, iChina, iKorea, iMongolia], #Manchu
[iHolyRome, iPoland], #Germany
[iIndependent,iIndependent2], #America
[iSpain, iSpain, iIndependent,iIndependent2], #Argentina
[iIndependent,iIndependent2], #Brazil
[], #Australia
[iEngland, iNetherlands], #Boers
[], #Canada
]

# Leoreth
lTotalWarOnSpawn = [
[], #Egypt
[], #China
[], #Babylonia
[], #Harappa
[], #Greece
[], #India
[], #Phoenicia
[], #Polynesia
[iBabylonia, iCarthage], #Persia
[iGreece], #Rome
[], #Tamils
[], #Ethiopia
[],	#Vietnam
[], #Korea
[], #Maya
[iGreece], #Byzantium
[], #Japan
[], #Vikings
[iEgypt, iBabylonia, iCarthage, iPersia], #Arabia
[], #Tibet
[], #Indonesia
[], #Moors
[iMoors], #Spain
[], #France
[], #Khmer
[], #England
[iRome], #Holy Rome
[], #Russia
[],	#Philippines
[],	#Swahili
[],	#Mamluks
[], #Mali
[], #Poland
[],	#Zimbabwe
[], #Portugal
[], #Inca
[], #Italy
[],	#Nigeria
[iChina], #Mongolia
[iMaya], #Aztec
[iIndia], #Mughals
[iArabia, iEgypt], #Turkey
[iKhmer], #Thailand
[], #Congo
[], #Sweden
[], #Netherlands
[],	#Manchuria
[], #Germany
[], #America
[], #Argentina
[], #Brazil
[],	#Australia
[],	#Boers
[], #Canada
]


#AIWars
tAggressionLevel = (
0, #Egypt
1, #China
1, #Babylonia
0, #Harappa
2, #Greece
0, #India
0, #Carthage
0, #Polynesia
3, #Persia
3, #Rome
2, #Tamils
0, #Ethiopia
0, #Vietnam
0, #Korea
1, #Maya
1, #Byzantium
1, #Japan
2, #Viking
2, #Arabia
1, #Tibet
1, #Indonesia
1, #Moors
2, #Spain
1, #France
2, #Khmer
1, #England
3, #Holy Rome
1, #Russia
0, #Philippines
0, #Swahili
1, #Mamluks
0, #Mali
1, #Poland
0, #Zimbabwe
0, #Portugal
1, #Inca
0, #Italy
0, #Nigeria
2, #Mongolia
1, #Aztec
1, #Mughals
2, #Turkey
0, #Thailand
0, #Congo
1, #Sweden
0, #Holland
1, #Manchuria
2, #Germany
2, #America
0, #Argentina
0, #Brazil
0, #Australia
0, #Boers
0, #Canada
0) #Barbs


#war during rise of new civs
tAIStopBirthThreshold = (
    80, #Egypt
    60, #China
    50, #Babylonia
    50, #Harappa
    50, #Greece #would be 80 but with Turks must be lower
    80, #India
    80, #Carthage
    80, #Polynesia
    70, #Persia
    80, #Rome
    80, #Tamils
    80, #Ethiopia
	80,	#Vietnam
    80, #Korea
    80, #Maya
    80, #Byzantium
    80, #Japan
    80, #Viking
    80, #Arabia
    80, #Tibet
    80, #Indonesia
    80, #Moors
    80, #Spain  #60 in vanilla and Warlords
    80, #France #60 in vanilla and Warlords
    80, #Khmer
    50, #England
    80, #Holy Rome #70 in vanilla and Warlords
    50, #Russia
	70,	#Philippines
	70, #Swahili
	80,	#Mamluks
    70, #Mali
    40, #Poland
	80,	#Zimbabwe
    40, #Portugal
    70, #Inca
    60, #Italy
	80,	#Nigeria
    70, #Mongolia
    50, #Aztec
    70, #Mughals
    70, #Turkey
    80, #Thailand
    80, #Congo
    70, #Sweden
    40, #Holland
    70, #Manchuria
    80, #Germany
    50, #America
    60, #Argentina
    60, #Brazil
    60,	#Australia
	60,	#Boers
    60, #Canada
    100,
    100,
    100,
    100,
    100)


#RiseAndFall
tResurrectionProb = (
10, #Egypt
100, #China
40, #Babylonia
0, #Harappa
60, #Greece
50, #India
30, #Carthage
40, #Polynesia
70, #Persia
65, #Rome
10, #Tamils
80, #Ethopia
80,	#Vietnam
80, #Korea
30, #Maya
65, #Byzantium
100, #Japan
60, #Viking
100, #Arabia
60, #Tibet
80, #Indonesia
70, #Moors
100, #Spain
100, #France
60, #Khmer
100, #England
80, #Holy Rome
100, #Russia
30,	#Philippines
30,	#Swahili
40,	#Mamluks
30, #Mali
65, #Poland
30,	#Zimbabwe
100, #Portugal
70, #Inca
100, #Italy
30,	#Nigeria
80, #Mongolia
70, #Aztec
80, #Mughals
100, #Turkey
100, #Thailand
20, #Congo
100, #Sweden
100, #Holland
20, #Manchuria
100, #Germany
100, #America
100, #Argentina
100, #Brazil
100, #Australia
100, #Boers
100, #Canada
#    100, #Holland
#    100, #Portugal
100) #Barbs 


#Congresses.
tPatienceThreshold = (
30, #Egypt
30, #China
30, #Babylonia
30, #Harappa
35, #Greece
50, #India
35, #Carthage
50, #Polynesia
30, #Persia
25, #Rome
45, #Tamils
20, #Ethopia
25,	#Vietnam
25, #Korea
35, #Maya
25, #Byzantium
25, #Japan
30, #Viking
30, #Arabia
50, #Tibet
30, #Indonesia
20, #Moors
20, #Spain
20, #France
30, #Khmer
20, #England
20, #Holy Rome
30, #Russia
30,	#Philipinnes
30,	#Swahili
20,	#Mamluks
35, #Mali
20, #Poland
20,	#Zimbabwe
30, #Portugal
35, #Inca
25, #Italy
20,	#Nigeria
20, #Mongolia
30, #Aztec
35, #Mughals
35, #Turkey
30, #Thailand
20, #Congo
30, #Sweden
30, #Holland
20,	#Manchuria
20, #Germany
30, #America
40, #Argentina
40, #Brazil
40,	#Australia
40,	#Boers
40, #Canada
100) #Barbs


#RnF Colonists
tMaxColonists = (
0, #Egypt
0, #China
0, #Babylonia
0, #Harappa
0, #Greece
0, #India
0, #Carthage
0, #Polynesia
0, #Persia
0, #Rome
0, #Tamils
0, #Ethopia
0, #Vietnam
0, #Korea
0, #Maya
0, #Byzantium
0, #Japan
1, #Viking
0, #Arabia
0, #Tibet
0, #Indonesia
0, #Moors
7, #Spain
5, #France
0, #Khmer
6, #England
0, #Holy Rome
0, #Russia
0, #Philippines
0, #Swahili
0, #Mamluks
0, #Mali
0, #Poland
0, #Zimbabwe
6, #Portugal
0, #Inca
0, #Italy
0, #Nigeria
0, #Mongolia
0, #Aztec
0, #Mughals
0, #Turkey
0, #Thailand
0, #Congo
2, #Sweden
6, #Holland
0, #Manchuria
2, #Germany
0, #America
0, #Argentina
0, #Brazil
0, #Australia
0, #Boers
0) #Canada


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

lCatholicStart = [iSpain, iFrance, iEngland, iHolyRome, iPoland, iPortugal, iItaly, iNetherlands, iSweden, iGermany, iAmerica, iArgentina, iBrazil, iBoers, iAustralia, iCanada]
lProtestantStart = [iSweden, iNetherlands, iGermany, iAmerica, iAustralia, iBoers]

iNumCompanies = 9
(iSilkRoute, iTradingCompany, iCerealIndustry, iFishingIndustry, iTextileIndustry, iSteelIndustry, iOilIndustry, iLuxuryIndustry, iComputerIndustry) = range(iNumCompanies)

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

iNumUnits = 190
(iLion, iBear, iPanther, iWolf, iRabbit, iSettler, iCityBuilder, iWorker, iPunjabiWorker, iLabourer, iMadeireiro, 
iScout, iExplorer, iSpy, iReligiousPersecutor, iJewishMissionary, iOrthodoxMissionary, iCatholicMissionary, iProtestantMissionary, iIslamicMissionary, iHinduMissionary, 
iBuddhistMissionary, iConfucianMissionary, iTaoistMissionary, iZoroastrianMissionary, iWarrior, iMilitia, iAxeman, iLightSwordsman, iVulture, iDogSoldier, 
iSwordsman, iJaguar, iLegion, iGallicWarrior, iAucac, iHeavySwordsman, iSamurai, iHuscarl, iPombos, iSpearman, 
iHoplite, iImmortal, iImpi, iHeavySpearman, iPikeman, iLandsknecht, iRozwiWarrior, iArquebusier, iJanissary, iAskari, iQizilbash, 
iMohawk, iMusketeer, iMusketman, iRedcoat, iMinuteman, iKarolin, iRifleman, iGrenadier, iAlbionLegion, iAntiTank, iInfantry, 
iBersagliere, iDigger, iSamInfantry, iMobileSam, iMarine, iNavySeal, iParatrooper, iMechanizedInfantry, iArcher, iAsharittuBowman, iMedjay, 
iSkirmisher, iHolkan, iKelebolo, iLongbowman, iPatiyodha, iRattanArcher, iCrossbowman, iChokonu, iChariot, iWarChariot, iHuluganni, 
iCidainh, iHorseman, iNumidianCavalry, iAsvaka, iHorseArcher, iCamelArcher, iKhampa, iLancer, iKeshik, iCataphract, 
iChangSuek, iRoyalMamluk, iYanLifida, iGhulamWarrior, iFarari, iPistolier, iCuirassier, iConquistador, iWingedHussar, iEightBanner, iMountedBrave, iCamelGunner, iHussar, 
iDragoon, iCossack, iGrenadierCavalry, iCavalry, iRurales, iKommando, iWarElephant, iBallistaElephant, iAtlasElephant, iTank, iPanzer, 
iMainBattleTank, iGunship, iCatapult, iHwacha, iTrebuchet, iBombard, iSiegeElephant, iCannon, iHeavyCannon, iArtillery, 
iMachineGun, iHowitzer, iMobileArtillery, iWorkboat, iGalley, iWaka, iBireme, iBalangay, iWarGalley, iHeavyGalley, iDharani,
iCog, iDhow, iGalleass, iCaravel, iCarrack, iGalleon, iEastIndiaman, iPrivateer, iOrangLaut, iCorsair, iFrigate, 
iShipOfTheLine, iIronclad, iTorpedoBoat, iCruiser, iTransport, iDestroyer, iCorvette, iBattleship, iMissileCruiser, iStealthDestroyer, 
iSubmarine, iNuclearSubmarine, iCarrier, iBiplane, iFighter, iJetFighter, iBomber, iStealthBomber, iGuidedMissile, iNuclearBomber, 
iICBM, iGreatProphet, iGreatArtist, iGreatScientist, iGreatMerchant, iGreatEngineer, iGreatStatesman, iGreatGeneral, iGreatSpy, iFemaleGreatProphet, 
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

iNumBuildings = 248
(iPalace, iWalls, iDun, iIya, iCastle, iCitadel, iStarFort, iPlaas, iBarracks, iIkhanda, iStable, iGer, 
iBunker, iBombShelters, iGranary, iTerrace, iSmokehouse, iKraal, iAqueduct, iBaray, iNoria, iStepwell, iBath, 
iReservoir, iHammam, iPharmacy, iAlchemist, iSewer, iPark, iHospital, iRecyclingCenter, iLighthouse, iTradingPost, 
iHarbor, iPort, iCustomsHouse, iFeitoria, iImmigrationOffice, iWharf, iPostOffice, iTambo, iDrydock, iAirport, iForge, iMint, 
iArtStudio, iFactory, iAssemblyPlant, iZaibatsu, iCoalPlant, iHydroPlant, iNuclearPlant, iSolarPlant, iElectricalGrid, iIndustrialPark, 
iPaganTemple, iMonument, iObelisk, iStele, iCandi, iEdict, iMalae, iTotemPole, iZiara, iPublicTransportation, iLibrary,
iEdubba, iTaixue, iHoTrai, iSangam, iUniversity, iSeowon, iGompa, iObservatory, iLaboratory, iResearchInstitute,
iWeaver, iMbwadi, iTheatre, iOdeon, iHippodrome, iPavilion, iAmphitheatre, iBallCourt, iCharreadaArena, iGarden, 
iCinema, iBroadcastTower, iMarket, iForum, iApothecary, iCaravanserai, iGlassmaker, iSouq, iBank, iRoyalExchange, iRiksbank, iPiaohao, iRailwayStation, 
iDepartmentStore, iMall, iSupermarket, iRefrigerationPlant, iCoffeehouse, iSalon, iDistillery, iHotel, iConstabulary, iMountedPolice, 
iCivicSquare, iRathaus, iSejmik, iDinh, iEstate, iMausoleum, iFazenda, iHacienda, iNewsPress, iCourthouse, iJail, 
iSacrificialAltar, iLevee, iDike, iIntelligenceAgency, iSecurityBureau, iJewishTemple, iJewishCathedral, iJewishMonastery, iJewishShrine, iOrthodoxTemple, 
iOrthodoxCathedral, iOrthodoxMonastery, iOrthodoxShrine, iCatholicChurch, iCatholicCathedral, iCatholicMonastery, iCatholicShrine, iProtestantTemple, iProtestantCathedral, iProtestantMonastery, 
iProtestantShrine, iIslamicTemple, iIslamicCathedral, iIslamicMonastery, iIslamicShrine, iHinduTemple, iHinduCathedral, iHinduMonastery, iHinduShrine, iBuddhistTemple, 
iBuddhistCathedral, iBuddhistMonastery, iBuddhistShrine, iConfucianTemple, iConfucianCathedral, iConfucianMonastery, iConfucianShrine, iTaoistTemple, iTaoistCathedral, iTaoistMonastery, 
iTaoistShrine, iZoroastrianTemple, iZoroastrianCathedral, iZoroastrianMonastery, iZoroastrianShrine, iAcademy, iStockExchange, iManufactory, iMuseum, iArmoury, 
iAdministrativeCenter, iSecretService, iTriumphalArch, iNationalTheatre, iTradingCompany, iIberianTradingCompany, iCentralBank, iNationalCollege, iNationalGallery, iNationalMonument,
iIronworks, iMilitaryAcademy, iNationalPark, iRedCross, iGreatSphinx, iGreatLighthouse, iGreatCothon, iTerracottaArmy, iTempleOfArtemis, iPyramids, 
iHangingGardens, iOracle, iMoaiStatues, iIshtarGate, iColossus, iParthenon, iStatueOfZeus, iShwedagonPaya, iKhajuraho, iGreatLibrary,
iMausoleumOfMaussollos, iFloatingGardens, iColosseum, iGreatWall, iTheodosianWalls, iMachuPicchu, iBorobudur, iGrandCanal, iHagiaSophia, iNotreDame, 
iTempleOfKukulkan, iHimejiCastle, iBlueMosque, iWatPreahPisnulok, iTopkapiPalace, iMezquita, iSistineChapel, iLeaningTower, iRedFort, iVersailles, 
iForbiddenPalace, iSpiralMinaret, iDomeOfTheRock, iUniversityOfSankore, iTajMahal, iSanMarcoBasilica, iPorcelainTower, iSaintBasilsCathedral, iHarmandirSahib, iTrafalgarSquare, 
iBrandenburgGate, iStatueOfLiberty, iPentagon, iLubyanka, iWestminsterPalace, iEiffelTower, iEmpireStateBuilding, iCERN, iWembley, iGraceland, 
iCristoRedentor, iItaipuDam, iHollywood, iUnitedNations, iCNTower, iSydneyOpera, iSpaceElevator, iGreatZimbabwe) = range(iNumBuildings)

iBeginWonders = iGreatSphinx # different from DLL constant because that includes national wonders

iTemple = iJewishTemple #generic
iCathedral = iJewishCathedral #generic
iMonastery = iJewishMonastery #generic
iShrine = iJewishShrine #generic

iPlague = iNumBuildings
iNumBuildingsPlague = iNumBuildings+1

#Civics
iNumCivics = 42
(iChiefdom, iDespotism, iMonarchy, iRepublic, iElective, iStateParty, iDemocracy,
iAuthority, iCitizenship, iVassalage, iMeritocracy, iCentralism, iIdeology, iConstitution,
iTraditionalism, iSlavery, iManorialism, iCasteSystem, iIndividualism, iTotalitarianism, iEgalitarianism,
iReciprocity, iRedistribution, iMerchantTrade, iRegulatedTrade, iFreeEnterprise, iCentralPlanning, iPublicWelfare,
iAnimism, iDeification, iClergy, iMonasticism, iTheocracy, iTolerance, iSecularism,
iSovereignty, iConquest, iTributaries, iIsolationism, iColonialism, iNationhood, iMultilateralism) = range(iNumCivics)

iNumCivicCategories = 6
(iCivicsGovernment, iCivicsLegitimacy, iCivicsSociety, iCivicsEconomy, iCivicsReligion, iCivicsTerritory) = range(iNumCivicCategories)

#Specialists
iNumSpecialists = 16
(iSpecialistCitizen, iSpecialistPriest, iSpecialistArtist, iSpecialistScientist, iSpecialistMerchant, iSpecialistEngineer, iSpecialistStatesman,
iSpecialistGreatProphet, iSpecialistGreatArtist, iSpecialistGreatScientist, iSpecialistGreatMerchant, iSpecialistGreatEngineer, iSpecialistGreatStatesman, iSpecialistGreatGeneral, iSpecialistGreatSpy, iSpecialistSlave) = range(iNumSpecialists)

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
lMiddleEast = [rAnatolia, rMesopotamia, rArabia, rEgypt, rMaghreb, rPersia, rCentralAsia]
lIndia = [rIndia, rDeccan]
lEastAsia = [rIndochina, rIndonesia, rChina, rKorea, rJapan, rManchuria, rTibet]
lAfrica = [rEgypt, rMaghreb, rEthiopia, rSouthAfrica, rWestAfrica]
lSouthAmerica = [rCaribbean, rMesoamerica, rBrazil, rArgentina, rPeru, rColombia]
lNorthAmerica = [rCanada, rAlaska, rUnitedStates]

iArea_Europe = 1000
iArea_MiddleEast = 1001
iArea_India = 1002
iArea_EastAsia = 1003
iArea_Africa = 1004
iArea_SouthAmerica = 1005
iArea_NorthAmerica = 1006

mercRegions = {
	iArea_Europe : set([rBritain, rIberia, rItaly, rBalkans, rEurope, rScandinavia, rRussia]),
	iArea_MiddleEast : set([rAnatolia, rMesopotamia, rArabia, rEgypt, rMaghreb, rPersia, rCentralAsia]),
	iArea_India : set([rIndia, rDeccan]),
	iArea_EastAsia : set([rIndochina, rIndonesia, rChina, rKorea, rJapan, rManchuria, rTibet]),
	iArea_Africa : set([rEgypt, rMaghreb, rEthiopia, rSouthAfrica, rWestAfrica]),
	iArea_SouthAmerica : set([rCaribbean, rMesoamerica, rBrazil, rArgentina, rPeru, rColombia]),
	iArea_NorthAmerica : set([rCanada, rAlaska, rUnitedStates]),
}

#Projects

iNumProjects = 11
(iManhattanProject, iTheInternet, iSDI, iApolloProgram, iSSCockpit, iSSLifeSupport, iSSStasisChamber, iSSDockingBay,
iSSEngine, iSSCasing, iSSThrusters) = range(iNumProjects)


#Eras

iNumEras = 7
(iAncient, iClassical, iMedieval, iRenaissance, iIndustrial, iGlobal, iDigital) = range (iNumEras)


#Improvements

iNumImprovements = 28
(iLandWorked, iWaterWorked, iCityRuins, iHut, iFarm, iPaddyField, iFishingBoats, iOceanFishery, iWhalingBoats, iMine, 
iWorkshop, iLumbermill, iWindmill, iWatermill, iPlantation, iSlavePlantation, iQuarry, iPasture, iCamp, iWell, 
iOffshorePlatform, iWinery, iCottage, iHamlet, iVillage, iTown, iFort, iForestPreserve) = range(iNumImprovements)

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

iNumLeaders = 143
(iLeaderBarbarian, iNativeLeader, iIndependentLeader, iAlexanderTheGreat, iAsoka, iAugustus, iBismarck, iBoudica, iBrennus, iCatherine, 
iCharlemagne, iChurchill, iCyrus, iDarius, iDeGaulle, iElizabeth, iFrederick, iGandhi, iGenghisKhan, iSargon, 
iHammurabi, iHannibal, iCleopatra, iHuaynaCapac, iIsabella, iJoao, iJuliusCaesar, iJustinian, iKublaiKhan, iLincoln, 
iLouis, iMansaMusa, iMao, iMehmed, iMontezuma, iNapoleon, iPacal, iPericles, iPeter, iQinShiHuang, 
iRamesses, iRagnar, iRoosevelt, iSaladin, iSittingBull, iStalin, iSuleiman, iSuryavarman, iOdaNobunaga, iVictoria, 
iWangKon, iWashington, iWillemVanOranje, iZaraYaqob, iKammu, iMeiji, iAkbar, iHiram, iHaileSelassie, iGustav, 
iMongkut, iPhilip, iBarbarossa, iCharles, iFrancis, iIvan, iAfonso, iAtaturk, iMaria, iHitler,
iFranco, iAlexanderII, iCavour, iAbbas, iKhomeini, iTaizong, iHongwu, iDharmasetu, iHayamWuruk, iSuharto, 
iShahuji, iNaresuan, iAlpArslan, iBaibars, iNasser, iAlfred, iTrudeau, iChandragupta, iTughluq, iBasil, 
iRahman, iRajendra, iLobsangGyatso, iSobieski, iVatavelli, iMbemba, iHarun, iSongtsen, iCasimir, iYaqub, 
iLorenzo, iSantaAnna, iJuarez, iCardenas, iPedro, iSanMartin, iPeron, iBolivar, iAhoeitu, iKrishnaDevaRaya, 
iMussolini, iSejong, iBhutto, iPilsudski, iWalesa, iGerhardsen, iVargas, iMacDonald, iCastilla, iWilliam,
iGeorge, iChristian, iGustavVasa, iKarl, iCurtin, iMenzies, iMustasim, iKangxi, iCixi, iOduduwa, iEwuare,
iAminatu, iLapuLapu, iKruger, iMandela, iShirazi, iDawud, iBarghash, iTrung, iChieuHoang, iHoChiMinh, iRusvingo, iMutota) = range(iNumLeaders)

resurrectionLeaders = {
	iChina : iHongwu,
	iIndia : iShahuji,
	iEgypt : iBaibars,
}

rebirthLeaders = {
	iMaya : iBolivar,
	iPersia : iAbbas,
	iAztecs : iJuarez,
}

tTradingCompanyPlotLists = (
[(109, 33)], #Spain
[(101, 37), (101, 36), (102, 36), (102, 35), (103, 35), (103, 34), (104, 34), (104, 33)], #France
[(95, 37), (94, 37), (94, 36), (94, 35), (94, 34), (93, 34), (93, 33), (92, 33), (92, 32), (88, 33), (88, 34), (88, 35)], #England
[(82, 34), (89, 31), (101, 29), (105, 39), (93, 28), (93, 27), (71, 17), (69, 13), (54, 26), (62, 20)], #Portugal
[(99, 28), (99, 27), (100, 27), (100, 26), (101, 26), (104, 25), (105, 25), (106, 25), (107, 24), (104, 27), (105, 27), (106, 27), (104, 28), (106, 28), (105, 29), (106, 29)] #Netherlands
)

lSecondaryCivs = [iHarappa, iPolynesia, iTamils, iTibet, iMoors, iPoland, iCongo, iArgentina, iBrazil]

lMongolCivs = [iPersia, iByzantium, iArabia, iRussia, iMughals]

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

iNumSpawnTypes = 3
(iForcedSpawn, iNoSpawn, iConditionalSpawn) = range(iNumSpawnTypes)