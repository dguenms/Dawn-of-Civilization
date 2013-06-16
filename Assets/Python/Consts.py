# Rhye's and Fall of Civilization - Constants


# globals

from CvPythonExtensions import *
gc = CyGlobalContext()

# initialise player variables to player IDs from WBS
iNumPlayers = 41
(iEgypt, iChina, iBabylonia, iGreece, iIndia, iCarthage, iPersia, iRome, iTamils, iEthiopia, iKorea, iMaya, iByzantium, iJapan, 
iVikings, iArabia, iTibet, iKhmer, iIndonesia, iMoors, iSpain, iFrance, iEngland, iHolyRome, iRussia, iMali, iPoland, iPortugal, 
iInca, iItaly, iMongolia, iAztecs, iMughals, iTurkey, iThailand, iCongo, iNetherlands, iGermany, iAmerica, iArgentina, iBrazil) = range(iNumPlayers)

iHolland = iNetherlands
iDelhi = iMughals
#iItaly = iRome
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
iSeljuks = iNumPlayers+4
iNumTotalPlayers = iNumPlayers+5
iBarbarian = iNumPlayers+5
iNumTotalPlayersB = iBarbarian+1

l0Array =       [0 for i in range(iNumPlayers)]
l0ArrayActive = [0 for i in range(iNumPlayers)]
l0ArrayTotal =  [0 for i in range(iNumTotalPlayers)]

lm1Array =      [-1 for i in range(iNumPlayers)]

# civilizations, not players
iNumCivilizations = 54
(iCivAmerica, iCivArabia, iCivAztec, iCivArgentina, iCivBabylonia, iCivBrazil, iCivByzantium, iCivCarthage, iCivCelt, iCivChina, iCivEgypt, iCivEngland, 
iCivEthiopia, iCivFrance, iCivGermany, iCivGreece, iCivHarappa, iCivHolyRoman, iCivInca, iCivIndia, iCivIndonesia, iCivIran, iCivItaly, 
iCivJapan, iCivKhmer, iCivKongo, iCivKorea, iCivMali, iCivMaya, iCivMexico, iCivMongol, iCivMoors, iCivMughals, iCivNativeAmericans, iCivNetherlands,
iCivOttomans, iCivPersia, iCivPoland, iCivPortugal, iCivRome, iCivRussia, iCivSeljuks, iCivSpain, iCivSumeria, iCivTamils, iCivThailand, 
iCivTibet, iCivViking, iCivZulu, iCivIndependent, iCivIndependent2, iCivNative, iCivMinor, iCivBarbarian) = range(iNumCivilizations)

#for Congresses and Victory
lCivGroups = [[iGreece, iRome, iByzantium, iVikings, iMoors, iSpain, iFrance, iEngland, iHolyRome, iRussia, iNetherlands, iItaly, iPoland, iPortugal, iGermany],  #Euros
                [iIndia, iChina, iPersia, iJapan, iTamils, iKorea, iByzantium, iTibet, iKhmer, iIndonesia, iRussia, iMongolia, iMughals, iThailand], #Asian
                [iEgypt, iBabylonia, iPersia, iByzantium, iArabia, iTurkey, iCarthage], #MiddleEastern
                [iEgypt, iGreece, iCarthage, iRome, iByzantium, iMoors], #Mediterranean
                [iEgypt, iCarthage, iEthiopia, iMali, iCongo], #African
                [iMaya, iInca, iAztecs, iAmerica, iArgentina, iBrazil]] #American

lCivStabilityGroups = [[iVikings, iSpain, iFrance, iEngland, iHolyRome, iRussia, iNetherlands, iPoland, iPortugal, iItaly, iGermany],  #Euros
                [iIndia, iChina, iJapan, iKorea, iTibet, iKhmer, iIndonesia, iMongolia, iThailand, iTamils], #Asian
                [iBabylonia, iPersia, iArabia, iTurkey, iMughals], #MiddleEastern
                [iEgypt, iGreece, iCarthage, iRome, iEthiopia, iByzantium, iMoors, iMali, iCongo], #Mediterranean
                [iMaya, iInca, iAztecs, iAmerica, iArgentina, iBrazil]] #American
		
lTechGroups = [[iRome, iGreece, iByzantium, iVikings, iSpain, iFrance, iEngland, iHolyRome, iRussia, iNetherlands, iPoland, iPortugal, iItaly, iGermany, iAmerica, iArgentina, iBrazil], #Europe and NA
	       [iEgypt, iBabylonia, iIndia, iCarthage, iPersia, iEthiopia, iArabia, iMoors, iMali, iTurkey, iMughals, iTamils, iCongo], #Middle East
	       [iChina, iKorea, iJapan, iTibet, iKhmer, iIndonesia, iMongolia, iThailand], #Far East
	       [iMaya, iInca, iAztecs]] #Native America


lCivBioOldWorld = [iEgypt, iIndia, iChina, iBabylonia, iGreece, iPersia, iCarthage, iRome, iJapan, iTamils, \
                   iEthiopia, iKorea, iByzantium, iVikings, iArabia, iTibet, iKhmer, iIndonesia, iMoors, iSpain, iFrance, iEngland, iHolyRome, iRussia, \
                   iNetherlands, iMali, iTurkey, iPoland, iPortugal, iItaly, iMongolia, iAmerica, iMughals, iThailand, iCongo, iGermany, \
                   iIndependent, iIndependent2, iCeltia, iBarbarian]
lCivBioNewWorld = [iMaya, iInca, iAztecs] #, iNative]


#for Victory and the handler
tAmericasTL = (3, 0)
tAmericasBR = (43, 63)

tEuropeTL = (48, 40)
tEuropeBR = (68, 65)
iEuropeTiles = 297

tEasternEuropeTL = (69, 48)
tEasternEuropeBR = (73, 64)
iEasternEuropeTiles = 154

tNorthAmericaTL = (10, 40)
tNorthAmericaBR = (37, 54)
iNorthAmericaTiles = 297

tSouthCentralAmericaTL = (13, 3)
tSouthCentralAmericaBR = (41, 39)


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

#neighbours
lNeighbours = [
[iBabylonia, iGreece, iPersia, iCarthage, iRome, iEthiopia, iByzantium, iArabia, iMoors, iTurkey], #Egypt
[iIndia, iJapan, iKorea, iTibet, iKhmer, iMongolia, iThailand], #China
[iEgypt, iGreece, iPersia, iTurkey, iMongolia, iCarthage, iByzantium], #Babylonia
[iPersia, iCarthage, iRome, iByzantium, iHolyRome, iRussia, iTurkey, iItaly], #Greece
[iChina, iPersia, iTamils, iTibet, iKhmer, iMongolia, iMughals, iThailand], #India
[iEgypt, iGreece, iRome, iSpain, iMali, iPortugal, iBabylonia, iPersia, iArabia, iMoors, iTurkey, iItaly], #Carthage
[iIndia, iBabylonia, iGreece, iByzantium, iTurkey, iMongolia, iCarthage, iMughals], #Persia
[iEgypt, iBabylonia, iGreece, iCarthage, iSpain, iFrance, iHolyRome, iPortugal, iItaly, iGermany], #Rome
[iIndia, iKhmer, iIndonesia, iMughals, iThailand], #Tamils
[iEgypt, iArabia, iMali, iCongo], #Ethiopia
[iChina, iKorea, iMongolia], #Korea
[iSpain, iInca, iAztecs, iAmerica], #Maya
[iEgypt, iBabylonia, iGreece, iPersia, iArabia, iRussia], #Byzantium
[iChina, iKorea, iKhmer, iMongolia, iThailand], #Japan
[iFrance, iEngland, iHolyRome, iRussia, iPoland, iNetherlands, iGermany], #Vikings
[iEgypt, iBabylonia, iPersia, iEthiopia, iByzantium, iTurkey, iCarthage], #Arabia
[iChina, iIndia, iMongolia, iMughals], #Tibet
[iIndia, iChina, iTamils, iJapan, iIndonesia, iThailand], #Khmer
[iIndia, iJapan, iKhmer, iThailand, iTamils], #Indonesia
[iEgypt, iSpain, iPortugal, iMali], #Moors
[iCarthage, iRome, iMoors, iFrance, iEngland, iPortugal], #Spain
[iRome, iVikings, iSpain, iEngland, iHolyRome, iNetherlands, iPortugal, iItaly, iGermany], #France
[iRome, iVikings, iSpain, iFrance, iHolyRome, iNetherlands, iGermany], #England
[iRome, iVikings, iFrance, iEngland, iNetherlands, iItaly, iPoland, iGermany], #Holy Rome
[iPersia, iByzantium, iVikings, iPoland, iTurkey, iMongolia, iGermany], #Russia
[iEgypt, iCarthage, iEthiopia, iMoors, iCongo], #Mali
[iVikings, iHolyRome, iRussia, iGermany], #Poland
[iCarthage, iRome, iSpain, iFrance], #Portugal
[iSpain, iAztecs, iAmerica, iArgentina, iBrazil], #Inca
[iGreece, iCarthage, iRome, iFrance, iHolyRome], #Italy
[iIndia, iChina, iPersia, iJapan, iKorea, iTibet, iRussia, iTurkey], #Mongolia
[iSpain, iInca, iAmerica], #Aztec
[iIndia, iPersia, iTamils, iTibet], #Mughals
[iBabylonia, iGreece, iPersia, iByzantium, iRussia, iMongolia, iCarthage], #Turkey
[iIndia, iChina, iJapan, iIndonesia, iKhmer, iTamils], #Thailand
[iEthiopia, iMali], #Congo
[iVikings, iFrance, iEngland, iHolyRome, iGermany], #Netherlands
[iRome, iVikings, iFrance, iEngland, iHolyRome, iRussia, iPoland, iNetherlands], #Germany
[iJapan, iSpain, iFrance, iEngland, iRussia, iInca, iAztecs], #America
[iSpain, iPortugal, iInca, iBrazil], #Argentina
[iSpain, iPortugal, iInca, iArgentina], #Brazil
]

#for stability hit on spawn
lOlderNeighbours = [
[], #Egypt
[], #China
[], #Babylonia
[iEgypt, iBabylonia], #Greece
[], #India
[iEgypt, iBabylonia], #Carthage
[iEgypt, iBabylonia, iGreece], #Persia
[iEgypt, iGreece, iCarthage], #Rome
[iIndia], #Tamils
[iEgypt], #Ethiopia
[iChina], #Korea
[], #Maya
[iGreece], #Byzantium
[iKorea], #Japan
[], #Vikings
[iEgypt, iPersia, iByzantium], #Arabia
[iChina, iIndia], #Tibet
[iIndia], #Khmer
[iKhmer], #Indonesia
[], #Moors
[iCarthage, iRome], #Spain
[iRome], #France
[], #England
[iGreece, iRome, iVikings], #Holy Rome
[iPersia, iGreece], #Russia
[iCarthage, iEthiopia], #Mali
[iVikings, iHolyRome], #Poland
[iCarthage, iRome], #Portugal
[], #Inca
[iByzantium, iHolyRome], #Italy
[iChina, iJapan, iKorea, iTibet, iKhmer, iRussia], #Mongolia
[iMaya], #Aztec
[iIndia, iIndia, iPersia, iTibet], #Mughals
[iBabylonia, iGreece, iPersia, iByzantium], #Turkey
[iIndia, iChina, iJapan, iKhmer, iIndonesia], #Thailand
[], #Congo
[iRome, iHolyRome], #Netherlands
[iHolyRome, iPoland], #Germany
[iSpain, iFrance, iEngland, iNetherlands, iPortugal, iAztecs, iMaya], #America
[iSpain, iPortugal, iInca], #Argentina
[iSpain, iPortugal, iInca], #Brazil
]

