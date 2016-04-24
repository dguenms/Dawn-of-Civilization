# Rhye's and Fall of Civilization - Constants
# globals

from CvPythonExtensions import *
gc = CyGlobalContext()

iWorldX = 124
iWorldY = 68

# initialise player variables to player IDs from WBS
iNumPlayers = 44
(iEgypt, iChina, iBabylonia, iHarappa, iGreece, iIndia, iPhoenicia, iPolynesia, iPersia, iRome, 
iTamils, iEthiopia, iKorea, iMaya, iByzantium, iJapan, iVikings, iArabia, iTibet, iKhmer, 
iIndonesia, iMoors, iSpain, iFrance, iEngland, iHolyRome, iRussia, iMali, iPoland, iPortugal, 
iInca, iItaly, iMongolia, iAztecs, iMughals, iTurkey, iThailand, iCongo, iNetherlands, iGermany,
iAmerica, iArgentina, iBrazil, iCanada) = range(iNumPlayers)

(pEgypt, pChina, pBabylonia, pHarappa, pGreece, pIndia, pPhoenicia, pPolynesia, pPersia, pRome, 
pTamils, pEthiopia, pKorea, pMaya, pByzantium, pJapan, pVikings, pArabia, pTibet, pKhmer, 
pIndonesia, pMoors, pSpain, pFrance, pEngland, pHolyRome, pRussia, pMali, pPoland, pPortugal, 
pInca, pItaly, pMongolia, pAztecs, pMughals, pTurkey, pThailand, pCongo, pNetherlands, pGermany, 
pAmerica, pArgentina, pBrazil, pCanada) = [gc.getPlayer(i) for i in range(iNumPlayers)]

(teamEgypt, teamChina, teamBabylonia, teamHarappa, teamGreece, teamIndia, teamPhoenicia, teamPolynesia, teamPersia, teamRome, 
teamTamils, teamEthiopia, teamKorea, teamMaya, teamByzantium, teamJapan, teamVikings, teamArabia, teamTibet, teamKhmer, 
teamIndonesia, teamMoors, teamSpain, teamFrance, teamEngland, teamHolyRome, teamRussia, teamMali, teamPoland, teamPortugal, 
teamInca, teamItaly, teamMongolia, teamAztecs, teamMughals, teamTurkey, teamThailand, teamCongo, teamNetherlands, teamGermany, 
teamAmerica, teamArgentina, teamBrazil, teamCanada) = [gc.getTeam(i) for i in range(iNumPlayers)]

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
iNumCivilizations = 57
(iCivEgypt, iCivChina, iCivBabylonia, iCivHarappa, iCivGreece, iCivIndia, iCivPhoenicia, iCivPolynesia, iCivPersia, iCivRome,
iCivTamils, iCivEthiopia, iCivKorea, iCivMaya, iCivByzantium, iCivJapan, iCivVikings, iCivArabia, iCivTibet, iCivKhmer,
iCivIndonesia, iCivMoors, iCivSpain, iCivFrance, iCivEngland, iCivHolyRome, iCivRussia, iCivMali, iCivPoland, iCivPortugal,
iCivInca, iCivItaly, iCivMongolia, iCivAztecs, iCivMughals, iCivTurkey, iCivThailand, iCivCongo, iCivIran, iCivNetherlands, iCivGermany,
iCivAmerica, iCivArgentina, iCivMexico, iCivColombia, iCivBrazil, iCivCanada,
iCivIndependent, iCivIndependent2, iCivNative, iCivCeltia, iCivSeljuks, iCivBarbarian, iCivNativeAmericans, iCivSumeria, iCivZulu, iCivMinor) = range(iNumCivilizations)

#for Congresses and Victory
lCivGroups = [[iGreece, iRome, iByzantium, iVikings, iMoors, iSpain, iFrance, iEngland, iHolyRome, iRussia, iNetherlands, iItaly, iPoland, iPortugal, iGermany],  #Euros
		[iIndia, iChina, iHarappa, iPolynesia, iPersia, iJapan, iTamils, iKorea, iByzantium, iTibet, iKhmer, iIndonesia, iRussia, iMongolia, iMughals, iThailand], #Asian
		[iEgypt, iBabylonia, iPersia, iByzantium, iArabia, iTurkey, iPhoenicia], #MiddleEastern
		[iEgypt, iGreece, iPhoenicia, iRome, iByzantium, iMoors], #Mediterranean
		[iEgypt, iPhoenicia, iEthiopia, iMali, iCongo], #African
		[iMaya, iInca, iAztecs, iAmerica, iArgentina, iBrazil, iCanada]] #American

lCivStabilityGroups = [[iVikings, iSpain, iFrance, iEngland, iHolyRome, iRussia, iNetherlands, iPoland, iPortugal, iItaly, iGermany],  #Euros
		[iIndia, iChina, iHarappa, iPolynesia, iJapan, iKorea, iTibet, iKhmer, iIndonesia, iMongolia, iThailand, iTamils], #Asian
		[iBabylonia, iPersia, iArabia, iTurkey, iMughals], #MiddleEastern
		[iEgypt, iGreece, iPhoenicia, iRome, iEthiopia, iByzantium, iMoors, iMali, iCongo], #Mediterranean
		[iMaya, iInca, iAztecs, iAmerica, iArgentina, iBrazil, iCanada]] #American
		
lTechGroups = [[iRome, iGreece, iByzantium, iVikings, iSpain, iFrance, iEngland, iHolyRome, iRussia, iNetherlands, iPoland, iPortugal, iItaly, iGermany, iAmerica, iArgentina, iBrazil, iCanada], #Europe and NA
	       [iEgypt, iBabylonia, iHarappa, iIndia, iPhoenicia, iPersia, iEthiopia, iArabia, iMoors, iMali, iTurkey, iMughals, iTamils, iCongo], #Middle East
	       [iChina, iKorea, iJapan, iTibet, iKhmer, iIndonesia, iMongolia, iThailand], #Far East
	       [iPolynesia, iMaya, iInca, iAztecs]] #Native America