# civ birth dates

# converted to years - edead
tBirth = (
-3000, # 0, #3000BC			# Egypt
-3000, # 0, #3000BC			# China
-3000, # 0, #3000BC			# Babylonia
-1600, # 50, #1600BC			# Greece
-1500, # 0, #3000BC			# India
-1200, # 66, #814BC # Leoreth: 1200 BC	# Carthage
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
1200, # 241, #1195AD			# Aztecs
1206,					# Mughals
1280, # 249, #1280AD (1071AD)		# Turkey
1350,					# Thailand
1390,					# Congo
1580, # 281, #922AD # Leoreth: 1500 AD	# Netherlands
1701,					# Germany
1775, # 346, #1775AD #332 for 1733AD	# America
1810,					# Argentina
1822,					# Brazil
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
1271,					# China
-539,					# Babylonia
-146,					# Greece
600, # end of Gupta Empire		# India
-146,					# Phoenicia
651,					# Persia
476,					# Rome
1200,					# Tamils
960,					# Ethiopia
1255, #Mongol invasion			# Korea
900,					# Maya
1204, #fourth crusade			# Byzantium
2020,					# Japan
1300,					# Vikings
1258,					# Arabia
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
1725,					# Mughals
2020,					# Turkey
2020,					# Thailand
1800,					# Congo
2020,					# Netherlands
2020,					# Germany
2020,					# America
2020,					# Argentina
2020)					# Brazil

# Leoreth: date-triggered respawn for certain civs
tRebirth = (
-1,				# Egypt
-1,				# China
-1,				# Babylonia
-1,	# Byzantium		# Greece
-1,				# India
-1,				# Phoenicia
#1674,	# Maratha Empire
1501,	# Safavid Persia	# Persia
-1, #1167,	# Italy		# Rome
-1,				# Tamils
-1,				# Ethiopia
-1,				# Korea
-1,				# Maya
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
-1)				# Brazil

# Leoreth: ID of the civilization a player is turned into on rebirth
tRebirthCiv = (
-1,		# Egypt
-1,		# China
-1,		# Babylonia
-1,		# Greece
-1,		# India
-1,		# Phoenicia
iCivIran,	# Persia
iCivItaly,	# Rome
-1,		# Tamils
-1,		# Ethiopia
-1,		# Korea
-1,		# Maya
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
-1)		# Brazil

tRebirthPlot = (
-1,		# Egypt
-1,		# China
-1,		# Babylonia
(69,44),	# Greece
(88,36),	# Marathas - Raigad/Mumbai # India
-1,		# Phoenicia
(81,41),	# Safavids - Esfahan # Persia
(59,46),	# Italy - Florence # Rome
-1,		# Tamils
-1,		# Ethiopia
-1,		# Korea
-1,		# Maya
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
(18, 37),	# Mexico - Ciudad de Mexico # Aztecs
-1,		# Mughals
-1,		# Turkey
-1,		# Thailand
-1,		# Congo
-1,		# Netherlands
-1,		# Germany
-1,		# America
-1,		# Argentina
-1)		# Brazil
		
tRebirthArea = (
-1,			# Egypt
-1,			# China
-1,			# Babylonia
((64,45),(74,42)),	# Byzantium - Balkans, Greece, Anatolia, Levant # Greece
((87,28),(94,37)),	# Maratha - Deccan	# India
-1,			# Phoenicia
((78,38),(86,43)),	# Safavids - Azerbaijan, Iran, Afghanistan (no Merv, no Baghdad) # Persia
((57,45),(62,47)),	# Italy - Lombardy and Tuscany without Rome
-1,			# Tamils
-1,			# Ethiopia
-1,			# Korea
-1,			# Maya
-1,			# Byzantium
-1,			# Japan
-1,			# Vikings
-1,			# Arabia
-1,			# Tibet
-1,			# Khmer
-1,			# Indonesia
-1,			# Moors
-1,			# Spain
-1,			# France
-1,			# England
-1,			# Holy Rome
-1,			# Russia
-1,			# Mali
-1,			# Poland
-1,			# Portugal
-1,			# Inca
-1,			# Italy
-1,			# Mongolia
((11, 34), (23, 48)),	# Mexico - Mexico, Yucatan, Texas
-1,			# Mughals
-1,			# Turkey
-1,			# Thailand
-1,			# Congo
-1,			# Netherlands
-1,			# Germany
-1,			# America
-1,			# Argentina
-1)			# Brazil

dRebirthExceptions = {
iAztecs : ((17, 48), (18, 48), (19, 48), (20, 48), (21, 48), (22, 48), (23, 48), (18, 47), (19, 47), (20, 47), (21, 47), (22, 47), (23, 47), (18, 46), (19, 46), (20, 46), (21, 46), (22, 46), (23, 46), (21, 45), (22, 45), (23, 45), (22, 44), (23, 44), (22, 43), (23, 43), (23, 42), (22, 35), (21, 34), (22, 34), (23, 34)),
}

tResurrectionIntervals = (
[(900, 1300), (1800, 2020)], #Egypt
[(1500, 2020)], #China
[], #Babylonia
[(1820, 2020)], #Greece
[(1600, 1800), (1900, 2020)], #India
[], #Carthage
[(220, 650), (1500, 2020)], #Persia
[], #Rome
[], #Tamils
[(1270, 1520), (1850, 1930)], #Ethiopia
[(1800, 2020)], #Korea
[], #Maya
[(1100, 1280)], #Byzantium
[(1800, 2020)], #Japan
[(1520, 2020)], #Vikings
[(1900, 2020)], #Arabia
[],		#Tibet
[(1950, 2020)], #Khmer
[(1900, 2020)], #Indonesia
[],		#Moors
[(1700, 2020)], #Spain
[(1700, 2020)], #France
[(1700, 2020)], #England
[(1800, 2020)], #Holy Rome
[(1280, 1550), (1700, 2020)], #Russia
[(1340, 1590)], #Mali
[(1920, 2020)], #Poland
[(1700, 2020)], #Portugal
[(1800, 1900)], #Inca
[(1850, 2020)], #Italy
[(1910, 2020)], #Mongolia
[], 		#Aztec
[(1940, 2020)], #Mughals
[(1700, 2020)], #Turkey
[(1700, 2020)], #Thailand
[],		#Congo
[(1700, 2020)], #Netherlands
[(1870, 2020)], #Germany
[(1770, 2020)], #America
[(1810, 2020)], #Argentina
[(1820, 2020)], #Brazil
)

tYear = (
("3000 ", "TXT_KEY_BC"),	# Egypt
("3000 ", "TXT_KEY_BC"),	# China
("3000 ", "TXT_KEY_BC"),	# Babylonia
("1600 ", "TXT_KEY_BC"),	# Greece
("1500 ", "TXT_KEY_BC"),	# India
("1200 ", "TXT_KEY_BC"),	# Phoenicia
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
("1822 ", "TXT_KEY_AD"))	# Brazil

# edead: tGoals[iGameSpeed][iCiv][iGoal]
# Leoreth: tGoals[reborn][iGameSpeed][iCiv][iGoal]
tGoals1 = (
( # Marathon
("TXT_KEY_UHV_EGY1_MARATHON", "TXT_KEY_UHV_EGY2_MARATHON", "TXT_KEY_UHV_EGY3_MARATHON"),
("TXT_KEY_UHV_CHI1", "TXT_KEY_UHV_CHI2", "TXT_KEY_UHV_CHI3"),
("TXT_KEY_UHV_BAB1", "TXT_KEY_UHV_BAB2_MARATHON", "TXT_KEY_UHV_BAB3_MARATHON"),
("TXT_KEY_UHV_GRE1", "TXT_KEY_UHV_GRE2_MARATHON", "TXT_KEY_UHV_GRE3_MARATHON"),
("TXT_KEY_UHV_IND1_MARATHON", "TXT_KEY_UHV_IND2", "TXT_KEY_UHV_IND3"),
("TXT_KEY_UHV_CAR1_MARATHON", "TXT_KEY_UHV_CAR2_MARATHON", "TXT_KEY_UHV_CAR3_MARATHON"),
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
("TXT_KEY_UHV_KON1", "TXT_KEY_UHV_KON2_MARATHON", "TXT_KEY_UHV_KON3"),
("TXT_KEY_UHV_HOL1", "TXT_KEY_UHV_HOL2+", "TXT_KEY_UHV_HOL3"),
("TXT_KEY_UHV_GER1", "TXT_KEY_UHV_GER2", "TXT_KEY_UHV_GER3"),
("TXT_KEY_UHV_AME1", "TXT_KEY_UHV_AME2", "TXT_KEY_UHV_AME3"),
("TXT_KEY_UHV_ARG1", "TXT_KEY_UHV_ARG2", "TXT_KEY_UHV_ARG3_MARATHON"),
("TXT_KEY_UHV_BRA1", "TXT_KEY_UHV_BRA2", "TXT_KEY_UHV_BRA3"),
),
( # Epic
("TXT_KEY_UHV_EGY1_EPIC", "TXT_KEY_UHV_EGY2_EPIC", "TXT_KEY_UHV_EGY3_EPIC"),
("TXT_KEY_UHV_CHI1", "TXT_KEY_UHV_CHI2", "TXT_KEY_UHV_CHI3"),
("TXT_KEY_UHV_BAB1", "TXT_KEY_UHV_BAB2_EPIC", "TXT_KEY_UHV_BAB3_EPIC"),
("TXT_KEY_UHV_GRE1", "TXT_KEY_UHV_GRE2_EPIC", "TXT_KEY_UHV_GRE3_EPIC"),
("TXT_KEY_UHV_IND1_EPIC", "TXT_KEY_UHV_IND2", "TXT_KEY_UHV_IND3"),
("TXT_KEY_UHV_CAR1_EPIC", "TXT_KEY_UHV_CAR2_EPIC", "TXT_KEY_UHV_CAR3_EPIC"),
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
("TXT_KEY_UHV_KON1", "TXT_KEY_UHV_KON2_EPIC", "TXT_KEY_UHV_KON3"),
("TXT_KEY_UHV_HOL1", "TXT_KEY_UHV_HOL2+", "TXT_KEY_UHV_HOL3"),
("TXT_KEY_UHV_GER1", "TXT_KEY_UHV_GER2", "TXT_KEY_UHV_GER3"),
("TXT_KEY_UHV_AME1", "TXT_KEY_UHV_AME2", "TXT_KEY_UHV_AME3"),
("TXT_KEY_UHV_ARG1", "TXT_KEY_UHV_ARG2", "TXT_KEY_UHV_ARG3_EPIC"),
("TXT_KEY_UHV_BRA1", "TXT_KEY_UHV_BRA2", "TXT_KEY_UHV_BRA3"),
),
( # Normal
("TXT_KEY_UHV_EGY1", "TXT_KEY_UHV_EGY2", "TXT_KEY_UHV_EGY3"),
("TXT_KEY_UHV_CHI1", "TXT_KEY_UHV_CHI2", "TXT_KEY_UHV_CHI3"),
("TXT_KEY_UHV_BAB1", "TXT_KEY_UHV_BAB2", "TXT_KEY_UHV_BAB3"),
("TXT_KEY_UHV_GRE1", "TXT_KEY_UHV_GRE2", "TXT_KEY_UHV_GRE3"),
("TXT_KEY_UHV_IND1", "TXT_KEY_UHV_IND2", "TXT_KEY_UHV_IND3"),
("TXT_KEY_UHV_CAR1", "TXT_KEY_UHV_CAR2", "TXT_KEY_UHV_CAR3"),
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
("TXT_KEY_UHV_KON1", "TXT_KEY_UHV_KON2", "TXT_KEY_UHV_KON3"),
("TXT_KEY_UHV_HOL1", "TXT_KEY_UHV_HOL2", "TXT_KEY_UHV_HOL3"),
("TXT_KEY_UHV_GER1", "TXT_KEY_UHV_GER2", "TXT_KEY_UHV_GER3"),
("TXT_KEY_UHV_AME1", "TXT_KEY_UHV_AME2", "TXT_KEY_UHV_AME3"),
("TXT_KEY_UHV_ARG1", "TXT_KEY_UHV_ARG2", "TXT_KEY_UHV_ARG3"),
("TXT_KEY_UHV_BRA1", "TXT_KEY_UHV_BRA2", "TXT_KEY_UHV_BRA3"),
)
)