lCivBioOldWorld = [iEgypt, iIndia, iChina, iBabylonia, iHarappa, iGreece, iPolynesia, iPersia, iPhoenicia, iRome, iJapan, iTamils, 
		   iEthiopia, iKorea, iByzantium, iVikings, iArabia, iTibet, iKhmer, iIndonesia, iMoors, iSpain, iFrance, iEngland, iHolyRome, iRussia, 
		   iNetherlands, iMali, iTurkey, iPoland, iPortugal, iItaly, iMongolia, iAmerica, iMughals, iThailand, iCongo, iGermany, 
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
iNumMinorCities = 37

# scripted conquerors
iNumConquests = 10

#neighbours
lNeighbours = [
[iBabylonia, iGreece, iPersia, iPhoenicia, iRome, iEthiopia, iByzantium, iArabia, iMoors, iTurkey], #Egypt
[iIndia, iJapan, iKorea, iTibet, iKhmer, iMongolia, iThailand], #China
[iEgypt, iGreece, iPersia, iTurkey, iMongolia, iPhoenicia, iByzantium], #Babylonia
[iIndia, iPersia, iTamils, iTibet, iMughals], #Harappa
[iPersia, iPhoenicia, iRome, iByzantium, iHolyRome, iRussia, iTurkey, iItaly], #Greece
[iChina, iHarappa, iPersia, iTamils, iTibet, iKhmer, iMongolia, iMughals, iThailand], #India
[iEgypt, iGreece, iRome, iSpain, iMali, iPortugal, iBabylonia, iPersia, iArabia, iMoors, iTurkey, iItaly], #Carthage
[], # Polynesia
[iIndia, iBabylonia, iHarappa, iGreece, iByzantium, iTurkey, iMongolia, iPhoenicia, iMughals], #Persia
[iEgypt, iBabylonia, iGreece, iPhoenicia, iSpain, iFrance, iHolyRome, iPortugal, iItaly, iGermany], #Rome
[iHarappa, iIndia, iKhmer, iIndonesia, iMughals, iThailand], #Tamils
[iEgypt, iArabia, iMali, iCongo], #Ethiopia
[iChina, iKorea, iMongolia], #Korea
[iSpain, iInca, iAztecs, iAmerica], #Maya
[iEgypt, iBabylonia, iGreece, iPersia, iArabia, iRussia], #Byzantium
[iChina, iKorea, iKhmer, iMongolia, iThailand], #Japan
[iFrance, iEngland, iHolyRome, iRussia, iPoland, iNetherlands, iGermany], #Vikings
[iEgypt, iBabylonia, iPersia, iEthiopia, iByzantium, iTurkey, iPhoenicia], #Arabia
[iChina, iHarappa, iIndia, iMongolia, iMughals], #Tibet
[iIndia, iChina, iTamils, iJapan, iIndonesia, iThailand], #Khmer
[iIndia, iJapan, iKhmer, iThailand, iTamils], #Indonesia
[iEgypt, iSpain, iPortugal, iMali], #Moors
[iPhoenicia, iRome, iMoors, iFrance, iEngland, iPortugal], #Spain
[iRome, iVikings, iSpain, iEngland, iHolyRome, iNetherlands, iPortugal, iItaly, iGermany], #France
[iRome, iVikings, iSpain, iFrance, iHolyRome, iNetherlands, iGermany], #England
[iRome, iVikings, iFrance, iEngland, iNetherlands, iItaly, iPoland, iGermany], #Holy Rome
[iPersia, iByzantium, iVikings, iPoland, iTurkey, iMongolia, iGermany], #Russia
[iEgypt, iPhoenicia, iEthiopia, iMoors, iCongo], #Mali
[iVikings, iHolyRome, iRussia, iGermany], #Poland
[iPhoenicia, iRome, iSpain, iFrance], #Portugal
[iSpain, iAztecs, iAmerica, iArgentina, iBrazil], #Inca
[iGreece, iPhoenicia, iRome, iFrance, iHolyRome], #Italy
[iIndia, iChina, iPersia, iJapan, iKorea, iTibet, iRussia, iTurkey], #Mongolia
[iSpain, iInca, iAmerica], #Aztec
[iHarappa, iIndia, iPersia, iTamils, iTibet], #Mughals
[iBabylonia, iGreece, iPersia, iByzantium, iRussia, iMongolia, iPhoenicia], #Turkey
[iIndia, iChina, iJapan, iIndonesia, iKhmer, iTamils], #Thailand
[iEthiopia, iMali], #Congo
[iVikings, iFrance, iEngland, iHolyRome, iGermany], #Netherlands
[iRome, iVikings, iFrance, iEngland, iHolyRome, iRussia, iPoland, iNetherlands], #Germany
[iJapan, iSpain, iFrance, iEngland, iRussia, iInca, iAztecs], #America
[iSpain, iPortugal, iInca, iBrazil], #Argentina
[iSpain, iPortugal, iInca, iArgentina], #Brazil
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
[iEgypt, iGreece, iPhoenicia], #Rome
[iHarappa, iIndia], #Tamils
[iEgypt], #Ethiopia
[iChina], #Korea
[], #Maya
[iGreece], #Byzantium
[iKorea], #Japan
[], #Vikings
[iEgypt, iPersia, iByzantium], #Arabia
[iChina, iHarappa, iIndia], #Tibet
[iIndia], #Khmer
[iKhmer], #Indonesia
[], #Moors
[iPhoenicia, iRome], #Spain
[iRome], #France
[], #England
[iGreece, iRome, iVikings], #Holy Rome
[iPersia, iGreece, iByzantium], #Russia
[iPhoenicia, iEthiopia, iArabia, iMoors], #Mali
[iVikings, iHolyRome], #Poland
[iPhoenicia, iRome], #Portugal
[], #Inca
[iByzantium, iHolyRome], #Italy
[iChina, iJapan, iKorea, iArabia, iTibet, iKhmer, iRussia], #Mongolia
[iMaya], #Aztec
[iHarappa, iIndia, iPersia, iArabia, iTibet], #Mughals
[iBabylonia, iGreece, iPersia, iByzantium, iArabia], #Turkey
[iIndia, iChina, iJapan, iKhmer, iIndonesia], #Thailand
[], #Congo
[iRome, iHolyRome], #Netherlands
[iHolyRome, iPoland], #Germany
[iSpain, iFrance, iEngland, iNetherlands, iPortugal, iAztecs, iMaya], #America
[iSpain, iPortugal, iInca], #Argentina
[iSpain, iPortugal, iInca], #Brazil
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
-50,					# Korea
60, # 145, #60AD			# Maya
330,					# Byzantium
525, # 97, #660BC			# Japan
551, # 177, #551AD			# Vikings
620, # 183, #622AD			# Arabia
630,					# Tibet
655, # 187, #657AD			# Khmer
700,					# Indonesia
711,					# Moors
722, # 193, #718AD			# Spain
750, # 196, #751AD			# France
820, # 203, #829AD			# England
840, # 205, #843AD			# Holy Rome
860, # 207, #860AD			# Russia
989, # 220, #989AD			# Mali
1025,					# Poland
1130, # 234, #1128AD			# Portugal
1150, # 236, #1150AD			# Inca
1167, # Italy				# Italy
1190, # 240, #1190AD			# Mongolia
1195, # 241, #1195AD			# Aztecs
1206,					# Mughals
1280, # 249, #1280AD (1071AD)		# Turkey
1350,					# Thailand
1390,					# Congo
1580, # 281, #922AD # Leoreth: 1500 AD	# Netherlands
1700,					# Germany
1775, # 346, #1775AD #332 for 1733AD	# America
1810,					# Argentina
1822,					# Brazil
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
1255, #Mongol invasion			# Korea
900,					# Maya
1204, #fourth crusade			# Byzantium
2020,					# Japan
1300,					# Vikings
900,					# Arabia
1500,					# Tibet
1200, # earlier so that the Thai can spawn # Khmer
1500,					# Indonesia
1500,					# Moors
2020,					# Spain
2020,					# France
2020,					# England
2020, #1648,				# Holy Rome
2020,					# Russia
1600,					# Mali
1650,					# Poland
2020,					# Portugal
1533,					# Inca
2020,					# Italy
1368,					# Mongolia
1521,					# Aztecs
1640,					# Mughals
2020,					# Turkey
2020,					# Thailand
1800,					# Congo
2020,					# Netherlands
2020,					# Germany
2020,					# America
2020,					# Argentina
2020,					# Brazil
2020)					# Canada

dVictoryYears = {
iCivEgypt : (-850, -100, 170),
iCivChina : (1000, -1, 1800),
iCivBabylonia : (-1, -850, -700),
iCivHarappa : (-1600, -1500, -800),
iCivGreece : (-1, -250, -330),
iCivIndia : (-100, 700, 1200),
iCivPhoenicia : (-300, -100, 200),
iCivPolynesia : (800, 1000, 1200),
iCivPersia : (140, 350, 350),
iCivRome : (100, 320, -1),
iCivTamils : (800, 1000, 1200),
iCivEthiopia : (-1, 600, 1910),
iCivKorea : (1200, -1, -1),
iCivMaya : (600, 900, -1),
iCivByzantium : (1000, 1200, 1450),
iCivJapan : (1600, 1940, -1),
iCivVikings : (1050, 1100, 1500),
iCivArabia : (1300, 1300, -1),
iCivTibet : (1000, 1400, 1700),
iCivKhmer : (1200, 1450, 1450),
iCivIndonesia : (1300, 1500, 1940),
iCivMoors : (1200, 1300, 1650),
iCivSpain : (-1, 1650, 1650),
iCivFrance : (1700, 1800, 1900),
iCivEngland : (1730, 1800, -1),
iCivHolyRome : (1200, -1, 1700),
iCivRussia : (1920, -1, 1950),
iCivMali : (1350, 1500, 1700),
iCivPoland : (1400, -1, 1600),
iCivPortugal : (1550, 1650, 1700),
iCivInca : (1500, 1550, 1700),
iCivItaly : (1500, 1600, 1930),
iCivMongolia : (1300, -1, 1500),
iCivAztecs : (1520, 1650, -1),
iCivMughals : (1500, 1660, 1750),
iCivTurkey : (1550, 1700, 1800),
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
-1,				# Korea
1814,	# Colombia
-1,				# Byzantium
-1,				# Japan
-1,				# Vikings
-1,				# Arabia
-1,				# Tibet
-1,				# Khmer
-1,				# Indonesia
-1,				# Moors
-1,				# Spain
-1,				# France
-1,				# England
-1,				# Holy Rome
-1,				# Russia
-1,				# Mali
-1,				# Poland
-1,				# Portugal
-1,				# Inca
-1,				# Italy	
-1,				# Mongolia
1810,	# Mexico
-1,				# Mughals
-1,				# Turkey
-1,				# Thailand
-1,				# Congo
-1,				# Netherlands
-1,				# Germany
-1,				# America
-1,				# Argentina
-1,				# Brazil
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
-1,		# Korea
iCivColombia,	# Maya
-1,		# Byzantium
-1,		# Japan
-1,		# Vikings
-1,		# Arabia
-1,		# Tibet
-1,		# Khmer
-1,		# Indonesia
-1,		# Moors
-1,		# Spain
-1,		# France
-1,		# England
-1,		# Holy Rome
-1,		# Russia
-1,		# Mali
-1,		# Poland
-1,		# Portugal
-1,		# Inca
-1,		# Italy	
-1,		# Mongolia
iCivMexico,	# Aztecs
-1,		# Mughals
-1,		# Turkey
-1,		# Thailand
-1,		# Netherlands
-1,		# Germany
-1,		# America
-1,		# Argentina
-1,		# Brazil
-1,		# Canada
)

tResurrectionIntervals = (
[(900, 1300), (1800, 2020)], #Egypt
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
[(1800, 2020)], #Korea
[(0, 800)], #Maya
[(1100, 1280)], #Byzantium
[(1800, 2020)], #Japan
[(1520, 2020)], #Vikings
[(1900, 2020)], #Arabia
[],		#Tibet
[(1950, 2020)], #Khmer
[(1900, 2020)], #Indonesia
[(1000, 2020)],	#Moors
[(1700, 2020)], #Spain
[(1700, 2020)], #France
[(1700, 2020)], #England
[(1800, 2020)], #Holy Rome
[(1280, 1550), (1700, 2020)], #Russia
[(1340, 1590)], #Mali
[(1920, 2020)], #Poland
[(1700, 2020)], #Portugal
[(1800, 1930)], #Inca
[(1820, 2020)], #Italy
[(1910, 2020)], #Mongolia
[], 		#Aztec
[(1940, 2020)], #Mughals
[(1700, 2020)], #Turkey
[(1700, 2020)], #Thailand
[],		#Congo
[(1700, 2020)], #Netherlands
[(1840, 2020)], #Germany
[(1770, 2020)], #America
[(1810, 2020)], #Argentina
[(1820, 2020)], #Brazil
[(1867, 2020)], #Canada
)

tYear = (
("3000 ", "TXT_KEY_BC"),	# Egypt
("3000 ", "TXT_KEY_BC"),	# China
("3000 ", "TXT_KEY_BC"),	# Babylonia
("3000 ", "TXT_KEY_BC"),	# Harappa
("1600 ", "TXT_KEY_BC"),	# Greece
("1500 ", "TXT_KEY_BC"),	# India
("1200 ", "TXT_KEY_BC"),	# Phoenicia
("1000 ", "TXT_KEY_BC"),	# Polynesia
("850 ", "TXT_KEY_BC"),		# Persia
("760 ", "TXT_KEY_BC"),		# Rome
("300 ", "TXT_KEY_BC"),		# Tamils
("295 ", "TXT_KEY_BC"),		# Ethiopia
("50 ", "TXT_KEY_BC"),		# Korea
("65 ", "TXT_KEY_AD"),		# Maya
("330 ", "TXT_KEY_AD"),		# Byzantium
("525 ", "TXT_KEY_AD"),		# Japan
("545 ", "TXT_KEY_AD"),		# Vikings
("620 ", "TXT_KEY_AD"),		# Arabia
("630 ", "TXT_KEY_AD"),		# Tibet
("660 ", "TXT_KEY_AD"),		# Khmer
("700 ", "TXT_KEY_AD"),		# Indonesia
("711 ", "TXT_KEY_AD"),		# Moors
("722 ", "TXT_KEY_AD"),		# Spain
("750 ", "TXT_KEY_AD"),		# France
("820 ", "TXT_KEY_AD"),		# England
("840 ", "TXT_KEY_AD"),		# Holy Rome
("860 ", "TXT_KEY_AD"),		# Russia
("980 ", "TXT_KEY_AD"),		# Mali
("1025 ", "TXT_KEY_AD"),	# Poland
("1130 ", "TXT_KEY_AD"),	# Portugal
("1150 ", "TXT_KEY_AD"),	# Inca
("1167 ", "TXT_KEY_AD"),	# Italy
("1190 ", "TXT_KEY_AD"),	# Mongolia
("1200 ", "TXT_KEY_AD"),	# Aztecs
("1206 ", "TXT_KEY_AD"),	# Mughals
("1280 ", "TXT_KEY_AD"),	# Turkey
("1350 ", "TXT_KEY_AD"),	# Thailand
("1390 ", "TXT_KEY_AD"),	# Congo
("1500 ", "TXT_KEY_AD"),	# Netherlands
("1701 ", "TXT_KEY_AD"),	# Germany
("1775 ", "TXT_KEY_AD"),	# America
("1810 ", "TXT_KEY_AD"),	# Argentina
("1822 ", "TXT_KEY_AD"),	# Brazil
("1867 ", "TXT_KEY_AD"))	# Canada

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
("TXT_KEY_UHV_PHO1", "TXT_KEY_UHV_PHO2", "TXT_KEY_UHV_PHO3_MARATHON"),
("TXT_KEY_UHV_PLY1", "TXT_KEY_UHV_PLY2", "TXT_KEY_UHV_PLY3"),
("TXT_KEY_UHV_PER1_MARATHON", "TXT_KEY_UHV_PER2_MARATHON", "TXT_KEY_UHV_PER3_MARATHON"),
("TXT_KEY_UHV_ROM1_MARATHON", "TXT_KEY_UHV_ROM2_MARATHON", "TXT_KEY_UHV_ROM3"),
("TXT_KEY_UHV_TAM1_MARATHON", "TXT_KEY_UHV_TAM2", "TXT_KEY_UHV_TAM3_MARATHON"),
("TXT_KEY_UHV_ETH1", "TXT_KEY_UHV_ETH2_MARATHON", "TXT_KEY_UHV_ETH3"),
("TXT_KEY_UHV_KOR1", "TXT_KEY_UHV_KOR2", "TXT_KEY_UHV_KOR3"),
("TXT_KEY_UHV_MAY1_MARATHON", "TXT_KEY_UHV_MAY2", "TXT_KEY_UHV_MAY3"),
("TXT_KEY_UHV_BYZ1_MARATHON", "TXT_KEY_UHV_BYZ2", "TXT_KEY_UHV_BYZ3"),
("TXT_KEY_UHV_JAP1_MARATHON", "TXT_KEY_UHV_JAP2", "TXT_KEY_UHV_JAP3"),
("TXT_KEY_UHV_VIK1", "TXT_KEY_UHV_VIK2", "TXT_KEY_UHV_VIK3_MARATHON"),
("TXT_KEY_UHV_ARA1", "TXT_KEY_UHV_ARA2", "TXT_KEY_UHV_ARA3"),
("TXT_KEY_UHV_TIB1", "TXT_KEY_UHV_TIB2", "TXT_KEY_UHV_TIB3"),
("TXT_KEY_UHV_KHM1", "TXT_KEY_UHV_KHM2", "TXT_KEY_UHV_KHM3_MARATHON"),
("TXT_KEY_UHV_INO1", "TXT_KEY_UHV_INO2", "TXT_KEY_UHV_INO3"),
("TXT_KEY_UHV_MOO1", "TXT_KEY_UHV_MOO2", "TXT_KEY_UHV_MOO3"),
("TXT_KEY_UHV_SPA1", "TXT_KEY_UHV_SPA2", "TXT_KEY_UHV_SPA3"),
("TXT_KEY_UHV_FRA1_MARATHON", "TXT_KEY_UHV_FRA2", "TXT_KEY_UHV_FRA3"),
("TXT_KEY_UHV_ENG1", "TXT_KEY_UHV_ENG2", "TXT_KEY_UHV_ENG3"),
("TXT_KEY_UHV_HRE1", "TXT_KEY_UHV_HRE2", "TXT_KEY_UHV_HRE3"),
("TXT_KEY_UHV_RUS1", "TXT_KEY_UHV_RUS2", "TXT_KEY_UHV_RUS3"),
("TXT_KEY_UHV_MAL1", "TXT_KEY_UHV_MAL2", "TXT_KEY_UHV_MAL3_MARATHON"),
("TXT_KEY_UHV_POL1", "TXT_KEY_UHV_POL2", "TXT_KEY_UHV_POL3"),
("TXT_KEY_UHV_POR1", "TXT_KEY_UHV_POR2", "TXT_KEY_UHV_POR3"),
("TXT_KEY_UHV_INC1", "TXT_KEY_UHV_INC2_MARATHON", "TXT_KEY_UHV_INC3"),
("TXT_KEY_UHV_ITA1", "TXT_KEY_UHV_ITA2", "TXT_KEY_UHV_ITA3"),
("TXT_KEY_UHV_MON1", "TXT_KEY_UHV_MON2", "TXT_KEY_UHV_MON3"),
("TXT_KEY_UHV_AZT1", "TXT_KEY_UHV_AZT2", "TXT_KEY_UHV_AZT3"),
("TXT_KEY_UHV_MUG1", "TXT_KEY_UHV_MUG2", "TXT_KEY_UHV_MUG3_MARATHON"),
("TXT_KEY_UHV_TUR1", "TXT_KEY_UHV_TUR2", "TXT_KEY_UHV_TUR3"),
("TXT_KEY_UHV_THA1", "TXT_KEY_UHV_THA2", "TXT_KEY_UHV_THA3"),
("TXT_KEY_UHV_CON1", "TXT_KEY_UHV_CON2_MARATHON", "TXT_KEY_UHV_CON3"),
("TXT_KEY_UHV_HOL1", "TXT_KEY_UHV_HOL2", "TXT_KEY_UHV_HOL3"),
("TXT_KEY_UHV_GER1", "TXT_KEY_UHV_GER2", "TXT_KEY_UHV_GER3"),
("TXT_KEY_UHV_AME1", "TXT_KEY_UHV_AME2", "TXT_KEY_UHV_AME3"),
("TXT_KEY_UHV_ARG1", "TXT_KEY_UHV_ARG2_MARATHON", "TXT_KEY_UHV_ARG3"),
("TXT_KEY_UHV_BRA1", "TXT_KEY_UHV_BRA2", "TXT_KEY_UHV_BRA3"),
("TXT_KEY_UHV_CAN1", "TXT_KEY_UHV_CAN2", "TXT_KEY_UHV_CAN3"),
),
( # Epic
("TXT_KEY_UHV_EGY1_EPIC", "TXT_KEY_UHV_EGY2_EPIC", "TXT_KEY_UHV_EGY3_EPIC"),
("TXT_KEY_UHV_CHI1", "TXT_KEY_UHV_CHI2", "TXT_KEY_UHV_CHI3"),
("TXT_KEY_UHV_BAB1", "TXT_KEY_UHV_BAB2_EPIC", "TXT_KEY_UHV_BAB3_EPIC"),
("TXT_KEY_UHV_HAR1", "TXT_KEY_UHV_HAR2", "TXT_KEY_UHV_HAR3"),
("TXT_KEY_UHV_GRE1", "TXT_KEY_UHV_GRE2_EPIC", "TXT_KEY_UHV_GRE3_EPIC"),
("TXT_KEY_UHV_IND1_EPIC", "TXT_KEY_UHV_IND2", "TXT_KEY_UHV_IND3"),
("TXT_KEY_UHV_PHO1", "TXT_KEY_UHV_PHO2", "TXT_KEY_UHV_PHO3_EPIC"),
("TXT_KEY_UHV_PLY1", "TXT_KEY_UHV_PLY2", "TXT_KEY_UHV_PLY3"),
("TXT_KEY_UHV_PER1_EPIC", "TXT_KEY_UHV_PER2_EPIC", "TXT_KEY_UHV_PER3_EPIC"),
("TXT_KEY_UHV_ROM1_EPIC", "TXT_KEY_UHV_ROM2_EPIC", "TXT_KEY_UHV_ROM3"),
("TXT_KEY_UHV_TAM1_EPIC", "TXT_KEY_UHV_TAM2", "TXT_KEY_UHV_TAM3_EPIC"),
("TXT_KEY_UHV_ETH1", "TXT_KEY_UHV_ETH2_EPIC", "TXT_KEY_UHV_ETH3"),
("TXT_KEY_UHV_KOR1", "TXT_KEY_UHV_KOR2", "TXT_KEY_UHV_KOR3"),
("TXT_KEY_UHV_MAY1_EPIC", "TXT_KEY_UHV_MAY2", "TXT_KEY_UHV_MAY3"),
("TXT_KEY_UHV_BYZ1_EPIC", "TXT_KEY_UHV_BYZ2", "TXT_KEY_UHV_BYZ3"),
("TXT_KEY_UHV_JAP1_EPIC", "TXT_KEY_UHV_JAP2", "TXT_KEY_UHV_JAP3"),
("TXT_KEY_UHV_VIK1", "TXT_KEY_UHV_VIK2", "TXT_KEY_UHV_VIK3_EPIC"),
("TXT_KEY_UHV_ARA1", "TXT_KEY_UHV_ARA2", "TXT_KEY_UHV_ARA3"),
("TXT_KEY_UHV_TIB1", "TXT_KEY_UHV_TIB2", "TXT_KEY_UHV_TIB3"),
("TXT_KEY_UHV_KHM1", "TXT_KEY_UHV_KHM2", "TXT_KEY_UHV_KHM3_EPIC"),
("TXT_KEY_UHV_INO1", "TXT_KEY_UHV_INO2", "TXT_KEY_UHV_INO3"),
("TXT_KEY_UHV_MOO1", "TXT_KEY_UHV_MOO2", "TXT_KEY_UHV_MOO3"),
("TXT_KEY_UHV_SPA1", "TXT_KEY_UHV_SPA2", "TXT_KEY_UHV_SPA3"),
("TXT_KEY_UHV_FRA1_EPIC", "TXT_KEY_UHV_FRA2", "TXT_KEY_UHV_FRA3"),
("TXT_KEY_UHV_ENG1", "TXT_KEY_UHV_ENG2", "TXT_KEY_UHV_ENG3"),
("TXT_KEY_UHV_HRE1", "TXT_KEY_UHV_HRE2", "TXT_KEY_UHV_HRE3"),
("TXT_KEY_UHV_RUS1", "TXT_KEY_UHV_RUS2", "TXT_KEY_UHV_RUS3"),
("TXT_KEY_UHV_MAL1", "TXT_KEY_UHV_MAL2", "TXT_KEY_UHV_MAL3_EPIC"),
("TXT_KEY_UHV_POL1", "TXT_KEY_UHV_POL2", "TXT_KEY_UHV_POL3"),
("TXT_KEY_UHV_POR1", "TXT_KEY_UHV_POR2", "TXT_KEY_UHV_POR3"),
("TXT_KEY_UHV_INC1", "TXT_KEY_UHV_INC2_EPIC", "TXT_KEY_UHV_INC3"),
("TXT_KEY_UHV_ITA1", "TXT_KEY_UHV_ITA2", "TXT_KEY_UHV_ITA3"),
("TXT_KEY_UHV_MON1", "TXT_KEY_UHV_MON2", "TXT_KEY_UHV_MON3"),
("TXT_KEY_UHV_AZT1", "TXT_KEY_UHV_AZT2", "TXT_KEY_UHV_AZT3"),
("TXT_KEY_UHV_MUG1", "TXT_KEY_UHV_MUG2", "TXT_KEY_UHV_MUG3_EPIC"),
("TXT_KEY_UHV_TUR1", "TXT_KEY_UHV_TUR2", "TXT_KEY_UHV_TUR3"),
("TXT_KEY_UHV_THA1", "TXT_KEY_UHV_THA2", "TXT_KEY_UHV_THA3"),
("TXT_KEY_UHV_CON1", "TXT_KEY_UHV_CON2_EPIC", "TXT_KEY_UHV_CON3"),
("TXT_KEY_UHV_HOL1", "TXT_KEY_UHV_HOL2", "TXT_KEY_UHV_HOL3"),
("TXT_KEY_UHV_GER1", "TXT_KEY_UHV_GER2", "TXT_KEY_UHV_GER3"),
("TXT_KEY_UHV_AME1", "TXT_KEY_UHV_AME2", "TXT_KEY_UHV_AME3"),
("TXT_KEY_UHV_ARG1", "TXT_KEY_UHV_ARG2_EPIC", "TXT_KEY_UHV_ARG3"),
("TXT_KEY_UHV_BRA1", "TXT_KEY_UHV_BRA2", "TXT_KEY_UHV_BRA3"),
("TXT_KEY_UHV_CAN1", "TXT_KEY_UHV_CAN2", "TXT_KEY_UHV_CAN3"),
),
( # Normal
("TXT_KEY_UHV_EGY1", "TXT_KEY_UHV_EGY2", "TXT_KEY_UHV_EGY3"),
("TXT_KEY_UHV_CHI1", "TXT_KEY_UHV_CHI2", "TXT_KEY_UHV_CHI3"),
("TXT_KEY_UHV_BAB1", "TXT_KEY_UHV_BAB2", "TXT_KEY_UHV_BAB3"),
("TXT_KEY_UHV_HAR1", "TXT_KEY_UHV_HAR2", "TXT_KEY_UHV_HAR3"),
("TXT_KEY_UHV_GRE1", "TXT_KEY_UHV_GRE2", "TXT_KEY_UHV_GRE3"),
("TXT_KEY_UHV_IND1", "TXT_KEY_UHV_IND2", "TXT_KEY_UHV_IND3"),
("TXT_KEY_UHV_PHO1", "TXT_KEY_UHV_PHO2", "TXT_KEY_UHV_PHO3"),
("TXT_KEY_UHV_PLY1", "TXT_KEY_UHV_PLY2", "TXT_KEY_UHV_PLY3"),
("TXT_KEY_UHV_PER1", "TXT_KEY_UHV_PER2", "TXT_KEY_UHV_PER3"),
("TXT_KEY_UHV_ROM1", "TXT_KEY_UHV_ROM2", "TXT_KEY_UHV_ROM3"),
("TXT_KEY_UHV_TAM1", "TXT_KEY_UHV_TAM2", "TXT_KEY_UHV_TAM3"),
("TXT_KEY_UHV_ETH1", "TXT_KEY_UHV_ETH2", "TXT_KEY_UHV_ETH3"),
("TXT_KEY_UHV_KOR1", "TXT_KEY_UHV_KOR2", "TXT_KEY_UHV_KOR3"),
("TXT_KEY_UHV_MAY1", "TXT_KEY_UHV_MAY2", "TXT_KEY_UHV_MAY3"),
("TXT_KEY_UHV_BYZ1", "TXT_KEY_UHV_BYZ2", "TXT_KEY_UHV_BYZ3"),
("TXT_KEY_UHV_JAP1", "TXT_KEY_UHV_JAP2", "TXT_KEY_UHV_JAP3"),
("TXT_KEY_UHV_VIK1", "TXT_KEY_UHV_VIK2", "TXT_KEY_UHV_VIK3"),
("TXT_KEY_UHV_ARA1", "TXT_KEY_UHV_ARA2", "TXT_KEY_UHV_ARA3"),
("TXT_KEY_UHV_TIB1", "TXT_KEY_UHV_TIB2", "TXT_KEY_UHV_TIB3"),
("TXT_KEY_UHV_KHM1", "TXT_KEY_UHV_KHM2", "TXT_KEY_UHV_KHM3"),
("TXT_KEY_UHV_INO1", "TXT_KEY_UHV_INO2", "TXT_KEY_UHV_INO3"),
("TXT_KEY_UHV_MOO1", "TXT_KEY_UHV_MOO2", "TXT_KEY_UHV_MOO3"),
("TXT_KEY_UHV_SPA1", "TXT_KEY_UHV_SPA2", "TXT_KEY_UHV_SPA3"),
("TXT_KEY_UHV_FRA1", "TXT_KEY_UHV_FRA2", "TXT_KEY_UHV_FRA3"),
("TXT_KEY_UHV_ENG1", "TXT_KEY_UHV_ENG2", "TXT_KEY_UHV_ENG3"),
("TXT_KEY_UHV_HRE1", "TXT_KEY_UHV_HRE2", "TXT_KEY_UHV_HRE3"),
("TXT_KEY_UHV_RUS1", "TXT_KEY_UHV_RUS2", "TXT_KEY_UHV_RUS3"),
("TXT_KEY_UHV_MAL1", "TXT_KEY_UHV_MAL2", "TXT_KEY_UHV_MAL3"),
("TXT_KEY_UHV_POL1", "TXT_KEY_UHV_POL2", "TXT_KEY_UHV_POL3"),
("TXT_KEY_UHV_POR1", "TXT_KEY_UHV_POR2", "TXT_KEY_UHV_POR3"),
("TXT_KEY_UHV_INC1", "TXT_KEY_UHV_INC2", "TXT_KEY_UHV_INC3"),
("TXT_KEY_UHV_ITA1", "TXT_KEY_UHV_ITA2", "TXT_KEY_UHV_ITA3"),
("TXT_KEY_UHV_MON1", "TXT_KEY_UHV_MON2", "TXT_KEY_UHV_MON3"),
("TXT_KEY_UHV_AZT1", "TXT_KEY_UHV_AZT2", "TXT_KEY_UHV_AZT3"),
("TXT_KEY_UHV_MUG1", "TXT_KEY_UHV_MUG2", "TXT_KEY_UHV_MUG3"),
("TXT_KEY_UHV_TUR1", "TXT_KEY_UHV_TUR2", "TXT_KEY_UHV_TUR3"),
("TXT_KEY_UHV_THA1", "TXT_KEY_UHV_THA2", "TXT_KEY_UHV_THA3"),
("TXT_KEY_UHV_CON1", "TXT_KEY_UHV_CON2", "TXT_KEY_UHV_CON3"),
("TXT_KEY_UHV_HOL1", "TXT_KEY_UHV_HOL2", "TXT_KEY_UHV_HOL3"),
("TXT_KEY_UHV_GER1", "TXT_KEY_UHV_GER2", "TXT_KEY_UHV_GER3"),
("TXT_KEY_UHV_AME1", "TXT_KEY_UHV_AME2", "TXT_KEY_UHV_AME3"),
("TXT_KEY_UHV_ARG1", "TXT_KEY_UHV_ARG2", "TXT_KEY_UHV_ARG3"),
("TXT_KEY_UHV_BRA1", "TXT_KEY_UHV_BRA2", "TXT_KEY_UHV_BRA3"),
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
("TXT_KEY_UHV_PHO1", "TXT_KEY_UHV_PHO2", "TXT_KEY_UHV_PHO3_MARATHON"),
("TXT_KEY_UHV_PLY1", "TXT_KEY_UHV_PLY2", "TXT_KEY_UHV_PLY3"),
("TXT_KEY_UHV_IRA1", "TXT_KEY_UHV_IRA2", "TXT_KEY_UHV_IRA3_MARATHON"),
("TXT_KEY_UHV_ITA1", "TXT_KEY_UHV_ITA2", "TXT_KEY_UHV_ITA3"),
("TXT_KEY_UHV_TAM1_MARATHON", "TXT_KEY_UHV_TAM2", "TXT_KEY_UHV_TAM3_MARATHON"),
("TXT_KEY_UHV_ETH1", "TXT_KEY_UHV_ETH2", "TXT_KEY_UHV_ETH3"),
("TXT_KEY_UHV_KOR1", "TXT_KEY_UHV_KOR2", "TXT_KEY_UHV_KOR3"),
("TXT_KEY_UHV_COL1", "TXT_KEY_UHV_COL2", "TXT_KEY_UHV_COL3_MARATHON"),
("TXT_KEY_UHV_BYZ1_MARATHON", "TXT_KEY_UHV_BYZ2", "TXT_KEY_UHV_BYZ3"),
("TXT_KEY_UHV_JAP1_MARATHON", "TXT_KEY_UHV_JAP2", "TXT_KEY_UHV_JAP3"),
("TXT_KEY_UHV_VIK1", "TXT_KEY_UHV_VIK2", "TXT_KEY_UHV_VIK3_MARATHON"),
("TXT_KEY_UHV_ARA1", "TXT_KEY_UHV_ARA2", "TXT_KEY_UHV_ARA3"),
("TXT_KEY_UHV_TIB1", "TXT_KEY_UHV_TIB2", "TXT_KEY_UHV_TIB3"),
("TXT_KEY_UHV_KHM1", "TXT_KEY_UHV_KHM2", "TXT_KEY_UHV_KHM3_MARATHON"),
("TXT_KEY_UHV_INO1", "TXT_KEY_UHV_INO2", "TXT_KEY_UHV_INO3"),
("TXT_KEY_UHV_MOO1", "TXT_KEY_UHV_MOO2", "TXT_KEY_UHV_MOO3"),
("TXT_KEY_UHV_SPA1", "TXT_KEY_UHV_SPA2", "TXT_KEY_UHV_SPA3"),
("TXT_KEY_UHV_FRA1", "TXT_KEY_UHV_FRA2", "TXT_KEY_UHV_FRA3"),
("TXT_KEY_UHV_ENG1", "TXT_KEY_UHV_ENG2", "TXT_KEY_UHV_ENG3"),
("TXT_KEY_UHV_HRE1", "TXT_KEY_UHV_HRE2", "TXT_KEY_UHV_HRE3"),
("TXT_KEY_UHV_RUS1", "TXT_KEY_UHV_RUS2", "TXT_KEY_UHV_RUS3"),
("TXT_KEY_UHV_MAL1", "TXT_KEY_UHV_MAL2_MARATHON", "TXT_KEY_UHV_MAL3_MARATHON"),
("TXT_KEY_UHV_POL1", "TXT_KEY_UHV_POL2", "TXT_KEY_UHV_POL3"),
("TXT_KEY_UHV_POR1", "TXT_KEY_UHV_POR2", "TXT_KEY_UHV_POR3"),
("TXT_KEY_UHV_INC1", "TXT_KEY_UHV_INC2_MARATHON", "TXT_KEY_UHV_INC3"),
("TXT_KEY_UHV_ITA1", "TXT_KEY_UHV_ITA2", "TXT_KEY_UHV_ITA3"),
("TXT_KEY_UHV_MON1", "TXT_KEY_UHV_MON2", "TXT_KEY_UHV_MON3"),
("TXT_KEY_UHV_MEX1", "TXT_KEY_UHV_MEX2", "TXT_KEY_UHV_MEX3"),
("TXT_KEY_UHV_MUG1", "TXT_KEY_UHV_MUG2", "TXT_KEY_UHV_MUG3_MARATHON"),
("TXT_KEY_UHV_TUR1", "TXT_KEY_UHV_TUR2", "TXT_KEY_UHV_TUR3"),
("TXT_KEY_UHV_THA1", "TXT_KEY_UHV_THA2", "TXT_KEY_UHV_THA3"),
("TXT_KEY_UHV_CON1", "TXT_KEY_UHV_CON2_MARATHON", "TXT_KEY_UHV_CON3"),
("TXT_KEY_UHV_HOL1", "TXT_KEY_UHV_HOL2", "TXT_KEY_UHV_HOL3"),
("TXT_KEY_UHV_GER1", "TXT_KEY_UHV_GER2", "TXT_KEY_UHV_GER3"),
("TXT_KEY_UHV_AME1", "TXT_KEY_UHV_AME2", "TXT_KEY_UHV_AME3"),
("TXT_KEY_UHV_ARG1", "TXT_KEY_UHV_ARG2_MARATHON", "TXT_KEY_UHV_ARG3"),
("TXT_KEY_UHV_BRA1", "TXT_KEY_UHV_BRA2", "TXT_KEY_UHV_BRA3"),
("TXT_KEY_UHV_CAN1", "TXT_KEY_UHV_CAN2", "TXT_KEY_UHV_CAN3")
),
( # Epic
("TXT_KEY_UHV_EGY1_EPIC", "TXT_KEY_UHV_EGY2_EPIC", "TXT_KEY_UHV_EGY3_EPIC"),
("TXT_KEY_UHV_CHI1", "TXT_KEY_UHV_CHI2", "TXT_KEY_UHV_CHI3"),
("TXT_KEY_UHV_BAB1", "TXT_KEY_UHV_BAB2_NOTURN", "TXT_KEY_UHV_BAB3_NOTURN"),
("TXT_KEY_UHV_HAR1", "TXT_KEY_UHV_HAR2", "TXT_KEY_UHV_HAR3"),
("TXT_KEY_UHV_GRE1", "TXT_KEY_UHV_GRE2_NOTURN", "TXT_KEY_UHV_GRE3"),
("TXT_KEY_UHV_IND1", "TXT_KEY_UHV_IND2", "TXT_KEY_UHV_IND3"),
("TXT_KEY_UHV_PHO1", "TXT_KEY_UHV_PHO2", "TXT_KEY_UHV_PHO3_EPIC"),
("TXT_KEY_UHV_PLY1", "TXT_KEY_UHV_PLY2", "TXT_KEY_UHV_PLY3"),
("TXT_KEY_UHV_IRA1", "TXT_KEY_UHV_IRA2", "TXT_KEY_UHV_IRA3_EPIC"),
("TXT_KEY_UHV_ITA1", "TXT_KEY_UHV_ITA2", "TXT_KEY_UHV_ITA3"),
("TXT_KEY_UHV_TAM1_EPIC", "TXT_KEY_UHV_TAM2", "TXT_KEY_UHV_TAM3_EPIC"),
("TXT_KEY_UHV_ETH1", "TXT_KEY_UHV_ETH2", "TXT_KEY_UHV_ETH3"),
("TXT_KEY_UHV_KOR1", "TXT_KEY_UHV_KOR2", "TXT_KEY_UHV_KOR3"),
("TXT_KEY_UHV_COL1", "TXT_KEY_UHV_COL2", "TXT_KEY_UHV_COL3_EPIC"),
("TXT_KEY_UHV_BYZ1_EPIC", "TXT_KEY_UHV_BYZ2", "TXT_KEY_UHV_BYZ3"),
("TXT_KEY_UHV_JAP1_EPIC", "TXT_KEY_UHV_JAP2", "TXT_KEY_UHV_JAP3"),
("TXT_KEY_UHV_VIK1", "TXT_KEY_UHV_VIK2", "TXT_KEY_UHV_VIK3_EPIC"),
("TXT_KEY_UHV_ARA1", "TXT_KEY_UHV_ARA2", "TXT_KEY_UHV_ARA3"),
("TXT_KEY_UHV_TIB1", "TXT_KEY_UHV_TIB2", "TXT_KEY_UHV_TIB3"),
("TXT_KEY_UHV_KHM1", "TXT_KEY_UHV_KHM2", "TXT_KEY_UHV_KHM3_EPIC"),
("TXT_KEY_UHV_INO1", "TXT_KEY_UHV_INO2", "TXT_KEY_UHV_INO3"),
("TXT_KEY_UHV_MOO1", "TXT_KEY_UHV_MOO2", "TXT_KEY_UHV_MOO3"),
("TXT_KEY_UHV_SPA1", "TXT_KEY_UHV_SPA2", "TXT_KEY_UHV_SPA3"),
("TXT_KEY_UHV_FRA1", "TXT_KEY_UHV_FRA2", "TXT_KEY_UHV_FRA3"),
("TXT_KEY_UHV_ENG1", "TXT_KEY_UHV_ENG2", "TXT_KEY_UHV_ENG3"),
("TXT_KEY_UHV_HRE1", "TXT_KEY_UHV_HRE2", "TXT_KEY_UHV_HRE3"),
("TXT_KEY_UHV_RUS1", "TXT_KEY_UHV_RUS2", "TXT_KEY_UHV_RUS3"),
("TXT_KEY_UHV_MAL1", "TXT_KEY_UHV_MAL2_EPIC", "TXT_KEY_UHV_MAL3_EPIC"),
("TXT_KEY_UHV_POL1", "TXT_KEY_UHV_POL2", "TXT_KEY_UHV_POL3"),
("TXT_KEY_UHV_POR1", "TXT_KEY_UHV_POR2", "TXT_KEY_UHV_POR3"),
("TXT_KEY_UHV_INC1", "TXT_KEY_UHV_INC2_EPIC", "TXT_KEY_UHV_INC3"),
("TXT_KEY_UHV_ITA1", "TXT_KEY_UHV_ITA2", "TXT_KEY_UHV_ITA3"),
("TXT_KEY_UHV_MON1", "TXT_KEY_UHV_MON2", "TXT_KEY_UHV_MON3"),
("TXT_KEY_UHV_MEX1", "TXT_KEY_UHV_MEX2", "TXT_KEY_UHV_MEX3"),
("TXT_KEY_UHV_MUG1", "TXT_KEY_UHV_MUG2", "TXT_KEY_UHV_MUG3_EPIC"),
("TXT_KEY_UHV_TUR1", "TXT_KEY_UHV_TUR2", "TXT_KEY_UHV_TUR3"),
("TXT_KEY_UHV_THA1", "TXT_KEY_UHV_THA2", "TXT_KEY_UHV_THA3"),
("TXT_KEY_UHV_CON1", "TXT_KEY_UHV_CON2_EPIC", "TXT_KEY_UHV_CON3"),
("TXT_KEY_UHV_HOL1", "TXT_KEY_UHV_HOL2", "TXT_KEY_UHV_HOL3"),
("TXT_KEY_UHV_GER1", "TXT_KEY_UHV_GER2", "TXT_KEY_UHV_GER3"),
("TXT_KEY_UHV_AME1", "TXT_KEY_UHV_AME2", "TXT_KEY_UHV_AME3"),
("TXT_KEY_UHV_ARG1", "TXT_KEY_UHV_ARG2_EPIC", "TXT_KEY_UHV_ARG3"),
("TXT_KEY_UHV_BRA1", "TXT_KEY_UHV_BRA2", "TXT_KEY_UHV_BRA3"),
("TXT_KEY_UHV_CAN1", "TXT_KEY_UHV_CAN2", "TXT_KEY_UHV_CAN3")
),
( # Normal
("TXT_KEY_UHV_EGY1", "TXT_KEY_UHV_EGY2", "TXT_KEY_UHV_EGY3"),
("TXT_KEY_UHV_CHI1", "TXT_KEY_UHV_CHI2", "TXT_KEY_UHV_CHI3"),
("TXT_KEY_UHV_BAB1", "TXT_KEY_UHV_BAB2", "TXT_KEY_UHV_BAB3"),
("TXT_KEY_UHV_HAR1", "TXT_KEY_UHV_HAR2", "TXT_KEY_UHV_HAR3"),
("TXT_KEY_UHV_GRE1", "TXT_KEY_UHV_GRE2", "TXT_KEY_UHV_GRE3"),
("TXT_KEY_UHV_IND1", "TXT_KEY_UHV_IND2", "TXT_KEY_UHV_IND3"),
("TXT_KEY_UHV_PHO1", "TXT_KEY_UHV_PHO2", "TXT_KEY_UHV_PHO3"),
("TXT_KEY_UHV_PLY1", "TXT_KEY_UHV_PLY2", "TXT_KEY_UHV_PLY3"),
("TXT_KEY_UHV_IRA1", "TXT_KEY_UHV_IRA2", "TXT_KEY_UHV_IRA3"),
("TXT_KEY_UHV_ITA1", "TXT_KEY_UHV_ITA2", "TXT_KEY_UHV_ITA3"),
("TXT_KEY_UHV_TAM1", "TXT_KEY_UHV_TAM2", "TXT_KEY_UHV_TAM3"),
("TXT_KEY_UHV_ETH1", "TXT_KEY_UHV_ETH2", "TXT_KEY_UHV_ETH3"),
("TXT_KEY_UHV_KOR1", "TXT_KEY_UHV_KOR2", "TXT_KEY_UHV_KOR3"),
("TXT_KEY_UHV_COL1", "TXT_KEY_UHV_COL2", "TXT_KEY_UHV_COL3"),
("TXT_KEY_UHV_BYZ1", "TXT_KEY_UHV_BYZ2", "TXT_KEY_UHV_BYZ3"),
("TXT_KEY_UHV_JAP1", "TXT_KEY_UHV_JAP2", "TXT_KEY_UHV_JAP3"),
("TXT_KEY_UHV_VIK1", "TXT_KEY_UHV_VIK2", "TXT_KEY_UHV_VIK3"),
("TXT_KEY_UHV_ARA1", "TXT_KEY_UHV_ARA2", "TXT_KEY_UHV_ARA3"),
("TXT_KEY_UHV_TIB1", "TXT_KEY_UHV_TIB2", "TXT_KEY_UHV_TIB3"),
("TXT_KEY_UHV_KHM1", "TXT_KEY_UHV_KHM2", "TXT_KEY_UHV_KHM3"),
("TXT_KEY_UHV_INO1", "TXT_KEY_UHV_INO2", "TXT_KEY_UHV_INO3"),
("TXT_KEY_UHV_MOO1", "TXT_KEY_UHV_MOO2", "TXT_KEY_UHV_MOO3"),
("TXT_KEY_UHV_SPA1", "TXT_KEY_UHV_SPA2", "TXT_KEY_UHV_SPA3"),
("TXT_KEY_UHV_FRA1", "TXT_KEY_UHV_FRA2", "TXT_KEY_UHV_FRA3"),
("TXT_KEY_UHV_ENG1", "TXT_KEY_UHV_ENG2", "TXT_KEY_UHV_ENG3"),
("TXT_KEY_UHV_HRE1", "TXT_KEY_UHV_HRE2", "TXT_KEY_UHV_HRE3"),
("TXT_KEY_UHV_RUS1", "TXT_KEY_UHV_RUS2", "TXT_KEY_UHV_RUS3"),
("TXT_KEY_UHV_MAL1", "TXT_KEY_UHV_MAL2", "TXT_KEY_UHV_MAL3"),
("TXT_KEY_UHV_POL1", "TXT_KEY_UHV_POL2", "TXT_KEY_UHV_POL3"),
("TXT_KEY_UHV_POR1", "TXT_KEY_UHV_POR2", "TXT_KEY_UHV_POR3"),
("TXT_KEY_UHV_INC1", "TXT_KEY_UHV_INC2", "TXT_KEY_UHV_INC3"),
("TXT_KEY_UHV_ITA1", "TXT_KEY_UHV_ITA2", "TXT_KEY_UHV_ITA3"),
("TXT_KEY_UHV_MON1", "TXT_KEY_UHV_MON2", "TXT_KEY_UHV_MON3"),
("TXT_KEY_UHV_MEX1", "TXT_KEY_UHV_MEX2", "TXT_KEY_UHV_MEX3"),
("TXT_KEY_UHV_MUG1", "TXT_KEY_UHV_MUG2", "TXT_KEY_UHV_MUG3"),
("TXT_KEY_UHV_TUR1", "TXT_KEY_UHV_TUR2", "TXT_KEY_UHV_TUR3"),
("TXT_KEY_UHV_THA1", "TXT_KEY_UHV_THA2", "TXT_KEY_UHV_THA3"),
("TXT_KEY_UHV_CON1", "TXT_KEY_UHV_CON", "TXT_KEY_UHV_CON3"),
("TXT_KEY_UHV_HOL1", "TXT_KEY_UHV_HOL2", "TXT_KEY_UHV_HOL3"),
("TXT_KEY_UHV_GER1", "TXT_KEY_UHV_GER2", "TXT_KEY_UHV_GER3"),
("TXT_KEY_UHV_AME1", "TXT_KEY_UHV_AME2", "TXT_KEY_UHV_AME3"),
("TXT_KEY_UHV_ARG1", "TXT_KEY_UHV_ARG2", "TXT_KEY_UHV_ARG3"),
("TXT_KEY_UHV_BRA1", "TXT_KEY_UHV_BRA2", "TXT_KEY_UHV_BRA3"),
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
iPhoenicia	:	"TXT_KEY_DOM_PHOENICIA",
iPolynesia	:	"TXT_KEY_DOM_POLYNESIA",
iPersia		:	"TXT_KEY_DOM_PERSIA",
iRome		:	"TXT_KEY_DOM_ROME",
iTamils		:	"TXT_KEY_DOM_TAMILS",
iEthiopia	:	"TXT_KEY_DOM_ETHIOPIA",
iJapan		:	"TXT_KEY_DOM_JAPAN",
iKorea		:	"TXT_KEY_DOM_KOREA",
iMaya		:	"TXT_KEY_DOM_MAYA",
iByzantium	:	"TXT_KEY_DOM_BYZANTIUM",
iVikings	:	"TXT_KEY_DOM_VIKINGS",
iArabia		:	"TXT_KEY_DOM_ARABIA",
iTibet		:	"TXT_KEY_DOM_TIBET",
iMoors		:	"TXT_KEY_DOM_MOORS",
iIndonesia	:	"TXT_KEY_DOM_INDONESIA",
iKhmer		:	"TXT_KEY_DOM_KHMER",
iSpain		:	"TXT_KEY_DOM_SPAIN",
iFrance		:	"TXT_KEY_DOM_FRANCE",
iEngland	:	"TXT_KEY_DOM_ENGLAND",
iHolyRome	:	"TXT_KEY_DOM_HOLY_ROME",
iRussia		:	"TXT_KEY_DOM_RUSSIA",
iMali		:	"TXT_KEY_DOM_MALI",
iPoland		:	"TXT_KEY_DOM_POLAND",
iItaly		:	"TXT_KEY_DOM_ITALY",
iPortugal	:	"TXT_KEY_DOM_PORTUGAL",
iInca		:	"TXT_KEY_DOM_INCA",
iAztecs		:	"TXT_KEY_DOM_AZTECS",
iMongolia	:	"TXT_KEY_DOM_MONGOLIA",
iMughals	:	"TXT_KEY_DOM_MUGHALS",
iTurkey		:	"TXT_KEY_DOM_TURKEY",
iThailand	:	"TXT_KEY_DOM_THAILAND",
iCongo		:	"TXT_KEY_DOM_CONGO",
iNetherlands	:	"TXT_KEY_DOM_NETHERLANDS",
iGermany	:	"TXT_KEY_DOM_GERMANY",
iAmerica	:	"TXT_KEY_DOM_AMERICA",
iArgentina	:	"TXT_KEY_DOM_ARGENTINA",
iBrazil		:	"TXT_KEY_DOM_BRAZIL",
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
iChina		:	"TXT_KEY_DOM_CHINA_1700AD",
iIndia		:	"TXT_KEY_DOM_INDIA_1700AD",
iPersia		:	"TXT_KEY_DOM_PERSIA_1700AD",
iTamils		:	"TXT_KEY_DOM_TAMILS_1700AD",
iKorea		:	"TXT_KEY_DOM_KOREA_1700AD",
iJapan		:	"TXT_KEY_DOM_JAPAN_1700AD",
iVikings	:	"TXT_KEY_DOM_SWEDEN_1700AD",
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
200,	# Korea
200,	# Maya
400,	# Byzantium
100,	# Japan
150,	# Viking
300,	# Arabia
50,	# Tibet
200,	# Khmer
300,	# Indonesia
200,	# Moors
200,	# Spain
150,	# France
200,	# England
150,	# Holy Rome
200,	# Russia
600,	# Mali
100,	# Poland
200,	# Portugal
700,	# Inca
350,	# Italy
250,	# Mongolia
600,	# Aztecs
400,	# Mughals
300,	# Turkey
800,	# Thailand
300,	# Congo
600,	# Netherlands
800,	# Germany
1500,	# America
1200,	# Argentina
1600,	# Brazil
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
[iBabylonia,iBabylonia,iGreece,iPhoenicia,iPhoenicia,iIndia,iIndia], #Persia
#[iEgypt,iGreece,iGreece,iPhoenicia,iPhoenicia], #Rome
[], # rome for testing
[], #Tamils
[], #Ethiopia
[], #Korea
[], #Maya
[iGreece, iPersia], #Byzantium
[], #Japan
[iEngland,iEngland,iFrance,iIndependent,iIndependent2], #Vikings
[iEgypt,iEgypt,iEgypt,iBabylonia,iBabylonia,iGreece,iPersia,iPhoenicia,iRome,iByzantium,iByzantium,iSpain,iFrance,iCeltia,iCeltia,iIndependent,iIndependent2], #Arabia
[], #Tibet
[], #Khmer
[iKhmer, iKhmer], #Indonesia
[], #Moors
[], #Spain
[], #France
[], #England
[iRome,iArabia,iArabia], #Holy Rome
[], #Russia
[], #Mali
[], #Poland
[], #Portugal
[], #Inca
[], #Italy
[iChina,iChina,iChina,iKorea,iKorea,iIndependent,iIndependent,iIndependent2,iIndependent2], #Mongolia
[iMaya], #Aztec
[iIndia, iIndia], #Mughals
[iEgypt,iEgypt,iBabylonia,iGreece,iGreece,iArabia,iArabia,iArabia,iByzantium,iByzantium,iByzantium], #Turkey
[iKhmer, iKhmer, iKhmer], #Thailand
[], #Congo
[], #Netherlands
[iHolyRome, iPoland], #Germany
[iIndependent,iIndependent2], #America
[iSpain, iSpain, iIndependent,iIndependent2], #Argentina
[iIndependent,iIndependent2], #Brazil
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
[iBabylonia, iPhoenicia], #Persia
[iGreece], #Rome
[], #Tamils
[], #Ethiopia
[], #Korea
[], #Maya
[iGreece], #Byzantium
[], #Japan
[], #Vikings
[iEgypt, iBabylonia, iPhoenicia, iPersia], #Arabia
[], #Tibet
[], #Khmer
[], #Indonesia
[], #Moors
[iMoors], #Spain
[], #France
[], #England
[iRome], #Holy Rome
[], #Russia
[], #Mali
[], #Poland
[], #Portugal
[], #Inca
[], #Italy
[iChina], #Mongolia
[iMaya], #Aztec
[iIndia], #Mughals
[iArabia, iEgypt], #Turkey
[iKhmer], #Thailand
[], #Congo
[], #Netherlands
[], #Germany
[], #America
[], #Argentina
[], #Brazil
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
0, #Korea
1, #Maya
1, #Byzantium
1, #Japan
2, #Viking
2, #Arabia
1, #Tibet
2, #Khmer
1, #Indonesia
1, #Moors
2, #Spain
1, #France
1, #England
3, #Holy Rome
1, #Russia
0, #Mali
1, #Poland
0, #Portugal
1, #Inca
0, #Italy
2, #Mongolia
1, #Aztec
1, #Mughals
2, #Turkey
0, #Thailand
0, #Congo
0, #Holland
2, #Germany
2, #America
0, #Argentina
0, #Brazil
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
    80, #Korea
    80, #Maya
    80, #Byzantium
    80, #Japan
    80, #Viking
    80, #Arabia
    80, #Tibet
    80, #Khmer
    80, #Indonesia
    80, #Moors
    80, #Spain  #60 in vanilla and Warlords
    80, #France #60 in vanilla and Warlords
    50, #England
    80, #Holy Rome #70 in vanilla and Warlords
    50, #Russia
    70, #Mali
    40, #Poland
    40, #Portugal
    70, #Inca
    60, #Italy
    70, #Mongolia
    50, #Aztec
    70, #Mughals
    70, #Turkey
    80, #Thailand
    80, #Congo
    40, #Holland
    80, #Germany
    50, #America
    60, #Argentina
    60, #Brazil
	60, #Canada
    100,
    100,
    100,
    100,
    100)