tGoals2 = (
( # Marathon
("TXT_KEY_UHV_EGY1_MARATHON", "TXT_KEY_UHV_EGY2_MARATHON", "TXT_KEY_UHV_EGY3_MARATHON"),
("TXT_KEY_UHV_CHI1", "TXT_KEY_UHV_CHI2", "TXT_KEY_UHV_CHI3"),
("TXT_KEY_UHV_BAB1", "TXT_KEY_UHV_BAB2_NOTURN", "TXT_KEY_UHV_BAB3_NOTURN"),
("TXT_KEY_UHV_GRE1", "TXT_KEY_UHV_GRE2_NOTURN", "TXT_KEY_UHV_GRE3"),
("TXT_KEY_UHV_IND1", "TXT_KEY_UHV_IND2", "TXT_KEY_UHV_IND3"),
("TXT_KEY_UHV_CAR1_NOTURN", "TXT_KEY_UHV_CAR2_NOTURN", "TXT_KEY_UHV_CAR3"),
("TXT_KEY_UHV_IRA1", "TXT_KEY_UHV_IRA2", "TXT_KEY_UHV_IRA3_MARATHON"),
("TXT_KEY_UHV_ITA1", "TXT_KEY_UHV_ITA2", "TXT_KEY_UHV_ITA3"),
("TXT_KEY_UHV_TAM1_MARATHON", "TXT_KEY_UHV_TAM2", "TXT_KEY_UHV_TAM3_MARATHON"),
("TXT_KEY_UHV_ETH1", "TXT_KEY_UHV_ETH2", "TXT_KEY_UHV_ETH3"),
("TXT_KEY_UHV_KOR1", "TXT_KEY_UHV_KOR2", "TXT_KEY_UHV_KOR3"),
("TXT_KEY_UHV_MAY1_NOTURN", "TXT_KEY_UHV_MAY2", "TXT_KEY_UHV_MAY3"),
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
("TXT_KEY_UHV_KON1", "TXT_KEY_UHV_KON2_MARATHON", "TXT_KEY_UHV_KON3"),
("TXT_KEY_UHV_HOL1", "TXT_KEY_UHV_HOL2", "TXT_KEY_UHV_HOL3"),
("TXT_KEY_UHV_GER1", "TXT_KEY_UHV_GER2", "TXT_KEY_UHV_GER3"),
("TXT_KEY_UHV_AME1", "TXT_KEY_UHV_AME2", "TXT_KEY_UHV_AME3"),
("TXT_KEY_UHV_ARG1", "TXT_KEY_UHV_ARG2", "TXT_KEY_UHV_ARG3_EPIC"),
("TXT_KEY_UHV_BRA1", "TXT_KEY_UHV_BRA2", "TXT_KEY_UHV_BRA3")
),
( # Epic
("TXT_KEY_UHV_EGY1_EPIC", "TXT_KEY_UHV_EGY2_EPIC", "TXT_KEY_UHV_EGY3_EPIC"),
("TXT_KEY_UHV_CHI1", "TXT_KEY_UHV_CHI2", "TXT_KEY_UHV_CHI3"),
("TXT_KEY_UHV_BAB1", "TXT_KEY_UHV_BAB2_NOTURN", "TXT_KEY_UHV_BAB3_NOTURN"),
("TXT_KEY_UHV_GRE1", "TXT_KEY_UHV_GRE2_NOTURN", "TXT_KEY_UHV_GRE3"),
("TXT_KEY_UHV_IND1", "TXT_KEY_UHV_IND2", "TXT_KEY_UHV_IND3"),
("TXT_KEY_UHV_CAR1_NOTURN", "TXT_KEY_UHV_CAR2_NOTURN", "TXT_KEY_UHV_CAR3"),
("TXT_KEY_UHV_IRA1", "TXT_KEY_UHV_IRA2", "TXT_KEY_UHV_IRA3_EPIC"),
("TXT_KEY_UHV_ITA1", "TXT_KEY_UHV_ITA2", "TXT_KEY_UHV_ITA3"),
("TXT_KEY_UHV_TAM1_EPIC", "TXT_KEY_UHV_TAM2", "TXT_KEY_UHV_TAM3_EPIC"),
("TXT_KEY_UHV_ETH1", "TXT_KEY_UHV_ETH2", "TXT_KEY_UHV_ETH3"),
("TXT_KEY_UHV_KOR1", "TXT_KEY_UHV_KOR2", "TXT_KEY_UHV_KOR3"),
("TXT_KEY_UHV_MAY1", "TXT_KEY_UHV_MAY2", "TXT_KEY_UHV_MAY3"),
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
("TXT_KEY_UHV_KON1", "TXT_KEY_UHV_KON2_EPIC", "TXT_KEY_UHV_KON3"),
("TXT_KEY_UHV_HOL1", "TXT_KEY_UHV_HOL2", "TXT_KEY_UHV_HOL3"),
("TXT_KEY_UHV_GER1", "TXT_KEY_UHV_GER2", "TXT_KEY_UHV_GER3"),
("TXT_KEY_UHV_AME1", "TXT_KEY_UHV_AME2", "TXT_KEY_UHV_AME3"),
("TXT_KEY_UHV_ARG1", "TXT_KEY_UHV_ARG2", "TXT_KEY_UHV_ARG3_EPIC"),
("TXT_KEY_UHV_BRA1", "TXT_KEY_UHV_BRA2", "TXT_KEY_UHV_BRA3")
),
( # Normal
("TXT_KEY_UHV_EGY1", "TXT_KEY_UHV_EGY2", "TXT_KEY_UHV_EGY3"),
("TXT_KEY_UHV_CHI1", "TXT_KEY_UHV_CHI2", "TXT_KEY_UHV_CHI3"),
("TXT_KEY_UHV_BAB1", "TXT_KEY_UHV_BAB2", "TXT_KEY_UHV_BAB3"),
("TXT_KEY_UHV_GRE1", "TXT_KEY_UHV_GRE2", "TXT_KEY_UHV_GRE3"),
("TXT_KEY_UHV_IND1", "TXT_KEY_UHV_IND2", "TXT_KEY_UHV_IND3"),
("TXT_KEY_UHV_CAR1", "TXT_KEY_UHV_CAR2", "TXT_KEY_UHV_CAR3"),
("TXT_KEY_UHV_IRA1", "TXT_KEY_UHV_IRA2", "TXT_KEY_UHV_IRA3"),
("TXT_KEY_UHV_ITA1", "TXT_KEY_UHV_ITA2", "TXT_KEY_UHV_ITA3"),
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
("TXT_KEY_UHV_MEX1", "TXT_KEY_UHV_MEX2", "TXT_KEY_UHV_MEX3"),
("TXT_KEY_UHV_MUG1", "TXT_KEY_UHV_MUG2", "TXT_KEY_UHV_MUG3"),
("TXT_KEY_UHV_TUR1", "TXT_KEY_UHV_TUR2", "TXT_KEY_UHV_TUR3"),
("TXT_KEY_UHV_THA1", "TXT_KEY_UHV_THA2", "TXT_KEY_UHV_THA3"),
("TXT_KEY_UHV_KON1", "TXT_KEY_UHV_KON2", "TXT_KEY_UHV_KON3"),
("TXT_KEY_UHV_HOL1", "TXT_KEY_UHV_HOL2", "TXT_KEY_UHV_HOL3"),
("TXT_KEY_UHV_GER1", "TXT_KEY_UHV_GER2", "TXT_KEY_UHV_GER3"),
("TXT_KEY_UHV_AME1", "TXT_KEY_UHV_AME2", "TXT_KEY_UHV_AME3"),
("TXT_KEY_UHV_ARG1", "TXT_KEY_UHV_ARG2", "TXT_KEY_UHV_ARG3"),
("TXT_KEY_UHV_BRA1", "TXT_KEY_UHV_BRA2", "TXT_KEY_UHV_BRA3")
)
)

tGoals = (tGoals1, tGoals2)

# Dawn of Man texts
dawnOfMan = {
iEgypt		:	"TXT_KEY_DOM_EGYPT",
iIndia		:	"TXT_KEY_DOM_INDIA",
iChina		:	"TXT_KEY_DOM_CHINA",
iBabylonia	:	"TXT_KEY_DOM_BABYLONIA",
iGreece		:	"TXT_KEY_DOM_GREECE",
iCarthage	:	"TXT_KEY_DOM_PHOENICIA",
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
}

dawnOfManLate = {
iChina		:	"TXT_KEY_DOM_CHINA_LATE",
iJapan		:	"TXT_KEY_DOM_JAPAN_LATE",
iKorea		:	"TXT_KEY_DOM_KOREA_LATE",
iByzantium	:	"TXT_KEY_DOM_BYZANTIUM_LATE",
}


iEurope = gc.getMap().plot(55, 50).getArea()
iAfrica = gc.getMap().plot(72, 29).getArea()
iAsia = gc.getMap().plot(102, 47).getArea()

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
		

# starting locations coordinates
tCapitals = (
((69, 33), #tThebes
#(102, 47), #tBeijing
(100, 44), #Chang'an
(76, 40), #tBabylon
(67, 41), #tAthens
#(90, 40), #tDelhi
(94, 40), #tPataliputra
#(58, 39), #tCarthage
(73, 40), #tSur
(82, 39), #tPersepolis
(60, 44), #tRome
(91, 31), #Thanjavur
(72, 29), #tAksum
(109, 46), #tSeoul
(22, 35), #tTikal
(68, 45), #tConstantinople
(113, 45), #tKyoto
#(61, 62), #tNidaros
(60, 59), #tOslo
(75, 33), #tMecca
(96, 43), #Lhasa
#(102, 34), #tAngkor
(102, 33), #tAngkor
(100, 26), #Palembang
(51, 41), #Cordoba
(52, 44), #tMadrid
(55, 50), #tParis
(53, 54), #tLondon
#(62, 52), #tBerlin
#(63, 49), #tVienna
(59, 50), #Frankfurt
(73, 54), #tMoskow
(53, 31), #tTimbuktu
(65, 51), #Krakow
(49, 43), #tLisboa
(28, 22), #tCuzco
(59, 46), #Florence
(99, 51), #tKarakorum
(18, 37), #tTenochtitlan
(90, 40), #tDelhi
(70, 43), #tSogut ((72, 43), #tKonya  #71?)
(101, 33), #Ayutthaya
(62, 20), #Mbanza Kongo
(57, 53), #tAmsterdam
(62, 52), #Berlin
(27, 46), #tWashington
(34, 11), #Buenos Aires
(41, 18), #Rio de Janeiro
),
((69, 33), #tThebes
(102, 47), #tBeijing
(76, 40), #tBabylon
(67, 41), #tAthens
(90, 40), #tDelhi
#(58, 39), #tCarthage
(73, 40), #tSur
(81, 41), #Esfahan
(60, 44), #tRome
(91, 31), #Thanjavur
(72, 29), #tAksum
(109, 46), #tSeoul
(22, 35), #tTikal
(68, 45), #tConstantinople
(113, 45), #tKyoto
#(61, 62), #tNidaros
(60, 59), #tOslo
(75, 33), #tMecca
(96, 43), #Lhasa
#(102, 34), #tAngkor
(102, 33), #tAngkor
(100, 26), #Palembang
(51, 41), #Cordoba
(52, 44), #tMadrid
(55, 50), #tParis
(53, 54), #tLondon
#(62, 52), #tBerlin
(63, 49), #tVienna
#(59, 50), #Frankfurt
(73, 54), #tMoskow
(53, 31), #tTimbuktu
(65, 51), #Krakow
(49, 43), #tLisboa
(28, 22), #tCuzco
(59, 46), #Florence
(99, 51), #tKarakorum
(18, 37), #tTenochtitlan
(90, 40), #Delhi
(70, 43), #tSogut ((72, 43), #tKonya  #71?)
(101, 33), #Ayutthaya
(62, 20), #Mbanza Kongo
(57, 53), #tAmsterdam
(62, 52), #Berlin
(27, 46), #tWashington
(34, 11), #Buenos Aires
(41, 18), #Rio de Janeiro
)) 

#for minor civs
tReserveCapitals = (
(), 
(), 
(), 
(), 
(), 
(), 
(), 
(), 
(),
(), 
(),
(), 
(), 
(), 
(), 
(), 
(), 
(),
(), 
(), 
(),
(),
(),
(), 
(),
(), 
(),
(), #((49, 42), (49, 44)) #tLisboa
(),
(),
(),
(),
(),
(),
(), 
(), #((57, 52), (56, 52), (58, 53)), #tAmsterdam
(),
(), 
(),
(),
)

#core areas (for RiseAndFall and Victory)

tCoreAreasTL = (
((66, 30), #Egypt
(99, 43), #China 
(75, 38), #Babylonia
(65, 39), #Greece
(87, 33), #India
(71, 39), #Carthage
(79, 37), #Persia
(59, 41), #Rome
(90, 28), #Tamils
(69, 27), #Ethiopia
(107, 45), #Korea
(20, 35), #Maya
(64, 38), #Byzantium
(111, 41), #Japan
(57, 57), #Vikings
(67, 30), #Arabia	73,30
(92, 41), #Tibet
(100, 32), #Khmer
(98, 24), #Indonesia
(51, 37), #Moors
(49, 43), #Spain
(51, 46), #France
(50, 53), #England
(58, 48), #Holy Rome
(67, 50), #Russia
(49, 26), #Mali
(63, 50), #Poland
(44, 42), #Portugal
(26, 20), #Inca
(58, 45), #Italy
(87, 46), #Mongolia
(15, 36), #Aztecs
(86, 38), #Mughals
(69, 41), #Turkey
(100, 32), #Thailand
(61, 19), #Congo
(56, 52), #Holland
(58, 49), #Germany
(25, 43), #America
(31,  9), #Buenos Aires
(36, 14), #Brazil
),
((66, 30), #Egypt
(99, 43), #China 
(75, 38), #Babylonia
(65, 39), #Greece
(87, 33), #India
(71, 39), #Carthage
(79, 37), #Persia
(58, 45), #Rome		# ITALY (now doesn't include southern italy because that apparently causes a crash with Byzantine or independent Naples?)
(90, 28), #Tamils
(69, 27), #Ethiopia
(107, 45), #Korea
(20, 35), #Maya
(64, 41), #Byzantium
(111, 41), #Japan
(57, 57), #Vikings
(73, 30), #Arabia
(92, 41), #Tibet
(100, 32), #Khmer
(98, 24), #Indonesia
(51, 37), #Moors
(49, 43), #Spain
(51, 46), #France
(50, 53), #England
(61, 46), #Holy Rome
(67, 50), #Russia
(49, 26), #Mali
(63, 50), #Poland
(44, 42), #Portugal
(26, 20), #Inca
(58, 45), #Italy
(87, 46), #Mongolia
(12, 33), #Mexico
(86, 37), #Mughals
(69, 41), #Turkey
(100, 32), #Thailand
(61, 19), #Congo
(56, 52), #Holland
(58, 49), #Germany
(25, 43), #America
(31,  9), #Buenos Aires
(36, 14), #Brazil
)) 

tCoreAreasBR = (
((70, 36), #Egypt
(107, 47), #China
(77, 42), #Babylonia
(70, 44), #Greece
(94, 40), #India
(74, 41), #Carthage
(85, 44), #Persia
(63, 47), #Rome
(93, 34), #Tamils
(73, 30), #Ethiopia
(110, 49), #Korea
(23, 37), #Maya
(74, 45), #Byzantium
(116, 49), #Japan
(70, 65), #Vikings
(80, 40), #Arabia	81,39
(98, 45), #Tibet
(103, 36), #Khmer
(107, 31), #Indonesia
(58, 43), #Moors
(53, 46), #Spain
(57, 52), #France
(54, 60), #England   57 without Scotland
(65, 54), #Holy Rome
(74, 57), #Russia
(57, 31), #Mali
(67, 54), #Poland
(50, 44), #Portugal
(29, 24), #Inca
(63, 47), #Italy
(105, 58), #Mongolia
(20, 41), #Aztecs
(94, 43), #Mughals
(77, 48), #Turkey
(103, 36), #Thailand
(65, 22), #Congo
(58, 53), #Holland
(66, 54), #Germany
(32, 50), #America
(36, 13), #Argentina
(43, 28), #Brazil
),
((70, 36), #Egypt
(107, 47), #China
(77, 42), #Babylonia
(70, 44), #Greece
(94, 40), #India
(74, 41), #Carthage
(85, 44), #Persia
(63, 47), #Rome
(93, 34), #Tamils
(73, 30), #Ethiopia
(110, 49), #Korea
(23, 37), #Maya
(74, 45), #Byzantium
(116, 49), #Japan
(70, 65), #Vikings
(81, 39), #Arabia
(98, 45), #Tibet
(103, 36), #Khmer
(107, 31), #Indonesia
(58, 43), #Moors
(53, 46), #Spain
(57, 52), #France
(54, 60), #England   57 without Scotland
(66, 50), #Holy Rome
(74, 57), #Russia
(57, 31), #Mali
(67, 54), #Poland
(50, 44), #Portugal
(29, 24), #Inca
(63, 47), #Italy
(106, 58), #Mongolia
(23, 43), #Mexico
(94, 43), #Mughals
(77, 48), #Turkey
(103, 36), #Thailand
(65, 22), #Congo
(58, 53), #Holland
(66, 54), #Germany
(32, 50), #America
(36, 13), #Argentina
(43, 28), #Brazil
))


tExceptions = (  #for RiseAndFall
((), #Egypt
(), #China
((78, 41), (78, 42)), #Babylonia
(), #Greece
(), #India
(),#(73, 40), (73, 41)), #Carthage
((72, 39), (72, 40), (72, 41), (73, 41), (74, 41), (75, 41), (76, 41), (77, 41), (78, 41), (73, 40), (74, 40), (75, 40), (76, 40), (77, 40), (78, 40), (73, 39), (74, 39), (75, 39), (76, 39), (77, 39), (78, 39), (73, 38), (74, 38), (75, 38), (76, 38), (77, 38), (72, 37), (73, 37), (74, 37), (75, 37), (76, 37), (77, 37), (78, 37)), #Persia
(), #Rome
((90, 33), (90, 34), (91, 34)), #Tamils
(), #Ethiopia
(), #Korea
(), #Maya
(), #Byzantium
(), #Japan
((59, 55), (60, 55), (62, 55), (59, 56), (62, 56), (63, 56)), #Vikings
((82, 34), (73, 40), (75, 40), (71, 36), (72, 37), (67, 30), (68, 30), (69, 30), (70, 30), (71, 30), (72, 30), (72, 31), (72, 32), (71, 32)),  #Arabia
((98, 42),), #Tibet
(), #Khmer
((100, 31), (100, 30), (101, 29)), #Indonesia
((58, 43), (58, 42)), #Moors
((49, 41), (49, 42), (49, 43), (49, 44)), #Spain
((55, 46), (57, 46), (56, 45), (57, 45), (58, 48), (58, 49), (58, 50), (53, 46), (52, 46), (51, 46), (57, 46)), #France
(), #England
((62, 47), (63, 47), (64, 47), (58, 51), (58, 52), (58, 53), (57, 53), (65, 55), (66, 55), (66, 56)),  #Holy Rome
((68, 58), (69, 58), (70, 58), (65, 55), (66, 55), (66, 56)), #Russia
(), #Mali
((63, 50), (64, 50)), #Poland
(), #Portugal
(), #Inca
((63,47), (63,46)), #Italy
((99, 47), (100, 47), (101, 47), (102, 47), (103, 47), (99, 46), (100, 46), (101, 46), (102, 46), (103, 46), (104, 46), (99, 45), (100, 45), (101, 45), (102, 45), (103, 45), (104, 45), (105, 45), (106, 45)), #Mongolia
(), #Aztecs
((92, 43), (93, 42), (93, 43), (94, 42), (94, 43)), #Mughals
((68, 48), (68, 49), (73, 40), (73, 41), (73, 42), (71, 42), (70, 42), (74, 42), (75, 42), (80, 47), (80, 48), (80, 49), (67, 42), (67, 41)), #Turkey
(), #Thailand
(), #Congo
((57, 51), (58, 51)), #Holland
((62, 49), (62, 50), (63, 49), (63, 50), (64, 49), (64, 50), (64, 51), (65, 49), (65, 50), (65, 51), (66, 49), (66, 50), (66, 51), (58, 52), (58, 53)),  #Germany
((25, 48), (25, 49), (26, 48), (27, 49), (27, 50), (28, 50), (29, 50), (30, 50)), #America
((35, 12), (35, 13), (36, 12), (36, 13)), #Argentina
(), #Brazil
),
((), #Egypt
(), #China
((78, 41), (78, 42)), #Babylonia
(), #Greece
(), #India
(),#(73, 40), (73, 41)), #Carthage
(), #Persia
((63,47), (63,46)), #Rome		# ITALY
((90, 33), (90, 34), (91, 34)), #Tamils
(), #Ethiopia
(), #Korea
(), #Maya
(), #Byzantium
(), #Japan
((59, 55), (60, 55), (62, 55), (59, 56), (62, 56), (63, 56)), #Vikings
((82, 34), (73, 40), (75, 40), (71, 36), (72, 37), (67, 30), (68, 30), (69, 30), (70, 30), (71, 30), (72, 30), (72, 31), (72, 32), (71, 32)),  #Arabia
((98, 42),), #Tibet
(), #Khmer
((100, 31), (100, 30), (101, 29)), #Indonesia
((58, 43), (58, 42)), #Moors
((49, 41), (49, 42), (49, 43), (49, 44)), #Spain
((55, 46), (57, 46), (56, 45), (57, 45), (58, 48), (58, 49), (58, 50), (53, 46), (52, 46), (51, 46), (57, 46)), #France
(), #England
(),  #HolyRome
((68, 58), (69, 58), (70, 58), (65, 55), (66, 55), (66, 56)), #Russia
(), #Mali
((63, 50), (64, 50)), #Poland
(), #Portugal
(), #Inca
((63,47), (63,46)), #Italy
((90, 47), (91, 47), (92, 47), (93, 47), (94, 47), (95, 47), (96, 47), (97, 47), (98, 47), (99, 47), (100, 47), (101, 47), (102, 47), (103, 47), (99, 46), (100, 46), (101, 46), (102, 46), (103, 46), (104, 46), (99, 45), (100, 45), (101, 45), (102, 45), (103, 45), (104, 45), (105, 45), (106, 45)), #Mongolia
((19, 40), (19, 41), (20, 41), (19, 42), (20, 42), (21, 42), (23, 42), (18, 43), (19, 43), (20, 43), (21, 43), (22, 43), (23, 43), (21, 33), (22, 33), (23, 33), (22, 34), (23, 34), (22, 35)), #Mexico
((92, 43)), #Mughals
((68, 48), (68, 49), (73, 40), (73, 41), (73, 42), (71, 42), (70, 42), (74, 42), (75, 42), (80, 47), (80, 48), (80, 49)), #Turkey
(), #Thailand
(), #Congo
((57, 51), (58, 51)), #Holland
((62, 49), (62, 50), (63, 49), (63, 50), (64, 49), (64, 50), (64, 51), (65, 49), (65, 50), (65, 51), (66, 49), (66, 50), (66, 51)),  #Germany
((25, 48), (25, 49), (26, 48), (27, 49), (27, 50), (28, 50), (29, 50), (30, 50)), #America
((35, 12), (35, 13), (36, 12), (36, 13)), #Argentina
(), #Brazil
))