#RiseAndFall
tResurrectionProb = (
25, #Egypt
100, #China
30, #Babylonia
0, #Harappa
60, #Greece
20, #India
30, #Carthage
40, #Polynesia
70, #Persia
65, #Rome
10, #Tamils
80, #Ethopia
80, #Korea
30, #Maya
65, #Byzantium
100, #Japan
60, #Viking
100, #Arabia
60, #Tibet
60, #Khmer
80, #Indonesia
70, #Moors
100, #Spain
100, #France
100, #England
80, #Holy Rome
100, #Russia
30, #Mali
65, #Poland
100, #Portugal
70, #Inca
100, #Italy
80, #Mongolia
70, #Aztec
80, #Mughals
100, #Turkey
100, #Thailand
20, #Congo
100, #Holland
100, #Germany
100, #America
100, #Argentina
100, #Brazil
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
25, #Korea
35, #Maya
25, #Byzantium
25, #Japan
30, #Viking
30, #Arabia
50, #Tibet
30, #Khmer
30, #Indonesia
20, #Moors
20, #Spain
20, #France
20, #England
20, #Holy Rome
30, #Russia
35, #Mali
20, #Poland
30, #Portugal
35, #Inca
25, #Italy
20, #Mongolia
30, #Aztec
35, #Mughals
35, #Turkey
30, #Thailand
20, #Congo
30, #Holland
20, #Germany
30, #America
40, #Argentina
40, #Brazil
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
0, #Korea
0, #Maya
0, #Byzantium
0, #Japan
1, #Viking
0, #Arabia
0, #Tibet
0, #Khmer
0, #Indonesia
0, #Moors
7, #Spain
5, #France
6, #England
0, #Holy Rome
0, #Russia
0, #Mali
0, #Poland
6, #Portugal
0, #Inca
0, #Italy
0, #Mongolia
0, #Aztec
0, #Mughals
0, #Turkey
0, #Thailand
0, #Congo
6, #Holland
2, #Germany
0, #America
0, #Argentina
0, #Brazil
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

lCatholicStart = [iSpain, iFrance, iEngland, iHolyRome, iPoland, iPortugal, iItaly, iNetherlands, iGermany, iAmerica, iArgentina, iBrazil, iCanada]
lProtestantStart = [iNetherlands, iGermany, iAmerica]

# initialise tech variables to unit indices from XML

iNumTechs = 93
(iMysticism, iMeditation, iPolytheism, iPriesthood, iMonotheism, iMonarchy, iLiterature, iCodeOfLaws, iDrama, iFeudalism,
iTheology, iMusic, iCivilService, iGuilds, iDivineRight, iPatronage, iNationalism, iMilitaryTradition, iConstitution, iLiberalism,
iDemocracy, iCorporation, iFascism, iCommunism, iMassMedia, iEcology, iFishing, iWheel, iAgriculture, iPottery,
iAesthetics, iSailing, iWriting, iMathematics, iAlphabet, iCalendar, iCurrency, iPhilosophy, iPaper, iBanking, 
iEducation, iPrintingPress, iEconomics, iAstronomy, iChemistry, iScientificMethod, iPhysics, iBiology, iMedicine, iElectricity,
iCombustion, iFission, iFlight, iAdvancedFlight, iPlastics, iComposites, iStealth, iGenetics, iFiberOptics, iFusion,
iHunting, iMining, iArchery, iMasonry, iAnimalHusbandry, iBronzeWorking, iHorsebackRiding, iIronWorking, iMetalCasting, iCompass, 
iConstruction, iMachinery, iEngineering, iOptics, iGunpowder, iReplaceableParts, iMilitaryScience, iRifling, iSteamPower, iSteel, 
iAssemblyLine, iRailroad, iTechArtillery, iIndustrialism, iRadio, iRefrigeration, iSuperconfuctors, iComputers, iLaser, iRocketry, 
iSatellites, iRobotics, iFutureTech) = range(iNumTechs)

# initialise unit variables to unit indices from XML

iNumUnits = 164
(iLion, iBear, iPanther, iWolf, iSettler, iHarappanCityBuilder, iWorker, iBrazilianMadeireiro, iIndianPunjabiWorker, iScout, iExplorer, iSpy, iReligiousPersecutor,
iJewishMissionary, iOrthodoxMissionary, iCatholicMissionary, iProtestantMissionary, iIslamicMissionary, iHinduMissionary, iBuddhistMissionary, iConfucianMissionary,
iTaoistMissionary, iZoroastrianMissionary, iWarrior, iSwordsman, iAztecJaguar, iRomanLegion, iCelticGallicWarrior,
iAxeman, iGreekHoplite, iIncanAucac, iSumerianVulture, iNativeAmericanDogSoldier, iHeavySwordsman, iJapaneseSamurai, iVikingHuscarl, iCongolesePombos,
iSpearman, iPersianImmortal, iZuluImpi, iPikeman, iHolyRomanLandsknecht, iMusketman, iTurkishJanissary, iEthiopianAskari, 
iIranianQizilbash, iIroquoisMohawk, iFrenchMusketeer, iRifleman, iEnglishRedcoat, iAmericanMinuteman, iGrenadier, iColombianAlbionLegion, iAtInfantry, iInfantry, iItalianBersagliere,
iSamInfantry, iMobileSam, iMarine, iAmericanNavySeal, iParatrooper, iMechanizedInfantry, iArcher, iMandeSkirmisher, iBabylonAsharittuBowman, iMayanHolkan, iNubianMedjay,
iLongbowman, iIndianPatiyodha, iCrossbowman, iChineseChokonu, iChariot, iEgyptianWarChariot, iHittiteHuluganni, iCelticCidainh, iHorseArcher, iTibetanKhampa,
iNumidianCavalry, iKushanAsvaka, iKnight, iMongolianKeshik, iArabianCamelArcher, iByzantineCataphract, iThaiChangSuek, iSeljukGhulamWarrior,
iMandeFarari, iCuirassier, iSpanishConquistador, iPolishWingedHussar, iSiouxMountedBrave, iMoorishCamelGunner, iCavalry, iRussianCossack, iMexicanRurales,
iArgentineGrenadierCavalry, iWarElephant, iKhmerBallistaElephant, iPhoenicianAfricanWarElephant, iTank, iGermanPanzer, iMainBattleTank, iGunship, iCatapult, iKoreanHwacha,
iTrebuchet, iBombard, iMughalSiegeElephant, iCannon, iFrenchHeavyCannon, iMachineGun, iArtillery, iMobileArtillery, iWorkboat, iGalley, iPolynesianWaka, iPhoenicianBireme, iTrireme,
iCaravel, iPortugalCarrack, iTamilDharani, iGalleon, iDutchEastIndiaman, iPrivateer, iIndonesianOrangLaut, iMoorishCorsair, iFrigate,
iShipOfTheLine, iIronclad, iTransport, iDestroyer, iCanadianCorvette, iBattleship, iMissileCruiser, iStealthDestroyer, iSubmarine, iAttackSubmarine, iCarrier, iAirship, iFighter,
iJetFighter, iBomber, iStealthBomber, iGuidedMissile, iTacticalNuke, iIcbm, iGreatProphet, iGreatArtist, iGreatScientist, iGreatMerchant, iGreatEngineer, iGreatStatesman, iGreatGeneral,
iGreatSpy, iFemaleGreatProphet, iFemaleGreatArtist, iFemaleGreatScientist, iFemaleGreatMerchant, iFemaleGreatEngineer, iFemaleGreatStatesman, iFemaleGreatGeneral,
iFemaleGreatSpy, iSlave, iNativeSlave, iAztecSlave) = range(iNumUnits)

iMissionary = iJewishMissionary # generic

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
iNumBonuses = 40
(iAluminium, iCoal, iCopper, iHorse, iIron, iMarble, iOil, iStone, iUranium, iBanana, iClam, iCorn, iCow, iCrab,
iDeer, iFish, iPig, iRice, iSheep, iWheat, iCoffee, iCotton, iDye, iFur, iGems, iGold, iIncense, iIvory, iPearls, iSilk, iSilver, iSpices,
iSugar, iTea, iTobacco, iWine, iWhales, iSoccer, iSongs, iMovies) = range(iNumBonuses)

#Buildings (update Persian UHV every time this is changed)

iNumBuildings = 212
(iPalace, iWalls, iCelticDun, iCastle, iSpanishCitadel, iIncanTambo, iBarracks, iZuluIkhanda, iStable,
iMongolianGer, iBunker, iBombShelter, iGranary, iIncanTerrace, iSmokehouse, iAqueduct, iTurkishHammam, iKhmerBaray, iMoorishNoria, iHarappanBath, iIndianStepwell,
iHospital, iRecyclingCenter, iLighthouse, iVikingTradingPost, iHarbor, iCustomHouse, iPortugueseFeitoria, iDrydock, iAirport,
iForge, iMandeMint, iItalianArtStudio, iArabianAlchemist, iFactory, iGermanAssemblyPlant, iJapaneseZaibatsu, iCoalPlant, iHydroPlant, iNuclearPlant,
iIndustrialPark, iPaganTemple, iEgyptianObelisk, iEthiopianStele, iIndonesianCandi, iIndianEdict, iBabylonianZiggurat, iNativeAmericanTotemPole, iPublicTransportation,
iLibrary, iChineseTaixue, iThaiHoTrai, iTamilSangam, iUniversity, iKoreanSeowon, iTibetanGompa, iObservatory, iLaboratory, 
iRussianResearchInstitute, iTheatre, iGreekOdeon, iByzantineHippodrome, iChinesePavillion, iAmphitheatre, iMayanBallCourt, iMexicanCharreada, 
iPolynesianMalae, iBabylonianGarden, iBroadcastTower, iMarket, iRomanForum, iPersianApothecary, iIranianCaravanserai, iCongoleseMbwadi, iPhoenicianGlassmaker, 
iGrocer, iBrazilianFazenda, iColombianHacienda, iBank, iEnglishRoyalExchange, iSupermarket, iAmericanMall, iArgentineRefrigerationPlant, iCourthouse,
iAztecSacrificialAltar, iHolyRomanRathaus, iPolishSejmik, iJail, iFrenchSalon, iMughalMausoleum, iCanadianRoyalMountedPolice, iLevee, 
iDutchDike, iIntelligenceAgency, iSecurityBureau, iAcademy, iMilitaryAcademy, iAdministrativeCenter, iJewishTemple, iJewishCathedral, iJewishMonastery, iJewishShrine,
iOrthodoxTemple, iOrthodoxCathedral, iOrthodoxMonastery, iOrthodoxShrine, iCatholicTemple, iCatholicCathedral, iCatholicMonastery, iCatholicShrine, iProtestantTemple, 
iProtestantCathedral, iProtestantMonastery, iProtestantShrine, iIslamicTemple, iIslamicCathedral, iIslamicMonastery, iIslamicShrine, iHinduTemple, iHinduCathedral, 
iHinduMonastery, iHinduShrine, iBuddhistTemple, iBuddhistCathedral, iBuddhistMonastery, iBuddhistShrine, iConfucianTemple, iConfucianCathedral, iConfucianMonastery,
iConfucianShrine, iTaoistTemple, iTaoistCathedral, iTaoistMonastery, iTaoistShrine, iZoroastrianTemple, iZoroastrianCathedral,
iZoroastrianMonastery, iZoroastrianShrine, iTriumphalArch, iOperaHouse, iTradingCompany, iIberianTradingCompany, iStockExchange, iOlympicPark, iNationalGallery,
iIronWorks, iInterpol, iNationalPark, iRedCross, iGreatSphinx, iGreatLighthouse, iGreatCothon, iTerracottaArmy, iTempleOfArtemis,
iPyramids, iHangingGardens, iOracle, iMoaiStatues, iIshtarGate, iColossus, iParthenon, iStatueOfZeus,
iShwedagonPaya, iKhajuraho, iGreatLibrary, iMausoleumOfMaussollos, iFloatingGardens, iColosseum,
iGreatWall, iTheodosianWalls, iMachuPicchu, iBorobudur, iGrandCanal, iNotreDame, iTempleOfKukulkan, iHimejiCastle,
iBlueMosque, iAngkorWat, iTopkapiPalace, iLaMezquita, iHagiaSophia, iSistineChapel, iLeaningTower, iRedFort,
iVersailles, iForbiddenPalace, iSpiralMinaret, iDomeOfTheRock, iUniversityofSankore, iTajMahal, iSanMarcoBasilica, iPorcelainTower,
iStBasilsCathedral, iHarmandirSahib, iTrafalgarSquare, iBrandenburgGate, iStatueOfLiberty, iPentagon, iLubyanka, iWestminsterPalace, iMtRushmore,
iEiffelTower, iEmpireStateBuilding, iCERNResearchComplex, iWembley, iGraceland, iCristoRedentor, iThreeGorgesDam, iHollywood, iUnitedNations, iCNTower, iSpaceElevator) = range(iNumBuildings)

iBeginWonders = iGreatSphinx # different from DLL constant because that includes national wonders

iTemple = iJewishTemple #generic
iCathedral = iJewishCathedral #generic
iMonastery = iJewishMonastery #generic
iShrine = iJewishShrine #generic

iPlague = iNumBuildings
iNumBuildingsPlague = iNumBuildings+1

#Civics
iNumCivics = 36
(iCivicTyranny, iCivicDynasticism, iCivicCityStates, iCivicTheocracy, iCivicAutocracy, iCivicRepublic,
iCivicDirectRule, iCivicVassalage, iCivicAbsolutism, iCivicRepresentation, iCivicTotalitarianism, iCivicEgalitarianism,
iCivicTribalism, iCivicSlavery, iCivicAgrarianism, iCivicCapitalism, iCivicIndustrialism, iCivicPublicWelfare,
iCivicSubsistence, iCivicGuilds, iCivicMercantilism, iCivicFreeMarket, iCivicCentralPlanning, iCivicEnvironmentalism,
iCivicAnimism, iCivicPantheon, iCivicOrganizedReligion, iCivicScholasticism, iCivicFanaticism, iCivicSecularism,
iCivicMilitia, iCivicMercenaries, iCivicLevyArmies, iCivicStandingArmy, iCivicNavalSupremacy, iCivicMultilateralism) = range(iNumCivics)

#Specialists
iNumSpecialists = 17
(iSpecialistCitizen, iSpecialistPriest, iSpecialistArtist, iSpecialistScientist, iSpecialistMerchant, iSpecialistEngineer, iSpecialistStatesman, iSpecialistSpy,
iSpecialistGreatProphet, iSpecialistGreatArtist, iSpecialistGreatScientist, iSpecialistGreatMerchant, iSpecialistGreatEngineer, iSpecialistGreatStatesman, iSpecialistGreatGeneral, iSpecialistGreatSpy, iSpecialistSlave) = range(iNumSpecialists)

#Stability Levels
iNumStabilityLevels = 5
(iStabilityCollapsing, iStabilityUnstable, iStabilityShaky, iStabilityStable, iStabilitySolid) = range(iNumStabilityLevels)

#Stability Types
iNumStabilityTypes = 5
(iStabilityExpansion, iStabilityEconomy, iStabilityDomestic, iStabilityForeign, iStabilityMilitary) = range(iNumStabilityTypes)

#Stability Parameters
iNumStabilityParameters = 22
(iParameterCorePeriphery, iParameterCoreScore, iParameterPeripheryScore, iParameterRazedCities,									# Expansion
iParameterEconomicGrowth, iParameterTrade, iParameterMercantilism, iParameterCentralPlanning,									# Economy
iParameterHappiness, iParameterCivicCombinations, iParameterCivicsEraTech, iParameterReligion,									# Domestic
iParameterNeighbors, iParameterVassals, iParameterDefensivePacts, iParameterRelations, iParameterAutocracy, iParameterFanaticism, iParameterMultilateralism,	# Foreign
iParameterWarSuccess, iParameterWarWeariness, iParameterBarbarianLosses) = range(iNumStabilityParameters)							# Military

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
(iManhattanProject, iInternet, iSDI, iApolloProgram, iSSCockpit, iSSLifeSupport, iSSStasisChamber, iSSDockingBay,
iSSEngine, iSSCasing, iSSThrusters) = range(iNumProjects)


#Eras

iNumEras = 7
(iAncient, iClassical, iMedieval, iRenaissance, iIndustrial, iModern, iFuture) = range (iNumEras)


#Improvements

iNumImprovements = 27
(iLandWorked, iWaterWorked, iCityRuins, iHut, iFarm, iFishingBoats, iHighSeaFishingBoats, iWhalingBoats, iMine, iWorkshop, iLumbermill, iWindmill, iWatermill, iPlantation, 
iSlavePlantation, iQuarry, iPasture, iCamp, iWell, iOffshorePlatform, iWinery, iCottage, iHamlet, iVillage, iTown, iFort, iForestPreserve) = range(iNumImprovements)

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
iVictoryPolytheism = 10
iVictorySecularism = 11


#leaders

iNumLeaders = 122
(iRamesses, iCleopatra, iBaibars, iNasser, iQinShiHuang, iTaizong, iHongwu, iMao, iSargon, iHammurabi, iVatavelli, iPericles, iAlexander, iGeorge, iAsoka, iChandragupta, iShahuji,
iGandhi, iHiram, iHannibal, iAhoeitu, iCyrus, iDarius, iJuliusCaesar, iAugustus, iRajendra, iKrishnaDevaRaya, iZaraYaqob, iHaileSelassie, iWangKon, iSejong, iPacal,
iJustinian, iBasil, iKammu, iOdaNobunaga, iMeiji, iRagnar, iGustav, iGerhardsen, iHarun, iSaladin, iSongtsen, iLobsangGyatso, iSuryavarman, iDharmasetu, iHayamWuruk,
iSuharto, iRahman, iYaqub, iIsabella, iPhilip, iFranco, iCharlemagne, iLouis, iNapoleon, iDeGaulle, iAlfred, iElizabeth, iVictoria, iChurchill, iBarbarossa,
iCharles, iFrancis, iIvan, iPeter, iCatherine, iNicholas, iStalin, iMansaMusa, iCasimir, iSobieski, iPilsudski, iWalesa, iAfonso, iJoao, iMaria, iHuaynaCapac,
iCastilla, iLorenzo, iCavour, iMussolini, iGenghisKhan, iKublaiKhan, iMontezuma, iTughluq, iAkbar, iBhutto, iMehmed, iSuleiman, iAtaturk, iNaresuan, iMongkut, iMbemba,
iAbbas, iKhomeini, iWillemVanOranje, iWilliam, iFrederick, iBismarck, iHitler, iWashington, iLincoln, iRoosevelt, iSanMartin, iPeron, iSantaAnna, iJuarez, iCardenas, iBolivar,
iPedro, iVargas, iMacDonald, iTrudeau, iBrennus, iAlpArslan, iNativeLeader, iIndependentLeader, iBarbarianLeader, iSittingBull, iBoudica, iAbuBakr) = range(iNumLeaders)

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

(i3000BC, i600AD, i1700AD) = range(3)

# Stability overlay and editor
iNumPlotStabilityTypes = 5
(iCore, iHistorical, iContest, iForeignCore, iAIForbidden) = range(iNumPlotStabilityTypes)
lStabilityColors = ["COLOR_CYAN", "COLOR_GREEN", "COLOR_YELLOW", "COLOR_RED", "COLOR_PLAYER_LIGHT_PURPLE"]
lPresetValues = [3, 20, 90, 200, 500, 700]

iMaxWarValue = 12
lWarMapColors = ["COLOR_RED", "COLOR_PLAYER_ORANGE", "COLOR_YELLOW", "COLOR_GREEN", "COLOR_PLAYER_DARK_GREEN", "COLOR_BLUE"]