#normal areas (for Victory and resurrection)

tNormalAreasTL = (
((65, 30), #Egypt
(99, 39), #China
(74, 38), #Babylonia
(64, 39), #Greece
(87, 28), #India
(72, 39), #Carthage
(79, 37), #Persia
(57, 40), #Rome
(90, 28), #Tamils
(68, 25), #Ethiopia
(108, 45), #Korea
(20, 32), #Maya
(64, 40), #Byzantium
(111, 41), #Japan
(57, 55), #Vikings
(72, 30), #Arabia
(92, 41), #Tibet
(98, 26), #Khmer
(98, 24), #Indonesia
(51, 37), #Moors
(49, 40), #Spain
(51, 46), #France
(50, 53), #England
(58, 48), #Holy Rome
(68, 49), #Russia
(48, 26), #Mali
(63, 50), #Poland
(44, 41), #Portugal
(24, 14), #Inca
(57, 40), #Italy
(92, 48), #Mongolia
(15, 35), #Aztecs
(86, 37), #Mughals
(68, 42), #Turkey
(98, 26), #Thailand
(61, 19), #Congo
(56, 51), #Holland
(59, 48), #Germany
(11, 43), #America
(31,  3), #Argentina
(32, 14), #Brazil
),
((65, 30), #Egypt
(99, 39), #China
(74, 38), #Babylonia
(64, 39), #Greece
(86, 29), #India
(71, 39), #Carthage
(79, 37), #Persia
(57, 40), #Rome
(90, 28), #Tamils
(68, 25), #Ethiopia
(108, 45), #Korea
(20, 32), #Maya
(64, 40), #Byzantium
(111, 41), #Japan
(57, 55), #Vikings
(73, 30), #Arabia
(92, 41), #Tibet
(98, 26), #Khmer
(98, 24), #Indonesia
(51, 37), #Moors
(49, 40), #Spain
(51, 46), #France
(50, 53), #England
(61, 46), #Holy Rome
(68, 49), #Russia
(48, 26), #Mali
(63, 50), #Poland
(44, 41), #Portugal
(24, 14), #Inca
(57, 40), #Italy
(92, 48), #Mongolia
(15, 35), #Aztecs
(86, 37), #Mughals
(68, 42), #Turkey
(98, 26), #Thailand
(61, 19), #Congo
(56, 51), #Holland
(59, 48), #Germany
(11, 43), #America
(31,  3), #Argentina
(32, 14), #Brazil
))

tNormalAreasBR = (
((72, 37), #Egypt
(108, 50), #China
(79, 44), #Babylonia
(68, 44), #Greece
(94, 37), #India
(74, 41), #Carthage
(86, 46), #Persia
(63, 47), #Rome
(93, 34), #Tamils
(77, 30), #Ethiopia
(110, 49), #Korea
(23, 37), #Maya
(72, 45), #Byzantium
(116, 52), #Japan
(67, 65), #Vikings
(82, 38), #Arabia
(98, 45), #Tibet
(103, 37), #Khmer
(113, 31), #Indonesia
(58, 43), #Moors
(55, 46), #Spain
(58, 52), #France
(54, 60), #England
(65, 54), #Holy Rome
(83, 62), #Russia
(60, 33), #Mali
(67, 54), #Poland
(50, 44), #Portugal
(30, 29), #Inca
(63, 47), #Italy
(104, 54), #Mongolia
(20, 40), #Aztecs
(94, 43), #Mughals
(78, 49), #Turkey
(103, 37), #Thailand
(65, 22), #Congo
(58, 53), #Holland
(66, 54), #Germany
(31, 49), #America
(36, 15), #Argentina
(43, 28), #Brazil
),
((72, 37), #Egypt
(108, 50), #China
(79, 44), #Babylonia
(68, 44), #Greece
(97, 42), #India
(74, 41), #Carthage
(86, 46), #Persia
(63, 47), #Rome
(93, 34), #Tamils
(77, 30), #Ethiopia
(110, 49), #Korea
(23, 37), #Maya
(72, 45), #Byzantium
(116, 52), #Japan
(67, 65), #Vikings
(82, 38), #Arabia
(98, 45), #Tibet
(103, 37), #Khmer
(113, 31), #Indonesia
(58, 43), #Moors
(55, 46), #Spain
(58, 52), #France
(54, 60), #England
(66, 50), #Holy Rome
(83, 62), #Russia
(60, 33), #Mali
(67, 54), #Poland
(50, 44), #Portugal
(30, 29), #Inca
(63, 47), #Italy
(104, 54), #Mongolia
(20, 40), #Aztecs
(94, 43), #Mughals
(78, 49), #Turkey
(103, 37), #Thailand
(65, 22), #Congo
(58, 53), #Holland
(66, 54), #Germany
(31, 49), #America
(36, 15), #Argentina
(43, 28), #Brazil
))


tNormalAreasSubtract = (  #for resurrection and stability
(((72, 37), (70, 30), (71, 30), (72, 30)), #Egypt
((99, 49), (100, 49), (101, 49), (99, 50), (100, 50), (101, 50), (102, 50), (100, 39), (101, 39)), #China
(), #Babylonia
(), #Greece
((93, 42), (94, 42), (95, 42), (96, 42)), #India
(), #Carthage
((86, 39), (86, 38), (86, 37)), #Persia
((62, 47), (63, 47), (63, 46)), #Rome
(), #Tamils
((76, 30), (77, 30)), #Ethiopia
(), #Korea
(), #Maya
(), #Byzantium
((111, 52), (112, 52), (111, 51)), #Japan
((65, 55), (66, 55), (67, 55), (66, 56), (67, 56)), #Vikings
((81, 38), (82, 38), (82, 37)),  #Arabia
(), #Tibet
(), #Khmer
(), #Indonesia
(),
((49, 44), (49, 43), (49, 42), (49, 41)), #Spain #bts only
((51, 46), (52, 46), (53, 46), (58, 47), (58, 46), (58, 51), (58, 52), (57, 52)), #France #changed in BTS
(), #England
(),  #Holy Rome
((80, 49), (68, 62), (68, 61), (68, 60), (68, 59)), #Russia
(), #Mali
((63, 50), (64, 50)), #Poland
(), #Portugal
(), #Inca
((62, 47), (63, 47), (63, 46)), #Italy
((92, 52), (92, 53), (92, 54), (93, 54), (94, 54), (100, 48), (101, 48), (102, 48), (103, 48), (104, 48)), #Mongolia
((20, 35)), #Aztecs #bts only
(), #Mughals
(), #Turkey
(), #Thailand
(), #Congo
(), #Holland
(), #Germany
(), #America
((35, 12), (35, 13), (36, 12), (36, 13), (36, 14), (36, 15)), #Argentina
(), #Brazil STILL NEEDS TO BE DONE
),
(((72, 37), (70, 30), (71, 30), (72, 30)), #Egypt
((99, 49), (100, 49), (101, 49), (99, 50), (100, 50), (101, 50), (102, 50)), #China
(), #Babylonia
(), #Greece
((93, 42), (94, 42), (95, 42), (96, 42)), #India
(), #Carthage
((86, 39), (86, 38), (86, 37)), #Persia
((62, 47), (63, 47), (63, 46)), #Rome
(), #Tamils
((76, 30), (77, 30)), #Ethiopia
(), #Maya
(), #Byzantium
((111, 52), (112, 52), (111, 51)), #Japan
((65, 55), (66, 55), (67, 55), (66, 56), (67, 56)), #Vikings
((81, 38), (82, 38), (82, 37)),  #Arabia
(), #Tibet
(), #Khmer
(), #Indonesia
(), #Moors
((49, 44), (49, 43), (49, 42), (49, 41)), #Spain #bts only
((51, 46), (52, 46), (53, 46), (58, 47), (58, 46), (58, 51), (58, 52), (57, 52)), #France #changed in BTS
(), #England
(),  #Holy Rome
((80, 49), (68, 62), (68, 61), (68, 60), (68, 59)), #Russia
(), #Mali
((63, 50), (64, 50)), #Poland
(), #Portugal
(), #Inca
((62, 47), (63, 47), (63, 46)), #Italy
((92, 52), (92, 53), (92, 54), (93, 54), (94, 54), (100, 48), (101, 48), (102, 48), (103, 48), (104, 48)), #Mongolia
((20, 35)), #Aztecs #bts only
(), #Mughals
(), #Turkey
(), #Thailand
(), #Congo
(), #Holland
(), #Germany
(), #America
((35, 12), (35, 13), (36, 12), (36, 13), (36, 14), (36, 15)), #Argentina
(), #Brazil STILL NEEDS TO BE DONE
))

# broader areas coordinates (top left and bottom right) (for RiseAndFall)

tBroaderAreasTL = (
((60, 26), #Egypt
(95, 38), #China
(72, 37), #Babylonia
(62, 39), #Greece
(85, 28), #India
(71, 39), #Carthage
(70, 37), #Persia
(49, 35), #Rome
(90, 28), #Tamils
(67, 21), #Ethiopia
(106, 45), #Korea
(19, 30), #Maya
(58, 34), #Byzantium
(110, 40), #Japan
(57, 55), #Vikings
(64, 30), #Arabia
(92, 41), #Tibet
(97, 25), #Khmer
(98, 24), #Indonesia
(51, 37), #Moors
(49, 38), #Spain
(49, 44), #France
(48, 53), #England
(55, 46), #Holy Rome
(65, 48), #Russia
(48, 21), #Mali
(63, 50), #Poland
(49, 40), #Portugal
(24, 14), #Inca
(57, 47), #Italy
(82, 44), #Mongolia
(14, 32), #Aztecs
(86, 37), #Mughals
(68, 42), #Turkey
(97, 25), #Thailand
(61, 19), #Congo
(56, 51), #Holland
(55, 46), #Germany
(10, 42), #America
(29,  3), #Argentina
(32, 14), #Brazil
),
((60, 26), #Egypt
(95, 38), #China
(72, 37), #Babylonia
(62, 39), #Greece
(85, 28), #India
(71, 39), #Carthage
(70, 37), #Persia
(57, 47), #Rome		# ITALY
(90, 28), #Tamils
(67, 21), #Ethiopia
(106, 45), #Korea
(19, 30), #Maya
(64, 38), #Byzantium
(110, 40), #Japan
(57, 55), #Vikings
(64, 30), #Arabia
(92, 41), #Tibet
(97, 25), #Khmer
(98, 24), #Indonesia
(51, 37), #Moors
(49, 38), #Spain
(49, 44), #France
(48, 53), #England
(61, 46), #Holy Rome
(65, 48), #Russia
(48, 21), #Mali
(63, 50), #Poland
(49, 40), #Portugal
(24, 14), #Inca
(57, 47), #Italy
(82, 44), #Mongolia
(14, 32), #Aztecs
(86, 37), #Mughals
(68, 42), #Turkey
(97, 25), #Thailand
(61, 19), #Congo
(56, 51), #Holland
(55, 46), #Germany
(10, 42), #America
(29,  3), #Argentina
(32, 14), #Brazil
))

tBroaderAreasBR = (
((74, 38), #Egypt
(108, 50), #China
(78, 44), #Babylonia
(77, 47), #Greece
(99, 43), #India
(74, 41), #Carthage
(87, 49), #Persia
(73, 50), #Rome
(93, 34), #Tamils
(77, 30), #Ethiopia
(110, 52), #Korea
(26, 37), #Maya
(74, 45), #Byzantium
(116, 56), #Japan
(71, 65), #Vikings
(85, 44), #Arabia
(98, 45), #Tibet
(105, 39), #Khmer
(113, 31), #Indonesia
(58, 43), #Moors
(55, 46), #Spain
(61, 52), #France
(54, 60), #England
(66, 56), #Holy Rome
(92, 59), #Russia
(67, 32), #Mali
(67, 54), #Poland
(51, 45), #Portugal
(30, 27), #Inca
(65, 47), #Italy
(110, 62), #Mongolia
(24, 43), #Aztecs
(94, 43), #Mughals
(86, 49), #Turkey
(105, 39), #Thailand
(65, 22), #Congo
(58, 53), #Holland
(67, 56), #Germany
(37, 56), #America
(36, 15), #Argentina
(43, 28), #Brazil
),
((74, 38), #Egypt
(108, 50), #China
(78, 44), #Babylonia
(77, 47), #Greece
(99, 43), #India
(74, 41), #Carthage
(87, 49), #Persia
(65, 47), #Rome		# ITALY
(93, 34), #Tamils
(77, 30), #Ethiopia
(110, 52), #Korea
(26, 37), #Maya
(74, 45), #Byzantium
(116, 56), #Japan
(71, 65), #Vikings
(85, 44), #Arabia
(98, 45), #Tibet
(105, 39), #Khmer
(113, 31), #Indonesia
(58, 43), #Moors
(55, 46), #Spain
(61, 52), #France
(54, 60), #England
(66, 50), #Holy Rome
(92, 59), #Russia
(67, 32), #Mali
(67, 54), #Poland
(51, 45), #Portugal
(30, 27), #Inca
(65, 47), #Italy
(110, 62), #Mongolia
(24, 43), #Aztecs
(94, 43), #Mughals
(86, 49), #Turkey
(105, 39), #Thailand
(65, 22), #Congo
(58, 53), #Holland
(67, 56), #Germany
(37, 56), #America
(36, 15), #Argentina
(43, 28), #Brazil
))

#Leoreth: respawn areas and capitals similar to SoI
tRespawnCapitals = (
(69, 35), #Al-Qahira
(102, 47), #Beijing
-1,		# Babylonia
-1,		# Greece
(88, 36), #Mumbai
-1,		# Phoenicia
(81, 41), #Esfahan
-1,		# Rome
-1,
(72, 36), # Addis Ababa
-1,		# Korea
-1,		# Maya
-1,		# Byzantium
(116, 46), #Tokyo
(63, 58), #Stockholm
-1,		# Arabia
-1,		# Tibet
-1,		# Khmer
(104, 25), #Jakarta
-1,		# Moors
-1,		# Spain
-1,		# France
-1,		# England
(63, 49), #Vienna
-1,		# Russia
-1,		# Mali
-1,		# Poland
-1,		# Portugal
-1,		# Inca
(59, 41), #Rome	# Italy
-1,		# Mongolia
-1,		# Aztecs
(85, 37), #Karachi
(68, 45), #Istanbul
-1,		# Thailand
-1,		# Congo
-1,		# Netherlands
-1,		# Germany
-1,		# America
-1, 		# Argentina
-1)		# Brazil

# area flipped on respawn, if -1 normal area is used instead
tRespawnTL = (
(58, 31), #Egypt
(99, 39), #China
-1,		# Babylonia
-1,		# Greece
(88, 29), #India
-1,		# Phoenicia
-1,		# Persia
-1,		# Rome
-1,		# Tamils
-1,		# Ethiopia
-1,		# Korea
-1,		# Maya
(65, 40), #Byzantium
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
-1,		# Aztecs
(85, 37), #Mughals
-1,		# Turkey
-1,		# Thailand
-1,		# Congo
-1,		# Netherlands
-1,		# Germany
-1,		# America
-1, 		# Argentina
-1)		# Brazil

tRespawnBR = (
(71, 39), #Egypt
(107, 47), #China
-1,		# Babylonia
-1,		# Greece
(94, 37), #India
-1,		# Phoenicia
-1,		# Persia
-1,		# Rome
-1,		# Tamils
-1,		# Ethiopia
-1,		# Korea
-1,		# Maya
(69, 46), #Byzantium
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
-1,		# Aztecs
(88, 43), #Mughals
-1,		# Turkey
-1,		# Thailand
-1,		# Congo
-1,		# Netherlands
-1,		# Germany
-1,		# America
-1,		# Argentina
-1)		# Brazil

#Mercenaries. Higher number = less likely to hire
tHire = (
10, #Egypt
30, #China
30, #Babylonia
50, #Greece
30, #India
10, #Carthage
20, #Persia
30, #Rome
30, #Tamils
30, #Ethiopia
60, #Korea
30, #Maya
10, #Byzantium
60, #Japan
60, #Viking
50, #Arabia
90, #Tibet
30, #Khmer
60, #Indonesia
90, #Moors
50, #Spain
50, #France
50, #England
60, #Holy Rome
60, #Russia
30, #Mali
40, #Poland
60, #Portugal
30, #Inca
10, #Italy
70, #Mongolia
30, #Aztec
50, #Mughals
50, #Turkey
30, #Thailand
60, #Congo
10, #Holland
60, #Germany
50, #America
30, #Argentina
50, #Brazil
100,
100,
100,
100,
100) #Barbs



#rnf. Some civs have a double entry, for a higher chance
lEnemyCivsOnSpawn = [
[], #Egypt
[iIndependent,iIndependent2,iIndependent2], #China
[iIndependent,iIndependent2], #Babylonia
[iIndependent,iIndependent2,iBabylonia], #Greece
[], #India
[], #Carthage
[iBabylonia,iBabylonia,iGreece,iCarthage,iCarthage,iIndia,iIndia], #Persia
#[iEgypt,iGreece,iGreece,iCarthage,iCarthage], #Rome
[], # rome for testing
[], #Tamils
[], #Ethiopia
[], #Korea
[], #Maya
[iGreece, iPersia], #Byzantium
[], #Japan
[iRome,iArabia,iSpain,iEngland,iEngland,iFrance,iFrance,iCeltia,iIndependent,iIndependent2], #Vikings
[iEgypt,iEgypt,iEgypt,iBabylonia,iBabylonia,iGreece,iPersia,iCarthage,iRome,iByzantium,iByzantium,iSpain,iFrance,iCeltia,iCeltia,iIndependent,iIndependent2], #Arabia
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
[iIndependent,iIndependent2], #Argentina
[iIndependent,iIndependent2], #Brazil
]

# Leoreth
lTotalWarOnSpawn = [
[], #Egypt
[], #China
[], #Babylonia
[], #Greece
[], #India
[], #Phoenicia
[iBabylonia, iCarthage], #Persia
[iGreece], #Rome
[], #Tamils
[], #Ethiopia
[], #Korea
[], #Maya
[iGreece], #Byzantium
[], #Japan
[], #Vikings
[iEgypt, iBabylonia, iCarthage, iPersia], #Arabia
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
]


#AIWars
tAggressionLevel = (
0, #Egypt
1, #China
1, #Babylonia
2, #Greece
0, #India
0, #Carthage
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
0) #Barbs


#war during rise of new civs
tAIStopBirthThreshold = (
    80, #Egypt
    60, #China
    50, #Babylonia
    50, #Greece #would be 80 but with Turks must be lower
    80, #India
    80, #Carthage
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
60, #Greece
20, #India
30, #Carthage
70, #Persia
65, #Rome
20, #Tamils
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
#    100, #Holland
#    100, #Portugal
100) #Barbs 


#Congresses.
tPatienceThreshold = (
30, #Egypt
30, #China
30, #Babylonia
35, #Greece
50, #India
35, #Carthage
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
100) #Barbs


#RnF Colonists
tMaxColonists = (
0, #Egypt
0, #China
0, #Babylonia
0, #Greece
0, #India
0, #Carthage
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
0) #Brazil


# initialise religion variables to religion indices from XML
iNumReligions = 9
(iJudaism, iChristianity, iOrthodoxy, iIslam, iHinduism, iBuddhism, iConfucianism, iTaoism, iZoroastrianism) = range(iNumReligions)
iProtestantism = iJudaism
iCatholicism = iChristianity

#Persecution preference
tPersecutionPreference = (
(iIslam, iCatholicism, iOrthodoxy, iZoroastrianism, iHinduism, iBuddhism, iTaoism, iConfucianism), # Protestantism
(iIslam, iProtestantism, iOrthodoxy, iZoroastrianism, iHinduism, iBuddhism, iTaoism, iConfucianism), # Catholicism
(iIslam, iProtestantism, iCatholicism, iZoroastrianism, iHinduism, iBuddhism, iTaoism, iConfucianism), # Orthodoxy
(iHinduism, iProtestantism, iCatholicism, iOrthodoxy, iTaoism, iConfucianism, iZoroastrianism, iBuddhism), # Islam
(iIslam, iCatholicism, iProtestantism, iOrthodoxy, iZoroastrianism, iTaoism, iConfucianism, iBuddhism), # Hinduism
(iCatholicism, iProtestantism, iOrthodoxy, iZoroastrianism, iTaoism, iIslam, iConfucianism, iHinduism), # Buddhism
(iIslam, iCatholicism, iProtestantism, iOrthodoxy, iZoroastrianism, iHinduism, iBuddhism, iTaoism), # Confucianism
(iIslam, iCatholicism, iProtestantism, iOrthodoxy, iZoroastrianism, iHinduism, iBuddhism, iConfucianism), # Taoism
(iIslam, iCatholicism, iProtestantism, iOrthodoxy, iBuddhism, iHinduism, iTaoism, iConfucianism), # Zoroastrianism
)


# initialise tech variables to unit indices from XML

iNumTechs = 92
(iMysticism, iMeditation, iPolytheism, iPriesthood, iMonotheism, iMonarchy, iLiterature, iCodeOfLaws, iDrama, iFeudalism,
iTheology, iMusic, iCivilService, iGuilds, iDivineRight, iPatronage, iNationalism, iMilitaryTradition, iConstitution, iLiberalism,
iDemocracy, iCorporation, iFascism, iCommunism, iMassMedia, iEcology, iFishing, iTheWheel, iAgriculture, iPottery,
iAesthetics, iSailing, iWriting, iMathematics, iAlphabet, iCalendar, iCurrency, iPhilosophy, iPaper, iBanking, iEducation,
iPrintingPress, iEconomics, iAstronomy, iChemistry, iScientificMethod, iPhysics, iBiology, iMedicine, iElectricity,
iCombustion, iFission, iFlight, iAdvancedFlight, iPlastics, iComposites, iStealth, iGenetics, iFiberOptics, iFusion,
iHunting, iMining, iArchery, iMasonry, iAnimalHusbandry, iBronzeWorking, iHorsebackRiding, iIronWorking, iMetalCasting,
iCompass, iConstruction, iMachinery, iEngineering, iOptics, iGunpowder, iReplaceableParts, iMilitaryScience, iRifling,
iSteamPower, iSteel, iAssemblyLine, iRailroad, iArtillery, iIndustrialism, iRadio, iRefrigeration, iSuperconfuctors,
iComputers, iLaser, iRocketry, iSatellites, iRobotics) = range(iNumTechs)

iUtopia = iCommunism

iFutureTech = iNumTechs
iNumTechsFuture = iNumTechs+1


# initialise unit variables to unit indices from XML

iNumUnits = 149
(iLion, iBear, iPanther, iWolf, iSettler, iWorker, iIndianFastWorker, iBrazilianLenhador, iScout, iExplorer, iSpy, iJewishMissionary,
iChristianMissionary, iOrthodoxMissionary, iIslamicMissionary, iHinduMissionary, iBuddhistMissionary, iConfucianMissionary, iTaoistMissionary,
iZoroastrianMissionary, iWarrior, iIncanQuechua, iHarappanMilitia, iSwordsman, iAztecJaguar, iCelticGallicWarrior, iRomePraetorian,
iAxeman, iGreekPhalanx, iSumerianVulture, iNativeAmericaDogSoldier, iMaceman, iJapanSamurai, iVikingBerserker, iIranianQizilbash, iKongoPombos, 
iSpearman, iZuluImpi, iMayaHolkan, iPikeman, iHolyRomanLandsknecht, iMusketman, iFrenchMusketeer, iOttomanJanissary,
iEthiopianOromoWarrior, iIroquoisMohawk, iRifleman, iEnglishRedcoat, iAmericanMinuteman, iGrenadier, iAtInfantry, iInfantry, iSamInfantry, iMobileSam,
iMarine, iAmericanNavySeal, iParatrooper, iMechanizedInfantry, iArcher, iMaliSkirmisher, iBabylonBowman, iNubianMedjay, iLongbowman,
iCrossbowman, iChinaChokonu, iChariot, iEgyptWarChariot, iCelticCidainh, iHittiteHuluganni, iPersiaImmortal, iHorseArcher, iCarthageNumidianCavalry, iKushanAsvaka,
iMongolKeshik, iTibetanKhampa, iKnight, iArabiaCamelarcher, iByzantineCataphract, iSeljukGhulamWarrior, iThaiChangSuek, iMandeFarari, iSpanishConquistador, 
iCuirassier,  iMoorishCamelGunner, iPolishWingedHussar, iSiouxMountedBrave, iCavalry, iRussiaCossack, iMexicoRurales, iArgentineGrenadierCavalry, 
iWarElephant, iKhmerBallistaElephant, iCarthaginianWarElephant, iTank, iGermanPanzer, iModernArmor, iGunship, iCatapult, iKoreanHwacha, iTrebuchet, 
iBombard, iMughalSiegeElephant, iCannon, iFrenchHeavyCannon, iMachineGun, iArtillery, iMobileArtillery, iWorkboat, iGalley, iTrireme, iCaravel, 
iPortugalCarrack, iTamilDharani, iGalleon, iNetherlandsOostindievaarder, iPrivateer, iIndonesianOrangLaut, iFrigate, iShipOfTheLine, iIronclad, iTransport, 
iDestroyer, iBattleship, iMissileCruiser, iStealthDestroyer, iSubmarine, iAttackSubmarine, iCarrier, iAirship, iFighter, iJetFighter, iBomber,
iStealthBomber, iGuidedMissile, iTacticalNuke, iIcbm, iProphet, iArtist, iScientist, iMerchant, iEngineer, iGreatGeneral, iGreatSpy,
iBireme, iBersagliere, iLevy, iSlave, iNativeSlave, iAztecSlave) = range(iNumUnits)

iCongoPombos = iKongoPombos
iCamelArcher = iArabiaCamelarcher
iConquistador = iSpanishConquistador
iWorkBoat = iWorkboat
iHeavySwordsman = iMaceman
iEthiopianAskari = iEthiopianOromoWarrior

# initialise bonuses variables to bonuses IDs from WBS
iNumBonuses = 39
(iAluminium, iCoal, iCopper, iHorse, iIron, iMarble, iOil, iStone, iUranium, iBanana, iClam, iCorn, iCow, iCrab,
iDeer, iFish, iPig, iRice, iSheep, iWheat, iDye, iFur, iGems, iGold, iIncense, iIvory, iSilk, iSilver, iSpices,
iSugar, iWine, iWhales, iSoccer, iSongs, iMovies, iCotton, iCoffee, iTea, iTobacco) = range(iNumBonuses)

#Buildings (update Persian UHV every time this is changed)

iNumBuildings = 202
(iPalace, iGreatPalace, iForbiddenPalace, iWalls, iCelticDun, iCastle, iSpanishCitadel, iIncanTambo, iBarracks, iZuluIkhanda, iStable,
iMongolGer, iBunker, iBombShelter, iGranary, iIncanTerrace, iAqueduct, iOttomanHammam, iKhmerBaray, iIndianStepwell, iMoorishNoria, iHarappanBath,
iHospital, iRecyclingCenter, iLighthouse, iVikingTradingPost, iHarbor, iCustomHouse, iPortugalFeitoria, iDrydock, iAirport,
iForge, iMaliMint, iFactory, iGermanAssemblyPlant, iCoalPlant, iJapaneseShalePlant, iHydroPlant, iNuclearPlant,
iIndustrialPark, iObelisk, iEgyptianObelisk, iEthiopianStele, iNativeAmericaTotem, iIndonesianCandi, iPublicTransportation, iAcademy,
iLibrary, iArabianMadrassa, iChineseTaixue, iThaiHoTrai, iTamilSangam, iUniversity, iKoreanSeowon, iTibetanGompa, iObservatory, iLaboratory, 
iRussianResearchInstitute, iTheatre, iFrenchSalon, iByzantineHippodrome, iChinesePavillion, iColosseum, iGreekOdeon, iMayaBallCourt,
iBabylonGarden, iMexicoCharreada, iBroadcastTower, iMarket, iRomanForum, iPersianApothecary, iIranianCaravanserai, iKongoMbwadi, iPhoenicianGlassmaker, 
iGrocer, iBrazilianFazenda, iBank, iEnglishStockExchange, iSupermarket, iAmericanMall, iArgentineRefrigerationPlant, iCourthouse, iAztecSacrificialAltar, 
iHolyRomanRathaus, iSumerianZiggurat, iPolishSejmik, iJail,  iIndianMausoleum, iLevee, iNetherlandsDike, iIntelligenceAgency, iNationalSecurity, 
iJewishTemple, iJewishCathedral, iJewishMonastery, iJewishShrine, iChristianTemple, iChristianCathedral, iChristianMonastery, iChristianShrine, 
iOrthodoxTemple, iOrthodoxCathedral, iOrthodoxMonastery, iOrthodoxShrine, iIslamicTemple, iIslamicCathedral,
iIslamicMonastery, iIslamicShrine, iHinduTemple, iHinduCathedral, iHinduMonastery, iHinduShrine, iBuddhistTemple, 
iBuddhistCathedral, iBuddhistMonastery, iBuddhistShrine, iConfucianTemple, iConfucianCathedral, iConfucianMonastery,
iConfucianShrine, iTaoistTemple, iTaoistCathedral, iTaoistMonastery, iTaoistShrine, iZoroastrianTemple, iZoroastrianCathedral,
iZoroastrianMonastery, iZoroastrianShrine, iFlavianAmphitheatre, iTriumphalArch, iGlobeTheatre, iNationalPark, iNationalGallery,
iChannelTunnel, iWallStreet, iIronWorks, iTradingCompany, iIberianTradingCompany, iMtRushmore, iRedCross, iInterpol, iPyramid,
iStonehenge, iGreatLibrary, iGreatLighthouse, iHangingGarden, iColossus, iOracle, iParthenon, iAngkorWat,
iTempleOfKukulkan, iSistineChapel, iSpiralMinaret, iNotreDame, iTajMahal, iKremlin, iEiffelTower, iStatueOfLiberty,
iWembley, iGraceland, iHollywood, iGreatDam, iPentagon, iUnitedNations, iSpaceElevator, iMilitaryAcademy, iArtemis,
iSankore, iGreatWall, iStatueOfZeus, iMausoleumOfMaussollos, iCristoRedentor, iShwedagonPaya, iMoaiStatues, iApostolicPalace,
iLeaningTower, iOlympicPark, iTempleOfSalomon, iIshtarGate, iTheodosianWalls, iTerracottaArmy, iMezquita, iDomeOfTheRock,
iTopkapiPalace, iBrandenburgGate, iSanMarcoBasilica, iWestminster, iItalianArtStudio, iBorobudur, iKhajuraho,
iHimejiCastle, iPorcelainTower, iHarmandirSahib, iBlueMosque, iRedFort, iVersailles, iTrafalgarSquare, iEmpireState,
iGrandCanal, iFloatingGardens, iLubyanka, iMachuPicchu) = range(iNumBuildings)

iSummerPalace = iGreatPalace
iHeroicEpic = iFlavianAmphitheatre
iNationalEpic = iTriumphalArch
iHermitage = iNationalGallery 
iScotlandYard = iInterpol
iChichenItza = iTempleOfKukulkan
iBroadway = iWembley
iRocknroll = iGraceland
iGreatCothon = iMoaiStatues
iThreeGorgesDam = iGreatDam

iPaganTemple = iObelisk

iTemple = iJewishTemple #generic
iCathedral = iJewishCathedral #generic
iMonastery = iJewishMonastery #generic
iShrine = iJewishShrine #generic

iPlague = iNumBuildings
iNumBuildingsPlague = iNumBuildings+1

iNumBuildingsEmbassy = iNumBuildingsPlague+iNumPlayers
(iEgyEmbassy, iChiEmbassy, iBabEmbassy, iGreEmbassy, iIndEmbassy, iCarEmbassy, iPerEmbassy, iRomEmbassy, iTamEmbassy, iEthEmbassy, 
iKorEmbassy, iMayEmbassy, iByzEmbassy, iJapEmbassy, iVikEmbassy, iAraEmbassy, iTibEmbassy, iKhmEmbassy, iInoEmbassy, iMooEmbassy, iSpaEmbassy,
iFraEmbassy, iEngEmbassy, HreEmbassy, iRusEmbassy, iMalEmbassy, iPolEmbassy, iPorEmbassy, iIncEmbassy, iItaEmbassy, iMonEmbassy, 
iAztEmbassy, iMugEmbassy, iTurEmbassy, iThaEmbassy, iConEmbassy, iHolEmbassy, iGerEmbassy, iAmeEmbassy, iArgEmbassy, iBraEmbassy) = range(iNumBuildingsPlague, iNumBuildingsPlague+iNumPlayers)

#Civics
iNumCivics = 36
(iTyranny, iDynasticism, iCityStates, iTheocracy, iAutocracy, iRepublic,
iDirectRule, iVassalage, iAbsolutism, iRepresentation, iSupremeCouncil, iUniversalSuffrage,
iTribalism, iAgrarianism, iUrbanization, iCapitalism, iTotalitarianism, iEgalitarianism,
iSelfSufficiency, iForcedLabor, iMercantilism, iFreeMarket, iStateProperty, iEnvironmentalism,
iAnimism, iPantheon, iOrganizedReligion, iScholasticism, iFanaticism, iSecularism,
iSubjugation, iViceroyalty, iResettlement, iOccupation, iImperialism, iCommonwealth) = range(iNumCivics)

#Stability Display
iNumStabilityTypes = 44
(iStabilityDiplomacy, iStabilityNeighbor, iStabilityVassal, iStabilityImperialism, iStabilityContacts, iStabilityExpansion, iStabilityOuterExpansion,
iStabilityOccupiedCore, iStabilityCivics, iStabilityCivicEra, iStabilityCivicCities, iStabilityCivicCap, iStabilityCivicTech, iStabilityForeignCoreCities,
iStabilityCityHappiness, iStabilityCityCivics, iStabilityCityCulture, iStabilityCityTotal, iStabilityTrade, iStabilityEconomy, iStabilityHappiness,
iStabilityEconomyExtra, iStabilityGreatDepression, iStabilityForeignGreatDepression, iStabilityPostCommunism, iStabilityDemocracyTransition, 
iStabilityNumCities, iStabilityCombat, iStabilityCombatExtra, iStabilityAnarchy, iStabilityGoldenAge, iStabilityFall, iStabilityBase, iStabilityNormalization,
iStabilityCitiesBuilt, iStabilityCitiesLost, iStabilityCitiesConquered, iStabilityCitiesRazed, iStabilityTech, iStabilityBuildings,
iStabilityReligion, iStabilityDifficulty, iStabilityCap, iStabilityHit) = range(iNumStabilityTypes)

#Regions
iNumRegions = 38
(rBritain, rIberia, rItaly, rBalkans, rEurope, rScandinavia, rRussia, rAnatolia, rMesopotamia, rArabia, rEgypt, rMaghreb,
rPersia, rIndia, rDeccan, rIndochina, rIndonesia, rChina, rKorea, rJapan, rManchuria, rTibet, rCentralAsia, rSiberia,
rAustralia, rOceania, rEthiopia, rWestAfrica, rSouthAfrica, rCanada, rAlaska, rUnitedStates, rCaribbean, rMesoamerica,
rBrazil, rArgentina, rPeru, rColombia) = range(iNumRegions)

lNewWorld = [rAustralia, rOceania, rCanada, rAlaska, rUnitedStates, rCaribbean, rMesoamerica, rBrazil, rArgentina, rPeru, rColombia]

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

iNumProjects = 12
(iManhattanProject, iTheInternet, iSDI, iApolloProgram, iSSCasing, iSSThrusters, iSSEngine, iSSDockingBay,
iSSCockpit, iSSLifeSupport, iSSStasisChamber, iPersecutionProject) = range(iNumProjects)


#Eras

iNumEras = 7
(iAncient, iClassical, iMedieval, iRenaissance, iIndustrial, iModern, iFuture) = range (iNumEras)


#Improvements

iNumImprovements = 26
(iLandWorked, iWaterWorked, iCityRuins, iHut, iFarm, iFishingBoats, iWhalingBoats, iMine, iWorkshop, iLumbermill, iWindmill, iWatermill, iPlantation, 
iSlavePlantation, iQuarry, iPasture, iCamp, iWell, iOffshorePlatform, iWinery, iCottage, iHamlet, iVillage, iTown, iFort, iForestPreserve) = range(iNumImprovements)

#feature & terrain

iSeaIce = 0
iJungle = 1
iOasis = 2
iFloodPlains = 3
iForest = 4
iFallout = 5
iMud = 6

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

iSwamp = 36 #bonus


#Stability Parameters

iParCities3 = 0
iParCitiesE = 1
iParCivics3 = 2
iParCivics1 = 3
iParCivicsE = 4
iParDiplomacy3 = 5
iParDiplomacyE = 6
iParEconomy3 = 7
iParEconomy1 = 8
iParEconomyE = 9
iParExpansion3 = 10
iParExpansion1 = 11
iParExpansionE = 12
iNumStabilityParameters = 13

#Plague
iImmunity = 20


#leaders

iNumLeaders = 109
(iLeaderBarbarian, iAlexander, iAsoka, iAugustus, iBismarck, iBoudica, iBrennus, iCatherine, iCharlemagne, iChurchill,
iCyrus, iDarius, iDeGaulle, iElizabeth, iFrederick, iGandhi, iGenghisKhan, iGilgamesh, iHammurabi, iHannibal, iHatshepsut,
iHuaynaCapac, iIsabella, iJoao, iJuliusCaesar, iJustinian, iKublaiKhan, iLincoln, iLouis, iMansaMusa, iMao,
iMehmed, iMontezuma, iNapoleon, iPacal, iPericles, iPeter, iQinShiHuang, iRamesses, iRagnar, iFranklinRoosevelt,
iSaladin, iShaka, iSittingBull, iStalin, iSuleiman, iSuryavarman, iTokugawa, iVictoria, iWangKon, iWashington, iWillemVanOranje, 
iZaraYaqob, iJimmu, iMeiji, iAkbar, iHiram, iHaileSelassie, iGustav, iAbuBakr, iMongkut, iElishat,
iPhilip, iBarbarossa, iCharles, iFrancis, iYaroslav, iAfonso, iAtaturk, iMaria, iHitler, iFranco, iNicholas, iCixi,
iChiangKaishek, iCavour, iAbbas, iKhomeini, iTaizong, iHongwu, iDharmasetu, iHayamWuruk, iSuharto, iShivaji,
iNaresuan, iAlpArslan, iBaibars, iNasser, iAlfred, iChandragupta, iTughluq, iBasil, iRahman, iRajendra, iLobsangGyatso,
iSobieski, iVatavelli, iMbemba, iHarun, iSongtsen, iCasimir, iYaqub, iLorenzo, iSantaAnna, iJuarez, iCardenas, iDomPedro, 
iSanMartin, iPeron) = range(iNumLeaders)

iCleopatra = iHatshepsut
iSargon = iGilgamesh

resurrectionLeaders = {
	iChina : iHongwu,
	iIndia : iShivaji,
	iEgypt : iBaibars,
}

rebirthLeaders = {
	#iRome : iCavour,
	iPersia : iAbbas,
	iAztecs : iJuarez,
}

tIsActiveOnLateStart = (
0, 	# Egypt
1,	# China
0,	# Babylonia
0,	# Greece
0,	# India
0,	# Phoenicia
0,	# Persia
0,	# Rome
0,	# Tamils
0,	# Ethiopia
1,	# Korea
0,	# Maya
1,	# Byzantium
1,	# Japan
1,	# Vikings
1,	# Arabia
1,	# Tibet
1,	# Khmer
1,	# Indonesia
1,	# Moors
1,	# Spain
1,	# France
1,	# England
1,	# Holy Rome
1,	# Russia
1,	# Mali
1,	# Poland
1,	# Portugal
1,	# Inca
1,	# Italy
1,	# Mongolia
1,	# Aztecs
1,	# Mughals
1,	# Turkey
1,	# Thailand
1,	# Congo
1,	# Netherlands
1,	# Germany
1,	# America
1,	# Argentina
1,	# Brazil
1,
1,
1,
1)

tTradingCompanyPlotLists = (
[(109, 33)], #Spain
[(89, 33), (90, 33), (91, 33), (92, 33), (89, 32), (90, 32), (91, 32), (90, 31), (91, 31), (90, 30), (91, 29)], #France
[(88, 36), (88, 35), (88, 34), (89, 34), (89, 33), (89, 32), (90, 32), (90, 31), (90, 30), (91, 29), (91, 31), (91, 32), (91, 33), (92, 33), (92, 34), (93, 34), (93, 35), (94, 35), (94, 36), (94, 37)], #England
[(82, 34), (89, 33), (90, 31), (101, 29), (105, 39), (93, 28), (71, 17), (69, 13), (54, 26), (62, 20)], #Portugal
[(99, 28), (99, 27), (100, 27), (100, 26), (101, 26), (104, 25), (105, 25), (106, 25), (107, 24), (104, 27), (105, 27), (106, 27), (104, 28), (106, 28), (105, 29), (106, 29)] #Netherlands
)

lSecondaryCivs = [iTamils, iTibet, iMoors, iPoland, iCongo]
